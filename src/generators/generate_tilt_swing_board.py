#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_tilt_swing_board.py
Tilt-and-Swing Front Board — The Big Shoebox Project
Drawing series TBS-TSB  (3 sheets)

Sheet 1 — Assembly overview & Outer Adapter Frame (ICP-01)
Sheet 2 — Inner Carrier Plate (ICP-02), Bearing & Adjustment mechanism
Sheet 3 — Light seal (bellows), Locking, Calibration scale & Swap procedure

Style matches generate_plate_drawing.py (white background, same palette & helpers).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
from tbs_constants import (DIAGRAMS_DIR, FRONT_BOARD_MAX_DEG, FRONT_BOARD_CLICK_DEG,
                           FRONT_BOARD_DETENTS, FRONT_BOARD_TRAVEL_MM, FRONT_BOARD_SCREW_PITCH)
from tbs_title_block import title_block
from tbs_drawing import (draw_dim_h, draw_dim_v, draw_cl, draw_circle,
                         draw_rect, leader, bolt_holes)
from tbs_constants import DIAGRAM_DPI

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

# --- ICP-01 Outer Adapter Frame ---
TSB01_THICK  = 40     # plate thickness
TSB01_BORE   = 380    # central bore diameter
BRG_SEAT_D   = 80     # bearing outer ring OD / seat bore diameter
BRG_SEAT_DEP = 50     # depth of bearing pocket
ADJ_PCD      = 270    # adjustment screw PCD (in frame)
ADJ_N        = 4      # 4 screws
LAB_D1, LAB_D2, LAB_D3 = 382, 390, 400  # labyrinth step diameters
BELL_OUT_PCD = 375    # bellows outer flange bolt PCD

# --- ICP-02 Inner Carrier Plate ---
CARR_OD      = 320    # carrier plate OD
CARR_THICK   = 25     # thickness
BRG_SHANK_D  = 50     # bearing shank diameter (k5)
BRG_SHANK_L  = 35     # shank length
SOCK_PCD     = 260    # ball socket insert PCD
BELL_IN_PCD  = 310    # bellows inner flange bolt PCD

# --- Bearing ICP-03 ---
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
C_BEAR  = '#C0C8D8'   # bearing / steel blue-gray
C_BELL  = '#303030'   # bellows black




# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — Assembly overview & Outer Adapter Frame
# ═══════════════════════════════════════════════════════════════════════════════

FW, FH = 700, 500
FW1, FH1 = 5600, 4000
fig1, ax1 = plt.subplots(figsize=(FW*0.9/25.4, FH*0.9/25.4))
fig1.patch.set_facecolor('white')
ax1.set_facecolor('white')
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_xlim(0, FW1)
ax1.set_ylim(0, FH1)

title_block(ax1, "SHEET 1 OF 3",
            drawing_title="TILT-SWING FRONT BOARD",
            subtitle="Assembly overview & Outer Adapter Frame",
            scale_note="AXES IN mm",
            doc_id="TBS-TSB · Tilt-Swing Board")

# ── Section header lines ──────────────────────────────────────────────────────
def section_label(ax, x, y, text):
    ax.text(x, y, text, fontsize=7.5, fontweight='bold', color='black')
    ax.plot([x, x+1600], [y-24, y-24], color='black', lw=0.7)

section_label(ax1, 80, 3920, 'PANEL A — FULL ASSEMBLY (1:8)')
section_label(ax1, 1360, 3920, 'PANEL B — ICP-01 EXTERIOR FACE (1:8)')
section_label(ax1, 2640, 3920, 'PANEL C — ICP-01 INTERIOR FACE (1:8)')

SC = 1
def s1(mm): return mm * SC

# ───────────────────────────────────────────────
# PANEL A: Full assembly front view
# ───────────────────────────────────────────────
cx_a, cy_a = 680, 2640
hw = s1(PL_OD/2)

# Outer adapter frame (ICP-01) — aluminum, slightly thicker than normal plates
p = mpatches.Rectangle((cx_a - hw, cy_a - hw), s1(PL_OD), s1(PL_OD),
                        lw=LW_THICK, edgecolor=C_OUT, facecolor=C_ALUM, zorder=3)
ax1.add_patch(p)

# Central bore
draw_circle(ax1, cx_a, cy_a, s1(TSB01_BORE/2), lw=LW_MED, color=C_OUT, fill=True, fc='white', zorder=4)

# Inner carrier plate (ICP-02) — circular, darker Al
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
draw_dim_h(ax1, cx_a - s1(CARR_OD/2), cx_a + s1(CARR_OD/2), cy_a - hw - 48,
           'Ø320 CARRIER', above=False, fs=5, offset=24)
draw_dim_h(ax1, cx_a - hw, cx_a + hw, cy_a + hw + 48, '600mm', above=True, fs=5.5, offset=24)

ax1.text(cx_a, cy_a - hw - 200, 'PANEL A — ASSEMBLY (1:8)\nICP-01 outer frame + ICP-02 carrier\nBlack knobs = TILT  Silver knobs = SWING',
         ha='center', fontsize=5, color='#333333', style='italic')

# ───────────────────────────────────────────────
# PANEL B: ICP-01 Exterior (container-wall-facing) face
# ───────────────────────────────────────────────
cx_b, cy_b = 2064, 2640

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
leader(ax1, cx_b + s1(TSB01_BORE/2)*0.7, cy_b + s1(TSB01_BORE/2)*0.7,
       cx_b + 240, cy_b + 360,
       'Ø380 BORE\n(PANEL B VIEW)', fs=4.8, color=C_DIM, arrow_style='->')
