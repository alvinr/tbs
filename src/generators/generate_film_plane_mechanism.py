#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_film_plane_mechanism.py
Moveable film plane mechanism — engineering drawings (8 sheets)
OPTION A — RIGID PLANE: a fixed-size rigid rectangle whose ANGLE changes. The 4 corners ride
SLIDE-AND-CLAMP corners (acetal skates on 304 U-channel + UHMW-pad cross-slides) moved by hand in COORDINATED PAIRS —
single-axis tilt (top vs bottom) or swing (left vs right); limited combined; NO compound twist
(a rigid plane cannot warp). A pinhole has infinite depth of field, so this is scene control,
not focus: push each corner into position, then lock the cam clamp. Each corner connects through
a single Ruland USKC12-6-6-SS U-joint (2 axes, twist-locked) — no leadscrews, no handwheels.

Sheet 1 — Plan view (top-down): 4-corner rail layout, example configs
Sheet 2 — Elevations: side elevation (tilt) + plan cross-section (swing)
Sheet 3 — Corner carriage detail: acetal skate on U-channel + capture sections + cross-slide + U-joint
Sheet 4 — Rail mounting & transport drop-in: left split (stub + removable + bridge) · right flanged · stub clamp
Sheet 5 — Movement specification table & BOM
Sheet 6 — Muslin clamp detail: spring clip at the ALU frame edge
Sheet 7 — System schematic: four-corner frame front elevation
Sheet 8 — Frame-corner ↔ cross-slide attachment: how the frame hangs off the two slides through the U-joint
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc, Polygon

from tbs_constants import FP_X_L, FP_X_R, FP_Y, FP_Y_MIN, FP_W, FP_H, PH_X as PH_X_C, MAX_TILT_DEG, MAX_SWING_DEG, DIAGRAMS_DIR, FP_ANGLE_LEG, FP_ANGLE_T, CLAMP_SPACING, CLAMP_JAW_W, CLAMP_OPEN_GAP, CLAMP_SPRING_F, CLAMP_N_TOTAL, BRACE_Z_BOT, BRACE_Z_TOP, C_WID, WALL_T, IBC_WBKT_PLATE_W, IBC_WBKT_SEAT_PROJ, IBC_WBKT_SEAT_T, DRUM_CY, DRUM_R, DRUM_CX, DRUM_D
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
C_ACM   = "#E4E0D6"   # ACM backing board (warm grey)
C_MUSLIN = "#D4B896"  # muslin fabric (warm tan)
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

# ── LEFT-rail transport drop-in (Sheet 4). These MIRROR generate_film_plane_mechanism_model.py; promote
# both to tbs_constants at the FP_W/FP_H cascade so 2D + 3D single-source them (see TODO). ──
from tbs_constants import PIVOT_YD, PIVOT_POST_OD, RAIL_OFF, RAIL_OFF_BOT, WALKWAY_H
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
    title_block(ax, "SHEET 1 OF 9",
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
    title_block(ax_tb, "SHEET 2 OF 9",
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
#   B   — U-joint detail (Ruland USKC12-6-6-SS, enlarged)
#   A-A — captive-carriage section (U-profile polymer liner)
#   C   — swing slide face-on
# ═══════════════════════════════════════════════════════════════════════════════
def _rect(ax, x, y, w, h, fc, ec=OUT, lw=1.4, z=4, alpha=1.0):
    draw_rect(ax, x, y, w, h, fc=fc, color=ec, lw=lw, zorder=z)
    if alpha < 1.0:
        ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec="none", alpha=alpha, zorder=z - 1))


def view_a(ax):
    """Corner assembly elevation — BOTTOM (weight) corner. Yd (horizontal) × Z (vertical), mm.
    The WEIGHT rail is at the TOP; the 4-wheel skate rides it and the whole stack HANGS DOWN to the
    film corner ~110 mm below (the film hangs BELOW the bottom rail — BUILD_BOT, matches the 3D). The
    film/ACM rises back up. Section A-A is cut through the bottom carriage."""
    ax.set_xlim(-60, 470); ax.set_ylim(110, 560); ax.set_aspect("equal"); ax.axis("off")

    # depth RAIL at the TOP — 3×1.5 304 U-CHANNEL, web-vertical, runs in Yd (BEHIND the carriage plate)
    ax.add_patch(plt.Rectangle((-30, 232), 420, 76, fc=C_STEEL, ec=OUT, lw=1.0, zorder=3))
    ax.plot([-30, 390], [237, 237], color=OUT, lw=0.8, zorder=4)                     # bottom flange (running surface)
    ax.plot([-30, 390], [303, 303], color=OUT, lw=0.8, zorder=4)                     # top flange
    for bx in (-20, 380):                                                            # zigzag break symbols (rail continues in Yd)
        zz = [(bx-5,234),(bx+4,252),(bx-4,270),(bx+4,288),(bx-5,306)]
        ax.plot([p[0] for p in zz],[p[1] for p in zz], color=OUT, lw=0.7, zorder=4)
    # ── WIDE carriage plate (red) — the MOVING part, drawn FULLY and IN FRONT: it extends UP over the skate, so
    #    the 4 wheels sit BEHIND it and are shown ghosted (dotted). The Z-slide (green) runs up its centre. ──
    _rect(ax, 130, 134, 80, 171, C_CAR, z=5)                                         # carriage plate Z134-305 (covers the wheels)
    _rect(ax, 161, 156, 18, 76, C_TILT, z=6); _hatch316(ax, 161, 156, 18, 76)        # Z (tilt) slide — centred, IN FRONT
    _rect(ax, 161, 156, 2.5, 76, C_POLY, z=7); _rect(ax, 176.5, 156, 2.5, 76, C_POLY, z=7)
    ax.plot([170, 170], [232, 210], color=C_PIN, lw=1.4, zorder=8)                   # axle-retainer bolt down through the plate
    _rect(ax, 200, 200, 14, 16, C_CLAMP, z=7)                                        # cam clamp on the carriage
    # 4-wheel skate — GHOSTED (dotted), hidden behind the plate: 2 LOAD rollers + 2 KEEPER rollers + the axle
    for wx in (150, 190):
        ax.add_patch(plt.Circle((wx, 253), 16, fc="none", ec=OUT, lw=0.7, ls=(0, (3, 2)), zorder=10))  # load roller Ø32
        ax.add_patch(plt.Circle((wx, 291), 10, fc="none", ec=OUT, lw=0.6, ls=(0, (3, 2)), zorder=10))  # keeper Ø20
    ax.plot([150, 190], [253, 253], color=OUT, lw=0.6, dashes=(3, 2), zorder=10)     # axle (ghost) through both load rollers
    # section A-A cut through the bottom carriage
    ax.plot([170, 170], [232, 250], color=OUT, lw=0.6, zorder=11)
    ax.plot([170, 170], [120, 134], color=OUT, lw=0.6, zorder=11)
    ax.text(170, 254, "A", fontsize=6.5, ha="center", va="bottom", color=OUT, **FONT)
    ax.text(170, 116, "A", fontsize=6.5, ha="center", va="top", color=OUT, **FONT)
    # ── compact cluster: U-joint + X (swing) slide + L-bracket + frame angle (IN FRONT of the plate) ──
    _rect(ax, 158, 146, 24, 24, C_UJ, z=7)                                           # U-joint
    draw_circle(ax, 170, 158, 5, color=C_PIN, fill=True, fc=C_PIN, lw=1.0, zorder=8)
    _rect(ax, 164, 156, 12, 12, C_SWING, z=8)                                        # X (swing) slide — end-on
    _rect(ax, 160, 134, 26, 24, C_STEEL, z=6)                                        # L-bracket
    _rect(ax, 168, 158, 30, 6, C_FRAME, z=8)                                         # frame angle in-plane leg
    _rect(ax, 168, 158, 6, 26, C_FRAME, z=8)                                         # frame angle perp leg
    ax.add_patch(plt.Rectangle((178, 160), 6, 380, fc=C_PANEL, ec="none", alpha=0.16, zorder=1))  # ACM rises UP
    ax.plot([176,186,176,186,176],[455,461,467,473,479], color=OUT, lw=0.6, zorder=6)  # break on the ACM

    # ── dimensions ──
    draw_dim_v(ax, 108, 160, 270, "≈110mm\nfilm corner\nBELOW\nthe rail\n(BUILD_BOT)", offset=14, fs=5.4, color=DIM, font=FONT)
    ax.annotate("", xy=(224, 300), xytext=(224, 156), arrowprops=dict(arrowstyle="<->", color=C_TILT, lw=0.6))
    ax.text(228, 228, "Z-slide TILT travel ~250mm (way runs up behind the rail)", fontsize=5.2, color=C_TILT, ha="left", va="center", rotation=90, **FONT)

    # ── leaders ──
    leader(ax, 60, 270, 232, 300, "DEPTH RAIL (Y) — 3×1.5 304 U-channel, web-vertical, runs in Yd; the traverse (~2.4 m floor rail)", ha="left", fs=5.8, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 190, 253, 232, 262, "4-wheel acetal skate — Ø32 LOAD rollers on the bottom flange\n+ Ø20 KEEPER rollers under the top flange (captive)", ha="left", fs=5.8, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 210, 210, 232, 210, "wide carriage plate (red) + cam clamp — hangs from the skate axles", ha="left", fs=5.8, color=C_CAR, font=FONT, bbox=LBL_BG)
    leader(ax, 170, 200, 232, 186, "Z (TILT) slide — 316 flat bar + UHMW + gib (green, up the plate centre)", ha="left", fs=5.8, color=C_TILT, font=FONT, bbox=LBL_BG)
    leader(ax, 176, 162, 232, 160, "X (SWING) slide — 316 flat bar, INTO PAGE (end-on)", ha="left", fs=5.8, color=C_SWING, font=FONT, bbox=LBL_BG)
    leader(ax, 182, 158, 232, 138, "single U-joint (Ruland USKC12-6-6-SS) + 304 SS corner plate → frame angle", ha="left", fs=5.8, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 181, 300, 232, 118, "2x2 6061 Al frame angle + ACM/muslin — rises UP (the rigid plane)", ha="left", fs=5.8, color=OUT, font=FONT, bbox=LBL_BG)

    ax.text(-60, 558, "A — CORNER ASSEMBLY ELEVATION  (BOTTOM / weight corner; Yd × Z — film hangs below the rail, matches the 3D)",
            fontsize=7.6, fontweight="bold", color=OUT, ha="left", va="top", **FONT)


