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
    EVAP_DUCT_X, EVAP_DUCT_Z, EVAP_DUCT_D,
    PWR_PANEL_X, PWR_PANEL_W, PWR_PANEL_H,
    EP_X, EP_W, EP_H_LO, EP_H_HI,
    BA_X, BA_W, BA_H_LO, BA_H_HI, BA_D,
    PUMP_PIPE_OD, PUMP_PIPE_WALL,
    TAP_X, TAP_Z,
    SHELF_X_L, SHELF_X_R, SHELF_H, SHELF_T, SHELF_HANGER_N,
    SHELF_YD_NEAR, SHELF_DEPTH,
    WALKWAY_H, WALKWAY_GRATE_T, WALKWAY_W,
    WALKWAY_BRACKET_H, WALKWAY_BRACKET_T,
    WALKWAY_NEAR_WIDE_W, WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_X_R,
    CONTAINER_RIB_SPACING,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_DRAIN_X,
    PROC_TRAY_SUMP_W, PROC_TRAY_SUMP_D, PROC_TRAY_SUMP_Z, PROC_TRAY_RIM,
    PROC_TRAY_YD_NEAR, PROC_TRAY_D, PROC_TRAY_PITCH,
    SPRAY_BAR_FEED_Z,
    RAIL_OFF,
    FAN_B_H, FAN_B_YD, FAN_DIAM,
    C_OUT, C_CL, C_DIM,
    C_ALUM, C_STEEL, C_EVAP, C_ELEC, C_BATT,
    C_PINHOLE_EQ, C_WALL,
    ZONE_R_START,
    EQPANEL_X, EQPANEL_W,
    DIAGRAMS_DIR,
)
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_cl, draw_notes
from tbs_title_block import title_block

# ── Local constants (computed from tbs_constants) ────────────────────────────
# Pipe colors for Blue circuit (only Blue supply remains on this wall)
C_BLUE  = "#2979B8"      # Blue circuit pipe fill
C_BLUE_EC = "#1A5A8A"    # Blue circuit pipe edge
OD_H = PUMP_PIPE_OD     # 21mm (1/2" HDPE)
WALL_H = PUMP_PIPE_WALL  # 3mm

# Walkway X range (near walkway = pinhole wall side)
WK_X_L = PROC_TRAY_X_L + WALKWAY_W   # 470mm — near walkway left edge (past left walkway)
WK_X_R = PROC_TRAY_X_R               # 4629mm — near walkway right edge

# Pull-cord switches (near evap duct penetration)
PS_X_D = EVAP_DUCT_X - 30   # 1170mm — switch D
PS_X_G = EVAP_DUCT_X + 90   # 1290mm — switch G
PS_Z = C_HGT - 60           # 2328mm — switch body Z
CORD_HANG_Z = 900           # pull cord bottom Z

# Cable trunking
TK_H = 25                   # trunking height (mm)
TK_Z = C_HGT - TK_H        # 2363mm — trunking bottom Z

# Power panel Z (flush-mount, exterior — shown as dashed outline)
PWR_Z_LO = 900              # external power panel bottom Z (fixed, not tied to EP height)

# Colors
C_SHELF = "#C8B06A"   # chemistry shelf (warm gold)
C_TRUNKING = "#808080" # cable trunking
C_DUCT = "#3DAA96"    # evap duct penetration (reuse evap color)

# ── Scale and layout ────────────────────────────────────────────────────────
# S maps mm → figure inches.  Container 5893×2388 must fit comfortably.
# Available drawing area ≈ 22" wide × 8" tall (in a 26×12" figure).
S = 0.00335   # mm → inches  (≈1:7.6 at screen DPI, ≈1:20 at 300dpi print)
FW = 26.0
FH = 12.0                       # elevation panel height (inches)
FH_PLAN = 5.0                   # plan view panel height (inches)
FH_TOTAL = FH + FH_PLAN         # total figure height
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
PLAN_FRAC = FH_PLAN / FH_TOTAL
ELEV_FRAC = FH / FH_TOTAL

