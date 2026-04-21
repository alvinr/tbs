#!/usr/bin/env python3
"""
generate_assembly_overview.py

Generates assembly-overview.png — a high-level schematic side-elevation of the
TBS-001 container interior showing how all systems relate spatially.

View direction: looking at the near LONG WALL (Y=0 face) from outside.
  X (horizontal) = 0–5893 mm  (container long axis; left=cargo door, right=far end)
  Y (vertical)   = 0–2388 mm  (container height)
  Z (into page)  = 0–2362 mm  (optical depth; not a diagram axis)

The pinhole is at (X=2946, H=1194) on the near long wall.
The film plane is on the opposite long wall at optical depth 2262 mm — shown
symbolically as a hatched band, since depth cannot be represented in 2D.

ASPECT RATIO RULE: figsize is always derived from data limits.
  FIG_H = FIG_W * (Y_HI - Y_LO) / (X_HI - X_LO)
  ax.set_aspect("equal") is always set.
"""

import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# ── Container geometry ────────────────────────────────────────────────────────
CL   = 5893   # container interior length (long axis, mm)
CH   = 2388   # container interior height (mm)
CW   = 2362   # container interior width  (optical depth, mm)
D_FAR = 2262  # film-plane depth from pinhole wall (mm)
EQ_X  = 2700  # equipment zone / optical zone boundary (mm)
PH_X  = 2946  # pinhole long-axis position (centre of long wall, mm)
PH_H  = 1194  # pinhole height (mm)
WALL_T = 60   # container wall thickness (symbolic, mm)

# ── Palette ───────────────────────────────────────────────────────────────────
BG        = "#FFFFFF"
C_OUT     = "#1A1A1A"
C_DIM     = "#404040"
C_CL      = "#2060A0"
C_INTERIOR = "#F0F0F0"   # container interior fill
C_WALL    = "#B0B0B8"    # container wall
C_EQ_ZONE = "#FFF8EE"    # equipment zone tint

# Equipment colours
C_IBC_BLUE  = "#4A90D9"
C_IBC_BROWN = "#9C7A3C"
C_DRUM      = "#7A6B5A"
C_EVAP      = "#3DAA96"
C_PUMP      = "#E8884A"
C_ELEC      = "#F5C518"
C_FILM_PLN  = "#B8D4E8"   # film plane
C_PINHOLE   = "#CC2020"   # pinhole symbol
C_DOOR      = "#C8C8C0"   # hinged panel
C_FAN       = "#A0A0A8"   # ventilation fans

# ── Data coordinate range → figure size ──────────────────────────────────────
# Container spans X=0–5893, Y=0–2388.  Add margins for dim lines and labels.
X_LO, X_HI = -400, 6700    # 7100 mm wide
Y_LO, Y_HI = -600, 3000    # 3600 mm tall

FIG_W = 24.0                                           # inches, target width
FIG_H = FIG_W * (Y_HI - Y_LO) / (X_HI - X_LO)       # = 24 * 3600/7100 ≈ 12.17 in
# Derived figsize guarantees set_aspect("equal") will not squeeze anything.

DPI = 150

# ── Helpers ───────────────────────────────────────────────────────────────────
FS_SM = 7.5   # small label font size (pt)
FS_MD = 8.5   # medium
FS_LG = 10.0  # large / title


def draw_dim_h(ax, x1, x2, y, label, offset=80, fs=FS_SM, color=C_DIM):
    """Horizontal dimension line between x1 and x2 at height y."""
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.8))
    ax.plot([x1, x1], [y - offset * 0.3, y + offset * 0.3], color=color, lw=0.6)
    ax.plot([x2, x2], [y - offset * 0.3, y + offset * 0.3], color=color, lw=0.6)
    mx = (x1 + x2) / 2
    ax.text(mx, y + offset * 0.55, label, ha="center", va="bottom",
            fontsize=fs, color=color)


