#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_reorg_proposal.py — Proposed walkway reorganization diagram.

Shows the pinhole wall interior elevation and plan view AFTER the proposed
equipment relocation:
  - Evap cooler moved external (duct penetration only)
  - EP raised to Z=1600-2200
  - Slim batteries (120mm depth)
  - Pump manifold + filter unit relocated to IBC zone (X=4650-5700)
  - Tray sump moved to near-pinhole/IBC corner (X=4550)
  - Spray bar feed at walkway level (Z=75)
  - Walkway widened to 500mm at X=1600-2310 only
  - Corner triangle at right walkway junction

Output: diagrams/reorg-proposal.png
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
    EVAP_W, EVAP_H, EVAP_D,
    EP_X, EP_W,
    BA_X, BA_W,
    PUMP_X, PUMP_W,
    FSKID_X, FSKID_W,
    SHELF_X_L, SHELF_X_R, SHELF_H, SHELF_T, SHELF_HANGER_N,
    SHELF_YD_NEAR, SHELF_DEPTH,
    WALKWAY_H, WALKWAY_GRATE_T, WALKWAY_W,
    WALKWAY_BRACKET_H, WALKWAY_BRACKET_T,
    CONTAINER_RIB_SPACING,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_DRAIN_X,
    PROC_TRAY_SUMP_W, PROC_TRAY_SUMP_D, PROC_TRAY_SUMP_Z, PROC_TRAY_RIM,
    PROC_TRAY_YD_NEAR, PROC_TRAY_D,
    RAIL_OFF, ZONE_R_START,
    IBC_COL_X, IBC_W,
    C_OUT, C_CL, C_DIM,
    C_ALUM, C_STEEL, C_EVAP, C_ELEC, C_BATT, C_PUMP,
    C_PINHOLE_EQ, C_WALL,
    DIAGRAMS_DIR,
)
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_cl, draw_notes
from tbs_title_block import title_block

EVAP_X = 930  # old evap position (removed in rev7 — shown ghosted)

# ── Proposed positions ─────────────────────────────────────────────────────

# EP raised
EP_Z_LO_NEW = 1600
EP_Z_HI_NEW = 2200
EP_DEPTH_YD = 160

# Slim batteries
BA_Z_LO_NEW = 100
BA_Z_HI_NEW = 600
BA_DEPTH_YD_NEW = 120

# IBC plumbing corridor (context only — equipment now on panel)
CORRIDOR_YD_NEAR = 1046
CORRIDOR_YD_FAR = 1316
CORRIDOR_W = CORRIDOR_YD_FAR - CORRIDOR_YD_NEAR  # 270mm

# Equipment panel in IBC plumbing corridor
# Panel spans across corridor (Yd direction), perpendicular to pinhole wall.
# Panel face visible from the open end (lower X = accessible side).
PANEL_T = 18         # plywood thickness (mm) — along X in plan view
PANEL_X = 5000       # panel X position — close to walkway for access
PANEL_DEPTH_MAX = 130  # max equipment protrusion from panel face (along X)

# In plan view the panel is a thin strip running Yd = corridor near to far
PANEL_YD_NEAR = CORRIDOR_YD_NEAR   # 1046 — near IBC face
PANEL_YD_FAR = CORRIDOR_YD_FAR     # 1316 — far IBC face
PANEL_YD_SPAN = PANEL_YD_FAR - PANEL_YD_NEAR  # 270mm

# Equipment footprints in plan view (protrude from panel toward open end = lower X)
# Pumps and filters are stacked vertically (Z), so plan view shows single footprints.
# Pump zone: 127mm wide in Yd, 100mm deep in X
PM_YD_NEAR = PANEL_YD_NEAR         # 1046
PM_YD_FAR = PM_YD_NEAR + 127       # 1173
PM_DEPTH_X = 100                    # protrusion from panel face

# Filter zone: 130mm wide in Yd (single housing OD — 3 stacked vertically)
FILT_YD_NEAR = PM_YD_FAR + 13      # 1186 — small gap after pumps
FILT_YD_FAR = FILT_YD_NEAR + 130   # 1316
FILT_DEPTH_X = 130                  # housing OD = protrusion

# Legacy elevation constants (used by ghost blocks and notes)
FILT_Z_LO_NEW = 300
FILT_Z_HI_NEW = 830
PM_Z_LO_NEW = 280
PM_Z_HI_NEW = 1160

# IBC near column (for plan view context)
IBC_NEAR_YD_START = 30    # BLUE_IBC_Y
IBC_NEAR_YD_END = 1046    # = 30 + IBC_D
IBC_FAR_YD_START = 1316
IBC_FAR_YD_END = 2332     # = 1316 + IBC_D

# Tray sump relocated to near-pinhole/IBC corner
SUMP_X_NEW = 4550
SUMP_YD = PROC_TRAY_YD_NEAR  # 80mm

# Duct penetration for external evap cooler
DUCT_X = 1000
DUCT_Z = 1020
DUCT_DIAM = 200

# Walkway widening zone
WK_WIDE_X_L = 1600
WK_WIDE_X_R = 2310
WK_WIDE_W = 500

# Corner triangle
CORNER_X_L = 4329
CORNER_X_R = 4650

# Spray bar feed pipe
SPRAY_FEED_Z = 75

# Colors
C_BLUE   = "#2979B8"
C_BROWN  = "#8B5E3C"
C_FILTER = "#4A90D9"
C_FSKID  = "#B0A898"
C_SHELF  = "#C8B06A"
C_TRUNKING = "#808080"
C_TRAY   = "#C8D8E8"
C_TRAY_EC = "#5A8AAF"
C_GHOST  = "#D0D0D0"
C_GHOST_EC = "#AAAAAA"
C_NEW    = "#22AA44"
C_DUCT   = "#CC8844"
C_RELOCATED = "#66BB66"
C_WIDENED = "#E8F5E8"
C_PLY    = "#D4C8A0"
C_PLY_EC = "#A09060"

# Walkway X range (near walkway = pinhole wall side)
WK_X_L = PROC_TRAY_X_L + WALKWAY_W   # 470mm
WK_X_R = PROC_TRAY_X_R               # 4629mm

# Cable trunking
TK_H = 25
TK_Z = C_HGT - TK_H  # 2363mm

# Processing tray
TRAY_FLOOR_Z = PROC_TRAY_SUMP_Z   # 20mm
TRAY_RIM_TOP = TRAY_FLOOR_Z + PROC_TRAY_RIM  # 70mm

# ── Shurflo 2088 pump dimensions ───────────────────────────────────────────
PUMP_BODY_W = 127   # body width incl. port threads (mm)
PUMP_BODY_H = 218   # body height (mm)
PUMP_BODY_D = 100   # body depth (mm) — approximate

