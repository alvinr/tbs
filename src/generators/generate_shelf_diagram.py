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
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_notes
from tbs_constants import WALKWAY_H, WALKWAY_GRATE_T, WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_X_R, WALKWAY_NEAR_WIDE_W, SHELF_X_L, SHELF_X_R, SHELF_W, SHELF_YD_NEAR, SHELF_YD_FAR, SHELF_DEPTH, SHELF_H, SHELF_T, SHELF_STOW_TOP_Z, SHELF_STAY_N, TAP_X, TAP_Z, BA_X, BA_W, BA_D, EP_X, EP_W, EVAP_STOW_X, EVAP_W, EVAP_D, EVAP_H, EVAP_STOW_Z, cone_left, C_OUT, C_DIM, DIAGRAMS_DIR
from tbs_constants import DIAGRAM_DPI

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
    # Y_HI raised so the notes block (anchored at Y_HI-20) lifts clear of the diagram (walkway box
    # tops at y=500) instead of hanging down over it.
    Y_LO, Y_HI = -160, 800
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

    # optical-cone left boundary (shelf must stay left of it) — capped below the notes band
    cone_top = 600
    cone_xs = [cone_left(y) for y in (0, cone_top)]
    ax.plot(cone_xs, [0, cone_top], color="#CC4444", lw=1.1, ls="--", zorder=3)
    ax.text(cone_xs[1] + 25, cone_top - 30, "OPTICAL CONE\nLEFT BOUNDARY",
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
    title_block(ax, "SHEET 1 OF 5", drawing_title="CHEMISTRY PREP SHELF",
                subtitle="PLAN — FOLD-DOWN, WIDENED WALKWAY (LEFT OF BATTERIES)",
                scale_note="Axes in mm · PLAN VIEW", height=0.08)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "shelf-sheet1.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
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
        f"2. In use: folds DOWN to horizontal, held level by {SHELF_STAY_N} SS chain stays from the wall above.",
        f"3. Transport: folds UP flat against the wall (top Z{SHELF_STOW_TOP_Z}).",
        f"4. Evap cooler (top Z{EVAP_STOW_Z + EVAP_H}) slides under the shelf underside (Z1050).",
    ]
    draw_notes(ax, notes, 560, 1480, spacing=64, fs=7, width=680, font=FONT)
    title_block(ax, "SHEET 2 OF 5", drawing_title="CHEMISTRY PREP SHELF",
                subtitle="SECTION — FOLD-DOWN MECHANISM (DEPLOYED + STOWED)",
                scale_note="Axes in mm · SECTION LOOKING ALONG X", height=0.07)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "shelf-sheet2.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/shelf-sheet2.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — DETAIL: piano hinge (wall mount) + stay
