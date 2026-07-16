#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_film_plane_mechanism.py
Moveable film plane mechanism — engineering drawings (7 sheets)
OPTION A — RIGID PLANE: a fixed-size rigid rectangle whose ANGLE changes. The 4 corners ride
SLIDE-AND-CLAMP corners (acetal skates on 304 U-channel + UHMW-pad cross-slides) moved by hand in COORDINATED PAIRS —
single-axis tilt (top vs bottom) or swing (left vs right); limited combined; NO compound twist
(a rigid plane cannot warp). A pinhole has infinite depth of field, so this is scene control,
not focus: push each corner into position, then lock the cam clamp. Each corner connects through
a single Ruland US12-6-6-SS U-joint (2 axes, twist-locked) — no leadscrews, no handwheels.

Sheet 1 — Plan view (top-down): 4-corner rail layout, example configs
Sheet 2 — Elevations: side elevation (tilt) + plan cross-section (swing)
Sheet 3 — Corner carriage detail: acetal skate on U-channel + capture sections + cross-slide + U-joint
Sheet 4 — Rail mounting & transport drop-in: left split (stub + removable + bridge) · right flanged · stub clamp
Sheet 5 — Movement specification table & BOM
Sheet 6 — Muslin clamp detail: suspension chain + cam-lever spring clamp
Sheet 7 — System schematic: four-corner frame front elevation
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc

from tbs_constants import FP_X_L, FP_X_R, FP_Y, FP_Y_MIN, FP_W, FP_H, PH_X as PH_X_C, MAX_TILT_DEG, MAX_SWING_DEG, DIAGRAMS_DIR, FP_ANGLE_LEG, FP_ANGLE_T, CLAMP_SPACING, CLAMP_BASE_W, CLAMP_BASE_H, CLAMP_BASE_T, CLAMP_LEVER_L, CLAMP_JAW_W, CLAMP_JAW_H, CLAMP_JAW_T, CLAMP_OPEN_GAP, CLAMP_SPRING_F, CLAMP_N_TOTAL, BRACE_Z_BOT, BRACE_Z_TOP, C_WID, WALL_T, IBC_WBKT_PLATE_W, IBC_WBKT_SEAT_PROJ, IBC_WBKT_SEAT_T, DRUM_CY, DRUM_R, DRUM_CX, DRUM_D
from tbs_title_block import title_block
from tbs_drawing import (leader, draw_notes, draw_dim_h, draw_dim_v,
                         draw_rect, draw_circle, hatch_rect, reset_label_registry)

# ── Palette (white engineering style) ────────────────────────────────────────
BG      = "#FFFFFF"   # white background
GRID    = "#FFFFFF"   # container interior (white)
STRUCT  = "#B0B0B8"   # steel section fill (walls)
STRUCT2 = "#C8D8E8"   # aluminum / secondary structure
DIM     = "#404040"   # dimension lines and text (dark grey)
ANNO    = "#1A1A1A"   # annotation text (near black)
WHITE   = "#1A1A1A"   # outlines / text (was white-on-dark; now dark-on-white)
C_FLAT  = "#2060A0"   # flat position line (blue)
C_T1    = "#1A7A1A"   # tilt config (dark green)
C_T2    = "#B07010"   # swing config (amber)
C_T3    = "#CC2020"   # combined tilt+swing config (red)
RAIL    = "#5A3E00"   # rail (dark brown-gold — dark enough for white text labels)
MECH    = "#2A6B2A"   # mechanism/carriage (dark green — dark enough for white text)
PINHOLE = "#CC6600"   # pinhole aperture (orange, visible on white)

# ── Corner-detail palette (ported from the retired generate_corner_detail.py) ──
# Sheets 3 (corner detail) & 4 (U-joint sections) use this richer, color-coded set.
OUT     = "#1A1A1A"   # outlines / bold text
C_STEEL = "#B0B0B8"   # steel section fill
C_CAR   = "#C04010"   # depth carriage (red)
C_TILT  = "#2E8B57"   # vertical (tilt) slide — green
C_SWING = "#7B5EA7"   # horizontal (swing) slide — purple
C_UJ    = "#C8D8E8"   # U-joint body (light blue)
C_PIN   = "#B07010"   # pins / set screws (gold)
C_FRAME = "#8FB0C8"   # film-frame angle
C_PANEL = "#1F3B66"   # film-plane panel ghost
C_CLAMP = "#3A3A40"   # cam-clamp body
C_POLY  = "#C9B78F"   # self-lube UHMW pad (tan)
C_ACET  = "#ECE7DA"   # acetal roller (natural off-white)
LBL_BG  = dict(fc="white", ec="none", alpha=0.85, pad=1)

# ── Container dimensions (mm) ─────────────────────────────────────────────────
L = 5893   # interior length (film plane spans this direction)
W = 2362   # interior width = optical axis = focal length
H = 2388   # interior height
from tbs_constants import WALL_T
from tbs_constants import DIAGRAM_DPI

# Carriage travel limits (100mm clearance each end)
D_NEAR = 100
D_FAR  = W - 100   # = 2262
D_CTR  = (D_NEAR + D_FAR) / 2   # = 1181 — mid-rail; Option A rotates the plane about here

# ── Option A configs (angle-based) — the rigid plane rotates about its centre ──
# (name, tilt_deg, swing_deg, colour, linestyle). The corner depths/positions are
# DERIVED from the rigid rotation (see rigid_corners3d), foreshortening rather than
# stretching. Combined tilt+swing stays well inside the rails (no C7 twist).
CONFIGS = [
    ("Flat  0°",            0.0,  0.0,  C_FLAT, "-"),
    ("Tilt  20°",          20.0,  0.0,  C_T1,   "--"),
    ("Swing 14°",           0.0, 14.0,  C_T2,   "-."),
    ("Tilt+Swing\n(limited)", 14.0, 10.0, C_T3,   ":"),
]

FONT = {"fontfamily": "monospace"}

# ── Geometry helpers ──────────────────────────────────────────────────────────
RAIL_X_L = FP_X_L       # left rail X position (mm) — tracks FP_X_L from constants
RAIL_X_R = FP_X_R       # right rail X position (mm) — tracks FP_X_R from constants
RAIL_W   = 60           # rail width in plan view

# ── LEFT-rail transport drop-in (Sheet 4). These MIRROR generate_corner_gimbal_model.py; promote
# both to tbs_constants at the FP_W/FP_H cascade so 2D + 3D single-source them (see TODO). ──
from tbs_constants import PIVOT_YD, PIVOT_POST_OD, RAIL_OFF_BOT, WALKWAY_H
LEFT_CUT_YD = 2090      # cut Yd on the X150 rail = the panel-swing-envelope edge; stub = C_WID−2090 = 272mm
SPLICE_YD   = 260       # length splice at the PINHOLE end (removable = 6 ft stock + 260mm)

# ── Option A rigid-plane geometry ────────────────────────────────────────────
# The film plane is a FIXED-SIZE rigid rectangle that rotates about its CENTRE
# (axis tilt / axis swing). A corner-depth difference Δd maps to the angle by
# asin (not the old stretching-model atan), and the projected edge FORESHORTENS
# (the corners move in Z for tilt, in X for swing) — it never grows. The plane is
# illustrated about the rail-travel centre (mid-rail depth) so the symmetric
# rotation fits inside the container; the film back-focuses along the rail.
CX_PLANE = (RAIL_X_L + RAIL_X_R) / 2     # plane centre X (width)


def tilt_edge(tilt_deg, d_c):
    """Rigid axis-tilt about the plane centre. Returns ((d_top,z_top),(d_bot,z_bot))
    in the side elevation (X=depth, Y=height). Edge length stays FP_H (foreshortens
    in Z); the cross-slide takes up H/2·(1−cos t) at each corner."""
    t = np.radians(tilt_deg); hh = FP_H / 2; zc = FP_H / 2
    return ((d_c - hh * np.sin(t), zc + hh * np.cos(t)),
            (d_c + hh * np.sin(t), zc - hh * np.cos(t)))


def swing_edge(swing_deg, d_c):
    """Rigid axis-swing about the plane centre. Returns ((x_L,d_L),(x_R,d_R)) in
    plan (X=length, Y=depth). Edge length stays FP_W (foreshortens in X)."""
    s = np.radians(swing_deg); hw = FP_W / 2
    return ((CX_PLANE - hw * np.cos(s), d_c - hw * np.sin(s)),
            (CX_PLANE + hw * np.cos(s), d_c + hw * np.sin(s)))


def rigid_corners3d(tilt_deg, swing_deg, d_c=D_CTR):
    """The four rigid-plane corners {cid:(x, y, z)} for tilt (about the X/width axis)
    then swing (about the Z/height axis), centred at (CX_PLANE, d_c, FP_H/2).
    x=length, y=optical depth, z=height. Edge lengths are preserved (no stretch)."""
    t = np.radians(tilt_deg); s = np.radians(swing_deg); zc = FP_H / 2
    out = {}
    for cid, (sw, sh) in (("TL", (-1, 1)), ("TR", (1, 1)),
                          ("BL", (-1, -1)), ("BR", (1, -1))):
        w = sw * FP_W / 2; h = sh * FP_H / 2
        x1, y1, z1 = w, -h * np.sin(t), h * np.cos(t)      # tilt about X
        x2 = x1 * np.cos(s) - y1 * np.sin(s)               # swing about Z
        y2 = x1 * np.sin(s) + y1 * np.cos(s)
        out[cid] = (CX_PLANE + x2, d_c + y2, zc + z1)
    return out


# ── Rail-end-flange / wall-seat drawing helpers (each rail end is flanged + wall-plated) ──
# The RIGHT rails are flanged wall-to-wall; the LEFT rails are a transport drop-in (Sheet 4).
# Each seat = a back-plate on the wall + a seat projecting in that the rail end rests on.
def draw_brace_portal(ax, color, *, lw=1.4, alpha=0.9, z=6):
    """Front elevation (X-Z): a wall-seat saddle back-plate at each of the 4 rail-end
    corners (near + far walls project to the same X-Z here)."""
    pw = IBC_WBKT_PLATE_W
    for xv in (RAIL_X_L, RAIL_X_R):
        for zc in (BRACE_Z_BOT, BRACE_Z_TOP):
            ax.add_patch(Rectangle((xv - pw / 2, zc - pw / 2), pw, pw,
                                   fc=color, ec=WHITE, lw=lw, alpha=alpha, zorder=z))


