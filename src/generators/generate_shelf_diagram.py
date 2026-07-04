#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_shelf_diagram.py  —  TBS-001 Chemistry Prep Shelf (WALL-HINGED FOLD-DOWN)

rev13: the chem prep shelf is a wall-hinged FOLD-DOWN in the widened near walkway,
LEFT of the battery bank.  Mixing-only (before exposure), so it folds away and is
fully decoupled from the film-plane swing.

Sheet 1 — Plan view: deployed footprint in the widened walkway, the relocated tap,
          battery/EP context, and the navigation clearance.
Sheet 2 — Section (Yd-Z): the fold-down mechanism — deployed + stowed positions,
          piano hinge, stay, and the evap cooler sliding under.
Sheet 3 — Detail: the piano hinge (wall mount) + the stay.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_notes
from tbs_constants import (
    C_WID, C_HGT,
    WALKWAY_H, WALKWAY_GRATE_T,
    WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_X_R, WALKWAY_NEAR_WIDE_W,
    SHELF_X_L, SHELF_X_R, SHELF_W, SHELF_YD_NEAR, SHELF_YD_FAR,
    SHELF_DEPTH, SHELF_H, SHELF_T, SHELF_STOW_TOP_Z, SHELF_STAY_N,
    TAP_X, TAP_Z,
    BA_X, BA_W, BA_H_LO, BA_H_HI, BA_D,
    EP_X, EP_W, EP_H_LO, EP_H_HI,
    EVAP_STOW_X, EVAP_W, EVAP_D, EVAP_H, EVAP_STOW_Z,
    cone_left,
    C_OUT, C_DIM, C_STEEL, C_CL,
    DIAGRAMS_DIR,
)

BG        = "#FFFFFF"
C_SHELF   = "#C8B06A"    # phenolic ply — warm tan
C_HINGE   = "#606870"    # steel hinge / stays
C_WALK    = "#ECECEC"    # walkway grating fill
C_BATT    = "#9BB36A"    # battery bank
C_ELEC    = "#E0A050"    # electrical panel
C_EVAP    = "#9AB0C0"    # evap cooler
C_BLUE    = "#3070C0"    # blue supply / tap
C_CONE    = "#E9534522"  # optical cone (faint)
FONT      = {"fontfamily": "monospace"}

