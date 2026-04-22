#!/usr/bin/env python3
"""
generate_assembly_fabrication.py

Generates two-sheet assembly fabrication drawing for TBS-001.

  Sheet 1 — Long-section elevation  (1:50)
    View along short axis (+Y), horizontal = long axis 0–5893 mm,
    vertical = height 0–2388 mm.  Engineering drawing style: section fills,
    dimension lines, ①–⑪ callout bubbles, drawing reference table.

  Sheet 2 — End elevation, cargo door end  (1:20)
    View from the short end wall (X=0), looking into the container:
    horizontal = container width  0–2362 mm,
    vertical   = container height 0–2388 mm.
    Nearly square; drum Ø750 mm appears as a true circle.

ASPECT RATIO RULE
  figsize is ALWAYS derived from data limits — never the reverse.
    fig_h = fig_w * (y_hi - y_lo) / (x_hi - x_lo)
  ax.set_aspect("equal") is ALWAYS set.
"""

import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# ── Container geometry ────────────────────────────────────────────────────────
CL   = 5893   # container interior length (long axis, mm)
CH   = 2388   # container interior height (mm)
CW   = 2362   # container interior width  (optical depth / short axis, mm)
D_FAR = 2262  # film-plane depth from pinhole wall (mm)
EQ_X  = 2700  # equipment zone boundary (mm, long axis)
PH_X  = 2946  # pinhole long-axis centre (mm)
PH_H  = 1194  # pinhole height (mm)
RAIL_OFF = 100  # film-plane rail offset from floor/ceiling (mm)
DRUM_D = 750   # revolving drum diameter (mm)
DRUM_R = DRUM_D // 2

# ── Drawing palette ───────────────────────────────────────────────────────────
BG       = "#FFFFFF"
C_OUT    = "#1A1A1A"
C_DIM    = "#404040"
C_CL     = "#2060A0"     # centre lines (blue dashed)
C_ALUM   = "#C8D8E8"
C_STEEL  = "#B0B0B8"
C_GASKT  = "#5A3020"
C_HATCH  = "#909090"     # hatch lines
C_FILL_INT = "#F4F4F4"   # interior fill (light)

# ── Shared helpers ────────────────────────────────────────────────────────────
FS_SM = 7.0
FS_MD = 8.5
FS_LG = 10.0


def draw_dim_h(ax, x1, x2, y, label, ext=60, gap=20, fs=FS_SM, color=C_DIM):
    """Horizontal dimension: arrow from x1 to x2 at height y."""
    # Extension lines
    ax.plot([x1, x1], [y - ext * 0.4, y + ext * 0.6], color=color, lw=0.5)
    ax.plot([x2, x2], [y - ext * 0.4, y + ext * 0.6], color=color, lw=0.5)
    # Arrow
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.7))
    # Label
    ax.text((x1 + x2) / 2, y + ext * 0.65 + gap, label,
            ha="center", va="bottom", fontsize=fs, color=color)


def draw_dim_v(ax, x, y1, y2, label, ext=60, gap=20, fs=FS_SM, color=C_DIM):
    """Vertical dimension: arrow from y1 to y2 at position x."""
    ax.plot([x - ext * 0.4, x + ext * 0.6], [y1, y1], color=color, lw=0.5)
    ax.plot([x - ext * 0.4, x + ext * 0.6], [y2, y2], color=color, lw=0.5)
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.7))
    ax.text(x - ext * 0.5 - gap, (y1 + y2) / 2, label,
            ha="right", va="center", fontsize=fs, color=color, rotation=90)


def draw_cl_h(ax, x1, x2, y, color=C_CL):
    """Horizontal centre line."""
    ax.plot([x1, x2], [y, y], color=color, lw=0.5,
            ls=(0, (8, 3, 2, 3)), dashes=(8, 3, 2, 3))


def draw_cl_v(ax, x, y1, y2, color=C_CL):
    """Vertical centre line."""
    ax.plot([x, x], [y1, y2], color=color, lw=0.5,
            ls=(0, (8, 3, 2, 3)), dashes=(8, 3, 2, 3))


def hatch_rect(ax, x, y, w, h, color=C_STEEL, hatch="///", alpha=0.5):
    """Hatched rectangle for structural cross-section."""
    p = mpatches.Rectangle((x, y), w, h,
                             facecolor=color, edgecolor=C_OUT,
                             hatch=hatch, linewidth=0.8, alpha=alpha, zorder=3)
    ax.add_patch(p)


