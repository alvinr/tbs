#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_tilt_swing_board.py
Tilt-and-Swing Front Board — The Big Shoebox Project
Drawing series TBS-TSB  (3 sheets)

Sheet 1 — Assembly overview & Outer Adapter Frame (TSB-01)
Sheet 2 — Inner Carrier Plate (TSB-02), Bearing & Adjustment mechanism
Sheet 3 — Light seal (bellows), Locking, Calibration scale & Swap procedure

Style matches generate_plate_drawing.py (white background, same palette & helpers).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
from tbs_constants import svg_path, SVG_DIR

# ── Dimensions (mm) ──────────────────────────────────────────────────────────

# --- existing plate interface (unchanged) ---
PL_OD      = 600      # plate outer dimension (square)
BOLT_BC    = 540      # bolt circle diameter
BOLT_D     = 13       # bolt hole clearance diameter
BOLT_N     = 8
DWL_D      = 8        # dowel pin diameter
DWL_OFF    = 200      # ± horizontal from center
SEAL_D     = 420      # neoprene groove PCD
TRAP_SQ    = 490      # light-trap rebate PCD (square)
FR_APT_D   = 350      # wall frame aperture diameter
PH_CB_D    = 52       # pinhole disc counterbore
PH_CB_DEP  = 3
PH_DISC_D  = 50
PH_BORE    = 90       # exterior taper bore

# --- TSB-01 Outer Adapter Frame ---
TSB01_THICK  = 40     # plate thickness
TSB01_BORE   = 380    # central bore diameter
BRG_SEAT_D   = 80     # bearing outer ring OD / seat bore diameter
BRG_SEAT_DEP = 50     # depth of bearing pocket
ADJ_PCD      = 270    # adjustment screw PCD (in frame)
ADJ_N        = 4      # 4 screws
LAB_D1, LAB_D2, LAB_D3 = 382, 390, 400  # labyrinth step diameters
BELL_OUT_PCD = 375    # bellows outer flange bolt PCD

# --- TSB-02 Inner Carrier Plate ---
CARR_OD      = 320    # carrier plate OD
CARR_THICK   = 25     # thickness
BRG_SHANK_D  = 50     # bearing shank diameter (k5)
BRG_SHANK_L  = 35     # shank length
SOCK_PCD     = 260    # ball socket insert PCD
BELL_IN_PCD  = 310    # bellows inner flange bolt PCD

# --- Bearing TSB-03 ---
BRG_OD       = 80
BRG_ID       = 50
BRG_W        = 46     # total width

# --- Adjustment screw ---
ADJ_D        = 8      # M8 screw
ADJ_ARM      = 130    # arm radius (frame ADJ_PCD/2 - a few mm for geometry)
BALL_D       = 8      # chrome steel ball
KNOB_D       = 40
KNOB_H       = 15
BUSH_OD      = 22
BUSH_L       = 35

# --- Bellows ---
BELL_ID      = 290
BELL_OD      = 360
BELL_FREE    = 60     # free length
BELL_PLEATS  = 4
BELL_PLEAT_D = 15     # pleat depth

SEAL_W   = 3          # neoprene seal groove width
SEAL_DEP = 3          # seal groove depth

# ── Drawing helpers (same as generate_plate_drawing.py) ───────────────────────

LW_THICK = 1.8
LW_MED   = 1.0
LW_THIN  = 0.5
LW_CUT   = 2.2
LW_DIM   = 0.7

C_OUT   = '#000000'
C_CL    = '#0055AA'
C_DIM   = '#333333'
C_HID   = '#888888'
C_STEEL = '#B0B0B0'
C_ALUM  = '#D8D8D8'
C_GASKT = '#404040'
C_RED   = '#CC0000'
C_DELR  = '#E8D8A0'   # Delrin/POM color
C_BEAR  = '#C0C8D8'   # bearing / steel blue-grey
C_BELL  = '#303030'   # bellows black

def draw_dim_h(ax, x1, x2, y, text, above=True, fontsize=6, scale=1.0):
    off = 3 * scale
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM,
                                mutation_scale=5*scale))
    mx = (x1 + x2) / 2
    va = 'bottom' if above else 'top'
    ax.text(mx, y + (1.5*scale if above else -1.5*scale), text,
            ha='center', va=va, fontsize=fontsize, color=C_DIM)
    ax.plot([x1, x1], [y - off*0.3, y + off*0.3], color=C_DIM, lw=0.5)
    ax.plot([x2, x2], [y - off*0.3, y + off*0.3], color=C_DIM, lw=0.5)

def draw_dim_v(ax, x, y1, y2, text, right=True, fontsize=6, scale=1.0):
    off = 3 * scale
    ax.annotate('', xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM,
                                mutation_scale=5*scale))
    my = (y1 + y2) / 2
    ha = 'left' if right else 'right'
    ax.text(x + (1.5*scale if right else -1.5*scale), my, text,
            ha=ha, va='center', fontsize=fontsize, color=C_DIM,
            rotation=90 if not right else 0)
    ax.plot([x - off*0.3, x + off*0.3], [y1, y1], color=C_DIM, lw=0.5)
    ax.plot([x - off*0.3, x + off*0.3], [y2, y2], color=C_DIM, lw=0.5)

def draw_cl(ax, cx, cy, r, horiz=True, vert=True):
    ext = max(r * 1.25, 5)
    ls = (0, (6, 2, 1, 2))
    if horiz:
        ax.plot([cx - ext, cx + ext], [cy, cy], color=C_CL, lw=LW_THIN, linestyle=ls)
    if vert:
        ax.plot([cx, cx], [cy - ext, cy + ext], color=C_CL, lw=LW_THIN, linestyle=ls)

def draw_circle(ax, cx, cy, r, lw=LW_THICK, color=C_OUT, ls='-', fill=False, fc='none', zorder=4):
    c = mpatches.Circle((cx, cy), r, lw=lw, edgecolor=color, facecolor=fc if fill else 'none',
                         linestyle=ls, zorder=zorder)
    ax.add_patch(c)

def draw_rect(ax, x, y, w, h, lw=LW_THICK, color=C_OUT, fc='white', zorder=3):
    r = mpatches.Rectangle((x, y), w, h, lw=lw, edgecolor=color, facecolor=fc, zorder=zorder)
    ax.add_patch(r)

def leader(ax, xfrom, yfrom, xto, yto, text, fontsize=6, color=C_DIM):
    ax.annotate(text, xy=(xto, yto), xytext=(xfrom, yfrom),
                fontsize=fontsize, color=color,
                arrowprops=dict(arrowstyle='->', linestyle=':', color=color, lw=0.7))

def bolt_holes(ax, cx, cy, bc_r, n, d_r, color=C_OUT, lw=LW_MED, angle_offset=22.5):
    for i in range(n):
        angle = np.radians(angle_offset + i * 360/n)
        bx = cx + bc_r * np.cos(angle)
        by = cy + bc_r * np.sin(angle)
        draw_circle(ax, bx, by, d_r, lw=lw, color=color)

def hatch_region(ax, patch, spacing=3, angle=45, color='#AAAAAA', lw=0.5):
    """Hatch inside an existing Rectangle patch using data coordinates."""
    # Use data-coordinate bounds directly (get_extents returns display coords
    # which are invalid before rendering and cause misplaced hatch lines)
    x, y = patch.get_xy()
    w = patch.get_width()
    h = patch.get_height()
    angle_r = np.radians(angle)
    diag = np.sqrt(w**2 + h**2) + spacing
    n = int(diag / spacing) + 2
    cx_h, cy_h = x + w/2, y + h/2
    for i in range(-n, n+1):
        off = i * spacing
        dx = diag * np.cos(angle_r)
        dy = diag * np.sin(angle_r)
        px0 = cx_h + off * np.cos(angle_r + np.pi/2) - dx/2
        py0 = cy_h + off * np.sin(angle_r + np.pi/2) - dy/2
        ax.plot([px0, px0+dx], [py0, py0+dy],
                color=color, lw=lw, clip_path=patch, clip_on=True)

def title_block(ax, fig_w, fig_h, sheet_n, sheet_total, title1, title2,
                scale_str, project='THE BIG SHOEBOX PROJECT',
                series='TBS-TSB', position='bottom'):
    # Outer border — zorder=0 so content drawn later is not hidden
    draw_rect(ax, 5, 5, fig_w-10, fig_h-10, lw=1.5, color='black', fc='white', zorder=0)
    # Title block box
    tb_w, tb_h = 215, 75
    tb_x = fig_w - tb_w - 5
    if position == 'top':
        tb_y = fig_h - tb_h - 5
    else:
        tb_y = 5
    draw_rect(ax, tb_x, tb_y, tb_w, tb_h, lw=0.5, color='black', fc='#F5F5F5')
    cx_tb = tb_x + tb_w / 2
    # Row positions relative to tb_y
    ax.text(cx_tb, tb_y + 68, project, ha='center', fontsize=9, fontweight='bold', color='black')
    ax.text(cx_tb, tb_y + 60, title1, ha='center', fontsize=7.5, color='black')
    ax.text(cx_tb, tb_y + 52, title2, ha='center', fontsize=7, color='black')
    # Divider between title area and info fields
    ax.plot([tb_x, tb_x+tb_w], [tb_y + 49, tb_y + 49], color='black', lw=0.3)
    val_x = tb_x + 68  # left-aligned value column
    ax.text(tb_x+8, tb_y + 43, 'DRAWING:', fontsize=6, color='black')
    ax.text(val_x, tb_y + 43, f'{series}-0{sheet_n}', fontsize=6, fontweight='bold', color='black')
    ax.text(tb_x+8, tb_y + 36, 'SHEET:', fontsize=6, color='black')
    ax.text(val_x, tb_y + 36, f'{sheet_n} OF {sheet_total}', fontsize=6, fontweight='bold', color='black')
    ax.text(tb_x+8, tb_y + 29, 'SCALE:', fontsize=6, color='black')
    ax.text(val_x, tb_y + 29, scale_str, fontsize=6, fontweight='bold', color='black')
    ax.text(tb_x+8, tb_y + 22, 'UNITS:', fontsize=6, color='black')
    ax.text(val_x, tb_y + 22, 'ALL DIMENSIONS IN mm', fontsize=6, fontweight='bold', color='black')
    ax.text(tb_x+8, tb_y + 15, 'TOLERANCE:', fontsize=6, color='black')
    ax.text(val_x, tb_y + 15, '±0.25 UNLESS NOTED', fontsize=6, color='black')
    ax.text(tb_x+8, tb_y + 8, 'MATERIAL:', fontsize=6, color='black')
    ax.text(val_x, tb_y + 8, 'Al 6061-T6 HARD ANODIZE', fontsize=6, color='black')
    # Copyright — inside the box
    ax.plot([tb_x, tb_x+tb_w], [tb_y + 4, tb_y + 4], color='black', lw=0.3)
    ax.text(cx_tb, tb_y + 1, '\u00a9 2026 Alvin Richards \u2014 GNU AGPLv3',
            ha='center', fontsize=5, color='black', style='italic')


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — Assembly overview & Outer Adapter Frame
# ═══════════════════════════════════════════════════════════════════════════════

