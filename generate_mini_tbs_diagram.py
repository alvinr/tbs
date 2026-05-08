#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_mini_tbs_diagram.py

Mini-TBS proof-of-concept pinhole camera — engineering drawing.
Output: diagrams/mini-tbs-sheet1.png

Single sheet with five panels showing the two-box design:
  Top (full width):    Side cross-section — camera box + prep box, hinged flap
  Bottom-left:         Front view — pinhole face with armholes
  Bottom-center:       Plan view — both boxes from above
  Bottom-right:        Assembly notes
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
SLEEVE_SPACING = 230  # mm — armhole center-to-center on pinhole face
SLEEVE_LEN = 457  # mm — sleeve tube length (18")

WALL_T  = 4      # mm — cardboard wall thickness (schematic)
BACKING = 5      # mm — foam-core backing board thickness

# Prep box dimensions (same box model)
PREP_D  = BOX_D  # mm — prep box depth (matches camera box)

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
# SINGLE SHEET — Five panels
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
ax_front = fig.add_subplot(gs[1, 0])    # front view — pinhole face w/ armholes
ax_planv = fig.add_subplot(gs[1, 1])    # plan view — both boxes from above
ax_asm   = fig.add_subplot(gs[1, 2])    # assembly notes + spec table


# ══════════════════════════════════════════════════════════════════════════════
# TOP: Side cross-section — camera box + prep box with hinged flap
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_xsec
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

# Layout: camera box on left, prep box on right, sharing a wall
# X origin at left edge of camera box, Y origin at floor
TOTAL_D = BOX_D + PREP_D  # both boxes end-to-end
PAD = 120
ax.set_xlim(-PAD - 40, TOTAL_D + PAD * 1.5)
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

# No right wall on camera box — that's where the flap/opening is
# Draw just the top and bottom edges at the junction
ax.plot([BOX_D, BOX_D], [0, WALL_T], color=C_OUT, lw=0.8, zorder=2)
ax.plot([BOX_D, BOX_D], [BOX_H - WALL_T, BOX_H], color=C_OUT, lw=0.8, zorder=2)

# ── Prep box (right) ────────────────────────────────────────────────────────
ax.add_patch(mpatches.Rectangle((BOX_D, 0), PREP_D, BOX_H,
             facecolor=C_BOX, edgecolor=C_OUT, linewidth=1.5, alpha=0.15, zorder=1))

# Prep box walls
for rect in [
    (BOX_D + PREP_D - WALL_T, 0, WALL_T, BOX_H),  # far right wall
    (BOX_D, 0, PREP_D, WALL_T),                     # floor
    (BOX_D, BOX_H - WALL_T, PREP_D, WALL_T),       # ceiling
]:
    ax.add_patch(mpatches.Rectangle(rect[:2], rect[2], rect[3],
                 facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=0.8, alpha=0.7, zorder=2))

# ── Hinged flap — shown in UPRIGHT position (solid) ─────────────────────────
flap_x = BOX_D  # at the junction between boxes
flap_bottom = WALL_T
flap_top = BOX_H - WALL_T
flap_height = flap_top - flap_bottom

# Flap upright (solid) — the backing board with paper
ax.add_patch(mpatches.Rectangle((flap_x - BACKING, flap_bottom), BACKING, flap_height,
             facecolor=C_BACKING, edgecolor=C_OUT, linewidth=1.0, zorder=5))
# Paper on the camera side of the flap
ax.plot([flap_x - BACKING, flap_x - BACKING],
        [flap_bottom + MARGIN, flap_top - MARGIN],
        color=C_CL, lw=3.0, solid_capstyle="butt", zorder=6)

# ── Hinged flap — shown in FOLDED DOWN position (dashed) ────────────────────
# When folded down, the flap lies flat on the prep box floor
# Hinge point is at (flap_x, flap_bottom)
folded_y = flap_bottom + BACKING  # lies on top of floor
folded_x_end = flap_x + flap_height  # extends into prep box

