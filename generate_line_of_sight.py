#!/usr/bin/env python3
"""
generate_line_of_sight.py

Generates diagrams/line-of-sight.png — two-panel optical clearance diagram
for TBS-001 (redesigned film-plane-reduction layout).

Panel A — Plan view (top-down):
  Shows the optical cone from the pinhole (X=2874, Yd=0) expanding to the
  new film plane edges (X=625–4649 at Yd=2262mm).
  Equipment in shadow-free end zones (X<625 or X>4649) is always clear.
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

from tbs_constants import (
    C_LEN, C_WID, C_HGT,
    FP_X_L, FP_X_R, FP_Y, FP_Y_MIN,
    PH_X, PH_H,
    ZONE_L_END, ZONE_R_START,
    DRUM_CX, DRUM_D, DRUM_R, DRUM_H_LT,
    EVAP_X, EVAP_W, EVAP_Y, EVAP_D, EVAP_H,
    EP_X, EP_W, EP_H_LO, EP_H_HI,
    BA_X, BA_W, BA_H_LO, BA_H_HI,
    PUMP_X, PUMP_W, PUMP_H_LO, PUMP_H_HI,
    IBC_COL_X, IBC_W, IBC_D, IBC_H_STK, IBC_H_600,
    BLUE_IBC_Y, BROWN_IBC_Y,
    DRUM_EQ_D, DRUM_EQ_H, DRUM_EQ_R, DRUM_STACKED_H,
    DRUM_LZ_CX, DRUM_LZ_YD, DRUM_LZ_YD_LO, DRUM_LZ_YD_HI,
    DIAGRAMS_DIR,
    cone_left, cone_right,
    C_OUT, C_CL, C_DIM,
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
         color="#8B6F47", zone="left"),

    # Black-water drums — near cargo door end wall, Yd=25–605mm (below light trap Yd band)
    dict(name="55-gal drums ×2 (stacked)",
         x=DRUM_LZ_CX - DRUM_EQ_R, yd=DRUM_LZ_YD_LO,
         w=DRUM_EQ_D, d=DRUM_EQ_D,
         h_bot=0, h_top=DRUM_STACKED_H,
         color="#7A6B5A", zone="left"),

    # PINHOLE WALL — Yd=0 face (always shadow-free)
    # Evap cooler relocated here (rev 3) — X=700–1300mm, Yd=0 (pinhole wall face)
    dict(name="Evap cooler",
         x=EVAP_X, yd=EVAP_Y, w=EVAP_W, d=EVAP_D,
         h_bot=0, h_top=EVAP_H,
         color="#3DAA96", zone="wall"),
    dict(name="Electrical panel",
         x=EP_X, yd=0, w=EP_W, d=80,
         h_bot=EP_H_LO, h_top=EP_H_HI,
         color="#F5C518", zone="wall"),

    dict(name="Battery bank",
         x=BA_X, yd=0, w=BA_W, d=80,
         h_bot=BA_H_LO, h_top=BA_H_HI,
         color="#6A5ACD", zone="wall"),

    dict(name="Pump manifold",
         x=PUMP_X, yd=0, w=PUMP_W, d=80,
         h_bot=PUMP_H_LO, h_top=PUMP_H_HI,
         color="#E8884A", zone="wall"),

    # RIGHT END ZONE — IBCs only, right-justified to end wall
    dict(name="Blue IBC stack (×2)",
         x=IBC_COL_X, yd=BLUE_IBC_Y, w=IBC_W, d=IBC_D,
         h_bot=0, h_top=IBC_H_STK,
         color="#4A90D9", zone="right"),

    dict(name="Brown IBC ×1",
         x=IBC_COL_X, yd=BROWN_IBC_Y, w=IBC_W, d=IBC_D,
         h_bot=0, h_top=IBC_H_600,
         color="#9C7A3C", zone="right"),
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
        fontweight="bold")
ax.text((ZONE_L_END + ZONE_R_START) / 2, C_WID + 120,
        f"OPTICAL ZONE\nX={ZONE_L_END}–{ZONE_R_START}mm",
        ha="center", va="bottom", fontsize=FS_SM - 0.5, color="#006000",
        fontweight="bold")
ax.text((ZONE_R_START + C_LEN) / 2, C_WID + 120,
        f"RIGHT END ZONE\nX={ZONE_R_START}–{C_LEN}mm\nshadow-free",
        ha="center", va="bottom", fontsize=FS_SM - 0.5, color="#004080",
        fontweight="bold")

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
ax.text((FP_X_L + FP_X_R) / 2, FP_Y + 55,
        f"Film plane  X={FP_X_L}–{FP_X_R}mm  (Yd={FP_Y}mm)",
        ha="center", va="bottom", fontsize=FS_SM, color=C_CL)

# Pinhole
ax.plot(PH_X, 0, "o", color=C_BLOCK, ms=9, zorder=6)
ax.annotate(f"Pinhole  X={PH_X}mm",
            xy=(PH_X, 0), xytext=(PH_X + 250, -300),
            fontsize=FS_SM, color=C_BLOCK, ha="left",
            arrowprops=dict(arrowstyle="-", color=C_BLOCK, lw=0.8))

# Optical axis
ax.annotate("", xy=(PH_X, FP_Y - 20), xytext=(PH_X, 20),
            arrowprops=dict(arrowstyle="->", color=C_CL, lw=1.0))
ax.text(PH_X + 80, FP_Y / 2, "Optical axis",
        ha="left", va="center", fontsize=FS_SM, color=C_CL)

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

    # Label inside footprint (skip drum — too narrow in Y)
    if eq["d"] >= 150 and eq["w"] >= 200:
        short = eq["name"].split(" (")[0].split(" x")[0]
        ax.text(eq["x"] + eq["w"] / 2, eq["yd"] + eq["d"] / 2,
                short, ha="center", va="center",
                fontsize=max(FS_SM - 1.5, 5), color="white", zorder=5,
                fontweight="bold")

    if in_cone:
        ax.text(eq["x"] + eq["w"] / 2, eq["yd"] + eq["d"] + 70,
                "IN CONE", ha="center", va="bottom",
                fontsize=FS_SM - 1, color=C_BLOCK, fontweight="bold", zorder=6)

# ── Dimension labels ──────────────────────────────────────────────────────────
ax.text(C_LEN / 2, -250, "PLAN VIEW — TOP-DOWN (Z axis)",
        ha="center", va="top", fontsize=FS_MD, color=C_OUT, fontweight="bold")
ax.text(C_LEN / 2, -350,
        f"Optical cone: Pinhole (X={PH_X}, Yd=0) → Film plane edges "
        f"(X={FP_X_L} & X={FP_X_R}, Yd={FP_Y}mm)",
        ha="center", va="top", fontsize=FS_SM, color=C_DIM)

ax.annotate("", xy=(C_LEN, -320), xytext=(0, -320),
            arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax.text(C_LEN / 2, -280, f"{C_LEN} mm", ha="center", va="bottom",
        fontsize=FS_SM, color=C_DIM)

ax.annotate("", xy=(-350, C_WID), xytext=(-350, 0),
            arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax.text(-370, C_WID / 2, f"{C_WID} mm", ha="right", va="center",
        fontsize=FS_SM, color=C_DIM, rotation=90)

# Legend box
ax.text(PA_X_LO + 60, PA_Y_HI - 60,
        "RED border = equipment inside optical cone (shadow risk)\n"
        "GREEN border = equipment clear of optical cone",
        ha="left", va="top", fontsize=FS_SM - 0.5, color=C_OUT,
        bbox=dict(boxstyle="round,pad=4", facecolor="#FFFFF0",
                  edgecolor=C_DIM, linewidth=0.6))


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
ax.text(FP_Y + 45, C_HGT / 2, f"Film plane\nYd={FP_Y}mm",
        ha="left", va="center", fontsize=FS_SM, color=C_CL)

# Pinhole
ax.plot(0, PH_H, "o", color=C_BLOCK, ms=9, zorder=6)
ax.text(80, PH_H + 70, f"Pinhole  H={PH_H}mm",
        ha="left", va="bottom", fontsize=FS_SM, color=C_BLOCK)

# Optical axis
ax.plot([0, FP_Y], [PH_H, PH_H], color=C_CL, lw=0.8, ls="--",
        dashes=(8, 4), zorder=3)
ax.text(FP_Y / 2, PH_H + 55, "Optical axis",
        ha="center", va="bottom", fontsize=FS_SM - 1, color=C_CL)

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
    if h_span >= 200:
        ax.text(mid_yd, mid_h, label,
                ha="center", va="center",
                fontsize=max(FS_SM - 2, 4.5), color="white", zorder=5,
                fontweight="bold")

# ── Elevation labels ──────────────────────────────────────────────────────────
ax.text(C_WID / 2, -220, "SIDE ELEVATION — along long axis (X)",
        ha="center", va="top", fontsize=FS_MD, color=C_OUT, fontweight="bold")
ax.text(C_WID / 2, -320,
        f"Cone spread in HEIGHT — Pinhole at H={PH_H}mm",
        ha="center", va="top", fontsize=FS_SM, color=C_DIM)

ax.annotate("", xy=(C_WID, -270), xytext=(0, -270),
            arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax.text(C_WID / 2, -230, f"{C_WID} mm (optical depth)",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM)

ax.annotate("", xy=(-280, C_HGT), xytext=(-280, 0),
            arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax.text(-300, C_HGT / 2, f"{C_HGT} mm",
        ha="right", va="center", fontsize=FS_SM, color=C_DIM, rotation=90)


# ── Title and analysis note ───────────────────────────────────────────────────
fig.text(0.5, 0.98,
         "TBS-001  —  OPTICAL LINE-OF-SIGHT CLEARANCE DIAGRAM",
         ha="center", va="top", fontsize=FS_LG + 1, color=C_OUT,
         fontweight="bold")
fig.text(0.5, 0.955,
         f"Pinhole X={PH_X}mm  |  Film plane X={FP_X_L}–{FP_X_R}mm at Yd={FP_Y}mm  |  "
         "Amber = optical cone  |  RED border = cone intersection  |  GREEN border = clear",
         ha="center", va="top", fontsize=FS_SM, color=C_DIM)

# Determine flagged items
plan_flags = [eq["name"] for eq in EQUIPMENT if equipment_in_plan_cone(eq)]
elev_flags = [eq["name"] for eq in EQUIPMENT if equipment_in_elevation_cone(eq)]
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
         bbox=dict(boxstyle="round,pad=5", facecolor=note_bg,
                   edgecolor=note_col, linewidth=1.0))

fig.text(0.99, 0.01, "© 2026 Alvin Richards — GNU AGPLv3",
         ha="right", va="bottom", fontsize=FS_SM - 1.5, color=C_DIM, style="italic")

# ── Save ──────────────────────────────────────────────────────────────────────
out = f"{DIAGRAMS_DIR}/line-of-sight.png"
plt.savefig(out, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
plt.close(fig)
print(f"Saved: {out}")
if both_flags:
    print(f"  WARNING — Items in optical cone: {', '.join(both_flags)}")
else:
    print("  All clear — no equipment intersects optical cone.")
