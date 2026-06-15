#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_panel_layout.py — Equipment panel layout in IBC corridor.

Front elevation of an 18mm plywood panel spanning the 270mm IBC plumbing
corridor (Yd=1046–1316), perpendicular to the sealed end wall at X=5000.
Equipment mounts on the panel face, protruding toward the open end (-X).

Left pump column:  P-01 (Blue) + P-04 (Tray drain) + ACC-01.
Right pump column: P-02 (Brown) + P-03 (Waste evac) + DV-02 + P-05 (Brown drain).
BV-07/BV-08 manual isolation valves on IBC drain-out suction lines.
Filters (×3) centered on panel below pump zone.

Plus a cross-section strip showing panel/walkway/wall relationship.

Output: diagrams/panel-layout.png
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math
import matplotlib.patches as mpatches

from tbs_constants import C_OUT, C_DIM, C_CL, C_STEEL, DIAGRAMS_DIR, PUMP_PIPE_OD, PUMP_PIPE_WALL, EQPANEL_X, EQPANEL_H
from tbs_drawing import (draw_dim_h, draw_dim_v, leader, draw_notes, hatch_rect,
                         draw_pipe_path as _tbs_pipe_path)
from tbs_title_block import title_block

# ── Panel geometry ────────────────────────────────────────────────────────
PANEL_T      = 18    # plywood thickness (mm)
PANEL_YD     = 1046  # panel near edge Yd (mm from pinhole wall)
PANEL_WALL_X = EQPANEL_X  # panel face X position (= EQPANEL_X)
WALKWAY_W    = 300   # standard walkway width (mm)
WALKWAY_Z    = 100   # walkway grating top (mm AFF)

# Panel face dimensions (new orientation: spans corridor)
PANEL_W  = 270   # face width (mm, Yd span: 1046–1316)
PANEL_H  = EQPANEL_H  # face height (mm, =2060; Z span: 250–2310)
PANEL_Z_AFF = 200  # panel bottom Z above finished floor

# ── Shurflo 2088 pump dimensions ─────────────────────────────────────────
PUMP_W   = 127   # front face width (mm)
PUMP_H   = 218   # front face height (mm) — body length, vertical mount
PUMP_D   = 114   # depth from panel (mm) — = tbs_constants PUMP_D (real Shurflo 2088 height 4.5"); KEEP IN SYNC
PUMP_GAP = 40    # vertical gap between pumps (mm)
PORT_HALF = 30   # half of port-to-port spacing (mm)

# ── Accumulator ───────────────────────────────────────────────────────────
ACC_OD  = 127    # body OD (mm)
ACC_LEN = 200    # body length (mm) — real SeaFlo 0.75L ~200; KEEP IN SYNC with the 3D equipment_panel() ACC cylinder

# ── Filter housing (separate, 4.5"×10") ──────────────────────────────────
FILT_OD  = 184   # housing OD (mm) — = tbs_constants BB_OD (real Big Blue 4.5x10 = Ø184); KEEP IN SYNC
FILT_H   = 340   # total height (mm) — head + sump, hung vertically
FILT_GAP = 30    # gap between housings (mm)
FILT_HEAD = 70   # head section height (mm)

# ── Layout on panel face (panel-relative coordinates) ────────────────────
# Horizontal axis = Yd from left edge (0=near wall, 270=far wall)
# Vertical axis = Z from panel bottom (0=bottom, 2060=top)
# Filters at BOTTOM, pumps at TOP.  F-01 at top of filter stack for gravity flow.

# Right column: 3 filter housings stacked vertically (sump-down) — BOTTOM
# F-01 (coarsest) at top, F-03 (finest) at bottom: gravity-assisted series flow
FILT_COL = PANEL_W // 2               # filter column center — centered on panel

F01_Z = 2 * (FILT_H + FILT_GAP)      # = 740 (top — P-02 feeds here first)
F02_Z = FILT_H + FILT_GAP            # = 370 (middle)
F03_Z = 0                             # = 0   (bottom — filtered exit)
FILT_STACK_TOP = F01_Z + FILT_H       # = 1080

# 2×2 pump grid above filter stack:
#   Left column  (Yd=0–127):  P-01 (Blue) + P-04 (Tray drain) + ACC-01
#   Right column (Yd=110–240): P-02 (Brown) + P-03 (Waste evac)
# Pairing follows pipe routing — left-fed pumps left, right-fed pumps right.

PUMP_COL = PUMP_W // 2               # = 63mm — left column center
PORT_IN_YD  = PUMP_COL + PORT_HALF   # right — inlet (suction)
PORT_OUT_YD = PUMP_COL - PORT_HALF   # left — outlet (discharge)

R_COL = PANEL_W - PUMP_COL           # = 207mm — right pump column center (symmetric)
R_PORT_IN  = R_COL + PORT_HALF       # 205 — right (inlet/suction)
R_PORT_OUT = R_COL - PORT_HALF       # 145 — left (outlet/discharge)

PUMP_ZONE_BOT = FILT_STACK_TOP + 40  # = 1120 (40mm gap above filter stack)

P01_Z = PUMP_ZONE_BOT                 # = 1120 (left col, bottom)
P04_Z = P01_Z + PUMP_H + PUMP_GAP    # = 1378 (left col, top)

P02_Z = PUMP_ZONE_BOT                 # = 1120 (right col, bottom)
P03_Z = P02_Z + PUMP_H + PUMP_GAP    # = 1378 (right col, top)

ACC_YD = PUMP_COL
ACC_Z  = P04_Z + PUMP_H + 150        # = 1746 (raised above P-04 for pipe separation)

P05_Z = ACC_Z                         # = 1746 (right column, beside ACC-01)

# ── Colors ────────────────────────────────────────────────────────────────
C_FRAME      = "#1A1A1A"
C_FRAME_FILL = "#B0B0B8"
C_PLY        = "#D4C8A0"
C_PLY_EC     = "#A09060"
C_BLUE       = "#2979B8"
C_BLUE_EC    = "#1A5A8A"
C_BROWN      = "#8B5E3C"
C_BROWN_EC   = "#5A3A20"
C_BLACK_SYS  = "#777777"
C_BLACK_EC   = "#444444"
C_FILTER     = "#4A90D9"
C_PUMP_BODY  = "#E0D0C0"
C_PUMP_EC    = "#806040"
C_ACC        = "#5A9ACC"
C_PIPE_FILL  = "#2A5A2A"
C_PIPE_EC    = "#1A3A1A"
C_NEW        = "#22AA44"
C_WALK       = "#A8D8A8"
C_WALL       = "#C0C0C8"
C_WALL_HATCH = "#999999"

# ── Layout ───────────────────────────────────────────────────────────────
FW  = 13.0
FH  = 33.0

X_SHOW_L = -130
X_SHOW_R = 400
Z_SHOW_L = -100
Z_SHOW_R = 2160

OX = 104
OZ = 280


def sx(x_mm):
    return OX + (x_mm - X_SHOW_L)


def sz(z_mm):
    return OZ + (z_mm - Z_SHOW_L)


# ── Figure setup ─────────────────────────────────────────────────────────
fig, ax = plt.subplots(1, 1, figsize=(FW, FH), dpi=200)
ax.set_xlim(0, FW * 80)
ax.set_ylim(0, FH * 80)
ax.set_aspect("equal")
ax.axis("off")

FONT = {"fontfamily": "monospace"}


def rect(x, z, w, h, fc, ec=C_FRAME, lw=1.0, zorder=5, alpha=1.0):
    """Rectangle in panel coords."""
    ax.add_patch(mpatches.Rectangle(
        (sx(x), sz(z)), w, h,
        fc=fc, ec=ec, lw=lw, zorder=zorder, alpha=alpha))


def circ(x_c, z_c, r, fc, ec=C_FRAME, lw=1.0, zorder=5, alpha=1.0):
    """Circle in panel coords."""
    ax.add_patch(plt.Circle(
        (sx(x_c), sz(z_c)), r,
        fc=fc, ec=ec, lw=lw, zorder=zorder, alpha=alpha))


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN ELEVATION — PANEL FACE
#  Looking at panel from open end (viewer facing +X toward sealed wall).
#  LEFT = near wall (Yd=1046), RIGHT = far wall (Yd=1316).
# ═══════════════════════════════════════════════════════════════════════════

# Title above panel
ax.text(sx(PANEL_W / 2), sz(Z_SHOW_R) + 12,
        "FRONT ELEVATION — EQUIPMENT PANEL",
        ha="center", va="bottom",
        fontsize=8, color=C_DIM, fontweight="bold", zorder=10, **FONT)