# Folded flap (dashed outline)
ax.add_patch(mpatches.Rectangle((flap_x, flap_bottom), flap_height, BACKING,
             facecolor=C_BACKING, edgecolor=C_OUT, linewidth=0.8,
             linestyle="--", alpha=0.4, zorder=3))
# Paper on the folded flap (dashed)
ax.plot([flap_x + MARGIN, folded_x_end - MARGIN],
        [flap_bottom + BACKING, flap_bottom + BACKING],
        color=C_CL, lw=2.5, ls="--", dashes=(4, 3), alpha=0.5,
        solid_capstyle="butt", zorder=4)

# ── Hinge arc (motion indicator) ────────────────────────────────────────────
# Arc from upright to folded, pivot at (flap_x, flap_bottom)
arc_r = flap_height * 0.35
arc = Arc((flap_x, flap_bottom), arc_r * 2, arc_r * 2,
          angle=0, theta1=0, theta2=90,
          color=C_MOTION, lw=1.5, ls="--", zorder=7)
ax.add_patch(arc)
# Arrowhead at the end of the arc (at 0°, pointing right)
ax.annotate("", xy=(flap_x + arc_r, flap_bottom),
            xytext=(flap_x + arc_r - 15, flap_bottom + 12),
            arrowprops=dict(arrowstyle="->", color=C_MOTION, lw=1.5), zorder=7)

# ── Hinge detail (duct tape) ────────────────────────────────────────────────
hinge_w = 20
ax.add_patch(mpatches.Rectangle((flap_x - hinge_w / 2, flap_bottom - 3),
             hinge_w, 6,
             facecolor=C_HINGE, edgecolor=C_OUT, linewidth=0.5, alpha=0.8, zorder=8))

# ── Chemistry tray in prep box ──────────────────────────────────────────────
# Tray must accommodate the full paper size (16×18" / 406×457mm).
# In cross-section we see the tray's depth (457mm) and height.
# Position it on the prep box floor, centered.
TRAY_DEPTH = BOX_D   # 457mm — same as paper width (18")
TRAY_RIM   = 40      # mm — tray rim height
tray_x = BOX_D + (PREP_D - TRAY_DEPTH) / 2  # centered in prep box
ax.add_patch(mpatches.Rectangle((tray_x, WALL_T), TRAY_DEPTH, TRAY_RIM,
             facecolor=C_TRAY, edgecolor=C_OUT, linewidth=0.8, alpha=0.3, zorder=3))
# Tray rims (left and right walls)
ax.plot([tray_x, tray_x], [WALL_T, WALL_T + TRAY_RIM], color=C_OUT, lw=1.2, zorder=4)
ax.plot([tray_x + TRAY_DEPTH, tray_x + TRAY_DEPTH], [WALL_T, WALL_T + TRAY_RIM],
        color=C_OUT, lw=1.2, zorder=4)

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
paper_x = flap_x - BACKING
paper_y1 = flap_bottom + MARGIN
paper_y2 = flap_top - MARGIN
cone_verts = [
    (WALL_T, ph_y),
    (paper_x, paper_y2),
    (paper_x, paper_y1),
]
ax.add_patch(mpatches.Polygon(cone_verts, closed=True,
             facecolor=C_CONE, edgecolor="none", alpha=0.2, zorder=1))
ax.plot([WALL_T, paper_x], [ph_y, paper_y2],
        color=C_CONE_LN, lw=0.8, ls="--", dashes=(6, 4), alpha=0.7, zorder=2)
ax.plot([WALL_T, paper_x], [ph_y, paper_y1],
        color=C_CONE_LN, lw=0.8, ls="--", dashes=(6, 4), alpha=0.7, zorder=2)

# Optical axis
ax.plot([0, flap_x], [ph_y, ph_y],
        color=C_CL, lw=0.7, ls="--", dashes=(8, 4), zorder=2)

