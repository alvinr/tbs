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

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from tbs_constants import C_LEN, C_HGT, PH_X, PH_H, EVAP_DUCT_X, EVAP_DUCT_Z, EVAP_DUCT_D, EVAP_STOW_X, EVAP_W, EVAP_D, EVAP_H, EVAP_STOW_Z, PWR_PANEL_X, PWR_PANEL_W, PWR_PANEL_H, PWR_PANEL_Z, EP_X, EP_W, EP_H_LO, EP_H_HI, BA_X, BA_W, BA_H_LO, BA_H_HI, BA_D, PUMP_PIPE_OD, PUMP_PIPE_WALL, TAP_X, TAP_Z, SHELF_X_L, SHELF_X_R, SHELF_H, SHELF_T, SHELF_STOW_TOP_Z, SHELF_YD_NEAR, SHELF_DEPTH, PULL_CORD_BOTTOM_Z, WALKWAY_H, WALKWAY_GRATE_T, WALKWAY_W, WALKWAY_BRACKET_T, WALKWAY_NEAR_WIDE_W, WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_X_R, CONTAINER_RIB_SPACING, PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_DRAIN_X, PROC_TRAY_SUMP_W, PROC_TRAY_SUMP_Z, PROC_TRAY_RIM, PROC_TRAY_YD_NEAR, SPRAY_BAR_FEED_Z, BV02_X, BV02_Z, C_OUT, C_CL, C_DIM, C_ALUM, C_STEEL, C_EVAP, C_ELEC, C_BATT, C_PINHOLE_EQ, ZONE_R_START, DIAGRAMS_DIR
from tbs_drawing import (draw_dim_h, draw_dim_v, leader, draw_cl, draw_notes,
                         draw_pipe_path as _tbs_pipe_path)
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

# Pull-cord switches — ceiling-mounted, left of the electrical panel (cleared)
PS_X_D = 1450               # switch D — left of EP (EP now starts at X=1910)
PS_X_G = 1530               # switch G
PS_Z = C_HGT - 30           # 2358mm — ceiling-mounted switch body Z
CORD_HANG_Z = PULL_CORD_BOTTOM_Z   # 1180 — cord bottom; clears the deployed chem shelf below

# Cable trunking
TK_H = 25                   # trunking height (mm)
TK_Z = C_HGT - TK_H        # 2363mm — trunking bottom Z

# Power panel Z (flush-mount, exterior — shown as dashed outline)
PWR_PANEL_Z = 900              # external power panel bottom Z (fixed, not tied to EP height)

# Colors
C_SHELF = "#C8B06A"   # chemistry shelf (warm gold)
C_TRUNKING = "#808080" # cable trunking
C_DUCT = "#3DAA96"    # evap duct penetration (reuse evap color)

# ── Scale and layout ────────────────────────────────────────────────────────
# All coordinates in mm.  Axis inversion handles the interior-view mirror
# (high X / IBC end on LEFT, low X / cargo door on RIGHT).
FIG_W = 26.0                     # figure width (inches)
FIG_H_ELEV = 12.0                # elevation panel height (inches)
FIG_H_PLAN = 5.0                 # plan view panel height (inches)
FIG_H_TOTAL = FIG_H_ELEV + FIG_H_PLAN

PAD_X_IBC = 750                  # margin past IBC end (left in display)
PAD_X_CARGO = 1120               # margin past cargo door (right in display)
PAD_Z_BOT = 750                  # below floor (notes + dims)
PAD_Z_TOP = 450                  # above ceiling (annotations)

X_LO = -PAD_X_CARGO              # -1120
X_HI = C_LEN + PAD_X_IBC         # 6643
Z_LO = -PAD_Z_BOT                # -750
Z_HI = C_HGT + PAD_Z_TOP         # 2838

YD_EXAG = 1.5                    # plan view Yd exaggeration factor
PLAN_Y_LO = -240                 # plan Y range (plan_sy units)
PLAN_Y_HI = 1260

def sx(x_mm):
    """X position in mm — axis inversion handles interior-view mirror."""
    return x_mm

def sz(z_mm):
    """Z position in mm AFF."""
    return z_mm

# ── Figure setup ────────────────────────────────────────────────────────────
PLAN_FRAC = FIG_H_PLAN / FIG_H_TOTAL
ELEV_FRAC = FIG_H_ELEV / FIG_H_TOTAL

fig = plt.figure(figsize=(FIG_W, FIG_H_TOTAL), dpi=150)