# ── Filter housing dimensions ──────────────────────────────────────────────
FILT_BB_OD = 130    # housing OD incl. bracket (mm)
FILT_BB_H = 530     # housing total height (mm)
FILT_HEAD_H = 70    # head height (mm)

# ── Scale and layout ───────────────────────────────────────────────────────
FW_IN = 26.0
FH_ELEV_IN = 12.0
FH_PLAN_IN = 5.0
FH_TOTAL_IN = FH_ELEV_IN + FH_PLAN_IN

# ── Figure setup — 3 panels ───────────────────────────────────────────────
# Elevation (top-left, ~78% width), Detail (top-right, ~22%), Plan (bottom full)
PLAN_FRAC = FH_PLAN_IN / FH_TOTAL_IN
ELEV_FRAC = FH_ELEV_IN / FH_TOTAL_IN
DETAIL_W_FRAC = 0.22
ELEV_W_FRAC = 1.0 - DETAIL_W_FRAC

# Elevation axis limits (mm)
ELEV_XL, ELEV_XR = -750, 5310
ELEV_ZB, ELEV_ZT = -750, 2840

def sx(x_mm):
    """Mirrored X for elevation — works in both ax (cropped) and ax2 (full width)."""
    return C_LEN - x_mm

def sz(z_mm):
    return z_mm

fig = plt.figure(figsize=(FW_IN, FH_TOTAL_IN), dpi=150)

ax = fig.add_axes([0, PLAN_FRAC, ELEV_W_FRAC, ELEV_FRAC])
ax.set_xlim(ELEV_XL, ELEV_XR)
ax.set_ylim(ELEV_ZB, ELEV_ZT)
ax.set_aspect("equal")
ax.axis("off")

ax3 = fig.add_axes([ELEV_W_FRAC, PLAN_FRAC, DETAIL_W_FRAC, ELEV_FRAC])
ax3.set_aspect("equal")
ax3.axis("off")

# Plan view: Yd reversed via subtraction (0=top); aspect auto ("NOT TO SCALE IN Yd")
PLAN_YD_TOP = 1750

def plan_sy(yd_mm):
    return PLAN_YD_TOP - yd_mm

def plan_sx(x_mm):
    return C_LEN - x_mm

ax2 = fig.add_axes([0, 0, 1, PLAN_FRAC])
ax2.set_xlim(-750, 7020)
ax2.set_ylim(0, 2750)
ax2.set_aspect("auto")
ax2.axis("off")

FONT = {"fontfamily": "monospace"}


def equip_block(axes, x_mm, z_mm, w_mm, h_mm, label, fc, *,
                ec=C_OUT, lw=1.0, zorder=5, ls="-", alpha=0.85,
                label_fs=5.5, label_color=C_OUT, sz_fn=sz):
    x_draw = sx(x_mm + w_mm)
    w_draw = sx(x_mm) - sx(x_mm + w_mm)
    rect = mpatches.FancyBboxPatch(
        (x_draw, sz_fn(z_mm)), w_draw, h_mm if sz_fn == sz else (sz_fn(z_mm + h_mm) - sz_fn(z_mm)),
        boxstyle="square,pad=0", facecolor=fc, edgecolor=ec,
        linewidth=lw, linestyle=ls, alpha=alpha, zorder=zorder)
    axes.add_patch(rect)
    if label:
        cx = sx(x_mm + w_mm / 2)
        if sz_fn == sz:
            cz = sz_fn(z_mm + h_mm / 2)
        else:
            cz = sz_fn(z_mm) + (sz_fn(z_mm + h_mm) - sz_fn(z_mm)) / 2
        axes.text(cx, cz, label, ha="center", va="center",
                fontsize=label_fs, color=label_color, zorder=zorder + 1,
                **FONT)


def equip_block_elev(x_mm, z_mm, w_mm, h_mm, label, fc, **kwargs):
    equip_block(ax, x_mm, z_mm, w_mm, h_mm, label, fc, sz_fn=sz, **kwargs)


# ═══════════════════════════════════════════════════════════════════════════
# ELEVATION VIEW — PROPOSED LAYOUT
# ═══════════════════════════════════════════════════════════════════════════

# ── 1. Container outline ──────────────────────────────────────────────────
wall_left = sx(C_LEN)
wall_right = sx(0)
wall_w = wall_right - wall_left
ax.add_patch(mpatches.Rectangle(
    (wall_left, sz(0)), wall_w, C_HGT,
    facecolor="white", edgecolor=C_OUT, linewidth=2.0, zorder=1))

ax.plot([wall_left, wall_right], [sz(0), sz(0)], color=C_OUT, lw=2.5, zorder=2)
ax.plot([wall_left, wall_right], [sz(C_HGT), sz(C_HGT)], color=C_OUT, lw=2.0, zorder=2)
ax.plot([wall_left, wall_left], [sz(0), sz(C_HGT)], color=C_OUT, lw=2.0, zorder=2)
ax.plot([wall_right, wall_right], [sz(0), sz(C_HGT)], color=C_OUT, lw=2.0, zorder=2)

# Corrugation ribs
rib_x = CONTAINER_RIB_SPACING
while rib_x < C_LEN:
    ax.plot([sx(rib_x), sx(rib_x)], [sz(0), sz(C_HGT)],
            color="#D0D0D0", lw=0.3, ls="--", zorder=1)
    rib_x += CONTAINER_RIB_SPACING

# ── 2. Cable trunking ─────────────────────────────────────────────────────
equip_block_elev(0, TK_Z, C_LEN, TK_H, "", C_TRUNKING,
                 lw=0.5, zorder=3, alpha=0.5, label_fs=4)
ax.text(sx(C_LEN / 2), sz(TK_Z + TK_H / 2), "CABLE TRUNKING",
        ha="center", va="center", fontsize=4, color="white", zorder=4, **FONT)

# ── 3. Walkway deck ───────────────────────────────────────────────────────
deck_z_bot = WALKWAY_H - WALKWAY_GRATE_T  # 75mm

# Standard width walkway sections
equip_block_elev(WK_X_L, deck_z_bot, WK_X_R - WK_X_L, WALKWAY_GRATE_T,
                 "", C_STEEL, lw=0.6, zorder=4, alpha=0.4)
for gx in range(int(WK_X_L), int(WK_X_R), 80):
    ax.plot([sx(gx), sx(gx + 40)], [sz(deck_z_bot), sz(WALKWAY_H)],
            color=C_STEEL, lw=0.2, zorder=4, alpha=0.3)

