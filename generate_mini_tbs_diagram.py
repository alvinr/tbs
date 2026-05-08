#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_mini_tbs_diagram.py

Mini-TBS proof-of-concept pinhole camera — engineering drawing.
Output: diagrams/mini-tbs-sheet1.png

Single sheet with four panels showing the two-box design:
  Top (full width):    Side cross-section — camera box + prep box, photo tray,
                       removable backing board (exposure + prep positions)
  Bottom-left:         Rear view — prep box end face (armholes + board slot)
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
# Internal: 12 × 16" (305 × 406 mm) — for prints up to 11 × 14"
# External: ~13.4 × 17.5 × 2.5" (~340 × 445 × 65 mm)
# Paper (16 × 18") overhangs slightly during brush coating — standard practice.
TRAY_EXT_D = 340   # mm — external depth in cross-section (~13.4")
TRAY_EXT_W = 445   # mm — external width (perpendicular to cross-section)
TRAY_RIM   = 65    # mm — rim height (~2.5")

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
# SINGLE SHEET — Four panels
# ══════════════════════════════════════════════════════════════════════════════

FIG_W = 26.0
FIG_H = 20.0
fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=150)
fig.patch.set_facecolor(BG)

gs = fig.add_gridspec(2, 3,
                      height_ratios=[1.1, 1],
                      width_ratios=[0.85, 1.15, 0.85],
                      hspace=0.22, wspace=0.16,
                      left=0.03, right=0.97, bottom=0.06, top=0.95)

ax_xsec  = fig.add_subplot(gs[0, :])    # side cross-section — full top row
ax_rear  = fig.add_subplot(gs[1, 0])    # rear view — prep box end face
ax_planv = fig.add_subplot(gs[1, 1])    # plan view — both boxes from above
ax_asm   = fig.add_subplot(gs[1, 2])    # assembly notes + spec table


# ══════════════════════════════════════════════════════════════════════════════
# TOP: Side cross-section — camera box + prep box with photo tray
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_xsec
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

# ── Layout constants ───────────────────────────────────────────────────────
# Board extends past prep box when folded down from tray rim.
board_height = BOX_H - 2 * WALL_T  # 398 mm — full camera interior height
tray_x = BOX_D + WALL_T            # tray near edge (camera side of prep box)
tray_x_far = tray_x + TRAY_EXT_D   # tray far rim — hinge point
hinge_y = WALL_T + TRAY_RIM        # hinge height (at tray rim level)
board_fold_end = tray_x_far + board_height  # board tip when folded horizontal

PAD = 120
ax.set_xlim(-PAD - 40, board_fold_end + PAD)
ax.set_ylim(-PAD - 30, BOX_H + PAD + 20)

# ── Camera box (left) ───────────────────────────────────────────────────────
ax.add_patch(mpatches.Rectangle((0, 0), BOX_D, BOX_H,
             facecolor=C_BOX, edgecolor=C_OUT, linewidth=1.5, alpha=0.25, zorder=1))

# Camera box walls
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

# Prep box walls
for rect in [
    (BOX_D + PREP_D - WALL_T, 0, WALL_T, BOX_H),  # far right wall (end face)
    (BOX_D, 0, PREP_D, WALL_T),                     # floor
    (BOX_D, BOX_H - WALL_T, PREP_D, WALL_T),       # ceiling
]:
    ax.add_patch(mpatches.Rectangle(rect[:2], rect[2], rect[3],
                 facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=0.8, alpha=0.7, zorder=2))

# Board slot in prep box end face (bottom portion, for board to extend through)
slot_y = WALL_T
slot_h = BACKING + 6  # slot height — board thickness + clearance
prep_end_x = BOX_D + PREP_D - WALL_T
ax.add_patch(mpatches.Rectangle((prep_end_x, slot_y), WALL_T, slot_h,
             facecolor=BG, edgecolor=C_OUT, linewidth=0.6, zorder=3))

# ── Photo tray (Paterson 12×16") inside prep box ──────────────────────────
ax.add_patch(mpatches.Rectangle((tray_x, WALL_T), TRAY_EXT_D, TRAY_RIM,
             facecolor=C_TRAY, edgecolor=C_OUT, linewidth=0.8, alpha=0.3, zorder=3))
