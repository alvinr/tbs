#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_spray_bar_diagram.py
Spray bar assembly detail for TBS-001 processing tray wash system.

Sheet 1 — Gantry spray bar:
  Left panel:  Yd-Z cross-section (operator view) looking along X.
               Equal 1:4 scale. Walkway, beam, wheels, U-clamp.
  Right panel: X-Z section viewed from film plane (along Yd).
               Centered on beam centerline. Walkway slit, pole,
               beam (full span), BV-02, flex hose. H1:18 / V1:4.5.

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
# RIGHT PANEL — X-Z section viewed from film plane (looking along Yd)
# Centered on beam centerline.  Shows walkway slit, pole, beam, BV-02.
# Horizontal scale 1:18, Vertical scale 1:4.5 (4× vert exaggeration)
# ─────────────────────────────────────────────────────────────────────────────
ax = fig.add_subplot(gs[0, 1])
ax.set_facecolor(C_BG)
ax.axis("off")

H_SC = 18.0
V_SC = 4.5

def sx(x_mm):
    return 1.0 + x_mm / H_SC

def sz(z_mm):
    return 1.0 + z_mm / V_SC

pole_x = (PROC_OPEN_X_L + PROC_OPEN_X_R) / 2
BV02_X = PROC_OPEN_X_L + 200

X_LO = -100
X_HI = 5100
Z_LO = -50
Z_HI = 1100

ax.set_xlim(sx(X_LO), sx(X_HI))
ax.set_ylim(sz(Z_LO), sz(Z_HI))

# ── Container floor ──────────────────────────────────────────────────────
ax.plot([sx(X_LO), sx(X_HI)], [sz(0), sz(0)], color=C_OUT, lw=2.0, zorder=3)
ax.add_patch(Rectangle((sx(X_LO), sz(-25)),
                         (X_HI - X_LO) / H_SC, 25 / V_SC,
                         fc="#E0E0D8", ec=C_OUT, lw=0.8, hatch="...", zorder=1))

# ── Container side walls ────────────────────────────────────────────────
wall_vis_t = WALL_T * 6
for wall_x in [0, C_LEN]:
    ax.add_patch(Rectangle((sx(wall_x - wall_vis_t / 2), sz(Z_LO)),
                             wall_vis_t / H_SC, (Z_HI - Z_LO) / V_SC,
                             fc=C_WALL, ec=C_OUT, lw=1.0, hatch="///", zorder=2))
ax.text(sx(0), sz(Z_HI - 30), "CONTAINER\nWALL (X=0)",
        ha="center", va="top", fontsize=4.5, color=C_DIM, **FONT)
ax.text(sx(C_LEN), sz(Z_HI - 30), f"CONTAINER\nWALL (X={C_LEN})",
        ha="center", va="top", fontsize=4.5, color=C_DIM, **FONT)

# ── Processing tray ──────────────────────────────────────────────────────
tray_x_l = PROC_TRAY_X_L
tray_x_r = PROC_TRAY_X_R

ax.add_patch(Rectangle((sx(tray_x_l), sz(0)),
                         (tray_x_r - tray_x_l) / H_SC, TRAY_FLOOR_Z / V_SC,
                         fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))
for rim_x in [tray_x_l, tray_x_r]:
    rim_w = 4
    ax.add_patch(Rectangle((sx(rim_x - rim_w / 2), sz(0)),
                             rim_w / H_SC, PROC_TRAY_RIM / V_SC,
                             fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=5))

ax.text(sx(pole_x), sz(TRAY_FLOOR_Z + 3),
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

# ── Right walkway grating (X=4329-4629) ─────────────────────────────────
wk_r_l = WALKWAY_RIGHT_X
wk_r_r = PROC_TRAY_X_R

ax.add_patch(Rectangle((sx(wk_r_l), sz(GRATE_Z_BOT)),
                         (wk_r_r - wk_r_l) / H_SC, WALKWAY_GRATE_T / V_SC,
                         fc=C_GRATE, ec=C_OUT, lw=1.2, zorder=8))
ax.text(sx((wk_r_l + wk_r_r) / 2), sz(GRATE_Z_TOP + 5),
        "RIGHT WK", ha="center", va="bottom",
        fontsize=4.5, color=C_GRATE, fontweight="bold", **FONT, zorder=10)

# ── Near walkway slit at pole_x (cross-section through walkway) ─────────
SLIT_WIDTH = 30
slit_x_l = pole_x - SLIT_WIDTH / 2
slit_x_r = pole_x + SLIT_WIDTH / 2

# Near walkway grating runs full X span at Yd=0-300 — shown as thin strip
# at deck height. Section through slit shows gap.
nwk_grate_l = tray_x_l
nwk_grate_r = tray_x_r
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
       sx(pole_x + 300), sz(GRATE_Z_TOP + 50),
       f"{SLIT_WIDTH}mm SLIT\n(NEAR WALKWAY\nAT POLE POSITION)",
       fs=5, color=C_FRAME, font=FONT, zorder=15)

