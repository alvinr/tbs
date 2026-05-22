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
    C_LEN, C_WID,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_W,
    PROC_TRAY_D, PROC_TRAY_RIM, PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR,
    WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T,
    WALKWAY_LEFT_X, WALKWAY_RIGHT_X, WALKWAY_FAR_YD,
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

# PVC pipe inside beam (1" Sch 40)
PVC_OD = 33.4
PVC_ID = 26.6
PVC_WALL = (PVC_OD - PVC_ID) / 2  # 3.4mm
C_PVC = "#B8B8C8"
APERTURE_DIA = 12  # beam aperture hole diameter (mm)

# U-clamp dimensions
UC_T = 3   # clamp material thickness (mm)
UC_GAP = 1  # clearance between clamp and beam (mm)
C_UCLAMP = "#D0D0D8"
C_BOLT = "#808088"
UC_FLARE = 12  # flare extension beyond beam on each side (mm)

GRATE_Z_BOT = WALKWAY_H - WALKWAY_GRATE_T  # 75mm
GRATE_Z_TOP = WALKWAY_H                     # 100mm

BEAM_SPAN = PROC_OPEN_X_R - PROC_OPEN_X_L  # 3,859mm

CARRIAGE_X_L = WALKWAY_LEFT_X + WALKWAY_W / 2    # ≈ 320mm

WALL_T = 3

# ═════════════════════════════════════════════════════════════════════════════
# SHEET 1
# ═════════════════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(28, 32))
fig.patch.set_facecolor(C_BG)
gs = GridSpec(4, 2, figure=fig, width_ratios=[1, 1.3],
              height_ratios=[2.5, 1, 1, 1],
              wspace=0.06, hspace=0.08, bottom=0.035, top=0.97)

# ─────────────────────────────────────────────────────────────────────────────
# RIGHT PANEL — X-Z elevation looking along Yd, left carriage area
# Horizontal 1:6, Vertical 1:2.5 (2.4× vertical exaggeration)
# ─────────────────────────────────────────────────────────────────────────────
ax = fig.add_subplot(gs[0, 1])
ax.set_facecolor(C_BG)
ax.axis("off")

H_SC = 6.0
V_SC = 2.5

def sx(x_mm):
    return 1.0 + x_mm / H_SC

def sz(z_mm):
    return 1.0 + z_mm / V_SC

X_LO = -80
X_HI = 1100
Z_LO = -50
Z_HI = 1050

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

# Walkway slit (for structural arm to pass through, runs in Yd)
SLIT_WIDTH = 30  # mm width of slit in grating
slit_x_ctr = CARRIAGE_X_L  # slit at carriage X position
ax.add_patch(Rectangle((sx(slit_x_ctr - SLIT_WIDTH / 2), sz(GRATE_Z_BOT)),
                         SLIT_WIDTH / H_SC, WALKWAY_GRATE_T / V_SC,
                         fc=C_BG, ec=C_FRAME, lw=0.8, zorder=8.5))
leader(ax, sx(slit_x_ctr), sz(GRATE_Z_TOP),
       sx(slit_x_ctr + 60), sz(GRATE_Z_TOP + 20),
       f"{SLIT_WIDTH}mm SLIT\n(BOTH WALKWAYS)",
       fs=4.5, color=C_FRAME, font=FONT, zorder=15)

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

# L-bracket: horizontal arm at axle height + U-clamp over beam
brk_t = 5   # bracket thickness (visual)
brk_x_l = carriage_cx - 20
brk_x_r = PROC_OPEN_X_L + 5

# Horizontal arm (at axle height, under walkway — extends under beam)
ax.add_patch(Rectangle((sx(brk_x_l), sz(WHEEL_AXLE_Z - brk_t / 2)),
                         (brk_x_r - brk_x_l) / H_SC, brk_t / V_SC,
                         fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=7))
# U-clamp over beam (profile view: top plate + flared legs)
uc_elev_l = brk_x_r - BEAM_W / 2 - UC_T - UC_GAP
uc_elev_r = brk_x_r + BEAM_W / 2 + UC_GAP + UC_T
# Top plate
ax.add_patch(Rectangle((sx(uc_elev_l), sz(BEAM_Z_TOP)),
                         (uc_elev_r - uc_elev_l) / H_SC, UC_T / V_SC,
                         fc=C_UCLAMP, ec=C_FRAME, lw=1.0, zorder=10))
# Side legs (straight portion)
for u_x in [uc_elev_l, uc_elev_r - UC_T]:
    ax.add_patch(Rectangle((sx(u_x), sz(BEAM_Z_BOT + UC_T)),
                             UC_T / H_SC, (BEAM_Z_TOP - BEAM_Z_BOT - UC_T) / V_SC,
                             fc=C_UCLAMP, ec=C_FRAME, lw=0.8, zorder=10))
# Flared feet
ax.add_patch(Rectangle((sx(uc_elev_l - UC_FLARE), sz(BEAM_Z_BOT)),
                         (UC_T + UC_FLARE) / H_SC, UC_T / V_SC,
                         fc=C_UCLAMP, ec=C_FRAME, lw=0.8, zorder=10))
ax.add_patch(Rectangle((sx(uc_elev_r - UC_T), sz(BEAM_Z_BOT)),
                         (UC_T + UC_FLARE) / H_SC, UC_T / V_SC,
                         fc=C_UCLAMP, ec=C_FRAME, lw=0.8, zorder=10))

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
# PVC pipe inside bore (1" Sch 40, OD 33.4mm, ID 26.6mm)
ax.add_patch(Rectangle((sx(beam_x_start + 10), sz(BEAM_Z_BOT + BEAM_T + 0.3)),
                         (beam_x_end - beam_x_start - 20) / H_SC, PVC_OD / V_SC,
                         fc=C_PVC, ec=C_FRAME, lw=0.5, alpha=0.5, zorder=9.3))
# Water inside PVC pipe
ax.add_patch(Rectangle((sx(beam_x_start + 10), sz(BEAM_Z_BOT + BEAM_T + 0.3 + PVC_WALL)),
                         (beam_x_end - beam_x_start - 20) / H_SC, PVC_ID / V_SC,
                         fc=C_WATER, ec="none", lw=0, alpha=0.3, zorder=9.5))

# Beam continuation arrow
arrow_y = sz(BEAM_Z_BOT + BEAM_W / 2)
ax.annotate("", xy=(sx(X_HI - 10), arrow_y),
            xytext=(sx(X_HI - 80), arrow_y),
            arrowprops=dict(arrowstyle="-|>", color=C_FRAME, lw=2.0),
            zorder=15)

ax.text(sx((beam_x_start + beam_x_end) / 2), sz(BEAM_Z_TOP + 12),
        "40×40×3mm 6061-T6 AL SHS — STRUCTURAL BEAM",
        ha="center", va="bottom", fontsize=6.5, color=C_FRAME,
        fontweight="bold", **FONT, zorder=15)
ax.text(sx((beam_x_start + beam_x_end) / 2), sz(BEAM_Z_TOP + 3),
        f"(SPANS {BEAM_SPAN}mm — 1\" PVC PIPE INSIDE, 12mm APERTURES, CENTER FEED)",
        ha="center", va="bottom", fontsize=5, color=C_DIM,
        **FONT, zorder=15)

# ── Spray apertures (12mm in beam, 2mm in PVC pipe) and water droplets ───
n_drops = 6
for i in range(n_drops):
    frac = (i + 0.5) / n_drops
    drop_x = beam_x_start + 40 + (beam_x_end - beam_x_start - 80) * frac
    # 12mm aperture in beam bottom
    ax.plot([sx(drop_x - APERTURE_DIA / 2), sx(drop_x + APERTURE_DIA / 2)],
            [sz(BEAM_Z_BOT), sz(BEAM_Z_BOT)],
            color=C_WATER, lw=2.5, zorder=10)
    # Water jet from pipe through aperture
    ax.plot([sx(drop_x), sx(drop_x)],
            [sz(BEAM_Z_BOT - 1), sz(TRAY_FLOOR_Z + 3)],
            color=C_WATER, lw=0.8, alpha=0.5, zorder=6)
    ax.add_patch(Circle((sx(drop_x), sz(TRAY_FLOOR_Z + 3)),
                          2 / V_SC, fc=C_WATER, ec="none", alpha=0.5, zorder=6))

# Water on tray
ax.add_patch(Rectangle((sx(beam_x_start), sz(TRAY_FLOOR_Z)),
                         (beam_x_end - beam_x_start) / H_SC, 3 / V_SC,
                         fc=C_WATER, ec="none", alpha=0.12, zorder=4.5))

# ── End cap (plain AL plate — PVC pipe sealed inside with PVC cap) ───────
cap_t = 5
ax.add_patch(Rectangle((sx(beam_x_start - cap_t), sz(BEAM_Z_BOT)),
                         cap_t / H_SC, BEAM_W / V_SC,
                         fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=9.5))

leader(ax, sx(beam_x_start - cap_t / 2), sz(BEAM_Z_BOT),
       sx(beam_x_start - 50), sz(BEAM_Z_BOT - 20),
       "AL END CAP\n(PVC PIPE CAPPED\nINSIDE)",
       fs=5, color=C_FRAME, font=FONT, zorder=15)