def draw_brace_portal_yd_z(ax, color, *, lw=1.4, alpha=0.9, z=6):
    """Side elevation (Yd-Z): a wall-seat saddle at each wall (Yd 0 + Yd C_WID) at both
    rail heights — a back-plate on the wall + a seat projecting into the container the
    rail end rests on. X-axis of ax = optical depth (Yd), Y-axis = height (Z)."""
    proj, st = IBC_WBKT_SEAT_PROJ, IBC_WBKT_SEAT_T
    pw = IBC_WBKT_PLATE_W
    for wall_yd, din in ((0, 1), (C_WID, -1)):
        for zc in (BRACE_Z_BOT, BRACE_Z_TOP):
            px = wall_yd if din > 0 else wall_yd - 8
            ax.add_patch(Rectangle((px, zc - pw / 2), 8, pw,           # back-plate
                                   fc=color, ec=WHITE, lw=lw, alpha=alpha, zorder=z))
            sy = min(wall_yd, wall_yd + din * proj)
            ax.add_patch(Rectangle((sy, zc - st), proj, st,           # seat (rail rests on it)
                                   fc=color, ec=WHITE, lw=lw, alpha=alpha, zorder=z + 1))


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — PLAN VIEW (top-down)
# X = container length (left→right, 0→L)
# Y = optical axis depth (0=pinhole wall → W=far wall)
# In this view TILT (height difference) is invisible; SWING is visible as diagonal.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    PAD = 500
    ax.set_xlim(-PAD, L + 1400)
    ax.set_ylim(-1150, W + 750)
    ax.set_aspect("equal")
    ax.axis("off")

    # Container outline
    ax.add_patch(Rectangle((0, 0), L, W, fc=GRID, ec=WHITE, lw=1.8, zorder=2))

    # Wall hatching (structural ribs every 457mm)
    for x in np.arange(80, L, 457):
        ax.plot([x, x], [0, W], color=STRUCT2, lw=0.4, alpha=0.35, zorder=3)

    # Pinhole wall (y=0)
    ax.add_patch(Rectangle((0, -WALL_T), L, WALL_T, fc=STRUCT2, ec=WHITE, lw=1.5, zorder=4))
    ax.text(L/2, -WALL_T/2 - 125, "PINHOLE WALL  (20ft LONG SIDE)",
            color=WHITE, fontsize=7.5, ha="center", va="center", **FONT, zorder=5)

    # Far wall (y=W)
    ax.add_patch(Rectangle((0, W), L, WALL_T, fc=STRUCT, ec=WHITE, lw=1.0, zorder=4))
    ax.text(L/2, W + WALL_T/2, "FAR WALL", color=DIM, fontsize=7,
            ha="center", va="center", **FONT, zorder=5)

    # End walls
    for xw in [(-WALL_T, -WALL_T, WALL_T, W+2*WALL_T), (L, -WALL_T, WALL_T, W+2*WALL_T)]:
        ax.add_patch(Rectangle((xw[0], xw[1]), xw[2], xw[3],
                               fc=STRUCT, ec=WHITE, lw=1.0, zorder=4))

    # Pinhole (X=2399mm, centered on the film plane)
    ph_x = PH_X_C
    ax.add_patch(Circle((ph_x, 0), 60, fc=PINHOLE, ec=WHITE, lw=1.5, zorder=6))
    ax.add_patch(Circle((ph_x, 0), 20, fc=BG, ec=WHITE, lw=1.0, zorder=7))
    ax.text(ph_x + 130, 75, f"PINHOLE  X={ph_x}mm  Ø2.17mm", color=PINHOLE, fontsize=7, **FONT)

    # ── 4 RAILS — one at each corner (Option A: rigid plane, coordinated pairs) ──────────────────────────────
    # Left rails: at X=RAIL_X_L (ceiling = label TL/BL, floor = label TL/BL)
    # Right rails: at X=RAIL_X_R (ceiling = label TR/BR, floor = label TR/BR)
    # In plan view both ceiling and floor rails project to same X position.
    # We show them slightly offset for clarity.
    for (rx, label_side) in [(RAIL_X_L, "LEFT"), (RAIL_X_R, "RIGHT")]:
        # Ceiling rail (slightly inward)
        rx_ceil = rx - RAIL_W//2 - 5
        ax.add_patch(Rectangle((rx_ceil, 0), RAIL_W*0.8, C_WID,   # rev11: span wall-to-wall
                               fc=RAIL, ec=WHITE, lw=1.0, zorder=5, alpha=0.85))
        # Floor rail (slightly outward)
        rx_floor = rx + 5
        ax.add_patch(Rectangle((rx_floor, 0), RAIL_W*0.8, C_WID,
                               fc=RAIL, ec=WHITE, lw=1.0, zorder=5, alpha=0.65))
        # Labels — 45° leaders outward from rail midpoint
        rail_mid_y = D_NEAR + (D_FAR - D_NEAR) * 0.8
        ldr_off = 150
        if label_side == "LEFT":
            # Leaders go left
            ax.annotate(f"CEILING RAIL  ({label_side})",
                        xy=(rx_ceil + RAIL_W * 0.4, rail_mid_y + 200),
                        xytext=(rx_ceil - ldr_off, rail_mid_y + 200 + ldr_off),
                        fontsize=6.5, color=RAIL, ha="right", va="bottom", **FONT,
                        arrowprops=dict(arrowstyle="-", color=RAIL, lw=0.8),
                        zorder=15)
            ax.annotate(f"FLOOR RAIL  ({label_side})",
                        xy=(rx_floor + RAIL_W * 0.2, rail_mid_y - 200),
                        xytext=(rx_floor - ldr_off, rail_mid_y - ldr_off),
                        fontsize=6.5, color=RAIL, ha="right", va="top", **FONT,
                        arrowprops=dict(arrowstyle="-", color=RAIL, lw=0.8),
                        zorder=15)
        else:
            # Leaders go right
            ax.annotate(f"CEILING RAIL  ({label_side})",
                        xy=(rx_ceil + RAIL_W * 0.4, rail_mid_y + 200),
                        xytext=(rx_ceil + ldr_off, rail_mid_y + 200 + ldr_off),
                        fontsize=6.5, color=RAIL, ha="left", va="bottom", **FONT,
                        arrowprops=dict(arrowstyle="-", color=RAIL, lw=0.8),
                        zorder=15)
            ax.annotate(f"FLOOR RAIL  ({label_side})",
                        xy=(rx_floor + RAIL_W * 0.2, rail_mid_y - 200),
                        xytext=(rx_floor + ldr_off, rail_mid_y - ldr_off),
                        fontsize=6.5, color=RAIL, ha="left", va="top", **FONT,
                        arrowprops=dict(arrowstyle="-", color=RAIL, lw=0.8),
                        zorder=15)
        # Rail end stops
        for ry in [D_NEAR, D_FAR]:
            for rx_ in [rx_ceil, rx_floor]:
                ax.add_patch(Rectangle((rx_-15, ry-12), RAIL_W*0.8+30, 24,
                                       fc=WHITE, ec=WHITE, lw=0.5, zorder=6))

    # ── RAIL END FLANGES + WALL PLATES — plan view (each rail end seated at the wall) ──
    # Each rail end lands on an IBC-style wall-seat saddle at the near (Yd0) + far
    # (Yd C_WID) walls; the seat projects IBC_WBKT_SEAT_PROJ into the container.
    pw, proj = IBC_WBKT_PLATE_W, IBC_WBKT_SEAT_PROJ
    for rx in (RAIL_X_L, RAIL_X_R):
        for wall_yd, din in ((0, 1), (C_WID, -1)):
            sy = min(wall_yd, wall_yd + din * proj)
            ax.add_patch(Rectangle((rx - pw / 2, sy), pw, proj,
                                   fc=STRUCT, ec=WHITE, lw=1.2, alpha=0.8, zorder=6))
    leader(ax, RAIL_X_L, proj,
           RAIL_X_L + 920, proj + 200,
           "U-CHANNEL END FLANGE + WALL PLATE\nRIGHT rails flanged wall-to-wall;\nLEFT rails = transport drop-in (Sheet 4)",
           color=STRUCT, ha="center", fs=6.5, font=FONT)
    # rev12: the bottom-right (BR) rail ends share a combined corner plate with
    # the right walkway right beam (replaces the 2 BR saddles).
    leader(ax, RAIL_X_R, proj,
           RAIL_X_R - 700, proj + 200,
           "BR END flanges also anchor the\nright walkway beam (shared plate)",
           color=STRUCT, ha="center", fs=6.5, font=FONT)

    # Travel dim — on the INNER (right) side of the left rail (the outer side overlaps the drum ghost)
    tr_x = RAIL_X_L + RAIL_W + 50
    tr_tick = 15
    ax.annotate("", xy=(tr_x, D_FAR-20),
                xytext=(tr_x, D_NEAR+20),
                arrowprops=dict(arrowstyle="<->", color=WHITE, lw=0.8, mutation_scale=5))
    ax.plot([tr_x - tr_tick, tr_x + tr_tick], [D_NEAR+20, D_NEAR+20], color=WHITE, lw=0.6)
    ax.plot([tr_x - tr_tick, tr_x + tr_tick], [D_FAR-20, D_FAR-20], color=WHITE, lw=0.6)
    ax.text(RAIL_X_L + RAIL_W + 160, (D_NEAR+D_FAR) * 0.6,
            f"{D_FAR-D_NEAR}\nmm\ntravel",
            color=WHITE, fontsize=6.5, ha="center", va="center", **FONT)

    # Corner labels
    for (cx, cy, lbl) in [
        (RAIL_X_L, D_FAR,  "TL"),
        (RAIL_X_R, D_FAR,  "TR"),
        (RAIL_X_L, D_NEAR, "BL"),
        (RAIL_X_R, D_NEAR, "BR"),
    ]:
        ax.text(cx, cy + 60, lbl, color=ANNO, fontsize=8, ha="center",
                fontweight="bold", **FONT, zorder=9)

    # ── FILM PLANE POSITIONS — rigid plane projected to plan for each config ──
    # Option A: the rigid plane rotates about its centre. SWING foreshortens the
    # X-span (corners move inboard of the fixed rails) and shifts left/right corners
    # in depth; TILT is hidden here (height axis is into the page). The carriage
    # stays on the rail; an X cross-slide bridges to the (foreshortened) corner.
    order = ["TL", "TR", "BR", "BL"]
    for i, (name, tilt_deg, swing_deg, col, ls) in enumerate(CONFIGS):
        lw = 2.2 if i == 0 else 1.8
        alpha = 1.0 if i == 0 else 0.88
        z = 8 + i
        C = rigid_corners3d(tilt_deg, swing_deg)

        xs = [C[c][0] for c in order] + [C["TL"][0]]
        ys = [C[c][1] for c in order] + [C["TL"][1]]
        ax.plot(xs, ys, color=col, lw=lw, ls=ls, alpha=alpha, zorder=z,
                solid_capstyle="round")
        # carriages on the fixed rails + X cross-slide bridge to each corner
        for c in order:
            cxc, cyc = C[c][0], C[c][1]
            rail_x = RAIL_X_L if c in ("TL", "BL") else RAIL_X_R
            ax.add_patch(Circle((rail_x, cyc), 55, fc=col, ec=WHITE, lw=0.7,
                                alpha=0.55, zorder=z))
            if abs(rail_x - cxc) > 8:
                ax.plot([rail_x, cxc], [cyc, cyc], color=col, lw=1.0,
                        alpha=0.5, zorder=z)
        # inline legend label on the right
        ly = (D_NEAR + D_FAR)/2 - i*220 + 400
        ax.text(L + 200, ly, name.replace("\n", " "),
                color=col, fontsize=7, va="center", **FONT, zorder=10)
        ax.plot([L+50, L+180], [ly, ly], color=col, lw=2.0, ls=ls, zorder=10)

    # ── DRUM FOOTPRINT — ghost circle for light-trap drum ─────────────────────
    # Drum is a vertical cylinder at X=DRUM_CX=0, Yd=DRUM_CY=1181, radius=DRUM_R=450
    # (rev8: Ø900 housed door). In this plan view it appears as a circle at (DRUM_CX, DRUM_CY).
    C_DRUM = "#C8A860"   # amber-gold ghost for drum footprint
    ax.add_patch(Circle((DRUM_CX, DRUM_CY), DRUM_R,
                        fc=C_DRUM, ec=C_DRUM, lw=1.2, alpha=0.18, zorder=4,
                        linestyle="--"))
    ax.add_patch(Circle((DRUM_CX, DRUM_CY), DRUM_R,
                        fc="none", ec=C_DRUM, lw=1.2, alpha=0.55, zorder=4,
                        linestyle="--"))
    ax.text(DRUM_CX, DRUM_CY, f"LIGHT-TRAP\nDRUM\n(Ø{DRUM_D}mm)",
            color=C_DRUM, fontsize=6, ha="center", va="center", **FONT, zorder=5,
            alpha=0.75)

    # The drum is offset clear of the X=150 rail (via the hinge-panel punch-out bay),
    # so the LEFT RAIL is continuous IN FILM MODE — no gap at the drum. (It still lifts
    # out at the transport cut for folding — Sheet 4.)
    leader(ax, RAIL_X_L, DRUM_CY,
           RAIL_X_L - 600, DRUM_CY + 250,
           "LEFT RAIL — continuous in FILM MODE\n(drum offset out via panel bay, no drum gap);\nlifts out for TRANSPORT (Sheet 4)",
           color=RAIL, ha="right", fs=6.5, font=FONT)

    # ── Annotations ───────────────────────────────────────────────────────────
    # Swing annotation arrow
    ax.annotate("SWING moves\nthis edge", xy=(RAIL_X_R, 800), xytext=(RAIL_X_R+400, 700),
                color=C_T2, fontsize=6.5, **FONT,
                arrowprops=dict(arrowstyle="-|>", color=C_T2, lw=0.8, mutation_scale=5),
                ha="left")
    ax.annotate("TILT moves\nboth rails\nat same end",
                xy=(RAIL_X_L, (800+D_FAR)/2-800), xytext=(RAIL_X_L-750, (800+D_FAR)/2-800),
                color=C_T1, fontsize=6.5, **FONT,
                arrowprops=dict(arrowstyle="-|>", color=C_T1, lw=0.8, mutation_scale=5),
                ha="right")

    # Dims
    draw_dim_h(ax, 0, L, W+150, f"INTERIOR LENGTH  {L}mm  (19 ft 4 in)",
               offset=35, color=DIM, fs=7.5, font=FONT)
    draw_dim_v(ax, L+950, 0, W, f"OPTICAL AXIS {W}mm  (7 ft 9 in)",
               offset=35, color=DIM, right=True, font=FONT)
    draw_dim_h(ax, 0, RAIL_X_L, -350, f"{RAIL_X_L}mm\n(left end zone)",
               color=DIM, fs=6.5, above=False, offset=45, font=FONT)
    draw_dim_h(ax, RAIL_X_L, RAIL_X_R, -350, f"Rail span  {RAIL_X_R-RAIL_X_L}mm",
               color=RAIL, fs=6.5, above=False, offset=45, font=FONT)
    draw_dim_h(ax, RAIL_X_R, L, -350, f"{L-RAIL_X_R}mm\n(right end zone)",
               color=DIM, fs=6.5, above=False, offset=45, font=FONT)

    ax.text(L/2, W+580, "SHEET 1 — PLAN VIEW  (TOP DOWN, LOOKING AT CONTAINER FLOOR)",
            color=WHITE, fontsize=9, ha="center", fontweight="bold", **FONT)
    ax.text(L/2, W+470,
            "4 CORNER SLIDE-AND-CLAMP CARRIAGES (acetal skates on 304 U-channel + UHMW-pad cross-slides, RIGID PLANE, COORDINATED PAIRS)  ·  TILT = CEILING vs FLOOR  ·  SWING = LEFT vs RIGHT",
            color=DIM, fontsize=7, ha="center", **FONT)
    ax.text(L/2, W+370,
            "IN THIS VIEW: SWING IS VISIBLE AS DIAGONAL  ·  TILT IS HIDDEN (HEIGHT AXIS = INTO PAGE)",
            color=DIM, fontsize=6.5, ha="center", **FONT)

    # Legend box — right side, above title block
    leg_x = L + 200
    leg_y = -250
    ax.text(leg_x + 500, leg_y + 160, "LEGEND", color=WHITE,
            fontsize=8, fontweight="bold", ha="center", **FONT)
    for i, (name, tilt_deg, swing_deg, col, ls) in enumerate(CONFIGS):
        ly = leg_y - i * 160
        ax.plot([leg_x, leg_x + 400], [ly, ly], color=col, lw=2.0, ls=ls)
        ang_str = f"tilt={tilt_deg:g}°  swing={swing_deg:g}°"
        ax.text(leg_x + 440, ly, f"{name.replace(chr(10), ' ')}\n  {ang_str}",
                color=col, fontsize=6, va="center", **FONT)

    # Title block
    title_block(ax, "SHEET 1 OF 7",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="Plan view — 4-corner rail layout",
                scale_note="Proportional (mm)",
                doc_id="TBS-FM01 · Film Plane Mechanism",
                height=0.05)

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet1.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet1.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — TWO ELEVATION VIEWS
# Left panel:  SIDE ELEVATION (section through container centerline)
#              X = optical axis depth, Y = height → shows TILT
# Right panel: PLAN CROSS-SECTION AT CEILING HEIGHT
#              X = container length, Y = optical axis depth → shows SWING
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():
    fig = plt.figure(figsize=(18, 11))
    fig.patch.set_facecolor(BG)

    ax_tilt  = fig.add_axes([0.03, 0.12, 0.44, 0.80])
    ax_swing = fig.add_axes([0.53, 0.12, 0.44, 0.80])
    for ax in [ax_tilt, ax_swing]:
        ax.set_facecolor(BG)
        ax.axis("off")

    # ── LEFT PANEL: SIDE ELEVATION — TILT ─────────────────────────────────────
    ax = ax_tilt
    PADX, PADY = 350, 250
    ax.set_xlim(-PADX, W + PADX)
    ax.set_ylim(-PADY, H + PADY + 80)
    ax.set_aspect("equal")

    # Container walls
    ax.add_patch(Rectangle((-WALL_T, -WALL_T), WALL_T, H+2*WALL_T,
                           fc=STRUCT2, ec=WHITE, lw=2.0, zorder=4))
    ax.add_patch(Rectangle((W, -WALL_T), WALL_T, H+2*WALL_T,
                           fc=STRUCT, ec=WHITE, lw=1.5, zorder=4))
    ax.add_patch(Rectangle((-WALL_T, -WALL_T), W+2*WALL_T, WALL_T,
                           fc=STRUCT, ec=WHITE, lw=1.5, zorder=4))
    ax.add_patch(Rectangle((-WALL_T, H), W+2*WALL_T, WALL_T,
                           fc=STRUCT, ec=WHITE, lw=1.5, zorder=4))
    ax.add_patch(Rectangle((0, 0), W, H, fc=GRID, ec="none", zorder=2))

    ax.text(-WALL_T/2-100, H/2, "PINHOLE\nWALL",
            color=WHITE, fontsize=6.5, ha="center", va="center",
            rotation=90, **FONT, zorder=5)
    ax.text(W+WALL_T/2+100, H/2, "FAR\nWALL",
            color=DIM, fontsize=6.5, ha="center", va="center",
            rotation=90, **FONT, zorder=5)

    # Rails — span wall-to-wall (saddle-to-saddle), rev11
    RAIL_H = 28
    ax.add_patch(Rectangle((0, 0), C_WID, RAIL_H,
                           fc=RAIL, ec=WHITE, lw=0.8, zorder=5, alpha=0.9))
    ax.text(W/2, RAIL_H/2, "FLOOR DEPTH RAIL  3×1.5 304 U-channel + acetal skate  ×2  (BL  +  BR — roll, cam-clamp, moved as a pair)",
            color=BG, fontsize=5.5, ha="center", va="center", **FONT, zorder=6)
    ax.add_patch(Rectangle((0, H-RAIL_H), C_WID, RAIL_H,
                           fc=RAIL, ec=WHITE, lw=0.8, zorder=5, alpha=0.9))
    ax.text(W/2, H-RAIL_H/2, "CEILING DEPTH RAIL  3×1.5 304 U-channel + acetal skate  ×2  (TL  +  TR — roll, cam-clamp, moved as a pair)",
            color=BG, fontsize=5.5, ha="center", va="center", **FONT, zorder=6)

    # ── RAIL END FLANGES / WALL SEATS — side elevation (Yd on X-axis, Z on Y-axis) ──
    # A seat at each wall (Yd0 + Yd C_WID) at both rail heights: back-plate on the
    # wall + a seat projecting in that the rail end rests on (replaces the brace cage).
    # rev12: the bottom-right (BR) ends sit on the combined corner plate shared with
    # the right walkway (not a standalone saddle).
    draw_brace_portal_yd_z(ax_tilt, STRUCT, lw=1.2, alpha=0.65, z=4)
    leader(ax_tilt, IBC_WBKT_SEAT_PROJ / 2, BRACE_Z_TOP,
           IBC_WBKT_SEAT_PROJ / 2 - 180, BRACE_Z_TOP + 130,
           "U-CHANNEL END FLANGE + WALL PLATE\nRIGHT rail flanged wall-to-wall;\nLEFT rail = transport drop-in (Sheet 4)",
           color=STRUCT, ha="right", fs=6.5, font=FONT)

    CARRIAGE_W = 80
    CARRIAGE_H = 55
    PH_Y = H / 2

    # Tilt configs: use TL for top, BL for bottom (left-side section)
    # Option A: rigid AXIS tilt about the plane centre (mid-rail depth D_CTR). The
    # plane edge stays length FP_H and FORESHORTENS in Z; the carriage stays on the
    # rail and a Z cross-slide bridges the H/2·(1−cos t) gap to the corner.
    tilt_configs = [
        ("Flat  0°",  0.0,  C_FLAT, "-"),
        ("Tilt 20°", 20.0,  C_T1,   "--"),
        ("Tilt 40°", 40.0,  C_T3,   ":"),
    ]

    for i, (name, tdeg, col, ls) in enumerate(tilt_configs):
        lw = 2.6 if i == 0 else 2.0
        alpha = 1.0 if i == 0 else 0.88
        zord = 10 + i
        (d_top, z_top), (d_bot, z_bot) = tilt_edge(tdeg, D_CTR)

        # ceiling carriage (on top rail) + Z cross-slide down to the top corner
        ax.add_patch(Rectangle((d_top - CARRIAGE_W/2, H - RAIL_H - CARRIAGE_H),
                               CARRIAGE_W, CARRIAGE_H, fc=col, ec=WHITE, lw=0.8,
                               alpha=0.45, zorder=zord))
        ax.text(d_top, H - RAIL_H - CARRIAGE_H/2, "T", color=col, fontsize=5.5,
                ha="center", va="center", **FONT, zorder=zord+1)
        ax.plot([d_top, d_top], [H - RAIL_H, z_top], color=col, lw=1.6,
                alpha=0.7, zorder=zord)
        # floor carriage (on bottom rail) + Z cross-slide up to the bottom corner
        ax.add_patch(Rectangle((d_bot - CARRIAGE_W/2, RAIL_H),
                               CARRIAGE_W, CARRIAGE_H, fc=col, ec=WHITE, lw=0.8,
                               alpha=0.45, zorder=zord))
        ax.text(d_bot, RAIL_H + CARRIAGE_H/2, "B", color=col, fontsize=5.5,
                ha="center", va="center", **FONT, zorder=zord+1)
        ax.plot([d_bot, d_bot], [RAIL_H, z_bot], color=col, lw=1.6,
                alpha=0.7, zorder=zord)
        # rigid (foreshortened) plane edge, top corner → bottom corner
        ax.plot([d_top, d_bot], [z_top, z_bot], color=col, lw=lw, ls=ls,
                alpha=alpha, zorder=zord+1, solid_capstyle="round")

        # tilt angle arc at the plane centre
        if tdeg > 0:
            arc_r = 230 + (i - 1) * 150
            ax.add_patch(Arc((D_CTR, H/2), arc_r*2, arc_r*2, angle=0,
                             theta1=90, theta2=90 + tdeg, color=col, lw=1.2,
                             alpha=0.8, zorder=zord))
            ma = np.radians(90 + tdeg/2)
            ax.text(D_CTR + (arc_r+35)*np.cos(ma), H/2 + (arc_r+35)*np.sin(ma),
                    f"{tdeg:.0f}°", color=col, fontsize=7, ha="center",
                    va="center", **FONT, zorder=zord+2)
        ax.text(d_top - 60, z_top, name, color=col, fontsize=6.5,
                va="center", ha="right", **FONT, zorder=zord+2)

    # Pinhole
    ax.add_patch(Circle((0, PH_Y), 38, fc=PINHOLE, ec=WHITE, lw=1.5, zorder=12))
    ax.add_patch(Circle((0, PH_Y), 13, fc=BG, ec=WHITE, lw=0.8, zorder=13))
    ax.text(+150, PH_Y, "PINHOLE\nØ2.17mm", color=PINHOLE,
            fontsize=7, ha="center", va="center", **FONT)

    # Focal-length arrow
    fl_y = 50
    fl_tick = 15
    ax.annotate("", xy=(D_CTR, fl_y), xytext=(0, fl_y),
                arrowprops=dict(arrowstyle="<->", color=C_FLAT, lw=1.0, mutation_scale=7))
    ax.plot([0, 0], [fl_y - fl_tick, fl_y + fl_tick], color=C_FLAT, lw=0.6)
    ax.plot([D_CTR, D_CTR], [fl_y - fl_tick, fl_y + fl_tick], color=C_FLAT, lw=0.6)
    ax.text(D_CTR/2, fl_y+35,
            f"FLAT shown at mid-rail (axis tilt)  ·  back-focus 100–{D_FAR}mm  ·  max f = {W}mm at far wall",
            color=C_FLAT, fontsize=6, ha="center", **FONT)

    draw_dim_h(ax, 0, W, H+100, f"INTERIOR WIDTH (OPTICAL AXIS)  {W}mm",
               offset=15, color=DIM, font=FONT)
    draw_dim_v(ax, W+210, 0, H, f"INTERIOR HEIGHT\n{H}mm",
               offset=20, color=DIM, right=True, font=FONT)
    draw_dim_h(ax, D_NEAR, D_FAR, -190, f"RAIL TRAVEL  {D_FAR-D_NEAR}mm",
               offset=15, color=RAIL, above=False, font=FONT)
    draw_dim_h(ax, 0, D_NEAR, -100, f"{D_NEAR}mm",
               offset=20, color=DIM, fs=6, font=FONT)
    draw_dim_h(ax, D_FAR, W, -100, f"{W-D_FAR}mm",
               offset=20, color=DIM, fs=6, font=FONT)

    ax.text(W/2, H+255, "VIEW A — SIDE ELEVATION  (TILT)",
            color=WHITE, fontsize=9, ha="center", fontweight="bold", **FONT)
    ax.text(W/2, H+215, "Section through centerline  ·  vertical bridge = Z cross-slide (316 flat bar + UHMW pads; gib preload holds gravity, absorbs tilt foreshorten)  ·  slide-and-clamp, moved in coordinated pairs (rigid plane)",
            color=DIM, fontsize=6.5, ha="center", **FONT)

    # ── RIGHT PANEL: PLAN CROSS-SECTION — SWING ───────────────────────────────
    ax = ax_swing
    PAD2 = 300
    ax.set_xlim(-PAD2, L + PAD2)
    ax.set_ylim(-PAD2, W + 500)
    ax.set_aspect("equal")

    # Container outline (plan)
    ax.add_patch(Rectangle((0, 0), L, W, fc=GRID, ec=WHITE, lw=1.8, zorder=2))
    for x in np.arange(80, L, 457):
        ax.plot([x, x], [0, W], color=STRUCT2, lw=0.4, alpha=0.3, zorder=3)

    ax.add_patch(Rectangle((0, -WALL_T), L, WALL_T, fc=STRUCT2, ec=WHITE, lw=1.5, zorder=4))
    ax.text(L/2, -WALL_T/2-100, "PINHOLE WALL",
            color=WHITE, fontsize=7, ha="center", va="center", **FONT, zorder=5)
    ax.add_patch(Rectangle((0, W), L, WALL_T, fc=STRUCT, ec=WHITE, lw=1.0, zorder=4))
    ax.text(L/2, W+WALL_T/2+75, "FAR WALL",
            color=DIM, fontsize=7, ha="center", va="center", **FONT, zorder=5)
    for xw in [(-WALL_T, -WALL_T, WALL_T, W+2*WALL_T), (L, -WALL_T, WALL_T, W+2*WALL_T)]:
        ax.add_patch(Rectangle((xw[0], xw[1]), xw[2], xw[3],
                               fc=STRUCT, ec=WHITE, lw=1.0, zorder=4))

    # Pinhole (centered at X=2399 on the film plane)
    ax.add_patch(Circle((PH_X_C, 0), 55, fc=PINHOLE, ec=WHITE, lw=1.5, zorder=6))
    ax.add_patch(Circle((PH_X_C, 0), 18, fc=BG, ec=WHITE, lw=1.0, zorder=7))

    # Rails (plan view — ceiling rails projected down)
    RAIL_W_P = 50
    for rx in [RAIL_X_L - RAIL_W_P//2, RAIL_X_R - RAIL_W_P//2]:
        ax.add_patch(Rectangle((rx, D_NEAR), RAIL_W_P, D_FAR-D_NEAR,
                               fc=RAIL, ec=WHITE, lw=0.9, zorder=5, alpha=0.8))
    ax.text(RAIL_X_L, D_NEAR+(D_FAR-D_NEAR)*0.5, "CEIL\nRAIL\nLEFT",
            color=BG, fontsize=5.5, ha="center", va="center", rotation=90,
            **FONT, zorder=7)
    ax.text(RAIL_X_R, D_NEAR+(D_FAR-D_NEAR)*0.5, "CEIL\nRAIL\nRIGHT",
            color=BG, fontsize=5.5, ha="center", va="center", rotation=90,
            **FONT, zorder=7)

    # Swing configs — Option A rigid AXIS swing about the plane centre. The edge
    # stays length FP_W and FORESHORTENS in X (corners move inboard of the fixed
    # rails); an X cross-slide bridges the W/2·(1−cos s) gap.
    swing_configs = [
        ("Flat  0°",  0.0,  C_FLAT, "-"),
        ("Swing 14°", 14.0, C_T2,   "-."),
        ("Swing 28°", 28.0, C_T3,   ":"),
    ]

    for i, (name, sdeg, col, ls) in enumerate(swing_configs):
        lw = 2.4 if i == 0 else 1.9
        alpha = 1.0 if i == 0 else 0.85
        zord = 8 + i
        (x_L, d_L), (x_R, d_R) = swing_edge(sdeg, D_CTR)

        # rigid foreshortened plane edge
        ax.plot([x_L, x_R], [d_L, d_R], color=col, lw=lw, ls=ls, alpha=alpha,
                zorder=zord+1, solid_capstyle="round")
        # carriages on the fixed rails + X cross-slide bridge to each corner
        for (rx, dc, xc) in [(RAIL_X_L, d_L, x_L), (RAIL_X_R, d_R, x_R)]:
            ax.add_patch(Rectangle((rx-40, dc-40), 80, 80, fc=col, ec=WHITE,
                                   lw=0.7, alpha=0.5, zorder=zord))
            if abs(rx - xc) > 8:
                ax.plot([rx, xc], [dc, dc], color=col, lw=1.4, alpha=0.6, zorder=zord)

        # swing angle arc at the plane centre
        if sdeg > 0:
            arc_r = 700 + (i - 1) * 320
            ax.add_patch(Arc((CX_PLANE, D_CTR), arc_r*2, arc_r*2, angle=0,
                             theta1=0, theta2=sdeg, color=col, lw=1.2,
                             alpha=0.8, zorder=zord))
            ma = np.radians(sdeg/2)
            ax.text(CX_PLANE + (arc_r+45)*np.cos(ma), D_CTR + (arc_r+45)*np.sin(ma),
                    f"{sdeg:.0f}°", color=col, fontsize=7, ha="center",
                    va="center", **FONT, zorder=zord+2)
        ax.text(L/2, (d_L + d_R)/2 + 90, name, color=col, fontsize=6.5,
                ha="center", **FONT, zorder=zord+2)

    draw_dim_h(ax, 0, L, W+180, f"INTERIOR LENGTH  {L}mm",
               offset=15, color=DIM, fs=7, font=FONT)
    draw_dim_v(ax, L+230, 0, W, f"OPTICAL AXIS  {W}mm",
               offset=20, color=DIM, fs=7, right=True, font=FONT)
    draw_dim_v(ax, RAIL_X_L - 120, D_NEAR, D_FAR,
               f"RAIL\nTRAVEL\n{D_FAR-D_NEAR}mm", offset=400, color=RAIL, fs=6.5, font=FONT)

    ax.text(L/2, W+455, "VIEW B — CEILING CROSS-SECTION  (SWING)",
            color=WHITE, fontsize=9, ha="center", fontweight="bold", **FONT)
    ax.text(L/2, W+375, "Section at ceiling height  ·  horizontal bridge = X cross-slide (316 flat bar + UHMW pads; floats then cam-clamps, absorbs swing foreshorten)  ·  left/right slide-and-clamp as pairs (rigid single-axis swing)",
            color=DIM, fontsize=6.5, ha="center", **FONT)

    # Combined title
    fig.text(0.5, 0.98, "SHEET 2 — TILT ELEVATION (left)  &  SWING CROSS-SECTION (right)",
             color=WHITE, fontsize=11, ha="center", fontweight="bold", **FONT)

    # Title block (full-figure overlay for multi-subplot sheet)
    ax_tb = fig.add_axes([0, 0, 1, 1], facecolor="none")
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 2 OF 7",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="Tilt elevation & Swing cross-section",
                scale_note="Proportional (mm)",
                doc_id="TBS-FM01 · Film Plane Mechanism")

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet2.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet2.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — CORNER MECHANISM DETAIL  (slide-and-clamp + single U-joint)
# ═══════════════════════════════════════════════════════════════════════════════
# Consolidated from the retired generate_corner_detail.py. Color-coded corner views:
#   A   — corner assembly elevation (lower/floor corner; Yd × Z)
#   B   — U-joint detail (Ruland US12-6-6-SS, enlarged)
#   A-A — captive-carriage section (U-profile polymer liner)
#   C   — swing slide face-on
# ═══════════════════════════════════════════════════════════════════════════════
def _rect(ax, x, y, w, h, fc, ec=OUT, lw=1.4, z=4, alpha=1.0):
    draw_rect(ax, x, y, w, h, fc=fc, color=ec, lw=lw, zorder=z)
    if alpha < 1.0:
        ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec="none", alpha=alpha, zorder=z - 1))


