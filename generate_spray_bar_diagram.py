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

fig = plt.figure(figsize=(28, 26))
fig.patch.set_facecolor(C_BG)
gs = GridSpec(3, 2, figure=fig, width_ratios=[1.3, 1],
              height_ratios=[2.5, 1, 1],
              wspace=0.06, hspace=0.08, bottom=0.045)

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


# ── Detail callout circle on main view ────────────────────────────────────
cap_cx = beam_x_start - cap_t / 2
cap_cz = BEAM_Z_BOT + BEAM_W / 2
ax.add_patch(mpatches.Ellipse((sx(cap_cx), sz(cap_cz)),
                               80 / H_SC, 80 / V_SC,
                               fc="none", ec="#CC0000", lw=1.5, ls="--", zorder=20))
ax.text(sx(cap_cx), sz(cap_cz - 50),
        "DETAIL A", ha="center", va="top", fontsize=8, color="#CC0000",
        fontweight="bold", **FONT, zorder=20)

# Detail B callout — carriage / wheel area
carr_cx = carriage_cx
carr_cz = WHEEL_AXLE_Z
ax.add_patch(mpatches.Ellipse((sx(carr_cx), sz(carr_cz)),
                               90 / H_SC, 90 / V_SC,
                               fc="none", ec="#0066AA", lw=1.5, ls="--", zorder=20))
ax.text(sx(carr_cx), sz(carr_cz + 55),
        "DETAIL B", ha="center", va="bottom", fontsize=8, color="#0066AA",
        fontweight="bold", **FONT, zorder=20)


# ─────────────────────────────────────────────────────────────────────────────
# BOTTOM-LEFT PANEL — Detail A: End cap water connection
# Longitudinal section through beam center at end cap, scale 2:1.
# X: along beam axis, - = outside (hose side), + = inside (bore/water)
# Y: perpendicular to beam axis, 0 = beam centerline
#
# Assembly (outside → inside):
#   flex hose → clamp → barb → hex → boss (NPT tapped) → end cap → SHS bore
# Boss provides 15mm thread engagement for 1/2" NPT (cap alone is too thin).
# ─────────────────────────────────────────────────────────────────────────────
ax_d = fig.add_subplot(gs[1, 0])
ax_d.set_facecolor(C_BG)
ax_d.axis("off")

d_xl, d_xr = -44, 50
d_yb, d_yt = -26, 26
ax_d.set_xlim(d_xl, d_xr)
ax_d.set_ylim(d_yb, d_yt)

ax_d.text((d_xl + d_xr) / 2, d_yt - 1,
          "DETAIL A — END CAP WATER CONNECTION",
          ha="center", va="top", fontsize=8, color="#CC0000",
          fontweight="bold", **FONT, zorder=20)
ax_d.text((d_xl + d_xr) / 2, d_yt - 5,
          "(LONGITUDINAL SECTION THROUGH BEAM CENTER — SCALE 2:1)",
          ha="center", va="top", fontsize=5, color=C_DIM,
          **FONT, zorder=20)

C_BRASS = "#C0A860"
C_WASHER = "#5A3020"

# ── Water in bore (right of cap, between SHS walls) ──────────────────────
ax_d.add_patch(Rectangle((20, -17), d_xr - 20, 34,
               fc=C_WATER, ec="none", alpha=0.15, zorder=1))

# ── SHS top wall — cut section, hatched ──────────────────────────────────
ax_d.add_patch(Rectangle((20, 17), d_xr - 20, 3,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=3))

# ── SHS bottom wall — cut section, hatched ───────────────────────────────
ax_d.add_patch(Rectangle((20, -20), d_xr - 20, 3,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=3))

# ── End cap plate (X=15–20, full SHS height except fitting hole) ─────────
ax_d.add_patch(Rectangle((15, 10.5), 5, 9.5,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.2, hatch="///", zorder=4))
ax_d.add_patch(Rectangle((15, -20), 5, 9.5,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.2, hatch="///", zorder=4))

# ── Boss welded to outside of cap (15mm deep, 30mm OD → Y=±15) ──────────
ax_d.add_patch(Rectangle((0, 10.5), 15, 4.5,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=4))
ax_d.add_patch(Rectangle((0, -15), 15, 4.5,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=4))

