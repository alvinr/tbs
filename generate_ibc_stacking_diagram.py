#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_ibc_stacking_diagram.py  —  TBS-001 IBC Stacking & Securing

Sheet 1 — Cross-section elevation (looking along X toward sealed end):
  Side view showing the 2-tier stack in the right end zone.  Bottom tier
  IBCs sit on the container floor; the stacking frame platform supports
  the top tier.  D-ring lashing points at frame corners.  Container
  ceiling, floor, and right walkway shown for context.

Sheet 2 — Plan view (looking down):
  Top-down view of the 4 IBCs in 2×2 arrangement within the right end
  zone.  Frame perimeter, 25mm gap between columns, fill/drain port
  positions through the end wall, and walkway edges shown.

Sheet 3 — Fastening details:
  Detail A: D-ring lashing point (cross-section, welded to frame).
  Detail B: Anti-rotation lip on platform perimeter (cross-section).
  Detail C: Access gate for lower IBC drain valve (front elevation).
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch, Circle
import matplotlib.patches as mpatches

from tbs_constants import (
    svg_path, SVG_DIR,
    C_LEN, C_WID, C_HGT,
    IBC_COL_X, IBC_W, IBC_D, IBC_H_600, IBC_H_STK,
    BLUE_IBC_Y, BROWN_IBC_Y, IBC_FAR_Y, WASTE_IBC_Y,
    WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T,
    WALKWAY_RIGHT_X,
    C_BLUE_IBC, C_BROWN_IBC, C_WASTE_IBC,
    PROC_TRAY_RIM,
)
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader

# ── Palette ───────────────────────────────────────────────────────────────────
BG      = "#FFFFFF"
C_OUT   = "#1A1A1A"
C_CL    = "#2060A0"
C_DIM   = "#404040"
C_STEEL = "#B0B0B8"
C_FRAME = "#606068"
C_FLOOR = "#E0DDD8"
C_WALL  = "#C0C0C8"
C_GRATE = "#A0A0A8"
C_RUBBER = "#404040"
C_PORT  = "#708090"
FONT    = {"fontfamily": "monospace"}

# ── Frame constants (from equipment-layout-report.md §5) ──────────────────────
FRAME_RHS      = 50     # 50×50×3mm RHS
FRAME_T        = 3      # wall thickness
FRAME_FOOTPRINT_W = 2187  # frame footprint width (across Yd, spans both columns + 65mm overhang/side)
FRAME_FOOTPRINT_D = 1284  # frame footprint depth (along X, 65mm overhang cargo-door side, flush to end wall)
FRAME_PLATFORM_H  = 1060  # platform height (1,010 + 50mm clearance plate)
FRAME_PLATFORM_T  = FRAME_RHS  # platform beam depth = RHS size
FRAME_LIP_H    = 40     # anti-rotation lip height above platform
FRAME_LIP_T    = 5      # lip thickness (steel plate)
FRAME_WEIGHT   = 75     # kg (midpoint of 65–85 range, unified frame)

# D-ring lashing
DRING_SIZE     = 25     # D-ring strap width (mm)
DRING_STANDOFF = 30     # standoff from frame corner
DRING_WLL      = 1100   # working load limit per ring (kg)

# Access gate
GATE_H         = 300    # gate panel height (mm)
GATE_BOLT_D    = 12     # M12 bolts
GATE_BOLT_N    = 4      # bolts per gate

# Rubber mat
MAT_T          = 12     # anti-slip rubber mat thickness (mm)

# IBC cage post visual width
CAGE_POST_W    = 40     # visual representation of cage uprights

# Gap between near and far columns
IBC_GAP        = IBC_FAR_Y - (BLUE_IBC_Y + IBC_D)  # = 25mm

# Ceiling clearance
CEIL_CLEAR     = C_HGT - IBC_H_STK  # = 368mm