ax = fig.add_axes([0, PLAN_FRAC, 1, ELEV_FRAC])
ax.set_xlim(X_LO, X_HI)
ax.set_ylim(Z_LO, Z_HI)
ax.invert_xaxis()
ax.set_aspect("equal")
ax.axis("off")

ax2 = fig.add_axes([0, 0, 1, PLAN_FRAC])
ax2.set_xlim(X_LO, X_HI)
ax2.set_ylim(PLAN_Y_LO, PLAN_Y_HI)
ax2.invert_xaxis()
ax2.set_aspect("equal")
ax2.axis("off")

FONT = {"fontfamily": "monospace"}

# ── Helper: filled, labeled equipment block ─────────────────────────────────
def equip_block(x_mm, z_mm, w_mm, h_mm, label, fc, *,
                ec=C_OUT, lw=1.0, zorder=5, ls="-", alpha=0.85,
                label_fs=5.5, label_color=C_OUT):
    """Draw a filled rectangle with centered label."""
    rect = mpatches.FancyBboxPatch(
        (sx(x_mm), sz(z_mm)), w_mm, h_mm,
        boxstyle="square,pad=0", facecolor=fc, edgecolor=ec,
        linewidth=lw, linestyle=ls, alpha=alpha, zorder=zorder)
    ax.add_patch(rect)
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
    """Thin wrapper → tbs_drawing.draw_pipe_path (canonical body); injects the
    mirrored sx()/sz() scale funcs.  See skills/skill_plumbing_drawing.md."""
    _tbs_pipe_path(ax, x_pts, z_pts, od_mm, wall_mm, fc, ec=ec,
                   bore_fc=bore_fc, elbow_r=elbow_r, zorder=zorder,
                   lw=0.5, sx=sx, sz=sz)


# ═══════════════════════════════════════════════════════════════════════════
# 1. CONTAINER OUTLINE
# ═══════════════════════════════════════════════════════════════════════════
# Outer rectangle
ax.add_patch(mpatches.Rectangle(
    (0, 0), C_LEN, C_HGT,
    facecolor="white", edgecolor=C_OUT, linewidth=2.0, zorder=1))

# Floor line (thicker)
ax.plot([0, C_LEN], [0, 0], color=C_OUT, lw=2.5, zorder=2)
# Ceiling line
ax.plot([0, C_LEN], [C_HGT, C_HGT], color=C_OUT, lw=2.0, zorder=2)
# Cargo door wall (X=0, right in display)
ax.plot([0, 0], [0, C_HGT], color=C_OUT, lw=2.0, zorder=2)
# IBC end wall (X=C_LEN, left in display)
ax.plot([C_LEN, C_LEN], [0, C_HGT], color=C_OUT, lw=2.0, zorder=2)

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
    (PWR_PANEL_X + PWR_PANEL_W / 2, PWR_PANEL_Z + PWR_PANEL_H),  # ext power panel
    (PS_X_D,               PS_Z + 15),                # pull-cord switch D
    (PS_X_G,               PS_Z + 15),                # pull-cord switch G
]
conduit_w = CONDUIT_OD       # conduit width in mm
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
ax.add_patch(plt.Circle((sx(EVAP_DUCT_X), sz(EVAP_DUCT_Z)), duct_r,
             fill=True, facecolor=C_DUCT, edgecolor=C_OUT,
             linewidth=1.2, zorder=8, alpha=0.6))
ax.text(sx(EVAP_DUCT_X), sz(EVAP_DUCT_Z), f"DUCT\nØ{EVAP_DUCT_D}",
        ha="center", va="center", fontsize=4.0, color=C_OUT, zorder=9, **FONT)
leader(ax, sx(EVAP_DUCT_X), sz(EVAP_DUCT_Z - duct_r),
       sx(EVAP_DUCT_X + 100), sz(EVAP_DUCT_Z - 200),
       "EVAP COOLER DUCT\n(EXTERNAL UNIT)", fs=4.5, color=C_DIM,
       ha="center", va="top", lw=0.6, zorder=10, font=FONT)

# ── Evaporative cooler — transport stowage ghost outline ───────────────────
equip_block(EVAP_STOW_X, EVAP_STOW_Z, EVAP_W, EVAP_H,
            "EVAP COOLER\n(TRANSPORT\nPOSITION ONLY)", C_EVAP,
            ls="--", alpha=0.25, lw=1.0, zorder=3, label_fs=4.5,
            label_color="#666666")

