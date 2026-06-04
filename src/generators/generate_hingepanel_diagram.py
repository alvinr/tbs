#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_hingepanel_diagram.py  —  TBS-001 Hinged Light-Trap Panel

Sheet 1 — Front elevation (exterior view, 1:20):
  Panel dimensions, revolving drum position, hinges, latches, EPDM perimeter seal.
  Stepped profile: 40mm corner zones, 120mm center zone (drum housing).

Sheet 2 — Plan cross-section (1:20 equal aspect):
  Panel thickness (center zone), drum cross-section with 4 baffles, S-path
  light route, container wall interface, EPDM gasket engagement, latch detail.

Sheet 3 — Drum vertical section:
  Drum elevation showing walking height, bearings, person silhouette.

Sheet 4 — Sliding rail transport system:
  HGR20 panel carriage, V-groove drum dollies, fixed door frame,
  operational vs transport positions.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Arc, Polygon, Ellipse, Wedge
from matplotlib.lines import Line2D
import os
from tbs_constants import (
    C_LT_DRUM,
    WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T,
    WALKWAY_BRACKET_H, WALKWAY_BRACKET_T,
    DIAGRAMS_DIR,
    DRUM_D as LT_HOUSING_D,                       # Ø900 fixed housing OD (rev8)
    PANEL_CORNER_YD_L, PANEL_CORNER_YD_R,         # widened center-zone step lines
    LT_DRUM_OR, LT_OPENING_DEG,
    RAIL_X_L, BRACE_LEFT_DEMOUNT_Y0, BRACE_LEFT_DEMOUNT_Y1,   # film-plane left rail
    FP_Y_MIN, FP_Y, PANEL_SLIDE, PANEL_CENTER_T,
)
from tbs_title_block import title_block
from tbs_drawing import (draw_dim_h, draw_dim_v,
                         leader as _leader_shared, hatch_rect, draw_notes,
                         draw_legend)

# ── Palette (white engineering) ───────────────────────────────────────────────
BG      = "#FFFFFF"   # white background
C_OUT   = "#1A1A1A"   # outlines
C_CL    = "#2060A0"   # centre lines (blue, dashed)
C_DIM   = "#404040"   # dimensions / annotation text
C_ALUM  = "#C8D8E8"   # aluminium / ply fill
C_STEEL = "#B0B0B8"   # steel section fill
C_GASKT = "#5A3020"   # EPDM gasket fill
C_LIGHT = "#FFE0A0"   # light-path indication (amber)
FONT    = {"fontfamily": "monospace"}

# ── Panel dimensions (mm) ─────────────────────────────────────────────────────
PW = 2362   # panel width  (= container interior short-axis width)
PH = 2388   # panel height (= container interior height)
PT = 120    # panel overall thickness (50×50 RHS frame + 18mm ply each face)

# Light-trap housing (rev8: housed revolving door — see tbs_constants)
DRUM_D  = LT_HOUSING_D  # = 900mm fixed housing outer diameter
DRUM_R  = DRUM_D / 2   # = 450mm housing radius
DRUM_H  = 2200          # housing/drum height (floor → top bearing, mm)
DRUM_CX = PW / 2        # light-lock centre X in panel (centred horizontally)
DRUM_CY = DRUM_H / 2   # light-lock centre Y

# ── Drawing helpers (wrappers around tbs_drawing shared functions) ────────────
def dim_h(ax, x0, x1, y, label, offset=70, fs=7, col=C_DIM):
    draw_dim_h(ax, x0, x1, y, label, offset=offset, fs=fs, color=col, font=FONT)

def dim_v(ax, x, y0, y1, label, offset=70, fs=7, col=C_DIM):
    draw_dim_v(ax, x, y0, y1, label, offset=offset, fs=fs, right=True,
               color=col, font=FONT)

def leader(ax, xy, xytext, text, col=C_DIM, fs=6.5, fw="normal"):
    font = dict(FONT)
    if fw != "normal":
        font["fontweight"] = fw
    _leader_shared(ax, xy[0], xy[1], xytext[0], xytext[1], text,
                   fs=fs, color=col, ha="center", va="center",
                   arrow_style="-|>", font=font)



# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1  —  Front Elevation (Exterior View)
# X = panel width (0 → 2362mm),  Y = panel height (0 → 2388mm)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():
    fig, ax = plt.subplots(figsize=(18, 14))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    PAD_L = 550; PAD_R = 650; PAD_B = 500; PAD_T = 450
    ax.set_xlim(-PAD_L, PW + PAD_R)
    ax.set_ylim(-PAD_B, PH + PAD_T)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Panel body ────────────────────────────────────────────────────────────
    # Outer steel frame (50mm wide)
    ax.add_patch(Rectangle((0, 0), PW, PH, fc=C_STEEL, ec=C_OUT, lw=2.5, zorder=2))
    # Ply skin area (inset of frame, shown slightly lighter)
    FR = 55  # visible frame width at face
    ax.add_patch(Rectangle((FR, FR), PW - 2 * FR, PH - 2 * FR,
                            fc=C_ALUM, ec=C_OUT, lw=0.8, zorder=3))
    ax.text(PW / 4 - 275, PH / 2,
            "18mm EXT-GRADE PLY\nFLAT BLACK INTERIOR",
            color=C_DIM, fontsize=6.5, ha="center", va="center", **FONT, zorder=15, alpha=0.7)

    # ── EPDM perimeter seal (dashed inner contour) ────────────────────────────
    S = 30  # seal inset
    epdm = plt.Polygon([(S, S), (PW - S, S), (PW - S, PH - S), (S, PH - S)],
                       closed=True, fill=False, ec=C_GASKT, lw=2.0, ls=(0, (4, 3)),
                       zorder=5)
    ax.add_patch(epdm)

    # ── Stepped profile zone transitions (rev 4) ────────────────────────────
    # Corner zones: 40mm thick.  Center zone: 120mm thick (drum housing).
    STEP_YD_L = PANEL_CORNER_YD_L   # 653 (rev8 widened)
    STEP_YD_R = PANEL_CORNER_YD_R  # 1709
    for sx in [STEP_YD_L, STEP_YD_R]:
        ax.plot([sx, sx], [0, PH], color="#C04010", lw=1.2,
                ls=(0, (6, 3)), zorder=4, alpha=0.8)
    # Zone labels (positioned between step lines and panel edges)
    ax.text(STEP_YD_L / 2, PH - 120,
            "40mm\nCORNER\nZONE", color="#C04010", fontsize=6,
            ha="center", va="top", fontweight="bold", **FONT, zorder=15, alpha=0.7)
    ax.text((STEP_YD_L + STEP_YD_R) / 2, PH - 220,
            "120mm\nCENTER ZONE\n(DRUM HOUSING)", color="#C04010", fontsize=6,
            ha="center", va="top", fontweight="bold", **FONT, zorder=15, alpha=0.7)
    ax.text((STEP_YD_R + PW) / 2, PH - 120,
            "40mm\nCORNER\nZONE", color="#C04010", fontsize=6,
            ha="center", va="top", fontweight="bold", **FONT, zorder=15, alpha=0.7)
    # Step dimension
    dim_h(ax, STEP_YD_L, STEP_YD_R, -210,
          f"{STEP_YD_R - STEP_YD_L}mm CENTER ZONE (DRUM Ø{DRUM_D} + 50mm CLEARANCE EACH SIDE)", offset=20)

    # ── Revolving drum ────────────────────────────────────────────────────────
    DX = DRUM_CX - DRUM_R   # drum left edge in panel
    DY_BOT = 100             # drum bottom clearance from panel bottom edge
    DY_TOP = DY_BOT + DRUM_H  # = 2100

    BRG_H = 45  # bearing housing height

    # Top + bottom bearing housings
    for by, label in [(DY_BOT, "LOWER BEARING"), (DY_TOP - BRG_H, "UPPER BEARING")]:
        ax.add_patch(Rectangle((DX - 35, by), DRUM_D + 70, BRG_H,
                                fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=6))
        ax.text(DRUM_CX, by + BRG_H / 2, f"SKF 6215  {label}",
                color=C_OUT, fontsize=5.5, ha="center", va="center", **FONT, zorder=15)

    # Drum body (shown as tall rectangle in elevation)
    drum_body_y0 = DY_BOT + BRG_H
    drum_body_h  = DRUM_H - 2 * BRG_H
    ax.add_patch(Rectangle((DX, drum_body_y0), DRUM_D, drum_body_h,
                            fc=C_LT_DRUM, ec=C_OUT, lw=2.0, zorder=5))

    # Arc lines indicating cylindrical form (top and bottom ellipses in elevation)
    for arc_y, angle1, angle2 in [(drum_body_y0, 0, 180), (drum_body_y0 + drum_body_h, 180, 360)]:
        arc = Arc((DRUM_CX, arc_y), DRUM_D, 60,
                  angle=0, theta1=angle1, theta2=angle2,
                  color=C_OUT, lw=1.2, zorder=7)
        ax.add_patch(arc)

    # Drum centre line (vertical)
    ax.plot([DRUM_CX, DRUM_CX], [DY_BOT - 80, DY_TOP + 80],
            color=C_CL, lw=0.9, ls="--", zorder=6)
    ax.text(DRUM_CX, DY_TOP + 110, "CL", color=C_CL, fontsize=7,
            ha="center", va="bottom", **FONT, zorder=15)

    # Rotation arrows (inside drum body)
    for ry_offset in [-350, 0, 350]:
        ry = drum_body_y0 + drum_body_h / 2 + ry_offset
        ax.annotate("", xy=(DRUM_CX + DRUM_R * 0.6, ry + 120),
                    xytext=(DRUM_CX + DRUM_R * 0.6, ry - 120),
                    arrowprops=dict(arrowstyle="->", color=C_DIM, lw=0.9,
                                    connectionstyle="arc3,rad=0.5", mutation_scale=8))

    ax.text(DRUM_CX + DRUM_R * 0.6 + 70,
            drum_body_y0 + drum_body_h / 2,
            "DRUM\nROTATES", color=C_DIM, fontsize=6,
            ha="left", va="center", **FONT, zorder=15)

    # Handle bar — interior face only, shown as hidden (dashed) line inside drum body.
    # The handle is on the inner curved surface of the drum; from the exterior elevation
    # it is fully hidden behind the exterior drum wall — shown dashed per convention.
    HY = DY_BOT + DRUM_H * 0.45   # handle Y centre (~900mm)
    HW = 110; HH = 42  # handle footprint
    # Place handle inside the drum body rectangle, 20mm clear of the interior drum wall.
    hx_handle = DX + DRUM_D - HW - 20
    ax.add_patch(Rectangle((hx_handle, HY - HH / 2), HW, HH,
                            fc="none", ec=C_OUT, lw=1.2, ls=(0, (4, 3)), zorder=7))
    leader(ax, (hx_handle + HW / 2, HY), (DX + DRUM_D + 300, HY + 300),
           "100mm PULL HANDLE\n(INTERIOR FACE — HIDDEN)\nWelded bracket\nno through-hole")

    # ── Hinges (3 × left edge from exterior view) ────────────────────────────
    HINGE_YS = [220, 1190, PH - 230]
    HINGE_W = 85; HINGE_L = 220
    for hy in HINGE_YS:
        # Hinge leaf (exterior face)
        ax.add_patch(Rectangle((-HINGE_W, hy - HINGE_L // 2), HINGE_W, HINGE_L,
                                fc=C_ALUM, ec=C_OUT, lw=1.2, zorder=6))
        ax.add_patch(Circle((-HINGE_W / 2, hy), 22, fc=C_OUT, ec=BG, lw=0.8, zorder=7))
        # Extension line to hinge pin axis
        ax.plot([-HINGE_W / 2, -HINGE_W / 2], [hy - 8, hy + 8],
                color=BG, lw=1.5, zorder=8)

    # Hinge pin axis line
    ax.plot([-HINGE_W / 2, -HINGE_W / 2], [-60, PH + 80],
            color=C_CL, lw=0.9, ls="--", zorder=4)
    ax.text(-HINGE_W / 2, PH + 100, "HINGE PIN AXIS — 180° SWING",
            color=C_CL, fontsize=6.5, ha="center", va="bottom", **FONT, zorder=15)

    leader(ax, (-HINGE_W / 2, HINGE_YS[1]),
           (-HINGE_W - 280, HINGE_YS[1] + 300),
           "3 × 200mm S.S.\nBALL-BEARING PIANO HINGE")

    # ── Sliding carriage system ─────────────────────────────────────────────
    # The entire panel slides 300mm in the X direction (into the container)
    # on HGR20 linear rails mounted to both container walls at floor and
    # ceiling level. Rails run parallel to the container long walls.
    #
    # LEFT (hinge) side: carriage beam (60×60mm SHS) rides on rails,
    #   panel hinges mount to this beam.
    # RIGHT (latch) side: panel frame rides on rails via carriage blocks,
    #   no separate beam needed — the panel RHS frame provides rigidity.
    C_RAIL = "#CC4422"   # red, matching assembly overview
    C_CARR = "#C04010"   # carriage beam color
    RAIL_H = 20          # rail cross-section height (visible in elevation)
    RAIL_LEN = 350       # visible rail length (extends behind panel, into page)

    # ── LEFT SIDE — carriage beam + rails ────────────────────────────────
    CBEAM_W = 60
    CBEAM_X = -HINGE_W - CBEAM_W   # left of hinges (behind panel)
    ax.add_patch(Rectangle((CBEAM_X, 0), CBEAM_W, PH,
                            fc="none", ec=C_CARR, lw=1.5,
                            ls=(0, (5, 3)), zorder=3, alpha=0.6))
    ax.text(CBEAM_X + CBEAM_W / 2, PH / 2,
            "CARRIAGE BEAM 60×60mm SHS",
            color=C_CARR, fontsize=5, ha="center", va="center",
            **FONT, zorder=15, alpha=0.6, rotation=90)

    # Left floor rail
    ax.add_patch(Rectangle((CBEAM_X - RAIL_LEN / 2, -10), RAIL_LEN, RAIL_H,
                            fc=C_RAIL, ec=C_OUT, lw=0.8, alpha=0.5, zorder=3))
    ax.text(CBEAM_X - RAIL_LEN / 2 - 15, -30 + RAIL_H / 2,
            "HGR20 FLOOR\nRAIL (500mm)",
            color=C_RAIL, fontsize=5.5, ha="right", va="center",
            **FONT, zorder=15)
    # Left ceiling rail
    ax.add_patch(Rectangle((CBEAM_X - RAIL_LEN / 2, PH - 10), RAIL_LEN, RAIL_H,
                            fc=C_RAIL, ec=C_OUT, lw=0.8, alpha=0.5, zorder=3))
    ax.text(CBEAM_X - RAIL_LEN / 2 - 15, PH - 10 + RAIL_H / 2,
            "HGR20 CEILING\nRAIL (500mm)",
            color=C_RAIL, fontsize=5.5, ha="right", va="center",
            **FONT, zorder=15)

    # Left slide direction arrow
    arr_y = -80
    ax.annotate("", xy=(CBEAM_X - 120, arr_y), xytext=(CBEAM_X + 120, arr_y),
                arrowprops=dict(arrowstyle="<->", color=C_RAIL, lw=1.2,
                                mutation_scale=10), zorder=15)
    ax.text(CBEAM_X, arr_y - 40, "300mm SLIDE\n(X-DIRECTION)",
            ha="center", va="top", fontsize=5.5, color=C_RAIL,
            fontweight="bold", **FONT, zorder=15)

    # ── RIGHT SIDE — guide rails (panel frame rides directly on blocks) ──
    RSIDE_X = PW + 30   # right side guide position (just past panel right edge)

    # Right floor rail
    ax.add_patch(Rectangle((RSIDE_X - RAIL_LEN / 2, -10), RAIL_LEN, RAIL_H,
                            fc=C_RAIL, ec=C_OUT, lw=0.8, alpha=0.5, zorder=3))
    ax.text(RSIDE_X + RAIL_LEN / 2 + 15, -10 + RAIL_H / 2,
            "HGR20 FLOOR\nRAIL (500mm)",
            color=C_RAIL, fontsize=5.5, ha="left", va="center",
            **FONT, zorder=15)
    # Right ceiling rail
    ax.add_patch(Rectangle((RSIDE_X - RAIL_LEN / 2, PH - 10), RAIL_LEN, RAIL_H,
                            fc=C_RAIL, ec=C_OUT, lw=0.8, alpha=0.5, zorder=3))
    ax.text(RSIDE_X + RAIL_LEN / 2 + 15, PH - 10 + RAIL_H / 2,
            "HGR20 CEILING\nRAIL (500mm)",
            color=C_RAIL, fontsize=5.5, ha="left", va="center",
            **FONT, zorder=15)

    # Right slide direction arrow
    ax.annotate("", xy=(RSIDE_X - 120, arr_y), xytext=(RSIDE_X + 120, arr_y),
                arrowprops=dict(arrowstyle="<->", color=C_RAIL, lw=1.2,
                                mutation_scale=10), zorder=15)
    ax.text(RSIDE_X, arr_y - 50, "300mm SLIDE\n(X-DIRECTION)",
            ha="center", va="top", fontsize=5.5, color=C_RAIL,
            fontweight="bold", **FONT, zorder=15)

    # ── Southco C2-33 cam latches (4 corners) — INTERIOR FACE ───────────────
    # Latches are mounted on the INTERIOR face of the panel.
    # From this exterior view they are hidden features — shown dashed per
    # engineering convention for features on the far/hidden face.
    # Interior mounting enables emergency egress: if the revolving drum jams,
    # operators inside the container can release the latches and push the panel
    # open outward without requiring access to the exterior face.
    LATCH_XS = [210, PW - 210]
    LATCH_YS = [220, PH - 220]
    for lx in LATCH_XS:
        for ly in LATCH_YS:
            ax.add_patch(Rectangle((lx - 35, ly - 35), 70, 70,
                                    fc="none", ec=C_DIM, lw=0.9,
                                    ls=(0, (4, 2)), zorder=6))
            ax.plot([lx - 22, lx + 22], [ly - 22, ly + 22],
                    color=C_DIM, lw=0.9, ls=(0, (4, 2)), zorder=7)
            ax.plot([lx - 22, lx + 22], [ly + 22, ly - 22],
                    color=C_DIM, lw=0.9, ls=(0, (4, 2)), zorder=7)
    leader(ax, (LATCH_XS[1], LATCH_YS[0]),
           (PW + 430, LATCH_YS[0]),
           "SOUTHCO C2-33 CAM LATCH (×4)\nINTERIOR FACE — shown dashed\nEMERGENCY EGRESS:\noperate from inside if drum jams")

    # ── Outward-opening annotation ────────────────────────────────────────────
    # Panel hinges on left (X=0); right edge is the free edge.
    # Opens outward — away from interior camera equipment.
    leader(ax, (PW, PH * 0.36),
           (PW + 275, PH * 0.36),
           "OPENS OUTWARD\n(180° SWING —\nCLEAR OF INTERIOR\nEQUIPMENT)",
           col="#204080", fw="bold")
#     ax.annotate("",
#                 xy=(PW + 55, PH * 0.36),
#                 xytext=(PW, PH * 0.36),
#                 arrowprops=dict(arrowstyle="-|>", color="#204080", lw=1.3,
#                                 mutation_scale=9))
#     ax.text(PW + 175, PH * 0.36 -55,
#             "OPENS OUTWARD\n(180° SWING —\nCLEAR OF INTERIOR\nEQUIPMENT)",
#             color="#204080", fontsize=6.5, ha="left", va="bottom",
#             fontweight="bold", **FONT, zorder=15)

    # ── Emergency egress safety note ──────────────────────────────────────────
    ax.text(PW / 2, -280,
            "SAFETY: Interior-mounted cam latches (×4) allow emergency panel release from inside — "
            "operate if revolving drum jams. Panel opens outward, clear of all equipment.",
            color="#C04010", fontsize=6.5, ha="center", va="center",
            fontweight="bold", **FONT, zorder=15)

    # ── EPDM seal leader ─────────────────────────────────────────────────────
    leader(ax, (PW - S, PH / 2),
           (PW + 320, PH / 2 + 300),
           "20mm EPDM GASKET\nIN ALUMINIUM CHANNEL\n(PERIMETER, ALL SIDES)")

    # ── Dimension lines ───────────────────────────────────────────────────────
    # Panel width
    dim_h(ax, 0, PW, PH + 200, f"{PW}mm  (CONTAINER INTERIOR WIDTH)", offset=20)
    # Panel height
    dim_v(ax, PW + 75, 0, PH, f"{PH}mm", offset=-25)
    # Drum diameter
    dim_h(ax, DX, DX + DRUM_D, DY_TOP + 170, f"Ø{DRUM_D}mm DRUM", offset=20)
    # Drum clear height
    dim_v(ax, DX - 200, DY_BOT, DY_TOP, f"{DRUM_H}mm\nCLEAR HEIGHT", offset=25)
    # Drum centre from left
    dim_h(ax, 0, DRUM_CX, DY_BOT - 180, f"{int(DRUM_CX)}mm  (PANEL CL — CENTRED)", offset=-50)
    # Hinge positions from floor
    for hy in HINGE_YS:
        ax.plot([-HINGE_W - 10, -HINGE_W - 80], [hy, hy],
                color=C_DIM, lw=0.6, ls="--", zorder=3)
        ax.text(-HINGE_W - 90, hy, f"{hy}", color=C_DIM, fontsize=6,
                ha="right", va="center", **FONT, zorder=15)
    hinge_2_flr = round(HINGE_YS[0] - HINGE_L/2)
    dim_v(ax, -HINGE_W - 100, hinge_2_flr, HINGE_YS[0] - HINGE_L, f"HINGE CL HEIGHT\nFROM FLOOR {hinge_2_flr}mm", offset=-320)

#     ax.text(-HINGE_W - 80, 90, "HINGE CL HEIGHT\nFROM FLOOR (mm)",
#             color=C_DIM, fontsize=6, ha="right", va="top", **FONT, zorder=15)

    # ── Section A-A cut indicator (at H=1000mm — corresponds to Sheet 2 plan cut)
    AA_H = 1000   # height of plan section cut
    ax.plot([-PAD_L, PW + PAD_R], [AA_H, AA_H],
            color=C_CL, lw=0.8, ls=(0, (10, 4, 2, 4)), zorder=4, alpha=0.7)
    ax.text(-PAD_L + 20, AA_H + 40, "A", color=C_CL, fontsize=9,
            fontweight="bold", ha="left", va="bottom", **FONT, zorder=15)
    ax.text(-PAD_L + 20, AA_H - 40, "A", color=C_CL, fontsize=9,
            fontweight="bold", ha="left", va="top", **FONT, zorder=15)
    ax.text(PW + PAD_R - 20, AA_H + 40, "A", color=C_CL, fontsize=9,
            fontweight="bold", ha="right", va="bottom", **FONT, zorder=15)
    ax.text(PW + PAD_R - 20, AA_H - 40, "A", color=C_CL, fontsize=9,
            fontweight="bold", ha="right", va="top", **FONT, zorder=15)
    ax.text(PW / 2, AA_H - 30,
            "SECTION A-A  (Plan cross-section — Sheet 2)",
            color=C_CL, fontsize=6.5, ha="center", va="bottom", **FONT, alpha=0.8, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 6",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="FRONT ELEVATION — EXTERIOR VIEW",
                scale_note="SCALE 1:20",
                doc_id="TBS-001 \u00b7 Hinged Light-Trap Panel")

    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet1.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet1.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2  —  Plan Cross-Section at drum mid-height (looking down)
# Equal aspect — all coordinates in real mm.
# X = panel width direction.
# Y = depth direction (0 = container exterior face, positive into container).
#
# NOTE: This section cuts through the CENTER ZONE (120mm thick) of the
# stepped panel.  Corner zones (Yd=0-756 and Yd=1606-2362) are only 40mm
# thick — see Sheet 1 for the step transition locations.
#
# The drum (Ø750mm) is much larger than the panel depth (120mm + 40mm wall).
# In plan, the drum circle overhangs both panel faces — this is physically
# correct: the drum is secured by top/bottom bearings, not by the panel depth.
# The plan section shows this clearly.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():
    # ── Key dimensions (mm) ──────────────────────────────────────────────────
    WALL_T = 40     # container end-wall steel thickness
    PLY_T  = 18     # ply skin thickness (each face)
    PT     = 120    # panel overall thickness (frame + 2 × ply)
    FRAME_T = PT - 2 * PLY_T   # = 84mm RHS frame depth

    # Y positions (from exterior face of container wall)
    Y0_W  = 0            # exterior face
    Y1_W  = WALL_T       # = 40  (inner face of wall / outer face of panel)
    Y0_PL = Y1_W         # outer ply starts
    Y1_PL = Y1_W + PLY_T # = 58
    Y0_FR = Y1_PL        # frame starts = 58
    Y1_FR = Y0_FR + FRAME_T  # = 142
    Y0_PL2 = Y1_FR       # inner ply = 142
    Y1_PL2 = Y0_PL2 + PLY_T  # = 160  (panel inner face)

    Y_EXT = Y0_W         # exterior face = 0
    Y_INT = Y1_PL2       # interior face = 160

    # Drum geometry — axis is vertical; plan section shows horizontal circle
    D_CX = PW / 2        # drum centre X: centred in panel width = 1181mm
    D_CY = (Y_EXT + Y_INT) / 2   # drum centre Y: centre of wall+panel depth = 80mm
    DR   = DRUM_R        # = 375mm

    # Drum Y extents
    D_YB = D_CY - DR     # exterior overhang bottom = 80 - 375 = -295mm
    D_YT = D_CY + DR     # interior overhang top    = 80 + 375 = 455mm

    # Drum X extents
    D_XL = D_CX - DR    # = 806mm
    D_XR = D_CX + DR    # = 1556mm

    # ── View window — full panel width + margins ────────────────────────────
    # Corner zone thicknesses
    CORNER_T = 40   # corner zone panel thickness
    STEP_YD_L = PANEL_CORNER_YD_L   # 653 (rev8 widened)
    STEP_YD_R = PANEL_CORNER_YD_R  # 1709

    PAD_X  = 450   # horizontal margin each side (room for rails + labels)
    PAD_YB = 350   # bottom margin (exterior zone)
    PAD_YT = 220   # top margin (interior zone)

    X_LO = -PAD_X                # left of panel
    X_HI = PW + PAD_X            # right of panel
    Y_LO = D_YB - PAD_YB         # below drum exterior overhang
    Y_HI = D_YT + PAD_YT         # above drum interior overhang

    FIG_W = 22.0
    FIG_H = FIG_W * (Y_HI - Y_LO) / (X_HI - X_LO)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Y_LO, Y_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Background zones ──────────────────────────────────────────────────────
    # Exterior zone (Y < 0)
    ax.add_patch(Rectangle((X_LO, Y_LO), X_HI - X_LO, Y_EXT - Y_LO,
                            fc="#EEF2F8", ec="none", zorder=1))
    ax.text(D_CX - PAD_X / 2 - 450, (Y_LO + Y_EXT) / 2 - 125,
            "EXTERIOR", color="#5060A0", fontsize=9, ha="center", va="center",
            **FONT, fontweight="bold", alpha=0.55, zorder=15)

    # Interior zone (Y > Y_INT)
    ax.add_patch(Rectangle((X_LO, Y_INT), X_HI - X_LO, Y_HI - Y_INT,
                            fc="#EEF6EE", ec="none", zorder=1))
    ax.text(D_CX - PAD_X / 2 - 450, (Y_INT + Y_HI) / 2 + 125,
            "INTERIOR", color="#407040", fontsize=9, ha="center", va="center",
            **FONT, fontweight="bold", alpha=0.55, zorder=15)

    # ── Container end-wall cross-section (Y=0→40) — full width ────────────────
    # Continuous wall except for the drum opening
    ax.add_patch(Rectangle((0, Y0_W), D_XL, WALL_T,
                            fc=C_STEEL, ec=C_OUT, lw=1.0, hatch="///", zorder=3))
    ax.add_patch(Rectangle((D_XR, Y0_W), PW - D_XR, WALL_T,
                            fc=C_STEEL, ec=C_OUT, lw=1.0, hatch="///", zorder=3))

    # ── CENTER ZONE panel (120mm thick, Yd=756→1606) ─────────────────────────
    # Outer ply, frame, inner ply — between drum opening edges and step lines
    for x, w in [(STEP_YD_L, D_XL - STEP_YD_L), (D_XR, STEP_YD_R - D_XR)]:
        ax.add_patch(Rectangle((x, Y0_PL), w, PLY_T,
                                fc=C_ALUM, ec=C_OUT, lw=0.8, zorder=3))
        ax.add_patch(Rectangle((x, Y0_FR), w, FRAME_T,
                                fc=C_STEEL, ec=C_OUT, lw=0.8, hatch="\\\\", zorder=3))
        ax.add_patch(Rectangle((x, Y0_PL2), w, PLY_T,
                                fc=C_ALUM, ec=C_OUT, lw=0.8, zorder=3))

    # ── CORNER ZONES (40mm thick, Yd=0→756 and Yd=1606→2362) ─────────────────
    # Corner zones: 18mm ply + 4mm steel plate + 18mm ply = 40mm
    CORN_PLY   = 18
    CORN_PLATE = 4
    CORN_Y0_PL  = Y1_W                          # outer ply starts at wall inner face
    CORN_Y1_PL  = CORN_Y0_PL + CORN_PLY          # = 58
    CORN_Y0_ST  = CORN_Y1_PL                     # steel plate
    CORN_Y1_ST  = CORN_Y0_ST + CORN_PLATE         # = 62
    CORN_Y0_PL2 = CORN_Y1_ST                     # inner ply
    CORN_Y1_PL2 = CORN_Y0_PL2 + CORN_PLY          # = 80

    for x0, x1 in [(0, STEP_YD_L), (STEP_YD_R, PW)]:
        w = x1 - x0
        ax.add_patch(Rectangle((x0, CORN_Y0_PL), w, CORN_PLY,
                                fc=C_ALUM, ec=C_OUT, lw=0.8, zorder=3))
        ax.add_patch(Rectangle((x0, CORN_Y0_ST), w, CORN_PLATE,
                                fc=C_STEEL, ec=C_OUT, lw=0.6, zorder=3))
        ax.add_patch(Rectangle((x0, CORN_Y0_PL2), w, CORN_PLY,
                                fc=C_ALUM, ec=C_OUT, lw=0.8, zorder=3))

    # ── Step transition lines ─────────────────────────────────────────────────
    for sx in [STEP_YD_L, STEP_YD_R]:
        # Vertical step face at transition
        ax.plot([sx, sx], [Y0_PL, Y1_PL2], color=C_OUT, lw=1.5, zorder=5)
        # Horizontal shelf connecting 40mm→120mm
        ax.plot([sx, sx], [CORN_Y1_PL2, Y1_PL2], color=C_OUT, lw=1.0,
                ls=(0, (4, 2)), zorder=4, alpha=0.7)

    # ── Layer labels (leaders from center zone) ───────────────────────────────
    LBL_OFF = 130
    lbl_x_r = D_XR + 60
    for ly, lbl, off in [
        (Y0_W + WALL_T / 2,  f"CONTAINER END WALL ({WALL_T}mm STEEL)", 2 * LBL_OFF),
        (Y0_PL + PLY_T / 2,  f"OUTER PLY ({PLY_T}mm)",                 1 * LBL_OFF),
    ]:
        ax.annotate(lbl, xy=(lbl_x_r, ly),
                    xytext=(lbl_x_r + off, ly - off),
                    fontsize=6.5, color=C_OUT, ha="left", va="top", **FONT,
                    arrowprops=dict(arrowstyle="->", linestyle=':', color=C_DIM, lw=0.8),
                    bbox=dict(fc="#EEF2F8", ec="none", pad=1.5), zorder=15)
    lbl_x_l = D_XL - 60
    for ly, lbl, off in [
        (Y0_FR + FRAME_T / 2, f"50×50mm RHS STEEL FRAME ({FRAME_T}mm)", 1.5 * LBL_OFF),
        (Y0_PL2 + PLY_T / 2,  f"INNER PLY — FLAT BLACK ({PLY_T}mm)",    2 * LBL_OFF),
    ]:
        ax.annotate(lbl, xy=(lbl_x_l, ly),
                    xytext=(lbl_x_l - off, ly + off),
                    fontsize=6.5, color=C_OUT, ha="right", va="bottom", **FONT,
                    arrowprops=dict(arrowstyle="->", linestyle=':', color=C_DIM, lw=0.8),
                    zorder=15)

    # ── EPDM perimeter seal strips at panel edges ─────────────────────────────
    SEAL_W = 20
    # Left edge
    ax.add_patch(Rectangle((0, Y0_PL), SEAL_W, PT,
                            fc=C_GASKT, ec=C_OUT, lw=1.0, zorder=6, alpha=0.9))
    # Right edge
    ax.add_patch(Rectangle((PW - SEAL_W, Y0_PL), SEAL_W, PT,
                            fc=C_GASKT, ec=C_OUT, lw=1.0, zorder=6, alpha=0.9))
    leader(ax, (SEAL_W / 2, Y0_PL + PT / 2),
           (-180, Y0_PL + PT / 2 + 100),
           "20mm EPDM GASKET\n(PERIMETER SEAL)", fs=6.5)

    # ── HGR20 rails and carriage system (both panel edges) ───────────────────
    C_RAIL = "#CC4422"
    C_CARR = "#C04010"
    RAIL_W = 20     # HGR20 rail width (cross-section in plan)
    RAIL_D = 500    # rail length in depth direction (extends behind panel into page)
    CBEAM  = 60     # carriage beam SHS section

    # LEFT SIDE — carriage beam + HGR20 rail
    # Rail is at Yd≈30mm, running in depth (Y) direction — shown as a small rectangle
    rail_left_x = -80   # left of panel edge
    ax.add_patch(Rectangle((rail_left_x, -20), RAIL_W, WALL_T + PT + 40,
                            fc=C_RAIL, ec=C_OUT, lw=0.8, alpha=0.6, zorder=5))
    # Carriage beam cross-section (60×60mm SHS)
    ax.add_patch(Rectangle((rail_left_x - 10, Y0_PL - 5), CBEAM + 30, CORNER_T + 10,
                            fc="none", ec=C_CARR, lw=1.5,
                            ls=(0, (5, 3)), zorder=5, alpha=0.7))
    # Brush seal strip (doubled, both sides of slot)
    brush_w = 8
    ax.add_patch(Rectangle((-brush_w, Y0_W), brush_w, Y1_PL2 - Y0_W,
                            fc="#806040", ec=C_OUT, lw=0.5, zorder=6, alpha=0.8))
    ax.add_patch(Rectangle((0, Y0_W), brush_w, Y1_PL2 - Y0_W,
                            fc="#806040", ec=C_OUT, lw=0.5, zorder=6, alpha=0.8))

    leader(ax, (rail_left_x + RAIL_W / 2, Y0_W + WALL_T / 2),
           (rail_left_x - 200, Y_LO + 160),
           "HGR20 RAIL\n(FLOOR/CEILING)\n500mm X-TRAVEL", col=C_RAIL, fs=6)
    leader(ax, (rail_left_x + CBEAM / 2, Y0_PL + CORNER_T / 2),
           (rail_left_x - 200, Y_HI - 80),
           "CARRIAGE BEAM\n60×60mm SHS\n+ BRUSH SEAL", col=C_CARR, fs=6)

    # RIGHT SIDE — guide rail + carriage blocks (no separate beam)
    rail_right_x = PW + 60
    ax.add_patch(Rectangle((rail_right_x, -20), RAIL_W, WALL_T + PT + 40,
                            fc=C_RAIL, ec=C_OUT, lw=0.8, alpha=0.6, zorder=5))
    # Brush seal strip (right slot)
    ax.add_patch(Rectangle((PW - brush_w, Y0_W), brush_w, Y1_PL2 - Y0_W,
                            fc="#806040", ec=C_OUT, lw=0.5, zorder=6, alpha=0.8))
    ax.add_patch(Rectangle((PW, Y0_W), brush_w, Y1_PL2 - Y0_W,
                            fc="#806040", ec=C_OUT, lw=0.5, zorder=6, alpha=0.8))

    leader(ax, (rail_right_x + RAIL_W / 2, Y0_W + WALL_T / 2),
           (rail_right_x + 200, Y_LO + 160),
           "HGR20 RAIL\n(FLOOR/CEILING)\n500mm X-TRAVEL", col=C_RAIL, fs=6)
    leader(ax, (PW + brush_w / 2, Y0_PL + PT / 2),
           (rail_right_x + 200, Y_HI - 80),
           "GUIDE SLOT\n+ BRUSH SEAL\n(DOUBLED NYLON)", col=C_CARR, fs=6)

    # ── Drum: draw filled circle on top to cut out the drum hole ─────────────
    # First stamp BG colour over wall/panel where drum sits, then draw drum ring
    drum_bg = Circle((D_CX, D_CY), DR, fc=BG, ec="none", zorder=7)
    ax.add_patch(drum_bg)

    # ── Housed revolving-door light lock (rev8) ──────────────────────────────
    # Fixed Ø900 housing (two 80° openings: exterior=down / interior=up) + a
    # single-opening C-shell drum (~Ø850 bore) rotating inside it. No fins.
    def _arc(cx, cy, r, gaps, lw, color, z=9):
        deg = np.arange(0, 360.4, 0.4); openm = np.zeros(deg.shape, bool)
        for gc, gw in gaps:
            openm |= np.abs((deg - gc + 180) % 360 - 180) <= gw / 2
        th = np.radians(deg)
        ax.plot(np.where(openm, np.nan, cx + r * np.cos(th)),
                np.where(openm, np.nan, cy + r * np.sin(th)),
                color=color, lw=lw, solid_capstyle="butt", zorder=z)
    OD = LT_OPENING_DEG                          # 80° openings
    BORE_R = LT_DRUM_OR - 3                       # ~Ø850 bore
    ax.add_patch(Circle((D_CX, D_CY), LT_DRUM_OR, fc="#F8F4EC", ec="none", zorder=8))
    _arc(D_CX, D_CY, DR, [(90, OD), (270, OD)], 4.0, C_STEEL, z=9)      # fixed housing
    _arc(D_CX, D_CY, LT_DRUM_OR, [(270, OD)], 3.0, "#9C7B4D", z=10)      # C-shell drum (ENTER)
    # daylight ray at ENTER: enters bore from exterior, blocked at interior by drum
    ax.annotate("", xy=(D_CX, D_CY + LT_DRUM_OR * 0.9), xytext=(D_CX, D_YB - 70),
                arrowprops=dict(arrowstyle="-|>", color="#D08000", lw=1.8), zorder=12)
    ax.plot([D_CX], [D_CY + LT_DRUM_OR], marker="x", ms=10, mew=2.4,
            color="#2E8B57", zorder=13)
    ax.text(D_CX, D_CY, f"Ø{int(2 * BORE_R)}\nbore\n~625mm\npassage", color=C_DIM,
            fontsize=6.2, ha="center", va="center", **FONT, zorder=15)

    # Opening labels + component leaders
    ax.text(D_CX, D_YB - 95, "exterior opening (ENTER)", color="#A05000",
            fontsize=6.5, ha="center", va="top", **FONT, zorder=15)
    ax.text(D_CX, D_YT + 60, "interior opening → onto walkway", color=C_OUT,
            fontsize=6.5, ha="center", va="bottom", **FONT, zorder=15)
    leader(ax, (D_CX + DR * 0.92, D_CY + DR * 0.30),
           (D_XR + 150, D_CY + DR * 0.55),
           f"FIXED HOUSING Ø{int(DRUM_D)} (2 × {OD}° openings)\n"
           f"+ C-SHELL DRUM, 1 opening, no fins\nlight-tight by geometry", fs=6.3)

    # ── Centre lines ──────────────────────────────────────────────────────────
    CL_EXT = 55
    ax.plot([D_CX - DR - CL_EXT, D_CX + DR + CL_EXT], [D_CY, D_CY],
            color=C_CL, lw=0.8, ls="--", zorder=7, alpha=0.6)
    ax.plot([D_CX, D_CX], [D_CY - DR - CL_EXT, D_CY + DR + CL_EXT],
            color=C_CL, lw=0.8, ls="--", zorder=7, alpha=0.6)
    ax.text(D_CX + DR + CL_EXT + 15, D_CY, "CL",
            color=C_CL, fontsize=7, ha="left", va="center", **FONT, zorder=15)

    # ── Light-tightness note ──────────────────────────────────────────────────
    ax.text(D_XR - 25, D_CY - DR * 0.78,
            f"Two {OD}° openings, 180° apart;\nthe housing's solid wall always\ncovers the opening the drum\n"
            "isn't aligned with → NO straight-\nline sight at any rotation.\nSee Sheet 5 (enter / transit / exit).",
            color="#2E8B57", fontsize=6.4, ha="left", va="center", **FONT, zorder=15)

    # ── Dimension lines ────────────────────────────────────────────────────────
    DIM_X_R = D_XR + PAD_X * 0.35   # right-side dim column

    # Drum diameter (horizontal)
    dim_h(ax, D_XL, D_XR, D_YT + PAD_YT * 0.55,
          f"Ø{DRUM_D}mm  DRUM DIAMETER", fs=7, offset=-25)

    # Container wall thickness — arrow + inline label (no leader, avoids crossing
    # the nearby CONTAINER END WALL and OUTER PLY leader lines)
    dim_v(ax, DIM_X_R, Y0_W, Y1_W,
          f"  {WALL_T}mm", offset=15, fs=6.5)

    # Panel overall thickness — arrow + inline label
    dim_v(ax, DIM_X_R, Y1_W, Y1_PL2,
          f"  {PT}mm", offset=15, fs=6.5)

    # Exterior drum overhang — 45° leader going south-left
    ext_oh_mid = (D_YB + Y0_W) / 2
    dim_v(ax, D_XL - 150, D_YB, Y0_W, f"{int(Y0_W - D_YB)}mm EXT. OVERHANG", offset=15, fs=6)

    # Interior drum overhang — 45° leader going north-left
    int_oh_mid = (Y1_PL2 + D_YT) / 2
    dim_v(ax, D_XL - 150, Y1_PL2, D_YT, f"{int(D_YT - Y1_PL2)}mm INT. OVERHANG", offset=15, fs=6)
#     ax.annotate(f"{int(D_YT - Y1_PL2)}mm INT. OVERHANG",
#                 xy=(D_XL - 180, int_oh_mid),
#                 xytext=(D_XL - 180 - LBL_OFF * 1.5, int_oh_mid + LBL_OFF * 1.5),
#                 fontsize=6, color=C_DIM, ha="right", va="bottom", **FONT,
#                 arrowprops=dict(arrowstyle="->", linestyle=':', color=C_DIM, lw=0.8),
#                 bbox=dict(fc="white", ec="none", pad=1.5), zorder=15)

    # Full panel width dimension
    dim_h(ax, 0, PW, Y_LO + 230, f"{PW}mm  (FULL PANEL WIDTH)", fs=7, offset=-25)

    # Zone width dimensions (above panel)
    zone_dim_y = D_YT + PAD_YT * 0.85
    dim_h(ax, 0, STEP_YD_L, zone_dim_y-30,
          f"{STEP_YD_L}mm", fs=6, offset=-20)
    dim_h(ax, STEP_YD_L, STEP_YD_R, zone_dim_y-30,
          f"{STEP_YD_R - STEP_YD_L}mm CENTER", fs=6, offset=-20)
    dim_h(ax, STEP_YD_R, PW, zone_dim_y-30,
          f"{PW - STEP_YD_R}mm", fs=6, offset=-20)

    # Corner zone thickness dimension
    dim_v(ax, STEP_YD_L / 2 - 100, Y1_W, CORN_Y1_PL2,
          f"{CORNER_T}mm", offset=15, fs=6)

    # ── Zone labels ─────────────────────────────────────────────────────────────
    ax.text(STEP_YD_L / 2, CORN_Y1_PL2 + 25,
            f"40mm\nCORNER", color="#C04010", fontsize=6, ha="center", va="bottom",
            fontweight="bold", **FONT, zorder=15, alpha=0.7)
    ax.text((STEP_YD_L + STEP_YD_R) / 2, Y1_PL2 + 25,
            f"120mm CENTER", color="#C04010", fontsize=6, ha="center", va="bottom",
            fontweight="bold", **FONT, zorder=15, alpha=0.7)
    ax.text((STEP_YD_R + PW) / 2, CORN_Y1_PL2 + 25,
            f"40mm\nCORNER", color="#C04010", fontsize=6, ha="center", va="bottom",
            fontweight="bold", **FONT, zorder=15, alpha=0.7)

    # ── Scale and note ────────────────────────────────────────────────────────
    ax.text(PW / 2, Y_HI - 20,
            "EQUAL ASPECT  ·  SCALE 1:20 (APPROX)  ·  FULL PANEL WIDTH  ·  "
            "DRUM OVERHANGS PANEL ON BOTH FACES — SECURED BY BEARINGS AT TOP AND BOTTOM",
            color=C_DIM, fontsize=6.5, ha="center", va="top", **FONT, zorder=15)

    # ── Orientation clarification box ─────────────────────────────────────────
    # Small inset box top-right, making the viewing direction explicit
    OB_X = D_XR + 30
    OB_Y = D_YT - 100
    OB_W = 450
    OB_H = 190
    import matplotlib.patches as mpatches
    ax.add_patch(mpatches.FancyBboxPatch((OB_X, OB_Y), OB_W, OB_H,
                 boxstyle="round,pad=3",
                 facecolor="#FFFBF0", edgecolor="#806010", linewidth=1.0, zorder=12))
    ax.text(OB_X + OB_W / 2, OB_Y + OB_H - 18,
            "ORIENTATION NOTE",
            ha="center", va="top", fontsize=6.5, color="#806010",
            fontweight="bold", **FONT, zorder=15)
    ax.text(OB_X + OB_W / 2, OB_Y + OB_H * 0.42,
            "DRUM AXIS IS VERTICAL.\nPERSONNEL WALK THROUGH\nIN AN UPRIGHT POSITION.\nSee Sheet 3 for elevation view.",
            ha="center", va="center", fontsize=6, color="#403000",
            **FONT, zorder=15)

    # ── Interior latch safety note ─────────────────────────────────────────────
    # Small note below orientation box (latches are outside the drum-zone crop
    # in this view but their presence and position is relevant to egress design)
    ax.text(OB_X + OB_W / 2 + 450, OB_Y - 25,
            "PANEL LATCHES (×4, SOUTHCO C2-33):\nMOUNTED ON INTERIOR FACE —\nEGRESS OPERABLE FROM INSIDE",
            ha="center", va="top", fontsize=6, color="#C04010",
            fontweight="bold", **FONT, zorder=15)

    # ── Title block ────────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 6",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="PLAN CROSS-SECTION (SECTION A-A AT H=1000mm) — DRUM BAFFLES & S-PATH LIGHT ROUTE",
                scale_note="EQUAL ASPECT  \u00b7  SCALE 1:20 (APPROX)  \u00b7  ALL DIMS IN mm",
                doc_id="TBS-001 \u00b7 Hinged Light-Trap Panel", height=0.055)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet2.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet2.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3  —  Drum Vertical Section (Section A-A, looking along panel width)