leader(ax1, cx_b + s1(SEAL_D/2)*0.65, cy_b - s1(SEAL_D/2)*0.65,
       cx_b + 176, cy_b - 384,
       'Ø420 SEAL\nGROOVE\n3×3 DEEP', fs=4.5, color=C_DIM, arrow_style='->')
leader(ax1, cx_b + s1(ADJ_PCD/2) + s1(BUSH_OD/2), cy_b,
       cx_b + s1(ADJ_PCD/2) + 112, cy_b + 32,
       'M22×1.0\nBUSHING\n(4 OFF)', fs=4.5, color=C_DIM, arrow_style='->')
leader(ax1, cx_b + s1(BOLT_BC/2)*0.65, cy_b + s1(BOLT_BC/2)*0.65,
       cx_b + 128, cy_b + 224,
       'Ø540 B.C.\n8×M12\nCLR', fs=4.5, color=C_DIM, arrow_style='->')

ax1.text(cx_b, cy_b - hw - 200, 'PANEL B — ICP-01 EXTERIOR (1:8)\n(Same bolt/dowel/seal interface\nas standard pinhole plate)',
         ha='center', fontsize=5, color='#333333', style='italic')

# ───────────────────────────────────────────────
# PANEL C: ICP-01 Interior (container-facing) face
# ───────────────────────────────────────────────
cx_c, cy_c = 3400, 2640

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

leader(ax1, cx_c - s1(BRG_SEAT_D/2)*0.7, cy_c + s1(BRG_SEAT_D/2)*0.7,
       cx_c - 144, cy_c + 96,
       'Ø80 H7 BEARING\nSEAT × 50 DEEP', fs=4.8, color=C_DIM, arrow_style='->')
leader(ax1, cx_c + s1(BELL_OUT_PCD/2)*0.6, cy_c + s1(BELL_OUT_PCD/2)*0.6,
       cx_c + 200, cy_c + 224,
       '6×M6 ON\nØ375 PCD\n(BELLOWS)', fs=4.5, color=C_DIM, arrow_style='->')
leader(ax1, cx_c + s1(LAB_D3/2)*0.65, cy_c - s1(LAB_D3/2)*0.65,
       cx_c + 160, cy_c - 360,
       '3-STEP\nLABYRINTH\nØ382/390/400\n5 DEEP EACH', fs=4.3, color=C_DIM, arrow_style='->')

ax1.text(cx_c, cy_c - hw - 200, 'PANEL C — ICP-01 INTERIOR (1:8)\n(Bearing pocket + labyrinth + bellows attach)',
         ha='center', fontsize=5, color='#333333', style='italic')

# ───────────────────────────────────────────────
# PANEL D: Section A-A — separate X/Y scales so 600×40mm section is readable
# Horizontal: 1:5  →  600mm = 120 units
# Vertical:   1:1  →  40mm frame + 25mm carrier + 35mm bearing shank = 100 units
# ───────────────────────────────────────────────

ax1.text(80, 1776, 'PANEL D — SECTION A-A  (AXES IN mm  — thickness exaggerated for clarity)',
         fontsize=7, fontweight='bold')
ax1.plot([80, 3920], [1752, 1752], color='black', lw=0.7)

# Center section
cx_d = 2000
frame_top = 1680   # top of ICP-01 frame

# Heights in drawing units (1:1 vertical)
fh = (TSB01_THICK)   # frame height = 40
ch = (CARR_THICK)    # carrier height = 25
bh = (BRG_W)         # bearing height = 46

# Y positions (drawing downward = interior side)
frame_y_top = frame_top
frame_y_bot = frame_top - fh          # interior face of ICP-01
carrier_y_top = frame_y_bot           # carrier sits flush on interior face
carrier_y_bot = carrier_y_top - ch
seat_y_top = frame_y_bot              # bearing pocket starts at interior face
seat_y_bot = seat_y_top + (BRG_SEAT_DEP)   # pocket goes INTO frame (upward)

# Frame footprint — left wing
left_wing_w = ((PL_OD - TSB01_BORE) / 2)
right_x = cx_d + (PL_OD/2)
left_x  = cx_d - (PL_OD/2)
bore_hw_d = (TSB01_BORE/2)

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
    gx = cx_d + sgn * (SEAL_D/2) - sgn * (SEAL_W/2)
    sg_p = mpatches.Rectangle((gx - (SEAL_W/2), frame_y_top - (SEAL_DEP)),
                                (SEAL_W), (SEAL_DEP),
                                lw=0.5, edgecolor=C_OUT, facecolor=C_GASKT, zorder=5)
    ax1.add_patch(sg_p)

# Light-trap rebate (exterior face)
for sgn in [-1, 1]:
    tx2 = cx_d + sgn * (TRAP_SQ/2) - sgn * (5)
    tr_p = mpatches.Rectangle((tx2 - (2.5), frame_y_top - (5)),
                                (5), (5),
                                lw=0.5, edgecolor=C_OUT, facecolor='white', zorder=4)
    ax1.add_patch(tr_p)

# Bearing seat pocket (opens on interior face, goes INTO frame)
seat_hw = (BRG_SEAT_D/2)
seat_dep_d = (BRG_SEAT_DEP)
ax1.plot([cx_d - seat_hw, cx_d - seat_hw], [frame_y_bot, frame_y_bot + seat_dep_d],
         color=C_OUT, lw=LW_MED)
ax1.plot([cx_d + seat_hw, cx_d + seat_hw], [frame_y_bot, frame_y_bot + seat_dep_d],
         color=C_OUT, lw=LW_MED)
ax1.plot([cx_d - seat_hw, cx_d + seat_hw], [frame_y_bot + seat_dep_d, frame_y_bot + seat_dep_d],
         color=C_OUT, lw=LW_MED)