def callout(ax, cx, cy, number, r=60, fs=FS_SM - 0.5):
    """Circled callout number (engineering drawing style)."""
    circ = plt.Circle((cx, cy), r, facecolor="white", edgecolor=C_OUT,
                       linewidth=0.8, zorder=8)
    ax.add_patch(circ)
    ax.text(cx, cy, str(number), ha="center", va="center",
            fontsize=fs, color=C_OUT, fontweight="bold", zorder=9)


def title_block(ax, x, y, w, h, title_line1, title_line2, scale, sheet_no):
    """Standard title block."""
    ax.add_patch(mpatches.Rectangle((x, y), w, h,
                 facecolor="#F0F0F4", edgecolor=C_OUT, linewidth=1.0, zorder=6))
    # Header bar
    ax.add_patch(mpatches.Rectangle((x, y + h * 0.60), w, h * 0.40,
                 facecolor="#D8DCE8", edgecolor=C_OUT, linewidth=0.5, zorder=6))
    ax.text(x + w / 2, y + h * 0.80, "TBS-001",
            ha="center", va="center", fontsize=FS_LG + 2,
            color=C_OUT, fontweight="bold", zorder=7)
    ax.text(x + w / 2, y + h * 0.65, title_line1,
            ha="center", va="center", fontsize=FS_MD, color=C_OUT, zorder=7)
    ax.text(x + w / 2, y + h * 0.56, title_line2,
            ha="center", va="center", fontsize=FS_SM, color=C_DIM, zorder=7)
    ax.text(x + 20, y + h * 0.43, f"Scale: {scale}",
            ha="left", va="center", fontsize=FS_SM, color=C_DIM, zorder=7)
    ax.text(x + 20, y + h * 0.33, f"Sheet: {sheet_no}",
            ha="left", va="center", fontsize=FS_SM, color=C_DIM, zorder=7)
    ax.text(x + 20, y + h * 0.20,
            "© 2026 Alvin Richards — GNU AGPLv3",
            ha="left", va="center", fontsize=FS_SM - 1, color=C_DIM,
            style="italic", zorder=7)
    ax.text(x + 20, y + h * 0.08,
            f"Container interior: {CL}L × {CW}W × {CH}H (mm)",
            ha="left", va="center", fontsize=FS_SM - 1, color=C_DIM, zorder=7)


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — LONG-SECTION ELEVATION  (1:50)
# ═══════════════════════════════════════════════════════════════════════════════

