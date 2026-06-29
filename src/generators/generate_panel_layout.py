#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_panel_layout.py — Two plumbing panels + the corridor backside.

The water system has two physically separate plumbing panels:

CORRIDOR PLUMBING PANEL (panel-layout.png) — 18mm plywood spanning the 270mm
IBC plumbing corridor (Yd=1046–1316), perpendicular to the sealed end wall.
Carries the four transfer pumps and the tray-drain diverter:
  Left column:  P-01 (Blue supply) + P-04 (Tray drain) + ACC-01.
  Right column: P-03 (Waste evac) + P-05 (Brown drain) + DV-02 (tray-sump
                diverter) + SV-02 (pH sample tap on the P-04 discharge).
  Ball valves: BV-01 (P-01 suction), BV-02 (P-05 suction), BV-06 (P-03 suction).

PINHOLE WALL PLUMBING PANEL (pinhole-panel.png) — the Brown recycle / filter
train mounted on the pinhole wall:
  P-02 (Brown recycle) + 3-stage Big Blue filter stack (F-01 50µm → F-02 5µm →
  F-03 GAC) + DV-01 (filtered-water diverter) + SV-01 (pH sample tap) +
  BV-03 (P-02 suction).
  Flow: IBC-3 Brown → BV-03 → P-02 → F-01 → F-02 → F-03 → SV-01 → DV-01 →
        (Blue recycle / Waste).

Plus a corridor-backside section (panel-layout-back.png) showing the
drain-riser spine and Circuit-C pump power.

Outputs: diagrams/panel-layout.png, diagrams/pinhole-panel.png,
         diagrams/panel-layout-back.png
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
from tbs_constants import WALKWAY_W   # standard walkway width (mm)
WALKWAY_Z    = 100   # walkway grating top (mm AFF)

# Panel face dimensions (new orientation: spans corridor)
PANEL_W  = 270   # face width (mm, Yd span: 1046–1316)
PANEL_H  = EQPANEL_H  # face height (mm, =2060; Z span: 250–2310)
PANEL_Z_AFF = 200  # panel bottom Z above finished floor

# ── Shurflo 2088 pump dimensions ─────────────────────────────────────────
PUMP_W   = 127   # front face width (mm)
PUMP_H   = 218   # front face height (mm) — body length, vertical mount
from tbs_constants import PUMP_D   # depth from panel (mm) — real Shurflo 2088 (4.5")
from tbs_constants import IBC_D    # IBC tote depth (mm) — used by the cross-section strip
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

# Two-column pump centers (shared by both panels' pump drawing)
PUMP_COL = PUMP_W // 2               # = 63mm — left column center
PORT_IN_YD  = PUMP_COL + PORT_HALF   # right — inlet (suction)
PORT_OUT_YD = PUMP_COL - PORT_HALF   # left — outlet (discharge)

R_COL = PANEL_W - PUMP_COL           # = 207mm — right pump column center (symmetric)
R_PORT_IN  = R_COL + PORT_HALF       # 205 — right (inlet/suction)
R_PORT_OUT = R_COL - PORT_HALF       # 145 — left (outlet/discharge)

# ── CORRIDOR PANEL layout ────────────────────────────────────────────────
# Four pumps only (filters + P-02 moved to the Pinhole Wall panel).  Center the
# pump grid vertically on the panel so the freed lower zone reads as intentional
# open space rather than a deletion.
#   Left column:  P-01 (Blue) bottom + P-04 (Tray drain) top + ACC-01 above.
#   Right column: P-03 (Waste) bottom + P-05 (Brown drain) top + DV-02/SV-02.
PUMP_ZONE_BOT = 760                   # bottom pump row Z (centered grid)

P01_Z = PUMP_ZONE_BOT                 # left col, bottom
P04_Z = P01_Z + PUMP_H + PUMP_GAP    # left col, top

P03_Z = PUMP_ZONE_BOT                 # right col, bottom
P05_Z = P03_Z + PUMP_H + PUMP_GAP    # right col, top

ACC_YD = PUMP_COL
ACC_Z  = P04_Z + PUMP_H + 150        # raised above P-04 for pipe separation

# ── PINHOLE WALL PANEL layout ────────────────────────────────────────────
# 3 filter housings stacked vertically (sump-down) at BOTTOM; P-02 above.
# F-01 (coarsest) at top, F-03 (finest) at bottom: gravity-assisted series flow.
FILT_COL = PANEL_W // 2               # filter column center — centered on panel
F01_Z = 2 * (FILT_H + FILT_GAP)      # = 740 (top — P-02 feeds here first)
F02_Z = FILT_H + FILT_GAP            # = 370 (middle)
F03_Z = 0                             # = 0   (bottom — filtered exit)
FILT_STACK_TOP = F01_Z + FILT_H       # = 1080

P02_COL = PANEL_W // 2                # P-02 centered above the filter stack
P02_PORT_IN_YD  = P02_COL + PORT_HALF
P02_PORT_OUT_YD = P02_COL - PORT_HALF
P02_Z = FILT_STACK_TOP + 60          # P-02 sits 60mm above the filter stack

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
# `ax` is the current panel axes; each draw_*_panel() rebinds it via _new_panel_fig().
ax = None

FONT = {"fontfamily": "monospace"}


def _new_panel_fig():
    """Create a fresh figure + axes for a panel front elevation; rebinds global ax."""
    global ax
    fig, ax = plt.subplots(1, 1, figsize=(FW, FH), dpi=200)
    ax.set_xlim(0, FW * 80)
    ax.set_ylim(0, FH * 80)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


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


# ── Shared plumbing constants + helpers (used by both panel elevations) ────
PIPE_OD = PUMP_PIPE_OD
PIPE_WALL = PUMP_PIPE_WALL
BV_R = 15                     # valve half-diagonal (mm in panel coords)

# Pipe layer zorders
Z_BLACK = 6
Z_BROWN = 7
Z_BLUE  = 8
Z_DISCH = 9    # discharge riser draws OVER suction pipes

PORT_DROP = 30               # discharge route drops below port Z
SUCT_RISE = 50               # suction route rises above port Z

# Flow arrow style
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


