#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_spray_bar_diagram.py
Spray bar assembly detail for TBS-001 processing tray wash system.

Sheet 1 — Gantry spray bar:
  Left panel:  X-Z section viewed from film plane (along Yd).
               Centered on beam centerline. Walkway slit, pole,
               beam (full span), BV-02, flex hose. H1:18 / V1:4.5.
  Right panel: Yd-Z composite cross section looking along X.
               Equal 1:2 scale. Carriage, beam, ball joint, arm.

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
    BV02_X, BV02_Z,
    SPRAY_BAR_SLIT_W,
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

# PVC socket cap geometry (also used in gantry elevation Detail A content)
CAP_SOCKET_DEPTH = 20
CAP_WALL_T = 3.5
CAP_CLOSED_T = 3.5
PVC_EXTEND = 25

BEAM_SPAN = PROC_OPEN_X_R - PROC_OPEN_X_L  # 3,859mm

CARRIAGE_X_L = WALKWAY_LEFT_X + WALKWAY_W / 2    # ≈ 320mm

WALL_T = 3

# ═════════════════════════════════════════════════════════════════════════════
# SHEET 1
# ═════════════════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(28, 30))
fig.patch.set_facecolor(C_BG)
gs = GridSpec(3, 2, figure=fig, width_ratios=[1, 1.3],
              height_ratios=[2.5, 1, 1],
              wspace=0.06, hspace=0.08, bottom=0.06, top=0.97)

# ─────────────────────────────────────────────────────────────────────────────
# LEFT PANEL — X-Z section viewed from film plane (looking along Yd)
# Centered on beam centerline.  Shows walkway slit, pole, beam, BV-02.
# Horizontal scale 1:18, Vertical scale 1:4.5 (4× vert exaggeration)
# ─────────────────────────────────────────────────────────────────────────────
ax = fig.add_subplot(gs[0, 0])
ax.set_facecolor(C_BG)
ax.axis("off")

H_SC = 18.0
V_SC = 4.5

def sx(x_mm):
    return 1.0 + x_mm / H_SC

def sz(z_mm):
    return 1.0 + z_mm / V_SC

pole_x = (PROC_OPEN_X_L + PROC_OPEN_X_R) / 2

CUT_X = int(pole_x) + 300
X_LO = -100
X_HI = CUT_X + 150
Z_LO = -50
Z_HI = 2050

ax.set_xlim(sx(X_LO), sx(X_HI))
ax.set_ylim(sz(Z_LO), sz(Z_HI))

# ── Container floor ──────────────────────────────────────────────────────
ax.plot([sx(X_LO), sx(X_HI)], [sz(0), sz(0)], color=C_OUT, lw=2.0, zorder=3)
ax.add_patch(Rectangle((sx(X_LO), sz(-25)),
                         (X_HI - X_LO) / H_SC, 25 / V_SC,
                         fc="#E0E0D8", ec=C_OUT, lw=0.8, hatch="...", zorder=1))

# ── Container side wall (X=0 only; right side cut) ─────────────────────
wall_vis_t = WALL_T * 6
ax.add_patch(Rectangle((sx(0 - wall_vis_t / 2), sz(Z_LO)),
                         wall_vis_t / H_SC, (Z_HI - Z_LO) / V_SC,
                         fc=C_WALL, ec=C_OUT, lw=1.0, hatch="///", zorder=2))
ax.text(sx(0), sz(Z_HI - 30), "CONTAINER\nWALL (X=0)",
        ha="center", va="top", fontsize=4.5, color=C_DIM, **FONT)

# ── Processing tray ──────────────────────────────────────────────────────
tray_x_l = PROC_TRAY_X_L
tray_x_r = PROC_TRAY_X_R
tray_vis_r = CUT_X  # clip to cut line

ax.add_patch(Rectangle((sx(tray_x_l), sz(0)),
                         (tray_vis_r - tray_x_l) / H_SC, TRAY_FLOOR_Z / V_SC,
                         fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))
# Left rim only (right is beyond cut line)
rim_w = 4
ax.add_patch(Rectangle((sx(tray_x_l - rim_w / 2), sz(0)),
                         rim_w / H_SC, PROC_TRAY_RIM / V_SC,
                         fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=5))

ax.text(sx((tray_x_l + pole_x) / 2), sz(TRAY_FLOOR_Z + 13),
        "PROCESSING TRAY (304 SS)", ha="center", va="bottom",
        fontsize=5, color=C_DIM, style="italic", **FONT, zorder=10)

# ── Left walkway grating (X=170-470) ────────────────────────────────────
wk_l = WALKWAY_LEFT_X
wk_r = PROC_OPEN_X_L

ax.add_patch(Rectangle((sx(wk_l), sz(GRATE_Z_BOT)),
                         (wk_r - wk_l) / H_SC, WALKWAY_GRATE_T / V_SC,
                         fc=C_GRATE, ec=C_OUT, lw=1.2, zorder=8))
ax.text(sx((wk_l + wk_r) / 2), sz(GRATE_Z_TOP + 5),
        "LEFT WK", ha="center", va="bottom",
        fontsize=4.5, color=C_GRATE, fontweight="bold", **FONT, zorder=10)

# (Right walkway omitted — beyond cut line)

# ── Near walkway slit at pole_x (cross-section through walkway) ─────────
SLIT_WIDTH = SPRAY_BAR_SLIT_W
slit_x_l = pole_x - SLIT_WIDTH / 2
slit_x_r = pole_x + SLIT_WIDTH / 2

# Near walkway grating runs full X span at Yd=0-300 — shown as thin strip
# at deck height. Section through slit shows gap. Trimmed at CUT_X.
nwk_grate_l = tray_x_l
nwk_grate_r = CUT_X
# Grating left of slit
ax.add_patch(Rectangle((sx(nwk_grate_l), sz(GRATE_Z_BOT)),
                         (slit_x_l - nwk_grate_l) / H_SC, WALKWAY_GRATE_T / V_SC,
                         fc=C_GRATE, ec=C_OUT, lw=0.5, alpha=0.35, zorder=7.5))
# Grating right of slit
ax.add_patch(Rectangle((sx(slit_x_r), sz(GRATE_Z_BOT)),
                         (nwk_grate_r - slit_x_r) / H_SC, WALKWAY_GRATE_T / V_SC,
                         fc=C_GRATE, ec=C_OUT, lw=0.5, alpha=0.35, zorder=7.5))
# Slit opening
ax.add_patch(Rectangle((sx(slit_x_l), sz(GRATE_Z_BOT)),
                         SLIT_WIDTH / H_SC, WALKWAY_GRATE_T / V_SC,
                         fc=C_BG, ec=C_FRAME, lw=1.0, zorder=8.5))
leader(ax, sx(pole_x), sz(GRATE_Z_TOP + 3),
       sx(pole_x - 300), sz(GRATE_Z_TOP + 50),
       f"{SLIT_WIDTH}mm SLIT\n(NEAR WALKWAY\nAT POLE POSITION)",
       fs=5, color=C_FRAME, font=FONT, zorder=15)

ax.text(sx(pole_x - 500), sz(GRATE_Z_BOT - 5),
        "NEAR WALKWAY (PROJECTED, Yd=0–300)",
        ha="center", va="top", fontsize=4.5, color=C_GRATE,
        style="italic", **FONT, zorder=10)

# ── Beam / spray bar (left end to cut line) ─────────────────────────────
beam_x_l = PROC_TRAY_X_L + 30    # 30mm from tray lip — beam extends under walkway
beam_x_r = PROC_TRAY_X_R - 30    # 30mm from right tray lip
beam_length = beam_x_r - beam_x_l
beam_vis_r = CUT_X  # visual right end (cut line)

# Beam shown in cut section (reveals internal PVC pipe)
ax.add_patch(Rectangle((sx(beam_x_l), sz(BEAM_Z_BOT)),
                         (beam_vis_r - beam_x_l) / H_SC, BEAM_W / V_SC,
                         fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=9))
# PVC pipe inside
ax.add_patch(Rectangle((sx(beam_x_l + 20), sz(BEAM_Z_BOT + BEAM_T + 0.3)),
                         (beam_vis_r - beam_x_l - 20) / H_SC, PVC_OD / V_SC,
                         fc=C_PVC, ec=C_FRAME, lw=0.5, alpha=0.5, zorder=9.3))