def draw_dim_v(ax, x, y1, y2, label, offset=80, fs=FS_SM, color=C_DIM):
    """Vertical dimension line between y1 and y2 at position x."""
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.8))
    ax.plot([x - offset * 0.3, x + offset * 0.3], [y1, y1], color=color, lw=0.6)
    ax.plot([x - offset * 0.3, x + offset * 0.3], [y2, y2], color=color, lw=0.6)
    mx = (y1 + y2) / 2
    ax.text(x - offset * 0.6, mx, label, ha="right", va="center",
            fontsize=fs, color=color, rotation=90)


def leader(ax, x_tip, y_tip, x_txt, y_txt, label, fs=FS_SM, color=C_OUT, ha="left"):
    """Leader line from tip to text."""
    ax.annotate(label, xy=(x_tip, y_tip), xytext=(x_txt, y_txt),
                fontsize=fs, color=color, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color=color, lw=0.7,
                                connectionstyle="arc3,rad=0.0"))


def equip_rect(ax, x, y, w, h, color, alpha=0.85, ec=C_OUT, lw=0.8):
    """Filled rectangle for equipment block."""
    rect = mpatches.FancyBboxPatch((x, y), w, h,
                                    boxstyle="square,pad=0",
                                    facecolor=color, edgecolor=ec,
                                    linewidth=lw, alpha=alpha, zorder=3)
    ax.add_patch(rect)


def corrugation_marks(ax, y, x_start, x_end, step=600, color="#B0B0B0"):
    """Tick marks on floor or ceiling to suggest corrugated wall texture."""
    x = x_start
    while x <= x_end:
        ax.plot([x, x], [y, y + 60 if y == 0 else y - 60],
                color=color, lw=0.5, zorder=1)
        x += step


# ── Figure setup ─────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

ax.set_xlim(X_LO, X_HI)
ax.set_ylim(Y_LO, Y_HI)
ax.set_aspect("equal")   # MANDATORY — never omit
ax.axis("off")


# ── Container interior fill ───────────────────────────────────────────────────
# Equipment zone tint
ax.add_patch(mpatches.Rectangle((0, 0), EQ_X, CH,
             facecolor=C_EQ_ZONE, edgecolor="none", alpha=0.5, zorder=0))

# Optical zone fill (slightly cooler)
ax.add_patch(mpatches.Rectangle((EQ_X, 0), CL - EQ_X, CH,
             facecolor="#EEF4FA", edgecolor="none", alpha=0.5, zorder=0))


# ── Container outline ─────────────────────────────────────────────────────────
cont = mpatches.Rectangle((0, 0), CL, CH,
                            facecolor="none", edgecolor=C_OUT,
                            linewidth=1.6, zorder=5)
ax.add_patch(cont)

# Floor and ceiling corrugation marks
corrugation_marks(ax, 0,    0, CL, step=600)
corrugation_marks(ax, CH,   0, CL, step=600)


# ── Equipment zone / optical zone boundary ────────────────────────────────────
ax.plot([EQ_X, EQ_X], [0, CH],
        color=C_DIM, lw=0.9, ls="--", dashes=(6, 4), zorder=4)
ax.text(EQ_X + 60, CH - 150, "OPTICAL ZONE",
        ha="left", va="top", fontsize=FS_SM, color="#2060A0",
        style="italic", zorder=5)
ax.text(EQ_X - 60, CH - 150, "EQUIPMENT\n(COLONNADE ZONE)",
        ha="right", va="top", fontsize=FS_SM, color="#804020",
        style="italic", zorder=5)


# ── Cargo door end — hinged panel + drum ─────────────────────────────────────
# The short end wall (X=0) is indicated by the container outline.
# Draw the hinged panel as a filled rect, and drum as a circle on its face.
DRUM_D = 750
DRUM_R = DRUM_D / 2
panel_rect = mpatches.Rectangle((0, 0), 80, CH,
                                  facecolor=C_DOOR, edgecolor=C_OUT,
                                  linewidth=0.8, alpha=0.9, zorder=4)