# ── Blue supply pipe riser on container wall ─────────────────────────────
bv_z = BV02_Z  # 900mm
bv_size = 30
pipe_w = 8

# Vertical pipe riser from floor up to BV-02
pipe_z_bot = 0
pipe_z_top = bv_z - bv_size / 2
ax.add_patch(Rectangle((sx(-pipe_w / 2), sz(pipe_z_bot)),
                         pipe_w / H_SC, (pipe_z_top - pipe_z_bot) / V_SC,
                         fc=C_BLUE, ec=C_FRAME, lw=0.8, alpha=0.4, zorder=11))

# BV-02 ball valve symbol at Z=900
ax.add_patch(Rectangle((sx(-bv_size / 3), sz(bv_z - bv_size / 2)),
                         (bv_size / 3) / H_SC, bv_size / V_SC,
                         fc=C_BLUE, ec=C_FRAME, lw=1.5, alpha=0.6, zorder=12))
# Valve handle
ax.plot([sx(0), sx(-20)], [sz(bv_z), sz(bv_z + 20)],
        color=C_FRAME, lw=2.0, zorder=12)

leader(ax, sx(-15), sz(bv_z + 25),
       sx(-60), sz(bv_z + 60),
       f"BV-02 @ Z={int(bv_z)}mm\n(1/2\" BALL VALVE)\nWAIST HEIGHT",
       fs=5.5, color=C_BLUE, font=FONT, zorder=15)

# ── Flex hose from BV-02 down to beam center feed ────────────────────────
hose_start_x = 15
hose_start_z = bv_z - bv_size / 2
hose_end_x = X_HI - 20
hose_end_z = BEAM_Z_BOT + BEAM_W / 2

n_pts = 80
ht = np.linspace(0, 1, n_pts)
P0 = np.array([hose_start_x, hose_start_z])
P1 = np.array([hose_start_x + 80, hose_start_z - 200])
P2 = np.array([hose_end_x - 300, hose_end_z + 50])
P3 = np.array([hose_end_x, hose_end_z])
hose_xs = (1-ht)**3*P0[0] + 3*(1-ht)**2*ht*P1[0] + 3*(1-ht)*ht**2*P2[0] + ht**3*P3[0]
hose_zs = (1-ht)**3*P0[1] + 3*(1-ht)**2*ht*P1[1] + 3*(1-ht)*ht**2*P2[1] + ht**3*P3[1]
envelope = np.clip(np.minimum(ht, 1 - ht) * 4, 0, 1)
hose_zs += 2.0 * np.sin(np.linspace(0, 12 * np.pi, n_pts)) * envelope

ax.plot([sx(x) for x in hose_xs], [sz(z) for z in hose_zs],
        color=C_HOSE, lw=2.5, alpha=0.7, zorder=11)
# Continuation arrow (hose continues to center feed)
ax.annotate("", xy=(sx(hose_end_x), sz(hose_end_z)),
            xytext=(sx(hose_end_x - 60), sz(hose_end_z)),
            arrowprops=dict(arrowstyle="-|>", color=C_HOSE, lw=1.5),
            zorder=15)

ax.text(sx(hose_start_x + 150), sz(hose_start_z - 100),
        "1/2\" FLEX HOSE → CENTER\nFEED (4m COILED)",
        ha="left", va="top", fontsize=4.5, color=C_HOSE, **FONT, zorder=15)

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
    f"1. 40×40×3mm AL SHS structural beam. 1\" PVC pipe inside carries water.",
    f"2. 12mm apertures in beam, 2mm holes drilled through pipe at each aperture.",
    f"3. Center feed: 1/2\" bulkhead through beam wall at X midpoint.",
    f"4. PVC pipe swappable — change flow rate/nozzles without replacing beam.",
    f"5. U-clamp secures beam to carriage (no beam wall penetration).",
]
draw_notes(ax, notes, sx(X_LO + 250), sz(Z_HI - 25), spacing=5 / V_SC,
           fs=7, font=FONT, width=455 / H_SC)

ax.text(sx((X_LO + X_HI) / 2), sz(Z_HI - 5),
        "GANTRY ELEVATION — VIEW ALONG Yd (LEFT CARRIAGE)",
        ha="center", va="top", fontsize=9, color=C_FRAME,
        fontweight="bold", **FONT, zorder=15)
ax.text(sx((X_LO + X_HI) / 2), sz(Z_HI - 20),
        "(H 1:6 / V 1:1.5 — 4× VERT EXAG — ALL DIMS IN mm)",
        ha="center", va="top", fontsize=5, color=C_DIM,
        **FONT, zorder=15)

ax.text(sx(-30), sz(Z_HI - 40),
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
# Detail A: Beam end cap (longitudinal section)
# Water now feeds at center — end is simply capped (no fitting).
# X: along beam axis, - = outside, + = inside (bore)
# Y: perpendicular to beam axis, 0 = beam centerline
# ─────────────────────────────────────────────────────────────────────────────
ax_a = fig.add_subplot(gs[3, 1])
ax_a.set_facecolor(C_BG)
ax_a.axis("off")

d_xl, d_xr = -15, 50
d_yb, d_yt = -26, 26
ax_a.set_xlim(d_xl, d_xr)
ax_a.set_ylim(d_yb, d_yt)

ax_a.text((d_xl + d_xr) / 2, d_yt - 1,
          "DETAIL A — BEAM END CAP",
          ha="center", va="top", fontsize=8, color="#CC0000",
          fontweight="bold", **FONT, zorder=20)
ax_a.text((d_xl + d_xr) / 2, d_yt - 5,
          "(LONGITUDINAL SECTION — SCALE 2:1)",
          ha="center", va="top", fontsize=5, color=C_DIM,
          **FONT, zorder=20)

_bbox_a = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.85)

# ── SHS top wall — cut section, hatched ──────────────────────────────────
ax_a.add_patch(Rectangle((5, 17), d_xr - 5, 3,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=3))
# ── SHS bottom wall — cut section, hatched ───────────────────────────────
ax_a.add_patch(Rectangle((5, -20), d_xr - 5, 3,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=3))

# ── AL end cap plate (X=0–5, full SHS height, welded to SHS) ────────────
ax_a.add_patch(Rectangle((0, -20), 5, 40,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, hatch="///", zorder=4))
# Weld symbols at cap-to-SHS joint
for wy in [17, -17]:
    ax_a.plot([4.5, 5.5], [wy - 1.5, wy + 1.5],
              color=C_FRAME, lw=1.2, zorder=6)
    ax_a.plot([4.5, 5.5], [wy + 1.5, wy - 1.5],
              color=C_FRAME, lw=1.2, zorder=6)

# ── Square bore ──────────────────────────────────────────────────────────
ax_a.add_patch(Rectangle((5, -17), d_xr - 5, 34,
               fc=C_BG, ec=C_FRAME, lw=0.5, zorder=3.5))

# ── PVC pipe inside bore ─────────────────────────────────────────────────
pvc_od_h = PVC_OD / 2
pvc_id_h = PVC_ID / 2
# PVC pipe walls (top and bottom in section)
ax_a.add_patch(Rectangle((5, pvc_id_h), d_xr - 5, PVC_WALL,
               fc=C_PVC, ec=C_FRAME, lw=0.6, zorder=4))
ax_a.add_patch(Rectangle((5, -pvc_od_h), d_xr - 5, PVC_WALL,
               fc=C_PVC, ec=C_FRAME, lw=0.6, zorder=4))

# PVC end cap (glued)
ax_a.add_patch(Rectangle((5, -pvc_od_h), 4, PVC_OD,
               fc=C_PVC, ec=C_FRAME, lw=0.8, zorder=4.5))

# Water inside PVC pipe
ax_a.add_patch(Rectangle((9, -pvc_id_h), d_xr - 9, PVC_ID,
               fc=C_WATER, ec="none", alpha=0.15, zorder=3.8))

# ── Labels ────────────────────────────────────────────────────────────────
leader(ax_a, 2.5, 15, -5, d_yt - 8,
       "5mm AL END CAP\n(TIG WELDED TO SHS)",
       fs=5, color=C_FRAME, font=FONT, zorder=20, bbox=_bbox_a)

leader(ax_a, 7, pvc_od_h, 25, d_yt - 10,
       "1\" Sch 40 PVC PIPE\n(PVC END CAP GLUED)",
       fs=5, color=C_PVC, font=FONT, zorder=20, bbox=_bbox_a)

ax_a.text(d_xr - 8, 0, "WATER",
          ha="center", va="center", fontsize=5, color=C_WATER,
          fontweight="bold", bbox=_bbox_a, **FONT, zorder=15)

ax_a.text((d_xl + 0) / 2, 0, "NO WATER\nCONNECTION\nAT ENDS",
          ha="center", va="center", fontsize=4.5, color=C_DIM,
          style="italic", bbox=_bbox_a, **FONT, zorder=15)

# ── Dimensions ────────────────────────────────────────────────────────────
draw_dim_h(ax_a, 0, 5, d_yb + 4,
           "5mm CAP", offset=3, fs=5, font=FONT)

draw_dim_v(ax_a, d_xr - 3, -17, 17,
           "34mm\nBORE", offset=4, fs=5, font=FONT, right=True)

draw_dim_v(ax_a, d_xr - 8, 17, 20,
           "3mm\nWALL", offset=3, fs=4.5, font=FONT, right=True)

