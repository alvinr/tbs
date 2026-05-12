#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_water_system.py
Generates three engineering diagrams for the cyanotype processing water system:
  Sheet 1 — System flow schematic (three-system P&ID overview)
  Sheet 2 — Tank & filter skid layout plan (dimensioned arrangement)
  Sheet 3 — Processing tray drainage plan (slope direction, flow arrows, drain)

Output:
  water-system-sheet1.png  (1800 x 1200 px, 150 dpi)
  water-system-sheet2.png  (1800 x 1200 px, 150 dpi)
  water-system-sheet3.png  (1800 x 1200 px, 150 dpi)
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
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_W, PROC_TRAY_D,
    PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR, PROC_TRAY_RIM, PROC_TRAY_PITCH,
    PROC_TRAY_DRAIN_X, PROC_TRAY_DRAIN_YD,
    WALKWAY_W, WALKWAY_NEAR_YD, WALKWAY_FAR_YD,
    C_BLUE_IBC, C_BROWN_IBC, C_WASTE_IBC, C_PUMP, C_WALL,
    svg_path, SVG_DIR,
)
import os
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v

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

def pump(ax, x, y, color=C_BLUE, zorder=5, r=0.05):
    """Draw a centrifugal pump symbol (circle with triangle arrow)."""
    circ = plt.Circle((x, y), r, fc="white", ec=color, lw=1.8, zorder=zorder)
    ax.add_patch(circ)
    # Triangle inside
    tri = plt.Polygon([(x - r*0.55, y - r*0.55),
                       (x - r*0.55, y + r*0.55),
                       (x + r*0.65, y)],
                      fc=color, ec=color, zorder=zorder + 1)
    ax.add_patch(tri)

def valve(ax, x, y, color=C_BLUE, zorder=5, size=0.04, label="V"):
    """Draw a ball valve symbol (bowtie)."""
    tri1 = plt.Polygon([(x - size, y - size),
                        (x - size, y + size),
                        (x, y)],
                       fc=color, ec=color, alpha=0.85, zorder=zorder)
    tri2 = plt.Polygon([(x + size, y - size),
                        (x + size, y + size),
                        (x, y)],
                       fc=color, ec=color, alpha=0.85, zorder=zorder)
    ax.add_patch(tri1)
    ax.add_patch(tri2)

def filter_sym(ax, x, y, color=C_FILT, zorder=4, label="F"):
    """Draw a filter symbol (pentagon/diamond)."""
    size = 0.07
    h    = 0.09
    pts  = [(x, y + h*0.6),
            (x + size*0.7, y + h*0.2),
            (x + size*0.5, y - h*0.5),
            (x - size*0.5, y - h*0.5),
            (x - size*0.7, y + h*0.2)]
    poly = plt.Polygon(pts, fc=color, ec=C_FRAME, lw=1.2, zorder=zorder)
    ax.add_patch(poly)
    ax.text(x, y, label, ha="center", va="center", fontsize=6, zorder=zorder + 1,
            fontweight="bold")

def note(ax, x, y, txt, fs=6.5, color=C_TEXT):
    ax.text(x, y, txt, ha="left", va="center", fontsize=fs, color=color,
            zorder=10)

def pipe_bridge(ax, x, y, direction='h', r=0.14, color=C_FRAME, lw=LW_PIPE,
                zorder=11, bg='white'):
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
    ax.plot(bx, by, color=color, lw=lw, zorder=zorder, solid_capstyle='round')

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
X_J  = 12.07                # Y-junction X: floor drain + bypass merge before waste IBC
Y_J  = 5.62                 # Y level of Y-junction (matches heavy contam bypass exit)

# ── BLUE SYSTEM ───────────────────────────────────────────────────────────────
# IBC1 Clean water A
tank(ax1, 1.5, 8.2, 1.4, 1.4, fc="#BBDEFB", ec=C_BLUE_IBC, lw=2,
     label="IBC-1", sublabel="159 gal (600L)\nCLEAN A")
# IBC2 Clean water B
tank(ax1, 3.3, 8.2, 1.4, 1.4, fc="#BBDEFB", ec=C_BLUE_IBC, lw=2,
     label="IBC-2", sublabel="159 gal (600L)\nCLEAN B")