ax.text(sx(pole_x - 500), sz(GRATE_Z_BOT - 5),
        "NEAR WALKWAY (PROJECTED, Yd=0–300)",
        ha="center", va="top", fontsize=4.5, color=C_GRATE,
        style="italic", **FONT, zorder=10)

# ── Beam / spray bar (full span) ────────────────────────────────────────
beam_x_l = PROC_OPEN_X_L
beam_x_r = PROC_OPEN_X_R

# Beam shown in cut section (reveals internal PVC pipe)
ax.add_patch(Rectangle((sx(beam_x_l), sz(BEAM_Z_BOT)),
                         (beam_x_r - beam_x_l) / H_SC, BEAM_W / V_SC,
                         fc=C_ALUM_FILL, ec=C_FRAME, lw=1.5, zorder=9))
# PVC pipe inside
ax.add_patch(Rectangle((sx(beam_x_l + 20), sz(BEAM_Z_BOT + BEAM_T + 0.3)),
                         (beam_x_r - beam_x_l - 40) / H_SC, PVC_OD / V_SC,
                         fc=C_PVC, ec=C_FRAME, lw=0.5, alpha=0.5, zorder=9.3))
# Water inside PVC
ax.add_patch(Rectangle((sx(beam_x_l + 20), sz(BEAM_Z_BOT + BEAM_T + 0.3 + PVC_WALL)),
                         (beam_x_r - beam_x_l - 40) / H_SC, PVC_ID / V_SC,
                         fc=C_WATER, ec="none", alpha=0.3, zorder=9.5))

ax.text(sx(pole_x), sz(BEAM_Z_TOP + 8),
        f"40×40×3mm AL SHS — SPANS {BEAM_SPAN}mm — 1\" PVC PIPE INSIDE",
        ha="center", va="bottom", fontsize=5.5, color=C_FRAME,
        fontweight="bold", **FONT, zorder=15)

# Spray apertures and droplets
n_drops = 12
for i in range(n_drops):
    frac = (i + 0.5) / n_drops
    drop_x = beam_x_l + 50 + (beam_x_r - beam_x_l - 100) * frac
    ax.plot([sx(drop_x - APERTURE_DIA / 2), sx(drop_x + APERTURE_DIA / 2)],
            [sz(BEAM_Z_BOT), sz(BEAM_Z_BOT)],
            color=C_WATER, lw=1.5, zorder=10)
    ax.plot([sx(drop_x), sx(drop_x)],
            [sz(BEAM_Z_BOT - 1), sz(TRAY_FLOOR_Z + 2)],
            color=C_WATER, lw=0.5, alpha=0.4, zorder=6)

# End caps (open beam, PVC capped inside)
for end_x in [beam_x_l, beam_x_r]:
    ax.plot([sx(end_x), sx(end_x)], [sz(BEAM_Z_BOT), sz(BEAM_Z_TOP)],
            color=C_FRAME, lw=2.0, zorder=9.5)

# ── Pole through slit down to beam ──────────────────────────────────────
pole_top_z = GRATE_Z_TOP + 80
pole_bot_z = BEAM_Z_TOP + 5

ax.plot([sx(pole_x), sx(pole_x)],
        [sz(pole_top_z), sz(pole_bot_z)],
        color="#8B6914", lw=2.5, zorder=10, solid_capstyle="round")
ax.plot([sx(pole_x), sx(pole_x)],
        [sz(pole_top_z), sz(pole_bot_z)],
        color="#BFA040", lw=1.0, zorder=10.5)

leader(ax, sx(pole_x + 5), sz(pole_top_z),
       sx(pole_x + 400), sz(pole_top_z + 30),
       "TELESCOPING POLE\n(THROUGH WALKWAY SLIT)",
       fs=4.5, color="#8B6914", font=FONT, zorder=15)

# ── BV-02 on pinhole wall ───────────────────────────────────────────────
bv_z = BV02_Z
bv_size = 30
pipe_w = 10

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
       sx(BV02_X - 200), sz(bv_z + 80),
       f"BV-02 @ Z={int(bv_z)}mm\n(1/2\" BALL VALVE)\nWAIST HEIGHT",
       fs=5.5, color=C_BLUE, font=FONT, zorder=15)

# ── Flex hose from BV-02 to beam center feed ────────────────────────────
hose_start_x = BV02_X + bv_size / 2
hose_start_z = bv_z
hose_end_x = pole_x
hose_end_z = BEAM_Z_TOP + 5

