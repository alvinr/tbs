#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_filter_skid_diagram.py
Generates a detailed plumbing diagram of the 3-stage filter skid mounted
on the equipment panel in the IBC plumbing corridor (Yd=1046).

Sheet 1 — Filter Skid Elevation (1:5)
  View from corridor side looking at the equipment panel face.
  X axis horizontal, Z axis vertical.
  Shows: slotted angle frame, three separate Big Blue 4.5"×10" housings
         (F1/F2/F3) with external inter-stage piping,
         P-02 supply riser, 1" HDPE inlet/outlet pipes with parallel-wall
         drawing, pH test point, DV-01 diverter valve, dimensions and leaders.

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
    DIAGRAMS_DIR,
)
from tbs_title_block import title_block
from tbs_drawing import (
    draw_dim_h, draw_dim_v, leader, draw_rect, hatch_rect,
    place_label, register_pipe, reset_label_registry, draw_notes,
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

def sx(x_mm):
    return x_mm

def sz(z_mm):
    return z_mm


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — FILTER SKID ELEVATION (1:5)
# View from corridor looking at equipment panel face (Yd=1046)
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

# Set axis limits — main elevation (skid Z=1600–1940, header ~2000)
ax.set_xlim(4495, 6105)
ax.set_ylim(1095, 2510)

# Mirror X axis for interior view: matches combined elevation convention
# (high X / IBC end on LEFT, low X / cargo door end on RIGHT)
ax.invert_xaxis()

# Reset label registry for collision avoidance
reset_label_registry()

# ── Context lines ────────────────────────────────────────────────────────────
# Ceiling line
ax.plot([sx(4600), sx(6050)], [sz(2388), sz(2388)],
        color="#888888", lw=1.0, ls="-", zorder=1)
ax.text(sx(4700), sz(2388 + 15), "CEILING (Z=2388mm)", ha="right", va="bottom",
        fontsize=6, color="#888888", style="italic")

# ── Slotted angle frame ──────────────────────────────────────────────────────
# 25×25×3mm slotted steel angle — draw as rectangle outline with steel fill
FRAME_LW = 2.0
ANGLE_W = 25  # angle width in mm

# Bottom rail
ax.add_patch(plt.Rectangle((sx(FSKID_X), sz(FSKID_Z_LO)),
             FSKID_W, ANGLE_W,
             fc=C_STEEL_FILL, ec=C_FRAME, lw=FRAME_LW, zorder=3))

# Top rail
ax.add_patch(plt.Rectangle((sx(FSKID_X), sz(FSKID_Z_HI - ANGLE_W)),
             FSKID_W, ANGLE_W,
             fc=C_STEEL_FILL, ec=C_FRAME, lw=FRAME_LW, zorder=3))

# Left upright
ax.add_patch(plt.Rectangle((sx(FSKID_X), sz(FSKID_Z_LO)),
             ANGLE_W, FSKID_H,
             fc=C_STEEL_FILL, ec=C_FRAME, lw=FRAME_LW, zorder=3))

# Right upright
ax.add_patch(plt.Rectangle((sx(FSKID_X + FSKID_W - ANGLE_W), sz(FSKID_Z_LO)),
             ANGLE_W, FSKID_H,
             fc=C_STEEL_FILL, ec=C_FRAME, lw=FRAME_LW, zorder=3))

# Slot pattern indication (decorative dashes in uprights)
for upright_x in [FSKID_X + ANGLE_W / 2, FSKID_X + FSKID_W - ANGLE_W / 2]:
    for slot_z in range(FSKID_Z_LO + 50, FSKID_Z_HI - 50, 80):
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
             ply_w, ply_h,
             fc=C_PLY, ec="#A09060", lw=1.0, alpha=0.5, zorder=2.5))

