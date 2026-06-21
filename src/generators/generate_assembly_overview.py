#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_assembly_overview.py

Generates diagrams/assembly-overview.png — high-level schematic side-elevation
of the TBS-001 container interior (redesigned film-plane-reduction layout).

View direction: looking at the near long wall (Y=0 face) from outside.
  X (horizontal) = 0–5893mm  (container long axis; left=cargo door, right=far end)
  H (vertical)   = 0–2388mm  (container height)
  Yd (into page) = 0–2362mm  (optical depth; not a diagram axis)

Zones (shadow-free proof):
  Left end zone:   X = 0–150mm     (light trap drum only)
  Optical zone:    X = 150–4649mm   (film plane only)
  Right end zone:  X = 4649–5893mm  (IBCs only, right-justified)
  Pinhole wall:    Yd = 0 face  (electrical + battery + pump; flush-mount)

ASPECT RATIO RULE: FIG_H = FIG_W * (Y_HI - Y_LO) / (X_HI - X_LO)
                   ax.set_aspect("equal") always set.
"""

import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader
from tbs_constants import (
    C_LEN, C_WID, C_HGT,
    FP_X_L, FP_X_R, FP_Y, FP_W,
    PH_X, PH_H, PH_D, PH_FNO,
    ZONE_L_END, ZONE_R_START,
    DRUM_CX, DRUM_D, DRUM_R, DRUM_H_LT,
    EVAP_DUCT_X, EVAP_DUCT_D, EVAP_DUCT_Z,
    EP_X, EP_W, EP_H_LO, EP_H_HI,
    PWR_PANEL_X, PWR_PANEL_W, PWR_PANEL_H,
    BA_X, BA_W, BA_H_LO, BA_H_HI,
    PUMP_X, PUMP_W, PUMP_H_LO, PUMP_H_HI,
    EQPANEL_X, EQPANEL_T, EQPANEL_Z_LO, EQPANEL_Z_HI,
    FSKID_X,
    IBC_COL_X, IBC_W, IBC_D, IBC_H_STK_1000, IBC_H_1000,
    BLUE_IBC_Y, BROWN_IBC_Y, IBC_FAR_Y,
    PANEL_CORNER_T, PANEL_CENTER_T,
    PANEL_CORNER_YD_L, PANEL_CORNER_YD_R, PANEL_CENTER_W,
    PIVOT_X, PIVOT_YD, SWING_LOCK_DEG, PANEL_CUT_YD, FAR_STRIP_YD0,
    RAIL_X_L, RAIL_X_R, RAIL_SPAN,
    FAN_A_H, FAN_B_H, FAN_DIAM, DUCT_HEIGHT,
    DIAGRAMS_DIR, 
    C_OUT, C_CL, C_DIM,
    C_WALL, C_WASTE_IBC, C_LT_DRUM, C_BLUE_IBC, C_BROWN_IBC,
    C_ELEC, C_BATT, C_PUMP, C_HINGE_PANEL, C_FAN, C_ALUM,
    cone_left, cone_right,
)

os.makedirs(DIAGRAMS_DIR, exist_ok=True)

# ── Constants shared with previous session ────────────────────────────────────
from tbs_constants import RAIL_OFF   # floor offset for all floor-standing equipment (mm)
DRUM_H_ELV = DRUM_H_LT   # 2000mm — revolving drum height in elevation view

# ── Palette ───────────────────────────────────────────────────────────────────
BG        = "#FFFFFF"
C_INTERIOR = "#F4F4F4"
C_ZONE_L  = "#FFF0E0"   # left end zone (orange tint)
C_ZONE_O  = "#F0FFF0"   # optical zone (green tint)
C_ZONE_R  = "#E8F0FF"   # right end zone (blue tint)

C_FILM_PLN  = "#B8D4E8"
C_PINHOLE   = "#CC2020"

FS_SM = 7.5
FS_MD = 8.5
FS_LG = 10.0

# ── Data range → figure size ──────────────────────────────────────────────────
X_LO, X_HI = -500, 7900   # right edge must clear title block: TB_X+TB_W = C_LEN+420+1380 = 7693
Y_LO, Y_HI = -650, 3100

FIG_W = 24.0
FIG_H = FIG_W * (Y_HI - Y_LO) / (X_HI - X_LO)
DPI   = 150

# ── Helpers ───────────────────────────────────────────────────────────────────
def equip_rect(ax, x, y, w, h, color, alpha=0.85, ec=C_OUT, lw=0.8, zorder=3):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="square,pad=0",
        facecolor=color, edgecolor=ec, linewidth=lw, alpha=alpha, zorder=zorder))

def corrugation_marks(ax, y, x_start, x_end, step=600, color="#B0B0B0"):
    x = x_start
    while x <= x_end:
        ax.plot([x, x], [y, y + (60 if y == 0 else -60)],
                color=color, lw=0.5, zorder=1)
        x += step


# ── Figure setup ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(X_LO, X_HI)
ax.set_ylim(Y_LO, Y_HI)
ax.set_aspect("equal")
ax.axis("off")


# ── Zone fills ────────────────────────────────────────────────────────────────
ax.add_patch(mpatches.Rectangle((0, 0), ZONE_L_END, C_HGT,
             facecolor=C_ZONE_L, edgecolor="none", alpha=0.6, zorder=0))
ax.add_patch(mpatches.Rectangle((ZONE_L_END, 0), ZONE_R_START - ZONE_L_END, C_HGT,
             facecolor=C_ZONE_O, edgecolor="none", alpha=0.5, zorder=0))
ax.add_patch(mpatches.Rectangle((ZONE_R_START, 0), C_LEN - ZONE_R_START, C_HGT,
             facecolor=C_ZONE_R, edgecolor="none", alpha=0.6, zorder=0))

# Zone boundary dashed lines
for xb in [ZONE_L_END, ZONE_R_START]:
    ax.plot([xb, xb], [0, C_HGT], color=C_DIM, lw=1.0, ls="--",
            dashes=(8, 4), zorder=4)

# Zone labels (inside, at top)
ax.text(ZONE_L_END / 2, C_HGT + 100,
        f"LEFT END ZONE\nX=0–{ZONE_L_END}mm",
        ha="center", va="top", fontsize=FS_SM - 0.5, color="#805000",
        fontweight="bold", zorder=5)
ax.text((ZONE_L_END + ZONE_R_START) / 2, C_HGT + 100,
        f"OPTICAL ZONE\nX={ZONE_L_END}–{ZONE_R_START}mm",
        ha="center", va="top", fontsize=FS_SM - 0.5, color="#006000",
        fontweight="bold", zorder=5)
ax.text((ZONE_R_START + C_LEN) / 2, C_HGT + 100,
        f"RIGHT END ZONE\nX={ZONE_R_START}–{C_LEN}mm",
        ha="center", va="top", fontsize=FS_SM - 0.5, color="#004080",
        fontweight="bold", zorder=5)


# ── Container outline + corrugation ──────────────────────────────────────────
ax.add_patch(mpatches.Rectangle((0, 0), C_LEN, C_HGT,
             facecolor="none", edgecolor=C_OUT, linewidth=1.8, zorder=5))
corrugation_marks(ax, 0,    0, C_LEN, step=600)
corrugation_marks(ax, C_HGT, 0, C_LEN, step=600)


# ── LEFT END ZONE — revolving drum ────────────────────────────────────────────

# Hinged panel — stepped profile (rev 4): 40mm corner zones, 120mm center zone.
# In this side elevation (X-H plane), the stepped depth is visible.
# Corner zones (majority of panel width) shown at 40mm depth inside X=0.
# Center zone (drum housing, Yd=653-1709) shown at 120mm depth.
# Container wall (40mm steel) drawn outside at X=-40 to 0.
ax.add_patch(mpatches.Rectangle((-40, 0), 40, C_HGT,
             facecolor=C_HINGE_PANEL, edgecolor=C_OUT, linewidth=0.8, alpha=0.5, zorder=4))
# Corner zone panel (40mm, X=0 to 40) — visible in side elevation as dominant depth
ax.add_patch(mpatches.Rectangle((0, 0), PANEL_CORNER_T, C_HGT,
             facecolor=C_HINGE_PANEL, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=4))
# Center zone panel (120mm, X=0 to 120) — shown as dashed outline behind corner
ax.add_patch(mpatches.Rectangle((0, 0), PANEL_CENTER_T, C_HGT,
             facecolor="none", edgecolor=C_OUT, linewidth=0.6, ls=(0, (4, 3)),
             alpha=0.5, zorder=4))

# Revolving drum: center at X=0 (outside edge of container), bottom at Y=RAIL_OFF
# In this side elevation appears as a rectangle Ø900mm wide × 2000mm tall.
ax.add_patch(mpatches.Rectangle((-DRUM_R, RAIL_OFF), DRUM_D, DRUM_H_ELV,
             facecolor=C_LT_DRUM, edgecolor=C_OUT, linewidth=0.8, alpha=0.9, zorder=5))
# Center line through drum
ax.plot([DRUM_CX, DRUM_CX], [RAIL_OFF, RAIL_OFF + DRUM_H_ELV + 100],
        color=C_CL, lw=0.7, ls="--", dashes=(6, 3), zorder=6)
leader(ax, DRUM_CX, RAIL_OFF + DRUM_H_ELV + 60, -200, PH_H + 1250,
       f"Hinged panel +\nRevolving drum  VERTICAL AXIS\nO{DRUM_D}mm x {DRUM_H_ELV}mm H",
       ha="right", fs=FS_SM)

# Duct penetration — Ø200mm through pinhole wall for external evap cooler
duct_r = EVAP_DUCT_D / 2
ax.add_patch(plt.Circle((EVAP_DUCT_X, EVAP_DUCT_Z), duct_r,
             facecolor="#E8E8E8", edgecolor=C_OUT, linewidth=1.0,
             linestyle="--", zorder=4))
ax.text(EVAP_DUCT_X, EVAP_DUCT_Z,
        f"Ø{EVAP_DUCT_D}", ha="center", va="center",
        fontsize=FS_SM - 1.5, color=C_OUT, zorder=6)
leader(ax, EVAP_DUCT_X + duct_r, EVAP_DUCT_Z + duct_r, 1300, 2500,
       f"Evap duct penetration\nØ{EVAP_DUCT_D}mm (external unit)",
       ha="left", fs=FS_SM)

# Black-water drums — 2× 55-gal, one per Yd corner (rev 4: on slide dollies).
# In this side elevation both drums share X → collapse to single block.
# (waste drums eliminated in rev 5 — left zone is light trap only)


# ── PINHOLE WALL EQUIPMENT — flush-mount on near long wall (Yd=0 face) ────────

# Electrical panel: X=1910-2210 (stacked above the battery), Z=1650-2250
equip_rect(ax, EP_X, EP_H_LO, EP_W, EP_H_HI - EP_H_LO, C_ELEC, ec=C_OUT, lw=1.0, zorder=4)
ax.text(EP_X + EP_W/2, (EP_H_LO + EP_H_HI)/2,
        "Elec\npanel", ha="center", va="center",
        fontsize=FS_SM - 1, color=C_OUT, zorder=6)

# Battery bank: X=1810-2310, H=100-600
equip_rect(ax, BA_X, BA_H_LO, BA_W, BA_H_HI - BA_H_LO, C_BATT, zorder=4)
ax.text(BA_X + BA_W/2, (BA_H_LO + BA_H_HI)/2,
        "Battery\nbank", ha="center", va="center",
        fontsize=FS_SM - 1, color="#FFFFFF", zorder=6)

# Equipment panel zone: X=4870–5018, Z=900–2010 (pumps+filters, Yd=1046–1316)
EQ_ZONE_X = FSKID_X
EQ_ZONE_W = EQPANEL_X + EQPANEL_T - FSKID_X
equip_rect(ax, EQ_ZONE_X, EQPANEL_Z_LO, EQ_ZONE_W, EQPANEL_Z_HI - EQPANEL_Z_LO, C_PUMP,
           alpha=0.50, ec=C_OUT, lw=0.7, zorder=3)
ax.text(EQ_ZONE_X + EQ_ZONE_W/2, (EQPANEL_Z_LO + EQPANEL_Z_HI)/2,
        "Equip panel\n[Yd=1046]", ha="center", va="center",
        fontsize=FS_SM - 1, color=C_OUT, zorder=6)

leader(ax, EP_X + EP_W, (EP_H_LO + EP_H_HI)/2, EP_X + 500, 2000,
       f"Electrical panel\n(wall-mount, Yd=0 face)\nX={EP_X}–{EP_X+EP_W}mm",
       ha="left", fs=FS_SM)
leader(ax, BA_X + BA_W, BA_H_HI, BA_X + (BA_W*2), 800,
       f"Battery bank\nX={BA_X}–{BA_X+BA_W}mm", ha="left", fs=FS_SM)
leader(ax, EQ_ZONE_X + EQ_ZONE_W, (EQPANEL_Z_LO + EQPANEL_Z_HI)/2, EQ_ZONE_X + 1500, 700,
       f"Equipment panel  (pumps+filters, Yd=1046–1316)\nX={EQ_ZONE_X}–{EQ_ZONE_X+EQ_ZONE_W}mm", ha="left", fs=FS_SM)

# External power panel — flush-mount on exterior of pinhole wall (ghost from this view)
PP_CTR_H = (EP_H_LO + EP_H_HI) / 2
PP_H_BOT = PP_CTR_H - PWR_PANEL_H / 2
ax.add_patch(mpatches.FancyBboxPatch(
    (PWR_PANEL_X, PP_H_BOT), PWR_PANEL_W, PWR_PANEL_H, boxstyle="square,pad=0",
    facecolor=C_ALUM, edgecolor=C_OUT, linewidth=0.7,
    linestyle="--", alpha=0.20, zorder=2))
ax.text(PWR_PANEL_X + PWR_PANEL_W / 2, PP_CTR_H,
        "Ext pwr\npanel\n[exterior]",
        ha="center", va="center", fontsize=FS_SM - 1.5, color=C_DIM,
        alpha=0.6, zorder=3)


# ── RIGHT END ZONE — IBC column + drum column ─────────────────────────────────

# IBC 2×2 stack — side elevation (depth into page): near column in front, far behind.
# Near column: Blue #1 top + Brown bottom.  Far column: Blue #2 top + Waste bottom.

# Far column (behind — dimmer): Waste bottom + Blue #2 top
equip_rect(ax, IBC_COL_X, 0, IBC_W, IBC_H_1000, C_WASTE_IBC, alpha=0.40, zorder=3)
equip_rect(ax, IBC_COL_X, IBC_H_1000, IBC_W, IBC_H_1000, C_BLUE_IBC, alpha=0.40, zorder=3)

# Near column (front): Brown bottom + Blue #1 top
equip_rect(ax, IBC_COL_X, 0, IBC_W, IBC_H_1000, C_BROWN_IBC, alpha=0.80, zorder=5)
ax.text(IBC_COL_X + IBC_W/2, IBC_H_1000/2,
        "IBC-3 Brown\n(bottom, front)",
        ha="center", va="center", fontsize=FS_SM - 1, color="#FFFFFF", zorder=6)
equip_rect(ax, IBC_COL_X, IBC_H_1000, IBC_W, IBC_H_1000, C_BLUE_IBC, alpha=0.80, zorder=5)
ax.text(IBC_COL_X + IBC_W/2, IBC_H_1000 + IBC_H_1000/2,
        "IBC-1 Blue\n(top, front)",
        ha="center", va="center", fontsize=FS_SM, color="#FFFFFF",
        fontweight="bold", zorder=6)
# Stacking line
ax.plot([IBC_COL_X, IBC_COL_X + IBC_W], [IBC_H_1000, IBC_H_1000],
        color="#FFFFFF", lw=0.8, ls="--", alpha=0.7, zorder=7)

leader(ax, IBC_COL_X + IBC_W/2, IBC_H_STK_1000, 6000, 2750,
       f"4× IBC 2×2 stack  X={IBC_COL_X}–{IBC_COL_X+IBC_W}mm\n"
       f"Near: Blue #1 top + Brown bottom\n"
       f"Far: Blue #2 top + Waste bottom (behind)",
       ha="left", fs=FS_SM)

# (drums relocated to left end zone — right zone has IBCs only)


# ── Film plane (symbolic band at floor and ceiling) ───────────────────────────
# The film plane at Yd=2262mm spans X=FP_X_L–FP_X_R in this elevation.
FP_BAND = 80
ax.add_patch(mpatches.Rectangle((FP_X_L, 0), FP_X_R - FP_X_L, FP_BAND,
             facecolor=C_FILM_PLN, edgecolor=C_CL, linewidth=0.8,
             linestyle="--", alpha=0.8, zorder=2))
ax.text((FP_X_L + FP_X_R)/2, FP_BAND/2,
        f"Film plane  X={FP_X_L}–{FP_X_R}mm  "
        f"({FP_X_R-FP_X_L}mm wide x {C_HGT}mm H)  at Yd={FP_Y}mm",
        ha="center", va="center", fontsize=FS_SM, color=C_CL,
        style="italic", zorder=6)
ax.add_patch(mpatches.Rectangle((FP_X_L, C_HGT - FP_BAND), FP_X_R - FP_X_L, FP_BAND,
             facecolor=C_FILM_PLN, edgecolor=C_CL, linewidth=0.8,
             linestyle="--", alpha=0.5, zorder=2))

# Rail slot indicators at X=RAIL_X_L and X=RAIL_X_R
for rx in [RAIL_X_L, RAIL_X_R]:
    ax.plot([rx, rx], [0, 80], color=C_CL, lw=1.5, zorder=4)
    ax.plot([rx, rx], [C_HGT - 80, C_HGT], color=C_CL, lw=1.5, zorder=4)


# ── Pinhole ───────────────────────────────────────────────────────────────────
PINHOLE_SYM_R = 60
ph = plt.Circle((PH_X, PH_H), PINHOLE_SYM_R,
                 facecolor=C_PINHOLE, edgecolor=C_OUT, linewidth=0.8, zorder=7)
ax.add_patch(ph)
ax.plot([PH_X - 160, PH_X + 160], [PH_H, PH_H], color=C_PINHOLE, lw=0.8, zorder=8)
ax.plot([PH_X, PH_X], [PH_H - 160, PH_H + 160], color=C_PINHOLE, lw=0.8, zorder=8)
leader(ax, PH_X + PINHOLE_SYM_R + 40, PH_H, PH_X + 600, PH_H + 450,
       f"Pinhole  O{PH_D}mm\n(X={PH_X}, H={PH_H}mm)\nf/{PH_FNO}",
       ha="left", fs=FS_SM, color=C_PINHOLE)
ax.text(PH_X, PH_H - 300, f"Optical axis (into page)\nFocal length {C_WID}mm",
        ha="center", va="top", fontsize=FS_SM, color=C_CL, style="italic")


# ── Ventilation fans ──────────────────────────────────────────────────────────
# Fan A — EXHAUST: sealed end wall (X=C_LEN), Yd=FAN_A_YD=1181 (below X1, in corridor), H=FAN_A_H=2000mm
# Fan B — INTAKE: cargo door panel (X=0), low position (H=FAN_B_H=600mm)
FAN_HH = DUCT_HEIGHT  # duct opening height (200mm) — same as hatch block height
ax.add_patch(mpatches.Rectangle((C_LEN - 60, FAN_A_H - FAN_HH // 2), 60, FAN_HH,
             facecolor=C_FAN, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=4))
ax.text(C_LEN - 30, FAN_A_H, "FAN\nOUT", ha="center", va="center",
        fontsize=FS_SM - 1.5, color=C_OUT, zorder=5)

ax.add_patch(mpatches.Rectangle((0, FAN_B_H - FAN_HH // 2), 60, FAN_HH,
             facecolor=C_FAN, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=4))
ax.text(30, FAN_B_H, "FAN\nIN", ha="center", va="center",
        fontsize=FS_SM - 1.5, color=C_OUT, zorder=5)


# ── Safelight strip ───────────────────────────────────────────────────────────
ax.plot([100, C_LEN - 100], [C_HGT - 100, C_HGT - 100],
        color="#FFD700", lw=2, ls="--", dashes=(8, 5), alpha=0.7, zorder=4)
ax.text(C_LEN/2, C_HGT - 60, "Overhead safelight strip (Circuit D)",
        ha="center", va="bottom", fontsize=FS_SM - 1, color="#B8960A")


# ── Dimensions ────────────────────────────────────────────────────────────────
DIM_TOP   = C_HGT + 250
DIM_BOT   = -250
DIM_RIGHT = C_LEN + 350

draw_dim_h(ax, 0, C_LEN, DIM_TOP, f"Container length  {C_LEN}mm", offset=100, fs=FS_SM)
draw_dim_h(ax, ZONE_L_END, ZONE_R_START, DIM_TOP + 200,
           f"Optical zone  {ZONE_R_START-ZONE_L_END}mm", offset=80, fs=FS_SM, color=C_CL)
draw_dim_h(ax, FP_X_L, FP_X_R, DIM_TOP + 360,
           f"Film plane  {FP_X_R-FP_X_L}mm", offset=80, fs=FS_SM, color=C_CL)
draw_dim_v(ax, DIM_RIGHT - 225,        0, C_HGT, f"H={C_HGT}mm",     offset=50, fs=FS_SM)
draw_dim_v(ax, DIM_RIGHT - 100,  0, PH_H,  f"PH H={PH_H}mm",   offset=50, fs=FS_SM)

# Left / right zone widths
draw_dim_h(ax, 0, ZONE_L_END, DIM_BOT - 80,
           f"L zone\n{ZONE_L_END}mm", offset=60, fs=FS_SM - 0.5, color="#805000")
draw_dim_h(ax, ZONE_R_START, C_LEN, DIM_BOT - 80,
           f"R zone\n{C_LEN-ZONE_R_START}mm", offset=60, fs=FS_SM - 0.5, color="#004080")

ax.text(C_LEN/2, DIM_BOT - 300,
        f"All equipment in shadow-free end zones (X<{ZONE_L_END} or X>{ZONE_R_START}), on pinhole wall (Yd=0), or in IBC corridor",
        ha="center", va="top", fontsize=FS_SM, color="#004020", style="italic")


# ── Legend ────────────────────────────────────────────────────────────────────
LEG_X   = C_LEN + 420
LEG_Y   = 2200
LEG_W   = 600
LEG_H   = 60
LEG_GAP = 82

legend_items = [
    (C_BLUE_IBC,  "Blue IBC x2 (top tier)"),
    (C_BROWN_IBC, "Brown IBC x1 (bottom near)"),
    (C_WASTE_IBC, "Waste IBC x1 (bottom far)"),
    ("#E8E8E8",   "Evap duct penetration (ext unit)"),
    (C_PUMP,      "Equipment panel (pumps+filters)"),
    (C_ELEC,      "Electrical panel"),
    (C_BATT,      "Battery bank"),
    (C_FILM_PLN,  "Film plane (symbolic band)"),
    (C_PINHOLE,   "Pinhole O2.17mm"),
    (C_HINGE_PANEL,      "Hinged panel + drum"),
    (C_FAN,       "Ventilation fan"),
    (C_ALUM,      "Ext power panel  [ghost = exterior]"),
]

ax.text(LEG_X, LEG_Y + LEG_H + 30, "LEGEND", ha="left", va="bottom",
        fontsize=FS_MD, color=C_OUT, fontweight="bold")
for i, (col, lbl) in enumerate(legend_items):
    yy = LEG_Y - i * LEG_GAP
    ax.add_patch(mpatches.Rectangle((LEG_X, yy - LEG_H*0.5), LEG_W*0.28, LEG_H*0.7,
                 facecolor=col, edgecolor=C_OUT, linewidth=0.6, zorder=6))
    ax.text(LEG_X + LEG_W*0.34, yy, lbl, ha="left", va="center",
            fontsize=FS_SM, color=C_OUT)


# ── Title block ───────────────────────────────────────────────────────────────
title_block(ax, "SHEET 1 OF 3",
            drawing_title="ASSEMBLY OVERVIEW",
            subtitle="Side elevation — near long wall (+Y direction)",
            scale_note="1:75 (approx)",
            doc_id="TBS-001 · Assembly Overview")


# ── Save ──────────────────────────────────────────────────────────────────────
out = f"{DIAGRAMS_DIR}/assembly-overview.png"
fig.tight_layout(pad=0)
plt.savefig(out, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.close(fig)
print(f"Saved: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 2 — FILM PLANE SIDE ELEVATION
#
# Same axes as diagram 1 (X horizontal, H vertical) but viewed from the film
# plane wall (Yd = C_WID face) looking toward the pinhole wall (Yd = 0).
#
# In standard orthographic projection the left/right axis is MIRRORED vs the
# near-wall elevation: cargo door (X=0) now appears on the RIGHT, far end
# (X=C_LEN) on the LEFT.  Both diagrams are labelled with their view direction
# so the orientation is unambiguous.
#
# Hero elements in this view (absent or minimal in diagram 1):
#   • Optical cone — filled polygon from pinhole to all four film-plane corners
#   • Film plane rails — the dominant vertical features spanning floor→ceiling
#   • Rail carriage (symbolic) — horizontal traversing element
#   • Pinhole shown ghost/dashed — it lives on the far wall from this viewpoint
#   • Pinhole-wall equipment (elec/batt/pump) ghost — same reason
# ═══════════════════════════════════════════════════════════════════════════════

# Mirror function: convert real X coord → plotting coord for this view.
# Cargo door (X=0) → right edge; far end (X=C_LEN) → left edge.
def mx(x):
    return C_LEN - x

# Data range — same physical padding as diagram 1; title block on RIGHT side
# (which is the cargo door end in mirrored coordinates).
X2_LO, X2_HI = -500, 7900
Y2_LO, Y2_HI = -650, 3100

FIG2_W = 24.0
FIG2_H = FIG2_W * (Y2_HI - Y2_LO) / (X2_HI - X2_LO)

fig2, ax2 = plt.subplots(figsize=(FIG2_W, FIG2_H), dpi=DPI)
fig2.patch.set_facecolor(BG)
ax2.set_facecolor(BG)
ax2.set_xlim(X2_LO, X2_HI)
ax2.set_ylim(Y2_LO, Y2_HI)
ax2.set_aspect("equal")
ax2.axis("off")

# Helpers that apply the mirror transform
def eq2(x, y, w, h, color, alpha=0.85, ec=C_OUT, lw=0.8, zorder=3):
    """equip_rect with mirrored X (note: w is still positive, x is left edge in real coords)."""
    ax2.add_patch(mpatches.FancyBboxPatch(
        (mx(x + w), y), w, h, boxstyle="square,pad=0",
        facecolor=color, edgecolor=ec, linewidth=lw, alpha=alpha, zorder=zorder))

def ldr2(x_tip, y_tip, x_txt, y_txt, label, fs=FS_SM, color=C_OUT, ha="left"):
    """Leader line in mirrored coords."""
    leader(ax2, mx(x_tip), y_tip, mx(x_txt), y_txt, label, fs=fs, color=color, ha=ha)

def dim2h(x1, x2, y, label, offset=80, fs=FS_SM, color=C_DIM):
    """Horizontal dimension in mirrored coords (x1 < x2 in real space)."""
    draw_dim_h(ax2, mx(x2), mx(x1), y, label, offset=offset, fs=fs, color=color)

# ── Zone fills ────────────────────────────────────────────────────────────────
ax2.add_patch(mpatches.Rectangle((mx(ZONE_L_END), 0), ZONE_L_END, C_HGT,
             facecolor=C_ZONE_L, edgecolor="none", alpha=0.6, zorder=0))
ax2.add_patch(mpatches.Rectangle((mx(ZONE_R_START), 0), ZONE_R_START - ZONE_L_END, C_HGT,
             facecolor=C_ZONE_O, edgecolor="none", alpha=0.5, zorder=0))
ax2.add_patch(mpatches.Rectangle((0, 0), C_LEN - ZONE_R_START, C_HGT,
             facecolor=C_ZONE_R, edgecolor="none", alpha=0.6, zorder=0))

for xb in [ZONE_L_END, ZONE_R_START]:
    ax2.plot([mx(xb), mx(xb)], [0, C_HGT], color=C_DIM, lw=1.0, ls="--",
            dashes=(8, 4), zorder=4)

# Zone labels — note LEFT/RIGHT labels swap because view is mirrored
ax2.text(mx(ZONE_L_END/2), C_HGT + 100,
        f"RIGHT END ZONE\n(far end,  X={ZONE_R_START}–{C_LEN}mm)",
        ha="center", va="top", fontsize=FS_SM - 0.5, color="#004080",
        fontweight="bold", zorder=5)
ax2.text(mx((ZONE_L_END + ZONE_R_START) / 2), C_HGT + 100,
        f"OPTICAL ZONE\nX={ZONE_L_END}–{ZONE_R_START}mm",
        ha="center", va="top", fontsize=FS_SM - 0.5, color="#006000",
        fontweight="bold", zorder=5)
ax2.text(mx((ZONE_R_START + C_LEN) / 2), C_HGT + 100,
        f"LEFT END ZONE\n(cargo door,  X=0–{ZONE_L_END}mm)",
        ha="center", va="top", fontsize=FS_SM - 0.5, color="#805000",
        fontweight="bold", zorder=5)

# ── Container outline ─────────────────────────────────────────────────────────
ax2.add_patch(mpatches.Rectangle((0, 0), C_LEN, C_HGT,
             facecolor="none", edgecolor=C_OUT, linewidth=1.8, zorder=5))
for xc in range(0, C_LEN + 1, 600):
    pxc = mx(xc)
    ax2.plot([pxc, pxc], [0, 60], color="#B0B0B0", lw=0.5, zorder=1)
    ax2.plot([pxc, pxc], [C_HGT - 60, C_HGT], color="#B0B0B0", lw=0.5, zorder=1)

# ── OPTICAL CONE — the hero element of this view ──────────────────────────────
# The pinhole is at (PH_X, 0, PH_H) — on the near wall (Yd=0), which is the
# FAR wall from this viewpoint.  The cone fans out to the four corners of the
# film plane rectangle at Yd=FP_Y.
C_CONE   = "#4488CC"
C_CONE_L = "#CCE4FF"

cone_poly_x = [mx(PH_X), mx(FP_X_L), mx(FP_X_L), mx(FP_X_R), mx(FP_X_R), mx(PH_X)]
cone_poly_h = [PH_H,      0,           C_HGT,       C_HGT,       0,           PH_H]
ax2.fill(cone_poly_x, cone_poly_h, facecolor=C_CONE_L, edgecolor="none",
         alpha=0.30, zorder=1)
# Bounding rays
for fx in [FP_X_L, FP_X_R]:
    for fh in [0, C_HGT]:
        ax2.plot([mx(PH_X), mx(fx)], [PH_H, fh],
                color=C_CONE, lw=0.8, ls="--", dashes=(6, 4), alpha=0.7, zorder=2)

ax2.text(mx(PH_X + (FP_X_R - PH_X) * 0.55), PH_H + 300,
        f"Optical cone — f={C_WID}mm,  f/1088",
        ha="center", va="bottom", fontsize=FS_SM, color=C_CONE, style="italic", zorder=6)

# ── FILM PLANE RAILS — the dominant structural feature ───────────────────────
# Rail tracks at X=RAIL_X_L and X=RAIL_X_R, spanning RAIL_OFF to C_HGT-RAIL_OFF
RAIL_T   = 40    # rail half-width in drawing
RAIL_CLR = "#3060A0"

C_ALUM2 = "#C8D8E8"
for rx in [RAIL_X_L, RAIL_X_R]:
    ax2.add_patch(mpatches.Rectangle(
        (mx(rx) - RAIL_T, RAIL_OFF), RAIL_T * 2, C_HGT - 2 * RAIL_OFF,
        facecolor=C_ALUM2, edgecolor=RAIL_CLR, linewidth=1.2, alpha=0.9, zorder=5))

# Rail center lines
for rx in [RAIL_X_L, RAIL_X_R]:
    ax2.plot([mx(rx), mx(rx)], [0, C_HGT + 150],
            color=C_CL, lw=0.7, ls="--", dashes=(6, 3), zorder=6)

# Rail span dimension
# dim2h(RAIL_X_L, RAIL_X_R, C_HGT + 280,
#      f"Rail span  {RAIL_SPAN}mm  (= film plane width)", offset=80, color=RAIL_CLR)

# ── FILM PLANE carriage (symbolic) ───────────────────────────────────────────
# Carriage shown at mid-height and a representative depth (schematic only)
# CAR_H_MID = C_HGT // 2
# CAR_H_SZ  = 300    # half-height of carriage symbol
# ax2.add_patch(mpatches.Rectangle(
#     (mx(FP_X_R) + RAIL_T, CAR_H_MID - CAR_H_SZ), FP_W - 2 * RAIL_T, CAR_H_SZ * 2,
#     facecolor=C_FILM_PLN, edgecolor=C_CL, linewidth=0.8, linestyle="--",
#     alpha=0.55, zorder=3))
# ax2.text(mx((FP_X_L + FP_X_R) / 2), CAR_H_MID,
#         f"Film plane carriage\n(symbolic — {FP_W}mm × {C_HGT}mm active area)",
#         ha="center", va="center", fontsize=FS_SM, color=C_CL,
#         style="italic", zorder=7)

# Rail anchor marks at floor and ceiling
for rx in [RAIL_X_L, RAIL_X_R]:
    for ry in [RAIL_OFF, C_HGT - RAIL_OFF]:
        ax2.add_patch(plt.Circle((mx(rx), ry), 30,
                     facecolor=RAIL_CLR, edgecolor=C_OUT, linewidth=0.8, zorder=6))

# ── PINHOLE — on the near wall (far depth from this viewpoint): ghost ─────────
ax2.add_patch(plt.Circle((mx(PH_X), PH_H), PINHOLE_SYM_R,
             facecolor="none", edgecolor=C_PINHOLE, linewidth=1.2,
             linestyle="--", alpha=0.55, zorder=4))
ax2.plot([mx(PH_X) - 120, mx(PH_X) + 120], [PH_H, PH_H],
        color=C_PINHOLE, lw=0.7, alpha=0.55, zorder=4)
ax2.plot([mx(PH_X), mx(PH_X)], [PH_H - 120, PH_H + 120],
        color=C_PINHOLE, lw=0.7, alpha=0.55, zorder=4)
ldr2(PH_X, PH_H, PH_X - 225, PH_H + 500,
    f"Pinhole  Ø2.17mm\n(X={PH_X}, H={PH_H}mm)\n[on far wall — ghost]",
    ha="right", fs=FS_SM, color=C_PINHOLE)
ax2.text(mx(PH_X), PH_H - 320,
        "Optical axis (out of page)\nFocal length 2362mm",
        ha="center", va="top", fontsize=FS_SM, color=C_CL, style="italic")

# Rail labels
ldr2(RAIL_X_L, RAIL_OFF + 300, RAIL_X_L + 650, 600,
    f"Floor rail  X={RAIL_X_L}mm\n(left rail, cargo-door side)", ha="left", fs=FS_SM, color=RAIL_CLR)
ldr2(RAIL_X_R, C_HGT - 300, RAIL_X_R - 650, C_HGT - 600,
    f"Floor rail  X={RAIL_X_R}mm\n(right rail, far-end side)", ha="right", fs=FS_SM, color=RAIL_CLR)

# ── LEFT END ZONE (appears on RIGHT in this view) — drum ─────────────────────
# Hinged panel — stepped profile (rev 4): container wall outside, then
# corner zones (40mm) and center zone (120mm) inside.
ax2.add_patch(mpatches.Rectangle((C_LEN, 0), 40, C_HGT,
             facecolor=C_HINGE_PANEL, edgecolor=C_OUT, linewidth=0.8, alpha=0.5, zorder=4))
# Corner zone (40mm inside)
ax2.add_patch(mpatches.Rectangle((C_LEN - PANEL_CORNER_T, 0), PANEL_CORNER_T, C_HGT,
             facecolor=C_HINGE_PANEL, edgecolor=C_OUT, linewidth=0.6, alpha=0.4, zorder=4))
# Center zone outline (120mm inside, dashed — deeper zone behind)
ax2.add_patch(mpatches.Rectangle((C_LEN - PANEL_CENTER_T, 0), PANEL_CENTER_T, C_HGT,
             facecolor="none", edgecolor=C_OUT, linewidth=0.6, ls=(0, (4, 3)),
             alpha=0.4, zorder=4))

# Revolving drum
ax2.add_patch(mpatches.Rectangle((C_LEN - DRUM_D, RAIL_OFF), DRUM_D, DRUM_H_ELV,
             facecolor=C_LT_DRUM, edgecolor=C_OUT, linewidth=0.8, alpha=0.9, zorder=5))
ax2.plot([C_LEN, C_LEN], [RAIL_OFF, RAIL_OFF + DRUM_H_ELV + 100],
        color=C_CL, lw=0.7, ls="--", dashes=(6, 3), zorder=6)

# (evap cooler removed — external unit with duct penetration at X=1200)
# (waste drums eliminated in rev 5 — left zone is light trap only)

ldr2(0, RAIL_OFF + DRUM_H_ELV * 0.3, -750, 900,
    "Hinged panel +\nRevolving drum  Ø{0}mm × {1}mm H\n(cargo door, right in this view)".format(DRUM_D, DRUM_H_ELV),
    ha="left", fs=FS_SM)

# ── RIGHT END ZONE (appears on LEFT in this view) — 4× IBC 2×2 stack ────────
# Near column (behind in this view): Brown bottom + Blue #1 top
eq2(IBC_COL_X, 0, IBC_W, IBC_H_1000, C_BROWN_IBC, alpha=0.40, zorder=4)
eq2(IBC_COL_X, IBC_H_1000, IBC_W, IBC_H_1000, C_BLUE_IBC, alpha=0.40, zorder=4)

# Far column (front in this view): Waste bottom + Blue #2 top
eq2(IBC_COL_X, 0, IBC_W, IBC_H_1000, C_WASTE_IBC, alpha=0.80, zorder=6)
ax2.text(mx(IBC_COL_X + IBC_W/2), IBC_H_1000/2,
        "IBC-4 Waste\n(bottom, front)", ha="center", va="center",
        fontsize=FS_SM - 1, color="#FFFFFF", zorder=7)
eq2(IBC_COL_X, IBC_H_1000, IBC_W, IBC_H_1000, C_BLUE_IBC, alpha=0.80, zorder=6)
ax2.text(mx(IBC_COL_X + IBC_W/2), IBC_H_1000 + IBC_H_1000/2,
        "IBC-2 Blue\n(top, front)", ha="center", va="center",
        fontsize=FS_SM, color="#FFFFFF", fontweight="bold", zorder=7)
ax2.plot([mx(IBC_COL_X + IBC_W), mx(IBC_COL_X)],
        [IBC_H_1000, IBC_H_1000],
        color="#FFFFFF", lw=0.8, ls="--", alpha=0.7, zorder=8)

ldr2(IBC_COL_X + IBC_W/2 + 400, IBC_H_STK_1000, C_LEN - 50, 2800,
    f"4× IBC 2×2 stack  X={IBC_COL_X}–{IBC_COL_X+IBC_W}mm\n"
    f"(far end, left in this view)", ha="right", fs=FS_SM)

# ── Pinhole-wall equipment — ghost (they face Yd=0, far from this viewpoint) ─
for xw, yw, ww, hw, col, lbl in [
    (EP_X,   EP_H_LO,   EP_W,  EP_H_HI  - EP_H_LO,  C_ELEC, "Elec panel\n[Yd=0 wall]"),
    (BA_X,   BA_H_LO,   BA_W,  BA_H_HI  - BA_H_LO,  C_BATT, "Battery\n[Yd=0]"),
    (EQ_ZONE_X, EQPANEL_Z_LO, EQ_ZONE_W, EQPANEL_Z_HI - EQPANEL_Z_LO, C_PUMP, "Equip panel\n[Yd=1046]"),
    (PWR_PANEL_X, (EP_H_LO + EP_H_HI) / 2 - PWR_PANEL_H / 2,
     PWR_PANEL_W, PWR_PANEL_H, C_ALUM, "Ext pwr panel\n[exterior]"),
]:
    ax2.add_patch(mpatches.FancyBboxPatch(
        (mx(xw + ww), yw), ww, hw, boxstyle="square,pad=0",
        facecolor=col, edgecolor=C_OUT, linewidth=0.7,
        linestyle="--", alpha=0.20, zorder=2))
    ax2.text(mx(xw + ww/2), yw + hw/2, lbl,
            ha="center", va="center", fontsize=FS_SM - 1.5, color=C_DIM,
            alpha=0.6, zorder=3)

# ── Processing tray (304 SS, optical zone floor) ─────────────────────────────
TRAY_X0 = RAIL_X_L + 20     # 170mm
TRAY_X1 = RAIL_X_R - 20     # 4629mm
TRAY_H  = 50                # 50mm rim height
ax2.add_patch(mpatches.FancyBboxPatch(
    (mx(TRAY_X1), 0), TRAY_X1 - TRAY_X0, TRAY_H, boxstyle="square,pad=0",
    facecolor=C_WALL, edgecolor=C_OUT, linewidth=0.8, alpha=0.6, zorder=4))
ax2.text(mx((TRAY_X0 + TRAY_X1) / 2), TRAY_H / 2,
        "Processing tray (304 SS)  —  50mm rim",
        ha="center", va="center", fontsize=FS_SM - 2, color=C_OUT,
        style="italic", zorder=5)

# ── Ventilation fans ──────────────────────────────────────────────────────────
# Fan A (EXHAUST) at X=C_LEN (left edge in this view), H=FAN_A_H=2200 (above IBC)
# Fan B (INTAKE) at X=0 (right edge), H=FAN_B_H=600
FAN_HH = DUCT_HEIGHT
ax2.add_patch(mpatches.Rectangle((0, FAN_A_H - FAN_HH//2), 60, FAN_HH,
             facecolor=C_FAN, edgecolor=C_OUT, linewidth=0.6, alpha=0.8, zorder=6))
ax2.text(30, FAN_A_H, "FAN\nOUT", ha="center", va="center",
        fontsize=FS_SM - 1.5, color=C_OUT, zorder=7)

ax2.add_patch(mpatches.Rectangle((C_LEN - 60, FAN_B_H - FAN_HH//2), 60, FAN_HH,
             facecolor=C_FAN, edgecolor=C_OUT, linewidth=0.6, alpha=0.8, zorder=6))
ax2.text(C_LEN - 30, FAN_B_H, "FAN\nIN", ha="center", va="center",
        fontsize=FS_SM - 1.5, color=C_OUT, zorder=7)

# Fan cross-ventilation arrow — airflow intake (low, right) → exhaust (high, left)
ax2.annotate("", xy=(60, FAN_A_H), xytext=(C_LEN - 60, FAN_B_H),
            arrowprops=dict(arrowstyle="-|>,head_length=1.0,head_width=0.6",
                            color=C_FAN, lw=1.8,
                            linestyle=(0, (6, 3, 1, 3)),
                            connectionstyle="arc3,rad=0.25",
                            mutation_scale=15), zorder=8)
ax2.text((C_LEN)/2 - 1200, (FAN_A_H + FAN_B_H)/2 - 200,
        "Cross-ventilation diagonal\nlow IN → high OUT", ha="center",
        fontsize=FS_SM - 1, color=C_FAN, style="italic", zorder=5)

# ── Safelight ─────────────────────────────────────────────────────────────────
ax2.plot([100, C_LEN - 100], [C_HGT - 100, C_HGT - 100],
        color="#FFD700", lw=2, ls="--", dashes=(8, 5), alpha=0.7, zorder=4)
ax2.text(C_LEN/2, C_HGT - 60, "Overhead safelight strip (Circuit D)",
        ha="center", va="bottom", fontsize=FS_SM - 1, color="#B8960A")

# ── Dimensions ────────────────────────────────────────────────────────────────
DIM_TOP2   = C_HGT + 250
DIM_BOT2   = -250
DIM_LEFT2  = C_LEN + 350   # left in plot = far end (X=C_LEN) in real coords

draw_dim_h(ax2, 0, C_LEN, DIM_TOP2, f"Container length  {C_LEN}mm", offset=80, fs=FS_SM)

dim2h(FP_X_L, FP_X_R, DIM_TOP2 + 200, f"Rail span  {RAIL_SPAN}mm", offset=80, color=RAIL_CLR)

draw_dim_v(ax2, DIM_LEFT2, 0, C_HGT, f"H={C_HGT}mm", offset=80, fs=FS_SM)

ax2.text(C_LEN/2, DIM_BOT2 - 280,
        f"Optical cone illuminates full {FP_W}mm × {C_HGT}mm film plane"
        f"  (X={FP_X_L}–{FP_X_R}mm)  from pinhole at X={PH_X}mm",
        ha="center", va="top", fontsize=FS_SM, color=C_CONE, style="italic")

# Zone width dimension lines — dim2h handles mirroring correctly
# IBC zone: real X = ZONE_R_START–C_LEN  (appears on LEFT in this view)
dim2h(ZONE_R_START, C_LEN, DIM_BOT2 - 80,
      f"IBC zone  {C_LEN - ZONE_R_START}mm",
      offset=70, fs=FS_SM - 0.5, color="#004080")
# Drum zone: real X = 0–ZONE_L_END  (appears on RIGHT in this view)
dim2h(0, ZONE_L_END, DIM_BOT2 - 80,
      f"Drum zone  {ZONE_L_END}mm",
      offset=70, fs=FS_SM - 0.5, color="#805000")

# ── Legend ────────────────────────────────────────────────────────────────────
LEG2_X = C_LEN + 420
LEG2_Y = 2200
LEG_W2 = 600
LEG_H2 = 60
LEG_G2 = 82

legend2 = [
    (C_CONE_L,   "Optical cone (shadow-free projection)"),
    (C_ALUM2,    "Film plane rail (floor & ceiling)"),
    (C_FILM_PLN, "Film plane carriage (symbolic)"),
    (C_BLUE_IBC, "Blue IBC stack x2 (1000L, 1800L total)"),
    (C_BROWN_IBC,"Brown IBC x1 (1000L)"),
    (C_LT_DRUM,  "Revolving light-trap drum"),
    (C_HINGE_PANEL,     "Hinged panel"),
    (C_FAN,      "Ventilation fan (IN / OUT)"),
    (C_PINHOLE,  "Pinhole Ø2.17mm  [ghost = far wall]"),
    (C_ALUM,     "Ext power panel  [ghost = exterior]"),
    (C_WALL,     "Processing tray (304 SS, 50mm rim)"),
]

ax2.text(LEG2_X, LEG2_Y + LEG_H2 + 30, "LEGEND", ha="left", va="bottom",
        fontsize=FS_MD, color=C_OUT, fontweight="bold")
for i, (col, lbl) in enumerate(legend2):
    yy = LEG2_Y - i * LEG_G2
    ax2.add_patch(mpatches.Rectangle((LEG2_X, yy - LEG_H2*0.5), LEG_W2*0.28, LEG_H2*0.7,
                 facecolor=col, edgecolor=C_OUT, linewidth=0.6, zorder=6))
    ax2.text(LEG2_X + LEG_W2*0.34, yy, lbl, ha="left", va="center",
            fontsize=FS_SM, color=C_OUT)

# ── Title block ───────────────────────────────────────────────────────────────
title_block(ax2, "SHEET 2 OF 3",
            drawing_title="ASSEMBLY OVERVIEW",
            subtitle="Film plane side elevation — looking toward pinhole",
            scale_note="1:75 (approx)",
            doc_id="TBS-001 · Assembly Overview")

# ── Save ──────────────────────────────────────────────────────────────────────
out2 = f"{DIAGRAMS_DIR}/assembly-overview-fp.png"
fig2.tight_layout(pad=0)
plt.savefig(out2, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.close(fig2)
print(f"Saved: {out2}")


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 3 — PLAN VIEW: OPERATIONAL vs TRANSPORT MODE
#
# Top-down plan view of the cargo door end (X=0 end), showing two side-by-side
# views:
#   LEFT:  Transport mode  — panel + drum SWUNG ~56° about the Ø89 pivot post,
#          ISO container doors can close.
#   RIGHT: Operational mode — panel at X=0 (closed against the door frame),
#          drum extends out the open doors.
#
# Axes: X (vertical, up = into container) vs Yd (horizontal, 0=near wall).
# ═══════════════════════════════════════════════════════════════════════════════

# ── Palette for plan view ────────────────────────────────────────────────────
C_PANEL_C = "#A8B8A8"    # panel center zone (slightly different)
C_RAIL3   = "#CC4422"    # film-rail / pivot-post accent color
C_CONT_DR = "#9CA0A8"    # container door fill
C_GHOST   = "#D0D0D8"    # ghost position fill

# ── Geometry ─────────────────────────────────────────────────────────────────
# Operational position: panel outer face at X=0 (closed against the door frame)
OP_PANEL_X  = 0
# Transport: the panel + drum REVOLVE SWING_LOCK_DEG (~56°) about the Ø89 pivot
# post at (PIVOT_X, PIVOT_YD) — no slide (rev10, supersedes the HGR20 slide).
TR_SWING_DEG = SWING_LOCK_DEG

# Container exterior face and door thickness
CONT_WALL = 40   # container wall thickness (schematic)
DOOR_T    = 60   # ISO door leaf thickness (schematic)

# Light trap drum center in Yd
LT_DRUM_YD_CENTER = (PANEL_CORNER_YD_L + PANEL_CORNER_YD_R) / 2  # = 1181mm

# How much of the X axis to show — the swing sweeps the panel free edge to
# X≈1970mm into the container, so show enough depth for the full transport swing.
PLAN_X_MAX = 2100  # show X=0 to ~2100mm into container

# ── Figure: two subplots side by side ────────────────────────────────────────
FIG3_W = 24.0
FIG3_H = 12.0

fig3, (ax_tr, ax_op) = plt.subplots(1, 2, figsize=(FIG3_W, FIG3_H), dpi=DPI)
fig3.patch.set_facecolor(BG)

# ── Common drawing helpers ───────────────────────────────────────────────────
def plan_setup(ax, title_text, subtitle_text=""):
    """Configure axes for plan view: Yd horizontal (inverted: far wall left,
    pinhole/near wall right), X vertical (up = into container)."""
    pad_l, pad_r = 200, 200
    pad_b, pad_t = 350, 200
    ax.set_xlim(C_WID + pad_r, -pad_l)   # inverted: far wall on left, pinhole wall on right
    ax.set_ylim(-CONT_WALL - DOOR_T - pad_b, PLAN_X_MAX + pad_t)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor(BG)
    # Title above
    ax.text(C_WID / 2, PLAN_X_MAX + pad_t - 30, title_text,
            ha="center", va="top", fontsize=FS_LG + 1, color=C_OUT,
            fontweight="bold")
    if subtitle_text:
        ax.text(C_WID / 2, PLAN_X_MAX + pad_t - 120, subtitle_text,
                ha="center", va="top", fontsize=FS_SM, color=C_DIM,
                style="italic")


def draw_container_walls(ax):
    """Draw the container long walls and end wall (far end, X=PLAN_X_MAX)."""
    # Near wall (Yd=0)
    ax.add_patch(mpatches.Rectangle((-CONT_WALL, -CONT_WALL), CONT_WALL,
                 PLAN_X_MAX + CONT_WALL, facecolor=C_WALL, edgecolor=C_OUT,
                 linewidth=1.2, zorder=3))
    # Far wall (Yd=C_WID)
    ax.add_patch(mpatches.Rectangle((C_WID, -CONT_WALL), CONT_WALL,
                 PLAN_X_MAX + CONT_WALL, facecolor=C_WALL, edgecolor=C_OUT,
                 linewidth=1.2, zorder=3))
    # Container interior floor area
    ax.add_patch(mpatches.Rectangle((0, 0), C_WID, PLAN_X_MAX,
                 facecolor=C_INTERIOR, edgecolor="none", alpha=0.5, zorder=0))
    # Film plane floor rail at X=RAIL_X_L (= ZONE_L_END = 150mm)
    ax.add_patch(mpatches.Rectangle((0, RAIL_X_L - 10), C_WID, 20,
                 facecolor=C_RAIL3, edgecolor=C_OUT, linewidth=0.5,
                 alpha=0.5, zorder=4))
    ax.text(C_WID / 2, ZONE_L_END + 30,
            f"Film plane floor rail  X={ZONE_L_END}mm",
            ha="center", va="bottom", fontsize=FS_SM - 1, color=C_DIM,
            style="italic", zorder=5)


def _swing(X, Yd, deg):
    """Rotate a physical (X, Yd) point by `deg` about the \u00D889 pivot post; return
    DRAW coords (horizontal = Yd', vertical = X'). deg=0 is the identity."""
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    Xr  = PIVOT_X  + (X - PIVOT_X) * c - (Yd - PIVOT_YD) * s
    Ydr = PIVOT_YD + (X - PIVOT_X) * s + (Yd - PIVOT_YD) * c
    return (Ydr, Xr)


def draw_stepped_panel(ax, panel_x_outer, alpha=0.85, swing_deg=0):
    """Draw the stepped panel in plan view, optionally swung `swing_deg` about
    the pivot. panel_x_outer = X of the panel's exterior face (0 = operational).
    Each zone is a polygon through its 4 rotated corners (deg=0 \u21D2 rectangles).
    When swung, only the SWINGING part (Yd PANEL_CUT_YD..FAR_STRIP_YD0) rotates \u2014
    the fixed near/far strips stay at the door plane (drawn separately), so the
    swung panel is shorter than the full panel width."""
    zones = [
        (0, PANEL_CORNER_YD_L, PANEL_CORNER_T, C_HINGE_PANEL),              # near corner (40mm)
        (PANEL_CORNER_YD_L, PANEL_CORNER_YD_R, PANEL_CENTER_T, C_PANEL_C),  # center (120mm)
        (PANEL_CORNER_YD_R, C_WID, PANEL_CORNER_T, C_HINGE_PANEL),          # far corner (40mm)
    ]
    # clip to the swinging part when swung; full width when operational
    yd_lo, yd_hi = (PANEL_CUT_YD, FAR_STRIP_YD0) if swing_deg else (0, C_WID)
    for yd0, yd1, t, fc in zones:
        y0, y1 = max(yd0, yd_lo), min(yd1, yd_hi)
        if y1 <= y0:
            continue
        x0, x1 = panel_x_outer, panel_x_outer + t
        pts = [_swing(x0, y0, swing_deg), _swing(x1, y0, swing_deg),
               _swing(x1, y1, swing_deg), _swing(x0, y1, swing_deg)]
        ax.add_patch(mpatches.Polygon(pts, closed=True, facecolor=fc,
                     edgecolor=C_OUT, linewidth=1.0, alpha=alpha, zorder=5))


def draw_light_trap_drum(ax, panel_x_outer, swing_deg=0):
    """Draw the revolving light trap drum circle in the panel center zone,
    optionally swung `swing_deg` about the pivot."""
    drum_x_center = panel_x_outer + PANEL_CENTER_T / 2  # centered in 120mm zone
    cdraw = _swing(drum_x_center, LT_DRUM_YD_CENTER, swing_deg)  # (Yd', X')
    ax.add_patch(plt.Circle(cdraw, DRUM_R,
        facecolor=C_LT_DRUM, edgecolor=C_OUT, linewidth=1.0, zorder=6))
    # Center cross
    ax.plot([cdraw[0] - 40, cdraw[0] + 40], [cdraw[1], cdraw[1]],
            color=C_CL, lw=0.7, zorder=7)
    ax.plot([cdraw[0], cdraw[0]], [cdraw[1] - 40, cdraw[1] + 40],
            color=C_CL, lw=0.7, zorder=7)
    ax.text(cdraw[0], cdraw[1] + DRUM_R + 30,
            f"Light trap\n\u00D8{DRUM_D}mm",
            ha="center", va="bottom", fontsize=FS_SM - 0.5, color=C_OUT, zorder=7)


# (draw_waste_drums removed — drums eliminated in rev 5)


def draw_pivot_post(ax):
    """Draw the Ø89 vertical pivot post (the reused film far-left upright) about
    which the panel + drum swing for transport."""
    ax.add_patch(plt.Circle((PIVOT_YD, PIVOT_X), 55,
                 facecolor=C_RAIL3, edgecolor=C_OUT, linewidth=1.2, zorder=7))
    ax.text(PIVOT_YD - 90, PIVOT_X, "Ø89 PIVOT POST",
            ha="right", va="center", fontsize=FS_SM - 1, color=C_OUT,
            fontweight="bold", zorder=8)


# (draw_vgroove_tracks removed — dolly tracks eliminated in rev 5)


def draw_container_doors(ax, closed=True):
    """Draw ISO container doors at X=0 exterior face."""
    if closed:
        # Doors closed — two leaves spanning the full width
        ax.add_patch(mpatches.Rectangle(
            (0, -CONT_WALL - DOOR_T), C_WID / 2, DOOR_T,
            facecolor=C_CONT_DR, edgecolor=C_OUT, linewidth=1.0, zorder=4))
        ax.add_patch(mpatches.Rectangle(
            (C_WID / 2, -CONT_WALL - DOOR_T), C_WID / 2, DOOR_T,
            facecolor=C_CONT_DR, edgecolor=C_OUT, linewidth=1.0, zorder=4))
        ax.text(C_WID / 2, -CONT_WALL - DOOR_T / 2,
                "ISO CONTAINER DOORS (CLOSED)",
                ha="center", va="center", fontsize=FS_SM - 0.5, color=C_OUT,
                fontweight="bold", zorder=5)
    else:
        # Doors open — swung flat against container sides
        # Near-side door
        ax.add_patch(mpatches.Rectangle(
            (-CONT_WALL - DOOR_T, -CONT_WALL), DOOR_T, C_WID / 2 + CONT_WALL,
            facecolor=C_CONT_DR, edgecolor=C_OUT, linewidth=0.8,
            alpha=0.4, zorder=2))
        # Far-side door
        ax.add_patch(mpatches.Rectangle(
            (C_WID + CONT_WALL, -CONT_WALL), DOOR_T, C_WID / 2 + CONT_WALL,
            facecolor=C_CONT_DR, edgecolor=C_OUT, linewidth=0.8,
            alpha=0.4, zorder=2))
        ax.text(C_WID / 2, -CONT_WALL - 30,
                "DOORS OPEN",
                ha="center", va="top", fontsize=FS_SM - 0.5, color=C_DIM,
                style="italic", zorder=3)


# (draw_evap_cooler removed — evap cooler is now external)


# ── LEFT PANEL: Transport mode ──────────────────────────────────────────────
plan_setup(ax_tr, "TRANSPORT MODE",
           f"Panel + drum swung {TR_SWING_DEG}° about the pivot  |  Doors closed")
draw_container_walls(ax_tr)
draw_container_doors(ax_tr, closed=True)
draw_pivot_post(ax_tr)

# Ghost: operational (0°) panel position (dashed outline)
for yd0, w, t in [(0, PANEL_CORNER_YD_L, PANEL_CORNER_T),
                   (PANEL_CORNER_YD_L, PANEL_CENTER_W, PANEL_CENTER_T),
                   (PANEL_CORNER_YD_R, C_WID - PANEL_CORNER_YD_R, PANEL_CORNER_T)]:
    ax_tr.add_patch(mpatches.Rectangle(
        (yd0, OP_PANEL_X), w, t,
        facecolor="none", edgecolor=C_GHOST, linewidth=0.8,
        ls=(0, (4, 3)), alpha=0.6, zorder=2))

# Solid: swung (transport) position — panel + drum revolved about the pivot
draw_stepped_panel(ax_tr, OP_PANEL_X, swing_deg=TR_SWING_DEG)
draw_light_trap_drum(ax_tr, OP_PANEL_X, swing_deg=TR_SWING_DEG)

# Fixed strips (Yd 0..PANEL_CUT_YD near, FAR_STRIP_YD0..C_WID far) do NOT swing —
# the cargo doors close outboard of the fixed near strip.
for (y0, y1) in [(0, PANEL_CUT_YD), (FAR_STRIP_YD0, C_WID)]:
    ax_tr.add_patch(mpatches.Rectangle(
        (y0, OP_PANEL_X), y1 - y0, PANEL_CORNER_T,
        facecolor=C_HINGE_PANEL, edgecolor=C_OUT, linewidth=1.0,
        alpha=0.95, zorder=6))

# Door closure plane line
ax_tr.plot([0, C_WID], [-CONT_WALL, -CONT_WALL], color="#CC2020", lw=1.2,
           ls="--", dashes=(6, 3), zorder=8)
ax_tr.text(C_WID + 250, -CONT_WALL, "Door closure\nplane",
           ha="left", va="center", fontsize=FS_SM - 1, color="#CC2020", zorder=8)

# Swing arc — from the fixed-panel edge (Yd=PANEL_CUT_YD) to the swung tip, tracing
# the swinging part's free corner from 0° to the lock angle
arc_pts = [_swing(OP_PANEL_X, PANEL_CUT_YD, dd) for dd in range(0, TR_SWING_DEG + 1, 3)]
ax_tr.plot([p[0] for p in arc_pts], [p[1] for p in arc_pts],
           color="#2060A0", lw=1.5, ls=(0, (5, 3)), zorder=8)
arc_mid = arc_pts[int(len(arc_pts) * 0.6)]
ax_tr.annotate(f"SWING {TR_SWING_DEG}°",
               xy=arc_mid, xytext=(arc_mid[0] + 280, arc_mid[1] + 120),
               fontsize=FS_SM + 1, color="#2060A0", fontweight="bold",
               arrowprops=dict(arrowstyle="-|>", color="#2060A0", lw=1.3),
               zorder=9)


# ── RIGHT PANEL: Operational mode ────────────────────────────────────────────
plan_setup(ax_op, "OPERATIONAL MODE",
           "Panel at X=0  |  Doors open")
draw_container_walls(ax_op)
draw_container_doors(ax_op, closed=False)
draw_pivot_post(ax_op)

# Solid: operational positions
draw_stepped_panel(ax_op, OP_PANEL_X)
draw_light_trap_drum(ax_op, OP_PANEL_X)

# Door closure plane line (for reference)
ax_op.plot([0, C_WID], [-CONT_WALL, -CONT_WALL], color="#CC2020", lw=0.8,
           ls=":", alpha=0.5, zorder=2)

# Light trap drum overhang — show it extends past X=0
lt_drum_cx = OP_PANEL_X + PANEL_CENTER_T / 2
lt_drum_x_outer = lt_drum_cx - DRUM_R
ax_op.text(LT_DRUM_YD_CENTER, lt_drum_x_outer + 150,
           f"Drum extends {abs(lt_drum_x_outer):.0f}mm\npast exterior face",
           ha="center", va="top", fontsize=FS_SM - 1, color="#CC2020",
           style="italic", zorder=8)

# Fixed door frame
ax_op.plot([0, C_WID], [0, 0], color=C_OUT, lw=1.8, zorder=7)
ax_op.text(C_WID + 320, 0, "Fixed door\nframe (X=0)",
           ha="left", va="center", fontsize=FS_SM - 1, color=C_OUT, zorder=8)

# EPDM seal indicator
ax_op.plot([10, C_WID - 10], [-3, -3], color="#5A3020", lw=2.5,
           solid_capstyle="round", zorder=7)
ax_op.text(C_WID - 160, 15, "EPDM seal",
           ha="left", va="center", fontsize=FS_SM - 1, color="#5A3020", zorder=8)

# Panel thickness dims
draw_dim_v(ax_op, PANEL_CORNER_YD_L / 2, OP_PANEL_X,
           OP_PANEL_X + PANEL_CORNER_T, f"{PANEL_CORNER_T}mm",
           offset=60, fs=FS_SM - 1)
draw_dim_v(ax_op, LT_DRUM_YD_CENTER, OP_PANEL_X,
           OP_PANEL_X + PANEL_CENTER_T, f"{PANEL_CENTER_T}mm",
           offset=60, fs=FS_SM - 1, right=True)

# Cam latch indicators (4x, interior face) — label to the left with leader lines
latch_yds = [200, PANEL_CORNER_YD_L, PANEL_CORNER_YD_R, C_WID - 200]
latch_label_x = -CONT_WALL - DOOR_T - 250  # below the door closure plane
latch_label_yd = -120  # left of container wall
for yd in latch_yds:
    t = PANEL_CORNER_T if (yd < PANEL_CORNER_YD_L or yd > PANEL_CORNER_YD_R) else PANEL_CENTER_T
    ax_op.plot(yd, OP_PANEL_X + t - 5, marker="x", markersize=5,
              color="#CC2020", mew=1.2, zorder=8)
    # Leader line: 45° diagonal from latch marker, then horizontal to label
    latch_top = OP_PANEL_X + t - 5
    drop = latch_top - latch_label_x  # vertical distance to shared line
    diag_yd = yd - drop              # 45° means equal horizontal and vertical offset
    ax_op.plot([yd, diag_yd, latch_label_yd], [latch_top, latch_label_x, latch_label_x],
              color="#CC2020", lw=0.6, zorder=7)
ax_op.text(latch_label_yd, latch_label_x - 40,
           "Cam latches \u00d74\n(Southco C2-33, interior face)",
           ha="left", va="top", fontsize=FS_SM - 0.5, color="#CC2020", zorder=8)


# ── Shared legend (bottom center of figure) ─────────────────────────────────
legend_items3 = [
    (C_HINGE_PANEL,    "Panel corner zone (40mm)"),
    (C_PANEL_C,  "Panel center zone (120mm)"),
    (C_LT_DRUM, "Revolving light trap drum"),
    (C_CONT_DR,  "ISO container door"),
    (C_GHOST,    "Ghost (operational position)"),
]

# Draw legend as a horizontal row at the top of the figure
fig3.subplots_adjust(bottom=0.07, top=0.90)
leg_ax = fig3.add_axes([0.05, 0.92, 0.9, 0.04])
leg_ax.set_xlim(0, 1)
leg_ax.set_ylim(0, 1)
leg_ax.axis("off")

n_items = len(legend_items3)
item_w = 1.0 / n_items
for i, (col, lbl) in enumerate(legend_items3):
    cx = i * item_w + item_w * 0.08
    leg_ax.add_patch(mpatches.Rectangle(
        (cx, 0.35), item_w * 0.12, 0.35,
        facecolor=col, edgecolor=C_OUT, linewidth=0.5, transform=leg_ax.transAxes))
    leg_ax.text(cx + item_w * 0.16, 0.52, lbl,
                ha="left", va="center", fontsize=FS_SM - 0.5, color=C_OUT,
                transform=leg_ax.transAxes)

# ── Title block (full-figure overlay) ─────────────────────────────────────────
ax_tb3 = fig3.add_axes([0, 0, 1, 1], facecolor="none")
ax_tb3.axis("off")
title_block(ax_tb3, "SHEET 3 OF 3",
            drawing_title="ASSEMBLY OVERVIEW",
            subtitle="Plan view — cargo door end",
            scale_note="1:20 (approx)",
            doc_id="TBS-001 · Assembly Overview")

# ── Save ──────────────────────────────────────────────────────────────────────
out3 = f"{DIAGRAMS_DIR}/assembly-overview-plan.png"
plt.savefig(out3, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.close(fig3)
print(f"Saved: {out3}")
