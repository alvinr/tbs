#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_spray_bar_diagram.py
Spray bar assembly detail for TBS-001 processing tray wash system.

Sheet 1 — Gantry elevation (X-Z section viewed from film plane)
Sheet 2 — Cross section — beam assembly (Yd-Z composite, looking along X)
Sheet 3 — Plan view — walkways & slit positions (X-Yd, looking down)
Sheet 4 — Detail A — beam end (longitudinal section, 2:1)
Sheet 5 — Detail C — wheel attachment (section along axle, 2:1)
Sheet 6 — Detail D — wheel attachment plan (X-Yd, looking down)

Output:
  diagrams/spray-bar-sheet1.png … spray-bar-sheet6.png
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Wedge, Polygon

from tbs_constants import (
    C_OUT, C_CL, C_DIM, C_ALUM,
    C_LEN, C_WID,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_W,
    PROC_TRAY_D, PROC_TRAY_RIM, PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR,
    WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T,
    WALKWAY_LEFT_X, WALKWAY_RIGHT_X, WALKWAY_FAR_YD,
    PROC_OPEN_X_L, PROC_OPEN_X_R, PROC_TRAY_FLOOR_Z_LOW,
    SPRAY_BAR_BEAM, SPRAY_BAR_BEAM_W, SPRAY_BAR_BEAM_H, SPRAY_BAR_BEAM_T, SPRAY_BAR_BORE,
    SPRAY_BAR_WHEEL_DIA, SPRAY_BAR_WHEEL_W, SPRAY_BAR_WHEELS_PER_SIDE, SPRAY_BAR_WHEEL_SP,
    SPRAY_BAR_TRAY_FLOOR, SPRAY_BAR_AXLE_RISE, SPRAY_BAR_BRACKET_DROP,
    SPRAY_BAR_BEAM_BOT_RISE, SPRAY_BAR_BEAM_TOP_RISE,
    SPRAY_BAR_POLY_OD, SPRAY_BAR_POLY_ID,
    SPRAY_BAR_TRAVEL, SPRAY_BAR_HOLE_SP, SPRAY_BAR_N_NOZZLES,
    BV02_X, BV02_Z,
    SPRAY_BAR_SLIT_W,
    DIAGRAMS_DIR,
)
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_notes

# ── Palette ──────────────────────────────────────────────────────────────────
C_BG     = "#F5F5F0"
C_WALL   = "#C0C0C8"
C_GRATE  = "#A0A0A8"
C_TRAY   = "#D8D8D0"
C_ALUM_FILL = "#C8D8E8"
C_BLUE   = "#2979B8"
C_HOSE   = "#6090C0"
C_FRAME  = "#1A1A1A"
C_WATER  = "#80C0E0"
C_WHEEL  = "#606060"
C_NYLON  = "#E8E0D0"
C_OPER   = "#555555"
FONT     = dict(family="monospace")

# ── Gantry carriage geometry (rev10 — low-profile: Ø32 wheels, 40×25 SS RHS) ──
# The carriage rides the RAISED, dual-axis-sloped tray floor.  The detail/section
# sheets are cut at the near/low rim, so the LOCAL floor top sits at the low-corner
# height (PROC_TRAY_FLOOR_Z_LOW = 20mm on the shims); the wheel/axle/beam Z's are
# that floor + the floor-relative rises from tbs_constants.
WHEEL_DIA = SPRAY_BAR_WHEEL_DIA          # 32 (was 50)
WHEEL_WIDTH = SPRAY_BAR_WHEEL_W          # 20
N_WHEELS_PER_SIDE = SPRAY_BAR_WHEELS_PER_SIDE
WHEEL_SPACING_YD = SPRAY_BAR_WHEEL_SP    # 200
TRAY_FLOOR_Z = SPRAY_BAR_TRAY_FLOOR      # 2 — tray sheet thickness
FLOOR_LOCAL = PROC_TRAY_FLOOR_Z_LOW      # 20 — tray floor TOP at the near/low rim (raised on shims)

WHEEL_AXLE_Z = FLOOR_LOCAL + SPRAY_BAR_AXLE_RISE       # 36 — axle CL
BRACKET_DROP = SPRAY_BAR_BRACKET_DROP                  # 7
BEAM_Z_BOT = FLOOR_LOCAL + SPRAY_BAR_BEAM_BOT_RISE     # 29 — beam bottom
BEAM_Z_TOP = FLOOR_LOCAL + SPRAY_BAR_BEAM_TOP_RISE     # 54 — beam top
BEAM_W = SPRAY_BAR_BEAM_W                # 40 — beam width (X)
BEAM_H = SPRAY_BAR_BEAM_H                # 25 — beam height (Z), laid flat
BEAM_T = SPRAY_BAR_BEAM_T                # 3
BEAM_BORE_W = BEAM_W - 2 * BEAM_T        # 34 — bore width
BEAM_BORE_H = BEAM_H - 2 * BEAM_T        # 19 — bore height
BEAM_BORE = BEAM_BORE_W                  # legacy alias

# 3/4" LDPE irrigation poly pipe — SIDE-mounted on the beam's inboard face (no longer housed inside)
POLY_OD = SPRAY_BAR_POLY_OD              # 25
POLY_ID = SPRAY_BAR_POLY_ID              # 19
POLY_WALL = (POLY_OD - POLY_ID) / 2
C_POLY = "#2A2A2A"
C_SS   = "#B8BCC4"                        # 304 stainless RHS fill (cooler than the old alu blue)
N_NOZZLES = SPRAY_BAR_N_NOZZLES   # flat-fan nozzles (=26 today; tbs_constants computes from tray opening / 150mm pitch)
NOZZLE_BODY_W = 10
NOZZLE_BODY_H = 6
C_NOZZLE = "#3B7A3B"

# U-clamp dimensions
UC_T = 3
UC_GAP = 1
C_UCLAMP = "#D0D0D8"
C_BOLT = "#808088"
UC_FLARE = 12

GRATE_Z_BOT = WALKWAY_H - WALKWAY_GRATE_T
GRATE_Z_TOP = WALKWAY_H

# Fold-back end closure
FOLD_EXTEND = 40

BEAM_SPAN = PROC_OPEN_X_R - PROC_OPEN_X_L
WALL_T = 3

# Shared layout constants
POLE_X = (PROC_OPEN_X_L + PROC_OPEN_X_R) / 2
SLIT_WIDTH = SPRAY_BAR_SLIT_W
CARRIAGE_YD_CENTER = 220

TOTAL_SHEETS = 7


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 1 — Gantry Elevation
# X-Z section viewed from film plane (along Yd).
# Centered on beam centerline.  Shows walkway slit, pole, beam, BV-02.
# Horizontal scale 1:18, Vertical scale 1:4.5 (4× vert exaggeration)
# ═════════════════════════════════════════════════════════════════════════════

