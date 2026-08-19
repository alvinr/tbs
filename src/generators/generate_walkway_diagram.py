#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_walkway_diagram.py  —  TBS-001 Perimeter Walkway

Sheet 1 — Plan view of walkway layout:
  Top-down view showing all 4 walkway sections with bracket positions.
  Left walkway shown as removable lift-out (no brackets — panel conflict).
  Right walkway = cantilever rectangle (2×1×0.120in steel) off the IBC frame + wall cleats.
  Panel swing sweep (~56° about the pivot) shown as dashed red sector.

Sheet 2 — Cross-section + bolt pattern (near walkway bracket):
  View A: Detail cross-section (~5:1) showing grated deck, wall-cantilevered
  bracket, tray rim clearance, and dimensional annotations.  Section cut
  looking along X axis.  Triangular gusset brackets bolted to container wall
  ribs — no legs, no beam, no floor contact.  Entire tray clear for film.
  View B: Plate face showing triangular 3× M12 bolt pattern.

Sheet 3 — Detail A: Right walkway cantilever support (IBC end)  [rev 12]:
  245mm wide (F1-shortened from the standard 300 so the outer beam lands on the
  combined-plate seat).  Plan view of the closed 2×1in-tube (50.8×25.4)
  rectangle (2 long beams at X=4329/4574 running the full container width +
  2 short end beams), picked up at mid-span by 2 arms cantilevering off the
  IBC corridor uprights (half-lapped where the long beams cross), on wall
  cleats at the left corners and combined corner plates (shared with the
  bottom film rail) at the right corners.  Replaces the ceiling-hung
  hangers.  Zero tray contact, zero floor contact, zero roof penetrations.
  The INNER long beam is CRANKED outboard 100mm around the muslin-drop rod
  slot (Yd 1912-2062) so the rigid rod drops straight at the tray edge while
  the beam stays ONE continuous, uncut member.

Sheet 4 — Detail B: Left walkway butt joint and panel clearance:
  View looking along Yd (near wall toward far wall), X horizontal, Z vertical.
  Shows left walkway grating (X=170-470, removable lift-out) meeting the
  full-width steel edge beam at the butt joint (X=470); both grating edges bear
  on its Z65 ledges (no X=470 bracket). The swinging cage (panel + drum) is
  shown as ghost — it sweeps past the butt joint through the vacated left-walkway
  zone, riding the Z130 floor gap over the brackets. Bearing strip and floor leg
  shown in cross-section.

Sheet 5 — Detail C: Left walkway floor-leg support + drum-exit punch-out (plan):
  All 5 floor-leg cantilever brackets (post on bare floor X=140 + arm to the grate
  edge X=470) carrying the removable left grate, PLUS the drum-exit punch-out — the
  deck deepened to 600×760mm at the light-lock exit, on the 3 middle brackets whose
  arms extend to X=770. Zero processing tray contact. (Merged from the former Sheet 9.)

Sheet 6 — Detail D: Left walkway floor-leg cantilever bracket (section + foot plate):
  Two views of how the steel edge beam is simply supported at each end — an
  interior seat plate (drop-in pocket) + 3× M12 bolts through the corrugated
  wall to an exterior backing plate. Same load path as the IBC wall seats;
  demountable for transport.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
import os
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_notes, draw_legend
from tbs_constants import C_LEN, C_WID, PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_W, PROC_TRAY_D, PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR, PROC_TRAY_RIM, WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T, WALKWAY_GRATE_CLIP_PITCH, WALKWAY_BRACKET_H, WALKWAY_BRACKET_UPPER_BOLT_Z, WALKWAY_BRACKET_T, WALKWAY_BRACKET_SPACING, WALKWAY_REINF_W, WALKWAY_REINF_H, WALKWAY_REINF_T, WALKWAY_REINF_W_WIDE, WALKWAY_REINF_H_WIDE, WALKWAY_GUSSET_REACH, WALKWAY_BRACKET_BOLT_DX, WALKWAY_BRACKET_BOLT_DX_WIDE, WALKWAY_BRACKET_BOLT_Z_LO, WALKWAY_BRACKET_ARM_H, PIVOT_X, PIVOT_YD, SWING_LOCK_DEG, PANEL_CUT_YD, IBC_COL_X, IBC_W, CORRIDOR_YD_NEAR, CORRIDOR_YD_FAR, IBC_FRAME_RHS, RAIL_X_L, RAIL_X_R, PH_X, WALKWAY_BRACKET_ARM_Z0, WALKWAY_NEAR_YD, WALKWAY_FAR_YD, WALKWAY_LEFT_X, WALKWAY_RIGHT_X, WALKWAY_RIGHT_W, RWK_X_L, RWK_X_R, RWK_X_UP, RWK_BEARER_W, PROC_OPEN_X_L, PROC_OPEN_X_R, PROC_OPEN_YD_N, PROC_OPEN_YD_F, PROC_OPEN_AREA, PANEL_FLOOR_GAP, LEFT_WK_CANT_LEG_X, LEFT_WK_CANT_LEG_YDS, LEFT_WK_CANT_POST, LEFT_WK_CANT_POST_W, LEFT_WK_CANT_FOOT, LEFT_WK_CANT_FOOT_X0, LEFT_WK_CANT_FOOT_BOLT_N, LEFT_WK_CANT_FOOT_BOLT_DX, LEFT_WK_CANT_FOOT_BOLT_DY, LEFT_WK_CANT_ARM_Z0, LEFT_WK_CANT_ARM_W, LEFT_WK_CANT_ARM_W_WIDE, LEFT_WK_CANT_STD_REACH, LEFT_WK_CANT_WIDE_REACH, SPRAY_BAR_Z_BOT, SPRAY_BAR_Z_TOP, WALKWAY_NEAR_WIDE_W, WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_X_R, WALKWAY_MAX_OVERHANG, WALKWAY_LEFT_WIDE_W, WALKWAY_LEFT_WIDE_YD_L, WALKWAY_LEFT_WIDE_YD_R, WALKWAY_WIDE_BRACKET_T, WALKWAY_WIDE_BRACKET_H, WALKWAY_MUSLIN_NOTCH_DX, WALKWAY_MUSLIN_NOTCH_DY, WALKWAY_MUSLIN_NOTCH_YD0, WALKWAY_MUSLIN_NOTCH_L_X0, WALKWAY_MUSLIN_NOTCH_R_X0, SPRAY_BAR_SLIT_W, EP_X, EP_W, BA_X, BA_W, EVAP_W, EVAP_D, EVAP_STOW_X, EVAP_STOW_YD, DIAGRAMS_DIR
from tbs_constants import DIAGRAM_DPI

# ── Palette ───────────────────────────────────────────────────────────────────
BG      = "#FFFFFF"
C_OUT   = "#1A1A1A"
C_CL    = "#2060A0"
C_DIM   = "#404040"
C_STEEL = "#B0B0B8"
C_GRATE = "#A0A0A8"
C_FRAME = "#808890"
C_TRAY  = "#A0B0A0"
C_FLOOR = "#E0DDD8"
C_WALL  = "#C0C0C8"
C_BRKT  = C_STEEL     # bracket fill — unified to the project-standard steel tone (lighter, matches sheet6 + the IBC/film-plane/hingepanel sheets; the darker #707888 was a readability outlier, Alvin 2026-08-18)
FONT    = {"fontfamily": "monospace"}