# ── Wall mounting brackets ───────────────────────────────────────────────────
# L-brackets connecting frame to container ribs
BRACKET_W = 50
BRACKET_H = 80
for bz in [FSKID_Z_LO + 50, FSKID_Z_HI - 80]:
    for bx in [FSKID_X - BRACKET_W, FSKID_X + FSKID_W]:
        ax.add_patch(plt.Rectangle((sx(bx), sz(bz)),
                     BRACKET_W, BRACKET_H,
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
        body_w, body_h,
        fc=C_HOUSING, ec=C_FRAME, lw=1.5, alpha=0.6, zorder=5))

    # Rounded bottom of sump
    arc_r = body_w / 2
    theta = np.linspace(180, 360, 40)
    arc_x = sx(cx_mm) + arc_r * np.cos(np.radians(theta))
    arc_z = sz(body_z_bot) + arc_r * np.sin(np.radians(theta)) + arc_r
    ax.plot(arc_x, arc_z, color=C_FRAME, lw=1.5, zorder=5)

    # Head (reinforced nylon, darker)
    head_z_bot = FILT_HEAD_Z - BB_HEAD_H
    ax.add_patch(plt.Rectangle(
        (sx(cx_mm - body_w / 2), sz(head_z_bot)),
        body_w, BB_HEAD_H,
        fc=C_HEAD, ec=C_FRAME, lw=1.8, zorder=6))

    # Mounting bracket — steel U-bracket screwed through backing board
    # The bracket wraps around the head and bolts to the 18mm ply
    bracket_w = body_w + 20   # bracket width (wider than housing)
    bracket_h = 12            # bracket thickness
    bracket_tab = 30          # tab height extending above/below head

    # Horizontal bar across top of head
    ax.add_patch(plt.Rectangle(
        (sx(cx_mm - bracket_w / 2), sz(FILT_HEAD_Z)),
        bracket_w, bracket_h,
        fc="#999999", ec=C_FRAME, lw=1.2, zorder=7))

    # Left tab (down from bar, alongside housing)
    ax.add_patch(plt.Rectangle(
        (sx(cx_mm - bracket_w / 2), sz(FILT_HEAD_Z - bracket_tab)),
        bracket_h, (bracket_tab + bracket_h),
        fc="#999999", ec=C_FRAME, lw=1.0, zorder=7))

    # Right tab (down from bar, alongside housing)
    ax.add_patch(plt.Rectangle(
        (sx(cx_mm + bracket_w / 2 - bracket_h), sz(FILT_HEAD_Z - bracket_tab)),
        bracket_h, (bracket_tab + bracket_h),
        fc="#999999", ec=C_FRAME, lw=1.0, zorder=7))

    # HDPE spacer blocks (25mm standoff between bracket and backing board)
    # Visible in elevation as small rectangles behind bracket tabs
    SPACER_D = 50   # spacer depth (Yd direction — not visible in elevation)
    SPACER_H = 40   # spacer height (visible)
    SPACER_W = 20   # spacer width (visible, slightly wider than bracket tab)
    spacer_z = FILT_HEAD_Z - bracket_tab - 5
    for sp_x in [cx_mm - bracket_w / 2 - 4,
                 cx_mm + bracket_w / 2 - SPACER_W + 4]:
        ax.add_patch(plt.Rectangle(
            (sx(sp_x), sz(spacer_z)),
            SPACER_W, SPACER_H,
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
        (body_w + 16), clamp_h,
        fc="#888888", ec=C_FRAME, lw=1.0, zorder=6))

    # IN port (left side of head)
    port_z = FILT_HEAD_Z - BB_HEAD_H / 2
    in_x = cx_mm - BB_PORT_SEP / 2
    out_x = cx_mm + BB_PORT_SEP / 2

    # Port circles (1" NPT)
    port_r = 12  # visual radius for port indication
    ax.add_patch(plt.Circle((sx(in_x), sz(port_z)), port_r,
                 fc="white", ec=C_FRAME, lw=1.2, zorder=7))
    ax.add_patch(plt.Circle((sx(out_x), sz(port_z)), port_r,
                 fc="white", ec=C_FRAME, lw=1.2, zorder=7))

    # Port labels
    ax.text(sx(in_x), sz(port_z), "IN", ha="center", va="center",
            fontsize=4.5, fontweight="bold", color=C_FRAME, zorder=8)
    ax.text(sx(out_x), sz(port_z), "OUT", ha="center", va="center",
            fontsize=4.5, fontweight="bold", color=C_FRAME, zorder=8)

    # Filter label below housing
    place_label(ax, sx(cx_mm), sz(body_z_top - 30), f"{label}\n{filter_type}",
                component='filter', fontsize=7, color=C_TEXT,
                dx=0, dy=-0.8, ha='center', va='top')

    # Register pipe endpoints for collision avoidance
    register_pipe(sx(in_x), sz(port_z), sx(in_x), sz(port_z + 50))
    register_pipe(sx(out_x), sz(port_z), sx(out_x), sz(port_z + 50))

    return in_x, out_x, port_z


