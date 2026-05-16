#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_shelf_diagram.py  —  TBS-001 Chemistry Prep Shelf

Ceiling-suspended shelf in the bottom-right corner (where near walkway
meets right walkway).  Hung from M10 threaded rods — same system as the
right walkway.  On the tray side of the near walkway so the walkway
stays clear for passage.

Sheet 1 — Plan View (1:15):
  Top-down view showing shelf position relative to walkways, tray,
  IBC stack, and optical cone boundary.

Sheet 2 — Section Elevation (1:10):
  Cross-section looking along X axis (at shelf center X=4,479mm).
  Shows ceiling hangers, shelf platform, walkway below, and tray.

Sheet 3 — Detail: Hanger & Frame (1:5):
  Close-up of ceiling plate, threaded rod, shelf frame connection,
  and work surface layup.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyBboxPatch
from matplotlib.lines import Line2D

from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader
from tbs_constants import (
    svg_path, SVG_DIR,
    C_LEN, C_WID, C_HGT,
    PUMP_X, PUMP_W,
    WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T,
    WALKWAY_RIGHT_X, WALKWAY_RIGHT_W,
    WALKWAY_RIGHT_HANGER_D, WALKWAY_RIGHT_HANGER_N, WALKWAY_RIGHT_HANGER_Y1,
    CONTAINER_RIB_SPACING,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR,
    PROC_TRAY_RIM,
    IBC_COL_X, IBC_W, IBC_D, IBC_H_600, IBC_H_STK,
    BLUE_IBC_Y, IBC_FAR_Y,
    SHELF_X_L, SHELF_X_R, SHELF_W, SHELF_YD_NEAR, SHELF_YD_FAR,
    SHELF_DEPTH, SHELF_H, SHELF_T, SHELF_HANGER_D, SHELF_HANGER_N,
    ZONE_R_START, cone_right,
    C_OUT, C_DIM, C_STEEL, C_ALUM, C_CL,
)

# ── Local palette ────────────────────────────────────────────────────────────
BG       = "#FFFFFF"
C_SHELF  = "#C8B06A"    # phenolic ply — warm tan
C_FRAME  = C_STEEL      # steel frame
C_HANGER = "#606870"    # threaded rod / hardware
C_TRAY   = "#D0D8E0"    # processing tray
C_WALKWAY = "#E8E8E8"   # walkway grating fill
C_CONE   = "#FFE0E0"    # optical cone zone (faint red)
C_IBC    = "#B0D0F0"    # IBC outline
C_ZONE   = "#E8F4E8"    # shadow-free zone fill

# ── Derived constants ────────────────────────────────────────────────────────
SHELF_CX = (SHELF_X_L + SHELF_X_R) / 2   # shelf center X = 4,029mm
SHELF_CY = (SHELF_YD_NEAR + SHELF_YD_FAR) / 2  # shelf center Yd = 600mm
HANGER_ROD_L = C_HGT - SHELF_H            # rod length: 2388 - 1025 = 1363mm
# Hanger positions: 4 corners, inset 30mm from shelf edges
HANGER_INSET = 30
HANGER_POSITIONS = [
    (SHELF_X_L + HANGER_INSET, SHELF_YD_NEAR + HANGER_INSET),
    (SHELF_X_R - HANGER_INSET, SHELF_YD_NEAR + HANGER_INSET),
    (SHELF_X_L + HANGER_INSET, SHELF_YD_FAR - HANGER_INSET),
    (SHELF_X_R - HANGER_INSET, SHELF_YD_FAR - HANGER_INSET),
]


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — PLAN VIEW
# ═══════════════════════════════════════════════════════════════════════════════