ax.text(sx((WK_X_L + WK_X_R) * 0.6), sz(WALKWAY_H + 5),
        "NEAR WALKWAY DECK (Z=100mm)", ha="center", va="bottom",
        fontsize=4.5, color=C_DIM, zorder=10, **FONT)

# Walkway brackets
bx = WK_X_L
while bx <= WK_X_R:
    nearest_rib = round(bx / CONTAINER_RIB_SPACING) * CONTAINER_RIB_SPACING
    if WK_X_L <= nearest_rib <= WK_X_R:
        bw = WALKWAY_BRACKET_T
        bh = deck_z_bot
        equip_block_elev(nearest_rib - bw / 2, 0, bw, bh,
                         "", C_STEEL, ec=C_OUT, lw=0.5, zorder=3, alpha=0.6)
    bx += CONTAINER_RIB_SPACING

# ── 3a. Processing tray ───────────────────────────────────────────────────
equip_block_elev(PROC_TRAY_X_L, 0, PROC_TRAY_X_R - PROC_TRAY_X_L, TRAY_RIM_TOP,
                 "", C_TRAY, ec=C_TRAY_EC, lw=0.6, zorder=2.5, alpha=0.35)
ax.plot([sx(PROC_TRAY_X_L), sx(PROC_TRAY_X_R)],
        [sz(TRAY_FLOOR_Z), sz(TRAY_FLOOR_Z)],
        color=C_TRAY_EC, lw=0.6, zorder=2.8)
ax.plot([sx(PROC_TRAY_X_L), sx(PROC_TRAY_X_R)],
        [sz(TRAY_RIM_TOP), sz(TRAY_RIM_TOP)],
        color=C_TRAY_EC, lw=0.8, zorder=2.8)

# ── 4. GHOSTED: Former equipment positions (removed/relocated) ────────────
# Evap cooler ghost
equip_block_elev(EVAP_X, RAIL_OFF, EVAP_W, EVAP_H,
                 "EVAP COOLER\n(REMOVED —\nEXTERNAL)", C_GHOST,
                 ec=C_GHOST_EC, lw=0.8, ls="--", alpha=0.3,
                 label_fs=4.5, label_color="#999")

# Old EP position ghost
equip_block_elev(EP_X, 900, EP_W, 600,
                 "", C_GHOST,
                 ec=C_GHOST_EC, lw=0.5, ls=":", alpha=0.15,
                 label_fs=4.0, label_color="#BBB")

# Old pump manifold ghost
equip_block_elev(PUMP_X - 33, 235, 565, 546,
                 "PUMP MANIFOLD\n(RELOCATED →\nIBC ZONE)", C_GHOST,
                 ec=C_GHOST_EC, lw=0.8, ls="--", alpha=0.3,
                 label_fs=4.5, label_color="#999")

# Old filter unit ghost
equip_block_elev(FSKID_X, 1410, FSKID_W, 600,
                 "FILTER UNIT\n(RELOCATED →\nIBC ZONE)", C_GHOST,
                 ec=C_GHOST_EC, lw=0.8, ls="--", alpha=0.3,
                 label_fs=4.5, label_color="#999")

# ── 5. NEW: Relocated/modified equipment ──────────────────────────────────

# EP raised (green highlight border for "new position")
equip_block_elev(EP_X, EP_Z_LO_NEW, EP_W, EP_Z_HI_NEW - EP_Z_LO_NEW,
                 "ELECTRICAL\nPANEL\n(RAISED)", C_ELEC,
                 ec=C_NEW, lw=2.0, alpha=0.85, label_fs=5)
# Arrow from old to new position
ax.annotate("", xy=(sx(EP_X + EP_W / 2), sz(EP_Z_LO_NEW)),
            xytext=(sx(EP_X + EP_W / 2), sz(1500)),
            arrowprops=dict(arrowstyle="-|>", color=C_NEW, lw=1.5),
            zorder=10)

# Battery (slim) — same X, reduced depth shown in elevation
equip_block_elev(BA_X, BA_Z_LO_NEW, BA_W, BA_Z_HI_NEW - BA_Z_LO_NEW,
                 "BATTERY\nBANK\n(SLIM 120mm)", C_BATT,
                 ec=C_NEW, lw=2.0, alpha=0.85, label_fs=5)

# ── 6. Duct penetration (evap cooler) ────────────────────────────────────
duct_r = DUCT_DIAM / 2
circ = plt.Circle((sx(DUCT_X), sz(DUCT_Z)), duct_r,
                   facecolor=C_DUCT, edgecolor=C_NEW, linewidth=2.0,
                   alpha=0.7, zorder=7)
ax.add_patch(circ)
ax.text(sx(DUCT_X), sz(DUCT_Z), "DUCT\n200Ø", ha="center", va="center",
        fontsize=4, color=C_OUT, fontweight="bold", zorder=8, **FONT)
leader(ax, sx(DUCT_X) + duct_r + 15, sz(DUCT_Z),
       sx(DUCT_X) + 210, sz(DUCT_Z) + 120,
       "EVAP COOLER DUCT\nTO EXTERNAL UNIT\n(200mm Ø, Z=1020)\nMOTORIZED DAMPER",
       fs=4.5, color=C_NEW, font=FONT)

# ── 7. Spray bar feed pipe (walkway level) ────────────────────────────────
# Thin line at Z=75 from IBC zone leftward along pinhole wall
ax.plot([sx(IBC_COL_X), sx(WK_X_L)],
        [sz(SPRAY_FEED_Z), sz(SPRAY_FEED_Z)],
        color=C_BLUE, lw=1.5, ls="-", zorder=6, alpha=0.6)
ax.text(sx(3500), sz(SPRAY_FEED_Z) - 36,
        "BLUE SUPPLY (½\" HDPE, Z=75, BELOW GRATING)", ha="center", va="top",
        fontsize=4.0, color=C_BLUE, zorder=10, **FONT)

# ── 8. Tray sump marker (new position) ────────────────────────────────────
ax.add_patch(mpatches.Rectangle(
    (sx(SUMP_X_NEW + PROC_TRAY_SUMP_W / 2), sz(0)),
    PROC_TRAY_SUMP_W, PROC_TRAY_SUMP_Z,
    facecolor=C_NEW, edgecolor=C_NEW, linewidth=1.0, alpha=0.6, zorder=6))
leader(ax, sx(SUMP_X_NEW), sz(PROC_TRAY_SUMP_Z),
       sx(SUMP_X_NEW) + 150, sz(PROC_TRAY_SUMP_Z) + 150,
       "SUMP (NEW)\nX=4550, Yd=80\nDIRECT TO P-04",
       fs=4, color=C_NEW, font=FONT)