# Draw three separate filter housings
f1_in, f1_out, f_port_z = draw_filter_housing(ax, F1_X, "F1", "5μ MPP\nSEDIMENT")
f2_in, f2_out, _        = draw_filter_housing(ax, F2_X, "F2", "KDF-55 METAL")
f3_in, f3_out, _        = draw_filter_housing(ax, F3_X, "F3", "CTO CARBON")


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


# ── P-02 supply riser ────────────────────────────────────────────────────────
# P-02 is mounted on the same equipment panel (pump section below filter skid).
# Show the discharge riser entering from below.
P02_X = FSKID_X + 50
RISER_X = P02_X + 110  # discharge riser X (offset right of pump center)

# ── Pipe routing ─────────────────────────────────────────────────────────────
# Flow path: IBC-3 → P-02 discharge → F1 IN → F1 OUT → F2 IN →
#            F2 OUT → F3 IN → F3 OUT → pH test → DV-01

OD = FILT_PIPE_OD    # 33mm
WALL = FILT_PIPE_WALL  # 4mm

# Port Z position for all filters
PORT_Z = FILT_HEAD_Z - BB_HEAD_H / 2  # 1940 - 35 = 1905mm

# Header height (horizontal pipe run above filter heads connecting them)
HEADER_Z = FILT_HEAD_Z + 60  # 2000mm — above heads with clearance

# ── Supply riser: P-02 discharge rises to F1 inlet ──────────────────────────
# Riser enters visible area from below, runs up to port height, then to F1 IN.
RISER_ENTRY_Z = FSKID_Z_LO - 100  # just below visible frame
INLET_Z = PORT_Z
draw_pipe_path(ax,
    [RISER_X, RISER_X, f1_in],
    [RISER_ENTRY_Z, INLET_Z, INLET_Z],
    OD, WALL)

# Supply annotation at riser entry
ax.annotate("", xy=(sx(RISER_X), sz(RISER_ENTRY_Z + 80)),
            xytext=(sx(RISER_X), sz(RISER_ENTRY_Z + 10)),
            arrowprops=dict(arrowstyle="-|>", color=C_BROWN, lw=1.5), zorder=10)
ax.text(sx(RISER_X), sz(RISER_ENTRY_Z - 10),
        "FROM P-02\n(PUMP SECTION\nBELOW)", ha="center", va="top",
        fontsize=6, color=C_BROWN, style="italic")

# ── Inter-stage pipes (external, separate housings) ──────────────────────────
# F1 OUT → header rise → F2 IN
HEADER_Z = FILT_HEAD_Z + 40
draw_pipe_path(ax,
    [f1_out, f1_out, f2_in, f2_in],
    [PORT_Z, HEADER_Z, HEADER_Z, PORT_Z],
    OD, WALL, zorder=7)
# F2 OUT → header rise → F3 IN
draw_pipe_path(ax,
    [f2_out, f2_out, f3_in, f3_in],
    [PORT_Z, HEADER_Z, HEADER_Z, PORT_Z],
    OD, WALL, zorder=7)