FW, FH = 700, 500
fig1, ax1 = plt.subplots(figsize=(FW/25.4*0.9, FH/25.4*0.9))
fig1.patch.set_facecolor('white')
ax1.set_facecolor('white')
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_xlim(0, FW)
ax1.set_ylim(0, FH)

title_block(ax1, FW, FH, 1, 3,
            'TILT-SWING FRONT BOARD MECHANISM',
            'SHEET 1 — OVERVIEW & OUTER ADAPTER FRAME (TSB-01)',
            'AS NOTED')

# ── Section header lines ──────────────────────────────────────────────────────
def section_label(ax, x, y, text):
    ax.text(x, y, text, fontsize=7.5, fontweight='bold', color='black')
    ax.plot([x, x+200], [y-3, y-3], color='black', lw=0.7)

section_label(ax1, 10, 490, 'PANEL A — FULL ASSEMBLY (1:8)')
section_label(ax1, 170, 490, 'PANEL B — TSB-01 EXTERIOR FACE (1:8)')
section_label(ax1, 330, 490, 'PANEL C — TSB-01 INTERIOR FACE (1:8)')

SC = 1/8
def s1(mm): return mm * SC

# ───────────────────────────────────────────────
# PANEL A: Full assembly front view (center 85, 340)
# ───────────────────────────────────────────────
cx_a, cy_a = 85, 330
hw = s1(PL_OD/2)

# Outer adapter frame (TSB-01) — aluminium, slightly thicker than normal plates
p = mpatches.Rectangle((cx_a - hw, cy_a - hw), s1(PL_OD), s1(PL_OD),
                        lw=LW_THICK, edgecolor=C_OUT, facecolor=C_ALUM, zorder=3)
ax1.add_patch(p)

# Central bore
draw_circle(ax1, cx_a, cy_a, s1(TSB01_BORE/2), lw=LW_MED, color=C_OUT, fill=True, fc='white', zorder=4)

# Inner carrier plate (TSB-02) — circular, darker Al
draw_circle(ax1, cx_a, cy_a, s1(CARR_OD/2), lw=LW_THICK, color=C_OUT, fill=True, fc='#C0C0C0', zorder=5)

# Pinhole bore (cone opening)
draw_circle(ax1, cx_a, cy_a, s1(PH_BORE/2), lw=LW_MED, color=C_OUT, fill=True, fc=C_ALUM, zorder=6)

# Pinhole disc counterbore
draw_circle(ax1, cx_a, cy_a, s1(PH_CB_D/2), lw=LW_MED, color=C_HID, ls='--', zorder=7)
draw_circle(ax1, cx_a, cy_a, s1(PH_DISC_D/2), lw=0.7, color=C_OUT, fill=True, fc='#606060', zorder=8)

# 4 adjustment knob positions (visible as circles on the outer frame)
for angle_deg in [90, 0, 270, 180]:
    kx = cx_a + s1(ADJ_PCD/2) * np.cos(np.radians(angle_deg))
    ky = cy_a + s1(ADJ_PCD/2) * np.sin(np.radians(angle_deg))
    draw_circle(ax1, kx, ky, s1(KNOB_D/2), lw=LW_MED, color=C_OUT, fill=True,
                fc='#505050' if angle_deg in [90,270] else '#A0A0A0', zorder=6)
    # Knurling hint
    draw_circle(ax1, kx, ky, s1(KNOB_D/2)*0.75, lw=0.4, color=C_HID, ls=':', zorder=7)

# Axis labels on knobs
for angle_deg, label, col in [(90,'T+','white'),(270,'T−','white'),(0,'S+','black'),(180,'S−','black')]:
    kx = cx_a + s1(ADJ_PCD/2) * np.cos(np.radians(angle_deg))
    ky = cy_a + s1(ADJ_PCD/2) * np.sin(np.radians(angle_deg))
    ax1.text(kx, ky, label, ha='center', va='center', fontsize=4.5,
             fontweight='bold', color=col, zorder=9)

# Bolt holes
bolt_holes(ax1, cx_a, cy_a, s1(BOLT_BC/2), BOLT_N, s1(BOLT_D/2), color=C_OUT, lw=LW_MED)

# Dowel holes
for sign in [-1, 1]:
    draw_circle(ax1, cx_a + sign*s1(DWL_OFF), cy_a, s1(DWL_D/2), lw=LW_MED, color=C_OUT)

# Bellows flange circle (dashed)
draw_circle(ax1, cx_a, cy_a, s1(BELL_OUT_PCD/2), lw=LW_THIN, color='#606060', ls='--')

draw_cl(ax1, cx_a, cy_a, hw*1.15)

# Dimension: carrier OD
draw_dim_h(ax1, cx_a - s1(CARR_OD/2), cx_a + s1(CARR_OD/2), cy_a - hw - 12,
           'Ø320 CARRIER', above=False, fontsize=5)
draw_dim_h(ax1, cx_a - hw, cx_a + hw, cy_a + hw + 12, '600', above=True, fontsize=5.5)

ax1.text(cx_a, cy_a - hw - 25, 'PANEL A — ASSEMBLY (1:8)\nTSB-01 outer frame + TSB-02 carrier\nBlack knobs = TILT  Silver knobs = SWING',
         ha='center', fontsize=5, color='#333333', style='italic')

# ───────────────────────────────────────────────
# PANEL B: TSB-01 Exterior (container-wall-facing) face
# center 255, 330
# ───────────────────────────────────────────────
cx_b, cy_b = 258, 330

p2 = mpatches.Rectangle((cx_b - hw, cy_b - hw), s1(PL_OD), s1(PL_OD),
                         lw=LW_THICK, edgecolor=C_OUT, facecolor=C_ALUM, zorder=3)
ax1.add_patch(p2)

# Central bore (larger — Ø380)
draw_circle(ax1, cx_b, cy_b, s1(TSB01_BORE/2), lw=LW_THICK, color=C_OUT, fill=True, fc='white', zorder=4)

# Seal groove Ø420
draw_circle(ax1, cx_b, cy_b, s1(SEAL_D/2), lw=LW_MED, color=C_GASKT, ls='--')
# Light-trap rebate (dashed square)
tr = s1(TRAP_SQ/2)
ax1.plot([cx_b-tr, cx_b+tr, cx_b+tr, cx_b-tr, cx_b-tr],
         [cy_b-tr, cy_b-tr, cy_b+tr, cy_b+tr, cy_b-tr],
         color=C_HID, lw=LW_THIN, ls='--')

# Bolt circle
draw_circle(ax1, cx_b, cy_b, s1(BOLT_BC/2), lw=0.4, color=C_HID, ls=':')
bolt_holes(ax1, cx_b, cy_b, s1(BOLT_BC/2), BOLT_N, s1(BOLT_D/2))

# Dowel holes
for sign in [-1, 1]:
    draw_circle(ax1, cx_b + sign*s1(DWL_OFF), cy_b, s1(DWL_D/2), lw=LW_MED, color=C_OUT)

# 4 adjustment screw positions (seen as circles on face)
for angle_deg in [90, 0, 270, 180]:
    ax_x = cx_b + s1(ADJ_PCD/2) * np.cos(np.radians(angle_deg))
    ax_y = cy_b + s1(ADJ_PCD/2) * np.sin(np.radians(angle_deg))
    draw_circle(ax1, ax_x, ax_y, s1(BUSH_OD/2), lw=LW_MED, color=C_OUT, fill=True, fc=C_DELR, zorder=5)
    draw_circle(ax1, ax_x, ax_y, s1(ADJ_D/2), lw=0.7, color=C_OUT, fill=True, fc='white', zorder=6)

draw_cl(ax1, cx_b, cy_b, hw*1.15)

# Leaders
leader(ax1, cx_b + 30, cy_b + 45, cx_b + s1(TSB01_BORE/2)*0.7, cy_b + s1(TSB01_BORE/2)*0.7,
       'Ø380 BORE\n(PANEL B VIEW)', fontsize=4.8)
leader(ax1, cx_b + 22, cy_b - 38, cx_b + s1(SEAL_D/2)*0.65, cy_b - s1(SEAL_D/2)*0.65,
       'Ø420 SEAL\nGROOVE\n3×3 DEEP', fontsize=4.5)
leader(ax1, cx_b + s1(ADJ_PCD/2) + 14, cy_b + 4, cx_b + s1(ADJ_PCD/2) + s1(BUSH_OD/2), cy_b,
       'M22×1.0\nBUSHING\n(4 OFF)', fontsize=4.5)
leader(ax1, cx_b + 16, cy_b + 28, cx_b + s1(BOLT_BC/2)*0.65, cy_b + s1(BOLT_BC/2)*0.65,
       'Ø540 B.C.\n8×M12\nCLR', fontsize=4.5)
ax1.text(cx_b, cy_b - hw - 12, 'PANEL B — TSB-01 EXTERIOR (1:8)\n(Same bolt/dowel/seal interface\nas standard pinhole plate)',
         ha='center', fontsize=5, color='#333333', style='italic')