draw_dim_v(ax_a, d_xl + 3, -pvc_od_h, pvc_od_h,
           f"{PVC_OD:.1f}mm\nPVC OD", offset=3, fs=4.5, font=FONT)


# ─────────────────────────────────────────────────────────────────────────────
# LEFT PANEL — Yd-Z cross section (operator view)
# Looking along X.  Schematic — non-uniform H/V scale.
# Shows: tray, beam, near walkway, operator, telescoping pole.
# ─────────────────────────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 0])
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
R_Z_HI = 2150

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
# PVC pipe inside bore (cross-section circle, shown as rectangle in this view)
ax2.add_patch(Rectangle((dy(beam_yd - PVC_OD / 2), dz(BEAM_Z_BOT + BEAM_T + 0.3)),
                          PVC_OD / SC2_H, PVC_OD / SC2_V,
                          fc=C_PVC, ec=C_FRAME, lw=0.5, alpha=0.5, zorder=9.3))
# Water inside PVC pipe
ax2.add_patch(Rectangle((dy(beam_yd - PVC_ID / 2), dz(BEAM_Z_BOT + BEAM_T + 0.3 + PVC_WALL)),
                          PVC_ID / SC2_H, PVC_ID / SC2_V,
                          fc=C_WATER, ec="none", lw=0, alpha=0.35, zorder=9.5))

ax2.text(dy(beam_yd), dz(BEAM_Z_TOP + 15),
         f"40×40×3mm AL SHS\n+ 1\" PVC PIPE INSIDE", ha="center", va="bottom",
         fontsize=5.5, color=C_FRAME, fontweight="bold", **FONT, zorder=15)

# Center feed fitting (1/2" bulkhead through beam wall — shown at this section)
feed_fit_h = 12
feed_fit_w = 8
ax2.add_patch(Rectangle((dy(beam_yd_r), dz(BEAM_Z_BOT + BEAM_W / 2 - feed_fit_h / 2)),
                          feed_fit_w / SC2_H, feed_fit_h / SC2_V,
                          fc="#C0A860", ec=C_FRAME, lw=0.8, zorder=10))
leader(ax2, dy(beam_yd_r + feed_fit_w), dz(BEAM_Z_BOT + BEAM_W / 2),
       dy(beam_yd_r + 80), dz(BEAM_Z_BOT + BEAM_W / 2 + 20),
       "1/2\" BULKHEAD\nCENTER FEED",
       fs=4.5, color="#C0A860", font=FONT, zorder=15)

