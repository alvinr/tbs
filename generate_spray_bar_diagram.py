#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_spray_bar_diagram.py
Spray bar assembly detail for TBS-001 processing tray wash system.

Sheet 1 — Gantry spray bar:
  Left panel:  X-Z elevation looking along Yd (left carriage area).
               Shows container wall, processing tray, walkway grating,
               wheel carriage under walkway, beam/spray-pipe extending into
               open area, BV-02, flex hose.  Vertical exaggerated 4×.
  Right panel: Yd-Z cross-section looking along X (one carriage end view).
               Shows both wheels, carriage plate, beam/spray-pipe (SHS with
               water fill and spray holes), walkway grating above.
               Uniform 1:2 scale.

Output:
  diagrams/spray-bar-sheet1.png
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Circle
from matplotlib.gridspec import GridSpec

from tbs_constants import (
    svg_path,
    C_OUT, C_CL, C_DIM, C_ALUM,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_W,
    PROC_TRAY_D,
    PROC_TRAY_RIM,
    WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T,
    WALKWAY_LEFT_X,
    PROC_OPEN_X_L, PROC_OPEN_X_R,
    SPRAY_BAR_BEAM, SPRAY_BAR_BEAM_T,
    SPRAY_BAR_TRAVEL, SPRAY_BAR_HOLE_SP,
    BV02_Z,
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
FONT     = dict(family="monospace")

# ── Gantry carriage geometry (local — not yet in tbs_constants) ──────────────
WHEEL_DIA = 50         # 2" nylon wheel — matches tray rim height
WHEEL_WIDTH = 20       # wheel width (mm)
N_WHEELS_PER_SIDE = 2
WHEEL_SPACING_YD = 200 # spacing between wheels in Yd direction (mm)
TRAY_FLOOR_Z = 2       # tray sheet metal on floor (mm)

WHEEL_AXLE_Z = TRAY_FLOOR_Z + WHEEL_DIA / 2          # = 27mm

# L-bracket drops beam below axle for grating clearance.
# Target: ~25mm gap between beam top and grate bottom (75mm).
BRACKET_DROP = 17      # mm below axle centerline to beam bottom
BEAM_Z_BOT = WHEEL_AXLE_Z - BRACKET_DROP              # = 10mm
BEAM_Z_TOP = BEAM_Z_BOT + SPRAY_BAR_BEAM              # = 72mm
BEAM_W = SPRAY_BAR_BEAM        # 40mm
BEAM_T = SPRAY_BAR_BEAM_T      # 3mm
BEAM_BORE = BEAM_W - 2 * BEAM_T  # 34mm internal

GRATE_Z_BOT = WALKWAY_H - WALKWAY_GRATE_T  # 75mm
GRATE_Z_TOP = WALKWAY_H                     # 100mm

BEAM_SPAN = PROC_OPEN_X_R - PROC_OPEN_X_L  # 3,859mm

# Carriage X position (center of walkway width)
CARRIAGE_X_L = WALKWAY_LEFT_X + WALKWAY_W / 2    # ≈ 320mm

WALL_T = 3  # corrugated wall thickness (visual)

# ═════════════════════════════════════════════════════════════════════════════
# SHEET 1
# ═════════════════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(22, 12))
fig.patch.set_facecolor(C_BG)
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.6, 1], wspace=0.08)

# ─────────────────────────────────────────────────────────────────────────────
# LEFT PANEL — X-Z elevation looking along Yd, left carriage area
# Horizontal 1:6, Vertical 1:1.5 (4× vertical exaggeration)
# ─────────────────────────────────────────────────────────────────────────────
ax = fig.add_subplot(gs[0, 0])
ax.set_facecolor(C_BG)
ax.axis("off")

H_SC = 6.0    # horizontal scale (X dimension)
V_SC = 1.5    # vertical scale (Z dimension) — 4× exaggeration

def sx(x_mm):
    return 1.0 + x_mm / H_SC