# GE50 Bearing in section (in pocket)
brg_hw_d = (BRG_OD/2)
brg_wall = (7)
brg_top = frame_y_bot
brg_bot = brg_top + (BRG_W/2)

# Outer ring (two side walls, hatched)
for sgn in [-1, 1]:
    bx0 = cx_d + sgn * (brg_hw_d - brg_wall)
    br_p = mpatches.Rectangle((bx0 - brg_wall if sgn < 0 else bx0, brg_top),
                                brg_wall, (BRG_W/2),
                                lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR,
                                hatch='\\\\', zorder=4)
    ax1.add_patch(br_p)
# Outer ring top cap
br_top = mpatches.Rectangle((cx_d - brg_hw_d, brg_top), (BRG_OD), (4),
                              lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR, hatch='\\\\', zorder=4)
ax1.add_patch(br_top)

# Inner ring
ir_hw = (BRG_ID/2)
ir_wall = (5)
for sgn in [-1, 1]:
    ix0 = cx_d + sgn * (ir_hw - ir_wall)
    ir_p = mpatches.Rectangle((ix0 - ir_wall if sgn < 0 else ix0, brg_top + (4)),
                                ir_wall, (BRG_W/2 - 4),
                                lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR,
                                hatch='---', zorder=5)
    ax1.add_patch(ir_p)

# ICP-02 Carrier plate
carr_hw_d = (CARR_OD/2)
ph_hw_d   = (PH_BORE/2)
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
adj_x = cx_d + (ADJ_PCD/2)
adj_hw_d = (ADJ_D/2)
# Bushing
bush_d = mpatches.Rectangle((adj_x - (BUSH_OD/2), frame_y_bot),
                              (BUSH_OD), (BUSH_L),
                              lw=LW_THIN, edgecolor=C_OUT, facecolor=C_DELR, zorder=4)
ax1.add_patch(bush_d)
# Screw shaft through bushing + frame
screw_d = mpatches.Rectangle((adj_x - adj_hw_d, frame_y_bot),
                               (ADJ_D), fh,
                               lw=0.8, edgecolor=C_OUT, facecolor=C_STEEL, zorder=5)
ax1.add_patch(screw_d)
# Ø8 ball (at carrier rim)
ball_y_d = (carrier_y_top + carrier_y_bot) / 2
ax1.plot(adj_x, ball_y_d, 'o', ms=(BALL_D), color=C_BEAR, mec=C_OUT, mew=0.7, zorder=6)

# Bellows schematic (right side, between frame interior face and carrier)
bell_x_out = cx_d + (BELL_OUT_PCD/2)
bell_x_in  = cx_d + (BELL_IN_PCD/2)
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

# Centerline
ax1.plot([cx_d, cx_d], [carrier_y_bot - 80, frame_y_top + 80],
         color=C_CL, lw=LW_THIN, linestyle=(0, (6, 2, 1, 2)))

# Break lines on sides (zig-zag) to indicate plate continues
for side_x in [left_x - 16, right_x + 16]:
    for y_brk in [frame_y_top - 40, frame_y_bot + 16]:
        ax1.plot([side_x - 24, side_x + 24, side_x - 24, side_x + 24],
                 [y_brk, y_brk - 24, y_brk - 48, y_brk - 72],
                 color='black', lw=1.0)

# Dimensions
draw_dim_h(ax1, left_x, right_x, frame_y_top + 96, '600mm (FULL WIDTH)',
           above=True, fs=5, offset=24)
draw_dim_v(ax1, left_x - 80, frame_y_bot, frame_y_top, '40',
           fs=5, offset=24)
draw_dim_v(ax1, left_x - 80, carrier_y_bot, carrier_y_top, '25',
           fs=5, offset=24)
draw_dim_h(ax1, cx_d - bore_hw_d, cx_d + bore_hw_d, carrier_y_bot - 80,
           f'Ø{TSB01_BORE} BORE', above=False, fs=5, offset=24)

# Leaders
leader(ax1, cx_d + seat_hw + 16, frame_y_bot + seat_dep_d/2,
       cx_d + 640, frame_y_bot + seat_dep_d/2,
       'Ø80 H7 BEARING\nPOCKET × 50', fs=4.8, color=C_DIM, arrow_style='->')
leader(ax1, cx_d + carr_hw_d + 16, carrier_y_bot + ch/2,
       cx_d + 520, carrier_y_bot + ch/2,
       'ICP-02 CARRIER\nØ320 × 25 Al', fs=4.8, color=C_DIM, arrow_style='->')
leader(ax1, adj_x + (BUSH_OD/2), frame_y_bot + (BUSH_L)/2,
       adj_x + 304, frame_y_bot + (BUSH_L)/2,
       'M8 SCREW\n+ DELRIN\nBUSHING', fs=4.5, color=C_DIM, arrow_style='->')
leader(ax1, bell_x_out, (bell_span_top + bell_span_bot)/2.1,
       bell_x_out + 144, (bell_span_top + bell_span_bot)/2.2,
       'BELLOWS\nICP-10', fs=4.5, color=C_DIM, arrow_style='->')

ax1.text(cx_d, carrier_y_bot - 160, '← SCENE (EXTERIOR)    INTERIOR (CONTAINER) →',
         ha='center', fontsize=5, color='#555555')
ax1.text(cx_d, frame_y_top + 200, 'SECTION A-A  (AXES IN mm)',
         ha='center', fontsize=5, color='#333333', style='italic')

