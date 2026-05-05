#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_assembly_overview.py

Generates diagrams/assembly-overview.png — high-level schematic side-elevation
of the TBS-001 container interior (redesigned film-plane-reduction layout).

View direction: looking at the near long wall (Y=0 face) from outside.
  X (horizontal) = 0–5893 mm  (container long axis; left=cargo door, right=far end)
  H (vertical)   = 0–2388 mm  (container height)
  Yd (into page) = 0–2362 mm  (optical depth; not a diagram axis)

Zones (shadow-free proof):
  Left end zone:   X = 0–1,100 mm   (drum + evap cooler + 55-gal drums stacked)
  Optical zone:    X = 1,100–4,649 mm  (film plane only)
  Right end zone:  X = 4,649–5,893 mm  (IBCs only, right-justified)
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

from tbs_constants import (
    C_LEN, C_WID, C_HGT,
    FP_X_L, FP_X_R, FP_Y, FP_W,
    PH_X, PH_H, PH_FNO,
    ZONE_L_END, ZONE_R_START,
    DRUM_CX, DRUM_D, DRUM_R, DRUM_H_LT,
    EVAP_X, EVAP_W, EVAP_H, EVAP_Y, EVAP_D,
    EP_X, EP_W, EP_H_LO, EP_H_HI,
    BA_X, BA_W, BA_H_LO, BA_H_HI,
    PUMP_X, PUMP_W, PUMP_H_LO, PUMP_H_HI,
    IBC_COL_X, IBC_W, IBC_D, IBC_H_STK, IBC_H_600,
    BLUE_IBC_Y, BROWN_IBC_Y,
    DRUM_EQ_D, DRUM_EQ_H, DRUM_EQ_R,
    DRUM_LZ_CX, DRUM_FZ_CX,
    DRUM_LZ_YD_LO, DRUM_FZ_YD_LO,
    PANEL_CORNER_T, PANEL_CENTER_T,
    PANEL_CORNER_YD_L, PANEL_CORNER_YD_R, PANEL_CENTER_W,
    PANEL_SLIDE, DRUM_SLIDE,
    PERM_TRACK_END, BRIDGE_TRACK_START, BRIDGE_TRACK_END,
    RAIL_X_L, RAIL_X_R, RAIL_SPAN,
    FAN_A_H, FAN_B_H, FAN_DIAM, DUCT_HEIGHT,
    DIAGRAMS_DIR, SVG_DIR, svg_path,
    C_OUT, C_CL, C_DIM,
    cone_left, cone_right,
)

os.makedirs(DIAGRAMS_DIR, exist_ok=True)
os.makedirs(SVG_DIR, exist_ok=True)

# ── Constants shared with previous session ────────────────────────────────────
RAIL_OFF   = 100    # floor offset for all floor-standing equipment (mm)
DRUM_H_ELV = DRUM_H_LT   # 2000mm — revolving drum height in elevation view

# ── Palette ───────────────────────────────────────────────────────────────────
BG        = "#FFFFFF"
C_INTERIOR = "#F4F4F4"
C_WALL    = "#B0B0B8"
C_ZONE_L  = "#FFF0E0"   # left end zone (orange tint)
C_ZONE_O  = "#F0FFF0"   # optical zone (green tint)
C_ZONE_R  = "#E8F0FF"   # right end zone (blue tint)

C_IBC_BLUE  = "#4A90D9"
C_IBC_BROWN = "#9C7A3C"
C_DRUM_EQ   = "#7A6B5A"
C_EVAP      = "#3DAA96"
C_PUMP      = "#E8884A"
C_ELEC      = "#F5C518"
C_BATT      = "#6A5ACD"
C_FILM_PLN  = "#B8D4E8"
C_PINHOLE   = "#CC2020"
C_DOOR      = "#C8C8C0"
C_FAN       = "#A0A0A8"
C_DRUM_LT   = "#E8E8D0"   # revolving light-trap drum fill

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
def draw_dim_h(ax, x1, x2, y, label, offset=80, fs=FS_SM, color=C_DIM):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.8))
    ax.plot([x1, x1], [y - offset*0.3, y + offset*0.3], color=color, lw=0.6)
    ax.plot([x2, x2], [y - offset*0.3, y + offset*0.3], color=color, lw=0.6)
    ax.text((x1+x2)/2, y + offset*0.55, label, ha="center", va="bottom",
            fontsize=fs, color=color)

def draw_dim_v(ax, x, y1, y2, label, offset=80, fs=FS_SM, color=C_DIM):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.8))
    ax.plot([x-offset*0.3, x+offset*0.3], [y1, y1], color=color, lw=0.6)
    ax.plot([x-offset*0.3, x+offset*0.3], [y2, y2], color=color, lw=0.6)
    ax.text(x - offset*0.6, (y1+y2)/2, label, ha="right", va="center",
            fontsize=fs, color=color, rotation=90)

def leader(ax, x_tip, y_tip, x_txt, y_txt, label, fs=FS_SM, color=C_OUT, ha="left"):
    ax.annotate(label, xy=(x_tip, y_tip), xytext=(x_txt, y_txt),
                fontsize=fs, color=color, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color=color, lw=0.7,
                                connectionstyle="arc3,rad=0.0"))

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


# ── LEFT END ZONE — revolving drum + evap cooler ──────────────────────────────

# Hinged panel — stepped profile (rev 4): 40mm corner zones, 120mm center zone.
# In this side elevation (X-H plane), the stepped depth is visible.
# Corner zones (majority of panel width) shown at 40mm depth inside X=0.
# Center zone (drum housing, Yd=756-1606) shown at 120mm depth.
# Container wall (40mm steel) drawn outside at X=-40 to 0.
ax.add_patch(mpatches.Rectangle((-40, 0), 40, C_HGT,
             facecolor=C_DOOR, edgecolor=C_OUT, linewidth=0.8, alpha=0.5, zorder=4))
# Corner zone panel (40mm, X=0 to 40) — visible in side elevation as dominant depth
ax.add_patch(mpatches.Rectangle((0, 0), PANEL_CORNER_T, C_HGT,
             facecolor=C_DOOR, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=4))
# Center zone panel (120mm, X=0 to 120) — shown as dashed outline behind corner
ax.add_patch(mpatches.Rectangle((0, 0), PANEL_CENTER_T, C_HGT,
             facecolor="none", edgecolor=C_OUT, linewidth=0.6, ls=(0, (4, 3)),
             alpha=0.5, zorder=4))

# Revolving drum: centre at X=0 (outside edge of container), bottom at Y=RAIL_OFF
# In this side elevation appears as a rectangle Ø750mm wide × 2000mm tall.
ax.add_patch(mpatches.Rectangle((-DRUM_R, RAIL_OFF), DRUM_D, DRUM_H_ELV,
             facecolor=C_DRUM_LT, edgecolor=C_OUT, linewidth=0.8, alpha=0.9, zorder=5))
# Centre line through drum
ax.plot([DRUM_CX, DRUM_CX], [RAIL_OFF, RAIL_OFF + DRUM_H_ELV + 100],
        color=C_CL, lw=0.7, ls="--", dashes=(6, 3), zorder=6)
