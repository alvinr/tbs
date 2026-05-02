#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_water_system.py
Generates two engineering diagrams for the cyanotype processing water system:
  Sheet 1 — System flow schematic (three-system P&ID overview)
  Sheet 2 — Tank & filter skid layout plan (dimensioned arrangement)

Output:
  water-system-sheet1.png  (1800 x 1200 px, 150 dpi)
  water-system-sheet2.png  (1800 x 1200 px, 150 dpi)
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
    IBC_COL_X, ZONE_L_END, ZONE_R_START,
    DRUM_EQ_D, DRUM_EQ_R, DRUM_EQ_H,
    DRUM_LZ_CX, DRUM_LZ_YD, DRUM_LZ_YD_LO, DRUM_LZ_YD_HI,
    DRUM_FZ_CX, DRUM_FZ_YD, DRUM_FZ_YD_LO, DRUM_FZ_YD_HI,
)

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

def drum(ax, x, y, r=0.07, fc="white", ec=C_FRAME, label="", lw=1.4, zorder=2):
    """Draw a 55-gal drum (circle)."""
    circ = plt.Circle((x, y), r, fc=fc, ec=ec, lw=lw, zorder=zorder)
    ax.add_patch(circ)
    if label:
        ax.text(x, y, label, ha="center", va="center",
                fontsize=6.5, fontweight="bold", color=C_TEXT, zorder=zorder + 1,
                multialignment="center")

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

def pipe_bridge(ax, x, y, direction='h', r=0.14, color=C_FRAME, lw=LW_PIPE, zorder=11):
    """Draw a pipe-crossing bridge hump on the 'over' pipe.
    direction: 'h' = bridging pipe is horizontal (arc humps upward)
               'v' = bridging pipe is vertical (arc humps rightward)
    A white-filled semicircle masks the underlying pipe, then the arc is drawn.
    """
    if direction == 'h':
        theta = np.linspace(0, np.pi, 40)
        bx = x + r * np.cos(theta)
        by = y + r * np.sin(theta)
    else:
        theta = np.linspace(-np.pi / 2, np.pi / 2, 40)
        bx = x + r * np.cos(theta)
        by = y + r * np.sin(theta)
    ax.fill(bx, by, color='white', zorder=zorder - 1)
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
ax1.add_patch(plt.Rectangle((0, 0), 18, 1.1, fc="white", ec=C_FRAME, lw=1.5))
ax1.text(9, 0.65, "GIANT PINHOLE CAMERA — CYANOTYPE PROCESSING WATER SYSTEM",
         ha="center", va="center", fontsize=13, fontweight="bold", color=C_TITLE)
ax1.text(9, 0.25, "SHEET 1 OF 2 — SYSTEM FLOW SCHEMATIC (P&ID)   |   "
         "SCALE: NOT TO SCALE   |   REV 1.0",
         ha="center", va="center", fontsize=8.5, color="#444444")

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
D1_X, D2_X = 11.07, 12.23  # drum X centers — 1/3 and 2/3 across Black zone (9.9–13.4)
D_Y  = 7.5                  # drum centre Y (raised)
DR   = 0.42                 # drum radius
BR   = 0.14                 # pipe-crossing bridge hump radius
X_J  = D1_X + 0.5          # = 11.57, Y-junction X: floor drain + bypass merge before D1
Y_J  = 5.62                 # Y level of Y-junction (matches heavy contam bypass exit)

# ── BLUE SYSTEM ───────────────────────────────────────────────────────────────
# IBC1 Clean water A
tank(ax1, 1.5, 8.2, 1.4, 1.4, fc="#BBDEFB", ec=C_BLUE, lw=2,
     label="IBC-1", sublabel="159 gal (600L)\nCLEAN A")