out1 = os.path.join(DIAGRAMS_DIR, 'tilt-swing-board-sheet1.png')
fig1.savefig(out1, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white')
plt.close(fig1)
print(f'  → {out1}  Done.')


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Carrier Plate, Bearing & Adjustment Mechanism
# ═══════════════════════════════════════════════════════════════════════════════

FW2, FH2 = 1400, 1000
fig2, ax2 = plt.subplots(figsize=(FW*0.9/25.4, FH*0.9/25.4))
fig2.patch.set_facecolor('white')
ax2.set_facecolor('white')
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_xlim(0, FW2)
ax2.set_ylim(0, FH2)

title_block(ax2, "SHEET 2 OF 3",
            drawing_title="TILT-SWING FRONT BOARD",
            subtitle="Inner Carrier, Bearing & Adjustment mechanism",
            scale_note="AXES IN mm",
            doc_id="TBS-TSB · Tilt-Swing Board")

SC2 = 1
def s2(mm): return mm * SC2

# ── PANEL A: ICP-02 front (exterior) face at 1:2 ──────────────────────────────
ax2.text(30, 980, 'PANEL A — ICP-02 FRONT FACE (1:2)', fontsize=7.5, fontweight='bold')
ax2.plot([30, 660], [974, 974], color='black', lw=0.7)

cx2a, cy2a = 240, 710

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
draw_circle(ax2, cx2a, cy2a, 2.0, lw=0.5, color='white', fill=True, fc='white', zorder=7)

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
           cy2a - s2(CARR_OD/2) - 28, 'Ø320', above=False, fs=5.5, offset=9)
draw_dim_h(ax2, cx2a - s2(PH_BORE/2), cx2a + s2(PH_BORE/2),
           cy2a + s2(CARR_OD/2) + 20, 'Ø90 CONE', above=True, fs=5, offset=9)

leader(ax2, cx2a + s2(PH_CB_D/2) * 0.7, cy2a + s2(PH_CB_D/2) * 0.7,
       cx2a + 70, cy2a + 60,
       'Ø52 × 3 DEEP\nCOUNTERBORE\n(DISC SEAT)', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, cx2a + s2(SOCK_PCD/2) * np.cos(np.radians(-30)),
       cy2a + s2(SOCK_PCD/2) * np.sin(np.radians(-30)),
       cx2a + 120, cy2a - 44,
       '4×Ø16 H7\nSOCKET INSERT\nON Ø260 PCD', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, cx2a + s2(BELL_IN_PCD/2) * np.cos(np.radians(130)),
       cy2a + s2(BELL_IN_PCD/2) * np.sin(np.radians(130)),
       cx2a - 130, cy2a + 70,
       '6×M6 ON\nØ310 PCD\n(BELLOWS)', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, cx2a - s2(PH_DISC_D/2) * 0.7, cy2a - s2(PH_DISC_D/2) * 0.7,
       cx2a - 110, cy2a - 60,
       'Ø50 PINHOLE DISC\nSS-302 SHIM\nØ2.17 APERTURE', fs=5, color=C_DIM, arrow_style='->')

ax2.text(cx2a, cy2a - s2(CARR_OD/2) - 56, 'PANEL A — ICP-02 FRONT FACE (1:2)\nExterior / scene-facing side',
         ha='center', fontsize=5, style='italic', color='#333333')

# ── PANEL B: ICP-02 rear face at 1:2 ─────────────────────────────────────────
ax2.text(680, 980, 'PANEL B — ICP-02 REAR FACE (1:2)', fontsize=7.5, fontweight='bold')
ax2.plot([680, 1280], [974, 974], color='black', lw=0.7)

cx2b, cy2b = 980, 710

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

leader(ax2, cx2b + s2(BRG_SHANK_D/2)*0.7, cy2b + s2(BRG_SHANK_D/2)*0.7,
       cx2b + 60, cy2b + 60,
       'Ø50 k5 SHANK\n× 35 LONG\n(BEARING INNER)', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, cx2b - s2(BELL_ID/2)*0.7, cy2b,
       cx2b - 116, cy2b + 10,
       'Ø290 BELLOWS\nGROOVE\n4 WIDE × 3 DEEP', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, cx2b + s2(SOCK_PCD/2)*np.cos(np.radians(-45)),
       cy2b + s2(SOCK_PCD/2)*np.sin(np.radians(-45)),
       cx2b + 100, cy2b - 40,
       '4×Ø16 H7\nINSERT BORES\n(REAR SIDE)', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, cx2b - s2(8) * 0.7, cy2b - s2(8) * 0.7,
       cx2b - 110, cy2b - 50,
       'M16 TAPPED\nCENTRAL HOLE', fs=5, color=C_DIM, arrow_style='->')

ax2.text(cx2b, cy2b - s2(CARR_OD/2) - 56, 'PANEL B — ICP-02 REAR FACE (1:2)\nBearing-side / interior',
         ha='center', fontsize=5, style='italic', color='#333333')

# ── PANEL C: Bearing section detail (1:1) ─────────────────────────────────────
ax2.text(30, 430, 'PANEL C — GE50-DO-2RS BEARING SECTION (1:1)', fontsize=7.5, fontweight='bold')
ax2.plot([30, 690], [424, 424], color='black', lw=0.7)

cx2c, cy2c = 290, 250

SC1 = 1.0
def s1b(mm): return mm * SC1

# Outer ring (in ICP-01 pocket)
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

# Outer ring top/bottom
or_cap_h = s1b(4)
or_cap_t = mpatches.Rectangle((or_left, or_top - or_cap_h), s1b(BRG_OD), or_cap_h,
                                lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR)
or_cap_b = mpatches.Rectangle((or_left, or_bot), s1b(BRG_OD), or_cap_h,
                                lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR)
ax2.add_patch(or_cap_t); ax2.add_patch(or_cap_b)

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

# PTFE liner gap (vertical lines between inner and outer rings)
ptfe_left_x = cx2c - ir_outer_r + ir_wall + s1b(1)
ptfe_right_x = cx2c + ir_outer_r - ir_wall - s1b(1)
ax2.plot([ptfe_left_x, ptfe_left_x], [ir_y, ir_y + ir_h],
         color=C_GASKT, lw=2.0)
