#!/usr/bin/env python3
"""
generate_line_of_sight.py

Generates line-of-sight.png — two-panel optical clearance diagram for TBS-001.

Panel A — Plan view (top-down):
  Shows the optical cone from the pinhole (X=2946, Y_depth=0) to the full
  image plane (Y_depth=2262mm) overlaid on the equipment footprints.
  Any equipment footprint inside the cone is highlighted as a potential
  obstruction.

Panel B — Side elevation:
  Shows the optical cone in the HEIGHT direction (pinhole at H=1194mm,
  cone spreading to cover full image height H=0–2388mm at Y_depth=2262mm).
  Equipment shown at their heights to check vertical clearance.

Container coordinate system (matches floor plan):
  X  = 0–5893mm   (long axis; X=0 cargo door end, X=5893 far end)
  Yd = 0–2362mm   (optical depth; Yd=0 pinhole wall, Yd=2362 far wall)
  H  = 0–2388mm   (height)

  Pinhole: X=2946, Yd=0, H=1194
  Film plane: Yd=2262mm, spanning X=0–5893 and H=0–2388

ASPECT RATIO RULE: figsize derived from data limits. set_aspect("equal") always.
"""

import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon

# ── Container geometry ────────────────────────────────────────────────────────
CL    = 5893   # container interior length (long axis)
CW    = 2362   # container interior width  (optical depth)
CH    = 2388   # container interior height
D_FAR = 2262   # film plane depth from pinhole wall
PH_X  = 2946   # pinhole X (long axis)
PH_YD = 0      # pinhole depth (on near long wall)
PH_H  = 1194   # pinhole height
EQ_X  = 2700   # equipment zone boundary (long axis)

# ── Equipment footprints in plan (X, Yd, width, depth) ───────────────────────
# Positions match generate_floorplan_diagram.py
EQUIPMENT = [
    dict(name="Blue IBC ×2 (front)",  x=100,  yd=100,  w=1219, d=1016,
         color="#4A90D9", h_bot=0, h_top=1163),
    dict(name="Blue IBC ×2 (rear)",   x=100,  yd=1246, w=1219, d=1016,
         color="#2A70B9", h_bot=0, h_top=1163),
    dict(name="Brown IBC ×1",         x=1380, yd=100,  w=1219, d=1016,
         color="#9C7A3C", h_bot=0, h_top=1163),
    dict(name="55-gal Drum 1",        x=1440, yd=1310, w=580,  d=580,
         color="#7A6B5A", h_bot=0, h_top=870),
    dict(name="55-gal Drum 2",        x=2030, yd=1310, w=580,  d=580,
         color="#7A6B5A", h_bot=0, h_top=870),
    dict(name="Evap cooler",          x=1380, yd=1980, w=600,  d=350,
         color="#3DAA96", h_bot=0, h_top=800),
    dict(name="Pump manifold",        x=2050, yd=1980, w=400,  d=300,
         color="#E8884A", h_bot=0, h_top=500),
    dict(name="Electrical panel",     x=2400, yd=0,    w=80,   d=60,
         color="#F5C518", h_bot=900, h_top=1500),
]

# ── Optical cone geometry ─────────────────────────────────────────────────────
# In plan view, the cone boundaries (at depth Yd from the pinhole wall):
#   X_left(Yd)  = PH_X - PH_X * (Yd / D_FAR)          (ray to X=0 at film plane)
#   X_right(Yd) = PH_X + (CL-PH_X) * (Yd / D_FAR)     (ray to X=CL at film plane)

def cone_x_left(yd):
    return PH_X - PH_X * (yd / D_FAR)

def cone_x_right(yd):
    return PH_X + (CL - PH_X) * (yd / D_FAR)

# In side elevation, the cone boundaries (at depth Yd):
#   H_bottom(Yd) = PH_H - PH_H * (Yd / D_FAR)          (ray to H=0 at film plane)
#   H_top(Yd)    = PH_H + (CH - PH_H) * (Yd / D_FAR)   (ray to H=CH at film plane)

def cone_h_bottom(yd):
    return PH_H - PH_H * (yd / D_FAR)