# Weld symbols at boss-to-cap joint
for wy in [15, -15]:
    ax_d.plot([14.5, 15.5], [wy - 1.5, wy + 1.5],
              color=C_FRAME, lw=1.2, zorder=6)
    ax_d.plot([14.5, 15.5], [wy + 1.5, wy - 1.5],
              color=C_FRAME, lw=1.2, zorder=6)

# ── Fitting hex shoulder (X=-3 to 0, seats against boss face) ────────────
ax_d.add_patch(Rectangle((-3, -12), 3, 24,
               fc=C_BRASS, ec=C_FRAME, lw=1.2, zorder=5))

# ── Fitting threaded body through boss+cap (X=0 to 20) ──────────────────
ax_d.add_patch(Rectangle((0, 6.5), 20, 4,
               fc=C_BRASS, ec=C_FRAME, lw=0.8, zorder=5))
ax_d.add_patch(Rectangle((0, -10.5), 20, 4,
               fc=C_BRASS, ec=C_FRAME, lw=0.8, zorder=5))

# ── NPT thread crests (zigzag on fitting OD) ────────────────────────────
for i in range(10):
    tx = 0.5 + i * 2.0
    if tx + 2.0 > 20:
        break
    ax_d.plot([tx, tx + 1.0, tx + 2.0], [10.5, 11.8, 10.5],
              color=C_FRAME, lw=0.6, zorder=6)
    ax_d.plot([tx, tx + 1.0, tx + 2.0], [-10.5, -11.8, -10.5],
              color=C_FRAME, lw=0.6, zorder=6)

# ── PTFE tape on threads (thin white band) ───────────────────────────────
ax_d.plot([1, 19], [11.0, 11.0], color="white", lw=1.5, alpha=0.7, zorder=5.8)
ax_d.plot([1, 19], [-11.0, -11.0], color="white", lw=1.5, alpha=0.7, zorder=5.8)

# ── Fitting through-bore (water path, 13mm ID → Y=±6.5) ─────────────────
ax_d.add_patch(Rectangle((-3, -6.5), 25, 13,
               fc=C_WATER, ec="none", alpha=0.12, zorder=5.5))

# ── Fitting tip protrusion into bore (X=20–22) ──────────────────────────
ax_d.add_patch(Rectangle((20, -8), 2, 16,
               fc=C_BRASS, ec=C_FRAME, lw=0.5, alpha=0.4, zorder=5))

# ── Hose barb: stepped profile extending from hex (brass) ───────────────
for bx, by, bw, bh in [(-8, -7, 5, 14), (-14, -6.5, 6, 13), (-21, -6, 7, 12)]:
    ax_d.add_patch(Rectangle((bx, by), bw, bh,
                   fc=C_BRASS, ec=C_FRAME, lw=0.7, zorder=5))

# Barb through-bore
ax_d.add_patch(Rectangle((-21, -4.5), 18, 9,
               fc=C_WATER, ec="none", alpha=0.08, zorder=5.5))

# ── Flex hose over barb (1/2" ID ≈ 13mm, 3mm wall → 19mm OD) ────────────
ax_d.add_patch(Rectangle((-40, 6), 32, 3.5,
               fc=C_HOSE, ec=C_FRAME, lw=0.8, alpha=0.5, zorder=4))
ax_d.add_patch(Rectangle((-40, -9.5), 32, 3.5,
               fc=C_HOSE, ec=C_FRAME, lw=0.8, alpha=0.5, zorder=4))
ax_d.plot([-40, -40], [-9.5, 9.5], color=C_FRAME, lw=0.8, zorder=4)

# ── Worm-drive hose clamp ────────────────────────────────────────────────
clamp_x, clamp_w = -26, 6
ax_d.add_patch(Rectangle((clamp_x, -10.5), clamp_w, 21,
               fc="none", ec="#666666", lw=2.0, zorder=6))
ax_d.add_patch(Rectangle((clamp_x + 1.5, 10.5), clamp_w - 3, 2,
               fc="#A0A0A8", ec=C_FRAME, lw=0.5, zorder=6))