# 1. Panel outline (18mm plywood)
rect(0, 0, PANEL_W, PANEL_H,
     C_PLY, C_PLY_EC, lw=2.0, zorder=3, alpha=0.5)

# Panel label (near top)
ax.text(sx(PANEL_W / 2), sz(PANEL_H - 30),
        f"18mm MARINE PLY\n{PANEL_W}mm × {PANEL_H}mm",
        ha="center", va="top",
        fontsize=5.5, color=C_PLY_EC, zorder=4, **FONT)

# Zone separator (dashed line between left and right pump columns — pump zone only)
zone_yd = PUMP_W + 6   # 133mm — between pump columns
_zone_top = max(ACC_Z + ACC_LEN, P05_Z + PUMP_H) + 50
ax.plot([sx(zone_yd), sx(zone_yd)],
        [sz(PUMP_ZONE_BOT - 20), sz(_zone_top)],
        color=C_PLY_EC, lw=0.5, ls=(0, (4, 4)), zorder=3, alpha=0.5)


# ═══════════════════════════════════════════════════════════════════════════
#  2. PUMPS — 2×2 grid above filter stack
#     Left column:  P-01 (Blue) + P-04 (Tray drain)
#     Right column: P-02 (Brown) + P-03 (Waste evac)
# ═══════════════════════════════════════════════════════════════════════════


def _draw_pump(col_yd, port_in_yd, port_out_yd, pz, pname, pdesc, pfc, pec):
    rect(col_yd - PUMP_W / 2 - 10, pz - 8,
         PUMP_W + 20, 8,
         C_FRAME_FILL, C_FRAME, lw=0.5, zorder=4)
    rect(col_yd - PUMP_W / 2, pz, PUMP_W, PUMP_H,
         C_PUMP_BODY, C_PUMP_EC, lw=1.2, zorder=6)
    for port_yd in [port_out_yd, port_in_yd]:
        circ(port_yd, pz + PUMP_H - 25, 10,
             C_PIPE_FILL, C_PIPE_EC, lw=0.5, zorder=7)
    ax.text(sx(col_yd), sz(pz + PUMP_H / 2 + 15),
            pname, ha="center", va="center",
            fontsize=8, color=pfc, fontweight="bold", zorder=8, **FONT)
    ax.text(sx(col_yd), sz(pz + PUMP_H / 2 - 20),
            pdesc, ha="center", va="center",
            fontsize=5, color=pec, zorder=8, **FONT)


# Left column
_draw_pump(PUMP_COL, PORT_IN_YD, PORT_OUT_YD,
           P01_Z, "P-01", "BLUE\nSUPPLY", C_BLUE, C_BLUE_EC)
_draw_pump(PUMP_COL, PORT_IN_YD, PORT_OUT_YD,
           P04_Z, "P-04", "TRAY\nDRAIN", C_BLACK_SYS, C_BLACK_EC)

# Right column
_draw_pump(R_COL, R_PORT_IN, R_PORT_OUT,
           P02_Z, "P-02", "BROWN\nRECYCLE", C_BROWN, C_BROWN_EC)
_draw_pump(R_COL, R_PORT_IN, R_PORT_OUT,
           P03_Z, "P-03", "WASTE\nEVAC", C_BLACK_SYS, C_BLACK_EC)
_draw_pump(R_COL, R_PORT_IN, R_PORT_OUT,
           P05_Z, "P-05", "BROWN\nDRAIN", C_BROWN, C_BROWN_EC)


# ═══════════════════════════════════════════════════════════════════════════
#  3. ACC-01 — above pump stack (profile view, vertical, ports at bottom)
#     Inline: flow enters right port, exits left port (same as pump convention)
# ═══════════════════════════════════════════════════════════════════════════
ACC_BODY_Z = ACC_Z
rect(ACC_YD - ACC_OD / 2, ACC_BODY_Z, ACC_OD, ACC_LEN,
     C_ACC, C_BLUE_EC, lw=1.2, zorder=6, alpha=0.7)
ax.text(sx(ACC_YD), sz(ACC_BODY_Z + ACC_LEN / 2 + 10),
        "ACC-01", ha="center", va="center",
        fontsize=7, color="white", fontweight="bold", zorder=8, **FONT)
ax.text(sx(ACC_YD), sz(ACC_BODY_Z + ACC_LEN / 2 - 15),
        f"O/{ACC_OD}", ha="center", va="center",
        fontsize=5, color="white", zorder=8, **FONT)
# Two ports at bottom (IN right, OUT left — same spacing as pump ports)
for port_yd in [PORT_OUT_YD, PORT_IN_YD]:
    circ(port_yd, ACC_BODY_Z, 10,
         C_PIPE_FILL, C_PIPE_EC, lw=0.5, zorder=10)

# Mounting clamp (U-bracket at top)
clamp_w = ACC_OD + 20
rect(ACC_YD - clamp_w / 2, ACC_BODY_Z + ACC_LEN,
     clamp_w, 8,
     C_FRAME_FILL, C_FRAME, lw=0.5, zorder=5)


# ═══════════════════════════════════════════════════════════════════════════
#  4. FILTER HOUSINGS — 3× separate, stacked vertically (sump down)
#     Centered on panel (Yd=70–200), 130mm OD × 340mm tall
#     F-01 (50µm) at top → F-02 (5µm) → F-03 (GAC) at bottom: gravity-fed
# ═══════════════════════════════════════════════════════════════════════════
filter_specs = [
    ("F-01", "50µm\nSED.", F01_Z),
    ("F-02", "5µm\nSED.",  F02_Z),
    ("F-03", "GAC\nCARBON",    F03_Z),
]

for fname, fdesc, fz in filter_specs:
    # Housing body (rectangle — front view of vertical cylinder)
    rect(FILT_COL - FILT_OD / 2, fz, FILT_OD, FILT_H,
         C_FILTER, C_OUT, lw=1.2, zorder=6, alpha=0.6)
    # Head section (darker top)
    rect(FILT_COL - FILT_OD / 2, fz + FILT_H - FILT_HEAD, FILT_OD, FILT_HEAD,
         "#3A70B0", C_OUT, lw=0.8, zorder=6, alpha=0.7)
    # Sump bowl line (bottom section)
    ax.plot([sx(FILT_COL - FILT_OD / 2), sx(FILT_COL + FILT_OD / 2)],
            [sz(fz + 60), sz(fz + 60)],
            color=C_OUT, lw=0.5, ls="--", zorder=7)
    # Port indicators on head (IN left, OUT right)
    for port_off in [-35, 35]:
        circ(FILT_COL + port_off, fz + FILT_H - FILT_HEAD / 2, 12,
             "#B8D4F0", C_OUT, lw=0.4, zorder=7, alpha=0.6)
    # Label
    ax.text(sx(FILT_COL), sz(fz + FILT_H / 2 + 25),
            fname, ha="center", va="center",
            fontsize=7, color="white", fontweight="bold", zorder=8, **FONT)
    ax.text(sx(FILT_COL), sz(fz + FILT_H / 2 - 15),
            fdesc, ha="center", va="center",
            fontsize=4.5, color="white", zorder=8, **FONT)
    # Bracket at top
    rect(FILT_COL - FILT_OD / 2 - 10, fz + FILT_H,
         FILT_OD + 20, 10,
         C_FRAME_FILL, C_FRAME, lw=0.5, zorder=5)


# ═══════════════════════════════════════════════════════════════════════════
#  5. ZONE LABELS
# ═══════════════════════════════════════════════════════════════════════════
# Filter zone (bottom)
ax.text(sx(FILT_COL), sz(F03_Z - 20),
        "FILTER SKID (×3)", ha="center", va="top",
        fontsize=6, color=C_FILTER, fontweight="bold", zorder=10, **FONT)
ax.text(sx(FILT_COL), sz(F03_Z - 45),
        "SUMP DOWN", ha="center", va="top",
        fontsize=5, color=C_FILTER, zorder=10, **FONT)

