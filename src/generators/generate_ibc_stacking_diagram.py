#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_ibc_stacking_diagram.py  —  TBS-001 IBC Stacking & Securing

Sheet 1 — Cross-section elevation through the IBC stack, looking +X toward
          the sealed end (near/pinhole wall at right, far wall at left):
  Side view showing the 2-tier stack in the right end zone.  Bottom tier
  IBCs sit on the container floor; the stacking frame platform supports
  the top tier.  D-ring lashing points at frame corners.  Container
  ceiling, floor, and right walkway shown for context.

Sheet 2 — Fastening details:
  Detail A: D-ring lashing point (cross-section, welded to frame).
  Detail B: Anti-rotation lip on platform perimeter (cross-section).
  Detail C: Access gate for lower IBC drain valve (front elevation).
"""

import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch, Circle
import matplotlib.patches as mpatches

from tbs_constants import (
    C_LEN, C_WID, C_HGT,
    IBC_COL_X, IBC_W, IBC_D, IBC_H_600, IBC_H_STK,
    BLUE_IBC_Y, BROWN_IBC_Y, IBC_FAR_Y, WASTE_IBC_Y,
    WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T,
    WALKWAY_RIGHT_X,
    C_BLUE_IBC, C_BROWN_IBC, C_WASTE_IBC, C_PUMP,
    PROC_TRAY_RIM,
    EXT_PANEL_YD, EXT_FILL_1_H, EXT_DRAIN_3_H, EXT_DRAIN_4_H,
    EQPANEL_X, EQPANEL_T, EQPANEL_YD,
    PANEL_FRAME_X, PANEL_FRAME_TOP_Z, IBC_FRAME_RHS,
    IBC_FOOT_PLATE, IBC_FOOT_PLATE_T, IBC_FOOT_BOLT_PCD, IBC_FOOT_BOLT_N,
    IBC_WBKT_PLATE_T, IBC_WBKT_SEAT_PROJ, IBC_WBKT_SEAT_T, IBC_WBKT_GUSSET_H,
    PUMP_D, PUMP_YD, PUMP_YD_SPAN,
    BB_OD, FSKID_YD,
    DIAGRAMS_DIR,
)
from tbs_title_block import title_block
from tbs_drawing import (draw_dim_h, draw_dim_v, leader, draw_notes,
                         draw_pipe_path as _tbs_pipe_path,
                         draw_pipe_end as _tbs_pipe_end)

# ── Palette ───────────────────────────────────────────────────────────────────
BG      = "#FFFFFF"
C_OUT   = "#1A1A1A"
C_CL    = "#2060A0"
C_DIM   = "#404040"
C_STEEL = "#B0B0B8"
C_FRAME = "#606068"
C_FLOOR = "#E0DDD8"
C_WALL  = "#C0C0C8"
C_GRATE = "#A0A0A8"
C_RUBBER = "#404040"
C_PORT  = "#708090"
C_PLY   = "#D4C8A0"
FONT    = {"fontfamily": "monospace"}

# ── Frame constants (from equipment-layout-report.md §5) ──────────────────────
FRAME_RHS      = 50     # 50×50×3mm RHS
FRAME_T        = 3      # wall thickness
FRAME_FOOTPRINT_W = C_WID  # frame footprint width (across Yd, wall-to-wall via brackets)
FRAME_FOOTPRINT_D = 1284  # frame footprint depth (along X, 65mm overhang cargo-door side, flush to end wall)
CORRIDOR_W = IBC_FAR_Y - (BLUE_IBC_Y + IBC_D)  # = 270mm plumbing corridor between columns
FRAME_PLATFORM_H  = 1060  # platform height (1010 + 50mm clearance plate)
FRAME_PLATFORM_T  = FRAME_RHS  # platform beam depth = RHS size
FRAME_LIP_H    = 40     # anti-rotation lip height above platform
FRAME_LIP_T    = 5      # lip thickness (steel plate)
FRAME_WEIGHT   = 144    # kg (frame + feet + seat brackets + panel support frame)

# D-ring lashing
DRING_SIZE     = 25     # D-ring strap width (mm)
DRING_STANDOFF = 30     # standoff from frame corner
DRING_WLL      = 1100   # working load limit per ring (kg)

# Access gate
GATE_H         = 300    # gate panel height (mm)
GATE_BOLT_D    = 12     # M12 bolts
GATE_BOLT_N    = 4      # bolts per gate

# Rubber mat
MAT_T          = 12     # anti-slip rubber mat thickness (mm)

# IBC cage post visual width
CAGE_POST_W    = 40     # visual representation of cage uprights

# Gap between near and far columns
IBC_GAP        = IBC_FAR_Y - (BLUE_IBC_Y + IBC_D)  # = 270mm (plumbing corridor)

# Ceiling clearance
CEIL_CLEAR     = C_HGT - IBC_H_STK  # = 368mm

# Fill/drain port
PORT_DIA       = 50     # 2" NPT visual diameter (mm)
FILL_PORT_Z    = 1800   # fill port center height
DRAIN_PORT_Z   = 200    # drain port center height


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — Cross-Section Elevation (looking +X toward sealed end; near/pinhole wall at right, far wall at left)
#
# Horizontal = Yd (0=near/pinhole wall, positive toward far wall)
# Vertical   = Z  (0=floor, positive up)
# Shows both near and far IBC columns with stacking frame between.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():
    def sx(mm): return mm
    def sy(mm): return mm

    # ── Layout bounds ─────────────────────────────────────────────────────────
    YD_LO = -120
    YD_HI = C_WID + 120
    Z_LO  = -580
    Z_HI  = C_HGT + 100

    fig, ax = plt.subplots(figsize=(18, 22))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(sx(YD_LO), sx(YD_HI))
    ax.invert_xaxis()   # match physical view orientation (see sheet header)
    ax.set_ylim(sy(Z_LO), sy(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container shell ───────────────────────────────────────────────────────
    WALL_T = 2.0   # visual wall thickness (mm at this scale)

    # Floor
    ax.add_patch(Rectangle((sx(YD_LO), sy(-30)),
                            sx(YD_HI - YD_LO), sy(30),
                            fc=C_FLOOR, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Ceiling
    ax.add_patch(Rectangle((sx(YD_LO), sy(C_HGT)),
                            sx(YD_HI - YD_LO), sy(30),
                            fc=C_FLOOR, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Near wall (left)
    ax.add_patch(Rectangle((sx(-30), sy(0)),
                            sx(30), sy(C_HGT),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Far wall (right)
    ax.add_patch(Rectangle((sx(C_WID), sy(0)),
                            sx(30), sy(C_HGT),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))

    # Floor/ceiling/wall labels
    ax.text(sx(C_WID / 2), sy(-45), "CONTAINER FLOOR",
            ha="center", va="top", fontsize=6, color=C_DIM, **FONT)
    ax.text(sx(C_WID / 2), sy(C_HGT + 45), "CONTAINER CEILING (Z=2388mm)",
            ha="center", va="bottom", fontsize=6, color=C_DIM, **FONT)
    ax.text(sx(-45), sy(C_HGT / 2), "NEAR\nWALL\n(Yd=0)",
            ha="center", va="center", fontsize=5.5, color=C_DIM, **FONT,
            rotation=90)
    ax.text(sx(C_WID + 45), sy(C_HGT / 2), "FAR\nWALL\n(Yd=2362)",
            ha="center", va="center", fontsize=5.5, color=C_DIM, **FONT,
            rotation=90)

    # Interior face lines
    ax.plot([sx(0), sx(0)], [sy(0), sy(C_HGT)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([sx(C_WID), sx(C_WID)], [sy(0), sy(C_HGT)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([sx(0), sx(C_WID)], [sy(0), sy(0)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([sx(0), sx(C_WID)], [sy(C_HGT), sy(C_HGT)], color=C_OUT, lw=2.0, zorder=3)

    # ── IBCs ──────────────────────────────────────────────────────────────────
    # In this cross-section (looking along X), we see Yd vs Z.
    # Near column: Yd = BLUE_IBC_Y to BLUE_IBC_Y + IBC_D
    # Far column:  Yd = IBC_FAR_Y  to IBC_FAR_Y + IBC_D

    ibc_data = [
        ("IBC-3\nBROWN\n(recycled)", BLUE_IBC_Y, 0, IBC_D, IBC_H_600, C_BROWN_IBC),
        ("IBC-1\nBLUE\n(clean supply)", BLUE_IBC_Y, IBC_H_600 + MAT_T + FRAME_RHS,
         IBC_D, IBC_H_600, C_BLUE_IBC),
        ("IBC-4\nWASTE", IBC_FAR_Y, 0, IBC_D, IBC_H_600, C_WASTE_IBC),
        ("IBC-2\nBLUE\n(clean supply)", IBC_FAR_Y, IBC_H_600 + MAT_T + FRAME_RHS,
         IBC_D, IBC_H_600, C_BLUE_IBC),
    ]

    for label, yd, z, d, h, color in ibc_data:
        # IBC body (translucent tank)
        ax.add_patch(Rectangle((sx(yd), sy(z)),
                                sx(d), sy(h),
                                fc=color, ec=C_OUT, lw=1.5, alpha=0.35, zorder=5))
        # Cage uprights (4 posts at corners)
        for post_yd in [yd + 15, yd + d - 15]:
            ax.add_patch(Rectangle((sx(post_yd - CAGE_POST_W / 2), sy(z)),
                                    sx(CAGE_POST_W), sy(h),
                                    fc="none", ec=C_OUT, lw=0.6, zorder=6))
        # Cage top rail
        ax.plot([sx(yd), sx(yd + d)], [sy(z + h), sy(z + h)],
                color=C_OUT, lw=1.2, zorder=6)
        # Label
        ax.text(sx(yd + d / 2), sy(z + h / 2), label,
                ha="center", va="center", fontsize=7, color=C_OUT,
                fontweight="bold", **FONT, zorder=10)

    # ── Stacking frame (portal frame with open plumbing corridor) ───────────
    # Wall-side restraint via brackets; corridor uprights at inner IBC edges.
    # Platform and top beams span each column; cross-beams bridge the corridor.
    near_col_r = BLUE_IBC_Y + IBC_D    # = 1046mm (near column right edge)
    far_col_l  = IBC_FAR_Y             # = 1316mm (far column left edge)
    platform_z = IBC_H_600  # platform sits on top of bottom IBCs

    # Corridor uprights (4 visible as 2 near-corridor + 2 far-corridor)
    corridor_uprights = [near_col_r, far_col_l - FRAME_RHS]
    for uyd in corridor_uprights:
        ax.add_patch(Rectangle((sx(uyd), sy(0)),
                                sx(FRAME_RHS), sy(IBC_H_STK + FRAME_RHS),
                                fc=C_FRAME, ec=C_OUT, lw=1.2, zorder=7,
                                alpha=0.8))
        ax.add_patch(Rectangle((sx(uyd + FRAME_T), sy(FRAME_T)),
                                sx(FRAME_RHS - 2 * FRAME_T),
                                sy(IBC_H_STK + FRAME_RHS - 2 * FRAME_T),
                                fc=C_WALL, ec="none", lw=0, zorder=7,
                                alpha=0.3))

    # ── Wall seat brackets: welded knee bracket (vertical back-plate + horizontal
    # seat + triangular gusset web + M12 wall anchors) props each platform-beam
    # OUTER end against the container wall, turning the cantilever into a simple
    # span. Matches the 3D "Wall Bracket Plate / Seat / Gusset" fabrication
    # (~110 kg each, one per X-station per wall). ──
    C_BOLT    = "#3A3A42"
    seat_top  = platform_z              # 1010 — platform-beam end lands here
    proj      = IBC_WBKT_SEAT_PROJ      # seat projection into container (Yd)
    seat_t    = IBC_WBKT_SEAT_T         # seat plate thickness
    gh        = IBC_WBKT_GUSSET_H       # gusset web depth below the seat
    plate_t   = IBC_WBKT_PLATE_T        # back-plate thickness (against wall)
    seat_bot  = seat_top - seat_t
    guss_bot  = seat_bot - gh
    plate_top = seat_top + 10
    for wyd, dir_in in [(0, 1), (C_WID, -1)]:
        tip      = wyd + dir_in * proj
        plate_x0 = wyd if dir_in > 0 else wyd - plate_t
        seat_x0  = min(wyd, tip)
        # vertical back-plate bolted to the wall
        ax.add_patch(Rectangle((sx(plate_x0), sy(guss_bot)),
                                sx(plate_t), sy(plate_top - guss_bot),
                                fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=8))
        # horizontal seat the platform-beam end rests on
        ax.add_patch(Rectangle((sx(seat_x0), sy(seat_bot)),
                                sx(proj), sy(seat_t),
                                fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=8))
        # triangular gusset web welded between back-plate and seat tip
        ax.add_patch(Polygon([(sx(tip), sy(seat_bot)),
                              (sx(wyd), sy(seat_bot)),
                              (sx(wyd), sy(guss_bot))],
                             closed=True, fc=C_STEEL, ec=C_OUT, lw=1.0,
                             hatch="\\\\", zorder=8))
        # 2× visible M12 wall anchor bolt heads on the back-plate
        for bz in (guss_bot + 40, seat_bot - 25):
            ax.add_patch(Circle((sx(wyd + dir_in * plate_t / 2), sy(bz)), sy(7),
                                fc=C_BOLT, ec=C_OUT, lw=0.6, zorder=9))

    # Annotate the wall seat bracket (near-wall instance; typical at both walls)
    leader(ax, sx(45), sy(seat_bot - gh / 2), sx(-55), sy(720),
           "WALL SEAT BRACKET (TYP. ×6)\nWelded knee: back-plate + seat +\ntriangular gusset web,\n4× M12 wall anchors",
           color=C_FRAME, fs=6, ha="left", va="top",
           arrow_style="-|>", font=FONT)

    # ── Floor flange feet: a 150×150×12 plate fillet-welded to each corridor
    # upright base, sitting ON the floor surface and bolted down with 4× M12
    # anchors through the plate into the slab (uplift + lateral restraint).
    # Matches the 3D "Foot Flange Plate / Foot Anchor Bolt" parts. ──
    foot_half = IBC_FOOT_PLATE / 2
    for uyd in corridor_uprights:
        fcy = uyd + IBC_FRAME_RHS / 2               # foot centerd on the upright
        # flange plate sits ON the floor surface (Z 0 .. t)
        ax.add_patch(Rectangle((sx(fcy - foot_half), sy(0)),
                                sx(IBC_FOOT_PLATE), sy(IBC_FOOT_PLATE_T),
                                fc=C_STEEL, ec=C_OUT, lw=1.4, zorder=8))
        # 4× M12 anchors (2 visible) through the plate down into the floor slab
        for d in (-IBC_FOOT_BOLT_PCD / 2, IBC_FOOT_BOLT_PCD / 2):
            ax.plot([sx(fcy + d), sx(fcy + d)],
                    [sy(IBC_FOOT_PLATE_T), sy(-26)],
                    color=C_BOLT, lw=1.8, zorder=9)
            ax.plot(sx(fcy + d), sy(IBC_FOOT_PLATE_T), 'o',
                    color=C_BOLT, ms=3.5, mew=0, zorder=9)
    leader(ax, sx(corridor_uprights[0] + IBC_FRAME_RHS / 2), sy(IBC_FOOT_PLATE_T),
           sx((near_col_r + far_col_l) / 2), sy(320),
           "FLOOR FLANGE FOOT (TYP. ×6)\n150×150×12 plate on floor,\n4× M12 floor anchors",
           color=C_FRAME, fs=6, ha="center", va="bottom",
           arrow_style="-|>", font=FONT)

    # Platform beams — one per column (not spanning corridor)
    for col_l, col_r in [(BLUE_IBC_Y - 5, near_col_r + FRAME_RHS),
                          (far_col_l - FRAME_RHS, IBC_FAR_Y + IBC_D + 5)]:
        ax.add_patch(Rectangle((sx(col_l), sy(platform_z)),
                                sx(col_r - col_l), sy(FRAME_RHS),
                                fc=C_FRAME, ec=C_OUT, lw=1.5, zorder=7, alpha=0.85))
        ax.add_patch(Rectangle((sx(col_l + FRAME_T), sy(platform_z + FRAME_T)),
                                sx(col_r - col_l - 2 * FRAME_T),
                                sy(FRAME_RHS - 2 * FRAME_T),
                                fc="#D0D0D0", ec="none", zorder=7, alpha=0.4))

    # Cross-beam across corridor (at platform and top levels)
    corr_beam_l = near_col_r + FRAME_RHS
    corr_beam_r = far_col_l - FRAME_RHS
    for bz in [platform_z, IBC_H_STK]:
        ax.add_patch(Rectangle((sx(corr_beam_l), sy(bz)),
                                sx(corr_beam_r - corr_beam_l), sy(FRAME_RHS),
                                fc=C_FRAME, ec=C_OUT, lw=1.0, zorder=6, alpha=0.5))

    # Anti-slip rubber mat on platform (one per column)
    mat_z = platform_z + FRAME_RHS
    for col_l, col_r in [(BLUE_IBC_Y, near_col_r),
                          (IBC_FAR_Y, IBC_FAR_Y + IBC_D)]:
        ax.add_patch(Rectangle((sx(col_l), sy(mat_z)),
                                sx(col_r - col_l), sy(MAT_T),
                                fc=C_RUBBER, ec=C_OUT, lw=0.8, zorder=8, alpha=0.7))

    # Anti-rotation lip (corridor-side of each column)
    lip_z = mat_z + MAT_T
    for lip_yd in [near_col_r - FRAME_LIP_T,
                   IBC_FAR_Y]:
        ax.add_patch(Rectangle((sx(lip_yd), sy(lip_z - 5)),
                                sx(FRAME_LIP_T), sy(FRAME_LIP_H),
                                fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=9))

    # Top rail — one per column
    top_z = IBC_H_STK
    for col_l, col_r in [(BLUE_IBC_Y - 5, near_col_r + FRAME_RHS),
                          (far_col_l - FRAME_RHS, IBC_FAR_Y + IBC_D + 5)]:
        ax.add_patch(Rectangle((sx(col_l), sy(top_z)),
                                sx(col_r - col_l), sy(FRAME_RHS),
                                fc=C_FRAME, ec=C_OUT, lw=1.2, zorder=7, alpha=0.85))

    # Corridor label
    corr_cx = (near_col_r + far_col_l) / 2
    ax.text(sx(corr_cx), sy(platform_z / 2 + 30),
            f"PLUMBING\nCORRIDOR\n{IBC_GAP}mm",
            ha="center", va="center", fontsize=6.5, color=C_CL,
            fontweight="bold", **FONT, zorder=15)

    # ── D-ring lashing points (4 per tier, showing 2 near-side) ───────────────
    dring_color = "#D0A030"
    # Bottom tier D-rings: near corners at Z ≈ FRAME_RHS/2
    # Top tier D-rings: at Z ≈ platform_z + FRAME_RHS + IBC_H_600/2
    dring_positions = [
        (near_col_r + FRAME_RHS + 5, FRAME_RHS * 1.5, "BOTTOM"),
        (far_col_l - FRAME_RHS - 5, FRAME_RHS * 1.5, "BOTTOM"),
        (near_col_r + FRAME_RHS + 5, platform_z + FRAME_RHS * 1.5, "TOP"),
        (far_col_l - FRAME_RHS - 5, platform_z + FRAME_RHS * 1.5, "TOP"),
    ]
    for dyd, dz, tier in dring_positions:
        # D-ring as a small D shape
        ring_r = 18
        # Mount plate
        plate_w = 35
        plate_h = 8
        if dyd < C_WID / 2:
            plate_x = dyd + 5
        else:
            plate_x = dyd - plate_w - 5
        ax.add_patch(Rectangle((sx(plate_x), sy(dz - plate_h / 2)),
                                sx(plate_w), sy(plate_h),
                                fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=10))
        # D-ring arc
        ring_x = dyd - 10 if dyd < C_WID / 2 else dyd + 10
        ax.add_patch(Circle((sx(ring_x), sy(dz)),
                             sy(ring_r), fc="none", ec=dring_color,
                             lw=2.5, zorder=11))

    # D-ring label (one leader for all)
    leader(ax, sx(near_col_r + FRAME_RHS + 20), sy(FRAME_RHS * 1.5),
           sx(near_col_r + FRAME_RHS + CORRIDOR_W), sy(FRAME_RHS * 1.5 + 120),
           f"D-RING LASHING POINT\n25mm, {DRING_WLL}kg WLL\n8x TOTAL (4 PER TIER)\nMcMaster #3641T29",
           color=dring_color, fs=6.5,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # ── Access gate (lower tier, shown on near column corridor side) ──────────
    gate_yd = near_col_r
    gate_w = IBC_D - 2 * FRAME_RHS
    ax.add_patch(Rectangle((sx(BLUE_IBC_Y + FRAME_RHS), sy(0)),
                            sx(gate_w), sy(GATE_H),
                            fc="none", ec="#C04040", lw=2.0, ls="--", zorder=8))
    # Bolt symbols at gate corners
    for byd in [BLUE_IBC_Y + FRAME_RHS + 20, BLUE_IBC_Y + FRAME_RHS + gate_w - 20]:
        for bz in [30, GATE_H - 30]:
            ax.add_patch(Circle((sx(byd), sy(bz)), sy(6),
                                 fc="#C04040", ec=C_OUT, lw=0.5, zorder=12))

    leader(ax, sx(BLUE_IBC_Y + FRAME_RHS + gate_w / 2), sy(GATE_H),
           sx(BLUE_IBC_Y + FRAME_RHS + gate_w / 2 - 50), sy(GATE_H + 50),
           f"ACCESS GATE (x2)\nREMOVABLE PANEL\nH=0-{GATE_H}mm\n4x M{GATE_BOLT_D} BOLTS\n(DRAIN VALVE ACCESS)",
           color="#C04040", fs=6,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # ── Labels ────────────────────────────────────────────────────────────────
    # Frame label
    leader(ax, sx(near_col_r + FRAME_RHS / 2), sy(IBC_H_600 / 2),
           sx(near_col_r + FRAME_RHS + 20), sy(IBC_H_600 / 2 + 50),
           f"STACKING FRAME\n50x50x3mm RHS\nMILD STEEL\n~{FRAME_WEIGHT}kg",
           color=C_FRAME, fs=6.5,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # Platform label
    leader(ax, sx(BLUE_IBC_Y + IBC_D / 2), sy(platform_z + FRAME_RHS / 2),
           sx(BLUE_IBC_Y - 80), sy(platform_z + 180),
           f"PLATFORM BEAM\n50x50x3mm RHS\n+ {MAT_T}mm RUBBER MAT\n+ {FRAME_LIP_H}mm ANTI-ROTATION LIP",
           color=C_FRAME, fs=6,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # ── Dimension lines ───────────────────────────────────────────────────────
    # IBC height (bottom tier)
    draw_dim_v(ax, sx(IBC_FAR_Y + IBC_D + 80), sy(0), sy(IBC_H_600),
               f"{IBC_H_600}mm\nIBC HEIGHT", offset=sx(8), fs=6, right=True, font=FONT)

    # Stack total height
    draw_dim_v(ax, sx(IBC_FAR_Y + IBC_D + 160), sy(0), sy(IBC_H_STK + FRAME_RHS),
               f"{IBC_H_STK + FRAME_RHS}mm\nSTACK + FRAME", offset=sx(8), fs=6,
               right=True, font=FONT)

    # Ceiling clearance
    draw_dim_v(ax, sx(IBC_FAR_Y + IBC_D + 160), sy(IBC_H_STK + FRAME_RHS), sy(C_HGT),
               f"{CEIL_CLEAR - FRAME_RHS}mm\nCLEARANCE", offset=sx(8), fs=6,
               right=True, font=FONT)

    # Container interior width
    draw_dim_h(ax, sx(0), sx(C_WID), sy(-60),
               f"{C_WID}mm  INTERIOR WIDTH", offset=sy(5), fs=6.5, font=FONT)

    # Near column Yd position
    draw_dim_h(ax, sx(0), sx(BLUE_IBC_Y), sy(IBC_H_600 + 80),
               f"{BLUE_IBC_Y}mm", offset=sy(5), fs=5.5, font=FONT)

    # IBC depth
    draw_dim_h(ax, sx(BLUE_IBC_Y), sx(BLUE_IBC_Y + IBC_D), sy(IBC_H_600 + 80),
               f"{IBC_D}mm\nIBC DEPTH", offset=sy(5), fs=5.5, font=FONT)

    # Plumbing corridor between columns
    draw_dim_h(ax, sx(BLUE_IBC_Y + IBC_D), sx(IBC_FAR_Y), sy(IBC_H_600 + 80),
               f"{IBC_GAP}mm\nCORRIDOR", offset=sy(5), fs=5.5, font=FONT)

    # ── Right walkway (ghost, for context) ────────────────────────────────────
    # The right walkway is at the IBC end, perpendicular to this view
    # Show as a note/context only
    ax.text(sx(C_WID / 2), sy(C_HGT + 80),
            f"CEILING CLEARANCE: {CEIL_CLEAR}mm (transport safe \u2714)",
            ha="center", va="bottom", fontsize=7, color="#206020",
            fontweight="bold", **FONT, zorder=15)

    # ── Notes ─────────────────────────────────────────────────────────────────
    notes = [
        "CROSS-SECTION NOTES:",
        "1. Section through IBC stack, looking +X toward sealed end (near/pinhole wall at right, far wall at left).",
        f"2. 4x 600L IBCs (Schutz Ecobulk MX). Each: 55kg tare, {IBC_W}x{IBC_D}x{IBC_H_600}mm.",
        f"3. Portal frame: 50x50x3mm RHS mild steel, welded wall seat brackets (knee + gusset web, M12 anchors) + corridor uprights on {IBC_FOOT_PLATE}x{IBC_FOOT_PLATE}x{IBC_FOOT_PLATE_T} floor flange feet ({IBC_FOOT_BOLT_N}x M12 anchors each). ~{FRAME_WEIGHT}kg.",
        f"4. {IBC_GAP}mm plumbing corridor between columns for internal pipe routing.",
        f"5. Platform at Z={IBC_H_600}mm + {MAT_T}mm rubber anti-slip mat.",
        f"6. {FRAME_LIP_H}mm steel lip retains upper IBC cage against lateral movement.",
        f"7. 8x D-ring lashing points (4 per tier), {DRING_WLL}kg WLL each.",
        f"8. External plumbing panel on end wall centerline (see Sheets 3-4).",
    ]
    draw_notes(ax, notes, sx(C_WID / 2), sy(Z_LO + 480), spacing=sy(22),
               fs=7, ha="left", font=FONT, width=3800)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 5",
                drawing_title="IBC STACKING & SECURING",
                subtitle="CROSS-SECTION ELEVATION — 2x2 STACK IN RIGHT END ZONE",
                scale_note="Axes in mm - SECTION LOOKING +X (PINHOLE WALL AT RIGHT)",
                height=0.06)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "ibc-stacking-sheet1.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-stacking-sheet1.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Fastening Details
#
# Three detail views:
#   A — D-ring lashing point cross-section
#   B — Anti-rotation lip on platform perimeter
#   C — Access gate front elevation
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():
    def sx(mm): return mm
    def sy(mm): return mm

    fig, ax = plt.subplots(figsize=(20, 22))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, sx(600))
    ax.set_ylim(sy(-100), sy(500))
    ax.set_aspect("equal")
    ax.axis("off")

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL A — D-Ring Lashing Point (cross-section)
    # Shows frame RHS member with welded D-ring plate and ring
    # ══════════════════════════════════════════════════════════════════════════
    DA_OX = 30
    DA_OY = 280

    ax.text(sx(DA_OX + 80), sy(DA_OY + 190),
            "DETAIL A — D-RING LASHING POINT\n(CROSS-SECTION, WELDED TO FRAME)",
            ha="center", va="bottom", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # Frame RHS member (cross-section)
    rhs_x = DA_OX + 40
    rhs_y = DA_OY + 50
    ax.add_patch(Rectangle((sx(rhs_x), sy(rhs_y)),
                            sx(FRAME_RHS), sy(FRAME_RHS),
                            fc=C_FRAME, ec=C_OUT, lw=2.0, zorder=5))
    # Hollow
    ax.add_patch(Rectangle((sx(rhs_x + FRAME_T), sy(rhs_y + FRAME_T)),
                            sx(FRAME_RHS - 2 * FRAME_T), sy(FRAME_RHS - 2 * FRAME_T),
                            fc="#D8D8D8", ec=C_OUT, lw=0.8, zorder=6))
    ax.text(sx(rhs_x + FRAME_RHS / 2), sy(rhs_y + FRAME_RHS / 2),
            f"{FRAME_RHS}x{FRAME_RHS}\nx{FRAME_T} RHS",
            ha="center", va="center", fontsize=6, color=C_OUT, **FONT, zorder=10)

    # Mounting plate (welded to frame face)
    plate_t = 6
    plate_h = 80
    plate_x = rhs_x - plate_t
    plate_y = rhs_y + (FRAME_RHS - plate_h) / 2
    ax.add_patch(Rectangle((sx(plate_x), sy(plate_y)),
                            sx(plate_t), sy(plate_h),
                            fc=C_STEEL, ec=C_OUT, lw=1.5, hatch="///", zorder=7))

    # Weld symbols (triangles at plate-frame junction)
    for wy in [plate_y + 5, plate_y + plate_h - 5]:
        weld_verts = [
            (sx(rhs_x), sy(wy)),
            (sx(rhs_x - 2), sy(wy + 5)),
            (sx(rhs_x - 2), sy(wy - 5)),
        ]
        ax.add_patch(Polygon(weld_verts, closed=True,
                             fc="#404040", ec=C_OUT, lw=0.5, zorder=8))

    # D-ring (side view — D shape)
    ring_cx = plate_x - 25
    ring_cy = rhs_y + FRAME_RHS / 2
    ring_r = 20
    # Draw as a D: flat side against plate, curved side outward
    theta = np.linspace(-np.pi / 2, np.pi / 2, 50)
    ring_xs = [sx(ring_cx + ring_r * np.cos(t)) for t in theta]
    ring_ys = [sy(ring_cy + ring_r * np.sin(t)) for t in theta]
    # Close the D with straight side
    ring_xs = [sx(plate_x - 2)] + ring_xs + [sx(plate_x - 2)]
    ring_ys = [sy(ring_cy - ring_r)] + ring_ys + [sy(ring_cy + ring_r)]
    ax.plot(ring_xs, ring_ys, color="#D0A030", lw=3.5, zorder=9,
            solid_capstyle="round")

    # D-ring pin through plate
    pin_r = 4
    ax.add_patch(Circle((sx(plate_x - 1), sy(ring_cy - ring_r + 3)),
                         sx(pin_r), fc="#808080", ec=C_OUT, lw=1.0, zorder=10))
    ax.add_patch(Circle((sx(plate_x - 1), sy(ring_cy + ring_r - 3)),
                         sx(pin_r), fc="#808080", ec=C_OUT, lw=1.0, zorder=10))

    # Labels
    leader(ax, sx(ring_cx - ring_r), sy(ring_cy),
           sx(ring_cx - 55), sy(ring_cy + 40),
           f"25mm D-RING\n{DRING_WLL}kg WLL\nMcMaster #3641T29",
           color="#D0A030", fs=6.5,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    leader(ax, sx(plate_x + plate_t / 2), sy(plate_y + plate_h + 3),
           sx(plate_x + 40), sy(plate_y + plate_h + 30),
           f"MOUNTING PLATE\n{plate_t}mm STEEL\nFILLET WELDED",
           color=C_STEEL, fs=6,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # Dimensions
    draw_dim_h(ax, sx(plate_x), sx(plate_x + plate_t), sy(rhs_y - 15),
               f"{plate_t}mm", offset=sy(3), fs=5.5, font=FONT)
    draw_dim_v(ax, sx(rhs_x + FRAME_RHS + 10), sy(rhs_y), sy(rhs_y + FRAME_RHS),
               f"{FRAME_RHS}mm", offset=sx(3), fs=5.5, right=True, font=FONT)

    # Detail A border
    ax.add_patch(Rectangle((sx(DA_OX - 5), sy(DA_OY)),
                            sx(180), sy(190),
                            fc="none", ec=C_DIM, lw=0.8, ls="--", zorder=1))

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL B — Anti-Rotation Lip (cross-section through platform edge)
    # Shows platform beam, rubber mat, lip, and IBC cage foot
    # ══════════════════════════════════════════════════════════════════════════
    DB_OX = 240
    DB_OY = 280

    ax.text(sx(DB_OX + 100), sy(DB_OY + 190),
            "DETAIL B — ANTI-ROTATION LIP\n(CROSS-SECTION THROUGH PLATFORM EDGE)",
            ha="center", va="bottom", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # Platform beam (cross-section)
    beam_x = DB_OX + 20
    beam_y = DB_OY + 30
    beam_show_w = 140  # show wider to give context
    ax.add_patch(Rectangle((sx(beam_x), sy(beam_y)),
                            sx(beam_show_w), sy(FRAME_RHS),
                            fc=C_FRAME, ec=C_OUT, lw=2.0, zorder=5))
    # Hollow
    ax.add_patch(Rectangle((sx(beam_x + FRAME_T), sy(beam_y + FRAME_T)),
                            sx(beam_show_w - 2 * FRAME_T), sy(FRAME_RHS - 2 * FRAME_T),
                            fc="#D8D8D8", ec=C_OUT, lw=0.8, zorder=6))
    ax.text(sx(beam_x + beam_show_w / 2), sy(beam_y + FRAME_RHS / 2),
            f"PLATFORM BEAM\n{FRAME_RHS}x{FRAME_RHS}x{FRAME_T} RHS",
            ha="center", va="center", fontsize=5.5, color=C_OUT, **FONT, zorder=10)

    # Rubber mat on top of beam
    mat_y = beam_y + FRAME_RHS
    ax.add_patch(Rectangle((sx(beam_x + 5), sy(mat_y)),
                            sx(beam_show_w - 10), sy(MAT_T),
                            fc=C_RUBBER, ec=C_OUT, lw=1.0, zorder=7, alpha=0.8))
    ax.text(sx(beam_x + beam_show_w / 2), sy(mat_y + MAT_T / 2),
            f"{MAT_T}mm RUBBER MAT", ha="center", va="center",
            fontsize=5, color="white", fontweight="bold", **FONT, zorder=10)

    # Anti-rotation lip (left edge = near frame edge)
    lip_x = beam_x
    lip_y = mat_y
    ax.add_patch(Rectangle((sx(lip_x), sy(lip_y)),
                            sx(FRAME_LIP_T), sy(FRAME_LIP_H),
                            fc=C_STEEL, ec=C_OUT, lw=1.5, hatch="///", zorder=8))

    # Weld at lip base
    weld_verts = [
        (sx(lip_x + FRAME_LIP_T), sy(lip_y)),
        (sx(lip_x + FRAME_LIP_T + 5), sy(lip_y + 5)),
        (sx(lip_x + FRAME_LIP_T + 5), sy(lip_y - 3)),
    ]
    ax.add_patch(Polygon(weld_verts, closed=True,
                         fc="#404040", ec=C_OUT, lw=0.5, zorder=9))

    # IBC cage foot (ghost — sitting on mat, restrained by lip)
    cage_foot_x = lip_x + FRAME_LIP_T + 3
    cage_foot_y = mat_y + MAT_T
    cage_foot_w = 50
    cage_foot_h = 30
    ax.add_patch(Rectangle((sx(cage_foot_x), sy(cage_foot_y)),
                            sx(cage_foot_w), sy(cage_foot_h),
                            fc=C_BLUE_IBC, ec=C_OUT, lw=1.2, ls="--",
                            alpha=0.3, zorder=7))
    ax.text(sx(cage_foot_x + cage_foot_w / 2), sy(cage_foot_y + cage_foot_h / 2),
            "IBC CAGE\nFOOT", ha="center", va="center",
            fontsize=5, color=C_BLUE_IBC, **FONT, zorder=10)

    # Arrow showing lip prevents lateral movement
    arr_x = lip_x - 8
    ax.annotate("", xy=(sx(lip_x + 1), sy(lip_y + FRAME_LIP_H / 2)),
                xytext=(sx(lip_x - 25), sy(lip_y + FRAME_LIP_H / 2)),
                arrowprops=dict(arrowstyle="->", color="#C04040", lw=2.0))
    ax.text(sx(lip_x - 28), sy(lip_y + FRAME_LIP_H / 2),
            "LATERAL\nRETAINED", ha="right", va="center",
            fontsize=5.5, color="#C04040", fontweight="bold", **FONT, zorder=15)

    # Labels
    leader(ax, sx(lip_x + FRAME_LIP_T / 2), sy(lip_y + FRAME_LIP_H),
           sx(lip_x + 50), sy(lip_y + FRAME_LIP_H + 35),
           f"ANTI-ROTATION LIP\n{FRAME_LIP_T}mm STEEL x {FRAME_LIP_H}mm H\nFILLET WELDED TO PLATFORM\nFULL PERIMETER",
           color=C_STEEL, fs=6,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # Dimensions
    draw_dim_v(ax, sx(lip_x - 12), sy(lip_y), sy(lip_y + FRAME_LIP_H),
               f"{FRAME_LIP_H}mm", offset=sx(3), fs=5.5, right=False, font=FONT)
    draw_dim_v(ax, sx(beam_x - 12), sy(beam_y), sy(mat_y),
               f"{FRAME_RHS}mm", offset=sx(3), fs=5.5, right=False, font=FONT)
    draw_dim_v(ax, sx(beam_x + beam_show_w + 10), sy(mat_y), sy(mat_y + MAT_T),
               f"{MAT_T}", offset=sx(3), fs=5, right=True, font=FONT)

    # Detail B border
    ax.add_patch(Rectangle((sx(DB_OX - 5), sy(DB_OY)),
                            sx(220), sy(190),
                            fc="none", ec=C_DIM, lw=0.8, ls="--", zorder=1))

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL C — Access Gate (front elevation)
    # Shows removable panel at base of frame for lower IBC drain valve access
    # ══════════════════════════════════════════════════════════════════════════
    DC_OX = 30
    DC_OY = 20

    ax.text(sx(DC_OX + 170), sy(DC_OY + 230),
            "DETAIL C — ACCESS GATE\n(FRONT ELEVATION — LOWER IBC DRAIN VALVE ACCESS)",
            ha="center", va="bottom", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # Frame uprights (two verticals)
    upright_h = 200
    upright_l_x = DC_OX + 30
    upright_r_x = DC_OX + 30 + 250
    for ux in [upright_l_x, upright_r_x]:
        ax.add_patch(Rectangle((sx(ux), sy(DC_OY + 10)),
                                sx(FRAME_RHS), sy(upright_h),
                                fc=C_FRAME, ec=C_OUT, lw=1.5, zorder=5))
        ax.add_patch(Rectangle((sx(ux + FRAME_T), sy(DC_OY + 10 + FRAME_T)),
                                sx(FRAME_RHS - 2 * FRAME_T),
                                sy(upright_h - 2 * FRAME_T),
                                fc="#D8D8D8", ec=C_OUT, lw=0.5, zorder=6))

    # Gate panel (removable, shown between uprights)
    gate_x = upright_l_x + FRAME_RHS
    gate_w = upright_r_x - gate_x
    gate_y = DC_OY + 10
    gate_panel_h = 120  # visual gate height at this scale
    ax.add_patch(Rectangle((sx(gate_x), sy(gate_y)),
                            sx(gate_w), sy(gate_panel_h),
                            fc="#F0E0E0", ec="#C04040", lw=2.0, zorder=7))
    # Cross pattern on gate (mesh/perforated)
    for frac in np.arange(0.15, 1.0, 0.2):
        ax.plot([sx(gate_x + gate_w * frac), sx(gate_x + gate_w * frac)],
                [sy(gate_y + 5), sy(gate_y + gate_panel_h - 5)],
                color="#C04040", lw=0.5, alpha=0.3, zorder=8)

    ax.text(sx(gate_x + gate_w / 2), sy(gate_y + gate_panel_h / 2),
            f"REMOVABLE GATE PANEL\nH=0-{GATE_H}mm\n(BOLTED — 4x M{GATE_BOLT_D})",
            ha="center", va="center", fontsize=6, color="#C04040",
            fontweight="bold", **FONT, zorder=10)

    # Bolt positions (4 corners of gate)
    bolt_inset = 15
    for bx in [gate_x + bolt_inset, gate_x + gate_w - bolt_inset]:
        for by in [gate_y + bolt_inset, gate_y + gate_panel_h - bolt_inset]:
            ax.add_patch(Circle((sx(bx), sy(by)), sx(5),
                                 fc="#808080", ec=C_OUT, lw=1.0, zorder=12))
            # Hex nut symbol
            ax.add_patch(Circle((sx(bx), sy(by)), sx(8),
                                 fc="none", ec=C_OUT, lw=0.6, zorder=12))

    # IBC valve behind gate (ghost)
    valve_x = gate_x + gate_w / 2 - 20
    valve_y = gate_y + 20
    ax.add_patch(Rectangle((sx(valve_x), sy(valve_y)),
                            sx(40), sy(25),
                            fc=C_BLUE_IBC, ec=C_OUT, lw=1.0, ls="--",
                            alpha=0.25, zorder=6))
    ax.text(sx(valve_x + 20), sy(valve_y + 12),
            "2\" BALL\nVALVE", ha="center", va="center",
            fontsize=4.5, color=C_BLUE_IBC, **FONT, zorder=10)

    # Labels
    leader(ax, sx(gate_x + gate_w + 15), sy(gate_y + gate_panel_h / 2),
           sx(gate_x + gate_w + 60), sy(gate_y + gate_panel_h + 30),
           f"GATE REMOVED FOR\nDRAIN VALVE ACCESS\n(2x GATES — NEAR/FAR COLUMNS)",
           color="#C04040", fs=6,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    leader(ax, sx(upright_l_x + FRAME_RHS / 2), sy(DC_OY + 10 + upright_h),
           sx(upright_l_x - 30), sy(DC_OY + 10 + upright_h + 20),
           f"FRAME UPRIGHT\n{FRAME_RHS}x{FRAME_RHS}x{FRAME_T} RHS",
           color=C_FRAME, fs=6,
           ha="right", va="bottom", arrow_style="-|>", font=FONT)

    # Dimensions
    draw_dim_v(ax, sx(upright_l_x - 15), sy(gate_y), sy(gate_y + gate_panel_h),
               f"{GATE_H}mm\nGATE H", offset=sx(3), fs=5.5, right=False, font=FONT)
    draw_dim_h(ax, sx(gate_x), sx(gate_x + gate_w), sy(gate_y - 15),
               "GATE WIDTH", offset=sy(3), fs=5.5, font=FONT)

    # Detail C border
    ax.add_patch(Rectangle((sx(DC_OX - 5), sy(DC_OY)),
                            sx(350), sy(230),
                            fc="none", ec=C_DIM, lw=0.8, ls="--", zorder=1))

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL D — Lashing Arrangement (schematic top-down showing strap routing)
    # ══════════════════════════════════════════════════════════════════════════
    DD_OX = 400
    DD_OY = 20

    ax.text(sx(DD_OX + 90), sy(DD_OY + 230),
            "DETAIL D — TRANSPORT LASHING\n(SCHEMATIC — STRAP ROUTING)",
            ha="center", va="bottom", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # Simplified side elevation showing IBC with ratchet strap
    sch_x = DD_OX + 20
    sch_y = DD_OY + 20
    sch_w = 140  # IBC width representation
    sch_h = 180  # full stack height representation

    # IBC stack (simplified)
    ax.add_patch(Rectangle((sx(sch_x), sy(sch_y)),
                            sx(sch_w), sy(sch_h / 2),
                            fc=C_BROWN_IBC, ec=C_OUT, lw=1.2, alpha=0.3, zorder=5))
    ax.add_patch(Rectangle((sx(sch_x), sy(sch_y + sch_h / 2 + 5)),
                            sx(sch_w), sy(sch_h / 2),
                            fc=C_BLUE_IBC, ec=C_OUT, lw=1.2, alpha=0.3, zorder=5))
    ax.text(sx(sch_x + sch_w / 2), sy(sch_y + sch_h / 4),
            "BOTTOM\nTIER", ha="center", va="center", fontsize=5.5,
            color=C_OUT, **FONT, zorder=10)
    ax.text(sx(sch_x + sch_w / 2), sy(sch_y + 3 * sch_h / 4 + 3),
            "TOP\nTIER", ha="center", va="center", fontsize=5.5,
            color=C_OUT, **FONT, zorder=10)

    # Platform line
    ax.plot([sx(sch_x - 10), sx(sch_x + sch_w + 10)],
            [sy(sch_y + sch_h / 2 + 2), sy(sch_y + sch_h / 2 + 2)],
            color=C_FRAME, lw=2.0, zorder=6)
    ax.text(sx(sch_x + sch_w + 15), sy(sch_y + sch_h / 2 + 2),
            "PLATFORM", ha="left", va="center", fontsize=5,
            color=C_FRAME, **FONT, zorder=10)

    # D-ring positions
    dring_color = "#D0A030"
    dring_positions_sch = [
        (sch_x - 8, sch_y + 25, "1"),
        (sch_x + sch_w + 8, sch_y + 25, "2"),
        (sch_x - 8, sch_y + sch_h / 2 + 25, "3"),
        (sch_x + sch_w + 8, sch_y + sch_h / 2 + 25, "4"),
    ]
    for dx, dy, dlabel in dring_positions_sch:
        ax.add_patch(Circle((sx(dx), sy(dy)), sx(6),
                             fc=dring_color, ec=C_OUT, lw=1.0, zorder=11))
        ax.text(sx(dx), sy(dy), dlabel, ha="center", va="center",
                fontsize=5, color=C_OUT, fontweight="bold", **FONT, zorder=12)

    # Ratchet strap lines (over top of IBC, D-ring to D-ring)
    strap_color = "#2060A0"
    # Bottom tier strap: 1->2 over the bottom IBC
    strap_y_bot = sch_y + sch_h / 2 - 5
    ax.plot([sx(sch_x - 8), sx(sch_x + sch_w / 2)],
            [sy(sch_y + 25), sy(strap_y_bot)],
            color=strap_color, lw=2.0, ls="-", zorder=8)
    ax.plot([sx(sch_x + sch_w / 2), sx(sch_x + sch_w + 8)],
            [sy(strap_y_bot), sy(sch_y + 25)],
            color=strap_color, lw=2.0, ls="-", zorder=8)

    # Top tier strap: 3->4 over the top IBC
    strap_y_top = sch_y + sch_h - 5
    ax.plot([sx(sch_x - 8), sx(sch_x + sch_w / 2)],
            [sy(sch_y + sch_h / 2 + 25), sy(strap_y_top)],
            color=strap_color, lw=2.0, ls="-", zorder=8)
    ax.plot([sx(sch_x + sch_w / 2), sx(sch_x + sch_w + 8)],
            [sy(strap_y_top), sy(sch_y + sch_h / 2 + 25)],
            color=strap_color, lw=2.0, ls="-", zorder=8)

    # Strap labels
    ax.text(sx(sch_x + sch_w / 2), sy(strap_y_bot + 8),
            "RATCHET STRAP\n(BOTTOM TIER)", ha="center", va="bottom",
            fontsize=5, color=strap_color, fontweight="bold", **FONT, zorder=15)
    ax.text(sx(sch_x + sch_w / 2), sy(strap_y_top + 8),
            "RATCHET STRAP\n(TOP TIER)", ha="center", va="bottom",
            fontsize=5, color=strap_color, fontweight="bold", **FONT, zorder=15)

    # Notes for Detail D
    dn_x = sx(DD_OX + 10)
    dn_top = sy(DD_OY + 12)
    d_notes = [
        "NOTES:",
        "1. 25mm ratchet straps, 1,100kg WLL",
        "2. D-ring to D-ring over IBC top",
        "3. 1 strap per tier per side (4 total)",
        "4. Tighten before transport",
        "5. Check strap tension after 50km",
    ]

    draw_notes(ax, d_notes, dn_x, dn_top, spacing=22,
               fs=7, font=FONT, width=425)

    # Detail D border
    ax.add_patch(Rectangle((sx(DD_OX - 5), sy(DD_OY)),
                            sx(200), sy(230),
                            fc="none", ec=C_DIM, lw=0.8, ls="--", zorder=1))

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 5",
                drawing_title="IBC STACKING & SECURING",
                subtitle="FASTENING DETAILS — D-RING - LIP - ACCESS GATE - LASHING",
                scale_note="Axes in mm - DETAILS A-D",
                height=0.06)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "ibc-stacking-sheet2.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-stacking-sheet2.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — External Plumbing Panel Elevation
#
# View from outside the container, looking at the sealed end wall.
# Shows 3 ports stacked vertically on the container centerline:
#   Top:    Fill Blue IBC-1 (2250mm)
#           Drain Brown IBC-3 (400mm)
#   Bottom: Drain Waste IBC-4 (200mm)
# Reinforcing plate behind ports, camlock fittings, height dimensions.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet3():
    def sx(mm): return mm
    def sy(mm): return mm

    # View bounds — looking -X at the sealed-end exterior face from outside.
    # Components are drawn coordinate-mirrored (yd_ext = C_WID - yd); combined
    # with ax.invert_xaxis() this renders the physically-correct exterior view:
    # near/pinhole wall at LEFT, far wall at RIGHT.  Vertical = Z
    YD_LO = -300
    YD_HI = C_WID + 300
    Z_LO  = -500
    Z_HI  = C_HGT + 200

    fig, ax = plt.subplots(figsize=(18, 22))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(sx(YD_LO), sx(YD_HI))
    ax.invert_xaxis()   # match physical view orientation (see sheet header)
    ax.set_ylim(sy(Z_LO), sy(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container end wall ───────────────────────────────────────────────────
    WALL_T = 40  # visual wall thickness
    # End wall face
    ax.add_patch(Rectangle((sx(0), sy(0)),
                            sx(C_WID), sy(C_HGT),
                            fc="#E8E8E8", ec=C_OUT, lw=2.5, zorder=2))

    # Corrugation lines (vertical ribs on container wall)
    rib_spacing = 190  # typical 20ft container rib spacing
    for rib_yd in range(rib_spacing, C_WID, rib_spacing):
        ax.plot([sx(rib_yd), sx(rib_yd)], [sy(0), sy(C_HGT)],
                color=C_WALL, lw=0.5, alpha=0.4, zorder=3)

    # Ground line
    ax.plot([sx(YD_LO), sx(YD_HI)], [sy(0), sy(0)],
            color=C_OUT, lw=1.5, zorder=4)
    ax.text(sx(C_WID / 2), sy(-20), "GROUND / CONTAINER FLOOR",
            ha="center", va="top", fontsize=6, color=C_DIM, **FONT)

    # Wall labels
    ax.text(sx(-20), sy(C_HGT / 2), "FAR\nWALL",
            ha="right", va="center", fontsize=6, color=C_DIM,
            fontweight="bold", **FONT, rotation=0)
    ax.text(sx(C_WID + 20), sy(C_HGT / 2), "NEAR\nWALL\n(PINHOLE)",
            ha="left", va="center", fontsize=6, color=C_DIM,
            fontweight="bold", **FONT, rotation=0)
    ax.text(sx(C_WID / 2), sy(C_HGT + 30),
            "SEALED END WALL — EXTERIOR VIEW",
            ha="center", va="bottom", fontsize=9, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── Centerline ───────────────────────────────────────────────────────────
    cl_yd = C_WID / 2  # = 1181mm
    ax.plot([sx(cl_yd), sx(cl_yd)], [sy(-80), sy(C_HGT + 80)],
            color=C_CL, lw=1.0, ls="--", zorder=4)
    ax.text(sx(cl_yd), sy(C_HGT + 90), f"CENTERLINE\nYd={cl_yd:.0f}mm",
            ha="center", va="bottom", fontsize=6, color=C_CL,
            fontweight="bold", **FONT, zorder=15)

    # ── Ghost IBC outlines and stacking frame (behind wall) ────────────────
    # yd_ext = C_WID - yd_internal; with invert_xaxis (above) this lands the
    # near/pinhole wall at LEFT, far wall at RIGHT (correct exterior orientation)
    platform_z = IBC_H_600                        # 1010mm
    top_tier_z = platform_z + FRAME_RHS + MAT_T   # 1072mm

    # Near column (internal Yd 30–1046) → external Yd 1316–2332
    near_ext_l = C_WID - (BLUE_IBC_Y + IBC_D)     # 1316
    # Far column (internal Yd 1316–2332) → external Yd 30–1046
    far_ext_l  = C_WID - (IBC_FAR_Y + IBC_D)      # 30

    ghost_ibcs = [
        ("IBC-3\nBROWN",  near_ext_l, 0,          C_BROWN_IBC),
        ("IBC-1\nBLUE",   near_ext_l, top_tier_z, C_BLUE_IBC),
        ("IBC-4\nWASTE",  far_ext_l,  0,          C_WASTE_IBC),
        ("IBC-2\nBLUE",   far_ext_l,  top_tier_z, C_BLUE_IBC),
    ]
    for label, yd_l, z_base, color in ghost_ibcs:
        # Light fill
        ax.add_patch(Rectangle((sx(yd_l), sy(z_base)),
                                sx(IBC_D), sy(IBC_H_600),
                                fc=color, ec="none", lw=0,
                                alpha=0.12, zorder=2.5))
        # Dashed cage outline
        ax.add_patch(Rectangle((sx(yd_l), sy(z_base)),
                                sx(IBC_D), sy(IBC_H_600),
                                fc="none", ec=color, lw=1.8, ls=(0, (6, 3)),
                                alpha=0.5, zorder=2.6))
        # Cage uprights (ghost)
        for post_yd in [yd_l + 15, yd_l + IBC_D - 15]:
            ax.add_patch(Rectangle((sx(post_yd - CAGE_POST_W / 2), sy(z_base)),
                                    sx(CAGE_POST_W), sy(IBC_H_600),
                                    fc="none", ec=color, lw=0.5, ls=(0, (4, 3)),
                                    alpha=0.3, zorder=2.6))
        ax.text(sx(yd_l + IBC_D / 2), sy(z_base + IBC_H_600 / 2), label,
                ha="center", va="center", fontsize=6, color=color,
                alpha=0.55, fontweight="bold", **FONT, zorder=2.7)

    # Stacking frame — platform beams (ghost)
    for pl, pr in [(near_ext_l - FRAME_RHS, near_ext_l + IBC_D + 5),
                    (far_ext_l - 5,          far_ext_l + IBC_D + FRAME_RHS)]:
        ax.add_patch(Rectangle((sx(pl), sy(platform_z)),
                                sx(pr - pl), sy(FRAME_RHS),
                                fc=C_FRAME, ec=C_FRAME, lw=1.5, ls=(0, (6, 3)),
                                alpha=0.2, zorder=2.5))

    # Corridor uprights (ghost) — internal Yd 1046–1096 and 1266–1316
    # External: 1266–1316 and 1046–1096
    for uyd in [C_WID - (BLUE_IBC_Y + IBC_D + FRAME_RHS),
                C_WID - IBC_FAR_Y]:
        ax.add_patch(Rectangle((sx(uyd), sy(0)),
                                sx(FRAME_RHS), sy(IBC_H_STK + FRAME_RHS),
                                fc=C_FRAME, ec=C_FRAME, lw=1.2, ls=(0, (6, 3)),
                                alpha=0.18, zorder=2.5))

    # Ghost label
    ax.text(sx(C_WID / 2), sy(IBC_H_STK + FRAME_RHS + 30),
            "GHOST OUTLINE — IBCs & STACKING FRAME (BEHIND WALL)",
            ha="center", va="bottom", fontsize=5.5, color=C_FRAME,
            fontstyle="italic", **FONT, zorder=2.8)

    # ── Reinforcing plate ────────────────────────────────────────────────────
    plate_w = 300   # plate width (mm)
    plate_h = EXT_FILL_1_H - 100 + 100  # spans from below lowest port to above highest
    plate_yd = cl_yd - plate_w / 2
    plate_z = 100   # bottom edge
    ax.add_patch(Rectangle((sx(plate_yd), sy(plate_z)),
                            sx(plate_w), sy(plate_h),
                            fc=C_STEEL, ec=C_OUT, lw=1.5, alpha=0.3,
                            hatch="...", zorder=5))
    leader(ax, sx(plate_yd), sy(plate_z + plate_h / 2),
           sx(plate_yd - 180), sy(plate_z + plate_h / 2 + 100),
           f"REINFORCING PLATE\n6mm MILD STEEL\n{plate_w}x{plate_h}mm\nWELDED TO WALL",
           color=C_STEEL, fs=6,
           ha="right", va="bottom", arrow_style="-|>", font=FONT)

    # ── Port definitions ─────────────────────────────────────────────────────
    port_r = PORT_DIA / 2
    camlock_r = 38  # camlock fitting outer radius (visual)

    ports = [
        ("FILL — BLUE IBC-1\n(CLEAN SUPPLY, TOP NEAR)",
         EXT_FILL_1_H, C_BLUE_IBC, "X1"),
        ("DRAIN — BROWN IBC-3\n(RECYCLED, BOTTOM NEAR)",
         EXT_DRAIN_3_H, C_BROWN_IBC, "X3"),
        ("DRAIN — WASTE IBC-4\n(WASTE, BOTTOM FAR)",
         EXT_DRAIN_4_H, C_WASTE_IBC, "X4"),
    ]

    for label, port_z, color, tag in ports:
        # Camlock fitting (outer ring)
        ax.add_patch(Circle((sx(cl_yd), sy(port_z)),
                             sx(camlock_r), fc="none", ec=C_OUT,
                             lw=2.0, zorder=8))
        # Port opening
        ax.add_patch(Circle((sx(cl_yd), sy(port_z)),
                             sx(port_r), fc=color, ec=C_OUT,
                             lw=1.5, alpha=0.5, zorder=9))
        # Port tag
        ax.text(sx(cl_yd), sy(port_z), tag,
                ha="center", va="center", fontsize=7, color=C_OUT,
                fontweight="bold", **FONT, zorder=12)

        # Leader to the right
        leader_x = cl_yd + plate_w / 2 + 40
        leader(ax, sx(cl_yd + camlock_r + 5), sy(port_z),
               sx(leader_x), sy(port_z),
               f"{label}\n2\" CAMLOCK\nZ={port_z}mm",
               color=color, fs=6,
               ha="left", va="center", arrow_style="-|>", font=FONT)

    # ── Dimensions ───────────────────────────────────────────────────────────
    dim_yd = cl_yd - plate_w / 2 - 80

    # Individual port heights from ground
    for port_z, label in [(EXT_FILL_1_H, f"{EXT_FILL_1_H}mm"),
                           (EXT_DRAIN_3_H, f"{EXT_DRAIN_3_H}mm"),
                           (EXT_DRAIN_4_H, f"{EXT_DRAIN_4_H}mm")]:
        draw_dim_v(ax, sx(dim_yd), sy(0), sy(port_z),
                   label, offset=sx(5), fs=5.5, font=FONT)
        dim_yd -= 60  # stagger dimension lines

    # Container height
    draw_dim_v(ax, sx(C_WID + 80), sy(0), sy(C_HGT),
               f"{C_HGT}mm\nCONTAINER HEIGHT", offset=sx(5), fs=6,
               right=True, font=FONT)

    # Container width
    draw_dim_h(ax, sx(0), sx(C_WID), sy(-100),
               f"{C_WID}mm  CONTAINER WIDTH", offset=sy(5), fs=6.5, font=FONT)

    # Plate width
    draw_dim_h(ax, sx(plate_yd), sx(plate_yd + plate_w), sy(plate_z - 30),
               f"{plate_w}mm PLATE", offset=sy(5), fs=5.5, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        "EXTERNAL PLUMBING PANEL NOTES:",
        "1. 3x 2\" NPT bulkhead unions through sealed end wall on container centerline.",
        "2. 6mm mild steel reinforcing plate welded to wall interior before penetrations.",
        "3. Type DC camlock fittings (2\" aluminum) on exterior face — quick-connect for fill hose (X1) and drain hose (X3/X4).",
        "4. X1 fill port at top tees to BOTH Blue totes (IBC-1 & IBC-2, parallel). Drain ports at bottom (gravity drain).",
        "5. All penetrations sealed with neoprene gaskets — light-tight and watertight.",
        "6. Interior connections routed through plumbing corridor (see Sheet 4).",
    ]
    draw_notes(ax, notes, sx(YD_LO + 30), sy(Z_LO + 350), spacing=sy(18),
               fs=7, font=FONT, width=5000)

    # ── Title block ──────────────────────────────────────────────────────────
    title_block(ax, "SHEET 3 OF 5",
                drawing_title="IBC STACKING & SECURING",
                subtitle="EXTERNAL PLUMBING PANEL — END WALL ELEVATION",
                scale_note="Axes in mm - VIEW FROM OUTSIDE",
                height=0.06)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "ibc-stacking-sheet3.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-stacking-sheet3.png saved")


# ── Shared pipe drawing helpers ───────────────────────────────────────────────

def draw_pipe_path(ax, y_pts, z_pts, od_mm, wall_mm, sy, sz,
                   fc="#B0B0B8", ec="#333333", bore_fc="white",
                   elbow_r=None, zorder=5):
    """Thin wrapper → tbs_drawing.draw_pipe_path (canonical body)."""
    _tbs_pipe_path(ax, y_pts, z_pts, od_mm, wall_mm, fc, ec=ec,
                   bore_fc=bore_fc, elbow_r=elbow_r, zorder=zorder,
                   sx=sy, sz=sz)


def draw_pipe_end(ax, cy, cz, r_data, wall_data, fc="#B0B0B8", ec="#333333",
                  bore_fc="white", zorder=5):
    """Thin wrapper → tbs_drawing.draw_pipe_end."""
    _tbs_pipe_end(ax, cy, cz, r_data, wall_data, fc=fc, ec=ec,
                  bore_fc=bore_fc, zorder=zorder)


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 4 — Internal Plumbing Plan View + IBC Layout
#
# Looking down at the IBC zone from above, showing:
#   - Two IBC columns (near/far) with central plumbing corridor
#   - Portal frame structure, D-ring lashing points
#   - Pipe runs from end-wall bulkhead unions through corridor to each IBC
#   - Ball valves at each IBC connection
#   - Equipment panel with pumps and filters
#   - Pipe sizing and material annotations
# ═══════════════════════════════════════════════════════════════════════════════
def sheet4():
    def px(mm): return mm
    def py(mm): return mm

    # Plan view of IBC zone + corridor
    X_LO = IBC_COL_X - 500
    X_HI = C_LEN + 1350   # extra right margin holds the legend in free space
    WALL_R = C_LEN + 250  # wall-hatch right edge — do NOT extend it with X_HI
    YD_LO = -350
    YD_HI = C_WID + 200

    fig, ax = plt.subplots(figsize=(20, 18))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(px(X_LO), px(X_HI))
    ax.set_ylim(py(YD_LO), py(YD_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container walls (partial) ────────────────────────────────────────────
    WALL_T = 25
    # Near wall
    ax.add_patch(Rectangle((px(X_LO), py(-WALL_T)),
                            px(WALL_R - X_LO), py(WALL_T),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Far wall
    ax.add_patch(Rectangle((px(X_LO), py(C_WID)),
                            px(WALL_R - X_LO), py(WALL_T),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # End wall
    ax.add_patch(Rectangle((px(C_LEN), py(-WALL_T)),
                            px(WALL_T), py(C_WID + 2 * WALL_T),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))

    # Interior face lines
    ax.plot([px(X_LO), px(C_LEN)], [py(0), py(0)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([px(X_LO), px(C_LEN)], [py(C_WID), py(C_WID)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([px(C_LEN), px(C_LEN)], [py(0), py(C_WID)], color=C_OUT, lw=2.0, zorder=3)

    # Wall labels
    ax.text(px((X_LO + C_LEN) / 2), py(-WALL_T - 10),
            "NEAR WALL (PINHOLE, Yd=0)", ha="center", va="top",
            fontsize=6, color=C_DIM, **FONT)
    ax.text(px((X_LO + C_LEN) / 2), py(C_WID + WALL_T + 10),
            "FAR WALL (Yd=2362)", ha="center", va="bottom",
            fontsize=6, color=C_DIM, **FONT)
    ax.text(px(C_LEN + WALL_T + 10), py(C_WID / 2),
            f"SEALED END WALL (X={C_LEN}mm)", ha="left", va="center",
            fontsize=6.5, color=C_DIM, fontweight="bold", **FONT, rotation=90)

    # ── IBCs (plan view — top tier solid, bottom tier dashed) ──────────────
    near_col_r = BLUE_IBC_Y + IBC_D
    far_col_l  = IBC_FAR_Y

    ibc_plan = [
        ("IBC-3 BROWN\n(bottom, near)\nBELOW IBC-1", BLUE_IBC_Y, C_BROWN_IBC, False),
        ("IBC-4 WASTE\n(bottom, far)\nBELOW IBC-2", IBC_FAR_Y, C_WASTE_IBC, False),
        ("IBC-1\nBLUE\n(top, near)", BLUE_IBC_Y, C_BLUE_IBC, True),
        ("IBC-2\nBLUE\n(top, far)", IBC_FAR_Y, C_BLUE_IBC, True),
    ]
    for label, yd, color, is_top in ibc_plan:
        if is_top:
            ax.add_patch(Rectangle((px(IBC_COL_X), py(yd)),
                                    px(IBC_W), py(IBC_D),
                                    fc=color, ec=C_OUT, lw=1.5, alpha=0.35, zorder=5))
            for frac in [0.25, 0.5, 0.75]:
                ax.plot([px(IBC_COL_X + IBC_W * frac), px(IBC_COL_X + IBC_W * frac)],
                        [py(yd), py(yd + IBC_D)],
                        color=C_OUT, lw=0.3, alpha=0.25, zorder=5)
                ax.plot([px(IBC_COL_X), px(IBC_COL_X + IBC_W)],
                        [py(yd + IBC_D * frac), py(yd + IBC_D * frac)],
                        color=C_OUT, lw=0.3, alpha=0.25, zorder=5)
            ax.text(px(IBC_COL_X + IBC_W / 2), py(yd + IBC_D / 2), label,
                    ha="center", va="center", fontsize=7, color=C_OUT,
                    fontweight="bold", **FONT, zorder=10)
        else:
            ax.add_patch(Rectangle((px(IBC_COL_X), py(yd)),
                                    px(IBC_W), py(IBC_D),
                                    fc="none", ec=color, lw=1.0, ls="--",
                                    alpha=0.4, zorder=4))
            ax.text(px(IBC_COL_X + IBC_W / 2), py(yd - 25), label.split("\n")[0],
                    ha="center", va="top", fontsize=5, color=color,
                    style="italic", **FONT, zorder=10)

    # ── Portal frame (corridor uprights, column beams, wall brackets) ────────
    frame_x_l = IBC_COL_X - 65
    frame_x_r = min(IBC_COL_X + IBC_W + 65, C_LEN)
    for uyd in [near_col_r, far_col_l - FRAME_RHS]:
        for ux in [frame_x_l, frame_x_r - FRAME_RHS]:
            ax.add_patch(Rectangle((px(ux), py(uyd)),
                                    px(FRAME_RHS), py(FRAME_RHS),
                                    fc=C_FRAME, ec=C_OUT, lw=0.8, zorder=6, alpha=0.6))
    for col_yd_l, col_yd_r in [(BLUE_IBC_Y - 5, near_col_r + FRAME_RHS),
                                (far_col_l - FRAME_RHS, IBC_FAR_Y + IBC_D + 5)]:
        for bx in [frame_x_l, frame_x_r - FRAME_RHS]:
            ax.add_patch(Rectangle((px(bx), py(col_yd_l)),
                                    px(FRAME_RHS), py(col_yd_r - col_yd_l),
                                    fc=C_FRAME, ec=C_OUT, lw=0.6, zorder=6, alpha=0.4))
    corr_beam_l = near_col_r + FRAME_RHS
    corr_beam_r = far_col_l - FRAME_RHS
    for bx in [frame_x_l, frame_x_r - FRAME_RHS]:
        ax.add_patch(Rectangle((px(bx), py(corr_beam_l)),
                                px(FRAME_RHS), py(corr_beam_r - corr_beam_l),
                                fc=C_FRAME, ec=C_OUT, lw=0.5, zorder=6, alpha=0.3))
    for wyd in [0, C_WID - 8]:
        for bx in [frame_x_l, frame_x_r - FRAME_RHS]:
            ax.add_patch(Rectangle((px(bx), py(wyd)),
                                    px(FRAME_RHS), py(8),
                                    fc=C_FRAME, ec=C_OUT, lw=0.5, zorder=6, alpha=0.4))

    # ── Panel support frame (mid-bay): rectangle the wet-end panel bolts to ──
    ax.add_patch(Rectangle((px(PANEL_FRAME_X), py(near_col_r)),
                            px(IBC_FRAME_RHS), py(far_col_l - near_col_r),
                            fc=C_FRAME, ec=C_OUT, lw=1.0, alpha=0.55, zorder=7))
    ax.text(px(PANEL_FRAME_X + IBC_FRAME_RHS + 150), py(near_col_r - 22),
            "PANEL SUPPORT FRAME\n(uprights to Z=2310\n+ top rail + floor beam)",
            ha="left", va="top", fontsize=5, color=C_FRAME,
            fontweight="bold", **FONT, zorder=10)

    # ── D-ring lashing points ────────────────────────────────────────────────
    dring_color = "#D0A030"
    for dyd in [near_col_r + FRAME_RHS / 2, far_col_l - FRAME_RHS / 2]:
        for dx in [frame_x_l + FRAME_RHS / 2, frame_x_r - FRAME_RHS / 2]:
            ax.add_patch(Circle((px(dx), py(dyd)),
                                 px(10), fc=dring_color, ec=C_OUT,
                                 lw=0.8, zorder=11))
    ax.text(px(frame_x_l - 10), py(near_col_r + FRAME_RHS / 2 - 25),
            "D-RING (TYP. 8x)", ha="right", va="top",
            fontsize=5, color=dring_color, fontweight="bold", **FONT, zorder=15)

    # ── Plumbing corridor shading ────────────────────────────────────────────
    corr_yd_lo = near_col_r
    corr_yd_hi = far_col_l
    corr_cx = (corr_yd_lo + corr_yd_hi) / 2
    ax.add_patch(Rectangle((px(IBC_COL_X - 65), py(corr_yd_lo)),
                            px(IBC_W + 130), py(corr_yd_hi - corr_yd_lo),
                            fc=C_CL, ec="none", alpha=0.08, zorder=4))
    ax.text(px(IBC_COL_X + IBC_W * 0.1), py(corr_cx),
            f"PLUMBING CORRIDOR\n{CORRIDOR_W}mm",
            ha="center", va="center", fontsize=7, color=C_CL,
            fontweight="bold", **FONT, zorder=10)

    # Corridor centerline
    ax.plot([px(IBC_COL_X - 65), px(C_LEN)],
            [py(corr_cx), py(corr_cx)],
            color=C_CL, lw=1.0, ls="--", zorder=4)

    # ── Walkway context (ghost outline) ──────────────────────────────────────
    wk_x_l = WALKWAY_RIGHT_X
    ax.add_patch(Rectangle((px(wk_x_l), py(0)),
                            px(WALKWAY_W), py(C_WID),
                            fc="#E8F0E8", ec=C_GRATE, lw=0.8, ls="--",
                            alpha=0.2, zorder=3))
    ax.text(px(wk_x_l + WALKWAY_W / 2), py(C_WID / 2),
            f"RIGHT WALKWAY\n(X={wk_x_l}–{wk_x_l + WALKWAY_W}mm)",
            ha="center", va="center", fontsize=5, color=C_GRATE,
            style="italic", **FONT, zorder=5, rotation=90)

    # Cargo door direction arrow
    ax.annotate("", xy=(px(X_LO + 20), py(C_WID / 2)),
                xytext=(px(X_LO + 120), py(C_WID / 2)),
                arrowprops=dict(arrowstyle="->", color=C_DIM, lw=1.2))
    ax.text(px(X_LO + 10), py(C_WID / 2),
            "CARGO\nDOOR\nEND", ha="right", va="center",
            fontsize=5, color=C_DIM, **FONT)

    # ── Equipment panel (backing board + equipment depth) ────────────────
    # Panel spans ACROSS corridor (Yd direction), perpendicular to sealed end wall.
    # Panel face at X=EQPANEL_X (5240), ply extends toward sealed end.
    # Equipment protrudes toward open end (lower X).
    ep_face_x = EQPANEL_X                      # 5240 — equipment face
    ep_back_x = ep_face_x + EQPANEL_T          # 5018 — plywood back face
    ep_yd_near = EQPANEL_YD                    # 1046
    ep_yd_far  = EQPANEL_YD + CORRIDOR_W       # 1316
    ep_depth_x = ep_face_x - BB_OD             # 4870 — deepest protrusion (filters)

    # Full panel assembly footprint (backing board + equipment depth)
    ax.add_patch(Rectangle((px(ep_depth_x), py(ep_yd_near)),
                            px(ep_back_x - ep_depth_x), py(CORRIDOR_W),
                            fc=C_PLY, ec="#A09060", lw=1.5, alpha=0.3, zorder=5))

    # Plywood backing board (thin strip at back)
    ax.add_patch(Rectangle((px(ep_face_x), py(ep_yd_near)),
                            px(EQPANEL_T), py(CORRIDOR_W),
                            fc=C_PLY, ec="#A09060", lw=1.5, zorder=6))

    # Leader with panel contents
    leader(ax, px(ep_face_x - BB_OD / 2), py(ep_yd_near),
           px(ep_face_x - 260), py(ep_yd_near - 220),
           "EQUIPMENT PANEL\n"
           "Backing Board (18mm marine ply)\n"
           "P-01/P-02/P-03/P-04 pumps (Shurflo 2088)\n"
           "ACC-01 accumulator (125 PSI)\n"
           "F1 (50μ) / F2 (5μ) / F3 (GAC) filters\n"
           "3× Big Blue 4.5\"×10\" housings, stacked",
           fs=5.5, color="#A09060", ha="left", font=FONT)

    # ── Pipe fitting helpers (matching sheet 5 conventions) ────────────────
    PIPE_OD = 33.4    # 1" HDPE SDR-11 outer diameter (mm)
    PIPE_WALL_T = 3.0
    PIPE_HW = PIPE_OD / 2

    def flange_plan(ax, x, yd, orientation, color, zo=8):
        """Pipe flange at a connection in plan view."""
        fw = 8
        fh = PIPE_OD + 20
        if orientation == 'h':  # on horizontal pipe
            ax.add_patch(Rectangle((px(x - fw / 2), py(yd - fh / 2)),
                                    px(fw), py(fh),
                                    fc=color, ec=C_OUT, lw=1.5,
                                    alpha=0.4, zorder=zo))
        else:  # on vertical pipe
            ax.add_patch(Rectangle((px(x - fh / 2), py(yd - fw / 2)),
                                    px(fh), py(fw),
                                    fc=color, ec=C_OUT, lw=1.5,
                                    alpha=0.4, zorder=zo))

    def valve_plan(ax, x, yd, orientation, color, label, zo=11):
        """Ball valve bowtie in white circle, plan view. orientation: 'h' or 'v'."""
        vs = 18
        cr = vs * 1.6  # circle radius in mm
        # White circle background
        circ = plt.Circle((px(x), py(yd)),
                           abs(px(cr) - px(0)),  # radius in data coords
                           fc="white", ec=color, lw=1.5, zorder=zo)
        ax.add_patch(circ)
        if orientation == 'v':  # on a vertical (Yd-direction) pipe
            tri1 = Polygon([(px(x - vs), py(yd - vs)),
                             (px(x + vs), py(yd - vs)),
                             (px(x), py(yd))], closed=True,
                            fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=zo + 1)
            tri2 = Polygon([(px(x - vs), py(yd + vs)),
                             (px(x + vs), py(yd + vs)),
                             (px(x), py(yd))], closed=True,
                            fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=zo + 1)
        else:  # on a horizontal (X-direction) pipe
            tri1 = Polygon([(px(x - vs), py(yd - vs)),
                             (px(x - vs), py(yd + vs)),
                             (px(x), py(yd))], closed=True,
                            fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=zo + 1)
            tri2 = Polygon([(px(x + vs), py(yd - vs)),
                             (px(x + vs), py(yd + vs)),
                             (px(x), py(yd))], closed=True,
                            fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=zo + 1)
        ax.add_patch(tri1)
        ax.add_patch(tri2)
        if label:
            ax.text(px(x), py(yd), label,
                    ha="center", va="center", fontsize=5, color="white",
                    fontweight="bold", **FONT, zorder=zo + 2)

    # ── Pipe system colors (matching sheet 5) ────────────────────────────────
    C_PIPE_BLUE   = "#2060C0"
    C_PIPE_BROWN  = "#8D6E63"
    C_PIPE_BLACK  = "#505050"

    # ── Bulkhead ports at end wall ──────────────────────────────────────────
    # All 4 ports are at the same Yd (panel_yd = corridor centerline),
    # stacked vertically at different Z heights (matching sheet 3).
    # Looking down they project to the same point.
    panel_yd = C_WID / 2
    bh_x = C_LEN  # at end wall

    # Draw stacked port symbol — outermost ring is largest (X1, top),
    # inner rings for lower ports
    port_r = 22
    draw_pipe_end(ax, px(bh_x), py(panel_yd),
                  px(port_r), px(3),
                  fc=C_PIPE_BLUE, ec=C_OUT, zorder=12)
    # Color rings for the 4 circuits (concentric, largest = topmost)
    for r_frac, color in [(0.65, C_PIPE_BLUE), (0.45, C_PIPE_BROWN),
                           (0.25, C_PIPE_BLACK)]:
        ax.add_patch(Circle((px(bh_x), py(panel_yd)),
                     px(port_r * r_frac), fc=color, ec="none",
                     zorder=13, alpha=0.8))
    ax.text(px(bh_x + 40), py(panel_yd + 220),
            "3x BULKHEAD UNIONS\n2\" NPT, STACKED\nAT Yd=" + f"{int(panel_yd)}mm\n"
            "X1: Z={0}\nX3: Z={1}\nX4: Z={2}".format(
                EXT_FILL_1_H, EXT_DRAIN_3_H, EXT_DRAIN_4_H),
            ha="left", va="center", fontsize=5, color=C_PORT,
            fontweight="bold", **FONT, zorder=15)

    # ── Pipe routing ─────────────────────────────────────────────────────────
    # All pipes share the corridor centerline (panel_yd) from the bulkhead.
    # They separate at their branch points — fill pipes at fill_x,
    # drain pipes at drain_x.
    near_ibc_conn_yd = near_col_r   # 1046
    far_ibc_conn_yd  = far_col_l    # 1316

    # Connection X positions — BEHIND the panel support frame (sealed-wall side),
    # matching the 3D so the pipes clear the frame uprights (X=5258-5308).
    fill_tee_x  = PANEL_FRAME_X + 150          # 5408 — fill tee behind the top rail
    drain_x     = PANEL_FRAME_X + 142          # 5400 — drains behind the frame
    near_tote_c = BLUE_IBC_Y + IBC_D / 2       # 538  — tote center (fill drop)
    far_tote_c  = IBC_FAR_Y + IBC_D / 2        # 1824 — tote center (fill drop)

    # ── X4: IBC-4 (far, Waste) → bulkhead (lowest, drawn first) ───────────
    # X4 (Z=200) is the lowest pipe. Drawn first so X3 covers it in corridor.
    draw_pipe_path(ax,
                   [drain_x, drain_x, bh_x],
                   [far_ibc_conn_yd, panel_yd, panel_yd],
                   PIPE_OD, PIPE_WALL_T, px, py,
                   fc=C_PIPE_BLACK, ec="#333333", zorder=5)
    flange_plan(ax, drain_x, far_ibc_conn_yd, 'v', C_PIPE_BLACK)
    v4_yd = (far_ibc_conn_yd + panel_yd) / 2
    valve_plan(ax, drain_x, v4_yd, 'v', C_PIPE_BLACK, "V4")
    leader(ax, px(drain_x), py(far_ibc_conn_yd),
           px(drain_x - 180), py(far_ibc_conn_yd + 80),
           "X4 ← IBC-4\n(DRAIN, WASTE)\n1\" HDPE",
           fs=5.5, color=C_PIPE_BLACK, ha="right", font=FONT)
    # ── X3: IBC-3 (near, Brown) → bulkhead (above X4) ──────────────────────
    # X3 (Z=400) sits above X4 (Z=200). Covers X4 in the corridor run.
    draw_pipe_path(ax,
                   [drain_x, drain_x, bh_x],
                   [near_ibc_conn_yd, panel_yd, panel_yd],
                   PIPE_OD, PIPE_WALL_T, px, py,
                   fc=C_PIPE_BROWN, ec="#5A3020", zorder=6)
    flange_plan(ax, drain_x, near_ibc_conn_yd, 'v', C_PIPE_BROWN)
    v3_yd = (near_ibc_conn_yd + panel_yd) / 2
    valve_plan(ax, drain_x, v3_yd, 'v', C_PIPE_BROWN, "V3")
    leader(ax, px(drain_x), py(near_ibc_conn_yd),
           px(drain_x - 20), py(near_ibc_conn_yd - 80),
           "X3 ← IBC-3\n(DRAIN, BROWN)\n1\" HDPE",
           fs=5.5, color=C_PIPE_BROWN, ha="right", font=FONT)
    # ── X1: Bulkhead → fill tee (behind top rail) → BOTH Blue totes ───────
    # Matches the 3D: a tee splits the fill to IBC-1 and IBC-2 (no cross-connect);
    # each branch drops straight into its tote.
    draw_pipe_path(ax,
                   [bh_x, fill_tee_x],
                   [panel_yd, panel_yd],
                   PIPE_OD, PIPE_WALL_T, px, py,
                   fc=C_PIPE_BLUE, ec="#1A4A90", zorder=9)
    draw_pipe_path(ax,
                   [fill_tee_x, fill_tee_x],
                   [near_tote_c, far_tote_c],
                   PIPE_OD, PIPE_WALL_T, px, py,
                   fc=C_PIPE_BLUE, ec="#1A4A90", zorder=9)
    valve_plan(ax, fill_tee_x, (panel_yd + near_tote_c) / 2, 'v', C_PIPE_BLUE, "V1")
    flange_plan(ax, fill_tee_x, near_tote_c, 'v', C_PIPE_BLUE)
    flange_plan(ax, fill_tee_x, far_tote_c, 'v', C_PIPE_BLUE)
    leader(ax, px(fill_tee_x), py(far_tote_c),
           px(fill_tee_x + 150), py(far_tote_c + 90),
           "X1 → IBC-1 & IBC-2\n(FILL TEE, BLUE)\n1\" HDPE",
           fs=5.5, color=C_PIPE_BLUE, ha="left", font=FONT)

    # ── Legend ───────────────────────────────────────────────────────────────
    leg_x = px(C_LEN + 380)        # right of the container, in the free margin
    leg_top = py(C_WID - 100)
    leg_sp = py(33)
    pipe_lw = 2.5

    # Legend background box
    n_leg_items = 7  # 3 pipes + elbow + valve + panel + filter
    leg_box_x = leg_x - px(10)
    leg_box_top = leg_top + leg_sp * 0.5
    leg_box_bot = leg_top - n_leg_items * leg_sp + leg_sp * 0.3
    leg_box_w = px(800)
    ax.add_patch(Rectangle((leg_box_x, leg_box_bot), leg_box_w,
                            leg_box_top - leg_box_bot,
                            fc="#F0F0F0", ec=C_OUT, lw=0.6, zorder=14))

    legend_items = [
        (C_PIPE_BLUE,  "BLUE CIRCUIT — Fill (1\" HDPE SDR-11)"),
        (C_PIPE_BROWN, "BROWN CIRCUIT — Drain/recycle (1\" HDPE SDR-11)"),
        (C_PIPE_BLACK, "BLACK/WASTE — Drain, P-03 drain pump (1\" HDPE SDR-11)"),
    ]
    ec_map = {"#2060C0": "#1A4A90", "#8D6E63": "#5A3020", "#505050": "#333333"}
    for i, (color, desc) in enumerate(legend_items):
        y = leg_top - i * leg_sp
        lx0 = leg_x / px(1)  # back to mm
        ly0 = y / py(1)
        draw_pipe_path(ax, [lx0, lx0 + 60], [ly0, ly0],
                        PIPE_OD * 0.6, PIPE_WALL_T, px, py,
                        fc=color, ec=ec_map.get(color, C_OUT), zorder=15)
        ax.text(leg_x + px(70), y, desc,
                ha="left", va="center", fontsize=5.5, color=color,
                **FONT, zorder=15)

    # Elbow legend — draw a small sample elbow using draw_pipe_path
    y_el = leg_top - len(legend_items) * leg_sp
    el_x0 = (leg_x) / px(1)        # convert back to mm for draw_pipe_path
    el_yd0 = y_el / py(1)
    el_size = 20  # mm
    draw_pipe_path(ax,
                   [el_x0, el_x0 + el_size, el_x0 + el_size],
                   [el_yd0 - el_size / 2, el_yd0 - el_size / 2, el_yd0 + el_size / 2],
                   PIPE_OD * 0.6, PIPE_WALL_T, px, py,
                   fc="#A0A0A0", ec=C_OUT, zorder=15)
    ax.text(leg_x + px(70), y_el,
            "90° ELBOW (Banjo LE100, 1\" HDPE NPT)",
            ha="left", va="center", fontsize=5.5, color=C_DIM,
            **FONT, zorder=15)

    # Valve legend
    y_vl = y_el - leg_sp
    valve_plan(ax, (leg_x + px(30)) / px(1), y_vl / py(1), 'h', C_DIM, "")
    ax.text(leg_x + px(70), y_vl,
            "BALL VALVE (Banjo V100FP, 1\" poly, quarter-turn)",
            ha="left", va="center", fontsize=5.5, color=C_DIM,
            **FONT, zorder=15)

    # Equipment panel legend
    y_ep = y_vl - leg_sp
    ax.add_patch(Rectangle((leg_x, y_ep - leg_sp * 0.25),
                            px(60), leg_sp * 0.5,
                            fc=C_PLY, ec="#A09060", lw=1.0, zorder=15))
    ax.add_patch(Rectangle((leg_x + px(10), y_ep - leg_sp * 0.15),
                            px(40), leg_sp * 0.3,
                            fc=C_PUMP, ec=C_OUT, lw=0.5, alpha=0.25,
                            ls="--", zorder=15))
    ax.text(leg_x + px(70), y_ep,
            "EQUIPMENT PANEL P-01/P-02/P-03/P-04 pumps ACC-01 (18mm marine ply)",
            ha="left", va="center", fontsize=5.5, color="#A09060",
            **FONT, zorder=15)

    # Filter housing legend
    y_fl = y_ep - leg_sp
    ax.add_patch(Circle((leg_x + px(30), y_fl),
                 px(10), fc="#4A7A4A", ec=C_OUT, lw=1.0,
                 alpha=0.3, zorder=15))
    ax.text(leg_x + px(70), y_fl,
            "BIG BLUE FILTER HOUSING — 4.5\"×10\" (F1=50μ, F2=5μ, F3=GAC)",
            ha="left", va="center", fontsize=5.5, color="#2A5A2A",
            **FONT, zorder=15)

    # ── Dimensions ───────────────────────────────────────────────────────────
    # Corridor width
    draw_dim_v(ax, px(IBC_COL_X - 80), py(near_col_r), py(far_col_l),
               f"{CORRIDOR_W}mm\nCORRIDOR", offset=px(5), fs=6, font=FONT)

    # IBC depth (near column)
    draw_dim_v(ax, px(IBC_COL_X - 80), py(BLUE_IBC_Y), py(near_col_r),
               f"{IBC_D}mm", offset=px(5), fs=5.5, font=FONT)

    # Wall clearance
    draw_dim_v(ax, px(IBC_COL_X - 120), py(0), py(BLUE_IBC_Y),
               f"{BLUE_IBC_Y}mm", offset=px(5), fs=5.5, font=FONT)

    # Far column depth
    draw_dim_v(ax, px(IBC_COL_X - 80), py(IBC_FAR_Y), py(IBC_FAR_Y + IBC_D),
               f"{IBC_D}mm", offset=px(5), fs=5.5, font=FONT)

    # IBC width (along X)
    draw_dim_h(ax, px(IBC_COL_X), px(IBC_COL_X + IBC_W),
               py(IBC_FAR_Y + IBC_D + 120),
               f"{IBC_W}mm IBC WIDTH", offset=py(5), fs=6, font=FONT)

    # Container width (wall to wall)
    draw_dim_v(ax, px(frame_x_r + 225), py(0), py(C_WID),
               f"{C_WID}mm (WALL TO WALL)", offset=px(10), fs=6, right=True, font=FONT)

    # ── Notes (single block, in the right margin directly under the legend) ──
    notes = [
        "INTERNAL PLUMBING PLAN NOTES:",
        "1. 4× Schutz Ecobulk MX 600L IBCs in 2×2 stack.",
        "   Top tier visible; bottom tier shown dashed.",
        "2. All internal pipe 1\" HDPE SDR-11",
        "   (2\" NPT at bulkhead unions).",
        "3. IBC valve faces point toward corridor.",
        "   DN50 butterfly valve (S60×6 thread) at each IBC.",
        "4. S60×6 to 1\" NPT adapters at each IBC (8× total).",
        "5. Ball valves (Banjo V100FP) at each IBC connection.",
        f"6. Pipes routed through {CORRIDOR_W}mm plumbing corridor,",
        "   behind the panel support frame (clear of uprights).",
        "7. X1 fill tees to BOTH Blue totes (IBC-1 & IBC-2),",
        "   each branch dropping straight into its tote.",
        f"8. Equipment panel (18mm marine ply) at X={EQPANEL_X},",
        "   butting the panel support frame: pumps + filters.",
        f"9. Portal frame: seat brackets + corridor uprights. ~{FRAME_WEIGHT}kg.",
    ]
    draw_notes(ax, notes, leg_x, leg_box_bot - py(55), spacing=py(18),
               fs=7, font=FONT, width=775)

    # ── Title block ──────────────────────────────────────────────────────────
    title_block(ax, "SHEET 4 OF 5",
                drawing_title="IBC STACKING & SECURING",
                subtitle="INTERNAL PLUMBING PLAN — IBC LAYOUT, PIPE ROUTING & VALVES",
                scale_note="Axes in mm - VIEW LOOKING DOWN",
                height=0.04)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "ibc-stacking-sheet4.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-stacking-sheet4.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 5 — Internal Plumbing Elevation
#
# Internal plumbing on the sealed end wall, from inside looking +X
# (near/pinhole wall at right, far wall at left — Yd axis inverted).
# Horizontal = Yd (0 = near/pinhole wall), Vertical = Z.
# Shows the 3 bulkhead unions on the wall centerline with pipes routing
# outward to each IBC.  Near-column IBCs on the left, far-column on the
# right, plumbing corridor in the center.  Ball valves, pipe drops/rises,
# and IBC connection points all visible.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet5():
    """Sheet 5 — Internal plumbing elevation with all water system connections.

    Shows the internal plumbing on the sealed end wall, from inside looking +X
    (near/pinhole wall at right, far wall at left).
    All pipe connections rendered as proper fittings: double-wall pipes,
    curved elbows, flanges at unions, and cross-section circles for pipes
    running in the X direction (into the page).
    """
    def sx(mm): return mm
    def sy(mm): return mm

    # ── Pipe fitting drawing helpers ─────────────────────────────────────────
    PIPE_OD = 33.4    # 1" HDPE SDR-11 outer diameter (mm)
    PIPE_WALL = 3.0   # wall thickness
    PIPE_HW = PIPE_OD / 2  # half-width for double-wall rendering

    def draw_tee_fitting(ax, yd, z, color, zo=9):
        """Draw a tee fitting symbol at a pipe junction.
        1" HDPE NPT equal tee (Banjo TEE100 or equivalent).
        """
        s = PIPE_OD * 0.7
        ax.add_patch(Rectangle((sx(yd - s), sy(z - s)),
                                sx(2 * s), sy(2 * s),
                                fc=color, ec=C_OUT, lw=1.5,
                                alpha=0.35, zorder=zo))
        ax.text(sx(yd), sy(z), "T", ha="center", va="center",
                fontsize=4.5, color="white", fontweight="bold",
                **FONT, zorder=zo + 1)

    def draw_flange(ax, yd, z, orientation, color, zo=8):
        """Draw a pipe flange (thick ring) at a connection point.

        orientation: 'h' for horizontal pipe, 'v' for vertical pipe
        """
        fw = 8   # flange width
        fh = PIPE_OD + 20  # flange height (larger than pipe OD)
        if orientation == 'v':
            ax.add_patch(Rectangle((sx(yd - fh / 2), sy(z - fw / 2)),
                                    sx(fh), sy(fw),
                                    fc=color, ec=C_OUT, lw=1.5,
                                    alpha=0.4, zorder=zo))
        else:
            ax.add_patch(Rectangle((sx(yd - fw / 2), sy(z - fh / 2)),
                                    sx(fw), sy(fh),
                                    fc=color, ec=C_OUT, lw=1.5,
                                    alpha=0.4, zorder=zo))

    def pipe_stub_x(ax, yd, z, color, label, label_side="right", zo=8, offset=95):
        """Draw a pipe cross-section circle (pipe running in X, into/out of page) with its
        label on a LEADER pointing back at the circle. This sheet's x-axis is INVERTED, so
        a plain offset+ha label flowed back over the circle; route the label to the
        requested SCREEN side and let the arrow carry the association instead."""
        r_out = PIPE_OD / 2
        r_in = r_out - PIPE_WALL
        ax.add_patch(Circle((sx(yd), sy(z)), sx(r_out),
                             fc=color, ec=C_OUT, lw=1.8, alpha=0.3, zorder=zo))
        ax.add_patch(Circle((sx(yd), sy(z)), sx(r_in),
                             fc="white", ec=C_OUT, lw=0.8, alpha=0.7, zorder=zo + 1))
        # Dot at center
        ax.plot(sx(yd), sy(z), 'o', color=C_OUT, ms=2, zorder=zo + 2)
        # Label on a leader. Screen-right ⟺ smaller data-yd on the inverted axis.
        if label:
            inv = ax.get_xlim()[0] > ax.get_xlim()[1]
            screen_right = (label_side == "right")
            ddir = (-1 if inv else 1) * (1 if screen_right else -1)
            leader(ax, sx(yd + ddir * r_out), sy(z),
                   sx(yd + ddir * offset), sy(z), label,
                   fs=5.5, color=color, ha="left" if screen_right else "right",
                   va="center", arrow_style="-|>", font=FONT)

    # ── Layout bounds ────────────────────────────────────────────────────────
    YD_LO = -200
    YD_HI = C_WID + 200
    Z_LO  = -800
    Z_HI  = C_HGT + 150

    fig, ax = plt.subplots(figsize=(20, 24))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(sx(YD_LO), sx(YD_HI))
    ax.invert_xaxis()   # match physical view orientation (see sheet header)
    ax.set_ylim(sy(Z_LO), sy(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container shell (cross-section at end wall) ──────────────────────────
    # Floor
    ax.add_patch(Rectangle((sx(YD_LO), sy(-30)),
                            sx(YD_HI - YD_LO), sy(30),
                            fc=C_FLOOR, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Ceiling
    ax.add_patch(Rectangle((sx(YD_LO), sy(C_HGT)),
                            sx(YD_HI - YD_LO), sy(30),
                            fc=C_FLOOR, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Near wall (left)
    ax.add_patch(Rectangle((sx(-30), sy(0)),
                            sx(30), sy(C_HGT),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Far wall (right)
    ax.add_patch(Rectangle((sx(C_WID), sy(0)),
                            sx(30), sy(C_HGT),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))

    # Interior face lines
    ax.plot([sx(0), sx(0)], [sy(0), sy(C_HGT)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([sx(C_WID), sx(C_WID)], [sy(0), sy(C_HGT)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([sx(0), sx(C_WID)], [sy(0), sy(0)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([sx(0), sx(C_WID)], [sy(C_HGT), sy(C_HGT)], color=C_OUT, lw=2.0, zorder=3)

    # Wall labels
    ax.text(sx(C_WID / 2), sy(-45), "CONTAINER FLOOR",
            ha="center", va="top", fontsize=6, color=C_DIM, **FONT)
    ax.text(sx(C_WID / 2), sy(C_HGT + 45),
            "SEALED END WALL — INTERNAL PLUMBING ELEVATION (FROM INSIDE, LOOKING +X · NEAR/PINHOLE WALL AT RIGHT, FAR WALL AT LEFT)",
            ha="center", va="bottom", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)
    ax.text(sx(-45), sy(C_HGT / 2), "NEAR\nWALL\n(Yd=0)",
            ha="center", va="center", fontsize=5.5, color=C_DIM, **FONT,
            rotation=90)
    ax.text(sx(C_WID + 45), sy(C_HGT / 2), "FAR\nWALL\n(Yd=2362)",
            ha="center", va="center", fontsize=5.5, color=C_DIM, **FONT,
            rotation=90)

    # ── End wall face (background — the surface we're looking at) ────────────
    ax.add_patch(Rectangle((sx(0), sy(0)),
                            sx(C_WID), sy(C_HGT),
                            fc="#F0F0F0", ec="none", lw=0, alpha=0.3, zorder=1))

    # ── IBCs (shown in elevation, flanking the corridor) ─────────────────────
    near_col_r = BLUE_IBC_Y + IBC_D   # 1046
    far_col_l  = IBC_FAR_Y            # 1316
    platform_z = IBC_H_600             # 1010

    ibc_data = [
        ("IBC-3\nBROWN\n(recycled)", BLUE_IBC_Y, 0, IBC_D, IBC_H_600, C_BROWN_IBC),
        ("IBC-1\nBLUE\n(clean supply)", BLUE_IBC_Y, platform_z + FRAME_RHS + MAT_T,
         IBC_D, IBC_H_600, C_BLUE_IBC),
        ("IBC-4\nWASTE", IBC_FAR_Y, 0, IBC_D, IBC_H_600, C_WASTE_IBC),
        ("IBC-2\nBLUE\n(clean supply)", IBC_FAR_Y, platform_z + FRAME_RHS + MAT_T,
         IBC_D, IBC_H_600, C_BLUE_IBC),
    ]

    for label, yd, z, d, h, color in ibc_data:
        ax.add_patch(Rectangle((sx(yd), sy(z)),
                                sx(d), sy(h),
                                fc=color, ec=C_OUT, lw=1.5, alpha=0.25, zorder=4))
        # Cage uprights
        for post_yd in [yd + 15, yd + d - 15]:
            ax.add_patch(Rectangle((sx(post_yd - CAGE_POST_W / 2), sy(z)),
                                    sx(CAGE_POST_W), sy(h),
                                    fc="none", ec=C_OUT, lw=0.5, zorder=5))
        ax.text(sx(yd + d / 2), sy(z + h / 2), label,
                ha="center", va="center", fontsize=6.5, color=C_OUT,
                fontweight="bold", **FONT, zorder=10)

    # ── Platform beam (between tiers, one per column) ────────────────────────
    for col_l, col_r in [(BLUE_IBC_Y - 5, near_col_r + FRAME_RHS),
                          (far_col_l - FRAME_RHS, IBC_FAR_Y + IBC_D + 5)]:
        ax.add_patch(Rectangle((sx(col_l), sy(platform_z)),
                                sx(col_r - col_l), sy(FRAME_RHS),
                                fc=C_FRAME, ec=C_OUT, lw=1.2, zorder=6, alpha=0.7))

    # ── Corridor uprights ────────────────────────────────────────────────────
    for uyd in [near_col_r, far_col_l - FRAME_RHS]:
        ax.add_patch(Rectangle((sx(uyd), sy(0)),
                                sx(FRAME_RHS), sy(IBC_H_STK + FRAME_RHS),
                                fc=C_FRAME, ec=C_OUT, lw=1.0, zorder=6, alpha=0.6))

    # ── Corridor shading ────────────────────────────────────────────────────
    corr_l = near_col_r + FRAME_RHS
    corr_r = far_col_l - FRAME_RHS
    ax.add_patch(Rectangle((sx(corr_l), sy(0)),
                            sx(corr_r - corr_l), sy(C_HGT),
                            fc=C_CL, ec="none", alpha=0.06, zorder=3))

    # Corridor label
    corr_cx = (near_col_r + far_col_l) / 2
    ax.text(sx(corr_cx), sy(C_HGT - 60),
            f"PLUMBING CORRIDOR",
            ha="center", va="top", fontsize=6, color=C_CL,
            fontweight="bold", **FONT, zorder=10)

    # ── Centerline (vertical) ───────────────────────────────────────────────
    cl_yd = C_WID / 2
    ax.plot([sx(cl_yd), sx(cl_yd)], [sy(-50), sy(C_HGT + 50)],
            color=C_CL, lw=0.8, ls="--", zorder=3)

    # ── Reinforcing plate on wall interior ───────────────────────────────────
    plate_w = 300
    plate_h = EXT_FILL_1_H - 100 + 100  # spans from below lowest port to above highest
    plate_yd = cl_yd - plate_w / 2
    plate_z = 100
    ax.add_patch(Rectangle((sx(plate_yd), sy(plate_z)),
                            sx(plate_w), sy(plate_h),
                            fc=C_STEEL, ec=C_OUT, lw=1.0, alpha=0.2,
                            hatch="...", zorder=5))

    # ── Bulkhead unions (3 ports on wall centerline) ─────────────────────────
    port_r = PORT_DIA / 2
    bh_outer_r = 38   # camlock/union outer visual radius

    # tdir = leader direction for the tag: +1 above the circle, -1 below.
    # X1 routes DOWN (the "PLUMBING CORRIDOR" label sits just above it); X3/X4 route up.
    ports = [
        ("X1", EXT_FILL_1_H, C_BLUE_IBC,   "FILL → IBC-1 (BLUE, TOP NEAR)", -1),
        ("X3", EXT_DRAIN_3_H, C_BROWN_IBC, "DRAIN ← IBC-3 (BROWN, BOTTOM NEAR)", +1),
        ("X4", EXT_DRAIN_4_H, C_WASTE_IBC, "DRAIN ← IBC-4 (WASTE, BOTTOM FAR)", +1),
    ]

    for tag, port_z, color, desc, tdir in ports:
        # Bulkhead union (interior face — flanged circle)
        ax.add_patch(Circle((sx(cl_yd), sy(port_z)),
                             sx(bh_outer_r), fc="#D0D0D0", ec=C_OUT,
                             lw=1.8, zorder=8))
        ax.add_patch(Circle((sx(cl_yd), sy(port_z)),
                             sx(port_r), fc=color, ec=C_OUT,
                             lw=1.2, alpha=0.6, zorder=9))
        # tag on a short leader off the union circle (arrow points back at it)
        leader(ax, sx(cl_yd), sy(port_z + tdir * bh_outer_r),
               sx(cl_yd), sy(port_z + tdir * (bh_outer_r + 55)), tag,
               fs=6.5, color="#000000", ha="center",
               va="bottom" if tdir > 0 else "top",
               arrow_style="-|>", font=FONT)
        # Flange at bulkhead
        draw_flange(ax, cl_yd, port_z, 'h', color, zo=8)

    # ── Pipe system colors ───────────────────────────────────────────────────
    C_PIPE_BLUE   = "#2060C0"   # Blue circuit (clean supply)
    C_PIPE_BROWN  = "#8D6E63"   # Brown circuit (recycled)
    C_PIPE_BLACK  = "#505050"   # Black/waste
    C_PIPE_FILTER = "#E65100"   # Filter unit circuit
    pipe_lw = 2.5

    # ── IBC connection heights ───────────────────────────────────────────────
    top_ibc_top = platform_z + FRAME_RHS + MAT_T + IBC_H_600
    fill_conn_z = top_ibc_top - 80   # fill inlet near top of top-tier IBC
    drain_conn_z = 185   # IBC butterfly valve centerline ~175-200mm above floor

    near_ibc_cx = BLUE_IBC_Y + IBC_D / 2   # IBC-1/3 center Yd
    far_ibc_cx  = IBC_FAR_Y + IBC_D / 2    # IBC-2/4 center Yd

    # IBC valve faces point toward corridor. Fill cap is on top, offset
    # ~250mm from the valve face (front) toward the corridor side.
    FILL_CAP_OFFSET = 250  # mm from valve face (corridor edge)
    f1_fill_yd = BLUE_IBC_Y + IBC_D - FILL_CAP_OFFSET   # near IBC fill cap Yd

    # ── X1: Bulkhead → tee → drop into BOTH Blue totes (matches 3D) ───────
    # Fill header runs in Yd at Z=2250 over both top totes; a tee at the
    # corridor centerline (fed by the bulkhead) drops into each fill cap. No
    # cross-connect — both Blue totes are filled directly in parallel.
    f1_drop_yd = f1_fill_yd                      # near IBC-1 fill cap Yd
    far_fill_yd = IBC_FAR_Y + FILL_CAP_OFFSET    # far IBC-2 fill cap Yd
    # header + both drops as ONE ⊓-path so the 90° turns round into proper elbows
    # (drawing the header and the drops as separate straight calls left sharp corners).
    draw_pipe_path(ax,
                   [f1_drop_yd, f1_drop_yd, far_fill_yd, far_fill_yd],
                   [fill_conn_z, EXT_FILL_1_H, EXT_FILL_1_H, fill_conn_z],
                   PIPE_OD, PIPE_WALL, sx, sy,
                   fc=C_PIPE_BLUE, ec="#1A4A90", zorder=7)
    for dyd in (f1_drop_yd, far_fill_yd):
        draw_flange(ax, dyd, top_ibc_top, 'v', C_PIPE_BLUE)
        ax.annotate("", xy=(sx(dyd), sy(fill_conn_z + 15)),
                    xytext=(sx(dyd), sy(fill_conn_z + 80)),
                    arrowprops=dict(arrowstyle="-|>", color=C_PIPE_BLUE, lw=1.5))
    # tee at the corridor centerline (bulkhead feed point)
    draw_tee_fitting(ax, cl_yd, EXT_FILL_1_H, C_PIPE_BLUE)
    # CV1 check valve — prevents backflow toward the bulkhead
    _draw_check_valve_h(ax, sx, sy, cl_yd + 95, EXT_FILL_1_H, C_PIPE_BLUE, "CV1",
                        text_color = "#000000", flow_dir="left")
    # V1 on the near header run, in the corridor
    v1_yd = (cl_yd + near_col_r) / 2
    _draw_valve_elev_h(ax, sx, sy, v1_yd, EXT_FILL_1_H, C_PIPE_BLUE, "V1", text_color="#000000", lup=False)

    # ── X3: IBC-3 (near, bottom) → Bulkhead — BROWN drain ───────────────────
    d3_yd = near_col_r  # corridor-facing edge of near IBC
    # L-shaped path: vertical rise → 90° elbow → horizontal to bulkhead
    draw_pipe_path(ax,
                   [d3_yd, d3_yd, cl_yd + bh_outer_r + 5],
                   [drain_conn_z, EXT_DRAIN_3_H, EXT_DRAIN_3_H],
                   PIPE_OD, PIPE_WALL, sx, sy,
                   fc=C_PIPE_BROWN, ec="#5A3020", zorder=7)
    draw_flange(ax, d3_yd, drain_conn_z, 'v', C_PIPE_BROWN)
    # V3 on vertical run
    _draw_valve_elev(ax, sx, sy, d3_yd,
                     drain_conn_z + (EXT_DRAIN_3_H - drain_conn_z) * 0.45,
                     C_PIPE_BROWN, "V3")
    # CV3 check valve — prevents backflow from bulkhead into IBC-3
    cv3_yd = cl_yd + bh_outer_r + 50
    _draw_check_valve_h(ax, sx, sy, cv3_yd, EXT_DRAIN_3_H, C_PIPE_BROWN, "CV3",
                        flow_dir="right")
    # Flow arrow toward wall
    ax.annotate("", xy=(sx(cl_yd - 5), sy(EXT_DRAIN_3_H)),
                xytext=(sx(cl_yd - 70), sy(EXT_DRAIN_3_H)),
                arrowprops=dict(arrowstyle="-|>", color=C_PIPE_BROWN, lw=1.5))
    # P-05 brown drain pump — on X3 vertical run below elbow
    p05_z = EXT_DRAIN_3_H - 60
    _draw_pump_symbol(ax, sx, sy, d3_yd - 60, p05_z, C_PIPE_BROWN, "P-05")
    # Dashed connection from pump to pipe
    ax.plot([sx(d3_yd - PIPE_HW), sx(d3_yd - 60 + 22)],
            [sy(p05_z), sy(p05_z)],
            color=C_PIPE_BROWN, lw=1.5, ls="--", zorder=7)

    # ── X4: IBC-4 (far, bottom) → Bulkhead — WASTE drain ────────────────────
    # NOTE: X4 at Z=200mm limits gravity drain — P-03 waste pump evacuates
    # the residual ~120L below X4 height.
    d4_yd = far_col_l  # corridor-facing edge of far IBC
    # L-shaped path: vertical rise → 90° elbow → horizontal to bulkhead
    draw_pipe_path(ax,
                   [d4_yd, d4_yd, cl_yd - bh_outer_r - 5],
                   [drain_conn_z, EXT_DRAIN_4_H, EXT_DRAIN_4_H],
                   PIPE_OD, PIPE_WALL, sx, sy,
                   fc=C_PIPE_BLACK, ec="#333333", zorder=7)
    draw_flange(ax, d4_yd, drain_conn_z, 'v', C_PIPE_BLACK)
    # V4 on vertical run
    _draw_valve_elev(ax, sx, sy, d4_yd,
                     drain_conn_z + (EXT_DRAIN_4_H - drain_conn_z) * 0.45,
                     C_PIPE_BLACK, "V4", lside="left")
    # CV4 check valve — prevents backflow from bulkhead into IBC-4
    cv4_yd = cl_yd - bh_outer_r - 50
    _draw_check_valve_h(ax, sx, sy, cv4_yd, EXT_DRAIN_4_H, C_PIPE_BLACK, "CV4",
                        flow_dir="left")
    ax.annotate("", xy=(sx(cl_yd + 5), sy(EXT_DRAIN_4_H)),
                xytext=(sx(cl_yd + 70), sy(EXT_DRAIN_4_H)),
                arrowprops=dict(arrowstyle="-|>", color=C_PIPE_BLACK, lw=1.5))
    # P-03 waste evacuation pump — on X4 vertical run below elbow
    p03_z = EXT_DRAIN_4_H - 60
    _draw_pump_symbol(ax, sx, sy, d4_yd + 60, p03_z, C_PIPE_BLACK, "P-03")
    # Dashed connection from pump to pipe
    ax.plot([sx(d4_yd + PIPE_HW), sx(d4_yd + 60 - 22)],
            [sy(p03_z), sy(p03_z)],
            color=C_PIPE_BLACK, lw=1.5, ls="--", zorder=7)

    # ── Blue outflow manifold (X-direction, into the page) ───────────────────
    # Two isolation valves (V-B1, V-B2) — one per IBC outlet — join at tee
    # in corridor, then V-B3 after tee → single pipe to P-01 → spray bar.
    # Blue IBCs use their built-in DN50 butterfly valve (S60×6 thread) on the
    # corridor-facing face, ~185mm above the platform they sit on.
    top_tier_base = platform_z + FRAME_RHS + MAT_T  # floor of top-tier IBCs
    blue_out_z = top_tier_base + drain_conn_z  # drain valve height on top-tier

    # IBC-1 outlet (near column) — at corridor-facing drain valve
    b1_yd = near_col_r  # valve face points toward corridor
    pipe_stub_x(ax, b1_yd, blue_out_z, C_PIPE_BLUE,
                "IBC-1\nOUTLET", label_side="right")
    # Horizontal pipe from IBC-1 toward corridor center
    draw_pipe_path(ax, [b1_yd, corr_l + 10], [blue_out_z, blue_out_z],
                   PIPE_OD, PIPE_WALL, sx, sy,
                   fc=C_PIPE_BLUE, ec="#1A4A90", zorder=7)
    # V-B1 on this horizontal run
    vb1_yd = (b1_yd + corr_l) / 2
    _draw_valve_elev_h(ax, sx, sy, vb1_yd, blue_out_z, C_PIPE_BLUE, "VB1", text_color="#000000")

    # IBC-2 outlet (far column) — at corridor-facing drain valve
    b2_yd = far_col_l  # valve face points toward corridor
    pipe_stub_x(ax, b2_yd, blue_out_z, C_PIPE_BLUE,
                "IBC-2\nOUTLET", label_side="left")
    # Horizontal pipe from IBC-2 toward corridor center
    draw_pipe_path(ax, [corr_r - 10, b2_yd], [blue_out_z, blue_out_z],
                   PIPE_OD, PIPE_WALL, sx, sy,
                   fc=C_PIPE_BLUE, ec="#1A4A90", zorder=7)
    # V-B2 on this horizontal run
    vb2_yd = (b2_yd + corr_r) / 2
    _draw_valve_elev_h(ax, sx, sy, vb2_yd, blue_out_z, C_PIPE_BLUE, "VB2", text_color="#000000")

    # Tee fitting in corridor where both outlets merge
    draw_tee_fitting(ax, corr_cx, blue_out_z, C_PIPE_BLUE)

    # V-B3 after the tee — single merged pipe continues to P-01
    vb3_z = blue_out_z - 60
    draw_pipe_path(ax, [corr_cx, corr_cx], [vb3_z, blue_out_z],
                   PIPE_OD, PIPE_WALL, sx, sy,
                   fc=C_PIPE_BLUE, ec="#1A4A90", zorder=7)
    _draw_valve_elev(ax, sx, sy, corr_cx, vb3_z + 15, C_PIPE_BLUE, "VB3", text_color="#000000")
    # Merged pipe stub (X-direction → P-01 → spray bar)
    pipe_stub_x(ax, corr_cx, vb3_z - 30, C_PIPE_BLUE,
                "P-01 → SPRAY BAR", label_side="right", offset=225)

    # ── Brown IBC-3 inlet ← tray sump (pumped via P-04) ──────────────────────
    # Water collects in sump well at tray low point. P-04 suction pickup
    # draws from sump, pumps up to IBC-3 fill cap (DN150) on top.
    # Cannot gravity feed — fill cap is ~900mm above tray floor.
    brown_in_z = IBC_H_600 - 80  # near top of bottom-tier IBC
    pipe_stub_x(ax, near_ibc_cx, brown_in_z, C_PIPE_BROWN,
                "P-04 ← TRAY\nSUMP (PUMPED)", label_side="left")
    # P-04 tray drain transfer pump — on the brown inlet line
    p04_z = brown_in_z + 60
    _draw_pump_symbol(ax, sx, sy, near_ibc_cx - 80, p04_z, C_PIPE_BROWN, "P-04")
    ax.plot([sx(near_ibc_cx - 80 + 22), sx(near_ibc_cx - PIPE_OD / 2)],
            [sy(brown_in_z), sy(brown_in_z)],
            color=C_PIPE_BROWN, lw=1.5, ls="--", zorder=7)

    # ── Brown IBC-3 outlet → P-02 pump → filter unit ────────────────────────
    # Uses IBC-3's built-in DN50 butterfly valve at corridor-facing face.
    # Offset below X3 horizontal run at Z=400 to avoid pipe crossing.
    brown_out_z = 250
    pipe_stub_x(ax, near_col_r, brown_out_z, C_PIPE_BROWN,
                "TO P-02 →\nFILTER UNIT", label_side="right")

    # ── Filter unit return → IBC-2 (cleaned water returns to supply) ────────
    # Returns through top of IBC-2 (fill cap area)
    filter_ret_z = top_ibc_top - 80  # near top of top-tier far IBC
    pipe_stub_x(ax, far_ibc_cx, filter_ret_z, C_PIPE_FILTER,
                "FILTER\nRETURN", label_side="right")

    # ── Waste IBC-4 inlet ← diverter/bypass (rejected filtrate) ─────────────
    # Enters through IBC-4 fill cap (DN150) on top. Filter unit reject/bypass
    # line feeds into waste IBC via fill cap — cannot use drain valve (would
    # drain out existing waste when opened).
    waste_in_z = IBC_H_600 - 80  # near top of bottom-tier far IBC
    pipe_stub_x(ax, far_ibc_cx, waste_in_z, C_PIPE_BLACK,
                "FILTER REJECT\nVIA FILL CAP (DN150)", label_side="right")

    # ── Pipe labels for bulkhead connections ─────────────────────────────────
    leader(ax, sx(f1_fill_yd), sy(EXT_FILL_1_H),
           sx(BLUE_IBC_Y + IBC_D * 0.5), sy(EXT_FILL_1_H + 25),
           "X1 → IBC-1 FILL CAP\n(DN150, TOP NEAR)\n1\" HDPE",
           color=C_PIPE_BLUE, fs=5.5,
           ha="right", va="bottom", arrow_style="-|>", font=FONT)
    leader(ax, sx(near_col_r), sy(drain_conn_z),
           sx(BLUE_IBC_Y + IBC_D * 0.7), sy(drain_conn_z - 80),
           "X3 ← IBC-3 VALVE\n(DN50, S60×6, BROWN\nBOTTOM NEAR)\n1\" HDPE",
           color=C_PIPE_BROWN, fs=5.5,
           ha="right", va="top", arrow_style="-|>", font=FONT)
    leader(ax, sx(far_col_l), sy(drain_conn_z),
           sx(IBC_FAR_Y + IBC_D * 0.5), sy(drain_conn_z - 80),
           "X4 ← IBC-4 VALVE\n(DN50, S60×6, WASTE\nBOTTOM FAR)\n1\" HDPE",
           color=C_PIPE_BLACK, fs=5.5,
           ha="left", va="top", arrow_style="-|>", font=FONT)

    # ── Legend ───────────────────────────────────────────────────────────────
    leg_x = sx(YD_HI - 200)
    leg_top = sy(-200)
    leg_spacing = sy(33)

    # Legend background box
    n_leg_items = 8  # 4 pipes + cross-section + elbow + tee + check valve
    # This sheet's x-axis is INVERTED, so the ha="left" legend text at leg_x+70 renders
    # screen-rightward toward SMALLER data — the box must extend that way too. Anchor it
    # just past the swatch and give it a negative width so it surrounds swatch + text.
    leg_box_x = leg_x + sx(75)
    leg_box_top = leg_top + leg_spacing * 0.5
    leg_box_bot = leg_top - n_leg_items * leg_spacing + leg_spacing * 0.3
    leg_box_w = -sx(880)
    ax.add_patch(Rectangle((leg_box_x, leg_box_bot), leg_box_w,
                            leg_box_top - leg_box_bot,
                            fc="#F0F0F0", ec=C_OUT, lw=0.6, zorder=14))

    legend_items = [
        (C_PIPE_BLUE,   "BLUE CIRCUIT — Clean supply (fill, VB1/VB2 → tee → VB3 → P-01 → spray bar)"),
        (C_PIPE_BROWN,  "BROWN CIRCUIT — Recycled (P-04 ← tray sump → IBC-3, P-02 → filter unit, P-05 drain pump)"),
        (C_PIPE_FILTER, "FILTER CIRCUIT — Filtered return to IBC-2"),
        (C_PIPE_BLACK,  "BLACK/WASTE — Rejected filtrate via fill cap → IBC-4, P-03 drain pump"),
    ]
    ec_map6 = {"#2060C0": "#1A4A90", "#8D6E63": "#5A3020",
               "#E65100": "#B34000", "#505050": "#333333"}
    for i, (color, desc) in enumerate(legend_items):
        y = leg_top - i * leg_spacing
        lx0 = leg_x / sx(1)  # back to mm
        ly0 = y / sy(1)
        draw_pipe_path(ax, [lx0, lx0 + 60], [ly0, ly0],
                        PIPE_OD * 0.6, PIPE_WALL, sx, sy,
                        fc=color, ec=ec_map6.get(color, C_OUT), zorder=15)
        ax.text(leg_x + sx(-10), y, desc,
                ha="left", va="center", fontsize=5.5, color=color,
                **FONT, zorder=15)

    # Cross-section circle legend
    y_cs = leg_top - len(legend_items) * leg_spacing
    r_cs = PIPE_OD / 2 / (sx(1))  # scaled radius
    w_cs = PIPE_WALL / (sx(1))
    draw_pipe_end(ax, leg_x + sx(30), y_cs, sx(PIPE_OD / 2), sx(PIPE_WALL),
                  fc="#A0A0A0", ec=C_OUT, zorder=15)
    ax.text(leg_x + sx(-10), y_cs,
            "PIPE CROSS-SECTION (running in X direction, into page)",
            ha="left", va="center", fontsize=5.5, color=C_DIM,
            **FONT, zorder=15)

    # Elbow fitting legend — draw a small sample elbow
    y_el = y_cs - leg_spacing
    el_x0 = leg_x / sx(1)
    el_z0 = y_el / sy(1)
    el_size = 20
    draw_pipe_path(ax,
                   [el_x0, el_x0 + el_size, el_x0 + el_size],
                   [el_z0 - el_size / 2, el_z0 - el_size / 2, el_z0 + el_size / 2],
                   PIPE_OD * 0.6, PIPE_WALL, sx, sy,
                   fc="#A0A0A0", ec=C_OUT, zorder=15)
    ax.text(leg_x + sx(-10), y_el,
            "90° ELBOW FITTING (1\" HDPE NPT — Banjo LE100 or equiv.)",
            ha="left", va="center", fontsize=5.5, color=C_DIM,
            **FONT, zorder=15)

    # Tee fitting legend
    y_tee = y_el - leg_spacing
    s_el = PIPE_OD * 0.5  # fitting block half-size for tee symbol
    ax.add_patch(Rectangle((leg_x + sx(30) - sx(s_el), y_tee - sy(s_el)),
                            sx(2 * s_el), sy(2 * s_el),
                            fc="#A0A0A0", ec=C_OUT, lw=1.2, alpha=0.35, zorder=15))
    ax.text(leg_x + sx(30), y_tee, "T", ha="center", va="center",
            fontsize=4.5, color="white", fontweight="bold", **FONT, zorder=16)
    ax.text(leg_x + sx(-10), y_tee,
            "TEE FITTING (1\" HDPE NPT — Banjo TEE100 or equiv.)",
            ha="left", va="center", fontsize=5.5, color=C_DIM,
            **FONT, zorder=15)

    # Check valve legend
    y_cv = y_tee - leg_spacing
    cv_vs = 10
    tri_cv = Polygon([(leg_x + sx(30 - cv_vs), y_cv - sy(cv_vs)),
                       (leg_x + sx(30 - cv_vs), y_cv + sy(cv_vs)),
                       (leg_x + sx(30 + cv_vs), y_cv)], closed=True,
                      fc="#A0A0A0", ec=C_OUT, lw=1.0, alpha=0.45, zorder=15)
    ax.add_patch(tri_cv)
    ax.plot([leg_x + sx(30 - cv_vs), leg_x + sx(30 - cv_vs)],
            [y_cv - sy(cv_vs + 3), y_cv + sy(cv_vs + 3)],
            color=C_OUT, lw=1.8, zorder=16)
    ax.text(leg_x + sx(-10), y_cv,
            "CHECK VALVE (1\" NPT spring — prevents backflow on all bulkhead lines)",
            ha="left", va="center", fontsize=5.5, color=C_DIM,
            **FONT, zorder=15)

    # ── Dimensions ───────────────────────────────────────────────────────────
    dim_yd = cl_yd + plate_w / 2 + 100
    for port_z, label in [ (EXT_DRAIN_4_H, f"X4: {EXT_DRAIN_4_H}mm"),
                           (EXT_DRAIN_3_H, f"X3: {EXT_DRAIN_3_H}mm"),
                           (EXT_FILL_1_H, f"X1: {EXT_FILL_1_H}mm"),]:
        draw_dim_v(ax, sx(dim_yd), sy(0), sy(port_z),
                   label, offset=sx(30), fs=5.5, right=True, font=FONT)
        dim_yd += 50

    # Container interior width
    draw_dim_h(ax, sx(0), sx(C_WID), sy(-80),
               f"{C_WID}mm  INTERIOR WIDTH", offset=sy(10), above=False, fs=6, font=FONT)

    # Corridor width
    draw_dim_h(ax, sx(near_col_r), sx(far_col_l), sy(C_HGT - 30),
               f"{CORRIDOR_W}mm CORRIDOR", offset=sy(5), fs=5.5, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        "INTERNAL PLUMBING ELEVATION NOTES:",
        "1. Sealed end wall internal plumbing, from inside looking +X (near/pinhole wall at right, far wall at left). All internal pipe 1\" ",
        "   HDPE SDR-11 (2\" NPT at bulkhead unions).",
        "2. IBC valve faces point toward plumbing corridor. DN50 butterfly valve (S60×6 thread), ~185mm above floor.",
        "3. X1 fill header tees to BOTH Blue totes (IBC-1 & IBC-2); each branch drops into the fill cap (DN150, offset ~250mm from valve face",
        "   toward corridor). Filled in parallel — no cross-connect.",
        "4. S60×6 to 1\" NPT adapters (e.g. IBC-S60-1NPT) at each IBC valve connection (8× total).",
        "5. Fill tee + header set back behind the panel support frame top rail; drains routed behind the frame (clear of the uprights), matching",
        "   the 3D model.",
        "6. Blue outflow: IBC-1 valve → VB1 → tee ← VB2 ← IBC-2 valve; after tee → VB3 → P-01 → spray bar.",
        "7. Ball valves: Banjo V100FP 1\" polypropylene full-port, quarter-turn. All hand-operated.",
        "8. X3 at Z=400mm / X4 at Z=200mm: P-05 and P-03 drain pumps evacuate IBCs through bulkhead ports at disposal.",
        "9. 90° elbows (Banjo LE100) at all bends. Flanges at all bulkhead and IBC connections.",
        "10. Check valves CV1/CV3/CV4 (1\" NPT spring check) on all three bulkhead lines — prevents backflow through bulkhead unions.",
        "11. IBC-3 (Brown) filled from top via fill cap (DN150). P-04 suction pickup draws from tray sump, pumps to IBC-3 fill cap (~900mm lift).",
        "12. IBC-4 (Waste) filled from top via fill cap (DN150). Filter unit reject/bypass line feeds into waste IBC — cannot use drain valve.",
    ]
    draw_notes(ax, notes, sx(YD_LO + 1530), sy(-180), spacing=sy(22),
               fs=7, font=FONT, width=1500)

    # ── Title block ──────────────────────────────────────────────────────────
    title_block(ax, "SHEET 5 OF 5",
                drawing_title="IBC STACKING & SECURING",
                subtitle="INTERNAL PLUMBING ELEVATION — ALL WATER SYSTEM CONNECTIONS",
                scale_note="Axes in mm - VIEW FROM INSIDE",
                height=0.04)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "ibc-stacking-sheet5.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-stacking-sheet5.png saved")


def _draw_valve_elev(ax, sx, sy, yd, z, color, label, lside="right", text_color=None):
    """Draw a ball valve symbol (bowtie in white circle) in elevation view at (yd, z).
    On a VERTICAL pipe — so the label is leadered out to the SIDE (lside), not buried in
    the symbol. text_color overrides the label colour (default = the pipe colour, which is
    readable on the light background; pass e.g. 'white' if the label sits on a dark fill)."""
    vs = 18  # half-size in mm
    cr = vs * 1.6  # circle radius in mm
    # White circle background
    circ = plt.Circle((sx(yd), sy(z)),
                       abs(sx(cr) - sx(0)),  # radius in data coords
                       fc="white", ec=color, lw=1.5, zorder=11)
    ax.add_patch(circ)
    # Bowtie oriented horizontally (left/right triangles meeting at center)
    tri1 = Polygon([(sx(yd - vs), sy(z - vs)),
                     (sx(yd - vs), sy(z + vs)),
                     (sx(yd), sy(z))], closed=True,
                    fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=12)
    tri2 = Polygon([(sx(yd + vs), sy(z - vs)),
                     (sx(yd + vs), sy(z + vs)),
                     (sx(yd), sy(z))], closed=True,
                    fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=12)
    ax.add_patch(tri1)
    ax.add_patch(tri2)
    if label:
        # leader the label out to the side (inversion-aware), not white-on-symbol
        inv = ax.get_xlim()[0] > ax.get_xlim()[1]
        screen_right = (lside == "right")
        ddir = (-1 if inv else 1) * (1 if screen_right else -1)
        leader(ax, sx(yd + ddir * cr), sy(z),
               sx(yd + ddir * (cr + 48)), sy(z), label,
               fs=5, color=text_color or color,
               ha="left" if screen_right else "right",
               va="center", font=FONT)


def _draw_valve_elev_h(ax, sx, sy, yd, z, color, label, lup=True, text_color=None):
    """Draw a ball valve symbol (bowtie in white circle) on a HORIZONTAL pipe in elevation.
    Bowtie axis perpendicular to flow — oriented vertically. The label is leadered ABOVE
    (lup) or below the symbol instead of being buried white inside it. text_color overrides
    the label colour (default = the pipe colour)."""
    vs = 18  # half-size in mm
    cr = vs * 1.6  # circle radius in mm
    # White circle background
    circ = plt.Circle((sx(yd), sy(z)),
                       abs(sx(cr) - sx(0)),  # radius in data coords
                       fc="white", ec=color, lw=1.5, zorder=11)
    ax.add_patch(circ)
    # Top triangle (pointing down)
    tri1 = Polygon([(sx(yd - vs), sy(z + vs)),
                     (sx(yd + vs), sy(z + vs)),
                     (sx(yd), sy(z))], closed=True,
                    fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=12)
    # Bottom triangle (pointing up)
    tri2 = Polygon([(sx(yd - vs), sy(z - vs)),
                     (sx(yd + vs), sy(z - vs)),
                     (sx(yd), sy(z))], closed=True,
                    fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=12)
    ax.add_patch(tri1)
    ax.add_patch(tri2)
    if label:
        # leader the label above/below the symbol, not white-on-symbol
        zdir = 1 if lup else -1
        leader(ax, sx(yd), sy(z + zdir * cr),
               sx(yd), sy(z + zdir * (cr + 42)), label,
               fs=5, color=text_color or color, ha="center",
               va="bottom" if lup else "top", font=FONT)


def _draw_check_valve_h(ax, sx, sy, yd, z, color, label, text_color=None, flow_dir="right"):
    """Draw a check valve (non-return valve) on a HORIZONTAL pipe.

    Triangle pointing in flow direction with a perpendicular bar at the
    upstream end (the seat).  flow_dir: 'left' or 'right'.
    """
    vs = 16  # half-size in mm
    if flow_dir == "right":
        # Triangle pointing right  →
        tri = Polygon([(sx(yd - vs), sy(z - vs)),
                        (sx(yd - vs), sy(z + vs)),
                        (sx(yd + vs), sy(z))], closed=True,
                       fc=color, ec=C_OUT, lw=1.0, alpha=0.45, zorder=11)
        # Bar at upstream (left) end
        ax.plot([sx(yd - vs), sx(yd - vs)], [sy(z - vs - 4), sy(z + vs + 4)],
                color=C_OUT, lw=2.0, zorder=12)
    else:
        # Triangle pointing left  ←
        tri = Polygon([(sx(yd + vs), sy(z - vs)),
                        (sx(yd + vs), sy(z + vs)),
                        (sx(yd - vs), sy(z))], closed=True,
                       fc=color, ec=C_OUT, lw=1.0, alpha=0.45, zorder=11)
        # Bar at upstream (right) end
        ax.plot([sx(yd + vs), sx(yd + vs)], [sy(z - vs - 4), sy(z + vs + 4)],
                color=C_OUT, lw=2.0, zorder=12)
    ax.add_patch(tri)
    if label:
        ax.text(sx(yd), sy(z + vs + 14), label,
                ha="center", va="bottom", fontsize=4.5,
                color=color if text_color == None else text_color,
                fontweight="bold", **FONT, zorder=13)


def _draw_pump_symbol(ax, sx, sy, yd, z, color, label):
    """Draw a pump symbol (circle with arrow) in elevation view."""
    r = 22
    ax.add_patch(Circle((sx(yd), sy(z)), sx(r),
                         fc=color, ec=C_OUT, lw=1.8, alpha=0.3, zorder=11))
    # Triangle inside (flow direction indicator)
    ts = 12
    tri = Polygon([(sx(yd - ts), sy(z - ts)),
                    (sx(yd - ts), sy(z + ts)),
                    (sx(yd + ts), sy(z))], closed=True,
                   fc=color, ec=C_OUT, lw=1.0, alpha=0.6, zorder=12)
    ax.add_patch(tri)
    if label:
        ax.text(sx(yd), sy(z + r + 12), label,
                ha="center", va="bottom", fontsize=5.5, color=color,
                fontweight="bold", **FONT, zorder=13)

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    print("Generating IBC stacking diagrams...")
    sheet1()  # cross-section elevation -> ibc-stacking-sheet1.png
    sheet2()  # fastening details -> ibc-stacking-sheet2.png
    sheet3()  # external plumbing panel -> ibc-stacking-sheet3.png
    sheet4()  # internal plumbing plan -> ibc-stacking-sheet4.png
    sheet5()  # internal plumbing elevation -> ibc-stacking-sheet5.png
    print("Done.")
