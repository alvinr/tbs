#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_film_plane_mechanism.py
Moveable film plane mechanism — engineering drawings (6 sheets)
4-CORNER INDEPENDENT DESIGN: TL, TR, BL, BR each driven by its own leadscrew.
Supports full tilt, swing, and compound tilt+swing independently.

Sheet 1 — Plan view (top-down): 4-corner rail layout, example configs
Sheet 2 — Elevations: side elevation (tilt) + plan cross-section (swing)
Sheet 3 — Frame & hardware detail: corner bracket, universal joint, ACM panel
Sheet 4 — Movement specification table & BOM
Sheet 5 — Muslin clamp detail: cam-lever spring clamp
Sheet 6 — System schematic: four-corner frame front elevation
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Arc, Polygon
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe

from tbs_constants import (
    FP_X_L, FP_X_R, FP_Y, FP_Y_MIN, FP_W, FP_H,
    PH_X as PH_X_C, PH_H as PH_H_C,
    MAX_TILT_DEG, MAX_SWING_DEG, RAIL_SPAN, DIAGRAMS_DIR,
    FP_ANGLE_LEG, FP_ANGLE_T,
    CLAMP_SPACING, CLAMP_BASE_W, CLAMP_BASE_H, CLAMP_BASE_T,
    CLAMP_LEVER_L, CLAMP_JAW_W, CLAMP_JAW_H, CLAMP_JAW_T,
    CLAMP_OPEN_GAP, CLAMP_SPRING_F,
    CLAMP_N_HORIZ, CLAMP_N_VERT, CLAMP_N_TOTAL,
    BRACE_RHS, BRACE_T, BRACE_Z_BOT, BRACE_Z_TOP,
    C_WID, WALL_T,
    IBC_WBKT_PLATE_W, IBC_WBKT_SEAT_PROJ, IBC_WBKT_SEAT_T,
    DRUM_CY, DRUM_R, DRUM_CX, DRUM_D,
)
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
C_T3    = "#CC2020"   # compound config (red)
RAIL    = "#5A3E00"   # rail (dark brown-gold — dark enough for white text labels)
MECH    = "#2A6B2A"   # mechanism/carriage (dark green — dark enough for white text)
PINHOLE = "#CC6600"   # pinhole aperture (orange, visible on white)

