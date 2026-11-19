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

Outputs: docs/assets/panel-layout.png, docs/assets/pinhole-panel.png,
         docs/assets/panel-spine-view-a.png, docs/assets/panel-spine-view-b.png
"""

import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from tbs_constants import C_PIPE_FRESH, C_PIPE_RECYCLE, C_PIPE_WASTE, C_PIPE_FITTING
from tbs_constants import C_OUT, C_DIM, C_STEEL, DIAGRAMS_DIR, PUMP_PIPE_OD, PUMP_PIPE_WALL, EQPANEL_X, EQPANEL_H, DIAGRAM_DPI, FONT, C_WALL
from tbs_constants import PWP_PANEL_NOTCH_BR, PWP_PANEL_NOTCH_TR
from tbs_constants import BB_OD, PWP_FILTER_X1, PWP_FILTER_X2, PWP_FILTER_X3, PWP_FILTER_TOP_Z, PWP_FILTER_BOT_Z, PWP_FILTER_HEAD_Z, PWP_SV01_X, PWP_SV01_Z, PWP_SROW_Z0, PWP_SV02_Z, PWP_DV02_Z, PWP_ACC2_X, PWP_ACC2_Z0, PWP_PANEL_X0, PWP_PANEL_X1, PWP_PANEL_Z0, PWP_PANEL_H
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_notes, draw_pipe_path as _tbs_pipe_path, valve_ball, valve_3way, valve_check
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "models"))
import generate_corridor_water_panel as cwp   # corridor-panel geometry — single source for the side-section (was hard-coded + stale)
from tbs_title_block import title_block


_W3D = None


def water_3d():
    """The live water.skp build, captured in-process: every named pipe run's waypoints, every
    flex jumper's end points, every in-line check / ball valve's center (3D mm, keyed "CV-2", "BV-01"),
    and every P-clip on a standoff block (name, cx, cz, block face Yd, pipe Yd, vertical).  The 2D sheets read
    routes from here so they can't drift from the model."""
    global _W3D
    if _W3D is None:
        import tbs_draw as d
        runs, flex, checks, clips = {}, [], {}, []
        o_run, o_flex, o_cyl, o_clip = d.ruby_pipe_run, d.ruby_flex_run, d.ruby_cylinder, cwp.clip_on_block

        def run(name, wps, r, *a, **k):
            runs.setdefault(name, [tuple(map(float, q)) for q in wps])
            return o_run(name, wps, r, *a, **k)

        def fl(name, wps, r, *a, **k):
            flex.append((name, [tuple(map(float, q)) for q in wps]))
            return o_flex(name, wps, r, *a, **k)

        def cyl(name, cx, cy, cz, rad, h, *a, **k):
            if (name.startswith(("CV-", "BV-")) or "one-way valve" in name) and "handle" not in name:
                ax_ = k.get("axis", "z")
                c = [cx, cy, cz]
                c["xyz".index(ax_)] += h / 2
                checks["CV-1" if "one-way valve" in name else name.split(" ")[0]] = tuple(map(float, c))
            return o_cyl(name, cx, cy, cz, rad, h, *a, **k)

        def clip(nm, cx, cz, face_y, pipe_y, vertical, *a, **k):
            clips.append((nm, float(cx), float(cz), float(face_y), float(pipe_y), vertical))
            return o_clip(nm, cx, cz, face_y, pipe_y, vertical, *a, **k)

        d.ruby_pipe_run, d.ruby_flex_run, d.ruby_cylinder, cwp.clip_on_block = run, fl, cyl, clip
        try:
            import generate_pinhole_water_panel as pw
            ruby = pw.build()
        finally:
            d.ruby_pipe_run, d.ruby_flex_run, d.ruby_cylinder, cwp.clip_on_block = o_run, o_flex, o_cyl, o_clip
        runs = {n: w for n, w in runs.items() if f'grp.name = "{n}"' in ruby}    # emitted runs only
        _W3D = {"runs": runs, "flex": flex, "checks": checks, "clips": clips}
    return _W3D

# ── Panel geometry ────────────────────────────────────────────────────────
PANEL_T      = 18    # plywood thickness (mm)
PANEL_YD     = cwp.YD_NEAR  # 1046 — panel near edge Yd (mm from pinhole wall)
PANEL_WALL_X = EQPANEL_X  # panel face X position (= EQPANEL_X)
from tbs_constants import WALKWAY_W   # standard walkway width (mm)
WALKWAY_Z    = 100   # walkway grating top (mm AFF)

# Panel face dimensions (new orientation: spans corridor)
PANEL_W  = 270   # face width (mm, Yd span: 1046–1316)
PANEL_H  = EQPANEL_H  # face height (mm, =2060; Z span: 250–2310)
PANEL_Z_AFF = 200  # panel bottom Z above finished floor

# ── Shurflo 2088 pump dimensions ─────────────────────────────────────────
PUMP_W   = 2 * cwp.PVB_R                  # 100 — upright body Ø (3D pump_unit)
PUMP_BODY_H = cwp.PVB_H                   # 180 — body height
PUMP_H   = cwp.PVB_H + cwp.PCAP_H         # 210 — body + head
PORT_ZOFF = cwp.PVB_H - 18                # 162 — port centerline above the pump base (3D pz)
from tbs_constants import PUMP_D   # depth from panel (mm) — real Shurflo 2088 (4.5")
from tbs_constants import IBC_D    # IBC tote depth (mm) — used by the cross-section strip
PUMP_GAP = 40    # vertical gap between pumps (mm)
PORT_HALF = 30   # half of port-to-port spacing (mm)

# ── Accumulator ───────────────────────────────────────────────────────────
ACC_OD  = 2 * cwp.ACC_R    # 127 — body OD (mm)
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
PUMP_COL_C    = cwp.CTR_Y - PANEL_YD      # 135 — pump-column center (3D Yd1181)
CORR_PORT_IN  = cwp.PIY - PANEL_YD        # 71.5 — IN port TIP (Shurflo 2088-554-144: 127mm across the tips)
CORR_PORT_OUT = cwp.POY - PANEL_YD        # 198.5 — OUT port TIP
LANE_IN  = cwp.PORT_TURN_YD_IN - PANEL_YD    # 34 — near-board suction riser lane (adapter + turn elbow off the IN tip)
LANE_OUT = cwp.PORT_TURN_YD_OUT - PANEL_YD   # 237 — far-board discharge riser lane

# Pump body bases (panel-Z = 3D AFF − 200):
P01_Z = cwp.PSTACK["P-01"] - PANEL_Z_AFF   # P-01 Blue supply
P04_Z = cwp.PSTACK["P-04"] - PANEL_Z_AFF   # P-02 Brown recycle (in the tray-drain pump's vacated corridor slot)
P05_Z = cwp.PSTACK["P-05"] - PANEL_Z_AFF   # P-05 Brown drain
P03_Z = cwp.PSTACK["P-03"] - PANEL_Z_AFF   # P-03 Waste drain

# ACC-01 — Ø127 × 200 cylinder at the very bottom, below P-01.
ACC_YD = PUMP_COL_C
ACC_Z  = cwp.ACC_Z0 - PANEL_Z_AFF       # ACC bottom (3D ACC_Z0)
ACC_PORT_Z = cwp.ACC_PZ - PANEL_Z_AFF   # ACC IN/OUT port centerline (3D ACC_PZ)
ACC_PORT_L = 30                          # ACC IN/OUT port stub length (= the 3D port cylinders)

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
C_BLUE       = C_PIPE_FRESH
C_BLUE_EC    = "#1A5A8A"
C_BROWN      = C_PIPE_RECYCLE
C_BROWN_EC   = "#5A3A20"
C_BLACK_SYS  = C_PIPE_WASTE
C_BLACK_EC   = "#444444"
C_FILTER     = "#4A90D9"
C_PUMP_BODY  = "#E0D0C0"
C_PUMP_EC    = "#806040"
C_ACC        = "#5A9ACC"
C_PIPE_FILL  = C_PIPE_FITTING   # port stubs — neutral (black = waste only)
C_PIPE_EC    = "#5A5F66"
C_NEW        = "#22AA44"
C_WALK       = "#A8D8A8"
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


