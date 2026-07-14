#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_film_plane_mechanism.py
Moveable film plane mechanism — engineering drawings (6 sheets)
OPTION A — RIGID PLANE: a fixed-size rigid rectangle whose ANGLE changes. The 4 corners ride
SLIDE-AND-CLAMP stages (igus DryLin friction slides) moved by hand in COORDINATED PAIRS —
single-axis tilt (top vs bottom) or swing (left vs right); limited combined; NO compound twist
(a rigid plane cannot warp). A pinhole has infinite depth of field, so this is scene control,
not focus: push each corner into position, then lock the cam clamp. Each corner connects through
a single Ruland US12-6-6-SS U-joint (2 axes, twist-locked) — no leadscrews, no handwheels.

Sheet 1 — Plan view (top-down): 4-corner rail layout, example configs
Sheet 2 — Elevations: side elevation (tilt) + plan cross-section (swing)
Sheet 3 — Frame & hardware detail: corner bracket, universal joint, ACM panel
         (superseded in detail by generate_corner_detail.py — film-corner-detail.png)
Sheet 4 — Movement specification table & BOM
Sheet 5 — Muslin clamp detail: cam-lever spring clamp
Sheet 6 — System schematic: four-corner frame front elevation
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc

from tbs_constants import FP_X_L, FP_X_R, FP_Y, FP_Y_MIN, FP_W, FP_H, PH_X as PH_X_C, MAX_TILT_DEG, MAX_SWING_DEG, DIAGRAMS_DIR, FP_ANGLE_LEG, FP_ANGLE_T, CLAMP_SPACING, CLAMP_BASE_W, CLAMP_BASE_H, CLAMP_BASE_T, CLAMP_LEVER_L, CLAMP_JAW_W, CLAMP_JAW_H, CLAMP_JAW_T, CLAMP_OPEN_GAP, CLAMP_SPRING_F, CLAMP_N_TOTAL, BRACE_Z_BOT, BRACE_Z_TOP, C_WID, WALL_T, IBC_WBKT_PLATE_W, IBC_WBKT_SEAT_PROJ, IBC_WBKT_SEAT_T, DRUM_CY, DRUM_R, DRUM_CX, DRUM_D
from tbs_title_block import title_block
from tbs_drawing import leader, draw_notes, draw_dim_h, draw_dim_v

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