leader(ax, DRUM_CX, RAIL_OFF + DRUM_H_ELV + 60, -200, PH_H + 1250,
       f"Hinged panel +\nRevolving drum  VERTICAL AXIS\nO{DRUM_D}mm x {DRUM_H_ELV}mm H",
       ha="right", fs=FS_SM)

# Evap cooler: X=400-1000, bottom at RAIL_OFF, height EVAP_H=800
equip_rect(ax, EVAP_X, RAIL_OFF, EVAP_W, EVAP_H, C_EVAP, zorder=4)
ax.text(EVAP_X + EVAP_W/2, RAIL_OFF + EVAP_H/2,
        "Evap\ncooler", ha="center", va="center",
        fontsize=FS_SM - 0.5, color="#FFFFFF", zorder=6)

leader(ax, EVAP_X + EVAP_W/2, RAIL_OFF + EVAP_H, 1200, 1100,
       f"Evap cooler\nX={EVAP_X}–{EVAP_X+EVAP_W}mm", ha="left", fs=FS_SM)

# Black-water drums — 2× 55-gal, one per Yd corner (rev 4: on slide dollies).
# In this side elevation both drums share X → collapse to single block.
# Left edge flush with corner panel inner face (X=PANEL_CORNER_T=40mm),
# right edge 5mm inside ZONE_L_END.
_drum_x0 = PANEL_CORNER_T   # = 40mm — left edge flush with corner panel inner face
_drum_vis_x = -DRUM_R + DRUM_D        # = 375mm — revolving drum right edge (inside container)
equip_rect(ax, _drum_x0, RAIL_OFF, DRUM_EQ_D, DRUM_EQ_H, C_DRUM_EQ, alpha=0.80, zorder=5)
ax.text(_drum_vis_x + (_drum_x0 + DRUM_EQ_D - _drum_vis_x) / 2, RAIL_OFF + DRUM_EQ_H/2,
        "Waste\ndrums\n×2", ha="center", va="center",
        fontsize=FS_SM - 0.5, color="#FFFFFF", zorder=5)
leader(ax, _drum_x0 + DRUM_EQ_D, RAIL_OFF + DRUM_EQ_H * 0.6, 800, 1500,
       f"55-gal drums ×2 (on slide dollies — one per Yd corner)\n"
       f"D-1 near: Yd=0–{DRUM_EQ_D}mm  |  D-2 far: Yd={C_WID-DRUM_EQ_D}–{C_WID}mm\n"
       f"X={_drum_x0}–{_drum_x0+DRUM_EQ_D}mm  H={DRUM_EQ_H}mm each",
       ha="left", fs=FS_SM)


# ── PINHOLE WALL EQUIPMENT — flush-mount on near long wall (Yd=0 face) ────────

# Electrical panel: X=2050-2350, H=900-1500
equip_rect(ax, EP_X, EP_H_LO, EP_W, EP_H_HI - EP_H_LO, C_ELEC, ec=C_OUT, lw=1.0, zorder=4)
ax.text(EP_X + EP_W/2, (EP_H_LO + EP_H_HI)/2,
        "Elec\npanel", ha="center", va="center",
        fontsize=FS_SM - 1, color=C_OUT, zorder=6)

# Battery bank: X=2050-2550, H=100-600
equip_rect(ax, BA_X, BA_H_LO, BA_W, BA_H_HI - BA_H_LO, C_BATT, zorder=4)
ax.text(BA_X + BA_W/2, (BA_H_LO + BA_H_HI)/2,
        "Battery\nbank", ha="center", va="center",
        fontsize=FS_SM - 1, color="#FFFFFF", zorder=6)

# Pump manifold: X=2400-2700, H=200-600
equip_rect(ax, PUMP_X, PUMP_H_LO, PUMP_W, PUMP_H_HI - PUMP_H_LO, C_PUMP, zorder=4)
ax.text(PUMP_X + PUMP_W/2, (PUMP_H_LO + PUMP_H_HI)/2,
        "Pump", ha="center", va="center",
        fontsize=FS_SM - 1, color="#FFFFFF", zorder=6)

leader(ax, EP_X + EP_W, (EP_H_LO + EP_H_HI)/2, EP_X + 500, 2000,
       f"Electrical panel\n(wall-mount, Yd=0 face)\nX={EP_X}–{EP_X+EP_W}mm",
       ha="left", fs=FS_SM)
leader(ax, BA_X, (BA_H_LO + BA_H_HI)/4, BA_X - 500, 400,
       f"Battery bank\nX={BA_X}–{BA_X+BA_W}mm", ha="left", fs=FS_SM)
leader(ax, PUMP_X + PUMP_W, (PUMP_H_LO + PUMP_H_HI)/2, PUMP_X + 700, 500,
       f"Pump manifold\nX={PUMP_X}–{PUMP_X+PUMP_W}mm", ha="left", fs=FS_SM)


# ── RIGHT END ZONE — IBC column + drum column ─────────────────────────────────

# IBC column: Blue (front, Y-stacked) and Brown (rear, Y-stacked behind Blue)
# In this side elevation (depth into page) both occupy X=4044–5263.
# Blue IBC stack ×2 (2020mm tall) at front; Brown IBC ×1 (1010mm tall) behind.
# Draw Brown first (slightly dimmer / different alpha), then Blue on top.

# Brown IBC ×1 (behind Blue, dimmer)
equip_rect(ax, IBC_COL_X, RAIL_OFF, IBC_W, IBC_H_600, C_IBC_BROWN, alpha=0.60, zorder=3)
ax.text(IBC_COL_X + IBC_W/2, RAIL_OFF + IBC_H_600/2,
        "Brown IBC x1\n(600L, behind)",
        ha="center", va="center", fontsize=FS_SM - 1, color="#FFFFFF", zorder=4)

# Blue IBC stack ×2 (front, on top)
equip_rect(ax, IBC_COL_X, RAIL_OFF, IBC_W, IBC_H_STK, C_IBC_BLUE, alpha=0.80, zorder=5)
ax.text(IBC_COL_X + IBC_W/2, RAIL_OFF + IBC_H_STK/2,
        "Blue IBC x2\nstacked (front)\n2x600L",
        ha="center", va="center", fontsize=FS_SM, color="#FFFFFF",
        fontweight="bold", zorder=6)
# Stacking line
ax.plot([IBC_COL_X, IBC_COL_X + IBC_W], [RAIL_OFF + IBC_H_600, RAIL_OFF + IBC_H_600],
        color="#FFFFFF", lw=0.8, ls="--", alpha=0.7, zorder=7)

leader(ax, IBC_COL_X + IBC_W/2, RAIL_OFF + IBC_H_STK, 6300, 2750,
       f"IBC column  X={IBC_COL_X}–{IBC_COL_X+IBC_W}mm\n"
       f"Blue: 2x600L stacked H={IBC_H_STK}mm (front)\n"
       f"Brown: 1x600L H={IBC_H_600}mm (behind, Y-depth)",
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
       f"Pinhole  O2.17mm\n(X={PH_X}, H={PH_H}mm)\nf/1088",
       ha="left", fs=FS_SM, color=C_PINHOLE)