# ── Flow direction arrow ─────────────────────────────────────────────────
ax_d.annotate("", xy=(d_xr - 3, 0), xytext=(d_xr - 12, 0),
              arrowprops=dict(arrowstyle="-|>", color=C_WATER, lw=2.0),
              zorder=15)
ax_d.text(d_xr - 7, 3, "WATER", ha="center", va="bottom",
          fontsize=5, color=C_WATER, fontweight="bold", **FONT, zorder=15)

# ── Labels ────────────────────────────────────────────────────────────────
leader(ax_d, 7.5, 15, -8, d_yt - 9,
       "6061-T6 AL BOSS\n(TIG WELDED TO CAP,\n1/2\" NPT TAPPED)",
       fs=5, color=C_FRAME, font=FONT, zorder=20)

leader(ax_d, 17.5, 15, 35, d_yt - 9,
       "5mm AL END CAP\n(TIG WELDED TO SHS)",
       fs=5, color=C_FRAME, font=FONT, zorder=20)

leader(ax_d, -5, -12, -15, d_yb + 4,
       "1/2\" NPT BRASS\nHOSE-BARB FITTING",
       fs=5, color="#8B6914", font=FONT, zorder=20)

ax_d.text(-35, 12, "1/2\" REINFORCED\nPVC FLEX HOSE", ha="center", va="bottom",
          fontsize=5, color=C_HOSE, **FONT, zorder=20)

ax_d.text(clamp_x + clamp_w / 2, 15, "SS WORM-DRIVE\nHOSE CLAMP",
          ha="center", va="bottom", fontsize=4.5, color="#666666",
          **FONT, zorder=20)

ax_d.text(10, 13.5, "PTFE TAPE\nON THREADS",
          ha="center", va="bottom", fontsize=4.5, color="#999999",
          style="italic", **FONT, zorder=20)

# ── Dimensions ────────────────────────────────────────────────────────────
draw_dim_h(ax_d, 0, 20, d_yb + 4,
           "20mm (15mm BOSS + 5mm CAP)",
           offset=3, fs=5, font=FONT)

draw_dim_v(ax_d, d_xr - 8, 17, 20,
           "3mm", offset=3, fs=4.5, font=FONT, right=True)

draw_dim_v(ax_d, d_xr - 3, -17, 17,
           "34mm\nBORE", offset=4, fs=5, font=FONT, right=True)

draw_dim_v(ax_d, d_xl + 6, -9.5, 9.5,
           "19mm\nHOSE OD", offset=4, fs=4.5, font=FONT)


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
# Lollipop silhouette — matches hinge-panel Sheet 3 (light-trap design)
C_PERSON  = "#2060A0"
C_HEAD_FC = "#70A8D8"
C_HEAD_EC = "#1A4D80"
PERSON_H  = 1780
HEAD_R    = 80

op_yd = 170
op_foot_z = GRATE_Z_TOP  # 100mm (standing on deck)
P_body_top = op_foot_z + PERSON_H       # 1880mm
P_head_cz  = P_body_top + HEAD_R        # 1960mm

# Body line
ax2.plot([dy(op_yd), dy(op_yd)],
         [dz(op_foot_z), dz(P_body_top)],
         color=C_PERSON, lw=3.0, zorder=8, solid_capstyle="round")

# Head circle
ax2.add_patch(Circle((dy(op_yd), dz(P_head_cz)),
                       HEAD_R / SC2_V,
                       fc=C_HEAD_FC, ec=C_HEAD_EC, lw=1.0, zorder=8))

# Label
ax2.text(dy(op_yd - 40), dz(op_foot_z + PERSON_H / 2),
         f"{PERSON_H}mm\nOPERATOR\n(shoes)",
         ha="right", va="center", fontsize=5.5, color=C_HEAD_EC,
         **FONT, zorder=15)

# Pole grip point (on body line at chest height)
hand_yd = op_yd
hand_z = op_foot_z + 1100

# ── Telescoping push pole (item 4: show attachment) ──────────────────────
# Pole from operator grip to beam center
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


# ─────────────────────────────────────────────────────────────────────────────
# BOTTOM-RIGHT PANEL — Detail B: Carriage end view
# Yd-Z cross-section looking along X at one carriage.
# Uniform 1:2 scale.  Shows both wheels, fork brackets, L-bracket,
# beam/spray-pipe SHS cross-section, walkway grating above.
# ─────────────────────────────────────────────────────────────────────────────
ax_c = fig.add_subplot(gs[1, 1])
ax_c.set_facecolor(C_BG)
ax_c.set_aspect("equal")
ax_c.axis("off")

