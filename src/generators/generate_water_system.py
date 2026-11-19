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
from tbs_constants import C_LEN, C_WID, WALL_T, CORRIDOR_YD_NEAR, CORRIDOR_W, EQPANEL_T, BB_OD, PWP_PANEL_X0, PWP_PANEL_X1, PWP_FILTER_X1, PWP_FILTER_X2, PWP_FILTER_X3, PWP_FILTER_YD, TAP_X, SPRAY_BEAM_X_L, SPRAY_BEAM_X_R, SPRAY_BEAM_SPAN, PROC_TRAY_YD_FAR, C_HGT, IBC_COL_X, IBC_W, IBC_D, ZONE_L_END, ZONE_R_START, BLUE_IBC_Y, IBC_FAR_Y, PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_W, PROC_TRAY_D, PROC_TRAY_YD_NEAR, PROC_TRAY_RIM, PROC_TRAY_PITCH, PROC_TRAY_DRAIN_X, PROC_TRAY_DRAIN_YD, PROC_TRAY_SUMP_W, PROC_TRAY_SUMP_D, PROC_TRAY_SUMP_Z, PROC_TRAY_SHIM_H, PROC_TRAY_SHIM_W, WALKWAY_W, WALKWAY_NEAR_YD, WALKWAY_FAR_YD, C_BLUE_IBC, C_BROWN_IBC, C_WASTE_IBC, C_PUMP, DIAGRAMS_DIR
import os
from tbs_title_block import title_block
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "models"))
import generate_corridor_water_panel as cwp
from tbs_drawing import (draw_dim_h, draw_dim_v, leader, draw_notes, draw_mixed_pipe,
                         draw_pipe_path as _tbs_pipe_path,
                         draw_pipe_end as _tbs_pipe_end)
from tbs_constants import DIAGRAM_DPI, C_DIM, C_PIPE_FRESH, C_PIPE_RECYCLE, C_PIPE_WASTE

# ── Color palette ────────────────────────────────────────────────────────────
C_BLUE   = C_PIPE_FRESH     # clean water — Blue system
C_BROWN  = C_PIPE_RECYCLE   # used / recycled water — Brown system
C_BLACK  = C_PIPE_WASTE     # waste water — Black system
C_BLUE_L = "#D6E9F8"   # blue system fill (light)
C_BROWN_L= "#F0E0CC"   # brown system fill (light)
C_BLACK_L= "#DDDDDD"   # black system fill (light)
C_PROC   = "#E8F5E9"   # processing area fill
C_FILT   = "#FFF9C4"   # filter skid fill
C_FRAME  = "#444444"   # drawing frame
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

def box(ax, x, y, w, h, fc="white", ec=C_FRAME, lw=1.2, zorder=2, radius=0.5):
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
    leg_h = 0.75
    for dx in [-w/2 + 0.5, w/2 - 0.5]:
        ax.plot([x + dx, x + dx], [y - h/2 - leg_h, y - h/2],
                color=ec, lw=lw, zorder=zorder)
    # label
    if label:
        ax.text(x - 12.5, y + 13.75, label, ha="center", va="center",
                fontsize=7.5, fontweight="bold", color=C_TEXT, zorder=zorder + 1)
    if sublabel:
        ax.text(x, y - 1.5, sublabel, ha="center", va="center",
                fontsize=6.5, color="#555555", zorder=zorder + 1)

def pump(ax, x, y, color=C_BLUE, zorder=5, r=2.8125):
    """Draw a centrifugal pump symbol (circle with triangle arrow)."""
    circ = plt.Circle((x, y), r, fc="white", ec=color, lw=2.8, zorder=zorder)
    ax.add_patch(circ)
    # Triangle inside
    tri = plt.Polygon([(x - r*0.55, y - r*0.55),
                       (x - r*0.55, y + r*0.55),
                       (x + r*0.65, y)],
                      fc=color, ec=color, zorder=zorder + 1)
    ax.add_patch(tri)

def valve(ax, x, y, color=C_BLUE, zorder=5, size=1.5, label="V"):
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

def flex_conn(ax, x, y, color=C_BLUE, zorder=7, n=4, amp=1.5, length=7.5, horiz=False):
    """Flexible-connector symbol — a short coil marking the 1" flex jumper fitted at
    each IBC tote penetration. It de-couples the fixed tote from the semi-rigid
    plumbing panel so the solvent-weld PVC joints don't fatigue over time."""
    t = np.linspace(0, 1, 60)
    if horiz:
        xs = x - length / 2 + t * length
        ys = y + amp * np.sin(2 * np.pi * n * t)
    else:
        ys = y - length / 2 + t * length
        xs = x + amp * np.sin(2 * np.pi * n * t)
    ax.plot(xs, ys, color=color, lw=1.8, zorder=zorder, solid_capstyle="round")

def diverter(ax, x, y, color=C_BLUE, zorder=5, size=1.875, branch="up", label="DV"):
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

def check_valve(ax, x, y, dx, dy, color=C_BROWN, zorder=6, size=2.125):
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
    size = 3.15
    h    = 4.05
    pts  = [(x, y + h*0.6),
            (x + size*0.7, y + h*0.2),
            (x + size*0.5, y - h*0.5),
            (x - size*0.5, y - h*0.5),
            (x - size*0.7, y + h*0.2)]
    poly = plt.Polygon(pts, fc=color, ec=C_FRAME, lw=1.5, zorder=zorder)
    ax.add_patch(poly)
    ax.text(x, y, label, ha="center", va="center", fontsize=6.4, zorder=zorder + 1,
            fontweight="bold")

def ext_port(ax, x, y, color=C_BLUE, zorder=5, label="F1", size=3):
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

