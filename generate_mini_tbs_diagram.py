#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_mini_tbs_diagram.py

Mini-TBS proof-of-concept pinhole camera — engineering drawing.
Output: diagrams/mini-tbs-sheet1.png

Single sheet with five panels:
  Top-left:     Side cross-section
  Top-right:    Plan view (looking down)
  Bottom-left:  Front view of arm-sleeve face
  Bottom-center: Armhole detail cross-section
  Bottom-right: Assembly sequence notes
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

FS_SM = 6.5
FS_MD = 8.0

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
# SINGLE SHEET — Five panels
# ══════════════════════════════════════════════════════════════════════════════

FIG_W = 24.0
FIG_H = 20.0
fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=150)
fig.patch.set_facecolor(BG)

# Gridspec: 2 rows × 3 columns
# Top row: side cross-section (cols 0-1) + plan view (col 2)
# Bottom row: front view (col 0) + armhole detail (col 1) + assembly notes (col 2)
gs = fig.add_gridspec(2, 3,
                      height_ratios=[1, 1],
                      width_ratios=[1, 1.1, 0.9],
                      hspace=0.22, wspace=0.18,
                      left=0.04, right=0.96, bottom=0.06, top=0.95)

ax_xsec = fig.add_subplot(gs[0, 0:2])   # side cross-section — top-left, 2 cols
ax_plan = fig.add_subplot(gs[0, 2])      # plan view — top-right
ax_front = fig.add_subplot(gs[1, 0])     # front view — bottom-left
ax_det  = fig.add_subplot(gs[1, 1])      # armhole detail — bottom-center
ax_asm  = fig.add_subplot(gs[1, 2])      # assembly notes — bottom-right


# ══════════════════════════════════════════════════════════════════════════════
# TOP-LEFT: Side cross-section (looking at 18×16" face)
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_xsec
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

PAD = 120
ax.set_xlim(-PAD, BOX_D + PAD * 2)
ax.set_ylim(-PAD, BOX_H + PAD)

# Box outline (cross-section)
ax.add_patch(mpatches.Rectangle((0, 0), BOX_D, BOX_H,
             facecolor=C_BOX, edgecolor=C_OUT, linewidth=1.5, alpha=0.3, zorder=1))

# Wall thickness indicators
for rect in [
    (0, 0, WALL_T, BOX_H),
    (BOX_D - WALL_T, 0, WALL_T, BOX_H),
    (0, 0, BOX_D, WALL_T),
    (0, BOX_H - WALL_T, BOX_D, WALL_T),
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
ax.plot([WALL_T / 2 - 12, WALL_T / 2 + 12], [ph_y, ph_y],
        color=C_PINHOLE, lw=0.8, zorder=6)
ax.plot([WALL_T / 2, WALL_T / 2], [ph_y - 12, ph_y + 12],
        color=C_PINHOLE, lw=0.8, zorder=6)

# Aluminum plate behind pinhole (interior side)
ax.add_patch(mpatches.Rectangle((WALL_T, ph_y - 38), 2, 76,
             facecolor=C_ALUM, edgecolor=C_OUT, linewidth=0.6, zorder=4))

# Light cone
cone_verts = [
    (WALL_T, ph_y),
    (muslin_x, muslin_y2),
    (muslin_x, muslin_y1),
]
ax.add_patch(mpatches.Polygon(cone_verts, closed=True,
             facecolor=C_CONE, edgecolor="none", alpha=0.25, zorder=1))
ax.plot([WALL_T, muslin_x], [ph_y, muslin_y2],
        color=C_CONE_LN, lw=0.8, ls="--", dashes=(6, 4), alpha=0.7, zorder=2)
ax.plot([WALL_T, muslin_x], [ph_y, muslin_y1],
        color=C_CONE_LN, lw=0.8, ls="--", dashes=(6, 4), alpha=0.7, zorder=2)

# Optical axis
ax.plot([0, BOX_D], [ph_y, ph_y],
        color=C_CL, lw=0.7, ls="--", dashes=(8, 4), zorder=2)

# Shutter flap
ax.add_patch(mpatches.Rectangle((-30, ph_y - 50), 28, 100,
             facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=3))

# Dimensions
draw_dim_h(ax, 0, BOX_D, -50, f"Focal length  {BOX_D} mm  (18\")", offset=15)
draw_dim_v(ax, BOX_D + 60, 0, BOX_H, f"Box height  {BOX_H} mm  (16\")", offset=15, right=True)
draw_dim_v(ax, BOX_D + 120, muslin_y1, muslin_y2,
           f"Image  {FP_H} mm", offset=15, color=C_CL, right=True)

# Leaders
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
        ha="center", va="bottom", fontsize=FS_MD + 1, fontweight="bold", color=C_OUT)