SC_C = 2.0

def cy(yd_mm):
    return 3.0 + yd_mm / SC_C

def cz(z_mm):
    return 2.0 + z_mm / SC_C

carriage_yd_center = 200
wheel1_yd = carriage_yd_center - WHEEL_SPACING_YD / 2   # 100mm
wheel2_yd = carriage_yd_center + WHEEL_SPACING_YD / 2   # 300mm

C_YD_LO = wheel1_yd - 80
C_YD_HI = wheel2_yd + 100
C_Z_LO  = -20
C_Z_HI  = GRATE_Z_TOP + 40

ax_c.set_xlim(cy(C_YD_LO), cy(C_YD_HI))
ax_c.set_ylim(cz(C_Z_LO), cz(C_Z_HI))

# Title
ax_c.text(cy((C_YD_LO + C_YD_HI) / 2), cz(C_Z_HI + 2),
          "DETAIL B — CARRIAGE END VIEW",
          ha="center", va="bottom", fontsize=8, color="#0066AA",
          fontweight="bold", **FONT, zorder=15)
ax_c.text(cy((C_YD_LO + C_YD_HI) / 2), cz(C_Z_HI - 6),
          "(LOOKING ALONG X — SECTION THROUGH LEFT WALKWAY — SCALE 1:2)",
          ha="center", va="top", fontsize=5, color=C_DIM,
          **FONT, zorder=15)

# ── Container floor ──────────────────────────────────────────────────────
ax_c.plot([cy(C_YD_LO), cy(C_YD_HI)], [cz(0), cz(0)],
          color=C_OUT, lw=2.0, zorder=3)
ax_c.add_patch(Rectangle((cy(C_YD_LO), cz(-15)),
                           (C_YD_HI - C_YD_LO) / SC_C, 15 / SC_C,
                           fc="#E0E0D8", ec=C_OUT, lw=0.8, hatch="...", zorder=1))

# ── Tray floor ───────────────────────────────────────────────────────────
ax_c.add_patch(Rectangle((cy(C_YD_LO + 5), cz(0)),
                           (C_YD_HI - C_YD_LO - 10) / SC_C, TRAY_FLOOR_Z / SC_C,
                           fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))

# ── Walkway grating ─────────────────────────────────────────────────────
ax_c.add_patch(Rectangle((cy(C_YD_LO + 5), cz(GRATE_Z_BOT)),
                           (C_YD_HI - C_YD_LO - 10) / SC_C, WALKWAY_GRATE_T / SC_C,
                           fc=C_GRATE, ec=C_OUT, lw=2.0, zorder=10))
for frac in np.linspace(0.08, 0.92, 8):
    mesh_yd = C_YD_LO + 5 + (C_YD_HI - C_YD_LO - 10) * frac
    ax_c.plot([cy(mesh_yd), cy(mesh_yd)], [cz(GRATE_Z_BOT), cz(GRATE_Z_TOP)],
              color="#888888", lw=0.5, zorder=10)

ax_c.text(cy((C_YD_LO + C_YD_HI) / 2), cz(GRATE_Z_BOT - 4),
          f"WALKWAY GRATING ({WALKWAY_GRATE_T}mm)",
          ha="center", va="top", fontsize=5, color=C_GRATE, **FONT, zorder=12)

# ── Wheels (2× Ø50mm nylon) ─────────────────────────────────────────────
for w_yd in [wheel1_yd, wheel2_yd]:
    ax_c.add_patch(Circle((cy(w_yd), cz(WHEEL_AXLE_Z)),
                            WHEEL_DIA / 2 / SC_C,
                            fc=C_NYLON, ec=C_WHEEL, lw=2.0, zorder=6))
    ax_c.add_patch(Circle((cy(w_yd), cz(WHEEL_AXLE_Z)),
                            3 / SC_C, fc=C_WHEEL, ec=C_OUT, lw=0.5, zorder=6.5))
    # Contact patch on tray floor
    ax_c.plot([cy(w_yd - WHEEL_WIDTH / 2), cy(w_yd + WHEEL_WIDTH / 2)],
              [cz(TRAY_FLOOR_Z), cz(TRAY_FLOOR_Z)],
              color=C_WHEEL, lw=2.0, zorder=5)