def _new_panel_fig():
    """Create a fresh figure + axes for a panel front elevation; rebinds global ax."""
    global ax
    fig, ax = plt.subplots(1, 1, figsize=(FW, FH), dpi=DIAGRAM_DPI)
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
            f"18mm EXTERIOR PLY\n{PANEL_W}mm x {PANEL_H}mm",
            ha="center", va="top",
            fontsize=5.5, color=C_PLY_EC, zorder=4, **FONT)

    # ── #29 pump-run SIDE SUPPORT BOARDS — edge-on at the near/far corridor walls (this
    #    front-elevation plane cuts through them); each is an 18mm ply board recessed flush on
    #    welded steel L-brackets, the risers P-clipped to it. NEAR wall = local Yd 0 (lower board
    #    Z480-900 + upper board Z1260-1950, backing BV-02/BV-06); FAR wall = local Yd PANEL_W (Z400-820).
    SB_T = 18
    for xb, z0b, z1b in ((0, cwp.SB_NEAR_Z[0], cwp.SB_NEAR_Z[1]), (0, cwp.SB_NEAR_UP_Z[0], cwp.SB_NEAR_UP_Z[1]), (PANEL_W - SB_T, cwp.SB_FAR_Z[0], cwp.SB_FAR_Z[1])):
        rect(xb, z0b - PANEL_Z_AFF, SB_T, z1b - z0b, C_PLY, C_PLY_EC, lw=1.0, zorder=6, alpha=0.9)   # 3D AFF → panel Z
    ax.text(sx(SB_T + 6), sz(1450), "NEAR SIDE\nSUPPORT BOARDS\n(edge-on, on\nwelded L-brackets)",
            ha="left", va="center", fontsize=4.0, color=C_PLY_EC, zorder=9, **FONT)
    ax.text(sx(PANEL_W + 8), sz(560), "FAR SIDE\nSUPPORT BOARD\n(edge-on)",
            ha="left", va="center", fontsize=4.0, color=C_PLY_EC, zorder=9, **FONT)

    # ── PUMPS — SINGLE VERTICAL COLUMN ────────────────────────────────────
    #   Bottom→top: ACC-01 (below P-01), P-01, P-02, P-05, P-03 — all on the corridor
    #   center (3D CTR_Y).  Each upright body takes its IN port on the −Yd (LEFT) side and its
    #   OUT on +Yd (RIGHT), 127mm across the tips (Shurflo 2088-554-144 datasheet).
    _draw_pump(PUMP_COL_C, P01_Z, "P-01", "BLUE\nSUPPLY", C_BLUE, C_BLUE_EC)
    _draw_pump(PUMP_COL_C, P04_Z, "P-02", "BROWN\nRECYCLE", C_BROWN, C_BROWN_EC)
    _draw_pump(PUMP_COL_C, P05_Z, "P-05", "BROWN\nDRAIN", C_BROWN, C_BROWN_EC)
    _draw_pump(PUMP_COL_C, P03_Z, "P-03", "WASTE\nDRAIN", C_BLACK_SYS, C_BLACK_EC)

    # ── ACC-01 — Ø127 × 200 at the very bottom, below P-01; IN (+Yd) / OUT (−Yd) side ports ──
    rect(ACC_YD - ACC_OD / 2, ACC_Z, ACC_OD, ACC_LEN,
         C_ACC, C_BLUE_EC, lw=1.2, zorder=6, alpha=0.7)
    ax.text(sx(ACC_YD), sz(ACC_Z + ACC_LEN / 2 + 12),
            "ACC-01", ha="center", va="center",
            fontsize=7, color="white", fontweight="bold", zorder=8, **FONT)
    ax.text(sx(ACC_YD), sz(ACC_Z + ACC_LEN / 2 - 16),
            f"Ø{ACC_OD:.0f}", ha="center", va="center",
            fontsize=5, color="white", zorder=8, **FONT)
    for y0 in (ACC_YD - ACC_OD / 2 - ACC_PORT_L, ACC_YD + ACC_OD / 2):
        rect(y0, ACC_PORT_Z - PIPE_OD / 2, ACC_PORT_L, PIPE_OD, C_PIPE_FILL, C_PIPE_EC, lw=0.5, zorder=7)

    # ── Zone label ────────────────────────────────────────────────────────
    ax.text(sx(PANEL_W + 8), sz((P01_Z + P03_Z + PUMP_H) / 2),
            "PUMP COLUMN\n(4 transfer pumps,\nupright, in line)",
            ha="left", va="center",
            fontsize=5.5, color=C_PUMP_EC, fontweight="bold", zorder=10, **FONT)

    # ════════════════════════════════════════════════════════════════
    #  PLUMBING — read from the live 3D build (water_3d).  Every run off a port turns one
    #  elbow onto its side-board lane (IN → near board LANE_IN, OUT → far board LANE_OUT)
    #  after a ½" adapter leg.  Runs are drawn in this plane up to their first leg along X;
    #  that leg is marked end-on (⊙ toward the walkway / −X, ⊗ away behind the panel / +X).
    #  The suction risers share the near-board lane at different X depths, so they overlap
    #  in this elevation — their full routes are on Spine View A.
    # ════════════════════════════════════════════════════════════════
    W = water_3d()
    EXIT_L = -70    # label column past the left panel edge (near wall / walkway)
    EXIT_R = 340    # label column past the right panel edge (far wall / sealed end)

    def py(p):
        return p[1] - PANEL_YD, p[2] - PANEL_Z_AFF

    def endon(y, z, toward):
        r = PIPE_OD / 2 + 2
        circ(y, z, r, "white", C_FRAME, lw=1.0, zorder=Z_DISCH + 1)
        if toward:
            circ(y, z, 2.6, C_FRAME, C_FRAME, lw=0.5, zorder=Z_DISCH + 2)
        else:
            for sgn in (1, -1):
                ax.plot([sx(y - r * 0.6), sx(y + r * 0.6)], [sz(z - sgn * r * 0.6), sz(z + sgn * r * 0.6)],
                        color=C_FRAME, lw=0.9, zorder=Z_DISCH + 2)

    def from_tip(tip):
        """The 3D run that starts or ends on this port tip, ordered FROM the tip."""
        for wps in W["runs"].values():
            for seq in (wps, wps[::-1]):
                if math.dist(seq[0], tip) < 0.6:
                    return seq
        raise KeyError(f"no 3D run meets port tip {tip}")

    def port_run(tip, fc, label, side, label_z=None):
        seq = from_tip(tip)
        ys, zs = [], []
        for a, b in zip(seq, seq[1:]):
            if not ys:
                ys.append(py(a)[0]); zs.append(py(a)[1])
            if abs(b[0] - a[0]) > 0.5 and abs(b[1] - a[1]) < 0.5 and abs(b[2] - a[2]) < 0.5:
                endon(ys[-1], zs[-1], toward=b[0] < a[0])
                break
            ys.append(py(b)[0]); zs.append(py(b)[1])
        leg = math.hypot(ys[-1] - ys[-2], zs[-1] - zs[-2]) if len(ys) > 2 else PIPE_OD
        if leg < PIPE_OD:                # sub-OD last leg into a side port: socket it over the port stub so the elbow can form
            k = (leg + ACC_PORT_L) / leg
            ys[-1] = ys[-2] + (ys[-1] - ys[-2]) * k; zs[-1] = zs[-2] + (zs[-1] - zs[-2]) * k
        draw_pipe_path(ax, ys, zs, PIPE_OD, PIPE_WALL, fc=fc, zorder=Z_DISCH)
        if label:
            ex = EXIT_L if side == "left" else EXIT_R
            lz = zs[-1] if label_z is None else label_z
            leader(ax, sx(ys[-1]), sz(zs[-1]), sx(ex), sz(lz), label, fs=5.2, color=fc,
                   ha="right" if side == "left" else "left", va="center", font=FONT)
        return ys[-1], zs[-1]

    stacks = [("P-01", C_BLUE, "FROM IBC-1 (BLUE)\n−X, up past BV-01,\nbehind panel to IBC-1", None,
               "TO ACC-01 IN", None),
              ("P-04", C_BROWN, "FROM IBC-3 (BROWN)\n−X, down past BV-03\nto the shared tap", None,
               "TO ACC-02 (skid)\n−X, down the far board,\nunder-walkway ribbon", None),
              ("P-05", C_BROWN, "FROM IBC-3 (BROWN)\n−X, down past BV-02,\nshirt riser to the tap", None,
               "TO X3 PORT\n+X behind the panel", None),
              ("P-03", C_BLACK_SYS, "FROM IBC-4 (WASTE)\n−X, down past BV-06,\nspine pickup riser", None,
               "TO X4 PORT\n+X behind the panel", None)]
    for key, fc, lin, lzi, lout, lzo in stacks:
        zb = cwp.PSTACK[key]
        port_run(cwp.pump_in(cwp.PXC, cwp.CTR_Y, zb, "y"), fc, lin, "left", lzi)
        if key == "P-01":
            port_run(cwp.pump_out(cwp.PXC, cwp.CTR_Y, zb, "y"), fc, None, "right")
        else:
            port_run(cwp.pump_out(cwp.PXC, cwp.CTR_Y, zb, "y"), fc, lout, "right", lzo)
    # ACC-01 OUT → Blue supply trunk (drops to the panel foot, −X under the walkway to the spray bar)
    port_run((cwp.PXC, cwp.CTR_Y - cwp.ACC_R - 30, cwp.ACC_PZ), C_BLUE,
             "TO SPRAY BAR / TAP-01\n−X, under-walkway ribbon", "left", ACC_Z - 60)

    # ── Isolation ball valves on the near-board suction risers (3D centers, Yd1080 lane) ──
    for bv, fc in (("BV-01", C_BLUE), ("BV-03", C_BROWN), ("BV-02", C_BROWN), ("BV-06", C_BLACK_EC)):
        y, z = py(W["checks"][bv])
        draw_pipe_path(ax, [y, y], [z - BV_R - 8, z + BV_R + 8], PIPE_OD, PIPE_WALL, fc=fc, zorder=Z_DISCH)
        valve_ball(ax, sx(y), sz(z), BV_R, fc, vert=True)
        ax.text(sx(y + BV_R) + 4, sz(z), bv, ha="left", va="center",
                fontsize=4.6, color=fc, fontweight="bold", zorder=14, **FONT)

    # ── Flex jumpers (from the 3D): a gold band along an in-plane leg, a gold ring on an X leg
    #    (end-on); dashed where the jumper sits behind the pump column. ──
    for nm, (a, b) in ((n, (p[0], p[-1])) for n, p in W["flex"]):
        if not ("jumper" in nm and cwp.BACK_X - 200 < a[0] < cwp.BACK_X):
            continue
        (ya, za), (yb, zb_) = py(a), py(b)
        hidden = a[0] > cwp.PXC + cwp.PVB_R and abs(ya - PUMP_COL_C) < PUMP_W / 2 + 15
        ls = (0, (2, 1.5)) if hidden else "-"
        if math.hypot(yb - ya, zb_ - za) < 1:
            ax.add_patch(plt.Circle((sx(ya), sz(za)), PIPE_OD / 2 + 5, fc="none", ec="#E0A800",
                                    lw=2.0, ls=ls, zorder=Z_DISCH + 3))
        else:
            ax.plot([sx(ya), sx(yb)], [sz(za), sz(zb_)], color="#E0A800", lw=PIPE_OD * 0.9,
                    alpha=0.75, solid_capstyle="butt", ls=ls, zorder=Z_DISCH + 3)

    # ── DIMENSIONS ──────────────────────────────────────────────────
    draw_dim_h(ax, sx(0), sx(PANEL_W), sz(-50),
               f"{PANEL_W}mm", offset=4.8, fs=6, color=C_DIM, font=FONT)
    _p1z = P01_Z + PORT_ZOFF
    draw_dim_h(ax, sx(CORR_PORT_IN), sx(CORR_PORT_OUT), sz(P01_Z + PUMP_H + 40),
               f"{CORR_PORT_OUT - CORR_PORT_IN:.0f}mm PORT TIPS", offset=3.2, fs=5, color=C_DIM, font=FONT)
    draw_dim_h(ax, sx(LANE_IN), sx(CORR_PORT_IN), sz(_p1z - 45),
               f"{CORR_PORT_IN - LANE_IN:.1f}mm", offset=3.0, fs=4.4, color=C_DIM, above=False, font=FONT)
    draw_dim_v(ax, sx(PUMP_COL_C + PUMP_W / 2 + 15),
               sz(P05_Z), sz(P05_Z + PUMP_H),
               f"{PUMP_H:.0f}mm", offset=4.8, fs=5.5, color=C_DIM,
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
           sx(X_SHOW_L + 10), sz(P04_Z + PUMP_H / 2 + 120),
           f"Shurflo 2088-554-144\n12V · 3.5 GPM · 45 PSI\n1/2\"-14 NPSM ports,\n"
           f"{cwp.PUMP_YD_SPAN:.0f}mm across the tips",
           fs=5.5, color=C_PUMP_EC, font=FONT)
    leader(ax,
           sx(ACC_YD - ACC_OD / 2), sz(ACC_Z + ACC_LEN / 2),
           sx(ACC_YD - 200), sz(ACC_Z + ACC_LEN / 2 + 60),
           f"ACC-01: 0.75L ACCUM.\nØ{ACC_OD:.0f} × {ACC_LEN}mm",
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
        f"1. Panel: 18mm exterior ply spanning corridor Yd={PANEL_YD}-{PANEL_YD + PANEL_W} (270mm).",
        f"2. Panel face at X={PANEL_WALL_X}, equipment protrudes toward open end (-X direction).",
        f"3. Panel height: Z={PANEL_Z_AFF}-{PANEL_Z_AFF + PANEL_H}mm AFF ({PANEL_H}mm).",
        "4. SINGLE vertical pump column (bottom→top): ACC-01, P-01 (Blue supply),"
        " P-02 (Brown recycle), P-05 (Brown drain), P-03 (Waste drain).",
        "5. ACC-01: 0.75L bladder accumulator on the Blue supply, dead-leg below P-01.",
        "6. Each IN port (−Yd) takes a ½\" FNPT×slip adapter + elbow onto the near-board riser lane"
        f" (Yd{cwp.PORT_TURN_YD_IN:.0f}); each OUT (+Yd) onto the far-board lane (Yd{cwp.PORT_TURN_YD_OUT:.0f})."
        " Runs are drawn to their first leg along X: ⊙ = toward the walkway (−X), ⊗ = behind the panel (+X)."
        " The suction risers share the near lane at different X depths, so full routes are on Spine Views A/B.",
        "7. BV-01 (P-01 suction), BV-02 (P-05 suction), BV-03 (P-02 suction),"
        " BV-06 (P-03 suction) — manual ball valves.",
        "8. P-02 pulls IBC-3 (Brown buffer) and discharges to ACC-02 (recycle-spray damper"
        " on the pinhole-wall skid) → BV-05 → spray bar.",
        "9. The tray-drain skid (P-04 · SV-02 · DV-02) is on the PINHOLE WALL panel, not here.",
        f"10. Max protrusion: {max_depth}mm. The filter train + tray-drain skid are on the PINHOLE WALL panel.",
        "11. PIPE: 1/2\" PVC Sch-40 pump runs (solvent-weld) + threaded transitions at components; a braided flex"
        " jumper (gold; dashed where hidden behind the pump) on the first straight leg after each port turn."
        f" Pumps + ACC cam-clamp to a {cwp.EQT:.0f}mm ply shirt; 4-bolt brackets.",
        f"12. Pump-base Z (AFF): ACC-01 {cwp.ACC_Z0} · P-01 {cwp.PSTACK['P-01']} · P-02 {cwp.PSTACK['P-04']}"
        f" · P-05 {cwp.PSTACK['P-05']} · P-03 {cwp.PSTACK['P-03']}.",
    ]
    draw_notes(ax, notes, 575, 475, spacing=14,
               fs=6, wrap=80, width=425, color=C_DIM, title_color=C_NEW, font=FONT)

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
def _draw_pump(col_yd, pz, pname, pdesc, pfc, pec):
    """Upright pump as built in 3D (cwp.pump_unit): body + head, the IN/OUT ports as short side
    stubs reaching cwp.PORT_REACH from the axis (13.5mm off the Ø100 body)."""
    rect(col_yd - PUMP_W / 2, pz, PUMP_W, PUMP_BODY_H,
         C_PUMP_BODY, C_PUMP_EC, lw=1.2, zorder=6)
    rect(col_yd - PUMP_W / 2 - 3, pz + PUMP_BODY_H, PUMP_W + 6, cwp.PCAP_H,
         "#C9B8A6", C_PUMP_EC, lw=1.0, zorder=6)
    stub = cwp.PORT_REACH - cwp.PVB_R
    for y0 in (col_yd - cwp.PORT_REACH, col_yd + cwp.PVB_R):
        rect(y0, pz + PORT_ZOFF - PIPE_OD / 2, stub, PIPE_OD, C_PIPE_FILL, C_PIPE_EC, lw=0.5, zorder=7)
    ax.text(sx(col_yd), sz(pz + PUMP_BODY_H / 2 + 5),
            pname, ha="center", va="center",
            fontsize=8, color=pfc, fontweight="bold", zorder=8, **FONT)
    ax.text(sx(col_yd), sz(pz + PUMP_BODY_H / 2 - 30),
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
    PW_ZB, PW_ZT = PWP_PANEL_Z0 - 330, 2440   # view Z bounds (mm) — below the panel bottom for the corridor-drop callouts
    PW_OX, PW_OZ = 90, 200             # drawing-unit origin offsets
    PW_KX = 0.62                       # X mm→unit (board ~1720mm → ~1066 units)

    # MIRRORED X: +X (sealed end / corridor / DV-01) draws to the LEFT — this is
    # the view standing INSIDE the container looking at the pinhole wall, so the
    # filter train reads F-03→F-02→F-01 left-to-right and DV-01 exits off the left.
    def pwx(x_mm): return PW_OX + (PW_XR - x_mm) * PW_KX
    def pwz(z_mm): return PW_OZ + (z_mm - PW_ZB)

    fig, ax_p = plt.subplots(1, 1, figsize=(23, 13 * ((PW_ZT - PW_ZB) + 2 * PW_OZ) / 2020), dpi=DIAGRAM_DPI)   # height scales with the Z window (2020 = the original 820–2440 view) so the Z scale holds
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

    # ── Backing board (18mm exterior ply) — extents from PWP_PANEL_* ──────────
    BD_XL, BD_XR = PWP_PANEL_X0, PWP_PANEL_X1
    BD_ZB, BD_ZT = PWP_PANEL_Z0, PWP_PANEL_Z0 + PWP_PANEL_H
    (nbw, nbh), (ntw, nth) = PWP_PANEL_NOTCH_BR, PWP_PANEL_NOTCH_TR
    outline = [(BD_XL, BD_ZB), (BD_XR - nbw, BD_ZB), (BD_XR - nbw, BD_ZB + nbh), (BD_XR, BD_ZB + nbh),
               (BD_XR, BD_ZT - nth), (BD_XR - ntw, BD_ZT - nth), (BD_XR - ntw, BD_ZT), (BD_XL, BD_ZT)]
    ax_p.add_patch(mpatches.Polygon([(pwx(x), pwz(z)) for x, z in outline], closed=True, fc=C_PLY,
                                    ec=C_PLY_EC, lw=2.0, zorder=3, alpha=0.5))
    leader(ax_p, pwx(BD_XR - nbw / 2), pwz(BD_ZB + nbh / 2), pwx(BD_XR) - 60, pwz(BD_ZB + 330),
           f"{nbw}×{nbh}mm notch\n(rail end flange)", fs=5.5, color=C_PLY_EC, ha="right", va="center", font=FONT)
    leader(ax_p, pwx(BD_XR - ntw / 2), pwz(BD_ZT - nth / 2), pwx(BD_XR) - 60, pwz(BD_ZT - nth - 120),
           f"{ntw}×{nth}mm notch\n(rail saddle plate)", fs=5.5, color=C_PLY_EC, ha="right", va="center", font=FONT)
    pw_text(4470, 2255,
            f"{BD_XR - BD_XL} × {BD_ZT - BD_ZB}mm\n18mm EXTERIOR PLY\n(pinhole wall)",
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
    for x0 in (PWP_ACC2_X - cwp.ACC_R - ACC_PORT_L, PWP_ACC2_X + cwp.ACC_R):
        pw_rect(x0, PWP_ACC2_Z0 + 28 - cwp.RP, ACC_PORT_L, 2 * cwp.RP, C_PIPE_FILL, C_PIPE_EC, lw=0.5, zorder=7)
    pw_text(PWP_ACC2_X, PWP_ACC2_Z0 + 120, "ACC-02", ha="center", va="center", fontsize=7, color=C_BROWN_EC, fontweight="bold", zorder=8)
    pw_text(PWP_ACC2_X, PWP_ACC2_Z0 + 66, "RECYCLE\nSPRAY", ha="center", va="center", fontsize=5, color=C_BROWN_EC, zorder=8)
    leader(ax_p, pwx(PWP_ACC2_X), pwz(PWP_ACC2_Z0), pwx(PWP_ACC2_X) + 40, pwz(460),
           "ACC-02 pulsation damper\n(P-02 in corridor → ACC-02\n→ BV-05 spray selector)",
           fs=6, color=C_BROWN_EC, ha="left", va="center", font=FONT)

    # ════════════════════════════════════════════════════════════════
    #  FLOW — every pipe on the wall, projected from the live 3D build (water_3d) onto X×Z.
    #  Legs along Yd (off / onto the ply) collapse; a run is clipped where it leaves the wall
    #  zone into the corridor (Yd > WALL_YD) or the view's X window.
    # ════════════════════════════════════════════════════════════════
    W = water_3d()
    import generate_pinhole_water_panel as _pw
    WALL_YD = 200
    F1_CX, F2_CX, F3_CX = PWP_FILTER_X1, PWP_FILTER_X2, PWP_FILTER_X3
    drawn = []

    def wall_pieces(name):
        seq = W["runs"][name]
        ok = lambda q: q[1] <= WALL_YD and PW_XL <= q[0] <= PW_XR
        pcs, cur = [], []
        for a, b in zip(seq, seq[1:]):
            if ok(a) and not cur:
                cur.append(a)
            if ok(a) and ok(b):
                cur.append(b)
                continue
            if ok(a) != ok(b):
                inn, out = (a, b) if ok(a) else (b, a)
                edge = PW_XL if out[0] < PW_XL else (PW_XR if out[0] > PW_XR else None)
                c = inn
                if edge is not None and out[0] != inn[0]:
                    t = (edge - inn[0]) / (out[0] - inn[0])
                    c = tuple(inn[k] + t * (out[k] - inn[k]) for k in range(3))
                if ok(a):
                    cur.append(c); pcs.append(cur); cur = []
                else:
                    cur = [c, b]
        if cur:
            pcs.append(cur)
        res = []
        for pc in pcs:
            xs, zs = [], []
            for q in pc:
                if xs and abs(q[0] - xs[-1]) < 0.5 and abs(q[2] - zs[-1]) < 0.5:
                    continue
                xs.append(q[0]); zs.append(q[2])
            k = 1
            while k < len(xs) - 1:     # drop collinear waypoints (draw_pipe_path reads them as a U-turn)
                if abs((xs[k] - xs[k - 1]) * (zs[k + 1] - zs[k]) - (zs[k] - zs[k - 1]) * (xs[k + 1] - xs[k])) < 1e-6:
                    del xs[k], zs[k]
                else:
                    k += 1
            if len(xs) >= 2:
                res.append((xs, zs))
        return res

    def wall_run(name, fc, zorder):
        pcs = wall_pieces(name)
        for xs, zs in pcs:
            pw_pipe(xs, zs, fc, zorder=zorder)
            drawn.extend((xs[k], zs[k], xs[k + 1], zs[k + 1], zorder) for k in range(len(xs) - 1))
        return pcs

    for nm in ("Filter F1 in port", "Filter F1 out port", "Filter F2 in port", "Filter F2 out port",
               "Filter F3 in port", "Filter F3 out port", "F1 out -> F2 in", "F2 out -> F3 in"):
        wall_run(nm, C_BROWN, Z_BROWN)
    wall_run("F3 -> SV-01 (wall-mounted drop)", C_BROWN, Z_BROWN)
    sv = wall_run("SV-01 -> DV-01 (single filtered line)", C_BROWN, Z_BROWN + 3)
    ts = wall_run("Tray sump -> P-04 suction", C_BROWN, Z_BROWN + 3)
    wall_run("P-04 -> SV-02 -> DV-02", C_BROWN, Z_BROWN)
    wall_run("DV-02 feed -> F1 (recycle)", C_BROWN, Z_BROWN)
    dw = wall_run("DV-02 waste -> IBC-4", C_BLACK_SYS, Z_BLACK + 1)
    pa = wall_run("P-02 -> ACC-02 (recycle spray)", C_BROWN, Z_BROWN + 3)
    ab = wall_run("ACC-02 -> BV-05 (recycled spray)", C_BROWN, Z_BROWN)

    # projection crossings: the lower-zorder run gets a white break (skill_plumbing_drawing)
    gx = PIPE_OD / 2 + 8
    for h in drawn:
        if abs(h[1] - h[3]) > 0.5:
            continue
        for v in drawn:
            if abs(v[0] - v[2]) > 0.5 or v[4] == h[4]:
                continue
            x, z = v[0], h[1]
            if not (min(h[0], h[2]) + gx < x < max(h[0], h[2]) - gx and min(v[1], v[3]) + gx < z < max(v[1], v[3]) - gx):
                continue
            if h[4] < v[4]:
                pw_rect(x - gx, z - PIPE_OD / 2 - 2, 2 * gx, PIPE_OD + 4, "white", ec="none", lw=0, zorder=h[4] + 1.6)
            else:
                pw_rect(x - PIPE_OD / 2 - 2, z - gx, PIPE_OD + 4, 2 * gx, "white", ec="none", lw=0, zorder=v[4] + 1.6)

    # off-wall ends (where a run leaves into the corridor / past the view edge)
    def end_note(pcs, idx, txt, col, dx, dz, ha):
        xs, zs = pcs[0] if idx == 0 else pcs[-1]
        x, z = (xs[0], zs[0]) if idx == 0 else (xs[-1], zs[-1])
        leader(ax_p, pwx(x), pwz(z), pwx(x + dx), pwz(z + dz), txt, fs=5.8, color=col, ha=ha, va="center", font=FONT)
    end_note(ts, 0, "FROM TRAY SUMP\n(along the wall at Z230)", C_BROWN, -120, -60, "left")
    end_note(ab, -1, "→ BV-05 spray selector", C_BROWN, -110, 60, "left")
    end_note(sv, -1, "→ DV-01 (corridor mouth,\nunder-walkway ribbon)", C_BROWN, -260, -110, "left")
    end_note(dw, -1, "DV-02 waste → IBC-4\n(ribbon, CV-3 at the merge)", C_BLACK_SYS, -30, -215, "center")
    end_note(pa, 0, "FROM P-02 (corridor,\nunder-walkway ribbon)", C_BROWN, 230, -110, "right")

    # P-clips on the ply (3D, on 18mm offcut blocks — the low runs + the 3 corridor drops included)
    for nm, cx, cz, face_y, pipe_y, vert in W["clips"]:
        if face_y != _pw.SKID_FACE_YD or not (PW_XL <= cx <= PW_XR):
            continue
        w_, h_ = (16, 24) if vert else (24, 16)
        pw_rect(cx - w_ / 2, cz - h_ / 2, w_, h_, C_STEEL, ec=C_FRAME, lw=0.6, zorder=16)
    # P-04 discharge flex jumper (3D)
    for nm, wp in W["flex"]:
        a, b = wp[0], wp[-1]
        if a[1] <= WALL_YD and PW_XL <= a[0] <= PW_XR:
            ax_p.plot([pwx(a[0]), pwx(b[0])], [pwz(a[2]), pwz(b[2])], color="#E0A800", lw=6, alpha=0.8,
                      solid_capstyle="butt", zorder=15)

    # SV-01 (in-line pH sample tap on the filtered drop)
    SV01_X, SV01_Z = PWP_SV01_X, PWP_SV01_Z
    pw_valve(SV01_X, SV01_Z, "SV\n01", C_BROWN, half=20)
    leader(ax_p, pwx(SV01_X), pwz(SV01_Z) + 22, pwx(4450), pwz(1780),
           "SV-01 — pH sample tap\n(filtered line, before DV-01)",
           fs=6, color=C_BROWN, ha="left", va="bottom", font=FONT)
    HEAD_Z = (HEAD_ZB + HEAD_ZT) / 2
    F3_XR = PWP_FILTER_X3 + BB_OD // 2

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
    leader(ax_p, pwx(PWP_FILTER_X1), pwz(PWP_SROW_Z0 + 20), pwx(3420), pwz(700),
           "P-04 Shurflo 2088\n12V · 3.5 GPM · 45 PSI\n(tray-drain pump)",
           fs=6, color=C_PUMP_EC, ha="right", va="center", font=FONT)
    leader(ax_p, pwx(F2_CX), pwz(SUMP_ZB + 40), pwx(3500), pwz(1650),
           "Big Blue 4.5\"×20\" housing\n(Ø184 sump to Z1746, head Z2262–2340;\n"
           "F-01 5µm → F-02 KDF-55 → F-03 GAC)",
           fs=6, color=C_FILTER, ha="left", va="center", font=FONT)

    # ── NOTES ───────────────────────────────────────────────────────
    notes = [
        "PINHOLE WALL FILTER SKID — TRAY-DRAIN RECYCLE + FILTER TRAIN:",
        "1. Wide 18mm exterior-ply backing board on the pinhole wall (Yd≈0),"
        f" X={PWP_PANEL_X0}–{PWP_PANEL_X1}, Z={PWP_PANEL_Z0}–{PWP_PANEL_Z0 + PWP_PANEL_H}mm AFF (extended down so the low runs clip to the ply).",
        "2. Tray-drain skid row UNDER the filters: P-04 (tray-sump pump) →"
        " SV-02 (pH sample) → 3W-DV-02, on the row line Z≈1312.",
        "3. HORIZONTAL filter bank high on the wall: F-01 (5µm sediment) →"
        " F-02 (KDF-55) → F-03 (carbon/GAC); Big Blue 4.5\"×20\" housings.",
        "4. DV-02 recycle branch feeds F-01; its waste branch drops down the wall to the under-walkway"
        " ribbon → corridor → CV-3 → the IBC-4 merge tee.",
        "5. SV-01: pH sample tap on the filtered line, RAISED beside F-03"
        " (Z≈1610), before DV-01.",
        "6. 3W-DV-01 is at the corridor mouth (off this wall): the filtered line drops down the wall from SV-01"
        " to the under-walkway ribbon and splits there, pH-gated to recycle (IBC-3) or Waste (IBC-4).",
        "7. ACC-02 (recycle-spray damper, center-bottom) is fed from P-02 in the"
        " corridor and feeds BV-05 → the spray bar.",
        "8. Flow: sump → P-04 → SV-02 → DV-02 → F-01 → F-02 → F-03 → SV-01 → DV-01.",
        f"9. Filters at {PWP_FILTER_X2 - PWP_FILTER_X1}mm centers (X{PWP_FILTER_X1}/{PWP_FILTER_X2}/{PWP_FILTER_X3});"
        f" heads Z≈{(PWP_FILTER_HEAD_Z + PWP_FILTER_TOP_Z) / 2:.0f}, sump bottoms Z≈{PWP_FILTER_BOT_Z} AFF (4.5×20).",
        "10. PIPE: 1\" PVC Sch-40 (filter loop) / ½\" (recycle-spray); housings on their"
        " integral brackets through-bolted to the ply board. Routes are projected from the 3D; every pipe"
        f" clips to the ply on a {cwp.CLIP_SHIM:.0f}mm offcut block (grey), incl. the Z230 tray-suction run and"
        " the three corridor drops (SV-01→DV-01, DV-02 waste, P-02→ACC-02) on the extended board.",
    ]
    draw_notes(ax_p, notes, pwx(2600), pwz(1560), spacing=32,
               fs=6.5, wrap=95, width=720, color=C_DIM, title_color=C_NEW, font=FONT)

    # ── SYMBOL KEY (clear left margin strip, X4500–5060) ────────────
    draw_symbol_key(ax_p, 1600, pwz(2200), r=13, row=70, fs=6.5, w=375)

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
    axd = fig.add_axes([0.725, 0.60, 0.20, 0.30])
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
from tbs_constants import (C_LEN, C_HGT)

FB = {"fontfamily": "monospace"}
C_PLYB   = "#D9C9A3"   # plywood (tan)
C_BROWNB = C_PIPE_RECYCLE   # brown (used/recycled) drain
C_WASTEB = C_PIPE_WASTE     # waste drain (black)
C_BLUEB  = C_PIPE_FRESH     # blue fill
C_WALLB  = "#C8C8C8"

# ── Geometry (matches generate_corridor_water_panel.py: BACK_X=5104 rear panel) ──
PANX   = cwp.BACK_X                        # rear-panel front face (pumps hang -X off it)
PANX1  = cwp.BACK_X + cwp.EQT              # rear-panel rear face (18mm ply)
SHIRTX0, SHIRTX1 = cwp.SHIRT_X, cwp.SHIRT_X + cwp.EQT   # 18mm pump-mount shirt (in FRONT of the panel)
SHIRT_ZB, SHIRT_ZT = cwp.SHIRT_Z0, cwp.PANEL_TOP_Z      # shirt Z extent (bottom clears the raised P-05 elbow; top at the fan baffle)
SPX1   = cwp.SPINE_X_END                   # drain-riser spine rear
SPINE_ZB, SPINE_ZT = cwp.SPINE_Z0, cwp.TOP_Z - cwp.S    # spine Z extent
PAN_ZB, PAN_ZT = cwp.S, cwp.S + cwp.PH_CUT  # rear-panel BOARD Z extent (cut height PH_CUT=1845; the opening top is PANEL_TOP_Z 1900)
WALLX  = C_LEN                    # 5893 — sealed end wall
X1X    = cwp.X1_TEE_X                # X1 fill TEE X (on the spine face)
# End-wall port heights (3D drains_ports): X1 fill tee Z; X3 / X4 from the discharge runs' last points
X1_PORT_Z = cwp.X1_TEE_Z
# Pump / ACC stack on the shirt front (single column, projected along Yd)
PUMP_FRONT_X = cwp.PXC - cwp.PVB_R    # pump body front
PUMP_BACK_X  = cwp.PXC + cwp.PVB_R    # pump body back
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
    D0, D1, NOTE_MARGIN = 4200, 6760, 1120
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
           f"18mm REAR PANEL\n(edge-on)\nX={PANX:.0f}–{PANX1:.0f}\nZ={PAN_ZB:.0f}–{PAN_ZT:.0f}",
           color=C_OUT, fs=6, ha=_ha("left"), va="top", arrow_style="-|>", font=FB)

    # ── 18mm pump-mount shirt (in FRONT of the rear panel, −X) ───────────────
    _rect(SHIRTX0, SHIRT_ZB, SHIRTX1 - SHIRTX0, SHIRT_ZT - SHIRT_ZB,
          C_PLYB, lw=1.2, z0=6, alpha=0.85)
    leader(axb, (SHIRTX0 + SHIRTX1) / 2, 480, 4210, 600,
           f"{SHIRTX1 - SHIRTX0:.0f}mm PUMP-MOUNT SHIRT",   # dims + cam-clamp detail live in Note 1
           color="#7A6A40", fs=5.5, ha=_ha("left"), va="center", arrow_style="-|>", font=FB)
    # ~34mm chase gap (shirt back ≈5070 → panel front 5104) + 6 spacer blocks
    for bz in (320, 920, 1560):
        _rect(SHIRTX1, bz, PANX - SHIRTX1, 80, C_PLYB, ec=C_OUT, lw=0.6, z0=7)
    draw_dim_h(axb, SHIRTX1, PANX, 60, f"{PANX - SHIRTX1:.0f}mm\nchase", offset=4,
               fs=5, above=False, font=FB)
    axb.text(SHIRTX1 + (PANX - SHIRTX1) / 2 + 90, 1700,
             "6× SPACER\nBLOCKS", fontsize=4.6, ha="center", va="center",
             color="#7A6A40", zorder=10, **FB)

    # ── Pump + ACC stack on the shirt front (single column, projected along Yd) ──
    for zb, h, lbl, hot in [(cwp.ACC_Z0, 200, "ACC-01", True),
                            (cwp.PSTACK["P-01"], PUMP_H, "P-01", False),
                            (cwp.PSTACK["P-04"], PUMP_H, "P-02", True),
                            (cwp.PSTACK["P-05"], PUMP_H, "P-05", True),
                            (cwp.PSTACK["P-03"], PUMP_H, "P-03", False)]:
        _rect(PUMP_FRONT_X, zb, PUMP_BACK_X - PUMP_FRONT_X, h,
              "#E6D9F0" if hot else "#EAEAEA", ec=C_OUT, lw=0.9, z0=5)
        axb.text((PUMP_FRONT_X + PUMP_BACK_X) / 2, zb + h / 2, lbl, fontsize=6,
                 ha="center", va="center", color="#202020", fontweight="bold", zorder=15,
                 bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85), **FB)
    leader(axb, PUMP_FRONT_X, cwp.PSTACK["P-03"] + 90, 4570, 1980,
           "PUMP COLUMN + ACC-01\n(P-01/P-02/P-05/P-03 + ACC-01,\nsame stack as the front elevation)",
           color="#777", fs=5.3, ha=_ha("left"), va="center", arrow_style="-|>", font=FB)

    # ── Drain-riser spine (18mm ply fin, teed off the rear panel into the corridor) ──
    # The spine plane separates the two faces: VIEW A draws the −Yd intake runs,
    # VIEW B (mirror) draws the +Yd discharge runs.
    _rect(PANX, SPINE_ZB, SPX1 - PANX, SPINE_ZT - SPINE_ZB, C_PLYB, lw=1.2,
          z0=8, alpha=0.55)
    leader(axb, (PANX + SPX1) / 2, 1180, 6050, 1140,
           f"DRAIN-RISER SPINE\n18mm ply, teed perpendicular off the rear\n"
           f"panel (a T in plan) — X={PANX:.0f}–{SPX1:.0f}, Z={SPINE_ZB:.0f}–{SPINE_ZT:.0f};\n"
           "the drain risers P-clip to it on 18mm offcut blocks",
           color=C_OUT, fs=6, ha=_ha("left"), va="center", arrow_style="-|>", font=FB)

    # ── Pipe runs, projected from the live 3D build (water_3d) onto X×Z ──────
    # Legs along Yd collapse to a point; a run is clipped where it leaves the corridor
    # (into a tote, Yd outside YD_NEAR..YD_FAR) or −X of `xmin` (under the walkway).
    W = water_3d()

    def _pieces(name, xmin=4560.0):
        seq = W["runs"][name]
        out, cur = [], []
        inside = lambda q: q[0] >= xmin - 1e-6 and cwp.YD_NEAR - 1e-6 <= q[1] <= cwp.YD_FAR + 1e-6

        def cut(a, b):            # the point on a→b where it crosses back over the clip boundary
            if a[0] < xmin <= b[0] or b[0] < xmin <= a[0]:
                t = (xmin - a[0]) / (b[0] - a[0])
                return tuple(a[k] + t * (b[k] - a[k]) for k in range(3))
            return b if inside(b) else a
        for a, b in zip(seq, seq[1:]):
            ia, ib = inside(a), inside(b)
            if ia and not cur:
                cur.append(a)
            if ia and ib:
                cur.append(b)
            elif ia and not ib:
                cur.append(cut(a, b)); out.append(cur); cur = []
            elif ib and not ia:
                cur = [cut(a, b), b]
        if cur:
            out.append(cur)
        res = []
        for pc in out:
            xs, zs = [], []
            for q in pc:
                if xs and abs(q[0] - xs[-1]) < 0.5 and abs(q[2] - zs[-1]) < 0.5:
                    continue
                xs.append(q[0]); zs.append(q[2])
            k = 1
            while k < len(xs) - 1:     # drop collinear waypoints (draw_pipe_path reads them as a U-turn)
                if abs((xs[k] - xs[k - 1]) * (zs[k + 1] - zs[k]) - (zs[k] - zs[k - 1]) * (xs[k + 1] - xs[k])) < 1e-6:
                    del xs[k], zs[k]
                else:
                    k += 1
            if len(xs) >= 2:
                res.append((xs, zs))
        return res

    drawn = []                       # (x0, z0, x1, z1, zorder) of every straight leg drawn on this sheet

    def run3d(name, fc, zorder=11, xmin=4560.0, shift=None):
        """`shift` = {true X: drawn X} — a display-only offset for a leg that projects exactly onto
        another run (different Yd in 3D); every use is labelled on the sheet."""
        pcs = _pieces(name, xmin)
        if shift:
            pcs = [([shift.get(round(x), x) for x in xs], zs) for xs, zs in pcs]
        for xs, zs in pcs:
            _pipe(xs, zs, fc, zorder=zorder)
            drawn.extend((xs[k], zs[k], xs[k + 1], zs[k + 1], zorder) for k in range(len(xs) - 1))
        return pcs

    def gap_breaks():
        """Projection crossings (runs on different Yd that cross in this view): the lower-zorder
        run gets a white break so the upper one reads continuous (skill_plumbing_drawing)."""
        g = POD / 2 + 6
        for h in drawn:
            if abs(h[1] - h[3]) > 0.5:
                continue
            for v in drawn:
                if abs(v[0] - v[2]) > 0.5 or v[4] == h[4]:
                    continue
                x, z = v[0], h[1]
                if not (min(h[0], h[2]) + g < x < max(h[0], h[2]) - g and min(v[1], v[3]) + g < z < max(v[1], v[3]) - g):
                    continue
                lo = h if h[4] < v[4] else v
                if lo is h:
                    _rect(x - g, z - POD / 2 - 2, 2 * g, POD + 4, "white", ec="none", lw=0, z0=lo[4] + 1.6)
                else:
                    _rect(x - POD / 2 - 2, z - g, POD + 4, 2 * g, "white", ec="none", lw=0, z0=lo[4] + 1.6)

    def endon(x, z, col, toward=True, r=13):
        """A leg along Yd, end-on: ⊙ toward the viewer, ⊗ away."""
        axb.add_patch(mpatches.Circle((x, z), r, facecolor="white", edgecolor=col, lw=1.2, zorder=14))
        if toward:
            axb.add_patch(mpatches.Circle((x, z), 3, facecolor=col, edgecolor=col, zorder=15))
        else:
            for sgn in (1, -1):
                axb.plot([x - r * 0.6, x + r * 0.6], [z - sgn * r * 0.6, z + sgn * r * 0.6],
                         color=col, lw=0.9, zorder=15)

    def note(x, z, txt, col, ha="left", va="center", fs=4.2):
        axb.text(x, z, txt, fontsize=fs, ha=_ha(ha), va=va, color=col, zorder=15,
                 bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85), **FB)

    near = (lambda yd: yd < cwp.CTR_Y) if _NEAR == '-Yd' else (lambda yd: yd > cwp.CTR_Y)

    # ── Fitting landmarks (drawn in BOTH views) ──────────────────────────────
    X1Z = X1_PORT_Z
    run3d("X1 camlock -> one-way -> tee (straight)", C_BLUEB, zorder=11)
    cv1 = W["checks"]["CV-1"]
    valve_check(axb, cv1[0], cv1[2], 15, C_BLUEB, flow="left", zorder=18)
    axb.text(cv1[0], cv1[2] + 22, "CV-1", fontsize=4.2, ha="center", va="bottom", color=C_BLUEB, zorder=15, **FB)
    _rect(5836, X1Z - 16, 34, 32, "white", ec=C_BLUEB, lw=1.0, z0=14)      # 2" DC camlock (X1 fill)
    axb.text(5833, X1Z - 26, "X1 camlock\n(end wall)", fontsize=4.0, ha="center", va="top",
             color=C_BLUEB, zorder=15, **FB)
    # X1 fill TEE: run along Yd (IBC-1 −Yd · IBC-2 +Yd, both end-on here), branch +X to the camlock.
    endon(X1X, X1Z, C_BLUEB, toward=True, r=16)
    axb.text(X1X - 64, X1Z + 36, "X1 FILL TEE\n(X1 in → IBC-1 + IBC-2)", fontsize=5, ha="center",
             va="bottom", color=C_BLUEB, zorder=14, **FB)
    note(X1X, X1Z - 40, ("→ IBC-1 (−Yd, toward you)" if _NEAR == '-Yd' else "→ IBC-2 (+Yd, toward you)")
         + "\nflex jumper at the flange", C_BLUEB, ha="center", va="top", fs=4.0)
    # Blue EQUALIZATION tie IBC-1 ↔ IBC-2: 1" pipe straight across in Yd (end-on), a flex jumper at
    # each tote flange.
    beq = W["runs"]["Blue equalization (IBC-1 <-> IBC-2)"][0]
    axb.add_patch(mpatches.Circle((beq[0], beq[2]), 17, facecolor="white", edgecolor=C_BLUEB, lw=1.6, zorder=13))
    axb.add_patch(mpatches.Circle((beq[0], beq[2]), 12, facecolor="white", edgecolor=C_BLUEB, lw=0.9, zorder=14))
    axb.add_patch(mpatches.Circle((beq[0], beq[2]), 22, facecolor="none", edgecolor="#E0A800", lw=1.6,
                                  ls=(0, (2, 1.5)), zorder=14))
    note(beq[0], beq[2] - 30, "BLUE EQUALIZATION TIE\n1\" IBC-1 ↔ IBC-2 (end-on),\nflex jumper at each tote",
         C_BLUEB, ha="center", va="top", fs=4.4)
    # IBC-4 merge tee (run along X, branch z− from CV-2 / DV-01).
    mx, _, mz = cwp.MERGE4
    _rect(mx - 30, mz - 15, 60, 30, "white", ec=C_WASTEB, lw=1.4, z0=13)
    _rect(mx - 15, mz - 36, 30, 21, "white", ec=C_WASTEB, lw=1.4, z0=13)
    leader(axb, mx + 30, mz, 5620, 1110,
           "IBC-4 MERGE TEE\n(DV-01 + DV-02 waste,\none-way legs:\nCV-2 / CV-3)",
           color="#555", fs=5.5, ha=_ha("left"), va="center", arrow_style="-|>", font=FB)
    # DV-01 — pH-gated filtered-line diverter at the corridor mouth (input from SV-01 on the −X
    # port; recycle +X → IBC-3 on View B; waste −Yd → IBC-4 merge on View A).
    import generate_pinhole_water_panel as _pw
    DV01X, DV01Z = _pw.DV01_CX, _pw.DV01_CZ
    valve_3way(axb, DV01X, DV01Z, 16, "#8A6D08", ports=("left", "right", "up"), zorder=18)
    axb.text(DV01X, DV01Z + 26, "DV-01", fontsize=4.6, ha="center", va="bottom", color="#8A6D08", zorder=15, **FB)

    # ── P-clips on standoff blocks for this face's runs (3D) ─────────────────
    for nm, cx, cz, face_y, pipe_y, vert in W["clips"]:
        if cx < 4600 or not near(pipe_y):
            continue
        w_, h_ = (16, 22) if vert else (22, 16)
        _rect(cx - w_ / 2, cz - h_ / 2, w_, h_, C_STEEL, lw=0.6, z0=16)

    # ── Flex jumpers on this face (3D): gold band along X / Z, gold ring when end-on (along Yd) ──
    for nm, wp in W["flex"]:
        a, b = wp[0], wp[-1]
        on_b = "discharge" in nm or nm.startswith("DV-01 recycle")
        if a[0] < 4600 or on_b != (_NEAR == '+Yd') or "equalization" in nm or "X1 fill" in nm:
            continue
        if nm.startswith("Blue #1"):         # follows its riser's display offset (run3d shift, View A)
            a, b = (a[0] - 35, a[1], a[2]), (b[0] - 35, b[1], b[2])
        if abs(a[0] - b[0]) < 1 and abs(a[2] - b[2]) < 1:
            axb.add_patch(mpatches.Circle((a[0], a[2]), POD / 2 + 6, facecolor="none", edgecolor="#E0A800",
                                          lw=1.8, zorder=15))
        else:
            axb.plot([a[0], b[0]], [a[2], b[2]], color="#E0A800", lw=6, alpha=0.75,
                     solid_capstyle="butt", zorder=15)

    # ════════════════════════════════════════════════════════════════════════
    #  VIEW A ONLY — −Yd INTAKE face (suctions · waste · fills · merge)
    # ════════════════════════════════════════════════════════════════════════
    if _NEAR == '-Yd':
        GAPX = cwp.GAPX                          # tray↔IBC gap: where the under-walkway ribbon enters the corridor
        # filtered line (SV-01, pinhole skid) → under-walkway ribbon → rises at the mouth → DV-01 −X port
        run3d("SV-01 -> DV-01 (single filtered line)", "#8A8A8A", zorder=11, xmin=GAPX)
        note(GAPX - 10, cwp.RIBBON_Z + 40, "from SV-01 (filtered)\nunder-walkway ribbon", "#777", ha="right")
        # DV-01 WASTE → −Yd lane across the corridor at Z235 → up the merge riser (CV-2) into the tee
        run3d("DV-01 -> IBC-4 merge", C_WASTEB, zorder=8)
        # DV-02 WASTE (pinhole skid) → ribbon → corridor floor Z65 → hop to the rear-panel hole → up (CV-3)
        run3d("DV-02 waste -> IBC-4", C_WASTEB, zorder=14, xmin=GAPX + 1)
        note(GAPX + 20, 40, "from DV-02 (skid) waste,\nunder-walkway ribbon", C_WASTEB, va="top")
        for cv in ("CV-2", "CV-3"):
            c = W["checks"][cv]
            valve_check(axb, c[0], c[2], 14, C_WASTEB, flow="up", zorder=18)
            axb.text(c[0] + 20, c[2], cv, fontsize=4.6, ha=_ha("left"), va="center", color=C_WASTEB, zorder=15, **FB)
        # merge → IBC-4 entry (+X along the spine lane, then +Yd into the tote — end-on here)
        ent = run3d("IBC-4 (Waste) entry", C_WASTEB, zorder=11)
        ex, ez = ent[0][0][-1], ent[0][1][-1]
        endon(ex, ez, C_WASTEB, toward=False)
        note(ex + 20, ez + 20, "→ IBC-4 (+Yd, flex\njumper at the flange)", C_WASTEB, va="bottom", fs=4.4)
        # P-01 suction: IN → −X → up past BV-01 → +X behind the panel → up → −Yd into Blue #1 (IBC-1)
        bxt = W["runs"]["Blue #1 -> P-01 suction entry"][-1][0]
        p1 = run3d("Blue #1 -> P-01 suction entry", C_BLUEB, zorder=10, shift={round(bxt): bxt - 35})
        bx, bz = p1[-1][0][-1], p1[-1][1][-1]
        endon(bx, bz, C_BLUEB, toward=True)
        note(bx + 20, bz + 10, f"from Blue #1 (IBC-1) — behind-panel suction\nriser (true X{bxt:.0f}, drawn 35mm −X\nclear of the X4 riser)", C_BLUEB, va="bottom")
        # IBC-3 shared bottom tap (tee along X) → P-02 (−X) / P-05 (+X) suctions
        tx3, _, tz3 = cwp.BROWN_TAP
        run3d("IBC-3 (Brown) bottom tap (shared P-02/P-05)", C_BROWNB, zorder=10)
        _rect(tx3 - 30, tz3 - 15, 60, 30, "white", ec=C_BROWNB, lw=1.3, z0=13)
        run3d("IBC-3 tap -> P-02 suction", C_BROWNB, zorder=9)
        run3d("Brown tap -> P-05 inlet", C_BROWNB, zorder=12)
        leader(axb, tx3 - 30, tz3, 4740, 470, "IBC-3 (Brown) shared bottom tap\n→ P-02 (−X) · P-05 (+X, shirt riser)",
               color=C_BROWNB, fs=4.2, ha=_ha("right"), va="center", arrow_style="-|>", font=FB)
        # X4 waste pickup: IBC-4 bottom → up the spine → −X wrap → up past BV-06 → P-03 IN
        run3d("X4 Waste (P-03) pickup", C_WASTEB, zorder=14)
        note(cwp.SPINE_X_END - 380, 300, "from IBC-4 (bottom pickup)\n→ up the spine → BV-06 → P-03", C_WASTEB)
        # ACC-01 OUT → Blue supply trunk → −X to the ribbon slot → spray bar / TAP-01
        run3d("Blue supply trunk -> spray bar / TAP-01 (off-panel)", C_BLUEB, zorder=16, xmin=GAPX + 1)
        _flowhead(GAPX + 1, 200, "left", C_BLUEB)
        note(GAPX - 10, 250, "Blue supply → spray bar / TAP-01", C_BLUEB, ha="right")
        for bv, col in (("BV-01", C_BLUEB), ("BV-03", C_BROWNB), ("BV-02", C_BROWNB), ("BV-06", C_WASTEB)):
            c = W["checks"][bv]
            valve_ball(axb, c[0], c[2], 16, col, vert=True, zorder=18)
            if bv == "BV-01":               # BV-01 sits between the P-02 riser and the pump — label out on a leader
                leader(axb, c[0], c[2], 4620, c[2] + 90, bv, color=col, fs=4.6, ha=_ha("right"), va="center",
                       arrow_style="-|>", font=FB)
            else:
                axb.text(c[0] - 22, c[2], bv, fontsize=4.6, ha=_ha("right"), va="center", color=col, zorder=13, **FB)
        leader(axb, cwp.MERGE4[0], 700, 6050, 880,
               "FRONT of spine (−Yd face), P-clipped on blocks:\nX4 pickup riser (→ P-03), DV-01 waste\n(CV-2) + DV-02 waste (CV-3) merge risers",
               color="#555", fs=5.2, ha="left", va="top", arrow_style="-|>", font=FB)

    gap_breaks() if _NEAR == '-Yd' else None

    # ════════════════════════════════════════════════════════════════════════
    #  VIEW B ONLY — +Yd DISCHARGE face (pump discharges + the DV-01 recycle)
    # ════════════════════════════════════════════════════════════════════════
    if _NEAR == '+Yd':
        GAPX = cwp.GAPX
        run3d("P-05 -> X3 end-wall port", C_BROWNB, zorder=12)
        run3d("P-03 -> X4 end-wall port", C_WASTEB, zorder=14)
        run3d("P-01 -> ACC-01 (in)", C_BLUEB, zorder=9)
        # P-02 → down the far board → under-walkway ribbon → ACC-02 on the skid
        run3d("P-02 -> ACC-02 (recycle spray)", C_BROWNB, zorder=10, xmin=GAPX + 1)
        _flowhead(GAPX + 1, cwp.RIBBON_Z, "left", C_BROWNB)
        note(GAPX - 10, cwp.RIBBON_Z + 40, "→ ACC-02 (skid)\nunder-walkway ribbon", C_BROWNB, ha="right")
        # DV-01 RECYCLE → up the far board → −X → −Yd into IBC-3 (Brown buffer)
        rc = run3d("DV-01 recycle -> IBC-3 (buffer) entry", C_BROWNB, zorder=11)
        rx, rz = rc[0][0][-1], rc[0][1][-1]
        endon(rx, rz, C_BROWNB, toward=False)
        leader(axb, rx, rz, 5330, 960, "DV-01 RECYCLE → IBC-3 (Brown buffer)\n−Yd into the tote, flex jumper at the flange",
               color=C_BROWNB, fs=4.6, ha=_ha("left"), va="center", arrow_style="-|>", font=FB)
        leader(axb, 5640, 1700, 6120, 1820,
               "+Yd DISCHARGE face (near):\nX3 / X4 pump discharges → end-wall ports",
               color=C_BROWNB, fs=5.2, ha=_ha("left"), va="center", arrow_style="-|>", font=FB)

    gap_breaks() if _NEAR == '+Yd' else None

    # ── End-wall ports ───────────────────────────────────────────────────────
    X3_PORT_Z = W["runs"]["P-05 -> X3 end-wall port"][-1][2]
    X4_PORT_Z = W["runs"]["P-03 -> X4 end-wall port"][-1][2]
    for z, lab, col in [(X1_PORT_Z, "X1", C_BLUEB), (X3_PORT_Z, "X3", C_BROWNB),
                        (X4_PORT_Z, "X4", C_WASTEB)]:
        axb.add_patch(mpatches.Circle((WALLX, z), 22, facecolor="white",
                      edgecolor=col, lw=1.8, zorder=14))
        axb.text(WALLX, z, lab, fontsize=6, ha="center", va="center",
                 fontweight="bold", color=col, zorder=15, **FB)

    # ── Dimensions ───────────────────────────────────────────────────────────
    draw_dim_h(axb, PANX, SPX1, 150, f"{SPX1 - PANX:.0f}mm spine depth", offset=4,
               fs=5.5, above=False, font=FB)

    # ── Notes (right margin) ─────────────────────────────────────────────────
    if _NEAR == '-Yd':
        cross_note = ("Pump discharges, the DV-01 recycle + the IBC-2 fill are on Spine View B "
                      "(+Yd face).")
    else:
        cross_note = ("Suctions, waste legs, fills + merge are on Spine View A "
                      "(−Yd face).")
    cv_dz = cwp.MERGE_CV_DZ
    draw_notes(axb, [
        "CORRIDOR PLUMBING PANEL — SPINE SIDE SECTION (looking along Yd):",
        cross_note,
        f"1. Pumps + ACC-01 mount on the FRONT (−X) of the rear panel, cam-clamped to a {SHIRTX1 - SHIRTX0:.0f}mm pump-mount shirt that backs the bodies (X={SHIRTX0:.0f}–{SHIRTX1:.0f}, Z={SHIRT_ZB:.0f}–{SHIRT_ZT:.0f}).",
        f"2. A ~{PANX - SHIRTX1:.0f}mm chase gap separates the shirt back (X={SHIRTX1:.0f}) and the rear-panel front (X={PANX:.0f}); six ply spacer blocks bridge it.",
        f"3. Rear panel: 18mm ply, X={PANX:.0f}–{PANX1:.0f}, Z={PAN_ZB:.0f}–{PAN_ZT:.0f}. The drain-riser spine is an 18mm ply fin teed perpendicular off it into the rear corridor (X={PANX:.0f}–{SPX1:.0f}, Z={SPINE_ZB:.0f}–{SPINE_ZT:.0f}).",
        "4. View A (−Yd intake face): the four pump suctions (BV-01/03/02/06), the X4 pickup riser up the spine, DV-01 + DV-02 waste → IBC-4 merge, the IBC-1 fill and the Blue supply trunk.",
        f"5. View B (+Yd discharge face): P-05 → X3 (Z={X3_PORT_Z:.0f}) and P-03 → X4 (Z={X4_PORT_Z:.0f}) along the spine to the end-wall ports, P-01 → ACC-01, P-02 → ACC-02 (skid), and the DV-01 recycle → IBC-3 (Brown buffer).",
        f"6. IBC-4 merge tee on the spine: DV-01 waste rises into its branch through CV-2, DV-02 waste (from the skid, under the walkway) joins its run through CV-3 — each check {cv_dz:.0f}mm below the tee, so one leg can't back-feed the other.",
        "7. Circuit C1 (15A, pole 1 of the 2-pole EP master pump switch) feeds the four corridor pumps from the rear-panel distribution block; they run one at a time by valve selection. The tray-drain P-04 (pinhole skid) is on its own fuse, C2 (pole 2).",
        f"8. Spine riser X-lanes (3D): X4 pickup {W['runs']['X4 Waste (P-03) pickup'][0][0]:.0f}, DV-02 waste / CV-3 {W['checks']['CV-3'][0]:.0f}, DV-01 waste / CV-2 + merge {cwp.MERGE4[0]:.0f}, X1 tee {X1X:.0f}. End-wall ports: X1 fill Z{X1_PORT_Z:.0f}, X3 Z{X3_PORT_Z:.0f}, X4 Z{X4_PORT_Z:.0f}.",
        "9. X1 fill is a TEE (X1 in → IBC-1 + IBC-2) with the CV-1 one-way valve + 2\" DC camlock at the end wall. The 1\" Blue equalization tie runs straight across IBC-1 ↔ IBC-2 with a flex jumper at each tote.",
        f"10. PIPE: 1\" PVC Sch-40 (IBC fill/drain + recycle) and 1/2\" PVC (pump runs), threaded at components. Risers P-clip to the spine on {cwp.CLIP_SHIM:.0f}mm ply-offcut blocks (pipe {cwp.CLIP_SHIM:.0f}mm off the face). ⊙ = a leg along Yd toward you, ⊗ = away; gold = braided flex jumper.",
    ], mxa(6800), 2440, spacing=34, fs=9.3, ha="left", width=950, wrap=45, font=FB)

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