# Fill/drain port
PORT_DIA       = 50     # 2" NPT visual diameter (mm)
FILL_PORT_Z    = 1800   # fill port center height
DRAIN_PORT_Z   = 200    # drain port center height


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — Cross-Section Elevation (looking along X toward sealed end)
#
# Horizontal = Yd (0=near/pinhole wall, positive toward far wall)
# Vertical   = Z  (0=floor, positive up)
# Shows both near and far IBC columns with stacking frame between.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():
    S = 2.5   # scale factor (mm → drawing units)

    def sx(mm): return mm * S
    def sy(mm): return mm * S

    # ── Layout bounds ─────────────────────────────────────────────────────────
    YD_LO = -120
    YD_HI = C_WID + 120
    Z_LO  = -580
    Z_HI  = C_HGT + 100

    fig, ax = plt.subplots(figsize=(18, 22))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(sx(YD_LO), sx(YD_HI))
    ax.set_ylim(sy(Z_LO), sy(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container shell ───────────────────────────────────────────────────────
    WALL_T = 2.0   # visual wall thickness (mm at this scale)

    # Floor
    ax.add_patch(Rectangle((sx(YD_LO), sy(-30)),
                            sx(YD_HI - YD_LO), sy(30),
                            fc=C_FLOOR, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Ceiling
    ax.add_patch(Rectangle((sx(YD_LO), sy(C_HGT)),
                            sx(YD_HI - YD_LO), sy(30),
                            fc=C_FLOOR, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Near wall (left)
    ax.add_patch(Rectangle((sx(-30), sy(0)),
                            sx(30), sy(C_HGT),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Far wall (right)
    ax.add_patch(Rectangle((sx(C_WID), sy(0)),
                            sx(30), sy(C_HGT),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))

    # Floor/ceiling/wall labels
    ax.text(sx(C_WID / 2), sy(-45), "CONTAINER FLOOR",
            ha="center", va="top", fontsize=6, color=C_DIM, **FONT)
    ax.text(sx(C_WID / 2), sy(C_HGT + 45), "CONTAINER CEILING (Z=2,388mm)",
            ha="center", va="bottom", fontsize=6, color=C_DIM, **FONT)
    ax.text(sx(-45), sy(C_HGT / 2), "NEAR\nWALL\n(Yd=0)",
            ha="center", va="center", fontsize=5.5, color=C_DIM, **FONT,
            rotation=90)
    ax.text(sx(C_WID + 45), sy(C_HGT / 2), "FAR\nWALL\n(Yd=2,362)",
            ha="center", va="center", fontsize=5.5, color=C_DIM, **FONT,
            rotation=90)

    # Interior face lines
    ax.plot([sx(0), sx(0)], [sy(0), sy(C_HGT)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([sx(C_WID), sx(C_WID)], [sy(0), sy(C_HGT)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([sx(0), sx(C_WID)], [sy(0), sy(0)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([sx(0), sx(C_WID)], [sy(C_HGT), sy(C_HGT)], color=C_OUT, lw=2.0, zorder=3)

    # ── IBCs ──────────────────────────────────────────────────────────────────
    # In this cross-section (looking along X), we see Yd vs Z.
    # Near column: Yd = BLUE_IBC_Y to BLUE_IBC_Y + IBC_D
    # Far column:  Yd = IBC_FAR_Y  to IBC_FAR_Y + IBC_D

    ibc_data = [
        ("IBC-3\nBROWN\n(recycled)", BLUE_IBC_Y, 0, IBC_D, IBC_H_600, C_BROWN_IBC),
        ("IBC-1\nBLUE\n(clean supply)", BLUE_IBC_Y, IBC_H_600 + MAT_T + FRAME_RHS,
         IBC_D, IBC_H_600, C_BLUE_IBC),
        ("IBC-4\nWASTE", IBC_FAR_Y, 0, IBC_D, IBC_H_600, C_WASTE_IBC),
        ("IBC-2\nBLUE\n(clean supply)", IBC_FAR_Y, IBC_H_600 + MAT_T + FRAME_RHS,
         IBC_D, IBC_H_600, C_BLUE_IBC),
    ]

    for label, yd, z, d, h, color in ibc_data:
        # IBC body (translucent tank)
        ax.add_patch(Rectangle((sx(yd), sy(z)),
                                sx(d), sy(h),
                                fc=color, ec=C_OUT, lw=1.5, alpha=0.35, zorder=5))
        # Cage uprights (4 posts at corners)
        for post_yd in [yd + 15, yd + d - 15]:
            ax.add_patch(Rectangle((sx(post_yd - CAGE_POST_W / 2), sy(z)),
                                    sx(CAGE_POST_W), sy(h),
                                    fc="none", ec=C_OUT, lw=0.6, zorder=6))
        # Cage top rail
        ax.plot([sx(yd), sx(yd + d)], [sy(z + h), sy(z + h)],
                color=C_OUT, lw=1.2, zorder=6)
        # Label
        ax.text(sx(yd + d / 2), sy(z + h / 2), label,
                ha="center", va="center", fontsize=7, color=C_OUT,
                fontweight="bold", **FONT, zorder=10)

    # ── Stacking frame ────────────────────────────────────────────────────────
    # Frame spans both columns: from BLUE_IBC_Y - frame_overhang to IBC_FAR_Y + IBC_D + frame_overhang
    frame_overhang = (FRAME_FOOTPRINT_W - (IBC_FAR_Y + IBC_D - BLUE_IBC_Y)) / 2
    frame_yd_l = BLUE_IBC_Y - frame_overhang
    frame_yd_r = IBC_FAR_Y + IBC_D + frame_overhang
    platform_z = IBC_H_600  # platform sits on top of bottom IBCs

    # Vertical uprights at frame corners (4 visible as 2 near + 2 far)
    upright_positions = [frame_yd_l, frame_yd_r - FRAME_RHS]
    for uyd in upright_positions:
        ax.add_patch(Rectangle((sx(uyd), sy(0)),
                                sx(FRAME_RHS), sy(IBC_H_STK + FRAME_RHS),
                                fc=C_FRAME, ec=C_OUT, lw=1.2, zorder=7,
                                alpha=0.8))
        # Cross-hatch for steel
        ax.add_patch(Rectangle((sx(uyd + FRAME_T), sy(FRAME_T)),
                                sx(FRAME_RHS - 2 * FRAME_T),
                                sy(IBC_H_STK + FRAME_RHS - 2 * FRAME_T),
                                fc=C_WALL, ec="none", lw=0, zorder=7,
                                alpha=0.3))

    # Platform beam (horizontal, spans full width)
    ax.add_patch(Rectangle((sx(frame_yd_l), sy(platform_z)),
                            sx(frame_yd_r - frame_yd_l), sy(FRAME_RHS),
                            fc=C_FRAME, ec=C_OUT, lw=1.5, zorder=7, alpha=0.85))
    # Platform hollow
    ax.add_patch(Rectangle((sx(frame_yd_l + FRAME_T), sy(platform_z + FRAME_T)),
                            sx(frame_yd_r - frame_yd_l - 2 * FRAME_T),
                            sy(FRAME_RHS - 2 * FRAME_T),
                            fc="#D0D0D0", ec="none", zorder=7, alpha=0.4))

    # Anti-slip rubber mat on platform
    mat_z = platform_z + FRAME_RHS
    ax.add_patch(Rectangle((sx(frame_yd_l + FRAME_RHS), sy(mat_z)),
                            sx(frame_yd_r - frame_yd_l - 2 * FRAME_RHS), sy(MAT_T),
                            fc=C_RUBBER, ec=C_OUT, lw=0.8, zorder=8, alpha=0.7))

    # Anti-rotation lip (on platform perimeter)
    lip_z = mat_z + MAT_T
    for lip_yd in [frame_yd_l + FRAME_RHS - FRAME_LIP_T,
                   frame_yd_r - FRAME_RHS]:
        ax.add_patch(Rectangle((sx(lip_yd), sy(lip_z - 5)),
                                sx(FRAME_LIP_T), sy(FRAME_LIP_H),
                                fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=9))

    # Top rail
    top_z = IBC_H_STK
    ax.add_patch(Rectangle((sx(frame_yd_l), sy(top_z)),
                            sx(frame_yd_r - frame_yd_l), sy(FRAME_RHS),
                            fc=C_FRAME, ec=C_OUT, lw=1.2, zorder=7, alpha=0.85))

    # ── D-ring lashing points (4 per tier, showing 2 near-side) ───────────────
    dring_color = "#D0A030"
    # Bottom tier D-rings: near corners at Z ≈ FRAME_RHS/2
    # Top tier D-rings: at Z ≈ platform_z + FRAME_RHS + IBC_H_600/2
    dring_positions = [
        (frame_yd_l - 5, FRAME_RHS * 1.5, "BOTTOM"),
        (frame_yd_r + 5, FRAME_RHS * 1.5, "BOTTOM"),
        (frame_yd_l - 5, platform_z + FRAME_RHS * 1.5, "TOP"),
        (frame_yd_r + 5, platform_z + FRAME_RHS * 1.5, "TOP"),
    ]
    for dyd, dz, tier in dring_positions:
        # D-ring as a small D shape
        ring_r = 18
        # Mount plate
        plate_w = 35
        plate_h = 8
        if dyd < C_WID / 2:
            plate_x = dyd + 5
        else:
            plate_x = dyd - plate_w - 5
        ax.add_patch(Rectangle((sx(plate_x), sy(dz - plate_h / 2)),
                                sx(plate_w), sy(plate_h),
                                fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=10))
        # D-ring arc
        ring_x = dyd - 10 if dyd < C_WID / 2 else dyd + 10
        ax.add_patch(Circle((sx(ring_x), sy(dz)),
                             sy(ring_r), fc="none", ec=dring_color,
                             lw=2.5, zorder=11))

    # D-ring label (one leader for all)
    leader(ax, sx(frame_yd_l - 25), sy(FRAME_RHS * 1.5),
           sx(frame_yd_l - 80), sy(FRAME_RHS * 1.5 + 120),
           f"D-RING LASHING POINT\n25mm, {DRING_WLL}kg WLL\n8x TOTAL (4 PER TIER)\nMcMaster #3641T29",
           color=dring_color, fs=6.5,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # ── Access gate (lower tier, shown on near side) ──────────────────────────
    gate_yd = frame_yd_l
    gate_w = FRAME_FOOTPRINT_W / 2 - FRAME_RHS
    ax.add_patch(Rectangle((sx(gate_yd + FRAME_RHS), sy(0)),
                            sx(gate_w), sy(GATE_H),
                            fc="none", ec="#C04040", lw=2.0, ls="--", zorder=8))
    # Bolt symbols at gate corners
    for byd in [gate_yd + FRAME_RHS + 20, gate_yd + FRAME_RHS + gate_w - 20]:
        for bz in [30, GATE_H - 30]:
            ax.add_patch(Circle((sx(byd), sy(bz)), sy(6),
                                 fc="#C04040", ec=C_OUT, lw=0.5, zorder=12))

    leader(ax, sx(gate_yd + FRAME_RHS + gate_w / 2), sy(GATE_H),
           sx(gate_yd + FRAME_RHS + gate_w / 2 - 50), sy(GATE_H + 100),
           f"ACCESS GATE (x2)\nREMOVABLE PANEL\nH=0-{GATE_H}mm\n4x M{GATE_BOLT_D} BOLTS\n(DRAIN VALVE ACCESS)",
           color="#C04040", fs=6,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # ── Labels ────────────────────────────────────────────────────────────────
    # Frame label
    leader(ax, sx(frame_yd_l + FRAME_RHS / 2), sy(IBC_H_600 / 2),
           sx(frame_yd_l - 80), sy(IBC_H_600 / 2 + 50),
           f"STACKING FRAME\n50x50x3mm RHS\nMILD STEEL\n~{FRAME_WEIGHT}kg",
           color=C_FRAME, fs=6.5,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # Platform label
    leader(ax, sx(C_WID / 2), sy(platform_z + FRAME_RHS / 2),
           sx(C_WID / 2 + 200), sy(platform_z + 180),
           f"PLATFORM BEAM\n50x50x3mm RHS\n+ {MAT_T}mm RUBBER MAT\n+ {FRAME_LIP_H}mm ANTI-ROTATION LIP",
           color=C_FRAME, fs=6,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # ── Dimension lines ───────────────────────────────────────────────────────
    # IBC height (bottom tier)
    draw_dim_v(ax, sx(IBC_FAR_Y + IBC_D + 80), sy(0), sy(IBC_H_600),
               f"{IBC_H_600}mm\nIBC HEIGHT", offset=sx(8), fs=6, right=True, font=FONT)

    # Stack total height
    draw_dim_v(ax, sx(IBC_FAR_Y + IBC_D + 160), sy(0), sy(IBC_H_STK + FRAME_RHS),
               f"{IBC_H_STK + FRAME_RHS}mm\nSTACK + FRAME", offset=sx(8), fs=6,
               right=True, font=FONT)

    # Ceiling clearance
    draw_dim_v(ax, sx(IBC_FAR_Y + IBC_D + 160), sy(IBC_H_STK + FRAME_RHS), sy(C_HGT),
               f"{CEIL_CLEAR - FRAME_RHS}mm\nCLEARANCE", offset=sx(8), fs=6,
               right=True, font=FONT)

    # Container interior width
    draw_dim_h(ax, sx(0), sx(C_WID), sy(-60),
               f"{C_WID}mm  INTERIOR WIDTH", offset=sy(5), fs=6.5, font=FONT)

    # Near column Yd position
    draw_dim_h(ax, sx(0), sx(BLUE_IBC_Y), sy(IBC_H_600 + 80),
               f"{BLUE_IBC_Y}mm", offset=sy(5), fs=5.5, font=FONT)

    # IBC depth
    draw_dim_h(ax, sx(BLUE_IBC_Y), sx(BLUE_IBC_Y + IBC_D), sy(IBC_H_600 + 80),
               f"{IBC_D}mm\nIBC DEPTH", offset=sy(5), fs=5.5, font=FONT)

    # Gap between columns
    draw_dim_h(ax, sx(BLUE_IBC_Y + IBC_D), sx(IBC_FAR_Y), sy(IBC_H_600 + 80),
               f"{IBC_GAP}mm\nGAP", offset=sy(5), fs=5.5, font=FONT)

    # ── Right walkway (ghost, for context) ────────────────────────────────────
    # The right walkway is at the IBC end, perpendicular to this view
    # Show as a note/context only
    ax.text(sx(C_WID / 2), sy(C_HGT + 80),
            f"CEILING CLEARANCE: {CEIL_CLEAR}mm (transport safe \u2714)",
            ha="center", va="bottom", fontsize=7, color="#206020",
            fontweight="bold", **FONT, zorder=15)

    # ── Notes ─────────────────────────────────────────────────────────────────
    notes_x = sx(C_WID / 2)
    notes_top = sy(Z_LO + 480)
    notes = [
        "CROSS-SECTION NOTES:",
        "",
        "1. View looking along X toward sealed",
        "   end wall. Section through IBC stack.",
        f"2. 4x 600L IBCs (Schutz Ecobulk MX).",
        f"   Each: 55kg tare, {IBC_W}x{IBC_D}x{IBC_H_600}mm.",
        f"3. Stacking frame: 50x50x3mm RHS mild",
        f"   steel, welded. ~{FRAME_WEIGHT}kg frame alone.",
        f"4. Platform at Z={IBC_H_600}mm + {MAT_T}mm",
        f"   rubber anti-slip mat.",
        f"5. {FRAME_LIP_H}mm steel lip retains upper",
        "   IBC cage against lateral movement.",
        f"6. 8x D-ring lashing points (4 per tier),",
        f"   {DRING_WLL}kg WLL each.",
        f"7. 2x removable access gates (H=0-{GATE_H}mm)",
        "   for lower IBC drain valve access.",
        f"8. Total loaded: 4x655kg = 2,620kg",
        f"   + {FRAME_WEIGHT}kg frame = ~2,672kg.",
    ]
    for i, line in enumerate(notes):
        bold = i == 0
        ax.text(notes_x, notes_top - i * sy(12), line,
                ha="center", va="top", fontsize=6 if bold else 5.5,
                color=C_OUT if bold else C_DIM,
                fontweight="bold" if bold else "normal",
                **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 3",
                drawing_title="IBC STACKING & SECURING",
                subtitle="CROSS-SECTION ELEVATION — 2x2 STACK IN RIGHT END ZONE",
                scale_note=f"SCALE ~ 2.5:1 - ALL DIMS IN mm - SECTION LOOKING ALONG X",
                height=0.06)

    fig.savefig("diagrams/ibc-stacking-sheet1.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/ibc-stacking-sheet1.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-stacking-sheet1.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Plan View (looking down)
#
# Standard TBS plan view convention:
#   Horizontal = X  (0=cargo door at left, sealed end at right)
#   Vertical   = Yd (0=pinhole/near wall at bottom)
# Shows 4 IBCs from above with frame, ports, and walkway context.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():
    S = 2.5

    def px(mm): return mm * S   # X along horizontal
    def py(mm): return mm * S   # Yd along vertical

    # The plan view shows the area around the IBC stack
    X_LO = IBC_COL_X - 600
    X_HI = C_LEN + 350
    YD_LO = -400
    YD_HI = C_WID + 120

    fig, ax = plt.subplots(figsize=(20, 17))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(px(X_LO), px(X_HI))
    ax.set_ylim(py(YD_LO), py(YD_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container walls ───────────────────────────────────────────────────────
    WALL_T = 25  # visual wall thickness (plan view)

    # Near wall (pinhole, bottom of Yd range)
    ax.add_patch(Rectangle((px(X_LO), py(-WALL_T)),
                            px(X_HI - X_LO), py(WALL_T),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Far wall (top of Yd range)
    ax.add_patch(Rectangle((px(X_LO), py(C_WID)),
                            px(X_HI - X_LO), py(WALL_T),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # End wall (sealed end, right side of X range)
    ax.add_patch(Rectangle((px(C_LEN), py(-WALL_T)),
                            px(WALL_T), py(C_WID + 2 * WALL_T),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))

    # Interior face lines
    ax.plot([px(X_LO), px(C_LEN)], [py(0), py(0)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([px(X_LO), px(C_LEN)], [py(C_WID), py(C_WID)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([px(C_LEN), px(C_LEN)], [py(0), py(C_WID)], color=C_OUT, lw=2.0, zorder=3)

    # Wall labels
    ax.text(px((X_LO + C_LEN) / 2), py(-WALL_T - 10),
            "NEAR WALL (PINHOLE, Yd=0)", ha="center", va="top",
            fontsize=6, color=C_DIM, **FONT)
    ax.text(px((X_LO + C_LEN) / 2), py(C_WID + WALL_T + 10),
            "FAR WALL (Yd=2,362)", ha="center", va="bottom",
            fontsize=6, color=C_DIM, **FONT)
    ax.text(px(C_LEN + WALL_T + 10), py(C_WID / 2),
            f"SEALED END WALL\n(X={C_LEN}mm)", ha="left", va="center",
            fontsize=6.5, color=C_DIM, fontweight="bold", **FONT, rotation=90)

    # Arrow showing direction toward cargo door
    ax.annotate("", xy=(px(X_LO + 20), py(C_WID / 2)),
                xytext=(px(X_LO + 150), py(C_WID / 2)),
                arrowprops=dict(arrowstyle="->", color=C_DIM, lw=1.5))
    ax.text(px(X_LO + 10), py(C_WID / 2),
            "CARGO\nDOOR\nEND", ha="right", va="center",
            fontsize=6, color=C_DIM, **FONT)

    # ── Frame perimeter (plan view) ───────────────────────────────────────────
    frame_overhang = (FRAME_FOOTPRINT_W - (IBC_FAR_Y + IBC_D - BLUE_IBC_Y)) / 2
    frame_yd_l = BLUE_IBC_Y - frame_overhang
    frame_yd_r = IBC_FAR_Y + IBC_D + frame_overhang
    frame_x_l = IBC_COL_X - 65  # 65mm overhang on cargo-door side
    frame_x_r = min(IBC_COL_X + IBC_W + 65, C_LEN)  # clamp to end wall

    # Frame outline
    ax.add_patch(Rectangle((px(frame_x_l), py(frame_yd_l)),
                            px(frame_x_r - frame_x_l),
                            py(frame_yd_r - frame_yd_l),
                            fc="none", ec=C_FRAME, lw=2.5, zorder=6))

    # Frame RHS members (plan view — show as rectangles at perimeter)
    for yd in [frame_yd_l, frame_yd_r - FRAME_RHS]:
        ax.add_patch(Rectangle((px(frame_x_l), py(yd)),
                                px(frame_x_r - frame_x_l), py(FRAME_RHS),
                                fc=C_FRAME, ec=C_OUT, lw=0.8, zorder=6, alpha=0.5))
    for xp in [frame_x_l, frame_x_r - FRAME_RHS]:
        ax.add_patch(Rectangle((px(xp), py(frame_yd_l)),
                                px(FRAME_RHS), py(frame_yd_r - frame_yd_l),
                                fc=C_FRAME, ec=C_OUT, lw=0.8, zorder=6, alpha=0.5))

    # ── 4 IBCs (plan view — looking down onto top tier) ───────────────────────
    ibc_plan = [
        ("IBC-1\nBLUE\n(top, near)", BLUE_IBC_Y, IBC_COL_X, C_BLUE_IBC),
        ("IBC-2\nBLUE\n(top, far)", IBC_FAR_Y, IBC_COL_X, C_BLUE_IBC),
        ("IBC-3 BROWN\n(bottom, near)\nBELOW IBC-1", BLUE_IBC_Y, IBC_COL_X, C_BROWN_IBC),
        ("IBC-4 WASTE\n(bottom, far)\nBELOW IBC-2", IBC_FAR_Y, IBC_COL_X, C_WASTE_IBC),
    ]

    # Show top tier IBCs as solid, bottom tier labels only (since they're beneath)
    for i, (label, yd, x, color) in enumerate(ibc_plan):
        if i < 2:  # top tier — visible from above
            ax.add_patch(Rectangle((px(x), py(yd)),
                                    px(IBC_W), py(IBC_D),
                                    fc=color, ec=C_OUT, lw=1.8, alpha=0.4, zorder=7))
            # Cage grid lines (top view shows cage structure)
            for frac in [0.25, 0.5, 0.75]:
                ax.plot([px(x + IBC_W * frac), px(x + IBC_W * frac)],
                        [py(yd), py(yd + IBC_D)],
                        color=C_OUT, lw=0.4, alpha=0.3, zorder=7)
                ax.plot([px(x), px(x + IBC_W)],
                        [py(yd + IBC_D * frac), py(yd + IBC_D * frac)],
                        color=C_OUT, lw=0.4, alpha=0.3, zorder=7)
            ax.text(px(x + IBC_W / 2), py(yd + IBC_D / 2), label,
                    ha="center", va="center", fontsize=7, color=C_OUT,
                    fontweight="bold", **FONT, zorder=10)
        else:  # bottom tier — hidden below, show as dashed outline
            ax.add_patch(Rectangle((px(x), py(yd)),
                                    px(IBC_W), py(IBC_D),
                                    fc="none", ec=color, lw=1.0, ls="--",
                                    alpha=0.5, zorder=4))
            # Bottom tier label below the IBC footprint
            ax.text(px(x + IBC_W / 2), py(yd - 30), label.split("\n")[0],
                    ha="center", va="top", fontsize=5.5, color=color,
                    style="italic", **FONT, zorder=10)

    # ── Fill/drain ports through end wall ─────────────────────────────────────
    # 4x 2" NPT bulkhead fittings through the sealed end wall
    near_col_center = BLUE_IBC_Y + IBC_D / 2
    far_col_center = IBC_FAR_Y + IBC_D / 2

    port_data = [
        ("FILL\nIBC-1", near_col_center - 120, C_LEN),
        ("FILL\nIBC-2", far_col_center - 120, C_LEN),
        ("DRAIN\nIBC-3", near_col_center + 120, C_LEN),
        ("DRAIN\nIBC-4", far_col_center + 120, C_LEN),
    ]
    for plabel, pyd, pxv in port_data:
        ax.add_patch(Circle((px(pxv), py(pyd)),
                             px(PORT_DIA / 2), fc=C_PORT, ec=C_OUT,
                             lw=1.5, zorder=12))
        ax.text(px(pxv + 50), py(pyd), plabel,
                ha="left", va="center", fontsize=5, color=C_PORT,
                fontweight="bold", **FONT, zorder=15)

    ax.text(px(C_LEN + WALL_T + 60), py(C_WID / 2),
            "4x 2\" NPT BULKHEAD\nFITTINGS (EXTERNAL\nFILL/DRAIN — NO DOOR\nACCESS REQUIRED)",
            ha="left", va="center", fontsize=6, color=C_PORT,
            **FONT, zorder=15)

    # ── D-ring positions (plan view — at frame corners) ───────────────────────
    dring_color = "#D0A030"
    for dyd in [frame_yd_l, frame_yd_r]:
        for dx in [frame_x_l, frame_x_r]:
            ax.add_patch(Circle((px(dx), py(dyd)),
                                 px(12), fc=dring_color, ec=C_OUT,
                                 lw=1.0, zorder=11))
    ax.text(px(frame_x_l - 10), py(frame_yd_l - 30),
            "D-RING (TYP. 8x)", ha="right", va="top",
            fontsize=5.5, color=dring_color, fontweight="bold", **FONT, zorder=15)

    # ── Dimensions ────────────────────────────────────────────────────────────
    # IBC footprint depth (along Yd) — vertical dimension
    draw_dim_v(ax, px(IBC_COL_X - 60), py(BLUE_IBC_Y), py(BLUE_IBC_Y + IBC_D),
               f"{IBC_D}mm", offset=px(5), fs=6, font=FONT)

    # Gap between columns
    draw_dim_v(ax, px(IBC_COL_X - 60), py(BLUE_IBC_Y + IBC_D), py(IBC_FAR_Y),
               f"{IBC_GAP}mm\nGAP", offset=px(5), fs=5.5, font=FONT)

    # Far column depth
    draw_dim_v(ax, px(IBC_COL_X - 60), py(IBC_FAR_Y), py(IBC_FAR_Y + IBC_D),
               f"{IBC_D}mm", offset=px(5), fs=6, font=FONT)

    # IBC width (along X) — horizontal dimension
    draw_dim_h(ax, px(IBC_COL_X), px(IBC_COL_X + IBC_W),
               py(IBC_FAR_Y + IBC_D + 80),
               f"{IBC_W}mm IBC WIDTH", offset=py(5), fs=6, font=FONT)

    # Frame footprint width (along Yd) — vertical dimension
    draw_dim_v(ax, px(frame_x_r + 60), py(frame_yd_l), py(frame_yd_r),
               f"{FRAME_FOOTPRINT_W}mm FRAME", offset=px(5), fs=6, right=True, font=FONT)

    # Distance from near wall to IBC
    draw_dim_v(ax, px(IBC_COL_X - 120), py(0), py(BLUE_IBC_Y),
               f"{BLUE_IBC_Y}mm", offset=px(5), fs=5.5, font=FONT)

    # ── Walkway context (ghost) ───────────────────────────────────────────────
    # Right walkway runs along the left edge of the IBC zone
    wk_x_l = WALKWAY_RIGHT_X
    wk_x_r = WALKWAY_RIGHT_X + WALKWAY_W
    ax.add_patch(Rectangle((px(wk_x_l), py(0)),
                            px(WALKWAY_W), py(C_WID),
                            fc="#E8F0E8", ec=C_GRATE, lw=1.0, ls="--",
                            alpha=0.3, zorder=3))
    ax.text(px(wk_x_l + WALKWAY_W / 2), py(C_WID / 2),
            f"RIGHT WALKWAY\n(X={wk_x_l}-{wk_x_r}mm)\nCEILING HUNG",
            ha="center", va="center", fontsize=5.5, color=C_GRATE,
            style="italic", **FONT, zorder=5, rotation=90)

    # ── Notes ─────────────────────────────────────────────────────────────────
    notes_x = px(X_LO + 20)
    notes_top = py(YD_HI - 10 - (YD_HI - YD_LO) * 0.20)
    notes = [
        "PLAN VIEW NOTES:",
        "",
        f"1. 4x Schutz Ecobulk MX 600L IBCs",
        f"   in 2x2 stack. Top tier visible;",
        "   bottom tier shown dashed (below).",
        f"2. Frame footprint: {FRAME_FOOTPRINT_W}x{FRAME_FOOTPRINT_D}mm",
        f"   (65mm overhang per side).",
        f"3. {IBC_GAP}mm gap between near/far columns",
        "   allows frame uprights and air flow.",
        f"4. IBC right edge aligns with container",
        f"   end wall (X={C_LEN}mm). No wasted space.",
        f"5. 4x 2\" NPT bulkhead fittings through",
        "   end wall for external fill/drain.",
        "6. Right walkway (ceiling-hung) provides",
        "   access without floor contact.",
    ]
    for i, line in enumerate(notes):
        bold = i == 0
        ax.text(notes_x, notes_top - i * py(12), line,
                ha="left", va="top", fontsize=6 if bold else 5.5,
                color=C_OUT if bold else C_DIM,
                fontweight="bold" if bold else "normal",
                **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 3",
                drawing_title="IBC STACKING & SECURING",
                subtitle="PLAN VIEW — 2x2 IBC LAYOUT IN RIGHT END ZONE",
                scale_note=f"SCALE ~ 2.5:1 - ALL DIMS IN mm - VIEW LOOKING DOWN",
                height=0.06)

    fig.savefig("diagrams/ibc-stacking-sheet2.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/ibc-stacking-sheet2.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-stacking-sheet2.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — Fastening Details
#
# Three detail views:
#   A — D-ring lashing point cross-section
#   B — Anti-rotation lip on platform perimeter
#   C — Access gate front elevation
# ═══════════════════════════════════════════════════════════════════════════════
def sheet3():
    S = 5.0   # scale factor for detail views

    def sx(mm): return mm * S
    def sy(mm): return mm * S

    fig, ax = plt.subplots(figsize=(20, 22))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, sx(600))
    ax.set_ylim(sy(-100), sy(500))
    ax.set_aspect("equal")
    ax.axis("off")

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL A — D-Ring Lashing Point (cross-section)
    # Shows frame RHS member with welded D-ring plate and ring
    # ══════════════════════════════════════════════════════════════════════════
    DA_OX = 30
    DA_OY = 280

    ax.text(sx(DA_OX + 80), sy(DA_OY + 190),
            "DETAIL A — D-RING LASHING POINT\n(CROSS-SECTION, WELDED TO FRAME)",
            ha="center", va="bottom", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # Frame RHS member (cross-section)
    rhs_x = DA_OX + 40
    rhs_y = DA_OY + 50
    ax.add_patch(Rectangle((sx(rhs_x), sy(rhs_y)),
                            sx(FRAME_RHS), sy(FRAME_RHS),
                            fc=C_FRAME, ec=C_OUT, lw=2.0, zorder=5))
    # Hollow
    ax.add_patch(Rectangle((sx(rhs_x + FRAME_T), sy(rhs_y + FRAME_T)),
                            sx(FRAME_RHS - 2 * FRAME_T), sy(FRAME_RHS - 2 * FRAME_T),
                            fc="#D8D8D8", ec=C_OUT, lw=0.8, zorder=6))
    ax.text(sx(rhs_x + FRAME_RHS / 2), sy(rhs_y + FRAME_RHS / 2),
            f"{FRAME_RHS}x{FRAME_RHS}\nx{FRAME_T} RHS",
            ha="center", va="center", fontsize=6, color=C_OUT, **FONT, zorder=10)

    # Mounting plate (welded to frame face)
    plate_t = 6
    plate_h = 80
    plate_x = rhs_x - plate_t
    plate_y = rhs_y + (FRAME_RHS - plate_h) / 2
    ax.add_patch(Rectangle((sx(plate_x), sy(plate_y)),
                            sx(plate_t), sy(plate_h),
                            fc=C_STEEL, ec=C_OUT, lw=1.5, hatch="///", zorder=7))

    # Weld symbols (triangles at plate-frame junction)
    for wy in [plate_y + 5, plate_y + plate_h - 5]:
        weld_verts = [
            (sx(rhs_x), sy(wy)),
            (sx(rhs_x - 2), sy(wy + 5)),
            (sx(rhs_x - 2), sy(wy - 5)),
        ]
        ax.add_patch(Polygon(weld_verts, closed=True,
                             fc="#404040", ec=C_OUT, lw=0.5, zorder=8))

    # D-ring (side view — D shape)
    ring_cx = plate_x - 25
    ring_cy = rhs_y + FRAME_RHS / 2
    ring_r = 20
    # Draw as a D: flat side against plate, curved side outward
    theta = np.linspace(-np.pi / 2, np.pi / 2, 50)
    ring_xs = [sx(ring_cx + ring_r * np.cos(t)) for t in theta]
    ring_ys = [sy(ring_cy + ring_r * np.sin(t)) for t in theta]
    # Close the D with straight side
    ring_xs = [sx(plate_x - 2)] + ring_xs + [sx(plate_x - 2)]
    ring_ys = [sy(ring_cy - ring_r)] + ring_ys + [sy(ring_cy + ring_r)]
    ax.plot(ring_xs, ring_ys, color="#D0A030", lw=3.5, zorder=9,
            solid_capstyle="round")

    # D-ring pin through plate
    pin_r = 4
    ax.add_patch(Circle((sx(plate_x - 1), sy(ring_cy - ring_r + 3)),
                         sx(pin_r), fc="#808080", ec=C_OUT, lw=1.0, zorder=10))
    ax.add_patch(Circle((sx(plate_x - 1), sy(ring_cy + ring_r - 3)),
                         sx(pin_r), fc="#808080", ec=C_OUT, lw=1.0, zorder=10))

    # Labels
    leader(ax, sx(ring_cx - ring_r), sy(ring_cy),
           sx(ring_cx - 55), sy(ring_cy + 40),
           f"25mm D-RING\n{DRING_WLL}kg WLL\nMcMaster #3641T29",
           color="#D0A030", fs=6.5,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    leader(ax, sx(plate_x + plate_t / 2), sy(plate_y + plate_h + 3),
           sx(plate_x + 40), sy(plate_y + plate_h + 30),
           f"MOUNTING PLATE\n{plate_t}mm STEEL\nFILLET WELDED",
           color=C_STEEL, fs=6,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # Dimensions
    draw_dim_h(ax, sx(plate_x), sx(plate_x + plate_t), sy(rhs_y - 15),
               f"{plate_t}mm", offset=sy(3), fs=5.5, font=FONT)
    draw_dim_v(ax, sx(rhs_x + FRAME_RHS + 10), sy(rhs_y), sy(rhs_y + FRAME_RHS),
               f"{FRAME_RHS}mm", offset=sx(3), fs=5.5, right=True, font=FONT)

    # Detail A border
    ax.add_patch(Rectangle((sx(DA_OX - 5), sy(DA_OY)),
                            sx(180), sy(190),
                            fc="none", ec=C_DIM, lw=0.8, ls="--", zorder=1))

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL B — Anti-Rotation Lip (cross-section through platform edge)
    # Shows platform beam, rubber mat, lip, and IBC cage foot
    # ══════════════════════════════════════════════════════════════════════════
    DB_OX = 240
    DB_OY = 280

    ax.text(sx(DB_OX + 100), sy(DB_OY + 190),
            "DETAIL B — ANTI-ROTATION LIP\n(CROSS-SECTION THROUGH PLATFORM EDGE)",
            ha="center", va="bottom", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # Platform beam (cross-section)
    beam_x = DB_OX + 20
    beam_y = DB_OY + 30
    beam_show_w = 140  # show wider to give context
    ax.add_patch(Rectangle((sx(beam_x), sy(beam_y)),
                            sx(beam_show_w), sy(FRAME_RHS),
                            fc=C_FRAME, ec=C_OUT, lw=2.0, zorder=5))
    # Hollow
    ax.add_patch(Rectangle((sx(beam_x + FRAME_T), sy(beam_y + FRAME_T)),
                            sx(beam_show_w - 2 * FRAME_T), sy(FRAME_RHS - 2 * FRAME_T),
                            fc="#D8D8D8", ec=C_OUT, lw=0.8, zorder=6))
    ax.text(sx(beam_x + beam_show_w / 2), sy(beam_y + FRAME_RHS / 2),
            f"PLATFORM BEAM\n{FRAME_RHS}x{FRAME_RHS}x{FRAME_T} RHS",
            ha="center", va="center", fontsize=5.5, color=C_OUT, **FONT, zorder=10)

    # Rubber mat on top of beam
    mat_y = beam_y + FRAME_RHS
    ax.add_patch(Rectangle((sx(beam_x + 5), sy(mat_y)),
                            sx(beam_show_w - 10), sy(MAT_T),
                            fc=C_RUBBER, ec=C_OUT, lw=1.0, zorder=7, alpha=0.8))
    ax.text(sx(beam_x + beam_show_w / 2), sy(mat_y + MAT_T / 2),
            f"{MAT_T}mm RUBBER MAT", ha="center", va="center",
            fontsize=5, color="white", fontweight="bold", **FONT, zorder=10)

    # Anti-rotation lip (left edge = near frame edge)
    lip_x = beam_x
    lip_y = mat_y
    ax.add_patch(Rectangle((sx(lip_x), sy(lip_y)),
                            sx(FRAME_LIP_T), sy(FRAME_LIP_H),
                            fc=C_STEEL, ec=C_OUT, lw=1.5, hatch="///", zorder=8))

    # Weld at lip base
    weld_verts = [
        (sx(lip_x + FRAME_LIP_T), sy(lip_y)),
        (sx(lip_x + FRAME_LIP_T + 5), sy(lip_y + 5)),
        (sx(lip_x + FRAME_LIP_T + 5), sy(lip_y - 3)),
    ]
    ax.add_patch(Polygon(weld_verts, closed=True,
                         fc="#404040", ec=C_OUT, lw=0.5, zorder=9))

    # IBC cage foot (ghost — sitting on mat, restrained by lip)
    cage_foot_x = lip_x + FRAME_LIP_T + 3
    cage_foot_y = mat_y + MAT_T
    cage_foot_w = 50
    cage_foot_h = 30
    ax.add_patch(Rectangle((sx(cage_foot_x), sy(cage_foot_y)),
                            sx(cage_foot_w), sy(cage_foot_h),
                            fc=C_BLUE_IBC, ec=C_OUT, lw=1.2, ls="--",
                            alpha=0.3, zorder=7))
    ax.text(sx(cage_foot_x + cage_foot_w / 2), sy(cage_foot_y + cage_foot_h / 2),
            "IBC CAGE\nFOOT", ha="center", va="center",
            fontsize=5, color=C_BLUE_IBC, **FONT, zorder=10)

    # Arrow showing lip prevents lateral movement
    arr_x = lip_x - 8
    ax.annotate("", xy=(sx(lip_x + 1), sy(lip_y + FRAME_LIP_H / 2)),
                xytext=(sx(lip_x - 25), sy(lip_y + FRAME_LIP_H / 2)),
                arrowprops=dict(arrowstyle="->", color="#C04040", lw=2.0))
    ax.text(sx(lip_x - 28), sy(lip_y + FRAME_LIP_H / 2),
            "LATERAL\nRETAINED", ha="right", va="center",
            fontsize=5.5, color="#C04040", fontweight="bold", **FONT, zorder=15)

    # Labels
    leader(ax, sx(lip_x + FRAME_LIP_T / 2), sy(lip_y + FRAME_LIP_H),
           sx(lip_x + 50), sy(lip_y + FRAME_LIP_H + 35),
           f"ANTI-ROTATION LIP\n{FRAME_LIP_T}mm STEEL x {FRAME_LIP_H}mm H\nFILLET WELDED TO PLATFORM\nFULL PERIMETER",
           color=C_STEEL, fs=6,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # Dimensions
    draw_dim_v(ax, sx(lip_x - 12), sy(lip_y), sy(lip_y + FRAME_LIP_H),
               f"{FRAME_LIP_H}mm", offset=sx(3), fs=5.5, right=False, font=FONT)
    draw_dim_v(ax, sx(beam_x - 12), sy(beam_y), sy(mat_y),
               f"{FRAME_RHS}mm", offset=sx(3), fs=5.5, right=False, font=FONT)
    draw_dim_v(ax, sx(beam_x + beam_show_w + 10), sy(mat_y), sy(mat_y + MAT_T),
               f"{MAT_T}", offset=sx(3), fs=5, right=True, font=FONT)

    # Detail B border
    ax.add_patch(Rectangle((sx(DB_OX - 5), sy(DB_OY)),
                            sx(220), sy(190),
                            fc="none", ec=C_DIM, lw=0.8, ls="--", zorder=1))

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL C — Access Gate (front elevation)
    # Shows removable panel at base of frame for lower IBC drain valve access
    # ══════════════════════════════════════════════════════════════════════════
    DC_OX = 30
    DC_OY = 20

    ax.text(sx(DC_OX + 170), sy(DC_OY + 230),
            "DETAIL C — ACCESS GATE\n(FRONT ELEVATION — LOWER IBC DRAIN VALVE ACCESS)",
            ha="center", va="bottom", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # Frame uprights (two verticals)
    upright_h = 200
    upright_l_x = DC_OX + 30
    upright_r_x = DC_OX + 30 + 250
    for ux in [upright_l_x, upright_r_x]:
        ax.add_patch(Rectangle((sx(ux), sy(DC_OY + 10)),
                                sx(FRAME_RHS), sy(upright_h),
                                fc=C_FRAME, ec=C_OUT, lw=1.5, zorder=5))
        ax.add_patch(Rectangle((sx(ux + FRAME_T), sy(DC_OY + 10 + FRAME_T)),
                                sx(FRAME_RHS - 2 * FRAME_T),
                                sy(upright_h - 2 * FRAME_T),
                                fc="#D8D8D8", ec=C_OUT, lw=0.5, zorder=6))

    # Gate panel (removable, shown between uprights)
    gate_x = upright_l_x + FRAME_RHS
    gate_w = upright_r_x - gate_x
    gate_y = DC_OY + 10
    gate_panel_h = 120  # visual gate height at this scale
    ax.add_patch(Rectangle((sx(gate_x), sy(gate_y)),
                            sx(gate_w), sy(gate_panel_h),
                            fc="#F0E0E0", ec="#C04040", lw=2.0, zorder=7))
    # Cross pattern on gate (mesh/perforated)
    for frac in np.arange(0.15, 1.0, 0.2):
        ax.plot([sx(gate_x + gate_w * frac), sx(gate_x + gate_w * frac)],
                [sy(gate_y + 5), sy(gate_y + gate_panel_h - 5)],
                color="#C04040", lw=0.5, alpha=0.3, zorder=8)

    ax.text(sx(gate_x + gate_w / 2), sy(gate_y + gate_panel_h / 2),
            f"REMOVABLE GATE PANEL\nH=0-{GATE_H}mm\n(BOLTED — 4x M{GATE_BOLT_D})",
            ha="center", va="center", fontsize=6, color="#C04040",
            fontweight="bold", **FONT, zorder=10)

    # Bolt positions (4 corners of gate)
    bolt_inset = 15
    for bx in [gate_x + bolt_inset, gate_x + gate_w - bolt_inset]:
        for by in [gate_y + bolt_inset, gate_y + gate_panel_h - bolt_inset]:
            ax.add_patch(Circle((sx(bx), sy(by)), sx(5),
                                 fc="#808080", ec=C_OUT, lw=1.0, zorder=12))
            # Hex nut symbol
            ax.add_patch(Circle((sx(bx), sy(by)), sx(8),
                                 fc="none", ec=C_OUT, lw=0.6, zorder=12))

    # IBC valve behind gate (ghost)
    valve_x = gate_x + gate_w / 2 - 20
    valve_y = gate_y + 20
    ax.add_patch(Rectangle((sx(valve_x), sy(valve_y)),
                            sx(40), sy(25),
                            fc=C_BLUE_IBC, ec=C_OUT, lw=1.0, ls="--",
                            alpha=0.25, zorder=6))
    ax.text(sx(valve_x + 20), sy(valve_y + 12),
            "2\" BALL\nVALVE", ha="center", va="center",
            fontsize=4.5, color=C_BLUE_IBC, **FONT, zorder=10)

    # Labels
    leader(ax, sx(gate_x + gate_w + 15), sy(gate_y + gate_panel_h / 2),
           sx(gate_x + gate_w + 60), sy(gate_y + gate_panel_h + 30),
           f"GATE REMOVED FOR\nDRAIN VALVE ACCESS\n(2x GATES — NEAR/FAR COLUMNS)",
           color="#C04040", fs=6,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    leader(ax, sx(upright_l_x + FRAME_RHS / 2), sy(DC_OY + 10 + upright_h),
           sx(upright_l_x - 30), sy(DC_OY + 10 + upright_h + 20),
           f"FRAME UPRIGHT\n{FRAME_RHS}x{FRAME_RHS}x{FRAME_T} RHS",
           color=C_FRAME, fs=6,
           ha="right", va="bottom", arrow_style="-|>", font=FONT)

    # Dimensions
    draw_dim_v(ax, sx(upright_l_x - 15), sy(gate_y), sy(gate_y + gate_panel_h),
               f"{GATE_H}mm\nGATE H", offset=sx(3), fs=5.5, right=False, font=FONT)
    draw_dim_h(ax, sx(gate_x), sx(gate_x + gate_w), sy(gate_y - 15),
               "GATE WIDTH", offset=sy(3), fs=5.5, font=FONT)

    # Detail C border
    ax.add_patch(Rectangle((sx(DC_OX - 5), sy(DC_OY)),
                            sx(350), sy(230),
                            fc="none", ec=C_DIM, lw=0.8, ls="--", zorder=1))

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL D — Lashing Arrangement (schematic top-down showing strap routing)
    # ══════════════════════════════════════════════════════════════════════════
    DD_OX = 400
    DD_OY = 20

    ax.text(sx(DD_OX + 90), sy(DD_OY + 230),
            "DETAIL D — TRANSPORT LASHING\n(SCHEMATIC — STRAP ROUTING)",
            ha="center", va="bottom", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # Simplified side elevation showing IBC with ratchet strap
    sch_x = DD_OX + 20
    sch_y = DD_OY + 20
    sch_w = 140  # IBC width representation
    sch_h = 180  # full stack height representation

    # IBC stack (simplified)
    ax.add_patch(Rectangle((sx(sch_x), sy(sch_y)),
                            sx(sch_w), sy(sch_h / 2),
                            fc=C_BROWN_IBC, ec=C_OUT, lw=1.2, alpha=0.3, zorder=5))
    ax.add_patch(Rectangle((sx(sch_x), sy(sch_y + sch_h / 2 + 5)),
                            sx(sch_w), sy(sch_h / 2),
                            fc=C_BLUE_IBC, ec=C_OUT, lw=1.2, alpha=0.3, zorder=5))
    ax.text(sx(sch_x + sch_w / 2), sy(sch_y + sch_h / 4),
            "BOTTOM\nTIER", ha="center", va="center", fontsize=5.5,
            color=C_OUT, **FONT, zorder=10)
    ax.text(sx(sch_x + sch_w / 2), sy(sch_y + 3 * sch_h / 4 + 3),
            "TOP\nTIER", ha="center", va="center", fontsize=5.5,
            color=C_OUT, **FONT, zorder=10)

    # Platform line
    ax.plot([sx(sch_x - 10), sx(sch_x + sch_w + 10)],
            [sy(sch_y + sch_h / 2 + 2), sy(sch_y + sch_h / 2 + 2)],
            color=C_FRAME, lw=2.0, zorder=6)
    ax.text(sx(sch_x + sch_w + 15), sy(sch_y + sch_h / 2 + 2),
            "PLATFORM", ha="left", va="center", fontsize=5,
            color=C_FRAME, **FONT, zorder=10)

    # D-ring positions
    dring_color = "#D0A030"
    dring_positions_sch = [
        (sch_x - 8, sch_y + 25, "1"),
        (sch_x + sch_w + 8, sch_y + 25, "2"),
        (sch_x - 8, sch_y + sch_h / 2 + 25, "3"),
        (sch_x + sch_w + 8, sch_y + sch_h / 2 + 25, "4"),
    ]
    for dx, dy, dlabel in dring_positions_sch:
        ax.add_patch(Circle((sx(dx), sy(dy)), sx(6),
                             fc=dring_color, ec=C_OUT, lw=1.0, zorder=11))
        ax.text(sx(dx), sy(dy), dlabel, ha="center", va="center",
                fontsize=5, color=C_OUT, fontweight="bold", **FONT, zorder=12)

    # Ratchet strap lines (over top of IBC, D-ring to D-ring)
    strap_color = "#2060A0"
    # Bottom tier strap: 1->2 over the bottom IBC
    strap_y_bot = sch_y + sch_h / 2 - 5
    ax.plot([sx(sch_x - 8), sx(sch_x + sch_w / 2)],
            [sy(sch_y + 25), sy(strap_y_bot)],
            color=strap_color, lw=2.0, ls="-", zorder=8)
    ax.plot([sx(sch_x + sch_w / 2), sx(sch_x + sch_w + 8)],
            [sy(strap_y_bot), sy(sch_y + 25)],
            color=strap_color, lw=2.0, ls="-", zorder=8)

    # Top tier strap: 3->4 over the top IBC
    strap_y_top = sch_y + sch_h - 5
    ax.plot([sx(sch_x - 8), sx(sch_x + sch_w / 2)],
            [sy(sch_y + sch_h / 2 + 25), sy(strap_y_top)],
            color=strap_color, lw=2.0, ls="-", zorder=8)
    ax.plot([sx(sch_x + sch_w / 2), sx(sch_x + sch_w + 8)],
            [sy(strap_y_top), sy(sch_y + sch_h / 2 + 25)],
            color=strap_color, lw=2.0, ls="-", zorder=8)

    # Strap labels
    ax.text(sx(sch_x + sch_w / 2), sy(strap_y_bot + 8),
            "RATCHET STRAP\n(BOTTOM TIER)", ha="center", va="bottom",
            fontsize=5, color=strap_color, fontweight="bold", **FONT, zorder=15)
    ax.text(sx(sch_x + sch_w / 2), sy(strap_y_top + 8),
            "RATCHET STRAP\n(TOP TIER)", ha="center", va="bottom",
            fontsize=5, color=strap_color, fontweight="bold", **FONT, zorder=15)

    # Notes for Detail D
    dn_x = sx(DD_OX + 10)
    dn_top = sy(DD_OY + 12)
    d_notes = [
        "- 25mm ratchet straps, 1,100kg WLL",
        "- D-ring to D-ring over IBC top",
        "- 1 strap per tier per side (4 total)",
        "- Tighten before transport",
        "- Check strap tension after 50km",
    ]
    for i, note in enumerate(d_notes):
        ax.text(dn_x, dn_top - i * sy(6), note,
                ha="left", va="top", fontsize=5.5, color=C_DIM,
                **FONT, zorder=15)

    # Detail D border
    ax.add_patch(Rectangle((sx(DD_OX - 5), sy(DD_OY)),
                            sx(200), sy(230),
                            fc="none", ec=C_DIM, lw=0.8, ls="--", zorder=1))

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 3 OF 3",
                drawing_title="IBC STACKING & SECURING",
                subtitle="FASTENING DETAILS — D-RING - LIP - ACCESS GATE - LASHING",
                scale_note="SCALE ~ 5:1 - ALL DIMS IN mm - DETAILS A-D",
                height=0.06)

    fig.savefig("diagrams/ibc-stacking-sheet3.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/ibc-stacking-sheet3.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-stacking-sheet3.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    os.makedirs("diagrams", exist_ok=True)
    print("Generating IBC stacking diagrams...")
    sheet1()  # cross-section elevation -> ibc-stacking-sheet1.png
    sheet2()  # plan view -> ibc-stacking-sheet2.png
    sheet3()  # fastening details -> ibc-stacking-sheet3.png
    print("Done.")