# ── Container dimensions (mm) ─────────────────────────────────────────────────
L = 5893   # interior length (film plane spans this direction)
W = 2362   # interior width = optical axis = focal length
H = 2388   # interior height
from tbs_constants import WALL_T

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
    ("Tilt+Swing\n(comb.)", 14.0, 10.0, C_T3,   ":"),
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

    # Pinhole (X=2874mm in new layout, recenterd on new film plane)
    ph_x = PH_X_C
    ax.add_patch(Circle((ph_x, 0), 60, fc=PINHOLE, ec=WHITE, lw=1.5, zorder=6))
    ax.add_patch(Circle((ph_x, 0), 20, fc=BG, ec=WHITE, lw=1.0, zorder=7))
    ax.text(ph_x + 130, 75, f"PINHOLE  X={ph_x}mm  Ø2.17mm", color=PINHOLE, fontsize=7, **FONT)

    # ── 4 INDEPENDENT RAILS — one at each corner ──────────────────────────────
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

    # Travel dim
    tr_x = RAIL_X_L - RAIL_W - 50
    tr_tick = 15
    ax.annotate("", xy=(tr_x, D_FAR-20),
                xytext=(tr_x, D_NEAR+20),
                arrowprops=dict(arrowstyle="<->", color=WHITE, lw=0.8, mutation_scale=5))
    ax.plot([tr_x - tr_tick, tr_x + tr_tick], [D_NEAR+20, D_NEAR+20], color=WHITE, lw=0.6)
    ax.plot([tr_x - tr_tick, tr_x + tr_tick], [D_FAR-20, D_FAR-20], color=WHITE, lw=0.6)
    ax.text(RAIL_X_L - RAIL_W - 150, (D_NEAR+D_FAR)/2,
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
            "4 INDEPENDENT CORNER CARRIAGES  ·  TILT = CEILING vs FLOOR  ·  SWING = LEFT SIDE vs RIGHT SIDE",
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
                drawing_title="MOVEABLE FILM PLANE (4-CORNER)",
                subtitle="Plan view — 4-corner rail layout",
                scale_note="Proportional (mm)",
                doc_id="TBS-FM01 · Film Plane Mechanism",
                height=0.05)

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet1.png", dpi=130, bbox_inches="tight", facecolor=BG)
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
    ax.text(W/2, RAIL_H/2, "FLOOR RAIL  HGR20  ×2  (BL  +  BR — independent leadscrews)",
            color=BG, fontsize=5.5, ha="center", va="center", **FONT, zorder=6)
    ax.add_patch(Rectangle((0, H-RAIL_H), C_WID, RAIL_H,
                           fc=RAIL, ec=WHITE, lw=0.8, zorder=5, alpha=0.9))
    ax.text(W/2, H-RAIL_H/2, "CEILING RAIL  HGR20  ×2  (TL  +  TR — independent leadscrews)",
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
    ax.text(W/2, H+215, "Section through centerline  ·  each corner carriage moves independently",
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

    # Pinhole (recenterd at X=2874 on new film plane)
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
    ax.text(L/2, W+375, "Section at ceiling height  ·  left and right corner carriages move independently",
            color=DIM, fontsize=6.5, ha="center", **FONT)

    # Combined title
    fig.text(0.5, 0.98, "SHEET 2 — TILT ELEVATION (left)  &  SWING CROSS-SECTION (right)",
             color=WHITE, fontsize=11, ha="center", fontweight="bold", **FONT)

    # Title block (full-figure overlay for multi-subplot sheet)
    ax_tb = fig.add_axes([0, 0, 1, 1], facecolor="none")
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 2 OF 6",
                drawing_title="MOVEABLE FILM PLANE (4-CORNER)",
                subtitle="Tilt elevation & Swing cross-section",
                scale_note="Proportional (mm)",
                doc_id="TBS-FM01 · Film Plane Mechanism")

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet2.png", dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet2.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — FRAME & HARDWARE DETAIL (4-corner design)
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

    # ── TL: Corner carriage bracket assembly ──────────────────────────────────
    ax = ax_bracket
    ax.set_xlim(-100, 550); ax.set_ylim(-200, 400); ax.set_aspect("equal")

    # Rail (running into page — shown as end-on rectangle)
    rl_w = 44; rl_h = 30
    ax.add_patch(FancyBboxPatch((-rl_w/2, 0), rl_w, rl_h,
                               boxstyle="round,pad=2",
                               fc=RAIL, ec=WHITE, lw=1.5, zorder=3))
    ax.text(0, -40, "RAIL\nHGR20", color=RAIL, fontsize=6, ha="center", **FONT)

    # Carriage block (2× per corner)
    cb_w = 63; cb_h = 55
    ax.add_patch(Rectangle((-cb_w/2, rl_h-4), cb_w, cb_h,
                           fc=MECH, ec=WHITE, lw=1.5, zorder=5))
    ax.add_patch(Rectangle((-cb_w/2 + 4, rl_h + cb_h - 2), cb_w-8, cb_h*0.7,
                           fc=MECH, ec=WHITE, lw=1.0, alpha=0.6, zorder=5))
    ax.text(0, rl_h+cb_h/2, "HGH20CA\n×2 per\ncorner",
            color=BG, fontsize=5.5, ha="center", va="center", **FONT, zorder=6)

    # Corner bracket L-plate
    bk_h = 130; bk_w = 80
    ax.add_patch(Rectangle((cb_w/2, rl_h), bk_w, bk_h,
                           fc=STRUCT2, ec=WHITE, lw=1.5, zorder=6))
    # Leadscrew hole through bracket
    ax.add_patch(Circle((cb_w/2 + bk_w/2, rl_h + bk_h*0.6), 12,
                        fc=BG, ec=WHITE, lw=1.0, zorder=7))
    ax.text(cb_w/2 + bk_w/2, rl_h + bk_h*0.6,
            "ACME\nNUT", color=ANNO, fontsize=5, ha="center", va="center", **FONT)

    # Leadscrew
    ls_y0 = rl_h + bk_h*0.6
    ls_x0 = cb_w/2 + bk_w
    ax.add_patch(Rectangle((ls_x0, ls_y0 - 8), 200, 16,
                           fc=RAIL, ec=WHITE, lw=1.0, zorder=6))
    # Thread marks
    for tx in np.arange(ls_x0+10, ls_x0+200, 8):
        ax.plot([tx, tx+4], [ls_y0-8, ls_y0+8], color=BG, lw=0.7, zorder=7)
    ax.text(ls_x0 + 100, ls_y0 + 30, "3/4\"-6 ACME LEADSCREW",
            color=RAIL, fontsize=6, ha="center", **FONT)

    # Handwheel (simplified)
    hw_cx = ls_x0 + 220; hw_cy = ls_y0
    ax.add_patch(Circle((hw_cx, hw_cy), 55, fc=STRUCT, ec=WHITE, lw=1.5,
                        alpha=0.8, zorder=6))
    ax.add_patch(Circle((hw_cx, hw_cy), 8, fc=BG, ec=WHITE, lw=0.8, zorder=7))
    for ang_d in range(0, 360, 45):
        ang_r = np.radians(ang_d)
        ax.plot([hw_cx + 10*np.cos(ang_r), hw_cx + 50*np.cos(ang_r)],
                [hw_cy + 10*np.sin(ang_r), hw_cy + 50*np.sin(ang_r)],
                color=WHITE, lw=1.0, zorder=7)
    ax.text(hw_cx, hw_cy - 75, "8\" HANDWHEEL", color=DIM, fontsize=6,
            ha="center", **FONT)

    leader(ax, cb_w/2+bk_w/2, rl_h+bk_h, cb_w/2+bk_w/2, rl_h+bk_h+80,
           "CORNER\nBRACKET\n(L-PLATE)", color=STRUCT2, ha="center",
           arrow_style="-|>", font=FONT)

    ax.text(200, 370, "CORNER CARRIAGE BRACKET ASSEMBLY\n(ONE PER CORNER — 4 TOTAL)",
            color=WHITE, fontsize=8, ha="center", va="bottom", **FONT)
    ax.text(200, -100,
            "EACH CORNER: HGH20CA ×2  +  L-BRACKET  +  ACME NUT  +  3/4\"-6 LEADSCREW  +  HANDWHEEL",
            color=DIM, fontsize=6, ha="center", **FONT)

    # ── TR: HGR20 + HGH20CA cross-section ────────────────────────────────────
    ax = ax_rail
    ax.set_xlim(-200, 400); ax.set_ylim(-150, 350); ax.set_aspect("equal")

    rl_w = 44; rl_h = 30
    ax.add_patch(FancyBboxPatch((-rl_w/2, 0), rl_w, rl_h,
                               boxstyle="round,pad=2",
                               fc=RAIL, ec=WHITE, lw=1.5, zorder=3))
    for hx in [-16, 16]:
        ax.add_patch(Circle((hx, rl_h/2), 4.5, fc=BG, ec=WHITE, lw=0.8, zorder=4))
    for rx in [-12, 12]:
        ax.add_patch(Circle((rx, rl_h), 5, fc=BG, ec=WHITE, lw=0.7, zorder=4))

    cb_w = 63; cb_h = 55
    ax.add_patch(Rectangle((-cb_w/2, rl_h-5), cb_w, cb_h,
                           fc=MECH, ec=WHITE, lw=1.5, zorder=5))
    for cx_, cy_ in [(-22, rl_h+15), (22, rl_h+15), (-22, rl_h+38), (22, rl_h+38)]:
        ax.add_patch(Circle((cx_, cy_), 4, fc=BG, ec=WHITE, lw=0.7, zorder=6))

    draw_dim_h(ax, -rl_w/2, rl_w/2, -50, f"{rl_w}mm",
               offset=15, color=DIM, above=False, font=FONT)
    draw_dim_h(ax, -cb_w/2, cb_w/2, rl_h+cb_h+40, f"{cb_w}mm",
               offset=15, color=DIM, font=FONT)
    draw_dim_v(ax, cb_w/2+60, rl_h, rl_h+cb_h, f"{cb_h}mm",
               offset=15, color=MECH, right=True, font=FONT)

    ax.text(0, rl_h+cb_h+120, "RAIL + CARRIAGE CROSS-SECTION\nHIWIN HGR20  +  HGH20CA",
            color=WHITE, fontsize=7.5, ha="center", va="bottom", **FONT)
    ax.text(0, -90,
            "LOAD: 9.7 kN dynamic  ·  4 RAILS  ·  8 CARRIAGES (2 per rail)",
            color=DIM, fontsize=6.5, ha="center", **FONT)
    ax.text(-80, rl_h/2, "HGR20\nRAIL", color=BG, fontsize=6.5,
            ha="center", va="center", rotation=90, **FONT)
    ax.text(0, rl_h+cb_h/2, "HGH20CA\nCARRIAGE", color=BG, fontsize=6.5,
            ha="center", va="center", **FONT)

    # ── BL: Universal joint / rod-end bearing detail ──────────────────────────
    ax = ax_joint
    ax.set_xlim(-200, 500); ax.set_ylim(-200, 280); ax.set_aspect("equal")

    # Bracket end
    bm_w = 100; bm_h = 80
    ax.add_patch(Rectangle((0, 0), bm_w, bm_h, fc=STRUCT2, ec=WHITE, lw=1.5, zorder=3))
    ax.add_patch(Rectangle((10, 10), bm_w-20, bm_h-20, fc=BG, ec="none", zorder=4))
    ax.text(bm_w/2, bm_h/2, "CORNER\nBRACKET", color=DIM, fontsize=5.5,
            ha="center", va="center", **FONT)

    # Rod-end bearing housing
    rod_cx = bm_w + 45
    rod_cy = bm_h / 2
    ax.add_patch(Circle((rod_cx, rod_cy), 30, fc=RAIL, ec=WHITE, lw=1.5, zorder=5))
    ax.add_patch(Circle((rod_cx, rod_cy), 18, fc=MECH, ec=WHITE, lw=1.0, zorder=6))
    ax.add_patch(Circle((rod_cx, rod_cy), 10, fc=BG, ec=WHITE, lw=0.8, zorder=7))
    # Outer race
    ax.add_patch(Circle((rod_cx, rod_cy), 25, fc="none", ec=WHITE, lw=0.5,
                        linestyle="--", zorder=6))

    # Connecting arm to film frame
    ff_w = 130
    ax.add_patch(Rectangle((rod_cx+30, rod_cy-15), ff_w, 30,
                           fc=ANNO, ec=WHITE, lw=1.0, zorder=5, alpha=0.8))
    ax.add_patch(Circle((rod_cx+30+25, rod_cy), 18, fc=BG, ec=WHITE, lw=1.0, zorder=6))
    ax.add_patch(Circle((rod_cx+30+25, rod_cy), 10, fc=MECH, ec=WHITE, lw=0.8, zorder=7))
    ax.text(rod_cx+30+25, rod_cy, "25mm\nPIN", color=DIM, fontsize=4.5,
            ha="center", va="center", **FONT)

    leader(ax, rod_cx, rod_cy+30, rod_cx - 60, rod_cy + 130,
           "ROD-END SPHERICAL\nBEARING (GIR25-DO\nor equiv.)\n±45° ANY AXIS", color=MECH, ha="center",
           arrow_style="-|>", font=FONT)

    # Annotation of freedom axes
    for angle_d in [0, 45, -45]:
        angle_r = np.radians(angle_d)
        ax.annotate("", xy=(rod_cx + 35*np.cos(angle_r), rod_cy + 35*np.sin(angle_r)),
                    xytext=(rod_cx, rod_cy),
                    arrowprops=dict(arrowstyle="-|>", color=C_T2, lw=0.8,
                                   mutation_scale=5), zorder=8)

    draw_dim_h(ax, rod_cx-30, rod_cx+30, -80, "60mm",
               offset=15, color=DIM, above=False, font=FONT)
    ax.text(200, 240, "CORNER JOINT DETAIL — CROSS-SLIDE TO FILM FRAME\nROD-END (angular freedom) + 2-AXIS X-Z CROSS-SLIDE (translation)",
            color=WHITE, fontsize=7.5, ha="center", va="bottom", **FONT)
    ax.text(200, -100,
            "OPTION A: rod-end gives ±45° any axis; the cross-slide absorbs the rigid-rotation arc travel",
            color=DIM, fontsize=6.5, ha="center", **FONT)

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

    ax.text(280, 310, "ACM BACKING PANEL (OPTION A)\nSINGLE RIGID SHEET — FIXED SIZE, NO HINGE",
            color=WHITE, fontsize=7.5, ha="center", va="bottom", **FONT)
    ax.text(280, -95,
            "PANEL: DIBOND 4mm  ·  the plane never grows, so no folding two-panel system is needed",
            color=DIM, fontsize=6.5, ha="center", **FONT)

    fig.text(0.5, 0.97, "SHEET 3 — FRAME & HARDWARE DETAILS  (4-CORNER INDEPENDENT DESIGN)",
             color=WHITE, fontsize=11, ha="center", fontweight="bold", **FONT)

    # Title block (full-figure overlay for multi-subplot sheet)
    ax_tb = fig.add_axes([0, 0, 1, 1], facecolor="none")
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 3 OF 6",
                drawing_title="MOVEABLE FILM PLANE (4-CORNER)",
                subtitle="Frame & hardware details — 4-corner design",
                scale_note="As noted",
                doc_id="TBS-FM01 · Film Plane Mechanism")

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet3.png", dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet3.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 4 — MOVEMENT SPECIFICATION TABLE & BOM (4-corner design)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet4():
    fig, ax = plt.subplots(figsize=(16, 13))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis("off")

    ax.text(0.5, 0.968, "SHEET 4 — MOVEMENT SPECIFICATION",
            transform=ax.transAxes, color=WHITE, fontsize=13, ha="center",
            fontweight="bold", **FONT)
    ax.text(0.5, 0.948, f"TBS-001  ·  MOVEABLE FILM PLANE (4-CORNER)  ·  RAILS: X={RAIL_X_L}–{RAIL_X_R}mm  SPAN={RAIL_X_R-RAIL_X_L}mm  MAX SWING={MAX_SWING_DEG:.1f}deg",
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
    ax.text(0.05, 0.933, "TABLE 1 — MOVEMENT AXES  (4-CORNER INDEPENDENT DESIGN)",
            transform=ax.transAxes, color=DIM, fontsize=8, fontweight="bold", **FONT)

    axes_headers = ["AXIS", "DESCRIPTION", "CORNERS\nCONTROLLED", "MAX TRAVEL", "ACTUATOR", "LOCK"]
    axes_rows = [
        ["TILT (top)",    "Both top corners move equally",      "TL + TR together", f"0–{FP_Y}mm", "2× leadscrew — turn both", "2 locking collars"],
        ["TILT (bottom)", "Both bottom corners move equally",   "BL + BR together", f"0–{FP_Y}mm", "2× leadscrew — turn both", "2 locking collars"],
        ["SWING (left)",  "Both left corners move equally",     "TL + BL together", f"0–{FP_Y}mm", "2× leadscrew — turn both", "2 locking collars"],
        ["SWING (right)", "Both right corners move equally",    "TR + BR together", f"0–{FP_Y}mm", "2× leadscrew — turn both", "2 locking collars"],
        ["COMPOUND",      "Limited tilt+swing — plane stays FLAT", "TL, TR, BL, BR", f"0–{FP_Y}mm", "4× leadscrews independently","4 locking collars"],
        ["BACK FOCUS",    "All 4 corners together",             "All",              f"{FP_Y_MIN}–{FP_Y}mm","All 4 leadscrews together", "All 4 locks"],
        ["MAX TILT",      "Top=414mm, Bot=1948mm (axis tilt)",  "TL=TR, BL=BR",     f"{MAX_TILT_DEG:.0f}deg (xslide-lim.)",  "Top+top / Bot+bot",        "All 4 locks"],
        ["MAX SWING",     "Left=125mm, Right=2237mm (axis swing)","TL=BL, TR=BR",    f"{MAX_SWING_DEG:.0f}deg (rail-lim.)", "Left+left / Right+right",  "All 4 locks"],
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
        ("Tilt+Swing",     14.0, 10.0,  "combined — plane stays FLAT"),
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

    # BOM removed — consolidated to master-shopping-list.md §4
    ax.text(0.50, 0.22,
            "Bill of materials: master-shopping-list.md — §4 Film Plane Mechanism",
            transform=ax.transAxes, color=DIM, fontsize=7,
            ha="center", va="center", style="italic", **FONT)

    # Title block
    title_block(ax, "SHEET 4 OF 6",
                drawing_title="MOVEABLE FILM PLANE (4-CORNER)",
                subtitle="Movement specification & BOM",
                scale_note="Not to scale",
                doc_id="TBS-FM01 · Film Plane Mechanism")

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet4.png", dpi=130, bbox_inches="tight", facecolor=BG)
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
    from tbs_drawing import hatch_rect

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
    RAIL_H = 30       # HGR20 rail height
    RAIL_W = 20       # HGR20 rail visible width
    CARRIAGE_H = 28   # HGH20CA carriage height
    CARRIAGE_W = 44   # HGH20CA carriage width
    BRACKET_H = 40    # suspension bracket height
    BRACKET_W = 60    # suspension bracket width
    LBRACKET_H = 50   # corner L-bracket vertical extent
    LBRACKET_W = 40   # corner L-bracket horizontal extent
    LBRACKET_T = 6    # 1/4" aluminum plate
    BEARING_D = 25    # GIR25-DO rod-end bore
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
           f"HGR20 RAIL\n({RAIL_W}×{RAIL_H}mm)",
           color=C_RAIL, fs=5.5, ha="left", va="center",
           arrow_style="-|>", font=FONT)

    # ── HGH20CA Carriage block ───────────────────────────────────────────────
    C_CARR = "#607080"
    ax_a.add_patch(Rectangle(((rail_cx - CARRIAGE_W / 2), (carriage_bot)),
                              (CARRIAGE_W), (CARRIAGE_H),
                              fc=C_CARR, ec=ANNO, lw=1.2, zorder=5))
    leader(ax_a, (rail_cx + CARRIAGE_W / 2), (carriage_bot + CARRIAGE_H / 2),
           (rail_cx + 55), (carriage_bot + CARRIAGE_H / 2 - 10),
           f"HGH20CA\nCARRIAGE\n({CARRIAGE_W}×{CARRIAGE_H}mm)",
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

    # ── Rod-end spherical bearing ────────────────────────────────────────────
    C_BEAR = "#C08040"
    ax_a.add_patch(Circle(((lbk_x + LBRACKET_T / 2), (bearing_cy)),
                           (BEARING_D / 2),
                           fc=C_BEAR, ec=ANNO, lw=1.0, zorder=6))
    ax_a.add_patch(Circle(((lbk_x + LBRACKET_T / 2), (bearing_cy)),
                           (BEARING_D / 4),
                           fc=BG, ec=ANNO, lw=0.8, zorder=7))
    leader(ax_a, (lbk_x - 2), (bearing_cy),
           (-25), (bearing_cy + 15),
           f"GIR25-DO\nROD-END BEARING\n(FREE ROTATION\nFOR TILT/SWING)",
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
        (rail_bot + RAIL_H / 2, "HGR20 RAIL"),
        (carriage_bot + CARRIAGE_H / 2, "CARRIAGE"),
        (bracket_bot + BRACKET_H / 2, "BRACKET"),
        (bearing_cy, "BEARING"),
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
                drawing_title="MOVEABLE FILM PLANE (4-CORNER)",
                subtitle="Muslin clamp detail — cam-lever spring clamp",
                scale_note="MULTIPLE SCALES — SEE INDIVIDUAL PANELS",
                doc_id="TBS-FM01 · Film Plane Mechanism",
                height=0.75)

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet5.png", dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet5.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 6 — SYSTEM SCHEMATIC: Four-corner frame front elevation
#
# View: looking at the film plane from the pinhole side (interior elevation).
# Shows ceiling/floor rail pairs, four corner carriages with leadscrews and
# handwheels, film plane frame with rod-end bearings at each corner.
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

    # ── Corner carriages + leadscrews + handwheels ────────────────────────────
    carr_w = 70
    carr_h = 50
    hw_r = 45         # handwheel radius
    ls_w = 12         # leadscrew width (visual)

    corners = [
        ("TL", RAIL_X_L, FH, "top",    "A"),
        ("TR", RAIL_X_R, FH, "top",    "B"),
        ("BL", RAIL_X_L, 0,  "bottom", "C"),
        ("BR", RAIL_X_R, 0,  "bottom", "D"),
    ]

    for label, cx, rail_z, pos, ls_id in corners:
        if pos == "top":
            cy = rail_z - rail_h - carr_h
            ax.add_patch(Rectangle((cx - carr_w / 2, cy), carr_w, carr_h,
                                    fc=MECH, ec=WHITE, lw=1.2, zorder=6))
            # Leadscrew runs vertically downward from carriage
            ls_top = cy
            ls_bot = cy - 400
            ax.plot([cx, cx], [ls_top, ls_bot], color=RAIL, lw=2.5, zorder=5)
            # Thread marks
            for tz in np.arange(ls_bot + 15, ls_top, 18):
                ax.plot([cx - 6, cx + 6], [tz, tz + 10], color=DIM, lw=0.6, zorder=5)
            # Handwheel at bottom of leadscrew
            hw_cy = ls_bot - hw_r - 5
            ax.add_patch(Circle((cx, hw_cy), hw_r, fc=STRUCT, ec=WHITE,
                                lw=1.2, alpha=0.85, zorder=6))
            ax.add_patch(Circle((cx, hw_cy), 6, fc=BG, ec=WHITE, lw=0.8, zorder=7))
            for ang_d in range(0, 360, 45):
                ang_r = np.radians(ang_d)
                ax.plot([cx + 8 * np.cos(ang_r), cx + (hw_r - 5) * np.cos(ang_r)],
                        [hw_cy + 8 * np.sin(ang_r), hw_cy + (hw_r - 5) * np.sin(ang_r)],
                        color=WHITE, lw=0.8, zorder=7)
            # Handwheel label
            ax.text(cx + hw_r + 30, hw_cy, f"HANDWHEEL {ls_id}",
                    color=DIM, fontsize=5.5, ha="left", va="center", **FONT, zorder=8)
        else:
            cy = rail_h
            ax.add_patch(Rectangle((cx - carr_w / 2, cy), carr_w, carr_h,
                                    fc=MECH, ec=WHITE, lw=1.2, zorder=6))
            # Leadscrew runs vertically upward from carriage
            ls_bot = cy + carr_h
            ls_top = ls_bot + 400
            ax.plot([cx, cx], [ls_bot, ls_top], color=RAIL, lw=2.5, zorder=5)
            for tz in np.arange(ls_bot + 15, ls_top, 18):
                ax.plot([cx - 6, cx + 6], [tz, tz + 10], color=DIM, lw=0.6, zorder=5)
            # Handwheel at top of leadscrew
            hw_cy = ls_top + hw_r + 5
            ax.add_patch(Circle((cx, hw_cy), hw_r, fc=STRUCT, ec=WHITE,
                                lw=1.2, alpha=0.85, zorder=6))
            ax.add_patch(Circle((cx, hw_cy), 6, fc=BG, ec=WHITE, lw=0.8, zorder=7))
            for ang_d in range(0, 360, 45):
                ang_r = np.radians(ang_d)
                ax.plot([cx + 8 * np.cos(ang_r), cx + (hw_r - 5) * np.cos(ang_r)],
                        [hw_cy + 8 * np.sin(ang_r), hw_cy + (hw_r - 5) * np.sin(ang_r)],
                        color=WHITE, lw=0.8, zorder=7)
            ax.text(cx + hw_r + 30, hw_cy, f"HANDWHEEL {ls_id}",
                    color=DIM, fontsize=5.5, ha="left", va="center", **FONT, zorder=8)

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

    # ── Rod-end bearings at each corner of the frame ──────────────────────────
    bearing_r = 22
    bearing_positions = [
        (fp_left, fp_top),    # TL
        (fp_right, fp_top),   # TR
        (fp_left, fp_bot),    # BL
        (fp_right, fp_bot),   # BR
    ]
    for bx, bz in bearing_positions:
        ax.add_patch(Circle((bx, bz), bearing_r, fc=MECH, ec=WHITE,
                            lw=1.0, zorder=9))
        ax.add_patch(Circle((bx, bz), bearing_r * 0.45, fc=BG, ec=WHITE,
                            lw=0.8, zorder=10))

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
            "ROD-END + cross-slide each corner",
            color=MECH, fontsize=7, ha="center", va="center", **FONT, zorder=11)

    # ── Leaders ───────────────────────────────────────────────────────────────
    # Leadscrew leader (from TL leadscrew)
    ls_mid_z = (FH - rail_h - carr_h - 200)
    leader(ax, RAIL_X_L + 10, ls_mid_z,
           RAIL_X_L + 450, ls_mid_z - 200,
           "3/4\"-6 ACME\nLEADSCREW\n(one per corner)",
           color=RAIL, ha="left", fs=6.5, font=FONT)

    # Rod-end bearing leader (from TL bearing)
    leader(ax, fp_left + bearing_r, fp_top - bearing_r,
           fp_left + 450, fp_top - 150,
           "GIR25-DO ROD-END\nSPHERICAL BEARING\n(±45° all axes)",
           color=MECH, ha="left", fs=6.5, font=FONT)

    # Carriage leader (from TR carriage)
    leader(ax, RAIL_X_R + carr_w / 2, FH - rail_h - carr_h / 2,
           RAIL_X_R + 450, FH - rail_h - carr_h / 2 - 300,
           "HGH20CA\nCARRIAGE ×2\n(per corner)",
           color=MECH, ha="left", fs=6.5, font=FONT)

    # Rail leader (from TR ceiling rail)
    leader(ax, RAIL_X_R + rail_len / 2, FH - rail_h / 2,
           RAIL_X_R + 450, FH - 150,
           "HGR20 LINEAR RAIL\n2200mm (into page)",
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
            "4 INDEPENDENT CORNER CARRIAGES  ·  4 LEADSCREWS  ·  4 HANDWHEELS  ·  ROD-END + X-Z CROSS-SLIDE AT EACH CORNER (Option A)",
            color=DIM, fontsize=7, ha="center", **FONT)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 6 OF 6",
                drawing_title="MOVEABLE FILM PLANE (4-CORNER)",
                subtitle="System schematic — four-corner frame front elevation",
                scale_note="Schematic — not to scale",
                doc_id="TBS-FM01 · Film Plane Mechanism",
                height=0.05)

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet6.png", dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet6.png")


# ── Run all sheets ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating film plane mechanism drawings (4-corner design)...")
    sheet1()
    sheet2()
    sheet3()
    sheet4()
    sheet5()
    sheet6()
    print("Done.")