# Manifold joining two tanks
pipe(ax1, 1.5, 7.48, 1.5, 7.0, C_BLUE)
pipe(ax1, 3.3, 7.48, 3.3, 7.0, C_BLUE)
pipe(ax1, 1.5, 7.0, 3.3, 7.0, C_BLUE)  # crossmember

# Valve on outlet
valve(ax1, 2.4, 7.0, color=C_BLUE)
ax1.text(2.4, 7.12, "BV-01", ha="center", fontsize=6, color=C_BLUE)

# Pump P1
pipe(ax1, 2.4, 7.0, 2.4, 6.5, C_BLUE)
arrow_pipe(ax1, 2.4, 6.9, 2.4, 6.6, color=C_BLUE)
pump(ax1, 2.4, 6.3, color=C_PUMP)
ax1.text(2.75, 6.3, "P-01\n12VDC\n3.5 GPM", ha="left", fontsize=6, color=C_PUMP)

# Pressure accumulator
pipe(ax1, 2.4, 6.1, 2.4, 5.6, C_BLUE)
box(ax1, 2.4, 5.35, 0.8, 0.45, fc="#E3F2FD", ec=C_BLUE, lw=1.5)
ax1.text(2.4, 5.35, "ACC-01\n1 GAL", ha="center", va="center",
         fontsize=6, color=C_BLUE)

# Valve + run to processing
pipe(ax1, 2.4, 5.12, 2.4, 4.5, C_BLUE)
arrow_pipe(ax1, 2.4, 4.95, 2.4, 4.65, color=C_BLUE)
valve(ax1, 2.4, 4.5, color=C_BLUE)
ax1.text(2.4, 4.37, "BV-02", ha="center", fontsize=6, color=C_BLUE)
pipe(ax1, 2.4, 4.3, 2.4, 3.8, C_BLUE)
# Run east to spray bar riser tap-off — humps over blue return (X=9.7) and waste vertical (W_X)
pipe(ax1, 2.4, 3.8, 14.5, 3.8, C_BLUE)
pipe_bridge(ax1, 9.7,   3.8, color=C_BLUE, lw=LW_PIPE, bg=C_BROWN_L)
pipe_bridge(ax1, W_X,   3.8, color=C_BLUE, lw=LW_PIPE, bg=C_BLACK_L)
ax1.text(12.75, 4.0, "1\" HDPE — BLUE (SUPPLY)", ha="center",
         fontsize=7, color=C_BLUE)