# ═══════════════════════════════════════════════════════════════════════════════
def sheet3():
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(-60, SHELF_DEPTH + 40); ax.set_ylim(SHELF_H - 80, STAY_Z + 80)
    ax.set_aspect("equal"); ax.axis("off")

    # wall
    ax.add_patch(Rectangle((-50, SHELF_H - 80), 50, (STAY_Z + 80) - (SHELF_H - 80),
                           fc="#E8E6DD", ec=C_OUT, lw=1.0, zorder=2))
    ax.text(-25, STAY_Z + 40, "PINHOLE WALL", fontsize=5.5, color=C_DIM, ha="center", rotation=90, **FONT)

    # welded 8mm steel backing plates on the wall face (behind the hinge cleat + each stay anchor)
    for (bz, bh) in [(SHELF_H - 8, 68), (STAY_Z - 14, 28)]:
        ax.add_patch(Rectangle((-6, bz), 8, bh, fc="white", ec=C_OUT, lw=1.0, hatch="///", zorder=3))
    leader(ax, -6, SHELF_H + 30, -34, SHELF_H + 60,
           "8mm BACKING PLATE (welded to wall)\n(flat load anchor — behind the\nhinge cleat + each chain\nwall anchor; TAPPED M8)",
           color=C_OUT, fs=6, ha="right", font=FONT)

    # hinge: wall leaf + knuckle + shelf leaf
    ax.add_patch(Rectangle((0, SHELF_H - 4), 8, 60, fc=C_HINGE, ec=C_OUT, lw=1.0, zorder=4))   # wall leaf (up)
    ax.add_patch(Circle((10, SHELF_H), 8, fc="#9098A0", ec=C_OUT, lw=1.0, zorder=6))            # knuckle
    ax.add_patch(Rectangle((10, SHELF_H - SHELF_T), SHELF_DEPTH - 10, SHELF_T, fc=C_SHELF, ec=C_OUT, lw=1.2, zorder=5))  # shelf board (full deployed depth)
    ax.add_patch(Rectangle((SHELF_DEPTH - 6, SHELF_H), 6, 15, fc=C_SHELF, ec=C_OUT, lw=0.8, zorder=6))  # front lip
    leader(ax, 10, SHELF_H, 35, SHELF_H + 50, "PIANO HINGE\n(continuous, along the back edge)",
           color=C_HINGE, fs=6.5, ha="left", font=FONT)
    leader(ax, 65, SHELF_H - SHELF_T, 120, SHELF_H + SHELF_T - 60,
           f"SHELF BOARD\n18mm ply, ply-primary ({SHELF_T}mm)\n(no steel frame; tee-nut attach)", color="#5a4a18", fs=6.5, ha="left", font=FONT)

    # stay anchor + stay to the front
    ax.add_patch(Rectangle((0, STAY_Z - 10), 16, 20, fc=C_HINGE, ec=C_OUT, lw=1.0, zorder=4))
    ax.plot([8, SHELF_DEPTH - 10], [STAY_Z, SHELF_H], color=C_HINGE, lw=3.0, zorder=5)
    ax.add_patch(Circle((SHELF_DEPTH - 10, SHELF_H), 6, fc="#9098A0", ec=C_OUT, lw=0.8, zorder=6))
    leader(ax, 8, STAY_Z, 70, STAY_Z + 40, "CHAIN WALL ANCHOR\n(M8 eye bolt, above the hinge)", color=C_HINGE, fs=6.5,
           ha="left", font=FONT)
    leader(ax, (8 + SHELF_DEPTH - 10) / 2, (STAY_Z + SHELF_H) / 2, SHELF_DEPTH - 60, (STAY_Z + SHELF_H) / 2 + 60,
           "SS CHAIN STAY (tension)\ncarries the deployed load;\nslackens when shelf folds up",
           color=C_HINGE, fs=6.5, ha="left", font=FONT)

    title_block(ax, "SHEET 3 OF 5", drawing_title="CHEMISTRY PREP SHELF",
                subtitle="DETAIL — PIANO HINGE + STAY",
                scale_note="Axes in mm · DETAIL", height=0.08)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "shelf-sheet3.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/shelf-sheet3.png saved")


# ── Fab-detail layout (diagram-of-record — exact hole positions belong in the drawing) ──
TNUT_HINGE_N  = 4                                  # hinge bolts (into tee-nuts) along the back edge
TNUT_MARGIN_X = 75                                 # first/last hinge tee-nut inset from the board sides
TNUT_HINGE_PITCH = (SHELF_W - 2 * TNUT_MARGIN_X) / (TNUT_HINGE_N - 1)   # = 150mm
TNUT_HINGE_YD = 7                                  # hinge tee-nut row inset — mid-leaf of the 12.7mm hinge leaf (1582A452 datasheet), clear of the ~2.9mm barrel
TNUT_EYE_X    = 30                                 # front-corner eye-bolt tee-nut inset from each side
TNUT_EYE_YD   = SHELF_DEPTH - 20                   # eye-bolt tee-nut inset from the front edge
TNUT_HOLE_D   = 8                                  # tee-nut barrel hole (5/16") — Ø8
LIP_W         = 15                                 # spill-lip width (3 free edges)
HINGE_XS      = [TNUT_MARGIN_X + i * TNUT_HINGE_PITCH for i in range(TNUT_HINGE_N)]
EYE_XS        = [TNUT_EYE_X, SHELF_W - TNUT_EYE_X]