#
# This view shows the drum in ELEVATION — makes clear it is a VERTICAL cylinder
# 2200mm tall that personnel walk through upright.
#
# Horizontal axis = DEPTH direction (exterior → interior, same as Sheet 2 Y axis)
# Vertical axis   = HEIGHT (0 → 2200mm, floor → top bearing)
#
# ASPECT RATIO: figsize derived from data limits. set_aspect("equal") always set.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet3():
    # ── Key dimensions (re-use Sheet 2 depth constants) ──────────────────────
    WALL_T  = 40    # container end-wall steel thickness
    PLY_T   = 18    # ply skin thickness each face
    PT      = 120   # panel overall thickness
    FRAME_T = PT - 2 * PLY_T   # = 84mm

    # Depth positions (horizontal axis in this view)
    Y0_W   = 0           # exterior face of container wall
    Y1_W   = WALL_T      # = 40
    Y0_PL  = Y1_W        # outer ply
    Y1_PL  = Y1_W + PLY_T  # = 58
    Y0_FR  = Y1_PL       # frame start = 58
    Y1_FR  = Y0_FR + FRAME_T  # = 142
    Y0_PL2 = Y1_FR       # inner ply = 142
    Y1_PL2 = Y0_PL2 + PLY_T  # = 160  (panel interior face)

    # Drum geometry in this view
    D_CX_DEPTH = (Y0_W + Y1_PL2) / 2   # drum centre in depth = 80mm
    D_HALF_W   = DRUM_R                 # drum radius = 375mm (in depth axis)

    D_DEPTH_L  = D_CX_DEPTH - D_HALF_W   # = 80 - 375 = -295mm (exterior overhang)
    D_DEPTH_R  = D_CX_DEPTH + D_HALF_W   # = 80 + 375 = 455mm  (interior overhang)

    # Height positions (vertical axis in this view)
    H_FLOOR    = 0
    H_BRG_BOT  = 100          # lower bearing base
    H_BRG_HT   = 45           # bearing housing height
    H_DRUM_BOT = H_BRG_BOT + H_BRG_HT   # = 145mm (drum body starts)
    H_DRUM_TOP = H_DRUM_BOT + (DRUM_H - 2 * H_BRG_HT)  # = 145 + 1910 = 2055mm
    H_BRG_TOP  = H_DRUM_TOP + H_BRG_HT  # = 2100mm
    H_HANDLE   = H_BRG_BOT + DRUM_H * 0.45  # handle height = ~1000mm

    # ── Data range → figure size ──────────────────────────────────────────────
    PAD_L, PAD_R = 300, 1380  # depth-axis margins (right margin holds Detail B)
    PAD_B, PAD_T = 500, 350   # height-axis margins (bottom includes title block + rail annotations)

    X_LO = D_DEPTH_L - PAD_L   # = -595mm
    X_HI = D_DEPTH_R + PAD_R   # = 1835mm  → width 2430mm
    Y_LO = H_FLOOR - PAD_B     # = -150mm
    Y_HI = H_BRG_TOP + PAD_T   # = 2450mm  → height 2600mm

    # Data ratio: 2430 : 2600
    FIG_H = 14.0
    FIG_W = FIG_H * (X_HI - X_LO) / (Y_HI - Y_LO)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=130)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Y_LO, Y_HI)
    ax.set_aspect("equal")   # MANDATORY
    ax.axis("off")

    # ── Background zones ──────────────────────────────────────────────────────
    # Exterior zone (depth < 0)
    ax.add_patch(plt.Rectangle((X_LO, Y_LO), Y0_W - X_LO, Y_HI - Y_LO,
                                fc="#EEF2F8", ec="none", zorder=1))
    ax.text((X_LO + Y0_W) / 2, Y_HI - 80, "EXTERIOR",
            color="#5060A0", fontsize=9, ha="center", va="top", **FONT,
            fontweight="bold", alpha=0.55, zorder=15)

    # Interior zone (depth > panel interior face)
    ax.add_patch(plt.Rectangle((Y1_PL2, Y_LO), X_HI - Y1_PL2, Y_HI - Y_LO,
                                fc="#EEF6EE", ec="none", zorder=1))
    ax.text((Y1_PL2 + X_HI) / 2, Y_HI - 80, "INTERIOR\n(DARKROOM)",
            color="#407040", fontsize=9, ha="center", va="top", **FONT,
            fontweight="bold", alpha=0.55, zorder=15)

    # ── Container end wall (depth 0→40, full height) ──────────────────────────
    ax.add_patch(plt.Rectangle((Y0_W, H_FLOOR), WALL_T, H_BRG_TOP + 100,
                                fc=C_STEEL, ec=C_OUT, lw=0.8, hatch="///", zorder=3))

    # ── Panel outer ply (depth 40→58) ────────────────────────────────────────
    ax.add_patch(plt.Rectangle((Y0_PL, H_FLOOR), PLY_T, H_BRG_TOP + 80,
                                fc=C_ALUM, ec=C_OUT, lw=0.6, zorder=3))

    # ── Panel RHS frame (depth 58→142) ────────────────────────────────────────
    ax.add_patch(plt.Rectangle((Y0_FR, H_FLOOR), FRAME_T, H_BRG_TOP + 80,
                                fc=C_STEEL, ec=C_OUT, lw=0.6, hatch="\\\\", zorder=3))

    # ── Panel inner ply (depth 142→160) ───────────────────────────────────────
    ax.add_patch(plt.Rectangle((Y0_PL2, H_FLOOR), PLY_T, H_BRG_TOP + 80,
                                fc=C_ALUM, ec=C_OUT, lw=0.6, zorder=3))

    # ── Layer thickness leaders (top) ─────────────────────────────────────────
    LDR_TOP = H_BRG_TOP + 100    # leader origin height (above bearings)
    LDR_TOP_TGT = H_BRG_TOP + 210  # leader text target height
    # Wall
    leader(ax, ((Y0_W + Y1_W) / 2, LDR_TOP - 50),
           ((Y0_W + Y1_W) / 2 - 120, LDR_TOP_TGT + 40),
           f"{WALL_T}mm WALL\n(STEEL)", col=C_DIM, fs=5.5)
    # Outer ply
    leader(ax, ((Y0_PL + Y1_PL) / 2 - 5, LDR_TOP - 80),
           ((Y0_PL + Y1_PL) / 2 + 100, LDR_TOP_TGT + 10),
           f"{PLY_T}mm\nPLY", col=C_DIM, fs=5.5)
    # RHS frame
    leader(ax, ((Y0_FR + Y1_FR) / 2, LDR_TOP - 50),
           ((Y0_FR + Y1_FR) / 2 + 120, LDR_TOP_TGT + 50),
           f"{FRAME_T}mm RHS FRAME", col=C_DIM, fs=5.5)
    # Inner ply
    leader(ax, ((Y0_PL2 + Y1_PL2) / 2 - 5, LDR_TOP - 60),
           ((Y0_PL2 + Y1_PL2) / 2 + 120, LDR_TOP_TGT + 10),
           f"{PLY_T}mm\nPLY", col=C_DIM, fs=5.5)

    # ── Layer thickness leaders (bottom) ──────────────────────────────────────
    LDR_BOT = H_FLOOR + 60       # leader origin height (just above floor)
    LDR_BOT_TGT = H_FLOOR - 40   # leader text target height (below floor line)
    # Wall
    leader(ax, ((Y0_W + Y1_W) / 2, LDR_BOT),
           ((Y0_W + Y1_W) / 2 - 120, LDR_BOT_TGT),
           f"{WALL_T}mm WALL", col=C_DIM, fs=5.5)
    # Outer ply
    leader(ax, ((Y0_PL + Y1_PL) / 2 - 5, LDR_BOT + 20),
           ((Y0_PL + Y1_PL) / 2 + 100, LDR_BOT_TGT - 50),
           f"{PLY_T}mm\nPLY", col=C_DIM, fs=5.5)
    # RHS frame
    leader(ax, ((Y0_FR + Y1_FR) / 2, LDR_BOT),
           ((Y0_FR + Y1_FR) / 2 + 120, LDR_BOT_TGT - 100),
           f"{FRAME_T}mm RHS FRAME", col=C_DIM, fs=5.5)
    # Inner ply
    leader(ax, ((Y0_PL2 + Y1_PL2) / 2 - 5, LDR_BOT + 20),
           ((Y0_PL2 + Y1_PL2) / 2 + 120, LDR_BOT_TGT - 50),
           f"{PLY_T}mm\nPLY", col=C_DIM, fs=5.5)

    # ── Floor (ground plane) ──────────────────────────────────────────────────
    ax.add_patch(plt.Rectangle((X_LO, H_FLOOR - PAD_B), X_HI - X_LO, PAD_B,
                                fc="#D8D0C0", ec="none", zorder=2))
    ax.plot([X_LO, X_HI], [H_FLOOR, H_FLOOR], color=C_OUT, lw=1.5, zorder=4)
    ax.text(X_LO + 30, H_FLOOR - PAD_B * 0.75, "FLOOR LEVEL",
            ha="left", va="center", fontsize=7, color=C_DIM, **FONT, zorder=15)

    # ── Interior walkway (near/far walls) ──────────────────────────────────────
    # In this Section A-A view (looking along Yd), the near and far walkways
    # project to the same position. They cantilever from the container side
    # walls, running along X. Show as cross-section on the interior side.
    C_WALKWAY = "#707078"
    BRKT_ARM_Z = WALKWAY_H - WALKWAY_GRATE_T  # = 75mm (top of bracket arm)
    WK_START = Y1_PL2 + 80   # start showing walkway past drum overhang
    WK_END   = D_DEPTH_R + 120  # extend into interior

    # Bracket arm (8mm thick at Z=67-75mm)
    ax.add_patch(plt.Rectangle((WK_START, BRKT_ARM_Z - WALKWAY_BRACKET_T),
                                WK_END - WK_START, WALKWAY_BRACKET_T,
                                fc=C_WALKWAY, ec=C_OUT, lw=0.6, zorder=4))
    # Grate (25mm thick at Z=75-100mm)
    ax.add_patch(plt.Rectangle((WK_START, BRKT_ARM_Z),
                                WK_END - WK_START, WALKWAY_GRATE_T,
                                fc="#D0D0D4", ec=C_OUT, lw=0.6, hatch="--", zorder=4))

    # Break lines at right end (walkway continues)
    for z_off in [-5, 5, 15]:
        ax.plot([WK_END - 3, WK_END + 3],
                [BRKT_ARM_Z + z_off - 3, BRKT_ARM_Z + z_off + 3],
                color=C_OUT, lw=0.6, zorder=5)

    leader(ax, (WK_START + (WK_END - WK_START) / 2, WALKWAY_H + 5),
           (WK_START + (WK_END - WK_START) / 2 + 300, WALKWAY_H + 200),
           f"WALKWAY DECK\n{WALKWAY_GRATE_T}mm GRATE AT\nZ={WALKWAY_H}mm\n(NEAR + FAR WALLS)",
           col=C_WALKWAY, fs=5.5)

    # Walkway deck height dimension
    dim_v(ax, WK_END + 30, H_FLOOR, WALKWAY_H,
          f"{WALKWAY_H}mm\nDECK", offset=30, fs=6)

    # ── HGR20 sliding rails (floor + ceiling, both container walls) ──────────
    # Rails run in the X (depth) direction, mounted on both side walls.
    # In this Section A-A view (looking along Yd), the rails on both walls
    # project to the same position.  Shown as side-profile rectangles.
    C_RAIL_S3 = "#CC4422"     # red, consistent with Sheet 1
    RAIL_PROF_H = 20          # rail profile height (mm)
    RAIL_PROF_L = 500         # rail length (mm) — 500mm HGR20 rail
    RAIL_BLOCK_H = 30         # carriage block height above rail
    RAIL_BLOCK_L = 44         # carriage block length (mm)
    SLIDE_TRAVEL = 300        # panel slide travel (mm)

    # Floor rail — sits on floor surface, runs from just behind wall to 500mm inward
    RAIL_FLOOR_Y = H_FLOOR                  # bottom of rail at floor level
    RAIL_FLOOR_X = Y0_W - 50                # start slightly exterior of wall
    ax.add_patch(plt.Rectangle((RAIL_FLOOR_X, RAIL_FLOOR_Y),
                                RAIL_PROF_L, RAIL_PROF_H,
                                fc=C_RAIL_S3, ec=C_OUT, lw=0.7, alpha=0.5, zorder=4))
    # Carriage block on floor rail (at panel position)
    BLOCK_FLOOR_X = Y0_PL - 10             # block near panel outer face
    ax.add_patch(plt.Rectangle((BLOCK_FLOOR_X, RAIL_FLOOR_Y + RAIL_PROF_H),
                                RAIL_BLOCK_L, RAIL_BLOCK_H,
                                fc=C_RAIL_S3, ec=C_OUT, lw=0.6, alpha=0.4, zorder=4))

    # Ceiling rail — at top of panel/container opening
    H_CEILING = H_BRG_TOP + 100            # ceiling height (above upper bearing)
    ax.add_patch(plt.Rectangle((RAIL_FLOOR_X, H_CEILING - RAIL_PROF_H),
                                RAIL_PROF_L, RAIL_PROF_H,
                                fc=C_RAIL_S3, ec=C_OUT, lw=0.7, alpha=0.5, zorder=4))
    # Carriage block on ceiling rail
    ax.add_patch(plt.Rectangle((BLOCK_FLOOR_X, H_CEILING - RAIL_PROF_H - RAIL_BLOCK_H),
                                RAIL_BLOCK_L, RAIL_BLOCK_H,
                                fc=C_RAIL_S3, ec=C_OUT, lw=0.6, alpha=0.4, zorder=4))

    # Rail labels — placed well clear of dimension lines below
    leader(ax, (RAIL_FLOOR_X + RAIL_PROF_L, RAIL_FLOOR_Y + RAIL_PROF_H / 2),
           (RAIL_FLOOR_X + RAIL_PROF_L + 200, RAIL_FLOOR_Y - 130),
           "HGR20 FLOOR RAIL\n(BOTH WALLS, 500mm)",
           col=C_RAIL_S3, fs=5.5)
    leader(ax, (RAIL_FLOOR_X + RAIL_PROF_L, H_CEILING - RAIL_PROF_H / 2),
           (RAIL_FLOOR_X + RAIL_PROF_L + 130, H_CEILING + 50),
           "HGR20 CEILING RAIL\n(BOTH WALLS, 500mm)",
           col=C_RAIL_S3, fs=5.5)

    # Slide travel arrow (below overhang dimensions, clear of title block)
    ARROW_Y = RAIL_FLOOR_Y - 160
    ax.annotate("", xy=(Y0_W, ARROW_Y), xytext=(Y0_W + SLIDE_TRAVEL, ARROW_Y),
                arrowprops=dict(arrowstyle="<->", color=C_RAIL_S3, lw=1.0,
                                mutation_scale=8), zorder=9)
    ax.text(Y0_W + SLIDE_TRAVEL / 2, ARROW_Y - 15,
            f"{SLIDE_TRAVEL}mm SLIDE TRAVEL", ha="center", va="top",
            fontsize=5.5, color=C_RAIL_S3, **FONT, zorder=15)

    # ── Lower bearing housing ─────────────────────────────────────────────────
    ax.add_patch(plt.Rectangle((D_DEPTH_L - 35, H_BRG_BOT),
                                DRUM_D + 70, H_BRG_HT,
                                fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=6))
    ax.text(D_CX_DEPTH, H_BRG_BOT + H_BRG_HT / 2,
            "SKF 6215  LOWER BEARING", ha="center", va="center",
            fontsize=5.5, color=C_OUT, **FONT, zorder=15)

    # ── Upper bearing housing ─────────────────────────────────────────────────
    ax.add_patch(plt.Rectangle((D_DEPTH_L - 35, H_DRUM_TOP),
                                DRUM_D + 70, H_BRG_HT,
                                fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=6))
    ax.text(D_CX_DEPTH, H_DRUM_TOP + H_BRG_HT / 2,
            "SKF 6215  UPPER BEARING", ha="center", va="center",
            fontsize=5.5, color=C_OUT, **FONT, zorder=15)

    # ── Drum body (tall rectangle, depth D_DEPTH_L→D_DEPTH_R, H_DRUM_BOT→H_DRUM_TOP)
    # This is the key visual: a tall vertical rectangle showing the drum is vertical
    ax.add_patch(plt.Rectangle((D_DEPTH_L, H_DRUM_BOT),
                                DRUM_D, H_DRUM_TOP - H_DRUM_BOT,
                                fc=C_LT_DRUM, ec=C_OUT, lw=2.0, zorder=5))

    # Drum wall thickness lines (3mm each side)
    DRUM_WALL_T = 3
    ax.plot([D_DEPTH_L + DRUM_WALL_T, D_DEPTH_L + DRUM_WALL_T],
            [H_DRUM_BOT, H_DRUM_TOP], color=C_DIM, lw=0.6, ls="--", zorder=6)
    ax.plot([D_DEPTH_R - DRUM_WALL_T, D_DEPTH_R - DRUM_WALL_T],
            [H_DRUM_BOT, H_DRUM_TOP], color=C_DIM, lw=0.6, ls="--", zorder=6)

    # ── 4 baffles (radial fins — shown as dashed lines at mid-depth in elevation)
    # Baffles run full height inside the drum.  In this elevation view they
    # appear as vertical dashed lines at their mid-chord depth positions.
    # Baffles are at 0°, 90°, 180°, 270° from horizontal (plan view).
    # In this elevation (looking along panel width = X axis in plan), the fins
    # at 0° and 180° appear at the drum wall, and 90° and 270° at drum centre.
    for fin_depth in [D_DEPTH_L, D_CX_DEPTH, D_DEPTH_R]:
        ax.plot([fin_depth, fin_depth], [H_DRUM_BOT + 20, H_DRUM_TOP - 20],
                color=C_OUT, lw=1.2, ls=(0, (5, 3)), zorder=7, alpha=0.7)

    ax.text(D_CX_DEPTH/2 - 150, H_DRUM_BOT + (H_DRUM_TOP - H_DRUM_BOT) * 0.5,
            "4 × INTERNAL BAFFLES\n(FULL HEIGHT)\nFlat black powder coat",
            ha="center", va="center", fontsize=6.5, color=C_DIM,
            **FONT, alpha=0.7, zorder=15)

    # ── Handle bar — interior face only, welded bracket (no through-hole) ────────
    # Handle projects INWARD from the drum wall into the hollow of the drum.
    # D_DEPTH_R is the interior drum wall face; handle runs D_DEPTH_R-110 → D_DEPTH_R.
    HH = 42
    hx = D_DEPTH_R - 110
    ax.add_patch(plt.Rectangle((hx, H_HANDLE - HH / 2), 110, HH,
                                fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=7))
    ax.text(hx + 255, H_HANDLE + 70, "INT. HANDLE\n(welded bracket\nno through-hole)",
            ha="center", va="top", fontsize=5.5, color=C_DIM, **FONT, zorder=15)

    # ── Person silhouette — standing inside drum, feet at drum floor (H_DRUM_BOT) ──
    PERSON_H = 1780   # mm — operator height with shoes
    HEAD_R   = 80     # head circle radius
    # Place person inside drum toward the interior wall, clear of centreline text
    PERSON_X = D_DEPTH_R - 130
    P_FOOT   = H_DRUM_BOT          # feet on drum floor (145mm above container floor)
    P_HEAD   = P_FOOT + PERSON_H   # head top = 145 + 1780 = 1925mm

    # Drum floor level indicator (thin horizontal line across drum base)
    ax.plot([D_DEPTH_L, D_DEPTH_R], [H_DRUM_BOT, H_DRUM_BOT],
            color="#A06020", lw=0.8, ls="--", zorder=6, alpha=0.7)
    # Vertical dimension arrow: container floor → drum floor
    DRUM_FL_DIM_X = D_DEPTH_L - 180
    dim_v(ax, DRUM_FL_DIM_X, H_FLOOR, H_DRUM_BOT,
          f"{H_DRUM_BOT}mm\nDRUM\nFLOOR", offset=-100, fs=6)

    # Person body (line) and head (circle) — blue tones
    ax.plot([PERSON_X, PERSON_X], [P_FOOT, P_HEAD],
            color="#2060A0", lw=3.0, zorder=8, solid_capstyle="round")
    ax.add_patch(plt.Circle((PERSON_X, P_HEAD + HEAD_R), HEAD_R,
                             fc="#70A8D8", ec="#1A4D80", lw=1.0, zorder=8))

    # Headroom gap: person head top → drum body ceiling
    drum_body_h    = H_DRUM_TOP - H_DRUM_BOT
    headroom_1780  = drum_body_h - PERSON_H
    GAP_X = PERSON_X
    ax.annotate("", xy=(GAP_X, H_DRUM_TOP), xytext=(GAP_X, P_HEAD + 2 * HEAD_R),
                arrowprops=dict(arrowstyle="<->", color="#20A020", lw=1.0,
                                mutation_scale=7), zorder=9)
    ax.text(GAP_X - 125, (H_DRUM_TOP + P_HEAD + 2 * HEAD_R) / 2,
            f"{headroom_1780}mm\nHEADROOM",
            ha="left", va="center", fontsize=6, color="#20A020", fontweight="bold", **FONT, zorder=15)

    # Label alongside person
    ax.text(PERSON_X - HEAD_R - 15, P_FOOT + PERSON_H / 2,
            f"{PERSON_H}mm\noperator\n(shoes)",
            ha="right", va="center", fontsize=6, color="#1A4D80", **FONT, zorder=15)

    # ── Drum body ceiling line ────────────────────────────────────────────────
    ax.plot([D_DEPTH_L - 50, D_DEPTH_R + 50], [H_DRUM_TOP, H_DRUM_TOP],
            color="#20A020", lw=1.2, ls="--", zorder=6)
    ax.text(X_LO + 1180, H_DRUM_TOP,
            f"DRUM BODY TOP H={H_DRUM_TOP}mm\nCLEAR WALKING HT={drum_body_h}mm",
            ha="left", va="bottom", fontsize=6.5, color="#20A020", **FONT, zorder=15)

    # ── Section A-A indicator ─────────────────────────────────────────────────
    ax.text(X_LO + 20, Y_HI + 50,
            "SECTION A-A (looking along panel width direction)",
            ha="left", va="top", fontsize=7, color=C_CL, **FONT,
            fontweight="bold", zorder=15)

    # ── Centre line (vertical drum axis) ──────────────────────────────────────
    ax.plot([D_CX_DEPTH, D_CX_DEPTH], [H_FLOOR - 80, H_BRG_TOP + 120],
            color=C_CL, lw=0.9, ls="--", zorder=6)
    ax.text(D_CX_DEPTH - 75, H_BRG_TOP - 240, "CL\nDRUM AXIS\n(VERTICAL)",
            ha="left", va="bottom", fontsize=6.5, color=C_CL, **FONT, zorder=15)

    # ── Entry / exit arrows ───────────────────────────────────────────────────
    # Person enters from EXTERIOR, pushes drum, exits to INTERIOR
    EAR_Y = H_FLOOR + DRUM_H * 0.4
    ax.annotate("", xy=(D_DEPTH_L - 20, EAR_Y + 450),
                xytext=(X_LO + 20, EAR_Y + 450),
                arrowprops=dict(arrowstyle="->", color="#C06010", lw=1.5,
                                mutation_scale=10))
    ax.text(X_LO + 20, EAR_Y + 500, "ENTER\n(from exterior)",
            ha="left", va="bottom", fontsize=7, color="#C06010", **FONT, zorder=15)

    ax.annotate("", xy=(D_DEPTH_R + 220, EAR_Y + 450),
                xytext=(D_DEPTH_R + 40, EAR_Y + 450),
                arrowprops=dict(arrowstyle="->", color="#20A060", lw=1.5,
                                mutation_scale=10))
    ax.text(D_DEPTH_R + 40, EAR_Y + 500, "EXIT\n(to interior /\ndarkroom)",
            ha="left", va="bottom", fontsize=7, color="#20A060", **FONT, zorder=15)

    ax.text(D_CX_DEPTH /2 - 150, H_FLOOR + DRUM_H * 0.2,
            "DRUM ROTATES\nARROUND VERTICAL\nAXIS — PUSH WALL\nTO ENTER/EXIT",
            ha="center", va="center", fontsize=6.5, color=C_DIM,
            **FONT, alpha=0.75, zorder=15)

    # ── Dimension callouts ────────────────────────────────────────────────────
    DIM_R = D_DEPTH_R + PAD_R * 0.55

    # Drum height
    dim_v(ax, DIM_R, H_DRUM_BOT, H_DRUM_TOP,
          f"{DRUM_H}mm DRUM HEIGHT\n(CLEAR WALKING HEIGHT)", offset=30, fs=7)

    # Drum diameter (horizontal) — placed below top bearing to avoid CL label clash
    dim_h(ax, D_DEPTH_L, D_DEPTH_R, H_DRUM_TOP + 180,
          f"Ø{DRUM_D}mm DRUM DIAMETER", offset=15, fs=7)

    # Panel thickness (horizontal) — offset above bearing top
    dim_h(ax, Y0_W, Y1_PL2, H_BRG_TOP + 295,
          f"{PT}mm PANEL", offset=15, fs=6.5)

    # (Wall thickness leaders are drawn above with the other layer leaders)

    # Exterior overhang (horizontal) — below floor rail
    dim_h(ax, D_DEPTH_L, Y0_W, H_FLOOR + 40,
          f"{abs(int(D_DEPTH_L))}mm EXT. OVERHANG", offset=15, fs=6)

    # Interior overhang (horizontal) — below floor rail
    dim_h(ax, Y1_PL2, D_DEPTH_R, H_FLOOR + 40,
          f"{int(D_DEPTH_R - Y1_PL2)}mm INT. OVERHANG", offset=15, fs=6)

    # Vertical dimension arrow: container floor → handle bottom
    HANDLE_DIM_X = D_DEPTH_L - 100
    HANDLE_BOT = H_HANDLE - HH / 2   # bottom of handle bar
    dim_v(ax, HANDLE_DIM_X/2 + DRUM_D, H_FLOOR, HANDLE_BOT,
          f"{int(HANDLE_BOT)}mm\nHANDLE HT", offset=-60, fs=6)

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL B — Panel bottom light seal (enlarged), section at a corner zone
    # (away from the drum). The 80mm floor gap is closed in the operational
    # ("camera") position by a fixed-frame seal lip the panel bottom edge recedes
    # into; a 20mm EPDM strip is compressed against it by the lower cam latches.
    # ══════════════════════════════════════════════════════════════════════════
    k = 3.3
    ox, oy = 980, 300
    def DX(d): return ox + k * d
    def DY(h): return oy + k * h

    bx0, bx1 = DX(-98), DX(178)
    by0, by1 = DY(-28), DY(182)
    ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0,
                           fc="#FBFBFD", ec=C_DIM, lw=1.0, ls=(0, (5, 3)), zorder=2))
    ax.text((bx0 + bx1) / 2, by1 + 34, "DETAIL B — PANEL BOTTOM SEAL",
            ha="center", va="bottom", fontsize=9, fontweight="bold", color=C_OUT, **FONT)
    ax.text((bx0 + bx1) / 2, by1 + 10,
            "operational / “camera” position  ·  section at corner zone  ·  enlarged ~3.3:1",
            ha="center", va="bottom", fontsize=6.4, color=C_DIM, **FONT)
    ax.text(DX(-90), DY(150), "EXTERIOR", fontsize=6, color="#5060A0",
            ha="left", va="center", fontweight="bold", **FONT)
    ax.text(DX(170), DY(150), "INTERIOR", fontsize=6, color="#407040",
            ha="right", va="center", fontweight="bold", **FONT)

    # floor + hatch below
    ax.add_patch(Rectangle((bx0, DY(-28)), bx1 - bx0, DY(0) - DY(-28),
                           fc="#ECECEC", ec="none", hatch="////", lw=0, zorder=19))
    ax.plot([bx0, bx1], [DY(0), DY(0)], color=C_OUT, lw=2.2, zorder=22)

    # door-frame threshold (50×50 RHS), seal lip, EPDM, panel corner zone, tray rim
    ax.add_patch(Rectangle((DX(-50), DY(0)), k * 50, k * 50,
                           fc=C_STEEL, ec=C_OUT, lw=1.2, zorder=21))
    ax.add_patch(Rectangle((DX(-32), DY(0)), k * 12, k * 110,
                           fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=23))
    ax.add_patch(Rectangle((DX(-20), DY(80)), k * 20, k * 40,
                           fc=C_GASKT, ec=C_OUT, lw=1.0, zorder=24))
    ax.add_patch(Rectangle((DX(0), DY(80)), k * 40, k * 100,
                           fc=C_ALUM, ec=C_OUT, lw=1.3, zorder=22))
    ax.add_patch(Rectangle((DX(70), DY(0)), k * 9, k * 50,
                           fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=21))

    # exterior light ray blocked by the lip
    ax.annotate("", xy=(DX(-33), DY(38)), xytext=(DX(-92), DY(38)),
                arrowprops=dict(arrowstyle="-|>", color="#D08000", lw=1.6), zorder=25)
    ax.plot([DX(-30)], [DY(38)], marker="x", ms=7, mew=2.2, color="#C02020", zorder=26)
    ax.text(DX(-92), DY(62), "ext. light\nblocked by lip", fontsize=5.8,
            color="#A05000", ha="left", va="center", **FONT)

    # cam-latch compression (panel pulled onto the seal)
    ax.annotate("", xy=(DX(2), DY(158)), xytext=(DX(34), DY(158)),
                arrowprops=dict(arrowstyle="-|>", color=C_CL, lw=1.8), zorder=25)

    # floor-gap dimension (interior side, clear lane)
    ax.annotate("", xy=(DX(52), DY(0)), xytext=(DX(52), DY(80)),
                arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=1.0), zorder=25)
    ax.text(DX(56), DY(40), "80 mm\nfloor gap", fontsize=5.8, color=C_DIM,
            ha="left", va="center", **FONT)

    # callout labels (right side, leaders pointing into the detail)
    def dlbl(target, ty, text):
        tx = DX(92)
        ax.annotate("", xy=target, xytext=(tx - 6, ty),
                    arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.8,
                                    shrinkA=1, shrinkB=1), zorder=24)
        ax.text(tx, ty, text, fontsize=6.0, color=C_DIM, ha="left", va="center", **FONT)
    dlbl((DX(20), DY(165)), DY(172), "Cam latch compresses panel\nonto seal (release to slide)")
    dlbl((DX(20), DY(120)), DY(138), "Panel bottom edge\n(40 mm corner zone)")
    dlbl((DX(-10), DY(100)), DY(108), "20 mm EPDM — panel\nrecedes into / seals on lip")
    dlbl((DX(-26), DY(64)), DY(74), "Frame seal lip — steel upstand\nfrom threshold (notched at drum)")
    dlbl((DX(-40), DY(22)), DY(34), "Fixed door-frame\nthreshold (50×50 RHS)")
    dlbl((DX(74), DY(28)), DY(6), "50 mm tray rim —\n30 mm clearance")

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL C — Panel top light seal (enlarged), the mirror of Detail B.
    # The panel hangs below the ceiling rails, leaving a gap between the panel
    # top and the frame top rail. A frame top seal lip (downstand) closes it; a
    # 20mm EPDM strip on the panel top edge compresses against it under the upper
    # cam latches. The drum does not reach the top, so the lip runs the full
    # width as one continuous member (meets across the center).
    # ══════════════════════════════════════════════════════════════════════════
    ox2, oy2 = 980, 1760
    def CX(d): return ox2 + k * d         # depth (mm) → sheet x  (exterior negative)
    def CY(hh): return oy2 + k * hh       # height about panel-top edge (h=0) → sheet y

    cbx0, cbx1 = CX(-98), CX(178)
    cby0, cby1 = CY(-108), CY(102)
    ax.add_patch(Rectangle((cbx0, cby0), cbx1 - cbx0, cby1 - cby0,
                           fc="#FBFBFD", ec=C_DIM, lw=1.0, ls=(0, (5, 3)), zorder=2))
    ax.text((cbx0 + cbx1) / 2, cby1 + 34, "DETAIL C — PANEL TOP SEAL",
            ha="center", va="bottom", fontsize=9, fontweight="bold", color=C_OUT, **FONT)
    ax.text((cbx0 + cbx1) / 2, cby1 + 10,
            "operational position  ·  mirror of Detail B  ·  lip runs full width (meets at center)",
            ha="center", va="bottom", fontsize=6.4, color=C_DIM, **FONT)
    ax.text(CX(-90), CY(-95), "EXTERIOR", fontsize=6, color="#5060A0",
            ha="left", va="center", fontweight="bold", **FONT)
    ax.text(CX(170), CY(-95), "INTERIOR", fontsize=6, color="#407040",
            ha="right", va="center", fontweight="bold", **FONT)

    # ceiling / frame top + hatch above (h = +90 is the frame top / ceiling line)
    ax.add_patch(Rectangle((cbx0, CY(90)), cbx1 - cbx0, CY(102) - CY(90),
                           fc="#ECECEC", ec="none", hatch="////", lw=0, zorder=19))
    ax.plot([cbx0, cbx1], [CY(90), CY(90)], color=C_OUT, lw=2.2, zorder=22)

    # frame top rail, top seal lip (downstand), EPDM, panel top edge, ceiling rail
    ax.add_patch(Rectangle((CX(-50), CY(40)), k * 50, k * 50,
                           fc=C_STEEL, ec=C_OUT, lw=1.2, zorder=21))      # frame top rail
    ax.add_patch(Rectangle((CX(-32), CY(-30)), k * 12, k * 120,
                           fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=23))      # top seal lip
    ax.add_patch(Rectangle((CX(-20), CY(-40)), k * 20, k * 40,
                           fc=C_GASKT, ec=C_OUT, lw=1.0, zorder=24))      # EPDM
    ax.add_patch(Rectangle((CX(0), CY(-100)), k * 40, k * 100,
                           fc=C_ALUM, ec=C_OUT, lw=1.3, zorder=22))       # panel top

    # exterior light ray (in the gap above the panel top) blocked by the lip
    ax.annotate("", xy=(CX(-33), CY(18)), xytext=(CX(-92), CY(18)),
                arrowprops=dict(arrowstyle="-|>", color="#D08000", lw=1.6), zorder=25)
    ax.plot([CX(-30)], [CY(18)], marker="x", ms=7, mew=2.2, color="#C02020", zorder=26)
    ax.text(CX(-92), CY(-6), "ext. light\nblocked by lip", fontsize=5.8,
            color="#A05000", ha="left", va="center", **FONT)

    # upper cam-latch compression (panel pulled onto the seal)
    ax.annotate("", xy=(CX(2), CY(-58)), xytext=(CX(34), CY(-58)),
                arrowprops=dict(arrowstyle="-|>", color=C_CL, lw=1.8), zorder=25)

    def clbl(target, ty, text):
        tx = CX(92)
        ax.annotate("", xy=target, xytext=(tx - 6, ty),
                    arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.8,
                                    shrinkA=1, shrinkB=1), zorder=24)
        ax.text(tx, ty, text, fontsize=6.0, color=C_DIM, ha="left", va="center", **FONT)
    clbl((CX(30), CY(55)), CY(96), "Panel hangs below the ceiling\nrails — this gap is the light path")
    clbl((CX(-40), CY(64)), CY(62), "Frame top rail (50×50 RHS)")
    clbl((CX(-26), CY(30)), CY(28), "Top seal lip — steel downstand,\nfull width (continuous, meets at center)")
    clbl((CX(-10), CY(-20)), CY(-10), "20 mm EPDM — panel top\nedge seals on lip")
    clbl((CX(20), CY(-70)), CY(-58), "Upper cam latch compresses\npanel onto seal")
    clbl((CX(20), CY(-95)), CY(-92), "Panel top edge")

    # ── Title block (portrait sheet — taller box, smaller fonts, clipped) ──────
    title_block(ax, "SHEET 3 OF 6",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="DRUM ELEVATION — SECTION A-A: VERTICAL DRUM, WALKING HEIGHT",
                scale_note="EQUAL ASPECT  \u00b7  SCALE 1:20 (APPROX)  \u00b7  ALL DIMS IN mm",
                doc_id="TBS-001 \u00b7 Hinged Light-Trap Panel",
                height=0.05, portrait=True)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet3.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet3.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 4  —  Sliding Rail Transport System (plan view at floor level)