# ── 9. IBC zone boundary ─────────────────────────────────────────────────
ax.plot([sx(ZONE_R_START), sx(ZONE_R_START)], [sz(0), sz(C_HGT)],
        color="#AA6600", lw=1.5, ls="-.", zorder=3, alpha=0.5)
ax.text(sx(ZONE_R_START) + 24, sz(C_HGT - 100),
        "IBC ZONE →", ha="left", va="top",
        fontsize=5, color="#AA6600", fontweight="bold", zorder=10, **FONT)

# ── 10. Chemistry shelf (unchanged — ghost, behind walkway) ──────────────
C_SHELF_DK = "#8A7A3A"
equip_block_elev(SHELF_X_L, SHELF_H - SHELF_T, SHELF_X_R - SHELF_X_L, SHELF_T,
                 "", C_SHELF_DK, ls="--", alpha=0.5, lw=1.0, zorder=4)
ax.text(sx((SHELF_X_L + SHELF_X_R) / 2), sz(SHELF_H - SHELF_T + 60),
        "CHEM SHELF (Yd=300)", ha="center", va="top",
        fontsize=4, color=C_SHELF_DK, zorder=10, **FONT)

# ── 11. Pinhole position ─────────────────────────────────────────────────
draw_cl(ax, sx(PH_X) - 45, sx(PH_X) + 45, sz(PH_H),
        color=C_CL, lw=0.5, zorder=8)
ax.plot(sx(PH_X), sz(PH_H), marker="+", color=C_CL, ms=8, mew=1.0, zorder=9)
ax.text(sx(PH_X), sz(PH_H) + 45, f"PINHOLE\nX={PH_X}", ha="center",
        va="bottom", fontsize=4, color=C_CL, zorder=10, **FONT)

# ── 12. Dimension lines for key positions ─────────────────────────────────
# EP height
draw_dim_v(ax, sx(EP_X - 40), sz(EP_Z_LO_NEW), sz(EP_Z_HI_NEW),
           "600", offset=45, fs=4.5, color=C_NEW, right=False, font=FONT)

# Battery height
draw_dim_v(ax, sx(BA_X + BA_W + 40), sz(BA_Z_LO_NEW), sz(BA_Z_HI_NEW),
           "500", offset=45, fs=4.5, color=C_NEW, right=True, font=FONT)

# Duct Z dimension
draw_dim_v(ax, sx(DUCT_X - 200), sz(C_HGT), sz(DUCT_Z - duct_r),
           f"{C_HGT - DUCT_Z + int(duct_r)}", offset=30, fs=3.5,
           color=C_DIM, right=False, font=FONT)

# ── 13. Elevation notes ──────────────────────────────────────────────────
notes = [
    "PROPOSED CHANGES",
    "1. Evap cooler → EXTERNAL. 200mm duct at X=1000, Z=1020 with motorized damper.",
    "2. EP raised from Z=900–1500 to Z=1600–2200. Same X position, same wiring.",
    "3. Battery → slim profile (120mm depth, was 220mm). Same X position.",
    f"4. Pump manifold + ACC-01 + 3× filter housings → panel in IBC corridor (Yd={PANEL_YD_NEAR}).",
    "5. Panel: 18mm ply, 780×1140mm, back against near IBC. Filters sump-down.",
    "6. Tray sump → X=4550 (near-pinhole/IBC corner). Direct P-04 connection.",
    "7. Blue supply feed at Z=75 (below walkway grating).",
    "8. Walkway widened to 500mm at X=1600–2310 only (see plan view).",
]
draw_notes(ax, notes, -110, 1580, spacing=75,
           fs=7, width=2240, color=C_DIM, title_color=C_NEW, font=FONT)


# ═══════════════════════════════════════════════════════════════════════════
# DETAIL — EQUIPMENT PANEL (FRONT ELEVATION)
# ═══════════════════════════════════════════════════════════════════════════
# Simplified front elevation of the 18mm panel at Yd=600, showing all
# relocated equipment.  Matches generate_panel_layout.py.

# Detail panel axis limits (mm)
D_XL, D_XR = -60, 860
D_ZB, D_ZT = -250, 1700

# Panel-relative layout (mm) — mirrors generate_panel_layout.py
D_PUMP_GAP = 40
D_PUMP_COL = 100
D_P01_Z = 280
D_P02_Z = D_P01_Z + PUMP_BODY_H + D_PUMP_GAP
D_P04_Z = D_P02_Z + PUMP_BODY_H + D_PUMP_GAP
D_ACC_OD = 127
D_ACC_Z = D_P04_Z + PUMP_BODY_H + D_PUMP_GAP + D_ACC_OD // 2

D_FILT_GAP = 35
D_FILT_X0 = 280
D_F01_X = D_FILT_X0 + FILT_BB_OD // 2
D_F02_X = D_F01_X + FILT_BB_OD + D_FILT_GAP
D_F03_X = D_F02_X + FILT_BB_OD + D_FILT_GAP
D_FILT_Z_BOT = 300

D_PANEL_MARGIN = 40
D_PANEL_X_R = D_F03_X + FILT_BB_OD // 2 + D_PANEL_MARGIN
D_PANEL_Z_BOT = 150
D_PANEL_Z_TOP = D_ACC_Z + D_ACC_OD // 2 + D_PANEL_MARGIN + 40
D_PANEL_W = D_PANEL_X_R
D_PANEL_H = D_PANEL_Z_TOP - D_PANEL_Z_BOT

def dsx(x_mm):
    return x_mm

def dsz(z_mm):
    return z_mm

ax3.set_xlim(D_XL, D_XR)
ax3.set_ylim(D_ZB, D_ZT)

# ── Detail border ─────────────────────────────────────────────────────────
ax3.add_patch(mpatches.Rectangle(
    (D_XL + 24, D_ZB + 48), (D_XR - D_XL) - 48, (D_ZT - D_ZB) - 96,
    fc="none", ec=C_DIM, lw=1.0, zorder=1))

# ── Detail title ──────────────────────────────────────────────────────────
ax3.text((D_XL + D_XR) / 2, D_ZT - 48,
        "DETAIL — EQUIPMENT PANEL",
        ha="center", va="top", fontsize=7, color=C_NEW,
        fontweight="bold", zorder=10, **FONT)
ax3.text((D_XL + D_XR) / 2, D_ZT - 128,
        f"FRONT ELEVATION\n18mm PLY AT Yd={PANEL_YD_NEAR}\n{D_PANEL_W}mm \u00d7 {D_PANEL_H}mm\nSCALE ~1:160",
        ha="center", va="top", fontsize=4, color=C_DIM,
        zorder=10, **FONT)