# Tray rims (left and right walls)
ax.plot([tray_x, tray_x], [WALL_T, WALL_T + TRAY_RIM], color=C_OUT, lw=1.2, zorder=4)
ax.plot([tray_x_far, tray_x_far], [WALL_T, WALL_T + TRAY_RIM], color=C_OUT, lw=1.2, zorder=4)
# Tray label
ax.text(tray_x + TRAY_EXT_D / 2, WALL_T + TRAY_RIM / 2, "TRAY", ha="center",
        va="center", fontsize=FS_SM - 1, color=C_TRAY, fontweight="bold", alpha=0.7)

# ── Backing board — EXPOSURE POSITION (inside camera box, solid) ───────────
board_x_cam = BOX_D - BACKING  # board against the junction, inside camera box
board_bottom = WALL_T
board_top = BOX_H - WALL_T

ax.add_patch(mpatches.Rectangle((board_x_cam, board_bottom), BACKING, board_height,
             facecolor=C_BACKING, edgecolor=C_OUT, linewidth=1.0, zorder=5))
# Paper on the camera side of the board
paper_y1 = board_bottom + MARGIN
paper_y2 = board_top - MARGIN
ax.plot([board_x_cam, board_x_cam], [paper_y1, paper_y2],
        color=C_CL, lw=3.0, solid_capstyle="butt", zorder=6)

# ── Backing board — PREP POSITION: folded down from tray rim (dashed) ──────
# Board lies horizontal at tray rim height, extending right through board slot
ax.add_patch(mpatches.Rectangle((tray_x_far, hinge_y - BACKING), board_height, BACKING,
             facecolor=C_BACKING, edgecolor=C_OUT, linewidth=0.8,
             linestyle="--", alpha=0.35, zorder=3))

# Portion of board outside the prep box (past end wall)
if board_fold_end > TOTAL_D:
    ax.add_patch(mpatches.Rectangle((TOTAL_D, hinge_y - BACKING),
                 board_fold_end - TOTAL_D, BACKING,
                 facecolor=C_BACKING, edgecolor=C_OUT, linewidth=0.8,
                 linestyle="--", alpha=0.2, zorder=3))

# ── Hinge detail (duct tape at tray far rim) ──────────────────────────────
hinge_w = 16
ax.add_patch(mpatches.Rectangle((tray_x_far - hinge_w / 2, hinge_y - BACKING - 2),
             hinge_w, BACKING + 4,
             facecolor=C_HINGE, edgecolor=C_OUT, linewidth=0.5, alpha=0.8, zorder=8))

# ── Motion arc (board fold from upright to horizontal at tray rim) ─────────
arc_r = board_height * 0.25
arc = Arc((tray_x_far, hinge_y), arc_r * 2, arc_r * 2,
          angle=0, theta1=-5, theta2=90,
          color=C_MOTION, lw=1.5, ls="--", zorder=7)
ax.add_patch(arc)
ax.annotate("", xy=(tray_x_far + arc_r, hinge_y),
            xytext=(tray_x_far + arc_r - 12, hinge_y + 10),
            arrowprops=dict(arrowstyle="->", color=C_MOTION, lw=1.5), zorder=7)

# ── Pinhole (on left wall) ──────────────────────────────────────────────────
ph_y = BOX_H / 2
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
    (board_x_cam, paper_y2),
    (board_x_cam, paper_y1),
]
ax.add_patch(mpatches.Polygon(cone_verts, closed=True,
             facecolor=C_CONE, edgecolor="none", alpha=0.2, zorder=1))
ax.plot([WALL_T, board_x_cam], [ph_y, paper_y2],
        color=C_CONE_LN, lw=0.8, ls="--", dashes=(6, 4), alpha=0.7, zorder=2)
ax.plot([WALL_T, board_x_cam], [ph_y, paper_y1],
        color=C_CONE_LN, lw=0.8, ls="--", dashes=(6, 4), alpha=0.7, zorder=2)

# Optical axis
ax.plot([0, BOX_D], [ph_y, ph_y],
        color=C_CL, lw=0.7, ls="--", dashes=(8, 4), zorder=2)

# Shutter flap (outside left wall)
ax.add_patch(mpatches.Rectangle((-30, ph_y - 50), 28, 100,
             facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=3))