# External fill port (top of IBC-1, via bulkhead fitting in far wall)
pipe(ax1, 1.5, 8.9, 1.5, 9.6, C_BLUE, style="--")
ax1.text(1.5, 9.75, "EXTERNAL FILL\nPORT (2\" NPT)", ha="center", fontsize=6,
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
pipe(ax1, 6.4, 7.48, 6.4, 7.0, C_BROWN)
valve(ax1, 6.4, 7.0, color=C_BROWN)
ax1.text(6.6, 6.97, "BV-03", ha="center", fontsize=6, color=C_BROWN)
pipe(ax1, 6.4, 6.8, 6.4, 6.3, C_BROWN)
# Arrow from processing area — humps over blue return (X=9.7) and waste vertical (W_X)
pipe(ax1, 6.4, 6.3, 15.65, 6.3, C_BROWN, style="--")
pipe_bridge(ax1, 9.7,   6.3, color=C_BROWN, lw=LW_PIPE, bg=C_BROWN_L)
pipe_bridge(ax1, W_X,   6.3, color=C_BROWN, lw=LW_PIPE, bg=C_BLACK_L)
pipe_bridge(ax1, 14.5,  6.3, color=C_BROWN, lw=LW_PIPE, bg=C_PROC)   # brown over spray bar riser
arrow_pipe(ax1, 6.6, 6.3, 6.4, 6.3, color=C_BROWN)
ax1.text(8.1, 6.1, "1\" HDPE — BROWN (DRAIN FROM FLOOR)", ha="center",
         fontsize=7, color=C_BROWN)

# Brown pump P2 — outlet from bottom of IBC-3
pipe(ax1, 6.4, 7.48, 6.4, 5.6, C_BROWN)
arrow_pipe(ax1, 6.4, 7.0, 6.4, 6.0, color=C_BROWN)       # downward from IBC-3
pump(ax1, 6.4, 5.4, color=C_PUMP)
ax1.text(6.75, 5.4, "P-02\n12VDC\n3.5 GPM", ha="left", fontsize=6, color=C_PUMP)

pipe(ax1, 6.4, 5.2, 6.4, 4.8, C_BROWN)

# ── FILTER SKID ───────────────────────────────────────────────────────────────
ax1.add_patch(plt.Rectangle((5.2, 3.0), 3.8, 2.0, fc=C_FILT, ec="#F57F17",
                             lw=1.5, alpha=0.8, zorder=1))
ax1.text(7.1, 4.88, "FILTER SKID", ha="center", fontsize=7.5,
         fontweight="bold", color="#E65100")

# Filter 1 — 50 micron sediment
filter_sym(ax1, 6.0, 3.9, label="F1")
ax1.text(6.6, 3.35, "50μ\nSEDIMENT", ha="center", fontsize=6, color="#E65100")
pipe(ax1, 6.4, 4.6, 6.0, 4.6, C_BROWN)
arrow_pipe(ax1, 6.3, 4.6, 6.1, 4.6, color=C_BROWN)       # leftward to F1
pipe(ax1, 6.0, 4.6, 6.0, 4.0, C_BROWN)
pipe(ax1, 6.0, 3.8, 6.0, 3.55, C_BROWN)

# Filter 2 — 5 micron sediment
filter_sym(ax1, 7.1, 3.9, label="F2")
ax1.text(7.6, 3.35, "5μ\nSEDIMENT", ha="center", fontsize=6, color="#E65100")
pipe(ax1, 6.0, 3.55, 6.0, 3.25, C_BROWN)
pipe(ax1, 6.0, 3.25, 7.1, 3.25, C_BROWN)
arrow_pipe(ax1, 6.4, 3.25, 6.8, 3.25, color=C_BROWN)     # rightward F1→F2
pipe(ax1, 7.1, 3.25, 7.1, 3.55, C_BROWN)
pipe(ax1, 7.1, 3.8, 7.1, 4.6, C_BROWN)
arrow_pipe(ax1, 7.1, 4.0, 7.1, 4.4, color=C_BROWN)       # upward F2 out

# Filter 3 — GAC carbon
filter_sym(ax1, 8.2, 3.9, label="F3")
ax1.text(8.6, 3.35, "GAC\nCARBON", ha="center", fontsize=6, color="#E65100")
pipe(ax1, 7.1, 4.6, 7.1, 4.6, C_BROWN)
pipe(ax1, 7.1, 4.6, 8.2, 4.6, C_BROWN)
arrow_pipe(ax1, 7.5, 4.6, 7.9, 4.6, color=C_BROWN)       # rightward F2→F3
pipe(ax1, 8.2, 4.6, 8.2, 4.0, C_BROWN)
pipe(ax1, 8.2, 3.8, 8.2, 3.25, C_BROWN)

# pH test point
pipe(ax1, 8.2, 3.25, 8.9, 3.25, C_BROWN)
arrow_pipe(ax1, 8.6, 3.25, 9.1, 3.25, color=C_BROWN)     # rightward to DV-01
box(ax1, 9.15, 3.25, 0.45, 0.35, fc="#FFF176", ec="#F9A825", lw=1.5)
ax1.text(9.15, 3.25, "pH\nTEST", ha="center", va="center", fontsize=5.5,
         color="#E65100")

# ── DIVERTER VALVE after filter — back to Blue OR forward to Black ─────────────
pipe(ax1, 9.4, 3.25, 9.7, 3.25, C_BROWN)
valve(ax1, 9.7, 3.25, color="#777777", size=0.05)
ax1.text(9.7, 3.0, "3W-DV-01\nDIVERTER", ha="center", fontsize=6, color="#444")

# Path back to Blue IBC — split at Y=3.8 (blue supply crosses over) and Y=6.3 (brown drain crosses over)
pipe(ax1, 9.7, 3.5,        9.7, 3.8 - BR,  C_BLUE, style="--")   # below blue supply
pipe(ax1, 9.7, 3.8 + BR,   9.7, 6.3 - BR,  C_BLUE, style="--")   # between crossings
pipe(ax1, 9.7, 6.3 + BR,   9.7, 10.3,      C_BLUE, style="--")   # above brown drain → raised
arrow_pipe(ax1, 9.7, 5.5, 9.7, 7.0, color=C_BLUE)                # upward return
pipe(ax1, 9.7, 10.3, 3.3, 10.3, C_BLUE, style="--")
arrow_pipe(ax1, 7.5, 10.3, 5.0, 10.3, color=C_BLUE)              # leftward return
pipe(ax1, 3.3, 10.3, 3.3, 8.9, C_BLUE, style="--")               # drop into IBC-2 top
ax1.text(6.5, 10.15, "RECYCLED → BLUE IBC-2 (if pH & clarity OK)",
         ha="center", fontsize=6, color=C_BLUE, style="italic")

# Path to Black system
pipe(ax1, 9.7, 3.0, 9.7, 2.5, C_BLACK)
arrow_pipe(ax1, 9.7, 2.85, 9.7, 2.6, color=C_BLACK)       # downward from DV-01
pipe(ax1, 9.7, 2.5, W_X, 2.5, C_BLACK)
arrow_pipe(ax1, 10.3, 2.5, W_X, 2.5, color=C_BLACK)       # rightward to waste IBC

# ── BLACK SYSTEM ──────────────────────────────────────────────────────────────
tank(ax1, W_X, W_Y, W_W, W_H, fc="#D5D5D0", ec=C_WASTE_IBC, lw=2,
     label="IBC-4", sublabel="159 gal (600L)\nWASTE")

# Heavy contamination bypass — left side of processing floor
pipe(ax1, 14.1, Y_J, X_J, Y_J, C_BLACK, style="-.")
valve(ax1, 12.6, 5.62, color=C_BLACK)                      # BV-04
ax1.text(12.6, 5.80, "BV-04", ha="center", fontsize=6, color=C_BLACK)
arrow_pipe(ax1, 13.8, 5.62, 12.0, 5.62, color=C_BLACK)    # leftward bypass flow
ax1.text(12.6, 5.44, "HEAVY CONTAM. BYPASS", ha="center",
         fontsize=6, color=C_BLACK, style="italic")

# Y-junction: floor drain riser meets heavy contam bypass at (X_J, Y_J)
pipe(ax1, X_J, 2.6,       X_J, 3.8 - BR,  C_BLACK)  # floor drain riser (below blue)
pipe_bridge(ax1, X_J, 3.8, direction='v', color=C_BLACK, lw=LW_PIPE, bg=C_BLACK_L)  # black over blue
pipe(ax1, X_J, 3.8 + BR,  X_J, Y_J,        C_BLACK)  # riser (above blue → junction)
# Combined flow exits junction left into waste IBC vertical
pipe(ax1, X_J, Y_J,  W_X, Y_J, C_BLACK)              # junction → waste IBC vertical
# Waste IBC vertical — filter skid feeds from Y=2.5; Y-junction joins at Y_J
pipe(ax1, W_X, 2.5,       W_X, 3.8 - BR,  C_BLACK)   # filter feed to blue crossing
pipe(ax1, W_X, 3.8 + BR,  W_X, 6.3 - BR,  C_BLACK)   # blue crossing to brown crossing
pipe(ax1, W_X, 6.3 + BR,  W_X, W_Y - W_H/2,  C_BLACK)  # brown crossing to IBC bottom
arrow_pipe(ax1, W_X, 3.2, W_X, 4.5,       color=C_BLACK)   # upward flow (lower)
arrow_pipe(ax1, W_X, Y_J + 0.1, W_X, W_Y - W_H/2 - 0.1, color=C_BLACK)  # upward (upper)

# External drain port — exits right side of black system box
DISP_X = 13.3
DISP_Y = W_Y - W_H/2 - 0.3
pipe(ax1, W_X, W_Y - W_H/2, W_X, DISP_Y, C_BLACK)    # IBC bottom → down
pipe(ax1, W_X, DISP_Y, DISP_X, DISP_Y, C_BLACK)      # right to near box edge
pipe(ax1, DISP_X, DISP_Y, DISP_X, 10.75, C_BLACK)    # up and out top of box
ax1.annotate("", xy=(DISP_X, 11.05), xytext=(DISP_X, 10.8),
             arrowprops=dict(arrowstyle="-|>", color=C_BLACK, lw=2,
                             mutation_scale=14), zorder=4)
ax1.text(DISP_X, 11.2, "EXTERNAL DRAIN\nPORT (2\" NPT)", ha="center",
         fontsize=6.5, color=C_BLACK, fontweight="bold", va="bottom")

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
ax1.text(15.6, 4.4, "TRAY DRAIN\n+ DIVERTER", ha="center",
         fontsize=6, color="#388E3C")

# 3-way valve at drain
pipe(ax1, 15.6, 4.0, 15.6, 3.65, C_BROWN)                      # drain circle → valve
valve(ax1, 15.6, 3.6, color="#777777", size=0.05)
ax1.text(15.6, 3.4, "3W-DV-02", ha="center", fontsize=6, color="#444")
# to brown: short horizontal from valve left to brown return riser
pipe(ax1, 15.1, 3.6, 15.55, 3.6, C_BROWN)                      # valve → brown return
pipe(ax1, 15.1, 3.6, 15.1, 6.3, C_BROWN)                      # brown return riser
arrow_pipe(ax1, 15.1, 4.5, 15.1, 5.5, color=C_BROWN)          # upward drain return
# to black: diverter outlet → down → left → DRUM-1 (heavy contamination route)
pipe(ax1, 15.6, 3.35, 15.6, 2.6, C_BLACK)
pipe(ax1, 15.6, 2.6, X_J,  2.6, C_BLACK)
arrow_pipe(ax1, 14.5, 2.6, 12.5, 2.6, color=C_BLACK)
ax1.text(13.5, 2.42, "TO WASTE IBC (HEAVY CONTAM.)", ha="center", fontsize=6,
         color=C_BLACK, style="italic")

# Spray bar riser — blue supply tap-off at Y=3.8 up to spray bar at Y=8.0
# Brown drain (Y=6.3) bridges over; riser is split with gap at crossing
pipe(ax1, 14.5, 3.8,       14.5, 6.3 - BR,  C_BLUE)    # riser below brown drain
pipe(ax1, 14.5, 6.3 + BR,  14.5, 8.0,        C_BLUE)    # riser above brown drain
valve(ax1, 14.5, 4.4, color=C_BLUE)                      # BV-05 spray bar shutoff
ax1.text(14.58, 4.38, "BV-05", ha="left", fontsize=6, color=C_BLUE)
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
    (C_BLACK, "-.", "Dash-dot — Heavy contamination bypass"),
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
    ("ACC",       "Pressure accumulator"),
]
for i, (sym, desc) in enumerate(syms):
    ax1.text(SYM_X + 0.15, ly - 0.10 - i * 0.25,
             f"{sym} — {desc}", va="center", fontsize=6.2, color=C_TEXT, zorder=7)