ax2.plot([ptfe_right_x, ptfe_right_x], [ir_y, ir_y + ir_h],
         color=C_GASKT, lw=2.0)

# ICP-01 bore context (frame material either side of bearing)
frame_ctx_w = s1b(20)
fc_l = mpatches.Rectangle((or_left - frame_ctx_w, or_bot), frame_ctx_w, s1b(BRG_W),
                            lw=LW_MED, edgecolor=C_OUT, facecolor=C_ALUM)
fc_r = mpatches.Rectangle((or_right, or_bot), frame_ctx_w, s1b(BRG_W),
                            lw=LW_MED, edgecolor=C_OUT, facecolor=C_ALUM)
ax2.add_patch(fc_l); ax2.add_patch(fc_r)

# ICP-02 shank through bearing
shank_p2 = mpatches.Rectangle((cx2c - s1b(BRG_SHANK_D/2), or_bot - s1b(15)),
                               s1b(BRG_SHANK_D), s1b(BRG_W) + s1b(15),
                               lw=LW_MED, edgecolor=C_OUT, facecolor='#C0C0C0')
ax2.add_patch(shank_p2)

# Seals (EPDM lips each end)
for sy in [or_bot, or_top - s1b(3)]:
    seal_p = mpatches.Rectangle((cx2c - ir_outer_r - s1b(1), sy), s1b(2*ir_outer_r + 2), s1b(3),
                                  lw=0.5, edgecolor=C_OUT, facecolor=C_GASKT)
    ax2.add_patch(seal_p)

# Centerline
ax2.plot([cx2c, cx2c], [or_bot - 40, or_top + 40],
         color=C_CL, lw=LW_THIN, linestyle=(0, (6, 2, 1, 2)))

# Dimensions
draw_dim_h(ax2, or_left - frame_ctx_w, or_right + frame_ctx_w, or_top + 24,
           f'Ø{BRG_OD} OD', above=True, fs=5, offset=7.2)
draw_dim_h(ax2, cx2c - s1b(BRG_ID/2), cx2c + s1b(BRG_ID/2), or_bot - 36,
           f'Ø{BRG_ID} BORE', above=False, fs=5, offset=7.2)
draw_dim_v(ax2, or_right + frame_ctx_w + 20, or_bot, or_top, f'{BRG_W} WIDE', right=True, fs=5, offset=7.2)

leader(ax2, ptfe_right_x, cy2c,
       cx2c + 170, cy2c + 50,
       'PTFE COMPOSITE\nLINING (2RS SEALED)\n±15° MISALIGN', fs=4.8, color=C_DIM, arrow_style='->')
leader(ax2, or_left - frame_ctx_w/2, cy2c,
       cx2c - 150, cy2c - 70,
       'ICP-01\nFRAME\nAl 6061', fs=4.8, color=C_DIM, arrow_style='->')
leader(ax2, cx2c - 30, or_bot - s1b(8),
       cx2c - 110, cy2c - 80,
       'ICP-02\nSHANK\nØ50 k5', fs=4.8, color=C_DIM, arrow_style='->')
leader(ax2, cx2c + ir_outer_r, or_bot + s1b(1.5),
       cx2c + 150, cy2c - 90,
       'RUBBER\nSEAL (2RS)', fs=4.8, color=C_DIM, arrow_style='->')
leader(ax2, or_right - out_ring_wall/2, or_top,
       cx2c + 170, cy2c + 84,
       'OUTER RING\n(PRESS-FIT H7/r6)', fs=4.8, color=C_DIM, arrow_style='->')

ax2.text(cx2c, or_bot - 56, 'SKF GE50-DO-2RS  (or INA / Kaydon equivalent)\nPress-fit outer ring H7/r6  •  Ø50 k5 shank',
         ha='center', fontsize=5, style='italic', color='#333333')

# ── PANEL D: Adjustment screw detail (1:1) ────────────────────────────────────
ax2.text(720, 430, 'PANEL D — ADJUSTMENT SCREW DETAIL (1:1)', fontsize=7.5, fontweight='bold')
ax2.plot([720, 1390], [424, 424], color='black', lw=0.7)

cx2d, cy2d = 848, 260

# Frame boss (outer adapter frame wall in section)
frame_wall_w = s1b(35)
frame_wall_p = mpatches.Rectangle((cx2d - frame_wall_w, cy2d - s1b(30)),
                                   frame_wall_w, s1b(60),
                                   lw=LW_MED, edgecolor=C_OUT, facecolor=C_ALUM)
ax2.add_patch(frame_wall_p)

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
    ax2.plot([tx, tx], [cy2d - s1b(ADJ_D/2) - 2, cy2d + s1b(ADJ_D/2) + 2],
             color=C_HID, lw=0.4, ls='--')

# Knob at right end
knob_p = mpatches.Rectangle((cx2d + screw_len, cy2d - s1b(KNOB_D/2)),
                              s1b(KNOB_H), s1b(KNOB_D),
                              lw=LW_MED, edgecolor=C_OUT, facecolor='#797979')
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
ax2.plot([cx2d - frame_wall_w - 10, cx2d + screw_len + s1b(KNOB_H) + 10],
         [cy2d, cy2d], color=C_CL, lw=LW_THIN, linestyle=(0, (6, 2, 1, 2)))

# Dims and leaders
draw_dim_h(ax2, cx2d, cx2d + screw_len, cy2d + s1b(KNOB_D/2) + 24,
           'M8 × 1.0 × 80 SCREW', above=True, fs=5, offset=7.2)