ax.add_patch(panel_rect)
drum_circ = plt.Circle((0, PH_H), DRUM_R,
                         facecolor="#E8E8D0", edgecolor=C_OUT,
                         linewidth=0.8, alpha=0.9, zorder=5)
ax.add_patch(drum_circ)
ax.text(0, PH_H, f"⊕", ha="center", va="center",
        fontsize=9, color=C_OUT, zorder=6)

leader(ax, 0, PH_H + DRUM_R + 100, -200, PH_H + 600,
       f"Hinged panel\n+ revolving drum\nØ{DRUM_D}mm",
       ha="right", fs=FS_SM)


# ── Equipment blocks — PINHOLE WALL COLONNADE ─────────────────────────────────
# All equipment sits adjacent to the pinhole long wall (near-wall, optical depth 0–1220mm).
# Side elevation: depth is into the page.  Equipment is close to this near wall face.
# Heights: 600L IBC = 1010mm; 2× stacked 600L = 2020mm; 55-gal drum = 870mm;
#          2× stacked drums = 1740mm.

IBC_H_600 = 1010   # 600L IBC height
IBC_H_STK = 2020   # 2× stacked 600L IBC height
IBC_W = 1219       # IBC footprint long axis
DRUM_H_EQ = 870
DRUM_W_EQ = 580
DRUM_H_STK = 1740  # 2× stacked drum height

# -- LEFT WING --
# Blue IBC stack ×2 (600L each, stacked vertical): X=100–1319, H=0–2020
equip_rect(ax, 100, 100, IBC_W, IBC_H_STK, C_IBC_BLUE)
ax.text(100 + IBC_W / 2, 100 + IBC_H_STK / 2,
        "Blue IBC\n×2 stacked\n(2×600L)", ha="center", va="center",
        fontsize=FS_SM, color="#FFFFFF", fontweight="bold", zorder=6)
# Stacking bracket indicator
ax.plot([100, 100 + IBC_W], [100 + IBC_H_600, 100 + IBC_H_600],
        color="#FFFFFF", lw=0.8, ls="--", alpha=0.7, zorder=7)
ax.text(100 + IBC_W + 40, 100 + IBC_H_600, "stacking\ninterface",
        color=C_IBC_BLUE, fontsize=FS_SM - 1, ha="left", va="center", zorder=7)

# Evap cooler: X=1380–1980, H=0–800 (in this elevation, depth is into page)
EVAP_X, EVAP_Y, EVAP_W, EVAP_HH = 1380, 100, 600, 800
equip_rect(ax, EVAP_X, EVAP_Y, EVAP_W, EVAP_HH, C_EVAP)
ax.text(EVAP_X + EVAP_W / 2, EVAP_Y + EVAP_HH / 2,
        "Evap\ncooler", ha="center", va="center",
        fontsize=FS_SM - 0.5, color="#FFFFFF", zorder=6)

# Pump manifold: X=1980–2380, H=0–500
PUMP_X, PUMP_Y, PUMP_W, PUMP_HH = 1980, 100, 400, 500
equip_rect(ax, PUMP_X, PUMP_Y, PUMP_W, PUMP_HH, C_PUMP)
ax.text(PUMP_X + PUMP_W / 2, PUMP_Y + PUMP_HH / 2,
        "Pump\nmanifold", ha="center", va="center",
        fontsize=FS_SM - 0.5, color="#FFFFFF", zorder=6)

# Electrical panel: wall-mounted on near long wall face (X=2050–2350, H=900–1500)
ELEC_X, ELEC_Y, ELEC_W, ELEC_HH = 2050, 900, 300, 600
equip_rect(ax, ELEC_X, ELEC_Y, ELEC_W, ELEC_HH, C_ELEC, ec=C_OUT, lw=1.0)
leader(ax, ELEC_X + ELEC_W, ELEC_Y + ELEC_HH * 0.5, ELEC_X + 700, 1700,
       "Electrical panel\n+ battery bank\n(pinhole wall, flush-mount)", ha="left", fs=FS_SM)