# ── Armholes (hidden line on prep box end face) ───────────────────────────
# Two armholes side by side, centered vertically on the upper portion of the
# end face (above the board slot). In the side cross-section both overlap —
# shown as a single dashed hidden-line circle.
arm_y_center = (hinge_y + BOX_H - WALL_T) / 2 + 15  # centered in upper portion
prep_wall_x = BOX_D + PREP_D - WALL_T
prep_wall_x_out = BOX_D + PREP_D
SLEEVE_PROJ_XS = 80

ax.add_patch(plt.Circle((prep_wall_x + WALL_T / 2, arm_y_center), SLEEVE_D / 2,
             facecolor="none", edgecolor=C_SLEEVE, linewidth=0.8,
             linestyle="--", alpha=0.6, zorder=4))
# Sleeve projection (extending right)
arm_top = arm_y_center + SLEEVE_D / 2
arm_bot = arm_y_center - SLEEVE_D / 2
ax.add_patch(mpatches.Rectangle((prep_wall_x_out, arm_bot),
             SLEEVE_PROJ_XS, SLEEVE_D,
             facecolor=C_SLEEVE, edgecolor="none", alpha=0.08, zorder=1))
ax.plot([prep_wall_x_out, prep_wall_x_out + SLEEVE_PROJ_XS], [arm_top, arm_top],
        color=C_SLEEVE, lw=1.0, ls="--", zorder=3)
ax.plot([prep_wall_x_out, prep_wall_x_out + SLEEVE_PROJ_XS], [arm_bot, arm_bot],
        color=C_SLEEVE, lw=1.0, ls="--", zorder=3)
ax.plot([prep_wall_x_out + SLEEVE_PROJ_XS, prep_wall_x_out + SLEEVE_PROJ_XS],
        [arm_bot + 8, arm_top - 8],
        color=C_PINHOLE, lw=2.0, solid_capstyle="round", zorder=4)

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
draw_dim_v(ax, board_fold_end + 60, paper_y1, paper_y2,
           f"Image  {FP_H} mm", offset=12, color=C_CL, right=True)
draw_dim_h(ax, tray_x, tray_x_far, BOX_H + 30,
           f"Tray  {TRAY_EXT_D} mm\n(12×16\" Paterson)", offset=10, fs=FS_SM - 0.5)

# ── Cross-section leaders ───────────────────────────────────────────────────
leader(ax, WALL_T / 2, ph_y + 10, -PAD + 10, ph_y + 100,
       f"Pinhole  Ø{PH_D} mm\nf/{F_NO}", ha="right", color=C_PINHOLE)
leader(ax, -16, ph_y, -PAD + 10, ph_y - 60,
       "Shutter flap", ha="right")
leader(ax, prep_wall_x_out + SLEEVE_PROJ_XS / 2, arm_top + 3,
       board_fold_end + 60, arm_top + 50,
       f"Arm sleeves (×2) Ø{SLEEVE_D} mm\n(side by side on prep face)", ha="left", fs=FS_SM - 0.5)
leader(ax, board_x_cam, (paper_y1 + paper_y2) / 2, board_fold_end + 60, ph_y + 40,
       "Watercolor paper on\nbacking board (exposure\nposition — removable)", ha="left", color=C_CL)
board_fold_mid = tray_x_far + board_height / 2
leader(ax, board_fold_mid, hinge_y + 3,
       board_fold_mid, hinge_y + 80,
       "Board folded down\n(prep position — extends\nthrough slot in end face)", ha="center", color=C_MOTION)
leader(ax, tray_x_far, hinge_y - BACKING, tray_x_far - 30, hinge_y - 50,
       "Duct tape hinge\n(at tray rim)", ha="right", color=C_HINGE)
leader(ax, tray_x + TRAY_EXT_D / 2, WALL_T + TRAY_RIM + 3,
       tray_x + TRAY_EXT_D / 2, WALL_T + TRAY_RIM + 60,
       f"Photo tray\n12×16\" (Paterson PTP326)", ha="center", color=C_TRAY)
leader(ax, BOX_D / 2, ph_y + 5, BOX_D / 2, ph_y + 80,
       "Light cone", ha="center", color=C_CONE_LN)

# View title
ax.text((TOTAL_D + board_fold_end) / 2, BOX_H + 100, "SIDE CROSS-SECTION",
        ha="center", va="bottom", fontsize=FS_MD + 2, fontweight="bold", color=C_OUT)
