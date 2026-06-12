#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_hingepanel_diagram.py  —  TBS-001 Hinged Light-Trap Panel

Sheet 1 — Front elevation (exterior view, 1:20):
  Panel dimensions, revolving drum position, hinges, latches, EPDM perimeter seal.
  Stepped profile: 40mm corner zones, 120mm center zone (drum housing).

Sheet 2 — Plan cross-section (1:20 equal aspect):
  Panel thickness (center zone), housed revolving door (fixed Ø900 housing +
  single-opening C-shell drum, no fins; light-tight by geometry), container
  wall interface, EPDM gasket engagement, latch detail.

Sheet 3 — Drum vertical section:
  Drum elevation showing walking height, bearings, person silhouette.

Sheet 4 — Rotating transport system (rev10, supersedes the slide):
  the split panel + drum swing 56° about the vertical pivot post (the film
  far-left upright); camera (shut) vs swung (transport) positions, removable
  left film rails, top+bottom wall stays.
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
    RAIL_X_L,                                    # film-plane left rail (now continuous, B2)
    FP_Y_MIN, FP_Y, PANEL_CENTER_T, DRUM_CY, BAY_FRONT_X, BAY_WALL_T, PANEL_SKIN_T,
)
from tbs_title_block import title_block
from tbs_drawing import (draw_dim_h, draw_dim_v,
                         leader as _leader_shared, hatch_rect, draw_notes,
                         draw_legend)

# ── Palette (white engineering) ───────────────────────────────────────────────
BG      = "#FFFFFF"   # white background
C_OUT   = "#1A1A1A"   # outlines
C_CL    = "#2060A0"   # center lines (blue, dashed)
C_DIM   = "#404040"   # dimensions / annotation text
C_ALUM  = "#C8D8E8"   # aluminum (3mm corner core plate)
C_STEEL = "#B0B0B8"   # steel section fill
C_GASKT = "#5A3020"   # EPDM gasket fill
C_WOOD    = "#C9A36B"  # plywood — Fan B mount band (rev11 material legend)
C_PLASTIC = "#6E8CA0"  # 4mm PP plastic sheet — panel skins + B2 bay (rev11)
C_HOLLOW  = "#EEEEE8"  # framed hollow core between the PP skins (rev11)
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
DRUM_CX = PW / 2        # light-lock center X in panel (centerd horizontally)
DRUM_CY = DRUM_H / 2   # light-lock center Y

