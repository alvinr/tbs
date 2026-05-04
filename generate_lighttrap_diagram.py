#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_lighttrap_diagram.py
TBS-001  Ventilation System — two drawing sheets.

Sheet 1: Ventilation system — container longitudinal section
Sheet 2: Fan & baffle duct — assembly section
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os
from tbs_constants import svg_path, SVG_DIR

# ── Palette ───────────────────────────────────────────────────────────────────
C_OUT   = "#1A1A1A"
C_CL    = "#2060A0"
C_DIM   = "#505050"
C_ALUM  = "#C8D8E8"
C_STEEL = "#B0B0B8"
C_ELEC  = "#FFF3CC"
C_SOLAR = "#D4EDDA"
C_BATT  = "#CCE5FF"
C_WARN  = "#F8D7DA"
C_GND   = "#2C5F2E"
C_PIPE  = "#6C757D"
C_AIR   = "#D0E8FF"   # airflow fill
C_VEST  = "#EEF5EE"   # vestibule interior
TITLE_COL = "#0F2D5E"


def title_block(ax, FW, sheet_n, sheet_total, title1, title2, scale_str):
    tb_y, tb_h = 0.05, 0.65
    ax.add_patch(mpatches.Rectangle((0.25, tb_y), FW - 0.5, tb_h,
                                    fc="white", ec=C_OUT, lw=1.5, zorder=6))
    for xd in [FW * 0.30, FW * 0.70]:
        ax.plot([xd, xd], [tb_y, tb_y + tb_h], color=C_OUT, lw=0.8, zorder=7)
    ax.text(FW * 0.15, tb_y + 0.44, "THE BIG SHOEBOX PROJECT",
            ha="center", va="center", fontsize=8.0, fontweight="bold",
            color=TITLE_COL, zorder=7)
    ax.text(FW * 0.15, tb_y + 0.28, "TBS-ELEC  ·  Light Trap & Ventilation",
            ha="center", va="center", fontsize=7.0, color=C_DIM, zorder=7)
    ax.text(FW * 0.15, tb_y + 0.13, "TBS-001  ·  20FT ISO CAMERA",
            ha="center", va="center", fontsize=6.5, color=C_DIM, zorder=7)
    ax.text(FW * 0.15, tb_y + 0.05, "© 2026 Alvin Richards — GNU AGPLv3",
            ha="center", va="center", fontsize=5.5, color=C_DIM, style="italic", zorder=7)
    ax.text(FW * 0.50, tb_y + 0.45, title1,
            ha="center", va="center", fontsize=11.0, fontweight="bold",
            color=C_OUT, zorder=7)
    ax.text(FW * 0.50, tb_y + 0.27, title2,
            ha="center", va="center", fontsize=7.5, color=C_DIM, zorder=7)
    ax.text(FW * 0.50, tb_y + 0.13, f"Scale: {scale_str}",
            ha="center", va="center", fontsize=7.0, color=C_DIM, zorder=7)
    ax.text(FW * 0.85, tb_y + 0.44, f"Sheet {sheet_n} of {sheet_total}",
            ha="center", va="center", fontsize=9.5, fontweight="bold",
            color=C_OUT, zorder=7)
    ax.text(FW * 0.85, tb_y + 0.27, "2026",
            ha="center", va="center", fontsize=8.0, color=C_DIM, zorder=7)


def ann(ax, text, xy, xytext, size=7.5):
    """Leader-line annotation with white-backed text."""
    ax.annotate(text, xy=xy, xytext=xytext,
                fontsize=size, color=C_OUT, ha="center", va="center",
                arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.9),
                bbox=dict(fc="white", ec="none", pad=1.5), zorder=10)


def dim_h(ax, x1, x2, y, text, col=C_DIM):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9), zorder=10)
    ax.text((x1+x2)/2, y + 0.18, text,
            ha="center", va="bottom", fontsize=7.5, color=col, zorder=10)


def dim_v(ax, x, y1, y2, text, col=C_DIM):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9), zorder=10)
    ax.text(x - 0.18, (y1+y2)/2, text,
            ha="right", va="center", fontsize=7.5, color=col, rotation=90, zorder=10)


