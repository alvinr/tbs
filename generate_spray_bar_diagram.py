#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_spray_bar_diagram.py
Spray bar assembly detail for TBS-001 processing tray wash system.

Sheet 1 — Gantry spray bar:
  Left panel:  X-Z elevation looking along Yd (left carriage area).
               Shows container wall, processing tray, walkway grating,
               wheel carriage with fork brackets under walkway, beam/spray-
               pipe with water connection detail, BV-02, flex hose.
               Vertical exaggerated 4×.
  Right panel: Yd-Z cross-section (operator view) looking along X.
               Shows processing tray, beam/spray pipe in open area,
               near walkway with operator figure, telescoping push pole
               with clip attachment.  Non-uniform scale (schematic).

Output:
  diagrams/spray-bar-sheet1.png
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
from matplotlib.gridspec import GridSpec

from tbs_constants import (
    svg_path,
    C_OUT, C_CL, C_DIM, C_ALUM,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_W,
    PROC_TRAY_D, PROC_TRAY_RIM, PROC_TRAY_YD_NEAR,
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
C_OPER   = "#555555"
FONT     = dict(family="monospace")

# ── Gantry carriage geometry ─────────────────────────────────────────────────
WHEEL_DIA = 50
WHEEL_WIDTH = 20
N_WHEELS_PER_SIDE = 2
WHEEL_SPACING_YD = 200
TRAY_FLOOR_Z = 2

WHEEL_AXLE_Z = TRAY_FLOOR_Z + WHEEL_DIA / 2          # = 27mm
BRACKET_DROP = 17
BEAM_Z_BOT = WHEEL_AXLE_Z - BRACKET_DROP              # = 10mm
BEAM_Z_TOP = BEAM_Z_BOT + SPRAY_BAR_BEAM              # = 50mm
BEAM_W = SPRAY_BAR_BEAM        # 40mm
BEAM_T = SPRAY_BAR_BEAM_T      # 3mm
BEAM_BORE = BEAM_W - 2 * BEAM_T  # 34mm

GRATE_Z_BOT = WALKWAY_H - WALKWAY_GRATE_T  # 75mm
GRATE_Z_TOP = WALKWAY_H                     # 100mm

BEAM_SPAN = PROC_OPEN_X_R - PROC_OPEN_X_L  # 3,859mm

CARRIAGE_X_L = WALKWAY_LEFT_X + WALKWAY_W / 2    # ≈ 320mm

WALL_T = 3

# ═════════════════════════════════════════════════════════════════════════════
# SHEET 1
# ═════════════════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(22, 14))
fig.patch.set_facecolor(C_BG)
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.3, 1], wspace=0.06)

# ─────────────────────────────────────────────────────────────────────────────
# LEFT PANEL — X-Z elevation looking along Yd, left carriage area
# Horizontal 1:6, Vertical 1:1.5 (4× vertical exaggeration)
# ─────────────────────────────────────────────────────────────────────────────
ax = fig.add_subplot(gs[0, 0])
ax.set_facecolor(C_BG)
ax.axis("off")

H_SC = 6.0
V_SC = 1.5

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

# Fork brackets — vertical plates straddling the wheel (item 3: show attachment)
fork_drop_top = WHEEL_AXLE_Z + 8
fork_drop_bot = TRAY_FLOOR_Z + 5
for fork_offset in [-15, 15]:
    fx = carriage_cx + fork_offset
    ax.plot([sx(fx), sx(fx)], [sz(fork_drop_bot), sz(fork_drop_top)],
            color=C_FRAME, lw=1.5, zorder=6.5)
# Axle pin through fork and wheel
ax.plot([sx(carriage_cx - 18), sx(carriage_cx + 18)],
        [sz(WHEEL_AXLE_Z), sz(WHEEL_AXLE_Z)],
        color=C_FRAME, lw=1.0, zorder=7.5)

# L-bracket: horizontal arm at axle height, vertical drop to beam
# Item 1: shortened carriage boss
brk_t = 5   # bracket thickness (visual)
brk_x_l = carriage_cx - 20   # shortened from -50
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
       f"Ø{WHEEL_DIA}mm NYLON WHEEL\n(FORK BRACKET + 10mm\nAXLE PIN, 2 PER SIDE)",
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
    ax.plot([sx(drop_x - 3), sx(drop_x + 3)],
            [sz(BEAM_Z_BOT), sz(BEAM_Z_BOT)],
            color=C_WATER, lw=2.0, zorder=10)
    ax.plot([sx(drop_x), sx(drop_x)],
            [sz(BEAM_Z_BOT - 1), sz(TRAY_FLOOR_Z + 3)],
            color=C_WATER, lw=0.8, alpha=0.5, zorder=6)
    ax.add_patch(Circle((sx(drop_x), sz(TRAY_FLOOR_Z + 3)),
                          2 / V_SC, fc=C_WATER, ec="none", alpha=0.5, zorder=6))

