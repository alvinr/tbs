#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_panel_layout.py — Equipment panel layout on pinhole wall.

Front elevation of an 18mm plywood panel at Yd=1046 (back against near
IBC column in plumbing corridor).  All relocated equipment mounted on
the panel face: 3× pumps, ACC-01, 3× separate 4.5"×10" filter housings.

Plus a cross-section strip showing panel/walkway/wall relationship.

Output: diagrams/panel-layout.png
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from tbs_constants import C_OUT, C_DIM, C_CL, C_STEEL, DIAGRAMS_DIR
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_notes, hatch_rect
from tbs_title_block import title_block

# ── Panel geometry ────────────────────────────────────────────────────────
PANEL_T      = 18    # plywood thickness (mm)
PANEL_YD     = 1046  # panel back face against near IBC column (mm from pinhole wall)
WALKWAY_W    = 300   # standard walkway width (mm)
WALKWAY_Z    = 100   # walkway grating top (mm AFF)

# Panel X position in IBC zone (spans corridor perpendicular to wall)
PANEL_WALL_X = 4800  # panel X position along container (matches EQPANEL_X)

# ── Shurflo 2088 pump dimensions ─────────────────────────────────────────
PUMP_W   = 127   # front face width (mm) — port-to-port
PUMP_H   = 218   # front face height (mm) — body length, vertical mount
PUMP_D   = 100   # depth from panel (mm)
PUMP_GAP = 40    # vertical gap between pumps (mm)

# ── Accumulator ───────────────────────────────────────────────────────────
ACC_OD  = 127    # body OD (mm)
ACC_LEN = 200    # body length (mm) — axis perpendicular to panel

# ── Filter housing (separate, 4.5"×10") ──────────────────────────────────
FILT_OD  = 130   # housing OD (mm)
FILT_H   = 340   # total height (mm) — head + sump, hung vertically
FILT_GAP = 35    # gap between housings (mm)
FILT_HEAD = 70   # head section height (mm)

# ── Layout on panel face ─────────────────────────────────────────────────
# Left column: 3 pumps stacked vertically + ACC-01 above
PUMP_COL_X = 100   # pump column center (panel-relative mm)

P01_Z = 280
P02_Z = P01_Z + PUMP_H + PUMP_GAP   # 548
P04_Z = P02_Z + PUMP_H + PUMP_GAP   # 816

ACC_X = PUMP_COL_X
ACC_Z = P04_Z + PUMP_H + PUMP_GAP + ACC_OD // 2   # 1097

# Right section: 3 filter housings side by side
FILT_START_X = 280   # left edge of first housing
F01_X_C = FILT_START_X + FILT_OD // 2              # 345 center
F02_X_C = F01_X_C + FILT_OD + FILT_GAP             # 510
F03_X_C = F02_X_C + FILT_OD + FILT_GAP             # 675
FILT_Z_BOT = 300     # housing bottom (sump bowl)
FILT_Z_TOP = FILT_Z_BOT + FILT_H                   # 830

# Panel dimensions (with margins)
PANEL_MARGIN = 40
PANEL_X_L = 0
PANEL_X_R = F03_X_C + FILT_OD // 2 + PANEL_MARGIN  # ~780
PANEL_Z_BOT = 150
PANEL_Z_TOP = ACC_Z + ACC_OD // 2 + PANEL_MARGIN + 40  # ~1200

PANEL_WIDTH  = PANEL_X_R - PANEL_X_L
PANEL_HEIGHT = PANEL_Z_TOP - PANEL_Z_BOT

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
SC  = 100.0   # mm per inch (main elevation)
FW  = 10.0
FH  = 17.5

# Show range (panel + margins for dimensions/leaders)
X_SHOW_L = -80
X_SHOW_R = PANEL_X_R + 100
Z_SHOW_L = 0
Z_SHOW_R = PANEL_Z_TOP + 80

OX = 1.2
OZ = 3.5    # leave room for cross-section strip below