def draw_sheet1():
    fig = plt.figure(figsize=(10, 12))
    fig.patch.set_facecolor(C_BG)
    ax = fig.add_axes([0.08, 0.05, 0.84, 0.91])
    ax.set_facecolor(C_BG)
    ax.set_aspect(4.0)
    ax.axis("off")

    pole_x = POLE_X
    CUT_X = int(pole_x) + 300
    X_LO = -100
    X_HI = CUT_X + 150
    Z_LO = -50
    PIPE_SKIP = 500
    HBREAK2_Z = 250
    Z_HI = 800
    HBREAK_Z = 600

    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)

    # ── Container floor ──────────────────────────────────────────────────
    ax.plot([X_LO, X_HI], [0, 0], color=C_OUT, lw=2.0, zorder=3)
    ax.add_patch(Rectangle((X_LO, -25), X_HI - X_LO, 25,
                 fc="#E0E0D8", ec=C_OUT, lw=0.8, hatch="...", zorder=1))

    # ── Container side wall (X=0 only; right side cut) ───────────────────
    wall_vis_t = WALL_T * 6
    ax.add_patch(Rectangle((0 - wall_vis_t / 2, Z_LO),
                 wall_vis_t, Z_HI - Z_LO,
                 fc=C_WALL, ec=C_OUT, lw=1.0, hatch="///", zorder=2))
    ax.text(0, Z_HI - 30, "CONTAINER\nWALL (X=0)",
            ha="center", va="top", fontsize=4.5, color=C_DIM, **FONT)

    # ── Processing tray ──────────────────────────────────────────────────
    tray_x_l = PROC_TRAY_X_L
    tray_vis_r = CUT_X

    ax.add_patch(Rectangle((tray_x_l, 0),
                 tray_vis_r - tray_x_l, TRAY_FLOOR_Z,
                 fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))
    rim_w = 4
    ax.add_patch(Rectangle((tray_x_l - rim_w / 2, 0),
                 rim_w, PROC_TRAY_RIM,
                 fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=5))

    ax.text((tray_x_l + pole_x) / 2, TRAY_FLOOR_Z + 13,
            "PROCESSING TRAY (304 SS)", ha="center", va="bottom",
            fontsize=5, color=C_DIM, style="italic", **FONT, zorder=10)

    # ── Left walkway grating (X=170-470) ─────────────────────────────────
    wk_l = WALKWAY_LEFT_X
    wk_r = PROC_OPEN_X_L

    ax.add_patch(Rectangle((wk_l, GRATE_Z_BOT),
                 wk_r - wk_l, WALKWAY_GRATE_T,
                 fc=C_GRATE, ec=C_OUT, lw=1.2, zorder=8))
    ax.text((wk_l + wk_r) / 2, GRATE_Z_TOP + 5,
            "LEFT WK", ha="center", va="bottom",
            fontsize=4.5, color=C_GRATE, fontweight="bold", **FONT, zorder=10)

    # ── Near walkway slit at pole_x ──────────────────────────────────────
    slit_x_l = pole_x - SLIT_WIDTH / 2
    slit_x_r = pole_x + SLIT_WIDTH / 2

    nwk_grate_l = tray_x_l
    nwk_grate_r = CUT_X
    ax.add_patch(Rectangle((nwk_grate_l, GRATE_Z_BOT),
                 slit_x_l - nwk_grate_l, WALKWAY_GRATE_T,
                 fc=C_GRATE, ec=C_OUT, lw=0.5, alpha=0.35, zorder=7.5))
    ax.add_patch(Rectangle((slit_x_r, GRATE_Z_BOT),
                 nwk_grate_r - slit_x_r, WALKWAY_GRATE_T,
                 fc=C_GRATE, ec=C_OUT, lw=0.5, alpha=0.35, zorder=7.5))
    ax.add_patch(Rectangle((slit_x_l, GRATE_Z_BOT),
                 SLIT_WIDTH, WALKWAY_GRATE_T,
                 fc=C_BG, ec=C_FRAME, lw=1.0, zorder=8.5))
    leader(ax, pole_x, GRATE_Z_TOP + 3,
           pole_x - 300, GRATE_Z_TOP + 50,
           f"{SLIT_WIDTH}mm SLIT\n(NEAR WALKWAY\nAT POLE POSITION)",
           fs=5, color=C_FRAME, font=FONT, zorder=15)

    ax.text(pole_x - 500, GRATE_Z_BOT - 5,
            "NEAR WALKWAY (PROJECTED, Yd=0-300)",
            ha="center", va="top", fontsize=4.5, color=C_GRATE,
            style="italic", **FONT, zorder=10)

    # ── Beam / spray bar (left end to cut line) ──────────────────────────
    beam_x_l = PROC_TRAY_X_L + 30
    beam_x_r = PROC_TRAY_X_R - 30
    beam_length = beam_x_r - beam_x_l
    beam_vis_r = CUT_X

    ax.add_patch(Rectangle((beam_x_l, BEAM_Z_BOT),
                 beam_vis_r - beam_x_l, BEAM_H,
                 fc=C_SS, ec=C_FRAME, lw=1.5, zorder=9))
    # SIDE-mounted poly manifold runs along the beam's inboard face — hidden behind
    # the beam in this elevation, so shown as a dashed line at beam mid-height.
    ax.plot([beam_x_l + 20, beam_vis_r], [BEAM_Z_BOT + BEAM_H / 2, BEAM_Z_BOT + BEAM_H / 2],
            color=C_POLY, lw=1.0, ls=(0, (5, 3)), alpha=0.8, zorder=9.3)

    ax.text((beam_x_l + pole_x) / 2, BEAM_Z_TOP + 8,
            f"40×25×3mm 304-SS RHS — {beam_length}mm LONG — SIDE 3/4\" LDPE MANIFOLD + {N_NOZZLES} NOZZLES",
            ha="center", va="bottom", fontsize=5.5, color=C_FRAME,
            fontweight="bold", **FONT, zorder=15)

    # Spray nozzles (irrigation flat-fan, 150mm pitch)
    spray_x_l = PROC_OPEN_X_L
    for i in range(N_NOZZLES):
        frac = (i + 0.5) / N_NOZZLES
        nz_x = spray_x_l + 50 + (beam_vis_r - spray_x_l - 100) * frac
        nz_w, nz_h = 6, 8
        ax.add_patch(Rectangle((nz_x - nz_w / 2, BEAM_Z_BOT - nz_h),
                     nz_w, nz_h,
                     fc=C_NOZZLE, ec=C_FRAME, lw=0.8, zorder=10))
        fan_w = 40
        fan_bot = TRAY_FLOOR_Z + 2
        ax.plot([nz_x, nz_x - fan_w / 2], [BEAM_Z_BOT - nz_h, fan_bot],
                color=C_WATER, lw=0.5, alpha=0.4, zorder=6)
        ax.plot([nz_x, nz_x + fan_w / 2], [BEAM_Z_BOT - nz_h, fan_bot],
                color=C_WATER, lw=0.5, alpha=0.4, zorder=6)
        ax.plot([nz_x, nz_x], [BEAM_Z_BOT - nz_h, fan_bot],
                color=C_WATER, lw=0.5, alpha=0.3, zorder=6)

    # Left end cap
    ax.plot([beam_x_l, beam_x_l], [BEAM_Z_BOT, BEAM_Z_TOP],
            color=C_FRAME, lw=2.0, zorder=9.5)

    # ── Break / cut line (zigzag at CUT_X) ───────────────────────────────
    zz_z_lo = Z_LO
    zz_z_hi = Z_HI - 150
    zz_amp = 20
    zz_n = 18
    zz_zs = np.linspace(zz_z_lo, zz_z_hi, zz_n * 2 + 1)
    zz_xs = [CUT_X + (zz_amp if i % 2 else -zz_amp) for i in range(len(zz_zs))]
    zz_xs[0] = CUT_X
    zz_xs[-1] = CUT_X
    ax.plot(zz_xs, list(zz_zs), color=C_FRAME, lw=1.5, zorder=25)
    ax.text(CUT_X + 40, Z_HI / 2, "CUT", ha="left", va="center",
            fontsize=6, color=C_DIM, rotation=90, **FONT, zorder=25)

    # ── Horizontal break line (zigzag at HBREAK_Z) ──────────────────────
    hzz_xs = np.linspace(X_LO, CUT_X, 41)
    hzz_zs = [HBREAK_Z + (8 if i % 2 else -8) for i in range(len(hzz_xs))]
    hzz_zs[0] = HBREAK_Z
    hzz_zs[-1] = HBREAK_Z
    ax.plot(list(hzz_xs), hzz_zs, color=C_FRAME, lw=1.5, zorder=25)
    ax.text(X_LO + 30, HBREAK_Z + 15, "CUT", ha="left", va="bottom",
            fontsize=6, color=C_DIM, **FONT, zorder=25)

    # ── Second horizontal break (pipe riser compression) ────────────────
    h2zz_xs = np.linspace(X_LO, CUT_X, 41)
    h2zz_zs = [HBREAK2_Z + (8 if i % 2 else -8) for i in range(len(h2zz_xs))]
    h2zz_zs[0] = HBREAK2_Z
    h2zz_zs[-1] = HBREAK2_Z
    ax.plot(list(h2zz_xs), h2zz_zs, color=C_FRAME, lw=1.5, zorder=25)
    ax.text(X_LO + 30, HBREAK2_Z + 15, "CUT", ha="left", va="bottom",
            fontsize=6, color=C_DIM, **FONT, zorder=25)

    # ── Pole through slit down to beam ───────────────────────────────────
    pole_top_z = GRATE_Z_TOP + 890 - PIPE_SKIP
    pole_bot_z = BEAM_Z_TOP + 5

    ax.plot([pole_x, pole_x], [pole_top_z, pole_bot_z],
            color="#8B6914", lw=2.5, zorder=10, solid_capstyle="round")
    ax.plot([pole_x, pole_x], [pole_top_z, pole_bot_z],
            color="#BFA040", lw=1.0, zorder=10.5)

    leader(ax, pole_x + 5, pole_top_z,
           pole_x - 375, pole_top_z + 30,
           "TELESCOPING POLE\n(THROUGH WALKWAY SLIT)",
           fs=4.5, color="#8B6914", font=FONT, zorder=15)

    # ── BV-02 on pinhole wall ────────────────────────────────────────────
    bv_z_real = BV02_Z
    bv_z = BV02_Z - PIPE_SKIP
    bv_size = 30
    pipe_w = 10

    wall_strip_w = 80
    ax.add_patch(Rectangle((BV02_X - wall_strip_w / 2, 0),
                 wall_strip_w, bv_z + bv_size,
                 fc=C_WALL, ec=C_OUT, lw=0.5, alpha=0.2,
                 hatch="///", zorder=10.5))

    for clamp_z in [GRATE_Z_TOP + 60, bv_z - 80]:
        clamp_w = pipe_w + 16
        ax.add_patch(Rectangle((BV02_X - clamp_w / 2, clamp_z - 4),
                     clamp_w, 8,
                     fc="#B0B0B8", ec=C_FRAME, lw=0.8, zorder=11.5))

    ax.add_patch(Rectangle((BV02_X - pipe_w / 2, 0),
                 pipe_w, bv_z,
                 fc=C_BLUE, ec=C_FRAME, lw=0.8, alpha=0.4, zorder=11))

    # BV-02 ball-valve symbol (bowtie inside white circle).
    # Axis aspect is 4.0 (1 X data-unit renders 4x wider than 1 Z data-unit), so
    # to make the symbol appear round/symmetric ON SCREEN every X extent is divided
    # by AR. The P&ID bowtie is drawn spread HORIZONTALLY on screen (the two
    # triangles meet tip-to-tip at center) so it reads as a ball valve regardless
    # of the vertical through-pipe.
    # This section axes has px-per-data X=0.285, Z=1.285 (≈1:4.5). To make the
    # P&ID bowtie read as a horizontal ball-valve symbol (not a thin vertical
    # lens) the data extents are sized from a target ON-SCREEN pixel size and
    # divided by those ratios. Drawn ABOVE the telescoping pole (zorder 12).
    PX_X, PX_Z = 0.2848, 1.2847             # px per data-unit on this axes
    CIRC_R_PX = 17.0                        # circle radius on screen (px)
    rx = CIRC_R_PX / PX_X                   # X data radius
    rz = CIRC_R_PX / PX_Z                   # Z data radius
    ax.add_patch(mpatches.Ellipse((BV02_X, bv_z), 2 * rx, 2 * rz,
                 fc="white", ec=C_FRAME, lw=1.5, zorder=14))
    # Horizontal bowtie: bases vertical at left/right circle edge, apexes meet
    # at the center.  Triangle half-extents sized in screen px then converted.
    _bx = (CIRC_R_PX * 0.92) / PX_X         # X data half-width (near circle edge)
    _bh = (CIRC_R_PX * 0.78) / PX_Z         # Z data half-height (base height)
    ax.add_patch(mpatches.Polygon([(BV02_X - _bx, bv_z - _bh),
                                   (BV02_X - _bx, bv_z + _bh),
                                   (BV02_X, bv_z)],
                                  fc=C_BLUE, ec=C_BLUE, zorder=15))
    ax.add_patch(mpatches.Polygon([(BV02_X + _bx, bv_z - _bh),
                                   (BV02_X + _bx, bv_z + _bh),
                                   (BV02_X, bv_z)],
                                  fc=C_BLUE, ec=C_BLUE, zorder=15))

    leader(ax, BV02_X - 30, bv_z + 35,
           BV02_X - 375, bv_z + 80,
           f"BV-02 @ Z={int(bv_z_real)}mm\n(1/2\" BALL VALVE)\nWAIST HEIGHT",
           fs=5.5, color=C_BLUE, font=FONT, zorder=15)

    # ── Flex hose from BV-02 to beam center feed ─────────────────────────
    hose_start_x = BV02_X
    hose_start_z = bv_z - bv_size / 2
    hose_end_x = pole_x
    hose_end_z = BEAM_Z_TOP + 5

    n_pts = 100
    ht = np.linspace(0, 1, n_pts)
    P0 = np.array([hose_start_x, hose_start_z])
    P1 = np.array([hose_start_x + 80, hose_start_z - 120])
    P2 = np.array([hose_end_x - 80, hose_end_z + 80])
    P3 = np.array([hose_end_x, hose_end_z])
    hose_xs = (1-ht)**3*P0[0] + 3*(1-ht)**2*ht*P1[0] + 3*(1-ht)*ht**2*P2[0] + ht**3*P3[0]
    hose_zs = (1-ht)**3*P0[1] + 3*(1-ht)**2*ht*P1[1] + 3*(1-ht)*ht**2*P2[1] + ht**3*P3[1]
    envelope = np.clip(np.minimum(ht, 1 - ht) * 4, 0, 1)
    hose_zs += 3.0 * np.sin(np.linspace(0, 14 * np.pi, n_pts)) * envelope

    ax.plot(hose_xs, hose_zs, color=C_HOSE, lw=2.0, alpha=0.7, zorder=11)

    ax.text(BV02_X + 75, bv_z - 60,
            "1/2\" FLEX HOSE\n-> MANIFOLD\n(4m COILED)",
            ha="left", va="top", fontsize=4.5, color=C_HOSE, **FONT, zorder=15)

    # ── Distribution manifold at the ball joint → irrigation feed tubes ──
    man_w, man_h = 50, 12
    ax.add_patch(Rectangle((pole_x - man_w / 2, BEAM_Z_TOP + 2), man_w, man_h,
                 fc="#C0A860", ec=C_FRAME, lw=0.8, zorder=12))
    # irrigation tube stubs fanning along the beam top to barbed feed points
    for dx in (-1400, -900, -450, 450, 900, 1400):
        fxp = pole_x + dx
        if beam_x_l < fxp < beam_vis_r:
            ax.plot([pole_x, fxp], [BEAM_Z_TOP + 8, BEAM_Z_TOP + 3],
                    color=C_HOSE, lw=1.0, alpha=0.8, zorder=11)
            ax.add_patch(Circle((fxp, BEAM_Z_TOP), 4,
                         fc="#3B7A3B", ec=C_FRAME, lw=0.5, zorder=12))
    leader(ax, pole_x + man_w / 2, BEAM_Z_TOP + 8,
           pole_x + 350, BEAM_Z_TOP + 40,
           "MANIFOLD -> 7 IRRIGATION\nFEED TUBES (see Sheet 7)",
           fs=4.5, color="#C0A860", font=FONT, zorder=15)

    # ── Centerline through beam and slit ─────────────────────────────────
    ax.plot([pole_x, pole_x], [Z_LO, Z_HI - 200],
            color=C_CL, lw=0.8, ls=(0, (10, 4, 2, 4)), zorder=1.5)
    ax.text(pole_x - 1, Z_LO, "CL BEAM CENTER",
            ha="center", va="bottom", fontsize=4.5, color=C_CL, **FONT, zorder=2)

    # ── Dimensions ───────────────────────────────────────────────────────
    draw_dim_h(ax, beam_x_l, beam_vis_r, BEAM_Z_BOT - 50,
               f"{beam_length}mm BEAM (CONTINUES →)",
               offset=4, fs=5, font=FONT, above=False)

    draw_dim_v(ax, beam_x_l - 45, 0, GRATE_Z_TOP,
               f"{WALKWAY_H}mm DECK",
               offset=6, fs=5, font=FONT)

    draw_dim_v(ax, CUT_X + 40, TRAY_FLOOR_Z, BEAM_Z_BOT,
               f"{BEAM_Z_BOT - TRAY_FLOOR_Z:.0f}mm\nSPRAY HGT",
               offset=8, fs=4.5, font=FONT, right=True)

    draw_dim_v(ax, BV02_X - 60, 0, bv_z,
               f"{int(bv_z_real)}mm BV-02",
               offset=8, fs=4.5, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────
    notes = [
        "GANTRY ELEVATION — SECTION THROUGH NEAR WALKWAY:",
        f"1. 40×25×3mm 304-SS RHS beam spans {BEAM_SPAN}mm. 3/4\" LDPE poly SIDE-mounted.",
        f"2. {SLIT_WIDTH}mm slit in walkway at beam center X for pole passage.",
        "3. BV-02 on pinhole wall at pinhole centerline, waist height → flex hose",
        "   → manifold at ball joint → 7 irrigation tubes → barbed into the side poly.",
        f"4. {N_NOZZLES}× flat-fan nozzles side-tapped into the poly, spray down-and-in.",
    ]
    draw_notes(ax, notes, X_LO + 155, 520, spacing=14, fs=7, font=FONT, width=1500)

    # ── Person silhouette (with break) ─────────────────────────────────
    PERSON_H = 1780
    HEAD_R = 80
    oper_x = pole_x - 650
    P_FOOT = GRATE_Z_TOP
    # Body below break
    ax.plot([oper_x, oper_x], [P_FOOT, HBREAK_Z - 10],
            color="#2060A0", lw=3.0, zorder=13, solid_capstyle="round")
    # Head + shoulders above break
    head_z = HBREAK_Z + 70
    ax.plot([oper_x, oper_x], [HBREAK_Z + 15, head_z],
            color="#2060A0", lw=3.0, zorder=13, solid_capstyle="round")
    ax.scatter([oper_x], [head_z],
               s=1800, c="#70A8D8", edgecolors="#1A4D80", linewidths=1.0, zorder=14)
    ax.text(oper_x - 30, (P_FOOT + HBREAK_Z) / 2,
            f"{PERSON_H}mm\noperator\n(shoes)",
            ha="right", va="center", fontsize=5, color="#1A4D80", **FONT, zorder=15)

    view_ctr_x = (X_LO + X_HI) / 2
    ax.text(view_ctr_x, Z_HI - 5,
            "GANTRY ELEVATION — VIEW FROM FILM PLANE",
            ha="center", va="top", fontsize=9, color=C_FRAME,
            fontweight="bold", **FONT, zorder=15)
    ax.text(view_ctr_x, Z_HI - 22,
            "(AXES IN mm — 4× VERT EXAG — SECTION THROUGH NEAR WALKWAY)",
            ha="center", va="top", fontsize=5, color=C_DIM,
            **FONT, zorder=15)

    # ── Walkway support risers ───────────────────────────────────────────
    riser_w = 6
    for rx in [wk_l + 30, wk_l + 150, wk_r - 30]:
        ax.add_patch(Rectangle((rx - riser_w / 2, TRAY_FLOOR_Z),
                     riser_w, GRATE_Z_BOT - TRAY_FLOOR_Z,
                     fc="#B0B0B8", ec=C_FRAME, lw=0.5, zorder=7))

    # ── Simplified beam end + carriage indicator ─────────────────────────
    carriage_cx = beam_x_l + 80
    ax.scatter([carriage_cx], [TRAY_FLOOR_Z],
               s=250, c=C_NYLON, edgecolors=C_WHEEL, linewidths=1.5,
               marker='v', zorder=10.5)
    ax.plot([carriage_cx, carriage_cx], [TRAY_FLOOR_Z, BEAM_Z_BOT],
            color=C_FRAME, lw=1.0, ls="--", zorder=10)
    leader(ax, carriage_cx + 10, TRAY_FLOOR_Z - 3,
           carriage_cx + 300, TRAY_FLOOR_Z + 140,
           "CARRIAGE\n(SEE CROSS SECTION)",
           fs=5, color=C_WHEEL, font=FONT, zorder=15)

    # ── Detail A callout ─────────────────────────────────────────────────
    callout_cx = beam_x_l + 40
    callout_cz = (TRAY_FLOOR_Z + BEAM_Z_TOP) / 2
    ax.add_patch(mpatches.Ellipse((callout_cx, callout_cz), 300, 90,
                 fc="none", ec="#CC0000", lw=1.5, ls="--", zorder=20))
    ax.text(callout_cx, BEAM_Z_TOP + 30,
            "DETAIL A", ha="center", va="bottom", fontsize=7, color="#CC0000",
            fontweight="bold", **FONT, zorder=20)

    # ── Title block ──────────────────────────────────────────────────────
    ax_tb = fig.add_axes([0.04, 0.005, 0.92, 0.04])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 1 OF {TOTAL_SHEETS}",
                drawing_title="SPRAY BAR ASSEMBLY",
                subtitle="GANTRY ELEVATION — X-Z SECTION FROM FILM PLANE",
                scale_note="AXES IN mm — 4× VERTICAL EXAGGERATION",
                height=0.7)

    _save(fig, "spray-bar-sheet1")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Cross Section: Beam Assembly
# Yd-Z composite cross section looking along X.
# Uniform 1:1 scale.  Carriage, beam, ball joint, arm tube.
# ═════════════════════════════════════════════════════════════════════════════