# Shutter flap (outside left wall)
ax.add_patch(mpatches.Rectangle((-30, ph_y - 50), 28, 100,
             facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=3))

# ── Armholes on prep box end face (far right wall in cross-section) ─────────
# The operator reaches into the prep box to coat the paper on the folded-down
# flap, then pulls arms out and folds the flap up.
SLEEVE_PROJ_XS = 80  # sleeve projection length in cross-section
prep_wall_x = BOX_D + PREP_D - WALL_T  # inside edge of far right wall
prep_wall_x_out = BOX_D + PREP_D       # outside edge
for arm_y_center in [ph_y + SLEEVE_SPACING / 2, ph_y - SLEEVE_SPACING / 2]:
    arm_top = arm_y_center + SLEEVE_D / 2
    arm_bot = arm_y_center - SLEEVE_D / 2
    # Erase wall at armhole opening
    ax.add_patch(mpatches.Rectangle((prep_wall_x, arm_bot), WALL_T, SLEEVE_D,
                 facecolor=C_BOX, edgecolor="none", linewidth=0, alpha=0.15, zorder=3))
    # Gap edges in wall
    ax.plot([prep_wall_x, prep_wall_x_out], [arm_top, arm_top], color=C_OUT, lw=0.8, zorder=4)
    ax.plot([prep_wall_x, prep_wall_x_out], [arm_bot, arm_bot], color=C_OUT, lw=0.8, zorder=4)
    # Sleeve tube projecting outward (to the right)
    ax.add_patch(mpatches.Rectangle((prep_wall_x_out, arm_bot),
                 SLEEVE_PROJ_XS, SLEEVE_D,
                 facecolor=C_SLEEVE, edgecolor="none", alpha=0.08, zorder=1))
    ax.plot([prep_wall_x_out, prep_wall_x_out + SLEEVE_PROJ_XS], [arm_top, arm_top],
            color=C_SLEEVE, lw=1.0, ls="--", zorder=3)
    ax.plot([prep_wall_x_out, prep_wall_x_out + SLEEVE_PROJ_XS], [arm_bot, arm_bot],
            color=C_SLEEVE, lw=1.0, ls="--", zorder=3)
    # Elastic band at wrist
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
draw_dim_h(ax, BOX_D, BOX_D + PREP_D, -55, f"Prep box  {PREP_D} mm  (18\")", offset=15)
draw_dim_h(ax, 0, TOTAL_D, -100, f"Total length  {TOTAL_D} mm  (36\")", offset=15)
draw_dim_v(ax, -50, 0, BOX_H, f"{BOX_H} mm\n(16\")", offset=15)
draw_dim_v(ax, TOTAL_D + 60, paper_y1, paper_y2,
           f"Image  {FP_H} mm", offset=12, color=C_CL, right=True)

# ── Cross-section leaders ───────────────────────────────────────────────────
leader(ax, WALL_T / 2, ph_y + 10, -PAD + 10, ph_y + 100,
       f"Pinhole  Ø{PH_D} mm\nf/{F_NO}", ha="right", color=C_PINHOLE)
leader(ax, -16, ph_y, -PAD + 10, ph_y - 60,
       "Shutter flap", ha="right")
# Armhole sleeves leader (point at upper sleeve on prep box end)
upper_arm_y = ph_y + SLEEVE_SPACING / 2
leader(ax, prep_wall_x_out + SLEEVE_PROJ_XS / 2, upper_arm_y + SLEEVE_D / 2 + 3,
       TOTAL_D + 100, upper_arm_y + SLEEVE_D / 2 + 60,
       f"Arm sleeve Ø{SLEEVE_D} mm\n(on prep box face)", ha="left", fs=FS_SM - 0.5)
leader(ax, paper_x, (paper_y1 + paper_y2) / 2, TOTAL_D + 100, ph_y + 50,
       "Watercolor paper\non backing board\n(upright = film plane)", ha="left", color=C_CL)