ax.text(BOX_D / 2, BOX_H + 84,
        "Looking at 18\" × 16\" face  —  pinhole left, film plane right",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, style="italic")


# ══════════════════════════════════════════════════════════════════════════════
# TOP-RIGHT: Plan view (looking down)
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_plan
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

PLAN_PAD = 130
ax.set_xlim(-PLAN_PAD, BOX_D + PLAN_PAD * 1.5)
ax.set_ylim(-PLAN_PAD, BOX_W + PLAN_PAD)

# Box outline — depth (left-right) × width (bottom-top)
ax.add_patch(mpatches.Rectangle((0, 0), BOX_D, BOX_W,
             facecolor=C_BOX, edgecolor=C_OUT, linewidth=1.5, alpha=0.3, zorder=1))

# Wall thickness
for rect in [
    (0, 0, WALL_T, BOX_W),
    (BOX_D - WALL_T, 0, WALL_T, BOX_W),
    (0, 0, BOX_D, WALL_T),
    (0, BOX_W - WALL_T, BOX_D, WALL_T),
]:
    ax.add_patch(mpatches.Rectangle(rect[:2], rect[2], rect[3],
                 facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=0.8, zorder=2))

# Backing board
plan_board_x = BOX_D - WALL_T - BACKING
ax.add_patch(mpatches.Rectangle((plan_board_x, WALL_T), BACKING, BOX_W - 2 * WALL_T,
             facecolor=C_BACKING, edgecolor=C_OUT, linewidth=0.8, zorder=3))

# Muslin
ax.plot([plan_board_x, plan_board_x], [WALL_T + MARGIN, BOX_W - WALL_T - MARGIN],
        color=C_CL, lw=3.0, solid_capstyle="butt", zorder=4)

# Pinhole marker
ph_plan_y = BOX_W / 2
ax.add_patch(plt.Circle((WALL_T / 2, ph_plan_y), 6,
             facecolor=C_PINHOLE, edgecolor=C_OUT, linewidth=0.8, zorder=5))

# Optical axis
ax.plot([0, BOX_D], [ph_plan_y, ph_plan_y],
        color=C_CL, lw=0.7, ls="--", dashes=(8, 4), zorder=2)

# Armholes on bottom wall
sleeve_plan_cx1 = BOX_D / 2 - SLEEVE_SPACING / 2
sleeve_plan_cx2 = BOX_D / 2 + SLEEVE_SPACING / 2
sleeve_plan_cy  = WALL_T / 2

for cx in [sleeve_plan_cx1, sleeve_plan_cx2]:
    ax.add_patch(plt.Circle((cx, sleeve_plan_cy), SLEEVE_D / 2,
                 facecolor=C_SLEEVE, edgecolor=C_OUT, linewidth=1.2, alpha=0.8, zorder=4))
    ax.add_patch(mpatches.Annulus((cx, sleeve_plan_cy), SLEEVE_D / 2 + 15, 12,
                 facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.5, alpha=0.4, zorder=3))
    # Sleeve projection
    sleeve_proj_len = 120
    ax.add_patch(mpatches.Rectangle(
        (cx - SLEEVE_D / 2, -sleeve_proj_len),
        SLEEVE_D, sleeve_proj_len,
        facecolor=C_SLEEVE, edgecolor=C_OUT, linewidth=0.8, alpha=0.15, zorder=1))
    ax.plot([cx - SLEEVE_D / 2, cx - SLEEVE_D / 2], [0, -sleeve_proj_len],
            color=C_SLEEVE, lw=1.0, ls="--", zorder=2)
    ax.plot([cx + SLEEVE_D / 2, cx + SLEEVE_D / 2], [0, -sleeve_proj_len],
            color=C_SLEEVE, lw=1.0, ls="--", zorder=2)
    ax.plot([cx - SLEEVE_D / 2 + 8, cx + SLEEVE_D / 2 - 8],
            [-sleeve_proj_len, -sleeve_proj_len],
            color=C_PINHOLE, lw=2.0, solid_capstyle="round", zorder=3)