def draw_sheet2():
    fig = plt.figure(figsize=(18, 12))
    fig.patch.set_facecolor(C_BG)
    ax2 = fig.add_axes([0.05, 0.08, 0.90, 0.88])
    ax2.set_facecolor(C_BG)
    ax2.set_aspect("equal")
    ax2.axis("off")

    wheel1_yd = CARRIAGE_YD_CENTER - WHEEL_SPACING_YD / 2
    wheel2_yd = CARRIAGE_YD_CENTER + WHEEL_SPACING_YD / 2

    C_YD_LO = -60
    C_YD_HI = 420
    C_Z_LO  = -30
    C_Z_HI  = 210

    ax2.set_xlim(C_YD_LO, C_YD_HI)
    ax2.set_ylim(C_Z_LO, C_Z_HI)

    ax2.text((C_YD_LO + C_YD_HI) / 2, C_Z_HI - 3,
             "CROSS SECTION — BEAM ASSEMBLY",
             ha="center", va="top", fontsize=9, color=C_FRAME,
             fontweight="bold", **FONT, zorder=15)
    ax2.text((C_YD_LO + C_YD_HI) / 2, C_Z_HI - 15,
             "(COMPOSITE — LOOKING ALONG X — AXES IN mm)",
             ha="center", va="top", fontsize=5, color=C_DIM,
             **FONT, zorder=15)

    _bbox_cs = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.85)

    # ── Container pinhole wall (Yd=0) ────────────────────────────────────
    wall_w = 40
    ax2.add_patch(Rectangle((-wall_w, C_Z_LO), wall_w, C_Z_HI - C_Z_LO,
                  fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    ax2.plot([0, 0], [C_Z_LO, C_Z_HI], color=C_OUT, lw=2.0, zorder=3)

    # ── Container floor ──────────────────────────────────────────────────
    ax2.plot([C_YD_LO, C_YD_HI], [0, 0], color=C_OUT, lw=2.0, zorder=3)
    ax2.add_patch(Rectangle((C_YD_LO, -20), C_YD_HI - C_YD_LO, 20,
                  fc="#E0E0D8", ec=C_OUT, lw=0.8, hatch="...", zorder=1))

    # ── Processing tray — WELDED 304-SS PAN, lifted whole on a tapered shim ramp ──
    #   The tray is fabricated as a complete rigid pan (2mm base + lip fully welded),
    #   then the WHOLE pan is lifted and tilted on the HDPE shim ramp so the corner
    #   sump bottom rests on the container floor.  The drainage slope IS the pan tilt
    #   (rim tilts with it) — it is NOT an internal fall built up inside the tray.
    tray_yd_start = PROC_TRAY_YD_NEAR
    shim_top = FLOOR_LOCAL - TRAY_FLOOR_Z                # 18 — shim stack top (pan base sits on it)
    ax2.add_patch(Rectangle((tray_yd_start, 0),
                  C_YD_HI - tray_yd_start, shim_top,
                  fc="#E6E0D2", ec=C_OUT, lw=0.6, hatch="xxx", zorder=3))
    # welded pan: base sheet + up-turned lip (one rigid unit) sitting ON the shim ramp
    ax2.add_patch(Rectangle((tray_yd_start, shim_top),
                  C_YD_HI - tray_yd_start, TRAY_FLOOR_Z,
                  fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=4))
    ax2.add_patch(Rectangle((tray_yd_start - 3, shim_top), 6, FLOOR_LOCAL + PROC_TRAY_RIM - shim_top,
                  fc=C_TRAY, ec=C_OUT, lw=1.2, zorder=5))
    # weld tick at the base↔lip junction
    ax2.add_patch(Circle((tray_yd_start, shim_top + TRAY_FLOOR_Z), 2.6,
                  fc="none", ec="#B03030", lw=1.0, zorder=6))
    ax2.text(340, FLOOR_LOCAL + PROC_TRAY_RIM + 4,
             "WELDED 304-SS PAN (base + lip welded) — lifted whole on the shim ramp",
             ha="center", va="bottom",
             fontsize=6, color=C_DIM, style="italic", **FONT, zorder=10)
    leader(ax2, (tray_yd_start + C_YD_HI) / 2, shim_top / 2,
           (tray_yd_start + C_YD_HI) / 2 + 20, shim_top / 2 - 22,
           "TAPERED HDPE SHIM RAMP\n(tilts the whole pan · dual-axis 1:200)",
           fs=5.2, color=C_DIM, font=FONT, zorder=15)

    # ── Near walkway grating (Yd=0-300) ──────────────────────────────────
    wk_yd_l = 0
    wk_yd_r = WALKWAY_W

    ax2.add_patch(Rectangle((wk_yd_l, GRATE_Z_BOT),
                  wk_yd_r - wk_yd_l, WALKWAY_GRATE_T,
                  fc=C_GRATE, ec=C_OUT, lw=0.8, alpha=0.20, zorder=10))
    for frac in np.linspace(0.08, 0.92, 8):
        mesh_yd = wk_yd_l + (wk_yd_r - wk_yd_l) * frac
        ax2.plot([mesh_yd, mesh_yd], [GRATE_Z_BOT, GRATE_Z_TOP],
                 color="#888888", lw=0.3, alpha=0.25, zorder=10)
    ax2.text((wk_yd_l + wk_yd_r) / 2, GRATE_Z_TOP + 6,
             "NEAR WALKWAY (PROJECTED)", ha="center", va="bottom",
             fontsize=6, color=C_GRATE, style="italic", **FONT, zorder=10)

    # Walkway support bracket (ghost)
    brk_depth_r = 60
    ax2.plot([0, 0], [GRATE_Z_BOT - brk_depth_r, GRATE_Z_BOT],
             color=C_FRAME, lw=0.8, alpha=0.25, zorder=5)
    ax2.plot([0, wk_yd_r], [GRATE_Z_BOT, GRATE_Z_BOT],
             color=C_FRAME, lw=0.6, alpha=0.25, zorder=5)
    ax2.plot([0, wk_yd_r], [GRATE_Z_BOT - brk_depth_r, GRATE_Z_BOT],
             color=C_FRAME, lw=0.5, ls="--", alpha=0.25, zorder=5)

    # ── Wheels (2× Ø50mm nylon) ────────────────────────────────────────
    for w_yd in [wheel1_yd, wheel2_yd]:
        ax2.add_patch(Circle((w_yd, WHEEL_AXLE_Z), WHEEL_DIA / 2,
                     fc=C_NYLON, ec=C_WHEEL, lw=2.0, zorder=6))
        ax2.plot([w_yd - WHEEL_WIDTH / 2, w_yd + WHEEL_WIDTH / 2],
                 [FLOOR_LOCAL, FLOOR_LOCAL],
                 color=C_WHEEL, lw=2.0, zorder=5)

    # ── Axle pin (Ø10mm, runs through wheel bore) ──────────────────
    axle_pin_r_cs = 5
    axle_ext = 3
    for w_yd in [wheel1_yd, wheel2_yd]:
        axle_left = w_yd - WHEEL_WIDTH / 2 - axle_ext
        axle_right = w_yd + WHEEL_WIDTH / 2 + axle_ext
        ax2.add_patch(Rectangle(
            (axle_left, WHEEL_AXLE_Z - axle_pin_r_cs),
            axle_right - axle_left, 2 * axle_pin_r_cs,
            fc="#D0D0D8", ec=C_FRAME, lw=0.8, zorder=6.3))

    leader(ax2, wheel2_yd + WHEEL_WIDTH / 2 + axle_ext,
           WHEEL_AXLE_Z,
           wheel2_yd + WHEEL_DIA / 2 + 25, WHEEL_AXLE_Z - 15,
           "Ø10mm SS\nAXLE PIN",
           fs=6, color=C_DIM, font=FONT, zorder=15)

    leader(ax2, wheel1_yd - WHEEL_DIA / 2, WHEEL_AXLE_Z,
           wheel1_yd - WHEEL_DIA / 2 - 25, WHEEL_AXLE_Z - 15,
           f"Ø{WHEEL_DIA}mm\nNYLON WHEEL",
           fs=6, color=C_WHEEL, font=FONT, zorder=15)

    # ── Carriage plate 2mm above wheel axle ──────────────────────────
    brk_t_c = 5
    plate_bot_z = WHEEL_AXLE_Z + 2
    plate_top_z = plate_bot_z + brk_t_c
    plate_cz = (plate_bot_z + plate_top_z) / 2

    c_beam_l = CARRIAGE_YD_CENTER - BEAM_W / 2
    c_beam_r = CARRIAGE_YD_CENTER + BEAM_W / 2
    notch_l = c_beam_l          # wings extend in to meet the beam faces
    notch_r = c_beam_r

    plate_yd_l = wheel1_yd - 18
    plate_yd_r = wheel2_yd + 18

    # Left plate wing (near walkway side)
    ax2.add_patch(Rectangle((plate_yd_l, plate_bot_z),
                  notch_l - plate_yd_l, brk_t_c,
                  fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=7))
    # Right plate wing (far side)
    ax2.add_patch(Rectangle((notch_r, plate_bot_z),
                  plate_yd_r - notch_r, brk_t_c,
                  fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=7))

    leader(ax2, plate_yd_r, plate_cz,
           plate_yd_r + 35, plate_cz - 12,
           "CARRIAGE PLATE\n(5mm AL, NOTCHED)",
           fs=6, color=C_FRAME, font=FONT, zorder=15)

    # ── Spacer / U-clamp seat height (drawn after U-clamp variables below) ─
    uc_seat_z = BEAM_Z_BOT + BEAM_H / 2 + brk_t_c / 2
    spacer_h = uc_seat_z - plate_top_z

    # ── Axle-retention saddle clamps (curved conduit-style clamps; 2 either
    #    side of each wheel — shown here straddling the axle) ────────────
    axle_pin_r = 5
    sad_ri = axle_pin_r + 1          # 1mm clearance on the Ø10 axle
    sad_t = 2                        # SS strap thickness
    sad_ro = sad_ri + sad_t
    foot_t = 2
    foot_len = 9
    for w_yd in [wheel1_yd, wheel2_yd]:
        # curved hump cradling under the axle
        ax2.add_patch(Wedge((w_yd, WHEEL_AXLE_Z), sad_ro, 180, 360, width=sad_t,
                      fc=C_UCLAMP, ec=C_FRAME, lw=0.9, zorder=7))
        for sign in [-1, 1]:
            # flat foot against the plate underside
            foot_x0 = (w_yd + sad_ro) if sign > 0 else (w_yd - sad_ro - foot_len)
            ax2.add_patch(Rectangle((foot_x0, plate_bot_z - foot_t), foot_len, foot_t,
                          fc=C_UCLAMP, ec=C_FRAME, lw=0.9, zorder=7))
            # bolt through foot + plate (head on top, nut below)
            bolt_yd = w_yd + sign * (sad_ro + foot_len / 2)
            ax2.add_patch(Rectangle((bolt_yd - 1.5, plate_bot_z - foot_t - 3), 3,
                          plate_top_z - (plate_bot_z - foot_t - 3),
                          fc=C_BOLT, ec=C_FRAME, lw=0.4, zorder=11))
            ax2.add_patch(Rectangle((bolt_yd - 3, plate_top_z), 6, 2.5,
                          fc=C_BOLT, ec=C_FRAME, lw=0.5, zorder=11))
            ax2.add_patch(Rectangle((bolt_yd - 2.5, plate_bot_z - foot_t - 3), 5, 3,
                          fc=C_BOLT, ec=C_FRAME, lw=0.5, zorder=11))

    leader(ax2, wheel1_yd - sad_ro, WHEEL_AXLE_Z - sad_t, wheel1_yd - 30,
           WHEEL_AXLE_Z - 18,
           "SS SADDLE CLAMP\n(AXLE RETENTION)",
           fs=6, color=C_BOLT, font=FONT, zorder=15)

    # ── Beam cross-section: 40×25 304-SS RHS with SIDE-mounted poly manifold ──
    ax2.add_patch(Rectangle((c_beam_l, BEAM_Z_BOT), BEAM_W, BEAM_H,
                  fc=C_SS, ec=C_FRAME, lw=2.5, zorder=8))
    ax2.add_patch(Rectangle((CARRIAGE_YD_CENTER - BEAM_BORE_W / 2, BEAM_Z_BOT + BEAM_T),
                  BEAM_BORE_W, BEAM_BORE_H,
                  fc=C_BG, ec=C_FRAME, lw=0.8, zorder=8.5))

    # 3/4" LDPE poly manifold clipped to the beam's INBOARD (tray-side, +Yd) face
    poly_cy = c_beam_r + POLY_OD / 2
    pipe_cz = BEAM_Z_BOT + BEAM_H / 2
    ax2.add_patch(Circle((poly_cy, pipe_cz), POLY_OD / 2,
                 fc=C_POLY, ec=C_FRAME, lw=1.0, alpha=0.8, zorder=8.7))
    ax2.add_patch(Circle((poly_cy, pipe_cz), POLY_ID / 2,
                 fc=C_WATER, ec=C_FRAME, lw=0.5, alpha=0.5, zorder=8.8))
    # pipe clip strap holding the poly to the beam face
    ax2.add_patch(Wedge((poly_cy, pipe_cz), POLY_OD / 2 + 1.6, 300, 60, width=1.6,
                  fc=C_UCLAMP, ec=C_FRAME, lw=0.7, zorder=8.9))
    leader(ax2, poly_cy + POLY_OD / 2, pipe_cz, poly_cy + 34, pipe_cz + 18,
           '3/4" LDPE POLY MANIFOLD\n(SIDE-MOUNTED)',
           fs=5.5, color=C_POLY, font=FONT, zorder=15)

    ax2.text(CARRIAGE_YD_CENTER, BEAM_Z_TOP + 4,
             "40×25×3mm 304-SS RHS\n(laid flat — low profile)", ha="center", va="bottom",
             fontsize=6, color=C_FRAME, fontweight="bold", **FONT, zorder=15)

    # ── Beam clamp: a bottom plate under the beam + a top plate over it, drawn
    #    together by bolts each side with a solid spacer block — sandwiches the
    #    beam (and carriage plate) vertically ──────────────────────────────
    clp_t = 3                                   # clamp plate thickness
    clp_half = BEAM_W / 2 + 12                  # plate Yd half-width (32)
    spacer_w = 8                                # spacer block Yd width
    clamp_bolt_yd = BEAM_W / 2 + 4              # bolt just outside the beam face (24)

    # bottom + top clamp plates
    ax2.add_patch(Rectangle((CARRIAGE_YD_CENTER - clp_half, BEAM_Z_BOT - clp_t),
                  2 * clp_half, clp_t, fc=C_UCLAMP, ec=C_FRAME, lw=1.0, zorder=10))
    ax2.add_patch(Rectangle((CARRIAGE_YD_CENTER - clp_half, BEAM_Z_TOP),
                  2 * clp_half, clp_t, fc=C_UCLAMP, ec=C_FRAME, lw=1.0, zorder=10))

    for sign in [-1, 1]:
        # solid spacer block between the plates, just outside the beam face
        sp_x0 = (CARRIAGE_YD_CENTER + BEAM_W / 2) if sign > 0 \
            else (CARRIAGE_YD_CENTER - BEAM_W / 2 - spacer_w)
        ax2.add_patch(Rectangle((sp_x0, BEAM_Z_BOT), spacer_w, BEAM_H,
                      fc=C_SS, ec=C_FRAME, lw=0.8, zorder=9.5))
        # bolt: COUNTERSUNK flat head flush in the bottom plate (nothing protrudes
        #   below — reclaims grate clearance), tightened by a nut on TOP only
        bolt_yd = CARRIAGE_YD_CENTER + sign * clamp_bolt_yd
        ax2.add_patch(Rectangle((bolt_yd - 2.5, BEAM_Z_BOT - clp_t), 5,
                      (BEAM_Z_TOP + clp_t + 3) - (BEAM_Z_BOT - clp_t),
                      fc=C_BOLT, ec=C_FRAME, lw=0.5, zorder=11))
        # top nut
        ax2.add_patch(Rectangle((bolt_yd - 4, BEAM_Z_TOP + clp_t), 8, 3,
                      fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=11))
        # countersunk flat head, flush in the bottom plate underside (chamfered seat)
        ax2.add_patch(Polygon([(bolt_yd - 4, BEAM_Z_BOT - clp_t),
                               (bolt_yd + 4, BEAM_Z_BOT - clp_t),
                               (bolt_yd + 2.5, BEAM_Z_BOT),
                               (bolt_yd - 2.5, BEAM_Z_BOT)],
                      closed=True, fc=C_BOLT, ec=C_FRAME, lw=0.4, zorder=11))

    leader(ax2, CARRIAGE_YD_CENTER + clp_half, BEAM_Z_BOT - clp_t,
           CARRIAGE_YD_CENTER + clp_half + 20, BEAM_Z_BOT - 24,
           "M6 COUNTERSUNK (FLUSH\nUNDERSIDE — CLEARANCE)",
           fs=4.5, color=C_BOLT, font=FONT, zorder=15)
    leader(ax2, CARRIAGE_YD_CENTER - clp_half, BEAM_Z_TOP + clp_t / 2,
           CARRIAGE_YD_CENTER - clp_half - 22, BEAM_Z_TOP + 12,
           "SS CLAMP PLATES\n(TOP + BOTTOM)\n+ SPACER + BOLTS",
           fs=4.5, color=C_BOLT, font=FONT, zorder=15)

    # Flat-fan nozzle: barbs into the SIDE poly manifold and sprays DOWN-AND-IN over
    #   the tray (no vertical cost — the reason side-mounting lets the beam sit low).
    FITTING_DIA = 8
    nz_barb_y = poly_cy + POLY_OD / 2
    ax2.add_patch(Rectangle((nz_barb_y, pipe_cz - FITTING_DIA / 2), 4, FITTING_DIA,
                  fc=C_NOZZLE, ec=C_FRAME, lw=0.5, zorder=9))
    nz_body_y = nz_barb_y + 4
    nz_tip_z = pipe_cz - NOZZLE_BODY_W          # tip drops below the poly
    ax2.add_patch(Rectangle((nz_body_y, nz_tip_z), NOZZLE_BODY_H, pipe_cz - nz_tip_z,
                  fc=C_NOZZLE, ec=C_FRAME, lw=1.0, zorder=9.2))
    # down-and-in flat-fan spray toward the tray floor
    for dyd in (-40, 10):
        ax2.plot([nz_body_y + NOZZLE_BODY_H / 2, nz_body_y + NOZZLE_BODY_H / 2 + dyd],
                 [nz_tip_z, FLOOR_LOCAL + 2],
                 color=C_WATER, lw=0.8, alpha=0.5, zorder=9.3)
    leader(ax2, nz_barb_y + 2, pipe_cz, nz_barb_y + 30, pipe_cz - 20,
           f"FLAT-FAN NOZZLE ×{N_NOZZLES}\n(SIDE-TAP BARB)",
           fs=4.5, color=C_NOZZLE, font=FONT, zorder=15)

    # ── Detail C callout ─────────────────────────────────────────────────
    ax2.add_patch(Circle((wheel1_yd, WHEEL_AXLE_Z), WHEEL_DIA / 2 + 8,
                 fc="none", ec="#008800", lw=1.5, ls="--", zorder=20))
    ax2.text(wheel1_yd, WHEEL_AXLE_Z + WHEEL_DIA / 2 + 10,
             "C", ha="center", va="bottom", fontsize=9, color="#008800",
             fontweight="bold", **FONT, zorder=20)

    # ── Ball joint on beam top ──────────────────────────────────────────
    BALL_DIA = 20
    SOCKET_OD = 36
    SOCKET_H = 28
    FLANGE_W = 44
    FLANGE_T = 5
    STUD_DIA = 12
    STUD_EXT = 20
    C_JOINT = "#C8B070"

    bj_yd = CARRIAGE_YD_CENTER
    flange_bot_z = BEAM_Z_TOP
    socket_bot_z = flange_bot_z + FLANGE_T
    ball_ctr_z = socket_bot_z + SOCKET_H / 2 + 2
    socket_top_z = socket_bot_z + SOCKET_H
    stud_top_z = socket_top_z + STUD_EXT

    ax2.add_patch(Rectangle((bj_yd - FLANGE_W / 2, flange_bot_z),
                  FLANGE_W, FLANGE_T,
                  fc="#B0B0B8", ec=C_FRAME, lw=1.2, zorder=7))

    # Flange fastened with self-tapping screws into the beam top wall (no internal
    # access for nuts) — nothing overhangs the ball, so the arm pivots freely
    for scr_yd in (bj_yd - 19.5, bj_yd + 19.5):
        # shank: through the flange + threaded into the beam top wall
        ax2.add_patch(Rectangle((scr_yd - 1.6, BEAM_Z_TOP - BEAM_T), 3.2,
                      FLANGE_T + BEAM_T, fc=C_BOLT, ec=C_FRAME, lw=0.5, zorder=8))
        # pan head on top of the flange
        ax2.add_patch(Rectangle((scr_yd - 3, BEAM_Z_TOP + FLANGE_T), 6, 2.5,
                      fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=9))

    # Socket housing
    ax2.add_patch(Rectangle((bj_yd - SOCKET_OD / 2, socket_bot_z),
                  SOCKET_OD, SOCKET_H,
                  fc=C_JOINT, ec=C_FRAME, lw=1.5, hatch="///", zorder=6))
    bore_r = BALL_DIA / 2 + 1
    ax2.add_patch(Circle((bj_yd, ball_ctr_z), bore_r,
                 fc=C_BG, ec=C_FRAME, lw=0.5, zorder=6.5))

    # Ball
    ax2.add_patch(Circle((bj_yd, ball_ctr_z), BALL_DIA / 2,
                 fc="#E0D8C0", ec=C_FRAME, lw=1.5, zorder=7))

    # Stud
    ax2.add_patch(Rectangle((bj_yd - STUD_DIA / 2, ball_ctr_z),
                  STUD_DIA, stud_top_z - ball_ctr_z,
                  fc="#D0C8B0", ec=C_FRAME, lw=1.0, zorder=7.5))

    # ── Round tube arm ───────────────────────────────────────────────────
    ARM_OD = 25
    ARM_WALL = 2
    ARM_ID = ARM_OD - 2 * ARM_WALL
    arm_base_z_bj = stud_top_z - STUD_EXT + 2
    arm_top_z_bj = arm_base_z_bj + 80

    ax2.add_patch(Rectangle((bj_yd - ARM_OD / 2, arm_base_z_bj),
                  ARM_OD, arm_top_z_bj - arm_base_z_bj,
                  fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=8))
    ax2.add_patch(Rectangle((bj_yd - ARM_ID / 2, arm_base_z_bj),
                  ARM_ID, stud_top_z - arm_base_z_bj,
                  fc="#D0C8B0", ec="none", zorder=8.3))
    ax2.add_patch(Rectangle((bj_yd - ARM_ID / 2, stud_top_z),
                  ARM_ID, arm_top_z_bj - stud_top_z,
                  fc=C_BG, ec=C_FRAME, lw=0.5, zorder=8.5))

    # Pinch bolt
    pinch_z = arm_base_z_bj + 12
    ax2.add_patch(Rectangle((bj_yd - ARM_OD / 2 - 8, pinch_z - 2), 8, 4,
                 fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=9))
    ax2.plot([bj_yd - ARM_OD / 2 - 8, bj_yd - ARM_ID / 2],
             [pinch_z, pinch_z],
             color=C_BOLT, lw=1.5, zorder=9)

    # Continuation arrow
    ax2.annotate("", xy=(bj_yd, arm_top_z_bj + 8),
                 xytext=(bj_yd, arm_top_z_bj),
                 arrowprops=dict(arrowstyle="->", color=C_FRAME, lw=1.5), zorder=12)
    ax2.text(bj_yd - 3, arm_top_z_bj + 5,
             "ARM CONTINUES\nTO TRAY SURFACE",
             ha="right", va="center", fontsize=4.5, color=C_DIM,
             style="italic", **FONT, zorder=15)

    # Movement arcs
    for arc_ang in [-25, 25]:
        ang_rad = np.radians(arc_ang)
        arc_len = 35
        ax2.annotate("",
            xy=(bj_yd + arc_len * np.sin(ang_rad),
                ball_ctr_z + arc_len * np.cos(ang_rad)),
            xytext=(bj_yd, ball_ctr_z),
            arrowprops=dict(arrowstyle="->", color="#AA0000", lw=0.8,
                            connectionstyle=f"arc3,rad={0.3 if arc_ang > 0 else -0.3}"),
            zorder=12)
    ax2.text(bj_yd + SOCKET_OD / 2 + 5, ball_ctr_z + 20,
             "MULTI-AXIS\nARTICULATION",
             ha="left", va="center", fontsize=4.5, color="#AA0000",
             bbox=_bbox_cs, **FONT, zorder=15)

    # ── Water hose zip-tied to arm ───────────────────────────────────────
    hose_od = 16
    hose_ctr_yd = bj_yd + ARM_OD / 2 + hose_od / 2 + 3

    ax2.add_patch(Rectangle((hose_ctr_yd - hose_od / 2, arm_base_z_bj - 5),
                  hose_od, arm_top_z_bj - arm_base_z_bj + 10,
                  fc=C_HOSE, ec=C_BLUE, lw=1.0, alpha=0.6, zorder=7.5))

    for zt_z in [arm_base_z_bj + 15, arm_base_z_bj + 40, arm_base_z_bj + 65]:
        zt_l = bj_yd - ARM_OD / 2 - 4
        zt_r = hose_ctr_yd + hose_od / 2 + 2
        ax2.add_patch(Rectangle((zt_l, zt_z - 1.5), zt_r - zt_l, 3,
                     fc="none", ec="#222222", lw=1.2, zorder=11))
        ax2.add_patch(Rectangle((zt_l - 2, zt_z - 2), 2, 4,
                     fc="#333333", ec="#222222", lw=0.5, zorder=11))

    # ── Labels ───────────────────────────────────────────────────────────
    leader(ax2, bj_yd - SOCKET_OD / 2, ball_ctr_z,
           bj_yd - SOCKET_OD / 2 - 20, ball_ctr_z - 30,
           f"Ø{BALL_DIA}mm FLANGE-BASE\nBALL JOINT",
           fs=5, color=C_JOINT, font=FONT, zorder=20)

    leader(ax2, bj_yd - 19.5, BEAM_Z_TOP + FLANGE_T,
           bj_yd - 19.5 - 24, BEAM_Z_TOP - 6,
           "4× SELF-TAPPING\nSCREW (FLANGE\n-> BEAM TOP WALL)",
           fs=4.5, color=C_BOLT, font=FONT, zorder=20)

    leader(ax2, bj_yd - ARM_OD / 2 - 8, pinch_z,
           bj_yd - 35, pinch_z + 12,
           "M6 PINCH BOLT",
           fs=4.5, color=C_BOLT, font=FONT, zorder=20)

    leader(ax2, bj_yd - ARM_OD / 2, arm_base_z_bj + 50,
           bj_yd - 45, arm_base_z_bj + 62,
           f"Ø{ARM_OD}mm AL TUBE\n(2mm WALL)",
           fs=5, color=C_FRAME, font=FONT, zorder=20)

    leader(ax2, hose_ctr_yd, arm_base_z_bj + 55,
           hose_ctr_yd + 20, arm_base_z_bj + 75,
           "1/2\" FLEX HOSE\n(ZIP-TIED)",
           fs=5, color=C_HOSE, font=FONT, zorder=20)

    # ── Dimensions ───────────────────────────────────────────────────────
    draw_dim_v(ax2, c_beam_l - 10, BEAM_Z_BOT, BEAM_Z_TOP,
               f"{BEAM_W}mm", offset=6, fs=5.5, font=FONT)

    draw_dim_h(ax2, wheel1_yd, wheel2_yd, TRAY_FLOOR_Z + WHEEL_DIA + 8,
               f"{WHEEL_SPACING_YD}mm WHEEL SPACING",
               offset=6, fs=5, font=FONT)

    clearance_c = GRATE_Z_BOT - plate_top_z
    draw_dim_v(ax2, c_beam_r + 10, plate_top_z, GRATE_Z_BOT,
               f"{clearance_c:.0f}mm\nCLR", offset=6, fs=5, font=FONT, right=True)

    draw_dim_v(ax2, c_beam_l - 22, TRAY_FLOOR_Z, BEAM_Z_BOT,
               f"{BEAM_Z_BOT - TRAY_FLOOR_Z:.0f}mm\nSPRAY",
               offset=6, fs=4.5, font=FONT)

    draw_dim_h(ax2, wk_yd_l, wk_yd_r, GRATE_Z_TOP + 18,
               f"{WALKWAY_W}mm WALKWAY", offset=6, fs=5, font=FONT)

    draw_dim_v(ax2, C_YD_HI - 20, 0, GRATE_Z_TOP,
               f"{WALKWAY_H}mm\nDECK HGT",
               offset=6, fs=5, font=FONT, right=True)

    draw_dim_v(ax2, bj_yd - SOCKET_OD / 2 - 10, BEAM_Z_TOP, socket_top_z,
               f"{int(socket_top_z - BEAM_Z_TOP)}mm\nJOINT",
               offset=6, fs=4.5, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────
    cs_notes = [
        "CROSS SECTION (COMPOSITE):",
        f"1. Beam rides on Ø{SPRAY_BAR_WHEEL_DIA}mm nylon wheels; saddle clamps each side retain axle.",
        "2. Clamp plates sandwich beam; underside bolts COUNTERSUNK flush for clearance.",
        "3. Ball joint on plate wing → arm → pole through walkway slit.",
        "4. Water: SIDE poly manifold → side-tap barb → flat-fan nozzle → spray down-and-in.",
        "5. Tray = welded 304-SS pan, lifted whole on the tapered shim ramp (slope = pan tilt).",
    ]
    draw_notes(ax2, cs_notes, C_YD_LO + 10, C_Z_HI - 260, spacing=5,
               fs=7, font=FONT, width=100)

    # ── Title block ──────────────────────────────────────────────────────
    ax_tb = fig.add_axes([0.04, 0.005, 0.92, 0.06])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 2 OF {TOTAL_SHEETS}",
                drawing_title="SPRAY BAR ASSEMBLY",
                subtitle="CROSS SECTION — BEAM ASSEMBLY (COMPOSITE, LOOKING ALONG X)",
                scale_note="AXES IN mm — 1:1",
                height=0.7)

    _save(fig, "spray-bar-sheet2")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 3 — Plan View: Walkways & Slit Positions
# X-Yd looking down.  Shows container outline, walkways, tray, slits.
# ═════════════════════════════════════════════════════════════════════════════

def draw_sheet3():
    fig = plt.figure(figsize=(22, 12))
    fig.patch.set_facecolor(C_BG)
    ax_p = fig.add_axes([0.05, 0.08, 0.90, 0.88])
    ax_p.set_facecolor(C_BG)
    ax_p.set_aspect("equal")
    ax_p.axis("off")

    P_X_LO = -200
    P_X_HI = C_LEN + 200
    P_YD_LO = -200
    P_YD_HI = C_WID + 200

    ax_p.set_xlim(P_X_LO, P_X_HI)
    ax_p.set_ylim(P_YD_LO, P_YD_HI)

    # Title
    ax_p.text(C_LEN / 2, P_YD_HI - 50,
              "PLAN VIEW — WALKWAYS & SLIT POSITIONS",
              ha="center", va="top", fontsize=7, color="#006600",
              fontweight="bold", **FONT, zorder=20)
    ax_p.text(C_LEN / 2, P_YD_HI - 150,
              "(LOOKING DOWN — AXES IN mm)",
              ha="center", va="top", fontsize=5, color=C_DIM,
              **FONT, zorder=20)

    # ── Container outline ────────────────────────────────────────────────
    ax_p.add_patch(Rectangle((0, 0), C_LEN, C_WID,
                   fc="#F0F0EA", ec=C_OUT, lw=2.0, zorder=2))

    # ── Processing tray ──────────────────────────────────────────────────
    ax_p.add_patch(Rectangle((PROC_TRAY_X_L, PROC_TRAY_YD_NEAR),
                   PROC_TRAY_W, PROC_TRAY_D,
                   fc=C_TRAY, ec=C_OUT, lw=1.0, alpha=0.5, zorder=3))
    ax_p.text((PROC_TRAY_X_L + PROC_TRAY_X_R) / 2, C_WID / 3,
              "PROCESSING TRAY",
              ha="center", va="center", fontsize=5, color=C_DIM,
              style="italic", **FONT, zorder=5)

    # ── Near walkway ─────────────────────────────────────────────────────
    ax_p.add_patch(Rectangle((PROC_TRAY_X_L, 0),
                   PROC_TRAY_W, WALKWAY_W,
                   fc=C_GRATE, ec=C_OUT, lw=1.0, alpha=0.4, zorder=4))
    ax_p.text(C_LEN / 2, WALKWAY_W / 2,
              "NEAR WALKWAY", ha="center", va="center",
              fontsize=4.5, color=C_GRATE, fontweight="bold", **FONT, zorder=6)

    # ── Far walkway ──────────────────────────────────────────────────────
    ax_p.add_patch(Rectangle((PROC_TRAY_X_L, WALKWAY_FAR_YD),
                   PROC_TRAY_W, WALKWAY_W,
                   fc=C_GRATE, ec=C_OUT, lw=1.0, alpha=0.4, zorder=4))
    ax_p.text(C_LEN / 2, WALKWAY_FAR_YD + WALKWAY_W / 2,
              "FAR WALKWAY", ha="center", va="center",
              fontsize=4.5, color=C_GRATE, fontweight="bold", **FONT, zorder=6)

    # ── Left walkway ─────────────────────────────────────────────────────
    ax_p.add_patch(Rectangle((WALKWAY_LEFT_X, 0),
                   WALKWAY_W, C_WID,
                   fc=C_GRATE, ec=C_OUT, lw=1.0, alpha=0.4, zorder=4))
    ax_p.text(WALKWAY_LEFT_X + WALKWAY_W / 2, C_WID / 2,
              "LEFT\nWALKWAY", ha="center", va="center",
              fontsize=4, color=C_GRATE, rotation=90, **FONT, zorder=6)

    # ── Right walkway ────────────────────────────────────────────────────
    ax_p.add_patch(Rectangle((WALKWAY_RIGHT_X, 0),
                   WALKWAY_W, C_WID,
                   fc=C_GRATE, ec=C_OUT, lw=1.0, alpha=0.4, zorder=4))
    ax_p.text(WALKWAY_RIGHT_X + WALKWAY_W / 2, C_WID / 2,
              "RIGHT\nWALKWAY", ha="center", va="center",
              fontsize=4, color=C_GRATE, rotation=90, **FONT, zorder=6)

    # ── Slits in near & far walkways ─────────────────────────────────────
    pole_x = POLE_X
    slit_x = pole_x - SLIT_WIDTH / 2

    near_slit_top = PROC_TRAY_YD_NEAR             # 80mm — tray lip
    near_slit_bot = WALKWAY_W                     # 300mm — walkway inner edge
    far_slit_top  = WALKWAY_FAR_YD                # 2062mm — walkway inner edge
    far_slit_bot  = PROC_TRAY_YD_FAR              # 2280mm — tray lip

    ax_p.add_patch(Rectangle((slit_x, near_slit_top),
                   SLIT_WIDTH, near_slit_bot - near_slit_top,
                   fc="#FF4444", ec="#CC0000", lw=1.5, alpha=0.6, zorder=7))
    ax_p.add_patch(Rectangle((slit_x, far_slit_top),
                   SLIT_WIDTH, far_slit_bot - far_slit_top,
                   fc="#FF4444", ec="#CC0000", lw=1.5, alpha=0.6, zorder=7))

    leader(ax_p, pole_x, -10,
           pole_x - 500, -220,
           f"{SLIT_WIDTH}mm SLIT @ BEAM CENTER\n(WALKWAY EDGE TO TRAY LIP —\n"
           f"NEAR {near_slit_bot - near_slit_top}mm, FAR {far_slit_bot - far_slit_top}mm)",
           fs=5, color="#CC0000", font=FONT, zorder=20)

    ax_p.plot([pole_x, pole_x], [-5, WALKWAY_W + 5],
              color="#CC0000", lw=0.8, ls="-.", zorder=6.5)
    ax_p.plot([pole_x, pole_x], [WALKWAY_FAR_YD - 5, C_WID + 5],
              color="#CC0000", lw=0.8, ls="-.", zorder=6.5)

    # ── Beam position (example) ──────────────────────────────────────────
    beam_example_yd = PROC_TRAY_YD_NEAR + PROC_TRAY_D / 2
    ax_p.plot([PROC_OPEN_X_L, PROC_OPEN_X_R],
              [beam_example_yd, beam_example_yd],
              color=C_FRAME, lw=1.5, ls="--", zorder=6)
    ax_p.text((PROC_OPEN_X_L + PROC_OPEN_X_R) / 2, beam_example_yd + 90,
              "BEAM (EXAMPLE POSITION)",
              ha="center", va="bottom", fontsize=4.5, color=C_FRAME,
              style="italic", **FONT, zorder=8)

    # Travel arrow
    ax_p.annotate("", xy=(PROC_OPEN_X_L + 400, beam_example_yd + 300),
                  xytext=(PROC_OPEN_X_L + 400, beam_example_yd - 300),
                  arrowprops=dict(arrowstyle="<->", color=C_BLUE, lw=1.0), zorder=8)
    ax_p.text(PROC_OPEN_X_L + 500, beam_example_yd,
              f"TRAVEL\n{SPRAY_BAR_TRAVEL}mm",
              ha="left", va="center", fontsize=4.5, color=C_BLUE, **FONT, zorder=8)

    # ── Key dimensions ───────────────────────────────────────────────────
    draw_dim_h(ax_p, 0, C_LEN, -130,
               f"{C_LEN}mm CONTAINER", offset=10, fs=5, font=FONT)
    draw_dim_v(ax_p, -100, 0, C_WID,
               f"{C_WID}mm", offset=10, fs=5, font=FONT)

    # ── Pinhole wall label ───────────────────────────────────────────────
    ax_p.text(C_LEN / 2, -30,
              "PINHOLE WALL (Yd=0)", ha="center", va="top",
              fontsize=4, color=C_DIM, style="italic", **FONT, zorder=5)

    # ── Title block ──────────────────────────────────────────────────────
    ax_tb = fig.add_axes([0.04, 0.005, 0.92, 0.06])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 3 OF {TOTAL_SHEETS}",
                drawing_title="SPRAY BAR ASSEMBLY",
                subtitle="PLAN VIEW — WALKWAYS & SLIT POSITIONS",
                scale_note="AXES IN mm",
                height=0.7)

    _save(fig, "spray-bar-sheet3")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 4 — Detail A: Beam End
# Longitudinal section through beam end showing fold-back end closure
# with retainer clip on LDPE poly pipe.  Scale 2:1.
# ═════════════════════════════════════════════════════════════════════════════

def draw_sheet4():
    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor(C_BG)
    ax_a = fig.add_axes([0.05, 0.08, 0.90, 0.88])
    ax_a.set_facecolor(C_BG)
    ax_a.set_aspect("equal")
    ax_a.axis("off")

    poly_od_h = POLY_OD / 2        # 12.5
    poly_id_h = POLY_ID / 2        # 9.5
    beam_half = BEAM_W / 2         # 20
    bore_half = BEAM_BORE / 2      # 17
    CLIP_GAP = 3                                   # poly-to-beam pipe-clip gap
    BOFF = poly_od_h + CLIP_GAP + beam_half        # 35.5 — beam shifted OFF the poly:
    #   the poly + fold-back closure stay put; the beam rides above so the poly is
    #   clipped to its OUTSIDE face (rev10 — poly no longer housed inside the bore).

    beam_end_x = 0
    pipe_past = FOLD_EXTEND         # pipe extends 40mm past beam end

    # Fold geometry — pipe folds downward beneath main run
    bend_inner_r = 8                # inner void radius at fold apex
    bend_center_r = bend_inner_r + poly_od_h  # pipe centerline bend radius
    fold_offset = 2 * bend_center_r  # center-to-center between main and return leg
    fold_leg_y = -fold_offset       # center Y of folded-back leg
    fold_apex_x = beam_end_x - pipe_past
    fold_leg_len = pipe_past - bend_center_r  # straight portion of return leg

    # Pre-compute taper point for view limits
    _clip_x_pre = (fold_apex_x + fold_leg_len - 5
                   if fold_leg_len > 10 else beam_end_x - 10)
    _taper_x_pre = _clip_x_pre - 10 / 2 - 22

    d_xl = _taper_x_pre - 20
    d_xr = 55
    d_yb = fold_leg_y - poly_od_h - 18
    d_yt = BOFF + beam_half + 8
    ax_a.set_xlim(d_xl, d_xr)
    ax_a.set_ylim(d_yb, d_yt)

    ax_a.text((d_xl + d_xr) / 2, d_yt - 1,
              "DETAIL A — BEAM END",
              ha="center", va="top", fontsize=8, color="#CC0000",
              fontweight="bold", **FONT, zorder=20)
    ax_a.text((d_xl + d_xr) / 2, d_yt - 5,
              "(LONGITUDINAL SECTION — SCALE 2:1)",
              ha="center", va="top", fontsize=5, color=C_DIM,
              **FONT, zorder=20)

    _bbox_a = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.85)

    # ── SHS top wall (hatched section) — beam shifted UP by BOFF ──────────
    ax_a.add_patch(Rectangle((beam_end_x, BOFF + bore_half), d_xr - beam_end_x, BEAM_T,
                   fc=C_SS, ec=C_FRAME, lw=1.0, hatch="///", zorder=3))
    # ── SHS bottom wall ──────────────────────────────────────────────────
    ax_a.add_patch(Rectangle((beam_end_x, BOFF - beam_half), d_xr - beam_end_x, BEAM_T,
                   fc=C_SS, ec=C_FRAME, lw=1.0, hatch="///", zorder=3))

    # ── Open beam end face ───────────────────────────────────────────────
    ax_a.plot([beam_end_x, beam_end_x], [BOFF - beam_half, BOFF + beam_half],
              color=C_FRAME, lw=1.5, zorder=5)

    # ── Hollow bore of the SS RHS (poly no longer inside) ─────────────────
    ax_a.add_patch(Rectangle((beam_end_x, BOFF - bore_half), d_xr - beam_end_x, BEAM_BORE,
                   fc=C_BG, ec="none", zorder=3.5))

    # ── Pipe clip: strap from the beam's lower face down around the poly ───
    ax_a.add_patch(Rectangle((beam_end_x + 26, poly_od_h), 9,
                             (BOFF - beam_half) - poly_od_h,
                   fc=C_UCLAMP, ec=C_FRAME, lw=0.8, zorder=3.6))

    # ── Retainer clip position ──────────────────────────────────────────
    fold_leg_left = fold_apex_x + fold_leg_len
    clip_x = fold_leg_left - 5 if fold_leg_len > 10 else beam_end_x - 10
    clip_w = 10
    clip_left_x = clip_x - clip_w / 2
    clip_right_x = clip_x + clip_w / 2
    clip_span_top = poly_od_h + 3
    clip_span_bot = fold_leg_y - poly_od_h - 3
    clip_t = 2.5

    # ── Taper geometry — outside edges converge to a point left of clip ──
    taper_len = 22
    taper_x = clip_left_x - taper_len
    taper_y = fold_leg_y / 2

    # ── Main pipe — parallel from clip left to right edge ────────────────
    ax_a.add_patch(Rectangle((clip_left_x, poly_id_h),
                   d_xr - clip_left_x, POLY_WALL,
                   fc="#404040", ec=C_FRAME, lw=0.6, hatch="...", zorder=4))
    ax_a.add_patch(Rectangle((clip_left_x, -poly_od_h),
                   d_xr - clip_left_x, POLY_WALL,
                   fc="#404040", ec=C_FRAME, lw=0.6, hatch="...", zorder=4))
    ax_a.add_patch(Rectangle((beam_end_x + 2, -poly_id_h),
                   d_xr - beam_end_x - 2, POLY_ID,
                   fc=C_WATER, ec="none", alpha=0.25, zorder=3.8))

    # ── Fold-back leg — parallel through clip ────────────────────────────
    ax_a.add_patch(Rectangle((clip_left_x, fold_leg_y + poly_id_h),
                   clip_right_x - clip_left_x, POLY_WALL,
                   fc="#404040", ec=C_FRAME, lw=0.6, hatch="...", zorder=4))
    ax_a.add_patch(Rectangle((clip_left_x, fold_leg_y - poly_od_h),
                   clip_right_x - clip_left_x, POLY_WALL,
                   fc="#404040", ec=C_FRAME, lw=0.6, hatch="...", zorder=4))
    ax_a.add_patch(Rectangle((clip_left_x, fold_leg_y - poly_id_h),
                   clip_right_x - clip_left_x, POLY_ID,
                   fc=C_WATER, ec="none", alpha=0.20, zorder=3.9))

    # ── Tapered sections — left of clip, converging to point ─────────────
    _pipe_fc = "#404040"
    _pipe_kw = dict(fc=_pipe_fc, ec=C_FRAME, lw=0.6, hatch="...", zorder=4)
    _water_kw = dict(fc=C_WATER, ec="none", alpha=0.20, zorder=3.9)

    # Main pipe top wall taper
    ax_a.add_patch(mpatches.Polygon([
        (clip_left_x, poly_od_h), (clip_left_x, poly_id_h),
        (taper_x, taper_y)], closed=True, **_pipe_kw))
    # Main pipe bottom wall taper
    ax_a.add_patch(mpatches.Polygon([
        (clip_left_x, -poly_id_h), (clip_left_x, -poly_od_h),
        (taper_x, taper_y)], closed=True, **_pipe_kw))
    # Main pipe water taper
    ax_a.add_patch(mpatches.Polygon([
        (clip_left_x, poly_id_h), (clip_left_x, -poly_id_h),
        (taper_x, taper_y)], closed=True, **_water_kw))
    # Fold-back top wall taper
    ax_a.add_patch(mpatches.Polygon([
        (clip_left_x, fold_leg_y + poly_od_h), (clip_left_x, fold_leg_y + poly_id_h),
        (taper_x, taper_y)], closed=True, **_pipe_kw))
    # Fold-back bottom wall taper
    ax_a.add_patch(mpatches.Polygon([
        (clip_left_x, fold_leg_y - poly_id_h), (clip_left_x, fold_leg_y - poly_od_h),
        (taper_x, taper_y)], closed=True, **_pipe_kw))
    # Fold-back water taper
    ax_a.add_patch(mpatches.Polygon([
        (clip_left_x, fold_leg_y + poly_id_h), (clip_left_x, fold_leg_y - poly_id_h),
        (taper_x, taper_y)], closed=True, **_water_kw))

    # ── Retainer clip (holds fold closed) ────────────────────────────────
    clip_verts = [
        (clip_left_x, clip_span_top),
        (clip_right_x, clip_span_top),
        (clip_right_x, clip_span_bot),
        (clip_left_x, clip_span_bot),
        (clip_left_x, clip_span_bot + clip_t),
        (clip_right_x - clip_t, clip_span_bot + clip_t),
        (clip_right_x - clip_t, clip_span_top - clip_t),
        (clip_left_x, clip_span_top - clip_t),
    ]
    ax_a.add_patch(mpatches.Polygon(clip_verts, closed=True,
                   fc="#B0B0B8", ec=C_FRAME, lw=1.2, zorder=6))

    # ── Labels ───────────────────────────────────────────────────────────
    leader(ax_a, beam_end_x + 8, BOFF + bore_half + BEAM_T / 2,
           beam_end_x + 25, d_yt - 6,
           "40×25×3 304-SS RHS\n(HOLLOW — POLY OUTSIDE)",
           fs=5, color=C_FRAME, font=FONT, zorder=20, bbox=_bbox_a)

    leader(ax_a, d_xr - 10, poly_od_h + 2,
           d_xr - 5, d_yt - 3,
           "3/4\" LDPE POLY PIPE",
           fs=5, color="#404040", font=FONT, zorder=20, bbox=_bbox_a)

    leader(ax_a, taper_x + 3, taper_y - 5,
           d_xl + 5, taper_y - 10,
           "180° FOLD-BACK\nEND CLOSURE",
           fs=5, color="#404040", font=FONT, zorder=20, bbox=_bbox_a)

    leader(ax_a, clip_x, clip_span_bot - 1,
           clip_x - 12, d_yb + 3,
           "RETAINER CLIP\n(SS OR NYLON)",
           fs=5, color="#808080", font=FONT, zorder=20, bbox=_bbox_a)

    ax_a.text(d_xr - 8, 0, "WATER",
              ha="center", va="center", fontsize=5, color=C_WATER,
              fontweight="bold", bbox=_bbox_a, **FONT, zorder=15)

    # ── Dimensions ───────────────────────────────────────────────────────
    protrusion = beam_end_x - taper_x
    draw_dim_h(ax_a, taper_x, beam_end_x, d_yb + 5,
               f"{protrusion:.0f}mm\nPROTRUSION",
               offset=2, fs=4.5, font=FONT)

    draw_dim_v(ax_a, d_xr - 3, BOFF - bore_half, BOFF + bore_half,
               f"{BEAM_BORE_W:.0f}mm BORE", offset=1, fs=5, font=FONT, right=True)

    draw_dim_v(ax_a, d_xr - 8, BOFF + bore_half, BOFF + beam_half,
               "3mm\nWALL", offset=2, fs=4.5, font=FONT, right=True)

    draw_dim_v(ax_a, d_xl + 8, -poly_od_h, poly_od_h,
               f"{POLY_OD:.0f}mm\nPOLY OD", offset=3, fs=4.5, font=FONT)

    # ── Title block ──────────────────────────────────────────────────────
    ax_tb = fig.add_axes([0.04, 0.005, 0.92, 0.06])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 4 OF {TOTAL_SHEETS}",
                drawing_title="SPRAY BAR ASSEMBLY",
                subtitle="DETAIL A — BEAM END (FOLD-BACK CLOSURE)",
                scale_note="SCALE 2:1 — AXES IN mm",
                height=0.7)

    _save(fig, "spray-bar-sheet4")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 5 — Detail C: Wheel Attachment Plan (LOOKING DOWN)