# Water inside PVC
ax.add_patch(Rectangle((sx(beam_x_l + 20), sz(BEAM_Z_BOT + BEAM_T + 0.3 + PVC_WALL)),
                         (beam_vis_r - beam_x_l - 20) / H_SC, PVC_ID / V_SC,
                         fc=C_WATER, ec="none", alpha=0.3, zorder=9.5))

ax.text(sx((beam_x_l + pole_x) / 2), sz(BEAM_Z_TOP + 8),
        f"40×40×3mm AL SHS — {beam_length}mm LONG — 1\" PVC PIPE INSIDE",
        ha="center", va="bottom", fontsize=5.5, color=C_FRAME,
        fontweight="bold", **FONT, zorder=15)

# Spray apertures and droplets (open processing area only, not under walkway)
spray_x_l = PROC_OPEN_X_L
n_drops = 6
for i in range(n_drops):
    frac = (i + 0.5) / n_drops
    drop_x = spray_x_l + 50 + (beam_vis_r - spray_x_l - 100) * frac
    ax.plot([sx(drop_x - APERTURE_DIA / 2), sx(drop_x + APERTURE_DIA / 2)],
            [sz(BEAM_Z_BOT), sz(BEAM_Z_BOT)],
            color=C_WATER, lw=1.5, zorder=10)
    ax.plot([sx(drop_x), sx(drop_x)],
            [sz(BEAM_Z_BOT - 1), sz(TRAY_FLOOR_Z + 2)],
            color=C_WATER, lw=0.5, alpha=0.4, zorder=6)

# Left end cap (open beam)
ax.plot([sx(beam_x_l), sx(beam_x_l)], [sz(BEAM_Z_BOT), sz(BEAM_Z_TOP)],
        color=C_FRAME, lw=2.0, zorder=9.5)

# ── Break / cut line (zigzag at CUT_X) ─────────────────────────────────
zz_z_lo = Z_LO
zz_z_hi = Z_HI - 150
zz_amp = 20
zz_n = 18
zz_zs = np.linspace(zz_z_lo, zz_z_hi, zz_n * 2 + 1)
zz_xs = [CUT_X + (zz_amp if i % 2 else -zz_amp) for i in range(len(zz_zs))]
zz_xs[0] = CUT_X
zz_xs[-1] = CUT_X
ax.plot([sx(x) for x in zz_xs], [sz(z) for z in zz_zs],
        color=C_FRAME, lw=1.5, zorder=25)
ax.text(sx(CUT_X + 40), sz(Z_HI / 2),
        "CUT", ha="left", va="center", fontsize=6, color=C_DIM,
        rotation=90, **FONT, zorder=25)

# ── Pole through slit down to beam ──────────────────────────────────────
pole_top_z = GRATE_Z_TOP + 890   # extends to operator waist height (1780/2)
pole_bot_z = BEAM_Z_TOP + 5

ax.plot([sx(pole_x), sx(pole_x)],
        [sz(pole_top_z), sz(pole_bot_z)],
        color="#8B6914", lw=2.5, zorder=10, solid_capstyle="round")
ax.plot([sx(pole_x), sx(pole_x)],
        [sz(pole_top_z), sz(pole_bot_z)],
        color="#BFA040", lw=1.0, zorder=10.5)

leader(ax, sx(pole_x + 5), sz(pole_top_z),
       sx(pole_x - 375), sz(pole_top_z + 30),
       "TELESCOPING POLE\n(THROUGH WALKWAY SLIT)",
       fs=4.5, color="#8B6914", font=FONT, zorder=15)

# ── BV-02 on pinhole wall (wall-mounted) ────────────────────────────────
bv_z = BV02_Z
bv_size = 30
pipe_w = 10

# Pinhole wall surface behind BV-02 (hatched strip — we're looking AT the wall)
wall_strip_w = 80
ax.add_patch(Rectangle((sx(BV02_X - wall_strip_w / 2), sz(0)),
                         wall_strip_w / H_SC, (bv_z + bv_size) / V_SC,
                         fc=C_WALL, ec=C_OUT, lw=0.5, alpha=0.2,
                         hatch="///", zorder=10.5))

# Wall mounting brackets (pipe clamps to wall)
for clamp_z in [bv_z * 0.3, bv_z * 0.6]:
    clamp_w = pipe_w + 16
    ax.add_patch(Rectangle((sx(BV02_X - clamp_w / 2), sz(clamp_z - 4)),
                             clamp_w / H_SC, 8 / V_SC,
                             fc="#B0B0B8", ec=C_FRAME, lw=0.8, zorder=11.5))

# Pipe riser from floor to BV-02
ax.add_patch(Rectangle((sx(BV02_X - pipe_w / 2), sz(0)),
                         pipe_w / H_SC, bv_z / V_SC,
                         fc=C_BLUE, ec=C_FRAME, lw=0.8, alpha=0.4, zorder=11))

# BV-02 valve body
ax.add_patch(Rectangle((sx(BV02_X - bv_size / 2), sz(bv_z - bv_size / 2)),
                         bv_size / H_SC, bv_size / V_SC,
                         fc=C_BLUE, ec=C_FRAME, lw=1.5, alpha=0.6, zorder=12))
ax.plot([sx(BV02_X), sx(BV02_X - 30)],
        [sz(bv_z), sz(bv_z + 30)],
        color=C_FRAME, lw=2.0, zorder=12)

leader(ax, sx(BV02_X - 30), sz(bv_z + 35),
       sx(BV02_X - 375), sz(bv_z + 80),
       f"BV-02 @ Z={int(bv_z)}mm\n(1/2\" BALL VALVE)\nWAIST HEIGHT",
       fs=5.5, color=C_BLUE, font=FONT, zorder=15)

# ── Flex hose from BV-02 to beam center feed ────────────────────────────
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

ax.plot([sx(x) for x in hose_xs], [sz(z) for z in hose_zs],
        color=C_HOSE, lw=2.0, alpha=0.7, zorder=11)

ax.text(sx(BV02_X + 75), sz(bv_z - 200),
        "1/2\" FLEX HOSE\n-> CENTER FEED\n(4m COILED)",
        ha="left", va="top", fontsize=4.5, color=C_HOSE, **FONT, zorder=15)

# ── Center feed fitting at beam center ───────────────────────────────────
feed_dot_r = 8
ax.add_patch(Circle((sx(pole_x), sz(BEAM_Z_TOP)),
                      feed_dot_r / V_SC,
                      fc="#C0A860", ec=C_FRAME, lw=0.8, zorder=12))
leader(ax, sx(pole_x + feed_dot_r), sz(BEAM_Z_TOP + feed_dot_r),
       sx(pole_x + 350), sz(BEAM_Z_TOP + 40),
       "1/2\" BULKHEAD CENTER FEED",
       fs=4.5, color="#C0A860", font=FONT, zorder=15)

# ── Centerline through beam and slit ─────────────────────────────────────
ax.plot([sx(pole_x), sx(pole_x)], [sz(Z_LO), sz(Z_HI - 200)],
        color=C_CL, lw=0.8, ls=(0, (10, 4, 2, 4)), zorder=1.5)
ax.text(sx(pole_x-1), sz(Z_LO), "CL BEAM CENTER",
        ha="center", va="bottom", fontsize=4.5, color=C_CL, **FONT, zorder=2)

# ── Dimensions ────────────────────────────────────────────────────────────
# Beam span shown with note (full span beyond cut)
draw_dim_h(ax, sx(beam_x_l), sx(beam_vis_r), sz(BEAM_Z_BOT - 50),
           f"{beam_length}mm BEAM (CONTINUES →)",
           offset=4 / V_SC, fs=5, font=FONT, above=False)

draw_dim_v(ax, sx(beam_x_l - 45), sz(0), sz(GRATE_Z_TOP),
           f"{WALKWAY_H}mm DECK",
           offset=6 / H_SC, fs=5, font=FONT)

draw_dim_v(ax, sx(CUT_X + 40), sz(TRAY_FLOOR_Z), sz(BEAM_Z_BOT),
           f"{BEAM_Z_BOT - TRAY_FLOOR_Z:.0f}mm\nSPRAY HGT",
           offset=8 / H_SC, fs=4.5, font=FONT, right=True)

draw_dim_v(ax, sx(BV02_X - 60), sz(0), sz(bv_z),
           f"{int(bv_z)}mm BV-02",
           offset=8 / H_SC, fs=4.5, font=FONT)

