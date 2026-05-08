#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_mini_tbs_diagram.py

Mini-TBS proof-of-concept pinhole camera — engineering drawing.
Output: diagrams/mini-tbs-sheet1.png, diagrams/mini-tbs-sheet2.png

Sheet 1: Side cross-section (top) + front view of arm-sleeve face (bottom).
Sheet 2: Plan view (top) + armhole detail cross-section (bottom).
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
title_block(ax_tb, "SHEET 1 OF 2",
            drawing_title="MINI-TBS PROOF OF CONCEPT",
            subtitle="Side cross-section + arm-sleeve face — cardboard box pinhole camera",
            scale_note="Approx 1:3",
            doc_id="TBS-POC · Mini-TBS")

# ── Save Sheet 1 ─────────────────────────────────────────────────────────────
out1 = f"{DIAGRAMS_DIR}/mini-tbs-sheet1.png"
plt.savefig(out1, dpi=150, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.savefig(svg_path(out1), bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(f"Saved: {out1}")


# ══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Plan view (top) + armhole detail (bottom)
# ══════════════════════════════════════════════════════════════════════════════

fig2 = plt.figure(figsize=(FIG_W, FIG_H), dpi=150)
fig2.patch.set_facecolor(BG)
fig2.subplots_adjust(hspace=0.32, bottom=0.07, top=0.95, left=0.06, right=0.94)

# Use gridspec for unequal panel sizes: plan view wider, detail taller
gs = fig2.add_gridspec(2, 2, height_ratios=[1, 1.1], width_ratios=[1.2, 1],
                       hspace=0.30, wspace=0.22)

ax_plan = fig2.add_subplot(gs[0, :])     # plan view spans full width
ax_det  = fig2.add_subplot(gs[1, 0])     # armhole cross-section detail
ax_exp  = fig2.add_subplot(gs[1, 1])     # exploded/assembly notes

# ── TOP: Plan view (looking down) ───────────────────────────────────────────
ax = ax_plan
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

PLAN_PAD = 140
ax.set_xlim(-PLAN_PAD, BOX_D + PLAN_PAD * 2)
ax.set_ylim(-PLAN_PAD, BOX_W + PLAN_PAD)

# Box outline — depth (left-right) × width (bottom-top)
# Left face = pinhole face, right face = film plane face
# Bottom face = arm-sleeve face
ax.add_patch(mpatches.Rectangle((0, 0), BOX_D, BOX_W,
             facecolor=C_BOX, edgecolor=C_OUT, linewidth=1.5, alpha=0.3, zorder=1))

# Wall thickness
for rect in [
    (0, 0, WALL_T, BOX_W),                     # left wall (pinhole face)
    (BOX_D - WALL_T, 0, WALL_T, BOX_W),        # right wall (film plane face)
    (0, 0, BOX_D, WALL_T),                      # bottom wall (arm-sleeve face)
    (0, BOX_W - WALL_T, BOX_D, WALL_T),        # top wall (opposite side)
]:
    ax.add_patch(mpatches.Rectangle(rect[:2], rect[2], rect[3],
                 facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=0.8, zorder=2))

# Backing board (against right wall, inside)
board_x = BOX_D - WALL_T - BACKING
ax.add_patch(mpatches.Rectangle((board_x, WALL_T), BACKING, BOX_W - 2 * WALL_T,
             facecolor=C_BACKING, edgecolor=C_OUT, linewidth=0.8, zorder=3))

# Muslin strip on backing board
ax.plot([board_x, board_x], [WALL_T + MARGIN, BOX_W - WALL_T - MARGIN],
        color=C_CL, lw=3.0, solid_capstyle="butt", zorder=4)

# Pinhole marker on left wall
ph_plan_y = BOX_W / 2
ax.add_patch(plt.Circle((WALL_T / 2, ph_plan_y), 6,
             facecolor=C_PINHOLE, edgecolor=C_OUT, linewidth=0.8, zorder=5))

# Optical axis
ax.plot([0, BOX_D], [ph_plan_y, ph_plan_y],
        color=C_CL, lw=0.7, ls="--", dashes=(8, 4), zorder=2)

# Armholes on bottom wall (arm-sleeve face)
# In plan view, sleeves project downward (toward viewer) through the bottom wall
sleeve_plan_cx1 = BOX_D / 2 - SLEEVE_SPACING / 2
sleeve_plan_cx2 = BOX_D / 2 + SLEEVE_SPACING / 2
sleeve_plan_cy  = WALL_T / 2  # centered in the wall thickness

for cx in [sleeve_plan_cx1, sleeve_plan_cx2]:
    # Armhole through wall (dark circle)
    ax.add_patch(plt.Circle((cx, sleeve_plan_cy), SLEEVE_D / 2,
                 facecolor=C_SLEEVE, edgecolor=C_OUT, linewidth=1.2, alpha=0.8, zorder=4))
    # Gaffer tape ring
    ax.add_patch(mpatches.Annulus((cx, sleeve_plan_cy), SLEEVE_D / 2 + 15, 12,
                 facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.5, alpha=0.4, zorder=3))
    # Sleeve projection extending below the box (fabric tube)
    sleeve_proj_len = 160  # mm shown below box
    ax.add_patch(mpatches.Rectangle(
        (cx - SLEEVE_D / 2, -sleeve_proj_len),
        SLEEVE_D, sleeve_proj_len,
        facecolor=C_SLEEVE, edgecolor=C_OUT, linewidth=0.8, alpha=0.15, zorder=1))
    # Sleeve outline
    ax.plot([cx - SLEEVE_D / 2, cx - SLEEVE_D / 2], [0, -sleeve_proj_len],
            color=C_SLEEVE, lw=1.0, ls="--", zorder=2)
    ax.plot([cx + SLEEVE_D / 2, cx + SLEEVE_D / 2], [0, -sleeve_proj_len],
            color=C_SLEEVE, lw=1.0, ls="--", zorder=2)
    # Elastic band at wrist (end of sleeve)
    ax.plot([cx - SLEEVE_D / 2 + 8, cx + SLEEVE_D / 2 - 8],
            [-sleeve_proj_len, -sleeve_proj_len],
            color=C_PINHOLE, lw=2.0, solid_capstyle="round", zorder=3)

# Face labels
ax.text(WALL_T / 2, BOX_W + 30, "PINHOLE\nFACE", ha="center", va="bottom",
        fontsize=FS_SM - 0.5, color=C_PINHOLE, fontweight="bold", rotation=0)
ax.text(BOX_D - WALL_T / 2, BOX_W + 30, "FILM PLANE\nFACE", ha="center", va="bottom",
        fontsize=FS_SM - 0.5, color=C_CL, fontweight="bold", rotation=0)
ax.text(BOX_D / 2, -PLAN_PAD + 10, "ARM-SLEEVE FACE (below)", ha="center", va="bottom",
        fontsize=FS_SM, color=C_DIM, style="italic")

# ── Plan dimensions ─────────────────────────────────────────────────────────
draw_dim_h(ax, 0, BOX_D, BOX_W + 60, f"Depth (focal length)  {BOX_D} mm  (18\")", offset=15)
draw_dim_v(ax, BOX_D + 70, 0, BOX_W, f"Width  {BOX_W} mm  (18\")", offset=15, right=True)
draw_dim_h(ax, sleeve_plan_cx1, sleeve_plan_cx2, -80,
           f"Sleeve spacing  {SLEEVE_SPACING} mm  (10\")", offset=12)
# Distance from pinhole face to first sleeve center
draw_dim_h(ax, 0, sleeve_plan_cx1, -40,
           f"{int(BOX_D/2 - SLEEVE_SPACING/2)} mm", offset=10, fs=FS_SM - 0.5)

# ── Plan leaders ────────────────────────────────────────────────────────────
leader(ax, sleeve_plan_cx1, -80, -80, -60,
       f"Fabric sleeve\nØ{SLEEVE_D} mm × {SLEEVE_LEN} mm long\n(projects downward)", ha="right")
leader(ax, sleeve_plan_cx2 + SLEEVE_D / 2 + 20, sleeve_plan_cy,
       BOX_D + 120, 60,
       "Gaffer tape\nseal ring", ha="left")
leader(ax, sleeve_plan_cx1, -sleeve_proj_len, -80, -sleeve_proj_len,
       "Elastic band\nat wrist", ha="right", color=C_PINHOLE)
leader(ax, board_x + BACKING / 2, BOX_W / 2, BOX_D + 120, BOX_W / 2,
       "Backing board +\ncoated muslin", ha="left", color=C_CL)

# View title
ax.text(BOX_D / 2, BOX_W + 110, "PLAN VIEW — LOOKING DOWN",
        ha="center", va="bottom", fontsize=FS_MD + 2, fontweight="bold", color=C_OUT)
ax.text(BOX_D / 2, BOX_W + 92,
        "Showing armhole placement on bottom face  —  sleeves project downward",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, style="italic")


# ── BOTTOM LEFT: Armhole detail cross-section ────────────────────────────────
ax = ax_det
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

# Detail drawing: cross-section through the armhole, showing layers
# Scale ~2:1 for clarity
# X = horizontal (through box wall and sleeve), Y = vertical (armhole height)
DET_PAD = 60
ax.set_xlim(-DET_PAD - 200, 300)
ax.set_ylim(-130, 130)

# ── Box wall (cross-section, horizontal slice) ──────────────────────────────
# Wall shown as thick vertical band at x=0
WALL_DRAW = 4 * 5     # exaggerated wall thickness for detail (20 drawing units)
HOLE_R = 51 * 1.0     # armhole radius at detail scale (51mm = ~102mm Ø at 1:1)

# Wall above armhole
ax.add_patch(mpatches.Rectangle((-WALL_DRAW / 2, HOLE_R), WALL_DRAW, 120 - HOLE_R,
             facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=1.0, zorder=3))
# Wall below armhole
ax.add_patch(mpatches.Rectangle((-WALL_DRAW / 2, -120), WALL_DRAW, 120 - HOLE_R,
             facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=1.0, zorder=3))

# Interior side label (right of wall)
ax.text(40, 115, "INTERIOR", ha="left", va="top", fontsize=FS_SM, color=C_DIM,
        fontweight="bold", style="italic")
# Exterior side label (left of wall)
ax.text(-40, 115, "EXTERIOR", ha="right", va="top", fontsize=FS_SM, color=C_DIM,
        fontweight="bold", style="italic")

# ── Armhole opening ─────────────────────────────────────────────────────────
# The hole in the wall
ax.plot([-WALL_DRAW / 2, -WALL_DRAW / 2], [-HOLE_R, HOLE_R],
        color=BG, lw=3, zorder=4)  # erase wall edge at hole
ax.plot([WALL_DRAW / 2, WALL_DRAW / 2], [-HOLE_R, HOLE_R],
        color=BG, lw=3, zorder=4)

# ── Fabric sleeve ────────────────────────────────────────────────────────────
SLEEVE_DRAW_LEN = 200  # sleeve extends to the left (exterior)
FABRIC_T = 3           # fabric line thickness (drawing units for fill)

# Sleeve tube — upper edge
ax.plot([-SLEEVE_DRAW_LEN, WALL_DRAW / 2 + 20], [HOLE_R, HOLE_R],
        color=C_SLEEVE, lw=1.5, zorder=5)
# Sleeve tube — lower edge
ax.plot([-SLEEVE_DRAW_LEN, WALL_DRAW / 2 + 20], [-HOLE_R, -HOLE_R],
        color=C_SLEEVE, lw=1.5, zorder=5)

# Fabric fill (semi-transparent)
ax.add_patch(mpatches.Rectangle((-SLEEVE_DRAW_LEN, -HOLE_R), SLEEVE_DRAW_LEN + WALL_DRAW / 2 + 20,
             HOLE_R * 2, facecolor=C_SLEEVE, edgecolor="none", alpha=0.06, zorder=1))

# ── Gaffer tape attachment (interior side) ───────────────────────────────────
# Tape wraps from inside the box, over the wall edge, onto the sleeve fabric
TAPE_W = 25  # tape width (drawing units)

# Upper tape strip — inside wall surface, across edge, onto sleeve
tape_upper_verts = [
    (WALL_DRAW / 2, HOLE_R + TAPE_W),       # top of tape on inside wall
    (WALL_DRAW / 2, HOLE_R),                 # wall edge at hole
    (WALL_DRAW / 2 + 20, HOLE_R),            # wrap onto sleeve (outside edge)
    (WALL_DRAW / 2 + 20, HOLE_R + TAPE_W),  # top of tape on sleeve
]
ax.add_patch(mpatches.Polygon(tape_upper_verts, closed=True,
             facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=6))

# Lower tape strip
tape_lower_verts = [
    (WALL_DRAW / 2, -HOLE_R - TAPE_W),
    (WALL_DRAW / 2, -HOLE_R),
    (WALL_DRAW / 2 + 20, -HOLE_R),
    (WALL_DRAW / 2 + 20, -HOLE_R - TAPE_W),
]
ax.add_patch(mpatches.Polygon(tape_lower_verts, closed=True,
             facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=6))

# ── Second tape layer (exterior side, optional reinforcement) ────────────────
tape_ext_upper = [
    (-WALL_DRAW / 2, HOLE_R + TAPE_W),
    (-WALL_DRAW / 2, HOLE_R),
    (-WALL_DRAW / 2 - 20, HOLE_R),
    (-WALL_DRAW / 2 - 20, HOLE_R + TAPE_W),
]
ax.add_patch(mpatches.Polygon(tape_ext_upper, closed=True,
             facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.6, alpha=0.5, zorder=6))

tape_ext_lower = [
    (-WALL_DRAW / 2, -HOLE_R - TAPE_W),
    (-WALL_DRAW / 2, -HOLE_R),
    (-WALL_DRAW / 2 - 20, -HOLE_R),
    (-WALL_DRAW / 2 - 20, -HOLE_R - TAPE_W),
]
ax.add_patch(mpatches.Polygon(tape_ext_lower, closed=True,
             facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.6, alpha=0.5, zorder=6))

# ── Elastic band at wrist ───────────────────────────────────────────────────
ELASTIC_X = -SLEEVE_DRAW_LEN + 10
# Gathered fabric (narrowing at wrist)
ax.plot([ELASTIC_X, ELASTIC_X - 15], [HOLE_R, HOLE_R - 15],
        color=C_SLEEVE, lw=1.5, zorder=5)
ax.plot([ELASTIC_X, ELASTIC_X - 15], [-HOLE_R, -HOLE_R + 15],
        color=C_SLEEVE, lw=1.5, zorder=5)
# Elastic band ring
ax.add_patch(mpatches.Rectangle((ELASTIC_X - 18, -HOLE_R + 12), 8, (HOLE_R - 12) * 2,
             facecolor=C_PINHOLE, edgecolor=C_OUT, linewidth=0.8, alpha=0.6, zorder=7))

# ── Detail dimensions ───────────────────────────────────────────────────────
draw_dim_v(ax, 100, -HOLE_R, HOLE_R,
           f"Ø{SLEEVE_D} mm\n(4\")", offset=18, right=True, fs=FS_SM)
draw_dim_h(ax, -SLEEVE_DRAW_LEN, WALL_DRAW / 2, -HOLE_R - 50,
           f"Sleeve length  ~{SLEEVE_LEN} mm  (18\")", offset=12, fs=FS_SM - 0.5)
draw_dim_h(ax, -WALL_DRAW / 2, WALL_DRAW / 2, HOLE_R + 60,
           f"Wall  ~{WALL_T} mm", offset=10, fs=FS_SM - 0.5)

# ── Detail leaders ──────────────────────────────────────────────────────────
leader(ax, WALL_DRAW / 2 + 10, HOLE_R + TAPE_W / 2, 180, HOLE_R + 50,
       "Gaffer tape\n(2\" wide, light-tight)\nInterior side", ha="left")
leader(ax, -WALL_DRAW / 2 - 10, HOLE_R + TAPE_W / 2, -DET_PAD - 140, HOLE_R + 50,
       "Gaffer tape\nExterior reinforcement", ha="right")
leader(ax, ELASTIC_X - 14, 0, -DET_PAD - 140, -20,
       "Heavy-duty\nrubber band\n(wrist seal)", ha="right", color=C_PINHOLE)
leader(ax, -SLEEVE_DRAW_LEN / 2, HOLE_R + 3, -SLEEVE_DRAW_LEN / 2, HOLE_R + 50,
       "Black cotton fabric\nsleeve (cut from t-shirt\nor 1/2 yd fabric)", ha="center")

# View title
ax.text(-10, -120, "DETAIL A — ARMHOLE CROSS-SECTION",
        ha="center", va="top", fontsize=FS_MD + 1, fontweight="bold", color=C_OUT)
ax.text(-10, -108,
        "Section through box wall at armhole centerline",
        ha="center", va="top", fontsize=FS_SM, color=C_DIM, style="italic")


# ── BOTTOM RIGHT: Assembly sequence notes ────────────────────────────────────
ax = ax_exp
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(0, 400)
ax.set_ylim(0, 300)

# Assembly steps callout box
ax.add_patch(mpatches.FancyBboxPatch((10, 10), 380, 280,
             boxstyle="round,pad=8", facecolor="#F8F6F0", edgecolor=C_OUT,
             linewidth=0.8, zorder=1))

ax.text(200, 275, "ARMHOLE ASSEMBLY SEQUENCE", ha="center", va="top",
        fontsize=FS_MD + 0.5, fontweight="bold", color=C_OUT)
ax.plot([30, 370], [265, 265], color=C_OUT, lw=0.6)

steps = [
    "1.  Mark two Ø102 mm (4\") circles on the\n"
    "     arm-sleeve face, spaced 254 mm (10\")\n"
    "     center-to-center, vertically centered.",
    "2.  Cut holes with a box cutter. Clean edges.",
    "3.  Cut two sleeves from black fabric:\n"
    "     each ~Ø150 mm × 457 mm (18\") long.",
    "4.  Insert sleeve through hole from exterior.\n"
    "     Pull 50 mm (~2\") through to interior side.",
    "5.  Tape interior flap to inside wall surface\n"
    "     with 2\" gaffer tape — full circumference.\n"
    "     Ensure no gaps (light-tight seal).",
    "6.  Tape exterior junction for reinforcement.",
    "7.  Slip heavy-duty rubber band over wrist\n"
    "     end of each sleeve for light seal.",
]

y = 250
for step in steps:
    ax.text(30, y, step, ha="left", va="top",
            fontsize=FS_SM - 0.3, color=C_DIM, linespacing=1.3)
    y -= 32


# ── Title block ─────────────────────────────────────────────────────────────
ax_tb2 = fig2.add_axes([0, 0, 1, 1], facecolor="none")
ax_tb2.axis("off")
title_block(ax_tb2, "SHEET 2 OF 2",
            drawing_title="MINI-TBS PROOF OF CONCEPT",
            subtitle="Plan view + armhole detail — construction and attachment",
            scale_note="Approx 1:3 (plan) / ~2:1 (detail)",
            doc_id="TBS-POC · Mini-TBS")

# ── Save Sheet 2 ─────────────────────────────────────────────────────────────
out2 = f"{DIAGRAMS_DIR}/mini-tbs-sheet2.png"
plt.savefig(out2, dpi=150, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.savefig(svg_path(out2), bbox_inches="tight", facecolor=BG)
plt.close(fig2)
print(f"Saved: {out2}")
