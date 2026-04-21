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
    # Drum circle (Ø750 centred at X=0, H=PH_H)
    drum_c = plt.Circle((0, PH_H), DRUM_R,
                         facecolor="white", edgecolor=C_OUT,
                         linewidth=0.8, alpha=0.9, zorder=5)
    ax.add_patch(drum_c)
    draw_cl_v(ax, 0, PH_H - DRUM_R - 100, PH_H + DRUM_R + 100)

    # ── Fans ──────────────────────────────────────────────────────────────────
    FAN_W_FAB = 200
    # Intake (left end, low)
    hatch_rect(ax, -WALL_T, 200, WALL_T, FAN_W_FAB, C_ALUM, "xx", alpha=0.6)
    # Exhaust (right end, high)
    hatch_rect(ax, CL, CH - FAN_W_FAB - 200, WALL_T, FAN_W_FAB, C_ALUM, "xx", alpha=0.6)

    # ── Equipment blocks (simplified cross-section fills) ─────────────────────
    # Equipment appears at their long-axis positions, heights per spec.
    IBC_H_EQ = 1163
    DRUM_H_EQ = 870
    DRUM_W_EQ = 585

    # Blue IBCs (×2 stacked in depth — single block in this elevation)
    ax.add_patch(mpatches.Rectangle((100, RAIL_OFF), 1219, IBC_H_EQ,
                 facecolor=C_ALUM, edgecolor=C_OUT, linewidth=0.6,
                 alpha=0.7, zorder=3))

    # Brown IBC
    ax.add_patch(mpatches.Rectangle((1380, RAIL_OFF), 1219, IBC_H_EQ,
                 facecolor=C_STEEL, edgecolor=C_OUT, linewidth=0.6,
                 alpha=0.7, zorder=3))

    # Drums ×2
    ax.add_patch(mpatches.Rectangle((1438, RAIL_OFF), DRUM_W_EQ, DRUM_H_EQ,
                 facecolor=C_STEEL, edgecolor=C_OUT, linewidth=0.6,
                 alpha=0.6, zorder=3))
    ax.add_patch(mpatches.Rectangle((2028, RAIL_OFF), DRUM_W_EQ, DRUM_H_EQ,
                 facecolor=C_STEEL, edgecolor=C_OUT, linewidth=0.6,
                 alpha=0.6, zorder=3))

    # Evap cooler
    ax.add_patch(mpatches.Rectangle((1380, 1300), 600, 750,
                 facecolor=C_ALUM, edgecolor=C_OUT, linewidth=0.6,
                 alpha=0.7, zorder=3))

    # Pump manifold
    ax.add_patch(mpatches.Rectangle((2100, RAIL_OFF), 400, 500,
                 facecolor=C_STEEL, edgecolor=C_OUT, linewidth=0.6,
                 alpha=0.6, zorder=3))

    # Electrical panel (wall-mounted)
    ax.add_patch(mpatches.Rectangle((2400, 900), 80, 600,
                 facecolor=C_ALUM, edgecolor=C_OUT, linewidth=0.6,
                 alpha=0.8, zorder=4))

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
        (700,       IBC_H_EQ / 2 + RAIL_OFF, "4"),  # IBC cluster
        (1800,      DRUM_H_EQ / 2 + RAIL_OFF, "5"),  # Drums
        (2440,      900 + 300,  "6"),    # Electrical enclosure
        (1680,      1300 + 375, "7"),    # Evap cooler
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

    # ── Revolving drum (Ø750 mm, centred in panel) ───────────────────────────
    # Centre of panel: X = CW/2 = 1181, H = CH/2 = 1194
    DRUM_CX = CW // 2   # = 1181
    DRUM_CY = CH // 2   # = 1194

    # Drum circle — must appear as a true circle (equal aspect guarantees this)
    drum_circ = plt.Circle((DRUM_CX, DRUM_CY), DRUM_R,
                             facecolor="white", edgecolor=C_OUT,
                             linewidth=1.2, zorder=6)
    ax.add_patch(drum_circ)

    # Drum centre lines
    draw_cl_h(ax, DRUM_CX - DRUM_R - 200, DRUM_CX + DRUM_R + 200, DRUM_CY)
    draw_cl_v(ax, DRUM_CX, DRUM_CY - DRUM_R - 200, DRUM_CY + DRUM_R + 200)

    # Drum baffles (4 × radial fins at 22.5°, 112.5°, 202.5°, 292.5°)
    for angle_deg in [22.5, 112.5, 202.5, 292.5]:
        rad = math.radians(angle_deg)
        fx = DRUM_CX + DRUM_R * math.cos(rad)
        fy = DRUM_CY + DRUM_R * math.sin(rad)
        ax.plot([DRUM_CX, fx], [DRUM_CY, fy],
                color=C_OUT, lw=0.8, zorder=7)

    # Grab handle symbol (horizontal bar inside drum)
    ax.plot([DRUM_CX - 180, DRUM_CX + 180], [DRUM_CY - 80, DRUM_CY - 80],
            color=C_OUT, lw=1.5, zorder=7)
    ax.plot([DRUM_CX - 180, DRUM_CX + 180], [DRUM_CY + 80, DRUM_CY + 80],
            color=C_OUT, lw=1.5, zorder=7)

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

    # ── IBC / drum dashed projections (plan footprints, depth direction) ──────
    # Shown as dashed rectangles indicating where equipment sits behind this wall.
    # Footprint centres (from floor plan, Y depth = their long-axis band):
    #   Blue IBCs:  horiz spans X=100–1319 (floor plan)
    #   Brown IBC:  horiz spans X=1380–2599
    # In end view (width=CW=2362mm), floor-plan X → this view X is NOT the same.
    # Floor plan X (long axis) is the DEPTH direction in this end elevation.
    # Floor plan Y (optical depth, 0–2362mm) → the HORIZONTAL axis in this view.
    # Heights are actual heights (0–CH).
    # Equipment Y (depth) in floor plan: IBCs at Y=100–1116, drums at Y=1600.

    # Blue IBCs (floor plan Y_depth = 100–1116, height 1163mm)
    ax.add_patch(mpatches.Rectangle((100, RAIL_OFF), 1016, 1163,
                 facecolor="#4A90D9", edgecolor="#2060A0",
                 linewidth=0.7, linestyle="--", alpha=0.25, zorder=2))
    ax.text(100 + 508, RAIL_OFF + 582, "Blue IBC\n×2", ha="center", va="center",
            fontsize=FS_SM - 1, color="#2060A0", alpha=0.7, zorder=3)

    # Brown IBC (floor plan Y_depth = 100–1116, height 1163mm)
    ax.add_patch(mpatches.Rectangle((100, RAIL_OFF), 1016, 1163,
                 facecolor="#9C7A3C", edgecolor="#7A5A1C",
                 linewidth=0.7, linestyle=":", alpha=0.15, zorder=2))

    # Drums (floor plan Y_depth = 1310–1890 i.e. cx=1600±290, height 870mm)
    ax.add_patch(mpatches.Rectangle((1310, RAIL_OFF), 580, 870,
                 facecolor="#7A6B5A", edgecolor="#5A4B3A",
                 linewidth=0.7, linestyle="--", alpha=0.25, zorder=2))
    ax.text(1600, RAIL_OFF + 435, "Drums\n×2", ha="center", va="center",
            fontsize=FS_SM - 1, color="#5A4B3A", alpha=0.7, zorder=3)

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

    # Drum diameter (horizontal)
    draw_dim_h(ax, DRUM_CX - DRUM_R, DRUM_CX + DRUM_R, DRUM_CY - DRUM_R - 200,
               f"Drum Ø {DRUM_D} mm", ext=60, gap=20, fs=FS_SM)

    # Drum centre X
    draw_dim_h(ax, 0, DRUM_CX, DIM_TOP - 250,
               f"Drum centre  {DRUM_CX} mm", ext=60, gap=20, fs=FS_SM)

    # Container height
    draw_dim_v(ax, DIM_R, 0, CH, f"H = {CH} mm", ext=80, gap=20, fs=FS_SM)

    # Drum centre height
    draw_dim_v(ax, DIM_R + 300, 0, DRUM_CY,
               f"Drum centre  {DRUM_CY} mm", ext=60, gap=20, fs=FS_SM)

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