leader(ax, flap_x + flap_height / 2, flap_bottom + BACKING + 3,
       flap_x + flap_height / 2, flap_bottom + 80,
       "Flap folded down\n(dashed — coating position)", ha="center", color=C_MOTION)
leader(ax, flap_x, flap_bottom, flap_x - 40, flap_bottom - 40,
       "Duct tape hinge", ha="right", color=C_HINGE)
leader(ax, tray_x + TRAY_DEPTH / 2, WALL_T + TRAY_RIM,
       tray_x + TRAY_DEPTH / 2, WALL_T + TRAY_RIM + 70,
       f"Chemistry tray\n16 × 18\" ({BOX_H} × {BOX_D} mm)\n(fits full paper sheet)", ha="center", color=C_TRAY)
leader(ax, BOX_D / 2, ph_y + 5, BOX_D / 2, ph_y + 80,
       "Light cone", ha="center", color=C_CONE_LN)

# View title
ax.text(TOTAL_D / 2, BOX_H + 100, "SIDE CROSS-SECTION",
        ha="center", va="bottom", fontsize=FS_MD + 2, fontweight="bold", color=C_OUT)
ax.text(TOTAL_D / 2, BOX_H + 82,
        "Two-box design  —  camera box (left) + prep box (right)  —  hinged flap between",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, style="italic")


# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM-LEFT: Rear view — prep box end face with armholes
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_front
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

# Armholes centered on the face, spaced vertically
arm_cx1 = BOX_W / 2 - SLEEVE_SPACING / 2
arm_cx2 = BOX_W / 2 + SLEEVE_SPACING / 2
arm_cy = BOX_H / 2

for cx in [arm_cx1, arm_cx2]:
    ax.add_patch(plt.Circle((cx, arm_cy), SLEEVE_D / 2,
                 facecolor=C_SLEEVE, edgecolor=C_OUT, linewidth=1.2, alpha=0.8, zorder=4))
    ax.add_patch(mpatches.Annulus((cx, arm_cy), SLEEVE_D / 2 + 12, 10,
                 facecolor=C_TAPE, edgecolor=C_OUT, linewidth=0.5, alpha=0.4, zorder=3))

# Dimensions
draw_dim_h(ax, 0, BOX_W, -50, f"Width  {BOX_W} mm  (18\")", offset=12)
draw_dim_v(ax, BOX_W + 50, 0, BOX_H, f"Height  {BOX_H} mm  (16\")", offset=12, right=True)
draw_dim_h(ax, arm_cx1, arm_cx2, BOX_H + 40,
           f"Armhole spacing  {SLEEVE_SPACING} mm", offset=10, fs=FS_SM - 0.5)
draw_dim_h(ax, arm_cx1 - SLEEVE_D / 2, arm_cx1 + SLEEVE_D / 2,
           arm_cy - SLEEVE_D / 2 - 25,
           f"Ø{SLEEVE_D} mm (4\")", offset=10, fs=FS_SM - 0.5)

# Leaders
leader(ax, arm_cx1, arm_cy, -60, arm_cy + 50,
       f"Armhole Ø{SLEEVE_D} mm\n(fabric sleeve\n+ elastic at wrist)", ha="right", fs=FS_SM - 0.5)
leader(ax, arm_cx1 + SLEEVE_D / 2 + 15, arm_cy, BOX_W + 80, arm_cy + 70,
       "Gaffer tape seal", ha="left", fs=FS_SM - 0.5)

