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
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

from tbs_constants import (
    svg_path,
    C_OUT, C_CL, C_DIM, C_ALUM,
    C_LEN, C_WID,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_W,
    PROC_TRAY_D, PROC_TRAY_RIM, PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR,
    WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T,
    WALKWAY_LEFT_X, WALKWAY_RIGHT_X, WALKWAY_FAR_YD,
    PROC_OPEN_X_L, PROC_OPEN_X_R,
    SPRAY_BAR_BEAM, SPRAY_BAR_BEAM_T,
    SPRAY_BAR_TRAVEL, SPRAY_BAR_HOLE_SP,
    BV02_X, BV02_Z,
    SPRAY_BAR_SLIT_W,
)
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_notes

DIAGRAMS_DIR = "diagrams"

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

# ── Gantry carriage geometry ─────────────────────────────────────────────────
WHEEL_DIA = 50
WHEEL_WIDTH = 20
N_WHEELS_PER_SIDE = 2
WHEEL_SPACING_YD = 200
TRAY_FLOOR_Z = 2

WHEEL_AXLE_Z = TRAY_FLOOR_Z + WHEEL_DIA / 2
BRACKET_DROP = 17
BEAM_Z_BOT = WHEEL_AXLE_Z - BRACKET_DROP
BEAM_Z_TOP = BEAM_Z_BOT + SPRAY_BAR_BEAM
BEAM_W = SPRAY_BAR_BEAM
BEAM_T = SPRAY_BAR_BEAM_T
BEAM_BORE = BEAM_W - 2 * BEAM_T

# PVC pipe inside beam (1" Sch 40)
PVC_OD = 33.4
PVC_ID = 26.6
PVC_WALL = (PVC_OD - PVC_ID) / 2
C_PVC = "#B8B8C8"
APERTURE_DIA = 12

# U-clamp dimensions
UC_T = 3
UC_GAP = 1
C_UCLAMP = "#D0D0D8"
C_BOLT = "#808088"
UC_FLARE = 12

GRATE_Z_BOT = WALKWAY_H - WALKWAY_GRATE_T
GRATE_Z_TOP = WALKWAY_H

# PVC socket cap geometry
CAP_SOCKET_DEPTH = 20
CAP_WALL_T = 3.5
CAP_CLOSED_T = 3.5
PVC_EXTEND = 25

BEAM_SPAN = PROC_OPEN_X_R - PROC_OPEN_X_L
WALL_T = 3

# Shared layout constants
POLE_X = (PROC_OPEN_X_L + PROC_OPEN_X_R) / 2
SLIT_WIDTH = SPRAY_BAR_SLIT_W
CARRIAGE_YD_CENTER = 200

TOTAL_SHEETS = 6


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 1 — Gantry Elevation
# X-Z section viewed from film plane (along Yd).
# Centered on beam centerline.  Shows walkway slit, pole, beam, BV-02.
# Horizontal scale 1:18, Vertical scale 1:4.5 (4× vert exaggeration)
# ═════════════════════════════════════════════════════════════════════════════