# Top-down plan: the carriage plate (notched fork) is in front; each wheel pokes
# up through a slot in its wing (shown as the 20×50 footprint + axle pin); only
# the C-clamp retaining bolt HEADS show (the axle + clamp are below the plate).
# The mirror of Sheet 6 (Detail D, looking UP — wheels whole, in front).
# ═════════════════════════════════════════════════════════════════════════════

def draw_sheet5():
    fig = plt.figure(figsize=(14, 14))
    fig.patch.set_facecolor(C_BG)
    ax_w = fig.add_axes([0.05, 0.06, 0.90, 0.90])
    ax_w.set_facecolor(C_BG)
    ax_w.axis("off")
    ax_w.set_aspect("equal")

    BEAM_SHOW_LEN = 140
    cox = -BEAM_SHOW_LEN + 20             # -120 — carriage center X
    C_X_LO, C_X_HI = -165, 165
    C_YD_LO, C_YD_HI = -150, 150
    ax_w.set_xlim(C_X_LO, C_X_HI)
    ax_w.set_ylim(C_YD_LO, C_YD_HI)

    ax_w.text(0, C_YD_HI - 3, "DETAIL C — WHEEL ATTACHMENT PLAN",
              ha="center", va="top", fontsize=8, color="#008800",
              fontweight="bold", **FONT, zorder=20)
    ax_w.text(0, C_YD_HI - 12, "(LOOKING DOWN FROM ABOVE — AXES IN mm)",
              ha="center", va="top", fontsize=5, color=C_DIM, **FONT, zorder=20)

    C_BOLT_FILL = "#D0D0D8"
    notch_half  = BEAM_W / 2 + 2              # 22 — beam notch half-width (Yd)
    arm_half    = WHEEL_SPACING_YD / 2 + 18   # 118 — wing outer edge (Yd)
    arm_w       = BEAM_W                       # 40 — plate length in X
    wh_x, wh_y  = WHEEL_WIDTH / 2, WHEEL_DIA / 2   # 10, 25 — wheel footprint halves
    sgap        = WHEEL_WIDTH / 2 + 6          # 16 — clamp offset from wheel center

    # ── Beam through the central notch (along X) ──
    ax_w.add_patch(Rectangle((-BEAM_SHOW_LEN, -BEAM_W / 2), 2 * BEAM_SHOW_LEN,
                   BEAM_W, fc=C_SS, ec=C_FRAME, lw=2.0, zorder=5))
    # SIDE-mounted poly manifold running along the beam's inboard (+Yd) face
    ax_w.add_patch(Rectangle((-BEAM_SHOW_LEN, BEAM_W / 2), 2 * BEAM_SHOW_LEN,
                   POLY_OD, fc=C_POLY, ec=C_FRAME, lw=0.6, alpha=0.6, zorder=5.5))
    ax_w.add_patch(Rectangle((-BEAM_SHOW_LEN, BEAM_W / 2 + POLY_WALL), 2 * BEAM_SHOW_LEN,
                   POLY_ID, fc=C_WATER, ec="none", alpha=0.3, zorder=5.6))
    ax_w.plot([-BEAM_SHOW_LEN, BEAM_SHOW_LEN], [0, 0], color=C_FRAME, lw=0.3,
              ls="--", alpha=0.3, zorder=5.9)

    # ── Carriage plate — notched fork (two wings), drawn IN FRONT (we look DOWN
    #    on it). Each wheel pokes UP through a slot in its wing. ──
    for wsgn in (-1, 1):
        y_in, y_out = wsgn * notch_half, wsgn * arm_half
        ax_w.add_patch(Rectangle((cox - arm_w / 2, min(y_in, y_out)), arm_w,
                       abs(y_out - y_in), fc=C_ALUM_FILL, ec=C_FRAME, lw=1.2,
                       hatch="///", zorder=6))
        wyd = wsgn * WHEEL_SPACING_YD / 2
        # slot cut in the wing (clears the plate hatch where the wheel comes through)
        ax_w.add_patch(Rectangle((cox - wh_x, wyd - wh_y), 2 * wh_x, 2 * wh_y,
                       fc=C_BG, ec="none", zorder=6.3))
        # wheel seen through the slot — its 20×50 footprint (tread × Ø50, end-on)
        ax_w.add_patch(Rectangle((cox - wh_x, wyd - wh_y), 2 * wh_x, 2 * wh_y,
                       fc=C_NYLON, ec=C_WHEEL, lw=1.4, hatch="...", alpha=0.85,
                       zorder=6.5))
        # axle pin across the wheel, sticking out each side (same length as Detail D)
        ax_w.add_patch(Rectangle((cox - WHEEL_WIDTH / 2 - 18, wyd - 5),
                       WHEEL_WIDTH + 36, 10,
                       fc="#D0D0D8", ec=C_FRAME, lw=0.5, zorder=6.6))
        # slot edge (the cut in the carriage)
        ax_w.add_patch(Rectangle((cox - wh_x, wyd - wh_y), 2 * wh_x, 2 * wh_y,
                       fc="none", ec="#A06000", lw=1.1, ls=(0, (4, 2)), zorder=6.7))

    # notch callout
    leader(ax_w, cox, notch_half + 1, cox - 35, notch_half + 40,
           "NOTCH\n(BEAM THROUGH FORK)", fs=5, color="#A06000", font=FONT, zorder=20)

    # ── Beam clamp top plate (over the beam) + 4 bolt heads ──
    clp_half = BEAM_W / 2 + 12
    ax_w.add_patch(Rectangle((cox - BEAM_W / 2, -clp_half), BEAM_W, 2 * clp_half,
                   fc=C_UCLAMP, ec=C_FRAME, lw=0.8, alpha=0.55, zorder=6.1))
    for side in (-1, 1):
        for bx_off in (-BEAM_W / 2 + 9, BEAM_W / 2 - 9):
            ax_w.add_patch(Circle((cox + bx_off, side * (BEAM_W / 2 + 4)), 2.5,
                           fc=C_BOLT, ec=C_FRAME, lw=0.5, zorder=8))

    # ── C-clamp retaining bolt HEADS (the axle clamps, seen from above — the
    #    axle + clamp body are BELOW the plate, so only the heads show) ──
    for wsgn in (-1, 1):
        wyd = wsgn * WHEEL_SPACING_YD / 2
        for sx_off in (-sgap, sgap):
            for bolt_off in (-12, 12):
                ax_w.add_patch(Circle((cox + sx_off, wyd + bolt_off), 2.8,
                               fc=C_BOLT_FILL, ec=C_FRAME, lw=0.7, zorder=8))
                ax_w.add_patch(Circle((cox + sx_off, wyd + bolt_off), 1.3,
                               fc="#6E6E78", ec="none", zorder=8.1))

    # ── Labels ───────────────────────────────────────────────────────────
    leader(ax_w, cox + wh_x, WHEEL_SPACING_YD / 2 + wh_y - 4,
           cox + 70, WHEEL_SPACING_YD / 2 + 32,
           f"Ø{WHEEL_DIA} WHEEL THROUGH SLOT\nIN CARRIAGE ({WHEEL_WIDTH}mm TREAD)",
           fs=5, color=C_WHEEL, font=FONT, zorder=20)

    leader(ax_w, cox + sgap, -WHEEL_SPACING_YD / 2 - 12,
           cox + 70, -WHEEL_SPACING_YD / 2 - 34,
           "C-CLAMP RETAINING BOLTS (HEADS)\n2 each side of the wheel —\naxle + clamp are below the plate",
           fs=5, color=C_FRAME, font=FONT, zorder=20)

    leader(ax_w, cox + arm_w / 2, 62, cox + 60, 86,
           "CARRIAGE PLATE\n(5mm AL, NOTCHED FORK)",
           fs=5, color=C_FRAME, font=FONT, zorder=20)

    leader(ax_w, 95, BEAM_W / 2 + POLY_OD, 115, BEAM_W / 2 + POLY_OD + 18,
           "40×25×3mm 304-SS RHS\n+ SIDE 3/4\" LDPE MANIFOLD",
           fs=5, color=C_FRAME, font=FONT, zorder=20)

    # ── Dimensions ───────────────────────────────────────────────────────
    draw_dim_v(ax_w, C_X_LO + 14, -WHEEL_SPACING_YD / 2, WHEEL_SPACING_YD / 2,
               f"{WHEEL_SPACING_YD}mm WHEEL SPACING", offset=3, fs=5, font=FONT)

    # ── Title block ──────────────────────────────────────────────────────
    ax_tb = fig.add_axes([0.04, 0.005, 0.92, 0.045])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 5 OF {TOTAL_SHEETS}",
                drawing_title="SPRAY BAR ASSEMBLY",
                subtitle="DETAIL C — WHEEL ATTACHMENT PLAN (LOOKING DOWN)",
                scale_note="AXES IN mm",
                height=0.7)

    _save(fig, "spray-bar-sheet5")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 6 — Detail D: Wheel Attachment Plan