# ───────────────────────────────────────────────
# PANEL C: TSB-01 Interior (container-facing) face
# center 420, 330
# ───────────────────────────────────────────────
cx_c, cy_c = 425, 330

p3 = mpatches.Rectangle((cx_c - hw, cy_c - hw), s1(PL_OD), s1(PL_OD),
                         lw=LW_THICK, edgecolor=C_OUT, facecolor=C_ALUM, zorder=3)
ax1.add_patch(p3)

# Central bearing pocket (Ø80 H7)
draw_circle(ax1, cx_c, cy_c, s1(BRG_SEAT_D/2), lw=LW_THICK, color=C_OUT, fill=True, fc=C_BEAR, zorder=4)
# Bearing bore (Ø50)
draw_circle(ax1, cx_c, cy_c, s1(BRG_ID/2), lw=LW_MED, color=C_OUT, fill=True, fc='white', zorder=5)

# Labyrinth steps (3 concentric dashed circles)
for d, ls_str in [(LAB_D1,'--'),(LAB_D2,'-.'),(LAB_D3,':')]:
    draw_circle(ax1, cx_c, cy_c, s1(d/2), lw=LW_THIN, color='#555555', ls=ls_str)

# 4 × M22 adjustment bushing holes (interior side — seen from behind)
for angle_deg in [90, 0, 270, 180]:
    ax_x = cx_c + s1(ADJ_PCD/2) * np.cos(np.radians(angle_deg))
    ax_y = cy_c + s1(ADJ_PCD/2) * np.sin(np.radians(angle_deg))
    draw_circle(ax1, ax_x, ax_y, s1(BUSH_OD/2), lw=LW_MED, color=C_OUT, fill=True, fc=C_DELR, zorder=5)
    draw_circle(ax1, ax_x, ax_y, s1(ADJ_D/2), lw=0.7, color=C_OUT, fill=True, fc='white', zorder=6)

# 6 × M6 bellows flange bolts on Ø375
for i in range(6):
    ang = np.radians(i*60)
    bx = cx_c + s1(BELL_OUT_PCD/2) * np.cos(ang)
    by = cy_c + s1(BELL_OUT_PCD/2) * np.sin(ang)
    draw_circle(ax1, bx, by, s1(3.5), lw=LW_THIN, color=C_OUT, fill=True, fc='#888888', zorder=5)

draw_cl(ax1, cx_c, cy_c, hw*1.15)

leader(ax1, cx_c - 18, cy_c + 12, cx_c - s1(BRG_SEAT_D/2)*0.7, cy_c + s1(BRG_SEAT_D/2)*0.7,
       'Ø80 H7 BEARING\nSEAT × 50 DEEP', fontsize=4.8)
leader(ax1, cx_c + 25, cy_c + 28, cx_c + s1(BELL_OUT_PCD/2)*0.6, cy_c + s1(BELL_OUT_PCD/2)*0.6,
       '6×M6 ON\nØ375 PCD\n(BELLOWS)', fontsize=4.5)
leader(ax1, cx_c + 20, cy_c - 35, cx_c + s1(LAB_D3/2)*0.65, cy_c - s1(LAB_D3/2)*0.65,
       '3-STEP\nLABYRINTH\nØ382/390/400\n5 DEEP EACH', fontsize=4.3)

ax1.text(cx_c, cy_c - hw - 12, 'PANEL C — TSB-01 INTERIOR (1:8)\n(Bearing pocket + labyrinth + bellows attach)',
         ha='center', fontsize=5, color='#333333', style='italic')

# ───────────────────────────────────────────────
# PANEL D: Section A-A — separate X/Y scales so 600×40mm section is readable
# Horizontal: 1:5  →  600mm = 120 units
# Vertical:   1:1  →  40mm frame + 25mm carrier + 35mm bearing shank = 100 units
# ───────────────────────────────────────────────
def sx(mm): return mm / 5.0   # horizontal 1:5
def sy(mm): return mm * 1.0   # vertical 1:1

ax1.text(10, 222, 'PANEL D — SECTION A-A  (HORIZ 1:5 / VERT 1:1  — thickness exaggerated for clarity)',
         fontsize=7, fontweight='bold')
ax1.plot([10, 490], [219, 219], color='black', lw=0.7)

# Centre section at x=250, top of frame at y=210
cx_d = 250
frame_top = 210   # top of TSB-01 frame (exterior/scene face)

# Heights in drawing units (1:1 vertical)
fh = sy(TSB01_THICK)   # frame height = 40
ch = sy(CARR_THICK)    # carrier height = 25
bh = sy(BRG_W)         # bearing height = 46

# Y positions (drawing downward = interior side)
frame_y_top = frame_top
frame_y_bot = frame_top - fh          # interior face of TSB-01
carrier_y_top = frame_y_bot           # carrier sits flush on interior face
carrier_y_bot = carrier_y_top - ch
seat_y_top = frame_y_bot              # bearing pocket starts at interior face
seat_y_bot = seat_y_top + sy(BRG_SEAT_DEP)   # pocket goes INTO frame (upward)

# Frame footprint — left wing
left_wing_w = sx((PL_OD - TSB01_BORE) / 2)
right_x = cx_d + sx(PL_OD/2)
left_x  = cx_d - sx(PL_OD/2)
bore_hw_d = sx(TSB01_BORE/2)

# Left frame wing
lw_p = mpatches.Rectangle((left_x, frame_y_bot), left_wing_w, fh,
                            lw=LW_THICK, edgecolor=C_OUT, facecolor=C_ALUM,
                            hatch='////', zorder=3)
ax1.add_patch(lw_p)
# Right frame wing
rw_p = mpatches.Rectangle((cx_d + bore_hw_d, frame_y_bot), left_wing_w, fh,
                            lw=LW_THICK, edgecolor=C_OUT, facecolor=C_ALUM,
                            hatch='////', zorder=3)
ax1.add_patch(rw_p)

# Bore walls (vertical lines at bore edges)
ax1.plot([cx_d - bore_hw_d, cx_d - bore_hw_d], [frame_y_bot, frame_y_top], color=C_OUT, lw=LW_MED)
ax1.plot([cx_d + bore_hw_d, cx_d + bore_hw_d], [frame_y_bot, frame_y_top], color=C_OUT, lw=LW_MED)

# Top and bottom face lines (full width)
ax1.plot([left_x, right_x], [frame_y_top, frame_y_top], color=C_OUT, lw=LW_THICK)
ax1.plot([left_x, cx_d - bore_hw_d], [frame_y_bot, frame_y_bot], color=C_OUT, lw=LW_THICK)
ax1.plot([cx_d + bore_hw_d, right_x], [frame_y_bot, frame_y_bot], color=C_OUT, lw=LW_THICK)

# Neoprene seal groove (exterior face, at ±SEAL_D/2 from center)
for sgn in [-1, 1]:
    gx = cx_d + sgn * sx(SEAL_D/2) - sgn * sx(SEAL_W/2)
    sg_p = mpatches.Rectangle((gx - sx(SEAL_W/2), frame_y_top - sy(SEAL_DEP)),
                                sx(SEAL_W), sy(SEAL_DEP),
                                lw=0.5, edgecolor=C_OUT, facecolor=C_GASKT, zorder=5)
    ax1.add_patch(sg_p)

# Light-trap rebate (exterior face)
for sgn in [-1, 1]:
    tx2 = cx_d + sgn * sx(TRAP_SQ/2) - sgn * sx(5)
    tr_p = mpatches.Rectangle((tx2 - sx(2.5), frame_y_top - sy(5)),
                                sx(5), sy(5),
                                lw=0.5, edgecolor=C_OUT, facecolor='white', zorder=4)
    ax1.add_patch(tr_p)

# Bearing seat pocket (opens on interior face, goes INTO frame)
seat_hw = sx(BRG_SEAT_D/2)
seat_dep_d = sy(BRG_SEAT_DEP)
ax1.plot([cx_d - seat_hw, cx_d - seat_hw], [frame_y_bot, frame_y_bot + seat_dep_d],
         color=C_OUT, lw=LW_MED)
ax1.plot([cx_d + seat_hw, cx_d + seat_hw], [frame_y_bot, frame_y_bot + seat_dep_d],
         color=C_OUT, lw=LW_MED)
ax1.plot([cx_d - seat_hw, cx_d + seat_hw], [frame_y_bot + seat_dep_d, frame_y_bot + seat_dep_d],
         color=C_OUT, lw=LW_MED)

# GE50 Bearing in section (in pocket)
brg_hw_d = sx(BRG_OD/2)
brg_wall = sx(7)
brg_top = frame_y_bot
brg_bot = brg_top + sy(BRG_W/2)

# Outer ring (two side walls, hatched)
for sgn in [-1, 1]:
    bx0 = cx_d + sgn * (brg_hw_d - brg_wall)
    br_p = mpatches.Rectangle((bx0 - brg_wall if sgn < 0 else bx0, brg_top),
                                brg_wall, sy(BRG_W/2),
                                lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR,
                                hatch='\\\\', zorder=4)
    ax1.add_patch(br_p)
# Outer ring top cap
br_top = mpatches.Rectangle((cx_d - brg_hw_d, brg_top), sx(BRG_OD), sy(4),
                              lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR, hatch='\\\\', zorder=4)
ax1.add_patch(br_top)

# Inner ring
ir_hw = sx(BRG_ID/2)
ir_wall = sx(5)
for sgn in [-1, 1]:
    ix0 = cx_d + sgn * (ir_hw - ir_wall)
    ir_p = mpatches.Rectangle((ix0 - ir_wall if sgn < 0 else ix0, brg_top + sy(4)),
                                ir_wall, sy(BRG_W/2 - 4),
                                lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR,
                                hatch='---', zorder=5)
    ax1.add_patch(ir_p)

