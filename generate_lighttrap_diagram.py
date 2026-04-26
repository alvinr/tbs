#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_lighttrap_diagram.py
TBS-001  Light Trap Vestibule & Ventilation System — two drawing sheets.

Sheet 1: Light trap vestibule — top-down plan cross-section showing S-path
Sheet 2: Ventilation system — longitudinal container section + fan baffle detail
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Arc, FancyArrowPatch

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
C_CURTAIN = "#3A1A10" # Duvetyne (dark brown-black)
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
                bbox=dict(fc="white", ec="none", pad=1.5), zorder=8)


def dim_h(ax, x1, x2, y, text, col=C_DIM):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9))
    ax.text((x1+x2)/2, y + 0.18, text,
            ha="center", va="bottom", fontsize=7.5, color=col)


def dim_v(ax, x, y1, y2, text, col=C_DIM):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9))
    ax.text(x - 0.18, (y1+y2)/2, text,
            ha="right", va="center", fontsize=7.5, color=col, rotation=90)


# ─────────────────────────────────────────────────────────────────────────────
# SHEET 1 — Light Trap Vestibule — Plan View (top-down cross-section)
# Scale 1:100  (1 drawing unit = 100 mm)
# Vestibule: 2,400 mm wide × 1,200 mm deep
# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet1():
    FW, FH = 26.0, 24.0
    fig, ax = plt.subplots(figsize=(FW, FH), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, FW)
    ax.set_ylim(0, FH)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax.text(FW/2, FH - 0.38,
            "LIGHT TRAP VESTIBULE — PLAN CROSS-SECTION (top-down)",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color=TITLE_COL)
    ax.text(FW/2, FH - 0.70,
            "TBS-001  ·  Scale 1:100  ·  All dimensions in mm  ·  "
            "Section cut at standing height (~1,500mm AFF)",
            ha="center", va="center", fontsize=8.0, color=C_DIM)

    # Scale: 1 unit = 100 mm
    S = 1 / 100.0

    # Vestibule real dimensions (mm)
    V_W  = 2400   # vestibule width (along long axis of container wall)
    V_D  = 1200   # vestibule depth (away from container)
    WT   = 120    # schematic wall/baffle thickness mm
    DOOR = 900    # exterior door clear opening mm

    # Drawing origin — container inner face at bottom of vestibule
    OX, OY = 1.3, 7.0

    vw = V_W * S   # 24.0 units
    vd = V_D * S   # 12.0 units
    wt = WT  * S   # 1.2 units
    dw = DOOR* S   # 9.0 units

    # ── Container wall (bottom of vestibule) ─────────────────────────────────
    # Show container end wall as hatched steel block
    ax.add_patch(mpatches.Rectangle((OX, OY - wt * 1.5), vw, wt * 1.5,
                 fc=C_STEEL, ec=C_OUT, lw=2.0, zorder=3))
    ax.text(OX + vw/2, OY - wt * 0.75,
            "CONTAINER CARGO-DOOR END WALL  (ISO corner castings)",
            ha="center", va="center", fontsize=8.5, fontweight="bold",
            color=C_OUT, zorder=4)

    # Hatch lines on wall
    for xi in range(1, 12):
        ax.plot([OX + xi*2, OX + xi*2 + wt*1.5],
                [OY - wt*1.5, OY],
                color=C_OUT, lw=0.4, alpha=0.5, zorder=4)

    # ── Side walls of vestibule ───────────────────────────────────────────────
    # Left wall
    ax.add_patch(mpatches.Rectangle((OX, OY), wt, vd,
                 fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=3))
    # Right wall
    ax.add_patch(mpatches.Rectangle((OX + vw - wt, OY), wt, vd,
                 fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=3))

    # ── Exterior wall (top of vestibule) with door opening ───────────────────
    door_x1 = OX + (vw - dw) / 2   # centre the door
    door_x2 = door_x1 + dw
    # Left section of exterior wall
    ax.add_patch(mpatches.Rectangle((OX, OY + vd), door_x1 - OX, wt,
                 fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=3))
    # Right section
    ax.add_patch(mpatches.Rectangle((door_x2, OY + vd), OX + vw - door_x2, wt,
                 fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=3))
    # Door panel (closed, shown as thin rectangle)
    ax.add_patch(mpatches.Rectangle((door_x1, OY + vd), dw, wt * 0.3,
                 fc="white", ec=C_OUT, lw=1.2, zorder=4))
    # Door swing arc
    ax.add_patch(Arc((door_x1, OY + vd), 2*dw, 2*dw,
                     angle=0, theta1=0, theta2=90,
                     color=C_DIM, lw=0.8, linestyle=":", zorder=3))
    ax.text(OX + vw/2, OY + vd + wt * 0.15,
            "EXTERIOR DOOR  900mm clear  (outward-opening, compression latch)",
            ha="center", va="center", fontsize=7.5, fontweight="bold",
            color=C_OUT, zorder=5)

    # ── Vestibule interior fill ───────────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle((OX + wt, OY), vw - 2*wt, vd,
                 fc=C_VEST, ec="none", zorder=2))

    # ── BAFFLE 1: from left wall, at 30% depth ────────────────────────────────
    # Spans 58% of interior width (left to right)
    BF_SPAN = 0.58 * (vw - 2*wt)  # 58% of clear interior width
    B1_Y = OY + vd * 0.30         # 30% from container end
    ax.add_patch(mpatches.Rectangle((OX + wt, B1_Y), BF_SPAN, wt * 0.8,
                 fc=C_OUT, ec=C_OUT, lw=1.0, zorder=5))
    # Gap indicator
    gap_x1 = OX + wt + BF_SPAN
    gap_x2 = OX + vw - wt
    ax.add_patch(mpatches.Rectangle((gap_x1, B1_Y - 0.2), gap_x2 - gap_x1, wt * 0.8 + 0.4,
                 fc="#FFFDE7", ec=C_CL, lw=1.0, linestyle="--", zorder=4))
    ax.text((gap_x1 + gap_x2)/2, B1_Y + wt * 0.4,
            "GAP\n1,000mm", ha="center", va="center",
            fontsize=7.0, color=C_CL, fontweight="bold", zorder=6)

    # ── BAFFLE 2: from right wall, at 65% depth ───────────────────────────────
    B2_Y = OY + vd * 0.65
    ax.add_patch(mpatches.Rectangle((OX + vw - wt - BF_SPAN, B2_Y), BF_SPAN, wt * 0.8,
                 fc=C_OUT, ec=C_OUT, lw=1.0, zorder=5))
    gap2_x1 = OX + wt
    gap2_x2 = OX + vw - wt - BF_SPAN
    ax.add_patch(mpatches.Rectangle((gap2_x1 - 0.2, B2_Y - 0.2), gap2_x2 - gap2_x1 + 0.4, wt * 0.8 + 0.4,
                 fc="#FFFDE7", ec=C_CL, lw=1.0, linestyle="--", zorder=4))
    ax.text((gap2_x1 + gap2_x2)/2, B2_Y + wt * 0.4,
            "GAP\n1,000mm", ha="center", va="center",
            fontsize=7.0, color=C_CL, fontweight="bold", zorder=6)

    # ── Duvetyne curtains (3 layers at container door end) ────────────────────
    for ci, cx_off in enumerate([0.3, 0.6, 0.9]):
        cx = OX + wt + cx_off
        ax.plot([cx, cx], [OY, OY + 2.5],
                color=C_CURTAIN, lw=3.5 - ci * 0.8, alpha=0.85, zorder=5)
    ax.text(OX + wt + 1.4, OY + 1.5,
            "3 layers\nRosco Duvetyne\nblackout curtain\n(200mm overlap each)",
            ha="left", va="center", fontsize=7.5, color=C_CURTAIN, zorder=6,
            bbox=dict(fc="white", ec="none", pad=1))

    # ── Safelight D (red LED strip on ceiling/wall) ───────────────────────────
    sl_x = OX + vw - wt - 1.5
    sl_y = OY + vd * 0.10
    ax.add_patch(mpatches.Rectangle((sl_x - 1.2, sl_y - 0.15), 2.4, 0.30,
                 fc="#FF6B6B", ec=C_OUT, lw=0.8, zorder=5))
    ax.text(sl_x, sl_y, "SAFELIGHT\nCct D  (red LED)", ha="center", va="center",
            fontsize=7.0, color="white", fontweight="bold", zorder=6)

    # ── Ventilation stub ──────────────────────────────────────────────────────
    vent_y = OY + vd * 0.50
    ax.add_patch(mpatches.Rectangle((OX - 0.8, vent_y - 0.4), 0.8, 0.8,
                 fc="#A8D8B0", ec=C_OUT, lw=1.0, zorder=5))
    ax.text(OX - 0.4, vent_y, "VENT\nSTUB", ha="center", va="center",
            fontsize=6.5, color=C_OUT, zorder=6)
    ax.annotate("4\" duct stub\n(cap when loading;\nopen during processing)",
                xy=(OX - 0.8, vent_y), xytext=(OX - 3.0, vent_y),
                fontsize=7.5, color=C_DIM, ha="right", va="center",
                arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.9),
                bbox=dict(fc="white", ec="none", pad=1))

    # ── S-path travel arrows ──────────────────────────────────────────────────
    path_col = "#1565C0"
    path_lw = 2.2
    # Step 1: enter from container, go up toward baffle 1 (in right-side gap)
    px = OX + vw - wt - 1.5   # path x (right zone)
    ax.annotate("", xy=(px, B1_Y - 0.3), xytext=(px, OY + 1.5),
                arrowprops=dict(arrowstyle="-|>", color=path_col, lw=path_lw), zorder=7)
    # Step 2: cross left through baffle 1 gap
    ax.annotate("", xy=(OX + wt + 1.0, B1_Y + wt * 0.4 + 0.4),
                xytext=(gap_x1 + 0.3, B1_Y + wt * 0.4 + 0.4),
                arrowprops=dict(arrowstyle="-|>", color=path_col, lw=path_lw), zorder=7)
    # Step 3: go up in left zone toward baffle 2 gap
    px2 = OX + wt + 1.0
    ax.annotate("", xy=(px2, B2_Y - 0.3), xytext=(px2, B1_Y + wt * 0.4 + 0.7),
                arrowprops=dict(arrowstyle="-|>", color=path_col, lw=path_lw), zorder=7)
    # Step 4: cross right through baffle 2 gap
    ax.annotate("", xy=(gap2_x2 - 0.2 + 1.5, B2_Y + wt * 0.4 + 0.4),
                xytext=(gap2_x1 - 0.0, B2_Y + wt * 0.4 + 0.4),
                arrowprops=dict(arrowstyle="-|>", color=path_col, lw=path_lw), zorder=7)
    # Step 5: go up and out
    px3 = OX + vw / 2
    ax.annotate("", xy=(px3, OY + vd + wt + 0.4), xytext=(px3, B2_Y + wt + 0.7),
                arrowprops=dict(arrowstyle="-|>", color=path_col, lw=path_lw), zorder=7)

    # Path label
    ax.text(OX + vw * 0.52, OY + vd * 0.50,
            "S-PATH\n(no direct\nline of sight)",
            ha="center", va="center", fontsize=9.0,
            fontweight="bold", color=path_col, zorder=8,
            bbox=dict(fc="white", ec=path_col, pad=3, lw=0.8, alpha=0.9))

    # ── Dimension lines ───────────────────────────────────────────────────────
    DY_BOT = OY - wt * 1.5 - 0.8
    DX_L = OX - 1.2

    # Vestibule width
    dim_h(ax, OX, OX + vw, DY_BOT - 0.5, "2,400 mm  (vestibule width)")
    ax.plot([OX, OX], [OY - wt*1.5, DY_BOT - 0.5], color=C_DIM, lw=0.5, linestyle=":")
    ax.plot([OX+vw, OX+vw], [OY - wt*1.5, DY_BOT - 0.5], color=C_DIM, lw=0.5, linestyle=":")

    # Door opening
    dim_h(ax, door_x1, door_x2, DY_BOT, "900 mm  (door clear)")
    ax.plot([door_x1, door_x1], [OY + vd, DY_BOT], color=C_DIM, lw=0.5, linestyle=":")
    ax.plot([door_x2, door_x2], [OY + vd, DY_BOT], color=C_DIM, lw=0.5, linestyle=":")

    # Vestibule depth
    dim_v(ax, DX_L, OY, OY + vd, "1,200 mm  (vestibule depth)")
    ax.plot([OX, DX_L], [OY, OY], color=C_DIM, lw=0.5, linestyle=":")
    ax.plot([OX, DX_L], [OY+vd, OY+vd], color=C_DIM, lw=0.5, linestyle=":")

    # Baffle positions
    dim_v(ax, DX_L - 1.2, OY, B1_Y, "360 mm", col="#888888")
    dim_v(ax, DX_L - 1.2, B1_Y, B2_Y, "420 mm", col="#888888")
    dim_v(ax, DX_L - 1.2, B2_Y, OY + vd, "420 mm", col="#888888")

    # Baffle length
    dim_h(ax, OX + wt, OX + wt + BF_SPAN,
          OY + vd + wt + 0.6, "1,400 mm  (baffle span)")

    # ── Material callout key ──────────────────────────────────────────────────
    KX = OX + vw + 1.5
    KY = OY + vd + wt
    ax.text(KX, KY, "CONSTRUCTION NOTES",
            ha="left", va="top", fontsize=9.5,
            fontweight="bold", color=C_OUT)
    ax.plot([KX, KX + 7.0], [KY - 0.25, KY - 0.25],
            color=C_OUT, lw=1.0)

    notes = [
        ("FRAME",
         "40 × 40 mm RHS steel, hot-dip galvanised",
         "Bolt to ISO corner castings — M10 × 50mm × 8 off\nNo welding to container required"),
        ("WALLS / ROOF",
         "18mm exterior-grade plywood, both faces",
         "Interior: flat black paint (zero sheen)\nExterior: weatherproof sealant + paint"),
        ("BAFFLES (×2)",
         "3mm mild steel plate, floor-to-ceiling",
         "Flat black paint, both faces\nBolted to side walls via M8 × 25mm bolts"),
        ("CURTAINS (×3)",
         "Rosco Duvetyne 100% blackout fabric",
         "Velcro-tab rail, 200mm overlap per layer\nHung at container-door end of vestibule"),
        ("DOOR",
         "900mm × 2,000mm, outward-opening",
         "Full-height piano hinge\nCompression latch, weatherstripped perimeter"),
        ("SAFELIGHT",
         "12V red LED strip — Circuit D",
         "Switched from inside\nNo UV component — safe during sensitiser coating"),
        ("VENT STUB",
         "4\" duct with weatherproof cap",
         "Cap during film loading\nOpen + connect to ventilation during processing"),
    ]
    for j, (hdr, spec, detail) in enumerate(notes):
        ny = KY - 0.55 - j * 1.05
        ax.text(KX, ny, hdr + ":",
                ha="left", va="top", fontsize=8.5,
                fontweight="bold", color=C_OUT)
        ax.text(KX + 0.15, ny - 0.28, spec,
                ha="left", va="top", fontsize=7.8, color=C_OUT)
        ax.text(KX + 0.15, ny - 0.55, detail,
                ha="left", va="top", fontsize=7.2, color=C_DIM)

    # ── Install sequence note ─────────────────────────────────────────────────
    nx, ny2 = OX, 1.1
    ax.add_patch(FancyBboxPatch((nx - 0.1, ny2 - 0.15), 15.0, 1.6,
                 boxstyle="round,pad=0.04", fc="#F8F9FA", ec=C_DIM, lw=0.8, zorder=2))
    ax.text(nx + 0.10, ny2 + 1.28, "INSTALLATION SEQUENCE:",
            ha="left", va="center", fontsize=8.5, fontweight="bold", color=C_OUT)
    install = [
        "1.  Fabricate RHS frame. Galvanise before installation.",
        "2.  Bolt frame to ISO corner castings (M10 × 50mm, 8 bolts). Check plumb and square.",
        "3.  Fix 18mm ply cladding to frame with TEK screws. Seal all exterior joints.",
        "4.  Install baffle plates to side walls. Paint all interior surfaces flat black — two coats.",
        "5.  Fit exterior door (piano hinge, full height). Install compression latch.",
        "6.  Hang Duvetyne curtains (3 layers, Velcro rail). Test: each layer must fully overlap the next.",
        "7.  Wire safelight from Circuit D branch (run conduit through sealed penetration in container wall).",
        "8.  Light-leak test per Operating Manual Phase 0.7. Target: zero light after 15min dark adaptation.",
    ]
    col1 = [install[i] for i in range(0, len(install), 2)]
    col2 = [install[i] for i in range(1, len(install), 2)]
    for ri, (s1, s2) in enumerate(zip(col1, col2)):
        ax.text(nx + 0.15, ny2 + 0.98 - ri * 0.28, s1,
                ha="left", va="center", fontsize=7.2, color=C_DIM)
        ax.text(nx + 7.65, ny2 + 0.98 - ri * 0.28, s2,
                ha="left", va="center", fontsize=7.2, color=C_DIM)

    title_block(ax, FW, 1, 2,
                "LIGHT TRAP VESTIBULE — PLAN CROSS-SECTION",
                "S-path baffle layout  ·  Materials  ·  Installation notes",
                "1:100  (1 unit = 100 mm)")

    plt.savefig("diagrams/lighttrap-sheet1.png", dpi=150, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet1.png  Done.")


# ─────────────────────────────────────────────────────────────────────────────
# SHEET 2 — Ventilation System
# Left: longitudinal container section (schematic, not to scale)
# Right: fan light-safe baffle detail (scale 1:10)
# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet2():
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
            "VENTILATION SYSTEM — CONTAINER SECTION & FAN BAFFLE DETAIL",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color=TITLE_COL)
    ax.text(FW/2, FH - 0.70,
            "TBS-001  ·  Left: container longitudinal section (schematic, not to scale)  ·  "
            "Right: fan light-safe baffle detail (scale 1:10)",
            ha="center", va="center", fontsize=8.0, color=C_DIM)

    # ── LEFT HALF: Container longitudinal section ────────────────────────────
    # Schematic box representing the container interior
    CX, CY = 0.8, 4.0      # container interior bottom-left
    CW, CH = 13.0, 7.0     # container interior drawing dimensions (schematic)
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

    # ── INTAKE FAN A (right end wall — interior-mounted, low position) ──────────
    import math
    R_FAN = 0.45
    BD_W  = 0.80    # baffle duct schematic depth (between wall interior face and fan body)
    FA_Y  = CY + WT + CH * 0.18    # low position (unchanged)

    # Baffle duct box — between interior face of right wall and fan body
    bd_a_x0 = CX + CW - WT - BD_W         # left edge of baffle duct box
    ax.add_patch(mpatches.Rectangle((bd_a_x0, FA_Y - 0.40), BD_W, 0.80,
                 fc="#D8E8D8", ec=C_OUT, lw=0.9, zorder=5))
    ax.text(bd_a_x0 + BD_W / 2, FA_Y, "BAFFLE\nDUCT",
            ha="center", va="center", fontsize=5.5, color=C_DIM, zorder=6)

    # Grille indicator — tinted strip in right wall exterior face
    ax.add_patch(mpatches.Rectangle((CX + CW - WT, FA_Y - 0.40), WT, 0.80,
                 fc="#A8D8B0", ec=C_OUT, lw=0.7, zorder=5))
    ax.text(CX + CW - WT / 2, FA_Y, "G", ha="center", va="center",
            fontsize=6.0, color=C_GND, fontweight="bold", zorder=6)

    # Fan body — inside container, left of baffle duct
    FA_X = bd_a_x0 - R_FAN - 0.10
    ax.add_patch(plt.Circle((FA_X, FA_Y), R_FAN, fc=C_ALUM, ec=C_OUT, lw=1.5, zorder=5))
    ax.text(FA_X, FA_Y, "A", ha="center", va="center",
            fontsize=12, fontweight="bold", color=C_OUT, zorder=6)
    for angle in [0, 60, 120, 180, 240, 300]:
        bx = FA_X + 0.30 * math.cos(math.radians(angle))
        by = FA_Y + 0.30 * math.sin(math.radians(angle))
        ax.plot([FA_X, bx], [FA_Y, by], color=C_DIM, lw=1.5, alpha=0.5, zorder=5)

    # Airflow: exterior right → grille → baffle → fan (leftward into container)
    ax.annotate("", xy=(CX + CW, FA_Y),
                xytext=(CX + CW + 1.6, FA_Y),
                arrowprops=dict(arrowstyle="-|>", color=C_CL, lw=2.5), zorder=7)
    ax.text(CX + CW + 1.8, FA_Y, "OUTSIDE\nAIR IN",
            ha="left", va="center", fontsize=8.0, color=C_CL, fontweight="bold")
    # Short interior distribution arrow from fan into container
    ax.annotate("", xy=(FA_X - R_FAN - 0.7, FA_Y),
                xytext=(FA_X - R_FAN - 0.1, FA_Y),
                arrowprops=dict(arrowstyle="-|>", color=C_CL, lw=1.2, alpha=0.6), zorder=6)

    ann(ax, "Cct A  |  6\" (150mm) inline fan\n5A / 16AWG / 60W / 200 CFM\n(interior-mounted)",
        (FA_X, FA_Y + R_FAN), (FA_X - 1.8, FA_Y + 2.2), size=7.5)
    ann(ax, "LOW POSITION\n~600mm AFF",
        (FA_X, FA_Y - R_FAN), (FA_X - 1.2, FA_Y - 1.5), size=7.5)

    # ── EXHAUST FAN B (left end wall — interior-mounted, high position) ──────
    FB_Y  = CY + CH - WT - CH * 0.18   # high position (unchanged)

    # Baffle duct box — between interior face of left wall and fan body
    bd_b_x0 = CX + WT                 # right edge of left wall = duct left face
    ax.add_patch(mpatches.Rectangle((bd_b_x0, FB_Y - 0.40), BD_W, 0.80,
                 fc="#D8E8D8", ec=C_OUT, lw=0.9, zorder=5))
    ax.text(bd_b_x0 + BD_W / 2, FB_Y, "BAFFLE\nDUCT",
            ha="center", va="center", fontsize=5.5, color=C_DIM, zorder=6)

    # Grille indicator — tinted strip in left wall exterior face
    ax.add_patch(mpatches.Rectangle((CX, FB_Y - 0.40), WT, 0.80,
                 fc="#A8D8B0", ec=C_OUT, lw=0.7, zorder=5))
    ax.text(CX + WT / 2, FB_Y, "G", ha="center", va="center",
            fontsize=6.0, color=C_GND, fontweight="bold", zorder=6)

    # Fan body — inside container, right of baffle duct
    FB_X = bd_b_x0 + BD_W + R_FAN + 0.10
    ax.add_patch(plt.Circle((FB_X, FB_Y), R_FAN, fc=C_ALUM, ec=C_OUT, lw=1.5, zorder=5))
    ax.text(FB_X, FB_Y, "B", ha="center", va="center",
            fontsize=12, fontweight="bold", color=C_OUT, zorder=6)
    for angle in [0, 60, 120, 180, 240, 300]:
        bx = FB_X + 0.30 * math.cos(math.radians(angle))
        by = FB_Y + 0.30 * math.sin(math.radians(angle))
        ax.plot([FB_X, bx], [FB_Y, by], color=C_DIM, lw=1.5, alpha=0.5, zorder=5)

    # Airflow: container → fan → baffle → grille → outside (leftward)
    ax.annotate("", xy=(CX - 1.6, FB_Y),
                xytext=(CX, FB_Y),
                arrowprops=dict(arrowstyle="-|>", color="#D32F2F", lw=2.5), zorder=7)
    ax.text(CX - 1.8, FB_Y, "HOT AIR\nOUT",
            ha="right", va="center", fontsize=8.0, color="#D32F2F", fontweight="bold")
    # Short interior collection arrow into fan
    ax.annotate("", xy=(FB_X + R_FAN + 0.1, FB_Y),
                xytext=(FB_X + R_FAN + 0.7, FB_Y),
                arrowprops=dict(arrowstyle="-|>", color="#D32F2F", lw=1.2, alpha=0.6), zorder=6)

    ann(ax, "Cct B  |  6\" (150mm) inline fan\n5A / 16AWG / 60W / 200 CFM\n(interior-mounted)",
        (FB_X, FB_Y + R_FAN), (FB_X + 1.8, FB_Y + 2.2), size=7.5)
    ann(ax, "HIGH POSITION\n~1,800mm AFF",
        (FB_X, FB_Y - R_FAN), (FB_X + 1.2, FB_Y - 1.5), size=7.5)

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
    # Curved arrow from intake (low right) diagonally to exhaust (high left)
    flow_pts_x = [FA_X - R_FAN - 0.5, CX + CW * 0.7, CX + CW * 0.3, FB_X + R_FAN + 0.5]
    flow_pts_y = [FA_Y, FA_Y + 1.5, FB_Y - 1.5, FB_Y]
    ax.annotate("", xy=(FB_X + R_FAN + 0.3, FB_Y),
                xytext=(FA_X - R_FAN - 0.3, FA_Y),
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
    for dx, dy in [(FA_X, FA_Y + R_FAN), (FB_X, FB_Y + R_FAN),
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
    ax.add_patch(mpatches.FancyBboxPatch((MX - 0.1, MY - 1.05), CW + 0.2, 1.15,
                 boxstyle="round,pad=0.04", fc="#F8F9FA", ec=C_DIM, lw=0.8, zorder=2))
    ax.text(MX + CW/2, MY - 0.05, "FAN OPERATING MODES",
            ha="center", va="top", fontsize=9.0, fontweight="bold", color=C_OUT)
    modes = [
        ("EXPOSURE",               "OFF",        "OFF",        "OFF"),
        ("LOADING / DEVELOPMENT",  "Low speed",  "Low speed",  "ON"),
        ("POST-SESSION PURGE",     "Full speed", "Full speed", "OFF"),
        ("PRE-COOL (before entry)", "Full speed", "Full speed", "ON"),
    ]
    hdrs = ["MODE", "FAN A (intake)", "FAN B (exhaust)", "EVAP COOLER"]
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

    # ── RIGHT HALF: Fan baffle — ELEVATION SECTION (EXTERIOR left → INTERIOR right)
    # Air flows left-to-right through two vertical baffles creating an S-path.
    DX, DY = 14.0, 4.0   # detail origin
    DW, DH = 11.5, 9.0   # detail drawing area
    DS = 1 / 30.0         # 1 unit = 30 mm

    # Duct dimensions: 200mm height (vertical) × 300mm depth (horizontal, through wall)
    D_OW = 300 * DS         # 10.0 units — depth shown HORIZONTALLY
    D_OH = 200 * DS         # 6.67 units — height shown VERTICALLY
    D_WT = 10  * DS         # 0.33 units — wall thickness
    D_BT = max(5 * DS, 0.30)  # baffle plate — min 0.30 units for visibility

    B_OX = DX + (DW - D_OW) / 2
    B_OY = DY + (DH - D_OH) / 2

    # Section header
    ax.text(DX + DW/2, DY + DH + 0.50,
            "FAN LIGHT-SAFE BAFFLE — ELEVATION SECTION",
            ha="center", va="center", fontsize=10.5,
            fontweight="bold", color=C_OUT)
    ax.text(DX + DW/2, DY + DH + 0.15,
            "Longitudinal section through duct  ·  Scale 1:30  ·  "
            "EXTERIOR left → INTERIOR right",
            ha="center", va="center", fontsize=7.5, color=C_DIM)

    # Duct outer box
    ax.add_patch(mpatches.Rectangle((B_OX, B_OY), D_OW, D_OH,
                 fc="#F5F5F5", ec=C_OUT, lw=2.0, zorder=3))

    # Duct walls (steel)
    for rx, ry, rw, rh in [
        (B_OX,            B_OY,            D_OW, D_WT),          # bottom wall
        (B_OX,            B_OY+D_OH-D_WT,  D_OW, D_WT),          # top wall
        (B_OX,            B_OY+D_WT,       D_WT, D_OH-2*D_WT),   # left wall (exterior)
        (B_OX+D_OW-D_WT,  B_OY+D_WT,      D_WT, D_OH-2*D_WT),   # right wall (interior)
    ]:
        ax.add_patch(mpatches.Rectangle((rx, ry), rw, rh,
                     fc=C_STEEL, ec=C_OUT, lw=0.5, zorder=4))

    int_h = D_OH - 2 * D_WT    # clear height ≈ 6.0 units
    int_w = D_OW - 2 * D_WT    # clear depth  ≈ 9.33 units

    # BAFFLE 1: vertical fin from TOP, at 30% of depth from exterior
    # Leaves gap at BOTTOM — air passes under it
    B1_X  = B_OX + D_WT + int_w * 0.30
    B1_H  = int_h * 0.65
    B1_Y  = B_OY + D_WT + int_h - B1_H          # top-anchored
    ax.add_patch(mpatches.Rectangle((B1_X, B1_Y), D_BT, B1_H,
                 fc=C_OUT, ec=C_OUT, lw=0.5, zorder=5))
    # Gap 1 (bottom)
    gap1_y = B_OY + D_WT
    gap1_h = int_h - B1_H
    ax.add_patch(mpatches.Rectangle((B1_X - 0.1, gap1_y), D_BT + 0.2, gap1_h,
                 fc="#FFFDE7", ec=C_CL, lw=0.8, ls="--", zorder=4))
    ann(ax, "BAFFLE 1\n(from top)\ngap at bottom",
        (B1_X + D_BT / 2, B1_Y + B1_H * 0.5),
        (B1_X - 2.0, B1_Y + B1_H * 0.5 + 0.8), size=7.5)

    # BAFFLE 2: vertical fin from BOTTOM, at 70% of depth from exterior
    # Leaves gap at TOP — air passes over it
    B2_X  = B_OX + D_WT + int_w * 0.70
    B2_H  = int_h * 0.65
    B2_Y  = B_OY + D_WT                          # bottom-anchored
    ax.add_patch(mpatches.Rectangle((B2_X, B2_Y), D_BT, B2_H,
                 fc=C_OUT, ec=C_OUT, lw=0.5, zorder=5))
    # Gap 2 (top)
    gap2_y = B2_Y + B2_H
    gap2_h = int_h - B2_H
    ax.add_patch(mpatches.Rectangle((B2_X - 0.1, gap2_y), D_BT + 0.2, gap2_h,
                 fc="#FFFDE7", ec=C_CL, lw=0.8, ls="--", zorder=4))
    ann(ax, "BAFFLE 2\n(from bottom)\ngap at top",
        (B2_X + D_BT / 2, B2_Y + B2_H * 0.5),
        (B2_X + 1.8, B2_Y + B2_H * 0.5 - 0.8), size=7.5)

    # Airflow S-path: enter left at mid height → drop to gap 1 → cross → rise to gap 2 → exit right
    mid_y  = B_OY + D_OH / 2
    y_gap1 = gap1_y + gap1_h / 2
    y_gap2 = gap2_y + gap2_h / 2
    pc, plw = C_CL, 1.5
    # Enter left
    ax.annotate("", xy=(B_OX + D_WT + 0.2, mid_y), xytext=(B_OX - 0.8, mid_y),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    # Drop to gap 1
    ax.annotate("", xy=(B1_X - 0.4, y_gap1), xytext=(B1_X - 0.4, mid_y),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    # Pass through gap 1
    ax.annotate("", xy=(B1_X + D_BT + 0.4, y_gap1), xytext=(B1_X - 0.2, y_gap1),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    # Rise to gap 2
    ax.annotate("", xy=(B2_X - 0.4, y_gap2), xytext=(B2_X - 0.4, y_gap1),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    # Pass through gap 2
    ax.annotate("", xy=(B2_X + D_BT + 0.4, y_gap2), xytext=(B2_X - 0.2, y_gap2),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    # Exit right
    ax.annotate("", xy=(B_OX + D_OW + 0.8, mid_y),
                xytext=(B_OX + D_OW - D_WT - 0.3, mid_y),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)

    # EXTERIOR / INTERIOR labels
    ax.text(B_OX - 0.3, B_OY + D_OH / 2, "EXTERIOR",
            ha="right", va="center", fontsize=8.5, color=C_DIM, fontweight="bold")
    ax.text(B_OX + D_OW + 0.3, B_OY + D_OH / 2, "INTERIOR",
            ha="left", va="center", fontsize=8.5, color=C_DIM, fontweight="bold")

    # Dimension lines
    dim_h(ax, B_OX, B_OX + D_OW, B_OY - 0.7, "300 mm  (depth through wall)")
    dim_v(ax, B_OX - 1.1, B_OY, B_OY + D_OH, "200 mm")

    # No-LOS callout
    ax.text(B_OX + D_OW + 0.3, B_OY + D_OH * 0.82,
            "✓ No direct line\n   of sight at\n   any angle",
            ha="left", va="center", fontsize=8.0,
            color="#2E7D32", fontweight="bold")

    # Spec note + sheet 3 reference
    ax.text(DX + DW / 2, B_OY - 1.05,
            "3mm mild steel  ·  flat black all faces  ·  "
            "baffles alternate top/bottom  ·  gap = 35% of clear height",
            ha="center", va="center", fontsize=7.5, color=C_DIM)
    ax.text(DX + DW / 2, B_OY - 1.55,
            "Fan mounting, wall penetration & duct assembly — see Sheet 3",
            ha="center", va="center", fontsize=8.0, color=C_CL,
            style="italic",
            bbox=dict(fc="#F0F8FF", ec=C_CL, pad=3, lw=0.8))

    title_block(ax, FW, 2, 3,
                "VENTILATION SYSTEM — SECTION & BAFFLE DETAIL",
                "Cross-ventilation layout  ·  Fan positions  ·  Light-safe baffle (elevation section)",
                "Section: not to scale  ·  Baffle detail: 1:30")

    plt.savefig("diagrams/lighttrap-sheet2.png", dpi=150, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet2.png  Done.")


# ─────────────────────────────────────────────────────────────────────────────
# SHEET 3 — Fan + Baffle Duct + Wall Assembly
# Longitudinal cross-section through the fan axis showing how the fan,
# baffle duct housing, and container wall connect.
# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet3():
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
            style="italic", alpha=0.85, zorder=6)

    # ── Fan body (interior-mounted — on right face of duct housing) ───────────
    # Fan mounting flange at right face of duct
    FM_T = 0.22
    ax.add_patch(mpatches.Rectangle((FAN_X - FM_T, DUCT_Y - FL_W), FM_T, DH + 2 * FL_W,
                 fc=C_ALUM, ec=C_OUT, lw=1.2, zorder=6))
    for by in [DUCT_Y - FL_W * 0.55, DUCT_Y + DH + FL_W * 0.55]:
        ax.plot(FAN_X - FM_T / 2, by, "o", color=C_OUT, ms=4, zorder=7)
    ann(ax, "Fan mounting flange\n5mm plate · 4×M10 bolts",
        (FAN_X - FM_T / 2, DUCT_Y + DH + FL_W + 0.15),
        (FAN_X - FM_T / 2, DUCT_Y + DH + FL_W + 1.2))

    # Fan body (rectangular elevation view)
    ax.add_patch(mpatches.FancyBboxPatch(
        (FAN_X, FAN_CY - FAN_R), FAN_LEN, FAN_D,
        boxstyle="round,pad=0.08",
        fc=C_ALUM, ec=C_OUT, lw=1.8, zorder=5))
    # Impeller disc
    ax.add_patch(plt.Circle((FAN_CX, FAN_CY), FAN_R * 0.70,
                 fc="none", ec=C_DIM, lw=1.2, ls="--", zorder=6))
    # Blade lines
    for angle in range(0, 360, 45):
        bx = FAN_CX + FAN_R * 0.70 * math.cos(math.radians(angle))
        by = FAN_CY + FAN_R * 0.70 * math.sin(math.radians(angle))
        ax.plot([FAN_CX, bx], [FAN_CY, by],
                color=C_DIM, lw=1.4, alpha=0.55, zorder=7)
    # Motor casing (right end of fan body)
    ax.add_patch(mpatches.Rectangle(
        (FAN_X + FAN_LEN - 0.9, FAN_CY - FAN_R * 0.5),
        0.9, FAN_D * 0.5,
        fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=6))

    # Wiring run from motor into container interior (right of fan)
    WR_X = FAN_X + FAN_LEN + 0.15
    ax.plot([WR_X, WR_X + 2.0], [FAN_CY - FAN_R * 0.35, FAN_CY - FAN_R * 0.35],
            color=C_PIPE, lw=2.5, solid_capstyle="round", zorder=5)
    ax.text(WR_X + 2.15, FAN_CY - FAN_R * 0.35,
            "16 AWG wiring → Cct A/B\n→ electrical panel\n(all inside container)",
            ha="left", va="center", fontsize=7.5, color=C_PIPE)

    ax.text(FAN_CX, FAN_CY - FAN_R - 0.55,
            "6\" (150mm) INLINE FAN  ·  Fan A (intake) or Fan B (exhaust)\n"
            "Cct A/B  ·  60W  ·  200 CFM  ·  Interior-mounted",
            ha="center", va="top", fontsize=8.0, fontweight="bold", color=C_OUT)

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
            ha="right", va="center", fontsize=9.0, color=pc, fontweight="bold")
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
    ax.annotate("", xy=(FAN_X + FAN_LEN + 1.8, mid_y),
                xytext=(FAN_X + FAN_LEN + 0.2, mid_y),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=2.5), zorder=8)
    ax.text(FAN_X + FAN_LEN + 2.0, mid_y, "INTO\nCONTAINER",
            ha="left", va="center", fontsize=9.0, color=pc, fontweight="bold")
    ax.text(FAN_X + FAN_LEN + 2.0, mid_y - FAN_R - 0.3,
            "(exhaust Fan B: flow reversed)",
            ha="left", va="top", fontsize=7.0, color=C_DIM, style="italic")

    # ── Zone labels ───────────────────────────────────────────────────────────
    ax.text(WX / 2, wall_y0 - 0.3, "EXTERIOR",
            ha="center", va="top", fontsize=9.0, color=C_DIM, fontweight="bold")
    ax.text(DUCT_X + (FAN_X + FAN_LEN - DUCT_X) / 2, wall_y0 - 0.3,
            "INTERIOR (container)",
            ha="center", va="top", fontsize=9.0, color=C_DIM, fontweight="bold")
    ax.plot([WX + WT / 2, WX + WT / 2], [wall_y0 - 0.6, wall_y0 - 0.15],
            color=C_DIM, lw=1.0, ls=":")

    # ── Dimension lines ───────────────────────────────────────────────────────
    dim_h(ax, DUCT_X, DUCT_X + DD, DUCT_Y - 1.0, "300 mm  (duct depth)")
    dim_v(ax, DUCT_X - 1.5, DUCT_Y, DUCT_Y + DH, "200 mm")
    dim_h(ax, WX, WX + WT, DUCT_Y + DH + 0.7, "wall")
    ax.plot([WX, WX], [DUCT_Y + DH, DUCT_Y + DH + 0.85], color=C_DIM, lw=0.5, ls=":")
    ax.plot([WX + WT, WX + WT], [DUCT_Y + DH, DUCT_Y + DH + 0.85], color=C_DIM, lw=0.5, ls=":")
    dim_h(ax, FAN_X, FAN_X + FAN_LEN, DUCT_Y - 1.0, "~150 mm  (fan body)")

    title_block(ax, FW, 3, 3,
                "FAN & BAFFLE DUCT — ASSEMBLY SECTION",
                "Interior-mounted fan  ·  Passive louvre grille (exterior only)  ·  "
                "Baffle duct interior-mounted  ·  All wiring inside container",
                "Schematic NTS  ·  Refer to Sheet 2 for baffle detail geometry")

    plt.savefig("diagrams/lighttrap-sheet3.png", dpi=150, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet3.png  Done.")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating TBS-001 Light Trap & Ventilation diagrams...")
    draw_sheet1()
    draw_sheet2()
    draw_sheet3()
    print("Done.")