def sx(x_mm):
    """Panel-relative X (mm) → figure x (inches)."""
    return OX + (x_mm - X_SHOW_L) / SC


def sz(z_mm):
    """Z AFF (mm) → figure y (inches)."""
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
#  MAIN ELEVATION — PANEL FACE (looking at panel from walkway side)
# ═══════════════════════════════════════════════════════════════════════════

# Title above panel
ax.text(sx(PANEL_WIDTH / 2), sz(Z_SHOW_R) + 0.15,
        "FRONT ELEVATION — EQUIPMENT PANEL",
        ha="center", va="bottom",
        fontsize=6, color=C_DIM, fontweight="bold", zorder=10, **FONT)

# 1. Panel outline (18mm plywood)
rect(PANEL_X_L, PANEL_Z_BOT, PANEL_WIDTH, PANEL_HEIGHT,
     C_PLY, C_PLY_EC, lw=2.0, zorder=3, alpha=0.5)

# Panel label
ax.text(sx(PANEL_WIDTH / 2), sz(PANEL_Z_BOT + 20),
        f"18mm MARINE PLY PANEL — {PANEL_WIDTH}mm × {PANEL_HEIGHT}mm",
        ha="center", va="bottom",
        fontsize=4.5, color=C_PLY_EC, zorder=4, **FONT)

# Floor line
ax.plot([sx(X_SHOW_L), sx(X_SHOW_R)], [sz(0), sz(0)],
        color=C_OUT, lw=2.5, zorder=3)