# ── F3 OUT → pH test point → DV-01 ──────────────────────────────────────────
# pH test point: inline tee fitting with probe pocket, positioned after F3 outlet
PH_TEST_X = F3_X + 200  # 3745mm
PH_TEST_Z = PORT_Z

DV01_X = PH_TEST_X + 150  # 3895mm
DV01_Z = PORT_Z
DV01_R = 50  # valve body radius

# ── pH test point symbol ─────────────────────────────────────────────────────
# Draw the pH stub FIRST (lower zorder) so the main pipe's elbow covers it
PH_STUB_H = 80  # stub height

draw_pipe_path(ax,
    [PH_TEST_X, PH_TEST_X],
    [PORT_Z, PORT_Z + PH_STUB_H],
    OD, WALL, zorder=6)

# Main pipe: F3 OUT → pH test → DV-01
# Runs directly from outlet at port height
draw_pipe_path(ax,
    [f3_out, PH_TEST_X, PH_TEST_X, DV01_X - DV01_R],
    [PORT_Z, PORT_Z, PORT_Z, PORT_Z],
    OD, WALL, zorder=8)

# Probe cap (circle at top of stub)
cap_r = 18
ax.add_patch(plt.Circle((sx(PH_TEST_X), sz(PORT_Z + PH_STUB_H + cap_r)),
             cap_r, fc="#FFFFCC", ec=C_FRAME, lw=1.5, zorder=8))
ax.text(sx(PH_TEST_X), sz(PORT_Z + PH_STUB_H + cap_r), "pH",
        ha="center", va="center", fontsize=5.5, fontweight="bold", zorder=9)