n_pts = 100
ht = np.linspace(0, 1, n_pts)
P0 = np.array([hose_start_x, hose_start_z])
P1 = np.array([hose_start_x + 300, hose_start_z - 300])
P2 = np.array([hose_end_x - 500, hose_end_z + 100])
P3 = np.array([hose_end_x, hose_end_z])
hose_xs = (1-ht)**3*P0[0] + 3*(1-ht)**2*ht*P1[0] + 3*(1-ht)*ht**2*P2[0] + ht**3*P3[0]
hose_zs = (1-ht)**3*P0[1] + 3*(1-ht)**2*ht*P1[1] + 3*(1-ht)*ht**2*P2[1] + ht**3*P3[1]
envelope = np.clip(np.minimum(ht, 1 - ht) * 4, 0, 1)
hose_zs += 3.0 * np.sin(np.linspace(0, 14 * np.pi, n_pts)) * envelope

ax.plot([sx(x) for x in hose_xs], [sz(z) for z in hose_zs],
        color=C_HOSE, lw=2.0, alpha=0.7, zorder=11)

ax.text(sx(BV02_X + 500), sz(bv_z - 200),
        "1/2\" FLEX HOSE → CENTER FEED (4m COILED)",
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
ax.text(sx(pole_x), sz(Z_LO + 5), "CL BEAM CENTER",
        ha="center", va="bottom", fontsize=4.5, color=C_CL, **FONT, zorder=2)

# ── Dimensions ────────────────────────────────────────────────────────────
draw_dim_h(ax, sx(beam_x_l), sx(beam_x_r), sz(BEAM_Z_BOT - 20),
           f"{BEAM_SPAN}mm BEAM SPAN",
           offset=6 / V_SC, fs=5, font=FONT)

draw_dim_v(ax, sx(beam_x_l - 30), sz(0), sz(GRATE_Z_TOP),
           f"{WALKWAY_H}mm\nDECK",
           offset=6 / H_SC, fs=5, font=FONT)

draw_dim_v(ax, sx(beam_x_r + 30), sz(TRAY_FLOOR_Z), sz(BEAM_Z_BOT),
           f"{BEAM_Z_BOT - TRAY_FLOOR_Z:.0f}mm\nSPRAY\nHGT",
           offset=6 / H_SC, fs=4.5, font=FONT, right=True)

draw_dim_v(ax, sx(BV02_X + 40), sz(0), sz(bv_z),
           f"{int(bv_z)}mm\nBV-02",
           offset=6 / H_SC, fs=4.5, font=FONT, right=True)

# ── Notes ────────────────────────────────────────────────────────────────
notes = [
    "GANTRY ELEVATION — SECTION THROUGH NEAR WALKWAY:",
    f"1. 40×40×3mm AL SHS beam spans {BEAM_SPAN}mm. 1\" PVC pipe inside.",
    f"2. {SLIT_WIDTH}mm slit in walkway at beam center X for pole passage.",
    "3. BV-02 on pinhole wall at waist height → flex hose → center feed.",
    "4. 12mm apertures in beam, 2mm holes in PVC pipe.",
]
draw_notes(ax, notes, sx(X_LO + 800), sz(Z_HI - 25), spacing=5 / V_SC,
           fs=5.5, font=FONT, width=2000 / H_SC)

ax.text(sx(pole_x), sz(Z_HI - 5),
        "GANTRY ELEVATION — VIEW FROM FILM PLANE",
        ha="center", va="top", fontsize=9, color=C_FRAME,
        fontweight="bold", **FONT, zorder=15)
ax.text(sx(pole_x), sz(Z_HI - 22),
        "(H 1:18 / V 1:4.5 — 4× VERT EXAG — SECTION THROUGH NEAR WALKWAY)",
        ha="center", va="top", fontsize=5, color=C_DIM,
        **FONT, zorder=15)

# ── Detail callouts ──────────────────────────────────────────────────────
# Detail A — beam end
ax.add_patch(mpatches.Ellipse((sx(beam_x_l), sz(BEAM_Z_BOT + BEAM_W / 2)),
                               150 / H_SC, 80 / V_SC,
                               fc="none", ec="#CC0000", lw=1.5, ls="--", zorder=20))
ax.text(sx(beam_x_l), sz(BEAM_Z_BOT - 30),
        "DETAIL A", ha="center", va="top", fontsize=7, color="#CC0000",
        fontweight="bold", **FONT, zorder=20)

# Detail B — carriage area (near left walkway)
carriage_cx = CARRIAGE_X_L
ax.add_patch(mpatches.Ellipse((sx(carriage_cx), sz(WHEEL_AXLE_Z)),
                               200 / H_SC, 80 / V_SC,
                               fc="none", ec="#0066AA", lw=1.5, ls="--", zorder=20))
ax.text(sx(carriage_cx), sz(WHEEL_AXLE_Z + 50),
        "DETAIL B", ha="center", va="bottom", fontsize=7, color="#0066AA",
        fontweight="bold", **FONT, zorder=20)


# ─────────────────────────────────────────────────────────────────────────────
# Detail A: Beam end — open SHS with PVC pipe extending beyond
# PVC socket cap slides OVER pipe OD; pipe end seats against cap interior.
# X: along beam axis, - = outside (past beam end), + = inside (bore)
# Y: perpendicular to beam axis, 0 = beam centerline
# ─────────────────────────────────────────────────────────────────────────────
ax_a = fig.add_subplot(gs[3, 1])
ax_a.set_facecolor(C_BG)
ax_a.axis("off")

CAP_SOCKET_DEPTH = 20    # pipe slides 20mm into cap socket
CAP_WALL_T = 3.5         # cap wall thickness (thicker than pipe)
CAP_CLOSED_T = 3.5       # cap closed-end wall thickness
PVC_EXTEND = 25          # pipe extension past beam end (enough for cap clearance)
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

# ── PVC socket cap (slides OVER pipe OD — engagement zone) ──────────────
# Cap top wall (from closed end to open edge, at pipe OD + cap wall)
ax_a.add_patch(Rectangle((cap_closed_x, pvc_od_h),
               cap_open_x - cap_closed_x, CAP_WALL_T,
               fc=C_PVC, ec=C_FRAME, lw=0.8, zorder=5))
# Cap bottom wall
ax_a.add_patch(Rectangle((cap_closed_x, -cap_od_h),
               cap_open_x - cap_closed_x, CAP_WALL_T,
               fc=C_PVC, ec=C_FRAME, lw=0.8, zorder=5))
# Cap closed end (solid wall sealing the end)
ax_a.add_patch(Rectangle((cap_closed_x, -cap_od_h),
               CAP_CLOSED_T, cap_od_h * 2,
               fc=C_PVC, ec=C_FRAME, lw=0.8, zorder=5.5))
# Cap open edge lines
ax_a.plot([cap_open_x, cap_open_x], [pvc_od_h, cap_od_h],
          color=C_FRAME, lw=0.8, zorder=5.5)
ax_a.plot([cap_open_x, cap_open_x], [-cap_od_h, -pvc_od_h],
          color=C_FRAME, lw=0.8, zorder=5.5)

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

leader(ax_a, (cap_open_x + beam_end_x) / 2, pvc_od_h + CAP_WALL_T + 1,
       d_xr - 15, d_yt - 12,
       "1\" Sch 40 PVC PIPE\n(EXTENDS PAST BEAM)",
       fs=5, color=C_PVC, font=FONT, zorder=20, bbox=_bbox_a)

leader(ax_a, cap_closed_x + CAP_CLOSED_T / 2, -cap_od_h - 1,
       cap_closed_x - 3, d_yb + 6,
       "1\" PVC SOCKET CAP\n(SOLVENT WELDED)",
       fs=5, color=C_PVC, font=FONT, zorder=20, bbox=_bbox_a)

ax_a.text(d_xr - 8, 0, "WATER",
          ha="center", va="center", fontsize=5, color=C_WATER,
          fontweight="bold", bbox=_bbox_a, **FONT, zorder=15)

ax_a.text((pipe_end_x + cap_closed_x + CAP_CLOSED_T) / 2, 0,
          "BUTT\nJOINT",
          ha="center", va="center", fontsize=4, color="#AA3030",
          fontweight="bold", bbox=_bbox_a, **FONT, zorder=15)

# ── Dimensions ────────────────────────────────────────────────────────────
draw_dim_h(ax_a, cap_closed_x, beam_end_x, d_yb + 3,
           f"{PVC_EXTEND + CAP_CLOSED_T:.0f}mm\nPROTRUSION",
           offset=3, fs=4.5, font=FONT)

draw_dim_h(ax_a, cap_closed_x, cap_open_x, d_yb + 10,
           f"{CAP_SOCKET_DEPTH + CAP_CLOSED_T:.0f}mm\nCAP LENGTH",
           offset=2, fs=4.5, font=FONT)

draw_dim_h(ax_a, pipe_end_x, cap_open_x, cap_od_h + 5,
           f"{CAP_SOCKET_DEPTH}mm\nENGAGEMENT",
           offset=2, fs=4, font=FONT)

draw_dim_v(ax_a, d_xr - 3, -17, 17,
           "34mm\nBORE", offset=4, fs=5, font=FONT, right=True)

draw_dim_v(ax_a, d_xr - 8, 17, 20,
           "3mm\nWALL", offset=3, fs=4.5, font=FONT, right=True)

draw_dim_v(ax_a, d_xl + 3, -pvc_od_h, pvc_od_h,
           f"{PVC_OD:.1f}mm\nPVC OD", offset=3, fs=4.5, font=FONT)


# ─────────────────────────────────────────────────────────────────────────────
# LEFT PANEL — Yd-Z cross section (operator view)
# Looking along X. Equal H/V scale. Cropped to carriage/beam/walkway area.
# ─────────────────────────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 0])
ax2.set_facecolor(C_BG)
ax2.set_aspect("equal")
ax2.axis("off")

SC2 = 4.0

def dy(yd_mm):
    return 3.0 + yd_mm / SC2

def dz(z_mm):
    return 2.0 + z_mm / SC2

R_YD_LO = -50
R_YD_HI = 600
R_Z_LO = -30
R_Z_HI = 250

ax2.set_xlim(dy(R_YD_LO), dy(R_YD_HI))
ax2.set_ylim(dz(R_Z_LO), dz(R_Z_HI))

ax2.text(dy((R_YD_LO + R_YD_HI) / 2), dz(R_Z_HI - 3),
         "CROSS SECTION — OPERATOR VIEW",
         ha="center", va="top", fontsize=9, color=C_FRAME,
         fontweight="bold", **FONT, zorder=15)
ax2.text(dy((R_YD_LO + R_YD_HI) / 2), dz(R_Z_HI - 15),
         "(LOOKING ALONG X — SCALE 1:4)",
         ha="center", va="top", fontsize=5, color=C_DIM,
         **FONT, zorder=15)

# ── Container pinhole wall (Yd=0) ────────────────────────────────────────
wall_w = 40
ax2.add_patch(Rectangle((dy(-wall_w), dz(R_Z_LO)),
                          wall_w / SC2, (R_Z_HI - R_Z_LO) / SC2,
                          fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
ax2.plot([dy(0), dy(0)], [dz(R_Z_LO), dz(R_Z_HI)],
         color=C_OUT, lw=2.0, zorder=3)

# ── Container floor ──────────────────────────────────────────────────────
ax2.plot([dy(R_YD_LO), dy(R_YD_HI)], [dz(0), dz(0)],
         color=C_OUT, lw=2.0, zorder=3)
ax2.add_patch(Rectangle((dy(R_YD_LO), dz(-25)),
                          (R_YD_HI - R_YD_LO) / SC2, 25 / SC2,
                          fc="#E0E0D8", ec=C_OUT, lw=0.8, hatch="...", zorder=1))

# ── Processing tray floor and near rim ───────────────────────────────────
tray_yd_start = PROC_TRAY_YD_NEAR
ax2.add_patch(Rectangle((dy(tray_yd_start), dz(0)),
                          (R_YD_HI - tray_yd_start) / SC2, TRAY_FLOOR_Z / SC2,
                          fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))
ax2.add_patch(Rectangle((dy(tray_yd_start - 3), dz(0)),
                          6 / SC2, PROC_TRAY_RIM / SC2,
                          fc=C_TRAY, ec=C_OUT, lw=1.2, zorder=5))

ax2.text(dy(450), dz(TRAY_FLOOR_Z + 8),
         "PROCESSING TRAY (304 SS)", ha="center", va="bottom",
         fontsize=5, color=C_DIM, style="italic", **FONT, zorder=10)

# ── Near walkway grating (Yd=0–300) ──────────────────────────────────────
wk_yd_l = 0
wk_yd_r = WALKWAY_W

ax2.add_patch(Rectangle((dy(wk_yd_l), dz(GRATE_Z_BOT)),
                          (wk_yd_r - wk_yd_l) / SC2, WALKWAY_GRATE_T / SC2,
                          fc=C_GRATE, ec=C_OUT, lw=1.5, zorder=8))
for frac in np.linspace(0.1, 0.9, 5):
    gyd = wk_yd_l + (wk_yd_r - wk_yd_l) * frac
    ax2.plot([dy(gyd), dy(gyd)], [dz(GRATE_Z_BOT), dz(GRATE_Z_TOP)],
             color="#888888", lw=0.4, zorder=8)

brk_depth_r = 60
ax2.plot([dy(0), dy(0)], [dz(GRATE_Z_BOT - brk_depth_r), dz(GRATE_Z_BOT)],
         color=C_FRAME, lw=1.5, zorder=5)
ax2.plot([dy(0), dy(wk_yd_r)], [dz(GRATE_Z_BOT), dz(GRATE_Z_BOT)],
         color=C_FRAME, lw=1.2, zorder=5)
ax2.plot([dy(0), dy(wk_yd_r)],
         [dz(GRATE_Z_BOT - brk_depth_r), dz(GRATE_Z_BOT)],
         color=C_FRAME, lw=0.8, ls="--", zorder=5)

ax2.text(dy((wk_yd_l + wk_yd_r) / 2), dz(GRATE_Z_TOP + 10),
         "NEAR WALKWAY", ha="center", va="bottom",
         fontsize=5.5, color=C_GRATE, fontweight="bold", **FONT, zorder=10)

# ── Beam cross-section (Yd-Z, matching Detail B proportions) ─────────────
beam_yd = 450
beam_yd_l = beam_yd - BEAM_W / 2
beam_yd_r = beam_yd + BEAM_W / 2

ax2.add_patch(Rectangle((dy(beam_yd_l), dz(BEAM_Z_BOT)),
                          BEAM_W / SC2, BEAM_W / SC2,
                          fc=C_ALUM_FILL, ec=C_FRAME, lw=2.0, zorder=9))
# Square bore
ax2.add_patch(Rectangle((dy(beam_yd - BEAM_BORE / 2), dz(BEAM_Z_BOT + BEAM_T)),
                          BEAM_BORE / SC2, BEAM_BORE / SC2,
                          fc=C_BG, ec=C_FRAME, lw=0.5, zorder=9.3))
# PVC pipe (circle cross-section inside square bore)
ax2.add_patch(Circle((dy(beam_yd), dz(BEAM_Z_BOT + BEAM_W / 2)),
                       PVC_OD / 2 / SC2,
                       fc=C_PVC, ec=C_FRAME, lw=0.8, alpha=0.7, zorder=9.5))
ax2.add_patch(Circle((dy(beam_yd), dz(BEAM_Z_BOT + BEAM_W / 2)),
                       PVC_ID / 2 / SC2,
                       fc=C_WATER, ec=C_FRAME, lw=0.5, alpha=0.4, zorder=9.6))

ax2.text(dy(beam_yd), dz(BEAM_Z_TOP + 8),
         "40×40×3mm AL SHS\n+ 1\" PVC PIPE", ha="center", va="bottom",
         fontsize=5.5, color=C_FRAME, fontweight="bold", **FONT, zorder=15)

# Center feed fitting
feed_fit_h = 12
feed_fit_w = 8
ax2.add_patch(Rectangle((dy(beam_yd_r), dz(BEAM_Z_BOT + BEAM_W / 2 - feed_fit_h / 2)),
                          feed_fit_w / SC2, feed_fit_h / SC2,
                          fc="#C0A860", ec=C_FRAME, lw=0.8, zorder=10))
leader(ax2, dy(beam_yd_r + feed_fit_w), dz(BEAM_Z_BOT + BEAM_W / 2),
       dy(beam_yd_r + 60), dz(BEAM_Z_BOT + BEAM_W / 2 + 25),
       "1/2\" BULKHEAD\nCENTER FEED",
       fs=4.5, color="#C0A860", font=FONT, zorder=15)

# 12mm aperture at bottom
ax2.add_patch(Rectangle((dy(beam_yd - APERTURE_DIA / 2), dz(BEAM_Z_BOT - 0.5)),
                          APERTURE_DIA / SC2, (BEAM_T + 1) / SC2,
                          fc=C_BG, ec=C_FRAME, lw=0.5, zorder=9))
ax2.plot([dy(beam_yd), dy(beam_yd)],
         [dz(BEAM_Z_BOT - 1), dz(TRAY_FLOOR_Z + 2)],
         color=C_WATER, lw=1.0, alpha=0.5, zorder=6)

# ── Carriage wheels (2× Ø50mm nylon, equal scale circles) ───────────────
carriage_ctr_yd = beam_yd
cw1_yd = carriage_ctr_yd - WHEEL_SPACING_YD / 2
cw2_yd = carriage_ctr_yd + WHEEL_SPACING_YD / 2

for cw_yd in [cw1_yd, cw2_yd]:
    ax2.add_patch(Circle((dy(cw_yd), dz(WHEEL_AXLE_Z)),
                            WHEEL_DIA / 2 / SC2,
                            fc=C_NYLON, ec=C_WHEEL, lw=1.5, zorder=6))
    ax2.add_patch(Circle((dy(cw_yd), dz(WHEEL_AXLE_Z)),
                            2 / SC2, fc=C_WHEEL, ec=C_OUT, lw=0.3, zorder=6.5))
    ax2.plot([dy(cw_yd - WHEEL_WIDTH / 2), dy(cw_yd + WHEEL_WIDTH / 2)],
             [dz(TRAY_FLOOR_Z), dz(TRAY_FLOOR_Z)],
             color=C_WHEEL, lw=1.5, zorder=5)
    for offset in [-WHEEL_WIDTH / 2 - 2, WHEEL_WIDTH / 2 + 2]:
        ax2.plot([dy(cw_yd + offset), dy(cw_yd + offset)],
                 [dz(WHEEL_AXLE_Z + 6), dz(WHEEL_AXLE_Z - WHEEL_DIA / 2 + 4)],
                 color=C_FRAME, lw=0.8, zorder=5.5)
    ax2.plot([dy(cw_yd - WHEEL_WIDTH / 2 - 4), dy(cw_yd + WHEEL_WIDTH / 2 + 4)],
             [dz(WHEEL_AXLE_Z), dz(WHEEL_AXLE_Z)],
             color=C_FRAME, lw=0.5, zorder=6.5)

# L-bracket arm
brk_arm_l = cw1_yd - 18
brk_arm_r = cw2_yd + 18
brk_t_op = 5
ax2.add_patch(Rectangle((dy(brk_arm_l), dz(WHEEL_AXLE_Z - brk_t_op / 2)),
                           (brk_arm_r - brk_arm_l) / SC2, brk_t_op / SC2,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=0.8, zorder=7))

# U-clamp over beam
uc_l_op = carriage_ctr_yd - BEAM_W / 2 - UC_T - UC_GAP
uc_r_op = carriage_ctr_yd + BEAM_W / 2 + UC_GAP + UC_T
ax2.add_patch(Rectangle((dy(uc_l_op), dz(BEAM_Z_TOP)),
                           (uc_r_op - uc_l_op) / SC2, UC_T / SC2,
                           fc=C_UCLAMP, ec=C_FRAME, lw=0.6, zorder=10))
for u_yd in [uc_l_op, uc_r_op - UC_T]:
    ax2.add_patch(Rectangle((dy(u_yd), dz(BEAM_Z_BOT + UC_T)),
                               UC_T / SC2,
                               (BEAM_Z_TOP - BEAM_Z_BOT - UC_T) / SC2,
                               fc=C_UCLAMP, ec=C_FRAME, lw=0.5, zorder=10))
ax2.add_patch(Rectangle((dy(uc_l_op - UC_FLARE), dz(BEAM_Z_BOT)),
                           (UC_T + UC_FLARE) / SC2, UC_T / SC2,
                           fc=C_UCLAMP, ec=C_FRAME, lw=0.5, zorder=10))
ax2.add_patch(Rectangle((dy(uc_r_op - UC_T), dz(BEAM_Z_BOT)),
                           (UC_T + UC_FLARE) / SC2, UC_T / SC2,
                           fc=C_UCLAMP, ec=C_FRAME, lw=0.5, zorder=10))

leader(ax2, dy(cw1_yd), dz(WHEEL_AXLE_Z - WHEEL_DIA / 2 - 5),
       dy(cw1_yd - 40), dz(WHEEL_AXLE_Z - WHEEL_DIA / 2 - 25),
       f"Ø{WHEEL_DIA}mm NYLON WHEELS\n(2 PER CARRIAGE,\nFORK + AXLE PIN)",
       fs=4.5, color=C_WHEEL, font=FONT, zorder=15)

# ── Dimensions ────────────────────────────────────────────────────────────
draw_dim_h(ax2, dy(wk_yd_l), dy(wk_yd_r), dz(GRATE_Z_TOP + 30),
           f"{WALKWAY_W}mm WALKWAY", offset=6 / SC2, fs=5.5, font=FONT)

draw_dim_v(ax2, dy(R_YD_HI - 20), dz(0), dz(GRATE_Z_TOP),
           f"{WALKWAY_H}mm\nDECK HGT",
           offset=6 / SC2, fs=5, font=FONT, right=True)

draw_dim_h(ax2, dy(wk_yd_r), dy(beam_yd), dz(BEAM_Z_TOP + 50),
           f"{beam_yd - int(wk_yd_r)}mm\n(BEAM TO\nWALKWAY EDGE)",
           offset=6 / SC2, fs=4.5, font=FONT)

draw_dim_v(ax2, dy(beam_yd_l - 20), dz(BEAM_Z_BOT), dz(BEAM_Z_TOP),
           f"{BEAM_W}mm", offset=6 / SC2, fs=5, font=FONT)

draw_dim_v(ax2, dy(tray_yd_start - 20), dz(0), dz(PROC_TRAY_RIM),
           f"{PROC_TRAY_RIM}mm\nRIM",
           offset=6 / SC2, fs=4.5, font=FONT)

draw_dim_h(ax2, dy(cw1_yd), dy(cw2_yd), dz(TRAY_FLOOR_Z + WHEEL_DIA + 8),
           f"{WHEEL_SPACING_YD}mm\nWHEEL SPACING",
           offset=6 / SC2, fs=4.5, font=FONT)

# ── Notes ────────────────────────────────────────────────────────────────
r_notes = [
    "CROSS SECTION:",
    f"1. Beam travels {SPRAY_BAR_TRAVEL}mm along Yd (push/pull with pole).",
    "2. 1\" PVC pipe inside beam carries water. Center feed via bulkhead.",
    "3. U-clamp holds beam to carriage — no beam wall penetration.",
]
draw_notes(ax2, r_notes, dy(R_YD_LO + 350), dz(R_Z_HI - 30), spacing=5 / SC2,
           fs=5.5, font=FONT, width=300 / SC2)


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
# Beam runs left-right in X (long rectangle).  Wheels above/below in Yd.
# ─────────────────────────────────────────────────────────────────────────────
ax_d = fig.add_subplot(gs[2, 1])
ax_d.set_facecolor(C_BG)
ax_d.axis("off")

SC_D = 2.0
BEAM_SHOW_LEN = 140  # mm of beam shown on each side of center

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
ax_d.add_patch(Rectangle((px(-arm_w_x / 2), py_d(-arm_half_span)),
                           arm_w_x / SC_D, (2 * arm_half_span) / SC_D,
                           fc=C_ALUM_FILL, ec=C_FRAME, lw=1.0,
                           hatch="///", alpha=0.7, zorder=4))

# ── U-clamp top plate (visible from above — spans Yd across beam) ──────
uc_w_yd_top = BEAM_W + 2 * UC_T + 2 * UC_GAP
ax_d.add_patch(Rectangle((px(-arm_w_x / 2), py_d(-uc_w_yd_top / 2)),
                           arm_w_x / SC_D, uc_w_yd_top / SC_D,
                           fc=C_UCLAMP, ec=C_FRAME, lw=1.0, alpha=0.5, zorder=6))
# Flared feet (extend outward in Yd)
for side in [-1, 1]:
    foot_yd = side * (BEAM_W / 2 + UC_GAP + UC_T)
    if side < 0:
        foot_yd -= UC_FLARE
    ax_d.add_patch(Rectangle((px(-arm_w_x / 2), py_d(foot_yd)),
                               arm_w_x / SC_D, (UC_FLARE + UC_T) / SC_D,
                               fc=C_UCLAMP, ec=C_FRAME, lw=0.8, alpha=0.6, zorder=6))

# Bolt holes through flared feet
for side in [-1, 1]:
    bolt_yd = side * (BEAM_W / 2 + UC_GAP + UC_T + UC_FLARE / 2)
    ax_d.add_patch(Circle((px(0), py_d(bolt_yd)),
                            3 / SC_D,
                            fc=C_BOLT, ec=C_FRAME, lw=0.5, zorder=8))

leader(ax_d, px(arm_w_x / 2), py_d(BEAM_W / 2 + UC_GAP + UC_T + UC_FLARE),
       px(D_X_HI - 30), py_d(BEAM_W / 2 + 30),
       "U-CLAMP\nFLARED LEGS\n+ WING NUTS",
       fs=5, color=C_BOLT, font=FONT, zorder=20, bbox=_bbox_d)

# ── Fork brackets (vertical plates straddling each wheel) ────────────────
fork_t = 6
for w_sign in [-1, 1]:
    w_yd_ctr = w_sign * WHEEL_SPACING_YD / 2
    for offset in [-WHEEL_WIDTH / 2 - 2, WHEEL_WIDTH / 2 + 2]:
        fork_yd = w_yd_ctr + offset
        ax_d.add_patch(Rectangle((px(-fork_t / 2 - 4), py_d(fork_yd - 1)),
                                   fork_t / SC_D, 2 / SC_D,
                                   fc=C_ALUM_FILL, ec=C_FRAME, lw=0.6, zorder=7))

# ── Wheels (footprint — rectangles: WHEEL_DIA in X, WHEEL_WIDTH in Yd) ──
for w_sign in [-1, 1]:
    w_yd_ctr = w_sign * WHEEL_SPACING_YD / 2
    ax_d.add_patch(Rectangle((px(-WHEEL_DIA / 2), py_d(w_yd_ctr - WHEEL_WIDTH / 2)),
                               WHEEL_DIA / SC_D, WHEEL_WIDTH / SC_D,
                               fc=C_NYLON, ec=C_WHEEL, lw=1.5, alpha=0.6, zorder=3))
    ax_d.add_patch(Circle((px(0), py_d(w_yd_ctr)),
                            5 / SC_D,
                            fc="#D0D0D8", ec=C_FRAME, lw=0.5, zorder=7))

# ── Labels ──────────────────────────────────────────────────────────────
leader(ax_d, px(WHEEL_DIA / 2), py_d(-WHEEL_SPACING_YD / 2),
       px(D_X_HI - 25), py_d(-WHEEL_SPACING_YD / 2 - 10),
       f"Ø{WHEEL_DIA}mm WHEEL\n({WHEEL_WIDTH}mm WIDE)",
       fs=5, color=C_WHEEL, font=FONT, zorder=20, bbox=_bbox_d)

leader(ax_d, px(-arm_w_x / 2 - 1), py_d(0),
       px(D_X_LO + 15), py_d(25),
       "L-BRACKET ARM\n(5mm AL PLATE)",
       fs=5, color=C_FRAME, font=FONT, zorder=20, bbox=_bbox_d)

# ── Dimensions ──────────────────────────────────────────────────────────
draw_dim_v(ax_d, px(D_X_LO + 12),
           py_d(-WHEEL_SPACING_YD / 2), py_d(WHEEL_SPACING_YD / 2),
           f"{WHEEL_SPACING_YD}mm\nWHEEL\nSPACING",
           offset=3 / SC_D, fs=5, font=FONT)

draw_dim_h(ax_d, px(-BEAM_W / 2), px(BEAM_W / 2),
           py_d(D_YD_LO + 8),
           f"{BEAM_W}mm\nBEAM",
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
       ppx(pole_x - 500), ppy(-120),
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