# IBC2 Clean water B
tank(ax1, 3.3, 8.2, 1.4, 1.4, fc="#BBDEFB", ec=C_BLUE, lw=2,
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
pump(ax1, 2.4, 6.3, color=C_BLUE)
ax1.text(2.75, 6.3, "P-01\n12VDC\n3.5 GPM", ha="left", fontsize=6, color=C_BLUE)

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
# Run east to spray bar riser tap-off — humps over blue return (X=9.7), D1 vertical (D1_X), floor drain riser (X_J)
pipe(ax1, 2.4, 3.8, 14.5, 3.8, C_BLUE)
pipe_bridge(ax1, 9.7,   3.8, color=C_BLUE, lw=LW_PIPE)
pipe_bridge(ax1, D1_X,  3.8, color=C_BLUE, lw=LW_PIPE)
pipe_bridge(ax1, X_J,   3.8, color=C_BLUE, lw=LW_PIPE)
ax1.text(8.5, 3.6, "1\" HDPE — BLUE (SUPPLY)", ha="center",
         fontsize=7, color=C_BLUE)

# Refill inlet (top of IBC-1)
pipe(ax1, 1.5, 8.9, 1.5, 9.6, C_BLUE, style="--")
ax1.text(1.5, 9.75, "FILL\nINLET", ha="center", fontsize=6,
         color=C_BLUE, style="italic")

# Water level sensor labels
ax1.text(4.8, 8.2, "LOW-LEVEL\nFLOAT SW.", ha="center",
         fontsize=5.5, color=C_BLUE, alpha=0.8)
ax1.plot([4.5, 3.95], [8.2, 8.2], color=C_BLUE, lw=0.8, ls=":")

# ── BROWN SYSTEM ──────────────────────────────────────────────────────────────
# IBC3 — used water buffer
tank(ax1, 6.4, 8.2, 1.4, 1.4, fc="#D7CCC8", ec=C_BROWN, lw=2,
     label="IBC-3", sublabel="159 gal (600L)\nUSED BUFFER")

# Inlet from processing floor drain
pipe(ax1, 6.4, 7.48, 6.4, 7.0, C_BROWN)
valve(ax1, 6.4, 7.0, color=C_BROWN)
ax1.text(6.6, 6.97, "BV-03", ha="center", fontsize=6, color=C_BROWN)
pipe(ax1, 6.4, 6.8, 6.4, 6.3, C_BROWN)
# Arrow from processing area — humps over blue return (X=9.7) and black vertical (D1_X)
pipe(ax1, 6.4, 6.3, 15.65, 6.3, C_BROWN, style="--")
pipe_bridge(ax1, 9.7,   6.3, color=C_BROWN, lw=LW_PIPE)
pipe_bridge(ax1, D1_X,  6.3, color=C_BROWN, lw=LW_PIPE)
pipe_bridge(ax1, 14.5,  6.3, color=C_BROWN, lw=LW_PIPE)   # brown over spray bar riser
arrow_pipe(ax1, 6.6, 6.3, 6.4, 6.3, color=C_BROWN)
ax1.text(10.8, 6.1, "1\" HDPE — BROWN (DRAIN FROM FLOOR)", ha="center",
         fontsize=7, color=C_BROWN)

# Brown pump P2 — outlet from bottom of IBC-3
pipe(ax1, 6.4, 7.48, 6.4, 5.6, C_BROWN)
arrow_pipe(ax1, 6.4, 7.0, 6.4, 6.0, color=C_BROWN)       # downward from IBC-3
pump(ax1, 6.4, 5.4, color=C_BROWN)
ax1.text(6.75, 5.4, "P-02\n12VDC\n3.5 GPM", ha="left", fontsize=6, color=C_BROWN)

pipe(ax1, 6.4, 5.2, 6.4, 4.8, C_BROWN)

# ── FILTER SKID ───────────────────────────────────────────────────────────────
ax1.add_patch(plt.Rectangle((5.2, 3.0), 3.8, 2.0, fc=C_FILT, ec="#F57F17",
                             lw=1.5, alpha=0.8, zorder=1))
ax1.text(7.1, 4.88, "FILTER SKID", ha="center", fontsize=7.5,
         fontweight="bold", color="#E65100")

# Filter 1 — 50 micron sediment
filter_sym(ax1, 6.0, 3.9, label="F1")
ax1.text(6.0, 3.35, "50μ\nSEDIMENT", ha="center", fontsize=6, color="#E65100")
pipe(ax1, 6.4, 4.6, 6.0, 4.6, C_BROWN)
arrow_pipe(ax1, 6.3, 4.6, 6.1, 4.6, color=C_BROWN)       # leftward to F1
pipe(ax1, 6.0, 4.6, 6.0, 4.0, C_BROWN)
pipe(ax1, 6.0, 3.8, 6.0, 3.55, C_BROWN)

# Filter 2 — 5 micron sediment
filter_sym(ax1, 7.1, 3.9, label="F2")
ax1.text(7.1, 3.35, "5μ\nSEDIMENT", ha="center", fontsize=6, color="#E65100")
pipe(ax1, 6.0, 3.55, 6.0, 3.25, C_BROWN)
pipe(ax1, 6.0, 3.25, 7.1, 3.25, C_BROWN)
arrow_pipe(ax1, 6.4, 3.25, 6.8, 3.25, color=C_BROWN)     # rightward F1→F2
pipe(ax1, 7.1, 3.25, 7.1, 3.55, C_BROWN)
pipe(ax1, 7.1, 3.8, 7.1, 4.6, C_BROWN)
arrow_pipe(ax1, 7.1, 4.0, 7.1, 4.4, color=C_BROWN)       # upward F2 out

# Filter 3 — GAC carbon
filter_sym(ax1, 8.2, 3.9, label="F3")
ax1.text(8.2, 3.35, "GAC\nCARBON", ha="center", fontsize=6, color="#E65100")
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
pipe(ax1, 9.7, 2.5, D1_X, 2.5, C_BLACK)
arrow_pipe(ax1, 10.3, 2.5, D1_X, 2.5, color=C_BLACK)      # rightward to D1

# ── BLACK SYSTEM ──────────────────────────────────────────────────────────────
drum(ax1, D1_X, D_Y, r=DR, fc=C_BLACK_L, ec=C_BLACK, lw=2,
     label="DRUM-1\n55 GAL\nWASTE")
drum(ax1, D2_X, D_Y, r=DR, fc=C_BLACK_L, ec=C_BLACK, lw=2,
     label="DRUM-2\n55 GAL\nWASTE")

# Heavy contamination bypass — left side of processing floor, 1/5th up (Y=5.62)
pipe(ax1, 14.1, Y_J, X_J, Y_J, C_BLACK, style="-.")
valve(ax1, 13.3, 5.62, color=C_BLACK)                      # BV-04
ax1.text(13.3, 5.80, "BV-04", ha="center", fontsize=6, color=C_BLACK)
arrow_pipe(ax1, 13.8, 5.62, 12.0, 5.62, color=C_BLACK)    # leftward bypass flow
ax1.text(12.6, 5.44, "HEAVY CONTAM. BYPASS", ha="center",
         fontsize=6, color=C_BLACK, style="italic")

# Y-junction: floor drain riser meets heavy contam bypass at (X_J, Y_J)
# Riser climbs at X_J, bridges over blue supply at Y=3.8
pipe(ax1, X_J, 2.6,       X_J, 3.8 - BR,  C_BLACK)  # floor drain riser (below blue)
pipe(ax1, X_J, 3.8 + BR,  X_J, Y_J,        C_BLACK)  # riser (above blue → junction)
# Combined flow exits junction left into D1 vertical
pipe(ax1, X_J, Y_J,  D1_X, Y_J, C_BLACK)             # junction → D1 vertical entry
# D1 vertical — full height: filter skid feeds from Y=2.5; Y-junction joins at Y_J; drum above
# Bridges at Y=3.8 (blue supply over) and Y=6.3 (brown drain over)
pipe(ax1, D1_X, 2.5,       D1_X, 3.8 - BR,  C_BLACK)         # filter skid inlet to blue crossing
pipe(ax1, D1_X, 3.8 + BR,  D1_X, 6.3 - BR,  C_BLACK)         # blue crossing to brown crossing
pipe(ax1, D1_X, 6.3 + BR,  D1_X, D_Y - DR,  C_BLACK)         # brown crossing to drum
arrow_pipe(ax1, D1_X, 3.2, D1_X, 4.5,       color=C_BLACK)   # upward flow (lower)
arrow_pipe(ax1, D1_X, Y_J + 0.1, D1_X, D_Y - DR - 0.1, color=C_BLACK)  # upward flow (upper)

# Overflow from D1 top → D2 top
OV_Y = D_Y + DR + 0.25
pipe(ax1, D1_X, D_Y + DR, D1_X, OV_Y, C_BLACK, style="--")
pipe(ax1, D1_X, OV_Y, D2_X, OV_Y, C_BLACK, style="--")
arrow_pipe(ax1, D1_X + 0.3, OV_Y, D2_X - 0.1, OV_Y, color=C_BLACK)
pipe(ax1, D2_X, OV_Y, D2_X, D_Y + DR, C_BLACK, style="--")
ax1.text((D1_X + D2_X) / 2, OV_Y + 0.14,
         "OVERFLOW →\nDRUM-2", ha="center", fontsize=6, color=C_BLACK)

# Disposal from D2 — exits top of black system box
DISP_Y = D_Y - DR - 0.55   # = 6.53, above brown drain at 6.3 so no bridge needed
DISP_X = 13.3               # near right edge of black zone box (box right = 13.4)
pipe(ax1, D2_X, D_Y - DR, D2_X, DISP_Y, C_BLACK)     # D2 bottom → down
pipe(ax1, D2_X, DISP_Y, DISP_X, DISP_Y, C_BLACK)     # right to near box edge
pipe(ax1, DISP_X, DISP_Y, DISP_X, 10.75, C_BLACK)    # up and out top of box
ax1.annotate("", xy=(DISP_X, 11.05), xytext=(DISP_X, 10.8),
             arrowprops=dict(arrowstyle="-|>", color=C_BLACK, lw=2,
                             mutation_scale=14), zorder=4)
ax1.text(DISP_X, 11.2, "TO APPROVED\nDISPOSAL SITE", ha="center",
         fontsize=6.5, color=C_BLACK, fontweight="bold", va="bottom")

# ── PROCESSING AREA ───────────────────────────────────────────────────────────
ax1.add_patch(plt.Rectangle((13.7, 3.5), 3.8, 5.5, fc="#C8E6C9", ec="#388E3C",
                             lw=1.5, zorder=2))
ax1.text(15.6, 8.8, "PRINT PROCESSING FLOOR", ha="center", fontsize=7.5,
         fontweight="bold", color="#2E7D32")
ax1.text(15.6, 8.5, "(140 sq ft containment zone)", ha="center",
         fontsize=6.5, color="#388E3C")

# Print on floor representation
ax1.add_patch(plt.Rectangle((14.1, 5.0), 3.0, 3.1, fc="white", ec="#66BB6A",
                             lw=1.2, ls="--", alpha=0.8, zorder=3))
ax1.text(15.6, 6.55, "PRINT\n(5893 × 2388 mm)", ha="center", va="center",
         fontsize=7, color="#388E3C", style="italic", zorder=4)


# Floor drain
circle_drain = plt.Circle((15.6, 4.15), 0.15, fc="white", ec="#388E3C", lw=1.5,
                            zorder=4)
ax1.add_patch(circle_drain)
ax1.plot([15.45, 15.75], [4.15, 4.15], color="#388E3C", lw=1.2, zorder=5)
ax1.plot([15.6, 15.6], [4.0, 4.3], color="#388E3C", lw=1.2, zorder=5)
ax1.text(15.6, 4.4, "FLOOR DRAIN\n+ DIVERTER", ha="center",
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
ax1.text(13.5, 2.42, "TO DRUM (HEAVY CONTAM.)", ha="center", fontsize=6,
         color=C_BLACK, style="italic")

# Spray bar riser — blue supply tap-off at Y=3.8 up to spray bar at Y=8.0
# Brown drain (Y=6.3) bridges over; riser is split with gap at crossing
pipe(ax1, 14.5, 3.8,       14.5, 6.3 - BR,  C_BLUE)    # riser below brown drain
pipe(ax1, 14.5, 6.3 + BR,  14.5, 8.0,        C_BLUE)    # riser above brown drain
valve(ax1, 14.5, 4.4, color=C_BLUE)                      # BV-05 spray bar shutoff
ax1.text(14.72, 4.4, "BV-05", ha="left", fontsize=6, color=C_BLUE)
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
fig1.text(0.99, 0.005, "© 2026 Alvin Richards — GNU AGPLv3",
          ha="right", va="bottom", fontsize=6.0, color="#888888", style="italic")
fig1.savefig("diagrams/water-system-sheet1.png", dpi=150, bbox_inches="tight",
             facecolor=fig1.get_facecolor())
fig1.savefig("diagrams/water-system-sheet1.svg", bbox_inches="tight", facecolor=fig1.get_facecolor())
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
fig2.text(0.5, 0.97, "TBS-001 — WATER SYSTEM EQUIPMENT LAYOUT",
          ha="center", fontsize=13, fontweight="bold", color=C_TITLE)
fig2.text(0.5, 0.94, "SHEET 2 OF 2 — PLAN VIEW (INSIDE CONTAINER)  |  "
          "SCALE: 1:25 (APPROX)  |  ALL DIMS IN MILLIMETRES",
          ha="center", fontsize=9, color="#444444")

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
ax2.text(6.0, -0.35, "CONTAINER INTERIOR — PLAN VIEW  (6,096 × 2,438 mm interior)",
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

# Right end zone: Blue IBC stack x2 — Y-stacked FRONT (Yd=100–1116mm)
BLUE_IBC_DY = 100 * SY   # ≈ 0.21
ibc_plan(ax2, IBC_COL_DX, BLUE_IBC_DY, "#BBDEFB", C_BLUE,
         "IBC-1/2 BLUE x2", "2x159 gal (2x600L)\nYd=100–1116mm (front)")
# Brown IBC x1 — Y-stacked REAR (Yd=1141–2157mm)
BROWN_IBC_DY = 1141 * SY  # ≈ 2.42
ibc_plan(ax2, IBC_COL_DX, BROWN_IBC_DY, "#D7CCC8", C_BROWN,
         "IBC-3 BROWN", "159 gal (600L)\nYd=1141–2157mm (rear)")

# Filter skid (600×400mm → 0.6×0.4 → scaled = 0.96×0.64)
FS_X, FS_Y, FS_W, FS_D = 2.3, 0.2, 2.5, 0.9
ax2.add_patch(plt.Rectangle((FS_X, FS_Y), FS_W, FS_D, fc=C_FILT, ec="#F57F17",
                             lw=2, zorder=2))
ax2.text(FS_X + FS_W/2, FS_Y + FS_D/2 + 0.1, "FILTER SKID",
         ha="center", fontsize=7, fontweight="bold", color="#E65100", zorder=3)
ax2.text(FS_X + FS_W/2, FS_Y + FS_D/2 - 0.15, "F1 → F2 → F3 (pH)",
         ha="center", fontsize=6.5, color="#E65100", zorder=3)

# Pump P1 (blue) — wall-mounted, left side
pump(ax2, 0.55, 0.6, color=C_BLUE, r=0.2)
ax2.text(0.55, 0.25, "P-01\nBLUE SUPPLY", ha="center", fontsize=6, color=C_BLUE)

# Pump P2 (brown) — near filter skid
pump(ax2, 2.05, 0.6, color=C_BROWN, r=0.2)
ax2.text(2.05, 0.25, "P-02\nBROWN RECYCLE", ha="center", fontsize=6, color=C_BROWN)

# ACC accumulator
box(ax2, 1.3, 0.6, 0.55, 0.4, fc="#E3F2FD", ec=C_BLUE, lw=1.5)
ax2.text(1.45, 0.6, "ACC-01", ha="center", va="center", fontsize=6.5, color=C_BLUE)

# 55-gal drums D-1, D-2 — LEFT end zone, one per Yd corner (rev 4: unstacked)
DRUM_R_DU = DRUM_EQ_R * SY    # radius in drawing units
for drum_cx, drum_cy, label in [
    (DRUM_LZ_CX, DRUM_LZ_YD, "D-1\nnear"),   # near corner (pinhole wall side)
    (DRUM_FZ_CX, DRUM_FZ_YD, "D-2\nfar"),    # far corner (far wall side)
]:
    dx = drum_cx * SX
    dy = drum_cy * SY
    ax2.add_patch(plt.Circle((dx, dy), DRUM_R_DU,
                             fc=C_BLACK_L, ec=C_BLACK, lw=2, zorder=2))
    ax2.text(dx, dy, label, ha="center", va="center",
             fontsize=5.5, fontweight="bold", color=C_BLACK, zorder=3,
             multialignment="center")

# Spray bar along top wall
pipe(ax2, 5.0, 4.75, 11.5, 4.75, C_BLUE, lw=3)
ax2.text(8.25, 4.88, "FLOOD/SPRAY BAR (3/4\" HDPE, 1\" NPT inlets every 600mm)",
         ha="center", fontsize=7, color=C_BLUE)

# Processing area berm
ax2.add_patch(plt.Rectangle((4.8, 0.3), 6.9, 4.3, fc=C_PROC, ec="#388E3C",
                             lw=2, ls="--", zorder=1, alpha=0.5))
ax2.text(8.25, 4.45, "PROCESSING CONTAINMENT ZONE (~22 sq m)",
         ha="center", fontsize=7, color="#2E7D32")

# Floor drain
fd = plt.Circle((8.25, 0.5), 0.18, fc="white", ec="#388E3C", lw=1.8, zorder=4)
ax2.add_patch(fd)
ax2.plot([8.07, 8.43], [0.5, 0.5], color="#388E3C", lw=1.2, zorder=5)
ax2.plot([8.25, 8.25], [0.32, 0.68], color="#388E3C", lw=1.2, zorder=5)
ax2.text(8.25, 0.18, "FLOOR DRAIN\n3W-DV-02", ha="center",
         fontsize=6, color="#388E3C")

# Left end zone shading (X=0–625mm = drum zone)
ZONE_L_DX = ZONE_L_END * SX   # = 625mm → ≈ 1.27
ax2.add_patch(plt.Rectangle((0, 0), ZONE_L_DX, CH,
              fc="#FFF3E0", ec="none", alpha=0.45, zorder=0))
ax2.plot([ZONE_L_DX, ZONE_L_DX], [0, CH], color="#805000", lw=1.5, ls="--",
         zorder=6)
ax2.text(ZONE_L_DX - 0.05, -CH/6, #CH - 0.15,
         f"LEFT END ZONE\nX=0–{ZONE_L_END:,}mm\n(drum zone)",
         ha="right", va="top", fontsize=6.5, color="#805000", fontweight="bold")

# Right end zone shading (X=4649–5893mm in drawing)
ZONE_R_DX = ZONE_R_START * SX   # ≈ 9.45
ax2.add_patch(plt.Rectangle((ZONE_R_DX, 0), CW - ZONE_R_DX, CH,
              fc="#E8F0FF", ec="none", alpha=0.45, zorder=0))
ax2.plot([ZONE_R_DX, ZONE_R_DX], [0, CH], color="#004080", lw=1.5, ls="--",
         zorder=6)
ax2.text(ZONE_R_DX + 0.05, -CH/6,
         f"RIGHT END ZONE\nX={ZONE_R_START:,}–5,893mm\n(shadow-free, IBCs only)",
         ha="left", va="top", fontsize=6.5, color="#004080", fontweight="bold")

# Pinhole wall — BOTTOM of plan view (Yd=0 = near side, pinhole aperture wall)
ax2.add_patch(plt.Rectangle((0.0, -0.15), CW, 0.15, fc="#BDBDBD", ec=C_FRAME,
                             lw=2, zorder=5))
ax2.text(CW / 2, -0.08, "PINHOLE WALL (FRONT — Yd = 0)",
         ha="center", va="center", fontsize=6, color="#333", zorder=6)

# Dimensions
def dim_h(ax, x1, x2, y, label, color=C_DIM, offset=0.25):
    yy = y - offset
    ax.annotate("", xy=(x2, yy), xytext=(x1, yy),
                arrowprops=dict(arrowstyle="<->", color=color, lw=1.0,
                                mutation_scale=8))
    ax.text((x1+x2)/2, yy - 0.12, label, ha="center", fontsize=6.5, color=color)

def dim_v(ax, x, y1, y2, label, color=C_DIM, offset=0.3):
    xx = x - offset
    ax.annotate("", xy=(xx, y2), xytext=(xx, y1),
                arrowprops=dict(arrowstyle="<->", color=color, lw=1.0,
                                mutation_scale=8))
    ax.text(xx - 0.1, (y1+y2)/2, label, ha="right", va="center",
            fontsize=6.5, color=color, rotation=90)

dim_h(ax2, 0, CW, -0.35, "5,893 mm (CONTAINER INTERIOR)")
dim_v(ax2, -0.2, 0, CH, "2,362 mm")
dim_h(ax2, IBC_COL_DX, IBC_COL_DX + IBC_W, 5.2, "IBC col: 1,219 mm")
dim_h(ax2, 0, ZONE_L_DX, 5.5, f"LEFT END ZONE: {ZONE_L_END} mm", color="#805000")
dim_h(ax2, ZONE_R_DX, CW, 5.5, f"RIGHT END ZONE: {5893 - ZONE_R_START} mm", color="#004080")

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
fig2.savefig("diagrams/water-system-sheet2.svg", bbox_inches="tight", facecolor=fig2.get_facecolor())
plt.close(fig2)
print("Sheet 2 written → diagrams/water-system-sheet2.png")
print("Done.")