# 12mm aperture + spray hole at bottom
ax2.add_patch(Rectangle((dy(beam_yd - APERTURE_DIA / 2), dz(BEAM_Z_BOT - 0.5)),
                          APERTURE_DIA / SC2_H, (BEAM_T + 1) / SC2_V,
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
         f"12mm APERTURE\n2mm PIPE HOLES\n@{SPRAY_BAR_HOLE_SP}mm c/c",
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

# ── Blue supply pipe riser on near wall ──────────────────────────────────
bv2_yd = 10    # BV-02 near wall, on pipe riser
bv2_z = BV02_Z  # 900mm
bv_sz = 25
pipe_w_op = 6

# Vertical pipe from floor to BV-02
ax2.add_patch(Rectangle((dy(bv2_yd - pipe_w_op / 2), dz(0)),
                          pipe_w_op / SC2_H, bv2_z / SC2_V,
                          fc=C_BLUE, ec=C_FRAME, lw=0.8, alpha=0.4, zorder=11))

# BV-02 valve body
ax2.add_patch(Rectangle((dy(bv2_yd - bv_sz / 2), dz(bv2_z - bv_sz / 2)),
                          bv_sz / SC2_H, bv_sz / SC2_V,
                          fc=C_BLUE, ec=C_FRAME, lw=1.5, alpha=0.6, zorder=12))
# Valve handle
ax2.plot([dy(bv2_yd), dy(bv2_yd + 15)],
         [dz(bv2_z), dz(bv2_z + 15)],
         color=C_FRAME, lw=2.0, zorder=12)

ax2.text(dy(bv2_yd + 20), dz(bv2_z + 20),
         f"BV-02 @ Z={int(bv2_z)}mm\n(WAIST HEIGHT)",
         ha="left", va="bottom",
         fontsize=5, color=C_BLUE, fontweight="bold", **FONT, zorder=15)

# Flex hose from BV-02 drooping down to beam center feed
hose_n = 60
ht2 = np.linspace(0, 1, hose_n)
H0 = np.array([bv2_yd + bv_sz / 2, bv2_z])
H1 = np.array([bv2_yd + 100, bv2_z - 300])
H2 = np.array([beam_yd - 100, BEAM_Z_BOT + BEAM_W + 50])
H3 = np.array([beam_yd_r + feed_fit_w, BEAM_Z_BOT + BEAM_W / 2])
hose_yd = (1-ht2)**3*H0[0] + 3*(1-ht2)**2*ht2*H1[0] + 3*(1-ht2)*ht2**2*H2[0] + ht2**3*H3[0]
hose_zz = (1-ht2)**3*H0[1] + 3*(1-ht2)**2*ht2*H1[1] + 3*(1-ht2)*ht2**2*H2[1] + ht2**3*H3[1]
env2 = np.clip(np.minimum(ht2, 1 - ht2) * 4, 0, 1)
hose_zz += 2.0 * np.sin(np.linspace(0, 10 * np.pi, hose_n)) * env2

ax2.plot([dy(y) for y in hose_yd], [dz(z) for z in hose_zz],
         color=C_HOSE, lw=2.0, alpha=0.6, zorder=11)
ax2.text(dy(bv2_yd + 60), dz(bv2_z - 150),
         "1/2\" FLEX HOSE\n(4m COILED)",
         ha="left", va="top", fontsize=4.5, color=C_HOSE, **FONT, zorder=15)

# ── Carriage wheels under walkway (2× Ø50mm nylon) ──────────────────────
carriage_ctr_yd = beam_yd
cw1_yd = carriage_ctr_yd - WHEEL_SPACING_YD / 2
cw2_yd = carriage_ctr_yd + WHEEL_SPACING_YD / 2

for cw_yd in [cw1_yd, cw2_yd]:
    ax2.add_patch(Circle((dy(cw_yd), dz(WHEEL_AXLE_Z)),
                            WHEEL_DIA / 2 / SC2_V,
                            fc=C_NYLON, ec=C_WHEEL, lw=1.5, zorder=6))
    ax2.add_patch(Circle((dy(cw_yd), dz(WHEEL_AXLE_Z)),
                            1.5 / SC2_V, fc=C_WHEEL, ec=C_OUT, lw=0.3, zorder=6.5))
    # Contact patch on tray
    ax2.plot([dy(cw_yd - WHEEL_WIDTH / 2), dy(cw_yd + WHEEL_WIDTH / 2)],
             [dz(TRAY_FLOOR_Z), dz(TRAY_FLOOR_Z)],
             color=C_WHEEL, lw=1.5, zorder=5)
    # Fork brackets straddling each wheel
    for offset in [-WHEEL_WIDTH / 2 - 2, WHEEL_WIDTH / 2 + 2]:
        ax2.plot([dy(cw_yd + offset), dy(cw_yd + offset)],
                 [dz(WHEEL_AXLE_Z + 6), dz(WHEEL_AXLE_Z - WHEEL_DIA / 2 + 4)],
                 color=C_FRAME, lw=0.8, zorder=5.5)
    # Axle pin through wheel
    ax2.plot([dy(cw_yd - WHEEL_WIDTH / 2 - 4), dy(cw_yd + WHEEL_WIDTH / 2 + 4)],
             [dz(WHEEL_AXLE_Z), dz(WHEEL_AXLE_Z)],
             color=C_FRAME, lw=0.5, zorder=6.5)

# L-bracket arm (horizontal plate connecting wheels to beam)
brk_arm_l = cw1_yd - 18
brk_arm_r = cw2_yd + 18
brk_t_op = 5
ax2.add_patch(Rectangle((dy(brk_arm_l), dz(WHEEL_AXLE_Z - brk_t_op / 2)),
                           (brk_arm_r - brk_arm_l) / SC2_H, brk_t_op / SC2_V,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=0.8, zorder=7))

# U-clamp over beam (profile: top plate + flared legs)
uc_l_op = carriage_ctr_yd - BEAM_W / 2 - UC_T - UC_GAP
uc_r_op = carriage_ctr_yd + BEAM_W / 2 + UC_GAP + UC_T
# Top plate
ax2.add_patch(Rectangle((dy(uc_l_op), dz(BEAM_Z_TOP)),
                           (uc_r_op - uc_l_op) / SC2_H, UC_T / SC2_V,
                           fc=C_UCLAMP, ec=C_FRAME, lw=0.6, zorder=10))
# Side legs (straight portion)
for u_yd in [uc_l_op, uc_r_op - UC_T]:
    ax2.add_patch(Rectangle((dy(u_yd), dz(BEAM_Z_BOT + UC_T)),
                               UC_T / SC2_H,
                               (BEAM_Z_TOP - BEAM_Z_BOT - UC_T) / SC2_V,
                               fc=C_UCLAMP, ec=C_FRAME, lw=0.5, zorder=10))
# Flared feet
ax2.add_patch(Rectangle((dy(uc_l_op - UC_FLARE), dz(BEAM_Z_BOT)),
                           (UC_T + UC_FLARE) / SC2_H, UC_T / SC2_V,
                           fc=C_UCLAMP, ec=C_FRAME, lw=0.5, zorder=10))
ax2.add_patch(Rectangle((dy(uc_r_op - UC_T), dz(BEAM_Z_BOT)),
                           (UC_T + UC_FLARE) / SC2_H, UC_T / SC2_V,
                           fc=C_UCLAMP, ec=C_FRAME, lw=0.5, zorder=10))

leader(ax2, dy(cw1_yd), dz(WHEEL_AXLE_Z - WHEEL_DIA / 2 - 8),
       dy(cw1_yd - 50), dz(WHEEL_AXLE_Z - WHEEL_DIA / 2 - 30),
       f"Ø{WHEEL_DIA}mm NYLON WHEELS\n(2 PER CARRIAGE,\nFORK + AXLE PIN)",
       fs=4.5, color=C_WHEEL, font=FONT, zorder=15)

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
    "2. 1\" PVC pipe inside beam carries water. Center feed via bulkhead.",
    "3. U-clamp holds beam to carriage — no beam wall penetration.",
    "4. PVC pipe swappable for different flow rates / nozzle patterns.",
]
draw_notes(ax2, r_notes, dy(R_YD_LO + 400), dz(R_Z_HI - 120), spacing=30 / SC2_V,
           fs=5.5, font=FONT, width=350 / SC2_H)


# ─────────────────────────────────────────────────────────────────────────────
# Detail B: Carriage end view
# Yd-Z cross-section looking along X at one carriage.
# Uniform 1:2 scale.  Shows both wheels, fork brackets, L-bracket,
# beam/spray-pipe SHS cross-section, walkway grating above.
# ─────────────────────────────────────────────────────────────────────────────
ax_c = fig.add_subplot(gs[1, 0])
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

# ── L-bracket (arm only — no drop cheeks) ────────────────────────────────
brk_t_c = 5
plate_yd_l = wheel1_yd - 18
plate_yd_r = wheel2_yd + 18

# Horizontal arm at axle height (beam sits on top of this)
ax_c.add_patch(Rectangle((cy(plate_yd_l), cz(WHEEL_AXLE_Z - brk_t_c / 2)),
                           (plate_yd_r - plate_yd_l) / SC_C, brk_t_c / SC_C,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=7))

leader(ax_c, cy(plate_yd_r), cz(WHEEL_AXLE_Z),
       cy(plate_yd_r + 40), cz(WHEEL_AXLE_Z + 10),
       "AL L-BRACKET\nARM (5mm PLATE)",
       fs=5, color=C_FRAME, font=FONT, zorder=15)

# ── Fork-to-arm M5 through-bolts ────────────────────────────────────────
arm_top_z = WHEEL_AXLE_Z + brk_t_c / 2
arm_bot_z = WHEEL_AXLE_Z - brk_t_c / 2

for w_yd in [wheel1_yd, wheel2_yd]:
    for offset in [-WHEEL_WIDTH / 2 - 2, WHEEL_WIDTH / 2 + 2]:
        fork_yd = w_yd + offset
        ax_c.add_patch(Rectangle((cy(fork_yd - 4), cz(arm_top_z)),
                                   8 / SC_C, 3 / SC_C,
                                   fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=11))
        ax_c.add_patch(Rectangle((cy(fork_yd - 2.5), cz(arm_bot_z)),
                                   5 / SC_C, brk_t_c / SC_C,
                                   fc=C_BOLT, ec=C_FRAME, lw=0.4, zorder=11))
        ax_c.add_patch(Rectangle((cy(fork_yd - 4), cz(arm_bot_z - 4)),
                                   8 / SC_C, 4 / SC_C,
                                   fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=11))

leader(ax_c, cy(wheel2_yd + WHEEL_WIDTH / 2 + 2), cz(WHEEL_AXLE_Z),
       cy(wheel2_yd + 55), cz(WHEEL_AXLE_Z - 20),
       "M5 SS THRU-BOLT\n+ NYLOC NUT\n(1 PER FORK)",
       fs=4.5, color=C_BOLT, font=FONT, zorder=15)

# ── Beam / structural SHS cross-section with PVC pipe inside ────────────
c_beam_l = carriage_yd_center - BEAM_W / 2
c_beam_r = carriage_yd_center + BEAM_W / 2

# AL SHS outer wall
ax_c.add_patch(Rectangle((cy(c_beam_l), cz(BEAM_Z_BOT)),
                           BEAM_W / SC_C, BEAM_W / SC_C,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=2.5, zorder=8))
# Square bore
ax_c.add_patch(Rectangle((cy(carriage_yd_center - BEAM_BORE / 2),
                            cz(BEAM_Z_BOT + BEAM_T)),
                           BEAM_BORE / SC_C, BEAM_BORE / SC_C,
                           fc=C_BG, ec=C_FRAME, lw=0.8, zorder=8.5))
# PVC pipe (circle cross-section inside square bore)
ax_c.add_patch(Circle((cy(carriage_yd_center), cz(BEAM_Z_BOT + BEAM_W / 2)),
                         PVC_OD / 2 / SC_C,
                         fc=C_PVC, ec=C_FRAME, lw=1.0, alpha=0.7, zorder=8.7))
# Water inside PVC pipe
ax_c.add_patch(Circle((cy(carriage_yd_center), cz(BEAM_Z_BOT + BEAM_W / 2)),
                         PVC_ID / 2 / SC_C,
                         fc=C_WATER, ec=C_FRAME, lw=0.5, alpha=0.4, zorder=8.8))

ax_c.text(cy(carriage_yd_center), cz(BEAM_Z_TOP + 5),
          "40×40×3mm AL SHS\n+ 1\" PVC PIPE",
          ha="center", va="bottom", fontsize=5.5, color=C_FRAME,
          fontweight="bold", **FONT, zorder=15)

# ── U-clamp over beam (with flared legs for bolting to arm) ─────────────
uc_l = carriage_yd_center - BEAM_W / 2 - UC_T - UC_GAP
uc_r = carriage_yd_center + BEAM_W / 2 + UC_GAP + UC_T
flare_l = uc_l - UC_FLARE
flare_r = uc_r + UC_FLARE

# Top plate
ax_c.add_patch(Rectangle((cy(uc_l), cz(BEAM_Z_TOP)),
                           (uc_r - uc_l) / SC_C, UC_T / SC_C,
                           fc=C_UCLAMP, ec=C_FRAME, lw=1.0, zorder=10))
# Left leg (straight portion down beam side)
ax_c.add_patch(Rectangle((cy(uc_l), cz(BEAM_Z_BOT + UC_T)),
                           UC_T / SC_C, (BEAM_Z_TOP - BEAM_Z_BOT - UC_T) / SC_C,
                           fc=C_UCLAMP, ec=C_FRAME, lw=0.8, zorder=10))
# Right leg (straight portion)
ax_c.add_patch(Rectangle((cy(uc_r - UC_T), cz(BEAM_Z_BOT + UC_T)),
                           UC_T / SC_C, (BEAM_Z_TOP - BEAM_Z_BOT - UC_T) / SC_C,
                           fc=C_UCLAMP, ec=C_FRAME, lw=0.8, zorder=10))
# Left flared foot (extends outward at bottom)
ax_c.add_patch(Rectangle((cy(flare_l), cz(BEAM_Z_BOT)),
                           (uc_l + UC_T - flare_l) / SC_C, UC_T / SC_C,
                           fc=C_UCLAMP, ec=C_FRAME, lw=0.8, zorder=10))
# Right flared foot
ax_c.add_patch(Rectangle((cy(uc_r - UC_T), cz(BEAM_Z_BOT)),
                           (flare_r - uc_r + UC_T) / SC_C, UC_T / SC_C,
                           fc=C_UCLAMP, ec=C_FRAME, lw=0.8, zorder=10))

# Bolts through flared feet + L-bracket arm
for bolt_yd in [flare_l + UC_FLARE / 2, flare_r - UC_FLARE / 2]:
    # Bolt shank through foot + arm
    ax_c.add_patch(Rectangle((cy(bolt_yd - 2.5), cz(arm_bot_z - 4)),
                               5 / SC_C, (BEAM_Z_BOT + UC_T - arm_bot_z + 4) / SC_C,
                               fc=C_BOLT, ec=C_FRAME, lw=0.5, zorder=11))
    # Bolt head on top of foot
    ax_c.add_patch(Rectangle((cy(bolt_yd - 4), cz(BEAM_Z_BOT + UC_T)),
                               8 / SC_C, 3 / SC_C,
                               fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=11))
    # Wing nut below arm
    ax_c.add_patch(Rectangle((cy(bolt_yd - 5), cz(arm_bot_z - 8)),
                               10 / SC_C, 4 / SC_C,
                               fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=11))

leader(ax_c, cy(flare_r), cz(BEAM_Z_BOT + UC_T / 2),
       cy(flare_r + 25), cz(BEAM_Z_BOT - 6),
       "SS U-CLAMP\nFLARED LEGS\n+ WING NUTS",
       fs=4.5, color=C_BOLT, font=FONT, zorder=15)

# 12mm aperture + 2mm spray hole at bottom
ax_c.add_patch(Rectangle((cy(carriage_yd_center - APERTURE_DIA / 2), cz(BEAM_Z_BOT - 0.5)),
                           APERTURE_DIA / SC_C, (BEAM_T + 1) / SC_C,
                           fc=C_BG, ec=C_FRAME, lw=0.5, zorder=9))
# Water jet through aperture
ax_c.plot([cy(carriage_yd_center), cy(carriage_yd_center)],
          [cz(BEAM_Z_BOT - 1), cz(BEAM_Z_BOT - 16)],
          color=C_WATER, lw=1.2, alpha=0.6, zorder=6)
ax_c.text(cy(carriage_yd_center + 8), cz(BEAM_Z_BOT - 10),
          f"12mm APERTURE\n2mm PIPE HOLE\n(TYP. @{SPRAY_BAR_HOLE_SP}mm c/c)",
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
ax_w.add_patch(Rectangle((-17, 13), 34, 5,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=3))

# ── Left fork arm (cut — hatched, 6mm thick for M5 bolts) ───────────────
ax_w.add_patch(Rectangle((-17, -13), 6, 26,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=4))

# ── Right fork arm (cut — hatched, 6mm thick) ───────────────────────────
ax_w.add_patch(Rectangle((11, -13), 6, 26,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=4))

# ── Nylon wheel body (cut — dot hatch) ───────────────────────────────────
ax_w.add_patch(Rectangle((-10, -25), 20, 50,
               fc=C_NYLON_FILL, ec=C_WHEEL, lw=1.5, hatch="...", zorder=3))

# ── Clearance gaps fork ↔ wheel (1mm each side) ─────────────────────────
for gap_x in [-11, 10]:
    ax_w.add_patch(Rectangle((gap_x, -13), 1, 26,
                   fc=C_BG, ec="none", zorder=3.5))

# ── Axle pin (not cut — solid fill, passes through) ─────────────────────
ax_w.add_patch(Rectangle((-20, -5), 40, 10,
               fc="#D0D0D8", ec=C_FRAME, lw=1.0, zorder=5))

# Clear bore through wheel (axle sits in this)
ax_w.add_patch(Rectangle((-10, -5), 20, 10,
               fc="#D0D0D8", ec="none", zorder=5))

# ── Snap rings at axle ends (retain axle in fork) ────────────────────────
for sr_x in [-20, 18.5]:
    ax_w.add_patch(Rectangle((sr_x, -7), 1.5, 2,
                   fc="#888888", ec=C_FRAME, lw=0.8, zorder=6))
    ax_w.add_patch(Rectangle((sr_x, 5), 1.5, 2,
                   fc="#888888", ec=C_FRAME, lw=0.8, zorder=6))

# ── M5 through-bolts: fork-to-arm (profile view) ────────────────────────
C_BOLT_FILL = "#D0D0D8"
for bolt_cx in [-14, 14]:
    # Bolt head (on top of arm)
    ax_w.add_patch(Rectangle((bolt_cx - 4, 18), 8, 3,
                   fc=C_BOLT_FILL, ec=C_FRAME, lw=0.8, zorder=7))
    # Shank through arm and into fork
    ax_w.add_patch(Rectangle((bolt_cx - 2.5, 4), 5, 14,
                   fc=C_BOLT_FILL, ec=C_FRAME, lw=0.6, zorder=7))
    # Nyloc nut below fork
    ax_w.add_patch(Rectangle((bolt_cx - 4, 0), 8, 4,
                   fc=C_BOLT_FILL, ec=C_FRAME, lw=0.8, zorder=7))

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
       "6mm AL\nFORK ARM",
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

leader(ax_w, -14, 20, -6, w_yt - 10,
       "M5×16 SS\nTHRU-BOLT\n+ NYLOC NUT\n(1 PER FORK)",
       fs=5, color="#808088", font=FONT, zorder=20, bbox=_bbox_w)

# ── Dimensions ────────────────────────────────────────────────────────────
draw_dim_h(ax_w, -10, 10, w_yb + 3,
           "20mm", offset=2, fs=5.5, font=FONT)

draw_dim_v(ax_w, w_xl + 2, -5, 5,
           "Ø10", offset=2, fs=5, font=FONT)


# ─────────────────────────────────────────────────────────────────────────────
# DETAIL D — Wheel attachment plan view (X-Yd, looking down)
# Shows beam (cut), L-bracket arm, fork brackets, wheel footprints,
# and set screw positions from above.
# ─────────────────────────────────────────────────────────────────────────────
ax_d = fig.add_subplot(gs[2, 1])
ax_d.set_facecolor(C_BG)
ax_d.axis("off")

# Plan view coordinates: X horizontal (along beam length), Yd vertical (depth)
# Center on one carriage. Beam runs left-right (X). Wheels above/below (Yd).
# Scale 1:2 to match Detail B.
SC_D = 2.0

D_X_LO = -80
D_X_HI = 80
D_YD_LO = -70
D_YD_HI = 70

ax_d.set_xlim(D_X_LO / SC_D, D_X_HI / SC_D)
ax_d.set_ylim(D_YD_LO / SC_D, D_YD_HI / SC_D)
ax_d.set_aspect("equal")

def px(x_mm):
    return x_mm / SC_D

def py_d(yd_mm):
    return yd_mm / SC_D

# Title
ax_d.text(px(0), py_d(D_YD_HI - 2),
          "DETAIL D — WHEEL ATTACHMENT PLAN",
          ha="center", va="top", fontsize=8, color="#AA6600",
          fontweight="bold", **FONT, zorder=20)
ax_d.text(px(0), py_d(D_YD_HI - 10),
          "(LOOKING DOWN — SCALE 1:2)",
          ha="center", va="top", fontsize=5, color=C_DIM,
          **FONT, zorder=20)

_bbox_d = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.85)

# ── Beam (cut section — runs left-right in X) ──────────────────────────
ax_d.add_patch(Rectangle((px(-BEAM_W / 2), py_d(-BEAM_W / 2)),
                           BEAM_W / SC_D, BEAM_W / SC_D,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=2.0, zorder=5))
# Square bore
ax_d.add_patch(Rectangle((px(-BEAM_BORE / 2), py_d(-BEAM_BORE / 2)),
                           BEAM_BORE / SC_D, BEAM_BORE / SC_D,
                           fc=C_BG, ec=C_FRAME, lw=0.8, zorder=5.5))
# PVC pipe inside (circle in plan view)
ax_d.add_patch(Circle((px(0), py_d(0)),
                         PVC_OD / 2 / SC_D,
                         fc=C_PVC, ec=C_FRAME, lw=0.8, alpha=0.7, zorder=5.7))
ax_d.add_patch(Circle((px(0), py_d(0)),
                         PVC_ID / 2 / SC_D,
                         fc=C_WATER, ec=C_FRAME, lw=0.5, alpha=0.4, zorder=5.8))
ax_d.text(px(0), py_d(0),
          "40×40 SHS\n+ 1\" PVC",
          ha="center", va="center", fontsize=4.5, color=C_FRAME,
          bbox=_bbox_d, **FONT, zorder=15)

# ── L-bracket arm (horizontal plate spanning both wheels, runs in Yd) ───
arm_half_span = WHEEL_SPACING_YD / 2 + 18
arm_w_x = 20
ax_d.add_patch(Rectangle((px(-arm_w_x / 2), py_d(-arm_half_span)),
                           arm_w_x / SC_D, (2 * arm_half_span) / SC_D,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0,
                           hatch="///", alpha=0.7, zorder=4))

# ── U-clamp with flared legs (plan view — wraps beam in X direction) ────
uc_span_x = BEAM_W + 2 * UC_T + 2 * UC_GAP   # top plate span in X
uc_mat_yd = 20                                  # clamp material width in Yd
# Top plate (visible from above — spans X across beam)
ax_d.add_patch(Rectangle((px(-uc_span_x / 2), py_d(-uc_mat_yd / 2)),
                           uc_span_x / SC_D, uc_mat_yd / SC_D,
                           fc=C_UCLAMP, ec=C_FRAME, lw=1.0, alpha=0.5, zorder=6))
# Flared feet (extend in X beyond top plate, sit on L-bracket arm)
for side in [-1, 1]:
    foot_x = side * (BEAM_W / 2 + UC_GAP + UC_T)
    if side < 0:
        foot_x -= UC_FLARE
    ax_d.add_patch(Rectangle((px(foot_x), py_d(-uc_mat_yd / 2)),
                               (UC_FLARE + UC_T) / SC_D, uc_mat_yd / SC_D,
                               fc=C_UCLAMP, ec=C_FRAME, lw=0.8, alpha=0.6, zorder=6))

# Bolt holes through flared feet (circles in plan = bolt going vertically)
for side in [-1, 1]:
    bolt_x = side * (BEAM_W / 2 + UC_GAP + UC_T + UC_FLARE / 2)
    ax_d.add_patch(Circle((px(bolt_x), py_d(0)),
                            3 / SC_D,
                            fc=C_BOLT, ec=C_FRAME, lw=0.5, zorder=8))

leader(ax_d, px(BEAM_W / 2 + UC_GAP + UC_T + UC_FLARE), py_d(uc_mat_yd / 2),
       px(D_X_HI - 15), py_d(BEAM_W / 2 + 30),
       "U-CLAMP\nFLARED LEGS\n+ WING NUTS",
       fs=5, color=C_BOLT, font=FONT, zorder=20, bbox=_bbox_d)

# ── Fork brackets (vertical plates straddling each wheel) ────────────────
fork_t = 6  # fork thickness in X
for w_sign in [-1, 1]:  # two wheels
    w_yd_ctr = w_sign * WHEEL_SPACING_YD / 2
    for offset in [-WHEEL_WIDTH / 2 - 2, WHEEL_WIDTH / 2 + 2]:
        fork_yd = w_yd_ctr + offset
        ax_d.add_patch(Rectangle((px(-fork_t / 2 - 4), py_d(fork_yd - 1)),
                                   fork_t / SC_D, 2 / SC_D,
                                   fc=C_ALUM_FILL, ec=C_FRAME, lw=0.6, zorder=7))

# ── Wheels (footprint — rectangles in plan, width × diameter) ────────────
for w_sign in [-1, 1]:
    w_yd_ctr = w_sign * WHEEL_SPACING_YD / 2
    ax_d.add_patch(Rectangle((px(-WHEEL_DIA / 2), py_d(w_yd_ctr - WHEEL_WIDTH / 2)),
                               WHEEL_DIA / SC_D, WHEEL_WIDTH / SC_D,
                               fc=C_NYLON, ec=C_WHEEL, lw=1.5, alpha=0.6, zorder=3))
    # Axle pin (dot at center)
    ax_d.add_patch(Circle((px(0), py_d(w_yd_ctr)),
                            5 / SC_D,
                            fc="#D0D0D8", ec=C_FRAME, lw=0.5, zorder=7))

# ── Wheel labels ────────────────────────────────────────────────────────
leader(ax_d, px(WHEEL_DIA / 2), py_d(-WHEEL_SPACING_YD / 2),
       px(D_X_HI - 10), py_d(-WHEEL_SPACING_YD / 2 - 10),
       f"Ø{WHEEL_DIA}mm WHEEL\n({WHEEL_WIDTH}mm WIDE)",
       fs=5, color=C_WHEEL, font=FONT, zorder=20, bbox=_bbox_d)

leader(ax_d, px(-arm_w_x / 2 - 1), py_d(0),
       px(D_X_LO + 10), py_d(25),
       "L-BRACKET ARM\n(5mm AL PLATE)",
       fs=5, color=C_FRAME, font=FONT, zorder=20, bbox=_bbox_d)

# ── Dimensions ──────────────────────────────────────────────────────────
draw_dim_v(ax_d, px(D_X_LO + 8),
           py_d(-WHEEL_SPACING_YD / 2), py_d(WHEEL_SPACING_YD / 2),
           f"{WHEEL_SPACING_YD}mm\nWHEEL\nSPACING",
           offset=3 / SC_D, fs=5, font=FONT)

draw_dim_h(ax_d, px(-WHEEL_DIA / 2), px(WHEEL_DIA / 2),
           py_d(D_YD_LO + 12),
           f"Ø{WHEEL_DIA}mm",
           offset=3 / SC_D, fs=5, font=FONT)

# ─────────────────────────────────────────────────────────────────────────────
# PLAN VIEW — Container floor plan showing walkways, tray, and slit positions
# Looking down (X horizontal, Yd vertical).  Scaled to fit panel.
# ─────────────────────────────────────────────────────────────────────────────
ax_p = fig.add_subplot(gs[1, 1])
ax_p.set_facecolor(C_BG)
ax_p.set_aspect("equal")
ax_p.axis("off")

SC_P = 80.0

def ppx(x_mm):
    return x_mm / SC_P

def ppy(yd_mm):
    return yd_mm / SC_P

P_X_LO = -200
P_X_HI = C_LEN + 200
P_YD_LO = -200
P_YD_HI = C_WID + 200

ax_p.set_xlim(ppx(P_X_LO), ppx(P_X_HI))
ax_p.set_ylim(ppy(P_YD_LO), ppy(P_YD_HI))

# Title
ax_p.text(ppx(C_LEN / 2), ppy(P_YD_HI - 50),
          "PLAN VIEW — WALKWAYS & SLIT POSITIONS",
          ha="center", va="top", fontsize=7, color="#006600",
          fontweight="bold", **FONT, zorder=20)
ax_p.text(ppx(C_LEN / 2), ppy(P_YD_HI - 150),
          f"(LOOKING DOWN — SCALE 1:{int(SC_P)})",
          ha="center", va="top", fontsize=5, color=C_DIM,
          **FONT, zorder=20)

# ── Container outline ────────────────────────────────────────────────────
ax_p.add_patch(Rectangle((ppx(0), ppy(0)),
                           C_LEN / SC_P, C_WID / SC_P,
                           fc="#F0F0EA", ec=C_OUT, lw=2.0, zorder=2))

# ── Processing tray ─────────────────────────────────────────────────────
ax_p.add_patch(Rectangle((ppx(PROC_TRAY_X_L), ppy(PROC_TRAY_YD_NEAR)),
                           PROC_TRAY_W / SC_P, PROC_TRAY_D / SC_P,
                           fc=C_TRAY, ec=C_OUT, lw=1.0, alpha=0.5, zorder=3))
ax_p.text(ppx((PROC_TRAY_X_L + PROC_TRAY_X_R) / 2), ppy(C_WID / 2),
          "PROCESSING TRAY",
          ha="center", va="center", fontsize=5, color=C_DIM,
          style="italic", **FONT, zorder=5)

# ── Near walkway (pinhole side, Yd=0 to WALKWAY_W) ─────────────────────
ax_p.add_patch(Rectangle((ppx(PROC_TRAY_X_L), ppy(0)),
                           PROC_TRAY_W / SC_P, WALKWAY_W / SC_P,
                           fc=C_GRATE, ec=C_OUT, lw=1.0, alpha=0.4, zorder=4))
ax_p.text(ppx(C_LEN / 2), ppy(WALKWAY_W / 2),
          "NEAR WALKWAY", ha="center", va="center",
          fontsize=4.5, color=C_GRATE, fontweight="bold", **FONT, zorder=6)

# ── Far walkway (film plane side, Yd=WALKWAY_FAR_YD to C_WID) ──────────
ax_p.add_patch(Rectangle((ppx(PROC_TRAY_X_L), ppy(WALKWAY_FAR_YD)),
                           PROC_TRAY_W / SC_P, WALKWAY_W / SC_P,
                           fc=C_GRATE, ec=C_OUT, lw=1.0, alpha=0.4, zorder=4))
ax_p.text(ppx(C_LEN / 2), ppy(WALKWAY_FAR_YD + WALKWAY_W / 2),
          "FAR WALKWAY", ha="center", va="center",
          fontsize=4.5, color=C_GRATE, fontweight="bold", **FONT, zorder=6)

# ── Left walkway (cargo door end) ───────────────────────────────────────
ax_p.add_patch(Rectangle((ppx(WALKWAY_LEFT_X), ppy(0)),
                           WALKWAY_W / SC_P, C_WID / SC_P,
                           fc=C_GRATE, ec=C_OUT, lw=1.0, alpha=0.4, zorder=4))
ax_p.text(ppx(WALKWAY_LEFT_X + WALKWAY_W / 2), ppy(C_WID / 2),
          "LEFT\nWALKWAY", ha="center", va="center",
          fontsize=4, color=C_GRATE, rotation=90, **FONT, zorder=6)

# ── Right walkway ──────────────────────────────────────────────────────
ax_p.add_patch(Rectangle((ppx(WALKWAY_RIGHT_X), ppy(0)),
                           WALKWAY_W / SC_P, C_WID / SC_P,
                           fc=C_GRATE, ec=C_OUT, lw=1.0, alpha=0.4, zorder=4))
ax_p.text(ppx(WALKWAY_RIGHT_X + WALKWAY_W / 2), ppy(C_WID / 2),
          "RIGHT\nWALKWAY", ha="center", va="center",
          fontsize=4, color=C_GRATE, rotation=90, **FONT, zorder=6)

# ── Slits in near walkway (for boom arm to slide through) ───────────────
# Left carriage slit
slit_x_l = CARRIAGE_X_L - SLIT_WIDTH / 2
ax_p.add_patch(Rectangle((ppx(slit_x_l), ppy(0)),
                           SLIT_WIDTH / SC_P, WALKWAY_W / SC_P,
                           fc="#FF4444", ec="#CC0000", lw=1.5, alpha=0.6, zorder=7))
# Right carriage slit (mirrored position in right walkway)
carriage_x_r = WALKWAY_RIGHT_X + WALKWAY_W / 2
slit_x_r = carriage_x_r - SLIT_WIDTH / 2
ax_p.add_patch(Rectangle((ppx(slit_x_r), ppy(0)),
                           SLIT_WIDTH / SC_P, WALKWAY_W / SC_P,
                           fc="#FF4444", ec="#CC0000", lw=1.5, alpha=0.6, zorder=7))

# ── Slits in far walkway ────────────────────────────────────────────────
ax_p.add_patch(Rectangle((ppx(slit_x_l), ppy(WALKWAY_FAR_YD)),
                           SLIT_WIDTH / SC_P, WALKWAY_W / SC_P,
                           fc="#FF4444", ec="#CC0000", lw=1.5, alpha=0.6, zorder=7))
ax_p.add_patch(Rectangle((ppx(slit_x_r), ppy(WALKWAY_FAR_YD)),
                           SLIT_WIDTH / SC_P, WALKWAY_W / SC_P,
                           fc="#FF4444", ec="#CC0000", lw=1.5, alpha=0.6, zorder=7))

# Slit labels
leader(ax_p, ppx(slit_x_l + SLIT_WIDTH / 2), ppy(-10),
       ppx(slit_x_l - 200), ppy(-120),
       f"{SLIT_WIDTH}mm SLIT\n(NEAR & FAR\nWALKWAYS)",
       fs=5, color="#CC0000", font=FONT, zorder=20)

leader(ax_p, ppx(slit_x_r + SLIT_WIDTH / 2), ppy(-10),
       ppx(slit_x_r + 250), ppy(-120),
       f"{SLIT_WIDTH}mm SLIT\n(MIRRORED)",
       fs=5, color="#CC0000", font=FONT, zorder=20)

# ── Beam position (example — dashed line across tray) ────────────────────
beam_example_yd = PROC_TRAY_YD_NEAR + PROC_TRAY_D / 2
ax_p.plot([ppx(PROC_OPEN_X_L), ppx(PROC_OPEN_X_R)],
          [ppy(beam_example_yd), ppy(beam_example_yd)],
          color=C_FRAME, lw=1.5, ls="--", zorder=6)
ax_p.text(ppx((PROC_OPEN_X_L + PROC_OPEN_X_R) / 2), ppy(beam_example_yd + 80),
          "BEAM (EXAMPLE POSITION)",
          ha="center", va="bottom", fontsize=4.5, color=C_FRAME,
          style="italic", **FONT, zorder=8)

# Travel arrow
ax_p.annotate("", xy=(ppx(PROC_OPEN_X_L + 400), ppy(beam_example_yd + 300)),
              xytext=(ppx(PROC_OPEN_X_L + 400), ppy(beam_example_yd - 300)),
              arrowprops=dict(arrowstyle="<->", color=C_BLUE, lw=1.0),
              zorder=8)
ax_p.text(ppx(PROC_OPEN_X_L + 500), ppy(beam_example_yd),
          f"TRAVEL\n{SPRAY_BAR_TRAVEL}mm",
          ha="left", va="center", fontsize=4.5, color=C_BLUE, **FONT, zorder=8)

# ── Key dimensions ──────────────────────────────────────────────────────
draw_dim_h(ax_p, ppx(0), ppx(C_LEN), ppy(-130),
           f"{C_LEN}mm CONTAINER", offset=10 / SC_P, fs=5, font=FONT)
draw_dim_v(ax_p, ppx(-100), ppy(0), ppy(C_WID),
           f"{C_WID}mm", offset=10 / SC_P, fs=5, font=FONT)

# ── Pinhole wall label ──────────────────────────────────────────────────
ax_p.text(ppx(C_LEN / 2), ppy(-30),
          "PINHOLE WALL (Yd=0)", ha="center", va="top",
          fontsize=4, color=C_DIM, style="italic", **FONT, zorder=5)


# ─────────────────────────────────────────────────────────────────────────────
# DETAIL E — Handle / arm attachment (section through beam at center)
# Shows ball joint on beam top face, round tube arm extending upward,
# water hose zip-tied to arm.
# ─────────────────────────────────────────────────────────────────────────────
ax_e = fig.add_subplot(gs[3, 0])
ax_e.set_facecolor(C_BG)
ax_e.axis("off")

SC_E = 1.5

E_YD_LO = -60
E_YD_HI = 90
E_Z_LO = -10
E_Z_HI = 175

ax_e.set_xlim(E_YD_LO / SC_E, E_YD_HI / SC_E)
ax_e.set_ylim(E_Z_LO / SC_E, E_Z_HI / SC_E)
ax_e.set_aspect("equal")

def ey(yd_mm):
    return yd_mm / SC_E

def ez(z_mm):
    return z_mm / SC_E

_bbox_e = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.85)