# ── Piano hinge 1582A452 (blank) geometry — from the McMaster datasheet ──
HINGE_OPEN    = 25.4     # open width (1in) — both leaves flat
HINGE_LEAF    = 12.7     # each leaf, pin-line to edge (0.5in)
HINGE_BARREL  = 2.9      # knuckle barrel Ø (0.113in)
HINGE_GAUGE   = TNUT_HINGE_YD   # hole gauge from the pin line = the 7mm board row (mid-leaf)
HINGE_DRILL_D = 7        # 1/4-20 clearance in each leaf (Ø~7)


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 4 — BOARD FABRICATION (top view: cut + tee-nut drill positions)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet4():
    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(-95, SHELF_W + 150); ax.set_ylim(-150, SHELF_DEPTH + 330)
    ax.set_aspect("equal"); ax.axis("off")

    # board outline (top view; back edge = hinge at Yd0, front edge at Yd=SHELF_DEPTH)
    ax.add_patch(Rectangle((0, 0), SHELF_W, SHELF_DEPTH, fc="white", ec=C_OUT, lw=1.4, zorder=2))
    # spill lip inner lines on the 3 free edges (front + 2 sides); back edge = hinge, no lip
    for (x0, y0, x1, y1) in [(0, SHELF_DEPTH - LIP_W, SHELF_W, SHELF_DEPTH - LIP_W),
                             (LIP_W, 0, LIP_W, SHELF_DEPTH),
                             (SHELF_W - LIP_W, 0, SHELF_W - LIP_W, SHELF_DEPTH)]:
        ax.plot([x0, x1], [y0, y1], color=C_DIM, lw=0.8, ls=(0, (4, 3)), zorder=3)

    # hinge tee-nut row + front-corner eye-bolt tee-nuts
    for x in HINGE_XS:
        ax.add_patch(Circle((x, TNUT_HINGE_YD), TNUT_HOLE_D / 2, fc="white", ec=C_OUT, lw=1.0, zorder=5))
    for x in EYE_XS:
        ax.add_patch(Circle((x, TNUT_EYE_YD), TNUT_HOLE_D / 2, fc="white", ec=C_OUT, lw=1.2, zorder=5))

    # dimensions — overall + per-hole (chained X for the hinge row, X-from-each-side for eyes; row Y)
    draw_dim_h(ax, 0, SHELF_W, -106, f"{SHELF_W}mm", fs=6, font=FONT, above=False)
    draw_dim_v(ax, SHELF_W + 34, 0, SHELF_DEPTH, f"{SHELF_DEPTH}mm", fs=6, font=FONT)

    # hinge row (4 holes): chained X so every hole is dimensioned; row Y from the back/hinge edge
    hx = [0] + HINGE_XS + [SHELF_W]
    for a, b in zip(hx[:-1], hx[1:]):
        draw_dim_h(ax, a, b, -34, f"{int(round(b - a))}mm", fs=5.2, font=FONT, above=False)
    draw_dim_v(ax, -34, 0, TNUT_HINGE_YD, f"{TNUT_HINGE_YD}mm", fs=5.5, font=FONT)

    # eye holes (2): X inset from each side; row Y from the back edge
    draw_dim_h(ax, 0, EYE_XS[0], -70, f"{TNUT_EYE_X}mm", fs=5.2, font=FONT, above=False)
    draw_dim_h(ax, EYE_XS[1], SHELF_W, -70, f"{TNUT_EYE_X}mm", fs=5.2, font=FONT, above=False)
    draw_dim_v(ax, -62, 0, int(TNUT_EYE_YD), f"{int(TNUT_EYE_YD)}mm", fs=5.5, font=FONT)

    # callouts (right side — front-corner eye tee-nut + lip; hinge row is dimensioned + noted)
    leader(ax, EYE_XS[1], TNUT_EYE_YD, SHELF_W + 44, TNUT_EYE_YD,
           "2× Ø8 tee-nut — front corner\n(1/4-20 eye bolt → chain)", fs=6, font=FONT, ha="left")
    leader(ax, SHELF_W - LIP_W, LIP_W * 2, SHELF_W + 44, LIP_W * 2 - 26,
           f"{LIP_W}mm spill lip\n(ply/HDPE, 3 free edges)", fs=6, font=FONT, ha="left")

    # notes (top — clear of the board + dims)
    draw_notes(ax, [
        "BOARD FAB — 18mm phenolic / UV-coated ply; ply-primary (NO steel frame). Seal all cut edges.",
        f"HINGE ROW (back/bottom edge): {TNUT_HINGE_N}× Ø{TNUT_HOLE_D} pronged tee-nut (825001) at "
        f"{int(TNUT_HINGE_PITCH)}mm pitch, {TNUT_MARGIN_X}mm side margin — seat from the BACK face.",
        "Piano hinge 1582A452 supplied BLANK — 25.4mm open / 12.7mm leaf. Hinge row sits 7mm off the "
        "back edge (mid-leaf, clear of the barrel); drill both leaves to this pitch. Use pan/truss-head "
        "screws — a CSK head overhangs the narrow leaf.",
        "Back (bottom) edge = piano hinge (no lip). Front corners: 2× Ø8 tee-nut for the chain eye bolts.",
    ], 0, SHELF_DEPTH + 285, spacing=18, fs=6, width=680, wrap=112, font=FONT)

    title_block(ax, "SHEET 4 OF 5", drawing_title="CHEMISTRY PREP SHELF",
                subtitle="BOARD FABRICATION — 18mm PLY (cut + tee-nut drill)",
                scale_note="Axes in mm", height=0.08)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "shelf-sheet4.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/shelf-sheet4.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 5 — WALL PLATES + HINGE CLEAT + PIANO HINGE DRILLING