# Face labels
ax.text(WALL_T / 2, BOX_W + 25, "PINHOLE\nFACE", ha="center", va="bottom",
        fontsize=FS_SM - 0.5, color=C_PINHOLE, fontweight="bold")
ax.text(BOX_D - WALL_T / 2, BOX_W + 25, "FILM PLANE\nFACE", ha="center", va="bottom",
        fontsize=FS_SM - 0.5, color=C_CL, fontweight="bold")
ax.text(BOX_D / 2, -PLAN_PAD + 15, "ARM-SLEEVE FACE (below)", ha="center", va="bottom",
        fontsize=FS_SM - 0.5, color=C_DIM, style="italic")

# Dimensions
draw_dim_h(ax, 0, BOX_D, BOX_W + 55, f"Depth  {BOX_D} mm  (18\")", offset=12)
draw_dim_v(ax, BOX_D + 55, 0, BOX_W, f"Width  {BOX_W} mm  (18\")", offset=12, right=True)
draw_dim_h(ax, sleeve_plan_cx1, sleeve_plan_cx2, -60,
           f"Spacing  {SLEEVE_SPACING} mm  (10\")", offset=10, fs=FS_SM - 0.5)

# Leaders
leader(ax, sleeve_plan_cx1, -60, -80, -50,
       f"Fabric sleeve\nØ{SLEEVE_D} mm", ha="right", fs=FS_SM - 0.5)
leader(ax, sleeve_plan_cx2 + SLEEVE_D / 2 + 20, sleeve_plan_cy,
       BOX_D + 100, 50,
       "Gaffer tape\nseal ring", ha="left", fs=FS_SM - 0.5)
leader(ax, sleeve_plan_cx1, -sleeve_proj_len, -80, -sleeve_proj_len,
       "Elastic band", ha="right", color=C_PINHOLE, fs=FS_SM - 0.5)

# Section cut indicator — dashed line through one armhole with "A" labels
cut_cx = sleeve_plan_cx1
ax.plot([cut_cx, cut_cx], [-sleeve_proj_len - 15, BOX_W * 0.35],
        color=C_PINHOLE, lw=1.0, ls="-.", dashes=(8, 3, 2, 3), alpha=0.6, zorder=6)
ax.text(cut_cx + 8, BOX_W * 0.35, "A", fontsize=FS_MD, fontweight="bold",
        color=C_PINHOLE, ha="left", va="center")
ax.text(cut_cx + 8, -sleeve_proj_len - 10, "A", fontsize=FS_MD, fontweight="bold",
        color=C_PINHOLE, ha="left", va="center")

# View title
ax.text(BOX_D / 2, BOX_W + 100, "PLAN VIEW — LOOKING DOWN",
        ha="center", va="bottom", fontsize=FS_MD + 1, fontweight="bold", color=C_OUT)
ax.text(BOX_D / 2, BOX_W + 84,
        "Armhole placement on bottom face",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, style="italic")


# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM-LEFT: Front view of arm-sleeve face (18×18" face)
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_front
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

ax.set_xlim(-PAD, BOX_W + PAD * 1.5)
ax.set_ylim(-PAD - 20, BOX_D + PAD)

# Box face outline
ax.add_patch(mpatches.Rectangle((0, 0), BOX_W, BOX_D,
             facecolor=C_BOX, edgecolor=C_OUT, linewidth=1.5, alpha=0.3, zorder=1))