# pH test label
place_label(ax, sx(PH_TEST_X), sz(PORT_Z + PH_STUB_H + cap_r * 3),
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
place_label(ax, sx(DV01_X), sz(DV01_Z - 40), "DV-01\n(3-WAY DIVERTER)",
            component='diverter', fontsize=6, color=C_TEXT,
            dx=0, dy=-2.5, ha='center', va='top')

# DV-01 outputs
# Top output → Blue system (clean)
draw_pipe_path(ax,
    [DV01_X, DV01_X],
    [DV01_Z + DV01_R, DV01_Z + DV01_R + 100],
    OD, WALL, fc=C_BLUE)
ax.text(sx(DV01_X + 20), sz(DV01_Z + DV01_R + 120), "← BLUE\n  (pH 6.5–8.0)",
        ha="right", va="bottom", fontsize=5.5, color=C_BLUE, fontweight="bold")

# Right output → Black system (waste)
draw_pipe_path(ax,
    [DV01_X + DV01_R, DV01_X + DV01_R + 80],
    [DV01_Z, DV01_Z],
    OD, WALL, fc="#333333")
ax.text(sx(DV01_X + DV01_R + 90), sz(DV01_Z), "← BLACK\n  (pH outside range)",
        ha="right", va="center", fontsize=5.5, color="#333333", fontweight="bold")

# ── Flow arrows ──────────────────────────────────────────────────────────────
arrow_style = dict(arrowstyle="-|>", color=C_HDPE, lw=1.8, mutation_scale=10)
# Arrow on supply riser (horizontal leg from riser to F1 inlet)
mid_x1 = (RISER_X + f1_in) / 2
ax.annotate("", xy=(sx(mid_x1 + 30), sz(INLET_Z)),
            xytext=(sx(mid_x1 - 30), sz(INLET_Z)),
            arrowprops=arrow_style, zorder=12)

# Inter-stage flow arrows
for xa, xb in [(f1_out, f2_in), (f2_out, f3_in)]:
    mid_x = (xa + xb) / 2
    ax.annotate("", xy=(sx(mid_x + 30), sz(HEADER_Z)),
                xytext=(sx(mid_x - 30), sz(HEADER_Z)),
                arrowprops=arrow_style, zorder=12)

# Arrow between F3 outlet and pH test (horizontal run)
mid_x4 = (f3_out + PH_TEST_X) / 2
ax.annotate("", xy=(sx(mid_x4 + 30), sz(PORT_Z)),
            xytext=(sx(mid_x4 - 30), sz(PORT_Z)),
            arrowprops=arrow_style, zorder=12)

# ── Dimensions ───────────────────────────────────────────────────────────────
# Frame width
draw_dim_h(ax, sx(FSKID_X), sx(FSKID_X + FSKID_W), sz(FSKID_Z_LO - 50),
           f"{FSKID_W}mm", offset=2.2)

# Frame height
draw_dim_v(ax, sx(FSKID_X - 80), sz(FSKID_Z_LO), sz(FSKID_Z_HI),
           f"{FSKID_H}mm", offset=2.2)

# Filter spacing (F1 to F2)
f_spacing = F2_X - F1_X
draw_dim_h(ax, sx(F1_X), sx(F2_X), sz(FILT_SUMP_Z - 80),
           f"{f_spacing}mm", offset=1.65, fs=5.5)

# Filter spacing (F2 to F3)
draw_dim_h(ax, sx(F2_X), sx(F3_X), sz(FILT_SUMP_Z - 80),
           f"{F3_X - F2_X}mm", offset=1.65, fs=5.5)

# Sump bottom height AFF
ax.plot([sx(FSKID_X - 120), sx(FSKID_X + FSKID_W + 60)],
        [sz(FILT_SUMP_Z), sz(FILT_SUMP_Z)],
        color=C_DIM, lw=0.5, ls=":", zorder=2)
ax.text(sx(FSKID_X - 130), sz(FILT_SUMP_Z),
        f"Z={FILT_SUMP_Z}mm AFF",
        ha="left", va="center", fontsize=5.5, color=C_DIM)

# Ceiling clearance (measured from header pipes above heads)
CEILING_Z = 2388
TOP_OF_PIPES = HEADER_Z + OD / 2
draw_dim_v(ax, sx(FSKID_X + FSKID_W + 150), sz(TOP_OF_PIPES), sz(CEILING_Z),
           f"{int(CEILING_Z - TOP_OF_PIPES)}mm\nCLEARANCE", offset=2.2)

# ── Leader callouts ──────────────────────────────────────────────────────────
# Frame
leader(ax, sx(FSKID_X + FSKID_W * 0.35), sz(FSKID_Z_LO),
       sx(FSKID_X + FSKID_W * 0.55), sz(FSKID_Z_LO - 120),
       "25×25×3 SLOTTED\nSTEEL ANGLE FRAME", fs=6)

# Backing board
leader(ax, sx(FSKID_X + FSKID_W / 2 + 100), sz(FSKID_Z_LO + ANGLE_W + 30),
       sx(FSKID_X + FSKID_W / 2 + 100), sz(FSKID_Z_LO - 20),
       "18mm PLYWOOD\nBACKING BOARD", fs=6)

# Pipe material on inlet riser leg
leader(ax, sx(RISER_X), sz(RISER_ENTRY_Z + 200),
       sx(RISER_X - 120), sz(RISER_ENTRY_Z + 300),
       "1\" HDPE Sch40\n(OD 33mm, WALL 4mm)", fs=6)

# Panel bracket
leader(ax, sx(FSKID_X - BRACKET_W / 2), sz(FSKID_Z_LO + 50 + BRACKET_H * 0.3),
       sx(FSKID_X - BRACKET_W / 2 - 160), sz(FSKID_Z_LO + 50 + BRACKET_H / 2 + 30),
       "L-BRACKET\nTO PANEL", fs=6)

# ── Notes ────────────────────────────────────────────────────────────────────
notes = [
    "NOTES",
    "1. 3× separate 4.5\"×10\" Big Blue housings, individual U-bracket mounts.",
    "2. External inter-stage piping: F1 OUT → F2 IN → F2 OUT → F3 IN (1\" HDPE).",
    "3. Flow: F1 (5μ MPP sediment) → F2 (KDF-55 metal) → F3 (CTO carbon).",
    "4. 18mm plywood backing board inside frame — mounting surface for housings.",
    "5. 50mm HDPE spacer blocks between bracket and ply — clears rear port fittings (Detail B).",
    "6. Frame mounted to equipment panel in IBC plumbing corridor (Yd=1046).",
    "7. pH test point: inline tee with removable cap for handheld probe insertion.",
    "8. DV-01 routes to Blue system (pH 6.5–8.0) or Black waste (outside range).",
]
draw_notes(ax, notes, sx(FSKID_X+FSKID_W*1.45), sz(1230), spacing=4.5, fs=7,
           width=180, font={"fontfamily": "monospace"})

# ═══════════════════════════════════════════════════════════════════════════════
# DETAIL B — FILTER MOUNTING CROSS-SECTION (~1:2)
# Side elevation (vertical section perpendicular to equipment panel)
# Yd horizontal (wall at left), Z vertical
# Shows: corrugated wall → 18mm ply → 50mm HDPE spacer → bracket tab →
#        filter head → sump bowl below → 1" NPT port with pipe
# ═══════════════════════════════════════════════════════════════════════════════

def sb_y(yd_mm):
    return yd_mm

def sb_z(z_mm):
    return z_mm

# Detail limits — Yd = -15 to 200, Z relative to head center
# Sump bottom at Z = -35 - 460 = -495; rounded bottom adds ~65 → need Z to -510
HEAD_CZ = 0
ax2.set_xlim(-26, 212)
ax2.set_ylim(-521, 132)

# Detail title
ax2.text(sb_y(90), sb_z(115), "DETAIL B — FILTER MOUNTING\nCROSS-SECTION (AXES IN mm)",
         ha="center", va="top", fontsize=9, fontweight="bold",
         color="#1A237E", zorder=10)

# All Z coordinates below are relative to filter head center (PORT_Z)

# ── 1. Equipment panel (18mm marine ply at Yd=1046) ──────────────────────────
PANEL_T = 18.0
ax2.add_patch(plt.Rectangle((sb_y(-PANEL_T), sb_z(-510)),
              PANEL_T, 610,
              fc="#D4C8A0", ec="#A09060", lw=1.8, zorder=3))
ax2.text(sb_y(-PANEL_T / 2), sb_z(105), "EQUIP\nPANEL", ha="center", va="bottom",
         fontsize=5, color=C_FRAME, rotation=0)

# ── 2. Plywood backing board (18mm) ─────────────────────────────────────────
PLY_YD_START = 0   # flush against wall inner face
PLY_THICK = 18
ax2.add_patch(plt.Rectangle((sb_y(PLY_YD_START), sb_z(-510)),
              PLY_THICK, 610,
              fc="#D4C8A0", ec="#A09060", lw=1.5, zorder=3))
# Wood grain indication
for gz in range(-500, 100, 15):
    ax2.plot([sb_y(PLY_YD_START + 2), sb_y(PLY_YD_START + PLY_THICK - 2)],
             [sb_z(gz), sb_z(gz + 3)],
             color="#C0B080", lw=0.4, zorder=3.5)

# Dimension: ply thickness
draw_dim_h(ax2, sb_y(PLY_YD_START), sb_y(PLY_YD_START + PLY_THICK),
           sb_z(-60), "18mm", offset=0.66, fs=5.5)

# ── 3. HDPE spacer block (50mm) ─────────────────────────────────────────────
SPACER_YD = PLY_YD_START + PLY_THICK
SPACER_THICK = 50
SPACER_VIS_H = 40   # visible height in section
ax2.add_patch(plt.Rectangle((sb_y(SPACER_YD), sb_z(-SPACER_VIS_H / 2)),
              SPACER_THICK, SPACER_VIS_H,
              fc="#E0D8B0", ec="#A09060", lw=1.2, zorder=4,
              hatch=".."))

# Dimension: spacer thickness
draw_dim_h(ax2, sb_y(SPACER_YD), sb_y(SPACER_YD + SPACER_THICK),
           sb_z(SPACER_YD - SPACER_THICK), f"{SPACER_THICK}mm", offset=1.0, fs=5.5)

# ── 4. Steel bracket tab (3mm) ──────────────────────────────────────────────
BRACKET_YD = SPACER_YD + SPACER_THICK
BRACKET_THICK = 3
BRACKET_VIS_H = 50
ax2.add_patch(plt.Rectangle((sb_y(BRACKET_YD), sb_z(-BRACKET_VIS_H / 2)),
              BRACKET_THICK, BRACKET_VIS_H,
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
              5, 8,
              fc="#666666", ec=C_FRAME, lw=1.0, zorder=7))

# Washer + nut on back side
ax2.add_patch(plt.Rectangle((sb_y(bolt_y_tip - 3), sb_z(BOLT_Z - 5)),
              3, 10,
              fc="#666666", ec=C_FRAME, lw=1.0, zorder=7))

# Bolt label
leader(ax2, sb_y(bolt_y_head + 3), sb_z(BOLT_Z),
       sb_y(bolt_y_head + 40), sb_z(BOLT_Z - 30),
       "M6×80 BOLT\n+ NYLOC NUT", fs=5)

# ── 5. Filter head (section through center) ─────────────────────────────────
HEAD_YD = BRACKET_YD + BRACKET_THICK + 2  # small gap for clamp band
HEAD_DEPTH = 80   # head depth in Yd direction (front-to-back)
HEAD_VIS_H = BB_HEAD_H  # 70mm

ax2.add_patch(plt.Rectangle((sb_y(HEAD_YD), sb_z(-HEAD_VIS_H / 2)),
              HEAD_DEPTH, HEAD_VIS_H,
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
    SUMP_W_SEC, SUMP_H,
    fc=C_HOUSING, ec=C_FRAME, lw=1.5, alpha=0.6, zorder=4))

# Rounded bottom
arc_r_b = SUMP_W_SEC / 2
theta_b = np.linspace(180, 360, 40)
arc_bx = sb_y(sump_yd_center) + arc_r_b * np.cos(np.radians(theta_b))
arc_bz = sb_z(-HEAD_VIS_H / 2 - SUMP_H) + arc_r_b * np.sin(np.radians(theta_b)) + arc_r_b
ax2.plot(arc_bx, arc_bz, color=C_FRAME, lw=1.5, zorder=5)

ax2.text(sb_y(sump_yd_center), sb_z(-HEAD_VIS_H / 2 - SUMP_H / 2), "SUMP\nBOWL",
         ha="center", va="center", fontsize=6, color="white",
         fontweight="bold", zorder=6)

# Sump height dimension
draw_dim_v(ax2, sb_y(sump_yd_center + SUMP_W_SEC / 2 + 15),
           sb_z(-HEAD_VIS_H / 2 - SUMP_H), sb_z(-HEAD_VIS_H / 2),
           f"{int(SUMP_H)}mm", offset=0.66, fs=5)

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
              15, PIPE_OD_SEC,
              fc="white", ec=C_FRAME, lw=1.0, zorder=6))