def view_b(ax):
    """U-joint detail (enlarged ~2:1). Ruland USKC12-6-6-SS; through-axis horizontal."""
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

    ax.text(0, 146, "B — U-JOINT DETAIL  (Ruland USKC12-6-6-SS, enlarged)",
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
    _rect(ax, 9, 5, 16, 32, C_ACET, z=7)                                            # Ø32 LOAD roller (rim, cut)
    _rect(ax, 6, 16, 44, 10, C_STEEL, z=8)                                          # Ø10 axle/shaft — runs THROUGH the wheel, cantilevered to the carriage
    draw_circle(ax, 17, 21, 3.2, color=OUT, fill=True, fc="#9AA0A8", lw=0.5, zorder=9)  # hub at the wheel centre (shaft goes through)
    # ── KEEPER roller, just under the top flange (anti-lift), on its own stub axle ──
    _rect(ax, 11, 55, 13, 15, C_ACET, z=7)                                          # keeper roller (rim, cut)
    _rect(ax, 8, 58, 42, 8, C_STEEL, z=8)                                           # keeper stub axle — THROUGH the wheel to the carriage
    draw_circle(ax, 17, 62, 2.6, color=OUT, fill=True, fc="#9AA0A8", lw=0.5, zorder=9)  # hub at the keeper centre
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
    draw_dim_v(ax, -14, 0, 76, "76mm\n(3\")", offset=9, fs=5.4, color=DIM, font=FONT)
    draw_dim_h(ax, 5, 43, -10, "38mm flange", offset=7, fs=5.4, color=DIM, above=False, font=FONT)
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
    web = closed TOP, flanges hang DOWN, so the channel OPENS DOWNWARD. The guide drum's axle therefore stays
    WITHIN the throat; the carriage is a YOKE that reaches UP through the opening (past the lips) — its arms
    bear the flanges (lateral X) + hook the lips (anti-drop) and grab the axle ends, so nothing pierces a
    flange. Top rail carries NO weight (a depth/lateral guide); short in Z = minimum ceiling cost."""
    ax.set_xlim(-26, 122); ax.set_ylim(-66, 50); ax.set_aspect("equal"); ax.axis("off")
    # inverted-U: web on top (closed), flanges hang down — opening faces DOWN
    _uchan_hatch(ax, 0, 33, 76, 5)          # web = closed top / splice face (76 wide)
    for fx in (0, 71):
        _uchan_hatch(ax, fx, 0, 5, 38)      # flanges hang down (38)
    # WIDE Ø32 acetal guide WHEEL in the throat (Z guide, up against the web) — face width = 10mm NARROWER than the
    # yoke span (arms at x10/x66 → 56 span → 46 face), leaving ~5mm running clearance to each yoke arm.
    _rect(ax, 15, 1, 46, 32, C_ACET, z=7)
    # AXLE — a HORIZONTAL shaft along the wheel's length (X); it runs out to the yoke arms and stays in the throat
    _rect(ax, 10, 12, 56, 10, C_STEEL, z=6)
    # ghost the axle where it is HIDDEN behind the wheel — shows the shaft passing THROUGH the wheel
    ax.add_patch(plt.Rectangle((15, 12), 46, 10, fc="none", ec=OUT, lw=0.6, ls=(0, (3, 2)), zorder=9))
    ax.plot([38, 38], [12, 22], color="#6A6A72", lw=0.5, zorder=8)
    # ~5mm running-clearance marks between the wide wheel and each yoke arm
    for gx0, gx1 in ((10, 15), (61, 66)):
        ax.annotate("", xy=(gx1, 6), xytext=(gx0, 6), arrowprops=dict(arrowstyle="<->", color=DIM, lw=0.5))
    # YOKE — a JOINED U-bracket up through the OPENING: two arms grab the axle ends + bear the flanges (lateral X)
    # + hook the lips (anti-drop), JOINED by a cross-piece below the opening (one part).
    for ax_x in (4, 66):
        _rect(ax, ax_x, -14, 6, 36, C_CAR, z=8)                                      # yoke arm (through opening, against a flange)
    _rect(ax, 4, -22, 68, 8, C_CAR, z=8)                                             # cross-piece JOINS the two arms
    _rect(ax, 58, -8, 14, 4, C_CAR, z=9)                                             # inboard lip-hook (anti-drop)
    # carriage + stack hang from the joined yoke
    _rect(ax, 40, -46, 12, 24, C_CAR, z=6)                                           # carriage plate (below the yoke)
    _rect(ax, 40, -60, 12, 14, C_TILT, z=5)                                          # cross-slide (green) hangs below
    ax.add_patch(plt.Rectangle((16, -64), 56, 5, fc=C_PANEL, ec="none", alpha=0.16, zorder=2))  # film top edge ghost (hangs)
    ax.annotate("", xy=(38, 33), xytext=(38, 25), arrowprops=dict(arrowstyle="->", color=OUT, lw=1.0))  # guide reaction UP
    draw_dim_v(ax, -14, 0, 38, "38mm\n(short:\nceiling)", offset=7, fs=5.2, color=DIM, font=FONT)
    leader(ax, 38, 30, 52, 44, "Ø32 guide WHEEL — 10mm narrower than the yoke (~5mm clearance each side)", ha="left", fs=5.0, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 18, 17, -24, 2, "AXLE — a horizontal shaft along the wheel;\nheld by the yoke arms (never crosses a flange)", ha="left", fs=5.0, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 4, -18, -24, -38, "YOKE — a JOINED U up through the OPENING;\narms bear the flanges + hook the lips (anti-drop)", ha="left", fs=5.0, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 46, -50, 74, -50, "carriage + cross-slide\nstack hang BELOW", ha="left", fs=5.0, color=DIM, font=FONT, bbox=LBL_BG)
    ax.text(-26, 50, "SECTION B-B — TOP (guide) carriage",
            fontsize=6.8, fontweight="bold", color=OUT, ha="left", va="top", **FONT)
    ax.text(-26, 43, "wide wheel + horizontal axle; a JOINED yoke reaches up through the opening — nothing pierces a flange",
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
        "~250mm) + HORIZONTAL (X, purple, ~260mm) cross-slides (316 flat bar + UHMW pad + gib) absorb the "
        "tilt/swing foreshortening.",
        "3. Roll the skate / push each cross-slide into position; the gib drag holds the vertical, "
        "then throw the cam clamp (rail brake) to lock for the shot and for transport.",
        "4. The U-joint (Ruland USKC12-6-6-SS, 303 SS, self-lube, grease-free, nitrile-booted) gives "
        "tilt + swing and locks twist so the flat plane stays square. The plane's WEIGHT is carried by "
        "the BOTTOM rail (web-vertical, load rollers gravity-seated on the bottom flange); the TOP rail "
        "is a GUIDE only (flat inverted-U, minimum ceiling cost).",
        "5. WHEEL CAPTURE: BOTTOM rail (opens inboard) — load rollers on the bottom flange, axle out the "
        "OPENING to the carriage; + a KEEPER under the top flange (anti-lift) + a LIP on the inboard flange "
        "edge (stops X walk-off). TOP rail (opens down) — a wide guide wheel (10mm narrower than the yoke); the "
        "carriage is a JOINED YOKE that reaches UP through the opening: arms bear the flanges (lateral X) + "
        "hook the lips (anti-drop) and grab the horizontal axle WITHIN the throat (nothing pierces a flange). "
        "(LEFT rails = a transport drop-in — see Sheet 4.)",
        "6. OVERTURNING COUPLE: the film-corner load is ~50mm INBOARD of the rail (via the stack) — a moment "
        "about the rollers. The load↓ / keeper↑ pair, spaced by the channel depth, reacts it — so the keepers "
        "carry this static couple too. Tightest link: the 316 cross-slide bar in weak-axis bending; keep the "
        "stack compact.",
    ], 2, 99, 3.6, fs=5.4, title_fs=6.6, color=DIM, width=52, wrap=88, font=FONT)

    ax_tb = fig.add_axes([0.03, 0.008, 0.94, 0.06])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, "SHEET 3 OF 9",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="Corner carriage detail — acetal skate on 3×1.5 304 U-channel + cross-slides + U-joint + stub clamp",
                scale_note="Proportional (mm)",
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
    ax_te = fig.add_axes([0.03, 0.52, 0.94, 0.40]); ax_te.set_facecolor(BG)
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
    ], 2, 99, 4.1, fs=6.2, title_fs=6.8, color=DIM, width=79, wrap=132, font=FONT)

    ax_tb = fig.add_axes([0.03, 0.008, 0.94, 0.052]); ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1)
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 4 OF 9", drawing_title="MOVEABLE FILM PLANE",
                subtitle="Rail mounting & transport drop-in — left split (stub + removable + web-back bridge) · right flanged wall-to-wall",
                scale_note="Proportional (mm)",
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
        "U-joint  1× Ruland USKC12-6-6-SS (303 SS, KEYWAY+CLAMP hubs, 45° max, self-lube bronze)   ·   boot  1× Ruland UBOOT12/19-NI-KIT (nitrile, fitted dry)",
        "Shaft support  2× McMaster 4040N12 (304 SS)   ·   stub  2× 3/8\" 304 SS KEYED (McMaster 89535K873 + keyway machined for the U-joint)",
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
    title_block(ax, "SHEET 5 OF 9",
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
#   A (top-left):  Cross-section of clamp on 2"×2" 6061 Al angle profile
#   B (top-right): Clamp in open vs closed positions (side view)
#   C (bottom):    Elevation: 3 clamps at 150mm spacing along frame edge
# ═══════════════════════════════════════════════════════════════════════════════
def sheet6():
    from tbs_constants import (
        FP_ANGLE_LEG, FP_ANGLE_T, CLAMP_SPACING, CLAMP_JAW_W,
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

    # Cross-section at the frame edge, ROTATED 90° CCW so the PINHOLE is at LEFT
    # (matching Sheet 9 View B). The geometry below is authored in a "logical" frame
    # (pinhole = +y up, outboard = -x) and every primitive is pushed through _R (a
    # 90° CCW rotation) on the way to the axes; leaders/titles are placed directly in
    # the rotated frame. Per Sheet 9: the ACM board is NESTED into the corner of the
    # 2×2 ALU angle — butted against the flat leg (behind the board) AND against the
    # upstand leg. The upstand stands PROUD toward the pinhole; the clip mounts on the
    # upstand INBOARD face and presses the muslin toward the board. Support chain
    # (rail->skate->slides->U-joint) is on Sheets 3 & 8.
    ACM_T = 4                                    # ACM board thickness (matches Sheet 9)
    XO    = 11                                    # upstand outboard face (logical x)
    XI    = XO + T                                # upstand inboard face (logical x = 15.8)
    BL    = 46                                    # board length shown (cut short)
    ax_a.set_xlim(-74, 46)
    ax_a.set_ylim(-24, 84)
    ax_a.set_aspect("equal")

    C_ACM = "#E4E0D6"

    def _R(x, y):                                # 90° CCW rotation
        return (-y, x)
    def _rr(x, y, w, h, **kw):                   # rotated rectangle
        nx, ny = -(y + h), x
        ax_a.add_patch(Rectangle((nx, ny), h, w, **kw))
    def _rc(cx, cy, r, **kw):                    # rotated circle
        ax_a.add_patch(Circle(_R(cx, cy), r, **kw))
    def _rl(xs, ys, **kw):                        # rotated polyline
        p = [_R(a, b) for a, b in zip(xs, ys)]
        ax_a.plot([q[0] for q in p], [q[1] for q in p], **kw)
    def _rf(xs, ys, **kw):                        # rotated filled polygon
        p = [_R(a, b) for a, b in zip(xs, ys)]
        ax_a.fill([q[0] for q in p], [q[1] for q in p], **kw)

    # ── 2×2 (50.8) × 3/16" (4.8) ALU angle — a SINGLE L-section (no internal seam) ─
    _Lpts = [_R(x, y) for (x, y) in
             [(XO, -T), (XO + LEG, -T), (XO + LEG, 0), (XI, 0), (XI, -T + LEG), (XO, -T + LEG)]]
    ax_a.add_patch(Polygon(_Lpts, closed=True, fc=C_FRAME, ec=ANNO, lw=1.5, zorder=3))
    ax_a.add_patch(Polygon(_Lpts, closed=True, fc="none", ec="#8898A8", lw=0.3, hatch="///", zorder=4))
    leader(ax_a, (2), (40), (16), (30),
           "2×2 ALU ANGLE (3/16\")\nflat leg behind the board;\nupstand proud toward the pinhole",
           color=C_FRAME, fs=5, ha="left", va="center", arrow_style="-|>", font=FONT)

    # ── ACM backing board — NESTED in the corner ─────────────────────────────────
    _rr(XI, 0, BL, ACM_T, fc=C_ACM, ec=ANNO, lw=1.4, zorder=3)
    _rr(XI, 0, BL, ACM_T, fc="none", ec="#9a9a9a", lw=0.3, hatch="///", zorder=4)
    leader(ax_a, (-2), (52), (16), (50),
           "ACM BACKING BOARD", color=DIM, fs=5, ha="left", va="center", arrow_style="-|>", font=FONT)
    leader(ax_a, (-2), (18), (16), (12),
           "ACM butts into the frame corner",
           color=DIM, fs=4.7, ha="left", va="center", arrow_style="-|>", font=FONT)

    # ── Muslin — over the board (pinhole face); a short tuck around the upstand ───
    mx = [XI + BL, XI + 0.2, XI + 0.2]
    my = [ACM_T + 0.7, ACM_T + 0.7, 9]
    _rl(mx, my, color=C_MUSLIN, lw=4, solid_capstyle="round", zorder=6, alpha=0.95)
    _rl(mx, my, color=ANNO, lw=0.8, zorder=6.5)
    leader(ax_a, _R(XI + 26, ACM_T + 0.7)[0], _R(XI + 26, ACM_T + 0.7)[1], (16), (64),
           "MUSLIN — on the pinhole face;\nclamped toward the board at the edge",
           color="#8a6d3b", fs=5, ha="left", va="center", arrow_style="-|>", font=FONT)

    # ── Spring clip — mounted on the INBOARD side of the upstand; presses the muslin
    #    toward the board. Bracket bolted through the upstand, nuts on the inside. ──
    _rr(XI, 10, 3.2, 42, fc=C_CLAMP, ec=ANNO, lw=1.2, zorder=7)                      # bracket
    def _thru_bolt(by):   # csk head flush on the upstand OUTBOARD face; shank THROUGH the leg + bracket; NUT on the inside edge
        _rf([XO, XO, XO + 2, XO + 2], [by - 1.7, by + 1.7, by + 0.7, by - 0.7], color=C_BOLT, zorder=11)   # csk head
        _rr(XO + 2, by - 0.7, 9.5, 1.4, fc=C_BOLT, ec=ANNO, lw=0.4, zorder=10)                              # shank through to inside
        _rr(XI + 3.2, by - 1.6, 2.2, 3.2, fc=C_BOLT, ec=ANNO, lw=0.5, zorder=11)                            # hex NUT on the inside edge
    _thru_bolt(18); _thru_bolt(32)
    _rl([17.5, 33], [49, 8.4], color=C_CLAMP, lw=2.6, solid_capstyle="round", zorder=7)   # lever
    _rr(27, 5.0, 11, 2.6, fc=C_NEOP, ec=ANNO, lw=0.8, zorder=8)                            # neoprene pad
    ax_a.annotate("", xy=_R(33, 4.9), xytext=_R(33, 14),
                  arrowprops=dict(arrowstyle="-|>", color="#208020", lw=1.4), zorder=12)   # press force (toward board)
    _rc(17.5, 49, 2.6, fc="none", ec=C_CLAMP, lw=1.1, zorder=9)                            # torsion coil
    _rc(17.5, 49, 1.3, fc="none", ec=C_CLAMP, lw=0.9, zorder=9)
    _rl([17.5, -14], [49, 55], color=C_CLAMP, lw=2.2, solid_capstyle="round", zorder=7)    # squeeze handle
    for i in range(5):
        _rl([-14 - 1 + i * 0.4, -12 - 1 + i * 0.4], [53 - i * 1.4, 57 - i * 1.4],
            color=C_CLAMP, lw=0.9, zorder=8)

    # ── OPEN position (ghost) — squeeze the handle; the pad lifts off the muslin ──
    import math as _ma
    _pv = (17.5, 49)                             # pivot (torsion-spring coil), logical
    def _rot(p, deg):
        a = _ma.radians(deg); dx, dy = p[0] - _pv[0], p[1] - _pv[1]
        return (_pv[0] + dx * _ma.cos(a) - dy * _ma.sin(a),
                _pv[1] + dx * _ma.sin(a) + dy * _ma.cos(a))
    _od = -20
    _pad_c = (33, 8.4)
    _pad_o = _rot(_pad_c, _od)
    _ht_o = _rot((-14, 55), _od)
    _rl([_pv[0], _pad_o[0]], [_pv[1], _pad_o[1]], color=C_CLAMP, lw=2.0, ls=(0, (4, 2)), alpha=0.5, zorder=6)
    _rl([_pv[0], _ht_o[0]], [_pv[1], _ht_o[1]], color=C_CLAMP, lw=2.0, ls=(0, (4, 2)), alpha=0.5, zorder=6)
    _r = _ma.hypot(_pad_c[0] - _pv[0], _pad_c[1] - _pv[1])
    _a_c = _ma.degrees(_ma.atan2(_pad_c[1] - _pv[1], _pad_c[0] - _pv[0]))
    ax_a.add_patch(Arc(_R(*_pv), 2 * _r, 2 * _r, angle=0, theta1=_a_c + _od + 90, theta2=_a_c + 90,
                        color=C_CLAMP, lw=0.9, ls=":", alpha=0.6, zorder=6))
    _po = _R(*_pad_o)
    leader(ax_a, _po[0], _po[1], (-50), (68),
           f"OPEN (ghost) — squeeze the\nhandle; the pad lifts off\n(~{CLAMP_OPEN_GAP}mm gap)",
           color=C_CLAMP, fs=5, ha="left", va="center", arrow_style="-|>", font=FONT)

    # Leaders (rotated frame)
    _b = _R(XI + 1.6, 40)
    leader(ax_a, _b[0], _b[1], (-73), (6),
           "CLIP BRACKET — through-bolted to the\nupstand; 2× csk screws, nuts on the inside",
           color=C_BOLT, fs=5, ha="left", va="center", arrow_style="-|>", font=FONT)
    _p = _R(32, 6.5)
    leader(ax_a, _p[0], _p[1], (-56), (54),
           "SPRING JAW — presses the\nmuslin toward the board",
           color=C_CLAMP, fs=5, ha="left", va="center", arrow_style="-|>", font=FONT)
    _c = _R(17.5, 51.6)
    leader(ax_a, _c[0], _c[1], (-73), (28),
           "TORSION SPRING — holds it closed;\nsqueeze the handle to lift",
           color=C_CLAMP, fs=5, ha="left", va="center", arrow_style="-|>", font=FONT)

    # → TO PINHOLE (pinhole is at left)
    ax_a.annotate("", xy=(-66, 42), xytext=(-54, 42),
                  arrowprops=dict(arrowstyle="-|>", color=DIM, lw=1.4))
    ax_a.text(-60, 44.5, "TO PINHOLE", ha="center", va="bottom", fontsize=6, color=DIM, **FONT)

    # Panel title
    ax_a.text((-23), (80),
              "PANEL A — MUSLIN CLIP: SPRING CLAMP AT THE FRAME EDGE",
              ha="center", va="top", fontsize=6.6, color=ANNO,
              fontweight="bold", **FONT, zorder=15)
    ax_a.text((-23), (75),
              "AXES IN mm · pinhole at LEFT — ACM nested in the corner; clip on the upstand inboard face",
              ha="center", va="top", fontsize=5.0, color=DIM, **FONT, zorder=15)

    # ── CLAMP NOTES (top-right) — Panel B (a separate open/closed diagram) was
    #    redundant and removed; open/closed is now shown INLINE on Panel A as a
    #    ghosted jaw + swing arc + annotation ────────────────────────────────────
    ax_b = fig.add_axes([0.55, 0.50, 0.42, 0.38])
    ax_b.set_facecolor(BG)
    ax_b.set_xlim(0, 100)
    ax_b.set_ylim(0, 100)
    ax_b.axis("off")

    # ── PANEL C: Plan view — spring clips along the frame edge (bottom-left) ───
    ax_c = fig.add_axes([0.04, 0.06, 0.46, 0.36])
    ax_c.set_facecolor(BG)
    ax_c.axis("off")

    # Plan (looking down the pinhole axis): X = along the frame edge; +Y = inboard
    # (ACM / image side), -Y = outboard (clip side).
    frame_len = CLAMP_SPACING * 2 + 40  # ~2 clip spacings
    ax_c.set_xlim(-34, frame_len + 48)
    ax_c.set_ylim(-40, 46)
    ax_c.set_aspect("equal")
    C_ACM = "#E4E0D6"

    # ACM board surface (pinhole face), inboard
    ax_c.add_patch(Rectangle((-22, 4), frame_len + 60, 30, fc=C_ACM, ec=ANNO, lw=1.0,
                              hatch="///", zorder=3))
    ax_c.text((frame_len / 2), (20), "ACM BOARD (pinhole face)", ha="center", va="center",
              fontsize=5, color=DIM, **FONT, zorder=15)
    # ALU frame outboard edge (the strip the clips grip), running along X
    ax_c.add_patch(Rectangle((-22, 0), frame_len + 60, 4, fc=C_FRAME, ec=ANNO, lw=1.0, zorder=4))
    ax_c.text((frame_len + 30), (2), "ALU FRAME EDGE", ha="left", va="center",
              fontsize=5, color=DIM, **FONT, zorder=15)
    # muslin wraps the edge (a line along the edge)
    ax_c.plot([-22, frame_len + 36], [0, 0], color=C_MUSLIN, lw=3, alpha=0.85, zorder=5)

    # 2 spring clips at 150mm — CLIP ON THE INSIDE of the frame: neoprene pad on the
    # board (inboard), bracket through-bolted in the upstand, handle projecting outboard
    for cx in [CLAMP_SPACING * 0.5, CLAMP_SPACING * 1.5]:
        # neoprene pad pressing the muslin onto the board (inboard side, +Y)
        ax_c.add_patch(Rectangle((cx - CLAMP_JAW_W / 2, 5), CLAMP_JAW_W, 7,
                                  fc=C_NEOP, ec=ANNO, lw=0.9, zorder=7))
        # bracket footprint on the upstand + 2 through-bolts (nuts on the inside)
        ax_c.add_patch(Rectangle((cx - CLAMP_JAW_W / 2, 0.5), CLAMP_JAW_W, 4.5,
                                  fc=C_CLAMP, ec=ANNO, lw=0.9, alpha=0.95, zorder=6))
        for boff in (-11, 11):
            ax_c.add_patch(Circle((cx + boff, 2.4), 1.6, fc=C_BOLT, ec=ANNO, lw=0.5, zorder=9))
        # squeeze handle projecting OUTBOARD (over the frame edge, -Y)
        ax_c.plot([cx, cx], [0.5, -16], color=C_CLAMP, lw=2.0, solid_capstyle="round", zorder=6)
        for i in range(4):   # knurled grip
            ax_c.plot([cx - 4, cx + 4], [-12 - i * 1.2, -12 - i * 1.2], color=C_CLAMP, lw=0.8, zorder=6)

    # Leaders (kept below the frame edge — clear of the board)
    leader(ax_c, (CLAMP_SPACING * 0.5 - 6), (8), (CLAMP_SPACING * 0.5 - 48), (-22),
           "NEOPRENE PAD — presses the\nmuslin onto the board (inboard)",
           color=C_CLAMP, fs=5, ha="center", va="center", arrow_style="-|>", font=FONT)
    leader(ax_c, (CLAMP_SPACING * 0.5 + 11), (2.4), (CLAMP_SPACING * 0.5 + 34), (-22),
           "2 csk through-bolts\n(nuts on the inside)",
           color=C_BOLT, fs=5, ha="left", va="center", arrow_style="-|>", font=FONT)
    leader(ax_c, (CLAMP_SPACING * 1.5), (-14), (CLAMP_SPACING * 1.5 + 26), (-16),
           "handle projects outboard\n(over the frame edge)",
           color=C_CLAMP, fs=5, ha="left", va="center", arrow_style="-|>", font=FONT)

    # Spacing dimension
    draw_dim_h(ax_c, (CLAMP_SPACING * 0.5), (CLAMP_SPACING * 1.5), (-34),
               f"{CLAMP_SPACING}mm SPACING", offset=(3), fs=6, font=FONT)
    # direction arrow
    ax_c.annotate("", xy=(-26, 22), xytext=(-26, 6),
                  arrowprops=dict(arrowstyle="-|>", color=DIM, lw=1.0))
    ax_c.text(-29, 14, "↑ TO\nPINHOLE", ha="right", va="center", fontsize=5, color=DIM, **FONT, zorder=15)

    ax_c.text((frame_len / 2), (44),
              "PANEL C — PLAN VIEW: SPRING CLIPS ALONG THE FRAME EDGE",
              ha="center", va="bottom", fontsize=7, color=ANNO,
              fontweight="bold", **FONT, zorder=15)
    ax_c.text((frame_len / 2), (40.5),
              "AXES IN mm · LOOKING DOWN THE PINHOLE AXIS AT THE FRAME EDGE",
              ha="center", va="bottom", fontsize=5.2, color=DIM, **FONT, zorder=15)

    # ── PANEL D removed — the elevation only re-stated Panel C's 150mm spacing.
    #    Bottom-right is free for a repurposed detail if wanted (see report TODO).

    # Notes — CLAMP NOTES panel (top-right; ax_b, 0–100 data coords)
    notes = [
        "CLAMP NOTES:",
        f"1. {CLAMP_N_TOTAL} spring clips at {CLAMP_SPACING}mm centers around the frame perimeter.",
        "2. ALU angle frames the ACM board; the clip mounts on the upstand's inboard face.",
        "3. Muslin lies over the board (pinhole face); the clip presses it onto the board at the edge.",
        "4. Bracket through-bolts to the upstand (2 countersunk screws, nuts on the inside); the spring jaw presses the muslin onto the board.",
        f"5. Torsion spring holds the jaw closed (~{CLAMP_SPRING_F}N); squeeze the handle to lift it (~{CLAMP_OPEN_GAP}mm gap).",
        "6. Neoprene jaw pad grips the muslin without tearing; snap open/closed by feel in safelight.",
    ]
    notes_x = 2
    notes_y_start = 96
    draw_notes(ax_b, notes, notes_x, notes_y_start, spacing=(9),
               fs=7, title_fs=7.5, color=DIM, title_color=ANNO, font=FONT,
               width=(88))

    # ── Title block ───────────────────────────────────────────────────────────
    # Create a full-width axes at the bottom for the title block
    ax_tb = fig.add_axes([0.04, 0.0, 0.92, 0.06])
    ax_tb.set_xlim(0, 1)
    ax_tb.set_ylim(0, 1)
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 6 OF 9",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="Muslin clamp detail — spring-clip at the ALU frame edge",
                scale_note="MULTIPLE SCALES — SEE INDIVIDUAL PANELS",
                doc_id="TBS-FM01 · Film Plane Mechanism",
                height=0.75)

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet6.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet6.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 7 — SYSTEM ELEVATION (to scale): Four-corner frame front elevation
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

    # True-scale coordinates (mm) — front elevation, aspect equal (container, rails,
    # frame all at real mm; corner mechanisms drawn to size — small at this scale)
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
    # 3×1.5" 304 U-channel seen END-ON (it runs into the page along the optical axis):
    # its cross-section is 76mm (3") wide × 38mm (1.5") tall — drawn to scale.
    rail_len = 76     # rail cross-section width (3")
    rail_h = 38       # rail cross-section height (1.5")

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
    carr_w = 110      # acetal-skate carriage plate width (to scale)
    carr_h = 60       # skate carriage height (to scale — fits the true rail↔frame gap)
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
    fp_bot = RAIL_OFF_BOT          # true frame bottom Z (floor offset, 160mm)
    fp_top = FH - RAIL_OFF         # true frame top Z (ceiling offset, 2288mm)
    frame_t = FP_ANGLE_LEG         # 2×2 angle leg = 50.8mm (to scale)

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
    # Ruland USKC12-6-6-SS: light-blue body, two crossed pins (tilt + swing, twist-locked).
    joint_r = 9.5     # Ø19 U-joint (to scale — small at this system scale; detail on Sheets 8-9)
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
           "SINGLE U-JOINT — Ruland USKC12-6-6-SS\n(2 axes, twist-locked, 45°)",
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
           "2\"×2\"×3/16\"\n6061 Al ANGLE\n(welded frame)",
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
               f"FRAME HEIGHT {FP_H}mm", offset=30, color=C_FLAT,
               fs=6.5, right=True, font=FONT)

    # ── Title text ────────────────────────────────────────────────────────────
    ax.text(FW / 2, FH + 380,
            "SHEET 7 — SYSTEM ELEVATION, TO SCALE  (FRONT — LOOKING FROM PINHOLE SIDE)",
            color=WHITE, fontsize=9, ha="center", fontweight="bold", **FONT)
    ax.text(FW / 2, FH + 290,
            "4 CORNER ACETAL SKATES (4-wheel on 304 U-channel, COORDINATED PAIRS)  ·  CAM CLAMP + SINGLE U-JOINT + X-Z UHMW-PAD CROSS-SLIDES AT EACH CORNER",
            color=DIM, fontsize=7, ha="center", **FONT)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 7 OF 9",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="System elevation — four-corner frame front elevation (proportional)",
                scale_note="Proportional (mm)",
                doc_id="TBS-FM01 · Film Plane Mechanism",
                height=0.05)

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet7.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet7.png")


def _joint(ax, x, y, r=3.4):
    """A joint marker seen END-ON (a vertical bolt viewed down its axis, e.g. in the plan view) — gold dot."""
    draw_circle(ax, x, y, r, color=OUT, fill=True, fc=C_PIN, lw=0.8, zorder=12)


def _hatch316(ax, x, y, w, h, z=6):
    hatch_rect(ax, x, y, w, h, color="#6E747C", hatch="\\\\\\", lw=0.0)


def attach_plan(ax):
    """PLAN VIEW (Yd × X), looking DOWN the Z axis — the SWING stack. Here the X (swing) slide shows its
    real travel along X, and the U-joint's SWING pin is seen true. The Z (tilt) slide is edge-on (into page)."""
    ax.set_xlim(-20, 470); ax.set_ylim(-70, 90); ax.set_aspect("equal"); ax.axis("off")
    cyy = 0
    # carriage plate + Z slide edge-on (into the page here)
    _rect(ax, 40, cyy - 20, 40, 40, C_CAR, z=4)
    _rect(ax, 52, cyy - 12, 18, 24, C_TILT, z=5); _hatch316(ax, 52, cyy - 12, 18, 24)
    ax.text(60, cyy - 26, "Z slide\n(edge-on)", fontsize=5.0, color=C_TILT, ha="center", va="top", **FONT)
    # X (SWING) way — a long 316 flat bar along X + carriage that traverses it
    _rect(ax, 90, cyy - 8, 300, 16, C_SWING, z=5); _hatch316(ax, 90, cyy - 8, 300, 16)
    _rect(ax, 300, cyy - 12, 46, 24, C_SWING, z=6)                # X carriage (near one end = swung)
    ax.annotate("", xy=(96, cyy + 26), xytext=(384, cyy + 26), arrowprops=dict(arrowstyle="<->", color=C_SWING, lw=1.0))
    ax.text(240, cyy + 30, "X travel ~260mm = SWING accommodation", fontsize=6, color=C_SWING, ha="center", va="bottom", **FONT)
    # stub → U-joint (swing pin seen true here) → frame
    _rect(ax, 346, cyy - 6, 16, 12, C_STEEL, z=6)
    _rect(ax, 362, cyy - 18, 34, 36, C_UJ, z=6)
    ax.plot([379, 379], [cyy - 22, cyy + 22], color=C_PIN, lw=2.4, zorder=8)       # SWING pin (true)
    draw_circle(ax, 379, cyy + 14, 3.5, color=C_PIN, fill=True, fc=C_PIN, lw=0.7, zorder=9)
    draw_circle(ax, 379, cyy - 14, 3.5, color=C_PIN, fill=True, fc=C_PIN, lw=0.7, zorder=9)
    _rect(ax, 396, cyy - 6, 14, 12, C_STEEL, z=6)                 # output stub
    _rect(ax, 410, cyy - 22, 22, 44, C_STEEL, z=6)                # frame corner bracket
    _rect(ax, 432, cyy - 26, 8, 52, C_FRAME, z=7)                 # frame angle (runs along X)
    ax.add_patch(plt.Rectangle((440, cyy - 26), 6, 52, fc=C_PANEL, ec="none", alpha=0.16, zorder=2))
    _joint(ax, 354, cyy); _joint(ax, 403, cyy); _joint(ax, 421, cyy - 16)
    leader(ax, 320, cyy - 12, 250, -50, "X carriage — 316 on UHMW; cam-clamp locks swing", ha="left", fs=5.6, color=C_SWING, font=FONT, bbox=LBL_BG)
    leader(ax, 379, cyy + 18, 300, 58, "U-joint SWING pin (true here)", ha="left", fs=5.6, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 421, cyy - 16, 405, -52, "frame angle + ACM\n(runs along X)", ha="left", fs=5.6, color=OUT, font=FONT, bbox=LBL_BG)
    ax.text(-20, 88, "B — PLAN  (Yd × X; looking down Z) — the SWING slide + U-joint swing pin", fontsize=8, fontweight="bold", color=OUT, ha="left", va="top", **FONT)


def attach_tilt(ax):
    """SECTION (Yd × Z), looking along +X — the TILT stack (companion to plan B, which does the SWING / X slide).
    Here the Z (tilt) slide shows its real VERTICAL travel and the U-joint's TILT pin is seen true; the X (swing)
    slide is edge-on (into the page)."""
    ax.set_xlim(-96, 118); ax.set_ylim(-44, 332); ax.set_aspect("equal"); ax.axis("off")
    cx = 30
    # carriage plate (top, hangs from the skate) + X (swing) slide edge-on (into page)
    _rect(ax, cx - 24, 296, 48, 24, C_CAR, z=4)
    _rect(ax, cx - 10, 300, 20, 16, C_SWING, z=5); _hatch316(ax, cx - 10, 300, 20, 16)
    ax.text(cx, 324, "carriage plate + X slide (edge-on)", fontsize=5.2, color=DIM, ha="center", va="bottom", **FONT)
    # Z (TILT) way — a long 316 flat bar running in Z (vertical) + carriage traversing it (lower = nominal)
    _rect(ax, cx - 8, 44, 16, 256, C_TILT, z=5); _hatch316(ax, cx - 8, 44, 16, 256)
    _rect(ax, cx - 15, 44, 30, 50, C_TILT, z=6)
    _rect(ax, cx - 11, 48, 4, 42, C_POLY, z=7); _rect(ax, cx + 7, 48, 4, 42, C_POLY, z=7)   # UHMW pads
    _rect(ax, cx - 15, 66, 8, 10, C_PIN, z=7)                                               # gib
    ax.annotate("", xy=(cx + 34, 300), xytext=(cx + 34, 44), arrowprops=dict(arrowstyle="<->", color=C_TILT, lw=1.0))
    ax.text(cx + 38, 172, "Z travel ~250mm = TILT accommodation", fontsize=6, color=C_TILT, ha="left", va="center", rotation=90, **FONT)
    # stub → U-joint (TILT pin seen true) → 304 SS corner plate → frame angle (below)
    _rect(ax, cx - 6, 30, 12, 16, C_STEEL, z=6)                                             # stub
    _rect(ax, cx - 18, -4, 36, 34, C_UJ, z=6)                                               # U-joint
    ax.plot([cx - 24, cx + 24], [13, 13], color=C_PIN, lw=2.4, zorder=8)                    # TILT pin (horizontal, true)
    draw_circle(ax, cx - 16, 13, 3.5, color=C_PIN, fill=True, fc=C_PIN, lw=0.7, zorder=9)
    draw_circle(ax, cx + 16, 13, 3.5, color=C_PIN, fill=True, fc=C_PIN, lw=0.7, zorder=9)
    _rect(ax, cx - 12, -26, 24, 22, C_STEEL, z=6)                                           # L-bracket
    _rect(ax, cx - 12, -32, 34, 6, C_FRAME, z=7)                                            # frame angle
    ax.add_patch(plt.Rectangle((cx - 12, -40), 34, 8, fc=C_PANEL, ec="none", alpha=0.16, zorder=2))
    _joint(ax, cx, 37); _joint(ax, cx, -8)
    leader(ax, cx - 15, 68, -94, 128, "Z carriage — 316 on UHMW + gib; cam-clamp locks tilt", ha="left", fs=5.6, color=C_TILT, font=FONT, bbox=LBL_BG)
    leader(ax, cx - 24, 13, -94, 44, "U-joint TILT pin (true here)", ha="left", fs=5.6, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, cx + 20, -30, 44, -38, "frame angle + ACM", ha="left", fs=5.6, color=OUT, font=FONT, bbox=LBL_BG)
    ax.text(-96, 330, "A — SECTION  (Yd × Z; looking along X) — the TILT slide + U-joint tilt pin", fontsize=7.6, fontweight="bold", color=OUT, ha="left", va="top", **FONT)


def _corner_elevation(ax):
    """VIEW A — the corner SQUARE-ON from the X-SLIDE / RAIL side (X × Z), TO SCALE (mm): the assembly turned
    180° about the vertical axis so we view it FROM BEHIND the film plane. Depth order BACK→FRONT is now
    reversed vs the pinhole view: ACM → 6061 angle L → 304 SS corner plate → U-joint (Ø19) → X-slide. The
    mechanism (plate, U-joint, X-slide) is FRONTMOST and solid; the ACM + frame are hidden → dashed/faint."""
    AL = 50.8                                                        # 2" angle leg
    ax.set_xlim(-70, 250); ax.set_ylim(-48, 258); ax.set_aspect("equal"); ax.axis("off")
    ax.invert_xaxis()                                               # 180° about the vertical axis — view from the other side
    # BACK → FRONT (from behind: ACM farthest, X-slide nearest)
    ax.add_patch(plt.Rectangle((AL - 6, AL - 6), 214, 190, fc=C_ACM, ec=OUT, lw=0.8, ls=(0, (4, 2)),
                               alpha=0.22, zorder=3))                                    # ACM — backmost now (hidden)
    ax.add_patch(plt.Rectangle((0, 0), 232, AL, fc=C_FRAME, ec=OUT, lw=1.0, ls=(0, (4, 2)),
                               alpha=0.30, zorder=4))                                    # 6061 angle L — bottom leg (behind the plate)
    ax.add_patch(plt.Rectangle((0, 0), AL, 214, fc=C_FRAME, ec=OUT, lw=1.0, ls=(0, (4, 2)),
                               alpha=0.30, zorder=4))                                    # 6061 angle L — left leg
    ax.add_patch(plt.Rectangle((-2, -2), 152, 152, fc=C_STEEL, ec=OUT, lw=1.2, zorder=5))  # 304 SS corner plate — NOW the visible face
    _hatch316(ax, -2, -2, 152, 152)
    ax.add_patch(plt.Rectangle((-58, 21), 168, 38, fc=C_SWING, ec=OUT, lw=1.0, zorder=6))   # X (swing) slide — frontmost now, solid
    ax.add_patch(plt.Circle((40, 40), 9.5, fc=C_UJ, ec=OUT, lw=1.1, zorder=7))              # U-joint Ø19 end-on — yoke toward us
    draw_circle(ax, 40, 40, 2.6, color=OUT, fill=False, lw=0.9, zorder=8)                   # swing pin (end-on)
    # M6 bolt HEADS on the plate back face, angle → 304 SS corner plate (J5, 2 per leg) — end-on, now toward us
    for (bx, bz) in [(96, 25.4), (134, 25.4), (25.4, 96), (25.4, 134)]:
        draw_circle(ax, bx, bz, 3.0, color=OUT, fill=True, fc=C_PIN, lw=0.9, zorder=9)
    draw_dim_v(ax, 162, 0, AL, "2\" (50.8)", fs=5.4, font=FONT)                          # angle leg size (on the now-right leg)
    # labels
    leader(ax, 75, 120, 175, 150, "304 SS corner plate 6×8 — U-joint mount\n(this face toward us now)", ha="left", fs=5.4, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 40, 40, -40, 92, "U-joint Ø19 end-on (yoke toward us)\nRuland USKC12-6-6-SS", ha="left", fs=5.4, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 90, 40, 150, 15, "X (swing) slide — frontmost this view", ha="left", fs=5.2, color=C_SWING, font=FONT, bbox=LBL_BG)
    leader(ax, 25.4, 134, -30, 175, "M6 ×2 per leg (angle → plate, J5)\nheads on the plate back", ha="left", fs=5.2, color=C_PIN, font=FONT, bbox=LBL_BG)
    leader(ax, 200, 25.4, 210, -34, "2x2 6061 Al angle L (FRAME)\n— behind the plate now (ACM behind it)", ha="left", fs=5.4, color=C_FRAME, font=FONT, bbox=LBL_BG)
    ax.text(-70, 256, "A — FROM THE X-SLIDE / RAIL SIDE  (X × Z)",
            fontsize=7.0, fontweight="bold", color=OUT, ha="left", va="top", **FONT)
    ax.text(-70, 247, "180° flip of the pinhole view — mechanism forward,\nACM + frame hidden behind (to scale)",
            fontsize=5.6, color=DIM, ha="left", va="top", **FONT)


def _corner_section(ax):
    """VIEW B — CROSS-SECTION, TO SCALE (mm). Yd × X, looking down Z. The X (swing) slide runs vertical
    (along X, broken); the corner stacks 90° toward the PINHOLE (right): X-carriage → U-joint (Ø19 × 68) →
    304 SS corner plate (¼") → 6061 angle L (2") with the ACM (4mm) + muslin nested inside → muslin."""
    AL, AW = 50.8, 4.8
    ax.set_xlim(-52, 252); ax.set_ylim(-96, 108); ax.set_aspect("equal"); ax.axis("off")
    ax.invert_xaxis(); ax.invert_yaxis()   # turn the whole section 180° (pinhole to the left, per Alvin)
    # X (swing) slide — 316 flat bar ¼(6) way + carriage, along X (vertical), BROKEN
    ax.add_patch(plt.Rectangle((18, -70), 6, 140, fc=C_SWING, ec=OUT, lw=1.0, zorder=5)); _hatch316(ax, 18, -70, 6, 140)
    for yb in (70, -70):
        s = 1 if yb > 0 else -1
        ax.plot([13, 18, 24, 29], [yb, yb + 4 * s, yb - 4 * s, yb], color=OUT, lw=0.8, zorder=6)
    ax.add_patch(plt.Rectangle((6, -24), 40, 48, fc=C_SWING, ec=OUT, lw=1.0, zorder=6))    # X carriage
    ax.annotate("", xy=(-38, 60), xytext=(-38, -60), arrowprops=dict(arrowstyle="<->", color=C_SWING, lw=1.0))
    ax.text(-44, 0, "X travel ~260 (broken)", fontsize=5.4, color=C_SWING, ha="center", va="center", rotation=90, **FONT)
    # input stub 3/8"(9.5) → U-joint → output stub
    ax.add_patch(plt.Rectangle((46, -4.75), 26, 9.5, fc=C_STEEL, ec=OUT, lw=1.0, zorder=6))
    ax.add_patch(plt.Rectangle((72, -9.5), 68, 19, fc=C_UJ, ec=OUT, lw=1.0, zorder=6))     # U-joint Ø19 × 68
    ax.plot([106, 106], [-13, 13], color=C_PIN, lw=2.0, zorder=8)                          # tilt pin (along X, true)
    draw_circle(ax, 106, 0, 2.6, color=OUT, fill=False, lw=0.9, zorder=9)                  # swing pin (end-on)
    ax.add_patch(plt.Rectangle((140, -4.75), 26, 9.5, fc=C_STEEL, ec=OUT, lw=1.0, zorder=6))
    # 304 SS corner plate — ¼"(6) thick, 6×8 (part shown)
    ax.add_patch(plt.Rectangle((166, -70), 6, 140, fc=C_STEEL, ec=OUT, lw=1.0, zorder=6)); _hatch316(ax, 166, -70, 6, 140)
    # 6061 angle L (2", 3/16" wall): in-plane leg + perp leg; ACM (4mm) + muslin NEST inside
    ax.add_patch(plt.Rectangle((172, -56), AW, 112, fc=C_FRAME, ec=OUT, lw=1.2, zorder=7))        # in-plane leg
    ax.add_patch(plt.Rectangle((172, -56), AW + AL, AW, fc=C_FRAME, ec=OUT, lw=1.2, zorder=7))    # perp leg → pinhole
    ax.add_patch(plt.Rectangle((172 + AW, -56 + AW), 4, 108, fc=C_ACM, ec=OUT, lw=0.9, zorder=7)) # ACM 4mm, in the L
    ax.plot([180.8, 180.8, 172 + AW + AL, 172 + AW + AL], [56, -51.2, -51.2, -60],
            color=C_MUSLIN, lw=2.6, alpha=0.95, zorder=12)                                        # muslin — front, wraps the perp leg
    # retaining bolts — COUNTERSUNK (M6). J5: angle → 304 SS plate; and angle → ACM (flush).
    for by in (-24, 24):                                            # J5 frame → SS corner plate — secured FROM THE PLATE side
        ax.fill([166, 166, 168.5, 168.5], [by - 3, by + 3, by + 1.1, by - 1.1], color=C_PIN, zorder=12)  # countersunk head in the plate back (U-joint side)
        ax.add_patch(plt.Rectangle((168.5, by - 0.9), 8.3, 1.8, fc=C_PIN, ec=OUT, lw=0.3, zorder=11))     # shank forward through the plate, threads into the frame leg
    for by in (-10, 10):                                           # ACM secured FROM the frame INTO the ACM — head
        ax.fill([172, 172, 175, 175], [by - 3, by + 3, by + 1.1, by - 1.1], color=C_PIN, zorder=11)  # countersunk in the frame BACK
        ax.add_patch(plt.Rectangle((175, by - 0.9), 6, 1.8, fc=C_PIN, ec=OUT, lw=0.3, zorder=9))       # shank forward into the ACM (front clean)
    # countersunk cap screw, 304 SS corner plate → output stub — secures the shaft that carries the U-joint (axial, on CL)
    ax.fill([172, 172, 168.5, 168.5], [-3.4, 3.4, 1.2, -1.2], color=C_PIN, zorder=12)               # countersunk head in the plate (frame-side face)
    ax.add_patch(plt.Rectangle((148, -1.2), 20.5, 2.4, fc=C_PIN, ec=OUT, lw=0.3, zorder=12))         # shank axial into the output stub
    # USKC clamp hubs — a clamp screw locks each hub onto its KEYED shaft (shown on the U-joint, radial)
    for hx in (84, 128):                          # input hub (→ X-carriage stub) · output hub (→ corner-plate stub)
        ax.add_patch(plt.Rectangle((hx - 0.9, 2.5), 1.8, 7.0, fc=C_PIN, ec=OUT, lw=0.3, zorder=13))   # clamp-screw shank into the hub
        ax.add_patch(plt.Rectangle((hx - 2.2, 9.5), 4.4, 2.4, fc=C_PIN, ec=OUT, lw=0.4, zorder=13))    # cap-screw head at the hub OD
    # 4040N12 304 shaft support — a two-piece clamp on the input stub, bolted to the X-carriage,
    # so the stub (and the whole corner load through it) is positively secured to the purple X-slide
    for (yb, yh) in [(4.75, 7.0), (-11.75, 7.0)]:                 # upper & lower halves — bore = the Ø9.5 stub between them
        ax.add_patch(plt.Rectangle((47, yb), 13, yh, fc=C_STEEL, ec=OUT, lw=1.0, zorder=8)); _hatch316(ax, 47, yb, 13, yh)
    ax.add_patch(plt.Rectangle((52.4, 11.75), 2.2, 4.5, fc=C_PIN, ec=OUT, lw=0.3, zorder=13))          # clamp screw — pulls the halves onto the stub
    for by in (-8.5, 8.5):                                        # 2 bolts fix the support to the carriage (purple slide)
        ax.add_patch(plt.Rectangle((40, by - 0.9), 9.6, 1.8, fc=C_PIN, ec=OUT, lw=0.3, zorder=13))
    # dimensions
    draw_dim_h(ax, 72, 140, 30, "68", fs=5.2, font=FONT)                                   # U-joint length
    draw_dim_v(ax, 150, -9.5, 9.5, "Ø19", fs=5.2, font=FONT)                               # U-joint dia
    draw_dim_h(ax, 176, 172 + AW + AL, -70, '2" (50.8)', fs=5.2, font=FONT)                # perp leg
    # → TO PINHOLE — horizontal, 90° to the vertical X slide
    ax.annotate("", xy=(244, 0), xytext=(220, 0), arrowprops=dict(arrowstyle="-|>", color=DIM, lw=1.4))
    ax.text(232, 5, "TO PINHOLE", ha="center", va="bottom", fontsize=6, color=DIM, **FONT)
    # labels
    leader(ax, 26, -18, 6, -74, "X carriage — 316 on UHMW;\ncam-clamp locks swing", ha="left", fs=5.2, color=C_SWING, font=FONT, bbox=LBL_BG)
    leader(ax, 60, -6, 40, -78, "J3  X-carriage stub Ø9.5 (3/8\") → U-joint bore", ha="left", fs=5.0, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 53, 11.75, 12, 58, "4040N12 304 shaft support — two-piece clamp\nsecures the input stub to the X-slide (purple)", ha="left", fs=5.0, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 84, 11.9, 56, 86, "U-joint (tilt + swing, twist-locked) — Ruland USKC12-6-6-SS\nclamp screw per hub locks it on its keyed shaft", ha="left", fs=5.2, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 169, -40, 170, -74, "304 SS corner plate — J4 U-joint stub KEYED + CLAMPED", ha="left", fs=5.0, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 167, 24, 150, 66, "J5 COUNTERSUNK from the plate side → frame (M6 ×2/leg)", ha="left", fs=5.0, color=C_PIN, font=FONT, bbox=LBL_BG)
    leader(ax, 174, 10, 202, 38, "ACM secured FROM the frame INTO the ACM\n(countersunk in the frame back; front face clean)", ha="left", fs=5.0, color=C_PIN, font=FONT, bbox=LBL_BG)
    leader(ax, 170, -1.2, 128, -46, "countersunk cap screw:\ncorner plate → output stub (secures the shaft)", ha="left", fs=5.0, color=C_PIN, font=FONT, bbox=LBL_BG)
    leader(ax, 178, 40, 208, 90, "6061 angle L cradles the ACM (4mm) + muslin;\nACM on the pinhole face — Sheet 6", ha="left", fs=5.2, color=DIM, font=FONT, bbox=LBL_BG)
    ax.text(170, -92, "B — CROSS-SECTION  (Yd × X, to scale)",
            fontsize=7.0, fontweight="bold", color=OUT, ha="left", va="top", **FONT)
    ax.text(170, -85, "pinhole at left · X-slide at right (90° to it)",
            fontsize=5.6, color=DIM, ha="left", va="top", **FONT)


def sheet9():
    reset_label_registry()
    fig = plt.figure(figsize=(16, 10.5)); fig.patch.set_facecolor(BG)
    axA = fig.add_axes([0.02, 0.55, 0.31, 0.42]); axA.set_facecolor(BG)   # View A — square-on elevation (smaller)
    axB = fig.add_axes([0.35, 0.40, 0.64, 0.57]); axB.set_facecolor(BG)   # View B — cross-section (~50% larger)
    _corner_elevation(axA)
    _corner_section(axB)
    # notes
    axN = fig.add_axes([0.05, 0.08, 0.90, 0.26]); axN.set_xlim(0, 100); axN.set_ylim(0, 100); axN.axis("off")
    draw_notes(axN, [
        "HOW THE FILM PLANE HANGS OFF THE X (SWING) SLIDE — ONE OF FOUR CORNERS:",
        "The ACM backing board is captured in the 2x2 6061 Al angle perimeter frame (the muslin wraps + "
        "clamps to the angle's perp leg — Sheet 6). At each corner the angle bolts to a 304 SS CORNER PLATE "
        "(steel, not the expendable aluminum: the U-joint funnels the whole corner load into a few bolts — "
        "too concentrated for 6061 — and stainless matches the 303 SS U-joint in the wet zone).",
        "The corner plate carries a single U-JOINT (Ruland USKC12-6-6-SS). The U-joint's other yoke bolts to "
        "the X (SWING) slide carriage. So the corner is CARRIED BY the purple X-slide THROUGH the U-joint — "
        "it never bolts to the slide directly. The U-joint gives tilt + swing angular freedom (twist-locked); "
        "the X slide (~260mm) + the Z slide beneath it (~250mm, Sheet 8) take the in-plane arc travel.",
        "LOAD PATH, film → rail:  ACM board → 6061 angle frame → 304 SS corner plate → U-joint → "
        "X (swing) slide → Z (tilt) slide → carriage plate → 4-wheel acetal skate → 304 U-channel rail.",
    ], 1, 97, spacing=6.0, fs=7, title_fs=7.6, color=DIM, title_color=ANNO, font=FONT, width=140)
    # title block
    ax_tb = fig.add_axes([0.02, 0.0, 0.96, 0.055]); ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, "SHEET 9 OF 9",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="Frame + ACM ↔ U-joint ↔ X (swing) slide — corner connection detail",
                scale_note="TO SCALE — SEE PANELS",
                doc_id="TBS-FM01 · Film Plane Mechanism", height=0.75)
    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet9.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet9.png")