ax.text((TOTAL_D + board_fold_end) / 2, BOX_H + 82,
        "Two-box design — camera box (left) + prep box (right) — standard photo tray with hinged board",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, style="italic")


# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM-LEFT: Rear view — prep box end face (armholes + board slot)
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_rear
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

FPAD = 100
ax.set_xlim(-FPAD, BOX_W + FPAD * 1.5)
ax.set_ylim(-FPAD, BOX_H + FPAD)

# Prep box end face outline (18" wide × 16" high)
ax.add_patch(mpatches.Rectangle((0, 0), BOX_W, BOX_H,
             facecolor=C_BOX, edgecolor=C_OUT, linewidth=1.5, alpha=0.2, zorder=1))

# Wall thickness
for rect in [
    (0, 0, WALL_T, BOX_H),
    (BOX_W - WALL_T, 0, WALL_T, BOX_H),
    (0, 0, BOX_W, WALL_T),
    (0, BOX_H - WALL_T, BOX_W, WALL_T),
]:
    ax.add_patch(mpatches.Rectangle(rect[:2], rect[2], rect[3],
                 facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=0.8, zorder=2))

# Board slot at bottom of end face
slot_w = BOX_W - 2 * WALL_T  # full interior width
slot_h_rear = BACKING + 8     # slot height (board thickness + clearance)
ax.add_patch(mpatches.Rectangle((WALL_T, WALL_T), slot_w, slot_h_rear,
             facecolor="#F0EDE5", edgecolor=C_OUT, linewidth=0.8, zorder=3))
ax.text(BOX_W / 2, WALL_T + slot_h_rear / 2, "BOARD SLOT", ha="center", va="center",
        fontsize=FS_SM - 1.5, color=C_DIM, fontweight="bold")

# Armholes centered on the face, in the upper portion (above slot + tray rim)
arm_face_cy = (WALL_T + slot_h_rear + TRAY_RIM + BOX_H - WALL_T) / 2 + 10
arm_cx1 = BOX_W / 2 - SLEEVE_SPACING / 2
arm_cx2 = BOX_W / 2 + SLEEVE_SPACING / 2

for cx in [arm_cx1, arm_cx2]:
    ax.add_patch(plt.Circle((cx, arm_face_cy), SLEEVE_D / 2,
                 facecolor=C_SLEEVE, edgecolor=C_OUT, linewidth=1.2, alpha=0.8, zorder=4))
    ax.add_patch(mpatches.Annulus((cx, arm_face_cy), SLEEVE_D / 2 + 12, 10,
                 facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.5, alpha=0.4, zorder=3))

# Dimensions
draw_dim_h(ax, 0, BOX_W, -50, f"Width  {BOX_W} mm  (18\")", offset=12)
draw_dim_v(ax, BOX_W + 50, 0, BOX_H, f"Height  {BOX_H} mm  (16\")", offset=12, right=True)
draw_dim_h(ax, arm_cx1, arm_cx2, BOX_H + 40,
           f"Armhole spacing  {SLEEVE_SPACING} mm", offset=10, fs=FS_SM - 0.5)
draw_dim_h(ax, arm_cx1 - SLEEVE_D / 2, arm_cx1 + SLEEVE_D / 2,
           arm_face_cy - SLEEVE_D / 2 - 45,
           f"Ø{SLEEVE_D} mm (4\")", offset=10, fs=FS_SM - 0.5)

# Leaders
leader(ax, arm_cx1, arm_face_cy, -60, arm_face_cy + 50,
       f"Armhole Ø{SLEEVE_D} mm\n(fabric sleeve\n+ elastic at wrist)", ha="right", fs=FS_SM - 0.5)
leader(ax, BOX_W / 2, WALL_T + slot_h_rear, BOX_W + 60, WALL_T + slot_h_rear + 50,
       "Board slot\n(full width, sealed\nwith tape when not\nin use)", ha="left", fs=FS_SM - 0.5)

# View title
ax.text(BOX_W / 2, BOX_H + 85, "REAR VIEW — PREP BOX FACE",
        ha="center", va="bottom", fontsize=FS_MD + 1, fontweight="bold", color=C_OUT)