#
# Shows: panel slide rails (HGR20), drum dolly tracks (V-groove), fixed door
# frame, and both operational / transport positions.
#
# Horizontal axis = X (container long axis, 0 = wall inner face at cargo door)
# Vertical axis   = Yd (container width, 0 = pinhole wall)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet4():
    import matplotlib.patches as mpatches
    from tbs_constants import (C_WID, PANEL_CORNER_T, PANEL_CENTER_T,
                               PANEL_CORNER_YD_L, PANEL_CORNER_YD_R, PANEL_SLIDE,
                               ZONE_L_END, WALL_T as C_WALL_T)

    # ── Layout constants ─────────────────────────────────────────────────────
    # Plan view:  horizontal = Yd (container width, 0 → C_WID)
    #             vertical   = X  (depth from wall inner face, positive inward)
    # This matches the Sheet 2 convention and the floorplan left-end detail.
    PANEL_CT = PANEL_CORNER_T   # = 40mm
    PANEL_CC = PANEL_CENTER_T   # = 120mm
    SLIDE_P  = PANEL_SLIDE      # = 300mm
    DR       = DRUM_R           # = 375mm (light trap drum)

    # Positions in each mode (X = depth from wall inner face)
    OP_PANEL_X = 0
    TR_PANEL_X = SLIDE_P        # = 300

    # ── Figure — landscape, Yd horizontal, X vertical ────────────────────────
    # Yd range is ~3100mm but X range is only ~840mm. Increase vertical padding
    # so the diagram fills the figure and text is readable.
    PAD_L = 350     # left of Yd=0 — room for dims + slide labels
    PAD_R = 380     # right of Yd=C_WID — room for legend + callouts
    PAD_B = 550     # below wall exterior — room for notes + title block
    PAD_T = 500     # above ZONE_L_END — room for dim lines + headroom

    YD_LO = -PAD_L
    YD_HI = C_WID + PAD_R
    X_LO  = -C_WALL_T - PAD_B
    X_HI  = ZONE_L_END + PAD_T

    fig, ax = plt.subplots(figsize=(18, 12))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(YD_LO, YD_HI)
    ax.set_ylim(X_LO, X_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Axis labels ──────────────────────────────────────────────────────────
    ax.text(C_WID / 2, X_LO + 15, "Yd  (container width)  →",
            ha="center", va="bottom", fontsize=7, color=C_DIM,
            **FONT, zorder=15, style="italic")
    ax.text(YD_LO + 15, ZONE_L_END / 2,
            "X  (depth from wall)  →",
            ha="left", va="center", fontsize=7, color=C_DIM,
            **FONT, zorder=15, style="italic", rotation=90)

    # ── Background zone tints ────────────────────────────────────────────────
    # Exterior zone (below wall)
    ax.add_patch(Rectangle((YD_LO, X_LO), YD_HI - YD_LO, C_WALL_T + PAD_B,
                            fc="#F0EDE8", ec="none", zorder=1))
    ax.text(C_WID / 2, X_LO + 70,
            "EXTERIOR", color="#806050", fontsize=8, ha="center", va="bottom",
            fontweight="bold", **FONT, zorder=2, alpha=0.5)
    # Interior zone (above wall)
    ax.add_patch(Rectangle((YD_LO, 0), YD_HI - YD_LO, X_HI,
                            fc="#F8FAF8", ec="none", zorder=1))

    # ── Container wall (X = -C_WALL_T to 0) — horizontal band ───────────────
    ax.add_patch(Rectangle((0, -C_WALL_T), C_WID, C_WALL_T,
                            fc=C_STEEL, ec=C_OUT, lw=1.5, hatch="///", zorder=3))
    ax.text(-60, -C_WALL_T / 2, f"{int(C_WALL_T)}mm WALL",
            ha="right", va="center", fontsize=6, color=C_DIM,
            fontweight="bold", **FONT, zorder=15)

    # ── Door closure plane (exterior face of wall at X = -C_WALL_T) ──────────
    ax.plot([YD_LO + 60, YD_HI - 60], [-C_WALL_T, -C_WALL_T],
            color="#804020", lw=1.2, ls=":", zorder=4, alpha=0.7)
    ax.text(C_WID + 80, -C_WALL_T + 20, "DOOR CLOSURE PLANE",
            ha="left", va="center", fontsize=6, color="#804020",
            fontweight="bold", **FONT, zorder=15)

    # ── Fixed door frame (at X=0, 50mm RHS) ─────────────────────────────────
    FRAME_W = 50
    ax.add_patch(Rectangle((0, 0), C_WID, FRAME_W,
                            fc="none", ec="#806010", lw=2.0, ls="--", zorder=5))
    leader(ax, (C_WID - 100, FRAME_W / 2), (C_WID + 175, 25),
           "FIXED DOOR FRAME\n50×50mm RHS · SEAL LANDING", col="#806010", fs=6)

    # ── ZONE_L_END boundary ──────────────────────────────────────────────────
    ax.plot([YD_LO + 60, YD_HI - 60], [ZONE_L_END, ZONE_L_END],
            color="#20A020", lw=1.5, ls=(0, (8, 4)), zorder=4, alpha=0.7)
    ax.text(C_WID + 80, ZONE_L_END + 20,
            f"ZONE_L_END = {ZONE_L_END}mm",
            ha="left", va="center", fontsize=6.5, color="#20A020",
            fontweight="bold", **FONT, zorder=15)
    ax.text(C_WID + 80, ZONE_L_END - 35,
            "(FILM PLANE LEFT EDGE)",
            ha="left", va="center", fontsize=5.5, color="#20A020",
            **FONT, zorder=15)

    # ── Helper: draw panel at given X offset ─────────────────────────────────
    def draw_panel(x_off, alpha=1.0, label=""):
        """Draw stepped panel. Yd = horizontal, X = vertical."""
        # Corner zone near (Yd=0 to PANEL_CORNER_YD_L) — 40mm thick
        ax.add_patch(Rectangle((0, x_off), PANEL_CORNER_YD_L, PANEL_CT,
                                fc=C_ALUM, ec=C_OUT, lw=1.0, alpha=alpha, zorder=6))
        # Center zone (Yd=PANEL_CORNER_YD_L to PANEL_CORNER_YD_R) — 120mm thick
        ax.add_patch(Rectangle((PANEL_CORNER_YD_L, x_off),
                                PANEL_CORNER_YD_R - PANEL_CORNER_YD_L, PANEL_CC,
                                fc=C_STEEL, ec=C_OUT, lw=1.0, alpha=alpha, zorder=6))
        # Corner zone far (Yd=PANEL_CORNER_YD_R to C_WID) — 40mm thick
        ax.add_patch(Rectangle((PANEL_CORNER_YD_R, x_off),
                                C_WID - PANEL_CORNER_YD_R, PANEL_CT,
                                fc=C_ALUM, ec=C_OUT, lw=1.0, alpha=alpha, zorder=6))
        # Light trap drum circle
        drum_yd = C_WID / 2    # centered in container width
        drum_x = x_off + 40    # drum center is 40mm from panel inner face
        ax.add_patch(Circle((drum_yd, drum_x), DR,
                            fc=C_LT_DRUM, ec=C_OUT, lw=1.5,
                            alpha=alpha * 0.7, zorder=7))
        if label:
            ax.text(drum_yd, drum_x, label,
                    ha="center", va="center", fontsize=7, color=C_OUT,
                    fontweight="bold", **FONT, alpha=alpha, zorder=15)

    # (waste drums eliminated in rev 5 — panel slide only)

    # ── Draw OPERATIONAL position (solid) ─────────────────────────────────────
    draw_panel(OP_PANEL_X, alpha=0.9, label="OPERATIONAL\nPANEL")

    # ── Draw TRANSPORT position (ghost) ───────────────────────────────────────
    draw_panel(TR_PANEL_X, alpha=0.20, label="TRANSPORT\nPANEL")

    # ── Slide arrows — panel ─────────────────────────────────────────────────
    # Arrow between operational and transport panel positions, in the gap
    # between D-1 and D-2 (around Yd=1181, the drum center)
    arr_yd_p = C_WID / 2    # center of container width — clear area
    arr_x0 = OP_PANEL_X + PANEL_CT / 2
    arr_x1 = TR_PANEL_X + PANEL_CT / 2
    ax.annotate("", xy=(arr_yd_p, arr_x1), xytext=(arr_yd_p, arr_x0),
                arrowprops=dict(arrowstyle="->,head_length=0.6,head_width=0.4",
                                color="#C04010", lw=2.0,
                                connectionstyle="arc3,rad=0.3",
                                mutation_scale=12), zorder=15)
    ax.text(arr_yd_p + 80, (arr_x0 + arr_x1) / 2 + 120,
            f"PANEL SLIDE\n{SLIDE_P}mm",
            ha="left", va="center", fontsize=6.5, color="#C04010",
            fontweight="bold", **FONT, zorder=15)

    # (drum slide arrows removed — drums eliminated in rev 5)

    # ── HGR20 rail indicators (along Yd edges, near floor/ceiling) ───────────
    RAIL_X_START = -30
    RAIL_X_END = SLIDE_P + 150
    for yd_pos, offset, ha_pos in [
        (30,        -15, "right"),
        (C_WID - 30, 15, "left")
    ]:
        ax.plot([yd_pos, yd_pos], [RAIL_X_START, RAIL_X_END],
                color="#404040", lw=3.0, zorder=3, alpha=0.5)
    # (V-groove tracks removed — dolly tracks eliminated in rev 5)

    # ── Carriage beam (dashed rectangle, full height at X=0) ─────────────────
    BEAM_W = 60
    ax.add_patch(Rectangle((0, OP_PANEL_X - 5), C_WID, BEAM_W,
                            fc="none", ec="#C04010", lw=1.5, ls="--",
                            alpha=0.5, zorder=5))
    leader(ax, (C_WID - 100, BEAM_W / 2), (C_WID + 130, 250),
           "CARRIAGE BEAM\n60×60mm SHS", col="#C04010", fs=6)

    # ── Lock position labels ────────────────────────────────────────────────
    # Operational lock at X=0 — label on left side, well below transport lock
    ax.plot([YD_LO + 60, 0], [OP_PANEL_X, OP_PANEL_X],
            color="#20A060", lw=1.0, ls="--", zorder=4)
    ax.text(YD_LO + 60, OP_PANEL_X + 20,
            "OPERATIONAL LOCK (X=0)",
            ha="left", va="top", fontsize=5.5, color="#20A060",
            fontweight="bold", **FONT, zorder=15)

    # Transport lock at X=SLIDE_P — label on left side
    ax.plot([YD_LO + 60, 0], [TR_PANEL_X, TR_PANEL_X],
            color="#C04010", lw=1.0, ls="--", zorder=4)
    ax.text(YD_LO + 60, TR_PANEL_X + 10,
            f"TRANSPORT LOCK (X={SLIDE_P}mm)",
            ha="left", va="bottom", fontsize=5.5, color="#C04010",
            fontweight="bold", **FONT, zorder=15)

    # ── Dimension lines ──────────────────────────────────────────────────────
    # Panel thickness dims — use leaders into the panel zones for clarity
    # Corner zone thickness
    leader(ax, (PANEL_CORNER_YD_L / 2, PANEL_CT / 2),
           (YD_LO + 160, PANEL_CT + 60),
           f"{PANEL_CT}mm CORNER ZONE", col=C_DIM, fs=6)

    # Center zone thickness
    leader(ax, (C_WID / 2, PANEL_CC - 10),
           (C_WID / 2 + 350, PANEL_CC + 60),
           f"{PANEL_CC}mm CENTER ZONE", col=C_DIM, fs=6)

    # (waste drum dimensions removed — drums eliminated in rev 5)

    # Step transition Yd widths (top edge, well above ZONE_L_END)
    _dim_top = ZONE_L_END + 60
    dim_h(ax, 0, PANEL_CORNER_YD_L, _dim_top,
          f"{PANEL_CORNER_YD_L}mm", offset=15, fs=6)
    dim_h(ax, PANEL_CORNER_YD_L, PANEL_CORNER_YD_R, _dim_top,
          f"{PANEL_CORNER_YD_R - PANEL_CORNER_YD_L}mm (CENTER)", offset=15, fs=6)
    dim_h(ax, PANEL_CORNER_YD_R, C_WID, _dim_top,
          f"{C_WID - PANEL_CORNER_YD_R}mm", offset=15, fs=6)

    # ── Notes (left-justified, bottom left) ─────────────────────────────────
    from tbs_constants import PANEL_FLOOR_GAP, PROC_TRAY_RIM
    notes = [
        f"TRANSPORT MODE",
        f"1. Slide panel inward {SLIDE_P}mm (single slide only — drums eliminated).",
        "2. Light trap drum exterior edge clears door closure plane by 5mm.",
        f"3. Panel suspended from ceiling HGR20 rails — {PANEL_FLOOR_GAP}mm floor gap clears {PROC_TRAY_RIM}mm tray rim.",
        "4. Single-person operation, ~5 minutes per mode conversion.",
        "5. Panel locks: 2× Destaco 207-U toggle clamps per position.",
        "6. See ceiling-rail-sheet1/2 for rail suspension detail.",
    ]
    notes_x = YD_LO + 50
    notes_y_top = X_LO + 150 + (len(notes) - 1) * 26
    draw_notes(ax, notes, notes_x, notes_y_top, spacing=33,
               fs=7, title_fs=7, color=C_DIM, title_color=C_DIM,
               width=1070, font=FONT)

    # ── Legend (right side, stacked vertically) ─────────────────────────────
    legend_top = X_LO + 122 + len(notes) * 26 + 10 + 4 * 30 + 50
    draw_legend(ax, [
        (C_ALUM,   0.9,  "Corner zone (40mm)"),
        (C_STEEL,  0.9,  "Center zone (120mm)"),
        (C_LT_DRUM, 0.7,  "Light trap drum"),
        (C_STEEL,  0.20, "Transport (ghost)"),
    ], C_WID + 70, legend_top, row_h=30, swatch_w=20, swatch_h=14,
       col_w=300, fs=5.5, font=FONT)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 4 OF 6",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="SLIDING RAIL TRANSPORT SYSTEM — PLAN VIEW AT FLOOR LEVEL",
                scale_note="EQUAL ASPECT  \u00b7  ALL DIMS IN mm  \u00b7  SOLID = OPERATIONAL, GHOST = TRANSPORT",
                doc_id="TBS-001 \u00b7 Hinged Light-Trap Panel",
                height=0.06)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet4.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet4.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 5  —  Drum access & light-tightness analysis (design review)