draw_dim_h(ax2, cx2d - frame_wall_w, cx2d - frame_wall_w + bush_w,
           cy2d - s1b(KNOB_D/2) - 24, f'BUSH L={BUSH_L}', above=False, fs=5, offset=7.2)

leader(ax2, cx2d + screw_len + s1b(KNOB_H)/2, cy2d + s1b(KNOB_D/2),
       cx2d + screw_len + s1b(KNOB_H) + 24, cy2d + 20,
       f'Ø40 KNURLED KNOB\n{FRONT_BOARD_DETENTS}-DETENT\n{FRONT_BOARD_CLICK_DEG}°/CLICK', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, cx2d - frame_wall_w + bush_w/2, cy2d + s1b(BUSH_OD/2),
       cx2d - frame_wall_w - 50, cy2d + 28,
       'DELRIN/POM\nGUIDE BUSHING\nM22×1.0 OD', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, ball_x2 - s1b(8), cy2d - s1b(BALL_D/2),
       ball_x2 - s1b(8) - 110, cy2d - 36,
       '440C SS INSERT\nHEMI SOCKET\nRa 0.4 GROUND', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, ball_x2, cy2d + s1b(BALL_D/2),
       ball_x2 + 28, cy2d + 24,
       'Ø8 Gr25\nCHROME\nSTEEL BALL', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, ball_x2 - carrier_rim_w/2, cy2d + s1b(CARR_THICK/2),
       ball_x2 - carrier_rim_w - 70, cy2d + 50,
       'ICP-02\nCARRIER RIM', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, cx2d - frame_wall_w/2, cy2d + s1b(30),
       cx2d - frame_wall_w/2, cy2d + s1b(30) + 20,
       'ICP-01\nFRAME WALL', fs=5, color=C_DIM, arrow_style='->')

# Angular resolution table — top right of Panel D
tbl_x, tbl_y = 1160, 414
ax2.text(tbl_x, tbl_y, 'ANGULAR RESOLUTION', fontsize=6, fontweight='bold', color='black')
rows = [
    ('Arm radius (pivot→ball)', '130mm'),
    ('Screw pitch', f'{FRONT_BOARD_SCREW_PITCH}mm / turn'),
    ('Linear travel ÷ arm', '1/130 rad/mm = 0.0077°/mm'),
    ('Resolution per turn', '0.44° / turn'),
    ('Detents per turn', f'{FRONT_BOARD_DETENTS}'),
    ('Resolution per click', f'{FRONT_BOARD_CLICK_DEG}° / click'),
    ('Full ±5° range', '~410 clicks (11.4 turns)'),
    ('Hard stop travel', f'±{FRONT_BOARD_TRAVEL_MM}mm = ±{FRONT_BOARD_MAX_DEG}°'),
]
for i, (k, v) in enumerate(rows):
    ry = tbl_y - 20 - i*18
    bg = '#F8F8F8' if i%2==0 else 'white'
    draw_rect(ax2, tbl_x - 4, ry - 14, 220, 18, lw=0.15, color='#DDDDDD', fc=bg, zorder=1)
    ax2.text(tbl_x, ry, k, fontsize=4.5, color='black', zorder=10)
    ax2.text(tbl_x + 136, ry, v, fontsize=4.5, color='black', fontweight='bold', zorder=10)