# Pipe stub (1" HDPE extending from port)
STUB_LEN = 50
# Outer wall
ax2.add_patch(plt.Rectangle((sb_y(PORT_YD), sb_z(PORT_Z_SEC - PIPE_OD_SEC / 2)),
              STUB_LEN, PIPE_OD_SEC,
              fc=C_HDPE, ec=C_FRAME, lw=1.0, zorder=5))
# Inner bore
ax2.add_patch(plt.Rectangle(
    (sb_y(PORT_YD), sb_z(PORT_Z_SEC - PIPE_OD_SEC / 2 + PIPE_WALL_SEC)),
    STUB_LEN, (PIPE_OD_SEC - 2 * PIPE_WALL_SEC),
    fc="white", ec="none", zorder=6))

# Pipe label
leader(ax2, sb_y(PORT_YD + STUB_LEN), sb_z(PORT_Z_SEC),
       sb_y(PORT_YD + STUB_LEN + 30), sb_z(PORT_Z_SEC + 25),
       "1\" HDPE\nTO NEXT STAGE\n/ OUTLET", fs=5)

# ── 8. Clamp band (at head/sump junction) ───────────────────────────────────
CLAMP_H_SEC = 15
CLAMP_YD_L = sump_yd_center - SUMP_W_SEC / 2 - 5
CLAMP_W_SEC = SUMP_W_SEC + 10
ax2.add_patch(plt.Rectangle(
    (sb_y(CLAMP_YD_L), sb_z(-HEAD_VIS_H / 2 - CLAMP_H_SEC)),
    CLAMP_W_SEC, CLAMP_H_SEC,
    fc="#888888", ec=C_FRAME, lw=1.0, zorder=6))

