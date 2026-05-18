#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_pump_manifold_diagram.py
Generates a detailed plumbing diagram of the pump manifold assembly mounted on
the pinhole wall (Yd=0).

Sheet 1 — Pump Manifold Elevation (1:5)
  View from inside the container looking at the pinhole wall.
  X axis horizontal (mirrored), Z axis vertical.
  Shows: mounting frame, four Shurflo 2088 pumps (P-01 through P-04),
         ACC-01 accumulator, BV-01/BV-02 ball valves, all pipe connections
         with parallel-wall drawing, dimensions and leader callouts.

  Detail A — Pump Mounting Cross-Section (~1:2)
  Shows: container wall → plywood → mounting bracket → pump body → ports.

Output:
  diagrams/pump-manifold-sheet1.png  (1800 x 1200 px, 150 dpi)
"""

import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Arc
from matplotlib.gridspec import GridSpec

from tbs_constants import (
    C_OUT, C_CL, C_DIM, C_ALUM, C_STEEL, C_GASKT,
    PUMP_X, PUMP_W, PUMP_H_LO, PUMP_H_HI,
    FILT_PIPE_OD, FILT_PIPE_WALL,
    C_LEN, C_WID, WALKWAY_W,
    PROC_TRAY_YD_NEAR, PROC_TRAY_D, PROC_TRAY_DRAIN_X, PROC_TRAY_DRAIN_YD,
    FSKID_X, FSKID_W,
    BLUE_IBC_Y, IBC_FAR_Y, IBC_COL_X, IBC_W, IBC_D,
    svg_path,
)
from tbs_title_block import title_block
from tbs_drawing import (
    draw_dim_h, draw_dim_v, leader, draw_rect, hatch_rect,
    place_label, register_pipe, reset_label_registry,
)

# ── Color palette ─────────────────────────────────────────────────────────────
C_FRAME      = "#1A1A1A"     # structural outlines
C_STEEL_FILL = "#B0B0B8"     # steel section fill
C_PLY        = "#D4C8A0"     # plywood backboard fill
C_HDPE       = "#4A7A4A"     # HDPE pipe fill (green-grey)
C_BLUE       = "#2979B8"     # Blue system color
C_BROWN      = "#8B5E3C"     # Brown system color
C_BLACK_SYS  = "#555555"     # Black/waste system color
C_PUMP_BODY  = "#E8884A"     # pump body fill (orange)
C_ACC        = "#3366AA"     # accumulator body (blue tank)
C_VALVE      = "#CC4444"     # valve symbol fill
C_TEXT       = "#1A1A1A"     # general text
C_BG         = "#F5F5F0"     # background

# ── Scale: 1:5 ───────────────────────────────────────────────────────────────
SC = 5.0  # mm per drawing unit

# Drawing origin offsets (data units)
OX = 3.0
OZ = 2.0

def sx(x_mm):
    """Convert X position in mm to drawing x coordinate."""
    return OX + (x_mm - PUMP_X + 200) / SC  # 200mm margin left of frame

def sz(z_mm):
    """Convert Z position in mm to drawing y coordinate."""
    return OZ + z_mm / SC


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — PUMP MANIFOLD ELEVATION (1:5)
# View from inside container looking at pinhole wall (Yd=0)
# X horizontal (mirrored), Z vertical
# ═══════════════════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(24, 16))
fig.patch.set_facecolor(C_BG)
gs = GridSpec(2, 2, figure=fig, width_ratios=[1.6, 1],
             height_ratios=[1.2, 1], wspace=0.05, hspace=0.06)

ax = fig.add_subplot(gs[0, 0])   # Main elevation (top left)
ax.set_facecolor(C_BG)
ax.set_aspect("equal")
ax.axis("off")

ax2 = fig.add_subplot(gs[0, 1])  # Detail A — cross-section (top right)
ax2.set_facecolor(C_BG)
ax2.set_aspect("equal")
ax2.axis("off")

ax3 = fig.add_subplot(gs[1, :])  # Detail B — plan view (full bottom row)
ax3.set_facecolor(C_BG)
ax3.set_aspect("equal")
ax3.axis("off")

# Axis limits — manifold zone: X=2300–3000, Z=0–800
ax.set_xlim(sx(2200) - 1, sx(3100) + 1)
ax.set_ylim(sz(-50) - 1, sz(850) + 2)

# Mirror X axis for interior view convention
ax.invert_xaxis()

# Reset label registry for collision avoidance
reset_label_registry()

# ── Manifold layout constants ────────────────────────────────────────────────
# Frame: X=2500–2800, Z=200–600 (from tbs_constants)
FRAME_X = PUMP_X        # 2500
FRAME_W = PUMP_W         # 300
FRAME_Z_LO = PUMP_H_LO   # 200
FRAME_Z_HI = PUMP_H_HI   # 600
FRAME_H = FRAME_Z_HI - FRAME_Z_LO  # 400

ANGLE_W = 25   # frame member width (25×25×3mm SHS)
FRAME_LW = 2.0

# Pump body dimensions (Shurflo 2088, simplified for elevation)
PUMP_BODY_W = 100   # width in X direction (elevation view, simplified)
PUMP_BODY_H = 70    # height in Z direction
PUMP_PORT_OD = 12   # 1/2" NPSM port visual radius

# 2×2 pump grid within the frame
# Inner frame width: 300 - 2*25 = 250mm. Two pumps at 100mm + gaps = fits.
# Inner frame height: 400 - 2*25 = 350mm. Two rows at 70mm + gaps = fits.
PUMP_MARGIN_X = 10   # gap from frame inner edge to pump
PUMP_GAP_X = FRAME_W - 2 * ANGLE_W - 2 * PUMP_BODY_W - 2 * PUMP_MARGIN_X  # 30mm
PUMP_GAP_Z = 30      # vertical gap between rows

P01_X = FRAME_X + ANGLE_W + PUMP_MARGIN_X
P02_X = FRAME_X + FRAME_W - ANGLE_W - PUMP_MARGIN_X - PUMP_BODY_W
P03_X = P01_X
P04_X = P02_X

# Vertical positions (bottom of pump body)
ROW_TOP_Z = FRAME_Z_HI - ANGLE_W - PUMP_BODY_H - 20  # top row near frame top
ROW_BOT_Z = FRAME_Z_LO + ANGLE_W + 20                 # bottom row near frame bottom

P01_Z = ROW_TOP_Z
P02_Z = ROW_TOP_Z
P03_Z = ROW_BOT_Z
P04_Z = ROW_BOT_Z

# Pipe constants
OD = FILT_PIPE_OD      # 33mm
WALL = FILT_PIPE_WALL   # 4mm

# ── Container wall context ───────────────────────────────────────────────────
CORR_SPACING = 457
for rib_x in range(2285, 3200, CORR_SPACING):
    ax.plot([sx(rib_x), sx(rib_x)], [sz(-30), sz(800)],
            color="#AAAAAA", lw=0.6, ls="--", zorder=1)

# Floor line
ax.plot([sx(2200), sx(3100)], [sz(0), sz(0)],
        color="#888888", lw=1.5, ls="-", zorder=1)
ax.text(sx(2250), sz(-15), "FLOOR (Z=0)", ha="left", va="top",
        fontsize=6, color="#888888", style="italic")

# Walkway deck line
WALKWAY_Z = 100
ax.plot([sx(2300), sx(3000)], [sz(WALKWAY_Z), sz(WALKWAY_Z)],
        color=C_STEEL_FILL, lw=2.0, ls="-", zorder=1)
ax.text(sx(2350), sz(WALKWAY_Z + 10), "WALKWAY DECK (Z=100)",
        ha="left", va="bottom", fontsize=5.5, color="#888888", style="italic")


# ── Mounting frame (25×25×3mm SHS perimeter) ─────────────────────────────────

# Bottom rail
ax.add_patch(plt.Rectangle((sx(FRAME_X), sz(FRAME_Z_LO)),
             FRAME_W / SC, ANGLE_W / SC,
             fc=C_STEEL_FILL, ec=C_FRAME, lw=FRAME_LW, zorder=3))

# Top rail
ax.add_patch(plt.Rectangle((sx(FRAME_X), sz(FRAME_Z_HI - ANGLE_W)),
             FRAME_W / SC, ANGLE_W / SC,
             fc=C_STEEL_FILL, ec=C_FRAME, lw=FRAME_LW, zorder=3))

# Left upright
ax.add_patch(plt.Rectangle((sx(FRAME_X), sz(FRAME_Z_LO)),
             ANGLE_W / SC, FRAME_H / SC,
             fc=C_STEEL_FILL, ec=C_FRAME, lw=FRAME_LW, zorder=3))

# Right upright
ax.add_patch(plt.Rectangle((sx(FRAME_X + FRAME_W - ANGLE_W), sz(FRAME_Z_LO)),
             ANGLE_W / SC, FRAME_H / SC,
             fc=C_STEEL_FILL, ec=C_FRAME, lw=FRAME_LW, zorder=3))


# ── Backing board (18mm plywood) ─────────────────────────────────────────────
ply_x = FRAME_X + ANGLE_W
ply_w = FRAME_W - 2 * ANGLE_W
ply_z = FRAME_Z_LO + ANGLE_W
ply_h = FRAME_H - 2 * ANGLE_W
ax.add_patch(plt.Rectangle((sx(ply_x), sz(ply_z)),
             ply_w / SC, ply_h / SC,
             fc=C_PLY, ec="#A09060", lw=1.0, alpha=0.5, zorder=2.5))


# ── Wall mounting brackets ───────────────────────────────────────────────────
BRACKET_W = 50
BRACKET_H = 60
for bz in [FRAME_Z_LO + 40, FRAME_Z_HI - 80]:
    for bx in [FRAME_X - BRACKET_W, FRAME_X + FRAME_W]:
        ax.add_patch(plt.Rectangle((sx(bx), sz(bz)),
                     BRACKET_W / SC, BRACKET_H / SC,
                     fc="#D0D0D0", ec=C_FRAME, lw=1.2, zorder=2))
        bolt_cx = bx + BRACKET_W / 2
        bolt_cz = bz + BRACKET_H / 2
        ax.plot(sx(bolt_cx), sz(bolt_cz), 'x', color=C_FRAME,
                markersize=5, mew=1.5, zorder=4)


# ── Pipe drawing helper (parallel-wall style) ────────────────────────────────
# Copied from generate_filter_skid_diagram.py for consistency
def draw_pipe_path(ax, x_pts, z_pts, od_mm, wall_mm,
                   fc=C_HDPE, ec=C_FRAME, bore_fc="white",
                   elbow_r=None, zorder=8):
    """Draw a pipe run with parallel walls."""
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
        alpha = math.acos(cos_a)
        turn = math.pi - alpha
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

        def _arc_ring(r_out, r_in, color, z_ord, _cy=cy, _cz=cz_e, _angles=angles):
            ox_ = [sx(_cy + r_out * math.cos(a)) for a in _angles]
            oz_ = [sz(_cz + r_out * math.sin(a)) for a in _angles]
            ix_ = [sx(_cy + r_in * math.cos(a)) for a in _angles]
            iz_ = [sz(_cz + r_in * math.sin(a)) for a in _angles]
            ax.fill(ox_ + ix_[::-1], oz_ + iz_[::-1],
                    fc=color, ec=ec if color != bore_fc else "none",
                    lw=0.8 if color != bore_fc else 0, zorder=z_ord)

        _arc_ring(r_eff + half_od, max(r_eff - half_od, 0.5), fc, zorder)
        _arc_ring(r_eff + half_id, max(r_eff - half_id, 0.5), bore_fc, zorder + 1)


# ── Draw pump body ───────────────────────────────────────────────────────────
def draw_pump(ax, px, pz, label, sublabel, color=C_PUMP_BODY):
    """Draw a single Shurflo 2088 pump in elevation.

    px, pz: bottom-left corner position in mm.
    Returns: (inlet_x, outlet_x, port_z) — port centers.
    """
    # Pump body rectangle
    ax.add_patch(plt.Rectangle((sx(px), sz(pz)),
                 PUMP_BODY_W / SC, PUMP_BODY_H / SC,
                 fc=color, ec=C_FRAME, lw=1.5, alpha=0.85, zorder=5))

    # Pump motor dome (top of body, simplified as arc)
    dome_cx = px + PUMP_BODY_W / 2
    dome_cz = pz + PUMP_BODY_H
    dome_r = 25
    theta = np.linspace(0, 180, 30)
    dome_x = [sx(dome_cx + dome_r * np.cos(np.radians(a))) for a in theta]
    dome_z = [sz(dome_cz + dome_r * np.sin(np.radians(a))) for a in theta]
    ax.fill(dome_x, dome_z, fc=color, ec=C_FRAME, lw=1.2, alpha=0.85, zorder=5)

    # Pump label inside body
    ax.text(sx(px + PUMP_BODY_W / 2), sz(pz + PUMP_BODY_H / 2),
            label, ha="center", va="center",
            fontsize=7, fontweight="bold", color="white", zorder=6)

    # Sub-label below pump
    ax.text(sx(px + PUMP_BODY_W / 2), sz(pz - 8),
            sublabel, ha="center", va="top",
            fontsize=5, color=C_TEXT, style="italic", zorder=6)

    # Ports: IN on higher-X side (facing IBCs, appears LEFT in mirrored view)
    #        OUT on lower-X side (facing cargo door, appears RIGHT in mirrored view)
    port_z = pz + PUMP_BODY_H / 2
    inlet_x = px + PUMP_BODY_W   # higher X = left in mirrored view
    outlet_x = px                 # lower X = right in mirrored view

    # Port circles
    ax.add_patch(plt.Circle((sx(inlet_x), sz(port_z)), PUMP_PORT_OD / SC,
                 fc="white", ec=C_FRAME, lw=1.2, zorder=7))
    ax.add_patch(plt.Circle((sx(outlet_x), sz(port_z)), PUMP_PORT_OD / SC,
                 fc="white", ec=C_FRAME, lw=1.2, zorder=7))

    # Port labels
    ax.text(sx(inlet_x), sz(port_z), "IN", ha="center", va="center",
            fontsize=3.5, fontweight="bold", color=C_FRAME, zorder=8)
    ax.text(sx(outlet_x), sz(port_z), "OUT", ha="center", va="center",
            fontsize=3.5, fontweight="bold", color=C_FRAME, zorder=8)

    return inlet_x, outlet_x, port_z


# Draw all four pumps
p01_in, p01_out, p01_port_z = draw_pump(ax, P01_X, P01_Z, "P-01", "BLUE SUPPLY")
p02_in, p02_out, p02_port_z = draw_pump(ax, P02_X, P02_Z, "P-02", "BROWN RECYCLE")
p03_in, p03_out, p03_port_z = draw_pump(ax, P03_X, P03_Z, "P-03", "WASTE EVAC")
p04_in, p04_out, p04_port_z = draw_pump(ax, P04_X, P04_Z, "P-04", "TRAY DRAIN")


# ── ACC-01 Accumulator ──────────────────────────────────────────────────────
# Mounted between the two pump rows, centered in the frame
# The gap between rows is ~170mm (P-01 bottom at Z=485, P-03 top at Z=315)
ACC_W = 60    # width in X
ACC_H = 50    # height in Z
ACC_X = FRAME_X + (FRAME_W - ACC_W) / 2   # centered in frame X
ACC_Z = (ROW_BOT_Z + PUMP_BODY_H + ROW_TOP_Z) / 2 - ACC_H / 2  # centered between rows

ax.add_patch(plt.Rectangle((sx(ACC_X), sz(ACC_Z)),
             ACC_W / SC, ACC_H / SC,
             fc=C_ACC, ec=C_FRAME, lw=1.5, alpha=0.8, zorder=5))

# Pressure vessel dome (rounded top)
acc_cx = ACC_X + ACC_W / 2
acc_top = ACC_Z + ACC_H
acc_dome_r = ACC_W / 2
theta_acc = np.linspace(0, 180, 30)
acc_dome_x = [sx(acc_cx + acc_dome_r * np.cos(np.radians(a))) for a in theta_acc]
acc_dome_z = [sz(acc_top + acc_dome_r * 0.3 * np.sin(np.radians(a))) for a in theta_acc]
ax.fill(acc_dome_x, acc_dome_z, fc=C_ACC, ec=C_FRAME, lw=1.2, alpha=0.8, zorder=5)

ax.text(sx(acc_cx), sz(ACC_Z + ACC_H / 2), "ACC-01",
        ha="center", va="center", fontsize=6, fontweight="bold",
        color="white", zorder=6)


# ── Ball valve helper ────────────────────────────────────────────────────────
BV_R = 18  # valve symbol radius

def draw_ball_valve(ax, bvx, bvz, label):
    """Draw a ball valve diamond symbol at (bvx, bvz) in mm."""
    pts_x = [sx(bvx), sx(bvx + BV_R), sx(bvx), sx(bvx - BV_R)]
    pts_z = [sz(bvz + BV_R), sz(bvz), sz(bvz - BV_R), sz(bvz)]
    poly = plt.Polygon(list(zip(pts_x, pts_z)),
                        fc=C_VALVE, ec=C_FRAME, lw=1.5, alpha=0.8, zorder=9)
    ax.add_patch(poly)
    ax.text(sx(bvx), sz(bvz), "BV", ha="center", va="center",
            fontsize=4, fontweight="bold", color="white", zorder=10)


# ── BV-01 Ball Valve (Blue supply inlet) ────────────────────────────────────
# On the Blue suction line — inline between IBC entry and P-01 inlet
BV01_X = FRAME_X + FRAME_W + 80   # to the right of frame (higher X = IBC side)
BV01_Z = p01_port_z               # at P-01 port height

draw_ball_valve(ax, BV01_X, BV01_Z, "BV-01")
place_label(ax, sx(BV01_X), sz(BV01_Z + 30), "BV-01\n(1\" BALL)",
            component='valve', fontsize=5, color=C_TEXT,
            dx=0, dy=1.2, ha='center', va='bottom')


# ── BV-02 Ball Valve (Blue supply outlet) ───────────────────────────────────
# Post-ACC-01, controls discharge to spray bar — at a different height
# Route: P-01 out → ACC-01 → up → BV-02 → spray bar exit (higher X)
BV02_X = FRAME_X + FRAME_W + 80   # same X column as BV-01
BV02_Z = FRAME_Z_HI + 60          # above the frame, separate from BV-01

draw_ball_valve(ax, BV02_X, BV02_Z, "BV-02")
place_label(ax, sx(BV02_X), sz(BV02_Z + 30), "BV-02\n(1\" BALL)",
            component='valve', fontsize=5, color=C_TEXT,
            dx=0, dy=1.2, ha='center', va='bottom')


# ═══════════════════════════════════════════════════════════════════════════════
# PIPE CONNECTIONS
# Suction lines enter from higher X (IBC side = LEFT in mirrored view)
# Pump IN port = higher X side of body = p_in = px + PUMP_BODY_W
# Pump OUT port = lower X side of body = p_out = px
# ═══════════════════════════════════════════════════════════════════════════════

PIPE_EXIT_X = FRAME_X + FRAME_W + 200  # where pipes enter/exit to higher X (IBC side)
PIPE_ENTRY_X = FRAME_X - 150           # where pipes exit to lower X (cargo door side)

# ── Blue supply chain: IBC → BV-01 → P-01 → ACC-01 → BV-02 → spray bar ────

# Blue suction: from IBC (high X) → BV-01
draw_pipe_path(ax,
    [PIPE_EXIT_X, BV01_X + BV_R],
    [BV01_Z, BV01_Z],
    OD, WALL, fc=C_BLUE, zorder=6)

# BV-01 → P-01 inlet (P-01 IN is at higher X side = p01_in)
draw_pipe_path(ax,
    [BV01_X - BV_R, p01_in],
    [BV01_Z, p01_port_z],
    OD, WALL, fc=C_BLUE, zorder=6)

# P-01 outlet (lower X side) → down to ACC-01 top
draw_pipe_path(ax,
    [p01_out, acc_cx, acc_cx],
    [p01_port_z, p01_port_z, ACC_Z + ACC_H],
    OD, WALL, fc=C_BLUE, zorder=6)

# ACC-01 bottom → right and up to BV-02
acc_exit_x = ACC_X + ACC_W  # right side of ACC
draw_pipe_path(ax,
    [acc_exit_x, BV02_X, BV02_X],
    [ACC_Z + ACC_H / 2, ACC_Z + ACC_H / 2, BV02_Z - BV_R],
    OD, WALL, fc=C_BLUE, zorder=6)

# BV-02 → spray bar exit (higher X)
draw_pipe_path(ax,
    [BV02_X + BV_R, PIPE_EXIT_X],
    [BV02_Z, BV02_Z],
    OD, WALL, fc=C_BLUE, zorder=6)


# ── Brown recycle: IBC-3 → P-02 → riser to filter skid ─────────────────────

# Brown suction from higher X → P-02 inlet (p02_in = higher X side)
BROWN_ENTRY_Z = p02_port_z
draw_pipe_path(ax,
    [PIPE_EXIT_X, p02_in],
    [BROWN_ENTRY_Z, BROWN_ENTRY_Z],
    OD, WALL, fc=C_BROWN, zorder=6)

# P-02 outlet (lower X) → riser going up to filter skid
RISER_EXIT_Z = 780
draw_pipe_path(ax,
    [p02_out, p02_out],
    [p02_port_z, RISER_EXIT_Z],
    OD, WALL, fc=C_BROWN, zorder=6)

# Riser exit arrow and annotation
ax.annotate("", xy=(sx(p02_out), sz(RISER_EXIT_Z)),
            xytext=(sx(p02_out), sz(RISER_EXIT_Z - 60)),
            arrowprops=dict(arrowstyle="-|>", color=C_BROWN, lw=1.5), zorder=10)
ax.text(sx(p02_out), sz(RISER_EXIT_Z + 10),
        "TO FILTER SKID\n(F1 → F2 → F3)", ha="center", va="bottom",
        fontsize=5.5, color=C_BROWN, style="italic", fontweight="bold")


# ── Waste: IBC-4 → P-03 → external drain ───────────────────────────────────

# Waste suction from higher X → P-03 inlet (p03_in = higher X side)
draw_pipe_path(ax,
    [PIPE_EXIT_X, p03_in],
    [p03_port_z, p03_port_z],
    OD, WALL, fc=C_BLACK_SYS, zorder=6)

# P-03 outlet (lower X) → external drain port (lower X direction)
draw_pipe_path(ax,
    [p03_out, PIPE_ENTRY_X],
    [p03_port_z, p03_port_z],
    OD, WALL, fc=C_BLACK_SYS, zorder=6)

# Drain exit annotation (lower X = right in mirrored view)
ax.text(sx(PIPE_ENTRY_X - 5), sz(p03_port_z),
        "TO EXT.\nDRAIN PORT →", ha="left", va="center",
        fontsize=5.5, color=C_BLACK_SYS, style="italic", fontweight="bold")


# ── Tray drain: sump → P-04 → DV-02 → IBC-3 or IBC-4 ──────────────────────

# Suction from tray sump (below, same X zone) → P-04 inlet (higher X side)
SUMP_ENTRY_Z = 50
draw_pipe_path(ax,
    [p04_in, p04_in],
    [SUMP_ENTRY_Z, p04_port_z],
    OD, WALL, fc=C_BLACK_SYS, zorder=6)

# Sump entry annotation
ax.annotate("", xy=(sx(p04_in), sz(SUMP_ENTRY_Z)),
            xytext=(sx(p04_in), sz(SUMP_ENTRY_Z + 50)),
            arrowprops=dict(arrowstyle="-|>", color=C_BLACK_SYS, lw=1.5), zorder=10)
ax.text(sx(p04_in), sz(SUMP_ENTRY_Z - 10),
        "FROM TRAY\nSUMP", ha="center", va="top",
        fontsize=5.5, color=C_BLACK_SYS, style="italic")

# P-04 outlet (lower X) → DV-02 diverter
# DV-02 is below the manifold frame (lower X, below frame)
DV02_X = FRAME_X + FRAME_W / 2   # centered in X
DV02_Z = FRAME_Z_LO - 60         # below frame
DV02_R = 20

draw_pipe_path(ax,
    [p04_out, p04_out, DV02_X],
    [p04_port_z, DV02_Z, DV02_Z],
    OD, WALL, fc=C_BROWN, zorder=6)

# DV-02 symbol (diamond)
dv02_pts_x = [sx(DV02_X), sx(DV02_X + DV02_R), sx(DV02_X), sx(DV02_X - DV02_R)]
dv02_pts_z = [sz(DV02_Z + DV02_R), sz(DV02_Z), sz(DV02_Z - DV02_R), sz(DV02_Z)]
dv02_poly = plt.Polygon(list(zip(dv02_pts_x, dv02_pts_z)),
                         fc="white", ec=C_FRAME, lw=2.0, zorder=9)
ax.add_patch(dv02_poly)
ax.text(sx(DV02_X), sz(DV02_Z), "3W", ha="center", va="center",
        fontsize=4, fontweight="bold", color=C_FRAME, zorder=10)

# DV-02 outputs
# Right (higher X) → Brown (IBC-3)
draw_pipe_path(ax,
    [DV02_X + DV02_R, DV02_X + DV02_R + 80],
    [DV02_Z, DV02_Z],
    OD, WALL, fc=C_BROWN, zorder=6)
ax.text(sx(DV02_X + DV02_R + 90), sz(DV02_Z + 10), "← BROWN (IBC-3)",
        ha="right", va="bottom", fontsize=5, color=C_BROWN, fontweight="bold")

# Left (lower X) → Black (IBC-4)
draw_pipe_path(ax,
    [DV02_X - DV02_R, DV02_X - DV02_R - 80],
    [DV02_Z, DV02_Z],
    OD, WALL, fc=C_BLACK_SYS, zorder=6)
ax.text(sx(DV02_X - DV02_R - 90), sz(DV02_Z + 10), "BLACK (IBC-4) →",
        ha="left", va="bottom", fontsize=5, color=C_BLACK_SYS, fontweight="bold")

# DV-02 label
place_label(ax, sx(DV02_X), sz(DV02_Z - 25), "DV-02\n(3-WAY DIVERTER)",
            component='diverter', fontsize=5.5, color=C_TEXT,
            dx=0, dy=-2.0, ha='center', va='top')


# ── Flow direction arrows ────────────────────────────────────────────────────
arrow_style = dict(arrowstyle="-|>", lw=1.5, mutation_scale=10)

# Blue supply arrow (incoming from higher X toward P-01)
mid_blue_in = (PIPE_EXIT_X + BV01_X) / 2
ax.annotate("", xy=(sx(mid_blue_in - 30), sz(BV01_Z)),
            xytext=(sx(mid_blue_in + 30), sz(BV01_Z)),
            arrowprops=dict(**arrow_style, color=C_BLUE), zorder=12)

# Blue discharge arrow (outgoing to higher X)
mid_blue_out = (BV02_X + PIPE_EXIT_X) / 2
ax.annotate("", xy=(sx(mid_blue_out + 30), sz(BV02_Z)),
            xytext=(sx(mid_blue_out - 30), sz(BV02_Z)),
            arrowprops=dict(**arrow_style, color=C_BLUE), zorder=12)

# Brown suction arrow (incoming from higher X)
mid_brown = (PIPE_EXIT_X + p02_in) / 2
ax.annotate("", xy=(sx(mid_brown - 30), sz(BROWN_ENTRY_Z)),
            xytext=(sx(mid_brown + 30), sz(BROWN_ENTRY_Z)),
            arrowprops=dict(**arrow_style, color=C_BROWN), zorder=12)


# ── Pipe entry/exit annotations ──────────────────────────────────────────────
# Blue supply label at entry (higher X side)
ax.text(sx(PIPE_EXIT_X + 5), sz(BV01_Z + 15),
        "FROM IBC-1 & IBC-2\n(BLUE SUPPLY)", ha="right", va="bottom",
        fontsize=5, color=C_BLUE, style="italic")

# Blue discharge label at exit (higher X side)
ax.text(sx(PIPE_EXIT_X + 5), sz(BV02_Z + 15),
        "TO SPRAY BAR\n(BLUE DISCHARGE)", ha="right", va="bottom",
        fontsize=5, color=C_BLUE, style="italic")

# Brown suction label (higher X side)
ax.text(sx(PIPE_EXIT_X + 5), sz(BROWN_ENTRY_Z - 15),
        "FROM IBC-3\n(BROWN RECYCLE)", ha="right", va="top",
        fontsize=5, color=C_BROWN, style="italic")

# Waste suction label (higher X side)
ax.text(sx(PIPE_EXIT_X + 5), sz(p03_port_z + 15),
        "FROM IBC-4\n(WASTE)", ha="right", va="bottom",
        fontsize=5, color=C_BLACK_SYS, style="italic")


# ── Dimensions ───────────────────────────────────────────────────────────────
# Frame width
draw_dim_h(ax, sx(FRAME_X), sx(FRAME_X + FRAME_W), sz(FRAME_Z_LO - 60),
           f"{FRAME_W}mm", offset=0.44)

# Frame height
draw_dim_v(ax, sx(FRAME_X - 100), sz(FRAME_Z_LO), sz(FRAME_Z_HI),
           f"{FRAME_H}mm", offset=0.44)

# Height above floor
draw_dim_v(ax, sx(FRAME_X - 160), sz(0), sz(FRAME_Z_LO),
           f"{FRAME_Z_LO}mm AFF", offset=0.44)

# Pump body width
draw_dim_h(ax, sx(P01_X), sx(P01_X + PUMP_BODY_W), sz(P01_Z + PUMP_BODY_H + 35),
           f"{PUMP_BODY_W}mm", offset=0.25, fs=5.5)


# ── Leader callouts ──────────────────────────────────────────────────────────
# Frame material
leader(ax, sx(FRAME_X + FRAME_W / 2), sz(FRAME_Z_LO),
       sx(FRAME_X + FRAME_W / 2), sz(FRAME_Z_LO - 45),
       "25×25×3 SHS STEEL\nMOUNTING FRAME", fs=5.5)

# Plywood
leader(ax, sx(FRAME_X + FRAME_W / 2 + 50), sz(FRAME_Z_LO + ANGLE_W + 20),
       sx(FRAME_X + FRAME_W / 2 + 50), sz(FRAME_Z_LO - 15),
       "18mm PLYWOOD\nBACKING BOARD", fs=5)

# Accumulator specs
leader(ax, sx(acc_cx), sz(ACC_Z + ACC_H + 15),
       sx(acc_cx - 40), sz(ACC_Z + ACC_H + 80),
       "ACC-01: 1 GAL\n125 PSI, 1/2\" NPT\n(SEAFLO)", fs=5.5)

# Pump spec (general — one callout for all)
leader(ax, sx(P01_X + PUMP_BODY_W / 2), sz(P01_Z + PUMP_BODY_H + 30),
       sx(P01_X + PUMP_BODY_W / 2 - 60), sz(P01_Z + PUMP_BODY_H + 100),
       "ALL PUMPS: SHURFLO 2088\n12V DC, 3.5 GPM, 45 PSI\n1/2\" NPSM PORTS", fs=5.5)

# Wall bracket
leader(ax, sx(FRAME_X - BRACKET_W / 2), sz(FRAME_Z_LO + 40 + BRACKET_H / 2),
       sx(FRAME_X - BRACKET_W / 2 - 80), sz(FRAME_Z_LO + 40 + BRACKET_H / 2 + 50),
       "L-BRACKET\nTO WALL RIB", fs=5)

# Pipe material (on the suction line between BV-01 and IBC exit)
pipe_label_x = (BV01_X + PIPE_EXIT_X) / 2
leader(ax, sx(pipe_label_x), sz(BV01_Z + 8),
       sx(pipe_label_x), sz(BV01_Z + 60),
       "1\" HDPE Sch40\n(OD 33mm, WALL 4mm)", fs=5)


# ── Notes ────────────────────────────────────────────────────────────────────
notes = [
    "1. All pumps: Shurflo 2088-554-144, 12V DC, 3.5 GPM, 45 PSI, self-priming diaphragm.",
    "2. All pipe: 1\" HDPE Sch40 (OD 33mm, wall 4mm). Hose barb push-fit connections.",
    "3. P-01 (Blue): IBC-1/IBC-2 → BV-01 → P-01 → ACC-01 → BV-02 → spray bar.",
    "4. P-02 (Brown): IBC-3 → P-02 → filter skid (F1 → F2 → F3 → DV-01).",
    "5. P-03 (Waste): IBC-4 → P-03 → external 2\" NPT drain port.",
    "6. P-04 (Tray drain): sump pickup → P-04 → DV-02 → IBC-3 (Brown) or IBC-4 (Waste).",
    "7. ACC-01: SeaFlo 1-gallon pressure accumulator, smooths pump cycling.",
    "8. Each pump circuit fused at 10A. Do not run >2 pumps simultaneously without load check.",
]
for i, n in enumerate(notes):
    fig.text(0.04, 0.10 - i * 0.018, n, fontsize=6.5, color=C_TEXT,
             fontfamily="monospace", va="top")


# ═══════════════════════════════════════════════════════════════════════════════
# DETAIL A — PUMP MOUNTING CROSS-SECTION (~1:2)
# Side elevation (vertical section perpendicular to pinhole wall)
# Yd horizontal (wall at left), Z vertical
# Shows: corrugated wall → 18mm ply → pump bracket → pump body → ports
# ═══════════════════════════════════════════════════════════════════════════════

SC_A = 2.0  # mm per drawing unit for detail
OAY = 3.0   # Yd origin
OAZ = 4.0   # Z origin

def sa_y(yd_mm):
    return OAY + yd_mm / SC_A

def sa_z(z_mm):
    return OAZ + z_mm / SC_A

# Detail limits
ax2.set_xlim(sa_y(-25) - 0.5, sa_y(220) + 1)
ax2.set_ylim(sa_z(-100) - 0.5, sa_z(130) + 1)

# Detail title
ax2.text(sa_y(100), sa_z(120), "DETAIL A — PUMP MOUNTING\nCROSS-SECTION (APPROX 1:2)",
         ha="center", va="top", fontsize=9, fontweight="bold",
         color="#1A237E", zorder=10)

# All Z coordinates below are relative to pump port center

# ── 1. Container corrugated wall (section fill) ─────────────────────────────
WALL_T = 2.0
ax2.add_patch(plt.Rectangle((sa_y(-WALL_T), sa_z(-90)),
              WALL_T / SC_A, 200 / SC_A,
              fc=C_STEEL_FILL, ec=C_FRAME, lw=1.8, zorder=3, hatch="//"))
ax2.text(sa_y(-WALL_T / 2), sa_z(105), "WALL", ha="center", va="bottom",
         fontsize=5.5, color=C_FRAME)

# ── 2. Plywood backing board (18mm) ─────────────────────────────────────────
PLY_YD_START = 0
PLY_THICK = 18
ax2.add_patch(plt.Rectangle((sa_y(PLY_YD_START), sa_z(-90)),
              PLY_THICK / SC_A, 200 / SC_A,
              fc=C_PLY, ec="#A09060", lw=1.5, zorder=3))
# Wood grain
for gz in range(-85, 100, 12):
    ax2.plot([sa_y(PLY_YD_START + 2), sa_y(PLY_YD_START + PLY_THICK - 2)],
             [sa_z(gz), sa_z(gz + 2)],
             color="#C0B080", lw=0.4, zorder=3.5)

draw_dim_h(ax2, sa_y(PLY_YD_START), sa_y(PLY_YD_START + PLY_THICK),
           sa_z(-50), "18mm", offset=0.33, fs=5.5)

# ── 3. Pump mounting bracket (steel L-bracket) ──────────────────────────────
BRACKET_YD = PLY_YD_START + PLY_THICK
BRACKET_THICK_A = 3
BRACKET_VIS_H = 70  # visible height of bracket vertical leg

# Vertical leg (bolted to ply)
ax2.add_patch(plt.Rectangle((sa_y(BRACKET_YD), sa_z(-BRACKET_VIS_H / 2)),
              BRACKET_THICK_A / SC_A, BRACKET_VIS_H / SC_A,
              fc="#999999", ec=C_FRAME, lw=1.2, zorder=5))

# Horizontal leg (pump sits on this)
BRACKET_HORIZ_LEN = 40
BRACKET_HORIZ_Z = -BRACKET_VIS_H / 2
ax2.add_patch(plt.Rectangle((sa_y(BRACKET_YD), sa_z(BRACKET_HORIZ_Z - BRACKET_THICK_A)),
              BRACKET_HORIZ_LEN / SC_A, BRACKET_THICK_A / SC_A,
              fc="#999999", ec=C_FRAME, lw=1.2, zorder=5))

# ── M6 bolt through bracket + ply ───────────────────────────────────────────
BOLT_Z_A = 0
bolt_y_head = BRACKET_YD + BRACKET_THICK_A
bolt_y_tip = PLY_YD_START - 2

ax2.plot([sa_y(bolt_y_tip), sa_y(bolt_y_head)],
         [sa_z(BOLT_Z_A), sa_z(BOLT_Z_A)],
         color=C_FRAME, lw=1.8, zorder=6)

# Bolt head
ax2.add_patch(plt.Rectangle((sa_y(bolt_y_head), sa_z(BOLT_Z_A - 4)),
              5 / SC_A, 8 / SC_A,
              fc="#666666", ec=C_FRAME, lw=1.0, zorder=7))

# Nut on back
ax2.add_patch(plt.Rectangle((sa_y(bolt_y_tip - 3), sa_z(BOLT_Z_A - 5)),
              3 / SC_A, 10 / SC_A,
              fc="#666666", ec=C_FRAME, lw=1.0, zorder=7))

leader(ax2, sa_y(bolt_y_head + 3), sa_z(BOLT_Z_A),
       sa_y(bolt_y_head + 35), sa_z(BOLT_Z_A - 25),
       "M6×40 BOLT\n+ NYLOC NUT", fs=5)

# ── 4. Pump body (cross-section) ────────────────────────────────────────────
PUMP_YD = BRACKET_YD + BRACKET_THICK_A + 5  # small gap
PUMP_DEPTH = 100   # depth in Yd direction
PUMP_SEC_H = 85    # height in section

# Pump body rectangle
ax2.add_patch(plt.Rectangle((sa_y(PUMP_YD), sa_z(-PUMP_SEC_H / 2 + 10)),
              PUMP_DEPTH / SC_A, PUMP_SEC_H / SC_A,
              fc=C_PUMP_BODY, ec=C_FRAME, lw=1.8, alpha=0.85, zorder=5))

ax2.text(sa_y(PUMP_YD + PUMP_DEPTH / 2), sa_z(10),
         "PUMP\nBODY", ha="center", va="center",
         fontsize=6, color="white", fontweight="bold", zorder=6)

# Diaphragm chamber indication (internal circle)
chamber_cx = PUMP_YD + PUMP_DEPTH / 2
chamber_cz = 10
chamber_r = 25
ax2.add_patch(plt.Circle((sa_y(chamber_cx), sa_z(chamber_cz)), chamber_r / SC_A,
              fc="#D0A070", ec="#8B5E3C", lw=1.0, alpha=0.5, zorder=5.5))
ax2.text(sa_y(chamber_cx), sa_z(chamber_cz - 12), "DIAPHRAGM",
         ha="center", va="top", fontsize=4, color="#8B5E3C", zorder=6)

# Motor dome (top)
motor_z_bot = -PUMP_SEC_H / 2 + 10 + PUMP_SEC_H
motor_h = 30
ax2.add_patch(plt.Rectangle((sa_y(PUMP_YD + 15), sa_z(motor_z_bot)),
              (PUMP_DEPTH - 30) / SC_A, motor_h / SC_A,
              fc="#CC8844", ec=C_FRAME, lw=1.2, alpha=0.85, zorder=5))
ax2.text(sa_y(PUMP_YD + PUMP_DEPTH / 2), sa_z(motor_z_bot + motor_h / 2),
         "MOTOR", ha="center", va="center",
         fontsize=5, color="white", fontweight="bold", zorder=6)

# ── 5. Port stubs (1/2" NPSM) ──────────────────────────────────────────────
PORT_YD = PUMP_YD + PUMP_DEPTH  # port exits front face
PORT_OD_SEC = 21   # 1/2" pipe OD ~21mm
PORT_WALL_SEC = 3
PORT_Z_SEC = 0

# Port bore through pump body
ax2.add_patch(plt.Rectangle((sa_y(PORT_YD - 10), sa_z(PORT_Z_SEC - PORT_OD_SEC / 2)),
              10 / SC_A, PORT_OD_SEC / SC_A,
              fc="white", ec=C_FRAME, lw=1.0, zorder=6))

# Hose barb fitting
BARB_LEN = 35
# Outer wall
ax2.add_patch(plt.Rectangle((sa_y(PORT_YD), sa_z(PORT_Z_SEC - PORT_OD_SEC / 2)),
              BARB_LEN / SC_A, PORT_OD_SEC / SC_A,
              fc=C_STEEL_FILL, ec=C_FRAME, lw=1.0, zorder=5))
# Inner bore
ax2.add_patch(plt.Rectangle(
    (sa_y(PORT_YD), sa_z(PORT_Z_SEC - PORT_OD_SEC / 2 + PORT_WALL_SEC)),
    BARB_LEN / SC_A, (PORT_OD_SEC - 2 * PORT_WALL_SEC) / SC_A,
    fc="white", ec="none", zorder=6))

# Barb ridges
for bx in range(10, BARB_LEN, 8):
    barb_yd = PORT_YD + bx
    ax2.plot([sa_y(barb_yd), sa_y(barb_yd + 3)],
             [sa_z(PORT_Z_SEC - PORT_OD_SEC / 2 - 2), sa_z(PORT_Z_SEC - PORT_OD_SEC / 2)],
             color=C_FRAME, lw=0.8, zorder=6)
    ax2.plot([sa_y(barb_yd), sa_y(barb_yd + 3)],
             [sa_z(PORT_Z_SEC + PORT_OD_SEC / 2 + 2), sa_z(PORT_Z_SEC + PORT_OD_SEC / 2)],
             color=C_FRAME, lw=0.8, zorder=6)

leader(ax2, sa_y(PORT_YD + BARB_LEN), sa_z(PORT_Z_SEC),
       sa_y(PORT_YD + BARB_LEN + 25), sa_z(PORT_Z_SEC + 25),
       "1/2\" NPSM\nHOSE BARB\n→ 1\" HDPE", fs=5)

# ── Overall standoff dimension ───────────────────────────────────────────────
total_standoff = PLY_THICK + BRACKET_THICK_A + 5  # 18 + 3 + 5 = 26mm
draw_dim_h(ax2, sa_y(PLY_YD_START), sa_y(PUMP_YD),
           sa_z(-75), f"{int(PUMP_YD)}mm\nSTANDOFF", offset=0.33, fs=5.5)

# Pump depth dimension
draw_dim_h(ax2, sa_y(PUMP_YD), sa_y(PUMP_YD + PUMP_DEPTH),
           sa_z(-75), f"{PUMP_DEPTH}mm\nPUMP DEPTH", offset=0.33, fs=5.5)

# ── Component labels along section ──────────────────────────────────────────
label_z_a = 100
label_items = [
    (PLY_YD_START + PLY_THICK / 2, "18mm PLY"),
    (BRACKET_YD + BRACKET_THICK_A / 2, "BRACKET"),
    (PUMP_YD + PUMP_DEPTH / 2, "SHURFLO 2088"),
]
for ly, ltxt in label_items:
    ax2.text(sa_y(ly), sa_z(label_z_a), ltxt, ha="center", va="bottom",
             fontsize=5, color=C_FRAME)
    ax2.plot([sa_y(ly), sa_y(ly)], [sa_z(label_z_a - 5), sa_z(motor_z_bot + motor_h + 2)],
             color=C_DIM, lw=0.5, ls=":", zorder=2)

# Section cut indicator note
ax2.text(sa_y(100), sa_z(-95),
         "SECTION THROUGH PUMP CENTER\nPERPENDICULAR TO WALL AT PORT HEIGHT",
         ha="center", va="top", fontsize=6, color="#666666", style="italic")


# ═══════════════════════════════════════════════════════════════════════════════
# DETAIL B — PLAN VIEW (PUMP MANIFOLD ONLY)
# View from ceiling looking down at the manifold zone
# X horizontal (mirrored to match elevation), Yd vertical (wall at top)
# Shows: 4 pumps from above, ACC-01, BV-01/BV-02, DV-02, pipe stubs with
#        direction arrows indicating where each pipe routes to
# ═══════════════════════════════════════════════════════════════════════════════

SC_B = 3.0    # mm per drawing unit (1:3 — large detail of manifold zone)
OBX = 2.0     # X origin offset
OBY = 1.5     # Yd origin offset

def sp_x(x_mm):
    """Convert X position (mm) to plan view x coordinate."""
    return OBX + (x_mm - PUMP_X + 200) / SC_B

def sp_y(yd_mm):
    """Convert Yd position (mm) to plan view y coordinate (Yd=0 at top)."""
    return OBY + (500 - yd_mm) / SC_B  # flip so wall (Yd=0) is at top

# Set axis limits — focus on X=2200–3100, Yd=-50 to 500
ax3.set_xlim(sp_x(2150) - 1, sp_x(3150) + 1)
ax3.set_ylim(sp_y(550) - 1, sp_y(-120) + 1)

# Mirror X to match elevation convention (high X on left)
ax3.invert_xaxis()

# Detail title
ax3.text(sp_x(2650), sp_y(-80),
         "DETAIL B — PUMP MANIFOLD PLAN VIEW\nLOOKING DOWN FROM CEILING  |  SCALE ~1:3",
         ha="center", va="top", fontsize=9, fontweight="bold",
         color="#1A237E", zorder=10)

# ── Pinhole wall (Yd=0) ─────────────────────────────────────────────────────
ax3.plot([sp_x(2150), sp_x(3150)], [sp_y(0), sp_y(0)],
         color=C_FRAME, lw=3.0, zorder=3)
ax3.text(sp_x(2200), sp_y(-15), "PINHOLE WALL (Yd=0)", ha="left", va="top",
         fontsize=7, color=C_FRAME, fontweight="bold")

# Corrugation ribs at Yd=0 (wall detail)
for rib_x in range(2285, 3100, CORR_SPACING):
    ax3.plot([sp_x(rib_x), sp_x(rib_x)], [sp_y(-5), sp_y(5)],
             color="#AAAAAA", lw=1.5, zorder=2)

# ── Near walkway edge (Yd=300) ──────────────────────────────────────────────
ax3.plot([sp_x(2150), sp_x(3150)], [sp_y(WALKWAY_W), sp_y(WALKWAY_W)],
         color="#BBBBBB", lw=1.0, ls="--", zorder=2)
ax3.text(sp_x(3100), sp_y(WALKWAY_W + 10), "WALKWAY EDGE (Yd=300)",
         ha="right", va="top", fontsize=5.5, color="#999999", style="italic")

# ── Mounting frame footprint (plan view) ────────────────────────────────────
# Frame sits against wall, depth = 18mm ply + pump body depth (~120mm total)
MANIFOLD_DEPTH = 130  # Yd depth from wall (ply + bracket + pump body)
# Frame perimeter
ax3.add_patch(plt.Rectangle(
    (sp_x(FRAME_X), sp_y(MANIFOLD_DEPTH)),
    FRAME_W / SC_B, MANIFOLD_DEPTH / SC_B,
    fc=C_PLY, ec=C_FRAME, lw=2.0, alpha=0.4, zorder=3))

# Frame label
ax3.text(sp_x(FRAME_X + FRAME_W / 2), sp_y(MANIFOLD_DEPTH + 10),
         f"MOUNTING FRAME\n{FRAME_W}×{MANIFOLD_DEPTH}mm", ha="center", va="top",
         fontsize=6, color=C_FRAME, style="italic")

# ── Four pumps from above ───────────────────────────────────────────────────
# Pump plan dimensions (Shurflo 2088 from above: ~190mm long × 100mm wide)
PP_W = 90     # pump plan width in X (shorter in plan than elevation)
PP_D = 50     # pump plan depth in Yd
PP_PORT_R = 8  # port circle radius

# Pumps are stacked vertically (Z): P-01 above P-03, P-02 above P-04.
# In plan view (looking down) only top-row pumps are visible; bottom-row
# are ghosted (dashed outline, faded fill) offset slightly in Yd.
GHOST_ALPHA = 0.2
GHOST_LW = 1.0
GHOST_LS = (0, (4, 3))  # dashed
GHOST_YD_OFFSET = 8     # slight offset so ghost outline peeks out

# Top row (solid — visible from above)
pumps_solid = [
    (P01_X + PUMP_BODY_W / 2, 25,  "P-01", C_BLUE,       "BLUE SUPPLY"),
    (P02_X + PUMP_BODY_W / 2, 25,  "P-02", C_BROWN,      "BROWN RECYCLE"),
]
# Bottom row (ghost — hidden below top row)
pumps_ghost = [
    (P03_X + PUMP_BODY_W / 2, 25 + GHOST_YD_OFFSET, "P-03", C_BLACK_SYS,  "WASTE EVAC\n(BELOW P-01)"),
    (P04_X + PUMP_BODY_W / 2, 25 + GHOST_YD_OFFSET, "P-04", C_BLACK_SYS,  "TRAY DRAIN\n(BELOW P-02)"),
]

# Draw ghost pumps first (lower zorder)
for pcx, pyd, plabel, pcolor, psub in pumps_ghost:
    ax3.add_patch(plt.Rectangle(
        (sp_x(pcx - PP_W / 2), sp_y(pyd + PP_D)),
        PP_W / SC_B, PP_D / SC_B,
        fc=pcolor, ec=pcolor, lw=GHOST_LW, alpha=GHOST_ALPHA,
        ls=GHOST_LS, zorder=3))
    ax3.text(sp_x(pcx), sp_y(pyd + PP_D / 2),
             plabel, ha="center", va="center",
             fontsize=6, color=pcolor, fontweight="bold", alpha=0.4, zorder=4)
    # Ports — ghost
    in_x = pcx + PP_W / 2
    out_x = pcx - PP_W / 2
    port_yd = pyd + PP_D / 2
    ax3.add_patch(plt.Circle((sp_x(in_x), sp_y(port_yd)), PP_PORT_R / SC_B,
                  fc="white", ec=pcolor, lw=0.8, alpha=GHOST_ALPHA, zorder=3))
    ax3.add_patch(plt.Circle((sp_x(out_x), sp_y(port_yd)), PP_PORT_R / SC_B,
                  fc="white", ec=pcolor, lw=0.8, alpha=GHOST_ALPHA, zorder=3))

# Draw solid pumps on top
for pcx, pyd, plabel, pcolor, psub in pumps_solid:
    ax3.add_patch(plt.Rectangle(
        (sp_x(pcx - PP_W / 2), sp_y(pyd + PP_D)),
        PP_W / SC_B, PP_D / SC_B,
        fc=pcolor, ec=C_FRAME, lw=1.2, alpha=0.8, zorder=5))
    ax3.text(sp_x(pcx), sp_y(pyd + PP_D / 2),
             plabel, ha="center", va="center",
             fontsize=7, color="white", fontweight="bold", zorder=6)
    ax3.text(sp_x(pcx), sp_y(pyd + PP_D + 8),
             psub, ha="center", va="top",
             fontsize=4.5, color=pcolor, fontweight="bold", zorder=6)
    # Ports — solid
    in_x = pcx + PP_W / 2
    out_x = pcx - PP_W / 2
    port_yd = pyd + PP_D / 2
    ax3.add_patch(plt.Circle((sp_x(in_x), sp_y(port_yd)), PP_PORT_R / SC_B,
                  fc="white", ec=C_FRAME, lw=1.0, zorder=7))
    ax3.add_patch(plt.Circle((sp_x(out_x), sp_y(port_yd)), PP_PORT_R / SC_B,
                  fc="white", ec=C_FRAME, lw=1.0, zorder=7))
    ax3.text(sp_x(in_x), sp_y(port_yd), "IN", ha="center", va="center",
             fontsize=3.5, fontweight="bold", color=C_FRAME, zorder=8)
    ax3.text(sp_x(out_x), sp_y(port_yd), "OUT", ha="center", va="center",
             fontsize=3.5, fontweight="bold", color=C_FRAME, zorder=8)

# ── ACC-01 from above ───────────────────────────────────────────────────────
# Circular pressure tank between pump rows
ACC_PLAN_R = 30   # tank radius in plan
acc_plan_cx = FRAME_X + FRAME_W / 2
acc_plan_cy = 25 + PP_D / 2         # at pump row center Yd
ax3.add_patch(plt.Circle((sp_x(acc_plan_cx), sp_y(acc_plan_cy)),
              ACC_PLAN_R / SC_B, fc=C_ACC, ec=C_FRAME, lw=1.5, alpha=0.8, zorder=5))
ax3.text(sp_x(acc_plan_cx), sp_y(acc_plan_cy), "ACC-01",
         ha="center", va="center", fontsize=5.5, fontweight="bold",
         color="white", zorder=6)

# ── Valve position constants (needed before pipe routing) ──────────────────
bv01_plan_x = FRAME_X + FRAME_W + 50   # 2850
bv01_plan_yd = 35
bv_plan_r = 12
bv02_plan_x = FRAME_X + FRAME_W + 50   # 2850
bv02_plan_yd = 115
dv02_plan_x = FRAME_X - 50             # 2450
dv02_plan_yd = 95
dv_plan_r = 14

# ── Pipe routing — parallel-wall pipes (plan view) ─────────────────────────
# Adapted from draw_pipe_path() to use plan-view coordinate transforms sp_x/sp_y.
# x_pts/yd_pts are in mm; OD/WALL in mm; elbow_r auto-calculated.

def draw_pipe_path_plan(ax_p, x_pts, yd_pts, od_mm, wall_mm,
                        fc=C_HDPE, ec=C_FRAME, bore_fc="white",
                        elbow_r=None, zorder=8):
    """Draw a pipe run with parallel walls in plan view."""
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
        dy = yd_pts[i + 1] - yd_pts[i]
        length = max(math.hypot(dx, dy), 1e-6)
        segs.append((dx / length, dy / length, length))

    elbows = []
    for i in range(1, n - 1):
        d1x, d1y, _ = segs[i - 1]
        d2x, d2y, _ = segs[i]
        cos_a = max(-1.0, min(1.0, d1x * d2x + d1y * d2y))
        alpha = math.acos(cos_a)
        turn = math.pi - alpha
        if turn < 0.01:
            elbows.append(None)
            continue
        tangent = elbow_r * math.tan(turn / 2)
        max_t = 0.4 * min(segs[i - 1][2], segs[i][2])
        if tangent > max_t:
            tangent = max_t
        cross = d1x * d2y - d1y * d2x
        if cross > 0:
            nx, ny = -d1y, d1x
        else:
            nx, ny = d1y, -d1x
        tp_x = x_pts[i] - d1x * tangent
        tp_y = yd_pts[i] - d1y * tangent
        r_eff = tangent / math.tan(turn / 2) if turn > 0.01 else elbow_r
        cy = tp_x + nx * r_eff
        cy_e = tp_y + ny * r_eff
        start_a = math.atan2(tp_y - cy_e, tp_x - cy)
        sweep = turn if cross > 0 else -turn
        elbows.append({
            'tangent': tangent, 'r': r_eff,
            'center': (cy, cy_e), 'start': start_a, 'sweep': sweep,
        })

    def _rect_plan(sx0, sy0, sx1, sy1, nx, ny, half_r, color, z_ord):
        pts = [(sp_x(sx0 + nx * half_r), sp_y(sy0 + ny * half_r)),
               (sp_x(sx1 + nx * half_r), sp_y(sy1 + ny * half_r)),
               (sp_x(sx1 - nx * half_r), sp_y(sy1 - ny * half_r)),
               (sp_x(sx0 - nx * half_r), sp_y(sy0 - ny * half_r))]
        ax_p.fill([p[0] for p in pts], [p[1] for p in pts],
                  fc=color, ec=ec if color != bore_fc else "none",
                  lw=0.8 if color != bore_fc else 0, zorder=z_ord)

    for i in range(len(segs)):
        dx, dy, seg_len = segs[i]
        nx, ny = -dy, dx
        trim_s = elbows[i - 1]['tangent'] if (i > 0 and elbows[i - 1]) else 0
        trim_e = elbows[i]['tangent'] if (i < len(elbows) and elbows[i]) else 0
        p0x = x_pts[i] + dx * trim_s
        p0y = yd_pts[i] + dy * trim_s
        p1x = x_pts[i + 1] - dx * trim_e
        p1y = yd_pts[i + 1] - dy * trim_e
        remaining = seg_len - trim_s - trim_e
        if remaining < 0.5:
            continue
        _rect_plan(p0x, p0y, p1x, p1y, nx, ny, half_od, fc, zorder)
        _rect_plan(p0x, p0y, p1x, p1y, nx, ny, half_id, bore_fc, zorder + 1)

    for elb in elbows:
        if elb is None:
            continue
        cy, cy_e = elb['center']
        r_eff = elb['r']
        sa = elb['start']
        sw = elb['sweep']
        n_arc = max(20, int(abs(sw) / 0.04))
        angles = [sa + sw * t / n_arc for t in range(n_arc + 1)]

        def _arc_ring_plan(r_out, r_in, color, z_ord,
                           _cy=cy, _ce=cy_e, _angles=angles):
            ox_ = [sp_x(_cy + r_out * math.cos(a)) for a in _angles]
            oy_ = [sp_y(_ce + r_out * math.sin(a)) for a in _angles]
            ix_ = [sp_x(_cy + r_in * math.cos(a)) for a in _angles]
            iy_ = [sp_y(_ce + r_in * math.sin(a)) for a in _angles]
            ax_p.fill(ox_ + ix_[::-1], oy_ + iy_[::-1],
                      fc=color, ec=ec if color != bore_fc else "none",
                      lw=0.8 if color != bore_fc else 0, zorder=z_ord)

        _arc_ring_plan(r_eff + half_od, max(r_eff - half_od, 0.5), fc, zorder)
        _arc_ring_plan(r_eff + half_id, max(r_eff - half_id, 0.5), bore_fc, zorder + 1)


# ── Plan-view pipe routing ─────────────────────────────────────────────────
# Compute pump port positions in plan view (mm)
# IN port = higher X side, OUT port = lower X side; port_yd = center of pump body
p01_cx = P01_X + PUMP_BODY_W / 2   # 2585
p02_cx = P02_X + PUMP_BODY_W / 2   # 2715
p03_cx = P03_X + PUMP_BODY_W / 2   # 2585
p04_cx = P04_X + PUMP_BODY_W / 2   # 2715

p01_in_x  = p01_cx + PP_W / 2      # 2630 (higher X = toward IBCs)
p01_out_x = p01_cx - PP_W / 2      # 2540 (lower X)
p02_in_x  = p02_cx + PP_W / 2      # 2760
p02_out_x = p02_cx - PP_W / 2      # 2670
p03_in_x  = p03_cx + PP_W / 2      # 2630
p03_out_x = p03_cx - PP_W / 2      # 2540
p04_in_x  = p04_cx + PP_W / 2      # 2760
p04_out_x = p04_cx - PP_W / 2      # 2670

ROW_TOP_YD = 25 + PP_D / 2         # 50  — top row port Yd
ROW_BOT_YD = 75 + PP_D / 2         # 100 — bottom row port Yd

# Exit point X for IBC-side pipes (beyond the frame + stub)
EXIT_X_R = 3050   # right exit (toward IBCs)
EXIT_X_L = 2250   # left exit (toward lower X / ext drain)
EXIT_YD_BOT = MANIFOLD_DEPTH + 200  # below frame (from walkway side)

# ── Blue supply: IBC-1/IBC-2 → BV-01 → P-01 IN ───────────────────────────
draw_pipe_path_plan(ax3,
    [EXIT_X_R, bv01_plan_x + bv_plan_r],
    [35, 35],
    OD, WALL, fc=C_BLUE, zorder=4)
# BV-01 → P-01 IN
draw_pipe_path_plan(ax3,
    [bv01_plan_x - bv_plan_r, p01_in_x],
    [35, ROW_TOP_YD],
    OD, WALL, fc=C_BLUE, zorder=4)
# Label at exit
ax3.text(sp_x(EXIT_X_R + 10), sp_y(35),
         "FROM IBC-1/IBC-2\n(BLUE SUPPLY)",
         ha="left", va="center", fontsize=5, color=C_BLUE, fontweight="bold")

# ── Blue discharge: P-01 OUT → ACC-01 → BV-02 → spray bar ────────────────
# P-01 OUT → down to ACC zone → across to ACC
draw_pipe_path_plan(ax3,
    [p01_out_x, p01_out_x, acc_plan_cx - ACC_PLAN_R],
    [ROW_TOP_YD, acc_plan_cy, acc_plan_cy],
    OD, WALL, fc=C_BLUE, zorder=4)
# ACC → right along gap between rows → turn down to BV-02
draw_pipe_path_plan(ax3,
    [acc_plan_cx + ACC_PLAN_R, bv02_plan_x, bv02_plan_x - bv_plan_r],
    [acc_plan_cy, acc_plan_cy, bv02_plan_yd],
    OD, WALL, fc=C_BLUE, zorder=4)
# BV-02 → spray bar exit
draw_pipe_path_plan(ax3,
    [bv02_plan_x + bv_plan_r, EXIT_X_R],
    [ROW_BOT_YD + 15, ROW_BOT_YD + 15],
    OD, WALL, fc=C_BLUE, zorder=4)
# Label at exit
ax3.text(sp_x(EXIT_X_R + 10), sp_y(ROW_BOT_YD + 15),
         "TO SPRAY BAR",
         ha="left", va="center", fontsize=5, color=C_BLUE, fontweight="bold")

# ── Brown suction: IBC-3 → P-02 IN ────────────────────────────────────────
# Route along wall side (Yd=20) to avoid crossing P-01, then turn down to port
draw_pipe_path_plan(ax3,
    [EXIT_X_R, p02_in_x, p02_in_x],
    [20, 20, ROW_TOP_YD],
    OD, WALL, fc=C_BROWN, zorder=4)
ax3.text(sp_x(EXIT_X_R + 10), sp_y(20),
         "FROM IBC-3\n(BROWN SUCTION)",
         ha="left", va="center", fontsize=5, color=C_BROWN, fontweight="bold")

# ── Brown discharge: P-02 OUT → riser to filter skid ──────────────────────
# P-02 outlet goes toward wall (Yd=0) as a vertical riser
draw_pipe_path_plan(ax3,
    [p02_out_x, p02_out_x],
    [ROW_TOP_YD, -20],
    OD, WALL, fc=C_BROWN, zorder=4)
# Riser arrow (going up through floor toward filter skid above)
ax3.annotate("", xy=(sp_x(p02_out_x), sp_y(-30)),
             xytext=(sp_x(p02_out_x), sp_y(-10)),
             arrowprops=dict(arrowstyle="-|>", color=C_BROWN, lw=2.0), zorder=9)
ax3.text(sp_x(p02_out_x), sp_y(-40),
         "RISER TO\nFILTER SKID",
         ha="center", va="top", fontsize=5, color=C_BROWN, fontweight="bold")

# ── Ghost pipes: P-03 and P-04 connections (hidden below top row) ──────────
# These pumps are stacked below P-01/P-02; shown as dashed ghost lines.
GHOST_PIPE_ALPHA = 0.3
GHOST_PIPE_LW = 2.0

def ghost_pipe(x_pts, yd_pts, color):
    """Draw a ghosted pipe as a dashed centerline (not filled parallel walls)."""
    ax3.plot([sp_x(x) for x in x_pts], [sp_y(y) for y in yd_pts],
             color=color, lw=GHOST_PIPE_LW, ls=(0, (5, 4)),
             alpha=GHOST_PIPE_ALPHA, zorder=3)

def ghost_label(x, yd, text, color, ha="left", va="center"):
    ax3.text(sp_x(x), sp_y(yd), text, ha=ha, va=va,
             fontsize=5, color=color, fontweight="bold", alpha=0.4)

# Waste suction: IBC-4 → P-03 IN (ghost)
ghost_pipe([EXIT_X_R, p03_in_x, p03_in_x], [135, 135, ROW_TOP_YD + GHOST_YD_OFFSET], C_BLACK_SYS)
ghost_label(EXIT_X_R + 10, 135, "FROM IBC-4\n(WASTE SUCTION)", C_BLACK_SYS)

# Waste discharge: P-03 OUT → ext drain (ghost)
ghost_pipe([p03_out_x, p03_out_x, EXIT_X_L], [ROW_TOP_YD + GHOST_YD_OFFSET, 140, 140], C_BLACK_SYS)
ghost_label(EXIT_X_L - 10, 140, "TO EXT.\nDRAIN", C_BLACK_SYS, ha="right")

# Tray drain suction: tray sump → P-04 IN (ghost)
ghost_pipe([p04_in_x, p04_in_x], [EXIT_YD_BOT, ROW_TOP_YD + GHOST_YD_OFFSET], C_BLACK_SYS)
ghost_label(p04_in_x + 10, EXIT_YD_BOT + 15, "FROM TRAY\nSUMP", C_BLACK_SYS, ha="left", va="top")

# Tray drain discharge: P-04 OUT → DV-02 → IBC-3/IBC-4 (ghost)
ghost_pipe([p04_out_x, dv02_plan_x + dv_plan_r], [ROW_TOP_YD + GHOST_YD_OFFSET, dv02_plan_yd], C_BROWN)
ghost_pipe([dv02_plan_x - dv_plan_r, EXIT_X_L], [dv02_plan_yd, dv02_plan_yd], C_BROWN)
ghost_label(EXIT_X_L - 10, dv02_plan_yd, "VIA DV-02 TO\nIBC-3 or IBC-4", C_BROWN, ha="right")

# ── BV-01 and BV-02 symbols in plan ─────────────────────────────────────────
# (positions defined above with pipe routing constants)
bv_pts_x = [sp_x(bv01_plan_x), sp_x(bv01_plan_x + bv_plan_r),
            sp_x(bv01_plan_x), sp_x(bv01_plan_x - bv_plan_r)]
bv_pts_y = [sp_y(bv01_plan_yd + bv_plan_r), sp_y(bv01_plan_yd),
            sp_y(bv01_plan_yd - bv_plan_r), sp_y(bv01_plan_yd)]
ax3.add_patch(plt.Polygon(list(zip(bv_pts_x, bv_pts_y)),
              fc=C_VALVE, ec=C_FRAME, lw=1.2, alpha=0.8, zorder=9))
ax3.text(sp_x(bv01_plan_x), sp_y(bv01_plan_yd - 18), "BV-01",
         ha="center", va="top", fontsize=5, color=C_VALVE, fontweight="bold")

# BV-02 on Blue discharge line
bv2_pts_x = [sp_x(bv02_plan_x), sp_x(bv02_plan_x + bv_plan_r),
             sp_x(bv02_plan_x), sp_x(bv02_plan_x - bv_plan_r)]
bv2_pts_y = [sp_y(bv02_plan_yd + bv_plan_r), sp_y(bv02_plan_yd),
             sp_y(bv02_plan_yd - bv_plan_r), sp_y(bv02_plan_yd)]
ax3.add_patch(plt.Polygon(list(zip(bv2_pts_x, bv2_pts_y)),
              fc=C_VALVE, ec=C_FRAME, lw=1.2, alpha=0.8, zorder=9))
ax3.text(sp_x(bv02_plan_x), sp_y(bv02_plan_yd - 18), "BV-02",
         ha="center", va="top", fontsize=5, color=C_VALVE, fontweight="bold")

# ── DV-02 symbol in plan (ghost — on P-04 discharge line) ──────────────────
dv_pts_x = [sp_x(dv02_plan_x), sp_x(dv02_plan_x + dv_plan_r),
            sp_x(dv02_plan_x), sp_x(dv02_plan_x - dv_plan_r)]
dv_pts_y = [sp_y(dv02_plan_yd + dv_plan_r), sp_y(dv02_plan_yd),
            sp_y(dv02_plan_yd - dv_plan_r), sp_y(dv02_plan_yd)]
ax3.add_patch(plt.Polygon(list(zip(dv_pts_x, dv_pts_y)),
              fc="white", ec=C_FRAME, lw=1.0, ls=GHOST_LS,
              alpha=GHOST_ALPHA, zorder=3))
ax3.text(sp_x(dv02_plan_x), sp_y(dv02_plan_yd), "3W",
         ha="center", va="center", fontsize=4, fontweight="bold",
         color=C_FRAME, alpha=0.4, zorder=4)
ax3.text(sp_x(dv02_plan_x), sp_y(dv02_plan_yd - 20), "DV-02",
         ha="center", va="top", fontsize=5, color=C_FRAME,
         fontweight="bold", alpha=0.4)

# ── Dimensions ──────────────────────────────────────────────────────────────
# Frame width
draw_dim_h(ax3, sp_x(FRAME_X), sp_x(FRAME_X + FRAME_W), sp_y(-40),
           f"{FRAME_W}mm", offset=0.33, fs=6)

# Frame depth from wall
draw_dim_v(ax3, sp_x(FRAME_X - 30), sp_y(MANIFOLD_DEPTH), sp_y(0),
           f"{MANIFOLD_DEPTH}mm\nDEPTH", offset=0.33, fs=5.5)


# ── Title block ──────────────────────────────────────────────────────────────
title_block(ax, "SHEET 1 OF 1",
            drawing_title="PUMP MANIFOLD — PLUMBING ELEVATION",
            subtitle="INTERIOR VIEW LOOKING AT PINHOLE WALL (Yd=0) — MATCHES COMBINED ELEVATION",
            scale_note="ELEVATION 1:5  |  DETAIL A ~1:2  |  DETAIL B (PLAN) ~1:3  |  ALL DIMS IN mm",
            doc_id="TBS-001 · Water System — Pump Manifold Detail",
            height=0.05)

# ── Copyright ────────────────────────────────────────────────────────────────
fig.text(0.99, 0.005, "© 2026 Alvin Richards — GNU AGPLv3",
         ha="right", va="bottom", fontsize=6.0, color="#888888", style="italic")

# ── Save ─────────────────────────────────────────────────────────────────────
import os
os.makedirs("diagrams", exist_ok=True)
fig.savefig("diagrams/pump-manifold-sheet1.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
fig.savefig(svg_path("diagrams/pump-manifold-sheet1.png"), bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close(fig)
print("Pump manifold diagram written → diagrams/pump-manifold-sheet1.png")