# ── External power panel (flush-mount, exterior — dashed outline) ──────────
equip_block(PWR_PANEL_X, PWR_PANEL_Z, PWR_PANEL_W, PWR_PANEL_H,
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
draw_cl(ax, sx(PH_X), sz(PH_H), ph_r,
        horiz=True, vert=True, color=C_CL, lw=0.6, ext_factor=3.0)
ax.add_patch(plt.Circle((sx(PH_X), sz(PH_H)), ph_r,
             fill=True, facecolor=C_PINHOLE_EQ, edgecolor=C_OUT,
             linewidth=1.2, zorder=8))
ax.text(sx(PH_X), sz(PH_H - 80), "PINHOLE\nØ2.17mm",
        ha="center", va="top", fontsize=5, color=C_PINHOLE_EQ,
        zorder=10, **FONT)

# ── Pinhole Wall Plumbing Panel — wet-end filter loop (pinhole-wall-mount refactor) ──
# The 3-stage Big Blue filter bank rides HIGH under the ceiling (heads ~2262-2340, sump bowls
# hanging to 1746); P-02 (Brown recycle) sits to its left; SV-01 drops to waist; DV-01 exits to
# the corridor mouth off the high-X edge. Positions match the pinhole-panel detail + the 3D
# pinhole-water-panel model. (The four CORRIDOR pumps P-01/P-03/P-04/P-05 + ACC-01 stay in the
# IBC corridor — see the panel-layout detail.)
C_FILT, C_FILT_EC, C_BROWN = "#C3D6E8", "#5A7A9A", "#8A5A3A"
_bb_r, _bb_bot, _bb_top, _bb_head = 92, 1746, 2340, 2262
ax.add_patch(mpatches.Rectangle((sx(2780), sz(920)), sx(4500) - sx(2780), sz(2360) - sz(920),
             facecolor="#EFE7D0", edgecolor="none", alpha=0.30, zorder=1))
ax.text(sx(3640), sz(2372),
        "PINHOLE-WALL PLUMBING PANEL — WET-END FILTER LOOP  (IBC-3 -> P-02 -> F-01/F-02/F-03 -> SV-01 -> DV-01)",
        ha="center", va="bottom", fontsize=4, color="#8A7A4A", zorder=3, **FONT)
# P-02 (Brown recycle pump) — upright, left of the bank
ax.add_patch(mpatches.Rectangle((sx(3008), sz(2139)), sx(3108) - sx(3008), sz(2319) - sz(2139),
             facecolor=C_BROWN, edgecolor=C_OUT, lw=0.8, zorder=8))
ax.text(sx(3058), sz(2129), "P-02\nBROWN\nRECYCLE", ha="center", va="top", fontsize=3.6, color=C_BROWN, zorder=10, **FONT)
# 3-stage Big Blue filter bank (heads near ceiling, sump bowls hanging)
for _fid, _fcx, _media in [("F-01", 3300, "5um SED"), ("F-02", 3638, "KDF-55"), ("F-03", 3976, "CARBON")]:
    _x0, _x1 = sx(_fcx - _bb_r), sx(_fcx + _bb_r)
    ax.add_patch(mpatches.Rectangle((_x0, sz(_bb_bot)), _x1 - _x0, sz(_bb_top) - sz(_bb_bot),
                 facecolor=C_FILT, edgecolor=C_FILT_EC, lw=1.0, zorder=7))
    ax.add_patch(mpatches.Rectangle((_x0, sz(_bb_head)), _x1 - _x0, sz(_bb_top) - sz(_bb_head),
                 facecolor="#8FA6BE", edgecolor=C_FILT_EC, lw=0.7, zorder=8))
    ax.text(sx(_fcx), sz(2000), _fid + "\n" + _media, ha="center", va="center", fontsize=3.6, color="#2A4A6A", zorder=10, **FONT)
# brown flow along the bank ports (P-02 -> F-01 -> F-02 -> F-03)
for _x0, _x1 in [(3108, 3208), (3392, 3546), (3730, 3884)]:
    ax.annotate("", xy=(sx(_x1), sz(2301)), xytext=(sx(_x0), sz(2301)),
                arrowprops=dict(arrowstyle="-|>", color=C_BROWN, lw=0.7), zorder=9)
# SV-01 pH sample tap (dropped to waist) + DV-01 exit to the corridor
ax.add_patch(plt.Circle((sx(4250), sz(975)), 5, facecolor="#C0392B", edgecolor=C_OUT, lw=0.7, zorder=9))
ax.annotate("", xy=(sx(4250), sz(1010)), xytext=(sx(4068), sz(2301)),
            arrowprops=dict(arrowstyle="-|>", color=C_BROWN, lw=0.7,
                            connectionstyle="angle,angleA=-90,angleB=0"), zorder=9)
ax.text(sx(4250), sz(915), "SV-01\npH SAMPLE", ha="center", va="top", fontsize=3.6, color="#C0392B", zorder=10, **FONT)
ax.annotate("", xy=(sx(4500), sz(975)), xytext=(sx(4262), sz(975)),
            arrowprops=dict(arrowstyle="-|>", color=C_BROWN, lw=0.7), zorder=9)
ax.text(sx(4510), sz(975), "-> DV-01\n(corridor)", ha="left", va="center", fontsize=3.6, color=C_BROWN, zorder=10, **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 4a. PLUMBING — Blue supply to spray bar (rev 7: simplified)
# ═══════════════════════════════════════════════════════════════════════════
# The wet-end FILTER LOOP (P-02 + F-01/F-02/F-03 + SV-01) is on THIS wall (drawn above); the four
# CORRIDOR pumps (P-01/P-03/P-04/P-05) + ACC-01 are in the IBC corridor. Blue supply trunk + chem tap below.

IBC_PIPE_EXIT_X = ZONE_R_START   # pipes enter IBC stack zone

# Blue supply pipe: IBC zone → TAP_X. The trunk TERMINATES at the chem tap (its leftmost
# consumer), so the trunk→tap-riser corner is a 90° elbow, not a through-tee (matches the
# 3D overview spray_supply(), x_l = TAP_X).
SUPPLY_Z = SPRAY_BAR_FEED_Z  # 30mm — beam center, below walkway grating
draw_pipe_path(ax,
    [IBC_PIPE_EXIT_X, TAP_X],
    [SUPPLY_Z, SUPPLY_Z],
    OD_H, WALL_H, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=8)

# Flow arrow: Blue supply flowing right in drawing (toward cargo door = lower X)
_supply_mid_x = (IBC_PIPE_EXIT_X + TAP_X) / 2
ax.annotate("", xy=(sx(_supply_mid_x - 200), sz(SUPPLY_Z)),
            xytext=(sx(_supply_mid_x + 200), sz(SUPPLY_Z)),
            arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=1.0), zorder=10)
ax.text(sx(_supply_mid_x + 500), sz(SUPPLY_Z + 5),
        f"BLUE SUPPLY → SPRAY BAR (Z={SUPPLY_Z}, BELOW GRATING)", ha="center", va="top",
        fontsize=4, color=C_BLUE, zorder=10, **FONT)

# ── BV-02 — spray bar isolation valve (riser from supply to Z=900) ───────


BV02_R = 25              # valve body radius for symbol

# Riser from supply pipe up to BV-02
draw_pipe_path(ax,
    [BV02_X, BV02_X],
    [SUPPLY_Z, BV02_Z],
    OD_H, WALL_H, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=8)

# BV-02 ball-valve symbol (bowtie inside white circle)
_bvx, _bvz = sx(BV02_X), sz(BV02_Z)
ax.add_patch(plt.Circle((_bvx, _bvz), BV02_R,
             fc="white", ec=C_BLUE_EC, lw=1.5, zorder=12))
_bs = BV02_R * 0.62      # bowtie triangle half-size
ax.add_patch(plt.Polygon([(_bvx - _bs, _bvz - _bs),
                          (_bvx - _bs, _bvz + _bs),
                          (_bvx, _bvz)],
                         fc=C_BLUE, ec=C_BLUE, zorder=13))
ax.add_patch(plt.Polygon([(_bvx + _bs, _bvz - _bs),
                          (_bvx + _bs, _bvz + _bs),
                          (_bvx, _bvz)],
                         fc=C_BLUE, ec=C_BLUE, zorder=13))
ax.text(_bvx, _bvz - BV02_R - 8, "BV-02",
        ha="center", va="top", fontsize=4, fontweight="bold",
        color=C_BLUE, zorder=13, **FONT)

leader(ax, sx(BV02_X), sz(BV02_Z + BV02_R + 5),
       sx(BV02_X - 10), sz(BV02_Z + 80),
       f"BV-02 @ Z={BV02_Z}mm\n(1/2\" BALL VALVE)\nSPRAY BAR ISOLATION\nWAIST HEIGHT",
       fs=4, color=C_BLUE, font=FONT, zorder=15)

# Flex hose stub from BV-02 (drops down to spray bar — off-wall)
ax.annotate("", xy=(sx(BV02_X - 100), sz(BV02_Z - 50)),
            xytext=(sx(BV02_X), sz(BV02_Z - BV02_R)),
            arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=0.8,
                            connectionstyle="arc3,rad=0.3"),
            zorder=10)