# ── Panel outline (plywood) ──────────────────────────────────────────────
ax3.add_patch(mpatches.Rectangle(
    (dsx(0), dsz(D_PANEL_Z_BOT)), D_PANEL_W, D_PANEL_H,
    fc=C_PLY, ec=C_PLY_EC, lw=2.0, zorder=3, alpha=0.5))

# ── Floor line ────────────────────────────────────────────────────────────
ax3.plot([dsx(-30), dsx(D_PANEL_X_R + 30)], [dsz(0), dsz(0)],
        color=C_OUT, lw=1.5, zorder=3)

# ── 3x Pump bodies ───────────────────────────────────────────────────────
d_pump_specs = [
    ("P-01", "BLUE",  D_P01_Z, C_BLUE),
    ("P-02", "BROWN", D_P02_Z, C_BROWN),
    ("P-04", "DRAIN", D_P04_Z, "#888888"),
]

for pname, pdesc, pz, pcolor in d_pump_specs:
    ax3.add_patch(mpatches.Rectangle(
        (dsx(D_PUMP_COL - PUMP_BODY_W / 2), dsz(pz)),
        PUMP_BODY_W, PUMP_BODY_H,
        fc="#E0D0C0", ec="#806040", lw=1.0, zorder=6))
    ax3.text(dsx(D_PUMP_COL), dsz(pz + PUMP_BODY_H / 2 + 15),
            pname, ha="center", va="center",
            fontsize=5, color=pcolor, fontweight="bold", zorder=8, **FONT)
    ax3.text(dsx(D_PUMP_COL), dsz(pz + PUMP_BODY_H / 2 - 20),
            pdesc, ha="center", va="center",
            fontsize=4, color=pcolor, zorder=8, **FONT)

# ── ACC-01 (end-on circle) ───────────────────────────────────────────────
ax3.add_patch(plt.Circle(
    (dsx(D_PUMP_COL), dsz(D_ACC_Z)), D_ACC_OD / 2,
    fc="#5A9ACC", ec=C_BLUE, lw=1.0, zorder=6, alpha=0.7))
ax3.text(dsx(D_PUMP_COL), dsz(D_ACC_Z),
        "ACC-01", ha="center", va="center",
        fontsize=4, color="white", fontweight="bold", zorder=8, **FONT)

# ── 3x Filter housings ──────────────────────────────────────────────────
d_filt_specs = [
    ("F-01", D_F01_X),
    ("F-02", D_F02_X),
    ("F-03", D_F03_X),
]

for fname, fx_c in d_filt_specs:
    ax3.add_patch(mpatches.Rectangle(
        (dsx(fx_c - FILT_BB_OD / 2), dsz(D_FILT_Z_BOT)),
        FILT_BB_OD, FILT_BB_H,
        fc=C_FILTER, ec=C_OUT, lw=1.0, zorder=6, alpha=0.6))
    ax3.add_patch(mpatches.Rectangle(
        (dsx(fx_c - FILT_BB_OD / 2), dsz(D_FILT_Z_BOT + FILT_BB_H - FILT_HEAD_H)),
        FILT_BB_OD, FILT_HEAD_H,
        fc="#3A70B0", ec=C_OUT, lw=0.6, zorder=6, alpha=0.7))
    ax3.text(dsx(fx_c), dsz(D_FILT_Z_BOT + FILT_BB_H / 2),
            fname, ha="center", va="center",
            fontsize=4, color="white", fontweight="bold", zorder=8, **FONT)

# ── Zone labels ──────────────────────────────────────────────────────────
ax3.text(dsx(D_PUMP_COL), dsz(D_P01_Z - 30),
        "PUMP\nMANIFOLD", ha="center", va="top",
        fontsize=4.0, color="#806040", fontweight="bold", zorder=10, **FONT)
ax3.text(dsx(D_F02_X), dsz(D_FILT_Z_BOT + FILT_BB_H + 25),
        "FILTER SKID (\u00d73)", ha="center", va="bottom",
        fontsize=4.0, color=C_FILTER, fontweight="bold", zorder=10, **FONT)
ax3.text(dsx(D_F02_X), dsz(D_FILT_Z_BOT - 15),
        "\u2193 SUMP DOWN", ha="center", va="top",
        fontsize=4, color=C_FILTER, zorder=10, **FONT)

# ── Key specs note ───────────────────────────────────────────────────────
d_notes = [
    "EQUIPMENT PANEL",
    f"18mm marine ply at Yd={PANEL_YD_NEAR}",
    "3\u00d7 Shurflo 2088 (12V, 3.5 GPM)",
    "ACC-01: 0.75L accum., 1/2\" MNPT",
    "3\u00d7 4.5\"\u00d720\" housings, sump-down",
    f"Max depth from panel: {max(PUMP_BODY_D, FILT_BB_OD)}mm",
]
_dnx = 8
_dny = dsz(0) - 32
for i, line in enumerate(d_notes):
    _fs = 4 if i == 0 else 3.5
    _fc = C_NEW if i == 0 else C_DIM
    _fw = "bold" if i == 0 else "normal"
    ax3.text(_dnx, _dny - i * 26, line,
            fontsize=_fs, color=_fc, fontweight=_fw, zorder=10, **FONT)



# ═══════════════════════════════════════════════════════════════════════════
# PLAN VIEW — PROPOSED WALKWAY ACCESS
# ═══════════════════════════════════════════════════════════════════════════

# plan_sx and plan_sy defined above with axes setup


def plan_block(xl, xr, yd_near, yd_far, label, fc, *,
               ec=C_OUT, lw=1.0, ls="-", alpha=0.75,
               label_fs=4.5, label_color=C_OUT, zorder=5):
    x1, x2 = plan_sx(xl), plan_sx(xr)
    y1, y2 = plan_sy(yd_near), plan_sy(yd_far)
    x_draw = min(x1, x2)
    w_draw = abs(x2 - x1)
    y_draw = min(y1, y2)
    h_draw = abs(y2 - y1)
    ax2.add_patch(mpatches.FancyBboxPatch(
        (x_draw, y_draw), w_draw, h_draw,
        boxstyle="square,pad=0", fc=fc, ec=ec,
        lw=lw, ls=ls, alpha=alpha, zorder=zorder))
    if label:
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        ax2.text(cx, cy, label, ha="center", va="center",
                fontsize=label_fs, color=label_color,
                zorder=zorder + 1, **FONT)


# ── Container wall line (Yd=0) ─────────────────────────────────────────────
ax2.plot([plan_sx(0), plan_sx(C_LEN)], [plan_sy(0), plan_sy(0)],
        color=C_OUT, lw=2.5, zorder=2)
ax2.text(plan_sx(C_LEN / 2), plan_sy(0) + 66,
        "PINHOLE WALL (Yd = 0)", ha="center", va="bottom",
        fontsize=5, color=C_OUT, fontweight="bold", zorder=10, **FONT)