def sheet1():
    """Plan view showing shelf position relative to walkways and optical cone."""
    # View: looking down.  X horizontal (cargo door left, far end right).
    # Yd vertical (pinhole wall at bottom, far wall at top).
    # Near walkway = horizontal band at bottom, right walkway = vertical
    # band on right, shelf in the L-shaped corner between them.
    # Tight crop centered on shelf with surrounding context.
    X_LO, X_HI = 3400, 5100
    YD_LO, YD_HI = -120, 1000
    SC = 8.0

    def px(x): return (x - X_LO) / SC      # X → horizontal
    def py(yd): return (yd - YD_LO) / SC    # Yd → vertical (bottom=wall)

    fig, ax = plt.subplots(figsize=(18, 12), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(px(X_LO), px(X_HI))
    ax.set_ylim(py(YD_LO), py(YD_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Optical cone right boundary (at various Yd, as a shaded zone) ──
    cone_yds = np.linspace(0, YD_HI, 50)
    cone_xs = [cone_right(yd) for yd in cone_yds]
    # Shade the cone zone (everything left of the boundary)
    cone_poly_x = [px(max(x, X_LO)) for x in cone_xs] + [px(X_LO), px(X_LO)]
    cone_poly_y = [py(yd) for yd in cone_yds] + [py(YD_HI), py(0)]
    ax.fill(cone_poly_x, cone_poly_y, fc=C_CONE, alpha=0.15, zorder=1)
    # Cone boundary line (only draw where it's in view)
    vis = [(x, yd) for x, yd in zip(cone_xs, cone_yds) if x >= X_LO]
    if vis:
        ax.plot([px(x) for x, _ in vis], [py(yd) for _, yd in vis],
                color="#CC4444", lw=1.2, ls="--", zorder=3)
        mid_idx = len(vis) // 2
        mx, myd = vis[mid_idx]
        ax.text(px(mx + 40), py(myd), "OPTICAL CONE\nRIGHT BOUNDARY",
                fontsize=6, color="#CC4444", ha="left", va="center", rotation=25)

    # ── Right end zone (shadow-free, green tint) ──
    if ZONE_R_START < X_HI:
        ax.add_patch(Rectangle((px(ZONE_R_START), py(YD_LO + 10)),
                                px(X_HI) - px(ZONE_R_START),
                                py(YD_HI - 10) - py(YD_LO + 10),
                                fc=C_ZONE, ec="none", alpha=0.25, zorder=1))
        ax.text(px(ZONE_R_START + 20), py(YD_HI - 40),
                "RIGHT END ZONE (SHADOW-FREE)",
                fontsize=5.5, color="#408040", ha="left", va="top")
        ax.plot([px(ZONE_R_START), px(ZONE_R_START)],
                [py(YD_LO + 10), py(YD_HI - 10)],
                color="#408040", lw=0.8, ls=(0, (6, 3)), zorder=3)

    # ── Container walls ──
    # Pinhole wall (Yd=0) — bottom
    ax.plot([px(X_LO), px(X_HI)], [py(0), py(0)],
            color=C_OUT, lw=2.0, zorder=5)
    ax.text(px((X_LO + X_HI) / 2), py(-60), "PINHOLE WALL (Yd=0)",
            fontsize=6, color=C_DIM, ha="center", va="top")

    # ── Near walkway (Yd=0 to 300) — horizontal band at bottom ──
    ax.add_patch(Rectangle((px(X_LO), py(0)),
                            px(X_HI) - px(X_LO),
                            py(WALKWAY_W) - py(0),
                            fc=C_WALKWAY, ec=C_OUT, lw=0.6, alpha=0.4, zorder=2))
    ax.text(px(3700), py(WALKWAY_W / 2), "NEAR WALKWAY  300mm",
            fontsize=6, color=C_DIM, ha="center", va="center")

    # ── Right walkway (X=4329 to 4629) — vertical band on right ──
    rw_yd_top = min(C_WID, YD_HI)
    ax.add_patch(Rectangle((px(WALKWAY_RIGHT_X), py(0)),
                            px(WALKWAY_RIGHT_X + WALKWAY_RIGHT_W) - px(WALKWAY_RIGHT_X),
                            py(rw_yd_top) - py(0),
                            fc=C_WALKWAY, ec=C_OUT, lw=0.6, alpha=0.4, zorder=2))
    ax.text(px(WALKWAY_RIGHT_X + WALKWAY_RIGHT_W / 2), py(min(800, rw_yd_top - 50)),
            "RIGHT\nWALKWAY\n(CEILING-\nHUNG)",
            fontsize=6, color=C_DIM, ha="center", va="center", rotation=90)

    # Right walkway hanger positions (filled dots — same as shelf hangers)
    rw_hanger_yds = np.array([WALKWAY_RIGHT_HANGER_Y1] + list(
        np.arange(CONTAINER_RIB_SPACING / 2 + CONTAINER_RIB_SPACING,
                   C_WID, CONTAINER_RIB_SPACING)))[:WALKWAY_RIGHT_HANGER_N]
    rw_rod_x_inner = WALKWAY_RIGHT_X + 15
    rw_rod_x_outer = WALKWAY_RIGHT_X + WALKWAY_RIGHT_W - 15
    for hy in rw_hanger_yds:
        if hy > YD_HI - 20:
            continue  # skip if outside view
        for rx in [rw_rod_x_inner, rw_rod_x_outer]:
            ax.plot(px(rx), py(hy), "o", color=C_HANGER, ms=7, zorder=6)
    # Label first visible hanger pair
    vis_hangers = [hy for hy in rw_hanger_yds if hy < YD_HI - 20]
    if vis_hangers:
        leader(ax, px(rw_rod_x_outer), py(vis_hangers[0]),
               px(rw_rod_x_outer + 80), py(vis_hangers[0] - 50),
               f"M{WALKWAY_RIGHT_HANGER_D} HANGER\nPAIRS (×{WALKWAY_RIGHT_HANGER_N})\n1st @ {WALKWAY_RIGHT_HANGER_Y1}mm",
               fs=5.5, ha="left")

    # ── Processing tray outline ──
    tray_x_lo = max(PROC_TRAY_X_L, X_LO)
    tray_x_hi = min(PROC_TRAY_X_R, X_HI)
    tray_yd_lo = PROC_TRAY_YD_NEAR
    tray_yd_hi = min(PROC_TRAY_YD_FAR, YD_HI)
    ax.add_patch(Rectangle((px(tray_x_lo), py(tray_yd_lo)),
                            px(tray_x_hi) - px(tray_x_lo),
                            py(tray_yd_hi) - py(tray_yd_lo),
                            fc="none", ec=C_TRAY, lw=0.8, ls=":", zorder=2))
    ax.text(px(3900), py(700), "PROCESSING TRAY\n(BELOW, H=0–50mm)",
            fontsize=5.5, color=C_TRAY, ha="center", va="center")

    # ── IBC stack (right end zone — show near column only, clipped) ──
    ibc_x_lo = max(IBC_COL_X, X_LO)
    ibc_x_hi = min(IBC_COL_X + IBC_W, X_HI)
    if ibc_x_lo < X_HI and BLUE_IBC_Y < YD_HI:
        ibc_yd_hi = min(BLUE_IBC_Y + IBC_D, YD_HI)
        ax.add_patch(Rectangle((px(ibc_x_lo), py(BLUE_IBC_Y)),
                                px(ibc_x_hi) - px(ibc_x_lo),
                                py(ibc_yd_hi) - py(BLUE_IBC_Y),
                                fc=C_IBC, ec=C_OUT, lw=0.8, alpha=0.3, zorder=2))
        ax.text(px((ibc_x_lo + ibc_x_hi) / 2), py((BLUE_IBC_Y + ibc_yd_hi) / 2),
                "IBC", fontsize=6, color=C_DIM, ha="center", va="center")

    # ── SHELF (main feature — bold) ──
    ax.add_patch(Rectangle((px(SHELF_X_L), py(SHELF_YD_NEAR)),
                            px(SHELF_X_R) - px(SHELF_X_L),
                            py(SHELF_YD_FAR) - py(SHELF_YD_NEAR),
                            fc=C_SHELF, ec=C_OUT, lw=2.5, zorder=8))
    ax.text(px(SHELF_CX), py(SHELF_CY),
            f"CHEMISTRY PREP SHELF\n{SHELF_W}×{SHELF_DEPTH}mm  H={SHELF_H}mm\n(CEILING-HUNG)",
            fontsize=7, color=C_OUT, ha="center", va="center", fontweight="bold")

    # Hanger positions (4 dots)
    for hx, hy in HANGER_POSITIONS:
        ax.plot(px(hx), py(hy), "o", color=C_HANGER, ms=7, zorder=10)
    leader(ax, px(HANGER_POSITIONS[2][0]), py(HANGER_POSITIONS[2][1]),
           px(HANGER_POSITIONS[2][0] - 80), py(HANGER_POSITIONS[2][1] + 60),
           f"M{SHELF_HANGER_D} HANGER\nROD (×4)", fs=6, ha="right")

    # ── Operator position annotation ──
    op_yd = 150  # standing on near walkway
    op_x = SHELF_CX  # at shelf center X
    ax.plot(px(op_x), py(op_yd), "x", color="#2060A0", ms=12, mew=2, zorder=9)
    ax.text(px(op_x - 60), py(op_yd), "OPERATOR\nSTANDS HERE",
            fontsize=6, color="#2060A0", ha="right", va="center")

    # ── Dimensions ──
    # Shelf width (X direction) — horizontal
    draw_dim_h(ax, px(SHELF_X_L), px(SHELF_X_R), py(SHELF_YD_FAR + 50),
               f"{SHELF_W}mm", offset=5, fs=7)
    # Shelf depth (Yd direction) — vertical
    draw_dim_v(ax, px(SHELF_X_L - 50), py(SHELF_YD_NEAR), py(SHELF_YD_FAR),
               f"{SHELF_DEPTH}mm", offset=5, fs=7)
    # Distance from pinhole wall (Yd direction)
    draw_dim_v(ax, px(SHELF_X_R + 50), py(0), py(SHELF_YD_NEAR),
               f"{SHELF_YD_NEAR}mm FROM WALL", offset=5, fs=6, right=True)
    # Near walkway width
    draw_dim_v(ax, px(X_LO + 80), py(0), py(WALKWAY_W),
               "300mm\nWALKWAY", offset=5, fs=6)
    # Right walkway width
    draw_dim_h(ax, px(WALKWAY_RIGHT_X), px(WALKWAY_RIGHT_X + WALKWAY_RIGHT_W),
               py(-80), f"{WALKWAY_RIGHT_W}mm", offset=5, fs=6)

    # ── Title block ──
    title_block(ax, "SHEET 1 OF 3",
                drawing_title="CHEMISTRY PREP SHELF",
                subtitle="PLAN VIEW — CEILING-SUSPENDED, RIGHT CORNER",
                scale_note="SCALE ~1:12",
                doc_id="TBS-001 · Chem Prep")

    out = "diagrams/shelf-sheet1.png"
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  [1/3] {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — SECTION ELEVATION
# ═══════════════════════════════════════════════════════════════════════════════

def sheet2():
    """Cross-section looking along X axis showing hangers and shelf."""
    # View: looking along X (toward cargo door). Yd horizontal, Z vertical.
    YD_LO, YD_HI = -100, 1100
    Z_LO, Z_HI = -50, 2500

    def px(yd): return (yd - YD_LO) / 10.0
    def pz(z): return (z - Z_LO) / 10.0

    fig, ax = plt.subplots(figsize=(16, 18), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(px(YD_LO), px(YD_HI))
    ax.set_ylim(pz(Z_LO), pz(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container outline (section) ──
    # Floor
    ax.plot([px(YD_LO + 20), px(YD_HI - 20)], [pz(0), pz(0)],
            color=C_OUT, lw=2.0, zorder=5)
    # Ceiling
    ax.plot([px(YD_LO + 20), px(YD_HI - 20)], [pz(C_HGT), pz(C_HGT)],
            color=C_OUT, lw=2.0, zorder=5)
    # Pinhole wall (left edge, Yd=0)
    ax.plot([px(0), px(0)], [pz(0), pz(C_HGT)],
            color=C_OUT, lw=2.0, zorder=5)
    ax.text(px(-40), pz(C_HGT / 2), "PINHOLE\nWALL",
            fontsize=5, color=C_DIM, ha="right", va="center", rotation=90)

    # ── Processing tray (at floor level) ──
    tray_yd_l = PROC_TRAY_YD_NEAR  # 80mm
    tray_yd_r = min(PROC_TRAY_YD_FAR, YD_HI - 50)
    ax.add_patch(Rectangle((px(tray_yd_l), pz(0)),
                            px(tray_yd_r) - px(tray_yd_l),
                            pz(PROC_TRAY_RIM) - pz(0),
                            fc=C_TRAY, ec=C_OUT, lw=0.8, alpha=0.5, zorder=3))
    ax.text(px((tray_yd_l + 400) / 2 + 100), pz(PROC_TRAY_RIM + 10),
            "PROCESSING TRAY RIM (50mm)", fontsize=5, color=C_TRAY,
            ha="center", va="bottom")

    # ── Near walkway (Yd=0–300, deck at H=100) ──
    # Grating
    ax.add_patch(Rectangle((px(0), pz(WALKWAY_H - WALKWAY_GRATE_T)),
                            px(WALKWAY_W) - px(0),
                            pz(WALKWAY_H) - pz(WALKWAY_H - WALKWAY_GRATE_T),
                            fc=C_WALKWAY, ec=C_OUT, lw=1.0, zorder=4))
    ax.text(px(WALKWAY_W / 2), pz(WALKWAY_H + 15), "NEAR WALKWAY\nDECK H=100",
            fontsize=5, color=C_DIM, ha="center", va="bottom")

    # ── Ceiling hanger rods (4, but in this section view we see 2 — near and far) ──
    nut_h_s2 = 8   # nut height in mm (visual, at 1:10 scale)
    washer_w_s2 = 20  # washer width in mm
    nut_w_s2 = 14     # nut width in mm
    shelf_z_top_s2 = SHELF_H
    shelf_z_bot_s2 = SHELF_H - SHELF_T
    for yd in [SHELF_YD_NEAR + HANGER_INSET, SHELF_YD_FAR - HANGER_INSET]:
        # Rod from ceiling down past shelf bottom (extends to lower nut)
        ax.plot([px(yd), px(yd)], [pz(C_HGT), pz(shelf_z_bot_s2 - nut_h_s2 - 4)],
                color=C_HANGER, lw=2.0, zorder=6)
        # Ceiling plate
        plate_w = 60
        ax.add_patch(Rectangle((px(yd - plate_w / 2), pz(C_HGT - 6)),
                                px(yd + plate_w / 2) - px(yd - plate_w / 2),
                                pz(C_HGT) - pz(C_HGT - 6),
                                fc=C_FRAME, ec=C_OUT, lw=0.8, zorder=7))
        # Top lock nut (above shelf surface)
        ax.add_patch(Rectangle((px(yd - nut_w_s2 / 2), pz(shelf_z_top_s2)),
                                px(yd + nut_w_s2 / 2) - px(yd - nut_w_s2 / 2),
                                pz(shelf_z_top_s2 + nut_h_s2) - pz(shelf_z_top_s2),
                                fc=C_HANGER, ec=C_OUT, lw=0.6, zorder=9))
        # Bottom nut (below shelf frame)
        ax.add_patch(Rectangle((px(yd - nut_w_s2 / 2), pz(shelf_z_bot_s2 - nut_h_s2)),
                                px(yd + nut_w_s2 / 2) - px(yd - nut_w_s2 / 2),
                                pz(shelf_z_bot_s2) - pz(shelf_z_bot_s2 - nut_h_s2),
                                fc=C_HANGER, ec=C_OUT, lw=0.6, zorder=9))
        # Bottom washer
        ax.add_patch(Rectangle((px(yd - washer_w_s2 / 2), pz(shelf_z_bot_s2 - nut_h_s2 - 3)),
                                px(yd + washer_w_s2 / 2) - px(yd - washer_w_s2 / 2),
                                pz(shelf_z_bot_s2 - nut_h_s2) - pz(shelf_z_bot_s2 - nut_h_s2 - 3),
                                fc=C_HANGER, ec=C_OUT, lw=0.5, zorder=9))

    # ── Shelf platform ──
    shelf_z_top = SHELF_H
    shelf_z_bot = SHELF_H - SHELF_T
    ax.add_patch(Rectangle((px(SHELF_YD_NEAR), pz(shelf_z_bot)),
                            px(SHELF_YD_FAR) - px(SHELF_YD_NEAR),
                            pz(shelf_z_top) - pz(shelf_z_bot),
                            fc=C_SHELF, ec=C_OUT, lw=1.5, zorder=7))
    # Frame edges (SHS perimeter visible in section)
    frame_t = 4
    ax.add_patch(Rectangle((px(SHELF_YD_NEAR), pz(shelf_z_bot)),
                            px(SHELF_YD_NEAR + 25) - px(SHELF_YD_NEAR),
                            pz(shelf_z_top) - pz(shelf_z_bot),
                            fc=C_FRAME, ec=C_OUT, lw=0.6, zorder=8))
    ax.add_patch(Rectangle((px(SHELF_YD_FAR - 25), pz(shelf_z_bot)),
                            px(SHELF_YD_FAR) - px(SHELF_YD_FAR - 25),
                            pz(shelf_z_top) - pz(shelf_z_bot),
                            fc=C_FRAME, ec=C_OUT, lw=0.6, zorder=8))

    # ── Operator silhouette (simple rectangle) ──
    op_yd = 150  # center of near walkway
    op_w = 100   # shoulder half-width
    op_h_bottom = WALKWAY_H  # feet on deck
    op_h_top = WALKWAY_H + 1700  # ~1700mm tall
    ax.add_patch(Rectangle((px(op_yd - op_w / 2), pz(op_h_bottom)),
                            px(op_yd + op_w / 2) - px(op_yd - op_w / 2),
                            pz(op_h_top) - pz(op_h_bottom),
                            fc="#2060A0", ec="none", alpha=0.12, zorder=3))
    ax.text(px(op_yd), pz(op_h_top + 20), "OPERATOR",
            fontsize=5, color="#2060A0", ha="center", va="bottom")

    # ── Dimensions ──
    # Shelf height above floor
    draw_dim_v(ax, px(SHELF_YD_FAR + 80), pz(0), pz(SHELF_H),
               f"{SHELF_H}mm AFF", offset=5, fs=6, right=True)
    # Shelf height above walkway deck
    draw_dim_v(ax, px(SHELF_YD_NEAR - 50), pz(WALKWAY_H), pz(SHELF_H),
               f"{SHELF_H - WALKWAY_H}mm\nABOVE DECK", offset=5, fs=5.5)
    # Hanger rod length
    draw_dim_v(ax, px(SHELF_YD_FAR + 140), pz(SHELF_H), pz(C_HGT),
               f"{int(HANGER_ROD_L)}mm\nROD", offset=5, fs=5.5, right=True)
    # Shelf depth (Yd)
    draw_dim_h(ax, px(SHELF_YD_NEAR), px(SHELF_YD_FAR), pz(shelf_z_bot - 50),
               f"{SHELF_DEPTH}mm DEPTH", offset=5, fs=6)
    # Walkway width
    draw_dim_h(ax, px(0), px(WALKWAY_W), pz(-30),
               "300mm WALKWAY", offset=5, fs=5.5)
    # Gap between walkway edge and shelf
    draw_dim_h(ax, px(WALKWAY_W), px(SHELF_YD_NEAR), pz(SHELF_H + 40),
               "0mm (FLUSH)", offset=5, fs=5)
    # Shelf thickness
    draw_dim_v(ax, px(SHELF_YD_NEAR - 20), pz(shelf_z_bot), pz(shelf_z_top),
               "22mm", offset=5, fs=5, right=True)
    # Container height
    draw_dim_v(ax, px(YD_HI - 50), pz(0), pz(C_HGT),
               f"{C_HGT}mm", offset=5, fs=5.5, right=True)

    # ── Leader callouts ──
    leader(ax, px(SHELF_CY), pz(shelf_z_top + 5),
           px(SHELF_CY * 0.8), pz(shelf_z_top + 100),
           "18mm PHENOLIC PLY\nON 25×25×3mm SHS FRAME",
           fs=5.5, ha="left")
    leader(ax, px(SHELF_YD_NEAR + HANGER_INSET), pz(C_HGT - 3),
           px(SHELF_YD_NEAR + HANGER_INSET + 100), pz(C_HGT + 60),
           f"CEILING PLATE\n100×60×6mm",
           fs=5, ha="left")
    leader(ax, px(SHELF_YD_FAR - HANGER_INSET), pz((SHELF_H + C_HGT) / 2),
           px(SHELF_YD_FAR - HANGER_INSET + 50), pz((SHELF_H + C_HGT) / 2 + 50),
           f"M{SHELF_HANGER_D} THREADED\nROD HANGER",
           fs=5, ha="left")

    # ── Section cut label ──
    ax.text(px(YD_HI - 50), pz(Z_HI - 50),
            f"SECTION AT X={int(SHELF_CX)}mm\nLOOKING TOWARD CARGO DOOR",
            fontsize=6, color=C_DIM, ha="right", va="top")

    # ── Title block ──
    title_block(ax, "SHEET 2 OF 3",
                drawing_title="CHEMISTRY PREP SHELF",
                subtitle="SECTION ELEVATION — CEILING-HUNG DETAIL",
                scale_note="SCALE ~1:10",
                doc_id="TBS-001 · Chem Prep")

    out = "diagrams/shelf-sheet2.png"
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  [2/3] {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — HANGER & FRAME DETAIL
# ═══════════════════════════════════════════════════════════════════════════════

def sheet3():
    """Detail of ceiling hanger connection and shelf frame cross-section."""
    # View: close-up cross-section at one hanger corner. Yd horizontal, Z vertical.
    # Scale 1:5
    YD_LO, YD_HI = -50, 250
    Z_LO, Z_HI = 900, 2450

    def px(yd): return (yd - YD_LO) / 5.0
    def pz(z): return (z - Z_LO) / 5.0

    fig, ax = plt.subplots(figsize=(14, 18), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(px(YD_LO), px(YD_HI))
    ax.set_ylim(pz(Z_LO), pz(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # Reference hanger at Yd=30 (HANGER_INSET from shelf near edge)
    rod_yd = HANGER_INSET  # 30mm from shelf edge (Yd=0 in this detail = shelf near edge)

    # ── Ceiling (top of view) ──
    ax.plot([px(YD_LO + 10), px(YD_HI - 10)], [pz(C_HGT), pz(C_HGT)],
            color=C_OUT, lw=2.5, zorder=5)
    ax.text(px(YD_HI / 2), pz(C_HGT + 20), "CONTAINER CEILING (CORRUGATED STEEL)",
            fontsize=6, color=C_DIM, ha="center", va="bottom")

    # ── Ceiling corrugation rib (simplified) ──
    rib_depth = 45  # rib protrusion below ceiling
    rib_w = 60
    ax.add_patch(Rectangle((px(rod_yd - rib_w / 2), pz(C_HGT - rib_depth)),
                            px(rod_yd + rib_w / 2) - px(rod_yd - rib_w / 2),
                            pz(C_HGT) - pz(C_HGT - rib_depth),
                            fc="#D0D0D0", ec=C_OUT, lw=1.0, zorder=4))

    # ── Ceiling plate (100×60×6mm, bolted to rib) ──
    plate_w = 100
    plate_t = 6
    plate_z_top = C_HGT - rib_depth
    plate_z_bot = plate_z_top - plate_t
    ax.add_patch(Rectangle((px(rod_yd - plate_w / 2), pz(plate_z_bot)),
                            px(rod_yd + plate_w / 2) - px(rod_yd - plate_w / 2),
                            pz(plate_z_top) - pz(plate_z_bot),
                            fc=C_FRAME, ec=C_OUT, lw=1.2, zorder=6))
    # Through-bolts into rib
    for bx in [rod_yd - 30, rod_yd + 30]:
        ax.plot([px(bx), px(bx)], [pz(plate_z_bot), pz(C_HGT)],
                color=C_OUT, lw=1.0, zorder=7)
        ax.plot(px(bx), pz(plate_z_bot), "v", color=C_OUT, ms=3, zorder=8)

    leader(ax, px(rod_yd + plate_w / 2), pz(plate_z_bot + plate_t / 2),
           px(rod_yd + plate_w / 2 + 40), pz(plate_z_bot - 30),
           "CEILING PLATE\n100×60×6mm STEEL\n2× M10 BOLTS TO RIB",
           fs=5.5, ha="left")

    # ── Threaded rod (M10, from ceiling plate down to shelf) ──
    rod_z_top = plate_z_bot
    rod_z_bot = SHELF_H
    ax.plot([px(rod_yd), px(rod_yd)], [pz(rod_z_bot), pz(rod_z_top)],
            color=C_HANGER, lw=2.5, zorder=6)

    # Rod passes through plate — nut + washer on top
    nut_h = 10
    washer_t = 3
    ax.add_patch(Rectangle((px(rod_yd - 8), pz(rod_z_top - nut_h)),
                            px(rod_yd + 8) - px(rod_yd - 8),
                            pz(rod_z_top) - pz(rod_z_top - nut_h),
                            fc=C_HANGER, ec=C_OUT, lw=0.8, zorder=7))

    leader(ax, px(rod_yd - 3), pz((rod_z_top + rod_z_bot) / 2),
           px(rod_yd - 60), pz((rod_z_top + rod_z_bot) / 2),
           f"M{SHELF_HANGER_D} THREADED ROD\nL={int(HANGER_ROD_L)}mm\n(ZINC-PLATED)",
           fs=5.5, ha="right")

    # ── Shelf frame (at bottom of rod) ──
    shelf_z_top = SHELF_H
    shelf_z_bot = SHELF_H - SHELF_T
    frame_size = 25  # 25×25×3mm SHS
    frame_t = 3

    # Full shelf cross-section (zoomed)
    # Frame SHS at shelf edge (perimeter)
    ax.add_patch(Rectangle((px(0), pz(shelf_z_bot)),
                            px(frame_size) - px(0),
                            pz(shelf_z_top) - pz(shelf_z_bot),
                            fc=C_FRAME, ec=C_OUT, lw=1.2, zorder=7))
    # SHS hollow interior
    ax.add_patch(Rectangle((px(frame_t), pz(shelf_z_bot + frame_t)),
                            px(frame_size - frame_t) - px(frame_t),
                            pz(shelf_z_top - frame_t) - pz(shelf_z_bot + frame_t),
                            fc=BG, ec=C_OUT, lw=0.5, zorder=8))

    # Ply surface (on top of frame)
    ply_t = 18
    ax.add_patch(Rectangle((px(0), pz(shelf_z_top - ply_t)),
                            px(200) - px(0),
                            pz(shelf_z_top) - pz(shelf_z_top - ply_t),
                            fc=C_SHELF, ec=C_OUT, lw=0.8, zorder=7))
    # Frame bottom rail
    ax.add_patch(Rectangle((px(0), pz(shelf_z_bot)),
                            px(200) - px(0),
                            pz(shelf_z_bot + frame_t) - pz(shelf_z_bot),
                            fc=C_FRAME, ec=C_OUT, lw=0.6, zorder=7))

    # Rod connection to frame: nut + washer below frame
    ax.add_patch(Rectangle((px(rod_yd - 8), pz(shelf_z_bot - nut_h)),
                            px(rod_yd + 8) - px(rod_yd - 8),
                            pz(shelf_z_bot) - pz(shelf_z_bot - nut_h),
                            fc=C_HANGER, ec=C_OUT, lw=0.8, zorder=8))
    # Washer
    ax.add_patch(Rectangle((px(rod_yd - 12), pz(shelf_z_bot - nut_h - washer_t)),
                            px(rod_yd + 12) - px(rod_yd - 12),
                            pz(shelf_z_bot - nut_h) - pz(shelf_z_bot - nut_h - washer_t),
                            fc=C_HANGER, ec=C_OUT, lw=0.5, zorder=8))
    # Top nut (locks position)
    ax.add_patch(Rectangle((px(rod_yd - 8), pz(shelf_z_top)),
                            px(rod_yd + 8) - px(rod_yd - 8),
                            pz(shelf_z_top + nut_h) - pz(shelf_z_top),
                            fc=C_HANGER, ec=C_OUT, lw=0.8, zorder=8))

    leader(ax, px(rod_yd + 10), pz(shelf_z_bot - nut_h / 2),
           px(rod_yd + 70), pz(shelf_z_bot - 50),
           "M10 NUT + WASHER\n(DOUBLE-NUTTED\nFOR LEVEL ADJ.)",
           fs=5, ha="left")

    # ── Shelf surface label ──
    leader(ax, px(100), pz(shelf_z_top - 5),
           px(150), pz(shelf_z_top + 80),
           "18mm PHENOLIC PLY\n(CHEMICAL RESISTANT)\nON 25×25×3mm SHS",
           fs=5.5, ha="left")

    # ── Lip / edge trim ──
    lip_h = 15
    ax.add_patch(Rectangle((px(-2), pz(shelf_z_top)),
                            px(3) - px(-2),
                            pz(shelf_z_top + lip_h) - pz(shelf_z_top),
                            fc=C_FRAME, ec=C_OUT, lw=0.8, zorder=8))
    leader(ax, px(0), pz(shelf_z_top + lip_h),
           px(-30), pz(shelf_z_top + lip_h + 40),
           "15mm RAISED LIP\n(SPILL GUARD)\nAL ANGLE 15×15×2",
           fs=5, ha="right")

    # ── Key dimensions ──
    # Shelf thickness
    draw_dim_v(ax, px(-30), pz(shelf_z_bot), pz(shelf_z_top),
               "22mm", offset=5, fs=6)
    # Ceiling to shelf (rod length)
    draw_dim_v(ax, px(YD_HI - 30), pz(shelf_z_top), pz(C_HGT),
               f"{int(HANGER_ROD_L)}mm", offset=10, fs=6, right=True)
    # Ply thickness
    draw_dim_v(ax, px(210), pz(shelf_z_top - ply_t), pz(shelf_z_top),
               "18mm PLY", offset=5, fs=5, right=True)
    # Frame height
    draw_dim_v(ax, px(210), pz(shelf_z_bot), pz(shelf_z_bot + frame_size),
               "25mm SHS", offset=5, fs=5, right=True)

    # ── Assembly note ──
    ax.text(px(YD_HI / 2), pz(Z_LO + 30),
            "NOTE: Double-nut lock on each rod allows ±10mm\n"
            "height adjustment for leveling. Use spirit level\n"
            "across all 4 rods during installation.",
            fontsize=5.5, color=C_DIM, ha="center", va="bottom",
            fontfamily="monospace",
            bbox=dict(fc="#F8F8F0", ec=C_DIM, lw=0.5, pad=5))

    # ── Title block ──
    title_block(ax, "SHEET 3 OF 3",
                drawing_title="CHEMISTRY PREP SHELF",
                subtitle="HANGER & FRAME DETAIL",
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