# Tests the Ø750 / 4-fin revolving drum against two questions:
#   A. Can a person fit through a 90° sector?
#   B. As the drum rotates, can daylight enter the container?
# Both currently fail — this sheet shows why.
# ═════════════════════════════════════════════════════════════════════════════

def sheet5():
    R, OR = DRUM_R, LT_DRUM_OR             # housing 450, drum outer 432
    BORE = OR - 3                           # bore radius (~Ø850)
    OD = LT_OPENING_DEG                      # 80
    SHO, DEP = 520, 330                      # person plan footprint
    GREEN, RED, AMBER = "#2E8B57", "#C0202A", "#D08000"
    HOUS, DRUMC, BLUE = "#9A9AA2", "#C9A86B", "#3060A0"

    fig, ax = plt.subplots(figsize=(20, 13.6))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(-130, 2130); ax.set_ylim(-260, 1380)
    ax.set_aspect("equal"); ax.axis("off")

    def arc(cx, cy, r, gaps, lw, color, z=5):
        deg = np.arange(0, 360.4, 0.4); openm = np.zeros(deg.shape, bool)
        for gc, gw in gaps:
            openm |= np.abs((deg - gc + 180) % 360 - 180) <= gw / 2
        th = np.radians(deg)
        ax.plot(np.where(openm, np.nan, cx + r * np.cos(th)),
                np.where(openm, np.nan, cy + r * np.sin(th)),
                color=color, lw=lw, solid_capstyle="butt", zorder=z)

    def zones(cx, cy, w):
        ax.add_patch(Rectangle((cx - w, cy - w), 2 * w, w, fc="#EEF2F8", ec="none", zorder=1))
        ax.add_patch(Rectangle((cx - w, cy), 2 * w, w, fc="#EEF6EE", ec="none", zorder=1))
        ax.plot([cx - w, cx + w], [cy, cy], color=C_DIM, lw=0.8, ls=(0, (5, 3)), zorder=2)

    def sun(x, y, s=28):
        ax.add_patch(Circle((x, y), s, fc="#FFD24D", ec=AMBER, lw=1.2, zorder=8))
        for a in range(0, 360, 45):
            r = np.radians(a)
            ax.plot([x + s * 1.2 * np.cos(r), x + s * 1.7 * np.cos(r)],
                    [y + s * 1.2 * np.sin(r), y + s * 1.7 * np.sin(r)], color=AMBER, lw=1.3, zorder=8)

    ax.text(1000, 1335, "REVOLVING-DOOR LIGHT LOCK (rev 8) — PASSES BOTH TESTS",
            ha="center", fontsize=15, fontweight="bold", color=C_OUT, **FONT)
    ax.text(1000, 1298, "Fixed Ø900 housing (two 80° openings, 180° apart) + single-opening C-shell drum, NO fins",
            ha="center", fontsize=9, color=GREEN, **FONT)
    ax.plot([-130, 2130], [660, 660], color=C_DIM, lw=1.0, ls=(0, (6, 4)), zorder=3)

    # ── PANEL A — person fit ──
    ax.text(-110, 1230, "A.  PERSON FIT  —  open Ø850 bore, no fins", ha="left",
            fontsize=12, fontweight="bold", color=C_OUT, **FONT)
    Acx, Acy, s = 470, 940, 0.78
    Rd, ORd = R * s, OR * s
    zones(Acx, Acy, Rd + 64)
    arc(Acx, Acy, Rd, [(90, OD), (270, OD)], 6, HOUS, 5)
    arc(Acx, Acy, ORd, [(270, OD)], 4, DRUMC, 6)
    ax.add_patch(Ellipse((Acx, Acy), SHO * s, DEP * s, fc=GREEN, ec="#16613a",
                         lw=1.3, alpha=0.40, zorder=7))
    ax.text(Acx, Acy, "operator\n~520×330\nfits the bore", fontsize=6.8, color="#16613a",
            **FONT, ha="center", va="center", zorder=8)
    ax.text(Acx, Acy - Rd - 46, "EXTERIOR (enter)", fontsize=7.5, color=BLUE, **FONT,
            fontweight="bold", ha="center")
    ax.text(Acx, Acy + Rd + 46, "INTERIOR / walkway (exit)", fontsize=7.5, color=GREEN,
            **FONT, fontweight="bold", ha="center")
    axv0, ayv0, axv1, ayv1 = 905, 720, 2090, 1190
    ax.add_patch(FancyBboxPatch((axv0, ayv0), axv1 - axv0, ayv1 - ayv0,
                                boxstyle="round,pad=6,rounding_size=14",
                                fc="#EAF6EE", ec=GREEN, lw=1.6, zorder=2))
    ax.text(axv0 + 26, ayv1 - 34, "VERDICT  ✓  PASS — fits", ha="left", va="center",
            fontsize=12, fontweight="bold", color=GREEN, **FONT)
    for i, line in enumerate([
        "• The four radial fins are GONE — the drum is a single-opening",
        "  C-shell, so the whole ~Ø850 bore is clear standing space.",
        f"• Passage ≈ 625mm (the {OD}° opening on the Ø900 housing); a single",
        "  operator (~520 × 330mm in plan) enters and turns inside.",
        "• Emergency egress is still the whole panel swinging open.",
    ]):
        ax.text(axv0 + 26, ayv1 - 84 - i * 52, line, ha="left", va="center",
                fontsize=8.6, color="#16361f", **FONT)

    # ── PANEL B — light-tight at every rotation ──
    ax.text(-110, 588, "B.  LIGHT-TIGHT AT EVERY ROTATION", ha="left", fontsize=12,
            fontweight="bold", color=C_OUT, **FONT)
    Bcy, bs = 350, 0.52
    Rd, ORd = R * bs, OR * bs
    for bx, (da, ttl, desc) in zip(
            [370, 1090, 1810],
            [(270, "1 · ENTER", "exterior open; interior\ncovered by drum →\nlight enters bore, no exit"),
             (0,   "2 · TRANSIT", "drum opening at the side;\nboth openings covered →\nfully sealed"),
             (90,  "3 · EXIT", "interior open to walkway;\nexterior covered by drum →\nno daylight enters")]):
        zones(bx, Bcy, Rd + 58)
        arc(bx, Bcy, Rd, [(90, OD), (270, OD)], 5, HOUS, 5)
        arc(bx, Bcy, ORd, [(da, OD)], 4, DRUMC, 6)
        sun(bx - Rd - 30, Bcy - Rd * 0.5)
        ax.text(bx, Bcy + Rd + 60, ttl, ha="center", fontsize=9.5, fontweight="bold", color=GREEN, **FONT)
        ax.text(bx, Bcy - Rd - 48, desc, ha="center", va="top", fontsize=7, color=C_DIM, **FONT)
        if da == 270:   # ray enters bore, blocked at interior
            ax.annotate("", xy=(bx, Bcy + ORd * 0.92), xytext=(bx, Bcy - Rd - 24),
                        arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=2.0), zorder=9)
            ax.plot([bx], [Bcy + ORd], marker="x", ms=9, mew=2.4, color=GREEN, zorder=10)
        else:           # blocked at exterior face
            ax.annotate("", xy=(bx, Bcy - ORd * 0.92), xytext=(bx, Bcy - Rd - 24),
                        arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=2.0), zorder=9)
            ax.plot([bx], [Bcy - ORd], marker="x", ms=9, mew=2.4, color=GREEN, zorder=10)
    ax.add_patch(FancyBboxPatch((-110, -250), 2220, 196,
                                boxstyle="round,pad=6,rounding_size=12",
                                fc="#EAF6EE", ec=GREEN, lw=1.6, zorder=2))
    ax.text(-78, -86, "VERDICT  ✓  PASS — no daylight path at any rotation", ha="left",
            va="center", fontsize=12.5, fontweight="bold", color=GREEN, **FONT)
    for i, line in enumerate([
        "The two housing openings are 80° wide and 180° apart, so the 80° drum opening can never reach both at once.",
        "The housing's solid wall always covers the opening the drum isn't aligned with — light enters the bore but",
        "never exits to the interior. A fixed housing (the panel aperture is no longer relied on as the seal) does the work.",
    ]):
        ax.text(-78, -130 - i * 38, line, ha="left", va="center", fontsize=8.4, color="#16361f", **FONT)

    title_block(ax, "SHEET 5 OF 6",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="REVOLVING-DOOR LIGHT LOCK (rev 8) — ACCESS & LIGHT-TIGHTNESS VERIFICATION (BOTH PASS)",
                scale_note="PLAN VIEWS · NOT TO SCALE · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.045)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet5.png"), dpi=130,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet5.png saved")