bbox = dict(fc="white", ec="none", pad=1.5, alpha=0.85)

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — Plan View of Walkway Layout
#
# Top-down view showing all 4 walkway sections with bracket positions.
# Horizontal = X (container long axis)
# Vertical   = Yd (container width)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():

    BRKT_MARK_W = 30   # bracket marker width in plan view (mm, visual)
    BRKT_MARK_D = 20   # bracket marker depth in plan view (mm, visual)

    # ── Figure ───────────────────────────────────────────────────────────────
    PAD_X = 300
    PAD_Y_BOT = 1650  # extra room below for notes + title block (notes drop clear of the plan)
    PAD_Y_TOP = 300
    fig, ax = plt.subplots(figsize=(18, 14))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-PAD_X, C_LEN + PAD_X)
    ax.set_ylim(-PAD_Y_BOT, C_WID + PAD_Y_TOP)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container outline ────────────────────────────────────────────────────
    ax.add_patch(Rectangle((0, 0), C_LEN, C_WID,
                            fc="#F8F8F8", ec=C_OUT, lw=2.0, zorder=1))
    # Wall labels
    ax.text(C_LEN / 2, -40, "PINHOLE WALL",
            ha="center", va="top", fontsize=6, color=C_DIM, **FONT, zorder=15)
    ax.text(C_LEN / 2, C_WID + 40, f"FAR WALL",
            ha="center", va="bottom", fontsize=6, color=C_DIM, **FONT, zorder=15)
    ax.text(-40, C_WID / 2, "CARGO DOOR END",
            ha="right", va="center", fontsize=6, color=C_DIM,
            **FONT, zorder=15, rotation=90)
    ax.text(C_LEN + 40, C_WID / 2, f"FAR END",
            ha="left", va="center", fontsize=6, color=C_DIM,
            **FONT, zorder=15, rotation=90)

    # ── Processing tray (light fill) ─────────────────────────────────────────
    ax.add_patch(Rectangle((PROC_TRAY_X_L, PROC_TRAY_YD_NEAR),
                            PROC_TRAY_W, PROC_TRAY_D,
                            fc="#E8F0FF", ec=C_DIM, lw=1.0, ls="--",
                            alpha=0.3, zorder=2))
    ax.text((PROC_TRAY_X_L + PROC_TRAY_X_R) / 2,
            (PROC_TRAY_YD_NEAR + PROC_TRAY_YD_FAR) / 1.75,
            f"PROCESSING TRAY\n{PROC_TRAY_W}\u00d7{PROC_TRAY_D}mm",
            ha="center", va="center", fontsize=8, color=C_DIM,
            alpha=0.4, **FONT, zorder=3)

    # ── Draw walkway sections ────────────────────────────────────────────────
    # Left corners: BUTT JOINT — near/far walkways start at X=LXR (470)
    # so they clear the panel swing sweep at the door end.
    # Right corners: BUTT JOINT — right walkway is the cantilever rectangle (same 300mm width).
    C_WK = "#D0C8B8"
    WK_ALPHA = 0.3   # grating hatch at half the old alpha (0.6) — keeps the plan readable
    W = WALKWAY_W

    LX  = WALKWAY_LEFT_X;   LXR = LX + W
    RX  = WALKWAY_RIGHT_X;  RXR = RX + W      # right walkway inner/outer edges
    NY  = WALKWAY_NEAR_YD;  NYI = NY + W
    FY  = WALKWAY_FAR_YD;   FYO = FY + W
    TL  = PROC_TRAY_X_L;   TR = TL + PROC_TRAY_W

    # Near walkway: L-shaped polygon with bump-out aligned to transition brackets
    near_len = TR - LXR   # near/far walkway length (from butt joint to tray right)
    WXL = WALKWAY_NEAR_WIDE_X_L
    WXR = WALKWAY_NEAR_WIDE_X_R
    WW  = WALKWAY_NEAR_WIDE_W    # 500
    # Snap bump-out edges to actual bracket positions (ribs)
    _all_brkt = np.arange(LXR + WALKWAY_BRACKET_SPACING / 2,
                          TR + W, WALKWAY_BRACKET_SPACING)
    _wide_brkt = [bx for bx in _all_brkt if WXL <= bx <= WXR]
    WXL_B = _wide_brkt[0]  if _wide_brkt else WXL  # first widened bracket
    WXR_B = _wide_brkt[-1] if _wide_brkt else WXR  # last widened bracket
    near_verts = [
        (LXR, NY), (TR, NY), (TR, NYI),
        (WXR_B, NYI), (WXR_B, WW), (WXL_B, WW), (WXL_B, NYI),
        (LXR, NYI),
    ]
    walkway_polys = [
        ("NEAR",  near_verts, LXR, NY, near_len, W, True),
        ("FAR",   [(LXR, FYO), (TR, FYO), (TR, FY), (LXR, FY)],
         LXR, FY, near_len, W, True),
        ("LEFT",  [(LX, NY), (LX, FYO), (LXR, FYO), (LXR, NY)],
         LX, 0, W, C_WID, False),
        ("RIGHT", [(RX, NY), (RX, FYO), (RXR, FYO), (RXR, NY)],
         RX, 0, W, C_WID, False),
    ]

    for name, verts, wx, wy, ww, wh, is_x_axis in walkway_polys:
        # Walkway fill — polygon
        ax.add_patch(Polygon(verts, closed=True,
                             fc=C_WK, ec=C_OUT, lw=1.0, hatch="xx",
                             alpha=WK_ALPHA, zorder=4))

        # Wall bracket positions — small rectangles at wall edge
        if is_x_axis:
            # Near/far walkways: brackets along the long wall (Yd=0 or Yd=C_WID)
            x_start = wx
            x_end = wx + ww
            brkt_xs = np.arange(x_start + WALKWAY_BRACKET_SPACING / 2,
                                x_end, WALKWAY_BRACKET_SPACING)
            for bx in brkt_xs:
                is_wide = (name == "NEAR"
                           and WXL <= bx <= WXR)
                bfc = "#CC6644" if is_wide else C_BRKT
                blw = 1.2 if is_wide else 0.6
                if name == "NEAR":
                    ax.add_patch(Rectangle((bx - BRKT_MARK_W / 2, NY),
                                 BRKT_MARK_W, BRKT_MARK_D,
                                 fc=bfc, ec=C_OUT, lw=blw, zorder=6))
                else:
                    ax.add_patch(Rectangle((bx - BRKT_MARK_W / 2, FYO - BRKT_MARK_D),
                                 BRKT_MARK_W, BRKT_MARK_D,
                                 fc=bfc, ec=C_OUT, lw=blw, zorder=6))
        elif name == "RIGHT":
            # Right walkway: cantilever rectangle (rev 12) — show the 2 center
            # arms cantilevering off the IBC corridor uprights toward the long
            # beams, with half-lap marks where they cross.
            arm_w = 40
            arm_yds = [CORRIDOR_YD_NEAR + IBC_FRAME_RHS / 2,
                       CORRIDOR_YD_FAR - IBC_FRAME_RHS / 2]
            for ay in arm_yds:
                ax.add_patch(Rectangle((RX, ay - arm_w / 2),
                             (RXR - RX) + 70, arm_w,
                             fc="#9098A0", ec=C_OUT, lw=0.8, zorder=8, alpha=0.85))
                for bx in [RX, RXR - arm_w]:
                    ax.add_patch(Rectangle((bx, ay - arm_w / 2), arm_w, arm_w,
                                 fc="none", ec=C_OUT, lw=0.7, ls=(0, (2, 1.5)), zorder=9))
        # LEFT walkway: NO brackets — removable lift-out section

        # Section label
        cx = wx + ww * 0.55
        cy = wy + wh * 0.5
        rot = 0 if is_x_axis else 90
        length = ww if is_x_axis else wh
        if name == "LEFT":
            lbl = f"LEFT WALKWAY\n{int(length)}\u00d7{WALKWAY_W}mm\nREMOVABLE LIFT-OUT"
        elif name == "RIGHT":
            lbl = f"RIGHT WALKWAY\n{int(length)}\u00d7{WALKWAY_RIGHT_W}mm\nCANTILEVER"
        elif name == "NEAR":
            lbl = f"NEAR WALKWAY\n{int(length)}\u00d7{WALKWAY_W}mm\n(WIDENED TO {WALKWAY_NEAR_WIDE_W}mm\nAT EP/BATT ZONE)"
        else:
            lbl = f"{name} WALKWAY\n{int(length)}\u00d7{WALKWAY_W}mm"
        ax.text(cx, cy, lbl,
                ha="center", va="center", fontsize=6, color=C_OUT,
                bbox=bbox,
                fontweight="bold", **FONT, zorder=9, rotation=rot)

    # ── Left walkway — removable section marking ──────────────────────────────
    # The left walkway (X 170–470, full Yd depth) is a LIFT-OUT section so the
    # light-trap (cargo panel + drum) can swing ~56° about the pivot for transport.
    # It stays installed for camera operation.
    # Mark it with a dashed orange outline to indicate removable status.
    C_REMOVABLE = "#C06000"   # orange for removable section
    ax.add_patch(Rectangle((LX, NY), W, FYO - NY,
                            fc="none", ec=C_REMOVABLE, lw=2.0, ls=(0, (8, 4)),
                            zorder=13))
    # Leader from left walkway center pointing left (clear of panel swing sweep)
    leader(ax, LX + W / 2, (NY + FYO) / 2,
           LX - 380, (NY + FYO) / 2 + 300,
           f"LEFT WALKWAY — LIFT-OUT SECTION\n"
           f"REMOVE FOR TRANSPORT\n(panel + drum swing 56° about the pivot)",
           color=C_REMOVABLE, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Muslin-drop notches (rev 2026-07-23) ──────────────────────────────────
    # 150(X)×100(Yd) grate notch at the FAR corner of the LEFT + RIGHT walkways where the
    # far walkway butt-joins — the exposed muslin slides from the image plane down into the tray.
    _DX, _DY, _NY0 = WALKWAY_MUSLIN_NOTCH_DX, WALKWAY_MUSLIN_NOTCH_DY, WALKWAY_MUSLIN_NOTCH_YD0
    for _nx0 in (WALKWAY_MUSLIN_NOTCH_L_X0, WALKWAY_MUSLIN_NOTCH_R_X0):
        ax.add_patch(Rectangle((_nx0, _NY0), _DX, _DY, fc="white", ec="none", zorder=14))
        ax.add_patch(Rectangle((_nx0, _NY0), _DX, _DY, fc="none", ec="#B00020",
                               lw=1.6, ls=(0, (4, 2)), zorder=15))
    leader(ax, WALKWAY_MUSLIN_NOTCH_R_X0 + _DX / 2, _NY0 + _DY / 2,
           WALKWAY_MUSLIN_NOTCH_R_X0 + 380, _NY0 - 260,
           f"MUSLIN-DROP NOTCH ({_DX}\u00d7{_DY}mm)\ntray-facing edge, L + R walkways —\nslide muslin from image plane into tray",
           color="#B00020", fs=5.0, ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Drum-exit punch-out ───────────────────────────────────────────────────
    # The left walkway deepens from 300mm to WALKWAY_LEFT_WIDE_W (600mm) in +X
    # over Yd WALKWAY_LEFT_WIDE_YD_L..R, giving a landing where an operator steps
    # out of the light-trap drum.  Cantilever sub-frame off the main bearer (Detail E).
    pX0 = LXR                                  # bump starts at the 470mm edge
    pW  = WALKWAY_LEFT_WIDE_W - W               # extra depth = 300mm (→ X=770)
    pY0 = WALKWAY_LEFT_WIDE_YD_L
    pH  = WALKWAY_LEFT_WIDE_YD_R - WALKWAY_LEFT_WIDE_YD_L
    ax.add_patch(Rectangle((pX0, pY0), pW, pH,
                           fc=C_WK, ec=C_OUT, lw=1.0, hatch="xx",
                           alpha=WK_ALPHA, zorder=5))
    ax.add_patch(Rectangle((pX0, pY0), pW, pH,
                           fc="none", ec="#408040", lw=1.8, ls=(0, (5, 3)),
                           zorder=14))
    ax.text(pX0 + pW / 2, pY0 + pH / 2,
            f"DRUM-EXIT\nPUNCH-OUT\n{WALKWAY_LEFT_WIDE_W}mm DEEP",
            ha="center", va="center", fontsize=5.5, color="#204820",
            fontweight="bold", **FONT, zorder=15, bbox=bbox)
    # Support leg under the cantilevered landing (see support detail sheet)
    leader(ax, pX0 + pW, pY0 + pH / 2,
           pX0 + pW + 360, pY0 + pH / 2 - 360,
           "CANTILEVER SUB-FRAME off the\nX=470 bearer (see Detail E)",
           color="#408040", fs=5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Corner joints ────────────────────────────────────────────────────────
    # All corners are butt joints (same walkway width on all sides)
    # Right corners
    ax.plot([TR, TR], [NY, NYI], color=C_OUT, lw=1.5, zorder=8)   # near-right butt
    ax.plot([TR, TR], [FY, FYO], color=C_OUT, lw=1.5, zorder=8)   # far-right butt
    # Left corners
    ax.plot([LXR, LXR], [NY, NYI], color=C_OUT, lw=1.5, zorder=8)   # near-left butt
    ax.plot([LXR, LXR], [FY, FYO], color=C_OUT, lw=1.5, zorder=8)   # far-left butt

    # Label one butt joint (bottom-left)
    leader(ax, LXR, W / 2, LXR - 350, W / 2 - 350,
           f"BUTT JOINT AT X={LXR}\n(LEFT WALKWAY LIFTS OUT\nCLEARS PANEL TRANSPORT\nENVELOPE AT X\u2264420)",
           color=C_OUT, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # \u2500\u2500 Sheet seams (molded GRP max 3'\u00d710' = 3048mm/panel) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
    # The near & far runs are longer than one sheet, so each is spliced at ONE seam,
    # drawn in dashed RED to distinguish it from the black corner butt joints. The
    # seam is placed past the bump-out shoulder (WXR) so the widening is never a joint.
    GRP_MAX_LEN = 3048
    seam_x = LXR + GRP_MAX_LEN
    if near_len > GRP_MAX_LEN:
        for (y0, y1) in [(NY, NYI), (FY, FYO)]:
            ax.plot([seam_x, seam_x], [y0, y1], color="#B00020", lw=1.4,
                    ls=(0, (4, 2)), zorder=8)
        leader(ax, seam_x, NYI + 20, seam_x + 260, NYI + 360,
               f"SHEET SEAM AT X={int(seam_x)}\n(near/far spliced here \u2014 GRP\nmax 3'\u00d710'; clear of the\nbump-out shoulder at X={int(WXR)})",
               color="#B00020", fs=5.5, ha="center", va="center",
               arrow_style="-|>", font=FONT)

    # Label right walkway cantilever detail
    hanger_lbl_x = RX + W / 2
    leader(ax, hanger_lbl_x + 120, W / 2 + 90,
           hanger_lbl_x + 650, W / 2 + 350,
           "CANTILEVER RECTANGLE\n(2 arms off the IBC uprights +\n"
           "combined corner plates — see Sheet 3)",
           color="#606068", fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Near walkway bump-out annotation ────────────────────────────────────
    bump_cx = (WXL + WXR) / 2
    bump_cy = (NYI + WW) / 2
    ax.text(bump_cx, bump_cy, f"WIDENED TO {WW}mm\n(EP + BATTERY ZONE)",
            ha="center", va="center", fontsize=5.5, color=C_OUT,
            backgroundcolor="#FFFFFF", fontweight="bold", **FONT, zorder=9)
    draw_dim_v(ax, WXL - 40, NY, WW,
               f"{WW}mm", offset=50, fs=6, right=False, font=FONT)
    # Dimension the ACTUAL drawn bump-out (snapped to the widened-bracket ribs WXL_B..WXR_B),
    # not the un-snapped nominal WXL..WXR — otherwise the extension lines and value (1114mm)
    # overshoot the deck edges that are really drawn.
    draw_dim_h(ax, WXL_B, WXR_B, WW + 30,
               f"{int(round(WXR_B - WXL_B))}mm BUMP-OUT", offset=50, fs=6, font=FONT)

    # EP + battery ghost outlines (wall-mounted equipment that drives bump-out)
    C_EQUIP_GHOST = "#808080"
    ax.add_patch(Rectangle((EP_X, NY), EP_W, 120,
                            fc="none", ec=C_EQUIP_GHOST, lw=1.0, ls="--",
                            alpha=0.6, zorder=5))
    ax.text(EP_X + EP_W / 2, 60, "EP", ha="center", va="center",
            fontsize=5, color=C_EQUIP_GHOST, **FONT, zorder=6, alpha=0.6)
    ax.add_patch(Rectangle((BA_X, NY), BA_W, 120,
                            fc="none", ec=C_EQUIP_GHOST, lw=1.0, ls="--",
                            alpha=0.6, zorder=5))
    ax.text(BA_X + BA_W / 2, 60, "BATT", ha="center", va="center",
            fontsize=5, color=C_EQUIP_GHOST, **FONT, bbox=bbox, zorder=6, alpha=0.6)

    # ── Spray bar slit in near & far walkways ──────────────────────────────────
    slit_cx = (PROC_OPEN_X_L + PROC_OPEN_X_R) / 2
    slit_w = SPRAY_BAR_SLIT_W
    C_SLIT = "#CC0000"
    tray_lip = PROC_TRAY_YD_NEAR  # Yd=80mm — slit stops at tray lip

    # Near walkway slit — extends from inner edge to tray lip only
    near_slit_inner = WW if WXL <= slit_cx <= WXR else NYI
    ax.add_patch(Rectangle((slit_cx - slit_w / 2, tray_lip),
                 slit_w, near_slit_inner - tray_lip,
                 fc="#FF4444", ec=C_SLIT, lw=1.5, alpha=0.6, zorder=7))
    # Far walkway slit — extends from inner edge to tray lip only
    far_tray_lip = PROC_TRAY_YD_FAR
    ax.add_patch(Rectangle((slit_cx - slit_w / 2, FY),
                 slit_w, far_tray_lip - FY,
                 fc="#FF4444", ec=C_SLIT, lw=1.5, alpha=0.6, zorder=7))

    leader(ax, slit_cx, NYI + 15,
           slit_cx + 500, NYI + 300,
           f"{slit_w}mm SLIT (NEAR + FAR)\nSPRAY BAR POLE PASSAGE\n(SEE SPRAY BAR ASSEMBLY)",
           color=C_SLIT, fs=5.5,
           ha="left", va="center", arrow_style="-|>", font=FONT)

    # ── Evap cooler transport stowage (on near walkway) ───────────────────────
    C_EVAP_STOW = "#3DAA96"
    ax.add_patch(Rectangle((EVAP_STOW_X, EVAP_STOW_YD),
                            EVAP_W, EVAP_D,
                            fc=C_EVAP_STOW, ec=C_OUT, lw=1.5,
                            alpha=0.35, zorder=7))
    ax.plot([EVAP_STOW_X, EVAP_STOW_X + EVAP_W],
            [EVAP_STOW_YD + EVAP_D / 2, EVAP_STOW_YD + EVAP_D / 2],
            color=C_OUT, lw=0.5, ls="--", alpha=0.4, zorder=7)
    ax.text(EVAP_STOW_X + EVAP_W / 2, EVAP_STOW_YD + EVAP_D / 2,
            f"EVAP COOLER\nTRANSPORT STOW\n{EVAP_W}×{EVAP_D}mm",
            ha="center", va="center", fontsize=5, color=C_OUT,
            fontweight="bold", **FONT, zorder=8)
    # Ratchet strap indicators (two lines across cooler to bracket arms)
    for strap_x in [EVAP_STOW_X + 100, EVAP_STOW_X + EVAP_W - 100]:
        ax.plot([strap_x, strap_x], [NY - 20, EVAP_STOW_YD + EVAP_D + 30],
                color="#CC6600", lw=2.0, ls=(0, (3, 2)), alpha=0.7, zorder=8)
    ax.text(EVAP_STOW_X + EVAP_W + 40, EVAP_STOW_YD + EVAP_D * 0.8,
            "RATCHET\nSTRAPS (×2)\nTO WALL\nBRACKETS",
            ha="left", va="center", fontsize=4.5, color="#CC6600",
            **FONT, bbox=bbox, zorder=8)

    # ── Panel swing sweep (dashed red) ───────────────────────────────────────
    # rev10: the cargo panel + drum SWING ~56° about the Ø89 pivot (PIVOT_X, PIVOT_YD),
    # they no longer slide. The left walkway must lift out before the swing so the
    # swinging cage can transition the X=150 rail line / near-door deck. Shade the
    # sector swept by the SWINGING part's free edge (Yd=PANEL_CUT_YD — the fixed near
    # strip Yd0..180 does NOT swing) — the keep-clear transport zone.
    def _sw(x, y, deg):
        t = np.radians(deg); c, s = np.cos(t), np.sin(t)
        return (PIVOT_X + (x - PIVOT_X) * c - (y - PIVOT_YD) * s,
                PIVOT_YD + (x - PIVOT_X) * s + (y - PIVOT_YD) * c)
    sweep_arc = [_sw(0, PANEL_CUT_YD, d) for d in np.linspace(0, SWING_LOCK_DEG, 28)]
    ax.add_patch(Polygon([(PIVOT_X, PIVOT_YD)] + sweep_arc, closed=True,
                         fc="#FF0000", ec="#CC0000", lw=1.2, ls=(0, (4, 3)),
                         alpha=0.06, zorder=3))
    ax.plot([p[0] for p in sweep_arc], [p[1] for p in sweep_arc],
            color="#CC0000", lw=1.2, ls=(0, (4, 3)), zorder=5)
    ax.add_patch(Circle((PIVOT_X, PIVOT_YD), 48, fc="#CC0000", ec=C_OUT,
                        lw=1.0, zorder=6))
    ax.text(PIVOT_X + 90, PIVOT_YD, "\u00d889 PIVOT", ha="left", va="center",
            fontsize=5.5, color="#CC0000", **FONT, bbox=bbox, zorder=8)
    _mid = sweep_arc[int(len(sweep_arc) * 0.55)]
    ax.text(_mid[0] + 750, _mid[1] + 350,
            f"PANEL SWING SWEEP {int(SWING_LOCK_DEG)}\u00b0\n(keep clear \u2014 left walkway lifts out)",
            ha="center", va="center", fontsize=6, color="#CC0000",
            fontweight="bold", **FONT, zorder=15, alpha=0.85,
            backgroundcolor="#FFFFFF")

    # ── Open processing area outline ─────────────────────────────────────────
    open_w = PROC_OPEN_X_R - PROC_OPEN_X_L
    open_h = PROC_OPEN_YD_F - PROC_OPEN_YD_N
    ax.add_patch(Rectangle((PROC_OPEN_X_L, PROC_OPEN_YD_N),
                            open_w, open_h,
                            fc="none", ec="#208020", lw=1.5, ls=(0, (6, 3)),
                            zorder=5))
    ax.text(PROC_OPEN_X_L + open_w / 2, PROC_OPEN_YD_N + open_h / 2.25,
            f"OPEN PROCESSING AREA\n{open_w}\u00d7{open_h}mm = {PROC_OPEN_AREA:.1f} m\u00b2",
            ha="center", va="center", fontsize=7, color="#208020",
            **FONT, zorder=5, alpha=0.6)

    # ── Left walkway support — FLOOR-LEG CANTILEVER brackets (plan) ──
    C_SUPPORT = "#D08020"   # orange for support elements
    leg_x = LEFT_WK_CANT_LEG_X                 # 140 (bare floor, outside tray)
    arm_x0 = leg_x + LEFT_WK_CANT_POST / 2     # 165
    leg_sz = 24
    for cy in LEFT_WK_CANT_LEG_YDS:
        wide_b = WALKWAY_LEFT_WIDE_YD_L <= cy <= WALKWAY_LEFT_WIDE_YD_R
        reach = LEFT_WK_CANT_WIDE_REACH if wide_b else LEFT_WK_CANT_STD_REACH
        aw = 16 if wide_b else 10
        # cantilever arm to the grate inner edge (X470) / punch-out (X770)
        ax.add_patch(Rectangle((arm_x0, cy - aw / 2), reach - arm_x0, aw,
                     fc=C_SUPPORT, ec=C_OUT, lw=0.6, alpha=0.7, zorder=8))
        # foot/post marker on the floor
        ax.add_patch(Rectangle((leg_x - leg_sz / 2, cy - leg_sz / 2), leg_sz, leg_sz,
                     fc=C_SUPPORT, ec=C_OUT, lw=0.8, zorder=9))
    leader(ax, leg_x, LEFT_WK_CANT_LEG_YDS[0] + leg_sz / 2 + 5,
           leg_x - 300, LEFT_WK_CANT_LEG_YDS[0] + 180,
           "FLOOR-LEG CANTILEVER\nBRACKETS (x5) on BARE FLOOR (X140)\narms reach to X470 (3 extend to X770)",
           color=C_SUPPORT, fs=5.5, ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Dimension lines ──────────────────────────────────────────────────────
    # Walkway width dimension (near walkway)
    draw_dim_v(ax, PROC_TRAY_X_L - 90, WALKWAY_NEAR_YD, WALKWAY_NEAR_YD + WALKWAY_W,
               f"{WALKWAY_W}mm", offset=50, fs=6, right=True, font=FONT)

    # Bracket spacing callout
    # Find two adjacent bracket positions on near walkway for dimensioning
    # Match the drawn near-walkway bracket grid: markers start at LXR + spacing/2 (the walkway
    # origin, X=470), NOT the tray-left TL — otherwise the dim sits offset from the ribs.
    brkt_x0 = LXR + WALKWAY_BRACKET_SPACING / 2
    brkt_x1 = brkt_x0 + WALKWAY_BRACKET_SPACING
    draw_dim_h(ax, brkt_x0, brkt_x1, -40,
               f"{WALKWAY_BRACKET_SPACING}mm BRACKET SPACING (TYP.)",
               offset=50, fs=6, above=False, font=FONT)

    # ── Legend ────────────────────────────────────────────────────────────────
    draw_legend(ax, [
        (C_WK,         WK_ALPHA, "xx",  "Walkway (grated deck) — lowered to Z=65mm"),
        (C_REMOVABLE,  0.6,      None,  "Left walkway — removable lift-out (dashed orange outline)"),
        ("#E8F0FF",    0.3,      None,  "Processing tray"),
        (C_BRKT,     1.0,      None,  f"Wall bracket ({WALKWAY_BRACKET_T}mm std)"),
        ("#CC6644",  1.0,      None,  f"Widened bracket ({WALKWAY_WIDE_BRACKET_T}mm, 500mm arm)"),
        (C_SUPPORT,  0.8,      None,  f"Floor-leg cantilever bracket (x5, removable grate)"),
        ("#3DAA96",  0.35,     None,  f"Evap cooler transport stowage ({EVAP_W}×{EVAP_D}mm)"),
        ("#FF4444",  0.6,      None,  f"Spray bar slit ({SPRAY_BAR_SLIT_W}mm, near + far)"),
        ("#FF0000",  0.06,     None,  "Panel swing sweep (transport keep-clear)"),
        ("#CC6600",  0.7,      None,  "Ratchet strap (transport securing)"),
    ], C_LEN - 1525, C_WID + PAD_Y_TOP - 2850, pad=35, col_w=1400, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    n_brackets_near = len(np.arange(LXR + WALKWAY_BRACKET_SPACING / 2,
                                     TR, WALKWAY_BRACKET_SPACING))
    n_brackets_total = n_brackets_near * 2  # near + far only (no right brackets)
    notes = [
        "CONSTRUCTION NOTES:",
        f"1. 4 removable grated sections, {WALKWAY_W}mm wide standard. Butt joints ONLY at the 4 corners;",
        f"   the bump-out + drum-exit widenings are INTEGRAL (cut as one piece, no mid-deck joint).",
        f"2. Near walkway WIDENED to {WALKWAY_NEAR_WIDE_W}mm at X={WXL}\u2013{WXR} (clears EP + battery bank) \u2014 an",
        f"   integral inboard tab, not a bolted-on section. Deeper cantilever brackets ({WALKWAY_NEAR_WIDE_W}mm arm)",
        f"   with heavier gussets carry the bump-out; the near deck is >3m so it splits at ONE sheet",
        f"   seam placed away from the bump shoulders (molded GRP max 3'\u00d710').",
        f"3. Near/far: wall-cantilevered brackets ({WALKWAY_BRACKET_T}mm gussets) at {WALKWAY_BRACKET_SPACING}mm centers.",
        f"   Start at X={LXR} (butt joint), clear of the door-end panel swing sweep.",
        f"4. Right: CANTILEVER RECTANGLE \u2014 closed 2\u00d71in-tube frame on 2 arms off the IBC uprights + combined corner plates.",
        f"5. Left: REMOVABLE LIFT-OUT \u2014 5 FLOOR-LEG CANTILEVER brackets on bare floor (X140, outside tray),",
        f"   arms reach the grate inner edge (X={LXR}); 3 extend to X770 on the drum-exit punch-out. See sheets 5/6.",
        f"6. ZERO tray contact \u2014 all supports outside or above tray. Open area: {PROC_OPEN_AREA:.1f} m\u00b2.",
        f"7. ~{n_brackets_total} wall brackets (near + far). Each grating section lifts off for tray access.",
        f"8. SPRAY BAR SLIT: {SPRAY_BAR_SLIT_W}mm slot at beam center X={int((PROC_OPEN_X_L + PROC_OPEN_X_R) / 2)} in near + far walkway",
        f"   grating for telescoping pole passage. See Spray Bar Assembly drawings.",
        f"9. EVAP COOLER TRANSPORT: stow on near walkway (X={EVAP_STOW_X}–{EVAP_STOW_X + EVAP_W}mm),",
        f"   ply base plate on grating, 2× ratchet straps to wall brackets. ~20 kg dry.",
        f"10. WIDENED BRACKETS ({len(_wide_brkt)}): {WALKWAY_WIDE_BRACKET_T}mm plate, {WALKWAY_WIDE_BRACKET_H}mm vert leg, 4× M12 rectangular",
        f"    pattern. 500mm arm reach for EP + battery access. See Sheet 2 View C.",
        f"11. LOWERED DECK: deck top at Z={WALKWAY_H}mm; {WALKWAY_GRATE_T}mm grate bottom at Z=65, bracket arm",
        f"    clears the {PROC_TRAY_RIM}mm tray rim by 5mm. Film-plane frame bottom at Z=100mm gives {100 - WALKWAY_H}mm clearance.",
        f"    Walkway stays installed during camera operation.",
        f"12. LEFT WALKWAY — LIFT-OUT: remove before the light-trap (panel + drum) swings",
        f"    ~{SWING_LOCK_DEG}° about the pivot for transport. Reinstall for operation. See Sheet 4.",
        f"13. DOOR-END BRACKETS STAY BOLTED: the swing rides Z{PANEL_FLOOR_GAP} — the cage underside",
        f"    passes OVER the Z115 bracket tops, so no bracket is struck for transport (rev10).",
    ]
    draw_notes(ax, notes, 1100,
               -PAD_Y_BOT + 450 + (len(notes) - 1) * 44,
               spacing=44, fs=7, width=3000, font=FONT)

    # ── DATUMS & TOLERANCES callout (Phase C) ────────────────────────────────
    dt_lines = [
        "DATUMS & TOLERANCES",
        "A  floor plane (all Z)   ·   B  the two long wall faces (all Yd)",
        f"C  film-plane rail datum  X{int(RAIL_X_L)} / X{int(RAIL_X_R)}  (right corner + combined plate)",
        "GENERAL: ISO 13920 Class B   ·   WELDS: AWS D1.1",
        "Functional: deck coplanarity (A) ±2  ·  wall-bolt pattern (B) ±0.5",
        f"  combined corner seat Z (A+C) ±1  ·  beam soffit Z{WALKWAY_BRACKET_ARM_Z0:.1f} (A) +2/−0",
        "  spray-bar slit (C) ±2  ·  foot-anchor pattern (A) ±1   ·   §10.3",
    ]
    ax.text(-280, -1010, "\n".join(dt_lines), ha="left", va="top", fontsize=6.5,
            color=C_OUT, **FONT, zorder=16,
            bbox=dict(boxstyle="round,pad=0.6", fc="#F4F4F0", ec=C_OUT, lw=1.0))

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 10",
                drawing_title="PERIMETER WALKWAY",
                subtitle="PLAN VIEW \u2014 BRACKET LAYOUT + LEFT WALKWAY SUPPORT",
                scale_note=f"Axes in mm \u00b7 BRACKETS AT {WALKWAY_BRACKET_SPACING}mm CENTERS",
                height=0.06)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "walkway-sheet1.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet1.png saved")

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Cross-Section + Bolt Pattern
#
# Two-panel layout:
#   VIEW A (left): Standard bracket cross-section (300mm arm, 8mm plate).
#     Horizontal = Yd (0 = pinhole wall, positive toward far wall)
#     Vertical   = Z  (0 = floor, positive up)
#   VIEW B (right): Plate face looking along −Yd — triangular
#     bolt pattern on vertical mounting plate with gusset footprint.
# Scale ≈ 5:1 for clarity.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():

    # ── Structural dimensions (mm real) ──────────────────────────────────────
    TRAY_WALL  = 3     # tray wall thickness (SS)
    TRAY_FLOOR = 2     # tray floor thickness (SS)
    CORR_DEPTH = 38    # corrugation depth (mm)
    WALL_T     = 1.6   # wall steel thickness (mm)
    BRKT_ARM_H = WALKWAY_H - WALKWAY_GRATE_T  # = 65mm (bracket arm top Z)
    BRKT_T     = WALKWAY_BRACKET_T  # 8mm plate thickness
    BRKT_VERT  = WALKWAY_BRACKET_H  # 150mm vertical leg on wall
    REINF_W    = WALKWAY_REINF_W   # reinforcing plate width (covers triangular bolt pattern)
    REINF_H    = WALKWAY_REINF_H   # reinforcing plate height
    REINF_T    = WALKWAY_REINF_T   # reinforcing plate thickness

    # Positions (mm real)
    TRAY_RIM_YD = PROC_TRAY_YD_NEAR  # = 80mm from wall

    # ── Figure ───────────────────────────────────────────────────────────────
    YD_LO = -100
    YD_HI = WALKWAY_W + 180
    Z_LO  = -70
    Z_HI  = WALKWAY_H + WALKWAY_GRATE_T + 80

    from matplotlib.gridspec import GridSpec
    fig = plt.figure(figsize=(22, 12))
    gs = GridSpec(1, 2, figure=fig, width_ratios=[2.2, 1], wspace=0.08)
    ax  = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim((YD_LO), (YD_HI))
    ax.set_ylim((Z_LO), (Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # View A title
    ax.text((YD_HI / 2), (Z_HI - 5),
            "VIEW A — CROSS-SECTION AT BRACKET (LOOKING ALONG X)",
            ha="center", va="top", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── Container floor ──────────────────────────────────────────────────────
    ax.add_patch(Rectangle(((YD_LO), (-15)), (YD_HI - YD_LO), (15),
                            fc=C_FLOOR, ec=C_OUT, lw=1.0, hatch="///", zorder=2))

    # ── Corrugated wall (cross-section through rib — HOLLOW profile) ─────────
    # Matching sheet 3 convention: exterior panel, air gap, rib side walls, rib face
    wall_z_top = Z_HI
    ext_panel_yd = -CORR_DEPTH - WALL_T

    # Exterior wall steel panel (full height)
    ax.add_patch(Rectangle(((ext_panel_yd), (0)),
                            (WALL_T), (wall_z_top),
                            fc="#909098", ec=C_OUT, lw=1.2, zorder=3,
                            hatch="///"))
    # Rib side wall (connecting exterior panel to rib face)
    ax.add_patch(Rectangle(((-CORR_DEPTH), (0)),
                            (WALL_T), (wall_z_top),
                            fc="#909098", ec=C_OUT, lw=0.8, zorder=3,
                            hatch="///"))
    # Rib interior face (flange — where bracket bolts on)
    ax.add_patch(Rectangle(((-WALL_T), (0)),
                            (WALL_T), (wall_z_top),
                            fc="#909098", ec=C_OUT, lw=1.2, zorder=3,
                            hatch="///"))
    # Air gap inside the rib (light fill to show it's hollow)
    ax.add_patch(Rectangle(((-CORR_DEPTH + WALL_T), (0)),
                            (CORR_DEPTH - 2 * WALL_T), (wall_z_top),
                            fc="#F0F0F0", ec="none", lw=0, zorder=2))
    ax.add_patch(Rectangle(((-CORR_DEPTH + WALL_T), (0)),
                            (CORR_DEPTH - 2 * WALL_T), (wall_z_top),
                            fc="none", ec=C_DIM, lw=0.5, ls="--", zorder=3))
    ax.text((-CORR_DEPTH / 2), (wall_z_top * 0.45),
            "AIR\nGAP",
            ha="center", va="center", fontsize=6, color=C_DIM,
            **FONT, zorder=15, style="italic")
    # Rib face (interior surface at Yd=0)
    ax.plot([(0), (0)], [(0), (wall_z_top)],
            color=C_OUT, lw=2.0, zorder=4)
    ax.text((-CORR_DEPTH / 2), (wall_z_top - 8),
            "CORRUGATED\nWALL RIB\n(1.6mm CORTEN\nHOLLOW PROFILE)",
            ha="center", va="top", fontsize=5.5, color=C_DIM,
            fontweight="bold", **FONT, zorder=15)

    # ── Reinforcing plate (bonded to exterior wall face) ─────────────────────
    reinf_yd = ext_panel_yd - REINF_T
    ax.add_patch(Rectangle(((reinf_yd), (0)),
                            (REINF_T), (REINF_H),
                            fc="#C08040", ec=C_OUT, lw=1.0, zorder=4))
    leader(ax, (reinf_yd - 1), (REINF_H * 0.8),
           (reinf_yd - 25), (REINF_H),
           f"REINFORCING\nPLATE\n{REINF_W}\u00d7{REINF_H}\n\u00d7{REINF_T}mm\n(EXTERIOR)",
           color="#C08040", fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Processing tray ──────────────────────────────────────────────────────
    # Tray near rim (vertical wall at Yd=TRAY_RIM_YD)
    ax.add_patch(Rectangle(((TRAY_RIM_YD - TRAY_WALL), (0)),
                            (TRAY_WALL), (PROC_TRAY_RIM),
                            fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=4))
    # Tray floor (extends inward from rim)
    tray_floor_start = TRAY_RIM_YD
    tray_floor_end = YD_HI - 20
    ax.add_patch(Rectangle(((tray_floor_start), (0)),
                            (tray_floor_end - tray_floor_start), (TRAY_FLOOR),
                            fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))
    # Tray rim label
    leader(ax, (TRAY_RIM_YD - 5), (PROC_TRAY_RIM / 2 + 20),
           (TRAY_RIM_YD - 20), (PROC_TRAY_RIM + 10),
           f"TRAY RIM\n{PROC_TRAY_RIM}mm\n(304 SS, 3mm)", color=C_TRAY, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)
    # Sawtooth break line on tray floor (continues right)
    bx = (tray_floor_end)
    z_lo, z_hi = 0, TRAY_FLOOR
    zz = np.linspace(z_lo, z_hi, 5)
    ax.plot([bx - 3, bx + 3, bx - 3, bx + 3, bx - 3],
            zz, color=C_OUT, lw=1.0, zorder=5)

    # Tray "water level" indication (wavy line at ~15mm)
    water_h = 15
    wave_x = np.linspace((TRAY_RIM_YD + 5), (tray_floor_end - 10), 40)
    wave_y = (water_h) + 3 * np.sin(wave_x * 0.08)
    ax.plot(wave_x, wave_y, color="#4080C0", lw=1.0, alpha=0.6, zorder=4)
    ax.text((TRAY_RIM_YD + 60), (water_h + 5),
            "PROCESS WATER\n(~15mm depth)",
            ha="left", va="bottom", fontsize=5.5, color="#4080C0",
            **FONT, alpha=0.7, zorder=15)

    # ── Cantilever bracket (3-piece: vertical plate + arm + gusset underneath) ─
    # The bracket is three welded pieces:
    #   1. Vertical mounting plate: flat against wall, Z=0 to BRKT_VERT (150mm)
    #      — bolted to wall rib, does NOT project into tray zone
    #   2. Horizontal arm: welded to vertical plate at Z=BRKT_ARM_H (65mm),
    #      projects inward 300mm — ABOVE the 50mm tray rim
    #   3. Gusset underneath the arm: right triangle bracing the arm from below,
    #      extends 70mm from wall (stops before tray rim at Yd=80mm).
    #      Vertices: wall/floor (0,0), wall/arm-bottom (0, arm_bot), (70, arm_bot).

    brkt_arm_z = BRKT_ARM_H  # top of horizontal arm = grate support (Z115)
    ARM_DEPTH  = WALKWAY_BRACKET_ARM_H  # 25.4 — arm is a 2×1×0.120 tube (redesign; was an 8mm plate edge)
    arm_bot    = brkt_arm_z - ARM_DEPTH  # bottom of arm (Z89.6)
    GUSSET_REACH = WALKWAY_GUSSET_REACH  # gusset extends 70mm from wall (< 80mm tray rim position)

    # 1. Vertical mounting plate (flat against rib interior face, Yd=0 to BRKT_T)
    ax.add_patch(Rectangle(((0), (0)),
                            (BRKT_T), (BRKT_VERT),
                            fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=6, alpha=0.85))

    # 2. Horizontal arm (projects inward at Z=brkt_arm_z)
    ax.add_patch(Rectangle(((0), (arm_bot)),
                            (WALKWAY_W), (ARM_DEPTH),
                            fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=6, alpha=0.85))
    # Arm top surface (where grate sits) — emphasize
    ax.plot([(0), (WALKWAY_W)], [(brkt_arm_z), (brkt_arm_z)],
            color=C_OUT, lw=2.0, zorder=7)

    # 3. Gusset UNDERNEATH the arm — right triangle bracing from below
    # Stops at Yd=70mm, before the tray rim at Yd=80mm
    gusset_verts = [
        ((0), (0)),                   # wall at floor level
        ((0), (arm_bot)),             # wall at arm bottom
        ((GUSSET_REACH), (arm_bot)),  # 70mm out along arm bottom
    ]
    ax.add_patch(Polygon(gusset_verts, closed=True,
                         fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=5, alpha=0.85))
    # Diagonal edge emphasis (hypotenuse)
    ax.plot([(0), (GUSSET_REACH)], [(0), (arm_bot)],
            color=C_OUT, lw=1.5, zorder=6)

    # Weld symbol at gusset-to-arm joint
    weld_x = GUSSET_REACH / 3
    ax.plot([(weld_x - 4), (weld_x), (weld_x + 4)],
            [(arm_bot), (arm_bot - 5), (arm_bot)],
            color="#CC4400", lw=1.5, zorder=8)
    ax.text((weld_x), (arm_bot - 7), "WELD WW1/WW3\n(§10.2)",
            ha="center", va="top", fontsize=4.5, color="#CC4400",
            **FONT, zorder=15)

    # Through-bolts (3× M12) — horizontal shanks through wall + bracket
    # Triangular pattern: 2× lower (flanking gusset in X), 1× upper (centered)
    # In this side view (along X), the two lower bolts overlap — shown as one + "2×" label
    BOLT_D    = 12
    BOLT_R    = BOLT_D / 2
    BOLT_HEAD = 8    # hex head height (Yd direction)
    NUT_H     = 10   # nut height (Yd direction)
    WASHER_T  = 3
    C_BOLT    = "#505058"
    bolt_z_lo = WALKWAY_BRACKET_BOLT_Z_LO   # 42 — lower pair, flanking gusset in X at ±WALKWAY_BRACKET_BOLT_DX (27mm, standard bracket) from CL (matches the 3D pattern)
    bolt_z_hi = WALKWAY_BRACKET_UPPER_BOLT_Z  # = 155 — SHARED with sheet7 + the 3D; clears the grate deck top (Z140)

    for bz in [bolt_z_lo, bolt_z_hi]:
        shank_hw = BOLT_R * 0.4  # half-width of shank in Z
        # Bolt shank — from reinf plate through to bracket face
        ax.add_patch(Rectangle(((reinf_yd), (bz - shank_hw)),
                                (BRKT_T - reinf_yd), (shank_hw * 2),
                                fc=C_BOLT, ec=C_OUT, lw=0.8, zorder=10))
        # Hex head on exterior side (left of reinforcing plate)
        ax.add_patch(Rectangle(((reinf_yd - BOLT_HEAD), (bz - BOLT_R)),
                                (BOLT_HEAD), (BOLT_D),
                                fc=C_BOLT, ec=C_OUT, lw=1.0, zorder=10))
        # Washer under head
        ax.add_patch(Rectangle(((reinf_yd - WASHER_T), (bz - BOLT_R - 1)),
                                (WASHER_T), (BOLT_D + 2),
                                fc="#808080", ec=C_OUT, lw=0.5, zorder=9))
        # Nut on interior side (right of bracket plate)
        ax.add_patch(Rectangle(((BRKT_T), (bz - BOLT_R)),
                                (NUT_H), (BOLT_D),
                                fc=C_BOLT, ec=C_OUT, lw=1.0, zorder=10))
        # Washer under nut
        ax.add_patch(Rectangle(((BRKT_T), (bz - BOLT_R - 1)),
                                (WASHER_T), (BOLT_D + 2),
                                fc="#808080", ec=C_OUT, lw=0.5, zorder=9))

    # Bracket label — point at the arm
    leader(ax, (WALKWAY_W * 0.4), (brkt_arm_z - 5),
           (WALKWAY_W * 0.4 + 50), (brkt_arm_z - 30),
           f"CANTILEVER BRACKET\n{BRKT_T}mm PLATE (vert leg + gusset)\n+ 2×1×0.120 TUBE ARM\n(50.8×25.4, welded on)",
           color=C_BRKT, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # Gusset label
    leader(ax, (GUSSET_REACH / 2), (arm_bot / 2 - 5),
           (GUSSET_REACH-20), (arm_bot / 2 - 25),
           f"GUSSET ({GUSSET_REACH}mm)\nSTOPS BEFORE\nTRAY RIM",
           color=C_BRKT, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # Bolt labels
    leader(ax, (reinf_yd - BOLT_HEAD - 2), (bolt_z_lo),
           (reinf_yd - 30), (bolt_z_lo + 20),
           f"WF1 \u00b7 2\u00d7 M12 AT Z={bolt_z_lo}\n(STRADDLE GUSSET\nIN X \u2014 SEE VIEW B)",
           color=C_DIM, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)
    leader(ax, (reinf_yd - BOLT_HEAD - 2), (bolt_z_hi),
           (reinf_yd - 30), (bolt_z_hi + 20),
           f"1\u00d7 M12 AT Z={bolt_z_hi}\n(ON GUSSET CL\nIN X \u2014 SEE VIEW B)",
           color=C_DIM, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Grated deck ──────────────────────────────────────────────────────────
    # Grating sits on bracket arm: bottom at BRKT_ARM_H (65mm), top at WALKWAY_H (80mm)
    grate_bot = brkt_arm_z  # = 65mm
    grate_top = grate_bot + WALKWAY_GRATE_T  # = 80mm = WALKWAY_H
    ax.add_patch(Rectangle(((BRKT_T), (grate_bot)),
                            (WALKWAY_W - BRKT_T), (WALKWAY_GRATE_T),
                            fc=C_GRATE, ec=C_OUT, lw=1.2, zorder=7))
    # Grate pattern (vertical bars in cross-section)
    bar_spacing = 34.2  # ~34mm bearing bar pitch (standard)
    bar_w = 3           # bearing bar thickness
    for yd in np.arange(BRKT_T + bar_w, WALKWAY_W - bar_w, bar_spacing):
        ax.add_patch(Rectangle(((yd), (grate_bot)),
                                (bar_w), (WALKWAY_GRATE_T),
                                fc="#909098", ec=C_OUT, lw=0.3, zorder=8))
    # Cross bars (twist-locked — shown as small rectangles at mid-height)
    cross_h = 3
    for yd in np.arange(BRKT_T + bar_spacing / 2, WALKWAY_W, bar_spacing):
        ax.add_patch(Rectangle(((yd - 1), (grate_bot + WALKWAY_GRATE_T / 2 - cross_h / 2)),
                                (2), (cross_h),
                                fc="#808088", ec="none", zorder=9, alpha=0.7))

    leader(ax, (WALKWAY_W / 4), ((grate_bot + grate_top) / 2),
           (WALKWAY_W / 4 - 30), (grate_top + 35),
           f"MOLDED GRP (FIBERGLASS) GRATING\n{WALKWAY_GRATE_T}mm \u00b7 VINYL-ESTER \u00b7 GRIT TOP",
           color=C_OUT, fs=6, ha="center", va="center",
           arrow_style="-|>", font=FONT)

    # ── Grating clip (innermost edge, closest to processing tray) ──────────
    clip_yd = WALKWAY_W - 20
    clip_w = 8
    clip_below = 12   # extends below arm top
    clip_above = 5    # extends above grate top
    clip_bot = brkt_arm_z - clip_below
    clip_top = grate_top + clip_above
    ax.add_patch(Rectangle(((clip_yd), (clip_bot)),
                            (clip_w), (clip_top - clip_bot),
                            fc="#505058", ec=C_OUT, lw=0.8, zorder=9))
    leader(ax, (clip_yd + clip_w), (brkt_arm_z),
           (clip_yd + 30), (brkt_arm_z + 55),
           "316 SS HOLD-DOWN\nCLIP + BOLT", color="#505058", fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Clear tray area annotation ───────────────────────────────────────────
    # Arrow showing clear air under the entire walkway — no legs, no beam
    clr_x = (WALKWAY_W * 0.7)
    ax.annotate("", xy=(clr_x, (TRAY_FLOOR + 1)), xytext=(clr_x, (arm_bot - 1)),
                arrowprops=dict(arrowstyle="<->", color="#208020", lw=1.2, mutation_scale=8))
    gap_mm = arm_bot - TRAY_FLOOR   # clear air below the arm UNDERSIDE (the lowest obstruction)
    ax.text(clr_x + (5), ((TRAY_FLOOR + brkt_arm_z) / 2),
            f"{gap_mm:.0f}mm\nCLEAR AIR\n(NO LEGS,\nNO BEAM —\nFILM LAYS\nFLAT HERE)",
            ha="left", va="center", fontsize=5, color="#208020",
            fontweight="bold", **FONT, zorder=15, alpha=0.8)

    # ── Dimension lines ──────────────────────────────────────────────────────
    # Walkway width (= bracket arm cantilever)
    draw_dim_h(ax, (0), (WALKWAY_W), (grate_top + 55),
               f"{WALKWAY_W}mm WALKWAY WIDTH", offset=(8), fs=7, font=FONT)

    # Deck height (floor to grate top)
    draw_dim_v(ax, (WALKWAY_W + 22), (0), (grate_top),
               f"{WALKWAY_H}mm DECK TOP", offset=(6), fs=7, right=True, font=FONT)

    # Grate thickness
    draw_dim_v(ax, (WALKWAY_W + 5), (grate_bot), (grate_top),
               f"{WALKWAY_GRATE_T}mm DECK\nHEIGHT", offset=(8), fs=6.5, right=True, font=FONT)

    # Bracket vertical leg height
    draw_dim_v(ax, (reinf_yd - BOLT_HEAD - 45), (0), (BRKT_VERT),
               f"{BRKT_VERT}mm VERT LEG", offset=(8), fs=6.5, right=False, font=FONT)

    # Bracket arm height
    draw_dim_v(ax, (WALKWAY_W + 5), (0), (brkt_arm_z),
               f"{brkt_arm_z}mm ARM TOP", offset=(8), fs=6.5, right=True, font=FONT)

    # Tray rim height
    draw_dim_v(ax, (TRAY_RIM_YD + 15), (0), (PROC_TRAY_RIM),
               f"{PROC_TRAY_RIM}mm", offset=(8), fs=6.5, right=True,
               color=C_TRAY, font=FONT)

    # Clearance above rim (grate bottom to rim top)
    clr = grate_bot - PROC_TRAY_RIM
    draw_dim_v(ax, (TRAY_RIM_YD + 15), (PROC_TRAY_RIM), (grate_bot),
               f"{clr}mm\nCLR", offset=(8), fs=6.5, right=True,
               color="#208020", font=FONT)

    # Corrugation depth
    draw_dim_h(ax, (-CORR_DEPTH), (0), (-22),
               f"{CORR_DEPTH}mm\nCORR", offset=(10), fs=6, above=False, font=FONT)

    # Wall to tray rim
    draw_dim_h(ax, (0), (TRAY_RIM_YD), (-35),
               f"{TRAY_RIM_YD}mm", offset=(10), fs=6, above=False, font=FONT)

    # ── Operator shoes (pair, US size 9 = ~270mm long × 100mm wide) ────────
    # In this cross-section (looking along X), shoes appear as their width
    # (100mm along Yd) × sole height (~15mm along Z). Show two shoes
    # side-by-side with a small gap between them.
    SHOE_W = 100   # shoe width (mm) — visible in Yd cross-section
    SHOE_H = 15    # sole height (mm)
    SHOE_GAP = 20  # gap between shoes (mm)
    shoe_pair_w = 2 * SHOE_W + SHOE_GAP
    shoe_start = (WALKWAY_W - shoe_pair_w) / 2  # center pair on walkway
    shoe_z = grate_top

    for i in range(2):
        s_yd = shoe_start + i * (SHOE_W + SHOE_GAP)
        # Shoe sole (yellow ghost)
        ax.add_patch(Rectangle(
            ((s_yd), (shoe_z)), (SHOE_W), (SHOE_H),
            fc="#FFD700", ec="#B89600", lw=0.6,
            zorder=10, alpha=0.3, ls="--"))

    # Shoe length annotation (into-page dimension, since shoes point along X)
    ax.text((WALKWAY_W / 2), (shoe_z + SHOE_H + 6),
            "US 9 SHOE PAIR\n(270mm LONG \u00d7 100mm WIDE)",
            ha="center", va="bottom", fontsize=5.5, color="#404040",
            **FONT, zorder=15, alpha=0.7)
    leader(ax, (shoe_start + SHOE_W / 2), (shoe_z + SHOE_H),
           (95), (shoe_z + SHOE_H + 15),
           "OPERATOR\nSTANDING", color=C_TRAY, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Axis labels ──────────────────────────────────────────────────────────
    ax.text((YD_HI / 2), (Z_LO + 5),
            "Yd  (container width, 0 = pinhole wall)  \u2192",
            ha="center", va="bottom", fontsize=6.5, color=C_DIM,
            **FONT, zorder=15, style="italic")

    # ── Notes ────────────────────────────────────────────────────────────────
    notes_x = (WALKWAY_W + 40)
    notes_top = (Z_HI - 10)
    notes = [
        "CONSTRUCTION NOTES:",
        "",
        f"1. Grating: {WALKWAY_GRATE_T}mm molded GRP (fiberglass),",
         "   vinyl-ester resin, grit top. Corrosion-proof",
         "   in the wet chemistry zone.",
        f"2. Cantilever brackets: {BRKT_T}mm plate (vert leg +",
        f"   gusset) + 2×1×0.120 tube arm, bolted to wall",
        f"   ribs at {WALKWAY_BRACKET_SPACING}mm centers.",
        f"3. Rib is HOLLOW — bolt bridges the air gap.",
        f"   Path: head \u2192 reinf plate \u2192 ext panel",
        f"   \u2192 air gap \u2192 rib face \u2192 bracket",
         "   \u2192 nut.",
        f"4. Reinforcing plate welded to exterior panel",
        f"   face. Bearing surface for bolt head + ",
         "   washer.",
        f"5. Gusset reach stops before tray rim at",
        f"   {PROC_TRAY_YD_NEAR}mm.",
        f"6. NO legs, NO beam — entire tray floor clear",
        f"   for film loading. Zero tray contact.",
        f"7. 316 SS hold-down clips + bolts to bracket",
         "   arms.",
        f"8. Right walkway: CANTILEVER RECTANGLE off the",
        f"   IBC frame + combined corner plates. See Sheet 3.",
        f"9. Left walkway: REMOVABLE LIFT-OUT —",
        f"   no brackets (panel conflict). Rests on",
        f"   near/far butt joints. {WALKWAY_GRATE_T}mm grating.",
    ]
    draw_notes(ax, notes, notes_x, notes_top, spacing=(6), fs=7, width=(150), font=FONT)

    # ══════════════════════════════════════════════════════════════════════════
    # VIEW B — Plate face (looking along −Yd, toward wall)
    # Horizontal = X (bracket width), Vertical = Z (height)
    # Shows triangular bolt pattern on the vertical mounting plate
    # ══════════════════════════════════════════════════════════════════════════
    ax2.set_facecolor(BG)

    BOLT_X_OFF = WALKWAY_BRACKET_BOLT_DX   # 27 — standard-bracket lower-bolt X offset (single-sourced; matches the 3D)
    HOLE_D = 14
    HOLE_R_B = HOLE_D / 2

    PL_X_LO = -REINF_W / 2 - 55
    PL_X_HI =  REINF_W / 2 + 65
    PL_Z_LO = -40
    PL_Z_HI =  BRKT_VERT + 55
    ax2.set_xlim(PL_X_LO, PL_X_HI)
    ax2.set_ylim(PL_Z_LO, PL_Z_HI)
    ax2.set_aspect("equal")
    ax2.axis("off")

    ax2.text(0, PL_Z_HI - 5,
             "VIEW B — PLATE FACE (−Yd)",
             ha="center", va="top", fontsize=8, color=C_OUT,
             fontweight="bold", **FONT, zorder=15)

    cx2 = 0
    pl2 = cx2 - REINF_W / 2
    pr2 = cx2 + REINF_W / 2

    ax2.add_patch(Rectangle((pl2, 0), REINF_W, BRKT_VERT,
                             fc=C_BRKT, ec=C_OUT, lw=2.0, zorder=5, alpha=0.85))

    gusset_hw = BRKT_T / 2
    gusset_fp = [
        (cx2 - gusset_hw, 0),
        (cx2 - gusset_hw, arm_bot),
        (cx2 + gusset_hw, arm_bot),
        (cx2 + gusset_hw, 0),
    ]
    ax2.add_patch(Polygon(gusset_fp, closed=True,
                          fc="#606870", ec=C_OUT, lw=1.0, ls="--",
                          zorder=6, alpha=0.5))
    ax2.text(cx2, arm_bot / 2,
             f"GUSSET\n{BRKT_T}mm",
             ha="center", va="center", fontsize=5, color="#E0E0E0",
             **FONT, zorder=15)

    ax2.add_patch(Rectangle((cx2 - BRKT_T / 2, arm_bot), BRKT_T, ARM_DEPTH,
                             fc="none", ec=C_OUT, lw=1.2, ls="--", zorder=6))
    ax2.text(pr2 + 4, (arm_bot + brkt_arm_z) / 2,
             f"ARM\nZ={arm_bot}–{brkt_arm_z}",
             ha="left", va="center", fontsize=5, color=C_DIM,
             **FONT, zorder=15)

    for z in [grate_bot, grate_top]:
        ax2.plot([pl2 - 10, pr2 + 10], [z, z],
                 color="#208020", lw=0.8, ls=(0, (6, 4)), zorder=3, alpha=0.5)
    ax2.text(pr2 + 4, (grate_bot + grate_top) / 2,
             f"GRATE\n{WALKWAY_GRATE_T}mm",
             ha="left", va="center", fontsize=5, color="#208020",
             **FONT, zorder=15, alpha=0.7)

    bolt_positions_b = [
        (-BOLT_X_OFF, bolt_z_lo, "BOLT 1"),
        ( BOLT_X_OFF, bolt_z_lo, "BOLT 2"),
        ( 0,          bolt_z_hi, "BOLT 3"),
    ]

    for bx, bz, lbl in bolt_positions_b:
        ax2.add_patch(Circle((bx, bz), HOLE_R_B,
                             fc=BG, ec=C_BOLT, lw=1.5, zorder=8))
        ch = HOLE_R_B + 3
        ax2.plot([bx - ch, bx + ch], [bz, bz],
                 color=C_BOLT, lw=0.6, zorder=9)
        ax2.plot([bx, bx], [bz - ch, bz + ch],
                 color=C_BOLT, lw=0.6, zorder=9)

    ax2.plot([-BOLT_X_OFF, BOLT_X_OFF, 0, -BOLT_X_OFF],
             [bolt_z_lo, bolt_z_lo, bolt_z_hi, bolt_z_lo],
             color=C_BOLT, lw=0.6, ls=(0, (3, 3)), zorder=7, alpha=0.5)

    leader(ax2, -BOLT_X_OFF - HOLE_R_B - 1, bolt_z_lo,
           pl2 - 8, bolt_z_lo + 20,
           f"BOLT 1\nM12 ({HOLE_D}mm CLR)",
           color=C_BOLT, fs=5.5,
           ha="right", va="top", arrow_style="-|>", font=FONT)
    leader(ax2, BOLT_X_OFF + HOLE_R_B + 1, bolt_z_lo,
           pr2 + 8, bolt_z_lo - 10,
           f"BOLT 2\nM12 ({HOLE_D}mm CLR)",
           color=C_BOLT, fs=5.5,
           ha="left", va="top", arrow_style="-|>", font=FONT)
    leader(ax2, 0, bolt_z_hi + HOLE_R_B + 1,
           10, bolt_z_hi + 35,
           f"BOLT 3 — M12 ({HOLE_D}mm CLR)\nON GUSSET CL",
           color=C_BOLT, fs=5.5,
           ha="center", va="bottom", arrow_style="-|>", font=FONT)

    dim_x2 = pl2 - 30
    draw_dim_v(ax2, dim_x2 - 10, 0, bolt_z_lo,
               f"{bolt_z_lo}mm", offset=4, fs=6.5, right=False, font=FONT)
    draw_dim_v(ax2, dim_x2 - 10, bolt_z_lo, bolt_z_hi,
               f"{bolt_z_hi - bolt_z_lo}mm", offset=4, fs=6.5, right=False, font=FONT)
    draw_dim_v(ax2, dim_x2 - 10, bolt_z_hi, BRKT_VERT,
               f"{BRKT_VERT - bolt_z_hi}mm", offset=4, fs=6.5, right=False, font=FONT)

    draw_dim_h(ax2, -BOLT_X_OFF, BOLT_X_OFF, bolt_z_lo - 22,
               f"{BOLT_X_OFF * 2}mm", offset=4, fs=6.5, above=False, font=FONT)

    draw_dim_h(ax2, pl2, pr2, -28,
               f"{REINF_W}mm PLATE", offset=4, fs=6, above=False, font=FONT)
    draw_dim_v(ax2, dim_x2 - 18, 0, BRKT_VERT,
               f"{BRKT_VERT}mm", offset=4, fs=6, right=False, font=FONT)

    ax2.text(cx2, BRKT_VERT + 20,
             f"MOUNTING PLATE\n{BRKT_T}mm STEEL · {REINF_W}×{BRKT_VERT}mm",
             ha="center", va="bottom", fontsize=6.5, color=C_BRKT,
             fontweight="bold", **FONT, zorder=15)

    notes_b = [
        "BOLT PATTERN NOTES:",
        f"1. Triangular pattern: 2 lower + 1 upper.",
        f"2. Lower pair at Z={bolt_z_lo}mm, X=±{BOLT_X_OFF}mm from CL — centered between plate edge and {BRKT_T}mm gusset.",
        f"3. Upper bolt at Z={bolt_z_hi}mm (above grating deck Z={WALKWAY_H}mm), centered on gusset CL.",
        f"4. All holes {HOLE_D}mm clearance for M12.",
        f"5. Head on exterior 6mm reinforcing plate, nut on interior bracket face.",
        f"6. See View A for bolt cross-section.",
    ]
    draw_notes(ax2, notes_b, PL_X_LO + 5, -5,
               spacing=7, fs=5.5, title_fs=6, color=C_DIM,
               title_color=C_OUT, font=FONT,
               width=PL_X_HI - PL_X_LO - 10)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 10",
                drawing_title="PERIMETER WALKWAY",
                subtitle="CROSS-SECTION + BOLT PATTERN — STANDARD NEAR WALKWAY BRACKET",
                scale_note="AXES IN mm · VIEW A: SECTION ALONG X / VIEW B: PLATE FACE (−Yd)",
                height=0.07)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "walkway-sheet2.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet2.png saved")

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — Detail A: Right Walkway Cantilever Support (IBC End)  [rev 12]
#
# PLAN view (looking down): X horizontal, Yd vertical.  The right walkway is a
# closed 2×1in-tube rectangle (2 long beams at X=4329/4574 running full width +
# 2 short end beams) picked up at mid-span by 2 arms cantilevering off the IBC
# corridor uprights, on wall cleats at the left corners and combined corner
# plates (shared with the bottom film rail) at the right corners.  Replaces the
# ceiling-hung hanger scheme.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet3():
    """Right walkway — cantilever-rectangle support (rev 12).

    PLAN view looking down.  Horizontal = X, Vertical = Yd.
    """

    # ── Geometry ─────────────────────────────────────────────────────────────
    SHS       = RWK_BEARER_W                  # 50.8 — 2×1in section face shown in plan (long beam, end beam & arm all present their 2in face top-down)
    WK_L_X    = RWK_X_L                       # 4329 — inner long beam / deck left edge
    WK_R_X    = RWK_X_R                       # 4574 — outer long beam / deck right edge (F1-shortened; lands on the combined-plate seat)
    WALL_X    = RAIL_X_R                      # 4649 — right side-wall station (film rail / combined plate)
    UP_X0     = RWK_X_UP                      # 4654 — deep-box FRONT upright (arm clamps here)
    ARM_X     = RWK_X_UP                      # 4654 — arm root station
    UP_YDS    = [(CORRIDOR_YD_NEAR, CORRIDOR_YD_NEAR + IBC_FRAME_RHS),  # near upright 1046–1096
                 (CORRIDOR_YD_FAR - IBC_FRAME_RHS, CORRIDOR_YD_FAR)]     # far  upright 1266–1316
    ARM_YDS   = [yc + IBC_FRAME_RHS / 2 for (yc, _) in UP_YDS]           # arm centerlines

    C_IBC   = "#B08040"
    C_STEEL = C_BRKT
    C_PLATE = "#8090A0"

    # ── View window (X 4250 → IBC stack, Yd 0 → C_WID) ───────────────────────
    X_LO = WK_L_X - 520     # wide left gutter so the cleat/plate callouts clear the beam
    PLAN_X_R = IBC_COL_X + IBC_W + 20    # plan right edge — walls + full-width dim stop here
    X_HI = IBC_COL_X + 2 * IBC_W + 130    # extended right: the notes go in a clean column past the IBC ghost
    Y_LO = -150
    Y_HI = C_WID + 120

    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim((X_LO), (X_HI))
    ax.set_ylim((Y_LO), (Y_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Side walls (Yd=0 near, Yd=C_WID far) ─────────────────────────────────
    for wy in [0, C_WID]:
        ax.plot([(X_LO), (PLAN_X_R)], [(wy), (wy)],
                color=C_OUT, lw=2.0, zorder=3)
    ax.text((WK_L_X), (0 - 55), "NEAR WALL", ha="left", va="center",
            fontsize=6, color=C_OUT, **FONT)
    ax.text((WK_L_X), (C_WID + 55), f"FAR WALL", ha="left", va="center",
            fontsize=6, color=C_OUT, **FONT)

    # ── IBC 2×2 stack ghost ──────────────────────────────────────────────────
    ax.add_patch(Rectangle(((IBC_COL_X), (0)), (IBC_W), (C_WID),
                            fc="#FFE8C0", ec=C_IBC, lw=1.0, ls="--", alpha=0.18, zorder=1))
    ax.text((IBC_COL_X + IBC_W / 2), (C_WID / 2), "IBC 2×2 STACK\n(GHOST)",
            ha="center", va="center", fontsize=7, color=C_IBC, fontweight="bold",
            **FONT, alpha=0.55, zorder=2)

    # Left-margin label gutter (avoids overlap with the narrow rectangle)
    GUT_X = X_LO + 15

    # ── Grated deck (hatched) over the rectangle ─────────────────────────────
    ax.add_patch(Rectangle(((WK_L_X), (0)), (WK_R_X - WK_L_X), (C_WID),
                            fc=C_GRATE, ec="none", alpha=0.30, zorder=4, hatch="++"))

    # ── Closed SHS rectangle: 2 long beams + 2 end beams ─────────────────────
    # Outer long beam — straight; inner long beam — CRANKED outboard around the muslin-drop rod
    # slot (mirrors the model's _rwk_inner_beam_cranked: jog = notch depth, 100mm angled ramps).
    ax.add_patch(Rectangle(((WK_R_X - SHS), (0)), (SHS), (C_WID),
                            fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=8, alpha=0.9))
    cN0 = WALKWAY_MUSLIN_NOTCH_YD0
    cN1 = WALKWAY_MUSLIN_NOTCH_YD0 + WALKWAY_MUSLIN_NOTCH_DY
    cDX = WALKWAY_MUSLIN_NOTCH_DX                 # 100 — jog = notch depth
    cRAMP = 100
    cY0, cY1 = cN0 - cRAMP, cN1 + cRAMP
    xi, xo = WK_L_X, WK_L_X + SHS
    inner_beam = [(xi, 0), (xi, cY0), (xi + cDX, cN0), (xi + cDX, cN1), (xi, cY1), (xi, C_WID),
                  (xo, C_WID), (xo, cY1), (xo + cDX, cN1), (xo + cDX, cN0), (xo, cY0), (xo, 0)]
    ax.add_patch(Polygon(inner_beam, closed=True, fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=8, alpha=0.9))
    for ey in [0, C_WID - SHS]:   # end beams butt BETWEEN the long beams (inner faces), matching the model
        ax.add_patch(Rectangle(((WK_L_X + SHS), (ey)), ((WK_R_X - SHS) - (WK_L_X + SHS)), (SHS),
                                fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=8, alpha=0.9))

    # Muslin-rod drop slot — vacated by the crank (clear vertical passage at the tray edge)
    ax.add_patch(Rectangle((WK_L_X, cN0), cDX, cN1 - cN0, fc="#FFFFFF", ec="#C03028",
                           lw=1.1, ls=(0, (3, 2)), zorder=9))
    ax.plot([WK_L_X + cDX / 2], [(cN0 + cN1) / 2], marker="v", color="#C03028", ms=8, zorder=10)
    leader(ax, (WK_L_X + cDX / 2), (cN0), (GUT_X - 150), (cN0 - 240),
           "MUSLIN ROD DROPS HERE\n(inner beam CRANKED out 100mm\nto clear the full notch — one\ncontinuous, uncut member)",
           color="#C03028", fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)

    leader(ax, (WK_L_X + SHS / 2), (C_WID * 0.80),
           (GUT_X - 150), (C_WID * 0.84),
           f"LONG BEAM\n2×1in tube (50.8×25.4)\n(×2, X={WK_L_X}/{WK_R_X};\ninner cranked at the rod slot)",
           color=C_STEEL, fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)
    leader(ax, ((WK_L_X + WK_R_X) / 2), (C_WID - SHS / 2),
           ((WK_L_X + WK_R_X) / 2), (C_WID + 120),
           "END BEAM (×2)\ncloses the rectangle\nWW5 corners (§10.2)",
           color=C_STEEL, fs=6, ha="center", va="bottom", arrow_style="-|>", font=FONT)

    # ── Center cantilever arms off the IBC uprights ──────────────────────────
    for (yc0, yc1), ay in zip(UP_YDS, ARM_YDS):
        ax.add_patch(Rectangle(((UP_X0), (yc0)), (IBC_FRAME_RHS), (yc1 - yc0),
                                fc=C_IBC, ec=C_OUT, lw=1.0, zorder=6, alpha=0.7))
        ax.add_patch(Rectangle(((WK_L_X), (ay - SHS / 2)), (ARM_X - WK_L_X), (SHS),
                                fc=C_STEEL, ec=C_OUT, lw=1.2, zorder=7, alpha=0.95))
        for bx in [WK_L_X, WK_R_X - SHS]:   # half-lap boxes on the two long beams (inner flush-left, outer flush-right)
            ax.add_patch(Rectangle(((bx), (ay - SHS / 2)), (SHS), (SHS),
                                    fc="none", ec=C_OUT, lw=0.9, ls=(0, (2, 1.5)), zorder=9))
    leader(ax, (WK_L_X + SHS / 2), (ARM_YDS[0]),
           (GUT_X - 150), (C_WID * 0.52),
           "CENTER CANTILEVER ARM (×2)\n2×1in solid flat bar off the IBC\ncorridor uprights",
           color=C_STEEL, fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)
    leader(ax, (WK_R_X + SHS / 2), (ARM_YDS[1] + SHS / 2),
           (WK_R_X + 330), (ARM_YDS[1] + 180),
           "HALF-LAP JOINT\n(arm + long beam\ncross-halved, flush top)",
           color=C_OUT, fs=5.5, ha="center", va="bottom", arrow_style="-|>", font=FONT)

    # ── Corner supports ──────────────────────────────────────────────────────
    # Left corners (X=WK_L_X) on wall cleats
    for cy in [0, C_WID]:
        cyb = cy if cy == 0 else cy - SHS
        ax.add_patch(Rectangle(((WK_L_X - 12), (cyb - 9)), (SHS + 24), (SHS + 18),
                                fc=C_PLATE, ec=C_OUT, lw=1.0, zorder=6, alpha=0.6))
    leader(ax, (WK_L_X + SHS / 2), (SHS / 2),
           (GUT_X - 150), (C_WID * 0.24),
           "WALL CLEAT (left corners)\nback-plate + ext. plate +\nshelf, M12 through-bolts\nWF3 bolts · WW8 welds",
           color=C_PLATE, fs=5.5, ha="left", va="center", arrow_style="-|>", font=FONT)

    # Right corners (X≈WALL_X) on combined corner plates — shared with BR film rail
    for cy in [0, C_WID]:
        cyb = cy if cy == 0 else cy - 70
        ax.add_patch(Rectangle(((WK_R_X - 6), (cyb)), ((WALL_X + 18) - (WK_R_X - 6)), (70),
                                fc=C_PLATE, ec=C_OUT, lw=1.2, zorder=10, alpha=0.85))
    ax.plot([(WALL_X), (WALL_X)], [(0), (C_WID)],
            color=C_CL, lw=1.4, ls=(0, (6, 3)), zorder=5)
    ax.text((WALL_X + 75), (C_WID * 0.50), "BOTTOM FILM RAIL (BR)",
            ha="left", va="center", fontsize=5.5, color=C_CL, rotation=90, **FONT)
    leader(ax, (WK_R_X + SHS / 2), (70),
           (GUT_X + 1000), (C_WID * 0.06),
           "COMBINED CORNER PLATE (right corners)\nshared with the BR film rail — 10mm,\n4× M12, permanently bolted\nWF3 bolts · WW9 welds",
           color=C_PLATE, fs=5.5, ha="left", va="center", arrow_style="-|>", font=FONT)

    # ── Dimensions ───────────────────────────────────────────────────────────
    draw_dim_h(ax, (WK_L_X), (WK_R_X), (-90),
               f"{WALKWAY_RIGHT_W}mm", offset=(9), fs=7, above=False, font=FONT)
    # Label to the LEFT (right=False) so it doesn't overhang X_HI — otherwise the dim text
    # pokes past the axes box and the (transAxes) title block reads narrower than the crop.
    draw_dim_v(ax, (PLAN_X_R - 25), (0), (C_WID),
               f"{C_WID}mm", offset=(8), fs=6.5, right=False, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        "RIGHT WALKWAY — CANTILEVER RECTANGLE:",
        f"1. Closed 2×1in-tube frame: 2 long beams (X={WK_L_X}/{WK_R_X},",
        f"   full {C_WID}mm width) + 2 end beams.",
        "2. Picked up at mid-span by 2 arms cantilevering off the",
        f"   IBC corridor uprights (Yd {CORRIDOR_YD_NEAR}–{CORRIDOR_YD_FAR});",
        "   half-lapped where the long beams cross them.",
        "3. LEFT corners on wall cleats; RIGHT corners on combined",
        "   corner plates SHARED with the bottom film rail (BR).",
        f"4. Deck {WALKWAY_H}mm; {WALKWAY_GRATE_T}mm grate spans the rectangle.",
        "5. ZERO floor contact, ZERO roof penetrations.",
    ]
    draw_notes(ax, notes, (IBC_COL_X + IBC_W + 90), (C_WID * 0.62),
               spacing=(52), fs=6.5, width=(IBC_W - 60), font=FONT)

    # ── Title block ─────────────────────────────────────────────────────────
    title_block(ax, "SHEET 3 OF 10",
                drawing_title="PERIMETER WALKWAY",
                subtitle="DETAIL A — RIGHT WALKWAY CANTILEVER SUPPORT (IBC END)",
                scale_note="Axes in mm · PLAN VIEW LOOKING DOWN",
                height=0.07)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "walkway-sheet3.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet3.png saved")

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 4 — Detail B: Left Walkway Lift-Out at Butt Joint
#
# Elevation showing the left walkway grating sitting on the near/far walkway
# bracket arms at the butt joint (X=470).  Left corners are NOT mitered —
# butt joints keep the near/far walkways entirely past the panel transport
# envelope (X≤420), so only the left walkway needs to be removed for transport.
# No brackets on the left walkway itself — it's a removable lift-out section.
# Scale ≈ 2:1 for clarity.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet4():

    # ── Key geometry ─────────────────────────────────────────────────────────
    BRKT_ARM_Z = WALKWAY_H - WALKWAY_GRATE_T  # 65mm (bracket arm top = grate bottom)
    ARM_DEPTH  = WALKWAY_BRACKET_T + 2         # arm visual thickness
    arm_bot    = BRKT_ARM_Z - ARM_DEPTH
    TRAY_WALL  = 3       # tray wall thickness (SS)
    TRAY_FLOOR_T = 2     # tray floor thickness

    # X positions (horizontal axis in this view — looking along Yd)
    LEFT_WK_L = WALKWAY_LEFT_X                    # = 170mm (left walkway left edge)
    LEFT_WK_R = WALKWAY_LEFT_X + WALKWAY_W        # = 470mm (butt joint / near walkway start)
    PANEL_INNER = 1000   # representative swept X-reach of the cage at the door end (rev10: the
                         # panel + drum swing about the pivot, the cage sweeping roughly to here)
    SWEEP_OVER = PANEL_INNER - LEFT_WK_R          # = 530mm the cage sweeps past the X=470 butt joint into the vacated zone
    NEAR_WK_SHOW = 200   # show 200mm of near walkway past butt joint

    grate_bot = BRKT_ARM_Z   # = 65mm
    grate_top = BRKT_ARM_Z + WALKWAY_GRATE_T  # = 80mm

    # ── Figure ───────────────────────────────────────────────────────────────
    # View: looking along Yd axis (from near wall toward far wall).
    # X = horizontal axis (0 = cargo door end wall, positive into container)
    # Z = vertical axis (0 = floor)
    X_LO = -50
    X_HI = LEFT_WK_R + NEAR_WK_SHOW + 350  # room for near walkway + notes
    Z_LO = -190   # extra room at the bottom so the title block sits clear below the floor
    Z_HI = WALKWAY_H + 110

    fig, ax = plt.subplots(figsize=(18, 13))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim((X_LO), (X_HI))
    ax.set_ylim((Z_LO), (Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container floor ──────────────────────────────────────────────────────
    ax.add_patch(Rectangle(((X_LO), (-15)), (X_HI - X_LO), (15),
                            fc=C_FLOOR, ec=C_OUT, lw=1.0, hatch="///", zorder=2))

    # ── Processing tray rim (at X = PROC_TRAY_X_L = 170mm) ──────────────────
    tray_x = PROC_TRAY_X_L   # = 170mm (same as LEFT_WK_L)
    # Tray left rim (vertical wall)
    ax.add_patch(Rectangle(((tray_x - TRAY_WALL), (0)),
                            (TRAY_WALL), (PROC_TRAY_RIM),
                            fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=4))
    # Tray floor extending right
    tray_floor_end = X_HI - 200
    ax.add_patch(Rectangle(((tray_x), (0)),
                            (tray_floor_end - tray_x), (TRAY_FLOOR_T),
                            fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))
    # Sawtooth break line on tray floor
    bx = (tray_floor_end)
    z_lo, z_hi = 0, TRAY_FLOOR_T
    zz = np.linspace(z_lo, z_hi, 5)
    ax.plot([bx - 3, bx + 3, bx - 3, bx + 3, bx - 3],
            zz, color=C_OUT, lw=1.0, zorder=5)
    # Tray rim label
    leader(ax, (tray_x - 5), (PROC_TRAY_RIM / 2 + 10),
           (tray_x + 50), (PROC_TRAY_RIM),
           f"TRAY RIM\n{PROC_TRAY_RIM}mm\n(304 SS)", color=C_TRAY, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Floor-leg cantilever bracket carrying the grate inner edge (X470) ─────
    C_SUPPORT = "#D08020"
    legx = LEFT_WK_CANT_LEG_X
    post = LEFT_WK_CANT_POST
    fl, fw, ft = LEFT_WK_CANT_FOOT
    fx0 = LEFT_WK_CANT_FOOT_X0
    arm_z0 = LEFT_WK_CANT_ARM_Z0
    arm_x0 = legx + post / 2
    ax.add_patch(Rectangle(((fx0), (0)), (fl), (ft),
                            fc=C_SUPPORT, ec=C_OUT, lw=0.9, zorder=5))
    ax.add_patch(Rectangle(((legx - post / 2), (0)), (post), (grate_bot),
                            fc=C_SUPPORT, ec=C_OUT, lw=1.0, zorder=5))
    ax.add_patch(Rectangle(((arm_x0), (arm_z0)), (LEFT_WK_R - arm_x0),
                            (grate_bot - arm_z0), fc=C_SUPPORT, ec=C_OUT, lw=1.0, zorder=6))
    leader(ax, (legx), (grate_bot * 0.5), (legx - 70), (grate_bot * 0.5),
           "FLOOR-LEG CANTILEVER\nBRACKET (x5) - 50x50 post\non bare floor + arm to X470\n(SEE SHEET 6)",
           color=C_SUPPORT, fs=5, ha="center", va="center", arrow_style="-|>", font=FONT)
    # Spray bar passes under the arm tip (40×25 SS, rides the sloped tray floor)
    ax.add_patch(Rectangle(((LEFT_WK_R), (SPRAY_BAR_Z_BOT)), (40),
                            (SPRAY_BAR_Z_TOP - SPRAY_BAR_Z_BOT), fc="#C8D8E8", ec=C_OUT, lw=1.0, zorder=4))

    # ── Panel swing sweep (ghost) ────────────────────────────────────────────
    # The swinging cage sweeps X=0 to X=PANEL_INNER, bottom at Z=PANEL_FLOOR_GAP
    PANEL_Z_TOP = 250   # show enough of panel to be visible (not full height)
    ax.add_patch(Rectangle(((0), (PANEL_FLOOR_GAP)),
                            (PANEL_INNER), (PANEL_Z_TOP - PANEL_FLOOR_GAP),
                            fc="#CC4422", ec="#CC4422", lw=1.5, ls="--",
                            alpha=0.08, zorder=3))
    ax.add_patch(Rectangle(((0), (PANEL_FLOOR_GAP)),
                            (PANEL_INNER), (PANEL_Z_TOP - PANEL_FLOOR_GAP),
                            fc="none", ec="#CC4422", lw=1.5, ls="--",
                            alpha=0.5, zorder=8))
    # Panel bottom line (Z=80mm)
    ax.plot([(0), (PANEL_INNER)], [(PANEL_FLOOR_GAP), (PANEL_FLOOR_GAP)],
            color="#CC4422", lw=2.0, ls="--", alpha=0.6, zorder=8)
    ax.text((PANEL_INNER / 2), (PANEL_Z_TOP - 10),
            f"PANEL SWING\nSWEEP\n(rides Z={PANEL_FLOOR_GAP}mm over\nthe Z115 brackets)",
            ha="center", va="top", fontsize=6, color="#CC4422",
            fontweight="bold", **FONT, alpha=0.7, zorder=15)

    # ── Left walkway grating (X=170 to X=470, removable lift-out) ────────────
    C_LEFT_WK = "#A8C8A8"   # green tint for removable section
    ax.add_patch(Rectangle(((LEFT_WK_L), (grate_bot)),
                            (WALKWAY_W), (WALKWAY_GRATE_T),
                            fc=C_LEFT_WK, ec=C_OUT, lw=1.5, zorder=7))
    # Bearing bars
    bar_spacing = 34.2
    bar_w = 3
    for x in np.arange(LEFT_WK_L + bar_w, LEFT_WK_R - bar_w, bar_spacing):
        ax.add_patch(Rectangle(((x), (grate_bot)),
                                (bar_w), (WALKWAY_GRATE_T),
                                fc="#8AAA8A", ec=C_OUT, lw=0.3, zorder=8))
    ax.text(((LEFT_WK_L + LEFT_WK_R) / 2), (grate_top + 4),
            f"LEFT WALKWAY GRATING\n({WALKWAY_GRATE_T}mm) \u2014 REMOVABLE LIFT-OUT",
            ha="center", va="bottom", fontsize=6.5, color="#206020",
            fontweight="bold", **FONT, zorder=15)

    # -- The grate inner edge (X470) bears on the cantilever-arm tip (Z115) -----
    ax.plot([(LEFT_WK_R - 60), (LEFT_WK_R)], [(grate_bot), (grate_bot)],
            color="#CC4400", lw=3.0, zorder=10)
    leader(ax, (LEFT_WK_R - 30), (grate_bot),
           (LEFT_WK_R - 150), (grate_bot - 65),
           f"GRATE INNER EDGE BEARS\nON THE ARM TIP (Z={int(grate_bot)})\nX={LEFT_WK_R} \u2014 LIFT TO REMOVE",
           color="#CC4400", fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Near walkway grating (X=470 onward, standard gray) ───────────────────
    near_wk_start = LEFT_WK_R
    near_wk_end = near_wk_start + NEAR_WK_SHOW
    ax.add_patch(Rectangle(((near_wk_start), (grate_bot)),
                            (NEAR_WK_SHOW), (WALKWAY_GRATE_T),
                            fc=C_GRATE, ec=C_OUT, lw=1.2, zorder=7))
    # Bearing bars
    for x in np.arange(near_wk_start + bar_w, near_wk_end - bar_w, bar_spacing):
        ax.add_patch(Rectangle(((x), (grate_bot)),
                                (bar_w), (WALKWAY_GRATE_T),
                                fc="#909098", ec=C_OUT, lw=0.3, zorder=8))
    # Sawtooth break line on right edge (near walkway continues)
    bx = (near_wk_end)
    z_lo, z_hi = (grate_bot - 2), (grate_top + 2)
    zz = np.linspace(z_lo, z_hi, 7)
    ax.plot([bx - 3, bx + 3, bx - 3, bx + 3, bx - 3, bx + 3, bx - 3],
            zz, color=C_OUT, lw=1.0, zorder=10)
    ax.text((near_wk_start + NEAR_WK_SHOW / 2), (grate_top + 4),
            f"NEAR WALKWAY\n({WALKWAY_GRATE_T}mm GRATE)",
            ha="center", va="bottom", fontsize=5.5, color=C_OUT,
            **FONT, zorder=15)

    # ── Grating clip on near walkway (innermost edge, toward processing tray)
    clip_x = near_wk_end - 30
    clip_w = 8
    clip_below = 12
    clip_above = 5
    clip_bot_z = BRKT_ARM_Z - clip_below
    clip_top_z = grate_top + clip_above
    ax.add_patch(Rectangle(((clip_x), (clip_bot_z)),
                            (clip_w), (clip_top_z - clip_bot_z),
                            fc="#505058", ec=C_OUT, lw=0.8, zorder=9))
    leader(ax, (clip_x + clip_w + 2), (grate_top),
           (clip_x + 50), (grate_top + 20),
           "316 SS HOLD-DOWN\nCLIP + BOLT", color="#505058", fs=5.5,
           ha="left", va="center", arrow_style="-|>", font=FONT)

    # ── Butt joint line at X=470 ─────────────────────────────────────────────
    ax.plot([(LEFT_WK_R), (LEFT_WK_R)], [(-5), (grate_top + 3)],
            color=C_OUT, lw=2.0, ls=(0, (5, 3)), zorder=9)
    ax.text((LEFT_WK_R), (-18),
            f"BUTT JOINT\nX={LEFT_WK_R}mm",
            ha="center", va="top", fontsize=6, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── Panel swing reach past the butt joint (left walkway removed first) ────
    # rev10: the panel + drum swing ~56° about the pivot; the cage sweeps roughly to
    # X=PANEL_INNER (~1000), ~SWEEP_OVER (~530mm) PAST the X=470 butt joint — through
    # the zone the removable left walkway + edge beam have vacated, riding the Z130 gap.
    draw_dim_h(ax, (LEFT_WK_R), (PANEL_INNER), (grate_top + 45),
               f"{SWEEP_OVER}mm CAGE SWEEPS PAST X={LEFT_WK_R}\n(LEFT WALKWAY REMOVED FIRST)",
               offset=(5), fs=6.5, color="#CC4422", font=FONT)
    # Vertical guide line at the panel front face
    ax.plot([(PANEL_INNER), (PANEL_INNER)], [(0), (grate_top + 55)],
            color="#CC4422", lw=0.6, ls=":", alpha=0.5, zorder=3)
    ax.plot([(LEFT_WK_R), (LEFT_WK_R)], [(grate_top + 5), (grate_top + 55)],
            color="#CC4422", lw=0.6, ls=":", alpha=0.5, zorder=3)

    # ── Left walkway span dimension ──────────────────────────────────────────
    draw_dim_h(ax, (LEFT_WK_L), (LEFT_WK_R), (grate_top + 70),
               f"{WALKWAY_W}mm LEFT WALKWAY", offset=(5), fs=7, font=FONT)

    # ── Height dimensions (right side) ───────────────────────────────────────
    dim_x = near_wk_end + 40
    # Grate top
    draw_dim_v(ax, (dim_x-30), (0), (grate_top),
               f"{int(grate_top)}mm\nDECK", offset=(6), fs=6, right=True, font=FONT)
    # Beam ledge height (grating bears here)
    draw_dim_v(ax, (dim_x), (0), (BRKT_ARM_Z),
               f"{BRKT_ARM_Z}mm\nLEDGE", offset=(30), fs=6, right=True, font=FONT)
    # Tray rim
    draw_dim_v(ax, (tray_x + 10), (0), (PROC_TRAY_RIM),
               f"{PROC_TRAY_RIM}mm", offset=(6), fs=6, right=True,
               color=C_TRAY, font=FONT)
    # Panel bottom
    draw_dim_v(ax, (LEFT_WK_L - 150), (0), (PANEL_FLOOR_GAP),
               f"{PANEL_FLOOR_GAP}mm\nPANEL\nBOTTOM", offset=(6), fs=5.5, right=False,
               color="#CC4422", font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes_x = (20)
    notes_top = (-50)
    notes = [
        "LEFT WALKWAY \u2014 REMOVABLE LIFT-OUT:",
        f"1. NO wall brackets \u2014 panel occupies end wall.",
        f"2. Inner edge (X={LEFT_WK_R}): carried by FLOOR-LEG CANTILEVER arms (5 brackets; 3 extend to X770 on the punch-out). See sheets 5/6.",
        f"3. Brackets bolted to BARE FLOOR outboard of the tray (X<{LEFT_WK_L}) \u2014 zero tray/wall contact.",
        f"4. The arms pass 15mm OVER the floor-level spray bar (Z60); the +50mm walkway raise enables it.",
        f"5. Panel + drum swing {SWING_LOCK_DEG}\u00b0 about the pivot; the cage sweeps ~{SWEEP_OVER}mm past the X={LEFT_WK_R} butt joint (rides Z{PANEL_FLOOR_GAP}, clears the Z115 brackets).",
        f"6. The grate lifts out before the swing; the floor brackets stay bolted (permanent). No kerb.",
    ]
    draw_notes(ax, notes, notes_x, notes_top, spacing=(8), fs=7, width=(600), font=FONT)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 4 OF 10",
                drawing_title="PERIMETER WALKWAY",
                subtitle="DETAIL B \u2014 LEFT WALKWAY BUTT JOINT AND PANEL CLEARANCE",
                scale_note=f"Axes in mm \u00b7 VIEW ALONG Yd (NEAR \u2192 FAR)",
                height=0.10)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "walkway-sheet4.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet4.png saved")

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 5 — Detail C: Left Walkway Support System
#
# Elevation cross-section showing the support elements for the left walkway:
#   (a) Floor-standing support leg (cargo door side, X=140, on bare floor)
#       with cantilever arm to walkway edge.
#   (b) Steel edge beam (40×40×3mm steel SHS) at X=470 (processing tray side),
#       standing in the Z52–92 envelope (top ~12mm proud as a toe-board kerb),
#       simply supported wall-to-wall on bolt-through wall seats (see Sheet 6).
#       The grating bears on a ledge at Z65; the kerb stops it sliding tray-ward.
#   (c) Bearing strip (15mm Al flat bar) on tray rim at X=170.
# View: looking along Yd (same as sheets 1, 3, 5).
# Zero processing tray contact — all supports outside or above tray; the edge
# beam bottom (Z52) clears the bath (Z≈42) by 10mm and the near/far tray rims
# (Z50, crossed at Yd≈80/2280) by 2mm.
# Scale ≈ 3.5:1 for clarity.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet5():
    """Sheet 5 - Detail C: Left walkway support SYSTEM (plan, looking down).
    The 5 floor-leg cantilever brackets along Yd carry the removable grate; the 3 on
    the drum-exit punch-out (Yd 800-1560) have EXTENDED arms to X770. The spray bar
    travels under the grate (X>=470); the brackets are bolted to bare floor (X<170)."""
    C_SUPPORT = "#D08020"
    C_LEFT_WK = "#A8C8A8"
    legx = LEFT_WK_CANT_LEG_X                 # 140
    post = LEFT_WK_CANT_POST                  # 50
    pw   = LEFT_WK_CANT_POST_W                # 60
    fl, fw, ft = LEFT_WK_CANT_FOOT            # 128, 60, 8
    fx0  = LEFT_WK_CANT_FOOT_X0               # 38
    aw_s, aw_w = LEFT_WK_CANT_ARM_W, LEFT_WK_CANT_ARM_W_WIDE   # 50.8 (2×1) / 101.6 (4×1, IBC/OSHA)
    std, wide = LEFT_WK_CANT_STD_REACH, LEFT_WK_CANT_WIDE_REACH  # 580 / 880 tip X
    arm_x0 = legx + post / 2                  # 165
    wyl, wyr = WALKWAY_LEFT_WIDE_YD_L, WALKWAY_LEFT_WIDE_YD_R    # 800, 1560
    tray_x = PROC_TRAY_X_L                    # 170
    lwx = WALKWAY_LEFT_X                      # 170
    yds = LEFT_WK_CANT_LEG_YDS                # (250,800,1180,1560,2110)

    fig, ax = plt.subplots(figsize=(18, 8.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(-110, 2460)                   # Yd (along the walkway)
    ax.set_ylim(-360, 980)                    # X (reach toward the tray)
    ax.set_aspect("equal"); ax.axis("off")
    ax.text(1181, 955, "DETAIL C - LEFT WALKWAY SUPPORT + DRUM-EXIT PUNCH-OUT (plan, looking down)",
            ha="center", va="bottom", fontsize=9, color=C_OUT, fontweight="bold", **FONT)

    # Spray-bar travel zone (X>=470, under the grate)
    ax.add_patch(Rectangle((0, std), C_WID, 980 - std, fc="#EAF2FA", ec="none", zorder=1))
    ax.text(2080, (std + wide) / 2, "SPRAY BAR travels here\n(under the grate, on the sloped floor)",
            ha="center", va="center", fontsize=6, color="#3A7AB0", style="italic", zorder=2)
    # Tray rim line at X=170
    ax.plot([0, C_WID], [tray_x, tray_x], color=C_TRAY, lw=1.6, zorder=3)
    ax.text(-95, tray_x - 4, "TRAY RIM (X170)\ntray + spray bar STAY at floor level",
            ha="left", va="top", fontsize=5.5, color=C_TRAY, zorder=3)

    # Grate footprint + drum-exit punch-out
    ax.add_patch(Rectangle((0, lwx), C_WID, std - lwx, fc=C_LEFT_WK, ec=C_OUT, lw=1.0, alpha=0.5, zorder=2))
    ax.add_patch(Rectangle((wyl, std), wyr - wyl, wide - std, fc=C_LEFT_WK, ec=C_OUT, lw=1.0, alpha=0.62, zorder=2))
    ax.text(450, (lwx + std) / 2, "LEFT WALKWAY GRATE\n(300mm, removable lift-out)",
            ha="center", va="center", fontsize=7, color="#206020", fontweight="bold", zorder=5)
    ax.text(990, (std + wide) / 2, "DRUM-EXIT PUNCH-OUT\n600×760mm (lift-out landing\nat the light-lock exit)",
            ha="center", va="center", fontsize=6, color="#206020", fontweight="bold", zorder=5)

    # The 5 floor-leg cantilever brackets
    for i, y in enumerate(yds, 1):
        wb = wyl <= y <= wyr
        reach = wide if wb else std
        aw = aw_w if wb else aw_s
        ax.add_patch(Rectangle((y - fw / 2, fx0), fw, fl, fc=C_SUPPORT, ec=C_OUT, lw=0.7, alpha=0.45, zorder=6))
        ax.add_patch(Rectangle((y - pw / 2, legx - post / 2), pw, post, fc=C_SUPPORT, ec=C_OUT, lw=1.0, zorder=8))
        ax.add_patch(Rectangle((y - aw / 2, arm_x0), aw, reach - arm_x0, fc=C_SUPPORT, ec=C_OUT, lw=1.0, zorder=7))

    # Callouts: one standard + one widened bracket
    leader(ax, yds[0], legx, yds[0] - 210, legx - 70,
           f"FLOOR-LEG CANTILEVER\nBRACKET (x5) - 2×2 post\non bare floor + 2×1 arm to X{int(std)}",
           color=C_SUPPORT, fs=6, ha="center", va="top", arrow_style="-|>", font=FONT)
    leader(ax, 1180, (std + wide) / 2, 1180, arm_x0 - 130,
           f"4×1 arm (punch-out)\nSF 1.99",
           color=C_SUPPORT, fs=6, ha="center", va="top", arrow_style="-|>", font=FONT)

    # Bracket Yd spacing chain (along the bottom)
    chain_x = -70
    pts = [0] + list(yds) + [C_WID]
    for a, b in zip(pts[:-1], pts[1:]):
        draw_dim_h(ax, a, b, chain_x, f"{int(b - a)}mm", offset=6, fs=5.5, above=False, font=FONT)
    ax.text(1181, chain_x - 26, "BRACKET Yd SPACING (3 land on the punch-out edges 800/1560 + centre 1180)",
            ha="center", va="top", fontsize=6, color=C_OUT, **FONT)

    # Reach dims (left side)
    draw_dim_v(ax, -55, arm_x0, std, f"{int(std - arm_x0)}mm std", offset=6, fs=5.5, right=False, font=FONT)
    draw_dim_v(ax, -100, arm_x0, wide, f"{int(wide - arm_x0)}mm wide", offset=6, fs=5.5, right=False, font=FONT)
    # Punch-out Yd extent
    draw_dim_h(ax, wyl, wyr, wide + 30, f"{wyr - wyl}mm punch-out", offset=5, fs=6, font=FONT)

    notes = [
        "FLOOR-LEG CANTILEVER SUPPORT (replaces the edge beam):",
        "1. 5 brackets bolted to BARE FLOOR (X<170) - zero tray/wall contact.",
        f"2. foot plate + 2×2×0.120 post + 2×1×0.120 arm (Z{int(LEFT_WK_CANT_ARM_Z0)}-115) to grate edge X{int(std)}.",
        f"3. 3 punch-out brackets EXTEND to X{int(wide)} on 4×1×0.120 arms (IBC/OSHA SF 1.99).",
        "4. arms clear the traveling spray bar (top Z67) by ~22mm; zero tray contact.",
        f"5. DRUM-EXIT PUNCH-OUT: deck deepened to 600mm over Yd800-1560 — landing at the",
        f"   light-lock exit, on the 3 extended (X{int(wide)}) brackets.",
        "6. grate + punch-out lift out together before panel transport; brackets stay floor-bolted.",
        "   No kerb. Bracket section on Sheet 6.",
    ]
    draw_notes(ax, notes, 10, 930, spacing=24, fs=6, ha="left", width=760, font=FONT)

    title_block(ax, "SHEET 5 OF 10",
                drawing_title="PERIMETER WALKWAY",
                subtitle="DETAIL C - LEFT WALKWAY FLOOR-LEG SUPPORT + DRUM-EXIT PUNCH-OUT",
                scale_note="Axes in mm . PLAN (looking down)",
                height=0.07)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "walkway-sheet5.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet5.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 6 — Detail D: Left Edge-Beam Wall-Seat Bracket (IBC-style bolt-through)
#
# How the full-width steel edge beam (50x50x3mm SHS) is simply supported at each
# end: a seat bracket bolted THROUGH the corrugated container wall, exactly like
# the IBC platform-beam wall seats. Two views.
#
# VIEW A — Section along the beam axis (Yd-Z plane at X=470):
#   Wall at Yd=0 (exterior to the left). A drop-in pocket (floor + triangular gusset
#   sides) on an interior mounting plate cradles the beam end. 4x M12 bolts at the
#   plate corners run through the wall to a matching exterior plate (heads outside,
#   clear of the pocket). Grating bears on the Z65 ledge.
#
# VIEW B — Exterior elevation of the backing plate (X-Z plane, from outside):
#   100x135x6mm plate with the 4x M12 bolts at the corners (clear of the pocket).
#
# Scale ~4:1 for clarity.
# ===============================================================================
def sheet6():
    """Sheet 6 — Detail D: Left walkway FLOOR-LEG CANTILEVER bracket.
    VIEW A — section through one bracket (X-Z, looking along Yd): foot plate on bare
    floor outside the tray + 50x50 post + arm reaching IN over the (floor-level) spray
    bar to the grate inner edge. VIEW B — foot-plate plan with the 4x #14 SS self-drilling floor anchors."""
    C_BOLT = "#505058"
    C_SB = "#C8D8E8"                          # spray bar (aluminum)
    legx = LEFT_WK_CANT_LEG_X                # 140
    post = LEFT_WK_CANT_POST                 # 50
    fl, fw, ft = LEFT_WK_CANT_FOOT           # 128, 60, 8
    fx0 = LEFT_WK_CANT_FOOT_X0               # 38
    arm_z0 = LEFT_WK_CANT_ARM_Z0             # 75
    grate_bot = WALKWAY_H - WALKWAY_GRATE_T  # 115
    grate_top = WALKWAY_H                    # 130
    std_reach = LEFT_WK_CANT_STD_REACH       # 470
    arm_x0 = legx + post / 2                 # 165
    rim = PROC_TRAY_RIM                      # 50
    sb0, sb1 = SPRAY_BAR_Z_BOT, SPRAY_BAR_Z_TOP   # 29, 54 @ low corner (floor-relative)
    nb = LEFT_WK_CANT_FOOT_BOLT_N            # 4

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(18, 10),
                                   gridspec_kw={"width_ratios": [1.7, 1.0]})
    for ax in (axA, axB):
        fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
        ax.set_aspect("equal"); ax.axis("off")

    # ===================== VIEW A — bracket section (X-Z) =====================
    TX = PROC_TRAY_X_L                 # real tray LEFT edge (280) — the floor-leg post/arm sit outboard/over it
    XW = int(std_reach + 120)          # view width — reach to the arm tip (grate inner edge) + margin
    axA.set_xlim(0, XW)
    axA.set_ylim(-95, 205)
    axA.text(XW / 2, 196, "VIEW A — FLOOR-LEG CANTILEVER BRACKET (section, looking along Yd)",
             ha="center", va="bottom", fontsize=8, color=C_OUT, fontweight="bold", **FONT)
    # Container floor (hatched)
    axA.add_patch(Rectangle((0, -14), XW, 14, fc=C_FLOOR, ec=C_OUT, lw=1.0, hatch="///", zorder=2))
    # Processing tray — near rim wall at X=PROC_TRAY_X_L (Z0-50), floor + bath to its right
    axA.add_patch(Rectangle((TX, 0), 4, rim, fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=4))
    axA.add_patch(Rectangle((TX + 4, 0), XW - (TX + 4), 2, fc=C_STEEL, ec=C_OUT, lw=0.6, zorder=3))
    axA.add_patch(Rectangle((TX + 4, 2), XW - (TX + 4), rim - 2 - 8, fc="#BFE0F0", ec="none", alpha=0.45, zorder=2))
    leader(axA, TX + 2, rim, TX + 70, rim - 5, "PROCESSING TRAY RIM\n(Z0-50, STAYS at floor level)",
           color=C_OUT, fs=5.5, ha="center", va="bottom", arrow_style="-|>", font=FONT)
    # Foot plate (on bare floor, outboard of the tray)
    axA.add_patch(Rectangle((fx0, 0), fl, ft, fc=C_STEEL, ec=C_OUT, lw=1.2, zorder=6))
    # Post 50x50 (floor to grate bottom)
    axA.add_patch(Rectangle((legx - post / 2, 0), post, grate_bot, fc=C_STEEL, ec=C_OUT, lw=1.4, zorder=6))
    leader(axA, legx, grate_bot * 0.55, legx - 20, grate_bot * 1.3,
           "50x50x3 STEEL\nSHS POST\n(bare floor, outside tray)\nWW7 post→foot (§10.2)",
           color=C_OUT, fs=5.5, ha="center", va="center", arrow_style="-|>", font=FONT)
    # Cantilever arm (Z75-115) reaching to the grate inner edge (X470)
    axA.add_patch(Rectangle((arm_x0, arm_z0), std_reach - arm_x0, grate_bot - arm_z0,
                            fc=C_STEEL, ec=C_OUT, lw=1.4, zorder=7))
    leader(axA, 245, arm_z0 + 20, 220, arm_z0 + 75,
           f"CANTILEVER ARM 2×1 (25.4 DEEP)\n(Z{int(arm_z0)}-{int(grate_bot)}); punch-out arms\nEXTEND to X{int(LEFT_WK_CANT_WIDE_REACH)} on a 4×1\nWW6 arm→post (§10.2)",
           color=C_OUT, fs=5.5, ha="center", va="bottom", arrow_style="-|>", font=FONT)
    # Grate (sits on the arm/post tops)
    axA.add_patch(Rectangle((TX, grate_bot), std_reach - TX, grate_top - grate_bot,
                            fc=C_STEEL, ec=C_OUT, lw=1.0, hatch="xx", alpha=0.85, zorder=8))
    leader(axA, 430, grate_top, 445, grate_top + 30, f"{WALKWAY_GRATE_T}mm GRATE (lift-out)",
           color=C_OUT, fs=5.5, ha="center", va="bottom", arrow_style="-|>", font=FONT)
    # Spray bar (passes UNDER the arm tip — 40×25 SS RHS, rides the sloped tray floor)
    axA.add_patch(Rectangle((std_reach, sb0), 40, sb1 - sb0, fc=C_SB, ec=C_OUT, lw=1.2, zorder=5))
    leader(axA, std_reach + 20, sb1, std_reach + 60, sb1 + 30,
           "SPRAY BAR (40×25 SS)\n(rides the sloped floor)",
           color=C_OUT, fs=5.5, ha="left", va="bottom", arrow_style="-|>", font=FONT)
    # The key clearance: arm underside over the spray-bar top (computed from the constants)
    draw_dim_v(axA, std_reach + 5, sb1, arm_z0, f"{arm_z0 - sb1:.0f}mm", offset=8, fs=6, right=True, font=FONT)
    axA.text(std_reach - 52, (sb1 + arm_z0) / 2, "SPRAY-BAR\nCLEARANCE", ha="right", va="center",
             fontsize=5, color="#208020", fontweight="bold", **FONT)
    # Floor anchors — #14 SS self-drillers (2 of the 4 visible). SAME convention as the IBC corridor-post
    # floor anchors (_foot_elev): hex head on the plate + a shank driving DOWN into the ply-over-steel
    # floor to a drill-point marker — self-driller, NO nut (no accessible underside on a container floor).
    # Positions single-sourced from LEFT_WK_CANT_FOOT_BOLT_DX (outboard, clear of the post).
    for dx in LEFT_WK_CANT_FOOT_BOLT_DX:
        ax_ = fx0 + dx
        axA.plot([ax_, ax_], [ft, -16], color=C_OUT, lw=1.8, zorder=8)              # shank: head level → into the floor
        axA.plot(ax_, -16, 'v', color=C_OUT, ms=4, mew=0, zorder=8)                 # self-drill point (into floor)
        axA.add_patch(Rectangle((ax_ - 6, ft), 12, 5, fc=C_BOLT, ec=C_OUT, lw=0.9, zorder=9))   # hex head on the plate
    # Load arrow at the arm tip
    axA.annotate("", xy=(std_reach - 6, grate_bot + 4), xytext=(std_reach - 6, grate_bot + 30),
                 arrowprops=dict(arrowstyle="-|>", color="#208020", lw=2.0))
    # Key vertical dims
    draw_dim_v(axA, 95, 0, grate_bot, f"{grate_bot}mm", offset=6, fs=6, right=False, font=FONT)
    draw_dim_h(axA, arm_x0, std_reach, arm_z0 - 16, f"{int(std_reach - arm_x0)}mm reach",
               offset=4, fs=6, above=True, font=FONT)
    # Foot plate length (fab dim). The post-height dim_v is already drawn on the left (grate_bot), so no
    # second one here (obs 3).
    draw_dim_h(axA, fx0, fx0 + fl, -30, f"{fl}mm FOOT", offset=4, fs=5.5, above=False, font=FONT)

    # ===================== VIEW B — foot-plate plan =====================
    axB.set_xlim(-90, 90)
    axB.set_ylim(-70, 110)
    axB.text(0, 100, "VIEW B — FOOT PLATE (plan, looking down)",
             ha="center", va="bottom", fontsize=8, color=C_OUT, fontweight="bold", **FONT)
    # plate fl x fw centred
    axB.add_patch(Rectangle((-fl / 2, -fw / 2), fl, fw, fc=C_STEEL, ec=C_OUT, lw=1.4, zorder=5))
    # post footprint — REAL position (from LEFT_WK_CANT_LEG_X), in the centered plan frame
    post_cx = legx - (fx0 + fl / 2)          # post centre, centered frame (foot centre at 0)
    axB.add_patch(Rectangle((post_cx - post / 2, -post / 2), post, post, fill=False,
                            ec="#888", lw=0.8, ls=(0, (4, 3)), zorder=6))
    axB.text(post_cx, 0, "POST", ha="center", va="center", fontsize=5,
             color="#888", fontfamily="monospace", zorder=7)
    # 4 anchors — columns from LEFT_WK_CANT_FOOT_BOLT_DX (centered = dx − fl/2), rows ±DY. Both columns
    # OUTBOARD of the post (it reacts the cantilever uplift), with driver clearance to the post.
    anchor_oxs = [dx - fl / 2 for dx in LEFT_WK_CANT_FOOT_BOLT_DX]
    anchor_oys = [-LEFT_WK_CANT_FOOT_BOLT_DY, LEFT_WK_CANT_FOOT_BOLT_DY]
    HOLE_R6 = 7   # open hole + center crosshair — SAME convention as sheet7 View B (obs 1)
    for ox in anchor_oxs:
        for oy in anchor_oys:
            axB.add_patch(Circle((ox, oy), HOLE_R6, fc=BG, ec=C_BOLT, lw=1.5, zorder=8))
            _ch = HOLE_R6 + 3
            axB.plot([ox - _ch, ox + _ch], [oy, oy], color=C_BOLT, lw=0.6, zorder=9)
            axB.plot([ox, ox], [oy - _ch, oy + _ch], color=C_BOLT, lw=0.6, zorder=9)
    # dashed rectangle connecting the 4 anchor centers (bolt-pattern outline, as sheet7)
    axB.plot([anchor_oxs[0], anchor_oxs[1], anchor_oxs[1], anchor_oxs[0], anchor_oxs[0]],
             [anchor_oys[0], anchor_oys[0], anchor_oys[1], anchor_oys[1], anchor_oys[0]],
             color=C_BOLT, lw=0.6, ls=(0, (3, 3)), zorder=7, alpha=0.5)
    leader(axB, anchor_oxs[0], anchor_oys[1], -fl / 2 - 18, fw / 2 + 24,
           f"WF4 · {nb}x #14 FLOOR ANCHORS", color=C_BOLT, fs=6, ha="center", va="bottom",
           arrow_style="-|>", font=FONT)
    draw_dim_h(axB, -fl / 2, fl / 2, -fw / 2 - 12, f"{fl}mm", offset=4, fs=6, above=False, font=FONT)
    draw_dim_v(axB, fl / 2 + 14, -fw / 2, fw / 2, f"{fw}mm", offset=6, fs=6, right=True, font=FONT)
    # Anchor PATTERN dims (what the shop drills to): column spacing (dim_h) + row spacing (dim_v)
    draw_dim_h(axB, anchor_oxs[0], anchor_oxs[1], anchor_oys[1] + 13,
               f"{int(anchor_oxs[1] - anchor_oxs[0])}mm", offset=4, fs=5.5, above=True, font=FONT)
    draw_dim_v(axB, anchor_oxs[0] - 13, anchor_oys[0], anchor_oys[1],
               f"{int(anchor_oys[1] - anchor_oys[0])}mm", offset=5, fs=5.5, right=False, font=FONT)

    # ── Notes ──
    notes = [
        "FLOOR-LEG CANTILEVER BRACKET (x5, at Yd 250/800/1180/1560/2110):",
        "1. Bolted to BARE FLOOR outboard of the tray (X<170) — ZERO tray contact, ZERO wall fixings.",
        f"2. 50x50x3 steel SHS post (floor to grate bottom Z{grate_bot}) + {nb}x #14 SS self-drilling floor anchors per foot (no nut — bite the ply floor).",
        f"3. Arm Z{int(arm_z0)}-{int(grate_bot)} (2×1×0.120, 25.4 deep) carries the grate inner edge (X{int(LEFT_WK_CANT_STD_REACH)}); the 3 punch-out brackets EXTEND to X{int(LEFT_WK_CANT_WIDE_REACH)} on a 4×1×0.120 arm (IBC/OSHA SF 1.99).",
        "4. The arm clears the traveling spray bar (top Z67) by ~22mm — enabled by the raised Z140 deck.",
        "5. The grate lifts out for transport; the brackets stay bolted (permanent). Replaces the former edge-beam-on-wall-seats.",
    ]
    draw_notes(axA, notes, 4, -58, spacing=7, fs=6.5, ha="left", width=552, font=FONT)

    # The two views share ONE title block. Drawing it on the narrow axB squeezed the
    # three columns together (PROJECT|PERIMETER ran into each other); give it a
    # full-width strip along the figure bottom instead.
    fig.subplots_adjust(bottom=0.16)
    axT = fig.add_axes([0.03, 0.005, 0.94, 0.13]); axT.axis("off")
    axT.set_xlim(0, 1); axT.set_ylim(0, 1)
    title_block(axT, "SHEET 6 OF 10",
                drawing_title="PERIMETER WALKWAY",
                subtitle="DETAIL D — LEFT FLOOR-LEG CANTILEVER BRACKET",
                scale_note="Axes in mm · VIEWS A/B",
                height=0.55)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "walkway-sheet6.png"), dpi=DIAGRAM_DPI, facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet6.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 7 — Widened Bracket Cross-Section (EP/Battery Zone)
#
# Single-panel cross-section of the 500mm cantilever bracket used at
# X=1613 and X=2070 in the EP/battery zone. 10mm plate, 200mm vertical
# leg, 4× M12 rectangular bolt pattern. Same view orientation as Sheet 2
# View A (looking along X axis), but wider viewport for the 500mm arm.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet7():

    # ── Structural dimensions ────────────────────────────────────────────────
    TRAY_WALL  = 3
    TRAY_FLOOR = 2
    CORR_DEPTH = 38
    WALL_T     = 1.6
    BRKT_ARM_H = WALKWAY_H - WALKWAY_GRATE_T   # 65mm
    BRKT_T     = WALKWAY_BRACKET_T              # 8mm (standard, for reference)
    BRKT_VERT  = WALKWAY_BRACKET_H              # 150mm (standard, for reference)
    REINF_T    = 6
    TRAY_RIM_YD = PROC_TRAY_YD_NEAR            # 80mm

    W_BRKT_T    = WALKWAY_WIDE_BRACKET_T        # 10mm plate
    W_BRKT_VERT = WALKWAY_WIDE_BRACKET_H        # 200mm vertical leg
    W_ARM_W     = WALKWAY_NEAR_WIDE_W           # 500mm arm reach
    W_ARM_DEPTH = WALKWAY_BRACKET_ARM_H         # 25.4 — arm is a 3×1×0.120 tube (redesign; was a 12mm plate edge)
    w_arm_bot   = BRKT_ARM_H - W_ARM_DEPTH       # Z89.6
    W_GUSSET    = 70
    W_REINF_W   = WALKWAY_REINF_W_WIDE   # 120
    W_REINF_H   = WALKWAY_REINF_H_WIDE   # 200 — = the widened vertical leg (interior + exterior plates same footprint)
    BOLT_D      = 12
    BOLT_R      = BOLT_D / 2
    C_BOLT      = "#505058"

    # ── Figure (2-panel: View A cross-section + View B bolt pattern) ───────
    YD_LO = -100
    YD_HI = W_ARM_W + 180
    Z_LO  = -70
    Z_HI  = W_BRKT_VERT + 80

    from matplotlib.gridspec import GridSpec
    fig = plt.figure(figsize=(22, 12))
    gs = GridSpec(1, 2, figure=fig, width_ratios=[2.2, 1], wspace=0.08)
    ax  = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim((YD_LO), (YD_HI))
    ax.set_ylim((Z_LO), (Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text((YD_HI / 2), (Z_HI - 5),
            "VIEW A — WIDENED BRACKET CROSS-SECTION (LOOKING ALONG X)",
            ha="center", va="top", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── Container floor ──────────────────────────────────────────────────────
    ax.add_patch(Rectangle(((YD_LO), (-15)), (YD_HI - YD_LO), (15),
                            fc=C_FLOOR, ec=C_OUT, lw=1.0, hatch="///", zorder=2))

    # ── Corrugated wall ──────────────────────────────────────────────────────
    wall_z_top = Z_HI
    ext_panel_yd = -CORR_DEPTH - WALL_T

    ax.add_patch(Rectangle(((ext_panel_yd), (0)),
                            (WALL_T), (wall_z_top),
                            fc="#909098", ec=C_OUT, lw=1.2, zorder=3, hatch="///"))
    ax.add_patch(Rectangle(((-CORR_DEPTH), (0)),
                            (WALL_T), (wall_z_top),
                            fc="#909098", ec=C_OUT, lw=0.8, zorder=3, hatch="///"))
    ax.add_patch(Rectangle(((-WALL_T), (0)),
                            (WALL_T), (wall_z_top),
                            fc="#909098", ec=C_OUT, lw=1.2, zorder=3, hatch="///"))
    ax.add_patch(Rectangle(((-CORR_DEPTH + WALL_T), (0)),
                            (CORR_DEPTH - 2 * WALL_T), (wall_z_top),
                            fc="#F0F0F0", ec="none", lw=0, zorder=2))
    ax.add_patch(Rectangle(((-CORR_DEPTH + WALL_T), (0)),
                            (CORR_DEPTH - 2 * WALL_T), (wall_z_top),
                            fc="none", ec=C_DIM, lw=0.5, ls="--", zorder=3))
    ax.text((-CORR_DEPTH / 2), (wall_z_top * 0.45),
            "AIR\nGAP",
            ha="center", va="center", fontsize=6, color=C_DIM,
            **FONT, zorder=15, style="italic")
    ax.plot([(0), (0)], [(0), (wall_z_top)],
            color=C_OUT, lw=2.0, zorder=4)
    ax.text((-CORR_DEPTH / 2), (wall_z_top - 8),
            "CORRUGATED\nWALL RIB\n(1.6mm CORTEN\nHOLLOW PROFILE)",
            ha="center", va="top", fontsize=5.5, color=C_DIM,
            fontweight="bold", **FONT, zorder=15)

    # ── Reinforcing plate ────────────────────────────────────────────────────
    reinf_yd = ext_panel_yd - REINF_T
    ax.add_patch(Rectangle(((reinf_yd), (0)),
                            (REINF_T), (W_REINF_H),
                            fc="#C08040", ec=C_OUT, lw=1.0, zorder=4))
    leader(ax, (reinf_yd - 1), (W_REINF_H * 0.8),
           (reinf_yd - 25), (W_REINF_H),
           f"REINFORCING\nPLATE\n{W_REINF_W}×{W_REINF_H}\n×{REINF_T}mm\n(EXTERIOR)",
           color="#C08040", fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Processing tray ──────────────────────────────────────────────────────
    ax.add_patch(Rectangle(((TRAY_RIM_YD - TRAY_WALL), (0)),
                            (TRAY_WALL), (PROC_TRAY_RIM),
                            fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=4))
    tray_floor_end = YD_HI - 20
    ax.add_patch(Rectangle(((TRAY_RIM_YD), (0)),
                            (tray_floor_end - TRAY_RIM_YD), (TRAY_FLOOR),
                            fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))
    bx = (tray_floor_end)
    zz = np.linspace(0, TRAY_FLOOR, 5)
    ax.plot([bx - 3, bx + 3, bx - 3, bx + 3, bx - 3],
            zz, color=C_OUT, lw=1.0, zorder=5)
    leader(ax, (TRAY_RIM_YD), (PROC_TRAY_RIM / 2 + 20),
           (TRAY_RIM_YD + 20), (PROC_TRAY_RIM + 15),
           f"TRAY RIM\n{PROC_TRAY_RIM}mm", color=C_TRAY, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # Tray water level
    water_h = 15
    wave_x = np.linspace((TRAY_RIM_YD + 5), (tray_floor_end - 10), 40)
    wave_y = (water_h) + 3 * np.sin(wave_x * 0.08)
    ax.plot(wave_x, wave_y, color="#4080C0", lw=1.0, alpha=0.6, zorder=4)

    # ── Widened cantilever bracket ───────────────────────────────────────────
    brkt_arm_z = BRKT_ARM_H

    # 1. Vertical mounting plate (10mm thick, 200mm tall)
    ax.add_patch(Rectangle(((0), (0)),
                            (W_BRKT_T), (W_BRKT_VERT),
                            fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=6, alpha=0.85))

    # 2. Horizontal arm (500mm reach)
    ax.add_patch(Rectangle(((0), (w_arm_bot)),
                            (W_ARM_W), (W_ARM_DEPTH),
                            fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=6, alpha=0.85))
    ax.plot([(0), (W_ARM_W)], [(brkt_arm_z), (brkt_arm_z)],
            color=C_OUT, lw=2.0, zorder=7)

    # 3. Gusset underneath arm — back edge ON the plate inner face (Yd=W_BRKT_T), not through the plate
    gusset_verts = [
        ((W_BRKT_T), (0)),
        ((W_BRKT_T), (w_arm_bot)),
        ((W_GUSSET), (w_arm_bot)),
    ]
    ax.add_patch(Polygon(gusset_verts, closed=True,
                         fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=5, alpha=0.85))
    ax.plot([(W_BRKT_T), (W_GUSSET)], [(0), (w_arm_bot)],
            color=C_OUT, lw=1.5, zorder=6)

    # Weld symbol
    weld_x = W_GUSSET / 3
    ax.plot([(weld_x - 4), (weld_x), (weld_x + 4)],
            [(w_arm_bot), (w_arm_bot - 5), (w_arm_bot)],
            color="#CC4400", lw=1.5, zorder=8)
    ax.text((weld_x), (w_arm_bot - 7), "WELD WW2/WW3\n(§10.2)",
            ha="center", va="top", fontsize=4.5, color="#CC4400",
            **FONT, zorder=15)

    # ── Through-bolts (4× M12 rectangular pattern: 2 lower + 2 upper) ───────
    bolt_z_lo = 35
    bolt_z_hi = WALKWAY_BRACKET_UPPER_BOLT_Z  # = 155 — SHARED with sheet2 + the 3D (same rule: clears the grate deck)
    BOLT_HEAD = 8
    NUT_H     = 10
    WASHER_T  = 3

    for bz in [bolt_z_lo, bolt_z_hi]:
        shank_hw = BOLT_R * 0.4
        ax.add_patch(Rectangle(((reinf_yd), (bz - shank_hw)),
                                (W_BRKT_T - reinf_yd), (shank_hw * 2),
                                fc=C_BOLT, ec=C_OUT, lw=0.8, zorder=10))
        ax.add_patch(Rectangle(((reinf_yd - BOLT_HEAD), (bz - BOLT_R)),
                                (BOLT_HEAD), (BOLT_D),
                                fc=C_BOLT, ec=C_OUT, lw=1.0, zorder=10))
        ax.add_patch(Rectangle(((reinf_yd - WASHER_T), (bz - BOLT_R - 1)),
                                (WASHER_T), (BOLT_D + 2),
                                fc="#808080", ec=C_OUT, lw=0.5, zorder=9))
        ax.add_patch(Rectangle(((W_BRKT_T), (bz - BOLT_R)),
                                (NUT_H), (BOLT_D),
                                fc=C_BOLT, ec=C_OUT, lw=1.0, zorder=10))
        ax.add_patch(Rectangle(((W_BRKT_T), (bz - BOLT_R - 1)),
                                (WASHER_T), (BOLT_D + 2),
                                fc="#808080", ec=C_OUT, lw=0.5, zorder=9))

    # Bracket label
    leader(ax, (W_ARM_W * 0.4), (brkt_arm_z - 5),
           (W_ARM_W * 0.4 + 50), (brkt_arm_z - 30),
           f"WIDENED BRACKET\n{W_BRKT_T}mm PLATE (vert leg + gusset)\n+ 3×1×0.120 TUBE ARM\n(76.2×25.4, welded on)",
           color=C_BRKT, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # Gusset label
    leader(ax, (W_GUSSET / 2), (w_arm_bot / 2 - 5),
           (W_GUSSET - 20), (w_arm_bot / 2 - 25),
           f"GUSSET ({W_GUSSET}mm)\nSTOPS BEFORE\nTRAY RIM",
           color=C_BRKT, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # Bolt labels
    leader(ax, (reinf_yd - BOLT_HEAD), (bolt_z_lo),
           (reinf_yd - 30), (bolt_z_lo + 20),
           f"WF2 · 2× M12 AT Z={bolt_z_lo}\n(STRADDLE GUSSET\nIN X — SEE VIEW B)",
           color=C_DIM, fs=5,
           ha="center", va="center", arrow_style="-|>", font=FONT)
    leader(ax, (reinf_yd - BOLT_HEAD), (bolt_z_hi),
           (reinf_yd - 30), (bolt_z_hi + 20),
           f"2× M12 AT Z={bolt_z_hi}\n(ABOVE DECK — SEE VIEW B)",
           color=C_DIM, fs=5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Grated deck (500mm wide) ─────────────────────────────────────────────
    grate_bot = brkt_arm_z
    grate_top = grate_bot + WALKWAY_GRATE_T
    ax.add_patch(Rectangle(((W_BRKT_T), (grate_bot)),
                            (W_ARM_W - W_BRKT_T), (WALKWAY_GRATE_T),
                            fc=C_GRATE, ec=C_OUT, lw=1.2, zorder=7))
    for yd in np.arange(W_BRKT_T + 3, W_ARM_W - 3, 34.2):
        ax.add_patch(Rectangle(((yd), (grate_bot)),
                                (3), (WALKWAY_GRATE_T),
                                fc="#909098", ec=C_OUT, lw=0.3, zorder=8))
    cross_h = 3
    for yd in np.arange(W_BRKT_T + 34.2 / 2, W_ARM_W, 34.2):
        ax.add_patch(Rectangle(((yd - 1), (grate_bot + WALKWAY_GRATE_T / 2 - cross_h / 2)),
                                (2), (cross_h),
                                fc="#808088", ec="none", zorder=9, alpha=0.7))

    leader(ax, (W_ARM_W / 4), ((grate_bot + grate_top) / 2),
           (W_ARM_W / 4 - 30), (grate_top + 40),
           f"MOLDED GRP (FIBERGLASS) GRATING\n{WALKWAY_GRATE_T}mm · VINYL-ESTER · GRIT TOP",
           color=C_OUT, fs=6, ha="center", va="center",
           arrow_style="-|>", font=FONT)

    # ── Grating clip ─────────────────────────────────────────────────────────
    clip_yd = W_ARM_W - 20
    clip_bot = brkt_arm_z - 12
    clip_top = grate_top + 5
    ax.add_patch(Rectangle(((clip_yd), (clip_bot)),
                            (8), (clip_top - clip_bot),
                            fc="#505058", ec=C_OUT, lw=0.8, zorder=9))
    leader(ax, (clip_yd + 10), (brkt_arm_z + 30),
           (clip_yd + 40), (brkt_arm_z + 55),
           "316 SS HOLD-DOWN\nCLIP + BOLT", color="#505058", fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Clear tray annotation ────────────────────────────────────────────────
    clr_x = (W_ARM_W * 0.7)
    ax.annotate("", xy=(clr_x, (TRAY_FLOOR + 1)),
                xytext=(clr_x, (w_arm_bot - 1)),
                arrowprops=dict(arrowstyle="<->", color="#208020", lw=1.2, mutation_scale=8))
    gap_mm = w_arm_bot - TRAY_FLOOR   # clear air below the arm underside (lowest obstruction)
    ax.text(clr_x + (5), ((TRAY_FLOOR + brkt_arm_z) / 2),
            f"{gap_mm:.0f}mm\nCLEAR AIR\n(NO LEGS,\nNO BEAM —\nFILM LAYS\nFLAT HERE)",
            ha="left", va="center", fontsize=5, color="#208020",
            fontweight="bold", **FONT, zorder=15, alpha=0.8)

    # ── Operator shoes ───────────────────────────────────────────────────────
    SHOE_W = 100
    SHOE_H = 15
    SHOE_GAP = 20
    shoe_pair_w = 2 * SHOE_W + SHOE_GAP
    shoe_start = (W_ARM_W - shoe_pair_w) / 2
    for i in range(2):
        s_yd = shoe_start + i * (SHOE_W + SHOE_GAP)
        ax.add_patch(Rectangle(
            ((s_yd), (grate_top)), (SHOE_W), (SHOE_H),
            fc="#FFD700", ec="#B89600", lw=0.6,
            zorder=10, alpha=0.3, ls="--"))
    ax.text((W_ARM_W / 2), (grate_top + SHOE_H + 6),
            "US 9 SHOE PAIR\n(270mm LONG × 100mm WIDE)",
            ha="center", va="bottom", fontsize=5.5, color="#404040",
            **FONT, zorder=15, alpha=0.7)

    # ── Dimensions ───────────────────────────────────────────────────────────
    draw_dim_h(ax, (0), (W_ARM_W), (grate_top + 75),
               f"{W_ARM_W}mm WIDENED ARM", offset=(8), fs=7, font=FONT)
    draw_dim_h(ax, (0), (WALKWAY_W), (grate_top + 55),
               f"{WALKWAY_W}mm STD (REF)", offset=(5), fs=5.5,
               color="#808080", font=FONT)
    draw_dim_v(ax, (W_ARM_W + 20), (0), (grate_top),
               f"{WALKWAY_H}mm\nDECK TOP", offset=(8), fs=7, right=True, font=FONT)
    draw_dim_v(ax, (W_ARM_W + 5), (grate_bot), (grate_top),
               f"{WALKWAY_GRATE_T}mm", offset=(8), fs=6.5, right=True, font=FONT)
    draw_dim_v(ax, (reinf_yd - BOLT_HEAD - 45), (0), (W_BRKT_VERT),
               f"{W_BRKT_VERT}mm\nVERT LEG", offset=(8), fs=6.5, right=False, font=FONT)
    draw_dim_v(ax, (W_ARM_W + 5), (0), (brkt_arm_z),
               f"{brkt_arm_z}mm ARM TOP", offset=(8), fs=6.5, right=True, font=FONT)
    draw_dim_v(ax, (TRAY_RIM_YD + 15), (0), (PROC_TRAY_RIM),
               f"{PROC_TRAY_RIM}mm", offset=(8), fs=6.5, right=True,
               color=C_TRAY, font=FONT)
    draw_dim_h(ax, (-CORR_DEPTH), (0), (-22),
               f"{CORR_DEPTH}mm\nCORR", offset=(10), fs=6, above=False, font=FONT)
    draw_dim_h(ax, (0), (TRAY_RIM_YD), (-22),
               f"{TRAY_RIM_YD}mm", offset=(10), fs=6, above=False, font=FONT)

    # ── Axis label ───────────────────────────────────────────────────────────
    ax.text((YD_HI / 2), (Z_LO + 5),
            "Yd  (container width, 0 = pinhole wall)  →",
            ha="center", va="bottom", fontsize=6.5, color=C_DIM,
            **FONT, zorder=15, style="italic")

    # ── Notes ────────────────────────────────────────────────────────────────
    notes_x = (W_ARM_W + 10)
    notes_top = (Z_HI - 10)
    notes = [
        "WIDENED BRACKET NOTES:",
        f"1. {W_BRKT_T}mm plate (vs {BRKT_T}mm standard).",
        f"2. {W_BRKT_VERT}mm vertical leg (vs {BRKT_VERT}mm standard).",
        f"3. 500mm arm reach for EP + battery bank access.",
        f"4. Gusset same {W_GUSSET}mm reach (tray rim limit).",
        f"5. 4× M12 rectangular pattern (2+2)",
        f"   vs 3× triangular on standard bracket.",
        f"6. {W_REINF_W}×{W_REINF_H}×{REINF_T}mm reinforcing plate.",
        f"7. 2 brackets only (X≈1613, 2070).",
        f"8. All other near/far brackets remain standard",
        f"   (Sheet 2).",
    ]
    draw_notes(ax, notes, notes_x, notes_top,
               spacing=(6), fs=7, width=(190), font=FONT)

    # ══════════════════════════════════════════════════════════════════════════
    # VIEW B — Plate face (looking along −Yd, toward wall)
    # Horizontal = X (bracket width), Vertical = Z (height)
    # Shows rectangular 4× M12 bolt pattern on the vertical mounting plate
    # ══════════════════════════════════════════════════════════════════════════
    ax2.set_facecolor(BG)

    BOLT_X_OFF_W = WALKWAY_BRACKET_BOLT_DX_WIDE   # 32 — widened-bracket lower/upper-bolt X offset (single-sourced; matches the 3D)
    HOLE_D = 14
    HOLE_R_B = HOLE_D / 2

    PL_X_LO = -W_REINF_W / 2 - 55
    PL_X_HI =  W_REINF_W / 2 + 65
    PL_Z_LO = -40
    PL_Z_HI =  W_BRKT_VERT + 55
    ax2.set_xlim(PL_X_LO, PL_X_HI)
    ax2.set_ylim(PL_Z_LO, PL_Z_HI)
    ax2.set_aspect("equal")
    ax2.axis("off")

    ax2.text(0, PL_Z_HI - 5,
             "VIEW B — PLATE FACE (−Yd)",
             ha="center", va="top", fontsize=8, color=C_OUT,
             fontweight="bold", **FONT, zorder=15)

    cx2 = 0
    pl2 = cx2 - W_REINF_W / 2
    pr2 = cx2 + W_REINF_W / 2

    ax2.add_patch(Rectangle((pl2, 0), W_REINF_W, W_BRKT_VERT,
                             fc=C_BRKT, ec=C_OUT, lw=2.0, zorder=5, alpha=0.85))

    gusset_hw = W_BRKT_T / 2
    gusset_fp = [
        (cx2 - gusset_hw, 0),
        (cx2 - gusset_hw, w_arm_bot),
        (cx2 + gusset_hw, w_arm_bot),
        (cx2 + gusset_hw, 0),
    ]
    ax2.add_patch(Polygon(gusset_fp, closed=True,
                          fc="#606870", ec=C_OUT, lw=1.0, ls="--",
                          zorder=6, alpha=0.5))
    ax2.text(cx2, w_arm_bot / 2,
             f"GUSSET\n{W_BRKT_T}mm",
             ha="center", va="center", fontsize=5, color="#E0E0E0",
             **FONT, zorder=15)

    ARM_DEPTH_B = W_ARM_DEPTH
    ax2.add_patch(Rectangle((cx2 - W_BRKT_T / 2, w_arm_bot), W_BRKT_T, ARM_DEPTH_B,
                             fc="none", ec=C_OUT, lw=1.2, ls="--", zorder=6))
    ax2.text(pr2 + 4, (w_arm_bot + brkt_arm_z) / 2,
             f"ARM\nZ={w_arm_bot}–{brkt_arm_z}",
             ha="left", va="center", fontsize=5, color=C_DIM,
             **FONT, zorder=15)

    grate_bot_b = brkt_arm_z
    grate_top_b = grate_bot_b + WALKWAY_GRATE_T
    for z in [grate_bot_b, grate_top_b]:
        ax2.plot([pl2 - 10, pr2 + 10], [z, z],
                 color="#208020", lw=0.8, ls=(0, (6, 4)), zorder=3, alpha=0.5)
    ax2.text(pr2 + 4, (grate_bot_b + grate_top_b) / 2,
             f"GRATE\n{WALKWAY_GRATE_T}mm",
             ha="left", va="center", fontsize=5, color="#208020",
             **FONT, zorder=15, alpha=0.7)

    bolt_positions_b = [
        (-BOLT_X_OFF_W, bolt_z_lo, "BOLT 1"),
        ( BOLT_X_OFF_W, bolt_z_lo, "BOLT 2"),
        (-BOLT_X_OFF_W, bolt_z_hi, "BOLT 3"),
        ( BOLT_X_OFF_W, bolt_z_hi, "BOLT 4"),
    ]

    for bx, bz, lbl in bolt_positions_b:
        ax2.add_patch(Circle((bx, bz), HOLE_R_B,
                             fc=BG, ec=C_BOLT, lw=1.5, zorder=8))
        ch = HOLE_R_B + 3
        ax2.plot([bx - ch, bx + ch], [bz, bz],
                 color=C_BOLT, lw=0.6, zorder=9)
        ax2.plot([bx, bx], [bz - ch, bz + ch],
                 color=C_BOLT, lw=0.6, zorder=9)

    ax2.plot([-BOLT_X_OFF_W, BOLT_X_OFF_W, BOLT_X_OFF_W, -BOLT_X_OFF_W, -BOLT_X_OFF_W],
             [bolt_z_lo, bolt_z_lo, bolt_z_hi, bolt_z_hi, bolt_z_lo],
             color=C_BOLT, lw=0.6, ls=(0, (3, 3)), zorder=7, alpha=0.5)

    leader(ax2, -BOLT_X_OFF_W - HOLE_R_B - 1, bolt_z_lo,
           pl2 - 8, bolt_z_lo + 20,
           f"BOLT 1\nM12 ({HOLE_D}mm CLR)",
           color=C_BOLT, fs=5.5,
           ha="right", va="top", arrow_style="-|>", font=FONT)
    leader(ax2, BOLT_X_OFF_W + HOLE_R_B + 1, bolt_z_lo,
           pr2 + 8, bolt_z_lo - 10,
           f"BOLT 2\nM12 ({HOLE_D}mm CLR)",
           color=C_BOLT, fs=5.5,
           ha="left", va="top", arrow_style="-|>", font=FONT)
    leader(ax2, -BOLT_X_OFF_W - HOLE_R_B - 1, bolt_z_hi,
           pl2 - 8, bolt_z_hi - 15,
           f"BOLT 3\nM12 ({HOLE_D}mm CLR)",
           color=C_BOLT, fs=5.5,
           ha="right", va="top", arrow_style="-|>", font=FONT)
    leader(ax2, BOLT_X_OFF_W + HOLE_R_B + 1, bolt_z_hi,
           pr2 + 8, bolt_z_hi + 25,
           f"BOLT 4\nM12 ({HOLE_D}mm CLR)",
           color=C_BOLT, fs=5.5,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    dim_x2 = pl2 - 30
    draw_dim_v(ax2, dim_x2 - 10, 0, bolt_z_lo,
               f"{bolt_z_lo}mm", offset=4, fs=6.5, right=True, font=FONT)
    draw_dim_v(ax2, dim_x2 - 10, bolt_z_lo, bolt_z_hi,
               f"{bolt_z_hi - bolt_z_lo}mm", offset=4, fs=6.5, right=True, font=FONT)
    draw_dim_v(ax2, dim_x2 - 10, bolt_z_hi, W_BRKT_VERT,
               f"{W_BRKT_VERT - bolt_z_hi}mm", offset=4, fs=6.5, right=True, font=FONT)

    draw_dim_h(ax2, -BOLT_X_OFF_W, BOLT_X_OFF_W, bolt_z_lo - 22,
               f"{BOLT_X_OFF_W * 2}mm", offset=4, fs=6.5, above=False, font=FONT)

    draw_dim_h(ax2, pl2, pr2, -28,
               f"{W_REINF_W}mm PLATE", offset=4, fs=6, above=False, font=FONT)
    draw_dim_v(ax2, dim_x2 - 18, 0, W_BRKT_VERT,
               f"{W_BRKT_VERT}mm", offset=4, fs=6, right=False, font=FONT)

    ax2.text(cx2, W_BRKT_VERT + 20,
             f"MOUNTING PLATE\n{W_BRKT_T}mm STEEL · {W_REINF_W}×{W_BRKT_VERT}mm",
             ha="center", va="bottom", fontsize=6.5, color=C_BRKT,
             fontweight="bold", **FONT, zorder=15)

    notes_b = [
        "BOLT PATTERN NOTES:",
        f"1. Rectangular pattern: 2 lower + 2 upper.",
        f"2. Lower pair at Z={bolt_z_lo}mm, X=±{BOLT_X_OFF_W}mm from CL — centered between plate edge and {W_BRKT_T}mm gusset.",
        f"3. Upper pair at Z={bolt_z_hi}mm (above grating deck Z={WALKWAY_H}mm), same X offset as lower pair.",
        f"4. All holes {HOLE_D}mm clearance for M12.",
        f"5. Head on exterior {REINF_T}mm reinforcing plate, nut on interior bracket face.",
        f"6. See View A for bolt cross-section.",
    ]
    draw_notes(ax2, notes_b, PL_X_LO + 5, -5,
               spacing=7, fs=5.5, title_fs=6, color=C_DIM,
               title_color=C_OUT, font=FONT,
               width=PL_X_HI - PL_X_LO - 30)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 7 OF 10",
                drawing_title="PERIMETER WALKWAY",
                subtitle="CROSS-SECTION + BOLT PATTERN — WIDENED BRACKET (EP/BATTERY ZONE, 500mm ARM)",
                scale_note="AXES IN mm · VIEW A: SECTION ALONG X / VIEW B: PLATE FACE (−Yd)",
                height=0.07)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "walkway-sheet7.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet7.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 8 — Width Transition Detail (Plan View)
#
# Plan view looking down at a transition bracket where the grating changes
# from 500mm (widened) to 300mm (standard).  Shows bearing plate on bracket
# arm, M saddle clips, and grating bearing bar pattern.
# Horizontal = Yd (0 = wall, positive toward container center)
# Vertical   = X (negative = wide side, positive = narrow side)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet8():
    SC = 2.0  # 1:2 scale


    # ── Dimensions ───────────────────────────────────────────────────────────
    W_STD    = WALKWAY_W              # 300mm standard width
    W_WIDE   = WALKWAY_NEAR_WIDE_W    # 500mm widened width
    BRKT_T   = WALKWAY_WIDE_BRACKET_T # 10mm bracket arm plate thickness
    ARM_LEN  = W_WIDE                 # 500mm arm (widened bracket)
    GUSSET_R = 70                     # gusset reach from wall
    BAR_W    = 3                      # bearing bar width
    BAR_H    = 30                     # bearing bar depth (height of grating)
    BAR_PITCH = 34.2                  # bearing bar spacing
    XBAR_W   = 3                      # cross bar width
    GRATE_T  = WALKWAY_GRATE_T        # 25mm grating thickness
    CLIP_W   = 24                     # M saddle clip width in Yd
    CLIP_L   = 2 * BAR_PITCH + BAR_W  # clip spans 2 bearing bars
    BEARING_PLATE_W = 40              # bearing plate width in X
    BEARING_PLATE_L = ARM_LEN         # bearing plate length in Yd (= arm)
    TRAY_LIP = PROC_TRAY_YD_NEAR     # 80mm

    # Show extent in X: ±350mm from bracket center (enough for grating overlap)
    SHOW_X = 350
    # Show extent in Yd: -50 to ARM_LEN + 80
    YD_LO = -80
    YD_HI = ARM_LEN + 100
    TITLE_Y = SHOW_X + 80  # title zone above diagram

    # ── Figure ───────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(18, 18))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim((YD_LO), (YD_HI))
    ax.set_ylim((-SHOW_X - 150), (TITLE_Y))
    ax.set_aspect("equal")
    ax.axis("off")

    C_WIDE_GRATE = "#C8C0A8"
    C_STD_GRATE  = "#D0C8B8"
    C_PLATE      = "#A0A0B0"
    C_CLIP       = "#606878"
    C_GUSSET     = "#909098"

    # Bracket center is at X=0 in local coords
    # Wide grating on the -X side (left in diagram), std on +X side (right)

    # ── Wall ─────────────────────────────────────────────────────────────────
    ax.add_patch(Rectangle(((-40), (-SHOW_X)),
                 (40), (2 * SHOW_X),
                 fc="#D8D4D0", ec=C_OUT, lw=2.0, zorder=1))
    ax.text((-20), (0), "WALL\n(Yd=0)",
            ha="center", va="center", fontsize=7, color=C_DIM,
            rotation=90, **FONT, zorder=20)

    # ── Processing tray rim line ─────────────────────────────────────────────
    ax.plot([(TRAY_LIP), (TRAY_LIP)], [(-SHOW_X), (SHOW_X)],
            color="#4A8A4A", lw=1.0, ls="--", alpha=0.5, zorder=2)
    ax.text((TRAY_LIP + 8), (SHOW_X - 30),
            f"PROC. TRAY LIP\n(Yd={TRAY_LIP}mm)",
            ha="left", va="top", fontsize=5.5, color="#4A8A4A",
            **FONT, zorder=20)

    # ── Bracket arm (10mm plate, edge-on in plan view) ───────────────────────
    ax.add_patch(Rectangle(((0), (-BRKT_T / 2)),
                 (ARM_LEN), (BRKT_T),
                 fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=5))
    ax.text((ARM_LEN / 2), (-BRKT_T / 2 - 5),
            f"BRACKET ARM (10mm × {ARM_LEN}mm)",
            ha="center", va="top", fontsize=5.5, color=C_DIM,
            **FONT, zorder=20)

    # ── Gusset (triangle in plan view, 70mm reach from wall) ─────────────────
    gusset_verts = [
        ((0), (-BRKT_T / 2)),
        ((GUSSET_R), (0)),
        ((0), (BRKT_T / 2)),
    ]
    ax.add_patch(Polygon(gusset_verts, closed=True,
                         fc=C_GUSSET, ec=C_OUT, lw=1.0, zorder=4))

    # ── Bearing plate (40mm × 500mm, centered on arm) ────────────────────────
    bp_x0 = -BEARING_PLATE_W / 2
    ax.add_patch(Rectangle(((0), (bp_x0)),
                 (BEARING_PLATE_L), (BEARING_PLATE_W),
                 fc=C_PLATE, ec=C_OUT, lw=1.2, ls="--", alpha=0.7,
                 zorder=6))
    leader(ax, (BEARING_PLATE_L + 5), (bp_x0 + BEARING_PLATE_W / 2),
           (BEARING_PLATE_L + 20), (bp_x0 + BEARING_PLATE_W / 2 + 60),
           f"BEARING PLATE\n{BEARING_PLATE_W}×{BEARING_PLATE_L}×5mm\n(WELDED TO ARM)",
           color=C_DIM, fs=5.5, ha="left", va="bottom",
           arrow_style="-|>", font=FONT)

    # ── Wide grating (−X side) ───────────────────────────────────────────────
    # Grating extends from Yd=0 to Yd=W_WIDE (500mm), from X=-SHOW_X to X≈0
    gw_x0 = -SHOW_X
    gw_x1 = -BEARING_PLATE_W / 2  # ends at bearing plate edge
    ax.add_patch(Rectangle(((0), (gw_x0)),
                 (W_WIDE), (gw_x1 - gw_x0),
                 fc=C_WIDE_GRATE, ec=C_OUT, lw=0.6, alpha=0.15,
                 hatch="xx", zorder=3))
    ax.text((W_WIDE / 2), (gw_x0 + (gw_x1 - gw_x0) / 2 - 30),
            f"WIDENED GRATING\n(500mm)",
            ha="center", va="center", fontsize=7, color=C_OUT, backgroundcolor="#FFFFFF",
            **FONT, zorder=20, alpha=0.8)

    # ── Standard grating (+X side) ───────────────────────────────────────────
    gs_x0 = BEARING_PLATE_W / 2   # starts at bearing plate edge
    gs_x1 = SHOW_X
    ax.add_patch(Rectangle(((0), (gs_x0)),
                 (W_STD), (gs_x1 - gs_x0),
                 fc=C_STD_GRATE, ec=C_OUT, lw=0.6, alpha=0.15,
                 hatch="xx", zorder=3))
    ax.text((W_STD / 2), (gs_x0 + (gs_x1 - gs_x0) / 2 + 30),
            f"STANDARD GRATING\n(300mm)",
            ha="center", va="center", fontsize=7, color=C_OUT, backgroundcolor="#FFFFFF",
            **FONT, zorder=20, alpha=0.8)

    # ── Show outer 200mm of widened grating past standard edge ───────────────
    # Light fill for the outer zone (Yd=300 to Yd=500) on the wide side
    ax.add_patch(Rectangle(((W_STD), (gw_x0)),
                 (W_WIDE - W_STD), (gw_x1 - gw_x0),
                 fc="#E8D8B8", ec="none", lw=0, alpha=0.10, zorder=3.5))
    ax.text((W_STD + (W_WIDE - W_STD) / 2), (gw_x0 + 30),
            f"EXTENDED\n200mm",
            ha="center", va="center", fontsize=5.5, color="#8B6B3C",
            **FONT, zorder=20, alpha=0.9)

    # ── Bearing bars (representative, perpendicular to walkway length) ───────
    # Bearing bars run in the X direction (along the walkway)
    # Show them as thin lines spanning the grating width
    bar_color = "#888890"
    n_bars_show = 12
    for i in range(-n_bars_show, n_bars_show + 1):
        bar_x = i * BAR_PITCH
        if abs(bar_x) > SHOW_X - 20:
            continue
        # Wide side bars: extend to Yd=W_WIDE
        if bar_x < -BEARING_PLATE_W / 2:
            ax.plot([(0), (W_WIDE)],
                    [(bar_x), (bar_x)],
                    color=bar_color, lw=0.4, alpha=0.5, zorder=3.5)
        # Narrow side bars: extend to Yd=W_STD
        elif bar_x > BEARING_PLATE_W / 2:
            ax.plot([(0), (W_STD)],
                    [(bar_x), (bar_x)],
                    color=bar_color, lw=0.4, alpha=0.5, zorder=3.5)

    # ── M saddle clips ───────────────────────────────────────────────────────
    # Clip sits on top of grating, centered over the bracket arm / bearing plate.
    # TEK screw goes DOWN through clip center → between grating bars → into arm.
    # Clip long axis spans 2 bearing bars (X direction); centered on arm (X≈0).
    # One clip per grating section at this bracket, at different Yd positions.

    clip_positions = [
        # (Yd center, X center) — TEK screw at center must hit bearing plate (±20mm)
        (120,          -BAR_PITCH / 2),   # wide-side clip, inner zone
        (W_WIDE - 80,  -BAR_PITCH / 2),   # wide-side clip, outer zone
        (120,           BAR_PITCH / 2),   # std-side clip, inner zone
    ]

    for yd_c, x_c in clip_positions:
        cw = CLIP_W
        cl = CLIP_L
        ax.add_patch(Rectangle(
            ((yd_c - cw / 2), (x_c - cl / 2)),
            (cw), (cl),
            fc=C_CLIP, ec=C_OUT, lw=0.8, alpha=0.8, zorder=8))
        # TEK screw (small circle at center — directly over arm)
        ax.add_patch(Circle(
            ((yd_c), (x_c)),
            (3), fc="#333333", ec=C_OUT, lw=0.5, zorder=9))

    # Label one clip
    bbox = dict(fc="white", ec="none", pad=1.5, alpha=0.85)
    leader(ax, (clip_positions[0][0]), (clip_positions[0][1]),
           (80), (-72),
           "316 SS HOLD-DOWN CLIP\nBOLTED INTO\nBRACKET ARM BELOW\n(TYP. BOTH SIDES)",
           color=C_DIM, fs=5.5, ha="right", va="top",
           arrow_style="-|>", font=FONT, bbox=bbox)

    # ── Dimension: standard grating width ────────────────────────────────────
    draw_dim_h(ax, (0), (W_STD), (SHOW_X - 20),
               f"{W_STD}mm", color=C_DIM, fs=6, offset=(8), font=FONT)

    # ── Dimension: widened grating width ─────────────────────────────────────
    draw_dim_h(ax, (0), (W_WIDE), (-SHOW_X + 20),
               f"{W_WIDE}mm", color=C_DIM, fs=6, offset=(8), font=FONT)

    # ── Dimension: bearing plate width ───────────────────────────────────────
    draw_dim_v(ax, (ARM_LEN + 40),
               (-BEARING_PLATE_W / 2), (BEARING_PLATE_W / 2),
               f"{BEARING_PLATE_W}mm", color=C_DIM, fs=5.5,
               offset=(8), font=FONT)

    # ── Dimension: tray lip to wall ──────────────────────────────────────────
    draw_dim_h(ax, (0), (TRAY_LIP), (SHOW_X - 60),
               f"{TRAY_LIP}mm", color="#4A8A4A", fs=5.5,
               offset=(8), font=FONT)

    # ── Edge labels ──────────────────────────────────────────────────────────
    ax.annotate("", xy=((W_STD), (SHOW_X - 5)),
                xytext=((W_STD), (SHOW_X - 40)),
                arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.6, ls="--"))
    ax.text((W_STD + 10), (SHOW_X - 50),
            "STD INNER\nEDGE", ha="left", va="top",
            fontsize=5, color=C_DIM, **FONT, zorder=20)

    ax.annotate("", xy=((W_WIDE), (-SHOW_X + 5)),
                xytext=((W_WIDE), (-SHOW_X + 40)),
                arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.6, ls="--"))
    ax.text((W_WIDE + 10), (-SHOW_X + 50),
            "WIDE INNER\nEDGE", ha="left", va="bottom",
            fontsize=5, color=C_DIM, **FONT, zorder=20)

    # ── View label (in title zone, above diagram) ──────────────────────────
    ax.text((W_WIDE / 2), (TITLE_Y - 10),
            "PLAN VIEW — WIDTH TRANSITION AT BRACKET",
            ha="center", va="top", fontsize=9, color=C_OUT,
            weight="bold", **FONT, zorder=20)
    ax.text((W_WIDE / 2), (TITLE_Y - 35),
            "LOOKING DOWN · WALL AT LEFT · Yd HORIZONTAL · X VERTICAL",
            ha="center", va="top", fontsize=6, color=C_DIM,
            **FONT, zorder=20)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        "NOTES:",
        f"1. TRANSITION BRACKET: {BRKT_T}mm ARM PLATE, {ARM_LEN}mm REACH (WIDENED DESIGN)",
        f"2. BEARING PLATE: {BEARING_PLATE_W}×{BEARING_PLATE_L}×5mm FLAT BAR WELDED TO ARM TOP",
        f"3. WIDENED GRATING (500mm) ENDS AT BRACKET — STANDARD (300mm) BEGINS",
        f"4. 316 SS HOLD-DOWN CLIPS CLAMP THE GRP PANEL, RETAINED BY SS BOLT",
        f"5. GRATING SECTIONS BUTT AT BEARING PLATE — NO OVERLAP",
        f"6. OUTER 200mm OF BRACKET ARM EXPOSED ON STANDARD SIDE",
        f"7. TRANSITION BRACKETS AT X≈1156mm AND X≈2526mm",
    ]
    draw_notes(ax, notes, (YD_LO + 440), (SHOW_X - 10),
               spacing=(7), fs=5.5, title_fs=6, color=C_DIM,
               title_color=C_OUT, font=FONT,
               width=(225))

    # ── Title block ──────────────────────────────────────────────────────────
    title_block(ax, "SHEET 8 OF 10",
                drawing_title="PERIMETER WALKWAY",
                subtitle="WIDTH TRANSITION DETAIL — PLAN VIEW AT BRACKET",
                scale_note="SCALE 1:2 · LOOKING DOWN · Yd HORIZONTAL / X VERTICAL",
                height=0.06)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "walkway-sheet8.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet8.png saved")


def sheet9():
    """Sheet 9 — Detail F: Near-walkway BUMP-OUT on the pinhole wall (plan, looking down).

    The pinhole-wall counterpart to the left drum-exit punch-out (now folded into Sheet 5).
    The near walkway widens from WALKWAY_W to WALKWAY_NEAR_WIDE_W over
    X=WALKWAY_NEAR_WIDE_X_L..X_R, giving the operator standing room at the wall-mounted EP
    panel + battery bank and a full bay past the spray-bar pole slit. Carried by 5 WIDENED
    wall-cantilever brackets (500mm arm) at the ribs; standard 300mm-arm brackets flank it.
    """
    C_STD = "#707888"; C_WIDE = "#CC6644"; C_WK = "#D0C8B8"
    nxl = WALKWAY_LEFT_X + WALKWAY_W                 # 470 — near deck start
    nxr = WALKWAY_RIGHT_X                            # 4329 — near deck end
    W, WW = WALKWAY_W, WALKWAY_NEAR_WIDE_W           # 300, 500
    WXL, WXR = WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_X_R   # 1055, 3083
    slit_cx = int((PROC_OPEN_X_L + PROC_OPEN_X_R) / 2)       # 2399 — pole slit / pinhole X
    stations = list(np.arange(nxl + WALKWAY_BRACKET_SPACING / 2, nxr, WALKWAY_BRACKET_SPACING))
    wide_st = [s for s in stations if WXL <= s <= WXR]        # the 5 widened ribs
    ovh = WALKWAY_MAX_OVERHANG                       # 100 — deck overhang past the end bracket

    x0, x1 = 620, 3560
    fig, ax = plt.subplots(figsize=(17, 8.4))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(x0, x1); ax.set_ylim(-360, 1160)
    ax.set_aspect("equal"); ax.axis("off")
    ax.text((x0 + x1) / 2, 1140, "DETAIL F - NEAR-WALKWAY BUMP-OUT (PINHOLE WALL, plan looking down)",
            ha="center", va="bottom", fontsize=9, color=C_OUT, fontweight="bold", **FONT)

    # Processing tray beyond the inboard deck edge (ghost)
    ax.add_patch(Rectangle((x0, WW), x1 - x0, 150, fc="#EAF2F8", ec="none", zorder=1))
    ax.text(x0 + 40, WW + 118, "PROCESSING TRAY (open, beyond the deck)",
            ha="left", va="top", fontsize=6, color="#5A88A8", style="italic", **FONT, zorder=2)

    # Pinhole wall at Yd 0, with the EP panel + battery column mounted on it (shared X footprint)
    ax.add_patch(Rectangle((x0, -46), x1 - x0, 46, fc="#C8C8C8", ec=C_OUT, lw=1.2, zorder=3))
    ax.text(x0 + 30, -58, "PINHOLE WALL", ha="left", va="top", fontsize=7, color=C_OUT, fontweight="bold", **FONT)
    eq_x0 = min(EP_X, BA_X); eq_x1 = max(EP_X + EP_W, BA_X + BA_W)
    ax.add_patch(Rectangle((eq_x0, -46), eq_x1 - eq_x0, 46, fc="#B8C4D0", ec=C_OUT, lw=0.9, zorder=4))
    ax.text((eq_x0 + eq_x1) / 2, -22, "EP PANEL + BATTERY (wall-mounted, stacked)",
            ha="center", va="center", fontsize=5, color=C_OUT, **FONT, zorder=5)

    # Near deck — ONE continuous L-piece (std strip + integral bump tab), matching the model
    deck = [(nxl, 0), (nxr, 0), (nxr, W), (WXR, W), (WXR, WW), (WXL, WW), (WXL, W), (nxl, W)]
    ax.add_patch(Polygon(deck, closed=True, fc=C_WK, ec=C_OUT, lw=1.4, hatch="xx", alpha=0.5, zorder=6))
    # Highlight the added band (the 200mm-deep bump tab) so it reads as the widening
    ax.add_patch(Rectangle((WXL, W), WXR - WXL, WW - W, fc="#8FBF8F", ec="none", alpha=0.35, zorder=7))
    ax.text((WXL + WXR) / 2, (W + WW) / 2, "NEAR-WALKWAY BUMP-OUT  ·  500mm-deep standing band",
            ha="center", va="center", fontsize=7, color="#1D5A1D", fontweight="bold", **FONT, zorder=12)
    ax.text((nxl + WXL) / 2, W / 2, "300mm\nstd deck", ha="center", va="center",
            fontsize=5.5, color="#206020", **FONT, zorder=12)

    # Wall-cantilever brackets: standard (300mm arm) + widened (500mm arm, heavier)
    for s in stations:
        wide = s in wide_st
        reach = WW if wide else W
        bw = 46 if wide else 30
        ax.add_patch(Rectangle((s - bw / 2, 0), bw, reach,
                               fc=(C_WIDE if wide else C_STD), ec=C_OUT,
                               lw=(1.2 if wide else 0.7), alpha=0.9 if wide else 0.7, zorder=8))

    # Spray-bar pole slit through the bump deck at the beam center
    ax.add_patch(Rectangle((slit_cx - SPRAY_BAR_SLIT_W / 2, 0), SPRAY_BAR_SLIT_W, WW,
                           fc="#C03028", ec=C_OUT, lw=0.8, zorder=10))
    leader(ax, slit_cx + SPRAY_BAR_SLIT_W / 2, WW - 40, slit_cx + 360, WW + 150,
           f"SPRAY-BAR POLE SLIT ({SPRAY_BAR_SLIT_W}mm)\nat pinhole X{slit_cx}",
           color="#C03028", fs=5.5, ha="center", va="bottom", arrow_style="-|>", font=FONT)

    # Bracket callouts — widened (up-right, clear of the notes box) + a small standard tag.
    # Full bracket specs live in the notes + Sheet 7, so keep these short.
    wcx = wide_st[-1]
    leader(ax, wcx, WW - 30, wcx + 150, WW + 175,
           f"WIDENED (×{len(wide_st)})\n500mm arm, 4× M12",
           color=C_WIDE, fs=6, ha="center", va="bottom", arrow_style="-|>", font=FONT)
    std_right = [s for s in stations if s > WXR and s < x1]
    if std_right:
        leader(ax, std_right[0], W - 20, std_right[0] + 30, W + 150,
               "STANDARD\n300mm arm, 3× M12",
               color=C_STD, fs=6, ha="center", va="bottom", arrow_style="-|>", font=FONT)

    # Toward-IBC arrow (the extension direction)
    ax.annotate("", xy=(x1 - 40, -150), xytext=(x1 - 360, -150),
                arrowprops=dict(arrowstyle="-|>", color=C_OUT, lw=1.4))
    ax.text(x1 - 200, -172, "toward IBC", ha="center", va="top", fontsize=6, color=C_OUT, style="italic", **FONT)

    # ── Dimensions ───────────────────────────────────────────────────────────
    draw_dim_v(ax, WXL - 70, 0, WW, f"{WW}mm", offset=6, fs=6, right=False, font=FONT)
    draw_dim_v(ax, nxl - 10, 0, W, f"{W}mm", offset=6, fs=5.5, right=False, font=FONT)
    draw_dim_h(ax, WXL, WXR, WW + 60, f"{int(WXR - WXL)}mm BUMP-OUT (X{WXL}-{WXR})", offset=6, fs=6.5, font=FONT)
    # 100mm deck overhang past the end widened brackets
    draw_dim_h(ax, WXL, wide_st[0], -110, f"{ovh}mm ovh", offset=5, fs=5, above=False, font=FONT)
    draw_dim_h(ax, wide_st[-1], WXR, -110, f"{ovh}mm ovh", offset=5, fs=5, above=False, font=FONT)
    # rib spacing between two widened brackets
    draw_dim_h(ax, wide_st[0], wide_st[1], -200,
               f"{int(WALKWAY_BRACKET_SPACING)}mm rib", offset=5, fs=5, above=False, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        "NEAR-WALKWAY BUMP-OUT (PINHOLE WALL):",
        f"1. Widens {W}->{WW}mm over X{WXL}-{WXR} ({int(WXR - WXL)}mm) — standing room at the",
        "   wall-mounted EP panel + battery bank and full room for spray-bar work.",
        f"2. Carried by {len(wide_st)} WIDENED wall-cantilever brackets (10mm plate, 500mm arm,",
        f"   4× M12) at {int(WALKWAY_BRACKET_SPACING)}mm ribs; deck overhangs the end brackets {ovh}mm.",
        f"3. Extended a 2nd rib toward the IBC so the operator has a full bay PAST the",
        f"   spray-bar pole slit (X{slit_cx}).",
        "4. Standard 300mm-arm brackets flank it. Widened-bracket section on Sheet 7;",
        "   the left drum-exit punch-out counterpart is on Sheet 5.",
    ]
    draw_notes(ax, notes, 700, 1085, spacing=40, fs=6.5, ha="left", width=1950, font=FONT)

    title_block(ax, "SHEET 9 OF 10",
                drawing_title="PERIMETER WALKWAY",
                subtitle="DETAIL F — NEAR-WALKWAY BUMP-OUT (PINHOLE WALL, PLAN)",
                scale_note="Axes in mm · PLAN VIEW (X right, Yd up from pinhole wall)",
                height=0.07)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "walkway-sheet9.png"), dpi=DIAGRAM_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet9.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 10 — Grate cut-plan (GRP nesting)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet10():
    """Sheet 10 — GRATE CUT-PLAN: the 4 molded-FRP grate sections laid out for the fabricator,
    each dimensioned with its cut features (spray-bar slits, drum-exit punch-out, near bump-out,
    muslin notches) and FRP hold-down-clip positions (WF5, 610mm centers + corners). Molded GRP
    ships in 3'×10' (914×3048mm) panels, so the 4049mm near/far runs splice at one seam."""
    C_GRP = "#BFE3C9"; C_CUT = "#C03028"; C_CLIP = "#2060A0"
    W, WW = WALKWAY_W, WALKWAY_NEAR_WIDE_W          # 300 / 500
    RW = WALKWAY_RIGHT_W                            # 245
    nf_len = (PROC_TRAY_X_L + PROC_TRAY_W) - (WALKWAY_LEFT_X + WALKWAY_W)   # 4049
    lr_len = (WALKWAY_FAR_YD + WALKWAY_W) - WALKWAY_NEAR_YD                 # 2362
    pitch = WALKWAY_GRATE_CLIP_PITCH               # 610
    GRP_MAX = 3048                                 # 10 ft molded panel length
    slit_c = PH_X - (WALKWAY_LEFT_X + WALKWAY_W)   # slit X within the near/far piece
    # Spray-slit support: the grate on EACH side of the slit bears on the flanking wall bracket.
    _st = list(np.arange((WALKWAY_LEFT_X + WALKWAY_W) + WALKWAY_BRACKET_SPACING / 2,
                         PROC_TRAY_X_L + PROC_TRAY_W, WALKWAY_BRACKET_SPACING))
    flL = max(s for s in _st if s < PH_X) - (WALKWAY_LEFT_X + WALKWAY_W)   # left flanking bracket (within-piece X)
    flR = min(s for s in _st if s > PH_X) - (WALKWAY_LEFT_X + WALKWAY_W)   # right flanking bracket

    def slit(y, depth):
        """Spray-bar pole slit through the FULL grate depth + the flanking-bracket support marks (▲)."""
        ax.add_patch(Rectangle((slit_c - SPRAY_BAR_SLIT_W / 2, y), SPRAY_BAR_SLIT_W, depth,
                               fc="#FFFFFF", ec=C_CUT, lw=1.1, zorder=6))
        for fx in (flL, flR):
            ax.plot([fx], [y - 20], marker="^", ms=7, color="#208020", zorder=9)   # ▲ bears on a bracket
        ax.text(slit_c, y - 44, f"SLIT X{PH_X}", ha="center", va="top",
                fontsize=5, color=C_CUT, **FONT)
    lw_l, lw_r = WALKWAY_LEFT_WIDE_YD_L, WALKWAY_LEFT_WIDE_YD_R             # punch-out 800-1560
    lw_w = WALKWAY_LEFT_WIDE_W                      # 600
    mn0, mnd, mnw = WALKWAY_MUSLIN_NOTCH_YD0, WALKWAY_MUSLIN_NOTCH_DX, WALKWAY_MUSLIN_NOTCH_DY  # 1912/100/150
    nw_l, nw_r = WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_X_R               # 1165-3193

    fig, ax = plt.subplots(figsize=(18, 11))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(-500, 4400); ax.set_ylim(-700, 3800)
    ax.set_aspect("equal"); ax.axis("off")
    ax.text(1950, 3720, "GRATE CUT-PLAN — 4 molded-FRP sections (nesting / fabricator drawing)",
            ha="center", va="bottom", fontsize=10, color=C_OUT, fontweight="bold", **FONT)

    def clips(x0, x1, y, n_edge=2, ysp=None):
        """Tick the clip positions along a bearing edge from x0..x1 at `pitch`, + the two ends."""
        xs = list(np.arange(x0, x1 + 1, pitch))
        if xs[-1] < x1 - 30:
            xs.append(x1)
        for x in xs:
            ax.plot([x], [y], marker="s", ms=3.4, color=C_CLIP, zorder=9)
        return len(xs)

    def chain(pts, y_dim):
        """A dimension chain along a piece bottom locating every cutout edge (skips <25mm slivers)."""
        for a, b in zip(sorted(set(pts))[:-1], sorted(set(pts))[1:]):
            if b - a >= 25:
                draw_dim_h(ax, a, b, y_dim, f"{b - a:.0f}", offset=3, fs=4.5, above=False, font=FONT)

    y = 2850
    # ── LEFT piece (2362 × 300, punch-out to 600 over Yd800-1560, muslin notch) ──
    ax.add_patch(Rectangle((0, y), lr_len, W, fc=C_GRP, ec=C_OUT, lw=1.4, zorder=5))
    ax.add_patch(Rectangle((lw_l, y + W), lw_r - lw_l, lw_w - W, fc=C_GRP, ec=C_OUT, lw=1.4, zorder=5))  # punch-out
    ax.text(lw_l + (lw_r - lw_l) / 2, y + W + (lw_w - W) / 2, "DRUM-EXIT\nPUNCH-OUT\n600 deep",
            ha="center", va="center", fontsize=6, color="#206020", fontweight="bold", **FONT, zorder=7)
    ax.add_patch(Rectangle((mn0, y), mnw, mnd, fc="#FFFFFF", ec=C_CUT, lw=1.1, ls=(0, (3, 2)), zorder=6))  # muslin notch
    ax.text(0, y + lw_w + 35, "LEFT WALKWAY GRATE (removable lift-out) — 1 pc, no clips (gravity)",
            ha="left", va="bottom", fontsize=7, color=C_OUT, fontweight="bold", **FONT)
    draw_dim_h(ax, 0, lr_len, y - 60, f"{lr_len:.0f}mm", offset=8, fs=6.5, above=False, font=FONT)
    draw_dim_v(ax, -60, y, y + W, f"{W}mm", offset=8, fs=6, right=False, font=FONT)
    # cutout dims — punch-out (width above, 600 depth on the right) + muslin notch depth + position chain
    draw_dim_h(ax, lw_l, lw_r, y + lw_w + 12, f"{lw_r - lw_l:.0f}", offset=4, fs=5.5, font=FONT)
    draw_dim_v(ax, lw_r + 58, y, y + lw_w, f"{lw_w:.0f}", offset=5, fs=5.5, right=True, font=FONT)
    draw_dim_v(ax, mn0 - 26, y, y + mnd, f"{mnd:.0f}", offset=4, fs=5, right=False, font=FONT)
    ax.text(mn0 + mnw + 20, y + mnd / 2, f"MUSLIN NOTCH {mnd}×{mnw}", ha="left", va="center",
            fontsize=5.5, color=C_CUT, **FONT)
    chain([0, lw_l, lw_r, mn0, mn0 + mnw, lr_len], y - 108)

    # ── RIGHT piece (2362 × 245, muslin notch) ──
    y = 2250
    ax.add_patch(Rectangle((0, y), lr_len, RW, fc=C_GRP, ec=C_OUT, lw=1.4, zorder=5))
    ax.add_patch(Rectangle((mn0, y), mnw, mnd, fc="#FFFFFF", ec=C_CUT, lw=1.1, ls=(0, (3, 2)), zorder=6))
    nc = clips(0, lr_len, y - 8) + clips(0, lr_len, y + RW + 8)
    ax.text(0, y + RW + 55, f"RIGHT WALKWAY GRATE (cantilever) — 1 pc · {nc} clips (WF5)",
            ha="left", va="bottom", fontsize=7, color=C_OUT, fontweight="bold", **FONT)
    draw_dim_h(ax, 0, lr_len, y - 60, f"{lr_len:.0f}mm", offset=8, fs=6.5, above=False, font=FONT)
    draw_dim_v(ax, -60, y, y + RW, f"{RW}mm", offset=8, fs=6, right=False, font=FONT)
    # muslin notch — depth + width + position chain
    draw_dim_v(ax, mn0 - 26, y, y + mnd, f"{mnd:.0f}", offset=4, fs=5, right=False, font=FONT)
    ax.text(mn0 + mnw + 20, y + mnd / 2, f"MUSLIN NOTCH {mnd}×{mnw}", ha="left", va="center",
            fontsize=5.5, color=C_CUT, **FONT)
    chain([0, mn0, mn0 + mnw, lr_len], y - 108)

    # ── NEAR piece (4049 × 300, widened to 500 over X1165-3193, spray slit, GRP seam) ──
    y = 1350
    xoff_nw_l = nw_l - (WALKWAY_LEFT_X + WALKWAY_W)   # widened region within the piece
    xoff_nw_r = nw_r - (WALKWAY_LEFT_X + WALKWAY_W)
    ax.add_patch(Rectangle((0, y), nf_len, W, fc=C_GRP, ec=C_OUT, lw=1.4, zorder=5))
    ax.add_patch(Rectangle((xoff_nw_l, y + W), xoff_nw_r - xoff_nw_l, WW - W, fc=C_GRP, ec=C_OUT, lw=1.4, zorder=5))
    ax.text((xoff_nw_l + xoff_nw_r) / 2, y + W + (WW - W) / 2, "BUMP-OUT to 500 (EP/battery)",
            ha="center", va="center", fontsize=6, color="#206020", fontweight="bold", **FONT, zorder=7)
    slit(y, WW)   # the near slit is INSIDE the bump-out → cut the full 500mm depth
    ax.plot([GRP_MAX, GRP_MAX], [y - 20, y + W + 20], color="#A040A0", lw=1.6, ls=(0, (5, 3)), zorder=8)
    ax.text(GRP_MAX, y - 34, f"GRP SEAM\n(3048 panel)", ha="center", va="top", fontsize=5.5, color="#A040A0", **FONT)
    nc = clips(0, nf_len, y - 8) + clips(0, nf_len, y + W + 8)
    ax.text(0, y + W + 260, f"NEAR WALKWAY GRATE — 2 pcs spliced at the seam · {nc} clips (WF5) · spray-bar slit {SPRAY_BAR_SLIT_W}mm",
            ha="left", va="bottom", fontsize=7, color=C_OUT, fontweight="bold", **FONT)
    draw_dim_v(ax, -60, y, y + W, f"{W}mm", offset=8, fs=6, right=False, font=FONT)
    # cutout dims — bump-out (width above, 500 depth on the right) + position chain (incl. the 30 slit);
    # the position chain replaces the overall length line on the long near/far sections (Alvin 2026-08-19)
    draw_dim_h(ax, xoff_nw_l, xoff_nw_r, y + WW + 12, f"{xoff_nw_r - xoff_nw_l:.0f}", offset=4, fs=5.5, font=FONT)
    draw_dim_v(ax, xoff_nw_r + 58, y, y + WW, f"{WW}mm", offset=5, fs=5.5, right=True, font=FONT)
    chain([0, xoff_nw_l, slit_c - SPRAY_BAR_SLIT_W / 2, slit_c + SPRAY_BAR_SLIT_W / 2, xoff_nw_r, GRP_MAX, nf_len], y - 92)

    # ── FAR piece (4049 × 300, spray slit, seam) ──
    y = 650
    ax.add_patch(Rectangle((0, y), nf_len, W, fc=C_GRP, ec=C_OUT, lw=1.4, zorder=5))
    slit(y, W)   # far walkway is uniform 300 (no bump-out) — full 300mm depth
    ax.plot([GRP_MAX, GRP_MAX], [y - 20, y + W + 20], color="#A040A0", lw=1.6, ls=(0, (5, 3)), zorder=8)
    nc = clips(0, nf_len, y - 8) + clips(0, nf_len, y + W + 8)
    ax.text(0, y + W + 55, f"FAR WALKWAY GRATE — 2 pcs spliced at the seam · {nc} clips (WF5) · spray-bar slit {SPRAY_BAR_SLIT_W}mm",
            ha="left", va="bottom", fontsize=7, color=C_OUT, fontweight="bold", **FONT)
    draw_dim_v(ax, -60, y, y + W, f"{W}mm", offset=8, fs=6, right=False, font=FONT)
    chain([0, slit_c - SPRAY_BAR_SLIT_W / 2, slit_c + SPRAY_BAR_SLIT_W / 2, GRP_MAX, nf_len], y - 92)

    # ── Notes / legend ──
    notes = [
        "GRATE CUT-PLAN NOTES:",
        "1. Material: 1\" (25mm) molded GRP, vinyl-ester, grit top (McNichols MS-S-100); ships 3'×10' (914×3048mm).",
        "2. Near/far runs are 4,049mm > the 3,048 panel, so each splices at ONE seam (place clear of the bump-out/slit).",
        f"3. HOLD-DOWN CLIPS (WF5): 316 SS M-clips at {pitch}mm ({int(pitch/25.4+0.5)}\") along both bearing edges + one at each corner (■).",
        "4. LEFT walkway lifts out by gravity — NO clips (removed before panel transport).",
        f"5. SPRAY-BAR SLIT cuts the FULL grate depth (500mm through the near bump-out, 300mm far). The grate on",
        f"   EACH side of the slit bears on the flanking wall bracket (▲, X{int(flL + WALKWAY_LEFT_X + WALKWAY_W)} / X{int(flR + WALKWAY_LEFT_X + WALKWAY_W)}) — both sides supported.",
        "6. Field-seal all cut edges (epoxy kit); cut features: spray-bar slits, drum-exit punch-out (left),",
        "   near bump-out, muslin notches (left+right). All dims from tbs_constants — see report §8 + §10.4.",
    ]
    ax.plot([-380], [460], marker="s", ms=3.4, color=C_CLIP)
    ax.text(-350, 460, "= FRP hold-down clip (WF5)", ha="left", va="center", fontsize=6.5, color=C_CLIP, **FONT)
    draw_notes(ax, notes, -450, 360, spacing=58, fs=7, width=4600, font=FONT)

    title_block(ax, "SHEET 10 OF 10", drawing_title="PERIMETER WALKWAY",
                subtitle="GRATE CUT-PLAN — 4 GRP SECTIONS (nesting) · CLIPS AT 610mm")
    fig.savefig(os.path.join(DIAGRAMS_DIR, "walkway-sheet10.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet10.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    print("Generating perimeter walkway diagrams...")
    sheet1()  # plan view → sheet1.png
    sheet2()  # cross-section → sheet2.png
    sheet3()  # cantilever support → sheet3.png
    sheet4()  # butt joint → sheet4.png
    sheet5()  # left support (floor-leg plan) → sheet5.png
    sheet6()  # floor-leg bracket detail → sheet6.png
    sheet7()  # widened bracket → sheet7.png
    sheet8()  # width transition → sheet8.png
    sheet9()  # drum-exit punch-out support → sheet9.png
    sheet10()  # grate cut-plan (GRP nesting) → sheet10.png
    print("Done.")