# Spec table
spec_x = BOX_W + 80
spec_y = BOX_H - 60
specs = [
    f"Focal length:  {FOCAL} mm",
    f"Pinhole:  Ø{PH_D} mm",
    f"f-number:  f/{F_NO}",
    f"Film plane:  {FP_W} × {FP_H} mm",
    f"Exposure:  ~10 min (full sun)",
    "Substrate:  WC paper 300 gsm",
    "Process:  Ware New Cyanotype",
]
ax.text(spec_x, spec_y + 18, "SPECIFICATION", ha="left", va="bottom",
        fontsize=FS_SM + 0.5, fontweight="bold", color=C_OUT)
ax.plot([spec_x, spec_x + 200], [spec_y + 14, spec_y + 14], color=C_OUT, lw=0.8)
for i, line in enumerate(specs):
    ax.text(spec_x, spec_y - i * 18, line, ha="left", va="top",
            fontsize=FS_SM - 0.5, color=C_DIM)

# View title
ax.text(BOX_W / 2, BOX_H + 85, "REAR VIEW — PREP BOX FACE",
        ha="center", va="bottom", fontsize=FS_MD + 1, fontweight="bold", color=C_OUT)
ax.text(BOX_W / 2, BOX_H + 70,
        "Operator side — two armholes for coating access",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, style="italic")


# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM-CENTER: Plan view — both boxes from above
# ══════════════════════════════════════════════════════════════════════════════
ax = ax_planv
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

PPAD = 100
ax.set_xlim(-PPAD - 40, TOTAL_D + PPAD)
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
    (BOX_D + PREP_D - WALL_T, 0, WALL_T, BOX_W),  # far right
    (BOX_D, 0, PREP_D, WALL_T),                     # bottom
    (BOX_D, BOX_W - WALL_T, PREP_D, WALL_T),       # top
]:
    ax.add_patch(mpatches.Rectangle(rect[:2], rect[2], rect[3],
                 facecolor=C_BOX_WALL, edgecolor=C_OUT, linewidth=0.8, alpha=0.7, zorder=2))

# Hinged flap position (upright — shown as thin line at junction)
ax.plot([BOX_D, BOX_D], [WALL_T, BOX_W - WALL_T],
        color=C_BACKING, lw=3.0, solid_capstyle="butt", zorder=4)

# Backing board / flap (folded down — dashed, extending into prep box)
flap_plan_len = BOX_H - 2 * WALL_T  # flap length when folded
ax.add_patch(mpatches.Rectangle((BOX_D, WALL_T), flap_plan_len, BOX_W - 2 * WALL_T,
             facecolor=C_BACKING, edgecolor=C_OUT, linewidth=0.6,
             linestyle="--", alpha=0.15, zorder=2))

# Chemistry tray in prep box (plan view) — sized to fit the paper (16×18" / 406×457mm)
# In plan view: tray depth = 457mm (along X), tray width = 406mm (along Y)
tray_plan_x = BOX_D + (PREP_D - TRAY_DEPTH) / 2  # centered in prep box depth
tray_plan_w = TRAY_DEPTH  # 457mm
TRAY_WIDTH = BOX_H  # 406mm — matches paper height (16")
tray_plan_h = TRAY_WIDTH
tray_plan_y = BOX_W / 2 - tray_plan_h / 2  # centered in box width
ax.add_patch(mpatches.Rectangle((tray_plan_x, tray_plan_y), tray_plan_w, tray_plan_h,
             facecolor=C_TRAY, edgecolor=C_OUT, linewidth=0.8, alpha=0.3, zorder=3))

# Pinhole marker on left wall
ax.add_patch(plt.Circle((WALL_T / 2, BOX_W / 2), 5,
             facecolor=C_PINHOLE, edgecolor=C_OUT, linewidth=0.8, zorder=5))

# Armholes on prep box end face (right wall) — shown as gaps in wall
arm_plan_cy1 = BOX_W / 2 - SLEEVE_SPACING / 2
arm_plan_cy2 = BOX_W / 2 + SLEEVE_SPACING / 2
right_wall_x = TOTAL_D - WALL_T  # inner edge of right wall
right_wall_xo = TOTAL_D          # outer edge of right wall