# Title
ax_e.text(ey((E_YD_LO + E_YD_HI) / 2), ez(E_Z_HI - 2),
          "DETAIL E — HANDLE ARM ATTACHMENT",
          ha="center", va="top", fontsize=8, color="#880088",
          fontweight="bold", **FONT, zorder=20)
ax_e.text(ey((E_YD_LO + E_YD_HI) / 2), ez(E_Z_HI - 12),
          "(SECTION THROUGH BEAM AT CENTER — SCALE 1:1.5)",
          ha="center", va="top", fontsize=5, color=C_DIM,
          **FONT, zorder=20)

# ── Beam cross-section (Yd-Z view at beam center) ─────────────────────
e_beam_ctr = 0
e_beam_l = e_beam_ctr - BEAM_W / 2
e_beam_r = e_beam_ctr + BEAM_W / 2
e_beam_bot = 0

# AL SHS outer
ax_e.add_patch(Rectangle((ey(e_beam_l), ez(e_beam_bot)),
                           BEAM_W / SC_E, BEAM_W / SC_E,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=2.5, zorder=5))
# Square bore
ax_e.add_patch(Rectangle((ey(e_beam_ctr - BEAM_BORE / 2),
                            ez(e_beam_bot + BEAM_T)),
                           BEAM_BORE / SC_E, BEAM_BORE / SC_E,
                           fc=C_BG, ec=C_FRAME, lw=0.8, zorder=5.5))