def cone_h_top(yd):
    return PH_H + (CH - PH_H) * (yd / D_FAR)

# ── Check if equipment intersects cone ────────────────────────────────────────
def equipment_in_plan_cone(eq):
    """
    Returns True if ANY part of the equipment footprint overlaps the optical
    cone in plan view (top-down).  Checks at both yd_near and yd_far edges.
    """
    for yd in np.linspace(eq["yd"], eq["yd"] + eq["d"], 20):
        if yd < 0 or yd > D_FAR:
            continue
        xl = cone_x_left(yd)
        xr = cone_x_right(yd)
        eq_xl = eq["x"]
        eq_xr = eq["x"] + eq["w"]
        if eq_xr > xl and eq_xl < xr:
            return True
    return False

def equipment_in_elevation_cone(eq):
    """
    Returns True if ANY part of the equipment height intersects the optical
    cone in the side elevation at the equipment's plan Yd position.
    """
    for yd in np.linspace(eq["yd"], eq["yd"] + eq["d"], 20):
        if yd < 0 or yd > D_FAR:
            continue
        h_bot = cone_h_bottom(yd)
        h_top = cone_h_top(yd)
        if eq["h_top"] > h_bot and eq["h_bot"] < h_top:
            return True
    return False

# ── Palette ───────────────────────────────────────────────────────────────────
BG       = "#FFFFFF"
C_OUT    = "#1A1A1A"
C_DIM    = "#404040"
C_CL     = "#2060A0"
C_CONE   = "#FFE0A0"      # optical cone fill (amber)
C_CONE_EDGE = "#C07000"   # optical cone edge
C_CLEAR  = "#20A020"      # clearance OK
C_BLOCK  = "#CC2020"      # potential obstruction

FS_SM = 7.0
FS_MD = 8.5
FS_LG = 10.0

# ── Figure setup: two panels side-by-side ────────────────────────────────────
# Panel A (plan): X=0-5893mm long axis, Yd=0-2362mm depth
# Panel B (elevation): Yd=0-2362mm depth (horizontal), H=0-2388mm (vertical)
#
# Data ranges with margins:
PA_X_LO, PA_X_HI = -400, 6400      # plan: long axis
PA_Y_LO, PA_Y_HI = -400, 2800      # plan: optical depth
PB_X_LO, PB_X_HI = -400, 2800      # elevation: optical depth (X axis)
PB_Y_LO, PB_Y_HI = -300, 2700      # elevation: height (Y axis)

PA_W = PA_X_HI - PA_X_LO   # 6800
PA_H = PA_Y_HI - PA_Y_LO   # 3200
PB_W = PB_X_HI - PB_X_LO   # 3200
PB_H = PB_Y_HI - PB_Y_LO   # 3000

# Choose figure width so Panel A fills ~60% of width, Panel B ~40%
# Use a gridspec to control widths proportionally
# Total data width: PA_W + PB_W = 6800 + 3200 = 10000mm
# Target total figure width: 28 inches

FIG_TOT_W = 28.0
FIG_TOT_H = FIG_TOT_W * max(PA_H, PB_H) / (PA_W + PB_W)
# Exact: height = 28 * 3200/10000 = 8.96in

DPI = 150

fig = plt.figure(figsize=(FIG_TOT_W, FIG_TOT_H), dpi=DPI)
fig.patch.set_facecolor(BG)

# Gridspec: 2 columns, width proportional to panel data widths
gs = fig.add_gridspec(1, 2, width_ratios=[PA_W, PB_W],
                       wspace=0.08, left=0.01, right=0.99, top=0.97, bottom=0.03)
ax_a = fig.add_subplot(gs[0])   # Plan view
ax_b = fig.add_subplot(gs[1])   # Elevation view

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
# PANEL A — PLAN VIEW (TOP-DOWN)
# X = long axis (0–5893mm), Y = optical depth (0–2362mm)
# ═══════════════════════════════════════════════════════════════════════════════
ax = ax_a

# Container outline
ax.add_patch(mpatches.Rectangle((0, 0), CL, CW,
             facecolor="#F4F4F4", edgecolor=C_OUT, linewidth=1.6, zorder=1))