def view_a(ax):
    """Corner assembly elevation — LOWER (floor) corner. Yd (horizontal) × Z (vertical), mm.
    Shown at the NOMINAL (flat) pose: the vertical carriage sits LOW, the green rail towers
    above it as the ~280 mm tilt-travel headroom."""
    ax.set_xlim(-60, 500); ax.set_ylim(-60, 432); ax.set_aspect("equal"); ax.axis("off")

    ax.plot([-30, 460], [0, 0], color="#999", lw=0.8, zorder=1)   # floor line

    # depth RAIL — 3x1.5 (76x38) 304 U-CHANNEL stood WEB-VERTICAL, seen along Yd (opening toward the
    # viewer = film side); 76 mm deep web, partial w/ break marks. The BOTTOM flange is the running surface.
    CT = 76                                                            # channel top Z (= carriage / stack base)
    ax.add_patch(plt.Rectangle((30, 0), 430, CT, fc=C_STEEL, ec="none", alpha=0.16, zorder=2))  # outboard web (behind)
    _rect(ax, 30, 0, 430, 5, C_STEEL, z=5)                             # BOTTOM flange — the rollers run on this
    _rect(ax, 30, CT - 5, 430, 5, C_STEEL, z=5)                        # top flange
    for bx in (44, 446):                                                   # zigzag break symbols (rail continues)
        zz = [(bx - 5, -2), (bx + 4, CT * 0.28), (bx - 4, CT * 0.55), (bx + 4, CT * 0.82), (bx - 5, CT + 2)]
        ax.plot([p[0] for p in zz], [p[1] for p in zz], color=OUT, lw=0.7, zorder=6)
    # 4-wheel acetal skate — 2 LOAD rollers on the bottom flange + 2 KEEPER rollers under the top flange
    for wx in (238, 298):
        draw_circle(ax, wx, 21, 16, color=OUT, fill=True, fc=C_ACET, lw=1.1, zorder=7)      # load roller Ø32 (bottom flange)
        draw_circle(ax, wx, 21, 4, color=OUT, fill=True, fc=C_STEEL, lw=0.6, zorder=8)      # Ø10 axle end
        draw_circle(ax, wx, CT - 15, 10, color=OUT, fill=True, fc=C_ACET, lw=0.9, zorder=7) # keeper roller Ø20 (under top flange)
        draw_circle(ax, wx, CT - 15, 3, color=OUT, fill=True, fc=C_STEEL, lw=0.5, zorder=8)
    _rect(ax, 224, CT, 90, 7, C_CAR, z=6)                             # carriage plate on the axle ends → stack
    ax.plot([268, 268], [CT + 7, CT + 22], color=OUT, lw=0.6, zorder=8)   # section cut A-A marker
    ax.plot([268, 268], [-14, 0], color=OUT, lw=0.6, zorder=8)
    ax.text(268, CT + 26, "A", fontsize=6.5, ha="center", va="bottom", color=OUT, **FONT)
    ax.text(268, -20, "A", fontsize=6.5, ha="center", va="top", color=OUT, **FONT)
    _rect(ax, 312, CT, 14, 16, C_CLAMP, z=8)                          # cam clamp / rail brake on the carriage
    ax.plot([326, 350], [CT + 12, CT + 4], color=C_CLAMP, lw=2.0, zorder=8)

    # vertical (TILT) slide rail — green; low carriage at nominal, rail = ~280 mm tilt headroom
    _rect(ax, 236, CT, 18, 280, C_TILT)                 # tall rail (travel envelope)
    _rect(ax, 228, CT + 8, 34, 52, C_TILT)              # vertical friction carriage (LOW = nominal)
    _rect(ax, 262, CT + 20, 14, 20, C_CLAMP)            # cam clamp body
    ax.plot([276, 306], [CT + 30, CT + 22], color=C_CLAMP, lw=2.2, zorder=6)   # clamp lever
    _rect(ax, 262, CT + 46, 44, 12, C_UJ)               # bracket carriage → corner stack

    # horizontal (SWING) slide — purple, runs into the page (X); shown edge-on
    _rect(ax, 292, CT + 58, 48, 16, C_SWING)

    # single U-joint (Ruland US12-6-6-SS)
    _rect(ax, 300, CT + 74, 32, 30, C_UJ)
    draw_circle(ax, 316, CT + 89, 5.5, color=C_PIN, fill=True, fc=C_PIN, lw=1.0, zorder=6)
    ax.plot([316, 316], [CT + 70, CT + 108], color=C_PIN, lw=1.6, zorder=5)

    # film-frame corner (2x2 Al angle) + film plane edge (ghost)
    _rect(ax, 308, CT + 104, 44, 8, C_FRAME)            # horizontal leg
    _rect(ax, 308, CT + 104, 8, 214, C_FRAME)          # vertical leg
    ax.add_patch(plt.Rectangle((320, CT + 112), 6, 202, fc=C_PANEL, ec="none", alpha=0.16, zorder=2))

    # ── dimensions (both on the left, near the green rail) ──
    draw_dim_v(ax, 8, CT, CT + 104, "~150mm\nnominal\nstack", offset=28, fs=6, color=DIM, font=FONT)
    draw_dim_v(ax, 206, CT, CT + 280, "~280mm\ntilt travel", offset=26, fs=6, color=DIM, font=FONT)

    # ── leaders ──
    leader(ax, 90, 23, 40, -44, "DEPTH RAIL (Y) — 3×1.5 304 U-CHANNEL, web-vertical; the traverse; ~2.4 m (floor rail)",
           ha="left", fs=6.2, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 268, 45, 336, -36, "4-wheel acetal skate — Ø32 LOAD rollers on the bottom flange\n+ Ø20 KEEPER rollers under the top flange (captive); carriage plate → stack",
           ha="left", fs=6.2, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 245, 340, 250, 372, "VERTICAL way (Z, green) — 316 flat bar\n+ UHMW pads; TILT accommodation",
           ha="left", fs=6.2, color=C_TILT, font=FONT, bbox=LBL_BG)
    leader(ax, 306, CT + 30, 352, CT + 16, "cam clamp — one per slide\n(push → lock)",
           ha="left", fs=6.2, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 316, CT + 66, 356, CT + 58, "HORIZONTAL way (X, purple) — 316 flat bar\n+ UHMW pads; SWING accom. (into page)",
           ha="left", fs=6.2, color=C_SWING, font=FONT, bbox=LBL_BG)
    leader(ax, 332, CT + 89, 372, CT + 110, "single U-joint\n(Ruland US12-6-6-SS)",
           ha="left", fs=6.2, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 318, 336, 352, 358, "film-frame corner\n(2x2 Al angle) + film",
           ha="left", fs=6.2, color=OUT, font=FONT, bbox=LBL_BG)

    ax.text(-58, 424, "A — CORNER ASSEMBLY ELEVATION  (lower / floor corner; Yd × Z; nominal pose)",
            fontsize=8, fontweight="bold", color=OUT, ha="left", va="top", **FONT)


def view_b(ax):
    """U-joint detail (enlarged ~2:1). Ruland US12-6-6-SS; through-axis horizontal."""
    ax.set_xlim(0, 200); ax.set_ylim(-10, 150); ax.set_aspect("equal"); ax.axis("off")
    cy = 70
    # through-axis centre line
    ax.plot([8, 192], [cy, cy], color="#2060A0", lw=0.6, dashes=(8, 3, 2, 3), zorder=2)

    # input shaft stub + hub (carrier side, left)
    _rect(ax, 10, cy - 9, 26, 18, C_STEEL)
    # input yoke — two ears (top + bottom) opening right, holding the vertical (SWING) pin
    _rect(ax, 40, cy + 14, 40, 16, C_UJ); _rect(ax, 40, cy - 30, 40, 16, C_UJ)
    ax.plot([70, 70], [cy - 34, cy + 34], color=C_PIN, lw=2.4, zorder=6)          # swing pin (vertical)
    draw_circle(ax, 70, cy + 22, 4, color=C_PIN, fill=True, fc=C_PIN, lw=0.8, zorder=7)
    draw_circle(ax, 70, cy - 22, 4, color=C_PIN, fill=True, fc=C_PIN, lw=0.8, zorder=7)
    # cross / spider block
    _rect(ax, 62, cy - 14, 30, 28, "#9AA0A8")
    # output yoke — ears opening left (perpendicular, into page → ghost), holding the tilt pin
    _rect(ax, 84, cy + 12, 40, 14, C_UJ, ec="#7A8290", lw=1.0)
    _rect(ax, 84, cy - 26, 40, 14, C_UJ, ec="#7A8290", lw=1.0)
    draw_circle(ax, 90, cy, 5, color=C_PIN, fill=True, fc=C_PIN, lw=0.8, zorder=7)  # tilt pin (into page)
    # output shaft stub (frame side, right)
    _rect(ax, 128, cy - 9, 26, 18, C_STEEL)

    # ±45° articulation arc on the through-axis (schematic)
    ax.add_patch(Arc((70, cy), 150, 150, angle=0, theta1=-45, theta2=45, color=DIM, lw=0.9, zorder=5))
    for ang in (45, -45):
        import math
        ex = 70 + 75 * math.cos(math.radians(ang)); ey = cy + 75 * math.sin(math.radians(ang))
        ax.plot([70, ex], [cy, ey], color=DIM, lw=0.5, dashes=(4, 3), zorder=4)
    ax.text(150, cy + 40, "±45°\nmax swivel", fontsize=6, color=DIM, ha="left", va="center", **FONT)

    # dims
    draw_dim_h(ax, 10, 154, cy - 44, "68mm overall", offset=12, fs=6, color=DIM, above=False, font=FONT)
    draw_dim_v(ax, 176, cy - 9, cy + 9, "19mm OD", offset=13, fs=6, color=DIM, right=True,
               perpendicular=True, font=FONT)

    # callouts
    leader(ax, 70, cy + 30, 30, cy + 46, "SWING axis (vertical pin)", ha="left", fs=6, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 90, cy, 120, cy + 30, "TILT axis (perpendicular pin, into page)", ha="left", fs=6, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 23, cy - 9, 20, cy - 30, "to carrier / cross-slide", ha="left", fs=6, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 141, cy + 9, 120, cy - 30, "to film-frame corner", ha="left", fs=6, color=OUT, font=FONT, bbox=LBL_BG)

    ax.text(0, 146, "B — U-JOINT DETAIL  (Ruland US12-6-6-SS, enlarged)",
            fontsize=8, fontweight="bold", color=OUT, ha="left", va="top", **FONT)