# Water on tray
ax.add_patch(Rectangle((sx(beam_x_start), sz(TRAY_FLOOR_Z)),
                         (beam_x_end - beam_x_start) / H_SC, 3 / V_SC,
                         fc=C_WATER, ec="none", alpha=0.12, zorder=4.5))

# ── End cap with bulkhead fitting (item 2: show water connection) ────────
cap_t = 5
ax.add_patch(Rectangle((sx(beam_x_start - cap_t), sz(BEAM_Z_BOT)),
                         cap_t / H_SC, BEAM_W / V_SC,
                         fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=9.5))

# Bulkhead fitting protruding from end cap
fitting_w = 12
fitting_h = 15
fitting_x = beam_x_start - cap_t - fitting_w
fitting_z = BEAM_Z_BOT + BEAM_W / 2 - fitting_h / 2
ax.add_patch(Rectangle((sx(fitting_x), sz(fitting_z)),
                         fitting_w / H_SC, fitting_h / V_SC,
                         fc="#C0A860", ec=C_FRAME, lw=1.0, zorder=9.5))
# Hose barb adapter
barb_w = 8
ax.add_patch(Rectangle((sx(fitting_x - barb_w), sz(fitting_z + 3)),
                         barb_w / H_SC, (fitting_h - 6) / V_SC,
                         fc="#C0A860", ec=C_FRAME, lw=0.8, zorder=9.5))

leader(ax, sx(fitting_x), sz(fitting_z),
       sx(fitting_x - 40), sz(fitting_z - 25),
       "1/2\" NPT BULKHEAD\n+ HOSE BARB",
       fs=5, color=C_FRAME, font=FONT, zorder=15)

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
hose_end_x = fitting_x - barb_w
hose_end_z = BEAM_Z_BOT + BEAM_W / 2

n_pts = 80
ht = np.linspace(0, 1, n_pts)
P0 = np.array([hose_start_x, hose_start_z])
P1 = np.array([hose_start_x + 80, hose_end_z - 5])
P2 = np.array([hose_end_x - 120, hose_end_z - 5])
P3 = np.array([hose_end_x, hose_end_z])
hose_xs = (1-ht)**3*P0[0] + 3*(1-ht)**2*ht*P1[0] + 3*(1-ht)*ht**2*P2[0] + ht**3*P3[0]
hose_zs = (1-ht)**3*P0[1] + 3*(1-ht)**2*ht*P1[1] + 3*(1-ht)*ht**2*P2[1] + ht**3*P3[1]
envelope = np.clip(np.minimum(ht, 1 - ht) * 4, 0, 1)
hose_zs += 1.5 * np.sin(np.linspace(0, 10 * np.pi, n_pts)) * envelope

