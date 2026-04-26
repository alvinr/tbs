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
    FP_X_L, FP_X_R, FP_Y,
    PH_X, PH_H,
    ZONE_L_END, ZONE_R_START,
    DRUM_CX, DRUM_D, DRUM_R, DRUM_H_LT,
    EVAP_X, EVAP_W, EVAP_H,
    EP_X, EP_W, EP_H_LO, EP_H_HI,
    BA_X, BA_W, BA_H_LO, BA_H_HI,
    PUMP_X, PUMP_W, PUMP_H_LO, PUMP_H_HI,
    IBC_COL_X, IBC_W, IBC_H_STK, IBC_H_600,
    DRUM_EQ_D, DRUM_EQ_H,
    DRUM_LZ_CX,
    RAIL_X_L, RAIL_X_R,
    DIAGRAMS_DIR,
    C_OUT, C_CL, C_DIM,
)

os.makedirs(DIAGRAMS_DIR, exist_ok=True)

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
X_LO, X_HI = -500, 6900
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
ax.text(ZONE_L_END / 2, C_HGT - 100,
        f"LEFT END ZONE\nX=0–{ZONE_L_END}mm",
        ha="center", va="top", fontsize=FS_SM - 0.5, color="#805000",
        fontweight="bold", zorder=5)
ax.text((ZONE_L_END + ZONE_R_START) / 2, C_HGT - 100,
        f"OPTICAL ZONE\nX={ZONE_L_END}–{ZONE_R_START}mm",
        ha="center", va="top", fontsize=FS_SM - 0.5, color="#006000",
        fontweight="bold", zorder=5)
ax.text((ZONE_R_START + C_LEN) / 2, C_HGT - 100,
        f"RIGHT END ZONE\nX={ZONE_R_START}–{C_LEN}mm",
        ha="center", va="top", fontsize=FS_SM - 0.5, color="#004080",
        fontweight="bold", zorder=5)


# ── Container outline + corrugation ──────────────────────────────────────────
ax.add_patch(mpatches.Rectangle((0, 0), C_LEN, C_HGT,
             facecolor="none", edgecolor=C_OUT, linewidth=1.8, zorder=5))
corrugation_marks(ax, 0,    0, C_LEN, step=600)
corrugation_marks(ax, C_HGT, 0, C_LEN, step=600)


# ── LEFT END ZONE — revolving drum + evap cooler ──────────────────────────────

# Hinged panel (symbolic thin rect on near long wall face)
ax.add_patch(mpatches.Rectangle((0, 0), 80, C_HGT,
             facecolor=C_DOOR, edgecolor=C_OUT, linewidth=0.8, alpha=0.9, zorder=4))

# Revolving drum: centre at X=0 (outside edge of container), bottom at Y=RAIL_OFF
# In this side elevation appears as a rectangle Ø750mm wide × 2000mm tall.
ax.add_patch(mpatches.Rectangle((-DRUM_R, RAIL_OFF), DRUM_D, DRUM_H_ELV,
             facecolor=C_DRUM_LT, edgecolor=C_OUT, linewidth=0.8, alpha=0.9, zorder=5))
# Centre line through drum
ax.plot([DRUM_CX, DRUM_CX], [RAIL_OFF, RAIL_OFF + DRUM_H_ELV + 100],
        color=C_CL, lw=0.7, ls="--", dashes=(6, 3), zorder=6)
leader(ax, DRUM_CX, RAIL_OFF + DRUM_H_ELV + 60, -200, PH_H + 650,
       f"Hinged panel +\nRevolving drum  VERTICAL AXIS\nO{DRUM_D}mm x {DRUM_H_ELV}mm H",
       ha="right", fs=FS_SM)

# Evap cooler: X=400-1000, bottom at RAIL_OFF, height EVAP_H=800
equip_rect(ax, EVAP_X, RAIL_OFF, EVAP_W, EVAP_H, C_EVAP, zorder=4)
ax.text(EVAP_X + EVAP_W/2, RAIL_OFF + EVAP_H/2,
        "Evap\ncooler", ha="center", va="center",
        fontsize=FS_SM - 0.5, color="#FFFFFF", zorder=6)

leader(ax, EVAP_X + EVAP_W/2, RAIL_OFF + EVAP_H, 600, 1900,
       f"Evap cooler\nX={EVAP_X}–{EVAP_X+EVAP_W}mm", ha="left", fs=FS_SM)

# Black-water drums — 2× 55-gal, one per Yd corner (rev 4: unstacked).
# In this side elevation both drums share X=DRUM_LZ_CX → overlap. Draw as single block.
_drum_x0 = DRUM_LZ_CX - DRUM_EQ_D // 2
equip_rect(ax, _drum_x0, RAIL_OFF, DRUM_EQ_D, DRUM_EQ_H, C_DRUM_EQ, alpha=0.80, zorder=4)
ax.text(_drum_x0 + DRUM_EQ_D/2, RAIL_OFF + DRUM_EQ_H/2,
        "Waste\ndrums\n×2\n(near+far)", ha="center", va="center",
        fontsize=FS_SM - 0.5, color="#FFFFFF", zorder=5)
leader(ax, _drum_x0 + DRUM_EQ_D/2, RAIL_OFF + DRUM_EQ_H, 800, 2200,
       f"55-gal drums ×2 (unstacked — one per Yd corner)\n"
       f"D-1 near: Yd=25–605mm  |  D-2 far: Yd=1,757–2,337mm\n"
       f"X={_drum_x0}–{_drum_x0+DRUM_EQ_D}mm  H={DRUM_EQ_H}mm each",
       ha="left", fs=FS_SM)