ax.text(PH_X, PH_H - 300, "Optical axis (into page)\nFocal length 2362mm",
        ha="center", va="top", fontsize=FS_SM, color=C_CL, style="italic")


# ── Ventilation fans ──────────────────────────────────────────────────────────
# Fan A — INTAKE: far end wall (X=C_LEN), low position (H=FAN_A_H=600mm)
# Fan B — EXHAUST: cargo door end wall (X=0), high position (H=FAN_B_H=1800mm)
FAN_HH = DUCT_HEIGHT  # duct opening height (200mm) — same as hatch block height
ax.add_patch(mpatches.Rectangle((C_LEN - 60, FAN_A_H - FAN_HH // 2), 60, FAN_HH,
             facecolor=C_FAN, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=4))
ax.text(C_LEN - 30, FAN_A_H, "FAN\nIN", ha="center", va="center",
        fontsize=FS_SM - 1.5, color=C_OUT, zorder=5)

ax.add_patch(mpatches.Rectangle((0, FAN_B_H - FAN_HH // 2), 60, FAN_HH,
             facecolor=C_FAN, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=4))
ax.text(30, FAN_B_H, "FAN\nOUT", ha="center", va="center",
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

draw_dim_h(ax, 0, C_LEN, DIM_TOP, f"Container length  {C_LEN}mm", offset=100)
draw_dim_h(ax, ZONE_L_END, ZONE_R_START, DIM_TOP + 200,
           f"Optical zone  {ZONE_R_START-ZONE_L_END}mm", offset=80, color=C_CL)
draw_dim_h(ax, FP_X_L, FP_X_R, DIM_TOP + 360,
           f"Film plane  {FP_X_R-FP_X_L}mm", offset=80, color=C_CL)
draw_dim_v(ax, DIM_RIGHT,        0, C_HGT, f"H={C_HGT}mm",     offset=100)
draw_dim_v(ax, DIM_RIGHT + 300,  0, PH_H,  f"PH H={PH_H}mm",   offset=100)

# Left / right zone widths
draw_dim_h(ax, 0, ZONE_L_END, DIM_BOT - 80,
           f"L zone\n{ZONE_L_END}mm", offset=60, fs=FS_SM - 0.5, color="#805000")
draw_dim_h(ax, ZONE_R_START, C_LEN, DIM_BOT - 80,
           f"R zone\n{C_LEN-ZONE_R_START}mm", offset=60, fs=FS_SM - 0.5, color="#004080")

ax.text(C_LEN/2, DIM_BOT - 300,
        f"All equipment in shadow-free end zones (X<{ZONE_L_END} or X>{ZONE_R_START}) or on pinhole wall (Yd=0)",
        ha="center", va="top", fontsize=FS_SM, color="#004020", style="italic")


# ── Legend ────────────────────────────────────────────────────────────────────
LEG_X   = C_LEN + 420
LEG_Y   = 2200
LEG_W   = 600
LEG_H   = 60
LEG_GAP = 82

legend_items = [
    (C_IBC_BLUE,  "Blue IBC stack x2 (2x600L)"),
    (C_IBC_BROWN, "Brown IBC x1 (600L)"),
    (C_DRUM_EQ,   "55-gal drums x2"),
    (C_EVAP,      "Evaporative cooler"),
    (C_PUMP,      "Pump manifold"),
    (C_ELEC,      "Electrical panel"),
    (C_BATT,      "Battery bank"),
    (C_FILM_PLN,  "Film plane (symbolic band)"),
    (C_PINHOLE,   "Pinhole O2.17mm"),
    (C_DOOR,      "Hinged panel + drum"),
    (C_FAN,       "Ventilation fan"),
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
TB_X = C_LEN + 420
TB_Y = -450
TB_W = 1380
TB_H = 420

ax.add_patch(mpatches.Rectangle((TB_X, TB_Y), TB_W, TB_H,
             facecolor="#F8F8F8", edgecolor=C_OUT, linewidth=1.0))
ax.add_patch(mpatches.Rectangle((TB_X, TB_Y + 280), TB_W, TB_H - 280,
             facecolor="#E0E0E8", edgecolor=C_OUT, linewidth=0.6))
ax.text(TB_X + TB_W/2, TB_Y + 360, "TBS-001",
        ha="center", va="center", fontsize=FS_LG + 2, color=C_OUT, fontweight="bold")
ax.text(TB_X + TB_W/2, TB_Y + 305, "ASSEMBLY — SIDE ELEVATION",
        ha="center", va="center", fontsize=FS_MD, color=C_OUT)
ax.text(TB_X + 20, TB_Y + 240, "Scale: 1:75 (approx)",
        ha="left", va="center", fontsize=FS_SM, color=C_DIM)
ax.text(TB_X + 20, TB_Y + 180,
        f"Container: {C_LEN}L x {C_WID}W x {C_HGT}H (mm interior)",
        ha="left", va="center", fontsize=FS_SM, color=C_DIM)
ax.text(TB_X + 20, TB_Y + 120,
        f"Pinhole: X={PH_X}mm  H={PH_H}mm  f/1088  Focal length {C_WID}mm",
        ha="left", va="center", fontsize=FS_SM, color=C_DIM)
ax.text(TB_X + 20, TB_Y + 60,
        "View: near long wall (+Y direction). Optical axis perpendicular to page.",
        ha="left", va="center", fontsize=FS_SM - 0.5, color=C_DIM)
ax.text(TB_X + TB_W - 20, TB_Y + 0, "© 2026 Alvin Richards — GNU AGPLv3",
        ha="right", va="bottom", fontsize=FS_SM - 1, color=C_DIM, style="italic")


# ── Save ──────────────────────────────────────────────────────────────────────
out = f"{DIAGRAMS_DIR}/assembly-overview.png"
fig.tight_layout(pad=0)
plt.savefig(out, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
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
    ax2.annotate(label, xy=(mx(x_tip), y_tip), xytext=(mx(x_txt), y_txt),
                fontsize=fs, color=color, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color=color, lw=0.7,
                                connectionstyle="arc3,rad=0.0"))

def dim2h(x1, x2, y, label, offset=80, fs=FS_SM, color=C_DIM):
    """Horizontal dimension in mirrored coords (x1 < x2 in real space)."""
    px1, px2 = mx(x2), mx(x1)   # note swap: real x1 → right plot edge
    ax2.annotate("", xy=(px2, y), xytext=(px1, y),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.8))
    ax2.plot([px1, px1], [y - offset*0.3, y + offset*0.3], color=color, lw=0.6)
    ax2.plot([px2, px2], [y - offset*0.3, y + offset*0.3], color=color, lw=0.6)
    ax2.text((px1+px2)/2, y + offset*0.55, label, ha="center", va="bottom",
            fontsize=fs, color=color)

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

# Rail centre lines
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
ldr2(PH_X, PH_H, PH_X - 600, PH_H + 500,
    f"Pinhole  Ø2.17mm\n(X={PH_X}, H={PH_H}mm)\n[on far wall — ghost]",
    ha="right", fs=FS_SM, color=C_PINHOLE)
ax2.text(mx(PH_X), PH_H - 320,
        "Optical axis (out of page)\nFocal length 2,362mm",
        ha="center", va="top", fontsize=FS_SM, color=C_CL, style="italic")

# Rail labels
ldr2(RAIL_X_L, RAIL_OFF + 300, RAIL_X_L + 650, 600,
    f"Floor rail  X={RAIL_X_L}mm\n(left rail, cargo-door side)", ha="left", fs=FS_SM, color=RAIL_CLR)
ldr2(RAIL_X_R, C_HGT - 300, RAIL_X_R - 650, C_HGT - 600,
    f"Floor rail  X={RAIL_X_R}mm\n(right rail, far-end side)", ha="right", fs=FS_SM, color=RAIL_CLR)

# ── LEFT END ZONE (appears on RIGHT in this view) — drum, evap, waste drums ──
# Hinged panel — stepped profile (rev 4): container wall outside, then
# corner zones (40mm) and center zone (120mm) inside.
ax2.add_patch(mpatches.Rectangle((C_LEN, 0), 40, C_HGT,
             facecolor=C_DOOR, edgecolor=C_OUT, linewidth=0.8, alpha=0.5, zorder=4))
# Corner zone (40mm inside)
ax2.add_patch(mpatches.Rectangle((C_LEN - PANEL_CORNER_T, 0), PANEL_CORNER_T, C_HGT,
             facecolor=C_DOOR, edgecolor=C_OUT, linewidth=0.6, alpha=0.4, zorder=4))
# Center zone outline (120mm inside, dashed — deeper zone behind)
ax2.add_patch(mpatches.Rectangle((C_LEN - PANEL_CENTER_T, 0), PANEL_CENTER_T, C_HGT,
             facecolor="none", edgecolor=C_OUT, linewidth=0.6, ls=(0, (4, 3)),
             alpha=0.4, zorder=4))

# Revolving drum
ax2.add_patch(mpatches.Rectangle((C_LEN - DRUM_D, RAIL_OFF), DRUM_D, DRUM_H_ELV,
             facecolor=C_DRUM_LT, edgecolor=C_OUT, linewidth=0.8, alpha=0.9, zorder=5))
ax2.plot([C_LEN, C_LEN], [RAIL_OFF, RAIL_OFF + DRUM_H_ELV + 100],
        color=C_CL, lw=0.7, ls="--", dashes=(6, 3), zorder=6)

# Evap cooler (ghost — at Yd=0)
eq2(EVAP_X, RAIL_OFF, EVAP_W, EVAP_H, C_EVAP, alpha=0.30, zorder=3,
    ec="#3DAA96", lw=0.7)
ax2.text(mx(EVAP_X + EVAP_W/2), RAIL_OFF + EVAP_H/2,
        "Evap\ncooler\n[Yd=0]", ha="center", va="center",
        fontsize=FS_SM - 1.5, color="#3DAA96", alpha=0.7, zorder=4)

# Waste drums: two 55-gal drums, same X column, different Yd.
# Left edge flush with corner panel inner face (X=PANEL_CORNER_T=40mm).
# From this viewpoint (Yd=2362 looking toward Yd=0):
#   DRUM_LZ (Yd=0–580mm)      — behind the revolving drum → ghost, low zorder
#   DRUM_FZ (Yd=1782–2362mm)  — in front of the revolving drum → solid, high zorder
_dlx0 = PANEL_CORNER_T   # = 40mm — left edge flush with corner panel inner face

# D-1 (far from viewer — ghost, behind light trap drum)
eq2(_dlx0, RAIL_OFF, DRUM_EQ_D, DRUM_EQ_H, C_DRUM_EQ, alpha=0.20, zorder=4,
    ec="#7A6B5A", lw=0.6)

# Revolving light trap drum drawn at zorder=5 (above D-1 ghost)

# D-2 (close to viewer — solid, in front of light trap drum)
_dfx0 = PANEL_CORNER_T   # = 40mm — same X as D-1
eq2(_dfx0, RAIL_OFF, DRUM_EQ_D, DRUM_EQ_H, C_DRUM_EQ, alpha=0.85, zorder=7,
    ec="#7A6B5A", lw=1.0)
ax2.text(mx(_dfx0 + DRUM_EQ_D / 2), RAIL_OFF + DRUM_EQ_H / 2,
        "Waste\ndrum D-2\n(front)",
        ha="center", va="center", fontsize=FS_SM - 1, color="#3D2E22", zorder=8)

ldr2(0, RAIL_OFF + DRUM_H_ELV * 0.3, -750, 900,
    "Hinged panel +\nRevolving drum  Ø{0}mm × {1}mm H\n(cargo door, right in this view)".format(DRUM_D, DRUM_H_ELV),
    ha="left", fs=FS_SM)

# ── RIGHT END ZONE (appears on LEFT in this view) — IBCs ─────────────────────
eq2(IBC_COL_X, RAIL_OFF, IBC_W, IBC_H_600, C_IBC_BROWN, alpha=0.60, zorder=6)
ax2.text(mx(IBC_COL_X + IBC_W/2), RAIL_OFF + IBC_H_600/2,
        "Brown IBC x1\n(600L, behind)", ha="center", va="center",
        fontsize=FS_SM - 1, color="#FFFFFF", zorder=6)

eq2(IBC_COL_X, RAIL_OFF, IBC_W, IBC_H_STK, C_IBC_BLUE, alpha=0.80, zorder=5)
ax2.text(mx(IBC_COL_X + IBC_W/2), RAIL_OFF + IBC_H_STK/2 + 200,
        "Blue IBC x2\nstacked (front)\n2×600L", ha="center", va="center",
        fontsize=FS_SM, color="#FFFFFF", fontweight="bold", zorder=6)
ax2.plot([mx(IBC_COL_X + IBC_W), mx(IBC_COL_X)],
        [RAIL_OFF + IBC_H_600, RAIL_OFF + IBC_H_600],
        color="#FFFFFF", lw=0.8, ls="--", alpha=0.7, zorder=7)

ldr2(IBC_COL_X + IBC_W/2 + 400, RAIL_OFF + IBC_H_STK, C_LEN - 50, 2800,
    f"IBC column  X={IBC_COL_X}–{IBC_COL_X+IBC_W}mm\n"
    f"(far end, left in this view)", ha="right", fs=FS_SM)

# ── Pinhole-wall equipment — ghost (they face Yd=0, far from this viewpoint) ─
for xw, yw, ww, hw, col, lbl in [
    (EP_X,   EP_H_LO,   EP_W,  EP_H_HI  - EP_H_LO,  C_ELEC, "Elec panel\n[Yd=0 wall]"),
    (BA_X,   BA_H_LO,   BA_W,  BA_H_HI  - BA_H_LO,  C_BATT, "Battery\n[Yd=0]"),
    (PUMP_X, PUMP_H_LO, PUMP_W, PUMP_H_HI - PUMP_H_LO, C_PUMP, "Pump\n[Yd=0]"),
]:
    ax2.add_patch(mpatches.FancyBboxPatch(
        (mx(xw + ww), yw), ww, hw, boxstyle="square,pad=0",
        facecolor=col, edgecolor=C_OUT, linewidth=0.7,
        linestyle="--", alpha=0.20, zorder=2))
    ax2.text(mx(xw + ww/2), yw + hw/2, lbl,
            ha="center", va="center", fontsize=FS_SM - 1.5, color=C_DIM,
            alpha=0.6, zorder=3)

# ── Ventilation fans ──────────────────────────────────────────────────────────
# Fan A (INTAKE) at X=C_LEN (left edge in this view), H=FAN_A_H=600
# Fan B (EXHAUST) at X=0 (right edge), H=FAN_B_H=1800
FAN_HH = DUCT_HEIGHT
ax2.add_patch(mpatches.Rectangle((0, FAN_A_H - FAN_HH//2), 60, FAN_HH,
             facecolor=C_FAN, edgecolor=C_OUT, linewidth=0.6, alpha=0.8, zorder=6))
ax2.text(30, FAN_A_H, "FAN\nIN", ha="center", va="center",
        fontsize=FS_SM - 1.5, color=C_OUT, zorder=7)

ax2.add_patch(mpatches.Rectangle((C_LEN - 60, FAN_B_H - FAN_HH//2), 60, FAN_HH,
             facecolor=C_FAN, edgecolor=C_OUT, linewidth=0.6, alpha=0.8, zorder=6))
ax2.text(C_LEN - 30, FAN_B_H, "FAN\nOUT", ha="center", va="center",
        fontsize=FS_SM - 1.5, color=C_OUT, zorder=7)

# Fan cross-ventilation arrow (diagonal)
ax2.annotate("", xy=(C_LEN - 60, FAN_B_H), xytext=(60, FAN_A_H),
            arrowprops=dict(arrowstyle="-|>", color=C_FAN, lw=1.2,
                            linestyle="dashed"), zorder=4)
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

ax2.annotate("", xy=(C_LEN, DIM_TOP2), xytext=(0, DIM_TOP2),
            arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax2.plot([0, 0], [DIM_TOP2 - 80*0.3, DIM_TOP2 + 80*0.3], color=C_DIM, lw=0.6)
ax2.plot([C_LEN, C_LEN], [DIM_TOP2 - 80*0.3, DIM_TOP2 + 80*0.3], color=C_DIM, lw=0.6)
ax2.text(C_LEN/2, DIM_TOP2 + 80*0.55, f"Container length  {C_LEN}mm",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM)

dim2h(FP_X_L, FP_X_R, DIM_TOP2 + 200, f"Rail span  {RAIL_SPAN}mm", offset=80, color=RAIL_CLR)

ax2.annotate("", xy=(DIM_LEFT2, C_HGT), xytext=(DIM_LEFT2, 0),
            arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax2.plot([DIM_LEFT2 - 80*0.3, DIM_LEFT2 + 80*0.3], [0, 0], color=C_DIM, lw=0.6)
ax2.plot([DIM_LEFT2 - 80*0.3, DIM_LEFT2 + 80*0.3], [C_HGT, C_HGT], color=C_DIM, lw=0.6)
ax2.text(DIM_LEFT2 - 80*0.6, C_HGT/2, f"H={C_HGT}mm",
        ha="right", va="center", fontsize=FS_SM, color=C_DIM, rotation=90)

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
    (C_IBC_BLUE, "Blue IBC stack x2 (2×600L)"),
    (C_IBC_BROWN,"Brown IBC x1 (600L)"),
    (C_DRUM_LT,  "Revolving light-trap drum"),
    (C_EVAP,     "Evap cooler  [ghost = Yd=0 wall]"),
    (C_DOOR,     "Hinged panel"),
    (C_FAN,      "Ventilation fan (IN / OUT)"),
    (C_PINHOLE,  "Pinhole Ø2.17mm  [ghost = far wall]"),
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
TB2_X = C_LEN + 420
TB2_Y = -450
TB2_W = 1550
TB2_H = 420

ax2.add_patch(mpatches.Rectangle((TB2_X, TB2_Y), TB2_W, TB2_H,
             facecolor="#F8F8F8", edgecolor=C_OUT, linewidth=1.0))
ax2.add_patch(mpatches.Rectangle((TB2_X, TB2_Y + 280), TB2_W, TB2_H - 280,
             facecolor="#E0E0E8", edgecolor=C_OUT, linewidth=0.6))
ax2.text(TB2_X + TB2_W/2, TB2_Y + 360, "TBS-001",
        ha="center", va="center", fontsize=FS_LG + 2, color=C_OUT, fontweight="bold")
ax2.text(TB2_X + TB2_W/2, TB2_Y + 305, "ASSEMBLY — FILM PLANE SIDE ELEVATION",
        ha="center", va="center", fontsize=FS_MD, color=C_OUT)
ax2.text(TB2_X + 20, TB2_Y + 240, "Scale: 1:75 (approx)",
        ha="left", va="center", fontsize=FS_SM, color=C_DIM)
ax2.text(TB2_X + 20, TB2_Y + 180,
        "View: from film plane wall (Yd=2,362mm)  →  looking toward pinhole (Yd=0)",
        ha="left", va="center", fontsize=FS_SM, color=C_DIM)
ax2.text(TB2_X + 20, TB2_Y + 120,
        "X axis mirrored: far end (X=5,893mm) at LEFT;  cargo door (X=0) at RIGHT",
        ha="left", va="center", fontsize=FS_SM, color=C_DIM)
ax2.text(TB2_X + 20, TB2_Y + 60,
        f"Rail span {RAIL_SPAN}mm  |  Film plane {FP_W}×{C_HGT}mm  |  f/{PH_FNO}",
        ha="left", va="center", fontsize=FS_SM - 0.5, color=C_DIM)
ax2.text(TB2_X + TB2_W - 20, TB2_Y + 0, "© 2026 Alvin Richards — GNU AGPLv3",
        ha="right", va="bottom", fontsize=FS_SM - 1, color=C_DIM, style="italic")

# ── Save ──────────────────────────────────────────────────────────────────────
out2 = f"{DIAGRAMS_DIR}/assembly-overview-fp.png"
fig2.tight_layout(pad=0)
plt.savefig(out2, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.savefig(svg_path(out2), bbox_inches="tight", facecolor=BG)
plt.close(fig2)
print(f"Saved: {out2}")


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 3 — PLAN VIEW: OPERATIONAL vs TRANSPORT MODE
#
# Top-down plan view of the cargo door end (X=0 end), showing two side-by-side
# views:
#   LEFT:  Transport mode  — panel slid inward 300mm, drums slid inward 305mm,
#          ISO container doors can close.
#   RIGHT: Operational mode — panel at X=0, drums at operational positions,
#          panel can swing open 180° for loading.
#
# Axes: X (vertical, up = into container) vs Yd (horizontal, 0=near wall).
# ═══════════════════════════════════════════════════════════════════════════════

# ── Palette for plan view ────────────────────────────────────────────────────
C_PANEL   = "#C8C8C0"    # panel fill (same as C_DOOR)
C_PANEL_C = "#A8B8A8"    # panel center zone (slightly different)
C_DRUM_LT3 = "#E8E8D0"  # light trap drum fill
C_WASTE   = "#7A6B5A"    # waste drum fill
C_RAIL3   = "#CC4422"    # HGR20 panel slide rail color (red — distinct from brown tracks)
C_TRACK   = "#8B7355"    # V-groove track color
C_CONT_DR = "#9CA0A8"    # container door fill
C_GHOST   = "#D0D0D8"    # ghost position fill

# ── Geometry ─────────────────────────────────────────────────────────────────
# Operational positions
OP_PANEL_X  = 0                               # panel outer face at X=0
OP_DRUM_D1_YD = DRUM_LZ_YD_LO                 # = 0mm (near wall)
OP_DRUM_D2_YD = DRUM_FZ_YD_LO                 # = 1782mm (far wall)
OP_DRUM_X     = PANEL_CORNER_T                 # = 40mm (left edge)

# Transport positions
TR_PANEL_X  = PANEL_SLIDE                     # = 300mm (slid inward)
TR_DRUM_X   = OP_DRUM_X + DRUM_SLIDE          # = 345mm (slid inward)

# Container exterior face and door thickness
CONT_WALL = 40   # container wall thickness (schematic)
DOOR_T    = 60   # ISO door leaf thickness (schematic)

# Light trap drum center in Yd
LT_DRUM_YD_CENTER = (PANEL_CORNER_YD_L + PANEL_CORNER_YD_R) / 2  # = 1181mm

# How much of the X axis to show (cargo door end detail)
PLAN_X_MAX = 1200  # show X=0 to ~1200mm into container

# ── Figure: two subplots side by side ────────────────────────────────────────
FIG3_W = 24.0
FIG3_H = 12.0

fig3, (ax_tr, ax_op) = plt.subplots(1, 2, figsize=(FIG3_W, FIG3_H), dpi=DPI)
fig3.patch.set_facecolor(BG)

# ── Common drawing helpers ───────────────────────────────────────────────────
def plan_setup(ax, title_text, subtitle_text=""):
    """Configure axes for plan view: Yd horizontal, X vertical (up = into container)."""
    pad_l, pad_r = 200, 200
    pad_b, pad_t = 350, 200
    ax.set_xlim(-pad_l, C_WID + pad_r)
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
    # Film plane floor rail at X=RAIL_X_L (= ZONE_L_END = 625mm)
    ax.add_patch(mpatches.Rectangle((0, RAIL_X_L - 10), C_WID, 20,
                 facecolor=C_RAIL3, edgecolor=C_OUT, linewidth=0.5,
                 alpha=0.5, zorder=4))
    ax.text(C_WID / 2, ZONE_L_END + 30,
            f"Film plane floor rail  X={ZONE_L_END}mm",
            ha="center", va="bottom", fontsize=FS_SM - 1, color=C_DIM,
            style="italic", zorder=5)


def draw_stepped_panel(ax, panel_x_outer, alpha=0.85):
    """
    Draw the stepped panel in plan view.
    panel_x_outer = X position of the panel's exterior face.
    """
    # Corner zone near (Yd=0 to PANEL_CORNER_YD_L): 40mm thick
    ax.add_patch(mpatches.Rectangle(
        (0, panel_x_outer), PANEL_CORNER_YD_L, PANEL_CORNER_T,
        facecolor=C_PANEL, edgecolor=C_OUT, linewidth=1.0,
        alpha=alpha, zorder=5))
    # Center zone (Yd=PANEL_CORNER_YD_L to _R): 120mm thick
    ax.add_patch(mpatches.Rectangle(
        (PANEL_CORNER_YD_L, panel_x_outer), PANEL_CENTER_W, PANEL_CENTER_T,
        facecolor=C_PANEL_C, edgecolor=C_OUT, linewidth=1.0,
        alpha=alpha, zorder=5))
    # Corner zone far (Yd=PANEL_CORNER_YD_R to C_WID): 40mm thick
    ax.add_patch(mpatches.Rectangle(
        (PANEL_CORNER_YD_R, panel_x_outer), C_WID - PANEL_CORNER_YD_R, PANEL_CORNER_T,
        facecolor=C_PANEL, edgecolor=C_OUT, linewidth=1.0,
        alpha=alpha, zorder=5))
    # Step lines
    for yd_step in [PANEL_CORNER_YD_L, PANEL_CORNER_YD_R]:
        ax.plot([yd_step, yd_step],
                [panel_x_outer + PANEL_CORNER_T, panel_x_outer + PANEL_CENTER_T],
                color=C_OUT, lw=1.0, zorder=6)


def draw_light_trap_drum(ax, panel_x_outer):
    """Draw the revolving light trap drum circle in the panel center zone."""
    drum_x_center = panel_x_outer + PANEL_CENTER_T / 2  # centered in 120mm zone
    ax.add_patch(plt.Circle(
        (LT_DRUM_YD_CENTER, drum_x_center), DRUM_R,
        facecolor=C_DRUM_LT3, edgecolor=C_OUT, linewidth=1.0, zorder=6))
    # Center cross
    ax.plot([LT_DRUM_YD_CENTER - 40, LT_DRUM_YD_CENTER + 40],
            [drum_x_center, drum_x_center], color=C_CL, lw=0.7, zorder=7)
    ax.plot([LT_DRUM_YD_CENTER, LT_DRUM_YD_CENTER],
            [drum_x_center - 40, drum_x_center + 40], color=C_CL, lw=0.7, zorder=7)
    ax.text(LT_DRUM_YD_CENTER, drum_x_center + DRUM_R + 30,
            f"Light trap\n\u00D8{DRUM_D}mm",
            ha="center", va="bottom", fontsize=FS_SM - 0.5, color=C_OUT, zorder=7)


def draw_waste_drums(ax, drum_x_left, d1_yd, d2_yd, alpha=0.85):
    """Draw the two 55-gal waste drums in plan view (circles)."""
    r = DRUM_EQ_R
    cx = drum_x_left + r  # center X
    for yd_lo, label in [(d1_yd, "D-1"), (d2_yd, "D-2")]:
        yd_c = yd_lo + r
        ax.add_patch(plt.Circle(
            (yd_c, cx), r, facecolor=C_WASTE, edgecolor=C_OUT,
            linewidth=0.8, alpha=alpha, zorder=5))
        ax.text(yd_c, cx, label, ha="center", va="center",
                fontsize=FS_SM - 0.5, color="#FFFFFF", fontweight="bold", zorder=6)


def draw_hgr20_rails(ax):
    """Draw the HGR20 panel slide rails (floor level, X direction)."""
    rail_len = PANEL_SLIDE + 100  # show slightly longer than travel
    for yd_pos in [100, C_WID - 100]:  # near and far wall
        ax.add_patch(mpatches.Rectangle(
            (yd_pos - 10, -20), 20, rail_len + 40,
            facecolor=C_RAIL3, edgecolor=C_OUT, linewidth=0.5,
            alpha=0.6, zorder=4))


C_BRIDGE  = "#4A90D9"    # bridge section color (blue — distinct from brown permanent)

def draw_vgroove_tracks(ax, drum_x_left, show_bridges=False):
    """Draw V-groove roller tracks for waste drums.
    Permanent sections: X=PANEL_CORNER_T to PERM_TRACK_END.
    Bridge sections (removable): X=BRIDGE_TRACK_START to BRIDGE_TRACK_END.
    """
    for yd_c in [DRUM_EQ_R, C_WID - DRUM_EQ_R]:
        for offset in [-80, 80]:  # two parallel tracks per drum
            # Permanent section
            ax.add_patch(mpatches.Rectangle(
                (yd_c + offset - 5, PANEL_CORNER_T), 10,
                PERM_TRACK_END - PANEL_CORNER_T,
                facecolor=C_TRACK, edgecolor=C_OUT, linewidth=0.4,
                alpha=0.4, zorder=3))
            # Bridge section (removable)
            if show_bridges:
                ax.add_patch(mpatches.Rectangle(
                    (yd_c + offset - 5, BRIDGE_TRACK_START), 10,
                    BRIDGE_TRACK_END - BRIDGE_TRACK_START,
                    facecolor=C_BRIDGE, edgecolor=C_OUT, linewidth=0.4,
                    alpha=0.5, zorder=3, linestyle="--"))


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


def draw_evap_cooler(ax):
    """Draw evaporative cooler footprint in plan view."""
    ax.add_patch(mpatches.Rectangle(
        (EVAP_Y, EVAP_X), EVAP_D, EVAP_W,
        facecolor=C_EVAP, edgecolor=C_OUT, linewidth=0.8, alpha=0.7, zorder=5))
    ax.text(EVAP_Y + EVAP_D / 2, EVAP_X + EVAP_W / 2,
            "Evap\ncooler", ha="center", va="center",
            fontsize=FS_SM - 1, color="#FFFFFF", zorder=6)


# ── LEFT PANEL: Transport mode ──────────────────────────────────────────────
plan_setup(ax_tr, "TRANSPORT MODE",
           f"Panel retracted {PANEL_SLIDE}mm  |  Drums retracted {DRUM_SLIDE}mm  |  Doors closed")
draw_container_walls(ax_tr)
draw_container_doors(ax_tr, closed=True)
draw_hgr20_rails(ax_tr)
draw_vgroove_tracks(ax_tr, TR_DRUM_X, show_bridges=True)
draw_evap_cooler(ax_tr)

# Ghost: operational positions (dashed outlines)
# Ghost panel
for yd0, w, t in [(0, PANEL_CORNER_YD_L, PANEL_CORNER_T),
                   (PANEL_CORNER_YD_L, PANEL_CENTER_W, PANEL_CENTER_T),
                   (PANEL_CORNER_YD_R, C_WID - PANEL_CORNER_YD_R, PANEL_CORNER_T)]:
    ax_tr.add_patch(mpatches.Rectangle(
        (yd0, OP_PANEL_X), w, t,
        facecolor="none", edgecolor=C_GHOST, linewidth=0.8,
        ls=(0, (4, 3)), alpha=0.6, zorder=2))
# Ghost drums
for yd_lo in [OP_DRUM_D1_YD, OP_DRUM_D2_YD]:
    ax_tr.add_patch(plt.Circle(
        (yd_lo + DRUM_EQ_R, OP_DRUM_X + DRUM_EQ_R), DRUM_EQ_R,
        facecolor="none", edgecolor=C_GHOST, linewidth=0.8,
        ls=(0, (4, 3)), alpha=0.6, zorder=2))

# Solid: transport positions
draw_stepped_panel(ax_tr, TR_PANEL_X)
draw_light_trap_drum(ax_tr, TR_PANEL_X)
draw_waste_drums(ax_tr, TR_DRUM_X, OP_DRUM_D1_YD, OP_DRUM_D2_YD)

# Door closure plane line
ax_tr.plot([0, C_WID], [-CONT_WALL, -CONT_WALL], color="#CC2020", lw=1.2,
           ls="--", dashes=(6, 3), zorder=8)
ax_tr.text(C_WID + 40, -CONT_WALL, "Door closure\nplane",
           ha="left", va="center", fontsize=FS_SM - 1, color="#CC2020", zorder=8)

# Slide arrows
# Panel slide arrow
panel_mid_yd = C_WID / 2
ax_tr.annotate("", xy=(panel_mid_yd, TR_PANEL_X + PANEL_CORNER_T / 2),
               xytext=(panel_mid_yd, OP_PANEL_X + PANEL_CORNER_T / 2),
               arrowprops=dict(arrowstyle="-|>", color="#2060A0", lw=1.5,
                               connectionstyle="arc3,rad=0.15"), zorder=8)
ax_tr.text(panel_mid_yd + 120, (OP_PANEL_X + TR_PANEL_X) / 2 + PANEL_CORNER_T / 2,
           f"Panel slide\n{PANEL_SLIDE}mm",
           ha="left", va="center", fontsize=FS_SM - 0.5, color="#2060A0", zorder=8)

# Drum slide arrows
for yd_lo in [OP_DRUM_D1_YD, OP_DRUM_D2_YD]:
    yd_c = yd_lo + DRUM_EQ_R
    ax_tr.annotate("", xy=(yd_c, TR_DRUM_X + DRUM_EQ_R),
                   xytext=(yd_c, OP_DRUM_X + DRUM_EQ_R),
                   arrowprops=dict(arrowstyle="-|>", color="#805000", lw=1.2,
                                   connectionstyle="arc3,rad=-0.15"), zorder=8)
ax_tr.text(DRUM_EQ_R + 120, (OP_DRUM_X + TR_DRUM_X) / 2 + DRUM_EQ_R,
           f"Drum slide\n{DRUM_SLIDE}mm",
           ha="left", va="center", fontsize=FS_SM - 0.5, color="#805000", zorder=8)

# Dimensions
dim3_y_bot = -CONT_WALL - DOOR_T - 100
# Panel thickness dims
ax_tr.annotate("", xy=(PANEL_CORNER_YD_L / 2, TR_PANEL_X + PANEL_CORNER_T),
               xytext=(PANEL_CORNER_YD_L / 2, TR_PANEL_X),
               arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax_tr.text(PANEL_CORNER_YD_L / 2 - 60, TR_PANEL_X + PANEL_CORNER_T / 2,
           f"{PANEL_CORNER_T}mm", ha="right", va="center",
           fontsize=FS_SM - 1, color=C_DIM, rotation=90)

ax_tr.annotate("", xy=(LT_DRUM_YD_CENTER, TR_PANEL_X + PANEL_CENTER_T),
               xytext=(LT_DRUM_YD_CENTER, TR_PANEL_X),
               arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax_tr.text(LT_DRUM_YD_CENTER + DRUM_R + 30, TR_PANEL_X + PANEL_CENTER_T / 2,
           f"{PANEL_CENTER_T}mm", ha="left", va="center",
           fontsize=FS_SM - 1, color=C_DIM, rotation=90)


# ── RIGHT PANEL: Operational mode ────────────────────────────────────────────
plan_setup(ax_op, "OPERATIONAL MODE",
           "Panel at X=0  |  Drums at operational positions  |  Doors open")
draw_container_walls(ax_op)
draw_container_doors(ax_op, closed=False)
draw_hgr20_rails(ax_op)
draw_vgroove_tracks(ax_op, OP_DRUM_X)
draw_evap_cooler(ax_op)

# Solid: operational positions
draw_stepped_panel(ax_op, OP_PANEL_X)
draw_light_trap_drum(ax_op, OP_PANEL_X)
draw_waste_drums(ax_op, OP_DRUM_X, OP_DRUM_D1_YD, OP_DRUM_D2_YD)

# Door closure plane line (for reference)
ax_op.plot([0, C_WID], [-CONT_WALL, -CONT_WALL], color="#CC2020", lw=0.8,
           ls=":", alpha=0.5, zorder=2)

# Light trap drum overhang — show it extends past X=0
lt_drum_cx = OP_PANEL_X + PANEL_CENTER_T / 2
lt_drum_x_outer = lt_drum_cx - DRUM_R
ax_op.text(LT_DRUM_YD_CENTER, lt_drum_x_outer - 30,
           f"Drum extends {abs(lt_drum_x_outer):.0f}mm\npast exterior face",
           ha="center", va="top", fontsize=FS_SM - 1, color="#CC2020",
           style="italic", zorder=8)

# Fixed door frame
ax_op.plot([0, C_WID], [0, 0], color=C_OUT, lw=1.8, zorder=7)
ax_op.text(C_WID + 40, 0, "Fixed door\nframe (X=0)",
           ha="left", va="center", fontsize=FS_SM - 1, color=C_OUT, zorder=8)

# EPDM seal indicator
ax_op.plot([10, C_WID - 10], [-3, -3], color="#5A3020", lw=2.5,
           solid_capstyle="round", zorder=7)
ax_op.text(C_WID + 40, -3, "EPDM seal",
           ha="left", va="center", fontsize=FS_SM - 1, color="#5A3020", zorder=8)

# Panel thickness dims
ax_op.annotate("", xy=(PANEL_CORNER_YD_L / 2, OP_PANEL_X + PANEL_CORNER_T),
               xytext=(PANEL_CORNER_YD_L / 2, OP_PANEL_X),
               arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax_op.text(PANEL_CORNER_YD_L / 2 - 60, OP_PANEL_X + PANEL_CORNER_T / 2,
           f"{PANEL_CORNER_T}mm", ha="right", va="center",
           fontsize=FS_SM - 1, color=C_DIM, rotation=90)

ax_op.annotate("", xy=(LT_DRUM_YD_CENTER, OP_PANEL_X + PANEL_CENTER_T),
               xytext=(LT_DRUM_YD_CENTER, OP_PANEL_X),
               arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax_op.text(LT_DRUM_YD_CENTER + DRUM_R + 30, OP_PANEL_X + PANEL_CENTER_T / 2,
           f"{PANEL_CENTER_T}mm", ha="left", va="center",
           fontsize=FS_SM - 1, color=C_DIM, rotation=90)

# Cam latch indicators (4x, interior face)
latch_yds = [200, 756, 1606, C_WID - 200]
for yd in latch_yds:
    t = PANEL_CORNER_T if (yd < PANEL_CORNER_YD_L or yd > PANEL_CORNER_YD_R) else PANEL_CENTER_T
    ax_op.plot(yd, OP_PANEL_X + t - 5, marker="x", markersize=5,
              color="#CC2020", mew=1.2, zorder=8)
ax_op.text(latch_yds[-1] + 60, OP_PANEL_X + PANEL_CORNER_T - 5,
           "Cam latches x4",
           ha="left", va="center", fontsize=FS_SM - 1, color="#CC2020", zorder=8)


# ── Shared legend (bottom center of figure) ─────────────────────────────────
legend_items3 = [
    (C_PANEL,    "Panel corner zone (40mm)"),
    (C_PANEL_C,  "Panel center zone (120mm)"),
    (C_DRUM_LT3, "Revolving light trap drum"),
    (C_WASTE,    "55-gal waste drum"),
    (C_TRACK,    "Permanent dolly track"),
    (C_BRIDGE,   "Removable bridge section"),
    (C_EVAP,     "Evaporative cooler"),
    (C_CONT_DR,  "ISO container door"),
    (C_GHOST,    "Ghost (operational position)"),
]

# Draw legend as a horizontal row under the figure using fig3 coordinates
fig3.subplots_adjust(bottom=0.12)
leg_ax = fig3.add_axes([0.05, 0.09, 0.9, 0.06])
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

# ── Shared title block (figure-level) ────────────────────────────────────────
fig3.text(0.5, 0.97, "TBS-001  —  CARGO DOOR END PLAN VIEW",
          ha="center", va="top", fontsize=14, color=C_OUT, fontweight="bold")
fig3.text(0.5, 0.945,
          f"Stepped panel (40mm corners / 120mm center) on HGR20 sliding carriage  |  "
          f"Waste drums on V-groove dollies  |  Scale: approx 1:20",
          ha="center", va="top", fontsize=9, color=C_DIM, style="italic")

# Title block box (bottom-right, figure coords)
tb_ax = fig3.add_axes([0.62, 0.01, 0.36, 0.07])
tb_ax.set_xlim(0, 1)
tb_ax.set_ylim(0, 1)
tb_ax.set_axis_off()
tb_ax.add_patch(mpatches.FancyBboxPatch(
    (0.0, 0.0), 1.0, 1.0, boxstyle="round,pad=0.01",
    facecolor="#F8F8F8", edgecolor=C_OUT, linewidth=1.0))
tb_ax.add_patch(mpatches.Rectangle(
    (0.0, 0.65), 1.0, 0.35,
    facecolor="#E0E0E8", edgecolor=C_OUT, linewidth=0.6))
tb_ax.text(0.5, 0.82, "TBS-001", ha="center", va="center",
           fontsize=12, color=C_OUT, fontweight="bold")
tb_ax.text(0.02, 0.45, "ASSEMBLY — PLAN VIEW (CARGO DOOR END)",
           ha="left", va="center", fontsize=9, color=C_OUT)
tb_ax.text(0.02, 0.22, f"Container: {C_LEN}L \u00d7 {C_WID}W \u00d7 {C_HGT}H (mm interior)",
           ha="left", va="center", fontsize=8, color=C_DIM)
tb_ax.text(0.98, 0.05, "\u00a9 2026 Alvin Richards \u2014 GNU AGPLv3",
           ha="right", va="bottom", fontsize=7, color=C_DIM, style="italic")

# ── Save ──────────────────────────────────────────────────────────────────────
out3 = f"{DIAGRAMS_DIR}/assembly-overview-plan.png"
plt.savefig(out3, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.savefig(svg_path(out3), bbox_inches="tight", facecolor=BG)
plt.close(fig3)
print(f"Saved: {out3}")