# TSB-02 Carrier plate
carr_hw_d = sx(CARR_OD/2)
ph_hw_d   = sx(PH_BORE/2)
# Carrier wings (either side of pinhole bore)
for sgn in [-1, 1]:
    x0 = cx_d + sgn * ph_hw_d
    w0 = carr_hw_d - ph_hw_d
    cp = mpatches.Rectangle((x0 if sgn > 0 else cx_d - carr_hw_d,
                              carrier_y_bot),
                              w0, ch,
                              lw=LW_THICK, edgecolor=C_OUT, facecolor='#C0C0C0',
                              hatch='...', zorder=3)
    ax1.add_patch(cp)
# Carrier face lines
ax1.plot([cx_d - carr_hw_d, cx_d - ph_hw_d], [carrier_y_top, carrier_y_top], color=C_OUT, lw=LW_MED)
ax1.plot([cx_d + ph_hw_d, cx_d + carr_hw_d], [carrier_y_top, carrier_y_top], color=C_OUT, lw=LW_MED)
ax1.plot([cx_d - carr_hw_d, cx_d + carr_hw_d], [carrier_y_bot, carrier_y_bot], color=C_OUT, lw=LW_THICK)
ax1.plot([cx_d - carr_hw_d, cx_d - carr_hw_d], [carrier_y_bot, carrier_y_top], color=C_OUT, lw=LW_THICK)
ax1.plot([cx_d + carr_hw_d, cx_d + carr_hw_d], [carrier_y_bot, carrier_y_top], color=C_OUT, lw=LW_THICK)
ax1.plot([cx_d - ph_hw_d, cx_d - ph_hw_d], [carrier_y_bot, carrier_y_top], color=C_OUT, lw=LW_MED)
ax1.plot([cx_d + ph_hw_d, cx_d + ph_hw_d], [carrier_y_bot, carrier_y_top], color=C_OUT, lw=LW_MED)

# M8 adjustment screw (one side — right)
adj_x = cx_d + sx(ADJ_PCD/2)
adj_hw_d = sx(ADJ_D/2)
# Bushing
bush_d = mpatches.Rectangle((adj_x - sx(BUSH_OD/2), frame_y_bot),
                              sx(BUSH_OD), sy(BUSH_L),
                              lw=LW_THIN, edgecolor=C_OUT, facecolor=C_DELR, zorder=4)
ax1.add_patch(bush_d)
# Screw shaft through bushing + frame
screw_d = mpatches.Rectangle((adj_x - adj_hw_d, frame_y_bot),
                               sx(ADJ_D), fh,
                               lw=0.8, edgecolor=C_OUT, facecolor=C_STEEL, zorder=5)
ax1.add_patch(screw_d)
# Ø8 ball (at carrier rim)
ball_y_d = (carrier_y_top + carrier_y_bot) / 2
ax1.plot(adj_x, ball_y_d, 'o', ms=sx(BALL_D), color=C_BEAR, mec=C_OUT, mew=0.7, zorder=6)

# Bellows schematic (right side, between frame interior face and carrier)
bell_x_out = cx_d + sx(BELL_OUT_PCD/2)
bell_x_in  = cx_d + sx(BELL_IN_PCD/2)
bell_y_top = frame_y_bot
bell_y_bot = carrier_y_top
n_p = BELL_PLEATS
ph2 = (bell_y_top - bell_y_bot) / n_p   # note: y_top > y_bot here? Let's check
# frame_y_bot is lower y value (interior is down), carrier_y_top == frame_y_bot
# Actually carrier sits below the frame, so carrier_y_top = frame_y_bot
# and bellows connects frame interior face to carrier exterior (scene) face
# bellows goes from frame_y_bot (frame interior) to carrier_y_top (carrier exterior = same point)
# The carrier hangs below the frame via the bearing shank. The bellows fills the gap.
# Actually in this orientation: the bellows spans AROUND the outside of the assembly
# spanning vertically from the frame face down to the carrier edge.
# But in section the bellows would be at the radii between ~BELL_IN_PCD/2 and BELL_OUT_PCD/2
# and spanning from the frame interior face down to the carrier exterior face.
# The carrier_y_top equals frame_y_bot only if there's no gap. With a bearing, there IS a gap.
# The bearing width is 46mm and the carrier shank goes INTO the bearing.
# The carrier exterior face (scene side) is below the frame exterior face by ~BRG_SEAT_DEP + CARR_THICK gap
# For the section, let's show the bellows at the outer edge spanning from frame to carrier
bell_span_top = frame_y_bot
bell_span_bot = carrier_y_bot
pleat_step = (bell_span_bot - bell_span_top) / n_p
for i in range(n_p):
    p_y = bell_span_top + i * pleat_step
    ax1.plot([bell_x_in, bell_x_out], [p_y, p_y + pleat_step*0.5], color=C_BELL, lw=1.5, zorder=6)
    ax1.plot([bell_x_out, bell_x_in], [p_y + pleat_step*0.5, p_y + pleat_step], color=C_BELL, lw=1.5, zorder=6)

# Centreline
ax1.plot([cx_d, cx_d], [carrier_y_bot - 10, frame_y_top + 10],
         color=C_CL, lw=LW_THIN, linestyle=(0, (6, 2, 1, 2)))

# Break lines on sides (zig-zag) to indicate plate continues
for side_x in [left_x - 2, right_x + 2]:
    for y_brk in [frame_y_top - 5, frame_y_bot + 2]:
        ax1.plot([side_x - 3, side_x + 3, side_x - 3, side_x + 3],
                 [y_brk, y_brk - 3, y_brk - 6, y_brk - 9],
                 color='black', lw=1.0)

# Dimensions
draw_dim_h(ax1, left_x, right_x, frame_y_top + 12, '600 (FULL WIDTH)',
           above=True, fontsize=5, scale=1.0)
draw_dim_v(ax1, left_x - 10, frame_y_bot, frame_y_top, '40',
           right=False, fontsize=5, scale=1.0)
draw_dim_v(ax1, left_x - 10, carrier_y_bot, carrier_y_top, '25',
           right=False, fontsize=5, scale=1.0)
draw_dim_h(ax1, cx_d - bore_hw_d, cx_d + bore_hw_d, carrier_y_bot - 10,
           f'Ø{TSB01_BORE} BORE', above=False, fontsize=5, scale=1.0)

# Leaders
leader(ax1, cx_d + 60, frame_y_bot + seat_dep_d/2,
       cx_d + seat_hw + 2, frame_y_bot + seat_dep_d/2,
       'Ø80 H7 BEARING\nPOCKET × 50', fontsize=4.8)
leader(ax1, cx_d + 65, carrier_y_bot + ch/2,
       cx_d + carr_hw_d + 2, carrier_y_bot + ch/2,
       'TSB-02 CARRIER\nØ320 × 25 Al', fontsize=4.8)
leader(ax1, adj_x + 18, frame_y_bot + sy(BUSH_L)/2,
       adj_x + sx(BUSH_OD/2), frame_y_bot + sy(BUSH_L)/2,
       'M8 SCREW\n+ DELRIN\nBUSHING', fontsize=4.5)
leader(ax1, bell_x_out + 18, (bell_span_top + bell_span_bot)/2,
       bell_x_out + 2, (bell_span_top + bell_span_bot)/2,
       'BELLOWS\nTSB-10', fontsize=4.5)

ax1.text(cx_d, carrier_y_bot - 20, '← SCENE (EXTERIOR)    INTERIOR (CONTAINER) →',
         ha='center', fontsize=5, color='#555555')
ax1.text(cx_d, frame_y_top + 25, 'SECTION A-A  (HORIZONTAL SCALE 1:5 / VERTICAL SCALE 1:1)',
         ha='center', fontsize=5, color='#333333', style='italic')

out1 = 'diagrams/tilt-swing-board-sheet1.png'
os.makedirs(SVG_DIR, exist_ok=True)
fig1.savefig(out1, dpi=150, bbox_inches='tight', facecolor='white')
fig1.savefig(svg_path(out1), bbox_inches="tight", facecolor='white')
plt.close(fig1)
print(f'  → {out1}  Done.')


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Carrier Plate, Bearing & Adjustment Mechanism
# ═══════════════════════════════════════════════════════════════════════════════

fig2, ax2 = plt.subplots(figsize=(FW/25.4*0.9, FH/25.4*0.9))
fig2.patch.set_facecolor('white')
ax2.set_facecolor('white')
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_xlim(0, FW)
ax2.set_ylim(0, FH)

title_block(ax2, FW, FH, 2, 3,
            'TILT-SWING FRONT BOARD MECHANISM',
            'SHEET 2 — INNER CARRIER (TSB-02), BEARING (TSB-03) & ADJUSTMENT',
            'AS NOTED')

SC2 = 1/2
def s2(mm): return mm * SC2

# ── PANEL A: TSB-02 front (exterior) face at 1:2 ──────────────────────────────
ax2.text(15, 490, 'PANEL A — TSB-02 FRONT FACE (1:2)', fontsize=7.5, fontweight='bold')
ax2.plot([15, 330], [487, 487], color='black', lw=0.7)

cx2a, cy2a = 120, 355

# Circular carrier plate
carr_p = mpatches.Circle((cx2a, cy2a), s2(CARR_OD/2),
                          lw=LW_THICK, edgecolor=C_OUT, facecolor=C_ALUM, zorder=3)
ax2.add_patch(carr_p)

# Taper bore (Ø90)
draw_circle(ax2, cx2a, cy2a, s2(PH_BORE/2), lw=LW_MED, color=C_OUT, fill=True, fc='white', zorder=4)

# Counterbore Ø52
draw_circle(ax2, cx2a, cy2a, s2(PH_CB_D/2), lw=LW_MED, color=C_HID, ls='--', zorder=5)
# Pinhole disc Ø50
draw_circle(ax2, cx2a, cy2a, s2(PH_DISC_D/2), lw=LW_THICK, color=C_OUT, fill=True, fc='#707070', zorder=6)
# Pinhole (tiny)
draw_circle(ax2, cx2a, cy2a, 0.5, lw=0.5, color='white', fill=True, fc='white', zorder=7)