def _uchan_hatch(ax, x, y, w, h, z=6):
    _rect(ax, x, y, w, h, C_STEEL, z=z)
    hatch_rect(ax, x, y, w, h, color="#8A93A0", hatch="///", lw=0.0)


def section_aa(ax):
    """SECTION A-A — cut ACROSS the BOTTOM (weight) depth rail (channel runs into the page). The 3×1.5 304
    U-channel is stood WEB-VERTICAL: web = OUTBOARD back (splice/mount face), flanges project INBOARD as the
    roller channel. A Ø32 acetal LOAD roller is gravity-seated on the BOTTOM flange (this rail carries the
    plane's weight in every tilt/swing pose). A smaller KEEPER roller runs just under the TOP flange —
    anti-lift capture for transport shock / load reversal — and a shallow LIP on the bottom flange's inboard
    edge stops the roller walking off in X when the plane swings. Ø10 axles cantilever INBOARD to the
    carriage plate only (never cross the web); the retainer bolt passes DOWN through the plate (saddle clamp)."""
    ax.set_xlim(-26, 118); ax.set_ylim(-16, 92); ax.set_aspect("equal"); ax.axis("off")
    # ── U-channel, web-vertical (outboard web at left; flanges project inboard/right) ──
    _uchan_hatch(ax, 0, 0, 5, 76)          # web = outboard back / splice face (76 tall)
    _uchan_hatch(ax, 5, 0, 38, 5)          # BOTTOM flange (running surface)
    _uchan_hatch(ax, 39, 5, 4, 9)          # inboard LIP on the bottom flange (lateral keeper, X)
    _uchan_hatch(ax, 5, 71, 38, 5)         # top flange
    # ── Ø32 acetal LOAD roller, gravity-seated on the bottom flange (edge-on: axis = X, in-plane) ──
    _rect(ax, 9, 5, 16, 32, C_ACET, z=7)
    draw_circle(ax, 17, 21, 5, color=OUT, fill=True, fc=C_STEEL, lw=0.8, zorder=8)   # Ø10 axle (end-on)
    _rect(ax, 25, 16, 25, 10, C_STEEL, z=6)                                         # short axle → carriage (inboard only)
    # ── KEEPER roller, just under the top flange (anti-lift), on its own stub axle ──
    _rect(ax, 11, 55, 13, 15, C_ACET, z=7)
    draw_circle(ax, 17, 62, 4, color=OUT, fill=True, fc=C_STEEL, lw=0.7, zorder=8)
    _rect(ax, 21, 58, 29, 8, C_STEEL, z=6)                                          # keeper stub axle → carriage
    # ── carriage plate (inboard, close to the channel opening) — the MOVING part; both axles land on it ──
    _rect(ax, 50, -2, 14, 74, C_CAR, z=6)
    ax.plot([57, 57], [-2, 70], color=C_PIN, lw=1.8, zorder=8)                       # retainer bolt DOWN thru plate
    draw_circle(ax, 57, 68, 3, color=OUT, fill=True, fc=C_PIN, lw=0.6, zorder=9)
    # ── the stack inboard: green Z slide begins on the plate ──
    _rect(ax, 64, 10, 12, 46, C_TILT, z=5)
    ax.annotate("", xy=(108, 33), xytext=(76, 33), arrowprops=dict(arrowstyle="->", color=DIM, lw=1.0))
    # seating + lift arrows
    ax.annotate("", xy=(17, 42), xytext=(17, 52), arrowprops=dict(arrowstyle="->", color=OUT, lw=1.4))
    ax.text(6, 47, "WEIGHT", fontsize=5.4, ha="right", va="center", color=OUT, **FONT)
    # dims
    draw_dim_v(ax, -14, 0, 76, "76\n(3\")", offset=9, fs=5.4, color=DIM, font=FONT)
    draw_dim_h(ax, 5, 43, -10, "38 flange", offset=7, fs=5.4, color=DIM, above=False, font=FONT)
    # leaders
    leader(ax, 2, 38, -25, 28, "WEB (outboard,\nsplice face)", ha="left", fs=5.0, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 17, 9, -8, -12, "Ø32 LOAD roller\n(gravity-seated)", ha="left", fs=5.0, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 17, 68, 30, 84, "KEEPER roller — runs under the top\nflange = anti-lift (shock / reversal)", ha="left", fs=5.0, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 41, 12, 52, -2, "LIP on the bottom flange —\nstops X walk-off on swing", ha="left", fs=5.0, color=C_TILT, font=FONT, bbox=LBL_BG)
    leader(ax, 57, 2, 84, -12, "retainer bolt DOWN through the plate\n(saddle clamp — not through the rail)", ha="left", fs=5.0, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 104, 33, 96, 50, "→ cross-slide stack (Z/X)\n→ U-joint → film corner", ha="left", fs=5.0, color=DIM, font=FONT, bbox=LBL_BG)
    ax.text(-26, 92, "SECTION A-A — BOTTOM (weight) carriage",
            fontsize=6.8, fontweight="bold", color=OUT, ha="left", va="top", **FONT)
    ax.text(-26, 85, "web-vertical channel", fontsize=5.4, color=DIM, ha="left", va="top", **FONT)


def section_top(ax):
    """SECTION B-B — cut across the TOP (guide) rail. The 3×1.5 304 U-channel is laid FLAT (inverted-U):
    web = closed TOP (splice face), flanges hang DOWN. The top rail carries NO weight (it's a depth/lateral
    GUIDE — the plane's weight is on the bottom rail), so a Ø32 acetal GUIDE roller runs lightly in the
    channel and a KEEPER roller hooks under a flange lip to hold the skate captive against dynamic drift.
    Short in Z = minimum ceiling cost. The carriage plate + stack hang BELOW; the film top rides ~10 mm
    under the web (guide gap)."""
    ax.set_xlim(-26, 130); ax.set_ylim(-58, 50); ax.set_aspect("equal"); ax.axis("off")
    # inverted-U: web on top (closed), flanges hang down — opening faces DOWN
    _uchan_hatch(ax, 0, 33, 76, 5)          # web = closed top / splice face (76 wide)
    for fx in (0, 71):
        _uchan_hatch(ax, fx, 0, 5, 38)      # flanges hang down (38)
    # WIDE Ø32 acetal guide DRUM — nearly spans the throat, so BOTH flanges locate it laterally (tight X)
    _rect(ax, 8, 1, 60, 32, C_ACET, z=7)
    draw_circle(ax, 38, 17, 5, color=OUT, fill=True, fc=C_STEEL, lw=0.8, zorder=8)   # Ø10 axle end
    for gx in (7, 69):                                                               # lateral-clearance marks to the flanges
        ax.plot([gx, gx], [4, 30], color=DIM, lw=0.4, dashes=(1, 1), zorder=8)
    # KEEPER roller — hooks under the inboard (right) flange lip from BELOW (anti-drop; holds the drum to the web)
    _rect(ax, 66, -10, 12, 12, C_ACET, z=7)
    draw_circle(ax, 72, -4, 3, color=OUT, fill=True, fc=C_STEEL, lw=0.6, zorder=8)
    # carriage plate — INBOARD; the drum axle + keeper axle land on it, stack hangs below
    _rect(ax, 88, -40, 14, 62, C_CAR, z=6)
    _rect(ax, 68, 13, 20, 8, C_STEEL, z=6)                                           # drum axle → carriage
    _rect(ax, 78, -6, 12, 8, C_STEEL, z=6)                                           # keeper axle → carriage
    ax.plot([95, 95], [-40, 20], color=C_PIN, lw=1.6, zorder=8)                       # retainer bolt through plate
    _rect(ax, 88, -54, 12, 14, C_TILT, z=5)                                          # cross-slide (green) hangs below
    ax.add_patch(plt.Rectangle((62, -58), 50, 5, fc=C_PANEL, ec="none", alpha=0.16, zorder=2))  # film top edge ghost (hangs)
    ax.annotate("", xy=(38, 33), xytext=(38, 25), arrowprops=dict(arrowstyle="->", color=OUT, lw=1.0))  # guide reaction UP
    draw_dim_v(ax, -14, 0, 38, "38\n(short:\nceiling)", offset=7, fs=5.2, color=DIM, font=FONT)
    leader(ax, 30, 18, 46, -16, "wide guide DRUM (Ø32) — no weight", ha="left", fs=5.0, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 72, -8, 90, -30, "KEEPER hooks the flange lip from below\n(anti-drop — holds the drum to the web)", ha="left", fs=5.0, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 95, -18, 108, -18, "carriage + cross-slide\nstack hang BELOW", ha="left", fs=5.0, color=DIM, font=FONT, bbox=LBL_BG)
    ax.text(-26, 50, "SECTION B-B — TOP (guide) carriage",
            fontsize=6.8, fontweight="bold", color=OUT, ha="left", va="top", **FONT)
    ax.text(-26, 43, "wide drum spans the throat → flanges locate it in X (the flat rail's lip)",
            fontsize=5.0, color=DIM, ha="left", va="top", **FONT)


def view_c(ax):
    """C — CROSS-SLIDE SECTION (Z tilt / X swing): a 316 flat bar captured by a 316 carriage on
    UHMW pads; an adjustable brass-tip gib sets the drag that HOLDS the gravity-loaded vertical (Z)
    axis, yet still hand-slides. The X (swing) cross-slide is the same part, gravity-neutral."""
    C_WAY = "#8E949C"
    ax.set_xlim(-40, 150); ax.set_ylim(-24, 64); ax.set_aspect("equal"); ax.axis("off")
    # 316 carriage — inverted-U wrapping the bar (hatched = cut solid) + bottom plate
    for (x, y, w, h) in [(10, 27, 52, 7), (10, 2, 52, 4), (10, 6, 4, 21), (58, 6, 4, 21)]:
        _rect(ax, x, y, w, h, C_STEEL, z=5)
        hatch_rect(ax, x, y, w, h, color="#8A93A0", hatch="///", lw=0.0)
    # 316 flat-bar way (the Z-tilt / X-swing accommodation bar), captured in the middle
    _rect(ax, 14, 16, 44, 8, C_WAY, z=6)
    hatch_rect(ax, 14, 16, 44, 8, color="#6E747C", hatch="\\\\\\", lw=0.0)
    # UHMW pads on both faces
    _rect(ax, 16, 24, 40, 3, C_POLY, z=7)
    _rect(ax, 16, 13, 40, 3, C_POLY, z=7)
    # adjustable gib + brass-tip screw
    _rect(ax, 14, 8.5, 44, 4, C_STEEL, z=6)
    hatch_rect(ax, 14, 8.5, 44, 4, color="#8A93A0", hatch="///", lw=0.0)
    _rect(ax, 33, 3.5, 6, 5.5, C_PIN, z=8)
    for yy in (4.6, 5.9, 7.2):
        ax.plot([31.7, 40.3], [yy, yy], color=OUT, lw=0.4, zorder=9)
    leader(ax, 44, 20, 68, 48, "316 flat-bar WAY (Z tilt / X swing)",
           ha="left", fs=5.8, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 30, 25.5, 68, 36, "UHMW pad — self-lube, DRY (both faces)",
           ha="left", fs=5.8, color="#8A6A2A", font=FONT, bbox=LBL_BG)
    leader(ax, 12, 32, 68, 24, "316 carriage — the MOVING part",
           ha="left", fs=5.8, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 36, 5, 42, -16, "adjustable GIB + brass-tip screw — sets the drag that HOLDS\nthe gravity-loaded Z axis, yet still hand-slides (re-tune after break-in)",
           ha="left", fs=5.8, color=OUT, font=FONT, bbox=LBL_BG)
    ax.text(-40, 64, "C — CROSS-SLIDE SECTION  (Z tilt / X swing): UHMW pad on 316 flat bar; the gib holds the vertical axis",
            fontsize=7.0, fontweight="bold", color=OUT, ha="left", va="top", **FONT)


def sheet3():
    reset_label_registry()
    fig = plt.figure(figsize=(18, 13))
    fig.patch.set_facecolor(BG)

    ax_a = fig.add_axes([0.03, 0.42, 0.45, 0.55]); ax_a.set_facecolor(BG)
    ax_b = fig.add_axes([0.52, 0.68, 0.24, 0.29]); ax_b.set_facecolor(BG)
    ax_stub = fig.add_axes([0.78, 0.68, 0.21, 0.28]); ax_stub.set_facecolor(BG)
    ax_sec = fig.add_axes([0.52, 0.45, 0.23, 0.21]); ax_sec.set_facecolor(BG)
    ax_sec2 = fig.add_axes([0.75, 0.45, 0.22, 0.21]); ax_sec2.set_facecolor(BG)
    ax_c = fig.add_axes([0.03, 0.10, 0.45, 0.28]); ax_c.set_facecolor(BG)
    view_a(ax_a)
    view_b(ax_b)
    _stub_carrier(ax_stub)
    section_aa(ax_sec)
    section_top(ax_sec2)
    view_c(ax_c)

    # notes block
    ax_n = fig.add_axes([0.52, 0.085, 0.45, 0.35]); ax_n.set_xlim(0, 100); ax_n.set_ylim(0, 100)
    ax_n.axis("off")
    draw_notes(ax_n, [
        "CORNER MECHANISM — ONE OF FOUR:",
        "1. A pinhole has infinite depth of field, so the plane is positioned for scene control "
        "(tilt / swing / rise), not focus — hence slide-and-clamp, not leadscrews.",
        "2. Three axes per corner: DEPTH (Y) is the traverse — a 4-wheel acetal skate in a 3x1.5 304 "
        "U-channel (McMaster 1262T21; top-bottom depth = tilt, left-right = swing); VERTICAL (Z, green, "
        "~280mm) + HORIZONTAL (X, purple, ~260mm) cross-slides (316 flat bar + UHMW pad + gib) absorb the "
        "tilt/swing foreshortening.",
        "3. Roll the skate / push each cross-slide into position; the gib drag holds the vertical, "
        "then throw the cam clamp (rail brake) to lock for the shot and for transport.",
        "4. The U-joint (Ruland US12-6-6-SS, 303 SS, self-lube, grease-free, nitrile-booted) gives "
        "tilt + swing and locks twist so the flat plane stays square. The plane's WEIGHT is carried by "
        "the BOTTOM rail (web-vertical, load rollers gravity-seated on the bottom flange); the TOP rail "
        "is a GUIDE only (flat inverted-U, minimum ceiling cost).",
        "5. WHEEL CAPTURE: BOTTOM rail — load rollers on the bottom flange + a KEEPER under the top flange "
        "(anti-lift) + a LIP on the inboard flange edge (stops X walk-off on swing). TOP rail — a WIDE guide "
        "DRUM spans the throat so both flanges locate it in X, + a KEEPER hooking a flange (anti-drop). "
        "(LEFT rails = a transport drop-in — see Sheet 4.)",
        "6. OVERTURNING COUPLE: the film-corner load is ~50mm INBOARD of the rail (via the stack) — a moment "
        "about the rollers. The load↓ / keeper↑ pair, spaced by the channel depth, reacts it — so the keepers "
        "carry this static couple too. Tightest link: the 316 cross-slide bar in weak-axis bending; keep the "
        "stack compact.",
    ], 2, 99, 4.2, fs=5.2, title_fs=6.4, color=DIM, width=96, wrap=90, font=FONT)

    ax_tb = fig.add_axes([0.03, 0.008, 0.94, 0.06])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, "SHEET 3 OF 7",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="Corner carriage detail — acetal skate on 3×1.5 304 U-channel + cross-slides + U-joint + stub clamp",
                scale_note="DIMS IN mm",
                doc_id="TBS-FM01 · Film Plane Mechanism",
                height=0.75)

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet3.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet3.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 4 — U-JOINT SECTIONS  (how each side secures)
# ═══════════════════════════════════════════════════════════════════════════════
def _body(ax, x, y, w, h, z=4):
    """A sectioned (cut) U-joint body element: light fill + section hatch + outline."""
    draw_rect(ax, x, y, w, h, fc=C_UJ, color=OUT, lw=1.2, zorder=z)
    hatch_rect(ax, x, y, w, h, color="#7A8AA0", hatch="////", lw=0.0)


def _setscrew(ax, cx, y0, w=5.0, h=6.5, hub_top=None):
    """Set screw with serrated (threaded) sides + hex socket, plus the MATING thread cut into the
    (blue) hub wall where it threads in."""
    import numpy as np
    if hub_top is None:
        hub_top = y0 + 4.9
    for yy in np.arange(y0 + 0.3, hub_top, 1.3):
        ax.plot([cx - w / 2, cx - w / 2 - 1.3], [yy, yy + 0.9], color="#4E627E", lw=0.5, zorder=7)
        ax.plot([cx + w / 2, cx + w / 2 + 1.3], [yy, yy + 0.9], color="#4E627E", lw=0.5, zorder=7)
    draw_rect(ax, cx - w / 2, y0, w, h, fc="#7C7C86", color=OUT, lw=0.8, zorder=9)
    ys = list(np.arange(y0 + 0.3, y0 + h - 0.2, 1.3))
    ax.plot([cx - w / 2 + (0.9 if i % 2 else 0.0) for i in range(len(ys))], ys, color=OUT, lw=0.5, zorder=10)
    ax.plot([cx + w / 2 - (0.9 if i % 2 else 0.0) for i in range(len(ys))], ys, color=OUT, lw=0.5, zorder=10)
    ax.plot([cx - 1.2, cx + 1.2], [y0 + h - 0.9, y0 + h - 0.9], color=OUT, lw=1.0, zorder=11)