leader(ax_c, cy(wheel1_yd - WHEEL_DIA / 2), cz(WHEEL_AXLE_Z),
       cy(wheel1_yd - WHEEL_DIA / 2 - 35), cz(WHEEL_AXLE_Z - 12),
       f"Ø{WHEEL_DIA}mm\nNYLON WHEEL",
       fs=5, color=C_WHEEL, font=FONT, zorder=15)

# ── Fork brackets (vertical plates straddling each wheel) ────────────────
for w_yd in [wheel1_yd, wheel2_yd]:
    for offset in [-WHEEL_WIDTH / 2 - 2, WHEEL_WIDTH / 2 + 2]:
        ax_c.plot([cy(w_yd + offset), cy(w_yd + offset)],
                  [cz(WHEEL_AXLE_Z + 6), cz(WHEEL_AXLE_Z - WHEEL_DIA / 2 + 4)],
                  color=C_FRAME, lw=1.2, zorder=5.5)
    # Axle pin
    ax_c.plot([cy(w_yd - WHEEL_WIDTH / 2 - 4), cy(w_yd + WHEEL_WIDTH / 2 + 4)],
              [cz(WHEEL_AXLE_Z), cz(WHEEL_AXLE_Z)],
              color=C_FRAME, lw=0.8, zorder=6.5)

# ── L-bracket ────────────────────────────────────────────────────────────
brk_t_c = 5
plate_yd_l = wheel1_yd - 18
plate_yd_r = wheel2_yd + 18

# Horizontal arm at axle height
ax_c.add_patch(Rectangle((cy(plate_yd_l), cz(WHEEL_AXLE_Z - brk_t_c / 2)),
                           (plate_yd_r - plate_yd_l) / SC_C, brk_t_c / SC_C,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=7))

# Vertical drops flanking beam
for side_yd in [carriage_yd_center - BEAM_W / 2 - brk_t_c,
                carriage_yd_center + BEAM_W / 2]:
    ax_c.add_patch(Rectangle((cy(side_yd), cz(BEAM_Z_BOT)),
                               brk_t_c / SC_C,
                               (WHEEL_AXLE_Z - BEAM_Z_BOT + brk_t_c / 2) / SC_C,
                               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, zorder=7))

leader(ax_c, cy(plate_yd_r), cz(WHEEL_AXLE_Z),
       cy(plate_yd_r + 40), cz(WHEEL_AXLE_Z + 10),
       "AL L-BRACKET\n(DROPS BEAM\nBELOW AXLE)",
       fs=5, color=C_FRAME, font=FONT, zorder=15)

# ── Beam / spray pipe SHS cross-section ──────────────────────────────────
c_beam_l = carriage_yd_center - BEAM_W / 2
c_beam_r = carriage_yd_center + BEAM_W / 2

ax_c.add_patch(Rectangle((cy(c_beam_l), cz(BEAM_Z_BOT)),
                           BEAM_W / SC_C, BEAM_W / SC_C,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=2.5, zorder=8))
ax_c.add_patch(Rectangle((cy(carriage_yd_center - BEAM_BORE / 2),
                            cz(BEAM_Z_BOT + BEAM_T)),
                           BEAM_BORE / SC_C, BEAM_BORE / SC_C,
                           fc=C_WATER, ec=C_FRAME, lw=0.8, alpha=0.35, zorder=8.5))

ax_c.text(cy(carriage_yd_center), cz(BEAM_Z_TOP + 5),
          "40×40×3mm\n6061-T6 AL SHS\n(SPRAY PIPE)",
          ha="center", va="bottom", fontsize=5.5, color=C_FRAME,
          fontweight="bold", **FONT, zorder=15)

# Spray hole at bottom
ax_c.add_patch(Rectangle((cy(carriage_yd_center - 1.5), cz(BEAM_Z_BOT - 0.5)),
                           3 / SC_C, (BEAM_T + 1) / SC_C,
                           fc=C_WATER, ec=C_FRAME, lw=0.5, zorder=9))