# 4 × Ball socket inserts on Ø260
for angle_deg in [90, 0, 270, 180]:
    sx = cx2a + s2(SOCK_PCD/2) * np.cos(np.radians(angle_deg))
    sy = cy2a + s2(SOCK_PCD/2) * np.sin(np.radians(angle_deg))
    draw_circle(ax2, sx, sy, s2(16/2), lw=LW_MED, color=C_OUT, fill=True, fc=C_BEAR, zorder=5)
    draw_circle(ax2, sx, sy, s2(BALL_D/2), lw=0.7, color=C_OUT, fill=True, fc='#D0D0D0', zorder=6)

# 6 × M6 bellows bolts on Ø310
for i in range(6):
    ang = np.radians(30 + i*60)
    bx = cx2a + s2(BELL_IN_PCD/2) * np.cos(ang)
    by = cy2a + s2(BELL_IN_PCD/2) * np.sin(ang)
    draw_circle(ax2, bx, by, s2(3.5), lw=LW_THIN, color=C_OUT, fill=True, fc='#888888', zorder=5)

# Bolt circle ref
draw_circle(ax2, cx2a, cy2a, s2(SOCK_PCD/2), lw=0.4, color=C_HID, ls=':')
draw_circle(ax2, cx2a, cy2a, s2(BELL_IN_PCD/2), lw=0.4, color='#999999', ls=':')

draw_cl(ax2, cx2a, cy2a, s2(CARR_OD/2)*1.2)

# Dims
draw_dim_h(ax2, cx2a - s2(CARR_OD/2), cx2a + s2(CARR_OD/2),
           cy2a - s2(CARR_OD/2) - 14, 'Ø320', above=False, fontsize=5.5, scale=1.5)
draw_dim_h(ax2, cx2a - s2(PH_BORE/2), cx2a + s2(PH_BORE/2),
           cy2a + s2(CARR_OD/2) + 10, 'Ø90 CONE', above=True, fontsize=5, scale=1.5)

leader(ax2, cx2a + 55, cy2a + 30, cx2a + s2(PH_CB_D/2) * 0.7, cy2a + s2(PH_CB_D/2) * 0.7,
       'Ø52 × 3 DEEP\nCOUNTERBORE\n(DISC SEAT)', fontsize=5)
leader(ax2, cx2a + 60, cy2a - 22, cx2a + s2(SOCK_PCD/2) * np.cos(np.radians(-30)),
       cy2a + s2(SOCK_PCD/2) * np.sin(np.radians(-30)),
       '4×Ø16 H7\nSOCKET INSERT\nON Ø260 PCD', fontsize=5)
leader(ax2, cx2a - 65, cy2a + 35, cx2a + s2(BELL_IN_PCD/2) * np.cos(np.radians(130)),
       cy2a + s2(BELL_IN_PCD/2) * np.sin(np.radians(130)),
       '6×M6 ON\nØ310 PCD\n(BELLOWS)', fontsize=5)

ax2.text(cx2a, cy2a - s2(CARR_OD/2) - 28, 'PANEL A — TSB-02 FRONT FACE (1:2)\nExterior / scene-facing side',
         ha='center', fontsize=5, style='italic', color='#333333')

# ── PANEL B: TSB-02 rear face at 1:2 ─────────────────────────────────────────
ax2.text(340, 490, 'PANEL B — TSB-02 REAR FACE (1:2)', fontsize=7.5, fontweight='bold')
ax2.plot([340, 640], [487, 487], color='black', lw=0.7)

cx2b, cy2b = 490, 355

carr_p2 = mpatches.Circle((cx2b, cy2b), s2(CARR_OD/2),
                           lw=LW_THICK, edgecolor=C_OUT, facecolor='#C0C0C0', zorder=3)
ax2.add_patch(carr_p2)

# Bearing shank boss (Ø50 k5) — raised circular boss on rear face
shank_p = mpatches.Circle((cx2b, cy2b), s2(BRG_SHANK_D/2),
                           lw=LW_THICK, edgecolor=C_OUT, facecolor=C_BEAR, zorder=4)
ax2.add_patch(shank_p)

# M16 tapped central hole
draw_circle(ax2, cx2b, cy2b, s2(8), lw=LW_MED, color=C_OUT, fill=True, fc='white', zorder=5)

# 4 × socket insert bores (Ø16 H7) — same PCD
for angle_deg in [90, 0, 270, 180]:
    sx = cx2b + s2(SOCK_PCD/2) * np.cos(np.radians(angle_deg))
    sy = cy2b + s2(SOCK_PCD/2) * np.sin(np.radians(angle_deg))
    draw_circle(ax2, sx, sy, s2(16/2), lw=LW_MED, color=C_OUT, fill=True, fc=C_BEAR, zorder=5)

# Bellows groove Ø290
draw_circle(ax2, cx2b, cy2b, s2(BELL_ID/2), lw=LW_MED, color=C_GASKT, ls='--')

draw_cl(ax2, cx2b, cy2b, s2(CARR_OD/2)*1.2)

leader(ax2, cx2b + 60, cy2b + 30, cx2b + s2(BRG_SHANK_D/2)*0.7, cy2b + s2(BRG_SHANK_D/2)*0.7,
       'Ø50 k5 SHANK\n× 35 LONG\n(BEARING INNER)', fontsize=5)
leader(ax2, cx2b - 58, cy2b + 5, cx2b - s2(BELL_ID/2)*0.7, cy2b,
       'Ø290 BELLOWS\nGROOVE\n4 WIDE × 3 DEEP', fontsize=5)
leader(ax2, cx2b + 50, cy2b - 20, cx2b + s2(SOCK_PCD/2)*np.cos(np.radians(-45)),
       cy2b + s2(SOCK_PCD/2)*np.sin(np.radians(-45)),
       '4×Ø16 H7\nINSERT BORES\n(REAR SIDE)', fontsize=5)

ax2.text(cx2b, cy2b - s2(CARR_OD/2) - 28, 'PANEL B — TSB-02 REAR FACE (1:2)\nBearing-side / interior',
         ha='center', fontsize=5, style='italic', color='#333333')

# ── PANEL C: Bearing section detail (1:1) ─────────────────────────────────────
ax2.text(15, 215, 'PANEL C — GE50-DO-2RS BEARING SECTION (1:1)', fontsize=7.5, fontweight='bold')
ax2.plot([15, 345], [212, 212], color='black', lw=0.7)

cx2c, cy2c = 145, 125

SC1 = 1.0
def s1b(mm): return mm * SC1

# Outer ring (in TSB-01 pocket)
or_left = cx2c - s1b(BRG_OD/2)
or_right = cx2c + s1b(BRG_OD/2)
or_bot = cy2c - s1b(BRG_W/2)
or_top = cy2c + s1b(BRG_W/2)
# Outer ring walls (left portion)
out_ring_wall = s1b(6)   # outer ring wall thickness
or_p_l = mpatches.Rectangle((or_left, or_bot), out_ring_wall, s1b(BRG_W),
                              lw=LW_THICK, edgecolor=C_OUT, facecolor=C_BEAR)
or_p_r = mpatches.Rectangle((or_right - out_ring_wall, or_bot), out_ring_wall, s1b(BRG_W),
                              lw=LW_THICK, edgecolor=C_OUT, facecolor=C_BEAR)
ax2.add_patch(or_p_l); ax2.add_patch(or_p_r)
hatch_region(ax2, or_p_l, spacing=3, angle=-45, color='#8090A0', lw=0.4)
hatch_region(ax2, or_p_r, spacing=3, angle=-45, color='#8090A0', lw=0.4)

# Outer ring top/bottom
or_cap_h = s1b(4)
or_cap_t = mpatches.Rectangle((or_left, or_top - or_cap_h), s1b(BRG_OD), or_cap_h,
                                lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR)
or_cap_b = mpatches.Rectangle((or_left, or_bot), s1b(BRG_OD), or_cap_h,
                                lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR)
ax2.add_patch(or_cap_t); ax2.add_patch(or_cap_b)
hatch_region(ax2, or_cap_t, spacing=3, angle=-45, color='#8090A0', lw=0.4)
hatch_region(ax2, or_cap_b, spacing=3, angle=-45, color='#8090A0', lw=0.4)

# Inner ring
ir_wall = s1b(5)
ir_outer_r = s1b(BRG_OD/2) - out_ring_wall - s1b(2)
ir_inner_r = s1b(BRG_ID/2)
ir_h = s1b(BRG_W) - 2*or_cap_h
ir_y = or_bot + or_cap_h
ir_l = mpatches.Rectangle((cx2c - ir_outer_r, ir_y), ir_wall, ir_h,
                            lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR)
ir_r = mpatches.Rectangle((cx2c + ir_outer_r - ir_wall, ir_y), ir_wall, ir_h,
                            lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR)
ax2.add_patch(ir_l); ax2.add_patch(ir_r)
hatch_region(ax2, ir_l, spacing=2, angle=45, color='#7080A0', lw=0.4)
hatch_region(ax2, ir_r, spacing=2, angle=45, color='#7080A0', lw=0.4)

# PTFE liner gap (vertical lines between inner and outer rings)
ptfe_left_x = cx2c - ir_outer_r + ir_wall + s1b(1)
ptfe_right_x = cx2c + ir_outer_r - ir_wall - s1b(1)
ax2.plot([ptfe_left_x, ptfe_left_x], [ir_y, ir_y + ir_h],
         color=C_GASKT, lw=2.0)
ax2.plot([ptfe_right_x, ptfe_right_x], [ir_y, ir_y + ir_h],
         color=C_GASKT, lw=2.0)

# TSB-01 bore context (frame material either side of bearing)
frame_ctx_w = s1b(20)
fc_l = mpatches.Rectangle((or_left - frame_ctx_w, or_bot), frame_ctx_w, s1b(BRG_W),
                            lw=LW_MED, edgecolor=C_OUT, facecolor=C_ALUM)
fc_r = mpatches.Rectangle((or_right, or_bot), frame_ctx_w, s1b(BRG_W),
                            lw=LW_MED, edgecolor=C_OUT, facecolor=C_ALUM)
ax2.add_patch(fc_l); ax2.add_patch(fc_r)
hatch_region(ax2, fc_l, spacing=4, angle=45, color='#999999', lw=0.4)
hatch_region(ax2, fc_r, spacing=4, angle=45, color='#999999', lw=0.4)

