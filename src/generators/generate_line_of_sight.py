#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_line_of_sight.py

Generates diagrams/line-of-sight.png — two-panel optical clearance diagram
for TBS-001 (redesigned film-plane-reduction layout).

Panel A — Plan view (top-down):
  Shows the optical cone from the pinhole (X=2399, Yd=0) expanding to the
  film plane edges (X=150–4649 at Yd=2262mm).
  Equipment in shadow-free end zones (X<150 or X>4649) is always clear.
  Equipment on the pinhole wall (Yd=0) is also always clear.

Panel B — Side elevation:
  Shows the optical cone in the HEIGHT direction (pinhole at H=1194mm,
  cone spreading to cover full image height H=0–2388mm at Yd=2262mm).

Container coordinate system:
  X  = 0–5893mm   (long axis; X=0 cargo door end, X=5893 far end)
  Yd = 0–2362mm   (optical depth; Yd=0 pinhole wall, Yd=2362 far wall)
  H  = 0–2388mm   (height)

ASPECT RATIO RULE: figsize derived from data limits. set_aspect("equal") always.
"""

import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

from tbs_title_block import title_block
from tbs_constants import (
    C_LEN, C_WID, C_HGT,
    FP_X_L, FP_X_R, FP_Y, FP_Y_MIN,
    PH_X, PH_H,
    ZONE_L_END, ZONE_R_START,
    DRUM_CX, DRUM_D, DRUM_R, DRUM_H_LT,
    EP_X, EP_W, EP_H_LO, EP_H_HI,
    BA_X, BA_W, BA_H_LO, BA_H_HI,
    PUMP_X, PUMP_W, PUMP_H_LO, PUMP_H_HI, PUMP_D,
    CORRIDOR_YD_NEAR,
    IBC_COL_X, IBC_W, IBC_D, IBC_H_STK, IBC_H_600,
    BLUE_IBC_Y, BROWN_IBC_Y,
    IBC_FAR_Y, WASTE_IBC_Y,
    DIAGRAMS_DIR, 
    cone_left, cone_right,
    C_OUT, C_CL, C_DIM,
    C_LT_DRUM, C_WASTE_IBC, C_ELEC, C_BATT, C_PUMP,
    C_BLUE_IBC, C_BROWN_IBC, C_WALL,
)

os.makedirs(DIAGRAMS_DIR, exist_ok=True)

# ── Palette ───────────────────────────────────────────────────────────────────
BG          = "#FFFFFF"
C_CONE      = "#FFE0A0"    # optical cone fill (amber)
C_CONE_EDGE = "#C07000"    # optical cone edge
C_CLEAR     = "#20A020"    # clearance OK
C_BLOCK     = "#CC2020"    # potential obstruction
C_ZONE_L    = "#FFF0E0"    # left end zone tint (orange)
C_ZONE_OPT  = "#F0FFF0"    # optical zone tint (green)
C_ZONE_R    = "#E8F0FF"    # right end zone tint (blue)

FS_SM = 7.0
FS_MD = 8.5
FS_LG = 10.0

# ── Equipment list ────────────────────────────────────────────────────────────
# Each entry: plan position (x, yd, w, d) and elevation height (h_bot, h_top)
# zone: "left", "wall", "right" — used to assign expected clearance status

EQUIPMENT = [
    # LEFT END ZONE — X=0–625mm (shadow-free at all depths)
    dict(name="Light trap drum",
         x=DRUM_CX - DRUM_R, yd=C_WID//2 - DRUM_R, w=DRUM_D, d=DRUM_D,  # centred at Yd=CW/2=1181mm
         h_bot=0, h_top=DRUM_H_LT,
         color=C_LT_DRUM, zone="left"),

    # (waste drums eliminated in rev 5 — left zone is light trap only)

    # PINHOLE WALL — Yd=0 face (always shadow-free)
    dict(name="Electrical panel",
         x=EP_X, yd=0, w=EP_W, d=80,
         h_bot=EP_H_LO, h_top=EP_H_HI,
         color=C_ELEC, zone="wall"),

    dict(name="Battery bank",
         x=BA_X, yd=0, w=BA_W, d=80,
         h_bot=BA_H_LO, h_top=BA_H_HI,
         color=C_BATT, zone="wall"),

    dict(name="Pump manifold",
         x=PUMP_X, yd=CORRIDOR_YD_NEAR, w=PUMP_W, d=PUMP_D,
         h_bot=PUMP_H_LO, h_top=PUMP_H_HI,
         color=C_PUMP, zone="right"),

    # RIGHT END ZONE — IBCs only, right-justified to end wall
    dict(name="Blue IBC #1 + Brown (near column)",
         x=IBC_COL_X, yd=BLUE_IBC_Y, w=IBC_W, d=IBC_D,
         h_bot=0, h_top=IBC_H_STK,
         color=C_BLUE_IBC, zone="right"),

    dict(name="Brown IBC (bottom near)",
         x=IBC_COL_X, yd=BROWN_IBC_Y, w=IBC_W, d=IBC_D,
         h_bot=0, h_top=IBC_H_600,
         color=C_BROWN_IBC, zone="right"),

    dict(name="Waste IBC-4 (bottom far)",
         x=IBC_COL_X, yd=IBC_FAR_Y, w=IBC_W, d=IBC_D,
         h_bot=0, h_top=IBC_H_600,
         color=C_WASTE_IBC, zone="right"),

    dict(name="Blue IBC #2 (top far)",
         x=IBC_COL_X, yd=IBC_FAR_Y, w=IBC_W, d=IBC_D,
         h_bot=IBC_H_600, h_top=IBC_H_STK,
         color=C_BLUE_IBC, zone="right"),

    # OPTICAL ZONE — processing tray on floor
    dict(name="Processing tray (304 SS)",
         x=FP_X_L + 20, yd=80, w=FP_X_R - FP_X_L - 40, d=2200,
         h_bot=0, h_top=50,
         color=C_WALL, zone="optical", skip_cone_check=True),
]

# ── Cone check functions ──────────────────────────────────────────────────────
def equipment_in_plan_cone(eq):
    """True if ANY part of the equipment footprint overlaps the optical cone."""
    yd_near = eq["yd"]
    yd_far  = eq["yd"] + eq["d"]
    for yd in np.linspace(max(yd_near, 0), min(yd_far, FP_Y), 30):
        xl = cone_left(yd)
        xr = cone_right(yd)
        eq_xl = eq["x"]
        eq_xr = eq["x"] + eq["w"]
        if eq_xr > xl and eq_xl < xr:
            return True
    return False

def cone_h_bottom(yd):
    return PH_H - PH_H * (yd / FP_Y)

def cone_h_top(yd):
    return PH_H + (C_HGT - PH_H) * (yd / FP_Y)

def equipment_in_elevation_cone(eq):
    """True if ANY part of the equipment height intersects the cone at its depth."""
    yd_near = eq["yd"]
    yd_far  = eq["yd"] + eq["d"]
    for yd in np.linspace(max(yd_near, 0), min(yd_far, FP_Y), 30):
        h_bot = cone_h_bottom(yd)
        h_top = cone_h_top(yd)
        if eq["h_top"] > h_bot and eq["h_bot"] < h_top:
            return True
    return False

# ── Figure layout ─────────────────────────────────────────────────────────────
# Panel A (plan): long axis X, depth Yd
# Panel B (elevation): depth Yd (X axis), height H (Y axis)

PA_X_LO, PA_X_HI = -500, 6500
PA_Y_LO, PA_Y_HI = -450, 2900
PB_X_LO, PB_X_HI = -400, 2900
PB_Y_LO, PB_Y_HI = -350, 2750

PA_W = PA_X_HI - PA_X_LO   # 7000
PA_H = PA_Y_HI - PA_Y_LO   # 3350
PB_W = PB_X_HI - PB_X_LO   # 3300
PB_H = PB_Y_HI - PB_Y_LO   # 3100

FIG_TOT_W = 28.0
FIG_TOT_H = FIG_TOT_W * max(PA_H, PB_H) / (PA_W + PB_W)

DPI = 150

fig = plt.figure(figsize=(FIG_TOT_W, FIG_TOT_H), dpi=DPI)
fig.patch.set_facecolor(BG)

gs = fig.add_gridspec(1, 2, width_ratios=[PA_W, PB_W],
                      wspace=0.06, left=0.01, right=0.99, top=0.95, bottom=0.05)
ax_a = fig.add_subplot(gs[0])
ax_b = fig.add_subplot(gs[1])

for ax in [ax_a, ax_b]:
    ax.set_facecolor(BG)
    ax.axis("off")

ax_a.set_xlim(PA_X_LO, PA_X_HI)
ax_a.set_ylim(PA_Y_LO, PA_Y_HI)
ax_a.set_aspect("equal")

ax_b.set_xlim(PB_X_LO, PB_X_HI)
ax_b.set_ylim(PB_Y_LO, PB_Y_HI)
ax_b.set_aspect("equal")


# ═══════════════════════════════════════════════════════════════════════════════
# PANEL A — PLAN VIEW
# ═══════════════════════════════════════════════════════════════════════════════
ax = ax_a

# Zone fills
ax.add_patch(mpatches.Rectangle((0, 0), ZONE_L_END, C_WID,
             facecolor=C_ZONE_L, edgecolor="none", zorder=0))
ax.add_patch(mpatches.Rectangle((ZONE_L_END, 0), ZONE_R_START - ZONE_L_END, C_WID,
             facecolor=C_ZONE_OPT, edgecolor="none", zorder=0))
ax.add_patch(mpatches.Rectangle((ZONE_R_START, 0), C_LEN - ZONE_R_START, C_WID,
             facecolor=C_ZONE_R, edgecolor="none", zorder=0))

# Container outline
ax.add_patch(mpatches.Rectangle((0, 0), C_LEN, C_WID,
             facecolor="none", edgecolor=C_OUT, linewidth=1.8, zorder=3))

# Zone boundary lines
for xb in [ZONE_L_END, ZONE_R_START]:
    ax.plot([xb, xb], [0, C_WID], color=C_DIM, lw=1.0, ls="--",
            dashes=(8, 4), zorder=3)

# Zone labels
ax.text(ZONE_L_END / 2, C_WID + 120, f"LEFT END ZONE\nX=0–{ZONE_L_END}mm\nshadow-free",
        ha="center", va="bottom", fontsize=FS_SM - 0.5, color="#805000",
        fontweight="bold", zorder=10)
ax.text((ZONE_L_END + ZONE_R_START) / 2, C_WID + 120,
        f"OPTICAL ZONE\nX={ZONE_L_END}–{ZONE_R_START}mm",
        ha="center", va="bottom", fontsize=FS_SM - 0.5, color="#006000",
        fontweight="bold", zorder=10)
ax.text((ZONE_R_START + C_LEN) / 2, C_WID + 120,
        f"RIGHT END ZONE\nX={ZONE_R_START}–{C_LEN}mm\nshadow-free",
        ha="center", va="bottom", fontsize=FS_SM - 0.5, color="#004080",
        fontweight="bold", zorder=10)

# ── Optical cone (plan view) ──────────────────────────────────────────────────
yd_vals = np.linspace(0, FP_Y, 300)
xl_vals = np.array([cone_left(yd) for yd in yd_vals])
xr_vals = np.array([cone_right(yd) for yd in yd_vals])

cone_xs = np.concatenate([xl_vals, xr_vals[::-1]])
cone_ys = np.concatenate([yd_vals, yd_vals[::-1]])
ax.fill(cone_xs, cone_ys, color=C_CONE, alpha=0.50, zorder=2)
ax.plot(xl_vals, yd_vals, color=C_CONE_EDGE, lw=1.4, ls="--", zorder=3)
ax.plot(xr_vals, yd_vals, color=C_CONE_EDGE, lw=1.4, ls="--", zorder=3)

# Film plane line
ax.plot([FP_X_L, FP_X_R], [FP_Y, FP_Y], color=C_CL, lw=2.0, zorder=4)
ax.text((FP_X_L + FP_X_R) / 2, FP_Y + 115,
        f"Film plane  X={FP_X_L}–{FP_X_R}mm  (Yd={FP_Y}mm)",
        ha="center", va="bottom", fontsize=FS_SM, color=C_CL, zorder=10)

# Pinhole
ax.plot(PH_X, 0, "o", color=C_BLOCK, ms=9, zorder=6)
ax.annotate(f"Pinhole  X={PH_X}mm",
            xy=(PH_X, 0), xytext=(PH_X - 650, -150),
            fontsize=FS_SM, color=C_BLOCK, ha="left",
            arrowprops=dict(arrowstyle="->", linestyle=":", color=C_BLOCK, lw=0.8))

# Optical axis
ax.annotate("", xy=(PH_X, FP_Y - 20), xytext=(PH_X, 20),
            arrowprops=dict(arrowstyle="->", color=C_CL, lw=1.0))
ax.text(PH_X + 80, FP_Y / 2 + 400, "Optical axis",
        ha="left", va="center", fontsize=FS_SM, color=C_CL, zorder=10)

# ── Equipment footprints ──────────────────────────────────────────────────────
for eq in EQUIPMENT:
    in_cone = equipment_in_plan_cone(eq)
    edge_color = C_BLOCK if in_cone else C_CLEAR
    edge_lw = 2.2 if in_cone else 1.4
    alpha = 0.75 if in_cone else 0.55

    ax.add_patch(mpatches.Rectangle(
        (eq["x"], eq["yd"]), eq["w"], eq["d"],
        facecolor=eq["color"], edgecolor=edge_color,
        linewidth=edge_lw, alpha=alpha, zorder=4))

    # Label inside footprint, or outside for small items
    short = eq["name"].split(" (")[0].split(" x")[0]
    if eq["d"] >= 150 and eq["w"] >= 200:
        ax.text(eq["x"] + eq["w"] / 2, eq["yd"] + eq["d"] / 2,
                short, ha="center", va="center",
                fontsize=max(FS_SM - 1.5, 5), color="white", zorder=10,
                fontweight="bold")
    else:
        # External label with 45° leader line for small items
        _small_idx = getattr(ax, '_small_label_n', 0)
        offsets = [150, 300, 450]
        label_off = offsets[_small_idx % len(offsets)]
        ax._small_label_n = _small_idx + 1
        lx = eq["x"] + eq["w"] / 2
        ly = eq["yd"] + eq["d"]
        ax.annotate(short, xy=(lx, ly),
                    xytext=(lx + label_off, ly + label_off),
                    ha="left", va="bottom",
                    fontsize=max(FS_SM - 1.5, 5), color=C_OUT, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", linestyle=":", color=C_DIM, lw=0.7),
                    zorder=10)

    if in_cone:
        ax.text(eq["x"] + eq["w"] / 1.5, eq["yd"] + eq["d"] + 870,
                "IN CONE", ha="center", va="bottom",
                fontsize=FS_SM - 1, color=C_BLOCK, fontweight="bold", zorder=10)

# ── Dimension labels ──────────────────────────────────────────────────────────
ax.text(C_LEN / 2, -150, "PLAN VIEW — TOP-DOWN (Z axis)",
        ha="center", va="top", fontsize=FS_MD, color=C_OUT, fontweight="bold", zorder=10)
ax.text(C_LEN / 2, -350,
        f"Optical cone: Pinhole (X={PH_X}, Yd=0) → Film plane edges "
        f"(X={FP_X_L} & X={FP_X_R}, Yd={FP_Y}mm)",
        ha="center", va="top", fontsize=FS_SM, color=C_DIM, zorder=10)

ax.annotate("", xy=(C_LEN, -320), xytext=(0, -320),
            arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax.text(C_LEN / 2, -280, f"{C_LEN}mm", ha="center", va="bottom",
        fontsize=FS_SM, color=C_DIM, zorder=10)

ax.annotate("", xy=(-450, C_WID), xytext=(-450, 0),
            arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax.text(-500, C_WID / 2, f"{C_WID}mm", ha="right", va="center",
        fontsize=FS_SM, color=C_DIM, rotation=90, zorder=10)

# Legend box
ax.text(PA_X_LO + 60, PA_Y_HI - 60,
        "RED border = equipment inside optical cone (shadow risk)\n"
        "GREEN border = equipment clear of optical cone",
        ha="left", va="top", fontsize=FS_SM - 0.5, color=C_OUT,
        bbox=dict(boxstyle="round,pad=2", facecolor="#FFFFF0",
                  edgecolor=C_DIM, linewidth=0.6),
        zorder=10)


# ═══════════════════════════════════════════════════════════════════════════════
# PANEL B — SIDE ELEVATION
# X axis = optical depth Yd (0–2362mm), Y axis = height H (0–2388mm)
# ═══════════════════════════════════════════════════════════════════════════════
ax = ax_b

# Container fill
ax.add_patch(mpatches.Rectangle((0, 0), C_WID, C_HGT,
             facecolor="#F4F4F4", edgecolor=C_OUT, linewidth=1.8, zorder=1))

# ── Optical cone (elevation) ──────────────────────────────────────────────────
yd_e = np.linspace(0, FP_Y, 300)
hb   = np.array([cone_h_bottom(y) for y in yd_e])
ht   = np.array([cone_h_top(y) for y in yd_e])

cone_xs_e = np.concatenate([yd_e, yd_e[::-1]])
cone_ys_e = np.concatenate([hb, ht[::-1]])
ax.fill(cone_xs_e, cone_ys_e, color=C_CONE, alpha=0.50, zorder=2)
ax.plot(yd_e, hb, color=C_CONE_EDGE, lw=1.4, ls="--", zorder=3)
ax.plot(yd_e, ht, color=C_CONE_EDGE, lw=1.4, ls="--", zorder=3)

# Film plane
ax.plot([FP_Y, FP_Y], [0, C_HGT], color=C_CL, lw=1.8, zorder=4)
ax.text(FP_Y + 125, C_HGT / 2, f"Film plane\nYd={FP_Y}mm",
        ha="left", va="center", fontsize=FS_SM, color=C_CL, zorder=10)

# Pinhole
ax.plot(0, PH_H, "o", color=C_BLOCK, ms=9, zorder=6)
ax.text(-250, PH_H + 70, f"Pinhole\nH={PH_H}mm",
        ha="left", va="bottom", fontsize=FS_SM, color=C_BLOCK, zorder=10)

# Optical axis
ax.plot([0, FP_Y], [PH_H, PH_H], color=C_CL, lw=0.8, ls="--",
        dashes=(8, 4), zorder=3)
ax.text(FP_Y / 2 + 600, PH_H + 55, "Optical axis",
        ha="center", va="bottom", fontsize=FS_SM - 1, color=C_CL, zorder=10)

# ── Equipment in elevation ────────────────────────────────────────────────────
# For overlapping drums in X (same Yd range), offset slightly so labels visible
for eq in EQUIPMENT:
    in_cone_h = equipment_in_elevation_cone(eq)
    edge_color = C_BLOCK if in_cone_h else C_CLEAR
    edge_lw = 2.2 if in_cone_h else 1.4

    yd_near = eq["yd"]
    yd_far  = min(eq["yd"] + eq["d"], C_WID)

    ax.add_patch(mpatches.Rectangle(
        (yd_near, eq["h_bot"]), yd_far - yd_near, eq["h_top"] - eq["h_bot"],
        facecolor=eq["color"], edgecolor=edge_color,
        linewidth=edge_lw, alpha=0.65, zorder=4))

    mid_yd = (yd_near + yd_far) / 2
    mid_h  = (eq["h_bot"] + eq["h_top"]) / 2
    label  = eq["name"].split(" (")[0]
    h_span = eq["h_top"] - eq["h_bot"]
    yd_span = yd_far - yd_near
    if h_span >= 200 and yd_span >= 150:
        ax.text(mid_yd, mid_h, label,
                ha="center", va="center",
                fontsize=max(FS_SM - 2, 4.5), color="white", zorder=10,
                fontweight="bold")
    else:
        # External label with 45° leader line for small items
        _elev_idx = getattr(ax, '_elev_label_n', 0)
        offsets = [200, 400, 600]
        label_off = offsets[_elev_idx % len(offsets)]
        ax._elev_label_n = _elev_idx + 1
        ax.annotate(label, xy=(mid_yd, eq["h_top"]),
                    xytext=(mid_yd + label_off, eq["h_top"] + label_off),
                    ha="left", va="bottom",
                    fontsize=max(FS_SM - 2, 4.5), color=C_OUT, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", linestyle=":", color=C_DIM, lw=0.7),
                    zorder=10)

# ── Elevation labels ──────────────────────────────────────────────────────────
ax.text(C_WID / 2, -120, "SIDE ELEVATION — along long axis (X)",
        ha="center", va="top", fontsize=FS_MD, color=C_OUT, fontweight="bold", zorder=10)
ax.text(C_WID / 2, -320,
        f"Cone spread in HEIGHT — Pinhole at H={PH_H}mm",
        ha="center", va="top", fontsize=FS_SM, color=C_DIM, zorder=10)

ax.annotate("", xy=(C_WID, -270), xytext=(0, -270),
            arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax.text(C_WID / 2, -250, f"{C_WID}mm (optical depth)",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM, zorder=10)

ax.annotate("", xy=(-280, C_HGT), xytext=(-280, 0),
            arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax.text(-300, C_HGT / 2, f"{C_HGT}mm",
        ha="right", va="center", fontsize=FS_SM, color=C_DIM, rotation=90, zorder=10)


# ── Title block (full-figure overlay) ──────────────���──────────────────────────
ax_tb = fig.add_axes([0, 0, 1, 1], facecolor="none")
ax_tb.axis("off")
title_block(ax_tb, "SHEET 1 OF 1",
            drawing_title="OPTICAL LINE-OF-SIGHT CLEARANCE",
            subtitle=f"Pinhole X={PH_X}mm  |  Film plane X={FP_X_L}–{FP_X_R}mm at Yd={FP_Y}mm",
            scale_note="Not to scale",
            doc_id="TBS-001 · Line of Sight")

# Determine flagged items (skip items marked as floor-level fixtures)
checkable = [eq for eq in EQUIPMENT if not eq.get("skip_cone_check")]
plan_flags = [eq["name"] for eq in checkable if equipment_in_plan_cone(eq)]
elev_flags = [eq["name"] for eq in checkable if equipment_in_elevation_cone(eq)]
both_flags = [n for n in plan_flags if n in elev_flags]

if both_flags:
    note = (f"OBSTRUCTION RISK: {', '.join(both_flags)}.\n"
            "These items fall within the optical cone in both plan and elevation.\n"
            "Reposition or reduce height to clear the cone before fabrication.")
    note_col = C_BLOCK
    note_bg  = "#FFF0F0"
else:
    note = ("All equipment clears the optical cone in both plan and elevation.  "
            f"End zones X=0–{ZONE_L_END}mm and X={ZONE_R_START}–{C_LEN}mm are provably shadow-free.")
    note_col = C_CLEAR
    note_bg  = "#F0FFF0"

fig.text(0.5, 0.028, note, ha="center", va="bottom",
         fontsize=FS_SM, color=note_col,
         bbox=dict(boxstyle="round,pad=2", facecolor=note_bg,
                   edgecolor=note_col, linewidth=1.0))


# ── Save ──────────────────────────────────────────────────────────────────────
out = f"{DIAGRAMS_DIR}/line-of-sight.png"
plt.savefig(out, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.close(fig)
print(f"Saved: {out}")
if both_flags:
    print(f"  WARNING — Items in optical cone: {', '.join(both_flags)}")
else:
    print("  All clear — no equipment intersects optical cone.")