# PVC pipe (circle cross-section)
ax_e.add_patch(Circle((ey(e_beam_ctr), ez(e_beam_bot + BEAM_W / 2)),
                         PVC_OD / 2 / SC_E,
                         fc=C_PVC, ec=C_FRAME, lw=1.0, alpha=0.7, zorder=5.7))
# Water inside PVC
ax_e.add_patch(Circle((ey(e_beam_ctr), ez(e_beam_bot + BEAM_W / 2)),
                         PVC_ID / 2 / SC_E,
                         fc=C_WATER, ec=C_FRAME, lw=0.5, alpha=0.4, zorder=5.8))

ax_e.text(ey(e_beam_ctr), ez(e_beam_bot + BEAM_W / 2),
          "SHS +\nPVC",
          ha="center", va="center", fontsize=4, color=C_FRAME,
          bbox=_bbox_e, **FONT, zorder=15)

# ── Ball joint on beam top face ───────────────────────────────────────
BALL_DIA = 20       # ball diameter (mm)
SOCKET_OD = 36      # socket housing outer diameter
SOCKET_H = 28       # socket housing height (base to top rim)
FLANGE_W = 50       # mounting flange width
FLANGE_T = 5        # flange thickness
STUD_DIA = 12       # stud extending from ball
STUD_EXT = 20       # stud length above socket top
C_JOINT = "#C8B070"

