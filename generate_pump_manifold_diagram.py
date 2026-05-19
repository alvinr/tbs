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
  Shows: mounting frame, three Shurflo 2088 pumps (P-01, P-02, P-04),
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
    PUMP_PIPE_OD, PUMP_PIPE_WALL,
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

fig = plt.figure(figsize=(26, 18))
fig.patch.set_facecolor(C_BG)
gs = GridSpec(2, 2, figure=fig, width_ratios=[0.35, 0.65],
             height_ratios=[0.9, 1.2], wspace=0.04, hspace=0.06)

ax = fig.add_subplot(gs[:, 1])   # Main elevation — full right column, both rows
ax.set_facecolor(C_BG)
ax.set_aspect("equal")
ax.axis("off")

ax2 = fig.add_subplot(gs[0, 0])  # Detail A — cross-section (top left)
ax2.set_facecolor(C_BG)
ax2.set_aspect("equal")
ax2.axis("off")

ax3 = fig.add_subplot(gs[1, 0])  # Detail B — plan view (bottom left)
ax3.set_facecolor(C_BG)
ax3.set_aspect("equal")
ax3.axis("off")

# Axis limits — elevation panel
ax.set_xlim(sx(2200) - 1, sx(3550) + 1)
ax.set_ylim(sz(-30) - 1, sz(1150) + 2)

# Mirror X axis for interior view convention
ax.invert_xaxis()

# Reset label registry for collision avoidance
reset_label_registry()

# ── Manifold layout constants ────────────────────────────────────────────────
# Matches pinhole-wall-elevation.py pump manifold layout exactly.
# Frame widened 40%; P-04 centered below P-01/P-02; P-03 relocated to IBC corridor.
ANGLE_W = 25   # frame member width (25×25×3mm SHS)
FRAME_LW = 2.0

# Pump body dimensions — VERTICAL ORIENTATION (Shurflo 2088 datasheet)
# Pump stands upright: long axis (218mm) vertical, width (127mm) horizontal
# 127mm is the TOTAL width to the end of the threaded port fittings.
# Ports on head end (top), facing LEFT and RIGHT (81mm apart in X)
PUMP_BODY_W = 127    # 5.00" TOTAL width in X incl. port threads (from datasheet)
PUMP_BODY_H = 218    # 8.60" height in Z (long axis, from datasheet)
PORT_SPACING = 81    # 3.20" between IN and OUT port centers (left-right on head)
PORT_OD = 18         # 1/2" male thread visual diameter

# Frame: widened 40% to separate P-01 and P-02 horizontally
PUMP_GAP_X = 60       # nominal gap (before 40% stretch)
PUMP_MARGIN_X = 20    # margin from frame inner edge to pump body edge
PUMP_MARGIN_Z = 20    # vertical margin inside frame
FRAME_W = int((2 * ANGLE_W + 2 * PUMP_MARGIN_X
               + 2 * PUMP_BODY_W + 1 * PUMP_GAP_X) * 1.4)  # 565mm
FRAME_X = PUMP_X + (PUMP_W - FRAME_W) // 2  # centered within pump zone

# Pump Z positions — single top row + centered P-04 below
PUMP_Z_TOP = 518      # top row (P-01, P-02) bottom edge

P04_Z = PUMP_Z_TOP - PUMP_BODY_H - 80   # 220mm — dropped for tray drain routing clearance
P04_X = FRAME_X + (FRAME_W - PUMP_BODY_W) // 2  # centered in frame

FRAME_Z_LO = P04_Z - PUMP_MARGIN_Z - ANGLE_W   # 235mm
FRAME_Z_HI = (PUMP_Z_TOP + PUMP_BODY_H
              + PUMP_MARGIN_Z + ANGLE_W)          # 781mm
FRAME_H = FRAME_Z_HI - FRAME_Z_LO

# Pump X positions — P-01 at left inner edge, P-02 at right inner edge
P01_X = FRAME_X + ANGLE_W + PUMP_MARGIN_X
P02_X = FRAME_X + FRAME_W - ANGLE_W - PUMP_MARGIN_X - PUMP_BODY_W

P01_Z = PUMP_Z_TOP
P02_Z = PUMP_Z_TOP

# Pipe constants — single size for all pump-driven runs
# All internal plumbing is 1/2" HDPE, matching Shurflo 2088 pump ports.
# 1" pipe used only at filter housings (1" NPT ports) and IBC fill/drain.
OD_H = PUMP_PIPE_OD       # 21mm — 1/2" nominal, matches pump ports
WALL_H = PUMP_PIPE_WALL   # 3mm
# Keep OD_1 for filter skid riser label reference only
OD_1 = FILT_PIPE_OD       # 33mm — 1" nominal (filter housing ports)
WALL_1 = FILT_PIPE_WALL   # 4mm

# Panel title (placed after FRAME_Z_HI is computed)
ax.text(sx(PUMP_X + PUMP_W / 2), sz(1080),
        "PUMP MANIFOLD ELEVATION — 3-PUMP LAYOUT (P-01, P-02, P-04)\n"
        "Interior View Looking at Pinhole Wall (Yd=0)  |  Scale 1:5",
        ha="center", va="top", fontsize=11, fontweight="bold",
        color="#1A237E", zorder=10)

# ── Container wall context ───────────────────────────────────────────────────
CORR_SPACING = 457
for rib_x in range(2285, 3200, CORR_SPACING):
    ax.plot([sx(rib_x), sx(rib_x)], [sz(0), sz(1100)],
            color="#AAAAAA", lw=0.6, ls="--", zorder=1)

# Floor line
ax.plot([sx(2200), sx(3400)], [sz(0), sz(0)],
        color="#888888", lw=1.5, ls="-", zorder=1)
ax.text(sx(2250), sz(-15), "FLOOR (Z=0)", ha="left", va="top",
        fontsize=6, color="#888888", style="italic")

