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
from matplotlib.patches import FancyBboxPatch
from matplotlib.gridspec import GridSpec
from tbs_constants import C_LEN, C_HGT, IBC_COL_X, IBC_W, IBC_D, ZONE_L_END, ZONE_R_START, FP_X_L, FP_X_R, BLUE_IBC_Y, IBC_FAR_Y, PUMP_X, PUMP_W, PUMP_H_LO, PUMP_D, EQPANEL_X, EQPANEL_W, EQPANEL_T, CORRIDOR_YD_NEAR, PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_W, PROC_TRAY_D, PROC_TRAY_YD_NEAR, PROC_TRAY_RIM, PROC_TRAY_PITCH, PROC_TRAY_DRAIN_X, PROC_TRAY_DRAIN_YD, PROC_TRAY_SUMP_W, PROC_TRAY_SUMP_D, PROC_TRAY_SUMP_Z, PROC_TRAY_SHIM_H, PROC_TRAY_SHIM_W, WALKWAY_W, WALKWAY_NEAR_YD, WALKWAY_FAR_YD, C_BLUE_IBC, C_BROWN_IBC, C_WASTE_IBC, C_PUMP, DIAGRAMS_DIR
import os
from tbs_title_block import title_block
from tbs_drawing import (draw_dim_h, draw_dim_v, leader, draw_notes,
                         draw_pipe_path as _tbs_pipe_path,
                         draw_pipe_end as _tbs_pipe_end)
from tbs_constants import DIAGRAM_DPI

# ── Color palette ────────────────────────────────────────────────────────────
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

def diverter(ax, x, y, color=C_BLUE, zorder=5, size=0.075, branch="up", label="DV"):
    """Draw a 3-way diverter valve symbol — a ball-valve bowtie (two triangles
    tip-to-tip in a white circle) PLUS a third triangle pointing to the branch
    port, so it reads as a 3-port diverter rather than a 2-port ball valve.
    branch in {"up","down","left","right"} selects the branch-port direction.
    Drawn in the same style/scale as valve() (circle radius = size * 1.6)."""
    r = size * 1.6
    circ = plt.Circle((x, y), r, fc="white", ec=color, lw=2.0, zorder=zorder)
    ax.add_patch(circ)
    # Bowtie — the two through-port triangles (left+right, tips meeting at center)
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
    # Third (branch) triangle — apex at center, base out at the branch port.
    bdir = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}[branch]
    bx, by = bdir
    px, py = -by, bx                    # perpendicular (base spread direction)
    base1 = (x + bx*size + px*size, y + by*size + py*size)
    base2 = (x + bx*size - px*size, y + by*size - py*size)
    tri3 = plt.Polygon([base1, base2, (x, y)],
                       fc=color, ec=color, alpha=0.85, zorder=zorder + 1)
    ax.add_patch(tri3)

def check_valve(ax, x, y, dx, dy, color=C_BROWN, zorder=6, size=0.085):
    """Check / non-return valve (anti-siphon): a triangle pointing DOWNSTREAM
    (the permitted flow direction) seated against a stop bar it cannot pass."""
    L = (dx**2 + dy**2) ** 0.5
    ux, uy = dx / L, dy / L            # downstream unit vector
    px, py = -uy, ux                   # perpendicular
    base1 = (x - ux*size + px*size, y - uy*size + py*size)
    base2 = (x - ux*size - px*size, y - uy*size - py*size)
    apex  = (x + ux*size, y + uy*size)
    ax.add_patch(plt.Polygon([base1, base2, apex], fc=color, ec=color, zorder=zorder))
    ax.plot([apex[0] + px*size, apex[0] - px*size],
            [apex[1] + py*size, apex[1] - py*size],
            color=color, lw=2.4, solid_capstyle="round", zorder=zorder + 1)

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


TOTAL_SHEETS = 4


def _save(fig, stem):
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    png = os.path.join(DIAGRAMS_DIR, f'{stem}.png')
    fig.savefig(png, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f'  {png} saved')


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — SYSTEM FLOW SCHEMATIC (P&ID overview)
# ═══════════════════════════════════════════════════════════════════════════════