def _stub_carrier(ax):
    """Section ACROSS the stub shaft (shaft end-on) at the 304 SS base-mount clamping shaft
    support (McMaster 4040N12): the base flange bolts down to the X-slide carriage, the removable
    cap is pulled onto the shaft by two clamp screws that flank it, and the shaft continues out of
    the page into the U-joint hub. The frame end is identical."""
    C_SS = "#7C7C86"
    ax.set_xlim(-42, 96); ax.set_ylim(-40, 34); ax.set_aspect("equal"); ax.axis("off")
    cx = 26
    # carrier bracket (the X-slide carriage face the support bolts down to)
    draw_rect(ax, -10, -34, 84, 14, fc=C_STEEL, color=OUT, lw=1.2, zorder=3)
    hatch_rect(ax, -10, -34, 84, 14, color="#7A8AA0", hatch="////", lw=0.0)
    # support base flange (on the carrier) + removable clamp cap on top, split at the shaft centre
    _body(ax, 4, -20, 44, 20, z=5)      # base flange  x4..48, y-20..0
    _body(ax, 12, 0, 28, 14, z=5)       # removable cap  x12..40, y0..14
    ax.plot([12, 40], [0, 0], color=OUT, lw=0.6, zorder=8)   # cap/base parting line at the shaft centre
    # stub shaft, END-ON (a circle) sitting in the bore on the parting line
    draw_circle(ax, cx, 0, 6, color=OUT, fill=True, fc=C_STEEL, lw=1.2, zorder=7)
    draw_circle(ax, cx, 0, 2, color=OUT, fill=True, fc="white", lw=0.6, zorder=8)
    # 2 clamp screws — flank the shaft, from the cap top DOWN into the base (pull the cap onto the shaft)
    for sx in (cx - 9, cx + 9):
        draw_rect(ax, sx - 1.8, -3, 3.6, 17, fc=C_PIN, color=OUT, lw=0.7, zorder=6)   # y-3..14
        ax.plot([sx - 2.6, sx + 2.6], [13, 13], color=OUT, lw=1.0, zorder=10)         # head slot
    # 2 mounting bolts — flank the base, head on the flange top, one continuous shank into the carrier
    for bx in (9, 43):
        draw_rect(ax, bx - 1.9, -32, 3.8, 32, fc=C_SS, color=OUT, lw=0.7, zorder=6)   # shank y-32..0 (continuous)
        ax.add_patch(plt.Rectangle((bx - 3, 0), 6, 3.4, fc=C_SS, ec=OUT, lw=0.7, zorder=9))  # head on the flange
    draw_dim_v(ax, 56, -6, 6, "9.5mm\n(3/8)", offset=9, fs=5.0, color=DIM, right=True,
               perpendicular=True, font=FONT)
    leader(ax, cx + 4, 4, cx + 26, 24, "STUB (end-on) →\nU-joint hub (view B)",
           ha="left", fs=5.2, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, cx + 9, 10, cx + 4, 30, "clamp screws pull the\nCAP onto the shaft",
           ha="left", fs=5.2, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 30, -27, 34, -39, "base-mount clamp (4040N12, 304 SS)\nbolts to the X-slide carrier",
           ha="left", fs=5.2, color=OUT, font=FONT, bbox=LBL_BG)
    ax.text(-42, 32, "STUB → CARRIER CLAMP", fontsize=6.5, fontweight="bold", color=OUT, ha="left", va="top", **FONT)
    ax.text(-42, 25, "section across the shaft; frame end identical", fontsize=4.9, color=DIM, ha="left", va="top", **FONT)
    ax.text(-42, 27, "section ACROSS the shaft; the film-frame end is identical", fontsize=5.4, color=DIM, ha="left", va="top", **FONT)


def _rail_band(ax, y0, ylen, z0, z1, fc, z=4):
    """A depth-rail segment drawn along its LENGTH (Yd × Z elevation): a filled web band with a
    darker top + bottom flange line, so it reads as a U-channel seen side-on."""
    _rect(ax, y0, z0, ylen, z1 - z0, fc, z=z)
    for zz in (z0, z1 - 5):
        ax.add_patch(plt.Rectangle((y0, zz), ylen, 5, fc="#9AA2AC", ec="none", zorder=z + 1))


def transport_elev(ax):
    """LEFT depth rail — TRANSPORT DROP-IN, side elevation (Yd × Z; Yd positions dimensioned, Z schematic).
    For transport the hinge panel folds about the pivot post (Yd PIVOT_YD) and sweeps the X150 rail line, so
    the LEFT rail is SPLIT: a fixed STUB (parks the corner, anchored at the pivot post + far wall) and a
    REMOVABLE section that lifts out. A welded BRIDGE (welded to the stub) spans the cut; the removable
    THUMB-SCREWS to it. A length SPLICE at the pinhole end makes 6 ft stock reach; a pinhole-wall GUSSET seats
    that end. (RIGHT rail = flanged wall-to-wall, panel at lower right.)"""
    ax.set_xlim(-320, 2660); ax.set_ylim(-235, 185); ax.axis("off")
    rz0, rz1 = 74, 118
    # walls + floor
    ax.add_patch(plt.Rectangle((-16, -30), 16, 210, fc=STRUCT, ec=OUT, lw=1.0, zorder=2))       # pinhole wall
    ax.add_patch(plt.Rectangle((C_WID, -30), 16, 210, fc=STRUCT, ec=OUT, lw=1.0, zorder=2))     # far wall
    ax.plot([-320, 2660], [0, 0], color="#999", lw=0.9, zorder=1)                               # floor
    ax.text(-16, 188, "PINHOLE WALL (Yd 0)", fontsize=5.6, color=DIM, ha="left", va="bottom", **FONT)
    ax.text(C_WID + 16, 188, "FAR WALL", fontsize=5.6, color=DIM, ha="right", va="bottom", **FONT)
    # REMOVABLE (light) + STUB (solid)
    _rail_band(ax, 0, LEFT_CUT_YD, rz0, rz1, "#D6DEEA")
    _rail_band(ax, LEFT_CUT_YD, C_WID - LEFT_CUT_YD, rz0, rz1, C_STEEL)
    # CUT parting line
    ax.plot([LEFT_CUT_YD, LEFT_CUT_YD], [rz0 - 12, rz1 + 14], color=OUT, lw=1.1, dashes=(4, 3), zorder=7)
    # welded BRIDGE — sits ON TOP of the rail at the cut so GRAVITY holds it down; WELDED to the REMOVABLE
    # (left of cut), it laps + BEARS on the STUB (right of cut). A retaining SCREW into the stub stops it
    # lifting/sliding (the weight rides the bridge, not the screw).
    _rect(ax, LEFT_CUT_YD - 96, rz1, 168, 12, C_CAR, z=8)                       # fishplate ON TOP, straddling the cut
    for wx in (LEFT_CUT_YD - 84, LEFT_CUT_YD - 60, LEFT_CUT_YD - 36):           # fillet weld beads (removable side, on top)
        ax.plot([wx, wx + 10], [rz1 + 1, rz1 + 1], color=OUT, lw=2.0, zorder=10)
    draw_circle(ax, LEFT_CUT_YD + 44, rz1 + 6, 5.5, color=OUT, fill=True, fc=C_PIN, lw=0.9, zorder=11)  # retaining screw (stub side)
    # length SPLICE at the pinhole end — on the OUTBOARD WEB-BACK (far side), so shown as a GHOST outline
    ax.add_patch(plt.Rectangle((SPLICE_YD - 55, rz0), 110, rz1 - rz0, fc="none", ec=OUT, lw=1.0, ls=(0, (5, 3)), zorder=8))
    # pinhole-wall gusset/seat (Yd 0)
    _rect(ax, 0, rz0 - 36, 44, (rz1 - rz0) + 42, C_STEEL, z=3)
    # pivot post down to floor (Ø89 CHS)
    _rect(ax, PIVOT_YD - PIVOT_POST_OD / 2, 0, PIVOT_POST_OD, rz0, C_STEEL, z=3)
    hatch_rect(ax, PIVOT_YD - PIVOT_POST_OD / 2, 0, PIVOT_POST_OD, rz0, color="#8A93A0", hatch="//", lw=0.0)
    # far flange (stub → far wall)
    _rect(ax, C_WID - 42, rz0 - 8, 42, (rz1 - rz0) + 16, C_CAR, z=6)
    # transport-fold note — the fold is about the VERTICAL pivot (a plan-view motion, 90° to this elevation),
    # so no in-plane arc; the removable simply lifts UP/out of the channel first. Placed below the rail.
    ax.text(1000, -20, "REMOVABLE lifts OUT (↑) for transport; the panel then folds about\nthe vertical pivot (a plan-view motion — see Sheet 1)",
            fontsize=5.8, color=C_T3, ha="center", va="top", **FONT)
    # ── dimensions (Yd) ──
    draw_dim_h(ax, 0, LEFT_CUT_YD, -70, f"REMOVABLE = {LEFT_CUT_YD} (lifts out)", offset=12, fs=6, color=DIM, above=False, font=FONT)
    draw_dim_h(ax, LEFT_CUT_YD, C_WID, -130, f"STUB = {C_WID - LEFT_CUT_YD}\n(parks corner)", offset=12, fs=6, color=DIM, above=False, font=FONT)
    # ── leaders (spread above / below the rail to keep the crowded cut region legible) ──
    leader(ax, SPLICE_YD, (rz0 + rz1) / 2, 470, -55, "length SPLICE (web-back, GHOST — far side) — 6 ft stock + reach",
           ha="left", fs=5.8, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 22, rz0 - 18, 60, -58, "pinhole-wall GUSSET / seat",
           ha="left", fs=5.8, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, LEFT_CUT_YD + 44, rz1 + 6, 1380, 150, "welded BRIDGE (ON TOP) — welded to the REMOVABLE; GRAVITY bears it on the STUB;\na retaining SCREW into the stub stops it lifting (weight on the bridge, not the screw)",
           ha="left", fs=5.8, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, PIVOT_YD, 30, PIVOT_YD + 30, -150, f"swing PIVOT POST (Ø{PIVOT_POST_OD} CHS)\nanchors the stub — no floor post at the cut",
           ha="left", fs=5.8, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, C_WID - 20, rz0 + 8, C_WID + 34, 58, "far flange\n→ far wall",
           ha="left", fs=5.8, color=OUT, font=FONT, bbox=LBL_BG)
    ax.text(-320, 182, "LEFT RAIL — TRANSPORT DROP-IN  (bottom rail shown; the top rail splits the same way)",
            fontsize=8.5, fontweight="bold", color=OUT, ha="left", va="top", **FONT)
    ax.text(-320, 166, "REMOVABLE (light) lifts out so the panel can fold; STUB (solid) stays",
            fontsize=6.0, color=DIM, ha="left", va="top", **FONT)


def right_flanged(ax):
    """RIGHT depth rail — flanged WALL-TO-WALL (permanent), side elevation (Yd × Z). Continuous 304 U-channel
    with an end flange through-bolted to each wall; the outboard end plate is trimmed 35 mm for IBC clearance
    and shares the IBC combined corner plate. No transport split (the panel folds away from this side)."""
    ax.set_xlim(-260, 2620); ax.set_ylim(-70, 150); ax.axis("off")
    rz0, rz1 = 60, 104
    ax.add_patch(plt.Rectangle((-16, -20), 16, 160, fc=STRUCT, ec=OUT, lw=1.0, zorder=2))
    ax.add_patch(plt.Rectangle((C_WID, -20), 16, 160, fc=STRUCT, ec=OUT, lw=1.0, zorder=2))
    ax.plot([-260, 2620], [0, 0], color="#999", lw=0.9, zorder=1)
    _rail_band(ax, 0, C_WID, rz0, rz1, C_STEEL)
    for yf in (0, C_WID - 40):                    # end flanges through-bolted to each wall
        _rect(ax, yf, rz0 - 8, 40, (rz1 - rz0) + 16, C_CAR, z=6)
        for bz in (rz0 + 4, rz1 - 4):
            draw_circle(ax, yf + 20, bz, 3, color=OUT, fill=True, fc=C_PIN, lw=0.7, zorder=8)
    # length SPLICE (GHOST) — the 2362 mm wall-to-wall rail also exceeds 6 ft stock, so it too takes one splice
    sx = 900
    ax.add_patch(plt.Rectangle((sx - 55, rz0), 110, rz1 - rz0, fc="none", ec=OUT, lw=1.0, ls=(0, (5, 3)), zorder=8))
    leader(ax, sx, rz1, sx + 40, 132, "length SPLICE (web-back, GHOST) — rail > 6 ft stock",
           ha="left", fs=5.8, color=DIM, font=FONT, bbox=LBL_BG)
    leader(ax, 20, rz1, 120, 132, "end flange → wall (through-bolted)", ha="left", fs=5.8, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, C_WID - 20, rz0 - 4, C_WID - 260, -44, "outboard end plate trimmed 35mm (IBC clearance);\nshares the IBC combined corner plate",
           ha="left", fs=5.8, color=OUT, font=FONT, bbox=LBL_BG)
    ax.text(-260, 146, "RIGHT RAIL — FLANGED WALL-TO-WALL  (permanent; no transport split)",
            fontsize=7.4, fontweight="bold", color=OUT, ha="left", va="top", **FONT)


