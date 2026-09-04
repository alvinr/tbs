#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_hingepanel_diagram.py  —  TBS-001 Hinged Light-Trap Panel

Sheet 1 — Front elevation (exterior view, 1:20):
  Panel dimensions, revolving drum position, hinges, latches, EPDM perimeter seal.
  Stepped profile: 40mm corner zones, 120mm center zone (drum housing).

Sheet 2 — Plan cross-section (1:20 equal aspect):
  Panel thickness (center zone), housed revolving door (fixed Ø800 housing +
  single-opening C-shell drum, no fins; light-tight by geometry), container
  wall interface, EPDM gasket engagement, latch detail.

Sheet 3 — Drum vertical section:
  Drum elevation showing walking height, bearings, person silhouette.

Sheet 4 — Rotating transport system (rev10, supersedes the slide):
  the split panel + drum swing 56° about the vertical pivot post (the film
  far-left upright); camera (shut) vs swung (transport) positions, removable
  left film rails, top+bottom wall stays.
"""

import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Arc, Ellipse, Polygon
import os
from tbs_constants import C_LT_DRUM, WALKWAY_H, WALKWAY_GRATE_T, WALKWAY_BRACKET_T, DIAGRAMS_DIR, DRUM_D as LT_HOUSING_D, DRUM_H_LT, LT_HOUSING_T, PANEL_CORNER_YD_L, PANEL_CORNER_YD_R, PANEL_CENTER_W, PANEL_CUT_YD, PIVOT_YD, DRUM_CAGE_YD_L, DRUM_CAGE_YD_R, BRACE_RHS, LT_CAGE_TOP, PIVOT_POST_OD, C_HGT, FAN_DIAM, LT_DRUM_OR, LT_OPENING_DEG, RAIL_X_L, FP_Y_MIN, FP_Y, PANEL_CENTER_T, DRUM_CY, BAY_FRONT_X, BAY_BACK_X, BAY_WALL_T, PANEL_SKIN_T, LT_RIVET_HOLE, LT_RIVET_PITCH, SWUNG_DOOR_CLEARANCE_MM, DRUM_CX as LT_DRUM_CX, DRUM_CAGE_X0, DRUM_CAGE_X1, DOOR_FRAME_DEPTH
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader as _leader_shared, draw_notes, draw_legend
from tbs_constants import DIAGRAM_DPI

# ── Palette (white engineering) ───────────────────────────────────────────────
BG      = "#FFFFFF"   # white background
C_OUT   = "#1A1A1A"   # outlines
C_CL    = "#2060A0"   # center lines (blue, dashed)
C_DIM   = "#404040"   # dimensions / annotation text
C_ALUM  = "#C8D8E8"   # aluminum (corner stiffener rib)
C_STEEL = "#B0B0B8"   # steel section fill
C_GASKT = "#5A3020"   # EPDM gasket fill
C_WOOD    = "#C9A36B"  # plywood — Fan B mount band (rev11 material legend)
C_PLASTIC = "#6E8CA0"  # 1/8″ HDPE plastic sheet — panel skins + B2 bay (rev11)
C_HOLLOW  = "#EEEEE8"  # framed hollow core between the HDPE skins (rev11)
C_LIGHT = "#FFE0A0"   # light-path indication (amber)
FONT    = {"fontfamily": "monospace"}

# ── Panel dimensions (mm) ─────────────────────────────────────────────────────
PW = 2362   # panel width  (= container interior short-axis width)
PH = 2388   # panel height (= container interior height)
PT = 120    # panel overall thickness (2×2×0.120in steel frame + 18mm ply each face)

# Light-trap housing (rev8: housed revolving door — see tbs_constants)
DRUM_D  = LT_HOUSING_D  # = 800mm fixed housing outer diameter (Ø900→Ø800 resize)
DRUM_R  = DRUM_D / 2   # = 400mm housing radius
DRUM_H  = DRUM_H_LT     # housing/drum height (floor → top bearing, mm) — single-sourced (was hardcoded 2200)
DRUM_CX = PW / 2        # light-lock center X in panel (centered horizontally)
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
    # The panel bottom is STEPPED: the two corner zones (Yd0..PANEL_CORNER_YD_L and
    # PANEL_CORNER_YD_R..PW) step UP by PANEL_BOTTOM_STEP to clear the bare walkway
    # cantilever bracket legs (walkway removed for transport — Sheet 16); the center
    # (drum bay) keeps the low bottom over the tray.
    from tbs_constants import PANEL_BOTTOM_STEP as STEP
    _sjL, _sjR = PANEL_CORNER_YD_L, PANEL_CORNER_YD_R

    def sbot(x0, x1, ztop, base):
        """Stepped-bottom band polygon: center bottom at `base`, corner bottoms at base+STEP."""
        return [(x0, base + STEP), (_sjL, base + STEP), (_sjL, base), (_sjR, base),
                (_sjR, base + STEP), (x1, base + STEP), (x1, ztop), (x0, ztop)]

    # Outer steel frame (50mm wide) — stepped bottom
    ax.add_patch(Polygon(sbot(0, PW, PH, 0), closed=True, fc=C_STEEL, ec=C_OUT, lw=2.5, zorder=2))
    # Skin area (inset of frame): rev11 — 1/8″ HDPE plastic sheet (C_PLASTIC), stepped bottom
    FR = 55  # visible frame width at face
    ax.add_patch(Polygon(sbot(FR, PW - FR, PH - FR, FR), closed=True,
                         fc=C_PLASTIC, ec=C_OUT, lw=0.8, zorder=3))
    ax.text(PW / 4 - 225, PH * 0.62,
            "1/8″ HDPE PLASTIC SKIN\n(U-channel set\nflat-black interior)",
            color=C_DIM, fontsize=6.5, ha="center", va="center", **FONT, zorder=15, alpha=0.8)
    # Fan B corner keeps an 18mm PLYWOOD mount band (bottom up to PANEL_FAN_BAND_Z)
    from tbs_constants import PANEL_FAN_BAND_Z as _PFBZ
    ax.add_patch(Rectangle((FR, STEP + FR), PANEL_CORNER_YD_L - FR, _PFBZ - STEP - FR,
                            fc=C_WOOD, ec=C_OUT, lw=0.8, zorder=3.2))    # bottom raised with the corner step
    ax.text(PANEL_CORNER_YD_L / 2 + 50, (_PFBZ + FR) / 2 + 200,
            "18mm PLY\nFAN-MOUNT BAND", color="#6a4010", fontsize=6,
            ha="center", va="center", fontweight="bold", **FONT, zorder=15, alpha=0.85)

    # ── EPDM perimeter seal (dashed inner contour) ────────────────────────────
    S = 30  # seal inset
    epdm = plt.Polygon(sbot(S, PW - S, PH - S, S),
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
    ax.text(STEP_YD_L + 210, PH - 360,
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
    for (y0, y1) in [(0, _CUT), (_FAR, PW)]:                  # both fixed strips sit in the stepped corner zones
        ax.add_patch(Rectangle((y0, STEP + FR), y1 - y0, PH - 2 * FR - STEP, fc="#C8A060",
                               ec="none", alpha=0.45, hatch="\\\\\\", zorder=4))
    for cx in [_CUT, _FAR]:
        ax.plot([cx, cx], [0, PH], color="#A000A0", lw=2.6, ls=(0, (5, 2)), zorder=11)
        ax.text(cx, PH + 35, f"CUT @ Yd{cx}\n(fixed ↔ swing)", color="#A000A0", fontsize=6,
                ha="center", va="bottom", fontweight="bold", **FONT, zorder=15)
    leader(ax, (_FAR + (PW - _FAR) / 2, PH / 2 - 250), (PW + 325, PH / 2 - 250),
           "FIXED FAR STRIP (Yd2287–2362)\nbolted to the door frame —\ndoes NOT swing", col="#6a4010", fs=6)
    leader(ax, (_CUT / 2, FR + 250), (-220, FR + 250),
           "FIXED LEFT PANEL (Yd0–180)\nbolted to the door frame —\ndoes NOT swing", col="#6a4010", fs=6)
    ax.text(PW / 2, FR + 170, "SWINGING PANEL  (Yd180 → 2287, pivots 56°)", color="#1763C8",
            fontsize=7, ha="center", va="bottom", fontweight="bold", **FONT, zorder=15, alpha=0.8)
    # ── bottom-step callout (corner zones raised to clear the walkway cantilever legs) ──
    for _sx in (PANEL_CORNER_YD_L, PANEL_CORNER_YD_R):
        ax.plot([_sx, _sx], [0, STEP], color="#B00", lw=2.0, zorder=12)
    draw_dim_v(ax, PANEL_CORNER_YD_L - 45, 0, STEP, f"{STEP}mm", offset=14, fs=6, font=FONT, right=False)
    ax.text(PW / 2, -145,
            f"BOTTOM STEPPED UP {STEP}mm AT BOTH CORNER ZONES — clears the bare walkway cantilever legs (walkway removed for transport, Sheet 16)",
            ha="center", va="center", fontsize=6.4, color="#B00", fontweight="bold", **FONT, zorder=15)

    # ── Fan B intake — weatherproof louvre on the panel exterior (near corner) ──
    from tbs_constants import FAN_B_YD as _FBY, FAN_B_H as _FBH
    fb_w, fb_h = 200, 200
    ax.add_patch(Rectangle((_FBY - fb_w / 2, _FBH - fb_h / 2), fb_w, fb_h,
                           fc="#8090A0", ec=C_OUT, lw=1.3, zorder=6))
    for i in range(1, 5):
        yy = _FBH - fb_h / 2 + i * fb_h / 5
        ax.plot([_FBY - fb_w / 2, _FBY + fb_w / 2], [yy, yy], color=C_OUT, lw=0.6, zorder=7)
    leader(ax, (_FBY, _FBH - fb_h / 2), (_FBY, _FBH - 200),
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

    ax.text(DRUM_CX + DRUM_R * 0.6 - 170,
            drum_body_y0 + drum_body_h * 0.45,
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
    leader(ax, (hx_handle + HW / 2, HY), (DX + DRUM_D - 230, HY + 200),
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
    leader(ax, (PIVOT_PX + 20, PH * 0.55), (PIVOT_PX + 250, PH / 2),
           "PIVOT POST\nØ89 CHS\n(vertical swing axis)",
           col="#5A5AA0", fs=6, fw="bold")
    # swing direction arc on the near (left) side
    arr_y = -80
    ax.annotate("", xy=(-HINGE_W - 40, arr_y + 80), xytext=(-HINGE_W - 40, arr_y),
                arrowprops=dict(arrowstyle="-|>", color="#1763C8", lw=1.6,
                                connectionstyle="arc3,rad=0.4", mutation_scale=11), zorder=15)
    ax.text(-HINGE_W - 425, PH / 2,
            "Panel + drum SWING 56°\nabout the far-edge pivot for\ntransport (no rails / no slide)\n— see Sheet 4",
            color=C_DIM, fontsize=6, ha="right", va="center", **FONT, zorder=15)

    # ── Cam latches (×2, OPENING EDGE) — INTERIOR FACE ──────────────────────
    # Only the free (latching) edge needs latching — the pivot edge is hinged and a
    # frame stop takes the outward direction. So TWO lift-and-turn cam latches (top +
    # bottom) on the OPENING edge (Yd≈180 cut, near side) hold the panel shut.
    # From this exterior view they are hidden features — shown dashed per
    # engineering convention for features on the far/hidden face. Interior mounting
    # enables emergency egress: if the drum jams, operators release them and push the
    # panel open INWARD (into the container about the pivot), clearing the door plane.
    LATCH_XS = [210]                       # opening edge only (pivot is on the far edge)
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
    leader(ax, (LATCH_XS[0], LATCH_YS[0]),
           (LATCH_XS[0] - 430, LATCH_YS[0] - 60),
           "CAM LATCH (McMaster 1619A74, ×2)\nOPENING EDGE, INTERIOR FACE — shown dashed\nEMERGENCY EGRESS: operate from inside if drum jams")

    # ── Interior pull handle — bolted to the frame, interior face (§4.3) ──────
    # Interior feature on this exterior view → dashed (like the latches above).
    # Mounted on the LEFT drum-aperture jamb (frame), just left of the Ø800 housing.
    HXD, HZD, HGL = 683, 1300, 300        # Yd 683 (left drum jamb) / Z 1300 / ~300mm grip
    ax.add_patch(Rectangle((HXD - 16, HZD - HGL / 2), 32, HGL, fc="none",
                           ec="#204080", lw=1.3, ls=(0, (4, 2)), zorder=8))
    for bz in (HZD - HGL / 2 + 18, HZD + HGL / 2 - 18):
        ax.add_patch(Circle((HXD, bz), 9, fc="#204080", ec="#204080", lw=0.8, zorder=9))
    leader(ax, (HXD - 16, HZD + HGL / 2),
           (HXD - 380, HZD + 540),
           "INTERIOR PULL HANDLE (§4.3)\nbolted to the drum-aperture jamb (frame) —\npull the panel open from inside",
           col="#204080", fw="bold")
    # the steel jamb beam the handle bolts to — shown so the mount beam is visible (cf. Sheet 6)
    JX0 = PANEL_CORNER_YD_L + 6            # 659 — left center-zone jamb (full-height frame member)
    ax.add_patch(Rectangle((JX0, 0), 40, PH, fc=C_STEEL, ec=C_OUT, lw=1.1, alpha=0.7, zorder=2))
    leader(ax, (JX0 - 20, HZD - HGL / 2), (980, 640),
           "2×2 STEEL JAMB —\nhandle bolts to steel,\nnot the skin (Sheet 6/9)", col=C_OUT, fs=6)

    # ── Inward-opening annotation ─────────────────────────────────────────────
    # The panel opens INWARD only (into the container about the Ø89 pivot); a stop on
    # the fixed frame takes the outward direction — the cam latches hold it shut (Sheet 13).
    leader(ax, (PW, PH * 0.36),
           (PW + 275, PH * 0.25),
           "OPENS INWARD ONLY\n(swings into the container;\na frame stop takes the\noutward direction — Sheet 13)",
           col="#204080", fw="bold")

    # ── Emergency egress safety note ──────────────────────────────────────────
    ax.text(PW / 2, -280,
            "SAFETY: Interior-mounted cam latches (×2, opening edge) allow emergency panel release from inside — "
            "operate if revolving drum jams. Panel opens INWARD about the pivot, clearing the door plane.",
            color="#C04010", fontsize=6.5, ha="center", va="center",
            fontweight="bold", **FONT, zorder=15)

    # ── EPDM seal leader ─────────────────────────────────────────────────────
    leader(ax, (PW - S, PH / 2 + 200),
           (PW + 320, PH / 2 + 300),
           "20mm EPDM GASKET\nIN ALUMINUM CHANNEL\n(PERIMETER, ALL SIDES)")

    # ── Dimension lines ───────────────────────────────────────────────────────
    # Panel width
    draw_dim_h(ax, 0, PW, PH + 200, f"{PW}mm  (CONTAINER INTERIOR WIDTH)", offset=20, fs=7, font=FONT)
    # Panel height
    draw_dim_v(ax, PW + 75, 0, PH, f"{PH}mm", offset=55, fs=7, right=True, font=FONT)
    # Drum diameter
    draw_dim_h(ax, DX, DX + DRUM_D, DY_TOP + 170, f"Ø{DRUM_D}mm DRUM", offset=30, fs=7, font=FONT)    # Drum clear height
    draw_dim_v(ax, DX - 200, DY_BOT, DY_TOP, f"{DRUM_H}mm CLEAR HEIGHT", offset=45, fs=7, right=True, font=FONT)
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
    title_block(ax, "SHEET 1 OF 17",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="FRONT ELEVATION — EXTERIOR VIEW",
                scale_note="SCALE 1:20",
                doc_id="TBS-001 \u00b7 Hinged Light-Trap Panel")

    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet1.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
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
# The drum (Ø800mm) is much larger than the panel depth (120mm + 40mm wall).
# In plan, the drum circle overhangs both panel faces — this is physically
# correct: the drum is secured by top/bottom bearings, not by the panel depth.
# The plan section shows this clearly.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():
    # ── Key dimensions (mm) ──────────────────────────────────────────────────
    from tbs_constants import WALL_T     # container end-wall steel thickness
    PLY_T  = 18     # ply skin thickness (each face)
    PT     = 120    # panel overall thickness (frame + 2 × ply)
    FRAME_T = PT - 2 * PLY_T   # = 84mm RHS frame depth

    # Y positions (depth) — TWO distinct members sit in front of the panel, matching the 3D:
    # the 40mm CONTAINER WALL, then the 50×20×3 RHS DOOR FRAME bolted into the opening. The panel
    # seals against the door frame's inner face (= the panel exterior).
    Y0_W  = 0                          # container-wall exterior face
    Y1_W  = WALL_T                     # = 40  wall inner face (= door-frame exterior)
    Y0_DF = Y1_W                       # door frame front (bolted to the wall opening)
    Y1_DF = Y0_DF + DOOR_FRAME_DEPTH   # = 60  door-frame inner face
    PANEL_EXT = Y1_DF                  # = 60  panel exterior (seal landing) — origin for the shared drum/cage X
    Y0_PL = PANEL_EXT    # outer ply starts at the panel exterior
    Y1_PL = Y0_PL + PLY_T
    Y0_FR = Y1_PL        # frame layer
    Y1_FR = Y0_FR + FRAME_T
    Y0_PL2 = Y1_FR       # inner ply
    Y1_PL2 = Y0_PL2 + PLY_T  # panel inner face

    Y_EXT = Y0_W         # exterior face = 0
    Y_INT = Y1_PL2       # interior face

    # Drum geometry — axis is vertical; plan section shows horizontal circle.
    # DEPTH single-sources from the SHARED 3D constants (DRUM_CX, DRUM_CAGE_X0/X1), which are
    # referenced to the PANEL exterior face; this plan's depth origin is the wall exterior, PANEL_EXT
    # in front — so a shared X maps to plan depth via `+ PANEL_EXT`. Zero drift with the 3D lighttrap
    # model (2026-09-02, Alvin: "both represent the same factual world").
    D_CX = PW / 2                    # drum center X: centered in panel width = 1181mm
    D_CY = LT_DRUM_CX + PANEL_EXT    # shared drum-axis depth (LT_DRUM_CX = tbs DRUM_CX)
    DR   = DRUM_R                    # = 400mm

    # Drum Y (depth) extents
    D_YB = D_CY - DR     # exterior overhang
    D_YT = D_CY + DR     # interior overhang
    # Cage depth envelope — the SHARED cage extent (embeds in the panel frame like the 3D)
    CAGE_YB = DRUM_CAGE_X0 + PANEL_EXT   # cage exterior face
    CAGE_YT = DRUM_CAGE_X1 + PANEL_EXT   # cage interior face (lands INSIDE the panel frame → welded)

    # Drum X extents
    D_XL = D_CX - DR    # = 731mm
    D_XR = D_CX + DR    # = 1631mm

    # ── View window — full panel width + margins ────────────────────────────
    # Corner zone thicknesses
    CORNER_T = 40   # corner zone panel thickness
    STEP_YD_L = PANEL_CORNER_YD_L   # 653 (rev8 widened)
    STEP_YD_R = PANEL_CORNER_YD_R  # 1709

    PAD_X  = 450   # horizontal margin each side (room for rails + labels)
    PAD_YB = 620   # bottom margin (exterior zone + room for the L-angle inset detail, clear of the title block)
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
    ax.text(D_CX - PAD_X / 2 - 450, (Y_INT + Y_HI) / 2 + 40,
            "INTERIOR", color="#407040", fontsize=9, ha="center", va="center",
            **FONT, fontweight="bold", alpha=0.55, zorder=15)

    # ── Container CARGO-DOOR FRAME cross-section (Y=0→40) — the panel seals against it (no solid "end
    #    wall" at the opening: the opening is FRAMED, not walled — Alvin 2026-09-01). Drawn at the side
    #    zones; the drum opening is cut out. ──
    # solid "#5A5E66" — the SAME cargo-frame grey as Sheets 9/10, so it reads as the door frame (not the
    # hatched panel steel). Drawn at the side zones; the drum opening is cut out.
    for _fx, _fw in [(0, D_XL), (D_XR, PW - D_XR)]:
        ax.add_patch(Rectangle((_fx, Y0_W), _fw, WALL_T, fc="#5A5E66", ec=C_OUT, lw=1.1, alpha=0.9, zorder=3.2))
    # 50×20×3 RHS DOOR FRAME (Y0_DF..Y1_DF) bolted into the opening, in front of the panel — the
    # panel EPDM seals against its inner face. Distinct lighter steel so it reads apart from the wall.
    for _fx, _fw in [(0, D_XL), (D_XR, PW - D_XR)]:
        ax.add_patch(Rectangle((_fx, Y0_DF), _fw, DOOR_FRAME_DEPTH, fc=C_STEEL, ec=C_OUT, lw=1.0, alpha=0.9, zorder=3.3))

    # ── CENTER ZONE = B2 PUNCH-OUT BAY ───────────────────────────────────────
    # The center zone is a rigid box protruding forward (depth from the panel
    # interior face Y_INT out to BAY_FRONT_X) that encloses the offset Ø800 housing.
    # The 128mm flank between the step line and the drum is the STEEL center-zone
    # frame jamb (over the panel depth); the bay side walls are THIN 1/8″ HDPE at
    # the step lines (drawn exaggerated for visibility — true wall = BAY_WALL_T 3.18mm).
    for x, w in [(STEP_YD_L, D_XL - STEP_YD_L), (D_XR, STEP_YD_R - D_XR)]:
        ax.add_patch(Rectangle((x, PANEL_EXT), w, Y_INT - PANEL_EXT,                  # steel frame jamb (panel depth)
                                fc=C_STEEL, ec=C_OUT, lw=1.0, hatch="///", zorder=3, alpha=0.75))
    BWALL = 16                                                              # bay-wall drawn thickness (true 3.18mm)
    # HDPE bay SIDE skins LAP the outboard face of the cage corner posts (no floating
    # gap) and are blind-riveted to them — same fixing as the front skin (Sheet 8). The
    # left skin covers post face X=DRUM_CAGE_YD_L; the right skin covers X=DRUM_CAGE_YD_R.
    side_faces = [(DRUM_CAGE_YD_L - BWALL, DRUM_CAGE_YD_L),                   # (skin x0, post face) — left
                  (DRUM_CAGE_YD_R, DRUM_CAGE_YD_R + BWALL)]                   # right (post face = x0)
    for xw, _pf in side_faces:
        ax.add_patch(Rectangle((xw, CAGE_YB), BWALL, PANEL_EXT - CAGE_YB,
                                fc=C_PLASTIC, ec=C_OUT, lw=1.0, zorder=4))
    # rivet line: horizontal-axis blind rivets (SIDE-VIEW glyph, not end-on circles) through
    # the HDPE side skin into each corner post — one at the exterior post, one at the interior.
    # Left skin is outboard of post face → factory head at −X (ang 180); right skin mirror (ang 0).
    post_face_L, post_face_R = DRUM_CAGE_YD_L, DRUM_CAGE_YD_R
    for pf, ang, cxr in ((post_face_L, 180, post_face_L - 8), (post_face_R, 0, post_face_R + 8)):
        for ry in (D_YB, D_YT):                              # exterior post + interior post
            _blind_rivet(ax, cxr, ry, ang, 16, d=6)
    ax.add_patch(Rectangle((DRUM_CAGE_YD_L, CAGE_YB), DRUM_CAGE_YD_R - DRUM_CAGE_YD_L, BAY_WALL_T * 4,  # bay front wall — width matches the cage frame (post-to-post)
                            fc=C_PLASTIC, ec=C_OUT, lw=1.0, zorder=4))
    # FRONT-face HDPE blind-riveted to the front cage frame (was missing — the SIDE skins have theirs above).
    # Vertical-axis glyph, factory head FLUSH on the exterior (−Y) surface (cz = BAY_FRONT_X + grip/2); SPREAD
    # along the wall, clear of the side-skin corner rivets. Smaller d so they don't crowd the corners.
    for fx in (DRUM_CAGE_YD_L + 170, (DRUM_CAGE_YD_L + DRUM_CAGE_YD_R) / 2, DRUM_CAGE_YD_R - 170):
        _blind_rivet(ax, fx, CAGE_YB + 6.5, 270, 13, d=6)
    leader(ax, (DRUM_CAGE_YD_L + 170, CAGE_YB), (DRUM_CAGE_YD_L - 250, CAGE_YB + 150),
           "FRONT-face HDPE riveted\nto the front cage frame", col="#4a5a70", fs=5.8)
    leader(ax, (post_face_L, D_YB), (STEP_YD_L - 240, D_YB - 200),
           "1/8″ HDPE bay SIDE skin — sits FLAT on the\nOUTSIDE face of the cage post; blind-riveted\nSTRAIGHT THROUGH into the post (see DETAIL below)", col="#4a5a70", fs=5.8)

    # ── ENLARGED DETAIL — HDPE side skin → cage post (the skin lies FLAT on the post's OUTSIDE face and
    #    is blind-riveted straight through the skin into the post's outer wall — no L-angle standoff) ──
    Lx0, Ly0, Ls = 1560, D_YB - 300, 2.4
    def dL(x, y): return (Lx0 + x * Ls, Ly0 + y * Ls)
    ax.add_patch(Rectangle(dL(-6, -6), 122 * Ls, 96 * Ls, fc="#FBFAF6", ec=C_DIM, lw=0.8, zorder=8))  # inset panel
    ax.text(*dL(58, 88), "DETAIL — HDPE SIDE SKIN → CAGE POST", ha="center", fontsize=7.4, fontweight="bold", color=C_OUT, zorder=12, **FONT)
    ax.text(*dL(58, 80), "skin flat on the post's outside face — riveted straight through", ha="center", fontsize=6.0, color=C_DIM, zorder=12, **FONT)
    ax.add_patch(Rectangle(dL(40, 8), 40, 62, fc=C_STEEL, ec=C_OUT, lw=1.3, hatch="///", zorder=9))             # cage post RHS (cut)
    ax.add_patch(Rectangle(dL(43, 11), 34, 56, fc="#FBFAF6", ec=C_OUT, lw=0.5, zorder=9))                       # RHS bore
    ax.text(*dL(60, 1), "cage post RHS", ha="center", fontsize=5.6, color=C_OUT, zorder=12, **FONT)
    ax.add_patch(Rectangle(dL(31, 8), 9, 62, fc=C_PLASTIC, ec=C_OUT, lw=1.2, zorder=10))                        # HDPE skin FLAT on the outboard face
    # blind rivet driven straight through the skin + post outer wall (factory head on the outboard face)
    ax.add_patch(Rectangle(dL(27, 34), 4, 10, fc="#C9CCD2", ec=C_OUT, lw=0.9, zorder=11))                       # factory head (outboard)
    ax.add_patch(Rectangle(dL(31, 37), 16, 4, fc="#C9CCD2", ec=C_OUT, lw=0.9, zorder=11))                       # shank through skin + wall
    ax.add_patch(Circle(dL(47, 39), 3.0, fc="#C9CCD2", ec=C_OUT, lw=0.9, zorder=11))                            # set (bulbed) tail inside the post
    leader(ax, dL(35, 39), dL(12, 6), "1/8″ HDPE skin\nflat on the post\noutside face", col=C_OUT, fw="bold", fs=6.0)
    leader(ax, dL(44, 39), dL(70, 58), "blind rivet — straight\nthrough the skin into\nthe post outer wall", col=C_OUT, fw="bold", fs=6.0)
    ax.text((STEP_YD_L + STEP_YD_R) / 2, CAGE_YB - 110, "PUNCH-OUT BAY (rev9)",
            color=C_OUT, fontsize=8.5, ha="center", va="top", **FONT,
            fontweight="bold", zorder=15)

    # ── CORNER ZONES (40mm envelope, Yd=0→653 and Yd=1709→2362) ──────────────
    # rev11: 1/8″ HDPE skin + framed HOLLOW core (Al stiffener rib grid) + 1/8″ HDPE skin.
    # The 40mm envelope is unchanged (frame depth). SS/weight audit 2026-07-29: the former
    # solid 3mm Al core is replaced by a 1"×1"×1/8" 6061 Al angle rib grid (redundant plate
    # dropped) — one VERTICAL rib per corner shows in this horizontal cut as an angle section.
    CORN_SKIN  = PANEL_SKIN_T                     # 1/8″ HDPE skin each face
    RIB        = 25                              # 1"×1"×1/8" Al stiffener rib (angle leg)
    CORN_Y_OUT = PANEL_EXT                       # panel exterior (seal landing)
    CORN_Y_IN  = PANEL_EXT + CORNER_T             # inner face (40mm envelope)

    # This section is cut at H=1000mm — BELOW the Fan B ply-band top (PANEL_FAN_BAND_Z), so the
    # NEAR corner (Yd 0→653, the fan side) is cut through the 18mm PLYWOOD band, while
    # the FAR corner is the 1/8″ HDPE skin. Both keep the 40mm envelope + Al stiffener rib.
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
        # Al stiffener rib (vertical, one per corner) — angle section at the corner mid-width
        xr = (x0 + x1) / 2 - RIB / 2
        ax.add_patch(Rectangle((xr, CORN_Y_OUT + skin_t), RIB, RIB,
                                fc=C_ALUM, ec=C_OUT, lw=0.6, hatch="xx", zorder=3.2))

    # ── Step transition lines ─────────────────────────────────────────────────
    for sx in [STEP_YD_L, STEP_YD_R]:
        # Vertical step face at transition
        ax.plot([sx, sx], [Y0_PL, Y1_PL2], color=C_OUT, lw=1.5, zorder=5)
        # Horizontal shelf connecting 40mm→120mm
        ax.plot([sx, sx], [CORN_Y_IN, Y1_PL2], color=C_OUT, lw=1.0,
                ls=(0, (4, 2)), zorder=4, alpha=0.7)

    # ── Layer labels (leaders from center zone) ───────────────────────────────
    LBL_OFF = 70
    lbl_x_r = D_XR + 60
    for ly, lbl, off in [
        (Y0_W + WALL_T / 2,  f"{WALL_T}mm CONTAINER WALL\n(door opening · M10 anchors)", 2.7 * LBL_OFF),
        (Y0_DF + DOOR_FRAME_DEPTH / 2,  "50×20×3 RHS DOOR FRAME\npanel seals here · U-frame welds (opening edge)", 1.6 * LBL_OFF),
        (Y0_PL + PLY_T / 2,  f"OUTER PLY ({PLY_T}mm)",                 1 * LBL_OFF),
    ]:
        ax.annotate(lbl, xy=(lbl_x_r, ly),
                    xytext=(lbl_x_r + off, ly - off),
                    fontsize=6.5, color=C_OUT, ha="left", va="top", **FONT,
                    arrowprops=dict(arrowstyle="->", linestyle=':', color=C_DIM, lw=0.8),
                    bbox=dict(fc="#EEF2F8", ec="none", pad=1.5), zorder=15)
    lbl_x_l = D_XL - 50
    for ly, lbl, off in [
        (Y0_FR - FRAME_T / 2, f"2×2×0.120in STEEL FRAME ({FRAME_T}mm)", 1.5 * LBL_OFF),
        (Y0_PL2 - PLY_T / 2,  f"INNER PLY — FLAT BLACK ({PLY_T}mm)",    2 * LBL_OFF),
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

    # (The exterior band along Y0..Y1_W is the container CARGO-DOOR FRAME the panel seals against — labeled
    #  below; per Option 1 there is no separate solid "end wall" at the opening, so no duplicate stile here.
    #  M10 anchor heads mark the frame→container bolts.)
    for df_x, df_wid in ((0, D_XL), (D_XR, PW - D_XR)):
        for ay in range(int(df_x) + 120, int(df_x + df_wid) - 60, 300):
            ax.add_patch(Circle((ay, Y0_W + WALL_T / 2), 5, fc="#2A2E34", ec=C_OUT, lw=0.5, zorder=6.2))  # M10 → container

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
           (rail_right_x + 200, Y_HI - 460),
           "PIVOT POST Ø89 CHS\n(vertical swing axis —\nno slide rail)", col="#5A5AA0", fs=6)
    leader(ax, (PW + brush_w / 2, Y0_PL + PT / 2),
           (rail_right_x + 200, Y_HI - 80),
           "GUIDE SLOT\n+ BRUSH SEAL\n(DOUBLED NYLON)", col=C_CARR, fs=6)

    # ── Drum: draw filled circle on top to cut out the drum hole ─────────────
    # First stamp BG color over wall/panel where drum sits, then draw drum ring
    drum_bg = Circle((D_CX, D_CY), DR, fc=BG, ec="none", zorder=7)
    ax.add_patch(drum_bg)

    # ── Housed revolving-door light lock (rev8) ──────────────────────────────
    # Fixed Ø800 housing (two 80° openings: exterior=down / interior=up) + a
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

    # ── Drum support CAGE — full 4-wall steel box around the drum (corner posts +
    #    perimeter rails) + the cross-beam carrying the central revolve bearing. ──
    from tbs_constants import DRUM_CAGE_YD_L as _CGL, DRUM_CAGE_YD_R as _CGR
    cage_yb, cage_yt = CAGE_YB, CAGE_YT                           # SHARED cage depth envelope (DRUM_CAGE_X0/X1)
    # CAGE TOP PERIMETER RAILS (50×50 RHS ring welded across the corner-post tops) — these
    # sit ABOVE the H=1000 cut, so they read as HIDDEN (dashed) members, not an envelope line.
    RAIL = 50
    top_rails = [
        (_CGL, cage_yb, _CGR - _CGL, RAIL),                      # exterior top rail
        (_CGL, cage_yt - RAIL, _CGR - _CGL, RAIL),               # interior top rail
        (_CGL, cage_yb, RAIL, cage_yt - cage_yb),                # left top rail
        (_CGR - RAIL, cage_yb, RAIL, cage_yt - cage_yb),         # right top rail
    ]
    for rx, ry, rw, rh in top_rails:
        ax.add_patch(Rectangle((rx, ry), rw, rh, fc=C_STEEL, ec=C_STEEL,
                               lw=1.2, ls=(0, (6, 3)), alpha=0.30, zorder=9.5))
    for cxp in (_CGL, _CGR - 50):                                 # 4 corner posts (50×50 RHS) — CUT at H=1000 (solid)
        for cyp in (cage_yb, cage_yt - 50):
            ax.add_patch(Rectangle((cxp, cyp), 50, 50, fc=C_STEEL, ec=C_OUT, lw=1.0, alpha=0.8, zorder=11))
    # ── DRUM SIDE LIGHT SEALS — vertical EPDM baffles at the drum-center plane (D_CY) closing the open
    #    gap between the fixed housing outer skin (D_XL/D_XR) and the cage/bay SIDE walls (_CGL/_CGR).
    #    At the drum equator the round housing spans the full width, so these two strips make the
    #    cross-section light-tight — blocks the straight-down-the-side leak (matches the 3D lighttrap). ──
    for bx0, bx1 in ((_CGL, D_XL), (D_XR, _CGR)):
        ax.add_patch(Rectangle((bx0, D_CY - 10), bx1 - bx0, 20, fc=C_GASKT, ec=C_OUT, lw=1.0, zorder=11.5))
    leader(ax, ((_CGL + D_XL) / 2, D_CY + 10), (D_XL - 300, D_CY + 300),
           "DRUM SIDE LIGHT SEAL (both sides)\nEPDM baffle: housing → cage side wall\n— blocks the down-the-side light leak", col=C_GASKT, fw="bold", fs=6)
    # ── EDGE L-ANGLES on the side-skin VERTICAL edges (both ends of each side wall): the post leg rivets to
    #    the cage corner post, the upstand backs the HDPE edge + the HDPE rivets to it (matches the 3D). ──
    LEG_A, LT_A = 40, 3
    def _edge_l(ux, uy, px, py):     # upstand (LT_A × LEG_A) + post leg (LEG_A+LT_A × LT_A)
        ax.add_patch(Rectangle((ux, uy), LT_A, LEG_A, fc=C_ALUM, ec=C_OUT, lw=0.8, zorder=11.7))
        ax.add_patch(Rectangle((px, py), LEG_A + LT_A, LT_A, fc=C_ALUM, ec=C_OUT, lw=0.8, zorder=11.7))
    _edge_l(_CGL - LT_A, cage_yb, _CGL - LT_A, cage_yb - LT_A)                       # near-front
    _edge_l(_CGL - LT_A, cage_yt - LEG_A, _CGL - LT_A, cage_yt)                      # near-back
    _edge_l(_CGR, cage_yb, _CGR - LEG_A, cage_yb - LT_A)                             # far-front
    _edge_l(_CGR, cage_yt - LEG_A, _CGR - LEG_A, cage_yt)                            # far-back
    leader(ax, (_CGL - LT_A, cage_yt - LEG_A / 2), (STEP_YD_L - 220, cage_yt + 120),
           "EDGE L-ANGLE (Al, 4× — each side-skin vertical edge)\npost leg riveted to the cage post · HDPE riveted to the upstand", col=C_OUT, fw="bold", fs=5.8)
    leader(ax, (_CGR - 25, cage_yb + 25), (D_XR + 200, cage_yb + 80),
           "DRUM SUPPORT CAGE (4-wall 50×50 steel box) — WELDED\nto the frame: back corner posts LAND IN / weld along the\ncenter-zone jambs (cage + frame = one swinging weldment)", col=C_STEEL, fs=6)
    leader(ax, (_CGL + (_CGR - _CGL) * 0.32, cage_yb + RAIL / 2), (D_XL - 300, cage_yb - 120),
           "CAGE TOP PERIMETER RAILS\n(50×50 RHS ring, above the\nH=1000 cut — shown hidden)", col=C_STEEL, fs=5.8)
    # cage → frame connection: the cage's BACK corner posts LAND INSIDE the frame jambs — the cage
    # interior face (CAGE_YT) sits at panel depth ~90mm, WITHIN the 40–160 frame depth — so cage +
    # frame are ONE weldment, welded along the embedded overlap (matches the 3D lighttrap model, where
    # the back posts are embedded in the jambs). Fillet-weld ticks mark where each post enters the frame.
    for cxp in (_CGL, _CGR - 50):                                         # back corner posts (Yd), embedded in the jambs
        for wy, dy in ((cxp + 6, 12), (cxp + 44, -12)):                  # weld fillets along the post↔jamb interface
            ax.add_patch(Polygon([(wy, PANEL_EXT), (wy, PANEL_EXT + 16), (wy + dy, PANEL_EXT)], closed=True, fc=C_OUT, ec="none", zorder=12))
    cb_t = 50
    # cross-beam is ABOVE + BELOW the H=1000 cut → drawn HIDDEN (dashed outline, no fill), like the top
    # perimeter rails, so the side light-seal baffles read as the SOLID cut element, not "through" it.
    ax.add_patch(Rectangle((_CGL, D_CY - cb_t / 2), _CGR - _CGL, cb_t,
                           fc="none", ec=C_STEEL, lw=1.0, ls=(0, (6, 3)), alpha=0.6, zorder=11))
    # revolve bearing — CENTERED on the drum axis (the bore label is offset below it instead)
    ax.add_patch(Circle((D_CX, D_CY), 60, fc="#5A5AA0", ec=C_OUT, lw=1.3, zorder=12))
    leader(ax, (_CGL + 40, D_CY - cb_t / 2), (D_XL - 320, D_CY - DR * 0.4),
           "DRUM CAGE CROSS-BEAM (top +\nbottom) carrying the central\nØ220/Ø120 revolve bearing", col=C_STEEL, fs=6)
    # daylight ray at ENTER: enters bore from exterior, blocked at interior by drum
    ax.annotate("", xy=(D_CX, D_CY + LT_DRUM_OR * 0.9), xytext=(D_CX, D_YB - 70),
                arrowprops=dict(arrowstyle="-|>", color="#D08000", lw=1.8), zorder=12)
    ax.plot([D_CX], [D_CY + LT_DRUM_OR], marker="x", ms=10, mew=2.4,
            color="#2E8B57", zorder=13)
    ax.text(D_CX, D_CY - DR * 0.45, f"Ø{int(2 * BORE_R)} bore\n~555mm passage", color=C_DIM,
            fontsize=6.2, ha="center", va="center", **FONT, zorder=15)

    # Opening labels + component leaders
    ax.text(D_CX, D_YB - 75, "exterior opening (ENTER)", color="#A05000",
            fontsize=6.5, ha="center", va="top", **FONT, zorder=15)
    ax.text(D_CX, D_YT + 60, "interior opening → onto walkway", color=C_OUT,
            fontsize=6.5, ha="center", va="bottom", **FONT, zorder=15)
    leader(ax, (D_CX + DR * 0.92, D_CY + DR * 0.30),
           (D_XR + 350, D_CY + DR * 0.25),
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
    ax.text(D_XR + 95, D_CY - DR * 0.78,
            f"Two {OD}° openings, 180° apart;\nthe housing's solid wall always\ncovers the opening the drum\n"
            "isn't aligned with → NO straight-\nline sight at any rotation.\nSee Sheet 5 (enter / transit / exit).",
            color="#2E8B57", fontsize=6.4, ha="left", va="center", **FONT, zorder=15)

    # ── Dimension lines ────────────────────────────────────────────────────────
    DIM_X_R = D_XR + PAD_X * 0.35   # right-side dim column

    # Drum diameter (horizontal)
    draw_dim_h(ax, D_XL, D_XR, D_YT + PAD_YT * 0.55,
          f"Ø{DRUM_D}mm  DRUM DIAMETER", fs=7, offset=-25, above=False, font=FONT)
    # Container wall thickness — arrow + inline label (no leader, avoids crossing
    # the nearby CONTAINER END WALL and OUTER PLY leader lines)
    draw_dim_v(ax, DIM_X_R, Y0_W, Y1_W,
          f"  {WALL_T}mm", offset=15, fs=6.5, right=True, font=FONT)

    # Panel overall thickness — arrow + inline label
    draw_dim_v(ax, DIM_X_R, PANEL_EXT, Y1_PL2,
          f"  {PT}mm", offset=15, fs=6.5, right=True, font=FONT)

    # Exterior drum overhang — 45° leader going south-left
    ext_oh_mid = (D_YB + Y0_W) / 2
    draw_dim_v(ax, D_XL - 150, D_YB, Y0_W, f"{int(Y0_W - D_YB)}mm EXT. OVERHANG", offset=15, fs=6, right=True, font=FONT)

    # Interior drum overhang dimension
    # (No interior overhang: the drum sits in the exterior punch-out; its back edge is ~flush with the
    #  panel exterior and the cage embeds into the panel frame — so an "INT. OVERHANG" dim is N/A.)

    # Full panel width dimension
    draw_dim_h(ax, 0, PW, Y_LO + 220, f"{PW}mm  (FULL PANEL WIDTH)", fs=7, offset=-15, font=FONT)

    # Zone width dimensions (above panel)
    zone_dim_y = D_YT + PAD_YT * 0.80
    draw_dim_h(ax, 0, STEP_YD_L, zone_dim_y-30,
          f"{STEP_YD_L}mm", fs=6, offset=-15, font=FONT)
    draw_dim_h(ax, STEP_YD_L, STEP_YD_R, zone_dim_y-30,
          f"{STEP_YD_R - STEP_YD_L}mm CENTER", fs=6, offset=-15, font=FONT)
    draw_dim_h(ax, STEP_YD_R, PW, zone_dim_y-30,
          f"{PW - STEP_YD_R}mm", fs=6, offset=-15, font=FONT)

    # Corner zone thickness dimension
    draw_dim_v(ax, STEP_YD_L / 2 - 100, PANEL_EXT, CORN_Y_IN,
          f"{CORNER_T}mm", offset=15, fs=6, right=True, font=FONT)

    # ── Scale and note ────────────────────────────────────────────────────────
    ax.text(PW / 2, Y_HI - 20,
            "EQUAL ASPECT  ·  SCALE 1:20 (APPROX)  ·  FULL PANEL WIDTH  ·  "
            "DRUM OVERHANGS PANEL ON BOTH FACES — SECURED BY BEARINGS AT TOP AND BOTTOM",
            color=C_DIM, fontsize=6.5, ha="center", va="top", **FONT, zorder=15)

    # ── Orientation clarification note (standard draw_notes block, top-right) ──
    OB_X = D_XR + 330
    OB_Y = D_YT - 600
    OB_W = 450   # retained: the latch note below positions itself off the note width
    draw_notes(ax, [
        "ORIENTATION NOTE",
        "Drum axis is vertical.",
        "Personnel walk through in",
        "an upright position.",
        "See Sheet 3 for the elevation view.",
    ], OB_X + 32, OB_Y + 174, spacing=32, fs=6, title_fs=6.5,
       color="#403000", title_color="#806010", width=400,
       border_color="#806010", font=FONT)

    # ── Interior latch safety note ─────────────────────────────────────────────
    # Small note below orientation box (latches are outside the drum-zone crop
    # in this view but their presence and position is relevant to egress design)
    ax.text(OB_X + OB_W / 2 + 450, OB_Y - 25,
            "CAM LATCH (McMaster 1619A74, lift-and-turn):\nINTERIOR handle → welded keeper on the stub wall.\nPANEL OPENS INWARD ONLY (frame stop takes outward).\nEgress operable from inside. See Sheet 13 Detail A.",
            ha="center", va="top", fontsize=6, color="#C04010",
            fontweight="bold", **FONT, zorder=15)

    # ── Material legend (rev11 wood/plastic differentiation) ──────────────────
    draw_legend(ax, [
        (C_PLASTIC, "1/8″ HDPE skin + B2 bay"),
        (C_WOOD, "18mm ply — Fan B mount band"),
        (C_ALUM, "Al corner stiffener rib"),
        (C_STEEL, "steel RHS frame / wall"),
        (C_GASKT, "20mm EPDM seal"),
    ], X_LO + 20, (Y_LO + Y_HI) / 2 + 160, title="MATERIALS", fs=6, col_w=420)

    # ── Title block ────────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 17",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="PLAN CROSS-SECTION (SECTION A-A AT H=1000mm) — HOUSED REVOLVING DOOR (HOUSING + C-SHELL DRUM, NO FINS)",
                scale_note="EQUAL ASPECT  \u00b7  SCALE 1:20 (APPROX)  \u00b7  ALL DIMS IN mm",
                doc_id="TBS-001 \u00b7 Hinged Light-Trap Panel", height=0.055)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet2.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
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
    from tbs_constants import WALL_T    # container end-wall steel thickness
    PLY_T   = PANEL_SKIN_T   # rev11: 1/8″ HDPE skin each face (was 18mm ply); envelope kept via FRAME_T
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
    D_CX_DEPTH = BAY_FRONT_X + DRUM_R + 40   # B2: housing depth center = -450mm
    D_HALF_W   = DRUM_R                 # drum/housing radius = 400mm (in depth axis)

    D_DEPTH_L  = D_CX_DEPTH - D_HALF_W   # = -450 - 400 = -850mm (exterior overhang)
    D_DEPTH_R  = D_CX_DEPTH + D_HALF_W   # = -450 + 400 = -50mm  (interior overhang)

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

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DIAGRAM_DPI)
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
    # The Ø750 / 4-baffle drum was replaced (rev8) by a fixed Ø800 housing with a
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

    bx0, bx1 = DX(-98), DX(300)
    by0, by1 = DY(-28), DY(182)
    ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0,
                           fc="#FBFBFD", ec=C_DIM, lw=1.0, ls=(0, (5, 3)), zorder=2))
    ax.text((bx0 + bx1) / 2, by1 + 34, "DETAIL B — PANEL BOTTOM SEAL",
            ha="center", va="bottom", fontsize=9, fontweight="bold", color=C_OUT, **FONT)
    ax.text((bx0 + bx1) / 2, by1 + 10,
            "operational / “camera” position  ·  section at corner zone  ·  enlarged ~3.3:1",
            ha="center", va="bottom", fontsize=6.4, color=C_DIM, **FONT)
    ax.text(DX(-90), DY(170), "EXTERIOR", fontsize=6, color="#5060A0",
            ha="left", va="center", fontweight="bold", **FONT)
    ax.text(DX(170), DY(170), "INTERIOR", fontsize=6, color="#407040",
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
    dlbl((DX(20), DY(165)), DY(155), "Cam latch compresses panel\nonto seal (release to swing)")
    dlbl((DX(20), DY(120)), DY(128), "Panel bottom edge\n(40 mm corner zone)")
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

    cbx0, cbx1 = CX(-98), CX(300)
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
    odx, ody = 1250, 1240   # right border aligned with Details C/B (DDX(60)=1567≈bx1/cbx1);
                            # ody keeps it vertically between Details C (above) and B (below)
    def DDX(x): return odx + k * x          # panel depth (mm) → sheet x (exterior negative)
    def DDY(yr): return ody + k * yr        # Yd about the cut (yr=0) → sheet y
    dbx0, dbx1 = DDX(-180), DDX(220)
    dby0, dby1 = DDY(-64), DDY(60)

#         cbx0, cbx1 = CX(-98), CX(300)
#     cby0, cby1 = CY(-108), CY(102)

    ax.add_patch(Rectangle((dbx0, dby0), dbx1 - dbx0, dby1 - dby0,
                           fc="#FBFBFD", ec=C_DIM, lw=1.0, ls=(0, (5, 3)), zorder=2))
    ax.text((dbx0 + dbx1) / 2, dby1 + 30, "DETAIL D — VERTICAL CUT SEAL",
            ha="center", va="bottom", fontsize=9, fontweight="bold", color=C_OUT, **FONT)
    ax.text((dbx0 + dbx1) / 2, dby1 + 8,
            "plan section at the fixed↔swing joint (Yd180 / Yd2287)  ·  enlarged ~3.3:1",
            ha="center", va="bottom", fontsize=6.4, color=C_DIM, **FONT)
    ax.text(DDX(-75), DDY(48), "EXTERIOR", fontsize=6, color="#5060A0",
            ha="left", va="center", fontweight="bold", **FONT)
    ax.text(DDX(100), DDY(48), "INTERIOR", fontsize=6, color="#407040",
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
    ddlbl((DDX(20), DDY(30)), DDY(35), "SWINGING panel edge\n(joint opens as it swings)")

    # ── Title block (portrait sheet — taller box, smaller fonts, clipped) ──────
    title_block(ax, "SHEET 3 OF 17",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="DRUM ELEVATION — SECTION A-A: VERTICAL DRUM, WALKING HEIGHT",
                scale_note="EQUAL ASPECT  \u00b7  SCALE 1:20 (APPROX)  \u00b7  ALL DIMS IN mm",
                doc_id="TBS-001 \u00b7 Hinged Light-Trap Panel",
                height=0.05, portrait=True)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet3.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
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
    R, OR = DRUM_R, LT_DRUM_OR             # housing 400, drum outer 382
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
    ax.text(1000, 1378, "Fixed Ø800 housing (two 80° openings, 180° apart) + single-opening C-shell drum",
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

    title_block(ax, "SHEET 5 OF 17",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="REVOLVING-DOOR LIGHT LOCK (rev 8) — ACCESS & LIGHT-TIGHTNESS VERIFICATION (BOTH PASS)",
                scale_note="PLAN VIEWS · NOT TO SCALE · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.045)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet5.png"), dpi=DIAGRAM_DPI,
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
    ax.text(d1[0], d1[1], f"SWUNG {int(LOCK)}°\n(door clears +{SWUNG_DOOR_CLEARANCE_MM}mm)", fontsize=7, color=BLUE, **FONT,
            ha="center", va="center", fontweight="bold", zorder=15)
    arc = [rot(0, CUT, dd) for dd in np.linspace(0, LOCK, 36)]
    ax.plot([p[0] for p in arc], [p[1] for p in arc], color=BLUE, lw=1.3, ls=(0, (4, 2)), zorder=11)

    # numbered markers
    def mark(x, y, n, col=BLUE):
        ax.add_patch(Circle((x, y), 58, fc="white", ec=col, lw=2.2, zorder=14))
        ax.text(x, y, str(n), fontsize=12, color=col, **FONT, fontweight="bold",
                ha="center", va="center", zorder=15)
    mark(RX, 430, 1); mark(RX, 1940, 1)       # left rails struck so the cage transitions
    mark(40, cyd, 2)                          # swing clears the door plane (SWUNG_DOOR_CLEARANCE_MM)

    ax.text(-280, 2640, "SWING CLEARANCE vs FILM-PLANE LEFT MECHANISM  (plan, looking down)",
            fontsize=13, fontweight="bold", color=C_OUT, **FONT)
    notes = [
        "ROTATION TRANSPORT (rev10):",
        "The panel + drum SWING ~56° about the vertical",
        "pivot (the film far-left post), pulling the punch-",
        "out bay inboard of the door plane so the cargo",
        f"doors close (true min X +{SWUNG_DOOR_CLEARANCE_MM}mm).",
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

    title_block(ax, "SHEET 4 OF 17",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="ROTATING TRANSPORT + SWING CLEARANCE vs FILM-PLANE LEFT MECHANISM (PLAN)",
                scale_note="PLAN VIEW · NOT TO SCALE · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.045)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet4.png"), dpi=DIAGRAM_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet4.png saved")

def sheet6():
    """Sheet 6 — interior pull-handle mounting detail. Horizontal section through the
    panel's left drum-aperture jamb: the matte-black McMaster 1871A65 round pull handle
    (the SAME off-the-shelf part as the interior drum handle) screwed into RIVNUTS set in
    the near wall of the 2×2×0.120in steel frame RHS — the load reacts into the STEEL, not
    the HDPE skin (rivnuts because the 3mm tube wall can't be tapped)."""
    fig, ax = plt.subplots(figsize=(11, 8.0))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-95, 215); ax.set_ylim(-150, 150)

    ax.text(60, 135, "INTERIOR PULL HANDLE — MOUNTING DETAIL", ha="center",
            fontsize=12, fontweight="bold", color=C_OUT, **FONT)
    ax.text(60, 116, "Horizontal section through the swinging-panel drum-aperture frame jamb",
            ha="center", fontsize=8, color=C_DIM, **FONT)

    # exterior ↔ interior axis (exterior = door plane on the left, container interior right)
    ax.annotate("", xy=(150, 95), xytext=(80, 95),
                arrowprops=dict(arrowstyle="-|>", color=C_DIM, lw=1.4))
    ax.text(115, 84, "INTERIOR →", ha="center", fontsize=7.5, color=C_DIM, **FONT)
    ax.text(-58, 88, "← EXTERIOR\n(door plane)", ha="center", fontsize=7.5, color=C_DIM, **FONT)

    # 2×2×0.120in steel frame member (3mm walls)
    ax.add_patch(Rectangle((0, -25), 50, 50, fc=C_STEEL, ec=C_OUT, lw=1.8, zorder=3))
    ax.add_patch(Rectangle((3, -22), 44, 44, fc=BG, ec=C_OUT, lw=1.0, zorder=4))
    leader(ax, (24, -25), (50, -50), "2×2×0.120in steel frame jamb\n(beside drum aperture)", col=C_OUT)
    # 1/8″ HDPE interior skin on the +X face
    ax.add_patch(Rectangle((50, -25), 4, 50, fc=C_PLASTIC, ec=C_OUT, lw=0.8, zorder=4))
    leader(ax, (52, 20), (78, 95), "1/8″ HDPE\ninterior skin", col=C_OUT)
    # 1871A65 round pull handle (SAME part as the interior drum handle): foot plate,
    # two ~52mm standoff posts, Ø12.7 grip bar (vertical → a circle in this section).
    HA = 0.65
    ax.add_patch(Rectangle((54, -20), 5, 40, fc="#202020", ec=C_OUT, lw=1.0, alpha=HA, zorder=5))   # foot plate
    for fy in (-15, 15):
        ax.add_patch(Rectangle((59, fy - 4), 52, 8, fc="#202020", ec=C_OUT, lw=0.8, alpha=HA, zorder=5))  # standoff post
    ax.add_patch(Circle((117, 0), 6.35, fc="#202020", ec=C_OUT, lw=1.2, alpha=HA, zorder=6))         # Ø12.7 grip bar
    leader(ax, (117, 7), (150, 58),
           "12\" round pull handle — McMaster 1871A65\n(Ø12.7 bar) — SAME as the interior drum handle;\nmatte-black (optically dead)", col=C_OUT, fw="bold")
    # 2× 1/4" screws through the feet into RIVNUTS set in the near RHS wall (load into steel, not the skin)
    for by in (-15, 15):
        _draw_bolt(ax, 54, by, 10, d=6, vertical=False, head=1, end="rivnut", wall=3, zb=7)
    leader(ax, (49, 15), (8, 58),
           "2× 1/4\" screws into RIVNUTS in the near\nRHS wall (can't tap the 3mm tube; load\nreacts into STEEL, not the HDPE skin)", col=C_OUT, fw="bold")

    # ── dimensions (prove the drawing is to scale) ──
    draw_dim_h(ax, 0, 50, -62, "50mm", offset=10, fs=6.5, font=FONT, above=False)          # frame width
    draw_dim_v(ax, 128, -6.35, 6.35, "Ø12.7mm", offset=9, fs=6.2, font=FONT, right=True)   # grip bar Ø
    draw_dim_h(ax, 59, 111, 40, "~52mm standoff", offset=9, fs=6.0, font=FONT)             # handle projection
    ax.text(110, -30, "grip bar runs VERTICAL, ~308mm\n(shown here in cross-section)", ha="center", va="top", fontsize=5.8, color=C_DIM, **FONT)
    # ── scale bar (50mm) ──
    sbx0 = -88
    ax.plot([sbx0, sbx0 + 50], [-118, -118], color=C_OUT, lw=2.2, zorder=9)
    for xt in (sbx0, sbx0 + 25, sbx0 + 50):
        ax.plot([xt, xt], [-118, -111], color=C_OUT, lw=1.1, zorder=9)
    ax.text(sbx0 + 25, -128, "0   25   50 mm", ha="center", fontsize=6.2, color=C_OUT, **FONT)

    ax.text(60, -103,
            "The handle screws into RIVNUTS set in the 50×50 RHS wall — the swing load\n"
            "reacts into the STEEL frame, never the HDPE skin. Same off-the-shelf pull handle\n"
            "(McMaster 1871A65) as the interior drum handle. Matte-black keeps the interior\n"
            "optically dead (stray-light control for the pinhole).",
            ha="center", fontsize=7.5, color=C_OUT, **FONT,
            bbox=dict(boxstyle="round,pad=0.4", fc="#F4F1E8", ec=C_DIM, lw=0.7))

    title_block(ax, "SHEET 6 OF 17", drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="INTERIOR PULL HANDLE — MOUNTING DETAIL (HORIZONTAL SECTION)",
                scale_note="DRAWN TO SCALE (isotropic ~1:1) · 50mm BAR · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet6.png"), dpi=DIAGRAM_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet6.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 7  —  HDPE Surround: Flat-Pattern Cut Sheets
