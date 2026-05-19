#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_pinhole_wall_elevation.py — Combined interior elevation of the
pinhole wall (Yd=0) showing all mounted systems for interference checking.

View: looking at the pinhole wall from inside the container.
Horizontal axis = X (mm), Vertical axis = Z (mm AFF).

Output: diagrams/pinhole-wall-elevation.png
"""

import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from tbs_constants import (
    C_LEN, C_WID, C_HGT,
    PH_X, PH_H, PH_D,
    EVAP_X, EVAP_W, EVAP_H,
    PWR_PANEL_X, PWR_PANEL_W, PWR_PANEL_H,
    EP_X, EP_W, EP_H_LO, EP_H_HI,
    BA_X, BA_W, BA_H_LO, BA_H_HI,
    PUMP_X, PUMP_W, PUMP_H_LO, PUMP_H_HI,
    FSKID_X, FSKID_W, FSKID_Z_LO, FSKID_Z_HI,
    F1_X, F2_X, F3_X, BB_OD, BB_H, BB_HEAD_H, BB_PORT_SEP,
    FILT_HEAD_Z, FILT_SUMP_Z, FILT_PIPE_OD, FILT_PIPE_WALL,
    PUMP_PIPE_OD, PUMP_PIPE_WALL,
    TAP_X, TAP_Z,
    SHELF_X_L, SHELF_X_R, SHELF_H, SHELF_T, SHELF_HANGER_N,
    SHELF_YD_NEAR,
    WALKWAY_H, WALKWAY_GRATE_T, WALKWAY_W,
    WALKWAY_BRACKET_H, WALKWAY_BRACKET_T,
    CONTAINER_RIB_SPACING,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_DRAIN_X,
    PROC_TRAY_SUMP_W, PROC_TRAY_SUMP_D, PROC_TRAY_SUMP_Z, PROC_TRAY_RIM,
    PROC_TRAY_YD_NEAR, PROC_TRAY_D, PROC_TRAY_PITCH,
    RAIL_OFF,
    FAN_B_H, FAN_B_YD, FAN_DIAM,
    C_OUT, C_CL, C_DIM,
    C_ALUM, C_STEEL, C_EVAP, C_ELEC, C_BATT, C_PUMP,
    C_PINHOLE_EQ, C_WALL,
    ZONE_R_START,
    DIAGRAMS_DIR,
)
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_cl
from tbs_title_block import title_block

# ── Local constants (computed from tbs_constants) ────────────────────────────
HEADER_Z = FILT_HEAD_Z + 60          # 2000mm — filter header pipe Z
RISER_X = None  # set after PM_FRAME_R is computed (depends on frame width)
PH_TEST_X = F3_X + 200               # 3745mm — pH test point X
DV01_X = PH_TEST_X + 150             # 3895mm — diverter valve X
DV01_R = 50                           # DV-01 body radius

# ── Pump manifold frame constants ──
# Layout: P-01, P-02 side by side in top row,
#         P-04 centered below (raised 250mm, overlapping top row in elevation).
# P-03 is in the IBC plumbing corridor (separate from manifold).
PM_ANGLE = 25            # 25×25mm SHS frame member width
PM_PUMP_W = 127          # Shurflo 2088 body width (mm), includes port threads
PM_PUMP_H = 218          # Shurflo 2088 body height (mm)
PM_GAP_X = 60            # gap between pumps horizontally
PM_MARGIN_X = 20         # margin from frame inner edge to pump body
PM_MARGIN_Z = 20         # vertical margin inside frame
# Frame: 2 pumps wide, 40% wider than minimum for pump separation
PM_FRAME_W = int((2 * PM_ANGLE + 2 * PM_MARGIN_X
              + 2 * PM_PUMP_W + 1 * PM_GAP_X) * 1.4)      # 565mm
PM_FRAME_X = PUMP_X + (PUMP_W - PM_FRAME_W) // 2          # centered (may extend past zone)
# Top row (P-01, P-02) — kept at original Z position
PM_PUMP_Z_TOP = 518
# P-04 centered horizontally, 20mm below top row for clearance
PM_P04_Z = PM_PUMP_Z_TOP - PM_PUMP_H - 80   # 220mm — dropped for tray drain routing clearance
PM_P04_X = PM_FRAME_X + (PM_FRAME_W - PM_PUMP_W) // 2     # centered in frame
# Frame wraps all pumps tightly
PM_FRAME_Z_LO = PM_P04_Z - PM_MARGIN_Z - PM_ANGLE         # 355mm
PM_FRAME_Z_HI = (PM_PUMP_Z_TOP + PM_PUMP_H
                 + PM_MARGIN_Z + PM_ANGLE)                  # 781mm
# Pump X positions — top row: 2 pumps at frame edges, separated
PM_P01_X = PM_FRAME_X + PM_ANGLE + PM_MARGIN_X            # left pump
PM_P02_X = PM_FRAME_X + PM_FRAME_W - PM_ANGLE - PM_MARGIN_X - PM_PUMP_W  # right pump
PM_PORT_OFF = 30         # port offset from top of pump body
PM_PORT_Z_TOP = PM_PUMP_Z_TOP + PM_PUMP_H - PM_PORT_OFF   # 706mm — port Z, top row
PM_PORT_Z_P04 = PM_P04_Z + PM_PUMP_H - PM_PORT_OFF        # 588mm — port Z, P-04
PM_HEADER_Z_BLUE_SUC   = PM_PUMP_Z_TOP + PM_PUMP_H + 260  # Blue suction header
PM_HEADER_Z_BLUE_DISCH = PM_FRAME_Z_HI + 20               # Blue discharge header
# DV-02: to the right of P-04 in drawing (lower X), at P-04 port height
PM_DV02_R = 20           # DV-02 symbol radius (mm)
PM_DV02_X = PM_P04_X - 60                                  # 60mm right of P-04 in drawing
PM_DV02_Z = PM_PORT_Z_P04                                  # at P-04 port height
# ACC-01 accumulator: 200×127mm, mounted right of frame
PM_ACC_W = 200
PM_ACC_H = 127
PM_ACC_X = PM_FRAME_X + PM_FRAME_W + 40
PM_ACC_Z = PM_HEADER_Z_BLUE_DISCH - PM_ACC_H // 2 + 25

# Pipe colors for Blue and Brown circuits
C_BLUE  = "#2979B8"      # Blue circuit pipe fill
C_BLUE_EC = "#1A5A8A"    # Blue circuit pipe edge
C_BROWN = "#8B5E3C"      # Brown circuit pipe fill
C_BROWN_EC = "#5A3A20"   # Brown circuit pipe edge
C_BLACK_SYS = "#555555"  # Black/waste system pipe fill
C_BLACK_EC  = "#333333"  # Black/waste system pipe edge
# Small pipe OD for manifold internals
OD_H = PUMP_PIPE_OD     # 21mm (1/2" HDPE)
WALL_H = PUMP_PIPE_WALL  # 3mm

# Walkway X range (near walkway = pinhole wall side)
WK_X_L = PROC_TRAY_X_L + WALKWAY_W   # 470mm — near walkway left edge (past left walkway)
WK_X_R = PROC_TRAY_X_R               # 4629mm — near walkway right edge

# Pull-cord switches
PS_X_D = EVAP_X + EVAP_W // 2 - 60   # 1170mm — switch D
PS_X_G = EVAP_X + EVAP_W // 2 + 60   # 1290mm — switch G
PS_Z = C_HGT - 60                     # 2328mm — switch body Z
CORD_HANG_Z = 900                     # pull cord bottom Z

# Cable trunking
TK_H = 25                             # trunking height (mm)
TK_Z = C_HGT - TK_H                  # 2363mm — trunking bottom Z

# Power panel Z (flush-mount, exterior — shown as dashed outline)
PWR_Z_LO = EP_H_LO                   # 900mm — aligned with EP bottom

# Colors
C_FSKID = "#B0A898"   # filter skid frame (warm gray)
C_FILTER = "#4A90D9"  # filter housings (blue)
C_HDPE = "#2A5A2A"    # HDPE pipe (dark green)
C_SHELF = "#C8B06A"   # chemistry shelf (warm gold)
C_TRUNKING = "#808080" # cable trunking

# ── Scale and layout ────────────────────────────────────────────────────────
# S maps mm → figure inches.  Container 5893×2388 must fit comfortably.
# Available drawing area ≈ 22" wide × 8" tall (in a 26×12" figure).
S = 0.00335   # mm → inches  (≈1:7.6 at screen DPI, ≈1:20 at 300dpi print)
FW, FH = 26.0, 12.0
OX = 2.5    # drawing origin X offset (inches)
OZ = 2.5    # drawing origin Z offset (inches) — room for notes below

def sx(x_mm):
    """Convert X position (mm) to drawing x coordinate.
    Mirrored: viewing from inside container toward pinhole wall,
    high X (IBC end) is on the LEFT, low X (cargo door) on the RIGHT."""
    return OX + (C_LEN - x_mm) * S

def sz(z_mm):
    """Convert Z position (mm) to drawing y coordinate."""
    return OZ + z_mm * S

# ── Figure setup ────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(FW, FH), dpi=150)
ax.set_xlim(0, FW)
ax.set_ylim(0, FH)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

FONT = {"fontfamily": "monospace"}

# ── Helper: filled, labeled equipment block ─────────────────────────────────
def equip_block(x_mm, z_mm, w_mm, h_mm, label, fc, *,
                ec=C_OUT, lw=1.0, zorder=5, ls="-", alpha=0.85,
                label_fs=5.5, label_color=C_OUT):
    """Draw a filled rectangle with centered label."""
    # sx() is mirrored, so sx(x_mm + w_mm) < sx(x_mm) — use the left corner
    x_draw = sx(x_mm + w_mm)
    w_draw = sx(x_mm) - sx(x_mm + w_mm)  # positive width in drawing space
    rect = mpatches.FancyBboxPatch(
        (x_draw, sz(z_mm)), w_draw, h_mm * S,
        boxstyle="square,pad=0", facecolor=fc, edgecolor=ec,
        linewidth=lw, linestyle=ls, alpha=alpha, zorder=zorder)
    ax.add_patch(rect)
    # Centered label
    cx = sx(x_mm + w_mm / 2)
    cz = sz(z_mm + h_mm / 2)
    ax.text(cx, cz, label, ha="center", va="center",
            fontsize=label_fs, color=label_color, zorder=zorder + 1,
            **FONT)

# ── Helper: parallel-wall pipe drawing ──────────────────────────────────────
C_HDPE_FILL = "#2A5A2A"   # HDPE pipe fill (dark green)
C_HDPE_EDGE = "#1A3A1A"   # HDPE pipe edge

def draw_pipe_path(ax, x_pts, z_pts, od_mm, wall_mm,
                   fc=C_HDPE_FILL, ec=C_HDPE_EDGE, bore_fc="white",
                   elbow_r=None, zorder=8):
    """Draw a pipe run with parallel walls and rounded elbows.
    x_pts, z_pts: waypoint coordinates in mm (before scaling).
    Uses the mirrored sx()/sz() scale functions.
    """
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
                lw=0.5 if color != bore_fc else 0, zorder=z_ord)

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
            ox = [sx(_cy + r_out * math.cos(a)) for a in _angles]
            oz = [sz(_cz + r_out * math.sin(a)) for a in _angles]
            ix_a = [sx(_cy + r_in * math.cos(a)) for a in _angles]
            iz_a = [sz(_cz + r_in * math.sin(a)) for a in _angles]
            ax.fill(ox + ix_a[::-1], oz + iz_a[::-1],
                    fc=color, ec=ec if color != bore_fc else "none",
                    lw=0.5 if color != bore_fc else 0, zorder=z_ord)

        _arc_ring(r_eff + half_od, max(r_eff - half_od, 0.5), fc, zorder)
        _arc_ring(r_eff + half_id, max(r_eff - half_id, 0.5), bore_fc, zorder + 1)


# ═══════════════════════════════════════════════════════════════════════════
# 1. CONTAINER OUTLINE
# ═══════════════════════════════════════════════════════════════════════════
# Outer rectangle — sx() is mirrored, so sx(C_LEN) < sx(0)
wall_left = sx(C_LEN)   # left edge of container in drawing space
wall_right = sx(0)       # right edge
wall_w = wall_right - wall_left
ax.add_patch(mpatches.Rectangle(
    (wall_left, sz(0)), wall_w, C_HGT * S,
    facecolor="white", edgecolor=C_OUT, linewidth=2.0, zorder=1))

# Floor line (thicker)
ax.plot([wall_left, wall_right], [sz(0), sz(0)], color=C_OUT, lw=2.5, zorder=2)
# Ceiling line
ax.plot([wall_left, wall_right], [sz(C_HGT), sz(C_HGT)], color=C_OUT, lw=2.0, zorder=2)
# Left wall line
ax.plot([wall_left, wall_left], [sz(0), sz(C_HGT)], color=C_OUT, lw=2.0, zorder=2)
# Right wall line
ax.plot([wall_right, wall_right], [sz(0), sz(C_HGT)], color=C_OUT, lw=2.0, zorder=2)

# ── Corrugation ribs (faint vertical dashed lines) ─────────────────────────
rib_x = CONTAINER_RIB_SPACING
while rib_x < C_LEN:
    ax.plot([sx(rib_x), sx(rib_x)], [sz(0), sz(C_HGT)],
            color="#D0D0D0", lw=0.3, ls="--", zorder=1)
    rib_x += CONTAINER_RIB_SPACING

# ═══════════════════════════════════════════════════════════════════════════
# 2. CABLE TRUNKING (ceiling, full length)
# ═══════════════════════════════════════════════════════════════════════════
equip_block(0, TK_Z, C_LEN, TK_H, "", C_TRUNKING,
            lw=0.5, zorder=3, alpha=0.5, label_fs=4)
ax.text(sx(C_LEN / 2), sz(TK_Z + TK_H / 2), "CABLE TRUNKING (40×25mm PVC)",
        ha="center", va="center", fontsize=4, color="white", zorder=4, **FONT)

# ── Drop conduits (10mm corrugated flex) from trunking to devices ────────
C_CONDUIT_FILL = "#A0A0A0"   # conduit fill (light gray)
C_CONDUIT_EDGE = "#606060"   # conduit outline (darker gray)
CONDUIT_OD = 10              # conduit outer diameter (mm)

conduit_drops = [
    # (X center mm, Z top of device mm)
    (EVAP_X + EVAP_W / 2,  RAIL_OFF + EVAP_H),      # evap cooler — circuit E
    (EP_X + EP_W / 2,      EP_H_HI),                 # electrical panel
    (BA_X + BA_W / 2,      BA_H_HI),                 # battery bank
    (PM_FRAME_X + PM_FRAME_W / 2, PM_FRAME_Z_HI),     # pump manifold — circuit F
    (PWR_PANEL_X + PWR_PANEL_W / 2, PWR_Z_LO + PWR_PANEL_H),  # ext power panel
    (PS_X_D,               PS_Z + 15),                # pull-cord switch D
    (PS_X_G,               PS_Z + 15),                # pull-cord switch G
]
conduit_w = CONDUIT_OD * S   # drawing width of conduit
for cx_mm, ztop_mm in conduit_drops:
    # Filled rectangle representing the conduit cross-section at true scale
    cx_draw = sx(cx_mm)
    z_top = sz(TK_Z)
    z_bot = sz(ztop_mm)
    h_draw = z_top - z_bot
    ax.add_patch(mpatches.Rectangle(
        (cx_draw - conduit_w / 2, z_bot), conduit_w, h_draw,
        facecolor=C_CONDUIT_FILL, edgecolor=C_CONDUIT_EDGE,
        linewidth=0.4, zorder=3, alpha=0.75))

# ═══════════════════════════════════════════════════════════════════════════
# 3. WALKWAY DECK (near walkway along pinhole wall)
# ═══════════════════════════════════════════════════════════════════════════
# Grating deck
deck_z_bot = WALKWAY_H - WALKWAY_GRATE_T  # 75mm
equip_block(WK_X_L, deck_z_bot, WK_X_R - WK_X_L, WALKWAY_GRATE_T,
            "", C_STEEL, lw=0.6, zorder=4, alpha=0.4)
# Grating hatch marks
for gx in range(int(WK_X_L), int(WK_X_R), 80):
    ax.plot([sx(gx), sx(gx + 40)], [sz(deck_z_bot), sz(WALKWAY_H)],
            color=C_STEEL, lw=0.2, zorder=4, alpha=0.3)

# Label
ax.text(sx((WK_X_L + WK_X_R) / 2), sz(WALKWAY_H + 15),
        "NEAR WALKWAY DECK (Z=100mm)", ha="center", va="bottom",
        fontsize=4.5, color=C_DIM, zorder=10, **FONT)

# ── Walkway brackets (cantilever arms at rib positions) ─────────────────────
# Viewed end-on: brackets project in Yd (toward viewer), so they appear as
# small rectangles (bracket thickness × vertical leg height), not triangles.
bx = WK_X_L
while bx <= WK_X_R:
    nearest_rib = round(bx / CONTAINER_RIB_SPACING) * CONTAINER_RIB_SPACING
    if WK_X_L <= nearest_rib <= WK_X_R:
        # End-on rectangle: WALKWAY_BRACKET_T wide × deck_z_bot tall
        bw = WALKWAY_BRACKET_T  # 8mm plate thickness (visible width in X)
        bh = deck_z_bot         # 75mm from floor to grating underside
        equip_block(nearest_rib - bw / 2, 0, bw, bh,
                    "", C_STEEL, ec=C_OUT, lw=0.5, zorder=3, alpha=0.6)
    bx += CONTAINER_RIB_SPACING

# ═══════════════════════════════════════════════════════════════════════════
# 3a. PROCESSING TRAY — edge-on in elevation (below walkway deck)
# ═══════════════════════════════════════════════════════════════════════════
# The tray sits on shim strips at Z=PROC_TRAY_SUMP_Z (20mm), spanning from
# PROC_TRAY_X_L (170mm) to PROC_TRAY_X_R (4629mm).  Near rim at Yd=80 rises
# 50mm above tray floor.  Sump well at X=2399 dips from Z=20 down to Z=0.

TRAY_FLOOR_Z = PROC_TRAY_SUMP_Z   # 20mm — tray floor raised by sump depth
TRAY_RIM_TOP = TRAY_FLOOR_Z + PROC_TRAY_RIM  # 70mm
C_TRAY = "#C8D8E8"    # 304 SS tray fill (light blue-gray)
C_TRAY_EC = "#5A8AAF"  # tray edge color

# Tray body — filled band from Z=0 to rim top (70mm), full width
# At this scale, show the entire tray profile as a single colored band
equip_block(PROC_TRAY_X_L, 0, PROC_TRAY_X_R - PROC_TRAY_X_L, TRAY_RIM_TOP,
            "", C_TRAY, ec=C_TRAY_EC, lw=0.6, zorder=2.5, alpha=0.35)

# Tray floor line at Z=20mm (where the flat bottom of the tray sits)
ax.plot([sx(PROC_TRAY_X_L), sx(PROC_TRAY_X_R)],
        [sz(TRAY_FLOOR_Z), sz(TRAY_FLOOR_Z)],
        color=C_TRAY_EC, lw=0.6, zorder=2.8)

# Rim top line (shows 50mm rim height across full span)
ax.plot([sx(PROC_TRAY_X_L), sx(PROC_TRAY_X_R)],
        [sz(TRAY_RIM_TOP), sz(TRAY_RIM_TOP)],
        color=C_TRAY_EC, lw=0.8, zorder=2.8)

# Left rim upstand (thickened for visibility)
ax.plot([sx(PROC_TRAY_X_L), sx(PROC_TRAY_X_L)],
        [sz(0), sz(TRAY_RIM_TOP)],
        color=C_TRAY_EC, lw=1.0, zorder=2.8)
# Right rim upstand
ax.plot([sx(PROC_TRAY_X_R), sx(PROC_TRAY_X_R)],
        [sz(0), sz(TRAY_RIM_TOP)],
        color=C_TRAY_EC, lw=1.0, zorder=2.8)

# Sump well — depression at X=2399, width=150mm in X, depth from Z=20 to Z=0
SUMP_X_L = PROC_TRAY_DRAIN_X - PROC_TRAY_SUMP_W / 2  # 2324mm
SUMP_X_R = PROC_TRAY_DRAIN_X + PROC_TRAY_SUMP_W / 2  # 2474mm

# Sump cavity — darker fill from tray floor down to Z=0
sump_pts_x = [sx(SUMP_X_L), sx(SUMP_X_L), sx(SUMP_X_R), sx(SUMP_X_R)]
sump_pts_z = [sz(TRAY_FLOOR_Z), sz(0), sz(0), sz(TRAY_FLOOR_Z)]
ax.fill(sump_pts_x, sump_pts_z, fc="#8BB8D8", ec=C_TRAY_EC, lw=0.8,
        alpha=0.5, zorder=2.9)

# Pickup tube — 1" HDPE tube from Z=5 up to walkway level
TUBE_OD_VIS = 25.4  # 1" OD
TUBE_X = PROC_TRAY_DRAIN_X  # 2399mm — at sump center
TUBE_Z_BOT = 5   # 5mm above sump floor
TUBE_Z_TOP = WALKWAY_H  # tube top at walkway level (100mm)

# Tube drawn as a thickened vertical line (visible at combined elevation scale)
ax.plot([sx(TUBE_X), sx(TUBE_X)],
        [sz(TUBE_Z_BOT), sz(TUBE_Z_TOP)],
        color="#888888", lw=1.5, zorder=3.5, solid_capstyle='round')

# Foot valve indicator at bottom
ax.plot(sx(TUBE_X), sz(TUBE_Z_BOT), 's',
        color="#666666", markersize=3, zorder=4)

# Labels — positioned to be readable at combined elevation scale
ax.text(sx(PROC_TRAY_X_L + 100), sz(TRAY_RIM_TOP / 2),
        "PROCESSING TRAY (304 SS, 50mm RIM)", ha="left", va="center",
        fontsize=3.5, color=C_TRAY_EC, zorder=10, **FONT)

ax.text(sx(SUMP_X_L - 20), sz(TRAY_FLOOR_Z / 2 + 3),
        "SUMP\nWELL", ha="right", va="center",
        fontsize=2.5, color="#0D47A1", zorder=10, **FONT)

ax.text(sx(TUBE_X - 40), sz(TRAY_RIM_TOP + 5),
        "PICKUP TUBE", ha="right", va="bottom",
        fontsize=2.5, color="#666666", zorder=10, **FONT)
# Leader from pickup label to tube
ax.plot([sx(TUBE_X - 35), sx(TUBE_X - 5)],
        [sz(TRAY_RIM_TOP + 5), sz(TRAY_RIM_TOP + 5)],
        color="#666666", lw=0.3, zorder=10)
ax.plot([sx(TUBE_X - 5), sx(TUBE_X)],
        [sz(TRAY_RIM_TOP + 5), sz(TUBE_Z_TOP - 5)],
        color="#666666", lw=0.3, zorder=10)

# ── Zone labels for empty areas ───────────────────────────────────────────
# Left end zone (X=0–150mm, cargo door / hinged panel)
ax.text(sx(75), sz(C_HGT / 2), "CARGO DOOR\nEND\n(HINGED PANEL)",
        ha="center", va="center", fontsize=5, color="#AAAAAA",
        style="italic", zorder=2, **FONT)

# Right end zone (X=4649–5893mm, IBC stack)
ax.text(sx(ZONE_R_START + (C_LEN - ZONE_R_START) / 2), sz(C_HGT / 2),
        "IBC STACK\nZONE", ha="center", va="center",
        fontsize=5, color="#AAAAAA", style="italic", zorder=2, **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 4. EQUIPMENT BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

# ── Evaporative cooler ──────────────────────────────────────────────────────
equip_block(EVAP_X, RAIL_OFF, EVAP_W, EVAP_H,
            "EVAPORATIVE\nCOOLER", C_EVAP, label_fs=6)

# ── External power panel (flush-mount, exterior — dashed outline) ──────────
equip_block(PWR_PANEL_X, PWR_Z_LO, PWR_PANEL_W, PWR_PANEL_H,
            "EXT. POWER\nPANEL\n(FLUSH)", C_ALUM,
            ls="--", alpha=0.4, label_fs=4.5)

# ── Electrical panel (EP) ──────────────────────────────────────────────────
equip_block(EP_X, EP_H_LO, EP_W, EP_H_HI - EP_H_LO,
            "ELECTRICAL\nPANEL (EP)", C_ELEC, label_fs=5)

# ── Battery bank (BAT) ────────────────────────────────────────────────────
equip_block(BA_X, BA_H_LO, BA_W, BA_H_HI - BA_H_LO,
            "BATTERY\nBANK\n(2× LiFePO4)", C_BATT, label_fs=4.5, label_color="white")

# ── Pinhole aperture ──────────────────────────────────────────────────────
ph_r = 15  # drawing radius (exaggerated for visibility)
draw_cl(ax, sx(PH_X), sz(PH_H), ph_r * S,
        horiz=True, vert=True, color=C_CL, lw=0.6, ext_factor=3.0)
ax.add_patch(plt.Circle((sx(PH_X), sz(PH_H)), ph_r * S,
             fill=True, facecolor=C_PINHOLE_EQ, edgecolor=C_OUT,
             linewidth=1.2, zorder=8))
ax.text(sx(PH_X), sz(PH_H - 80), "PINHOLE\nØ2.17mm",
        ha="center", va="top", fontsize=5, color=C_PINHOLE_EQ,
        zorder=10, **FONT)

# ── Pump manifold (P-01/P-02 top, P-04 centered below) ────
# Frame outline (25×25mm SHS perimeter)
PM_FRAME_H = PM_FRAME_Z_HI - PM_FRAME_Z_LO
equip_block(PM_FRAME_X, PM_FRAME_Z_LO, PM_FRAME_W, PM_FRAME_H,
            "", C_STEEL, lw=1.2, zorder=4, alpha=0.35)

# Plywood backing (faint fill inside frame)
equip_block(PM_FRAME_X + PM_ANGLE, PM_FRAME_Z_LO + PM_ANGLE,
            PM_FRAME_W - 2 * PM_ANGLE, PM_FRAME_H - 2 * PM_ANGLE,
            "", "#D4C8A0", lw=0.5, zorder=3, alpha=0.3)

# 3 pump bodies: P-04 drawn first (behind), then P-01/P-02 on top
equip_block(PM_P04_X, PM_P04_Z, PM_PUMP_W, PM_PUMP_H,
            "P-04", C_PUMP, lw=0.8, zorder=5, alpha=0.85,
            label_fs=3.5, label_color="white")
for (px, plabel) in [
    (PM_P01_X, "P-01"),
    (PM_P02_X, "P-02"),
]:
    equip_block(px, PM_PUMP_Z_TOP, PM_PUMP_W, PM_PUMP_H,
                plabel, C_PUMP, lw=0.8, zorder=6, alpha=0.85,
                label_fs=3.5, label_color="white")

# Frame label
ax.text(sx(PM_FRAME_X + PM_FRAME_W / 2), sz(PM_FRAME_Z_HI + 15),
        "PUMP MANIFOLD\n(P-01, P-02, P-04)", ha="center", va="bottom",
        fontsize=4.5, color=C_DIM, zorder=10, **FONT)

# ACC-01 accumulator (blue rectangle, right of frame)
equip_block(PM_ACC_X, PM_ACC_Z, PM_ACC_W, PM_ACC_H,
            "ACC-01", C_BLUE, lw=0.8, zorder=6, alpha=0.7,
            label_fs=3.5, label_color="white")

# ── Filter skid frame ────────────────────────────────────────────────────
equip_block(FSKID_X, FSKID_Z_LO, FSKID_W, FSKID_Z_HI - FSKID_Z_LO,
            "", C_FSKID, alpha=0.35, lw=1.2)
ax.text(sx(FSKID_X + FSKID_W / 2), sz(FSKID_Z_HI - 30),
        "FILTER SKID FRAME", ha="center", va="top",
        fontsize=4.5, color=C_DIM, zorder=10, **FONT)

# ── Filter housings F1, F2, F3 ───────────────────────────────────────────
for fx, flabel in [(F1_X, "F1"), (F2_X, "F2"), (F3_X, "F3")]:
    # Housing body (simplified rectangle)
    hx = fx - BB_OD / 2
    hz = FILT_SUMP_Z
    hh = FILT_HEAD_Z - FILT_SUMP_Z
    equip_block(hx, hz, BB_OD, hh, flabel, C_FILTER,
                lw=0.8, zorder=6, alpha=0.8, label_fs=5.5, label_color="white")

# ═══════════════════════════════════════════════════════════════════════════
# 4a. PLUMBING — parallel-wall pipe routing
# ═══════════════════════════════════════════════════════════════════════════
OD = FILT_PIPE_OD      # 33mm (1" HDPE Sch40)
PIPE_WALL = FILT_PIPE_WALL  # 4mm
PORT_Z = FILT_HEAD_Z - BB_HEAD_H / 2   # 1905mm — filter port centerline

# Filter port X positions (IN on left, OUT on right of each housing)
f1_in  = F1_X - BB_PORT_SEP / 2   # 3010mm
f1_out = F1_X + BB_PORT_SEP / 2   # 3100mm
f2_in  = F2_X - BB_PORT_SEP / 2   # 3255mm
f2_out = F2_X + BB_PORT_SEP / 2   # 3345mm
f3_in  = F3_X - BB_PORT_SEP / 2   # 3500mm
f3_out = F3_X + BB_PORT_SEP / 2   # 3590mm

# ── F1 OUT → F2 IN (via header) ─────────────────────────────────────────
draw_pipe_path(ax,
    [f1_out, f1_out, f2_in, f2_in],
    [PORT_Z, HEADER_Z, HEADER_Z, PORT_Z],
    OD, PIPE_WALL)

# ── F2 OUT → F3 IN (via header) ─────────────────────────────────────────
draw_pipe_path(ax,
    [f2_out, f2_out, f3_in, f3_in],
    [PORT_Z, HEADER_Z, HEADER_Z, PORT_Z],
    OD, PIPE_WALL)

# ── F3 OUT → pH test → DV-01 ────────────────────────────────────────────
PH_STUB_H = 80   # pH probe stub height

# Draw pH stub FIRST at lower zorder (main pipe elbow covers the junction)
draw_pipe_path(ax,
    [PH_TEST_X, PH_TEST_X],
    [PORT_Z, PORT_Z + PH_STUB_H],
    OD, PIPE_WALL, zorder=6)

# Main pipe: F3 OUT → header → pH test X → down → DV-01
draw_pipe_path(ax,
    [f3_out, f3_out, PH_TEST_X, PH_TEST_X, DV01_X - DV01_R],
    [PORT_Z, HEADER_Z, HEADER_Z, PORT_Z, PORT_Z],
    OD, PIPE_WALL, zorder=8)

# pH probe cap (circle at top of stub)
cap_r = 18
ax.add_patch(plt.Circle((sx(PH_TEST_X), sz(PORT_Z + PH_STUB_H + cap_r)),
             cap_r * S, fc="#FFFFCC", ec=C_OUT, lw=0.8, zorder=9))
ax.text(sx(PH_TEST_X), sz(PORT_Z + PH_STUB_H + cap_r), "pH",
        ha="center", va="center", fontsize=3.5, fontweight="bold",
        color=C_OUT, zorder=10, **FONT)

# ── DV-01 diverter valve ─────────────────────────────────────────────────
ax.add_patch(plt.Circle((sx(DV01_X), sz(PORT_Z)), DV01_R * S,
             fill=True, facecolor="white", edgecolor=C_OUT,
             linewidth=1.0, zorder=9))
ax.annotate("DV-01\n(3-WAY DIVERTER)", xy=(sx(DV01_X), sz(PORT_Z + DV01_R)),
            xytext=(sx(DV01_X - 80), sz(PORT_Z + DV01_R + 120)),
            fontsize=4.2, color=C_DIM, fontweight="bold",
            ha="center", va="bottom",
            arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.6),
            zorder=11, **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# PUMP MANIFOLD — INTERNAL PIPE ROUTING
# All pipe runs shown entering the manifold frame and connecting to
# individual pump ports, ACC-01, BV-01/BV-02, and DV-02.
#
# Coordinate reminder (mirrored view — sx(x) = OX + (C_LEN − x) * S):
#   Higher X (physical) → LEFT in drawing  (IBC zone is far LEFT)
#   Lower X (physical)  → RIGHT in drawing (cargo door is far RIGHT)
# ═══════════════════════════════════════════════════════════════════════════
IBC_PIPE_EXIT_X = ZONE_R_START          # pipes disappear into IBC stack zone
PM_FRAME_R = PM_FRAME_X + PM_FRAME_W    # right edge of manifold frame (LEFT in drawing)
RISER_X = PM_FRAME_R + 30               # Brown riser X, just right of frame

# ── Pump port positions (matching pump manifold detail diagram) ────────────
# Ports are 30mm below top of each pump body.
# IN port on right edge (higher X = LEFT in drawing),
# OUT on left edge (lower X = RIGHT in drawing).
p01_in_x  = PM_P01_X + PM_PUMP_W;  p01_out_x = PM_P01_X
p01_port_z = PM_PORT_Z_TOP
p02_in_x  = PM_P02_X + PM_PUMP_W;  p02_out_x = PM_P02_X
p02_port_z = PM_PORT_Z_TOP
# P-04 centered in manifold (raised)
p04_in_x  = PM_P04_X + PM_PUMP_W;  p04_out_x = PM_P04_X
p04_port_z = PM_PORT_Z_P04

# Elbow offset for internal pipes (small at overview scale)
ELB = 30

# Zorder layers: Black=6 (back), Brown=7 (middle), Blue=8 (front)
Z_BLACK = 6;  Z_BROWN = 7;  Z_BLUE = 8

# Ball valve symbol (small diamond)
BV_R = 15  # radius at overview scale
def _bv_symbol(ax, bvx, bvz, label, zorder=9):
    pts_x = [sx(bvx), sx(bvx + BV_R), sx(bvx), sx(bvx - BV_R)]
    pts_z = [sz(bvz + BV_R), sz(bvz), sz(bvz - BV_R), sz(bvz)]
    ax.add_patch(plt.Polygon(list(zip(pts_x, pts_z)),
                 fc="#CC4444", ec=C_OUT, lw=0.8, alpha=0.8, zorder=zorder))

# ════════════════════════════════════════════════════════════════════════════
# P-01 BLUE SUPPLY: IBC-1/2 → BV-01 → P-01 → ACC-01 → BV-02 → spray bar
# ════════════════════════════════════════════════════════════════════════════
BV01_X = PM_FRAME_R + 60        # BV-01 on suction header (right of frame)
BV01_Z = PM_HEADER_Z_BLUE_SUC
BV02_X = PM_ACC_X + PM_ACC_W + 40   # BV-02 on discharge header (right of ACC-01)
BV02_Z = PM_HEADER_Z_BLUE_DISCH

# 1/2" suction: IBC → BV-01
draw_pipe_path(ax,
    [IBC_PIPE_EXIT_X, BV01_X + BV_R],
    [PM_HEADER_Z_BLUE_SUC, PM_HEADER_Z_BLUE_SUC],
    OD_H, WALL_H, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=Z_BLUE)
# Arrow: flow from IBC (LEFT) toward manifold (RIGHT in drawing)
ax.annotate("", xy=(sx(BV01_X + BV_R + 30), sz(PM_HEADER_Z_BLUE_SUC)),
            xytext=(sx(BV01_X + BV_R + 150), sz(PM_HEADER_Z_BLUE_SUC)),
            arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=1.0), zorder=10)
ax.text(sx((IBC_PIPE_EXIT_X + BV01_X) / 2), sz(PM_HEADER_Z_BLUE_SUC + 30),
        "BLUE SUCTION FROM IBC-1/2", ha="center", va="bottom",
        fontsize=3.5, color=C_BLUE, zorder=10, **FONT)

# BV-01 symbol + leader
_bv_symbol(ax, BV01_X, BV01_Z, "BV\n01")
ax.annotate("BV-01\n(½\" BALL)", xy=(sx(BV01_X), sz(BV01_Z + BV_R)),
            xytext=(sx(BV01_X + 80), sz(BV01_Z + 80)),
            fontsize=4.2, color=C_DIM, fontweight="bold",
            ha="center", va="bottom",
            arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.6),
            zorder=11, **FONT)
# 1/2" from BV-01 to right edge of frame
draw_pipe_path(ax,
    [BV01_X - BV_R, PM_FRAME_R],
    [PM_HEADER_Z_BLUE_SUC, PM_HEADER_Z_BLUE_SUC],
    OD_H, WALL_H, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=Z_BLUE)
# 1/2": frame edge → horizontal across frame → 90° drop → P-01 IN
# Split at Blue discharge crossing (Z=PM_HEADER_Z_BLUE_DISCH): suction drop
# breaks flush against the discharge pipe (both Blue, discharge drawn later = front)
_suc_gap = OD_H / 2.0
draw_pipe_path(ax,
    [PM_FRAME_R, p01_in_x + ELB, p01_in_x + ELB],
    [PM_HEADER_Z_BLUE_SUC, PM_HEADER_Z_BLUE_SUC, PM_HEADER_Z_BLUE_DISCH + _suc_gap],
    OD_H, WALL_H, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=Z_BLUE)
draw_pipe_path(ax,
    [p01_in_x + ELB, p01_in_x + ELB, p01_in_x],
    [PM_HEADER_Z_BLUE_DISCH - _suc_gap, p01_port_z, p01_port_z],
    OD_H, WALL_H, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=Z_BLUE)

# P-01 OUT → 90° up → Blue discharge header → ACC-01 → BV-02
draw_pipe_path(ax,
    [p01_out_x, p01_out_x - ELB, p01_out_x - ELB, PM_ACC_X],
    [p01_port_z, p01_port_z, PM_HEADER_Z_BLUE_DISCH, PM_HEADER_Z_BLUE_DISCH],
    OD_H, WALL_H, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=Z_BLUE)
# ACC-01 exit → BV-02 (1/2" pipe)
draw_pipe_path(ax,
    [PM_ACC_X + PM_ACC_W, BV02_X - BV_R],
    [PM_HEADER_Z_BLUE_DISCH, PM_HEADER_Z_BLUE_DISCH],
    OD_H, WALL_H, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=Z_BLUE)
_bv_symbol(ax, BV02_X, BV02_Z, "BV\n02")
ax.annotate("BV-02\n(½\" BALL)", xy=(sx(BV02_X), sz(BV02_Z + BV_R)),
            xytext=(sx(BV02_X + 80), sz(BV02_Z + 80)),
            fontsize=4.2, color=C_DIM, fontweight="bold",
            ha="center", va="bottom",
            arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.6),
            zorder=11, **FONT)
# BV-02 → 1/2" discharge → spray bar (runs LEFT in drawing toward IBC zone)
draw_pipe_path(ax,
    [BV02_X + BV_R, IBC_PIPE_EXIT_X],
    [PM_HEADER_Z_BLUE_DISCH, PM_HEADER_Z_BLUE_DISCH],
    OD_H, WALL_H, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=Z_BLUE)
# Arrow: flow from manifold toward spray bar (LEFT in drawing = higher X)
ax.annotate("", xy=(sx(IBC_PIPE_EXIT_X + 150), sz(PM_HEADER_Z_BLUE_DISCH)),
            xytext=(sx(IBC_PIPE_EXIT_X + 30), sz(PM_HEADER_Z_BLUE_DISCH)),
            arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=1.0), zorder=10)
ax.text(sx((BV02_X + IBC_PIPE_EXIT_X) / 2), sz(PM_HEADER_Z_BLUE_DISCH + 25),
        "BLUE DISCHARGE → SPRAY BAR", ha="center", va="bottom",
        fontsize=3.5, color=C_BLUE, zorder=10, **FONT)

# ════════════════════════════════════════════════════════════════════════════
# P-02 BROWN RECYCLE: IBC-3 → P-02 → riser → filter skid F1 IN
# ════════════════════════════════════════════════════════════════════════════
# 1/2" suction: IBC-3 → right edge of frame at top-row port Z
draw_pipe_path(ax,
    [IBC_PIPE_EXIT_X, PM_FRAME_R],
    [p02_port_z, p02_port_z],
    OD_H, WALL_H, fc=C_BROWN, ec=C_BROWN_EC, bore_fc="white", zorder=Z_BROWN)
ax.annotate("", xy=(sx(PM_FRAME_R + 30), sz(p02_port_z)),
            xytext=(sx(PM_FRAME_R + 150), sz(p02_port_z)),
            arrowprops=dict(arrowstyle="-|>", color=C_BROWN, lw=1.0), zorder=10)
ax.text(sx((IBC_PIPE_EXIT_X + PM_FRAME_R) / 2), sz(p02_port_z + 30),
        "P-02 SUCTION FROM IBC-3", ha="center", va="bottom",
        fontsize=3.5, color=C_BROWN, zorder=10, **FONT)
# 1/2" manifold: frame edge → P-02 IN
draw_pipe_path(ax,
    [PM_FRAME_R, p02_in_x],
    [p02_port_z, p02_port_z],
    OD_H, WALL_H, fc=C_BROWN, ec=C_BROWN_EC, bore_fc="white", zorder=Z_BROWN)

# P-02 OUT → left elbow → straight north to F1 header height → right to F1 IN
# Riser at p02_out_x - ELB goes directly up, crossing both Blue headers.
RISER_X = p02_out_x - ELB  # riser is right at the first bend
# Split at Blue discharge crossing (Z=PM_HEADER_Z_BLUE_DISCH): Brown breaks flush
_p02_gap = OD_H / 2.0  # break flush against Blue discharge OD
draw_pipe_path(ax,
    [p02_out_x, RISER_X, RISER_X],
    [p02_port_z, p02_port_z, PM_HEADER_Z_BLUE_DISCH - _p02_gap],
    OD_H, WALL_H, fc=C_BROWN, ec=C_BROWN_EC, bore_fc="white", zorder=Z_BROWN)
# Riser resumes above Blue discharge, up to Blue suction crossing
_riser_gap = OD_H / 2.0  # break flush against Blue suction OD
draw_pipe_path(ax,
    [RISER_X, RISER_X],
    [PM_HEADER_Z_BLUE_DISCH + _p02_gap, PM_HEADER_Z_BLUE_SUC - _riser_gap],
    OD_H, WALL_H, fc=C_BROWN, ec=C_BROWN_EC, bore_fc="white", zorder=Z_BROWN)
# Riser resumes above Blue suction, up to F1 header → horizontal to F1 IN
draw_pipe_path(ax,
    [RISER_X, RISER_X, f1_in, f1_in],
    [PM_HEADER_Z_BLUE_SUC + _riser_gap, HEADER_Z, HEADER_Z, PORT_Z + 30],
    OD_H, WALL_H, fc=C_BROWN, ec=C_BROWN_EC, bore_fc="white", zorder=Z_BROWN)
# 1/2→1" reducer bushing at F1 IN port
REDUCER_H = 20
red_pts = [
    (sx(f1_in - OD_H / 2), sz(PORT_Z + 30)),
    (sx(f1_in + OD_H / 2), sz(PORT_Z + 30)),
    (sx(f1_in + OD / 2),   sz(PORT_Z)),
    (sx(f1_in - OD / 2),   sz(PORT_Z)),
]
ax.add_patch(plt.Polygon(red_pts, fc=C_BROWN, ec=C_BROWN_EC, lw=0.6, zorder=Z_BROWN))
ax.annotate("", xy=(sx(RISER_X), sz(PM_FRAME_Z_HI + 100)),
            xytext=(sx(RISER_X), sz(PM_FRAME_Z_HI + 20)),
            arrowprops=dict(arrowstyle="-|>", color=C_BROWN, lw=1.0), zorder=10)

# ════════════════════════════════════════════════════════════════════════════
# P-04 TRAY DRAIN: sump → P-04 → DV-02 → IBC-3 / IBC-4
# ════════════════════════════════════════════════════════════════════════════
TRAY_DRAIN_Z = WALKWAY_H + 20   # 120mm — just above walkway deck
TRAY_SUMP_X = PROC_TRAY_DRAIN_X  # 2399mm

# DV-02 output routing: both Black and Brown run south then left to IBCs
# Both horizontal runs above the walkway deck (Z=100)
# Brown closest to walkway (turns last, lower Z), Black above (turns sooner, higher Z)
DV02_BROWN_Z = WALKWAY_H + 40    # 140mm — Brown horizontal run (closest to walkway)
DV02_BLACK_Z = DV02_BROWN_Z + 25 # 165mm — Black horizontal run (above Brown)
# Vertical risers: Black drops at DV-02 X, Brown offset 25mm to the right (lower X)
DV02_BLACK_RISER_X = PM_DV02_X
DV02_BROWN_RISER_X = PM_DV02_X - 25  # 25mm right in drawing (lower X)

# Tray drain suction: pickup tube rises vertically from sump (X=2399),
# 90° left above P-04, then two 90° turns down into P-04 IN port.
# Path: vertical up → left → down → left into port
_riser_top_z = PM_P04_Z + PM_PUMP_H + 40  # 40mm above P-04 top
_drop_x = p04_in_x + ELB                  # X where pipe drops toward port
draw_pipe_path(ax,
    [TRAY_SUMP_X, TRAY_SUMP_X, _drop_x, _drop_x, p04_in_x],
    [TRAY_DRAIN_Z, _riser_top_z, _riser_top_z, p04_port_z, p04_port_z],
    OD_H, WALL_H, fc=C_BLACK_SYS, ec=C_BLACK_EC, bore_fc="white", zorder=Z_BLACK)
ax.annotate("", xy=(sx(TRAY_SUMP_X), sz(_riser_top_z - 30)),
            xytext=(sx(TRAY_SUMP_X), sz(TRAY_DRAIN_Z + 60)),
            arrowprops=dict(arrowstyle="-|>", color=C_BLACK_SYS, lw=1.0), zorder=10)
ax.text(sx(TRAY_SUMP_X - 30), sz((_riser_top_z + TRAY_DRAIN_Z) / 2),
        "TRAY DRAIN\nRISER", ha="right", va="center",
        fontsize=3.5, color=C_BLACK_SYS, zorder=10, **FONT)

# P-04 OUT → right in drawing (lower X) → horizontal to DV-02 left vertex
draw_pipe_path(ax,
    [p04_out_x, PM_DV02_X + PM_DV02_R],
    [p04_port_z, p04_port_z],
    OD_H, WALL_H, fc=C_BROWN, ec=C_BROWN_EC, bore_fc="white", zorder=Z_BROWN)
# DV-02 symbol (diamond)
dv02_pts_x = [sx(PM_DV02_X), sx(PM_DV02_X + PM_DV02_R),
              sx(PM_DV02_X), sx(PM_DV02_X - PM_DV02_R)]
dv02_pts_z = [sz(PM_DV02_Z + PM_DV02_R), sz(PM_DV02_Z),
              sz(PM_DV02_Z - PM_DV02_R), sz(PM_DV02_Z)]
ax.add_patch(plt.Polygon(list(zip(dv02_pts_x, dv02_pts_z)),
             fc="white", ec=C_OUT, lw=1.0, zorder=9))
ax.annotate("DV-02\n(3-WAY DIVERTER)", xy=(sx(PM_DV02_X), sz(PM_DV02_Z - PM_DV02_R)),
            xytext=(sx(PM_DV02_X + 80), sz(PM_DV02_Z - 120)),
            fontsize=4.2, color=C_DIM, fontweight="bold",
            ha="center", va="top",
            arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.6),
            zorder=11, **FONT)

# DV-02 BOTTOM vertex → Black: south to Z=165, then left to IBC-4
draw_pipe_path(ax,
    [DV02_BLACK_RISER_X, DV02_BLACK_RISER_X, IBC_PIPE_EXIT_X],
    [PM_DV02_Z - PM_DV02_R, DV02_BLACK_Z, DV02_BLACK_Z],
    OD_H, WALL_H, fc=C_BLACK_SYS, ec=C_BLACK_EC, bore_fc="white", zorder=Z_BLACK)
# Flow arrow: Black from DV-02 toward IBC-4
_dv02_blk_mid = (DV02_BLACK_RISER_X + IBC_PIPE_EXIT_X) / 2
ax.annotate("", xy=(sx(_dv02_blk_mid + 150), sz(DV02_BLACK_Z)),
            xytext=(sx(_dv02_blk_mid + 30), sz(DV02_BLACK_Z)),
            arrowprops=dict(arrowstyle="-|>", color=C_BLACK_SYS, lw=1.0), zorder=10)
ax.text(sx((PM_DV02_X + IBC_PIPE_EXIT_X) / 2), sz(DV02_BLACK_Z - 25),
        "WASTE → BLACK IBC-4", ha="center", va="top",
        fontsize=3.5, color=C_BLACK_SYS, zorder=10, **FONT)

# DV-02 RIGHT vertex (drawing) → Brown: right stub → south to Z=140 → left to IBC-3
# Right vertex in drawing = lower physical X = PM_DV02_X - PM_DV02_R
draw_pipe_path(ax,
    [PM_DV02_X - PM_DV02_R, DV02_BROWN_RISER_X,
     DV02_BROWN_RISER_X, IBC_PIPE_EXIT_X],
    [PM_DV02_Z, PM_DV02_Z,
     DV02_BROWN_Z, DV02_BROWN_Z],
    OD_H, WALL_H, fc=C_BROWN, ec=C_BROWN_EC, bore_fc="white", zorder=Z_BROWN)
# Flow arrow: Brown from DV-02 toward IBC-3
_dv02_brn_mid = (DV02_BROWN_RISER_X + IBC_PIPE_EXIT_X) / 2
ax.annotate("", xy=(sx(_dv02_brn_mid + 150), sz(DV02_BROWN_Z)),
            xytext=(sx(_dv02_brn_mid + 30), sz(DV02_BROWN_Z)),
            arrowprops=dict(arrowstyle="-|>", color=C_BROWN, lw=1.0), zorder=10)
ax.text(sx((PM_DV02_X + IBC_PIPE_EXIT_X) / 2), sz(DV02_BROWN_Z + 25),
        "DRAIN → BROWN IBC-3", ha="center", va="bottom",
        fontsize=3.5, color=C_BROWN, zorder=10, **FONT)

# ── DV-01 output: filtered water return to Blue IBC-2 ─────────────────────
draw_pipe_path(ax,
    [DV01_X + DV01_R, IBC_PIPE_EXIT_X],
    [PORT_Z, PORT_Z],
    OD_H, WALL_H, fc="#3070B0", ec="#1A3A6A", bore_fc="white", zorder=8)
ax.annotate("", xy=(sx(IBC_PIPE_EXIT_X + 150), sz(PORT_Z)),
            xytext=(sx(IBC_PIPE_EXIT_X + 30), sz(PORT_Z)),
            arrowprops=dict(arrowstyle="-|>", color="#3070B0", lw=1.2),
            zorder=10)
ax.text(sx((DV01_X + IBC_PIPE_EXIT_X) / 2), sz(PORT_Z + 35),
        "FILTERED RETURN → BLUE IBC-2", ha="center", va="bottom",
        fontsize=3.5, color="#3070B0", zorder=10, **FONT)

# ── DV-01 waste output: to Black IBC-4 ────────────────────────────────────
DV01_WASTE_Z = PORT_Z - 200
draw_pipe_path(ax,
    [DV01_X, DV01_X, IBC_PIPE_EXIT_X],
    [PORT_Z - DV01_R, DV01_WASTE_Z, DV01_WASTE_Z],
    OD_H, WALL_H, fc="#555555", ec="#333333", bore_fc="white", zorder=8)
ax.text(sx((DV01_X + IBC_PIPE_EXIT_X) / 2), sz(DV01_WASTE_Z - 35),
        "WASTE → BLACK IBC-4", ha="center", va="top",
        fontsize=3.5, color="#555555", zorder=10, **FONT)

# ── Chemistry tap branch (TAP-01 / BV-06) ───────────────────────────────
# Branch tee off the Blue discharge trunk, rises to tap height.
# Ball valve BV-06 inline on horizontal run, close to shelf for easy access.
TAP_OD = 25     # 3/4" branch pipe
TAP_WALL = 3
TAP_BRANCH_Z = TAP_Z + 100   # horizontal run height (1250mm)
TAP_TEE_X = 3400              # tee point on Blue discharge trunk
BV06_X = 3600                 # valve position — close to shelf left edge (3729)
BV06_R = 25                   # valve body radius for symbol

# Pipe: Blue discharge tee → riser up → horizontal → valve gap → drop to tap
# TAP riser crosses Blue suction trunk at Z=PM_HEADER_Z_BLUE_SUC.
# Crossing: rear pipe breaks flush against front pipe walls (zero extra gap).
# Front pipe (Blue suction, zorder=Z_BLUE) is continuous; rear pipe butts
# exactly to the front pipe OD edge.
_gap_half = OD_H / 2.0  # rear pipe stops at front pipe outer wall
# Rear pipe: below crossing (TAP_TEE_X, discharge Z → gap below suction Z)
draw_pipe_path(ax,
    [TAP_TEE_X, TAP_TEE_X],
    [PM_HEADER_Z_BLUE_DISCH, PM_HEADER_Z_BLUE_SUC - _gap_half],
    TAP_OD, TAP_WALL, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=7)
# Rear pipe: above crossing (gap above suction Z → BV-06)
draw_pipe_path(ax,
    [TAP_TEE_X, TAP_TEE_X, BV06_X - BV06_R],
    [PM_HEADER_Z_BLUE_SUC + _gap_half, TAP_BRANCH_Z, TAP_BRANCH_Z],
    TAP_OD, TAP_WALL, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=7)
draw_pipe_path(ax,
    [BV06_X + BV06_R, TAP_X, TAP_X],
    [TAP_BRANCH_Z, TAP_BRANCH_Z, TAP_Z],
    TAP_OD, TAP_WALL, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=7)

# BV-06 valve symbol (filled circle with label)
ax.add_patch(plt.Circle((sx(BV06_X), sz(TAP_BRANCH_Z)), BV06_R * S,
             fill=True, facecolor="white", edgecolor=C_OUT,
             linewidth=0.8, zorder=9))
ax.text(sx(BV06_X), sz(TAP_BRANCH_Z), "BV\n06",
        ha="center", va="center", fontsize=3, color=C_OUT,
        zorder=10, **FONT)

# Tap spout symbol
leader(ax, sx(TAP_X), sz(TAP_Z),
       sx(TAP_X + 150), sz(TAP_Z - 80),
       "TAP-01", fs=4.5, color=C_DIM, zorder=10)

# ── Pull-cord switches ───────────────────────────────────────────────────
for psx, plabel in [(PS_X_D, "D"), (PS_X_G, "G")]:
    # Switch body (small rectangle at ceiling)
    sw_w, sw_h = 30, 30
    equip_block(psx - sw_w / 2, PS_Z - sw_h / 2, sw_w, sw_h,
                plabel, "#F0E0C0", lw=0.5, zorder=6, alpha=0.7, label_fs=4)
    # Pull cord (dashed line)
    ax.plot([sx(psx), sx(psx)], [sz(PS_Z - sw_h / 2), sz(CORD_HANG_Z)],
            color=C_DIM, lw=0.4, ls=":", zorder=5)

# ── Shelf hanger rods (ghost — shelf is at Yd=300, not on wall face) ─────
# Show the 4 hanger rod positions as solid dark lines
C_SHELF_DK = "#8A7A3A"   # darker gold for hangers/shelf — contrast with wall
hanger_xs = [SHELF_X_L, SHELF_X_R]  # 2 pairs at shelf corners
for hx in hanger_xs:
    ax.plot([sx(hx), sx(hx)], [sz(SHELF_H), sz(TK_Z)],
            color=C_SHELF_DK, lw=1.2, ls="--", zorder=4)

# Shelf ghost outline (behind walkway plane at Yd=300, but drawn darker)
equip_block(SHELF_X_L, SHELF_H - SHELF_T, SHELF_X_R - SHELF_X_L, SHELF_T,
            "", C_SHELF_DK, ls="--", alpha=0.6, lw=1.2, zorder=4)
ax.text(sx((SHELF_X_L + SHELF_X_R) / 2), sz(SHELF_H - SHELF_T - 30),
        "CHEM SHELF (Yd=300, BEHIND)", ha="center", va="top",
        fontsize=4, color=C_SHELF_DK, style="italic", zorder=10, **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 5. DIMENSION LINES — key clearances and positions
# ═══════════════════════════════════════════════════════════════════════════

# Right-side vertical dims (cargo door end = X=0 = right side after mirror)
rx0 = sx(0) + 0.15        # first dim line
rx1 = rx0 + 0.5           # second

# Full container height
draw_dim_v(ax, rx0, sz(0), sz(C_HGT),
           f"{C_HGT}mm", offset=0.2, fs=5, right=True)

# Walkway deck height
draw_dim_v(ax, rx1, sz(0), sz(WALKWAY_H),
           f"{WALKWAY_H}", offset=0.2, fs=5, right=True)

# Filter skid Z range
draw_dim_v(ax, rx1, sz(FSKID_Z_LO), sz(FSKID_Z_HI),
           f"{FSKID_Z_HI - FSKID_Z_LO}", offset=0.2, fs=5, right=True)

# Left-side vertical dims (IBC end = X=C_LEN = left side after mirror)
lx0 = sx(C_LEN) - 0.15
lx1 = lx0 - 0.5

# Pinhole height
draw_dim_v(ax, lx0, sz(0), sz(PH_H),
           f"{PH_H}mm", offset=0.2, fs=5)

# ── Horizontal dims below floor ─────────────────────────────────────────────
# Row 1: equipment widths
row1_z = sz(0) - 0.20
row2_z = row1_z - 0.25

# Key gap dimensions
evap_r = EVAP_X + EVAP_W
pump_r = PUMP_X + PUMP_W
ba_r = BA_X + BA_W

# Evap → EP gap
draw_dim_h(ax, sx(evap_r), sx(EP_X), row1_z,
           f"{EP_X - evap_r}mm", offset=0.15, fs=4.5, above=False)

# BAT right → Pinhole
draw_dim_h(ax, sx(ba_r), sx(PH_X), row1_z,
           f"{PH_X - ba_r}mm", offset=0.15, fs=4.5, above=False)

# Pump → Filter skid gap
draw_dim_h(ax, sx(pump_r), sx(FSKID_X), row1_z,
           f"{FSKID_X - pump_r}mm", offset=0.15, fs=4.5, above=False)

# Full container length (below all)
draw_dim_h(ax, sx(0), sx(C_LEN), row2_z,
           f"{C_LEN}mm", offset=0.15, fs=5, above=False)

# ── Clearance leaders ──────────────────────────────────────────────────────
fskid_clr = TK_Z - FSKID_Z_HI
leader(ax, sx(FSKID_X + FSKID_W / 2), sz(FSKID_Z_HI),
       sx(FSKID_X + FSKID_W + 250), sz(FSKID_Z_HI + 250),
       f"SKID TOP → TRUNKING: {fskid_clr}mm", fs=4.5, color=C_DIM, zorder=10)

ep_clr = C_HGT - EP_H_HI
leader(ax, sx(EP_X + EP_W / 2), sz(EP_H_HI),
       sx(EP_X - 300), sz(EP_H_HI + 300),
       f"EP TOP → CEILING: {ep_clr}mm", fs=4.5, color=C_DIM, zorder=10)

# ═══════════════════════════════════════════════════════════════════════════
# 6. X-POSITION ANNOTATIONS (absolute positions along top)
# ═══════════════════════════════════════════════════════════════════════════
ann_y = sz(C_HGT) + 0.15
items = [
    (EVAP_X, "EVAP\nX=930"),
    (EP_X, "EP\nX=1600"),
    (BA_X, "BAT\nX=1810"),
    (PH_X, "PH\nX=2399"),
    (PUMP_X, "PUMP\nX=2500"),
    (FSKID_X, "FSKID\nX=2850"),
    (TAP_X, "TAP\nX=3729"),
]
for ix_mm, ilabel in items:
    ax.plot([sx(ix_mm), sx(ix_mm)], [sz(C_HGT), ann_y],
            color=C_DIM, lw=0.3, ls=":", zorder=1)
    ax.text(sx(ix_mm), ann_y + 0.05, ilabel, ha="center", va="bottom",
            fontsize=3.5, color=C_DIM, zorder=10, **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 7. INTERFERENCE NOTES
# ═══════════════════════════════════════════════════════════════════════════
notes = [
    "1. All internal pipe: ½\" HDPE (OD=21mm) except filter housings (1\" NPT). Blue circuit in blue, Brown in brown, Waste/Black in gray.",
    "2. Ext. power panel (dashed) is flush-mount on EXTERIOR face — no interior conflict with evap cooler.",
    "3. Chemistry shelf (dashed) is ceiling-hung at Yd=300mm — behind near walkway plane, not on wall face.",
    "4. Shelf hanger rods pass through cable trunking zone — requires grommets/slots in trunking lid.",
    "5. Pump manifold frame: 404mm W (Z=235–781). P-01/P-02 top, P-04 centered below with 20mm clearance. DV-02 on P-04 discharge.",
    "6. Battery right edge (X=2310) clears pinhole cone left boundary (X=2319 at Yd=0) by 9mm.",
    "7. Processing tray (304 SS, 50mm rim) sits on shims at Z=20. Sump well at X=2399, pickup tube to P-04 via walkway.",
    "8. All horizontal runs to IBCs enter IBC stack zone (X>4649) — routing within zone not shown.",
]
note_y = 0.06
for i, note in enumerate(notes):
    ax.text(0.01, note_y + i * 0.018, note, transform=ax.transAxes,
            fontsize=4.5, color=C_DIM, va="bottom", **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 8. TITLE BLOCK
# ═══════════════════════════════════════════════════════════════════════════
title_block(ax, "SHEET 1 OF 1",
            drawing_title="PINHOLE WALL — COMBINED INTERIOR ELEVATION",
            subtitle="ALL SYSTEMS · INTERFERENCE CHECK",
            scale_note="SCALE 1:20  ·  ALL DIMS IN mm",
            doc_id="TBS-001 · Pinhole Wall")

# ── Save ────────────────────────────────────────────────────────────────────
os.makedirs(DIAGRAMS_DIR, exist_ok=True)
out = os.path.join(DIAGRAMS_DIR, "pinhole-wall-elevation.png")
fig.savefig(out, dpi=150, facecolor="white", edgecolor="none")
plt.close(fig)
print(f"Pinhole wall elevation → {out}")