# ═══════════════════════════════════════════════════════════════════════════════
def sheet5():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(-70, 1180); ax.set_ylim(0, 820)
    ax.set_aspect("equal"); ax.axis("off")

    # ── Hinge cleat + its 8mm hinge-backing plate (drawn 1:1-ish, top zone) ──
    cx0, cy0, CL_W, CL_H = 60, 660, 600, 40
    ax.add_patch(Rectangle((cx0, cy0), CL_W, CL_H, fc="white", ec=C_OUT, lw=1.2, zorder=3))
    for x in HINGE_XS:                                        # hinge-screw holes (align to the board tee-nut row)
        ax.add_patch(Circle((cx0 + x, cy0 + CL_H * 0.68), 3.2, fc="white", ec=C_OUT, lw=0.9, zorder=5))
    for x in HINGE_XS:                                        # M8 cleat→backing bolts (1 per hinge bolt)
        ax.add_patch(Circle((cx0 + x, cy0 + CL_H * 0.30), 5, fc="white", ec=C_OUT, lw=1.1, zorder=5))
    draw_dim_h(ax, cx0, cx0 + CL_W, cy0 - 40, f"{CL_W}mm", fs=6, font=FONT, above=False)
    # per-hole X (hinge-screw row, chained — the M8 cleat bolts share these node positions)
    cx = [0] + HINGE_XS + [SHELF_W]
    for a, b in zip(cx[:-1], cx[1:]):
        draw_dim_h(ax, cx0 + a, cx0 + b, cy0 - 18, f"{int(round(b - a))}mm", fs=5.0, font=FONT, above=False)
    # per-hole Y (both rows, from the bottom edge)
    draw_dim_v(ax, cx0 - 16, cy0, cy0 + CL_H * 0.68, f"{int(round(CL_H * 0.68))}mm", fs=5.0, font=FONT)
    draw_dim_v(ax, cx0 - 40, cy0, cy0 + CL_H * 0.30, f"{int(round(CL_H * 0.30))}mm", fs=5.0, font=FONT)
    leader(ax, cx0 + HINGE_XS[1], cy0 + CL_H * 0.68, cx0 + HINGE_XS[1], cy0 + CL_H + 42,
           f"hinge-screw holes — {TNUT_HINGE_N}× TAPPED 1/4-20 at {int(TNUT_HINGE_PITCH)}mm (wall leaf → cleat)", fs=5.6, font=FONT, ha="center")
    leader(ax, cx0 + HINGE_XS[-1], cy0 + CL_H * 0.30, cx0 + CL_W + 20, cy0 + 4,
           f"{TNUT_HINGE_N}× Ø9 clear → TAPPED M8 backing plate", fs=5.6, font=FONT, ha="left")
    ax.text(cx0, cy0 + CL_H + 60, "HINGE CLEAT — 6mm steel, 600 long (piano-hinge wall leaf bolts to it)",
            fontsize=6.5, color=C_OUT, ha="left", **FONT)

    # ── 8mm backing plates (mid zone) ──
    # hinge-backing plate (long)
    hbx, hby, HB_W, HB_H = 60, 470, 600, 60
    ax.add_patch(Rectangle((hbx, hby), HB_W, HB_H, fc="white", ec=C_OUT, lw=1.2, hatch="///", zorder=3))
    for x in HINGE_XS:
        ax.add_patch(Circle((hbx + x, hby + HB_H / 2), 5, fc="white", ec=C_OUT, lw=1.1, zorder=5))
    draw_dim_h(ax, hbx, hbx + HB_W, hby - 40, f"{HB_W}mm", fs=6, font=FONT, above=False)
    draw_dim_v(ax, hbx - 14, hby, hby + HB_H, f"{HB_H}mm", fs=5.5, font=FONT)
    # per-hole X (M8 row, chained — 1 per hinge bolt) + Y (row centered in the plate)
    bx = [0] + HINGE_XS + [HB_W]
    for a, b in zip(bx[:-1], bx[1:]):
        draw_dim_h(ax, hbx + a, hbx + b, hby - 18, f"{int(round(b - a))}mm", fs=5.0, font=FONT, above=False)
    draw_dim_v(ax, hbx - 40, hby, hby + HB_H / 2, f"{int(HB_H / 2)}mm", fs=5.0, font=FONT)
    ax.text(hbx, hby + HB_H + 14, f"HINGE-BACKING PLATE — 8mm steel (welded to wall crests; {TNUT_HINGE_N}× TAPPED M8)",
            fontsize=6.2, color=C_OUT, ha="left", **FONT)

    # chain-anchor backing plate (small, ×2)
    abx, aby, AB = 720, 470, 80
    ax.add_patch(Rectangle((abx, aby), AB, AB, fc="white", ec=C_OUT, lw=1.2, hatch="///", zorder=3))
    ax.add_patch(Circle((abx + AB / 2, aby + AB / 2), 5, fc="white", ec=C_OUT, lw=1.1, zorder=5))
    draw_dim_h(ax, abx, abx + AB, aby - 40, f"{AB}mm", fs=5.5, font=FONT, above=False)
    draw_dim_v(ax, abx + AB + 22, aby, aby + AB, f"{AB}mm", fs=5.5, font=FONT)
    # centered hole
    draw_dim_h(ax, abx, abx + AB / 2, aby - 18, f"{int(AB / 2)}mm", fs=5.0, font=FONT, above=False)
    draw_dim_v(ax, abx - 16, aby, aby + AB / 2, f"{int(AB / 2)}mm", fs=5.0, font=FONT)
    leader(ax, abx + AB / 2, aby + AB / 2, abx + AB + 30, aby + AB + 20,
           "TAPPED M8 —\nchain wall-anchor eye bolt", fs=5.6, font=FONT, ha="left")
    ax.text(abx, aby + AB + 44, "CHAIN-ANCHOR PLATE ×2 — 8mm steel", fontsize=6.2, color=C_OUT, ha="left", **FONT)

    # ── piano hinge drilling (blank 1582A452, opened flat — bottom zone) ──
    HX0, HY0 = 60, 310                               # strip left x (aligned with the cleat + backing plate), pin-line y
    ax.text(HX0, HY0 + 74, "PIANO HINGE DRILLING — blank 1582A452, opened flat (drill BOTH leaves)",
            fontsize=6.5, color=C_OUT, ha="left", **FONT)
    ax.add_patch(Rectangle((HX0, HY0 - HINGE_LEAF), SHELF_W, HINGE_OPEN, fc="white", ec=C_OUT, lw=1.4, zorder=3))
    ax.add_patch(Rectangle((HX0, HY0 - HINGE_BARREL / 2), SHELF_W, HINGE_BARREL, fc="#EDEDED", ec="none", zorder=4))
    ax.plot([HX0, HX0 + SHELF_W], [HY0, HY0], color=C_OUT, lw=0.8, ls=(0, (5, 3)), zorder=5)
    for x in HINGE_XS:
        ax.add_patch(Circle((HX0 + x, HY0 + HINGE_GAUGE), HINGE_DRILL_D / 2, fc="white", ec=C_OUT, lw=1.1, zorder=6))
        ax.add_patch(Circle((HX0 + x, HY0 - HINGE_GAUGE), HINGE_DRILL_D / 2, fc="white", ec=C_OUT, lw=1.1, zorder=6))
    leader(ax, HX0 + HINGE_XS[-1], HY0 + HINGE_GAUGE, HX0 + SHELF_W + 24, HY0 + HINGE_LEAF + 8,
           "SHELF LEAF → board tee-nut row (Sheet 4)", fs=5.8, font=FONT, ha="left")
    leader(ax, HX0 + HINGE_XS[-1], HY0 - HINGE_GAUGE, HX0 + SHELF_W + 24, HY0 - HINGE_LEAF - 8,
           "WALL LEAF → the cleat holes (above)", fs=5.8, font=FONT, ha="left")
    leader(ax, HX0 + HINGE_XS[1], HY0 + HINGE_GAUGE, HX0 + HINGE_XS[1], HY0 + 44,
           f"Ø{HINGE_DRILL_D} clear (1/4-20), both leaves", fs=5.8, font=FONT, ha="center")
    hx = [0] + HINGE_XS + [SHELF_W]
    for a, b in zip(hx[:-1], hx[1:]):
        draw_dim_h(ax, HX0 + a, HX0 + b, HY0 - HINGE_LEAF - 16, f"{int(round(b - a))}mm", fs=5.2, font=FONT, above=False)
    draw_dim_h(ax, HX0, HX0 + SHELF_W, HY0 - HINGE_LEAF - 38, f"{SHELF_W}mm (2ft stock, cut)", fs=5.8, font=FONT, above=False)
    draw_dim_v(ax, HX0 - 34, HY0 - HINGE_LEAF, HY0 + HINGE_LEAF, f"{HINGE_OPEN}mm open", fs=5.2, font=FONT)
    draw_dim_v(ax, HX0 - 62, HY0, HY0 + HINGE_GAUGE, f"{HINGE_GAUGE}mm", fs=5.0, font=FONT)
    draw_dim_v(ax, HX0 - 62, HY0 - HINGE_GAUGE, HY0, f"{HINGE_GAUGE}mm", fs=5.0, font=FONT)
    draw_notes(ax, [
        f"HINGE DRILLING — drill BOTH leaves {TNUT_HINGE_N}× at {int(TNUT_HINGE_PITCH)}mm pitch, "
        f"{TNUT_MARGIN_X}mm margin, gauge {HINGE_GAUGE}mm off the pin line (mid-leaf). Shelf leaf → board "
        "tee-nuts (Sheet 4); wall leaf → the tapped cleat above.",
        "Pan/truss-head 1/4-20 — a CSK head overhangs the 12.7mm leaf. Open 25.4 / leaf 12.7 / barrel Ø2.9. "
        "Deburr; keep the knuckle clear.",
    ], 60, HY0 - HINGE_LEAF - 66, spacing=17, fs=6, width=1080, wrap=142, font=FONT)

    title_block(ax, "SHEET 5 OF 5", drawing_title="CHEMISTRY PREP SHELF",
                subtitle="WALL PLATES + HINGE CLEAT + PIANO HINGE DRILLING",
                scale_note="Axes in mm · 1:1", height=0.07)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "shelf-sheet5.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/shelf-sheet5.png saved")


if __name__ == "__main__":
    print("Generating chemistry prep shelf diagrams (fold-down)...")
    sheet1(); sheet2(); sheet3(); sheet4(); sheet5()
    print("Done.")