# ── Notes (positioned low to avoid hiding graphics) ─────────────────────
notes = [
    "GANTRY ELEVATION — SECTION THROUGH NEAR WALKWAY:",
    f"1. 40×40×3mm AL SHS beam spans {BEAM_SPAN}mm. 1\" PVC pipe inside.",
    f"2. {SLIT_WIDTH}mm slit in walkway at beam center X for pole passage.",
    "3. BV-02 on pinhole wall at pinhole centerline, waist height → flex hose → center feed.",
    "4. 12mm apertures in beam, 2mm holes in PVC pipe.",
]
draw_notes(ax, notes, sx(X_LO + 85), sz(1800), spacing=20 / V_SC,
           fs=7, font=FONT, width=1600 / H_SC)

# ── Person silhouette (same style as hinge panel diagram) ───────────────
PERSON_H = 1780
HEAD_R = 80
oper_x = pole_x - 650
P_FOOT = GRATE_Z_TOP
P_HEAD = P_FOOT + PERSON_H
# Body (vertical line from feet to head center — head circle overlaps the join)
ax.plot([sx(oper_x), sx(oper_x)],
        [sz(P_FOOT), sz(P_HEAD + HEAD_R)],
        color="#2060A0", lw=3.0, zorder=13, solid_capstyle="round")
# Head (scatter marker — always a true circle regardless of axis scaling)
ax.scatter([sx(oper_x)], [sz(P_HEAD + HEAD_R)],
           s=1800, c="#70A8D8", edgecolors="#1A4D80", linewidths=1.0, zorder=14)
# Label
ax.text(sx(oper_x - 30), sz(P_FOOT + PERSON_H / 2),
        f"{PERSON_H}mm\noperator\n(shoes)",
        ha="right", va="center", fontsize=5, color="#1A4D80", **FONT, zorder=15)

view_ctr_x = (X_LO + X_HI) / 2
ax.text(sx(view_ctr_x), sz(Z_HI - 5),
        "GANTRY ELEVATION — VIEW FROM FILM PLANE",
        ha="center", va="top", fontsize=9, color=C_FRAME,
        fontweight="bold", **FONT, zorder=15)
ax.text(sx(view_ctr_x), sz(Z_HI - 22),
        "(H 1:18 / V 1:4.5 — 4× VERT EXAG — SECTION THROUGH NEAR WALKWAY)",
        ha="center", va="top", fontsize=5, color=C_DIM,
        **FONT, zorder=15)

# ── Walkway support risers (under left walkway grating) ─────────────────
riser_w = 6   # riser width in X (mm)
for rx in [wk_l + 30, wk_l + 150, wk_r - 30]:
    ax.add_patch(Rectangle((sx(rx - riser_w / 2), sz(TRAY_FLOOR_Z)),
                             riser_w / H_SC, (GRATE_Z_BOT - TRAY_FLOOR_Z) / V_SC,
                             fc="#B0B0B8", ec=C_FRAME, lw=0.5, zorder=7))

# ── Simplified beam end + carriage indicator ─────────────────────────
# Beam end cap and carriage assembly are fully detailed in panels A–E.
# This elevation shows only a simplified support indicator at the beam end.
carriage_cx = beam_x_l + 80

# Carriage support point on tray floor (triangle marker — fixed screen size)
ax.scatter([sx(carriage_cx)], [sz(TRAY_FLOOR_Z)],
           s=250, c=C_NYLON, edgecolors=C_WHEEL, linewidths=1.5,
           marker='v', zorder=10.5)
# Dashed line from support point up to beam bottom
ax.plot([sx(carriage_cx), sx(carriage_cx)],
        [sz(TRAY_FLOOR_Z), sz(BEAM_Z_BOT)],
        color=C_FRAME, lw=1.0, ls="--", zorder=10)

leader(ax, sx(carriage_cx + 10), sz(TRAY_FLOOR_Z - 3),
       sx(carriage_cx + 300), sz(TRAY_FLOOR_Z + 140),
       "CARRIAGE\n(SEE CROSS SECTION)",
       fs=5, color=C_WHEEL, font=FONT, zorder=15)

# ── Combined detail callout ──────────────────────────────────────────────
callout_cx = beam_x_l + 40
callout_cz = (TRAY_FLOOR_Z + BEAM_Z_TOP) / 2
ax.add_patch(mpatches.Ellipse((sx(callout_cx), sz(callout_cz)),
                               300 / H_SC, 90 / V_SC,
                               fc="none", ec="#CC0000", lw=1.5, ls="--", zorder=20))
ax.text(sx(callout_cx), sz(BEAM_Z_TOP + 30),
        "DETAIL A", ha="center", va="bottom", fontsize=7, color="#CC0000",
        fontweight="bold", **FONT, zorder=20)


# ─────────────────────────────────────────────────────────────────────────────
# Detail A: Beam end — open SHS with PVC pipe extending beyond
# PVC socket cap slides OVER pipe OD; pipe end seats against cap interior.
# X: along beam axis, - = outside (past beam end), + = inside (bore)
# Y: perpendicular to beam axis, 0 = beam centerline
# ─────────────────────────────────────────────────────────────────────────────
ax_a = fig.add_subplot(gs[2, 1])
ax_a.set_facecolor(C_BG)
ax_a.axis("off")

pvc_od_h = PVC_OD / 2
pvc_id_h = PVC_ID / 2
cap_od_h = pvc_od_h + CAP_WALL_T

beam_end_x = 0
pipe_end_x = beam_end_x - PVC_EXTEND
cap_open_x = pipe_end_x + CAP_SOCKET_DEPTH   # cap open edge (nearest beam)
cap_closed_x = pipe_end_x - CAP_CLOSED_T     # cap closed end (farthest)

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

# ── SHS top wall — cut section, hatched ──────────────────────────────────
ax_a.add_patch(Rectangle((beam_end_x, 17), d_xr - beam_end_x, 3,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=3))
# ── SHS bottom wall — cut section, hatched ───────────────────────────────
ax_a.add_patch(Rectangle((beam_end_x, -20), d_xr - beam_end_x, 3,
               fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0, hatch="///", zorder=3))

# ── Open beam end face (vertical line at X=0) ───────────────────────────
ax_a.plot([beam_end_x, beam_end_x], [-20, 20],
          color=C_FRAME, lw=1.5, zorder=5)

# ── Square bore inside beam ──────────────────────────────────────────────
ax_a.add_patch(Rectangle((beam_end_x, -17), d_xr - beam_end_x, 34,
               fc=C_BG, ec=C_FRAME, lw=0.5, zorder=3.5))

# ── PVC pipe walls (from pipe end through bore to far end) ──────────────
# Top wall (pipe runs from pipe_end_x to d_xr)
ax_a.add_patch(Rectangle((pipe_end_x, pvc_id_h), d_xr - pipe_end_x, PVC_WALL,
               fc=C_PVC, ec=C_FRAME, lw=0.6, zorder=4))
# Bottom wall
ax_a.add_patch(Rectangle((pipe_end_x, -pvc_od_h), d_xr - pipe_end_x, PVC_WALL,
               fc=C_PVC, ec=C_FRAME, lw=0.6, zorder=4))
# Pipe end face (inside cap — the butt joint)
ax_a.plot([pipe_end_x, pipe_end_x], [-pvc_od_h, pvc_od_h],
          color=C_FRAME, lw=1.0, zorder=5.5)

# ── PVC socket cap (slides OVER pipe OD — single U-shaped piece) ────────
cap_verts = [
    (cap_open_x,                  cap_od_h),     # outer top right
    (cap_closed_x,                cap_od_h),     # outer top left
    (cap_closed_x,               -cap_od_h),     # outer bottom left
    (cap_open_x,                 -cap_od_h),     # outer bottom right
    (cap_open_x,                 -pvc_od_h),     # step in at open edge
    (cap_closed_x + CAP_CLOSED_T, -pvc_od_h),   # inner bottom at end wall
    (cap_closed_x + CAP_CLOSED_T,  pvc_od_h),   # inner top at end wall
    (cap_open_x,                  pvc_od_h),     # inner top at open edge
]
ax_a.add_patch(mpatches.Polygon(cap_verts, closed=True,
               fc=C_PVC, ec=C_FRAME, lw=0.8, zorder=5))

# ── Solvent weld line (where pipe OD meets cap socket bore) ─────────────
ax_a.plot([cap_open_x, pipe_end_x], [pvc_od_h, pvc_od_h],
          color="#AA3030", lw=0.8, ls="--", zorder=6)
ax_a.plot([cap_open_x, pipe_end_x], [-pvc_od_h, -pvc_od_h],
          color="#AA3030", lw=0.8, ls="--", zorder=6)

