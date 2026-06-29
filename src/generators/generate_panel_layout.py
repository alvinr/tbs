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
# Single vertical column of four upright pumps + ACC-01 (matches the 3D
# massing_corridor_panel.py).  All pumps centered on the corridor center
# (3D Yd1181 → panel-Yd 135); IN/suction on the LEFT (panel-Yd 55 = 3D Yd1101,
# faces -Yd / near wall), OUT/discharge on the RIGHT (panel-Yd 215 = 3D Yd1261).
# Bottom→top: ACC-01 (dead-leg), P-01, P-04, P-05, P-03.  Panel-Z = (3D AFF Z) − 200.
PUMP_COL_C   = 135    # pump-column center (panel-Yd; 3D Yd1181 corridor center)
CORR_PORT_IN  = 55    # IN / suction port panel-Yd (3D Yd1101, faces near wall)
CORR_PORT_OUT = 215   # OUT / discharge port panel-Yd (3D Yd1261)

# Pump body bases (panel-Z = 3D AFF − 200):
P01_Z = 415                           # P-01 Blue supply
P04_Z = 740                           # P-04 Tray drain
P05_Z = 1140                          # P-05 Brown drain
P03_Z = 1540                          # P-03 Waste drain

# ACC-01 — Ø127 × 200 cylinder at the very bottom, below P-01.
ACC_YD = PUMP_COL_C
ACC_Z  = 155                          # ACC bottom (3D z355 − 200)

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

    # ── PUMPS — SINGLE VERTICAL COLUMN ────────────────────────────────────
    #   Bottom→top: ACC-01 (below P-01), P-01, P-04, P-05, P-03.  All centered
    #   on PUMP_COL_C; IN/suction LEFT (CORR_PORT_IN), OUT/discharge RIGHT.
    _draw_pump(PUMP_COL_C, CORR_PORT_IN, CORR_PORT_OUT,
               P01_Z, "P-01", "BLUE\nSUPPLY", C_BLUE, C_BLUE_EC)
    _draw_pump(PUMP_COL_C, CORR_PORT_IN, CORR_PORT_OUT,
               P04_Z, "P-04", "TRAY\nDRAIN", C_BLACK_SYS, C_BLACK_EC)
    _draw_pump(PUMP_COL_C, CORR_PORT_IN, CORR_PORT_OUT,
               P05_Z, "P-05", "BROWN\nDRAIN", C_BROWN, C_BROWN_EC)
    _draw_pump(PUMP_COL_C, CORR_PORT_IN, CORR_PORT_OUT,
               P03_Z, "P-03", "WASTE\nDRAIN", C_BLACK_SYS, C_BLACK_EC)

    # ── ACC-01 — Ø127 × 200 cylinder at the very bottom, below P-01 ───────
    rect(ACC_YD - ACC_OD / 2, ACC_Z, ACC_OD, ACC_LEN,
         C_ACC, C_BLUE_EC, lw=1.2, zorder=6, alpha=0.7)
    ax.text(sx(ACC_YD), sz(ACC_Z + ACC_LEN / 2 + 12),
            "ACC-01", ha="center", va="center",
            fontsize=7, color="white", fontweight="bold", zorder=8, **FONT)
    ax.text(sx(ACC_YD), sz(ACC_Z + ACC_LEN / 2 - 16),
            f"O/{ACC_OD}", ha="center", va="center",
            fontsize=5, color="white", zorder=8, **FONT)
    # ACC ports underneath (SeaFlo bottom-port bladder): IN +Yd, OUT -Yd
    for port_yd in [CORR_PORT_OUT, CORR_PORT_IN]:
        circ(port_yd, ACC_Z + 12, 9, C_PIPE_FILL, C_PIPE_EC, lw=0.5, zorder=10)
    clamp_w = ACC_OD + 20
    rect(ACC_YD - clamp_w / 2, ACC_Z + ACC_LEN, clamp_w, 8,
         C_FRAME_FILL, C_FRAME, lw=0.5, zorder=5)

    # ── Zone label ────────────────────────────────────────────────────────
    ax.text(sx(PANEL_W + 8), sz((P01_Z + P03_Z + PUMP_H) / 2),
            "PUMP COLUMN\n(4 transfer pumps,\nupright, in line)",
            ha="left", va="center",
            fontsize=5.5, color=C_PUMP_EC, fontweight="bold", zorder=10, **FONT)

    # ════════════════════════════════════════════════════════════════
    #  PLUMBING — suctions enter LEFT (via BV); discharges exit RIGHT
    # ════════════════════════════════════════════════════════════════
    EXIT_L = -70    # past left panel edge (near wall / walkway)
    EXIT_R = 340    # past right panel edge (far wall / sealed end)

    P01_PORT_Z = P01_Z + PUMP_H - 25
    P04_PORT_Z = P04_Z + PUMP_H - 25
    P05_PORT_Z = P05_Z + PUMP_H - 25
    P03_PORT_Z = P03_Z + PUMP_H - 25

    # Far-right discharge riser lane (clear of the OUT ports at CORR_PORT_OUT)
    DISCH_RISER = 255

    # ── BLUE SYSTEM (P-01) ──────────────────────────────────────────
    # Blue suction: IBC-1/2 (LEFT) → BV-01 → 90° elbow → P-01 inlet (LEFT port)
    _P01_SUCT_Z = P01_PORT_Z + SUCT_RISE
    BV01_YD = CORR_PORT_IN
    BV01_Z  = _P01_SUCT_Z
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

    # P-01 discharge: outlet (RIGHT port) → drop to ACC-01 inlet (right port,
    # dead-leg cylinder just below P-01).  Down the right side, around to ACC.
    _ACC_DROP_YD = CORR_PORT_OUT
    draw_pipe_path(ax,
        [CORR_PORT_OUT, CORR_PORT_OUT],
        [P01_PORT_Z, ACC_Z + 12],
        PIPE_OD, PIPE_WALL, fc=C_BLUE, zorder=Z_DISCH)
    # ACC-01 outlet (left port) → exit LEFT to spray bar / TAP-01
    draw_pipe_path(ax,
        [EXIT_L, CORR_PORT_IN, CORR_PORT_IN],
        [ACC_Z - 30, ACC_Z - 30, ACC_Z + 12],
        PIPE_OD, PIPE_WALL, fc=C_BLUE, zorder=Z_DISCH)
    ax.annotate("", xy=(sx(EXIT_L), sz(ACC_Z - 30)),
                xytext=(sx(EXIT_L + _AW), sz(ACC_Z - 30)),
                arrowprops=dict(**_arrow_kw, color=C_BLUE), zorder=11)
    ax.text(sx(EXIT_L - 5), sz(ACC_Z - 30),
            "TO SPRAY BAR\n/ TAP-01", ha="right", va="center",
            fontsize=5.5, color=C_BLUE, zorder=10, **FONT)

    # ── TRAY DRAIN (P-04) ────────────────────────────────────────────
    # P-04 suction: tray sump (LEFT) → P-04 inlet (LEFT port)
    _P04_SUCT_Z = P04_PORT_Z + SUCT_RISE
    draw_pipe_path(ax,
        [EXIT_L, CORR_PORT_IN, CORR_PORT_IN],
        [_P04_SUCT_Z, _P04_SUCT_Z, P04_PORT_Z],
        PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)
    ax.annotate("", xy=(sx(EXIT_L + _AW), sz(_P04_SUCT_Z)),
                xytext=(sx(EXIT_L), sz(_P04_SUCT_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BLACK_SYS), zorder=11)
    ax.text(sx(EXIT_L - 5), sz(_P04_SUCT_Z),
            "FROM\nTRAY\nSUMP", ha="right", va="center",
            fontsize=5.5, color=C_BLACK_SYS, zorder=10, **FONT)

    # P-04 discharge: outlet (RIGHT port) → up the far-right riser lane
    # (DISCH_RISER, clear of the OUT ports) → SV-02 pH tap → DV-02 (high).
    DV02_YD = DISCH_RISER
    DV02_Z  = 1945                        # 3D z2145 − 200
    SV02_Z  = 950                         # 3D z1150 − 200 (low on the riser)
    draw_pipe_path(ax,
        [CORR_PORT_OUT, DISCH_RISER, DISCH_RISER],
        [P04_PORT_Z, P04_PORT_Z, DV02_Z],
        PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK + 0.5)
    # SV-02 pH sample tap — small ball valve on the riser + downturned spout
    draw_ball_valve(DISCH_RISER, SV02_Z, "SV\n02", C_BLACK_EC)
    ax.annotate("", xy=(sx(DISCH_RISER + BV_R + 28), sz(SV02_Z)),
                xytext=(sx(DISCH_RISER + BV_R), sz(SV02_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BLACK_SYS), zorder=11)
    leader(ax, sx(DISCH_RISER + BV_R), sz(SV02_Z),
           sx(EXIT_R + 10), sz(SV02_Z - 120),
           "SV-02 — pH sample tap\n(P-04 discharge, before DV-02)",
           fs=6, color=C_BLACK_EC, ha="left", va="center", font=FONT)

    # DV-02 (3-way diverter — tray sump → IBC-3 Brown / IBC-4 Waste), high up.
    _DV_IBC4_Z = DV02_Z - 70
    draw_ball_valve(DV02_YD, DV02_Z, "DV\n02", C_BLACK_EC)
    # DV-02 Brown output → IBC-3: exits LEFT (brown)
    draw_pipe_path(ax,
        [EXIT_L, DV02_YD - BV_R],
        [DV02_Z, DV02_Z],
        PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_DISCH)
    ax.annotate("", xy=(sx(EXIT_L), sz(DV02_Z)),
                xytext=(sx(EXIT_L + _AW), sz(DV02_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BROWN), zorder=11)
    ax.text(sx(EXIT_L - 5), sz(DV02_Z),
            "TO\nIBC-3", ha="right", va="center",
            fontsize=5.5, color=C_BROWN, zorder=10, **FONT)
    # DV-02 Waste output → IBC-4: exits BOTTOM then RIGHT (grey/black)
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

    # ── BROWN DRAIN (P-05) ───────────────────────────────────────────
    # P-05 suction: IBC-3 Brown (LEFT) → BV-02 → P-05 inlet (LEFT port)
    _P05_SUCT_Z = P05_PORT_Z + SUCT_RISE
    BV02_YD = CORR_PORT_IN
    BV02_Z  = _P05_SUCT_Z
    draw_pipe_path(ax,
        [EXIT_L, CORR_PORT_IN, CORR_PORT_IN],
        [_P05_SUCT_Z, _P05_SUCT_Z, P05_PORT_Z],
        PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
    draw_ball_valve(BV02_YD, BV02_Z, "BV\n02", C_BROWN)
    ax.annotate("", xy=(sx(EXIT_L + _AW), sz(_P05_SUCT_Z)),
                xytext=(sx(EXIT_L), sz(_P05_SUCT_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BROWN), zorder=11)
    ax.text(sx(EXIT_L - 5), sz(_P05_SUCT_Z),
            "FROM\nIBC-3\n(BROWN)", ha="right", va="center",
            fontsize=5.5, color=C_BROWN, zorder=10, **FONT)
    # P-05 discharge: outlet (RIGHT port) → exit RIGHT to X3 port (behind panel).
    # It CROSSES the P-04 discharge riser (DISCH_RISER) — they do NOT join, so the
    # discharge is gap-broken at the crossing (skill_plumbing_drawing § crossings).
    _xg = PIPE_OD / 2 + 3
    draw_pipe_path(ax, [CORR_PORT_OUT, DISCH_RISER - _xg], [P05_PORT_Z, P05_PORT_Z],
                   PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
    draw_pipe_path(ax, [DISCH_RISER + _xg, EXIT_R], [P05_PORT_Z, P05_PORT_Z],
                   PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
    ax.annotate("", xy=(sx(EXIT_R), sz(P05_PORT_Z)),
                xytext=(sx(EXIT_R - _AW), sz(P05_PORT_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BROWN), zorder=11)
    ax.text(sx(EXIT_R + 5), sz(P05_PORT_Z),
            "TO X3\nPORT", ha="left", va="center",
            fontsize=5.5, color=C_BROWN, zorder=10, **FONT)

    # ── WASTE DRAIN (P-03) ───────────────────────────────────────────
    # P-03 suction: IBC-4 Waste (LEFT) → BV-06 → P-03 inlet (LEFT port)
    _P03_SUCT_Z = P03_PORT_Z + SUCT_RISE
    BV06_YD = CORR_PORT_IN
    BV06_Z  = _P03_SUCT_Z
    draw_pipe_path(ax,
        [EXIT_L, CORR_PORT_IN, CORR_PORT_IN],
        [_P03_SUCT_Z, _P03_SUCT_Z, P03_PORT_Z],
        PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)
    draw_ball_valve(BV06_YD, BV06_Z, "BV\n06", C_BLACK_EC)
    ax.annotate("", xy=(sx(EXIT_L + _AW), sz(_P03_SUCT_Z)),
                xytext=(sx(EXIT_L), sz(_P03_SUCT_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BLACK_SYS), zorder=11)
    ax.text(sx(EXIT_L - 5), sz(_P03_SUCT_Z),
            "FROM\nIBC-4\n(WASTE)", ha="right", va="center",
            fontsize=5.5, color=C_BLACK_SYS, zorder=10, **FONT)
    # P-03 discharge: outlet (RIGHT port) → exit RIGHT to X4 port (behind panel).
    # Gap-broken where it CROSSES the P-04 discharge riser (DISCH_RISER) — cross, not join.
    draw_pipe_path(ax, [CORR_PORT_OUT, DISCH_RISER - _xg], [P03_PORT_Z, P03_PORT_Z],
                   PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK + 0.5)
    draw_pipe_path(ax, [DISCH_RISER + _xg, EXIT_R], [P03_PORT_Z, P03_PORT_Z],
                   PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK + 0.5)
    ax.annotate("", xy=(sx(EXIT_R), sz(P03_PORT_Z)),
                xytext=(sx(EXIT_R - _AW), sz(P03_PORT_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BLACK_SYS), zorder=11)
    ax.text(sx(EXIT_R + 5), sz(P03_PORT_Z),
            "TO X4\nPORT", ha="left", va="center",
            fontsize=5.5, color=C_BLACK_SYS, zorder=10, **FONT)

    # ── DIMENSIONS ──────────────────────────────────────────────────
    draw_dim_h(ax, sx(0), sx(PANEL_W), sz(-50),
               f"{PANEL_W}", offset=4.8, fs=6, color=C_DIM, font=FONT)
    draw_dim_h(ax, sx(PUMP_COL_C - PUMP_W / 2), sx(PUMP_COL_C + PUMP_W / 2),
               sz(P01_Z - 15),
               f"{PUMP_W}", offset=3.2, fs=5.5, color=C_DIM, font=FONT)
    draw_dim_v(ax, sx(PUMP_COL_C + PUMP_W / 2 + 15),
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
           sx(PUMP_COL_C - PUMP_W / 2), sz(P04_Z + PUMP_H / 2),
           sx(X_SHOW_L + 10), sz(P04_Z + PUMP_H / 2 + 40),
           "Shurflo 2088\n12V · 3.5 GPM · 45 PSI\n(4 pumps on SS L-brackets)",
           fs=5.5, color=C_PUMP_EC, font=FONT)
    leader(ax,
           sx(ACC_YD - ACC_OD / 2), sz(ACC_Z + ACC_LEN / 2),
           sx(ACC_YD - 200), sz(ACC_Z + ACC_LEN / 2 + 60),
           "ACC-01: 0.75L ACCUM.\nO/127 × 200mm\n1/2\" MNPT (bottom)",
           fs=5.5, color=C_BLUE_EC, font=FONT)
    max_depth = PUMP_D
    leader(ax,
           sx(PUMP_COL_C), sz(PANEL_H + 10),
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
        "4. SINGLE vertical pump column (bottom→top): ACC-01, P-01 (Blue supply),",
        "    P-04 (Tray drain), P-05 (Brown drain), P-03 (Waste drain).",
        "5. ACC-01: 0.75L bladder accumulator on the Blue supply, dead-leg below P-01.",
        "6. Suctions enter on the LEFT through their isolation valve; discharges exit RIGHT.",
        "7. BV-01 (P-01 suction), BV-02 (P-05 suction), BV-06 (P-03 suction) — manual ball valves.",
        "8. SV-02: pH sample tap on the P-04 tray-drain discharge riser, before DV-02.",
        "9. DV-02: 3-way tray-sump diverter (high) — to IBC-3 (Brown) or IBC-4 (Waste).",
        f"10. Max protrusion: {max_depth}mm. Brown filter train is on the PINHOLE WALL panel.",
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
#  PINHOLE WALL PLUMBING PANEL — WALL ELEVATION (looking at the Yd≈0 wall)
#  Horizontal axis = X (mm along the container); vertical axis = Z (mm AFF).
#  Wide backing board with a HORIZONTAL filter bank high on the wall:
#    P-02 (Brown recycle) + F-01/F-02/F-03 Big Blue filters, then SV-01 pH tap
#    near the bottom-right; 3W-DV-01 lives off-board at the corridor mouth.
#  Flow (right→left in this mirrored elevation): IBC-3 Brown → BV-03 → P-02 → F-01 → F-02 → F-03 →
#                     SV-01 → 3W-DV-01 → (Blue recycle IBC-2 / Waste IBC-4).
#  Matches the live 3D (massing_pinhole_wall.py: kit() + backing()).
# ═══════════════════════════════════════════════════════════════════════════
def draw_pinhole_panel():
    # Local X×Z scale (this elevation is wide, not the corridor panel-Yd strip).
    PW_XL, PW_XR = 2680, 5060          # view X bounds (mm)
    PW_ZB, PW_ZT = 820, 2440           # view Z bounds (mm)
    PW_OX, PW_OZ = 90, 200             # drawing-unit origin offsets
    PW_KX = 0.62                       # X mm→unit (board ~1720mm → ~1066 units)

    # MIRRORED X: +X (sealed end / corridor / DV-01) draws to the LEFT — this is
    # the view standing INSIDE the container looking at the pinhole wall, so the
    # filter train reads F-03→F-02→F-01 left-to-right and DV-01 exits off the left.
    def pwx(x_mm): return PW_OX + (PW_XR - x_mm) * PW_KX
    def pwz(z_mm): return PW_OZ + (z_mm - PW_ZB)

    fig, ax_p = plt.subplots(1, 1, figsize=(16, 13), dpi=200)
    ax_p.set_xlim(0, (PW_XR - PW_XL) * PW_KX + 2 * PW_OX)
    ax_p.set_ylim(0, (PW_ZT - PW_ZB) + 2 * PW_OZ)
    ax_p.set_aspect("auto")
    ax_p.axis("off")

    def pw_rect(x, z, w, h, fc, ec=C_FRAME, lw=1.0, zorder=5, alpha=1.0):
        # mirrored X: x+w is the LEFT screen edge (pwx decreases with x)
        ax_p.add_patch(mpatches.Rectangle(
            (pwx(x + w), pwz(z)), w * PW_KX, h, fc=fc, ec=ec, lw=lw,
            zorder=zorder, alpha=alpha))

    def pw_text(x, z, s, **kw):
        ax_p.text(pwx(x), pwz(z), s, zorder=kw.pop("zorder", 10), **kw, **FONT)

    def pw_pipe(xs, zs, fc, zorder=8, ec=C_FRAME):
        draw_pipe_path(ax_p, xs, zs, PIPE_OD, PIPE_WALL, fc=fc, ec=ec,
                       zorder=zorder, sxf=pwx, szf=pwz)

    def pw_arrow(x0, z0, x1, z1, color):
        ax_p.annotate("", xy=(pwx(x1), pwz(z1)), xytext=(pwx(x0), pwz(z0)),
                      arrowprops=dict(**_arrow_kw, color=color), zorder=11)

    def pw_valve(x, z, label, color, half=22):
        pts_x = [pwx(x), pwx(x) + half, pwx(x), pwx(x) - half]
        pts_z = [pwz(z) + half, pwz(z), pwz(z) - half, pwz(z)]
        ax_p.add_patch(plt.Polygon(list(zip(pts_x, pts_z)),
                       fc="white", ec=color, lw=1.5, zorder=12))
        ax_p.text(pwx(x), pwz(z), label, ha="center", va="center",
                  fontsize=4.5, color=color, fontweight="bold", zorder=13, **FONT)

    # Title above the board
    pw_text((PW_XL + PW_XR) / 2, PW_ZT + 60,
            "WALL ELEVATION — PINHOLE WALL PLUMBING PANEL",
            ha="center", va="bottom", fontsize=11, color=C_DIM,
            fontweight="bold")

    # ── Backing board (18mm marine ply) — X 2780–4500, Z 920–2360 ──────────
    BD_XL, BD_XR = 2780, 4500
    BD_ZB, BD_ZT = 920, 2360
    pw_rect(BD_XL, BD_ZB, BD_XR - BD_XL, BD_ZT - BD_ZB,
            C_PLY, C_PLY_EC, lw=2.0, zorder=3, alpha=0.5)
    pw_text(4360, 1960,
            f"{BD_XR - BD_XL} × {BD_ZT - BD_ZB}mm\n18mm MARINE PLY\n(pinhole wall)",
            ha="center", va="center", fontsize=6.5, color=C_PLY_EC, zorder=4)

    # ── Filter geometry (Big Blue 4.5x10: head block + Ø184 sump below) ────
    HEAD_ZB, HEAD_ZT = 2262, 2340      # head block Z band
    SUMP_ZB, SUMP_ZT = 2000, 2262      # cylindrical sump hanging below
    HEAD_Z = (HEAD_ZB + HEAD_ZT) / 2   # head-line port height
    filters = [
        ("F-01", "5µm\nSEDIMENT", 3208, 3392),
        ("F-02", "KDF-55",        3546, 3730),
        ("F-03", "CARBON\n(GAC)", 3884, 4068),
    ]
    for fname, fdesc, fxl, fxr in filters:
        fcx = (fxl + fxr) / 2
        # sump (cylinder) hanging below the head
        pw_rect(fxl, SUMP_ZB, fxr - fxl, SUMP_ZT - SUMP_ZB,
                C_FILTER, C_OUT, lw=1.2, zorder=6, alpha=0.55)
        # head block
        pw_rect(fxl - 6, HEAD_ZB, (fxr - fxl) + 12, HEAD_ZT - HEAD_ZB,
                "#3A70B0", C_OUT, lw=1.0, zorder=7, alpha=0.85)
        pw_text(fcx, (SUMP_ZB + SUMP_ZT) / 2 + 55, fname, ha="center",
                va="center", fontsize=8, color="white", fontweight="bold",
                zorder=8)
        pw_text(fcx, (SUMP_ZB + SUMP_ZT) / 2 - 25, fdesc, ha="center",
                va="center", fontsize=5, color="white", zorder=8)

    # ── P-02 (Brown recycle pump) — leftmost, upright pump symbol ──────────
    P2_XL, P2_XR = 3008, 3108
    P2_CX = (P2_XL + P2_XR) / 2
    P2_ZB, P2_ZT = SUMP_ZB, HEAD_ZT    # body spans the filter tier height
    pw_rect(P2_XL, P2_ZB, P2_XR - P2_XL, P2_ZT - P2_ZB,
            C_PUMP_BODY, C_PUMP_EC, lw=1.2, zorder=6)
    pw_rect(P2_XL - 4, HEAD_ZB, (P2_XR - P2_XL) + 8, HEAD_ZT - HEAD_ZB,
            "#4A4038", C_PUMP_EC, lw=0.8, zorder=7)   # motor head/cap
    pw_text(P2_CX, (P2_ZB + P2_ZT) / 2 + 35, "P-02", ha="center", va="center",
            fontsize=8, color=C_BROWN, fontweight="bold", zorder=8)
    pw_text(P2_CX, (P2_ZB + P2_ZT) / 2 - 15, "BROWN\nRECYCLE", ha="center",
            va="center", fontsize=5, color=C_BROWN_EC, zorder=8)

    # ════════════════════════════════════════════════════════════════
    #  FLOW — series along the head line at Z≈HEAD_Z (P-02 right → F-01 → F-02 →
    #  F-03 → SV-01 → DV-01 left, in this mirrored inside-the-container elevation)
    # ════════════════════════════════════════════════════════════════
    EXIT_L = 2740                       # IBC-3 / BV-03 inlet margin (draws to the RIGHT, mirrored)
    F1_CX, F2_CX, F3_CX = 3300, 3638, 3976
    F1_XL, F1_XR = 3208, 3392
    F3_XR = 4068

    # IBC-3 Brown → BV-03 → P-02 IN (left side of P-02, on the head line)
    BV03_X = 2880
    pw_pipe([EXIT_L, BV03_X, P2_XL], [HEAD_Z, HEAD_Z, HEAD_Z],
            C_BROWN, zorder=Z_BROWN)
    pw_valve(BV03_X, HEAD_Z, "BV\n03", C_BROWN, half=18)
    pw_arrow(EXIT_L, HEAD_Z, EXIT_L + 30, HEAD_Z, C_BROWN)
    pw_text(EXIT_L - 8, HEAD_Z + 70, "FROM IBC-3\n(BROWN)", ha="center",
            va="bottom", fontsize=6, color=C_BROWN, zorder=10)

    # P-02 OUT → F-01 IN, then F-01 → F-02 → F-03 (straight jumpers, head line)
    pw_pipe([P2_XR, F1_XL], [HEAD_Z, HEAD_Z], C_BROWN, zorder=Z_BROWN)
    pw_pipe([3392, 3546], [HEAD_Z, HEAD_Z], C_BROWN, zorder=Z_BROWN)   # F1→F2
    pw_pipe([3730, 3884], [HEAD_Z, HEAD_Z], C_BROWN, zorder=Z_BROWN)   # F2→F3

    # F-03 OUT → drops down at X≈4090 → SV-01 (pH sample tap, bottom-right)
    SV01_X = 4250
    SV01_Z = 1071                       # valve center (3D body z975 + ~96)
    F3_OUT_X = 4090
    pw_pipe([F3_XR, F3_OUT_X, F3_OUT_X, SV01_X, SV01_X],
            [HEAD_Z, HEAD_Z, SV01_Z, SV01_Z, SV01_Z],
            C_FILTER, zorder=Z_BROWN)
    pw_valve(SV01_X, SV01_Z, "SV\n01", C_BROWN, half=20)
    # SV-01 downturned sample spout dropping to ~Z885
    pw_pipe([SV01_X, SV01_X, SV01_X - 45, SV01_X - 45],
            [SV01_Z - 20, 960, 960, 905], C_BROWN, zorder=Z_BROWN)
    pw_arrow(SV01_X - 45, 925, SV01_X - 45, 890, C_BROWN)
    leader(ax_p, pwx(SV01_X), pwz(SV01_Z) + 22, pwx(4150), pwz(1380),
           "SV-01 — pH sample tap\n(filtered line, before DV-01;\n"
           "draw sample, meter, then set DV-01)",
           fs=6, color=C_BROWN, ha="left", va="bottom", font=FONT)

    # SV-01 → 3W-DV-01: the filtered line leaves the board's LEFT edge (mirrored
    # view — the corridor mouth / DV-01 sits on the sealed-end/+X side).
    DV01_EDGE_X = BD_XR + 40            # just past the board's (mirrored) left edge
    pw_pipe([SV01_X, DV01_EDGE_X], [SV01_Z, SV01_Z], C_FILTER, zorder=Z_BROWN)
    pw_arrow(DV01_EDGE_X - 30, SV01_Z, DV01_EDGE_X, SV01_Z, C_FILTER)
    leader(ax_p, pwx(DV01_EDGE_X), pwz(SV01_Z), pwx(DV01_EDGE_X) - 8, pwz(SV01_Z) - 150,
           "3W-DV-01 (corridor mouth):\npH-gated split →\n"
           "Blue recycle (IBC-2) / Waste (IBC-4)",
           fs=6, color=C_BROWN_EC, ha="right", va="top", font=FONT)

    # ── DIMENSIONS ──────────────────────────────────────────────────
    draw_dim_h(ax_p, pwx(BD_XR), pwx(BD_XL), pwz(BD_ZB - 50),
               f"{BD_XR - BD_XL}mm", offset=10, fs=7, color=C_DIM, font=FONT)
    draw_dim_v(ax_p, pwx(BD_XL) + 40, pwz(BD_ZB), pwz(BD_ZT),
               f"{BD_ZT - BD_ZB}mm", offset=12, fs=7, color=C_DIM,
               right=True, font=FONT)
    ax_p.text(pwx(F3_CX) + 90, pwz(HEAD_Z) + 20,
              f"FILTER HEAD\nZ={int(HEAD_Z)}mm AFF", ha="left", va="bottom",
              fontsize=5.5, color=C_FILTER, zorder=10, **FONT)
    ax_p.text(pwx(F1_CX), pwz(SUMP_ZB) - 14,
              f"SUMP BOTTOM Z={SUMP_ZB}", ha="center", va="top",
              fontsize=5.5, color=C_FILTER, zorder=10, **FONT)

    # ── LEADERS ─────────────────────────────────────────────────────
    leader(ax_p, pwx(P2_CX), pwz(P2_ZB), pwx(2880), pwz(1700),
           "P-02 Shurflo 2088\n12V · 3.5 GPM · 45 PSI\n(Brown recycle, upright)",
           fs=6, color=C_PUMP_EC, ha="left", va="center", font=FONT)
    leader(ax_p, pwx(F2_CX), pwz(SUMP_ZB + 40), pwx(3500), pwz(1640),
           "Big Blue 4.5\"×10\" housing\n(Ø184 sump, head Z2262–2340;\n"
           "F-01 5µm → F-02 KDF-55 → F-03 GAC)",
           fs=6, color=C_FILTER, ha="left", va="center", font=FONT)

    # ── NOTES ───────────────────────────────────────────────────────
    notes = [
        "PINHOLE WALL PLUMBING PANEL — BROWN WASH-RECYCLE FILTER TRAIN:",
        "1. Wide 18mm marine-ply backing board on the pinhole wall (Yd≈0),",
        "    X=2780–4500, Z=920–2360mm AFF.",
        "2. P-02 (Brown recycle pump) pulls IBC-3 Brown through the 3-stage filter bank.",
        "3. HORIZONTAL filter bank high on the wall: F-01 (5µm sediment) →",
        "    F-02 (KDF-55) → F-03 (carbon/GAC); Big Blue 4.5\"×10\" housings.",
        "4. BV-03: P-02 suction isolation (manual ball valve).",
        "5. SV-01: pH sample tap on the filtered line, before DV-01 (cup spout, near bottom-right).",
        "6. 3W-DV-01 is PHYSICALLY at the corridor mouth (off this wall) — the filtered",
        "    line leaves the board's bottom-right and splits there: pH-gated to Blue",
        "    recycle (IBC-2) or Waste (IBC-4).",
        "7. Flow: IBC-3 → BV-03 → P-02 → F-01 → F-02 → F-03 → SV-01 → 3W-DV-01.",
    ]
    draw_notes(ax_p, notes, pwx(2700), pwz(1560), spacing=46,
               fs=7, width=560, color=C_DIM, title_color=C_NEW, font=FONT)

    # ── TITLE BLOCK ─────────────────────────────────────────────────
    title_block(ax_p, "PINHOLE WALL PANEL",
                drawing_title="PINHOLE WALL PLUMBING PANEL",
                subtitle="WALL ELEVATION (X × Z) + FILTER TRAIN ROUTING",
                scale_note="WALL ELEVATION · AXES IN mm",
                doc_id="TBS-001 · Plumbing Panel",
                height=0.05)

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
from tbs_constants import (C_LEN, C_HGT, EXT_FILL_1_H)

FB = {"fontfamily": "monospace"}
C_PLYB   = "#D9C9A3"   # plywood (tan)
C_BROWNB = "#7A5230"   # brown developer drain
C_WASTEB = "#8A8A8A"   # waste/grey drain
C_BLUEB  = "#3A78C0"   # blue fill
C_WALLB  = "#C8C8C8"

# ── Geometry (matches massing_corridor_panel.py: BACK_X=5104 rear panel) ──
PANX   = 5104                     # rear-panel front face (pumps hang -X off it)
PANX1  = 5122                     # rear-panel rear face (18mm ply)
SHIRTX0, SHIRTX1 = 5052, 5077     # 25mm pump-mount shirt (in FRONT of the panel)
SHIRT_ZB, SHIRT_ZT = 275, 1925    # shirt Z extent
SPX1   = 5560                     # drain-riser spine rear (X5104–5560)
SPINE_ZB, SPINE_ZT = 280, 2246    # spine Z extent
PAN_ZB, PAN_ZT = 50, 2246         # rear-panel Z extent
WALLX  = C_LEN                    # 5893 — sealed end wall
# Back-of-panel riser X lanes (in the rear corridor, +X of the panel)
RX4    = 5200                     # X4 waste riser X (3D)
RX_BLUE = 5239                    # blue-recycle riser X (onto the spine, to X1 cross)
X1X    = 5500                     # X1 fill cross X (3D X1_TEE_X)
MERGEX = 5404                     # IBC-4 merge tee X (3D MERGE4[0])
DV02X  = 4909                     # 3W-DV-02 X (3D DV02X = PXC-75)
# End-wall port heights (3D drains_ports): X1 fill high, X3 Z1700, X4 Z1620
X1_PORT_Z, X3_PORT_Z, X4_PORT_Z = EXT_FILL_1_H, 1700, 1620
# Pump / ACC stack on the shirt front (single column, projected along Yd)
PUMP_FRONT_X = 4934              # pump body front (PXC 4984 − radius 50)
PUMP_BACK_X  = 5034             # pump body back  (PXC 4984 + radius 50)
POD = 24                         # pipe OD (mm)

figb, axb = plt.subplots(figsize=(12.6, 15.3))
axb.set_xlim(4560, 6760)
axb.set_ylim(-300, 2520)
axb.set_aspect("equal")
axb.axis("off")


def _rect(x, z, w, h, fc, ec=C_OUT, lw=1.0, z0=5, hatch=None, alpha=1.0):
    axb.add_patch(mpatches.Rectangle((x, z), w, h, facecolor=fc, edgecolor=ec,
                  lw=lw, zorder=z0, hatch=hatch, alpha=alpha))


_sid = lambda v: v          # backside section draws in true mm (identity scale)
PWALL = 4                   # pipe wall thickness (mm) — colored wall + white bore


def _pipe(xs, zs, fc, zorder=8):
    """Color-coded pipe run with parallel walls + concentric-arc elbow fittings
    at every direction change (skill_plumbing_drawing.md). xs/zs = waypoints.
    Reuses the panel's draw_pipe_path with identity scale (backside = true mm)."""
    draw_pipe_path(axb, xs, zs, POD, PWALL, fc, ec=C_OUT, bore_fc="white",
                   zorder=zorder, sxf=_sid, szf=_sid)


# ── Container shell context ──────────────────────────────────────────────
_rect(4860, -90, 5933 - 4860, 90, C_WALLB, lw=0.8, z0=2, hatch="////")   # floor
axb.text(4890, -45, "CONTAINER FLOOR", fontsize=6, va="center", color="#555", **FB)
_rect(WALLX, 0, 40, C_HGT, C_WALLB, lw=0.8, z0=2, hatch="\\\\")           # sealed end wall
axb.text(WALLX + 20, C_HGT - 60, f"SEALED\nEND WALL\n(X={int(C_LEN)})", fontsize=6,
         ha="center", va="top", color="#555", **FB)
axb.plot([4860, WALLX], [C_HGT, C_HGT], color="#999", lw=0.8, ls=(0, (6, 4)), zorder=2)
axb.text(4890, C_HGT + 25, f"CEILING (Z={int(C_HGT)})", fontsize=6, color="#777", **FB)

# ── Rear panel (edge-on) ─────────────────────────────────────────────────
_rect(PANX, PAN_ZB, PANX1 - PANX, PAN_ZT - PAN_ZB, C_PLYB, lw=1.3, z0=6)
leader(axb, PANX1, 640, 5640, 520,
       f"18mm REAR PANEL\n(edge-on)\nX={PANX}–{PANX1}\nZ={PAN_ZB}–{PAN_ZT}",
       color=C_OUT, fs=6, ha="left", va="top", arrow_style="-|>", font=FB)

# ── 25mm pump-mount shirt (in FRONT of the rear panel, −X) ───────────────
_rect(SHIRTX0, SHIRT_ZB, SHIRTX1 - SHIRTX0, SHIRT_ZT - SHIRT_ZB,
      C_PLYB, lw=1.2, z0=6, alpha=0.85)
leader(axb, (SHIRTX0 + SHIRTX1) / 2, 480, 4570, 360,
       f"25mm PUMP-MOUNT SHIRT\nX={SHIRTX0}–{SHIRTX1}, Z={SHIRT_ZB}–{SHIRT_ZT}\n"
       "(pumps cam-clamp to it)",
       color="#7A6A40", fs=5.5, ha="left", va="top", arrow_style="-|>", font=FB)
# ~27mm chase gap (shirt back 5077 → panel front 5104) + 6 spacer blocks
for bz in (320, 920, 1560):
    _rect(SHIRTX1, bz, PANX - SHIRTX1, 80, C_PLYB, ec=C_OUT, lw=0.6, z0=7)
draw_dim_h(axb, SHIRTX1, PANX, 60, f"{PANX - SHIRTX1}mm\nchase", offset=4,
           fs=5, above=False, font=FB)
axb.text(SHIRTX1 + (PANX - SHIRTX1) / 2, 1700,
         "6× SPACER\nBLOCKS", fontsize=4.6, ha="center", va="center",
         color="#7A6A40", zorder=10, **FB)

# ── Pump + ACC stack on the shirt front (single column, projected along Yd) ──
# 3D bases (Z AFF): ACC 355, P-01 615, P-04 940, P-05 1340, P-03 1740.
for zb, h, lbl, hot in [(355, 200, "ACC-01", True), (615, 180, "P-01", False),
                        (940, 180, "P-04", True), (1340, 180, "P-05", True),
                        (1740, 180, "P-03", False)]:
    _rect(PUMP_FRONT_X, zb, PUMP_BACK_X - PUMP_FRONT_X, h,
          "#E6D9F0" if hot else "#EAEAEA", ec=C_OUT, lw=0.9, z0=5)
    axb.text((PUMP_FRONT_X + PUMP_BACK_X) / 2, zb + h / 2, lbl, fontsize=5.5,
             ha="center", va="center", color="#333", fontweight="bold", **FB)
leader(axb, PUMP_FRONT_X, 1830, 4570, 1900,
       "PUMP COLUMN + ACC-01\n(on the front of the shirt;\nsame stack as the front elevation)",
       color="#777", fs=5.3, ha="left", va="center", arrow_style="-|>", font=FB)

# ── Circuit C pump power: feed → distribution block → pump switches ──────
CWIRE = "#1565C0"
busx = PUMP_FRONT_X - 40                          # wiring bus, just −X of the pumps
db_z = 2210                                       # distribution block, above the pumps
axb.plot([busx, busx], [C_HGT, db_z], color=CWIRE, lw=1.4, zorder=12)     # feed
_rect(busx - 42, db_z - 4, 66, 32, "#D9E8F7", ec=CWIRE, lw=1.0, z0=12)
axb.text(busx - 9, db_z + 12, "Cct C\nDIST", fontsize=4.3, ha="center", va="center",
         color=CWIRE, fontweight="bold", **FB)
axb.plot([busx, busx], [db_z - 4, 705], color=CWIRE, lw=1.2, zorder=11)   # bus
for zr in (705, 1030, 1430, 1830):
    _rect(busx - 12, zr - 12, 24, 24, "white", ec=CWIRE, lw=0.9, z0=13)   # switch
    axb.plot([busx + 12, PUMP_FRONT_X], [zr, zr], color=CWIRE, lw=1.0, zorder=12)
leader(axb, busx - 24, db_z + 40, 4570, 2300,
       "CIRCUIT C POWER — 12V feed → distribution\nblock → 5 IP-rated switches "
       "(one per pump,\nP-01..P-05; run one at a time). P-02 is on\nthe Pinhole Wall "
       "panel and shares Circuit C.",
       color=CWIRE, fs=5.3, ha="left", va="top", arrow_style="-|>", font=FB)

# ── Drain-riser spine (18mm ply fin, teed off the rear panel into the corridor) ──
_rect(PANX, SPINE_ZB, SPX1 - PANX, SPINE_ZT - SPINE_ZB, C_PLYB, lw=1.2,
      z0=3, alpha=0.40)
leader(axb, (PANX + SPX1) / 2, 1180, 5650, 1140,
       f"DRAIN-RISER SPINE\n18mm ply, teed perpendicular off the rear\n"
       f"panel (a T in plan) — X={PANX}–{SPX1}, Z={SPINE_ZB}–{SPINE_ZT};\n"
       "the back-of-panel drain risers P-clip to it",
       color=C_OUT, fs=6, ha="left", va="center", arrow_style="-|>", font=FB)

# ── Back-of-panel pipe runs (faithful X–Z routing from the live 3D) ───────
DV01X = 4700                       # 3W-DV-01 X (corridor mouth, low ~Z235)
# X4 WASTE — two grey runs: (a) the suction PICKUP riser climbs the spine from
# the floor pickup to the pump; (b) the P-03 DISCHARGE runs high along the spine,
# then drops to the X4 end-wall port (Z1620).
_pipe([RX4, RX4, PUMP_BACK_X], [300, 1820, 1820], C_WASTEB, zorder=8)
_pipe([PUMP_BACK_X, 5763, 5763, WALLX],
      [1902, 1902, X4_PORT_Z, X4_PORT_Z], C_WASTEB, zorder=8)
# X3 BROWN — P-05 discharge routed BEHIND the panel, rising to the X3 port (Z1700).
_pipe([PUMP_BACK_X, 5763, 5763, WALLX],
      [1502, 1502, X3_PORT_Z, X3_PORT_Z], C_BROWNB, zorder=9)
# DV-01 — pH-gated filter-output diverter, low at the corridor mouth; two legs:
#   BLUE RECYCLE rises up the spine → X1 fill cross; WASTE → the IBC-4 merge tee.
axb.add_patch(mpatches.Polygon(
    [(DV01X, 251), (DV01X + 16, 235), (DV01X, 219), (DV01X - 16, 235)],
    fc="white", ec="#8A6D08", lw=1.3, zorder=12))
axb.text(DV01X, 305, "DV-01\n(corridor mouth)", fontsize=4.6, ha="center",
         va="bottom", color="#8A6D08", zorder=13, **FB)
_pipe([DV01X, RX_BLUE, RX_BLUE, X1X],
      [248, 248, X1_PORT_Z, X1_PORT_Z], C_BLUEB, zorder=7)
_pipe([DV01X, MERGEX, MERGEX], [222, 222, 1214], C_WASTEB, zorder=6)
# X1 fill cross + the IBC-4 merge tee, both consolidated on the spine.
axb.add_patch(mpatches.Circle((X1X, X1_PORT_Z), 16, facecolor="white",
              edgecolor=C_BLUEB, lw=1.4, zorder=12))
axb.text(X1X, X1_PORT_Z + 60, "X1 FILL\nCROSS", fontsize=5, ha="center",
         va="bottom", color=C_BLUEB, zorder=13, **FB)
axb.add_patch(mpatches.Circle((MERGEX, 1230), 16, facecolor="white",
              edgecolor=C_WASTEB, lw=1.6, zorder=13))
leader(axb, MERGEX, 1230, 5650, 1370,
       "IBC-4 MERGE TEE\n(DV-01 + DV-02 waste,\nconsolidated on the spine)",
       color="#555", fs=5.5, ha="left", va="center", arrow_style="-|>", font=FB)
# DV-02 (above the pump column) waste leg → drops to the IBC-4 merge tee.
axb.add_patch(mpatches.Polygon(
    [(DV02X, 2145 + 18), (DV02X + 18, 2145), (DV02X, 2145 - 18), (DV02X - 18, 2145)],
    fc="white", ec="#B8860B", lw=1.4, zorder=12))
axb.text(DV02X, 2145 + 30, "DV-02", fontsize=5, ha="center", va="bottom",
         color="#8A6D08", zorder=13, **FB)
_pipe([DV02X, DV02X, MERGEX, MERGEX],
      [2145 - 18, 1290, 1290, 1244], C_WASTEB, zorder=7)   # DV-02 waste → merge
# P-clips fastening the spine risers (suction pickup, blue recycle, DV-01 waste).
for rx, zt in [(RX4, 1800), (RX_BLUE, X1_PORT_Z), (MERGEX, 1214)]:
    for i in range(4):
        cz = 460 + i * 400
        if cz < zt - 80:
            _rect(rx - 8, cz - 11, 16, 22, C_STEEL, lw=0.6, z0=11)
leader(axb, RX4, 1000, 5680, 900, "X4 SUCTION PICKUP RISER\n(waste pickup → P-03) — P-clips",
       color="#555", fs=5.3, ha="left", va="top", arrow_style="-|>", font=FB)
leader(axb, 5763, 1610, 6120, 1500, "X3 / X4 DISCHARGES\n(behind the panel → end-wall ports)",
       color=C_BROWNB, fs=5.3, ha="left", va="center", arrow_style="-|>", font=FB)
leader(axb, RX_BLUE, 900, 4720, 740, "BLUE-RECYCLE RISER\n(DV-01 → up the spine → X1 cross)",
       color=C_BLUEB, fs=5.3, ha="right", va="top", arrow_style="-|>", font=FB)

# ── End-wall ports ───────────────────────────────────────────────────────
for z, lab, col in [(X1_PORT_Z, "X1", C_BLUEB), (X3_PORT_Z, "X3", C_BROWNB),
                    (X4_PORT_Z, "X4", C_WASTEB)]:
    axb.add_patch(mpatches.Circle((WALLX, z), 22, facecolor="white",
                  edgecolor=col, lw=1.8, zorder=14))
    axb.text(WALLX, z, lab, fontsize=6, ha="center", va="center",
             fontweight="bold", color=col, zorder=15, **FB)

# ── Dimensions ───────────────────────────────────────────────────────────
draw_dim_h(axb, PANX, SPX1, 150, f"{SPX1 - PANX}mm spine depth", offset=4,
           fs=5.5, above=False, font=FB)

# ── Notes (right margin) ─────────────────────────────────────────────────
draw_notes(axb, [
    "CORRIDOR PLUMBING PANEL — BACKSIDE (corridor side section, looking along Yd):",
    "1. Pumps + ACC-01 mount on the FRONT (−X) of the rear panel, cam-clamped to a 25mm pump-mount shirt that backs the bodies (X=5052–5077, Z=275–1925).",
    "2. A ~27mm chase gap separates the shirt back (X=5077) and the rear-panel front (X=5104); six ply spacer blocks bridge it.",
    "3. Rear panel: 18mm ply, X=5104–5122, Z=50–2246. The drain-riser spine is an 18mm ply fin teed perpendicular off it into the rear corridor (X=5104–5560, Z=280–2246).",
    "4. Back-of-panel risers P-clip to the spine: the X4 waste riser (P-03 → up the spine → X4 end-wall port @ Z=1620) and the blue-recycle riser climbing onto the spine into the X1 fill cross (high).",
    "5. The X3 brown discharge (P-05) routes BEHIND the panel to the X3 end-wall port @ Z=1700.",
    "6. DV-02 → IBC-3 / IBC-4; the IBC-4 merge tee (DV-01 + DV-02 waste) is consolidated on the spine.",
    "7. Circuit C powers all 5 pumps (one IP switch each, run one at a time); P-02 lives on the Pinhole Wall panel and shares Circuit C.",
], 6065, 2440, spacing=54, fs=6.5, ha="left", width=620, font=FB)

title_block(axb, "CORRIDOR PANEL — BACKSIDE",
            drawing_title="CORRIDOR PLUMBING PANEL — BACKSIDE",
            subtitle="PUMP-MOUNT SHIRT · DRAIN-RISER SPINE · BEHIND-PANEL RISERS · END-WALL PORTS",
            scale_note="CORRIDOR SIDE SECTION ALONG Yd · AXES IN mm",
            doc_id="TBS-001 · Plumbing Panel",
            height=0.05)

outb = os.path.join(DIAGRAMS_DIR, "panel-layout-back.png")
figb.savefig(outb, dpi=150, facecolor="white", edgecolor="none",
             bbox_inches="tight", pad_inches=0.2)
plt.close(figb)
print(f"Panel backside → {outb}")