# Equipment zone tint
ax.add_patch(mpatches.Rectangle((0, 0), EQ_X, CW,
             facecolor="#FFF8EE", edgecolor="none", alpha=0.6, zorder=0))

# Equipment zone boundary
ax.plot([EQ_X, EQ_X], [0, CW], color=C_DIM, lw=0.8, ls="--",
        dashes=(6, 4), zorder=2)
ax.text(EQ_X + 40, CW - 60, "Equipment\nzone boundary",
        ha="left", va="top", fontsize=FS_SM - 1, color=C_DIM)

# ── Optical cone (plan view) ──────────────────────────────────────────────────
yd_vals = np.linspace(0, D_FAR, 300)
xl_vals = cone_x_left(yd_vals)
xr_vals = cone_x_right(yd_vals)

# Fill cone
cone_xs = np.concatenate([xl_vals, xr_vals[::-1]])
cone_ys = np.concatenate([yd_vals, yd_vals[::-1]])
ax.fill(cone_xs, cone_ys, color=C_CONE, alpha=0.45, zorder=2, label="Optical cone")
ax.plot(xl_vals, yd_vals, color=C_CONE_EDGE, lw=1.2, ls="--", zorder=3)
ax.plot(xr_vals, yd_vals, color=C_CONE_EDGE, lw=1.2, ls="--", zorder=3)

# Film plane line
ax.plot([0, CL], [D_FAR, D_FAR], color="#2060A0", lw=1.5, ls="-", zorder=4)
ax.text(CL / 2, D_FAR + 50, f"Film plane  (Yd = {D_FAR} mm)",
        ha="center", va="bottom", fontsize=FS_SM, color="#2060A0")

# Pinhole
ax.plot(PH_X, PH_YD, "o", color=C_BLOCK, ms=8, zorder=6)
ax.annotate(f"Pinhole\nX={PH_X}, Yd=0",
            xy=(PH_X, PH_YD), xytext=(PH_X + 300, -250),
            fontsize=FS_SM, color=C_BLOCK, ha="left",
            arrowprops=dict(arrowstyle="-", color=C_BLOCK, lw=0.7))

# Optical axis arrow
ax.annotate("", xy=(PH_X, D_FAR - 20), xytext=(PH_X, 20),
            arrowprops=dict(arrowstyle="->", color=C_CL, lw=1.0))
ax.text(PH_X + 60, D_FAR / 2,
        f"Optical axis\n{D_FAR}mm", ha="left", va="center",
        fontsize=FS_SM, color=C_CL)

# ── Equipment footprints ──────────────────────────────────────────────────────
PLOTTED_LABELS = {}   # avoid legend duplicates

for eq in EQUIPMENT:
    in_cone = equipment_in_plan_cone(eq)
    edge_color = C_BLOCK if in_cone else C_CLEAR
    edge_lw = 2.0 if in_cone else 1.2
    facecolor = eq["color"]
    alpha = 0.75 if in_cone else 0.55

    ax.add_patch(mpatches.Rectangle(
        (eq["x"], eq["yd"]), eq["w"], eq["d"],
        facecolor=facecolor, edgecolor=edge_color,
        linewidth=edge_lw, alpha=alpha, zorder=4))

    # Small label inside footprint
    ax.text(eq["x"] + eq["w"] / 2, eq["yd"] + eq["d"] / 2,
            eq["name"].split(" ×")[0].split(" (")[0],
            ha="center", va="center",
            fontsize=max(FS_SM - 2, 5), color="white", zorder=5,
            fontweight="bold" if in_cone else "normal")

    # Obstruction flag
    if in_cone:
        ax.text(eq["x"] + eq["w"] / 2, eq["yd"] + eq["d"] + 60,
                "⚠ IN CONE",
                ha="center", va="bottom", fontsize=FS_SM - 1,
                color=C_BLOCK, fontweight="bold", zorder=6)

# ── Plan labels ───────────────────────────────────────────────────────────────
ax.text(CL / 2, -250, "PLAN VIEW — TOP-DOWN (Z axis)",
        ha="center", va="top", fontsize=FS_MD, color=C_OUT, fontweight="bold")