# -- RIGHT WING --
# 55-gal drum stack ×2: X=3900–4480, H=0–1740
DRM_X = 3900
equip_rect(ax, DRM_X, 100, DRUM_W_EQ, DRUM_H_STK, C_DRUM)
ax.text(DRM_X + DRUM_W_EQ / 2, 100 + DRUM_H_STK / 2,
        "55-gal\ndrums\n×2 stacked", ha="center", va="center",
        fontsize=FS_SM - 0.5, color="#FFFFFF", zorder=6)
ax.plot([DRM_X, DRM_X + DRUM_W_EQ], [100 + DRUM_H_EQ, 100 + DRUM_H_EQ],
        color="#FFFFFF", lw=0.8, ls="--", alpha=0.7, zorder=7)

# Brown IBC ×1 (600L): X=4674–5893, H=0–1010
equip_rect(ax, 4674, 100, IBC_W, IBC_H_600, C_IBC_BROWN)
ax.text(4674 + IBC_W / 2, 100 + IBC_H_600 / 2,
        "Brown IBC\n×1 (600L)", ha="center", va="center",
        fontsize=FS_SM, color="#FFFFFF", fontweight="bold", zorder=6)

# -- Leader labels --
leader(ax, 100 + IBC_W / 2, 100 + IBC_H_STK, 400, 2400,
       "Blue IBC ×2 stacked\n(2×600L = 1,200L)\nH=2,020mm", ha="left", fs=FS_SM)
leader(ax, DRM_X + DRUM_W_EQ, 100 + DRUM_H_STK * 0.5, DRM_X + 700, 1600,
       "55-gal drums ×2 stacked\n(2×208L = 416L)\nH=1,740mm", ha="left", fs=FS_SM)
leader(ax, 4674 + IBC_W / 2, 100 + IBC_H_600, 4800, 1400,
       "Brown IBC ×1\n(600L = waste/fix)\nH=1,010mm", ha="left", fs=FS_SM)
leader(ax, EVAP_X + EVAP_W / 2, EVAP_Y + EVAP_HH, 1600, 2200,
       "Evap cooler", ha="left", fs=FS_SM)
leader(ax, PUMP_X + PUMP_W / 2, PUMP_Y + PUMP_HH, 2200, 1600,
       "Pump manifold", ha="left", fs=FS_SM)


# ── Film plane (far long wall, optical depth 2262 mm) ─────────────────────────
# In this side elevation, the film plane is PERPENDICULAR to the view direction
# and cannot be shown as a projection.  Represent symbolically as a hatched band
# across the full container width, and annotate clearly.
FP_BAND = 80   # symbolic thickness of hatched band
film_rect = mpatches.Rectangle((0, 0), CL, FP_BAND,
                                 facecolor=C_FILM_PLN, edgecolor="#2060A0",
                                 linewidth=0.8, linestyle="--", alpha=0.8, zorder=2)
ax.add_patch(film_rect)
ax.text(CL / 2, FP_BAND / 2,
        f"Film plane / image surface — 5893 × 2388 mm muslin  (optical depth {D_FAR} mm from pinhole wall)",
        ha="center", va="center", fontsize=FS_SM, color="#2060A0",
        style="italic", zorder=6)

# Film plane repeats at top (ceiling equivalent — muslin draped full height)
film_top = mpatches.Rectangle((0, CH - FP_BAND), CL, FP_BAND,
                                facecolor=C_FILM_PLN, edgecolor="#2060A0",
                                linewidth=0.8, linestyle="--", alpha=0.5, zorder=2)
ax.add_patch(film_top)


