#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_panel_layout.py — Two plumbing panels + the corridor backside.

The water system has two physically separate plumbing panels:

CORRIDOR PLUMBING PANEL (panel-layout.png) — 18mm plywood spanning the 270mm
IBC plumbing corridor (Yd=1046–1316), perpendicular to the sealed end wall.
Carries the transfer pumps + the Blue-supply accumulator:
  Pump column (bottom→top): ACC-01 + P-01 (Blue supply) + P-02 (Brown recycle) +
  P-05 (Brown drain) + P-03 (Waste evac).
  Ball valves: BV-01 (P-01 suction), BV-02 (P-05 suction), BV-03 (P-02 suction),
  BV-06 (P-03 suction).  P-02 discharges to ACC-02 on the pinhole-wall skid.

PINHOLE WALL PLUMBING PANEL (pinhole-panel.png) — the filter train + the
tray-drain skid, mounted on the pinhole wall:
  Tray-drain skid row P-04 (tray-sump pump) · SV-02 (pH sample) · 3W-DV-02, UNDER
  the 3-stage Big Blue filter stack (F-01 5µm → F-02 KDF-55 → F-03 GAC) + SV-01
  (pH sample, raised) + DV-01 (filtered diverter) + ACC-02 (recycle-spray damper).
  Flow: tray sump → P-04 → SV-02 → DV-02 → F-01 → F-02 → F-03 → SV-01 → DV-01 →
        (recycle / Waste).

Plus TWO corridor spine side-sections — opposite faces of the drain-riser
spine, looking along Yd:
  panel-spine-view-a.png — −Yd INTAKE face (suctions, recycle, fills, merge).
  panel-spine-view-b.png — +Yd DISCHARGE face (pump discharges); a mirror of A.
Both share all structure + fittings/valves/diverters as landmarks; each face's
own pipe runs are drawn only on its own sheet.

Outputs: diagrams/panel-layout.png, diagrams/pinhole-panel.png,
         diagrams/panel-spine-view-a.png, diagrams/panel-spine-view-b.png
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from tbs_constants import C_OUT, C_DIM, C_STEEL, DIAGRAMS_DIR, PUMP_PIPE_OD, PUMP_PIPE_WALL, EQPANEL_X, EQPANEL_H, DIAGRAM_DPI
from tbs_constants import BB_OD, PWP_FILTER_X1, PWP_FILTER_X2, PWP_FILTER_X3, PWP_FILTER_TOP_Z, PWP_FILTER_BOT_Z, PWP_FILTER_HEAD_Z, PWP_SV01_X, PWP_SV01_Z, PWP_SROW_Z0, PWP_SV02_Z, PWP_DV02_Z, PWP_ACC2_X, PWP_ACC2_Z0, PWP_PANEL_X0, PWP_PANEL_X1, PWP_PANEL_Z0
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_notes, draw_pipe_path as _tbs_pipe_path, valve_ball, valve_3way, valve_check
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

# ── Filter housing (separate, 4.5"×20") ──────────────────────────────────
FILT_OD  = 184   # housing OD (mm) — = tbs_constants BB_OD (real Big Blue 4.5×20 = Ø184; diameter same 10↔20"); KEEP IN SYNC
FILT_H   = 594   # total height (mm) — head + sump (4.5×20) — = tbs_constants BB_H; KEEP IN SYNC
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
# generate_corridor_water_panel.py).  All pumps centered on the corridor center
# (3D Yd1181 → panel-Yd 135); IN/suction on the LEFT (panel-Yd 55 = 3D Yd1101,
# faces -Yd / near wall), OUT/discharge on the RIGHT (panel-Yd 215 = 3D Yd1261).
# Bottom→top: ACC-01 (dead-leg), P-01, P-04, P-05, P-03.  Panel-Z = (3D AFF Z) − 200.
PUMP_COL_C   = 135    # pump-column center (panel-Yd; 3D Yd1181 corridor center)
CORR_PORT_IN  = 55    # IN / suction port panel-Yd (3D Yd1101, faces near wall)
CORR_PORT_OUT = 215   # OUT / discharge port panel-Yd (3D Yd1261)

# Pump body bases (panel-Z = 3D AFF − 200):
P01_Z = 415                           # P-01 Blue supply
P04_Z = 740                           # P-02 Brown recycle (took the tray-drain pump's vacated corridor slot)
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


def draw_symbol_key(ax_t, x, y_top, *, r=11, row=58, fs=6.5, w=300):
    """P&ID valve symbol key/legend drawn in `ax_t` data coords.  `x, y_top` anchors
    the SCREEN top-left corner; rows step DOWN by `row`.  Draws the box, a title, then
    a ball / 3-way / check sample with its name.  Reversed-x axes (the mirrored spine
    View B) are handled: all horizontal layout follows the screen reading direction so
    the symbols+labels stay left-to-right and the check-valve arrow points right.."""
    # +1 normal axis, -1 if the x-axis is reversed (xlim flipped) — every horizontal
    # offset below is multiplied by `dxs` so layout is in SCREEN space.
    xl = ax_t.get_xlim()
    dxs = -1 if xl[0] > xl[1] else 1
    flow_dir = "right" if dxs == 1 else "left"     # screen-rightward arrow
    box_h = 4 * row + 18
    ax_t.add_patch(mpatches.Rectangle((x, y_top - box_h), w * dxs, box_h,
                   fc="#FAFAFA", ec=C_DIM, lw=0.8, zorder=14))
    ax_t.text(x + dxs * w / 2, y_top - 20, "VALVE SYMBOL KEY",
              ha="center", va="center", fontsize=fs + 1, color=C_OUT,
              fontweight="bold", zorder=16, **FONT)
    sym_x = x + dxs * 30
    txt_x = x + dxs * 58
    rows = [
        ("ball",  "BALL VALVE"),
        ("3way",  "3-WAY DIVERTER"),
        ("check", "CHECK VALVE (CV)"),
    ]
    for i, (kind, name) in enumerate(rows):
        cy = y_top - 60 - i * row
        if kind == "ball":
            valve_ball(ax_t, sym_x, cy, r, C_OUT, vert=False, zorder=15)
        elif kind == "3way":
            valve_3way(ax_t, sym_x, cy, r, C_OUT, ports=("left", "right", "down"),
                       zorder=15)
        else:
            valve_check(ax_t, sym_x, cy, r, C_OUT, flow=flow_dir, zorder=15)
        ax_t.text(txt_x, cy, name, ha="left", va="center", fontsize=fs,
                  color=C_DIM, zorder=16, **FONT)