ax.text(BOX_W / 2, BOX_H + 70,
        "Operator side — armholes (upper) + board slot (bottom)",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, style="italic")


# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM-CENTER: Plan view — both boxes from above
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_planv
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

PPAD = 100
# Extend xlim to show the board extending past the prep box
ax.set_xlim(-PPAD - 40, board_fold_end + PPAD)
ax.set_ylim(-PPAD, BOX_W + PPAD)

# Camera box (left) — depth × width
ax.add_patch(mpatches.Rectangle((0, 0), BOX_D, BOX_W,
             facecolor=C_BOX, edgecolor=C_OUT, linewidth=1.5, alpha=0.25, zorder=1))

# Camera box walls
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

# Prep box walls
for rect in [
    (BOX_D + PREP_D - WALL_T, 0, WALL_T, BOX_W),  # far right (end face)
    (BOX_D, 0, PREP_D, WALL_T),                     # bottom
    (BOX_D, BOX_W - WALL_T, PREP_D, WALL_T),       # top
]:
    ax.add_patch(mpatches.Rectangle(rect[:2], rect[2], rect[3],
                 facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=0.8, alpha=0.7, zorder=2))

# Board slot in end face (shown as gap in wall at bottom)
slot_plan_w = BOX_W - 2 * WALL_T
slot_plan_x = TOTAL_D - WALL_T
# Gap in end wall — erase the wall section
ax.add_patch(mpatches.Rectangle((slot_plan_x, WALL_T), WALL_T, slot_plan_w,
             facecolor=BG, edgecolor=BG, linewidth=0, zorder=3))
# Redraw wall segments above and below the gap (gap is full width for simplicity)
# Actually the slot is a narrow horizontal gap. In plan view the slot appears as a
# thin gap across the full width of the end wall. Show wall as solid with a gap line.
ax.plot([slot_plan_x, TOTAL_D], [WALL_T, WALL_T], color=C_OUT, lw=0.8, zorder=4)
ax.plot([slot_plan_x, TOTAL_D], [BOX_W - WALL_T, BOX_W - WALL_T], color=C_OUT, lw=0.8, zorder=4)

# Photo tray in plan view — inside prep box, against camera-box wall
# In plan view: tray depth (TRAY_EXT_D) along X, tray width (TRAY_EXT_W) along Y
tray_plan_x = BOX_D + WALL_T  # against camera side
tray_plan_y = BOX_W / 2 - TRAY_EXT_W / 2  # centered in box width
ax.add_patch(mpatches.Rectangle((tray_plan_x, tray_plan_y), TRAY_EXT_D, TRAY_EXT_W,
             facecolor=C_TRAY, edgecolor=C_OUT, linewidth=0.8, alpha=0.3, zorder=3))

# Board at camera junction (exposure position — solid line)
ax.plot([BOX_D - BACKING, BOX_D - BACKING], [WALL_T, BOX_W - WALL_T],
        color=C_BACKING, lw=3.0, solid_capstyle="butt", zorder=4)

# Board folded down from tray rim (dashed, extending past prep box)
ax.add_patch(mpatches.Rectangle((tray_plan_x + TRAY_EXT_D, WALL_T),
             board_height, BOX_W - 2 * WALL_T,
             facecolor=C_BACKING, edgecolor=C_OUT, linewidth=0.6,
             linestyle="--", alpha=0.15, zorder=2))

# Pinhole marker on left wall
ax.add_patch(plt.Circle((WALL_T / 2, BOX_W / 2), 5,
             facecolor=C_PINHOLE, edgecolor=C_OUT, linewidth=0.8, zorder=5))

# Armholes on prep box end face (right wall) — shown as gaps in wall
# with dashed hidden-line circles
arm_plan_cy1 = BOX_W / 2 - SLEEVE_SPACING / 2
arm_plan_cy2 = BOX_W / 2 + SLEEVE_SPACING / 2
right_wall_x = TOTAL_D - WALL_T
right_wall_xo = TOTAL_D