fig = plt.figure(figsize=(FW, FH_TOTAL), dpi=150)

ax = fig.add_axes([0, PLAN_FRAC, 1, ELEV_FRAC])
ax.set_xlim(0, FW)
ax.set_ylim(0, FH)
ax.set_aspect("equal")
ax.axis("off")

ax2 = fig.add_axes([0, 0, 1, PLAN_FRAC])
ax2.set_xlim(0, FW)
ax2.set_ylim(0, FH_PLAN)
ax2.set_aspect("equal")
ax2.axis("off")

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
    (EVAP_DUCT_X,          EVAP_DUCT_Z + EVAP_DUCT_D / 2),  # evap duct — circuit E
    (EP_X + EP_W / 2,      EP_H_HI),                 # electrical panel
    (BA_X + BA_W / 2,      BA_H_HI),                 # battery bank
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
ax.text(sx((WK_X_L + WK_X_R) * 0.6), sz(WALKWAY_H + 5),
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

SUMP_X_L = PROC_TRAY_DRAIN_X - PROC_TRAY_SUMP_W / 2
SUMP_X_R = PROC_TRAY_DRAIN_X + PROC_TRAY_SUMP_W / 2

# Sump cavity — darker fill from tray floor down to Z=0
sump_pts_x = [sx(SUMP_X_L), sx(SUMP_X_L), sx(SUMP_X_R), sx(SUMP_X_R)]
sump_pts_z = [sz(TRAY_FLOOR_Z), sz(0), sz(0), sz(TRAY_FLOOR_Z)]
ax.fill(sump_pts_x, sump_pts_z, fc="#8BB8D8", ec=C_TRAY_EC, lw=0.8,
        alpha=0.5, zorder=2.9)

# Pickup tube — 1" HDPE tube from Z=5 up to walkway level
TUBE_OD_VIS = 25.4  # 1" OD
TUBE_X = PROC_TRAY_DRAIN_X
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
ax.text(sx(PROC_TRAY_X_L + 350), sz(TRAY_RIM_TOP / 2),
        "PROCESSING TRAY (304 SS, 50mm RIM)", ha="left", va="center",
        fontsize=4.0, color=C_TRAY_EC, zorder=10, **FONT)

ax.text(sx(SUMP_X_L - 40), sz(TRAY_FLOOR_Z / 2 + 20),
        "SUMP WELL", ha="right", va="center",
        fontsize=4.5, color="#0D47A1", zorder=10, **FONT)

ax.text(sx(TUBE_X - 40), sz(TRAY_RIM_TOP + 5),
        "PICKUP TUBE", ha="right", va="bottom",
        fontsize=4.5, color="#666666", zorder=10, **FONT)
# Leader from pickup label to tube
ax.plot([sx(TUBE_X - 35), sx(TUBE_X - 5)],
        [sz(TRAY_RIM_TOP + 5), sz(TRAY_RIM_TOP + 5)],
        color="#666666", lw=0.3, zorder=10)
ax.plot([sx(TUBE_X - 5), sx(TUBE_X)],
        [sz(TRAY_RIM_TOP + 5), sz(TUBE_Z_TOP - 5)],
        color="#666666", lw=0.3, zorder=10)

# ── Zone labels for empty areas ───────────────────────────────────────────
# Left end zone (X=0–150mm, cargo door / hinged panel)
ax.text(sx(125), sz(C_HGT / 2), "CARGO DOOR\nEND\n(HINGED PANEL)",
        ha="center", va="center", fontsize=5, color="#AAAAAA",
        style="italic", zorder=2, **FONT)

# Right end zone (X=4649–5893mm, IBC stack)
ax.text(sx(ZONE_R_START + (C_LEN - ZONE_R_START) / 2), sz(C_HGT * 0.8),
        "IBC STACK\nZONE", ha="center", va="center",
        fontsize=5, color="#AAAAAA", style="italic", zorder=2, **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 4. EQUIPMENT BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

# ── Evaporative cooler duct penetration (rev 7: cooler now external) ────────
duct_r = EVAP_DUCT_D / 2
ax.add_patch(plt.Circle((sx(EVAP_DUCT_X), sz(EVAP_DUCT_Z)), duct_r * S,
             fill=True, facecolor=C_DUCT, edgecolor=C_OUT,
             linewidth=1.2, zorder=8, alpha=0.6))
ax.text(sx(EVAP_DUCT_X), sz(EVAP_DUCT_Z), f"DUCT\nØ{EVAP_DUCT_D}",
        ha="center", va="center", fontsize=4.0, color=C_OUT, zorder=9, **FONT)
leader(ax, sx(EVAP_DUCT_X), sz(EVAP_DUCT_Z - duct_r),
       sx(EVAP_DUCT_X + 300), sz(EVAP_DUCT_Z - 200),
       "EVAP COOLER DUCT\n(EXTERNAL UNIT)", fs=4.5, color=C_DIM,
       ha="center", va="top", lw=0.6, zorder=10, font=FONT)

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

# ── Equipment panel relocation note (rev 7) ───────────────────────────────
# Pump manifold (P-01/P-02/P-04), ACC-01, and filter housings (F1/F2/F3)
# are now on the equipment panel in the IBC plumbing corridor (Yd=1046).
# They are NOT on the pinhole wall — see panel layout detail diagram.
_note_x = (PH_X + ZONE_R_START) / 2  # centered between pinhole and IBC zone
_note_z = 450
ax.text(sx(_note_x), sz(_note_z),
        "PUMPS · FILTERS · ACC-01\nRELOCATED TO EQUIPMENT PANEL\n(IBC CORRIDOR, Yd=1046)\nSEE PANEL LAYOUT DETAIL",
        ha="center", va="center", fontsize=5, color="#999999",
        style="italic", zorder=2, **FONT,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#CCCCCC", lw=0.5, alpha=0.8))

# ═══════════════════════════════════════════════════════════════════════════
# 4a. PLUMBING — Blue supply to spray bar (rev 7: simplified)
# ═══════════════════════════════════════════════════════════════════════════
# All pump/filter/valve internal routing relocated to equipment panel
# (Yd=1046). Only the Blue supply trunk and chemistry tap remain on this wall.

IBC_PIPE_EXIT_X = ZONE_R_START   # pipes enter IBC stack zone

# Blue supply pipe: IBC zone → full length to spray bar at Z=75
SUPPLY_Z = SPRAY_BAR_FEED_Z  # 75mm — below walkway grating
draw_pipe_path(ax,
    [IBC_PIPE_EXIT_X, WK_X_L],
    [SUPPLY_Z, SUPPLY_Z],
    OD_H, WALL_H, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=8)

# Flow arrow: Blue supply flowing right in drawing (toward cargo door = lower X)
_supply_mid_x = (IBC_PIPE_EXIT_X + WK_X_L) / 2
ax.annotate("", xy=(sx(_supply_mid_x - 200), sz(SUPPLY_Z)),
            xytext=(sx(_supply_mid_x + 200), sz(SUPPLY_Z)),
            arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=1.0), zorder=10)
ax.text(sx(_supply_mid_x), sz(SUPPLY_Z - 30),
        "BLUE SUPPLY → SPRAY BAR (Z=75, BELOW GRATING)", ha="center", va="top",
        fontsize=4, color=C_BLUE, zorder=10, **FONT)

# ── Chemistry tap branch (TAP-01 / BV-06) ───────────────────────────────
# Branch tee off the Blue supply trunk at Z=75, rises to tap height.
TAP_OD = 25     # 3/4" branch pipe
TAP_WALL = 3
TAP_BRANCH_Z = TAP_Z + 100   # 1250mm — horizontal run height
TAP_TEE_X = 3400              # tee point on Blue supply trunk
BV06_X = 3600                 # valve position — close to shelf left edge (3729)
BV06_R = 25                   # valve body radius for symbol

# Riser from Z=75 up to TAP_BRANCH_Z, horizontal to BV-06
draw_pipe_path(ax,
    [TAP_TEE_X, TAP_TEE_X, BV06_X - BV06_R],
    [SUPPLY_Z, TAP_BRANCH_Z, TAP_BRANCH_Z],
    TAP_OD, TAP_WALL, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=7)
# BV-06 to TAP-01
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
ax.text(sx((SHELF_X_L + SHELF_X_R) / 2), sz(SHELF_H - SHELF_T + 60),
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
           f"{WALKWAY_H}mm", offset=0.2, fs=5, right=True)

# Electrical panel Z range
draw_dim_v(ax, rx1, sz(EP_H_LO), sz(EP_H_HI),
           f"{EP_H_HI - EP_H_LO}mm", offset=0.2, fs=5, right=True)

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
ba_r = BA_X + BA_W

# Duct → EP gap
draw_dim_h(ax, sx(EVAP_DUCT_X), sx(EP_X), row1_z,
           f"{EP_X - EVAP_DUCT_X}mm", offset=0.15, fs=4.5, above=False)

# BAT right → Pinhole
draw_dim_h(ax, sx(ba_r), sx(PH_X), row1_z,
           f"{PH_X - ba_r}mm", offset=0.15, fs=4.5, above=False)

# Full container length (below all)
draw_dim_h(ax, sx(0), sx(C_LEN), row2_z,
           f"{C_LEN}mm", offset=0.15, fs=5, above=False)

# ── Clearance leaders ──────────────────────────────────────────────────────
ep_clr = C_HGT - EP_H_HI
leader(ax, sx(EP_X + EP_W / 2), sz(EP_H_HI),
       sx(EP_X - 300), sz(EP_H_HI + 300),
       f"EP TOP → CEILING: {ep_clr}mm", fs=4.5, color=C_DIM, zorder=10)

# ═══════════════════════════════════════════════════════════════════════════
# 6. X-POSITION ANNOTATIONS (absolute positions along top)
# ═══════════════════════════════════════════════════════════════════════════
ann_y = sz(C_HGT) + 0.15
items = [
    (EVAP_DUCT_X, f"DUCT\nX={EVAP_DUCT_X}"),
    (EP_X, f"EP\nX={EP_X}"),
    (BA_X, f"BAT\nX={BA_X}"),
    (PH_X, f"PH\nX={PH_X}"),
    (TAP_X, f"TAP\nX={TAP_X}"),
]
for ix_mm, ilabel in items:
    ax.plot([sx(ix_mm), sx(ix_mm)], [sz(C_HGT), ann_y],
            color=C_DIM, lw=0.3, ls=":", zorder=1)
    ax.text(sx(ix_mm), ann_y + 0.05, ilabel, ha="center", va="bottom",
            fontsize=4, color=C_DIM, zorder=10, **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 7. INTERFERENCE NOTES
# ═══════════════════════════════════════════════════════════════════════════
notes = [
    "NOTES — REV 7 REORG",
    "1. Blue supply pipe: ½\" HDPE (OD=21mm) at Z=75 (below walkway grating),",
    "   from IBC zone to spray bar. Chemistry tap branch (¾\") rises to shelf.",
    "2. Evap cooler relocated EXTERNAL — only Ø200mm duct penetration remains at X=1200, Z=2100.",
    "3. Pumps (P-01/P-02/P-04), ACC-01, filter housings (F1/F2/F3), DV-01, DV-02",
    "   relocated to equipment panel in IBC plumbing corridor (Yd=1046). See panel layout detail.",
    "4. Ext. power panel (dashed) is flush-mount on EXTERIOR face — no interior conflict.",
    "5. Chemistry shelf (dashed) is ceiling-hung at Yd=300mm — behind near walkway plane.",
    "6. Shelf hanger rods pass through cable trunking zone — requires grommets/slots in trunking lid.",
    "7. Battery bank: slim-profile 120mm depth (was 220mm). Right edge (X=2310) clears pinhole cone",
    "   left boundary (X=2319 at Yd=0) by 9mm.",
    "8. EP raised to Z=1600–2200 (was 900–1500) to clear widened walkway at 500mm.",
    "9. Processing tray sump relocated to X=4550 (IBC corner), slope to corner.",
]
draw_notes(ax, notes, 0.105 * FW, 0.65 * FH, spacing=0.012 * FH,
           fs=4.5, width=4.75, color=C_DIM, title_color=C_DIM, font=FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 8. PLAN VIEW — NEAR WALKWAY ACCESS ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
# Shows component footprints in X vs Yd (depth from pinhole wall).
# Yd scale is exaggerated 1.5x vs X for depth visibility.
# The component with the largest egress into the walkway at any X position
# is drawn solid; others at the same X position are ghosted.

EP_DEPTH_YD     = 160    # electrical panel box depth (mm)
BA_DEPTH_YD     = BA_D   # battery bank: slim-profile (120mm)

PLAN_S_YD = S * 1.5             # Yd scale ~1.5x elevation X scale
PLAN_OYD  = 0.8                 # Y offset in ax2 data coords

def plan_sy(yd_mm):
    """Convert Yd (mm from wall) to plan view y coordinate on ax2."""
    return PLAN_OYD + yd_mm * PLAN_S_YD

def plan_block(xl, xr, yd_near, yd_far, label, fc, *,
               ec=C_OUT, lw=1.0, ls="-", alpha=0.75,
               label_fs=4.5, label_color=C_OUT, zorder=5):
    """Draw a component footprint rectangle on the plan view (ax2)."""
    x_draw = sx(xr)
    w_draw = sx(xl) - sx(xr)
    y_draw = plan_sy(yd_near)
    h_draw = plan_sy(yd_far) - plan_sy(yd_near)
    ax2.add_patch(mpatches.FancyBboxPatch(
        (x_draw, y_draw), w_draw, h_draw,
        boxstyle="square,pad=0", fc=fc, ec=ec,
        lw=lw, ls=ls, alpha=alpha, zorder=zorder))
    if label:
        cx = sx((xl + xr) / 2)
        cy = plan_sy((yd_near + yd_far) / 2)
        ax2.text(cx, cy, label, ha="center", va="center",
                fontsize=label_fs, color=label_color,
                zorder=zorder + 1, **FONT)

# ── Container wall line (Yd=0) ──────────────────────────────────────────────
ax2.plot([sx(0), sx(C_LEN)], [plan_sy(0), plan_sy(0)],
        color=C_OUT, lw=2.5, zorder=2)
ax2.text(sx(C_LEN / 2), plan_sy(0) - 0.12,
        "PINHOLE WALL (Yd = 0)", ha="center", va="top",
        fontsize=5, color=C_OUT, fontweight="bold", zorder=10, **FONT)

# ── Walkway grating zone (X=470-4629, Yd=0-300mm) ──────────────────────────
wk_x_draw = sx(WK_X_R)
wk_w_draw = sx(WK_X_L) - sx(WK_X_R)
ax2.add_patch(mpatches.FancyBboxPatch(
    (wk_x_draw, plan_sy(0)), wk_w_draw, plan_sy(WALKWAY_W) - plan_sy(0),
    boxstyle="square,pad=0", fc="#F0F0F0", ec="none", alpha=0.5, zorder=1))
for hx in range(int(WK_X_L), int(WK_X_R), 200):
    ax2.plot([sx(hx), sx(hx + 100)],
            [plan_sy(0), plan_sy(WALKWAY_W)],
            color="#D8D8D8", lw=0.2, zorder=1)
ax2.text(sx(500), plan_sy(WALKWAY_W / 2),
        "NEAR WALKWAY\n(300mm)", ha="center", va="center",
        fontsize=5, color="#BBBBBB", style="italic", zorder=2, **FONT)

# ── Walkway outer edge (Yd=300mm) ──────────────────────────────────────────
ax2.plot([sx(0), sx(C_LEN)], [plan_sy(WALKWAY_W), plan_sy(WALKWAY_W)],
        color=C_OUT, lw=1.0, ls="--", zorder=2)
ax2.text(sx(50), plan_sy(WALKWAY_W) + 0.06,
        "WALKWAY OUTER EDGE (Yd = 300)", ha="left", va="bottom",
        fontsize=4.5, color=C_DIM, zorder=10, **FONT)

# ── Component footprints ────────────────────────────────────────────────────
plan_comps = [
    ("ELECTRICAL\nPANEL", EP_X, EP_X + EP_W,
     0, EP_DEPTH_YD, C_ELEC, f"Z = {EP_H_LO}–{EP_H_HI}"),
    ("BATTERY\nBANK", BA_X, BA_X + BA_W,
     0, BA_DEPTH_YD, C_BATT, f"Z = {BA_H_LO}–{BA_H_HI}"),
    ("CHEMISTRY\nSHELF", SHELF_X_L, SHELF_X_R,
     SHELF_YD_NEAR, SHELF_YD_NEAR + SHELF_DEPTH, C_SHELF, f"Z = {SHELF_H}"),
]

# Determine max-egress status: solid if no other component fully covers
# this component's X range with deeper Yd; ghosted otherwise.
comp_solid = []
for i, (_, xl, xr, yn, yf, _, _) in enumerate(plan_comps):
    dominated = False
    for j, (_, oxl, oxr, oyn, oyf, _, _) in enumerate(plan_comps):
        if i == j:
            continue
        if oxl <= xl and oxr >= xr and oyn <= yn and oyf > yf:
            dominated = True
            break
    comp_solid.append(not dominated)

# Draw ghosted components first, then solid on top
for solid_pass in (False, True):
    for k, (name, xl, xr, yn, yf, color, zr) in enumerate(plan_comps):
        is_solid = comp_solid[k]
        if is_solid != solid_pass:
            continue
        alpha = 0.75 if is_solid else 0.25
        lw_c = 1.0 if is_solid else 0.5
        ls_c = "-" if is_solid else "--"
        zo = 5 if is_solid else 3
        lbl_fs = 4.5 if is_solid else 3.5
        lbl_col = C_OUT if is_solid else "#999"
        plan_block(xl, xr, yn, yf, name, color,
                   lw=lw_c, ls=ls_c, alpha=alpha, zorder=zo,
                   label_fs=lbl_fs, label_color=lbl_col)

# Z range annotations inside solid components (lower portion)
for k, (name, xl, xr, yn, yf, color, zr) in enumerate(plan_comps):
    if not comp_solid[k]:
        continue
    cx = sx((xl + xr) / 2)
    cy_bot = plan_sy(yn + (yf - yn) * 0.2)
    ax2.text(cx, cy_bot, zr, ha="center", va="center",
            fontsize=3, color="#666", zorder=6, **FONT)

# ── Processing tray near rim (context) ──────────────────────────────────────
ax2.plot([sx(PROC_TRAY_X_L), sx(PROC_TRAY_X_R)],
        [plan_sy(PROC_TRAY_YD_NEAR), plan_sy(PROC_TRAY_YD_NEAR)],
        color=C_TRAY_EC, lw=0.8, ls=":", zorder=4)
ax2.text(sx(PROC_TRAY_X_R - 150), plan_sy(PROC_TRAY_YD_NEAR) + 0.04,
        "PROC TRAY NEAR RIM (Yd = 80)", ha="right", va="bottom",
        fontsize=4.0, color=C_TRAY_EC, zorder=10, **FONT)

# ── Widened walkway section (EP/BAT zone, 500mm) ───────────────────────────
ww_x_draw = sx(WALKWAY_NEAR_WIDE_X_R)
ww_w_draw = sx(WALKWAY_NEAR_WIDE_X_L) - sx(WALKWAY_NEAR_WIDE_X_R)
ax2.add_patch(mpatches.FancyBboxPatch(
    (ww_x_draw, plan_sy(WALKWAY_W)), ww_w_draw,
    plan_sy(WALKWAY_NEAR_WIDE_W) - plan_sy(WALKWAY_W),
    boxstyle="square,pad=0", fc="#E8FFE8", ec="#66AA66",
    lw=1.0, ls="--", alpha=0.4, zorder=2))
ax2.text(sx((WALKWAY_NEAR_WIDE_X_L + WALKWAY_NEAR_WIDE_X_R) / 2),
        plan_sy((WALKWAY_W + WALKWAY_NEAR_WIDE_W) / 2),
        f"WIDENED TO {WALKWAY_NEAR_WIDE_W}mm", ha="center", va="center",
        fontsize=4, color="#448844", fontweight="bold", zorder=10, **FONT)

# ── Depth dimension lines ───────────────────────────────────────────────────
_dim_items = [
    (EP_X + EP_W * 0.75, EP_DEPTH_YD, f"{EP_DEPTH_YD}mm", C_ELEC),
    (BA_X + BA_W * 0.75, BA_DEPTH_YD, f"{BA_DEPTH_YD}mm", C_BATT),
]
for _dx_mm, _yd_max, _dlabel, _dcolor in _dim_items:
    draw_dim_v(ax2, sx(_dx_mm), plan_sy(0), plan_sy(_yd_max),
               _dlabel, offset=0.1, fs=4.5, color=_dcolor,
               right=True, font=FONT)

# ── Yd scale marks (right side) ─────────────────────────────────────────────
_yd_scale_x = sx(0) + 0.2
for _yd_val in range(0, 601, 100):
    _y = plan_sy(_yd_val)
    ax2.plot([_yd_scale_x - 0.04, _yd_scale_x + 0.04], [_y, _y],
            color=C_DIM, lw=0.4, zorder=10)
    ax2.text(_yd_scale_x + 0.08, _y, f"{_yd_val}",
            ha="left", va="center", fontsize=4.0, color=C_DIM,
            zorder=10, **FONT)
ax2.text(_yd_scale_x + 0.08, plan_sy(300) + 0.25,
        "Yd (mm)\n↑ INTO CONTAINER", ha="left", va="bottom",
        fontsize=4, color=C_DIM, fontweight="bold", zorder=10, **FONT)

# ── Section title ───────────────────────────────────────────────────────────
_plan_title_y = FH_PLAN - 0.45
ax2.text(sx(C_LEN / 2), _plan_title_y,
        "PLAN VIEW — NEAR WALKWAY ACCESS ANALYSIS",
        ha="center", va="bottom", fontsize=9, color=C_OUT,
        fontweight="bold", zorder=10, **FONT)
ax2.text(sx(C_LEN / 2), _plan_title_y - 0.12,
        "VIEW: LOOKING DOWN · Yd SCALE 1.5× EXAGGERATED"
        " · MAX-EGRESS SOLID, OTHERS GHOSTED",
        ha="center", va="top", fontsize=4.5, color=C_DIM,
        zorder=10, **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 9. TITLE BLOCK
# ═══════════════════════════════════════════════════════════════════════════
title_block(ax2, "SHEET 1 OF 1",
            drawing_title="PINHOLE WALL — COMBINED ELEVATION + PLAN VIEW",
            subtitle="ALL SYSTEMS · INTERFERENCE CHECK · WALKWAY ACCESS",
            scale_note="ELEV ~1:20 · PLAN Yd 1.5× EXAG."
                       " · ALL DIMS IN mm",
            doc_id="TBS-001 · Pinhole Wall",
            height=0.045 * FH / FH_PLAN)

# ── Save ────────────────────────────────────────────────────────────────────
os.makedirs(DIAGRAMS_DIR, exist_ok=True)
out = os.path.join(DIAGRAMS_DIR, "pinhole-wall-elevation.png")
fig.savefig(out, dpi=150, facecolor="white", edgecolor="none")
plt.close(fig)
print(f"Pinhole wall elevation → {out}")