def draw_sheet1():
    fig1, ax1 = plt.subplots(figsize=(18, 12))
    ax1.set_xlim(0, 18)
    ax1.set_ylim(0, 12)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_facecolor("#F5F5F0")
    fig1.patch.set_facecolor("#F5F5F0")

    # ── Title block ───────────────────────────────────────────────────────────────
    ax1.add_patch(plt.Rectangle((0, 0), 18, 12, fc="#F5F5F0", ec=C_FRAME, lw=2))
    title_block(ax1, f"SHEET 1 OF {TOTAL_SHEETS}",
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
    tank(ax1, 1.5, 7.5, 1.4, 1.4, fc="#BBDEFB", ec=C_BLUE_IBC, lw=2,
         label="IBC-1", sublabel="264 gal (1000L)\nCLEAN A (~900L)")
    # IBC2 Clean water B
    tank(ax1, 3.3, 7.5, 1.4, 1.4, fc="#BBDEFB", ec=C_BLUE_IBC, lw=2,
         label="IBC-2", sublabel="264 gal (1000L)\nCLEAN B (~900L)")

    # X1 fill tees to BOTH Blue totes; both supply the pump via BV-01 — the two
    # totes are connected in parallel (no cross-connect), matching the 3D.
    VR = 0.06 * 1.6  # standard valve circle radius = 0.096

    # Blue totes dropped so their tops align with IBC-4 (whole supply train shifts
    # down 0.7 with the tanks; BV-02 lands at the fixed supply run at Y=3.8).
    # IBC-1 outlet → BV-01
    pipe(ax1, 1.5, 6.78, 1.5, 6.3, C_BLUE)
    pipe(ax1, 1.5, 6.3, 2.4 - VR, 6.3, C_BLUE)
    # IBC-2 outlet → BV-01 (parallel with IBC-1)
    pipe(ax1, 3.3, 6.78, 3.3, 6.3, C_BLUE)
    pipe(ax1, 3.3, 6.3, 2.4 + VR, 6.3, C_BLUE)
    ax1.text(2.4, 6.85, 'IBC-1 & IBC-2 IN PARALLEL  (X1 fill tee · shared BV-01 supply\n· 1" tank-to-tank EQUALIZATION, level balance)',
             ha="center", fontsize=5.2, color=C_BLUE, style="italic")

    # Blue equalization — 1" cross-tie DIRECTLY between the two tank bodies, low on
    # the wall (IBC-1 right wall ↔ IBC-2 left wall) — level balance, not off the outlets.
    EQ_Y = 7.15
    pipe(ax1, 2.2, EQ_Y, 2.6, EQ_Y, C_BLUE)
    ax1.plot([2.2, 2.6], [EQ_Y, EQ_Y], "o", ms=3.5, color=C_BLUE, zorder=6)

    # Valve on outlet
    valve(ax1, 2.4, 6.3, color=C_BLUE)
    ax1.text(2.4, 6.44, "BV-01", ha="center", fontsize=6, color=C_BLUE)

    # Pump P1
    PR = 0.1125  # pump radius
    pipe(ax1, 2.4, 6.3 - VR, 2.4, 5.6 + PR, C_BLUE)
    arrow_pipe(ax1, 2.4, 6.15, 2.4, 5.8, color=C_BLUE)
    pump(ax1, 2.4, 5.6, color=C_PUMP)
    ax1.text(2.60, 5.5, "P-01\n12VDC\n3.5 GPM", ha="left", fontsize=6, color=C_PUMP)

    # Pressure accumulator
    pipe(ax1, 2.4, 5.6 - PR, 2.4, 4.9, C_BLUE)
    box(ax1, 2.4, 4.65, 0.8, 0.45, fc="#E3F2FD", ec=C_BLUE, lw=1.5)
    ax1.text(2.4, 4.65, "ACC-01\n1 GAL", ha="center", va="center",
             fontsize=6, color=C_BLUE)

    # ACC-01 → supply run (Y=3.8). No isolation valve here — the two downstream
    # branches carry their own (BV-04 at TAP-01, BV-05 at the spray bar).
    pipe(ax1, 2.4, 4.42, 2.4, 3.8, C_BLUE)
    arrow_pipe(ax1, 2.4, 4.25, 2.4, 3.95, color=C_BLUE)
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
    ax1.text(TAP_SCH_X + 0.30, 3.30, "BV-04", ha="center", fontsize=6, color=C_BLUE)
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

    # External fill (X1) via end-wall bulkhead — gravity feed. A SINGLE check valve
    # (CV-1) sits right after the port — the ONLY check valve in the system, since this is the
    # only flow path with no pump (the pumps' integral checks cover the return legs).  The fill
    # then tees to BOTH Blue totes near the top — a separate path from the dotted DV-01 return.
    ext_port(ax1, 1.5, 9.65, color=C_BLUE, label="X1")
    ax1.text(1.5, 9.95, "EXT. FILL\n2\" NPT\nGRAVITY", ha="center", fontsize=5.5,
             color=C_BLUE, style="italic")
    pipe(ax1, 1.5, 9.53, 1.5, 9.08, C_BLUE)                        # port → CV-1 → tee
    check_valve(ax1, 1.5, 9.38, 0, -1, color=C_BLUE)              # single anti-siphon on the fill
    ax1.text(1.18, 9.38, "CV-1", ha="right", va="center", fontsize=5.5, color=C_BLUE)
    pipe(ax1, 1.5, 9.08, 2.9, 9.08, C_BLUE)                        # fill header → IBC-2 branch
    ax1.plot([1.5], [9.08], "o", ms=3.5, color=C_BLUE, zorder=6)   # tee node
    pipe(ax1, 1.5, 9.08, 1.5, 8.2, C_BLUE)                         # drop into IBC-1
    arrow_pipe(ax1, 1.5, 8.42, 1.5, 8.30, color=C_BLUE)
    pipe(ax1, 2.9, 9.08, 2.9, 8.2, C_BLUE)                         # drop into IBC-2 (top-left)
    arrow_pipe(ax1, 2.9, 8.42, 2.9, 8.30, color=C_BLUE)
    ax1.text(2.2, 9.22, "X1 fill → IBC-1 & IBC-2", ha="center", fontsize=5.2,
             color=C_BLUE, style="italic")

    # Water level sensor labels
    ax1.text(4.75, 8.08, "IBC-2 LOW-LEVEL\nFLOAT SW.", ha="center",
             fontsize=5.5, color=C_BLUE, alpha=0.8)
    ax1.plot([4.45, 3.95], [7.92, 7.85], color=C_BLUE, lw=0.8, ls=":")

    # ── BROWN SYSTEM ──────────────────────────────────────────────────────────────
    # IBC3 — used water buffer
    tank(ax1, 6.4, 8.2, 1.4, 1.4, fc="#D7CCC8", ec=C_BROWN_IBC, lw=2,
         label="IBC-3", sublabel="264 gal (1000L)\nUSED BUFFER")

    # ── IBC-3 BUFFER — recycle return inlet (from DV-02 brown leg) ────────────────
    # Recycled drain water from DV-02 fills the buffer near the top; an anti-siphon
    # check valve + isolation BV-03 sit on the riser before the tank.
    RIN_X = 7.7                      # return riser, just right of IBC-3
    pipe(ax1, RIN_X, 6.3, 15.1, 6.3, C_BROWN, style="--")           # recycle return run
    pipe_bridge(ax1, 9.7, 6.3, color=C_BROWN, lw=LW_PIPE, bg=C_BROWN_L, style="--")
    pipe_bridge(ax1, W_X, 6.3, color=C_BROWN, lw=LW_PIPE, bg=C_BLACK_L, style="--")
    arrow_pipe(ax1, 10.6, 6.3, 10.3, 6.3, color=C_BROWN)            # return flow (toward buffer)
    ax1.text(11.4, 6.12, '1" BROWN — RECYCLE TO IBC-3 BUFFER (from DV-02)',
             ha="center", fontsize=6.5, color=C_BROWN)
    RIN_TOP = 8.55
    pipe(ax1, RIN_X, 6.3, RIN_X, RIN_TOP, C_BROWN, style="--")      # riser up to tank (no CV-3 — P-04 has an integral check valve)
    arrow_pipe(ax1, RIN_X, 7.7, RIN_X, 8.15, color=C_BROWN)
    pipe(ax1, RIN_X, RIN_TOP, 7.1, RIN_TOP, C_BROWN, style="--")    # into tank right side, near top
    arrow_pipe(ax1, 7.35, RIN_TOP, 7.16, RIN_TOP, color=C_BROWN)

    # ── IBC-3 bottom shared tap → P-02 (recycle) + P-05 (drain): ONE penetration ──
    TAP_Y = 6.85
    pipe(ax1, 6.4, 7.5, 6.4, TAP_Y, C_BROWN)                        # tank bottom → shared tee
    ax1.plot([6.4], [TAP_Y], "o", ms=4.5, color=C_BROWN, zorder=6)  # tee node
    ax1.text(6.62, 7.12, "IBC-3 BOTTOM TAP\n(1 penetration\n→ P-02 + P-05)",
             ha="left", va="center", fontsize=5.0, color=C_BROWN, style="italic")

    # P-02 recycle leg — BV-03 suction isolation (consistent with the other pumps), then down to the filter skid
    pipe(ax1, 6.4, TAP_Y, 6.4, 6.1 + VR, C_BROWN)
    valve(ax1, 6.4, 6.1, color=C_BROWN)
    ax1.text(6.62, 6.1, "BV-03", ha="left", fontsize=6, color=C_BROWN)
    pipe(ax1, 6.4, 6.1 - VR, 6.4, 5.4 + PR, C_BROWN)
    arrow_pipe(ax1, 6.4, 5.85, 6.4, 5.65, color=C_BROWN)
    pump(ax1, 6.4, 5.4, color=C_PUMP)
    ax1.text(6.60, 5.3, "P-02\n12VDC\n3.5 GPM", ha="left", fontsize=6, color=C_PUMP)
    pipe(ax1, 6.4, 5.4 - PR, 6.4, 4.6, C_BROWN)                     # P-02 → filter skid

    # ── Brown drain-out — shared tap → P-05 → exterior drain port X3 ─────────────
    BD_X = 5.35
    pipe(ax1, 6.4, TAP_Y, BD_X, TAP_Y, C_BROWN)                     # tee branch → drain riser
    pipe(ax1, BD_X, TAP_Y, BD_X, 7.55, C_BROWN)                     # up to BV-02 (P-05 drain isolation)
    valve(ax1, BD_X, 7.65, color=C_BROWN)
    ax1.text(BD_X - 0.15, 7.62, "BV-02", ha="right", fontsize=6, color=C_BROWN)
    pipe(ax1, BD_X, 7.75, BD_X, 8.3 - PR, C_BROWN)                  # valve top → pump bottom
    pump(ax1, BD_X, 8.3, color=C_PUMP)
    ax1.text(BD_X - 0.15, 8.2, "P-05\n12VDC", ha="right", fontsize=6, color=C_PUMP)
    pipe(ax1, BD_X, 8.3 + PR, BD_X, 9.5, C_BROWN)                   # pump top → ext port
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

    # SV-01 pH sample tap — on the filtered line, before the diverter
    pipe(ax1, 8.2, 3.25, 8.9, 3.25, C_BROWN)
    arrow_pipe(ax1, 8.6, 3.25, 9.1, 3.25, color=C_BROWN)     # rightward to DV-01
    valve(ax1, 9.15, 3.25, color="#F9A825", size=0.05, label="SV")   # SV-01 sample valve
    pipe(ax1, 9.15, 3.25 - 0.05 * 1.6, 9.15, 2.78, C_BROWN)  # downturned spout for the cup
    leader(ax1, 9.15, 3.25, 10.55, 2.30,
           "SV-01 — pH sample tap\n(draw sample → meter → set DV-01)",
           fs=6, color="#E65100", ha="right")

    # ── DIVERTER VALVE after filter — back to Blue OR forward to Black ─────────────
    DVR = 0.075 * 1.6  # diverter valve circle radius = 0.12
    pipe(ax1, 9.4, 3.25, 9.7 - DVR, 3.25, C_BROWN)
    diverter(ax1, 9.7, 3.25, color="#777777", size=0.075, branch="up")  # branch up = recycle to Blue; through L→R = to Black
    ax1.text(9.7, 2.9, "3W-DV-01\nDIVERTER", ha="center", fontsize=6, color="#444")

    # Path back to Blue IBC-2 — up at X=9.7, left at Y=9.2, into IBC-2 side-entry near top
    RET_Y = 9.2   # return horizontal — below ext fill port at Y=9.65
    pipe(ax1, 9.7, 3.25 + DVR,  9.7, 3.8 - BR,  C_BLUE, style="--")   # below blue supply
    pipe(ax1, 9.7, 3.8 + BR,   9.7, 6.3 - BR,  C_BLUE, style="--")   # between crossings
    pipe(ax1, 9.7, 6.3 + BR,   9.7, RET_Y,     C_BLUE, style="--")   # above brown drain → return level
    arrow_pipe(ax1, 9.7, 7.0, 9.7, 7.3, color=C_BLUE)                # short upward return arrow
    pipe(ax1, 9.7, RET_Y, 3.7, RET_Y, C_BLUE, style="--")            # left to IBC-2 top-right
    pipe_bridge(ax1, BD_X, RET_Y, color=C_BLUE, lw=LW_PIPE, bg=C_BROWN_L, style="--")  # over brown drain-out pipe
    arrow_pipe(ax1, 5.0, RET_Y, 4.7, RET_Y, color=C_BLUE)            # short leftward return arrow
    pipe(ax1, 3.7, RET_Y, 3.7, 8.2, C_BLUE, style="--")              # down to IBC-2 (top-right) — SEPARATE from the X1 fill (no CV-2 — P-02 has an integral check valve)
    arrow_pipe(ax1, 3.7, 8.36, 3.7, 8.28, color=C_BLUE)             # downward return arrow
    ax1.text(6.5, RET_Y + 0.15, "DV-01 RECYCLE → IBC-2 SIDE-ENTRY (separate return path)",
             ha="center", fontsize=6, color=C_BLUE, style="italic")

    # Path to Black system — right from DV-01 at Y=3.25, then up via W_X vertical
    DV01_R = 0.075 * 1.6  # diverter valve circle radius
    pipe(ax1, 9.7 + DV01_R, 3.25, W_X, 3.25, C_BLACK)
    arrow_pipe(ax1, 10.3, 3.25, W_X - 0.1, 3.25, color=C_BLACK)  # rightward to waste vertical

    # ── BLACK SYSTEM ──────────────────────────────────────────────────────────────
    tank(ax1, W_X, W_Y, W_W, W_H, fc="#D5D5D0", ec=C_WASTE_IBC, lw=2,
         label="IBC-4", sublabel="264 gal (1000L)\nWASTE")

    # Waste IBC vertical — DV-01 feeds at Y=3.25, DV-02 black feeds at Y=2.6
    pipe(ax1, W_X, 2.6,       W_X, 3.8 - BR,  C_BLACK)   # DV-02 feed to blue crossing
    pipe(ax1, W_X, 3.8 + BR,  W_X, 6.3 - BR,  C_BLACK)   # blue crossing to brown crossing
    pipe(ax1, W_X, 6.3 + BR,  W_X, W_Y - W_H/2,  C_BLACK)  # brown crossing to IBC bottom
    arrow_pipe(ax1, W_X, 3.4, W_X, 4.5,       color=C_BLACK)   # upward flow (lower)
    # (no CV-4 — P-02/P-04 have integral check valves)
    arrow_pipe(ax1, W_X, 6.62, W_X, W_Y - W_H/2 - 0.02, color=C_BLACK)  # upward (upper)

    # ── Waste drain-out — IBC-4 to exterior drain port X4 via P-03 ────────────
    # Separate outlet from right side of IBC-4 (left side carries waste inflow)
    WD_X = 12.6
    pipe(ax1, W_X + W_W/2, 7.8, WD_X + VR, 7.8, C_BLACK)   # stub from IBC right edge → valve
    valve(ax1, WD_X, 7.8, color=C_BLACK)
    ax1.text(WD_X + 0.15, 7.75, "BV-06", ha="left", fontsize=6, color=C_BLACK)
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
    ax1.text(15.6, 6.55, f"PRINT\n({C_LEN} × {C_HGT}mm)", ha="center", va="center",
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
    ax1.text(14.95, 3.18,
             "NOTE — P-04 manually primed & started:\nsuction leg gravity-drains to the sump\nbetween cycles (no self-prime / auto-start)",
             ha="right", va="top", fontsize=5.0, color="#555555", style="italic", zorder=6)

    # 3-way diverter valve below P-04
    DV02_Y = 3.05
    DV02_R = 0.075 * 1.6   # diverter valve circle radius = 0.12
    pipe(ax1, 15.6, 3.65 - PUMP_R, 15.6, DV02_Y + DV02_R, C_BROWN)  # P-04 → DV-02
    # SV-02 sample tap — teed off the P-04 discharge, ahead of the diverter
    SV2_Y = 3.40
    pipe(ax1, 15.6, SV2_Y, 15.98, SV2_Y, C_BROWN)                   # tee branch (right)
    valve(ax1, 16.08, SV2_Y, color="#F9A825", size=0.05, label="SV")
    pipe(ax1, 16.08, SV2_Y - 0.08, 16.08, SV2_Y - 0.22, C_BROWN)   # downturned sample spout
    ax1.text(16.22, SV2_Y + 0.02, "SV-02", ha="left", fontsize=6, color="#E65100")
    diverter(ax1, 15.6, DV02_Y, color="#777777", size=0.075, branch="left")  # branch left = recycle to brown; through top→bottom = to Black
    ax1.text(16.00, DV02_Y - 0.22, "3W-DV-02", ha="center", fontsize=6, color="#444")

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
    BOX_H = 2.05
    BOX_X = 0.3    # Blue System left edge
    BOX_Y = 0.6    # bottom of system boxes
    lx = BOX_X + 0.1            # left margin for content
    ly = BOX_Y + BOX_H - 0.25   # top content Y (just inside box top)

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
        ("SV-xx",     "Sample / test tap"),
        ("▷|",        "Check valve — CV-1 (X1 gravity fill only; pumps have integral checks)"),
        ("F1/F2/F3",  "Filter cartridge"),
        ("⬡",         "External bulkhead port (2\" NPT)"),
    ]
    for i, (sym, desc) in enumerate(syms):
        ax1.text(SYM_X + 0.15, ly - 0.10 - i * 0.25,
                 f"{sym} — {desc}", va="center", fontsize=6.2, color=C_TEXT, zorder=7)


    _save(fig1, "water-system-sheet1")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — TANK & FILTER SKID LAYOUT (PLAN VIEW — inside container)
# ═══════════════════════════════════════════════════════════════════════════════


def draw_sheet2():
    fig2, ax2 = plt.subplots(1, 1, figsize=(18, 12))
    fig2.patch.set_facecolor("#F5F5F0")
    ax2.set_facecolor("#F5F5F0")
    ax2.axis("off")

    # ── Title block ───────────────────────────────────────────────────────────────
    title_block(ax2, f"SHEET 2 OF {TOTAL_SHEETS}",
                drawing_title="WATER SYSTEM EQUIPMENT LAYOUT",
                subtitle="Plan view (inside container)",
                scale_note="1:25 (approx)",
                doc_id="TBS-001 · Water System")

    # ── Plan view ─────────────────────────────────────────────────────────────────
    ax2.set_xlim(-0.5, 12.5)
    ax2.set_ylim(-0.8, 6.8)
    ax2.set_aspect("equal")

    # Container outline (20ft = 6096mm; 8ft = 2438mm → scaled ×1/25)
    # At 1:25: 6096/25 = 243.8 → use 12 units; 2438/25 = 97.5 → use 5 units
    CW = 12.0   # container width in drawing units
    CH = 5.0    # container depth in drawing units
    ax2.add_patch(plt.Rectangle((0, 0), CW, CH, fc="white", ec=C_FRAME, lw=3,
                                 zorder=1))
    ax2.text(6.0, -0.25, "CONTAINER INTERIOR — PLAN VIEW  (6096 × 2438mm interior)",
             ha="center", fontsize=8, color=C_FRAME)

    # Wall thickness (container wall ~75mm → 0.075 at 1:25, round to 0.1)
    WT = 0.1
    ax2.add_patch(plt.Rectangle((-WT, -WT), CW + 2*WT, CH + 2*WT,
                                 fc="none", ec="#777", lw=1.2, ls="--", zorder=0))

    # ── Equipment placement ───────────────────────────────────────────────────────
    # IBCs in RIGHT END ZONE (X=4649–5893mm); drums in LEFT END ZONE (X=0–1100mm).
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
             "IBC-1 BLUE / IBC-3 BROWN", "Top: Blue ~900L clean\nBottom: Brown recycle")
    # Far column (Yd=1316–2332mm): Blue #2 on top, Waste on bottom — 270mm plumbing corridor between columns
    # Plan view sees top tier (Blue #2)
    FAR_IBC_DY = IBC_FAR_Y * SY
    ibc_plan(ax2, IBC_COL_DX, FAR_IBC_DY, "#BBDEFB", C_BLUE_IBC,
             "IBC-2 BLUE / IBC-4 WASTE", "Top: Blue ~900L clean\nBottom: Waste")

    # Equipment panel in IBC plumbing corridor (between IBC columns)
    EP_X_DU = PUMP_X * SX             # ≈ 9.77
    EP_W_DU = PUMP_W * SX             # ≈ 1.59
    EP_Y_DU = 1046 * SY               # ≈ 2.21 (corridor near face)
    EP_D_DU = 270 * SY                # ≈ 0.57 (corridor width)
    ax2.add_patch(plt.Rectangle((EP_X_DU, EP_Y_DU), EP_W_DU, EP_D_DU,
                  fc=C_FILT, ec="#F57F17", lw=2, zorder=2))
    # Panel box is a thin sliver between the IBC stacks — label it with a leader into
    # the clear tray white space to the left so the text doesn't bury the IBC geometry.
    leader(ax2, EP_X_DU, EP_Y_DU + EP_D_DU / 2,
           EP_X_DU - 1.5, EP_Y_DU + EP_D_DU / 2 - 0.62,
           "CORRIDOR PLUMBING PANEL\nP-01/P-03/P-04/P-05 · ACC-01\nDV-02 · SV-02 · BV-01/02/06",
           fs=6, color="#E65100", ha="center")

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
    # Panel split line (two panels, each 1992mm wide)
    tray_mid_x = (TRAY_X0 + TRAY_X1) / 2
    ax2.plot([tray_mid_x, tray_mid_x], [TRAY_Y0, TRAY_Y0 + TRAY_DY],
             color="#388E3C", lw=1.2, ls="--", zorder=2)
    ax2.text((TRAY_X0 + TRAY_X1) / 2, TRAY_Y0 + TRAY_DY - 0.15,
             "PROCESSING TRAY (304 SS, 50mm RIM, 2 PANELS)",
             ha="center", fontsize=7, color="#2E7D32")
    ax2.text(tray_mid_x - 0.8, TRAY_Y0 + TRAY_DY / 2,
             "PANEL A\n1992 × 2200mm", ha="center", fontsize=6, color="#388E3C")
    ax2.text(tray_mid_x + 0.8, TRAY_Y0 + TRAY_DY / 2,
             "PANEL B\n1992 × 2200mm", ha="center", fontsize=6, color="#388E3C")

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

    # Left end zone shading (X=0–150mm — light trap only, drums removed rev 5)
    ZONE_L_DX = ZONE_L_END * SX   # = 150mm
    ax2.add_patch(plt.Rectangle((0, 0), ZONE_L_DX, CH,
                  fc="#FFF3E0", ec="none", alpha=0.45, zorder=0))
    ax2.plot([ZONE_L_DX, ZONE_L_DX], [0, CH], color="#805000", lw=1.5, ls="--",
             zorder=6)
    ax2.text(ZONE_L_DX - 0.05, CH + 1,
             f"LEFT END ZONE\nX=0–{ZONE_L_END}mm\n(light trap only)",
             ha="right", va="top", fontsize=6.5, color="#805000", fontweight="bold")

    # Right end zone shading (X=4649–5893mm in drawing)
    ZONE_R_DX = ZONE_R_START * SX   # ≈ 9.45
    ax2.add_patch(plt.Rectangle((ZONE_R_DX, 0), CW - ZONE_R_DX, CH,
                  fc="#E8F0FF", ec="none", alpha=0.45, zorder=0))
    ax2.plot([ZONE_R_DX, ZONE_R_DX], [0, CH], color="#004080", lw=1.5, ls="--",
             zorder=6)
    ax2.text(ZONE_R_DX + 1, CH + 1,
             f"RIGHT END ZONE\nX={ZONE_R_START}–5893mm\n(4× IBC 2×2 stack)",
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
    draw_dim_h(ax2, 0, CW, -0.30, "5893mm (CONTAINER INTERIOR)", offset=0.21, fs=6.5, above=False)
    draw_dim_v(ax2, -0.2 - 0.1, 0, CH, "2362mm", offset=0.27, fs=6.5, right=False)
    draw_dim_h(ax2, IBC_COL_DX, IBC_COL_DX + IBC_W, 5.2 - 0.25, "IBC col: 1219mm", offset=0.27, fs=6.5, above=False)
    draw_dim_h(ax2, 0, ZONE_L_DX, 5.5, f"LEFT END ZONE: {ZONE_L_END}mm", offset=0.27, fs=6.5, color="#805000", above=False)
    draw_dim_h(ax2, ZONE_R_DX, CW, 5.5, f"RIGHT END ZONE: {C_LEN - ZONE_R_START}mm", offset=0.27, fs=6.5, color="#004080", above=False)

    # Orientation arrow — points toward pinhole wall (bottom, Yd=0)
    ax2.annotate("", xy=(CW + 0.3, 0.4), xytext=(CW + 0.3, 1.6),
                 arrowprops=dict(arrowstyle="-|>", color=C_FRAME, lw=1.5,
                                 mutation_scale=12))
    ax2.text(CW + 0.3, 1.8, "FRONT\n(PINHOLE\nWALL)", ha="center", fontsize=6,
             color=C_FRAME)


    _save(fig2, "water-system-sheet2")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — PROCESSING TRAY DRAINAGE PLAN (water flow direction)
# ═══════════════════════════════════════════════════════════════════════════════


def draw_sheet3():
    fig3, ax3 = plt.subplots(1, 1, figsize=(18, 12))
    fig3.patch.set_facecolor("#F5F5F0")
    ax3.set_facecolor("#F5F5F0")
    ax3.axis("off")

    # ── Title block ───────────────────────────────────────────────────────────────
    title_block(ax3, f"SHEET 3 OF {TOTAL_SHEETS}",
                drawing_title="PROCESSING TRAY DRAINAGE PLAN",
                subtitle="Plan view (water flow direction)",
                scale_note="Axes in mm",
                doc_id="TBS-001 · Water System")

    # ── Coordinates in mm (identity scale) ──────────────────────────────────────
    TRAY_DRAW_W = PROC_TRAY_W
    TRAY_DRAW_H = PROC_TRAY_D




    ax3.set_xlim((-620), (PROC_TRAY_W + 860))
    ax3.set_ylim((-1820), (PROC_TRAY_D + 620))
    ax3.set_aspect("equal")

    # ── Tray outline ─────────────────────────────────────────────────────────────
    ax3.add_patch(plt.Rectangle(((0), (0)),
                  (PROC_TRAY_W), (PROC_TRAY_D),
                  fc="#E8F5E9", ec="#388E3C", lw=2.5, zorder=1))

    # Rim shading (inner border)
    ax3.add_patch(plt.Rectangle(((PROC_TRAY_RIM), (PROC_TRAY_RIM)),
                  (PROC_TRAY_W - 2*PROC_TRAY_RIM),
                  (PROC_TRAY_D - 2*PROC_TRAY_RIM),
                  fc="#C8E6C9", ec="none", zorder=1, alpha=0.5))

    # Label corners with elevation annotations (high/low)
    # Low point: IBC corner (near rim, right side) — drain at X=4550, Yd=80
    # High point: far-left corner (opposite diagonal)
    drain_local_x_s3 = PROC_TRAY_DRAIN_X - PROC_TRAY_X_L
    ax3.text((drain_local_x_s3), (-380), "LOW CORNER\n(DRAIN — IBC SIDE)",
             ha="center", fontsize=7.5, fontweight="bold", color="#D32F2F")
    ax3.text((-50), (PROC_TRAY_D + 120),
             "HIGH CORNER\n(FAR-LEFT)",
             ha="left", fontsize=7.5, fontweight="bold", color="#1565C0")

    ax3.text((-50), (PROC_TRAY_D / 2), "HIGH\nEDGE",
             ha="right", va="center", fontsize=6.5, color="#1565C0", fontweight="bold")
    ax3.text((PROC_TRAY_W + 50), (-70), "LOW EDGE",
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
            arrow_len = (120)
            dx_du = dx_mm / mag * arrow_len
            dy_du = dy_mm / mag * arrow_len

            ax_du = (ax_mm)
            ay_du = (ay_mm)

            ax3.annotate("", xy=(ax_du + dx_du, ay_du + dy_du),
                         xytext=(ax_du - dx_du * 0.3, ay_du - dy_du * 0.3),
                         arrowprops=dict(arrowstyle="-|>", color=ARROW_COLOR,
                                         lw=1.5, mutation_scale=10, alpha=ARROW_ALPHA),
                         zorder=4)

    # ── Drain symbol (circle + crosshair) ───────────────────────────────────────
    drain_dx = (drain_local_x)
    drain_dy = (drain_local_yd)
    DRAIN_R = (100)

    drain_circle = plt.Circle((drain_dx, drain_dy), DRAIN_R,
                               fc="white", ec="#D32F2F", lw=2.5, zorder=6)
    ax3.add_patch(drain_circle)
    ax3.plot([drain_dx - DRAIN_R*0.7, drain_dx + DRAIN_R*0.7],
             [drain_dy, drain_dy], color="#D32F2F", lw=1.8, zorder=7)
    ax3.plot([drain_dx, drain_dx],
             [drain_dy - DRAIN_R*0.7, drain_dy + DRAIN_R*0.7],
             color="#D32F2F", lw=1.8, zorder=7)

    # Drain label — single leader to the right (clear side)
    leader(ax3, (drain_local_x), (drain_local_yd + DRAIN_R),
           (drain_local_x + 250), (drain_local_yd + 450),
           f"SUMP WELL (P-04 PICKUP)\n"
           f"X={PROC_TRAY_DRAIN_X}  Yd={PROC_TRAY_DRAIN_YD}\n"
           f"{PROC_TRAY_SUMP_W}x{PROC_TRAY_SUMP_D}x{PROC_TRAY_SUMP_Z}mm",
           fs=7, color="#D32F2F", ha="left")

    # ── Slope annotations ────────────────────────────────────────────────────────
    # Slope: 1:200 in both X and Yd toward drain corner (IBC side)
    x_fall = PROC_TRAY_W / 200  # full-width fall (left to right)
    yd_fall = PROC_TRAY_D / 200  # full-depth fall (far to near)

    # X-slope annotation (center of tray)
    ann_x = (PROC_TRAY_W * 0.5)
    ann_y = (PROC_TRAY_D * 0.5)
    ax3.text(ann_x, ann_y,
             f"X-SLOPE: 1:200 → IBC CORNER\n({x_fall:.1f}mm fall over {PROC_TRAY_W:.0f}mm)",
             ha="center", va="center", fontsize=7, color="#0D47A1",
             bbox=dict(fc="white", ec="#0D47A1", lw=0.8, pad=3, alpha=0.9),
             zorder=8)

    # Yd-axis slope annotation (upper area)
    ann_y2 = (PROC_TRAY_D * 0.78)
    ax3.text((PROC_TRAY_W * 0.5), ann_y2,
             f"Yd-SLOPE: 1:200\n({yd_fall:.1f}mm fall over {PROC_TRAY_D}mm)",
             ha="center", va="center", fontsize=7, color="#0D47A1",
             bbox=dict(fc="white", ec="#0D47A1", lw=0.8, pad=3, alpha=0.9),
             zorder=8)

    # ── Dimensions ───────────────────────────────────────────────────────────────
    # Tray width (X direction)
    draw_dim_h(ax3, (0), (PROC_TRAY_W), (PROC_TRAY_D + 310),
               f"{PROC_TRAY_W}mm", offset=93, fs=6.5, above=True)


    # ax3.annotate("", xy=(OX + TRAY_DRAW_W, OY + TRAY_DRAW_H + 0.6),
    #              xytext=(OX, OY + TRAY_DRAW_H + 0.6),
    #              arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=1.2,
    #                              mutation_scale=10))
    # ax3.text(OX + TRAY_DRAW_W/2, OY + TRAY_DRAW_H + 0.75,
    #          f"{PROC_TRAY_W}mm (X={PROC_TRAY_X_L}–{PROC_TRAY_X_R})",
    #          ha="center", fontsize=7, color=C_DIM)

    # Tray depth (Yd direction)
    draw_dim_v(ax3, (-310), (PROC_TRAY_D), (0),
               f"{PROC_TRAY_D}mm", offset=93, fs=6.5, right=False)

    # Drain X position dimension
    draw_dim_h(ax3, (drain_local_x), (0), (-170),
               f"{drain_local_x}mm from left edge", offset=58, fs=6.5, above=False)

    # ── Walkway positions (dashed outlines) ──────────────────────────────────────
    WK_COLOR = "#8D6E63"
    WK_ALPHA_L = 0.4

    # Near walkway (overlaps tray near edge)
    near_wk_y0 = (-PROC_TRAY_YD_NEAR + WALKWAY_NEAR_YD)  # Yd=0 in container coords
    near_wk_y1 = (-PROC_TRAY_YD_NEAR + WALKWAY_NEAR_YD + WALKWAY_W)
    ax3.add_patch(plt.Rectangle(((0), near_wk_y0),
                  (PROC_TRAY_W), near_wk_y1 - near_wk_y0,
                  fc=WK_COLOR, ec=WK_COLOR, lw=1.2, ls="--",
                  alpha=WK_ALPHA_L, hatch="//", zorder=2))
    ax3.text((PROC_TRAY_W + 50), (near_wk_y0 + near_wk_y1)/2,
             "NEAR\nWALKWAY\n(300mm)",
             ha="left", va="center", fontsize=6, color=WK_COLOR)

    # Far walkway
    far_wk_yd_local = WALKWAY_FAR_YD - PROC_TRAY_YD_NEAR
    far_wk_y0 = (far_wk_yd_local)
    far_wk_y1 = (far_wk_yd_local + WALKWAY_W)
    ax3.add_patch(plt.Rectangle(((0), far_wk_y0),
                  (PROC_TRAY_W), far_wk_y1 - far_wk_y0,
                  fc=WK_COLOR, ec=WK_COLOR, lw=1.2, ls="--",
                  alpha=WK_ALPHA_L, hatch="//", zorder=2))
    ax3.text((PROC_TRAY_W + 50), (far_wk_y0 + far_wk_y1)/2,
             "FAR\nWALKWAY\n(300mm)",
             ha="left", va="center", fontsize=6, color=WK_COLOR)

    # ── Pipe run from drain (rev12 routing) ──────────────────────────────────────
    # 1" suction hose exits the sump, drops in the grate gap in FRONT of the tray
    # (Yd~50, clear of the rev12 right-walkway long beam), runs RIGHT to the tray–IBC
    # gap, then turns NORTH up the gap to the equipment panel (corridor, Yd≈1046).
    corner_local_x = PROC_TRAY_W + 15   # just past tray right edge (into the tray–IBC gap)
    pipe_rim_yd = drain_local_yd - 30    # ~Yd50 — in front of the tray near rim (the twist depth)
    pipe_rim_dy = (pipe_rim_yd)

    # Short drop from sump to rim exterior
    ax3.plot([drain_dx, drain_dx], [drain_dy - DRAIN_R, pipe_rim_dy],
             color=C_BROWN, lw=2.5, solid_capstyle="round", zorder=5)

    # Right along rim exterior to tray corner
    corner_dx = (corner_local_x)
    ax3.plot([drain_dx, corner_dx], [pipe_rim_dy, pipe_rim_dy],
             color=C_BROWN, lw=2.5, solid_capstyle="round", zorder=5)

    # North from tray corner to corridor level
    panel_local_yd = CORRIDOR_YD_NEAR - PROC_TRAY_YD_NEAR   # 966mm
    panel_local_x = EQPANEL_X - PROC_TRAY_X_L               # 4830mm
    panel_dy = (panel_local_yd)
    panel_dx = (panel_local_x)
    ax3.plot([corner_dx, corner_dx], [pipe_rim_dy, panel_dy],
             color=C_BROWN, lw=2.5, solid_capstyle="round", zorder=5)

    # Right into equipment panel
    ax3.plot([corner_dx, panel_dx], [panel_dy, panel_dy],
             color=C_BROWN, lw=2.5, solid_capstyle="round", zorder=5)

    # Equipment panel symbol (small rectangle at pipe terminus)
    ax3.add_patch(plt.Rectangle(((panel_local_x), (panel_local_yd - 85)),
                  (50), (170),
                  fc="#D4C8A0", ec="#A09060", lw=1.5, zorder=6))

    leader(ax3, (panel_local_x + 50), (panel_local_yd),
           (panel_local_x + 25), (panel_local_yd + 205),
           "CORRIDOR PLUMBING PANEL\n(P-04 — tray drain)", fs=6.5, color=C_PUMP)

    ax3.text(((drain_local_x + corner_local_x) / 2), (pipe_rim_yd - 120),
             "P-04 SUCTION HOSE ALONG RIM EXTERIOR",
             ha="center", fontsize=6.5, color=C_BROWN, style="italic", zorder=8)

    # ── Notes ────────────────────────────────────────────────────────────────────
    notes = [
        "NOTES:",
        f"1. Dual-axis pitch 1:200 — water converges on sump at X={PROC_TRAY_DRAIN_X}, Yd={PROC_TRAY_DRAIN_YD}.",
        f"2. Maximum fall: {PROC_TRAY_PITCH}mm (Yd axis) + {x_fall:.1f}mm (X axis from far corner to sump).",
        f"3. Sump well ({PROC_TRAY_SUMP_W}x{PROC_TRAY_SUMP_D}x{PROC_TRAY_SUMP_Z}mm) pressed into tray floor — P-04 suction pickup lifts to IBC-3 side-entry near top.",
        f"4. Tray: 304 SS, {PROC_TRAY_RIM}mm rim, on tapered HDPE shim strips. No tray floor penetration.",
        f"5. Wall-cantilevered walkway — no legs or structure on tray floor near sump.",
    ]
    draw_notes(ax3, notes, (-410), (-890), spacing=(70), fs=7,
               width=(3600), color=C_TEXT, title_color=C_TEXT,
               font={"fontfamily": "monospace"})

    _save(fig3, "water-system-sheet3")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 4 — PROCESSING TRAY DRAIN CROSS-SECTION ELEVATION
# Two panels:
#   LEFT  — Zoomed detail of sump well + pickup tube + shim strips (~1:2)
#   RIGHT — Full cross-section showing suction line from sump to P-04
#           pump to 3W-DV-02 diverter to IBC-3 (~1:15)
# Horizontal = Yd, Vertical = Z (height above floor).
# ═══════════════════════════════════════════════════════════════════════════════


def draw_sheet4():
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
    title_block(ax4_tb, f"SHEET 4 OF {TOTAL_SHEETS}",
                drawing_title="PROCESSING TRAY DRAIN — SUMP PICKUP CROSS-SECTION",
                subtitle=f"Section A-A at X={PROC_TRAY_DRAIN_X}mm (through sump) + plan view of rim hose routing",
                scale_note="AXES IN mm — MULTIPLE PANELS",
                doc_id="TBS-001 · Water System",
                height=0.75)



    def draw_pipe_path(ax, y_pts, z_pts, od_mm, wall_mm,
                       fc="#B0B0B8", ec="#333333", bore_fc="white",
                       elbow_r=None, zorder=5):
        """Thin wrapper → tbs_drawing.draw_pipe_path (canonical body); injects
        this sheet's scale funcs.  See skills/skill_plumbing_drawing.md."""
        _tbs_pipe_path(ax, y_pts, z_pts, od_mm, wall_mm, fc, ec=ec,
                       bore_fc=bore_fc, elbow_r=elbow_r, zorder=zorder)

    def draw_pipe_end(ax, cy, cz, r_data, wall_data, fc="#B0B0B8",
                      ec="#333333", bore_fc="white", zorder=5):
        """Thin wrapper → tbs_drawing.draw_pipe_end (canonical body)."""
        _tbs_pipe_end(ax, cy, cz, r_data, wall_data, fc=fc, ec=ec,
                      bore_fc=bore_fc, zorder=zorder)


    # ═════════════════════════════════════════════════════════════════════════════
    # PANEL A — SUMP WELL & PICKUP DETAIL (~1:2)
    # Focused view: Yd = -20 to 420mm, Z = -50 to 200mm
    # Shows: shim strips under tray, tray floor with slope, sump well,
    #         pickup tube with foot valve, suction hose over rim, walkway.
    # ═════════════════════════════════════════════════════════════════════════════
    SC_A = 1.0
    OA_X = 0
    OA_Y = 0



    ax4a.set_xlim((-41), (422))
    ax4a.set_ylim((-56), (223))

    # Panel A title
    ax4a.text((195), (195), "DETAIL A — SUMP WELL & PICKUP (AXES IN mm)",
              ha="center", va="top", fontsize=10, fontweight="bold",
              color="#1A237E", zorder=10)

    # ── Container floor (section fill) ──────────────────────────────────────────
    FLOOR_T = 4.0   # simplified floor thickness in section
    ax4a.add_patch(plt.Rectangle(((-20), (-FLOOR_T)),
                  450 / SC_A, FLOOR_T / SC_A,
                  fc="#B0B0B8", ec=C_FRAME, lw=1.8, zorder=2, hatch=".."))

    # Near wall (Yd=0) — vertical
    WALL_T = 2.0
    ax4a.add_patch(plt.Rectangle(((-WALL_T), (-FLOOR_T)), WALL_T / SC_A,
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
        ax4a.add_patch(plt.Rectangle(((shim_yd - shim_vis_w/2), (0)),
                      shim_vis_w / SC_A, shim_h_here / SC_A,
                      fc=shim_color, ec="#A09070", lw=0.8, zorder=3))

    # ── Tray floor (sloped, sitting on shims) ────────────────────────────────────
    # Tray bottom surface at near end = TRAY_BASE_Z (20mm), rises with slope
    tray_z_at_near = TRAY_BASE_Z  # 20mm — sits at sump depth level
    tray_z_at_far = TRAY_BASE_Z + (tray_yd_far_view - tray_yd_near) * slope_per_mm * SLOPE_EXAG_A

    # Tray floor polygon
    tray_pts_x = [(tray_yd_near), (tray_yd_far_view),
                  (tray_yd_far_view), (tray_yd_near)]
    tray_pts_y = [(tray_z_at_near), (tray_z_at_far),
                  (tray_z_at_far + TRAY_T), (tray_z_at_near + TRAY_T)]
    ax4a.fill(tray_pts_x, tray_pts_y, fc="#C8D8E8", ec=C_FRAME, lw=1.5, zorder=4)

    # Near rim — extends from tray floor (Z=20mm) up by rim height (50mm)
    rim_h = PROC_TRAY_RIM  # 50mm
    RIM_TOP = TRAY_BASE_Z + rim_h  # 20 + 50 = 70mm above container floor
    ax4a.add_patch(plt.Rectangle(((tray_yd_near - TRAY_T), (TRAY_BASE_Z)),
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
    sump_pts_x = [(sump_yd_start + 3), (sump_yd_end - 3),
                  (sump_yd_end - 3), (sump_yd_end),
                  (sump_yd_end), (sump_yd_start),
                  (sump_yd_start), (sump_yd_start + 3)]
    sump_pts_z = [(sump_z_floor + TRAY_T), (sump_z_floor + TRAY_T),
                  (sump_z_floor), (sump_z_floor),
                  (tray_z_at_near), (tray_z_at_near),
                  (sump_z_floor), (sump_z_floor)]
    ax4a.fill(sump_pts_x, sump_pts_z, fc="#C8D8E8", ec=C_FRAME, lw=1.5, zorder=4)

    # Water pooled in sump (blue fill) — water collects from Z=0 up to near tray floor
    ax4a.fill([(sump_yd_start + 4), (sump_yd_end - 4),
               (sump_yd_end - 4), (sump_yd_start + 4)],
              [(TRAY_BASE_Z - 4), (TRAY_BASE_Z - 4),
               (sump_z_floor + TRAY_T), (sump_z_floor + TRAY_T)],
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
                   TUBE_OD, TUBE_WALL,
                   fc="#D0D0D0", ec=C_FRAME, zorder=6)
    ax4a.add_patch(plt.Rectangle(((tube_yd - foot_valve_w/2), (tube_z_bot)),
                  foot_valve_w / SC_A, foot_valve_h / SC_A,
                  fc="#D0D0D0", ec=C_FRAME, lw=1.0, zorder=7))
    # Strainer mesh marks
    for sy_m in range(3):
        mesh_y = tube_yd - foot_valve_w/2 + 5 + sy_m * (foot_valve_w - 10) / 2
        ax4a.plot([(mesh_y), (mesh_y)],
                 [(tube_z_bot), (tube_z_bot + foot_valve_h)],
                 color="#999999", lw=0.4, zorder=8)

    # ── Suction hose from tube top, along tray rim exterior ──────────────────────
    HOSE_OD = 33.0   # 1" reinforced suction hose OD (mm)
    HOSE_WALL = 4.0  # hose wall thickness (mm)
    RIM_EXT_YD = tray_yd_near - HOSE_OD / 2 - 5  # ~60mm — hose CL on exterior of rim
    HOSE_RIM_Z = TRAY_BASE_Z + rim_h / 2 - 25    # ~20mm — lowered to clear cantilever brackets

    # Hose path: short vertical overlap with tube top (creates 90° elbow) →
    # horizontal above walkway → 90° elbow → down along rim exterior
    ELBOW_OVERLAP = HOSE_OD  # vertical approach length for visible elbow fitting
    hose_pts_y = [tube_yd, tube_yd, RIM_EXT_YD, RIM_EXT_YD]
    hose_pts_z = [tube_z_top - ELBOW_OVERLAP, tube_z_top, tube_z_top, HOSE_RIM_Z]
    draw_pipe_path(ax4a, hose_pts_y, hose_pts_z, HOSE_OD, HOSE_WALL,
                   fc=C_BROWN, ec="#5A3020", zorder=8)

    # Pipe end-on at rim exterior (hose turns to run along X — into the page)
    pipe_r_a = HOSE_OD / 2 / SC_A
    pipe_wall_a = HOSE_WALL / SC_A
    draw_pipe_end(ax4a, (RIM_EXT_YD), (HOSE_RIM_Z),
                  pipe_r_a, pipe_wall_a,
                  fc=C_BROWN, ec=C_FRAME, bore_fc="white", zorder=9)

    # ── Water surface in tray (away from sump) ───────────────────────────────────
    FLOOD_DEPTH = 6
    water_z_left = tray_z_at_near + TRAY_T + FLOOD_DEPTH
    water_z_right = tray_z_at_far + TRAY_T + FLOOD_DEPTH
    ax4a.fill([(sump_yd_end + 5), (tray_yd_far_view),
               (tray_yd_far_view), (sump_yd_end + 5)],
              [(water_z_left + 1), (water_z_right),
               (tray_z_at_far + TRAY_T), (tray_z_at_near + TRAY_T + 1)],
              fc="#B3D9F2", ec="none", alpha=0.3, zorder=3)
    ax4a.plot([(sump_yd_end + 5), (tray_yd_far_view)],
             [(water_z_left + 1), (water_z_right)],
             color=C_BLUE, lw=1.0, ls="--", zorder=5)

    # ── Walkway grate ───────────────────────────────────────────────────────────
    ax4a.add_patch(plt.Rectangle(((0), (WK_DECK_H - WK_GRATE_T)),
                  WALKWAY_W / SC_A, WK_GRATE_T / SC_A,
                  fc="#E0D6C8", ec="#8D6E63", lw=1.0, hatch="///", zorder=3,
                  alpha=0.7))

    # Bracket arm (triangle)
    ax4a.fill([(0), (0), (WALKWAY_W * 0.9)],
              [(WK_DECK_H - WK_GRATE_T), (WK_DECK_H - WK_GRATE_T - 30),
               (WK_DECK_H - WK_GRATE_T)],
              fc="#B0B0B8", ec=C_FRAME, lw=0.8, zorder=3, alpha=0.5)

    # ── Detail dimensions ────────────────────────────────────────────────────────
    # Rim top to floor
    draw_dim_v(ax4a, (tray_yd_near - 45), (0), (RIM_TOP),
               f"{int(RIM_TOP)}mm\nRIM TOP AFF", offset=3, fs=7, right=False)

    # Tray floor height (20mm — too short for dim_v label, use leader)
    leader(ax4a, (sump_yd_end + 20), (TRAY_BASE_Z),
           (sump_yd_end + 40), (TRAY_BASE_Z + 30),
           f"{PROC_TRAY_SUMP_Z}mm TRAY FLOOR AFF", fs=6.5, color=C_DIM)

    # Sump depth (20mm — too short for dim_v label, use leader)
    leader(ax4a, (sump_yd_end + 5), (sump_z_floor + TRAY_BASE_Z / 2),
           (sump_yd_end + 100), (-15),
           f"{PROC_TRAY_SUMP_Z}mm SUMP DEPTH", fs=6.5, color=C_DIM)

    # Sump width (Yd extent)
    draw_dim_h(ax4a, (sump_yd_start), (sump_yd_end),
               (sump_z_floor - 8),
               f"{PROC_TRAY_SUMP_D}mm", offset=1.6, fs=7, above=False)

    # Pickup clearance from sump floor
    draw_dim_v(ax4a, (tube_yd + TUBE_OD/2 + 8), (sump_z_floor), (tube_z_bot),
               "5mm", offset=1.2, fs=6, right=True)

    # Sump to wall
    draw_dim_h(ax4a, (0), (sump_yd_start), (FLOOR_T - 12),
               f"{sump_yd_start}mm", offset=1.6, fs=7, above=False)

    # Walkway deck height
    draw_dim_v(ax4a, (WALKWAY_W + 105), (0), (WK_DECK_H),
               f"{WK_DECK_H}mm DECK", offset=2, fs=6.5, right=True)

    # ── Detail leaders ───────────────────────────────────────────────────────────
    leader(ax4a, (tube_yd), (tube_z_bot + foot_valve_h/2),
           (tube_yd + 80), (-25),
           "1\" SS FOOT VALVE\nW/ STRAINER SCREEN", fs=7, color=C_FRAME)

    leader(ax4a, (tube_yd), (tube_z_top - 5),
           (tube_yd + 90), (140),
           "1\" HDPE\nPICKUP TUBE", fs=7, color=C_FRAME)

    leader(ax4a, (RIM_EXT_YD + 5), (HOSE_RIM_Z),
           (RIM_EXT_YD - 40), (HOSE_RIM_Z - 50),
           "1\" REINFORCED SUCTION\nHOSE ALONG RIM TO P-04\n(INTO PAGE — SEE PLAN)", fs=6, color=C_BROWN)

    leader(ax4a, (sump_yd_start + PROC_TRAY_SUMP_D/4), (TRAY_BASE_Z / 2),
           (150), (-30),
           f"SUMP WELL\n({PROC_TRAY_SUMP_W}x{PROC_TRAY_SUMP_D}x{PROC_TRAY_SUMP_Z}mm)\nBOTTOM ON CONTAINER FLOOR", fs=6.5, color="#0D47A1")

    leader(ax4a, (250), (water_z_left),
           (350), (TRAY_BASE_Z + rim_h + 10),
           "WATER LEVEL\n(6mm FLOOD)", fs=6.5, color=C_BLUE)

    leader(ax4a, (150), (WK_DECK_H - WK_GRATE_T/2),
           (330), (155),
           "WALKWAY GRATING\n(WALL-CANTILEVERED)", fs=6, color="#8D6E63")

    leader(ax4a, (250), (TRAY_BASE_Z / 2),
           (350), (TRAY_BASE_Z + rim_h /2 + 10),
           f"HDPE SHIM STRIP\n({PROC_TRAY_SHIM_W}mm WIDE,\n{PROC_TRAY_SUMP_Z}-{PROC_TRAY_SUMP_Z + PROC_TRAY_SHIM_H}mm)", fs=6, color="#A09070")

    # Slope note
    ax4a.text((360), (-40),
              f"FALL: {PROC_TRAY_PITCH}mm / {PROC_TRAY_D}mm (1:220)\n"
              f"SLOPE EXAGGERATED {SLOPE_EXAG_A:.0f}x",
              ha="center", va="center", fontsize=6, color="#0D47A1",
              bbox=dict(fc="white", ec="#0D47A1", lw=0.5, pad=2, alpha=0.9),
              zorder=8)

    # ═════════════════════════════════════════════════════════════════════════════
    # PANEL B — FULL CROSS-SECTION ELEVATION (~1:15)
    # Yd = -20 to 1150mm, Z = -50 to 1150mm
    # Shows tray, sump, suction hose routing to equipment panel (Yd=1046)
    # ═════════════════════════════════════════════════════════════════════════════
    SC_B = 1.0
    OB_X = 0
    OB_Y = 0



    ax4b.set_xlim((-26), (1162))
    ax4b.set_ylim((-66), (638))

    # Panel B title
    ax4b.text((550), (650), "SECTION A-A — SUMP TO CORRIDOR PLUMBING PANEL (AXES IN mm)",
              ha="center", va="top", fontsize=10, fontweight="bold",
              color="#1A237E", zorder=10)

    # ── Container structure ──────────────────────────────────────────────────────
    # Floor
    ax4b.add_patch(plt.Rectangle(((-20), (-FLOOR_T)),
                  1180 / SC_B, FLOOR_T / SC_B,
                  fc="#B0B0B8", ec=C_FRAME, lw=1.5, zorder=2, hatch=".."))

    # ── Shim strips (visible as small rectangles on floor) ───────────────────────
    # Shims start at TRAY_BASE_Z (20mm) at near end and add slope on top
    SLOPE_EXAG_B = 8.0
    for shim_yd in [130, 250, 370, 490]:
        sh_h = TRAY_BASE_Z + (shim_yd - tray_yd_near) * slope_per_mm * SLOPE_EXAG_B
        ax4b.add_patch(plt.Rectangle(((shim_yd - 8), (0)),
                      16 / SC_B, max(sh_h, 1) / SC_B,
                      fc="#E8DCC0", ec="#A09070", lw=0.6, zorder=3))

    # ── Tray ─────────────────────────────────────────────────────────────────────
    tray_z_near_b = TRAY_BASE_Z  # 20mm — raised by sump depth
    tray_z_far_b = TRAY_BASE_Z + (550 - tray_yd_near) * slope_per_mm * SLOPE_EXAG_B

    # Tray floor
    ax4b.fill([(tray_yd_near), (550), (550), (tray_yd_near)],
              [(tray_z_near_b), (tray_z_far_b),
               (tray_z_far_b + TRAY_T * 5), (tray_z_near_b + TRAY_T * 5)],
              fc="#C8D8E8", ec=C_FRAME, lw=1.2, zorder=4)

    # Near rim — from tray floor (Z=20) up by rim height
    ax4b.add_patch(plt.Rectangle(((tray_yd_near - 3), (TRAY_BASE_Z)),
                  6 / SC_B, rim_h / SC_B,
                  fc="#C8D8E8", ec=C_FRAME, lw=1.2, zorder=4))

    # ── Sump well (simplified at this scale) ────────────────────────────────────
    # Sump bottom at Z=0, tray floor at Z=TRAY_BASE_Z (20mm)
    sump_yd_b = PROC_TRAY_DRAIN_YD
    ax4b.add_patch(plt.Rectangle(((sump_yd_b), (0)),
                  PROC_TRAY_SUMP_D / SC_B, PROC_TRAY_SUMP_Z / SC_B,
                  fc="#B3D9F2", ec=C_FRAME, lw=1.2, alpha=0.6, zorder=5))

    # Pickup tube (simplified) — from sump floor+5 to above rim
    tube_yd_b = sump_yd_b + PROC_TRAY_SUMP_D / 2
    RIM_TOP_B = TRAY_BASE_Z + rim_h  # 70mm
    tube_z_top_b = WK_DECK_H + WK_GRATE_T + 10  # 135mm — above walkway grate + clearance
    draw_pipe_path(ax4b, [tube_yd_b, tube_yd_b], [5, tube_z_top_b],
                   TUBE_OD, TUBE_WALL,
                   fc="#D0D0D0", ec=C_FRAME, zorder=5)
    ax4b.text((tube_yd_b/2), (RIM_TOP_B + 85), "PICKUP\nTUBE",
              ha="left", va="bottom", fontsize=5.5, color=C_FRAME,
              fontweight="bold", zorder=6)

    # ── Suction hose from pickup, along tray rim exterior to equipment panel ─────
    P04_Z = PUMP_H_LO + 80  # P-04 on equipment panel
    PANEL_YD = 1046           # equipment panel Yd position
    RIM_EXT_YD_B = tray_yd_near - HOSE_OD / 2 - 5  # ~60mm — hose CL on rim exterior
    HOSE_RIM_Z_B = TRAY_BASE_Z + rim_h / 2 - 25    # ~20mm — lowered to clear cantilever brackets

    # Hose path: short vertical overlap with tube top (creates 90° elbow) →
    # horizontal above walkway → 90° elbow → down along rim exterior
    ELBOW_OVERLAP_B = HOSE_OD
    hose_b_y = [tube_yd_b, tube_yd_b, RIM_EXT_YD_B, RIM_EXT_YD_B]
    hose_b_z = [tube_z_top_b - ELBOW_OVERLAP_B, tube_z_top_b, tube_z_top_b, HOSE_RIM_Z_B]
    draw_pipe_path(ax4b, hose_b_y, hose_b_z, HOSE_OD, HOSE_WALL,
                   fc=C_BROWN, ec="#5A3020", zorder=4)

    # Pipe end-on at rim exterior (hose runs along X — into the page toward IBC corner)
    pipe_r_b = HOSE_OD / 2 / SC_B
    pipe_wall_b = HOSE_WALL / SC_B
    draw_pipe_end(ax4b, (RIM_EXT_YD_B), (HOSE_RIM_Z_B),
                  pipe_r_b, pipe_wall_b,
                  fc=C_BROWN, ec=C_FRAME, bore_fc="white", zorder=6)

    # Dashed routing indicator from rim to equipment panel (truncated to view range)
    ROUTE_Z_TOP = 500
    ax4b.plot([(RIM_EXT_YD_B), (PANEL_YD)],
              [(HOSE_RIM_Z_B), (ROUTE_Z_TOP)],
              color=C_BROWN, lw=1.0, ls=":", zorder=3, alpha=0.6)
    ax4b.text(((RIM_EXT_YD_B + PANEL_YD) / 2), ((HOSE_RIM_Z_B + ROUTE_Z_TOP) / 2 + 30),
              "HOSE ALONG RIM →\nCROSSES AT IBC CORNER\n(SEE PLAN VIEW)",
              ha="center", va="bottom", fontsize=5.5, color=C_BROWN,
              style="italic", zorder=4)

    # ── Near walkway (Yd=0-300) ──────────────────────────────────────────────────
    ax4b.add_patch(plt.Rectangle(((0), (WK_DECK_H - WK_GRATE_T)),
                  WALKWAY_W / SC_B, WK_GRATE_T / SC_B,
                  fc="#E0D6C8", ec="#8D6E63", lw=1.0, hatch="///", zorder=3,
                  alpha=0.7))

    # ── Equipment panel destination (schematic, within view range) ───────────────
    # The equipment panel is at Yd=1046, Z=1370–2270 — far above this view's
    # Z range (0–620).  Show a compact representation at the top of the view
    # with the plywood strip truncated and a destination leader.
    EP_Z_TOP = 580   # truncated top within view
    ax4b.add_patch(plt.Rectangle(((PANEL_YD - 9), (0)),
                  18 / SC_B, EP_Z_TOP / SC_B,
                  fc="#D4C8A0", ec="#A09060", lw=1.5, zorder=3))

    # Break marks (zigzag) at truncation
    brk_z = EP_Z_TOP
    brk_w = 30
    for side in [-1, 1]:
        bx = PANEL_YD + side * 9
        ax4b.plot([(bx - brk_w/2), (bx), (bx + brk_w/2)],
                  [(brk_z - 8), (brk_z + 8), (brk_z - 8)],
                  color="#A09060", lw=1.2, zorder=4, clip_on=True)

    # Destination leader
    leader(ax4b, (PANEL_YD), (EP_Z_TOP),
           (PANEL_YD + 80), (EP_Z_TOP + 30),
           "CORRIDOR PLUMBING PANEL (Yd=1046)\n"
           "P-04 Shurflo 2088 (Z=1400)\n"
           "3W-DV-02 diverter → IBC-3 / IBC-4",
           fs=6, color=C_PUMP, ha="left")

    # ── Dimensions ───────────────────────────────────────────────────────────────
    # Rim top above floor
    draw_dim_v(ax4b, (tray_yd_near - 50), (0), (RIM_TOP_B),
               f"{int(RIM_TOP_B)}mm", offset=4.8, fs=6.5, right=False)

    # Walkway
    draw_dim_v(ax4b, (WALKWAY_W + 265), (0), (WK_DECK_H),
               f"{WK_DECK_H}mm", offset=4.8, fs=6, right=True)

    # ── Labels ───────────────────────────────────────────────────────────────────
    leader(ax4b, (WALKWAY_W/2), (WK_DECK_H),
           (200), (WK_DECK_H + 40),
           "WALKWAY", fs=6.5, color="#8D6E63")

    # ═════════════════════════════════════════════════════════════════════════════
    # PANEL C — PLAN VIEW: HOSE ROUTING ALONG TRAY RIM (~1:8)
    # Looking down (standard plan orientation matching floorplan/IBC sheets):
    #   Horizontal = X (left=cargo door, right=sealed end)
    #   Vertical   = Yd (bottom=near wall/pinhole, top=far wall)
    # Sump at bottom-right, pipe travels north to equipment panel.
    # ═════════════════════════════════════════════════════════════════════════════
    SC_C = 1.0

    SUMP_X = PROC_TRAY_DRAIN_X   # 4550mm
    TRAY_X_R = PROC_TRAY_X_R     # 4629mm
    IBC_X = IBC_COL_X             # 4674mm
    EP_X = EQPANEL_X              # 4874mm — equipment panel face X (v2 corridor mouth)
    EP_W = EQPANEL_W              # 148mm — total X footprint (panel + protrusion)

    X_VIEW_L = 4350
    X_VIEW_R = EP_X + EQPANEL_T + 80   # ~5098mm
    YD_VIEW_BOT = -30
    YD_VIEW_TOP = 1130



    ax4c.set_xlim((X_VIEW_L - 4), (X_VIEW_R + 4))
    ax4c.set_ylim((YD_VIEW_BOT - 4), (YD_VIEW_TOP + 4))

    # Panel C title
    ax4c.text(((X_VIEW_L + X_VIEW_R) / 2), (YD_VIEW_TOP + 15),
              "PLAN VIEW — HOSE ROUTING ALONG TRAY RIM (AXES IN mm)",
              ha="center", va="bottom", fontsize=9, fontweight="bold",
              color="#1A237E", zorder=10)

    # ── Container near wall (Yd=0, horizontal line at bottom) ─────────────────
    ax4c.add_patch(plt.Rectangle(((X_VIEW_L - 20), (-WALL_T)),
                  (X_VIEW_R - X_VIEW_L + 40) / SC_C, WALL_T / SC_C,
                  fc="#B0B0B8", ec=C_FRAME, lw=1.2, zorder=2, hatch=".."))

    # ── Tray outline (partial) ─────────────────────────────────────────────────
    tray_x_l_vis = max(PROC_TRAY_X_L, X_VIEW_L)
    ax4c.add_patch(plt.Rectangle(((tray_x_l_vis), (tray_yd_near)),
                  (TRAY_X_R - tray_x_l_vis) / SC_C,
                  (400 - tray_yd_near) / SC_C,
                  fc="#E8F0F8", ec="#C8D8E8", lw=1.0, zorder=2, alpha=0.4))
    ax4c.text(((tray_x_l_vis + TRAY_X_R) / 2), (200),
              "PROCESSING TRAY", ha="center", va="center",
              fontsize=6, color="#6A8CAF", style="italic", alpha=0.7, zorder=3)

    # Near rim line (Yd=80, runs along X — horizontal)
    ax4c.plot([(tray_x_l_vis), (TRAY_X_R)],
             [(tray_yd_near), (tray_yd_near)],
             color="#C8D8E8", lw=2.0, zorder=4)

    # Right rim line (X=4629, runs along Yd — vertical)
    ax4c.plot([(TRAY_X_R), (TRAY_X_R)],
             [(tray_yd_near), (400)],
             color="#C8D8E8", lw=2.0, zorder=4)

    # ── Sump (small rectangle inside tray at near rim) ─────────────────────────
    ax4c.add_patch(plt.Rectangle(
        ((SUMP_X - PROC_TRAY_SUMP_W / 2), (PROC_TRAY_DRAIN_YD)),
        PROC_TRAY_SUMP_W / SC_C, PROC_TRAY_SUMP_D / SC_C,
        fc="#B3D9F2", ec=C_FRAME, lw=1.0, zorder=5))
    ax4c.text((SUMP_X), (PROC_TRAY_DRAIN_YD + PROC_TRAY_SUMP_D / 2),
              "SUMP", ha="center", va="center", fontsize=5.5,
              fontweight="bold", color="#0D47A1", zorder=6)

    # ── Pickup tube end-on (vertical tube seen from above) ─────────────────────
    tube_r_c = TUBE_OD / 2 / SC_C
    tube_wall_c = TUBE_WALL / SC_C
    draw_pipe_end(ax4c, (SUMP_X), (tube_yd),
                  tube_r_c, tube_wall_c,
                  fc="#D0D0D0", ec=C_FRAME, bore_fc="white", zorder=7)

    # ── Equipment panel (spans corridor at X=EQPANEL_X, perpendicular to sealed end) ──
    ax4c.add_patch(plt.Rectangle(
        ((EP_X), (CORRIDOR_YD_NEAR - 9)),
        EQPANEL_T / SC_C, 270 / SC_C,
        fc="#D4C8A0", ec="#A09060", lw=1.5, zorder=3))
    ax4c.text((EP_X + EQPANEL_T / 2), (CORRIDOR_YD_NEAR - 65),
              f"CORRIDOR PLUMBING PANEL (X={int(EQPANEL_X)})",
              ha="center", va="bottom", fontsize=5.5, color=C_PUMP,
              style="italic", zorder=4)

    # P-04 on equipment panel — pump protrudes from panel face toward lower X
    P04_PLAN_X = EP_X - PUMP_D / 2
    ax4c.add_patch(plt.Circle(
        ((P04_PLAN_X), (CORRIDOR_YD_NEAR)),
        20 / SC_C,
        fc="#E8884A", ec=C_FRAME, lw=1.2, zorder=6))
    ax4c.text((P04_PLAN_X), (CORRIDOR_YD_NEAR + 35),
              "P-04", ha="center", va="center", fontsize=5.5,
              fontweight="bold", color="#E8884A", zorder=7)

    # ── Hose routing along tray rim exterior ───────────────────────────────────
    RIM_EXT_YD_C = tray_yd_near - HOSE_OD / 2 - 5  # ~60mm
    CORNER_X = TRAY_X_R + 15   # just past tray right edge
    draw_pipe_path(ax4c,
                   [SUMP_X, SUMP_X, CORNER_X, CORNER_X, P04_PLAN_X],
                   [tube_yd, RIM_EXT_YD_C, RIM_EXT_YD_C, CORRIDOR_YD_NEAR, CORRIDOR_YD_NEAR],
                   HOSE_OD, HOSE_WALL,
                   fc=C_BROWN, ec="#5A3020", zorder=6)

    # P-clip marks along rim run (small ticks — horizontal marks along vertical pipe)
    for clip_x in range(SUMP_X, CORNER_X, 60):
        ax4c.plot([(clip_x), (clip_x)],
                 [(RIM_EXT_YD_C - 8), (RIM_EXT_YD_C + 8)],
                 color="#666666", lw=0.6, zorder=5)

    # ── Labels ──────────────────────────────────────────────────────────────────
    leader(ax4c, (SUMP_X - 50), (RIM_EXT_YD_C),
           (X_VIEW_L + 50), (RIM_EXT_YD_C - 120),
           "1\" SUCTION HOSE\nALONG RIM EXTERIOR\n(P-CLIPPED TO RIM)", fs=6, color=C_BROWN)

    leader(ax4c, (CORNER_X), ((RIM_EXT_YD_C + CORRIDOR_YD_NEAR) / 2),
           (CORNER_X + 60), (500),
           "CROSSES TO\nCORRIDOR PLUMBING PANEL\nAT TRAY CORNER", fs=6, color=C_BROWN)

    # ── Dimensions ──────────────────────────────────────────────────────────────
    # Rim-to-panel Yd distance (vertical dim)
    draw_dim_v(ax4c, (X_VIEW_L - 5), (RIM_EXT_YD_C), (CORRIDOR_YD_NEAR),
               f"{CORRIDOR_YD_NEAR - RIM_EXT_YD_C:.0f}mm", offset=6.4, fs=6)

    # Hose run along rim (X distance — horizontal dim)
    draw_dim_h(ax4c, (SUMP_X), (CORNER_X),
               (RIM_EXT_YD_C - 50),
               f"{CORNER_X - SUMP_X}mm", offset=4, fs=6)

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
        "5. P-04: Shurflo 2088, 12V DC, self-priming, on the Corridor Plumbing Panel.",
        "6. Hose runs along tray rim exterior, P-clipped to rim.",
        "7. Tray slope exaggerated for clarity in elevation panels.",
    ]
    draw_notes(ax4_notes, notes4, 38, 9.25, spacing=1.1,
               fs=7, width=26, color=C_TEXT, title_color=C_TEXT,
               font={"fontfamily": "monospace"})

    flow_notes = [
        "FLOW PATH:",
        "1. Water drains by gravity to sump well (Yd=80mm)",
        "2. P-04 suction pickup draws from sump via foot valve",
        "3. 1\" hose along rim exterior to tray corner, then to equip panel",
        "4. P-04 discharge to 3W-DV-02 three-way diverter",
        "5. Default: lifts to IBC-3 side-entry (Brown, ~900mm head)",
        "6. Alt: divert to IBC-4 (Waste) when selected",
    ]
    draw_notes(ax4_notes, flow_notes, 70, 9.25, spacing=1.1,
               fs=7, width=26, color=C_TEXT, title_color=C_TEXT,
               font={"fontfamily": "monospace"})


    _save(fig4, "water-system-sheet4")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    draw_sheet1()
    draw_sheet2()
    draw_sheet3()
    draw_sheet4()