plt.tight_layout(pad=0.3)
os.makedirs(SVG_DIR, exist_ok=True)
fig1.text(0.99, 0.005, "© 2026 Alvin Richards — GNU AGPLv3",
          ha="right", va="bottom", fontsize=6.0, color="#888888", style="italic")
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
# Near column (Yd=100–1116mm): Blue #1 on top, Brown on bottom
NEAR_IBC_DY = BLUE_IBC_Y * SY
ibc_plan(ax2, IBC_COL_DX, NEAR_IBC_DY, "#BBDEFB", C_BLUE_IBC,
         "IBC-1 BLUE / IBC-3 BROWN", "Top: 600L clean\nBottom: 600L recycle")
# Far column (Yd=1141–2157mm): Blue #2 on top, Waste on bottom
FAR_IBC_DY = IBC_FAR_Y * SY
ibc_plan(ax2, IBC_COL_DX, FAR_IBC_DY, "#D5D5D0", C_WASTE_IBC,
         "IBC-2 BLUE / IBC-4 WASTE", "Top: 600L clean\nBottom: 600L waste")

# Filter skid (600×400mm → 0.6×0.4 → scaled = 0.96×0.64)
FS_X, FS_Y, FS_W, FS_D = 2.3, 0.2, 2.5, 0.9
ax2.add_patch(plt.Rectangle((FS_X, FS_Y), FS_W, FS_D, fc=C_FILT, ec="#F57F17",
                             lw=2, zorder=2))