def draw_ball_valve(x, z, label, color):
    """P&ID ball valve (bowtie + centre ball) at (x, z) in panel mm coords, on a
    vertical riser, with the label set just to the side (clear of the ball)."""
    valve_ball(ax, sx(x), sz(z), BV_R, color, vert=True)
    lbl = label.replace("\n", "-")
    ax.text(sx(x + BV_R) + 6, sz(z) + 6, lbl, ha="left", va="center",
            fontsize=5, color=color, fontweight="bold", zorder=14, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  CORRIDOR PLUMBING PANEL — FRONT ELEVATION
#  Looking at panel from open end (viewer facing +X toward sealed wall).
#  LEFT = near wall (Yd=1046), RIGHT = far wall (Yd=1316).
#  Single upright pump column: ACC-01 + P-01 + P-02 + P-05 + P-03.
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
               P04_Z, "P-02", "BROWN\nRECYCLE", C_BROWN, C_BROWN_EC)
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

    # ── BROWN RECYCLE (P-02) ─────────────────────────────────────────
    # P-02 suction: IBC-3 Brown buffer (LEFT) → BV-03 → P-02 inlet (LEFT port)
    _P04_SUCT_Z = P04_PORT_Z + SUCT_RISE
    draw_pipe_path(ax,
        [EXIT_L, CORR_PORT_IN, CORR_PORT_IN],
        [_P04_SUCT_Z, _P04_SUCT_Z, P04_PORT_Z],
        PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
    draw_ball_valve(CORR_PORT_IN, _P04_SUCT_Z, "BV\n03", C_BROWN)
    ax.annotate("", xy=(sx(EXIT_L + _AW), sz(_P04_SUCT_Z)),
                xytext=(sx(EXIT_L), sz(_P04_SUCT_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BROWN), zorder=11)
    ax.text(sx(EXIT_L - 5), sz(_P04_SUCT_Z),
            "FROM\nIBC-3\n(BROWN)", ha="right", va="center",
            fontsize=5.5, color=C_BROWN, zorder=10, **FONT)

    # P-02 discharge: outlet (RIGHT port) → up the far-right riser lane (DISCH_RISER,
    # clear of the OUT ports) → exits to ACC-02 (the recycle-spray damper on the
    # pinhole-wall skid) → BV-05 → the spray bar.
    _P02_DISCH_Z = 1650                   # discharge-riser exit height (above P-05, below the symbol-key box)
    draw_pipe_path(ax,
        [CORR_PORT_OUT, DISCH_RISER, DISCH_RISER, EXIT_R],
        [P04_PORT_Z, P04_PORT_Z, _P02_DISCH_Z, _P02_DISCH_Z],
        PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BLACK + 0.5)
    ax.annotate("", xy=(sx(EXIT_R), sz(_P02_DISCH_Z)),
                xytext=(sx(EXIT_R - _AW), sz(_P02_DISCH_Z)),
                arrowprops=dict(**_arrow_kw, color=C_BROWN), zorder=11)
    ax.text(sx(EXIT_R + 5), sz(_P02_DISCH_Z),
            "TO ACC-02\n(skid) →\nBV-05 spray", ha="left", va="center",
            fontsize=5.5, color=C_BROWN, zorder=10, **FONT)

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
    # It CROSSES the P-02 discharge riser (DISCH_RISER) — they do NOT join, so the
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
               f"{PANEL_W}mm", offset=4.8, fs=6, color=C_DIM, font=FONT)
    draw_dim_h(ax, sx(PUMP_COL_C - PUMP_W / 2), sx(PUMP_COL_C + PUMP_W / 2),
               sz(P01_Z - 15),
               f"{PUMP_W}mm", offset=3.2, fs=5.5, color=C_DIM, font=FONT)
    draw_dim_v(ax, sx(PUMP_COL_C + PUMP_W / 2 + 15),
               sz(P01_Z), sz(P01_Z + PUMP_H),
               f"{PUMP_H}mm", offset=4.8, fs=5.5, color=C_DIM,
               right=True, font=FONT)
    draw_dim_v(ax, sx(-30), sz(0), sz(PANEL_H),
               f"{PANEL_H}mm", offset=8.0, fs=7, color=C_DIM,
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
        "    P-02 (Brown recycle), P-05 (Brown drain), P-03 (Waste drain).",
        "5. ACC-01: 0.75L bladder accumulator on the Blue supply, dead-leg below P-01.",
        "6. Suctions enter on the LEFT through their isolation valve; discharges exit RIGHT.",
        "7. BV-01 (P-01 suction), BV-02 (P-05 suction), BV-03 (P-02 suction),",
        "    BV-06 (P-03 suction) — manual ball valves.",
        "8. P-02 pulls IBC-3 (Brown buffer) and discharges to ACC-02 (recycle-spray damper",
        "    on the pinhole-wall skid) → BV-05 → spray bar.",
        "9. The tray-drain skid (P-04 · SV-02 · DV-02) is on the PINHOLE WALL panel, not here.",
        f"10. Max protrusion: {max_depth}mm. The filter train + tray-drain skid are on the PINHOLE WALL panel.",
        "11. PIPE: 1/2\" PVC Sch-40 pump runs (solvent-weld) + threaded transitions at components; braided flex hose",
        "     at each pump port. Pumps + ACC cam-clamp to a 25mm ply shirt; 4-bolt brackets.",
        "12. Pump-base Z (AFF): ACC-01 355 · P-01 615 · P-02 940 · P-05 1340 · P-03 1740.",
    ]
    draw_notes(ax, notes, 575, 375, spacing=14,
               fs=6, width=450, color=C_DIM, title_color=C_NEW, font=FONT)

    # ── SYMBOL KEY ──────────────────────────────────────────────────
    draw_symbol_key(ax, 575, 2540, r=11, row=58, fs=6.5, w=300)

    # ── TITLE BLOCK ─────────────────────────────────────────────────
    title_block(ax, "CORRIDOR PANEL",
                drawing_title="CORRIDOR PLUMBING PANEL",
                subtitle="FRONT ELEVATION + PIPE ROUTING + CROSS-SECTION",
                scale_note="ELEV 1:80 · X-SECTION NTS · AXES IN mm",
                doc_id="TBS-001 · Plumbing Panel",
                height=0.028)

    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    out = os.path.join(DIAGRAMS_DIR, "panel-layout.png")
    fig.savefig(out, dpi=DIAGRAM_DPI, facecolor="white", edgecolor="none",
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
               "270mm CORRIDOR", offset=3.2, fs=5.5, color=C_DIM, font=FONT)
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
#  Matches the live 3D (generate_pinhole_water_panel.py: kit() + backing()).
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

    fig, ax_p = plt.subplots(1, 1, figsize=(23, 13), dpi=200)
    # +750 units of right-hand room so the notes block (a border PATCH, which matplotlib clips to the
    # axes) fits inside the page instead of being cut at the xlim; figsize widened in step to keep the
    # board's X scale.
    ax_p.set_xlim(0, (PW_XR - PW_XL) * PW_KX + 2 * PW_OX + 750)
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
        valve_ball(ax_p, pwx(x), pwz(z), half, color, vert=True)
        lbl = label.replace("\n", "-")
        ax_p.text(pwx(x) + half + 6, pwz(z), lbl, ha="left", va="center",
                  fontsize=6, color=color, fontweight="bold", zorder=14, **FONT)

    # Title above the board
    pw_text((PW_XL + PW_XR) / 2, PW_ZT + 60,
            "WALL ELEVATION — PINHOLE WALL PLUMBING PANEL",
            ha="center", va="bottom", fontsize=11, color=C_DIM,
            fontweight="bold")

    # ── Backing board (18mm marine ply) — X 2780–4500, Z 920–2360 ──────────
    BD_XL, BD_XR = PWP_PANEL_X0, PWP_PANEL_X1
    BD_ZB, BD_ZT = PWP_PANEL_Z0, 2360
    pw_rect(BD_XL, BD_ZB, BD_XR - BD_XL, BD_ZT - BD_ZB,
            C_PLY, C_PLY_EC, lw=2.0, zorder=3, alpha=0.5)
    pw_text(4470, 2255,
            f"{BD_XR - BD_XL} × {BD_ZT - BD_ZB}mm\n18mm MARINE PLY\n(pinhole wall)",
            ha="center", va="center", fontsize=6.5, color=C_PLY_EC, zorder=4)

    # ── Filter geometry (Big Blue 4.5×20: head block + Ø184 sump below) ────
    HEAD_ZB, HEAD_ZT = PWP_FILTER_HEAD_Z, PWP_FILTER_TOP_Z      # head block Z band (pinned near the ceiling)
    SUMP_ZB, SUMP_ZT = PWP_FILTER_BOT_Z, PWP_FILTER_HEAD_Z      # cylindrical sump hanging below (4.5×20 — drops ~230mm lower than the 10")
    HEAD_Z = (HEAD_ZB + HEAD_ZT) / 2   # head-line port height
    filters = [
        ("F-01", "5µm\nSEDIMENT", PWP_FILTER_X1 - BB_OD // 2, PWP_FILTER_X1 + BB_OD // 2),
        ("F-02", "KDF-55",        PWP_FILTER_X2 - BB_OD // 2, PWP_FILTER_X2 + BB_OD // 2),
        ("F-03", "CARBON\n(GAC)", PWP_FILTER_X3 - BB_OD // 2, PWP_FILTER_X3 + BB_OD // 2),
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

    # ── Tray-drain skid row (P-04 · SV-02 · DV-02) — UNDER the filters, on the row line ──
    ROW_Z = PWP_DV02_Z                  # row line (= P-04 OUT / DV-02 center, Z1312)
    P4_XL, P4_XR = PWP_FILTER_X1 - 50, PWP_FILTER_X1 + 50
    pw_rect(P4_XL, PWP_SROW_Z0, P4_XR - P4_XL, 180, C_PUMP_BODY, C_PUMP_EC, lw=1.2, zorder=6)
    pw_rect(P4_XL - 4, PWP_SROW_Z0 + 154, (P4_XR - P4_XL) + 8, 26, "#4A4038", C_PUMP_EC, lw=0.8, zorder=7)  # motor cap
    pw_text(PWP_FILTER_X1, PWP_SROW_Z0 + 112, "P-04", ha="center", va="center", fontsize=8, color=C_PUMP_EC, fontweight="bold", zorder=8)
    pw_text(PWP_FILTER_X1, PWP_SROW_Z0 + 60, "TRAY\nDRAIN", ha="center", va="center", fontsize=5, color=C_PUMP_EC, zorder=8)
    pw_valve(PWP_FILTER_X2, PWP_SV02_Z, "SV\n02", C_BROWN, half=18)          # SV-02 sample, under F-02
    valve_3way(ax_p, pwx(PWP_FILTER_X3), pwz(PWP_DV02_Z), 22, "#B8860B", ports=("left", "up", "right"))  # DV-02, under F-03
    pw_text(PWP_FILTER_X3, PWP_DV02_Z - 54, "DV-02\n3-WAY", ha="center", va="top", fontsize=6, color="#8A6D08", fontweight="bold", zorder=14)
    # ── ACC-02 (recycle-spray damper) — center-bottom cylinder, fed from P-02 in the corridor ──
    pw_rect(PWP_ACC2_X - 63, PWP_ACC2_Z0, 126, 200, C_ACC, C_BLUE_EC, lw=1.2, zorder=6, alpha=0.85)
    pw_text(PWP_ACC2_X, PWP_ACC2_Z0 + 120, "ACC-02", ha="center", va="center", fontsize=7, color=C_BLUE_EC, fontweight="bold", zorder=8)
    pw_text(PWP_ACC2_X, PWP_ACC2_Z0 + 66, "RECYCLE\nSPRAY", ha="center", va="center", fontsize=5, color=C_BLUE_EC, zorder=8)
    leader(ax_p, pwx(PWP_ACC2_X) - 24, pwz(PWP_ACC2_Z0 + 200), pwx(PWP_ACC2_X) - 150, pwz(1560),
           "ACC-02 pulsation damper\n(P-02 in corridor → ACC-02\n→ BV-05 spray selector)",
           fs=6, color=C_BLUE_EC, ha="left", va="center", font=FONT)

    # ════════════════════════════════════════════════════════════════
    #  FLOW — tray sump → P-04 → SV-02 → DV-02 (row line); DV-02 recycle branch UP the
    #  edge into F-01; F-01 → F-02 → F-03 along the head line; F-03 → SV-01 → DV-01 (left).
    # ════════════════════════════════════════════════════════════════
    F1_CX, F2_CX, F3_CX = PWP_FILTER_X1, PWP_FILTER_X2, PWP_FILTER_X3
    F1_XL, F1_XR = PWP_FILTER_X1 - BB_OD // 2, PWP_FILTER_X1 + BB_OD // 2
    F3_XR = PWP_FILTER_X3 + BB_OD // 2

    # tray-sump suction: brown drops from P-04 IN below the ply toward the tray sump
    SUCT_TURN_Z = 850
    SRC_X = PWP_FILTER_X1 - 250
    pw_pipe([PWP_FILTER_X1, PWP_FILTER_X1, SRC_X],
            [PWP_SROW_Z0, SUCT_TURN_Z, SUCT_TURN_Z], C_BROWN, zorder=Z_BROWN)
    pw_arrow(SRC_X, SUCT_TURN_Z, SRC_X - 42, SUCT_TURN_Z, C_BLUE)
    pw_text(SRC_X - 52, SUCT_TURN_Z, "FROM\nTRAY SUMP", ha="left", va="center", fontsize=6, color=C_BROWN, zorder=10)
    # P-04 OUT → SV-02 → DV-02 along the row line (SV-02 taps in-line)
    pw_pipe([PWP_FILTER_X1 + 50, PWP_FILTER_X3 - 22], [ROW_Z, ROW_Z], C_BROWN, zorder=Z_BROWN)
    pw_arrow(PWP_FILTER_X2 + 80, ROW_Z, PWP_FILTER_X2 + 20, ROW_Z, C_BROWN)
    # DV-02 recycle branch (up port) → up the panel edge → F-01 IN at the head line
    EDGE_X = 2830
    pw_pipe([PWP_FILTER_X3, PWP_FILTER_X3, EDGE_X, EDGE_X, F1_XL],
            [ROW_Z + 22, 1600, 1600, HEAD_Z, HEAD_Z], C_BROWN, zorder=Z_BROWN)
    # F-01 → F-02 → F-03 (straight jumpers, head line)
    pw_pipe([PWP_FILTER_X1 + BB_OD // 2, PWP_FILTER_X2 - BB_OD // 2], [HEAD_Z, HEAD_Z], C_BROWN, zorder=Z_BROWN)   # F1→F2
    pw_pipe([PWP_FILTER_X2 + BB_OD // 2, PWP_FILTER_X3 - BB_OD // 2], [HEAD_Z, HEAD_Z], C_BROWN, zorder=Z_BROWN)   # F2→F3

    # F-03 OUT → drops down to SV-01 (RAISED beside F-03) — pH sample tap
    SV01_X = PWP_SV01_X
    SV01_Z = PWP_SV01_Z                 # raised beside F-03 (Z1610)
    F3_OUT_X = 4090
    pw_pipe([F3_XR, F3_OUT_X, F3_OUT_X, SV01_X, SV01_X],
            [HEAD_Z, HEAD_Z, SV01_Z, SV01_Z, SV01_Z],
            C_FILTER, zorder=Z_BROWN)
    pw_valve(SV01_X, SV01_Z, "SV\n01", C_BROWN, half=20)
    # SV-01 downturned sample spout
    pw_pipe([SV01_X, SV01_X, SV01_X - 45, SV01_X - 45],
            [SV01_Z - 20, SV01_Z - 130, SV01_Z - 130, SV01_Z - 175], C_BROWN, zorder=Z_BROWN)
    pw_arrow(SV01_X - 45, SV01_Z - 150, SV01_X - 45, SV01_Z - 185, C_BROWN)
    leader(ax_p, pwx(SV01_X), pwz(SV01_Z) + 22, pwx(4370), pwz(1980),
           "SV-01 — pH sample tap\n(filtered line, before DV-01;\n"
           "raised beside F-03)",
           fs=6, color=C_BROWN, ha="left", va="bottom", font=FONT)

    # SV-01 → 3W-DV-01: the filtered line leaves the board's LEFT edge (mirrored
    # view — the corridor mouth / DV-01 sits on the sealed-end/+X side).
    DV01_EDGE_X = BD_XR + 40            # just past the board's (mirrored) left edge
    pw_pipe([SV01_X, DV01_EDGE_X], [SV01_Z, SV01_Z], C_FILTER, zorder=Z_BROWN)
    pw_arrow(DV01_EDGE_X - 30, SV01_Z, DV01_EDGE_X, SV01_Z, C_FILTER)
    leader(ax_p, pwx(DV01_EDGE_X), pwz(SV01_Z), pwx(DV01_EDGE_X) - 8, pwz(SV01_Z) - 150,
           "3W-DV-01 (corridor mouth):\npH-gated split →\n"
           "recycle (IBC-3) / Waste (IBC-4)",
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
    leader(ax_p, pwx(PWP_FILTER_X1) - 40, pwz(PWP_SROW_Z0 + 90), pwx(3060), pwz(1030),
           "P-04 Shurflo 2088\n12V · 3.5 GPM · 45 PSI\n(tray-drain pump)",
           fs=6, color=C_PUMP_EC, ha="left", va="center", font=FONT)
    leader(ax_p, pwx(F2_CX), pwz(SUMP_ZB + 40), pwx(3500), pwz(1640),
           "Big Blue 4.5\"×20\" housing\n(Ø184 sump to Z1746, head Z2262–2340;\n"
           "F-01 5µm → F-02 KDF-55 → F-03 GAC)",
           fs=6, color=C_FILTER, ha="left", va="center", font=FONT)

    # ── NOTES ───────────────────────────────────────────────────────
    notes = [
        "PINHOLE WALL FILTER SKID — TRAY-DRAIN RECYCLE + FILTER TRAIN:",
        "1. Wide 18mm marine-ply backing board on the pinhole wall (Yd≈0),",
        "    X=2780–4575, Z=920–2360mm AFF.",
        "2. Tray-drain skid row UNDER the filters: P-04 (tray-sump pump) →",
        "   SV-02 (pH sample) → 3W-DV-02, on the row line Z≈1312.",
        "3. HORIZONTAL filter bank high on the wall: F-01 (5µm sediment) →",
        "    F-02 (KDF-55) → F-03 (carbon/GAC); Big Blue 4.5\"×20\" housings.",
        "4. DV-02 recycle branch feeds F-01; waste branch → IBC-4 (corridor).",
        "5. SV-01: pH sample tap on the filtered line, RAISED beside F-03",
        "   (Z≈1610), before DV-01.",
        "6. 3W-DV-01 is PHYSICALLY at the corridor mouth (off this wall) — the filtered",
        "    line leaves the board's edge and splits there: pH-gated to recycle",
        "    (IBC-3) or Waste (IBC-4).",
        "7. ACC-02 (recycle-spray damper, center-bottom) is fed from P-02 in the",
        "   corridor and feeds BV-05 → the spray bar.",
        "8. Flow: sump → P-04 → SV-02 → DV-02 → F-01 → F-02 → F-03 → SV-01 → DV-01.",
        "9. Filters at 338mm centres (X3300/3638/3976); heads Z≈2300, sump bottoms",
        "    Z≈1746 AFF (4.5×20).",
        "10. PIPE: 1\" PVC Sch-40 (filter loop) / ½\" (recycle-spray); housings on their",
        "    integral brackets through-bolted to the ply board.",
    ]
    draw_notes(ax_p, notes, pwx(2600), pwz(1560), spacing=32,
               fs=6.5, width=720, color=C_DIM, title_color=C_NEW, font=FONT)

    # ── SYMBOL KEY (clear left margin strip, X4500–5060) ────────────
    draw_symbol_key(ax_p, 20, pwz(1900), r=13, row=70, fs=6.5, w=395)

    # ── TITLE BLOCK ─────────────────────────────────────────────────
    title_block(ax_p, "PINHOLE WALL PANEL",
                drawing_title="PINHOLE WALL PLUMBING PANEL",
                subtitle="WALL ELEVATION (X × Z) + FILTER TRAIN ROUTING",
                scale_note="WALL ELEVATION · AXES IN mm",
                doc_id="TBS-001 · Plumbing Panel",
                height=0.05)

    # ── MOUNTING DETAIL (side section) — how each Big Blue head fixes to the ply ──
    #   Replaces the retired steel U-bracket: the head's own mounting ear lag-screws
    #   through a 25mm HDPE standoff straight into the 18mm ply; the Ø184 sump hangs
    #   below and clears the wall.
    axd = fig.add_axes([0.775, 0.60, 0.20, 0.30])
    axd.set_facecolor("white")
    axd.set_xlim(-50, 160); axd.set_ylim(-165, 150); axd.set_aspect("equal"); axd.axis("off")
    C_HDPE = "#7FBF8A"
    axd.text(55, 138, "DETAIL — HOUSING MOUNT (section)", ha="center", va="bottom",
             fontsize=7, color=C_DIM, fontweight="bold", **FONT)
    axd.add_patch(mpatches.Rectangle((-18, -150), 18, 268, fc=C_PLY, ec=C_OUT, lw=1.3,
                  hatch="////", zorder=3))                                             # 18mm ply
    axd.text(-9, -142, "18mm\nply", ha="center", va="bottom", fontsize=5.5, color=C_PLY_EC, zorder=7, **FONT)
    axd.add_patch(mpatches.Rectangle((0, 40), 25, 55, fc=C_HDPE, ec=C_OUT, lw=1.1, zorder=5))   # 25mm HDPE standoff
    axd.add_patch(mpatches.Rectangle((25, 48), 9, 40, fc="#3A70B0", ec=C_OUT, lw=1.0, zorder=6)) # head mounting ear
    axd.add_patch(mpatches.Rectangle((34, 40), 95, 60, fc="#3A70B0", ec=C_OUT, lw=1.0, alpha=0.85, zorder=6))  # head
    axd.add_patch(mpatches.Rectangle((45, -150), 90, 190, fc=C_FILTER, ec=C_OUT, lw=1.2, alpha=0.5, zorder=4))  # Ø184 sump
    axd.text(90, -55, "Ø184\nsump", ha="center", va="center", fontsize=6, color=C_OUT, zorder=7, **FONT)
    axd.plot([-14, 34], [66, 66], color="#505058", lw=2.6, zorder=8, solid_capstyle="butt")     # lag/wood screw
    axd.add_patch(mpatches.Rectangle((30, 62), 5, 8, fc="#505058", ec=C_OUT, lw=0.5, zorder=9))  # screw head
    leader(axd, 14, 67, 52, 116, "SS lag screw into the ply\n(no bracket)",
           color="#505058", fs=5.3, ha="left", va="top", arrow_style="-|>", font=FONT)
    leader(axd, 12, 55, -36, 96, "25mm HDPE\nstandoff",
           color="#2e7d32", fs=5.3, ha="right", va="bottom", arrow_style="-|>", font=FONT)
    leader(axd, 30, 55, 74, 24, "head mounting ear",
           color="#3A70B0", fs=5.3, ha="left", va="center", arrow_style="-|>", font=FONT)
    axd.annotate("", xy=(45, -105), xytext=(0, -105), arrowprops=dict(arrowstyle="<|-|>", color=C_DIM, lw=0.9), zorder=8)
    axd.text(22, -99, "sump hangs\nclear of the ply", ha="center", va="bottom", fontsize=5, color=C_DIM, zorder=8, **FONT)
    axd.add_patch(mpatches.Rectangle((-50, -165), 210, 315, fc="none", ec=C_DIM, lw=1.2, zorder=2))

    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    out = os.path.join(DIAGRAMS_DIR, "pinhole-panel.png")
    fig.savefig(out, dpi=DIAGRAM_DPI, facecolor="white", edgecolor="none",
                bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print(f"Pinhole wall panel → {out}")

# ── Render the two front-elevation panels ──────────────────────────────────
draw_corridor_panel()
draw_pinhole_panel()


# ═══════════════════════════════════════════════════════════════════════════
#  SPINE SIDE-SECTIONS — two sheets, opposite faces of the drain-riser spine
#  (corridor side section, looking along Yd).  Absolute X/Z (mm) — matches the 3D.
#  VIEW A (−Yd INTAKE face): suctions, recycle, fills, merge.
#  VIEW B (+Yd DISCHARGE face): pump discharges — a MIRROR image of A
#    (matplotlib renders mirrored via a reversed xlim; text stays upright).
#  Structure + all fittings/valves/diverters are landmarks drawn in BOTH; each
#  face's own pipe runs are guarded to its own sheet via the _NEAR flag.
# ═══════════════════════════════════════════════════════════════════════════
from tbs_constants import (C_LEN, C_HGT, EXT_FILL_1_H)

FB = {"fontfamily": "monospace"}
C_PLYB   = "#D9C9A3"   # plywood (tan)
C_BROWNB = "#7A5230"   # brown developer drain
C_WASTEB = "#8A8A8A"   # waste/grey drain
C_BLUEB  = "#3A78C0"   # blue fill
C_WALLB  = "#C8C8C8"

# ── Geometry (matches generate_corridor_water_panel.py: BACK_X=5104 rear panel) ──
PANX   = 5104                     # rear-panel front face (pumps hang -X off it)
PANX1  = 5122                     # rear-panel rear face (18mm ply)
SHIRTX0, SHIRTX1 = 5052, 5077     # 25mm pump-mount shirt (in FRONT of the panel)
SHIRT_ZB, SHIRT_ZT = 325, 2191    # shirt Z extent (bottom shortened to 325 to clear the
                                  # raised P-05 inlet elbow; top raised to back DV-02 at DV_Z+DVB)
SPX1   = 5560                     # drain-riser spine rear (X5104–5560)
SPINE_ZB, SPINE_ZT = 280, 2246    # spine Z extent
PAN_ZB, PAN_ZT = 50, 2246         # rear-panel Z extent
WALLX  = C_LEN                    # 5893 — sealed end wall
# Back-of-panel riser X lanes (in the rear corridor, +X of the panel)
RX4    = 5200                     # X4 waste riser X (3D)
RX_BLUE = 5239                    # blue-recycle riser X (onto the spine, to X1 cross)
X1X    = 5500                     # X1 fill cross X (3D X1_TEE_X)
MERGEX = 5404                     # IBC-4 merge tee X (3D MERGE4[0])
DV02X  = 5028                     # 3W-DV-02 X (3D DV02X = SHIRT_X − DVB/2 = 5028.5; PXC mounts DV-02 on the shirt front)
# End-wall port heights (3D drains_ports): X1 fill high, X3 Z1700, X4 Z1620
X1_PORT_Z, X3_PORT_Z, X4_PORT_Z = EXT_FILL_1_H, 1700, 1620
# Pump / ACC stack on the shirt front (single column, projected along Yd)
PUMP_FRONT_X = 4934              # pump body front (PXC 4984 − radius 50)
PUMP_BACK_X  = 5034             # pump body back  (PXC 4984 + radius 50)
PXC          = 4984             # pump axis / IN-port X (upright pumps take suction at the top-centre)
POD = 24                         # pipe OD (mm)

# `axb` is the current spine-view axes; spine_view() rebinds it per sheet.
axb = None
_NEAR = None       # which spine face this sheet shows: '-Yd' (A) or '+Yd' (B)


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


def _hpipe(z, x0, x1, fc, zorder=8, crosses=()):
    """A horizontal back-of-panel run that CROSSES the spine risers without joining
    them: gap-break the run at each riser X it passes (skill_plumbing_drawing §
    crossings — the riser, in front on the spine, reads continuous)."""
    g = 16
    cuts = sorted(c for c in crosses if min(x0, x1) + g < c < max(x0, x1) - g)
    a = x0
    for c in cuts:
        _pipe([a, c - g], [z, z], fc, zorder=zorder)
        a = c + g
    _pipe([a, x1], [z, z], fc, zorder=zorder)


# spine riser X-lanes that the horizontal drain/recycle runs cross
SPINE_RISERS = (5200, 5239, 5404)


def spine_view(side):
    """Render one spine side-section sheet. side='a' (−Yd intake face) or
    'b' (+Yd discharge face, a mirror of A). Rebinds the module globals axb +
    _NEAR so the _rect/_pipe/_hpipe helpers draw on this sheet's axes."""
    global axb, _NEAR
    _NEAR = '-Yd' if side == 'a' else '+Yd'
    # ── side-aware annotation helpers (B mirrors via the reversed xlim, so any
    #    hand-placed label/leader keeps its SCREEN side only if its ha is flipped;
    #    mxa() mirrors a margin-anchor X so a standalone block stays in the same
    #    screen corner) ──
    _FLIP = {"left": "right", "right": "left", "center": "center"}
    _ha = (lambda a: a) if side == 'a' else (lambda a: _FLIP.get(a, a))
    mxa = (lambda x: x) if side == 'a' else (lambda x: 4560 + 6760 - x)

    def _flowhead(x, z, dxn, color, L=44):
        """A flow-direction arrowhead drawn ON an off-section ('open') pipe end,
        pointing the way the water actually moves (into the section for a
        suction, out of it for a supply/fill/discharge)."""
        v = {"up": (0, L), "down": (0, -L), "left": (-L, 0), "right": (L, 0)}[dxn]
        axb.annotate("", xy=(x + v[0], z + v[1]), xytext=(x, z),
                     arrowprops=dict(arrowstyle="-|>", lw=1.4, mutation_scale=9,
                                     color=color), zorder=15)

    # Paper x-extent.  The drawing lives in D0–D1 (4560–6760); NOTE_MARGIN adds a
    # right-hand column wide enough that the notes block sits ON the sheet — under
    # the full-width title block — instead of hanging off its right edge.  The
    # mirror map (mxa) pivots on the DRAWING-span center (D0+D1)/2, independent of
    # the margin, so View B still mirrors with the notes in the same screen corner.
    D0, D1, NOTE_MARGIN = 4560, 6760, 1120
    figb, axb = plt.subplots(figsize=(12.6 * (D1 - D0 + NOTE_MARGIN) / (D1 - D0), 15.3))
    if side == 'a':
        axb.set_xlim(D0, D1 + NOTE_MARGIN)
    else:
        axb.set_xlim(D1, D0 - NOTE_MARGIN)   # reversed → whole drawing renders mirrored
    axb.set_ylim(-300, 2520)
    axb.set_aspect("equal")
    axb.axis("off")

    # ── Container shell context ──────────────────────────────────────────────
    _rect(4860, -90, 5933 - 4860, 90, C_WALLB, lw=0.8, z0=2, hatch="////")   # floor
    axb.text(4890, -125, "CONTAINER FLOOR", fontsize=6, ha=_ha("left"), va="center", color="#555", **FB)
    _rect(WALLX, 0, 40, C_HGT, C_WALLB, lw=0.8, z0=2, hatch="\\\\")           # sealed end wall
    axb.text(WALLX + 120, C_HGT - 60, f"SEALED\nEND WALL\n(X={int(C_LEN)})", fontsize=6,
             ha="center", va="top", color="#555", **FB)
    axb.plot([4860, WALLX], [C_HGT, C_HGT], color="#999", lw=0.8, ls=(0, (6, 4)), zorder=2)
    axb.text(4890, C_HGT + 25, f"CEILING (Z={int(C_HGT)})", fontsize=6, ha=_ha("left"), color="#777", **FB)

    # ── Rear panel (edge-on) ─────────────────────────────────────────────────
    _rect(PANX, PAN_ZB, PANX1 - PANX, PAN_ZT - PAN_ZB, C_PLYB, lw=1.3, z0=6)
    leader(axb, PANX1, 640, 5640, 520,
           f"18mm REAR PANEL\n(edge-on)\nX={PANX}–{PANX1}\nZ={PAN_ZB}–{PAN_ZT}",
           color=C_OUT, fs=6, ha=_ha("left"), va="top", arrow_style="-|>", font=FB)

    # ── 25mm pump-mount shirt (in FRONT of the rear panel, −X) ───────────────
    _rect(SHIRTX0, SHIRT_ZB, SHIRTX1 - SHIRTX0, SHIRT_ZT - SHIRT_ZB,
          C_PLYB, lw=1.2, z0=6, alpha=0.85)
    leader(axb, (SHIRTX0 + SHIRTX1) / 2, 480, 4570, 545,
           "25mm PUMP-MOUNT SHIRT",   # dims + cam-clamp detail live in Note 1
           color="#7A6A40", fs=5.5, ha=_ha("left"), va="center", arrow_style="-|>", font=FB)
    # ~27mm chase gap (shirt back 5077 → panel front 5104) + 6 spacer blocks
    for bz in (320, 920, 1560):
        _rect(SHIRTX1, bz, PANX - SHIRTX1, 80, C_PLYB, ec=C_OUT, lw=0.6, z0=7)
    draw_dim_h(axb, SHIRTX1, PANX, 60, f"{PANX - SHIRTX1}mm\nchase", offset=4,
               fs=5, above=False, font=FB)
    axb.text(SHIRTX1 + (PANX - SHIRTX1) / 2 + 90, 1700,
             "6× SPACER\nBLOCKS", fontsize=4.6, ha="center", va="center",
             color="#7A6A40", zorder=10, **FB)

    # ── Pump + ACC stack on the shirt front (single column, projected along Yd) ──
    # 3D bases (Z AFF): ACC 355, P-01 615, P-04 940, P-05 1340, P-03 1740.
    for zb, h, lbl, hot in [(355, 200, "ACC-01", True), (615, 180, "P-01", False),
                            (940, 180, "P-04", True), (1340, 180, "P-05", True),
                            (1740, 180, "P-03", False)]:
        _rect(PUMP_FRONT_X, zb, PUMP_BACK_X - PUMP_FRONT_X, h,
              "#E6D9F0" if hot else "#EAEAEA", ec=C_OUT, lw=0.9, z0=5)
        axb.text((PUMP_FRONT_X + PUMP_BACK_X) / 2, zb + h / 2, lbl, fontsize=6,
                 ha="center", va="center", color="#202020", fontweight="bold", zorder=15,
                 bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85), **FB)
    leader(axb, PUMP_FRONT_X, 1830, 4570, 1980,
           "PUMP COLUMN + ACC-01\n(P-01/P-04/P-05/P-03 + ACC-01,\nsame stack as the front elevation)",
           color="#777", fs=5.3, ha=_ha("left"), va="center", arrow_style="-|>", font=FB)

    # ── Drain-riser spine (18mm ply fin, teed off the rear panel into the corridor) ──
    # The spine plane separates the two faces: VIEW A draws the −Yd intake runs,
    # VIEW B (mirror) draws the +Yd discharge runs.
    _rect(PANX, SPINE_ZB, SPX1 - PANX, SPINE_ZT - SPINE_ZB, C_PLYB, lw=1.2,
          z0=8, alpha=0.55)
    leader(axb, (PANX + SPX1) / 2, 1180, 5650, 1140,
           f"DRAIN-RISER SPINE\n18mm ply, teed perpendicular off the rear\n"
           f"panel (a T in plan) — X={PANX}–{SPX1}, Z={SPINE_ZB}–{SPINE_ZT};\n"
           "the back-of-panel drain risers P-clip to it",
           color=C_OUT, fs=6, ha=_ha("left"), va="center", arrow_style="-|>", font=FB)

    # ── Fitting landmarks (drawn in BOTH views) ──────────────────────────────
    # (DV-01 and DV-02 diverters are View-A-only — their recycle/waste/brown
    #  legs all run on the −Yd intake face — so they live in the VIEW A block.)
    # X1 fill cross (4-way) on the spine + the end-wall X1 camlock + CV-1.
    _pipe([X1X, WALLX], [X1_PORT_Z, X1_PORT_Z], C_BLUEB, zorder=11)              # → end-wall X1 fill camlock
    # CV-1 (one-way / check valve) + the end-wall DC camlock on the X1 gravity-fill line.
    # Flow allowed toward lower X (the cross / IBC fills); keep data-space "left" so
    # View B's reversed xlim flips the arrow with the rest of the drawing.
    valve_check(axb, 5693, X1_PORT_Z, 15, C_BLUEB, flow="left")
    axb.text(5693, X1_PORT_Z + 22, "CV-1", fontsize=4.2, ha="center", va="bottom", color=C_BLUEB, zorder=15, **FB)
    _rect(5836, X1_PORT_Z - 16, 34, 32, "white", ec=C_BLUEB, lw=1.0, z0=14)      # 2" DC camlock (X1 fill)
    axb.text(5833, X1_PORT_Z - 26, "X1 camlock\n(end wall)", fontsize=4.0, ha="center", va="top",
             color=C_BLUEB, zorder=15, **FB)
    axb.add_patch(mpatches.Circle((X1X, X1_PORT_Z), 16, facecolor="white",
                  edgecolor=C_BLUEB, lw=1.4, zorder=14))
    axb.text(X1X - 64, X1_PORT_Z + 36, "X1 FILL CROSS\n(4-way)", fontsize=5, ha="center",
             va="bottom", color=C_BLUEB, zorder=14, **FB)
    axb.text(X1X, X1_PORT_Z - 182, "IBC-1 (X1) +\nIBC-2 (X2) fills", fontsize=4.4,
             ha="center", va="top", color=C_BLUEB, zorder=13, **FB)
    # X1/X2 balance — Blue equalization cross-tie between IBC-1 ↔ IBC-2: a 2"
    # pipe running in Yd between the two totes, so it reads end-on as a pipe
    # cross-section (2× the POD drain runs → OD ring + bore).
    axb.add_patch(mpatches.Circle((X1X, 1376), POD, facecolor="white",
                  edgecolor=C_BLUEB, lw=1.6, zorder=13))                        # 2" OD
    axb.add_patch(mpatches.Circle((X1X, 1376), POD - 9, facecolor="white",
                  edgecolor=C_BLUEB, lw=0.9, zorder=14))                        # bore
    axb.text(X1X - POD - 6, 1376, "X1/X2 BALANCE\n(2\" Blue equalization tie)", fontsize=4.4,
             ha=_ha("right"), va="center", color=C_BLUEB, zorder=14, **FB)
    # IBC-4 merge tee (a circle on the spine).
    axb.add_patch(mpatches.Circle((MERGEX, 1230), 16, facecolor="white",
                  edgecolor=C_WASTEB, lw=1.6, zorder=13))
    leader(axb, MERGEX, 1230, 5650, 1370,
           "IBC-4 MERGE TEE\n(DV-01 + DV-02 waste,\nconsolidated on the spine)",
           color="#555", fs=5.5, ha=_ha("left"), va="center", arrow_style="-|>", font=FB)

    # ════════════════════════════════════════════════════════════════════════
    #  VIEW A ONLY — −Yd INTAKE face (suctions · recycle · fills · merge)
    # ════════════════════════════════════════════════════════════════════════
    if _NEAR == '-Yd':
        # DV-01 — pH-gated filter-output diverter, low at the corridor mouth
        # (its blue-recycle and waste legs are both on this −Yd intake face).
        DV01X = 4700
        valve_3way(axb, DV01X, 235, 16, "#8A6D08", ports=("left", "up", "down"))
        axb.text(DV01X, 258, "DV-01", fontsize=4.6, ha="center",
                 va="bottom", color="#8A6D08", zorder=13, **FB)
        # P-01 suction: P-01 IN → −X to BV-01 (front of the corridor, walkway-
        # reachable, Z≈1000) → UP the front vertical to the loop top → +X back
        # through the shirt + panel → up the behind-panel riser to the Blue tote.
        BV01X = 4840                                       # drawn −X of its true X (3D bvx=4875) so the blue
        #   suction reads CLEAR of the brown P-05 riser (X4898) — their 24mm pipe walls otherwise abut
        BLUE_BEHIND_X = 5165                               # 3D beh_x=5200; drawn −X of the X4 riser (5200) so the
        #   two read as SEPARATE risers (in 3D they share X5200 but sit on different Yd lanes / depths)
        BLUE_LOOPZ = 1210                                  # 3D loopz — loop top (P-04↔P-05 gap)
        # pump-front → −X to BV-01 → UP the front vertical to the loop top → +X (ONE pipe, so the elbow at the
        # riser top IS drawn).  GAP-BROKEN where the +X run crosses the P-05 brown SHIRT riser (X5070) so it
        # reads continuous (projection crossing — different Yd in 3D).
        _pipe([PUMP_FRONT_X, BV01X, BV01X, 5070 - 16], [777, 777, BLUE_LOOPZ, BLUE_LOOPZ], C_BLUEB, zorder=11)
        valve_ball(axb, BV01X, 1000, 16, C_BLUEB, vert=True)
        _pipe([5070 + 16, BLUE_BEHIND_X, BLUE_BEHIND_X], [BLUE_LOOPZ, BLUE_LOOPZ, 1400], C_BLUEB, zorder=11)
        _flowhead(BLUE_BEHIND_X, 1380, "down", C_BLUEB)    # suction: Blue #1 tote → down the riser → P-01
        axb.text(BLUE_BEHIND_X + 60, 1370, "from Blue #1\n(behind-panel\nP-01 suction riser)", fontsize=4.2,
                 ha="left", va="top", color=C_BLUEB, zorder=13, **FB)
        leader(axb, BV01X, 1000, 4600, 1140, "BV-01 (P-01 suction)\nfront · walkway-reachable",
               color=C_BLUEB, fs=5, ha="right", va="center", arrow_style="-|>", font=FB)
        # X4 suction PICKUP riser climbs the spine, then WRAPS −X to the forward BV-06 riser, up through
        # BV-06, +X into the P-03 IN — BV-06 on a forward loop (operator side), same pattern as BV-02.
        # The wrap gap-breaks where it crosses the DV-02→IBC-3 brown chase drop (X5090).
        BV06X = 4898                                       # 3D rx6 = PXC−86 (forward)
        _pipe([RX4, RX4, 5090 + 16], [300, 1700, 1700], C_WASTEB, zorder=11)                    # riser up → −X wrap
        _pipe([5090 - 16, BV06X, BV06X, PXC], [1700, 1700, 1902, 1902], C_WASTEB, zorder=11)    # → BV-06 riser → up → +X into P-03 IN
        valve_ball(axb, BV06X, 1792, 16, C_WASTEB, vert=True)
        axb.text(BV06X - 22, 1792, "BV-06", fontsize=4.6, ha="right", va="center", color=C_WASTEB, zorder=13, **FB)
        _flowhead(RX4, 330, "up", C_WASTEB)                # suction: IBC-4 waste pickup → up the spine → BV-06 → P-03
        axb.text(RX4 + 135, 255, "from IBC-4 (waste pickup)", fontsize=4.0, ha="right",
                 va="top", color=C_WASTEB, zorder=12,
                 bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85), **FB)
        # DV-01 BLUE RECYCLE — straight +X off the diverter, THROUGH the rear panel, up the spine to X1.
        _pipe([DV01X, RX_BLUE, RX_BLUE, X1X],
              [276, 276, X1_PORT_Z, X1_PORT_Z], C_BLUEB, zorder=13)
        axb.text(PANX + 9, 300, "through\npanel", fontsize=4.0, ha="center", va="bottom",
                 color="#999", zorder=14, **FB)
        # DV-01 WASTE → the IBC-4 merge tee (lower, parallel lane).
        _pipe([DV01X, MERGEX, MERGEX], [222, 222, 1214], C_WASTEB, zorder=11)
        # → IBC-1 (X1) fill stub off the cross (water continues down to IBC-1, off-section).
        _pipe([X1X - 14, X1X - 14], [X1_PORT_Z, X1_PORT_Z - 140], C_BLUEB, zorder=11)
        _flowhead(X1X - 14, X1_PORT_Z - 140, "down", C_BLUEB)   # fill: → IBC-1 tote (below)
        # DV-02 — tray-drain diverter above the pump column (3D: run along Yd,
        # branch z−).  Its input is the P-04 discharge (rear +Yd face, Spine View
        # B), arriving at the junction.  Both outputs sit on this −Yd face and
        # leave toward +X: BROWN runs +X into the shirt↔panel chase then drops to
        # IBC-3; WASTE runs +X then drops to the IBC-4 merge tee.  DV-02 is now
        # mounted on the raised shirt front (X5028).  Symbol centred on the junction.
        valve_3way(axb, DV02X, 2145, 18, "#B8860B", ports=("left", "right", "down"))
        axb.text(DV02X, 2145 + 32, "DV-02", fontsize=5, ha="center", va="bottom",
                 color="#8A6D08", zorder=14, **FB)
        axb.text(DV02X - 26, 2145, "← P-04\n(View B)", fontsize=3.8, ha="right",
                 va="center", color="#999", zorder=13, **FB)
        # DV-02 BROWN output → IBC-3 (Brown): leaves the −Yd run port, runs +X into
        # the ~27mm shirt↔panel chase (X≈5090), then DROPS down the chase to the
        # IBC-3 entry level. (3D: down off the run port, +X to the chase, drop.)
        BROWN_CHASE_X = 5090
        # brown leaves at z2120 (below the waste run at 2145) so the two +X outputs read SEPARATELY
        # near the diverter (in 3D they leave opposite Yd run ports — projection-coincident here).
        # GAP-BROKEN where it crosses the X4 suction-pickup horizontal into P-03 (z1820) so that run reads continuous
        _pipe([DV02X, DV02X, BROWN_CHASE_X, BROWN_CHASE_X], [2128, 2120, 2120, 1836], C_BROWNB, zorder=10)
        _pipe([BROWN_CHASE_X, BROWN_CHASE_X], [1804, 1130], C_BROWNB, zorder=10)
        axb.annotate("", xy=(BROWN_CHASE_X, 1135), xytext=(BROWN_CHASE_X, 1185),
                     arrowprops=dict(arrowstyle="-|>", lw=1.2, mutation_scale=7, color=C_BROWNB), zorder=12)
        axb.text(BROWN_CHASE_X + 26, 1175, "IBC-3\n(Brown,\ndown chase)", fontsize=4.2, ha="left", va="top",
                 color=C_BROWNB, zorder=13, **FB)
        # DV-02 WASTE output → leaves the +Yd run port, PENETRATES the rear panel
        # near the spine top, then DROPS at X5289 (3D dvwx = MERGE4[0]−115) into the
        # merge tee's LEFT side.
        _hpipe(2145, DV02X + 18, 5289, C_WASTEB, zorder=11, crosses=(PANX + 9, RX_BLUE))
        axb.text(PANX + 9, 2178, "through\npanel", fontsize=4.0, ha="center", va="bottom",
                 color="#999", zorder=12, **FB)
        # Lead the drop in from a short horizontal (from 5261, clear of the blue-
        # riser crossing gap) so the top corner at (5289,2145) is an INTERIOR
        # vertex and draws an elbow fitting — the _hpipe ends there straight, so
        # without this the left turn into the DV-02 horizontal had no elbow.
        _pipe([5261, 5289, 5289, MERGEX], [2145, 2145, 1230, 1230], C_WASTEB, zorder=11)
        # IBC-4 (Waste) tote entry — the merge tee's RIGHT pipe.
        _pipe([MERGEX, 5494, 5494], [1230, 1230, 1085], C_WASTEB, zorder=11)
        axb.annotate("", xy=(5494, 1100), xytext=(5494, 1150),
                     arrowprops=dict(arrowstyle="-|>", lw=1.3, mutation_scale=8, color=C_WASTEB), zorder=12)
        axb.text(5506, 1120, "→ IBC-4\n(Waste tote)", fontsize=4.8, ha="left", va="top",
                 color=C_WASTEB, zorder=13, **FB)
        # ACC-01 OUT → Blue supply trunk → spray bar / TAP-01.  The trunk teed onto
        # the ACC-01 bottom OUT port (3D acc_out(), Z383 on the −Yd face) DROPS to
        # the corridor-entry lane (Z235 = DV-01's low lane, out of the operator's
        # way at the mouth), then −X to the tray-gap drop.
        ACC_OUT_Z = 383                                   # 3D ACC_PZ = ACC_Z0 + 28 — bottom OUT port
        circ_yd = PXC                                     # ACC OUT port projects to the body axis
        axb.add_patch(mpatches.Circle((circ_yd, ACC_OUT_Z), 6, facecolor="white",
                      edgecolor=C_BLUEB, lw=1.0, zorder=12))     # ACC-01 OUT port stub
        # Gap-broken at Z308 where the drop crosses the brown P-05 tap run (X4910–5070,
        # a projection crossing — different Yd in 3D) so the blue does not read as
        # teeing into the brown.
        _pipe([PXC, PXC], [ACC_OUT_Z, 308 + 18], C_BLUEB, zorder=9)                  # port stub → down to the brown crossing
        _pipe([PXC, PXC, 4655, 4655], [308 - 18, 235, 235, 30], C_BLUEB, zorder=9)   # below the crossing → −X → down to spray bar
        _flowhead(4655, 80, "down", C_BLUEB)              # supply: → spray bar / TAP-01 (off-section)
        axb.text(4648, -10, "Blue supply\nto spray bar / TAP-01", fontsize=4.2, ha="left",
                 va="bottom", color=C_BLUEB, zorder=12, **FB)
        # P-04 tray-drain SUCTION (← from the tray sump, far −X) up to P-04 IN.
        # Gap-broken where it crosses the blue supply trunk, now lowered to Z235:
        # the floor run at Z205 crosses the blue VERTICAL drop at X4655, and the
        # rise at X4908 crosses the blue HORIZONTAL trunk at Z235 — so the blue
        # reads continuous (skill_plumbing_drawing: the crossing run breaks).
        _pipe([4600, 4655 - 16], [205, 205], C_WASTEB, zorder=9)   # floor, before the blue drop at 4655
        _pipe([4655 + 16, 4908], [205, 205], C_WASTEB, zorder=9)   # floor, after the blue drop
        _pipe([4908, 4908], [205, 235 - 16], C_WASTEB, zorder=9)   # rise, up to the blue trunk crossing
        # rise past blue → +X back to the P-04 IN at the pump axis (PXC) — the forward-riser LOOP
        _pipe([4908, 4908, PXC], [235 + 16, 1075, 1075], C_WASTEB, zorder=9)
        _flowhead(4600, 205, "right", C_WASTEB)            # suction: tray sump → P-04
        axb.text(4546, 185, "from\ntray sump", fontsize=4.2, ha="left", va="top", color="#555", zorder=12, **FB)
        # P-05 brown-drain SUCTION (IBC-3 Brown tap via BV-02).  3D: +X off the tee to the SHIRT riser
        # (X5070, P-clipped for support — the down-route to the tap), UP the shirt, then −X (forward) to the
        # BV-02 riser (X4898, operator side) through the P-04↔P-05 gap, up through BV-02, +X into the P-05 IN.
        BV02X = 4898                                       # 3D rx = PXC−86 (BV-02 forward, operator side)
        SHIRT_RX = 5070                                    # 3D shirt_rx — shirt riser, the down-route to the tap
        ZLOOP = 1300                                       # 3D zloop — step −X from the shirt riser onto BV-02's
        _pipe([4910, SHIRT_RX, SHIRT_RX, BV02X, BV02X, PXC],
              [308, 308, ZLOOP, ZLOOP, 1502, 1502], C_BROWNB, zorder=9)
        valve_ball(axb, BV02X, 1417, 16, C_BROWNB, vert=True)
        axb.text(BV02X - 22, 1417, "BV-02", fontsize=4.6, ha="right", va="center",
                 color=C_BROWNB, zorder=13, **FB)
        _flowhead(SHIRT_RX, 700, "up", C_BROWNB)           # suction: IBC-3 shared tap → up the shirt riser → BV-02 → P-05
        axb.text(4914, 296, "from IBC-3 (shared tap):\n+X to shirt riser, up, then\nforward loop to BV-02",
                 fontsize=3.8, ha="left", va="top", color=C_BROWNB, zorder=12, **FB)
        # P-clips fastening the −Yd-face spine risers.
        for rx, zt in [(RX4, 1800), (RX_BLUE, X1_PORT_Z), (MERGEX, 1214)]:
            for i in range(4):
                cz = 460 + i * 400
                if cz < zt - 80:
                    _rect(rx - 8, cz - 11, 16, 22, C_STEEL, lw=0.6, z0=11)
        leader(axb, RX4, 1000, 5690, 880,
               "FRONT of spine (−Yd face), P-clipped:\nX4 suction-pickup riser (→ P-03),\nblue-recycle + DV-01-waste risers",
               color="#555", fs=5.2, ha="left", va="top", arrow_style="-|>", font=FB)
        leader(axb, RX_BLUE, 900, 4720, 740, "BLUE-RECYCLE RISER\n(DV-01 → up the spine → X1 cross)",
               color=C_BLUEB, fs=5.2, ha="right", va="top", arrow_style="-|>", font=FB)

    # ════════════════════════════════════════════════════════════════════════
    #  VIEW B ONLY — +Yd DISCHARGE face (pump discharges)
    #  These are the NEAR face here, so each discharge is drawn FULL: pump →
    #  along the spine → end-wall port (no spine occlusion).
    # ════════════════════════════════════════════════════════════════════════
    if _NEAR == '+Yd':
        X4V, X3V = 5750, 5772
        # X4 discharge (P-03 → X4 port): full run from the pump along the spine.
        _pipe([PUMP_BACK_X, X4V, X4V, WALLX], [1902, 1902, X4_PORT_Z, X4_PORT_Z],
              C_WASTEB, zorder=12)
        # X3 discharge (P-05 → X3 port): full run from the pump along the spine.
        _pipe([PUMP_BACK_X, X3V, X3V, WALLX], [1502, 1502, X3_PORT_Z, X3_PORT_Z],
              C_BROWNB, zorder=13)
        # P-01 discharge → ACC-01 (short drop into the accumulator below P-01).
        _pipe([5012, 5012], [612, 558], C_BLUEB, zorder=9)
        # P-04 tray-drain DISCHARGE → up the back (SV-02 sample tap) → DV-02
        # (the diverter itself is drawn on Spine View A).
        _pipe([5046, 5046, DV02X, DV02X], [1113, 2025, 2025, 2110], C_WASTEB, zorder=9)
        axb.annotate("", xy=(DV02X, 2140), xytext=(DV02X, 2098),
                     arrowprops=dict(arrowstyle="-|>", lw=1.1, mutation_scale=7, color=C_WASTEB), zorder=12)
        axb.text(DV02X + 22, 2088, "→ DV-02\n(Spine View A)", fontsize=4.0, ha="left",
                 va="bottom", color="#999", zorder=13, **FB)
        valve_ball(axb, 5046, 1150, 14, "#555", vert=True)
        axb.text(5066, 1150, "SV-02", fontsize=4.0, ha=_ha("left"), va="center", color="#555", zorder=13, **FB)
        # → IBC-2 (X2) fill stub off the cross (water continues down to IBC-2, off-section).
        _pipe([X1X + 14, X1X + 14], [X1_PORT_Z, X1_PORT_Z - 140], C_BLUEB, zorder=11)
        _flowhead(X1X + 14, X1_PORT_Z - 140, "down", C_BLUEB)   # fill: → IBC-2 tote (below)
        leader(axb, 5640, 1700, 6120, 1820,
               "+Yd DISCHARGE face (near):\nX3 / X4 pump discharges → end-wall ports",
               color=C_BROWNB, fs=5.2, ha=_ha("left"), va="center", arrow_style="-|>", font=FB)

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
    if _NEAR == '-Yd':
        cross_note = ("Pump discharges + IBC-2 fill are on Spine View B "
                      "(+Yd face).")
    else:
        cross_note = ("Suctions, recycle, fills + merge are on Spine View A "
                      "(−Yd face).")
    draw_notes(axb, [
        "CORRIDOR PLUMBING PANEL — SPINE SIDE SECTION (looking along Yd):",
        cross_note,
        "1. Pumps + ACC-01 mount on the FRONT (−X) of the rear panel, cam-clamped to a 25mm pump-mount shirt that backs the bodies (X=5052–5077, Z=325–2191); the shirt top backs DV-02.",
        "2. A ~27mm chase gap separates the shirt back (X=5077) and the rear-panel front (X=5104); six ply spacer blocks bridge it.",
        "3. Rear panel: 18mm ply, X=5104–5122, Z=50–2246. The drain-riser spine is an 18mm ply fin teed perpendicular off it into the rear corridor (X=5104–5560, Z=280–2246).",
        "4. View A (−Yd intake face): X4 suction-pickup riser, blue-recycle riser onto the spine into the X1 fill cross, DV-01-waste → merge, suctions, fills.",
        "5. View B (+Yd discharge face): the X3 brown (P-05 → Z=1700) and X4 grey (P-03 → Z=1620) pump discharges run full along the spine to the end-wall ports.",
        "6. DV-02 → IBC-3 / IBC-4; the IBC-4 merge tee (DV-01 + DV-02 waste) is consolidated on the spine.",
        "7. Circuit C powers all 5 pumps (one IP switch each, run one at a time); P-02 lives on the Pinhole Wall panel and shares Circuit C.",
        "8. Spine riser X-lanes: X4 suction pickup 5200, blue-recycle 5239, DV-01-waste/merge 5404, X1 cross 5500. End-wall ports: X1 fill Z2250, X3 Z1700, X4 Z1620.",
        "9. X1 fill is a 4-way cross (X1 in + IBC-1 + IBC-2 + DV-01 recycle return) with CV-1 one-way valve + 2\" DC camlock at the end wall; X1/X2 balance = Blue equalization tank-body tie.",
        "10. PIPE: 1\" PVC Sch-40 (IBC fill/drain + recycle) and 1/2\" PVC (pump runs), threaded at components; risers stainless P-clipped to the spine face.",
    ], mxa(6800), 2440, spacing=27, fs=9.3, ha="left", width=900, wrap=42, font=FB)

    # ── SYMBOL KEY (top-left screen corner; mxa anchors the screen-left edge,
    #    and draw_symbol_key lays out in screen space for the reversed View-B axis) ──
    draw_symbol_key(axb, mxa(4570), 2470, r=15, row=82, fs=6, w=280)

    if _NEAR == '-Yd':
        dtitle = "CORRIDOR PLUMBING PANEL — SPINE VIEW A"
        subt = "SPINE VIEW A · −Yd INTAKE FACE (suctions · recycle · fills)"
    else:
        dtitle = "CORRIDOR PLUMBING PANEL — SPINE VIEW B"
        subt = "SPINE VIEW B · +Yd DISCHARGE FACE (pump discharges)"
    title_block(axb, "CORRIDOR PANEL — SPINE",
                drawing_title=dtitle,
                subtitle=subt,
                scale_note="CORRIDOR SIDE SECTION ALONG Yd · AXES IN mm",
                doc_id="TBS-001 · Plumbing Panel",
                height=0.05)

    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    outb = os.path.join(DIAGRAMS_DIR, f"panel-spine-view-{side}.png")
    figb.savefig(outb, dpi=DIAGRAM_DPI, facecolor="white", edgecolor="none",
                 bbox_inches="tight", pad_inches=0.2)
    plt.close(figb)
    print(f"Spine view {side.upper()} → {outb}")


spine_view('a')
spine_view('b')
