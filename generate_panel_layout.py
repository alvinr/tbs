#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_panel_layout.py — Equipment panel layout in IBC corridor.

Front elevation of an 18mm plywood panel spanning the 270mm IBC plumbing
corridor (Yd=1046–1316), perpendicular to the sealed end wall at X=5000.
Equipment mounts on the panel face, protruding toward the open end (-X).

Left column (near wall, 127mm): 3× pumps + ACC-01.
Right column (far wall, 130mm): 3× filter housings stacked vertically.

Plus a cross-section strip showing panel/walkway/wall relationship.

Output: diagrams/panel-layout.png
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math
import matplotlib.patches as mpatches

from tbs_constants import C_OUT, C_DIM, C_CL, C_STEEL, DIAGRAMS_DIR, PUMP_PIPE_OD, PUMP_PIPE_WALL
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_notes, hatch_rect
from tbs_title_block import title_block

# ── Panel geometry ────────────────────────────────────────────────────────
PANEL_T      = 18    # plywood thickness (mm)
PANEL_YD     = 1046  # panel near edge Yd (mm from pinhole wall)
PANEL_WALL_X = 5000  # panel face X position (matches EQPANEL_X)
WALKWAY_W    = 300   # standard walkway width (mm)
WALKWAY_Z    = 100   # walkway grating top (mm AFF)

# Panel face dimensions (new orientation: spans corridor)
PANEL_W  = 270   # face width (mm, Yd span: 1046–1316)
PANEL_H  = 2060  # face height (mm, Z span: 200–2260)
PANEL_Z_AFF = 200  # panel bottom Z above finished floor

# ── Shurflo 2088 pump dimensions ─────────────────────────────────────────
PUMP_W   = 127   # front face width (mm)
PUMP_H   = 218   # front face height (mm) — body length, vertical mount
PUMP_D   = 100   # depth from panel (mm)
PUMP_GAP = 40    # vertical gap between pumps (mm)
PORT_HALF = 30   # half of port-to-port spacing (mm)

# ── Accumulator ───────────────────────────────────────────────────────────
ACC_OD  = 127    # body OD (mm)
ACC_LEN = 150    # body length (mm) — vertical mount, port at bottom

# ── Filter housing (separate, 4.5"×10") ──────────────────────────────────
FILT_OD  = 130   # housing OD (mm)
FILT_H   = 340   # total height (mm) — head + sump, hung vertically
FILT_GAP = 30    # gap between housings (mm)
FILT_HEAD = 70   # head section height (mm)

# ── Layout on panel face (panel-relative coordinates) ────────────────────
# Horizontal axis = Yd from left edge (0=near wall, 270=far wall)
# Vertical axis = Z from panel bottom (0=bottom, 2060=top)
# Filters at BOTTOM, pumps at TOP.  F-01 at top of filter stack for gravity flow.

# Right column: 3 filter housings stacked vertically (sump-down) — BOTTOM
# F-01 (coarsest) at top, F-03 (finest) at bottom: gravity-assisted series flow
FILT_COL = 175                        # filter column center (Yd from left edge)

F01_Z = 2 * (FILT_H + FILT_GAP)      # = 740 (top — P-02 feeds here first)
F02_Z = FILT_H + FILT_GAP            # = 370 (middle)
F03_Z = 0                             # = 0   (bottom — filtered exit)
FILT_STACK_TOP = F01_Z + FILT_H       # = 1080

# Left column: 3 pumps stacked vertically + ACC-01 above — TOP
PUMP_COL = PUMP_W // 2               # = 63mm from left edge (127mm zone center)
PORT_IN_YD  = PUMP_COL + PORT_HALF   # right — inlet (suction)
PORT_OUT_YD = PUMP_COL - PORT_HALF   # left — outlet (discharge)
PUMP_ZONE_BOT = FILT_STACK_TOP + 40  # = 1120 (40mm gap above filter stack)

P01_Z = PUMP_ZONE_BOT                 # = 1120
P02_Z = P01_Z + PUMP_H + PUMP_GAP    # = 1378
P04_Z = P02_Z + PUMP_H + PUMP_GAP    # = 1636

ACC_YD = PUMP_COL
ACC_Z  = P04_Z + PUMP_H + PUMP_GAP   # = 1894 (bottom of body / port)

# P-03 (waste evacuation) — right column, above filter stack
P03_COL = FILT_COL                    # 175 — right column center
P03_Z   = PUMP_ZONE_BOT              # 1120 — matches pump zone baseline

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

# ── Scale and layout ─────────────────────────────────────────────────────
SC  = 120.0   # mm per inch (main elevation, 1:120)
FW  = 10.0
FH  = 22.5

# Show range (panel-relative mm + margins for dims/leaders)
X_SHOW_L = -130
X_SHOW_R = 400
Z_SHOW_L = -100
Z_SHOW_R = 2160

OX = 1.3
OZ = 3.5    # leave room for cross-section strip below


def sx(x_mm):
    """Panel-relative Yd (mm) → figure x (inches)."""
    return OX + (x_mm - X_SHOW_L) / SC


def sz(z_mm):
    """Panel-relative Z (mm) → figure y (inches)."""
    return OZ + (z_mm - Z_SHOW_L) / SC


# ── Figure setup ─────────────────────────────────────────────────────────
fig, ax = plt.subplots(1, 1, figsize=(FW, FH), dpi=150)
ax.set_xlim(0, FW)
ax.set_ylim(0, FH)
ax.set_aspect("equal")
ax.axis("off")

FONT = {"fontfamily": "monospace"}


def rect(x, z, w, h, fc, ec=C_FRAME, lw=1.0, zorder=5, alpha=1.0):
    """Rectangle in panel coords."""
    ax.add_patch(mpatches.Rectangle(
        (sx(x), sz(z)), w / SC, h / SC,
        fc=fc, ec=ec, lw=lw, zorder=zorder, alpha=alpha))


def circ(x_c, z_c, r, fc, ec=C_FRAME, lw=1.0, zorder=5, alpha=1.0):
    """Circle in panel coords."""
    ax.add_patch(plt.Circle(
        (sx(x_c), sz(z_c)), r / SC,
        fc=fc, ec=ec, lw=lw, zorder=zorder, alpha=alpha))


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN ELEVATION — PANEL FACE
#  Looking at panel from open end (viewer facing +X toward sealed wall).
#  LEFT = near wall (Yd=1046), RIGHT = far wall (Yd=1316).
# ═══════════════════════════════════════════════════════════════════════════