def sheet6():
    """Transport-slide clearance vs the film-plane left mechanism (plan)."""
    RED, GREEN = "#C0202A", "#2E8B57"
    D0, D1 = BRACE_LEFT_DEMOUNT_Y0, BRACE_LEFT_DEMOUNT_Y1   # 731, 1631
    RX, SL, PT_ = RAIL_X_L, PANEL_SLIDE, PANEL_CENTER_T     # 150, 550, 120
    cyd = PW / 2                                            # 1181 light-lock Yd centre

    fig, ax = plt.subplots(figsize=(17, 12))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(-280, 2360); ax.set_ylim(-360, 2700)
    ax.set_aspect("equal"); ax.axis("off")

    ax.add_patch(Rectangle((0, 0), 1340, PW, fc="#EEF6EE", ec="none", zorder=0))
    ax.plot([-280, 1340], [0, 0], color=C_OUT, lw=2, zorder=3)
    ax.plot([-280, 1340], [PW, PW], color=C_OUT, lw=2, zorder=3)
    ax.text(-270, -80, "near wall (Yd=0)", fontsize=7.5, color=C_DIM, **FONT)
    ax.text(-270, PW + 35, "far wall (Yd=2362)", fontsize=7.5, color=C_DIM, **FONT)
    ax.plot([0, 0], [0, PW], color=C_CL, lw=1.4, ls=(0, (6, 4)), zorder=3)
    ax.text(10, PW + 95, "door plane X=0", fontsize=8, color=C_CL, **FONT)

    # film-plane left rail at X=150 (fixed ends + demount centre)
    for ya, yb, c in [(FP_Y_MIN, D0, C_STEEL), (D1, FP_Y + 38, C_STEEL), (D0, D1, C_LIGHT)]:
        ax.add_patch(Rectangle((RX - 13, ya), 26, yb - ya, fc=c, ec=C_OUT, lw=1, zorder=6))
    ax.text(RX, (D0 + D1) / 2, "left rail X=150\n· demount centre\n(drum zone only)",
            fontsize=6, color="#8a5a10", **FONT, ha="center", va="center", zorder=12)
    # brace-cage beams (run X 150->4649) at Yd 100 & 2262
    for yy in (FP_Y_MIN, FP_Y):
        ax.add_patch(Rectangle((RX, yy - 17), 1340 - RX, 34, fc=C_STEEL, ec=C_OUT,
                               lw=0.7, alpha=0.85, zorder=5))
    ax.text(1320, FP_Y_MIN - 60, "brace-cage beam (X 150→4649) →", fontsize=7, color=C_DIM, **FONT, ha="right")
    ax.text(1320, FP_Y + 52, "brace beam + muslin screen (Yd≈2262) →", fontsize=7, color=C_DIM, **FONT, ha="right")
    for yy in (FP_Y_MIN, FP_Y):                              # corner posts at X=150
        ax.add_patch(Rectangle((RX - 27, yy - 27), 54, 54, fc="#5A5A62", ec=C_OUT, lw=1, zorder=7))

    # hinged panel — deployed + transport ghost
    ax.add_patch(Rectangle((0, 0), PT_, PW, fc=C_ALUM, ec=C_OUT, lw=1.2, zorder=8))
    ax.text(PT_ / 2, -140, "panel\ndeployed", fontsize=7, color=C_DIM, **FONT, ha="center", va="top")
    ax.add_patch(Rectangle((SL, 0), PT_, PW, fc=C_ALUM, ec=RED, lw=1.6, ls=(0, (5, 3)),
                           alpha=0.30, zorder=9))
    ax.text(SL + PT_ / 2, -140, f"panel TRANSPORT\n(slid +{int(SL)})", fontsize=7.5,
            color=RED, **FONT, ha="center", va="top", fontweight="bold")
    ax.add_patch(Circle((0, cyd), DRUM_R, fc=C_ALUM, ec="#7a5a20", lw=1.0, alpha=0.45, zorder=8))
    ax.add_patch(Circle((SL, cyd), DRUM_R, fc=C_ALUM, ec=RED, lw=1.0, ls=(0, (4, 3)), alpha=0.16, zorder=9))
    ax.text(SL, cyd, "housing\ndrum-zone rail\ndemounted ✓\n(clears)", fontsize=6.4,
            color=GREEN, **FONT, ha="center", va="center", zorder=12)
    ax.annotate("", xy=(SL - 8, 1181), xytext=(PT_ + 20, 1181),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.0), zorder=11)
    ax.text((PT_ + SL) / 2, 1240, f"{int(SL)}mm slide", fontsize=7.5, color=RED, **FONT, ha="center")

    # numbered collision markers
    def mark(x, y, n):
        ax.add_patch(Circle((x, y), 58, fc="white", ec=RED, lw=2.2, zorder=14))
        ax.text(x, y, str(n), fontsize=12, color=RED, **FONT, fontweight="bold",
                ha="center", va="center", zorder=15)
    mark(RX, 430, 1); mark(RX, 1940, 1)
    mark(SL + PT_ / 2, FP_Y_MIN, 2); mark(SL + PT_ / 2, FP_Y, 2)

    ax.text(-280, 2640, "TRANSPORT SLIDE vs FILM-PLANE LEFT MECHANISM  (plan, looking down)",
            fontsize=13, fontweight="bold", color=C_OUT, **FONT)
    notes = ("THE ISSUE — the ~550mm transport slide sweeps the\n"
             "panel through X=150 (the film-plane left edge).\n\n"
             "①  Panel CORNERS hit the FIXED left-rail segments.\n"
             "    The operational demount segment (amber) clears\n"
             "    only the drum zone (Yd 731–1631), not the corners.\n\n"
             "②  Panel BAND overlaps the lengthwise brace-cage\n"
             "    beams (Yd≈100 & 2262) and the muslin screen.\n\n"
             "The housing itself clears — its drum-zone rail is\n"
             "demounted (green).\n\n"
             "NOT a regression: the panel always slid past X=150\n"
             "(rev 8 only deepened the slide 300→550mm).\n\n"
             "RESOLUTION (Hinged Panel Report §5.4) — strike the\n"
             "film plane FIRST: remove muslin screen → knock down\n"
             "the brace cage → remove the FULL left rail → lift the\n"
             "walkway → release latches → slide ~550mm → lock.")
    ax.add_patch(FancyBboxPatch((1440, 360), 880, 2150,
                                boxstyle="round,pad=8,rounding_size=16",
                                fc="#FBFBFD", ec=C_DIM, lw=1.0, zorder=2))
    ax.text(1470, 2440, notes, fontsize=8.6, color="#26323a", **FONT, va="top", zorder=12)

    title_block(ax, "SHEET 6 OF 6",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="TRANSPORT-SLIDE CLEARANCE vs FILM-PLANE LEFT MECHANISM — STRIKE FILM PLANE BEFORE SLIDING",
                scale_note="PLAN VIEW · NOT TO SCALE · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.045)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet6.png"), dpi=130,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet6.png saved")

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating hinged light-trap panel drawings...")
    sheet1()
    sheet2()
    sheet3()
    sheet4()
    sheet5()
    sheet6()
    print("Done.")