ax_c.plot([cy(carriage_yd_center), cy(carriage_yd_center)],
          [cz(BEAM_Z_BOT - 1), cz(BEAM_Z_BOT - 16)],
          color=C_WATER, lw=1.2, alpha=0.6, zorder=6)
ax_c.text(cy(carriage_yd_center + 8), cz(BEAM_Z_BOT - 10),
          f"3mm SPRAY HOLE\n(TYP. @{SPRAY_BAR_HOLE_SP}mm c/c)",
          ha="left", va="center", fontsize=4.5, color=C_WATER, **FONT, zorder=15)

# ── Dimensions ───────────────────────────────────────────────────────────
draw_dim_v(ax_c, cy(c_beam_l - 12), cz(BEAM_Z_BOT), cz(BEAM_Z_TOP),
           f"{BEAM_W}mm", offset=8 / SC_C, fs=5.5, font=FONT)

draw_dim_h(ax_c, cy(wheel1_yd), cy(wheel2_yd),
           cz(TRAY_FLOOR_Z + WHEEL_DIA + 8),
           f"{WHEEL_SPACING_YD}mm WHEEL SPACING",
           offset=8 / SC_C, fs=5, font=FONT)

clearance_c = GRATE_Z_BOT - BEAM_Z_TOP
draw_dim_v(ax_c, cy(c_beam_r + 12), cz(BEAM_Z_TOP), cz(GRATE_Z_BOT),
           f"{clearance_c:.0f}mm\nCLR", offset=8 / SC_C, fs=5, font=FONT, right=True)

draw_dim_v(ax_c, cy(c_beam_l - 25), cz(TRAY_FLOOR_Z), cz(BEAM_Z_BOT),
           f"{BEAM_Z_BOT - TRAY_FLOOR_Z:.0f}mm\nSPRAY",
           offset=8 / SC_C, fs=4.5, font=FONT)

draw_dim_v(ax_c, cy(wheel2_yd + WHEEL_DIA / 2 + 8),
           cz(TRAY_FLOOR_Z), cz(TRAY_FLOOR_Z + WHEEL_DIA),
           f"Ø{WHEEL_DIA}mm", offset=8 / SC_C, fs=5, font=FONT, right=True)

# ── Detail C callout on Detail B ─────────────────────────────────────────
ax_c.add_patch(Circle((cy(wheel1_yd), cz(WHEEL_AXLE_Z)),
                        (WHEEL_DIA / 2 + 8) / SC_C,
                        fc="none", ec="#008800", lw=1.5, ls="--", zorder=20))
ax_c.text(cy(wheel1_yd), cz(WHEEL_AXLE_Z + WHEEL_DIA / 2 + 10),
          "C", ha="center", va="bottom", fontsize=9, color="#008800",
          fontweight="bold", **FONT, zorder=20)


# ─────────────────────────────────────────────────────────────────────────────
# DETAIL C INSET — Wheel attachment (section along axle centerline)
# Shows fork bracket arms, nylon wheel bore, axle pin, snap-ring retention,
# and connection to L-bracket horizontal arm.
# ─────────────────────────────────────────────────────────────────────────────
ax_w = fig.add_subplot(gs[2, 0])
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

# Section coordinates: X along axle, Y vertical (mm)
# Axle center at origin.
#   Fork arms:  X = -15..-11 (left),  +11..+15 (right), 4mm thick
#   Wheel:      X = -10..+10, Ø50mm → Y = -25..+25
#   Axle pin:   X = -17..+17, Ø10mm → Y = -5..+5
#   L-bracket:  Y = +13..+18 (5mm arm above fork tops)

C_NYLON_FILL = "#E8DCC0"

# ── L-bracket horizontal arm (cut — hatched) ─────────────────────────────
ax_w.add_patch(Rectangle((-15, 13), 30, 5,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=3))

# ── Left fork arm (cut — hatched) ────────────────────────────────────────
ax_w.add_patch(Rectangle((-15, -13), 4, 26,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=4))

# ── Right fork arm (cut — hatched) ───────────────────────────────────────
ax_w.add_patch(Rectangle((11, -13), 4, 26,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=4))