for cy in [arm_plan_cy1, arm_plan_cy2]:
    # Gap in wall
    ax.add_patch(mpatches.Rectangle(
        (right_wall_x, cy - SLEEVE_D / 2), WALL_T, SLEEVE_D,
        facecolor=BG, edgecolor=BG, linewidth=0, zorder=3))
    ax.plot([right_wall_x, right_wall_xo], [cy - SLEEVE_D / 2, cy - SLEEVE_D / 2],
            color=C_OUT, lw=0.8, zorder=4)
    ax.plot([right_wall_x, right_wall_xo], [cy + SLEEVE_D / 2, cy + SLEEVE_D / 2],
            color=C_OUT, lw=0.8, zorder=4)
    # Hidden circle (dashed)
    ax.add_patch(plt.Circle((right_wall_x + WALL_T / 2, cy), SLEEVE_D / 2,
                 facecolor="none", edgecolor=C_SLEEVE, linewidth=0.8,
                 linestyle="--", alpha=0.5, zorder=3))
    # Sleeve projection (extending right)
    sleeve_proj = 80
    ax.add_patch(mpatches.Rectangle(
        (right_wall_xo, cy - SLEEVE_D / 2), sleeve_proj, SLEEVE_D,
        facecolor=C_SLEEVE, edgecolor="none", alpha=0.08, zorder=1))
    ax.plot([right_wall_xo, right_wall_xo + sleeve_proj],
            [cy - SLEEVE_D / 2, cy - SLEEVE_D / 2],
            color=C_SLEEVE, lw=0.8, ls="--", zorder=2)
    ax.plot([right_wall_xo, right_wall_xo + sleeve_proj],
            [cy + SLEEVE_D / 2, cy + SLEEVE_D / 2],
            color=C_SLEEVE, lw=0.8, ls="--", zorder=2)
    ax.plot([right_wall_xo + sleeve_proj, right_wall_xo + sleeve_proj],
            [cy - SLEEVE_D / 2 + 8, cy + SLEEVE_D / 2 - 8],
            color=C_PINHOLE, lw=2.0, solid_capstyle="round", zorder=3)

# Optical axis
ax.plot([0, BOX_D], [BOX_W / 2, BOX_W / 2],
        color=C_CL, lw=0.7, ls="--", dashes=(8, 4), zorder=2)

# Box labels
ax.text(BOX_D / 2, BOX_W / 2, "CAMERA", ha="center", va="center",
        fontsize=FS_SM, fontweight="bold", color=C_DIM, alpha=0.4)
ax.text(BOX_D + PREP_D / 2, BOX_W / 2, "PREP", ha="center", va="center",
        fontsize=FS_SM, fontweight="bold", color=C_DIM, alpha=0.4)

# Face labels
ax.text(WALL_T / 2, BOX_W + 20, "PINHOLE\nFACE", ha="center", va="bottom",
        fontsize=FS_SM - 1, color=C_PINHOLE, fontweight="bold")
ax.text(TOTAL_D - WALL_T / 2, BOX_W + 20, "PREP\nFACE", ha="center", va="bottom",
        fontsize=FS_SM - 1, color=C_SLEEVE, fontweight="bold")

# Dimensions
draw_dim_h(ax, 0, TOTAL_D, BOX_W + 45, f"Total  {TOTAL_D} mm  (36\")", offset=10, fs=FS_SM - 0.5)
draw_dim_v(ax, board_fold_end + sleeve_proj + 20, 0, BOX_W,
           f"{BOX_W} mm", offset=10, right=True, fs=FS_SM - 0.5)
draw_dim_h(ax, 0, BOX_D, -50, f"Camera  {BOX_D} mm", offset=8, fs=FS_SM - 0.5)
draw_dim_h(ax, BOX_D, TOTAL_D, -50, f"Prep  {PREP_D} mm", offset=8, fs=FS_SM - 0.5)

# Leaders
leader(ax, BOX_D - BACKING, BOX_W / 2, BOX_D - BACKING - 20, BOX_W + 30,
       "Board (exposure\nposition)", ha="right", color=C_MOTION, fs=FS_SM - 0.5)
leader(ax, tray_plan_x + TRAY_EXT_D / 2, tray_plan_y + TRAY_EXT_W,
       tray_plan_x + TRAY_EXT_D / 2, BOX_W + 30,
       "Photo tray", ha="center", color=C_TRAY, fs=FS_SM - 0.5)
leader(ax, tray_plan_x + TRAY_EXT_D + board_height / 2, BOX_W / 2,
       board_fold_end + 20, BOX_W / 2 + 30,
       "Board folded\n(prep position)", ha="left", color=C_MOTION, fs=FS_SM - 0.5)