# Wall thickness
for rect in [
    (0, 0, WALL_T, BOX_D),
    (BOX_W - WALL_T, 0, WALL_T, BOX_D),
    (0, 0, BOX_W, WALL_T),
    (0, BOX_D - WALL_T, BOX_W, WALL_T),
]:
    ax.add_patch(mpatches.Rectangle(rect[:2], rect[2], rect[3],
                 facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=0.8, zorder=2))

# Arm sleeves
sleeve_cy = BOX_D / 2
sleeve_cx1 = BOX_W / 2 - SLEEVE_SPACING / 2
sleeve_cx2 = BOX_W / 2 + SLEEVE_SPACING / 2

for cx in [sleeve_cx1, sleeve_cx2]:
    ax.add_patch(plt.Circle((cx, sleeve_cy), SLEEVE_D / 2,
                 facecolor=C_SLEEVE, edgecolor=C_OUT, linewidth=1.2, alpha=0.8, zorder=4))
    ax.add_patch(plt.Circle((cx, sleeve_cy), SLEEVE_D / 2 + 15,
                 facecolor="none", edgecolor=C_SLEEVE, linewidth=0.8,
                 linestyle="--", alpha=0.5, zorder=3))

# Gaffer tape seal
for cx in [sleeve_cx1, sleeve_cx2]:
    ax.add_patch(mpatches.Annulus((cx, sleeve_cy), SLEEVE_D / 2 + 15, 12,
                 facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.5, alpha=0.4, zorder=3))

# Dimensions
draw_dim_h(ax, 0, BOX_W, -50, f"Box width  {BOX_W} mm  (18\")", offset=12)
draw_dim_v(ax, BOX_W + 50, 0, BOX_D, f"Box depth  {BOX_D} mm  (18\")", offset=12, right=True)
draw_dim_h(ax, sleeve_cx1, sleeve_cx2, BOX_D + 40,
           f"Spacing  {SLEEVE_SPACING} mm  (10\")", offset=12, fs=FS_SM - 0.5)
draw_dim_h(ax, sleeve_cx1 - SLEEVE_D / 2, sleeve_cx1 + SLEEVE_D / 2,
           sleeve_cy - SLEEVE_D / 2 - 25,
           f"Ø{SLEEVE_D} mm (4\")", offset=10, fs=FS_SM - 0.5)

# Leaders
leader(ax, sleeve_cx1, sleeve_cy, -50, sleeve_cy + 50,
       f"Armhole Ø{SLEEVE_D} mm\n(black fabric sleeve)\nElastic at wrist", ha="right", fs=FS_SM - 0.5)
leader(ax, sleeve_cx1 + SLEEVE_D / 2 + 20, sleeve_cy, BOX_W + 80, sleeve_cy + 80,
       "Gaffer tape seal\n(light-tight)", ha="left", fs=FS_SM - 0.5)

# Specification table
spec_x = BOX_W + 80
spec_y = BOX_D - 60
specs = [
    f"Focal length:  {FOCAL} mm",
    f"Pinhole:  Ø{PH_D} mm",
    f"f-number:  f/{F_NO}",
    f"Film plane:  {FP_W} × {FP_H} mm",
    f"Exposure:  ~10 min  (full sun)",
    "Process:  Ware New Cyanotype",
    "Reciprocity:  None (iron-based)",
]
ax.text(spec_x, spec_y + 18, "SPECIFICATION", ha="left", va="bottom",
        fontsize=FS_SM + 0.5, fontweight="bold", color=C_OUT)
ax.plot([spec_x, spec_x + 200], [spec_y + 14, spec_y + 14], color=C_OUT, lw=0.8)
for i, line in enumerate(specs):
    ax.text(spec_x, spec_y - i * 18, line, ha="left", va="top",
            fontsize=FS_SM - 0.5, color=C_DIM)

# View title
ax.text(BOX_W / 2, BOX_D + 90, "FRONT VIEW — ARM-SLEEVE FACE",
        ha="center", va="bottom", fontsize=FS_MD + 1, fontweight="bold", color=C_OUT)
ax.text(BOX_W / 2, BOX_D + 74,
        "18\" × 18\" side face  —  two armholes",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, style="italic")


# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM-CENTER: Armhole detail cross-section (Detail A)
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_det
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