# ── Walkway zones ──────────────────────────────────────────────────────────

# Standard 300mm walkway: X=470 to 1600 and X=2310 to 4329
for sec_l, sec_r in [(WK_X_L, WK_WIDE_X_L), (WK_WIDE_X_R, CORNER_X_L)]:
    wk_x1, wk_x2 = plan_sx(sec_l), plan_sx(sec_r)
    wk_y1, wk_y2 = plan_sy(0), plan_sy(WALKWAY_W)
    ax2.add_patch(mpatches.FancyBboxPatch(
        (min(wk_x1, wk_x2), min(wk_y1, wk_y2)),
        abs(wk_x2 - wk_x1), abs(wk_y2 - wk_y1),
        boxstyle="square,pad=0", fc="#F0F0F0", ec="none", alpha=0.5, zorder=1))
    for hx in range(int(sec_l), int(sec_r), 200):
        ax2.plot([plan_sx(hx), plan_sx(hx + 100)],
                [plan_sy(0), plan_sy(WALKWAY_W)],
                color="#D8D8D8", lw=0.2, zorder=1)

# Widened 500mm section: X=1600 to 2310
ww_x1, ww_x2 = plan_sx(WK_WIDE_X_L), plan_sx(WK_WIDE_X_R)
ww_y1, ww_y2 = plan_sy(0), plan_sy(WK_WIDE_W)
ax2.add_patch(mpatches.FancyBboxPatch(
    (min(ww_x1, ww_x2), min(ww_y1, ww_y2)),
    abs(ww_x2 - ww_x1), abs(ww_y2 - ww_y1),
    boxstyle="square,pad=0", fc=C_WIDENED, ec=C_NEW,
    lw=1.5, alpha=0.6, zorder=1))
for hx in range(int(WK_WIDE_X_L), int(WK_WIDE_X_R), 200):
    ax2.plot([plan_sx(hx), plan_sx(hx + 100)],
            [plan_sy(0), plan_sy(WK_WIDE_W)],
            color="#B8D8B8", lw=0.2, zorder=1)
ax2.text(plan_sx((WK_WIDE_X_L + WK_WIDE_X_R) / 2), plan_sy(WK_WIDE_W / 2),
        "WIDENED\n500mm", ha="center", va="center",
        fontsize=5, color=C_NEW, fontweight="bold", zorder=6, **FONT)

# Corner triangle: X=4329 to 4650
tri_pts = [
    (plan_sx(CORNER_X_R), plan_sy(0)),       # IBC-side corner, wall
    (plan_sx(CORNER_X_L), plan_sy(0)),       # right walkway junction, wall
    (plan_sx(CORNER_X_L), plan_sy(WALKWAY_W)),  # right walkway junction, outer edge
    (plan_sx(CORNER_X_R), plan_sy(0)),       # back to start
]
tri_x = [p[0] for p in tri_pts]
tri_y = [p[1] for p in tri_pts]
ax2.fill(tri_x, tri_y, fc=C_WIDENED, ec=C_NEW, lw=1.5, alpha=0.6, zorder=1)
ax2.text(plan_sx((CORNER_X_L + CORNER_X_R) / 2),
        plan_sy(WALKWAY_W * 0.3),
        "CORNER\nTRIANGLE", ha="center", va="center",
        fontsize=4.0, color=C_NEW, fontweight="bold", zorder=6, **FONT)

# Walkway labels
ax2.text(plan_sx(900), plan_sy(WALKWAY_W / 2),
        "300mm\nWALKWAY", ha="center", va="center",
        fontsize=4.5, color="#999999", style="italic", zorder=2, **FONT)
ax2.text(plan_sx(3300), plan_sy(WALKWAY_W / 2),
        "300mm\nWALKWAY", ha="center", va="center",
        fontsize=4.5, color="#999999", style="italic", zorder=2, **FONT)

# ── Walkway outer edge (300mm standard) ─────────────────────────────────────
# Standard sections
for sec_l, sec_r in [(WK_X_L, WK_WIDE_X_L), (WK_WIDE_X_R, CORNER_X_L)]:
    ax2.plot([plan_sx(sec_l), plan_sx(sec_r)],
            [plan_sy(WALKWAY_W), plan_sy(WALKWAY_W)],
            color=C_OUT, lw=1.0, ls="--", zorder=2)

# Widened section outer edge (500mm)
ax2.plot([plan_sx(WK_WIDE_X_L), plan_sx(WK_WIDE_X_R)],
        [plan_sy(WK_WIDE_W), plan_sy(WK_WIDE_W)],
        color=C_NEW, lw=1.5, ls="--", zorder=4)

# Transition lines (tapered)
ax2.plot([plan_sx(WK_WIDE_X_L), plan_sx(WK_WIDE_X_L)],
        [plan_sy(WALKWAY_W), plan_sy(WK_WIDE_W)],
        color=C_NEW, lw=1.0, ls="-", zorder=3)
ax2.plot([plan_sx(WK_WIDE_X_R), plan_sx(WK_WIDE_X_R)],
        [plan_sy(WALKWAY_W), plan_sy(WK_WIDE_W)],
        color=C_NEW, lw=1.0, ls="-", zorder=3)

# Full-length 300mm reference line
ax2.plot([plan_sx(0), plan_sx(C_LEN)], [plan_sy(WALKWAY_W), plan_sy(WALKWAY_W)],
        color=C_DIM, lw=0.4, ls=":", zorder=1, alpha=0.5)
ax2.text(plan_sx(50), plan_sy(WALKWAY_W) - 33,
        "STANDARD WALKWAY EDGE (Yd = 300)", ha="right", va="top",
        fontsize=4, color=C_DIM, zorder=10, **FONT)

# ── Ghosted: removed components (former positions) ─────────────────────────
ghost_comps = [
    ("EVAP\n(REMOVED)", EVAP_X, EVAP_X + EVAP_W, 0, EVAP_D),
    ("PUMP\n(RELOCATED)", PUMP_X - 33, PUMP_X - 33 + 565, 0, 100),
    ("FILTER\n(RELOCATED)", FSKID_X, FSKID_X + FSKID_W, 0, 130),
]
for name, xl, xr, yn, yf in ghost_comps:
    plan_block(xl, xr, yn, yf, name, C_GHOST,
               ec=C_GHOST_EC, lw=0.8, ls="--", alpha=0.2,
               label_fs=4.0, label_color="#BBB", zorder=2)

# ── New positions: components that remain on pinhole wall ──────────────────
# EP (raised — same X/Yd footprint, just higher Z)
plan_block(EP_X, EP_X + EP_W, 0, EP_DEPTH_YD,
           "ELECTRICAL\nPANEL (RAISED)", C_ELEC,
           ec=C_NEW, lw=1.5, alpha=0.75, zorder=5,
           label_fs=4, label_color=C_OUT)