# ── Nylon wheel body (cut — dot hatch) ───────────────────────────────────
ax_w.add_patch(Rectangle((-10, -25), 20, 50,
               fc=C_NYLON_FILL, ec=C_WHEEL, lw=1.5, hatch="...", zorder=3))

# ── Clearance gaps fork ↔ wheel (1mm each side) ─────────────────────────
for gap_x in [-11, 10]:
    ax_w.add_patch(Rectangle((gap_x, -13), 1, 26,
                   fc=C_BG, ec="none", zorder=3.5))

# ── Axle pin (not cut — solid fill, passes through) ─────────────────────
ax_w.add_patch(Rectangle((-17, -5), 34, 10,
               fc="#D0D0D8", ec=C_FRAME, lw=1.0, zorder=5))

# Clear bore through wheel (axle sits in this)
ax_w.add_patch(Rectangle((-10, -5), 20, 10,
               fc="#D0D0D8", ec="none", zorder=5))

# ── Snap rings at axle ends (retain axle in fork) ────────────────────────
for sr_x in [-17, 15.5]:
    ax_w.add_patch(Rectangle((sr_x, -7), 1.5, 2,
                   fc="#888888", ec=C_FRAME, lw=0.8, zorder=6))
    ax_w.add_patch(Rectangle((sr_x, 5), 1.5, 2,
                   fc="#888888", ec=C_FRAME, lw=0.8, zorder=6))

_bbox_w = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.85)

# ── Tray floor reference ─────────────────────────────────────────────────
ax_w.plot([w_xl, w_xr], [-25, -25],
          color=C_TRAY, lw=1.0, ls="--", zorder=2)
ax_w.text(w_xr - 1, -26, "TRAY FLOOR",
          ha="right", va="top", fontsize=5, color=C_DIM,
          style="italic", bbox=_bbox_w, **FONT, zorder=15)

# ── Labels ────────────────────────────────────────────────────────────────

leader(ax_w, 13, 16, w_xr - 1, w_yt - 8,
       "L-BRACKET\nHORIZ. ARM\n(5mm AL)",
       fs=5.5, color=C_FRAME, font=FONT, zorder=20, bbox=_bbox_w)

leader(ax_w, 13, 0, w_xr - 1, -10,
       "4mm AL\nFORK ARM",
       fs=5.5, color=C_FRAME, font=FONT, zorder=20, bbox=_bbox_w)

ax_w.text(0, -18, "Ø50mm NYLON\nWHEEL (CUT)",
          ha="center", va="top", fontsize=5.5, color=C_WHEEL,
          bbox=_bbox_w, **FONT, zorder=20)

leader(ax_w, 5, 5, 5, 10,
       "Ø10mm SS\nAXLE PIN",
       fs=5.5, color="#888888", font=FONT, zorder=20, bbox=_bbox_w)

ax_w.text(-17.5, -10, "SNAP\nRING",
          ha="center", va="top", fontsize=5, color="#666666",
          bbox=_bbox_w, **FONT, zorder=20)

# ── Dimensions ────────────────────────────────────────────────────────────
draw_dim_h(ax_w, -10, 10, w_yb + 3,
           "20mm", offset=2, fs=5.5, font=FONT)

draw_dim_v(ax_w, w_xl + 2, -5, 5,
           "Ø10", offset=2, fs=5, font=FONT)


# ── Full-width title block ────────────────────────────────────────────────
ax_tb = fig.add_axes([0.05, 0.005, 0.90, 0.04])
title_block(ax_tb, "SHEET 1 OF 1",
            drawing_title="SPRAY BAR ASSEMBLY",
            subtitle="GANTRY SPRAY BAR — ELEVATION, CROSS SECTION & DETAILS",
            scale_note="MULTIPLE SCALES — ALL DIMS IN mm",
            height=0.75)

# ── Save ──────────────────────────────────────────────────────────────────
os.makedirs("diagrams", exist_ok=True)
fig.savefig("diagrams/spray-bar-sheet1.png", dpi=150, bbox_inches="tight", facecolor=C_BG)
fig.savefig(svg_path("diagrams/spray-bar-sheet1.png"), bbox_inches="tight", facecolor=C_BG)
plt.close(fig)
print("  diagrams/spray-bar-sheet1.png saved")