DET_PAD = 60
ax.set_xlim(-DET_PAD - 200, 280)
ax.set_ylim(-130, 130)

# Box wall cross-section
WALL_DRAW = 4 * 5     # exaggerated wall thickness (20 drawing units)
HOLE_R = 51 * 1.0     # armhole radius at detail scale

# Wall above armhole
ax.add_patch(mpatches.Rectangle((-WALL_DRAW / 2, HOLE_R), WALL_DRAW, 120 - HOLE_R,
             facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=1.0, zorder=3))
# Wall below armhole
ax.add_patch(mpatches.Rectangle((-WALL_DRAW / 2, -120), WALL_DRAW, 120 - HOLE_R,
             facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=1.0, zorder=3))

# Side labels
ax.text(40, 115, "INTERIOR", ha="left", va="top", fontsize=FS_SM - 0.5, color=C_DIM,
        fontweight="bold", style="italic")
ax.text(-40, 115, "EXTERIOR", ha="right", va="top", fontsize=FS_SM - 0.5, color=C_DIM,
        fontweight="bold", style="italic")

# Clear wall edges at hole
ax.plot([-WALL_DRAW / 2, -WALL_DRAW / 2], [-HOLE_R, HOLE_R],
        color=BG, lw=3, zorder=4)
ax.plot([WALL_DRAW / 2, WALL_DRAW / 2], [-HOLE_R, HOLE_R],
        color=BG, lw=3, zorder=4)

# Fabric sleeve
SLEEVE_DRAW_LEN = 200

ax.plot([-SLEEVE_DRAW_LEN, WALL_DRAW / 2 + 20], [HOLE_R, HOLE_R],
        color=C_SLEEVE, lw=1.5, zorder=5)
ax.plot([-SLEEVE_DRAW_LEN, WALL_DRAW / 2 + 20], [-HOLE_R, -HOLE_R],
        color=C_SLEEVE, lw=1.5, zorder=5)

ax.add_patch(mpatches.Rectangle((-SLEEVE_DRAW_LEN, -HOLE_R),
             SLEEVE_DRAW_LEN + WALL_DRAW / 2 + 20, HOLE_R * 2,
             facecolor=C_SLEEVE, edgecolor="none", alpha=0.06, zorder=1))

# Gaffer tape — interior side
TAPE_W = 25
tape_upper_verts = [
    (WALL_DRAW / 2, HOLE_R + TAPE_W),
    (WALL_DRAW / 2, HOLE_R),
    (WALL_DRAW / 2 + 20, HOLE_R),
    (WALL_DRAW / 2 + 20, HOLE_R + TAPE_W),
]
ax.add_patch(mpatches.Polygon(tape_upper_verts, closed=True,
             facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=6))

tape_lower_verts = [
    (WALL_DRAW / 2, -HOLE_R - TAPE_W),
    (WALL_DRAW / 2, -HOLE_R),
    (WALL_DRAW / 2 + 20, -HOLE_R),
    (WALL_DRAW / 2 + 20, -HOLE_R - TAPE_W),
]
ax.add_patch(mpatches.Polygon(tape_lower_verts, closed=True,
             facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=6))

# Gaffer tape — exterior side
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

# Elastic band at wrist
ELASTIC_X = -SLEEVE_DRAW_LEN + 10
ax.plot([ELASTIC_X, ELASTIC_X - 15], [HOLE_R, HOLE_R - 15],
        color=C_SLEEVE, lw=1.5, zorder=5)
ax.plot([ELASTIC_X, ELASTIC_X - 15], [-HOLE_R, -HOLE_R + 15],
        color=C_SLEEVE, lw=1.5, zorder=5)
ax.add_patch(mpatches.Rectangle((ELASTIC_X - 18, -HOLE_R + 12), 8, (HOLE_R - 12) * 2,
             facecolor=C_PINHOLE, edgecolor=C_OUT, linewidth=0.8, alpha=0.6, zorder=7))

# Dimensions
draw_dim_v(ax, 90, -HOLE_R, HOLE_R,
           f"Ø{SLEEVE_D} mm\n(4\")", offset=15, right=True, fs=FS_SM - 0.5)