#   The center-zone / B2-punch-out-bay HDPE surround (1/8" black HDPE, US Plastics
#   46684) developed flat for cutting. Six pieces: the two center-zone panel-face
#   skins (with the personnel light-lock opening), the two bay Yd side walls, and
#   the upper + lower floor caps (with the Ø800 housing seat). Every blank is
#   dimensioned off the panel/bay/drum constants, so the set tracks the housing Ø.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet7():
    W_CTR   = PANEL_CENTER_W               # 1056 — center-zone width (Yd 653..1709)
    H_PANEL = PH                           # 2388 — panel / door-opening height
    BAY_D   = BAY_BACK_X - BAY_FRONT_X      # 890 — bay depth (panel plane .. exterior face)
    R_HOUS  = DRUM_R                       # 400 — Ø800 housing seat radius
    RIV_P   = LT_RIVET_PITCH               # 60 — blind-rivet pitch
    OPEN_W  = round(2 * R_HOUS * math.sin(math.radians(LT_OPENING_DEG / 2)))  # ~514 — 80° passage chord

    fig, ax = plt.subplots(figsize=(21, 15))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_aspect("equal"); ax.axis("off")

    # ── piece-drawing helpers ────────────────────────────────────────────────
    def rivet_edge(x0, y0, w, h, edge, holes=True):
        """Blind-rivet lap line on one edge (bronze). holes=True draws the pattern;
        else a dashed 'typ' line. Rivet Ø drawn ~7mm (exaggerated) — true Ø is RIV_H."""
        inset = 24
        if edge in ("L", "R"):
            xr = x0 + inset if edge == "L" else x0 + w - inset
            pts = [y0 + 70 + i * RIV_P for i in range(int((h - 140) // RIV_P) + 1)]
            ax.plot([xr, xr], [pts[0], pts[-1]], color="#A8763A",
                    lw=0.6, ls=(0, (4, 3)), zorder=6)
            if holes:
                for yy in pts:
                    ax.add_patch(Circle((xr, yy), 7, fc="none", ec="#A8763A", lw=0.8, zorder=7))
        else:
            yr = y0 + inset if edge == "B" else y0 + h - inset
            pts = [x0 + 70 + i * RIV_P for i in range(int((w - 140) // RIV_P) + 1)]
            ax.plot([pts[0], pts[-1]], [yr, yr], color="#A8763A",
                    lw=0.6, ls=(0, (4, 3)), zorder=6)
            if holes:
                for xx in pts:
                    ax.add_patch(Circle((xx, yr), 7, fc="none", ec="#A8763A", lw=0.8, zorder=7))

    def blank(x0, y0, w, h):
        ax.add_patch(Rectangle((x0, y0), w, h, fc=C_PLASTIC, ec=C_OUT, lw=1.5, zorder=3))

    def piece_title(x0, y0, w, ytop, title, sub=""):
        """Title + material sub placed near the TOP of a piece (clear of a central opening)."""
        ax.text(x0 + w / 2, ytop, title, ha="center", va="center",
                fontsize=8.5, fontweight="bold", color=C_OUT, **FONT, zorder=8)
        if sub:
            ax.text(x0 + w / 2, ytop - 95, sub, ha="center", va="center",
                    fontsize=6.6, color=C_DIM, **FONT, zorder=8)

    # ── layout (mm canvas; equal aspect) ─────────────────────────────────────
    GAP = 430
    yA  = 0                                 # tall row (face skins + bay walls)
    yB  = -(BAY_D + 620)                     # caps row

    xS1 = 0                                  # exterior face skin
    xS2 = xS1 + W_CTR + GAP                   # interior face skin
    xW1 = xS2 + W_CTR + GAP                   # bay near wall
    xW2 = xW1 + BAY_D + GAP                   # bay far wall
    xC1 = 0                                  # upper floor cap
    xC2 = xC1 + W_CTR + GAP                    # lower floor cap

    # 1-2 · center-zone face skins (exterior + interior) with the personnel opening
    for i, (x0, face) in enumerate([(xS1, "EXTERIOR"), (xS2, "INTERIOR")]):
        blank(x0, yA, W_CTR, H_PANEL)
        piece_title(x0, yA, W_CTR, yA + H_PANEL - 150, f"{face} FACE SKIN", "1/8\" HDPE · center zone")
        # personnel light-lock opening — centered, trimmed to the housing at assembly
        ox = x0 + (W_CTR - OPEN_W) / 2
        oy0, oy1 = yA + 430, yA + H_PANEL - 430
        ax.add_patch(Rectangle((ox, oy0), OPEN_W, oy1 - oy0, fc=BG,
                               ec=C_OUT, lw=1.1, ls=(0, (6, 3)), zorder=4))
        ax.text(x0 + W_CTR / 2, (oy0 + oy1) / 2,
                "PERSONNEL OPENING\n(trim to housing\n— Sheet 2 / 8)",
                ha="center", va="center", fontsize=6.6, color=C_DIM, **FONT, zorder=5)
        draw_dim_h(ax, ox, ox + OPEN_W, oy1 + 70, f"{OPEN_W}mm personnel opening", offset=14, fs=6.2, font=FONT)
        ax.text(x0 + W_CTR / 2, oy1 + 150, "≥ drum 80° passage (~487mm, §3.1) — operator fits", ha="center", fontsize=5.8, color=C_DIM, **FONT, zorder=6)
        # size + locate the cutout: height (dim_v) beside it, bottom margin, and left edge offset
        opening_h = oy1 - oy0
        left_margin = (W_CTR - OPEN_W) / 2
        draw_dim_v(ax, ox + OPEN_W + 55, oy0, oy1, f"{int(opening_h)}mm opening ht", offset=14, fs=6.0, font=FONT, right=True)
        draw_dim_v(ax, ox + OPEN_W + 150, yA, oy0, f"{int(oy0 - yA)}mm btm margin", offset=14, fs=6.0, font=FONT, right=True)
        draw_dim_h(ax, x0, ox, oy0 - 70, f"{int(left_margin)}mm", offset=-12, fs=6.0, font=FONT)
        rivet_edge(x0, yA, W_CTR, H_PANEL, "L", holes=(i == 0))
        draw_dim_v(ax, x0 - 60, yA, yA + H_PANEL, f"{H_PANEL}mm", offset=16, fs=6.5, font=FONT)
        draw_dim_h(ax, x0, x0 + W_CTR, yA - 70, f"{W_CTR}mm", offset=14, fs=6.5, font=FONT)

    # 3-4 · bay Yd side walls (near + far) — flat rectangles, lap to frame + caps
    for x0, side in [(xW1, "NEAR"), (xW2, "FAR")]:
        blank(x0, yA, BAY_D, H_PANEL)
        piece_title(x0, yA, BAY_D, yA + H_PANEL / 2, f"BAY {side}\nYd WALL", "1/8\" HDPE · punch-out bay")
        rivet_edge(x0, yA, BAY_D, H_PANEL, "L", holes=False)
        draw_dim_h(ax, x0, x0 + BAY_D, yA - 70, f"{BAY_D}mm (bay depth)", offset=14, fs=6.5, font=FONT)
        draw_dim_v(ax, x0 - 60, yA, yA + H_PANEL, f"{H_PANEL}mm", offset=16, fs=6.5, font=FONT)

    # 5-6 · upper + lower floor caps — with the Ø800 housing seat (join → Sheet 8)
    for x0, cap in [(xC1, "UPPER"), (xC2, "LOWER")]:
        blank(x0, yB, W_CTR, BAY_D)
        piece_title(x0, yB, W_CTR, yB + BAY_D - 70, f"{cap} FLOOR CAP", "1/8\" HDPE")
        # Ø800 housing seat (centered on the drum footprint in the cap)
        ccx = x0 + (PW / 2 - PANEL_CORNER_YD_L)         # drum Yd center within the cap width (1181-653=528)
        ccy = yB + (DRUM_R + 40)                        # drum depth center from the bay front edge (~440)
        ax.add_patch(Circle((ccx, ccy), R_HOUS, fc=BG, ec=C_OUT, lw=1.2, ls=(0, (6, 3)), zorder=4))
        ax.plot([ccx - R_HOUS - 40, ccx + R_HOUS + 40], [ccy, ccy], color=C_CL, lw=0.7, ls="--", zorder=5)
        ax.plot([ccx, ccx], [ccy - R_HOUS - 40, ccy + R_HOUS + 40], color=C_CL, lw=0.7, ls="--", zorder=5)
        ax.text(ccx, ccy - 60, f"Ø{int(2 * R_HOUS)} housing seat", ha="center", va="center",
                fontsize=6.6, color=C_DIM, **FONT, zorder=6)
        rivet_edge(x0, yB, W_CTR, BAY_D, "B", holes=False)
        draw_dim_h(ax, x0, x0 + W_CTR, yB - 60, f"{W_CTR}mm", offset=14, fs=6.5, font=FONT)
        draw_dim_v(ax, x0 - 55, yB, yB + BAY_D, f"{BAY_D}mm", offset=16, fs=6.5, font=FONT, right=False)

    # ── scale bar (500mm) ────────────────────────────────────────────────────
    sbx, sby = xW2 + BAY_D - 500, yB + 40
    ax.plot([sbx, sbx + 500], [sby, sby], color=C_OUT, lw=2.2, zorder=9)
    for xt in (sbx, sbx + 250, sbx + 500):
        ax.plot([xt, xt], [sby, sby + 45], color=C_OUT, lw=1.2, zorder=9)
    ax.text(sbx + 250, sby - 70, "0        250       500 mm", ha="center", fontsize=6.5, color=C_OUT, **FONT)

    # ── materials / fabrication notes ────────────────────────────────────────
    notes = (
        "HDPE SURROUND — FABRICATION NOTES\n"
        "• Material: 1/8\" (3.18mm) black UV-HDPE sheet — US Plastics 46684; interior face flat-black.\n"
        "• 6 pieces: 2 center-zone face skins · 2 bay Yd side walls · upper + lower floor caps.\n"
        "• Bay = 4-wall corner-welded box (extrusion-welded seams); caps close the top + bottom.\n"
        f"• Rivet each lap to the steel frame — FRONT + SIDE faces of the posts (not the front only) — with\n"
        f"  1/8\" 18-8 SS blind rivets @ {RIV_P}mm (drill Ø{LT_RIVET_HOLE}). Ø800 housing seat + rivet lap detail → SHEET 8.\n"
        "• Personnel opening trimmed to the housing at assembly — align to SHEET 2 (plan)."
    )
    ax.text(xC2, yB + BAY_D + 120, notes, ha="left", va="bottom", fontsize=7.0,
            color=C_OUT, **FONT, zorder=10,
            bbox=dict(boxstyle="round,pad=0.5", fc="#F4F1E8", ec=C_DIM, lw=0.8))

    ax.text((xS1 + xW2 + BAY_D) / 2, yA + H_PANEL + 140,
            "HDPE SURROUND — FLAT-PATTERN CUT SHEETS  (developed flat; not the assembled bay)",
            ha="center", fontsize=11, fontweight="bold", color=C_OUT, **FONT)

    ax.set_xlim(-260, xW2 + BAY_D + 260)
    ax.set_ylim(yB - 320, yA + H_PANEL + 300)

    title_block(ax, "SHEET 7 OF 17",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="HDPE SURROUND — FLAT-PATTERN CUT SHEETS (6 PIECES)",
                scale_note="DRAWN TO SCALE (isotropic) · SCALE OFF THE 500mm BAR · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.045)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet7.png"), dpi=DIAGRAM_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet7.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 8  —  HDPE Surround: Housing Join + Frame Rivet Details
#   Two enlarged sections (thickness exaggerated for clarity):
#     Detail A — upper/lower floor cap → Ø800 housing wall join (extrusion weld +
#                20mm neoprene surround seal closing the housing↔panel gap, §3.4).
#     Detail B — surround skin/wall → steel frame flange blind-rivet lap.
#   Housing cut geometry single-sourced with light-trap Sheet 2 (LT_HOUSING_T).
# ═══════════════════════════════════════════════════════════════════════════════
def _blind_rivet(ax, cx, cz, ang, grip, d=12):
    """SS blind rivet in section — low-profile factory head at +axis, set (upset) head
    at −axis; `ang` = axis direction (deg), `grip` = joint stack. (Compact local glyph
    matching the light-trap `blind_rivet` profile; see skill_fastener_convention.md.)"""
    RSC = "#C9CCD2"
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))

    def T(u, v):
        return (cx + u * ca - v * sa, cz + u * sa + v * ca)
    g = grip / 2
    ax.add_patch(Polygon([T(-g, -d / 2), T(g, -d / 2), T(g, d / 2), T(-g, d / 2)],
                         closed=True, fc=RSC, ec=C_OUT, lw=1.0, zorder=8))
    HW, HH = d * 1.0, d * 0.35                      # factory head: Ø≈2d, low dome
    head = [T(g, HW)] + [T(g + HH * math.cos(math.pi * (0.5 - k / 12.0)),
                           HW * math.sin(math.pi * (0.5 - k / 12.0))) for k in range(13)] + [T(g, -HW)]
    ax.add_patch(Polygon(head, closed=True, fc=RSC, ec=C_OUT, lw=1.2, zorder=9))
    bb, br = -g - d * 0.22, d * 0.55                # set (blind) head at −axis
    blind = [T(-g, d * 0.6)] + [T(bb - br * math.cos(math.pi * (0.5 - k / 12.0)),
                                  d * 0.9 * math.sin(math.pi * (0.5 - k / 12.0))) for k in range(13)] + [T(-g, -d * 0.6)]
    ax.add_patch(Polygon(blind, closed=True, fc=RSC, ec=C_OUT, lw=1.2, zorder=9))


def _draw_bolt(ax, cx, cz, length, *, d=10, vertical=True, head=-1, end="nut", csk=False, wall=None, zb=10):
    """Bolt/screw in section — the project convention (light-trap draw_bolt): grey shank with a
    wider HEAD at the `head` end and a hex NUT / tapped thread / rivet-nut at the far end.
    cx,cz = shank mid; length = grip along the axis; d = nominal Ø drawn. head=-1 → head at the
    −axis end (below/left); +1 → +axis end. csk=True → flush countersunk head. end: 'nut' |
    'tapped' (no nut) | 'rivnut' (flanged insert spanning `wall`)."""
    SHK, HN = "#8A8F98", C_STEEL
    hh, hw = d * 0.6, d * 1.9
    g = length / 2

    def rect(u0, u1, v0, v1, **kw):
        if vertical:
            ax.add_patch(Rectangle((cx + v0, cz + u0), v1 - v0, u1 - u0, **kw))
        else:
            ax.add_patch(Rectangle((cx + u0, cz + v0), u1 - u0, v1 - v0, **kw))

    def pmap(u, v):
        return (cx + v, cz + u) if vertical else (cx + u, cz + v)
    hu = -g if head < 0 else g
    fu = g if head < 0 else -g
    if csk:
        into = 1 if head < 0 else -1
        cw = hw * 0.85
        tu = hu + into * hh * 1.4
        pts = [pmap(hu, -cw / 2), pmap(hu, cw / 2), pmap(tu, d / 2),
               pmap(fu, d / 2), pmap(fu, -d / 2), pmap(tu, -d / 2)]
        ax.add_patch(Polygon(pts, closed=True, fc=SHK, ec=C_OUT, lw=0.9, zorder=zb))
    else:
        rect(-g, g, -d / 2, d / 2, fc=SHK, ec=C_OUT, lw=0.8, zorder=zb)
        rect(hu - (hh if head < 0 else 0), hu + (0 if head < 0 else hh), -hw / 2, hw / 2,
             fc=HN, ec=C_OUT, lw=0.9, zorder=zb + 1)
    if end == "nut":
        rect(fu - (0 if head < 0 else hh), fu + (hh if head < 0 else 0), -hw / 2, hw / 2,
             fc=HN, ec=C_OUT, lw=0.9, zorder=zb + 1)
    elif end == "rivnut":                              # rivet-nut / blind threaded insert into a hollow wall
        RN = "#A8763A"                                 # bronze — distinct from silver hardware
        into = 1 if head < 0 else -1
        wt = wall if wall is not None else hh
        hp = fu + into * wt                            # inner (bore-side) edge of the wall
        rect(fu, hp, -hw * 0.44, hw * 0.44, fc=RN, ec=C_OUT, lw=0.8, zorder=zb + 1)   # barrel spanning the wall
        rect(fu, hp, -d * 0.48, d * 0.48, fc=SHK, ec="none", zorder=zb + 2)           # bolt threaded up inside
        HWr, HHr = d * 0.95, d * 0.42                                                 # low pancake head on the bore-side edge
        dome = [pmap(hp, HWr)] + [pmap(hp + into * HHr * math.cos(math.pi * (0.5 - kk / 12.0)),
                                       HWr * math.sin(math.pi * (0.5 - kk / 12.0))) for kk in range(13)] + [pmap(hp, -HWr)]
        ax.add_patch(Polygon(dome, closed=True, fc=RN, ec=C_OUT, lw=0.9, zorder=zb + 3))


def sheet8():
    T_SKIN = PANEL_SKIN_T          # 3.18 — 1/8" HDPE surround
    T_HOUS = LT_HOUSING_T          # 5 — housing wall (UV-HDPE)
    RIV_D  = 12                    # rivet glyph body Ø (exaggerated; true 1/8"/Ø3.18)

    fig, ax = plt.subplots(figsize=(17, 9))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(0, 340)
    ax.set_ylim(-40, 205)

    # ═══ DETAIL A — floor cap → Ø800 housing join ═══════════════════════════════
    ax.text(80, 190, "DETAIL A — FLOOR CAP → Ø800 HOUSING JOIN", ha="center",
            fontsize=10, fontweight="bold", color=C_OUT, **FONT)
    ax.text(80, 178, "vertical section · thickness exaggerated", ha="center",
            fontsize=7, color=C_DIM, **FONT)

    # Housing wall (Ø800 UV-HDPE, locally flat/vertical) — rises through the joint
    hx, hw = 96, 16                                 # housing wall at x=96, exaggerated width
    ax.add_patch(Rectangle((hx, 30), hw, 130, fc=C_PLASTIC, ec=C_OUT, lw=1.4, zorder=4))
    leader(ax, (hx + hw, 150), (150, 168),
           f"Ø{int(DRUM_D)} housing wall\n{T_HOUS}mm UV-HDPE (Sheet 2)", col=C_OUT)
    # Floor cap (horizontal 1/8" HDPE) — butts the housing OD, extrusion-welded
    cy, ch = 96, 14
    ax.add_patch(Rectangle((hx - 78, cy), 78, ch, fc=C_PLASTIC, ec=C_OUT, lw=1.4, zorder=4))
    leader(ax, (hx - 60, cy), (36, 60),
           f"floor cap\n{T_SKIN}mm HDPE", col=C_OUT)
    # extrusion-weld fillet at the cap↔housing corner
    ax.add_patch(Polygon([(hx, cy + ch), (hx, cy + ch + 12), (hx - 12, cy + ch)],
                         closed=True, fc="#8A6D3B", ec=C_OUT, lw=0.8, zorder=5))
    ax.add_patch(Polygon([(hx, cy), (hx, cy - 12), (hx - 12, cy)],
                         closed=True, fc="#8A6D3B", ec=C_OUT, lw=0.8, zorder=5))
    leader(ax, (hx - 8, cy + ch + 6), (50, 120), "extrusion-weld fillet\n(HDPE↔HDPE, both faces)", col=C_OUT)
    # 20mm neoprene surround seal closing the housing↔panel radial gap (§3.4)
    ax.add_patch(Rectangle((hx + hw, 44), 26, 18, fc=C_GASKT, ec=C_OUT, lw=1.0, zorder=4))
    leader(ax, (hx + hw + 13, 44), (160, 30),
           "20mm neoprene surround seal\n(closes 15mm housing↔panel gap, §3.4)", col=C_OUT)
    draw_dim_v(ax, hx - 90, cy, cy + ch, f"{T_SKIN}mm", offset=10, fs=6.2, font=FONT)
    draw_dim_h(ax, hx, hx + hw, 24, f"{T_HOUS}mm", offset=8, fs=6.2, font=FONT)

    # ═══ DETAIL B — surround → steel frame blind-rivet lap ══════════════════════
    ax.text(258, 190, "DETAIL B — SURROUND → FRAME RIVET LAP", ha="center",
            fontsize=10, fontweight="bold", color=C_OUT, **FONT)
    ax.text(258, 178, "section · thickness exaggerated", ha="center",
            fontsize=7, color=C_DIM, **FONT)

    # Steel frame flange (2×2×0.120 RHS wall, cut) — horizontal
    fx, fy, fw, ft = 210, 96, 96, 12
    ax.add_patch(Rectangle((fx, fy), fw, ft, fc=C_STEEL, ec=C_OUT, lw=1.4, hatch="///", zorder=4))
    leader(ax, (fx + 20, fy), (206, 52), "steel frame flange\n2×2×0.120in RHS", col=C_OUT)
    # HDPE surround skin lapped OVER the flange
    ax.add_patch(Rectangle((fx + 8, fy + ft), fw - 8, 10, fc=C_PLASTIC, ec=C_OUT, lw=1.4, zorder=5))
    leader(ax, (fx + 30, fy + ft + 5), (220, 160), f"HDPE surround lap\n{T_SKIN}mm 1/8\" skin/wall", col=C_OUT)
    # sealant bead at the lap edge (light-tight)
    ax.add_patch(Polygon([(fx + 8, fy + ft), (fx + 8, fy + ft + 10), (fx - 2, fy + ft)],
                         closed=True, fc="#5A3020", ec=C_OUT, lw=0.7, zorder=6))
    leader(ax, (fx + 6, fy + ft + 8), (200, 150), "DP8010 sealant bead\n(light-tight)", col=C_OUT)
    # blind rivet through the lap (axis vertical, +Z head on the HDPE side). CENTER on the full stack
    # (flange ft + HDPE 10) so the factory head BUTTS the HDPE outer face and the blind head the flange back.
    _blind_rivet(ax, fx + 40, fy + (ft + 10) / 2.0, 90, ft + 10, d=RIV_D)
    leader(ax, (fx + 40, fy + ft + 16), (300, 165),
           f"1/8\" 18-8 SS blind rivet\nMcMaster 97525A435\ndrill Ø{LT_RIVET_HOLE} @ {LT_RIVET_PITCH}mm", col=C_OUT, fw="bold")
    # the post's SIDE face (steel) turns down from the flange — the HDPE wraps this corner
    ax.add_patch(Rectangle((fx + fw - ft, fy - 44), ft, 44 + ft, fc=C_STEEL, ec=C_OUT, lw=1.4, hatch="///", zorder=4))  # post side wall (steel behind the HDPE)
    ax.add_patch(Rectangle((fx + fw, fy - 44), 8, 44 + ft, fc=C_PLASTIC, ec=C_OUT, lw=1.4, zorder=5))                   # HDPE lap down the side face
    # side rivet: axis horizontal, grip = HDPE(8) + steel wall(12) = 20, centered on the stack so the
    # factory head butts the HDPE outer face (x=fx+fw+8) and the set head forms in the tube bore (x=fx+fw-ft)
    _blind_rivet(ax, fx + fw - ft / 2 + 4, fy - 12, 0, 20, d=RIV_D)                                                     # HDPE → into the STEEL side wall, butted
    leader(ax, (fx + fw + 4, fy - 30), (270, 30),
           "HDPE also laps + rivets into the STEEL SIDE face of the post\n(fasten FRONT + SIDE faces — not the front only)", col=C_OUT, fw="bold", fs=6)

    ax.text(170, 4,
            "The HDPE surround (bay walls, floor caps, face skins) laps the steel center-zone frame and is\n"
            "blind-riveted @ {p}mm with a DP8010 sealant bead for light-tightness; the floor caps butt +\n"
            "extrusion-weld to the Ø{d} housing. See SHEET 7 for the flat patterns.".format(
                p=LT_RIVET_PITCH, d=int(DRUM_D)),
            ha="center", va="bottom", fontsize=7.0, color=C_OUT, **FONT,
            bbox=dict(boxstyle="round,pad=0.4", fc="#F4F1E8", ec=C_DIM, lw=0.7))

    title_block(ax, "SHEET 8 OF 17",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="HDPE SURROUND — HOUSING JOIN & FRAME RIVET DETAILS",
                scale_note="ENLARGED SECTIONS · THICKNESS EXAGGERATED · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.045)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet8.png"), dpi=DIAGRAM_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet8.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 9  —  Steel Frame General Arrangement
#   Front elevation of the swinging panel's 2×2×0.120in steel frame: perimeter
#   (stile + pivot-side verticals, top/bottom rails), the two center-zone jambs +
#   drum header/sill, and the drum cage ENVELOPE (shown, detailed in Light-Trap
#   Sheet 7). Detail bubbles route to Sheets 10 (pivot), 11 (plywood/Fan-B), 12
#   (frame hardware). Member schedule keyed to the frame.
# ═══════════════════════════════════════════════════════════════════════════════
def _frame_ga(mirror=False):
    # mirror=True → the EXTERIOR view (looking from outside the cargo door toward the drum): the same
    # frame GA with the X-axis reversed, so left↔right flip while the text stays upright.
    RHS = BRACE_RHS                        # 50.8 — 2×2×0.120in section
    yL, yR = PANEL_CUT_YD, PIVOT_YD         # 180, 2287 — swinging-frame left (stile) + right (pivot) edges
    jL, jR = PANEL_CORNER_YD_L, PANEL_CORNER_YD_R   # 653, 1709 — center-zone jambs
    z_hdr = LT_CAGE_TOP                     # 2217 — header over the drum cage
    z_sill = 130                            # sill under the cage (floor gap)
    from tbs_constants import PANEL_BOTTOM_STEP as STEP   # 65 — corner-zone bottom step-up (Sheet 16)

    fig, ax = plt.subplots(figsize=(16, 15))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(*( (PW + 360, -560) if mirror else (-560, PW + 360) ))   # reversed x → mirror (exterior view)
    ax.set_ylim(-360, PH + 320)

    def vbar(x, z0, z1, label=None, lp=None):        # vertical RHS member
        ax.add_patch(Rectangle((x, z0), RHS, z1 - z0, fc=C_STEEL, ec=C_OUT, lw=1.2, zorder=5))
        ax.add_patch(Rectangle((x + 1.6, z0 + 1.6), RHS - 3.2, z1 - z0 - 3.2, fc="none", ec=C_OUT, lw=0.4, zorder=5))
        if label:
            leader(ax, (x + RHS / 2, lp[0]), lp[1], label, col=C_OUT)

    def hbar(z, x0, x1):                              # horizontal RHS member
        ax.add_patch(Rectangle((x0, z), x1 - x0, RHS, fc=C_STEEL, ec=C_OUT, lw=1.2, zorder=5))
        ax.add_patch(Rectangle((x0 + 1.6, z + 1.6), x1 - x0 - 3.2, RHS - 3.2, fc="none", ec=C_OUT, lw=0.4, zorder=5))

    # ── fixed FAR strip (pivot side) — ghosted context ──
    ax.add_patch(Rectangle((yR, 0), PW - yR, PH, fc="#EEF0F2", ec=C_DIM, lw=0.6, ls=(0, (5, 3)), zorder=1))
    ax.text((yR + PW) / 2, PH / 2, "FIXED far strip\n(bolted to door\nframe — no swing)", ha="center",
            va="center", fontsize=6.6, color=C_DIM, rotation=90, **FONT, zorder=2)

    # ── fixed NEAR opening-edge U-FRAME (welded steel channel, Yd0..180) — the STRUCTURE the hinge panel
    #    BUTTS UP TO. Drawn as a C in this elevation: the web (right, at the Yd180 joint) faces the swing
    #    panel and carries the cam-latch STRIKE PLATES; the top + bottom flanges wrap back and the OPEN side
    #    (Yd0, container-wall side) is WELDED to the container door frame. Secures the HDPE + plywood skins. ──
    uf_z0, uf_z1 = STEP, PH
    WEB, FL = 18, 24
    # container CARGO-DOOR FRAME (50×20×3 RHS) — FULL perimeter. It sits just exterior of the panel plane,
    # so in the INTERIOR view (Sheet 9) it is the FAR structure → ghosted BEHIND; in the EXTERIOR mirror
    # (Sheet 10) it is NEAREST the viewer → drawn solid, IN FRONT of the frame. Bolted M10 @ ~300 to the
    # container; the U-frame welds to its LEFT stile.
    DFW = 30                                                                                   # drawn width (schematic; actual 50mm face)
    # same SOLID fill/opacity on both views (so the cargo frame reads identically); only the DEPTH differs —
    # in front in the exterior mirror (nearest the viewer), behind in the interior view.
    df_z = 8.5 if mirror else 1.5
    df_a, df_ls = 0.9, "-"
    for fx, fy, fw, fh in [(0, 0, DFW, PH), (PW - DFW, 0, DFW, PH),                             # left + right stiles
                           (0, 0, PW, DFW), (0, PH - DFW, PW, DFW)]:                            # threshold + top rail
        ax.add_patch(Rectangle((fx, fy), fw, fh, fc="#5A5E66", ec=C_DIM, lw=0.8, ls=df_ls, alpha=df_a, zorder=df_z))
    for az in range(300, int(PH) - 200, 300):                                                  # M10 anchor heads — the two stiles
        ax.add_patch(Circle((DFW / 2, az), 6, fc="#40444A", ec=C_OUT, lw=0.5, zorder=df_z + 0.2))
        ax.add_patch(Circle((PW - DFW / 2, az), 6, fc="#40444A", ec=C_OUT, lw=0.5, zorder=df_z + 0.2))
    for ay in range(400, int(PW) - 300, 400):                                                  # M10 anchor heads — threshold + top
        ax.add_patch(Circle((ay, DFW / 2), 6, fc="#40444A", ec=C_OUT, lw=0.5, zorder=df_z + 0.2))
        ax.add_patch(Circle((ay, PH - DFW / 2), 6, fc="#40444A", ec=C_OUT, lw=0.5, zorder=df_z + 0.2))
    ax.add_patch(Rectangle((yL - WEB, uf_z0), WEB, uf_z1 - uf_z0, fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=5))   # web (right/swing-facing)
    ax.add_patch(Rectangle((0, uf_z1 - FL), yL, FL, fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=5))                 # top flange → door frame
    ax.add_patch(Rectangle((0, uf_z0), yL, FL, fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=5))                      # bottom flange → door frame
    for wz, dz in ((uf_z0 + FL, 14), (uf_z1 - FL, -14)):                                                     # weld ticks at the door-frame side
        ax.add_patch(Polygon([(0, wz), (11, wz), (0, wz + dz)], closed=True, fc=C_OUT, ec="none", zorder=6))
    for lz in (500, 1900):                                                                                   # cam-latch strike plates on the web
        ax.add_patch(Rectangle((yL - WEB, lz - 45), WEB + 7, 90, fc="#8890A0", ec=C_OUT, lw=1.0, zorder=7))
    leader(ax, (yL - WEB / 2, 1120), (-325, 1130),
           "U-FRAME — welded steel channel\n(Yd0–180); hinge panel BUTTS UP\nhere. Flanges WELD to the container\ncargo-door frame (50×20×3 RHS,\nbolted M10 @ 300) — not load-bearing.", col=C_OUT, fw="bold", fs=6)
    leader(ax, (yL + 4, 500), (-275, 690), "web carries 2 cam-latch\nSTRIKE PLATES\n(engage the panel latches)", col=C_OUT, fs=6)

    # NOTE: the Fan-B plywood band and the drum/cage envelope are intentionally NOT drawn here —
    # this sheet is the STEEL FRAME general arrangement only. The drum + cage are detailed on
    # Light-Trap Sheet 7; the Fan-B ply on Sheet 12. The center zone is left open to read as frame.

    # ── swinging-frame perimeter + internal members ──
    vbar(yL, STEP, PH, "LEFT SWING STILE\n(2×2×0.120in RHS — transport-stay\nhooks weld here, Sheet 13)", (PH * 0.78, (-260, PH * 0.86)))  # bottom stepped up
    vbar(yR - RHS, STEP, PH)                                  # pivot-side vertical (bottom stepped up)
    hbar(PH - RHS, yL, yR)                                    # top rail
    # STEPPED bottom rail: center (jL..jR, drum bay) at Z0 — the corner zones step UP by STEP to clear
    # the bare wall-cantilever bracket legs when the walkway is lifted out for transport (Sheet 16).
    hbar(STEP, yL, jL)                                        # near-corner bottom rail (raised)
    hbar(0, jL, jR)                                           # center bottom rail (lowest — over the tray)
    hbar(STEP, jR, yR)                                        # far-corner bottom rail (raised)
    vbar(jL, 0, PH, "CENTER-ZONE JAMB\n(both sides — surround\nrivets here, Sheet 8)", (1700, (400, 1900)))
    vbar(jR, 0, PH)                                           # far center jamb
    hbar(z_hdr, jL, jR)                                       # drum header
    hbar(z_sill - RHS, jL, jR)                                 # drum sill
    # ── bottom-step callout + dim (both corner zones raised by STEP) ──
    for sxr in (jL, jR + RHS):                                # step risers at the outboard jamb faces
        ax.plot([sxr, sxr], [0, STEP], color="#B00", lw=2.2, zorder=8)
    draw_dim_v(ax, yL - 55, 0, STEP, f"{STEP}mm step", offset=50, fs=6, font=FONT, right=False)
    leader(ax, ((yL + jL) / 2, STEP), ((yL + jL) / 2 + 80, -75),
           f"CORNER BOTTOM STEPPED UP {STEP}mm at BOTH sides\n(clears the bare walkway cantilever legs;\nwalkway removed for transport — Sheet 16)", col="#B00", fw="bold", fs=6)

    # NOTE: the Ø89 CHS pivot post (swing axis) is intentionally NOT drawn on this sheet — it is a
    # distraction from the steel-frame GA. The post assembly + frame→hub bracket are detailed on Sheet 11.

    # ── detail bubbles ──
    def bubble(x, z, n, txt, tp):
        ax.add_patch(Circle((x, z), 46, fc=BG, ec="#B00", lw=1.6, zorder=9))
        ax.text(x, z, f"{n}", ha="center", va="center", fontsize=11, fontweight="bold", color="#B00", **FONT, zorder=10)
        ax.annotate("", xy=(x, z), xytext=tp, arrowprops=dict(arrowstyle="-", color="#B00", lw=0.8), zorder=8)
        ax.text(tp[0], tp[1], txt, ha="center", va="center", fontsize=6.6, color="#B00", **FONT, zorder=10)

    bubble(yR - RHS / 2, 300, 12, "cam latch mount\n(corners, Sheet 13)", (yR - 250, 300))

    # ── member schedule (in the clear near-corner white space) ──
    rows = [
        "MEMBER SCHEDULE",
        "(2×2×0.120in / 50.8mm A500 SHS)",
        " Stile Yd180 ....... 1 × 2,323",
        " Pivot vert Yd2287 . 1 × 2,323",
        " Top rail .......... 1 × 2,107",
        " Btm rails (stepped) 473 + 1,056 + 578",
        " Center jambs ...... 2 × 2,388",
        " Header + sill ..... 2 × 1,056",
    ]
    if not mirror:   # the schedule lives on Sheet 9; the exterior mirror (Sheet 10) omits it (avoids the reversed-axis overflow)
        ax.text(-650, 1560, '\n'.join(rows), ha="left", va="top", fontsize=6.8, color=C_OUT, **FONT,
                bbox=dict(boxstyle="round,pad=0.5", fc="#F4F1E8", ec=C_DIM, lw=0.8), zorder=11)

    draw_dim_h(ax, yL, yR, -150, f"{yR - yL}mm SWINGING FRAME (Yd{yL}–{yR})", offset=20, fs=7, font=FONT)
    # horizontal component chain (near strip · center zone · far strip) — top row, above the cage dim
    draw_dim_h(ax, 0, yL, PH + 135, f"{yL}mm", offset=16, fs=6, font=FONT)
    draw_dim_h(ax, jL, jR, PH + 135, f"{jR - jL}mm center zone", offset=16, fs=6, font=FONT)
    draw_dim_h(ax, yR, PW, PH + 135, f"{int(PW - yR)}mm", offset=16, fs=6, font=FONT)
    draw_dim_h(ax, DRUM_CAGE_YD_L, DRUM_CAGE_YD_R, PH + 45, f"{DRUM_CAGE_YD_R - DRUM_CAGE_YD_L}mm drum cage", offset=16, fs=6, font=FONT)
    # vertical component chain (sill · cage · header→top) on the right, overall PH outermost
    draw_dim_v(ax, PW + 100, 0, z_sill, f"{z_sill}mm", offset=50, fs=6, font=FONT, right=True)
    draw_dim_v(ax, PW + 100, z_sill, z_hdr, f"{z_hdr - z_sill}mm cage", offset=50, fs=6, font=FONT, right=True)
    draw_dim_v(ax, PW + 100, z_hdr, PH, f"{PH - z_hdr}mm", offset=50, fs=6, font=FONT, right=True)
    draw_dim_v(ax, PW + 200, 0, PH, f"{PH}mm", offset=50, fs=7, font=FONT, right=True)

    _view = "EXTERIOR elevation — viewed from OUTSIDE the cargo door toward the drum (mirror of Sheet 9)" if mirror else "swinging panel · front elevation"
    ax.text(PW / 2, PH + 295, f"STEEL FRAME — GENERAL ARRANGEMENT ({_view})",
            ha="center", fontsize=11, fontweight="bold", color=C_OUT, **FONT)

    title_block(ax, "SHEET 10 OF 17" if mirror else "SHEET 9 OF 17",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="STEEL FRAME — GA (EXTERIOR VIEW)" if mirror else "STEEL FRAME — GENERAL ARRANGEMENT + MEMBER SCHEDULE",
                scale_note=("EXTERIOR ELEVATION (mirror of Sheet 9) · SCALE 1:20 · ALL DIMS IN mm" if mirror
                            else "FRONT ELEVATION · SCALE 1:20 · ALL DIMS IN mm"),
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.045)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet10.png" if mirror else "hingepanel-sheet9.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet10.png saved" if mirror else "  diagrams/hingepanel-sheet9.png saved")


# RULE: function names match sheet numbers. Sheet 9 (interior) + Sheet 10 (exterior mirror) share the
# _frame_ga() drawing; every other sheetN() draws Sheet N.
def sheet9():  _frame_ga(mirror=False)   # Sheet 9  — steel frame GA, interior front elevation
def sheet10(): _frame_ga(mirror=True)    # Sheet 10 — steel frame GA, exterior mirror


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 11  —  Pivot-Post Assembly (documents the modeled swing pivot)
#   LEFT: vertical section on the swing axis — fixed Ø89 CHS post floor→roof, floor
#   + roof bolted Ø220 mount plates, 51118 thrust bearing at the base (carries the
#   ~330 kg vertical), 2× iglide journal bushings (react the overturning couple),
#   the MOVING hub tube, and 3 frame→hub hinge brackets. RIGHT: Detail A frame→hub
#   bracket (bolt pattern) + Detail B floor anchor-plate plan.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet11():
    R = PIVOT_POST_OD / 2                   # 44.5 — post radius
    cx = 250                                # post-axis canvas X
    HGT = C_HGT                             # 2388 — floor→roof
    LX = -250                               # left-label column (text center X)

    fig, ax = plt.subplots(figsize=(16, 13))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-720, 1250)
    ax.set_ylim(-300, HGT + 250)

    # ── pivot section (true scale) ────────────────────────────────────────────
    ax.plot([cx, cx], [-40, HGT + 40], color=C_CL, lw=0.8, ls=(0, (8, 4)), zorder=2)   # axis
    # fixed post (Ø89×8 CHS)
    ax.add_patch(Rectangle((cx - R, 0), 2 * R, HGT, fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=4))
    ax.add_patch(Rectangle((cx - R + 8, 0), 2 * R - 16, HGT, fc=BG, ec=C_OUT, lw=0.5, zorder=4))
    leader(ax, (cx - R, 1620), (LX, 1620), "FIXED Ø89×8 CHS POST (S355)\n3\" NPS Sch-80, floor→roof —\ncarries the 3.6 kN·m swing\ncantilever (SF 3.7)", col=C_OUT, fw="bold")
    # floor + roof mount plates (Ø220 × 20)
    ax.add_patch(Rectangle((cx - 110, 0), 220, 20, fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=5))
    ax.add_patch(Rectangle((cx - 110, HGT - 20), 220, 20, fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=5))
    leader(ax, (cx - 100, 10), (LX, 180), "FLOOR MOUNT PLATE Ø220×20\n— bolted to the container floor\n(Detail B)", col=C_OUT)
    leader(ax, (cx - 100, HGT - 10), (LX, HGT - 120), "ROOF MOUNT PLATE Ø220×20\n— bolted to the roof rail", col=C_OUT)
    # thrust bearing 51118 + collar
    ax.add_patch(Rectangle((cx - 60, 130), 120, 22, fc="#5A5AA0", ec=C_OUT, lw=1.1, zorder=6))
    ax.add_patch(Rectangle((cx - 75, 152), 150, 25, fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=6))
    leader(ax, (cx - 60, 141), (LX, 500), "51118 THRUST BEARING (Ø90×120×22)\ncarries ~330 kg vertical\n— single-direction", col=C_OUT)
    # moving hub tube (Ø116)
    for sgn in (-1, 1):
        ax.add_patch(Rectangle((cx + sgn * R, 180), sgn * 14, 2050 - 180, fc=C_ALUM, ec=C_OUT, lw=1.1, zorder=3))
    leader(ax, (cx - R - 14, 1150), (LX, 1150), "MOVING HUB TUBE (Ø116)\nswings with the frame", col=C_OUT)
    # iglide journal bushings (radial) — react the overturning couple
    for z in (220, 2000):
        for sgn in (-1, 1):
            ax.add_patch(Rectangle((cx + sgn * R, z), sgn * 14, 60, fc="#C08040", ec=C_OUT, lw=1.0, zorder=6))
    leader(ax, (cx - R - 14, 2030), (LX, 2020), "iglide J journal bushing (×2,\ntop + bottom) JFM-9095-100\n— radial + overturning couple", col=C_OUT)
    # 3 frame→hub hinge brackets (on the +X side, toward the frame)
    for z in (300, 1180, 2000):
        ax.add_patch(Rectangle((cx + R + 14, z - 20), 150, 70, fc=C_STEEL, ec=C_OUT, lw=1.1, zorder=6))
    leader(ax, (cx + R + 164, 1160), (cx + 630, 1000), "3× HINGE BRACKET\n(hub → leaf pivot-edge stile)\n— Sheet 15", col=C_OUT, fw="bold")
    draw_dim_v(ax, cx - 180, 0, HGT, f"{HGT}mm floor→roof", offset=16, fs=6.6, font=FONT)
    # diameters (dim_h) + component lengths (dim_v) on the pivot post
    draw_dim_h(ax, cx - R, cx + R, HGT + 60, f"Ø{PIVOT_POST_OD:.0f} CHS post", offset=14, fs=6.4, font=FONT)
    draw_dim_h(ax, cx - R - 14, cx + R + 14, 1000, "Ø116mm hub tube", offset=14, fs=6.2, font=FONT)  # Ø220 plate OD is dimensioned in Detail B
    draw_dim_v(ax, cx + 300, 180, 2050, f"{2050 - 180}mm hub tube", offset=16, fs=6.2, font=FONT, right=True)
    draw_dim_v(ax, cx + 240, 220, 2000, f"{2000 - 220}mm bushing ctrs", offset=16, fs=6.0, font=FONT, right=True)

    # ── RIGHT: frame→hub bracket is detailed on its own sheet ─────────────────
    ax.text(1000, 1900, "FRAME → HUB BRACKET", ha="center", fontsize=9.5, fontweight="bold", color=C_OUT, **FONT)
    ax.text(1000, 2200, "3 hinge brackets FILLET-WELDED to both the hub\ntube and the leaf's pivot-edge stile\n(hub + leaf + cage = one weldment).\nDrawn full-size on SHEET 15\n(Frame → Pivot-Post Connection).",
            ha="center", va="top", fontsize=6.6, color=C_OUT, **FONT,
            bbox=dict(boxstyle="round,pad=0.6", fc="#F4F1E8", ec=C_DIM, lw=0.9))

    # ── RIGHT DETAIL B: floor anchor-plate plan (enlarged) ────────────────────
    bx0, by0, sB = 890, 470, 1.9
    ax.text(bx0, by0 + 165 * sB, "DETAIL B — FLOOR ANCHOR PLATE (plan)", ha="center", fontsize=8.5, fontweight="bold", color=C_OUT, **FONT)
    ax.add_patch(Circle((bx0, by0), 110 * sB, fc=C_STEEL, ec=C_OUT, lw=1.4, zorder=5))
    ax.add_patch(Circle((bx0, by0), R * sB, fc=BG, ec=C_OUT, lw=1.0, zorder=6))    # post bore
    for k in range(6):
        a = math.radians(30 + k * 60)
        ax.add_patch(Circle((bx0 + 85 * sB * math.cos(a), by0 + 85 * sB * math.sin(a)), 7 * sB, fc=BG, ec=C_OUT, lw=1.0, zorder=6))
    # dimensions: plate OD, bolt PCD, post bore, hole size
    draw_dim_h(ax, bx0 - 110 * sB, bx0 + 110 * sB, by0 + 120 * sB, "Ø220mm plate OD", offset=12, fs=6.2, font=FONT)
    draw_dim_h(ax, bx0 - 85 * sB, bx0 + 85 * sB, by0 - 120 * sB, "Ø170mm bolt PCD", offset=12, fs=6.2, font=FONT, above=False)
    leader(ax, (bx0 + R * sB, by0), (bx0 + 165 * sB, by0 + 40 * sB), "Ø90 post bore", col=C_OUT, fs=6)
    leader(ax, (bx0 + 85 * sB * math.cos(math.radians(30)), by0 + 85 * sB * math.sin(math.radians(30))),
           (bx0 + 150 * sB, by0 + 85 * sB), "6× Ø14 (M12)", col=C_OUT, fs=6)
    ax.text(bx0, by0 - 170 * sB, "Ø220×20 A36 plate · into the container floor cross-member",
            ha="center", fontsize=6.4, color=C_OUT, **FONT)

    ax.text(280, HGT + 150, "PIVOT-POST ASSEMBLY — SECTION ON THE SWING AXIS",
            ha="center", fontsize=11, fontweight="bold", color=C_OUT, **FONT)

    title_block(ax, "SHEET 11 OF 17",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="PIVOT-POST ASSEMBLY — SECTION + ANCHOR PLATE (frame→hub: Sheet 15)",
                scale_note="SECTION 1:20 · DETAILS ENLARGED · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.045)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet11.png"), dpi=DIAGRAM_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet11.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 12  —  Fan-B Plywood: Cut Sheet + Attachments
#   LEFT: the 4'×8' PT-ply cut sheet — the Fan-B mount band + the cooler stow base
#   nested, with the Ø150 fan cutout, fan bolt holes, and the frame-tab T-nut edge
#   pattern. RIGHT: Detail A Fan-B→ply through-bolt; Detail B ply→frame welded tab
#   + captive tee-nut (the IBC-frame convention).
# ═══════════════════════════════════════════════════════════════════════════════
def sheet12():
    SW, SH = 1220, 2440                     # 4'×8' PT-ply sheet
    BW, BH = 610, 1220                      # Fan-B mount band
    CW, CH = 600, 350                       # cooler stow base plate
    PLY = 18
    FR = FAN_DIAM / 2                       # 75 — Ø150 fan cutout

    fig, ax = plt.subplots(figsize=(17, 12.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-520, SW + 520)
    ax.set_ylim(-320, SH + 230)

    # ── 4'×8' ply cut sheet (full sheet) ──────────────────────────────────────
    ax.add_patch(Rectangle((0, 0), SW, SH, fc="#EFE6D2", ec=C_OUT, lw=1.4, zorder=3))
    ax.text(SW / 2, SH + 90, "PLYWOOD CUT SHEET — 4'×8' ¾\" PT PINE (1220×2440)",
            ha="center", fontsize=9.5, fontweight="bold", color=C_OUT, **FONT)
    # Fan-B band (top) — cut piece
    bx, by = 0, SH - BH
    ax.add_patch(Rectangle((bx, by), BW, BH, fc=C_WOOD, ec=C_OUT, lw=1.3, alpha=0.55, zorder=4))
    ax.text(bx + BW / 2, by + BH - 90, "FAN-B MOUNT BAND\n610 × 1,220 · 18mm", ha="center", va="top",
            fontsize=7.5, fontweight="bold", color="#6b4a1f", **FONT, zorder=6)
    # Ø150 fan cutout + 4 bolt holes
    fcx, fcy = bx + BW / 2, by + 360
    ax.add_patch(Circle((fcx, fcy), FR, fc=BG, ec=C_OUT, lw=1.2, zorder=6))
    ax.text(fcx, fcy, f"Ø{int(FAN_DIAM)}\nfan\ncutout", ha="center", va="center", fontsize=6.4, color=C_DIM, **FONT, zorder=7)
    for k in range(4):
        a = math.radians(45 + k * 90)
        ax.add_patch(Circle((fcx + (FR + 24) * math.cos(a), fcy + (FR + 24) * math.sin(a)), 5, fc=BG, ec=C_OUT, lw=0.9, zorder=7))
    ax.text(fcx, fcy - FR - 55, "4× fan-flange bolts", ha="center", fontsize=6.2, color=C_DIM, **FONT, zorder=7)
    # frame-tab T-nut holes along the two vertical edges (to the jamb + stile)
    for ex in (bx + 30, bx + BW - 30):
        for zz in [by + 120 + i * 320 for i in range(4)]:
            ax.add_patch(Circle((ex, zz), 6, fc="#A8763A", ec=C_OUT, lw=0.8, zorder=7))
    ax.text(bx + BW + 150, by + BH / 2, "frame-tab T-nut holes\n(both edges, @ ~320mm)\n— see Sheet 14", ha="left", va="center", fontsize=6.2, color="#8a5a1f", **FONT, zorder=7)
    # cooler base (below the band)
    cx0, cy0 = 0, by - 60 - CH
    ax.add_patch(Rectangle((cx0, cy0), CW, CH, fc=C_WOOD, ec=C_OUT, lw=1.2, alpha=0.4, zorder=4))
    ax.text(cx0 + CW / 2, cy0 + CH / 2, "COOLER STOW\nBASE 600×350", ha="center", va="center", fontsize=6.8, color="#6b4a1f", **FONT, zorder=6)
    ax.text(SW / 2, cy0 / 2, "remainder — offcut stock", ha="center", va="center", fontsize=6.4, color=C_DIM, **FONT, zorder=5)
    draw_dim_h(ax, 0, SW, -110, f"{SW}mm", offset=16, fs=6.6, font=FONT)
    draw_dim_v(ax, -110, 0, SH, f"{SH}mm", offset=16, fs=6.6, font=FONT)
    # per-piece + fan-cutout position dimensions
    draw_dim_h(ax, bx, bx + BW, by + BH + 34, f"{BW}mm", offset=12, fs=6.0, font=FONT)               # band width
    draw_dim_v(ax, bx + BW + 60, by, by + BH, f"{BH}mm", offset=12, fs=6.0, font=FONT, right=True)     # band height
    draw_dim_v(ax, bx + BW - 100, by, fcy, "360mm to fan CL", offset=12, fs=5.8, font=FONT, right=True)  # fan vert position
    draw_dim_h(ax, bx, fcx, fcy + FR + 55, f"{int(BW / 2)}mm (fan CL, centered)", offset=10, fs=5.8, font=FONT)  # fan horiz position (above cutout)
    draw_dim_h(ax, cx0, cx0 + CW, cy0 - 34, f"{CW}mm", offset=12, fs=6.0, font=FONT, above=False)      # cooler base width
    draw_dim_v(ax, cx0 + CW + 60, cy0, cy0 + CH, f"{CH}mm", offset=12, fs=6.0, font=FONT, right=True)   # cooler base height

    draw_notes(ax, [
        "CROSS-REFERENCES",
        "• plywood → frame tab / captive T-nut detail — SHEET 14",
        "• Fan-B mount — Ventilation Sheet 3",
    ], SW / 2 - 470, cy0 - 120, spacing=48, fs=6.5, title_fs=7.0,
       color=C_OUT, title_color=C_OUT, width=950, border_color=C_DIM, font=FONT)

    title_block(ax, "SHEET 12 OF 17",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="FAN-B PLYWOOD — CUT SHEET (ply→frame on Sheet 14; Fan-B mount on Ventilation Sheet 3)",
                scale_note="CUT SHEET · DRAWN TO SCALE · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.045)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet12.png"), dpi=DIAGRAM_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet12.png saved")

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 13  —  Frame Hardware Attachments (three details)
#   A — Southco C2-33 cam latch: through-bolt + backing plate to the frame.
#   B — transport-stay hook: welded to the left perimeter RHS stile (§5.2).
#   C — top/bottom brush strip: McMaster 74405T12 brush in an 8813T53 Al holder,
#       screwed to the FIXED door frame.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet13():
    fig, ax = plt.subplots(figsize=(19, 8.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(0, 540)
    ax.set_ylim(-70, 220)

    # ═══ DETAIL A — 1619A74 lift-and-turn cam latch (SIDE SECTION through the latch axis) ══════
    #   The shaft runs HORIZONTALLY through the panel stile, so the L-shaped LIFT-AND-TURN handle shows in
    #   profile on the interior face; the cam behind hooks the strike welded to the adjacent (fixed) jamb.
    #   EXTERIOR at LEFT (cam + jamb) → INTERIOR at RIGHT (handle).
    Ax = 6
    ax.text(Ax + 92, 206, "DETAIL A — LIFT-AND-TURN CAM LATCH (McMaster 1619A74)", ha="center", fontsize=8.3, fontweight="bold", color=C_OUT, **FONT)
    ax.text(Ax + 92, 194, "side section · the two stiles are STACKED (short ends aligned); the latch crosses both", ha="center", fontsize=6.0, color=C_DIM, **FONT)
    # Two stiles STACKED vertically (short ends aligned): FIXED jamb (lower) + SWINGING panel (upper).
    ax.add_patch(Rectangle((Ax + 26, 24), 92, 42, fc=C_STEEL, ec=C_OUT, lw=1.4, hatch="///", zorder=4))    # FIXED jamb stile (LOWER)
    ax.add_patch(Rectangle((Ax + 29, 27), 86, 36, fc=BG, ec=C_OUT, lw=0.5, zorder=4))
    ax.add_patch(Rectangle((Ax + 26, 74), 92, 42, fc=C_STEEL, ec=C_OUT, lw=1.4, hatch="\\\\", zorder=4))   # SWINGING panel stile (UPPER)
    ax.add_patch(Rectangle((Ax + 29, 77), 86, 36, fc=BG, ec=C_OUT, lw=0.5, zorder=4))
    ax.add_patch(Rectangle((Ax + 26, 66), 92, 8, fc=C_GASKT, ec=C_OUT, lw=0.8, zorder=5))                  # 20mm EPDM between (compressed)
    leader(ax, (Ax + 72, 40), (Ax + 40, 4), "FIXED jamb stile (lower)\n(welded to the stub wall)", col=C_OUT, fs=6)
    leader(ax, (Ax + 78, 104), (Ax + 92, 132), "SWINGING panel stile (upper)\n(2\u00d72\u00d70.120 RHS)", col=C_OUT, fs=6)
    leader(ax, (Ax + 100, 70), (Ax + 150, 44), "20mm EPDM\n(cam draws it tight)", col=C_OUT, fs=6)
    # clamp SHAFT \u2014 horizontal, through the UPPER stile and extended LEFT past the stiles to carry the cam
    ax.add_patch(Rectangle((Ax + 4, 90), 120, 8, fc="#8A8F98", ec=C_OUT, lw=1.0, zorder=7))
    # cam arm drops from the shaft's left end; the catch hooks the STRIKE on the lower stile's VERTICAL short-end face
    ax.add_patch(Rectangle((Ax + 8, 48), 8, 46, fc="#7A6A9A", ec=C_OUT, lw=1.1, zorder=8))                 # cam arm (down)
    ax.add_patch(Rectangle((Ax + 8, 48), 16, 8, fc="#7A6A9A", ec=C_OUT, lw=1.0, zorder=8))                 # catch hooking the strike
    ax.add_patch(Rectangle((Ax + 20, 30), 6, 30, fc=C_STEEL, ec=C_OUT, lw=1.2, zorder=6))                  # STRIKE plate on the vertical short-end face
    ax.add_patch(Polygon([(Ax + 26, 34), (Ax + 26, 42), (Ax + 32, 38)], closed=True, fc=C_OUT, ec="none", zorder=7))  # weld to the vertical face
    leader(ax, (Ax + 18, 50), (Ax + 18, 150), "catch hooks the STRIKE PLATE\n(welded to the lower stile's\nvertical short-end face) \u2014\ndraws the two tight", col=C_OUT, fw="bold", fs=6)
    # escutcheon on the interior face of the UPPER stile
    ax.add_patch(Rectangle((Ax + 118, 80), 12, 28, fc="#8A8F98", ec=C_OUT, lw=1.1, zorder=7))
    # L-SHAPED lift-and-turn HANDLE \u2014 arm out (right) + grip bent UP 90\u00b0
    ax.add_patch(Rectangle((Ax + 130, 90), 40, 8, fc="#6E5E90", ec=C_OUT, lw=1.1, zorder=9))               # handle arm
    ax.add_patch(Rectangle((Ax + 162, 90), 8, 46, fc="#6E5E90", ec=C_OUT, lw=1.1, zorder=9))               # grip bent UP
    ax.annotate("", xy=(Ax + 166, 150), xytext=(Ax + 166, 138), arrowprops=dict(arrowstyle="-|>", color=C_OUT, lw=1.6), zorder=10)  # LIFT
    ax.annotate("", xy=(Ax + 154, 82), xytext=(Ax + 174, 82), arrowprops=dict(arrowstyle="-|>", color=C_OUT, lw=1.3, connectionstyle="arc3,rad=0.4"), zorder=10)  # TURN
    leader(ax, (Ax + 150, 92), (Ax + 150, 165), "LIFT-AND-TURN HANDLE (interior face,\negress) \u2014 L-arm bends up 90\u00b0; lift + turn\nto engage/release the cam", col=C_OUT, fw="bold", fs=6)

    # ═══ DETAIL B — transport-stay hook (welded to the stile) ════════════════
    Bx = 210
    ax.text(Bx + 80, 205, "DETAIL B — TRANSPORT-STAY HOOK", ha="center", fontsize=9, fontweight="bold", color=C_OUT, **FONT)
    ax.text(Bx + 80, 192, "welded to the left perimeter RHS stile (§5.2)", ha="center", fontsize=6.6, color=C_DIM, **FONT)
    ax.add_patch(Rectangle((Bx + 20, 40), 50, 50, fc=C_STEEL, ec=C_OUT, lw=1.4, hatch="///", zorder=4))
    ax.add_patch(Rectangle((Bx + 23, 43), 44, 44, fc=BG, ec=C_OUT, lw=0.5, zorder=4))
    leader(ax, (Bx + 45, 40), (Bx + 25, 8), "left swing stile\n(2×2×0.120 RHS)", col=C_OUT, fs=6)
    # welded eye plate + hook + turnbuckle to wall eye
    ax.add_patch(Rectangle((Bx + 70, 58), 22, 14, fc=C_STEEL, ec=C_OUT, lw=1.2, zorder=5))         # eye plate
    ax.add_patch(Polygon([(Bx + 70, 72), (Bx + 78, 78), (Bx + 70, 78)], closed=True, fc=C_OUT, ec="none", zorder=6))  # weld
    ax.add_patch(Circle((Bx + 88, 65), 7, fc=BG, ec=C_OUT, lw=1.3, zorder=6))                       # eye
    ax.plot([Bx + 95, Bx + 150], [65, 65], color="#101010", lw=2.0, zorder=6)                       # turnbuckle rod
    ax.add_patch(Rectangle((Bx + 118, 60), 16, 10, fc="#9AA0A6", ec=C_OUT, lw=1.0, zorder=7))        # turnbuckle body
    ax.add_patch(Circle((Bx + 156, 65), 7, fc=BG, ec=C_OUT, lw=1.3, zorder=6))                       # wall eye
    ax.add_patch(Rectangle((Bx + 160, 45), 8, 40, fc=C_STEEL, ec=C_OUT, lw=1.2, hatch="\\\\", zorder=5))  # wall
    leader(ax, (Bx + 88, 65), (Bx + 70, 120), "eye plate WELDED\nto the stile", col=C_OUT, fs=6)
    leader(ax, (Bx + 126, 65), (Bx + 150, 120), "M16 turnbuckle →\nwall eye (near wall)", col=C_DIM, fs=6)
    ax.text(Bx + 100, 24, "load reacts into steel, not the HDPE skin;\nengaged after the swing, released before swing-back", ha="center", va="top", fontsize=6.3, color=C_OUT, **FONT)

    # ═══ DETAIL C — brush strip in Al holder (door frame) ════════════════════
    Cx = 400
    ax.text(Cx + 70, 205, "DETAIL C — TOP/BOTTOM BRUSH STRIP", ha="center", fontsize=9, fontweight="bold", color=C_OUT, **FONT)
    ax.text(Cx + 70, 192, "74405T12 brush in 8813T53 Al holder → door frame", ha="center", fontsize=6.6, color=C_DIM, **FONT)
    ax.add_patch(Rectangle((Cx + 30, 100), 80, 40, fc=C_STEEL, ec=C_OUT, lw=1.4, hatch="///", zorder=4))   # fixed door frame RHS (outer)
    ax.add_patch(Rectangle((Cx + 33, 103), 74, 34, fc=BG, ec=C_OUT, lw=0.6, zorder=4))                     # hollow bore
    leader(ax, (Cx + 70, 140), (Cx + 60, 155), "FIXED door frame\n(50×50 RHS — hollow)", col=C_OUT, fs=6)
    # Al holder channel (U) screwed under the frame
    ax.add_patch(Rectangle((Cx + 48, 78), 44, 22, fc=C_ALUM, ec=C_OUT, lw=1.3, zorder=5))
    ax.add_patch(Rectangle((Cx + 52, 82), 36, 14, fc=BG, ec=C_OUT, lw=0.6, zorder=5))
    leader(ax, (Cx + 88, 89), (Cx + 120, 85), "8813T53 Al\nholder channel", col=C_OUT, fs=6)
    # #10 screw head bears on the EXPOSED (bottom) FACE of the Al holder (z=78); shank runs UP
    # through the holder into a RIVNUT set in the hollow frame's bottom wall (z 100–103).
    _draw_bolt(ax, Cx + 70, 89, 22, d=5, vertical=True, head=-1, end="rivnut", wall=3, zb=9)
    ax.plot([Cx + 63, Cx + 77], [78, 78], color=C_OUT, lw=1.0, zorder=10)                       # holder face line the head bears on
    leader(ax, (Cx + 70, 75), (Cx + 55, 30), "#10 screw HEAD on the holder FACE;\nshank up into a RIVNUT in the hollow\nframe wall (can't tap the 3mm tube)", col=C_OUT, fs=6)
    # brush bristles hanging down (clear column left for the mounting screw)
    for bxk in range(Cx + 54, Cx + 88, 4):
        if Cx + 62 <= bxk <= Cx + 78:
            continue
        ax.plot([bxk, bxk], [82, 50], color="#3A3A3A", lw=0.8, zorder=6)
    leader(ax, (Cx + 70, 60), (Cx + 118, 60), "74405T12 nylon\nstrip brush\n(panel sweeps through)", col=C_OUT, fs=6)

    title_block(ax, "SHEET 13 OF 17",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="FRAME HARDWARE — CAM LATCH · TRANSPORT STAY · BRUSH STRIP",
                scale_note="ENLARGED DETAILS · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.045)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet13.png"), dpi=DIAGRAM_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet13.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 14  —  Plywood → Frame attachment (enlarged): welded tab + captive tee-nut
# ═══════════════════════════════════════════════════════════════════════════════
def sheet14():
    fig, ax = plt.subplots(figsize=(12, 10.8))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(0, 250)
    ax.set_ylim(-95, 250)     # extra bottom room so the rotated-90° companion clears the title block

    # ── DETAIL B — plywood → frame (welded tab + captive tee-nut) ──
    bx0, byy, sB = 60, 40, 1.0
    def dB(x, y): return (bx0 + x * sB, byy + y * sB)
    ax.text(bx0 + 90, 200, "PLYWOOD → FRAME ATTACHMENT", ha="center", fontsize=10, fontweight="bold", color=C_OUT, **FONT)
    ax.text(bx0 + 90, 188, "welded steel tab + pronged captive tee-nut (IBC convention)", ha="center", fontsize=7, color=C_DIM, **FONT)
    ax.text(bx0 + 65, 180, "PLAN SECTION (horizontal cut)", ha="center", fontsize=6.6, color=C_DIM, **FONT)
    # frame RHS (vertical stile, cut) · welded L-tab · ply edge-on · bolt through the tab UPSTAND
    ax.add_patch(Rectangle(dB(0, 48), 48, 88, fc=C_STEEL, ec=C_OUT, lw=1.4, hatch="///", zorder=5))     # frame RHS
    ax.add_patch(Rectangle(dB(3, 51), 42, 82, fc=BG, ec=C_OUT, lw=0.5, zorder=5))                        # RHS bore
    ax.add_patch(Rectangle(dB(48, 66), 40, 7, fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=6))                   # L-tab base leg (welded to the frame) — LOW, clear of the bolt
    ax.add_patch(Polygon([dB(48, 73), dB(48, 66), dB(56, 66)], closed=True, fc=C_OUT, ec="none", zorder=7))  # weld fillet
    ax.add_patch(Rectangle(dB(84, 60), 7, 58, fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=6))                   # L-tab upstand (parallel to the ply)
    ax.add_patch(Rectangle(dB(91, 56), 18, 66, fc=C_WOOD, ec=C_OUT, lw=1.3, zorder=5))                    # 18mm ply (edge-on)
    # bolt — standard section convention (_draw_bolt): hex head bearing on the tab-upstand face, shank
    # through the upstand + into the captive TEE-NUT in the ply. Placed HIGH on the tab, well clear of
    # the weld base leg, so it cannot read as passing through the frame.
    _draw_bolt(ax, dB(95, 102)[0], dB(95, 102)[1], 22 * sB, d=6, vertical=False, head=-1, end="tapped", zb=9)
    ax.add_patch(Rectangle(dB(91, 99), 15, 6, fc="#A8763A", ec=C_OUT, lw=0.8, zorder=8))                 # tee-nut barrel (in the ply)
    ax.add_patch(Rectangle(dB(106, 96), 3, 12, fc="#A8763A", ec=C_OUT, lw=0.8, zorder=8))                # tee-nut flange on the ply FAR face
    leader(ax, dB(24, 48), (bx0 - 24, 65), "frame RHS member\n(no bolt enters it)", col=C_OUT, fs=6.2)
    leader(ax, dB(66, 71), (bx0 + 55, 65), "L-tab base leg\nWELDED to the frame", col=C_OUT, fs=6.2)
    leader(ax, dB(97, 102), (bx0 + 150, 126), "M8 bolt → the tab\nUPSTAND (hex head on its face)", col=C_OUT, fw="bold", fs=6.2)
    leader(ax, dB(108, 102), (bx0 + 150, 158), "captive TEE-NUT in the ply\n(flange on the far/back face)", col=C_OUT, fw="bold", fs=6.2)
    # dims (to scale)
    draw_dim_h(ax, dB(91, 0)[0], dB(109, 0)[0], dB(0, 50)[1], "18mm", offset=-7, above=False, fs=5.6, font=FONT)
    draw_dim_h(ax, dB(0, 0)[0], dB(48, 0)[0], dB(0, 40)[1], "50mm RHS", offset=-7, above=False, fs=5.6, font=FONT)

    # ── COMPANION: rotated 90° view (looking along the bolt axis) — the bolt seats in the tab plate;
    #    the frame stile is off to the side, so the bolt does NOT pass through the frame. ──
    def hexpts(cx0, cy0, r):
        return [(cx0 + r * math.cos(math.radians(60 * k + 30)), cy0 + r * math.sin(math.radians(60 * k + 30))) for k in range(6)]
    vby = -52
    def vB(x, y): return (bx0 + x, vby + y)
    ax.text(bx0 + 45, vby + 54, "ROTATED 90° — bolt seats in the TAB, not the frame", ha="center", fontsize=7.5, fontweight="bold", color=C_OUT, **FONT)
    ax.text(bx0 + 45, vby + 45, "(view along the bolt axis)", ha="center", fontsize=6.2, color=C_DIM, **FONT)
    ax.add_patch(Rectangle(vB(66, 2), 20, 38, fc=C_WOOD, ec=C_OUT, lw=1.0, ls=(0, (4, 2)), zorder=3))     # ply behind (dashed)
    ax.add_patch(Rectangle(vB(0, 0), 12, 42, fc=C_STEEL, ec=C_OUT, lw=1.3, hatch="///", zorder=4))         # frame stile (edge-on)
    ax.add_patch(Rectangle(vB(12, 16), 9, 10, fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=4))                     # welded base leg (edge)
    ax.add_patch(Polygon([vB(12, 26), vB(12, 16), vB(18, 16)], closed=True, fc=C_OUT, ec="none", zorder=5))  # weld
    ax.add_patch(Rectangle(vB(21, 4), 44, 34, fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=5))                      # tab upstand plate (face-on)
    hx, hy = vB(44, 21)
    ax.add_patch(Polygon(hexpts(hx, hy, 7), closed=True, fc="#8A8F98", ec=C_OUT, lw=1.1, zorder=7))         # bolt hex head on the tab face
    ax.add_patch(Circle((hx, hy), 2.2, fc="#606568", ec="none", zorder=8))
    leader(ax, (hx, hy), vB(110, 34), "M8 bolt seats in\nthe tab plate", col=C_OUT, fw="bold", fs=6.0)
    leader(ax, vB(6, 38), vB(-20, 46), "frame stile\n(to the side)", col=C_OUT, fs=6.0)
    leader(ax, vB(78, 8), vB(96, 6), "18mm ply\n(behind)", col=C_OUT, fs=6.0)

    title_block(ax, "SHEET 14 OF 17",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="PLYWOOD → FRAME ATTACHMENT — WELDED TAB + CAPTIVE TEE-NUT",
                scale_note="SECTIONS TO SCALE (≈1:1) · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.045)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet14.png"), dpi=DIAGRAM_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet14.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 15  —  Frame → Pivot-Post Connection (how the swinging frame is secured
#   to the moving hub that rides the fixed Ø89 post). LEFT: elevation of the hub +
#   3 welded hinge brackets. RIGHT: enlarged plan section of one bracket — the plate
#   is fillet-welded to BOTH the hub tube and the frame jamb (all-welded weldment;
#   no bolts through the closed jamb, which can't be back-tightened).
# ═══════════════════════════════════════════════════════════════════════════════
def sheet15():
    HGT = C_HGT
    fig, ax = plt.subplots(figsize=(16, 16))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-300, 1470)
    ax.set_ylim(-320, HGT + 220)

    # ── LEFT: elevation — hub tube + 3 hinge brackets welded on, tying to the jamb
    cx = 120
    ax.plot([cx, cx], [-30, HGT + 30], color=C_CL, lw=0.8, ls=(0, (8, 4)), zorder=2)
    ax.add_patch(Rectangle((cx - 58, 40), 116, HGT - 80, fc=C_ALUM, ec=C_OUT, lw=1.2, alpha=0.5, zorder=4))       # hub tube (full height for simplicity)
    ax.add_patch(Rectangle((cx - 58 + 12, 40), 116 - 24, HGT - 80, fc=BG, ec=C_OUT, lw=0.4, zorder=4))            # bore (post)
    ax.add_patch(Rectangle((cx + 58 + 120, 0), 30, HGT, fc=C_STEEL, ec=C_OUT, lw=1.1, alpha=0.85, zorder=3))       # leaf pivot-edge stile
    for z in (300, 1180, 2000):
        ax.add_patch(Rectangle((cx + 58, z - 22), 120, 66, fc=C_STEEL, ec=C_OUT, lw=1.1, zorder=5))               # hinge bracket (welded hub↔leaf stile)
        for jz in (z - 20, z + 42):                                                                               # weld ticks at the stile
            ax.add_patch(Polygon([(cx + 178, jz), (cx + 170, jz), (cx + 178, jz + (6 if jz < z else -6))], closed=True, fc=C_OUT, ec="none", zorder=7))
    leader(ax, (cx, 1400), (cx - 275, 1500), "MOVING HUB TUBE (Ø116)\nrides the fixed Ø89 post\n(Sheet 11)", col=C_OUT, fs=6.5)
    leader(ax, (cx + 118, 300), (cx - 250, 500), "3× HINGE BRACKET\nwelded to hub + stile", col=C_OUT, fw="bold", fs=6.5)
    leader(ax, (cx + 178, 2000), (cx + 550, 2200), "LEAF PIVOT-EDGE STILE\n(2×2 RHS — TRAVELS with\nthe leaf, carries its plywood)", col=C_OUT, fw="bold", fs=6.5)
    ax.text(cx + 40, HGT + 130, "ELEVATION — 3 brackets up the hub", ha="center", fontsize=8.5, fontweight="bold", color=C_OUT, **FONT)

    # ── RIGHT: enlarged plan section of one bracket ──
    ox, oy, s = 660, 900, 4.2
    def d(x, y): return (ox + x * s, oy + y * s)
    ax.text(ox + 55 * s, oy + 95 * s, "DETAIL — HINGE BRACKET (plan section)", ha="center", fontsize=9, fontweight="bold", color=C_OUT, **FONT)
    ax.add_patch(Rectangle(d(-14, -40), 14 * s, 80 * s, fc=C_ALUM, ec=C_OUT, lw=1.3, zorder=5))       # hub tube wall
    ax.add_patch(Rectangle(d(0, -22), 66 * s, 44 * s, fc=C_STEEL, ec=C_OUT, lw=1.4, zorder=6))         # bracket plate (welded to hub)
    ax.add_patch(Rectangle(d(66, -42), 50 * s, 84 * s, fc=C_STEEL, ec=C_OUT, lw=1.4, hatch="///", zorder=5))  # leaf pivot-edge stile
    ax.add_patch(Rectangle(d(69, -39), 44 * s, 78 * s, fc=BG, ec=C_OUT, lw=0.5, zorder=5))             # stile bore
    for wy, sgn in ((-22, 1), (22, -1)):                                                               # fillet welds bracket→hub, AT the tube surface
        ax.add_patch(Polygon([d(0, wy), d(0, wy + sgn * 9), d(11, wy)], closed=True, fc=C_OUT, ec="none", zorder=7))
    for wy, sgn in ((-22, 1), (22, -1)):                                                               # fillet welds bracket→jamb (both faces)
        ax.add_patch(Polygon([d(66, wy), d(66, wy + sgn * 9), d(56, wy)], closed=True, fc=C_OUT, ec="none", zorder=7))
    leader(ax, d(-7, 30), (ox - 200, oy + 40 * s), "hub tube\nwall", col=C_OUT, fs=6.5)
    leader(ax, d(4, -18), (ox - 200, oy - 6 * s), "fillet weld\nbracket→hub", col=C_OUT, fs=6.5)
    leader(ax, d(30, 20), (ox + 20 * s, oy + 80 * s), "bracket plate", col=C_OUT, fs=6.5)
    leader(ax, d(66, 20), (ox + 118 * s, oy + 78 * s), "fillet weld bracket→leaf stile\n(no bolts through the closed tube)", col=C_OUT, fw="bold", fs=6.5)

    draw_notes(ax, [
        "NOTES",
        "The bracket plate is FILLET-WELDED to BOTH the hub tube and the",
        "leaf's PIVOT-EDGE STILE — so the hub + leaf frame + drum cage swing",
        "as ONE weldment about the fixed post. The stile TRAVELS with the leaf",
        "and carries the pivot-corner plywood. No bolts pass through the closed",
        "stile (which can't be back-tightened); all-welded steel.",
        ], ox - 50 * s, oy - 64 * s, spacing=40, fs=6.0, width=1100, font=FONT)

    title_block(ax, "SHEET 15 OF 17",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="FRAME → PIVOT-POST CONNECTION (hub hinge bracket)",
                scale_note="ELEVATION + ENLARGED DETAIL · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.055)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet15.png"), dpi=DIAGRAM_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet15.png saved")

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 16  —  Bottom Clearance Cross-Section (Yd–Z), walkway grate lifted out.
#   The HARD-LIMIT envelope for the swinging panel's bottom edge in transport: it must
#   clear the BARE wall-cantilever bracket legs (Z180 std / Z200 widened) at the near+far
#   side walls AND the left lift-out floor-leg cantilever posts (top Z115). Derived rule:
#   15mm clearance over the tallest obstacle at each Yd → center bottom Z130, stepped side
#   bottoms Z195. Reconciles the 2D set with the stepped-frame bottom seen in the 3D model.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet16():
    from tbs_constants import (PANEL_FLOOR_GAP as P_CTR, PANEL_FLOOR_GAP_SIDE as P_SIDE,
                               PANEL_CORNER_YD_L as jL, PANEL_CORNER_YD_R as jR, WALKWAY_W,
                               WALKWAY_H, WALKWAY_GRATE_T, WALKWAY_BRACKET_H as WALL_LEG,
                               WALKWAY_WIDE_BRACKET_H as WALL_LEG_W, WALKWAY_BRACKET_ARM_Z0 as ARM_BOT,
                               PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR, PROC_TRAY_RIM,
                               PROC_TRAY_FLOOR_Z_LOW, LT_CAGE_BOT, LT_BBEAM_Z1,
                               DRUM_CAGE_YD_L, DRUM_CAGE_YD_R, LEFT_WK_CANT_LEG_YDS, LEFT_WK_CANT_POST_W)
    WID       = PW
    ARM_TOP   = WALKWAY_H - WALKWAY_GRATE_T      # 115 — grate seat / arm top
    CLR       = P_CTR - ARM_TOP                  # 60 — clearance over the arm/post tops (= P_SIDE − WALL_LEG)
    TRAY_FLR  = PROC_TRAY_FLOOR_Z_LOW            # 20 — tray floor
    TRAY_RIM  = TRAY_FLR + PROC_TRAY_RIM         # 70 — fixed tray rim TOP
    POST_CLR  = LT_CAGE_BOT - ARM_TOP            # 15 — drum-cage bottom over the floor-leg POSTS (Z115) — GOVERNS the floor gap
    TRAY_CLR  = LT_CAGE_BOT - TRAY_RIM           # 60 — drum-cage bottom over the fixed tray rim (Z70)
    BREAK_Z   = 480

    fig, ax = plt.subplots(figsize=(22, 8))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-370, WID + 520)
    ax.set_ylim(-215, 605)

    ax.text(WID / 2, 565, "BOTTOM CLEARANCE CROSS-SECTION  (Yd–Z · looking toward the cargo door)",
            ha="center", fontsize=11, fontweight="bold", color=C_OUT, **FONT)
    ax.text(WID / 2, 540, "transport: walkway grate LIFTED OUT; the FIXED tray stays — the swinging panel + drum-cage bottom must clear both",
            ha="center", fontsize=7.5, color=C_DIM, **FONT)

    # floor + side walls
    ax.plot([-310, WID + 310], [0, 0], color=C_OUT, lw=1.6, zorder=2)
    ax.text(WID + 305, -4, "FLOOR Z0", va="top", ha="right", fontsize=6.5, color=C_DIM, **FONT)
    for wx, lbl, ha_ in ((0, "NEAR WALL", "right"), (WID, "FAR WALL", "left")):
        ax.plot([wx, wx], [0, 505], color=C_OUT, lw=2.4, zorder=2)
        ax.text(wx + (-8 if ha_ == "right" else 8), 500, f"{lbl} (Yd{wx})", rotation=90,
                va="top", ha=ha_, fontsize=6.5, color=C_DIM, **FONT)

    # processing tray (center pan) — FIXED/installed; floor Z20, rim TOP Z70 (the governing swing obstacle)
    ax.add_patch(Rectangle((PROC_TRAY_YD_NEAR, TRAY_FLR), PROC_TRAY_YD_FAR - PROC_TRAY_YD_NEAR, PROC_TRAY_RIM,
                           fc="#DCEAF5", ec=C_OUT, lw=1.0, zorder=2))
    ax.text(560, TRAY_FLR + PROC_TRAY_RIM / 2,
            "PROCESSING TRAY — FIXED  (rim top Z70)", ha="center", va="center", fontsize=6.0, color="#2A5A80", **FONT, zorder=10)

    # ── wall-cantilever brackets (near + far) — vertical leg to Z180 std / Z200 widened; arm Z90–115 ──
    def wall_bracket(x_wall, sign):
        legw = 44
        x0 = x_wall if sign > 0 else x_wall - legw
        ax.add_patch(Rectangle((x0, 0), legw, WALL_LEG, fc=C_STEEL, ec=C_OUT, lw=1.2, hatch="///", zorder=4))
        ax.add_patch(Rectangle((x0, WALL_LEG), legw, WALL_LEG_W - WALL_LEG, fc="none", ec=C_STEEL,
                               lw=1.0, ls=(0, (4, 2)), zorder=4))       # widened-leg extension to Z200 (dashed)
        arm_x = x_wall if sign > 0 else x_wall - WALKWAY_W
        ax.add_patch(Rectangle((arm_x, ARM_BOT), WALKWAY_W, ARM_TOP - ARM_BOT, fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=4))
    wall_bracket(0, +1)
    wall_bracket(WID, -1)
    leader(ax, (22, WALL_LEG), (230, 400),
           "NEAR side-wall bracket\n(fixed): leg Z180/200,\narm Z90–115", col=C_OUT, fs=6.2)
    leader(ax, (WID - 22, WALL_LEG), (WID - 230, 400), "FAR side-wall bracket\n(fixed, mirror)", col=C_OUT, fs=6.2)

    # ── left lift-out FLOOR-LEG cantilever posts (Yd 250..2110) — remain when the grate lifts out ──
    for yd in LEFT_WK_CANT_LEG_YDS:
        pw = LEFT_WK_CANT_POST_W
        ax.add_patch(Rectangle((yd - pw / 2, 0), pw, ARM_BOT, fc=C_STEEL, ec=C_OUT, lw=0.9, zorder=3))
        ax.add_patch(Rectangle((yd - pw / 2 - 8, 0), pw + 16, 8, fc=C_STEEL, ec=C_OUT, lw=0.7, zorder=3))     # foot plate
        ax.add_patch(Rectangle((yd - pw / 2, ARM_BOT), pw, ARM_TOP - ARM_BOT, fc=C_STEEL, ec=C_OUT, lw=0.7, zorder=3))
    leader(ax, (1180, ARM_TOP), (1180, -100),
           "LEFT lift-out FLOOR-LEG cantilevers (×5 @ Yd 250/800/1180/1560/2110)\nposts REMAIN when the grate lifts out — top Z115", col=C_OUT, fs=6.4)

    # ── walkway grate — LIFTED OUT (ghost dashed at Z115..140) ──
    ax.add_patch(Rectangle((0, ARM_TOP), WID, WALKWAY_GRATE_T, fc="#EEEEEE", ec=C_DIM,
                           lw=1.0, ls=(0, (5, 3)), alpha=0.45, zorder=2))
    ax.text(WID * 0.30, ARM_TOP + WALKWAY_GRATE_T + 8, "WALKWAY GRATE — LIFTED OUT (ghosted, Z115–140)",
            ha="center", va="bottom", fontsize=6.6, color=C_DIM, style="italic", **FONT, zorder=6)

    # ── DRUM-CAGE lower beam — SWEPT transport position (ghosted): the panel+drum swing across the
    #    container, so the cage bottom (Z130) passes over the FIXED floor-leg posts (Z115) + tray (Z70).
    #    The floor gap was raised to 217 so LT_CAGE_BOT clears the tallest (the posts) by POST_CLR. ──
    ax.add_patch(Rectangle((DRUM_CAGE_YD_L, LT_CAGE_BOT), DRUM_CAGE_YD_R - DRUM_CAGE_YD_L,
                           LT_BBEAM_Z1 - LT_CAGE_BOT, fc="#E0C8C8", ec="#803030", lw=1.4, ls=(0, (5, 3)), zorder=8))
    ax.text((DRUM_CAGE_YD_L + DRUM_CAGE_YD_R) / 2, (LT_CAGE_BOT + LT_BBEAM_Z1) / 2,
            f"DRUM CAGE lower beam — SWEPT (Z{int(LT_CAGE_BOT)}–{int(LT_BBEAM_Z1)})", ha="center", va="center",
            fontsize=6.2, fontweight="bold", color="#803030", **FONT, zorder=9)
    leader(ax, (1450, LT_CAGE_BOT), (1780, 360),
           f"{POST_CLR}mm CLR — cage bottom (Z{int(LT_CAGE_BOT)}) over the\nfloor-leg POSTS (Z115) — GOVERNS the floor gap\n(clears the fixed tray rim Z70 by {TRAY_CLR}mm)", col="#B00", fw="bold", fs=6.2)

    # ── HINGE PANEL bottom profile (stepped): center Z217, sides Z282 ──
    panel = [(0, P_SIDE), (jL, P_SIDE), (jL, P_CTR), (jR, P_CTR), (jR, P_SIDE),
             (WID, P_SIDE), (WID, BREAK_Z), (0, BREAK_Z)]
    ax.add_patch(Polygon(panel, closed=True, fc=C_PLASTIC, ec="none", alpha=0.5, zorder=7))
    ax.plot([0, jL, jL, jR, jR, WID], [P_SIDE, P_SIDE, P_CTR, P_CTR, P_SIDE, P_SIDE],
            color="#1763C8", lw=2.8, zorder=9)
    ax.text(WID / 2, (P_CTR + BREAK_Z) / 2 + 55, "HINGE PANEL (swinging leaf) — BOTTOM PROFILE",
            ha="center", va="center", fontsize=8.5, fontweight="bold", color="#1763C8", **FONT, zorder=9)
    ax.text(WID / 2, BREAK_Z + 15, "↑ panel continues to Z2388 (top)", ha="center", va="bottom",
            fontsize=6.5, color=C_DIM, **FONT, zorder=9)


    # ── dimension ladders ──
    draw_dim_v(ax, -100, 0, ARM_TOP, "115mm posts", offset=14, fs=6.0, font=FONT, right=False)
    draw_dim_v(ax, -150, 0, LT_CAGE_BOT, f"{int(LT_CAGE_BOT)}mm cage btm", offset=14, fs=6.0, font=FONT, right=False)
    draw_dim_v(ax, -200, 0, P_CTR, f"{int(P_CTR)}mm ctr", offset=14, fs=6.0, font=FONT, right=False)
    draw_dim_v(ax, -50, 0, TRAY_RIM, "70mm tray", offset=10, fs=5.6, font=FONT, right=False)
    draw_dim_v(ax, WID + 50, 0, WALL_LEG_W, "200mm leg", offset=14, fs=6.0, font=FONT, right=True)
    draw_dim_v(ax, WID + 100, 0, P_SIDE, f"{int(P_SIDE)}mm side", offset=14, fs=6.0, font=FONT, right=True)
    draw_dim_v(ax, jL - 35, P_CTR, P_SIDE, f"{int(P_SIDE - P_CTR)}mm step", offset=12, fs=6.0, font=FONT, right=False)
    draw_dim_v(ax, DRUM_CAGE_YD_R + 60, ARM_TOP, LT_CAGE_BOT, f"{POST_CLR}mm", offset=10, fs=5.6, font=FONT, right=True)  # governing clr

    # ── Yd zone dims (bottom) ──
    draw_dim_h(ax, 0, jL, -50, f"{jL}mm near corner — STEP UP", offset=-14, fs=6, font=FONT)
    draw_dim_h(ax, jL, jR, -50, f"{jR - jL}mm center (Z{int(P_CTR)})", offset=-14, fs=6, font=FONT)
    draw_dim_h(ax, jR, WID, -50, f"{WID - jR}mm far corner — STEP UP", offset=-14, fs=6, font=FONT)

    # ── notes block (right margin) ──
    draw_notes(ax, [
        "HARD LIMIT — floor gap (transport swing, tray + posts FIXED)",
        "The panel+drum swing across the container. Governing obstacle:",
        "the LEFT walkway floor-leg POSTS (Z115, stay bolted) — taller",
        "than the fixed tray rim (Z70). So the drum-cage bottom must",
        "clear Z115.  Floor gap RAISED 130 → 217:",
        f"  • cage bottom Z{int(LT_CAGE_BOT)} clears the Z115 posts by {POST_CLR}mm (and",
        f"    the Z70 tray by {TRAY_CLR}mm).",
        f"  • panel center bottom Z{int(P_CTR)}, corners step up to Z{int(P_SIDE)}",
        f"    (step {int(P_SIDE - P_CTR)}mm) — now over-clears the Z180/200 wall legs.",
        f"  • costs drum interior: 1970 → 1883 (clears a 1780 operator by 103).",
        "Only the walkway GRATE lifts out; the floor-leg posts + tray stay.",
    ], WID + 45, 575, spacing=22, fs=5, title_fs=6, color="#403000",
       title_color="#806010", width=575, border_color="#806010", font=FONT)

    title_block(ax, "SHEET 16 OF 17",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="TRANSPORT-SWING BOTTOM CLEARANCE — DRUM CAGE vs FIXED POSTS/TRAY + PANEL vs WALL BRACKETS",
                scale_note="SECTION Yd–Z · EQUAL ASPECT · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.065)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet16.png"), dpi=DIAGRAM_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet16.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 17  —  Fold-Down Light Apron (closes the 217mm under-leaf gap that the
#   floor-gap raise opened). TWO fold-down aprons at the corner zones (bottom-hinged
#   to the threshold, fold INTO the container for the transport swing) + a FIXED
#   center baffle under the drum bay (the drum sweeps through, so no moving part).
# ═══════════════════════════════════════════════════════════════════════════════
def sheet17():
    from tbs_constants import (PANEL_FLOOR_GAP_SIDE as ATOP, PANEL_FLOOR_GAP as PBOT_CTR,
                               PANEL_CORNER_YD_L as jL, PANEL_CORNER_YD_R as jR, LT_CAGE_BOT,
                               APRON_IN_L, APRON_IN_R, APRON_CAGE_GAP,
                               DRUM_CAGE_YD_L as cgL, DRUM_CAGE_YD_R as cgR, APRON_FIX_W)
    WID  = PW
    STUB = WID - APRON_FIX_W     # 2162 — far fold-down apron ends here; beyond it is the TRAVELLING pivot-corner leaf
    THR  = 51        # threshold sill top Z
    AT   = 40        # apron thickness (12mm exterior BC plywood, flat-black interior)
    BAYB = 217       # bay bottom cap Z
    BAF_TOP = LT_CAGE_BOT - 10   # 130 — baffle top, 10mm under the swept drum-cage bottom (Z140)
    BRZ  = 51        # threshold top (baffle base)

    fig, ax = plt.subplots(figsize=(20, 11))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-130, WID + 500)
    ax.set_ylim(-170, 920)

    ax.text(WID / 2, 878, "FOLD-DOWN LIGHT APRON — closes the under-leaf gap opened by the 217mm floor-gap raise",
            ha="center", fontsize=12, fontweight="bold", color=C_OUT, **FONT)

    # ══ ELEVATION (Yd–Z) — door-bottom layout, interior face (top band) ══
    ez = 500
    ax.text(WID / 2, ez + ATOP + 70, "ELEVATION — door bottom (interior face)", ha="center", fontsize=9, fontweight="bold", color=C_OUT, **FONT)
    ax.plot([0, WID], [ez, ez], color=C_OUT, lw=1.6)
    ax.text(WID + 20, ez, "FLOOR Z0", va="center", ha="left", fontsize=6.5, color=C_DIM, **FONT)
    # Fold-down aprons — each extends INBOARD past the center-zone step line to a brush gap off the cage
    # (Yd APRON_IN_L / APRON_IN_R); its top steps 282 (corner) → 217 (center ext) to follow the leaf bottom.
    for y0, y1, top, lbl in [(0, jL, ATOP, "NEAR fold-down apron"), (jL, APRON_IN_L, PBOT_CTR, None),
                             (APRON_IN_R, jR, PBOT_CTR, None), (jR, STUB, ATOP, "FAR fold-down apron")]:
        ax.add_patch(Rectangle((y0, ez), y1 - y0, top, fc=C_PLASTIC, ec=C_OUT, lw=1.4, alpha=0.75))
        if lbl:
            ax.text((y0 + y1) / 2, ez + top * 0.5, f"{lbl}\n(UP = sealing)\nZ0–{int(top)}", ha="center", va="center",
                    fontsize=7, fontweight="bold", color="#204060", **FONT)
    # pivot-corner leaf TRAVELS with the swinging panel up to the pivot line; tiny fixed past-pivot at the wall
    ax.add_patch(Rectangle((STUB, ez), PIVOT_YD - STUB, ATOP, fc=C_PLASTIC, ec=C_OUT, lw=1.4, alpha=0.75))
    ax.text((STUB + PIVOT_YD) / 2, ez + ATOP * 0.5, f"PIVOT-CORNER\nLEAF (travels)\nZ0–{int(ATOP)}", ha="center", va="center",
            fontsize=5.8, fontweight="bold", color="#204060", **FONT)
    ax.add_patch(Rectangle((PIVOT_YD, ez), WID - PIVOT_YD, ATOP, fc="#B8B8C0", ec=C_OUT, lw=1.0, hatch="xx", alpha=0.6))
    ax.add_patch(Rectangle((APRON_IN_L, ez), APRON_IN_R - APRON_IN_L, BAF_TOP, fc="#C8A56A", ec=C_OUT, lw=1.2, hatch="///", alpha=0.6))
    ax.text((APRON_IN_L + APRON_IN_R) / 2, ez + 66, f"FIXED CENTER BAFFLE\n(trimmed to the apron edges — no moving part)\nZ51–{int(BAF_TOP)} (drum frame sweeps clear above)", ha="center", va="center",
            fontsize=7, fontweight="bold", color=C_OUT, **FONT)
    # Horizontal strip brush on the baffle top edge → bristles sweep the cage bottom (Z140), 10mm gap.
    ax.add_patch(Rectangle((cgL, ez + BAF_TOP), cgR - cgL, 12, fc="#2FA84F", ec="#1c6b32", lw=0.8))
    leader(ax, ((cgL + cgR) / 2 + 120, ez + BAF_TOP + 12), (WID * 0.60, ez + ATOP + 44),
           "top BRUSH on the baffle edge — bristles sweep the cage bottom (Z140), 10mm gap", col="#1c6b32", fw="bold", fs=6)
    # Vertical strip brushes on the two apron inner edges → reach APRON_CAGE_GAP to the cage sides.
    for yb in (APRON_IN_L - 4, APRON_IN_R - 2):
        ax.add_patch(Rectangle((yb, ez + BAF_TOP), 6, PBOT_CTR - BAF_TOP, fc="#2FA84F", ec="#1c6b32", lw=0.8))
    leader(ax, (APRON_IN_L, ez + (BAF_TOP + PBOT_CTR) / 2), (jL - 330, ez + PBOT_CTR + 20),
           f"vertical edge BRUSH on each apron inner\nedge → {APRON_CAGE_GAP}mm to the cage side", col="#1c6b32", fw="bold", fs=6)
    ax.plot([0, jL, jL, jR, jR, WID], [ez + ATOP, ez + ATOP, ez + PBOT_CTR, ez + PBOT_CTR, ez + ATOP, ez + ATOP],
            color="#1763C8", lw=1.6, ls=(0, (6, 3)))
    ax.text(WID / 2, ez + ATOP + 14, "swinging leaf bottom (stepped Z217 ctr / Z282 corners) — the aprons seal up to it",
            ha="center", fontsize=6.6, color="#1763C8", **FONT)
    draw_dim_h(ax, 0, APRON_IN_L, ez - 45, f"{int(APRON_IN_L)}mm near apron", offset=-12, fs=6, font=FONT)
    draw_dim_h(ax, APRON_IN_L, APRON_IN_R, ez - 45, f"{int(APRON_IN_R - APRON_IN_L)}mm center baffle", offset=-12, fs=6, font=FONT)
    draw_dim_h(ax, APRON_IN_R, STUB, ez - 45, f"{int(STUB - APRON_IN_R)}mm far apron", offset=-12, fs=6, font=FONT)
    draw_dim_h(ax, STUB, PIVOT_YD, ez - 45, f"{int(PIVOT_YD - STUB)}mm pivot leaf", offset=-12, fs=5.6, font=FONT)

    # ══ SECTION A (X–Z) — corner apron fold action (bottom-left) ══
    a0 = 130
    def aA(x, z): return (a0 + x, z)
    ax.text(a0 + 130, 400, "SECTION A — corner apron (fold action)", ha="center", fontsize=9, fontweight="bold", color=C_OUT, **FONT)
    ax.text(a0 + 130, 384, "vertical section · exterior LEFT → interior RIGHT", ha="center", fontsize=6.4, color=C_DIM, **FONT)
    ax.plot([a0 - 95, a0 + 340], [0, 0], color=C_OUT, lw=1.6)
    ax.add_patch(Rectangle(aA(-51, 0), 51, THR, fc=C_STEEL, ec=C_OUT, lw=1.2, hatch="///"))            # threshold sill
    leader(ax, aA(-25, THR), aA(-85, 165), "threshold sill\n(fixed, Z0–51)", col=C_OUT, fs=6)
    ax.add_patch(Rectangle(aA(-20, ATOP), 62, 95, fc=C_PLASTIC, ec=C_OUT, lw=1.4, alpha=0.7))          # leaf bottom (corner)
    leader(ax, aA(32, ATOP + 45), aA(150, 360), "swinging leaf bottom\n(corner zone, Z282)", col="#1763C8", fs=6)
    hx, hz = 6, 10
    ax.add_patch(Rectangle(aA(hx, hz), AT, ATOP - hz, fc=C_PLASTIC, ec=C_OUT, lw=1.7))                 # apron UP
    ax.text(a0 + hx + AT / 2, (ATOP + hz) / 2, "FOLD-DOWN APRON  (UP = sealing)", ha="center", va="center",
            fontsize=6.6, fontweight="bold", color="#204060", **FONT, rotation=90)
    for bxx in range(int(a0 + hx + 4), int(a0 + hx + AT - 2), 5):                                      # top brush seal
        ax.plot([bxx, bxx], [ATOP, ATOP + 17], color="#806040", lw=0.9)
    leader(ax, aA(hx + AT / 2, ATOP + 9), aA(175, 320), "top BRUSH seal to the leaf\n(leaf sweeps sideways off it)", col=C_OUT, fw="bold", fs=6)
    ax.add_patch(Circle(aA(hx, hz), 7, fc=C_STEEL, ec=C_OUT, lw=1.1))                                  # bottom hinge
    leader(ax, aA(hx, hz), aA(-80, 70), "piano hinge to the sill\n+ baffle lip (light-tight)", col=C_OUT, fw="bold", fs=6)
    R = ATOP - hz
    th = np.linspace(np.pi / 2, 0, 40)                                                                 # fold arc (top edge)
    ax.plot(a0 + hx + R * np.cos(th), hz + R * np.sin(th), color="#B00", lw=0.9, ls=(0, (4, 2)))
    ax.annotate("", xy=aA(hx + R * 0.78, hz + R * 0.30), xytext=aA(hx + 26, ATOP * 0.62),
                arrowprops=dict(arrowstyle="-|>", color="#B00", lw=1.5))
    ax.add_patch(Rectangle(aA(hx, hz), R, AT, fc=C_PLASTIC, ec="#B00", lw=1.2, ls=(0, (4, 2)), alpha=0.30))  # folded (transport)
    ax.text(a0 + hx + R * 0.55, hz + AT + 16, "FOLDED (transport) — flat INTO the container,\nclear of the swing path",
            ha="center", fontsize=6.3, color="#B00", fontweight="bold", **FONT)
    draw_dim_v(ax, a0 - 80, 0, ATOP, f"{int(ATOP)}mm", offset=12, fs=6, font=FONT)

    # ══ DETAIL D (X–Z) — fixed center baffle under the bay (bottom-right) ══
    d0 = 1560
    def dD(x, z): return (d0 + x, z)
    ax.text(d0 + 95, 400, "DETAIL D — fixed center baffle (drum bay)", ha="center", fontsize=9, fontweight="bold", color=C_OUT, **FONT)
    ax.plot([d0 - 45, d0 + 245], [0, 0], color=C_OUT, lw=1.6)
    ax.add_patch(Rectangle(dD(40, BAYB - 8), 155, 8, fc=C_PLASTIC, ec=C_OUT, lw=1.2))                  # bay bottom cap Z217
    leader(ax, dD(118, BAYB - 4), dD(195, 350), "bay bottom cap (Z217) —\nbay closes Z130→217 in operation", col=C_OUT, fs=6)
    ax.add_patch(Rectangle(dD(58, LT_CAGE_BOT), 118, 40, fc="none", ec="#803030", lw=1.0, ls=(0, (4, 2))))   # drum cage ghost (bottom beam)
    leader(ax, dD(117, LT_CAGE_BOT + 20), dD(210, 250), f"drum cage bottom (Z{int(LT_CAGE_BOT)})\nsweeps clear above the baffle", col="#803030", fs=6)
    ax.add_patch(Rectangle(dD(70, THR), 90, BAF_TOP - THR, fc="#C8A56A", ec=C_OUT, lw=1.2, hatch="///"))      # fixed plywood baffle Z51..130
    leader(ax, dD(115, (THR + BAF_TOP) / 2), dD(-35, 120), f"fixed plywood baffle\n(Z{THR}–{int(BAF_TOP)}) — kills the\nsightline under the bay", col=C_OUT, fw="bold", fs=6)
    # horizontal strip brush on the baffle top edge — fills the 10mm gap up to the swept cage bottom
    ax.add_patch(Rectangle(dD(70, BAF_TOP), 90, LT_CAGE_BOT - BAF_TOP, fc="#2FA84F", ec="#1c6b32", lw=0.8))
    for bx in range(int(dD(74, 0)[0]), int(dD(158, 0)[0]), 6):
        ax.plot([bx, bx], [BAF_TOP, LT_CAGE_BOT], color="#141414", lw=0.7)
    leader(ax, dD(160, (BAF_TOP + LT_CAGE_BOT) / 2), dD(230, 175), "top BRUSH strip — bristles sweep\nthe cage bottom (fills the 10mm gap)", col="#1c6b32", fw="bold", fs=6)
    draw_dim_v(ax, d0 - 28, THR, BAF_TOP, f"{int(BAF_TOP - THR)}mm", offset=10, fs=6, font=FONT)

    # ══ DETAIL E (enlarged 5:1) — plywood↔plywood 45° chamfer joint (TYP of all moving plywood joints) ══
    e0, ebz, S = 690, 150, 5.0
    def eE(x, z): return (e0 + x * S, ebz + z * S)
    T, xc, BL = 12, 16, 30          # 12mm ply · scarf start · panel run each side
    ax.text(e0 + 33 * S, 400, "DETAIL E — plywood↔plywood chamfer joint (TYP)", ha="center", fontsize=9, fontweight="bold", color=C_OUT, **FONT)
    ax.text(e0 + 33 * S, 384, "45° scarf · EPDM bonded to the FIXED face · enlarged 5:1", ha="center", fontsize=6.4, color=C_DIM, **FONT)
    A = [eE(0, 0), eE(xc, 0), eE(xc + T, T), eE(0, T)]                       # fixed panel (left)
    B = [eE(xc, 0), eE(xc + T + BL, 0), eE(xc + T + BL, T), eE(xc + T, T)]   # moving panel (right)
    ax.fill([p[0] for p in A], [p[1] for p in A], fc=C_PLASTIC, ec=C_OUT, lw=1.4, zorder=3)
    ax.fill([p[0] for p in B], [p[1] for p in B], fc="#C8A56A", ec=C_OUT, lw=1.4, zorder=3)
    ax.plot([eE(xc, 0)[0], eE(xc + T, T)[0]], [eE(xc, 0)[1], eE(xc + T, T)[1]],
            color="#5A3020", lw=4, solid_capstyle="butt", zorder=4)         # EPDM on the fixed scarf face
    leader(ax, eE(xc + T / 2, T / 2), (e0 - 20, ebz + T * S + 66), "EPDM bonded to the\nFIXED chamfer face", col="#5A3020", fw="bold", fs=6)
    ax.text(*eE(xc / 2, T + 3), "FIXED ply", ha="center", va="bottom", fontsize=6.4, fontweight="bold", color="#204060", **FONT)
    ax.text(*eE(xc + T + BL * 0.6, T + 3), "MOVING ply", ha="center", va="bottom", fontsize=6.4, fontweight="bold", color="#204060", **FONT)
    bx, bz = eE(xc + T + 6, T / 2)                                          # moving panel sweeps off along the 45° normal
    ax.annotate("", xy=(bx + 72, bz + 72), xytext=(bx, bz), arrowprops=dict(arrowstyle="-|>", color="#B00", lw=1.6))
    ax.text(bx + 78, bz + 80, "moving panel sweeps\noff the seal (no bind)", ha="left", fontsize=6, fontweight="bold", color="#B00", **FONT)
    ax.annotate("", xy=(eE(xc + T / 2, T / 2)[0] - 4, ebz + T * S * 0.5), xytext=(e0 - 46, ebz + T * S * 0.5),
                arrowprops=dict(arrowstyle="-|>", color="#E0A000", lw=1.4))    # light ray blocked at the diagonal lap
    ax.text(e0 - 46, ebz + T * S * 0.5 - 16, "light", ha="left", fontsize=5.6, color="#B07000", **FONT)
    draw_dim_v(ax, e0 - 24, ebz, ebz + T * S, "12mm", offset=10, fs=6, font=FONT)
    ax.text(*eE(xc + T + 2, 1.5), "45°", ha="left", va="bottom", fontsize=6, color=C_DIM, **FONT)

    # ══ notes ══
    draw_notes(ax, [
        "FOLD-DOWN LIGHT APRON — operation",
        f"• Two aprons, bottom-hinged to the threshold, fold INTO the container. Each runs from the door corner IN to {int(APRON_CAGE_GAP)}mm off the cage side (Yd {int(APRON_IN_L)} / {int(APRON_IN_R)}), crossing the step line — top steps 282→217 to follow the leaf. 12mm exterior BC plywood, flat-black interior (a light seal).",
        "• OPERATION: apron UP — top brush to the leaf bottom, EPDM to the jambs. Held vertical by an over-centre catch each side.",
        "• TRANSPORT: release the catches, fold both aprons flat into the container, then swing the panel; the leaf clears the ~40mm folded panel.",
        "• CENTER (drum bay): a FIXED plywood baffle (Z51–130), trimmed to the apron edges, closes the strip under the cage; a horizontal strip BRUSH on its top edge fills the 10mm up to the swept Z140 cage bottom.",
        f"• SIDE BRUSHES: a vertical strip brush on each apron inner edge bridges the {int(APRON_CAGE_GAP)}mm to the cage side; the bay bottom cap closes Z130→217 in operation.",
        "• CHAMFER JOINTS (Detail E): every plywood↔plywood MOVING joint is a 45° scarf with EPDM bonded to the FIXED face — a light-tight lap the moving panel sweeps off without binding. TYP at: apron top↔swing-leaf bottom, apron side↔fixed stub/jamb, swing-panel edge↔side leaves, apron↔center baffle.",
    ], WID + 30, 890, spacing=21, fs=5.8, title_fs=6.6, color="#403000",
       title_color="#806010", width=450, wrap=49, border_color="#806010", font=FONT)

    title_block(ax, "SHEET 17 OF 17",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="FOLD-DOWN LIGHT APRON + FIXED CENTER BAFFLE — under-leaf gap closure",
                scale_note="SECTION + ELEVATION · ALL DIMS IN mm",
                doc_id="TBS-001 · Hinged Light-Trap Panel", height=0.045)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "hingepanel-sheet17.png"), dpi=DIAGRAM_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet17.png saved")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating hinged light-trap panel drawings...")
    sheet1()
    sheet2()
    sheet3()
    sheet4()
    sheet5()
    sheet6()
    sheet7()
    sheet8()
    sheet9()
    sheet10()
    sheet11()
    sheet12()
    sheet13()
    sheet14()
    sheet15()
    sheet16()
    sheet17()
    print("Done.")