ax.text(sx(BV02_X - 80), sz(BV02_Z - 80),
        "FLEX HOSE\nTO SPRAY BAR\n(OFF WALL)",
        ha="center", va="top", fontsize=4.0, color=C_BLUE,
        style="italic", zorder=10, **FONT)

# ── Chemistry tap branch (TAP-01 / BV-06) ───────────────────────────────
# The Blue trunk ENDS at TAP_X, so the riser is an ELBOW off the trunk end (not a tee), and it
# rises RIGHT of the chem shelf (TAP_X=1130 < shelf X1180–1780, so clear of it). The spout then
# goosenecks out over the shelf to dispense at TAP_Z. (Matches the 3D overview spray_supply().)
TAP_OD = 25     # 3/4" branch pipe
TAP_WALL = 3
TAP_BRANCH_Z = SHELF_STOW_TOP_Z   # 1375 — riser top, above the stowed shelf
BV06_Z = 1010                     # BV-06 on the riser (matches the 3D BV-06 box at Z1010)
SPOUT_DX = 150                    # gooseneck reach over the shelf edge (display-left)

# Riser up at TAP_X (right of the shelf) — elbow off the trunk's terminating end.
draw_pipe_path(ax,
    [TAP_X, TAP_X],
    [SUPPLY_Z, TAP_BRANCH_Z],
    TAP_OD, TAP_WALL, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=7)