ax.text(CL / 2, -350,
        f"Optical cone from Pinhole (X={PH_X}, Yd=0) → Film plane (Yd={D_FAR}mm)",
        ha="center", va="top", fontsize=FS_SM, color=C_DIM)

# Long axis dimension
ax.annotate("", xy=(CL, -320), xytext=(0, -320),
            arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax.text(CL / 2, -280, f"{CL} mm", ha="center", va="bottom",
        fontsize=FS_SM, color=C_DIM)

# Optical depth dimension
ax.annotate("", xy=(-280, CW), xytext=(-280, 0),
            arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax.text(-300, CW / 2, f"{CW} mm", ha="right", va="center",
        fontsize=FS_SM, color=C_DIM, rotation=90)

# Legend: cone, clear, obstruction
for col, lbl in [(C_CONE, "Optical cone"),
                 (C_CLEAR, "Equipment — CLEAR of cone"),
                 (C_BLOCK, "Equipment — IN optical cone")]:
    pass   # using text annotations below

ax.text(PA_X_LO + 50, PA_Y_HI - 60,
        "RED BORDER = equipment footprint overlaps optical cone\n"
        "GREEN BORDER = equipment footprint clear of optical cone",
        ha="left", va="top", fontsize=FS_SM - 0.5, color=C_OUT,
        bbox=dict(boxstyle="round,pad=4", facecolor="#FFFFF0",
                  edgecolor=C_DIM, linewidth=0.6))


# ═══════════════════════════════════════════════════════════════════════════════
# PANEL B — SIDE ELEVATION
# X axis = optical depth Yd (0–2362mm), Y axis = height H (0–2388mm)
# ═══════════════════════════════════════════════════════════════════════════════
ax = ax_b

# Container interior fill
ax.add_patch(mpatches.Rectangle((0, 0), CW, CH,
             facecolor="#F4F4F4", edgecolor=C_OUT, linewidth=1.6, zorder=1))

# ── Optical cone (side elevation) ─────────────────────────────────────────────
yd_vals_e = np.linspace(0, D_FAR, 300)
hb_vals = cone_h_bottom(yd_vals_e)
ht_vals  = cone_h_top(yd_vals_e)

cone_xs_e = np.concatenate([yd_vals_e, yd_vals_e[::-1]])
cone_ys_e = np.concatenate([hb_vals, ht_vals[::-1]])
ax.fill(cone_xs_e, cone_ys_e, color=C_CONE, alpha=0.45, zorder=2)
ax.plot(yd_vals_e, hb_vals, color=C_CONE_EDGE, lw=1.2, ls="--", zorder=3)
ax.plot(yd_vals_e, ht_vals, color=C_CONE_EDGE, lw=1.2, ls="--", zorder=3)

# Film plane
ax.plot([D_FAR, D_FAR], [0, CH], color="#2060A0", lw=1.5, zorder=4)
ax.text(D_FAR + 40, CH / 2, f"Film plane\nYd={D_FAR}mm",
        ha="left", va="center", fontsize=FS_SM, color="#2060A0")

# Pinhole point
ax.plot(PH_YD, PH_H, "o", color=C_BLOCK, ms=8, zorder=6)
ax.text(PH_YD + 80, PH_H + 60,
        f"Pinhole\nH={PH_H}mm", ha="left", va="bottom",
        fontsize=FS_SM, color=C_BLOCK)

# Optical axis
ax.plot([0, D_FAR], [PH_H, PH_H], color=C_CL, lw=0.8, ls="--",
        dashes=(8, 4), zorder=3)
ax.text(D_FAR / 2, PH_H + 50, "Optical axis", ha="center", va="bottom",
        fontsize=FS_SM - 1, color=C_CL)

# ── Equipment in elevation ────────────────────────────────────────────────────
# In side elevation: X axis = Yd (optical depth), Y axis = height
# Equipment blocks shown at their Yd range and height range.
# For equipment with multiple Yd positions (stacked), show merged block.

for eq in EQUIPMENT:
    in_cone_h = equipment_in_elevation_cone(eq)
    edge_color = C_BLOCK if in_cone_h else C_CLEAR
    edge_lw = 2.0 if in_cone_h else 1.2

    ax.add_patch(mpatches.Rectangle(
        (eq["yd"], eq["h_bot"]), eq["d"], eq["h_top"] - eq["h_bot"],
        facecolor=eq["color"], edgecolor=edge_color,
        linewidth=edge_lw, alpha=0.65, zorder=4))

    mid_yd = eq["yd"] + eq["d"] / 2
    mid_h  = (eq["h_bot"] + eq["h_top"]) / 2
    label = eq["name"].split(" (")[0]
    ax.text(mid_yd, mid_h, label,
            ha="center", va="center",
            fontsize=max(FS_SM - 2.5, 4.5), color="white", zorder=5,
            fontweight="bold" if in_cone_h else "normal")

# ── Elevation labels ──────────────────────────────────────────────────────────
ax.text(CW / 2, -200, "SIDE ELEVATION — along long axis (X)",
        ha="center", va="top", fontsize=FS_MD, color=C_OUT, fontweight="bold")
ax.text(CW / 2, -300,
        f"Optical cone spread in HEIGHT — Pinhole at H={PH_H}mm",
        ha="center", va="top", fontsize=FS_SM, color=C_DIM)

# Depth axis dimension
ax.annotate("", xy=(CW, -230), xytext=(0, -230),
            arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax.text(CW / 2, -190, f"{CW} mm (optical depth)",
        ha="center", va="bottom", fontsize=FS_SM, color=C_DIM)

# Height dimension
ax.annotate("", xy=(-280, CH), xytext=(-280, 0),
            arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=0.8))
ax.text(-300, CH / 2, f"{CH} mm",
        ha="right", va="center", fontsize=FS_SM, color=C_DIM, rotation=90)

# ── Shared title / notes ──────────────────────────────────────────────────────
fig.text(0.5, 0.99,
         "TBS-001  —  OPTICAL LINE-OF-SIGHT CLEARANCE DIAGRAM",
         ha="center", va="top", fontsize=FS_LG + 1, color=C_OUT,
         fontweight="bold")
fig.text(0.5, 0.965,
         "Amber zone = optical cone.  "
         "RED border = component footprint or height intersects cone (shadow risk).  "
         "GREEN border = clear.",
         ha="center", va="top", fontsize=FS_SM, color=C_DIM)

# ── Analysis note ─────────────────────────────────────────────────────────────
# Determine which items are flagged
plan_flags = [eq["name"] for eq in EQUIPMENT if equipment_in_plan_cone(eq)]
elev_flags  = [eq["name"] for eq in EQUIPMENT if equipment_in_elevation_cone(eq)]
both_flags  = [n for n in plan_flags if n in elev_flags]

if both_flags:
    note = (f"OBSTRUCTION RISK: {', '.join(both_flags)}.\n"
            "These items fall within the optical cone in BOTH plan and elevation.\n"
            "Reposition or reduce height to clear the cone before fabrication.")
    note_col = C_BLOCK
else:
    note = "All equipment clears the optical cone in both plan and elevation. No shadow risk."
    note_col = C_CLEAR

fig.text(0.5, 0.025, note, ha="center", va="bottom",
         fontsize=FS_SM, color=note_col,
         bbox=dict(boxstyle="round,pad=5", facecolor="#FFF8F8" if both_flags else "#F0FFF0",
                   edgecolor=note_col, linewidth=1.0))

fig.text(0.99, 0.01, "© 2026 Alvin Richards — GNU AGPLv3",
         ha="right", va="bottom", fontsize=FS_SM - 1.5, color=C_DIM, style="italic")

# ── Save ──────────────────────────────────────────────────────────────────────
plt.savefig("line-of-sight.png",
            dpi=DPI, bbox_inches="tight",
            facecolor=BG, edgecolor="none")
plt.close(fig)
print(f"Saved: line-of-sight.png")
if both_flags:
    print(f"  WARNING — Items in optical cone: {', '.join(both_flags)}")
else:
    print("  All clear — no equipment intersects optical cone.")