# ── Drawing helpers (wrappers around tbs_drawing shared functions) ────────────
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
    # EXTERIOR view (looking at the door from outside, +X): the near wall (Yd=0) is on the
    # RIGHT and the far wall (Yd=2362) on the LEFT — so the x-axis is REVERSED. This puts
    # Fan B (near corner) on the right and the far-left pivot post on the left.
    ax.set_xlim(PW + PAD_R, -PAD_L)
    ax.set_ylim(-PAD_B, PH + PAD_T)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(PW / 2, -PAD_B + 60, "EXTERIOR VIEW — near wall (Yd 0) at RIGHT, far wall at LEFT",
            ha="center", va="bottom", fontsize=7, color=C_DIM, **FONT, style="italic", zorder=20)

    # ── Panel body ────────────────────────────────────────────────────────────
    # Outer steel frame (50mm wide)
    ax.add_patch(Rectangle((0, 0), PW, PH, fc=C_STEEL, ec=C_OUT, lw=2.5, zorder=2))
    # Skin area (inset of frame): rev11 — 4mm PP plastic sheet (C_PLASTIC)
    FR = 55  # visible frame width at face
    ax.add_patch(Rectangle((FR, FR), PW - 2 * FR, PH - 2 * FR,
                            fc=C_PLASTIC, ec=C_OUT, lw=0.8, zorder=3))
    ax.text(PW / 4 - 275, PH * 0.62,
            "4mm PP PLASTIC SKIN\n(U-channel set; flat-black interior)",
            color=C_DIM, fontsize=6.5, ha="center", va="center", **FONT, zorder=15, alpha=0.8)
    # Fan B corner keeps an 18mm PLYWOOD mount band (bottom up to PANEL_FAN_BAND_Z)
    from tbs_constants import PANEL_FAN_BAND_Z as _PFBZ
    ax.add_patch(Rectangle((FR, FR), PANEL_CORNER_YD_L - FR, _PFBZ - FR,
                            fc=C_WOOD, ec=C_OUT, lw=0.8, zorder=3.2))
    ax.text(PANEL_CORNER_YD_L / 2, (_PFBZ + FR) / 2,
            "18mm PLY\nFAN-MOUNT BAND", color="#6a4010", fontsize=6,
            ha="center", va="center", fontweight="bold", **FONT, zorder=15, alpha=0.85)

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
            "40mm CORNER ZONE", color="#C04010", fontsize=6,
            ha="center", va="top", fontweight="bold", **FONT, zorder=15, alpha=0.7)
    ax.text((STEP_YD_L + STEP_YD_R) / 2, PH - 220,
            "120mm CENTER ZONE\n(DRUM HOUSING)", color="#C04010", fontsize=6,
            ha="center", va="top", fontweight="bold", **FONT, zorder=15, alpha=0.7)
    ax.text((STEP_YD_R + PW) / 2, PH - 120,
            "40mm CORNER ZONE", color="#C04010", fontsize=6,
            ha="center", va="top", fontweight="bold", **FONT, zorder=15, alpha=0.7)
    # Step dimension
    draw_dim_h(ax, STEP_YD_L, STEP_YD_R, -210,
          f"{STEP_YD_R - STEP_YD_L}mm CENTER ZONE (DRUM Ø{DRUM_D} + 50mm CLEARANCE EACH SIDE)", offset=20, fs=7, font=FONT)
    # ── Swing split (rev10): fixed-left / swinging / fixed-far + the vertical CUT lines ──
    # The fixed strips are bolted to the door FRAME (hatched); the swinging panel butts them
    # at the cut lines. Cut lines drawn bold and on top so they read at both panel edges.
    from tbs_constants import PANEL_CUT_YD as _CUT, FAR_STRIP_YD0 as _FAR
    for (y0, y1) in [(0, _CUT), (_FAR, PW)]:
        ax.add_patch(Rectangle((y0, FR), y1 - y0, PH - 2 * FR, fc="#C8A060",
                               ec="none", alpha=0.45, hatch="\\\\\\", zorder=4))
    for cx in [_CUT, _FAR]:
        ax.plot([cx, cx], [0, PH], color="#A000A0", lw=2.6, ls=(0, (5, 2)), zorder=11)
        ax.text(cx, PH + 35, f"CUT @ Yd{cx}\n(fixed ↔ swing)", color="#A000A0", fontsize=6,
                ha="center", va="bottom", fontweight="bold", **FONT, zorder=15)
    leader(ax, (_FAR + (PW - _FAR) / 2, PH / 2 - 250), (PW + 180, PH / 2 - 250),
           "FIXED FAR STRIP (Yd2287–2362)\nbolted to the door frame —\ndoes NOT swing", col="#6a4010", fs=6)
    leader(ax, (_CUT / 2, FR + 250), (-220, FR + 250),
           "FIXED LEFT PANEL (Yd0–180)\nbolted to the door frame —\ndoes NOT swing", col="#6a4010", fs=6)
    ax.text(PW / 2, FR + 70, "SWINGING PANEL  (Yd180 → 2287, pivots 56°)", color="#1763C8",
            fontsize=7, ha="center", va="bottom", fontweight="bold", **FONT, zorder=15, alpha=0.8)

    # ── Fan B intake — weatherproof louvre on the panel exterior (near corner) ──
    from tbs_constants import FAN_B_YD as _FBY, FAN_B_H as _FBH
    fb_w, fb_h = 200, 200
    ax.add_patch(Rectangle((_FBY - fb_w / 2, _FBH - fb_h / 2), fb_w, fb_h,
                           fc="#8090A0", ec=C_OUT, lw=1.3, zorder=6))
    for i in range(1, 5):
        yy = _FBH - fb_h / 2 + i * fb_h / 5
        ax.plot([_FBY - fb_w / 2, _FBY + fb_w / 2], [yy, yy], color=C_OUT, lw=0.6, zorder=7)
    leader(ax, (_FBY, _FBH - fb_h / 2), (_FBY + 200, _FBH - 200),
           "FAN B (intake) louvre\n(panel exterior — camera mode;\nswings with the panel)", col="#506070", fs=6)

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

    # Drum center line (vertical)
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
    HY = DY_BOT + DRUM_H * 0.45   # handle Y center (~900mm)
    HW = 110; HH = 42  # handle footprint
    # Place handle inside the drum body rectangle, 20mm clear of the interior drum wall.
    hx_handle = DX + DRUM_D - HW - 20
    ax.add_patch(Rectangle((hx_handle, HY - HH / 2), HW, HH,
                            fc="none", ec=C_OUT, lw=1.2, ls=(0, (4, 3)), zorder=7))
    leader(ax, (hx_handle + HW / 2, HY), (DX + DRUM_D + 130, HY + 200),
           "100mm PULL HANDLE\n(interior face — hidden;\nwelded, no through-hole)")

    # ── (rev10: the left-edge barrel hinges are RETIRED — the panel pivots on the
    #    Ø89 post at the FAR edge, not on left-edge hinges. The HINGE_* values are kept
    #    only as left-edge layout references for the swing note + dimension positions.) ──
    HINGE_YS = [220, 1190, PH - 230]
    HINGE_W = 85; HINGE_L = 220

    # ── Former HGR20 slide rails (rev10: RETIRED) ────────────────────────────
    # The old transport scheme slid the panel on HGR20 linear rails along the
    # container walls. rev10 supersedes it: the panel + drum SWING ~56° about the
    # Ø89 pivot post. The rail profiles below are drawn faint, labeled as the
    # retired route (see Sheet 4 for the rotation plan).
    C_RAIL = "#CC4422"   # red, matching assembly overview
    C_CARR = "#C04010"   # carriage beam color
    RAIL_H = 20          # rail cross-section height (visible in elevation)
    RAIL_LEN = 350       # visible rail length (extends behind panel, into page)

    # ── Transport: the panel + drum SWING about the vertical PIVOT POST ──────
    # rev10 — supersedes the HGR20 ceiling-rail slide. The pivot is the film
    # far-left upright at the FAR (Yd) edge; the old left-edge barrel hinges +
    # ceiling-rail carriage are retired (see Sheet 4 for the plan).
    PIVOT_PX = PW + 35    # far-edge pivot post (just past the panel right edge)
    ax.add_patch(Rectangle((PIVOT_PX - 20, 0), 40, PH,
                            fc="#5A5AA0", ec=C_OUT, lw=1.2, zorder=3, alpha=0.85))
    ax.text(PIVOT_PX + 55, PH / 2, "PIVOT POST\nØ89 CHS\n(vertical swing axis)",
            color="#5A5AA0", fontsize=6, ha="left", va="center",
            fontweight="bold", **FONT, zorder=15)
    # swing direction arc on the near (left) side
    arr_y = -80
    ax.annotate("", xy=(-HINGE_W - 40, arr_y + 80), xytext=(-HINGE_W - 40, arr_y),
                arrowprops=dict(arrowstyle="-|>", color="#1763C8", lw=1.6,
                                connectionstyle="arc3,rad=0.4", mutation_scale=11), zorder=15)
    ax.text(-HINGE_W - 70, PH / 2,
            "Panel + drum SWING 56°\nabout the far-edge pivot for\ntransport (no rails / no slide)\n— see Sheet 4",
            color=C_DIM, fontsize=6, ha="right", va="center", **FONT, zorder=15)

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

    # ── Emergency egress safety note ──────────────────────────────────────────
    ax.text(PW / 2, -280,
            "SAFETY: Interior-mounted cam latches (×4) allow emergency panel release from inside — "
            "operate if revolving drum jams. Panel opens outward, clear of all equipment.",
            color="#C04010", fontsize=6.5, ha="center", va="center",
            fontweight="bold", **FONT, zorder=15)

    # ── EPDM seal leader ─────────────────────────────────────────────────────
    leader(ax, (PW - S, PH / 2),
           (PW + 320, PH / 2 + 300),
           "20mm EPDM GASKET\nIN ALUMINUM CHANNEL\n(PERIMETER, ALL SIDES)")

    # ── Dimension lines ───────────────────────────────────────────────────────
    # Panel width
    draw_dim_h(ax, 0, PW, PH + 200, f"{PW}mm  (CONTAINER INTERIOR WIDTH)", offset=20, fs=7, font=FONT)
    # Panel height
    draw_dim_v(ax, PW + 75, 0, PH, f"{PH}mm", offset=-25, fs=7, right=True, font=FONT)
    # Drum diameter
    draw_dim_h(ax, DX, DX + DRUM_D, DY_TOP + 170, f"Ø{DRUM_D}mm DRUM", offset=20, fs=7, font=FONT)    # Drum clear height
    draw_dim_v(ax, DX - 200, DY_BOT, DY_TOP, f"{DRUM_H}mm\nCLEAR HEIGHT", offset=25, fs=7, right=True, font=FONT)
    # Drum center from left
    draw_dim_h(ax, 0, DRUM_CX, DY_BOT - 180, f"{int(DRUM_CX)}mm  (PANEL CL — CENTERED)", offset=-50, fs=7, font=FONT)   # (hinge-position dims retired with the barrel hinges — the panel pivots on the post.)

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
    title_block(ax, "SHEET 1 OF 5",
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
# stepped panel.  Corner zones (Yd=0-653 and Yd=1709-2362) are only 40mm
# thick — see Sheet 1 for the step transition locations.
#
# The drum (Ø900mm) is much larger than the panel depth (120mm + 40mm wall).
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
    D_CX = PW / 2        # drum center X: centerd in panel width = 1181mm
    # B2: housing center offset out in DEPTH to the container DRUM_CX (= BAY_FRONT_X
    # + DRUM_R + 40 = -400mm), carried past the door plane by the punch-out bay.
    D_CY = BAY_FRONT_X + DRUM_R + 40   # = -400mm (container DRUM_CX)
    DR   = DRUM_R        # = 450mm

    # Drum Y (depth) extents
    D_YB = D_CY - DR     # exterior overhang = -400 - 450 = -850mm
    D_YT = D_CY + DR     # interior overhang = -400 + 450 = +50mm

    # Drum X extents
    D_XL = D_CX - DR    # = 731mm
    D_XR = D_CX + DR    # = 1631mm

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

    # ── CENTER ZONE = B2 PUNCH-OUT BAY ───────────────────────────────────────
    # The center zone is a rigid box protruding forward (depth from the panel
    # interior face Y_INT out to BAY_FRONT_X) that encloses the offset Ø900
    # housing. Side walls run the bay depth; a front face closes the exterior end.
    for x, w in [(STEP_YD_L, D_XL - STEP_YD_L), (D_XR, STEP_YD_R - D_XR)]:
        ax.add_patch(Rectangle((x, BAY_FRONT_X), w, Y_INT - BAY_FRONT_X,
                                fc=C_PLASTIC, ec=C_OUT, lw=1.0, hatch="\\\\",
                                zorder=3, alpha=0.85))  # rev11: 4mm PP bay walls
    ax.add_patch(Rectangle((STEP_YD_L, BAY_FRONT_X), STEP_YD_R - STEP_YD_L, BAY_WALL_T,
                            fc=C_STEEL, ec=C_OUT, lw=1.0, hatch="///", zorder=4))
    ax.text((STEP_YD_L + STEP_YD_R) / 2, BAY_FRONT_X - 110, "PUNCH-OUT BAY (rev9)",
            color=C_OUT, fontsize=8.5, ha="center", va="top", **FONT,
            fontweight="bold", zorder=15)

    # ── CORNER ZONES (40mm envelope, Yd=0→653 and Yd=1709→2362) ──────────────
    # rev11: 4mm PP skin + framed HOLLOW core (3mm Al stiffener mid) + 4mm PP skin.
    # The 40mm envelope is unchanged (frame depth); only the skins changed material.
    CORN_SKIN  = PANEL_SKIN_T                     # 4mm PP skin each face
    CORN_PLATE = 3                               # 3mm Al core stiffener
    CORN_Y_OUT = Y1_W                            # 40 — outer face (= wall inner face)
    CORN_Y_IN  = Y1_W + CORNER_T                  # 80 — inner face (40mm envelope)
    al_mid = CORN_Y_OUT + CORNER_T / 2 - CORN_PLATE / 2

    # This section is cut at H=1000mm — BELOW the Fan B ply-band top (1125mm), so the
    # NEAR corner (Yd 0→653, the fan side) is cut through the 18mm PLYWOOD band, while
    # the FAR corner is the 4mm PP skin. Both keep the 40mm envelope + 3mm Al core.
    for x0, x1, skin_c, skin_t in [(0, STEP_YD_L, C_WOOD, 18),
                                    (STEP_YD_R, PW, C_PLASTIC, CORN_SKIN)]:
        w = x1 - x0
        # framed hollow core between the skins
        ax.add_patch(Rectangle((x0, CORN_Y_OUT), w, CORNER_T,
                                fc=C_HOLLOW, ec=C_OUT, lw=0.6, zorder=3))
        # outer + inner skins (wood at the fan corner, PP at the far corner)
        ax.add_patch(Rectangle((x0, CORN_Y_OUT), w, skin_t,
                                fc=skin_c, ec=C_OUT, lw=0.8, zorder=3.1))
        ax.add_patch(Rectangle((x0, CORN_Y_IN - skin_t), w, skin_t,
                                fc=skin_c, ec=C_OUT, lw=0.8, zorder=3.1))
        # 3mm Al core stiffener (mid)
        ax.add_patch(Rectangle((x0, al_mid), w, CORN_PLATE,
                                fc=C_ALUM, ec=C_OUT, lw=0.6, hatch="xx", zorder=3.2))

    # ── Step transition lines ─────────────────────────────────────────────────
    for sx in [STEP_YD_L, STEP_YD_R]:
        # Vertical step face at transition
        ax.plot([sx, sx], [Y0_PL, Y1_PL2], color=C_OUT, lw=1.5, zorder=5)
        # Horizontal shelf connecting 40mm→120mm
        ax.plot([sx, sx], [CORN_Y_IN, Y1_PL2], color=C_OUT, lw=1.0,
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
           (rail_left_x - 200, Y_HI - 460),
           "NEAR EDGE — swings free\n(rev10: no slide rail;\npanel pivots at the far edge)", col=C_DIM, fs=6)
    leader(ax, (rail_left_x + CBEAM / 2, Y0_PL + CORNER_T / 2),
           (rail_left_x - 200, Y_HI - 180),
           "CARRIAGE BEAM\n60×60mm SHS\n+ BRUSH SEAL", col=C_CARR, fs=6)

    # RIGHT (far) edge — the vertical PIVOT POST (rev10: replaces the slide guide rail)
    rail_right_x = PW + 60
    ax.add_patch(Rectangle((rail_right_x, -20), RAIL_W, WALL_T + PT + 40,
                            fc="#5A5AA0", ec=C_OUT, lw=0.8, alpha=0.85, zorder=5))
    # Brush seal strip (right slot)
    ax.add_patch(Rectangle((PW - brush_w, Y0_W), brush_w, Y1_PL2 - Y0_W,
                            fc="#806040", ec=C_OUT, lw=0.5, zorder=6, alpha=0.8))
    ax.add_patch(Rectangle((PW, Y0_W), brush_w, Y1_PL2 - Y0_W,
                            fc="#806040", ec=C_OUT, lw=0.5, zorder=6, alpha=0.8))

    leader(ax, (rail_right_x + RAIL_W / 2, Y0_W + WALL_T / 2),
           (rail_right_x + 200, Y_LO + 160),
           "PIVOT POST Ø89 CHS\n(vertical swing axis —\nno slide rail)", col="#5A5AA0", fs=6)
    leader(ax, (PW + brush_w / 2, Y0_PL + PT / 2),
           (rail_right_x + 200, Y_HI - 80),
           "GUIDE SLOT\n+ BRUSH SEAL\n(DOUBLED NYLON)", col=C_CARR, fs=6)

    # ── Drum: draw filled circle on top to cut out the drum hole ─────────────
    # First stamp BG color over wall/panel where drum sits, then draw drum ring
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
    _arc(D_CX, D_CY, DR, [(90, OD), (270, OD)], 4.0, C_ALUM, z=9)      # fixed Al housing
    _arc(D_CX, D_CY, LT_DRUM_OR, [(270, OD)], 3.0, "#9C7B4D", z=10)      # C-shell drum (ENTER)

    # ── Drum support CAGE cross-beam (across the drum) carrying the central revolve
    #    bearing — top + bottom (rev10). Shown as a bar spanning the cage width. ──
    from tbs_constants import DRUM_CAGE_YD_L as _CGL, DRUM_CAGE_YD_R as _CGR
    cb_t = 50
    ax.add_patch(Rectangle((_CGL, D_CY - cb_t / 2), _CGR - _CGL, cb_t,
                           fc=C_STEEL, ec=C_OUT, lw=1.1, alpha=0.45, zorder=11))
    # revolve bearing — CENTERED on the drum axis (the bore label is offset below it instead)
    ax.add_patch(Circle((D_CX, D_CY), 60, fc="#5A5AA0", ec=C_OUT, lw=1.3, zorder=12))
    leader(ax, (_CGL + 40, D_CY - cb_t / 2), (D_XL - 120, D_CY - DR * 0.4),
           "DRUM CAGE CROSS-BEAM (top +\nbottom) carrying the central\nØ220/Ø120 revolve bearing", col=C_STEEL, fs=6)
    # daylight ray at ENTER: enters bore from exterior, blocked at interior by drum
    ax.annotate("", xy=(D_CX, D_CY + LT_DRUM_OR * 0.9), xytext=(D_CX, D_YB - 70),
                arrowprops=dict(arrowstyle="-|>", color="#D08000", lw=1.8), zorder=12)
    ax.plot([D_CX], [D_CY + LT_DRUM_OR], marker="x", ms=10, mew=2.4,
            color="#2E8B57", zorder=13)
    ax.text(D_CX, D_CY - DR * 0.45, f"Ø{int(2 * BORE_R)} bore\n~555mm passage", color=C_DIM,
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

    # ── Center lines ──────────────────────────────────────────────────────────
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
    draw_dim_h(ax, D_XL, D_XR, D_YT + PAD_YT * 0.55,
          f"Ø{DRUM_D}mm  DRUM DIAMETER", fs=7, offset=-25, font=FONT)
    # Container wall thickness — arrow + inline label (no leader, avoids crossing
    # the nearby CONTAINER END WALL and OUTER PLY leader lines)
    draw_dim_v(ax, DIM_X_R, Y0_W, Y1_W,
          f"  {WALL_T}mm", offset=15, fs=6.5, right=True, font=FONT)

    # Panel overall thickness — arrow + inline label
    draw_dim_v(ax, DIM_X_R, Y1_W, Y1_PL2,
          f"  {PT}mm", offset=15, fs=6.5, right=True, font=FONT)

    # Exterior drum overhang — 45° leader going south-left
    ext_oh_mid = (D_YB + Y0_W) / 2
    draw_dim_v(ax, D_XL - 150, D_YB, Y0_W, f"{int(Y0_W - D_YB)}mm EXT. OVERHANG", offset=15, fs=6, right=True, font=FONT)

    # Interior drum overhang dimension
    draw_dim_v(ax, D_XL - 150, Y1_PL2, D_YT, f"{int(D_YT - Y1_PL2)}mm INT. OVERHANG", offset=15, fs=6, right=True, font=FONT)

    # Full panel width dimension
    draw_dim_h(ax, 0, PW, Y_LO + 230, f"{PW}mm  (FULL PANEL WIDTH)", fs=7, offset=-25, font=FONT)

    # Zone width dimensions (above panel)
    zone_dim_y = D_YT + PAD_YT * 0.85
    draw_dim_h(ax, 0, STEP_YD_L, zone_dim_y-30,
          f"{STEP_YD_L}mm", fs=6, offset=-20, font=FONT)
    draw_dim_h(ax, STEP_YD_L, STEP_YD_R, zone_dim_y-30,
          f"{STEP_YD_R - STEP_YD_L}mm CENTER", fs=6, offset=-20, font=FONT)
    draw_dim_h(ax, STEP_YD_R, PW, zone_dim_y-30,
          f"{PW - STEP_YD_R}mm", fs=6, offset=-20, font=FONT)

    # Corner zone thickness dimension
    draw_dim_v(ax, STEP_YD_L / 2 - 100, Y1_W, CORN_Y_IN,
          f"{CORNER_T}mm", offset=15, fs=6, right=True, font=FONT)

    # ── Zone labels ─────────────────────────────────────────────────────────────
    ax.text(STEP_YD_L / 2, CORN_Y_IN + 25,
            f"40mm\nCORNER", color="#C04010", fontsize=6, ha="center", va="bottom",
            fontweight="bold", **FONT, zorder=15, alpha=0.7)
    ax.text((STEP_YD_L + STEP_YD_R) / 2, Y1_PL2 + 25,
            f"120mm CENTER", color="#C04010", fontsize=6, ha="center", va="bottom",
            fontweight="bold", **FONT, zorder=15, alpha=0.7)
    ax.text((STEP_YD_R + PW) / 2, CORN_Y_IN + 25,
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

    # ── Material legend (rev11 wood/plastic differentiation) ──────────────────
    draw_legend(ax, [
        (C_PLASTIC, "4mm PP skin + B2 bay"),
        (C_WOOD, "18mm ply — Fan B mount band"),
        (C_ALUM, "3mm Al corner core"),
        (C_STEEL, "steel RHS frame / wall"),
        (C_GASKT, "20mm EPDM seal"),
    ], X_LO + 20, (Y_LO + Y_HI) / 2 + 160, title="MATERIALS", fs=6, col_w=420)

    # ── Title block ────────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 5",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="PLAN CROSS-SECTION (SECTION A-A AT H=1000mm) — HOUSED REVOLVING DOOR (HOUSING + C-SHELL DRUM, NO FINS)",
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
    PLY_T   = PANEL_SKIN_T   # rev11: 4mm PP skin each face (was 18mm ply); envelope kept via FRAME_T
    PT      = 120   # panel overall thickness (envelope unchanged)
    FRAME_T = PT - 2 * PLY_T   # = 112mm framed core

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
    D_CX_DEPTH = BAY_FRONT_X + DRUM_R + 40   # B2: housing depth center = -400mm (DRUM_CX)
    D_HALF_W   = DRUM_R                 # drum/housing radius = 450mm (in depth axis)

    D_DEPTH_L  = D_CX_DEPTH - D_HALF_W   # = -400 - 450 = -850mm (exterior overhang)
    D_DEPTH_R  = D_CX_DEPTH + D_HALF_W   # = -400 + 450 = +50mm  (interior overhang)

    # Height positions (vertical axis in this view)
    H_FLOOR    = 0
    H_BRG_BOT  = 100          # lower bearing base
    H_BRG_HT   = 45           # bearing housing height
    H_DRUM_BOT = H_BRG_BOT + H_BRG_HT   # = 145mm (drum body starts)
    H_DRUM_TOP = H_DRUM_BOT + (DRUM_H - 2 * H_BRG_HT)  # = 145 + 1910 = 2055mm
    H_BRG_TOP  = H_DRUM_TOP + H_BRG_HT  # = 2100mm
    H_HANDLE   = H_BRG_BOT + DRUM_H * 0.45  # handle height = ~1000mm

    # ── Data range → figure size ──────────────────────────────────────────────
    PAD_L, PAD_R = 300, 2100  # depth-axis margins (right margin holds Details B/C + their
                              # annotations, which run out to ~1935mm — widened so they fit)
    PAD_B, PAD_T = 500, 350   # height-axis margins (bottom includes title block + rail annotations)

    X_LO = D_DEPTH_L - PAD_L   # = -1150mm
    X_HI = D_DEPTH_R + PAD_R   # = 2150mm
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
                                fc=C_PLASTIC, ec=C_OUT, lw=0.6, zorder=3))

    # ── Panel RHS frame (depth 58→142) ────────────────────────────────────────
    ax.add_patch(plt.Rectangle((Y0_FR, H_FLOOR), FRAME_T, H_BRG_TOP + 80,
                                fc=C_STEEL, ec=C_OUT, lw=0.6, hatch="\\\\", zorder=3))

    # ── Panel inner ply (depth 142→160) ───────────────────────────────────────
    ax.add_patch(plt.Rectangle((Y0_PL2, H_FLOOR), PLY_T, H_BRG_TOP + 80,
                                fc=C_PLASTIC, ec=C_OUT, lw=0.6, zorder=3))

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
           f"{PLY_T}mm\nPP", col=C_DIM, fs=5.5)
    # RHS frame
    leader(ax, ((Y0_FR + Y1_FR) / 2, LDR_TOP - 50),
           ((Y0_FR + Y1_FR) / 2 + 120, LDR_TOP_TGT + 50),
           f"{FRAME_T}mm RHS FRAME", col=C_DIM, fs=5.5)
    # Inner ply
    leader(ax, ((Y0_PL2 + Y1_PL2) / 2 - 5, LDR_TOP - 60),
           ((Y0_PL2 + Y1_PL2) / 2 + 120, LDR_TOP_TGT + 10),
           f"{PLY_T}mm\nPP", col=C_DIM, fs=5.5)

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
           f"{PLY_T}mm\nPP", col=C_DIM, fs=5.5)
    # RHS frame
    leader(ax, ((Y0_FR + Y1_FR) / 2, LDR_BOT),
           ((Y0_FR + Y1_FR) / 2 + 120, LDR_BOT_TGT - 100),
           f"{FRAME_T}mm RHS FRAME", col=C_DIM, fs=5.5)
    # Inner ply
    leader(ax, ((Y0_PL2 + Y1_PL2) / 2 - 5, LDR_BOT + 20),
           ((Y0_PL2 + Y1_PL2) / 2 + 120, LDR_BOT_TGT - 50),
           f"{PLY_T}mm\nPP", col=C_DIM, fs=5.5)

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
    # rev10: at the door end the walkway is REMOVABLE (left walkway + door-end near-deck
    # section lift out for the swing) — shown in AMBER to flag it carries no swing interference.
    C_WALKWAY = "#C8902A"          # amber — removable
    BRKT_ARM_Z = WALKWAY_H - WALKWAY_GRATE_T  # = 75mm (top of bracket arm)
    WK_START = Y1_PL2 + 80   # start showing walkway past drum overhang
    WK_END   = D_DEPTH_R + 120  # extend into interior

    # Bracket arm (8mm thick at Z=67-75mm)
    ax.add_patch(plt.Rectangle((WK_START, BRKT_ARM_Z - WALKWAY_BRACKET_T),
                                WK_END - WK_START, WALKWAY_BRACKET_T,
                                fc=C_WALKWAY, ec=C_OUT, lw=0.6, zorder=4))
    # Grate (amber, removable)
    ax.add_patch(plt.Rectangle((WK_START, BRKT_ARM_Z),
                                WK_END - WK_START, WALKWAY_GRATE_T,
                                fc="#E8B860", ec=C_OUT, lw=0.6, hatch="xx", zorder=4))

    # Break lines at right end (walkway continues)
    for z_off in [-5, 5, 15]:
        ax.plot([WK_END - 3, WK_END + 3],
                [BRKT_ARM_Z + z_off - 3, BRKT_ARM_Z + z_off + 3],
                color=C_OUT, lw=0.6, zorder=5)

    leader(ax, (WK_START + (WK_END - WK_START) / 2, WALKWAY_H + 5),
           (WK_START + (WK_END - WK_START) / 2 + 300, WALKWAY_H + 200),
           f"WALKWAY DECK — REMOVABLE\n(lifts out for transport;\nno swing interference)\n{WALKWAY_GRATE_T}mm grate at Z={WALKWAY_H}mm",
           col=C_WALKWAY, fs=5.5)

    # Walkway deck height dimension
    draw_dim_v(ax, WK_END + 30, H_FLOOR, WALKWAY_H,
          f"{WALKWAY_H}mm\nDECK", offset=30, fs=6, right=True, font=FONT)

    # ── Former HGR20 rails (rev10 RETIRED — drawn faint for reference) ───────
    # The old slide rails ran in the X (depth) direction on both side walls.
    # In this Section A-A view (looking along Yd), the rails on both walls
    # project to the same position. Shown faint as side-profile rectangles,
    # labeled retired below (the panel now SWINGS about the Ø89 pivot).
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

    # Rail labels (rev10: the floor/ceiling HGR20 slide rails are RETIRED — the panel
    # pivots on the Ø89 post; the rail profiles above are shown faint as the old route).
    leader(ax, (RAIL_FLOOR_X + RAIL_PROF_L, RAIL_FLOOR_Y + RAIL_PROF_H / 2),
           (RAIL_FLOOR_X + RAIL_PROF_L + 200, RAIL_FLOOR_Y - 130),
           "(former HGR20 slide rails —\nRETIRED; panel now SWINGS\nabout the Ø89 pivot post)",
           col=C_DIM, fs=5.5)

    # Swing note (replaces the old slide-travel arrow)
    ARROW_Y = RAIL_FLOOR_Y - 160
    ax.text(Y0_W + 300, ARROW_Y - 15, "PANEL SWINGS 56° ABOUT THE PIVOT (no slide) — see Sheet 4",
            ha="center", va="top", fontsize=5.5, color="#1763C8",
            fontweight="bold", **FONT, zorder=15)

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

    # ── rev8: NO internal fins — single-opening C-shell + fixed housing ──────
    # The Ø750 / 4-baffle drum was replaced (rev8) by a fixed Ø900 housing with a
    # single-opening C-shell drum (no fins); the whole ~Ø850 bore is clear. In
    # this elevation the bore reads as open space (light-tightness is by the
    # housing geometry — see Sheet 2 plan and Sheet 5).
    ax.text(D_CX_DEPTH / 2 - 150, H_DRUM_BOT + (H_DRUM_TOP - H_DRUM_BOT) * 0.5,
            "Single-opening C-shell\n~Ø850 clear bore\nFlat black interior",
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
    # Place person inside drum toward the interior wall, clear of centerline text
    PERSON_X = D_DEPTH_R - 130
    P_FOOT   = H_DRUM_BOT          # feet on drum floor (145mm above container floor)
    P_HEAD   = P_FOOT + PERSON_H   # head top = 145 + 1780 = 1925mm

    # Drum floor level indicator (thin horizontal line across drum base)
    ax.plot([D_DEPTH_L, D_DEPTH_R], [H_DRUM_BOT, H_DRUM_BOT],
            color="#A06020", lw=0.8, ls="--", zorder=6, alpha=0.7)
    # Vertical dimension arrow: container floor → drum floor
    DRUM_FL_DIM_X = D_DEPTH_L - 180
    draw_dim_v(ax, DRUM_FL_DIM_X, H_FLOOR, H_DRUM_BOT,
          f"{H_DRUM_BOT}mm\nDRUM\nFLOOR", offset=-100, fs=6, right=True, font=FONT)

    # Person body (line) and head (circle) — blue tones
    ax.plot([PERSON_X, PERSON_X], [P_FOOT, P_HEAD],
            color="#2060A0", lw=3.0, zorder=8, solid_capstyle="round")
    ax.add_patch(plt.Circle((PERSON_X, P_HEAD + HEAD_R), HEAD_R,
                             fc="#70A8D8", ec="#1A4D80", lw=1.0, zorder=8))

    # Headroom gap: person head top → drum body ceiling
    drum_body_h    = H_DRUM_TOP - H_DRUM_BOT
    headroom_1780  = drum_body_h - PERSON_H
    GAP_X = PERSON_X
    draw_dim_v(ax, GAP_X, P_HEAD + 2 * HEAD_R, H_DRUM_TOP, f"{headroom_1780}mm\nHEADROOM",
               offset=90, fs=6, right=False, perpendicular=True, color="#20A020", font=FONT)

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

    # ── Center line (vertical drum axis) ──────────────────────────────────────
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

    ax.annotate("", xy=(D_DEPTH_R + 420, EAR_Y + 450),
                xytext=(D_DEPTH_R + 150, EAR_Y + 450),
                arrowprops=dict(arrowstyle="->", color="#20A060", lw=1.5,
                                mutation_scale=10))
    ax.text(D_DEPTH_R + 150, EAR_Y + 500, "EXIT\n(to interior /\ndarkroom)",
            ha="left", va="bottom", fontsize=7, color="#20A060", **FONT, zorder=15)

    ax.text(D_CX_DEPTH /2 - 150, H_FLOOR + DRUM_H * 0.2,
            "DRUM REVOLVES ABOUT\nTHE VERTICAL AXIS —\nPUSH WALL TO ENTER/EXIT",
            ha="center", va="center", fontsize=6.5, color=C_DIM,
            **FONT, alpha=0.75, zorder=15)

    # ── Dimension callouts ────────────────────────────────────────────────────
    DIM_R = D_DEPTH_R + PAD_R * 0.25

    # Drum height
    draw_dim_v(ax, DIM_R, H_DRUM_BOT, H_DRUM_TOP,
          f"{DRUM_H}mm DRUM HEIGHT\n(CLEAR WALKING HEIGHT)", offset=30, fs=7, right=True, font=FONT)

    # Drum diameter (horizontal) — placed below top bearing to avoid CL label clash
    draw_dim_h(ax, D_DEPTH_L, D_DEPTH_R, H_DRUM_TOP + 180,
          f"Ø{DRUM_D}mm DRUM DIAMETER", offset=15, fs=7, font=FONT)
    # Panel thickness (horizontal) — offset above bearing top
    draw_dim_h(ax, Y0_W, Y1_PL2, H_BRG_TOP + 295,
          f"{PT}mm PANEL", offset=15, fs=6.5, font=FONT)

    # (Wall thickness leaders are drawn above with the other layer leaders)

    # Exterior overhang (horizontal) — below floor rail
    draw_dim_h(ax, D_DEPTH_L, Y0_W, H_FLOOR + 40,
          f"{abs(int(D_DEPTH_L))}mm EXT. OVERHANG", offset=15, fs=6, font=FONT)

    # Interior overhang (horizontal) — below floor rail
    draw_dim_h(ax, Y1_PL2, D_DEPTH_R, H_FLOOR + 40,
          f"{int(D_DEPTH_R - Y1_PL2)}mm INT. OVERHANG", offset=15, fs=6, font=FONT)

    # Vertical dimension arrow: container floor → handle bottom
    HANDLE_DIM_X = D_DEPTH_L - 100
    HANDLE_BOT = H_HANDLE - HH / 2   # bottom of handle bar
    draw_dim_v(ax, HANDLE_DIM_X / 2 + DRUM_D, H_FLOOR, HANDLE_BOT,
          f"{int(HANDLE_BOT)}mm\nHANDLE HT", offset=-60, fs=6, right=True, font=FONT)

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL B — Panel bottom light seal (enlarged), section at a corner zone
    # (away from the drum). The 130mm floor gap (PANEL_FLOOR_GAP, +50 raise) is closed in operational
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
    ax.annotate("", xy=(DX(-33), DY(78)), xytext=(DX(-92), DY(78)),
                arrowprops=dict(arrowstyle="-|>", color="#D08000", lw=1.6), zorder=25)
    ax.plot([DX(-30)], [DY(78)], marker="x", ms=7, mew=2.2, color="#C02020", zorder=26)
    ax.text(DX(-92), DY(62), "ext. light\nblocked by\nlip", fontsize=5.8,
            color="#A05000", ha="left", va="center", **FONT)

    # cam-latch compression (panel pulled onto the seal)
    ax.annotate("", xy=(DX(2), DY(158)), xytext=(DX(34), DY(158)),
                arrowprops=dict(arrowstyle="-|>", color=C_CL, lw=1.8), zorder=25)

    # floor-gap dimension (interior side, clear lane)
    from tbs_constants import PANEL_FLOOR_GAP as _PFG, PROC_TRAY_RIM as _TRIM
    draw_dim_v(ax, DX(52), DY(0), DY(80), f"{_PFG} mm\nfloor gap",
               offset=22, fs=5.8, right=False, perpendicular=True, color=C_DIM, font=FONT)

    # callout labels (right side, leaders pointing into the detail)
    def dlbl(target, ty, text):
        tx = DX(92)
        ax.annotate("", xy=target, xytext=(tx - 6, ty),
                    arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.8,
                                    shrinkA=1, shrinkB=1), zorder=24)
        ax.text(tx, ty, text, fontsize=6.0, color=C_DIM, ha="left", va="center", **FONT)
    dlbl((DX(20), DY(165)), DY(172), "Cam latch compresses panel\nonto seal (release to swing)")
    dlbl((DX(20), DY(120)), DY(138), "Panel bottom edge\n(40 mm corner zone)")
    dlbl((DX(-10), DY(100)), DY(108), "20 mm EPDM — panel\nrecedes into / seals on lip")
    dlbl((DX(-26), DY(64)), DY(74), "Frame seal lip — steel upstand\nfrom threshold (notched at drum)")
    dlbl((DX(-40), DY(22)), DY(45), "Fixed door-frame\nthreshold (50×50 RHS)")
    dlbl((DX(74), DY(28)), DY(12), f"{_TRIM} mm tray rim —\n{_PFG - _TRIM} mm clearance")

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL C — Panel top light seal (enlarged), the mirror of Detail B.
    # The panel hangs below the ceiling rails, leaving a gap between the panel
    # top and the frame top rail. A frame top seal lip (downstand) closes it; a
    # 20mm EPDM strip on the panel top edge compresses against it under the upper
    # cam latches. The drum does not reach the top, so the lip runs the full
    # width as one continuous member (meets across the center).
    # ══════════════════════════════════════════════════════════════════════════
    ox2, oy2 = 980, 1935   # raised so Details C / D / B clear each other vertically
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
    ax.text(CX(-92), CY(-6), "ext. light\nblocked by\nlip", fontsize=5.8,
            color="#A05000", ha="left", va="center", **FONT)

    # upper cam-latch compression (panel pulled onto the seal)
    ax.annotate("", xy=(CX(2), CY(-58)), xytext=(CX(34), CY(-58)),
                arrowprops=dict(arrowstyle="-|>", color=C_CL, lw=1.8), zorder=25)

    def clbl(target, ty, text):
        tx = CX(92)
        ax.annotate("", xy=target, xytext=(tx - 6, ty),
                    arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.8,
                                    shrinkA=1, shrinkB=1), zorder=24)
        ax.text(tx, ty, text, fontsize=6.0, color=C_DIM, ha="left", va="center", zorder=24, **FONT)
    clbl((CX(-40), CY(64)), CY(82), "Frame top rail (50×50 RHS)")
    clbl((CX(30), CY(55)), CY(68), "Panel top gap is the light path\n(carried by the pivot post — not ceiling-hung)")
    clbl((CX(-26), CY(30)), CY(28), "Top seal lip — steel downstand,\nfull width (continuous, meets at center)")
    clbl((CX(-10), CY(-20)), CY(-10), "20 mm EPDM — panel top\nedge seals on lip")
    clbl((CX(20), CY(-70)), CY(-58), "Upper cam latch compresses\npanel onto seal")
    clbl((CX(20), CY(-95)), CY(-85), "Panel top edge")

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL D — Vertical CUT seal (plan section at the fixed↔swinging joint, Yd180
    # & Yd2287). The swinging panel's vertical edge butts an EPDM bulb bonded to the
    # fixed strip's edge: the joint seals when shut (camera mode) and opens as the
    # panel swings. Plan section: depth X horizontal, Yd vertical (cut at yr=0).
    # ══════════════════════════════════════════════════════════════════════════
    odx, ody = 1369, 1240   # right border aligned with Details C/B (DDX(60)=1567≈bx1/cbx1);
                            # ody keeps it vertically between Details C (above) and B (below)
    def DDX(x): return odx + k * x          # panel depth (mm) → sheet x (exterior negative)
    def DDY(yr): return ody + k * yr        # Yd about the cut (yr=0) → sheet y
    dbx0, dbx1 = DDX(-26), DDX(60)
    dby0, dby1 = DDY(-54), DDY(54)
    ax.add_patch(Rectangle((dbx0, dby0), dbx1 - dbx0, dby1 - dby0,
                           fc="#FBFBFD", ec=C_DIM, lw=1.0, ls=(0, (5, 3)), zorder=2))
    ax.text((dbx0 + dbx1) / 2, dby1 + 30, "DETAIL D — VERTICAL CUT SEAL",
            ha="center", va="bottom", fontsize=9, fontweight="bold", color=C_OUT, **FONT)
    ax.text((dbx0 + dbx1) / 2, dby1 + 8,
            "plan section at the fixed↔swing joint (Yd180 / Yd2287)  ·  enlarged ~3.3:1",
            ha="center", va="bottom", fontsize=6.4, color=C_DIM, **FONT)
    ax.text(DDX(-20), DDY(48), "EXTERIOR", fontsize=6, color="#5060A0",
            ha="left", va="center", fontweight="bold", **FONT)
    ax.text(DDX(52), DDY(48), "INTERIOR", fontsize=6, color="#407040",
            ha="right", va="center", fontweight="bold", **FONT)
    # fixed strip edge (lower) + EPDM cut bulb (centre) + swinging panel edge (upper)
    ax.add_patch(Rectangle((DDX(0), DDY(-50)), k * 40, k * 43, fc="#C8A060", ec=C_OUT,
                           lw=1.3, hatch="\\\\\\", zorder=22))                 # fixed strip
    ax.add_patch(Rectangle((DDX(0), DDY(7)), k * 40, k * 43, fc=C_ALUM, ec=C_OUT,
                           lw=1.3, zorder=22))                                  # swinging panel
    ax.add_patch(Rectangle((DDX(-3), DDY(-7)), k * 43, k * 14, fc=C_GASKT, ec=C_OUT,
                           lw=1.0, zorder=24))                                  # EPDM cut seal
    ax.plot([DDX(0), DDX(0)], [DDY(-52), DDY(52)], color=C_CL, lw=0.8, ls=(0, (6, 4)), zorder=20)
    def ddlbl(target, ty, text):
        tx = DDX(70)
        ax.annotate("", xy=target, xytext=(tx - 6, ty),
                    arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.8, shrinkA=1, shrinkB=1), zorder=24)
        ax.text(tx, ty, text, fontsize=6.0, color=C_DIM, ha="left", va="center", **FONT)
    ddlbl((DDX(20), DDY(-30)), DDY(-40), "FIXED strip edge\n(bolted to the door frame)")
    ddlbl((DDX(8), DDY(0)), DDY(2), "EPDM cut-seal bulb — bonded to\nthe fixed edge; the swinging panel\nbutts + compresses it when shut")
    ddlbl((DDX(20), DDY(30)), DDY(42), "SWINGING panel edge\n(joint opens as it swings)")

    # ── Title block (portrait sheet — taller box, smaller fonts, clipped) ──────
    title_block(ax, "SHEET 3 OF 5",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="DRUM ELEVATION — SECTION A-A: VERTICAL DRUM, WALKING HEIGHT",
                scale_note="EQUAL ASPECT  \u00b7  SCALE 1:20 (APPROX)  \u00b7  ALL DIMS IN mm",
                doc_id="TBS-001 \u00b7 Hinged Light-Trap Panel",
                height=0.05, portrait=True)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet3.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet3.png saved")