# ── Pinhole ───────────────────────────────────────────────────────────────────
# The pinhole is ON the near long wall (Y=0 face), at X=2946, H=1194.
# In this side elevation it appears as a symbol at (PH_X, PH_H).
PINHOLE_SYM_R = 60   # symbolic radius for visibility
ph_circle = plt.Circle((PH_X, PH_H), PINHOLE_SYM_R,
                         facecolor=C_PINHOLE, edgecolor=C_OUT,
                         linewidth=0.8, zorder=7)
ax.add_patch(ph_circle)
# Crosshairs
ax.plot([PH_X - 160, PH_X + 160], [PH_H, PH_H],
        color=C_PINHOLE, lw=0.8, zorder=8)
ax.plot([PH_X, PH_X], [PH_H - 160, PH_H + 160],
        color=C_PINHOLE, lw=0.8, zorder=8)

leader(ax, PH_X + PINHOLE_SYM_R + 40, PH_H, PH_X + 600, PH_H + 400,
       f"Pinhole  Ø2.17 mm\n(X={PH_X}, H={PH_H} mm)\nf/1088",
       ha="left", fs=FS_SM, color=C_PINHOLE)

# Optical axis annotation: "⊗" symbol = into page, centered on pinhole
ax.text(PH_X, PH_H - 280, "⊗ Optical axis (⊥ this view)\nFocal length 2362 mm",
        ha="center", va="top", fontsize=FS_SM, color=C_CL, style="italic")


# ── Ventilation fans ──────────────────────────────────────────────────────────
# Low intake on left short wall, high exhaust on right short wall
FAN_W = 200
# Intake fan (low, at X=0 end — on end wall, shown at left edge)
fan_in = mpatches.Rectangle((0, 200), 60, FAN_W,
                              facecolor=C_FAN, edgecolor=C_OUT,
                              linewidth=0.6, alpha=0.7, zorder=4)
ax.add_patch(fan_in)
ax.text(30, 200 + FAN_W / 2, "FAN\nIN", ha="center", va="center",
        fontsize=FS_SM - 1.5, color=C_OUT, rotation=0, zorder=5)

# Exhaust fan (high, at X=5893 end)
fan_out = mpatches.Rectangle((CL - 60, CH - FAN_W - 200), 60, FAN_W,
                               facecolor=C_FAN, edgecolor=C_OUT,
                               linewidth=0.6, alpha=0.7, zorder=4)
ax.add_patch(fan_out)
ax.text(CL - 30, CH - FAN_W / 2 - 200, "FAN\nOUT", ha="center", va="center",
        fontsize=FS_SM - 1.5, color=C_OUT, rotation=0, zorder=5)


# ── Safelight / overhead lighting (symbolic dashed line) ─────────────────────
ax.plot([100, CL - 100], [CH - 100, CH - 100],
        color="#FFD700", lw=2, ls="--", dashes=(8, 5), alpha=0.7, zorder=4)
ax.text(CL / 2, CH - 60, "Overhead safelight strip (Circuit D)",
        ha="center", va="bottom", fontsize=FS_SM - 1, color="#B8960A")


# ── Dimension callouts ────────────────────────────────────────────────────────
DIM_Y_TOP = CH + 250    # above container
DIM_Y_BOT = -250        # below container
DIM_X_RIGHT = CL + 320  # right of container

# Container total length
draw_dim_h(ax, 0, CL, DIM_Y_TOP, f"Container length  5893 mm",
           offset=100, fs=FS_SM)

# Colonnade label (equipment is near-wall, all depths ≤1220mm — shown in plan, not elevation)
ax.text(CL / 4, DIM_Y_BOT - 60,
        "Equipment colonnade: all items Yd ≤ 1,220mm from pinhole wall (depth into page)",
        ha="center", va="top", fontsize=FS_SM, color="#804020", style="italic")

# Container height
draw_dim_v(ax, DIM_X_RIGHT, 0, CH, f"H = {CH} mm", offset=100, fs=FS_SM)