def sheet1():
    # ── Data extent ──────────────────────────────────────────────────────────
    X_LO, X_HI = -600, 7200    # 7800 mm wide (5893 + margins + title block)
    Y_LO, Y_HI = -700, 3100    # 3800 mm tall (2388 + dim lines + title block)

    FIG_W = 26.0
    FIG_H = FIG_W * (Y_HI - Y_LO) / (X_HI - X_LO)   # = 26 * 3800/7800 = 12.67 in
    DPI = 150

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Y_LO, Y_HI)
    ax.set_aspect("equal")   # MANDATORY
    ax.axis("off")

    # ── Container interior fill ───────────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle((0, 0), CL, CH,
                 facecolor=C_FILL_INT, edgecolor="none", alpha=0.7, zorder=0))

    # Container walls (cross-section, hatched)
    WALL_T = 80   # symbolic wall thickness for drawing
    hatch_rect(ax, -WALL_T, -WALL_T, CL + 2 * WALL_T, WALL_T, C_STEEL, "///")   # floor
    hatch_rect(ax, -WALL_T, CH,      CL + 2 * WALL_T, WALL_T, C_STEEL, "///")   # ceiling
    hatch_rect(ax, -WALL_T, -WALL_T, WALL_T, CH + 2 * WALL_T, C_STEEL, "///")   # left wall
    hatch_rect(ax, CL,      -WALL_T, WALL_T, CH + 2 * WALL_T, C_STEEL, "///")   # right wall

    # ── Container outline ─────────────────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle((0, 0), CL, CH,
                 facecolor="none", edgecolor=C_OUT, linewidth=1.6, zorder=5))

    # ── Equipment zone boundary (dashed) ─────────────────────────────────────
    ax.plot([EQ_X, EQ_X], [0, CH], color=C_DIM, lw=0.8, ls="--",
            dashes=(6, 4), zorder=4)

    # ── Film plane (far long wall, depth = D_FAR) ─────────────────────────────
    # In this elevation the film plane is an interior feature — not directly
    # visible but indicated with a centre-line symbol and dashed line.
    # Represent as a dashed full-width line at floor level (since it's on the
    # opposite long wall) with callout.
    ax.plot([0, CL], [RAIL_OFF, RAIL_OFF],
            color="#2060A0", lw=1.0, ls="--", dashes=(8, 4), zorder=4)
    ax.plot([0, CL], [CH - RAIL_OFF, CH - RAIL_OFF],
            color="#2060A0", lw=1.0, ls="--", dashes=(8, 4), zorder=4)

    # ── Pinhole symbol ────────────────────────────────────────────────────────
    ph_sym_r = 50
    ph_circ = plt.Circle((PH_X, PH_H), ph_sym_r,
                          facecolor="white", edgecolor=C_OUT,
                          linewidth=1.2, zorder=7)
    ax.add_patch(ph_circ)
    ax.plot([PH_X - 150, PH_X + 150], [PH_H, PH_H],
            color=C_OUT, lw=0.8, zorder=8)
    ax.plot([PH_X, PH_X], [PH_H - 150, PH_H + 150],
            color=C_OUT, lw=0.8, zorder=8)

    # ── Optical axis centre line ──────────────────────────────────────────────
    draw_cl_h(ax, 0, CL, PH_H)

    # ── Hinged panel + drum (cargo door end, X=0) ─────────────────────────────
    # Panel: full height at X=0
    ax.add_patch(mpatches.Rectangle((0, 0), 120, CH,
                 facecolor=C_ALUM, edgecolor=C_OUT, linewidth=0.8,
                 alpha=0.8, zorder=4))
    # Revolving drum — VERTICAL AXIS.  In this long-section elevation (looking
    # along +Y), the drum appears as a RECTANGLE: width = Ø750mm (X direction),
    # height = 2000mm (walking clearance).  Centre of drum aligns with outside
    # edge of container (X=0, panel affixed here): -DRUM_R to +DRUM_R horizontally.
    # Bottom aligns with other equipment at RAIL_OFF (100mm).
    DRUM_H_ELV = 2000   # drum height for elevation views
    ax.add_patch(mpatches.Rectangle((-DRUM_R, RAIL_OFF), DRUM_D, DRUM_H_ELV,
                 facecolor=C_ALUM, edgecolor=C_OUT,
                 linewidth=1.0, alpha=0.7, zorder=5))
    # Vertical centre-line of drum axis
    draw_cl_v(ax, 0, RAIL_OFF, RAIL_OFF + DRUM_H_ELV + 150)
    # Label
    ax.text(0, RAIL_OFF + DRUM_H_ELV / 2,
            f"REVOLVING DRUM\nVERTICAL AXIS\nØ{DRUM_D}×{DRUM_H_ELV}mm H",
            ha="center", va="center", fontsize=FS_SM - 1, color=C_OUT,
            style="italic", zorder=6)

    # ── Fans ──────────────────────────────────────────────────────────────────
    FAN_W_FAB = 200
    # Intake (left end, low)
    hatch_rect(ax, -WALL_T, 200, WALL_T, FAN_W_FAB, C_ALUM, "xx", alpha=0.6)
    # Exhaust (right end, high)
    hatch_rect(ax, CL, CH - FAN_W_FAB - 200, WALL_T, FAN_W_FAB, C_ALUM, "xx", alpha=0.6)

    # ── Equipment blocks — PINHOLE WALL COLONNADE positions ──────────────────
    # Heights per spec: 600L IBC=1010mm; 2× stacked=2020mm; drum×2 stacked=1740mm
    IBC_H_600 = 1010   # 600L IBC height
    IBC_H_STK = 2020   # 2× stacked 600L IBC
    DRUM_H_EQ = 870
    DRUM_H_STK = 1740  # 2× stacked drums
    DRUM_W_EQ = 580

    # Blue IBCs ×2 stacked (600L): X=100–1319, H=0–2020
    # Drum is repositioned to Y=1600mm — no drum-IBC overlap in plan view.
    ax.add_patch(mpatches.Rectangle((100, RAIL_OFF), 1219, IBC_H_STK,
                 facecolor=C_ALUM, edgecolor=C_OUT, linewidth=0.6,
                 alpha=0.7, zorder=3))
    # Stacking interface dashed line at H=1010mm
    ax.plot([100, 100 + 1219], [RAIL_OFF + IBC_H_600, RAIL_OFF + IBC_H_600],
            color=C_OUT, lw=0.7, ls="--", dashes=(6, 3), alpha=0.6, zorder=4)
    ax.text(100 + 1219 / 2, RAIL_OFF + IBC_H_STK / 2,
            "BLUE IBC ×2\n(STACKED 2×600L)\nH=2020mm",
            ha="center", va="center", fontsize=FS_SM - 1.5, color=C_OUT, zorder=4)

    # Evap cooler: X=1380–1980, H=0–800 (at pinhole wall side)
    ax.add_patch(mpatches.Rectangle((1380, RAIL_OFF), 600, 800,
                 facecolor=C_ALUM, edgecolor=C_OUT, linewidth=0.6,
                 alpha=0.7, zorder=3))
    ax.text(1680, RAIL_OFF + 400, "EVAP\nCOOLER", ha="center", va="center",
            fontsize=FS_SM - 1.5, color=C_OUT, zorder=4)

    # Pump manifold: X=1980–2380, H=0–500
    ax.add_patch(mpatches.Rectangle((1980, RAIL_OFF), 400, 500,
                 facecolor=C_STEEL, edgecolor=C_OUT, linewidth=0.6,
                 alpha=0.6, zorder=3))
    ax.text(2180, RAIL_OFF + 250, "PUMP\nMANIFOLD", ha="center", va="center",
            fontsize=FS_SM - 1.5, color=C_OUT, zorder=4)

    # Electrical panel (wall-mounted on pinhole long wall face)
    ax.add_patch(mpatches.Rectangle((2050, 900), 80, 600,
                 facecolor=C_ALUM, edgecolor=C_OUT, linewidth=0.6,
                 alpha=0.8, zorder=4))
    ax.text(2090, 1200, "ELEC\nPANEL", ha="center", va="center",
            fontsize=FS_SM - 2, color=C_OUT, zorder=5)

    # 55-gal drums ×2 stacked: X=3900–4480, H=0–1740
    ax.add_patch(mpatches.Rectangle((3900, RAIL_OFF), DRUM_W_EQ, DRUM_H_STK,
                 facecolor=C_STEEL, edgecolor=C_OUT, linewidth=0.6,
                 alpha=0.6, zorder=3))
    ax.plot([3900, 3900 + DRUM_W_EQ], [RAIL_OFF + DRUM_H_EQ, RAIL_OFF + DRUM_H_EQ],
            color=C_OUT, lw=0.7, ls="--", dashes=(6, 3), alpha=0.6, zorder=4)
    ax.text(3900 + DRUM_W_EQ / 2, RAIL_OFF + DRUM_H_STK / 2,
            "DRUMS ×2\nSTACKED", ha="center", va="center",
            fontsize=FS_SM - 1.5, color=C_OUT, zorder=4)

    # Brown IBC ×1 (600L): X=4674–5893, H=0–1010
    ax.add_patch(mpatches.Rectangle((4674, RAIL_OFF), 1219, IBC_H_600,
                 facecolor=C_STEEL, edgecolor=C_OUT, linewidth=0.6,
                 alpha=0.7, zorder=3))
    ax.text(4674 + 1219 / 2, RAIL_OFF + IBC_H_600 / 2,
            "BROWN IBC ×1\n(600L)\nH=1010mm",
            ha="center", va="center", fontsize=FS_SM - 1.5, color=C_OUT, zorder=4)

    # ── Film-plane rails (dashed lines at rail height) ────────────────────────
    ax.plot([EQ_X, CL], [RAIL_OFF, RAIL_OFF],
            color=C_CL, lw=1.2, ls="--", dashes=(8, 3), zorder=5)
    ax.plot([EQ_X, CL], [CH - RAIL_OFF, CH - RAIL_OFF],
            color=C_CL, lw=1.2, ls="--", dashes=(8, 3), zorder=5)

    # ── Callout bubbles ───────────────────────────────────────────────────────
    CALL_R = 80
    callouts = [
        (PH_X,      PH_H + 300, "1"),    # Pinhole aperture plate
        (CL - 200,  RAIL_OFF,   "2"),    # Film plane rails (lower)
        (CL - 400,  1194,       "3"),    # Film plane mechanism (centre)
        (710,       IBC_H_STK / 2 + RAIL_OFF, "4"),  # IBC cluster (X=100–1319 centre=710)
        (4190,      DRUM_H_STK / 2 + RAIL_OFF, "5"),  # Drums (X=3900–4480 centre=4190)
        (2090,      1200,        "6"),    # Electrical enclosure
        (1680,      RAIL_OFF + 400, "7"),  # Evap cooler
        (60,        PH_H + DRUM_R + 150, "8"),  # Hinged panel + drum
        (-WALL_T / 2, 300,      "9"),    # Fan intake
        (CL + WALL_T / 2, CH - 300, "10"),  # Fan exhaust
        (2300,      RAIL_OFF + 250, "11"),  # Pump manifold
    ]
    for (cx, cy, num) in callouts:
        callout(ax, cx, cy, num, r=CALL_R)

    # ── Dimension callouts ────────────────────────────────────────────────────
    DIM_TOP  = CH + 400
    DIM_BOT  = -350
    DIM_LEFT = -400

    # Total length
    draw_dim_h(ax, 0, CL, DIM_TOP, f"Container interior length  {CL} mm",
               ext=80, gap=30, fs=FS_SM)

    # Equipment zone
    draw_dim_h(ax, 0, EQ_X, DIM_BOT, f"Equipment zone  {EQ_X} mm",
               ext=80, gap=20, fs=FS_SM)

    # Optical zone
    draw_dim_h(ax, EQ_X, CL, DIM_BOT, f"Optical zone  {CL - EQ_X} mm",
               ext=80, gap=20, fs=FS_SM)

    # Film-plane depth (from right end wall)
    # Film plane is D_FAR=2262mm from the pinhole wall (right side).
    # Pinhole wall is at X=CL nominally (the far long wall, Y=0 in floor plan).
    # In this elevation the film plane is an interior feature; show its offset.
    draw_dim_h(ax, CL - D_FAR, CL, DIM_BOT - 250,
               f"Film plane  {D_FAR} mm from pinhole wall",
               ext=80, gap=20, fs=FS_SM)

    # Container height
    draw_dim_v(ax, CL + 400, 0, CH, f"H = {CH} mm", ext=80, gap=20, fs=FS_SM)

    # Rail heights
    draw_dim_v(ax, CL + 700, 0, RAIL_OFF,
               f"Rail offset  {RAIL_OFF} mm", ext=60, gap=20, fs=FS_SM)
    draw_dim_v(ax, CL + 700, CH - RAIL_OFF, CH,
               f"Rail offset  {RAIL_OFF} mm", ext=60, gap=20, fs=FS_SM)

    # Pinhole height
    draw_dim_v(ax, DIM_LEFT, 0, PH_H,
               f"Pinhole centre  {PH_H} mm", ext=60, gap=20, fs=FS_SM)

    # ── Reference table ───────────────────────────────────────────────────────
    REF_X = CL + 800
    REF_Y = CH - 100
    REF_DY = 120
    REF_W  = 1300
    REF_H  = 11 * REF_DY + 80

    ax.add_patch(mpatches.Rectangle((REF_X, REF_Y - REF_H), REF_W, REF_H,
                 facecolor="#F8F8FA", edgecolor=C_OUT, linewidth=0.8, zorder=5))
    ax.text(REF_X + REF_W / 2, REF_Y - 30,
            "DRAWING REFERENCE", ha="center", va="top",
            fontsize=FS_SM, color=C_OUT, fontweight="bold", zorder=6)

    ref_items = [
        ("1",  "Pinhole aperture plate",      "TBS-P01  (fabrication-drawings)"),
        ("2",  "Film plane rails  x4",        "TBS-FM01 (film-plane-mechanism)"),
        ("3",  "Film plane mechanism",         "TBS-FM01 (film-plane-mechanism)"),
        ("4",  "IBC tote cluster  x3",        "TBS-WS01 (water-system-report)"),
        ("5",  "55-gal drums  x2",            "TBS-WS01 (water-system-report)"),
        ("6",  "Electrical enclosure",         "TBS-EL01 (electrical-report)"),
        ("7",  "Evaporative cooler",           "TBS-EL01 (electrical-report)"),
        ("8",  "Hinged panel + revolving drum","TBS-LT01 (light-trap-selection)"),
        ("9",  "Intake fan",                   "TBS-EL01 (electrical-report)"),
        ("10", "Exhaust fan",                  "TBS-EL01 (electrical-report)"),
        ("11", "Pump manifold",                "TBS-WS01 (water-system-report)"),
    ]

    for i, (num, desc, ref) in enumerate(ref_items):
        yy = REF_Y - 80 - i * REF_DY
        ax.text(REF_X + 30, yy, num, ha="left", va="center",
                fontsize=FS_SM, color=C_OUT, fontweight="bold", zorder=6)
        ax.text(REF_X + 120, yy, desc, ha="left", va="center",
                fontsize=FS_SM - 0.5, color=C_OUT, zorder=6)
        ax.text(REF_X + REF_W - 20, yy, ref, ha="right", va="center",
                fontsize=FS_SM - 1.0, color=C_DIM, zorder=6)

    # ── Title block ───────────────────────────────────────────────────────────
    TB_X  = CL + 800
    TB_Y  = Y_LO + 40
    TB_W  = 1300
    TB_H  = 420
    title_block(ax, TB_X, TB_Y, TB_W, TB_H,
                "ASSEMBLY — LONG SECTION ELEVATION",
                "(view: along +Y, looking at near long wall)",
                "1:50", "1 of 2")

    # ── Save ──────────────────────────────────────────────────────────────────
    fig.tight_layout(pad=0)
    plt.savefig("assembly-fab-sheet1.png",
                dpi=DPI, bbox_inches="tight",
                facecolor=BG, edgecolor="none")
    plt.close(fig)
    print("Saved: assembly-fab-sheet1.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — END ELEVATION, CARGO DOOR END  (1:20)
# ═══════════════════════════════════════════════════════════════════════════════

def sheet2():
    """
    View from the SHORT END WALL at X=0, looking INTO the container (+X direction).
      Horizontal = container interior WIDTH  = CW = 2362 mm
      Vertical   = container interior HEIGHT = CH = 2388 mm
      Depth (into page) = container LENGTH   = CL = 5893 mm

    The 2362:2388 ratio is ≈ 0.989:1 (nearly square).
    Data range with margins → square figure, drum Ø750 appears as true circle.
    """
    # ── Data extent ──────────────────────────────────────────────────────────
    X_LO2, X_HI2 = -500, 3100    # 3600 mm wide  (CW=2362 + margins)
    Y_LO2, Y_HI2 = -600, 3000    # 3600 mm tall  (CH=2388 + margins)
    # Ratio: 3600:3600 = 1:1  → square figure

    FIG_W2 = 16.0
    FIG_H2 = FIG_W2 * (Y_HI2 - Y_LO2) / (X_HI2 - X_LO2)   # = 16.0 exactly (square)
    DPI = 150

    fig, ax = plt.subplots(figsize=(FIG_W2, FIG_H2), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO2, X_HI2)
    ax.set_ylim(Y_LO2, Y_HI2)
    ax.set_aspect("equal")   # MANDATORY — ensures drum circle is round
    ax.axis("off")

    # ── Container walls (cross-section, hatched) ──────────────────────────────
    WALL_T2 = 80
    hatch_rect(ax, -WALL_T2, -WALL_T2, CW + 2 * WALL_T2, WALL_T2, C_STEEL, "///")  # floor
    hatch_rect(ax, -WALL_T2, CH,       CW + 2 * WALL_T2, WALL_T2, C_STEEL, "///")  # ceiling
    hatch_rect(ax, -WALL_T2, -WALL_T2, WALL_T2, CH + 2 * WALL_T2, C_STEEL, "///")  # left
    hatch_rect(ax, CW,       -WALL_T2, WALL_T2, CH + 2 * WALL_T2, C_STEEL, "///")  # right

    # ── Container interior fill ───────────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle((0, 0), CW, CH,
                 facecolor=C_FILL_INT, edgecolor="none", alpha=0.7, zorder=0))

    # ── Container outline ─────────────────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle((0, 0), CW, CH,
                 facecolor="none", edgecolor=C_OUT, linewidth=1.6, zorder=5))

    # ── Hinged panel outline (fills the end opening) ──────────────────────────
    # Panel: 2362mm wide × 2388mm tall, 120mm thick
    panel_rect = mpatches.Rectangle((0, 0), CW, CH,
                                     facecolor=C_ALUM, edgecolor=C_OUT,
                                     linewidth=1.0, alpha=0.35, zorder=3)
    ax.add_patch(panel_rect)
    ax.text(CW * 0.15, CH * 0.92, "HINGED PANEL\n2362 × 2388 mm\n120mm thick, 50×50 RHS frame",
            ha="left", va="top", fontsize=FS_SM, color=C_DIM, zorder=6)

    # ── Revolving drum (Ø750 mm, vertical axis) ─────────────────────────────
    # Drum has a VERTICAL axis — person walks through it upright.
    # In this end elevation (looking into the container from X=0), the drum
    # appears as a RECTANGLE: 750mm wide × 2000mm tall.
    # Centre at Y=1600mm (offset from CW/2=1181mm toward far wall).
    # This keeps the drum footprint (Y=1225–1975mm) clear of equipment colonnade.
    DRUM_CX = 1600      # drum centre — offset from container centreline for IBC clearance
    DRUM_H_ELV = 2000   # walking height of drum
    DRUM_LEFT = DRUM_CX - DRUM_R   # = 1225mm
    DRUM_RIGHT = DRUM_CX + DRUM_R  # = 1975mm

    drum_rect = mpatches.Rectangle((DRUM_LEFT, RAIL_OFF), DRUM_D, DRUM_H_ELV,
                                    facecolor=C_ALUM, edgecolor=C_OUT,
                                    linewidth=1.2, alpha=0.7, zorder=6)
    ax.add_patch(drum_rect)

    # Vertical centre-line (drum axis)
    draw_cl_v(ax, DRUM_CX, RAIL_OFF, RAIL_OFF + DRUM_H_ELV + 150)

    # Horizontal baffle slot lines (plan view baffles project as horizontal
    # dashes across the drum in elevation — indicate the 4-baffle internal structure)
    for h_baff in [RAIL_OFF + 500, RAIL_OFF + 1000, RAIL_OFF + 1500]:
        ax.plot([DRUM_LEFT + 40, DRUM_RIGHT - 40], [h_baff, h_baff],
                color=C_OUT, lw=0.6, ls="--", alpha=0.5, zorder=7)

    # Entry threshold bar at equipment floor level
    ax.plot([DRUM_LEFT, DRUM_RIGHT], [RAIL_OFF, RAIL_OFF],
            color=C_OUT, lw=1.5, zorder=7)

    # Label
    ax.text(DRUM_CX, RAIL_OFF + DRUM_H_ELV / 2,
            f"REVOLVING DRUM\nVERTICAL AXIS\nØ{DRUM_D} × {DRUM_H_ELV}mm H",
            ha="center", va="center", fontsize=FS_SM - 0.5, color=C_OUT,
            style="italic", zorder=7)

    # ── Film plane (dashed rectangle at depth 2262 mm into page) ─────────────
    # Cannot be shown as a true projection in 2D end view.
    # Represent as a dashed rectangle inset to indicate "behind" this view.
    film_rect = mpatches.Rectangle((50, 50), CW - 100, CH - 100,
                                    facecolor="none", edgecolor="#2060A0",
                                    linewidth=0.7, linestyle="--",
                                    alpha=0.6, zorder=3)
    ax.add_patch(film_rect)
    ax.text(CW / 2, 30,
            f"Film plane — 5893 × 2388 mm  (depth {D_FAR} mm from pinhole wall)",
            ha="center", va="top", fontsize=FS_SM - 0.5, color="#2060A0",
            style="italic", zorder=6)

    # ── Film-plane rail mounting positions ────────────────────────────────────
    RAIL_X1 = 100    # left rail X (offset from left long wall)
    RAIL_X2 = CW - 100  # right rail X
    RAIL_Y1 = RAIL_OFF  # lower rail Y
    RAIL_Y2 = CH - RAIL_OFF  # upper rail Y

    # Rail circles at 4 corners
    for rx, ry in [(RAIL_X1, RAIL_Y1), (RAIL_X1, RAIL_Y2),
                   (RAIL_X2, RAIL_Y1), (RAIL_X2, RAIL_Y2)]:
        rail_c = plt.Circle((rx, ry), 40, facecolor=C_STEEL,
                              edgecolor=C_OUT, linewidth=0.7, zorder=6)
        ax.add_patch(rail_c)

    ax.text(RAIL_X1 - 50, RAIL_Y1, "Rail\n①", ha="right", va="center",
            fontsize=FS_SM - 0.5, color=C_DIM, zorder=6)
    ax.text(RAIL_X2 + 50, RAIL_Y2, "Rail\n②", ha="left", va="center",
            fontsize=FS_SM - 0.5, color=C_DIM, zorder=6)

    # ── Equipment projections (colonnade layout — depth into page) ───────────
    # In end elevation (horizontal = container width CW=2362mm = floor-plan Y axis,
    # vertical = height H). Floor-plan Y_depth → horizontal here; heights = actual.
    # Equipment colonnade: all at Y_depth=100–1116mm from pinhole wall.
    # Only items with Y_depth range visible in this view are drawn.

    # Blue IBCs ×2 stacked (colonnade Y_depth=100–1116, H=0–2020mm)
    # Appear at horizontal span matching their floor-plan Y_depth.
    ax.add_patch(mpatches.Rectangle((100, RAIL_OFF), 1016, 2020,
                 facecolor="#4A90D9", edgecolor="#2060A0",
                 linewidth=0.7, linestyle="--", alpha=0.2, zorder=2))
    ax.text(100 + 508, RAIL_OFF + 1010, "Blue IBC\n×2 stacked\n(2×600L)", ha="center", va="center",
            fontsize=FS_SM - 1.5, color="#2060A0", alpha=0.8, zorder=3)

    # Drums ×2 stacked (floor-plan Y_depth=100–680, H=0–1740mm)
    ax.add_patch(mpatches.Rectangle((100, RAIL_OFF), 580, 1740,
                 facecolor="#7A6B5A", edgecolor="#5A4B3A",
                 linewidth=0.7, linestyle=":", alpha=0.15, zorder=2))
    ax.text(100 + 290, RAIL_OFF + 870, "Drums\n×2", ha="center", va="center",
            fontsize=FS_SM - 1.5, color="#5A4B3A", alpha=0.7, zorder=3)

    # Brown IBC ×1 (floor-plan Y_depth=100–1116, H=0–1010mm)
    ax.add_patch(mpatches.Rectangle((100, RAIL_OFF), 1016, 1010,
                 facecolor="#9C7A3C", edgecolor="#7A5A1C",
                 linewidth=0.7, linestyle="--", alpha=0.15, zorder=2))

    # ── Overhead safelight ────────────────────────────────────────────────────
    ax.plot([100, CW - 100], [CH - 100, CH - 100],
            color="#FFD700", lw=2.0, ls="--", dashes=(8, 4), alpha=0.7, zorder=4)
    ax.text(CW / 2, CH - 60, "Safelight (Circuit D)",
            ha="center", va="bottom", fontsize=FS_SM - 1, color="#B8960A")

    # ── Ventilation fans on end walls ─────────────────────────────────────────
    # These fans are on the LONG WALLS (not visible in end elevation) or the
    # SHORT END WALLS. Show as annotations.
    ax.text(50, 350, "FAN\nINTAKE\n(low)", ha="center", va="center",
            fontsize=FS_SM - 1, color=C_DIM, rotation=90,
            bbox=dict(boxstyle="round,pad=0.2", facecolor=C_FILL_INT,
                      edgecolor=C_DIM, linewidth=0.5))
    ax.text(CW - 50, CH - 350, "FAN\nEXHAUST\n(high)", ha="center", va="center",
            fontsize=FS_SM - 1, color=C_DIM, rotation=90,
            bbox=dict(boxstyle="round,pad=0.2", facecolor=C_FILL_INT,
                      edgecolor=C_DIM, linewidth=0.5))

    # ── Dimension callouts ────────────────────────────────────────────────────
    DIM_TOP  = CH + 350
    DIM_LEFT = -320
    DIM_R    = CW + 320

    # Panel width
    draw_dim_h(ax, 0, CW, DIM_TOP, f"Panel / container width  {CW} mm",
               ext=80, gap=30, fs=FS_SM)

    # Drum width (horizontal)
    draw_dim_h(ax, DRUM_LEFT, DRUM_RIGHT, -200,
               f"Drum Ø {DRUM_D} mm", ext=60, gap=20, fs=FS_SM)

    # Drum horizontal centre (offset from container centreline for IBC clearance)
    draw_dim_h(ax, 0, DRUM_CX, DIM_TOP - 250,
               f"Drum centre  {DRUM_CX} mm  (offset — clears colonnade)", ext=60, gap=20, fs=FS_SM)

    # Container height
    draw_dim_v(ax, DIM_R, 0, CH, f"H = {CH} mm", ext=80, gap=20, fs=FS_SM)

    # Drum height (from equipment floor level RAIL_OFF to top)
    draw_dim_v(ax, DIM_R + 300, RAIL_OFF, RAIL_OFF + DRUM_H_ELV,
               f"Drum H  {DRUM_H_ELV} mm", ext=60, gap=20, fs=FS_SM)

    # Rail offset top
    draw_dim_v(ax, DIM_LEFT, 0, RAIL_OFF,
               f"Rail offset  {RAIL_OFF} mm", ext=60, gap=20, fs=FS_SM)

    # Rail centres (left rail to right rail)
    draw_dim_h(ax, RAIL_X1, RAIL_X2, DIM_TOP - 500,
               f"Rail centres  {RAIL_X2 - RAIL_X1} mm", ext=60, gap=20, fs=FS_SM)

    # ── Title block ───────────────────────────────────────────────────────────
    TB_X  = X_LO2 + 40
    TB_Y  = Y_LO2 + 40
    TB_W  = CW + 200
    TB_H  = 400
    title_block(ax, TB_X, TB_Y, TB_W, TB_H,
                "ASSEMBLY — END ELEVATION (CARGO DOOR END)",
                "(view: from X=0 short end wall, looking +X into container)",
                "1:20", "2 of 2")

    # ── Save ──────────────────────────────────────────────────────────────────
    fig.tight_layout(pad=0)
    plt.savefig("assembly-fab-sheet2.png",
                dpi=DPI, bbox_inches="tight",
                facecolor=BG, edgecolor="none")
    plt.close(fig)
    print("Saved: assembly-fab-sheet2.png")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sheet1()
    sheet2()