# Title above panel
ax.text(sx(PANEL_W / 2), sz(Z_SHOW_R) + 0.15,
        "FRONT ELEVATION — EQUIPMENT PANEL",
        ha="center", va="bottom",
        fontsize=6, color=C_DIM, fontweight="bold", zorder=10, **FONT)

# 1. Panel outline (18mm plywood)
rect(0, 0, PANEL_W, PANEL_H,
     C_PLY, C_PLY_EC, lw=2.0, zorder=3, alpha=0.5)

# Panel label (near top)
ax.text(sx(PANEL_W / 2), sz(PANEL_H - 30),
        f"18mm MARINE PLY\n{PANEL_W}mm × {PANEL_H}mm",
        ha="center", va="top",
        fontsize=4, color=C_PLY_EC, zorder=4, **FONT)

# Zone separator (dashed line between pump and filter columns)
zone_yd = PUMP_W + 6   # 133mm — midway in 13mm gap
ax.plot([sx(zone_yd), sx(zone_yd)], [sz(-10), sz(PANEL_H + 10)],
        color=C_PLY_EC, lw=0.5, ls=(0, (4, 4)), zorder=3, alpha=0.5)


# ═══════════════════════════════════════════════════════════════════════════
#  2. PUMPS — 3× stacked vertically (left column, Yd=0–127)
# ═══════════════════════════════════════════════════════════════════════════
pump_specs = [
    ("P-01", "BLUE\nSUPPLY",    P01_Z, C_BLUE,     C_BLUE_EC),
    ("P-02", "BROWN\nRECYCLE",  P02_Z, C_BROWN,    C_BROWN_EC),
    ("P-04", "TRAY\nDRAIN",     P04_Z, C_BLACK_SYS, C_BLACK_EC),
]

for pname, pdesc, pz, pfc, pec in pump_specs:
    # Mounting bracket
    rect(PUMP_COL - PUMP_W / 2 - 10, pz - 8,
         PUMP_W + 20, 8,
         C_FRAME_FILL, C_FRAME, lw=0.5, zorder=4)
    # Pump body
    rect(PUMP_COL - PUMP_W / 2, pz, PUMP_W, PUMP_H,
         C_PUMP_BODY, C_PUMP_EC, lw=1.2, zorder=6)
    # Port indicators (side by side at head — outlet LEFT, inlet RIGHT)
    for port_yd in [PORT_OUT_YD, PORT_IN_YD]:
        circ(port_yd, pz + PUMP_H - 25, 10,
             C_PIPE_FILL, C_PIPE_EC, lw=0.5, zorder=7)
    # Label
    ax.text(sx(PUMP_COL), sz(pz + PUMP_H / 2 + 15),
            pname, ha="center", va="center",
            fontsize=6, color=pfc, fontweight="bold", zorder=8, **FONT)
    ax.text(sx(PUMP_COL), sz(pz + PUMP_H / 2 - 20),
            pdesc, ha="center", va="center",
            fontsize=3.5, color=pec, zorder=8, **FONT)

# P-03 — right column, above filter stack
rect(P03_COL - PUMP_W / 2, P03_Z, PUMP_W, PUMP_H,
     C_PUMP_BODY, C_PUMP_EC, lw=1.2, zorder=6)
rect(P03_COL - PUMP_W / 2 - 10, P03_Z - 8,
     PUMP_W + 20, 8,
     C_FRAME_FILL, C_FRAME, lw=0.5, zorder=4)
for _p03_port_yd in [P03_COL - PORT_HALF, P03_COL + PORT_HALF]:
    circ(_p03_port_yd, P03_Z + PUMP_H - 25, 10,
         C_PIPE_FILL, C_PIPE_EC, lw=0.5, zorder=7)
ax.text(sx(P03_COL), sz(P03_Z + PUMP_H / 2 + 15),
        "P-03", ha="center", va="center",
        fontsize=6, color=C_BLACK_SYS, fontweight="bold", zorder=8, **FONT)
ax.text(sx(P03_COL), sz(P03_Z + PUMP_H / 2 - 20),
        "WASTE\nEVAC", ha="center", va="center",
        fontsize=3.5, color=C_BLACK_EC, zorder=8, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  3. ACC-01 — above pump stack (profile view, vertical, port at bottom)
#     Dead-end branch off main discharge pipe via tee — NOT inline
# ═══════════════════════════════════════════════════════════════════════════
ACC_STUB = 25   # gap between main pipe and ACC body for tee stub
ACC_BODY_Z = ACC_Z + ACC_STUB
rect(ACC_YD - ACC_OD / 2, ACC_BODY_Z, ACC_OD, ACC_LEN,
     C_ACC, C_BLUE_EC, lw=1.2, zorder=6, alpha=0.7)
ax.text(sx(ACC_YD), sz(ACC_BODY_Z + ACC_LEN / 2 + 10),
        "ACC-01", ha="center", va="center",
        fontsize=5, color="white", fontweight="bold", zorder=8, **FONT)
ax.text(sx(ACC_YD), sz(ACC_BODY_Z + ACC_LEN / 2 - 15),
        f"O/{ACC_OD}", ha="center", va="center",
        fontsize=3.5, color="white", zorder=8, **FONT)
# Port at bottom of ACC body (tee stub pipe drawn with Blue system pipes below)
circ(ACC_YD, ACC_BODY_Z, 10,
     C_PIPE_FILL, C_PIPE_EC, lw=0.5, zorder=10)

# Mounting clamp (U-bracket at top)
clamp_w = ACC_OD + 20
rect(ACC_YD - clamp_w / 2, ACC_BODY_Z + ACC_LEN,
     clamp_w, 8,
     C_FRAME_FILL, C_FRAME, lw=0.5, zorder=5)


# ═══════════════════════════════════════════════════════════════════════════
#  4. FILTER HOUSINGS — 3× separate, stacked vertically (sump down)
#     Right column (Yd=110–240), 130mm OD × 340mm tall
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
            fontsize=5.5, color="white", fontweight="bold", zorder=8, **FONT)
    ax.text(sx(FILT_COL), sz(fz + FILT_H / 2 - 15),
            fdesc, ha="center", va="center",
            fontsize=3, color="white", zorder=8, **FONT)
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
        fontsize=4.5, color=C_FILTER, fontweight="bold", zorder=10, **FONT)