def sz(z_mm):
    return 1.0 + z_mm / V_SC

X_LO = -80
X_HI = 1100
Z_LO = -50
Z_HI = 220

ax.set_xlim(sx(X_LO), sx(X_HI))
ax.set_ylim(sz(Z_LO), sz(Z_HI))

# ── Container left wall ────────────────────────────────────────────────────
wall_vis_t = WALL_T * 6
ax.add_patch(Rectangle((sx(-wall_vis_t), sz(Z_LO)),
                         wall_vis_t / H_SC, (Z_HI - Z_LO) / V_SC,
                         fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
ax.plot([sx(0), sx(0)], [sz(Z_LO), sz(Z_HI)], color=C_OUT, lw=2.0, zorder=3)

# ── Container floor ────────────────────────────────────────────────────────
ax.plot([sx(X_LO), sx(X_HI)], [sz(0), sz(0)], color=C_OUT, lw=2.0, zorder=3)
ax.add_patch(Rectangle((sx(X_LO), sz(-25)),
                         (X_HI - X_LO) / H_SC, 25 / V_SC,
                         fc="#E0E0D8", ec=C_OUT, lw=0.8, hatch="...", zorder=1))

# ── Processing tray ────────────────────────────────────────────────────────
tray_x_l = PROC_TRAY_X_L  # 170mm
tray_x_r = min(PROC_TRAY_X_R, X_HI)

ax.add_patch(Rectangle((sx(tray_x_l), sz(0)),
                         (tray_x_r - tray_x_l) / H_SC, TRAY_FLOOR_Z / V_SC,
                         fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))

# Tray left rim
rim_w = 4
ax.add_patch(Rectangle((sx(tray_x_l), sz(0)),
                         rim_w / H_SC, PROC_TRAY_RIM / V_SC,
                         fc=C_TRAY, ec=C_OUT, lw=1.2, zorder=5))

ax.text(sx(tray_x_l + 400), sz(TRAY_FLOOR_Z + 5),
        "PROCESSING TRAY (304 SS)", ha="center", va="bottom",
        fontsize=5.5, color=C_DIM, style="italic", **FONT, zorder=10)

# LDPE liner
ax.plot([sx(tray_x_l + 10), sx(tray_x_r)],
        [sz(TRAY_FLOOR_Z + 1), sz(TRAY_FLOOR_Z + 1)],
        color="#333333", lw=0.5, ls="--", zorder=5)

# ── Walkway grating (left walkway, X=170-470) ─────────────────────────────
wk_l = WALKWAY_LEFT_X    # 170mm
wk_r = PROC_OPEN_X_L     # 470mm

ax.add_patch(Rectangle((sx(wk_l), sz(GRATE_Z_BOT)),
                         (wk_r - wk_l) / H_SC, WALKWAY_GRATE_T / V_SC,
                         fc=C_GRATE, ec=C_OUT, lw=1.5, zorder=8))
for frac in np.linspace(0.1, 0.9, 5):
    gx = wk_l + (wk_r - wk_l) * frac
    ax.plot([sx(gx), sx(gx)], [sz(GRATE_Z_BOT), sz(GRATE_Z_TOP)],
            color="#888888", lw=0.4, zorder=8)

# Walkway support bracket
bracket_depth = 60
ax.plot([sx(0), sx(0)], [sz(GRATE_Z_BOT - bracket_depth), sz(GRATE_Z_BOT)],
        color=C_FRAME, lw=1.5, zorder=5)
ax.plot([sx(0), sx(wk_r)], [sz(GRATE_Z_BOT), sz(GRATE_Z_BOT)],
        color=C_FRAME, lw=1.2, zorder=5)
ax.plot([sx(0), sx(wk_r)],
        [sz(GRATE_Z_BOT - bracket_depth), sz(GRATE_Z_BOT)],
        color=C_FRAME, lw=0.8, ls="--", zorder=5)

ax.text(sx((wk_l + wk_r) / 2), sz(GRATE_Z_TOP + 12),
        "LEFT WALKWAY\n(PRESS-LOCKED\nSTEEL GRATING)", ha="center", va="bottom",
        fontsize=5.5, color=C_GRATE, fontweight="bold", **FONT, zorder=10)

# ── Wheel carriage under walkway ───────────────────────────────────────────
carriage_cx = CARRIAGE_X_L  # 320mm

# Wheel (ellipse due to different H/V scales)
ax.add_patch(mpatches.Ellipse((sx(carriage_cx), sz(WHEEL_AXLE_Z)),
                               WHEEL_DIA / H_SC, WHEEL_DIA / V_SC,
                               fc=C_NYLON, ec=C_WHEEL, lw=2.0, zorder=7))
ax.add_patch(Circle((sx(carriage_cx), sz(WHEEL_AXLE_Z)),
                      2 / V_SC, fc=C_WHEEL, ec=C_OUT, lw=0.5, zorder=7.5))

# L-bracket: horizontal arm at axle height, vertical drop to beam
brk_t = 5   # bracket thickness (visual)
brk_x_l = carriage_cx - 50
brk_x_r = PROC_OPEN_X_L + 5

# Horizontal arm (at axle height, under walkway)
ax.add_patch(Rectangle((sx(brk_x_l), sz(WHEEL_AXLE_Z - brk_t / 2)),
                         (brk_x_r - brk_x_l) / H_SC, brk_t / V_SC,
                         fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=7))
# Vertical drop (at walkway inner edge)
ax.add_patch(Rectangle((sx(brk_x_r - brk_t), sz(BEAM_Z_BOT)),
                         brk_t / H_SC, (WHEEL_AXLE_Z - BEAM_Z_BOT + brk_t / 2) / V_SC,
                         fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=7))

leader(ax, sx(carriage_cx), sz(WHEEL_AXLE_Z - WHEEL_DIA / 2),
       sx(carriage_cx - 80), sz(WHEEL_AXLE_Z - WHEEL_DIA / 2 - 30),
       f"Ø{WHEEL_DIA}mm NYLON WHEEL\n(2 PER CARRIAGE\nSPACED {WHEEL_SPACING_YD}mm IN Yd)",
       fs=5, color=C_WHEEL, font=FONT, zorder=15)

# ── Beam / spray pipe ─────────────────────────────────────────────────────
beam_x_start = PROC_OPEN_X_L  # 470mm
beam_x_end = X_HI - 50

# Outer SHS rectangle
ax.add_patch(Rectangle((sx(beam_x_start), sz(BEAM_Z_BOT)),
                         (beam_x_end - beam_x_start) / H_SC, BEAM_W / V_SC,
                         fc=C_ALUM_FILL, ec=C_FRAME, lw=2.0, zorder=9))
# Inner bore filled with water
ax.add_patch(Rectangle((sx(beam_x_start + 20), sz(BEAM_Z_BOT + BEAM_T)),
                         (beam_x_end - beam_x_start - 40) / H_SC, BEAM_BORE / V_SC,
                         fc=C_WATER, ec="none", lw=0, alpha=0.3, zorder=9.5))

# Beam continuation arrow
arrow_y = sz(BEAM_Z_BOT + BEAM_W / 2)
ax.annotate("", xy=(sx(X_HI - 10), arrow_y),
            xytext=(sx(X_HI - 80), arrow_y),
            arrowprops=dict(arrowstyle="-|>", color=C_FRAME, lw=2.0),
            zorder=15)

ax.text(sx((beam_x_start + beam_x_end) / 2), sz(BEAM_Z_TOP + 12),
        "40×40×3mm 6061-T6 AL SHS — SPRAY PIPE",
        ha="center", va="bottom", fontsize=6.5, color=C_FRAME,
        fontweight="bold", **FONT, zorder=15)
ax.text(sx((beam_x_start + beam_x_end) / 2), sz(BEAM_Z_TOP + 3),
        f"(SPANS {BEAM_SPAN}mm — WATER THROUGH BORE, 3mm HOLES IN BOTTOM)",
        ha="center", va="bottom", fontsize=5, color=C_DIM,
        **FONT, zorder=15)

# ── Spray holes and water droplets ────────────────────────────────────────
n_drops = 6
for i in range(n_drops):
    frac = (i + 0.5) / n_drops
    drop_x = beam_x_start + 40 + (beam_x_end - beam_x_start - 80) * frac
    # Spray hole marker on beam bottom
    ax.plot([sx(drop_x - 3), sx(drop_x + 3)],
            [sz(BEAM_Z_BOT), sz(BEAM_Z_BOT)],
            color=C_WATER, lw=2.0, zorder=10)
    # Water stream
    ax.plot([sx(drop_x), sx(drop_x)],
            [sz(BEAM_Z_BOT - 1), sz(TRAY_FLOOR_Z + 3)],
            color=C_WATER, lw=0.8, alpha=0.5, zorder=6)
    ax.add_patch(Circle((sx(drop_x), sz(TRAY_FLOOR_Z + 3)),
                          2 / V_SC, fc=C_WATER, ec="none", alpha=0.5, zorder=6))

# Water on tray
ax.add_patch(Rectangle((sx(beam_x_start), sz(TRAY_FLOOR_Z)),
                         (beam_x_end - beam_x_start) / H_SC, 3 / V_SC,
                         fc=C_WATER, ec="none", alpha=0.12, zorder=4.5))

# ── End caps (visible at beam left end — aluminum plate) ──────────────────
cap_t = 5
ax.add_patch(Rectangle((sx(beam_x_start - cap_t), sz(BEAM_Z_BOT)),
                         cap_t / H_SC, BEAM_W / V_SC,
                         fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=9.5))
ax.text(sx(beam_x_start - cap_t - 3), sz(BEAM_Z_BOT + BEAM_W / 2),
        "END\nCAP", ha="right", va="center",
        fontsize=4, color=C_FRAME, **FONT, zorder=15)

# ── BV-02 on container wall ──────────────────────────────────────────────
bv_z = BV02_Z  # 150mm
bv_size = 25

ax.add_patch(Rectangle((sx(-bv_size / 3), sz(bv_z - bv_size / 2)),
                         (bv_size / 3) / H_SC, bv_size / V_SC,
                         fc=C_BLUE, ec=C_FRAME, lw=1.5, alpha=0.6, zorder=12))
ax.plot([sx(0), sx(-15)], [sz(bv_z), sz(bv_z + 25)],
        color=C_FRAME, lw=2.0, zorder=12)

leader(ax, sx(-10), sz(bv_z + 30),
       sx(-60), sz(bv_z + 60),
       "BV-02\n(1/2\" BALL VALVE)",
       fs=5.5, color=C_BLUE, font=FONT, zorder=15)

# Rigid pipe from BV-02 down toward beam
pipe_z_top = bv_z - bv_size / 2
pipe_z_bot = GRATE_Z_TOP + 5
pipe_w = 6
ax.add_patch(Rectangle((sx(-pipe_w / 4), sz(pipe_z_bot)),
                         (pipe_w / 2) / H_SC, (pipe_z_top - pipe_z_bot) / V_SC,
                         fc=C_BLUE, ec=C_FRAME, lw=0.8, alpha=0.5, zorder=11))

# ── Flex hose from pipe to beam feed end ─────────────────────────────────
hose_start_x = 10
hose_start_z = pipe_z_bot
hose_end_x = beam_x_start - cap_t
hose_end_z = BEAM_Z_BOT + BEAM_W / 2

n_pts = 60
hose_xs = np.linspace(hose_start_x, hose_end_x, n_pts)
hose_zs = np.linspace(hose_start_z, hose_end_z, n_pts)
coil_amp = 10
coil_freq = 5
t = np.linspace(0, coil_freq * 2 * np.pi, n_pts)
hose_zs_coil = hose_zs + coil_amp * np.sin(t)

ax.plot([sx(x) for x in hose_xs], [sz(z) for z in hose_zs_coil],
        color=C_HOSE, lw=2.5, alpha=0.7, zorder=11)

ax.text(sx(hose_start_x + 100), sz(hose_start_z + 20),
        "1/2\" REINFORCED PVC\nFLEX HOSE (4m COILED)",
        ha="left", va="bottom", fontsize=4.5, color=C_HOSE, **FONT, zorder=15)

# ── Dimensions ────────────────────────────────────────────────────────────
draw_dim_h(ax, sx(wk_l), sx(wk_r), sz(GRATE_Z_TOP + 55),
           f"{WALKWAY_W}mm WALKWAY", offset=8 / V_SC, fs=5.5, font=FONT)

draw_dim_v(ax, sx(tray_x_l - 20), sz(0), sz(PROC_TRAY_RIM),
           f"{PROC_TRAY_RIM}mm\nRIM", offset=8 / H_SC, fs=5, font=FONT)

draw_dim_v(ax, sx(wk_r + 15), sz(0), sz(GRATE_Z_TOP),
           f"{WALKWAY_H}mm\nDECK", offset=8 / H_SC, fs=5, font=FONT, right=True)

draw_dim_v(ax, sx(beam_x_start + 500), sz(TRAY_FLOOR_Z), sz(BEAM_Z_BOT),
           f"{BEAM_Z_BOT - TRAY_FLOOR_Z:.0f}mm\nSPRAY\nHGT",
           offset=8 / H_SC, fs=4.5, font=FONT)

draw_dim_v(ax, sx(beam_x_start + 600), sz(0), sz(BEAM_Z_TOP),
           "%.0fmm\nBEAM TOP" % BEAM_Z_TOP,
           offset=8 / H_SC, fs=5, font=FONT, right=True)

# Gap between beam top and grate bottom
gap_to_grate = GRATE_Z_BOT - BEAM_Z_TOP
draw_dim_v(ax, sx(wk_r - 20), sz(BEAM_Z_TOP), sz(GRATE_Z_BOT),
           f"{gap_to_grate:.0f}mm\nCLR", offset=8 / H_SC, fs=4.5, font=FONT)

draw_dim_v(ax, sx(carriage_cx + 50), sz(TRAY_FLOOR_Z), sz(TRAY_FLOOR_Z + WHEEL_DIA),
           f"Ø{WHEEL_DIA}mm", offset=8 / H_SC, fs=5, font=FONT, right=True)

# ── Notes ─────────────────────────────────────────────────────────────────
notes = [
    "NOTES:",
    f"1. 40×40×3mm AL SHS beam doubles as spray pipe (water through bore).",
    f"2. Carriages (2× Ø{WHEEL_DIA}mm nylon wheels) ride on tray floor under grating.",
    f"3. Beam spans {BEAM_SPAN}mm (X). Coverage: X={PROC_OPEN_X_L}–{PROC_OPEN_X_R}mm.",
    f"4. Travel: {SPRAY_BAR_TRAVEL}mm in Yd. Tray rim walls guide laterally.",
    "5. Both ends capped; hose connects at one end. Right carriage mirrors left.",
]
draw_notes(ax, notes, sx(X_LO + 20), sz(Z_HI - 5), spacing=10 / V_SC,
           fs=7, font=FONT, width=155 / H_SC)

ax.text(sx(-30), sz(Z_HI - 10),
        "CONTAINER\nLEFT WALL\n(X=0)", ha="right", va="top",
        fontsize=5, color=C_DIM, **FONT)

title_block(ax, "SHEET 1 OF 1",
            drawing_title="SPRAY BAR ASSEMBLY",
            subtitle="GANTRY ELEVATION — VIEW ALONG Yd (LEFT CARRIAGE)",
            scale_note="H 1:6 / V 1:1.5 (4× VERT EXAG) — ALL DIMS IN mm",
            height=0.05)


# ─────────────────────────────────────────────────────────────────────────────
# RIGHT PANEL — Yd-Z cross-section looking along X (carriage end view)
# Uniform 1:2 scale
# ─────────────────────────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(C_BG)
ax2.set_aspect("equal")
ax2.axis("off")

SC2 = 2.0

def dy(yd_mm):
    return 3.0 + yd_mm / SC2

def dz(z_mm):
    return 2.0 + z_mm / SC2

carriage_yd_center = 200
wheel1_yd = carriage_yd_center - WHEEL_SPACING_YD / 2  # 100mm
wheel2_yd = carriage_yd_center + WHEEL_SPACING_YD / 2  # 300mm

DET_YD_LO = wheel1_yd - 100
DET_YD_HI = wheel2_yd + 120
DET_Z_LO = -25
DET_Z_HI = GRATE_Z_TOP + 50

ax2.set_xlim(dy(DET_YD_LO), dy(DET_YD_HI))
ax2.set_ylim(dz(DET_Z_LO), dz(DET_Z_HI))

# Detail title
ax2.text(dy((DET_YD_LO + DET_YD_HI) / 2), dz(DET_Z_HI + 5),
         "DETAIL A — CARRIAGE END VIEW",
         ha="center", va="bottom", fontsize=9, color=C_FRAME,
         fontweight="bold", **FONT, zorder=15)
ax2.text(dy((DET_YD_LO + DET_YD_HI) / 2), dz(DET_Z_HI - 5),
         "(LOOKING ALONG X — SECTION THROUGH LEFT WALKWAY)",
         ha="center", va="top", fontsize=5, color=C_DIM,
         **FONT, zorder=15)
ax2.text(dy((DET_YD_LO + DET_YD_HI) / 2), dz(DET_Z_HI - 15),
         "SCALE 1:2",
         ha="center", va="top", fontsize=5.5, color=C_DIM,
         **FONT, zorder=15)

# ── Container floor ────────────────────────────────────────────────────────
ax2.plot([dy(DET_YD_LO), dy(DET_YD_HI)], [dz(0), dz(0)],
         color=C_OUT, lw=2.0, zorder=3)
ax2.add_patch(Rectangle((dy(DET_YD_LO), dz(-20)),
                          (DET_YD_HI - DET_YD_LO) / SC2, 20 / SC2,
                          fc="#E0E0D8", ec=C_OUT, lw=0.8, hatch="...", zorder=1))

# ── Tray floor ─────────────────────────────────────────────────────────────
ax2.add_patch(Rectangle((dy(DET_YD_LO + 10), dz(0)),
                          (DET_YD_HI - DET_YD_LO - 20) / SC2, TRAY_FLOOR_Z / SC2,
                          fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))

# ── Walkway grating (above) ───────────────────────────────────────────────
ax2.add_patch(Rectangle((dy(DET_YD_LO + 5), dz(GRATE_Z_BOT)),
                          (DET_YD_HI - DET_YD_LO - 10) / SC2, WALKWAY_GRATE_T / SC2,
                          fc=C_GRATE, ec=C_OUT, lw=2.0, zorder=10))
n_mesh = 8
for i in range(n_mesh):
    frac = (i + 0.5) / n_mesh
    mesh_yd = DET_YD_LO + 5 + (DET_YD_HI - DET_YD_LO - 10) * frac
    ax2.plot([dy(mesh_yd), dy(mesh_yd)], [dz(GRATE_Z_BOT), dz(GRATE_Z_TOP)],
             color="#888888", lw=0.5, zorder=10)

ax2.text(dy((DET_YD_LO + DET_YD_HI) / 2), dz(GRATE_Z_BOT - 4),
         f"WALKWAY GRATING ({WALKWAY_GRATE_T}mm)", ha="center", va="top",
         fontsize=5, color=C_GRATE, **FONT, zorder=12)

# ── Wheels ─────────────────────────────────────────────────────────────────
for w_yd in [wheel1_yd, wheel2_yd]:
    ax2.add_patch(Circle((dy(w_yd), dz(WHEEL_AXLE_Z)),
                           WHEEL_DIA / 2 / SC2,
                           fc=C_NYLON, ec=C_WHEEL, lw=2.0, zorder=6))
    ax2.add_patch(Circle((dy(w_yd), dz(WHEEL_AXLE_Z)),
                           3 / SC2, fc=C_WHEEL, ec=C_OUT, lw=0.5, zorder=6.5))
    ax2.plot([dy(w_yd - WHEEL_WIDTH / 2), dy(w_yd + WHEEL_WIDTH / 2)],
             [dz(TRAY_FLOOR_Z), dz(TRAY_FLOOR_Z)],
             color=C_WHEEL, lw=2.0, zorder=5)

leader(ax2, dy(wheel1_yd - WHEEL_DIA / 2), dz(WHEEL_AXLE_Z),
       dy(wheel1_yd - WHEEL_DIA / 2 - 40), dz(WHEEL_AXLE_Z - 15),
       f"Ø{WHEEL_DIA}mm\nNYLON\nWHEEL",
       fs=5, color=C_WHEEL, font=FONT, zorder=15)

# ── L-bracket (end view) ───────────────────────────────────────────────────
brk_t2 = 5   # bracket thickness
plate_yd_l = wheel1_yd - 20
plate_yd_r = wheel2_yd + 20

# Horizontal arm at axle height (connects wheels)
ax2.add_patch(Rectangle((dy(plate_yd_l), dz(WHEEL_AXLE_Z - brk_t2 / 2)),
                          (plate_yd_r - plate_yd_l) / SC2, brk_t2 / SC2,
                          fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=7))

# Vertical drop (both sides of beam, dropping from axle height to beam bottom)
for side_yd in [carriage_yd_center - BEAM_W / 2 - brk_t2,
                carriage_yd_center + BEAM_W / 2]:
    ax2.add_patch(Rectangle((dy(side_yd), dz(BEAM_Z_BOT)),
                              brk_t2 / SC2, (WHEEL_AXLE_Z - BEAM_Z_BOT + brk_t2 / 2) / SC2,
                              fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, zorder=7))

# Axle fork brackets (drop from horizontal arm to hold wheels)
for w_yd in [wheel1_yd, wheel2_yd]:
    for offset in [-WHEEL_WIDTH / 2 - 2, WHEEL_WIDTH / 2 + 2]:
        ax2.plot([dy(w_yd + offset), dy(w_yd + offset)],
                 [dz(WHEEL_AXLE_Z + brk_t2 / 2), dz(WHEEL_AXLE_Z - WHEEL_DIA / 2 + 3)],
                 color=C_FRAME, lw=1.0, zorder=5.5)

leader(ax2, dy(plate_yd_r), dz(WHEEL_AXLE_Z),
       dy(plate_yd_r + 45), dz(WHEEL_AXLE_Z + 12),
       "ALUM. L-BRACKET\n(DROPS BEAM\nBELOW AXLE)",
       fs=5, color=C_FRAME, font=FONT, zorder=15)

# ── Beam / spray pipe cross-section (SHS with water) ─────────────────────
beam_yd_l = carriage_yd_center - BEAM_W / 2
beam_yd_r = carriage_yd_center + BEAM_W / 2

# Outer SHS
ax2.add_patch(Rectangle((dy(beam_yd_l), dz(BEAM_Z_BOT)),
                          BEAM_W / SC2, BEAM_W / SC2,
                          fc=C_ALUM_FILL, ec=C_FRAME, lw=2.5, zorder=8))
# Inner bore with water fill
ax2.add_patch(Rectangle((dy(carriage_yd_center - BEAM_BORE / 2), dz(BEAM_Z_BOT + BEAM_T)),
                          BEAM_BORE / SC2, BEAM_BORE / SC2,
                          fc=C_WATER, ec=C_FRAME, lw=0.8, alpha=0.35, zorder=8.5))

ax2.text(dy(carriage_yd_center), dz(BEAM_Z_TOP + 5),
         f"40×40×3mm\n6061-T6 AL SHS\n(SPRAY PIPE)",
         ha="center", va="bottom", fontsize=5.5, color=C_FRAME,
         fontweight="bold", **FONT, zorder=15)

# Spray hole at beam bottom center
hole_w = 3  # 3mm drill hole
ax2.add_patch(Rectangle((dy(carriage_yd_center - hole_w / 2), dz(BEAM_Z_BOT - 0.5)),
                          hole_w / SC2, (BEAM_T + 1) / SC2,
                          fc=C_WATER, ec=C_FRAME, lw=0.5, zorder=9))

# Water droplet below hole
ax2.plot([dy(carriage_yd_center), dy(carriage_yd_center)],
         [dz(BEAM_Z_BOT - 1), dz(BEAM_Z_BOT - 18)],
         color=C_WATER, lw=1.2, alpha=0.6, zorder=6)
ax2.text(dy(carriage_yd_center + 8), dz(BEAM_Z_BOT - 10),
         f"3mm SPRAY\nHOLE (TYP.\n@{SPRAY_BAR_HOLE_SP}mm c/c)", ha="left", va="center",
         fontsize=4.5, color=C_WATER, **FONT, zorder=15)

# ── Detail dimensions ─────────────────────────────────────────────────────
draw_dim_v(ax2, dy(beam_yd_l - 15), dz(BEAM_Z_BOT), dz(BEAM_Z_TOP),
           f"{BEAM_W}mm", offset=10 / SC2, fs=5.5, font=FONT)

draw_dim_h(ax2, dy(wheel1_yd), dy(wheel2_yd), dz(TRAY_FLOOR_Z + WHEEL_DIA + 8),
           f"{WHEEL_SPACING_YD}mm", offset=10 / SC2, fs=5.5, font=FONT)

draw_dim_v(ax2, dy(DET_YD_LO + 12), dz(GRATE_Z_BOT), dz(GRATE_Z_TOP),
           f"{WALKWAY_GRATE_T}mm", offset=10 / SC2, fs=5, font=FONT)

# Clearance: beam top to grate bottom
clearance = GRATE_Z_BOT - BEAM_Z_TOP
draw_dim_v(ax2, dy(beam_yd_r + 15), dz(BEAM_Z_TOP), dz(GRATE_Z_BOT),
           f"{clearance:.0f}mm\nCLR", offset=10 / SC2, fs=5, font=FONT, right=True)

# Beam bottom to tray floor
draw_dim_v(ax2, dy(beam_yd_l - 30), dz(TRAY_FLOOR_Z), dz(BEAM_Z_BOT),
           f"{BEAM_Z_BOT - TRAY_FLOOR_Z:.0f}mm", offset=10 / SC2, fs=5, font=FONT)

# Wheel diameter
draw_dim_v(ax2, dy(wheel2_yd + WHEEL_DIA / 2 + 10), dz(TRAY_FLOOR_Z), dz(TRAY_FLOOR_Z + WHEEL_DIA),
           f"Ø{WHEEL_DIA}mm", offset=10 / SC2, fs=5, font=FONT, right=True)


# ── Save ──────────────────────────────────────────────────────────────────
os.makedirs("diagrams", exist_ok=True)
fig.savefig("diagrams/spray-bar-sheet1.png", dpi=150, bbox_inches="tight", facecolor=C_BG)
fig.savefig(svg_path("diagrams/spray-bar-sheet1.png"), bbox_inches="tight", facecolor=C_BG)
plt.close(fig)
print("  diagrams/spray-bar-sheet1.png saved")