# Battery (slim)
plan_block(BA_X, BA_X + BA_W, 0, BA_DEPTH_YD_NEW,
           "BATTERY\n(SLIM 120mm)", C_BATT,
           ec=C_NEW, lw=1.5, alpha=0.75, zorder=5,
           label_fs=4, label_color=C_OUT)

# Chemistry shelf (unchanged)
plan_block(SHELF_X_L, SHELF_X_R, SHELF_YD_NEAR, SHELF_YD_NEAR + SHELF_DEPTH,
           "CHEMISTRY\nSHELF", C_SHELF,
           ec=C_OUT, lw=1.0, ls="--", alpha=0.5, zorder=3,
           label_fs=4, label_color="#8A7A3A")

# ── IBC footprints (context) ───────────────────────────────────────────────
C_IBC_GHOST = "#E0D8C8"
C_IBC_EC = "#B0A898"
# Near IBC column (Blue#1/Brown#3)
plan_block(IBC_COL_X, IBC_COL_X + IBC_W,
           IBC_NEAR_YD_START, IBC_NEAR_YD_END,
           "IBC NEAR\nCOLUMN\n(Blue#1 /\nBrown#3)", C_IBC_GHOST,
           ec=C_IBC_EC, lw=0.8, alpha=0.35, zorder=2,
           label_fs=4.0, label_color="#999")
# Far IBC column (Blue#2/Waste#4)
plan_block(IBC_COL_X, IBC_COL_X + IBC_W,
           IBC_FAR_YD_START, IBC_FAR_YD_END,
           "IBC FAR\nCOLUMN\n(Blue#2 /\nWaste#4)", C_IBC_GHOST,
           ec=C_IBC_EC, lw=0.8, alpha=0.35, zorder=2,
           label_fs=4.0, label_color="#999")

# ── IBC plumbing corridor (270mm gap between columns) ─────────────────────
plan_block(IBC_COL_X, IBC_COL_X + IBC_W,
           CORRIDOR_YD_NEAR, CORRIDOR_YD_FAR,
           "", "#F8F4E8",
           ec="#CC9933", lw=1.0, ls="-.", alpha=0.3, zorder=2)
ax2.text(plan_sx(IBC_COL_X + IBC_W / 2), plan_sy((CORRIDOR_YD_NEAR + CORRIDOR_YD_FAR) / 2),
        "PLUMBING\nCORRIDOR\n(270mm)", ha="center", va="center",
        fontsize=4.0, color="#AA7722", zorder=3, **FONT)

# ── Equipment panel in IBC corridor (spans Yd, perpendicular to wall) ────
# Panel is 18mm thick in X, spanning corridor from near to far IBC face
plan_block(PANEL_X, PANEL_X + PANEL_T,
           PANEL_YD_NEAR, PANEL_YD_FAR,
           "", C_PLY,
           ec=C_PLY_EC, lw=1.5, alpha=0.7, zorder=5)

# Equipment protrudes from panel toward open end (lower X = accessible)
# Pump footprint (3 stacked vertically — plan shows single outline)
plan_block(PANEL_X - PM_DEPTH_X, PANEL_X,
           PM_YD_NEAR, PM_YD_FAR,
           "PUMPS\n×3", C_PUMP,
           ec=C_NEW, lw=1.5, alpha=0.75, zorder=6,
           label_fs=4.0, label_color=C_OUT)

# Filter footprint (3 stacked vertically — plan shows single outline)
plan_block(PANEL_X - FILT_DEPTH_X, PANEL_X,
           FILT_YD_NEAR, FILT_YD_FAR,
           "FILTER\n×3", C_FILTER,
           ec=C_NEW, lw=1.5, alpha=0.75, zorder=6,
           label_fs=4.0, label_color=C_OUT)

# Panel label
ax2.text(plan_sx(PANEL_X), plan_sy(PANEL_YD_NEAR - 30),
        "EQUIP PANEL\n(18mm PLY, SPANS CORRIDOR)", ha="center", va="bottom",
        fontsize=4.0, color=C_NEW, fontweight="bold", zorder=7, **FONT)

# ── Duct penetration in plan view ──────────────────────────────────────────
# Duct passes through the wall in the Yd direction — plan view shows a
# rectangle crossing the wall line, not a circle.
duct_plan_w = DUCT_DIAM
duct_plan_l = 99
ax2.add_patch(mpatches.Rectangle(
    (plan_sx(DUCT_X) - duct_plan_w / 2, plan_sy(0) - duct_plan_l / 2),
    duct_plan_w, duct_plan_l,
    facecolor=C_DUCT, edgecolor=C_NEW, linewidth=1.5,
    alpha=0.7, zorder=7))
ax2.text(plan_sx(DUCT_X), plan_sy(0) - duct_plan_l / 2 - 33,
        "DUCT 200Ø", ha="center", va="top",
        fontsize=4.0, color=C_NEW, fontweight="bold", zorder=8, **FONT)

# ── Spray bar feed pipe (plan view — along Yd=0 at floor level) ───────────
ax2.plot([plan_sx(IBC_COL_X), plan_sx(WK_X_L)],
        [plan_sy(5), plan_sy(5)],
        color=C_BLUE, lw=1.5, ls="-", zorder=6, alpha=0.5)
ax2.text(plan_sx(3500), plan_sy(5) + 33,
        "BLUE SUPPLY AT FLOOR (Z=75)", ha="center", va="bottom",
        fontsize=4, color=C_BLUE, zorder=10, **FONT)

# ── Tray sump (new position) ──────────────────────────────────────────────
plan_block(SUMP_X_NEW - PROC_TRAY_SUMP_W / 2,
           SUMP_X_NEW + PROC_TRAY_SUMP_W / 2,
           PROC_TRAY_YD_NEAR,
           PROC_TRAY_YD_NEAR + PROC_TRAY_SUMP_D,
           "SUMP", C_NEW,
           ec=C_NEW, lw=1.5, alpha=0.6, zorder=6,
           label_fs=4.0, label_color="white")

# Old sump ghost
plan_block(PROC_TRAY_DRAIN_X - PROC_TRAY_SUMP_W / 2,
           PROC_TRAY_DRAIN_X + PROC_TRAY_SUMP_W / 2,
           PROC_TRAY_YD_NEAR,
           PROC_TRAY_YD_NEAR + PROC_TRAY_SUMP_D,
           "", C_GHOST,
           ec=C_GHOST_EC, lw=0.5, ls="--", alpha=0.2, zorder=2)
