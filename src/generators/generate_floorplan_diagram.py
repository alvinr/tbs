#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_floorplan_diagram.py  —  TBS-001 Container Floor Plan (redesigned 2026-04-23 rev 2)

Top-down schematic of the full container interior, showing all systems
in their real positions with space constraints respected.

Coordinate system (all mm):
  X = 0 → 5893  (container interior length — long axis)
           X=0: cargo door short end (hinged panel / light trap)
           X=5893: sealed short end
  Y = 0 → 2362  (container interior width = optical axis depth)
           Y=0:    pinhole long wall
           Y=2362: far long wall (image plane / film fabric)

Equipment layout — end-zone design rev 5 (4-IBC 2×2 stack, drums eliminated):
  Left end zone  (X=0–150):    light trap drum only (freed up by drum removal)
  Pinhole wall   (Yd=0 face):  duct penetration (X=1200) + electrical panel + battery bank
  Optical zone   (X=150–4649): film plane rails only — floor clear
  Right end zone (X=4649–5893): 4× IBC in 2×2 stack (2 columns × 2 high)

  Every item in the end zones is provably shadow-free at all depths:
    cone left boundary  >= 150mm  at any Y <= 2262  ✓
    cone right boundary <= 4649mm  at any Y <= 2262  ✓
"""

import numpy as np
from tbs_title_block import title_block
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Arc
from matplotlib.lines import Line2D
import matplotlib.patches

from tbs_constants import *
from tbs_drawing import draw_dim_h, draw_dim_v, draw_legend

# ── Palette (local overrides removed — equipment colors from tbs_constants) ──
BG            = "#FFFFFF"
C_RAIL        = "#5A3E00"
C_PINHOLE     = C_PINHOLE_EQ
C_OPT         = C_FILM
C_ZONE_L      = "#FFF3E8"   # left zone tint
C_ZONE_R      = "#E8F3FF"   # right zone tint
C_ZONE_OPT    = "#F0F8F0"   # optical zone tint
C_PROC_ZONE   = "#E8F0FF"   # interior processing zone tint
FONT          = {"fontfamily": "monospace"}

WALL  = 40   # schematic wall thickness


def equip_rect(ax, x, y, w, h, col, label, label_color="#FFFFFF", zorder=6, alpha=0.88):
    ax.add_patch(Rectangle((x, y), w, h, fc=col, ec=C_OUT, lw=1.2, alpha=alpha, zorder=zorder))
    ax.text(x + w/2, y + h/2, label, color=label_color, fontsize=6,
            ha="center", va="center", **FONT, fontweight="bold", zorder=zorder+1)

def penetration(ax, x, y, r=60, col=C_OUT, label="", label_offset=(0, 80)):
    ax.add_patch(Circle((x, y), r, fc="#FFE0A0", ec=col, lw=1.5, zorder=8))
    ax.plot([x-r, x+r], [y, y], color=col, lw=0.8, zorder=9)
    ax.plot([x, x], [y-r, y+r], color=col, lw=0.8, zorder=9)
    if label:
        ax.text(x + label_offset[0], y + label_offset[1], label,
                color=col, fontsize=6, ha="center", va="bottom", **FONT, zorder=9)



def floor_plan():
    PAD_L = 600; PAD_R = 800; PAD_B = 800; PAD_T = 500

    X_LO = -PAD_L; X_HI = C_LEN + PAD_R
    Y_LO = -PAD_B; Y_HI = C_WID + PAD_T

    FIG_W = 24.0
    FIG_H = FIG_W * (Y_HI - Y_LO) / (X_HI - X_LO)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=130)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Y_LO, Y_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Zone highlights ───────────────────────────────────────────────────────
    # Left end zone (X=0–ZONE_L_END, all depths)
    ax.add_patch(Rectangle((0, 0), ZONE_L_END, C_WID,
                            fc=C_ZONE_L, ec="none", zorder=1))
    ax.text(0, C_WID*1.06,
            f"LEFT END ZONE\nX=0–{ZONE_L_END}mm\n(shadow-free,\nall depths)",
            color="#C07030", fontsize=6.5, ha="center", va="center",
            **FONT, alpha=0.7, fontweight="bold", zorder=2)

    # Optical / film plane zone (X=ZONE_L_END–ZONE_R_START, all depths)
    ax.add_patch(Rectangle((ZONE_L_END, 0), ZONE_R_START - ZONE_L_END, C_WID,
                            fc=C_ZONE_OPT, ec="none", zorder=1))
    ax.text((ZONE_L_END + ZONE_R_START)/2, C_WID*1.06,
            f"OPTICAL ZONE  (X={ZONE_L_END}–{ZONE_R_START}mm) FILM PLANE RAILS ONLY — FLOOR CLEAR",
            color="#4A8040", fontsize=8, ha="center", va="center",
            **FONT, alpha=0.45, fontweight="bold", zorder=2)

    # Right end zone (X=ZONE_R_START–C_LEN, all depths)
    ax.add_patch(Rectangle((ZONE_R_START, 0), C_LEN - ZONE_R_START, C_WID,
                            fc=C_ZONE_R, ec="none", zorder=1))
    ax.text(ZONE_R_START + (C_LEN - ZONE_R_START)/2, C_WID*1.06,
            f"RIGHT END ZONE\nX={ZONE_R_START}–{C_LEN}mm\n(shadow-free,\nall depths)",
            color="#3060A0", fontsize=6.5, ha="center", va="center",
            **FONT, alpha=0.7, fontweight="bold", zorder=2)

    # ── Optical cone boundary lines (plan view) ───────────────────────────────
    # Left ray: PH_X,0 → FP_X_L,FP_Y
    ax.plot([PH_X, FP_X_L], [0, FP_Y],
            color="#C07000", lw=1.0, ls=(0, (4, 3)), zorder=4, alpha=0.7)
    # Right ray: PH_X,0 → FP_X_R,FP_Y
    ax.plot([PH_X, FP_X_R], [0, FP_Y],
            color="#C07000", lw=1.0, ls=(0, (4, 3)), zorder=4, alpha=0.7)
    ax.text(PH_X - 1220, FP_Y * 0.75, "OPTICAL CONE\n(dashed)",
            color="#C07000", fontsize=6, ha="right", va="center", **FONT, alpha=0.8)

    # ── Container outline ─────────────────────────────────────────────────────
    ax.add_patch(Rectangle((0, 0), C_LEN, C_WID,
                            fc="none", ec=C_OUT, lw=2.5, zorder=3))

    # Container walls
    for patch in [
        (-WALL, -WALL, C_LEN + 2*WALL, WALL),   # pinhole wall
        (-WALL, C_WID, C_LEN + 2*WALL, WALL),   # far wall
        (-WALL, -WALL, WALL, C_WID + 2*WALL),   # left short wall (cargo door)
        (C_LEN, -WALL, WALL, C_WID + 2*WALL),   # right short wall
    ]:
        ax.add_patch(Rectangle((patch[0], patch[1]), patch[2], patch[3],
                                fc=C_WALL, ec=C_OUT, lw=1.5, zorder=3))

    # Wall labels
    ax.text(C_LEN/2, -WALL/2, "PINHOLE WALL  (20ft LONG SIDE)",
            color=C_OUT, fontsize=7, ha="center", va="center", **FONT, zorder=4)
    ax.text(C_LEN/2, C_WID + WALL/2, "FAR WALL — IMAGE PLANE SIDE  (20ft LONG SIDE)",
            color=C_OUT, fontsize=7, ha="center", va="center", **FONT, zorder=4)
    ax.text(-WALL/2, C_WID/2, "CARGO\nDOOR\nEND", color=C_OUT, fontsize=6,
            ha="center", va="center", **FONT, rotation=90, zorder=4)
    ax.text(C_LEN + WALL/2 + 5, C_WID/2, "SEALED END", color=C_OUT, fontsize=6,
            ha="center", va="center", **FONT, rotation=90, zorder=4)

    # Structural ribs
    for x_rib in np.arange(200, C_LEN, 600):
        ax.plot([x_rib, x_rib], [0, C_WID], color=C_WALL, lw=0.4, alpha=0.35, zorder=2)

    # ── Film plane rails (floor/ceiling, from RAIL_X_L to RAIL_X_R) ──────────
    RAIL_W = 35
    ax.plot([RAIL_X_L, RAIL_X_R], [FP_Y, FP_Y],
            color=C_RAIL, lw=2.5, zorder=5)
    ax.plot([RAIL_X_L, RAIL_X_L], [FP_Y_MIN, FP_Y + RAIL_W], color=C_RAIL, lw=2.0, zorder=5)
    ax.plot([RAIL_X_R, RAIL_X_R], [FP_Y_MIN, FP_Y + RAIL_W], color=C_RAIL, lw=2.0, zorder=5)
    ax.text(RAIL_X_R + 80, FP_Y, f"FILM PLANE RAILS\n(X={RAIL_X_L}–{RAIL_X_R}mm)",
            color=C_RAIL, fontsize=6.5, ha="left", va="center", **FONT)

    # ── Film fabric / muslin ──────────────────────────────────────────────────
    ax.plot([FP_X_L, FP_X_R], [FP_Y, FP_Y],
            color=C_FILM, lw=4.0, zorder=5, alpha=0.9)
    for hx in np.arange(FP_X_L + 100, FP_X_R, 200):
        ax.plot([hx, hx + 60], [FP_Y, FP_Y], color=C_FILM, lw=1.5, zorder=5, alpha=0.5)
    ax.text(PH_X, FP_Y + 30,
            f"MUSLIN IMAGE PLANE  ({FP_W}×{FP_H}mm)  Y={FP_Y}mm",
            color=C_FILM, fontsize=7, ha="center", va="bottom", **FONT, backgroundcolor=BG)

    # ── Pinhole ───────────────────────────────────────────────────────────────
    penetration(ax, PH_X, 0, r=80, col=C_PINHOLE,
                label=f"PINHOLE X={PH_X}mm Ø{PH_D}mm",
                label_offset=(0, -135))

    # Optical axis arrow
    ax.annotate("", xy=(PH_X, FP_Y - 40), xytext=(PH_X, 80),
                arrowprops=dict(arrowstyle="->", color=C_OPT, lw=1.5,
                                mutation_scale=10, ls="--"))
    ax.text(PH_X + 50, C_WID/2 + 250, f"OPTICAL AXIS\n{C_WID}mm",
            color=C_OPT, fontsize=7, ha="left", va="center", **FONT)

    # ── LEFT END ZONE — equipment ─────────────────────────────────────────────
    # Hinged panel label
    ax.text(-WALL - 350, C_WID/5,
            "HINGED PANEL\n+ REVOLVING\nDRUM INLET",
            color=C_PINHOLE, fontsize=6.5, ha="right", va="center", **FONT, zorder=5)

    # Drum footprint in plan (semicircle inside container)
    DRUM_FP_CY = C_WID / 2   # centred on container Y
    drum_fp = matplotlib.patches.Wedge(
        (0, DRUM_FP_CY), DRUM_R, -90, 90,
        fc="#FFE8D0", ec=C_PINHOLE, lw=1.2, alpha=0.6, zorder=5)
    ax.add_patch(drum_fp)
    ax.text(DRUM_R - 160, DRUM_FP_CY,
            f"DRUM\nfootprint\nØ{DRUM_D}mm",
            color=C_PINHOLE, fontsize=5.5, ha="left", va="center", **FONT, zorder=6)
    penetration(ax, 0, DRUM_FP_CY, r=80,
                col=C_PINHOLE, label="DRUM\nINLET", label_offset=(-180, -30))

    # Evap duct penetration — cooler is external (rev 7)
    penetration(ax, EVAP_DUCT_X, 0, r=EVAP_DUCT_D / 2, col=C_EVAP,
                label=f"EVAP DUCT\nØ{EVAP_DUCT_D}\n(EXT. COOLER)",
                label_offset=(0, EVAP_DUCT_D / 2 + 60))

    # (waste drums and dolly tracks eliminated in rev 5 — left zone now light trap only)

    # ── PINHOLE WALL (Y=0 face) — wall-mounted items ──────────────────────────
    # Electrical panel (thin strip at Y=0) — raised to Z=1600–2200
    equip_rect(ax, EP_X, 0, EP_W, 80, C_ELEC,
               "ELEC\nPANEL", zorder=7, alpha=0.95)
    # Battery bank (slim profile, 120mm depth)
    equip_rect(ax, BA_X, 0, BA_W, BA_D, C_BATT,
               "BATT.", zorder=7, alpha=0.85)

    # ── EQUIPMENT PANEL (IBC plumbing corridor, Yd=1046) ────────────────────
    equip_rect(ax, EQPANEL_X, CORRIDOR_YD_NEAR, EQPANEL_W, CORRIDOR_W,
               C_PUMP, "EQUIP PANEL\n(PUMPS+FILTERS)", label_color="#000000", zorder=7, alpha=0.8)

    # External power panel (flush-mount, exterior of pinhole wall)
    PP_DEPTH = 60   # schematic depth on exterior face
    ax.add_patch(Rectangle(
        (PWR_PANEL_X, -WALL - PP_DEPTH), PWR_PANEL_W, PP_DEPTH,
        fc=C_ALUM, ec=C_OUT, lw=1.2, alpha=0.9, zorder=6))
    # Wall cutout / penetration line
    cut_x = PWR_PANEL_X + (PWR_PANEL_W - PWR_PANEL_CUTOUT_W) / 2
    ax.add_patch(Rectangle(
        (cut_x, -WALL), PWR_PANEL_CUTOUT_W, WALL,
        fc="white", ec=C_OUT, lw=0.8, alpha=0.7, zorder=6))
    ax.text(PWR_PANEL_X + PWR_PANEL_W / 2, -WALL - PP_DEPTH / 2,
            "EXT PWR\nPANEL",
            ha="center", va="center", fontsize=5, color=C_OUT,
            fontweight="bold", **FONT, zorder=7)

    # ── RIGHT END ZONE — 4× IBC in 2×2 stack ────────────────────────────────
    # Near column (Yd=30–1046): Blue #1 on top, Brown on bottom
    equip_rect(ax, IBC_COL_X, BLUE_IBC_Y, IBC_W, IBC_D, C_BLUE_IBC,
               f"IBC-1 BLUE\n600L (top)\nIBC-3 BROWN\n600L (bottom)\nYd={BLUE_IBC_Y}–{BLUE_IBC_Y+IBC_D}",
               zorder=6)
    ax.text(IBC_COL_X + IBC_W/2, BLUE_IBC_Y + IBC_D - 55,
            "▲ 2020mm tall (2-high)", fontsize=5.5,
            ha="center", va="bottom", **FONT, zorder=7)

    # Far column (Yd=1316–2332): Blue #2 on top, Waste on bottom — 270mm plumbing corridor between columns
    # Plan view sees top tier (Blue #2)
    equip_rect(ax, IBC_COL_X, IBC_FAR_Y, IBC_W, IBC_D, C_BLUE_IBC,
               f"IBC-2 BLUE\n600L (top)\nIBC-4 WASTE\n600L (bottom)\nYd={IBC_FAR_Y}–{IBC_FAR_Y+IBC_D}",
               zorder=6)
    ax.text(IBC_COL_X + IBC_W/2, IBC_FAR_Y + IBC_D - 55,
            "▲ 2020mm tall (2-high)", fontsize=5.5,
            ha="center", va="bottom", **FONT, zorder=7)

    # ── Wall penetrations ─────────────────────────────────────────────────────
    # Fan A — INTAKE: far end wall (X=C_LEN), near-wall corner (Yd=FAN_A_YD=75mm), LOW (H=600mm)
    penetration(ax, C_LEN, FAN_A_YD, r=55, col=C_DIM, label="FAN\nIN", label_offset=(130, -30))
    # Fan B — EXHAUST: cargo door end wall (X=0), centered between drum and far wall (Yd=FAN_B_YD=1959mm), HIGH (H=1800mm)
    penetration(ax, 0, FAN_B_YD, r=55, col=C_DIM, label="FAN\nOUT", label_offset=(-130, -30))

    # ── Hinged panel — transport position (ghost, slid 300mm into container) ──
    # Panel slides inward along pinhole wall (Yd=0) on HGR20 ceiling rails.
    # Ghost outline at X=PANEL_SLIDE shows transport position.
    TR_X = PANEL_SLIDE  # = 300mm
    GHOST_LS = (0, (6, 4))
    GHOST_A  = 0.35
    # Corner zones (Yd=0-756 and Yd=1606-2362)
    ax.add_patch(Rectangle((TR_X, 0), PANEL_CORNER_T, PANEL_CORNER_YD_L,
                            fc="none", ec=C_DIM, lw=1.0, ls=GHOST_LS,
                            zorder=4, alpha=GHOST_A))
    ax.add_patch(Rectangle((TR_X, PANEL_CORNER_YD_R), PANEL_CORNER_T,
                            C_WID - PANEL_CORNER_YD_R,
                            fc="none", ec=C_DIM, lw=1.0, ls=GHOST_LS,
                            zorder=4, alpha=GHOST_A))
    # Center zone (Yd=756-1606)
    ax.add_patch(Rectangle((TR_X, PANEL_CORNER_YD_L), PANEL_CENTER_T,
                            PANEL_CORNER_YD_R - PANEL_CORNER_YD_L,
                            fc="none", ec=C_DIM, lw=1.0, ls=GHOST_LS,
                            zorder=4, alpha=GHOST_A))
    ax.text(TR_X + PANEL_CENTER_T / 2, C_WID / 2,
            "PANEL\n(TRANSPORT)",
            color=C_DIM, fontsize=5.5, ha="center", va="center",
            **FONT, rotation=90, alpha=0.4, zorder=5)
    # Ghost drum in transport position (slides with panel)
    DRUM_TR_CX = TR_X + PANEL_CENTER_T / 2  # drum center follows panel center zone
    DRUM_TR_CY = C_WID / 2
    ax.add_patch(Circle((DRUM_TR_CX, DRUM_TR_CY), DRUM_R,
                         fc="none", ec=C_DIM, lw=1.0, ls=GHOST_LS,
                         zorder=4, alpha=GHOST_A))
    ax.plot([DRUM_TR_CX - 20, DRUM_TR_CX + 20], [DRUM_TR_CY, DRUM_TR_CY],
            color=C_DIM, lw=0.5, alpha=GHOST_A, zorder=4)
    ax.plot([DRUM_TR_CX, DRUM_TR_CX], [DRUM_TR_CY - 20, DRUM_TR_CY + 20],
            color=C_DIM, lw=0.5, alpha=GHOST_A, zorder=4)
    # Slide arrow: operational (X=0) → transport (X=300)
    arr_yd = -60
    ax.annotate("", xy=(TR_X + PANEL_CENTER_T / 2, arr_yd),
                xytext=(PANEL_CENTER_T / 2, arr_yd),
                arrowprops=dict(arrowstyle="->", color=C_DIM, lw=0.8),
                zorder=5)
    ax.text((PANEL_CENTER_T / 2 + TR_X + PANEL_CENTER_T / 2) / 2, arr_yd - 30,
            f"{PANEL_SLIDE}mm SLIDE", ha="center", va="top",
            color=C_DIM, fontsize=5, **FONT, alpha=0.5, zorder=5)

    # ── Processing tray (interior — optical zone floor) ─────────────────────
    ax.add_patch(Rectangle((PROC_TRAY_X_L, PROC_TRAY_YD_NEAR),
                            PROC_TRAY_W, PROC_TRAY_D,
                            fc=C_PROC_ZONE, ec=C_DIM, lw=1.0, ls=(0, (5, 3)),
                            zorder=1, alpha=0.35))
    ax.text((PROC_TRAY_X_L + PROC_TRAY_X_R) / 2,
            (PROC_TRAY_YD_NEAR + PROC_TRAY_YD_FAR) / 2,
            "PROCESSING TRAY  (304 SS, 50mm rim)\n"
            f"spray bar wash · sump at X={PROC_TRAY_DRAIN_X} (slope to IBC corner)",
            color=C_DIM, fontsize=6.5, ha="center", va="center", **FONT,
            alpha=0.7, zorder=4)

    # ── Perimeter walkway (4 mitered panels as polygons) ────────────────────
    from matplotlib.patches import Polygon
    C_WALKWAY = "#D0C8B8"   # warm gray for grating
    C_MITER   = "#806040"   # miter joint line color
    WK_HATCH  = "xx"        # cross-hatch pattern to indicate grating
    WK_ALPHA  = 0.55
    W = WALKWAY_W

    # Corner coordinates
    LX = WALKWAY_LEFT_X                    # left walkway left edge
    LXR = LX + W                          # left walkway right edge
    RX = WALKWAY_RIGHT_X                   # right walkway left edge
    RXR = RX + W                           # right walkway right edge (same width as all)
    NY = WALKWAY_NEAR_YD                   # near walkway outer (bottom) edge
    NYI = NY + W                           # near walkway inner edge
    FY = WALKWAY_FAR_YD                    # far walkway inner edge
    FYO = FY + W                           # far walkway outer (top) edge

    # Near walkway — mitered at both ends (triangles cut from corners)
    near_poly = Polygon([
        (LXR, NY),       # after left miter, bottom edge
        (RX, NY),        # before right miter, bottom edge
        (RXR, NYI),      # right miter point, inner edge
        (LX, NYI),       # left miter point, inner edge  — wait, this is wrong
    ], closed=True)
    # Actually: near walkway spans full X range but gets a diagonal cut at each end.
    # Bottom-left corner: miter goes from (LX, NY) to (LXR, NYI)
    #   Near panel keeps the triangle below the diagonal → vertices on near side
    # Bottom-right corner: miter goes from (RXR, NY) to (RX, NYI)
    #   Near panel keeps the triangle below the diagonal
    near_verts = [
        (LXR, NY),    # start: bottom edge, right of left miter
        (RX, NY),     # bottom edge, left of right miter
        (RXR, NYI),   # right miter diagonal endpoint (outer corner)
        # but wait — the near walkway outer edge extends to container wall...
    ]
    # Let me reconsider. The near/far walkways span from PROC_TRAY_X_L to
    # PROC_TRAY_X_L + PROC_TRAY_W. The left/right walkways span 0 to C_WID.
    # At the overlap corners (W×W squares), a 45° miter divides each square.
    #
    # Near walkway polygon (bottom, runs left–right):
    #   Outer edge (y=NY): from LX to RXR (full span)
    #   Inner edge (y=NYI): from LXR to RX (between miters)
    #   Left miter: diagonal from (LX, NY) to (LXR, NYI)
    #   Right miter: diagonal from (RXR, NY) to (RX, NYI)
    near_x0 = PROC_TRAY_X_L
    near_x1 = PROC_TRAY_X_L + PROC_TRAY_W
    near_verts = [
        (near_x0, NY),     # bottom-left corner (outer)
        (near_x1, NY),     # bottom-right corner (outer)
        (near_x1, NYI),    # top-right before miter — but right miter cuts here
        (RX, NYI),         # inner edge, left of right miter
        (RXR, NY),         # right miter hits outer edge — no, RXR > near_x1?
    ]
    # All 4 walkways are the same width — simple rectangles with butt joints.
    # Near walkway (pinhole side)
    ax.add_patch(Rectangle((LXR, NY), RX - LXR, W,
                         fc=C_WALKWAY, ec=C_DIM, lw=0.8, hatch=WK_HATCH,
                         alpha=WK_ALPHA, zorder=2))
    # Far walkway (film plane side)
    ax.add_patch(Rectangle((LXR, FY), RX - LXR, W,
                         fc=C_WALKWAY, ec=C_DIM, lw=0.8, hatch=WK_HATCH,
                         alpha=WK_ALPHA, zorder=2))
    # Left walkway (cargo door end)
    ax.add_patch(Rectangle((LX, NY), W, FYO - NY,
                         fc=C_WALKWAY, ec=C_DIM, lw=0.8, hatch=WK_HATCH,
                         alpha=WK_ALPHA, zorder=2))
    # Right walkway (IBC end) — ceiling-hung
    ax.add_patch(Rectangle((RX, NY), W, FYO - NY,
                         fc=C_WALKWAY, ec=C_DIM, lw=0.8, hatch=WK_HATCH,
                         alpha=WK_ALPHA, zorder=2))

    # Near walkway widened section (EP/BAT zone, 500mm) — rev 7
    WIDE_EXTRA = WALKWAY_NEAR_WIDE_W - W  # extra 200mm beyond standard 300mm
    ax.add_patch(Rectangle(
        (WALKWAY_NEAR_WIDE_X_L, NY + W), WALKWAY_NEAR_WIDE_X_R - WALKWAY_NEAR_WIDE_X_L, WIDE_EXTRA,
        fc="#E8FFE8", ec="#66AA66", lw=1.0, ls="--", hatch=WK_HATCH,
        alpha=0.4, zorder=2))
    ax.text((WALKWAY_NEAR_WIDE_X_L + WALKWAY_NEAR_WIDE_X_R) / 2,
            NY + W + WIDE_EXTRA / 2,
            f"WIDENED\n{WALKWAY_NEAR_WIDE_W}mm",
            color="#448844", fontsize=5, ha="center", va="center",
            fontweight="bold", **FONT, zorder=5)

    # Butt joint lines at corners
    C_MITER = C_DIM  # reuse color variable name
    butt_lines = [
        (LXR, NY, LXR, NYI),     # near-left butt
        (RX, NY, RX, NYI),       # near-right butt
        (LXR, FY, LXR, FYO),    # far-left butt
        (RX, FY, RX, FYO),      # far-right butt
    ]
    for x1, y1, x2, y2 in butt_lines:
        ax.plot([x1, x2], [y1, y2], color=C_MITER, lw=1.2, zorder=3)

    # Label the walkway
    ax.text(WALKWAY_RIGHT_X + WALKWAY_W / 2,
            C_WID / 2,
            f"WALKWAY {WALKWAY_W}mm",
            color=C_DIM, fontsize=5.5, ha="center", va="center",
            rotation=0, **FONT, backgroundcolor=BG, alpha=0.8, zorder=5)
    ax.text((PROC_TRAY_X_L + PROC_TRAY_X_R) / 2,
            WALKWAY_FAR_YD + WALKWAY_W / 2,
            f"WALKWAY  {WALKWAY_W}mm  (REMOVABLE GRATED · {WALKWAY_H}mm DECK HEIGHT)",
            color=C_DIM, fontsize=5.5, ha="center", va="center", backgroundcolor=BG,
            **FONT, alpha=0.8, zorder=5)

    # ── Dimension annotations ─────────────────────────────────────────────────
    draw_dim_h(ax, 0, C_LEN, C_WID + 300, f"{C_LEN}mm  ({C_LEN/304.8:.1f}ft)  INTERIOR LENGTH", offset=25, font=FONT)
    draw_dim_v(ax, C_LEN + 200, 0, C_WID,
          f"{C_WID}mm\nINTERIOR\nWIDTH\n(=FOCAL\nLENGTH)", offset=55, right=True, font=FONT)
    draw_dim_h(ax, 0, ZONE_L_END, -PAD_B + 600, f"{ZONE_L_END}mm\nLEFT ZONE", offset=25, fs=6, font=FONT)
    draw_dim_h(ax, ZONE_L_END, ZONE_R_START, -PAD_B + 600, f"{ZONE_R_START-ZONE_L_END}mm OPTICAL ZONE", offset=25, fs=6, font=FONT)
    draw_dim_h(ax, ZONE_R_START, C_LEN, -PAD_B + 600, f"{C_LEN-ZONE_R_START}mm RIGHT ZONE", offset=25, fs=6, font=FONT)
    draw_dim_h(ax, FP_X_L, FP_X_R, C_WID + 200, f"{FP_W}mm  FILM PLANE WIDTH", offset=25, fs=6, font=FONT)
    draw_dim_v(ax, PAD_L + 100, 0, FP_Y+100, f"Y={FP_Y}mm\nFILM PLANE\nDEPTH", offset=25, fs=6, right=True, font=FONT)

    # ── Shadow-free proof callout ─────────────────────────────────────────────
#     proof_x = C_LEN/2
#     ax.text(proof_x, -PAD_B + 80,
#             f"SHADOW-FREE PROOF:  cone left ≥ {FP_X_L}mm at all Y  ✓     "
#             f"cone right ≤ {FP_X_R}mm at all Y  ✓     "
#             "pinhole wall Y=0: outside cone ✓",
#             color="#204020", fontsize=6.5, ha="center", va="bottom",
#             **FONT, style="italic",
#             bbox=dict(boxstyle="round,pad=0.3", fc="#E8F8E8", ec="#408040", lw=0.8),
#             zorder=10)

    # ── Legend (three-column, below container) ───────────────────────────────
    leg_y_top = -PAD_B + 250 + 5 * 46 + 50   # position top of box
    draw_legend(ax, [
        (C_BLUE_IBC,  "Blue IBC ×2 (clean water, top tier)"),
        (C_BROWN_IBC, "Brown IBC ×1 (recycle, bottom near)"),
        (C_WASTE_IBC, "Waste IBC ×1 (bottom far)"),
        (C_EVAP,    "Evap duct penetration (cooler external)"),
        (C_ELEC,  "Electrical panel"),
        (C_BATT,  "Battery bank (slim 120mm)"),
        (C_PUMP,  "Equipment panel (pumps+filters, IBC corridor)"),
        (C_FILM,      f"Muslin image plane ({FP_W}×{FP_H}mm)"),
        (C_PINHOLE,   f"Pinhole Ø{PH_D}mm"),
        (C_OPT,       "Optical axis (2362mm focal length)"),
        (C_PINHOLE,   "Revolving light-trap drum"),
        (C_PROC_ZONE, "Processing tray (304 SS, 50mm rim)"),
        ("#D0C8B8",   f"Perimeter walkway ({WALKWAY_W}mm, removable grated)"),
        (C_ALUM,     "Ext power panel (flush-mount, exterior)"),
    ], 0, leg_y_top, cols=3, col_w=1900, font=FONT, zorder=8)

    # ── Film left-rail demountable segment (drum-mode clearance) ─────────────
    # The LEFT RAIL (X=RAIL_X_L=150mm) passes through the drum volume.
    # The segment spanning Yd=806–1556 is DEMOUNTABLE so the drum can rotate
    # ("drum mode"); carriage parks at Yd=2262 during drum mode.
    # Show this segment as a dashed orange overlay on the rail line.
    ax.plot([RAIL_X_L, RAIL_X_L],
            [BRACE_LEFT_DEMOUNT_Y0, BRACE_LEFT_DEMOUNT_Y1],
            color="#C07030", lw=4.0, ls=(0, (6, 3)), zorder=7, alpha=0.85,
            solid_capstyle="round")
    # Leader + note to the left (in the left end zone / exterior pad area)
    NOTE_NX = -PAD_L + 120
    NOTE_NY = (BRACE_LEFT_DEMOUNT_Y0 + BRACE_LEFT_DEMOUNT_Y1) / 2  # 1181
    ax.annotate("",
                xy=(RAIL_X_L, NOTE_NY),
                xytext=(NOTE_NX + 600, NOTE_NY),
                arrowprops=dict(arrowstyle="->", color="#C07030", lw=1.0),
                zorder=10)
    ax.text(NOTE_NX + 580, NOTE_NY + 80,
            f"FILM LEFT-RAIL SEGMENT DEMOUNTS FOR DRUM (drum mode)\n"
            f"X={RAIL_X_L}mm  Yd={BRACE_LEFT_DEMOUNT_Y0}–{BRACE_LEFT_DEMOUNT_Y1}mm\n"
            f"Swings clear for drum rotation · carriage parks at Yd={CARRIAGE_PARK_Y}",
            ha="right", va="bottom", fontsize=6.0, color="#7A3A00",
            fontweight="bold", **FONT, zorder=10,
            bbox=dict(boxstyle="round,pad=0.3", fc="#FFFBE6", ec="#C07030", lw=0.9))

    # ── Ghost overlays — in-envelope walkway sections (REMOVED for film-mech clearance) ──
    # The walkway portions inside the film-plane mechanism envelope
    # (X 150–4649, Yd 100–2262) are permanently removed.  Ghost them with the
    # same treatment as generate_walkway_diagram.py so both drawings agree.
    FM_YD_N = 100    # film-mechanism envelope near Yd boundary
    FM_YD_F = FYO    # = 2262 (CARRIAGE_PARK_Y = FYO)

    C_GHOST_WK   = "#CC4422"   # red-orange (matches walkway drawing)
    GHOST_WK_A   = 0.18        # ghost fill alpha
    GHOST_WK_A_E = 0.70        # ghost edge alpha

    def _ghost_rect(ax, x0, y0, w, h, zorder=12):
        """Overlay a ghosted cross-hatched rectangle to mark a removed walkway section."""
        ax.add_patch(Rectangle((x0, y0), w, h,
                                fc=C_GHOST_WK, ec="none", lw=0,
                                alpha=GHOST_WK_A, zorder=zorder))
        ax.add_patch(Rectangle((x0, y0), w, h,
                                fc="none", ec=C_GHOST_WK, lw=1.5, ls=(0, (6, 4)),
                                alpha=GHOST_WK_A_E, zorder=zorder + 1))
        import matplotlib.patches as _mp
        ax.add_patch(_mp.Rectangle((x0, y0), w, h,
                                   fc="none", ec=C_GHOST_WK, lw=0.5,
                                   hatch="////", alpha=0.30, zorder=zorder))

    # NEAR: inner strip Yd 100–300, full span X 470–4329
    _ghost_rect(ax, LXR, FM_YD_N, RX - LXR, NYI - FM_YD_N)
    # FAR: inner strip Yd 1962–2262, full span X 470–4329
    _ghost_rect(ax, LXR, FY, RX - LXR, FM_YD_F - FY)
    # LEFT: inner Yd span 100–2262, full width X 170–470
    _ghost_rect(ax, LX, FM_YD_N, W, FM_YD_F - FM_YD_N)
    # RIGHT: inner Yd span 100–2262, full width X 4329–4629
    _ghost_rect(ax, RX, FM_YD_N, W, FM_YD_F - FM_YD_N)

    # ── Dropped-walkway note (film-mechanism envelope) ────────────────────────
    ax.text((ZONE_L_END + ZONE_R_START) / 2, -PAD_B + 480,
            "NOTE: Walkway sections inside film-mechanism envelope\n"
            f"(X={ZONE_L_END}–{ZONE_R_START}mm, Yd 100–{CARRIAGE_PARK_Y}mm) are DROPPED — "
            "see walkway drawing for detail.",
            ha="center", va="top", fontsize=6.5, color="#AA3300",
            style="italic", **FONT, zorder=10,
            bbox=dict(boxstyle="round,pad=0.3", fc="#FFF0EE", ec="#AA3300", lw=0.8))

    # ── Egress path annotation ─────────────────────────────────────────────────
    # With drums eliminated, the full container width (2362mm) is clear for egress.
    # Panel opens 180° outward, light trap drum swings out with it.
    EGRESS_GAP    = C_WID   # full width clear — no drums
    EGRESS_MID_Y  = C_WID / 2
    EGRESS_ARROW_X = ZONE_L_END / 2

    # Dashed green arrow showing egress direction (interior → door)
    ax.annotate("", xy=(-WALL - 60, EGRESS_MID_Y),
                xytext=(ZONE_L_END - 60, EGRESS_MID_Y),
                arrowprops=dict(arrowstyle="->", color="#20A020", lw=2.0,
                                linestyle="-", mutation_scale=12),
                zorder=15)
    ax.text(EGRESS_ARROW_X, EGRESS_MID_Y + 90,
            f"EGRESS PATH — {EGRESS_GAP}mm CLEAR (FULL WIDTH)",
            color="#20A020", fontsize=6.5, ha="center", va="bottom",
            fontweight="bold", **FONT, zorder=10)

    title_block(ax, "SHEET 1 OF 1",
                drawing_title="CONTAINER FLOOR PLAN",
                subtitle="End-zone layout (top-down view)",
                scale_note="1:75 (approx)",
                doc_id="TBS-001 · Floor Plan")

    import os; os.makedirs(DIAGRAMS_DIR, exist_ok=True); os.makedirs(SVG_DIR, exist_ok=True)
    out = f"{DIAGRAMS_DIR}/container-floorplan.png"
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  {out} saved")


def egress_detail():
    """Sheet 2 — Cargo door end egress detail.

    Zoomed plan view showing the panel swung 180° OUTWARD (exterior).
    The panel hinges on the pinhole-wall edge (Yd=0) and swings into
    the exterior space (X<0).

    Physical constraints that prevent inward opening:
      • Light trap drum (750mm dia) would cross container wall
      • Film plane rails at X=150 (floor + ceiling) block swing path

    Egress: with drums eliminated (rev 5), the full container width
    (2362mm) is clear for egress once the panel is swung outward.
    """
    import math

    # ── Layout constants ─────────────────────────────────────────────────────
    PAD = 350
    # Extend X range leftward to show panel in open (exterior) position
    # Panel is 2362mm wide; when open 180° the far tip reaches X = -2362
    X_LO, X_HI = -2700, 1200
    TB_PAD = 600   # extra space at bottom for title block
    Y_LO, Y_HI = -PAD - TB_PAD, C_WID + PAD
    FIG_W = 22.0
    FIG_H = FIG_W * (Y_HI - Y_LO) / (X_HI - X_LO)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Y_LO, Y_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    C_EGRESS = "#20A020"
    C_GHOST  = "#9090C0"

    # ── Zone tints (interior only) ───────────────────────────────────────────
    ax.add_patch(Rectangle((0, 0), ZONE_L_END, C_WID,
                            fc=C_ZONE_L, ec="none", zorder=1))
    ax.add_patch(Rectangle((ZONE_L_END, 0), X_HI - ZONE_L_END, C_WID,
                            fc=C_ZONE_OPT, ec="none", zorder=1))

    # Exterior tint (outside cargo door)
    ax.add_patch(Rectangle((X_LO, 0), -X_LO, C_WID,
                            fc="#F0F0F0", ec="none", zorder=0))
    ax.text(X_LO / 2, C_WID / 2, "EXTERIOR",
            color=C_DIM, fontsize=12, ha="center", va="center",
            **FONT, alpha=0.3, fontweight="bold", zorder=1)

    ax.plot([ZONE_L_END, ZONE_L_END], [0, C_WID],
            color=C_DIM, lw=1.0, ls="--", zorder=3, alpha=0.5)
    ax.text(ZONE_L_END, C_WID + 60, f"X={ZONE_L_END}",
            color=C_DIM, fontsize=7, ha="center", va="bottom", **FONT)

    # ── Container walls ──────────────────────────────────────────────────────
    ax.plot([0, X_HI], [0, 0], color=C_OUT, lw=2.5, zorder=3)
    ax.plot([0, X_HI], [C_WID, C_WID], color=C_OUT, lw=2.5, zorder=3)

    # Wall thickness
    for patch in [
        (0, -WALL, X_HI, WALL),                     # pinhole wall
        (0, C_WID, X_HI, WALL),                     # far wall
        (-WALL, -WALL, WALL, C_WID + 2*WALL),       # cargo door end wall
    ]:
        ax.add_patch(Rectangle((patch[0], patch[1]), patch[2], patch[3],
                                fc=C_WALL, ec=C_OUT, lw=1.2, zorder=3))

    # Wall labels
    ax.text(-WALL/2-75, C_WID/2+50, "CARGO\nDOOR\nEND",
            color=C_OUT, fontsize=7, ha="center", va="center",
            **FONT, rotation=90, zorder=4)
    ax.text(X_HI/2, -WALL/2, "PINHOLE WALL  (Yd=0)",
            color=C_OUT, fontsize=6.5, ha="center", va="center", **FONT, zorder=4)
    ax.text(X_HI/2, C_WID + WALL/2, f"FAR WALL  (Yd={C_WID})",
            color=C_OUT, fontsize=6.5, ha="center", va="center", **FONT, zorder=4)

    # ── Door frame (50×50mm RHS at each corner of opening) ───────────────────
    FRAME = 50
    ax.add_patch(Rectangle((-FRAME, -FRAME), FRAME, C_WID + 2*FRAME,
                            fc="none", ec=C_OUT, lw=1.0, ls=(0, (3, 2)),
                            zorder=3, alpha=0.3))
    ax.add_patch(Rectangle((0, 0), FRAME, FRAME,
                            fc=C_WALL, ec=C_OUT, lw=0.8, zorder=5))
    ax.add_patch(Rectangle((0, C_WID - FRAME), FRAME, FRAME,
                            fc=C_WALL, ec=C_OUT, lw=0.8, zorder=5))

    # ── Film plane rails (floor/ceiling) ─────────────────────────────────────
    RAIL_VIS_W = 25
    ax.add_patch(Rectangle((RAIL_X_L - RAIL_VIS_W/2, FP_Y - 15),
                            RAIL_VIS_W, 30,
                            fc=C_RAIL, ec=C_OUT, lw=0.8, zorder=5, alpha=0.7))
    ax.text(RAIL_X_L, FP_Y + 40,
            f"FILM PLANE RAIL\n(floor + ceiling)\nX={RAIL_X_L}",
            color=C_RAIL, fontsize=5.5, ha="center", va="bottom", **FONT, zorder=8)

    # (waste drums and dolly tracks eliminated in rev 5 — left zone clear)

    # ── Panel open 180° OUTWARD ──────────────────────────────────────────────
    # Hinge axis: vertical line at X=0, Yd=0 (pinhole wall corner).
    # Panel spans full Yd width (2362mm). When closed, it sits at X=0.
    # When open 180° outward, it lies parallel to the pinhole wall but
    # in exterior space, extending from X=0 to X=-2362 along Yd=0.
    #
    # In plan view: the hinge is at (X=0, Yd=0). A point on the panel
    # at distance r from the hinge, when rotated 180° outward (clockwise
    # looking down, from +Yd toward -X), ends up at (X=-r, Yd=0).

    # Open panel — lies along Yd=0 in exterior space (X=0 to X=-C_WID)
    # Corner zone near (was Yd=0–756) → now X=0 to X=-756, Yd=0 to Yd=-40
    ax.add_patch(Rectangle((-PANEL_CORNER_YD_L, -PANEL_CORNER_T),
                            PANEL_CORNER_YD_L, PANEL_CORNER_T,
                            fc="#E0D0C0", ec=C_PINHOLE, lw=1.5,
                            alpha=0.6, zorder=5))
    # Center zone (was Yd=756–1606) → X=-756 to X=-1606, Yd=0 to Yd=-120
    ax.add_patch(Rectangle((-PANEL_CORNER_YD_R, -PANEL_CENTER_T),
                            PANEL_CENTER_W, PANEL_CENTER_T,
                            fc="#E0D0C0", ec=C_PINHOLE, lw=1.5,
                            alpha=0.6, zorder=5))
    # Far corner zone (was Yd=1606–2362) → X=-1606 to X=-2362, Yd=0 to Yd=-40
    ax.add_patch(Rectangle((-C_WID, -PANEL_CORNER_T),
                            C_WID - PANEL_CORNER_YD_R, PANEL_CORNER_T,
                            fc="#E0D0C0", ec=C_PINHOLE, lw=1.5,
                            alpha=0.6, zorder=5))

    # Light trap drum in open panel center — center of center zone
    # Was at Yd=1181, now at X=-1181, Yd below pinhole wall
    DRUM_OPEN_X = -(PANEL_CORNER_YD_L + PANEL_CORNER_YD_R) / 2  # -1181
    ax.add_patch(Circle((DRUM_OPEN_X, 0), DRUM_R,
                         fc="#FFE8D0", ec=C_PINHOLE, lw=1.2, alpha=0.5,
                         zorder=5, clip_on=True))
    ax.text(DRUM_OPEN_X, -PANEL_CENTER_T - 60,
            f"LIGHT TRAP DRUM\n(in open panel)\nO{DRUM_D}mm",
            color=C_PINHOLE, fontsize=6, ha="center", va="top",
            **FONT, zorder=8)

    # Panel label
    ax.text(-C_WID/2, -PANEL_CENTER_T - 275,
            f"PANEL OPENS 180° OUTWARD  ({C_WID}mm)",
            color=C_PINHOLE, fontsize=8, ha="center", va="top",
            fontweight="bold", **FONT, zorder=8)

    # Hinge pin marker
    ax.plot(0, 0, "o", color=C_PINHOLE, ms=10, zorder=9)
    ax.text(60, -80, "HINGE PIN\nAXIS",
            color=C_PINHOLE, fontsize=6, ha="left", va="top",
            fontweight="bold", **FONT, zorder=9)

    # Swing arc — panel far edge traces 90° from closed (+Yd) to open (-X)
    # Hinge at origin (0,0). Panel far edge at r=C_WID.
    # Closed: far edge at (0, C_WID).  Open: far edge at (-C_WID, 0).
    # In matplotlib angle convention: 90° = +Yd, 180° = -X.
    swing_r = C_WID  # full panel width = actual sweep radius
    swing_arc = Arc((0, 0), 2*swing_r, 2*swing_r,
                    angle=0, theta1=90, theta2=180,
                    color=C_PINHOLE, lw=1.8, ls=(0, (6, 4)),
                    zorder=4, alpha=0.6)
    ax.add_patch(swing_arc)

    # Arrowhead at the open-position end of the arc (near 180° = (-C_WID, 0))
    # Place arrow tangent at ~175° so it points in the sweep direction
    arr_angle = math.radians(175)
    arr_dx = -math.sin(arr_angle) * 40   # tangent direction
    arr_dy =  math.cos(arr_angle) * 40
    ax.annotate("",
                xy=(swing_r * math.cos(arr_angle) + arr_dx,
                    swing_r * math.sin(arr_angle) + arr_dy),
                xytext=(swing_r * math.cos(arr_angle),
                        swing_r * math.sin(arr_angle)),
                arrowprops=dict(arrowstyle="->", color=C_PINHOLE, lw=1.5,
                                mutation_scale=12), zorder=5)

    # Label on the arc midpoint (~135°)
    mid_angle = math.radians(135)
    ax.text(swing_r * math.cos(mid_angle) * 1.08,
            swing_r * math.sin(mid_angle) * 1.08,
            "PANEL TIP\nSWEEP ARC\n(180° outward)",
            color=C_PINHOLE, fontsize=6, ha="center", va="center",
            **FONT, alpha=0.7, zorder=5)

    # Ghost outline: panel in CLOSED position (stepped, at X=0, across Yd)
    ax.add_patch(Rectangle((0, 0), PANEL_CORNER_T, PANEL_CORNER_YD_L,
                            fc="none", ec=C_GHOST, lw=1.2, ls=(0, (4, 3)),
                            alpha=0.5, zorder=4))
    ax.add_patch(Rectangle((0, PANEL_CORNER_YD_L), PANEL_CENTER_T, PANEL_CENTER_W,
                            fc="none", ec=C_GHOST, lw=1.2, ls=(0, (4, 3)),
                            alpha=0.5, zorder=4))
    ax.add_patch(Rectangle((0, PANEL_CORNER_YD_R), PANEL_CORNER_T,
                            C_WID - PANEL_CORNER_YD_R,
                            fc="none", ec=C_GHOST, lw=1.2, ls=(0, (4, 3)),
                            alpha=0.5, zorder=4))
    # Ghost light trap drum in closed position
    ax.add_patch(Circle((0, C_WID/2), DRUM_R,
                         fc="none", ec=C_GHOST, lw=1.0, ls=(0, (4, 3)),
                         alpha=0.35, zorder=4))
    ax.text(PANEL_CENTER_T - 90, C_WID/2 - 50, "PANEL\nCLOSED",
            color=C_GHOST, fontsize=6, ha="left", va="center",
            **FONT, alpha=0.5, zorder=5, rotation=90)

    # ── Fan B penetration ────────────────────────────────────────────────────
    penetration(ax, 0, FAN_B_YD, r=55, col=C_DIM,
                label="FAN B\n(EXHAUST)", label_offset=(0, -22))

    # ── Evap duct penetration (partially visible at right edge) ──────────────
    if EVAP_DUCT_X < X_HI:
        penetration(ax, EVAP_DUCT_X, 0, r=EVAP_DUCT_D / 2, col=C_EVAP,
                    label=f"EVAP DUCT Ø{EVAP_DUCT_D}", label_offset=(0, 70))

    # ── EGRESS PATH ──────────────────────────────────────────────────────────
    # With drums eliminated (rev 5), the full container width is clear for egress.
    # Panel opens outward, door opening at X=0 is fully unobstructed.
    EGRESS_GAP    = C_WID   # full width clear
    EGRESS_MID_Y  = C_WID / 2

    # Egress arrow: from interior, through door to exterior
    ax.annotate("", xy=(-200, EGRESS_MID_Y),
                xytext=(ZONE_L_END - 60, EGRESS_MID_Y),
                arrowprops=dict(arrowstyle="->", color=C_EGRESS, lw=2.8,
                                linestyle=":", mutation_scale=15),
                zorder=10)
    ax.text(ZONE_L_END / 2, EGRESS_MID_Y + 120,
            f"EGRESS PATH — {EGRESS_GAP}mm CLEAR (FULL WIDTH)",
            color=C_EGRESS, fontsize=9, ha="center", va="bottom",
            fontweight="bold", **FONT, zorder=10)

    # Egress gap dimension line
    draw_dim_v(ax, -480, 0, C_WID,
          f"{EGRESS_GAP}mm FULL WIDTH", offset=-30, fs=7, color=C_EGRESS, right=True, font=FONT)

    # ── Clearance summary ────────────────────────────────────────────────────
    note_x = 850
    note_y = EGRESS_MID_Y
    ax.text(note_x, note_y,
            "EGRESS CLEARANCE SUMMARY\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Clear width (full container):   {EGRESS_GAP}mm ({EGRESS_GAP/25.4:.0f}\")\n"
            f"Avg. male shoulder width:   460mm (18\")\n"
            f"Emergency egress min:   610mm (24\")\n"
            f"Standard doorway min:   762mm (30\")\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Margin over emergency min:   {EGRESS_GAP - 610}mm\n"
            "Face-forward egress:   YES\n"
            "Left zone obstructions:   NONE\n\n"
            "PANEL OPENS OUTWARD ONLY\n"
            "Inward blocked by:\n"
            "film plane rails at X=150",
            color=C_OUT, fontsize=6.5, ha="center", va="center",
            **FONT, zorder=10,
            bbox=dict(boxstyle="round,pad=0.5", fc="#F0FFF0",
                      ec=C_EGRESS, lw=1.2))

    # ── Title block (bottom of page, standard format) ─────────────────────
    title_block(ax, "SHEET 2 OF 2",
                drawing_title="CARGO DOOR EGRESS DETAIL",
                subtitle="PANEL OPEN 180° OUTWARD (NO DRUM OBSTRUCTIONS)",
                scale_note="SCALE ~1:25  ·  ALL DIMS IN mm",
                doc_id="TBS-001 · Floor Plan")

    import os; os.makedirs(DIAGRAMS_DIR, exist_ok=True); os.makedirs(SVG_DIR, exist_ok=True)
    out = f"{DIAGRAMS_DIR}/container-floorplan-sheet2.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  {out} saved")


if __name__ == "__main__":
    print("Generating container floor plan...")
    floor_plan()
    egress_detail()
    print("Done.")
