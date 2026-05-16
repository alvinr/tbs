#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_shelf_diagram.py  —  TBS-001 Chemistry Prep Shelves

Sheet 1 — Pinhole Wall Elevation (1:15):
  Interior elevation of pinhole wall (Yd=0) showing both fold-down shelves
  in deployed and folded positions.  X horizontal, Z vertical.

Sheet 2 — Plan View (1:15):
  Top-down view showing shelf depth relative to walkway, processing tray,
  and pump manifold.  Yd horizontal (wall at left), X vertical.

Sheet 3 — Hinge & Support Detail (1:5):
  Cross-section through one shelf perpendicular to pinhole wall.
  Shows hinge, frame, wall attachment, folding leg, and ball catch.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch
from matplotlib.lines import Line2D

from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader
from tbs_constants import (
    svg_path, SVG_DIR,
    C_LEN, C_WID, C_HGT,
    PUMP_X, PUMP_W, PUMP_H_LO, PUMP_H_HI,
    WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T,
    CONTAINER_RIB_SPACING,
    PROC_TRAY_YD_NEAR, PROC_TRAY_RIM,
    IBC_COL_X, IBC_W,
    SHELF_A_X, SHELF_B_X, SHELF_W, SHELF_DEPTH, SHELF_H, SHELF_T, SHELF_GAP,
    C_OUT, C_DIM, C_STEEL, C_ALUM,
)

# ── Local palette ────────────────────────────────────────────────────────────
BG       = "#FFFFFF"
C_SHELF  = "#C8B06A"   # phenolic ply — warm tan
C_FRAME  = C_STEEL     # steel SHS frame
C_HINGE  = "#808090"   # hinge hardware
C_TRAY   = "#D0D8E0"   # processing tray (ghost)
C_WALKWAY = "#E8E8E8"  # walkway grating fill
C_GHOST  = "#A0A0A0"   # ghost outlines (folded position)
C_CABLE  = "#607080"   # cable trunking
C_PUMP   = "#B8C8B0"   # pump manifold context

# ── Derived constants ──────��─────────────────────────────────────────────────
SHELF_A_R = SHELF_A_X + SHELF_W         # 3,650mm
SHELF_B_R = SHELF_B_X + SHELF_W         # 4,629mm
SHELF_FOLD_TOP = SHELF_H + SHELF_DEPTH  # 1,275mm (top edge when folded)
CABLE_TRUNK_H = 1800                     # cable trunking height AFF
CABLE_TRUNK_SIZE = 40                    # trunking cross-section (40×25mm)
LEG_LENGTH = 925                         # folding leg approximate length (H=1025 - 100)
# Leg pivots at shelf front edge (Yd=250), foot on walkway deck at H=100
# When deployed: leg is vertical from shelf underside down to deck
LEG_PIVOT_YD = SHELF_DEPTH              # pivot at front edge of shelf (Yd=250)
LEG_FOOT_H = WALKWAY_H                  # rests on walkway deck = 100mm


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — PINHOLE WALL ELEVATION
# ═══════════════════════════════════════════════════════════════════════════════