ax.text(sx(X_SHOW_L + 10), sz(0) - 0.08,
        "FLOOR (Z=0)", ha="left", va="top",
        fontsize=4, color=C_DIM, zorder=10, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  2. PUMPS — 3× stacked vertically (left column)
# ═══════════════════════════════════════════════════════════════════════════
pump_specs = [
    ("P-01", "BLUE\nSUPPLY",    P01_Z, C_BLUE,     C_BLUE_EC),
    ("P-02", "BROWN\nRECYCLE",  P02_Z, C_BROWN,    C_BROWN_EC),
    ("P-04", "TRAY\nDRAIN",     P04_Z, C_BLACK_SYS, C_BLACK_EC),
]

for pname, pdesc, pz, pfc, pec in pump_specs:
    # Mounting bracket
    rect(PUMP_COL_X - PUMP_W / 2 - 10, pz - 8,
         PUMP_W + 20, 8,
         C_FRAME_FILL, C_FRAME, lw=0.5, zorder=4)
    # Pump body
    rect(PUMP_COL_X - PUMP_W / 2, pz, PUMP_W, PUMP_H,
         C_PUMP_BODY, C_PUMP_EC, lw=1.2, zorder=6)
    # Port indicators (top and bottom)
    for port_z in [pz + 25, pz + PUMP_H - 25]:
        circ(PUMP_COL_X, port_z, 10,
             C_PIPE_FILL, C_PIPE_EC, lw=0.5, zorder=7)
    # Label
    ax.text(sx(PUMP_COL_X), sz(pz + PUMP_H / 2 + 15),
            pname, ha="center", va="center",
            fontsize=6, color=pfc, fontweight="bold", zorder=8, **FONT)
    ax.text(sx(PUMP_COL_X), sz(pz + PUMP_H / 2 - 20),
            pdesc, ha="center", va="center",
            fontsize=3.5, color=pec, zorder=8, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  3. ACC-01 — above pump stack (end-on circle)
# ═══════════════════════════════════════════════════════════════════════════
circ(ACC_X, ACC_Z, ACC_OD / 2,
     C_ACC, C_BLUE_EC, lw=1.2, zorder=6, alpha=0.7)
ax.text(sx(ACC_X), sz(ACC_Z + 5),
        "ACC-01", ha="center", va="center",
        fontsize=5, color="white", fontweight="bold", zorder=8, **FONT)
ax.text(sx(ACC_X), sz(ACC_Z - 20),
        f"O/{ACC_OD}", ha="center", va="center",
        fontsize=3.5, color="white", zorder=8, **FONT)

# Mounting clamp (U-bracket)
clamp_w = ACC_OD + 20
rect(ACC_X - clamp_w / 2, ACC_Z + ACC_OD / 2,
     clamp_w, 8,
     C_FRAME_FILL, C_FRAME, lw=0.5, zorder=5)


# ═══════════════════════════════════════════════════════════════════════════
#  4. FILTER HOUSINGS — 3× separate, hung vertically (sump down)
# ═══════════════════════════════════════════════════════════════════════════
filter_specs = [
    ("F-01", F01_X_C),
    ("F-02", F02_X_C),
    ("F-03", F03_X_C),
]

for fname, fx_c in filter_specs:
    # Housing body (rectangle — side view of vertical cylinder)
    rect(fx_c - FILT_OD / 2, FILT_Z_BOT, FILT_OD, FILT_H,
         C_FILTER, C_OUT, lw=1.2, zorder=6, alpha=0.6)
    # Head section (darker top)
    rect(fx_c - FILT_OD / 2, FILT_Z_TOP - FILT_HEAD, FILT_OD, FILT_HEAD,
         "#3A70B0", C_OUT, lw=0.8, zorder=6, alpha=0.7)
    # Sump bowl line (bottom section)
    ax.plot([sx(fx_c - FILT_OD / 2), sx(fx_c + FILT_OD / 2)],
            [sz(FILT_Z_BOT + 60), sz(FILT_Z_BOT + 60)],
            color=C_OUT, lw=0.5, ls="--", zorder=7)
    # Port indicators on head (IN/OUT)
    for port_off in [-30, 30]:
        circ(fx_c + port_off, FILT_Z_TOP - FILT_HEAD / 2, 12,
             "#B8D4F0", C_OUT, lw=0.4, zorder=7, alpha=0.6)
    # Label
    ax.text(sx(fx_c), sz(FILT_Z_BOT + FILT_H / 2 + 30),
            fname, ha="center", va="center",
            fontsize=5.5, color="white", fontweight="bold", zorder=8, **FONT)
    # Bracket at top
    rect(fx_c - FILT_OD / 2 - 10, FILT_Z_TOP,
         FILT_OD + 20, 10,
         C_FRAME_FILL, C_FRAME, lw=0.5, zorder=5)

# "SUMP DOWN" annotation
ax.text(sx(F02_X_C), sz(FILT_Z_BOT - 25),
        "SUMP DOWN\n(cartridge access)", ha="center", va="top",
        fontsize=3.5, color=C_FILTER, zorder=10, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  5. ZONE LABELS
# ═══════════════════════════════════════════════════════════════════════════
# Pump zone
ax.text(sx(PUMP_COL_X), sz(P01_Z - 30),
        "PUMP MANIFOLD", ha="center", va="top",
        fontsize=4.5, color=C_PUMP_EC, fontweight="bold", zorder=10, **FONT)

# Filter zone
ax.text(sx(F02_X_C), sz(FILT_Z_TOP + 30),
        "FILTER SKID (×3)", ha="center", va="bottom",
        fontsize=4.5, color=C_FILTER, fontweight="bold", zorder=10, **FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  6. DIMENSIONS
# ═══════════════════════════════════════════════════════════════════════════

# Panel width
draw_dim_h(ax, sx(PANEL_X_L), sx(PANEL_X_R), sz(PANEL_Z_BOT - 40),
           f"{PANEL_WIDTH}", offset=0.06, fs=5, color=C_DIM, font=FONT)

# Pump body width
draw_dim_h(ax, sx(PUMP_COL_X - PUMP_W / 2), sx(PUMP_COL_X + PUMP_W / 2),
           sz(P01_Z - 15),
           f"{PUMP_W}", offset=0.04, fs=4, color=C_DIM, font=FONT)

# Filter OD
draw_dim_h(ax, sx(F01_X_C - FILT_OD / 2), sx(F01_X_C + FILT_OD / 2),
           sz(FILT_Z_BOT - 15),
           f"O/{FILT_OD}", offset=0.04, fs=4, color=C_FILTER, font=FONT)

# Filter housing height
draw_dim_v(ax, sx(F03_X_C + FILT_OD / 2 + 20),
           sz(FILT_Z_BOT), sz(FILT_Z_TOP),
           f"{FILT_H}", offset=0.08, fs=4.5, color=C_FILTER,
           right=True, font=FONT)

# Pump body height
draw_dim_v(ax, sx(PUMP_COL_X + PUMP_W / 2 + 15),
           sz(P01_Z), sz(P01_Z + PUMP_H),
           f"{PUMP_H}", offset=0.06, fs=4, color=C_DIM,
           right=True, font=FONT)

# Panel height
draw_dim_v(ax, sx(PANEL_X_L - 30), sz(PANEL_Z_BOT), sz(PANEL_Z_TOP),
           f"{PANEL_HEIGHT}", offset=0.1, fs=5, color=C_DIM,
           right=False, font=FONT)

# Filter spacing (center-to-center)
filt_cc = F02_X_C - F01_X_C
draw_dim_h(ax, sx(F01_X_C), sx(F02_X_C), sz(FILT_Z_TOP + 15),
           f"{int(filt_cc)} c/c", offset=0.04, fs=4, color=C_DIM, font=FONT)

# Panel Z position from floor
draw_dim_v(ax, sx(PANEL_X_R + 40), sz(0), sz(PANEL_Z_BOT),
           f"{PANEL_Z_BOT}", offset=0.08, fs=4.5, color=C_DIM,
           right=True, font=FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  7. LEADERS
# ═══════════════════════════════════════════════════════════════════════════

# Pump specs
leader(ax,
       sx(PUMP_COL_X - PUMP_W / 2), sz(P01_Z + PUMP_H / 2),
       sx(X_SHOW_L + 10), sz(P01_Z + PUMP_H / 2 + 40),
       "Shurflo 2088\n12V · 3.5 GPM · 45 PSI\n(×3 on SS L-brackets)",
       fs=4, color=C_PUMP_EC, font=FONT)

# ACC-01
leader(ax,
       sx(ACC_X + ACC_OD / 2), sz(ACC_Z),
       sx(PANEL_X_R + 30), sz(ACC_Z + 40),
       "ACC-01: 0.75L ACCUM.\nO/127 × 200mm\n1/2\" MNPT",
       fs=4, color=C_BLUE_EC, font=FONT)

# Filter specs
leader(ax,
       sx(F03_X_C + FILT_OD / 2), sz(FILT_Z_BOT + FILT_H / 2),
       sx(PANEL_X_R + 30), sz(FILT_Z_BOT + FILT_H / 2 + 30),
       "4.5\"×10\" FILTER HOUSING\n1\" NPT IN/OUT\n(×3 separate, sump-down)",
       fs=4, color=C_FILTER, font=FONT)

# Max depth annotation
max_depth = max(PUMP_D, FILT_OD)
leader(ax,
       sx(PUMP_COL_X), sz(PANEL_Z_TOP - 20),
       sx(X_SHOW_L + 10), sz(PANEL_Z_TOP + 30),
       f"MAX PROTRUSION: {max_depth}mm\nFROM PANEL FACE",
       fs=4, color=C_NEW, font=FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  CROSS-SECTION STRIP — panel position relative to walkway (Yd × Z)
# ═══════════════════════════════════════════════════════════════════════════

# Cross-section positioned at bottom of figure
CS_LEFT  = 1.0   # inches from left
CS_BOT   = 2.0   # inches from bottom
CS_W_IN  = 8.0   # strip width (inches)
CS_H_IN  = 1.2   # strip height (inches)

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
    (IBC_D) / YD_MAX * CS_W_IN, cs_z(Z_CS_MAX) - cs_z(0),
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

# Panel (18mm ply, back against near IBC at Yd=1046)
panel_yd_draw = cs_yd(PANEL_YD)
panel_t_draw = PANEL_T / YD_MAX * CS_W_IN
ax.add_patch(mpatches.Rectangle(
    (panel_yd_draw, cs_z(20)),
    panel_t_draw, cs_z(220) - cs_z(20),
    fc=C_PLY, ec=C_PLY_EC, lw=1.5, zorder=5))
ax.text(panel_yd_draw + panel_t_draw / 2, cs_z(230),
        "18mm\nPANEL", ha="center", va="bottom",
        fontsize=3, color=C_PLY_EC, fontweight="bold", zorder=10, **FONT)

# Equipment protrusion zone
equip_max_yd = PANEL_YD + PANEL_T + max_depth
ax.add_patch(mpatches.Rectangle(
    (panel_yd_draw + panel_t_draw, cs_z(30)),
    max_depth / YD_MAX * CS_W_IN,
    cs_z(200) - cs_z(30),
    fc="#FFE8D0", ec=C_PUMP_EC, lw=0.5, ls="--", zorder=4, alpha=0.4))
ax.text(cs_yd(PANEL_YD + PANEL_T + max_depth / 2), cs_z(115),
        f"EQUIP\n{max_depth}mm", ha="center", va="center",
        fontsize=3, color=C_PUMP_EC, zorder=5, **FONT)

# Clearance: equipment to far IBC
clearance = CORRIDOR_FAR - int(equip_max_yd)
draw_dim_h(ax, cs_yd(equip_max_yd), cs_yd(CORRIDOR_FAR), cs_z(-15),
           f"{clearance} CLEAR", offset=0.04, fs=3.5, color=C_NEW, font=FONT)

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
    "EQUIPMENT PANEL — IN IBC PLUMBING CORRIDOR",
    f"1. Panel: 18mm marine ply, back against near IBC column at Yd={PANEL_YD}.",
    f"2. Panel size: {PANEL_WIDTH}mm W × {PANEL_HEIGHT}mm H.",
    "3. Pumps: 3× Shurflo 2088 (12V, 3.5 GPM, 45 PSI) on SS L-brackets.",
    "4. ACC-01: 0.75L pressure accumulator, 1/2\" MNPT, inline P-01.",
    "5. Filters: 3× separate 4.5\"×10\" housings, sump-down for access.",
    f"6. Max protrusion from panel: {max_depth}mm into corridor.",
    f"7. Clearance to far IBC: {clearance}mm (of 270mm corridor).",
    f"8. Panel X position: ~{PANEL_WALL_X}–{PANEL_WALL_X + PANEL_WIDTH}mm along container.",
]
draw_notes(ax, notes, 0.3, 1.7, spacing=0.13,
           fs=4, width=FW - 0.6, color=C_DIM, title_color=C_NEW, font=FONT)


# ═══════════════════════════════════════════════════════════════════════════
#  TITLE BLOCK
# ═══════════════════════════════════════════════════════════════════════════
title_block(ax, "SHEET 1 OF 1",
            drawing_title="EQUIPMENT PANEL — IBC CORRIDOR MOUNTING",
            subtitle="FRONT ELEVATION + CROSS-SECTION",
            scale_note="ELEV SCALE 1:100 · X-SECTION NOT TO SCALE · ALL DIMS IN mm",
            doc_id="TBS-001 · Reorg Proposal",
            height=0.028)

# ── Save ─────────────────────────────────────────────────────────────────
os.makedirs(DIAGRAMS_DIR, exist_ok=True)
out = os.path.join(DIAGRAMS_DIR, "panel-layout.png")
fig.savefig(out, dpi=150, facecolor="white", edgecolor="none")
plt.close(fig)
print(f"Panel layout → {out}")