# ═════════════════════════════════════════════════════════════════════════════
# SHEET 5  —  Drum access & light-tightness analysis (design review)
# Shows why the rev8 housed door PASSES the two questions the old
# Ø750 / 4-fin drum failed:
#   A. Can a person fit through the opening?
#   B. As the drum rotates, can daylight enter the container?
# (The 4-fin drum failed both; the housed door passes both.)
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
    ax.set_xlim(-130, 2130); ax.set_ylim(-260, 1460)
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

    ax.text(1000, 1415, "REVOLVING-DOOR LIGHT LOCK (rev 8) — PASSES BOTH TESTS",
            ha="center", fontsize=15, fontweight="bold", color=C_OUT, **FONT)
    ax.text(1000, 1378, "Fixed Ø900 housing (two 80° openings, 180° apart) + single-opening C-shell drum, NO fins",
            ha="center", fontsize=9, color=GREEN, **FONT)
    ax.plot([-130, 2130], [660, 660], color=C_DIM, lw=1.0, ls=(0, (6, 4)), zorder=3)

    # ── PANEL A — person fit ──
    ax.text(-110, 1300, "A.  PERSON FIT  —  open Ø850 bore, no fins", ha="left",
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
    ax.text(Acx, Acy + Rd + 46, "INTERIOR / walkway (exit)", fontsize=7.5, color=GREEN,
            **FONT, fontweight="bold", ha="center")

    # ── PANEL B — light-tight at every rotation ──
    ax.text(-110, 588, "B.  LIGHT-TIGHT AT EVERY ROTATION", ha="left", fontsize=12,
            fontweight="bold", color=C_OUT, **FONT)
    Bcy, bs = 340, 0.52
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
    v_x, v_y, v_w, v_h = 920, 950, 1200, 250
    ax.add_patch(FancyBboxPatch((v_x, v_y), v_w, v_h,
                                boxstyle="round,pad=6,rounding_size=12",
                                fc="#EAF6EE", ec=GREEN, lw=1.6, zorder=2))
    ax.text(v_x + 5, v_y + v_h - 15, "VERDICT  ✓  PASS — no daylight path at any rotation", ha="left",
            va="center", fontsize=12.5, fontweight="bold", color=GREEN, **FONT)
    for i, line in enumerate([
        "The two housing openings are 80° wide and 180° apart, so the 80° drum opening can never reach both at once.",
        "The housing's solid wall always covers the opening the drum isn't aligned with — light enters the bore but",
        "never exits to the interior. A fixed housing (the panel aperture is no longer relied on as the seal)",
        "does the work.",
    ]):
        ax.text(v_x + 5, v_y + v_h - 55 - i * 42, line, ha="left", va="center", fontsize=8, color="#16361f", **FONT)

    title_block(ax, "SHEET 5 OF 5",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="REVOLVING-DOOR LIGHT LOCK (rev 8) — ACCESS & LIGHT-TIGHTNESS VERIFICATION (BOTH PASS)",
                scale_note="PLAN VIEWS · NOT TO SCALE · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.045)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet5.png"), dpi=130,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet5.png saved")




def sheet4():
    """COMBINED rotation transport + swing-clearance plan (X horizontal)."""
    import matplotlib.patches as mpatches
    from tbs_constants import (PIVOT_X, PIVOT_YD, SWING_LOCK_DEG, PANEL_CUT_YD,
                               FAR_STRIP_YD0, PIVOT_POST_OD)
    RED, GREEN, BLUE = "#C0202A", "#2E8B57", "#1763C8"
    RX, PT_ = RAIL_X_L, PANEL_CENTER_T                     # 150, 120
    HX, HY, LOCK = PIVOT_X, PIVOT_YD, SWING_LOCK_DEG
    CUT, FAR0 = PANEL_CUT_YD, FAR_STRIP_YD0
    cyd = PW / 2                                            # 1181 light-lock Yd center

    def rot(x, y, deg):
        t = np.radians(deg); c, s = np.cos(t), np.sin(t)
        return (HX + (x - HX) * c - (y - HY) * s, HY + (x - HX) * s + (y - HY) * c)

    fig, ax = plt.subplots(figsize=(17, 12))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(-980, 2360); ax.set_ylim(-360, 2700)
    ax.set_aspect("equal"); ax.axis("off")

    ax.add_patch(Rectangle((0, 0), 1340, PW, fc="#EEF6EE", ec="none", zorder=0))
    ax.plot([-280, 1340], [0, 0], color=C_OUT, lw=2, zorder=3)
    ax.plot([-280, 1340], [PW, PW], color=C_OUT, lw=2, zorder=3)
    ax.text(-270, -80, "near wall (Yd=0)", fontsize=7.5, color=C_DIM, **FONT)
    ax.text(-270, PW + 35, "far wall (Yd=2362)", fontsize=7.5, color=C_DIM, **FONT)
    ax.plot([0, 0], [0, PW], color=C_CL, lw=1.4, ls=(0, (6, 4)), zorder=3)
    ax.text(10, PW + 95, "door plane X=0", fontsize=8, color=C_CL, **FONT)

    # film-plane LEFT rails (X=150) — REMOVABLE: struck for transport so the swinging
    # cage can transition the X=150 rail plane, then re-seated to datum.
    ax.add_patch(Rectangle((RX - 13, FP_Y_MIN), 26, (FP_Y + 38) - FP_Y_MIN,
                           fc="#C06000", ec=C_OUT, lw=1, ls=(0, (4, 2)), alpha=0.55, zorder=6))
    ax.text(RX - 225, DRUM_CY, "left rails X=150\nREMOVABLE\n(struck for transport —\ndrop-in saddles)",
            fontsize=6, color="#8a5a10", **FONT, ha="right", va="center", zorder=12,
            bbox=dict(facecolor="white", edgecolor="none", boxstyle="round,pad=0.3", alpha=0.88))
    for yy in (FP_Y_MIN, FP_Y):                              # brace-cage beams (run X 150→far)
        ax.add_patch(Rectangle((RX, yy - 17), 1340 - RX, 34, fc=C_STEEL, ec=C_OUT,
                               lw=0.7, alpha=0.85, zorder=5))
    ax.text(1320, FP_Y_MIN - 60, "brace-cage beam →", fontsize=7, color=C_DIM, **FONT, ha="right")
    ax.add_patch(Rectangle((RX - 27, FP_Y_MIN - 27), 54, 54, fc="#5A5A62", ec=C_OUT, lw=1, zorder=7))  # near post
    # the FAR-left film post IS the Ø89 swing pivot
    ax.add_patch(Circle((HX, HY), PIVOT_POST_OD / 2 + 6, fc="#5A5AA0", ec=C_OUT, lw=1.2, zorder=9))
    ax.text(HX + 75, HY + 25, "PIVOT POST Ø89\n(= film far-left post)", fontsize=6.5,
            color="#5A5AA0", **FONT, va="center", zorder=12)

    # fixed left + far panel strips (do NOT swing)
    for (y0, y1) in [(0, CUT), (FAR0, PW)]:
        ax.add_patch(Rectangle((0, y0), 40, y1 - y0, fc="#C8A060", ec=C_OUT, lw=1.2, zorder=8))

    # swinging assembly (panel CUT..FAR0 + bay + drum): CAMERA (deployed) + SWUNG 56°
    def draw_moving(deg, ec, alpha, ls, hatch):
        pts = [rot(0, CUT, deg), rot(PT_, CUT, deg), rot(PT_, FAR0, deg), rot(0, FAR0, deg)]
        ax.add_patch(mpatches.Polygon(pts, closed=True, fc=C_ALUM, ec=ec, lw=1.4, ls=ls, alpha=alpha, zorder=9))
        bpts = [rot(BAY_FRONT_X, PANEL_CORNER_YD_L, deg), rot(0, PANEL_CORNER_YD_L, deg),
                rot(0, PANEL_CORNER_YD_R, deg), rot(BAY_FRONT_X, PANEL_CORNER_YD_R, deg)]
        ax.add_patch(mpatches.Polygon(bpts, closed=True, fc="#C8D8E8", ec=ec, lw=1.2, ls=ls,
                                       alpha=alpha * 0.9, zorder=9, hatch=hatch))
        dctr = rot(-400, cyd, deg)
        ax.add_patch(Circle(dctr, DRUM_R, fc=C_ALUM, ec=ec, lw=1.0, alpha=alpha * 0.5, ls=ls, zorder=9))
        return dctr
    draw_moving(0, "#7a5a20", 0.55, "-", "////")
    ax.text(BAY_FRONT_X / 2, -100, "CAMERA\n(deployed)", fontsize=7.5, color=C_DIM, **FONT, ha="center", va="top")
    d1 = draw_moving(LOCK, BLUE, 0.30, (0, (5, 3)), None)
    ax.text(d1[0], d1[1], f"SWUNG {int(LOCK)}°\n(door clears +59mm)", fontsize=7, color=BLUE, **FONT,
            ha="center", va="center", fontweight="bold", zorder=15)
    arc = [rot(0, CUT, dd) for dd in np.linspace(0, LOCK, 36)]
    ax.plot([p[0] for p in arc], [p[1] for p in arc], color=BLUE, lw=1.3, ls=(0, (4, 2)), zorder=11)

    # numbered markers
    def mark(x, y, n, col=BLUE):
        ax.add_patch(Circle((x, y), 58, fc="white", ec=col, lw=2.2, zorder=14))
        ax.text(x, y, str(n), fontsize=12, color=col, **FONT, fontweight="bold",
                ha="center", va="center", zorder=15)
    mark(RX, 430, 1); mark(RX, 1940, 1)       # left rails struck so the cage transitions
    mark(40, cyd, 2)                          # swing clears the door plane (+59mm)

    ax.text(-280, 2640, "SWING CLEARANCE vs FILM-PLANE LEFT MECHANISM  (plan, looking down)",
            fontsize=13, fontweight="bold", color=C_OUT, **FONT)
    notes = [
        "ROTATION TRANSPORT (rev10):",
        "The panel + drum SWING ~56° about the vertical",
        "pivot (the film far-left post), pulling the punch-",
        "out bay inboard of the door plane so the cargo",
        "doors close (true min X +59mm).",
        "",
        "1.  The swinging cage transitions the X=150 rail",
        "    plane, so the two LEFT film rails (TL+BL) are",
        "    REMOVABLE — lifted out (drop-in saddles) for",
        "    the swing, re-seated to datum after. The far-",
        "    left film post IS the Ø89 pivot.",
        "",
        "2.  The swing clears the door-end walkway brackets",
        "    at Z (panel/cage underside Z130 over the Z115",
        "    bracket tops); the left walkway + door-end",
        "    near-deck section lift out.",
        "",
        "OPERATING:  full symmetric film-plane travel is",
        "restored.",
        "",
        "TEARDOWN:  strike the left rails → lift the left",
        "walkway + near-deck section → unlatch → swing 56°",
        "→ engage top+bottom wall stays → close doors.",
    ]
    # Standard bordered notes block, raised into the upper-right so it clears the swung
    # panel's near-end (which sweeps to ~X1824/Yd964) — rule 35: never sit text on geometry.
    draw_notes(ax, notes, 1325, 2500, spacing=40, fs=7.0, width=985, font=FONT)

    title_block(ax, "SHEET 4 OF 5",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="ROTATING TRANSPORT + SWING CLEARANCE vs FILM-PLANE LEFT MECHANISM (PLAN)",
                scale_note="PLAN VIEW · NOT TO SCALE · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.045)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet4.png"), dpi=130,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet4.png saved")

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating hinged light-trap panel drawings...")
    sheet1()
    sheet2()
    sheet3()
    sheet4()
    sheet5()
    print("Done.")
