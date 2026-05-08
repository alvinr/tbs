#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_mini_tbs_diagram.py

Mini-TBS proof-of-concept pinhole camera — engineering drawing.
Output: diagrams/mini-tbs-sheet1.png

Sheet 1: Side cross-section (top) + front view of arm-sleeve face (bottom).
"""

import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

from tbs_title_block import title_block
from tbs_constants import DIAGRAMS_DIR, SVG_DIR, svg_path, C_OUT, C_CL, C_DIM

os.makedirs(DIAGRAMS_DIR, exist_ok=True)
os.makedirs(SVG_DIR, exist_ok=True)

# ── Mini-TBS constants ───────────────────────────────────────────────────────
BOX_W   = 457    # mm — box width (18")
BOX_D   = 457    # mm — box depth / focal length (18")
BOX_H   = 406    # mm — box height (16")

FOCAL   = BOX_D  # focal length = depth
PH_D    = 0.794  # mm — pinhole diameter (1/32" drill bit)
F_NO    = round(FOCAL / PH_D)  # f/575

MARGIN  = 25     # mm — mounting margin each side
FP_W    = BOX_W - 2 * MARGIN   # usable film plane width
FP_H    = BOX_H - 2 * MARGIN   # usable film plane height

SLEEVE_D = 102   # mm — armhole diameter (4")
SLEEVE_SPACING = 254  # mm — armhole center-to-center (10")
SLEEVE_LEN = 457  # mm — sleeve tube length (18")

WALL_T  = 4      # mm — cardboard wall thickness (schematic)
BACKING = 5      # mm — foam-core backing board thickness

# ── Drawing palette ──────────────────────────────────────────────────────────
BG         = "#FFFFFF"
C_BOX      = "#D2B48C"    # tan — cardboard
C_BOX_WALL = "#C4A882"    # darker cardboard for walls
C_TAPE     = "#1A1A1A"    # black gaffer tape
C_MUSLIN   = "#F5F0E0"    # muslin fabric
C_CONE     = "#CCE4FF"    # light cone fill
C_CONE_LN  = "#4488CC"    # light cone boundary
C_PINHOLE  = "#CC2020"    # pinhole marker
C_SLEEVE   = "#2A2A2A"    # arm sleeve fabric
C_BACKING  = "#E8E0D0"    # foam-core board
C_ALUM     = "#C0C0C8"    # aluminum pinhole plate

FS_SM = 7.0
FS_MD = 8.5

# ── Drawing helpers ──────────────────────────────────────────────────────────
def draw_dim_h(ax, x1, x2, y, label, offset=12, fs=FS_SM, color=C_DIM):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.8))
    ax.plot([x1, x1], [y - offset * 0.3, y + offset * 0.3], color=color, lw=0.6)
    ax.plot([x2, x2], [y - offset * 0.3, y + offset * 0.3], color=color, lw=0.6)
    ax.text((x1 + x2) / 2, y + offset * 0.55, label, ha="center", va="bottom",
            fontsize=fs, color=color)


def draw_dim_v(ax, x, y1, y2, label, offset=12, fs=FS_SM, color=C_DIM, right=False):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.8))
    ax.plot([x - offset * 0.3, x + offset * 0.3], [y1, y1], color=color, lw=0.6)
    ax.plot([x - offset * 0.3, x + offset * 0.3], [y2, y2], color=color, lw=0.6)
    if right:
        ax.text(x + offset * 0.6, (y1 + y2) / 2, label, ha="left", va="center",
                fontsize=fs, color=color, rotation=90)
    else:
        ax.text(x - offset * 0.6, (y1 + y2) / 2, label, ha="right", va="center",
                fontsize=fs, color=color, rotation=90)


def leader(ax, x_tip, y_tip, x_txt, y_txt, label, fs=FS_SM, color=C_OUT, ha="left"):
    ax.annotate(label, xy=(x_tip, y_tip), xytext=(x_txt, y_txt),
                fontsize=fs, color=color, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", linestyle=":", color=color, lw=0.7,
                                connectionstyle="arc3,rad=0.0"))


# ══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — Two views stacked vertically
# ══════════════════════════════════════════════════════════════════════════════

FIG_W = 20.0
FIG_H = 16.0
fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(FIG_W, FIG_H), dpi=150,
                                      gridspec_kw={"height_ratios": [1, 0.85]})
fig.patch.set_facecolor(BG)
fig.subplots_adjust(hspace=0.28, bottom=0.07, top=0.95, left=0.08, right=0.92)

# ── TOP: Side cross-section (looking at 18×16" face) ────────────────────────
ax = ax_top
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

# Scale: 1 drawing unit = 1 mm
# Origin: bottom-left of box interior at (0, 0)
PAD = 120
ax.set_xlim(-PAD, BOX_D + PAD * 2)
ax.set_ylim(-PAD, BOX_H + PAD)

# Box outline (cross-section)
ax.add_patch(mpatches.Rectangle((0, 0), BOX_D, BOX_H,
             facecolor=C_BOX, edgecolor=C_OUT, linewidth=1.5, alpha=0.3, zorder=1))

# Wall thickness indicators
for rect in [
    (0, 0, WALL_T, BOX_H),                          # left wall (pinhole side)
    (BOX_D - WALL_T, 0, WALL_T, BOX_H),             # right wall (film plane side)
    (0, 0, BOX_D, WALL_T),                           # floor
    (0, BOX_H - WALL_T, BOX_D, WALL_T),             # ceiling
]:
    ax.add_patch(mpatches.Rectangle(rect[:2], rect[2], rect[3],
                 facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=0.8, zorder=2))

# Backing board (against right/film-plane wall)
board_x = BOX_D - WALL_T - BACKING
ax.add_patch(mpatches.Rectangle((board_x, WALL_T), BACKING, BOX_H - 2 * WALL_T,
             facecolor=C_BACKING, edgecolor=C_OUT, linewidth=0.8, zorder=3))

# Muslin on backing board (thick line)
muslin_x = board_x
muslin_y1 = WALL_T + MARGIN
muslin_y2 = BOX_H - WALL_T - MARGIN
ax.plot([muslin_x, muslin_x], [muslin_y1, muslin_y2],
        color=C_CL, lw=3.0, solid_capstyle="butt", zorder=4)

# Pinhole (on left wall)
ph_y = BOX_H / 2
ax.add_patch(plt.Circle((WALL_T / 2, ph_y), 6,
             facecolor=C_PINHOLE, edgecolor=C_OUT, linewidth=0.8, zorder=5))
# Crosshairs
ax.plot([WALL_T / 2 - 12, WALL_T / 2 + 12], [ph_y, ph_y],
        color=C_PINHOLE, lw=0.8, zorder=6)
ax.plot([WALL_T / 2, WALL_T / 2], [ph_y - 12, ph_y + 12],
        color=C_PINHOLE, lw=0.8, zorder=6)

# Aluminum plate behind pinhole (interior side)
ax.add_patch(mpatches.Rectangle((WALL_T, ph_y - 38), 2, 76,
             facecolor=C_ALUM, edgecolor=C_OUT, linewidth=0.6, zorder=4))

# Light cone (from pinhole to film plane edges)
cone_verts = [
    (WALL_T, ph_y),         # pinhole
    (muslin_x, muslin_y2),  # top of muslin
    (muslin_x, muslin_y1),  # bottom of muslin
]
ax.add_patch(mpatches.Polygon(cone_verts, closed=True,
             facecolor=C_CONE, edgecolor="none", alpha=0.25, zorder=1))
# Boundary rays
ax.plot([WALL_T, muslin_x], [ph_y, muslin_y2],
        color=C_CONE_LN, lw=0.8, ls="--", dashes=(6, 4), alpha=0.7, zorder=2)
ax.plot([WALL_T, muslin_x], [ph_y, muslin_y1],
        color=C_CONE_LN, lw=0.8, ls="--", dashes=(6, 4), alpha=0.7, zorder=2)

# Optical axis (dashed center line)
ax.plot([0, BOX_D], [ph_y, ph_y],
        color=C_CL, lw=0.7, ls="--", dashes=(8, 4), zorder=2)

# Shutter flap (outside left wall)
ax.add_patch(mpatches.Rectangle((-30, ph_y - 50), 28, 100,
             facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=3))

# ── Dimensions ───────────────────────────────────────────────────────────────
draw_dim_h(ax, 0, BOX_D, -50, f"Focal length  {BOX_D} mm  (18\")", offset=15)
draw_dim_h(ax, 0, BOX_D, BOX_H + 50, f"Box depth  {BOX_D} mm", offset=15)
draw_dim_v(ax, BOX_D + 60, 0, BOX_H, f"Box height  {BOX_H} mm  (16\")", offset=15, right=True)
draw_dim_v(ax, BOX_D + 120, muslin_y1, muslin_y2,
           f"Image  {FP_H} mm", offset=15, color=C_CL, right=True)

# ── Leaders ──────────────────────────────────────────────────────────────────
leader(ax, WALL_T / 2, ph_y + 10, -80, ph_y + 100,
       f"Pinhole  Ø{PH_D} mm\n(1/32\" drill bit)\nf/{F_NO}", ha="right", color=C_PINHOLE)
leader(ax, -16, ph_y, -80, ph_y - 60,
       "Shutter flap\n(black card)", ha="right")
leader(ax, muslin_x, (muslin_y1 + muslin_y2) / 2, BOX_D + 170, ph_y + 60,
       "Coated muslin\non backing board", ha="left", color=C_CL)
leader(ax, board_x + BACKING / 2, WALL_T + 10, BOX_D + 170, WALL_T + 40,
       "Foam-core\nbacking board", ha="left")
leader(ax, WALL_T + 1, ph_y - 30, 70, ph_y - 100,
       "Aluminum plate\n(beverage can)", ha="left", color=C_DIM)
leader(ax, BOX_D / 2, ph_y + 5, BOX_D / 2, ph_y + 80,
       "Light cone", ha="center", color=C_CONE_LN)

# View title
ax.text(BOX_D / 2, BOX_H + 100, "SIDE CROSS-SECTION",
        ha="center", va="bottom", fontsize=FS_MD + 2, fontweight="bold", color=C_OUT)
ax.text(BOX_D / 2, BOX_H + 82,
        "Looking at 18\" × 16\" face  —  pinhole left, film plane right",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, style="italic")

# ── BOTTOM: Front view of arm-sleeve face (18×18" face) ─────────────────────
ax2 = ax_bot
ax2.set_facecolor(BG)
ax2.set_aspect("equal")
ax2.axis("off")

ax2.set_xlim(-PAD, BOX_W + PAD * 2)
ax2.set_ylim(-PAD - 40, BOX_D + PAD)

# Box face outline
ax2.add_patch(mpatches.Rectangle((0, 0), BOX_W, BOX_D,
              facecolor=C_BOX, edgecolor=C_OUT, linewidth=1.5, alpha=0.3, zorder=1))

# Wall thickness
for rect in [
    (0, 0, WALL_T, BOX_D),
    (BOX_W - WALL_T, 0, WALL_T, BOX_D),
    (0, 0, BOX_W, WALL_T),
    (0, BOX_D - WALL_T, BOX_W, WALL_T),
]:
    ax2.add_patch(mpatches.Rectangle(rect[:2], rect[2], rect[3],
                  facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=0.8, zorder=2))

# Arm sleeves — two circles on this face
sleeve_cy = BOX_D / 2  # centered vertically
sleeve_cx1 = BOX_W / 2 - SLEEVE_SPACING / 2
sleeve_cx2 = BOX_W / 2 + SLEEVE_SPACING / 2

for cx in [sleeve_cx1, sleeve_cx2]:
    # Armhole (dark circle)
    ax2.add_patch(plt.Circle((cx, sleeve_cy), SLEEVE_D / 2,
                  facecolor=C_SLEEVE, edgecolor=C_OUT, linewidth=1.2, alpha=0.8, zorder=4))
    # Sleeve tube indicated by concentric dashed circle (outer diameter with fabric)
    ax2.add_patch(plt.Circle((cx, sleeve_cy), SLEEVE_D / 2 + 15,
                  facecolor="none", edgecolor=C_SLEEVE, linewidth=0.8,
                  linestyle="--", alpha=0.5, zorder=3))

# Gaffer tape seal ring around each armhole
for cx in [sleeve_cx1, sleeve_cx2]:
    ax2.add_patch(mpatches.Annulus((cx, sleeve_cy), SLEEVE_D / 2 + 15, 12,
                  facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.5, alpha=0.4, zorder=3))

# ── Dimensions ───────────────────────────────────────────────────────────────
draw_dim_h(ax2, 0, BOX_W, -50, f"Box width  {BOX_W} mm  (18\")", offset=15)
draw_dim_v(ax2, BOX_W + 60, 0, BOX_D, f"Box depth  {BOX_D} mm  (18\")", offset=15, right=True)
draw_dim_h(ax2, sleeve_cx1, sleeve_cx2, BOX_D + 50,
           f"Sleeve spacing  {SLEEVE_SPACING} mm  (10\")", offset=15, color=C_DIM)

# Armhole diameter dimension
draw_dim_h(ax2, sleeve_cx1 - SLEEVE_D / 2, sleeve_cx1 + SLEEVE_D / 2,
           sleeve_cy - SLEEVE_D / 2 - 30,
           f"Ø{SLEEVE_D} mm (4\")", offset=12, fs=FS_SM - 0.5)

# ── Leaders ──────────────────────────────────────────────────────────────────
leader(ax2, sleeve_cx1, sleeve_cy, -60, sleeve_cy + 60,
       f"Armhole Ø{SLEEVE_D} mm\n(black fabric sleeve)\nElastic band at wrist", ha="right")
leader(ax2, sleeve_cx1 + SLEEVE_D / 2 + 20, sleeve_cy, BOX_W + 100, sleeve_cy + 100,
       "Gaffer tape seal\n(light-tight junction)", ha="left")

# View title
ax2.text(BOX_W / 2, BOX_D + 100, "FRONT VIEW — ARM-SLEEVE FACE",
         ha="center", va="bottom", fontsize=FS_MD + 2, fontweight="bold", color=C_OUT)
ax2.text(BOX_W / 2, BOX_D + 82,
         "18\" × 18\" side face  —  two armholes for changing-bag access",
         ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, style="italic")

# ── Specification table (between the two views, right side) ──────────────────
spec_x = BOX_W + 140
spec_y = BOX_D - 20
specs = [
    f"Focal length:  {FOCAL} mm",
    f"Pinhole:  Ø{PH_D} mm  (1/32\" drill bit)",
    f"f-number:  f/{F_NO}",
    f"Film plane:  {FP_W} × {FP_H} mm",
    f"Exposure:  ~10 min  (full sun, cyanotype)",
    "Process:  Ware New Cyanotype",
    "Reciprocity:  None (iron-based)",
]
ax2.text(spec_x, spec_y + 20, "SPECIFICATION", ha="left", va="bottom",
         fontsize=FS_MD, fontweight="bold", color=C_OUT)
ax2.plot([spec_x, spec_x + 240], [spec_y + 15, spec_y + 15],
         color=C_OUT, lw=0.8)
for i, line in enumerate(specs):
    ax2.text(spec_x, spec_y - i * 22, line, ha="left", va="top",
             fontsize=FS_SM, color=C_DIM)

# ── Title block (full-figure overlay) ────────────────────────────────────────
ax_tb = fig.add_axes([0, 0, 1, 1], facecolor="none")
ax_tb.axis("off")
title_block(ax_tb, "SHEET 1 OF 1",
            drawing_title="MINI-TBS PROOF OF CONCEPT",
            subtitle="Side cross-section + arm-sleeve face — cardboard box pinhole camera",
            scale_note="Approx 1:3",
            doc_id="TBS-POC · Mini-TBS")

# ── Save ─────────────────────────────────────────────────────────────────────
out = f"{DIAGRAMS_DIR}/mini-tbs-sheet1.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(f"Saved: {out}")