ax.plot([sx(x) for x in hose_xs], [sz(z) for z in hose_zs],
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

gap_to_grate = GRATE_Z_BOT - BEAM_Z_TOP
draw_dim_v(ax, sx(wk_r - 20), sz(BEAM_Z_TOP), sz(GRATE_Z_BOT),
           f"{gap_to_grate:.0f}mm\nCLR", offset=8 / H_SC, fs=4.5, font=FONT)

draw_dim_v(ax, sx(carriage_cx + 50), sz(TRAY_FLOOR_Z), sz(TRAY_FLOOR_Z + WHEEL_DIA),
           f"Ø{WHEEL_DIA}mm", offset=8 / H_SC, fs=5, font=FONT, right=True)

# ── Notes ─────────────────────────────────────────────────────────────────
notes = [
    "NOTES:",
    f"1. 40×40×3mm AL SHS beam doubles as spray pipe (water through bore).",
    f"2. Carriages (2× Ø{WHEEL_DIA}mm wheels) ride on tray floor under grating.",
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
            height=0.04)


# ─────────────────────────────────────────────────────────────────────────────
# RIGHT PANEL — Yd-Z cross section (operator view)
# Looking along X.  Schematic — non-uniform H/V scale.
# Shows: tray, beam, near walkway, operator, telescoping pole.
# ─────────────────────────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(C_BG)
ax2.axis("off")

SC2_H = 5.0    # Yd horizontal scale
SC2_V = 10.0   # Z vertical scale

def dy(yd_mm):
    return 3.0 + yd_mm / SC2_H

def dz(z_mm):
    return 2.0 + z_mm / SC2_V

# View range
R_YD_LO = -60
R_YD_HI = 800
R_Z_LO = -30
R_Z_HI = 1900

ax2.set_xlim(dy(R_YD_LO), dy(R_YD_HI))
ax2.set_ylim(dz(R_Z_LO), dz(R_Z_HI))

# Panel title
ax2.text(dy((R_YD_LO + R_YD_HI) / 2), dz(R_Z_HI - 10),
         "CROSS SECTION — OPERATOR VIEW",
         ha="center", va="top", fontsize=9, color=C_FRAME,
         fontweight="bold", **FONT, zorder=15)
ax2.text(dy((R_YD_LO + R_YD_HI) / 2), dz(R_Z_HI - 70),
         "(LOOKING ALONG X — SCHEMATIC, NOT TO SCALE)",
         ha="center", va="top", fontsize=5, color=C_DIM,
         **FONT, zorder=15)

# ── Container pinhole wall (Yd=0) ────────────────────────────────────────
wall_w = 40  # visual wall thickness
ax2.add_patch(Rectangle((dy(-wall_w), dz(R_Z_LO)),
                          wall_w / SC2_H, (R_Z_HI - R_Z_LO) / SC2_V,
                          fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
ax2.plot([dy(0), dy(0)], [dz(R_Z_LO), dz(R_Z_HI)],
         color=C_OUT, lw=2.0, zorder=3)

# ── Container floor ────────────────────────────────────────────────────────
ax2.plot([dy(R_YD_LO), dy(R_YD_HI)], [dz(0), dz(0)],
         color=C_OUT, lw=2.0, zorder=3)
ax2.add_patch(Rectangle((dy(R_YD_LO), dz(-25)),
                          (R_YD_HI - R_YD_LO) / SC2_H, 25 / SC2_V,
                          fc="#E0E0D8", ec=C_OUT, lw=0.8, hatch="...", zorder=1))

# ── Processing tray floor and near rim ───────────────────────────────────
tray_yd_start = PROC_TRAY_YD_NEAR  # 80mm
ax2.add_patch(Rectangle((dy(tray_yd_start), dz(0)),
                          (R_YD_HI - tray_yd_start) / SC2_H, TRAY_FLOOR_Z / SC2_V,
                          fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))

# Near rim (vertical wall at Yd=80)
ax2.add_patch(Rectangle((dy(tray_yd_start - 3), dz(0)),
                          6 / SC2_H, PROC_TRAY_RIM / SC2_V,
                          fc=C_TRAY, ec=C_OUT, lw=1.2, zorder=5))

ax2.text(dy(450), dz(TRAY_FLOOR_Z + 15),
         "PROCESSING TRAY (304 SS)", ha="center", va="bottom",
         fontsize=5, color=C_DIM, style="italic", **FONT, zorder=10)

# ── Near walkway grating (Yd=0–300) ──────────────────────────────────────
wk_yd_l = 0
wk_yd_r = WALKWAY_W  # 300mm

ax2.add_patch(Rectangle((dy(wk_yd_l), dz(GRATE_Z_BOT)),
                          (wk_yd_r - wk_yd_l) / SC2_H, WALKWAY_GRATE_T / SC2_V,
                          fc=C_GRATE, ec=C_OUT, lw=1.5, zorder=8))
for frac in np.linspace(0.1, 0.9, 5):
    gyd = wk_yd_l + (wk_yd_r - wk_yd_l) * frac
    ax2.plot([dy(gyd), dy(gyd)], [dz(GRATE_Z_BOT), dz(GRATE_Z_TOP)],
             color="#888888", lw=0.4, zorder=8)

# Support bracket (wall to grating)
brk_depth_r = 60
ax2.plot([dy(0), dy(0)], [dz(GRATE_Z_BOT - brk_depth_r), dz(GRATE_Z_BOT)],
         color=C_FRAME, lw=1.5, zorder=5)
ax2.plot([dy(0), dy(wk_yd_r)], [dz(GRATE_Z_BOT), dz(GRATE_Z_BOT)],
         color=C_FRAME, lw=1.2, zorder=5)
ax2.plot([dy(0), dy(wk_yd_r)],
         [dz(GRATE_Z_BOT - brk_depth_r), dz(GRATE_Z_BOT)],
         color=C_FRAME, lw=0.8, ls="--", zorder=5)

ax2.text(dy((wk_yd_l + wk_yd_r) / 2), dz(GRATE_Z_TOP + 20),
         "NEAR WALKWAY", ha="center", va="bottom",
         fontsize=5.5, color=C_GRATE, fontweight="bold", **FONT, zorder=10)

# ── Beam / spray pipe (in open area, just past walkway) ──────────────────
beam_yd = 450   # beam position (mid-travel example)
beam_yd_l = beam_yd - BEAM_W / 2
beam_yd_r = beam_yd + BEAM_W / 2

# Outer SHS
ax2.add_patch(Rectangle((dy(beam_yd_l), dz(BEAM_Z_BOT)),
                          BEAM_W / SC2_H, BEAM_W / SC2_V,
                          fc=C_ALUM_FILL, ec=C_FRAME, lw=2.0, zorder=9))
# Inner bore with water
ax2.add_patch(Rectangle((dy(beam_yd - BEAM_BORE / 2), dz(BEAM_Z_BOT + BEAM_T)),
                          BEAM_BORE / SC2_H, BEAM_BORE / SC2_V,
                          fc=C_WATER, ec=C_FRAME, lw=0.8, alpha=0.35, zorder=9.5))

ax2.text(dy(beam_yd), dz(BEAM_Z_TOP + 15),
         f"40×40×3mm AL SHS\nSPRAY PIPE", ha="center", va="bottom",
         fontsize=5.5, color=C_FRAME, fontweight="bold", **FONT, zorder=15)

# Spray hole at bottom
hole_w = 3
ax2.add_patch(Rectangle((dy(beam_yd - hole_w / 2), dz(BEAM_Z_BOT - 0.5)),
                          hole_w / SC2_H, (BEAM_T + 1) / SC2_V,
                          fc=C_WATER, ec=C_FRAME, lw=0.5, zorder=9))
# Water stream
for drip_offset in [-30, 0, 30]:
    drip_yd = beam_yd + drip_offset
    ax2.plot([dy(drip_yd), dy(drip_yd)],
             [dz(BEAM_Z_BOT - 1), dz(TRAY_FLOOR_Z + 2)],
             color=C_WATER, lw=0.8, alpha=0.4, zorder=6)

# Water on tray
ax2.add_patch(Rectangle((dy(beam_yd - 80), dz(TRAY_FLOOR_Z)),
                          160 / SC2_H, 3 / SC2_V,
                          fc=C_WATER, ec="none", alpha=0.15, zorder=4.5))

ax2.text(dy(beam_yd + 35), dz(BEAM_Z_BOT - 8),
         f"3mm SPRAY HOLES\n@{SPRAY_BAR_HOLE_SP}mm c/c",
         ha="left", va="center", fontsize=4.5, color=C_WATER, **FONT, zorder=15)

# ── Operator figure on walkway ───────────────────────────────────────────
op_yd = 170       # operator center on walkway
op_foot_z = GRATE_Z_TOP  # 100mm (standing on deck)
op_height = 1700  # total height (mm)

# Legs (two lines from feet to hips)
hip_z = op_foot_z + 850
ax2.plot([dy(op_yd - 20), dy(op_yd - 8)],
         [dz(op_foot_z), dz(hip_z)],
         color=C_OPER, lw=2.5, zorder=11)
ax2.plot([dy(op_yd + 20), dy(op_yd + 8)],
         [dz(op_foot_z), dz(hip_z)],
         color=C_OPER, lw=2.5, zorder=11)

# Torso (thick line from hips to shoulders)
shoulder_z = op_foot_z + 1400
ax2.plot([dy(op_yd), dy(op_yd)],
         [dz(hip_z), dz(shoulder_z)],
         color=C_OPER, lw=3.5, zorder=11)

# Head (circle)
head_z = op_foot_z + 1550
head_r = 70
ax2.add_patch(Circle((dy(op_yd), dz(head_z)),
                       head_r / SC2_V,
                       fc=C_OPER, ec=C_FRAME, lw=1.0, alpha=0.6, zorder=11))

# Arms — reaching forward and down toward pole
hand_yd = op_yd + 60
hand_z = op_foot_z + 1050
# Upper arms from shoulders
ax2.plot([dy(op_yd + 10), dy(hand_yd)],
         [dz(shoulder_z - 50), dz(hand_z)],
         color=C_OPER, lw=2.0, zorder=11)
ax2.plot([dy(op_yd - 5), dy(hand_yd - 10)],
         [dz(shoulder_z - 50), dz(hand_z + 30)],
         color=C_OPER, lw=2.0, zorder=11)

# Feet (small rectangles)
for foot_offset in [-20, 20]:
    ax2.add_patch(Rectangle((dy(op_yd + foot_offset - 8), dz(op_foot_z - 5)),
                              20 / SC2_H, 8 / SC2_V,
                              fc=C_OPER, ec="none", alpha=0.5, zorder=11))

ax2.text(dy(op_yd - 50), dz(head_z + 100),
         "OPERATOR", ha="center", va="bottom",
         fontsize=6, color=C_OPER, fontweight="bold", **FONT, zorder=15)

# ── Telescoping push pole (item 4: show attachment) ──────────────────────
# Pole from operator's hands down to beam center
pole_top_yd = hand_yd
pole_top_z = hand_z
pole_bot_yd = beam_yd
pole_bot_z = BEAM_Z_BOT + BEAM_W / 2   # beam center

# Draw pole as tapered line (thicker at handle, thinner at beam)
ax2.plot([dy(pole_top_yd), dy(pole_bot_yd)],
         [dz(pole_top_z), dz(pole_bot_z)],
         color="#8B6914", lw=3.0, zorder=10, solid_capstyle="round")
ax2.plot([dy(pole_top_yd), dy(pole_bot_yd)],
         [dz(pole_top_z), dz(pole_bot_z)],
         color="#BFA040", lw=1.5, zorder=10.5)

# Pole clip / U-bolt at beam (item 4)
clip_size = 18
ax2.add_patch(Rectangle((dy(beam_yd - clip_size / 2), dz(BEAM_Z_TOP)),
                          clip_size / SC2_H, clip_size / SC2_V,
                          fc="none", ec="#8B6914", lw=2.0, zorder=10))
ax2.add_patch(Rectangle((dy(beam_yd - clip_size / 2 + 2), dz(BEAM_Z_TOP + 2)),
                          (clip_size - 4) / SC2_H, (clip_size - 4) / SC2_V,
                          fc="#C0A860", ec="none", alpha=0.5, zorder=10))

leader(ax2, dy(beam_yd + clip_size / 2), dz(BEAM_Z_TOP + clip_size),
       dy(beam_yd + 120), dz(BEAM_Z_TOP + 80),
       "U-BOLT POLE CLIP\n(SS, BOLTED TO\nBEAM TOP FACE)",
       fs=5, color="#8B6914", font=FONT, zorder=15)

# Pole label
pole_mid_yd = (pole_top_yd + pole_bot_yd) / 2
pole_mid_z = (pole_top_z + pole_bot_z) / 2
ax2.text(dy(pole_mid_yd - 50), dz(pole_mid_z),
         "TELESCOPING\nALUM. POOL\nPOLE (1.2–2.4m)",
         ha="right", va="center",
         fontsize=5, color="#8B6914", **FONT, zorder=15)

# ── BV-02 and hose on container wall (water connection context) ──────────
bv2_yd = 10    # BV-02 near wall, on pipe
bv2_z = BV02_Z  # 150mm
bv_sz = 20
ax2.add_patch(Rectangle((dy(bv2_yd - bv_sz / 2), dz(bv2_z - bv_sz / 2)),
                          bv_sz / SC2_H, bv_sz / SC2_V,
                          fc=C_BLUE, ec=C_FRAME, lw=1.2, alpha=0.6, zorder=12))
ax2.text(dy(bv2_yd), dz(bv2_z + bv_sz),
         "BV-02", ha="center", va="bottom",
         fontsize=5, color=C_BLUE, fontweight="bold", **FONT, zorder=15)

# Flex hose from BV-02 along near rim to beam
hose_n = 60
ht2 = np.linspace(0, 1, hose_n)
H0 = np.array([bv2_yd + 20, bv2_z - bv_sz / 2])
H1 = np.array([tray_yd_start + 40, BEAM_Z_BOT + BEAM_W])
H2 = np.array([beam_yd - 80, BEAM_Z_BOT + BEAM_W])
H3 = np.array([beam_yd_l - 10, BEAM_Z_BOT + BEAM_W / 2])
hose_yd = (1-ht2)**3*H0[0] + 3*(1-ht2)**2*ht2*H1[0] + 3*(1-ht2)*ht2**2*H2[0] + ht2**3*H3[0]
hose_zz = (1-ht2)**3*H0[1] + 3*(1-ht2)**2*ht2*H1[1] + 3*(1-ht2)*ht2**2*H2[1] + ht2**3*H3[1]
env2 = np.clip(np.minimum(ht2, 1 - ht2) * 4, 0, 1)
hose_zz += 1.5 * np.sin(np.linspace(0, 8 * np.pi, hose_n)) * env2

ax2.plot([dy(y) for y in hose_yd], [dz(z) for z in hose_zz],
         color=C_HOSE, lw=2.0, alpha=0.6, zorder=11)
ax2.text(dy(200), dz(bv2_z - 20),
         "1/2\" FLEX HOSE\n(4m COILED)",
         ha="left", va="top", fontsize=4.5, color=C_HOSE, **FONT, zorder=15)

# ── Carriage wheels shown as ghost (item 3: context for wheel attachment) ─
# Wheels exist at a different X station (under left/right walkways).
# Show as dashed outline near the walkway inner edge for context.
ghost_w_yd = WALKWAY_W - 30   # 270mm — near inner edge of walkway
ghost_w_z = WHEEL_AXLE_Z
ax2.add_patch(Circle((dy(ghost_w_yd), dz(ghost_w_z)),
                       WHEEL_DIA / 2 / SC2_V,
                       fc="none", ec=C_WHEEL, lw=1.0, ls="--", zorder=6))
ax2.text(dy(ghost_w_yd), dz(ghost_w_z - WHEEL_DIA / 2 - 15),
         f"WHEEL (Ø{WHEEL_DIA})\nAT CARRIAGE\n(BEHIND SECTION)",
         ha="center", va="top", fontsize=4, color=C_WHEEL,
         style="italic", **FONT, zorder=15)

# ── Dimensions ────────────────────────────────────────────────────────────
draw_dim_h(ax2, dy(wk_yd_l), dy(wk_yd_r), dz(GRATE_Z_TOP + 50),
           f"{WALKWAY_W}mm WALKWAY", offset=10 / SC2_V, fs=5.5, font=FONT)

draw_dim_v(ax2, dy(R_YD_HI - 30), dz(0), dz(GRATE_Z_TOP),
           f"{WALKWAY_H}mm\nDECK HGT",
           offset=10 / SC2_H, fs=5, font=FONT, right=True)

draw_dim_h(ax2, dy(wk_yd_r), dy(beam_yd), dz(BEAM_Z_TOP + 120),
           f"{beam_yd - int(wk_yd_r)}mm\n(BEAM TO\nWALKWAY\nEDGE)",
           offset=10 / SC2_V, fs=4.5, font=FONT)

draw_dim_v(ax2, dy(beam_yd_l - 30), dz(BEAM_Z_BOT), dz(BEAM_Z_TOP),
           f"{BEAM_W}mm", offset=10 / SC2_H, fs=5, font=FONT)

draw_dim_v(ax2, dy(tray_yd_start - 25), dz(0), dz(PROC_TRAY_RIM),
           f"{PROC_TRAY_RIM}mm\nRIM",
           offset=8 / SC2_H, fs=4.5, font=FONT)

# ── Right panel notes ────────────────────────────────────────────────────
r_notes = [
    "OPERATOR VIEW:",
    f"1. Beam travels {SPRAY_BAR_TRAVEL}mm along Yd (push/pull with pole).",
    "2. Tray rim walls (50mm) guide beam laterally — no rails needed.",
    "3. Pole clips to beam top via SS U-bolt. Detaches for storage.",
    "4. Hose coils at pinhole wall; extends as beam travels toward far rim.",
]
draw_notes(ax2, r_notes, dy(R_YD_LO + 20), dz(R_Z_HI - 120), spacing=40 / SC2_V,
           fs=5.5, font=FONT, width=700 / SC2_H)


# ── Save ──────────────────────────────────────────────────────────────────
os.makedirs("diagrams", exist_ok=True)
fig.savefig("diagrams/spray-bar-sheet1.png", dpi=150, bbox_inches="tight", facecolor=C_BG)
fig.savefig(svg_path("diagrams/spray-bar-sheet1.png"), bbox_inches="tight", facecolor=C_BG)
plt.close(fig)
print("  diagrams/spray-bar-sheet1.png saved")