ax2.text(FS_X + FS_W/2, FS_Y + FS_D/2 + 0.1, "FILTER SKID",
         ha="center", fontsize=7, fontweight="bold", color="#E65100", zorder=3)
ax2.text(FS_X + FS_W/2, FS_Y + FS_D/2 - 0.15, "F1 → F2 → F3 (pH)",
         ha="center", fontsize=6.5, color="#E65100", zorder=3)

# Pump P1 (blue) — wall-mounted, left side
pump(ax2, 0.55, 0.6, color=C_PUMP, r=0.2)
ax2.text(0.55, 0.25, "P-01\nBLUE SUPPLY", ha="center", fontsize=6, color=C_PUMP)

# Pump P2 (brown) — near filter skid
pump(ax2, 2.05, 0.6, color=C_PUMP, r=0.2)
ax2.text(2.05, 0.25, "P-02\nBROWN RECYCLE", ha="center", fontsize=6, color=C_PUMP)

# ACC accumulator
box(ax2, 1.3, 0.6, 0.55, 0.4, fc="#E3F2FD", ec=C_BLUE, lw=1.5)
ax2.text(1.45, 0.6, "ACC-01", ha="center", va="center", fontsize=6.5, color=C_BLUE)

# Processing tray (304 SS, two panels, 50mm rim)
TRAY_X0 = (FP_X_L + 20) * SX   # left edge in drawing units
TRAY_X1 = (FP_X_R - 20) * SX   # right edge in drawing units