ax.text(sx(FILT_COL), sz(F03_Z - 45),
        "SUMP DOWN", ha="center", va="top",
        fontsize=3.5, color=C_FILTER, zorder=10, **FONT)

# Pump zone (top)
ax.text(sx(PUMP_COL), sz(P01_Z - 30),
        "PUMP MANIFOLD", ha="center", va="top",
        fontsize=4.5, color=C_PUMP_EC, fontweight="bold", zorder=10, **FONT)


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

P01_PORT_Z = P01_Z + PUMP_H - 25
P02_PORT_Z = P02_Z + PUMP_H - 25
P04_PORT_Z = P04_Z + PUMP_H - 25
P03_PORT_Z = P03_Z + PUMP_H - 25
P03_PORT_IN  = P03_COL + PORT_HALF   # 205 — right (inlet/suction)
P03_PORT_OUT = P03_COL - PORT_HALF   # 145 — left (outlet/discharge)

# ── Filter head Z positions ──
F01_HEAD_Z = F01_Z + FILT_H - FILT_HEAD / 2   # top filter head
F02_HEAD_Z = F02_Z + FILT_H - FILT_HEAD / 2   # middle filter head
F03_HEAD_Z = F03_Z + FILT_H - FILT_HEAD / 2   # bottom filter head

# Filter port Yd positions (IN=left/near, OUT=right/far)
F_IN_YD  = FILT_COL - 35
F_OUT_YD = FILT_COL + 35

# ── Routing rails ──
DISCH_RAIL = 260    # Blue discharge riser (right side of panel)
INTERZONE  = F_IN_YD                         # pump-to-filter transition
JMPR_RAIL1 = FILT_COL + FILT_OD // 2 + 10   # 10mm outside housing
JMPR_RAIL2 = JMPR_RAIL1 + 15                # 15mm further out

# ── Entry/exit positions ──
EXIT_L = -60    # past left panel edge (near wall / walkway)
EXIT_R = 330    # past right panel edge (far wall / IBCs)

# ── Valve positions ──
BV01_YD = 0
BV01_Z  = P01_PORT_Z + SUCT_RISE
BV02_YD = -40
BV02_Z  = ACC_Z   # on horizontal at ACC port Z
DV02_YD = PORT_IN_YD + 30
DV02_Z  = P04_PORT_Z - PORT_DROP

# ── Flow arrow style ──
_AW = 25
_arrow_kw = dict(arrowstyle="-|>", lw=1.5, mutation_scale=8)


def draw_pipe_path(ax, x_pts, z_pts, od_mm, wall_mm,
                   fc, ec=C_FRAME, bore_fc="white",
                   elbow_r=None, zorder=8):
    """Parallel-wall pipe run with concentric-arc elbows."""
    n = len(x_pts)
    if n < 2:
        return
    half_od = od_mm / 2.0
    half_id = half_od - wall_mm
    if elbow_r is None:
        elbow_r = od_mm * 1.0

    segs = []
    for i in range(n - 1):
        dx = x_pts[i + 1] - x_pts[i]
        dz = z_pts[i + 1] - z_pts[i]
        length = max(math.hypot(dx, dz), 1e-6)
        segs.append((dx / length, dz / length, length))

    elbows = []
    for i in range(1, n - 1):
        d1x, d1z, _ = segs[i - 1]
        d2x, d2z, _ = segs[i]
        cos_a = max(-1.0, min(1.0, d1x * d2x + d1z * d2z))
        alpha_a = math.acos(cos_a)
        turn = math.pi - alpha_a
        if turn < 0.01:
            elbows.append(None)
            continue
        tangent = elbow_r * math.tan(turn / 2)
        max_t = 0.4 * min(segs[i - 1][2], segs[i][2])
        if tangent > max_t:
            tangent = max_t
        cross = d1x * d2z - d1z * d2x
        if cross > 0:
            nx, nz = -d1z, d1x
        else:
            nx, nz = d1z, -d1x
        tp_x = x_pts[i] - d1x * tangent
        tp_z = z_pts[i] - d1z * tangent
        r_eff = tangent / math.tan(turn / 2) if turn > 0.01 else elbow_r
        cy = tp_x + nx * r_eff
        cz_e = tp_z + nz * r_eff
        start_a = math.atan2(tp_z - cz_e, tp_x - cy)
        sweep = turn if cross > 0 else -turn
        elbows.append({
            'tangent': tangent, 'r': r_eff,
            'center': (cy, cz_e), 'start': start_a, 'sweep': sweep,
        })

    def _rect(sx0, sz0, sx1, sz1, nx, nz, half_r, color, z_ord):
        pts = [(sx(sx0 + nx * half_r), sz(sz0 + nz * half_r)),
               (sx(sx1 + nx * half_r), sz(sz1 + nz * half_r)),
               (sx(sx1 - nx * half_r), sz(sz1 - nz * half_r)),
               (sx(sx0 - nx * half_r), sz(sz0 - nz * half_r))]
        ax.fill([p[0] for p in pts], [p[1] for p in pts],
                fc=color, ec=ec if color != bore_fc else "none",
                lw=0.8 if color != bore_fc else 0, zorder=z_ord)

    for i in range(len(segs)):
        dx, dz, seg_len = segs[i]
        nx, nz = -dz, dx
        trim_s = elbows[i - 1]['tangent'] if (i > 0 and elbows[i - 1]) else 0
        trim_e = elbows[i]['tangent'] if (i < len(elbows) and elbows[i]) else 0
        p0x = x_pts[i] + dx * trim_s
        p0z = z_pts[i] + dz * trim_s
        p1x = x_pts[i + 1] - dx * trim_e
        p1z = z_pts[i + 1] - dz * trim_e
        remaining = seg_len - trim_s - trim_e
        if remaining < 0.5:
            continue
        _rect(p0x, p0z, p1x, p1z, nx, nz, half_od, fc, zorder)
        _rect(p0x, p0z, p1x, p1z, nx, nz, half_id, bore_fc, zorder + 1)

    for elb in elbows:
        if elb is None:
            continue
        cy, cz_e = elb['center']
        r_eff = elb['r']
        sa = elb['start']
        sw = elb['sweep']
        n_arc = max(20, int(abs(sw) / 0.04))
        angles = [sa + sw * t / n_arc for t in range(n_arc + 1)]

        def _arc_ring(r_out, r_in, color, z_ord,
                      _cy=cy, _cz=cz_e, _angles=angles):
            ox_ = [sx(_cy + r_out * math.cos(a)) for a in _angles]
            oz_ = [sz(_cz + r_out * math.sin(a)) for a in _angles]
            ix_ = [sx(_cy + r_in * math.cos(a)) for a in _angles]
            iz_ = [sz(_cz + r_in * math.sin(a)) for a in _angles]
            ax.fill(ox_ + ix_[::-1], oz_ + iz_[::-1],
                    fc=color, ec=ec if color != bore_fc else "none",
                    lw=0.8 if color != bore_fc else 0, zorder=z_ord)

        _arc_ring(r_eff + half_od, max(r_eff - half_od, 0.5), fc, zorder)
        _arc_ring(r_eff + half_id, max(r_eff - half_id, 0.5),
                  bore_fc, zorder + 1)


