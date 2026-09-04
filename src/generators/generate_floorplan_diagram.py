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
from matplotlib.patches import Rectangle, Circle
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

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DIAGRAM_DPI)
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
            f"IMAGE PLANE / FILM FABRIC  ({FP_W}×{FP_H}mm frame; muslin cut {MUSLIN_CUT_W}×{MUSLIN_CUT_H})  Y={FP_Y}mm",
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
    DRUM_FP_CY = C_WID / 2   # centerd on container Y
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
    # Electrical panel (thin strip at Y=0) — Z=1500–2100 (rev11: dropped 150 for brace-beam clearance)
    equip_rect(ax, EP_X, 0, EP_W, 80, C_ELEC,
               "ELEC\nPANEL", zorder=7, alpha=0.95)
    # Battery bank (slim profile, 120mm depth)
    equip_rect(ax, BA_X, 0, BA_W, BA_D, C_BATT,
               "BATT.", zorder=7, alpha=0.85)

    # ── EQUIPMENT PANEL (IBC plumbing corridor, Yd=1046) ────────────────────
    equip_rect(ax, EQPANEL_X, CORRIDOR_YD_NEAR, EQPANEL_W, CORRIDOR_W,
               C_PUMP, "EQUIP PANEL\n(PUMPS+FILTERS)", label_color="#000000", zorder=7, alpha=0.8)

    # External power panel (penetration box, exterior of pinhole wall)
    PP_DEPTH = 60   # schematic depth of the flange + proud devices on the exterior face
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
               f"IBC-1 BLUE\n1000L (top, ~900L)\nIBC-3 BROWN\n1000L (bottom)\nYd={BLUE_IBC_Y}–{BLUE_IBC_Y+IBC_D}",
               zorder=6)
    ax.text(IBC_COL_X + IBC_W/2, BLUE_IBC_Y + IBC_D - 55,
            "▲ 2336mm tall (2-high)", fontsize=5.5,
            ha="center", va="bottom", **FONT, zorder=7)

    # Far column (Yd=1316–2332): Blue #2 on top, Waste on bottom — 270mm plumbing corridor between columns
    # Plan view sees top tier (Blue #2)
    equip_rect(ax, IBC_COL_X, IBC_FAR_Y, IBC_W, IBC_D, C_BLUE_IBC,
               f"IBC-2 BLUE\n1000L (top, ~900L)\nIBC-4 WASTE\n1000L (bottom)\nYd={IBC_FAR_Y}–{IBC_FAR_Y+IBC_D}",
               zorder=6)
    ax.text(IBC_COL_X + IBC_W/2, IBC_FAR_Y + IBC_D - 55,
            "▲ 2336mm tall (2-high)", fontsize=5.5,
            ha="center", va="bottom", **FONT, zorder=7)

    # ── Wall penetrations ─────────────────────────────────────────────────────
    # Fan A — EXHAUST: sealed end wall (X=C_LEN), Yd=FAN_A_YD=1181mm (below X1, in plumbing corridor), H=FAN_A_H=2000mm
    penetration(ax, C_LEN, FAN_A_YD, r=55, col=C_DIM, label="FAN\nOUT", label_offset=(130, -30))
    # Fan B — INTAKE: cargo door panel (X=0), near pinhole wall / near corner zone (Yd=FAN_B_YD=365mm, rev9/B2 swap), LOW (H=600mm)
    penetration(ax, 0, FAN_B_YD, r=55, col=C_DIM, label="FAN\nIN", label_offset=(-130, -30))

    # ── Hinged panel — transport position (ghost, SWUNG ~56° about the pivot) ──
    # rev10: the panel + punch-out bay + drum REVOLVE about the vertical Ø89 pivot
    # post (PIVOT_X, PIVOT_YD = the film far-left upright) to clear the cargo doors.
    # The old "slide 300mm on HGR20 ceiling rails" ghost is retired. The fixed strips
    # (Yd 0–PANEL_CUT_YD near, FAR_STRIP_YD0–C_WID far) do NOT swing. Drawn faint so
    # the swept footprint reads against the operational equipment (swing-clearance check).
    GHOST_LS = (0, (6, 4))
    GHOST_A  = 0.30

    def _rot(x, y, deg):
        t = np.radians(deg); c, s = np.cos(t), np.sin(t)
        return (PIVOT_X + (x - PIVOT_X) * c - (y - PIVOT_YD) * s,
                PIVOT_YD + (x - PIVOT_X) * s + (y - PIVOT_YD) * c)
    _L = SWING_LOCK_DEG
    # swung panel center section (Yd PANEL_CUT_YD..FAR_STRIP_YD0)
    _panel = [_rot(0, PANEL_CUT_YD, _L), _rot(PANEL_CENTER_T, PANEL_CUT_YD, _L),
              _rot(PANEL_CENTER_T, FAR_STRIP_YD0, _L), _rot(0, FAR_STRIP_YD0, _L)]
    ax.add_patch(matplotlib.patches.Polygon(_panel, closed=True, fc="none",
                 ec=C_DIM, lw=1.0, ls=GHOST_LS, zorder=4, alpha=GHOST_A))
    # swung punch-out bay (Yd PANEL_CORNER_YD_L..R, front face at BAY_FRONT_X)
    _bay = [_rot(BAY_FRONT_X, PANEL_CORNER_YD_L, _L), _rot(0, PANEL_CORNER_YD_L, _L),
            _rot(0, PANEL_CORNER_YD_R, _L), _rot(BAY_FRONT_X, PANEL_CORNER_YD_R, _L)]
    ax.add_patch(matplotlib.patches.Polygon(_bay, closed=True, fc="none",
                 ec=C_DIM, lw=1.0, ls=GHOST_LS, zorder=4, alpha=GHOST_A))
    # swung drum (center in the bay at DRUM_CX)
    _dctr = _rot(DRUM_CX, C_WID / 2, _L)
    ax.add_patch(Circle(_dctr, DRUM_R, fc="none", ec=C_DIM, lw=1.0,
                        ls=GHOST_LS, zorder=4, alpha=GHOST_A))
    ax.text(_dctr[0], _dctr[1], "PANEL + DRUM\n(SWUNG 56°,\nTRANSPORT)",
            color=C_DIM, fontsize=5.5, ha="center", va="center", **FONT,
            alpha=0.5, zorder=5)
    # pivot post marker
    ax.add_patch(Circle((PIVOT_X, PIVOT_YD), 45, fc="none", ec=C_DIM, lw=1.2,
                        zorder=5, alpha=0.7))
    ax.text(PIVOT_X + 75, PIVOT_YD, "PIVOT Ø89", color=C_DIM, fontsize=5,
            ha="left", va="center", **FONT, alpha=0.55, zorder=5)
    # rotation arc traced by the bay front-right corner (operational 0° → transport 56°)
    _arc = [_rot(BAY_FRONT_X, PANEL_CORNER_YD_R, dd) for dd in np.linspace(0, _L, 24)]
    ax.plot([p[0] for p in _arc], [p[1] for p in _arc], color=C_DIM, lw=0.7,
            ls=GHOST_LS, alpha=0.5, zorder=4)
    _mid = _arc[len(_arc) // 2]
    ax.text(_mid[0] - 30, _mid[1], f"SWING {int(_L)}°", ha="right", va="center",
            color=C_DIM, fontsize=5, **FONT, alpha=0.55, zorder=5)

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
        (C_ALUM,     "Ext power panel (penetration box, exterior)"),
    ], 0, leg_y_top, cols=3, col_w=1900, font=FONT, zorder=8)

    # ── Film left-rail demountable segment (drum-mode clearance) ─────────────
    # The LEFT RAIL (X=RAIL_X_L=150mm) passes through the drum volume.
    # B2 (rev9): the left rail is CONTINUOUS — the drum is offset out (center
    # X=DRUM_CX, via the hinge-panel punch-out bay), so no demountable segment.
    NOTE_NX = -PAD_L + 120
    NOTE_NY = DRUM_CY   # 1181 — light-lock Yd center
    ax.annotate("",
                xy=(RAIL_X_L, NOTE_NY),
                xytext=(NOTE_NX + 600, NOTE_NY),
                arrowprops=dict(arrowstyle="->", color="#7A3A00", lw=1.0),
                zorder=10)
    ax.text(NOTE_NX + 400, NOTE_NY - 380,
            f"FILM LEFT RAIL CONTINUOUS — full travel\n"
            f"Drum offset to X={DRUM_CX}mm via the panel bay\n— clears the X={RAIL_X_L}mm rail",
            ha="right", va="bottom", fontsize=6.0, color="#7A3A00",
            fontweight="bold", **FONT, zorder=10,
            bbox=dict(boxstyle="round,pad=0.3", fc="#FFFBE6", ec="#7A3A00", lw=0.9))

    # ── Left walkway — removable lift-out overlay + label ─────────────────────
    # The LEFT walkway (X WALKWAY_LEFT_X–470, full Yd span) is a removable
    # lift-out panel — removed only for transport so the light-trap cargo panel
    # + drum can swing ~56° about the pivot.  Highlight with a dashed green border.
    ax.add_patch(Rectangle((LX, NY), W, FYO - NY,
                            fc="none", ec="#408040", lw=2.0, ls=(0, (6, 3)),
                            zorder=13, alpha=0.85))
    # Drum-exit punch-out — deeper landing (X 470–770) in front of the light-lock exit.
    ax.add_patch(Rectangle((LXR, WALKWAY_LEFT_WIDE_YD_L),
                            WALKWAY_LEFT_WIDE_W - W,
                            WALKWAY_LEFT_WIDE_YD_R - WALKWAY_LEFT_WIDE_YD_L,
                            fc="#DCEEDC", ec="#408040", lw=1.8, ls=(0, (5, 3)),
                            zorder=13, alpha=0.7))
    ax.text(LXR + (WALKWAY_LEFT_WIDE_W - W) / 2,
            (WALKWAY_LEFT_WIDE_YD_L + WALKWAY_LEFT_WIDE_YD_R) / 2,
            "DRUM-EXIT\nPUNCH-OUT\n600mm", ha="center", va="center", fontsize=5.5,
            color="#204820", fontweight="bold", **FONT, zorder=14)
    # Leader pointing to left walkway mid-height
    LW_MID_Y = (NY + FYO) / 2
    LW_NOTE_X = -PAD_L + 120
    ax.annotate("",
                xy=(LXR, LW_MID_Y),
                xytext=(LW_NOTE_X + 520, LW_MID_Y),
                arrowprops=dict(arrowstyle="->", color="#408040", lw=1.0),
                zorder=14)
    ax.text(LW_NOTE_X + 400, LW_MID_Y + 200,
            f"LEFT WALKWAY — REMOVABLE LIFT-OUT\n"
            f"X={WALKWAY_LEFT_X}–{int(LXR)}mm\n"
            "Remove for transport (panel+drum swing 56°)",
            ha="right", va="bottom", fontsize=6.0, color="#204820",
            fontweight="bold", **FONT, zorder=14,
            bbox=dict(boxstyle="round,pad=0.3", fc="#F0FFF0", ec="#408040", lw=0.9))

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

    out = f"{DIAGRAMS_DIR}/container-floorplan.png"
    fig.savefig(out, dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  {out} saved")


if __name__ == "__main__":
    print("Generating container floor plan...")
    floor_plan()
    print("Done.")
