#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_mini_tbs_diagram.py

Mini-TBS proof-of-concept pinhole camera — engineering drawing.
Output: diagrams/mini-tbs-sheet1.png

Single sheet with four panels:
  Top (full width):    Side cross-section — camera box + prep box, photo tray,
                       permanently-hinged backing board with armholes
  Bottom-left:         Board face — prep side (armholes + sleeve attachment)
  Bottom-center:       Plan view — both boxes from above
  Bottom-right:        Specification + assembly notes
"""

import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Arc
import numpy as np
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
SLEEVE_SPACING = 230  # mm — armhole center-to-center spacing

WALL_T  = 4      # mm — cardboard wall thickness (schematic)
BACKING = 5      # mm — foam-core backing board thickness

# Prep box dimensions (same box model)
PREP_D  = BOX_D  # mm — prep box depth (matches camera box)
TOTAL_D = BOX_D + PREP_D

# Photo tray: Paterson 12×16" developing tray (PTP326)
TRAY_EXT_D = 340   # mm — external depth in cross-section (~13.4")
TRAY_EXT_W = 445   # mm — external width (perpendicular to cross-section)
TRAY_RIM   = 65    # mm — rim height (~2.5")

# Board dimensions (fits inside camera box, hinged at tray rim height)
BOARD_W = BOX_W - 2 * WALL_T - 6   # ~443 mm — board width (clearance)
HINGE_Y_ABS = WALL_T + TRAY_RIM    # 69 mm — hinge height (tray rim on floor)
BOARD_H = BOX_H - WALL_T - HINGE_Y_ABS  # ~333 mm — from hinge to ceiling interior

# ── Drawing palette ──────────────────────────────────────────────────────────
BG         = "#FFFFFF"
C_BOX      = "#D2B48C"    # tan — cardboard
C_BOX_WALL = "#C4A882"    # darker cardboard for walls
C_TAPE     = "#1A1A1A"    # black gaffer tape
C_CONE     = "#CCE4FF"    # light cone fill
C_CONE_LN  = "#4488CC"    # light cone boundary
C_PINHOLE  = "#CC2020"    # pinhole marker
C_SLEEVE   = "#2A2A2A"    # arm sleeve fabric
C_BACKING  = "#E8E0D0"    # foam-core board
C_ALUM     = "#C0C0C8"    # aluminum pinhole plate
C_PAPER    = "#FAFAE8"    # watercolor paper
C_HINGE    = "#886644"    # duct tape hinge
C_TRAY     = "#8899BB"    # chemistry tray
C_MOTION   = "#CC6600"    # motion arc color
C_FLAP     = "#77AA77"    # extraction flap

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

FIG_W = 30.0
FIG_H = 22.0
fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=150)
fig.patch.set_facecolor(BG)

gs = fig.add_gridspec(3, 4,
                      height_ratios=[1.0, 1.0, 0.55],
                      width_ratios=[0.7, 1.0, 0.8, 0.65],
                      hspace=0.22, wspace=0.18,
                      left=0.03, right=0.97, bottom=0.06, top=0.95)

ax_board = fig.add_subplot(gs[0, 0])    # end face — operator side (top-left)
ax_xsec  = fig.add_subplot(gs[0, 1:])   # side cross-section (top, columns 1-3)
ax_armdt = fig.add_subplot(gs[1, 0])    # armhole detail cross-section
ax_planv = fig.add_subplot(gs[1, 1:])   # plan view (columns 1-3, same span as xsec)
ax_asm   = fig.add_subplot(gs[2, :])    # spec + workflow — full-width bottom row


# ══════════════════════════════════════════════════════════════════════════════
# TOP: Side cross-section — camera box + prep box with photo tray
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_xsec
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

# ── Layout constants ───────────────────────────────────────────────────────
tray_x = BOX_D + WALL_T            # tray near edge (camera side of prep box)
tray_x_far = tray_x + TRAY_EXT_D   # tray far rim
hinge_x = tray_x                   # hinge at tray NEAR rim (camera side)
hinge_y = WALL_T + TRAY_RIM        # hinge height (at tray near rim level)
board_fold_end = hinge_x + BOARD_H  # board tip when folded horizontal

PAD = 120
# Extend right limit to show extraction flap arc and open position
flap_open_end = BOX_D + PREP_D + BOX_H * 0.3  # enough to show arc + partial open flap
ax.set_xlim(-PAD - 40, max(board_fold_end + PAD, flap_open_end + PAD))
ax.set_ylim(-PAD - 30, BOX_H + PAD + 20)

# ── Camera box (left) ───────────────────────────────────────────────────────
ax.add_patch(mpatches.Rectangle((0, 0), BOX_D, BOX_H,
             facecolor=C_BOX, edgecolor=C_OUT, linewidth=1.5, alpha=0.25, zorder=1))

for rect in [
    (0, 0, WALL_T, BOX_H),                     # left wall (pinhole face)
    (0, 0, BOX_D, WALL_T),                      # floor
    (0, BOX_H - WALL_T, BOX_D, WALL_T),        # ceiling
]:
    ax.add_patch(mpatches.Rectangle(rect[:2], rect[2], rect[3],
                 facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=0.8, zorder=2))

# No right wall on camera box (open at junction)
ax.plot([BOX_D, BOX_D], [0, WALL_T], color=C_OUT, lw=0.8, zorder=2)
ax.plot([BOX_D, BOX_D], [BOX_H - WALL_T, BOX_H], color=C_OUT, lw=0.8, zorder=2)

# ── Prep box (right) ────────────────────────────────────────────────────────
ax.add_patch(mpatches.Rectangle((BOX_D, 0), PREP_D, BOX_H,
             facecolor=C_BOX, edgecolor=C_OUT, linewidth=1.5, alpha=0.15, zorder=1))

for rect in [
    (BOX_D, 0, PREP_D, WALL_T),                     # floor
    (BOX_D, BOX_H - WALL_T, PREP_D, WALL_T),       # ceiling
]:
    ax.add_patch(mpatches.Rectangle(rect[:2], rect[2], rect[3],
                 facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=0.8, alpha=0.7, zorder=2))

# ── Extraction flap (prep box end face) — hinged at top ────────────────────
prep_end_x = BOX_D + PREP_D - WALL_T
ax.add_patch(mpatches.Rectangle((prep_end_x, 0), WALL_T, BOX_H,
             facecolor=C_FLAP, edgecolor=C_OUT, linewidth=1.0, alpha=0.3, zorder=2))
# Hinge indicator at top
hinge_flap_y = BOX_H - WALL_T
ax.add_patch(mpatches.Rectangle((prep_end_x - 2, hinge_flap_y - 3), WALL_T + 4, 6,
             facecolor=C_HINGE, edgecolor=C_OUT, linewidth=0.5, alpha=0.8, zorder=8))

# Extraction flap motion arc — swings outward from top hinge
flap_arc_r = BOX_H * 0.3
flap_hinge_x = prep_end_x + WALL_T / 2
flap_arc = Arc((flap_hinge_x, hinge_flap_y), flap_arc_r * 2, flap_arc_r * 2,
               angle=0, theta1=-90, theta2=-5,
               color=C_FLAP, lw=1.5, ls="--", zorder=9)
ax.add_patch(flap_arc)
# Arrow at the horizontal end (flap open position)
ax.annotate("", xy=(flap_hinge_x + flap_arc_r, hinge_flap_y),
            xytext=(flap_hinge_x + flap_arc_r - 12, hinge_flap_y + 10),
            arrowprops=dict(arrowstyle="->", color=C_FLAP, lw=1.5), zorder=9)

# ── Photo tray (Paterson 12×16") inside prep box ──────────────────────────
ax.add_patch(mpatches.Rectangle((tray_x, WALL_T), TRAY_EXT_D, TRAY_RIM,
             facecolor=C_TRAY, edgecolor=C_OUT, linewidth=0.8, alpha=0.3, zorder=3))
ax.plot([tray_x, tray_x], [WALL_T, WALL_T + TRAY_RIM], color=C_OUT, lw=1.2, zorder=4)
ax.plot([tray_x_far, tray_x_far], [WALL_T, WALL_T + TRAY_RIM], color=C_OUT, lw=1.2, zorder=4)
ax.text(tray_x + TRAY_EXT_D / 2, WALL_T + TRAY_RIM / 2, "TRAY", ha="center",
        va="center", fontsize=FS_SM - 1, color=C_TRAY, fontweight="bold", alpha=0.7)

# ── Backing board — UPRIGHT at tray near rim (in camera box, solid) ────────
board_x = hinge_x - BACKING  # board inside camera box (upright from near rim)
board_bottom = hinge_y
board_top = hinge_y + BOARD_H

# Board rectangle (thin vertical, 5mm thick)
ax.add_patch(mpatches.Rectangle((board_x, board_bottom), BACKING, BOARD_H,
             facecolor=C_BACKING, edgecolor=C_OUT, linewidth=1.0, zorder=5))

# Paper on the camera side of the board
paper_y1 = board_bottom + MARGIN
paper_y2 = board_top - MARGIN
ax.plot([board_x, board_x], [paper_y1, paper_y2],
        color=C_CL, lw=3.0, solid_capstyle="butt", zorder=6)

# Pinhole Y — centered on the board (film plane)
ph_y = HINGE_Y_ABS + BOARD_H / 2

# Arm sleeves on prep box end face
SLEEVE_PROJ = 80
sleeve_wall_x = prep_end_x  # end face inner surface
arm_endface_y = BOX_H / 2   # centered on the end face
arm_top_s = arm_endface_y + SLEEVE_D / 2
arm_bot_s = arm_endface_y - SLEEVE_D / 2
# Hidden-line circle on end face (both armholes project to same height in side view)
ax.add_patch(plt.Circle((sleeve_wall_x + WALL_T / 2, arm_endface_y), SLEEVE_D / 2,
             facecolor="none", edgecolor=C_SLEEVE, linewidth=0.8,
             linestyle="--", alpha=0.6, zorder=3))
# Sleeves projecting outward (rightward, beyond the box)
ax.add_patch(mpatches.Rectangle((sleeve_wall_x + WALL_T, arm_bot_s),
             SLEEVE_PROJ, SLEEVE_D,
             facecolor=C_SLEEVE, edgecolor="none", alpha=0.08, zorder=1))
ax.plot([sleeve_wall_x + WALL_T, sleeve_wall_x + WALL_T + SLEEVE_PROJ],
        [arm_top_s, arm_top_s], color=C_SLEEVE, lw=1.0, ls="--", zorder=3)
ax.plot([sleeve_wall_x + WALL_T, sleeve_wall_x + WALL_T + SLEEVE_PROJ],
        [arm_bot_s, arm_bot_s], color=C_SLEEVE, lw=1.0, ls="--", zorder=3)
ax.plot([sleeve_wall_x + WALL_T + SLEEVE_PROJ, sleeve_wall_x + WALL_T + SLEEVE_PROJ],
        [arm_bot_s + 8, arm_top_s - 8],
        color=C_PINHOLE, lw=2.0, solid_capstyle="round", zorder=4)

# ── Backing board — FOLDED DOWN (dashed, extending over tray into prep) ───
ax.add_patch(mpatches.Rectangle((hinge_x, hinge_y - BACKING), BOARD_H, BACKING,
             facecolor=C_BACKING, edgecolor=C_OUT, linewidth=0.8,
             linestyle="--", alpha=0.35, zorder=3))

# ── Hinge detail (duct tape at tray near rim) ─────────────────────────────
hinge_w = 16
ax.add_patch(mpatches.Rectangle((hinge_x - hinge_w / 2, hinge_y - BACKING - 2),
             hinge_w, BACKING + 4,
             facecolor=C_HINGE, edgecolor=C_OUT, linewidth=0.5, alpha=0.8, zorder=8))

# ── Motion arc (board folds down from upright to horizontal over tray) ────
arc_r = BOARD_H * 0.25
arc = Arc((hinge_x, hinge_y), arc_r * 2, arc_r * 2,
          angle=0, theta1=-5, theta2=90,
          color=C_MOTION, lw=1.5, ls="--", zorder=7)
ax.add_patch(arc)
ax.annotate("", xy=(hinge_x + arc_r, hinge_y),
            xytext=(hinge_x + arc_r - 12, hinge_y + 10),
            arrowprops=dict(arrowstyle="->", color=C_MOTION, lw=1.5), zorder=7)

# ── Pinhole (on left wall) ──────────────────────────────────────────────────
ax.add_patch(plt.Circle((WALL_T / 2, ph_y), 6,
             facecolor=C_PINHOLE, edgecolor=C_OUT, linewidth=0.8, zorder=5))
ax.plot([WALL_T / 2 - 12, WALL_T / 2 + 12], [ph_y, ph_y],
        color=C_PINHOLE, lw=0.8, zorder=6)
ax.plot([WALL_T / 2, WALL_T / 2], [ph_y - 12, ph_y + 12],
        color=C_PINHOLE, lw=0.8, zorder=6)

# Aluminum plate behind pinhole
ax.add_patch(mpatches.Rectangle((WALL_T, ph_y - 38), 2, 76,
             facecolor=C_ALUM, edgecolor=C_OUT, linewidth=0.6, zorder=4))

# ── Light cone ──────────────────────────────────────────────────────────────
cone_verts = [
    (WALL_T, ph_y),
    (board_x, paper_y2),
    (board_x, paper_y1),
]
ax.add_patch(mpatches.Polygon(cone_verts, closed=True,
             facecolor=C_CONE, edgecolor="none", alpha=0.2, zorder=1))
ax.plot([WALL_T, board_x], [ph_y, paper_y2],
        color=C_CONE_LN, lw=0.8, ls="--", dashes=(6, 4), alpha=0.7, zorder=2)
ax.plot([WALL_T, board_x], [ph_y, paper_y1],
        color=C_CONE_LN, lw=0.8, ls="--", dashes=(6, 4), alpha=0.7, zorder=2)

# Optical axis
ax.plot([0, board_x], [ph_y, ph_y],
        color=C_CL, lw=0.7, ls="--", dashes=(8, 4), zorder=2)

# Shutter flap (outside left wall)
ax.add_patch(mpatches.Rectangle((-30, ph_y - 50), 28, 100,
             facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=3))

# ── Box labels ──────────────────────────────────────────────────────────────
ax.text(BOX_D / 2, BOX_H - WALL_T - 15, "CAMERA BOX", ha="center", va="top",
        fontsize=FS_MD, fontweight="bold", color=C_DIM, alpha=0.5)
ax.text(BOX_D + PREP_D / 2, BOX_H - WALL_T - 15, "PREP BOX", ha="center", va="top",
        fontsize=FS_MD, fontweight="bold", color=C_DIM, alpha=0.5)

# ── Cross-section dimensions ────────────────────────────────────────────────
draw_dim_h(ax, 0, BOX_D, -55, f"Camera box  {BOX_D} mm  (18\"  =  focal length)", offset=15)
draw_dim_h(ax, BOX_D, TOTAL_D, -55, f"Prep box  {PREP_D} mm  (18\")", offset=15)
draw_dim_h(ax, 0, TOTAL_D, -100, f"Total length  {TOTAL_D} mm  (36\")", offset=15)
draw_dim_v(ax, -50, 0, BOX_H, f"{BOX_H} mm\n(16\")", offset=15)
draw_dim_v(ax, BOX_D + 10, paper_y1, paper_y2,
           f"Image  {int(paper_y2 - paper_y1)} mm", offset=12, color=C_CL, right=True)
draw_dim_h(ax, tray_x, tray_x_far, BOX_H + 30,
           f"Tray  {TRAY_EXT_D} mm\n(12×16\" Paterson)", offset=10, fs=FS_SM - 0.5)

# ── Cross-section leaders ───────────────────────────────────────────────────
leader(ax, WALL_T / 2, ph_y, -PAD + 10, ph_y + 100,
       f"Pinhole  Ø{PH_D} mm\nf/{F_NO}", ha="right", color=C_PINHOLE)
leader(ax, -16, ph_y, -PAD + 10, ph_y - 60,
       "Shutter flap", ha="right")
leader(ax, sleeve_wall_x + WALL_T + SLEEVE_PROJ / 2, arm_top_s + 3,
       TOTAL_D + SLEEVE_PROJ + 30, arm_top_s + 50,
       f"Arm sleeves (×2) Ø{SLEEVE_D} mm\n(on prep box end face)", ha="left", fs=FS_SM - 0.5)
leader(ax, board_x, (paper_y1 + paper_y2) / 2,
       board_x - 80, ph_y + 90,
       "Paper on board\n(film plane)", ha="center", color=C_CL)
board_fold_mid = hinge_x + BOARD_H / 2
leader(ax, board_fold_mid, hinge_y - 3,
       board_fold_mid, hinge_y + 80,
       "Board folded down\n(over tray into prep space —\nmount paper on this surface)", ha="center", color=C_MOTION)
leader(ax, hinge_x, hinge_y - BACKING, hinge_x + 30, hinge_y - 50,
       "Duct tape hinge\n(at tray near rim)", ha="left", color=C_HINGE)
leader(ax, tray_x + TRAY_EXT_D / 2 + 60, WALL_T + TRAY_RIM - 20,
       tray_x + TRAY_EXT_D / 2 + 80, WALL_T + TRAY_RIM + 30,
       f"Photo tray\n12×16\" (Paterson PTP326)", ha="center", color=C_TRAY)
ax.text(BOX_D / 2, ph_y + 10, "Light cone",
        ha="center", color=C_CONE_LN)
leader(ax, prep_end_x + WALL_T / 2, BOX_H / 2,
       TOTAL_D + 60, BOX_H / 2 + 30,
       "Extraction flap\n(opens after exposure)", ha="left", color=C_FLAP, fs=FS_SM - 0.5)
leader(ax, prep_end_x + WALL_T / 2, hinge_flap_y,
       TOTAL_D + 60, hinge_flap_y + 40,
       "Gaffer tape hinge", ha="left", color=C_HINGE, fs=FS_SM - 0.5)

# View title
ax.text((TOTAL_D + board_fold_end) / 2, BOX_H + 100, "SIDE CROSS-SECTION",
        ha="center", va="bottom", fontsize=FS_MD + 2, fontweight="bold", color=C_OUT)
ax.text((TOTAL_D + board_fold_end) / 2, BOX_H + 82,
        "Two-box design — board hinged at tray near rim — arm sleeves + extraction flap on end face",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, style="italic")


# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM-LEFT: Prep box end face — armholes + sleeve attachment
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_board
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

# End face is BOX_W × BOX_H (18×16")
EF_W = BOX_W
EF_H = BOX_H
FPAD = 100
ax.set_xlim(-FPAD, EF_W + FPAD * 1.5)
ax.set_ylim(-FPAD, EF_H + FPAD)

# End face outline (extraction flap)
ax.add_patch(mpatches.Rectangle((0, 0), EF_W, EF_H,
             facecolor=C_FLAP, edgecolor=C_OUT, linewidth=1.5, alpha=0.15, zorder=1))

# Armholes centered on the face, spaced horizontally
arm_cx1 = EF_W / 2 - SLEEVE_SPACING / 2
arm_cx2 = EF_W / 2 + SLEEVE_SPACING / 2
arm_cy = EF_H / 2

for cx in [arm_cx1, arm_cx2]:
    # Armhole
    ax.add_patch(plt.Circle((cx, arm_cy), SLEEVE_D / 2,
                 facecolor=C_SLEEVE, edgecolor=C_OUT, linewidth=1.2, alpha=0.8, zorder=4))
    # Gaffer tape seal ring (sleeve attachment)
    ax.add_patch(mpatches.Annulus((cx, arm_cy), SLEEVE_D / 2 + 12, 10,
                 facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.5, alpha=0.4, zorder=3))

# Hinge edge indicator (top edge — extraction flap hinged at top)
ax.add_patch(mpatches.Rectangle((0, EF_H - 4), EF_W, 8,
             facecolor=C_HINGE, edgecolor=C_OUT, linewidth=0.6, alpha=0.5, zorder=5))
ax.text(EF_W / 2, EF_H + 12, "HINGE EDGE (extraction flap — opens upward)",
        ha="center", va="bottom", fontsize=FS_SM - 1, color=C_HINGE, fontweight="bold")

# Dimensions
draw_dim_h(ax, 0, EF_W, -60, f"End face width  {EF_W} mm  (18\")", offset=12)
draw_dim_v(ax, EF_W + 50, 0, EF_H, f"End face height\n{EF_H} mm  (16\")", offset=12, right=True)
draw_dim_h(ax, arm_cx1, arm_cx2, EF_H + 40,
           f"Armhole spacing  {SLEEVE_SPACING} mm", offset=10, fs=FS_SM - 0.5)
draw_dim_h(ax, arm_cx1 - SLEEVE_D / 2, arm_cx1 + SLEEVE_D / 2,
           arm_cy - SLEEVE_D / 2 - 45,
           f"Ø{SLEEVE_D} mm (4\")", offset=10, fs=FS_SM - 0.5)

# Leaders
leader(ax, arm_cx1, arm_cy, -60, arm_cy + 50,
       f"Armhole Ø{SLEEVE_D} mm\n(fabric sleeve\n+ elastic at wrist)", ha="right", fs=FS_SM - 0.5)
leader(ax, arm_cx1 + SLEEVE_D / 2 + 5, arm_cy, EF_W + 80, arm_cy +270,
       "Gaffer tape seal", ha="left", fs=FS_SM - 0.5)

# View title
ax.text(EF_W / 2, EF_H + 85, "END FACE — OPERATOR SIDE",
        ha="center", va="bottom", fontsize=FS_MD + 1, fontweight="bold", color=C_OUT)
ax.text(EF_W / 2, EF_H + 70,
        "Extraction flap with armholes — sleeves project toward operator",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, style="italic")


# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM: Armhole detail — cross-section through sleeve attachment
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_armdt
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

# This is an enlarged cross-section through the center of one armhole,
# showing how the fabric sleeve attaches to the cardboard end face.
#
# Vertical cross-section (looking from inside the box outward):
#   cardboard wall | fabric fold-back | gaffer tape seal | sleeve tube
#
# Scale: approximately 1:1 for clarity

DPAD = 30
# Drawing coordinates — wall runs vertically, sleeve extends to the right
ax.set_xlim(-90, 280)
ax.set_ylim(-100, 140)

# ── Cardboard wall cross-section ─────────────────────────────────────────
wall_x = 0           # inner surface of wall
wall_thick = WALL_T   # 4 mm
hole_r = SLEEVE_D / 2  # 51 mm radius
wall_top = hole_r + 40   # cardboard above the hole
wall_bot = -(hole_r + 40)  # cardboard below the hole

# Upper wall section (above hole)
ax.add_patch(mpatches.Rectangle((wall_x, hole_r), wall_thick, wall_top - hole_r,
             facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=1.0, zorder=3))
# Lower wall section (below hole)
ax.add_patch(mpatches.Rectangle((wall_x, wall_bot), wall_thick, hole_r + wall_bot * -1,
             facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=1.0, zorder=3))

# ── Hole opening (the gap in the wall) ───────────────────────────────────
# Just the edges of the cut hole
ax.plot([wall_x, wall_x + wall_thick], [hole_r, hole_r],
        color=C_OUT, lw=0.8, zorder=4)
ax.plot([wall_x, wall_x + wall_thick], [-hole_r, -hole_r],
        color=C_OUT, lw=0.8, zorder=4)

# ── Fabric sleeve tube ──────────────────────────────────────────────────
sleeve_len = 200     # mm shown (full sleeve is ~450mm)
fabric_thick = 2     # mm — fabric wall thickness (schematic)

# Upper fabric wall
ax.add_patch(mpatches.Rectangle((wall_x + wall_thick, hole_r - fabric_thick),
             sleeve_len, fabric_thick,
             facecolor=C_SLEEVE, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=3))
# Lower fabric wall
ax.add_patch(mpatches.Rectangle((wall_x + wall_thick, -hole_r),
             sleeve_len, fabric_thick,
             facecolor=C_SLEEVE, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=3))
# Sleeve interior (light fill)
ax.add_patch(mpatches.Rectangle((wall_x + wall_thick, -hole_r + fabric_thick),
             sleeve_len, SLEEVE_D - 2 * fabric_thick,
             facecolor=C_SLEEVE, edgecolor="none", alpha=0.05, zorder=1))

# ── Fabric fold-back over cardboard edge ─────────────────────────────────
# The fabric wraps from outside, over the cut edge, and folds back ~50mm
# onto the inside surface of the wall
fold_back = 50  # mm fold-back length on inside

# Upper fold-back: fabric bends over the top edge of the hole
# Outside to edge
ax.plot([wall_x + wall_thick, wall_x + wall_thick], [hole_r - fabric_thick, hole_r],
        color=C_OUT, lw=0.6, zorder=4)
# Over the edge (short curve shown as line)
ax.plot([wall_x + wall_thick, wall_x], [hole_r, hole_r],
        color=C_SLEEVE, lw=2.0, zorder=5)
# Fold-back strip on inside (runs inward = leftward from the hole edge)
ax.add_patch(mpatches.Rectangle((-fold_back, hole_r), fold_back, fabric_thick,
             facecolor=C_SLEEVE, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=3))

# Lower fold-back
ax.plot([wall_x + wall_thick, wall_x + wall_thick], [-hole_r, -hole_r + fabric_thick],
        color=C_OUT, lw=0.6, zorder=4)
ax.plot([wall_x + wall_thick, wall_x], [-hole_r, -hole_r],
        color=C_SLEEVE, lw=2.0, zorder=5)
ax.add_patch(mpatches.Rectangle((-fold_back, -hole_r - fabric_thick), fold_back, fabric_thick,
             facecolor=C_SLEEVE, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=3))

# ── Gaffer tape seal (wraps over fold-back on inside surface) ────────────
tape_w = 50   # mm — 2" gaffer tape
tape_t = 1.5  # mm — tape thickness (schematic)

# Upper tape — on inside surface, covering the fold-back
ax.add_patch(mpatches.Rectangle((-fold_back, hole_r + fabric_thick),
             fold_back + 10, tape_t,
             facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.5, alpha=0.6, zorder=4))
# Tape also covers the outside fold
ax.add_patch(mpatches.Rectangle((wall_x + wall_thick, hole_r),
             tape_w * 0.6, tape_t,
             facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.5, alpha=0.6, zorder=4))

# Lower tape
ax.add_patch(mpatches.Rectangle((-fold_back, -hole_r - fabric_thick - tape_t),
             fold_back + 10, tape_t,
             facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.5, alpha=0.6, zorder=4))
ax.add_patch(mpatches.Rectangle((wall_x + wall_thick, -hole_r - tape_t),
             tape_w * 0.6, tape_t,
             facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.5, alpha=0.6, zorder=4))

# ── Elastic / rubber band at wrist end ───────────────────────────────────
elastic_x = wall_x + wall_thick + sleeve_len - 10
# Cinch marks (sleeve narrows at wrist)
cinch = 12
ax.plot([elastic_x, elastic_x], [-hole_r + cinch, hole_r - cinch],
        color=C_PINHOLE, lw=2.5, solid_capstyle="round", zorder=5)
# Small arrows showing cinch direction
for sign in [1, -1]:
    y_arr = sign * (hole_r - cinch)
    ax.annotate("", xy=(elastic_x, y_arr),
                xytext=(elastic_x, y_arr + sign * 10),
                arrowprops=dict(arrowstyle="->", color=C_PINHOLE, lw=1.0), zorder=5)

# ── Dimensions ───────────────────────────────────────────────────────────
draw_dim_v(ax, -90, -hole_r, hole_r,
           f"Ø{SLEEVE_D} mm\n(4\")", offset=10, fs=FS_SM - 0.5)
draw_dim_h(ax, -fold_back, 0, wall_top + 30,
           f"Fold-back\n{fold_back} mm", offset=8, fs=FS_SM - 1)
draw_dim_h(ax, 0, wall_thick, wall_top + 5,
           f"{wall_thick} mm\nwall", offset=8, fs=FS_SM - 1)
draw_dim_h(ax, wall_x + wall_thick, elastic_x, wall_bot - 25,
           f"Sleeve ~450 mm (18\")\n(shown truncated)", offset=8, fs=FS_SM - 1)

# ── Leaders ──────────────────────────────────────────────────────────────
leader(ax, wall_x + wall_thick / 2, wall_top - 5, -60, wall_top + 55,
       "Cardboard wall\n(end face)", ha="right", fs=FS_SM - 0.5)
leader(ax, -fold_back / 2, hole_r + fabric_thick + tape_t + 2, -60, hole_r + 45,
       "Gaffer tape\nseal (inside)", ha="right", fs=FS_SM - 0.5, color=C_TAPE)
leader(ax, -fold_back / 2, hole_r + 1, -60, hole_r + 25,
       "Fabric fold-back", ha="right", fs=FS_SM - 0.5, color=C_SLEEVE)
leader(ax, wall_x + wall_thick + sleeve_len / 3, hole_r - 1,
       wall_x + wall_thick + sleeve_len / 3, hole_r + 30,
       "Black fabric sleeve\n(cotton knit)", ha="center", fs=FS_SM - 0.5, color=C_SLEEVE)
leader(ax, elastic_x, hole_r - cinch + 2, elastic_x + 40, hole_r + 20,
       "Rubber band\n(cinch at wrist)", ha="left", fs=FS_SM - 0.5, color=C_PINHOLE)

# ── Section direction labels ─────────────────────────────────────────────
ax.text(-fold_back - 15, 0, "INSIDE\nBOX", ha="right", va="center",
        fontsize=FS_SM - 1, color=C_DIM, fontweight="bold", alpha=0.5)
ax.text(wall_x + wall_thick + sleeve_len + 15, 0, "OUTSIDE\n(OPERATOR)",
        ha="left", va="center",
        fontsize=FS_SM - 1, color=C_DIM, fontweight="bold", alpha=0.5)

# ── Center line through hole ─────────────────────────────────────────────
ax.plot([-fold_back - 5, elastic_x + 20], [0, 0],
        color=C_CL, lw=0.6, ls="--", dashes=(6, 4), alpha=0.5, zorder=1)

# View title
ax.text(wall_x + wall_thick + sleeve_len / 2 - 20, wall_top + 65,
        "ARMHOLE DETAIL", ha="center", va="bottom",
        fontsize=FS_MD + 1, fontweight="bold", color=C_OUT)
ax.text(wall_x + wall_thick + sleeve_len / 2 - 20, wall_top + 50,
        "Cross-section through sleeve attachment — scale ~2:1",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, style="italic")


# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM: Plan view — both boxes from above
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_planv
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

PPAD = PAD   # match cross-section padding for vertical alignment
ax.set_xlim(-PPAD - 40, max(board_fold_end + PPAD, flap_open_end + PPAD))
ax.set_ylim(-PPAD, BOX_W + PPAD)

# Camera box (left) — depth × width
ax.add_patch(mpatches.Rectangle((0, 0), BOX_D, BOX_W,
             facecolor=C_BOX, edgecolor=C_OUT, linewidth=1.5, alpha=0.25, zorder=1))

for rect in [
    (0, 0, WALL_T, BOX_W),                 # left (pinhole face)
    (0, 0, BOX_D, WALL_T),                 # bottom
    (0, BOX_W - WALL_T, BOX_D, WALL_T),   # top
]:
    ax.add_patch(mpatches.Rectangle(rect[:2], rect[2], rect[3],
                 facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=0.8, zorder=2))

# Prep box (right)
ax.add_patch(mpatches.Rectangle((BOX_D, 0), PREP_D, BOX_W,
             facecolor=C_BOX, edgecolor=C_OUT, linewidth=1.5, alpha=0.15, zorder=1))

for rect in [
    (BOX_D, 0, PREP_D, WALL_T),                     # bottom
    (BOX_D, BOX_W - WALL_T, PREP_D, WALL_T),       # top
]:
    ax.add_patch(mpatches.Rectangle(rect[:2], rect[2], rect[3],
                 facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=0.8, alpha=0.7, zorder=2))

# Extraction flap (end face — solid wall, hinged at top)
ax.add_patch(mpatches.Rectangle((TOTAL_D - WALL_T, 0), WALL_T, BOX_W,
             facecolor=C_FLAP, edgecolor=C_OUT, linewidth=1.0, alpha=0.25, zorder=2))
# Hinge line at top of end face (in plan view, "top" = the far edge in Y)
ax.plot([TOTAL_D - WALL_T, TOTAL_D], [BOX_W - WALL_T, BOX_W - WALL_T],
        color=C_HINGE, lw=2.0, zorder=4)

# Photo tray in plan view — inside prep box, against camera-box wall
tray_plan_x = BOX_D + WALL_T
tray_plan_y = BOX_W / 2 - TRAY_EXT_W / 2
ax.add_patch(mpatches.Rectangle((tray_plan_x, tray_plan_y), TRAY_EXT_D, TRAY_EXT_W,
             facecolor=C_TRAY, edgecolor=C_OUT, linewidth=0.8, alpha=0.3, zorder=3))

# Board upright at tray near rim (inside camera box, shown as line in plan view)
board_plan_x = tray_plan_x  # at the near rim of the tray
ax.plot([board_plan_x, board_plan_x], [BOX_W / 2 - BOARD_W / 2, BOX_W / 2 + BOARD_W / 2],
        color=C_OUT, lw=2.5, solid_capstyle="butt", zorder=4)

# Armholes on end face (dashed circles at the extraction flap wall)
arm_plan_cy1 = BOX_W / 2 - SLEEVE_SPACING / 2
arm_plan_cy2 = BOX_W / 2 + SLEEVE_SPACING / 2
endface_plan_x = TOTAL_D - WALL_T / 2
for cy in [arm_plan_cy1, arm_plan_cy2]:
    ax.add_patch(plt.Circle((endface_plan_x, cy), SLEEVE_D / 2,
                 facecolor="none", edgecolor=C_SLEEVE, linewidth=0.8,
                 linestyle="--", alpha=0.6, zorder=5))

# Board folded down from near rim (dashed, extending over tray into prep space)
ax.add_patch(mpatches.Rectangle((board_plan_x, BOX_W / 2 - BOARD_W / 2),
             BOARD_H, BOARD_W,
             facecolor=C_BACKING, edgecolor=C_OUT, linewidth=0.6,
             linestyle="--", alpha=0.12, zorder=2))

# Pinhole marker on left wall
ax.add_patch(plt.Circle((WALL_T / 2, BOX_W / 2), 5,
             facecolor=C_PINHOLE, edgecolor=C_OUT, linewidth=0.8, zorder=5))

# Optical axis
ax.plot([0, board_plan_x], [BOX_W / 2, BOX_W / 2],
        color=C_CL, lw=0.7, ls="--", dashes=(8, 4), zorder=2)

# Box labels
ax.text(BOX_D / 2, BOX_W / 2 + 20, "CAMERA", ha="center", va="center",
        fontsize=FS_SM, fontweight="bold", color=C_DIM, alpha=0.4)
ax.text((board_plan_x + TOTAL_D) / 2, BOX_W / 2 + 20, "PREP", ha="center", va="center",
        fontsize=FS_SM, fontweight="bold", color=C_DIM, alpha=0.4)

# Face labels
ax.text(WALL_T / 2, BOX_W + 20, "PINHOLE\nFACE", ha="center", va="bottom",
        fontsize=FS_SM - 1, color=C_PINHOLE, fontweight="bold")
ax.text(TOTAL_D - WALL_T / 2, BOX_W + 20, "EXTRACTION\nFLAP", ha="center", va="bottom",
        fontsize=FS_SM - 1, color=C_FLAP, fontweight="bold")

# Dimensions
draw_dim_h(ax, 0, TOTAL_D, BOX_W + 45, f"Total  {TOTAL_D} mm  (36\")", offset=10, fs=FS_SM - 0.5)
draw_dim_v(ax, board_fold_end + 40, 0, BOX_W,
           f"{BOX_W} mm", offset=10, right=True, fs=FS_SM - 0.5)
draw_dim_h(ax, 0, BOX_D, -50, f"Camera  {BOX_D} mm", offset=8, fs=FS_SM - 0.5)
draw_dim_h(ax, BOX_D, TOTAL_D, -50, f"Prep  {PREP_D} mm", offset=8, fs=FS_SM - 0.5)

# Leaders
leader(ax, board_plan_x, BOX_W / 2 + 90, board_plan_x - 50, BOX_W - 90,
       "Board (upright)\nfilm plane", ha="right", color=C_MOTION, fs=FS_SM - 0.5)
leader(ax, tray_plan_x + TRAY_EXT_D / 2 + 130, tray_plan_y + TRAY_EXT_W - 50,
       tray_plan_x + TRAY_EXT_D / 2 + 150, BOX_W + 30,
       "Photo tray", ha="center", color=C_TRAY, fs=FS_SM - 0.5)
leader(ax, board_plan_x + BOARD_H / 2, BOX_W / 2 + BOARD_W / 2,
       board_fold_end - 150, BOX_W / 2 + BOARD_W / 2 + 35,
       "Board folded\n(prep position)", ha="left", color=C_MOTION, fs=FS_SM - 0.5)

# View title
ax.text((TOTAL_D + board_fold_end) / 2, BOX_W + 80, "PLAN VIEW — LOOKING DOWN",
        ha="center", va="bottom", fontsize=FS_MD + 1, fontweight="bold", color=C_OUT)
ax.text((TOTAL_D + board_fold_end) / 2, BOX_W + 65,
        "Two-box arrangement — board at tray near rim, arm sleeves + extraction flap on end face",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, style="italic")


# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM ROW: Specification (left) + Workflow (right) — full width
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_asm
ax.set_facecolor(BG)
ax.axis("off")
ax.set_xlim(0, 1000)
ax.set_ylim(0, 160)

C_SPEC_BG = "#E8EEF4"   # cool blue-gray for specification
C_WORK_BG = "#F4EDE4"   # warm tan for workflow

BOX_W_SPEC = 340
BOX_W_WORK = 380
BOX_GAP = 40
spec_x = 10
work_x = spec_x + BOX_W_SPEC + BOX_GAP

# ── Specification table (left) ─────────────────────────────────────────────
ax.add_patch(mpatches.FancyBboxPatch((spec_x, 10), BOX_W_SPEC, 140,
             boxstyle="round,pad=6", facecolor=C_SPEC_BG, edgecolor=C_OUT,
             linewidth=0.8, zorder=1))

ax.text(spec_x + BOX_W_SPEC / 2, 145, "SPECIFICATION", ha="center", va="top",
        fontsize=FS_MD, fontweight="bold", color=C_OUT)
ax.plot([spec_x + 20, spec_x + BOX_W_SPEC - 20], [137, 137], color=C_OUT, lw=0.6)

specs = [
    f"Focal length:  {FOCAL} mm (18\")",
    f"Pinhole:  Ø{PH_D} mm (1/32\" drill bit)",
    f"f-number:  f/{F_NO}",
    f"Film plane:  {FP_W} × {int(paper_y2 - paper_y1)} mm",
    f"Exposure:  ~10 min (full sun)",
    "Substrate:  Watercolor paper 300 gsm",
    "Process:  Ware New Cyanotype",
    f"Tray:  Paterson 12×16\" (PTP326)",
]
y = 128
for line in specs:
    ax.text(spec_x + 20, y, line, ha="left", va="top",
            fontsize=FS_SM, color=C_DIM)
    y -= 14

# ── Workflow (right) ──────────────────────────────────────────────────────
ax.add_patch(mpatches.FancyBboxPatch((work_x, 10), BOX_W_WORK, 140,
             boxstyle="round,pad=6", facecolor=C_WORK_BG, edgecolor=C_OUT,
             linewidth=0.8, zorder=1))

ax.text(work_x + BOX_W_WORK / 2, 145, "WORKFLOW", ha="center", va="top",
        fontsize=FS_MD, fontweight="bold", color=C_OUT)
ax.plot([work_x + 20, work_x + BOX_W_WORK - 20], [137, 137], color=C_OUT, lw=0.6)

steps = [
    "1.  Mix chemistry (daylight OK).",
    "2.  Coat paper in tray through arm sleeves (safelight).",
    "3.  Tack-dry in sealed prep box.",
    "4.  Fold board down, mount paper, fold up (safelight).",
    "5.  Expose (sunlight through pinhole).",
    "6.  Open extraction flap (daylight safe) — remove print.",
    "7.  Wash in photo trays (daylight).",
]

y = 128
for step in steps:
    ax.text(work_x + 20, y, step, ha="left", va="top",
            fontsize=FS_SM, color=C_DIM, linespacing=1.2)
    y -= 14


# ── Title block (full-figure overlay) ────────────────────────────────────────
ax_tb = fig.add_axes([0, 0, 1, 1], facecolor="none")
ax_tb.axis("off")
title_block(ax_tb, "SHEET 1 OF 1",
            drawing_title="TBS-002 MINI-TBS PROOF OF CONCEPT",
            subtitle="Two-box camera — board at tray near rim, arm sleeves + extraction flap on end face",
            scale_note="Approx 1:4 (views) / NTS (detail)",
            doc_id="TBS-002 · Mini-TBS")

# ── Save ─────────────────────────────────────────────────────────────────────
out = f"{DIAGRAMS_DIR}/mini-tbs-sheet1.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(f"Saved: {out}")