SHELF_CX = (SHELF_X_L + SHELF_X_R) / 2
DECK_Z   = WALKWAY_H
STAY_Z   = SHELF_H + 230   # wall stay anchor, above the hinge


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — PLAN VIEW (looking down)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():
    fig, ax = plt.subplots(figsize=(13, 7))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    X_LO, X_HI = 900, 2520
    Y_LO, Y_HI = -160, 620
    ax.set_xlim(X_LO, X_HI); ax.set_ylim(Y_LO, Y_HI)
    ax.set_aspect("equal"); ax.axis("off")

    # pinhole wall (Yd0)
    ax.plot([X_LO, X_HI], [0, 0], color=C_OUT, lw=2.0, zorder=5)
    ax.text(X_LO + 20, -70, "PINHOLE WALL (Yd=0)", fontsize=6, color=C_DIM, **FONT)

    # widened near walkway (Yd0-500)
    ax.add_patch(Rectangle((WALKWAY_NEAR_WIDE_X_L, 0),
                           WALKWAY_NEAR_WIDE_X_R - WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_W,
                           fc=C_WALK, ec=C_OUT, lw=0.7, alpha=0.5, zorder=2))
    ax.text(2150, 470, f"WIDENED NEAR WALKWAY ({WALKWAY_NEAR_WIDE_W}mm)",
            fontsize=6, color=C_DIM, ha="center", **FONT)

    # optical-cone left boundary (shelf must stay left of it)
    cone_xs = [cone_left(y) for y in (0, Y_HI)]
    ax.plot(cone_xs, [0, Y_HI], color="#CC4444", lw=1.1, ls="--", zorder=3)
    ax.text(cone_xs[1] + 25, Y_HI - 30, "OPTICAL CONE\nLEFT BOUNDARY",
            fontsize=5.5, color="#CC4444", rotation=64, ha="left", va="top", **FONT)

    # battery bank + EP (to the RIGHT of the shelf)
    ax.add_patch(Rectangle((BA_X, 0), BA_W, BA_D, fc=C_BATT, ec=C_OUT, lw=0.8, alpha=0.7, zorder=4))
    ax.text(BA_X + BA_W / 2, BA_D / 2, "BATTERY BANK", fontsize=5.5, color="#3a4a20",
            ha="center", va="center", **FONT)
    ax.add_patch(Rectangle((EP_X, 0), EP_W, 60, fc=C_ELEC, ec=C_OUT, lw=0.6, alpha=0.4, zorder=3))
    ax.text(EP_X + EP_W / 2, 75, "EP (high)", fontsize=4.5, color="#8a5a10", ha="center", **FONT)

    # evap cooler (transport stow) — slides under, ghost
    ax.add_patch(Rectangle((EVAP_STOW_X, 0), EVAP_W, EVAP_D, fc=C_EVAP, ec=C_OUT, lw=0.6,
                           ls="--", alpha=0.25, zorder=3))
    ax.text(EVAP_STOW_X + EVAP_W / 2, EVAP_D - 30, "EVAP (stow,\nslides under)",
            fontsize=4.5, color="#3a5060", ha="center", va="top", **FONT)

    # the DEPLOYED shelf (X1180-1780, Yd0-300)
    ax.add_patch(Rectangle((SHELF_X_L, SHELF_YD_NEAR), SHELF_W, SHELF_DEPTH,
                           fc=C_SHELF, ec=C_OUT, lw=1.4, zorder=6))
    ax.text(SHELF_CX, SHELF_DEPTH / 2, f"CHEM SHELF\n{SHELF_W}×{SHELF_DEPTH}mm\n(deployed)",
            fontsize=6.5, color="#5a4a18", ha="center", va="center", fontweight="bold", **FONT)
    # piano hinge along the back edge (on the wall)
    ax.plot([SHELF_X_L, SHELF_X_R], [0, 0], color=C_HINGE, lw=3.2, zorder=7)
    leader(ax, SHELF_CX, 0, SHELF_CX - 250, -110,
           "PIANO HINGE on pinhole wall (back edge)", color=C_HINGE, fs=6, ha="center", font=FONT)

    # relocated TAP-01 (left of the shelf)
    ax.add_patch(Circle((TAP_X, 12), 14, fc=C_BLUE, ec=C_OUT, lw=0.8, zorder=8))
    leader(ax, TAP_X, 12, TAP_X - 30, 180,
           "TAP-01 (relocated)\nleft of the shelf", color=C_BLUE, fs=6, ha="center", font=FONT)

    # navigation clearance behind the deployed shelf
    draw_dim_v(ax, SHELF_X_R + 60, SHELF_DEPTH, WALKWAY_NEAR_WIDE_W,
               f"{WALKWAY_NEAR_WIDE_W - SHELF_DEPTH}mm\npass (deployed)", offset=8, fs=6, right=True, font=FONT)
    draw_dim_h(ax, SHELF_X_L, SHELF_X_R, -120, f"{SHELF_W}mm", offset=6, fs=7, font=FONT)

    notes = [
        "CHEM SHELF — WALL-HINGED FOLD-DOWN (PLAN):",
        f"1. Hinged on the pinhole wall (Yd0), deploys {SHELF_DEPTH}mm into the {WALKWAY_NEAR_WIDE_W}mm walkway.",
        f"2. Left of the battery bank (X{BA_X}); ~{int(cone_left(SHELF_YD_FAR) - SHELF_X_R)}mm clear of the optical cone.",
        "3. Deployed only while mixing (full walkway clear when folded up).",
        "4. TAP-01 relocated LEFT of the shelf (battery bank is to the right).",
    ]
    draw_notes(ax, notes, X_LO + 20, Y_HI - 20, spacing=26, fs=6.5, width=820, font=FONT)
    title_block(ax, "SHEET 1 OF 3", drawing_title="CHEMISTRY PREP SHELF",
                subtitle="PLAN — FOLD-DOWN, WIDENED WALKWAY (LEFT OF BATTERIES)",
                scale_note="Axes in mm · PLAN VIEW", height=0.08)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "shelf-sheet1.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/shelf-sheet1.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — SECTION (Yd-Z): the fold-down mechanism
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    Y_LO, Y_HI = -120, 1300
    Z_LO, Z_HI = -80, 1520
    ax.set_xlim(Y_LO, Y_HI); ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal"); ax.axis("off")

    # pinhole wall (Yd0) + floor + deck
    ax.add_patch(Rectangle((-40, 0), 40, Z_HI, fc="#E8E6DD", ec=C_OUT, lw=1.0, zorder=3))
    ax.text(-20, Z_HI - 40, "PINHOLE\nWALL", fontsize=5.5, color=C_DIM, ha="center", va="top", rotation=90, **FONT)
    ax.plot([Y_LO, Y_HI], [0, 0], color=C_OUT, lw=1.2, zorder=3)
    ax.add_patch(Rectangle((0, DECK_Z - WALKWAY_GRATE_T), WALKWAY_NEAR_WIDE_W, WALKWAY_GRATE_T,
                           fc=C_WALK, ec=C_OUT, lw=0.7, alpha=0.7, zorder=3))
    ax.text(WALKWAY_NEAR_WIDE_W - 10, DECK_Z + 30, "walkway deck Z130", fontsize=5, color=C_DIM,
            ha="right", **FONT)

    # evap cooler ghost (slides under)
    ax.add_patch(Rectangle((0, EVAP_STOW_Z), EVAP_D, EVAP_H, fc=C_EVAP, ec=C_OUT, lw=0.6,
                           ls="--", alpha=0.25, zorder=2))
    ax.text(EVAP_D / 2, EVAP_STOW_Z + EVAP_H - 40, f"EVAP COOLER\n(slides under,\ntop Z{EVAP_STOW_Z + EVAP_H})",
            fontsize=5, color="#3a5060", ha="center", va="top", **FONT)

    # DEPLOYED shelf (horizontal at Z = SHELF_H)
    ax.add_patch(Rectangle((0, SHELF_H - SHELF_T), SHELF_DEPTH, SHELF_T,
                           fc=C_SHELF, ec=C_OUT, lw=1.4, zorder=6))
    ax.add_patch(Rectangle((SHELF_DEPTH - 6, SHELF_H), 6, 15, fc=C_SHELF, ec=C_OUT, lw=0.8, zorder=6))  # front lip
    ax.text(SHELF_DEPTH / 2, SHELF_H - SHELF_T - 20, "SHELF (deployed)", fontsize=6, color="#5a4a18",
            ha="center", va="top", fontweight="bold", **FONT)
    # piano hinge at the back
    ax.add_patch(Circle((0, SHELF_H), 9, fc=C_HINGE, ec=C_OUT, lw=0.8, zorder=8))
    leader(ax, 0, SHELF_H, -90, SHELF_H + 90, "PIANO HINGE", color=C_HINGE, fs=6, ha="center", font=FONT)
    # stay (wall above -> front edge)
    ax.plot([0, SHELF_DEPTH - 10], [STAY_Z, SHELF_H], color=C_HINGE, lw=2.4, zorder=7)
    ax.add_patch(Rectangle((-6, STAY_Z - 8), 12, 16, fc=C_HINGE, ec=C_OUT, lw=0.6, zorder=7))
    leader(ax, (SHELF_DEPTH - 10) / 2, (STAY_Z + SHELF_H) / 2, SHELF_DEPTH + 30, 1000,
           f"STAY (×{SHELF_STAY_N})\ncarries the load,\nfolds flat when stowed", color=C_HINGE, fs=6,
           ha="left", font=FONT)

    # STOWED shelf ghost (folded up, vertical, Z SHELF_H..STOW_TOP)
    ax.add_patch(Rectangle((0, SHELF_H), SHELF_T, SHELF_STOW_TOP_Z - SHELF_H,
                           fc=C_SHELF, ec=C_OUT, lw=1.0, ls="--", alpha=0.35, zorder=4))
    ax.text(SHELF_T + 12, SHELF_STOW_TOP_Z - 20, "SHELF (folded up\nfor transport)",
            fontsize=5.5, color="#8a7a3a", ha="left", va="top", style="italic", **FONT)

    # tap spout over the shelf
    ax.plot([12, 12], [SHELF_H + 20, SHELF_STOW_TOP_Z], color=C_BLUE, lw=2.0, zorder=5)
    ax.plot([12, 100, 100], [SHELF_STOW_TOP_Z, SHELF_STOW_TOP_Z, TAP_Z], color=C_BLUE, lw=2.0, zorder=5)
    ax.text(110, TAP_Z, "TAP-01 spout", fontsize=5.5, color=C_BLUE, ha="left", va="center", **FONT)

    # dimensions
    draw_dim_v(ax, -70, 0, SHELF_H, f"{SHELF_H}mm AFF", offset=6, fs=6, right=False, font=FONT)
    draw_dim_v(ax, 430, DECK_Z, SHELF_H, f"{SHELF_H - DECK_Z}mm\nabove deck", offset=6, fs=6, right=True, font=FONT)
    draw_dim_h(ax, 0, SHELF_DEPTH, SHELF_H - SHELF_T - 70, f"{SHELF_DEPTH}mm deep", offset=6, fs=6, font=FONT)

    notes = [
        "FOLD-DOWN MECHANISM (SECTION):",
        f"1. Piano hinge (back edge, Z{SHELF_H}) on the pinhole wall.",
        f"2. In use: folds DOWN to horizontal, held level by {SHELF_STAY_N} stays from the wall above.",
        f"3. Transport: folds UP flat against the wall (top Z{SHELF_STOW_TOP_Z}).",
        f"4. Evap cooler (top Z{EVAP_STOW_Z + EVAP_H}) slides under the shelf underside (Z1050).",
    ]
    draw_notes(ax, notes, 560, 1480, spacing=64, fs=7, width=680, font=FONT)
    title_block(ax, "SHEET 2 OF 3", drawing_title="CHEMISTRY PREP SHELF",
                subtitle="SECTION — FOLD-DOWN MECHANISM (DEPLOYED + STOWED)",
                scale_note="Axes in mm · SECTION LOOKING ALONG X", height=0.07)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "shelf-sheet2.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/shelf-sheet2.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — DETAIL: piano hinge (wall mount) + stay