# Spout: goosenecks out over the shelf edge, then dispenses down at TAP_Z.
draw_pipe_path(ax,
    [TAP_X, TAP_X + SPOUT_DX, TAP_X + SPOUT_DX],
    [TAP_BRANCH_Z, TAP_BRANCH_Z, TAP_Z],
    TAP_OD, TAP_WALL, fc=C_BLUE, ec=C_BLUE_EC, bore_fc="white", zorder=7)

# BV-06 valve symbol (filled circle with label) on the riser
ax.add_patch(plt.Circle((sx(TAP_X), sz(BV06_Z)), 25,
             fill=True, facecolor="white", edgecolor=C_OUT,
             linewidth=0.8, zorder=9))
ax.text(sx(TAP_X), sz(BV06_Z), "BV\n06",
        ha="center", va="center", fontsize=4, color=C_OUT,
        zorder=10, **FONT)

# Tap spout symbol (at the gooseneck outlet, over the shelf)
leader(ax, sx(TAP_X + SPOUT_DX), sz(TAP_Z),
       sx(TAP_X + SPOUT_DX + 180), sz(TAP_Z - 90),
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

# ── Chem shelf — WALL-HINGED FOLD-DOWN (rev13) ──────────────────────────
C_SHELF_DK = "#8A7A3A"
# deployed board (solid) at work height, hinged on this wall (Yd0)
equip_block(SHELF_X_L, SHELF_H - SHELF_T, SHELF_X_R - SHELF_X_L, SHELF_T,
            "", C_SHELF, alpha=0.85, lw=1.2, zorder=6)
ax.text(sx((SHELF_X_L + SHELF_X_R) / 2), sz(SHELF_H - SHELF_T - 15),
        "CHEM SHELF (fold-down, deployed)", ha="center", va="top",
        fontsize=4, color=C_SHELF_DK, zorder=10, **FONT)
# piano hinge on the wall at the back edge (a tick at each end)
for hx in (SHELF_X_L, SHELF_X_R):
    ax.plot([sx(hx)], [sz(SHELF_H)], marker="o", ms=2.2, color=C_SHELF_DK, zorder=7)
# stowed (folded-up, transport) ghost — vertical against the wall, Z SHELF_H..STOW_TOP
equip_block(SHELF_X_L, SHELF_H, SHELF_X_R - SHELF_X_L, SHELF_STOW_TOP_Z - SHELF_H,
            "", C_SHELF_DK, ls="--", alpha=0.3, lw=1.0, zorder=4)
ax.text(sx((SHELF_X_L + SHELF_X_R) / 2), sz(SHELF_STOW_TOP_Z + 25),
        "(folds up for transport)", ha="center", va="bottom",
        fontsize=3.5, color=C_SHELF_DK, style="italic", zorder=10, **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 5. DIMENSION LINES — key clearances and positions
# ═══════════════════════════════════════════════════════════════════════════

# Right-side vertical dims (cargo door end = X=0, right in display)
# With inverted axis, lower X = further right in display
rx0 = -45        # first dim line, 45mm right of cargo door wall
rx1 = rx0 - 150  # second, 150mm further right

# Full container height
draw_dim_v(ax, rx0, sz(0), sz(C_HGT),
           f"{C_HGT}mm", offset=60, fs=5, right=False)

# Walkway deck height
draw_dim_v(ax, rx1, sz(0), sz(WALKWAY_H),
           f"{WALKWAY_H}mm", offset=60, fs=5, right=False)

# Electrical panel Z range
draw_dim_v(ax, rx1, sz(EP_H_LO), sz(EP_H_HI),
           f"{EP_H_HI - EP_H_LO}mm\nEP Height", offset=120, fs=5, right=False)

# Left-side vertical dims (IBC end = X=C_LEN, left in display)
# With inverted axis, higher X = further left in display
lx0 = C_LEN + 45

# Pinhole height
draw_dim_v(ax, lx0, sz(0), sz(PH_H),
           f"{PH_H}mm\nConatiner floor to Pinhole", offset=120, fs=5, right=True)

# ── Horizontal dims below floor ─────────────────────────────────────────────
row1_z = -60     # first dim row, 60mm below floor
row2_z = -135    # second dim row

ba_r = BA_X + BA_W

# Duct → EP gap
draw_dim_h(ax, sx(EVAP_DUCT_X), sx(EP_X), row1_z,
           f"{EP_X - EVAP_DUCT_X}mm", offset=45, fs=4.5, above=False)

# BAT right → Pinhole
draw_dim_h(ax, sx(ba_r), sx(PH_X), row1_z,
           f"{PH_X - ba_r}mm", offset=45, fs=4.5, above=False)

# Full container length (below all)
draw_dim_h(ax, sx(0), sx(C_LEN), row2_z,
           f"{C_LEN}mm", offset=45, fs=5, above=False)

# ── EP top → ceiling clearance — DIMENSIONED at rx1, continuing the EP chain
#    (1500→2100→2388). A ≥30mm clearance is a dimension, not a leader callout (skill P7). ──
draw_dim_v(ax, rx1, sz(EP_H_HI), sz(C_HGT),
           f"{C_HGT - EP_H_HI}mm\nEP to Ceiling", offset=120, fs=5, right=False)

# ═══════════════════════════════════════════════════════════════════════════
# 6. X-POSITION ANNOTATIONS (absolute positions along top)
# ═══════════════════════════════════════════════════════════════════════════
ann_y = C_HGT + 45
items = [
    (EVAP_DUCT_X, f"DUCT\nX={EVAP_DUCT_X}"),
    (EP_X, f"EP\nX={EP_X}"),
    (BA_X, f"BAT\nX={BA_X}"),
    (PH_X, f"PH\nX={PH_X}"),
    (TAP_X, f"TAP\nX={TAP_X}"),
]
for ix_mm, ilabel in items:
    ax.plot([sx(ix_mm), sx(ix_mm)], [C_HGT, ann_y],
            color=C_DIM, lw=0.3, ls=":", zorder=1)
    ax.text(sx(ix_mm), ann_y + 15, ilabel, ha="center", va="bottom",
            fontsize=4, color=C_DIM, zorder=10, **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 7. INTERFERENCE NOTES
# ═══════════════════════════════════════════════════════════════════════════
notes = [
    "NOTES",
    f"1. Blue supply pipe: ½\" HDPE (OD=21mm) at Z={SUPPLY_Z} (below walkway grating),"
    " from IBC zone to spray bar. BV-02 riser at pinhole centerline to Z=900 (waist height)."
    " Chemistry tap branch (¾\") rises to shelf.",
    f"2. Evap cooler relocated EXTERNAL — only Ø{EVAP_DUCT_D}mm duct penetration remains at X={EVAP_DUCT_X}, Z={EVAP_DUCT_Z}.",
    "3. Pinhole wall carries the wet-end filter loop: P-02, the 3-stage Big Blue bank (F-01/F-02/F-03)"
    " high under the ceiling, and SV-01. Corridor pumps P-01/P-03/P-04/P-05 + ACC-01 + DV-01/DV-02 are"
    " in the IBC corridor (Yd=1046). See panel-layout / pinhole-panel detail.",
    "4. Ext. power panel (dashed) is flush-mount on EXTERIOR face — no interior conflict.",
    "5. Chemistry shelf (dashed) is ceiling-hung at Yd=300mm — behind near walkway plane.",
    "6. Shelf hanger rods pass through cable trunking zone — requires grommets/slots in trunking lid.",
    "7. Battery bank: slim-profile 120mm depth (was 220mm). Right edge (X=2310) clears pinhole cone"
    " left boundary (X=2319 at Yd=0) by 9mm.",
    "8. EP raised to Z=1600–2200 (was 900–1500) to clear widened walkway at 500mm.",
    "9. Processing tray sump relocated to X=4550 (IBC corner), slope to corner.",
]
draw_notes(ax, notes, C_LEN - 70, -210, spacing=45,
           fs=7, width=3640, color=C_DIM, title_color=C_DIM, font=FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 8. PLAN VIEW — NEAR WALKWAY ACCESS ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
# Shows component footprints in X vs Yd (depth from pinhole wall).
# Yd scale is exaggerated 1.5x vs X for depth visibility.
# The component with the largest egress into the walkway at any X position
# is drawn solid; others at the same X position are ghosted.

EP_DEPTH_YD     = 160    # electrical panel box depth (mm)
BA_DEPTH_YD     = BA_D   # battery bank: slim-profile (120mm)

def plan_sy(yd_mm):
    """Convert Yd (mm from wall) to plan view y coordinate (1.5× exag.)."""
    return yd_mm * YD_EXAG

def plan_block(xl, xr, yd_near, yd_far, label, fc, *,
               ec=C_OUT, lw=1.0, ls="-", alpha=0.75,
               label_fs=4.5, label_color=C_OUT, zorder=5):
    """Draw a component footprint rectangle on the plan view (ax2)."""
    y_draw = plan_sy(yd_near)
    h_draw = plan_sy(yd_far) - plan_sy(yd_near)
    ax2.add_patch(mpatches.FancyBboxPatch(
        (xl, y_draw), xr - xl, h_draw,
        boxstyle="square,pad=0", fc=fc, ec=ec,
        lw=lw, ls=ls, alpha=alpha, zorder=zorder))
    if label:
        cx = sx((xl + xr) / 2)
        cy = plan_sy((yd_near + yd_far) / 2)
        ax2.text(cx, cy, label, ha="center", va="center",
                fontsize=label_fs, color=label_color,
                zorder=zorder + 1, **FONT)

# ── Container wall line (Yd=0) ──────────────────────────────────────────────
ax2.plot([0, C_LEN], [plan_sy(0), plan_sy(0)],
        color=C_OUT, lw=2.5, zorder=2)
ax2.text(C_LEN / 2, plan_sy(0) - 36,
        "PINHOLE WALL (Yd = 0)", ha="center", va="top",
        fontsize=5, color=C_OUT, fontweight="bold", zorder=10, **FONT)

# ── Walkway grating zone (X=470-4629, Yd=0-300mm) ──────────────────────────
ax2.add_patch(mpatches.FancyBboxPatch(
    (WK_X_L, plan_sy(0)), WK_X_R - WK_X_L, plan_sy(WALKWAY_W) - plan_sy(0),
    boxstyle="square,pad=0", fc="#F0F0F0", ec="none", alpha=0.5, zorder=1))
for hx in range(int(WK_X_L), int(WK_X_R), 200):
    ax2.plot([hx, hx + 100],
            [plan_sy(0), plan_sy(WALKWAY_W)],
            color="#D8D8D8", lw=0.2, zorder=1)
ax2.text(500, plan_sy(WALKWAY_W / 2),
        "NEAR WALKWAY\n(300mm)", ha="center", va="center",
        fontsize=5, color="#BBBBBB", style="italic", zorder=2, **FONT)

# ── Walkway outer edge (Yd=300mm) ──────────────────────────────────────────
ax2.plot([0, C_LEN], [plan_sy(WALKWAY_W), plan_sy(WALKWAY_W)],
        color=C_OUT, lw=1.0, ls="--", zorder=2)
ax2.text(50, plan_sy(WALKWAY_W) + 18,
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
            fontsize=4, color="#666", zorder=6, **FONT)

# ── Processing tray near rim (context) ──────────────────────────────────────
ax2.plot([PROC_TRAY_X_L, PROC_TRAY_X_R],
        [plan_sy(PROC_TRAY_YD_NEAR), plan_sy(PROC_TRAY_YD_NEAR)],
        color=C_TRAY_EC, lw=0.8, ls=":", zorder=4)
ax2.text(PROC_TRAY_X_R - 150, plan_sy(PROC_TRAY_YD_NEAR) + 12,
        "PROC TRAY NEAR RIM (Yd = 80)", ha="right", va="bottom",
        fontsize=4.0, color=C_TRAY_EC, zorder=10, **FONT)

# ── Widened walkway section (EP/BAT zone, 500mm) ───────────────────────────
ax2.add_patch(mpatches.FancyBboxPatch(
    (WALKWAY_NEAR_WIDE_X_L, plan_sy(WALKWAY_W)),
    WALKWAY_NEAR_WIDE_X_R - WALKWAY_NEAR_WIDE_X_L,
    plan_sy(WALKWAY_NEAR_WIDE_W) - plan_sy(WALKWAY_W),
    boxstyle="square,pad=0", fc="#E8FFE8", ec="#66AA66",
    lw=1.0, ls="--", alpha=0.4, zorder=2))
ax2.text((WALKWAY_NEAR_WIDE_X_L + WALKWAY_NEAR_WIDE_X_R) / 2,
        plan_sy((WALKWAY_W + WALKWAY_NEAR_WIDE_W) / 2),
        f"WIDENED TO {WALKWAY_NEAR_WIDE_W}mm", ha="center", va="center",
        fontsize=4, color="#448844", fontweight="bold", zorder=10, **FONT)

# ── Evap cooler transport stowage ghost (plan view) ───────────────────────
plan_block(EVAP_STOW_X, EVAP_STOW_X + EVAP_W, 0, EVAP_D,
           "EVAP COOLER\n(TRANSPORT ONLY)", C_EVAP,
           ls="--", alpha=0.25, lw=1.0, zorder=3,
           label_fs=4, label_color="#666666")

# ── Depth dimension lines ───────────────────────────────────────────────────
_dim_items = [
    (EP_X + EP_W * 0.75, EP_DEPTH_YD, f"{EP_DEPTH_YD}mm", C_ELEC),
    (BA_X + BA_W * 0.75, BA_DEPTH_YD, f"{BA_DEPTH_YD}mm", C_BATT),
]
for _dx_mm, _yd_max, _dlabel, _dcolor in _dim_items:
    draw_dim_v(ax2, _dx_mm, plan_sy(0), plan_sy(_yd_max),
               _dlabel, offset=30, fs=4.5, color=_dcolor,
               right=False, font=FONT)

# ── Yd scale marks (right side = low X with inverted axis) ─────────────────
_yd_scale_x = -60
for _yd_val in range(0, 601, 100):
    _y = plan_sy(_yd_val)
    ax2.plot([_yd_scale_x - 12, _yd_scale_x + 12], [_y, _y],
            color=C_DIM, lw=0.4, zorder=10)
    ax2.text(_yd_scale_x - 24, _y, f"{_yd_val}",
            ha="left", va="center", fontsize=4.0, color=C_DIM,
            zorder=10, **FONT)
ax2.text(_yd_scale_x - 24, plan_sy(300) + 75,
        "Yd (mm)\n↑ INTO CONTAINER", ha="left", va="bottom",
        fontsize=4, color=C_DIM, fontweight="bold", zorder=10, **FONT)

# ── Section title ───────────────────────────────────────────────────────────
_plan_title_y = 1125
ax2.text(C_LEN / 2, _plan_title_y,
        "PLAN VIEW — NEAR WALKWAY ACCESS ANALYSIS",
        ha="center", va="bottom", fontsize=9, color=C_OUT,
        fontweight="bold", zorder=10, **FONT)
ax2.text(C_LEN / 2, _plan_title_y - 36,
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
            height=0.045 * FIG_H_ELEV / FIG_H_PLAN)

# ── Save ────────────────────────────────────────────────────────────────────
os.makedirs(DIAGRAMS_DIR, exist_ok=True)
out = os.path.join(DIAGRAMS_DIR, "pinhole-wall-elevation.png")
fig.savefig(out, dpi=150, facecolor="white", edgecolor="none")
plt.close(fig)
print(f"Pinhole wall elevation → {out}")