draw_dim_h(ax, -SLEEVE_DRAW_LEN, WALL_DRAW / 2, -HOLE_R - 45,
           f"Sleeve  ~{SLEEVE_LEN} mm  (18\")", offset=10, fs=FS_SM - 0.5)
draw_dim_h(ax, -WALL_DRAW / 2, WALL_DRAW / 2, HOLE_R + 55,
           f"Wall  ~{WALL_T} mm", offset=8, fs=FS_SM - 0.5)

# Leaders
leader(ax, WALL_DRAW / 2 + 10, HOLE_R + TAPE_W / 2, 160, HOLE_R + 45,
       "Gaffer tape (2\" wide)\nInterior — light-tight seal", ha="left", fs=FS_SM - 0.5)
leader(ax, -WALL_DRAW / 2 - 10, HOLE_R + TAPE_W / 2, -DET_PAD - 120, HOLE_R + 45,
       "Gaffer tape\nExterior reinforcement", ha="right", fs=FS_SM - 0.5)
leader(ax, ELASTIC_X - 14, 0, -DET_PAD - 120, -20,
       "Rubber band\n(wrist seal)", ha="right", color=C_PINHOLE, fs=FS_SM - 0.5)
leader(ax, -SLEEVE_DRAW_LEN / 2, HOLE_R + 3, -SLEEVE_DRAW_LEN / 2, HOLE_R + 45,
       "Black cotton fabric sleeve", ha="center", fs=FS_SM - 0.5)

# View title
ax.text(-10, -120, "DETAIL A — ARMHOLE CROSS-SECTION",
        ha="center", va="top", fontsize=FS_MD, fontweight="bold", color=C_OUT)
ax.text(-10, -110,
        "Section through box wall at armhole centerline",
        ha="center", va="top", fontsize=FS_SM - 0.5, color=C_DIM, style="italic")


# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM-RIGHT: Assembly sequence notes
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_asm
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(0, 400)
ax.set_ylim(0, 300)

ax.add_patch(mpatches.FancyBboxPatch((10, 10), 380, 280,
             boxstyle="round,pad=8", facecolor="#F8F6F0", edgecolor=C_OUT,
             linewidth=0.8, zorder=1))

ax.text(200, 275, "ARMHOLE ASSEMBLY", ha="center", va="top",
        fontsize=FS_MD, fontweight="bold", color=C_OUT)
ax.plot([30, 370], [265, 265], color=C_OUT, lw=0.6)

steps = [
    "1.  Mark two Ø102 mm (4\") circles on\n"
    "     arm-sleeve face, spaced 254 mm\n"
    "     (10\") c-c, vertically centered.",
    "2.  Cut holes with box cutter.\n"
    "     Clean edges.",
    "3.  Cut two sleeves from black fabric:\n"
    "     each ~Ø150 mm × 457 mm long.",
    "4.  Insert sleeve from exterior.\n"
    "     Pull ~50 mm through to interior.",
    "5.  Tape interior flap to wall with\n"
    "     2\" gaffer tape — full circumference.\n"
    "     No gaps (light-tight seal).",
    "6.  Tape exterior junction for\n"
    "     reinforcement.",
    "7.  Slip rubber band over wrist end\n"
    "     of each sleeve for light seal.",
]

y = 250
for step in steps:
    ax.text(30, y, step, ha="left", va="top",
            fontsize=FS_SM - 0.5, color=C_DIM, linespacing=1.25)
    y -= 32


# ── Title block (full-figure overlay) ────────────────────────────────────────
ax_tb = fig.add_axes([0, 0, 1, 1], facecolor="none")
ax_tb.axis("off")
title_block(ax_tb, "SHEET 1 OF 1",
            drawing_title="MINI-TBS PROOF OF CONCEPT",
            subtitle="Cross-section, plan view, arm-sleeve face, and armhole detail",
            scale_note="Approx 1:3 (views) / ~2:1 (detail)",
            doc_id="TBS-POC · Mini-TBS")

# ── Save ─────────────────────────────────────────────────────────────────────
out = f"{DIAGRAMS_DIR}/mini-tbs-sheet1.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(f"Saved: {out}")