# ─────────────────────────────────────────────────────────────────────────────
# SHEET 1 — Ventilation System
# Longitudinal container section (schematic, not to scale)
# Fan positions, cross-ventilation path, evap cooler, cable trunking
# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet1():
    FW, FH = 24.0, 16.0
    fig, ax = plt.subplots(figsize=(FW, FH), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, FW)
    ax.set_ylim(0, FH)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax.text(FW/2, FH - 0.38,
            "VENTILATION SYSTEM — CONTAINER LONGITUDINAL SECTION",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color=TITLE_COL)
    ax.text(FW/2, FH - 0.70,
            "TBS-001  ·  Longitudinal section (schematic, not to scale)  ·  "
            "Fan positions, cross-ventilation path, evap cooler  ·  "
            "Baffle duct assembly detail — see Sheet 2",
            ha="center", va="center", fontsize=8.0, color=C_DIM)

    # ── LEFT HALF: Container longitudinal section ────────────────────────────
    # Schematic box representing the container interior
    CX, CY = 1.8, 4.0      # container interior bottom-left
    CW, CH = 20.0, 7.0     # container interior drawing dimensions (schematic)
    WT = 0.35               # wall thickness (schematic)

    # Container shell
    ax.add_patch(mpatches.Rectangle((CX, CY), CW, CH,
                 fc="#F2F2EE", ec=C_OUT, lw=2.5, zorder=2))
    # Hatched walls
    for rx, ry, rw, rh in [
        (CX,       CY,      CW, WT),            # floor
        (CX,       CY+CH-WT, CW, WT),           # ceiling
        (CX,       CY+WT,   WT, CH-2*WT),       # left wall (image plane end)
        (CX+CW-WT, CY+WT,   WT, CH-2*WT),      # right wall (door/vestibule end)
    ]:
        ax.add_patch(mpatches.Rectangle((rx, ry), rw, rh,
                     fc=C_STEEL, ec=C_OUT, lw=0.5, zorder=3))

    # Interior label
    ax.text(CX + CW/2, CY + CH/2,
            "CONTAINER INTERIOR\n5,898mm long × 2,352mm wide",
            ha="center", va="center", fontsize=9.0, color=C_DIM,
            style="italic", zorder=3)

    # ── INTAKE FAN A (left end wall — image plane / far end, compact axial panel fan, low position) ──
    # Both fans are identical: 150mm compact axial panel fan, ~50mm body depth.
    # Same part, same mounting flange, same baffle duct — simplified procurement.
    import math
    PF_T  = 0.16   # panel fan body thickness in drawing units (~50mm, schematic)
    R_PF  = 0.38   # panel fan impeller radius (150mm dia, schematic)
    BD_W  = 0.80   # baffle duct schematic depth
    FA_Y  = CY + WT + CH * 0.18    # low position

    # Baffle duct box — between interior face of left wall and panel fan
    bd_a_x0 = CX + WT                      # right edge of left wall = duct left face
    ax.add_patch(mpatches.Rectangle((bd_a_x0, FA_Y - 0.40), BD_W, 0.80,
                 fc="#D8E8D8", ec=C_OUT, lw=0.9, zorder=5))
    ax.text(bd_a_x0 + BD_W / 2, FA_Y, "BAFFLE\nDUCT",
            ha="center", va="center", fontsize=5.5, color=C_DIM, zorder=6)

    # Grille indicator — tinted strip in left wall exterior face
    ax.add_patch(mpatches.Rectangle((CX, FA_Y - 0.40), WT, 0.80,
                 fc="#A8D8B0", ec=C_OUT, lw=0.7, zorder=5))
    ax.text(CX + WT / 2, FA_Y, "G", ha="center", va="center",
            fontsize=6.0, color=C_GND, fontweight="bold", zorder=6)

    # Panel fan body — thin rectangle immediately right of baffle duct
    FA_X   = bd_a_x0 + BD_W + PF_T / 2    # fan centre (impeller plane)
    pf_a_x0 = bd_a_x0 + BD_W              # left face of panel fan
    ax.add_patch(mpatches.Rectangle((pf_a_x0, FA_Y - R_PF - 0.08), PF_T, (R_PF + 0.08) * 2,
                 fc=C_ALUM, ec=C_OUT, lw=1.5, zorder=5))
    ax.add_patch(plt.Circle((FA_X, FA_Y), R_PF,
                 fc="none", ec=C_OUT, lw=1.2, zorder=6))
    ax.text(FA_X, FA_Y, "A", ha="center", va="center",
            fontsize=9, fontweight="bold", color=C_OUT, zorder=7)
    for angle in [0, 60, 120, 180, 240, 300]:
        bx = FA_X + R_PF * 0.80 * math.cos(math.radians(angle))
        by = FA_Y + R_PF * 0.80 * math.sin(math.radians(angle))
        ax.plot([FA_X, bx], [FA_Y, by], color=C_DIM, lw=1.2, alpha=0.5, zorder=6)

    # Airflow: exterior left → grille → baffle → fan (rightward into container)
    ax.annotate("", xy=(CX, FA_Y),
                xytext=(CX - 1.6, FA_Y),
                arrowprops=dict(arrowstyle="-|>", color=C_CL, lw=2.5), zorder=7)
    ax.text(CX - 1.8, FA_Y, "OUTSIDE\nAIR IN",
            ha="right", va="center", fontsize=8.0, color=C_CL, fontweight="bold")
    # Short interior distribution arrow from fan into container
    ax.annotate("", xy=(pf_a_x0 + PF_T + 0.65, FA_Y),
                xytext=(pf_a_x0 + PF_T + 0.05, FA_Y),
                arrowprops=dict(arrowstyle="-|>", color=C_CL, lw=1.2, alpha=0.6), zorder=6)

    ann(ax, "Cct A  |  150mm compact axial panel fan\n3A / 16AWG / 40W / 150+ CFM\n~50mm body depth",
        (FA_X, FA_Y + R_PF), (FA_X + 1.8, FA_Y + 2.2), size=7.5)
    ann(ax, "LOW POSITION\n~600mm AFF",
        (FA_X, FA_Y - R_PF), (FA_X + 1.2, FA_Y - 1.5), size=7.5)

    # ── EXHAUST FAN B (right end wall — cargo door end, identical compact axial panel fan, high position)
    # Same fan, duct, and mounting as Fan A.
    FB_Y  = CY + CH - WT - CH * 0.18   # high position

    # Baffle duct box — between interior face of right wall and panel fan
    bd_b_x0 = CX + CW - WT - BD_W     # left edge of baffle duct box
    ax.add_patch(mpatches.Rectangle((bd_b_x0, FB_Y - 0.40), BD_W, 0.80,
                 fc="#D8E8D8", ec=C_OUT, lw=0.9, zorder=5))
    ax.text(bd_b_x0 + BD_W / 2, FB_Y, "BAFFLE\nDUCT",
            ha="center", va="center", fontsize=5.5, color=C_DIM, zorder=6)

    # Grille indicator — tinted strip in right wall exterior face
    ax.add_patch(mpatches.Rectangle((CX + CW - WT, FB_Y - 0.40), WT, 0.80,
                 fc="#A8D8B0", ec=C_OUT, lw=0.7, zorder=5))
    ax.text(CX + CW - WT / 2, FB_Y, "G", ha="center", va="center",
            fontsize=6.0, color=C_GND, fontweight="bold", zorder=6)

    # Panel fan body — thin rectangle immediately left of baffle duct
    FB_X  = bd_b_x0 - PF_T / 2           # fan centre (impeller plane)
    pf_x0 = bd_b_x0 - PF_T               # left face of panel fan
    ax.add_patch(mpatches.Rectangle((pf_x0, FB_Y - R_PF - 0.08), PF_T, (R_PF + 0.08) * 2,
                 fc=C_ALUM, ec=C_OUT, lw=1.5, zorder=5))
    # Impeller circle on face
    ax.add_patch(plt.Circle((FB_X, FB_Y), R_PF,
                 fc="none", ec=C_OUT, lw=1.2, zorder=6))
    ax.text(FB_X, FB_Y, "B", ha="center", va="center",
            fontsize=9, fontweight="bold", color=C_OUT, zorder=7)
    # Blade lines
    for angle in [0, 60, 120, 180, 240, 300]:
        bx = FB_X + R_PF * 0.80 * math.cos(math.radians(angle))
        by = FB_Y + R_PF * 0.80 * math.sin(math.radians(angle))
        ax.plot([FB_X, bx], [FB_Y, by],
                color=C_DIM, lw=1.2, alpha=0.5, zorder=6)

    # Airflow: container → fan → baffle → grille → outside (rightward)
    ax.annotate("", xy=(CX + CW + 1.6, FB_Y),
                xytext=(CX + CW, FB_Y),
                arrowprops=dict(arrowstyle="-|>", color="#D32F2F", lw=2.5), zorder=7)
    ax.text(CX + CW + 1.8, FB_Y, "HOT AIR\nOUT",
            ha="left", va="center", fontsize=8.0, color="#D32F2F", fontweight="bold")
    # Short interior collection arrow into fan
    ax.annotate("", xy=(pf_x0 - 0.05, FB_Y),
                xytext=(pf_x0 - 0.65, FB_Y),
                arrowprops=dict(arrowstyle="-|>", color="#D32F2F", lw=1.2, alpha=0.6), zorder=6)

    ann(ax, "Cct B  |  150mm compact axial panel fan\n3A / 16AWG / 40W / 150+ CFM\n~50mm body depth  ·  275mm cone margin",
        (FB_X, FB_Y + R_PF), (FB_X - 2.0, FB_Y + 2.2), size=7.5)
    ann(ax, "HIGH POSITION\n~1,800mm AFF",
        (FB_X, FB_Y - R_PF), (FB_X - 1.2, FB_Y - 1.5), size=7.5)

    # ── EVAP COOLER (floor level, with baffled intake through bottom wall) ─────
    EC_X = CX + CW * 0.60
    EC_Y = CY + WT + 0.1
    EC_W, EC_H = 1.5, 0.9
    ax.add_patch(mpatches.FancyBboxPatch((EC_X, EC_Y), EC_W, EC_H,
                 boxstyle="round,pad=0.04", fc=C_SOLAR, ec=C_OUT, lw=1.5, zorder=5))
    ax.text(EC_X + EC_W/2, EC_Y + EC_H/2, "EVAP\nCOOLER\n(Cct E)",
            ha="center", va="center", fontsize=8.0, fontweight="bold",
            color=C_OUT, zorder=6)
    # Baffled intake stub on floor
    ax.add_patch(mpatches.Rectangle((EC_X + EC_W/2 - 0.18, CY), 0.36, WT,
                 fc="#A8D8B0", ec=C_OUT, lw=1.0, zorder=5))
    ax.annotate("Light-safe\nbaffled intake\n(150mm dia.)",
                xy=(EC_X + EC_W/2, CY - 0.1), xytext=(EC_X + EC_W/2, CY - 1.2),
                fontsize=7.5, color=C_DIM, ha="center",
                arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.9),
                bbox=dict(fc="white", ec="none", pad=1))
    ax.annotate("", xy=(EC_X + EC_W/2, CY - 0.1), xytext=(EC_X + EC_W/2, CY - 0.5),
                arrowprops=dict(arrowstyle="-|>", color=C_CL, lw=2.0), zorder=6)

    # ── Cross-ventilation airflow path ────────────────────────────────────────
    # Curved arrow from intake Fan A (left wall, low) diagonally to exhaust Fan B (right wall, high)
    ax.annotate("", xy=(FB_X - R_PF - 0.3, FB_Y),
                xytext=(FA_X + R_PF + 0.3, FA_Y),
                arrowprops=dict(arrowstyle="-|>", color=C_CL, lw=1.2,
                                connectionstyle="arc3,rad=-0.35",
                                alpha=0.6), zorder=4)
    ax.text(CX + CW/2, CY + CH/2 - 0.8,
            "cross-ventilation\npath (low → high)",
            ha="center", va="center", fontsize=7.5, color=C_CL,
            style="italic", alpha=0.7)

    # ── Cable trunking (top corner rail) ──────────────────────────────────────
    TK_Y = CY + CH - WT - 0.12
    ax.plot([CX + WT, CX + CW - WT], [TK_Y, TK_Y],
            color=C_PIPE, lw=4.0, solid_capstyle="round", zorder=4)
    ax.text((CX + WT + CX + CW - WT)/2, TK_Y + 0.22,
            "40 × 25mm PVC cable trunking  (Circuits A, B, D, E)",
            ha="center", va="bottom", fontsize=7.5, color=C_PIPE, fontweight="bold")
    # Drop conduits
    for dx, dy in [(FA_X, FA_Y + R_PF), (FB_X, FB_Y + R_PF),
                   (EC_X + EC_W/2, EC_Y + EC_H)]:
        ax.plot([dx, dx], [TK_Y, dy], color=C_PIPE, lw=0.9, linestyle=":", zorder=3)

    # Revolving drum light trap label on right (replaces old vestibule)
    ax.add_patch(mpatches.Rectangle((CX + CW, CY), 1.5, CH,
                 fc=C_VEST, ec=C_OUT, lw=1.5, linestyle="--", zorder=2))
    ax.text(CX + CW + 0.75, CY + CH/2, "DRUM\nLIGHT\nTRAP",
            ha="center", va="center", fontsize=7.0, color="#2D6A2D",
            fontweight="bold", rotation=90)

    # Operating modes table
    MX, MY = CX, CY - 1.1
    ax.add_patch(mpatches.FancyBboxPatch((MX - 0.1, MY - 1.45), CW + 0.2, 1.55,
                 boxstyle="round,pad=0.04", fc="#F8F9FA", ec=C_DIM, lw=0.8, zorder=2))
    ax.text(MX + CW/2, MY - 0.05, "FAN OPERATING MODES",
            ha="center", va="top", fontsize=9.0, fontweight="bold", color=C_OUT)
    modes = [
        ("EXPOSURE",               "OFF",        "OFF",        "OFF"),
        ("LOADING / DEVELOPMENT",  "Low speed",  "Low speed",  "ON"),
        ("POST-SESSION PURGE",     "Full speed", "Full speed", "OFF"),
        ("PRE-COOL (before entry)", "Full speed", "Full speed", "ON"),
    ]
    hdrs = ["MODE", "FAN A — panel (intake)", "FAN B — panel (exhaust)", "EVAP COOLER"]
    for ci, hdr in enumerate(hdrs):
        hx = MX + ci * (CW / 4)
        ax.text(hx + CW/8, MY - 0.30, hdr,
                ha="center", va="center", fontsize=7.8, fontweight="bold", color=C_OUT)
    ax.plot([MX, MX + CW], [MY - 0.46, MY - 0.46], color=C_OUT, lw=0.7)
    for ri, (mode, fa, fb, ec_m) in enumerate(modes):
        ry = MY - 0.60 - ri * 0.22
        vals = [mode, fa, fb, ec_m]
        for ci, val in enumerate(vals):
            vx = MX + ci * (CW / 4)
            ax.text(vx + CW/8, ry, val,
                    ha="center", va="center", fontsize=7.5,
                    color=C_OUT if ci == 0 else ("#D32F2F" if "OFF" in val else "#2E7D32"))

    title_block(ax, FW, 1, 2,
                "VENTILATION SYSTEM — CONTAINER LONGITUDINAL SECTION",
                "Cross-ventilation layout  ·  Fan positions  ·  Evap cooler  ·  Cable trunking",
                "Schematic — not to scale  ·  Baffle duct assembly detail — see Sheet 2")

    os.makedirs(SVG_DIR, exist_ok=True)
    plt.savefig("diagrams/lighttrap-sheet1.png", dpi=150, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.savefig(svg_path("diagrams/lighttrap-sheet1.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet1.png  Done.")


# ─────────────────────────────────────────────────────────────────────────────
# SHEET 2 — Fan + Baffle Duct + Wall Assembly
# Longitudinal cross-section through the fan axis showing how the fan,
# baffle duct housing, and container wall connect.
# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet2():
    import math
    FW, FH = 24.0, 14.0
    fig, ax = plt.subplots(figsize=(FW, FH), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, FW)
    ax.set_ylim(0, FH)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax.text(FW / 2, FH - 0.38,
            "FAN & BAFFLE DUCT — ASSEMBLY SECTION",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color=TITLE_COL)
    ax.text(FW / 2, FH - 0.72,
            "TBS-001  ·  Longitudinal section through fan axis  ·  Exterior left → Interior right  ·  "
            "Fan & baffle duct interior-mounted — wiring inside container  ·  Schematic NTS",
            ha="center", va="center", fontsize=8.0, color=C_DIM)

    # ── Layout constants ──────────────────────────────────────────────────────
    # Exterior zone:  x = 0  ..  WX
    # Container wall: x = WX  ..  WX+WT
    # Baffle duct:    x = WX+WT  ..  WX+WT+DD     (interior-mounted)
    # Fan body:       x = WX+WT+DD  ..  WX+WT+DD+FAN_LEN  (interior)
    # Interior zone:  x = WX+WT+DD+FAN_LEN  ..  FW
    WX      = 3.5    # exterior face of container wall
    WT      = 1.2    # wall thickness (schematic)
    DD      = 10.0   # duct depth (represents 300 mm)
    DH      = 5.5    # duct outer height (represents 200 mm)
    SK      = 0.35   # duct housing wall thickness (10 mm steel)
    AY      = 4.5    # bottom of duct assembly
    BF_T    = 0.30   # baffle plate thickness (minimum visible)
    FAN_LEN = 5.0    # fan body depth in drawing units
    FAN_D   = 4.5    # fan body height (represents ~150 mm dia)
    FAN_R   = FAN_D / 2

    DUCT_X  = WX + WT           # interior face of wall = duct left face
    DUCT_Y  = AY
    FAN_X   = DUCT_X + DD       # fan mounts on right (interior) face of duct
    FAN_CX  = FAN_X + FAN_LEN / 2
    FAN_CY  = DUCT_Y + DH / 2
    int_h   = DH - 2 * SK       # clear interior height
    int_d   = DD - SK           # clear interior depth (right side has fan flange)
    wall_y0, wall_y1 = AY - 1.0, AY + DH + 1.0

    # ── Container wall ────────────────────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle((WX, wall_y0), WT, wall_y1 - wall_y0,
                 fc=C_STEEL, ec=C_OUT, lw=2.0, zorder=4))
    for yi in range(int(wall_y0 * 4), int(wall_y1 * 4)):
        yy = yi / 4.0
        ax.plot([WX, WX + WT], [yy, yy + 0.3],
                color=C_OUT, lw=0.4, alpha=0.4, zorder=5)
    # Clear opening in wall for duct penetration
    ax.add_patch(mpatches.Rectangle((WX, AY + SK), WT, int_h,
                 fc="#F2F2EE", ec="none", zorder=5))
    ann(ax, "CONTAINER WALL\ncorrugated steel\n(shown schematic)",
        (WX + WT / 2, wall_y1 - 0.2), (WX - 1.2, wall_y1 + 0.6))

    # ── Weatherproof louvre grille (exterior face of wall) ────────────────────
    GL_W = 0.45    # grille frame depth (protruding exterior)
    GL_H = DH * 0.65
    GL_Y = DUCT_Y + DH / 2 - GL_H / 2
    # Grille frame
    ax.add_patch(mpatches.Rectangle((WX - GL_W, GL_Y), GL_W, GL_H,
                 fc="#D0D8C8", ec=C_OUT, lw=1.2, zorder=6))
    # Louvre slats (5 horizontal angled slats)
    slat_h = 0.10
    slat_gap = GL_H / 6
    for i in range(5):
        sy = GL_Y + slat_gap * (i + 0.5)
        # Angled slat: left edge lower than right (rain-shedding angle)
        ax.add_patch(mpatches.FancyBboxPatch(
            (WX - GL_W + 0.05, sy - slat_h / 2), GL_W - 0.10, slat_h,
            boxstyle="round,pad=0.01", fc=C_DIM, ec="none", zorder=7, alpha=0.75))
    ann(ax, "Weatherproof louvre grille\n(no fan — passive inlet/outlet)\n150mm dia. round → rect adapter",
        (WX - GL_W / 2, GL_Y - 0.15), (WX - GL_W / 2 - 1.5, GL_Y - 1.4))

    # ── Baffle duct housing (interior-mounted, left face open to wall) ────────
    ax.add_patch(mpatches.Rectangle((DUCT_X, DUCT_Y), DD, DH,
                 fc="#F5F5F5", ec=C_OUT, lw=2.0, zorder=3))
    # Housing walls: top, bottom only — left (exterior) is open to wall, right (fan) has mounting flange
    for rx, ry, rw, rh in [
        (DUCT_X, DUCT_Y,        DD, SK),         # bottom wall
        (DUCT_X, DUCT_Y+DH-SK,  DD, SK),         # top wall
    ]:
        ax.add_patch(mpatches.Rectangle((rx, ry), rw, rh,
                     fc=C_STEEL, ec=C_OUT, lw=0.8, zorder=4))
    # Flat black interior
    ax.add_patch(mpatches.Rectangle((DUCT_X, DUCT_Y + SK), DD, int_h,
                 fc="#2A2A2A", ec="none", zorder=2, alpha=0.12))

    # Wall mounting flange — secures duct to interior face of container wall
    FL_W = 1.0    # flange overhang (top and bottom)
    FL_T = 0.22   # flange plate thickness
    ax.add_patch(mpatches.Rectangle((DUCT_X, DUCT_Y - FL_W), FL_T, DH + 2 * FL_W,
                 fc=C_ALUM, ec=C_OUT, lw=1.2, zorder=6))
    for by in [DUCT_Y - FL_W * 0.55, DUCT_Y + DH + FL_W * 0.55]:
        ax.plot(DUCT_X + FL_T / 2, by, "o", color=C_OUT, ms=4, zorder=7)
    ann(ax, "Wall mounting flange\n5mm plate · 4×M10 bolts\n(interior face of wall)",
        (DUCT_X + FL_T / 2, DUCT_Y - FL_W - 0.15),
        (DUCT_X + FL_T / 2 + 0.5, DUCT_Y - FL_W - 1.3))

    # ── Baffles inside duct ───────────────────────────────────────────────────
    # Baffle 1: from TOP, at 30% depth — gap at BOTTOM
    # Baffle 2: from BOTTOM, at 70% depth — gap at TOP
    B1_X = DUCT_X + int_d * 0.30
    B1_H = int_h * 0.65
    B1_Y = DUCT_Y + SK + int_h - B1_H      # top-anchored
    ax.add_patch(mpatches.Rectangle((B1_X, B1_Y), BF_T, B1_H,
                 fc=C_OUT, ec=C_OUT, lw=0.5, zorder=5))

    B2_X = DUCT_X + int_d * 0.70
    B2_H = int_h * 0.65
    B2_Y = DUCT_Y + SK                     # bottom-anchored
    ax.add_patch(mpatches.Rectangle((B2_X, B2_Y), BF_T, B2_H,
                 fc=C_OUT, ec=C_OUT, lw=0.5, zorder=5))

    ann(ax, "Baffle 1\n(from top, 65%)\ngap at bottom",
        (B1_X + BF_T / 2, B1_Y + B1_H * 0.6),
        (B1_X - 1.5, B1_Y + B1_H * 0.6 + 1.0))
    ann(ax, "Baffle 2\n(from bottom, 65%)\ngap at top",
        (B2_X + BF_T / 2, B2_Y + B2_H * 0.4),
        (B2_X + 1.5, B2_Y + B2_H * 0.4 - 0.9))
    ax.text(DUCT_X + DD / 2, DUCT_Y + SK + int_h * 0.5,
            "FLAT BLACK\nPOWDER COAT\nALL INTERIOR FACES",
            ha="center", va="center", fontsize=7.0, color="#808080",
            style="italic", alpha=0.85, zorder=9)

    # ── Fan body — compact axial panel fan (both Fan A and Fan B identical) ─────
    # Panel fan: ~50mm body depth, 150mm dia. One part number for both fans.
    FM_T  = 0.22     # mounting flange plate thickness
    PF_BD = 0.80     # panel fan body depth in drawing units (~50mm schematic)
    PF_R  = FAN_R    # impeller radius = FAN_R (150mm dia)

    # Mounting flange at right face of duct
    ax.add_patch(mpatches.Rectangle((FAN_X - FM_T, DUCT_Y - FL_W), FM_T, DH + 2 * FL_W,
                 fc=C_ALUM, ec=C_OUT, lw=1.2, zorder=6))
    for by in [DUCT_Y - FL_W * 0.55, DUCT_Y + DH + FL_W * 0.55]:
        ax.plot(FAN_X - FM_T / 2, by, "o", color=C_OUT, ms=4, zorder=7)
    ann(ax, "Fan mounting flange\n5mm plate · 4×M10 bolts\n(same both fans)",
        (FAN_X - FM_T / 2, DUCT_Y + DH + FL_W + 0.15),
        (FAN_X - FM_T / 2, DUCT_Y + DH + FL_W + 1.2))

    # Panel fan body — thin rectangle (shallow depth, ~50mm) with impeller on INLET face.
    # Impeller circle drawn on LEFT (inlet) face so orientation is unambiguous:
    # viewing the fan from the inlet side = you see the blades face-on.
    # Air enters LEFT face, exits RIGHT face (intake mode; reversed for exhaust).
    ax.add_patch(mpatches.Rectangle((FAN_X, FAN_CY - PF_R - 0.15), PF_BD, (PF_R + 0.15) * 2,
                 fc=C_ALUM, ec=C_OUT, lw=1.8, zorder=5))
    # Impeller disc on INLET (left) face — represents view along fan axis from inlet
    ax.add_patch(plt.Circle((FAN_X, FAN_CY), PF_R * 0.90,
                 fc="#E8EEF4", ec=C_OUT, lw=1.5, zorder=6))
    # Blade lines (fan blades as seen from inlet)
    for angle in range(0, 360, 45):
        bx = FAN_X + PF_R * 0.82 * math.cos(math.radians(angle))
        by = FAN_CY + PF_R * 0.82 * math.sin(math.radians(angle))
        ax.plot([FAN_X, bx], [FAN_CY, by],
                color=C_DIM, lw=1.4, alpha=0.60, zorder=7)
    # Motor hub at centre
    ax.add_patch(plt.Circle((FAN_X, FAN_CY), PF_R * 0.18,
                 fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=8))
    # INLET / OUTLET face labels
    ax.text(FAN_X, FAN_CY + PF_R + 0.30, "INLET\n(air enters)",
            ha="center", va="bottom", fontsize=7.0, color=C_CL, fontweight="bold", zorder=10)
    ax.text(FAN_X + PF_BD, FAN_CY + PF_R + 0.30, "OUTLET\n(air exits)",
            ha="center", va="bottom", fontsize=7.0, color="#D32F2F", fontweight="bold", zorder=10)
    # Axis direction note below fan
    ax.text(FAN_X + PF_BD / 2, FAN_CY - PF_R - 0.30,
            "← FAN AXIS HORIZONTAL →\nair flows along this axis",
            ha="center", va="top", fontsize=7.0, color=C_DIM, style="italic", zorder=10)

    # Wiring run from fan into container interior
    WR_X = FAN_X + PF_BD + 0.15
    ax.plot([WR_X, WR_X + 2.5], [FAN_CY - PF_R * 0.35, FAN_CY - PF_R * 0.35],
            color=C_PIPE, lw=2.5, solid_capstyle="round", zorder=5)
    ax.text(WR_X + 2.65, FAN_CY - PF_R * 0.35,
            "16 AWG wiring → Cct A/B\n→ electrical panel\n(all inside container)",
            ha="left", va="center", fontsize=7.5, color=C_PIPE, zorder=10)

    ax.text(FAN_X + PF_BD * 6, FAN_CY + PF_R - 0.65, #FAN_CY - PF_R - 0.55,
            "150mm COMPACT AXIAL PANEL FAN  ·  Fan A (intake) and Fan B (exhaust) — identical\n"
            "Cct A/B  ·  40W  ·  150+ CFM  ·  ~50mm body depth  ·  Interior-mounted",
            ha="center", va="top", fontsize=8.0, fontweight="bold", color=C_OUT, zorder=10)

    # ── Airflow arrows (intake mode shown — exhaust is identical, reversed) ───
    mid_y = FAN_CY
    gap1_h = int_h * 0.35
    gap1_y = DUCT_Y + SK
    gap2_h = int_h * 0.35
    gap2_y = DUCT_Y + SK + int_h - gap2_h
    y_gap1 = gap1_y + gap1_h / 2
    y_gap2 = gap2_y + gap2_h / 2
    pc, plw = C_CL, 1.6

    # Exterior: outside → grille
    ax.annotate("", xy=(WX - GL_W, mid_y), xytext=(WX - GL_W - 1.8, mid_y),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=2.5), zorder=8)
    ax.text(WX - GL_W - 2.0, mid_y, "OUTSIDE\nAIR IN",
            ha="right", va="center", fontsize=9.0, color=pc, fontweight="bold", zorder=10)
    # Through wall opening into duct
    ax.annotate("", xy=(DUCT_X + 0.3, mid_y), xytext=(WX + WT - 0.1, mid_y),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    # S-path through baffles
    ax.annotate("", xy=(B1_X - 0.4, y_gap1), xytext=(B1_X - 0.4, mid_y),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    ax.annotate("", xy=(B1_X + BF_T + 0.4, y_gap1), xytext=(B1_X - 0.1, y_gap1),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    ax.annotate("", xy=(B2_X - 0.4, y_gap2), xytext=(B2_X - 0.4, y_gap1),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    ax.annotate("", xy=(B2_X + BF_T + 0.4, y_gap2), xytext=(B2_X - 0.1, y_gap2),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    # Exit baffle → fan inlet
    ax.annotate("", xy=(FAN_X - 0.1, mid_y), xytext=(B2_X + BF_T + 0.6, mid_y),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    # Fan → interior container
    ax.annotate("", xy=(FAN_X + PF_BD + 1.8, mid_y),
                xytext=(FAN_X + PF_BD + 0.2, mid_y),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=2.5), zorder=8)
    ax.text(FAN_X + PF_BD + 2.0, mid_y, "INTO\nCONTAINER",
            ha="left", va="center", fontsize=9.0, color=pc, fontweight="bold", zorder=10)
    ax.text(FAN_X + PF_BD + 2.0, mid_y - FAN_R - 0.3,
            "(exhaust: flow reversed — same assembly)",
            ha="left", va="top", fontsize=7.0, color=C_DIM, style="italic", zorder=10)

    # ── Zone labels ───────────────────────────────────────────────────────────
    ax.text(WX / 2, wall_y0 - 0.3, "EXTERIOR",
            ha="center", va="top", fontsize=9.0, color=C_DIM, fontweight="bold", zorder=10)
    ax.text(DUCT_X + (FAN_X + PF_BD - DUCT_X) / 2, wall_y0 + 0.5,
            "INTERIOR (container)",
            ha="center", va="top", fontsize=9.0, color=C_DIM, fontweight="bold", zorder=10)
    ax.plot([WX + WT / 2, WX + WT / 2], [wall_y0 - 0.6, wall_y0 - 0.15],
            color=C_DIM, lw=1.0, ls=":")

    # ── Dimension lines ───────────────────────────────────────────────────────
    dim_h(ax, DUCT_X, DUCT_X + DD, DUCT_Y - 1.1, "300 mm  (duct depth)")
    dim_v(ax, DUCT_X - 1.85, DUCT_Y, DUCT_Y + DH, "200 mm")
    dim_h(ax, WX, WX + WT, DUCT_Y + DH + 0.7, "wall")
    ax.plot([WX, WX], [DUCT_Y + DH, DUCT_Y + DH + 0.85], color=C_DIM, lw=0.5, ls=":")
    ax.plot([WX + WT, WX + WT], [DUCT_Y + DH, DUCT_Y + DH + 0.85], color=C_DIM, lw=0.5, ls=":")
    dim_h(ax, FAN_X, FAN_X + PF_BD, DUCT_Y - 1.0, "~50 mm  (panel fan body)")

    # ── Shadow margin / procurement note ─────────────────────────────────────
    NX, NY = FW - 9.5 - 0.3, 1.6
    ax.add_patch(mpatches.FancyBboxPatch((NX, NY), 9.5, 1.6,
                 boxstyle="round,pad=0.08", fc="#F0F8FF", ec=C_CL, lw=1.0, zorder=9))
    ax.text(NX + 0.20, NY + 1.35,
            "BOTH FANS — 150mm COMPACT AXIAL PANEL FAN  ·  ONE PART NUMBER",
            ha="left", va="center", fontsize=8.5, fontweight="bold", color=C_CL, zorder=10)
    ax.text(NX + 0.20, NY + 1.00,
            "Fan A (intake, right end) and Fan B (exhaust, left end) are identical.\n"
            "Same fan body, same mounting flange, same baffle duct — simplified fabrication and procurement.",
            ha="left", va="center", fontsize=7.5, color=C_OUT, zorder=10)
    ax.text(NX + 0.20, NY + 0.58,
            "Total depth from wall (each):  300mm baffle duct + 50mm fan = 350mm",
            ha="left", va="center", fontsize=7.5, color=C_OUT, zorder=10)
    ax.text(NX + 0.20, NY + 0.25,
            "Shadow margins:  Fan A → +894mm clear of cone right edge  ·  Fan B → +275mm clear of cone left edge  ✓",
            ha="left", va="center", fontsize=7.5, color="#2E7D32", fontweight="bold", zorder=10)

    title_block(ax, FW, 2, 2,
                "FAN & BAFFLE DUCT — ASSEMBLY SECTION",
                "Interior-mounted fan  ·  Passive louvre grille (exterior only)  ·  "
                "Baffle duct interior-mounted  ·  All wiring inside container",
                "Schematic NTS  ·  Refer to Sheet 1 for container section")

    plt.savefig("diagrams/lighttrap-sheet2.png", dpi=150, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.savefig(svg_path("diagrams/lighttrap-sheet2.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet2.png  Done.")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating TBS-001 Light Trap & Ventilation diagrams...")
    draw_sheet1()
    draw_sheet2()
    print("Done.")