# ═══════════════════════════════════════════════════════════════════════════
#  CORRIDOR PLUMBING PANEL — FRONT ELEVATION
#  Looking at panel from open end (viewer facing +X toward sealed wall).
#  LEFT = near wall (Yd=1046), RIGHT = far wall (Yd=1316).
#  P-01/P-04 + ACC-01 (left), P-03/P-05 + DV-02 + SV-02 (right).
# ═══════════════════════════════════════════════════════════════════════════
def draw_corridor_panel():
    fig = _new_panel_fig()

    # Title above panel
    ax.text(sx(PANEL_W / 2), sz(Z_SHOW_R) + 12,
            "FRONT ELEVATION — CORRIDOR PLUMBING PANEL",
            ha="center", va="bottom",
            fontsize=8, color=C_DIM, fontweight="bold", zorder=10, **FONT)

    # 1. Panel outline (18mm plywood)
    rect(0, 0, PANEL_W, PANEL_H,
         C_PLY, C_PLY_EC, lw=2.0, zorder=3, alpha=0.5)

    # Panel label (near top)
    ax.text(sx(PANEL_W / 2), sz(PANEL_H - 30),
            f"18mm MARINE PLY\n{PANEL_W}mm x {PANEL_H}mm",
            ha="center", va="top",
            fontsize=5.5, color=C_PLY_EC, zorder=4, **FONT)

    # Zone separator (dashed line between left and right pump columns)
    zone_yd = PUMP_W + 6   # 133mm — between pump columns
    _zone_top = max(ACC_Z + ACC_LEN, P05_Z + PUMP_H) + 50
    ax.plot([sx(zone_yd), sx(zone_yd)],
            [sz(P01_Z - 40), sz(_zone_top)],
            color=C_PLY_EC, lw=0.5, ls=(0, (4, 4)), zorder=3, alpha=0.5)

    # ── PUMPS — 2×2 grid ──────────────────────────────────────────────────
    #   Left column:  P-01 (Blue supply) + P-04 (Tray drain)
    #   Right column: P-03 (Waste evac) + P-05 (Brown drain)
    _draw_pump(PUMP_COL, PORT_IN_YD, PORT_OUT_YD,
               P01_Z, "P-01", "BLUE\nSUPPLY", C_BLUE, C_BLUE_EC)
    _draw_pump(PUMP_COL, PORT_IN_YD, PORT_OUT_YD,
               P04_Z, "P-04", "TRAY\nDRAIN", C_BLACK_SYS, C_BLACK_EC)
    _draw_pump(R_COL, R_PORT_IN, R_PORT_OUT,
               P03_Z, "P-03", "WASTE\nEVAC", C_BLACK_SYS, C_BLACK_EC)
    _draw_pump(R_COL, R_PORT_IN, R_PORT_OUT,
               P05_Z, "P-05", "BROWN\nDRAIN", C_BROWN, C_BROWN_EC)

    # ── ACC-01 — above the left pump column ───────────────────────────────
    rect(ACC_YD - ACC_OD / 2, ACC_Z, ACC_OD, ACC_LEN,
         C_ACC, C_BLUE_EC, lw=1.2, zorder=6, alpha=0.7)
    ax.text(sx(ACC_YD), sz(ACC_Z + ACC_LEN / 2 + 10),
            "ACC-01", ha="center", va="center",
            fontsize=7, color="white", fontweight="bold", zorder=8, **FONT)
    ax.text(sx(ACC_YD), sz(ACC_Z + ACC_LEN / 2 - 15),
            f"O/{ACC_OD}", ha="center", va="center",
            fontsize=5, color="white", zorder=8, **FONT)
    for port_yd in [PORT_OUT_YD, PORT_IN_YD]:
        circ(port_yd, ACC_Z, 10, C_PIPE_FILL, C_PIPE_EC, lw=0.5, zorder=10)
    clamp_w = ACC_OD + 20
    rect(ACC_YD - clamp_w / 2, ACC_Z + ACC_LEN, clamp_w, 8,
         C_FRAME_FILL, C_FRAME, lw=0.5, zorder=5)

    # ── Zone label ────────────────────────────────────────────────────────
    ax.text(sx(PANEL_W / 2), sz(P01_Z - 30),
            "PUMP ZONE (4 transfer pumps)", ha="center", va="top",
            fontsize=6, color=C_PUMP_EC, fontweight="bold", zorder=10, **FONT)

    # ════════════════════════════════════════════════════════════════
    #  PLUMBING
    # ════════════════════════════════════════════════════════════════
    DISCH_RAIL = PUMP_W - 5
    EXIT_L = -60    # past left panel edge (near wall / walkway)
    EXIT_R = 330    # past right panel edge (far wall / IBCs)

    P01_PORT_Z = P01_Z + PUMP_H - 25
    P04_PORT_Z = P04_Z + PUMP_H - 25
    P03_PORT_Z = P03_Z + PUMP_H - 25
    P05_PORT_Z = P05_Z + PUMP_H - 25

    # Valve positions
    BV01_YD = PORT_IN_YD
    BV01_Z  = P01_PORT_Z + SUCT_RISE
    DV02_YD = R_COL
    DV02_Z  = P04_PORT_Z + 200            # tray-drain diverter (tall riser fits SV-02)
    BV02_YD = R_COL                       # P-05 suction isolation (was BV-07)
    BV02_Z  = DV02_Z + 130                # well above DV-02 so its feed line clears
    BV06_YD = 250                         # P-03 suction isolation (was BV-08)
    BV06_Z  = P03_PORT_Z + 150

    # ── BLUE SYSTEM ─────────────────────────────────────────────────
    # Blue suction: IBC-1/2 (LEFT) → BV-01 → 90° elbow → P-01 inlet
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

    # ── TRAY DRAIN / BLACK SYSTEM ───────────────────────────────────
    # Tray drain suction: LEFT → P-04 inlet (RIGHT port).  Crosses the Blue
    # discharge vertical at Yd=PORT_OUT_YD — break suction (discharge in front).
    _P04_SUCT_Z = P04_PORT_Z + SUCT_RISE
    _gap_half = PIPE_OD / 2.0
    draw_pipe_path(ax,
        [EXIT_L, PORT_OUT_YD - _gap_half],
        [_P04_SUCT_Z, _P04_SUCT_Z],
        PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)
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

    # P-04 discharge: outlet (LEFT port) → short jog right to a clear riser lane
    # (P04_RISER_YD, in the inter-column gap, clear of the blue ACC/spray-bar
    # lines on PORT_OUT_YD) → up (SV-02 sample tap) → right to DV-02.
    P04_RISER_YD = zone_yd - 8                  # just left of the zone separator (~125mm)
    SV02_Z = P04_PORT_Z + 100            # on the riser, between P-04 port and DV-02
    draw_pipe_path(ax,
        [PORT_OUT_YD, P04_RISER_YD, P04_RISER_YD, DV02_YD],
        [P04_PORT_Z, P04_PORT_Z, DV02_Z, DV02_Z],
        PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK + 0.5)
    # SV-02 pH sample tap — small ball valve on the riser + downturned barb spout
    draw_ball_valve(P04_RISER_YD, SV02_Z, "SV\n02", C_BLACK_EC)
    ax.annotate("", xy=(sx(P04_RISER_YD - BV_R - 28), sz(SV02_Z)),
                xytext=(sx(P04_RISER_YD - BV_R), sz(SV02_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BLACK_SYS), zorder=11)
    leader(ax, sx(P04_RISER_YD - BV_R), sz(SV02_Z),
           sx(EXIT_L - 5), sz(SV02_Z + 160),
           "SV-02 — pH sample tap\n(P-04 discharge, before DV-02)",
           fs=6, color=C_BLACK_EC, ha="right", va="center", font=FONT)

    # DV-02 (3-way diverter — tray sump → IBC-3 / IBC-4)
    # Both outputs run right to EXIT_R in FRONT of the P-05 suction drop.
    _DV_IBC4_Z = DV02_Z - 70
    draw_ball_valve(DV02_YD, DV02_Z, "DV\n02", C_BLACK_EC)
    # DV-02 Brown output → IBC-3: exits RIGHT
    draw_pipe_path(ax,
        [DV02_YD + BV_R, EXIT_R],
        [DV02_Z, DV02_Z],
        PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_DISCH)
    ax.annotate("", xy=(sx(EXIT_R), sz(DV02_Z)),
                xytext=(sx(EXIT_R - _AW), sz(DV02_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BROWN), zorder=11)
    ax.text(sx(EXIT_R + 5), sz(DV02_Z),
            "TO\nIBC-3", ha="left", va="center",
            fontsize=5.5, color=C_BROWN, zorder=10, **FONT)
    # DV-02 Black output → IBC-4: exits BOTTOM then RIGHT
    draw_pipe_path(ax,
        [DV02_YD, DV02_YD, EXIT_R],
        [DV02_Z - BV_R, _DV_IBC4_Z, _DV_IBC4_Z],
        PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_DISCH)
    ax.annotate("", xy=(sx(EXIT_R), sz(_DV_IBC4_Z)),
                xytext=(sx(EXIT_R - _AW), sz(_DV_IBC4_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BLACK_SYS), zorder=11)
    ax.text(sx(EXIT_R + 5), sz(_DV_IBC4_Z),
            "TO\nIBC-4", ha="left", va="center",
            fontsize=5.5, color=C_BLACK_SYS, zorder=10, **FONT)

    # ── P-03 WASTE EVACUATION (right column, bottom) ────────────────
    # P-03 suction: IBC-4 (RIGHT) → BV-06 → route down to P-03 inlet
    _P03_DROP_YD = 150
    _xing_z = DV02_Z
    _xing_gap = PIPE_OD / 2.0
    draw_pipe_path(ax,
        [EXIT_R, _P03_DROP_YD, _P03_DROP_YD],
        [BV06_Z, BV06_Z, _xing_z + _xing_gap],
        PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)
    _P03_HOOK_Z = P03_Z - 20
    _P03_DISCH_Z = P03_PORT_Z - PORT_DROP
    _p03_dx_gap = PIPE_OD / 2.0
    draw_pipe_path(ax,
        [_P03_DROP_YD, _P03_DROP_YD, R_PORT_IN, R_PORT_IN],
        [_xing_z - _xing_gap, _P03_HOOK_Z, _P03_HOOK_Z,
         _P03_DISCH_Z - _p03_dx_gap],
        PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)
    draw_pipe_path(ax,
        [R_PORT_IN, R_PORT_IN],
        [_P03_DISCH_Z + _p03_dx_gap, P03_PORT_Z],
        PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)
    ax.annotate("", xy=(sx(EXIT_R - _AW), sz(BV06_Z)),
                xytext=(sx(EXIT_R), sz(BV06_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BLACK_SYS), zorder=11)
    ax.text(sx(EXIT_R + 5), sz(BV06_Z),
            "FROM\nIBC-4\n(WASTE)", ha="left", va="center",
            fontsize=5.5, color=C_BLACK_SYS, zorder=10, **FONT)
    draw_ball_valve(BV06_YD, BV06_Z, "BV\n06", C_BLACK_EC)
    # P-03 discharge: outlet (left port) → drop → right to X4 drain port
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

    # ── P-05 BROWN DRAIN (right column, top, beside ACC-01) ─────────
    # P-05 suction: IBC-3 (RIGHT) → BV-02 → drop down the INLET column
    # (Yd=R_PORT_IN, clear of DV-02 on R_COL) → P-05 inlet.  The vertical drop
    # crosses BEHIND the two DV-02 output horizontals (TO IBC-3 @ DV02_Z,
    # TO IBC-4 @ _DV_IBC4_Z) — gap-break the rear (brown) pipe at each crossing.
    _p05_gap = PIPE_OD / 2.0
    _xings = sorted([DV02_Z, _DV_IBC4_Z], reverse=True)   # top-down
    draw_pipe_path(ax,                                    # horizontal entry
        [EXIT_R, R_PORT_IN],
        [BV02_Z, BV02_Z],
        PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
    # vertical, broken at each crossing
    _seg_top = BV02_Z
    for _xz in _xings:
        draw_pipe_path(ax,
            [R_PORT_IN, R_PORT_IN],
            [_seg_top, _xz + _p05_gap],
            PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
        _seg_top = _xz - _p05_gap
    draw_pipe_path(ax,
        [R_PORT_IN, R_PORT_IN],
        [_seg_top, P05_PORT_Z],
        PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
    draw_ball_valve(BV02_YD, BV02_Z, "BV\n02", C_BROWN)
    ax.annotate("", xy=(sx(EXIT_R - _AW), sz(BV02_Z)),
                xytext=(sx(EXIT_R), sz(BV02_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BROWN), zorder=11)
    ax.text(sx(EXIT_R + 5), sz(BV02_Z),
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

    # ── DIMENSIONS ──────────────────────────────────────────────────
    draw_dim_h(ax, sx(0), sx(PANEL_W), sz(-50),
               f"{PANEL_W}", offset=4.8, fs=6, color=C_DIM, font=FONT)
    draw_dim_h(ax, sx(PUMP_COL - PUMP_W / 2), sx(PUMP_COL + PUMP_W / 2),
               sz(P01_Z - 15),
               f"{PUMP_W}", offset=3.2, fs=5.5, color=C_DIM, font=FONT)
    draw_dim_v(ax, sx(PUMP_COL + PUMP_W / 2 + 15),
               sz(P01_Z), sz(P01_Z + PUMP_H),
               f"{PUMP_H}", offset=4.8, fs=5.5, color=C_DIM,
               right=True, font=FONT)
    draw_dim_v(ax, sx(-30), sz(0), sz(PANEL_H),
               f"{PANEL_H}", offset=8.0, fs=7, color=C_DIM,
               right=False, font=FONT)
    ax.text(sx(PANEL_W + 30), sz(0),
            f"Z={PANEL_Z_AFF}\nAFF", ha="left", va="center",
            fontsize=5.5, color=C_DIM, zorder=10, **FONT)

    # ── LEADERS ─────────────────────────────────────────────────────
    leader(ax,
           sx(PUMP_COL - PUMP_W / 2), sz(P01_Z + PUMP_H / 2),
           sx(X_SHOW_L + 10), sz(P01_Z + PUMP_H / 2 - 60),
           "Shurflo 2088\n12V · 3.5 GPM · 45 PSI\n(4 pumps on SS L-brackets)",
           fs=5.5, color=C_PUMP_EC, font=FONT)
    leader(ax,
           sx(ACC_YD - ACC_OD / 2), sz(ACC_Z + ACC_LEN / 2),
           sx(ACC_YD - 200), sz(ACC_Z + ACC_LEN / 2 + 60),
           "ACC-01: 0.75L ACCUM.\nO/127 × 200mm\n1/2\" MNPT (bottom)",
           fs=5.5, color=C_BLUE_EC, font=FONT)
    max_depth = PUMP_D
    leader(ax,
           sx(PUMP_COL), sz(PANEL_H + 10),
           sx(X_SHOW_L + 50), sz(PANEL_H + 40),
           f"MAX PROTRUSION: {max_depth}mm\nFROM PANEL FACE (in -X)",
           fs=5.5, color=C_NEW, font=FONT)

    # ── CROSS-SECTION STRIP ─────────────────────────────────────────
    _corridor_cross_section()

    # ── NOTES ───────────────────────────────────────────────────────
    notes = [
        "CORRIDOR PLUMBING PANEL — IBC PLUMBING CORRIDOR:",
        f"1. Panel: 18mm marine ply spanning corridor Yd={PANEL_YD}-{PANEL_YD + PANEL_W} (270mm).",
        f"2. Panel face at X={PANEL_WALL_X}, equipment protrudes toward open end (-X direction).",
        f"3. Panel height: Z={PANEL_Z_AFF}-{PANEL_Z_AFF + PANEL_H}mm AFF ({PANEL_H}mm).",
        "4. LEFT COL: P-01 (Blue supply) + P-04 (Tray drain) + ACC-01.",
        "5. RIGHT COL: P-03 (Waste evac) + P-05 (Brown drain) + DV-02 + SV-02.",
        "6. BV-01 (P-01 suction), BV-02 (P-05 suction), BV-06 (P-03 suction) — manual ball valves.",
        "7. SV-02: pH sample tap on the P-04 tray-drain discharge, before DV-02.",
        "8. DV-02: 3-way diverter — tray sump to IBC-3 or IBC-4.",
        f"9. Max protrusion: {max_depth}mm. Near IBCs LEFT, far IBCs RIGHT in this view.",
        "10. Brown recycle / filter train is on the PINHOLE WALL panel (separate sheet).",
    ]
    draw_notes(ax, notes, 575, 300, spacing=14,
               fs=6, width=470, color=C_DIM, title_color=C_NEW, font=FONT)

    # ── TITLE BLOCK ─────────────────────────────────────────────────
    title_block(ax, "CORRIDOR PANEL",
                drawing_title="CORRIDOR PLUMBING PANEL",
                subtitle="FRONT ELEVATION + PIPE ROUTING + CROSS-SECTION",
                scale_note="ELEV 1:80 · X-SECTION NTS · AXES IN mm",
                doc_id="TBS-001 · Plumbing Panel",
                height=0.028)

    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    out = os.path.join(DIAGRAMS_DIR, "panel-layout.png")
    fig.savefig(out, dpi=150, facecolor="white", edgecolor="none",
                bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print(f"Corridor panel → {out}")


# ── Shared pump symbol ─────────────────────────────────────────────────────
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


# ═══════════════════════════════════════════════════════════════════════════
#  CROSS-SECTION STRIP — panel position relative to walkway (Yd × Z)
# ═══════════════════════════════════════════════════════════════════════════
def _corridor_cross_section():
    CS_LEFT  = 48
    CS_BOT   = 160
    CS_W_IN  = 480
    CS_H_IN  = 80
    IBC_NEAR_YD = 30
    IBC_NEAR_END = IBC_NEAR_YD + IBC_D
    CORRIDOR_FAR = IBC_NEAR_END + 270
    YD_MAX = 1450
    Z_CS_MAX = 250

    def cs_yd(yd_mm):
        return CS_LEFT + yd_mm / YD_MAX * CS_W_IN

    def cs_z(z_mm):
        return CS_BOT + z_mm / Z_CS_MAX * CS_H_IN

    ax.text(CS_LEFT + CS_W_IN / 2, CS_BOT + CS_H_IN + 16,
            "CROSS-SECTION — PANEL IN IBC CORRIDOR (looking along X axis)",
            ha="center", va="bottom",
            fontsize=6.5, color=C_DIM, fontweight="bold", zorder=10, **FONT)
    ax.plot([cs_yd(0), cs_yd(0)], [cs_z(-20), cs_z(Z_CS_MAX)],
            color=C_WALL, lw=4.0, zorder=3)
    ax.text(cs_yd(0) - 4, cs_z(Z_CS_MAX / 2),
            "WALL\nYd=0", ha="right", va="center",
            fontsize=4, color=C_WALL_HATCH, zorder=10, **FONT)
    ax.plot([cs_yd(0), cs_yd(YD_MAX)], [cs_z(0), cs_z(0)],
            color=C_OUT, lw=1.5, zorder=3)
    ax.add_patch(mpatches.Rectangle(
        (cs_yd(0), cs_z(0)), WALKWAY_W / YD_MAX * CS_W_IN, WALKWAY_Z / Z_CS_MAX * CS_H_IN,
        fc=C_WALK, ec=C_NEW, lw=1.0, zorder=4, alpha=0.6))
    ax.text(cs_yd(WALKWAY_W / 2), cs_z(WALKWAY_Z / 2),
            "WALKWAY\n300mm", ha="center", va="center",
            fontsize=4, color=C_NEW, fontweight="bold", zorder=5, **FONT)
    C_IBC_CS = "#E0D8C8"
    C_IBC_CS_EC = "#B0A898"
    ax.add_patch(mpatches.Rectangle(
        (cs_yd(IBC_NEAR_YD), cs_z(0)),
        IBC_D / YD_MAX * CS_W_IN, cs_z(Z_CS_MAX) - cs_z(0),
        fc=C_IBC_CS, ec=C_IBC_CS_EC, lw=1.0, zorder=2, alpha=0.35))
    ax.text(cs_yd(IBC_NEAR_YD + IBC_D / 2), cs_z(Z_CS_MAX * 0.5),
            "NEAR IBC\nCOLUMN", ha="center", va="center",
            fontsize=4.5, color=C_IBC_CS_EC, zorder=3, **FONT)
    ax.add_patch(mpatches.Rectangle(
        (cs_yd(CORRIDOR_FAR), cs_z(0)),
        (YD_MAX - CORRIDOR_FAR) / YD_MAX * CS_W_IN, cs_z(Z_CS_MAX) - cs_z(0),
        fc=C_IBC_CS, ec=C_IBC_CS_EC, lw=1.0, zorder=2, alpha=0.35))
    ax.text(cs_yd((CORRIDOR_FAR + YD_MAX) / 2), cs_z(Z_CS_MAX * 0.5),
            "FAR IBC\nCOLUMN", ha="center", va="center",
            fontsize=4.5, color=C_IBC_CS_EC, zorder=3, **FONT)
    for yd_edge in [IBC_NEAR_END, CORRIDOR_FAR]:
        ax.plot([cs_yd(yd_edge), cs_yd(yd_edge)], [cs_z(0), cs_z(Z_CS_MAX)],
                color=C_IBC_CS_EC, lw=1.0, zorder=3)
    panel_left_draw = cs_yd(IBC_NEAR_END)
    panel_w_draw = (CORRIDOR_FAR - IBC_NEAR_END) / YD_MAX * CS_W_IN
    ax.add_patch(mpatches.Rectangle(
        (panel_left_draw, cs_z(40)),
        panel_w_draw, cs_z(200) - cs_z(40),
        fc=C_PLY, ec=C_PLY_EC, lw=1.5, zorder=5, alpha=0.7))
    ax.text(cs_yd((IBC_NEAR_END + CORRIDOR_FAR) / 2), cs_z(120),
            f"18mm PANEL\nSPANS CORRIDOR\n(Z={PANEL_Z_AFF}-{PANEL_Z_AFF + PANEL_H})",
            ha="center", va="center",
            fontsize=4.0, color=C_PLY_EC, fontweight="bold", zorder=10, **FONT)
    draw_dim_h(ax, cs_yd(IBC_NEAR_END), cs_yd(CORRIDOR_FAR), cs_z(Z_CS_MAX + 10),
               "270 CORRIDOR", offset=3.2, fs=5.5, color=C_DIM, font=FONT)
    ax.text(cs_yd(YD_MAX / 2), cs_z(-15) - 14.4,
            "Yd (mm from pinhole wall) →", ha="center", va="top",
            fontsize=5.5, color=C_DIM, zorder=10, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  PINHOLE WALL PLUMBING PANEL — FRONT ELEVATION
#  Brown recycle / filter train: P-02 + F-01/F-02/F-03 + DV-01 + SV-01 + BV-03.
#  Flow: IBC-3 Brown → BV-03 → P-02 → F-01 → F-02 → F-03 → SV-01 → DV-01 →
#        (Blue recycle / Waste).
# ═══════════════════════════════════════════════════════════════════════════
def draw_pinhole_panel():
    fig = _new_panel_fig()

    # Title above panel
    ax.text(sx(PANEL_W / 2), sz(Z_SHOW_R) + 12,
            "FRONT ELEVATION — PINHOLE WALL PLUMBING PANEL",
            ha="center", va="bottom",
            fontsize=8, color=C_DIM, fontweight="bold", zorder=10, **FONT)

    # Panel outline (18mm plywood)
    rect(0, 0, PANEL_W, PANEL_H,
         C_PLY, C_PLY_EC, lw=2.0, zorder=3, alpha=0.5)
    ax.text(sx(PANEL_W / 2), sz(PANEL_H - 30),
            f"18mm MARINE PLY\n{PANEL_W}mm x {PANEL_H}mm",
            ha="center", va="top",
            fontsize=5.5, color=C_PLY_EC, zorder=4, **FONT)

    # ── P-02 (Brown recycle pump), centered above filter stack ────────────
    P02_PORT_Z = P02_Z + PUMP_H - 25
    _draw_pump(P02_COL, P02_PORT_IN_YD, P02_PORT_OUT_YD,
               P02_Z, "P-02", "BROWN\nRECYCLE", C_BROWN, C_BROWN_EC)
    ax.text(sx(P02_COL), sz(P02_Z - 30),
            "RECYCLE PUMP", ha="center", va="top",
            fontsize=6, color=C_PUMP_EC, fontweight="bold", zorder=10, **FONT)

    # ── FILTER STACK (F-01 top → F-03 bottom, gravity-fed series) ─────────
    F_IN_YD  = FILT_COL - 35
    F_OUT_YD = FILT_COL + 35
    filter_specs = [
        ("F-01", "50µm\nSED.", F01_Z),
        ("F-02", "5µm\nSED.",  F02_Z),
        ("F-03", "GAC\nCARBON", F03_Z),
    ]
    for fname, fdesc, fz in filter_specs:
        rect(FILT_COL - FILT_OD / 2, fz, FILT_OD, FILT_H,
             C_FILTER, C_OUT, lw=1.2, zorder=6, alpha=0.6)
        rect(FILT_COL - FILT_OD / 2, fz + FILT_H - FILT_HEAD, FILT_OD, FILT_HEAD,
             "#3A70B0", C_OUT, lw=0.8, zorder=6, alpha=0.7)
        ax.plot([sx(FILT_COL - FILT_OD / 2), sx(FILT_COL + FILT_OD / 2)],
                [sz(fz + 60), sz(fz + 60)],
                color=C_OUT, lw=0.5, ls="--", zorder=7)
        for port_off in [-35, 35]:
            circ(FILT_COL + port_off, fz + FILT_H - FILT_HEAD / 2, 12,
                 "#B8D4F0", C_OUT, lw=0.4, zorder=7, alpha=0.6)
        ax.text(sx(FILT_COL), sz(fz + FILT_H / 2 + 25),
                fname, ha="center", va="center",
                fontsize=7, color="white", fontweight="bold", zorder=8, **FONT)
        ax.text(sx(FILT_COL), sz(fz + FILT_H / 2 - 15),
                fdesc, ha="center", va="center",
                fontsize=4.5, color="white", zorder=8, **FONT)
        rect(FILT_COL - FILT_OD / 2 - 10, fz + FILT_H,
             FILT_OD + 20, 10,
             C_FRAME_FILL, C_FRAME, lw=0.5, zorder=5)
    ax.text(sx(FILT_COL), sz(F03_Z - 20),
            "FILTER STACK (×3)", ha="center", va="top",
            fontsize=6, color=C_FILTER, fontweight="bold", zorder=10, **FONT)

    # ── PLUMBING ──────────────────────────────────────────────────────────
    EXIT_L = -60
    EXIT_R = 330
    F01_HEAD_Z = F01_Z + FILT_H - FILT_HEAD / 2
    F02_HEAD_Z = F02_Z + FILT_H - FILT_HEAD / 2
    F03_HEAD_Z = F03_Z + FILT_H - FILT_HEAD / 2
    JMPR_RAIL1 = FILT_COL + FILT_OD // 2 + 10
    JMPR_RAIL2 = JMPR_RAIL1 + 15

    BV03_YD = P02_PORT_IN_YD               # P-02 suction isolation
    BV03_Z  = P02_PORT_Z + SUCT_RISE

    # Brown suction: IBC-3 (RIGHT) → BV-03 → 90° elbow → P-02 inlet
    _P02_SUCT_Z = P02_PORT_Z + SUCT_RISE
    draw_pipe_path(ax,
        [EXIT_R, BV03_YD, BV03_YD],
        [_P02_SUCT_Z, _P02_SUCT_Z, P02_PORT_Z],
        PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
    draw_ball_valve(BV03_YD, BV03_Z, "BV\n03", C_BROWN)
    ax.annotate("", xy=(sx(EXIT_R - _AW), sz(_P02_SUCT_Z)),
                xytext=(sx(EXIT_R), sz(_P02_SUCT_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BROWN), zorder=11)
    ax.text(sx(EXIT_R + 5), sz(_P02_SUCT_Z),
            "FROM\nIBC-3\n(BROWN)", ha="left", va="center",
            fontsize=5.5, color=C_BROWN, zorder=10, **FONT)

    # P-02 discharge: outlet (LEFT port) → drop → left → down to F-01 IN
    draw_pipe_path(ax,
        [P02_PORT_OUT_YD, P02_PORT_OUT_YD, F_IN_YD, F_IN_YD],
        [P02_PORT_Z, P02_PORT_Z - 60, P02_PORT_Z - 60, F01_HEAD_Z],
        PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)

    # Filter jumpers — gravity-fed downward: F-01 → F-02 → F-03
    _JMPR_DROP = 50
    draw_pipe_path(ax,
        [F_OUT_YD, JMPR_RAIL1, JMPR_RAIL1, F_IN_YD, F_IN_YD],
        [F01_HEAD_Z, F01_HEAD_Z, F02_HEAD_Z + _JMPR_DROP,
         F02_HEAD_Z + _JMPR_DROP, F02_HEAD_Z],
        PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
    draw_pipe_path(ax,
        [F_OUT_YD, JMPR_RAIL2, JMPR_RAIL2, F_IN_YD, F_IN_YD],
        [F02_HEAD_Z, F02_HEAD_Z, F03_HEAD_Z + _JMPR_DROP,
         F03_HEAD_Z + _JMPR_DROP, F03_HEAD_Z],
        PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)

    # F-03 OUT → filtered line right → SV-01 sample tap → DV-01
    DV01_YD = R_COL
    DV01_Z  = F03_HEAD_Z
    draw_pipe_path(ax,
        [F_OUT_YD, DV01_YD - BV_R],
        [F03_HEAD_Z, DV01_Z],
        PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)

    # SV-01 pH sample tap — branch DOWN off the filtered line, BEFORE DV-01
    SV01_YD = F_OUT_YD + (DV01_YD - BV_R - F_OUT_YD) * 0.5
    SV01_Z  = F03_HEAD_Z - 95
    draw_pipe_path(ax,
        [SV01_YD, SV01_YD],
        [F03_HEAD_Z, SV01_Z + BV_R],
        PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN + 0.5)
    draw_ball_valve(SV01_YD, SV01_Z, "SV\n01", C_BROWN)
    ax.annotate("", xy=(sx(SV01_YD), sz(SV01_Z - BV_R - 35)),
                xytext=(sx(SV01_YD), sz(SV01_Z - BV_R)),
                arrowprops=dict(**_arrow_kw, color=C_BROWN), zorder=11)
    leader(ax, sx(SV01_YD), sz(SV01_Z), sx(EXIT_L - 5), sz(SV01_Z - 40),
           "SV-01 — pH sample tap\n(filtered line, before DV-01;\ndraw sample, meter, then set DV-01)",
           fs=6, color=C_BROWN, ha="right", va="center", font=FONT)

    # DV-01 (3-way diverter — filtered → IBC-2 Blue recycle / IBC-4 Waste)
    draw_ball_valve(DV01_YD, DV01_Z, "DV\n01", C_BROWN_EC)
    # DV-01 Blue-recycle output → IBC-2: exits RIGHT
    draw_pipe_path(ax,
        [DV01_YD + BV_R, EXIT_R],
        [DV01_Z, DV01_Z],
        PIPE_OD, PIPE_WALL, fc=C_BLUE, zorder=Z_BLUE)
    ax.annotate("", xy=(sx(EXIT_R), sz(DV01_Z)),
                xytext=(sx(EXIT_R - _AW), sz(DV01_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BLUE), zorder=11)
    ax.text(sx(EXIT_R + 5), sz(DV01_Z),
            "TO IBC-2\n(BLUE\nRECYCLE)", ha="left", va="center",
            fontsize=5.5, color=C_BLUE, zorder=10, **FONT)
    # DV-01 Waste output → IBC-4: exits BOTTOM then RIGHT
    _DV_WASTE_Z = DV01_Z - 30
    draw_pipe_path(ax,
        [DV01_YD, DV01_YD, EXIT_R],
        [DV01_Z - BV_R, _DV_WASTE_Z, _DV_WASTE_Z],
        PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)
    ax.annotate("", xy=(sx(EXIT_R), sz(_DV_WASTE_Z)),
                xytext=(sx(EXIT_R - _AW), sz(_DV_WASTE_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BLACK_SYS), zorder=11)
    ax.text(sx(EXIT_R + 5), sz(_DV_WASTE_Z),
            "TO IBC-4\n(WASTE)", ha="left", va="center",
            fontsize=5.5, color=C_BLACK_SYS, zorder=10, **FONT)

    # ── DIMENSIONS ──────────────────────────────────────────────────
    draw_dim_h(ax, sx(0), sx(PANEL_W), sz(-50),
               f"{PANEL_W}", offset=4.8, fs=6, color=C_DIM, font=FONT)
    draw_dim_h(ax, sx(FILT_COL - FILT_OD / 2), sx(FILT_COL + FILT_OD / 2),
               sz(F03_Z - 15),
               f"O/{FILT_OD}", offset=3.2, fs=5.5, color=C_FILTER, font=FONT)
    draw_dim_v(ax, sx(FILT_COL - FILT_OD / 2 - 20),
               sz(F03_Z), sz(F03_Z + FILT_H),
               f"{FILT_H}", offset=6.4, fs=6, color=C_FILTER,
               right=True, font=FONT)
    draw_dim_v(ax, sx(FILT_COL + FILT_OD / 2 + 70),
               sz(F03_Z), sz(FILT_STACK_TOP),
               f"{FILT_STACK_TOP}", offset=6.4, fs=6, color=C_DIM,
               right=True, font=FONT)
    draw_dim_v(ax, sx(P02_COL + PUMP_W / 2 + 15),
               sz(P02_Z), sz(P02_Z + PUMP_H),
               f"{PUMP_H}", offset=4.8, fs=5.5, color=C_DIM,
               right=True, font=FONT)
    draw_dim_v(ax, sx(-30), sz(0), sz(PANEL_H),
               f"{PANEL_H}", offset=8.0, fs=7, color=C_DIM,
               right=False, font=FONT)
    draw_dim_v(ax, sx(FILT_COL - FILT_OD / 2 - 20),
               sz(F03_Z + FILT_H), sz(F02_Z),
               f"{FILT_GAP}", offset=4.8, fs=5, color=C_DIM,
               right=False, font=FONT)
    ax.text(sx(PANEL_W + 30), sz(0),
            f"Z={PANEL_Z_AFF}\nAFF", ha="left", va="center",
            fontsize=5.5, color=C_DIM, zorder=10, **FONT)

    # ── LEADERS ─────────────────────────────────────────────────────
    leader(ax,
           sx(P02_COL - PUMP_W / 2), sz(P02_Z + PUMP_H / 2),
           sx(X_SHOW_L + 10), sz(P02_Z + PUMP_H / 2 + 60),
           "P-02 Shurflo 2088\n12V · 3.5 GPM · 45 PSI\n(Brown recycle, SS L-bracket)",
           fs=5.5, color=C_PUMP_EC, font=FONT)
    leader(ax,
           sx(FILT_COL + FILT_OD / 2), sz(F01_Z + FILT_H / 2),
           sx(PANEL_W + 40), sz(F01_Z + FILT_H / 2 + 30),
           "4.5\"×10\" FILTER HOUSING\n1\" NPT IN/OUT\n(×3 separate, sump-down)",
           fs=5.5, color=C_FILTER, font=FONT)
    max_depth = max(PUMP_D, FILT_OD)
    leader(ax,
           sx(FILT_COL), sz(PANEL_H + 10),
           sx(X_SHOW_L + 50), sz(PANEL_H + 40),
           f"MAX PROTRUSION: {max_depth}mm\nFROM PANEL FACE (in -X)",
           fs=5.5, color=C_NEW, font=FONT)

    # ── NOTES ───────────────────────────────────────────────────────
    notes = [
        "PINHOLE WALL PLUMBING PANEL — BROWN RECYCLE / FILTER TRAIN:",
        f"1. Panel: 18mm marine ply, {PANEL_W}mm × {PANEL_H}mm, mounted on the pinhole wall.",
        "2. P-02 (Brown recycle pump) feeds the 3-stage filter stack.",
        "3. FILTERS: F-01 (50µm, top) → F-02 (5µm) → F-03 (GAC, bottom) — gravity-fed series flow.",
        "4. BV-03: P-02 suction isolation (manual ball valve).",
        "5. SV-01: pH sample tap on the filtered line, BEFORE DV-01.",
        "6. DV-01: 3-way diverter — filtered water to IBC-2 (Blue recycle) or IBC-4 (Waste).",
        "7. Flow: IBC-3 → BV-03 → P-02 → F-01 → F-02 → F-03 → SV-01 → DV-01 → Blue recycle / Waste.",
        f"8. Max protrusion: {max_depth}mm from the panel face (in -X).",
    ]
    draw_notes(ax, notes, 575, 300, spacing=14,
               fs=6, width=470, color=C_DIM, title_color=C_NEW, font=FONT)

    # ── TITLE BLOCK ─────────────────────────────────────────────────
    title_block(ax, "PINHOLE WALL PANEL",
                drawing_title="PINHOLE WALL PLUMBING PANEL",
                subtitle="FRONT ELEVATION + FILTER TRAIN PIPE ROUTING",
                scale_note="ELEV 1:80 · AXES IN mm",
                doc_id="TBS-001 · Plumbing Panel",
                height=0.028)

    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    out = os.path.join(DIAGRAMS_DIR, "pinhole-panel.png")
    fig.savefig(out, dpi=150, facecolor="white", edgecolor="none",
                bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print(f"Pinhole wall panel → {out}")

# ── Render the two front-elevation panels ──────────────────────────────────
draw_corridor_panel()
draw_pinhole_panel()


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

# ── Plumbing panel (edge-on) + pumps on the front (-X) ──────────────────
_rect(PANX, EQPANEL_Z_LO, EQPANEL_T, EQPANEL_Z_HI - EQPANEL_Z_LO, C_PLYB, lw=1.3, z0=6)
leader(axb, PANX + EQPANEL_T / 2, 700, 5150, 560,
       f"PLUMBING PANEL\n18mm ply (edge-on)\nZ={EQPANEL_Z_LO}–{EQPANEL_Z_HI}", color=C_OUT, fs=6,
       ha="center", va="top", arrow_style="-|>", font=FB)
for zr, lbl, hot in [(Z_BOT, "P-01 /\nP-03", False),
                     (Z_MID, "P-04 /\nP-05", True),
                     (Z_TOP, "ACC-01", True)]:
    _rect(PANX - 100, zr, 100, 218, "#E6D9F0" if hot else "#EAEAEA",
          ec=C_OUT, lw=0.9, z0=5)
    axb.text(PANX - 50, zr + 109, lbl, fontsize=6, ha="center", va="center",
             color="#333", fontweight="bold", **FB)
axb.text(PANX - 50, Z_TOP - 70, "PUMPS\n(front face)", fontsize=5.5, ha="center",
         va="top", color="#777", style="italic", **FB)

# ── Circuit C pump power: feed → distribution block → 5 pump switches ─────
# 12V DC Circuit C drops from the ceiling to a distribution block above the pumps;
# one IP-rated switch per pump (P-01..P-05, run one at a time). P-02 lives on the
# Pinhole Wall panel and shares Circuit C. In this Yd-section the corridor pump
# columns overlap, so each row carries a pair.
CWIRE = "#1565C0"
busx = PANX - 135                                # wiring bus, just left of the pumps
db_z = 2210                                      # distribution block, above the pumps
axb.plot([busx, busx], [C_HGT, db_z], color=CWIRE, lw=1.4, zorder=12)     # feed
_rect(busx - 42, db_z - 4, 66, 32, "#D9E8F7", ec=CWIRE, lw=1.0, z0=12)
axb.text(busx - 9, db_z + 12, "Cct C\nDIST", fontsize=4.3, ha="center", va="center",
         color=CWIRE, fontweight="bold", **FB)
axb.plot([busx, busx], [db_z - 4, Z_BOT + 80], color=CWIRE, lw=1.2, zorder=11)  # bus
for zr in (Z_BOT, Z_MID, Z_TOP):
    swz = zr + 109
    _rect(busx - 12, swz - 12, 24, 24, "white", ec=CWIRE, lw=0.9, z0=13)   # switch
    axb.plot([busx + 12, PANX - 100], [swz, swz], color=CWIRE, lw=1.0, zorder=12)  # branch
leader(axb, busx - 24, db_z + 40, 5180, 2210,
       "CIRCUIT C POWER — 12V feed → distribution block →\n5 IP-rated switches (one per pump, P-01..P-05;\nrun one at a time). P-02 is on the Pinhole Wall\npanel and shares Circuit C. Rows = corridor pairs.",
       color=CWIRE, fs=5.5, ha="left", va="center", arrow_style="-|>", font=FB)

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
    "CORRIDOR PLUMBING PANEL — BACKSIDE (corridor side section, looking along Yd):",
    "1. Pumps mount on the FRONT face (−X); the drain risers + spine are on the BACK (+X), in the corridor gap (clear of both tote columns).",
    "2. Drain-riser spine: 18mm ply teed perpendicular off the panel (a T in plan), full panel height (Z=250–2310). v2: the Blue fill side-enters near the tote tops — no over-the-top trunk or shelf.",
    "3. The X3/X4 risers clamp to the spine face on SS P-clips at ~400mm centers.",
    "4. Risers feed from the pump discharges — P-05→X3 (Brown) @ Z=1946, P-03→X4 (Waste) @ Z=1578 — down to the sealed end-wall ports.",
    "5. Circuit C powers all 5 pumps (one IP switch each, run one at a time); P-02 lives on the Pinhole Wall panel and shares Circuit C.",
], 5985, 2380, spacing=64, fs=7, ha="left", width=600, font=FB)

title_block(axb, "CORRIDOR PANEL — BACKSIDE",
            drawing_title="CORRIDOR PLUMBING PANEL — BACKSIDE",
            subtitle="DRAIN-RISER SPINE · X3/X4 RISERS · X1/X3/X4 END-WALL PORTS",
            scale_note="CORRIDOR SIDE SECTION ALONG Yd · AXES IN mm",
            doc_id="TBS-001 · Plumbing Panel",
            height=0.05)

outb = os.path.join(DIAGRAMS_DIR, "panel-layout-back.png")
figb.savefig(outb, dpi=150, facecolor="white", edgecolor="none",
             bbox_inches="tight", pad_inches=0.2)
plt.close(figb)
print(f"Panel backside → {outb}")