# TSB-02 shank through bearing
shank_p2 = mpatches.Rectangle((cx2c - s1b(BRG_SHANK_D/2), or_bot - s1b(15)),
                               s1b(BRG_SHANK_D), s1b(BRG_W) + s1b(15),
                               lw=LW_MED, edgecolor=C_OUT, facecolor='#C0C0C0')
ax2.add_patch(shank_p2)
hatch_region(ax2, shank_p2, spacing=3, angle=45, color='#A0A0A0', lw=0.4)

# Seals (EPDM lips each end)
for sy in [or_bot, or_top - s1b(3)]:
    seal_p = mpatches.Rectangle((cx2c - ir_outer_r - s1b(1), sy), s1b(2*ir_outer_r + 2), s1b(3),
                                  lw=0.5, edgecolor=C_OUT, facecolor=C_GASKT)
    ax2.add_patch(seal_p)

# Centreline
ax2.plot([cx2c, cx2c], [or_bot - 20, or_top + 20],
         color=C_CL, lw=LW_THIN, linestyle=(0, (6, 2, 1, 2)))

# Dimensions
draw_dim_h(ax2, or_left - frame_ctx_w, or_right + frame_ctx_w, or_top + 12,
           f'Ø{BRG_OD} OD', above=True, fontsize=5, scale=1.2)
draw_dim_h(ax2, cx2c - s1b(BRG_ID/2), cx2c + s1b(BRG_ID/2), or_bot - 18,
           f'Ø{BRG_ID} BORE', above=False, fontsize=5, scale=1.2)
draw_dim_v(ax2, or_right + frame_ctx_w + 10, or_bot, or_top, f'{BRG_W} WIDE', right=True, fontsize=5, scale=1.2)

leader(ax2, cx2c + 85, cy2c + 5, cx2c + ir_outer_r - ir_wall/2, cy2c,
       'PTFE COMPOSITE\nLINING (2RS SEALED)\n±15° MISALIGN', fontsize=4.8)
leader(ax2, cx2c - 75, cy2c - 35, or_left - frame_ctx_w/2, cy2c,
       'TSB-01\nFRAME\nAl 6061', fontsize=4.8)
leader(ax2, cx2c - 55, cy2c - 40, cx2c - 15, or_bot - s1b(8),
       'TSB-02\nSHANK\nØ50 k5', fontsize=4.8)
leader(ax2, cx2c + 75, cy2c - 18, or_right - 4, or_bot + s1b(2),
       'RUBBER\nSEAL (2RS)', fontsize=4.8)

ax2.text(cx2c, or_bot - 28, 'SKF GE50-DO-2RS  (or INA / Kaydon equivalent)\nPress-fit outer ring H7/r6  •  Ø50 k5 shank',
         ha='center', fontsize=5, style='italic', color='#333333')

# ── PANEL D: Adjustment screw detail (1:1) ────────────────────────────────────
ax2.text(360, 215, 'PANEL D — ADJUSTMENT SCREW DETAIL (1:1)', fontsize=7.5, fontweight='bold')
ax2.plot([360, 695], [212, 212], color='black', lw=0.7)

cx2d, cy2d = 490, 130

# Frame boss (outer adapter frame wall in section)
frame_wall_w = s1b(35)
frame_wall_p = mpatches.Rectangle((cx2d - frame_wall_w, cy2d - s1b(30)),
                                   frame_wall_w, s1b(60),
                                   lw=LW_MED, edgecolor=C_OUT, facecolor=C_ALUM)
ax2.add_patch(frame_wall_p)
hatch_region(ax2, frame_wall_p, spacing=4, angle=45, color='#999999', lw=0.4)

# Delrin bushing (M22×1.0 OD × M8 bore)
bush_w = s1b(BUSH_L)
bush_p = mpatches.Rectangle((cx2d - frame_wall_w, cy2d - s1b(BUSH_OD/2)),
                              bush_w, s1b(BUSH_OD),
                              lw=LW_MED, edgecolor=C_OUT, facecolor=C_DELR, zorder=4)
ax2.add_patch(bush_p)
# M8 bore through bushing
bore_p = mpatches.Rectangle((cx2d - frame_wall_w, cy2d - s1b(ADJ_D/2)),
                              bush_w, s1b(ADJ_D),
                              lw=0, facecolor='white')
ax2.add_patch(bore_p)
ax2.plot([cx2d - frame_wall_w, cx2d - frame_wall_w + bush_w],
         [cy2d - s1b(ADJ_D/2), cy2d - s1b(ADJ_D/2)], color=C_OUT, lw=LW_THIN)
ax2.plot([cx2d - frame_wall_w, cx2d - frame_wall_w + bush_w],
         [cy2d + s1b(ADJ_D/2), cy2d + s1b(ADJ_D/2)], color=C_OUT, lw=LW_THIN)

# M8 adjustment screw shaft
screw_len = s1b(80)
screw_p = mpatches.Rectangle((cx2d, cy2d - s1b(ADJ_D/2)),
                               screw_len, s1b(ADJ_D),
                               lw=LW_MED, edgecolor=C_OUT, facecolor=C_STEEL, zorder=5)
ax2.add_patch(screw_p)
# Thread representation (dashed lines)
for i in range(1, 9):
    tx = cx2d + i * screw_len/9
    ax2.plot([tx, tx], [cy2d - s1b(ADJ_D/2) - 1, cy2d + s1b(ADJ_D/2) + 1],
             color=C_HID, lw=0.4, ls='--')

# Knob at right end
knob_p = mpatches.Rectangle((cx2d + screw_len, cy2d - s1b(KNOB_D/2)),
                              s1b(KNOB_H), s1b(KNOB_D),
                              lw=LW_MED, edgecolor=C_OUT, facecolor='#404040')
ax2.add_patch(knob_p)
# Knurling lines
for i in range(6):
    ky = cy2d - s1b(KNOB_D/2) + i*s1b(KNOB_D/5) + s1b(KNOB_D/10)
    ax2.plot([cx2d + screw_len + s1b(1), cx2d + screw_len + s1b(KNOB_H) - s1b(1)],
             [ky, ky], color='#888888', lw=0.5)

# Ball at left end of screw
ball_x2 = cx2d - s1b(BALL_D/2) - s1b(2)
draw_circle(ax2, ball_x2, cy2d, s1b(BALL_D/2), fill=True, fc=C_BEAR, lw=LW_MED, color=C_OUT, zorder=6)

# Carrier plate rim (socket side)
carrier_rim_w = s1b(25)
carrier_p2 = mpatches.Rectangle((ball_x2 - carrier_rim_w, cy2d - s1b(CARR_THICK/2)),
                                  carrier_rim_w, s1b(CARR_THICK),
                                  lw=LW_THICK, edgecolor=C_OUT, facecolor='#C0C0C0', zorder=3)
ax2.add_patch(carrier_p2)
hatch_region(ax2, carrier_p2, spacing=3, angle=45, color='#A0A0A0', lw=0.4)
# Socket insert
sock_p = mpatches.Circle((ball_x2 - s1b(8), cy2d), s1b(8),
                           lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR, zorder=5)
ax2.add_patch(sock_p)
# Hemispherical pocket (dashed semicircle)
theta = np.linspace(0, np.pi, 30)
ax2.plot(ball_x2 - s1b(8) + s1b(BALL_D/2)*np.cos(theta),
         cy2d + s1b(BALL_D/2)*np.sin(theta),
         color=C_HID, lw=0.8, ls='--', zorder=7)

# Horizontal centerline through screw
ax2.plot([cx2d - frame_wall_w - 5, cx2d + screw_len + s1b(KNOB_H) + 5],
         [cy2d, cy2d], color=C_CL, lw=LW_THIN, linestyle=(0, (6, 2, 1, 2)))

# Dims and leaders
draw_dim_h(ax2, cx2d, cx2d + screw_len, cy2d + s1b(KNOB_D/2) + 12,
           'M8 × 1.0 × 80 SCREW', above=True, fontsize=5, scale=1.2)
draw_dim_h(ax2, cx2d - frame_wall_w, cx2d - frame_wall_w + bush_w,
           cy2d - s1b(KNOB_D/2) - 12, f'BUSH L={BUSH_L}', above=False, fontsize=5, scale=1.2)

leader(ax2, cx2d + screw_len + s1b(KNOB_H) + 12, cy2d + 10,
       cx2d + screw_len + s1b(KNOB_H)/2, cy2d + s1b(KNOB_D/2),
       'Ø40 KNURLED KNOB\n36-DETENT\n0.012°/CLICK', fontsize=5)
leader(ax2, cx2d - frame_wall_w - 28, cy2d + 12,
       cx2d - frame_wall_w + bush_w/2, cy2d + s1b(BUSH_OD/2),
       'DELRIN/POM\nGUIDE BUSHING\nM22×1.0 OD', fontsize=5)
leader(ax2, ball_x2 - s1b(8) - 20, cy2d - 18,
       ball_x2 - s1b(8), cy2d - s1b(BALL_D/2),
       '440C SS INSERT\nHEMI SOCKET\nRa 0.4 GROUND', fontsize=5)
leader(ax2, ball_x2 + 14, cy2d + 12, ball_x2, cy2d + s1b(BALL_D/2),
       'Ø8 Gr25\nCHROME\nSTEEL BALL', fontsize=5)

# Angular resolution table
tbl_x, tbl_y = 580, 195
ax2.text(tbl_x, tbl_y, 'ANGULAR RESOLUTION', fontsize=6, fontweight='bold', color='black')
rows = [
    ('Arm radius (pivot→ball)', '130 mm'),
    ('Screw pitch', '1.0 mm / turn'),
    ('Linear travel ÷ arm', '1/130 rad/mm = 0.0077°/mm'),
    ('Resolution per turn', '0.44° / turn'),
    ('Detents per turn', '36'),
    ('Resolution per click', '0.012° / click'),
    ('Full ±5° range', '~410 clicks (11.4 turns)'),
    ('Hard stop travel', '±12 mm = ±5.3°'),
]
for i, (k, v) in enumerate(rows):
    ry = tbl_y - 10 - i*9
    bg = '#F8F8F8' if i%2==0 else 'white'
    draw_rect(ax2, tbl_x - 2, ry - 7, 110, 9, lw=0.3, color='#CCCCCC', fc=bg, zorder=1)
    ax2.text(tbl_x, ry, k, fontsize=4.5, color='black')
    ax2.text(tbl_x + 68, ry, v, fontsize=4.5, color='black', fontweight='bold')