beam_top_z = e_beam_bot + BEAM_W
flange_bot_z = beam_top_z
socket_bot_z = flange_bot_z + FLANGE_T
ball_ctr_z = socket_bot_z + SOCKET_H / 2 + 2
socket_top_z = socket_bot_z + SOCKET_H
stud_top_z = socket_top_z + STUD_EXT

# Saddle plate between beam top and socket (load distribution)
ax_e.add_patch(Rectangle((ey(e_beam_ctr - FLANGE_W / 2), ez(flange_bot_z)),
                           FLANGE_W / SC_E, FLANGE_T / SC_E,
                           fc="#B0B0B8", ec=C_FRAME, lw=1.2, zorder=7))

# U-bolt wrapping over socket housing, legs through beam top face
ubolt_gap = 2
ubolt_t = 4
ubolt_l = e_beam_ctr - SOCKET_OD / 2 - ubolt_gap - ubolt_t
ubolt_r = e_beam_ctr + SOCKET_OD / 2 + ubolt_gap + ubolt_t

# U-bolt arc over socket
ub_arc = np.linspace(0, np.pi, 30)
ub_arc_r = (ubolt_r - ubolt_l) / 2
ub_arc_cz = socket_bot_z + SOCKET_H * 0.6
ub_arc_yd = e_beam_ctr + ub_arc_r * np.cos(ub_arc)
ub_arc_z = ub_arc_cz + ub_arc_r * 0.45 * np.sin(ub_arc)
ax_e.plot([ey(y) for y in ub_arc_yd], [ez(z) for z in ub_arc_z],
          color=C_BOLT, lw=2.5, zorder=9, solid_capstyle="round")

# Left leg of U-bolt
ax_e.plot([ey(ubolt_l + ubolt_t / 2), ey(ubolt_l + ubolt_t / 2)],
          [ez(ub_arc_cz), ez(beam_top_z - BEAM_T - 5)],
          color=C_BOLT, lw=2.5, zorder=9)
# Right leg
ax_e.plot([ey(ubolt_r - ubolt_t / 2), ey(ubolt_r - ubolt_t / 2)],
          [ez(ub_arc_cz), ez(beam_top_z - BEAM_T - 5)],
          color=C_BOLT, lw=2.5, zorder=9)

# Nuts below beam top flange
for nut_yd in [ubolt_l + ubolt_t / 2, ubolt_r - ubolt_t / 2]:
    ax_e.add_patch(Rectangle((ey(nut_yd - 5), ez(beam_top_z - BEAM_T - 8)),
                               10 / SC_E, 4 / SC_E,
                               fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=10))