# ── Overall standoff dimension ───────────────────────────────────────────────
total_standoff = PLY_THICK + SPACER_THICK + BRACKET_THICK  # 18 + 50 + 3 = 71mm
draw_dim_h(ax2, sb_y(PLY_YD_START), sb_y(BRACKET_YD + BRACKET_THICK),
           sb_z(-85), f"{total_standoff}mm STANDOFF", offset=0.66, fs=5.5)

# ── Component labels along section ──────────────────────────────────────────
label_z = 85
label_items = [
    (PLY_YD_START + PLY_THICK / 2, "18mm PLY"),
    (SPACER_YD + SPACER_THICK / 2, "50mm HDPE\nSPACER"),
    (BRACKET_YD + BRACKET_THICK / 2, "BRACKET"),
]
for ly, ltxt in label_items:
    ax2.text(sb_y(ly), sb_z(label_z), ltxt, ha="center", va="bottom",
             fontsize=5, color=C_FRAME, rotation=0)
    ax2.plot([sb_y(ly), sb_y(ly)], [sb_z(label_z - 5), sb_z(50)],
             color=C_DIM, lw=0.5, ls=":", zorder=2)

# ── Section cut indicator note ───────────────────────────────────────────────
ax2.text(sb_y(90), sb_z(-505),
         "SECTION THROUGH FILTER HEAD\nPERPENDICULAR TO PANEL AT PORT HEIGHT\n(4.5\"×10\" BIG BLUE — SUMP-DOWN ORIENTATION)",
         ha="center", va="top", fontsize=6, color="#666666", style="italic")

# ── Title block (full-width axes spanning both columns) ──────────────────────
ax_tb = fig.add_axes([0.04, 0.0, 0.92, 0.06])
ax_tb.set_xlim(0, 1)
ax_tb.set_ylim(0, 1)
ax_tb.axis("off")
title_block(ax_tb, "SHEET 1 OF 1",
            drawing_title="3-STAGE FILTER SKID — PLUMBING ELEVATION",
            subtitle="VIEW FROM IBC CORRIDOR LOOKING AT EQUIPMENT PANEL (Yd=1046)",
            scale_note="AXES IN mm",
            doc_id="TBS-001 · Water System — 3-Stage Filter Skid Detail",
            height=0.75)

# ── Save ─────────────────────────────────────────────────────────────────────
import os
os.makedirs(DIAGRAMS_DIR, exist_ok=True)
fig.savefig(os.path.join(DIAGRAMS_DIR, "filter-skid-sheet1.png"), dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
fig.savefig(svg_path(os.path.join(DIAGRAMS_DIR, "filter-skid-sheet1.png")), bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close(fig)
print("Filter skid diagram written → diagrams/filter-skid-sheet1.png")