ax2.text(plan_sx(PROC_TRAY_DRAIN_X), plan_sy(PROC_TRAY_YD_NEAR + PROC_TRAY_SUMP_D + 10),
        "OLD SUMP\n(REMOVED)", ha="center", va="top",
        fontsize=4, color="#BBB", zorder=3, **FONT)

# Arrow from old sump to new sump
ax2.annotate("", xy=(plan_sx(SUMP_X_NEW), plan_sy(PROC_TRAY_YD_NEAR + PROC_TRAY_SUMP_D / 2)),
            xytext=(plan_sx(PROC_TRAY_DRAIN_X), plan_sy(PROC_TRAY_YD_NEAR + PROC_TRAY_SUMP_D / 2)),
            arrowprops=dict(arrowstyle="-|>", color=C_NEW, lw=1.5, ls="--"),
            zorder=8)

# ── Processing tray near rim ──────────────────────────────────────────────
ax2.plot([plan_sx(PROC_TRAY_X_L), plan_sx(PROC_TRAY_X_R)],
        [plan_sy(PROC_TRAY_YD_NEAR), plan_sy(PROC_TRAY_YD_NEAR)],
        color=C_TRAY_EC, lw=0.8, ls=":", zorder=4)

# ── IBC zone boundary ────────────────────────────────────────────────────
ax2.plot([plan_sx(ZONE_R_START), plan_sx(ZONE_R_START)],
        [plan_sy(0), plan_sy(CORRIDOR_YD_FAR)],
        color="#AA6600", lw=1.5, ls="-.", zorder=3, alpha=0.5)
ax2.text(plan_sx(ZONE_R_START) + 24, plan_sy(CORRIDOR_YD_FAR - 50),
        "← IBC ZONE", ha="left", va="top",
        fontsize=4, color="#AA6600", fontweight="bold", zorder=10, **FONT)

# ── Depth dimension lines ─────────────────────────────────────────────────
dim_items = [
    (EP_X + EP_W * 0.3, EP_DEPTH_YD, f"{EP_DEPTH_YD}mm", C_ELEC),
    (BA_X + BA_W * 0.7, BA_DEPTH_YD_NEW, f"{BA_DEPTH_YD_NEW}mm", C_BATT),
]
for dx_mm, yd_max, dlabel, dcolor in dim_items:
    draw_dim_v(ax2, plan_sx(dx_mm), plan_sy(0), plan_sy(yd_max),
               dlabel, offset=30, fs=4, color=dcolor,
               right=True, font=FONT)

# ── Clearance annotations ─────────────────────────────────────────────────
# Show clearance past EP in widened section
ep_clear = WK_WIDE_W - EP_DEPTH_YD  # 340mm
ax2.annotate("", xy=(plan_sx(EP_X + EP_W / 2), plan_sy(EP_DEPTH_YD)),
            xytext=(plan_sx(EP_X + EP_W / 2), plan_sy(WK_WIDE_W)),
            arrowprops=dict(arrowstyle="<->", color=C_NEW, lw=1.0),
            zorder=10)
ax2.text(plan_sx(EP_X + EP_W / 2) - 24,
        plan_sy((EP_DEPTH_YD + WK_WIDE_W) / 2),
        f"{ep_clear}mm\nCLEAR", ha="right", va="center",
        fontsize=4.0, color=C_NEW, fontweight="bold",
        zorder=10, **FONT)

# Show clearance past battery in widened section
ba_clear = WK_WIDE_W - BA_DEPTH_YD_NEW  # 380mm
ax2.annotate("", xy=(plan_sx(BA_X + BA_W * 0.8), plan_sy(BA_DEPTH_YD_NEW)),
            xytext=(plan_sx(BA_X + BA_W * 0.8), plan_sy(WK_WIDE_W)),
            arrowprops=dict(arrowstyle="<->", color=C_NEW, lw=1.0),
            zorder=10)
ax2.text(plan_sx(BA_X + BA_W * 0.8) - 24,
        plan_sy((BA_DEPTH_YD_NEW + WK_WIDE_W) / 2),
        f"{ba_clear}mm\nCLEAR", ha="right", va="center",
        fontsize=4.0, color=C_NEW, fontweight="bold",
        zorder=10, **FONT)

# ── Yd scale marks ─────────────────────────────────────────────────────────
_yd_scale_x = plan_sx(0) + 60
for _yd_val in [0, 100, 200, 300, 500, 1046, 1316]:
    _y = plan_sy(_yd_val)
    ax2.plot([_yd_scale_x - 12, _yd_scale_x + 12], [_y, _y],
            color=C_DIM, lw=0.4, zorder=10)
    ax2.text(_yd_scale_x + 24, _y, f"{_yd_val}",
            ha="left", va="center", fontsize=4.0, color=C_DIM,
            zorder=10, **FONT)
ax2.text(_yd_scale_x + 24, plan_sy(700),
        "Yd (mm)\n↓ INTO\nCONTAINER", ha="left", va="top",
        fontsize=4, color=C_DIM, fontweight="bold", zorder=10, **FONT)

# ── Section title ──────────────────────────────────────────────────────────
_plan_title_y = 2502
ax2.text(plan_sx(C_LEN / 2), _plan_title_y,
        "PLAN VIEW — PROPOSED WALKWAY (REORGANIZED)",
        ha="center", va="bottom", fontsize=9, color=C_NEW,
        fontweight="bold", zorder=10, **FONT)
ax2.text(plan_sx(C_LEN / 2), _plan_title_y - 66,
        "GREEN BORDER = NEW/MODIFIED · GRAY DASHED = REMOVED/RELOCATED"
        " · NOT TO SCALE IN Yd",
        ha="center", va="top", fontsize=4.5, color=C_DIM,
        zorder=10, **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# TITLE BLOCK
# ═══════════════════════════════════════════════════════════════════════════
title_block(ax2, "SHEET 1 OF 1",
            drawing_title="PINHOLE WALL — PROPOSED REORGANIZATION",
            subtitle="WALKWAY ACCESS · EQUIPMENT RELOCATION · FOR REVIEW",
            scale_note="ELEV ~1:20 · PLAN Yd NOT TO SCALE"
                       " · ALL DIMS IN mm",
            doc_id="TBS-001 · Reorg Proposal",
            height=0.045 * FH_ELEV_IN / FH_PLAN_IN)

# ── Save ───────────────────────────────────────────────────────────────────
os.makedirs(DIAGRAMS_DIR, exist_ok=True)
out = os.path.join(DIAGRAMS_DIR, "reorg-proposal.png")
fig.savefig(out, dpi=150, facecolor="white", edgecolor="none")
plt.close(fig)
print(f"Reorg proposal diagram → {out}")