out2 = 'diagrams/tilt-swing-board-sheet2.png'
fig2.savefig(out2, dpi=150, bbox_inches='tight', facecolor='white')
fig2.savefig(svg_path(out2), bbox_inches="tight", facecolor='white')
plt.close(fig2)
print(f'  → {out2}  Done.')


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — Bellows, Locking, Scale & Swap Procedure
# ═══════════════════════════════════════════════════════════════════════════════

FH3 = int(FH * 1.3)  # 30% taller canvas to shift content up
fig3, ax3 = plt.subplots(figsize=(FW/25.4*0.9, FH3/25.4*0.9))
fig3.patch.set_facecolor('white')
ax3.set_facecolor('white')
ax3.set_aspect('equal')
ax3.axis('off')
ax3.set_xlim(0, FW)
ax3.set_ylim(0, FH3)
S3_UP = FH3 - FH  # vertical shift = 150

title_block(ax3, FW, FH3, 3, 3,
            'TILT-SWING FRONT BOARD MECHANISM',
            'SHEET 3 — BELLOWS SEAL, LOCKING, CALIBRATION SCALE & SWAP PROCEDURE',
            'AS NOTED', position='top')

# ── PANEL A: Bellows section at 0° and 5° tilt ────────────────────────────────
ax3.text(15, 490 + S3_UP, 'PANEL A — BELLOWS SECTION: NEUTRAL (solid) & 5° TILT (dashed) (1:2)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([15, 480], [487 + S3_UP, 487 + S3_UP], color='black', lw=0.7)

cx3a, cy3a = 200, 430 + S3_UP

def draw_bellows_section(ax, cx, cy, tilt_deg, lw_style='-', alpha=1.0):
    """Draw bellows accordion cross-section for given tilt angle."""
    tilt = np.radians(tilt_deg)
    # Bellows geometry: outer attach at ±BELL_OD/2 radius, inner attach at ±BELL_ID/2
    # Free length BELL_FREE mm, drawn at 1:2 scale
    sc_b = 0.5
    r_out = s2(BELL_OD/2)
    r_in  = s2(BELL_ID/2)
    L     = s2(BELL_FREE)
    # At tilt angle, inner plate (bottom of bellows) tilts:
    # left side of inner: cx - r_in, compresses; right side: cx + r_in, extends
    delta = r_in * np.tan(tilt)  # asymmetric vertical offset at inner radius
    # Draw outline of bellows cross-section as two mirrored accordion strips
    for side in [-1, 1]:  # left and right
        x_out = cx + side * r_out  # fixed outer attachment
        x_in  = cx + side * r_in   # tilted inner attachment
        # Inner Y position offset by tilt
        y_inner = cy - L + side * delta
        n_p = BELL_PLEATS
        # Pleat points: alternating between outer and inner radii
        pts_x, pts_y = [x_out], [cy]
        for j in range(n_p):
            frac = (j + 0.5) / n_p
            y_mid = cy - frac * L
            if j % 2 == 0:
                pts_x.append(x_out + side * s2(BELL_PLEAT_D))
            else:
                pts_x.append(x_out - side * s2(BELL_PLEAT_D * 0.5))
            pts_y.append(y_mid + side * delta * frac * 0.5)
        pts_x.append(x_in)
        pts_y.append(y_inner)
        col = C_BELL if lw_style == '-' else '#808080'
        ax.plot(pts_x, pts_y, color=col, lw=1.5 if lw_style=='-' else 1.0,
                linestyle=lw_style, alpha=alpha)
    # Top attachment line (outer frame edge)
    ax.plot([cx - r_out, cx + r_out], [cy, cy], color='black', lw=1.5 if lw_style=='-' else 1.0,
            linestyle=lw_style, alpha=alpha)
    # Bottom attachment line (carrier plate, tilted)
    y_left  = cy - L - delta
    y_right = cy - L + delta
    ax.plot([cx - r_in, cx + r_in], [y_left, y_right],
            color='black', lw=1.5 if lw_style=='-' else 1.0, linestyle=lw_style, alpha=alpha)

# 0° (solid)
draw_bellows_section(ax3, cx3a, cy3a, 0, lw_style='-')
# 5° (dashed)
draw_bellows_section(ax3, cx3a, cy3a, 5, lw_style='--', alpha=0.7)

# Context: outer frame and carrier plate in section
frame_bar_h = s2(10)
draw_rect(ax3, cx3a - s2(BELL_OD/2) - 15, cy3a, 15 + s2(BELL_OD) + 15, frame_bar_h,
          lw=LW_MED, color=C_OUT, fc=C_ALUM)
ax3.text(cx3a, cy3a + frame_bar_h/2, 'TSB-01 OUTER FRAME', ha='center', va='center', fontsize=4.5, color='black', zorder=10)

carr_bar_h = s2(10)
# Neutral position carrier
draw_rect(ax3, cx3a - s2(BELL_ID/2) - 10, cy3a - s2(BELL_FREE) - carr_bar_h,
          s2(BELL_ID) + 20, carr_bar_h, lw=LW_MED, color=C_OUT, fc='#C0C0C0')
ax3.text(cx3a, cy3a - s2(BELL_FREE) - carr_bar_h/2,
         'TSB-02 CARRIER (NEUTRAL)', ha='center', va='center', fontsize=4.5, color='black', zorder=10)

# Dimensions
draw_dim_v(ax3, cx3a + s2(BELL_OD/2) + 15, cy3a - s2(BELL_FREE), cy3a,
           f'{BELL_FREE} FREE LEN', right=True, fontsize=5, scale=1.5)
draw_dim_h(ax3, cx3a - s2(BELL_OD/2), cx3a + s2(BELL_OD/2), cy3a + frame_bar_h + 14,
           f'OD Ø{BELL_OD}', above=True, fontsize=5, scale=1.5)
draw_dim_h(ax3, cx3a - s2(BELL_ID/2), cx3a + s2(BELL_ID/2),
           cy3a - s2(BELL_FREE) - carr_bar_h - 14, f'ID Ø{BELL_ID}', above=False, fontsize=5, scale=1.5)

ax3.text(cx3a + s2(BELL_OD/2) + 52, cy3a - s2(BELL_FREE*0.5),
         '——— NEUTRAL (0°)\n- - - - 5° TILT\n(asymmetric compression\nleft side: −13.9 mm\nright side: +13.9 mm)',
         fontsize=5, va='center', color='#333333', zorder=10)

ax3.text(cx3a, cy3a - s2(BELL_FREE) - carr_bar_h - 30,
         'BELLOWS TSB-10: Matte black neoprene/nylon  •  0.5 mm wall  •  4 pleats  •  15 mm pleat depth\nInner+outer flanges sealed with Ø4 mm neoprene cord gaskets (same spec as wall-frame seal)',
         ha='center', fontsize=5, style='italic', color='#333333', zorder=10)

# ── PANEL B: Locking set screw detail (1:1) ──────────────────────────────────
ax3.text(15, 245 + S3_UP, 'PANEL B — LOCKING SET SCREW (1:1)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([15, 200], [242 + S3_UP, 242 + S3_UP], color='black', lw=0.7)

cx3b, cy3b = 80, 175 + S3_UP

# M8 screw shaft (horizontal)
m8_sh = mpatches.Rectangle((cx3b - 40, cy3b - 4), 80, 8,
                             lw=LW_MED, edgecolor=C_OUT, facecolor=C_STEEL)
ax3.add_patch(m8_sh)
# M6 set screw (vertical, crossing M8)
m6_sh = mpatches.Rectangle((cx3b - 4, cy3b + 4), 8, 25,
                              lw=LW_MED, edgecolor=C_OUT, facecolor=C_STEEL, zorder=5)
ax3.add_patch(m6_sh)
# Nylon tip at bottom
ny_p = mpatches.Rectangle((cx3b - 3, cy3b + 4), 6, 5,
                            lw=0.5, edgecolor=C_OUT, facecolor='#F0E080', zorder=6)
ax3.add_patch(ny_p)
# Hex key socket (top of M6)
ax3.plot([cx3b - 2.5, cx3b + 2.5], [cy3b + 29, cy3b + 29], color=C_OUT, lw=2.0)
ax3.plot([cx3b - 1.5, cx3b - 1.5], [cy3b + 27, cy3b + 29], color=C_OUT, lw=1.0)
ax3.plot([cx3b + 1.5, cx3b + 1.5], [cy3b + 27, cy3b + 29], color=C_OUT, lw=1.0)
# Boss context (frame)
fr3b = mpatches.Rectangle((cx3b - 40, cy3b - 12), 80, 8,
                            lw=LW_MED, edgecolor=C_OUT, facecolor=C_ALUM)
ax3.add_patch(fr3b)
hatch_region(ax3, fr3b, spacing=3, angle=45, color='#AAAAAA', lw=0.4)
fr3bt = mpatches.Rectangle((cx3b - 8, cy3b + 29), 16, 10,
                             lw=LW_MED, edgecolor=C_OUT, facecolor=C_ALUM)
ax3.add_patch(fr3bt)
hatch_region(ax3, fr3bt, spacing=3, angle=45, color='#AAAAAA', lw=0.4)

leader(ax3, cx3b + 30, cy3b + 20, cx3b + 4, cy3b + 18,
       'M6×1.0\nNYLON-TIP\nSET SCREW', fontsize=5)
leader(ax3, cx3b + 30, cy3b - 2, cx3b + 40, cy3b - 2,
       'M8×1.0\nADJ SCREW\nSHANK', fontsize=5)
leader(ax3, cx3b - 40, cy3b + 10, cx3b - 4, cy3b + 6,
       'NYLON\nTIP', fontsize=5)
ax3.text(cx3b + 3, cy3b + 31, '3mm HEX', fontsize=4.5, color='#333333', zorder=10)
ax3.text(cx3b, cy3b - 28, 'Tighten set screw onto adj screw shank\nafter desired angle is set. 4 off (one per axis)',
         ha='center', fontsize=4.8, style='italic', color='#333333', zorder=10)

# ── PANEL C: Knob detail (2:1) ────────────────────────────────────────────────
ax3.text(215, 245 + S3_UP, 'PANEL C — KNOB DETAIL (2:1)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([215, 420], [242 + S3_UP, 242 + S3_UP], color='black', lw=0.7)

cx3c, cy3c = 305, 175 + S3_UP
SC_knob = 2.0
def sk(mm): return mm * SC_knob

# Knob in section view
knob_rec = mpatches.Rectangle((cx3c - sk(KNOB_H/2), cy3c - sk(KNOB_D/2)),
                                sk(KNOB_H), sk(KNOB_D),
                                lw=LW_THICK, edgecolor=C_OUT, facecolor='#404040')
ax3.add_patch(knob_rec)
# M8 bore through knob
knob_bore = mpatches.Rectangle((cx3c - sk(KNOB_H/2), cy3c - sk(ADJ_D/2)),
                                 sk(KNOB_H), sk(ADJ_D),
                                 lw=0, facecolor='white')
ax3.add_patch(knob_bore)
ax3.plot([cx3c - sk(KNOB_H/2), cx3c + sk(KNOB_H/2)], [cy3c - sk(ADJ_D/2)]*2, color=C_OUT, lw=LW_THIN)
ax3.plot([cx3c - sk(KNOB_H/2), cx3c + sk(KNOB_H/2)], [cy3c + sk(ADJ_D/2)]*2, color=C_OUT, lw=LW_THIN)
# Flat/keyway on bore (anti-rotation)
flat_p = mpatches.Rectangle((cx3c - sk(KNOB_H/2), cy3c + sk(ADJ_D/2 - 1.5)),
                              sk(KNOB_H), sk(1.5),
                              lw=0, facecolor='#404040')
ax3.add_patch(flat_p)
# Detent ball pocket (one shown)
det_x = cx3c + sk(KNOB_H/2) - sk(2)
draw_circle(ax3, det_x, cy3c + sk(KNOB_D/2) - sk(2), sk(1.5),
            fill=True, fc='white', lw=LW_THIN, color=C_OUT)
# Knurling on OD
for i in range(8):
    kang = np.radians(i * 22.5)
    kx = cx3c + sk(KNOB_H/2 - 1.5) * np.cos(kang)
    ky = cy3c + sk(KNOB_D/2 - 1.5) * np.sin(kang)
    # just line marks on top/bottom
for ky_off in np.linspace(-sk(KNOB_D/2)*0.9, sk(KNOB_D/2)*0.9, 10):
    ax3.plot([cx3c - sk(KNOB_H/2) + sk(1), cx3c + sk(KNOB_H/2) - sk(1)],
             [cy3c + ky_off, cy3c + ky_off], color='#888888', lw=0.4)
# Label engraved on face (top)
ax3.text(cx3c, cy3c + sk(KNOB_D/2) + 5, '"TILT +"', fontsize=5, ha='center',
         color='#333333', style='italic', zorder=10)

draw_dim_h(ax3, cx3c - sk(KNOB_H/2), cx3c + sk(KNOB_H/2),
           cy3c - sk(KNOB_D/2) - 12, f'{KNOB_H} WIDE', above=False, fontsize=5, scale=1.0)
draw_dim_v(ax3, cx3c + sk(KNOB_H/2) + 12, cy3c - sk(KNOB_D/2), cy3c + sk(KNOB_D/2),
           f'Ø{KNOB_D}', right=True, fontsize=5, scale=1.0)

leader(ax3, cx3c + 55, cy3c + 12, det_x, cy3c + sk(KNOB_D/2) - sk(2),
       '36-DETENT\nSPRING BALL\n(5° PER CLICK)', fontsize=5)
leader(ax3, cx3c + 55, cy3c - 10, cx3c + sk(3), cy3c + sk(ADJ_D/2 - 1.5),
       'FLAT/KEYWAY\n(ANTI-SPIN)', fontsize=5)

ax3.text(cx3c, cy3c - sk(KNOB_D/2) - 28,
         'Black anodize = TILT axis  |  Natural anodize = SWING axis\nEngraved label on knob face: TILT+ / TILT− / SWING+ / SWING−',
         ha='center', fontsize=5, style='italic', color='#333333', zorder=10)

# ── PANEL D: Angular scale layout ─────────────────────────────────────────────
ax3.text(430, 245 + S3_UP, 'PANEL D — ANGULAR CALIBRATION SCALE (1:1)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([430, 695], [242 + S3_UP, 242 + S3_UP], color='black', lw=0.7)

cx3d, cy3d = 530, 175 + S3_UP
arm = 130  # mm arm radius
scale_w_mm = 80  # scale total width in mm

ax3.text(cx3d, 240 + S3_UP, 'Non-linear (tangent) scale: position = 80 × tan(θ)/tan(5°) mm',
         ha='center', fontsize=5, color='#333333', style='italic', zorder=10)

# Draw the scale strip
scale_strip_w = 80  # drawing units = mm at 1:1
scale_strip_h = 12
draw_rect(ax3, cx3d - scale_strip_w/2, cy3d - scale_strip_h/2,
          scale_strip_w, scale_strip_h, lw=LW_MED, color=C_OUT, fc='#F8F8F8')

# Tick marks (tan-scale)
for deg in np.arange(-5, 5.5, 0.5):
    x_pos = cx3d + scale_strip_w/2 * (np.tan(np.radians(deg)) / np.tan(np.radians(5)))
    is_major = (deg == round(deg))
    tick_h = scale_strip_h * 0.6 if is_major else scale_strip_h * 0.3
    ax3.plot([x_pos, x_pos],
             [cy3d + scale_strip_h/2 - tick_h, cy3d + scale_strip_h/2],
             color='black', lw=1.0 if is_major else 0.5)
    if is_major:
        ax3.text(x_pos, cy3d - scale_strip_h/2 - 3, f'{deg:+.0f}°',
                 ha='center', va='top', fontsize=4.5, color='black', zorder=10)

ax3.text(cx3d, cy3d, '0', ha='center', va='center', fontsize=6, fontweight='bold', color=C_RED, zorder=10)
ax3.plot([cx3d, cx3d], [cy3d - scale_strip_h/2, cy3d + scale_strip_h/2],
         color=C_RED, lw=1.0)

draw_dim_h(ax3, cx3d - scale_strip_w/2, cx3d + scale_strip_w/2,
           cy3d + scale_strip_h/2 + 10, '80 mm TOTAL', above=True, fontsize=5, scale=1.0)
ax3.text(cx3d, cy3d - scale_strip_h/2 - 20,
         '2 off — one for TILT, one for SWING\nLaser-engraved Al 80×15×2 mm  •  Mounted on TSB-01 face adjacent to each knob pair',
         ha='center', fontsize=5, style='italic', color='#333333', zorder=10)

S3_E_DN = int(FH3 * 0.10)  # 10% drop for Panel E separation

# ── Separator line between panels B/C/D and panel E ──────────────────────────
ax3.plot([15, 685], [135 + S3_UP - S3_E_DN, 135 + S3_UP - S3_E_DN], color='#999999', lw=0.5, linestyle='--', zorder=5)

# ── PANEL E: Swap sequence ────────────────────────────────────────────────────
ax3.text(15, 125 + S3_UP - S3_E_DN, 'PANEL E — PLATE SWAP PROCEDURE (TSB ASSY ↔ STANDARD PINHOLE PLATE)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([15, 695], [122 + S3_UP - S3_E_DN, 122 + S3_UP - S3_E_DN], color='black', lw=0.7)

steps = [
    ('①', 'LOOSEN 4×\nLOCK SCREWS', '3 mm hex key\nM6 set screws'),
    ('②', 'ZERO ALL\n4 ADJ KNOBS', 'Return to 0°\nusing scale marks'),
    ('③', 'REMOVE 8×\nM12 BOLTS', 'M12 socket\n65 Nm torque'),
    ('④', 'PULL TSB\nASSEMBLY', 'Dowel pins\nretain alignment'),
    ('⑤', 'FIT STANDARD\nPINHOLE PLATE', 'Locate on same\ndowels — re-bolt'),
]

step_w = 120
step_gap = 15
for i, (num, title, note) in enumerate(steps):
    sx = 20 + i * (step_w + step_gap)
    sy = 60 + S3_UP - S3_E_DN
    draw_rect(ax3, sx, sy, step_w, 55, lw=1.0, color='black', fc='#F0F0F0')
    ax3.text(sx + step_w/2, sy + 48, num, ha='center', fontsize=14,
             fontweight='bold', color='black', zorder=10)
    ax3.text(sx + step_w/2, sy + 32, title, ha='center', fontsize=6.5,
             fontweight='bold', color='black', zorder=10)
    ax3.text(sx + step_w/2, sy + 12, note, ha='center', fontsize=5.5,
             color='#555555', style='italic', zorder=10)
    if i < 4:
        ax3.annotate('', xy=(sx + step_w + 13, sy + 27), xytext=(sx + step_w + 2, sy + 27),
                     arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

ax3.text(695/2, 45 + S3_UP - S3_E_DN, 'No special tooling required beyond M12 socket and 3 mm hex key  •  Swap time: approx. 10 minutes',
         ha='center', fontsize=5.5, color='#333333', style='italic', zorder=10)

out3 = 'diagrams/tilt-swing-board-sheet3.png'
fig3.savefig(out3, dpi=150, bbox_inches='tight', facecolor='white')
fig3.savefig(svg_path(out3), bbox_inches="tight", facecolor='white')
plt.close(fig3)
print(f'  → {out3}  Done.')