# ── Wall-seat saddle drawing helpers (rev11 — replaces the retired brace cage) ──
# Each of the 8 rail ends sits on an IBC-style wall-seat saddle (back-plate + seat +
# gusset, 4-bolt through-wall + exterior plate). The container shell carries rigidity.
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

    # ── WALL-SEAT SADDLES (rev11 — replaces the brace cage) — plan view ──
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
           "WALL-SEAT SADDLE (6) + COMBINED PLATE (2)\nIBC-style: 4-bolt + exterior plate\nLEFT thumb-screw / RIGHT bolted",
           color=STRUCT, ha="center", fs=6.5, font=FONT)
    # rev12: the bottom-right (BR) rail ends share a combined corner plate with
    # the right walkway right beam (replaces the 2 BR saddles).
    leader(ax, RAIL_X_R, proj,
           RAIL_X_R - 700, proj + 200,
           "BR ENDS → COMBINED CORNER PLATE (×2)\nshared with the right walkway right beam\n(rev12 — replaces the BR saddles)",
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

    # B2 (rev9): the drum is offset clear of the X=150 rail (via the hinge-panel
    # punch-out bay), so the LEFT RAIL IS CONTINUOUS — no demountable segment.
    leader(ax, RAIL_X_L, DRUM_CY,
           RAIL_X_L - 600, DRUM_CY + 250,
           "LEFT RAIL CONTINUOUS\n(drum offset out via panel bay —\nno demountable segment)",
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
            "4 CORNER SLIDE-AND-CLAMP CARRIAGES (igus DryLin, RIGID PLANE, COORDINATED PAIRS)  ·  TILT = CEILING vs FLOOR  ·  SWING = LEFT vs RIGHT",
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
    title_block(ax, "SHEET 1 OF 6",
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
    ax.text(W/2, RAIL_H/2, "FLOOR DEPTH SLIDE  DryLin W (316SS)  ×2  (BL  +  BR — hand-slide, cam-clamp, moved as a pair)",
            color=BG, fontsize=5.5, ha="center", va="center", **FONT, zorder=6)
    ax.add_patch(Rectangle((0, H-RAIL_H), C_WID, RAIL_H,
                           fc=RAIL, ec=WHITE, lw=0.8, zorder=5, alpha=0.9))
    ax.text(W/2, H-RAIL_H/2, "CEILING DEPTH SLIDE  DryLin W (316SS)  ×2  (TL  +  TR — hand-slide, cam-clamp, moved as a pair)",
            color=BG, fontsize=5.5, ha="center", va="center", **FONT, zorder=6)

    # ── WALL-SEAT SADDLES — side elevation (Yd on X-axis, Z on Y-axis), rev11/12 ──
    # A saddle at each wall (Yd0 + Yd C_WID) at both rail heights: back-plate on the
    # wall + a seat projecting in that the rail end rests on (replaces the brace cage).
    # rev12: the bottom-right (BR) ends sit on the combined corner plate shared with
    # the right walkway (not a standalone saddle).
    draw_brace_portal_yd_z(ax_tilt, STRUCT, lw=1.2, alpha=0.65, z=4)
    leader(ax_tilt, IBC_WBKT_SEAT_PROJ / 2, BRACE_Z_TOP,
           IBC_WBKT_SEAT_PROJ / 2 - 180, BRACE_Z_TOP + 130,
           "WALL-SEAT SADDLE (both walls)\nIBC-style, 4-bolt + ext. plate\n(BR ends = combined plate, shared w/ walkway)",
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
    ax.text(W/2, H+215, "Section through centerline  ·  vertical bridge = Z cross-slide (DryLin T, absorbs tilt foreshorten, preload holds gravity)  ·  slide-and-clamp, moved in coordinated pairs (rigid plane)",
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
    ax.text(L/2, W+375, "Section at ceiling height  ·  horizontal bridge = X cross-slide (DryLin T, floats free then cam-clamps, absorbs swing foreshorten)  ·  left/right slide-and-clamp as pairs (rigid single-axis swing)",
            color=DIM, fontsize=6.5, ha="center", **FONT)

    # Combined title
    fig.text(0.5, 0.98, "SHEET 2 — TILT ELEVATION (left)  &  SWING CROSS-SECTION (right)",
             color=WHITE, fontsize=11, ha="center", fontweight="bold", **FONT)

    # Title block (full-figure overlay for multi-subplot sheet)
    ax_tb = fig.add_axes([0, 0, 1, 1], facecolor="none")
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 2 OF 6",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="Tilt elevation & Swing cross-section",
                scale_note="Proportional (mm)",
                doc_id="TBS-FM01 · Film Plane Mechanism")

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet2.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet2.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — FRAME & HARDWARE DETAIL (Option A — rigid plane)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet3():
    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor(BG)

    positions = [
        (0.04, 0.52, 0.44, 0.42),  # TL — corner carriage bracket
        (0.52, 0.52, 0.44, 0.42),  # TR — rail + carriage cross-section
        (0.04, 0.10, 0.44, 0.36),  # BL — universal joint / rod-end
        (0.52, 0.10, 0.44, 0.36),  # BR — ACM panel arrangement
    ]
    axes = []
    for p in positions:
        a = fig.add_axes(p)
        a.set_facecolor(BG)
        a.axis("off")
        axes.append(a)
    ax_bracket, ax_rail, ax_joint, ax_acm = axes

    # ── TL: Slide-and-clamp corner stack (kinematic sub-assembly) ─────────────
    # From the depth rail up to the film frame: depth slide + cam clamp, then the
    # X and Z accommodation cross-slides, the single U-joint, and the frame corner.
    ax = ax_bracket
    ax.set_xlim(-160, 560); ax.set_ylim(-210, 400); ax.set_aspect("equal")

    C_POLY = "#C9B78F"   # self-lube polymer liner (igus iglide / DryLin)
    C_CLAMP = "#3A3A40"  # cam-clamp body
    C_PIN = "#B07010"    # set screws / pins (gold)
    cx = 150; bw = 130

    # vertical connector spine (behind the blocks)
    ax.plot([cx, cx], [-150, 300], color=DIM, lw=1.0, ls=(0, (3, 2)), zorder=2)

    def _stackbox(y0, h, fc, label, sublabel, ldr_col):
        ax.add_patch(Rectangle((cx - bw/2, y0), bw, h, fc=fc, ec=WHITE, lw=1.4, zorder=5))
        txt_col = BG if fc in (MECH, C_CLAMP, ANNO) else ANNO
        ax.text(cx, y0 + h/2, label, color=txt_col, fontsize=6, ha="center",
                va="center", fontweight="bold", **FONT, zorder=6)
        leader(ax, cx + bw/2, y0 + h/2, cx + bw/2 + 120, y0 + h/2,
               sublabel, color=ldr_col, ha="left", va="center", fs=5.6,
               arrow_style="-|>", font=FONT)

    # 1. depth slide (DryLin W) — a wider rail block with a carriage on it
    ax.add_patch(Rectangle((cx - bw/2 - 20, -178), bw + 40, 22,
                           fc=RAIL, ec=WHITE, lw=1.4, zorder=4))
    ax.text(cx, -167, "DryLin W RAIL (316SS)",
            color=BG, fontsize=5.5, ha="center", va="center", **FONT, zorder=5)
    _stackbox(-150, 44, MECH, "DEPTH CARRIAGE", "DryLin W carriage\n(depth = tilt+swing+focus)", MECH)
    # cam clamp lever off the depth carriage (left)
    ax.add_patch(Circle((cx - bw/2, -128), 7, fc=C_T3, ec=WHITE, lw=0.9, zorder=8))
    ax.plot([cx - bw/2, cx - bw/2 - 60], [-128, -168], color=C_T3, lw=2.4,
            solid_capstyle="round", zorder=8)
    leader(ax, cx - bw/2 - 55, -165, cx - bw/2 - 70, -110,
           "CAM CLAMP\n(locks each slide)", color=C_T3, ha="right", va="center",
           fs=5.6, arrow_style="-|>", font=FONT)
    # 2. X cross-slide (DryLin T, floats)
    _stackbox(-90, 40, C_POLY, "X CROSS-SLIDE", "DryLin T — floats free,\nabsorbs SWING foreshorten", "#8A6A2A")
    # 3. Z cross-slide (DryLin T, preload hold)
    _stackbox(-32, 40, C_POLY, "Z CROSS-SLIDE", "DryLin T adj-clearance —\npreload holds gravity, absorbs TILT", "#8A6A2A")
    # 4. U-joint
    ax.add_patch(Circle((cx, 55), 30, fc=STRUCT2, ec=WHITE, lw=1.4, zorder=6))
    ax.plot([cx - 24, cx + 24], [55, 55], color=C_T2, lw=1.8, zorder=7, solid_capstyle="round")
    ax.plot([cx, cx], [55 - 24, 55 + 24], color=MECH, lw=1.8, zorder=7, solid_capstyle="round")
    ax.add_patch(Circle((cx, 55), 9, fc=BG, ec=WHITE, lw=0.8, zorder=8))
    leader(ax, cx + 30, 55, cx + bw/2 + 120, 55,
           "SINGLE U-JOINT\nRuland US12-6-6-SS\n(2 crossed pins: tilt+swing,\ntwist-locked, 45°)",
           color=STRUCT2, ha="left", va="center", fs=5.6, arrow_style="-|>", font=FONT)
    # 5. film frame corner
    _stackbox(100, 50, ANNO, "FILM FRAME", "rigid ACM back\n(fixed size)", C_FLAT)

    ax.text(200, 372, "SLIDE-AND-CLAMP CORNER STACK\n(ONE PER CORNER — 4 TOTAL)",
            color=WHITE, fontsize=8, ha="center", va="bottom", **FONT)
    ax.text(200, -200,
            "EACH CORNER: DryLin W depth slide + cam clamp  +  X & Z DryLin T cross-slides  +  US12-6-6-SS U-joint",
            color=DIM, fontsize=5.6, ha="center", **FONT)

    # ── TR: DryLin W depth-slide cross-section (dry self-lube polymer) ─────────
    ax = ax_rail
    ax.set_xlim(-220, 400); ax.set_ylim(-160, 350); ax.set_aspect("equal")

    # base rail (316SS) with two guide upstands = the DryLin W double rail
    ax.add_patch(Rectangle((-70, 0), 140, 16, fc=RAIL, ec=WHITE, lw=1.5, zorder=3))
    for ux in (-48, 48):
        ax.add_patch(Rectangle((ux - 10, 16), 20, 26, fc=RAIL, ec=WHITE, lw=1.3, zorder=4))
    # polymer liner (iglide) — the dry low-friction bearing surface, wraps each upstand
    for ux in (-48, 48):
        ax.add_patch(Rectangle((ux - 14, 16), 4, 30, fc=C_POLY, ec=WHITE, lw=0.6, zorder=6))
        ax.add_patch(Rectangle((ux + 10, 16), 4, 30, fc=C_POLY, ec=WHITE, lw=0.6, zorder=6))
    # polymer carriage plate over the rail, wrapping down outside the upstands
    ax.add_patch(Rectangle((-74, 46), 148, 26, fc=MECH, ec=WHITE, lw=1.5, zorder=5))
    for ux in (-62, 48):
        ax.add_patch(Rectangle((ux, 16), 14, 34, fc=MECH, ec=WHITE, lw=1.3, zorder=5))

    draw_dim_h(ax, -70, 70, -46, "DryLin W rail",
               offset=14, color=DIM, above=False, fs=6, font=FONT)
    draw_dim_v(ax, 96, 46, 72, "carriage",
               offset=14, color=MECH, right=True, fs=6, font=FONT)

    ax.text(0, 66 + 120, "DEPTH-SLIDE CROSS-SECTION\nigus DryLin W (316SS rail)",
            color=WHITE, fontsize=7.5, ha="center", va="bottom", **FONT)
    leader(ax, -58, 31, -150, 70, "self-lube POLYMER liner\n(iglide — runs DRY, wash-safe;\nno rollers to corrode)",
           color="#8A6A2A", ha="right", va="center", fs=5.6, arrow_style="-|>", font=FONT)
    ax.text(0, 59, "DryLin W\nCARRIAGE", color=BG, fontsize=6,
            ha="center", va="center", **FONT, zorder=7)
    ax.text(0, -96,
            "Z & X CROSS-SLIDES: DryLin T single rail + adjustable-clearance carriage",
            color=DIM, fontsize=6, ha="center", **FONT)
    ax.text(0, -128,
            "STATIC positioning · modest load per corner · push-to-slide, cam-clamp",
            color=DIM, fontsize=6, ha="center", **FONT)

    # ── BL: U-joint + stub/support detail — how each side secures ─────────────
    ax = ax_joint
    ax.set_xlim(-72, 432); ax.set_ylim(-128, 196); ax.set_aspect("equal")

    # TWO VIEWS (panel ~1:1, 1 unit ≈ 1mm). LEFT — the Ruland US12-6-6-SS U-joint in
    # section: a centre block carrying two crossed pins in bronze plain bearings; each
    # yoke hub grips OUR stub shaft with a set screw. RIGHT — that stub clamped in the
    # McMaster 4040N12 base-mount support (removable cap + 2 clamp screws).

    # ── VIEW 1: U-joint (Ruland US12-6-6-SS), cut through the swing pin ──
    v1x, v1y = 110, 68
    # centre block (joint body)
    ax.add_patch(Rectangle((v1x-24, v1y-20), 48, 40, fc=STRUCT2, ec=WHITE, lw=1.4, zorder=5))
    # swing pin in section (vertical) — bronze plain bearing in the block
    ax.add_patch(Rectangle((v1x-6, v1y-32), 12, 64, fc=C_T2, ec=WHITE, lw=0.9, zorder=6))
    # tilt pin, end-on (the other axis)
    ax.add_patch(Circle((v1x, v1y), 6, fc=MECH, ec=WHITE, lw=0.8, zorder=7))
    # two yoke hubs (part of the joint) + OUR stub shafts, set-screw locked
    for sgn, tag in ((-1, "carrier"), (1, "frame")):
        hub_x = v1x + sgn*24
        ax.add_patch(Rectangle((min(hub_x, hub_x+sgn*20), v1y-11), 20, 22,
                               fc=STRUCT2, ec=WHITE, lw=1.2, zorder=5))   # yoke hub
        stub_x0 = hub_x + sgn*20
        ax.add_patch(Rectangle((min(stub_x0, stub_x0+sgn*40), v1y-6), 40, 12,
                               fc=MECH, ec=WHITE, lw=1.1, zorder=4))       # our stub shaft
        # set screw on the hub
        ax.add_patch(Circle((hub_x + sgn*10, v1y+11), 3.5, fc=C_PIN, ec=WHITE, lw=0.7, zorder=8))
    # protective boot (ghosted bellows over the joint)
    ax.add_patch(Rectangle((v1x-30, v1y-27), 60, 54, fill=False, ec=DIM, lw=1.0, ls=(0, (4, 3)), zorder=9))
    ax.text(v1x, 150, "U-JOINT SECTION", color=WHITE, fontsize=6, ha="center", va="bottom", **FONT)
    leader(ax, v1x, v1y-20, v1x-40, v1y+40, "CENTRE BLOCK\n(2 crossed pins,\nbronze plain bearing)", color=STRUCT2, ha="center", fs=5.4, font=FONT)
    leader(ax, v1x-54, v1y, v1x-66, v1y-56, "OUR STUB SHAFT\n3/8\" 304 SS\n(set-screw locked)", color=MECH, ha="center", fs=5.4, font=FONT)
    leader(ax, v1x+10, v1y+11, v1x+52, v1y+46, "HUB SET SCREW", color=C_PIN, ha="left", fs=5.4, font=FONT)
    leader(ax, v1x+30, v1y+20, v1x+30, v1y+62, "BOOT (nitrile, dry)\nUBOOT12/19-NI-KIT", color=DIM, ha="center", fs=5.4, font=FONT)

    # ── VIEW 2: stub clamped in the 4040N12 base-mount support ──
    v2x, v2y = 330, 60
    # support body + base feet
    ax.add_patch(Rectangle((v2x-32, v2y-6), 64, 34, fc=STRUCT, ec=WHITE, lw=1.3, zorder=4))     # body
    ax.add_patch(Rectangle((v2x-46, v2y-18), 92, 12, fc=STRUCT, ec=WHITE, lw=1.3, zorder=4))    # base
    for fx in (-38, 38):
        ax.add_patch(Circle((v2x+fx, v2y-12), 3.5, fc=BG, ec=WHITE, lw=0.7, zorder=6))          # mount holes
    # removable cap + 2 clamp screws
    ax.add_patch(Rectangle((v2x-32, v2y+28), 64, 12, fc=STRUCT2, ec=WHITE, lw=1.2, zorder=5))   # cap
    for sx in (-20, 20):
        ax.add_patch(Circle((v2x+sx, v2y+34), 3.5, fc=C_PIN, ec=WHITE, lw=0.7, zorder=7))       # clamp screws
    # the stub shaft clamped through it (into page — shown as a bore)
    ax.add_patch(Circle((v2x, v2y+13), 9, fc=MECH, ec=WHITE, lw=1.1, zorder=6))
    ax.add_patch(Circle((v2x, v2y+13), 4, fc=BG, ec=WHITE, lw=0.7, zorder=7))
    ax.text(v2x, 150, "STUB CLAMPED IN SUPPORT", color=WHITE, fontsize=6, ha="center", va="bottom", **FONT)
    leader(ax, v2x+32, v2y+34, v2x+52, v2y+58, "REMOVABLE CAP\n+ 2 clamp screws", color=C_PIN, ha="left", fs=5.4, font=FONT)
    leader(ax, v2x, v2y+13, v2x-56, v2y+40, "STUB SHAFT\n(clamped, no slip)", color=MECH, ha="right", fs=5.4, font=FONT)
    leader(ax, v2x-46, v2y-12, v2x-58, v2y-52, "4040N12 BASE-MOUNT\nSHAFT SUPPORT (304 SS)\n→ bolts to X-slide / frame", color=STRUCT, ha="right", fs=5.4, font=FONT)

    ax.text(180, 178, "CORNER JOINT DETAIL — SINGLE U-JOINT (US12-6-6-SS); EACH STUB CLAMPED IN A 4040N12 SUPPORT",
            color=WHITE, fontsize=6.5, ha="center", va="bottom", **FONT)
    ax.text(180, -116,
            "Each side: a 3/8\" 304 SS stub is set-screw locked in the U-joint hub and clamped in a 4040N12 support (removable cap) — one to the frame, one to the X-slide carriage",
            color=DIM, fontsize=5.5, ha="center", **FONT)

    # ── BR: single rigid ACM backing (Option A — no fold) ────────────────────
    ax = ax_acm
    ax.set_xlim(-100, 650); ax.set_ylim(-130, 350); ax.set_aspect("equal")

    panel_h = 240; panel_w = 300
    px0, py0 = 130, 40
    ax.add_patch(Rectangle((px0, py0), panel_w, panel_h, fc=ANNO, ec=WHITE,
                           lw=1.8, zorder=3, alpha=0.75))
    for (bx, by) in [(px0, py0), (px0+panel_w, py0),
                     (px0, py0+panel_h), (px0+panel_w, py0+panel_h)]:
        ax.add_patch(Circle((bx, by), 13, fc=MECH, ec=WHITE, lw=0.8, zorder=5))
    ax.text(px0+panel_w/2, py0+panel_h/2, "SINGLE RIGID\nACM BACKING",
            color=BG, fontsize=8, ha="center", va="center", **FONT, zorder=6)
    ax.text(px0+panel_w/2, py0+panel_h+22, "FIXED-SIZE — rotates rigidly (no fold)",
            color=C_FLAT, fontsize=7, ha="center", **FONT)
    ax.text(px0+panel_w/2, py0-22,
            f"Dibond ACM 4mm · {RAIL_X_R-RAIL_X_L+0}×{H}mm · bonded to angle frame",
            color=DIM, fontsize=6, ha="center", **FONT)
    draw_dim_v(ax, px0-55, py0, py0+panel_h, f"{H}mm (fixed)",
               offset=60, color=DIM, font=FONT)

    ax.text(280, 310, "ACM BACKING PANEL\nSINGLE RIGID SHEET — FIXED SIZE, NO HINGE",
            color=WHITE, fontsize=7.5, ha="center", va="bottom", **FONT)
    ax.text(280, -95,
            "PANEL: DIBOND 4mm  ·  the plane never grows, so no folding two-panel system is needed",
            color=DIM, fontsize=6.5, ha="center", **FONT)

    fig.text(0.5, 0.97, "SHEET 3 — FRAME & HARDWARE DETAILS",
             color=WHITE, fontsize=11, ha="center", fontweight="bold", **FONT)

    # Title block (full-figure overlay for multi-subplot sheet)
    ax_tb = fig.add_axes([0, 0, 1, 1], facecolor="none")
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 3 OF 6",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="Frame & hardware details",
                scale_note="As noted",
                doc_id="TBS-FM01 · Film Plane Mechanism")

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet3.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet3.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 4 — MOVEMENT SPECIFICATION TABLE & BOM (Option A — rigid plane)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet4():
    fig, ax = plt.subplots(figsize=(16, 13))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis("off")

    ax.text(0.5, 0.968, "SHEET 4 — MOVEMENT SPECIFICATION",
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
        "FILM-PLANE TRAVEL (rev9 B2 — continuous left rail)",
        f"FILM MODE: carriage free over the FULL travel (Yd 100–{FP_Y}) for tilt/swing,",
        "   both rails continuous — no demountable segment, no drum interlock.",
        f"DRUM: offset out via the hinge-panel punch-out bay (center X={DRUM_CX}mm),",
        "   so the Ø900 housing clears the X=150 left rail entirely.",
        "WALKWAY: frame bottom RAISED to Z=150mm (RAIL_OFF_BOT) to clear the Z130 walkway; active image = inter-rail span.",
        "   Clears the lowered walkway deck (Z=65mm) by 35mm — film plane travels above the in-place walkway.",
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
        "CORNER HARDWARE (per corner ×4 — slide-and-clamp, single U-joint):",
        "U-joint  1× Ruland US12-6-6-SS (303 SS, self-lube bronze, 45°)   ·   boot  1× Ruland UBOOT12/19-NI-KIT (nitrile, fitted dry)",
        "Shaft support  2× McMaster 4040N12 (304 SS)   ·   stub  2× 3/8\" 304 SS (McMaster 89535K873)   ·   nylon-isolated at the T-slide brackets",
        "Depth (Y)  DryLin W 316SS ~2.2 m + WW-HKX cam clamp   ·   Vertical (Z)  DryLin T adj-clearance TW-01-20-HKA   ·   Horizontal (X)  DryLin T TW-01-20 + clamp",
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
    title_block(ax, "SHEET 4 OF 6",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="Movement specification & BOM",
                scale_note="Not to scale",
                doc_id="TBS-FM01 · Film Plane Mechanism")

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet4.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet4.png")


# ═══════════════════════════════════════════════════════════════════════════════
# Sheet 5 — Muslin Clamp Detail: Cam-Lever Spring Clamp
#
# Three sub-panels:
#   A (top-left):  Cross-section of clamp on 2"×2" aluminum angle profile
#   B (top-right): Clamp in open vs closed positions (side view)
#   C (bottom):    Elevation: 3 clamps at 150mm spacing along frame edge
# ═══════════════════════════════════════════════════════════════════════════════
def sheet5():
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
    RAIL_H = 30       # DryLin W depth rail height (schematic)
    RAIL_W = 20       # DryLin W depth rail visible width (schematic)
    CARRIAGE_H = 28   # DryLin W carriage height (schematic)
    CARRIAGE_W = 44   # DryLin W carriage width (schematic)
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

    # ── HGR20 Rail (bolted to ceiling, hangs down) ───────────────────────────
    C_RAIL = "#708090"
    rail_cx = LEG / 2  # centered on angle
    ax_a.add_patch(Rectangle(((rail_cx - RAIL_W / 2), (rail_bot)),
                              (RAIL_W), (RAIL_H),
                              fc=C_RAIL, ec=ANNO, lw=1.2, zorder=4))
    leader(ax_a, (rail_cx), (rail_bot + RAIL_H / 2),
           (rail_cx + 50), (rail_bot + RAIL_H / 2),
           "DryLin W\nDEPTH RAIL\n(316SS, into page)",
           color=C_RAIL, fs=5.5, ha="left", va="center",
           arrow_style="-|>", font=FONT)

    # ── HGH20CA Carriage block ───────────────────────────────────────────────
    C_CARR = "#607080"
    ax_a.add_patch(Rectangle(((rail_cx - CARRIAGE_W / 2), (carriage_bot)),
                              (CARRIAGE_W), (CARRIAGE_H),
                              fc=C_CARR, ec=ANNO, lw=1.2, zorder=5))
    leader(ax_a, (rail_cx + CARRIAGE_W / 2), (carriage_bot + CARRIAGE_H / 2),
           (rail_cx + 55), (carriage_bot + CARRIAGE_H / 2 - 10),
           "DryLin W\nCARRIAGE\n(depth slide)",
           color=C_CARR, fs=5.5, ha="left", va="center",
           arrow_style="-|>", font=FONT)

    # ── Suspension bracket ───────────────────────────────────────────────────
    C_BRKT = "#8090A0"
    ax_a.add_patch(Rectangle(((rail_cx - BRACKET_W / 2), (bracket_bot)),
                              (BRACKET_W), (BRACKET_H),
                              fc=C_BRKT, ec=ANNO, lw=1.0, zorder=4))
    ax_a.text((rail_cx), (bracket_bot + BRACKET_H / 2),
              "BRACKET", ha="center", va="center",
              fontsize=5, color="white", fontweight="bold", **FONT, zorder=15)

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
        (rail_bot + RAIL_H / 2, "DEPTH SLIDE"),
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
    title_block(ax_tb, "SHEET 5 OF 6",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="Muslin clamp detail — cam-lever spring clamp",
                scale_note="MULTIPLE SCALES — SEE INDIVIDUAL PANELS",
                doc_id="TBS-FM01 · Film Plane Mechanism",
                height=0.75)

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet5.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet5.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 6 — SYSTEM SCHEMATIC: Four-corner frame front elevation
#
# View: looking at the film plane from the pinhole side (interior elevation).
# Shows ceiling/floor depth-slide pairs (DryLin W), four corner slide-and-clamp
# carriages with cam clamps, film plane frame with a single U-joint at each corner.
# The long depth rail runs into the page (optical axis); shown end-on here.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet6():
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
    # Each corner = a DryLin W depth-slide carriage (the long depth rail runs into
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

    # ── Wall-seat saddles (front elevation), rev11 ────────────────────────────
    # A saddle back-plate at each of the 4 rail-end corners (near + far walls project
    # to the same X-Z here). Replaces the retired demountable brace cage.
    draw_brace_portal(ax, STRUCT, lw=1.4, alpha=0.55, z=4)
    # Point to the bottom-left saddle and place the text INSIDE the frame's open
    # lower-left quadrant — the margins (left: INTERIOR HEIGHT dim, bottom: width
    # dims + title block) are all crowded.
    leader(ax, RAIL_X_L, BRACE_Z_BOT,
           RAIL_X_L + 620, BRACE_Z_BOT + 520,
           "WALL-SEAT SADDLES (8) — IBC-style: 4-bolt + ext. plate\nLEFT thumb-screw / RIGHT bolted",
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
            f"{RAIL_X_R - RAIL_X_L}mm wide  ×  {H}mm tall",
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

    # Depth-slide leader (from the TL carriage, end-on) — placed well below the U-joint label
    leader(ax, RAIL_X_L, tl_cy,
           RAIL_X_L + 470, tl_cy - 470,
           "DEPTH SLIDE — DryLin W 316SS\n2200mm (runs into page)\nhand-slide + cam clamp",
           color=RAIL, ha="left", fs=6.5, font=FONT)

    # Carriage leader (from TR carriage)
    leader(ax, RAIL_X_R + carr_w / 2, FH - rail_h - carr_h / 2,
           RAIL_X_R + 450, FH - rail_h - carr_h / 2 - 300,
           "DryLin W CARRIAGE\n(depth slide, per corner)",
           color=MECH, ha="left", fs=6.5, font=FONT)

    # Rail leader (from TR ceiling depth slide)
    leader(ax, RAIL_X_R + rail_len / 2, FH - rail_h / 2,
           RAIL_X_R + 450, FH - 150,
           "DryLin W RAIL 316SS\n2200mm (into page)",
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
            "SHEET 6 — SYSTEM SCHEMATIC  (FRONT ELEVATION — LOOKING FROM PINHOLE SIDE)",
            color=WHITE, fontsize=9, ha="center", fontweight="bold", **FONT)
    ax.text(FW / 2, FH + 290,
            "4 CORNER SLIDE-AND-CLAMP CARRIAGES (igus DryLin, COORDINATED PAIRS)  ·  CAM CLAMP + SINGLE U-JOINT + X-Z CROSS-SLIDES AT EACH CORNER",
            color=DIM, fontsize=7, ha="center", **FONT)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 6 OF 6",
                drawing_title="MOVEABLE FILM PLANE",
                subtitle="System schematic — four-corner frame front elevation",
                scale_note="Schematic — not to scale",
                doc_id="TBS-FM01 · Film Plane Mechanism",
                height=0.05)

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet6.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet6.png")


# ── Run all sheets ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating film plane mechanism drawings (rigid plane)...")
    sheet1()
    sheet2()
    sheet3()
    sheet4()
    sheet5()
    sheet6()
    print("Done.")