for cy in [arm_plan_cy1, arm_plan_cy2]:
    # Gap in wall
    ax.add_patch(mpatches.Rectangle(
        (right_wall_x, cy - SLEEVE_D / 2), WALL_T, SLEEVE_D,
        facecolor=BG, edgecolor=BG, linewidth=0, zorder=3))
    # Wall edges at gap
    ax.plot([right_wall_x, right_wall_xo], [cy - SLEEVE_D / 2, cy - SLEEVE_D / 2],
            color=C_OUT, lw=0.8, zorder=4)
    ax.plot([right_wall_x, right_wall_xo], [cy + SLEEVE_D / 2, cy + SLEEVE_D / 2],
            color=C_OUT, lw=0.8, zorder=4)
    # Hidden circle (dashed)
    ax.add_patch(plt.Circle((right_wall_x + WALL_T / 2, cy), SLEEVE_D / 2,
                 facecolor="none", edgecolor=C_SLEEVE, linewidth=0.8,
                 linestyle="--", alpha=0.5, zorder=3))
    # Sleeve projection (extending right, outside box)
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
    # Elastic
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
draw_dim_v(ax, TOTAL_D + 40, 0, BOX_W, f"{BOX_W} mm", offset=10, right=True, fs=FS_SM - 0.5)
draw_dim_h(ax, 0, BOX_D, -50, f"Camera  {BOX_D} mm", offset=8, fs=FS_SM - 0.5)
draw_dim_h(ax, BOX_D, TOTAL_D, -50, f"Prep  {PREP_D} mm", offset=8, fs=FS_SM - 0.5)

# Leaders
leader(ax, BOX_D, BOX_W / 2, BOX_D + flap_plan_len + 20, BOX_W + 30,
       "Hinged flap\n(upright position)", ha="left", color=C_MOTION, fs=FS_SM - 0.5)
leader(ax, tray_plan_x + tray_plan_w / 2, tray_plan_y + tray_plan_h,
       tray_plan_x + tray_plan_w / 2, BOX_W + 30,
       "Tray", ha="center", color=C_TRAY, fs=FS_SM - 0.5)
leader(ax, right_wall_xo + sleeve_proj / 2, arm_plan_cy1,
       TOTAL_D + sleeve_proj + 20, arm_plan_cy1 - 40,
       "Sleeves", ha="left", fs=FS_SM - 0.5)

# View title
ax.text(TOTAL_D / 2, BOX_W + 80, "PLAN VIEW — LOOKING DOWN",
        ha="center", va="bottom", fontsize=FS_MD + 1, fontweight="bold", color=C_OUT)
ax.text(TOTAL_D / 2, BOX_W + 65,
        "Two-box arrangement, armholes on prep box end face",
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
    "Reciprocity:  None (iron-based)",
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
    "1.  Seal both boxes with gaffer tape.",
    "2.  Remove shared wall. Hinge the\n"
    "     backing board at bottom with\n"
    "     duct tape (full width).",
    "3.  Cut armholes on pinhole face,\n"
    "     flanking the pinhole. Attach\n"
    "     fabric sleeves with gaffer tape.",
    "4.  Fabricate pinhole: drill 1/32\" hole\n"
    "     in aluminum can, sand burr.",
    "5.  Mount pinhole plate from inside.\n"
    "     Attach shutter flap outside.",
    "6.  Place chemistry tray in prep box.",
    "7.  Fold flap down → coat paper →\n"
    "     tack-dry → fold up → expose.",
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
            subtitle="Two-box camera + prep area — hinged flap, watercolor paper substrate",
            scale_note="Approx 1:4 (views) / NTS (detail)",
            doc_id="TBS-POC · Mini-TBS")

# ── Save ─────────────────────────────────────────────────────────────────────
out = f"{DIAGRAMS_DIR}/mini-tbs-sheet1.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
plt.close(fig)
print(f"Saved: {out}")