def sheet4():
    reset_label_registry()
    fig = plt.figure(figsize=(15, 11)); fig.patch.set_facecolor(BG)
    ax_te = fig.add_axes([0.03, 0.56, 0.94, 0.40]); ax_te.set_facecolor(BG)
    ax_rf = fig.add_axes([0.03, 0.34, 0.94, 0.18]); ax_rf.set_facecolor(BG)
    transport_elev(ax_te)
    right_flanged(ax_rf)

    # notes
    ax_n = fig.add_axes([0.03, 0.075, 0.94, 0.25]); ax_n.set_xlim(0, 100); ax_n.set_ylim(0, 100); ax_n.axis("off")
    draw_notes(ax_n, [
        "RAIL MOUNTING & TRANSPORT:",
        "1. RIGHT rail (BR/TR) is flanged WALL-TO-WALL — an end flange through-bolted to each container wall, "
        "sharing the IBC combined corner plate; it never comes apart. The panel folds away from this side.",
        "2. LEFT rail (BL/TL) is a TRANSPORT DROP-IN: the hinge panel folds about the pivot post (Yd "
        f"{PIVOT_YD}) and sweeps the X150 rail line, so the near ~{LEFT_CUT_YD}mm of BOTH left rails (top + "
        "bottom) LIFTS OUT. The fixed STUB parks the corner and is anchored at the pivot post + far wall.",
        "3. At the cut: a BRIDGE (fishplate) sits ON TOP and is WELDED to the REMOVABLE beam, lapping onto the "
        "STUB — GRAVITY bears the removable's end on the stub through the bridge (the WEIGHT rides the bridge, "
        "not the fastener). A retaining SCREW into the stub stops it lifting (hand-releasable): the removable "
        "drops straight in and the screw stays unloaded. No floor post at the cut — the stub cantilevers only ~"
        f"{PIVOT_YD - LEFT_CUT_YD}mm from the pivot post, so nothing fouls the sliding carriage.",
        "4. Each removable exceeds 6 ft stock, so a length SPLICE sits at the PINHOLE end (Yd ~"
        f"{SPLICE_YD}) — the shortest-throw, least-travelled zone, least likely for the skate to roll over it.",
        "5. The length-SPLICE fishplate sits on the OUTBOARD WEB-BACK (far side, ghosted), clear of the rollers; "
        "the cut BRIDGE sits on top (gravity-held). U-joint stub→carrier clamp (4040N12) + U-joint body: Sheet 3.",
    ], 2, 99, 4.7, fs=6.2, title_fs=6.8, color=DIM, width=96, wrap=132, font=FONT)

    ax_tb = fig.add_axes([0.03, 0.008, 0.94, 0.052]); ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1)
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 4 OF 7", drawing_title="MOVEABLE FILM PLANE",
                subtitle="Rail mounting & transport drop-in — left split (stub + removable + web-back bridge) · right flanged wall-to-wall",
                scale_note="DIMS IN mm",
                doc_id="TBS-FM01 · Film Plane Mechanism",
                height=0.75)

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet4.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet4.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 5 — MOVEMENT SPECIFICATION TABLE & BOM (Option A — rigid plane)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet5():
    fig, ax = plt.subplots(figsize=(16, 13))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis("off")

    ax.text(0.5, 0.968, "SHEET 5 — MOVEMENT SPECIFICATION",
            transform=ax.transAxes, color=WHITE, fontsize=13, ha="center",
            fontweight="bold", **FONT)
    ax.text(0.5, 0.948, f"TBS-001  ·  MOVEABLE FILM PLANE  ·  RAILS: X={RAIL_X_L}–{RAIL_X_R}mm  SPAN={RAIL_X_R-RAIL_X_L}mm  MAX SWING={MAX_SWING_DEG:.1f}deg",
            transform=ax.transAxes, color=DIM, fontsize=8.5, ha="center", **FONT)

    # row_h=0.022 fits 31 rows across 3 tables in the available page height.
    # At figsize height 13in: row height = 0.022×13×72 ≈ 20.6pt — comfortable for 7pt font.
    def draw_table(ax, x0, y0, headers, rows, col_widths, row_h=0.022,
                   hdr_col=STRUCT2, row_cols=(GRID, BG)):
        total_w = sum(col_widths)
        xc = x0
        ax.add_patch(Rectangle((x0, y0), total_w, row_h*1.2,
                               transform=ax.transAxes,
                               fc=hdr_col, ec=WHITE, lw=0.8, zorder=3, clip_on=False))
        for h, cw in zip(headers, col_widths):
            ax.text(xc+cw/2, y0+row_h*0.6, h,
                    transform=ax.transAxes, color=WHITE, fontsize=7.2,
                    ha="center", va="center", fontweight="bold", **FONT)
            xc += cw
        for ri, row in enumerate(rows):
            ry = y0 - (ri+1)*row_h
            fc = row_cols[ri % 2]
            ax.add_patch(Rectangle((x0, ry), total_w, row_h,
                                   transform=ax.transAxes,
                                   fc=fc, ec=GRID, lw=0.5, zorder=2, clip_on=False))
            xc = x0
            for cell, cw in zip(row, col_widths):
                col_text = WHITE if ri == 0 else ANNO
                ax.text(xc+cw/2, ry+row_h*0.5, str(cell),
                        transform=ax.transAxes, color=col_text, fontsize=6.8,
                        ha="center", va="center", **FONT)
                xc += cw

    # ── Table 1: Axis movement summary ────────────────────────────────────────
    # label sits 0.012 above header top: label_y = y0 + row_h*1.2 + 0.012
    # y0=0.895 → header top=0.895+0.026=0.921 → label at 0.933
    ax.text(0.05, 0.933, "TABLE 1 — MOVEMENT AXES",
            transform=ax.transAxes, color=DIM, fontsize=8, fontweight="bold", **FONT)

    axes_headers = ["AXIS", "DESCRIPTION", "CORNERS\nCONTROLLED", "MAX TRAVEL", "ACTUATOR", "LOCK"]
    axes_rows = [
        ["TILT (top)",    "Both top corners move equally",      "TL + TR together", f"0–{FP_Y}mm", "2× depth slide — push both", "2 cam clamps"],
        ["TILT (bottom)", "Both bottom corners move equally",   "BL + BR together", f"0–{FP_Y}mm", "2× depth slide — push both", "2 cam clamps"],
        ["SWING (left)",  "Both left corners move equally",     "TL + BL together", f"0–{FP_Y}mm", "2× depth slide — push both", "2 cam clamps"],
        ["SWING (right)", "Both right corners move equally",    "TR + BR together", f"0–{FP_Y}mm", "2× depth slide — push both", "2 cam clamps"],
        ["COMBINED",      "Limited tilt+swing — rigid, stays FLAT", "TL, TR, BL, BR", f"0–{FP_Y}mm", "4 depth slides, coordinated","4 cam clamps"],
        ["BACK FOCUS",    "All 4 corners together",             "All",              f"{FP_Y_MIN}–{FP_Y}mm","All 4 depth slides together", "All 4 clamps"],
        ["MAX TILT",      "Top=414mm, Bot=1948mm (axis tilt)",  "TL=TR, BL=BR",     f"{MAX_TILT_DEG:.0f}deg (Z-slide-lim.)",  "Top+top / Bot+bot",        "All 4 clamps"],
        ["MAX SWING",     "Left=125mm, Right=2237mm (axis swing)","TL=BL, TR=BR",    f"{MAX_SWING_DEG:.0f}deg (rail-lim.)", "Left+left / Right+right",  "All 4 clamps"],
    ]
    # y0=0.895; header top=0.895+0.026=0.921; bottom=0.895-8×0.022=0.719
    draw_table(ax, 0.05, 0.895, axes_headers, axes_rows,
               [0.12, 0.22, 0.15, 0.10, 0.22, 0.14])

    # ── Table 2: Config specs ─────────────────────────────────────────────────
    # T1 bottom=0.719; gap=0.025; label=0.694; y0=0.656; bottom=0.656-8×0.022=0.480
    ax.text(0.05, 0.694, "TABLE 2 — EXAMPLE TILT/SWING CONFIGURATION SPECS",
            transform=ax.transAxes, color=DIM, fontsize=8, fontweight="bold", **FONT)

    # Option A (rigid axis tilt/swing about the mid-rail centre). Corner depths are
    # DERIVED from the rotation; the plane stays a flat fixed-size rectangle, so no
    # compound TWIST and no growth. Combined tilt+swing is limited (corners on rails).
    config_defs = [
        ("Flat",            0.0,  0.0,  "Reference (flat, fixed size)"),
        ("Tilt mild",      11.0,  0.0,  "subtle keystone"),
        ("Tilt strong",    30.0,  0.0,  "strong keystone"),
        ("Tilt max",       40.0,  0.0,  "max tilt (cross-slide-Z limited)"),
        ("Swing mild",      0.0, 11.0,  "diagonal slant"),
        ("Swing strong",    0.0, 22.0,  "strong left-right skew"),
        ("Swing max",       0.0, 28.0,  "max swing (rail-depth limited)"),
        ("Tilt+Swing",     14.0, 10.0,  "limited combined — rigid, stays flat"),
    ]

    cfg_headers = ["CONFIG", "TL mm", "TR mm", "BL mm", "BR mm",
                   "TILT ANG.", "SWING ANG.", "PRINCIPAL EFFECT"]
    cfg_rows = []
    for (name, tdeg, sdeg, effect) in config_defs:
        C = rigid_corners3d(tdeg, sdeg, D_CTR)
        d = {k: round(C[k][1]) for k in ("TL", "TR", "BL", "BR")}
        cfg_rows.append([name, d["TL"], d["TR"], d["BL"], d["BR"],
                         f"{tdeg:.0f}°", f"{sdeg:.0f}°", effect])

    draw_table(ax, 0.05, 0.656, cfg_headers, cfg_rows,
               [0.13, 0.07, 0.07, 0.07, 0.07, 0.08, 0.09, 0.37])

    # ── Operating-modes note block ────────────────────────────────────────────
    # draw_notes uses data coordinates; sheet4 uses transAxes for layout,
    # so we render directly via ax.text with transAxes=True calls instead.
    modes_lines = [
        "FILM-PLANE TRAVEL",
        f"FILM MODE: with the LEFT rails in place, each carriage is free over the FULL travel (Yd 100–{FP_Y})",
        "   for tilt / swing / back-focus — no drum interlock.",
        "TRANSPORT: the LEFT rails (top + bottom) LIFT OUT at the cut so the hinge panel folds (see Sheet 4).",
        f"DRUM: offset out via the hinge-panel punch-out bay (center X={DRUM_CX}mm), clearing the X=150 left rail.",
        f"WALKWAY: film-plane bottom RAISED to Z={RAIL_OFF_BOT}mm (RAIL_OFF_BOT) to clear the Z{WALKWAY_H} walkway deck;",
        "   active image = the inter-rail span — the plane travels above the in-place walkway.",
    ]
    line_h = 0.030
    block_top = 0.46
    block_left = 0.05
    # Border background
    block_h = len(modes_lines) * line_h + 0.018
    ax.add_patch(Rectangle((block_left - 0.005, block_top - block_h + 0.005),
                            0.90, block_h,
                            transform=ax.transAxes,
                            fc=GRID, ec=DIM, lw=0.8, zorder=3, clip_on=False))
    for li, line in enumerate(modes_lines):
        ty = block_top - li * line_h
        fw = "bold" if li == 0 else "normal"
        col = WHITE if li == 0 else ANNO
        ax.text(block_left, ty, line,
                transform=ax.transAxes, color=col, fontsize=7,
                ha="left", va="top", fontweight=fw, **FONT)

    # BOM detail lives in master-shopping-list.md §4 — sheet carries a per-corner summary
    hw_lines = [
        "CORNER HARDWARE (per corner ×4 — acetal skate + cross-slides + single U-joint):",
        "U-joint  1× Ruland US12-6-6-SS (303 SS, self-lube bronze, 45°)   ·   boot  1× Ruland UBOOT12/19-NI-KIT (nitrile, fitted dry)",
        "Shaft support  2× McMaster 4040N12 (304 SS)   ·   stub  2× 3/8\" 304 SS (McMaster 89535K873)",
        "SKATE  Ø32 acetal rollers ×4 (2 load + 2 keeper) on Ø10 316 axles + carriage plate + inboard lip   ·   Z/X cross-slides  316 flat bar ¼\"×1.5\" + UHMW pads + adjustable gib   ·   cam clamp ×3",
        "DEPTH RAIL  3×1.5 (76×38) 304 U-channel (McMaster 1262T21), wall-to-wall   ·   RIGHT flanged   ·   LEFT transport drop-in (stub + removable + welded bridge + retaining screw + pinhole gusset)",
        "Full bill of materials: master-shopping-list.md — §4 Film Plane Mechanism",
    ]
    hw_top, hw_lh = 0.205, 0.026
    for li, line in enumerate(hw_lines):
        fw = "bold" if li == 0 else "normal"
        col = WHITE if li == 0 else ANNO
        st = "italic" if li == len(hw_lines) - 1 else "normal"
        ax.text(0.06, hw_top - li * hw_lh, line,
                transform=ax.transAxes, color=col, fontsize=6.6,
                ha="left", va="top", fontweight=fw, style=st, **FONT)

    # Title block
    title_block(ax, "SHEET 5 OF 7",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="Movement specification & BOM",
                scale_note="Not to scale",
                doc_id="TBS-FM01 · Film Plane Mechanism")

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet5.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet5.png")