# X-Yd looking UP from the tray.  Beam, carriage plate, beam clamp plates,
# axle C-clamps, wheels drawn WHOLE (in front, passing through the carriage).
# ═════════════════════════════════════════════════════════════════════════════

def draw_sheet6():
    fig = plt.figure(figsize=(14, 14))
    fig.patch.set_facecolor(C_BG)
    ax_d = fig.add_axes([0.05, 0.06, 0.90, 0.90])
    ax_d.set_facecolor(C_BG)
    ax_d.axis("off")
    ax_d.set_aspect("equal")

    BEAM_SHOW_LEN = 140
    CARRIAGE_OFFSET_X = -BEAM_SHOW_LEN + 20

    D_X_LO = -BEAM_SHOW_LEN - 20
    D_X_HI = BEAM_SHOW_LEN + 20
    D_YD_LO = -WHEEL_SPACING_YD / 2 - 40
    D_YD_HI = WHEEL_SPACING_YD / 2 + 40

    ax_d.set_xlim(D_X_LO, D_X_HI)
    ax_d.set_ylim(D_YD_LO, D_YD_HI)

    ax_d.text(0, D_YD_HI - 2,
              "DETAIL D — WHEEL ATTACHMENT PLAN",
              ha="center", va="top", fontsize=8, color="#AA6600",
              fontweight="bold", **FONT, zorder=20)
    ax_d.text(0, D_YD_HI - 10,
              "(LOOKING UP FROM THE TRAY — AXES IN mm)",
              ha="center", va="top", fontsize=5, color=C_DIM,
              **FONT, zorder=20)

    _bbox_d = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.85)

    # ── Beam (plan view) ─────────────────────────────────────────────────
    ax_d.add_patch(Rectangle((-BEAM_SHOW_LEN, -BEAM_W / 2),
                   2 * BEAM_SHOW_LEN, BEAM_W,
                   fc=C_SS, ec=C_FRAME, lw=2.0, zorder=5))
    ax_d.add_patch(Rectangle((-BEAM_SHOW_LEN, -BEAM_BORE / 2),
                   2 * BEAM_SHOW_LEN, BEAM_BORE,
                   fc=C_BG, ec=C_FRAME, lw=0.5, zorder=5.5))
    # SIDE-mounted poly manifold along the beam's inboard (+Yd) face
    ax_d.add_patch(Rectangle((-BEAM_SHOW_LEN, BEAM_W / 2),
                   2 * BEAM_SHOW_LEN, POLY_OD,
                   fc=C_POLY, ec=C_FRAME, lw=0.6, alpha=0.6, zorder=5.7))
    ax_d.add_patch(Rectangle((-BEAM_SHOW_LEN, BEAM_W / 2 + POLY_WALL),
                   2 * BEAM_SHOW_LEN, POLY_ID,
                   fc=C_WATER, ec="none", alpha=0.3, zorder=5.8))
    for bx in [-BEAM_SHOW_LEN, BEAM_SHOW_LEN]:
        ax_d.plot([bx, bx], [-BEAM_W / 2 - 3, BEAM_W / 2 + 3],
                  color=C_FRAME, lw=1.5, ls=(0, (5, 3)), zorder=6)

    ax_d.plot([-BEAM_SHOW_LEN, BEAM_SHOW_LEN], [0, 0],
              color=C_FRAME, lw=0.3, ls="--", alpha=0.3, zorder=5.9)

    # ── Carriage plate — NOTCHED FORK: two wings either side of the beam ──
    # The beam passes through the central notch; each wing carries one wheel
    # (matches the 3D model's separate Carriage Plate L / R wings).
    arm_half_span = WHEEL_SPACING_YD / 2 + 18    # ±118 — wing outer edge (Yd)
    arm_w_x = BEAM_W                              # 40 — plate length in X (= beam width)
    notch_half = BEAM_W / 2 + 2                    # ±22 — notch half-width (beam + clearance)
    for wsgn in (-1, 1):                          # left + right wing
        y_in, y_out = wsgn * notch_half, wsgn * arm_half_span
        ax_d.add_patch(Rectangle((CARRIAGE_OFFSET_X - arm_w_x / 2, min(y_in, y_out)),
                       arm_w_x, abs(y_out - y_in),
                       fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0,
                       hatch="///", alpha=0.7, zorder=4))
    # notch callout — the beam runs through the fork between the wings
    leader(ax_d, CARRIAGE_OFFSET_X, notch_half + 1,
           CARRIAGE_OFFSET_X - 35, notch_half + 40,
           "NOTCH\n(BEAM THROUGH FORK)",
           fs=4.5, color="#A06000", font=FONT, zorder=20)

    # ── Beam clamp — top plate (over beam) + 4 bolts (sandwich) ─────────
    clp_half_d = BEAM_W / 2 + 12
    clp_x_d = 40                    # clamp X-width (= carriage width)
    ghost_ls = (0, (4, 3))
    ghost_c = "#888888"
    # top clamp plate over the beam at the carriage
    ax_d.add_patch(Rectangle((CARRIAGE_OFFSET_X - clp_x_d / 2, -clp_half_d),
                   clp_x_d, 2 * clp_half_d,
                   fc=C_UCLAMP, ec=C_FRAME, lw=0.8, alpha=0.55, zorder=6))
    # 4 clamp bolts (2 each side of the beam, fore + aft)
    for side in [-1, 1]:
        for bx_off in [-clp_x_d / 2 + 9, clp_x_d / 2 - 9]:
            ax_d.add_patch(Circle((CARRIAGE_OFFSET_X + bx_off,
                                   side * (BEAM_W / 2 + 4)), 2.5,
                         fc=C_BOLT, ec=C_FRAME, lw=0.5, zorder=8))

    leader(ax_d, CARRIAGE_OFFSET_X + clp_x_d / 2, BEAM_W / 2 + 4,
           BEAM_W - 100, BEAM_W / 2 + 30,
           "BEAM CLAMP PLATE\n(TOP + BOTTOM)\n+ 4 BOLTS",
           fs=5, color=C_FRAME, font=FONT, zorder=20)

    # ── Wheels — one per Yd position (2 per carriage) ───────────────────
    for w_sign in [-1, 1]:
        w_yd_ctr = w_sign * WHEEL_SPACING_YD / 2
        wx = CARRIAGE_OFFSET_X
        # axle pin running in X across the wheel + saddle clamps
        ax_d.add_patch(Rectangle((wx - WHEEL_WIDTH / 2 - 18, w_yd_ctr - 5),
                       WHEEL_WIDTH + 36, 10,
                       fc="#D0D0D8", ec=C_FRAME, lw=0.5, zorder=4))
        # WHOLE nylon wheel, drawn IN FRONT of the carriage — this view looks UP
        # from the tray, so the wheel is nearest and clearly passes THROUGH the
        # carriage (no notch shown in this view). Ø50 × 20mm tread.
        ax_d.add_patch(Rectangle((wx - WHEEL_WIDTH / 2, w_yd_ctr - WHEEL_DIA / 2),
                       WHEEL_WIDTH, WHEEL_DIA,
                       fc=C_NYLON, ec=C_WHEEL, lw=1.8, hatch="...",
                       alpha=0.85, zorder=9))

    # ── Axle retention saddle clamps — one each side of each wheel ───────
    sgap_plan = WHEEL_WIDTH / 2 + 6        # 16 — saddle offset from wheel center (X)
    sad_w_plan = 6                          # saddle width along the axle (X)
    sad_half_yd = 17                        # foot half-span (Yd)
    for w_sign in [-1, 1]:
        w_yd_ctr = w_sign * WHEEL_SPACING_YD / 2
        for sx_off in [-sgap_plan, sgap_plan]:
            sx = CARRIAGE_OFFSET_X + sx_off
            ax_d.add_patch(Rectangle((sx - sad_w_plan / 2, w_yd_ctr - sad_half_yd),
                           sad_w_plan, 2 * sad_half_yd,
                           fc=C_UCLAMP, ec=C_FRAME, lw=0.6, alpha=0.6, zorder=7))
            for bolt_off in [-12, 12]:
                ax_d.add_patch(Circle((sx, w_yd_ctr + bolt_off), 2,
                             fc=C_BOLT, ec=C_FRAME, lw=0.4, zorder=8))

    # ── Labels ───────────────────────────────────────────────────────────
    # Wheels
    leader(ax_d, CARRIAGE_OFFSET_X + WHEEL_WIDTH / 2,
           -WHEEL_SPACING_YD / 2,
           D_X_HI - 225, -WHEEL_SPACING_YD / 2 - 10,
           f"Ø{WHEEL_DIA}mm NYLON WHEEL\n({WHEEL_WIDTH}mm WIDE)\n2 PER CARRIAGE",
           fs=5, color=C_WHEEL, font=FONT, zorder=20)

    # Carriage plate
    leader(ax_d, CARRIAGE_OFFSET_X + arm_w_x / 2, 45,
           CARRIAGE_OFFSET_X + 55, 60,
           "CARRIAGE PLATE\n(5mm AL, NOTCHED)",
           fs=5, color=C_FRAME, font=FONT, zorder=20)

    # Axle retention saddle clamp
    bot_right_wx = CARRIAGE_OFFSET_X + 16
    bot_w_yd = -WHEEL_SPACING_YD / 2
    leader(ax_d, bot_right_wx + 3, bot_w_yd - 14,
           bot_right_wx + 50, bot_w_yd + 20,
           "AXLE C-CLAMP\n(2mm SS, 2 EACH SIDE)",
           fs=5, color=C_FRAME, font=FONT, zorder=20)

    # Axle pin
    top_left_wx = CARRIAGE_OFFSET_X
    top_w_yd = WHEEL_SPACING_YD / 2
    leader(ax_d, top_left_wx + WHEEL_WIDTH / 2 + 18, top_w_yd,
           top_left_wx + 60, top_w_yd + 15,
           "Ø10mm SS\nAXLE PIN",
           fs=5, color="#888888", font=FONT, zorder=20)

    # Through-bolts (on axle saddle clamp)
    leader(ax_d, bot_right_wx, bot_w_yd + 12,
           bot_right_wx + 50, bot_w_yd - 20,
           "M5 THROUGH-BOLT\n(2 PER C-CLAMP)",
           fs=5, color=C_BOLT, font=FONT, zorder=20)

    # LDPE poly (side-mounted)
    leader(ax_d, 30, BEAM_W / 2 + POLY_OD / 2,
           60, BEAM_W / 2 + POLY_OD + 15,
           "3/4\" LDPE POLY\n(SIDE MANIFOLD)",
           fs=5, color=C_POLY, font=FONT, zorder=20)

    # Beam
    leader(ax_d, 100, -BEAM_W / 2,
           120, -BEAM_W / 2 - 18,
           "40×25×3mm 304-SS RHS",
           fs=5, color=C_FRAME, font=FONT, zorder=20)

    # ── Dimensions ───────────────────────────────────────────────────────
    draw_dim_v(ax_d, D_X_LO + 12,
               -WHEEL_SPACING_YD / 2, WHEEL_SPACING_YD / 2,
               f"{WHEEL_SPACING_YD}mm WHEEL SPACING",
               offset=3, fs=5, font=FONT)

    # ── Title block ──────────────────────────────────────────────────────
    ax_tb = fig.add_axes([0.04, 0.005, 0.92, 0.045])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 6 OF {TOTAL_SHEETS}",
                drawing_title="SPRAY BAR ASSEMBLY",
                subtitle="DETAIL D — WHEEL ATTACHMENT PLAN (LOOKING UP FROM TRAY)",
                scale_note="AXES IN mm",
                height=0.7)

    _save(fig, "spray-bar-sheet6")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 7 — Detail B: Center Feed & Nozzle Connections