def pipe_bridge(ax, x, y, direction='h', r=3.5, color=C_FRAME, lw=LW_PIPE,
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
    ax1.set_xlim(0, 450)
    ax1.set_ylim(0, 300)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_facecolor("#F5F5F0")
    fig1.patch.set_facecolor("#F5F5F0")

    # ── Title block ───────────────────────────────────────────────────────────────
    ax1.add_patch(plt.Rectangle((0, 0), 450, 300, fc="#F5F5F0", ec=C_FRAME, lw=2))
    title_block(ax1, f"SHEET 1 OF {TOTAL_SHEETS}",
                drawing_title="WATER SYSTEM",
                subtitle="System flow schematic (P&ID) — closed recycle loop",
                scale_note="Not to scale",
                doc_id="TBS-001 · Water System")

    # ── Zone fills ────────────────────────────────────────────────────────────────
    ax1.add_patch(plt.Rectangle((7.5, 32.5), 112.5, 235, fc=C_BLUE_L, ec=C_BLUE, lw=1.5, alpha=0.45, zorder=1))
    ax1.text(63.75, 262.5, "BLUE — CLEAN WATER (ISOLATED)", ha="center", fontsize=8, fontweight="bold", color=C_BLUE, zorder=5)
    ax1.add_patch(plt.Rectangle((127.5, 32.5), 112.5, 235, fc=C_BROWN_L, ec=C_BROWN, lw=1.5, alpha=0.45, zorder=1))
    ax1.text(183.75, 262.5, "BROWN — USED WATER (BUFFER · FILTERS · RECYCLED SPRAY)", ha="center", fontsize=7.2, fontweight="bold", color=C_BROWN, zorder=5)
    ax1.add_patch(plt.Rectangle((247.5, 32.5), 87.5, 235, fc=C_BLACK_L, ec=C_BLACK, lw=1.5, alpha=0.35, zorder=1))
    ax1.text(291.25, 262.5, "BLACK — WASTE WATER", ha="center", fontsize=8, fontweight="bold", color=C_BLACK, zorder=5)
    ax1.add_patch(plt.Rectangle((340, 32.5), 102.5, 235, fc=C_PROC, ec="#388E3C", lw=1.5, alpha=0.6, zorder=1))
    ax1.text(391.25, 262.5, "PROCESSING AREA", ha="center", fontsize=8, fontweight="bold", color="#2E7D32", zorder=5)

    # ── Shared geometry + the FOUR well-separated horizontal run lanes ────────────
    W_X = 291.25; W_Y = 187.5; W_W = 35; W_H = 35
    VR = 2.4; PR = 2.8125; DVR = 3
    L_FEED  = 60    # DV-02 -> filter feed (low, below the skid)
    L_RECY  = 111.25    # recycled-brown spray (ACC-02 -> selector)
    L_FRESH = 127.5    # blue fresh supply (ACC-01 -> chem prep + selector)
    L_DVREC = 153.75    # DV-01 recycle -> IBC-3 buffer (dashed)
    WASTE_LO = 76.25   # DV-02 heavy-contam waste run (= DV02_Y, so the black branch runs straight, no dog-leg)
    IBC3_RISER = 192.5
    WRX = W_X - W_W / 2 - 7.5       # waste inflow riser X — just LEFT of IBC-4 (outside the wall), so it elbows IN
    SEL_X, SEL_Y = 342.5, L_FRESH    # selector on the fresh line (blue enters straight — no dog-leg)

    # ═══ BLUE SYSTEM — clean, fully ISOLATED from recycle/waste ═════════════════════
    tank(ax1, 37.5, 187.5, 35, 35, fc="#BBDEFB", ec=C_BLUE_IBC, lw=2, label="IBC-1", sublabel="264 gal (1000L)\nCLEAN A (~900L)")
    tank(ax1, 82.5, 187.5, 35, 35, fc="#BBDEFB", ec=C_BLUE_IBC, lw=2, label="IBC-2", sublabel="264 gal (1000L)\nCLEAN B (~900L)")

    ext_port(ax1, 37.5, 241.25, color=C_BLUE, label="X1")
    ax1.text(37.5, 249.5, "EXT. FILL\n2\" NPT\nGRAVITY", ha="center", fontsize=5.5, color=C_BLUE, style="italic")
    pipe(ax1, 37.5, 238.25, 37.5, 227, C_BLUE)
    check_valve(ax1, 37.5, 234.5, 0, -25, color=C_BLUE)
    ax1.text(32, 234.5, "CV-1", ha="right", va="center", fontsize=5.5, color=C_BLUE)
    pipe(ax1, 37.5, 227, 72.5, 227, C_BLUE); ax1.plot([37.5], [227], "o", ms=4.5, color=C_BLUE, zorder=6)
    pipe(ax1, 37.5, 227, 37.5, 205, C_BLUE); arrow_pipe(ax1, 37.5, 210.5, 37.5, 207.5, color=C_BLUE)
    pipe(ax1, 72.5, 227, 72.5, 205, C_BLUE); arrow_pipe(ax1, 72.5, 210.5, 72.5, 207.5, color=C_BLUE)
    ax1.text(58, 238, "X1 FILL TEE → IBC-1 & IBC-2\n(fill only — no recycle)", ha="center", fontsize=5.2, color=C_BLUE, style="italic")

    pipe(ax1, 55, 178.75, 65, 178.75, C_BLUE); ax1.plot([55, 65], [178.75, 178.75], "o", ms=3.5, color=C_BLUE, zorder=6)
    pipe(ax1, 37.5, 169.5, 37.5, 166.25, C_BLUE); pipe(ax1, 37.5, 166.25, 60 - VR, 166.25, C_BLUE)
    pipe(ax1, 82.5, 169.5, 82.5, 166.25, C_BLUE); pipe(ax1, 82.5, 166.25, 60 + VR, 166.25, C_BLUE)
    ax1.text(60, 175.5, 'IBC-1 & IBC-2 PARALLEL (shared BV-01 · 1" equalization tie)', ha="center", fontsize=5.2, color=C_BLUE, style="italic")
    valve(ax1, 60, 166.25, color=C_BLUE)
    ax1.text(64, 164, "BV-01", ha="left", va="center", fontsize=6, color=C_BLUE)
    pipe(ax1, 60, 166.25 - VR, 60, 153.75 + PR, C_BLUE); arrow_pipe(ax1, 60, 162, 60, 159, color=C_BLUE)
    pump(ax1, 60, 153.75, color=C_PUMP); ax1.text(65.5, 152.5, "P-01\n12VDC\n3.5 GPM", ha="left", fontsize=6, color=C_PUMP)
    pipe(ax1, 60, 153.75 - PR, 60, 140.5 + 5.25, C_BLUE)
    box(ax1, 60, 140.5, 20, 10.5, fc="#E3F2FD", ec=C_BLUE, lw=1.5); ax1.text(60, 140.5, "ACC-01\n1 GAL", ha="center", va="center", fontsize=6, color=C_BLUE)

    # ACC-01 outlet leaves the BOTTOM edge, drops clear, then dog-legs east onto the fresh-supply run
    pipe(ax1, 60, 140.5 - 5.25, 60, L_FRESH, C_BLUE); arrow_pipe(ax1, 60, 133.25, 60, 130, color=C_BLUE)
    pipe(ax1, 60, L_FRESH, SEL_X - 3.5, L_FRESH, C_BLUE)
    pipe_bridge(ax1, 160, L_FRESH, color=C_BLUE, lw=LW_PIPE, bg=C_BROWN_L)     # over the P-02/ACC-02 riser
    pipe_bridge(ax1, 242.5, L_FRESH, color=C_BLUE, lw=LW_PIPE, bg=C_BROWN_L)     # over DV-01 recycle riser
    pipe_bridge(ax1, WRX, L_FRESH, color=C_BLUE, lw=LW_PIPE, bg=C_BLACK_L)     # over waste riser
    ax1.text(76.25, L_FRESH + 5, '1" BLUE — FRESH SUPPLY', ha="left", fontsize=6.8, color=C_BLUE)

    # TAP-01 chem prep — RAISED to a short drop just below the fresh line, clear of every
    # brown/black horizontal (chem prep needs clean water, so it stays high on the isolated blue line)
    TAP_X = 315
    pipe(ax1, TAP_X, L_FRESH, TAP_X, 122 + VR, C_BLUE)
    valve(ax1, TAP_X, 122, color=C_BLUE)
    ax1.text(TAP_X + 5, 123.5, "BV-04", ha="left", va="center", fontsize=6, color=C_BLUE)
    pipe(ax1, TAP_X, 122 - VR, TAP_X, 117.5, C_BLUE)
    ax1.plot([TAP_X - 4.5, TAP_X + 4.5, TAP_X, TAP_X - 4.5], [117.5, 117.5, 114, 117.5], color=C_BLUE, lw=2.0, solid_capstyle="round", zorder=5)
    ax1.add_patch(plt.Circle((TAP_X, 112.25), 1.55, fc="white", ec=C_BLUE, lw=1.6, zorder=6))   # OPEN egress point
    ax1.text(TAP_X - 20, 115, "TAP-01\n(CHEM PREP)", ha="left", va="center", fontsize=5.6, color=C_BLUE)

    # ═══ BROWN SYSTEM — buffer + recycled-spray pump ═══════════════════════════════
    tank(ax1, 160, 205, 35, 35, fc="#D7CCC8", ec=C_BROWN_IBC, lw=2, label="IBC-3", sublabel="264 gal (1000L)\nUSED BUFFER")

    # IBC-3 inflow = DV-01 recycle ONLY
    pipe(ax1, IBC3_RISER, L_DVREC, IBC3_RISER, 213.75, C_BROWN, style="--"); arrow_pipe(ax1, IBC3_RISER, 197.5, IBC3_RISER, 205, color=C_BROWN)
    pipe(ax1, IBC3_RISER, 213.75, 177.5, 213.75, C_BROWN, style="--"); arrow_pipe(ax1, 183.75, 213.75, 179, 213.75, color=C_BROWN)
    ax1.text(IBC3_RISER + 3.5, 218.5, "RECYCLE IN\n(from DV-01)", ha="left", va="center", fontsize=5.2, color=C_BROWN, style="italic")

    TAP_Y = 172.5
    pipe(ax1, 160, 187.5, 160, TAP_Y, C_BROWN); ax1.plot([160], [TAP_Y], "o", ms=4.5, color=C_BROWN, zorder=6)
    ax1.text(165.5, 178.75, "IBC-3 BOTTOM TAP (→ P-02 + P-05)", ha="left", va="center", fontsize=5.0, color=C_BROWN, style="italic")

    # P-02 recycled-spray leg: BV-03 → P-02 → ACC-02 → recycled-spray run → selector
    pipe(ax1, 160, TAP_Y, 160, 157.5 + VR, C_BROWN)
    valve(ax1, 160, 157.5, color=C_BROWN)
    ax1.text(164, 157.5, "BV-03", ha="left", fontsize=6, color=C_BROWN)
    pipe(ax1, 160, 157.5 - VR, 160, 143.75 + PR, C_BROWN)
    arrow_pipe(ax1, 160, 151.25, 160, 148, color=C_BROWN)
    pump(ax1, 160, 143.75, color=C_PUMP)
    ax1.text(165, 142, "P-02\n12VDC\n3.5 GPM", ha="left", fontsize=6, color=C_PUMP)
    pipe(ax1, 160, 143.75 - PR, 160, 117.5 + 5.25, C_BROWN)
    box(ax1, 160, 118.5, 20, 10.5, fc="#EFEBE9", ec=C_BROWN, lw=1.5, zorder=3)
    ax1.text(160, 118.5, "ACC-02\n1 GAL", ha="center", va="center", fontsize=6, color=C_BROWN)
    pipe(ax1, 160, 117.5 - 5.25, 160, L_RECY, C_BROWN)
    pipe(ax1, 160, L_RECY, SEL_X, L_RECY, C_BROWN)
    pipe_bridge(ax1, 242.5, L_RECY, color=C_BROWN, lw=LW_PIPE, bg=C_BROWN_L)     # under DV-01 recycle riser
    pipe_bridge(ax1, WRX, L_RECY, color=C_BROWN, lw=LW_PIPE, bg=C_BLACK_L)     # over waste riser
    arrow_pipe(ax1, 322.5, L_RECY, 332.5, L_RECY, color=C_BROWN)
    ax1.text(172.5, L_RECY + 4.25, '1" BROWN — RECYCLED SPRAY', ha="left", fontsize=6.2, color=C_BROWN)

    # P-05 buffer drain-out → exterior port X3
    BD_X = 133.75
    pipe(ax1, 160, TAP_Y, BD_X, TAP_Y, C_BROWN)
    pipe(ax1, BD_X, TAP_Y, BD_X, 188.75, C_BROWN)
    valve(ax1, BD_X, 191.25, color=C_BROWN); ax1.text(BD_X - 3.75, 190.5, "BV-02", ha="right", fontsize=6, color=C_BROWN)
    pipe(ax1, BD_X, 193.75, BD_X, 207.5 - PR, C_BROWN)
    pump(ax1, BD_X, 207.5, color=C_PUMP); ax1.text(BD_X - 3.75, 205, "P-05\n12VDC", ha="right", fontsize=6, color=C_PUMP)
    pipe(ax1, BD_X, 207.5 + PR, BD_X, 237.5, C_BROWN); arrow_pipe(ax1, BD_X, 232.5, BD_X, 236.25, color=C_BROWN)
    ext_port(ax1, BD_X, 241.25, color=C_BROWN, label="X3")
    ax1.text(BD_X + 2, 249.5, "EXT. DRAIN\n2\" NPT", ha="center", fontsize=5.5, color=C_BROWN, style="italic", va="bottom")

    # ═══ FILTER SKID (compact) — fed by DV-02 (P-04-driven); out via SV-01 → DV-01 ══
    ax1.add_patch(plt.Rectangle((130, 76.25), 95, 30, fc=C_FILT, ec="#F57F17", lw=1.5, alpha=0.8, zorder=1))
    ax1.text(177.5, 103, "FILTER SKID", ha="center", fontsize=7, fontweight="bold", color="#E65100")
    filter_sym(ax1, 150, 90, label="F1"); filter_sym(ax1, 177.5, 90, label="F2"); filter_sym(ax1, 205, 90, label="F3")
    ax1.text(150 + 4, 90, "5μm", ha="left", va="center", fontsize=5.4, color="#E65100")
    ax1.text(177.5 + 4, 90, "KDF-55", ha="left", va="center", fontsize=5.4, color="#E65100")
    ax1.text(205 + 4, 90, "GAC", ha="left", va="center", fontsize=5.4, color="#E65100")

    # feed into F1 bottom, serpentine F1→F2→F3, out F3 top → SV-01 → DV-01
    pipe(ax1, 150, L_FEED, 150, 86, C_BROWN); arrow_pipe(ax1, 150, 76.25, 150, 81.25, color=C_BROWN)   # feed rises into F1
    pipe(ax1, 150, 94, 150, 98.75, C_BROWN); pipe(ax1, 150, 98.75, 177.5, 98.75, C_BROWN); arrow_pipe(ax1, 160, 98.75, 170, 98.75, color=C_BROWN)
    pipe(ax1, 177.5, 98.75, 177.5, 94, C_BROWN); pipe(ax1, 177.5, 86, 177.5, 81.25, C_BROWN)
    pipe(ax1, 177.5, 81.25, 205, 81.25, C_BROWN); arrow_pipe(ax1, 187.5, 81.25, 197.5, 81.25, color=C_BROWN)
    pipe(ax1, 205, 81.25, 205, 86, C_BROWN); pipe(ax1, 205, 94, 205, 98.75, C_BROWN)
    pipe(ax1, 205, 98.75, 221.25, 98.75, C_BROWN); arrow_pipe(ax1, 212.5, 98.75, 220, 98.75, color=C_BROWN)
    pipe(ax1, 221.25, 98.75, 221.25, 87.5, C_BROWN)

    valve(ax1, 221.25, 87.5, color="#F9A825", size=1.25, label="SV"); pipe(ax1, 221.25, 85.5, 221.25, 80.5, C_BROWN)
    ax1.add_patch(plt.Circle((221.25, 78.75), 1.375, fc="white", ec="#E65100", lw=1.5, zorder=6))   # OPEN sample-egress point
    ax1.text(221.25, 73, "SV-01 · pH tap", ha="center", va="top", fontsize=5.2, color="#E65100")
    pipe(ax1, 221.25, 87.5, 242.5 - DVR, 87.5, C_BROWN); arrow_pipe(ax1, 228.75, 87.5, 236.25, 87.5, color=C_BROWN)

    # ── DV-01 — recycle to IBC-3 buffer OR reject to IBC-4 ────────────────────────
    diverter(ax1, 242.5, 87.5, color="#777777", size=1.875, branch="up")
    ax1.text(242.5, 78.5, "3W-DV-01", ha="center", fontsize=6, color="#444")
    ax1.text(242.5, 73.75, "recycle→IBC-3 / reject→IBC-4 / off", ha="center", fontsize=5.0, color="#444", style="italic")
    pipe(ax1, 242.5, 87.5 + DVR, 242.5, L_DVREC, C_BROWN, style="--")   # riser passes UNDER the fresh/recycled runs (they hump over it)
    pipe(ax1, 242.5, L_DVREC, IBC3_RISER, L_DVREC, C_BROWN, style="--"); arrow_pipe(ax1, 215, L_DVREC, 205, L_DVREC, color=C_BROWN)
    ax1.text(217.5, L_DVREC + 4.5, "RECYCLE → IBC-3 BUFFER", ha="center", fontsize=5.6, color=C_BROWN, style="italic")
    pipe(ax1, 242.5 + DVR, 87.5, WRX, 87.5, C_BLACK)
    check_valve(ax1, 253, 87.5, 25, 0, color=C_BLACK)
    ax1.text(253, 82, "CV-2", ha="center", fontsize=5.2, color=C_BLACK)
    arrow_pipe(ax1, 260.5, 87.5, WRX - 1.5, 87.5, color=C_BLACK)
    ax1.text(262.5, 92.5, "REJECT → IBC-4", ha="center", fontsize=5.4, color=C_BLACK, style="italic")

    # ═══ BLACK SYSTEM — waste ══════════════════════════════════════════════════════
    tank(ax1, W_X, W_Y, W_W, W_H, fc="#D5D5D0", ec=C_WASTE_IBC, lw=2, label="IBC-4", sublabel="264 gal (1000L)\nWASTE")
    pipe(ax1, WRX, WASTE_LO, WRX, 187.5, C_BLACK)             # waste riser up the LEFT of IBC-4 (outside; fresh/recycled hump over it)
    arrow_pipe(ax1, WRX, 167.5, WRX, 175, color=C_BLACK)
    pipe(ax1, WRX, 187.5, W_X - W_W / 2 + 3, 187.5, C_BLACK) # elbow RIGHT into the IBC-4 left wall near the top
    arrow_pipe(ax1, W_X - W_W / 2 - 1.5, 187.5, W_X - W_W / 2 + 1.75, 187.5, color=C_BLACK)

    WD_X = 323.75
    pipe(ax1, W_X + W_W / 2, 195, WD_X - VR, 195, C_BLACK)
    valve(ax1, WD_X, 195, color=C_BLACK); ax1.text(WD_X + 3.75, 193.75, "BV-06", ha="left", fontsize=6, color=C_BLACK)
    pipe(ax1, WD_X, 195 + VR, WD_X, 217.5 - PR, C_BLACK)
    pump(ax1, WD_X, 217.5, color=C_PUMP); ax1.text(WD_X + 3.75, 216.25, "P-03\n12VDC", ha="left", fontsize=6, color=C_PUMP)
    pipe(ax1, WD_X, 217.5 + PR, WD_X, 237.5, C_BLACK); arrow_pipe(ax1, WD_X, 232.5, WD_X, 236.25, color=C_BLACK)
    ext_port(ax1, WD_X, 241.25, color=C_BLACK, label="X4")
    ax1.text(WD_X, 249.5, "EXT. DRAIN\n2\" NPT", ha="center", fontsize=5.5, color=C_BLACK, style="italic", va="bottom")

    flex_conn(ax1, 37.5, 215.5, color=C_BLUE); flex_conn(ax1, 72.5, 215.5, color=C_BLUE)
    flex_conn(ax1, 57.25, 178.75, color=C_BLUE, horiz=True, n=2, amp=0.875, length=3)   # 1" equalization tie — flex jumper at EACH tote
    flex_conn(ax1, 62.75, 178.75, color=C_BLUE, horiz=True, n=2, amp=0.875, length=3)
    flex_conn(ax1, 160, 181.25, color=C_BROWN); flex_conn(ax1, IBC3_RISER, 207.5, color=C_BROWN)
    flex_conn(ax1, WRX, 178.75, color=C_BLACK)                             # waste INFLOW flex — on the riser, OUTSIDE the wall
    flex_conn(ax1, W_X + W_W / 2 + 4.5, 195, color=C_BLACK, horiz=True)   # waste OUTLET flex — OUTSIDE the right wall

    # ── #29 — braided flex connector on BOTH ports of every pump (suction + discharge) ──
    #    Vibration isolation: a braided ½" jumper de-couples each pump from the rigid PVC run so the
    #    solvent-weld joints can't fatigue-crack. P-04's suction coil = the existing 1" tray-drain hose.
    _pf = dict(n=3, amp=1.05, length=4)
    flex_conn(ax1, 60, 160, color=C_BLUE, **_pf);  flex_conn(ax1, 60, 148.75, color=C_BLUE, **_pf)   # P-01 suction / discharge
    flex_conn(ax1, 160, 151.25, color=C_BROWN, **_pf); flex_conn(ax1, 160, 136.25, color=C_BROWN, **_pf)   # P-02 suction / discharge
    flex_conn(ax1, BD_X, 198.75, color=C_BROWN, **_pf); flex_conn(ax1, BD_X, 218.75, color=C_BROWN, **_pf)  # P-05 suction / discharge
    flex_conn(ax1, WD_X, 207, color=C_BLACK, **_pf); flex_conn(ax1, WD_X, 224.5, color=C_BLACK, **_pf)  # P-03 suction / discharge
    flex_conn(ax1, 390, 97, color=C_BROWN, **_pf); flex_conn(ax1, 390, 82.5, color=C_BROWN, **_pf)  # P-04 suction (1" tray hose) / discharge

    # ═══ PROCESSING AREA ═══════════════════════════════════════════════════════════
    ax1.add_patch(plt.Rectangle((342.5, 87.5), 95, 137.5, fc="#C8E6C9", ec="#388E3C", lw=1.5, zorder=2))
    ax1.text(390, 220, "PROCESSING TRAY (304 SS)", ha="center", fontsize=7.5, fontweight="bold", color="#2E7D32")
    ax1.text(390, 212.5, "(50mm rim, 1:200 pitch, permanent)", ha="center", fontsize=6.5, color="#388E3C")
    ax1.add_patch(plt.Rectangle((357.5, 125), 72.5, 77.5, fc="white", ec="#66BB6A", lw=1.2, ls="--", alpha=0.8, zorder=3))
    ax1.text(393.75, 163.75, f"PRINT\n({C_LEN} × {C_HGT}mm)", ha="center", va="center", fontsize=7, color="#388E3C", style="italic", zorder=4)
    ax1.add_patch(plt.Circle((390, 103.75), 3.75, fc="white", ec="#388E3C", lw=1.5, zorder=4))
    ax1.plot([386.25, 393.75], [103.75, 103.75], color="#388E3C", lw=1.2, zorder=5); ax1.plot([390, 390], [100, 107.5], color="#388E3C", lw=1.2, zorder=5)
    ax1.text(390, 110.5, "TRAY DRAIN", ha="center", fontsize=6, color="#388E3C")

    pipe(ax1, 390, 100, 390, 91.25 + PR, C_BROWN)
    pump(ax1, 390, 91.25, color=C_PUMP); ax1.text(395, 90, "P-04\n12VDC", ha="left", fontsize=6, color=C_PUMP)
    ax1.text(436.25, 118.75, "† P-04 drives F1→F3 —\n  verify head vs. 3× Δp\n  (Phase-2)", ha="right", va="top", fontsize=5.0, color="#555555", style="italic", zorder=6)

    pipe(ax1, 390, 85, 399.5, 85, C_BROWN)
    valve(ax1, 402, 85, color="#F9A825", size=1.25, label="SV"); pipe(ax1, 402, 83, 402, 78.5, C_BROWN)
    ax1.add_patch(plt.Circle((402, 76.75), 1.375, fc="white", ec="#E65100", lw=1.5, zorder=6))   # OPEN sample-egress point
    ax1.text(405.5, 82.5, "SV-02", ha="left", fontsize=6, color="#E65100")

    DV02_Y = 76.25
    pipe(ax1, 390, 91.25 - PR, 390, DV02_Y + DVR, C_BROWN)
    diverter(ax1, 390, DV02_Y, color="#777777", size=1.875, branch="left")
    ax1.text(392, 68, "3W-DV-02\nrecycle→filters / waste→IBC-4 / off", ha="left", fontsize=6, color="#444")
    # recycle leg (brown) — straight THROUGH DV-02 (down) → filter-feed run → F1.  This run now
    # crosses nothing (TAP-01 raised, waste routed above it), so it carries NO bridges.
    pipe(ax1, 390, DV02_Y - DVR, 390, L_FEED, C_BROWN)
    pipe(ax1, 390, L_FEED, 150, L_FEED, C_BROWN)
    arrow_pipe(ax1, 257.5, L_FEED, 247.5, L_FEED, color=C_BROWN)
    ax1.text(260, L_FEED - 5.5, "RECYCLE → FILTER SKID (P-04 drives F1→F3)", ha="center", fontsize=6, color=C_BROWN)
    # waste leg (black) — BRANCH off DV-02 (left) → STRAIGHT west to the waste riser (no dog-leg)
    pipe(ax1, 390 - DVR, DV02_Y, WRX, DV02_Y, C_BLACK)
    check_valve(ax1, 371.25, DV02_Y, -25, 0, color=C_BLACK)
    ax1.text(371.25, DV02_Y - 5, "CV-3", ha="center", fontsize=5.2, color=C_BLACK)
    arrow_pipe(ax1, 332.5, DV02_Y, 312.5, DV02_Y, color=C_BLACK)
    ax1.text(333.75, DV02_Y + 4, "WASTE → IBC-4 (HEAVY CONTAM.)", ha="center", fontsize=5.8, color=C_BLACK, style="italic")

    # ── 3-way SPRAY-SOURCE SELECTOR (replaces BV-05) ─────────────────────────────
    diverter(ax1, SEL_X, SEL_Y, color="#6A1B9A", size=2.125, branch="up")
    ax1.text(SEL_X - 4, SEL_Y + 13, "3W-BV-05", ha="right", fontsize=6.2, color="#6A1B9A", fontweight="bold")
    ax1.text(SEL_X - 4, SEL_Y + 8.75, "(SPRAY SELECT)", ha="right", fontsize=5.0, color="#6A1B9A", style="italic")
    arrow_pipe(ax1, SEL_X - 8.5, SEL_Y, SEL_X - 5, SEL_Y, color=C_BLUE)                    # blue fresh IN — straight, no dog-leg
    pipe(ax1, SEL_X, L_RECY, SEL_X, SEL_Y - 3.5, C_BROWN); arrow_pipe(ax1, SEL_X, 116.25, SEL_X, 120, color=C_BROWN)   # recycled brown IN — from below
    draw_mixed_pipe(ax1, [SEL_X, SEL_X, 422.5], [SEL_Y + 3.5, 200, 200], LW_PIPE)              # spray OUT — Blue OR Brown (selector)
    arrow_pipe(ax1, SEL_X, 165, SEL_X, 172.5, color=C_BLUE)
    for xd in [347.5, 362.5, 377.5, 392.5, 407.5, 420]:
        ax1.annotate("", xy=(xd, 192.5), xytext=(xd, 198.75), arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=1.5, mutation_scale=10), zorder=5)
    ax1.text(387.5, 205, "FLOOD/SPRAY BAR (3/4\" HDPE)", ha="center", fontsize=6.5, color=C_BLUE)

    # ═══ Legend + symbols (compact) ════════════════════════════════════════════════
    BOX_W = 112.5; BOX_H = 40.5; BOX_X = 7.5; BOX_Y = 12.5
    lx = BOX_X + 2.5; ly = BOX_Y + BOX_H - 5.5
    ax1.add_patch(plt.Rectangle((BOX_X, BOX_Y), BOX_W, BOX_H, fc="white", ec=C_FRAME, lw=1, zorder=6))
    ax1.text(BOX_X + BOX_W / 2, ly + 1.5, "LEGEND", ha="center", fontsize=7.5, fontweight="bold", color=C_TITLE, zorder=7)
    legend_items = [
        (C_BLUE,  "-",  "Blue  — Clean supply (1\" HDPE) — ISOLATED"),
        (C_BROWN, "-",  "Brown — Used / recycled water"),
        (C_BLACK, "-",  "Black — Waste water"),
        (C_BROWN, "--", "Dashed — Recycle / fill / return"),
        (None,    "mixed", "Blue or Brown (BV-05a selector)"),
    ]
    for i, (col, ls, lbl) in enumerate(legend_items):
        yy = ly - 3 - i * 5
        if ls == "mixed":
            draw_mixed_pipe(ax1, [lx, lx + 12.5], [yy, yy], 2.2, zorder=7)
        else:
            ax1.plot([lx, lx + 12.5], [yy, yy], color=col, lw=2.2, ls=ls, zorder=7)
        ax1.text(lx + 15.5, yy, lbl, va="center", fontsize=6.2, color=C_TEXT, zorder=7)

    SYM_X = 127.5
    ax1.add_patch(plt.Rectangle((SYM_X, BOX_Y), BOX_W, BOX_H, fc="white", ec=C_FRAME, lw=1, zorder=6))
    ax1.text(SYM_X + BOX_W / 2, ly + 1.5, "SYMBOLS", ha="center", fontsize=7.5, fontweight="bold", color=C_TITLE, zorder=7)
    syms = [
        ("P-xx / BV-xx", "Pump (12V DC) / manual ball valve"),
        ("3W-DV",        "3-way L-port diverter (3-pos: route A / route B / all-off)"),
        ("3W-BV-05",     "3-way selector — spray source"),
        ("SV-xx / ▷|",   "Sample tap · check valve (CV-1 fill; CV-2/3 anti-backflow)"),
        ("F1/F2/F3 · ⬡ · ∿ · ○", "Filter · port · flex · open egress/draw point"),
    ]
    for i, (sym, desc) in enumerate(syms):
        ax1.text(SYM_X + 3.75, ly - 2.5 - i * 6.375, f"{sym} — {desc}", va="center", fontsize=5.8, color=C_TEXT, zorder=7)

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
                scale_note="PLAN · AXES IN mm",
                doc_id="TBS-001 · Water System")

    # ── Plan view (X along the container, Yd from the pinhole wall), true mm ─────
    ax2.set_xlim(-420, C_LEN + 520)
    ax2.set_ylim(-960, C_WID + 640)
    ax2.set_aspect("equal")

    ax2.add_patch(plt.Rectangle((0, 0), C_LEN, C_WID, fc="white", ec=C_FRAME, lw=3, zorder=1))
    ax2.add_patch(plt.Rectangle((-WALL_T, -WALL_T), C_LEN + 2 * WALL_T, C_WID + 2 * WALL_T,
                                fc="none", ec="#777", lw=1.2, ls="--", zorder=0))
    ax2.text(C_LEN / 2, -640, f"CONTAINER INTERIOR — PLAN VIEW  ({C_LEN} × {C_WID}mm)",
             ha="center", fontsize=8, color=C_FRAME)

    # ── End zones ─────────────────────────────────────────────────────────────────
    ax2.add_patch(plt.Rectangle((0, 0), ZONE_L_END, C_WID, fc="#FFF3E0", ec="none", alpha=0.45, zorder=0))
    ax2.plot([ZONE_L_END, ZONE_L_END], [0, C_WID], color="#805000", lw=1.5, ls="--", zorder=6)
    ax2.text(ZONE_L_END - 25, C_WID + 470, f"LEFT END ZONE\nX=0–{ZONE_L_END}mm\n(light trap only)",
             ha="right", va="top", fontsize=6.5, color="#805000", fontweight="bold")
    ax2.add_patch(plt.Rectangle((ZONE_R_START, 0), C_LEN - ZONE_R_START, C_WID,
                                fc="#E8F0FF", ec="none", alpha=0.45, zorder=0))
    ax2.plot([ZONE_R_START, ZONE_R_START], [0, C_WID], color="#004080", lw=1.5, ls="--", zorder=6)
    ax2.text(ZONE_R_START + 25, C_WID + 470, f"RIGHT END ZONE\nX={ZONE_R_START}–{C_LEN}mm\n(4× IBC 2×2 stack)",
             ha="left", va="top", fontsize=6.5, color="#004080", fontweight="bold")

    # ── IBC stack (plan sees the top tier of each column) ─────────────────────────
    def ibc_plan(ax, x, y, fc, ec, label, sublabel=""):
        ax.add_patch(plt.Rectangle((x, y), IBC_W, IBC_D, fc=fc, ec=ec, lw=1.8, zorder=2))
        for xi in [x + IBC_W / 3, x + 2 * IBC_W / 3]:
            ax.plot([xi, xi], [y, y + IBC_D], color=ec, lw=0.6, alpha=0.5)
        for yi in [y + IBC_D / 3, y + 2 * IBC_D / 3]:
            ax.plot([x, x + IBC_W], [yi, yi], color=ec, lw=0.6, alpha=0.5)
        ax.text(x + IBC_W / 2, y + IBC_D / 2 + 60, label, ha="center", va="center",
                fontsize=7.5, fontweight="bold", color="#111", zorder=3)
        ax.text(x + IBC_W / 2, y + IBC_D / 2 - 110, sublabel, ha="center", va="center",
                fontsize=6.5, color="#555", zorder=3)

    ibc_plan(ax2, IBC_COL_X, BLUE_IBC_Y, "#BBDEFB", C_BLUE_IBC,
             "IBC-1 BLUE / IBC-3 BROWN", "Top: Blue ~900L clean\nBottom: Brown recycle")
    ibc_plan(ax2, IBC_COL_X, IBC_FAR_Y, "#BBDEFB", C_BLUE_IBC,
             "IBC-2 BLUE / IBC-4 WASTE", "Top: Blue ~900L clean\nBottom: Waste")

    # ── Corridor plumbing panel (between the IBC columns) — the 3D geometry ──────
    ax2.add_patch(plt.Rectangle((cwp.BACK_X, CORRIDOR_YD_NEAR), cwp.EQT, CORRIDOR_W,
                                fc=C_FILT, ec="#F57F17", lw=1.5, zorder=3))
    ax2.add_patch(plt.Circle((cwp.PXC, cwp.CTR_Y), cwp.ACC_R, fc=C_PUMP, ec="#805000", lw=1.2, alpha=0.6, zorder=3))
    leader(ax2, cwp.PXC - cwp.ACC_R, cwp.CTR_Y,
           3900, 1620,
           "CORRIDOR PLUMBING PANEL\nP-01/P-02/P-03/P-05 · ACC-01 (one column)\nBV-01/02/03/06",
           fs=6, color="#E65100", ha="center")

    # ── Processing tray (304 SS, two panels, 50mm rim) ───────────────────────────
    ax2.add_patch(plt.Rectangle((PROC_TRAY_X_L, PROC_TRAY_YD_NEAR), PROC_TRAY_W, PROC_TRAY_D,
                                fc=C_PROC, ec="#388E3C", lw=2, zorder=1, alpha=0.5))
    tray_mid_x = (PROC_TRAY_X_L + PROC_TRAY_X_R) / 2
    tray_mid_y = PROC_TRAY_YD_NEAR + PROC_TRAY_D / 2
    ax2.plot([tray_mid_x, tray_mid_x], [PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR],
             color="#388E3C", lw=1.2, ls="--", zorder=2)
    ax2.text(tray_mid_x - PROC_TRAY_W / 4, PROC_TRAY_YD_FAR - 90,
             f"PROCESSING TRAY (304 SS, {PROC_TRAY_RIM}mm RIM, 2 PANELS)",
             ha="center", va="top", fontsize=7, color="#2E7D32")
    for sgn, nm in ((-1, "A"), (1, "B")):
        ax2.text(tray_mid_x + sgn * PROC_TRAY_W / 4, tray_mid_y,
                 f"PANEL {nm}\n{PROC_TRAY_W / 2:.0f} × {PROC_TRAY_D}mm", ha="center", va="center",
                 fontsize=6, color="#388E3C")

    # Spray bar — a full-width beam that slides in Yd over the tray depth (single center feed)
    SB_YD = PROC_TRAY_YD_FAR - 420
    draw_mixed_pipe(ax2, [SPRAY_BEAM_X_L, SPRAY_BEAM_X_R], [SB_YD, SB_YD], 3)   # Blue OR Brown (BV-05a selector)
    ax2.text(tray_mid_x - PROC_TRAY_W / 4, SB_YD + 70,
             f"SPRAY BAR (3/4\" LDPE manifold on a {SPRAY_BEAM_SPAN}mm beam · single center feed)",
             ha="center", fontsize=7, color=C_BLUE)
    SB_ARR_X = PROC_TRAY_X_L + 350
    ax2.annotate("", xy=(SB_ARR_X, PROC_TRAY_YD_NEAR + 450), xytext=(SB_ARR_X, SB_YD - 40),
                 arrowprops=dict(arrowstyle="<|-|>", color=C_BLUE, lw=1.0, mutation_scale=10), zorder=4)
    ax2.text(SB_ARR_X + 50, (PROC_TRAY_YD_NEAR + 450 + SB_YD) / 2, "slides in Yd\n(near ↔ far rim)",
             ha="left", va="center", fontsize=6, color=C_BLUE, style="italic")

    # Tray sump at the center pickup (P-04 suction → 3W-DV-02)
    _sx0, _sy0 = PROC_TRAY_DRAIN_X - PROC_TRAY_SUMP_W / 2, PROC_TRAY_DRAIN_YD
    ax2.add_patch(plt.Rectangle((_sx0, _sy0), PROC_TRAY_SUMP_W, PROC_TRAY_SUMP_D,
                                fc="white", ec="#388E3C", lw=1.8, zorder=4))
    _sy = _sy0 + PROC_TRAY_SUMP_D / 2
    ax2.plot([_sx0, _sx0 + PROC_TRAY_SUMP_W], [_sy, _sy], color="#388E3C", lw=1.2, zorder=5)
    ax2.plot([PROC_TRAY_DRAIN_X, PROC_TRAY_DRAIN_X], [_sy0, _sy0 + PROC_TRAY_SUMP_D], color="#388E3C", lw=1.2, zorder=5)
    leader(ax2, PROC_TRAY_DRAIN_X, _sy0 + PROC_TRAY_SUMP_D, PROC_TRAY_DRAIN_X - 330, _sy + 560,
           "SUMP WELL\nP-04 PICKUP", fs=6, color="#388E3C", ha="center")

    # ── Pinhole-wall filter skid (on the wall above the tray: F1→F3, P-04, DV-02, ACC-02) ──
    ax2.add_patch(plt.Rectangle((PWP_PANEL_X0, 0), PWP_PANEL_X1 - PWP_PANEL_X0, EQPANEL_T,
                                fc=C_FILT, ec="#F57F17", lw=1.5, zorder=6))
    for fx in (PWP_FILTER_X1, PWP_FILTER_X2, PWP_FILTER_X3):
        ax2.add_patch(plt.Circle((fx, PWP_FILTER_YD), BB_OD / 2, fc="none", ec="#F57F17", lw=1.2, ls="--", zorder=6))
    leader(ax2, PWP_FILTER_X2, PWP_FILTER_YD + BB_OD / 2, PWP_FILTER_X2, 600,
           "PINHOLE-WALL FILTER SKID (above the tray)\nF1→F3 · P-04 · SV-02 · DV-02 · ACC-02",
           fs=6, color="#E65100", ha="center", va="bottom")

    # Chemistry prep tap — on the pinhole wall beside the chem shelf
    ax2.plot(TAP_X, 40, "v", color=C_BLUE, ms=10, zorder=8)
    ax2.plot([TAP_X, TAP_X], [40, 140], color=C_BLUE, lw=2.0, zorder=7)
    ax2.text(TAP_X, 230, "TAP-01\n(CHEM PREP)", ha="center", va="bottom", fontsize=5.5, color=C_BLUE, zorder=8)

    # Pinhole wall — BOTTOM of plan view (Yd=0 = near side, pinhole aperture wall)
    ax2.add_patch(plt.Rectangle((0, -WALL_T), C_LEN, WALL_T, fc="#BDBDBD", ec=C_FRAME, lw=2, zorder=5))
    ax2.text(C_LEN / 2, -110, "PINHOLE WALL (FRONT — Yd = 0)",
             ha="center", va="center", fontsize=6, color="#333", zorder=6)

    # Dimensions — using shared helpers from tbs_drawing.
    draw_dim_h(ax2, 0, C_LEN, -300, f"{C_LEN}mm (CONTAINER INTERIOR)", offset=100, fs=6.5, above=False)
    draw_dim_v(ax2, -200, 0, C_WID, f"{C_WID}mm", offset=120, fs=6.5, right=False)
    draw_dim_h(ax2, IBC_COL_X, IBC_COL_X + IBC_W, C_WID + 120, f"IBC col: {IBC_W}mm", offset=100, fs=6.5, above=True)
    draw_dim_h(ax2, 0, ZONE_L_END, C_WID + 120, f"LEFT END ZONE: {ZONE_L_END}mm", offset=100, fs=6.5, color="#805000", above=True)
    draw_dim_h(ax2, ZONE_R_START, C_LEN, C_WID + 560, f"RIGHT END ZONE: {C_LEN - ZONE_R_START}mm", offset=100, fs=6.5, color="#004080", above=True)

    # Orientation arrow — points toward pinhole wall (bottom, Yd=0)
    ax2.annotate("", xy=(C_LEN + 250, 200), xytext=(C_LEN + 250, 800),
                 arrowprops=dict(arrowstyle="-|>", color=C_FRAME, lw=1.5, mutation_scale=12))
    ax2.text(C_LEN + 250, 880, "FRONT\n(PINHOLE\nWALL)", ha="center", va="bottom", fontsize=6, color=C_FRAME)

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

    # Yd-only slope: FAR rim HIGH → NEAR rim LOW; the surface is LEVEL across X. The near-rim gutter
    # then falls 1:200 in X inward to the single CENTER pickup well at X=PROC_TRAY_DRAIN_X (2399).
    drain_local_x_s3 = PROC_TRAY_DRAIN_X - PROC_TRAY_X_L
    ax3.text((drain_local_x_s3), (-380), "CENTER PICKUP\n(SUMP WELL — LOW POINT)",
             ha="center", fontsize=7.5, fontweight="bold", color="#D32F2F")
    ax3.text((PROC_TRAY_W / 2), (PROC_TRAY_D + 120),
             "FAR RIM (HIGH)",
             ha="center", fontsize=7.5, fontweight="bold", color="#1565C0")
    ax3.text((PROC_TRAY_W * 0.22), (-70), "NEAR-RIM GUTTER (LOW)",
             ha="center", va="center", fontsize=6.5, color="#D32F2F", fontweight="bold")

    # ── Slope arrows (flow direction) ───────────────────────────────────────────
    # Yd-only fall: the main surface sheets straight toward the NEAR rim (−Yd), level across X; in the
    # near-rim gutter band the flow turns and runs in X to the single CENTER pickup well.

    ARROW_COLOR = "#1976D2"
    ARROW_ALPHA = 0.7

    # Drain position in tray-local coordinates (used by arrows and drain symbol)
    drain_local_x = PROC_TRAY_DRAIN_X - PROC_TRAY_X_L
    drain_local_yd = PROC_TRAY_DRAIN_YD - PROC_TRAY_YD_NEAR

    # Grid of flow arrows across the tray interior
    n_cols = 9
    n_rows = 5
    GUTTER_BAND = PROC_TRAY_D * 0.16     # near-rim gutter zone: below this Yd the flow turns to X
    for i in range(n_cols):
        for j in range(n_rows):
            # Position in tray-local mm
            ax_mm = PROC_TRAY_W * (i + 0.5) / n_cols
            ay_mm = PROC_TRAY_D * (j + 0.5) / n_rows

            # Yd-only slope: main floor sheets toward the near rim (−Yd); the near-rim gutter then
            # carries it in X to the center pickup.
            if ay_mm > GUTTER_BAND:
                dx_mm, dy_mm = 0.0, -1.0                     # straight down the fall to the near rim
            else:
                dx_mm, dy_mm = (drain_local_x - ax_mm), 0.0  # along the gutter to the center pickup

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
    # Yd-only fall 1:200 (far → near rim), LEVEL across X; the near-rim gutter falls 1:200 in X to the
    # single center pickup.
    yd_fall = PROC_TRAY_D / 200            # far-to-near fall over the tray depth
    gutter_fall = (PROC_TRAY_W / 2) / 200  # near-rim gutter fall from an X-edge in to the center pickup

    # Main-surface Yd-slope annotation
    ax3.text((PROC_TRAY_W * 0.5), (PROC_TRAY_D * 0.55),
             f"Yd-SLOPE 1:200 (far → near rim)\n({yd_fall:.0f}mm fall over {PROC_TRAY_D}mm) — LEVEL across X",
             ha="center", va="center", fontsize=7, color="#0D47A1",
             bbox=dict(fc="white", ec="#0D47A1", lw=0.8, pad=3, alpha=0.9),
             zorder=8)

    # Near-rim gutter X-slope annotation
    ax3.text((PROC_TRAY_W * 0.5), (PROC_TRAY_D * 0.10),
             f"NEAR-RIM GUTTER 1:200 → center pickup\n(~{gutter_fall:.0f}mm fall over {PROC_TRAY_W/2:.0f}mm each side)",
             ha="center", va="center", fontsize=6.5, color="#0D47A1",
             bbox=dict(fc="white", ec="#0D47A1", lw=0.8, pad=2, alpha=0.9),
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

    # ── Suction pickup (current design) ──────────────────────────────────────────
    # The 1" suction pops UP through the walkway grate directly above the center pickup (a VERTICAL
    # riser at X=PROC_TRAY_DRAIN_X), then runs above the walkway to P-04 on the pinhole-wall filter
    # skid.  In this top-down plan the riser is a point at the pickup (out of the page); the above-
    # walkway run to P-04 is off this view.  A ⊙ riser marker sits on the drain symbol.
    ax3.plot(drain_dx, drain_dy, marker="o", ms=6, mfc=C_BROWN, mec="white", mew=1.2, zorder=8)

    leader(ax3, (drain_local_x), (drain_local_yd + DRAIN_R),
           (drain_local_x + 250), (drain_local_yd + 780),
           "P-04 SUCTION — VERTICAL RISER\n(pops UP through the walkway →\nP-04 on the pinhole-wall filter skid)",
           fs=6.5, color=C_BROWN, ha="left")

    # ── Notes ────────────────────────────────────────────────────────────────────
    notes = [
        "NOTES:",
        f"1. Yd-only pitch 1:200 (far → near rim, LEVEL across X); the near-rim gutter falls 1:200 in X to the center pickup at X={PROC_TRAY_DRAIN_X}, Yd={PROC_TRAY_DRAIN_YD}.",
        f"2. Maximum fall: {PROC_TRAY_PITCH}mm (Yd axis, far → near rim) + ~{gutter_fall:.0f}mm (near-rim gutter, X edge → center pickup).",
        f"3. Sump well ({PROC_TRAY_SUMP_W}x{PROC_TRAY_SUMP_D}x{PROC_TRAY_SUMP_Z}mm) at the gutter low point — the P-04 suction pops UP through the walkway to P-04 on the filter skid.",
        f"4. Tray: 304 SS, {PROC_TRAY_RIM}mm rim, on tapered HDPE shim strips. No tray floor penetration.",
        f"5. Wall-cantilevered walkway — no legs or structure on tray floor near sump.",
    ]
    draw_notes(ax3, notes, (-410), (-890), spacing=(70), fs=7,
               width=(3780), color=C_TEXT, title_color=C_TEXT,
               font={"fontfamily": "monospace"})

    _save(fig3, "water-system-sheet3")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 4 — PROCESSING TRAY DRAIN CROSS-SECTION ELEVATION
# Two panels:
#   LEFT  — Zoomed detail of sump well + pickup tube + shim strips (~1:2)
#   RIGHT — Full cross-section: sump pickup riser up through the walkway to P-04
#           on the pinhole-wall filter skid -> SV-02 -> 3W-DV-02 -> filter train (~1:15)
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
                subtitle=f"Section A-A at X={PROC_TRAY_DRAIN_X}mm (through sump) + plan view: sump pickup -> P-04 on the filter skid",
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
    TUBE_WALL = 3.0  # PVC tube wall thickness (mm)
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

    # ── Suction riser from tube top — straight UP through the walkway ─────────────
    HOSE_OD = 33.0   # 1" reinforced suction hose OD (mm)
    HOSE_WALL = 4.0  # hose wall thickness (mm)

    # The suction stays directly over the pickup and rises vertically (no fold-over
    # the rim).  Above the walkway grate it turns +X (into the page) to P-04 on the
    # pinhole-wall filter skid.
    RISER_Z_TOP_A = tube_z_top + 78   # short riser above the grate within this view
    draw_pipe_path(ax4a, [tube_yd, tube_yd],
                   [tube_z_top - HOSE_OD, RISER_Z_TOP_A],
                   HOSE_OD, HOSE_WALL,
                   fc=C_BROWN, ec="#5A3020", zorder=8)

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

    leader(ax4a, (tube_yd), (RISER_Z_TOP_A - 12),
           (tube_yd + 95), (RISER_Z_TOP_A + 8),
           "1\" REINFORCED SUCTION\nRISES UP THROUGH WALKWAY,\nthen +X TO P-04 (INTO PAGE)", fs=6, color=C_BROWN)

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
    ax4b.text((550), (650), "SECTION A-A — SUMP PICKUP → P-04 (FILTER SKID) (AXES IN mm)",
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

    # ── Suction riser: up ~150mm above the walkway, then 90° +X (INTO the page) ──
    # P-04 sits on the pinhole-wall filter skid at X≈3300 (INTO the page in this section
    # at X=2399).  The suction rises only ~150mm above the walkway deck, then DOG-LEGS +X
    # (into the page) along the deck and rises to P-04 AT the skid — no tall wall riser.
    RISER_YD_B = tube_yd_b            # stays directly over the pickup
    RISER_Z_TOP = WK_DECK_H + 150     # 250 — ~150mm above the walkway deck, then turns into the page
    draw_pipe_path(ax4b, [RISER_YD_B, RISER_YD_B],
                   [tube_z_top_b - HOSE_OD, RISER_Z_TOP],
                   HOSE_OD, HOSE_WALL,
                   fc=C_BROWN, ec="#5A3020", zorder=4)

    # into-the-page (⊗) turn marker at the riser top — the pipe turns +X, leaving the section plane
    _rr = HOSE_OD / 1.5 / SC_B
    ax4b.add_patch(plt.Circle((RISER_YD_B, RISER_Z_TOP), _rr, fc="white", ec=C_BROWN, lw=1.3, zorder=6))
    _d = _rr * 0.7
    ax4b.plot([RISER_YD_B - _d, RISER_YD_B + _d], [RISER_Z_TOP - _d, RISER_Z_TOP + _d], color=C_BROWN, lw=1.0, zorder=7)
    ax4b.plot([RISER_YD_B - _d, RISER_YD_B + _d], [RISER_Z_TOP + _d, RISER_Z_TOP - _d], color=C_BROWN, lw=1.0, zorder=7)

    # ── Near walkway (Yd=0-300) — pickup pops UP through the grate ───────────────
    ax4b.add_patch(plt.Rectangle(((0), (WK_DECK_H - WK_GRATE_T)),
                  WALKWAY_W / SC_B, WK_GRATE_T / SC_B,
                  fc="#E0D6C8", ec="#8D6E63", lw=1.0, hatch="///", zorder=3,
                  alpha=0.7))

    # Destination leader — the dog-leg into the page to P-04 at the skid
    leader(ax4b, (RISER_YD_B), (RISER_Z_TOP),
           (RISER_YD_B + 250), (RISER_Z_TOP + 150),
           "RISER ~150mm ABOVE THE WALKWAY,\n"
           "then 90° +X (INTO PAGE) along the deck,\n"
           "rising to P-04 at the FILTER SKID (X=3300):\n"
           "P-04 → SV-02 → 3W-DV-02 → filter train",
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
    # PANEL C — PLAN VIEW: SUMP PICKUP → P-04 (FILTER SKID) (~1:8)
    # Looking down (standard plan orientation matching floorplan/IBC sheets):
    #   Horizontal = X (left=cargo door, right=sealed end)
    #   Vertical   = Yd (bottom=near wall/pinhole, top=far wall)
    # Sump pickup at left; suction runs +X above the walkway to P-04 on the skid.
    # ═════════════════════════════════════════════════════════════════════════════
    SC_C = 1.0

    SUMP_X = PROC_TRAY_DRAIN_X   # 2399mm — center pickup
    P04_SKID_X = 3300            # P-04 on the pinhole-wall filter skid (= PWP_FILTER_X1)
    SKID_YD = 104                # skid lane Yd (near the pinhole wall)
    TRAY_X_R = PROC_TRAY_X_R     # 4629mm

    X_VIEW_L = SUMP_X - 260
    X_VIEW_R = P04_SKID_X + 340
    YD_VIEW_BOT = -30
    YD_VIEW_TOP = 400

    ax4c.set_xlim((X_VIEW_L - 4), (X_VIEW_R + 4))
    ax4c.set_ylim((YD_VIEW_BOT - 4), (YD_VIEW_TOP + 4))

    # Panel C title
    ax4c.text(((X_VIEW_L + X_VIEW_R) / 2), (YD_VIEW_TOP + 15),
              "PLAN VIEW — SUMP PICKUP → P-04 (FILTER SKID) (AXES IN mm)",
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
    ax4c.text((SUMP_X - 30), (330),
              "PROCESSING TRAY", ha="center", va="center",
              fontsize=6, color="#6A8CAF", style="italic", alpha=0.7, zorder=3)

    # Near rim line (Yd=80, runs along X — horizontal)
    ax4c.plot([(tray_x_l_vis), (X_VIEW_R)],
             [(tray_yd_near), (tray_yd_near)],
             color="#C8D8E8", lw=2.0, zorder=4)

    # ── Sump (small rectangle inside tray at near rim) ─────────────────────────
    ax4c.add_patch(plt.Rectangle(
        ((SUMP_X - PROC_TRAY_SUMP_W / 2), (PROC_TRAY_DRAIN_YD)),
        PROC_TRAY_SUMP_W / SC_C, PROC_TRAY_SUMP_D / SC_C,
        fc="#B3D9F2", ec=C_FRAME, lw=1.0, zorder=5))
    ax4c.text((SUMP_X), (PROC_TRAY_DRAIN_YD + PROC_TRAY_SUMP_D / 2),
              "SUMP", ha="center", va="center", fontsize=5.5,
              fontweight="bold", color="#0D47A1", zorder=6)

    # ── Pickup riser end-on (vertical suction seen from above, at the sump) ─────
    draw_pipe_end(ax4c, (SUMP_X), (SKID_YD),
                  HOSE_OD / 2 / SC_C, HOSE_WALL / SC_C,
                  fc=C_BROWN, ec=C_FRAME, bore_fc="white", zorder=8)

    # ── P-04 on the pinhole-wall filter skid ────────────────────────────────────
    ax4c.add_patch(plt.Circle(
        ((P04_SKID_X), (SKID_YD)),
        44 / SC_C,
        fc="#E8884A", ec=C_FRAME, lw=1.2, zorder=6))
    ax4c.text((P04_SKID_X), (SKID_YD + 82),
              "P-04\n(filter skid)", ha="center", va="center", fontsize=5.5,
              fontweight="bold", color="#E8884A", zorder=7)

    # ── Suction: sump riser → runs ABOVE the walkway (+X) to P-04 ────────────────
    draw_pipe_path(ax4c,
                   [SUMP_X, P04_SKID_X - 44],
                   [SKID_YD, SKID_YD],
                   HOSE_OD, HOSE_WALL,
                   fc=C_BROWN, ec="#5A3020", zorder=6)

    # ── Labels ──────────────────────────────────────────────────────────────────
    leader(ax4c, (SUMP_X), (SKID_YD - 22),
           (SUMP_X - 30), (-58),
           "VERTICAL RISER\n(pops UP through walkway)", fs=6, color=C_BROWN)

    ax4c.text(((SUMP_X + P04_SKID_X) / 2), (SKID_YD + 26),
              "1\" SUCTION — ABOVE THE WALKWAY", ha="center", va="bottom",
              fontsize=6, color=C_BROWN, style="italic", zorder=7)

    # ── Dimension: sump → P-04 (X distance) ─────────────────────────────────────
    draw_dim_h(ax4c, (SUMP_X), (P04_SKID_X),
               (SKID_YD - 62),
               f"{P04_SKID_X - SUMP_X}mm", offset=4, fs=6)

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
        "5. P-04: Shurflo 2088, 12V DC, self-priming, on the pinhole-wall filter skid.",
        "6. Suction rises vertically through the walkway, then runs above it to P-04.",
        "7. Tray slope exaggerated for clarity in elevation panels.",
    ]
    draw_notes(ax4_notes, notes4, 38, 9.25, spacing=1.1,
               fs=7, width=26, color=C_TEXT, title_color=C_TEXT,
               font={"fontfamily": "monospace"})

    flow_notes = [
        "FLOW PATH:",
        "1. Water drains by gravity to the center sump well (Yd=80mm)",
        "2. Pickup + foot valve; suction rises through the walkway",
        "3. Runs +X above the walkway to P-04 on the filter skid",
        "4. P-04 -> SV-02 sample tap -> 3W-DV-02 diverter",
        "5. Recycle -> F1/F2/F3 filter train -> SV-01 -> 3W-DV-01",
        "6. DV-01: IBC-3 (recycle) / IBC-4 (waste) when selected",
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