# ── Water inside PVC pipe ────────────────────────────────────────────────
ax_a.add_patch(Rectangle((pipe_end_x, -pvc_id_h),
               d_xr - pipe_end_x, PVC_ID,
               fc=C_WATER, ec="none", alpha=0.15, zorder=3.8))

# ── Labels ────────────────────────────────────────────────────────────────
leader(ax_a, beam_end_x + 5, 19, beam_end_x + 20, d_yt - 8,
       "40×40×3 AL SHS\n(OPEN END)",
       fs=5, color=C_FRAME, font=FONT, zorder=20, bbox=_bbox_a)

leader(ax_a, (cap_open_x + beam_end_x/2)+20, pvc_od_h + CAP_WALL_T - 4,
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

ax_a.text((pipe_end_x + cap_closed_x + CAP_CLOSED_T) / 2 + 3, -PVC_OD+PVC_ID - 8.5,
          "BUTT\nJOINT",
          ha="center", va="center", fontsize=4, color="#AA3030",
          fontweight="bold", bbox=_bbox_a, **FONT, zorder=15)

# ── Dimensions ────────────────────────────────────────────────────────────
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



# ─────────────────────────────────────────────────────────────────────────────
# RIGHT PANEL — Combined Yd-Z cross section (beam assembly)
# Composite view looking along X: carriage, beam, ball joint, handle arm.
# Uniform 1:2 scale. Shows container wall, walkway, tray, carriage mechanics,
# ball joint, and arm tube.
# ─────────────────────────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(C_BG)
ax2.set_aspect("equal")
ax2.axis("off")

SC2 = 2.0

def cy(yd_mm):
    return 3.0 + yd_mm / SC2

def cz(z_mm):
    return 2.0 + z_mm / SC2

carriage_yd_center = 200
wheel1_yd = carriage_yd_center - WHEEL_SPACING_YD / 2
wheel2_yd = carriage_yd_center + WHEEL_SPACING_YD / 2

C_YD_LO = -60
C_YD_HI = 420
C_Z_LO  = -30
C_Z_HI  = 210

ax2.set_xlim(cy(C_YD_LO), cy(C_YD_HI))
ax2.set_ylim(cz(C_Z_LO), cz(C_Z_HI))

ax2.text(cy((C_YD_LO + C_YD_HI) / 2), cz(C_Z_HI - 3),
         "CROSS SECTION — BEAM ASSEMBLY",
         ha="center", va="top", fontsize=9, color=C_FRAME,
         fontweight="bold", **FONT, zorder=15)
ax2.text(cy((C_YD_LO + C_YD_HI) / 2), cz(C_Z_HI - 15),
         "(COMPOSITE — LOOKING ALONG X — SCALE 1:2)",
         ha="center", va="top", fontsize=5, color=C_DIM,
         **FONT, zorder=15)

_bbox_cs = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.85)