# ── PINHOLE WALL EQUIPMENT — flush-mount on near long wall (Yd=0 face) ────────

# Electrical panel: X=2050-2350, H=900-1500
equip_rect(ax, EP_X, EP_H_LO, EP_W, EP_H_HI - EP_H_LO, C_ELEC, ec=C_OUT, lw=1.0, zorder=4)
ax.text(EP_X + EP_W/2, (EP_H_LO + EP_H_HI)/2,
        "Elec\npanel", ha="center", va="center",
        fontsize=FS_SM - 1, color=C_OUT, zorder=6)

# Battery bank: X=2050-2550, H=0-500
equip_rect(ax, BA_X, BA_H_LO, BA_W, BA_H_HI - BA_H_LO, C_BATT, zorder=4)
ax.text(BA_X + BA_W/2, (BA_H_LO + BA_H_HI)/2,
        "Battery\nbank", ha="center", va="center",
        fontsize=FS_SM - 1, color="#FFFFFF", zorder=6)

# Pump manifold: X=2400-2700, H=200-600
equip_rect(ax, PUMP_X, PUMP_H_LO, PUMP_W, PUMP_H_HI - PUMP_H_LO, C_PUMP, zorder=4)
ax.text(PUMP_X + PUMP_W/2, (PUMP_H_LO + PUMP_H_HI)/2,
        "Pump", ha="center", va="center",
        fontsize=FS_SM - 1, color="#FFFFFF", zorder=6)

leader(ax, EP_X + EP_W, (EP_H_LO + EP_H_HI)/2, EP_X + 700, 2000,
       f"Electrical panel\n(wall-mount, Yd=0 face)\nX={EP_X}–{EP_X+EP_W}mm",
       ha="left", fs=FS_SM)
leader(ax, BA_X + BA_W, (BA_H_LO + BA_H_HI)/2, BA_X + 800, 650,
       f"Battery bank\nX={BA_X}–{BA_X+BA_W}mm", ha="left", fs=FS_SM)
leader(ax, PUMP_X + PUMP_W, (PUMP_H_LO + PUMP_H_HI)/2, PUMP_X + 700, 1100,
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

leader(ax, IBC_COL_X + IBC_W/2, RAIL_OFF + IBC_H_STK, 4300, 2550,
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
FAN_W = 200
ax.add_patch(mpatches.Rectangle((0, 200), 60, FAN_W,
             facecolor=C_FAN, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=4))
ax.text(30, 200 + FAN_W/2, "FAN\nIN", ha="center", va="center",
        fontsize=FS_SM - 1.5, color=C_OUT, zorder=5)

ax.add_patch(mpatches.Rectangle((C_LEN - 60, C_HGT - FAN_W - 200), 60, FAN_W,
             facecolor=C_FAN, edgecolor=C_OUT, linewidth=0.6, alpha=0.7, zorder=4))
ax.text(C_LEN - 30, C_HGT - FAN_W/2 - 200, "FAN\nOUT", ha="center", va="center",
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
TB_Y = 450
TB_W = 1380
TB_H = 420

ax.add_patch(mpatches.Rectangle((TB_X, TB_Y), TB_W, TB_H,
             facecolor="#F8F8F8", edgecolor=C_OUT, linewidth=1.0))
ax.add_patch(mpatches.Rectangle((TB_X, TB_Y + 280), TB_W, TB_H - 280,
             facecolor="#E0E0E8", edgecolor=C_OUT, linewidth=0.6))
ax.text(TB_X + TB_W/2, TB_Y + 350, "TBS-001",
        ha="center", va="center", fontsize=FS_LG + 2, color=C_OUT, fontweight="bold")
ax.text(TB_X + TB_W/2, TB_Y + 295, "ASSEMBLY — SIDE ELEVATION",
        ha="center", va="center", fontsize=FS_MD, color=C_OUT)
ax.text(TB_X + 20, TB_Y + 230, "Scale: 1:75 (approx)",
        ha="left", va="center", fontsize=FS_SM, color=C_DIM)
ax.text(TB_X + 20, TB_Y + 170,
        f"Container: {C_LEN}L x {C_WID}W x {C_HGT}H (mm interior)",
        ha="left", va="center", fontsize=FS_SM, color=C_DIM)
ax.text(TB_X + 20, TB_Y + 110,
        f"Pinhole: X={PH_X}mm  H={PH_H}mm  f/1088  Focal length {C_WID}mm",
        ha="left", va="center", fontsize=FS_SM, color=C_DIM)
ax.text(TB_X + 20, TB_Y + 50,
        "View: near long wall (+Y direction). Optical axis perpendicular to page.",
        ha="left", va="center", fontsize=FS_SM - 0.5, color=C_DIM)
ax.text(TB_X + TB_W - 20, TB_Y + 15, "© 2026 Alvin Richards — GNU AGPLv3",
        ha="right", va="bottom", fontsize=FS_SM - 1, color=C_DIM, style="italic")


# ── Save ──────────────────────────────────────────────────────────────────────
out = f"{DIAGRAMS_DIR}/assembly-overview.png"
fig.tight_layout(pad=0)
plt.savefig(out, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.close(fig)
print(f"Saved: {out}")