def draw_sheet1():
    fig = plt.figure(figsize=(10, 28))
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
    Z_HI = 2050

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
                 beam_vis_r - beam_x_l, BEAM_W,
                 fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=9))
    ax.add_patch(Rectangle((beam_x_l + 20, BEAM_Z_BOT + BEAM_T + 0.3),
                 beam_vis_r - beam_x_l - 20, PVC_OD,
                 fc=C_PVC, ec=C_FRAME, lw=0.5, alpha=0.5, zorder=9.3))
    ax.add_patch(Rectangle((beam_x_l + 20, BEAM_Z_BOT + BEAM_T + 0.3 + PVC_WALL),
                 beam_vis_r - beam_x_l - 20, PVC_ID,
                 fc=C_WATER, ec="none", alpha=0.3, zorder=9.5))

    ax.text((beam_x_l + pole_x) / 2, BEAM_Z_TOP + 8,
            f"40×40×3mm AL SHS — {beam_length}mm LONG — 1\" PVC PIPE INSIDE",
            ha="center", va="bottom", fontsize=5.5, color=C_FRAME,
            fontweight="bold", **FONT, zorder=15)

    # Spray apertures and droplets
    spray_x_l = PROC_OPEN_X_L
    n_drops = 6
    for i in range(n_drops):
        frac = (i + 0.5) / n_drops
        drop_x = spray_x_l + 50 + (beam_vis_r - spray_x_l - 100) * frac
        ax.plot([drop_x - APERTURE_DIA / 2, drop_x + APERTURE_DIA / 2],
                [BEAM_Z_BOT, BEAM_Z_BOT],
                color=C_WATER, lw=1.5, zorder=10)
        ax.plot([drop_x, drop_x],
                [BEAM_Z_BOT - 1, TRAY_FLOOR_Z + 2],
                color=C_WATER, lw=0.5, alpha=0.4, zorder=6)

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

    # ── Pole through slit down to beam ───────────────────────────────────
    pole_top_z = GRATE_Z_TOP + 890
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
    bv_z = BV02_Z
    bv_size = 30
    pipe_w = 10

    wall_strip_w = 80
    ax.add_patch(Rectangle((BV02_X - wall_strip_w / 2, 0),
                 wall_strip_w, bv_z + bv_size,
                 fc=C_WALL, ec=C_OUT, lw=0.5, alpha=0.2,
                 hatch="///", zorder=10.5))

    for clamp_z in [bv_z * 0.3, bv_z * 0.6]:
        clamp_w = pipe_w + 16
        ax.add_patch(Rectangle((BV02_X - clamp_w / 2, clamp_z - 4),
                     clamp_w, 8,
                     fc="#B0B0B8", ec=C_FRAME, lw=0.8, zorder=11.5))

    ax.add_patch(Rectangle((BV02_X - pipe_w / 2, 0),
                 pipe_w, bv_z,
                 fc=C_BLUE, ec=C_FRAME, lw=0.8, alpha=0.4, zorder=11))

    ax.add_patch(Rectangle((BV02_X - bv_size / 2, bv_z - bv_size / 2),
                 bv_size, bv_size,
                 fc=C_BLUE, ec=C_FRAME, lw=1.5, alpha=0.6, zorder=12))
    ax.plot([BV02_X, BV02_X - 30], [bv_z, bv_z + 30],
            color=C_FRAME, lw=2.0, zorder=12)

    leader(ax, BV02_X - 30, bv_z + 35,
           BV02_X - 375, bv_z + 80,
           f"BV-02 @ Z={int(bv_z)}mm\n(1/2\" BALL VALVE)\nWAIST HEIGHT",
           fs=5.5, color=C_BLUE, font=FONT, zorder=15)

    # ── Flex hose from BV-02 to beam center feed ─────────────────────────
    hose_start_x = BV02_X
    hose_start_z = bv_z - bv_size / 2
    hose_end_x = pole_x
    hose_end_z = BEAM_Z_TOP + 5

    n_pts = 100
    ht = np.linspace(0, 1, n_pts)
    P0 = np.array([hose_start_x, hose_start_z])
    P1 = np.array([hose_start_x + 80, hose_start_z - 300])
    P2 = np.array([hose_end_x - 80, hose_end_z + 200])
    P3 = np.array([hose_end_x, hose_end_z])
    hose_xs = (1-ht)**3*P0[0] + 3*(1-ht)**2*ht*P1[0] + 3*(1-ht)*ht**2*P2[0] + ht**3*P3[0]
    hose_zs = (1-ht)**3*P0[1] + 3*(1-ht)**2*ht*P1[1] + 3*(1-ht)*ht**2*P2[1] + ht**3*P3[1]
    envelope = np.clip(np.minimum(ht, 1 - ht) * 4, 0, 1)
    hose_zs += 3.0 * np.sin(np.linspace(0, 14 * np.pi, n_pts)) * envelope

    ax.plot(hose_xs, hose_zs, color=C_HOSE, lw=2.0, alpha=0.7, zorder=11)

    ax.text(BV02_X + 75, bv_z - 200,
            "1/2\" FLEX HOSE\n-> CENTER FEED\n(4m COILED)",
            ha="left", va="top", fontsize=4.5, color=C_HOSE, **FONT, zorder=15)

    # ── Center feed fitting at beam center ───────────────────────────────
    feed_dot_r = 8
    ax.add_patch(Circle((pole_x, BEAM_Z_TOP), feed_dot_r,
                 fc="#C0A860", ec=C_FRAME, lw=0.8, zorder=12))
    leader(ax, pole_x + feed_dot_r, BEAM_Z_TOP + feed_dot_r,
           pole_x + 350, BEAM_Z_TOP + 40,
           "1/2\" BULKHEAD CENTER FEED",
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
               f"{int(bv_z)}mm BV-02",
               offset=8, fs=4.5, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────
    notes = [
        "GANTRY ELEVATION — SECTION THROUGH NEAR WALKWAY:",
        f"1. 40×40×3mm AL SHS beam spans {BEAM_SPAN}mm. 1\" PVC pipe inside.",
        f"2. {SLIT_WIDTH}mm slit in walkway at beam center X for pole passage.",
        "3. BV-02 on pinhole wall at pinhole centerline, waist height → flex hose → center feed.",
        "4. 12mm apertures in beam, 2mm holes in PVC pipe.",
    ]
    draw_notes(ax, notes, X_LO + 85, 1800, spacing=20, fs=7, font=FONT, width=1600)

    # ── Person silhouette ────────────────────────────────────────────────
    PERSON_H = 1780
    HEAD_R = 80
    oper_x = pole_x - 650
    P_FOOT = GRATE_Z_TOP
    P_HEAD = P_FOOT + PERSON_H
    ax.plot([oper_x, oper_x], [P_FOOT, P_HEAD + HEAD_R],
            color="#2060A0", lw=3.0, zorder=13, solid_capstyle="round")
    ax.scatter([oper_x], [P_HEAD + HEAD_R],
               s=1800, c="#70A8D8", edgecolors="#1A4D80", linewidths=1.0, zorder=14)
    ax.text(oper_x - 30, P_FOOT + PERSON_H / 2,
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

    # ── Processing tray floor and near rim ───────────────────────────────
    tray_yd_start = PROC_TRAY_YD_NEAR
    ax2.add_patch(Rectangle((tray_yd_start, 0),
                  C_YD_HI - tray_yd_start, TRAY_FLOOR_Z,
                  fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))
    ax2.add_patch(Rectangle((tray_yd_start - 3, 0), 6, PROC_TRAY_RIM,
                  fc=C_TRAY, ec=C_OUT, lw=1.2, zorder=5))
    ax2.text(340, TRAY_FLOOR_Z + 6,
             "PROCESSING TRAY (304 SS)", ha="center", va="bottom",
             fontsize=5, color=C_DIM, style="italic", **FONT, zorder=10)

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
             fontsize=5, color=C_GRATE, style="italic", **FONT, zorder=10)

    # Walkway support bracket (ghost)
    brk_depth_r = 60
    ax2.plot([0, 0], [GRATE_Z_BOT - brk_depth_r, GRATE_Z_BOT],
             color=C_FRAME, lw=0.8, alpha=0.25, zorder=5)
    ax2.plot([0, wk_yd_r], [GRATE_Z_BOT, GRATE_Z_BOT],
             color=C_FRAME, lw=0.6, alpha=0.25, zorder=5)
    ax2.plot([0, wk_yd_r], [GRATE_Z_BOT - brk_depth_r, GRATE_Z_BOT],
             color=C_FRAME, lw=0.5, ls="--", alpha=0.25, zorder=5)

    # ── Wheels (2x O50mm nylon) ──────────────────────────────────────────
    for w_yd in [wheel1_yd, wheel2_yd]:
        ax2.add_patch(Circle((w_yd, WHEEL_AXLE_Z), WHEEL_DIA / 2,
                     fc=C_NYLON, ec=C_WHEEL, lw=2.0, zorder=6))
        ax2.add_patch(Circle((w_yd, WHEEL_AXLE_Z), 3,
                     fc=C_WHEEL, ec=C_OUT, lw=0.5, zorder=6.5))
        ax2.plot([w_yd - WHEEL_WIDTH / 2, w_yd + WHEEL_WIDTH / 2],
                 [TRAY_FLOOR_Z, TRAY_FLOOR_Z],
                 color=C_WHEEL, lw=2.0, zorder=5)

    leader(ax2, wheel1_yd - WHEEL_DIA / 2, WHEEL_AXLE_Z,
           wheel1_yd - WHEEL_DIA / 2 - 30, WHEEL_AXLE_Z - 10,
           f"Ø{WHEEL_DIA}mm\nNYLON WHEEL",
           fs=5, color=C_WHEEL, font=FONT, zorder=15)

    # ── Fork brackets ────────────────────────────────────────────────────
    for w_yd in [wheel1_yd, wheel2_yd]:
        for offset in [-WHEEL_WIDTH / 2 - 2, WHEEL_WIDTH / 2 + 2]:
            ax2.plot([w_yd + offset, w_yd + offset],
                     [WHEEL_AXLE_Z + 6, WHEEL_AXLE_Z - WHEEL_DIA / 2 + 4],
                     color=C_FRAME, lw=1.2, zorder=5.5)
        ax2.plot([w_yd - WHEEL_WIDTH / 2 - 4, w_yd + WHEEL_WIDTH / 2 + 4],
                 [WHEEL_AXLE_Z, WHEEL_AXLE_Z],
                 color=C_FRAME, lw=0.8, zorder=6.5)

    # ── L-bracket arm ────────────────────────────────────────────────────
    brk_t_c = 5
    plate_yd_l = wheel1_yd - 18
    plate_yd_r = wheel2_yd + 18

    ax2.add_patch(Rectangle((plate_yd_l, WHEEL_AXLE_Z - brk_t_c / 2),
                  plate_yd_r - plate_yd_l, brk_t_c,
                  fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=7))
    leader(ax2, plate_yd_r, WHEEL_AXLE_Z,
           plate_yd_r + 35, WHEEL_AXLE_Z + 8,
           "AL L-BRACKET\nARM (5mm PLATE)",
           fs=5, color=C_FRAME, font=FONT, zorder=15)

    # ── Fork-to-arm M5 through-bolts ────────────────────────────────────
    arm_top_z = WHEEL_AXLE_Z + brk_t_c / 2
    arm_bot_z = WHEEL_AXLE_Z - brk_t_c / 2

    for w_yd in [wheel1_yd, wheel2_yd]:
        for offset in [-WHEEL_WIDTH / 2 - 2, WHEEL_WIDTH / 2 + 2]:
            fork_yd = w_yd + offset
            ax2.add_patch(Rectangle((fork_yd - 4, arm_top_z), 8, 3,
                         fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=11))
            ax2.add_patch(Rectangle((fork_yd - 2.5, arm_bot_z), 5, brk_t_c,
                         fc=C_BOLT, ec=C_FRAME, lw=0.4, zorder=11))
            ax2.add_patch(Rectangle((fork_yd - 4, arm_bot_z - 4), 8, 4,
                         fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=11))

    leader(ax2, wheel2_yd + WHEEL_WIDTH / 2 + 2, WHEEL_AXLE_Z,
           wheel2_yd + 50, WHEEL_AXLE_Z - 10,
           "M5 SS THRU-BOLT\n+ NYLOC NUT\n(1 PER FORK)",
           fs=4.5, color=C_BOLT, font=FONT, zorder=15)

    # ── Beam / SHS cross-section with PVC pipe ───────────────────────────
    c_beam_l = CARRIAGE_YD_CENTER - BEAM_W / 2
    c_beam_r = CARRIAGE_YD_CENTER + BEAM_W / 2

    ax2.add_patch(Rectangle((c_beam_l, BEAM_Z_BOT), BEAM_W, BEAM_W,
                  fc=C_ALUM_FILL, ec=C_FRAME, lw=2.5, zorder=8))
    ax2.add_patch(Rectangle((CARRIAGE_YD_CENTER - BEAM_BORE / 2, BEAM_Z_BOT + BEAM_T),
                  BEAM_BORE, BEAM_BORE,
                  fc=C_BG, ec=C_FRAME, lw=0.8, zorder=8.5))
    ax2.add_patch(Circle((CARRIAGE_YD_CENTER, BEAM_Z_BOT + BEAM_W / 2), PVC_OD / 2,
                 fc=C_PVC, ec=C_FRAME, lw=1.0, alpha=0.7, zorder=8.7))
    ax2.add_patch(Circle((CARRIAGE_YD_CENTER, BEAM_Z_BOT + BEAM_W / 2), PVC_ID / 2,
                 fc=C_WATER, ec=C_FRAME, lw=0.5, alpha=0.4, zorder=8.8))

    pipe_cz = BEAM_Z_BOT + BEAM_W / 2
    pipe_od_bot_z = pipe_cz - PVC_OD / 2
    PIPE_HOLE_DIA = 2
    ax2.add_patch(Rectangle((CARRIAGE_YD_CENTER - PIPE_HOLE_DIA / 2, pipe_od_bot_z),
                  PIPE_HOLE_DIA, PVC_WALL,
                  fc=C_WATER, ec=C_FRAME, lw=0.5, alpha=0.5, zorder=9.1))

    ax2.text(CARRIAGE_YD_CENTER, BEAM_Z_TOP + 4,
             "40×40×3mm AL SHS\n+ 1\" PVC PIPE", ha="center", va="bottom",
             fontsize=5.5, color=C_FRAME, fontweight="bold", **FONT, zorder=15)

    # ── U-clamp over beam ────────────────────────────────────────────────
    uc_l = CARRIAGE_YD_CENTER - BEAM_W / 2 - UC_T - UC_GAP
    uc_r = CARRIAGE_YD_CENTER + BEAM_W / 2 + UC_GAP + UC_T
    flare_l = uc_l - UC_FLARE
    flare_r = uc_r + UC_FLARE

    ax2.add_patch(Rectangle((uc_l, BEAM_Z_TOP), uc_r - uc_l, UC_T,
                  fc=C_UCLAMP, ec=C_FRAME, lw=1.0, zorder=10))
    for u_yd in [uc_l, uc_r - UC_T]:
        ax2.add_patch(Rectangle((u_yd, BEAM_Z_BOT + UC_T), UC_T,
                     BEAM_Z_TOP - BEAM_Z_BOT - UC_T,
                     fc=C_UCLAMP, ec=C_FRAME, lw=0.8, zorder=10))
    ax2.add_patch(Rectangle((flare_l, BEAM_Z_BOT),
                  uc_l + UC_T - flare_l, UC_T,
                  fc=C_UCLAMP, ec=C_FRAME, lw=0.8, zorder=10))
    ax2.add_patch(Rectangle((uc_r - UC_T, BEAM_Z_BOT),
                  flare_r - uc_r + UC_T, UC_T,
                  fc=C_UCLAMP, ec=C_FRAME, lw=0.8, zorder=10))

    for bolt_yd in [flare_l + UC_FLARE / 2, flare_r - UC_FLARE / 2]:
        ax2.add_patch(Rectangle((bolt_yd - 2.5, arm_bot_z - 4), 5,
                     BEAM_Z_BOT + UC_T - arm_bot_z + 4,
                     fc=C_BOLT, ec=C_FRAME, lw=0.5, zorder=11))
        ax2.add_patch(Rectangle((bolt_yd - 4, BEAM_Z_BOT + UC_T), 8, 3,
                     fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=11))
        ax2.add_patch(Rectangle((bolt_yd - 5, arm_bot_z - 8), 10, 4,
                     fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=11))

    leader(ax2, flare_r, BEAM_Z_BOT + UC_T / 2,
           flare_r + 20, BEAM_Z_BOT - 5,
           "SS U-CLAMP\n+ WING NUTS",
           fs=4.5, color=C_BOLT, font=FONT, zorder=15)

    # 12mm aperture + water jet
    pipe_id_bot_z = pipe_cz - PVC_ID / 2
    ax2.add_patch(Rectangle((CARRIAGE_YD_CENTER - APERTURE_DIA / 2, BEAM_Z_BOT - 0.5),
                  APERTURE_DIA, BEAM_T + 1,
                  fc=C_BG, ec=C_FRAME, lw=0.5, zorder=9))
    ax2.plot([CARRIAGE_YD_CENTER, CARRIAGE_YD_CENTER],
             [pipe_id_bot_z, BEAM_Z_BOT - 16],
             color=C_WATER, lw=1.2, alpha=0.6, zorder=9.2)
    leader(ax2, CARRIAGE_YD_CENTER + PIPE_HOLE_DIA / 2 + 1, pipe_od_bot_z + PVC_WALL / 2,
           CARRIAGE_YD_CENTER + 28, pipe_od_bot_z - 6,
           "2mm PIPE HOLE",
           fs=4.5, color=C_WATER, font=FONT, zorder=15)
    ax2.text(CARRIAGE_YD_CENTER + 4, BEAM_Z_BOT - 5,
             f"12mm APERTURE (TYP. @{SPRAY_BAR_HOLE_SP}mm c/c)",
             ha="left", va="center", fontsize=4.5, color=C_WATER, **FONT, zorder=15)

    # ── Detail C callout ─────────────────────────────────────────────────
    ax2.add_patch(Circle((wheel1_yd, WHEEL_AXLE_Z), WHEEL_DIA / 2 + 8,
                 fc="none", ec="#008800", lw=1.5, ls="--", zorder=20))
    ax2.text(wheel1_yd, WHEEL_AXLE_Z + WHEEL_DIA / 2 + 10,
             "C", ha="center", va="bottom", fontsize=9, color="#008800",
             fontweight="bold", **FONT, zorder=20)

    # ── Ball joint on beam top face ──────────────────────────────────────
    BALL_DIA = 20
    SOCKET_OD = 36
    SOCKET_H = 28
    FLANGE_W = 50
    FLANGE_T = 5
    STUD_DIA = 12
    STUD_EXT = 20
    C_JOINT = "#C8B070"

    beam_top_z_bj = BEAM_Z_TOP
    flange_bot_z = beam_top_z_bj
    socket_bot_z = flange_bot_z + FLANGE_T
    ball_ctr_z = socket_bot_z + SOCKET_H / 2 + 2
    socket_top_z = socket_bot_z + SOCKET_H
    stud_top_z = socket_top_z + STUD_EXT

    ax2.add_patch(Rectangle((CARRIAGE_YD_CENTER - FLANGE_W / 2, flange_bot_z),
                  FLANGE_W, FLANGE_T,
                  fc="#B0B0B8", ec=C_FRAME, lw=1.2, zorder=7))

    # U-bolt wrapping over socket housing
    ubolt_gap = 2
    ubolt_t = 4
    ubolt_l = CARRIAGE_YD_CENTER - SOCKET_OD / 2 - ubolt_gap - ubolt_t
    ubolt_r = CARRIAGE_YD_CENTER + SOCKET_OD / 2 + ubolt_gap + ubolt_t

    ub_arc = np.linspace(0, np.pi, 30)
    ub_arc_r = (ubolt_r - ubolt_l) / 2
    ub_arc_cz = socket_bot_z + SOCKET_H * 0.6
    ub_arc_yd = CARRIAGE_YD_CENTER + ub_arc_r * np.cos(ub_arc)
    ub_arc_z = ub_arc_cz + ub_arc_r * 0.45 * np.sin(ub_arc)
    ax2.plot(list(ub_arc_yd), list(ub_arc_z),
             color=C_BOLT, lw=2.5, zorder=9, solid_capstyle="round")

    ax2.plot([ubolt_l + ubolt_t / 2, ubolt_l + ubolt_t / 2],
             [ub_arc_cz, beam_top_z_bj - BEAM_T - 5],
             color=C_BOLT, lw=2.5, zorder=9)
    ax2.plot([ubolt_r - ubolt_t / 2, ubolt_r - ubolt_t / 2],
             [ub_arc_cz, beam_top_z_bj - BEAM_T - 5],
             color=C_BOLT, lw=2.5, zorder=9)

    for nut_yd in [ubolt_l + ubolt_t / 2, ubolt_r - ubolt_t / 2]:
        ax2.add_patch(Rectangle((nut_yd - 5, beam_top_z_bj - BEAM_T - 8), 10, 4,
                     fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=10))

    # Socket housing
    ax2.add_patch(Rectangle((CARRIAGE_YD_CENTER - SOCKET_OD / 2, socket_bot_z),
                  SOCKET_OD, SOCKET_H,
                  fc=C_JOINT, ec=C_FRAME, lw=1.5, hatch="///", zorder=6))
    bore_r = BALL_DIA / 2 + 1
    ax2.add_patch(Circle((CARRIAGE_YD_CENTER, ball_ctr_z), bore_r,
                 fc=C_BG, ec=C_FRAME, lw=0.5, zorder=6.5))

    # Ball
    ax2.add_patch(Circle((CARRIAGE_YD_CENTER, ball_ctr_z), BALL_DIA / 2,
                 fc="#E0D8C0", ec=C_FRAME, lw=1.5, zorder=7))

    # Stud
    ax2.add_patch(Rectangle((CARRIAGE_YD_CENTER - STUD_DIA / 2, ball_ctr_z),
                  STUD_DIA, stud_top_z - ball_ctr_z,
                  fc="#D0C8B0", ec=C_FRAME, lw=1.0, zorder=7.5))

    # ── Round tube arm ───────────────────────────────────────────────────
    ARM_OD = 25
    ARM_WALL = 2
    ARM_ID = ARM_OD - 2 * ARM_WALL
    arm_base_z_bj = stud_top_z - STUD_EXT + 2
    arm_top_z_bj = arm_base_z_bj + 80

    ax2.add_patch(Rectangle((CARRIAGE_YD_CENTER - ARM_OD / 2, arm_base_z_bj),
                  ARM_OD, arm_top_z_bj - arm_base_z_bj,
                  fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=8))
    ax2.add_patch(Rectangle((CARRIAGE_YD_CENTER - ARM_ID / 2, arm_base_z_bj),
                  ARM_ID, stud_top_z - arm_base_z_bj,
                  fc="#D0C8B0", ec="none", zorder=8.3))
    ax2.add_patch(Rectangle((CARRIAGE_YD_CENTER - ARM_ID / 2, stud_top_z),
                  ARM_ID, arm_top_z_bj - stud_top_z,
                  fc=C_BG, ec=C_FRAME, lw=0.5, zorder=8.5))

    # Pinch bolt
    pinch_z = arm_base_z_bj + 12
    ax2.add_patch(Rectangle((CARRIAGE_YD_CENTER + ARM_OD / 2, pinch_z - 2), 8, 4,
                 fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=9))
    ax2.plot([CARRIAGE_YD_CENTER + ARM_ID / 2, CARRIAGE_YD_CENTER + ARM_OD / 2 + 8],
             [pinch_z, pinch_z],
             color=C_BOLT, lw=1.5, zorder=9)

    # Continuation arrow
    ax2.annotate("", xy=(CARRIAGE_YD_CENTER, arm_top_z_bj + 8),
                 xytext=(CARRIAGE_YD_CENTER, arm_top_z_bj),
                 arrowprops=dict(arrowstyle="->", color=C_FRAME, lw=1.5), zorder=12)
    ax2.text(CARRIAGE_YD_CENTER + 3, arm_top_z_bj + 5,
             "ARM CONTINUES\nTO TRAY SURFACE",
             ha="left", va="center", fontsize=4.5, color=C_DIM,
             style="italic", **FONT, zorder=15)

    # Movement arcs
    for arc_ang in [-25, 25]:
        ang_rad = np.radians(arc_ang)
        arc_len = 35
        ax2.annotate("",
            xy=(CARRIAGE_YD_CENTER + arc_len * np.sin(ang_rad),
                ball_ctr_z + arc_len * np.cos(ang_rad)),
            xytext=(CARRIAGE_YD_CENTER, ball_ctr_z),
            arrowprops=dict(arrowstyle="->", color="#AA0000", lw=0.8,
                            connectionstyle=f"arc3,rad={0.3 if arc_ang > 0 else -0.3}"),
            zorder=12)
    ax2.text(CARRIAGE_YD_CENTER - SOCKET_OD / 2 - 5, ball_ctr_z + 20,
             "MULTI-AXIS\nARTICULATION",
             ha="right", va="center", fontsize=4.5, color="#AA0000",
             bbox=_bbox_cs, **FONT, zorder=15)

    # ── Water hose zip-tied to arm ───────────────────────────────────────
    hose_od = 16
    hose_ctr_yd = CARRIAGE_YD_CENTER + ARM_OD / 2 + hose_od / 2 + 3

    ax2.add_patch(Rectangle((hose_ctr_yd - hose_od / 2, arm_base_z_bj - 5),
                  hose_od, arm_top_z_bj - arm_base_z_bj + 10,
                  fc=C_HOSE, ec=C_BLUE, lw=1.0, alpha=0.6, zorder=7.5))

    for zt_z in [arm_base_z_bj + 15, arm_base_z_bj + 40, arm_base_z_bj + 65]:
        zt_l = CARRIAGE_YD_CENTER - ARM_OD / 2 - 4
        zt_r = hose_ctr_yd + hose_od / 2 + 2
        ax2.add_patch(Rectangle((zt_l, zt_z - 1.5), zt_r - zt_l, 3,
                     fc="none", ec="#222222", lw=1.2, zorder=11))
        ax2.add_patch(Rectangle((zt_l - 2, zt_z - 2), 2, 4,
                     fc="#333333", ec="#222222", lw=0.5, zorder=11))

    # ── Labels ───────────────────────────────────────────────────────────
    leader(ax2, CARRIAGE_YD_CENTER + SOCKET_OD / 2, ball_ctr_z,
           CARRIAGE_YD_CENTER + SOCKET_OD / 2 + 20, ball_ctr_z - 30,
           f"Ø{BALL_DIA}mm BALL JOINT\n(U-BOLT TO BEAM)",
           fs=5, color=C_JOINT, font=FONT, zorder=20)

    leader(ax2, ubolt_r, ub_arc_cz,
           ubolt_r + 22, ub_arc_cz - 8,
           "M8 SS U-BOLT\n+ NYLOC NUTS",
           fs=4.5, color=C_BOLT, font=FONT, zorder=20)

    leader(ax2, CARRIAGE_YD_CENTER + ARM_OD / 2 + 8, pinch_z,
           CARRIAGE_YD_CENTER + 35, pinch_z + 12,
           "M6 PINCH BOLT",
           fs=4.5, color=C_BOLT, font=FONT, zorder=20)

    leader(ax2, CARRIAGE_YD_CENTER + ARM_OD / 2, arm_base_z_bj + 50,
           CARRIAGE_YD_CENTER + 45, arm_base_z_bj + 62,
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

    clearance_c = GRATE_Z_BOT - BEAM_Z_TOP
    draw_dim_v(ax2, c_beam_r + 10, BEAM_Z_TOP, GRATE_Z_BOT,
               f"{clearance_c:.0f}mm\nCLR", offset=6, fs=5, font=FONT, right=True)

    draw_dim_v(ax2, c_beam_l - 22, TRAY_FLOOR_Z, BEAM_Z_BOT,
               f"{BEAM_Z_BOT - TRAY_FLOOR_Z:.0f}mm\nSPRAY",
               offset=6, fs=4.5, font=FONT)

    draw_dim_h(ax2, wk_yd_l, wk_yd_r, GRATE_Z_TOP + 18,
               f"{WALKWAY_W}mm WALKWAY", offset=6, fs=5, font=FONT)

    draw_dim_v(ax2, C_YD_HI - 20, 0, GRATE_Z_TOP,
               f"{WALKWAY_H}mm\nDECK HGT",
               offset=6, fs=5, font=FONT, right=True)

    draw_dim_v(ax2, c_beam_l - 34, beam_top_z_bj, socket_top_z,
               f"{int(socket_top_z - beam_top_z_bj)}mm\nJOINT",
               offset=6, fs=4.5, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────
    cs_notes = [
        "CROSS SECTION (COMPOSITE):",
        f"1. Beam rides on 2× Ø50mm nylon wheels (push/pull via pole).",
        "2. Ball joint on beam top → arm → pole through walkway slit.",
        "3. Water: PVC pipe → 2mm hole → 12mm aperture → spray.",
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

    ax_p.add_patch(Rectangle((slit_x, 0),
                   SLIT_WIDTH, WALKWAY_W,
                   fc="#FF4444", ec="#CC0000", lw=1.5, alpha=0.6, zorder=7))
    ax_p.add_patch(Rectangle((slit_x, WALKWAY_FAR_YD),
                   SLIT_WIDTH, WALKWAY_W,
                   fc="#FF4444", ec="#CC0000", lw=1.5, alpha=0.6, zorder=7))

    leader(ax_p, pole_x, -10,
           pole_x - 500, -220,
           f"{SLIT_WIDTH}mm SLIT @ BEAM\nCENTER (NEAR & FAR\nWALKWAYS — FOR POLE)",
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
# SHEET 4 — Detail A: Beam End (Open)
# Longitudinal section through beam end showing PVC pipe extending past beam,
# socket cap solvent-welded to pipe.  Scale 2:1.
# ═════════════════════════════════════════════════════════════════════════════

def draw_sheet4():
    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor(C_BG)
    ax_a = fig.add_axes([0.05, 0.08, 0.90, 0.88])
    ax_a.set_facecolor(C_BG)
    ax_a.axis("off")

    pvc_od_h = PVC_OD / 2
    pvc_id_h = PVC_ID / 2
    cap_od_h = pvc_od_h + CAP_WALL_T

    beam_end_x = 0
    pipe_end_x = beam_end_x - PVC_EXTEND
    cap_open_x = pipe_end_x + CAP_SOCKET_DEPTH
    cap_closed_x = pipe_end_x - CAP_CLOSED_T

    d_xl, d_xr = cap_closed_x - 10, 50
    d_yb, d_yt = -30, 30
    ax_a.set_xlim(d_xl, d_xr)
    ax_a.set_ylim(d_yb, d_yt)

    ax_a.text((d_xl + d_xr) / 2, d_yt - 1,
              "DETAIL A — BEAM END (OPEN)",
              ha="center", va="top", fontsize=8, color="#CC0000",
              fontweight="bold", **FONT, zorder=20)
    ax_a.text((d_xl + d_xr) / 2, d_yt - 5,
              "(LONGITUDINAL SECTION — SCALE 2:1)",
              ha="center", va="top", fontsize=5, color=C_DIM,
              **FONT, zorder=20)

    _bbox_a = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.85)

    # ── SHS top wall ─────────────────────────────────────────────────────
    ax_a.add_patch(Rectangle((beam_end_x, 17), d_xr - beam_end_x, 3,
                   fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=3))
    # ── SHS bottom wall ──────────────────────────────────────────────────
    ax_a.add_patch(Rectangle((beam_end_x, -20), d_xr - beam_end_x, 3,
                   fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=3))

    # ── Open beam end face ───────────────────────────────────────────────
    ax_a.plot([beam_end_x, beam_end_x], [-20, 20],
              color=C_FRAME, lw=1.5, zorder=5)

    # ── Square bore inside beam ──────────────────────────────────────────
    ax_a.add_patch(Rectangle((beam_end_x, -17), d_xr - beam_end_x, 34,
                   fc=C_BG, ec=C_FRAME, lw=0.5, zorder=3.5))

    # ── PVC pipe walls ───────────────────────────────────────────────────
    ax_a.add_patch(Rectangle((pipe_end_x, pvc_id_h), d_xr - pipe_end_x, PVC_WALL,
                   fc=C_PVC, ec=C_FRAME, lw=0.6, zorder=4))
    ax_a.add_patch(Rectangle((pipe_end_x, -pvc_od_h), d_xr - pipe_end_x, PVC_WALL,
                   fc=C_PVC, ec=C_FRAME, lw=0.6, zorder=4))
    ax_a.plot([pipe_end_x, pipe_end_x], [-pvc_od_h, pvc_od_h],
              color=C_FRAME, lw=1.0, zorder=5.5)

    # ── PVC socket cap ───────────────────────────────────────────────────
    cap_verts = [
        (cap_open_x,                  cap_od_h),
        (cap_closed_x,                cap_od_h),
        (cap_closed_x,               -cap_od_h),
        (cap_open_x,                 -cap_od_h),
        (cap_open_x,                 -pvc_od_h),
        (cap_closed_x + CAP_CLOSED_T, -pvc_od_h),
        (cap_closed_x + CAP_CLOSED_T,  pvc_od_h),
        (cap_open_x,                  pvc_od_h),
    ]
    ax_a.add_patch(mpatches.Polygon(cap_verts, closed=True,
                   fc=C_PVC, ec=C_FRAME, lw=0.8, zorder=5))

    # ── Solvent weld line ────────────────────────────────────────────────
    ax_a.plot([cap_open_x, pipe_end_x], [pvc_od_h, pvc_od_h],
              color="#AA3030", lw=0.8, ls="--", zorder=6)
    ax_a.plot([cap_open_x, pipe_end_x], [-pvc_od_h, -pvc_od_h],
              color="#AA3030", lw=0.8, ls="--", zorder=6)

    # ── Water inside PVC ─────────────────────────────────────────────────
    ax_a.add_patch(Rectangle((pipe_end_x, -pvc_id_h), d_xr - pipe_end_x, PVC_ID,
                   fc=C_WATER, ec="none", alpha=0.15, zorder=3.8))

    # ── Labels ───────────────────────────────────────────────────────────
    leader(ax_a, beam_end_x + 5, 19, beam_end_x + 20, d_yt - 8,
           "40×40×3 AL SHS\n(OPEN END)",
           fs=5, color=C_FRAME, font=FONT, zorder=20, bbox=_bbox_a)

    leader(ax_a, (cap_open_x + beam_end_x / 2) + 20, pvc_od_h + CAP_WALL_T - 4,
           d_xr - 15, d_yt - 4,
           "1\" Sch 40 PVC PIPE\n(EXTENDS PAST BEAM)",
           fs=5, color=C_PVC, font=FONT, zorder=20)

    leader(ax_a, cap_closed_x + CAP_CLOSED_T / 2, -cap_od_h,
           cap_closed_x - 5, d_yb + 2,
           "1\" PVC SOCKET CAP\n(SOLVENT WELDED)",
           fs=5, color=C_PVC, font=FONT, zorder=20)

    ax_a.text(d_xr - 8, 0, "WATER",
              ha="center", va="center", fontsize=5, color=C_WATER,
              fontweight="bold", bbox=_bbox_a, **FONT, zorder=15)

    ax_a.text((pipe_end_x + cap_closed_x + CAP_CLOSED_T) / 2 + 3, -PVC_OD + PVC_ID - 8.5,
              "BUTT\nJOINT",
              ha="center", va="center", fontsize=4, color="#AA3030",
              fontweight="bold", bbox=_bbox_a, **FONT, zorder=15)

    # ── Dimensions ───────────────────────────────────────────────────────
    draw_dim_h(ax_a, cap_closed_x, beam_end_x, d_yb + 4,
               f"{PVC_EXTEND + CAP_CLOSED_T:.0f}mm\nPROTRUSION",
               offset=2, fs=4.5, font=FONT)

    draw_dim_h(ax_a, cap_closed_x, cap_open_x, d_yb + 7,
               f"{CAP_SOCKET_DEPTH + CAP_CLOSED_T:.0f}mm\nCAP LENGTH",
               offset=2, fs=4.5, font=FONT)

    draw_dim_h(ax_a, pipe_end_x, cap_open_x, cap_od_h + 2,
               f"{CAP_SOCKET_DEPTH}mm\nENGAGEMENT",
               offset=2, fs=4, font=FONT)

    draw_dim_v(ax_a, d_xr - 3, -17, 17,
               "34mm BORE", offset=1, fs=5, font=FONT, right=True)

    draw_dim_v(ax_a, d_xr - 8, 17, 20,
               "3mm\nWALL", offset=2, fs=4.5, font=FONT, right=True)

    draw_dim_v(ax_a, d_xl + 8, -pvc_od_h, pvc_od_h,
               f"{PVC_OD:.1f}mm\nPVC OD", offset=3, fs=4.5, font=FONT)

    # ── Title block ──────────────────────────────────────────────────────
    ax_tb = fig.add_axes([0.04, 0.005, 0.92, 0.06])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 4 OF {TOTAL_SHEETS}",
                drawing_title="SPRAY BAR ASSEMBLY",
                subtitle="DETAIL A — BEAM END (OPEN, LONGITUDINAL SECTION)",
                scale_note="SCALE 2:1 — AXES IN mm",
                height=0.7)

    _save(fig, "spray-bar-sheet4")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 5 — Detail C: Wheel Attachment
# Section along axle centerline showing fork bracket arms, nylon wheel bore,
# axle pin, snap-ring retention, and connection to L-bracket horizontal arm.
# ═════════════════════════════════════════════════════════════════════════════

def draw_sheet5():
    fig = plt.figure(figsize=(12, 16))
    fig.patch.set_facecolor(C_BG)
    ax_w = fig.add_axes([0.08, 0.06, 0.84, 0.90])
    ax_w.set_facecolor(C_BG)
    ax_w.axis("off")

    w_xl, w_xr = -21, 21
    w_yb, w_yt = -30, 35
    ax_w.set_xlim(w_xl, w_xr)
    ax_w.set_ylim(w_yb, w_yt)

    ax_w.text(0, w_yt - 1,
              "DETAIL C — WHEEL ATTACHMENT",
              ha="center", va="top", fontsize=8, color="#008800",
              fontweight="bold", **FONT, zorder=20)
    ax_w.text(0, w_yt - 5,
              "(SECTION ALONG AXLE — SCALE 2:1)",
              ha="center", va="top", fontsize=5.5, color=C_DIM,
              **FONT, zorder=20)

    C_NYLON_FILL = "#E8DCC0"

    # ── L-bracket horizontal arm ─────────────────────────────────────────
    ax_w.add_patch(Rectangle((-17, 13), 34, 5,
                   fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=3))

    # ── Left fork arm ────────────────────────────────────────────────────
    ax_w.add_patch(Rectangle((-17, -13), 6, 26,
                   fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=4))

    # ── Right fork arm ───────────────────────────────────────────────────
    ax_w.add_patch(Rectangle((11, -13), 6, 26,
                   fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=4))

    # ── Nylon wheel body ─────────────────────────────────────────────────
    ax_w.add_patch(Rectangle((-10, -25), 20, 50,
                   fc=C_NYLON_FILL, ec=C_WHEEL, lw=1.5, hatch="...", zorder=3))

    # ── Clearance gaps fork/wheel ────────────────────────────────────────
    for gap_x in [-11, 10]:
        ax_w.add_patch(Rectangle((gap_x, -13), 1, 26,
                       fc=C_BG, ec="none", zorder=3.5))

    # ── Axle pin ─────────────────────────────────────────────────────────
    ax_w.add_patch(Rectangle((-20, -5), 40, 10,
                   fc="#D0D0D8", ec=C_FRAME, lw=1.0, zorder=5))
    ax_w.add_patch(Rectangle((-10, -5), 20, 10,
                   fc="#D0D0D8", ec="none", zorder=5))

    # ── Snap rings ───────────────────────────────────────────────────────
    for sr_x in [-20, 18.5]:
        ax_w.add_patch(Rectangle((sr_x, -7), 1.5, 2,
                       fc="#888888", ec=C_FRAME, lw=0.8, zorder=6))
        ax_w.add_patch(Rectangle((sr_x, 5), 1.5, 2,
                       fc="#888888", ec=C_FRAME, lw=0.8, zorder=6))

    # ── M5 through-bolts ────────────────────────────────────────────────
    C_BOLT_FILL = "#D0D0D8"
    for bolt_cx in [-14, 14]:
        ax_w.add_patch(Rectangle((bolt_cx - 4, 18), 8, 3,
                       fc=C_BOLT_FILL, ec=C_FRAME, lw=0.8, zorder=7))
        ax_w.add_patch(Rectangle((bolt_cx - 2.5, 4), 5, 14,
                       fc=C_BOLT_FILL, ec=C_FRAME, lw=0.6, zorder=7))
        ax_w.add_patch(Rectangle((bolt_cx - 4, 0), 8, 4,
                       fc=C_BOLT_FILL, ec=C_FRAME, lw=0.8, zorder=7))

    _bbox_w = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.85)

    # ── Tray floor reference ─────────────────────────────────────────────
    ax_w.plot([w_xl, w_xr], [-25, -25],
              color=C_TRAY, lw=1.0, ls="--", zorder=2)
    ax_w.text(w_xr - 1, -26, "TRAY FLOOR",
              ha="right", va="top", fontsize=5, color=C_DIM,
              style="italic", bbox=_bbox_w, **FONT, zorder=15)

    # ── Labels ───────────────────────────────────────────────────────────
    leader(ax_w, 13, 16, w_xr - 1, w_yt - 8,
           "L-BRACKET\nHORIZ. ARM\n(5mm AL)",
           fs=5.5, color=C_FRAME, font=FONT, zorder=20)

    leader(ax_w, 13, 0, w_xr - 1, -10,
           "6mm AL\nFORK ARM",
           fs=5.5, color=C_FRAME, font=FONT, zorder=20)

    ax_w.text(0, -18, "Ø50mm NYLON\nWHEEL (CUT)",
              ha="center", va="top", fontsize=5.5, color=C_WHEEL,
              bbox=_bbox_w, **FONT, zorder=20)

    leader(ax_w, 5, 5, 5, 10,
           "Ø10mm SS\nAXLE PIN",
           fs=5.5, color="#888888", font=FONT, zorder=20, bbox=_bbox_w)

    ax_w.text(-17.5, -10, "SNAP\nRING",
              ha="center", va="top", fontsize=5, color="#666666",
              bbox=_bbox_w, **FONT, zorder=20)

    leader(ax_w, -14, 20, -20, w_yt - 10,
           "M5×16 SS\nTHRU-BOLT\n+ NYLOC NUT\n(1 PER FORK)",
           fs=5, color="#808088", font=FONT, zorder=20)

    # ── Dimensions ───────────────────────────────────────────────────────
    draw_dim_h(ax_w, -10, 10, w_yb + 3,
               "20mm", offset=2, fs=5.5, font=FONT)

    draw_dim_v(ax_w, w_xl + 2, -5, 5,
               "Ø10", offset=2, fs=5, font=FONT)

    # ── Title block ──────────────────────────────────────────────────────
    ax_tb = fig.add_axes([0.04, 0.005, 0.92, 0.045])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 5 OF {TOTAL_SHEETS}",
                drawing_title="SPRAY BAR ASSEMBLY",
                subtitle="DETAIL C — WHEEL ATTACHMENT (SECTION ALONG AXLE)",
                scale_note="SCALE 2:1 — AXES IN mm",
                height=0.7)

    _save(fig, "spray-bar-sheet5")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 6 — Detail D: Wheel Attachment Plan
# X-Yd looking down.  Beam, L-bracket arm, U-clamp, fork brackets, wheels.
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
              "(LOOKING DOWN — AXES IN mm)",
              ha="center", va="top", fontsize=5, color=C_DIM,
              **FONT, zorder=20)

    _bbox_d = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.85)

    # ── Beam (plan view) ─────────────────────────────────────────────────
    ax_d.add_patch(Rectangle((-BEAM_SHOW_LEN, -BEAM_W / 2),
                   2 * BEAM_SHOW_LEN, BEAM_W,
                   fc=C_ALUM_FILL, ec=C_FRAME, lw=2.0, zorder=5))
    ax_d.add_patch(Rectangle((-BEAM_SHOW_LEN, -BEAM_BORE / 2),
                   2 * BEAM_SHOW_LEN, BEAM_BORE,
                   fc=C_BG, ec=C_FRAME, lw=0.5, zorder=5.5))
    ax_d.add_patch(Rectangle((-BEAM_SHOW_LEN, -PVC_OD / 2),
                   2 * BEAM_SHOW_LEN, PVC_OD,
                   fc=C_PVC, ec=C_FRAME, lw=0.6, alpha=0.6, zorder=5.7))
    ax_d.add_patch(Rectangle((-BEAM_SHOW_LEN, -PVC_ID / 2),
                   2 * BEAM_SHOW_LEN, PVC_ID,
                   fc=C_WATER, ec="none", alpha=0.3, zorder=5.8))
    for bx in [-BEAM_SHOW_LEN, BEAM_SHOW_LEN]:
        ax_d.plot([bx, bx], [-BEAM_W / 2 - 3, BEAM_W / 2 + 3],
                  color=C_FRAME, lw=1.5, ls=(0, (5, 3)), zorder=6)

    ax_d.text(60, 0, "40×40 SHS\n+ 1\" PVC",
              ha="center", va="center", fontsize=4.5, color=C_FRAME,
              bbox=_bbox_d, **FONT, zorder=15)

    # ── L-bracket arm ────────────────────────────────────────────────────
    arm_half_span = WHEEL_SPACING_YD / 2 + 18
    arm_w_x = 20
    ax_d.add_patch(Rectangle((CARRIAGE_OFFSET_X - arm_w_x / 2, -arm_half_span),
                   arm_w_x, 2 * arm_half_span,
                   fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0,
                   hatch="///", alpha=0.7, zorder=4))

    # ── U-clamp top plate ────────────────────────────────────────────────
    uc_w_yd_top = BEAM_W + 2 * UC_T + 2 * UC_GAP
    ax_d.add_patch(Rectangle((CARRIAGE_OFFSET_X - arm_w_x / 2, -uc_w_yd_top / 2),
                   arm_w_x, uc_w_yd_top,
                   fc=C_UCLAMP, ec=C_FRAME, lw=1.0, alpha=0.5, zorder=6))
    for side in [-1, 1]:
        foot_yd = side * (BEAM_W / 2 + UC_GAP + UC_T)
        if side < 0:
            foot_yd -= UC_FLARE
        ax_d.add_patch(Rectangle((CARRIAGE_OFFSET_X - arm_w_x / 2, foot_yd),
                       arm_w_x, UC_FLARE + UC_T,
                       fc=C_UCLAMP, ec=C_FRAME, lw=0.8, alpha=0.6, zorder=6))

    for side in [-1, 1]:
        bolt_yd = side * (BEAM_W / 2 + UC_GAP + UC_T + UC_FLARE / 2)
        ax_d.add_patch(Circle((CARRIAGE_OFFSET_X, bolt_yd), 3,
                     fc=C_BOLT, ec=C_FRAME, lw=0.5, zorder=8))

    leader(ax_d, CARRIAGE_OFFSET_X + arm_w_x / 2,
           BEAM_W / 2 + UC_GAP + UC_T + UC_FLARE,
           BEAM_W - 100, BEAM_W / 2 + 30,
           "U-CLAMP\nFLARED LEGS\n+ WING NUTS",
           fs=5, color=C_BOLT, font=FONT, zorder=20)

    # ── Fork brackets ────────────────────────────────────────────────────
    fork_t = 6
    for w_sign in [-1, 1]:
        w_yd_ctr = w_sign * WHEEL_SPACING_YD / 2
        for offset in [-WHEEL_WIDTH / 2 - 2, WHEEL_WIDTH / 2 + 2]:
            fork_yd = w_yd_ctr + offset
            ax_d.add_patch(Rectangle((CARRIAGE_OFFSET_X - fork_t / 2 - 4, fork_yd - 1),
                           fork_t, 2,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=0.6, zorder=7))

    # ── Wheels ───────────────────────────────────────────────────────────
    for w_sign in [-1, 1]:
        w_yd_ctr = w_sign * WHEEL_SPACING_YD / 2
        ax_d.add_patch(Rectangle((CARRIAGE_OFFSET_X - WHEEL_WIDTH / 2,
                                  w_yd_ctr - WHEEL_DIA / 2),
                       WHEEL_WIDTH, WHEEL_DIA,
                       fc=C_NYLON, ec=C_WHEEL, lw=1.5, alpha=0.6, zorder=3))
        ax_d.add_patch(Circle((CARRIAGE_OFFSET_X, w_yd_ctr), 5,
                     fc="#D0D0D8", ec=C_FRAME, lw=0.5, zorder=7))

    # ── Labels ───────────────────────────────────────────────────────────
    leader(ax_d, CARRIAGE_OFFSET_X + WHEEL_WIDTH / 2,
           -WHEEL_SPACING_YD / 2,
           D_X_HI - 225, -WHEEL_SPACING_YD / 2 - 10,
           f"Ø{WHEEL_DIA}mm WHEEL\n({WHEEL_WIDTH}mm WIDE)",
           fs=5, color=C_WHEEL, font=FONT, zorder=20)

    leader(ax_d, -arm_w_x / 2 - 1, 0,
           D_X_LO + 200, 45,
           "L-BRACKET ARM\n(5mm AL PLATE)",
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
                subtitle="DETAIL D — WHEEL ATTACHMENT PLAN (LOOKING DOWN)",
                scale_note="AXES IN mm",
                height=0.7)

    _save(fig, "spray-bar-sheet6")


# ═════════════════════════════════════════════════════════════════════════════
# Shared helpers
# ═════════════════════════════════════════════════════════════════════════════

def _save(fig, stem):
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    png = os.path.join(DIAGRAMS_DIR, f"{stem}.png")
    fig.savefig(png, dpi=150, bbox_inches="tight", facecolor=C_BG)
    fig.savefig(svg_path(png), bbox_inches="tight", facecolor=C_BG)
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