# Socket housing (sectioned — hatched)
ax_e.add_patch(Rectangle((ey(e_beam_ctr - SOCKET_OD / 2), ez(socket_bot_z)),
                           SOCKET_OD / SC_E, SOCKET_H / SC_E,
                           fc=C_JOINT, ec=C_FRAME, lw=1.5, hatch="///",
                           zorder=6))
# Socket bore (cavity for ball)
bore_r = BALL_DIA / 2 + 1
ax_e.add_patch(Circle((ey(e_beam_ctr), ez(ball_ctr_z)),
                         bore_r / SC_E,
                         fc=C_BG, ec=C_FRAME, lw=0.5, zorder=6.5))

# Ball
ax_e.add_patch(Circle((ey(e_beam_ctr), ez(ball_ctr_z)),
                         BALL_DIA / 2 / SC_E,
                         fc="#E0D8C0", ec=C_FRAME, lw=1.5, zorder=7))

# Stud extending upward from ball
ax_e.add_patch(Rectangle((ey(e_beam_ctr - STUD_DIA / 2), ez(ball_ctr_z)),
                           STUD_DIA / SC_E, (stud_top_z - ball_ctr_z) / SC_E,
                           fc="#D0C8B0", ec=C_FRAME, lw=1.0, zorder=7.5))

# ── Round tube arm (clamped onto stud with pinch bolt) ────────────────
ARM_OD = 25    # 25mm OD round tube (1" nominal)
ARM_WALL = 2   # 2mm wall thickness
ARM_ID = ARM_OD - 2 * ARM_WALL
arm_base_z = stud_top_z - STUD_EXT + 2
arm_top_z = arm_base_z + 80

# Arm tube
ax_e.add_patch(Rectangle((ey(e_beam_ctr - ARM_OD / 2), ez(arm_base_z)),
                           ARM_OD / SC_E, (arm_top_z - arm_base_z) / SC_E,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=8))
# Interior bore (stud visible inside)
ax_e.add_patch(Rectangle((ey(e_beam_ctr - ARM_ID / 2), ez(arm_base_z)),
                           ARM_ID / SC_E, (stud_top_z - arm_base_z) / SC_E,
                           fc="#D0C8B0", ec="none", zorder=8.3))
ax_e.add_patch(Rectangle((ey(e_beam_ctr - ARM_ID / 2), ez(stud_top_z)),
                           ARM_ID / SC_E, (arm_top_z - stud_top_z) / SC_E,
                           fc=C_BG, ec=C_FRAME, lw=0.5, zorder=8.5))

# Pinch bolt through arm tube wall (clamps onto stud)
pinch_z = arm_base_z + 12
ax_e.add_patch(Rectangle((ey(e_beam_ctr + ARM_OD / 2), ez(pinch_z - 2)),
                           8 / SC_E, 4 / SC_E,
                           fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=9))
ax_e.plot([ey(e_beam_ctr + ARM_ID / 2), ey(e_beam_ctr + ARM_OD / 2 + 8)],
          [ez(pinch_z), ez(pinch_z)],
          color=C_BOLT, lw=1.5, zorder=9)

# Continuation arrow
ax_e.annotate("", xy=(ey(e_beam_ctr), ez(arm_top_z + 8)),
              xytext=(ey(e_beam_ctr), ez(arm_top_z)),
              arrowprops=dict(arrowstyle="->", color=C_FRAME, lw=1.5),
              zorder=12)
ax_e.text(ey(e_beam_ctr + 3), ez(arm_top_z + 5),
          "ARM CONTINUES\nTO TRAY SURFACE",
          ha="left", va="center", fontsize=4.5, color=C_DIM,
          style="italic", **FONT, zorder=15)

# Movement arcs (show ball joint articulation range)
for arc_ang in [-25, 25]:
    ang_rad = np.radians(arc_ang)
    arc_len = 35
    ax_e.annotate("",
        xy=(ey(e_beam_ctr + arc_len * np.sin(ang_rad)),
            ez(ball_ctr_z + arc_len * np.cos(ang_rad))),
        xytext=(ey(e_beam_ctr), ez(ball_ctr_z)),
        arrowprops=dict(arrowstyle="->", color="#AA0000", lw=0.8,
                        connectionstyle=f"arc3,rad={0.3 if arc_ang > 0 else -0.3}"),
        zorder=12)
ax_e.text(ey(e_beam_ctr - SOCKET_OD / 2 - 5), ez(ball_ctr_z + 20),
          "MULTI-AXIS\nARTICULATION",
          ha="right", va="center", fontsize=4.5, color="#AA0000",
          bbox=_bbox_e, **FONT, zorder=15)

# Leaders
leader(ax_e, ey(e_beam_ctr + SOCKET_OD / 2), ez(ball_ctr_z),
       ey(e_beam_ctr + SOCKET_OD / 2 + 20), ez(ball_ctr_z - 12),
       f"Ø{BALL_DIA}mm BALL JOINT\n(SS BALL, ZINC SOCKET)\nU-BOLT TO BEAM",
       fs=5, color=C_JOINT, font=FONT, zorder=20, bbox=_bbox_e)

leader(ax_e, ey(ubolt_r), ez(ub_arc_cz),
       ey(ubolt_r + 15), ez(ub_arc_cz - 10),
       "M8 SS U-BOLT\n+ NYLOC NUTS",
       fs=4.5, color=C_BOLT, font=FONT, zorder=20, bbox=_bbox_e)

leader(ax_e, ey(e_beam_ctr + ARM_OD / 2 + 8), ez(pinch_z),
       ey(e_beam_ctr + 35), ez(pinch_z + 15),
       "M6 PINCH BOLT\n(CLAMPS ARM\nONTO STUD)",
       fs=4.5, color=C_BOLT, font=FONT, zorder=20, bbox=_bbox_e)

leader(ax_e, ey(e_beam_ctr + ARM_OD / 2), ez(arm_base_z + 50),
       ey(e_beam_ctr + 35), ez(arm_base_z + 65),
       f"Ø{ARM_OD}mm AL TUBE\n(2mm WALL)\nVERTICAL ARM",
       fs=5, color=C_FRAME, font=FONT, zorder=20, bbox=_bbox_e)

# ── Water hose zip-tied to arm ────────────────────────────────────────
hose_od = 16   # 1/2" ID hose ~ 16mm OD
hose_ctr_yd = e_beam_ctr + ARM_OD / 2 + hose_od / 2 + 3

# Hose (runs vertically alongside arm)
ax_e.add_patch(Rectangle((ey(hose_ctr_yd - hose_od / 2), ez(arm_base_z - 5)),
                           hose_od / SC_E, (arm_top_z - arm_base_z + 10) / SC_E,
                           fc=C_HOSE, ec=C_BLUE, lw=1.0, alpha=0.6, zorder=7.5))

# Zip ties (3 ties shown)
for zt_z in [arm_base_z + 15, arm_base_z + 40, arm_base_z + 65]:
    zt_l = e_beam_ctr - ARM_OD / 2 - 4
    zt_r = hose_ctr_yd + hose_od / 2 + 2
    ax_e.add_patch(Rectangle((ey(zt_l), ez(zt_z - 1.5)),
                               (zt_r - zt_l) / SC_E, 3 / SC_E,
                               fc="none", ec="#222222", lw=1.2, zorder=11))
    # Zip tie nub
    ax_e.add_patch(Rectangle((ey(zt_l - 2), ez(zt_z - 2)),
                               2 / SC_E, 4 / SC_E,
                               fc="#333333", ec="#222222", lw=0.5, zorder=11))

leader(ax_e, ey(hose_ctr_yd), ez(arm_base_z + 55),
       ey(hose_ctr_yd + 20), ez(arm_base_z + 70),
       "1/2\" FLEX HOSE\n(ZIP-TIED TO ARM)",
       fs=5, color=C_HOSE, font=FONT, zorder=20, bbox=_bbox_e)

ax_e.text(ey(e_beam_ctr - 5), ez(arm_base_z + 40),
          "ZIP\nTIES\n(TYP.)",
          ha="right", va="center", fontsize=4.5, color="#333333",
          bbox=_bbox_e, **FONT, zorder=15)

# ── Dimensions ────────────────────────────────────────────────────────
draw_dim_h(ax_e, ey(e_beam_l), ey(e_beam_r), ez(e_beam_bot - 8),
           f"{BEAM_W}mm SHS", offset=3 / SC_E, fs=5, font=FONT)

draw_dim_h(ax_e, ey(e_beam_ctr - ARM_OD / 2), ey(e_beam_ctr + ARM_OD / 2),
           ez(arm_top_z - 5),
           f"Ø{ARM_OD}mm", offset=3 / SC_E, fs=5, font=FONT)

draw_dim_v(ax_e, ey(e_beam_l - 8), ez(e_beam_bot), ez(e_beam_bot + BEAM_W),
           f"{BEAM_W}mm", offset=3 / SC_E, fs=4.5, font=FONT)

draw_dim_v(ax_e, ey(e_beam_l - 20), ez(e_beam_bot + BEAM_W), ez(socket_top_z),
           f"{int(socket_top_z - beam_top_z)}mm\nJOINT",
           offset=3 / SC_E, fs=4.5, font=FONT)

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