# Pinhole height
draw_dim_v(ax, DIM_X_RIGHT + 300, 0, PH_H,
           f"Pinhole centre\n{PH_H} mm", offset=100, fs=FS_SM)


# ── Legend ────────────────────────────────────────────────────────────────────
LEG_X = CL + 400
LEG_Y = 2100
LEG_W = 600
LEG_H = 60
LEG_GAP = 80

legend_items = [
    (C_IBC_BLUE,  "Blue IBC tote ×2"),
    (C_IBC_BROWN, "Brown IBC tote ×1"),
    (C_DRUM,      "55-gal drums ×2"),
    (C_EVAP,      "Evaporative cooler"),
    (C_PUMP,      "Pump manifold"),
    (C_ELEC,      "Electrical enclosure"),
    (C_FILM_PLN,  "Film plane / image surface"),
    (C_PINHOLE,   "Pinhole Ø2.17 mm"),
    (C_DOOR,      "Hinged panel + drum"),
    (C_FAN,       "Ventilation fan"),
]

ax.text(LEG_X, LEG_Y + LEG_H + 30, "LEGEND", ha="left", va="bottom",
        fontsize=FS_MD, color=C_OUT, fontweight="bold")
for i, (col, lbl) in enumerate(legend_items):
    yy = LEG_Y - i * LEG_GAP
    ax.add_patch(mpatches.Rectangle((LEG_X, yy - LEG_H * 0.5), LEG_W * 0.3, LEG_H * 0.7,
                                     facecolor=col, edgecolor=C_OUT, linewidth=0.6))
    ax.text(LEG_X + LEG_W * 0.35, yy, lbl,
            ha="left", va="center", fontsize=FS_SM, color=C_OUT)


# ── Title block ───────────────────────────────────────────────────────────────
TB_X = CL + 400
TB_Y = 500
TB_W = 1450
TB_H = 420

ax.add_patch(mpatches.Rectangle((TB_X, TB_Y), TB_W, TB_H,
             facecolor="#F8F8F8", edgecolor=C_OUT, linewidth=1.0))
ax.add_patch(mpatches.Rectangle((TB_X, TB_Y + 280), TB_W, TB_H - 280,
             facecolor="#E0E0E8", edgecolor=C_OUT, linewidth=0.6))

ax.text(TB_X + TB_W / 2, TB_Y + 350, "TBS-001",
        ha="center", va="center", fontsize=FS_LG + 2,
        color=C_OUT, fontweight="bold")
ax.text(TB_X + TB_W / 2, TB_Y + 295, "ASSEMBLY — SIDE ELEVATION",
        ha="center", va="center", fontsize=FS_MD, color=C_OUT)
ax.text(TB_X + 20, TB_Y + 230, "Scale: 1:75 (approx)",
        ha="left", va="center", fontsize=FS_SM, color=C_DIM)
ax.text(TB_X + 20, TB_Y + 170, f"Container: {CL}L × {CW}W × {CH}H (mm interior)",
        ha="left", va="center", fontsize=FS_SM, color=C_DIM)
ax.text(TB_X + 20, TB_Y + 110, f"Focal length: {CW} mm   f/1088",
        ha="left", va="center", fontsize=FS_SM, color=C_DIM)
ax.text(TB_X + 20, TB_Y + 50,
        "View: looking at near long wall (+Y direction)\nOptical axis perpendicular to page",
        ha="left", va="center", fontsize=FS_SM - 0.5, color=C_DIM)
ax.text(TB_X + TB_W - 20, TB_Y + 50, "© 2026 Alvin Richards — GNU AGPLv3",
        ha="right", va="center", fontsize=FS_SM - 1, color=C_DIM, style="italic")


# ── Save ──────────────────────────────────────────────────────────────────────
fig.tight_layout(pad=0)
plt.savefig("assembly-overview.png",
            dpi=DPI, bbox_inches="tight",
            facecolor=BG, edgecolor="none")
plt.close(fig)
print("Saved: assembly-overview.png")