# Pump zone (top — spans both columns)
ax.text(sx(PANEL_W / 2), sz(P01_Z - 30),
        "PUMP ZONE (×5)", ha="center", va="top",
        fontsize=6, color=C_PUMP_EC, fontweight="bold", zorder=10, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  5b. PLUMBING — parallel-wall pipes, diamond valves, concentric elbows
#
#  Orientation: looking at panel from open end (viewer facing +X).
#  LEFT = near wall / near IBC column (Blue IBCs)
#  RIGHT = far wall / far IBC column (Brown/Waste IBCs)
# ═══════════════════════════════════════════════════════════════════════════

# Pipe dimensions
PIPE_OD = PUMP_PIPE_OD
PIPE_WALL = PUMP_PIPE_WALL

# Valve half-diagonal (mm in panel coords)
BV_R = 15

# Pipe layer zorders
Z_BLACK = 6
Z_BROWN = 7
Z_BLUE  = 8
Z_DISCH = 9    # discharge riser draws OVER suction pipes

# ── Port Z positions (both ports at pump head, side by side) ──
PORT_DROP = 30               # discharge route drops below port Z
SUCT_RISE = 50               # suction route rises above port Z

P01_PORT_Z = P01_Z + PUMP_H - 25      # 1313 (left col, bottom)
P04_PORT_Z = P04_Z + PUMP_H - 25      # 1571 (left col, top)
P02_PORT_Z = P02_Z + PUMP_H - 25      # 1313 (right col, bottom)
P03_PORT_Z = P03_Z + PUMP_H - 25      # 1571 (right col, top)
P05_PORT_Z = P05_Z + PUMP_H - 25      # 1939 (right col, top — beside ACC-01)

# ── Filter head Z positions ──
F01_HEAD_Z = F01_Z + FILT_H - FILT_HEAD / 2   # top filter head
F02_HEAD_Z = F02_Z + FILT_H - FILT_HEAD / 2   # middle filter head
F03_HEAD_Z = F03_Z + FILT_H - FILT_HEAD / 2   # bottom filter head

# Filter port Yd positions (IN=left/near, OUT=right/far)
F_IN_YD  = FILT_COL - 35
F_OUT_YD = FILT_COL + 35

# ── Routing rails ──
DISCH_RAIL = PUMP_W - 5  # Blue discharge riser — 25mm left of prior position
INTERZONE  = F_IN_YD                         # pump-to-filter transition
JMPR_RAIL1 = FILT_COL + FILT_OD // 2 + 10   # 10mm outside housing
JMPR_RAIL2 = JMPR_RAIL1 + 15                # 15mm further out

# ── Entry/exit positions ──
EXIT_L = -60    # past left panel edge (near wall / walkway)
EXIT_R = 330    # past right panel edge (far wall / IBCs)

# ── Valve positions ──
BV01_YD = PORT_IN_YD                  # aligned with P-01 inlet port
BV01_Z  = P01_PORT_Z + SUCT_RISE
DV02_YD = R_COL                      # right column — blank space above P-03
DV02_Z  = P04_PORT_Z + 100           # 100mm rise from P-04 outlet before turn
BV07_YD = R_COL                       # centered above P-05
BV07_Z  = P05_Z + PUMP_H + 30        # 30mm above P-05 top
BV08_YD = 250                        # within panel, on raised suction horizontal
BV08_Z  = P03_PORT_Z + 150           # 1721 — raised 150mm for routing clearance

# ── Flow arrow style ──
_AW = 25
_arrow_kw = dict(arrowstyle="-|>", lw=1.5, mutation_scale=8)


def draw_pipe_path(ax, x_pts, z_pts, od_mm, wall_mm,
                   fc, ec=C_FRAME, bore_fc="white",
                   elbow_r=None, zorder=8, sxf=None, szf=None):
    """Thin wrapper → tbs_drawing.draw_pipe_path (canonical body).  Front view
    uses global sx/sz; the backside section passes identity via sxf/szf."""
    _tbs_pipe_path(ax, x_pts, z_pts, od_mm, wall_mm, fc, ec=ec,
                   bore_fc=bore_fc, elbow_r=elbow_r, zorder=zorder,
                   sx=(sxf if sxf is not None else sx),
                   sz=(szf if szf is not None else sz))


def draw_ball_valve(x, z, label, color):
    """Diamond valve symbol at (x, z) in panel mm coords."""
    pts_x = [sx(x), sx(x + BV_R), sx(x), sx(x - BV_R)]
    pts_z = [sz(z + BV_R), sz(z), sz(z - BV_R), sz(z)]
    ax.add_patch(plt.Polygon(list(zip(pts_x, pts_z)),
                             fc="white", ec=color, lw=1.5, zorder=12))
    ax.text(sx(x), sz(z), label, ha="center", va="center",
            fontsize=4.5, color=color, fontweight="bold", zorder=13, **FONT)


# ════════════════════════════════════════════════════════════════
#  BLUE SYSTEM (C_BLUE)
# ════════════════════════════════════════════════════════════════

# Blue suction: IBC-1/2 (LEFT) → BV-01 → 90° elbow → P-01 inlet (RIGHT port)
# Raised above port Z to clear outlet; discharge riser draws over via Z_DISCH
_P01_SUCT_Z = P01_PORT_Z + SUCT_RISE
draw_pipe_path(ax,
    [EXIT_L, BV01_YD, BV01_YD],
    [_P01_SUCT_Z, _P01_SUCT_Z, P01_PORT_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLUE, zorder=Z_BLUE)
draw_ball_valve(BV01_YD, BV01_Z, "BV\n01", C_BLUE)
ax.annotate("", xy=(sx(EXIT_L + _AW), sz(_P01_SUCT_Z)),
            xytext=(sx(EXIT_L), sz(_P01_SUCT_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BLUE), zorder=11)
ax.text(sx(EXIT_L - 5), sz(_P01_SUCT_Z),
        "FROM\nIBC-1/2\n(BLUE)", ha="right", va="center",
        fontsize=5.5, color=C_BLUE, zorder=10, **FONT)

# Blue discharge IN: P-01 outlet → riser → ACC-01 inlet (right port)
draw_pipe_path(ax,
    [PORT_IN_YD, DISCH_RAIL, DISCH_RAIL, PORT_OUT_YD, PORT_OUT_YD],
    [ACC_Z, ACC_Z, P01_PORT_Z - PORT_DROP, P01_PORT_Z - PORT_DROP, P01_PORT_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLUE, zorder=Z_DISCH)
# Blue discharge OUT: ACC-01 outlet (left port) → spray bar
# BV-02 relocated nearer the spray bar (not on this panel)
draw_pipe_path(ax,
    [EXIT_L, PORT_OUT_YD],
    [ACC_Z, ACC_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLUE, zorder=Z_DISCH)
ax.annotate("", xy=(sx(EXIT_L), sz(ACC_Z)),
            xytext=(sx(EXIT_L + _AW), sz(ACC_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BLUE), zorder=11)
ax.text(sx(EXIT_L - 5), sz(ACC_Z),
        "TO\nSPRAY\nBAR", ha="right", va="center",
        fontsize=5.5, color=C_BLUE, zorder=10, **FONT)


# ════════════════════════════════════════════════════════════════
#  BROWN SYSTEM (C_BROWN) — P-02 in right column
# ════════════════════════════════════════════════════════════════

# Brown suction: IBC-3 (far column, RIGHT) → P-02 inlet (right port)
draw_pipe_path(ax,
    [EXIT_R, R_PORT_IN],
    [P02_PORT_Z, P02_PORT_Z],
    PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
ax.annotate("", xy=(sx(EXIT_R - _AW), sz(P02_PORT_Z)),
            xytext=(sx(EXIT_R), sz(P02_PORT_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BROWN), zorder=11)
ax.text(sx(EXIT_R + 5), sz(P02_PORT_Z),
        "FROM\nIBC-3\n(BROWN)", ha="left", va="center",
        fontsize=5.5, color=C_BROWN, zorder=10, **FONT)

# Brown discharge: P-02 outlet → drop → left → down to F-01 IN
draw_pipe_path(ax,
    [R_PORT_OUT, R_PORT_OUT, F_IN_YD, F_IN_YD],
    [P02_PORT_Z, P02_PORT_Z - 100, P02_PORT_Z - 100, F01_HEAD_Z],
    PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)

# Filter jumpers — gravity-fed downward: F-01 → F-02 → F-03
_JMPR_DROP = 50

# F-01 OUT → rail 1 → drop to F-02 IN
draw_pipe_path(ax,
    [F_OUT_YD, JMPR_RAIL1, JMPR_RAIL1, F_IN_YD, F_IN_YD],
    [F01_HEAD_Z, F01_HEAD_Z, F02_HEAD_Z + _JMPR_DROP,
     F02_HEAD_Z + _JMPR_DROP, F02_HEAD_Z],
    PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)

# F-02 OUT → rail 2 → drop to F-03 IN
draw_pipe_path(ax,
    [F_OUT_YD, JMPR_RAIL2, JMPR_RAIL2, F_IN_YD, F_IN_YD],
    [F02_HEAD_Z, F02_HEAD_Z, F03_HEAD_Z + _JMPR_DROP,
     F03_HEAD_Z + _JMPR_DROP, F03_HEAD_Z],
    PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)

# F-03 OUT → exit RIGHT (filtered to IBC-1)
draw_pipe_path(ax,
    [F_OUT_YD, EXIT_R],
    [F03_HEAD_Z, F03_HEAD_Z],
    PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
ax.annotate("", xy=(sx(EXIT_R), sz(F03_HEAD_Z)),
            xytext=(sx(EXIT_R - _AW), sz(F03_HEAD_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BROWN), zorder=11)
ax.text(sx(EXIT_R + 5), sz(F03_HEAD_Z),
        "FILTERED\nTO IBC-1\n(REUSE)", ha="left", va="center",
        fontsize=5.5, color=C_BROWN, zorder=10, **FONT)


# ════════════════════════════════════════════════════════════════
#  TRAY DRAIN / BLACK SYSTEM (C_BLACK_SYS)
# ════════════════════════════════════════════════════════════════

# Tray drain suction: LEFT → P-04 inlet (RIGHT port)
# Suction horizontal crosses discharge vertical at Yd=PORT_OUT_YD —
# break suction at crossing (discharge is front pipe).
_P04_SUCT_Z = P04_PORT_Z + SUCT_RISE
_gap_half = PIPE_OD / 2.0
# Suction: before crossing
draw_pipe_path(ax,
    [EXIT_L, PORT_OUT_YD - _gap_half],
    [_P04_SUCT_Z, _P04_SUCT_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)
# Suction: after crossing + drop to port
draw_pipe_path(ax,
    [PORT_OUT_YD + _gap_half, PORT_IN_YD, PORT_IN_YD],
    [_P04_SUCT_Z, _P04_SUCT_Z, P04_PORT_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)
ax.annotate("", xy=(sx(EXIT_L + _AW), sz(_P04_SUCT_Z)),
            xytext=(sx(EXIT_L), sz(_P04_SUCT_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BLACK_SYS), zorder=11)
ax.text(sx(EXIT_L - 5), sz(_P04_SUCT_Z),
        "FROM\nTRAY\nSUMP", ha="right", va="center",
        fontsize=5.5, color=C_BLACK_SYS, zorder=10, **FONT)

# P-04 discharge: outlet (LEFT port) → up → right to DV-02 (front pipe at crossing)
draw_pipe_path(ax,
    [PORT_OUT_YD, PORT_OUT_YD, DV02_YD],
    [P04_PORT_Z, DV02_Z, DV02_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK + 0.5)

# DV-02 (3-way diverter — diamond symbol)
draw_ball_valve(DV02_YD, DV02_Z, "DV\n02", C_BLACK_EC)

# DV-02 Brown output → IBC-3: exits RIGHT from DV-02
draw_pipe_path(ax,
    [DV02_YD + BV_R, EXIT_R],
    [DV02_Z, DV02_Z],
    PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
ax.annotate("", xy=(sx(EXIT_R), sz(DV02_Z)),
            xytext=(sx(EXIT_R - _AW), sz(DV02_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BROWN), zorder=11)
ax.text(sx(EXIT_R + 5), sz(DV02_Z),
        "TO\nIBC-3", ha="left", va="center",
        fontsize=5.5, color=C_BROWN, zorder=10, **FONT)

# DV-02 Black output → IBC-4: exits BOTTOM from DV-02, then RIGHT
_DV_IBC4_Z = DV02_Z - 30
draw_pipe_path(ax,
    [DV02_YD, DV02_YD, EXIT_R],
    [DV02_Z - BV_R, _DV_IBC4_Z, _DV_IBC4_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)
ax.annotate("", xy=(sx(EXIT_R), sz(_DV_IBC4_Z)),
            xytext=(sx(EXIT_R - _AW), sz(_DV_IBC4_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BLACK_SYS), zorder=11)
ax.text(sx(EXIT_R + 5), sz(_DV_IBC4_Z),
        "TO\nIBC-4", ha="left", va="center",
        fontsize=5.5, color=C_BLACK_SYS, zorder=10, **FONT)


# ════════════════════════════════════════════════════════════════
#  P-03 WASTE EVACUATION (C_BLACK_SYS) — right column
# ════════════════════════════════════════════════════════════════

# P-03 suction: IBC-4 (RIGHT) → BV-08 → route down to P-03 inlet
# Raised 150mm (to Z=BV08_Z) so BV-08 sits within the backing board.
# Vertical drop at Yd=170 avoids DV-02 outputs; crosses P-04 discharge
# horizontal at Z=DV02_Z — gap-break (both black, P-03 suction behind).
_P03_DROP_YD = 150
_xing_z = DV02_Z
_xing_gap = PIPE_OD / 2.0

# Seg 1: horizontal entry from right + vertical above P-04 discharge crossing
draw_pipe_path(ax,
    [EXIT_R, _P03_DROP_YD, _P03_DROP_YD],
    [BV08_Z, BV08_Z, _xing_z + _xing_gap],
    PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)

# Seg 2: vertical below crossing, past port, U-turn back up to P-03 port
# Split at discharge crossing (Z=_P03_DISCH_Z) — gap-break, discharge in front.
_P03_HOOK_Z = P03_Z - 20
_P03_DISCH_Z = P03_PORT_Z - PORT_DROP
_p03_dx_gap = PIPE_OD / 2.0

# Seg 2a: hook + vertical up to below discharge crossing
draw_pipe_path(ax,
    [_P03_DROP_YD, _P03_DROP_YD, R_PORT_IN, R_PORT_IN],
    [_xing_z - _xing_gap, _P03_HOOK_Z, _P03_HOOK_Z,
     _P03_DISCH_Z - _p03_dx_gap],
    PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)

# Seg 2b: vertical above discharge crossing to P-03 port
draw_pipe_path(ax,
    [R_PORT_IN, R_PORT_IN],
    [_P03_DISCH_Z + _p03_dx_gap, P03_PORT_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)

ax.annotate("", xy=(sx(EXIT_R - _AW), sz(BV08_Z)),
            xytext=(sx(EXIT_R), sz(BV08_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BLACK_SYS), zorder=11)
ax.text(sx(EXIT_R + 5), sz(BV08_Z),
        "FROM\nIBC-4\n(WASTE)", ha="left", va="center",
        fontsize=5.5, color=C_BLACK_SYS, zorder=10, **FONT)
draw_ball_valve(BV08_YD, BV08_Z, "BV\n08", C_BLACK_EC)

# P-03 discharge: outlet (left port) → drop → right to X4 bulkhead
# zorder +0.5 so discharge draws in front of suction gap-break
draw_pipe_path(ax,
    [R_PORT_OUT, R_PORT_OUT, EXIT_R],
    [P03_PORT_Z, _P03_DISCH_Z, _P03_DISCH_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK + 0.5)
ax.annotate("", xy=(sx(EXIT_R), sz(_P03_DISCH_Z)),
            xytext=(sx(EXIT_R - _AW), sz(_P03_DISCH_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BLACK_SYS), zorder=11)
ax.text(sx(EXIT_R + 5), sz(_P03_DISCH_Z),
        "TO X4\nDRAIN\nPORT", ha="left", va="center",
        fontsize=5.5, color=C_BLACK_SYS, zorder=10, **FONT)


# ════════════════════════════════════════════════════════════════
#  P-05 BROWN DRAIN (C_BROWN) — right column, beside ACC-01
# ════════════════════════════════════════════════════════════════

# P-05 suction: IBC-3 (RIGHT) → BV-07 (centered above P-05) → drop → P-05 inlet
draw_pipe_path(ax,
    [EXIT_R, R_COL, R_COL, R_PORT_IN],
    [BV07_Z, BV07_Z, P05_PORT_Z, P05_PORT_Z],
    PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
draw_ball_valve(BV07_YD, BV07_Z, "BV\n07", C_BROWN)
ax.annotate("", xy=(sx(EXIT_R - _AW), sz(BV07_Z)),
            xytext=(sx(EXIT_R), sz(BV07_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BROWN), zorder=11)
ax.text(sx(EXIT_R + 5), sz(BV07_Z),
        "FROM\nIBC-3\n(DRAIN)", ha="left", va="center",
        fontsize=5.5, color=C_BROWN, zorder=10, **FONT)

# P-05 discharge: outlet (left port) → drop → right to X3 drain port
_P05_DISCH_Z = P05_PORT_Z - PORT_DROP
draw_pipe_path(ax,
    [R_PORT_OUT, R_PORT_OUT, EXIT_R],
    [P05_PORT_Z, _P05_DISCH_Z, _P05_DISCH_Z],
    PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
ax.annotate("", xy=(sx(EXIT_R), sz(_P05_DISCH_Z)),
            xytext=(sx(EXIT_R - _AW), sz(_P05_DISCH_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BROWN), zorder=11)
ax.text(sx(EXIT_R + 5), sz(_P05_DISCH_Z),
        "TO X3\nDRAIN\nPORT", ha="left", va="center",
        fontsize=5.5, color=C_BROWN, zorder=10, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  6. DIMENSIONS
# ═══════════════════════════════════════════════════════════════════════════

# Panel width (Yd span)
draw_dim_h(ax, sx(0), sx(PANEL_W), sz(-40),
           f"{PANEL_W}", offset=4.8, fs=7, color=C_DIM, font=FONT)

# Pump body width
draw_dim_h(ax, sx(PUMP_COL - PUMP_W / 2), sx(PUMP_COL + PUMP_W / 2),
           sz(P01_Z - 15),
           f"{PUMP_W}", offset=3.2, fs=5.5, color=C_DIM, font=FONT)

# Filter OD
draw_dim_h(ax, sx(FILT_COL - FILT_OD / 2), sx(FILT_COL + FILT_OD / 2),
           sz(F03_Z - 15),
           f"O/{FILT_OD}", offset=3.2, fs=5.5, color=C_FILTER, font=FONT)

# Filter housing height (single — bottom filter)
draw_dim_v(ax, sx(FILT_COL + FILT_OD / 2 + 20),
           sz(F03_Z), sz(F03_Z + FILT_H),
           f"{FILT_H}", offset=6.4, fs=6, color=C_FILTER,
           right=True, font=FONT)

# Filter stack height (full)
draw_dim_v(ax, sx(FILT_COL + FILT_OD / 2 + 50),
           sz(F03_Z), sz(FILT_STACK_TOP),
           f"{FILT_STACK_TOP}", offset=6.4, fs=6, color=C_DIM,
           right=True, font=FONT)

# Pump body height
draw_dim_v(ax, sx(PUMP_COL + PUMP_W / 2 + 15),
           sz(P01_Z), sz(P01_Z + PUMP_H),
           f"{PUMP_H}", offset=4.8, fs=5.5, color=C_DIM,
           right=True, font=FONT)

# Panel height
draw_dim_v(ax, sx(-30), sz(0), sz(PANEL_H),
           f"{PANEL_H}", offset=8.0, fs=7, color=C_DIM,
           right=False, font=FONT)

# Filter gap dimension (between bottom two filters)
draw_dim_v(ax, sx(FILT_COL - FILT_OD / 2 - 20),
           sz(F03_Z + FILT_H), sz(F02_Z),
           f"{FILT_GAP}", offset=4.8, fs=5, color=C_DIM,
           right=False, font=FONT)

# Panel Z position (AFF annotation at bottom edge)
ax.text(sx(PANEL_W + 30), sz(0),
        f"Z={PANEL_Z_AFF}\nAFF", ha="left", va="center",
        fontsize=5.5, color=C_DIM, zorder=10, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  7. LEADERS
# ═══════════════════════════════════════════════════════════════════════════

# Pump specs
leader(ax,
       sx(PUMP_COL - PUMP_W / 2), sz(P01_Z + PUMP_H / 2),
       sx(X_SHOW_L + 10), sz(P01_Z + PUMP_H / 2 - 60),
       "Shurflo 2088\n12V · 3.5 GPM · 45 PSI\n(×5 on SS L-brackets)",
       fs=5.5, color=C_PUMP_EC, font=FONT)

# ACC-01
leader(ax,
       sx(ACC_YD + ACC_OD / 2), sz(ACC_BODY_Z + ACC_LEN / 2),
       sx(PANEL_W + 40), sz(ACC_BODY_Z + ACC_LEN / 2 + 60),
       "ACC-01: 0.75L ACCUM.\nO/127 × 150mm\n1/2\" MNPT (bottom)",
       fs=5.5, color=C_BLUE_EC, font=FONT)

# Filter specs
leader(ax,
       sx(FILT_COL + FILT_OD / 2), sz(F01_Z + FILT_H / 2),
       sx(PANEL_W + 40), sz(F01_Z + FILT_H / 2 + 30),
       "4.5\"×10\" FILTER HOUSING\n1\" NPT IN/OUT\n(×3 separate, sump-down)",
       fs=5.5, color=C_FILTER, font=FONT)

# Max depth annotation
max_depth = max(PUMP_D, FILT_OD)
leader(ax,
       sx(PUMP_COL), sz(PANEL_H + 10),
       sx(X_SHOW_L + 10), sz(PANEL_H + 40),
       f"MAX PROTRUSION: {max_depth}mm\nFROM PANEL FACE (in -X)",
       fs=5.5, color=C_NEW, font=FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  CROSS-SECTION STRIP — panel position relative to walkway (Yd × Z)
# ═══════════════════════════════════════════════════════════════════════════

# Cross-section positioned at bottom of figure (axis units = mm-like, ×80)
CS_LEFT  = 48    # was 0.6 × 80
CS_BOT   = 160   # was 2.0 × 80
CS_W_IN  = 480   # was 6.0 × 80
CS_H_IN  = 80    # was 1.0 × 80

# Yd range to show (wall through corridor to far IBC edge)
IBC_NEAR_YD = 30
IBC_D = 1016
IBC_NEAR_END = IBC_NEAR_YD + IBC_D     # 1046
CORRIDOR_FAR = IBC_NEAR_END + 270       # 1316
YD_MAX = 1450
Z_CS_MAX = 250


def cs_yd(yd_mm):
    return CS_LEFT + yd_mm / YD_MAX * CS_W_IN


def cs_z(z_mm):
    return CS_BOT + z_mm / Z_CS_MAX * CS_H_IN


# Cross-section title
ax.text(CS_LEFT + CS_W_IN / 2, CS_BOT + CS_H_IN + 16,
        "CROSS-SECTION — PANEL IN IBC CORRIDOR (looking along X axis)",
        ha="center", va="bottom",
        fontsize=6.5, color=C_DIM, fontweight="bold", zorder=10, **FONT)

# Pinhole wall (Yd=0) — thick line
ax.plot([cs_yd(0), cs_yd(0)], [cs_z(-20), cs_z(Z_CS_MAX)],
        color=C_WALL, lw=4.0, zorder=3)
ax.text(cs_yd(0) - 4, cs_z(Z_CS_MAX / 2),
        "WALL\nYd=0", ha="right", va="center",
        fontsize=4, color=C_WALL_HATCH, zorder=10, **FONT)

# Floor
ax.plot([cs_yd(0), cs_yd(YD_MAX)], [cs_z(0), cs_z(0)],
        color=C_OUT, lw=1.5, zorder=3)

# Walkway (Yd=0 to 300)
ax.add_patch(mpatches.Rectangle(
    (cs_yd(0), cs_z(0)), WALKWAY_W / YD_MAX * CS_W_IN, WALKWAY_Z / Z_CS_MAX * CS_H_IN,
    fc=C_WALK, ec=C_NEW, lw=1.0, zorder=4, alpha=0.6))
ax.text(cs_yd(WALKWAY_W / 2), cs_z(WALKWAY_Z / 2),
        "WALKWAY\n300mm", ha="center", va="center",
        fontsize=4, color=C_NEW, fontweight="bold", zorder=5, **FONT)

# Near IBC column cross-section (Yd=30 to 1046)
C_IBC_CS = "#E0D8C8"
C_IBC_CS_EC = "#B0A898"
ax.add_patch(mpatches.Rectangle(
    (cs_yd(IBC_NEAR_YD), cs_z(0)),
    IBC_D / YD_MAX * CS_W_IN, cs_z(Z_CS_MAX) - cs_z(0),
    fc=C_IBC_CS, ec=C_IBC_CS_EC, lw=1.0, zorder=2, alpha=0.35))
ax.text(cs_yd(IBC_NEAR_YD + IBC_D / 2), cs_z(Z_CS_MAX * 0.5),
        "NEAR IBC\nCOLUMN", ha="center", va="center",
        fontsize=4.5, color=C_IBC_CS_EC, zorder=3, **FONT)

# Far IBC column (partial — Yd=1316 onward)
ax.add_patch(mpatches.Rectangle(
    (cs_yd(CORRIDOR_FAR), cs_z(0)),
    (YD_MAX - CORRIDOR_FAR) / YD_MAX * CS_W_IN, cs_z(Z_CS_MAX) - cs_z(0),
    fc=C_IBC_CS, ec=C_IBC_CS_EC, lw=1.0, zorder=2, alpha=0.35))
ax.text(cs_yd((CORRIDOR_FAR + YD_MAX) / 2), cs_z(Z_CS_MAX * 0.5),
        "FAR IBC\nCOLUMN", ha="center", va="center",
        fontsize=4.5, color=C_IBC_CS_EC, zorder=3, **FONT)

# Corridor boundaries
for yd_edge in [IBC_NEAR_END, CORRIDOR_FAR]:
    ax.plot([cs_yd(yd_edge), cs_yd(yd_edge)], [cs_z(0), cs_z(Z_CS_MAX)],
            color=C_IBC_CS_EC, lw=1.0, zorder=3)

# Panel spans full corridor (Yd=1046–1316)
panel_left_draw = cs_yd(IBC_NEAR_END)
panel_w_draw = (CORRIDOR_FAR - IBC_NEAR_END) / YD_MAX * CS_W_IN
ax.add_patch(mpatches.Rectangle(
    (panel_left_draw, cs_z(40)),
    panel_w_draw, cs_z(200) - cs_z(40),
    fc=C_PLY, ec=C_PLY_EC, lw=1.5, zorder=5, alpha=0.7))
ax.text(cs_yd((IBC_NEAR_END + CORRIDOR_FAR) / 2), cs_z(120),
        f"18mm PANEL\nSPANS CORRIDOR\n(Z={PANEL_Z_AFF}–{PANEL_Z_AFF + PANEL_H})",
        ha="center", va="center",
        fontsize=4.0, color=C_PLY_EC, fontweight="bold", zorder=10, **FONT)

# Corridor width dimension
draw_dim_h(ax, cs_yd(IBC_NEAR_END), cs_yd(CORRIDOR_FAR), cs_z(Z_CS_MAX + 10),
           "270 CORRIDOR", offset=3.2, fs=5.5, color=C_DIM, font=FONT)

# Yd axis
ax.text(cs_yd(YD_MAX / 2), cs_z(-15) - 14.4,
        "Yd (mm from pinhole wall) →", ha="center", va="top",
        fontsize=5.5, color=C_DIM, zorder=10, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  NOTES
# ═══════════════════════════════════════════════════════════════════════════
notes = [
    "EQUIPMENT PANEL — IBC PLUMBING CORRIDOR — ALL PIPE CONNECTIONS SHOWN",
    f"1. Panel: 18mm marine ply spanning corridor Yd={PANEL_YD}–{PANEL_YD + PANEL_W} (270mm).",
    f"2. Panel face at X={PANEL_WALL_X}, equipment protrudes toward open end (-X direction).",
    f"3. Panel height: Z={PANEL_Z_AFF}–{PANEL_Z_AFF + PANEL_H}mm AFF ({PANEL_H}mm), uses full IBC stack height.",
    "4. FILTERS: F-01 (50µm, top) → F-02 (5µm) → F-03 (GAC, bottom) — gravity-fed series flow.",
    "5. LEFT COL: P-01/P-04 + ACC-01. RIGHT COL: P-02/P-03 + DV-02 + P-05. All above filters.",
    "6. BV-01 (Blue supply), BV-07 (Brown drain), BV-08 (Waste drain) — manual ball valves.",
    "   BV-02 (Blue discharge) located near spray bar.",
    f"7. Max protrusion: {max_depth}mm. Near IBCs LEFT, far IBCs RIGHT in this view.",
    "8. Flow: P-02 ↑ F-01 (top) ↓ F-02 ↓ F-03 (bottom) → IBC-1. Gravity assists after F-01.",
]
draw_notes(ax, notes, 575, 300, spacing=14,
           fs=6, width=450, color=C_DIM, title_color=C_NEW, font=FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  DETAIL B — FILTER MOUNTING CROSS-SECTION
#  Side section perpendicular to panel face at filter head height.
#  Shows: 18mm ply panel → 50mm HDPE spacer → 3mm steel bracket →
#         filter head → sump bowl below → 1" NPT port with pipe stub
# ═══════════════════════════════════════════════════════════════════════════

# Detail B callout on main elevation — section cut line at F-01
_cut_z_top = sz(F01_Z + FILT_H - FILT_HEAD / 2 + 30)
_cut_z_bot = sz(F01_Z + FILT_H - FILT_HEAD / 2 - 30)
_cut_x = sx(FILT_COL + FILT_OD / 2 + 15)
ax.plot([_cut_x, _cut_x], [_cut_z_bot, _cut_z_top],
        color="#1A237E", lw=1.2, ls=(0, (6, 3, 1, 3)), zorder=11)
ax.text(_cut_x + 4.8, _cut_z_top,
        "B", fontsize=7, color="#1A237E", fontweight="bold",
        va="bottom", ha="center", zorder=11, **FONT)
ax.text(_cut_x + 4.8, _cut_z_bot,
        "B", fontsize=7, color="#1A237E", fontweight="bold",
        va="top", ha="center", zorder=11, **FONT)

# ── Position and scale ──
DET_LEFT = 720    # was 9.0 × 80
DET_Z0 = 760      # was 9.5 × 80


def det_y(yd_mm):
    """Detail Yd (mm from panel face) → axis units."""
    return DET_LEFT + yd_mm


def det_z(z_mm):
    """Detail Z (mm from head center) → axis units."""
    return DET_Z0 + z_mm


# Detail title
ax.text(det_y(80), det_z(85),
        "DETAIL B — FILTER MOUNTING\nCROSS-SECTION (~1:3)",
        ha="center", va="bottom",
        fontsize=6.5, fontweight="bold",
        color="#1A237E", zorder=10, **FONT)

# ── All Z coords relative to filter head port center ──

# 1. Equipment panel (18mm marine ply)
D_PANEL_T = 18.0
_dpanel_bot = -320
_dpanel_top = 65
ax.add_patch(mpatches.Rectangle(
    (det_y(-D_PANEL_T), det_z(_dpanel_bot)),
    D_PANEL_T, (_dpanel_top - _dpanel_bot),
    fc=C_PLY, ec=C_PLY_EC, lw=1.5, zorder=3))
for _gz in range(_dpanel_bot + 5, _dpanel_top - 5, 12):
    ax.plot([det_y(-D_PANEL_T + 2), det_y(-2)],
            [det_z(_gz), det_z(_gz + 2)],
            color="#C0B080", lw=0.3, zorder=3.5)

# 2. HDPE spacer block (50mm thick, 40mm visible height in section)
D_SPACER_YD = 0
D_SPACER_T = 50
D_SPACER_VIS_H = 40
ax.add_patch(mpatches.Rectangle(
    (det_y(D_SPACER_YD), det_z(-D_SPACER_VIS_H / 2)),
    D_SPACER_T, D_SPACER_VIS_H,
    fc="#E0D8B0", ec="#A09060", lw=1.0, zorder=4, hatch=".."))

# 3. Steel bracket tab (3mm)
D_BRACKET_YD = D_SPACER_YD + D_SPACER_T      # 50
D_BRACKET_T = 3
D_BRACKET_VIS_H = 50
ax.add_patch(mpatches.Rectangle(
    (det_y(D_BRACKET_YD), det_z(-D_BRACKET_VIS_H / 2)),
    D_BRACKET_T, D_BRACKET_VIS_H,
    fc="#999999", ec=C_FRAME, lw=1.0, zorder=5))

# 4. M6×80 bolt through panel + spacer + bracket
D_BOLT_Z = -10
_bolt_head_yd = D_BRACKET_YD + D_BRACKET_T   # 53
_bolt_tip_yd = -D_PANEL_T - 2                # -20
ax.plot([det_y(_bolt_tip_yd), det_y(_bolt_head_yd)],
        [det_z(D_BOLT_Z), det_z(D_BOLT_Z)],
        color=C_FRAME, lw=1.2, zorder=6)
ax.add_patch(mpatches.Rectangle(
    (det_y(_bolt_head_yd), det_z(D_BOLT_Z - 3)),
    4, 6,
    fc="#666666", ec=C_FRAME, lw=0.8, zorder=7))
ax.add_patch(mpatches.Rectangle(
    (det_y(_bolt_tip_yd - 2), det_z(D_BOLT_Z - 4)),
    3, 8,
    fc="#666666", ec=C_FRAME, lw=0.8, zorder=7))
leader(ax, det_y(_bolt_head_yd + 3), det_z(D_BOLT_Z),
       det_y(_bolt_head_yd + 35), det_z(D_BOLT_Z - 25),
       "M6×80 BOLT\n+ NYLOC NUT", fs=4.5, color=C_DIM, font=FONT)

# 5. Filter head (80mm depth × 70mm visible height)
D_HEAD_YD = D_BRACKET_YD + D_BRACKET_T + 2   # 55 (2mm gap for clamp)
D_HEAD_DEPTH = 80
D_HEAD_VIS_H = FILT_HEAD                     # 70
ax.add_patch(mpatches.Rectangle(
    (det_y(D_HEAD_YD), det_z(-D_HEAD_VIS_H / 2)),
    D_HEAD_DEPTH, D_HEAD_VIS_H,
    fc="#555555", ec=C_FRAME, lw=1.5, zorder=5))
ax.text(det_y(D_HEAD_YD + D_HEAD_DEPTH / 2), det_z(0),
        "HEAD", ha="center", va="center",
        fontsize=5.5, color="white", fontweight="bold", zorder=6, **FONT)

# 6. Sump bowl (hangs below head)
D_SUMP_H = FILT_H - FILT_HEAD               # 270
D_SUMP_W = FILT_OD                           # 130
_sump_cy = D_HEAD_YD + D_HEAD_DEPTH / 2      # 95
_sump_top_z = -D_HEAD_VIS_H / 2              # -35
_sump_bot_z = _sump_top_z - D_SUMP_H         # -305
ax.add_patch(mpatches.Rectangle(
    (det_y(_sump_cy - D_SUMP_W / 2), det_z(_sump_bot_z)),
    D_SUMP_W, D_SUMP_H,
    fc=C_FILTER, ec=C_FRAME, lw=1.2, alpha=0.6, zorder=4))
ax.text(det_y(_sump_cy), det_z(_sump_top_z - D_SUMP_H / 2),
        "SUMP\nBOWL", ha="center", va="center",
        fontsize=5.5, color="white", fontweight="bold", zorder=6, **FONT)

# Sump height dimension
draw_dim_v(ax, det_y(_sump_cy + D_SUMP_W / 2 + 10),
           det_z(_sump_bot_z), det_z(_sump_top_z),
           f"{int(D_SUMP_H)}", offset=4.8, fs=4.5, color=C_DIM,
           right=True, font=FONT)

# Cartridge removal arrow
ax.annotate("", xy=(det_y(_sump_cy), det_z(_sump_bot_z - 25)),
            xytext=(det_y(_sump_cy), det_z(_sump_bot_z - 5)),
            arrowprops=dict(arrowstyle="-|>", color="#CC4444", lw=1.5,
                            mutation_scale=8), zorder=10)
ax.text(det_y(_sump_cy), det_z(_sump_bot_z - 30),
        "UNSCREW SUMP\nFOR CARTRIDGE\nREPLACEMENT",
        ha="center", va="top",
        fontsize=4.5, color="#CC4444", fontweight="bold", zorder=10, **FONT)

# 7. 1" NPT port with pipe stub
D_PORT_YD = D_HEAD_YD + D_HEAD_DEPTH         # 135
D_PIPE_OD_D = 33
D_PIPE_WALL_D = 4
D_STUB_LEN = 40
ax.add_patch(mpatches.Rectangle(
    (det_y(D_PORT_YD - 12), det_z(-D_PIPE_OD_D / 2)),
    12, D_PIPE_OD_D,
    fc="white", ec=C_FRAME, lw=0.7, zorder=6))
ax.add_patch(mpatches.Rectangle(
    (det_y(D_PORT_YD), det_z(-D_PIPE_OD_D / 2)),
    D_STUB_LEN, D_PIPE_OD_D,
    fc=C_PIPE_FILL, ec=C_FRAME, lw=0.7, zorder=5))
ax.add_patch(mpatches.Rectangle(
    (det_y(D_PORT_YD), det_z(-D_PIPE_OD_D / 2 + D_PIPE_WALL_D)),
    D_STUB_LEN, (D_PIPE_OD_D - 2 * D_PIPE_WALL_D),
    fc="white", ec="none", zorder=6))
leader(ax, det_y(D_PORT_YD + D_STUB_LEN), det_z(0),
       det_y(D_PORT_YD + D_STUB_LEN + 25), det_z(18),
       "1\" HDPE\nTO NEXT STAGE", fs=4.5, color=C_PIPE_EC, font=FONT)

# 8. Clamp band at head/sump junction
D_CLAMP_H = 12
_clamp_yd_l = _sump_cy - D_SUMP_W / 2 - 4
_clamp_w = D_SUMP_W + 8
ax.add_patch(mpatches.Rectangle(
    (det_y(_clamp_yd_l), det_z(_sump_top_z - D_CLAMP_H)),
    _clamp_w, D_CLAMP_H,
    fc="#888888", ec=C_FRAME, lw=0.8, zorder=6))

# ── Detail dimensions ──
_standoff = D_SPACER_T + D_BRACKET_T   # 53mm from panel face
draw_dim_h(ax, det_y(0), det_y(D_BRACKET_YD + D_BRACKET_T),
           det_z(-55), f"{_standoff}mm STANDOFF", offset=4.0, fs=4.5,
           color=C_DIM, font=FONT)
draw_dim_h(ax, det_y(-D_PANEL_T), det_y(0),
           det_z(55), f"{int(D_PANEL_T)}", offset=3.2, fs=4,
           color=C_DIM, font=FONT)

# ── Component labels above section ──
_lbl_z = 68
for _ly, _ltxt in [(-D_PANEL_T / 2, "18mm\nPANEL"),
                    (D_SPACER_YD + D_SPACER_T / 2, "50mm\nHDPE"),
                    (D_BRACKET_YD + D_BRACKET_T / 2, "3mm\nBKT")]:
    ax.text(det_y(_ly), det_z(_lbl_z), _ltxt, ha="center", va="bottom",
            fontsize=4, color=C_FRAME, zorder=10, **FONT)
    ax.plot([det_y(_ly), det_y(_ly)], [det_z(_lbl_z - 3), det_z(40)],
            color=C_DIM, lw=0.4, ls=":", zorder=2)

# Section description
ax.text(det_y(80), det_z(_sump_bot_z - 50),
        "SECTION THROUGH FILTER HEAD\nPERPENDICULAR TO PANEL\nAT PORT HEIGHT\n(4.5\"×10\" BIG BLUE — SUMP-DOWN)",
        ha="center", va="top",
        fontsize=4.5, color="#666666", style="italic", zorder=10, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  TITLE BLOCK
# ═══════════════════════════════════════════════════════════════════════════
title_block(ax, "SHEET 1 OF 2",
            drawing_title="EQUIPMENT PANEL — IBC CORRIDOR MOUNTING",
            subtitle="FRONT ELEVATION + PIPE ROUTING + CROSS-SECTION + DETAIL B",
            scale_note="ELEV 1:80 · DETAIL B ~1:3 · X-SECTION NTS · AXES IN mm",
            doc_id="TBS-001 · Reorg Proposal",
            height=0.028)

# ── Save ─────────────────────────────────────────────────────────────────
os.makedirs(DIAGRAMS_DIR, exist_ok=True)
out = os.path.join(DIAGRAMS_DIR, "panel-layout.png")
fig.savefig(out, dpi=150, facecolor="white", edgecolor="none",
            bbox_inches="tight", pad_inches=0.2)
plt.close(fig)
print(f"Panel layout → {out}")


# ═══════════════════════════════════════════════════════════════════════════
#  SHEET 2 — BACKSIDE (corridor side section, looking along Yd)
#  Shows what is mounted on the BACK of the panel (toward the sealed wall):
#  the drain-riser spine and the X3/X4 drain risers running from the P-05/P-03
#  discharges down to the end-wall ports. (v2: the over-the-top Blue fill trunk +
#  its shelf are gone — the Blue fill now side-enters.) Absolute X/Z (mm) — matches the 3D model.
# ═══════════════════════════════════════════════════════════════════════════
from tbs_constants import (EQPANEL_X, EQPANEL_Z_LO, EQPANEL_Z_HI, EQPANEL_T,
                           C_LEN, C_HGT, EXT_DRAIN_3_H, EXT_DRAIN_H, EXT_FILL_H)

FB = {"fontfamily": "monospace"}
C_PLYB   = "#D9C9A3"   # plywood (tan)
C_BROWNB = "#7A5230"   # brown developer drain
C_WASTEB = "#8A8A8A"   # waste/grey drain
C_BLUEB  = "#3A78C0"   # blue fill
C_WALLB  = "#C8C8C8"

PANX  = EQPANEL_X                 # 4874 — panel face (ibc-reconfig-v2: moved forward)
PANX1 = EQPANEL_X + EQPANEL_T     # 4892 — panel rear
SPX1  = 5420                      # spine rear
WALLX = C_LEN                     # 5893 — sealed end wall
Z_BOT, Z_MID, Z_TOP = 1320, 1578, 1946          # pump rows
RX3, RX4 = 5400, 5340             # Brown / Waste riser X
POD = 24                          # pipe OD (mm)

figb, axb = plt.subplots(figsize=(11, 15.3))
axb.set_xlim(4600, 6620)
axb.set_ylim(-300, 2500)
axb.set_aspect("equal")
axb.axis("off")


def _rect(x, z, w, h, fc, ec=C_OUT, lw=1.0, z0=5, hatch=None, alpha=1.0):
    axb.add_patch(mpatches.Rectangle((x, z), w, h, facecolor=fc, edgecolor=ec,
                  lw=lw, zorder=z0, hatch=hatch, alpha=alpha))


_sid = lambda v: v          # backside section draws in true mm (identity scale)
PWALL = 4                   # pipe wall thickness (mm) — colored wall + white bore


def _pipe(xs, zs, fc):
    """Color-coded pipe run with parallel walls + concentric-arc elbow fittings
    at every direction change (skill_plumbing_drawing.md). xs/zs = waypoints.
    Reuses the panel's draw_pipe_path with identity scale (backside = true mm)."""
    draw_pipe_path(axb, xs, zs, POD, PWALL, fc, ec=C_OUT, bore_fc="white",
                   zorder=8, sxf=_sid, szf=_sid)


# ── Container shell context ──────────────────────────────────────────────
_rect(4980, -90, 5933 - 4980, 90, C_WALLB, lw=0.8, z0=2, hatch="////")   # floor
axb.text(5010, -45, "CONTAINER FLOOR", fontsize=6, va="center", color="#555", **FB)
_rect(WALLX, 0, 40, C_HGT, C_WALLB, lw=0.8, z0=2, hatch="\\\\")           # sealed end wall
axb.text(WALLX + 20, C_HGT - 60, f"SEALED\nEND WALL\n(X={int(C_LEN)})", fontsize=6,
         ha="center", va="top", color="#555", **FB)
axb.plot([4980, WALLX], [C_HGT, C_HGT], color="#999", lw=0.8, ls=(0, (6, 4)), zorder=2)
axb.text(5010, C_HGT + 25, f"CEILING (Z={int(C_HGT)})", fontsize=6, color="#777", **FB)

# ── Equipment panel (edge-on) + pumps on the front (-X) ──────────────────
_rect(PANX, EQPANEL_Z_LO, EQPANEL_T, EQPANEL_Z_HI - EQPANEL_Z_LO, C_PLYB, lw=1.3, z0=6)
leader(axb, PANX + EQPANEL_T / 2, 700, 5150, 560,
       f"EQUIPMENT PANEL\n18mm ply (edge-on)\nZ={EQPANEL_Z_LO}–{EQPANEL_Z_HI}", color=C_OUT, fs=6,
       ha="center", va="top", arrow_style="-|>", font=FB)
for zr, lbl, hot in [(Z_BOT, "P-01 /\nP-02", False),
                     (Z_MID, "P-03 /\nP-04", True),
                     (Z_TOP, "P-05 /\nACC-01", True)]:
    _rect(PANX - 100, zr, 100, 218, "#E6D9F0" if hot else "#EAEAEA",
          ec=C_OUT, lw=0.9, z0=5)
    axb.text(PANX - 50, zr + 109, lbl, fontsize=6, ha="center", va="center",
             color="#333", fontweight="bold", **FB)
axb.text(PANX - 50, Z_TOP - 70, "PUMPS\n(front face)", fontsize=5.5, ha="center",
         va="top", color="#777", style="italic", **FB)

# ── Drain-riser spine (full panel height) ────────────────────────────────
_rect(PANX1, EQPANEL_Z_LO, SPX1 - PANX1, EQPANEL_Z_HI - EQPANEL_Z_LO, C_PLYB, lw=1.2,
      z0=4, alpha=0.45)
leader(axb, (PANX1 + SPX1) / 2, 1150, 5560, 1080,
       "DRAIN-RISER SPINE\n18mm ply, teed off the panel\n(T in plan) — backs the\nX3/X4 drain risers",
       color=C_OUT, fs=6, ha="left", va="center", arrow_style="-|>", font=FB)

# ── Drain risers: P-05→X3 (Brown), P-03→X4 (Waste) ───────────────────────
# Each is one run: pump discharge stub → 90° elbow → riser down → 90° elbow →
# horizontal stub into the end-wall port (right-angle entry at both ends).
_pipe([PANX - 50, RX3, RX3,          WALLX],
      [Z_TOP,     Z_TOP, EXT_DRAIN_3_H, EXT_DRAIN_3_H], C_BROWNB)   # P-05 → X3
_pipe([PANX - 50, RX4, RX4,        WALLX],
      [Z_MID,     Z_MID, EXT_DRAIN_H, EXT_DRAIN_H], C_WASTEB)       # P-03 → X4
# P-clips on the risers (against the spine face)
for rx, ztop, n in [(RX3, Z_TOP, 4), (RX4, Z_MID, 3)]:
    for i in range(n):
        cz = 520 + i * 400
        if cz < ztop - 80:
            _rect(rx + POD / 2 - 2, cz - 11, 16, 22, C_STEEL, lw=0.6, z0=11)
leader(axb, RX3, 980, 5470, 760, "X3 BROWN DRAIN RISER\n(from P-05) — P-clips @400",
       color=C_BROWNB, fs=5.5, ha="left", va="top", arrow_style="-|>", font=FB)
leader(axb, RX4, 620, 5150, 380, "X4 WASTE DRAIN RISER\n(from P-03)",
       color="#555", fs=5.5, ha="center", va="top", arrow_style="-|>", font=FB)

# ── End-wall ports ───────────────────────────────────────────────────────
for z, lab, col in [(EXT_FILL_H, "X1", C_BLUEB), (EXT_DRAIN_3_H, "X3", C_BROWNB),
                    (EXT_DRAIN_H, "X4", C_WASTEB)]:
    axb.add_patch(mpatches.Circle((WALLX, z), 22, facecolor="white",
                  edgecolor=col, lw=1.8, zorder=12))
    axb.text(WALLX, z, lab, fontsize=6, ha="center", va="center",
             fontweight="bold", color=col, zorder=13, **FB)

# ── Dimensions ───────────────────────────────────────────────────────────
draw_dim_v(axb, 5300, EXT_DRAIN_3_H, Z_TOP, "X3 riser\n400→1946", offset=6,
           fs=5, right=False, font=FB)
draw_dim_h(axb, PANX1, SPX1, 150, f"{SPX1 - PANX1}mm spine depth", offset=4,
           fs=5.5, above=False, font=FB)

# ── Notes (right margin) ─────────────────────────────────────────────────
draw_notes(axb, [
    "BACKSIDE — corridor side section (looking along Yd):",
    "1. Pumps mount on the FRONT face (−X); the drain risers + spine are on the BACK (+X), in the corridor gap (clear of both tote columns).",
    "2. Drain-riser spine: 18mm ply teed perpendicular off the panel (a T in plan), full panel height (Z=250–2310). v2: the Blue fill side-enters near the tote tops — no over-the-top trunk or shelf.",
    "3. The X3/X4 risers clamp to the spine face on SS P-clips at ~400mm centers.",
    "4. Risers feed from the pump discharges — P-05→X3 (Brown) @ Z=1946, P-03→X4 (Waste) @ Z=1578 — down to the sealed end-wall ports.",
], 5985, 2380, spacing=64, fs=7, ha="left", width=600, font=FB)

title_block(axb, "SHEET 2 OF 2",
            drawing_title="EQUIPMENT PANEL — BACKSIDE",
            subtitle="DRAIN-RISER SPINE · X3/X4 RISERS · X1/X3/X4 END-WALL PORTS",
            scale_note="CORRIDOR SIDE SECTION ALONG Yd · AXES IN mm",
            doc_id="TBS-001 · Equipment Panel",
            height=0.05)

outb = os.path.join(DIAGRAMS_DIR, "panel-layout-back.png")
figb.savefig(outb, dpi=150, facecolor="white", edgecolor="none",
             bbox_inches="tight", pad_inches=0.2)
plt.close(figb)
print(f"Panel backside → {outb}")
