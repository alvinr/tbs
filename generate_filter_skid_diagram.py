#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_filter_skid_diagram.py
Generates a detailed plumbing diagram of the filter skid assembly mounted on
the pinhole wall (Yd=0).

Sheet 1 — Filter Skid Elevation (1:5)
  View from inside the container looking at the pinhole wall.
  X axis horizontal, Z axis vertical.
  Shows: slotted angle frame, three Big Blue 4.5"×10" housings (F1/F2/F3),
         P-02 pump, all 1" HDPE connecting pipes with parallel-wall drawing,
         pH test point, DV-01 diverter valve, dimensions and leader callouts.

Output:
  diagrams/filter-skid-sheet1.png  (1800 x 1200 px, 150 dpi)
"""

import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Arc

from tbs_constants import (
    C_OUT, C_CL, C_DIM, C_ALUM, C_STEEL, C_GASKT,
    FSKID_X, FSKID_W, FSKID_Z_LO, FSKID_Z_HI, FSKID_H,
    BB_OD, BB_H, BB_HEAD_H, BB_PORT_SEP,
    F1_X, F2_X, F3_X, FILT_HEAD_Z, FILT_SUMP_Z,
    FILT_PIPE_OD, FILT_PIPE_WALL,
    svg_path,
)
from tbs_title_block import title_block
from tbs_drawing import (
    draw_dim_h, draw_dim_v, leader, draw_rect, hatch_rect,
    place_label, register_pipe, reset_label_registry,
)

# ── Color palette ─────────────────────────────────────────────────────────────
C_FRAME  = "#1A1A1A"     # structural outlines
C_STEEL_FILL = "#B0B0B8" # steel section fill
C_HDPE   = "#4A7A4A"     # HDPE pipe fill (green-grey)
C_HOUSING = "#3366AA"    # filter housing fill (blue plastic)
C_HEAD   = "#555555"     # filter head (cast reinforced nylon)
C_PUMP   = "#CC4444"     # pump symbol
C_BROWN  = "#8B5E3C"     # brown system color
C_BLUE   = "#2979B8"     # blue system color
C_TEXT   = "#1A1A1A"     # general text
C_BG     = "#F5F5F0"     # background

# ── Scale: 1:5 ───────────────────────────────────────────────────────────────
SC = 5.0  # mm per drawing unit

# Drawing origin offsets (data units) — position the frame nicely in the figure
OX = 3.0   # X origin offset
OZ = 2.0   # Z origin offset

def sx(x_mm):
    """Convert X position in mm to drawing x coordinate."""
    return OX + (x_mm - FSKID_X + 100) / SC  # 100mm margin left of frame

def sz(z_mm):
    """Convert Z position in mm to drawing y coordinate."""
    return OZ + z_mm / SC


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — FILTER SKID ELEVATION (1:5)
# View from inside container looking at pinhole wall (Yd=0)
# X horizontal, Z vertical
# ═══════════════════════════════════════════════════════════════════════════════

from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(20, 12))
fig.patch.set_facecolor(C_BG)
gs = GridSpec(1, 2, figure=fig, width_ratios=[2.2, 1], wspace=0.06)

ax = fig.add_subplot(gs[0, 0])   # Main elevation
ax.set_facecolor(C_BG)
ax.set_aspect("equal")
ax.axis("off")

ax2 = fig.add_subplot(gs[0, 1])  # Detail cross-section
ax2.set_facecolor(C_BG)
ax2.set_aspect("equal")
ax2.axis("off")

# Set axis limits — main elevation
ax.set_xlim(sx(2600) - 1, sx(4200) + 1)
ax.set_ylim(sz(-100) - 1, sz(1000) + 2)

# Reset label registry for collision avoidance
reset_label_registry()

# ── Container wall context (corrugated profile) ──────────────────────────────
# Corrugation ribs at 457mm spacing — show as vertical dashed lines
CORR_SPACING = 457
for rib_x in range(2742, 3900, CORR_SPACING):  # ribs near our zone
    ax.plot([sx(rib_x), sx(rib_x)], [sz(0), sz(900)],
            color="#AAAAAA", lw=0.6, ls="--", zorder=1)

# Wall face (horizontal line at Yd=0, shown as the background)
ax.axhline(sz(0), color="#888888", lw=1.0, ls="-", xmin=0.02, xmax=0.98, zorder=1)
ax.text(sx(2750), sz(-30), "CONTAINER FLOOR", ha="left", va="top",
        fontsize=6, color="#888888", style="italic")

# ── Slotted angle frame ──────────────────────────────────────────────────────
# 25×25×3mm slotted steel angle — draw as rectangle outline with steel fill
FRAME_LW = 2.0
ANGLE_W = 25  # angle width in mm

# Bottom rail
ax.add_patch(plt.Rectangle((sx(FSKID_X), sz(FSKID_Z_LO)),
             FSKID_W / SC, ANGLE_W / SC,
             fc=C_STEEL_FILL, ec=C_FRAME, lw=FRAME_LW, zorder=3))

# Top rail
ax.add_patch(plt.Rectangle((sx(FSKID_X), sz(FSKID_Z_HI - ANGLE_W)),
             FSKID_W / SC, ANGLE_W / SC,
             fc=C_STEEL_FILL, ec=C_FRAME, lw=FRAME_LW, zorder=3))

# Left upright
ax.add_patch(plt.Rectangle((sx(FSKID_X), sz(FSKID_Z_LO)),
             ANGLE_W / SC, FSKID_H / SC,
             fc=C_STEEL_FILL, ec=C_FRAME, lw=FRAME_LW, zorder=3))

# Right upright
ax.add_patch(plt.Rectangle((sx(FSKID_X + FSKID_W - ANGLE_W), sz(FSKID_Z_LO)),
             ANGLE_W / SC, FSKID_H / SC,
             fc=C_STEEL_FILL, ec=C_FRAME, lw=FRAME_LW, zorder=3))

# Slot pattern indication (decorative dashes in uprights)
for upright_x in [FSKID_X + ANGLE_W / 2, FSKID_X + FSKID_W - ANGLE_W / 2]:
    for slot_z in range(250, 700, 80):
        ax.plot([sx(upright_x), sx(upright_x)],
                [sz(slot_z), sz(slot_z + 40)],
                color="#666666", lw=1.0, zorder=4)

# ── Backing board (18mm plywood) ─────────────────────────────────────────────
# Sits inside the frame, behind the filter housings — easy mounting surface
PLY_T = 18  # plywood thickness in mm
C_PLY = "#D4C8A0"  # plywood fill color
# The board spans the full inner frame width and height
ply_x = FSKID_X + ANGLE_W
ply_w = FSKID_W - 2 * ANGLE_W
ply_z = FSKID_Z_LO + ANGLE_W
ply_h = FSKID_H - 2 * ANGLE_W
ax.add_patch(plt.Rectangle((sx(ply_x), sz(ply_z)),
             ply_w / SC, ply_h / SC,
             fc=C_PLY, ec="#A09060", lw=1.0, alpha=0.5, zorder=2.5))

# ── Wall mounting brackets ───────────────────────────────────────────────────
# L-brackets connecting frame to container ribs
BRACKET_W = 50
BRACKET_H = 80
for bz in [FSKID_Z_LO + 50, FSKID_Z_HI - 80]:
    for bx in [FSKID_X - BRACKET_W, FSKID_X + FSKID_W]:
        ax.add_patch(plt.Rectangle((sx(bx), sz(bz)),
                     BRACKET_W / SC, BRACKET_H / SC,
                     fc="#D0D0D0", ec=C_FRAME, lw=1.2, zorder=2))
        # Bolt symbol
        bolt_cx = bx + BRACKET_W / 2
        bolt_cz = bz + BRACKET_H / 2
        ax.plot(sx(bolt_cx), sz(bolt_cz), 'x', color=C_FRAME,
                markersize=5, mew=1.5, zorder=4)


# ── Big Blue filter housings ─────────────────────────────────────────────────
def draw_filter_housing(ax, cx_mm, label, filter_type):
    """Draw a Big Blue 4.5x10 filter housing in elevation.

    cx_mm: center X position in mm
    """
    # Housing body (sump bowl) — cylindrical, shown as rectangle in elevation
    body_w = BB_OD
    body_h = BB_H - BB_HEAD_H
    body_z_bot = FILT_SUMP_Z
    body_z_top = FILT_HEAD_Z - BB_HEAD_H

    # Sump bowl (translucent blue plastic)
    ax.add_patch(plt.Rectangle(
        (sx(cx_mm - body_w / 2), sz(body_z_bot)),
        body_w / SC, body_h / SC,
        fc=C_HOUSING, ec=C_FRAME, lw=1.5, alpha=0.6, zorder=5))

    # Rounded bottom of sump
    arc_r = body_w / 2
    theta = np.linspace(180, 360, 40)
    arc_x = sx(cx_mm) + (arc_r / SC) * np.cos(np.radians(theta))
    arc_z = sz(body_z_bot) + (arc_r / SC) * np.sin(np.radians(theta)) + arc_r / SC
    ax.plot(arc_x, arc_z, color=C_FRAME, lw=1.5, zorder=5)

    # Head (reinforced nylon, darker)
    head_z_bot = FILT_HEAD_Z - BB_HEAD_H
    ax.add_patch(plt.Rectangle(
        (sx(cx_mm - body_w / 2), sz(head_z_bot)),
        body_w / SC, BB_HEAD_H / SC,
        fc=C_HEAD, ec=C_FRAME, lw=1.8, zorder=6))

    # Mounting bracket — steel U-bracket screwed through backing board
    # The bracket wraps around the head and bolts to the 18mm ply
    bracket_w = body_w + 20   # bracket width (wider than housing)
    bracket_h = 12            # bracket thickness
    bracket_tab = 30          # tab height extending above/below head

    # Horizontal bar across top of head
    ax.add_patch(plt.Rectangle(
        (sx(cx_mm - bracket_w / 2), sz(FILT_HEAD_Z)),
        bracket_w / SC, bracket_h / SC,
        fc="#999999", ec=C_FRAME, lw=1.2, zorder=7))

    # Left tab (down from bar, alongside housing)
    ax.add_patch(plt.Rectangle(
        (sx(cx_mm - bracket_w / 2), sz(FILT_HEAD_Z - bracket_tab)),
        bracket_h / SC, (bracket_tab + bracket_h) / SC,
        fc="#999999", ec=C_FRAME, lw=1.0, zorder=7))

    # Right tab (down from bar, alongside housing)
    ax.add_patch(plt.Rectangle(
        (sx(cx_mm + bracket_w / 2 - bracket_h), sz(FILT_HEAD_Z - bracket_tab)),
        bracket_h / SC, (bracket_tab + bracket_h) / SC,
        fc="#999999", ec=C_FRAME, lw=1.0, zorder=7))

    # HDPE spacer blocks (25mm standoff between bracket and backing board)
    # Visible in elevation as small rectangles behind bracket tabs
    SPACER_D = 25   # spacer depth (Yd direction — not visible in elevation)
    SPACER_H = 40   # spacer height (visible)
    SPACER_W = 20   # spacer width (visible, slightly wider than bracket tab)
    spacer_z = FILT_HEAD_Z - bracket_tab - 5
    for sp_x in [cx_mm - bracket_w / 2 - 4,
                 cx_mm + bracket_w / 2 - SPACER_W + 4]:
        ax.add_patch(plt.Rectangle(
            (sx(sp_x), sz(spacer_z)),
            SPACER_W / SC, SPACER_H / SC,
            fc="#E0D8B0", ec="#A09060", lw=0.8, zorder=3,
            hatch=".."))

    # Bolt symbols through tabs + spacers into backing board (2 per bracket)
    for bolt_x in [cx_mm - bracket_w / 2 + bracket_h / 2,
                   cx_mm + bracket_w / 2 - bracket_h / 2]:
        bolt_z = FILT_HEAD_Z - bracket_tab + 10
        ax.plot(sx(bolt_x), sz(bolt_z), 'x', color=C_FRAME,
                markersize=4, mew=1.2, zorder=8)

    # Clamp band at sump/head junction (existing from Big Blue kit)
    clamp_h = 15
    ax.add_patch(plt.Rectangle(
        (sx(cx_mm - body_w / 2 - 8), sz(head_z_bot - clamp_h)),
        (body_w + 16) / SC, clamp_h / SC,
        fc="#888888", ec=C_FRAME, lw=1.0, zorder=6))

    # IN port (left side of head)
    port_z = FILT_HEAD_Z - BB_HEAD_H / 2
    in_x = cx_mm - BB_PORT_SEP / 2
    out_x = cx_mm + BB_PORT_SEP / 2

    # Port circles (1" NPT)
    port_r = 12  # visual radius for port indication
    ax.add_patch(plt.Circle((sx(in_x), sz(port_z)), port_r / SC,
                 fc="white", ec=C_FRAME, lw=1.2, zorder=7))
    ax.add_patch(plt.Circle((sx(out_x), sz(port_z)), port_r / SC,
                 fc="white", ec=C_FRAME, lw=1.2, zorder=7))

    # Port labels
    ax.text(sx(in_x), sz(port_z), "IN", ha="center", va="center",
            fontsize=4.5, fontweight="bold", color=C_FRAME, zorder=8)
    ax.text(sx(out_x), sz(port_z), "OUT", ha="center", va="center",
            fontsize=4.5, fontweight="bold", color=C_FRAME, zorder=8)

    # Filter label below housing
    place_label(ax, sx(cx_mm), sz(body_z_bot - 30), f"{label}\n{filter_type}",
                component='filter', fontsize=7, color=C_TEXT,
                dx=0, dy=-0.8, ha='center', va='top')

    # Register pipe endpoints for collision avoidance
    register_pipe(sx(in_x), sz(port_z), sx(in_x), sz(port_z + 50))
    register_pipe(sx(out_x), sz(port_z), sx(out_x), sz(port_z + 50))

    return in_x, out_x, port_z


# Draw three filter housings
f1_in, f1_out, f_port_z = draw_filter_housing(ax, F1_X, "F1", "50μ SEDIMENT")
f2_in, f2_out, _        = draw_filter_housing(ax, F2_X, "F2", "5μ SEDIMENT")
f3_in, f3_out, _        = draw_filter_housing(ax, F3_X, "F3", "GAC CARBON")


# ── Pipe drawing helper (parallel-wall style) ────────────────────────────────
def draw_pipe_path(ax, x_pts, z_pts, od_mm, wall_mm,
                   fc=C_HDPE, ec=C_FRAME, bore_fc="white",
                   elbow_r=None, zorder=8):
    """Draw a pipe run with parallel walls — adapted for this diagram's scale.

    x_pts, z_pts: waypoint coordinates in mm (before scaling)
    """
    n = len(x_pts)
    if n < 2:
        return
    half_od = od_mm / 2.0
    half_id = half_od - wall_mm
    if elbow_r is None:
        elbow_r = od_mm * 1.0

    # Segment directions
    segs = []
    for i in range(n - 1):
        dx = x_pts[i + 1] - x_pts[i]
        dz = z_pts[i + 1] - z_pts[i]
        length = max(math.hypot(dx, dz), 1e-6)
        segs.append((dx / length, dz / length, length))

    # Elbow geometry at each intermediate waypoint
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
        cz = tp_z + nz * r_eff

        start_a = math.atan2(tp_z - cz, tp_x - cy)
        sweep = turn if cross > 0 else -turn

        elbows.append({
            'tangent': tangent,
            'r': r_eff,
            'center': (cy, cz),
            'start': start_a,
            'sweep': sweep,
        })

    # Draw straight sections
    def _rect(sx0, sz0, sx1, sz1, nx, nz, half_r, color, z_ord):
        pts = [(sx(sx0 + nx * half_r), sz(sz0 + nz * half_r)),
               (sx(sx1 + nx * half_r), sz(sz1 + nz * half_r)),
               (sx(sx1 - nx * half_r), sz(sz1 - nz * half_r)),
               (sx(sx0 - nx * half_r), sz(sz0 - nz * half_r))]
        ax.fill([p[0] for p in pts], [p[1] for p in pts],
                fc=color, ec=ec if color != bore_fc else "none",
                lw=0.8 if color != bore_fc else 0,
                zorder=z_ord)

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

    # Draw elbow fittings
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
            ox = [sx(_cy + r_out * math.cos(a)) for a in _angles]
            oz = [sz(_cz + r_out * math.sin(a)) for a in _angles]
            ix = [sx(_cy + r_in * math.cos(a)) for a in _angles]
            iz = [sz(_cz + r_in * math.sin(a)) for a in _angles]
            ax.fill(ox + ix[::-1], oz + iz[::-1],
                    fc=color, ec=ec if color != bore_fc else "none",
                    lw=0.8 if color != bore_fc else 0,
                    zorder=z_ord)

        _arc_ring(r_eff + half_od, max(r_eff - half_od, 0.5), fc, zorder)
        _arc_ring(r_eff + half_id, max(r_eff - half_id, 0.5), bore_fc, zorder + 1)


# ── P-02 pump ────────────────────────────────────────────────────────────────
# P-02 is in the pump manifold zone, left of the filter skid
# Position: X=2750, Z=400 (center)
P02_X = 2750
P02_Z = 400
P02_R = 60  # pump body radius in mm

# Pump body (circle)
ax.add_patch(plt.Circle((sx(P02_X), sz(P02_Z)), P02_R / SC,
             fc="#FFDDDD", ec=C_PUMP, lw=2.5, zorder=6))

# Pump impeller indication (arc arrow)
imp_r = P02_R * 0.6
theta_imp = np.linspace(30, 300, 50)
ax.plot(sx(P02_X) + (imp_r / SC) * np.cos(np.radians(theta_imp)),
        sz(P02_Z) + (imp_r / SC) * np.sin(np.radians(theta_imp)),
        color=C_PUMP, lw=1.5, zorder=7)

# Pump label
place_label(ax, sx(P02_X), sz(P02_Z), "P-02\n(12V DIAPHRAGM)",
            component='pump', fontsize=6.5, color=C_PUMP,
            dx=-0.5, dy=-2.5, ha='center', va='top')

# Pump suction port (bottom) and discharge port (right)
P02_SUCTION_Z = P02_Z - P02_R   # bottom
P02_DISCHARGE_X = P02_X + P02_R  # right side

# ── Pipe routing ─────────────────────────────────────────────────────────────
# Flow path: IBC-3 → P-02 suction (from below) → P-02 discharge → F1 IN →
#            F1 OUT → F2 IN → F2 OUT → F3 IN → F3 OUT → pH test → DV-01

OD = FILT_PIPE_OD    # 33mm
WALL = FILT_PIPE_WALL  # 4mm

# Port Z position for all filters
PORT_Z = FILT_HEAD_Z - BB_HEAD_H / 2  # 680 - 35 = 645mm

# Header height (horizontal pipe run above filter heads connecting them)
HEADER_Z = FILT_HEAD_Z + 60  # 740mm — above heads with clearance

# ── Suction pipe: from bottom (IBC-3 supply) up to P-02 ──────────────────────
draw_pipe_path(ax,
    [P02_X, P02_X],
    [100, P02_SUCTION_Z],
    OD, WALL, fc=C_BROWN)

# Suction annotation
ax.annotate("", xy=(sx(P02_X), sz(130)), xytext=(sx(P02_X), sz(200)),
            arrowprops=dict(arrowstyle="-|>", color=C_BROWN, lw=1.5), zorder=10)
ax.text(sx(P02_X), sz(60), "FROM IBC-3\n(BROWN RETURN)",
        ha="center", va="top", fontsize=6, color=C_BROWN, style="italic")

# ── Discharge pipe: P-02 right → up to header → right to F1 IN → down to port
draw_pipe_path(ax,
    [P02_DISCHARGE_X, P02_DISCHARGE_X + 50, P02_DISCHARGE_X + 50, f1_in, f1_in],
    [P02_Z, P02_Z, HEADER_Z, HEADER_Z, PORT_Z],
    OD, WALL)

# ── F1 OUT → F2 IN (via header) ─────────────────────────────────────────────
draw_pipe_path(ax,
    [f1_out, f1_out, f2_in, f2_in],
    [PORT_Z, HEADER_Z, HEADER_Z, PORT_Z],
    OD, WALL)

# ── F2 OUT → F3 IN (via header) ─────────────────────────────────────────────
draw_pipe_path(ax,
    [f2_out, f2_out, f3_in, f3_in],
    [PORT_Z, HEADER_Z, HEADER_Z, PORT_Z],
    OD, WALL)

# ── F3 OUT → pH test point → DV-01 ──────────────────────────────────────────
# pH test point: inline tee with probe pocket, positioned after F3
PH_TEST_X = F3_X + 200  # 3850mm
PH_TEST_Z = PORT_Z

# Pipe from F3 OUT up to header, right to pH test point, down, and on to DV-01
# Single path so elbows render at all turns
DV01_X = PH_TEST_X + 150  # 4000mm
DV01_Z = PORT_Z
DV01_R = 50  # valve body radius

draw_pipe_path(ax,
    [f3_out, f3_out, PH_TEST_X, PH_TEST_X, DV01_X - DV01_R],
    [PORT_Z, HEADER_Z, HEADER_Z, PORT_Z, PORT_Z],
    OD, WALL)

# ── pH test point symbol ─────────────────────────────────────────────────────
# Draw as a tee with upward stub (probe insertion point)
PH_STUB_H = 80  # stub height

# Vertical stub from pipe
draw_pipe_path(ax,
    [PH_TEST_X, PH_TEST_X],
    [PORT_Z, PORT_Z + PH_STUB_H],
    OD, WALL)

# Probe cap (circle at top of stub)
cap_r = 18
ax.add_patch(plt.Circle((sx(PH_TEST_X), sz(PORT_Z + PH_STUB_H + cap_r)),
             cap_r / SC, fc="#FFFFCC", ec=C_FRAME, lw=1.5, zorder=8))
ax.text(sx(PH_TEST_X), sz(PORT_Z + PH_STUB_H + cap_r), "pH",
        ha="center", va="center", fontsize=5.5, fontweight="bold", zorder=9)

# pH test label
place_label(ax, sx(PH_TEST_X), sz(PORT_Z + PH_STUB_H + cap_r),
            "pH TEST\nPOINT", component='generic', fontsize=6, color=C_TEXT,
            dx=1.5, dy=0.5, ha='left', va='center')

# DV-01 body (diamond shape for 3-way valve)
dv_pts_x = [sx(DV01_X), sx(DV01_X + DV01_R), sx(DV01_X), sx(DV01_X - DV01_R)]
dv_pts_z = [sz(DV01_Z + DV01_R), sz(DV01_Z), sz(DV01_Z - DV01_R), sz(DV01_Z)]
dv_poly = plt.Polygon(list(zip(dv_pts_x, dv_pts_z)),
                       fc="white", ec=C_FRAME, lw=2.0, zorder=8)
ax.add_patch(dv_poly)
ax.text(sx(DV01_X), sz(DV01_Z), "3W", ha="center", va="center",
        fontsize=5, fontweight="bold", color=C_FRAME, zorder=9)

# DV-01 label
place_label(ax, sx(DV01_X), sz(DV01_Z), "DV-01\n(3-WAY DIVERTER)",
            component='diverter', fontsize=6, color=C_TEXT,
            dx=0, dy=-2.5, ha='center', va='top')

# DV-01 outputs
# Top output → Blue system (clean)
draw_pipe_path(ax,
    [DV01_X, DV01_X],
    [DV01_Z + DV01_R, DV01_Z + DV01_R + 100],
    OD, WALL, fc=C_BLUE)
ax.text(sx(DV01_X + 20), sz(DV01_Z + DV01_R + 120), "→ BLUE\n  (pH 6.5–8.0)",
        ha="left", va="bottom", fontsize=5.5, color=C_BLUE, fontweight="bold")

# Right output → Black system (waste)
draw_pipe_path(ax,
    [DV01_X + DV01_R, DV01_X + DV01_R + 80],
    [DV01_Z, DV01_Z],
    OD, WALL, fc="#333333")
ax.text(sx(DV01_X + DV01_R + 90), sz(DV01_Z), "→ BLACK\n  (pH outside range)",
        ha="left", va="center", fontsize=5.5, color="#333333", fontweight="bold")

# ── Flow arrows on header ────────────────────────────────────────────────────
arrow_style = dict(arrowstyle="-|>", color=C_HDPE, lw=1.8, mutation_scale=10)
# Arrow between P-02 discharge and F1
mid_x1 = (P02_DISCHARGE_X + 50 + f1_in) / 2
ax.annotate("", xy=(sx(mid_x1 + 30), sz(HEADER_Z)),
            xytext=(sx(mid_x1 - 30), sz(HEADER_Z)),
            arrowprops=arrow_style, zorder=12)

# Arrow between F1 and F2
mid_x2 = (f1_out + f2_in) / 2
ax.annotate("", xy=(sx(mid_x2 + 30), sz(HEADER_Z)),
            xytext=(sx(mid_x2 - 30), sz(HEADER_Z)),
            arrowprops=arrow_style, zorder=12)

# Arrow between F2 and F3
mid_x3 = (f2_out + f3_in) / 2
ax.annotate("", xy=(sx(mid_x3 + 30), sz(HEADER_Z)),
            xytext=(sx(mid_x3 - 30), sz(HEADER_Z)),
            arrowprops=arrow_style, zorder=12)

# Arrow between F3 and pH test
mid_x4 = (f3_out + PH_TEST_X) / 2
ax.annotate("", xy=(sx(mid_x4 + 30), sz(HEADER_Z)),
            xytext=(sx(mid_x4 - 30), sz(HEADER_Z)),
            arrowprops=arrow_style, zorder=12)

# ── Dimensions ───────────────────────────────────────────────────────────────
# Frame width
draw_dim_h(ax, sx(FSKID_X), sx(FSKID_X + FSKID_W), sz(FSKID_Z_LO - 50),
           "900mm", offset=0.4)

# Frame height
draw_dim_v(ax, sx(FSKID_X - 80), sz(FSKID_Z_LO), sz(FSKID_Z_HI),
           "600mm", offset=0.4)

# Filter spacing (F1 to F2)
draw_dim_h(ax, sx(F1_X), sx(F2_X), sz(FILT_SUMP_Z - 80),
           "300mm", offset=0.3, fs=5.5)

# Filter spacing (F2 to F3)
draw_dim_h(ax, sx(F2_X), sx(F3_X), sz(FILT_SUMP_Z - 80),
           "300mm", offset=0.3, fs=5.5)

# Height: floor to frame bottom
draw_dim_v(ax, sx(FSKID_X + FSKID_W + 80), sz(0), sz(FSKID_Z_LO),
           "150mm", offset=0.3, fs=5.5)

# Height: floor to filter head
draw_dim_v(ax, sx(FSKID_X + FSKID_W + 150), sz(0), sz(FILT_HEAD_Z),
           "680mm", offset=0.4)

# Header height above ports
draw_dim_v(ax, sx(PH_TEST_X + 100), sz(PORT_Z), sz(HEADER_Z),
           f"{int(HEADER_Z - PORT_Z)}mm", offset=0.3, fs=5.5)

# ── Leader callouts ──────────────────────────────────────────────────────────
# Frame
leader(ax, sx(FSKID_X + FSKID_W / 2), sz(FSKID_Z_HI + 20),
       sx(FSKID_X + FSKID_W / 2), sz(FSKID_Z_HI + 80),
       "25×25×3 SLOTTED\nSTEEL ANGLE FRAME", fs=6)

# Backing board
leader(ax, sx(FSKID_X + FSKID_W / 2 + 100), sz(FSKID_Z_LO + ANGLE_W + 30),
       sx(FSKID_X + FSKID_W / 2 + 100), sz(FSKID_Z_LO - 20),
       "18mm PLYWOOD\nBACKING BOARD", fs=5.5)

# Mounting bracket
leader(ax, sx(F2_X + BB_OD / 2 + 10), sz(FILT_HEAD_Z + 6),
       sx(F2_X + BB_OD / 2 + 120), sz(FILT_HEAD_Z + 70),
       "U-BRACKET + 25mm\nHDPE SPACER (SEE DETAIL B)", fs=5.5)

# Pipe material
leader(ax, sx((f1_out + f2_in) / 2), sz(HEADER_Z + 10),
       sx((f1_out + f2_in) / 2), sz(HEADER_Z + 90),
       "1\" HDPE Sch40\n(OD 33mm, WALL 4mm)", fs=5.5)

# Wall bracket
leader(ax, sx(FSKID_X - BRACKET_W / 2), sz(FSKID_Z_LO + 50 + BRACKET_H / 2),
       sx(FSKID_X - BRACKET_W / 2 - 80), sz(FSKID_Z_LO + 50 + BRACKET_H / 2 + 60),
       "L-BRACKET\nTO WALL RIB", fs=5.5)

# ── Notes ────────────────────────────────────────────────────────────────────
notes = [
    "1. All pipe: 1\" HDPE Sch40 (OD 33mm, wall 4mm). Push-fit barb connections.",
    "2. Filter housings: Geekpure Big Blue 4.5\"×10\" (1\" NPT ports).",
    "3. Flow direction: P-02 → F1 (50μ) → F2 (5μ) → F3 (GAC) → pH test → DV-01.",
    "4. 18mm plywood backing board inside frame — easy mounting/repositioning of housings.",
    "5. 25mm HDPE spacer blocks between bracket and ply — clears rear port fittings (Detail B).",
    "6. Frame mounted to pinhole wall corrugation ribs with M8 bolts + nyloc nuts.",
    "7. pH test point: inline tee with removable cap for handheld probe insertion.",
    "8. DV-01 routes to Blue system (pH 6.5–8.0) or Black waste (outside range).",
]
for i, n in enumerate(notes):
    fig.text(0.04, 0.10 - i * 0.018, n, fontsize=7, color=C_TEXT,
             fontfamily="monospace", va="top")

# ═══════════════════════════════════════════════════════════════════════════════
# DETAIL B — FILTER MOUNTING CROSS-SECTION (~1:2)
# Side elevation (vertical section perpendicular to pinhole wall)
# Yd horizontal (wall at left), Z vertical
# Shows: corrugated wall → 18mm ply → 25mm HDPE spacer → bracket tab →
#        filter head → sump bowl below → 1" NPT port with pipe
# ═══════════════════════════════════════════════════════════════════════════════

SC_B = 2.0  # mm per drawing unit for detail
OBY = 3.0   # Yd origin
OBZ = 4.0   # Z origin

def sb_y(yd_mm):
    return OBY + yd_mm / SC_B

def sb_z(z_mm):
    return OBZ + z_mm / SC_B

# Detail limits — Yd = -15 to 200, Z relative to head center
# Sump bottom at Z = -35 - 270 = -305; rounded bottom adds ~65 → need Z to -320
HEAD_CZ = 0
ax2.set_xlim(sb_y(-25) - 0.5, sb_y(210) + 1)
ax2.set_ylim(sb_z(-330) - 0.5, sb_z(130) + 1)

# Detail title
ax2.text(sb_y(90), sb_z(115), "DETAIL B — FILTER MOUNTING\nCROSS-SECTION (APPROX 1:2)",
         ha="center", va="top", fontsize=9, fontweight="bold",
         color="#1A237E", zorder=10)

# All Z coordinates below are relative to filter head center (PORT_Z)

# ── 1. Container corrugated wall (section fill) ─────────────────────────────
# Wall is at Yd=0, ~2mm steel corrugated sheet — show as hatched rectangle
WALL_T = 2.0
# Corrugation profile — simplified as a thick hatched band
ax2.add_patch(plt.Rectangle((sb_y(-WALL_T), sb_z(-320)),
              WALL_T / SC_B, 420 / SC_B,
              fc=C_STEEL_FILL, ec=C_FRAME, lw=1.8, zorder=3, hatch="//"))
ax2.text(sb_y(-WALL_T / 2), sb_z(105), "WALL", ha="center", va="bottom",
         fontsize=5.5, color=C_FRAME, rotation=0)

# ── 2. Plywood backing board (18mm) ─────────────────────────────────────────
PLY_YD_START = 0   # flush against wall inner face
PLY_THICK = 18
ax2.add_patch(plt.Rectangle((sb_y(PLY_YD_START), sb_z(-320)),
              PLY_THICK / SC_B, 420 / SC_B,
              fc="#D4C8A0", ec="#A09060", lw=1.5, zorder=3))
# Wood grain indication
for gz in range(-310, 100, 15):
    ax2.plot([sb_y(PLY_YD_START + 2), sb_y(PLY_YD_START + PLY_THICK - 2)],
             [sb_z(gz), sb_z(gz + 3)],
             color="#C0B080", lw=0.4, zorder=3.5)

# Dimension: ply thickness
draw_dim_h(ax2, sb_y(PLY_YD_START), sb_y(PLY_YD_START + PLY_THICK),
           sb_z(-60), "18mm", offset=0.3, fs=5.5)

# ── 3. HDPE spacer block (25mm) ─────────────────────────────────────────────
SPACER_YD = PLY_YD_START + PLY_THICK
SPACER_THICK = 25
SPACER_VIS_H = 40   # visible height in section
ax2.add_patch(plt.Rectangle((sb_y(SPACER_YD), sb_z(-SPACER_VIS_H / 2)),
              SPACER_THICK / SC_B, SPACER_VIS_H / SC_B,
              fc="#E0D8B0", ec="#A09060", lw=1.2, zorder=4,
              hatch=".."))

# Dimension: spacer thickness
draw_dim_h(ax2, sb_y(SPACER_YD), sb_y(SPACER_YD + SPACER_THICK),
           sb_z(-60), "25mm", offset=0.3, fs=5.5)

# ── 4. Steel bracket tab (3mm) ──────────────────────────────────────────────
BRACKET_YD = SPACER_YD + SPACER_THICK
BRACKET_THICK = 3
BRACKET_VIS_H = 50
ax2.add_patch(plt.Rectangle((sb_y(BRACKET_YD), sb_z(-BRACKET_VIS_H / 2)),
              BRACKET_THICK / SC_B, BRACKET_VIS_H / SC_B,
              fc="#999999", ec=C_FRAME, lw=1.2, zorder=5))

# ── M6 bolt through bracket + spacer + ply ──────────────────────────────────
BOLT_Z = -10  # bolt centerline Z (relative)
bolt_y_head = BRACKET_YD + BRACKET_THICK  # bolt head on front face of bracket
bolt_y_tip = PLY_YD_START - 2  # bolt tip emerges slightly past ply back face

# Bolt shank
ax2.plot([sb_y(bolt_y_tip), sb_y(bolt_y_head)],
         [sb_z(BOLT_Z), sb_z(BOLT_Z)],
         color=C_FRAME, lw=1.8, zorder=6)

# Bolt head (hex, simplified as small rectangle)
ax2.add_patch(plt.Rectangle((sb_y(bolt_y_head), sb_z(BOLT_Z - 4)),
              5 / SC_B, 8 / SC_B,
              fc="#666666", ec=C_FRAME, lw=1.0, zorder=7))

# Washer + nut on back side
ax2.add_patch(plt.Rectangle((sb_y(bolt_y_tip - 3), sb_z(BOLT_Z - 5)),
              3 / SC_B, 10 / SC_B,
              fc="#666666", ec=C_FRAME, lw=1.0, zorder=7))

# Bolt label
leader(ax2, sb_y(bolt_y_head + 3), sb_z(BOLT_Z),
       sb_y(bolt_y_head + 40), sb_z(BOLT_Z - 30),
       "M6×70 BOLT\n+ NYLOC NUT", fs=5)

# ── 5. Filter head (section through center) ─────────────────────────────────
HEAD_YD = BRACKET_YD + BRACKET_THICK + 2  # small gap for clamp band
HEAD_DEPTH = 80   # head depth in Yd direction (front-to-back)
HEAD_VIS_H = BB_HEAD_H  # 70mm

ax2.add_patch(plt.Rectangle((sb_y(HEAD_YD), sb_z(-HEAD_VIS_H / 2)),
              HEAD_DEPTH / SC_B, HEAD_VIS_H / SC_B,
              fc=C_HEAD, ec=C_FRAME, lw=1.8, zorder=5))
ax2.text(sb_y(HEAD_YD + HEAD_DEPTH / 2), sb_z(0), "HEAD",
         ha="center", va="center", fontsize=6, color="white",
         fontweight="bold", zorder=6)

# ── 6. Sump bowl (hangs below head) ─────────────────────────────────────────
SUMP_H = BB_H - BB_HEAD_H   # 270mm
SUMP_W_SEC = BB_OD   # 130mm diameter shown in section
sump_yd_center = HEAD_YD + HEAD_DEPTH / 2

ax2.add_patch(plt.Rectangle(
    (sb_y(sump_yd_center - SUMP_W_SEC / 2), sb_z(-HEAD_VIS_H / 2 - SUMP_H)),
    SUMP_W_SEC / SC_B, SUMP_H / SC_B,
    fc=C_HOUSING, ec=C_FRAME, lw=1.5, alpha=0.6, zorder=4))

# Rounded bottom
arc_r_b = SUMP_W_SEC / 2
theta_b = np.linspace(180, 360, 40)
arc_bx = sb_y(sump_yd_center) + (arc_r_b / SC_B) * np.cos(np.radians(theta_b))
arc_bz = sb_z(-HEAD_VIS_H / 2 - SUMP_H) + (arc_r_b / SC_B) * np.sin(np.radians(theta_b)) + arc_r_b / SC_B
ax2.plot(arc_bx, arc_bz, color=C_FRAME, lw=1.5, zorder=5)

ax2.text(sb_y(sump_yd_center), sb_z(-HEAD_VIS_H / 2 - SUMP_H / 2), "SUMP\nBOWL",
         ha="center", va="center", fontsize=6, color="white",
         fontweight="bold", zorder=6)

# Sump height dimension
draw_dim_v(ax2, sb_y(sump_yd_center + SUMP_W_SEC / 2 + 15),
           sb_z(-HEAD_VIS_H / 2 - SUMP_H), sb_z(-HEAD_VIS_H / 2),
           f"{int(SUMP_H)}mm", offset=0.3, fs=5)

# Cartridge removal annotation — sump unscrews downward
ax2.annotate("", xy=(sb_y(sump_yd_center), sb_z(-HEAD_VIS_H / 2 - SUMP_H - 40)),
             xytext=(sb_y(sump_yd_center), sb_z(-HEAD_VIS_H / 2 - SUMP_H - 5)),
             arrowprops=dict(arrowstyle="-|>", color="#CC4444", lw=2.0,
                             mutation_scale=12), zorder=10)
ax2.text(sb_y(sump_yd_center), sb_z(-HEAD_VIS_H / 2 - SUMP_H - 45),
         "UNSCREW SUMP\nFOR CARTRIDGE\nREPLACEMENT",
         ha="center", va="top", fontsize=5.5, color="#CC4444", fontweight="bold")

# ── 7. 1" NPT port (front face of head) with pipe stub ──────────────────────
PORT_YD = HEAD_YD + HEAD_DEPTH  # port exits front face
PIPE_OD_SEC = FILT_PIPE_OD   # 33mm
PIPE_WALL_SEC = FILT_PIPE_WALL  # 4mm
PORT_Z_SEC = 0  # at head center

# Port bore through head
ax2.add_patch(plt.Rectangle((sb_y(PORT_YD - 15), sb_z(PORT_Z_SEC - PIPE_OD_SEC / 2)),
              15 / SC_B, PIPE_OD_SEC / SC_B,
              fc="white", ec=C_FRAME, lw=1.0, zorder=6))

# Pipe stub (1" HDPE extending from port)
STUB_LEN = 50
# Outer wall
ax2.add_patch(plt.Rectangle((sb_y(PORT_YD), sb_z(PORT_Z_SEC - PIPE_OD_SEC / 2)),
              STUB_LEN / SC_B, PIPE_OD_SEC / SC_B,
              fc=C_HDPE, ec=C_FRAME, lw=1.0, zorder=5))
# Inner bore
ax2.add_patch(plt.Rectangle(
    (sb_y(PORT_YD), sb_z(PORT_Z_SEC - PIPE_OD_SEC / 2 + PIPE_WALL_SEC)),
    STUB_LEN / SC_B, (PIPE_OD_SEC - 2 * PIPE_WALL_SEC) / SC_B,
    fc="white", ec="none", zorder=6))

# Pipe label
leader(ax2, sb_y(PORT_YD + STUB_LEN), sb_z(PORT_Z_SEC),
       sb_y(PORT_YD + STUB_LEN + 30), sb_z(PORT_Z_SEC + 25),
       "1\" HDPE\nTO HEADER", fs=5)

# ── 8. Clamp band (at head/sump junction) ───────────────────────────────────
CLAMP_H_SEC = 15
CLAMP_YD_L = sump_yd_center - SUMP_W_SEC / 2 - 5
CLAMP_W_SEC = SUMP_W_SEC + 10
ax2.add_patch(plt.Rectangle(
    (sb_y(CLAMP_YD_L), sb_z(-HEAD_VIS_H / 2 - CLAMP_H_SEC)),
    CLAMP_W_SEC / SC_B, CLAMP_H_SEC / SC_B,
    fc="#888888", ec=C_FRAME, lw=1.0, zorder=6))

# ── Overall standoff dimension ───────────────────────────────────────────────
total_standoff = PLY_THICK + SPACER_THICK + BRACKET_THICK  # 18 + 25 + 3 = 46mm
draw_dim_h(ax2, sb_y(PLY_YD_START), sb_y(BRACKET_YD + BRACKET_THICK),
           sb_z(-85), f"{total_standoff}mm STANDOFF", offset=0.3, fs=5.5)

# ── Component labels along section ──────────────────────────────────────────
label_z = 85
label_items = [
    (PLY_YD_START + PLY_THICK / 2, "18mm PLY"),
    (SPACER_YD + SPACER_THICK / 2, "25mm HDPE\nSPACER"),
    (BRACKET_YD + BRACKET_THICK / 2, "BRACKET"),
]
for ly, ltxt in label_items:
    ax2.text(sb_y(ly), sb_z(label_z), ltxt, ha="center", va="bottom",
             fontsize=5, color=C_FRAME, rotation=0)
    ax2.plot([sb_y(ly), sb_y(ly)], [sb_z(label_z - 5), sb_z(50)],
             color=C_DIM, lw=0.5, ls=":", zorder=2)

# ── Section cut indicator note ───────────────────────────────────────────────
ax2.text(sb_y(90), sb_z(-315),
         "SECTION THROUGH FILTER HEAD\nPERPENDICULAR TO WALL AT PORT HEIGHT",
         ha="center", va="top", fontsize=6, color="#666666", style="italic")

# ── Title block ──────────────────────────────────────────────────────────────
title_block(ax, "SHEET 1 OF 1",
            drawing_title="FILTER SKID — PLUMBING ELEVATION",
            subtitle="VIEW FROM INSIDE CONTAINER LOOKING AT PINHOLE WALL (Yd=0)",
            scale_note="ELEVATION 1:5  |  DETAIL B ~1:2  |  ALL DIMS IN mm",
            doc_id="TBS-001 · Water System — Filter Skid Detail")

# ── Copyright ────────────────────────────────────────────────────────────────
fig.text(0.99, 0.005, "© 2026 Alvin Richards — GNU AGPLv3",
         ha="right", va="bottom", fontsize=6.0, color="#888888", style="italic")

# ── Save ─────────────────────────────────────────────────────────────────────
import os
os.makedirs("diagrams", exist_ok=True)
fig.savefig("diagrams/filter-skid-sheet1.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
fig.savefig(svg_path("diagrams/filter-skid-sheet1.png"), bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close(fig)
print("Filter skid diagram written → diagrams/filter-skid-sheet1.png")