# ── Container pinhole wall (Yd=0) ────────────────────────────────────────
wall_w = 40
ax2.add_patch(Rectangle((cy(-wall_w), cz(C_Z_LO)),
                          wall_w / SC2, (C_Z_HI - C_Z_LO) / SC2,
                          fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
ax2.plot([cy(0), cy(0)], [cz(C_Z_LO), cz(C_Z_HI)],
         color=C_OUT, lw=2.0, zorder=3)

# ── Container floor ──────────────────────────────────────────────────────
ax2.plot([cy(C_YD_LO), cy(C_YD_HI)], [cz(0), cz(0)],
         color=C_OUT, lw=2.0, zorder=3)
ax2.add_patch(Rectangle((cy(C_YD_LO), cz(-20)),
                          (C_YD_HI - C_YD_LO) / SC2, 20 / SC2,
                          fc="#E0E0D8", ec=C_OUT, lw=0.8, hatch="...", zorder=1))

# ── Processing tray floor and near rim ───────────────────────────────────
tray_yd_start = PROC_TRAY_YD_NEAR
ax2.add_patch(Rectangle((cy(tray_yd_start), cz(0)),
                          (C_YD_HI - tray_yd_start) / SC2, TRAY_FLOOR_Z / SC2,
                          fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))
ax2.add_patch(Rectangle((cy(tray_yd_start - 3), cz(0)),
                          6 / SC2, PROC_TRAY_RIM / SC2,
                          fc=C_TRAY, ec=C_OUT, lw=1.2, zorder=5))

ax2.text(cy(340), cz(TRAY_FLOOR_Z + 6),
         "PROCESSING TRAY (304 SS)", ha="center", va="bottom",
         fontsize=5, color=C_DIM, style="italic", **FONT, zorder=10)

# ── Near walkway grating (Yd=0-300) ──────────────────────────────────────
wk_yd_l = 0
wk_yd_r = WALKWAY_W

ax2.add_patch(Rectangle((cy(wk_yd_l), cz(GRATE_Z_BOT)),
                          (wk_yd_r - wk_yd_l) / SC2, WALKWAY_GRATE_T / SC2,
                          fc=C_GRATE, ec=C_OUT, lw=0.8, alpha=0.20, zorder=10))
for frac in np.linspace(0.08, 0.92, 8):
    mesh_yd = wk_yd_l + (wk_yd_r - wk_yd_l) * frac
    ax2.plot([cy(mesh_yd), cy(mesh_yd)], [cz(GRATE_Z_BOT), cz(GRATE_Z_TOP)],
              color="#888888", lw=0.3, alpha=0.25, zorder=10)

ax2.text(cy((wk_yd_l + wk_yd_r) / 2), cz(GRATE_Z_TOP + 6),
         "NEAR WALKWAY (PROJECTED)", ha="center", va="bottom",
         fontsize=5, color=C_GRATE, style="italic", **FONT, zorder=10)

# Walkway support bracket (ghost)
brk_depth_r = 60
ax2.plot([cy(0), cy(0)], [cz(GRATE_Z_BOT - brk_depth_r), cz(GRATE_Z_BOT)],
         color=C_FRAME, lw=0.8, alpha=0.25, zorder=5)
ax2.plot([cy(0), cy(wk_yd_r)], [cz(GRATE_Z_BOT), cz(GRATE_Z_BOT)],
         color=C_FRAME, lw=0.6, alpha=0.25, zorder=5)
ax2.plot([cy(0), cy(wk_yd_r)],
         [cz(GRATE_Z_BOT - brk_depth_r), cz(GRATE_Z_BOT)],
         color=C_FRAME, lw=0.5, ls="--", alpha=0.25, zorder=5)

# ── Wheels (2× Ø50mm nylon) ──────────────────────────────────────────────
for w_yd in [wheel1_yd, wheel2_yd]:
    ax2.add_patch(Circle((cy(w_yd), cz(WHEEL_AXLE_Z)),
                            WHEEL_DIA / 2 / SC2,
                            fc=C_NYLON, ec=C_WHEEL, lw=2.0, zorder=6))
    ax2.add_patch(Circle((cy(w_yd), cz(WHEEL_AXLE_Z)),
                            3 / SC2, fc=C_WHEEL, ec=C_OUT, lw=0.5, zorder=6.5))
    ax2.plot([cy(w_yd - WHEEL_WIDTH / 2), cy(w_yd + WHEEL_WIDTH / 2)],
              [cz(TRAY_FLOOR_Z), cz(TRAY_FLOOR_Z)],
              color=C_WHEEL, lw=2.0, zorder=5)

leader(ax2, cy(wheel1_yd - WHEEL_DIA / 2), cz(WHEEL_AXLE_Z),
       cy(wheel1_yd - WHEEL_DIA / 2 - 30), cz(WHEEL_AXLE_Z - 10),
       f"Ø{WHEEL_DIA}mm\nNYLON WHEEL",
       fs=5, color=C_WHEEL, font=FONT, zorder=15)

# ── Fork brackets ────────────────────────────────────────────────────────
for w_yd in [wheel1_yd, wheel2_yd]:
    for offset in [-WHEEL_WIDTH / 2 - 2, WHEEL_WIDTH / 2 + 2]:
        ax2.plot([cy(w_yd + offset), cy(w_yd + offset)],
                  [cz(WHEEL_AXLE_Z + 6), cz(WHEEL_AXLE_Z - WHEEL_DIA / 2 + 4)],
                  color=C_FRAME, lw=1.2, zorder=5.5)
    ax2.plot([cy(w_yd - WHEEL_WIDTH / 2 - 4), cy(w_yd + WHEEL_WIDTH / 2 + 4)],
              [cz(WHEEL_AXLE_Z), cz(WHEEL_AXLE_Z)],
              color=C_FRAME, lw=0.8, zorder=6.5)

# ── L-bracket arm ────────────────────────────────────────────────────────
brk_t_c = 5
plate_yd_l = wheel1_yd - 18
plate_yd_r = wheel2_yd + 18

ax2.add_patch(Rectangle((cy(plate_yd_l), cz(WHEEL_AXLE_Z - brk_t_c / 2)),
                           (plate_yd_r - plate_yd_l) / SC2, brk_t_c / SC2,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=7))

leader(ax2, cy(plate_yd_r), cz(WHEEL_AXLE_Z),
       cy(plate_yd_r + 35), cz(WHEEL_AXLE_Z + 8),
       "AL L-BRACKET\nARM (5mm PLATE)",
       fs=5, color=C_FRAME, font=FONT, zorder=15)

# ── Fork-to-arm M5 through-bolts ────────────────────────────────────────
arm_top_z = WHEEL_AXLE_Z + brk_t_c / 2
arm_bot_z = WHEEL_AXLE_Z - brk_t_c / 2

for w_yd in [wheel1_yd, wheel2_yd]:
    for offset in [-WHEEL_WIDTH / 2 - 2, WHEEL_WIDTH / 2 + 2]:
        fork_yd = w_yd + offset
        ax2.add_patch(Rectangle((cy(fork_yd - 4), cz(arm_top_z)),
                                   8 / SC2, 3 / SC2,
                                   fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=11))
        ax2.add_patch(Rectangle((cy(fork_yd - 2.5), cz(arm_bot_z)),
                                   5 / SC2, brk_t_c / SC2,
                                   fc=C_BOLT, ec=C_FRAME, lw=0.4, zorder=11))
        ax2.add_patch(Rectangle((cy(fork_yd - 4), cz(arm_bot_z - 4)),
                                   8 / SC2, 4 / SC2,
                                   fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=11))

leader(ax2, cy(wheel2_yd + WHEEL_WIDTH / 2 + 2), cz(WHEEL_AXLE_Z),
       cy(wheel2_yd + 50), cz(WHEEL_AXLE_Z - 10),
       "M5 SS THRU-BOLT\n+ NYLOC NUT\n(1 PER FORK)",
       fs=4.5, color=C_BOLT, font=FONT, zorder=15)

# ── Beam / structural SHS cross-section with PVC pipe inside ────────────
c_beam_l = carriage_yd_center - BEAM_W / 2
c_beam_r = carriage_yd_center + BEAM_W / 2

ax2.add_patch(Rectangle((cy(c_beam_l), cz(BEAM_Z_BOT)),
                           BEAM_W / SC2, BEAM_W / SC2,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=2.5, zorder=8))
ax2.add_patch(Rectangle((cy(carriage_yd_center - BEAM_BORE / 2),
                            cz(BEAM_Z_BOT + BEAM_T)),
                           BEAM_BORE / SC2, BEAM_BORE / SC2,
                           fc=C_BG, ec=C_FRAME, lw=0.8, zorder=8.5))
ax2.add_patch(Circle((cy(carriage_yd_center), cz(BEAM_Z_BOT + BEAM_W / 2)),
                         PVC_OD / 2 / SC2,
                         fc=C_PVC, ec=C_FRAME, lw=1.0, alpha=0.7, zorder=8.7))
ax2.add_patch(Circle((cy(carriage_yd_center), cz(BEAM_Z_BOT + BEAM_W / 2)),
                         PVC_ID / 2 / SC2,
                         fc=C_WATER, ec=C_FRAME, lw=0.5, alpha=0.4, zorder=8.8))

# 2mm hole drilled through PVC pipe wall at bottom
pipe_cz = BEAM_Z_BOT + BEAM_W / 2
pipe_od_bot_z = pipe_cz - PVC_OD / 2
pipe_id_bot_z = pipe_cz - PVC_ID / 2
PIPE_HOLE_DIA = 2
ax2.add_patch(Rectangle((cy(carriage_yd_center - PIPE_HOLE_DIA / 2), cz(pipe_od_bot_z)),
                           PIPE_HOLE_DIA / SC2, PVC_WALL / SC2,
                           fc=C_WATER, ec=C_FRAME, lw=0.5, alpha=0.5, zorder=9.1))

ax2.text(cy(carriage_yd_center), cz(BEAM_Z_TOP + 4),
          "40×40×3mm AL SHS\n+ 1\" PVC PIPE", ha="center", va="bottom",
          fontsize=5.5, color=C_FRAME, fontweight="bold", **FONT, zorder=15)

# ── U-clamp over beam ─────────────────────────────────────────────────
uc_l = carriage_yd_center - BEAM_W / 2 - UC_T - UC_GAP
uc_r = carriage_yd_center + BEAM_W / 2 + UC_GAP + UC_T
flare_l = uc_l - UC_FLARE
flare_r = uc_r + UC_FLARE

ax2.add_patch(Rectangle((cy(uc_l), cz(BEAM_Z_TOP)),
                           (uc_r - uc_l) / SC2, UC_T / SC2,
                           fc=C_UCLAMP, ec=C_FRAME, lw=1.0, zorder=10))
for u_yd in [uc_l, uc_r - UC_T]:
    ax2.add_patch(Rectangle((cy(u_yd), cz(BEAM_Z_BOT + UC_T)),
                               UC_T / SC2,
                               (BEAM_Z_TOP - BEAM_Z_BOT - UC_T) / SC2,
                               fc=C_UCLAMP, ec=C_FRAME, lw=0.8, zorder=10))
ax2.add_patch(Rectangle((cy(flare_l), cz(BEAM_Z_BOT)),
                           (uc_l + UC_T - flare_l) / SC2, UC_T / SC2,
                           fc=C_UCLAMP, ec=C_FRAME, lw=0.8, zorder=10))
ax2.add_patch(Rectangle((cy(uc_r - UC_T), cz(BEAM_Z_BOT)),
                           (flare_r - uc_r + UC_T) / SC2, UC_T / SC2,
                           fc=C_UCLAMP, ec=C_FRAME, lw=0.8, zorder=10))

for bolt_yd in [flare_l + UC_FLARE / 2, flare_r - UC_FLARE / 2]:
    ax2.add_patch(Rectangle((cy(bolt_yd - 2.5), cz(arm_bot_z - 4)),
                               5 / SC2, (BEAM_Z_BOT + UC_T - arm_bot_z + 4) / SC2,
                               fc=C_BOLT, ec=C_FRAME, lw=0.5, zorder=11))
    ax2.add_patch(Rectangle((cy(bolt_yd - 4), cz(BEAM_Z_BOT + UC_T)),
                               8 / SC2, 3 / SC2,
                               fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=11))
    ax2.add_patch(Rectangle((cy(bolt_yd - 5), cz(arm_bot_z - 8)),
                               10 / SC2, 4 / SC2,
                               fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=11))

leader(ax2, cy(flare_r), cz(BEAM_Z_BOT + UC_T / 2),
       cy(flare_r + 20), cz(BEAM_Z_BOT - 5),
       "SS U-CLAMP\n+ WING NUTS",
       fs=4.5, color=C_BOLT, font=FONT, zorder=15)

# 12mm aperture + water jet
ax2.add_patch(Rectangle((cy(carriage_yd_center - APERTURE_DIA / 2), cz(BEAM_Z_BOT - 0.5)),
                           APERTURE_DIA / SC2, (BEAM_T + 1) / SC2,
                           fc=C_BG, ec=C_FRAME, lw=0.5, zorder=9))
ax2.plot([cy(carriage_yd_center), cy(carriage_yd_center)],
          [cz(pipe_id_bot_z), cz(BEAM_Z_BOT - 16)],
          color=C_WATER, lw=1.2, alpha=0.6, zorder=9.2)
leader(ax2, cy(carriage_yd_center + PIPE_HOLE_DIA / 2 + 1), cz(pipe_od_bot_z + PVC_WALL / 2),
       cy(carriage_yd_center + 28), cz(pipe_od_bot_z - 6),
       f"2mm PIPE HOLE",
       fs=4.5, color=C_WATER, font=FONT, zorder=15)
ax2.text(cy(carriage_yd_center + 4), cz(BEAM_Z_BOT - 5),
          f"12mm APERTURE (TYP. @{SPRAY_BAR_HOLE_SP}mm c/c)",
          ha="left", va="center", fontsize=4.5, color=C_WATER, **FONT, zorder=15)

# ── Detail C callout ─────────────────────────────────────────────────────
ax2.add_patch(Circle((cy(wheel1_yd), cz(WHEEL_AXLE_Z)),
                        (WHEEL_DIA / 2 + 8) / SC2,
                        fc="none", ec="#008800", lw=1.5, ls="--", zorder=20))
ax2.text(cy(wheel1_yd), cz(WHEEL_AXLE_Z + WHEEL_DIA / 2 + 10),
          "C", ha="center", va="bottom", fontsize=9, color="#008800",
          fontweight="bold", **FONT, zorder=20)

# ── Ball joint on beam top face ───────────────────────────────────────
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

# Saddle plate
ax2.add_patch(Rectangle((cy(carriage_yd_center - FLANGE_W / 2), cz(flange_bot_z)),
                           FLANGE_W / SC2, FLANGE_T / SC2,
                           fc="#B0B0B8", ec=C_FRAME, lw=1.2, zorder=7))

# U-bolt wrapping over socket housing
ubolt_gap = 2
ubolt_t = 4
ubolt_l = carriage_yd_center - SOCKET_OD / 2 - ubolt_gap - ubolt_t
ubolt_r = carriage_yd_center + SOCKET_OD / 2 + ubolt_gap + ubolt_t

ub_arc = np.linspace(0, np.pi, 30)
ub_arc_r = (ubolt_r - ubolt_l) / 2
ub_arc_cz = socket_bot_z + SOCKET_H * 0.6
ub_arc_yd = carriage_yd_center + ub_arc_r * np.cos(ub_arc)
ub_arc_z = ub_arc_cz + ub_arc_r * 0.45 * np.sin(ub_arc)
ax2.plot([cy(y) for y in ub_arc_yd], [cz(z) for z in ub_arc_z],
          color=C_BOLT, lw=2.5, zorder=9, solid_capstyle="round")

ax2.plot([cy(ubolt_l + ubolt_t / 2), cy(ubolt_l + ubolt_t / 2)],
          [cz(ub_arc_cz), cz(beam_top_z_bj - BEAM_T - 5)],
          color=C_BOLT, lw=2.5, zorder=9)
ax2.plot([cy(ubolt_r - ubolt_t / 2), cy(ubolt_r - ubolt_t / 2)],
          [cz(ub_arc_cz), cz(beam_top_z_bj - BEAM_T - 5)],
          color=C_BOLT, lw=2.5, zorder=9)

for nut_yd in [ubolt_l + ubolt_t / 2, ubolt_r - ubolt_t / 2]:
    ax2.add_patch(Rectangle((cy(nut_yd - 5), cz(beam_top_z_bj - BEAM_T - 8)),
                               10 / SC2, 4 / SC2,
                               fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=10))

# Socket housing
ax2.add_patch(Rectangle((cy(carriage_yd_center - SOCKET_OD / 2), cz(socket_bot_z)),
                           SOCKET_OD / SC2, SOCKET_H / SC2,
                           fc=C_JOINT, ec=C_FRAME, lw=1.5, hatch="///",
                           zorder=6))
bore_r = BALL_DIA / 2 + 1
ax2.add_patch(Circle((cy(carriage_yd_center), cz(ball_ctr_z)),
                         bore_r / SC2,
                         fc=C_BG, ec=C_FRAME, lw=0.5, zorder=6.5))

# Ball
ax2.add_patch(Circle((cy(carriage_yd_center), cz(ball_ctr_z)),
                         BALL_DIA / 2 / SC2,
                         fc="#E0D8C0", ec=C_FRAME, lw=1.5, zorder=7))

# Stud
ax2.add_patch(Rectangle((cy(carriage_yd_center - STUD_DIA / 2), cz(ball_ctr_z)),
                           STUD_DIA / SC2, (stud_top_z - ball_ctr_z) / SC2,
                           fc="#D0C8B0", ec=C_FRAME, lw=1.0, zorder=7.5))

# ── Round tube arm ────────────────────────────────────────────────────
ARM_OD = 25
ARM_WALL = 2
ARM_ID = ARM_OD - 2 * ARM_WALL
arm_base_z_bj = stud_top_z - STUD_EXT + 2
arm_top_z_bj = arm_base_z_bj + 80

ax2.add_patch(Rectangle((cy(carriage_yd_center - ARM_OD / 2), cz(arm_base_z_bj)),
                           ARM_OD / SC2, (arm_top_z_bj - arm_base_z_bj) / SC2,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=8))
ax2.add_patch(Rectangle((cy(carriage_yd_center - ARM_ID / 2), cz(arm_base_z_bj)),
                           ARM_ID / SC2, (stud_top_z - arm_base_z_bj) / SC2,
                           fc="#D0C8B0", ec="none", zorder=8.3))
ax2.add_patch(Rectangle((cy(carriage_yd_center - ARM_ID / 2), cz(stud_top_z)),
                           ARM_ID / SC2, (arm_top_z_bj - stud_top_z) / SC2,
                           fc=C_BG, ec=C_FRAME, lw=0.5, zorder=8.5))

# Pinch bolt
pinch_z = arm_base_z_bj + 12
ax2.add_patch(Rectangle((cy(carriage_yd_center + ARM_OD / 2), cz(pinch_z - 2)),
                           8 / SC2, 4 / SC2,
                           fc=C_BOLT, ec=C_FRAME, lw=0.6, zorder=9))
ax2.plot([cy(carriage_yd_center + ARM_ID / 2), cy(carriage_yd_center + ARM_OD / 2 + 8)],
          [cz(pinch_z), cz(pinch_z)],
          color=C_BOLT, lw=1.5, zorder=9)

# Continuation arrow
ax2.annotate("", xy=(cy(carriage_yd_center), cz(arm_top_z_bj + 8)),
              xytext=(cy(carriage_yd_center), cz(arm_top_z_bj)),
              arrowprops=dict(arrowstyle="->", color=C_FRAME, lw=1.5),
              zorder=12)
ax2.text(cy(carriage_yd_center + 3), cz(arm_top_z_bj + 5),
          "ARM CONTINUES\nTO TRAY SURFACE",
          ha="left", va="center", fontsize=4.5, color=C_DIM,
          style="italic", **FONT, zorder=15)

# Movement arcs
for arc_ang in [-25, 25]:
    ang_rad = np.radians(arc_ang)
    arc_len = 35
    ax2.annotate("",
        xy=(cy(carriage_yd_center + arc_len * np.sin(ang_rad)),
            cz(ball_ctr_z + arc_len * np.cos(ang_rad))),
        xytext=(cy(carriage_yd_center), cz(ball_ctr_z)),
        arrowprops=dict(arrowstyle="->", color="#AA0000", lw=0.8,
                        connectionstyle=f"arc3,rad={0.3 if arc_ang > 0 else -0.3}"),
        zorder=12)
ax2.text(cy(carriage_yd_center - SOCKET_OD / 2 - 5), cz(ball_ctr_z + 20),
          "MULTI-AXIS\nARTICULATION",
          ha="right", va="center", fontsize=4.5, color="#AA0000",
          bbox=_bbox_cs, **FONT, zorder=15)

# ── Water hose zip-tied to arm ────────────────────────────────────────
hose_od = 16
hose_ctr_yd = carriage_yd_center + ARM_OD / 2 + hose_od / 2 + 3

ax2.add_patch(Rectangle((cy(hose_ctr_yd - hose_od / 2), cz(arm_base_z_bj - 5)),
                           hose_od / SC2, (arm_top_z_bj - arm_base_z_bj + 10) / SC2,
                           fc=C_HOSE, ec=C_BLUE, lw=1.0, alpha=0.6, zorder=7.5))

for zt_z in [arm_base_z_bj + 15, arm_base_z_bj + 40, arm_base_z_bj + 65]:
    zt_l = carriage_yd_center - ARM_OD / 2 - 4
    zt_r = hose_ctr_yd + hose_od / 2 + 2
    ax2.add_patch(Rectangle((cy(zt_l), cz(zt_z - 1.5)),
                               (zt_r - zt_l) / SC2, 3 / SC2,
                               fc="none", ec="#222222", lw=1.2, zorder=11))
    ax2.add_patch(Rectangle((cy(zt_l - 2), cz(zt_z - 2)),
                               2 / SC2, 4 / SC2,
                               fc="#333333", ec="#222222", lw=0.5, zorder=11))

# ── Labels ────────────────────────────────────────────────────────────
leader(ax2, cy(carriage_yd_center + SOCKET_OD / 2), cz(ball_ctr_z),
       cy(carriage_yd_center + SOCKET_OD / 2 + 20), cz(ball_ctr_z - 30),
       f"Ø{BALL_DIA}mm BALL JOINT\n(U-BOLT TO BEAM)",
       fs=5, color=C_JOINT, font=FONT, zorder=20)

leader(ax2, cy(ubolt_r), cz(ub_arc_cz),
       cy(ubolt_r + 22), cz(ub_arc_cz - 8),
       "M8 SS U-BOLT\n+ NYLOC NUTS",
       fs=4.5, color=C_BOLT, font=FONT, zorder=20)

leader(ax2, cy(carriage_yd_center + ARM_OD / 2 + 8), cz(pinch_z),
       cy(carriage_yd_center + 35), cz(pinch_z + 12),
       "M6 PINCH BOLT",
       fs=4.5, color=C_BOLT, font=FONT, zorder=20)

leader(ax2, cy(carriage_yd_center + ARM_OD / 2), cz(arm_base_z_bj + 50),
       cy(carriage_yd_center + 45), cz(arm_base_z_bj + 62),
       f"Ø{ARM_OD}mm AL TUBE\n(2mm WALL)",
       fs=5, color=C_FRAME, font=FONT, zorder=20)

leader(ax2, cy(hose_ctr_yd), cz(arm_base_z_bj + 55),
       cy(hose_ctr_yd + 20), cz(arm_base_z_bj + 75),
       "1/2\" FLEX HOSE\n(ZIP-TIED)",
       fs=5, color=C_HOSE, font=FONT, zorder=20)

# ── Dimensions ───────────────────────────────────────────────────────
draw_dim_v(ax2, cy(c_beam_l - 10), cz(BEAM_Z_BOT), cz(BEAM_Z_TOP),
           f"{BEAM_W}mm", offset=6 / SC2, fs=5.5, font=FONT)

draw_dim_h(ax2, cy(wheel1_yd), cy(wheel2_yd),
           cz(TRAY_FLOOR_Z + WHEEL_DIA + 8),
           f"{WHEEL_SPACING_YD}mm WHEEL SPACING",
           offset=6 / SC2, fs=5, font=FONT)

clearance_c = GRATE_Z_BOT - BEAM_Z_TOP
draw_dim_v(ax2, cy(c_beam_r + 10), cz(BEAM_Z_TOP), cz(GRATE_Z_BOT),
           f"{clearance_c:.0f}mm\nCLR", offset=6 / SC2, fs=5, font=FONT, right=True)

draw_dim_v(ax2, cy(c_beam_l - 22), cz(TRAY_FLOOR_Z), cz(BEAM_Z_BOT),
           f"{BEAM_Z_BOT - TRAY_FLOOR_Z:.0f}mm\nSPRAY",
           offset=6 / SC2, fs=4.5, font=FONT)

draw_dim_h(ax2, cy(wk_yd_l), cy(wk_yd_r), cz(GRATE_Z_TOP + 18),
           f"{WALKWAY_W}mm WALKWAY", offset=6 / SC2, fs=5, font=FONT)

draw_dim_v(ax2, cy(C_YD_HI - 20), cz(0), cz(GRATE_Z_TOP),
           f"{WALKWAY_H}mm\nDECK HGT",
           offset=6 / SC2, fs=5, font=FONT, right=True)

draw_dim_v(ax2, cy(c_beam_l - 34), cz(beam_top_z_bj), cz(socket_top_z),
           f"{int(socket_top_z - beam_top_z_bj)}mm\nJOINT",
           offset=6 / SC2, fs=4.5, font=FONT)

# ── Notes ────────────────────────────────────────────────────────────
cs_notes = [
    "CROSS SECTION (COMPOSITE):",
    "1. Beam rides on 2× Ø50mm nylon wheels (push/pull via pole).",
    "2. Ball joint on beam top → arm → pole through walkway slit.",
    "3. Water: PVC pipe → 2mm hole → 12mm aperture → spray.",
]
draw_notes(ax2, cs_notes, cy(C_YD_LO + 10), cz(C_Z_HI - 260), spacing=5 / SC2,
           fs=7, font=FONT, width=100 / SC2)

# ─────────────────────────────────────────────────────────────────────────────
# DETAIL C INSET — Wheel attachment (section along axle centerline)
# Shows fork bracket arms, nylon wheel bore, axle pin, snap-ring retention,
# and connection to L-bracket horizontal arm.
# ─────────────────────────────────────────────────────────────────────────────
ax_w = fig.add_subplot(gs[1, 0])
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

# ── Dimensions ────────────────────────────────────────────────────────────
draw_dim_h(ax_w, -10, 10, w_yb + 3,
           "20mm", offset=2, fs=5.5, font=FONT)

draw_dim_v(ax_w, w_xl + 2, -5, 5,
           "Ø10", offset=2, fs=5, font=FONT)


# ─────────────────────────────────────────────────────────────────────────────
# DETAIL D — Wheel attachment plan view (X-Yd, looking down)
# Beam runs left-right in X (long rectangle).  Wheels above/below in Yd.
# ─────────────────────────────────────────────────────────────────────────────
ax_d = fig.add_subplot(gs[1, 1])
ax_d.set_facecolor(C_BG)
ax_d.axis("off")

SC_D = 2.0
BEAM_SHOW_LEN = 140  # mm of beam shown on each side of center
CARRIAGE_OFFSET_X = -BEAM_SHOW_LEN + 20  # carriage at beam end

D_X_LO = -BEAM_SHOW_LEN - 20
D_X_HI = BEAM_SHOW_LEN + 20
D_YD_LO = -WHEEL_SPACING_YD / 2 - 40
D_YD_HI = WHEEL_SPACING_YD / 2 + 40

ax_d.set_xlim(D_X_LO / SC_D, D_X_HI / SC_D)
ax_d.set_ylim(D_YD_LO / SC_D, D_YD_HI / SC_D)
ax_d.set_aspect("equal")

def px(x_mm):
    return x_mm / SC_D

def py_d(yd_mm):
    return yd_mm / SC_D

ax_d.text(px(0), py_d(D_YD_HI - 2),
          "DETAIL D — WHEEL ATTACHMENT PLAN",
          ha="center", va="top", fontsize=8, color="#AA6600",
          fontweight="bold", **FONT, zorder=20)
ax_d.text(px(0), py_d(D_YD_HI - 10),
          "(LOOKING DOWN — SCALE 1:2)",
          ha="center", va="top", fontsize=5, color=C_DIM,
          **FONT, zorder=20)

_bbox_d = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.85)

# ── Beam (plan view — long rectangle running in X, 40mm wide in Yd) ─────
ax_d.add_patch(Rectangle((px(-BEAM_SHOW_LEN), py_d(-BEAM_W / 2)),
                           2 * BEAM_SHOW_LEN / SC_D, BEAM_W / SC_D,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=2.0, zorder=5))
# Bore (long rectangle inside — 34mm wide in Yd)
ax_d.add_patch(Rectangle((px(-BEAM_SHOW_LEN), py_d(-BEAM_BORE / 2)),
                           2 * BEAM_SHOW_LEN / SC_D, BEAM_BORE / SC_D,
                           fc=C_BG, ec=C_FRAME, lw=0.5, zorder=5.5))
# PVC pipe inside bore (rectangle — 33.4mm wide in Yd, full length)
ax_d.add_patch(Rectangle((px(-BEAM_SHOW_LEN), py_d(-PVC_OD / 2)),
                           2 * BEAM_SHOW_LEN / SC_D, PVC_OD / SC_D,
                           fc=C_PVC, ec=C_FRAME, lw=0.6, alpha=0.6, zorder=5.7))
# Water inside PVC pipe
ax_d.add_patch(Rectangle((px(-BEAM_SHOW_LEN), py_d(-PVC_ID / 2)),
                           2 * BEAM_SHOW_LEN / SC_D, PVC_ID / SC_D,
                           fc=C_WATER, ec="none", alpha=0.3, zorder=5.8))
# Break lines at beam ends (indicating continuation)
for bx in [-BEAM_SHOW_LEN, BEAM_SHOW_LEN]:
    ax_d.plot([px(bx), px(bx)], [py_d(-BEAM_W / 2 - 3), py_d(BEAM_W / 2 + 3)],
              color=C_FRAME, lw=1.5, ls=(0, (5, 3)), zorder=6)

ax_d.text(px(60), py_d(0),
          "40×40 SHS\n+ 1\" PVC",
          ha="center", va="center", fontsize=4.5, color=C_FRAME,
          bbox=_bbox_d, **FONT, zorder=15)

# ── L-bracket arm (horizontal plate spanning both wheels, runs in Yd) ───
arm_half_span = WHEEL_SPACING_YD / 2 + 18
arm_w_x = 20
ax_d.add_patch(Rectangle((px(CARRIAGE_OFFSET_X - arm_w_x / 2), py_d(-arm_half_span)),
                           arm_w_x / SC_D, (2 * arm_half_span) / SC_D,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0,
                           hatch="///", alpha=0.7, zorder=4))

# ── U-clamp top plate (visible from above — spans Yd across beam) ──────
uc_w_yd_top = BEAM_W + 2 * UC_T + 2 * UC_GAP
ax_d.add_patch(Rectangle((px(CARRIAGE_OFFSET_X - arm_w_x / 2), py_d(-uc_w_yd_top / 2)),
                           arm_w_x / SC_D, uc_w_yd_top / SC_D,
                           fc=C_UCLAMP, ec=C_FRAME, lw=1.0, alpha=0.5, zorder=6))
# Flared feet (extend outward in Yd)
for side in [-1, 1]:
    foot_yd = side * (BEAM_W / 2 + UC_GAP + UC_T)
    if side < 0:
        foot_yd -= UC_FLARE
    ax_d.add_patch(Rectangle((px(CARRIAGE_OFFSET_X - arm_w_x / 2), py_d(foot_yd)),
                               arm_w_x / SC_D, (UC_FLARE + UC_T) / SC_D,
                               fc=C_UCLAMP, ec=C_FRAME, lw=0.8, alpha=0.6, zorder=6))

# Bolt holes through flared feet
for side in [-1, 1]:
    bolt_yd = side * (BEAM_W / 2 + UC_GAP + UC_T + UC_FLARE / 2)
    ax_d.add_patch(Circle((px(CARRIAGE_OFFSET_X), py_d(bolt_yd)),
                            3 / SC_D,
                            fc=C_BOLT, ec=C_FRAME, lw=0.5, zorder=8))

leader(ax_d, px(CARRIAGE_OFFSET_X + arm_w_x / 2),
       py_d(BEAM_W / 2 + UC_GAP + UC_T + UC_FLARE),
       px(BEAM_W - 100), py_d(BEAM_W / 2 + 30),
       "U-CLAMP\nFLARED LEGS\n+ WING NUTS",
       fs=5, color=C_BOLT, font=FONT, zorder=20)

# ── Fork brackets (vertical plates straddling each wheel) ────────────────
fork_t = 6
for w_sign in [-1, 1]:
    w_yd_ctr = w_sign * WHEEL_SPACING_YD / 2
    for offset in [-WHEEL_WIDTH / 2 - 2, WHEEL_WIDTH / 2 + 2]:
        fork_yd = w_yd_ctr + offset
        ax_d.add_patch(Rectangle((px(CARRIAGE_OFFSET_X - fork_t / 2 - 4),
                                   py_d(fork_yd - 1)),
                                   fork_t / SC_D, 2 / SC_D,
                                   fc=C_ALUM_FILL, ec=C_FRAME, lw=0.6, zorder=7))

# ── Wheels (footprint — rectangles: WHEEL_WIDTH in X, WHEEL_DIA in Yd) ──
# Wheels roll in Yd; axle runs in X → narrow in X, tall in Yd
for w_sign in [-1, 1]:
    w_yd_ctr = w_sign * WHEEL_SPACING_YD / 2
    ax_d.add_patch(Rectangle((px(CARRIAGE_OFFSET_X - WHEEL_WIDTH / 2),
                               py_d(w_yd_ctr - WHEEL_DIA / 2)),
                               WHEEL_WIDTH / SC_D, WHEEL_DIA / SC_D,
                               fc=C_NYLON, ec=C_WHEEL, lw=1.5, alpha=0.6, zorder=3))
    ax_d.add_patch(Circle((px(CARRIAGE_OFFSET_X), py_d(w_yd_ctr)),
                            5 / SC_D,
                            fc="#D0D0D8", ec=C_FRAME, lw=0.5, zorder=7))

# ── Labels ──────────────────────────────────────────────────────────────
leader(ax_d, px(CARRIAGE_OFFSET_X + WHEEL_WIDTH / 2),
       py_d(-WHEEL_SPACING_YD / 2),
       px(D_X_HI - 225), py_d(-WHEEL_SPACING_YD / 2 - 10),
       f"Ø{WHEEL_DIA}mm WHEEL\n({WHEEL_WIDTH}mm WIDE)",
       fs=5, color=C_WHEEL, font=FONT, zorder=20)

leader(ax_d, px(-arm_w_x / 2 - 1), py_d(0),
       px(D_X_LO + 200), py_d(45),
       "L-BRACKET ARM\n(5mm AL PLATE)",
       fs=5, color=C_FRAME, font=FONT, zorder=20)

# ── Dimensions ──────────────────────────────────────────────────────────
draw_dim_v(ax_d, px(D_X_LO + 12),
           py_d(-WHEEL_SPACING_YD / 2), py_d(WHEEL_SPACING_YD / 2),
           f"{WHEEL_SPACING_YD}mm WHEEL SPACING",
           offset=3 / SC_D, fs=5, font=FONT)

# ─────────────────────────────────────────────────────────────────────────────
# PLAN VIEW — Container floor plan showing walkways, tray, and slit positions
# Looking down (X horizontal, Yd vertical).  Scaled to fit panel.
# ─────────────────────────────────────────────────────────────────────────────
ax_p = fig.add_subplot(gs[2, 0])
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
ax_p.text(ppx((PROC_TRAY_X_L + PROC_TRAY_X_R) / 2), ppy(C_WID / 3),
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

# ── Slits in near & far walkways (for pole/arm to slide through) ─────────
# Pole is at beam center X — single slit at tray centerline on each walkway
pole_x = (PROC_OPEN_X_L + PROC_OPEN_X_R) / 2
slit_x = pole_x - SLIT_WIDTH / 2

# Near walkway slit
ax_p.add_patch(Rectangle((ppx(slit_x), ppy(0)),
                           SLIT_WIDTH / SC_P, WALKWAY_W / SC_P,
                           fc="#FF4444", ec="#CC0000", lw=1.5, alpha=0.6, zorder=7))
# Far walkway slit (same X, mirrored Yd)
ax_p.add_patch(Rectangle((ppx(slit_x), ppy(WALKWAY_FAR_YD)),
                           SLIT_WIDTH / SC_P, WALKWAY_W / SC_P,
                           fc="#FF4444", ec="#CC0000", lw=1.5, alpha=0.6, zorder=7))

# Slit label
leader(ax_p, ppx(pole_x), ppy(-10),
       ppx(pole_x - 500), ppy(-220),
       f"{SLIT_WIDTH}mm SLIT @ BEAM\nCENTER (NEAR & FAR\nWALKWAYS — FOR POLE)",
       fs=5, color="#CC0000", font=FONT, zorder=20)

# Centerline through slits (showing pole alignment)
ax_p.plot([ppx(pole_x), ppx(pole_x)],
          [ppy(-5), ppy(WALKWAY_W + 5)],
          color="#CC0000", lw=0.8, ls="-.", zorder=6.5)
ax_p.plot([ppx(pole_x), ppx(pole_x)],
          [ppy(WALKWAY_FAR_YD - 5), ppy(C_WID + 5)],
          color="#CC0000", lw=0.8, ls="-.", zorder=6.5)

# ── Beam position (example — dashed line across tray) ────────────────────
beam_example_yd = PROC_TRAY_YD_NEAR + PROC_TRAY_D / 2
ax_p.plot([ppx(PROC_OPEN_X_L), ppx(PROC_OPEN_X_R)],
          [ppy(beam_example_yd), ppy(beam_example_yd)],
          color=C_FRAME, lw=1.5, ls="--", zorder=6)
ax_p.text(ppx((PROC_OPEN_X_L + PROC_OPEN_X_R) / 2), ppy(beam_example_yd + 90),
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


# ── Full-width title block ────────────────────────────────────────────────
ax_tb = fig.add_axes([0.04, 0.005, 0.92, 0.045])
ax_tb.set_xlim(0, 1)
ax_tb.set_ylim(0, 1)
ax_tb.axis("off")
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