# Two-panel longitudinal section through beam showing:
#   Left:  barbed center feed (flex hose → through beam top → poly pipe)
#   Right: nozzle connection (poly pipe → through beam bottom → spray nozzle)
# Scale 2:1.
# ═════════════════════════════════════════════════════════════════════════════

def draw_sheet7():
    from matplotlib.gridspec import GridSpec

    fig = plt.figure(figsize=(21, 12))
    fig.patch.set_facecolor(C_BG)
    gs = GridSpec(1, 3, figure=fig, width_ratios=[1.15, 0.95, 0.8], wspace=0.16)
    ax_cf = fig.add_subplot(gs[0, 0])
    ax_nz = fig.add_subplot(gs[0, 1])
    ax_pole = fig.add_subplot(gs[0, 2])

    for ax in [ax_cf, ax_nz, ax_pole]:
        ax.set_facecolor(C_BG)
        ax.axis("off")

    _bbox = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.85)
    C_BRASS = "#C0A860"

    # Shared beam / pipe geometry (local Z: beam bottom = 0)
    BEAM = SPRAY_BAR_BEAM           # 40 — beam width (Yd)
    BEAMH = SPRAY_BAR_BEAM_H        # 25 — beam height (Z)
    WALL = SPRAY_BAR_BEAM_T         # 3
    BORE = BEAM - 2 * WALL          # 34
    poly_od_h = POLY_OD / 2         # 12.5
    poly_id_h = POLY_ID / 2         # 9.5
    poly_wall = POLY_WALL           # 3.0

    beam_bot = 0
    beam_top = BEAM                 # 40
    bore_bot = WALL                 # 3
    bore_top = BEAM - WALL          # 37
    poly_ctr = BEAM / 2             # 20
    poly_top = poly_ctr + poly_od_h # 32.5
    poly_bot = poly_ctr - poly_od_h # 7.5
    poly_inner_top = poly_ctr + poly_id_h  # 29.5
    poly_inner_bot = poly_ctr - poly_id_h  # 10.5
    gap_top = bore_top - poly_top   # 4.5 air gap above pipe
    gap_bot = poly_bot - bore_bot   # 4.5 air gap below pipe

    # Barbed fitting dimensions
    BARB_OD = 10            # barbed insert OD
    BARB_LEN = 12           # barb length into pipe
    DRILL_DIA = 12          # drill hole through beam wall
    FITTING_BODY_OD = 14    # threaded body through beam wall
    FITTING_BORE = 10       # internal passage
    HOSE_BARB_OD = 16       # 1/2" hose barb OD
    HOSE_BARB_LEN = 25      # hose barb length
    WASHER_OD = 22           # sealing washer OD
    WASHER_T = 1.5
    HOSE_OD = 19
    HOSE_LEN = 20

    # Nozzle dimensions
    NZ_THREAD_L = 8         # threaded stub below beam
    NZ_BODY_OD = 18         # nozzle body OD
    NZ_BODY_H = 12          # nozzle body height
    NZ_ORIFICE = 3          # orifice width at bottom

    # ─────────────────────────────────────────────────────────────────────
    # LEFT PANEL — CENTER FEED (barbed fitting through beam top)
    # ─────────────────────────────────────────────────────────────────────
    d_xl, d_xr = -50, 50
    d_yb, d_yt = -26, 78
    ax_cf.set_xlim(d_xl, d_xr)
    ax_cf.set_ylim(d_yb, d_yt)

    sec_w = d_xr - d_xl - 10  # section width

    # ── Poly manifold runs along X OUTSIDE the beam; barbed tee taps it from above ──
    # Poly top wall (split around the tee hole)
    ax_cf.add_patch(Rectangle((d_xl + 5, poly_inner_top),
                    -DRILL_DIA / 2 - (d_xl + 5), poly_wall,
                    fc=C_POLY, ec=C_FRAME, lw=0.6, zorder=4))
    ax_cf.add_patch(Rectangle((DRILL_DIA / 2, poly_inner_top),
                    d_xr - 5 - DRILL_DIA / 2, poly_wall,
                    fc=C_POLY, ec=C_FRAME, lw=0.6, zorder=4))
    ax_cf.add_patch(Rectangle((d_xl + 5, poly_bot),
                    sec_w, poly_wall,
                    fc=C_POLY, ec=C_FRAME, lw=0.6, zorder=4))
    ax_cf.add_patch(Rectangle((d_xl + 5, poly_inner_bot),
                    sec_w, POLY_ID,
                    fc=C_WATER, ec="none", alpha=0.15, zorder=3.8))

    # ── Beam: solid SS RHS shifted BELOW the poly (poly clipped to its top face) ──
    beam_top_z = poly_bot - 3                        # 3mm pipe-clip gap under the poly
    beam_bot_z = beam_top_z - BEAMH
    ax_cf.add_patch(Rectangle((d_xl + 5, beam_bot_z), sec_w, BEAMH,
                    fc=C_SS, ec=C_FRAME, lw=1.0, zorder=3))
    ax_cf.add_patch(Rectangle((d_xl + 8, beam_bot_z + WALL), sec_w - 6, BEAMH - 2 * WALL,
                    fc=C_BG, ec=C_FRAME, lw=0.4, zorder=3.1))   # hollow bore
    ax_cf.add_patch(Rectangle((d_xl + 22, beam_top_z), 8, poly_bot - beam_top_z,
                    fc=C_UCLAMP, ec=C_FRAME, lw=0.7, zorder=3.4))   # pipe clip poly→beam

    # Barbed tee body — barbs straight down into the poly (no beam wall to cross)
    body_top = poly_top + 4
    body_bot = poly_inner_top - BARB_LEN
    body_h = body_top - body_bot
    ax_cf.add_patch(Rectangle((-FITTING_BODY_OD / 2, body_bot),
                    FITTING_BODY_OD, body_h,
                    fc=C_BRASS, ec=C_FRAME, lw=1.0, hatch="...", zorder=5))
    ax_cf.add_patch(Rectangle((-FITTING_BORE / 2, body_bot),
                    FITTING_BORE, body_h,
                    fc=C_WATER, ec="none", alpha=0.25, zorder=5.5))

    # Barb ridges (inside poly pipe)
    for i in range(2):
        rz = poly_inner_top - 4 - i * 5
        ax_cf.plot([-FITTING_BODY_OD / 2 - 1.5, -FITTING_BODY_OD / 2],
                   [rz + 2, rz], color=C_FRAME, lw=0.8, zorder=5.5)
        ax_cf.plot([FITTING_BODY_OD / 2, FITTING_BODY_OD / 2 + 1.5],
                   [rz, rz + 2], color=C_FRAME, lw=0.8, zorder=5.5)

    # Hose barb above the tee
    hbarb_bot = body_top
    ax_cf.add_patch(Rectangle((-HOSE_BARB_OD / 2, hbarb_bot),
                    HOSE_BARB_OD, HOSE_BARB_LEN,
                    fc=C_BRASS, ec=C_FRAME, lw=0.8, zorder=6))
    for i in range(3):
        rz = hbarb_bot + 5 + i * 7
        ax_cf.plot([-HOSE_BARB_OD / 2 - 1.5, -HOSE_BARB_OD / 2],
                   [rz + 2, rz], color=C_FRAME, lw=0.8, zorder=6.5)
        ax_cf.plot([HOSE_BARB_OD / 2, HOSE_BARB_OD / 2 + 1.5],
                   [rz, rz + 2], color=C_FRAME, lw=0.8, zorder=6.5)
    ax_cf.add_patch(Rectangle((-FITTING_BORE / 2, hbarb_bot),
                    FITTING_BORE, HOSE_BARB_LEN,
                    fc=C_WATER, ec="none", alpha=0.25, zorder=6.3))

    # Flex hose stub
    hose_bot = hbarb_bot + 3
    hose_top = hbarb_bot + HOSE_BARB_LEN + HOSE_LEN
    ax_cf.add_patch(Rectangle((-HOSE_OD / 2, hose_bot),
                    HOSE_OD, hose_top - hose_bot,
                    fc=C_HOSE, ec=C_BLUE, lw=1.0, alpha=0.5, zorder=5.8))
    for bz in range(int(hose_bot) + 3, int(hose_top) - 2, 5):
        ax_cf.plot([-HOSE_OD / 2, HOSE_OD / 2], [bz, bz + 2],
                   color=C_BLUE, lw=0.4, alpha=0.4, zorder=5.9)

    # Water flow arrows
    arrow_props = dict(arrowstyle="-|>", color=C_WATER, lw=1.5, mutation_scale=12)
    ax_cf.annotate("", xy=(0, poly_inner_top + 1),
                   xytext=(0, hbarb_bot + 3),
                   arrowprops=arrow_props, zorder=8)
    ax_cf.annotate("", xy=(d_xl + 10, poly_ctr),
                   xytext=(-DRILL_DIA / 2 - 3, poly_ctr),
                   arrowprops=arrow_props, zorder=8)
    ax_cf.annotate("", xy=(d_xr - 10, poly_ctr),
                   xytext=(DRILL_DIA / 2 + 3, poly_ctr),
                   arrowprops=arrow_props, zorder=8)

    # Labels
    leader(ax_cf, 0, beam_bot_z + BEAMH / 2,
           d_xl + 6, beam_bot_z + BEAMH / 2 - 3,
           "40×25×3mm\n304-SS RHS",
           fs=5, color=C_FRAME, font=FONT, zorder=20, bbox=_bbox)
    leader(ax_cf, d_xr - 10, poly_top - poly_wall / 2,
           d_xr - 5, poly_ctr + 2,
           f"3/4\" LDPE POLY\nMANIFOLD OD {POLY_OD:.0f}",
           fs=5, color=C_POLY, font=FONT, zorder=20, bbox=_bbox)
    leader(ax_cf, FITTING_BODY_OD / 2 + 2, (poly_top + body_top) / 2,
           d_xr - 5, poly_top + 8,
           "BARBED TEE\n(BRASS, 1/2\" NPT)",
           fs=5, color=C_BRASS, font=FONT, zorder=20, bbox=_bbox)
    leader(ax_cf, HOSE_OD / 2, hose_top - 3,
           d_xr - 5, hose_top,
           "IRRIGATION TUBE\n(FROM MANIFOLD)",
           fs=5, color=C_HOSE, font=FONT, zorder=20, bbox=_bbox)
    ax_cf.text(d_xl + 15, poly_ctr, "WATER", ha="center", va="center",
               fontsize=5, color=C_WATER, fontweight="bold",
               bbox=_bbox, **FONT, zorder=15)

    # Dimensions
    draw_dim_v(ax_cf, d_xl + 8, beam_bot_z, beam_top_z,
               f"{BEAMH}mm\nRHS", offset=2, fs=5, font=FONT)
    draw_dim_v(ax_cf, d_xr - 8, poly_bot, poly_top,
               f"{POLY_OD:.0f}mm\nOD",
               offset=2, fs=4.5, font=FONT, right=True)

    ax_cf.text(0, d_yt - 1, "FEED CONNECTION (TYP. ×7)",
               ha="center", va="top", fontsize=7, color="#CC6600",
               fontweight="bold", **FONT, zorder=20)
    ax_cf.text(0, d_yt - 5, "(BARBED TEE INTO THE SIDE POLY MANIFOLD)",
               ha="center", va="top", fontsize=5, color=C_DIM,
               **FONT, zorder=20)

    # ─────────────────────────────────────────────────────────────────────
    # RIGHT PANEL — NOZZLE CONNECTION (barbed fitting through beam bottom)
    # ─────────────────────────────────────────────────────────────────────
    n_xl, n_xr = -45, 45
    n_yb, n_yt = -35, 64
    ax_nz.set_xlim(n_xl, n_xr)
    ax_nz.set_ylim(n_yb, n_yt)

    nsec_w = n_xr - n_xl - 10

    # ── Poly manifold OUTSIDE the beam; nozzle barbs into it from below ──
    ax_nz.add_patch(Rectangle((n_xl + 5, poly_inner_top),
                    nsec_w, poly_wall,
                    fc=C_POLY, ec=C_FRAME, lw=0.6, zorder=4))
    ax_nz.add_patch(Rectangle((n_xl + 5, poly_bot),
                    -DRILL_DIA / 2 - (n_xl + 5), poly_wall,
                    fc=C_POLY, ec=C_FRAME, lw=0.6, zorder=4))
    ax_nz.add_patch(Rectangle((DRILL_DIA / 2, poly_bot),
                    n_xr - 5 - DRILL_DIA / 2, poly_wall,
                    fc=C_POLY, ec=C_FRAME, lw=0.6, zorder=4))
    ax_nz.add_patch(Rectangle((n_xl + 5, poly_inner_bot),
                    nsec_w, POLY_ID,
                    fc=C_WATER, ec="none", alpha=0.15, zorder=3.8))

    # Beam: solid SS RHS shifted ABOVE the poly (poly clipped to its bottom face)
    beam_bot_z = poly_top + 3                        # 3mm pipe-clip gap over the poly
    ax_nz.add_patch(Rectangle((n_xl + 5, beam_bot_z), nsec_w, BEAMH,
                    fc=C_SS, ec=C_FRAME, lw=1.0, zorder=3))
    ax_nz.add_patch(Rectangle((n_xl + 8, beam_bot_z + WALL), nsec_w - 6, BEAMH - 2 * WALL,
                    fc=C_BG, ec=C_FRAME, lw=0.4, zorder=3.1))   # hollow bore
    ax_nz.add_patch(Rectangle((n_xl + 22, poly_top), 8, beam_bot_z - poly_top,
                    fc=C_UCLAMP, ec=C_FRAME, lw=0.7, zorder=3.4))   # pipe clip poly→beam

    # Barbed saddle-tee — barbs up into the poly bottom; nozzle hangs below
    nz_body_top = poly_inner_bot + BARB_LEN
    nz_body_bot = poly_bot - NZ_THREAD_L
    nz_body_h = nz_body_top - nz_body_bot
    ax_nz.add_patch(Rectangle((-FITTING_BODY_OD / 2, nz_body_bot),
                    FITTING_BODY_OD, nz_body_h,
                    fc=C_BRASS, ec=C_FRAME, lw=1.0, hatch="...", zorder=5))
    ax_nz.add_patch(Rectangle((-FITTING_BORE / 2, nz_body_bot),
                    FITTING_BORE, nz_body_h,
                    fc=C_WATER, ec="none", alpha=0.25, zorder=5.5))

    # Barb ridges (inside poly pipe, pointing up)
    for i in range(2):
        rz = poly_inner_bot + 3 + i * 5
        ax_nz.plot([-FITTING_BODY_OD / 2 - 1.5, -FITTING_BODY_OD / 2],
                   [rz, rz + 2], color=C_FRAME, lw=0.8, zorder=5.5)
        ax_nz.plot([FITTING_BODY_OD / 2, FITTING_BODY_OD / 2 + 1.5],
                   [rz + 2, rz], color=C_FRAME, lw=0.8, zorder=5.5)

    # Irrigation spray nozzle body
    nz_top = nz_body_bot
    nz_bot = nz_top - NZ_BODY_H
    ax_nz.add_patch(Rectangle((-NZ_BODY_OD / 2, nz_bot),
                    NZ_BODY_OD, NZ_BODY_H,
                    fc=C_NOZZLE, ec=C_FRAME, lw=1.2, zorder=6))
    ax_nz.add_patch(Rectangle((-NZ_ORIFICE / 2, nz_bot - 1),
                    NZ_ORIFICE, 1.5,
                    fc=C_WATER, ec=C_FRAME, lw=0.5, zorder=6.5))

    # Spray fan pattern
    fan_half = 20
    fan_drop = 18
    ax_nz.plot([0, -fan_half], [nz_bot - 1, nz_bot - fan_drop],
               color=C_WATER, lw=1.0, alpha=0.5, zorder=6)
    ax_nz.plot([0, fan_half], [nz_bot - 1, nz_bot - fan_drop],
               color=C_WATER, lw=1.0, alpha=0.5, zorder=6)
    ax_nz.plot([0, 0], [nz_bot - 1, nz_bot - fan_drop],
               color=C_WATER, lw=0.6, alpha=0.3, zorder=6)
    ax_nz.plot([0, -fan_half / 2], [nz_bot - 1, nz_bot - fan_drop],
               color=C_WATER, lw=0.6, alpha=0.3, zorder=6)
    ax_nz.plot([0, fan_half / 2], [nz_bot - 1, nz_bot - fan_drop],
               color=C_WATER, lw=0.6, alpha=0.3, zorder=6)

    # Water flow arrows
    ax_nz.annotate("", xy=(0, nz_body_bot + 1),
                   xytext=(0, poly_inner_bot - 1),
                   arrowprops=arrow_props, zorder=8)

    # Labels
    leader(ax_nz, 0, beam_bot_z + BEAMH / 2,
           n_xl + 6, beam_bot_z + BEAMH / 2 + 3,
           "40×25×3mm\n304-SS RHS",
           fs=5, color=C_FRAME, font=FONT, zorder=20, bbox=_bbox)
    leader(ax_nz, n_xr - 10, poly_top - poly_wall / 2,
           n_xr - 5, poly_ctr + 2,
           f"3/4\" LDPE POLY\nMANIFOLD OD {POLY_OD:.0f}",
           fs=5, color=C_POLY, font=FONT, zorder=20, bbox=_bbox)
    leader(ax_nz, FITTING_BODY_OD / 2 + 2, poly_bot - 3,
           n_xr - 5, poly_bot - 6,
           "BARBED SADDLE-TEE\n(BRASS)",
           fs=5, color=C_BRASS, font=FONT, zorder=20, bbox=_bbox)
    leader(ax_nz, NZ_BODY_OD / 2, nz_bot + NZ_BODY_H / 2,
           n_xr - 5, nz_bot + NZ_BODY_H / 2,
           "FLAT-FAN\nSPRAY NOZZLE",
           fs=5, color=C_NOZZLE, font=FONT, zorder=20, bbox=_bbox)
    ax_nz.text(n_xl + 12, poly_ctr, "WATER", ha="center", va="center",
               fontsize=5, color=C_WATER, fontweight="bold",
               bbox=_bbox, **FONT, zorder=15)

    # Dimensions
    draw_dim_v(ax_nz, n_xl + 8, beam_bot_z, beam_bot_z + BEAMH,
               f"{BEAMH}mm\nRHS", offset=2, fs=5, font=FONT)
    draw_dim_v(ax_nz, n_xr - 8, poly_bot, poly_top,
               f"{POLY_OD:.0f}mm\nOD", offset=2, fs=4.5, font=FONT, right=True)

    ax_nz.text(0, n_yt - 1, "NOZZLE CONNECTION",
               ha="center", va="top", fontsize=7, color="#CC6600",
               fontweight="bold", **FONT, zorder=20)
    ax_nz.text(0, n_yt - 5, f"(SADDLE-TEE INTO THE SIDE POLY — TYP. ×{N_NOZZLES})",
               ha="center", va="top", fontsize=5, color=C_DIM,
               **FONT, zorder=20)

    # ─────────────────────────────────────────────────────────────────────
    # RIGHT PANEL — FEED POLE: HOSE ZIP-TIE BUNDLING (elevation)
    # The 1/2" feed hose runs tangent down the Ø25 telescoping push pole and is
    # bound to it by grey zip-tie loops at ~200mm intervals (matches the 3D
    # model / report §3.12). Pole shown straight; it articulates at the ball
    # joint on the beam top.
    # ─────────────────────────────────────────────────────────────────────
    p_xl, p_xr = -78, 96
    ax_pole.set_xlim(p_xl, p_xr)
    ax_pole.set_ylim(-72, 1010)

    POLE_OD = 25
    HOSE_OD2 = 16
    pole_z0, pole_z1 = 30, 905              # pole bottom (ball joint) → handle base
    hose_x = POLE_OD / 2 + HOSE_OD2 / 2      # 20.5 — hose center, tangent to the pole
    hose_l = hose_x - HOSE_OD2 / 2           # 12.5 — hose left edge
    hose_r = hose_x + HOSE_OD2 / 2           # 28.5 — hose right edge
    zt_zs = [150, 350, 550, 750]             # zip-tie loops @ ~200mm

    # beam-top reference strip + manifold + ball joint at the base
    ax_pole.add_patch(Rectangle((p_xl + 5, -60), p_xr - p_xl - 10, 12,
                      fc=C_ALUM_FILL, ec=C_FRAME, lw=0.8, hatch="///", zorder=2))
    ax_pole.add_patch(Rectangle((hose_x - 17, -46), 36, 34,
                      fc=C_WATER, ec=C_FRAME, lw=1.0, alpha=0.85, zorder=4))   # manifold
    ax_pole.plot([hose_x, hose_x, hose_x + 1], [pole_z0 + 8, -10, -12],
                 color=C_BLUE, lw=2.2, alpha=0.6, zorder=5)                    # flex into manifold
    ax_pole.add_patch(Circle((0, pole_z0), 12, fc="#C8B070", ec=C_FRAME, lw=1.0, zorder=6))  # ball joint

    # telescoping pole (Ø25 Al) + tangent feed hose
    ax_pole.add_patch(Rectangle((-POLE_OD / 2, pole_z0), POLE_OD, pole_z1 - pole_z0,
                      fc=C_ALUM_FILL, ec=C_FRAME, lw=1.2, zorder=4))
    for zz in (560, 575):                                                      # telescope break
        ax_pole.plot([-POLE_OD / 2, POLE_OD / 2], [zz, zz + 8], color=C_FRAME, lw=0.7, zorder=4.6)
    ax_pole.add_patch(Rectangle((hose_l, pole_z0 + 8), HOSE_OD2, (pole_z1 - 35) - (pole_z0 + 8),
                      fc=C_HOSE, ec=C_BLUE, lw=1.0, alpha=0.6, zorder=5))

    # grey zip-tie loops binding pole + hose
    for zt in zt_zs:
        ax_pole.add_patch(Rectangle((-POLE_OD / 2 - 5, zt - 3),
                          (hose_r + 5) - (-POLE_OD / 2 - 5), 6,
                          fc="#9A9A9A", ec=C_FRAME, lw=0.7, zorder=7))
        ax_pole.add_patch(Rectangle((hose_r + 4, zt - 5), 6, 10,
                          fc="#6E6E6E", ec=C_FRAME, lw=0.5, zorder=7.5))        # tie head

    # T-handle at the operator end
    ax_pole.add_patch(Rectangle((-POLE_OD / 2, pole_z1 - 6), POLE_OD, 12,
                      fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, zorder=5))
    ax_pole.add_patch(Rectangle((-55, pole_z1 + 6), 110, 12,
                      fc="#B0B0B8", ec=C_FRAME, lw=1.0, zorder=5))

    # labels + spacing dim
    leader(ax_pole, 0, 660, p_xl + 16, 720,
           f"Ø{POLE_OD}mm AL\nTELESCOPING POLE", fs=5, color=C_FRAME, font=FONT, zorder=20, bbox=_bbox)
    leader(ax_pole, hose_x, 470, p_xr - 4, 540,
           "1/2\" FEED HOSE\n(TANGENT TO POLE)", fs=5, color=C_BLUE, font=FONT, zorder=20, bbox=_bbox)
    leader(ax_pole, hose_r + 7, zt_zs[1], p_xr - 4, zt_zs[1] + 95,
           "GRAY ZIP-TIE LOOP\n(@ ~200mm)", fs=5, color="#707070", font=FONT, zorder=20, bbox=_bbox)
    leader(ax_pole, 0, pole_z1 + 12, p_xl + 16, pole_z1 - 30,
           "T-HANDLE", fs=5, color=C_FRAME, font=FONT, zorder=20, bbox=_bbox)
    leader(ax_pole, 0, pole_z0, p_xl + 16, 130,
           "BALL JOINT +\nMANIFOLD\n(BEAM TOP)", fs=5, color="#A06000", font=FONT, zorder=20, bbox=_bbox)
    draw_dim_v(ax_pole, p_xl + 34, zt_zs[0], zt_zs[1], "~200", offset=2, fs=5, font=FONT)

    ax_pole.text((p_xl + p_xr) / 2, 1002, "FEED POLE — HOSE BUNDLING",
                 ha="center", va="top", fontsize=7, color="#CC6600",
                 fontweight="bold", **FONT, zorder=20)
    ax_pole.text((p_xl + p_xr) / 2, 960, "(zip-tie loops @ ~200mm · pole shown straight)",
                 ha="center", va="top", fontsize=5, color=C_DIM, **FONT, zorder=20)

    # ── Title block ──────────────────────────────────────────────────────
    ax_tb = fig.add_axes([0.04, 0.005, 0.92, 0.06])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 7 OF {TOTAL_SHEETS}",
                drawing_title="SPRAY BAR ASSEMBLY",
                subtitle="DETAIL B — CENTER FEED · NOZZLE · FEED-POLE HOSE BUNDLING",
                scale_note="SCALE 2:1 — AXES IN mm",
                height=0.7)

    _save(fig, "spray-bar-sheet7")


# ═════════════════════════════════════════════════════════════════════════════
# Shared helpers
# ═════════════════════════════════════════════════════════════════════════════

def _save(fig, stem):
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    png = os.path.join(DIAGRAMS_DIR, f"{stem}.png")
    fig.savefig(png, dpi=150, bbox_inches="tight", facecolor=C_BG)
    plt.close(fig)
    print(f"  {png} saved")


# ═════════════════════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    draw_sheet1()
    draw_sheet2()
    draw_sheet3()
    draw_sheet4()
    draw_sheet5()
    draw_sheet6()
    draw_sheet7()