def draw_ball_valve(x, z, label, color):
    """Diamond valve symbol at (x, z) in panel mm coords."""
    pts_x = [sx(x), sx(x + BV_R), sx(x), sx(x - BV_R)]
    pts_z = [sz(z + BV_R), sz(z), sz(z - BV_R), sz(z)]
    ax.add_patch(plt.Polygon(list(zip(pts_x, pts_z)),
                             fc="white", ec=color, lw=1.5, zorder=12))
    ax.text(sx(x), sz(z), label, ha="center", va="center",
            fontsize=3, color=color, fontweight="bold", zorder=13, **FONT)


# ════════════════════════════════════════════════════════════════
#  BLUE SYSTEM (C_BLUE)
# ════════════════════════════════════════════════════════════════

# Blue suction: IBC-1/2 (LEFT) → BV-01 → 90° elbow → P-01 inlet (RIGHT port)
# Raised above port Z to clear outlet; discharge riser draws over via Z_DISCH
_P01_SUCT_Z = P01_PORT_Z + SUCT_RISE
draw_pipe_path(ax,
    [EXIT_L, PORT_IN_YD, PORT_IN_YD],
    [_P01_SUCT_Z, _P01_SUCT_Z, P01_PORT_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLUE, zorder=Z_BLUE)
draw_ball_valve(BV01_YD, BV01_Z, "BV\n01", C_BLUE)
ax.annotate("", xy=(sx(EXIT_L + _AW), sz(_P01_SUCT_Z)),
            xytext=(sx(EXIT_L), sz(_P01_SUCT_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BLUE), zorder=11)
ax.text(sx(EXIT_L - 5), sz(_P01_SUCT_Z),
        "FROM\nIBC-1/2\n(BLUE)", ha="right", va="center",
        fontsize=4, color=C_BLUE, zorder=10, **FONT)

# Blue discharge: full path as single draw_pipe_path for proper elbows
# P-01 outlet → drop → right to riser → up to ACC_Z → left to spray bar
# Z_DISCH so riser draws OVER crossing suction pipes
draw_pipe_path(ax,
    [EXIT_L, DISCH_RAIL, DISCH_RAIL, PORT_OUT_YD, PORT_OUT_YD],
    [ACC_Z, ACC_Z, P01_PORT_Z - PORT_DROP, P01_PORT_Z - PORT_DROP, P01_PORT_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLUE, zorder=Z_DISCH)
# ACC-01 tee stub: branch up from main pipe to accumulator body
draw_pipe_path(ax,
    [ACC_YD, ACC_YD],
    [ACC_Z, ACC_BODY_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLUE, zorder=Z_DISCH)
draw_ball_valve(BV02_YD, BV02_Z, "BV\n02", C_BLUE)
ax.annotate("", xy=(sx(EXIT_L), sz(ACC_Z)),
            xytext=(sx(EXIT_L + _AW), sz(ACC_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BLUE), zorder=11)
ax.text(sx(EXIT_L - 5), sz(ACC_Z),
        "TO\nSPRAY\nBAR", ha="right", va="center",
        fontsize=4, color=C_BLUE, zorder=10, **FONT)


# ════════════════════════════════════════════════════════════════
#  BROWN SYSTEM (C_BROWN)
# ════════════════════════════════════════════════════════════════

# Brown suction: IBC-3 (far column, RIGHT) → P-02 inlet (RIGHT port)
draw_pipe_path(ax,
    [EXIT_R, PORT_IN_YD],
    [P02_PORT_Z, P02_PORT_Z],
    PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
ax.annotate("", xy=(sx(EXIT_R - _AW), sz(P02_PORT_Z)),
            xytext=(sx(EXIT_R), sz(P02_PORT_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BROWN), zorder=11)
ax.text(sx(EXIT_R + 5), sz(P02_PORT_Z),
        "FROM\nIBC-3\n(BROWN)", ha="left", va="center",
        fontsize=4, color=C_BROWN, zorder=10, **FONT)

# Brown discharge: P-02 outlet (LEFT port) → drop → right to F_IN_YD → down to F-01
draw_pipe_path(ax,
    [PORT_OUT_YD, PORT_OUT_YD, F_IN_YD, F_IN_YD],
    [P02_PORT_Z, P02_PORT_Z - PORT_DROP, P02_PORT_Z - PORT_DROP, F01_HEAD_Z],
    PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)

# Filter jumpers — gravity-fed downward: F-01 → F-02 → F-03
# Arrival horizontals offset 20mm above head Z to avoid merging with
# the departure pipe at the same filter head.
_JMPR_DROP = 20

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
        fontsize=4, color=C_BROWN, zorder=10, **FONT)


# ════════════════════════════════════════════════════════════════
#  TRAY DRAIN / BLACK SYSTEM (C_BLACK_SYS)
# ════════════════════════════════════════════════════════════════

# Tray drain suction: LEFT → P-04 inlet (RIGHT port)
# Raised above port Z to clear outlet; discharge riser draws over via Z_DISCH
_P04_SUCT_Z = P04_PORT_Z + SUCT_RISE
draw_pipe_path(ax,
    [EXIT_L, PORT_IN_YD, PORT_IN_YD],
    [_P04_SUCT_Z, _P04_SUCT_Z, P04_PORT_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)
ax.annotate("", xy=(sx(EXIT_L + _AW), sz(_P04_SUCT_Z)),
            xytext=(sx(EXIT_L), sz(_P04_SUCT_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BLACK_SYS), zorder=11)
ax.text(sx(EXIT_L - 5), sz(_P04_SUCT_Z),
        "FROM\nTRAY\nSUMP", ha="right", va="center",
        fontsize=4, color=C_BLACK_SYS, zorder=10, **FONT)

# P-04 discharge: outlet (LEFT port) → drop → right to DV-02
draw_pipe_path(ax,
    [PORT_OUT_YD, PORT_OUT_YD, DV02_YD],
    [P04_PORT_Z, DV02_Z, DV02_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)

# DV-02 (3-way diverter — diamond symbol)
draw_ball_valve(DV02_YD, DV02_Z, "DV\n02", C_BLACK_EC)

# DV-02 Brown output → IBC-3 (RIGHT)
DV_OUT_Z_BROWN = DV02_Z + BV_R + 15
draw_pipe_path(ax,
    [DV02_YD, DV02_YD, EXIT_R],
    [DV02_Z + BV_R, DV_OUT_Z_BROWN, DV_OUT_Z_BROWN],
    PIPE_OD, PIPE_WALL, fc=C_BROWN, zorder=Z_BROWN)
ax.text(sx(EXIT_R + 5), sz(DV_OUT_Z_BROWN),
        "→ IBC-3", ha="left", va="center",
        fontsize=4, color=C_BROWN, zorder=10, **FONT)

# DV-02 Black output → IBC-4 (RIGHT)
DV_OUT_Z_BLACK = DV02_Z - BV_R - 15
draw_pipe_path(ax,
    [DV02_YD, DV02_YD, EXIT_R],
    [DV02_Z - BV_R, DV_OUT_Z_BLACK, DV_OUT_Z_BLACK],
    PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)
ax.text(sx(EXIT_R + 5), sz(DV_OUT_Z_BLACK),
        "→ IBC-4", ha="left", va="center",
        fontsize=4, color=C_BLACK_SYS, zorder=10, **FONT)


# ════════════════════════════════════════════════════════════════
#  P-03 WASTE EVACUATION (C_BLACK_SYS) — right column
# ════════════════════════════════════════════════════════════════

# P-03 suction: IBC-4 (RIGHT) → P-03 inlet (right port)
draw_pipe_path(ax,
    [EXIT_R, P03_PORT_IN],
    [P03_PORT_Z, P03_PORT_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)
ax.annotate("", xy=(sx(EXIT_R - _AW), sz(P03_PORT_Z)),
            xytext=(sx(EXIT_R), sz(P03_PORT_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BLACK_SYS), zorder=11)
ax.text(sx(EXIT_R + 5), sz(P03_PORT_Z),
        "FROM\nIBC-4\n(WASTE)", ha="left", va="center",
        fontsize=4, color=C_BLACK_SYS, zorder=10, **FONT)

# P-03 discharge: outlet (left port) → drop 60mm → right to D4 bulkhead
_P03_DISCH_Z = P03_PORT_Z - 60
draw_pipe_path(ax,
    [P03_PORT_OUT, P03_PORT_OUT, EXIT_R],
    [P03_PORT_Z, _P03_DISCH_Z, _P03_DISCH_Z],
    PIPE_OD, PIPE_WALL, fc=C_BLACK_SYS, zorder=Z_BLACK)
ax.annotate("", xy=(sx(EXIT_R), sz(_P03_DISCH_Z)),
            xytext=(sx(EXIT_R - _AW), sz(_P03_DISCH_Z)),
            arrowprops=dict(**_arrow_kw, color=C_BLACK_SYS), zorder=11)
ax.text(sx(EXIT_R + 5), sz(_P03_DISCH_Z),
        "TO D4\nDRAIN\nPORT", ha="left", va="center",
        fontsize=4, color=C_BLACK_SYS, zorder=10, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  6. DIMENSIONS
# ═══════════════════════════════════════════════════════════════════════════

# Panel width (Yd span)
draw_dim_h(ax, sx(0), sx(PANEL_W), sz(-40),
           f"{PANEL_W}", offset=0.06, fs=5, color=C_DIM, font=FONT)

# Pump body width
draw_dim_h(ax, sx(PUMP_COL - PUMP_W / 2), sx(PUMP_COL + PUMP_W / 2),
           sz(P01_Z - 15),
           f"{PUMP_W}", offset=0.04, fs=4, color=C_DIM, font=FONT)

# Filter OD
draw_dim_h(ax, sx(FILT_COL - FILT_OD / 2), sx(FILT_COL + FILT_OD / 2),
           sz(F03_Z - 15),
           f"O/{FILT_OD}", offset=0.04, fs=4, color=C_FILTER, font=FONT)

# Filter housing height (single — bottom filter)
draw_dim_v(ax, sx(FILT_COL + FILT_OD / 2 + 20),
           sz(F03_Z), sz(F03_Z + FILT_H),
           f"{FILT_H}", offset=0.08, fs=4.5, color=C_FILTER,
           right=True, font=FONT)

# Filter stack height (full)
draw_dim_v(ax, sx(FILT_COL + FILT_OD / 2 + 50),
           sz(F03_Z), sz(FILT_STACK_TOP),
           f"{FILT_STACK_TOP}", offset=0.08, fs=4.5, color=C_DIM,
           right=True, font=FONT)

# Pump body height
draw_dim_v(ax, sx(PUMP_COL + PUMP_W / 2 + 15),
           sz(P01_Z), sz(P01_Z + PUMP_H),
           f"{PUMP_H}", offset=0.06, fs=4, color=C_DIM,
           right=True, font=FONT)

# Panel height
draw_dim_v(ax, sx(-30), sz(0), sz(PANEL_H),
           f"{PANEL_H}", offset=0.1, fs=5, color=C_DIM,
           right=False, font=FONT)

# Filter gap dimension (between bottom two filters)
draw_dim_v(ax, sx(FILT_COL - FILT_OD / 2 - 20),
           sz(F03_Z + FILT_H), sz(F02_Z),
           f"{FILT_GAP}", offset=0.06, fs=3.5, color=C_DIM,
           right=False, font=FONT)

# Panel Z position (AFF annotation at bottom edge)
ax.text(sx(PANEL_W + 30), sz(0),
        f"Z={PANEL_Z_AFF}\nAFF", ha="left", va="center",
        fontsize=4, color=C_DIM, zorder=10, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  7. LEADERS
# ═══════════════════════════════════════════════════════════════════════════

# Pump specs
leader(ax,
       sx(PUMP_COL - PUMP_W / 2), sz(P01_Z + PUMP_H / 2),
       sx(X_SHOW_L + 10), sz(P01_Z + PUMP_H / 2 - 60),
       "Shurflo 2088\n12V · 3.5 GPM · 45 PSI\n(×3 on SS L-brackets)",
       fs=4, color=C_PUMP_EC, font=FONT)

# ACC-01
leader(ax,
       sx(ACC_YD + ACC_OD / 2), sz(ACC_BODY_Z + ACC_LEN / 2),
       sx(PANEL_W + 40), sz(ACC_BODY_Z + ACC_LEN / 2 + 60),
       "ACC-01: 0.75L ACCUM.\nO/127 × 150mm\n1/2\" MNPT (bottom)",
       fs=4, color=C_BLUE_EC, font=FONT)

# Filter specs
leader(ax,
       sx(FILT_COL + FILT_OD / 2), sz(F01_Z + FILT_H / 2),
       sx(PANEL_W + 40), sz(F01_Z + FILT_H / 2 + 30),
       "4.5\"×10\" FILTER HOUSING\n1\" NPT IN/OUT\n(×3 separate, sump-down)",
       fs=4, color=C_FILTER, font=FONT)

# Max depth annotation
max_depth = max(PUMP_D, FILT_OD)
leader(ax,
       sx(PUMP_COL), sz(PANEL_H + 10),
       sx(X_SHOW_L + 10), sz(PANEL_H + 40),
       f"MAX PROTRUSION: {max_depth}mm\nFROM PANEL FACE (in -X)",
       fs=4, color=C_NEW, font=FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  CROSS-SECTION STRIP — panel position relative to walkway (Yd × Z)
# ═══════════════════════════════════════════════════════════════════════════

# Cross-section positioned at bottom of figure
CS_LEFT  = 0.6   # inches from left
CS_BOT   = 2.0   # inches from bottom
CS_W_IN  = 6.0   # strip width (inches)
CS_H_IN  = 1.0   # strip height (inches)

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
ax.text(CS_LEFT + CS_W_IN / 2, CS_BOT + CS_H_IN + 0.2,
        "CROSS-SECTION — PANEL IN IBC CORRIDOR (looking along X axis)",
        ha="center", va="bottom",
        fontsize=5, color=C_DIM, fontweight="bold", zorder=10, **FONT)

# Pinhole wall (Yd=0) — thick line
ax.plot([cs_yd(0), cs_yd(0)], [cs_z(-20), cs_z(Z_CS_MAX)],
        color=C_WALL, lw=4.0, zorder=3)
ax.text(cs_yd(0) - 0.05, cs_z(Z_CS_MAX / 2),
        "WALL\nYd=0", ha="right", va="center",
        fontsize=3, color=C_WALL_HATCH, zorder=10, **FONT)

# Floor
ax.plot([cs_yd(0), cs_yd(YD_MAX)], [cs_z(0), cs_z(0)],
        color=C_OUT, lw=1.5, zorder=3)

# Walkway (Yd=0 to 300)
ax.add_patch(mpatches.Rectangle(
    (cs_yd(0), cs_z(0)), WALKWAY_W / YD_MAX * CS_W_IN, WALKWAY_Z / Z_CS_MAX * CS_H_IN,
    fc=C_WALK, ec=C_NEW, lw=1.0, zorder=4, alpha=0.6))
ax.text(cs_yd(WALKWAY_W / 2), cs_z(WALKWAY_Z / 2),
        "WALKWAY\n300mm", ha="center", va="center",
        fontsize=3, color=C_NEW, fontweight="bold", zorder=5, **FONT)

# Near IBC column cross-section (Yd=30 to 1046)
C_IBC_CS = "#E0D8C8"
C_IBC_CS_EC = "#B0A898"
ax.add_patch(mpatches.Rectangle(
    (cs_yd(IBC_NEAR_YD), cs_z(0)),
    IBC_D / YD_MAX * CS_W_IN, cs_z(Z_CS_MAX) - cs_z(0),
    fc=C_IBC_CS, ec=C_IBC_CS_EC, lw=1.0, zorder=2, alpha=0.35))
ax.text(cs_yd(IBC_NEAR_YD + IBC_D / 2), cs_z(Z_CS_MAX * 0.5),
        "NEAR IBC\nCOLUMN", ha="center", va="center",
        fontsize=3.5, color=C_IBC_CS_EC, zorder=3, **FONT)

# Far IBC column (partial — Yd=1316 onward)
ax.add_patch(mpatches.Rectangle(
    (cs_yd(CORRIDOR_FAR), cs_z(0)),
    (YD_MAX - CORRIDOR_FAR) / YD_MAX * CS_W_IN, cs_z(Z_CS_MAX) - cs_z(0),
    fc=C_IBC_CS, ec=C_IBC_CS_EC, lw=1.0, zorder=2, alpha=0.35))
ax.text(cs_yd((CORRIDOR_FAR + YD_MAX) / 2), cs_z(Z_CS_MAX * 0.5),
        "FAR IBC\nCOLUMN", ha="center", va="center",
        fontsize=3.5, color=C_IBC_CS_EC, zorder=3, **FONT)

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
        fontsize=2.5, color=C_PLY_EC, fontweight="bold", zorder=10, **FONT)

# Corridor width dimension
draw_dim_h(ax, cs_yd(IBC_NEAR_END), cs_yd(CORRIDOR_FAR), cs_z(Z_CS_MAX + 10),
           "270 CORRIDOR", offset=0.04, fs=4, color=C_DIM, font=FONT)

# Yd axis
ax.text(cs_yd(YD_MAX / 2), cs_z(-15) - 0.18,
        "Yd (mm from pinhole wall) →", ha="center", va="top",
        fontsize=4, color=C_DIM, zorder=10, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  NOTES
# ═══════════════════════════════════════════════════════════════════════════
notes = [
    "EQUIPMENT PANEL — IBC PLUMBING CORRIDOR — ALL PIPE CONNECTIONS SHOWN",
    f"1. Panel: 18mm marine ply spanning corridor Yd={PANEL_YD}–{PANEL_YD + PANEL_W} (270mm).",
    f"2. Panel face at X={PANEL_WALL_X}, equipment protrudes toward open end (-X direction).",
    f"3. Panel height: Z={PANEL_Z_AFF}–{PANEL_Z_AFF + PANEL_H}mm AFF ({PANEL_H}mm), uses full IBC stack height.",
    "4. FILTERS: F-01 (50µm, top) → F-02 (5µm) → F-03 (GAC, bottom) — gravity-fed series flow.",
    "5. TOP: P-01/P-02/P-04 (left col) + ACC-01; P-03 waste evac (right col) — above filter stack.",
    "6. BV-01/BV-02 on Blue circuit. DV-02 on P-04 discharge (3-way to IBC-3 or IBC-4).",
    f"7. Max protrusion: {max_depth}mm. Near IBCs LEFT, far IBCs RIGHT in this view.",
    "8. Flow: P-02 ↑ F-01 (top) ↓ F-02 ↓ F-03 (bottom) → IBC-1. Gravity assists after F-01.",
]
draw_notes(ax, notes, 0.2, 1.6, spacing=0.13,
           fs=3.8, width=FW - 0.4, color=C_DIM, title_color=C_NEW, font=FONT)


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
ax.text(_cut_x + 0.06, _cut_z_top,
        "B", fontsize=5, color="#1A237E", fontweight="bold",
        va="bottom", ha="center", zorder=11, **FONT)
ax.text(_cut_x + 0.06, _cut_z_bot,
        "B", fontsize=5, color="#1A237E", fontweight="bold",
        va="top", ha="center", zorder=11, **FONT)

# ── Position and scale ──
SC_D = 70.0       # mm per figure inch (~1:3 scale)
DET_LEFT = 7.0    # figure x for Yd=0 (panel front face)
DET_Z0 = 9.5      # figure y for head center (Z=0)


def det_y(yd_mm):
    """Detail Yd (mm from panel face) → figure x."""
    return DET_LEFT + yd_mm / SC_D


def det_z(z_mm):
    """Detail Z (mm from head center) → figure y."""
    return DET_Z0 + z_mm / SC_D


# Detail title
ax.text(det_y(80), det_z(85),
        "DETAIL B — FILTER MOUNTING\nCROSS-SECTION (~1:3)",
        ha="center", va="bottom",
        fontsize=5, fontweight="bold",
        color="#1A237E", zorder=10, **FONT)

# ── All Z coords relative to filter head port center ──

# 1. Equipment panel (18mm marine ply)
D_PANEL_T = 18.0
_dpanel_bot = -320
_dpanel_top = 65
ax.add_patch(mpatches.Rectangle(
    (det_y(-D_PANEL_T), det_z(_dpanel_bot)),
    D_PANEL_T / SC_D, (_dpanel_top - _dpanel_bot) / SC_D,
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
    D_SPACER_T / SC_D, D_SPACER_VIS_H / SC_D,
    fc="#E0D8B0", ec="#A09060", lw=1.0, zorder=4, hatch=".."))

# 3. Steel bracket tab (3mm)
D_BRACKET_YD = D_SPACER_YD + D_SPACER_T      # 50
D_BRACKET_T = 3
D_BRACKET_VIS_H = 50
ax.add_patch(mpatches.Rectangle(
    (det_y(D_BRACKET_YD), det_z(-D_BRACKET_VIS_H / 2)),
    D_BRACKET_T / SC_D, D_BRACKET_VIS_H / SC_D,
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
    4 / SC_D, 6 / SC_D,
    fc="#666666", ec=C_FRAME, lw=0.8, zorder=7))
ax.add_patch(mpatches.Rectangle(
    (det_y(_bolt_tip_yd - 2), det_z(D_BOLT_Z - 4)),
    3 / SC_D, 8 / SC_D,
    fc="#666666", ec=C_FRAME, lw=0.8, zorder=7))
leader(ax, det_y(_bolt_head_yd + 3), det_z(D_BOLT_Z),
       det_y(_bolt_head_yd + 35), det_z(D_BOLT_Z - 25),
       "M6×80 BOLT\n+ NYLOC NUT", fs=3.5, color=C_DIM, font=FONT)

# 5. Filter head (80mm depth × 70mm visible height)
D_HEAD_YD = D_BRACKET_YD + D_BRACKET_T + 2   # 55 (2mm gap for clamp)
D_HEAD_DEPTH = 80
D_HEAD_VIS_H = FILT_HEAD                     # 70
ax.add_patch(mpatches.Rectangle(
    (det_y(D_HEAD_YD), det_z(-D_HEAD_VIS_H / 2)),
    D_HEAD_DEPTH / SC_D, D_HEAD_VIS_H / SC_D,
    fc="#555555", ec=C_FRAME, lw=1.5, zorder=5))
ax.text(det_y(D_HEAD_YD + D_HEAD_DEPTH / 2), det_z(0),
        "HEAD", ha="center", va="center",
        fontsize=4, color="white", fontweight="bold", zorder=6, **FONT)

# 6. Sump bowl (hangs below head)
D_SUMP_H = FILT_H - FILT_HEAD               # 270
D_SUMP_W = FILT_OD                           # 130
_sump_cy = D_HEAD_YD + D_HEAD_DEPTH / 2      # 95
_sump_top_z = -D_HEAD_VIS_H / 2              # -35
_sump_bot_z = _sump_top_z - D_SUMP_H         # -305
ax.add_patch(mpatches.Rectangle(
    (det_y(_sump_cy - D_SUMP_W / 2), det_z(_sump_bot_z)),
    D_SUMP_W / SC_D, D_SUMP_H / SC_D,
    fc=C_FILTER, ec=C_FRAME, lw=1.2, alpha=0.6, zorder=4))
ax.text(det_y(_sump_cy), det_z(_sump_top_z - D_SUMP_H / 2),
        "SUMP\nBOWL", ha="center", va="center",
        fontsize=4, color="white", fontweight="bold", zorder=6, **FONT)

# Sump height dimension
draw_dim_v(ax, det_y(_sump_cy + D_SUMP_W / 2 + 10),
           det_z(_sump_bot_z), det_z(_sump_top_z),
           f"{int(D_SUMP_H)}", offset=0.06, fs=3.5, color=C_DIM,
           right=True, font=FONT)

# Cartridge removal arrow
ax.annotate("", xy=(det_y(_sump_cy), det_z(_sump_bot_z - 25)),
            xytext=(det_y(_sump_cy), det_z(_sump_bot_z - 5)),
            arrowprops=dict(arrowstyle="-|>", color="#CC4444", lw=1.5,
                            mutation_scale=8), zorder=10)
ax.text(det_y(_sump_cy), det_z(_sump_bot_z - 30),
        "UNSCREW SUMP\nFOR CARTRIDGE\nREPLACEMENT",
        ha="center", va="top",
        fontsize=3.5, color="#CC4444", fontweight="bold", zorder=10, **FONT)

# 7. 1" NPT port with pipe stub
D_PORT_YD = D_HEAD_YD + D_HEAD_DEPTH         # 135
D_PIPE_OD_D = 33
D_PIPE_WALL_D = 4
D_STUB_LEN = 40
ax.add_patch(mpatches.Rectangle(
    (det_y(D_PORT_YD - 12), det_z(-D_PIPE_OD_D / 2)),
    12 / SC_D, D_PIPE_OD_D / SC_D,
    fc="white", ec=C_FRAME, lw=0.7, zorder=6))
ax.add_patch(mpatches.Rectangle(
    (det_y(D_PORT_YD), det_z(-D_PIPE_OD_D / 2)),
    D_STUB_LEN / SC_D, D_PIPE_OD_D / SC_D,
    fc=C_PIPE_FILL, ec=C_FRAME, lw=0.7, zorder=5))
ax.add_patch(mpatches.Rectangle(
    (det_y(D_PORT_YD), det_z(-D_PIPE_OD_D / 2 + D_PIPE_WALL_D)),
    D_STUB_LEN / SC_D, (D_PIPE_OD_D - 2 * D_PIPE_WALL_D) / SC_D,
    fc="white", ec="none", zorder=6))
leader(ax, det_y(D_PORT_YD + D_STUB_LEN), det_z(0),
       det_y(D_PORT_YD + D_STUB_LEN + 25), det_z(18),
       "1\" HDPE\nTO NEXT STAGE", fs=3.5, color=C_PIPE_EC, font=FONT)

# 8. Clamp band at head/sump junction
D_CLAMP_H = 12
_clamp_yd_l = _sump_cy - D_SUMP_W / 2 - 4
_clamp_w = D_SUMP_W + 8
ax.add_patch(mpatches.Rectangle(
    (det_y(_clamp_yd_l), det_z(_sump_top_z - D_CLAMP_H)),
    _clamp_w / SC_D, D_CLAMP_H / SC_D,
    fc="#888888", ec=C_FRAME, lw=0.8, zorder=6))

# ── Detail dimensions ──
_standoff = D_SPACER_T + D_BRACKET_T   # 53mm from panel face
draw_dim_h(ax, det_y(0), det_y(D_BRACKET_YD + D_BRACKET_T),
           det_z(-55), f"{_standoff}mm STANDOFF", offset=0.05, fs=3.5,
           color=C_DIM, font=FONT)
draw_dim_h(ax, det_y(-D_PANEL_T), det_y(0),
           det_z(55), f"{int(D_PANEL_T)}", offset=0.04, fs=3,
           color=C_DIM, font=FONT)

# ── Component labels above section ──
_lbl_z = 68
for _ly, _ltxt in [(-D_PANEL_T / 2, "18mm\nPANEL"),
                    (D_SPACER_YD + D_SPACER_T / 2, "50mm\nHDPE"),
                    (D_BRACKET_YD + D_BRACKET_T / 2, "3mm\nBKT")]:
    ax.text(det_y(_ly), det_z(_lbl_z), _ltxt, ha="center", va="bottom",
            fontsize=3, color=C_FRAME, zorder=10, **FONT)
    ax.plot([det_y(_ly), det_y(_ly)], [det_z(_lbl_z - 3), det_z(40)],
            color=C_DIM, lw=0.4, ls=":", zorder=2)

# Section description
ax.text(det_y(80), det_z(_sump_bot_z - 50),
        "SECTION THROUGH FILTER HEAD\nPERPENDICULAR TO PANEL\nAT PORT HEIGHT\n(4.5\"×10\" BIG BLUE — SUMP-DOWN)",
        ha="center", va="top",
        fontsize=3.5, color="#666666", style="italic", zorder=10, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  TITLE BLOCK
# ═══════════════════════════════════════════════════════════════════════════
title_block(ax, "SHEET 1 OF 1",
            drawing_title="EQUIPMENT PANEL — IBC CORRIDOR MOUNTING",
            subtitle="FRONT ELEVATION + PIPE ROUTING + CROSS-SECTION + DETAIL B",
            scale_note="ELEV 1:120 · DETAIL B ~1:3 · X-SECTION NTS · ALL DIMS IN mm",
            doc_id="TBS-001 · Reorg Proposal",
            height=0.028)

# ── Save ─────────────────────────────────────────────────────────────────
os.makedirs(DIAGRAMS_DIR, exist_ok=True)
out = os.path.join(DIAGRAMS_DIR, "panel-layout.png")
fig.savefig(out, dpi=150, facecolor="white", edgecolor="none")
plt.close(fig)
print(f"Panel layout → {out}")