out2 = os.path.join(DIAGRAMS_DIR, 'tilt-swing-board-sheet2.png')
fig2.savefig(out2, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white')
plt.close(fig2)
print(f'  → {out2}  Done.')


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — Bellows, Locking, Scale & Swap Procedure
# ═══════════════════════════════════════════════════════════════════════════════

FH3_FIG = int(FH * 1.3)
FW3, FH3 = 1400, 1300
fig3, ax3 = plt.subplots(figsize=(FW/25.4*0.9, FH3_FIG/25.4*0.9))
fig3.patch.set_facecolor('white')
ax3.set_facecolor('white')
ax3.set_aspect('equal')
ax3.axis('off')
ax3.set_xlim(0, FW3)
ax3.set_ylim(0, FH3)
S3_UP = FH3 - FH2  # vertical shift = 300

title_block(ax3, "SHEET 3 OF 3",
            drawing_title="TILT-SWING FRONT BOARD",
            subtitle="Bellows seal, Locking, Calibration scale & Swap procedure",
            scale_note="AXES IN mm",
            doc_id="TBS-TSB · Tilt-Swing Board")

# ── PANEL A: Bellows section at 0° and 5° tilt ────────────────────────────────
ax3.text(30, 980 + S3_UP, 'PANEL A — BELLOWS SECTION: NEUTRAL (solid) & 5° TILT (dashed) (1:2)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([30, 960], [974 + S3_UP, 974 + S3_UP], color='black', lw=0.7)

cx3a, cy3a = 400, 860 + S3_UP

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
draw_rect(ax3, cx3a - s2(BELL_OD/2) - 30, cy3a, 30 + s2(BELL_OD) + 30, frame_bar_h,
          lw=LW_MED, color=C_OUT, fc=C_ALUM)
ax3.text(cx3a, cy3a + frame_bar_h/2, 'ICP-01 OUTER FRAME', ha='center', va='center', fontsize=4.5, color='black', zorder=10)

carr_bar_h = s2(10)
# Neutral position carrier
draw_rect(ax3, cx3a - s2(BELL_ID/2) - 20, cy3a - s2(BELL_FREE) - carr_bar_h,
          s2(BELL_ID) + 40, carr_bar_h, lw=LW_MED, color=C_OUT, fc='#C0C0C0')
ax3.text(cx3a, cy3a - s2(BELL_FREE) - carr_bar_h/2,
         'ICP-02 CARRIER (NEUTRAL)', ha='center', va='center', fontsize=4.5, color='black', zorder=10)

# Dimensions
draw_dim_v(ax3, cx3a + s2(BELL_OD/2) + 30, cy3a - s2(BELL_FREE), cy3a,
           f'{BELL_FREE} FREE LEN', right=True, fs=5, offset=9)
draw_dim_h(ax3, cx3a - s2(BELL_OD/2), cx3a + s2(BELL_OD/2), cy3a + frame_bar_h + 28,
           f'OD Ø{BELL_OD}', above=True, fs=5, offset=9)
draw_dim_h(ax3, cx3a - s2(BELL_ID/2), cx3a + s2(BELL_ID/2),
           cy3a - s2(BELL_FREE) - carr_bar_h - 28, f'ID Ø{BELL_ID}', above=False, fs=5, offset=9)

ax3.text(cx3a + s2(BELL_OD/2) + 104, cy3a - s2(BELL_FREE*0.5),
         '——— NEUTRAL (0°)\n- - - - 5° TILT\n(asymmetric compression\nleft side: −13.9mm\nright side: +13.9mm)',
         fontsize=5, va='center', color='#333333', zorder=10)

ax3.text(cx3a, cy3a - s2(BELL_FREE) - carr_bar_h - 60,
         'BELLOWS ICP-10: Matte black neoprene/nylon  •  0.5mm wall  •  4 pleats  •  15mm pleat depth\nInner+outer flanges sealed with Ø4mm neoprene cord gaskets (same spec as wall-frame seal)',
         ha='center', fontsize=5, style='italic', color='#333333', zorder=10)

# ── PANEL B: Locking set screw detail (1:1) ──────────────────────────────────
ax3.text(30, 490 + S3_UP, 'PANEL B — LOCKING SET SCREW (1:1)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([30, 400], [484 + S3_UP, 484 + S3_UP], color='black', lw=0.7)

cx3b, cy3b = 160, 350 + S3_UP

# M8 screw shaft (horizontal)
m8_sh = mpatches.Rectangle((cx3b - 80, cy3b - 8), 160, 16,
                             lw=LW_MED, edgecolor=C_OUT, facecolor=C_STEEL)
ax3.add_patch(m8_sh)
# M6 set screw (vertical, crossing M8)
m6_sh = mpatches.Rectangle((cx3b - 8, cy3b + 8), 16, 50,
                              lw=LW_MED, edgecolor=C_OUT, facecolor=C_STEEL, zorder=5)
ax3.add_patch(m6_sh)
# Nylon tip at bottom
ny_p = mpatches.Rectangle((cx3b - 6, cy3b + 8), 12, 10,
                            lw=0.5, edgecolor=C_OUT, facecolor='#F0E080', zorder=6)
ax3.add_patch(ny_p)
# Hex key socket (top of M6)
ax3.plot([cx3b - 5, cx3b + 5], [cy3b + 58, cy3b + 58], color=C_OUT, lw=2.0)
ax3.plot([cx3b - 3, cx3b - 3], [cy3b + 54, cy3b + 58], color=C_OUT, lw=1.0)
ax3.plot([cx3b + 3, cx3b + 3], [cy3b + 54, cy3b + 58], color=C_OUT, lw=1.0)
# Boss context (frame)
fr3b = mpatches.Rectangle((cx3b - 80, cy3b - 24), 160, 16,
                            lw=LW_MED, edgecolor=C_OUT, facecolor=C_ALUM)
ax3.add_patch(fr3b)
fr3bt = mpatches.Rectangle((cx3b - 16, cy3b + 58), 32, 20,
                             lw=LW_MED, edgecolor=C_OUT, facecolor=C_ALUM)
ax3.add_patch(fr3bt)

leader(ax3, cx3b + 8, cy3b + 36,
       cx3b + 60, cy3b + 40,
       'M6×1.0\nNYLON-TIP\nSET SCREW', fs=5, color=C_DIM, arrow_style='->')
leader(ax3, cx3b + 80, cy3b - 4,
       cx3b + 60, cy3b - 4,
       'M8×1.0\nADJ SCREW\nSHANK', fs=5, color=C_DIM, arrow_style='->')
leader(ax3, cx3b - 8, cy3b + 12,
       cx3b - 80, cy3b + 20,
       'NYLON\nTIP', fs=5, color=C_DIM, arrow_style='->')
ax3.text(cx3b + 6, cy3b + 62, '3mm HEX', fontsize=4.5, color='#333333', zorder=10)
ax3.text(cx3b, cy3b - 56, 'Tighten set screw onto adj screw shank\nafter desired angle is set. 4 off (one per axis)',
         ha='center', fontsize=4.8, style='italic', color='#333333', zorder=10)

# ── PANEL C: Knob detail (2:1) ────────────────────────────────────────────────
ax3.text(430, 490 + S3_UP, 'PANEL C — KNOB DETAIL (2:1)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([430, 840], [484 + S3_UP, 484 + S3_UP], color='black', lw=0.7)

cx3c, cy3c = 610, 350 + S3_UP
SC_knob = 4.0
def sk(mm): return mm * SC_knob

# Knob in section view
knob_rec = mpatches.Rectangle((cx3c - sk(KNOB_H/2), cy3c - sk(KNOB_D/2)),
                                sk(KNOB_H), sk(KNOB_D),
                                lw=LW_THICK, edgecolor=C_OUT, facecolor='#797979')
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
                              lw=0, facecolor='#797979')
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
ax3.text(cx3c, cy3c + sk(KNOB_D/2) + 10, '"TILT +"', fontsize=5, ha='center',
         color='#333333', style='italic', zorder=10)

draw_dim_h(ax3, cx3c - sk(KNOB_H/2), cx3c + sk(KNOB_H/2),
           cy3c - sk(KNOB_D/2) - 24, f'{KNOB_H} WIDE', above=False, fs=5, offset=6)
draw_dim_v(ax3, cx3c + sk(KNOB_H/2) + 24, cy3c - sk(KNOB_D/2), cy3c + sk(KNOB_D/2),
           f'Ø{KNOB_D}', right=True, fs=5, offset=6)

leader(ax3, det_x, cy3c + sk(KNOB_D/2) - sk(2),
       cx3c + 110, cy3c + 24,
       '36-DETENT\nSPRING BALL\n(5° PER CLICK)', fs=5, color=C_DIM, arrow_style='->')
leader(ax3, cx3c + sk(3), cy3c + sk(ADJ_D/2 - 1.5),
       cx3c + 110, cy3c - 20,
       'FLAT/KEYWAY\n(ANTI-SPIN)', fs=5, color=C_DIM, arrow_style='->')

ax3.text(cx3c, cy3c - sk(KNOB_D/2) - 56,
         'Black anodize = TILT axis  |  Natural anodize = SWING axis\nEngraved label on knob face: TILT+ / TILT− / SWING+ / SWING−',
         ha='center', fontsize=5, style='italic', color='#333333', zorder=10)

# ── PANEL D: Angular scale layout ─────────────────────────────────────────────
ax3.text(860, 490 + S3_UP, 'PANEL D — ANGULAR CALIBRATION SCALE (1:1)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([860, 1390], [484 + S3_UP, 484 + S3_UP], color='black', lw=0.7)

cx3d, cy3d = 1060, 350 + S3_UP
arm = 130  # mm arm radius
scale_w_mm = 80  # scale total width in mm

ax3.text(cx3d, 480 + S3_UP, 'Non-linear (tangent) scale: position = 80 × tan(θ)/tan(5°) mm',
         ha='center', fontsize=5, color='#333333', style='italic', zorder=10)

# Draw the scale strip
scale_strip_w = 160
scale_strip_h = 24
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
        ax3.text(x_pos, cy3d - scale_strip_h/2 - 6, f'{deg:+.0f}°',
                 ha='center', va='top', fontsize=4.5, color='black', zorder=10)

ax3.text(cx3d, cy3d, '0', ha='center', va='center', fontsize=6, fontweight='bold', color=C_RED, zorder=10)
ax3.plot([cx3d, cx3d], [cy3d - scale_strip_h/2, cy3d + scale_strip_h/2],
         color=C_RED, lw=1.0)

draw_dim_h(ax3, cx3d - scale_strip_w/2, cx3d + scale_strip_w/2,
           cy3d + scale_strip_h/2 + 20, '80mm TOTAL', above=True, fs=5, offset=6)
ax3.text(cx3d, cy3d - scale_strip_h/2 - 40,
         '2 off — one for TILT, one for SWING\nLaser-engraved Al 80×15×2mm  •  Mounted on ICP-01 face adjacent to each knob pair',
         ha='center', fontsize=5, style='italic', color='#333333', zorder=10)

S3_E_DN = int(FH3 * 0.10)

# ── Separator line between panels B/C/D and panel E ──────────────────────────
ax3.plot([30, 1370], [270 + S3_UP - S3_E_DN, 270 + S3_UP - S3_E_DN], color='#999999', lw=0.5, linestyle='--', zorder=5)

# ── PANEL E: Swap sequence ────────────────────────────────────────────────────
ax3.text(30, 250 + S3_UP - S3_E_DN, 'PANEL E — PLATE SWAP PROCEDURE (TSB ASSY ↔ STANDARD PINHOLE PLATE)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([30, 1390], [244 + S3_UP - S3_E_DN, 244 + S3_UP - S3_E_DN], color='black', lw=0.7)

steps = [
    ('①', 'LOOSEN 4×\nLOCK SCREWS', '3mm hex key\nM6 set screws'),
    ('②', 'ZERO ALL\n4 ADJ KNOBS', 'Return to 0°\nusing scale marks'),
    ('③', 'REMOVE 8×\nM12 BOLTS', 'M12 socket\n65 Nm torque'),
    ('④', 'PULL TSB\nASSEMBLY', 'Dowel pins\nretain alignment'),
    ('⑤', 'FIT STANDARD\nPINHOLE PLATE', 'Locate on same\ndowels — re-bolt'),
]

step_w = 240
step_gap = 30
for i, (num, title, note) in enumerate(steps):
    sx = 40 + i * (step_w + step_gap)
    sy = 120 + S3_UP - S3_E_DN
    draw_rect(ax3, sx, sy, step_w, 110, lw=1.0, color='black', fc='#F0F0F0')
    ax3.text(sx + step_w/2, sy + 96, num, ha='center', fontsize=14,
             fontweight='bold', color='black', zorder=10)
    ax3.text(sx + step_w/2, sy + 64, title, ha='center', fontsize=6.5,
             fontweight='bold', color='black', zorder=10)
    ax3.text(sx + step_w/2, sy + 24, note, ha='center', fontsize=5.5,
             color='#555555', style='italic', zorder=10)
    if i < 4:
        ax3.annotate('', xy=(sx + step_w + 26, sy + 54), xytext=(sx + step_w + 4, sy + 54),
                     arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

ax3.text(1390/2, 90 + S3_UP - S3_E_DN, 'No special tooling required beyond M12 socket and 3mm hex key  •  Swap time: approx. 10 minutes',
         ha='center', fontsize=5.5, color='#333333', style='italic', zorder=10)

out3 = os.path.join(DIAGRAMS_DIR, 'tilt-swing-board-sheet3.png')
fig3.savefig(out3, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white')
plt.close(fig3)
print(f'  → {out3}  Done.')