def sheet1():
    """Wall elevation showing both shelves deployed and folded."""
    # View range
    X_LO, X_HI = 2400, 4900
    Z_LO, Z_HI = -150, 2100

    # Scale functions (1:15 approx)
    def px(mm): return (mm - X_LO) / 15.0
    def pz(mm): return (mm - Z_LO) / 15.0

    fig_w = (X_HI - X_LO) / 15.0 / 6.0 + 2.0  # ~19 inches
    fig_h = (Z_HI - Z_LO) / 15.0 / 6.0 + 2.5  # ~17 inches
    fig, ax = plt.subplots(figsize=(18, 14), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(px(X_LO), px(X_HI))
    ax.set_ylim(pz(Z_LO), pz(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container wall ribs (vertical dashed lines at 457mm spacing) ──
    rib_x = PUMP_X  # start from a known rib
    while rib_x > X_LO:
        rib_x -= CONTAINER_RIB_SPACING
    while rib_x < X_HI:
        if X_LO < rib_x < X_HI:
            ax.plot([px(rib_x), px(rib_x)], [pz(0), pz(C_HGT)],
                    color="#D0D0D0", lw=0.4, ls="--", zorder=1)
        rib_x += CONTAINER_RIB_SPACING

    # ── Floor line ──
    ax.plot([px(X_LO), px(X_HI)], [pz(0), pz(0)],
            color=C_OUT, lw=1.5, zorder=5)

    # ── Walkway deck level ──
    ax.plot([px(X_LO + 100), px(X_HI - 100)], [pz(WALKWAY_H), pz(WALKWAY_H)],
            color=C_OUT, lw=0.8, ls=(0, (4, 2)), zorder=3)
    ax.text(px(X_HI - 50), pz(WALKWAY_H + 15), "WALKWAY DECK H=100",
            fontsize=5, color=C_DIM, ha="right", va="bottom")

    # ── Cable trunking at H=1800mm ──
    trunk_y = CABLE_TRUNK_H
    ax.add_patch(Rectangle((px(X_LO + 50), pz(trunk_y)),
                            px(X_HI - 50) - px(X_LO + 50), pz(trunk_y + 25) - pz(trunk_y),
                            fc=C_CABLE, ec=C_OUT, lw=0.6, alpha=0.5, zorder=4))
    ax.text(px(X_HI - 50), pz(trunk_y + 35), "CABLE TRUNKING 40×25mm PVC — H=1,800",
            fontsize=5, color=C_DIM, ha="right", va="bottom")

    # ── Pump manifold (context, dashed) ──
    pm_x1, pm_x2 = PUMP_X, PUMP_X + PUMP_W
    pm_z1, pm_z2 = PUMP_H_LO, PUMP_H_HI
    ax.add_patch(Rectangle((px(pm_x1), pz(pm_z1)),
                            px(pm_x2) - px(pm_x1), pz(pm_z2) - pz(pm_z1),
                            fc=C_PUMP, ec=C_OUT, lw=0.8, ls="--", alpha=0.4, zorder=3))
    ax.text(px((pm_x1 + pm_x2) / 2), pz(pm_z2 + 20), "PUMP\nMANIFOLD",
            fontsize=5, color=C_DIM, ha="center", va="bottom")

    # ── Draw shelves (deployed — solid) ──
    for sx_left in [SHELF_A_X, SHELF_B_X]:
        sx_right = sx_left + SHELF_W
        # Shelf body (deployed = horizontal at SHELF_H)
        ax.add_patch(Rectangle((px(sx_left), pz(SHELF_H - SHELF_T)),
                                px(sx_right) - px(sx_left),
                                pz(SHELF_H) - pz(SHELF_H - SHELF_T),
                                fc=C_SHELF, ec=C_OUT, lw=1.2, zorder=8))
        # Hinge line (at bottom of shelf, against wall)
        ax.plot([px(sx_left), px(sx_right)],
                [pz(SHELF_H - SHELF_T), pz(SHELF_H - SHELF_T)],
                color=C_HINGE, lw=2.0, zorder=9)

        # Folding leg (shown as line from shelf underside to walkway deck)
        leg_x = sx_left + SHELF_W / 2  # center of shelf
        ax.plot([px(leg_x), px(leg_x)],
                [pz(WALKWAY_H), pz(SHELF_H - SHELF_T)],
                color=C_FRAME, lw=1.5, ls="-", zorder=7)
        # Leg foot
        ax.plot(px(leg_x), pz(WALKWAY_H), "v", color=C_FRAME, ms=4, zorder=9)

        # Wall bracket (angle iron behind hinge)
        bracket_z = SHELF_H - SHELF_T - 5  # just below shelf
        ax.add_patch(Rectangle((px(sx_left), pz(bracket_z - 50)),
                                px(sx_right) - px(sx_left),
                                pz(bracket_z) - pz(bracket_z - 50),
                                fc=C_FRAME, ec=C_OUT, lw=0.6, alpha=0.5, zorder=6))

    # ── Draw shelves (folded — ghost) ���─
    for sx_left in [SHELF_A_X, SHELF_B_X]:
        sx_right = sx_left + SHELF_W
        # Folded position: vertical against wall, from hinge line up
        fold_bottom = SHELF_H - SHELF_T
        fold_top = fold_bottom + SHELF_DEPTH
        ax.add_patch(Rectangle((px(sx_left), pz(fold_bottom)),
                                px(sx_right) - px(sx_left),
                                pz(fold_top) - pz(fold_bottom),
                                fc=C_GHOST, ec=C_GHOST, lw=1.0, ls="--",
                                alpha=0.15, zorder=4))
        ax.add_patch(Rectangle((px(sx_left), pz(fold_bottom)),
                                px(sx_right) - px(sx_left),
                                pz(fold_top) - pz(fold_bottom),
                                fc="none", ec=C_GHOST, lw=1.0, ls="--",
                                zorder=5))

    # ── Dimensions ──
    # Shelf A width
    draw_dim_h(ax, px(SHELF_A_X), px(SHELF_A_R), pz(SHELF_H + 60),
               "750", offset=8, fs=6)
    # Shelf B width
    draw_dim_h(ax, px(SHELF_B_X), px(SHELF_B_R), pz(SHELF_H + 60),
               "750", offset=8, fs=6)
    # Gap
    draw_dim_h(ax, px(SHELF_A_R), px(SHELF_B_X), pz(SHELF_H + 120),
               "229", offset=8, fs=5.5)
    # Height above floor
    draw_dim_v(ax, px(SHELF_A_X - 80), pz(0), pz(SHELF_H),
               "1,025", offset=8, fs=6)
    # Height above walkway deck
    draw_dim_v(ax, px(SHELF_A_X - 40), pz(WALKWAY_H), pz(SHELF_H),
               "925", offset=6, fs=5.5, right=True)
    # Folded top edge height
    draw_dim_v(ax, px(SHELF_B_R + 60), pz(0), pz(SHELF_FOLD_TOP),
               "1,475\n(FOLDED)", offset=8, fs=5.5, right=True)
    # Clearance to trunking
    draw_dim_v(ax, px(SHELF_B_R + 120), pz(SHELF_FOLD_TOP), pz(CABLE_TRUNK_H),
               "325\nCLEAR", offset=8, fs=5, right=True)
    # Overall X extent from pump manifold
    draw_dim_h(ax, px(PUMP_X + PUMP_W), px(SHELF_A_X), pz(-80),
               "100 GAP", offset=8, fs=5.5)

    # ── Leader callouts ──
    leader(ax, px(SHELF_A_X + 375), pz(SHELF_H - 11),
           px(SHELF_A_X + 375), pz(SHELF_H + 180),
           "18mm PHENOLIC PLY\nON 25×25×3mm SHS FRAME",
           fs=5.5, ha="center")
    leader(ax, px(SHELF_A_X + 50), pz(SHELF_H - SHELF_T - 25),
           px(SHELF_A_X - 60), pz(SHELF_H - 100),
           "SS PIANO HINGE\n50mm × 750mm",
           fs=5.5, ha="right")
    leader(ax, px(SHELF_A_X + 375), pz(WALKWAY_H + 5),
           px(SHELF_A_X + 500), pz(WALKWAY_H - 60),
           "FOLDING LEG\n25×25mm SHS",
           fs=5.5, ha="left")
    leader(ax, px(SHELF_B_X + 375), pz(SHELF_FOLD_TOP - 30),
           px(SHELF_B_X + 550), pz(SHELF_FOLD_TOP + 50),
           "FOLDED POSITION\n(GHOST)",
           fs=5.5, ha="left", color=C_GHOST)
    # Ball catch
    leader(ax, px(SHELF_A_X + 375), pz(SHELF_FOLD_TOP - 5),
           px(SHELF_A_X + 600), pz(SHELF_FOLD_TOP + 80),
           "BALL CATCH\nLATCH (×1/SHELF)",
           fs=5, ha="left")

    # ── Legend ──
    legend_x = px(X_LO + 50)
    legend_z = pz(Z_HI - 80)
    ax.text(legend_x, legend_z, "LEGEND:", fontsize=6, fontweight="bold",
            color=C_OUT, va="top")
    ax.add_patch(Rectangle((legend_x, legend_z - 18), 15, 8,
                            fc=C_SHELF, ec=C_OUT, lw=0.8))
    ax.text(legend_x + 18, legend_z - 14, "Shelf deployed", fontsize=5,
            color=C_DIM, va="center")
    ax.add_patch(Rectangle((legend_x, legend_z - 34), 15, 8,
                            fc=C_GHOST, ec=C_GHOST, lw=0.8, ls="--", alpha=0.3))
    ax.text(legend_x + 18, legend_z - 30, "Shelf folded (transport)", fontsize=5,
            color=C_DIM, va="center")

    # ── Title block ──
    title_block(ax, "SHEET 1 OF 3",
                drawing_title="CHEMISTRY PREP SHELVES",
                subtitle="PINHOLE WALL ELEVATION — DEPLOYED AND FOLDED",
                scale_note="SCALE ~1:15",
                doc_id="TBS-001 · Chem Prep")

    out = "diagrams/shelf-sheet1.png"
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  [1/3] {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — PLAN VIEW
# ═══════════��═══════════════════════════════════════════════════════════════════

def sheet2():
    """Plan view showing shelf depth relative to walkway."""
    # View: looking down. X vertical on page, Yd horizontal (wall at left)
    # Show X=2400 to 5000, Yd=-50 to 700
    X_LO, X_HI = 2300, 5100
    YD_LO, YD_HI = -100, 750

    def px(yd): return (yd - YD_LO) / 12.0
    def py(x): return (x - X_LO) / 12.0

    fig, ax = plt.subplots(figsize=(16, 22), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(px(YD_LO), px(YD_HI))
    ax.set_ylim(py(X_LO), py(X_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Pinhole wall (Yd=0, vertical line on page) ──
    ax.plot([px(0), px(0)], [py(X_LO + 50), py(X_HI - 50)],
            color=C_OUT, lw=2.0, zorder=5)
    ax.text(px(-30), py((X_LO + X_HI) / 2), "PINHOLE WALL\n(Yd=0)",
            fontsize=6, color=C_DIM, ha="right", va="center", rotation=90)

    # ── Walkway zone (Yd=0 to 300) ──
    ax.add_patch(Rectangle((px(0), py(X_LO + 100)),
                            px(WALKWAY_W) - px(0),
                            py(X_HI - 100) - py(X_LO + 100),
                            fc=C_WALKWAY, ec=C_OUT, lw=0.6, alpha=0.4, zorder=2))
    ax.text(px(WALKWAY_W / 2), py(X_LO + 150), "NEAR WALKWAY\n300mm WIDE",
            fontsize=5, color=C_DIM, ha="center", va="bottom", rotation=90)
    # Walkway outer edge
    ax.plot([px(WALKWAY_W), px(WALKWAY_W)], [py(X_LO + 100), py(X_HI - 100)],
            color=C_OUT, lw=0.8, ls=(0, (4, 2)), zorder=4)

    # ── Processing tray near edge (Yd=80, below shelf — at floor level) ──
    ax.plot([px(PROC_TRAY_YD_NEAR), px(PROC_TRAY_YD_NEAR)],
            [py(X_LO + 100), py(X_HI - 100)],
            color=C_TRAY, lw=0.6, ls=":", zorder=3)
    ax.text(px(PROC_TRAY_YD_NEAR + 10), py(X_HI - 120),
            "TRAY RIM\nYd=80\n(BELOW)", fontsize=4.5, color=C_TRAY, va="top")

    # ── Pump manifold context ──
    ax.add_patch(Rectangle((px(0), py(PUMP_X)),
                            px(80) - px(0),  # ~80mm depth on wall
                            py(PUMP_X + PUMP_W) - py(PUMP_X),
                            fc=C_PUMP, ec=C_OUT, lw=0.6, ls="--", alpha=0.4, zorder=3))
    ax.text(px(40), py(PUMP_X + PUMP_W / 2), "PUMP\nMANIFOLD",
            fontsize=5, color=C_DIM, ha="center", va="center")

    # ── IBC stack context (right end) ──
    ibc_yd_start = 0
    ax.add_patch(Rectangle((px(ibc_yd_start), py(IBC_COL_X)),
                            px(IBC_W) - px(ibc_yd_start) if IBC_W < YD_HI else px(YD_HI) - px(ibc_yd_start),
                            py(IBC_COL_X + 100) - py(IBC_COL_X),
                            fc="#E0E8F0", ec=C_OUT, lw=0.6, ls="--", alpha=0.3, zorder=2))
    ax.text(px(200), py(IBC_COL_X + 50), "IBC STACK →",
            fontsize=5, color=C_DIM, ha="center", va="center")

    # ── Shelves deployed (Yd=0 to 450, solid fill) ──
    for sx_left in [SHELF_A_X, SHELF_B_X]:
        sx_right = sx_left + SHELF_W
        ax.add_patch(Rectangle((px(0), py(sx_left)),
                                px(SHELF_DEPTH) - px(0),
                                py(sx_right) - py(sx_left),
                                fc=C_SHELF, ec=C_OUT, lw=1.2, zorder=6))
        # Label
        ax.text(px(SHELF_DEPTH / 2), py((sx_left + sx_right) / 2),
                f"SHELF {'A' if sx_left == SHELF_A_X else 'B'}\n750 × 450",
                fontsize=6, color=C_OUT, ha="center", va="center",
                fontweight="bold")

    # ── Shelf overhang annotation ──
    overhang = SHELF_DEPTH - WALKWAY_W  # 150mm
    draw_dim_h(ax, px(WALKWAY_W), px(SHELF_DEPTH),
               py(SHELF_A_X - 40), f"{overhang}", offset=6, fs=5.5)
    ax.text(px((WALKWAY_W + SHELF_DEPTH) / 2), py(SHELF_A_X - 70),
            "OVERHANG\nBEYOND WALKWAY", fontsize=4.5, color=C_DIM, ha="center")

    # ── Dimensions ──
    # Shelf depth from wall
    draw_dim_h(ax, px(0), px(SHELF_DEPTH), py(X_LO + 200),
               "450 DEPTH", offset=8, fs=6)
    # Walkway width
    draw_dim_h(ax, px(0), px(WALKWAY_W), py(X_LO + 300),
               "300 WALKWAY", offset=8, fs=5.5)
    # Shelf widths (along X axis = vertical on page)
    draw_dim_v(ax, px(SHELF_DEPTH + 80), py(SHELF_A_X), py(SHELF_A_R),
               "750", offset=8, fs=6, right=True)
    draw_dim_v(ax, px(SHELF_DEPTH + 80), py(SHELF_B_X), py(SHELF_B_R),
               "750", offset=8, fs=6, right=True)
    # Gap
    draw_dim_v(ax, px(SHELF_DEPTH + 40), py(SHELF_A_R), py(SHELF_B_X),
               "229", offset=6, fs=5.5, right=True)
    # Clearance from pump
    draw_dim_v(ax, px(-50), py(PUMP_X + PUMP_W), py(SHELF_A_X),
               "100", offset=6, fs=5.5)

    # ── Folding leg positions (dot at Yd=300, mid-shelf) ──
    for sx_left in [SHELF_A_X, SHELF_B_X]:
        leg_x = sx_left + SHELF_W / 2
        ax.plot(px(LEG_PIVOT_YD), py(leg_x), "s", color=C_FRAME, ms=5, zorder=8)
    leader(ax, px(LEG_PIVOT_YD), py(SHELF_A_X + SHELF_W / 2),
           px(LEG_PIVOT_YD + 120), py(SHELF_A_X + SHELF_W / 2 - 80),
           "LEG FOOT\n(ON DECK)",
           fs=5, ha="left")

    # ── Title block ──
    title_block(ax, "SHEET 2 OF 3",
                drawing_title="CHEMISTRY PREP SHELVES",
                subtitle="PLAN VIEW — DEPLOYED POSITION",
                scale_note="SCALE ~1:12",
                doc_id="TBS-001 · Chem Prep")

    out = "diagrams/shelf-sheet2.png"
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  [2/3] {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — HINGE & SUPPORT DETAIL
# ═══════════════════════════════════════════════════════════════════════════════

def sheet3():
    """Cross-section through one shelf showing hinge, leg, and wall attachment."""
    # View: looking along X axis (perpendicular to shelf width).
    # Yd horizontal (wall at left=0), Z vertical.
    YD_LO, YD_HI = -120, 650
    Z_LO, Z_HI = -50, 1600

    # Scale 1:5
    def px(yd): return (yd - YD_LO) / 5.0
    def pz(z): return (z - Z_LO) / 5.0

    fig, ax = plt.subplots(figsize=(16, 18), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(px(YD_LO), px(YD_HI))
    ax.set_ylim(pz(Z_LO), pz(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container wall section (Yd=0, corrugated) ──
    # Draw wall as thick vertical band at Yd=-5 to Yd=0
    wall_t = 2  # 2mm corrugated steel
    ax.add_patch(Rectangle((px(-wall_t - 15), pz(0)),
                            px(0) - px(-wall_t - 15),
                            pz(Z_HI - 50) - pz(0),
                            fc="#D8D8D8", ec=C_OUT, lw=1.0, zorder=3))
    # Corrugation rib bump (simplified)
    rib_w = 50  # rib protrusion depth
    rib_h = 80
    rib_z_center = SHELF_H - SHELF_T - 25  # at bracket height
    ax.add_patch(Rectangle((px(-wall_t - 15 - rib_w), pz(rib_z_center - rib_h / 2)),
                            px(-wall_t - 15) - px(-wall_t - 15 - rib_w),
                            pz(rib_z_center + rib_h / 2) - pz(rib_z_center - rib_h / 2),
                            fc="#C0C0C0", ec=C_OUT, lw=0.8, zorder=3))
    ax.text(px(-50), pz(Z_HI - 80), "CONTAINER\nWALL", fontsize=5.5,
            color=C_DIM, ha="center", va="top")

    # ── Exterior reinforcing plate ──
    plate_w = 6
    plate_h = 100
    ax.add_patch(Rectangle((px(-wall_t - 15 - rib_w - plate_w),
                             pz(rib_z_center - plate_h / 2)),
                            px(-wall_t - 15 - rib_w) - px(-wall_t - 15 - rib_w - plate_w),
                            pz(rib_z_center + plate_h / 2) - pz(rib_z_center - plate_h / 2),
                            fc=C_FRAME, ec=C_OUT, lw=0.8, zorder=3))
    leader(ax, px(-wall_t - 15 - rib_w - plate_w / 2), pz(rib_z_center - plate_h / 2),
           px(-80), pz(rib_z_center - 120),
           "75×100×6mm\nREINFORCING\nPLATE (EXT)",
           fs=5, ha="center")

    # ── Wall angle bracket (50×50×5mm) ──
    bracket_z_bottom = SHELF_H - SHELF_T - 55
    bracket_z_top = SHELF_H - SHELF_T
    bracket_yd = 0
    bracket_depth = 5  # 5mm thick angle, vertical leg
    # Vertical leg (against wall)
    ax.add_patch(Rectangle((px(bracket_yd), pz(bracket_z_bottom)),
                            px(bracket_yd + bracket_depth) - px(bracket_yd),
                            pz(bracket_z_top) - pz(bracket_z_bottom),
                            fc=C_FRAME, ec=C_OUT, lw=0.8, zorder=5))
    # Horizontal leg (supports hinge)
    ax.add_patch(Rectangle((px(bracket_yd), pz(bracket_z_top - 5)),
                            px(bracket_yd + 50) - px(bracket_yd),
                            pz(bracket_z_top) - pz(bracket_z_top - 5),
                            fc=C_FRAME, ec=C_OUT, lw=0.8, zorder=5))
    leader(ax, px(25), pz(bracket_z_bottom),
           px(80), pz(bracket_z_bottom - 60),
           "50×50×5mm STEEL\nANGLE BRACKET",
           fs=5, ha="left")

    # ── M10 through-bolt ──
    bolt_z = rib_z_center
    bolt_yd = bracket_depth / 2
    ax.plot([px(-wall_t - 15 - rib_w - plate_w), px(bracket_yd + bracket_depth)],
            [pz(bolt_z), pz(bolt_z)],
            color=C_OUT, lw=1.5, zorder=6)
    ax.plot(px(bolt_yd), pz(bolt_z), "o", color=C_OUT, ms=4, zorder=7)
    leader(ax, px(bolt_yd), pz(bolt_z + 3),
           px(80), pz(bolt_z + 50),
           "M10 THROUGH-BOLT",
           fs=5, ha="left")

    # ── Piano hinge ──
    hinge_z = SHELF_H - SHELF_T
    hinge_r = 4  # hinge barrel radius
    # Hinge barrel (circle at hinge line)
    from matplotlib.patches import Circle
    ax.add_patch(Circle((px(bracket_depth + hinge_r), pz(hinge_z)),
                        pz(hinge_z + hinge_r) - pz(hinge_z),
                        fc=C_HINGE, ec=C_OUT, lw=0.8, zorder=8))
    # Wall leaf (on bracket)
    ax.add_patch(Rectangle((px(bracket_depth), pz(hinge_z - 25)),
                            px(bracket_depth + 25) - px(bracket_depth),
                            pz(hinge_z) - pz(hinge_z - 25),
                            fc=C_HINGE, ec=C_OUT, lw=0.6, alpha=0.7, zorder=7))
    # Shelf leaf
    ax.add_patch(Rectangle((px(bracket_depth), pz(hinge_z)),
                            px(bracket_depth + 25) - px(bracket_depth),
                            pz(hinge_z + 4) - pz(hinge_z),
                            fc=C_HINGE, ec=C_OUT, lw=0.6, alpha=0.7, zorder=7))
    leader(ax, px(bracket_depth + hinge_r), pz(hinge_z + hinge_r + 2),
           px(-30), pz(hinge_z + 80),
           "SS PIANO HINGE\n50mm WIDE",
           fs=5, ha="right")

    # ── Shelf — deployed (horizontal) ──
    shelf_z_bottom = SHELF_H - SHELF_T
    shelf_z_top = SHELF_H
    shelf_yd_front = SHELF_DEPTH  # 450mm from wall
    # Frame (SHS perimeter)
    frame_t = 4  # 4mm visible frame thickness below ply
    ax.add_patch(Rectangle((px(bracket_depth + 10), pz(shelf_z_bottom)),
                            px(shelf_yd_front) - px(bracket_depth + 10),
                            pz(shelf_z_bottom + frame_t) - pz(shelf_z_bottom),
                            fc=C_FRAME, ec=C_OUT, lw=0.6, zorder=8))
    # Ply surface
    ax.add_patch(Rectangle((px(bracket_depth + 10), pz(shelf_z_bottom + frame_t)),
                            px(shelf_yd_front) - px(bracket_depth + 10),
                            pz(shelf_z_top) - pz(shelf_z_bottom + frame_t),
                            fc=C_SHELF, ec=C_OUT, lw=1.0, zorder=8))
    # Front edge frame
    ax.add_patch(Rectangle((px(shelf_yd_front - 25), pz(shelf_z_bottom)),
                            px(shelf_yd_front) - px(shelf_yd_front - 25),
                            pz(shelf_z_top) - pz(shelf_z_bottom),
                            fc=C_FRAME, ec=C_OUT, lw=0.6, zorder=8))

    # Shelf surface label
    ax.text(px(SHELF_DEPTH / 2 + 20), pz(SHELF_H + 15),
            "18mm PHENOLIC PLY — CHEMICAL RESISTANT", fontsize=5.5,
            color=C_DIM, ha="center", va="bottom")
    # Thickness dimension
    draw_dim_v(ax, px(shelf_yd_front + 30), pz(shelf_z_bottom), pz(shelf_z_top),
               "22", offset=6, fs=6, right=True)

    # ── Folding leg (deployed) ──
    # Leg pivots at shelf underside at Yd≈300 (2/3 depth), foot on walkway deck at H=100
    leg_pivot_yd = LEG_PIVOT_YD
    leg_pivot_z = shelf_z_bottom
    leg_foot_yd = LEG_PIVOT_YD  # straight down
    leg_foot_z = WALKWAY_H
    ax.plot([px(leg_pivot_yd), px(leg_foot_yd)],
            [pz(leg_pivot_z), pz(leg_foot_z)],
            color=C_FRAME, lw=2.5, zorder=7)
    # Leg cross-section indicator
    ax.plot(px(leg_pivot_yd), pz(leg_pivot_z), "o", color=C_FRAME, ms=5, zorder=9)
    ax.plot(px(leg_foot_yd), pz(leg_foot_z), "v", color=C_FRAME, ms=5, zorder=9)
    leader(ax, px(leg_pivot_yd + 5), pz((leg_pivot_z + leg_foot_z) / 2),
           px(leg_pivot_yd + 100), pz((leg_pivot_z + leg_foot_z) / 2),
           "FOLDING LEG\n25×25×3mm SHS\nL≈925mm",
           fs=5, ha="left")

    # ── Walkway deck ──
    ax.add_patch(Rectangle((px(0), pz(WALKWAY_H - WALKWAY_GRATE_T)),
                            px(WALKWAY_W) - px(0),
                            pz(WALKWAY_H) - pz(WALKWAY_H - WALKWAY_GRATE_T),
                            fc=C_WALKWAY, ec=C_OUT, lw=0.8, zorder=4))
    ax.text(px(WALKWAY_W / 2), pz(WALKWAY_H - WALKWAY_GRATE_T - 10),
            "WALKWAY GRATING\n25mm", fontsize=4.5, color=C_DIM,
            ha="center", va="top")

    # ── Floor line ──
    ax.plot([px(YD_LO + 20), px(YD_HI - 20)], [pz(0), pz(0)],
            color=C_OUT, lw=1.5, zorder=5)
    ax.text(px(YD_HI - 30), pz(-20), "FLOOR", fontsize=5, color=C_DIM,
            ha="right", va="top")

    # ── Shelf — folded (ghost, vertical) ──
    fold_yd_left = 0  # against wall
    fold_yd_right = SHELF_T  # 22mm protrusion
    fold_z_bottom = SHELF_H - SHELF_T  # hinge line
    fold_z_top = fold_z_bottom + SHELF_DEPTH  # 1,475mm
    ax.add_patch(Rectangle((px(fold_yd_left), pz(fold_z_bottom)),
                            px(fold_yd_right) - px(fold_yd_left),
                            pz(fold_z_top) - pz(fold_z_bottom),
                            fc=C_GHOST, ec=C_GHOST, lw=1.2, ls="--",
                            alpha=0.2, zorder=3))
    ax.add_patch(Rectangle((px(fold_yd_left), pz(fold_z_bottom)),
                            px(fold_yd_right) - px(fold_yd_left),
                            pz(fold_z_top) - pz(fold_z_bottom),
                            fc="none", ec=C_GHOST, lw=1.2, ls="--",
                            zorder=4))
    ax.text(px(fold_yd_right + 10), pz((fold_z_bottom + fold_z_top) / 2),
            "FOLDED\nPOSITION", fontsize=5, color=C_GHOST, ha="left",
            va="center", rotation=90, style="italic")

    # ── Ball catch (at top of folded shelf) ──
    catch_z = fold_z_top - 20
    ax.plot(px(fold_yd_right + 3), pz(catch_z), "D", color=C_HINGE, ms=5, zorder=9)
    leader(ax, px(fold_yd_right + 3), pz(catch_z),
           px(fold_yd_right + 60), pz(catch_z + 50),
           "BALL CATCH\n(SS, 50N)",
           fs=5, ha="left")

    # ── 90° stop tab ──
    stop_z = shelf_z_bottom - 2
    stop_yd = bracket_depth + 30
    ax.plot([px(stop_yd), px(stop_yd), px(stop_yd + 15)],
            [pz(stop_z - 20), pz(stop_z), pz(stop_z)],
            color=C_OUT, lw=1.5, zorder=8)
    leader(ax, px(stop_yd + 8), pz(stop_z - 10),
           px(stop_yd + 80), pz(stop_z - 60),
           "90° STOP TAB\n(WELDED)",
           fs=5, ha="left")

    # ── Key dimensions ──
    # Shelf depth from wall
    draw_dim_h(ax, px(0), px(SHELF_DEPTH), pz(SHELF_H + 50),
               "450 DEPTH", offset=8, fs=6)
    # Walkway width
    draw_dim_h(ax, px(0), px(WALKWAY_W), pz(30),
               "300 WALKWAY", offset=8, fs=5.5)
    # Overhang
    draw_dim_h(ax, px(WALKWAY_W), px(SHELF_DEPTH), pz(SHELF_H + 100),
               "150 OVERHANG", offset=6, fs=5.5)
    # Height above floor to work surface
    draw_dim_v(ax, px(SHELF_DEPTH + 80), pz(0), pz(SHELF_H),
               "1,025 AFF", offset=8, fs=6, right=True)
    # Height above deck
    draw_dim_v(ax, px(SHELF_DEPTH + 130), pz(WALKWAY_H), pz(SHELF_H),
               "925 ABOVE\nDECK", offset=8, fs=5.5, right=True)
    # Folded protrusion
    draw_dim_h(ax, px(0), px(SHELF_T), pz(fold_z_top + 30),
               "22", offset=5, fs=5.5)

    # ── Title block ──
    title_block(ax, "SHEET 3 OF 3",
                drawing_title="CHEMISTRY PREP SHELVES",
                subtitle="HINGE & SUPPORT DETAIL — SECTION THROUGH SHELF",
                scale_note="SCALE ~1:5",
                doc_id="TBS-001 · Chem Prep")

    out = "diagrams/shelf-sheet3.png"
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  [3/3] {out}")


# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    os.makedirs("diagrams", exist_ok=True)
    os.makedirs(SVG_DIR, exist_ok=True)
    print("Generating chemistry prep shelf diagrams...")
    sheet1()
    sheet2()
    sheet3()
    print("Done.")