# ═══════════════════════════════════════════════════════════════════════════════
# Sheet 6 — Muslin Clamp Detail: Cam-Lever Spring Clamp
#
# Three sub-panels:
#   A (top-left):  Cross-section of clamp on 2"×2" aluminum angle profile
#   B (top-right): Clamp in open vs closed positions (side view)
#   C (bottom):    Elevation: 3 clamps at 150mm spacing along frame edge
# ═══════════════════════════════════════════════════════════════════════════════
def sheet6():
    from tbs_constants import (
        FP_ANGLE_LEG, FP_ANGLE_T, CLAMP_SPACING, CLAMP_BASE_W, CLAMP_BASE_H,
        CLAMP_BASE_T, CLAMP_LEVER_L, CLAMP_JAW_W, CLAMP_JAW_H, CLAMP_JAW_T,
        CLAMP_OPEN_GAP, CLAMP_SPRING_F, CLAMP_N_TOTAL,
    )

    C_ALUM    = "#C8D8E8"   # aluminum section fill
    C_CLAMP   = "#D4522A"   # clamp mechanism (burnt orange)
    C_NEOP    = "#333333"   # neoprene jaw pad
    C_MUSLIN  = "#D4B896"   # muslin fabric (warm tan — visible on white bg)
    C_BOLT    = "#505058"   # bolt hardware

    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor(BG)

    # ── PANEL A: Context cross-section — ceiling rail to muslin (top-left) ────
    ax_a = fig.add_axes([0.04, 0.45, 0.46, 0.48])
    ax_a.set_facecolor(BG)
    ax_a.axis("off")


    LEG = FP_ANGLE_LEG   # 50.8mm
    T   = FP_ANGLE_T     # 4.8mm

    # Geometry constants for the suspension chain
    RAIL_H = 30       # 3×1.5 304 U-channel depth rail height (schematic)
    RAIL_W = 20       # 3×1.5 304 U-channel depth rail visible width (schematic)
    CARRIAGE_H = 28   # UHMW-pad carriage height (schematic)
    CARRIAGE_W = 44   # UHMW-pad carriage width (schematic)
    BRACKET_H = 40    # suspension bracket height
    BRACKET_W = 60    # suspension bracket width
    LBRACKET_H = 50   # corner L-bracket vertical extent
    LBRACKET_W = 40   # corner L-bracket horizontal extent
    LBRACKET_T = 6    # 1/4" aluminum plate
    BEARING_D = 25    # U-joint hub (schematic)
    CEILING_T = 8     # visual ceiling thickness

    # Coordinate system: angle corner at (0, 0).
    # Positive Y = up toward ceiling. Negative Y = down toward floor.
    # Positive X = toward pinhole (horizontal leg direction).

    # Stack heights above angle frame top (Y=T):
    lbracket_bot = T + 5          # small gap above angle
    lbracket_top = lbracket_bot + LBRACKET_H
    bearing_cy = lbracket_top - 15  # bearing center in L-bracket
    bracket_bot = lbracket_top + 5
    bracket_top = bracket_bot + BRACKET_H
    carriage_bot = bracket_top
    carriage_top = carriage_bot + CARRIAGE_H
    rail_bot = carriage_top
    rail_top = rail_bot + RAIL_H
    ceiling_bot = rail_top
    ceiling_top = ceiling_bot + CEILING_T

    ax_a.set_xlim((-35), (LEG + 85))
    ax_a.set_ylim((-LEG - 10), (ceiling_top + 15))
    ax_a.set_aspect("equal")

    # ── Ceiling ──────────────────────────────────────────────────────────────
    C_CEIL = "#A0A0A0"
    ax_a.add_patch(Rectangle(((-30), (ceiling_bot)),
                              (LEG + 110), (CEILING_T),
                              fc=C_CEIL, ec=ANNO, lw=1.2, hatch="xxx", zorder=3))
    ax_a.text((LEG + 85), (ceiling_bot + CEILING_T / 2),
              "CONTAINER\nCEILING", ha="left", va="center",
              fontsize=5, color=DIM, **FONT, zorder=15)

    # ── 304 U-channel depth rail (bolted to ceiling, hangs down) ──────────────
    C_RAIL = "#708090"
    rail_cx = LEG / 2  # centered on angle
    ax_a.add_patch(Rectangle(((rail_cx - RAIL_W / 2), (rail_bot)),
                              (RAIL_W), (RAIL_H),
                              fc=C_RAIL, ec=ANNO, lw=1.2, zorder=4))
    leader(ax_a, (rail_cx), (rail_bot + RAIL_H / 2),
           (rail_cx + 50), (rail_bot + RAIL_H / 2),
           "3×1.5 304 U-CHANNEL\nDEPTH RAIL",
           color=C_RAIL, fs=5.5, ha="left", va="center",
           arrow_style="-|>", font=FONT)

    # ── Acetal skate + carriage plate ────────────────────────────────────────
    C_CARR = "#607080"
    ax_a.add_patch(Rectangle(((rail_cx - CARRIAGE_W / 2), (carriage_bot)),
                              (CARRIAGE_W), (CARRIAGE_H),
                              fc=C_CARR, ec=ANNO, lw=1.2, zorder=5))
    leader(ax_a, (rail_cx + CARRIAGE_W / 2), (carriage_bot + CARRIAGE_H / 2),
           (rail_cx + 55), (carriage_bot + CARRIAGE_H / 2 - 10),
           "acetal SKATE\n+ carriage plate",
           color=C_CARR, fs=5.5, ha="left", va="center",
           arrow_style="-|>", font=FONT)

    # ── Z (tilt) + X (swing) cross-slides — the suspension stack ──────────────
    C_ZS = "#2E8B57"   # Z tilt slide (green)
    C_XS = "#7B5EA7"   # X swing slide (purple)
    half = BRACKET_H / 2
    ax_a.add_patch(Rectangle(((rail_cx - BRACKET_W / 2), (bracket_bot + half)),
                              (BRACKET_W), (half), fc=C_ZS, ec=ANNO, lw=1.0, zorder=4))
    ax_a.add_patch(Rectangle(((rail_cx - BRACKET_W / 2), (bracket_bot)),
                              (BRACKET_W), (half), fc=C_XS, ec=ANNO, lw=1.0, zorder=4))
    leader(ax_a, (rail_cx + BRACKET_W / 2), (bracket_bot + BRACKET_H * 0.75),
           (rail_cx + 55), (bracket_bot + BRACKET_H - 3),
           "Z cross-slide (TILT)", color=C_ZS, fs=5, ha="left", va="center",
           arrow_style="-|>", font=FONT)
    leader(ax_a, (rail_cx + BRACKET_W / 2), (bracket_bot + BRACKET_H * 0.25),
           (rail_cx + 55), (bracket_bot + 1),
           "X cross-slide (SWING)", color=C_XS, fs=5, ha="left", va="center",
           arrow_style="-|>", font=FONT)

    # ── Corner L-bracket (1/4" Al plate) ─────────────────────────────────────
    # Vertical part connects to bracket above; horizontal part connects to angle
    lbk_x = rail_cx - LBRACKET_W / 2
    # Vertical arm
    ax_a.add_patch(Rectangle(((lbk_x), (lbracket_bot)),
                              (LBRACKET_T), (LBRACKET_H),
                              fc=C_ALUM, ec=ANNO, lw=1.0, zorder=4))
    # Horizontal arm (connects to angle frame)
    ax_a.add_patch(Rectangle(((lbk_x), (lbracket_bot)),
                              (LBRACKET_W), (LBRACKET_T),
                              fc=C_ALUM, ec=ANNO, lw=1.0, zorder=4))
    leader(ax_a, (lbk_x + LBRACKET_T / 2 - 5), (lbracket_bot + LBRACKET_H / 2 - 10),
           (-25), (lbracket_bot + LBRACKET_H / 2),
           f"L-BRACKET\n(1/4\" Al PLATE)",
           color=DIM, fs=5, ha="right", va="center",
           arrow_style="-|>", font=FONT)

    # ── Single U-joint (Ruland US12-6-6-SS, bronze plain bearing) ─────────────
    C_BEAR = "#C08040"
    ax_a.add_patch(Circle(((lbk_x + LBRACKET_T / 2), (bearing_cy)),
                           (BEARING_D / 2),
                           fc=C_BEAR, ec=ANNO, lw=1.0, zorder=6))
    ax_a.add_patch(Circle(((lbk_x + LBRACKET_T / 2), (bearing_cy)),
                           (BEARING_D / 4),
                           fc=BG, ec=ANNO, lw=0.8, zorder=7))
    leader(ax_a, (lbk_x - 2), (bearing_cy),
           (-25), (bearing_cy + 15),
           f"SINGLE U-JOINT\nUS12-6-6-SS\n(TILT/SWING,\nTWIST-LOCKED)",
           color=C_BEAR, fs=5, ha="right", va="center",
           arrow_style="-|>", font=FONT)

    # ── Aluminum angle — L-profile ───────────────────────────────────────────
    # Pinhole-facing leg: horizontal
    ax_a.add_patch(Rectangle(((0), (0)), (LEG), (T),
                              fc=C_ALUM, ec=ANNO, lw=1.5, zorder=3))
    # Perpendicular leg: vertical (going down)
    ax_a.add_patch(Rectangle(((0), (-LEG + T)), (T), (LEG - T),
                              fc=C_ALUM, ec=ANNO, lw=1.5, zorder=3))
    # Hatching
    ax_a.add_patch(Rectangle(((0), (0)), (LEG), (T),
                              fc="none", ec="#8898A8", lw=0.3, hatch="///", zorder=4))
    ax_a.add_patch(Rectangle(((0), (-LEG + T)), (T), (LEG - T),
                              fc="none", ec="#8898A8", lw=0.3, hatch="///", zorder=4))

    ax_a.text((LEG / 2), (T + 3), "PINHOLE-FACING LEG",
              ha="center", va="bottom", fontsize=5, color=DIM, **FONT, zorder=15)
    ax_a.text((-5), (-LEG / 2 + T), "PERP. LEG",
              ha="right", va="center", fontsize=5, color=DIM, rotation=90, **FONT, zorder=15)

    # ── Muslin wrap path ──────────────────────────────────────────────────────
    muslin_t = 1.5
    hem_end = -CLAMP_BASE_H

    muslin_pts_x = [(LEG + 10), (LEG), (LEG), (LEG + muslin_t),
                    (LEG + muslin_t), (T + muslin_t), (T + muslin_t)]
    muslin_pts_y = [(T / 2), (T / 2), (T + muslin_t), (T + muslin_t),
                    (T + muslin_t), (T + muslin_t), (hem_end)]

    ax_a.plot(muslin_pts_x, muslin_pts_y, color=C_MUSLIN, lw=5, solid_capstyle="round",
              zorder=5, alpha=0.9)
    ax_a.plot(muslin_pts_x, muslin_pts_y, color=ANNO, lw=1.0, zorder=6)

    leader(ax_a, (LEG + 5), (T + muslin_t + 2),
           (LEG + 40), (T + 20),
           "MUSLIN\n(100mm HEM)", color=C_MUSLIN, fs=5,
           ha="left", va="center", arrow_style="-|>", font=FONT)

    # ── Clamp base plate ─────────────────────────────────────────────────────
    base_x = T
    base_y_bot = -CLAMP_BASE_H
    ax_a.add_patch(Rectangle(((base_x), (base_y_bot)),
                              (CLAMP_BASE_T), (CLAMP_BASE_H),
                              fc=C_CLAMP, ec=ANNO, lw=1.2, zorder=7, alpha=0.9))

    # M5 bolts
    bolt_z1 = -15
    bolt_z2 = -35
    bolt_d = 5
    for bz in [bolt_z1, bolt_z2]:
        ax_a.add_patch(Rectangle(((0), (bz - bolt_d * 0.2)),
                                  (T + CLAMP_BASE_T), (bolt_d * 0.4),
                                  fc=C_BOLT, ec=ANNO, lw=0.6, zorder=10))
        ax_a.add_patch(Rectangle(((-4), (bz - bolt_d * 0.5)),
                                  (4), (bolt_d),
                                  fc=C_BOLT, ec=ANNO, lw=0.8, zorder=10))
        ax_a.add_patch(Rectangle(((T + CLAMP_BASE_T), (bz - bolt_d * 0.5)),
                                  (5), (bolt_d),
                                  fc=C_BOLT, ec=ANNO, lw=0.8, zorder=10))

    # ── Cam lever + jaw (closed) ─────────────────────────────────────────────
    pivot_x = T + CLAMP_BASE_T / 2
    pivot_z = 0

    jaw_x = LEG - CLAMP_JAW_T
    jaw_z_top = T + muslin_t + CLAMP_JAW_H / 2
    jaw_z_bot = T + muslin_t - CLAMP_JAW_H / 2
    ax_a.add_patch(Rectangle(((jaw_x), (jaw_z_bot)),
                              (CLAMP_JAW_T), (CLAMP_JAW_H),
                              fc=C_NEOP, ec=ANNO, lw=1.0, zorder=8))

    ax_a.plot([(pivot_x), (jaw_x + CLAMP_JAW_T / 2)],
              [(pivot_z), (T + muslin_t)],
              color=C_CLAMP, lw=2.5, solid_capstyle="round", zorder=7)

    ax_a.add_patch(Circle(((pivot_x), (pivot_z)), (2.5),
                           fc=C_CLAMP, ec=ANNO, lw=1.0, zorder=9))

    # Spring schematic
    sp_x = pivot_x + 5
    sp_z = pivot_z + 3
    spring_xs = [(sp_x), (sp_x + 2), (sp_x + 4), (sp_x + 6),
                 (sp_x + 8), (sp_x + 10)]
    spring_zs = [(sp_z), (sp_z + 3), (sp_z - 2), (sp_z + 3),
                 (sp_z - 2), (sp_z)]
    ax_a.plot(spring_xs, spring_zs, color=C_CLAMP, lw=1.0, zorder=8)

    # Leader labels for clamp components
    leader(ax_a, (T + CLAMP_BASE_T + 6), (bolt_z1),
           (LEG - 20), (bolt_z1 - 20),
           f"M5 BOLT + NYLOCK\n(2 PER CLAMP)", color=C_BOLT, fs=5,
           ha="left", va="center", arrow_style="-|>", font=FONT)

    leader(ax_a, (jaw_x + CLAMP_JAW_T / 2), (jaw_z_top + 1),
           (LEG), (jaw_z_top + 25),
           f"NEOPRENE JAW\n60A SHORE", color=C_NEOP, fs=5,
           ha="left", va="center", arrow_style="-|>", font=FONT)

    leader(ax_a, (pivot_x + 3), (pivot_z - 5),
           (LEG + 40), (-20),
           f"CAM LEVER\nCLOSED", color=C_CLAMP, fs=5,
           ha="left", va="center", arrow_style="-|>", font=FONT)

    # ── Load path annotation (right side) ────────────────────────────────────
    # Vertical arrow showing load path direction
    path_x = LEG + 70
    arrow_positions = [
        (ceiling_bot - 2, "CEILING"),
        (rail_bot + RAIL_H / 2, "DEPTH TROLLEY"),
        (carriage_bot + CARRIAGE_H / 2, "CARRIAGE"),
        (bracket_bot + BRACKET_H / 2, "BRACKET"),
        (bearing_cy, "U-JOINT"),
        (lbracket_bot + 5, "L-BRACKET"),
        (T / 2, "ANGLE FRAME"),
        (-25, "CLAMP"),
        (-LEG + T, "MUSLIN"),
    ]
    for i in range(len(arrow_positions) - 1):
        y1 = arrow_positions[i][0]
        y2 = arrow_positions[i + 1][0]
        ax_a.annotate("", xy=((path_x), (y2 + 3)),
                      xytext=((path_x), (y1 - 3)),
                      arrowprops=dict(arrowstyle="-|>", color="#C04010",
                                      lw=1.0, alpha=0.6))

    ax_a.text((path_x), (ceiling_top + 5),
              "LOAD\nPATH", ha="center", va="bottom",
              fontsize=5, color="#C04010", fontweight="bold", **FONT, zorder=15)

    # Panel title
    ax_a.text((LEG / 2), (ceiling_top + 12),
              "PANEL A — CONTEXT: CEILING RAIL TO MUSLIN",
              ha="center", va="bottom", fontsize=7, color=ANNO,
              fontweight="bold", **FONT, zorder=15)
    ax_a.text((LEG / 2), (ceiling_top + 6),
              "AXES IN mm · CROSS-SECTION SHOWING FULL SUSPENSION CHAIN",
              ha="center", va="bottom", fontsize=5.5, color=DIM, **FONT, zorder=15)

    # ── PANEL B: Open vs closed positions (top-right) ────────────────────────
    ax_b = fig.add_axes([0.54, 0.45, 0.42, 0.48])
    ax_b.set_facecolor(BG)
    ax_b.axis("off")


    ax_b.set_xlim((-40), (LEG + 120))
    ax_b.set_ylim((-100), (LEG + CLAMP_LEVER_L + 10))
    ax_b.set_aspect("equal")

    # Simplified angle profile (side view — just the pinhole-facing leg top edge)
    ax_b.add_patch(Rectangle(((0), (0)), (LEG), (T),
                              fc=C_ALUM, ec=ANNO, lw=1.2, hatch="///", zorder=3))
    ax_b.add_patch(Rectangle(((0), (-LEG + T)), (T), (LEG - T),
                              fc=C_ALUM, ec=ANNO, lw=1.2, hatch="///", zorder=3))

    # Base plate
    b_x = T
    ax_b.add_patch(Rectangle(((b_x), (-CLAMP_BASE_H)),
                              (CLAMP_BASE_T), (CLAMP_BASE_H),
                              fc=C_CLAMP, ec=ANNO, lw=1.0, zorder=5, alpha=0.9))

    pv_x = T + CLAMP_BASE_T / 2
    pv_z = 0

    # Muslin wrap on pinhole-facing leg (same path as Panel A)
    muslin_b_pts_x = [(LEG + 8), (LEG), (LEG), (LEG + 1.5),
                      (LEG + 1.5), (T + 1.5), (T + 1.5)]
    muslin_b_pts_y = [(T / 2), (T / 2), (T + 1.5), (T + 1.5),
                      (T + 1.5), (T + 1.5), (-CLAMP_BASE_H)]
    ax_b.plot(muslin_b_pts_x, muslin_b_pts_y, color=C_MUSLIN, lw=4,
              solid_capstyle="round", zorder=4, alpha=0.9)
    ax_b.plot(muslin_b_pts_x, muslin_b_pts_y, color=ANNO, lw=0.8, zorder=4.5)

    # ── CLOSED position (solid) ──────────────────────────────────────────────
    jaw_x_closed = LEG - CLAMP_JAW_T
    jaw_z_closed = T + 2  # pressing against muslin on pinhole leg face
    ax_b.add_patch(Rectangle(((jaw_x_closed), (jaw_z_closed)),
                              (CLAMP_JAW_T), (CLAMP_JAW_H),
                              fc=C_NEOP, ec=ANNO, lw=1.0, zorder=7))
    ax_b.plot([(pv_x), (jaw_x_closed + CLAMP_JAW_T / 2)],
              [(pv_z), (jaw_z_closed + CLAMP_JAW_H / 2)],
              color=C_CLAMP, lw=3, solid_capstyle="round", zorder=6)
    ax_b.add_patch(Circle(((pv_x), (pv_z)), (3),
                           fc=C_CLAMP, ec=ANNO, lw=1.0, zorder=8))
    ax_b.text((jaw_x_closed - 3), (jaw_z_closed + CLAMP_JAW_H / 2),
              "CLOSED", ha="right", va="center", fontsize=6, color=C_CLAMP,
              fontweight="bold", **FONT, zorder=15)

    # ── OPEN position (dashed, rotated ~120 degrees from closed) ─────────────
    import math
    # Closed angle from pivot to jaw
    dx_c = (jaw_x_closed + CLAMP_JAW_T / 2) - pv_x
    dz_c = (jaw_z_closed + CLAMP_JAW_H / 2) - pv_z
    closed_angle = math.atan2(dz_c, dx_c)
    lever_len = math.sqrt(dx_c**2 + dz_c**2)
    open_angle = closed_angle + math.radians(120)  # flip open 120 degrees

    open_end_x = pv_x + lever_len * math.cos(open_angle)
    open_end_z = pv_z + lever_len * math.sin(open_angle)

    ax_b.plot([(pv_x), (open_end_x)],
              [(pv_z), (open_end_z)],
              color=C_CLAMP, lw=2.5, ls="--", alpha=0.5, zorder=5)

    # Open jaw position
    jaw_open_x = open_end_x - CLAMP_JAW_T / 2
    jaw_open_z = open_end_z - CLAMP_JAW_H / 2
    ax_b.add_patch(Rectangle(((jaw_open_x), (jaw_open_z)),
                              (CLAMP_JAW_T), (CLAMP_JAW_H),
                              fc=C_NEOP, ec=ANNO, lw=0.8, ls="--",
                              alpha=0.3, zorder=5))

    ax_b.text((open_end_x + 3), (open_end_z),
              "OPEN\n(120° FLIP)", ha="left", va="center", fontsize=6,
              color=C_CLAMP, alpha=0.7, fontweight="bold", **FONT, zorder=15)

    # Arc showing rotation
    arc_r = lever_len * 0.4
    arc_start_deg = math.degrees(closed_angle)
    arc_end_deg = math.degrees(open_angle)
    ax_b.add_patch(Arc(((pv_x), (pv_z)), (arc_r * 2), (arc_r * 2),
                        angle=0, theta1=arc_start_deg, theta2=arc_end_deg,
                        color=C_CLAMP, lw=1.0, ls=":", zorder=5, alpha=0.5))

    # Gap dimension when open
    draw_dim_h(ax_b, (T + CLAMP_BASE_T), (LEG), (-CLAMP_BASE_H - 10),
               f"{CLAMP_OPEN_GAP}mm GAP\n(OPEN)", offset=(3), fs=6, font=FONT)

    # Force annotation
    ax_b.annotate("", xy=((jaw_x_closed + CLAMP_JAW_T / 2), (jaw_z_closed)),
                  xytext=((jaw_x_closed + CLAMP_JAW_T / 2), (jaw_z_closed - 12)),
                  arrowprops=dict(arrowstyle="-|>", color="#208020", lw=1.5))
    ax_b.text((jaw_x_closed + CLAMP_JAW_T / 2), (jaw_z_closed - 14),
              f"~{CLAMP_SPRING_F}N\nCLAMP\nFORCE", ha="center", va="top",
              fontsize=5.5, color="#208020", fontweight="bold", **FONT, zorder=15)

    ax_b.text((LEG / 2), (LEG + CLAMP_LEVER_L - 5),
              "PANEL B — CLAMP OPEN vs CLOSED",
              ha="center", va="bottom", fontsize=8, color=ANNO,
              fontweight="bold", **FONT, zorder=15)
    ax_b.text((LEG / 2), (LEG + CLAMP_LEVER_L - 13),
              f"AXES IN mm · TORSION SPRING BIASES CLOSED",
              ha="center", va="bottom", fontsize=6, color=DIM, **FONT, zorder=15)

    # ── PANEL C: Plan view — clamp attachment to frame edge (bottom-left) ─────
    ax_c = fig.add_axes([0.04, 0.06, 0.46, 0.36])
    ax_c.set_facecolor(BG)
    ax_c.axis("off")


    # Plan view: looking down (Z-axis). X = along frame edge, Y = across frame.
    # Frame angle in plan: pinhole-facing leg runs along X,
    # perpendicular leg sticks out in +Y direction.
    frame_len = CLAMP_SPACING * 2 + 40  # show ~2 clamp spacings
    ax_c.set_xlim((-30), (frame_len + 30))
    ax_c.set_ylim((-50), (LEG + 50))
    ax_c.set_aspect("equal")

    # Pinhole-facing leg (horizontal bar along X, depth = LEG, thickness = T)
    ax_c.add_patch(Rectangle(((-10), (0)), (frame_len + 20), (T),
                              fc=C_ALUM, ec=ANNO, lw=1.2, hatch="///", zorder=3))
    ax_c.text((frame_len + 15), (T / 2), "PINHOLE-\nFACING LEG",
              ha="left", va="center", fontsize=5, color=DIM, **FONT, zorder=15)

    # Perpendicular leg — continuous strip in +Y from the angle corner
    ax_c.add_patch(Rectangle(((-10), (T)), (frame_len + 20), (LEG - T),
                              fc=C_ALUM, ec=ANNO, lw=1.2, hatch="///",
                              alpha=0.5, zorder=2))
    ax_c.text((frame_len + 15), (LEG / 2 + T / 2), "PERP.\nLEG",
              ha="left", va="center", fontsize=5, color=DIM, **FONT, zorder=15)

    # Muslin — draped over pinhole-facing leg (covers the full surface)
    ax_c.add_patch(Rectangle(((-10), (-8)), (frame_len + 20), (8 + T + 3),
                              fc=C_MUSLIN, ec=ANNO, lw=0.8, alpha=0.6, zorder=4))
    ax_c.text((frame_len / 2), (-12), "MUSLIN (DRAPES OVER PINHOLE LEG, HEM WRAPS AROUND CORNER)",
              ha="center", va="top", fontsize=5, color=DIM, style="italic", **FONT, zorder=15)

    # Draw 2 clamps in plan view
    for cx in [CLAMP_SPACING * 0.5, CLAMP_SPACING * 1.5]:
        # Base plate — bolted to outer face of perpendicular leg
        bp_y = LEG  # outer face of perp leg
        ax_c.add_patch(Rectangle(((cx - CLAMP_BASE_W / 2), (bp_y)),
                                  (CLAMP_BASE_W), (CLAMP_BASE_T),
                                  fc=C_CLAMP, ec=ANNO, lw=1.0, zorder=7, alpha=0.9))

        # M5 bolts (circles in plan view) — through base plate + perp leg
        for boff in [-12, 12]:
            bolt_cx = cx + boff
            ax_c.add_patch(Circle(((bolt_cx), (bp_y + CLAMP_BASE_T / 2)),
                                   (2.5), fc=C_BOLT, ec=ANNO, lw=0.6, zorder=9))

        # Lever arm — from base plate to jaw (in plan, it's a strip from
        # the perp leg outer face reaching over to the pinhole-facing leg)
        lever_tip_y = T + 2  # jaw presses on top of pinhole-facing leg
        ax_c.plot([(cx), (cx)],
                  [(bp_y), (lever_tip_y)],
                  color=C_CLAMP, lw=2.5, solid_capstyle="round", zorder=6)

        # Pivot dot at base plate
        ax_c.add_patch(Circle(((cx), (bp_y)), (2),
                               fc=C_CLAMP, ec=ANNO, lw=0.8, zorder=9))

        # Jaw pad (in plan view — width along frame edge, depth into frame)
        ax_c.add_patch(Rectangle(((cx - CLAMP_JAW_W / 2), (lever_tip_y - 1)),
                                  (CLAMP_JAW_W), (CLAMP_JAW_T),
                                  fc=C_NEOP, ec=ANNO, lw=0.8, zorder=8))

    # Leader labels
    clamp_x = CLAMP_SPACING * 0.5
    leader(ax_c, (clamp_x), (LEG + CLAMP_BASE_T / 2),
           (clamp_x - 40), (LEG + 30),
           f"BASE PLATE\n({CLAMP_BASE_W}×{CLAMP_BASE_H}×{CLAMP_BASE_T}mm)\n2× M5 BOLTS TO PERP LEG",
           color=C_CLAMP, fs=5, ha="center", va="center",
           arrow_style="-|>", font=FONT)

    leader(ax_c, (clamp_x), (T + 2),
           (clamp_x), (-25),
           f"NEOPRENE JAW\n({CLAMP_JAW_W}×{CLAMP_JAW_H}×{CLAMP_JAW_T}mm)\nPRESSES MUSLIN\nAGAINST FRAME",
           color=C_NEOP, fs=5, ha="center", va="center",
           arrow_style="-|>", font=FONT)

    # Spacing dimension
    draw_dim_h(ax_c, (CLAMP_SPACING * 0.5), (CLAMP_SPACING * 1.5),
               (LEG + 20), f"{CLAMP_SPACING}mm SPACING",
               offset=(3), fs=6, font=FONT)

    # Direction arrows / labels
    ax_c.annotate("", xy=((-20), (LEG / 2)), xytext=((-20), (LEG / 2 - 15)),
                  arrowprops=dict(arrowstyle="-|>", color=DIM, lw=1.0))
    ax_c.text((-25), (LEG / 2 - 8), "→ TO\nPINHOLE",
              ha="right", va="center", fontsize=5, color=DIM, **FONT, zorder=15)

    ax_c.text((frame_len / 2), (LEG + 42),
              "PANEL C — PLAN VIEW: CLAMP ATTACHMENT TO FRAME EDGE",
              ha="center", va="bottom", fontsize=8, color=ANNO,
              fontweight="bold", **FONT, zorder=15)
    ax_c.text((frame_len / 2), (LEG + 35),
              f"AXES IN mm · LOOKING DOWN (Z-AXIS) AT FRAME EDGE",
              ha="center", va="bottom", fontsize=6, color=DIM, **FONT, zorder=15)

    # ── PANEL D: Elevation — 3 clamps at 150mm spacing (bottom-right) ────────
    ax_d = fig.add_axes([0.54, 0.06, 0.42, 0.36])
    ax_d.set_facecolor(BG)
    ax_d.axis("off")


    span = CLAMP_SPACING * 3  # show 3 spacings = 450mm
    ax_d.set_xlim((-50), (span + 60))
    ax_d.set_ylim((-LEG - 30), (T + CLAMP_JAW_H + 40))
    ax_d.set_aspect("equal")

    # Frame angle profile — shown as continuous bar (pinhole-facing leg seen end-on)
    ax_d.add_patch(Rectangle(((-20), (0)), (span + 70), (T),
                              fc=C_ALUM, ec=ANNO, lw=1.0, hatch="///", zorder=3))

    # Muslin (continuous line across top of frame)
    muslin_y = T + 2
    ax_d.plot([(-20), (span + 50)], [(muslin_y), (muslin_y)],
              color=C_MUSLIN, lw=6, solid_capstyle="butt", alpha=0.9, zorder=4)
    ax_d.plot([(-20), (span + 50)], [(muslin_y), (muslin_y)],
              color=ANNO, lw=1.0, zorder=5)

    # Draw 3 clamps at 0, 150, 300mm
    for i, cx in enumerate([0, CLAMP_SPACING, CLAMP_SPACING * 2]):
        # Perpendicular leg (going down)
        ax_d.add_patch(Rectangle(((cx - T / 2), (-LEG + T)),
                                  (T), (LEG - T),
                                  fc=C_ALUM, ec=ANNO, lw=0.8, zorder=3))

        # Base plate on perp leg
        bp_x = cx + T / 2
        ax_d.add_patch(Rectangle(((bp_x), (-CLAMP_BASE_H)),
                                  (CLAMP_BASE_T), (CLAMP_BASE_H),
                                  fc=C_CLAMP, ec=ANNO, lw=0.8, zorder=6, alpha=0.9))

        # Lever arm (simplified)
        pv_cx = bp_x + CLAMP_BASE_T / 2
        jaw_cx = cx + LEG / 2
        ax_d.plot([(pv_cx), (jaw_cx)],
                  [(0), (T + 2)],
                  color=C_CLAMP, lw=2.5, solid_capstyle="round", zorder=6)

        # Pivot dot
        ax_d.add_patch(Circle(((pv_cx), (0)), (2),
                               fc=C_CLAMP, ec=ANNO, lw=0.8, zorder=8))

        # Jaw pad
        ax_d.add_patch(Rectangle(((jaw_cx - CLAMP_JAW_T / 2), (muslin_y - 1)),
                                  (CLAMP_JAW_T), (CLAMP_JAW_H),
                                  fc=C_NEOP, ec=ANNO, lw=0.8, zorder=7))

    # Spacing dimension lines
    for i in range(2):
        x1 = CLAMP_SPACING * i
        x2 = CLAMP_SPACING * (i + 1)
        draw_dim_h(ax_d, (x1), (x2), (-LEG - 10),
                   f"{CLAMP_SPACING}mm", offset=(4), fs=6, font=FONT)

    ax_d.text((span / 2), (T + CLAMP_JAW_H + 30),
              "PANEL D — ELEVATION: CLAMPS AT 150mm SPACING",
              ha="center", va="bottom", fontsize=7, color=ANNO,
              fontweight="bold", **FONT, zorder=15)
    ax_d.text((span / 2), (T + CLAMP_JAW_H + 22),
              f"AXES IN mm · {CLAMP_N_TOTAL} CLAMPS TOTAL",
              ha="center", va="bottom", fontsize=5.5, color=DIM, **FONT, zorder=15)

    # Notes — placed in panel B (top-right), below diagram content
    notes = [
        "CLAMP NOTES:",
        f"1. {CLAMP_N_TOTAL} cam-lever clamps at {CLAMP_SPACING}mm centers around full frame perimeter.",
        f"2. Base plate: 6061-T6 aluminum {CLAMP_BASE_W}×{CLAMP_BASE_H}×{CLAMP_BASE_T}mm, 2× M5 bolts to perp leg.",
        f"3. Neoprene jaw pad (60A shore) grips muslin without tearing.",
        f"4. Torsion spring biases clamp closed at any tilt angle.",
        f"5. Over-center cam action: snap open/closed by feel in safelight conditions.",
    ]
    notes_x = (-LEG+20)
    notes_y_start = (-65)
    draw_notes(ax_b, notes, notes_x, notes_y_start, spacing=(5),
               fs=7, title_fs=7.5, color=DIM, title_color=ANNO, font=FONT,
               width=(165))

    # ── Title block ───────────────────────────────────────────────────────────
    # Create a full-width axes at the bottom for the title block
    ax_tb = fig.add_axes([0.04, 0.0, 0.92, 0.06])
    ax_tb.set_xlim(0, 1)
    ax_tb.set_ylim(0, 1)
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 6 OF 7",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="Muslin clamp detail — cam-lever spring clamp",
                scale_note="MULTIPLE SCALES — SEE INDIVIDUAL PANELS",
                doc_id="TBS-FM01 · Film Plane Mechanism",
                height=0.75)

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet6.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet6.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 7 — SYSTEM SCHEMATIC: Four-corner frame front elevation
#
# View: looking at the film plane from the pinhole side (interior elevation).
# Shows ceiling/floor depth-rail pairs (3×1.5 304 U-channel), four corner acetal-skate
# carriages with cam clamps, film plane frame with a single U-joint at each corner.
# The long depth rail runs into the page (optical axis); shown end-on here.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet7():
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis("off")

    # Schematic coordinates (mm) — front elevation
    # X = container width (0=left wall, L=5893=right wall)
    # Z = height (0=floor, H=2388=ceiling)
    FW = L       # frame width extent for drawing
    FH = H       # frame height extent

    PAD_X = 1100
    PAD_Z = 550
    ax.set_xlim(-PAD_X, FW + PAD_X)
    ax.set_ylim(-PAD_Z, FH + PAD_Z)
    ax.set_aspect("equal")

    # ── Container outline (section cut) ───────────────────────────────────────
    wall_t = 40
    # Floor
    ax.add_patch(Rectangle((-wall_t, -wall_t), FW + 2 * wall_t, wall_t,
                            fc=STRUCT, ec=WHITE, lw=1.5, zorder=3))
    ax.text(FW / 2, -wall_t / 2, "CONTAINER FLOOR",
            color=BG, fontsize=6, ha="center", va="center", **FONT, zorder=4)
    # Ceiling
    ax.add_patch(Rectangle((-wall_t, FH), FW + 2 * wall_t, wall_t,
                            fc=STRUCT, ec=WHITE, lw=1.5, zorder=3))
    ax.text(FW / 2, FH + wall_t / 2, "CONTAINER CEILING",
            color=BG, fontsize=5, ha="center", va="center", **FONT, zorder=4)
    # Left wall
    ax.add_patch(Rectangle((-wall_t, -wall_t), wall_t, FH + 2 * wall_t,
                            fc=STRUCT, ec=WHITE, lw=1.5, zorder=3))
    # Right wall
    ax.add_patch(Rectangle((FW, -wall_t), wall_t, FH + 2 * wall_t,
                            fc=STRUCT, ec=WHITE, lw=1.5, zorder=3))

    # Interior fill
    ax.add_patch(Rectangle((0, 0), FW, FH, fc=GRID, ec="none", zorder=2))

    # ── Rail positions (X coords in this elevation = RAIL_X_L, RAIL_X_R) ─────
    rail_len = 200    # schematic rail length along optical axis (shown as width here)
    rail_h = 28       # rail profile height

    # Ceiling rails
    for rx, label in [(RAIL_X_L, "LEFT"), (RAIL_X_R, "RIGHT")]:
        ax.add_patch(Rectangle((rx - rail_len / 2, FH - rail_h), rail_len, rail_h,
                                fc=RAIL, ec=WHITE, lw=1.2, zorder=5))
        ldr_x = rx - 350 if label == "LEFT" else rx + 350
        ldr_ha = "right" if label == "LEFT" else "left"
        leader(ax, rx, FH - rail_h / 2, ldr_x, FH + 120,
               f"CEIL RAIL — {label}", color=RAIL, ha=ldr_ha, fs=6, font=FONT)

    # Floor rails
    for rx, label in [(RAIL_X_L, "LEFT"), (RAIL_X_R, "RIGHT")]:
        ax.add_patch(Rectangle((rx - rail_len / 2, 0), rail_len, rail_h,
                                fc=RAIL, ec=WHITE, lw=1.2, zorder=5))
        ldr_x = rx - 350 if label == "LEFT" else rx + 350
        ldr_ha = "right" if label == "LEFT" else "left"
        leader(ax, rx, rail_h / 2, ldr_x, -120,
               f"FLOOR RAIL — {label}", color=RAIL, ha=ldr_ha, fs=6, font=FONT)

    # ── Corner slide-and-clamp carriages + cam clamps ─────────────────────────
    # Each corner = a 4-wheel acetal skate (the long depth rail runs into
    # the page, so it reads end-on as a block) locked by a hand cam clamp. No
    # leadscrews, no handwheels — push to position, flip the clamp to lock.
    carr_w = 70
    carr_h = 50
    x_mid = (RAIL_X_L + RAIL_X_R) / 2

    corners = [
        ("TL", RAIL_X_L, FH, "top",    "A"),
        ("TR", RAIL_X_R, FH, "top",    "B"),
        ("BL", RAIL_X_L, 0,  "bottom", "C"),
        ("BR", RAIL_X_R, 0,  "bottom", "D"),
    ]

    for label, cx, rail_z, pos, cl_id in corners:
        cy = (rail_z - rail_h - carr_h) if pos == "top" else rail_h
        # depth-slide carriage (seen end-on)
        ax.add_patch(Rectangle((cx - carr_w / 2, cy), carr_w, carr_h,
                                fc=MECH, ec=WHITE, lw=1.2, zorder=6))
        # hand cam clamp on the outboard face — pivot + lever handle pointing away
        # from the frame (left carriages → left, right carriages → right)
        side = -1 if cx < x_mid else 1
        cam_cx = cx + side * carr_w / 2
        cam_cy = cy + carr_h / 2
        ax.add_patch(Circle((cam_cx, cam_cy), 7, fc=C_T3, ec=WHITE, lw=0.9, zorder=8))
        ax.plot([cam_cx, cam_cx + side * 55], [cam_cy, cam_cy + 48],
                color=C_T3, lw=2.4, solid_capstyle="round", zorder=8)
        ax.text(cam_cx + side * 60, cam_cy + 55, f"CAM CLAMP {cl_id}",
                color=DIM, fontsize=5.5, ha="left" if side > 0 else "right",
                va="center", **FONT, zorder=8)
        # Corner label inside carriage block
        ax.text(cx, cy + carr_h / 2, label, color=BG, fontsize=7,
                ha="center", va="center", fontweight="bold", **FONT, zorder=7)

    # ── Film plane frame ──────────────────────────────────────────────────────
    fp_left = RAIL_X_L
    fp_right = RAIL_X_R
    fp_bot = rail_h + carr_h
    fp_top = FH - rail_h - carr_h
    frame_t = 12  # frame member thickness (visual)

    # Frame outline (thick rectangle)
    frame_style = dict(fc="none", ec=C_FLAT, lw=2.8, zorder=8, linestyle="-")
    ax.add_patch(Rectangle((fp_left, fp_bot), fp_right - fp_left, fp_top - fp_bot,
                            **frame_style))

    # Frame member fill (thin strips along edges)
    for rect_args in [
        (fp_left, fp_bot, fp_right - fp_left, frame_t),               # bottom
        (fp_left, fp_top - frame_t, fp_right - fp_left, frame_t),     # top
        (fp_left, fp_bot, frame_t, fp_top - fp_bot),                  # left
        (fp_right - frame_t, fp_bot, frame_t, fp_top - fp_bot),       # right
    ]:
        ax.add_patch(Rectangle(rect_args[:2], rect_args[2], rect_args[3],
                                fc=STRUCT2, ec="none", lw=0, zorder=7, alpha=0.5))

    # ── Rail end flanges + wall plates (front elevation) ─────────────────────
    # A saddle back-plate at each of the 4 rail-end corners (near + far walls project
    # to the same X-Z here). Replaces the retired demountable brace cage.
    draw_brace_portal(ax, STRUCT, lw=1.4, alpha=0.55, z=4)
    # Point to the bottom-left saddle and place the text INSIDE the frame's open
    # lower-left quadrant — the margins (left: INTERIOR HEIGHT dim, bottom: width
    # dims + title block) are all crowded.
    leader(ax, RAIL_X_L, BRACE_Z_BOT,
           RAIL_X_L + 620, BRACE_Z_BOT + 520,
           "RAIL END FLANGE + WALL PLATE — RIGHT rails flanged wall-to-wall;\nLEFT rails = transport drop-in (Sheet 4)",
           color=STRUCT, ha="left", fs=6, font=FONT)

    # ── Single U-joint at each corner of the frame ────────────────────────────
    # Ruland US12-6-6-SS: light-blue body, two crossed pins (tilt + swing, twist-locked).
    joint_r = 22
    joint_positions = [
        (fp_left, fp_top),    # TL
        (fp_right, fp_top),   # TR
        (fp_left, fp_bot),    # BL
        (fp_right, fp_bot),   # BR
    ]
    for bx, bz in joint_positions:
        ax.add_patch(Circle((bx, bz), joint_r, fc=STRUCT2, ec=WHITE,
                            lw=1.0, zorder=9))
        # crossed pins (the two joint axes)
        ax.plot([bx - joint_r*0.8, bx + joint_r*0.8], [bz, bz],
                color=C_T2, lw=1.6, zorder=10, solid_capstyle="round")
        ax.plot([bx, bx], [bz - joint_r*0.8, bz + joint_r*0.8],
                color=MECH, lw=1.6, zorder=10, solid_capstyle="round")
        ax.add_patch(Circle((bx, bz), joint_r * 0.3, fc=BG, ec=WHITE,
                            lw=0.8, zorder=11))

    # ── Central label ─────────────────────────────────────────────────────────
    fp_cx = (fp_left + fp_right) / 2
    fp_cz = (fp_bot + fp_top) / 2
    ax.text(fp_cx, fp_cz + 80, "FILM PLANE FRAME",
            color=C_FLAT, fontsize=10, ha="center", va="center",
            fontweight="bold", **FONT, zorder=11)
    ax.text(fp_cx, fp_cz,
            f"{FP_W}mm wide  ×  {FP_H}mm tall",
            color=C_FLAT, fontsize=7.5, ha="center", va="center", **FONT, zorder=11)
    ax.text(fp_cx, fp_cz - 80,
            "SINGLE U-JOINT + X-Z cross-slides each corner",
            color=MECH, fontsize=7, ha="center", va="center", **FONT, zorder=11)

    # ── Leaders ───────────────────────────────────────────────────────────────
    # U-joint leader (from TL joint) — sits highest
    tl_cy = FH - rail_h - carr_h
    leader(ax, fp_left + joint_r, fp_top - joint_r,
           fp_left + 470, fp_top - 150,
           "SINGLE U-JOINT — Ruland US12-6-6-SS\n(2 axes, twist-locked, 45°)",
           color=MECH, ha="left", fs=6.5, font=FONT)

    # Depth-rail leader (from the TL trolley, end-on) — placed well below the U-joint label
    leader(ax, RAIL_X_L, tl_cy,
           RAIL_X_L + 470, tl_cy - 470,
           "DEPTH RAIL — 3×1.5 304 U-channel\nwall-to-wall (runs into page)\nacetal skate + cam clamp",
           color=RAIL, ha="left", fs=6.5, font=FONT)

    # Carriage leader (from TR carriage)
    leader(ax, RAIL_X_R + carr_w / 2, FH - rail_h - carr_h / 2,
           RAIL_X_R + 450, FH - rail_h - carr_h / 2 - 300,
           "acetal SKATE\n(4-wheel, depth, per corner)",
           color=MECH, ha="left", fs=6.5, font=FONT)

    # Rail leader (from TR ceiling depth rail)
    leader(ax, RAIL_X_R + rail_len / 2, FH - rail_h / 2,
           RAIL_X_R + 450, FH - 150,
           "3×1.5 304 U-CHANNEL RAIL\n(into page)",
           color=RAIL, ha="left", fs=6.5, font=FONT)

    # Frame leader (from right side midpoint)
    leader(ax, fp_right, fp_cz,
           fp_right + 450, fp_cz - 150,
           "2\"×2\"×3/16\"\nALUMINUM ANGLE\n(welded frame)",
           color=C_FLAT, ha="left", fs=6.5, font=FONT)

    # ── Dimensions ────────────────────────────────────────────────────────────
    # Container width (outermost)
    draw_dim_h(ax, 0, FW, -180,
               f"INTERIOR WIDTH  {L}mm", offset=14, color=DIM, fs=6,
               above=True, font=FONT)

    # Rail span + end zones (inner row)
    draw_dim_h(ax, 0, RAIL_X_L, -300,
               f"{RAIL_X_L}mm", offset=14, color=DIM, fs=6,
               above=True, font=FONT)
    draw_dim_h(ax, RAIL_X_L, RAIL_X_R, -300,
               f"RAIL SPAN  {RAIL_X_R - RAIL_X_L}mm", offset=14, color=DIM, fs=6,
               above=True, font=FONT)
    draw_dim_h(ax, RAIL_X_R, FW, -300,
               f"{FW - RAIL_X_R}mm", offset=14, color=DIM, fs=6,
               above=True, font=FONT)

    # Container height (left side)
    draw_dim_v(ax, -250, 0, FH,
               f"INTERIOR HEIGHT {H}mm", offset=150, color=DIM, fs=6.5, font=FONT)

    # Frame height (right side)
    draw_dim_v(ax, FW + 250, fp_bot, fp_top,
               f"FRAME HEIGHT {fp_top - fp_bot}mm", offset=30, color=C_FLAT,
               fs=6.5, right=True, font=FONT)

    # ── Title text ────────────────────────────────────────────────────────────
    ax.text(FW / 2, FH + 380,
            "SHEET 7 — SYSTEM SCHEMATIC  (FRONT ELEVATION — LOOKING FROM PINHOLE SIDE)",
            color=WHITE, fontsize=9, ha="center", fontweight="bold", **FONT)
    ax.text(FW / 2, FH + 290,
            "4 CORNER ACETAL SKATES (4-wheel on 304 U-channel, COORDINATED PAIRS)  ·  CAM CLAMP + SINGLE U-JOINT + X-Z UHMW-PAD CROSS-SLIDES AT EACH CORNER",
            color=DIM, fontsize=7, ha="center", **FONT)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 7 OF 7",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="System schematic — four-corner frame front elevation",
                scale_note="Schematic — not to scale",
                doc_id="TBS-FM01 · Film Plane Mechanism",
                height=0.05)

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet7.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet7.png")


# ── Run all sheets ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating film plane mechanism drawings (rigid plane)...")
    sheet1()
    sheet2()
    sheet3()
    sheet4()
    sheet5()
    sheet6()
    sheet7()
    print("Done.")
