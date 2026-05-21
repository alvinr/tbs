#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_water_system.py
Generates four engineering diagrams for the cyanotype processing water system:
  Sheet 1 — System flow schematic (three-system P&ID overview)
  Sheet 2 — Tank & filter skid layout plan (dimensioned arrangement)
  Sheet 3 — Processing tray drainage plan (slope direction, flow arrows, drain)
  Sheet 4 — Processing tray drain cross-section (elevation through drain fitting)

Output:
  water-system-sheet1.png  (1800 x 1200 px, 150 dpi)
  water-system-sheet2.png  (1800 x 1200 px, 150 dpi)
  water-system-sheet3.png  (1800 x 1200 px, 150 dpi)
  water-system-sheet4.png  (1800 x 1200 px, 150 dpi)
"""

import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Arc
from matplotlib.lines import Line2D
from tbs_constants import (
    C_LEN, C_WID, C_HGT, IBC_COL_X, IBC_W, IBC_D, IBC_H_600, IBC_H_STK,
    ZONE_L_END, ZONE_R_START,
    FP_X_L, FP_X_R, PH_X,
    BLUE_IBC_Y, BROWN_IBC_Y, IBC_FAR_Y, WASTE_IBC_Y,
    PUMP_X, PUMP_W, PUMP_H_LO, PUMP_H_HI, PUMP_D,
    EQPANEL_X, EQPANEL_W, CORRIDOR_YD_NEAR,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_W, PROC_TRAY_D,
    PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR, PROC_TRAY_RIM, PROC_TRAY_PITCH,
    PROC_TRAY_DRAIN_X, PROC_TRAY_DRAIN_YD,
    PROC_TRAY_SUMP_W, PROC_TRAY_SUMP_D, PROC_TRAY_SUMP_Z,
    PROC_TRAY_SHIM_H, PROC_TRAY_SHIM_W, PROC_TRAY_SHIM_N,
    WALKWAY_W, WALKWAY_NEAR_YD, WALKWAY_FAR_YD,
    C_BLUE_IBC, C_BROWN_IBC, C_WASTE_IBC, C_PUMP, C_WALL,
    svg_path, SVG_DIR,
)
import os
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_notes

# ── Colour palette ────────────────────────────────────────────────────────────
C_BLUE   = "#2979B8"   # clean water — Blue system
C_BROWN  = "#8B5E3C"   # used / grey water — Brown system
C_BLACK  = "#222222"   # waste water — Black system
C_BLUE_L = "#D6E9F8"   # blue system fill (light)
C_BROWN_L= "#F0E0CC"   # brown system fill (light)
C_BLACK_L= "#DDDDDD"   # black system fill (light)
C_PROC   = "#E8F5E9"   # processing area fill
C_FILT   = "#FFF9C4"   # filter skid fill
C_FRAME  = "#444444"   # drawing frame
C_DIM    = "#888888"   # dimension lines
C_TEXT   = "#111111"
C_TITLE  = "#1A237E"

LW_PIPE  = 2.8         # pipe linewidth
LW_THIN  = 1.2

# ── Helper: draw a pipe segment ───────────────────────────────────────────────
def pipe(ax, x1, y1, x2, y2, color=C_BLUE, lw=LW_PIPE, style="-", zorder=3):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, ls=style,
            solid_capstyle="round", zorder=zorder)

def arrow_pipe(ax, x1, y1, x2, y2, color=C_BLUE, lw=LW_PIPE, zorder=4):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=lw, mutation_scale=14),
                zorder=zorder)

def box(ax, x, y, w, h, fc="white", ec=C_FRAME, lw=1.2, zorder=2, radius=0.02):
    r = FancyBboxPatch((x - w/2, y - h/2), w, h,
                       boxstyle=f"round,pad={radius}",
                       fc=fc, ec=ec, lw=lw, zorder=zorder)
    ax.add_patch(r)

def tank(ax, x, y, w, h, fc="white", ec=C_FRAME, label="", sublabel="",
         lw=1.4, zorder=2):
    """Draw an IBC-tote-style tank (rectangle with fill level indicator)."""
    rect = plt.Rectangle((x - w/2, y - h/2), w, h, fc=fc, ec=ec, lw=lw, zorder=zorder)
    ax.add_patch(rect)
    # legs
    leg_h = 0.03
    for dx in [-w/2 + 0.02, w/2 - 0.02]:
        ax.plot([x + dx, x + dx], [y - h/2 - leg_h, y - h/2],
                color=ec, lw=lw, zorder=zorder)
    # label
    if label:
        ax.text(x - 0.5, y + 0.55, label, ha="center", va="center",
                fontsize=7.5, fontweight="bold", color=C_TEXT, zorder=zorder + 1)
    if sublabel:
        ax.text(x, y - 0.06, sublabel, ha="center", va="center",
                fontsize=6.5, color="#555555", zorder=zorder + 1)

def pump(ax, x, y, color=C_BLUE, zorder=5, r=0.1125):
    """Draw a centrifugal pump symbol (circle with triangle arrow)."""
    circ = plt.Circle((x, y), r, fc="white", ec=color, lw=2.8, zorder=zorder)
    ax.add_patch(circ)
    # Triangle inside
    tri = plt.Polygon([(x - r*0.55, y - r*0.55),
                       (x - r*0.55, y + r*0.55),
                       (x + r*0.65, y)],
                      fc=color, ec=color, zorder=zorder + 1)
    ax.add_patch(tri)

def valve(ax, x, y, color=C_BLUE, zorder=5, size=0.06, label="V"):
    """Draw a ball valve symbol (bowtie inside white circle)."""
    r = size * 1.6
    circ = plt.Circle((x, y), r, fc="white", ec=color, lw=2.0, zorder=zorder)
    ax.add_patch(circ)
    tri1 = plt.Polygon([(x - size, y - size),
                        (x - size, y + size),
                        (x, y)],
                       fc=color, ec=color, alpha=0.85, zorder=zorder + 1)
    tri2 = plt.Polygon([(x + size, y - size),
                        (x + size, y + size),
                        (x, y)],
                       fc=color, ec=color, alpha=0.85, zorder=zorder + 1)
    ax.add_patch(tri1)
    ax.add_patch(tri2)

def filter_sym(ax, x, y, color=C_FILT, zorder=4, label="F"):
    """Draw a filter symbol (pentagon/diamond)."""
    size = 0.126       # +20% from 0.105
    h    = 0.162       # +20% from 0.135
    pts  = [(x, y + h*0.6),
            (x + size*0.7, y + h*0.2),
            (x + size*0.5, y - h*0.5),
            (x - size*0.5, y - h*0.5),
            (x - size*0.7, y + h*0.2)]
    poly = plt.Polygon(pts, fc=color, ec=C_FRAME, lw=1.5, zorder=zorder)
    ax.add_patch(poly)
    ax.text(x, y, label, ha="center", va="center", fontsize=6.4, zorder=zorder + 1,
            fontweight="bold")

def ext_port(ax, x, y, color=C_BLUE, zorder=5, label="F1", size=0.12):
    """Draw an external bulkhead port symbol — hexagon (flange) with line stub."""
    # Hexagon
    angles = np.linspace(0, 2 * np.pi, 7)
    hx = x + size * np.cos(angles)
    hy = y + size * np.sin(angles)
    poly = plt.Polygon(np.column_stack([hx, hy]),
                        fc="white", ec=color, lw=2.2, zorder=zorder)
    ax.add_patch(poly)
    ax.text(x, y, label, ha="center", va="center", fontsize=5.5,
            fontweight="bold", color=color, zorder=zorder + 1)

def note(ax, x, y, txt, fs=6.5, color=C_TEXT):
    ax.text(x, y, txt, ha="left", va="center", fontsize=fs, color=color,
            zorder=10)

def pipe_bridge(ax, x, y, direction='h', r=0.14, color=C_FRAME, lw=LW_PIPE,
                zorder=11, bg='white', style='-'):
    """Draw a pipe-crossing bridge hump on the 'over' pipe.
    direction: 'h' = bridging pipe is horizontal (arc humps upward)
               'v' = bridging pipe is vertical (arc humps rightward)
    bg: fill color under the arc — match to the zone background.
    """
    if direction == 'h':
        theta = np.linspace(0, np.pi, 40)
        bx = x + r * np.cos(theta)
        by = y + r * np.sin(theta)
    else:
        theta = np.linspace(-np.pi / 2, np.pi / 2, 40)
        bx = x + r * np.cos(theta)
        by = y + r * np.sin(theta)
    ax.fill(bx, by, color=bg, zorder=zorder - 1)
    ax.plot(bx, by, color=color, lw=lw, ls=style, zorder=zorder, solid_capstyle='round')

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — SYSTEM FLOW SCHEMATIC (P&ID overview)
# ═══════════════════════════════════════════════════════════════════════════════

fig1, ax1 = plt.subplots(figsize=(18, 12))
ax1.set_xlim(0, 18)
ax1.set_ylim(0, 12)
ax1.set_aspect("equal")
ax1.axis("off")
ax1.set_facecolor("#F5F5F0")
fig1.patch.set_facecolor("#F5F5F0")

# ── Title block ───────────────────────────────────────────────────────────────
ax1.add_patch(plt.Rectangle((0, 0), 18, 12, fc="#F5F5F0", ec=C_FRAME, lw=2))
title_block(ax1, "SHEET 1 OF 3",
            drawing_title="WATER SYSTEM",
            subtitle="System flow schematic (P&ID)",
            scale_note="Not to scale",
            doc_id="TBS-001 · Water System")

# ── Zone fills ────────────────────────────────────────────────────────────────
# Blue zone
ax1.add_patch(plt.Rectangle((0.3, 1.3), 4.5, 9.4, fc=C_BLUE_L, ec=C_BLUE,
                             lw=1.5, alpha=0.45, zorder=1))
ax1.text(2.55, 10.5, "BLUE SYSTEM — CLEAN WATER", ha="center", fontsize=8,
         fontweight="bold", color=C_BLUE, zorder=5)

# Brown zone
ax1.add_patch(plt.Rectangle((5.1, 1.3), 4.5, 9.4, fc=C_BROWN_L, ec=C_BROWN,
                             lw=1.5, alpha=0.45, zorder=1))
ax1.text(7.35, 10.5, "BROWN SYSTEM — USED WATER (RECYCLABLE)",
         ha="center", fontsize=8, fontweight="bold", color=C_BROWN, zorder=5)

# Black zone
ax1.add_patch(plt.Rectangle((9.9, 1.3), 3.5, 9.4, fc=C_BLACK_L, ec=C_BLACK,
                             lw=1.5, alpha=0.35, zorder=1))
ax1.text(11.65, 10.5, "BLACK SYSTEM — WASTE WATER",
         ha="center", fontsize=8, fontweight="bold", color=C_BLACK, zorder=5)

# Processing area
ax1.add_patch(plt.Rectangle((13.6, 1.3), 4.1, 9.4, fc=C_PROC, ec="#388E3C",
                             lw=1.5, alpha=0.6, zorder=1))
ax1.text(15.65, 10.5, "PROCESSING AREA",
         ha="center", fontsize=8, fontweight="bold", color="#2E7D32", zorder=5)

# ── Shared geometry constants (used across multiple systems) ──────────────────
W_X  = 11.65                # waste IBC center X (centered in Black zone 9.9–13.4)
W_Y  = 7.5                  # waste IBC center Y (raised)
W_W  = 1.4                  # waste IBC box width (same as other IBCs on schematic)
W_H  = 1.4                  # waste IBC box height
BR   = 0.14                 # pipe-crossing bridge hump radius

# ── BLUE SYSTEM ───────────────────────────────────────────────────────────────
# IBC1 Clean water A
tank(ax1, 1.5, 8.2, 1.4, 1.4, fc="#BBDEFB", ec=C_BLUE_IBC, lw=2,
     label="IBC-1", sublabel="159 gal (600L)\nCLEAN A")
# IBC2 Clean water B
tank(ax1, 3.3, 8.2, 1.4, 1.4, fc="#BBDEFB", ec=C_BLUE_IBC, lw=2,
     label="IBC-2", sublabel="159 gal (600L)\nCLEAN B")

# Manifold joining two tanks
VR = 0.06 * 1.6  # standard valve circle radius = 0.096
pipe(ax1, 1.5, 7.48, 1.5, 7.0, C_BLUE)
pipe(ax1, 3.3, 7.48, 3.3, 7.0, C_BLUE)
pipe(ax1, 1.5, 7.0, 2.4 - VR, 7.0, C_BLUE)   # left crossmember → valve edge
pipe(ax1, 2.4 + VR, 7.0, 3.3, 7.0, C_BLUE)   # valve edge → right crossmember

# Valve on outlet
valve(ax1, 2.4, 7.0, color=C_BLUE)
ax1.text(2.4, 7.14, "BV-01", ha="center", fontsize=6, color=C_BLUE)

# Pump P1
PR = 0.1125  # pump radius
pipe(ax1, 2.4, 7.0 - VR, 2.4, 6.3 + PR, C_BLUE)
arrow_pipe(ax1, 2.4, 6.85, 2.4, 6.5, color=C_BLUE)
pump(ax1, 2.4, 6.3, color=C_PUMP)
ax1.text(2.60, 6.2, "P-01\n12VDC\n3.5 GPM", ha="left", fontsize=6, color=C_PUMP)

# Pressure accumulator
pipe(ax1, 2.4, 6.3 - PR, 2.4, 5.6, C_BLUE)
box(ax1, 2.4, 5.35, 0.8, 0.45, fc="#E3F2FD", ec=C_BLUE, lw=1.5)
ax1.text(2.4, 5.35, "ACC-01\n1 GAL", ha="center", va="center",
         fontsize=6, color=C_BLUE)

# Valve + run to processing
pipe(ax1, 2.4, 5.12, 2.4, 4.5 + VR, C_BLUE)
arrow_pipe(ax1, 2.4, 4.95, 2.4, 4.65, color=C_BLUE)
valve(ax1, 2.4, 4.5, color=C_BLUE)
ax1.text(2.70, 4.47, "BV-02", ha="center", fontsize=6, color=C_BLUE)
pipe(ax1, 2.4, 4.5 - VR, 2.4, 3.8, C_BLUE)
# Run east to spray bar riser tap-off — humps over filter verticals, blue return, waste vertical
pipe(ax1, 2.4, 3.8, 14.5, 3.8, C_BLUE)
pipe_bridge(ax1, 6.0,   3.8, color=C_BLUE, lw=LW_PIPE, bg=C_FILT)     # over F1 vertical
pipe_bridge(ax1, 7.1,   3.8, color=C_BLUE, lw=LW_PIPE, bg=C_FILT)     # over F2 vertical
pipe_bridge(ax1, 8.2,   3.8, color=C_BLUE, lw=LW_PIPE, bg=C_FILT)     # over F3 vertical
pipe_bridge(ax1, 9.7,   3.8, color=C_BLUE, lw=LW_PIPE, bg=C_BROWN_L)  # over blue return
pipe_bridge(ax1, W_X,   3.8, color=C_BLUE, lw=LW_PIPE, bg=C_BLACK_L)  # over waste vertical
ax1.text(12.75, 4.0, "1\" HDPE — BLUE (SUPPLY)", ha="center",
         fontsize=7, color=C_BLUE)

# Chemistry prep tap — tee off blue supply at shelf location
TAP_SCH_X = 12.0   # schematic X position for tap branch
pipe(ax1, TAP_SCH_X, 3.8, TAP_SCH_X, 3.3 + VR, C_BLUE)
valve(ax1, TAP_SCH_X, 3.3, color=C_BLUE)
ax1.text(TAP_SCH_X + 0.30, 3.30, "BV-06", ha="center", fontsize=6, color=C_BLUE)
tap_y = 2.36
pipe(ax1, TAP_SCH_X, 3.3 - VR, TAP_SCH_X, tap_y, C_BLUE)
pipe_bridge(ax1, TAP_SCH_X, 2.6, direction='v', color=C_BLUE, lw=LW_PIPE, bg=C_BLACK_L)  # over black waste line
# Tap symbol (inverted triangle)
ax1.plot([TAP_SCH_X - 0.2, TAP_SCH_X + 0.2, TAP_SCH_X, TAP_SCH_X - 0.2],
         [tap_y, tap_y, tap_y - 0.3, tap_y],
         color=C_BLUE, lw=2.0, solid_capstyle="round", zorder=5)
ax1.plot([TAP_SCH_X, TAP_SCH_X], [tap_y - 0.3, tap_y - 0.5],
         color=C_BLUE, lw=2.0, zorder=5)
ax1.text(TAP_SCH_X, tap_y - 0.7, "TAP-01\n(CHEM PREP)", ha="center",
         fontsize=6, color=C_BLUE)

# External fill ports (top of IBCs, via bulkhead fittings in end wall — gravity feed)
pipe(ax1, 1.5, 8.9, 1.5, 9.5, C_BLUE)
arrow_pipe(ax1, 1.5, 9.4, 1.5, 9.0, color=C_BLUE)               # downward fill flow
ext_port(ax1, 1.5, 9.65, color=C_BLUE, label="X1")
ax1.text(1.5, 9.95, "EXT. FILL\n2\" NPT\nGRAVITY", ha="center", fontsize=5.5,
         color=C_BLUE, style="italic")
pipe(ax1, 3.3, 8.9, 3.3, 9.5, C_BLUE)
arrow_pipe(ax1, 3.3, 9.4, 3.3, 9.0, color=C_BLUE)               # downward fill flow
ext_port(ax1, 3.3, 9.65, color=C_BLUE, label="X2")
ax1.text(3.3, 9.95, "EXT. FILL\n2\" NPT\nGRAVITY", ha="center", fontsize=5.5,
         color=C_BLUE, style="italic")

# Water level sensor labels
ax1.text(4.8, 8.2, "LOW-LEVEL\nFLOAT SW.", ha="center",
         fontsize=5.5, color=C_BLUE, alpha=0.8)
ax1.plot([4.5, 3.95], [8.2, 8.2], color=C_BLUE, lw=0.8, ls=":")

# ── BROWN SYSTEM ──────────────────────────────────────────────────────────────
# IBC3 — used water buffer
tank(ax1, 6.4, 8.2, 1.4, 1.4, fc="#D7CCC8", ec=C_BROWN_IBC, lw=2,
     label="IBC-3", sublabel="159 gal (600L)\nUSED BUFFER")

# Inlet from processing floor drain
pipe(ax1, 6.4, 7.48, 6.4, 7.0 + VR, C_BROWN)
valve(ax1, 6.4, 7.0, color=C_BROWN)
ax1.text(6.75, 6.97, "BV-03", ha="center", fontsize=6, color=C_BROWN)
pipe(ax1, 6.4, 7.0 - VR, 6.4, 6.3, C_BROWN)
# Arrow from processing area — humps over blue return (X=9.7) and waste vertical (W_X)
pipe(ax1, 6.4, 6.3, 15.1, 6.3, C_BROWN, style="--")
pipe_bridge(ax1, 9.7,   6.3, color=C_BROWN, lw=LW_PIPE, bg=C_BROWN_L, style="--")
pipe_bridge(ax1, W_X,   6.3, color=C_BROWN, lw=LW_PIPE, bg=C_BLACK_L, style="--")
pipe_bridge(ax1, 14.5,  6.3, color=C_BROWN, lw=LW_PIPE, bg=C_PROC, style="--")
arrow_pipe(ax1, 6.6, 6.3, 6.4, 6.3, color=C_BROWN)
ax1.text(8.1, 6.1, "1\" HDPE — BROWN (DRAIN FROM FLOOR)", ha="center",
         fontsize=7, color=C_BROWN)

# Brown pump P2 — outlet from bottom of IBC-3
pipe(ax1, 6.4, 7.0 - VR, 6.4, 5.4 + PR, C_BROWN)
arrow_pipe(ax1, 6.4, 6.8, 6.4, 5.8, color=C_BROWN)       # downward from IBC-3
pump(ax1, 6.4, 5.4, color=C_PUMP)
ax1.text(6.60, 5.3, "P-02\n12VDC\n3.5 GPM", ha="left", fontsize=6, color=C_PUMP)

pipe(ax1, 6.4, 5.4 - PR, 6.4, 4.6, C_BROWN)

# ── Brown drain-out — IBC-3 to exterior drain port D3 via P-05 ───────────
# Separate drain circuit from left side of IBC-3 (right side feeds P-02 recirculation)
BD_X = 5.35
pipe(ax1, 5.7, 8.0, BD_X + VR, 8.0, C_BROWN)        # stub from IBC left edge → valve edge
valve(ax1, BD_X, 8.0, color=C_BROWN)
ax1.text(BD_X - 0.15, 7.95, "BV-07", ha="right", fontsize=6, color=C_BROWN)
pipe(ax1, BD_X, 8.0 + VR, BD_X, 8.85 - PR, C_BROWN) # valve top → pump bottom
pump(ax1, BD_X, 8.85, color=C_PUMP)
ax1.text(BD_X - 0.15, 8.75, "P-05\n12VDC", ha="right", fontsize=6, color=C_PUMP)
pipe(ax1, BD_X, 8.85 + PR, BD_X, 9.5, C_BROWN)        # up from pump top → ext port
arrow_pipe(ax1, BD_X, 9.3, BD_X, 9.45, color=C_BROWN)
ext_port(ax1, BD_X, 9.65, color=C_BROWN, label="X3")
ax1.text(BD_X, 9.95, "EXT. DRAIN\n2\" NPT", ha="center", fontsize=5.5,
         color=C_BROWN, style="italic", va="bottom")

# ── FILTER SKID ───────────────────────────────────────────────────────────────
ax1.add_patch(plt.Rectangle((5.2, 3.0), 3.8, 2.0, fc=C_FILT, ec="#F57F17",
                             lw=1.5, alpha=0.8, zorder=1))
ax1.text(7.1, 4.88, "FILTER SKID", ha="center", fontsize=7.5,
         fontweight="bold", color="#E65100")

# Filter 1 — 50 micron sediment (symbol above blue supply bridge humps)
filter_sym(ax1, 6.0, 4.2, label="F1")
ax1.text(6.6, 3.35, "50μ\nSEDIMENT", ha="center", fontsize=6, color="#E65100")
pipe(ax1, 6.4, 4.6, 6.0, 4.6, C_BROWN)
arrow_pipe(ax1, 6.3, 4.6, 6.1, 4.6, color=C_BROWN)       # leftward to F1
pipe(ax1, 6.0, 4.6, 6.0, 4.33, C_BROWN)
pipe(ax1, 6.0, 4.07, 6.0, 3.25, C_BROWN)

# Filter 2 — 5 micron sediment
filter_sym(ax1, 7.1, 4.2, label="F2")
ax1.text(7.6, 3.35, "5μ\nSEDIMENT", ha="center", fontsize=6, color="#E65100")
pipe(ax1, 6.0, 3.25, 7.1, 3.25, C_BROWN)
arrow_pipe(ax1, 6.4, 3.25, 6.8, 3.25, color=C_BROWN)     # rightward F1→F2
pipe(ax1, 7.1, 3.25, 7.1, 4.07, C_BROWN)
pipe(ax1, 7.1, 4.33, 7.1, 4.6, C_BROWN)
arrow_pipe(ax1, 7.1, 4.45, 7.1, 4.55, color=C_BROWN)     # upward F2 out

# Filter 3 — GAC carbon
filter_sym(ax1, 8.2, 4.2, label="F3")
ax1.text(8.6, 3.35, "GAC\nCARBON", ha="center", fontsize=6, color="#E65100")
pipe(ax1, 7.1, 4.6, 8.2, 4.6, C_BROWN)
arrow_pipe(ax1, 7.5, 4.6, 7.9, 4.6, color=C_BROWN)       # rightward F2→F3
pipe(ax1, 8.2, 4.6, 8.2, 4.33, C_BROWN)
pipe(ax1, 8.2, 4.07, 8.2, 3.25, C_BROWN)

# pH test point
pipe(ax1, 8.2, 3.25, 8.9, 3.25, C_BROWN)
arrow_pipe(ax1, 8.6, 3.25, 9.1, 3.25, color=C_BROWN)     # rightward to DV-01
box(ax1, 9.15, 3.25, 0.45, 0.35, fc="#FFF176", ec="#F9A825", lw=1.5)
ax1.text(9.15, 3.25, "pH\nTEST", ha="center", va="center", fontsize=5.5,
         color="#E65100")

# ── DIVERTER VALVE after filter — back to Blue OR forward to Black ─────────────
DVR = 0.075 * 1.6  # diverter valve circle radius = 0.12
pipe(ax1, 9.4, 3.25, 9.7 - DVR, 3.25, C_BROWN)
valve(ax1, 9.7, 3.25, color="#777777", size=0.075)
ax1.text(9.7, 2.9, "3W-DV-01\nDIVERTER", ha="center", fontsize=6, color="#444")

# Path back to Blue IBC — up at X=9.7, left at Y=9.2 (below F2 fill port), down to IBC-2
RET_Y = 9.2   # return horizontal — below ext fill ports at Y=9.65
pipe(ax1, 9.7, 3.25 + DVR,  9.7, 3.8 - BR,  C_BLUE, style="--")   # below blue supply
pipe(ax1, 9.7, 3.8 + BR,   9.7, 6.3 - BR,  C_BLUE, style="--")   # between crossings
pipe(ax1, 9.7, 6.3 + BR,   9.7, RET_Y,     C_BLUE, style="--")   # above brown drain → return level
arrow_pipe(ax1, 9.7, 7.0, 9.7, 7.3, color=C_BLUE)                # short upward return arrow
pipe(ax1, 9.7, RET_Y, 3.3, RET_Y, C_BLUE, style="--")            # left to X2 fill line
pipe_bridge(ax1, BD_X, RET_Y, color=C_BLUE, lw=LW_PIPE, bg=C_BROWN_L, style="--")  # over brown drain-out pipe
arrow_pipe(ax1, 5.0, RET_Y, 4.7, RET_Y, color=C_BLUE)            # short leftward return arrow
ax1.text(6.5, RET_Y + 0.15, "RECYCLED → BLUE IBC-2 (if pH & clarity OK)",
         ha="center", fontsize=6, color=C_BLUE, style="italic")

# Path to Black system — right from DV-01 at Y=3.25, then up via W_X vertical
DV01_R = 0.075 * 1.6  # diverter valve circle radius
pipe(ax1, 9.7 + DV01_R, 3.25, W_X, 3.25, C_BLACK)
arrow_pipe(ax1, 10.3, 3.25, W_X - 0.1, 3.25, color=C_BLACK)  # rightward to waste vertical

# ── BLACK SYSTEM ──────────────────────────────────────────────────────────────
tank(ax1, W_X, W_Y, W_W, W_H, fc="#D5D5D0", ec=C_WASTE_IBC, lw=2,
     label="IBC-4", sublabel="159 gal (600L)\nWASTE")

# Waste IBC vertical — DV-01 feeds at Y=3.25, DV-02 black feeds at Y=2.6
pipe(ax1, W_X, 2.6,       W_X, 3.8 - BR,  C_BLACK)   # DV-02 feed to blue crossing
pipe(ax1, W_X, 3.8 + BR,  W_X, 6.3 - BR,  C_BLACK)   # blue crossing to brown crossing
pipe(ax1, W_X, 6.3 + BR,  W_X, W_Y - W_H/2,  C_BLACK)  # brown crossing to IBC bottom
arrow_pipe(ax1, W_X, 3.4, W_X, 4.5,       color=C_BLACK)   # upward flow (lower)
arrow_pipe(ax1, W_X, 6.5, W_X, W_Y - W_H/2 - 0.1, color=C_BLACK)  # upward (upper)

# ── Waste drain-out — IBC-4 to exterior drain port D4 via P-03 ────────────
# Separate outlet from right side of IBC-4 (left side carries waste inflow)
WD_X = 12.6
pipe(ax1, W_X + W_W/2, 7.8, WD_X + VR, 7.8, C_BLACK)   # stub from IBC right edge → valve
valve(ax1, WD_X, 7.8, color=C_BLACK)
ax1.text(WD_X + 0.15, 7.75, "BV-08", ha="left", fontsize=6, color=C_BLACK)
pipe(ax1, WD_X, 7.8 + VR, WD_X, 8.7 - PR, C_BLACK)     # valve top → pump bottom
pump(ax1, WD_X, 8.7, color=C_PUMP)
ax1.text(WD_X + 0.15, 8.65, "P-03\n12VDC", ha="left", fontsize=6, color=C_PUMP)
pipe(ax1, WD_X, 8.7 + PR, WD_X, 9.5, C_BLACK)           # pump top → ext port
arrow_pipe(ax1, WD_X, 9.3, WD_X, 9.45, color=C_BLACK)
ext_port(ax1, WD_X, 9.65, color=C_BLACK, label="X4")
ax1.text(WD_X, 9.95, "EXT. DRAIN\n2\" NPT", ha="center", fontsize=5.5,
         color=C_BLACK, style="italic", va="bottom")

# ── PROCESSING AREA ───────────────────────────────────────────────────────────
ax1.add_patch(plt.Rectangle((13.7, 3.5), 3.8, 5.5, fc="#C8E6C9", ec="#388E3C",
                             lw=1.5, zorder=2))
ax1.text(15.6, 8.8, "PROCESSING TRAY (304 SS)", ha="center", fontsize=7.5,
         fontweight="bold", color="#2E7D32")
ax1.text(15.6, 8.5, "(50mm rim, 1:200 pitch, permanent)", ha="center",
         fontsize=6.5, color="#388E3C")

# Print on floor representation
ax1.add_patch(plt.Rectangle((14.1, 5.0), 3.0, 3.1, fc="white", ec="#66BB6A",
                             lw=1.2, ls="--", alpha=0.8, zorder=3))
ax1.text(15.6, 6.55, f"PRINT\n({C_LEN} × {C_HGT} mm)", ha="center", va="center",
         fontsize=7, color="#388E3C", style="italic", zorder=4)


# Floor drain
circle_drain = plt.Circle((15.6, 4.15), 0.15, fc="white", ec="#388E3C", lw=1.5,
                            zorder=4)
ax1.add_patch(circle_drain)
ax1.plot([15.45, 15.75], [4.15, 4.15], color="#388E3C", lw=1.2, zorder=5)
ax1.plot([15.6, 15.6], [4.0, 4.3], color="#388E3C", lw=1.2, zorder=5)
ax1.text(15.6, 4.4, "TRAY DRAIN", ha="center",
         fontsize=6, color="#388E3C")

# P-04 pump — suction from tray sump, discharge to diverter
PUMP_R = 0.1125
pipe(ax1, 15.6, 4.0, 15.6, 3.65 + PUMP_R, C_BROWN)              # drain → P-04
pump(ax1, 15.6, 3.65, color=C_PUMP)
ax1.text(15.80, 3.60, "P-04\n12VDC", ha="left", fontsize=6, color=C_PUMP)

# 3-way diverter valve below P-04
DV02_Y = 3.05
DV02_R = 0.075 * 1.6   # diverter valve circle radius = 0.12
pipe(ax1, 15.6, 3.65 - PUMP_R, 15.6, DV02_Y + DV02_R, C_BROWN)  # P-04 → DV-02
valve(ax1, 15.6, DV02_Y, color="#777777", size=0.075)
ax1.text(16.00, DV02_Y, "3W-DV-02", ha="center", fontsize=6, color="#444")

# to brown: short horizontal from valve left to brown return riser (dashed — return flow)
pipe(ax1, 15.1, DV02_Y, 15.6 - DV02_R, DV02_Y, C_BROWN, style="--")  # valve → brown return
pipe(ax1, 15.1, DV02_Y, 15.1, 6.3, C_BROWN, style="--")              # brown return riser
arrow_pipe(ax1, 15.1, 5.5, 15.1, 5.8, color=C_BROWN)             # short upward drain return arrow

# to black: diverter outlet → down → left to waste IBC vertical
pipe(ax1, 15.6, DV02_Y - DV02_R, 15.6, 2.6, C_BLACK)
pipe(ax1, 15.6, 2.6, W_X,  2.6, C_BLACK)
arrow_pipe(ax1, 14.5, 2.6, 12.5, 2.6, color=C_BLACK)
ax1.text(13.5, 2.42, "TO WASTE IBC-4 (HEAVY CONTAM.)", ha="center", fontsize=6,
         color=C_BLACK, style="italic")

# Spray bar riser — blue supply tap-off at Y=3.8 up to spray bar at Y=8.0
# Brown drain (Y=6.3) bridges over; riser is split with gap at crossing
pipe(ax1, 14.5, 3.8,       14.5, 4.4 - VR,  C_BLUE)    # riser to valve bottom
valve(ax1, 14.5, 4.4, color=C_BLUE)                      # BV-05 spray bar shutoff
ax1.text(14.65, 4.38, "BV-05", ha="left", fontsize=6, color=C_BLUE)
pipe(ax1, 14.5, 4.4 + VR,  14.5, 6.3 - BR,  C_BLUE)    # valve top to brown crossing
pipe(ax1, 14.5, 6.3 + BR,  14.5, 8.0,        C_BLUE)    # above brown drain
arrow_pipe(ax1, 14.5, 5.0, 14.5, 6.8, color=C_BLUE)     # upward flow to spray bar

# Spray bar / flood hose symbol
pipe(ax1, 14.5, 8.0, 16.8, 8.0, C_BLUE)
for xd in [14.7, 15.2, 15.7, 16.2, 16.7]:
    ax1.annotate("", xy=(xd, 7.7), xytext=(xd, 7.95),
                 arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=1.5,
                                 mutation_scale=10), zorder=5)
ax1.text(15.65, 8.2, "FLOOD/SPRAY BAR (3/4\" HDPE)",
         ha="center", fontsize=6.5, color=C_BLUE)

# ── Legend ────────────────────────────────────────────────────────────────────
# Boxes bottom-aligned with Blue/Brown system zones (system box bottom = Y=1.3)
BOX_W = 4.5    # matches Blue/Brown System box width
BOX_H = 1.5
BOX_X = 0.3    # Blue System left edge
BOX_Y = 1.3    # bottom of system boxes
lx = BOX_X + 0.1            # left margin for content
ly = BOX_Y + BOX_H - 0.20   # top content Y (just inside box top)

ax1.add_patch(plt.Rectangle((BOX_X, BOX_Y), BOX_W, BOX_H,
                             fc="white", ec=C_FRAME, lw=1, zorder=6))
ax1.text(BOX_X + BOX_W / 2, ly + 0.08, "LEGEND", ha="center", fontsize=8,
         fontweight="bold", color=C_TITLE, zorder=7)
legend_items = [
    (C_BLUE,  "-",  "Blue  — Clean water supply (1\" HDPE)"),
    (C_BROWN, "-",  "Brown — Used/recyclable water (1\" HDPE)"),
    (C_BLACK, "-",  "Black — Waste water (1\" HDPE)"),
    (C_BLUE,  "--", "Dashed — Return / fill lines"),
]
for i, (col, ls, lbl) in enumerate(legend_items):
    yy = ly - 0.12 - i * 0.24
    ax1.plot([lx, lx + 0.5], [yy, yy], color=col, lw=2.2, ls=ls, zorder=7)
    ax1.text(lx + 0.62, yy, lbl, va="center", fontsize=6.5, color=C_TEXT, zorder=7)

# ── Symbols box — same styling as legend, aligned with Brown System zone ──────
# Brown System zone: X=5.1, width=4.5 → bottom also at Y=1.3
SYM_X = 5.1   # Brown System left edge
ax1.add_patch(plt.Rectangle((SYM_X, BOX_Y), BOX_W, BOX_H,
                             fc="white", ec=C_FRAME, lw=1, zorder=6))
ax1.text(SYM_X + BOX_W / 2, ly + 0.08, "SYMBOLS", ha="center", fontsize=8,
         fontweight="bold", color=C_TITLE, zorder=7)
syms = [
    ("P-xx",      "Pump (12V DC diaphragm)"),
    ("BV-xx",     "Ball valve (manual)"),
    ("3W-DV",     "3-way diverter valve"),
    ("F1/F2/F3",  "Filter cartridge"),
    ("⬡",         "External bulkhead port (2\" NPT)"),
]
for i, (sym, desc) in enumerate(syms):
    ax1.text(SYM_X + 0.15, ly - 0.10 - i * 0.25,
             f"{sym} — {desc}", va="center", fontsize=6.2, color=C_TEXT, zorder=7)

plt.tight_layout(pad=0.3)
os.makedirs(SVG_DIR, exist_ok=True)

fig1.savefig("diagrams/water-system-sheet1.png", dpi=150, bbox_inches="tight",
             facecolor=fig1.get_facecolor())
fig1.savefig(svg_path("diagrams/water-system-sheet1.png"), bbox_inches="tight", facecolor=fig1.get_facecolor())
plt.close(fig1)
print("Sheet 1 written → diagrams/water-system-sheet1.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — TANK & FILTER SKID LAYOUT (PLAN VIEW — inside container)
# ═══════════════════════════════════════════════════════════════════════════════

fig2, ax2 = plt.subplots(1, 1, figsize=(18, 12))
fig2.patch.set_facecolor("#F5F5F0")
ax2.set_facecolor("#F5F5F0")
ax2.axis("off")

# ── Title block ───────────────────────────────────────────────────────────────
title_block(ax2, "SHEET 2 OF 3",
            drawing_title="WATER SYSTEM EQUIPMENT LAYOUT",
            subtitle="Plan view (inside container)",
            scale_note="1:25 (approx)",
            doc_id="TBS-001 · Water System")

# ── Plan view ─────────────────────────────────────────────────────────────────
ax2.set_xlim(-0.5, 12.5)
ax2.set_ylim(-0.8, 6.8)
ax2.set_aspect("equal")

# Container outline (20ft = 6096 mm; 8ft = 2438 mm → scaled ×1/25)
# At 1:25: 6096/25 = 243.8 → use 12 units; 2438/25 = 97.5 → use 5 units
CW = 12.0   # container width in drawing units
CH = 5.0    # container depth in drawing units
ax2.add_patch(plt.Rectangle((0, 0), CW, CH, fc="white", ec=C_FRAME, lw=3,
                             zorder=1))
ax2.text(6.0, -0.25, "CONTAINER INTERIOR — PLAN VIEW  (6,096 × 2,438 mm interior)",
         ha="center", fontsize=8, color=C_FRAME)

# Wall thickness (container wall ~75mm → 0.075 at 1:25, round to 0.1)
WT = 0.1
ax2.add_patch(plt.Rectangle((-WT, -WT), CW + 2*WT, CH + 2*WT,
                             fc="none", ec="#777", lw=1.2, ls="--", zorder=0))

# ── Equipment placement ───────────────────────────────────────────────────────
# IBCs in RIGHT END ZONE (X=4,649–5,893mm); drums in LEFT END ZONE (X=0–1,100mm).
# Scale: CW=12 units = 5893mm interior → 1mm = 12/5893 units
#        CH=5  units = 2362mm interior → 1mm = 5/2362 units
SX = 12.0 / 5893.0   # mm to drawing unit (X direction)
SY = 5.0  / 2362.0   # mm to drawing unit (Y direction)

# IBC footprint in drawing units:
IBC_W = 1219 * SX    # ≈ 2.48 drawing units
IBC_D = 1016 * SY    # ≈ 2.15 drawing units

# IBC column X in drawing: IBC_COL_X = 4674mm (right-justified to end wall)
IBC_COL_DX = IBC_COL_X * SX  # ≈ 9.52

def ibc_plan(ax, x, y, fc, ec, label, sublabel=""):
    ax.add_patch(plt.Rectangle((x, y), IBC_W, IBC_D, fc=fc, ec=ec, lw=1.8, zorder=2))
    # cage lines
    for xi in [x + IBC_W/3, x + 2*IBC_W/3]:
        ax.plot([xi, xi], [y, y + IBC_D], color=ec, lw=0.6, alpha=0.5)
    for yi in [y + IBC_D/3, y + 2*IBC_D/3]:
        ax.plot([x, x + IBC_W], [yi, yi], color=ec, lw=0.6, alpha=0.5)
    ax.text(x + IBC_W/2, y + IBC_D/2 + 0.1, label, ha="center", va="center",
            fontsize=7.5, fontweight="bold", color="#111", zorder=3)
    ax.text(x + IBC_W/2, y + IBC_D/2 - 0.2, sublabel, ha="center", va="center",
            fontsize=6.5, color="#555", zorder=3)

# Right end zone: 4 IBCs in 2×2 stack (plan view shows top-down footprint)
# Near column (Yd=30–1046mm): Blue #1 on top, Brown on bottom
NEAR_IBC_DY = BLUE_IBC_Y * SY
ibc_plan(ax2, IBC_COL_DX, NEAR_IBC_DY, "#BBDEFB", C_BLUE_IBC,
         "IBC-1 BLUE / IBC-3 BROWN", "Top: 600L clean\nBottom: 600L recycle")
# Far column (Yd=1316–2332mm): Blue #2 on top, Waste on bottom — 270mm plumbing corridor between columns
FAR_IBC_DY = IBC_FAR_Y * SY
ibc_plan(ax2, IBC_COL_DX, FAR_IBC_DY, "#D5D5D0", C_WASTE_IBC,
         "IBC-2 BLUE / IBC-4 WASTE", "Top: 600L clean\nBottom: 600L waste")

# Drain pumps P-03 (waste) and P-05 (brown) — in plumbing corridor between IBC columns
CORR_DY = 1181 * SY  # corridor centerline in drawing coords
pump(ax2, IBC_COL_DX + IBC_W * 0.35, CORR_DY + 0.25, color=C_PUMP, r=0.15)
ax2.text(IBC_COL_DX + IBC_W * 0.35, CORR_DY + 0.55, "P-05\nBROWN\nDRAIN",
         ha="center", fontsize=5, color=C_PUMP)
pump(ax2, IBC_COL_DX + IBC_W * 0.65, CORR_DY - 0.25, color=C_PUMP, r=0.15)
ax2.text(IBC_COL_DX + IBC_W * 0.65, CORR_DY - 0.55, "P-03\nWASTE\nDRAIN",
         ha="center", fontsize=5, color=C_PUMP)

# Equipment panel in IBC plumbing corridor (between IBC columns)
EP_X_DU = PUMP_X * SX             # ≈ 9.77
EP_W_DU = PUMP_W * SX             # ≈ 1.59
EP_Y_DU = 1046 * SY               # ≈ 2.21 (corridor near face)
EP_D_DU = 270 * SY                # ≈ 0.57 (corridor width)
ax2.add_patch(plt.Rectangle((EP_X_DU, EP_Y_DU), EP_W_DU, EP_D_DU,
              fc=C_FILT, ec="#F57F17", lw=2, zorder=2))
ax2.text(EP_X_DU + EP_W_DU/2, EP_Y_DU + EP_D_DU/2 + 0.08,
         "EQUIPMENT PANEL", ha="center", fontsize=6.5,
         fontweight="bold", color="#E65100", zorder=3)
ax2.text(EP_X_DU + EP_W_DU/2, EP_Y_DU + EP_D_DU/2 - 0.12,
         "P-01, P-02, P-04, ACC-01\nF1 → F2 → F3 (3-STAGE FILTER)",
         ha="center", fontsize=5, color="#E65100", zorder=3)

# Processing tray (304 SS, two panels, 50mm rim)
TRAY_X0 = (FP_X_L + 20) * SX   # left edge in drawing units
TRAY_X1 = (FP_X_R - 20) * SX   # right edge in drawing units

# Spray bar along top wall — aligned with processing tray
pipe(ax2, TRAY_X0, 4.75, TRAY_X1, 4.75, C_BLUE, lw=3)
ax2.text((TRAY_X0 + TRAY_X1) / 2, 4.88,
         "FLOOD/SPRAY BAR (3/4\" HDPE, 1\" NPT inlets every 600mm)",
         ha="center", fontsize=7, color=C_BLUE)
TRAY_Y0 = PROC_TRAY_YD_NEAR * SY  # starts at near edge
TRAY_DY = 2200 * SY            # depth in drawing units
ax2.add_patch(plt.Rectangle((TRAY_X0, TRAY_Y0), TRAY_X1 - TRAY_X0, TRAY_DY,
              fc=C_PROC, ec="#388E3C", lw=2, zorder=1, alpha=0.5))
# Panel split line (two panels, each 1,992mm wide)
tray_mid_x = (TRAY_X0 + TRAY_X1) / 2
ax2.plot([tray_mid_x, tray_mid_x], [TRAY_Y0, TRAY_Y0 + TRAY_DY],
         color="#388E3C", lw=1.2, ls="--", zorder=2)
ax2.text((TRAY_X0 + TRAY_X1) / 2, TRAY_Y0 + TRAY_DY - 0.15,
         "PROCESSING TRAY (304 SS, 50mm RIM, 2 PANELS)",
         ha="center", fontsize=7, color="#2E7D32")
ax2.text(tray_mid_x - 0.8, TRAY_Y0 + TRAY_DY / 2,
         "PANEL A\n1,992 × 2,200mm", ha="center", fontsize=6, color="#388E3C")
ax2.text(tray_mid_x + 0.8, TRAY_Y0 + TRAY_DY / 2,
         "PANEL B\n1,992 × 2,200mm", ha="center", fontsize=6, color="#388E3C")

# Tray sump at IBC corner (P-04 suction pickup to 3W-DV-02)
drain_x = PROC_TRAY_DRAIN_X * SX
drain_y = PROC_TRAY_DRAIN_YD * SY
fd = plt.Circle((drain_x, drain_y), 0.18, fc="white", ec="#388E3C", lw=1.8, zorder=4)
ax2.add_patch(fd)
ax2.plot([drain_x - 0.18, drain_x + 0.18], [drain_y, drain_y],
         color="#388E3C", lw=1.2, zorder=5)
ax2.plot([drain_x, drain_x], [drain_y - 0.18, drain_y + 0.18],
         color="#388E3C", lw=1.2, zorder=5)
ax2.text(drain_x + 0.45, drain_y - 0.1, "SUMP WELL\nP-04 PICKUP", ha="center",
         fontsize=6, color="#388E3C")

# Left end zone shading (X=0–625mm — light trap only, drums removed rev 5)
ZONE_L_DX = ZONE_L_END * SX   # = 625mm → ≈ 1.27
ax2.add_patch(plt.Rectangle((0, 0), ZONE_L_DX, CH,
              fc="#FFF3E0", ec="none", alpha=0.45, zorder=0))
ax2.plot([ZONE_L_DX, ZONE_L_DX], [0, CH], color="#805000", lw=1.5, ls="--",
         zorder=6)
ax2.text(ZONE_L_DX - 0.05, CH + 1,
         f"LEFT END ZONE\nX=0–{ZONE_L_END:,}mm\n(light trap only)",
         ha="right", va="top", fontsize=6.5, color="#805000", fontweight="bold")

# Right end zone shading (X=4649–5893mm in drawing)
ZONE_R_DX = ZONE_R_START * SX   # ≈ 9.45
ax2.add_patch(plt.Rectangle((ZONE_R_DX, 0), CW - ZONE_R_DX, CH,
              fc="#E8F0FF", ec="none", alpha=0.45, zorder=0))
ax2.plot([ZONE_R_DX, ZONE_R_DX], [0, CH], color="#004080", lw=1.5, ls="--",
         zorder=6)
ax2.text(ZONE_R_DX + 1, CH + 1,
         f"RIGHT END ZONE\nX={ZONE_R_START:,}–5,893mm\n(4× IBC 2×2 stack)",
         ha="left", va="top", fontsize=6.5, color="#004080", fontweight="bold")

# Chemistry prep tap — on near wall at shelf position
TAP_DX = 3729 * SX   # TAP_X in drawing units
ax2.plot(TAP_DX, 0.05, "v", color=C_BLUE, ms=10, zorder=8)
ax2.plot([TAP_DX, TAP_DX], [0.05, 0.25], color=C_BLUE, lw=2.0, zorder=7)
ax2.text(TAP_DX, 0.40, "TAP-01\n(CHEM PREP)", ha="center", fontsize=5.5,
         color=C_BLUE, zorder=8)

# Pinhole wall — BOTTOM of plan view (Yd=0 = near side, pinhole aperture wall)
ax2.add_patch(plt.Rectangle((0.0, -0.15), CW, 0.15, fc="#BDBDBD", ec=C_FRAME,
                             lw=2, zorder=5))
ax2.text(CW / 2, -0.08, "PINHOLE WALL (FRONT — Yd = 0)",
         ha="center", va="center", fontsize=6, color="#333", zorder=6)

# Dimensions — using shared helpers from tbs_drawing.
draw_dim_h(ax2, 0, CW, -0.30, "5,893 mm (CONTAINER INTERIOR)", offset=0.21, fs=6.5, above=False)
draw_dim_v(ax2, -0.2 - 0.1, 0, CH, "2,362 mm", offset=0.27, fs=6.5, right=False)
draw_dim_h(ax2, IBC_COL_DX, IBC_COL_DX + IBC_W, 5.2 - 0.25, "IBC col: 1,219 mm", offset=0.27, fs=6.5, above=False)
draw_dim_h(ax2, 0, ZONE_L_DX, 5.5, f"LEFT END ZONE: {ZONE_L_END} mm", offset=0.27, fs=6.5, color="#805000", above=False)
draw_dim_h(ax2, ZONE_R_DX, CW, 5.5, f"RIGHT END ZONE: {C_LEN - ZONE_R_START} mm", offset=0.27, fs=6.5, color="#004080", above=False)

# Orientation arrow — points toward pinhole wall (bottom, Yd=0)
ax2.annotate("", xy=(CW + 0.3, 0.4), xytext=(CW + 0.3, 1.6),
             arrowprops=dict(arrowstyle="-|>", color=C_FRAME, lw=1.5,
                             mutation_scale=12))
ax2.text(CW + 0.3, 1.8, "FRONT\n(PINHOLE\nWALL)", ha="center", fontsize=6,
         color=C_FRAME)

plt.tight_layout(pad=0.5)

fig2.savefig("diagrams/water-system-sheet2.png", dpi=150, bbox_inches="tight",
             facecolor=fig2.get_facecolor())
fig2.savefig(svg_path("diagrams/water-system-sheet2.png"), bbox_inches="tight", facecolor=fig2.get_facecolor())
plt.close(fig2)
print("Sheet 2 written → diagrams/water-system-sheet2.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — PROCESSING TRAY DRAINAGE PLAN (water flow direction)
# ═══════════════════════════════════════════════════════════════════════════════

fig3, ax3 = plt.subplots(1, 1, figsize=(18, 12))
fig3.patch.set_facecolor("#F5F5F0")
ax3.set_facecolor("#F5F5F0")
ax3.axis("off")

# ── Title block ───────────────────────────────────────────────────────────────
title_block(ax3, "SHEET 3 OF 3",
            drawing_title="PROCESSING TRAY DRAINAGE PLAN",
            subtitle="Plan view (water flow direction)",
            scale_note="~1:20",
            doc_id="TBS-001 · Water System")

# ── Scale: map mm to drawing units ──────────────────────────────────────────
# Tray is 4,459 × 2,200mm.  Fit into a ~14 × 7 drawing region.
TRAY_DRAW_W = 13.0
TRAY_DRAW_H = TRAY_DRAW_W * PROC_TRAY_D / PROC_TRAY_W  # maintain aspect

# Origin offset (drawing units) — tray lower-left corner
OX = 1.5
OY = 1.8

def s3x(mm):
    """Convert tray-local X (mm from tray left edge) to drawing units."""
    return OX + mm * TRAY_DRAW_W / PROC_TRAY_W

def s3y(mm):
    """Convert tray-local Yd (mm from tray near edge) to drawing units."""
    return OY + mm * TRAY_DRAW_H / PROC_TRAY_D

ax3.set_xlim(-0.3, OX + TRAY_DRAW_W + 2.5)
ax3.set_ylim(-3.5, OY + TRAY_DRAW_H + 1.8)
ax3.set_aspect("equal")

# ── Tray outline ─────────────────────────────────────────────────────────────
ax3.add_patch(plt.Rectangle((OX, OY), TRAY_DRAW_W, TRAY_DRAW_H,
              fc="#E8F5E9", ec="#388E3C", lw=2.5, zorder=1))

# Rim shading (inner border)
RIM_DU = PROC_TRAY_RIM * TRAY_DRAW_W / PROC_TRAY_W  # rim in drawing units
ax3.add_patch(plt.Rectangle((OX + RIM_DU, OY + RIM_DU),
              TRAY_DRAW_W - 2*RIM_DU, TRAY_DRAW_H - 2*RIM_DU,
              fc="#C8E6C9", ec="none", zorder=1, alpha=0.5))

# Label corners with elevation annotations (high/low)
# Low point: IBC corner (near rim, right side) — drain at X=4550, Yd=80
# High point: far-left corner (opposite diagonal)
drain_local_x_s3 = PROC_TRAY_DRAIN_X - PROC_TRAY_X_L
ax3.text(s3x(drain_local_x_s3), OY - 0.55, "LOW CORNER\n(DRAIN — IBC SIDE)",
         ha="center", fontsize=7.5, fontweight="bold", color="#D32F2F")
ax3.text(OX - 0.15, OY + TRAY_DRAW_H + 0.35,
         "HIGH CORNER\n(FAR-LEFT)",
         ha="left", fontsize=7.5, fontweight="bold", color="#1565C0")

ax3.text(OX - 0.15, OY + TRAY_DRAW_H / 2, "HIGH\nEDGE",
         ha="right", va="center", fontsize=6.5, color="#1565C0", fontweight="bold")
ax3.text(OX + TRAY_DRAW_W + 0.15, OY - 0.3, "LOW\nEDGE",
         ha="left", va="center", fontsize=6.5, color="#D32F2F", fontweight="bold")

# ── Slope arrows (flow direction) ───────────────────────────────────────────
# Water flows toward drain at IBC corner (right side, near edge)
# Draw a grid of arrows showing combined flow direction

ARROW_COLOR = "#1976D2"
ARROW_ALPHA = 0.7

# Drain position in tray-local coordinates (used by arrows and drain symbol)
drain_local_x = PROC_TRAY_DRAIN_X - PROC_TRAY_X_L
drain_local_yd = PROC_TRAY_DRAIN_YD - PROC_TRAY_YD_NEAR

# Grid of flow arrows across the tray interior
n_cols = 9
n_rows = 5
for i in range(n_cols):
    for j in range(n_rows):
        # Position in tray-local mm
        ax_mm = PROC_TRAY_W * (i + 0.5) / n_cols
        ay_mm = PROC_TRAY_D * (j + 0.5) / n_rows

        # Flow direction: toward drain at IBC corner
        dx_mm = (drain_local_x - ax_mm)
        dy_mm = (drain_local_yd - ay_mm)

        # Normalize and scale to fixed arrow length
        mag = math.sqrt(dx_mm**2 + dy_mm**2)
        if mag < 1:
            continue
        arrow_len = 0.35  # drawing units
        dx_du = dx_mm / mag * arrow_len
        dy_du = dy_mm / mag * arrow_len

        ax_du = s3x(ax_mm)
        ay_du = s3y(ay_mm)

        ax3.annotate("", xy=(ax_du + dx_du, ay_du + dy_du),
                     xytext=(ax_du - dx_du * 0.3, ay_du - dy_du * 0.3),
                     arrowprops=dict(arrowstyle="-|>", color=ARROW_COLOR,
                                     lw=1.5, mutation_scale=10, alpha=ARROW_ALPHA),
                     zorder=4)

# ── Drain symbol (circle + crosshair) ───────────────────────────────────────
drain_dx = s3x(drain_local_x)
drain_dy = s3y(drain_local_yd)
DRAIN_R = 0.3

drain_circle = plt.Circle((drain_dx, drain_dy), DRAIN_R,
                           fc="white", ec="#D32F2F", lw=2.5, zorder=6)
ax3.add_patch(drain_circle)
ax3.plot([drain_dx - DRAIN_R*0.7, drain_dx + DRAIN_R*0.7],
         [drain_dy, drain_dy], color="#D32F2F", lw=1.8, zorder=7)
ax3.plot([drain_dx, drain_dx],
         [drain_dy - DRAIN_R*0.7, drain_dy + DRAIN_R*0.7],
         color="#D32F2F", lw=1.8, zorder=7)

# Drain label
ax3.text(drain_dx + 1.55, drain_dy + 0.2, "SUMP WELL (P-04 PICKUP)",
         ha="center", va="top", fontsize=7.5, fontweight="bold",
         color="#D32F2F", zorder=8)
ax3.text(drain_dx - 0.9, drain_dy + 0.1,
         f"X={PROC_TRAY_DRAIN_X:,}  Yd={PROC_TRAY_DRAIN_YD}\n{PROC_TRAY_SUMP_W}x{PROC_TRAY_SUMP_D}x{PROC_TRAY_SUMP_Z}mm",
         ha="center", va="bottom", fontsize=6.5, color="#D32F2F", zorder=8)

# ── Slope annotations ────────────────────────────────────────────────────────
# Slope: 1:200 in both X and Yd toward drain corner (IBC side)
x_fall = PROC_TRAY_W / 200  # full-width fall (left to right)
yd_fall = PROC_TRAY_D / 200  # full-depth fall (far to near)

# X-slope annotation (center of tray)
ann_x = s3x(PROC_TRAY_W * 0.5)
ann_y = s3y(PROC_TRAY_D * 0.5)
ax3.text(ann_x, ann_y,
         f"X-SLOPE: 1:200 → IBC CORNER\n({x_fall:.1f}mm fall over {PROC_TRAY_W:,.0f}mm)",
         ha="center", va="center", fontsize=7, color="#0D47A1",
         bbox=dict(fc="white", ec="#0D47A1", lw=0.8, pad=3, alpha=0.9),
         zorder=8)

# Yd-axis slope annotation (upper area)
ann_y2 = s3y(PROC_TRAY_D * 0.78)
ax3.text(s3x(PROC_TRAY_W * 0.5), ann_y2,
         f"Yd-SLOPE: 1:200\n({yd_fall:.1f}mm fall over {PROC_TRAY_D:,}mm)",
         ha="center", va="center", fontsize=7, color="#0D47A1",
         bbox=dict(fc="white", ec="#0D47A1", lw=0.8, pad=3, alpha=0.9),
         zorder=8)

# ── Dimensions ───────────────────────────────────────────────────────────────
# Tray width (X direction)
draw_dim_h(ax3, OX, OX + TRAY_DRAW_W, OY + TRAY_DRAW_H + 0.9,
           f"{PROC_TRAY_W:,}mm (X={PROC_TRAY_X_L}–{PROC_TRAY_X_R})", offset=0.27, fs=6.5, above=False)


# ax3.annotate("", xy=(OX + TRAY_DRAW_W, OY + TRAY_DRAW_H + 0.6),
#              xytext=(OX, OY + TRAY_DRAW_H + 0.6),
#              arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=1.2,
#                              mutation_scale=10))
# ax3.text(OX + TRAY_DRAW_W/2, OY + TRAY_DRAW_H + 0.75,
#          f"{PROC_TRAY_W:,}mm (X={PROC_TRAY_X_L}–{PROC_TRAY_X_R})",
#          ha="center", fontsize=7, color=C_DIM)

# Tray depth (Yd direction)
draw_dim_v(ax3, OX - 0.9, OY + TRAY_DRAW_H, OY,
           f"{PROC_TRAY_D:,}mm (Yd={PROC_TRAY_YD_NEAR}–{PROC_TRAY_YD_FAR})", offset=0.27, fs=6.5, right=False)

# Drain X position dimension
draw_dim_h(ax3, drain_dx, OX, OY - 0.5,
           f"{drain_local_x:,}mm from left edge", offset=0.17, fs=6.5, above=False)

# ── Walkway positions (dashed outlines) ──────────────────────────────────────
WK_COLOR = "#8D6E63"
WK_ALPHA_L = 0.4

# Near walkway (overlaps tray near edge)
near_wk_y0 = s3y(-PROC_TRAY_YD_NEAR + WALKWAY_NEAR_YD)  # Yd=0 in container coords
near_wk_y1 = s3y(-PROC_TRAY_YD_NEAR + WALKWAY_NEAR_YD + WALKWAY_W)
ax3.add_patch(plt.Rectangle((OX, near_wk_y0),
              TRAY_DRAW_W, near_wk_y1 - near_wk_y0,
              fc=WK_COLOR, ec=WK_COLOR, lw=1.2, ls="--",
              alpha=WK_ALPHA_L, hatch="//", zorder=2))
ax3.text(OX + TRAY_DRAW_W + 0.15, (near_wk_y0 + near_wk_y1)/2,
         "NEAR\nWALKWAY\n(300mm)",
         ha="left", va="center", fontsize=6, color=WK_COLOR)

# Far walkway
far_wk_yd_local = WALKWAY_FAR_YD - PROC_TRAY_YD_NEAR
far_wk_y0 = s3y(far_wk_yd_local)
far_wk_y1 = s3y(far_wk_yd_local + WALKWAY_W)
ax3.add_patch(plt.Rectangle((OX, far_wk_y0),
              TRAY_DRAW_W, far_wk_y1 - far_wk_y0,
              fc=WK_COLOR, ec=WK_COLOR, lw=1.2, ls="--",
              alpha=WK_ALPHA_L, hatch="//", zorder=2))
ax3.text(OX + TRAY_DRAW_W + 0.15, (far_wk_y0 + far_wk_y1)/2,
         "FAR\nWALKWAY\n(300mm)",
         ha="left", va="center", fontsize=6, color=WK_COLOR)

# ── Pipe run from drain ──────────────────────────────────────────────────────
# 1" HDPE runs along near wall (Yd≈60) to diverter valve 3W-DV-02
pipe_y = drain_dy - 0.8
ax3.plot([drain_dx, drain_dx], [drain_dy - DRAIN_R, pipe_y], color=C_BROWN,
         lw=2.5, solid_capstyle="round", zorder=5)
ax3.annotate("", xy=(OX - 0.2, pipe_y), xytext=(drain_dx, pipe_y),
             arrowprops=dict(arrowstyle="-|>", color=C_BROWN, lw=2.5,
                             mutation_scale=12), zorder=5)
ax3.text(drain_dx - 1.5, pipe_y - 0.2,
         "P-04 SUCTION HOSE (OVER RIM TO PUMP MANIFOLD)",
         ha="center", fontsize=6.5, color=C_BROWN, style="italic", zorder=8)

# ── Notes ────────────────────────────────────────────────────────────────────
notes = [
    "NOTES:",
    f"1. Dual-axis pitch 1:200 — water converges on sump at X={PROC_TRAY_DRAIN_X:,}, Yd={PROC_TRAY_DRAIN_YD}.",
    f"2. Maximum fall: {PROC_TRAY_PITCH}mm (Yd axis) + {x_fall:.1f}mm (X axis from far corner to sump).",
    f"3. Sump well ({PROC_TRAY_SUMP_W}x{PROC_TRAY_SUMP_D}x{PROC_TRAY_SUMP_Z}mm) pressed into tray floor — P-04 suction pickup lifts to IBC-3.",
    f"4. Tray: 304 SS, {PROC_TRAY_RIM}mm rim, on tapered HDPE shim strips. No tray floor penetration.",
    f"5. Wall-cantilevered walkway — no legs or structure on tray floor near sump.",
]
draw_notes(ax3, notes, 0.3, -0.8, spacing=0.2, fs=7, width=14,
           color=C_TEXT, title_color=C_TEXT, font={"fontfamily": "monospace"})

fig3.savefig("diagrams/water-system-sheet3.png", dpi=150, bbox_inches="tight",
             facecolor=fig3.get_facecolor())
fig3.savefig(svg_path("diagrams/water-system-sheet3.png"), bbox_inches="tight",
             facecolor=fig3.get_facecolor())
plt.close(fig3)
print("Sheet 3 written → diagrams/water-system-sheet3.png")

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 4 — PROCESSING TRAY DRAIN CROSS-SECTION ELEVATION
# Two panels:
#   LEFT  — Zoomed detail of sump well + pickup tube + shim strips (~1:2)
#   RIGHT — Full cross-section showing suction line from sump to P-04
#           pump to 3W-DV-02 diverter to IBC-3 (~1:15)
# Horizontal = Yd, Vertical = Z (height above floor).
# ═══════════════════════════════════════════════════════════════════════════════

from matplotlib.gridspec import GridSpec
fig4 = plt.figure(figsize=(20, 12))
fig4.patch.set_facecolor("#F5F5F0")
gs4 = GridSpec(2, 2, figure=fig4, width_ratios=[1, 1.2], height_ratios=[1.4, 1],
               hspace=0.08, wspace=0.05)
ax4a = fig4.add_subplot(gs4[0, 0])   # Detail A — top left
ax4c = fig4.add_subplot(gs4[1, 0])   # Plan view — bottom left
ax4b = fig4.add_subplot(gs4[:, 1])   # Section A-A — full right column
for axx in (ax4a, ax4b, ax4c):
    axx.set_facecolor("#F5F5F0")
    axx.axis("off")
    axx.set_aspect("equal")

# ── Title block (full-width axes spanning both columns) ───────────────────
ax4_tb = fig4.add_axes([0.04, 0.0, 0.92, 0.06])
ax4_tb.set_xlim(0, 1)
ax4_tb.set_ylim(0, 1)
ax4_tb.axis("off")
title_block(ax4_tb, "SHEET 4 OF 4",
            drawing_title="PROCESSING TRAY DRAIN — SUMP PICKUP CROSS-SECTION",
            subtitle=f"Section A-A at X={PROC_TRAY_DRAIN_X:,}mm (through sump) + plan view of rim hose routing",
            scale_note="DETAIL ~1:2  |  PLAN ~1:8  |  ELEVATION ~1:12",
            doc_id="TBS-001 · Water System",
            height=0.75)

from matplotlib.patches import Arc as MplArc


def draw_pipe_path(ax, y_pts, z_pts, od_mm, wall_mm, sy, sz,
                   fc="#B0B0B8", ec="#333333", bore_fc="white",
                   elbow_r=None, zorder=5):
    """Draw a pipe run with parallel-sided straight sections and elbow fittings.

    Pipes have constant OD with parallel walls.  Direction changes are drawn
    as discrete elbow fittings (concentric arcs), never as gradual curves.
    Supports 90 deg, 45 deg, and arbitrary-angle elbows.

    y_pts, z_pts : waypoint coordinates in mm (before scaling)
    od_mm        : pipe outer diameter in mm
    wall_mm      : pipe wall thickness in mm
    sy, sz       : scale functions  mm -> data coordinates
    elbow_r      : elbow centerline bend radius in mm (default 1.0 x od_mm)
    """
    n = len(y_pts)
    if n < 2:
        return
    half_od = od_mm / 2.0
    half_id = half_od - wall_mm
    if elbow_r is None:
        elbow_r = od_mm          # standard short-radius barb elbow

    # ── segment directions ──────────────────────────────────────────────
    segs = []
    for i in range(n - 1):
        dy = y_pts[i + 1] - y_pts[i]
        dz = z_pts[i + 1] - z_pts[i]
        length = max(math.hypot(dy, dz), 1e-6)
        segs.append((dy / length, dz / length, length))

    # ── elbow geometry at each intermediate waypoint ────────────────────
    elbows = []                  # one entry per interior waypoint
    for i in range(1, n - 1):
        d1y, d1z, _ = segs[i - 1]
        d2y, d2z, _ = segs[i]

        cos_a = max(-1.0, min(1.0, d1y * d2y + d1z * d2z))
        alpha = math.acos(cos_a)          # angle between direction vectors
        turn  = math.pi - alpha           # actual bend angle

        if turn < 0.01:                   # nearly straight — skip
            elbows.append(None)
            continue

        # clamp tangent so it never eats more than 40 % of either segment
        tangent = elbow_r * math.tan(turn / 2)
        max_t = 0.4 * min(segs[i - 1][2], segs[i][2])
        if tangent > max_t:
            tangent = max_t               # use a tighter bend radius

        cross = d1y * d2z - d1z * d2y     # +ve = left turn

        # normal toward arc center
        if cross > 0:
            ny, nz = -d1z, d1y
        else:
            ny, nz = d1z, -d1y

        # arc center from the incoming tangent point
        tp_y = y_pts[i] - d1y * tangent
        tp_z = z_pts[i] - d1z * tangent
        # radius may have been clamped — recompute from tangent
        r_eff = tangent / math.tan(turn / 2) if turn > 0.01 else elbow_r
        cy = tp_y + ny * r_eff
        cz = tp_z + nz * r_eff

        start_a = math.atan2(tp_z - cz, tp_y - cy)
        sweep   = turn if cross > 0 else -turn

        elbows.append({
            'tangent': tangent,
            'r': r_eff,
            'center': (cy, cz),
            'start': start_a,
            'sweep': sweep,
        })

    # ── helper: filled annular‐ring rectangle (one straight section) ───
    def _rect(sy0, sz0, sy1, sz1, nx, nz, half_r, color, z_ord):
        pts = [(sy(sy0 + nx * half_r), sz(sz0 + nz * half_r)),
               (sy(sy1 + nx * half_r), sz(sz1 + nz * half_r)),
               (sy(sy1 - nx * half_r), sz(sz1 - nz * half_r)),
               (sy(sy0 - nx * half_r), sz(sz0 - nz * half_r))]
        ax.fill([p[0] for p in pts], [p[1] for p in pts],
                fc=color, ec=ec if color != bore_fc else "none",
                lw=0.8 if color != bore_fc else 0,
                zorder=z_ord)

    # ── draw straight sections (trimmed by tangent lengths) ─────────────
    for i in range(len(segs)):
        dy, dz, seg_len = segs[i]
        nx, nz = -dz, dy          # perpendicular

        trim_s = elbows[i - 1]['tangent'] if (i > 0 and elbows[i - 1]) else 0
        trim_e = elbows[i]['tangent']     if (i < len(elbows) and elbows[i]) else 0

        p0y = y_pts[i]     + dy * trim_s
        p0z = z_pts[i]     + dz * trim_s
        p1y = y_pts[i + 1] - dy * trim_e
        p1z = z_pts[i + 1] - dz * trim_e

        remaining = seg_len - trim_s - trim_e
        if remaining < 0.5:
            continue              # segment fully consumed by elbows

        _rect(p0y, p0z, p1y, p1z, nx, nz, half_od, fc, zorder)
        _rect(p0y, p0z, p1y, p1z, nx, nz, half_id, bore_fc, zorder + 1)

    # ── draw elbow fittings (concentric arcs) ───────────────────────────
    for elb in elbows:
        if elb is None:
            continue
        cy, cz = elb['center']
        r_eff  = elb['r']
        sa     = elb['start']
        sw     = elb['sweep']
        n_arc  = max(20, int(abs(sw) / 0.04))
        angles = [sa + sw * t / n_arc for t in range(n_arc + 1)]

        def _arc_ring(r_out, r_in, color, z_ord):
            oy = [sy(cy + r_out * math.cos(a)) for a in angles]
            oz = [sz(cz + r_out * math.sin(a)) for a in angles]
            iy = [sy(cy + r_in  * math.cos(a)) for a in angles]
            iz = [sz(cz + r_in  * math.sin(a)) for a in angles]
            ax.fill(oy + iy[::-1], oz + iz[::-1],
                    fc=color,
                    ec=ec if color != bore_fc else "none",
                    lw=0.8 if color != bore_fc else 0,
                    zorder=z_ord)

        _arc_ring(r_eff + half_od, max(r_eff - half_od, 0.5), fc,      zorder)
        _arc_ring(r_eff + half_id, max(r_eff - half_id, 0.5), bore_fc, zorder + 1)


def draw_pipe_end(ax, cy, cz, r_data, wall_data, fc="#B0B0B8", ec="#333333",
                  bore_fc="white", zorder=5):
    """Draw pipe end-on at data coords (cy, cz) with radius r_data."""
    ax.add_patch(plt.Circle((cy, cz), r_data, fc=fc, ec=ec, lw=1.0, zorder=zorder))
    ax.add_patch(plt.Circle((cy, cz), r_data - wall_data,
                 fc=bore_fc, ec="none", zorder=zorder + 1))


# ═════════════════════════════════════════════════════════════════════════════
# PANEL A — SUMP WELL & PICKUP DETAIL (~1:2)
# Focused view: Yd = -20 to 420mm, Z = -50 to 200mm
# Shows: shim strips under tray, tray floor with slope, sump well,
#         pickup tube with foot valve, suction hose over rim, walkway.
# ═════════════════════════════════════════════════════════════════════════════
SC_A = 2.0   # mm per drawing unit
OA_X = 1.5   # drawing offset for Yd=0
OA_Y = 2.5   # drawing offset for Z=0

def sa_y(yd_mm):
    return OA_X + yd_mm / SC_A

def sa_z(z_mm):
    return OA_Y + z_mm / SC_A

ax4a.set_xlim(sa_y(-40) - 0.5, sa_y(420) + 1.0)
ax4a.set_ylim(sa_z(-55) - 0.5, sa_z(220) + 1.5)

# Panel A title
ax4a.text(sa_y(195), sa_z(195), "DETAIL A — SUMP WELL & PICKUP (APPROX 1:2)",
          ha="center", va="top", fontsize=10, fontweight="bold",
          color="#1A237E", zorder=10)

# ── Container floor (section fill) ──────────────────────────────────────────
FLOOR_T = 4.0   # simplified floor thickness in section
ax4a.add_patch(plt.Rectangle((sa_y(-20), sa_z(-FLOOR_T)),
              450 / SC_A, FLOOR_T / SC_A,
              fc="#B0B0B8", ec=C_FRAME, lw=1.8, zorder=2, hatch=".."))

# Near wall (Yd=0) — vertical
WALL_T = 2.0
ax4a.add_patch(plt.Rectangle((sa_y(-WALL_T), sa_z(-FLOOR_T)), WALL_T / SC_A,
              230 / SC_A,
              fc="#B0B0B8", ec=C_FRAME, lw=1.8, zorder=2, hatch=".."))

# ── HDPE shim strips under tray ─────────────────────────────────────────────
# CORRECT GEOMETRY: sump bottom sits ON container floor (Z=0).
# Tray floor is therefore RAISED by sump depth: Z = PROC_TRAY_SUMP_Z (20mm).
# Shim strips start at 20mm (near end) and taper to 20+PITCH=30mm (far end)
# to provide the 1:220 drainage slope toward the sump.
TRAY_T = 1.5  # 16-gauge SS
tray_yd_near = PROC_TRAY_YD_NEAR   # 80mm
tray_yd_far_view = 400  # visible range in detail

# Tray floor base height (raised by sump depth)
TRAY_BASE_Z = PROC_TRAY_SUMP_Z  # 20mm — tray floor at near end

# True slope per mm
slope_per_mm = PROC_TRAY_PITCH / PROC_TRAY_D  # 10/2200 = 0.00455

# Shim profile: height at any Yd = TRAY_BASE_Z + (Yd - tray_yd_near) * slope_per_mm
# At Yd=80 (near edge): shim height = 20mm (matches sump depth)
# At Yd=2280 (far edge): shim height = 30mm (20 + 10mm pitch)
# Exaggerate the SLOPE for visibility (base height shown proportionally)
SLOPE_EXAG_A = 5.0

# Draw representative shim strips as rectangles
shim_color = "#E8DCC0"  # HDPE tan
for shim_yd in [130, 250, 370]:
    if shim_yd > tray_yd_far_view:
        continue
    # Shim height = base (20mm) + slope component
    shim_h_base = TRAY_BASE_Z
    shim_h_slope = (shim_yd - tray_yd_near) * slope_per_mm * SLOPE_EXAG_A
    shim_h_here = shim_h_base + shim_h_slope
    shim_vis_w = 15  # visible width in cross-section (strip runs along X, we see its edge)
    ax4a.add_patch(plt.Rectangle((sa_y(shim_yd - shim_vis_w/2), sa_z(0)),
                  shim_vis_w / SC_A, shim_h_here / SC_A,
                  fc=shim_color, ec="#A09070", lw=0.8, zorder=3))

# ── Tray floor (sloped, sitting on shims) ────────────────────────────────────
# Tray bottom surface at near end = TRAY_BASE_Z (20mm), rises with slope
tray_z_at_near = TRAY_BASE_Z  # 20mm — sits at sump depth level
tray_z_at_far = TRAY_BASE_Z + (tray_yd_far_view - tray_yd_near) * slope_per_mm * SLOPE_EXAG_A

# Tray floor polygon
tray_pts_x = [sa_y(tray_yd_near), sa_y(tray_yd_far_view),
              sa_y(tray_yd_far_view), sa_y(tray_yd_near)]
tray_pts_y = [sa_z(tray_z_at_near), sa_z(tray_z_at_far),
              sa_z(tray_z_at_far + TRAY_T), sa_z(tray_z_at_near + TRAY_T)]
ax4a.fill(tray_pts_x, tray_pts_y, fc="#C8D8E8", ec=C_FRAME, lw=1.5, zorder=4)

# Near rim — extends from tray floor (Z=20mm) up by rim height (50mm)
rim_h = PROC_TRAY_RIM  # 50mm
RIM_TOP = TRAY_BASE_Z + rim_h  # 20 + 50 = 70mm above container floor
ax4a.add_patch(plt.Rectangle((sa_y(tray_yd_near - TRAY_T), sa_z(TRAY_BASE_Z)),
              TRAY_T / SC_A, rim_h / SC_A,
              fc="#C8D8E8", ec=C_FRAME, lw=1.5, zorder=4))

# ── Sump well ────────────────────────────────────────────────────────────────
# Pressed into tray floor at low point: 150mm (X) x 100mm (Yd) x 20mm deep
# CORRECT: sump bottom is AT container floor (Z=0), tray floor is at Z=20mm
# In this cross-section (cut along X), we see the Yd extent (100mm) and depth (20mm)
sump_yd_start = PROC_TRAY_DRAIN_YD  # 80mm (starts at near rim)
sump_yd_end = sump_yd_start + PROC_TRAY_SUMP_D  # 180mm
sump_z_floor = 0.0  # sump bottom sits ON container floor

# Sump well cavity — U-shaped depression from tray floor (Z=20) down to Z=0
sump_pts_x = [sa_y(sump_yd_start + 3), sa_y(sump_yd_end - 3),
              sa_y(sump_yd_end - 3), sa_y(sump_yd_end),
              sa_y(sump_yd_end), sa_y(sump_yd_start),
              sa_y(sump_yd_start), sa_y(sump_yd_start + 3)]
sump_pts_z = [sa_z(sump_z_floor + TRAY_T), sa_z(sump_z_floor + TRAY_T),
              sa_z(sump_z_floor), sa_z(sump_z_floor),
              sa_z(tray_z_at_near), sa_z(tray_z_at_near),
              sa_z(sump_z_floor), sa_z(sump_z_floor)]
ax4a.fill(sump_pts_x, sump_pts_z, fc="#C8D8E8", ec=C_FRAME, lw=1.5, zorder=4)

# Water pooled in sump (blue fill) — water collects from Z=0 up to near tray floor
ax4a.fill([sa_y(sump_yd_start + 4), sa_y(sump_yd_end - 4),
           sa_y(sump_yd_end - 4), sa_y(sump_yd_start + 4)],
          [sa_z(TRAY_BASE_Z - 4), sa_z(TRAY_BASE_Z - 4),
           sa_z(sump_z_floor + TRAY_T), sa_z(sump_z_floor + TRAY_T)],
          fc="#B3D9F2", ec="none", alpha=0.5, zorder=5)

# ── Walkway & hose pass-through constants ────────────────────────────────────
WK_DECK_H = 100
WK_GRATE_T = 25

# ── Pickup tube (dip tube with foot valve) ───────────────────────────────────
# 1" tube sits in the sump, extends up past the rim
TUBE_OD = 25.4  # 1" OD
tube_yd = sump_yd_start + PROC_TRAY_SUMP_D / 2  # center of sump in Yd = 130mm
tube_z_bot = sump_z_floor + 5  # 5mm above sump floor (Z=5mm)
tube_z_top = WK_DECK_H + WK_GRATE_T + 10  # 135mm — above walkway grate + clearance

# Foot valve / strainer at bottom
foot_valve_h = 15
foot_valve_w = 35

# Tube body — double-wall pipe section
TUBE_WALL = 3.0  # HDPE tube wall thickness (mm)
draw_pipe_path(ax4a,
               [tube_yd, tube_yd], [tube_z_bot + foot_valve_h, tube_z_top],
               TUBE_OD, TUBE_WALL, sa_y, sa_z,
               fc="#D0D0D0", ec=C_FRAME, zorder=6)
ax4a.add_patch(plt.Rectangle((sa_y(tube_yd - foot_valve_w/2), sa_z(tube_z_bot)),
              foot_valve_w / SC_A, foot_valve_h / SC_A,
              fc="#D0D0D0", ec=C_FRAME, lw=1.0, zorder=7))
# Strainer mesh marks
for sy_m in range(3):
    mesh_y = tube_yd - foot_valve_w/2 + 5 + sy_m * (foot_valve_w - 10) / 2
    ax4a.plot([sa_y(mesh_y), sa_y(mesh_y)],
             [sa_z(tube_z_bot), sa_z(tube_z_bot + foot_valve_h)],
             color="#999999", lw=0.4, zorder=8)

# ── Suction hose from tube top, along tray rim exterior ──────────────────────
HOSE_OD = 33.0   # 1" reinforced suction hose OD (mm)
HOSE_WALL = 4.0  # hose wall thickness (mm)
RIM_EXT_YD = tray_yd_near - HOSE_OD / 2 - 5  # ~60mm — hose CL on exterior of rim
HOSE_RIM_Z = TRAY_BASE_Z + rim_h / 2         # ~45mm — mid-rim height

# Hose path: short vertical overlap with tube top (creates 90° elbow) →
# horizontal above walkway → 90° elbow → down along rim exterior
ELBOW_OVERLAP = HOSE_OD  # vertical approach length for visible elbow fitting
hose_pts_y = [tube_yd, tube_yd, RIM_EXT_YD, RIM_EXT_YD]
hose_pts_z = [tube_z_top - ELBOW_OVERLAP, tube_z_top, tube_z_top, HOSE_RIM_Z]
draw_pipe_path(ax4a, hose_pts_y, hose_pts_z, HOSE_OD, HOSE_WALL,
               sa_y, sa_z, fc=C_BROWN, ec="#5A3020", zorder=8)

# Pipe end-on at rim exterior (hose turns to run along X — into the page)
pipe_r_a = HOSE_OD / 2 / SC_A
pipe_wall_a = HOSE_WALL / SC_A
draw_pipe_end(ax4a, sa_y(RIM_EXT_YD), sa_z(HOSE_RIM_Z),
              pipe_r_a, pipe_wall_a,
              fc=C_BROWN, ec=C_FRAME, bore_fc="white", zorder=9)

# ── Water surface in tray (away from sump) ───────────────────────────────────
FLOOD_DEPTH = 6
water_z_left = tray_z_at_near + TRAY_T + FLOOD_DEPTH
water_z_right = tray_z_at_far + TRAY_T + FLOOD_DEPTH
ax4a.fill([sa_y(sump_yd_end + 5), sa_y(tray_yd_far_view),
           sa_y(tray_yd_far_view), sa_y(sump_yd_end + 5)],
          [sa_z(water_z_left + 1), sa_z(water_z_right),
           sa_z(tray_z_at_far + TRAY_T), sa_z(tray_z_at_near + TRAY_T + 1)],
          fc="#B3D9F2", ec="none", alpha=0.3, zorder=3)
ax4a.plot([sa_y(sump_yd_end + 5), sa_y(tray_yd_far_view)],
         [sa_z(water_z_left + 1), sa_z(water_z_right)],
         color=C_BLUE, lw=1.0, ls="--", zorder=5)

# ── Walkway grate ───────────────────────────────────────────────────────────
ax4a.add_patch(plt.Rectangle((sa_y(0), sa_z(WK_DECK_H - WK_GRATE_T)),
              WALKWAY_W / SC_A, WK_GRATE_T / SC_A,
              fc="#E0D6C8", ec="#8D6E63", lw=1.0, hatch="///", zorder=3,
              alpha=0.7))

# Bracket arm (triangle)
ax4a.fill([sa_y(0), sa_y(0), sa_y(WALKWAY_W * 0.9)],
          [sa_z(WK_DECK_H - WK_GRATE_T), sa_z(WK_DECK_H - WK_GRATE_T - 30),
           sa_z(WK_DECK_H - WK_GRATE_T)],
          fc="#B0B0B8", ec=C_FRAME, lw=0.8, zorder=3, alpha=0.5)

# ── Detail dimensions ────────────────────────────────────────────────────────
# Rim top to floor
draw_dim_v(ax4a, sa_y(tray_yd_near - 25), sa_z(0), sa_z(RIM_TOP),
           f"{int(RIM_TOP)}mm\nRIM TOP AFF", offset=1.5, fs=7, right=False)

# Tray floor height above container floor
draw_dim_v(ax4a, sa_y(sump_yd_end + 30), sa_z(0), sa_z(TRAY_BASE_Z),
           f"{PROC_TRAY_SUMP_Z}mm\nTRAY FLOOR", offset=1.0, fs=6.5, right=True)

# Sump depth (same as tray floor height — shows the cavity)
draw_dim_v(ax4a, sa_y(sump_yd_end + 10), sa_z(sump_z_floor), sa_z(TRAY_BASE_Z),
           f"{PROC_TRAY_SUMP_Z}mm\nSUMP", offset=1.0, fs=7, right=True)

# Sump width (Yd extent)
draw_dim_h(ax4a, sa_y(sump_yd_start), sa_y(sump_yd_end),
           sa_z(sump_z_floor - 8),
           f"{PROC_TRAY_SUMP_D}mm", offset=0.8, fs=7, above=False)

# Pickup clearance from sump floor
draw_dim_v(ax4a, sa_y(tube_yd + TUBE_OD/2 + 8), sa_z(sump_z_floor), sa_z(tube_z_bot),
           "5mm", offset=0.6, fs=6, right=True)

# Sump to wall
draw_dim_h(ax4a, sa_y(0), sa_y(sump_yd_start), sa_z(RIM_TOP + 30),
           f"{sump_yd_start}mm", offset=0.8, fs=7)

# Walkway deck height
draw_dim_v(ax4a, sa_y(WALKWAY_W + 15), sa_z(0), sa_z(WK_DECK_H),
           f"{WK_DECK_H}mm DECK", offset=1.0, fs=6.5, right=True)

# ── Detail leaders ───────────────────────────────────────────────────────────
leader(ax4a, sa_y(tube_yd), sa_z(tube_z_bot + foot_valve_h/2),
       sa_y(tube_yd + 80), sa_z(-25),
       "1\" SS FOOT VALVE\nW/ STRAINER SCREEN", fs=7, color=C_FRAME)

leader(ax4a, sa_y(tube_yd), sa_z(tube_z_top - 5),
       sa_y(tube_yd + 90), sa_z(140),
       "1\" HDPE\nPICKUP TUBE", fs=7, color=C_FRAME)

leader(ax4a, sa_y(RIM_EXT_YD + 5), sa_z(HOSE_RIM_Z),
       sa_y(RIM_EXT_YD - 40), sa_z(HOSE_RIM_Z + 60),
       "1\" REINFORCED SUCTION\nHOSE ALONG RIM TO P-04\n(INTO PAGE — SEE PLAN)", fs=6, color=C_BROWN)

leader(ax4a, sa_y(sump_yd_start + PROC_TRAY_SUMP_D/4), sa_z(TRAY_BASE_Z / 2),
       sa_y(150), sa_z(-30),
       f"SUMP WELL\n({PROC_TRAY_SUMP_W}x{PROC_TRAY_SUMP_D}x{PROC_TRAY_SUMP_Z}mm)\nBOTTOM ON CONTAINER FLOOR", fs=6.5, color="#0D47A1")

leader(ax4a, sa_y(250), sa_z(water_z_left),
       sa_y(350), sa_z(TRAY_BASE_Z + rim_h + 10),
       "WATER LEVEL\n(6mm FLOOD)", fs=6.5, color=C_BLUE)

leader(ax4a, sa_y(150), sa_z(WK_DECK_H - WK_GRATE_T/2),
       sa_y(330), sa_z(155),
       "WALKWAY GRATING\n(WALL-CANTILEVERED)", fs=6, color="#8D6E63")

leader(ax4a, sa_y(250), sa_z(TRAY_BASE_Z / 2),
       sa_y(350), sa_z(TRAY_BASE_Z + rim_h /2),
       f"HDPE SHIM STRIP\n({PROC_TRAY_SHIM_W}mm WIDE,\n{PROC_TRAY_SUMP_Z}-{PROC_TRAY_SUMP_Z + PROC_TRAY_SHIM_H}mm)", fs=6, color="#A09070")

# Slope note
ax4a.text(sa_y(310), sa_z(-10),
          f"FALL: {PROC_TRAY_PITCH}mm / {PROC_TRAY_D:,}mm (1:220)\n"
          f"SLOPE EXAGGERATED {SLOPE_EXAG_A:.0f}x",
          ha="center", va="center", fontsize=6, color="#0D47A1",
          bbox=dict(fc="white", ec="#0D47A1", lw=0.5, pad=2, alpha=0.9),
          zorder=8)

# ═════════════════════════════════════════════════════════════════════════════
# PANEL B — FULL CROSS-SECTION ELEVATION (~1:15)
# Yd = -20 to 1150mm, Z = -50 to 1,150mm
# Shows tray, sump, suction hose routing to equipment panel (Yd=1046)
# ═════════════════════════════════════════════════════════════════════════════
SC_B = 12.0   # mm per drawing unit (wider view for panel routing)
OB_X = 1.0
OB_Y = 2.0

def sb_y(yd_mm):
    return OB_X + yd_mm / SC_B

def sb_z(z_mm):
    return OB_Y + z_mm / SC_B

ax4b.set_xlim(sb_y(-20) - 0.5, sb_y(1150) + 1.0)
ax4b.set_ylim(sb_z(-60) - 0.5, sb_z(620) + 1.5)

# Panel B title
ax4b.text(sb_y(550), sb_z(650), "SECTION A-A — SUMP TO EQUIPMENT PANEL (APPROX 1:12)",
          ha="center", va="top", fontsize=10, fontweight="bold",
          color="#1A237E", zorder=10)

# ── Container structure ──────────────────────────────────────────────────────
# Floor
ax4b.add_patch(plt.Rectangle((sb_y(-20), sb_z(-FLOOR_T)),
              1180 / SC_B, FLOOR_T / SC_B,
              fc="#B0B0B8", ec=C_FRAME, lw=1.5, zorder=2, hatch=".."))

# ── Shim strips (visible as small rectangles on floor) ───────────────────────
# Shims start at TRAY_BASE_Z (20mm) at near end and add slope on top
SLOPE_EXAG_B = 8.0
for shim_yd in [130, 250, 370, 490]:
    sh_h = TRAY_BASE_Z + (shim_yd - tray_yd_near) * slope_per_mm * SLOPE_EXAG_B
    ax4b.add_patch(plt.Rectangle((sb_y(shim_yd - 8), sb_z(0)),
                  16 / SC_B, max(sh_h, 1) / SC_B,
                  fc="#E8DCC0", ec="#A09070", lw=0.6, zorder=3))

# ── Tray ─────────────────────────────────────────────────────────────────────
tray_z_near_b = TRAY_BASE_Z  # 20mm — raised by sump depth
tray_z_far_b = TRAY_BASE_Z + (550 - tray_yd_near) * slope_per_mm * SLOPE_EXAG_B

# Tray floor
ax4b.fill([sb_y(tray_yd_near), sb_y(550), sb_y(550), sb_y(tray_yd_near)],
          [sb_z(tray_z_near_b), sb_z(tray_z_far_b),
           sb_z(tray_z_far_b + TRAY_T * 5), sb_z(tray_z_near_b + TRAY_T * 5)],
          fc="#C8D8E8", ec=C_FRAME, lw=1.2, zorder=4)

# Near rim — from tray floor (Z=20) up by rim height
ax4b.add_patch(plt.Rectangle((sb_y(tray_yd_near - 3), sb_z(TRAY_BASE_Z)),
              6 / SC_B, rim_h / SC_B,
              fc="#C8D8E8", ec=C_FRAME, lw=1.2, zorder=4))

# ── Sump well (simplified at this scale) ────────────────────────────────────
# Sump bottom at Z=0, tray floor at Z=TRAY_BASE_Z (20mm)
sump_yd_b = PROC_TRAY_DRAIN_YD
ax4b.add_patch(plt.Rectangle((sb_y(sump_yd_b), sb_z(0)),
              PROC_TRAY_SUMP_D / SC_B, PROC_TRAY_SUMP_Z / SC_B,
              fc="#B3D9F2", ec=C_FRAME, lw=1.2, alpha=0.6, zorder=5))

# Pickup tube (simplified) — from sump floor+5 to above rim
tube_yd_b = sump_yd_b + PROC_TRAY_SUMP_D / 2
RIM_TOP_B = TRAY_BASE_Z + rim_h  # 70mm
tube_z_top_b = WK_DECK_H + WK_GRATE_T + 10  # 135mm — above walkway grate + clearance
draw_pipe_path(ax4b, [tube_yd_b, tube_yd_b], [5, tube_z_top_b],
               TUBE_OD, TUBE_WALL, sb_y, sb_z,
               fc="#D0D0D0", ec=C_FRAME, zorder=5)
ax4b.text(sb_y(tube_yd_b + 20), sb_z(RIM_TOP_B + 35), "PICKUP\nTUBE",
          ha="left", va="bottom", fontsize=5.5, color=C_FRAME,
          fontweight="bold", zorder=6)

# ── Suction hose from pickup, along tray rim exterior to equipment panel ─────
P04_Z = PUMP_H_LO + 80  # P-04 on equipment panel
PANEL_YD = 1046           # equipment panel Yd position
RIM_EXT_YD_B = tray_yd_near - HOSE_OD / 2 - 5  # ~60mm — hose CL on rim exterior
HOSE_RIM_Z_B = TRAY_BASE_Z + rim_h / 2         # ~45mm — mid-rim height

# Hose path: short vertical overlap with tube top (creates 90° elbow) →
# horizontal above walkway → 90° elbow → down along rim exterior
ELBOW_OVERLAP_B = HOSE_OD
hose_b_y = [tube_yd_b, tube_yd_b, RIM_EXT_YD_B, RIM_EXT_YD_B]
hose_b_z = [tube_z_top_b - ELBOW_OVERLAP_B, tube_z_top_b, tube_z_top_b, HOSE_RIM_Z_B]
draw_pipe_path(ax4b, hose_b_y, hose_b_z, HOSE_OD, HOSE_WALL,
               sb_y, sb_z, fc=C_BROWN, ec="#5A3020", zorder=4)

# Pipe end-on at rim exterior (hose runs along X — into the page toward IBC corner)
pipe_r_b = HOSE_OD / 2 / SC_B
pipe_wall_b = HOSE_WALL / SC_B
draw_pipe_end(ax4b, sb_y(RIM_EXT_YD_B), sb_z(HOSE_RIM_Z_B),
              pipe_r_b, pipe_wall_b,
              fc=C_BROWN, ec=C_FRAME, bore_fc="white", zorder=6)

# Dashed routing indicator from rim to equipment panel
ax4b.plot([sb_y(RIM_EXT_YD_B), sb_y(PANEL_YD)],
          [sb_z(HOSE_RIM_Z_B), sb_z(P04_Z)],
          color=C_BROWN, lw=1.0, ls=":", zorder=3, alpha=0.6)
ax4b.text(sb_y((RIM_EXT_YD_B + PANEL_YD) / 2), sb_z((HOSE_RIM_Z_B + P04_Z) / 2 + 30),
          "HOSE ALONG RIM →\nCROSSES AT IBC CORNER\n(SEE PLAN VIEW)",
          ha="center", va="bottom", fontsize=5.5, color=C_BROWN,
          style="italic", zorder=4)

# ── Near walkway (Yd=0-300) ──────────────────────────────────────────────────
ax4b.add_patch(plt.Rectangle((sb_y(0), sb_z(WK_DECK_H - WK_GRATE_T)),
              WALKWAY_W / SC_B, WK_GRATE_T / SC_B,
              fc="#E0D6C8", ec="#8D6E63", lw=1.0, hatch="///", zorder=3,
              alpha=0.7))

# ── Equipment panel at Yd=1046 (dashed context) ─────────────────────────────
MANIFOLD_Z_LO = PUMP_H_LO
MANIFOLD_Z_HI = PUMP_H_HI
ax4b.add_patch(plt.Rectangle((sb_y(PANEL_YD - 9), sb_z(0)),
              18 / SC_B, (MANIFOLD_Z_HI + 100) / SC_B,
              fc="#D4C8A0", ec="#A09060", lw=1.5, zorder=3))
ax4b.add_patch(plt.Rectangle((sb_y(PANEL_YD - 20), sb_z(MANIFOLD_Z_LO)),
              60 / SC_B, (MANIFOLD_Z_HI - MANIFOLD_Z_LO) / SC_B,
              fc="none", ec=C_PUMP, lw=1.5, ls="--", zorder=3))
ax4b.text(sb_y(PANEL_YD + 50), sb_z((MANIFOLD_Z_LO + MANIFOLD_Z_HI) / 2),
          "EQUIP\nPANEL\n(Yd=1046)",
          ha="left", va="center", fontsize=5.5, color=C_PUMP, style="italic",
          zorder=4)

# ── P-04 pump (on equipment panel) ──────────────────────────────────────────
pump_r_b = 25  # mm
DV_YD_B = PANEL_YD
ax4b.add_patch(plt.Circle((sb_y(DV_YD_B), sb_z(P04_Z)),
              pump_r_b / SC_B,
              fc="#E8884A", ec=C_FRAME, lw=1.5, zorder=5))
ax4b.text(sb_y(DV_YD_B), sb_z(P04_Z), "P-04",
          ha="center", va="center", fontsize=7, fontweight="bold",
          color="white", zorder=6)

# ── 3W-DV-02 diverter valve (on P-04 discharge) ─────────────────────────────
DV_Z_B = P04_Z + 100   # above pump
dv_w_b = 60
dv_h_b = 40

# P-04 discharge to diverter
draw_pipe_path(ax4b, [DV_YD_B, DV_YD_B],
               [P04_Z + pump_r_b, DV_Z_B - dv_h_b/2],
               TUBE_OD, TUBE_WALL, sb_y, sb_z,
               fc=C_BROWN, ec="#5A3020", zorder=4)

# Diverter box
ax4b.add_patch(plt.Rectangle((sb_y(DV_YD_B - dv_w_b/2), sb_z(DV_Z_B - dv_h_b/2)),
              dv_w_b / SC_B, dv_h_b / SC_B,
              fc="#FFF9C4", ec=C_FRAME, lw=1.5, zorder=5))
ax4b.text(sb_y(DV_YD_B), sb_z(DV_Z_B), "3W-DV-02",
          ha="center", va="center", fontsize=6.5, fontweight="bold", zorder=6)

# ── Discharge from diverter to IBC-3 ────────────────────────────────────────
# IBC-3 is nearby (equipment panel is in the IBC corridor). From the diverter,
# the pipe runs along the panel toward IBC-3. In this cross-section (looking
# along +X), the run goes INTO the page — shown as a pipe end-on.
IBC3_FILL_Z = IBC_H_600   # ~1,010mm
ELBOW_Z = DV_Z_B + dv_h_b/2 + 40  # short rise above diverter

# Short vertical rise from diverter to elbow
draw_pipe_path(ax4b, [DV_YD_B, DV_YD_B],
               [DV_Z_B + dv_h_b/2, ELBOW_Z],
               TUBE_OD, TUBE_WALL, sb_y, sb_z,
               fc=C_BROWN, ec="#5A3020", zorder=4)

# Pipe end-on (circle with bore) — 90° elbow turns into the page toward IBC-3
# Centered on the vertical pipe centerline (DV_YD_B) at the top of the rise
pipe_end_r = TUBE_OD / 2 / SC_B
pipe_end_wall = TUBE_WALL / SC_B
draw_pipe_end(ax4b, sb_y(DV_YD_B), sb_z(ELBOW_Z),
              pipe_end_r, pipe_end_wall,
              fc=C_BROWN, ec=C_FRAME, zorder=6)

# Label
leader(ax4b, sb_y(DV_YD_B + 20), sb_z(ELBOW_Z),
       sb_y(DV_YD_B + 80), sb_z(ELBOW_Z + 80),
       f"90° ELBOW TO IBC-3\nVIA PANEL-MOUNTED 1\" LINE\n(INTO PAGE)", fs=6.5,
       color=C_BROWN)

# ── Waste branch (dashed) — IBC-4 is in the corridor (higher Yd) ────────────
ax4b.annotate("", xy=(sb_y(DV_YD_B + dv_w_b/2 + 40), sb_z(DV_Z_B)),
             xytext=(sb_y(DV_YD_B + dv_w_b/2), sb_z(DV_Z_B)),
             arrowprops=dict(arrowstyle="-|>", color=C_BLACK, lw=1.5,
                             linestyle="--", mutation_scale=10),
             zorder=3)
ax4b.text(sb_y(DV_YD_B + dv_w_b/2 + 55), sb_z(DV_Z_B),
          "IBC-4\n(WASTE)",
          ha="center", va="center", fontsize=6, color=C_BLACK,
          style="italic", zorder=4)

# ── Dimensions ───────────────────────────────────────────────────────────────
# Floor to manifold bottom (near equipment panel)
draw_dim_v(ax4b, sb_y(PANEL_YD + 60), sb_z(0), sb_z(MANIFOLD_Z_LO),
           f"{MANIFOLD_Z_LO}mm", offset=0.5, fs=7, right=True)

# Floor to manifold top
draw_dim_v(ax4b, sb_y(PANEL_YD + 100), sb_z(0), sb_z(MANIFOLD_Z_HI),
           f"{MANIFOLD_Z_HI}mm", offset=0.6, fs=6.5, right=True)

# Rim top above floor
draw_dim_v(ax4b, sb_y(tray_yd_near - 30), sb_z(0), sb_z(RIM_TOP_B),
           f"{int(RIM_TOP_B)}mm", offset=0.4, fs=6.5, right=False)

# Walkway
draw_dim_v(ax4b, sb_y(WALKWAY_W + 15), sb_z(0), sb_z(WK_DECK_H),
           f"{WK_DECK_H}mm", offset=0.4, fs=6, right=True)

# ── Labels ───────────────────────────────────────────────────────────────────
leader(ax4b, sb_y(WALKWAY_W/2), sb_z(WK_DECK_H),
       sb_y(200), sb_z(WK_DECK_H + 40),
       "WALKWAY", fs=6.5, color="#8D6E63")

leader(ax4b, sb_y(DV_YD_B), sb_z(P04_Z + pump_r_b + 5),
       sb_y(DV_YD_B - 120), sb_z(P04_Z + 80),
       "SHURFLO 2088\n12V DC, 3.5 GPM\nSELF-PRIMING", fs=6, color=C_PUMP)

# ═════════════════════════════════════════════════════════════════════════════
# PANEL C — PLAN VIEW: HOSE ROUTING ALONG TRAY RIM (~1:8)
# Looking down. Yd horizontal (wall at left, panel at right).
# X vertical (lower X at bottom, higher X at top).
# Shows hose along near rim exterior, around tray corner, to equipment panel.
# ═════════════════════════════════════════════════════════════════════════════
SC_C = 8.0   # mm per drawing unit
OC_H = 1.0   # horizontal offset (Yd=0 position)
OC_V = 1.5   # vertical offset (X baseline)

SUMP_X = PROC_TRAY_DRAIN_X   # 4,550mm
TRAY_X_R = PROC_TRAY_X_R     # 4,629mm
IBC_X = IBC_COL_X             # 4,674mm
EP_X = EQPANEL_X              # 4,800mm — equipment panel left edge
EP_W = EQPANEL_W              # 780mm — equipment panel width in X
X_VIEW_BOT = 4350
X_VIEW_TOP = EP_X + EP_W / 2 + 80  # ~5,270mm — includes P-04 center
YD_VIEW_L = -30
YD_VIEW_R = 1130

def sc_yd_c(yd_mm):
    return OC_H + (yd_mm - YD_VIEW_L) / SC_C

def sc_x_c(x_mm):
    return OC_V + (x_mm - X_VIEW_BOT) / SC_C

ax4c.set_xlim(sc_yd_c(YD_VIEW_L) - 0.5, sc_yd_c(YD_VIEW_R) + 0.5)
ax4c.set_ylim(sc_x_c(X_VIEW_BOT - 30) - 0.5, sc_x_c(X_VIEW_TOP + 30) + 0.5)

# Panel C title
ax4c.text(sc_yd_c((YD_VIEW_L + YD_VIEW_R) / 2), sc_x_c(X_VIEW_TOP + 15),
          "PLAN VIEW — HOSE ROUTING ALONG TRAY RIM (APPROX 1:8)",
          ha="center", va="top", fontsize=9, fontweight="bold",
          color="#1A237E", zorder=10)

# ── Container wall (Yd=0, vertical line at left) ───────────────────────────
ax4c.add_patch(plt.Rectangle((sc_yd_c(-WALL_T), sc_x_c(X_VIEW_BOT - 20)),
              WALL_T / SC_C, (X_VIEW_TOP - X_VIEW_BOT + 40) / SC_C,
              fc="#B0B0B8", ec=C_FRAME, lw=1.2, zorder=2, hatch=".."))

# ── Tray outline (partial) ─────────────────────────────────────────────────
tray_x_l_vis = max(PROC_TRAY_X_L, X_VIEW_BOT)
ax4c.add_patch(plt.Rectangle((sc_yd_c(tray_yd_near), sc_x_c(tray_x_l_vis)),
              (400 - tray_yd_near) / SC_C,
              (TRAY_X_R - tray_x_l_vis) / SC_C,
              fc="#E8F0F8", ec="#C8D8E8", lw=1.0, zorder=2, alpha=0.4))
ax4c.text(sc_yd_c(200), sc_x_c((tray_x_l_vis + TRAY_X_R) / 2),
          "PROCESSING\nTRAY", ha="center", va="center",
          fontsize=6, color="#6A8CAF", style="italic", alpha=0.7, zorder=3)

# Near rim line (Yd=80, runs along X)
ax4c.plot([sc_yd_c(tray_yd_near), sc_yd_c(tray_yd_near)],
         [sc_x_c(tray_x_l_vis), sc_x_c(TRAY_X_R)],
         color="#C8D8E8", lw=2.0, zorder=4)

# Right rim line (X=4,629, runs along Yd)
ax4c.plot([sc_yd_c(tray_yd_near), sc_yd_c(400)],
         [sc_x_c(TRAY_X_R), sc_x_c(TRAY_X_R)],
         color="#C8D8E8", lw=2.0, zorder=4)

# ── Sump (small rectangle inside tray at near rim) ─────────────────────────
ax4c.add_patch(plt.Rectangle(
    (sc_yd_c(PROC_TRAY_DRAIN_YD), sc_x_c(SUMP_X - PROC_TRAY_SUMP_W / 2)),
    PROC_TRAY_SUMP_D / SC_C, PROC_TRAY_SUMP_W / SC_C,
    fc="#B3D9F2", ec=C_FRAME, lw=1.0, zorder=5))
ax4c.text(sc_yd_c(PROC_TRAY_DRAIN_YD + PROC_TRAY_SUMP_D / 2),
          sc_x_c(SUMP_X),
          "SUMP", ha="center", va="center", fontsize=5.5,
          fontweight="bold", color="#0D47A1", zorder=6)

# ── Pickup tube end-on (vertical tube seen from above) ─────────────────────
tube_r_c = TUBE_OD / 2 / SC_C
tube_wall_c = TUBE_WALL / SC_C
draw_pipe_end(ax4c, sc_yd_c(tube_yd), sc_x_c(SUMP_X),
              tube_r_c, tube_wall_c,
              fc="#D0D0D0", ec=C_FRAME, bore_fc="white", zorder=7)

# ── Equipment panel (Yd=1,046, vertical strip at right) ────────────────────
ax4c.add_patch(plt.Rectangle(
    (sc_yd_c(CORRIDOR_YD_NEAR - 9), sc_x_c(EP_X)),
    18 / SC_C, EP_W / SC_C,
    fc="#D4C8A0", ec="#A09060", lw=1.5, zorder=3))
ax4c.text(sc_yd_c(CORRIDOR_YD_NEAR + 15), sc_x_c(EP_X + EP_W / 2),
          "EQUIPMENT\nPANEL\n(Yd=1,046)",
          ha="left", va="center", fontsize=5.5, color=C_PUMP,
          style="italic", zorder=4)

# P-04 on equipment panel (roughly at lower quarter of panel in X)
P04_PLAN_X = EP_X + EP_W * 0.25
ax4c.add_patch(plt.Circle(
    (sc_yd_c(CORRIDOR_YD_NEAR), sc_x_c(P04_PLAN_X)),
    20 / SC_C,
    fc="#E8884A", ec=C_FRAME, lw=1.2, zorder=6))
ax4c.text(sc_yd_c(CORRIDOR_YD_NEAR), sc_x_c(P04_PLAN_X),
          "P-04", ha="center", va="center", fontsize=5.5,
          fontweight="bold", color="white", zorder=7)

# ── Hose routing along tray rim exterior ───────────────────────────────────
# Step 1: Short Yd crossing from pickup tube to rim exterior
RIM_EXT_YD_C = tray_yd_near - HOSE_OD / 2 - 5  # ~60mm
draw_pipe_path(ax4c,
               [tube_yd, RIM_EXT_YD_C],
               [SUMP_X, SUMP_X],
               HOSE_OD, HOSE_WALL, sc_yd_c, sc_x_c,
               fc=C_BROWN, ec="#5A3020", zorder=6)

# Step 2: Along near rim exterior in X direction (toward tray right corner)
CORNER_X = TRAY_X_R + 15   # just past tray right edge
draw_pipe_path(ax4c,
               [RIM_EXT_YD_C, RIM_EXT_YD_C],
               [SUMP_X, CORNER_X],
               HOSE_OD, HOSE_WALL, sc_yd_c, sc_x_c,
               fc=C_BROWN, ec="#5A3020", zorder=6)

# Step 3: Around tray corner, cross in Yd to equipment panel
draw_pipe_path(ax4c,
               [RIM_EXT_YD_C, CORRIDOR_YD_NEAR],
               [CORNER_X, CORNER_X],
               HOSE_OD, HOSE_WALL, sc_yd_c, sc_x_c,
               fc=C_BROWN, ec="#5A3020", zorder=6)

# Step 4: Along equipment panel face to P-04
draw_pipe_path(ax4c,
               [CORRIDOR_YD_NEAR, CORRIDOR_YD_NEAR],
               [CORNER_X, P04_PLAN_X],
               HOSE_OD, HOSE_WALL, sc_yd_c, sc_x_c,
               fc=C_BROWN, ec="#5A3020", zorder=6)

# P-clip marks along rim run (small ticks)
for clip_x in range(SUMP_X, CORNER_X, 60):
    ax4c.plot([sc_yd_c(RIM_EXT_YD_C - 8), sc_yd_c(RIM_EXT_YD_C + 8)],
             [sc_x_c(clip_x), sc_x_c(clip_x)],
             color="#666666", lw=0.6, zorder=5)

# ── Labels ──────────────────────────────────────────────────────────────────
leader(ax4c, sc_yd_c(RIM_EXT_YD_C), sc_x_c(SUMP_X - 50),
       sc_yd_c(RIM_EXT_YD_C - 60), sc_x_c(X_VIEW_BOT + 50),
       "1\" SUCTION HOSE\nALONG RIM EXTERIOR\n(P-CLIPPED TO RIM)", fs=6, color=C_BROWN)

leader(ax4c, sc_yd_c((RIM_EXT_YD_C + CORRIDOR_YD_NEAR) / 2), sc_x_c(CORNER_X),
       sc_yd_c(500), sc_x_c(CORNER_X + 60),
       "CROSSES TO\nEQUIPMENT PANEL\nAT TRAY CORNER", fs=6, color=C_BROWN)

# ── Dimensions ──────────────────────────────────────────────────────────────
# Rim-to-panel Yd distance
draw_dim_h(ax4c, sc_yd_c(RIM_EXT_YD_C), sc_yd_c(CORRIDOR_YD_NEAR),
           sc_x_c(X_VIEW_BOT + 20),
           f"{CORRIDOR_YD_NEAR - RIM_EXT_YD_C:.0f}mm", offset=0.8, fs=6)

# Hose run along rim (X distance)
draw_dim_v(ax4c, sc_yd_c(RIM_EXT_YD_C - 25), sc_x_c(SUMP_X), sc_x_c(CORNER_X),
           f"{CORNER_X - SUMP_X}mm", offset=0.5, fs=6, right=False)

# ── Notes axes (full-width strip above title block) ─────────────────────────
ax4_notes = fig4.add_axes([0.04, 0.06, 0.92, 0.10])
ax4_notes.set_xlim(0, 100)
ax4_notes.set_ylim(0, 10)
ax4_notes.axis("off")

notes4 = [
    "NOTES:",
    "1. Sump bottom sits ON container floor (Z=0).",
    "2. Tray floor raised to Z=20mm (sump depth).",
    "3. Shims taper 20-30mm (base + slope).",
    "4. Pickup tube lifts out for cleaning (no tools).",
    "5. P-04: Shurflo 2088, 12V DC, self-priming, on equipment panel.",
    "6. Hose runs along tray rim exterior, P-clipped to rim.",
    "7. Tray slope exaggerated for clarity in elevation panels.",
]
draw_notes(ax4_notes, notes4, 42, 9, spacing=1.0,
           fs=6.5, width=24, color=C_TEXT, title_color=C_TEXT,
           font={"fontfamily": "monospace"})

flow_notes = [
    "FLOW PATH:",
    "1. Water drains by gravity to sump well (Yd=80mm)",
    "2. P-04 suction pickup draws from sump via foot valve",
    "3. 1\" hose along rim exterior to tray corner, then to equip panel",
    "4. P-04 discharge to 3W-DV-02 three-way diverter",
    "5. Default: lifts to IBC-3 (Brown, ~900mm head)",
    "6. Alt: divert to IBC-4 (Waste) when selected",
]
draw_notes(ax4_notes, flow_notes, 70, 9, spacing=1.0,
           fs=6.5, width=24, color=C_TEXT, title_color=C_TEXT,
           font={"fontfamily": "monospace"})

fig4.savefig("diagrams/water-system-sheet4.png", dpi=150, bbox_inches="tight",
             facecolor=fig4.get_facecolor())
fig4.savefig(svg_path("diagrams/water-system-sheet4.png"), bbox_inches="tight",
             facecolor=fig4.get_facecolor())
plt.close(fig4)
print("Sheet 4 written --> diagrams/water-system-sheet4.png")
print("Done.")