# Spray bar along top wall — aligned with processing tray
pipe(ax2, TRAY_X0, 4.75, TRAY_X1, 4.75, C_BLUE, lw=3)
ax2.text((TRAY_X0 + TRAY_X1) / 2, 4.88,
         "FLOOD/SPRAY BAR (3/4\" HDPE, 1\" NPT inlets every 600mm)",
         ha="center", fontsize=7, color=C_BLUE)
TRAY_Y0 = 60 * SY              # starts 60mm from pinhole wall
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

# Tray drain (gravity drain to 3W-DV-02)
drain_x = (TRAY_X0 + TRAY_X1) / 2
drain_y = TRAY_Y0 + 0.3
fd = plt.Circle((drain_x, drain_y), 0.18, fc="white", ec="#388E3C", lw=1.8, zorder=4)
ax2.add_patch(fd)
ax2.plot([drain_x - 0.18, drain_x + 0.18], [drain_y, drain_y],
         color="#388E3C", lw=1.2, zorder=5)
ax2.plot([drain_x, drain_x], [drain_y - 0.18, drain_y + 0.18],
         color="#388E3C", lw=1.2, zorder=5)
ax2.text(drain_x + 0.45, drain_y - 0.1, "TRAY DRAIN\n3W-DV-02", ha="center",
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
fig2.text(0.99, 0.005, "© 2026 Alvin Richards — GNU AGPLv3",
          ha="right", va="bottom", fontsize=6.0, color="#888888", style="italic")
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
ax3.set_ylim(-0.5, OY + TRAY_DRAW_H + 1.8)
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
# Low point: near rim (Yd=0), X-center
# High corners: far rim (Yd=2200), X extremes
ax3.text(s3x(PROC_TRAY_W/2) + 1.25, OY - 0.55, "LOW EDGE (Yd = 80mm)",
         ha="center", fontsize=7.5, fontweight="bold", color="#D32F2F")
ax3.text(s3x(PROC_TRAY_W/2), OY + TRAY_DRAW_H + 0.35,
         "HIGH EDGE (Yd = 2,280mm)",
         ha="center", fontsize=7.5, fontweight="bold", color="#1565C0")

ax3.text(OX - 0.15, OY + TRAY_DRAW_H / 2, "HIGH\nCORNER",
         ha="right", va="center", fontsize=6.5, color="#1565C0", fontweight="bold")
ax3.text(OX + TRAY_DRAW_W + 0.15, OY + TRAY_DRAW_H / 2, "HIGH\nCORNER",
         ha="left", va="center", fontsize=6.5, color="#1565C0", fontweight="bold")

# ── Slope arrows (flow direction) ───────────────────────────────────────────
# Water flows: (1) toward Yd=0 (near wall) and (2) toward X-center
# Draw a grid of arrows showing combined flow direction

ARROW_COLOR = "#1976D2"
ARROW_ALPHA = 0.7

# Grid of flow arrows across the tray interior
n_cols = 9
n_rows = 5
for i in range(n_cols):
    for j in range(n_rows):
        # Position in tray-local mm
        ax_mm = PROC_TRAY_W * (i + 0.5) / n_cols
        ay_mm = PROC_TRAY_D * (j + 0.5) / n_rows

        # Flow direction: toward (PROC_TRAY_W/2, 0) — the drain point
        # X component: toward center
        dx_mm = (PROC_TRAY_W / 2 - ax_mm)
        # Yd component: toward near wall (Yd=0)
        dy_mm = -ay_mm

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
# Drain is at tray-local X = PROC_TRAY_DRAIN_X - PROC_TRAY_X_L, Yd = 0 (near rim)
drain_local_x = PROC_TRAY_DRAIN_X - PROC_TRAY_X_L
drain_local_yd = PROC_TRAY_DRAIN_YD - PROC_TRAY_YD_NEAR

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
ax3.text(drain_dx + 1.55, drain_dy + 0.2, "1\" NPT DRAIN (TO 3W-DV-02)",
         ha="center", va="top", fontsize=7.5, fontweight="bold",
         color="#D32F2F", zorder=8)
ax3.text(drain_dx - 0.9, drain_dy + 0.1,
         f"X={PROC_TRAY_DRAIN_X:,}  Yd={PROC_TRAY_DRAIN_YD}",
         ha="center", va="bottom", fontsize=6.5, color="#D32F2F", zorder=8)

# ── Slope annotations ────────────────────────────────────────────────────────
# Yd-axis slope: 1:200 over 2,200mm = 11mm fall
yd_fall = PROC_TRAY_D * PROC_TRAY_PITCH / PROC_TRAY_D  # = PROC_TRAY_PITCH mm
x_half = PROC_TRAY_W / 2
x_fall = x_half / 200  # fall from each X extreme to center at 1:200

# Right-side slope annotation
ann_x = s3x(PROC_TRAY_W * 0.82)
ann_y = s3y(PROC_TRAY_D * 0.5)
ax3.text(ann_x, ann_y,
         f"X-SLOPE: 1:200\n({x_fall:.1f}mm fall\nover {x_half:,.0f}mm)",
         ha="center", va="center", fontsize=7, color="#0D47A1",
         bbox=dict(fc="white", ec="#0D47A1", lw=0.8, pad=3, alpha=0.9),
         zorder=8)

# Left-side slope annotation
ann_x2 = s3x(PROC_TRAY_W * 0.18)
ax3.text(ann_x2, ann_y,
         f"X-SLOPE: 1:200\n({x_fall:.1f}mm fall\nover {x_half:,.0f}mm)",
         ha="center", va="center", fontsize=7, color="#0D47A1",
         bbox=dict(fc="white", ec="#0D47A1", lw=0.8, pad=3, alpha=0.9),
         zorder=8)

# Yd-axis slope annotation (center-top area)
ann_y2 = s3y(PROC_TRAY_D * 0.78)
ax3.text(s3x(PROC_TRAY_W * 0.5), ann_y2,
         f"Yd-SLOPE: 1:200\n({PROC_TRAY_PITCH}mm fall over {PROC_TRAY_D:,}mm)",
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
         "1\" HDPE → 3W-DV-02 (ALONG PINHOLE WALL)",
         ha="center", fontsize=6.5, color=C_BROWN, style="italic", zorder=8)

# ── Notes ────────────────────────────────────────────────────────────────────
notes = [
    f"1. Dual-axis pitch 1:200 — water converges on drain at X={PROC_TRAY_DRAIN_X:,}, Yd={PROC_TRAY_DRAIN_YD}.",
    f"2. Maximum fall: {PROC_TRAY_PITCH}mm (Yd axis) + {x_fall:.1f}mm (X axis from far corner to drain).",
    f"3. Drain: 1\" NPT bulkhead fitting through tray floor → 3W-DV-02 diverter (Brown / Waste).",
    f"4. Tray: 304 stainless steel, {PROC_TRAY_RIM}mm rim, permanently installed.",
    f"5. Spanning beam walkway (legs at ends only) — no intermediate legs on tray floor near drain.",
]
for i, n in enumerate(notes):
    fig3.text(0.04, 0.08 - i * 0.018, n, fontsize=7, color=C_TEXT,
              fontfamily="monospace", va="top")

# ── Copyright ────────────────────────────────────────────────────────────────
fig3.text(0.99, 0.005, "© 2026 Alvin Richards — GNU AGPLv3",
          ha="right", va="bottom", fontsize=6.0, color="#888888", style="italic")
fig3.savefig("diagrams/water-system-sheet3.png", dpi=150, bbox_inches="tight",
             facecolor=fig3.get_facecolor())
fig3.savefig(svg_path("diagrams/water-system-sheet3.png"), bbox_inches="tight",
             facecolor=fig3.get_facecolor())
plt.close(fig3)
print("Sheet 3 written → diagrams/water-system-sheet3.png")
print("Done.")