# ═══════════════════════════════════════════════════════════════════════════════
def sheet3():
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(-60, 240); ax.set_ylim(SHELF_H - 80, STAY_Z + 80)
    ax.set_aspect("equal"); ax.axis("off")

    # wall
    ax.add_patch(Rectangle((-50, SHELF_H - 80), 50, (STAY_Z + 80) - (SHELF_H - 80),
                           fc="#E8E6DD", ec=C_OUT, lw=1.0, zorder=2))
    ax.text(-25, STAY_Z + 40, "PINHOLE WALL", fontsize=5.5, color=C_DIM, ha="center", rotation=90, **FONT)

    # hinge: wall leaf + knuckle + shelf leaf
    ax.add_patch(Rectangle((0, SHELF_H - 4), 8, 60, fc=C_HINGE, ec=C_OUT, lw=1.0, zorder=4))   # wall leaf (up)
    ax.add_patch(Circle((10, SHELF_H), 8, fc="#9098A0", ec=C_OUT, lw=1.0, zorder=6))            # knuckle
    ax.add_patch(Rectangle((10, SHELF_H - SHELF_T), 70, SHELF_T, fc=C_SHELF, ec=C_OUT, lw=1.2, zorder=5))  # shelf board
    leader(ax, 10, SHELF_H, 90, SHELF_H + 50, "PIANO HINGE\n(continuous, along the back edge)",
           color=C_HINGE, fs=6.5, ha="left", font=FONT)
    leader(ax, 45, SHELF_H - SHELF_T, 120, SHELF_H - SHELF_T - 60,
           f"SHELF BOARD\n18mm ply + frame ({SHELF_T}mm)", color="#5a4a18", fs=6.5, ha="left", font=FONT)

    # stay anchor + stay to the front
    ax.add_patch(Rectangle((0, STAY_Z - 10), 16, 20, fc=C_HINGE, ec=C_OUT, lw=1.0, zorder=4))
    ax.plot([8, 200], [STAY_Z, SHELF_H], color=C_HINGE, lw=3.0, zorder=5)
    ax.add_patch(Circle((200, SHELF_H), 6, fc="#9098A0", ec=C_OUT, lw=0.8, zorder=6))
    leader(ax, 8, STAY_Z, 70, STAY_Z + 40, "STAY WALL ANCHOR\n(above the hinge)", color=C_HINGE, fs=6.5,
           ha="left", font=FONT)
    leader(ax, 110, (STAY_Z + SHELF_H) / 2, 150, (STAY_Z + SHELF_H) / 2 + 60,
           "STAY (chain or folding strut)\ncarries the deployed load;\nfolds flat when shelf folds up",
           color=C_HINGE, fs=6.5, ha="left", font=FONT)

    title_block(ax, "SHEET 3 OF 3", drawing_title="CHEMISTRY PREP SHELF",
                subtitle="DETAIL — PIANO HINGE + STAY",
                scale_note="Axes in mm · DETAIL", height=0.08)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "shelf-sheet3.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/shelf-sheet3.png saved")


if __name__ == "__main__":
    print("Generating chemistry prep shelf diagrams (fold-down)...")
    sheet1(); sheet2(); sheet3()
    print("Done.")