# ── Run all sheets ─────────────────────────────────────────────────────────────
def sheet8():
    reset_label_registry()
    fig = plt.figure(figsize=(17, 12)); fig.patch.set_facecolor(BG)
    axA = fig.add_axes([0.01, 0.08, 0.32, 0.86]); axA.set_facecolor(BG)   # tall left — the TILT (green) slide
    axB = fig.add_axes([0.37, 0.66, 0.61, 0.30]); axB.set_facecolor(BG)   # wide top-right — the SWING (purple) slide
    attach_tilt(axA)
    attach_plan(axB)
    # notes + fastener schedule
    axN = fig.add_axes([0.37, 0.06, 0.61, 0.55]); axN.set_xlim(0, 100); axN.set_ylim(0, 100); axN.axis("off")
    draw_notes(axN, [
        "FRAME ↔ CROSS-SLIDE ATTACHMENT — ONE OF FOUR CORNERS:",
        "The film frame is NOT bolted straight to a slide. Each corner hangs off BOTH cross-slides "
        "through a single U-joint, so the rigid plane can tilt AND swing while every corner stays "
        "square (the U-joint locks twist). Load path, film → rail: 2x2 6061 Al frame angle → 304 SS "
        "corner plate → U-joint → X (swing) slide → Z (tilt) slide → carriage plate → 4-wheel skate. At the "
        "BOTTOM corner the film hangs ~110mm BELOW the weight rail (Sheet 3, View A) — the stack hangs off "
        "skate and the ACM rises back up; the TOP corner is the mirror (film below its guide rail).",
        "THE TWO SLIDES do different jobs: the Z (tilt, green) slide takes the vertical arc-travel a "
        "rigid tilt forces on the corner (~250mm); the X (swing, purple) slide takes the horizontal "
        "arc-travel of a swing (~260mm). Both are 316 flat bar on UHMW pads with a gib; the gib drag "
        "holds the gravity-loaded Z axis, and a cam clamp locks each for the shot.",
        "FIVE JOINTS make the chain (rail→frame, top-down — the full stack is on Sheet 3, View A):",
        "  J1  Z-way seats on the carriage-plate face  M8 ×4 SS (the green Z-slide runs up the plate centre)",
        "  J2  X-way → Z-carriage ................... M8 ×4 SS",
        "  J3  X-carriage stub Ø9.5 (3/8\") → U-joint bore .. KEY + CLAMP HUB (Ruland USKC12-6-6-SS, keyway-clamp)",
        "  J4  U-joint 2nd bore → 3/8\" stub → 304 SS corner plate .. KEY + CLAMP HUB (both stubs keyed)",
        "  J5  2x2 6061 Al frame angle → 304 SS corner plate .. M6 ×2 per leg, vertical (tapped into the angle)",
        "The U-joint's two bores are its ONLY rotating link; everything else is a rigid bolted/clamped "
        "stack. Set the pose by hand (push each slide), then throw the cam clamps — no leadscrews "
        "(a pinhole's infinite depth of field makes this scene control, not focus).",
    ], 2, 99, 3.6, fs=6.2, title_fs=7.4, color=DIM, width=78, wrap=128, font=FONT)
    # title block
    ax_tb = fig.add_axes([0.03, 0.008, 0.94, 0.06]); ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, "SHEET 8 OF 9",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="Frame-corner ↔ cross-slide attachment — how the film frame hangs off the two slides through the U-joint",
                scale_note="Proportional (mm)",
                doc_id="TBS-FM01 · Film Plane Mechanism",
                height=0.75)
    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet8.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet8.png")


if __name__ == "__main__":
    print("Generating film plane mechanism drawings (rigid plane)...")
    sheet1()
    sheet2()
    sheet3()
    sheet4()
    sheet5()
    sheet6()
    sheet7()
    sheet8()
    sheet9()
    print("Done.")