leader(ax, right_wall_xo + sleeve_proj / 2, arm_plan_cy1,
       board_fold_end + sleeve_proj + 10, arm_plan_cy1 - 40,
       "Sleeves", ha="left", fs=FS_SM - 0.5)

# View title
ax.text((TOTAL_D + board_fold_end) / 2, BOX_W + 80, "PLAN VIEW — LOOKING DOWN",
        ha="center", va="bottom", fontsize=FS_MD + 1, fontweight="bold", color=C_OUT)
ax.text((TOTAL_D + board_fold_end) / 2, BOX_W + 65,
        "Two-box arrangement, photo tray in prep box, board extends through slot",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, style="italic")


# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM-RIGHT: Assembly notes + specification
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_asm
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(0, 400)
ax.set_ylim(0, 420)

# ── Specification table ─────────────────────────────────────────────────────
ax.add_patch(mpatches.FancyBboxPatch((10, 250), 380, 160,
             boxstyle="round,pad=6", facecolor="#F8F6F0", edgecolor=C_OUT,
             linewidth=0.8, zorder=1))

ax.text(200, 400, "SPECIFICATION", ha="center", va="top",
        fontsize=FS_MD, fontweight="bold", color=C_OUT)
ax.plot([30, 370], [392, 392], color=C_OUT, lw=0.6)

specs = [
    f"Focal length:  {FOCAL} mm (18\")",
    f"Pinhole:  Ø{PH_D} mm (1/32\" drill bit)",
    f"f-number:  f/{F_NO}",
    f"Film plane:  {FP_W} × {FP_H} mm",
    f"Exposure:  ~10 min (full sun)",
    "Substrate:  Watercolor paper 300 gsm",
    "Process:  Ware New Cyanotype",
    f"Tray:  Paterson 12×16\" (PTP326)",
]
y = 382
for line in specs:
    ax.text(30, y, line, ha="left", va="top",
            fontsize=FS_SM, color=C_DIM)
    y -= 17

# ── Assembly notes ──────────────────────────────────────────────────────────
ax.add_patch(mpatches.FancyBboxPatch((10, 10), 380, 230,
             boxstyle="round,pad=6", facecolor="#F8F6F0", edgecolor=C_OUT,
             linewidth=0.8, zorder=1))

ax.text(200, 230, "ASSEMBLY SEQUENCE", ha="center", va="top",
        fontsize=FS_MD, fontweight="bold", color=C_OUT)
ax.plot([30, 370], [222, 222], color=C_OUT, lw=0.6)

steps = [
    "1.  Seal both boxes with gaffer tape.\n"
    "     Join end-to-end at 18×16\" faces.",
    "2.  Place Paterson 12×16\" tray in\n"
    "     prep box (against camera side).",
    "3.  Hinge backing board to tray far\n"
    "     rim with duct tape. Cut board\n"
    "     slot in prep box end face.",
    "4.  Cut armholes above board slot.\n"
    "     Attach fabric sleeves.",
    "5.  Fabricate pinhole: drill 1/32\" hole\n"
    "     in aluminum can, sand burr.",
    "6.  Mount pinhole plate + shutter.",
    "7.  Coat paper in tray → tack-dry →\n"
    "     fold board down → mount paper\n"
    "     → fold up → place in camera box.",
]

y = 210
for step in steps:
    ax.text(30, y, step, ha="left", va="top",
            fontsize=FS_SM - 0.5, color=C_DIM, linespacing=1.2)
    y -= 27


# ── Title block (full-figure overlay) ────────────────────────────────────────
ax_tb = fig.add_axes([0, 0, 1, 1], facecolor="none")
ax_tb.axis("off")
title_block(ax_tb, "SHEET 1 OF 1",
            drawing_title="MINI-TBS PROOF OF CONCEPT",
            subtitle="Two-box camera + prep area — photo tray with hinged board, watercolor paper",
            scale_note="Approx 1:4 (views) / NTS (detail)",
            doc_id="TBS-POC · Mini-TBS")

# ── Save ─────────────────────────────────────────────────────────────────────
out = f"{DIAGRAMS_DIR}/mini-tbs-sheet1.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(f"Saved: {out}")