# Walkway deck line
WALKWAY_Z = 100
ax.plot([sx(2300), sx(3300)], [sz(WALKWAY_Z), sz(WALKWAY_Z)],
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
# Pump head at top; ports project horizontally LEFT and RIGHT from head zone.
# Port Z is near the top of the body (head section).
PORT_Z_OFFSET = 30   # how far below the top of the body the port center is

def draw_pump(ax, px, pz, label, sublabel, color=C_PUMP_BODY):
    """Draw a single Shurflo 2088 pump in vertical orientation.

    px, pz: bottom-left corner of pump body in mm.
    127mm width includes port threads at each end.
    Ports face LEFT (OUT, lower X) and RIGHT (IN, higher X) from the head.
    Returns: (in_x, in_z, out_x, out_z) — port connection point centers.
    """
    # Pump body rectangle (127mm W × 218mm H, vertical — includes ports)
    ax.add_patch(plt.Rectangle((sx(px), sz(pz)),
                 PUMP_BODY_W / SC, PUMP_BODY_H / SC,
                 fc=color, ec=C_FRAME, lw=1.5, alpha=0.85, zorder=5))

    # Pump label inside body
    ax.text(sx(px + PUMP_BODY_W / 2), sz(pz + PUMP_BODY_H / 2),
            label, ha="center", va="center",
            fontsize=9, fontweight="bold", color="white", zorder=6)

    # Sub-label below pump
    ax.text(sx(px + PUMP_BODY_W / 2), sz(pz - 8),
            sublabel, ha="center", va="top",
            fontsize=5, color=C_TEXT, style="italic", zorder=6)

    # Port Z position near the head (top of body)
    port_z = pz + PUMP_BODY_H - PORT_Z_OFFSET

    # IN port: higher X side (right edge of 127mm body)
    in_x = px + PUMP_BODY_W
    ax.add_patch(plt.Circle((sx(in_x), sz(port_z)), PORT_OD / 2 / SC,
                 fc="#CCCCCC", ec=C_FRAME, lw=1.0, zorder=6))
    ax.text(sx(in_x + 8), sz(port_z), "IN",
            ha="left", va="center",
            fontsize=4, fontweight="bold", color=C_FRAME, zorder=8)

    # OUT port: lower X side (left edge of 127mm body)
    out_x = px
    ax.add_patch(plt.Circle((sx(out_x), sz(port_z)), PORT_OD / 2 / SC,
                 fc="#CCCCCC", ec=C_FRAME, lw=1.0, zorder=6))
    ax.text(sx(out_x - 8), sz(port_z), "OUT",
            ha="right", va="center",
            fontsize=4, fontweight="bold", color=C_FRAME, zorder=8)

    return in_x, port_z, out_x, port_z


# Draw 3 pumps — top row (P-01, P-02), P-04 centered below
# P-03 relocated to IBC plumbing corridor
p01_in_x, p01_in_z, p01_out_x, p01_out_z = draw_pump(ax, P01_X, P01_Z, "P-01", "BLUE SUPPLY")
p02_in_x, p02_in_z, p02_out_x, p02_out_z = draw_pump(ax, P02_X, P02_Z, "P-02", "BROWN RECYCLE")
p04_in_x, p04_in_z, p04_out_x, p04_out_z = draw_pump(ax, P04_X, P04_Z, "P-04", "TRAY DRAIN")

# Port Z heights (differ by row)
PORT_Z_TOP = p01_in_z      # top row port Z (706mm)
PORT_Z_P04 = p04_in_z      # P-04 port Z (468mm)
PUMP_TOP_Z_TOP = PUMP_Z_TOP + PUMP_BODY_H  # top of top-row pumps


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


# ═══════════════════════════════════════════════════════════════════════════════
# PIPE CONNECTIONS — 3 PUMPS (P-01, P-02, P-04)
# Top row (P-01/P-02) ports at PORT_Z_TOP; P-04 at PORT_Z_P04.
# Headers run above the top row. DV-02 right of P-04 at port height.
# P-03 has been relocated to the IBC plumbing corridor.
# ═══════════════════════════════════════════════════════════════════════════════

FRAME_R = FRAME_X + FRAME_W             # right edge of manifold frame
PIPE_EXIT_X = FRAME_R + 350             # pipes enter/exit toward IBCs (higher X)
PIPE_ENTRY_X = FRAME_X - 150            # pipes exit toward cargo door (lower X)
ELBOW_OFFSET = 40  # offset from port for visible 90° elbow
ELB = ELBOW_OFFSET

# Header Z heights above top-row pump bodies
HEADER_Z_BLUE_SUC    = PUMP_TOP_Z_TOP + 260  # Blue suction header
HEADER_Z_BLUE_DISCH  = FRAME_Z_HI + 20       # Blue discharge header

# Entry/exit X for pipes entering/leaving the manifold zone
TRANS_X = FRAME_R + 10  # just outside frame right

# DV-02: 60mm right of P-04 (lower physical X), at P-04 port height
DV02_R = 20
DV02_X = P04_X - 60
DV02_Z = PORT_Z_P04  # = P04_Z + PUMP_BODY_H - PORT_Z_OFFSET

# DV-02 output horizontal runs (above walkway)
DV02_BROWN_Z = WALKWAY_Z + 40    # 140mm — Brown closest to walkway
DV02_BLACK_Z = DV02_BROWN_Z + 25 # 165mm — Black above Brown
DV02_BLACK_RISER_X = DV02_X
DV02_BROWN_RISER_X = DV02_X - 25  # 25mm lower X (right in drawing)

# Tray drain suction
TRAY_DRAIN_Z = WALKWAY_Z + 20   # 120mm — just above walkway deck
TRAY_SUMP_X = PROC_TRAY_DRAIN_X  # 2399mm

# ── Pipe layer zorders (depth from wall) ────────────────────────────────────
# Layer 1 (back, closest to wall): Black/waste pipes
# Layer 2 (middle): Brown pipes
# Layer 3 (front, closest to viewer): Blue pipes
# Higher zorder = drawn on top = closer to viewer
Z_BLACK = 6    # Layer 1 — back
Z_BROWN = 7    # Layer 2 — middle
Z_BLUE  = 8    # Layer 3 — front

# ── Pipe crossing helper (break in rear pipe, front pipe continuous) ─────────

# ── Reducer symbol helper ────────────────────────────────────────────────────
def draw_reducer(ax, x_mm, z_mm, orientation="h"):
    """Draw a 1"→1/2" reducer symbol at (x_mm, z_mm). 'h'=horizontal, 'v'=vertical."""
    r = 12
    if orientation == "h":
        pts = [(sx(x_mm + r), sz(z_mm - OD_1 / 2)),
               (sx(x_mm + r), sz(z_mm + OD_1 / 2)),
               (sx(x_mm - r), sz(z_mm + OD_H / 2)),
               (sx(x_mm - r), sz(z_mm - OD_H / 2))]
    else:
        pts = [(sx(x_mm - OD_1 / 2), sz(z_mm + r)),
               (sx(x_mm + OD_1 / 2), sz(z_mm + r)),
               (sx(x_mm + OD_H / 2), sz(z_mm - r)),
               (sx(x_mm - OD_H / 2), sz(z_mm - r))]
    poly = plt.Polygon(pts, fc=C_STEEL_FILL, ec=C_FRAME, lw=1.0, zorder=9)
    ax.add_patch(poly)

# ── ACC-01 Accumulator (on Blue discharge header) ──────────────────────────
ACC_W = 200      # 7-7/8" length (horizontal, inline with header)
ACC_H = 127      # 5" diameter (vertical, from SeaFlo spec)
ACC_X = FRAME_R + 40
ACC_Z = HEADER_Z_BLUE_DISCH - ACC_H / 2 + 25   # 25mm above discharge header center

ax.add_patch(plt.Rectangle((sx(ACC_X), sz(ACC_Z)),
             ACC_W / SC, ACC_H / SC,
             fc=C_ACC, ec=C_FRAME, lw=1.5, alpha=0.8, zorder=5))
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

# ── BV-01 / BV-02 Ball Valves ──────────────────────────────────────────────
BV01_X = FRAME_R + 60
BV01_Z = HEADER_Z_BLUE_SUC
draw_ball_valve(ax, BV01_X, BV01_Z, "BV-01")
place_label(ax, sx(BV01_X), sz(BV01_Z + 30), "BV-01\n(½\" BALL)",
            component='valve', fontsize=5, color=C_TEXT,
            dx=0, dy=1.2, ha='center', va='bottom')

BV02_X = ACC_X + ACC_W + 40
BV02_Z = HEADER_Z_BLUE_DISCH
draw_ball_valve(ax, BV02_X, BV02_Z, "BV-02")
place_label(ax, sx(BV02_X), sz(BV02_Z + 30), "BV-02\n(½\" BALL)",
            component='valve', fontsize=5, color=C_TEXT,
            dx=0, dy=1.2, ha='center', va='bottom')

# ════════════════════════════════════════════════════════════════════════════
# P-01 BLUE SUPPLY — IBC → BV-01 → P-01 → ACC-01 → BV-02 → spray bar
# ════════════════════════════════════════════════════════════════════════════
# Blue suction: IBC → BV-01
draw_pipe_path(ax,
    [PIPE_EXIT_X, BV01_X + BV_R],
    [HEADER_Z_BLUE_SUC, HEADER_Z_BLUE_SUC],
    OD_H, WALL_H, fc=C_BLUE, zorder=Z_BLUE)
# BV-01 → manifold entry
draw_pipe_path(ax,
    [BV01_X - BV_R, FRAME_R],
    [HEADER_Z_BLUE_SUC, HEADER_Z_BLUE_SUC],
    OD_H, WALL_H, fc=C_BLUE, zorder=Z_BLUE)
# Suction drop → P-01 IN (split at Blue discharge crossing)
_suc_gap = OD_H / 2.0
draw_pipe_path(ax,
    [FRAME_R, p01_in_x + ELB, p01_in_x + ELB],
    [HEADER_Z_BLUE_SUC, HEADER_Z_BLUE_SUC, HEADER_Z_BLUE_DISCH + _suc_gap],
    OD_H, WALL_H, fc=C_BLUE, zorder=Z_BLUE)
draw_pipe_path(ax,
    [p01_in_x + ELB, p01_in_x + ELB, p01_in_x],
    [HEADER_Z_BLUE_DISCH - _suc_gap, PORT_Z_TOP, PORT_Z_TOP],
    OD_H, WALL_H, fc=C_BLUE, zorder=Z_BLUE)

# P-01 OUT → discharge header → ACC-01 → BV-02 → spray bar
draw_pipe_path(ax,
    [p01_out_x, p01_out_x - ELB, p01_out_x - ELB, ACC_X],
    [PORT_Z_TOP, PORT_Z_TOP, HEADER_Z_BLUE_DISCH, HEADER_Z_BLUE_DISCH],
    OD_H, WALL_H, fc=C_BLUE, zorder=Z_BLUE)
acc_exit_x = ACC_X + ACC_W
draw_pipe_path(ax,
    [acc_exit_x, BV02_X - BV_R],
    [HEADER_Z_BLUE_DISCH, HEADER_Z_BLUE_DISCH],
    OD_H, WALL_H, fc=C_BLUE, zorder=Z_BLUE)
draw_pipe_path(ax,
    [BV02_X + BV_R, PIPE_EXIT_X],
    [BV02_Z, BV02_Z],
    OD_H, WALL_H, fc=C_BLUE, zorder=Z_BLUE)

# ════════════════════════════════════════════════════════════════════════════
# P-02 BROWN RECYCLE — IBC-3 → P-02 → filter skid
# ════════════════════════════════════════════════════════════════════════════
# Brown suction: IBC-3 → manifold entry → P-02 IN
draw_pipe_path(ax,
    [PIPE_EXIT_X, FRAME_R],
    [PORT_Z_TOP, PORT_Z_TOP],
    OD_H, WALL_H, fc=C_BROWN, zorder=Z_BROWN)
draw_pipe_path(ax,
    [FRAME_R, p02_in_x],
    [PORT_Z_TOP, PORT_Z_TOP],
    OD_H, WALL_H, fc=C_BROWN, zorder=Z_BROWN)

# P-02 OUT → 90° bend → straight north riser → filter skid
# Riser goes straight up from first bend, crossing both Blue headers
BROWN_RISER_X = p02_out_x - ELB  # riser at first bend
_p02_gap = OD_H / 2.0  # gap for Blue pipe crossings
RISER_EXIT_Z = HEADER_Z_BLUE_SUC + 80  # exit above suction header

# P-02 out to first bend, then up to discharge header crossing
draw_pipe_path(ax,
    [p02_out_x, BROWN_RISER_X, BROWN_RISER_X],
    [PORT_Z_TOP, PORT_Z_TOP, HEADER_Z_BLUE_DISCH - _p02_gap],
    OD_H, WALL_H, fc=C_BROWN, zorder=Z_BROWN)
# Gap at discharge header, continue to suction header crossing
draw_pipe_path(ax,
    [BROWN_RISER_X, BROWN_RISER_X],
    [HEADER_Z_BLUE_DISCH + _p02_gap, HEADER_Z_BLUE_SUC - _p02_gap],
    OD_H, WALL_H, fc=C_BROWN, zorder=Z_BROWN)
# Gap at suction header, continue to riser exit
draw_pipe_path(ax,
    [BROWN_RISER_X, BROWN_RISER_X],
    [HEADER_Z_BLUE_SUC + _p02_gap, RISER_EXIT_Z],
    OD_H, WALL_H, fc=C_BROWN, zorder=Z_BROWN)
ax.annotate("", xy=(sx(BROWN_RISER_X), sz(RISER_EXIT_Z)),
            xytext=(sx(BROWN_RISER_X), sz(RISER_EXIT_Z - 60)),
            arrowprops=dict(arrowstyle="-|>", color=C_BROWN, lw=1.5), zorder=10)
ax.text(sx(BROWN_RISER_X), sz(RISER_EXIT_Z + 10),
        "TO FILTER SKID\n(F1 → F2 → F3)", ha="center", va="bottom",
        fontsize=5.5, color=C_BROWN, style="italic", fontweight="bold")

# ════════════════════════════════════════════════════════════════════════════
# P-04 TRAY DRAIN — sump → P-04 → DV-02 → IBC-3 / IBC-4
# ════════════════════════════════════════════════════════════════════════════
# Suction: tray sump → vertical riser → 90° left → drop to port → 90° into P-04 IN
_riser_top_z = P04_Z + PUMP_BODY_H + 40  # 40mm above P-04 top
_drop_x = p04_in_x + ELB                 # X where pipe drops toward port
draw_pipe_path(ax,
    [TRAY_SUMP_X, TRAY_SUMP_X, _drop_x, _drop_x, p04_in_x],
    [TRAY_DRAIN_Z, _riser_top_z, _riser_top_z, PORT_Z_P04, PORT_Z_P04],
    OD_H, WALL_H, fc=C_BLACK_SYS, zorder=Z_BLACK)
ax.annotate("", xy=(sx(TRAY_SUMP_X), sz(_riser_top_z - 30)),
            xytext=(sx(TRAY_SUMP_X), sz(TRAY_DRAIN_Z + 30)),
            arrowprops=dict(arrowstyle="-|>", color=C_BLACK_SYS, lw=1.2), zorder=10)
ax.text(sx(TRAY_SUMP_X - 30), sz((_riser_top_z + TRAY_DRAIN_Z) / 2),
        "FROM TRAY\nSUMP", ha="right", va="center",
        fontsize=4.5, color=C_BLACK_SYS, style="italic")

# Discharge: P-04 OUT → DV-02 (60mm right of P-04 at port height)
draw_pipe_path(ax,
    [p04_out_x, DV02_X + DV02_R],
    [PORT_Z_P04, PORT_Z_P04],
    OD_H, WALL_H, fc=C_BROWN, zorder=Z_BROWN)

# DV-02 symbol (diamond)
dv02_pts_x = [sx(DV02_X), sx(DV02_X + DV02_R), sx(DV02_X), sx(DV02_X - DV02_R)]
dv02_pts_z = [sz(DV02_Z + DV02_R), sz(DV02_Z), sz(DV02_Z - DV02_R), sz(DV02_Z)]
ax.add_patch(plt.Polygon(list(zip(dv02_pts_x, dv02_pts_z)),
                          fc="white", ec=C_FRAME, lw=2.0, zorder=9))
ax.text(sx(DV02_X), sz(DV02_Z), "3W", ha="center", va="center",
        fontsize=4, fontweight="bold", color=C_FRAME, zorder=10)
place_label(ax, sx(DV02_X), sz(DV02_Z - 25), "DV-02\n(3-WAY DIVERTER)",
            component='diverter', fontsize=5.5, color=C_TEXT,
            dx=0, dy=-2.0, ha='center', va='top')

# DV-02 Black output: bottom vertex → south to Z=165 → left to IBC
draw_pipe_path(ax,
    [DV02_BLACK_RISER_X, DV02_BLACK_RISER_X, PIPE_EXIT_X],
    [DV02_Z - DV02_R, DV02_BLACK_Z, DV02_BLACK_Z],
    OD_H, WALL_H, fc=C_BLACK_SYS, zorder=Z_BLACK)
ax.text(sx((DV02_X + PIPE_EXIT_X) / 2), sz(DV02_BLACK_Z - 25),
        "BLACK → IBC-4", ha="center", va="top",
        fontsize=5, color=C_BLACK_SYS, fontweight="bold")

# DV-02 Brown output: right vertex → riser south to Z=140 → left to IBC
draw_pipe_path(ax,
    [DV02_X - DV02_R, DV02_BROWN_RISER_X,
     DV02_BROWN_RISER_X, PIPE_EXIT_X],
    [DV02_Z, DV02_Z,
     DV02_BROWN_Z, DV02_BROWN_Z],
    OD_H, WALL_H, fc=C_BROWN, zorder=Z_BROWN)
ax.text(sx((DV02_X + PIPE_EXIT_X) / 2), sz(DV02_BROWN_Z + 25),
        "BROWN → IBC-3", ha="center", va="bottom",
        fontsize=5, color=C_BROWN, fontweight="bold")


# ── Flow direction arrows ────────────────────────────────────────────────────
arrow_style = dict(arrowstyle="-|>", lw=1.5, mutation_scale=10)

# Blue supply arrow (incoming from higher X toward P-01)
mid_blue_in = (PIPE_EXIT_X + BV01_X) / 2
ax.annotate("", xy=(sx(mid_blue_in - 30), sz(HEADER_Z_BLUE_SUC)),
            xytext=(sx(mid_blue_in + 30), sz(HEADER_Z_BLUE_SUC)),
            arrowprops=dict(**arrow_style, color=C_BLUE), zorder=12)

# Blue discharge arrow (outgoing to higher X)
mid_blue_out = (BV02_X + PIPE_EXIT_X) / 2
ax.annotate("", xy=(sx(mid_blue_out + 30), sz(HEADER_Z_BLUE_DISCH)),
            xytext=(sx(mid_blue_out - 30), sz(HEADER_Z_BLUE_DISCH)),
            arrowprops=dict(**arrow_style, color=C_BLUE), zorder=12)

# Brown suction arrow (incoming from higher X at PORT_Z_TOP)
mid_brown = (PIPE_EXIT_X + p02_in_x) / 2
ax.annotate("", xy=(sx(mid_brown - 30), sz(PORT_Z_TOP)),
            xytext=(sx(mid_brown + 30), sz(PORT_Z_TOP)),
            arrowprops=dict(**arrow_style, color=C_BROWN), zorder=12)


# ── Pipe entry/exit annotations ──────────────────────────────────────────────
# Blue supply label at entry (higher X side)
ax.text(sx(PIPE_EXIT_X + 5), sz(HEADER_Z_BLUE_SUC + 15),
        "FROM IBC-1 & IBC-2\n(BLUE SUPPLY)", ha="right", va="bottom",
        fontsize=5, color=C_BLUE, style="italic")

# Blue discharge label at exit (higher X side)
ax.text(sx(PIPE_EXIT_X + 5), sz(HEADER_Z_BLUE_DISCH + 15),
        "TO SPRAY BAR\n(BLUE DISCHARGE)", ha="right", va="bottom",
        fontsize=5, color=C_BLUE, style="italic")

# Brown suction label (higher X side)
ax.text(sx(PIPE_EXIT_X + 5), sz(PORT_Z_TOP - 15),
        "FROM IBC-3\n(BROWN RECYCLE)", ha="right", va="top",
        fontsize=5, color=C_BROWN, style="italic")


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

# Pump body width (P-01)
draw_dim_h(ax, sx(P01_X), sx(P01_X + PUMP_BODY_W), sz(P01_Z - 30),
           f"{PUMP_BODY_W}mm", offset=0.25, fs=5.5)

# P-04 centered position
draw_dim_h(ax, sx(P04_X), sx(P04_X + PUMP_BODY_W), sz(P04_Z - 30),
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
       sx(acc_cx + 30), sz(ACC_Z + ACC_H + 70),
       "ACC-01: 0.75L (23.5 OZ)\n125 PSI, 1/2\" MNPT\n200×127×114mm\n(SEAFLO)", fs=5.5)

# Pump spec (general — one callout for all)
leader(ax, sx(P01_X + PUMP_BODY_W / 2), sz(P01_Z + PUMP_BODY_H / 2),
       sx(P01_X - 80), sz(P01_Z + PUMP_BODY_H / 2 + 40),
       "ALL PUMPS: SHURFLO 2088\n12V DC, 3.5 GPM, 45 PSI\n218H × 127W × 113D mm\n(127mm INCL. PORT THREADS)", fs=5.5)

# Wall bracket
leader(ax, sx(FRAME_X - BRACKET_W / 2), sz(FRAME_Z_LO + 40 + BRACKET_H / 2),
       sx(FRAME_X - BRACKET_W / 2 - 80), sz(FRAME_Z_LO + 40 + BRACKET_H / 2 + 50),
       "FRAME BRACKET\nTO WALL RIB", fs=5)

# Pipe material leader
pipe_label_x = (BV01_X + PIPE_EXIT_X) / 2
leader(ax, sx(pipe_label_x), sz(HEADER_Z_BLUE_SUC + 8),
       sx(pipe_label_x), sz(HEADER_Z_BLUE_SUC + 60),
       "ALL MANIFOLD: 1/2\" HDPE Sch40\n(OD 21mm, WALL 3mm)", fs=5)


# ── Notes ────────────────────────────────────────────────────────────────────
notes = [
    "1. All pumps: Shurflo 2088-554-144, 12V DC, 3.5 GPM, 45 PSI, self-priming diaphragm.",
    "2. Pump body: 218H × 127W × 113D mm. Vertical, ports face L/R. Through-bolted to 18mm ply.",
    "3. All manifold piping: 1/2\" HDPE Sch40 (OD 21mm, wall 3mm).",
    "4. Frame widened 40% (565mm) for pump separation. P-04 centered below P-01/P-02.",
    "5. P-01 (Blue): IBC-1/2 → BV-01 → P-01 → ACC-01 → BV-02 → spray bar.",
    "6. P-02 (Brown): IBC-3 → P-02 → riser straight north → filter skid.",
    "7. P-04 (Tray drain): sump → P-04 → DV-02 → IBC-3 (Brown) or IBC-4 (Black).",
    "8. DV-02 outputs: Brown at Z=140 (closest to walkway), Black at Z=165 (above Brown).",
    "9. P-03 (Waste evac) relocated to IBC plumbing corridor — not shown on this diagram.",
    "10. ACC-01: SeaFlo 0.75L accumulator, 125 PSI, 1/2\" MNPT. Each circuit fused at 10A.",
]
for i, n in enumerate(notes):
    fig.text(0.35, 0.055 - i * 0.013, n, fontsize=6, color=C_TEXT,
             fontfamily="monospace", va="top")


# ═══════════════════════════════════════════════════════════════════════════════
# DETAIL A — PUMP MOUNTING CROSS-SECTION (~1:2)
# Side elevation (vertical section perpendicular to pinhole wall)
# Yd horizontal (wall at left), Z vertical
# Shows: corrugated wall → 18mm ply → pump bracket → pump body → ports
# ═══════════════════════════════════════════════════════════════════════════════

SC_A = 4.5  # mm per drawing unit for detail (~1:4.5, compact for side panel)
OAY = 1.0   # Yd origin
OAZ = 2.0   # Z origin

def sa_y(yd_mm):
    return OAY + yd_mm / SC_A

def sa_z(z_mm):
    return OAZ + z_mm / SC_A

# Detail limits — taller to show full 218mm pump height
ax2.set_xlim(sa_y(-25) - 0.5, sa_y(220) + 0.5)
ax2.set_ylim(sa_z(-160) - 0.5, sa_z(180) + 0.5)

# Detail title
ax2.text(sa_y(100), sa_z(175), "DETAIL A\nPUMP MOUNTING CROSS-SECTION\nScale ~1:4.5",
         ha="center", va="top", fontsize=7, fontweight="bold",
         color="#1A237E", zorder=10)

# All Z coordinates below are relative to pump port center

# ── 1. Container corrugated wall (section fill) ─────────────────────────────
WALL_T = 2.0
ax2.add_patch(plt.Rectangle((sa_y(-WALL_T), sa_z(-130)),
              WALL_T / SC_A, 280 / SC_A,
              fc=C_STEEL_FILL, ec=C_FRAME, lw=1.8, zorder=3, hatch="//"))
ax2.text(sa_y(-WALL_T / 2), sa_z(145), "WALL", ha="center", va="bottom",
         fontsize=5.5, color=C_FRAME)

# ── 2. Plywood backing board (18mm) ─────────────────────────────────────────
PLY_YD_START = 0
PLY_THICK = 18
ax2.add_patch(plt.Rectangle((sa_y(PLY_YD_START), sa_z(-130)),
              PLY_THICK / SC_A, 280 / SC_A,
              fc=C_PLY, ec="#A09060", lw=1.5, zorder=3))
# Wood grain
for gz in range(-125, 140, 12):
    ax2.plot([sa_y(PLY_YD_START + 2), sa_y(PLY_YD_START + PLY_THICK - 2)],
             [sa_z(gz), sa_z(gz + 2)],
             color="#C0B080", lw=0.4, zorder=3.5)

draw_dim_h(ax2, sa_y(PLY_YD_START), sa_y(PLY_YD_START + PLY_THICK),
           sa_z(-50), "18mm", offset=0.33, fs=5.5)

# ── 3. Pump body — through-bolted directly to plywood ────────────────────────
# No bracket. Pump base sits flat against ply face.
# Four 1/4"-20 bolts in two columns, 3.2" (81.3mm) apart, each column
# with two bolts.  Bolts pass through pump mounting feet + 18mm ply;
# nyloc nuts on wall side.
PUMP_YD = PLY_YD_START + PLY_THICK   # pump base face flush against ply
PUMP_DEPTH = 113   # 4.45" depth in Yd (from datasheet)
PUMP_SEC_H = 218   # FULL pump height in section (218mm = 8.60" per spec)
BOLT_COL_SPACING = 81.3  # 3.2" between bolt columns (vertical Z)

# Pump body Z range — centered on Z=0 (port height reference)
PUMP_SEC_Z_BOT = -PUMP_SEC_H / 2   # -109mm
PUMP_SEC_Z_TOP = PUMP_SEC_H / 2    # +109mm

# Pump body rectangle (full 218mm height × 113mm depth)
ax2.add_patch(plt.Rectangle((sa_y(PUMP_YD), sa_z(PUMP_SEC_Z_BOT)),
              PUMP_DEPTH / SC_A, PUMP_SEC_H / SC_A,
              fc=C_PUMP_BODY, ec=C_FRAME, lw=1.8, alpha=0.85, zorder=5))

ax2.text(sa_y(PUMP_YD + PUMP_DEPTH / 2), sa_z(0),
         "PUMP\nBODY", ha="center", va="center",
         fontsize=6, color="white", fontweight="bold", zorder=6)

# Diaphragm chamber indication (internal circle, centered on pump)
chamber_cx = PUMP_YD + PUMP_DEPTH / 2
chamber_cz = -20
chamber_r = 30
ax2.add_patch(plt.Circle((sa_y(chamber_cx), sa_z(chamber_cz)), chamber_r / SC_A,
              fc="#D0A070", ec="#8B5E3C", lw=1.0, alpha=0.5, zorder=5.5))
ax2.text(sa_y(chamber_cx), sa_z(chamber_cz - 18), "DIAPHRAGM",
         ha="center", va="top", fontsize=4, color="#8B5E3C", zorder=6)

# Head zone (top ~50mm of pump — ports exit from here)
HEAD_ZONE_H = 50
head_z_bot = PUMP_SEC_Z_TOP - HEAD_ZONE_H
ax2.add_patch(plt.Rectangle((sa_y(PUMP_YD + 10), sa_z(head_z_bot)),
              (PUMP_DEPTH - 20) / SC_A, HEAD_ZONE_H / SC_A,
              fc="#CC8844", ec=C_FRAME, lw=1.2, alpha=0.85, zorder=5))
ax2.text(sa_y(PUMP_YD + PUMP_DEPTH / 2), sa_z(head_z_bot + HEAD_ZONE_H / 2),
         "HEAD", ha="center", va="center",
         fontsize=5, color="white", fontweight="bold", zorder=6)

# Motor end indication (bottom ~40mm)
MOTOR_ZONE_H = 40
ax2.add_patch(plt.Rectangle((sa_y(PUMP_YD + 10), sa_z(PUMP_SEC_Z_BOT)),
              (PUMP_DEPTH - 20) / SC_A, MOTOR_ZONE_H / SC_A,
              fc="#CC7733", ec=C_FRAME, lw=1.0, alpha=0.6, zorder=5))
ax2.text(sa_y(PUMP_YD + PUMP_DEPTH / 2), sa_z(PUMP_SEC_Z_BOT + MOTOR_ZONE_H / 2),
         "MOTOR", ha="center", va="center",
         fontsize=4.5, color="white", fontweight="bold", zorder=6)

# ── 4. Through-bolts (4× 1/4"-20, two columns 3.2" apart) ──────────────────
# Cross-section shows two bolts (one column); the other column is 81.3mm
# away in X (into the page).  Each bolt goes: washer + nut (pump side) →
# shank through pump foot + 18mm ply → washer + nyloc nut (wall side).
BOLT_SHANK_D = 6.35   # 1/4" = 6.35mm
BOLT_HEAD_W = 10       # hex head/nut width (across flats)
BOLT_HEAD_H = 5        # hex head/nut height
NUT_H = 5              # nyloc nut height

# Two bolt Z positions (centered on pump body, 81.3mm apart)
pump_center_z = 0  # centered on port height reference
bolt_z_upper = pump_center_z + BOLT_COL_SPACING / 2
bolt_z_lower = pump_center_z - BOLT_COL_SPACING / 2

WASHER_T = 2   # washer thickness

for bz in [bolt_z_upper, bolt_z_lower]:
    # Assembly order (wall → pump side):
    #   nyloc nut | washer | PLY (18mm) | washer | pump foot | nut
    # Nut on pump side: sits flush against washer, which is against pump face
    washer_pump_yd = PUMP_YD                         # washer against pump face
    nut_pump_yd = washer_pump_yd + WASHER_T           # nut against washer

    # Bolt shank — through pump base + plywood, ends at nut
    bolt_tip_yd = PLY_YD_START - 2   # just past ply on wall side
    ax2.plot([sa_y(bolt_tip_yd), sa_y(nut_pump_yd)],
             [sa_z(bz), sa_z(bz)],
             color=C_FRAME, lw=1.8, zorder=7)

    # Washer (pump side, between nut and pump mounting foot)
    ax2.add_patch(plt.Rectangle(
        (sa_y(washer_pump_yd), sa_z(bz - 5)),
        WASHER_T / SC_A, 10 / SC_A,
        fc="#999999", ec=C_FRAME, lw=0.5, zorder=7.5))

    # Nut on pump side (tightened down against washer)
    ax2.add_patch(plt.Rectangle(
        (sa_y(nut_pump_yd), sa_z(bz - BOLT_HEAD_W / 2)),
        BOLT_HEAD_H / SC_A, BOLT_HEAD_W / SC_A,
        fc="#666666", ec=C_FRAME, lw=1.0, zorder=8))

    # Nyloc nut on wall side (behind ply)
    ax2.add_patch(plt.Rectangle(
        (sa_y(bolt_tip_yd - NUT_H), sa_z(bz - BOLT_HEAD_W / 2)),
        NUT_H / SC_A, BOLT_HEAD_W / SC_A,
        fc="#666666", ec=C_FRAME, lw=1.0, zorder=8))

    # Washer (wall side)
    ax2.add_patch(plt.Rectangle(
        (sa_y(bolt_tip_yd - 1), sa_z(bz - 5)),
        1 / SC_A, 10 / SC_A,
        fc="#999999", ec=C_FRAME, lw=0.5, zorder=7.5))

# Bolt column spacing dimension (vertical between two bolts)
_nut_outer_yd = nut_pump_yd + BOLT_HEAD_H
draw_dim_v(ax2, sa_y(_nut_outer_yd + 18), sa_z(bolt_z_lower), sa_z(bolt_z_upper),
           f"81.3mm\n(3.2\")", offset=0.33, fs=5)

# Bolt callout
leader(ax2, sa_y(_nut_outer_yd + 5), sa_z(bolt_z_upper),
       sa_y(_nut_outer_yd + 45), sa_z(bolt_z_upper + 25),
       "1/4\"-20 × 30mm\n+ NYLOC NUT\n(4 PER PUMP)", fs=5)

# ── 5. Port bores (1/2" NPSM — exit SIDEWAYS in X, not front face) ────────
# In this Yd section, the ports project LEFT and RIGHT out of the page.
# They appear as circles (cross-section through the port bore).
PORT_OD_SEC = 21   # 1/2" pipe OD ~21mm
PORT_WALL_SEC = 3
# Ports are near the head (top of pump), 30mm below top edge
PORT_Z_SEC = PUMP_SEC_Z_TOP - PORT_Z_OFFSET  # ~79mm above center

# Port bore — shown as a circle with dashed line indicating it exits sideways
port_bore_yd = PUMP_YD + PUMP_DEPTH / 2  # approximate center of head zone in Yd
port_bore_r = PORT_OD_SEC / 2

# Outer bore circle (port tube cross-section)
ax2.add_patch(plt.Circle((sa_y(port_bore_yd), sa_z(PORT_Z_SEC)),
              port_bore_r / SC_A, fc="white", ec=C_FRAME, lw=1.5, zorder=6))
# Inner bore
ax2.add_patch(plt.Circle((sa_y(port_bore_yd), sa_z(PORT_Z_SEC)),
              (port_bore_r - PORT_WALL_SEC) / SC_A,
              fc="white", ec=C_FRAME, lw=0.8, zorder=6.5))
# Center dot (convention for a bore going into the page)
ax2.plot(sa_y(port_bore_yd), sa_z(PORT_Z_SEC), 'o',
         color=C_FRAME, markersize=3, zorder=7)

# Arrow showing port direction (exits sideways in X)
ax2.annotate("", xy=(sa_y(port_bore_yd + 30), sa_z(PORT_Z_SEC)),
             xytext=(sa_y(port_bore_yd + 15), sa_z(PORT_Z_SEC)),
             arrowprops=dict(arrowstyle="-|>", color=C_FRAME, lw=1.2), zorder=8)
ax2.annotate("", xy=(sa_y(port_bore_yd - 30), sa_z(PORT_Z_SEC)),
             xytext=(sa_y(port_bore_yd - 15), sa_z(PORT_Z_SEC)),
             arrowprops=dict(arrowstyle="-|>", color=C_FRAME, lw=1.2), zorder=8)

leader(ax2, sa_y(port_bore_yd + 25), sa_z(PORT_Z_SEC + 5),
       sa_y(port_bore_yd + 50), sa_z(PORT_Z_SEC + 30),
       "1/2\" NPSM PORTS\nEXIT LEFT & RIGHT\n(81mm APART IN X)\n→ 1/2\" HDPE", fs=5)

# ── Dimensions ───────────────────────────────────────────────────────────────
# Ply thickness (already drawn above)
# Pump depth
draw_dim_h(ax2, sa_y(PUMP_YD), sa_y(PUMP_YD + PUMP_DEPTH),
           sa_z(PUMP_SEC_Z_BOT - 20), f"{PUMP_DEPTH}mm\nPUMP DEPTH", offset=0.33, fs=5.5)

# Wall + ply total
draw_dim_h(ax2, sa_y(-WALL_T), sa_y(PLY_YD_START + PLY_THICK),
           sa_z(PUMP_SEC_Z_BOT - 40), f"{PLY_THICK + int(WALL_T)}mm\nWALL + PLY", offset=0.33, fs=5)

# Pump height dimension (full 218mm)
draw_dim_v(ax2, sa_y(PUMP_YD + PUMP_DEPTH + 15), sa_z(PUMP_SEC_Z_BOT), sa_z(PUMP_SEC_Z_TOP),
           f"{PUMP_SEC_H}mm\n(8.60\")", offset=0.33, fs=5)

# ── Component labels along section ──────────────────────────────────────────
label_z_a = PUMP_SEC_Z_TOP + 20
label_items = [
    (PLY_YD_START + PLY_THICK / 2, "18mm PLY"),
    (PUMP_YD + PUMP_DEPTH / 2, "SHURFLO 2088"),
]
for ly, ltxt in label_items:
    ax2.text(sa_y(ly), sa_z(label_z_a), ltxt, ha="center", va="bottom",
             fontsize=5, color=C_FRAME)
    ax2.plot([sa_y(ly), sa_y(ly)], [sa_z(label_z_a - 5), sa_z(PUMP_SEC_Z_TOP + 2)],
             color=C_DIM, lw=0.5, ls=":", zorder=2)

# Section cut indicator note
ax2.text(sa_y(70), sa_z(PUMP_SEC_Z_BOT - 30),
         "SECTION IN Yd AT PORT HEIGHT\nPUMP THROUGH-BOLTED TO 18mm PLY\nNO BRACKET — DIRECT MOUNT",
         ha="center", va="top", fontsize=5.5, color="#666666", style="italic")


# ═══════════════════════════════════════════════════════════════════════════════
# DETAIL B — PLAN VIEW (PUMP MANIFOLD ONLY)
# View from ceiling looking down at the manifold zone
# X horizontal (mirrored to match elevation), Yd vertical (wall at top)
# Shows: 3 pumps from above (P-01, P-02, P-04), ACC-01, BV-01/BV-02, DV-02, pipe stubs with
#        direction arrows indicating where each pipe routes to
# ═══════════════════════════════════════════════════════════════════════════════

SC_B = 5.5    # mm per drawing unit (~1:5.5 — compact for side panel)
OBX = 1.0     # X origin offset
OBY = 0.8     # Yd origin offset

def sp_x(x_mm):
    """Convert X position (mm) to plan view x coordinate."""
    return OBX + (x_mm - PUMP_X + 200) / SC_B

def sp_y(yd_mm):
    """Convert Yd position (mm) to plan view y coordinate (Yd=0 at top)."""
    return OBY + (500 - yd_mm) / SC_B  # flip so wall (Yd=0) is at top

# Set axis limits — focus on X=2200–3500, Yd=-50 to 520
ax3.set_xlim(sp_x(2200) - 0.5, sp_x(3500) + 0.5)
ax3.set_ylim(sp_y(520) - 0.5, sp_y(-100) + 0.5)

# Mirror X to match elevation convention (high X on left)
ax3.invert_xaxis()

# Detail title
ax3.text(sp_x(2750), sp_y(-90),
         "DETAIL B\nPUMP MANIFOLD PLAN VIEW\nLooking Down from Ceiling  |  Scale ~1:5.5",
         ha="center", va="top", fontsize=7, fontweight="bold",
         color="#1A237E", zorder=10)

# ── Pinhole wall (Yd=0) ─────────────────────────────────────────────────────
ax3.plot([sp_x(2150), sp_x(3150)], [sp_y(0), sp_y(0)],
         color=C_FRAME, lw=3.0, zorder=3)
ax3.text(sp_x(2200), sp_y(-15), "PINHOLE WALL (Yd=0)", ha="left", va="top",
         fontsize=5.5, color=C_FRAME, fontweight="bold")

# Corrugation ribs at Yd=0 (wall detail)
for rib_x in range(2285, 3100, CORR_SPACING):
    ax3.plot([sp_x(rib_x), sp_x(rib_x)], [sp_y(-5), sp_y(5)],
             color="#AAAAAA", lw=1.5, zorder=2)

# ── Near walkway edge (Yd=300) ──────────────────────────────────────────────
ax3.plot([sp_x(2150), sp_x(3150)], [sp_y(WALKWAY_W), sp_y(WALKWAY_W)],
         color="#BBBBBB", lw=1.0, ls="--", zorder=2)
ax3.text(sp_x(3100), sp_y(WALKWAY_W + 10), "WALKWAY EDGE (Yd=300)",
         ha="right", va="top", fontsize=4.5, color="#999999", style="italic")

# ── Mounting frame footprint (plan view) ────────────────────────────────────
# Frame sits against wall, depth = 18mm ply + bracket + 113mm pump depth (vertical)
MANIFOLD_DEPTH = 160  # Yd depth from wall (ply + bracket + 113mm pump body + clearance)
# Frame perimeter
ax3.add_patch(plt.Rectangle(
    (sp_x(FRAME_X), sp_y(MANIFOLD_DEPTH)),
    FRAME_W / SC_B, MANIFOLD_DEPTH / SC_B,
    fc=C_PLY, ec=C_FRAME, lw=2.0, alpha=0.4, zorder=3))

# Frame label
ax3.text(sp_x(FRAME_X + FRAME_W / 2), sp_y(MANIFOLD_DEPTH + 10),
         f"MOUNTING FRAME\n{FRAME_W}×{MANIFOLD_DEPTH}mm", ha="center", va="top",
         fontsize=5, color=C_FRAME, style="italic")

# ── Three pumps from above (P-01, P-02, P-04) ──────────────────────────────
# Vertical pump orientation: from above, footprint is 127mm W (X) × 113mm D (Yd)
# Ports face LEFT (OUT) and RIGHT (IN) in X, near the head (top of pump).
PP_W = PUMP_BODY_W   # 127mm width in X (matches elevation)
PP_D = 113            # 113mm depth in Yd (vertical pump — from above)
PP_PORT_R = 10        # port circle radius (1/2" male thread)

# Pumps are stacked vertically (Z): P-01 above empty slot, P-02 above P-04.
# In plan view (looking down) only top-row pumps are visible; bottom-row
# P-04 is ghosted (dashed outline, faded fill) offset slightly in Yd.
# P-03 has been relocated to the IBC plumbing corridor.
GHOST_ALPHA = 0.2
GHOST_LW = 1.0
GHOST_LS = (0, (4, 3))  # dashed
GHOST_YD_OFFSET = 8     # slight offset so ghost outline peeks out

# Pump Yd start position (motor end at wall, head end outward)
PUMP_YD_START = 20   # 18mm ply + 2mm clearance

# Port positions in plan view: ports on LEFT and RIGHT sides in X
# IN port: higher X (right side), OUT port: lower X (left side)
# Ports are at the pump center Yd (visible from above at head end)
PORT_PLAN_YD = PUMP_YD_START + PP_D / 2  # pump center depth in Yd

# Top row (solid — visible from above)
pumps_solid = [
    (P01_X + PUMP_BODY_W / 2, PUMP_YD_START, "P-01", C_BLUE,  "BLUE SUPPLY"),
    (P02_X + PUMP_BODY_W / 2, PUMP_YD_START, "P-02", C_BROWN, "BROWN RECYCLE"),
]
# P-04 (ghost — hidden below top row, centered in frame); P-03 relocated to IBC corridor
pumps_ghost = [
    (P04_X + PUMP_BODY_W / 2, PUMP_YD_START + GHOST_YD_OFFSET, "P-04", C_BLACK_SYS, "TRAY DRAIN\n(CENTERED BELOW)"),
]

def _plan_pump_ports(pcx, pyd):
    """Return (in_x, in_yd, out_x, out_yd) for plan view port positions."""
    port_yd = pyd + PP_D / 2
    in_x = pcx + PP_W / 2    # right edge of body (port included in 127mm)
    out_x = pcx - PP_W / 2   # left edge of body
    return in_x, port_yd, out_x, port_yd

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
    # Ports — ghost (on LEFT and RIGHT sides in X)
    p_in_x, p_in_yd, p_out_x, p_out_yd = _plan_pump_ports(pcx, pyd)
    ax3.add_patch(plt.Circle((sp_x(p_in_x), sp_y(p_in_yd)), PP_PORT_R / SC_B,
                  fc="white", ec=pcolor, lw=0.8, alpha=GHOST_ALPHA, zorder=3))
    ax3.add_patch(plt.Circle((sp_x(p_out_x), sp_y(p_out_yd)), PP_PORT_R / SC_B,
                  fc="white", ec=pcolor, lw=0.8, alpha=GHOST_ALPHA, zorder=3))

# Draw solid pumps on top
for pcx, pyd, plabel, pcolor, psub in pumps_solid:
    ax3.add_patch(plt.Rectangle(
        (sp_x(pcx - PP_W / 2), sp_y(pyd + PP_D)),
        PP_W / SC_B, PP_D / SC_B,
        fc=pcolor, ec=C_FRAME, lw=1.2, alpha=0.8, zorder=5))
    ax3.text(sp_x(pcx), sp_y(pyd + PP_D / 2),
             plabel, ha="center", va="center",
             fontsize=5.5, color="white", fontweight="bold", zorder=6)
    ax3.text(sp_x(pcx), sp_y(pyd + PP_D + 8),
             psub, ha="center", va="top",
             fontsize=3.5, color=pcolor, fontweight="bold", zorder=6)
    # Port indicators — circles at body edges (ports within 127mm envelope)
    p_in_x, p_in_yd, p_out_x, p_out_yd = _plan_pump_ports(pcx, pyd)
    ax3.add_patch(plt.Circle((sp_x(p_in_x), sp_y(p_in_yd)),
                  PP_PORT_R / SC_B, fc="#CCCCCC", ec=C_FRAME, lw=0.8, zorder=6))
    ax3.add_patch(plt.Circle((sp_x(p_out_x), sp_y(p_out_yd)),
                  PP_PORT_R / SC_B, fc="#CCCCCC", ec=C_FRAME, lw=0.8, zorder=6))
    # Port labels
    ax3.text(sp_x(p_in_x + 15), sp_y(p_in_yd), "IN", ha="left", va="center",
             fontsize=3.5, fontweight="bold", color=C_FRAME, zorder=8)
    ax3.text(sp_x(p_out_x - 15), sp_y(p_out_yd), "OUT", ha="right", va="center",
             fontsize=3.5, fontweight="bold", color=C_FRAME, zorder=8)

# ── ACC-01 from above ───────────────────────────────────────────────────────
ACC_PLAN_R = 57   # tank half-depth in plan (~114mm H from spec)
acc_plan_cx = FRAME_R + 60             # to the right of the frame
acc_plan_cy = PUMP_YD_START + PP_D / 2  # at pump center depth
ax3.add_patch(plt.Circle((sp_x(acc_plan_cx), sp_y(acc_plan_cy)),
              ACC_PLAN_R / SC_B, fc=C_ACC, ec=C_FRAME, lw=1.5, alpha=0.8, zorder=5))
ax3.text(sp_x(acc_plan_cx), sp_y(acc_plan_cy), "ACC-01",
         ha="center", va="center", fontsize=4.5, fontweight="bold",
         color="white", zorder=6)

# ── Valve position constants (needed before pipe routing) ──────────────────
bv01_plan_x = FRAME_R + 60             # outside frame, right
bv01_plan_yd = PORT_PLAN_YD            # on blue supply line
bv_plan_r = 12
bv02_plan_x = FRAME_R + 60             # outside frame, right
bv02_plan_yd = acc_plan_cy             # on blue discharge line
dv02_plan_x = DV02_X                   # matches elevation DV-02 X position
dv02_plan_yd = PORT_PLAN_YD            # on tray drain discharge line
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
# Pump center X positions
p01_cx = P01_X + PUMP_BODY_W / 2
p02_cx = P02_X + PUMP_BODY_W / 2
p04_cx = P04_X + PUMP_BODY_W / 2

# Exit points
EXIT_X_R = 3100   # right exit (toward IBCs)
EXIT_X_L = 2200   # left exit (toward lower X / ext drain)
EXIT_YD_BOT = MANIFOLD_DEPTH + 150  # below frame (from walkway side)

# Plan-view port positions for P-01 and P-02
p01_plan_in_x, p01_plan_in_yd, p01_plan_out_x, p01_plan_out_yd = _plan_pump_ports(p01_cx, PUMP_YD_START)
p02_plan_in_x, p02_plan_in_yd, p02_plan_out_x, p02_plan_out_yd = _plan_pump_ports(p02_cx, PUMP_YD_START)

# Pipes connect to ports on LEFT (OUT) and RIGHT (IN) sides in X
# In plan view, pipes approach from the right (toward IBCs) or left

# ── Blue supply: from IBC (½") → BV-01 → P-01 IN ────────────────────────
draw_pipe_path_plan(ax3,
    [EXIT_X_R, bv01_plan_x + bv_plan_r],
    [PORT_PLAN_YD, PORT_PLAN_YD],
    OD_H, WALL_H, fc=C_BLUE, zorder=4)
draw_pipe_path_plan(ax3,
    [bv01_plan_x - bv_plan_r, p01_plan_in_x],
    [PORT_PLAN_YD, PORT_PLAN_YD],
    OD_H, WALL_H, fc=C_BLUE, zorder=4)
ax3.text(sp_x(EXIT_X_R + 10), sp_y(PORT_PLAN_YD),
         "FROM IBC-1/2\n(BLUE — ½\")",
         ha="left", va="center", fontsize=4, color=C_BLUE, fontweight="bold")

# ── Blue discharge: P-01 OUT (½") → ACC-01 → BV-02 → spray bar ──────────
draw_pipe_path_plan(ax3,
    [p01_plan_out_x, p01_plan_out_x, acc_plan_cx - ACC_PLAN_R],
    [PORT_PLAN_YD, acc_plan_cy, acc_plan_cy],
    OD_H, WALL_H, fc=C_BLUE, zorder=4)
draw_pipe_path_plan(ax3,
    [acc_plan_cx + ACC_PLAN_R, bv02_plan_x - bv_plan_r],
    [acc_plan_cy, acc_plan_cy],
    OD_H, WALL_H, fc=C_BLUE, zorder=4)
draw_pipe_path_plan(ax3,
    [bv02_plan_x + bv_plan_r, EXIT_X_R],
    [bv02_plan_yd, bv02_plan_yd],
    OD_H, WALL_H, fc=C_BLUE, zorder=4)
ax3.text(sp_x(EXIT_X_R + 10), sp_y(bv02_plan_yd),
         "TO SPRAY BAR (½\")",
         ha="left", va="center", fontsize=4, color=C_BLUE, fontweight="bold")

# ── Brown suction: IBC-3 (½") → P-02 IN ─────────────────────────────────
BROWN_PLAN_YD = PORT_PLAN_YD + 30
draw_pipe_path_plan(ax3,
    [EXIT_X_R, FRAME_R + 10],
    [BROWN_PLAN_YD, BROWN_PLAN_YD],
    OD_H, WALL_H, fc=C_BROWN, zorder=4)
draw_pipe_path_plan(ax3,
    [FRAME_R + 10, p02_plan_in_x, p02_plan_in_x],
    [BROWN_PLAN_YD, BROWN_PLAN_YD, PORT_PLAN_YD],
    OD_H, WALL_H, fc=C_BROWN, zorder=4)
ax3.text(sp_x(EXIT_X_R + 10), sp_y(BROWN_PLAN_YD),
         "FROM IBC-3\n(BROWN — ½\")",
         ha="left", va="center", fontsize=4, color=C_BROWN, fontweight="bold")

# ── Brown discharge: P-02 OUT (1/2") → riser to filter skid ─────────────
# Pipe runs from P-02 OUT toward the wall, then rises vertically (Z).
# In plan view a vertical riser appears as a filled circle (pipe cross-section).
RISER_PLAN_YD = 10  # just inside the wall, not through it
draw_pipe_path_plan(ax3,
    [p02_plan_out_x, p02_plan_out_x],
    [PORT_PLAN_YD, RISER_PLAN_YD],
    OD_H, WALL_H, fc=C_BROWN, zorder=4)
# Riser symbol: concentric circles (pipe cross-section going up in Z)
ax3.add_patch(plt.Circle((sp_x(p02_plan_out_x), sp_y(RISER_PLAN_YD)),
              OD_H / 2 / SC_B, fc=C_BROWN, ec=C_FRAME, lw=1.5, zorder=9))
ax3.add_patch(plt.Circle((sp_x(p02_plan_out_x), sp_y(RISER_PLAN_YD)),
              (OD_H / 2 - WALL_H) / SC_B, fc="white", ec=C_FRAME, lw=0.8, zorder=9.5))
ax3.plot(sp_x(p02_plan_out_x), sp_y(RISER_PLAN_YD), '+',
         color=C_FRAME, markersize=6, mew=1.2, zorder=10)
ax3.text(sp_x(p02_plan_out_x), sp_y(RISER_PLAN_YD - 18),
         "RISER TO\nFILTER SKID",
         ha="center", va="top", fontsize=4, color=C_BROWN, fontweight="bold")

# ── Ghost pipes: P-03 and P-04 connections (hidden below top row) ──────────
GHOST_PIPE_ALPHA_PLAN = 0.3
GHOST_PIPE_LW_PLAN = 2.0

def ghost_pipe(x_pts, yd_pts, color):
    """Draw a ghosted pipe as a dashed centerline (not filled parallel walls)."""
    ax3.plot([sp_x(x) for x in x_pts], [sp_y(y) for y in yd_pts],
             color=color, lw=GHOST_PIPE_LW_PLAN, ls=(0, (5, 4)),
             alpha=GHOST_PIPE_ALPHA_PLAN, zorder=3)

def ghost_label(x, yd, text, color, ha="left", va="center"):
    ax3.text(sp_x(x), sp_y(yd), text, ha=ha, va=va,
             fontsize=3.5, color=color, fontweight="bold", alpha=0.4)

# Tray drain suction: tray sump → P-04 IN (ghost) — at P-04 center X
p04_cx = P04_X + PUMP_BODY_W / 2
p04_plan_in_x = P04_X + PUMP_BODY_W  # IN port on right side
ghost_pipe([EXIT_X_R, p04_plan_in_x], [EXIT_YD_BOT, PORT_PLAN_YD], C_BLACK_SYS)
ghost_label(EXIT_X_R + 10, EXIT_YD_BOT + 15, "FROM TRAY\nSUMP", C_BLACK_SYS, ha="left", va="top")

# Tray drain discharge: P-04 OUT → DV-02 → IBC-3/IBC-4 (ghost)
p04_plan_out_x = P04_X  # OUT port on left side
ghost_pipe([p04_plan_out_x, dv02_plan_x + dv_plan_r], [PORT_PLAN_YD, dv02_plan_yd], C_BROWN)
ghost_pipe([dv02_plan_x - dv_plan_r, EXIT_X_R], [dv02_plan_yd, dv02_plan_yd + 30], C_BROWN)
ghost_label(EXIT_X_R + 10, dv02_plan_yd + 30, "VIA DV-02 TO\nIBC-3 or IBC-4", C_BROWN, ha="left")

# ── BV-01 and BV-02 symbols in plan ─────────────────────────────────────────
# (positions defined above with pipe routing constants)
bv_pts_x = [sp_x(bv01_plan_x), sp_x(bv01_plan_x + bv_plan_r),
            sp_x(bv01_plan_x), sp_x(bv01_plan_x - bv_plan_r)]
bv_pts_y = [sp_y(bv01_plan_yd + bv_plan_r), sp_y(bv01_plan_yd),
            sp_y(bv01_plan_yd - bv_plan_r), sp_y(bv01_plan_yd)]
ax3.add_patch(plt.Polygon(list(zip(bv_pts_x, bv_pts_y)),
              fc=C_VALVE, ec=C_FRAME, lw=1.2, alpha=0.8, zorder=9))
ax3.text(sp_x(bv01_plan_x), sp_y(bv01_plan_yd - 18), "BV-01",
         ha="center", va="top", fontsize=4, color=C_VALVE, fontweight="bold")

# BV-02 on Blue discharge line
bv2_pts_x = [sp_x(bv02_plan_x), sp_x(bv02_plan_x + bv_plan_r),
             sp_x(bv02_plan_x), sp_x(bv02_plan_x - bv_plan_r)]
bv2_pts_y = [sp_y(bv02_plan_yd + bv_plan_r), sp_y(bv02_plan_yd),
             sp_y(bv02_plan_yd - bv_plan_r), sp_y(bv02_plan_yd)]
ax3.add_patch(plt.Polygon(list(zip(bv2_pts_x, bv2_pts_y)),
              fc=C_VALVE, ec=C_FRAME, lw=1.2, alpha=0.8, zorder=9))
ax3.text(sp_x(bv02_plan_x), sp_y(bv02_plan_yd - 18), "BV-02",
         ha="center", va="top", fontsize=4, color=C_VALVE, fontweight="bold")

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
           f"{FRAME_W}mm", offset=0.25, fs=5)

# Frame depth from wall
draw_dim_v(ax3, sp_x(FRAME_X - 30), sp_y(MANIFOLD_DEPTH), sp_y(0),
           f"{MANIFOLD_DEPTH}mm\nDEPTH", offset=0.25, fs=4.5)


# ── Title block ──────────────────────────────────────────────────────────────
title_block(ax, "SHEET 1 OF 1",
            drawing_title="PUMP MANIFOLD — PLUMBING ELEVATION",
            subtitle="INTERIOR VIEW LOOKING AT PINHOLE WALL (Yd=0)",
            scale_note="ELEV 1:5  |  DETAIL A ~1:4.5  |  DETAIL B (PLAN) ~1:5.5  |  ALL DIMS IN mm",
            doc_id="TBS-001 · Water System — Pump Manifold Detail",
            height=0.04)

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
