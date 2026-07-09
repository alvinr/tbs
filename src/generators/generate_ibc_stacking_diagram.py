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
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle

from tbs_constants import C_LEN, C_WID, C_HGT, IBC_COL_X, IBC_W, IBC_D, IBC_H_1000, IBC_H_STK_1000, BLUE_IBC_Y, IBC_FAR_Y, WALKWAY_W, WALKWAY_RIGHT_X, C_BLUE_IBC, C_BROWN_IBC, C_WASTE_IBC, C_PUMP, EXT_FILL_1_H, EXT_DRAIN_3_H, EXT_DRAIN_4_H, EQPANEL_X, EQPANEL_T, EQPANEL_YD, PANEL_FRAME_X, IBC_FRAME_RHS, IBC_FOOT_PLATE, IBC_FOOT_PLATE_T, IBC_FOOT_BOLT_PCD, IBC_FOOT_BOLT_N, BB_OD, DIAGRAMS_DIR
sys_models = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models")
if sys_models not in os.sys.path:
    os.sys.path.insert(0, sys_models)
import generate_corridor_water_panel as cp   # deep-box frame geometry (single source: cp.frame)

from tbs_title_block import title_block
from tbs_drawing import (draw_dim_h, draw_dim_v, leader, draw_notes,
                         bolt_holes,
                         draw_pipe_path as _tbs_pipe_path,
                         draw_pipe_end as _tbs_pipe_end)
from tbs_constants import DIAGRAM_DPI

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
FRAME_WEIGHT   = 90     # kg (restraint deep 4-leg box: 4 uprights + rings + 4 feet + front bars + hangers + exterior wall plates); see weight-distribution-report §3.3

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
CEIL_CLEAR     = C_HGT - IBC_H_STK_1000  # = 368mm

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

    # ── Layout bounds ─────────────────────────────────────────────────────────
    YD_LO = -120
    YD_HI = C_WID + 120
    Z_LO  = -580
    Z_HI  = C_HGT + 100

    fig, ax = plt.subplots(figsize=(18, 22))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim((YD_LO), (YD_HI))
    ax.invert_xaxis()   # match physical view orientation (see sheet header)
    ax.set_ylim((Z_LO), (Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container shell ───────────────────────────────────────────────────────
    WALL_T = 2.0   # visual wall thickness (mm at this scale)

    # Floor
    ax.add_patch(Rectangle(((YD_LO), (-30)),
                            (YD_HI - YD_LO), (30),
                            fc=C_FLOOR, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Ceiling
    ax.add_patch(Rectangle(((YD_LO), (C_HGT)),
                            (YD_HI - YD_LO), (30),
                            fc=C_FLOOR, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Near wall (left)
    ax.add_patch(Rectangle(((-30), (0)),
                            (30), (C_HGT),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Far wall (right)
    ax.add_patch(Rectangle(((C_WID), (0)),
                            (30), (C_HGT),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))

    # Floor/ceiling/wall labels
    ax.text((C_WID / 2), (-45), "CONTAINER FLOOR",
            ha="center", va="top", fontsize=6, color=C_DIM, **FONT)
    ax.text((C_WID / 2), (C_HGT + 45), "CONTAINER CEILING (Z=2388mm)",
            ha="center", va="bottom", fontsize=6, color=C_DIM, **FONT)
    ax.text((-50), (C_HGT * 0.45), "NEAR WALL",
            ha="center", va="center", fontsize=5.5, color=C_DIM, **FONT,
            rotation=90)
    ax.text((C_WID + 45), (C_HGT * 0.55), "FAR WALL",
            ha="center", va="center", fontsize=5.5, color=C_DIM, **FONT,
            rotation=90)

    # Interior face lines
    ax.plot([(0), (0)], [(0), (C_HGT)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([(C_WID), (C_WID)], [(0), (C_HGT)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([(0), (C_WID)], [(0), (0)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([(0), (C_WID)], [(C_HGT), (C_HGT)], color=C_OUT, lw=2.0, zorder=3)

    # ── IBCs ──────────────────────────────────────────────────────────────────
    # In this cross-section (looking along X), we see Yd vs Z.
    # Near column: Yd = BLUE_IBC_Y to BLUE_IBC_Y + IBC_D
    # Far column:  Yd = IBC_FAR_Y  to IBC_FAR_Y + IBC_D

    # v2 layout (unchanged): Brown/Waste bottom, Blue on top; DIRECT-STACK so the
    # top tier sits at IBC_H_1000 (cage-on-cage, no platform deck).
    ibc_data = [
        ("IBC-3\nBROWN\n(recycled)", BLUE_IBC_Y, 0, IBC_D, IBC_H_1000, C_BROWN_IBC),
        ("IBC-1\nBLUE\n(clean supply)", BLUE_IBC_Y, IBC_H_1000,
         IBC_D, IBC_H_1000, C_BLUE_IBC),
        ("IBC-4\nWASTE", IBC_FAR_Y, 0, IBC_D, IBC_H_1000, C_WASTE_IBC),
        ("IBC-2\nBLUE\n(clean supply)", IBC_FAR_Y, IBC_H_1000,
         IBC_D, IBC_H_1000, C_BLUE_IBC),
    ]

    for label, yd, z, d, h, color in ibc_data:
        # IBC body (translucent tank)
        ax.add_patch(Rectangle(((yd), (z)),
                                (d), (h),
                                fc=color, ec=C_OUT, lw=1.5, alpha=0.35, zorder=5))
        # Cage uprights (4 posts at corners)
        for post_yd in [yd + 15, yd + d - 15]:
            ax.add_patch(Rectangle(((post_yd - CAGE_POST_W / 2), (z)),
                                    (CAGE_POST_W), (h),
                                    fc="none", ec=C_OUT, lw=0.6, zorder=6))
        # Cage top rail
        ax.plot([(yd), (yd + d)], [(z + h), (z + h)],
                color=C_OUT, lw=1.2, zorder=6)
        # Label
        ax.text((yd + d / 2), (z + h * 0.6), label,
                ha="center", va="center", fontsize=7, color=C_OUT,
                fontweight="bold", **FONT, zorder=10)

    # ── Restraint frame (deep 4-leg box — direct-stack, no platform) ──
    near_col_r = BLUE_IBC_Y + IBC_D          # 1046 — near corridor edge
    far_col_l  = IBC_FAR_Y                   # 1316 — far corridor edge
    junction_z = IBC_H_1000                  # 1168 — direct-stack junction
    top_z = IBC_H_STK_1000 - 40              # 2296 — restraint frame top
    C_BOLT = "#3A3A42"
    corridor_uprights = [near_col_r, far_col_l - FRAME_RHS]

    # Full-height corridor uprights (the deep-box FRONT pair, seen edge-on in section).
    for uyd in corridor_uprights:
        ax.add_patch(Rectangle(((uyd), (0)), (FRAME_RHS), (top_z),
                               fc=C_FRAME, ec=C_OUT, lw=1.2, zorder=7, alpha=0.85))

    # Top + bottom rings tie the near & far uprights (deep-box front ring pair, seen edge-on).
    ring_y0 = near_col_r + FRAME_RHS
    ring_w  = (far_col_l - FRAME_RHS) - ring_y0
    for rz in (0, top_z - FRAME_RHS):
        ax.add_patch(Rectangle(((ring_y0), (rz)), (ring_w), (FRAME_RHS),
                               fc=C_FRAME, ec=C_OUT, lw=1.2, zorder=7, alpha=0.8))
    leader(ax, ((ring_y0 + far_col_l - FRAME_RHS) / 2), (top_z - FRAME_RHS / 2),
           (far_col_l + 170), (top_z - 430),
           "TOP + BOTTOM RINGS\n50x50x3 RHS — tie the near +\nfar uprights (back pair too)",
           color=C_FRAME, fs=6, ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # Floor flange feet under each upright.
    foot_half = IBC_FOOT_PLATE / 2
    for uyd in corridor_uprights:
        fcy = uyd + IBC_FRAME_RHS / 2
        ax.add_patch(Rectangle(((fcy - foot_half), (0)), (IBC_FOOT_PLATE),
                               (IBC_FOOT_PLATE_T), fc=C_STEEL, ec=C_OUT, lw=1.4, zorder=8))
        for d in (-IBC_FOOT_BOLT_PCD / 2, IBC_FOOT_BOLT_PCD / 2):
            ax.plot([(fcy + d), (fcy + d)], [(IBC_FOOT_PLATE_T), (-26)],
                    color=C_BOLT, lw=1.8, zorder=9)

    # Direct-stack junction line (totes bear cage-on-cage, no deck).
    for col_l, col_r in [(BLUE_IBC_Y, near_col_r), (IBC_FAR_Y, IBC_FAR_Y + IBC_D)]:
        ax.plot([(col_l), (col_r)], [(junction_z)] * 2, color=C_OUT, lw=2.2, zorder=8)

    # Front retaining bars (foreground, at the IBC front) + wall hangers + D-ring holders.
    for bz in (560, 1760):
        for y0, y1 in ((0, near_col_r + FRAME_RHS), (far_col_l - FRAME_RHS, C_WID)):
            ax.add_patch(Rectangle(((y0), (bz)), (y1 - y0), (FRAME_RHS),
                                   fc=C_STEEL, ec=C_OUT, lw=1.0, hatch="xx", zorder=9, alpha=0.6))
        for wyd, din in ((0, 1), (C_WID, -1)):
            ax.add_patch(Rectangle(((min(wyd, wyd + din * 60)), (bz - 8)), (60),
                                   (FRAME_RHS + 16), fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=10, alpha=0.9))
    for ydh in (520, C_WID - 520):
        for bz in (560, 1760):
            ax.add_patch(Circle(((ydh), (bz + FRAME_RHS / 2)), (15),
                                fc="none", ec=C_STEEL, lw=2.0, zorder=11))

    # Corridor label + restraint callouts (lighter).
    corr_cx = (near_col_r + far_col_l) / 2
    ax.text((corr_cx), (junction_z / 2), f"PLUMBING\nCORRIDOR\n{IBC_GAP}mm",
            ha="center", va="center", fontsize=6.5, color=C_CL, fontweight="bold", **FONT, zorder=15)
    leader(ax, (near_col_r + FRAME_RHS / 2), (top_z * 0.72),
           (near_col_r - 90), (top_z * 0.72 + 40),
           "DEEP-BOX FRONT UPRIGHTS\n50x50x3 RHS (x2, full height)\non flange feet (back pair 450mm behind)",
           color=C_FRAME, fs=6, ha="left", va="bottom", arrow_style="-|>", font=FONT)
    leader(ax, (near_col_r + FRAME_RHS), (1760 + FRAME_RHS / 2),
           (near_col_r - 90), (1980),
           "FRONT RETAINING BARS (x4)\nZ560 + Z1760 — slide-stop +\nD-ring lashing; wall ends drop\ninto Simpson joist hangers",
           color=C_STEEL, fs=6, ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # ── Dimension lines ───────────────────────────────────────────────────────
    # IBC height (bottom tier)
    draw_dim_v(ax, (IBC_FAR_Y + IBC_D + 80), (0), (IBC_H_1000),
               f"{IBC_H_1000}mm IBC HEIGHT", offset=(22), fs=6, right=True, font=FONT)

    # Stack total height (direct-stack, no deck)
    draw_dim_v(ax, (IBC_FAR_Y + IBC_D + 120), (0), (IBC_H_STK_1000),
               f"{IBC_H_STK_1000}mm 2x STACK", offset=(22), fs=6,
               right=True, font=FONT)

    # Ceiling clearance (tight — the critical dimension)
    draw_dim_v(ax, (IBC_FAR_Y + IBC_D + 120), (IBC_H_STK_1000), (C_HGT),
               f"{CEIL_CLEAR}mm CLEARANCE", offset=(22), fs=6,
               right=True, font=FONT)

    # Container interior width
    draw_dim_h(ax, (0), (C_WID), (-90),
               f"{C_WID}mm  INTERIOR WIDTH", offset=(5), fs=6.5, font=FONT)

    # Near column Yd position
    draw_dim_h(ax, (0), (BLUE_IBC_Y), (IBC_H_1000 + 80),
               f"{BLUE_IBC_Y}mm", offset=(5), fs=5.5, font=FONT)

    # IBC depth
    draw_dim_h(ax, (BLUE_IBC_Y), (BLUE_IBC_Y + IBC_D), (IBC_H_1000 + 80),
               f"{IBC_D}mm\nIBC DEPTH", offset=(5), fs=5.5, font=FONT)

    # Plumbing corridor between columns
    draw_dim_h(ax, (BLUE_IBC_Y + IBC_D), (IBC_FAR_Y), (IBC_H_1000 + 80),
               f"{IBC_GAP}mm\nCORRIDOR", offset=(5), fs=5.5, font=FONT)

    # ── Right walkway (ghost, for context) ────────────────────────────────────
    # The right walkway is at the IBC end, perpendicular to this view
    # Show as a note/context only
    ax.text((C_WID / 2), (C_HGT + 80),
            f"CEILING CLEARANCE: {CEIL_CLEAR}mm (transport safe \u2714)",
            ha="center", va="bottom", fontsize=7, color="#206020",
            fontweight="bold", **FONT, zorder=15)

    # ── Notes ─────────────────────────────────────────────────────────────────
    notes = [
        "CROSS-SECTION NOTES:",
        "1. Section through IBC stack, looking +X toward sealed end (near/pinhole wall at right, far wall at left).",
        f"2. 4x identical 275-gal (~1000 L) caged composite IBCs. Each: 65kg tare, {IBC_W}x{IBC_D}x{IBC_H_1000}mm. v2 layout: Brown/Waste bottom, Blue on top (clean supply, 1600 L total).",
        f"3. RESTRAINT-ONLY frame: a DEEP 4-LEG BOX (front + back upright pairs, 450mm apart, tied by top + bottom rings) on {IBC_FOOT_PLATE}x{IBC_FOOT_PLATE}x{IBC_FOOT_PLATE_T} floor flange feet",
        f"   ({IBC_FOOT_BOLT_N}x M12 each). The totes DIRECT-STACK (no deck) so no platform/wall-seat brackets are needed. ~{FRAME_WEIGHT}kg.",
        f"4. {IBC_GAP}mm plumbing corridor between columns for internal pipe routing.",
        "5. Front retaining bars (4x, Z560 + Z1760) at the IBC front stop the totes sliding out; wall ends drop into Simpson-style joist hangers.",
        f"6. D-ring lashing holders on the front bars ({DRING_WLL}kg WLL); ratchet straps over each stack tie down to them.",
        f"7. Corridor Plumbing Panel moved forward to the corridor mouth for operator access (see Sheets 3-5).",
    ]
    draw_notes(ax, notes, (C_WID), (Z_LO + 425), spacing=(22),
               fs=7, ha="left", font=FONT, width=1800)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 5",
                drawing_title="IBC STACKING & SECURING",
                subtitle="CROSS-SECTION — 2x2 DIRECT-STACK, RESTRAINT DEEP 4-LEG BOX",
                scale_note="Axes in mm - SECTION LOOKING +X (PINHOLE WALL AT RIGHT)",
                height=0.06)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "ibc-stacking-sheet1.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
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

    fig, ax = plt.subplots(figsize=(20, 22))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, (600))
    ax.set_ylim((-240), (520))
    ax.set_aspect("equal")
    ax.axis("off")

    C_BOLT = "#3A3A42"
    C_STRAP = "#C08020"

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL A — Front retaining bar -> corridor upright (bolted cleat + lash eye)
    # The bar's inner end bolts to the front corridor upright via an angle cleat;
    # a weld-on lashing eye on the bar takes the ratchet strap (Detail C).
    # ══════════════════════════════════════════════════════════════════════════
    ax.text((150), (500),
            "DETAIL A — FRONT RETAINING BAR -> CORRIDOR UPRIGHT\n(BOLTED CLEAT + WELD-ON LASH EYE)",
            ha="center", va="bottom", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # Corridor upright (vertical 50x50 RHS, partial)
    up_x, up_y = 120, 330
    ax.add_patch(Rectangle(((up_x), (up_y)), (FRAME_RHS), (150),
                            fc=C_FRAME, ec=C_OUT, lw=2.0, zorder=5))
    ax.add_patch(Rectangle(((up_x + FRAME_T), (up_y)),
                            (FRAME_RHS - 2 * FRAME_T), (150),
                            fc="#D8D8D8", ec="none", zorder=6))
    ax.text((up_x + FRAME_RHS / 2), (up_y + 130), "CORRIDOR\nUPRIGHT",
            ha="center", va="center", fontsize=5.5, color=C_OUT, **FONT, zorder=10)

    # Front retaining bar (horizontal 50x50 RHS) butting the upright
    bar_y = 380
    bar_x0 = up_x + FRAME_RHS
    bar_len = 180
    ax.add_patch(Rectangle(((bar_x0), (bar_y)), (bar_len), (FRAME_RHS),
                            fc=C_STEEL, ec=C_OUT, lw=2.0, hatch="xx", zorder=5))
    ax.text((bar_x0 + bar_len * 0.62), (bar_y + FRAME_RHS / 2),
            "FRONT RETAINING BAR\n50x20x3 RHS",
            ha="center", va="center", fontsize=5.5, color=C_OUT, **FONT, zorder=10)

    # Angle cleat joining bar to upright (L-plate) + 2 M12 bolts
    cl_t = 6
    ax.add_patch(Rectangle(((up_x + FRAME_RHS), (bar_y - cl_t)),
                            (70), (cl_t), fc=C_STEEL, ec=C_OUT, lw=1.2, zorder=7))
    ax.add_patch(Rectangle(((up_x + FRAME_RHS), (bar_y - cl_t)),
                            (cl_t), (FRAME_RHS + cl_t), fc=C_STEEL, ec=C_OUT,
                            lw=1.2, zorder=7))
    for bx in (bar_x0 + 30, bar_x0 + 60):
        ax.add_patch(Circle(((bx), (bar_y - cl_t / 2)), (5),
                            fc=C_BOLT, ec=C_OUT, lw=0.6, zorder=9))
    leader(ax, (bar_x0 + 45), (bar_y - cl_t), (bar_x0 + 30), (bar_y - 25),
           "ANGLE CLEAT +\n2x M12 BOLTS", color=C_FRAME, fs=6, ha="center",
           va="top", arrow_style="-|>", font=FONT)

    # Weld-on lashing eye on the bar (outer end)
    eye_cx, eye_cy = bar_x0 + bar_len, bar_y + FRAME_RHS / 2
    ax.add_patch(Circle(((eye_cx), (eye_cy)), (16), fc="none",
                        ec=C_STRAP, lw=4.0, zorder=9))
    ax.add_patch(Circle(((eye_cx), (eye_cy)), (7), fc=BG,
                        ec=C_STRAP, lw=2.0, zorder=10))
    leader(ax, (eye_cx + 16), (eye_cy), (eye_cx + 30), (eye_cy + 25),
           "WELD-ON LASH EYE\n1100kg WLL\n(ratchet strap, Detail C)",
           color=C_STRAP, fs=6, ha="left", va="bottom", arrow_style="-|>", font=FONT)

    ax.add_patch(Rectangle(((40), (300)), (520), (210),
                            fc="none", ec=C_DIM, lw=0.8, ls="--", zorder=1))

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL B — Wall joist hanger (Simpson-style U-pocket, face-mount to wall)
    # The bar's outer (wall) end drops into a U-pocket face-bolted to the side wall.
    # ══════════════════════════════════════════════════════════════════════════
    ax.text((150), (270),
            "DETAIL B — WALL JOIST HANGER\n(U-POCKET, THROUGH-BOLTED TO EXTERIOR BACKING PLATE)",
            ha="center", va="bottom", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # Side wall (vertical, hatched)
    wall_x = 170
    ax.add_patch(Rectangle(((wall_x - 25), (120)), (25), (130),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=4))
    ax.plot([(wall_x), (wall_x)], [(120), (250)], color=C_OUT, lw=2.0, zorder=5)
    ax.text((wall_x - 12), (135), "SIDE\nWALL", ha="center", va="center",
            fontsize=5.5, color=C_DIM, **FONT, rotation=90, zorder=10)

    hb_y = 175           # pocket seat level
    pocket_d = 90
    # Back flange (on the wall)
    ax.add_patch(Rectangle(((wall_x), (hb_y - 15)), (8), (FRAME_RHS + 30),
                            fc=C_STEEL, ec=C_OUT, lw=1.4, zorder=7))
    # Bottom seat
    ax.add_patch(Rectangle(((wall_x), (hb_y - 8)), (pocket_d), (8),
                            fc=C_STEEL, ec=C_OUT, lw=1.4, zorder=7))
    # Side strap (near, front face shown)
    ax.add_patch(Rectangle(((wall_x), (hb_y - 8)), (pocket_d), (6),
                            fc="none", ec=C_STEEL, lw=2.5, zorder=8))
    # Bar end dropped into the pocket
    ax.add_patch(Rectangle(((wall_x + 8), (hb_y)), (pocket_d - 12), (FRAME_RHS),
                            fc=C_STEEL, ec=C_OUT, lw=2.0, hatch="xx", zorder=8))
    ax.text((wall_x + pocket_d / 2 + 6), (hb_y + FRAME_RHS / 2), "BAR END",
            ha="center", va="center", fontsize=5.5, color=C_OUT, **FONT, zorder=10)
    # Exterior backing plate (load-spreading) on the OUTSIDE of the wall — the thin
    # corrugated wall would pull through under the totes' transport thrust without it.
    ext_face = wall_x - 25            # exterior wall face
    ax.add_patch(Rectangle(((ext_face - 8), (hb_y - 30)), (8), (FRAME_RHS + 60),
                            fc=C_STEEL, ec=C_OUT, lw=1.4, zorder=7))
    ax.text((ext_face - 4), (hb_y + FRAME_RHS / 2), "EXT.\nPLATE", ha="center",
            va="center", fontsize=4.3, color="white", fontweight="bold",
            **FONT, rotation=90, zorder=12)
    # M12 through-bolts: exterior plate → through wall → interior back flange (hex heads outside)
    for by in (hb_y + 6, hb_y + FRAME_RHS - 2):
        ax.plot([(ext_face - 8), (wall_x + 12)], [(by), (by)],
                color=C_BOLT, lw=1.8, zorder=10)
        ax.add_patch(Rectangle(((ext_face - 14), (by - 4)), (6), (8),
                                fc=C_BOLT, ec=C_OUT, lw=0.6, zorder=11))   # hex head outside
    leader(ax, (ext_face - 11), (hb_y - 8), (ext_face - 75), (hb_y - 55),
           "EXTERIOR BACKING PLATE\n100x135x8 + 4x M12 THROUGH-BOLTS\n(hex heads outside, load-spread)",
           color=C_FRAME, fs=6, ha="left", va="top", arrow_style="-|>", font=FONT)
    leader(ax, (wall_x + pocket_d), (hb_y - 4), (wall_x + pocket_d + 15), (hb_y - 25),
           "U-POCKET SEAT\n(bar drops in)", color=C_STEEL, fs=6, ha="left",
           va="top", arrow_style="-|>", font=FONT)

    ax.add_patch(Rectangle(((10), (100)), (560), (185),
                            fc="none", ec=C_DIM, lw=0.8, ls="--", zorder=1))

    # ══════════════════════════════════════════════════════════════════════════
    # DETAIL C — Lashing strap over the stack, ratcheted to the front bar
    # ══════════════════════════════════════════════════════════════════════════
    ax.text((300), (80),
            "DETAIL C — RATCHET LASHING (FRONT ELEVATION)\nSTRAP OVER STACK -> WELD-ON LASH EYE ON FRONT BAR",
            ha="center", va="bottom", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # Two stacked totes (front elevation, schematic)
    t_x, t_w = 200, 200
    base_z = -90
    th = 65
    for i, tcol in enumerate([C_WASTE_IBC, C_BLUE_IBC]):  # v2: brown/waste bottom, blue top
        z0 = base_z + i * th
        ax.add_patch(Rectangle(((t_x), (z0)), (t_w), (th),
                                fc=tcol, ec=C_OUT, lw=1.5, alpha=0.4, zorder=5))
    ax.text((t_x + t_w / 2), (base_z + th), "IBC STACK\n(2 totes)",
            ha="center", va="center", fontsize=6, color=C_OUT, **FONT, zorder=10)

    # Front retaining bars (small RHS squares) at the two bar heights, each side
    for bx in (t_x - 14, t_x + t_w + 14 - FRAME_RHS / 2):
        for bz in (base_z + 8, base_z + th + 8):
            ax.add_patch(Rectangle(((bx), (bz)), (FRAME_RHS / 2), (FRAME_RHS / 2),
                                    fc=C_STEEL, ec=C_OUT, lw=1.0, hatch="xx", zorder=6))

    # Lash eyes on the lower front bars
    eyeL = (t_x - 2, base_z + 8 + FRAME_RHS / 4)
    eyeR = (t_x + t_w + 2, base_z + 8 + FRAME_RHS / 4)
    for ex, ez in (eyeL, eyeR):
        ax.add_patch(Circle(((ex), (ez)), (7), fc="none", ec=C_STRAP, lw=2.5, zorder=9))

    # Ratchet strap over the top of the stack, down both sides to the eyes
    strap_x = [eyeL[0], t_x + 6, t_x + t_w - 6, eyeR[0]]
    strap_z = [eyeL[1], base_z + 2 * th + 6, base_z + 2 * th + 6, eyeR[1]]
    ax.plot(strap_x, strap_z, color=C_STRAP, lw=3.0, zorder=8, solid_capstyle="round")
    # Ratchet buckle symbol on the right run
    ax.add_patch(Rectangle(((eyeR[0] - 6), ((eyeR[1] + base_z + 2 * th) / 2)),
                            (14), (16), fc=C_STRAP, ec=C_OUT, lw=1.0, zorder=10))

    leader(ax, ((t_x + t_w / 2)), (base_z + 2 * th + 6), (t_x + t_w / 2 + 10),
           (base_z + 2 * th + 25),
           "25mm POLY RATCHET STRAP\n1100kg LC, over the stack",
           color=C_STRAP, fs=6, ha="left", va="bottom", arrow_style="-|>", font=FONT)
    leader(ax, (eyeR[0] + 1), ((eyeR[1] + base_z + 2 * th) / 2 + 8),
           (eyeR[0] + 25), (base_z + 100),
           "RATCHET BUCKLE\n-> lash eye on front bar",
           color=C_STRAP, fs=6, ha="left", va="top", arrow_style="-|>", font=FONT)

    ax.add_patch(Rectangle(((150), (-110)), (300), (210),
                            fc="none", ec=C_DIM, lw=0.8, ls="--", zorder=1))

    # ── Notes ─────────────────────────────────────────────────────────────────
    notes = [
        "FASTENING NOTES (RESTRAINT-ONLY FRAME):",
        "1. Direct-stack totes are restrained, not deck-supported. Active restraint + lash points are at the OPEN container front (side/back walls leave a 30mm gap — no hand/hook access).",
        "2. Detail A: each front retaining bar bolts to the front corridor upright via an angle cleat (2x M12); a weld-on lash eye takes the strap.",
        "3. Detail B: the bar's wall end drops into a Simpson-style U-pocket joist hanger, through-bolted (4x M12) to a 100x135x8 EXTERIOR backing plate (hex heads outside) that spreads the load into the thin corrugated wall.",
        "4. Detail C: 25mm poly ratchet straps (1100kg LC) pass over each stack and ratchet down to the front-bar lash eyes.",
        "5. Floor feet (150x150x12, 4x M12 each) anchor the corridor uprights to the slab — see Sheet 1.",
    ]
    draw_notes(ax, notes, (20), (-120), spacing=(8),
               fs=7, ha="left", font=FONT, width=560)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 5",
                drawing_title="IBC STACKING & SECURING",
                subtitle="FASTENING DETAILS — FRONT BAR - WALL HANGER - RATCHET LASHING",
                scale_note="Axes in mm - DETAILS A-C",
                height=0.06)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "ibc-stacking-sheet2.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-stacking-sheet2.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — External Bulkhead Ports Elevation
#
# View from outside the container, looking at the sealed end wall.
# Shows 3 ports stacked vertically on the container centerline:
#   Top:    Fill Blue IBC-1 (2250mm)
#           Drain Brown IBC-3 (400mm)
#   Bottom: Drain Waste IBC-4 (200mm)
# Reinforcing plate behind ports, camlock fittings, height dimensions.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet3():

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
    ax.set_xlim((YD_LO), (YD_HI))
    ax.invert_xaxis()   # match physical view orientation (see sheet header)
    ax.set_ylim((Z_LO), (Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container end wall ───────────────────────────────────────────────────
    from tbs_constants import WALL_T  # visual wall thickness
    # End wall face
    ax.add_patch(Rectangle(((0), (0)),
                            (C_WID), (C_HGT),
                            fc="#E8E8E8", ec=C_OUT, lw=2.5, zorder=2))

    # Corrugation lines (vertical ribs on container wall)
    rib_spacing = 190  # typical 20ft container rib spacing
    for rib_yd in range(rib_spacing, C_WID, rib_spacing):
        ax.plot([(rib_yd), (rib_yd)], [(0), (C_HGT)],
                color=C_WALL, lw=0.5, alpha=0.4, zorder=3)

    # Ground line
    ax.plot([(YD_LO), (YD_HI)], [(0), (0)],
            color=C_OUT, lw=1.5, zorder=4)
    ax.text((C_WID / 2), (-20), "GROUND / CONTAINER FLOOR",
            ha="center", va="top", fontsize=6, color=C_DIM, **FONT)

    # Wall labels
    ax.text((-20), (C_HGT / 2), "FAR\nWALL",
            ha="right", va="center", fontsize=6, color=C_DIM,
            fontweight="bold", **FONT, rotation=0)
    ax.text((C_WID + 20), (C_HGT / 2), "NEAR\nWALL\n(PINHOLE)",
            ha="left", va="center", fontsize=6, color=C_DIM,
            fontweight="bold", **FONT, rotation=0)
    ax.text((C_WID / 2), (C_HGT + 30),
            "SEALED END WALL — EXTERIOR VIEW",
            ha="center", va="bottom", fontsize=9, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── Centerline ───────────────────────────────────────────────────────────
    cl_yd = C_WID / 2  # = 1181mm
    ax.plot([(cl_yd), (cl_yd)], [(-80), (C_HGT + 80)],
            color=C_CL, lw=1.0, ls="--", zorder=4)
    ax.text((cl_yd), (C_HGT + 90), f"CENTERLINE\nYd={cl_yd:.0f}mm",
            ha="center", va="bottom", fontsize=6, color=C_CL,
            fontweight="bold", **FONT, zorder=15)

    # ── Ghost IBC outlines and stacking frame (behind wall) ────────────────
    # yd_ext = C_WID - yd_internal; with invert_xaxis (above) this lands the
    # near/pinhole wall at LEFT, far wall at RIGHT (correct exterior orientation)
    platform_z = IBC_H_1000                        # 1168 - direct-stack junction
    top_tier_z = platform_z   # 1072mm

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
        ax.add_patch(Rectangle(((yd_l), (z_base)),
                                (IBC_D), (IBC_H_1000),
                                fc=color, ec="none", lw=0,
                                alpha=0.12, zorder=2.5))
        # Dashed cage outline
        ax.add_patch(Rectangle(((yd_l), (z_base)),
                                (IBC_D), (IBC_H_1000),
                                fc="none", ec=color, lw=1.8, ls=(0, (6, 3)),
                                alpha=0.5, zorder=2.6))
        # Cage uprights (ghost)
        for post_yd in [yd_l + 15, yd_l + IBC_D - 15]:
            ax.add_patch(Rectangle(((post_yd - CAGE_POST_W / 2), (z_base)),
                                    (CAGE_POST_W), (IBC_H_1000),
                                    fc="none", ec=color, lw=0.5, ls=(0, (4, 3)),
                                    alpha=0.3, zorder=2.6))
        ax.text((yd_l + IBC_D / 2), (z_base + IBC_H_1000 / 2), label,
                ha="center", va="center", fontsize=6, color=color,
                alpha=0.55, fontweight="bold", **FONT, zorder=2.7)

    # Stacking frame (ghost) — deep-box BACK uprights + top/bottom rings (no platform beam;
    # the totes direct-stack). Yd mirrored for the exterior (sealed-end) view.
    fr_top_z = IBC_H_STK_1000 - 40           # 2296 (matches cp.frame)
    ghost_uyds = [C_WID - (BLUE_IBC_Y + IBC_D + FRAME_RHS),   # 1266 (mirrored)
                  C_WID - IBC_FAR_Y]                          # 1046 (mirrored)
    for uyd in ghost_uyds:
        ax.add_patch(Rectangle(((uyd), (0)),
                                (FRAME_RHS), (fr_top_z),
                                fc=C_FRAME, ec=C_FRAME, lw=1.2, ls=(0, (6, 3)),
                                alpha=0.18, zorder=2.5))
    ring_gl, ring_gr = min(ghost_uyds), max(ghost_uyds)      # 1046, 1266
    for rz in (0, fr_top_z - FRAME_RHS):
        ax.add_patch(Rectangle(((ring_gl + FRAME_RHS), (rz)),
                                (ring_gr - (ring_gl + FRAME_RHS)), (FRAME_RHS),
                                fc=C_FRAME, ec=C_FRAME, lw=1.5, ls=(0, (6, 3)),
                                alpha=0.2, zorder=2.5))

    # Ghost label
    ax.text((C_WID / 2), (IBC_H_STK_1000 + FRAME_RHS + 30),
            "GHOST OUTLINE — IBCs & STACKING FRAME (BEHIND WALL)",
            ha="center", va="bottom", fontsize=5.5, color=C_FRAME,
            fontstyle="italic", **FONT, zorder=2.8)

    # ── Reinforcing plate ────────────────────────────────────────────────────
    plate_w = 300   # plate width (mm)
    plate_h = EXT_FILL_1_H - 100 + 100  # spans from below lowest port to above highest
    plate_yd = cl_yd - plate_w / 2
    plate_z = 100   # bottom edge
    ax.add_patch(Rectangle(((plate_yd), (plate_z)),
                            (plate_w), (plate_h),
                            fc=C_STEEL, ec=C_OUT, lw=1.5, alpha=0.3,
                            hatch="...", zorder=5))
    leader(ax, (plate_yd), (plate_z + plate_h / 2),
           (plate_yd - 300), (plate_z + plate_h / 2 + 100),
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
        ax.add_patch(Circle(((cl_yd), (port_z)),
                             (camlock_r), fc="none", ec=C_OUT,
                             lw=2.0, zorder=8))
        # Port opening
        ax.add_patch(Circle(((cl_yd), (port_z)),
                             (port_r), fc=color, ec=C_OUT,
                             lw=1.5, alpha=0.5, zorder=9))
        # Port tag
        ax.text((cl_yd), (port_z), tag,
                ha="center", va="center", fontsize=7, color=C_OUT,
                fontweight="bold", **FONT, zorder=12)

        # Leader to the right
        leader_x = cl_yd + plate_w / 2 + 300
        leader(ax, (cl_yd + camlock_r + 5), (port_z),
               (leader_x), (port_z),
               f"{label}\n2\" CAMLOCK\nZ={port_z}mm",
               color=color, fs=6,
               ha="left", va="center", arrow_style="-|>", font=FONT)

    # ── Dimensions ───────────────────────────────────────────────────────────
    dim_yd = cl_yd - plate_w / 2 - 80

    # Individual port heights from ground
    for port_z, label in [(EXT_FILL_1_H, f"{EXT_FILL_1_H}mm"),
                           (EXT_DRAIN_3_H, f"{EXT_DRAIN_3_H}mm"),
                           (EXT_DRAIN_4_H, f"{EXT_DRAIN_4_H}mm")]:
        draw_dim_v(ax, (dim_yd), (0), (port_z),
                   label, offset=(5), fs=5.5, font=FONT)
        dim_yd -= 60  # stagger dimension lines

    # Container height
    draw_dim_v(ax, (C_WID + 80), (0), (C_HGT),
               f"{C_HGT}mm\nCONTAINER HEIGHT", offset=(5), fs=6,
               right=True, font=FONT)

    # Container width
    draw_dim_h(ax, (0), (C_WID), (-100),
               f"{C_WID}mm  CONTAINER WIDTH", offset=(5), fs=6.5, font=FONT)

    # Plate width
    draw_dim_h(ax, (plate_yd), (plate_yd + plate_w), (plate_z - 30),
               f"{plate_w}mm PLATE", offset=(5), fs=5.5, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        "EXTERNAL BULKHEAD PORT NOTES:",
        "1. 3x 2\" NPT bulkhead unions through sealed end wall on container centerline.",
        "2. 6mm mild steel reinforcing plate welded to wall interior before penetrations.",
        "3. Type DC camlock fittings (2\" aluminum) on exterior face — quick-connect for fill hose (X1) and drain hose (X3/X4).",
        "4. X1 fill tees to BOTH Blue totes via SIDE entries near the top (gravity-linked, ~900L each). X3/X4 drains are PUMP-driven (P-05->X3, P-03->X4).",
        "5. All penetrations sealed with neoprene gaskets — light-tight and watertight.",
        "6. Interior connections routed through plumbing corridor (see Sheet 4).",
    ]
    draw_notes(ax, notes, (YD_HI - 25), (Z_LO + 350), spacing=(18),
               fs=7, font=FONT, width=1800)

    # ── Title block ──────────────────────────────────────────────────────────
    title_block(ax, "SHEET 3 OF 5",
                drawing_title="IBC STACKING & SECURING",
                subtitle="EXTERNAL BULKHEAD PORTS — END WALL ELEVATION",
                scale_note="Axes in mm - VIEW FROM OUTSIDE",
                height=0.06)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "ibc-stacking-sheet3.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-stacking-sheet3.png saved")


# ── Shared pipe drawing helpers ───────────────────────────────────────────────

def draw_pipe_path(ax, y_pts, z_pts, od_mm, wall_mm,
                   fc="#B0B0B8", ec="#333333", bore_fc="white",
                   elbow_r=None, zorder=5):
    """Thin wrapper → tbs_drawing.draw_pipe_path (canonical body)."""
    _tbs_pipe_path(ax, y_pts, z_pts, od_mm, wall_mm, fc, ec=ec,
                   bore_fc=bore_fc, elbow_r=elbow_r, zorder=zorder)


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

    # Plan view of IBC zone + corridor
    X_LO = IBC_COL_X - 500
    X_HI = C_LEN + 1350   # extra right margin holds the legend in free space
    WALL_R = C_LEN + 250  # wall-hatch right edge — do NOT extend it with X_HI
    YD_LO = -350
    YD_HI = C_WID + 200

    fig, ax = plt.subplots(figsize=(20, 18))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim((X_LO), (X_HI))
    ax.set_ylim((YD_LO), (YD_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container walls (partial) ────────────────────────────────────────────
    WALL_T = 25
    # Near wall
    ax.add_patch(Rectangle(((X_LO), (-WALL_T)),
                            (WALL_R - X_LO), (WALL_T),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Far wall
    ax.add_patch(Rectangle(((X_LO), (C_WID)),
                            (WALL_R - X_LO), (WALL_T),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # End wall
    ax.add_patch(Rectangle(((C_LEN), (-WALL_T)),
                            (WALL_T), (C_WID + 2 * WALL_T),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))

    # Interior face lines
    ax.plot([(X_LO), (C_LEN)], [(0), (0)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([(X_LO), (C_LEN)], [(C_WID), (C_WID)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([(C_LEN), (C_LEN)], [(0), (C_WID)], color=C_OUT, lw=2.0, zorder=3)

    # Wall labels
    ax.text(((X_LO + C_LEN) / 2), (-WALL_T - 10),
            "NEAR WALL (PINHOLE, Yd=0)", ha="center", va="top",
            fontsize=6, color=C_DIM, **FONT)
    ax.text(((X_LO + C_LEN) / 2), (C_WID + WALL_T + 10),
            "FAR WALL (Yd=2362)", ha="center", va="bottom",
            fontsize=6, color=C_DIM, **FONT)
    ax.text((C_LEN + WALL_T + 10), (C_WID / 2),
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
            ax.add_patch(Rectangle(((IBC_COL_X), (yd)),
                                    (IBC_W), (IBC_D),
                                    fc=color, ec=C_OUT, lw=1.5, alpha=0.35, zorder=5))
            for frac in [0.25, 0.5, 0.75]:
                ax.plot([(IBC_COL_X + IBC_W * frac), (IBC_COL_X + IBC_W * frac)],
                        [(yd), (yd + IBC_D)],
                        color=C_OUT, lw=0.3, alpha=0.25, zorder=5)
                ax.plot([(IBC_COL_X), (IBC_COL_X + IBC_W)],
                        [(yd + IBC_D * frac), (yd + IBC_D * frac)],
                        color=C_OUT, lw=0.3, alpha=0.25, zorder=5)
            ax.text((IBC_COL_X + IBC_W / 2), (yd + IBC_D / 2), label,
                    ha="center", va="center", fontsize=7, color=C_OUT,
                    fontweight="bold", **FONT, zorder=10)
        else:
            ax.add_patch(Rectangle(((IBC_COL_X), (yd)),
                                    (IBC_W), (IBC_D),
                                    fc="none", ec=color, lw=1.0, ls="--",
                                    alpha=0.4, zorder=4))
            ax.text((IBC_COL_X + IBC_W / 2), (yd - 25), label.split("\n")[0],
                    ha="center", va="top", fontsize=5, color=color,
                    style="italic", **FONT, zorder=10)

    # ── Deep 4-leg box frame (plan): 4 uprights (front X4654 + back X5104) tied
    #    by top + bottom rings — the horizontal ring perimeter — per cp.frame(). ──
    box_front_x = cp.FRONT_X                 # 4654 — front upright pair (corridor mouth; walkway arms clamp here)
    box_back_x  = cp.BACK_X                  # 5104 — back upright pair (carries the corridor pump panel + spine)
    box_yds = [near_col_r, far_col_l - FRAME_RHS]   # 1046 / 1266 — near + far corridor edges
    # ring perimeter (top + bottom rings project together in plan): X-rails front↔back + Yd-rails near↔far
    for uyd in box_yds:                      # X-rails (front→back) along each corridor edge
        ax.add_patch(Rectangle(((box_front_x + FRAME_RHS), (uyd)),
                                (box_back_x - (box_front_x + FRAME_RHS)), (FRAME_RHS),
                                fc=C_FRAME, ec=C_OUT, lw=1.0, zorder=6, alpha=0.55))
    for ux in [box_front_x, box_back_x]:     # Yd-rails (near→far) at the front + back
        ax.add_patch(Rectangle(((ux), (near_col_r + FRAME_RHS)),
                                (FRAME_RHS), (far_col_l - FRAME_RHS) - (near_col_r + FRAME_RHS),
                                fc=C_FRAME, ec=C_OUT, lw=1.0, zorder=6, alpha=0.55))
    # 4 uprights at the box corners (front + back × near + far)
    for ux in [box_front_x, box_back_x]:
        for uyd in box_yds:
            ax.add_patch(Rectangle(((ux), (uyd)), (FRAME_RHS), (FRAME_RHS),
                                    fc=C_FRAME, ec=C_OUT, lw=1.3, zorder=7, alpha=0.9))
    leader(ax, (box_front_x + FRAME_RHS / 2), (far_col_l - FRAME_RHS),
           (box_front_x + 30), (far_col_l + 380),
           f"DEEP 4-LEG BOX FRAME\n50x50x3 RHS — 4 uprights + top/bottom rings\n(front X{box_front_x} + back X{box_back_x}, {cp.DEPTH}mm deep)",
           color=C_FRAME, fs=5.5, ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # ── D-ring lashing points (on the FRONT retaining bars, at the box front) ──
    dring_color = "#D0A030"
    for dyd in [520, near_col_r - 40, far_col_l + 40, C_WID - 520]:
        ax.add_patch(Circle(((box_front_x + FRAME_RHS / 2), (dyd)),
                             (10), fc=dring_color, ec=C_OUT,
                             lw=0.8, zorder=11))
    ax.text((box_front_x - 10), (520 - 25),
            "D-RING (TYP. 8x)", ha="right", va="top",
            fontsize=5, color=dring_color, fontweight="bold", **FONT, zorder=15)

    # ── Plumbing corridor shading ────────────────────────────────────────────
    corr_yd_lo = near_col_r
    corr_yd_hi = far_col_l
    corr_cx = (corr_yd_lo + corr_yd_hi) / 2
    ax.add_patch(Rectangle(((IBC_COL_X - 65), (corr_yd_lo)),
                            (IBC_W + 130), (corr_yd_hi - corr_yd_lo),
                            fc=C_CL, ec="none", alpha=0.08, zorder=4))
    ax.text((IBC_COL_X + IBC_W * 0.1), (corr_cx),
            f"PLUMBING CORRIDOR\n{CORRIDOR_W}mm",
            ha="center", va="center", fontsize=7, color=C_CL,
            fontweight="bold", **FONT, zorder=10)

    # Corridor centerline
    ax.plot([(IBC_COL_X - 65), (C_LEN)],
            [(corr_cx), (corr_cx)],
            color=C_CL, lw=1.0, ls="--", zorder=4)

    # ── Walkway context (ghost outline) ──────────────────────────────────────
    wk_x_l = WALKWAY_RIGHT_X
    ax.add_patch(Rectangle(((wk_x_l), (0)),
                            (WALKWAY_W), (C_WID),
                            fc="#E8F0E8", ec=C_GRATE, lw=0.8, ls="--",
                            alpha=0.2, zorder=3))
    ax.text((wk_x_l + WALKWAY_W / 2), (C_WID / 2),
            f"RIGHT WALKWAY\n(X={wk_x_l}–{wk_x_l + WALKWAY_W}mm)",
            ha="center", va="center", fontsize=5, color=C_GRATE,
            style="italic", **FONT, zorder=5, rotation=90)

    # Cargo door direction arrow
    ax.annotate("", xy=((X_LO + 20), (C_WID / 2)),
                xytext=((X_LO + 120), (C_WID / 2)),
                arrowprops=dict(arrowstyle="->", color=C_DIM, lw=1.2))
    ax.text((X_LO + 10), (C_WID / 2),
            "CARGO\nDOOR\nEND", ha="right", va="center",
            fontsize=5, color=C_DIM, **FONT)

    # ── Equipment panel (backing board + equipment depth) ────────────────
    # Panel spans ACROSS corridor (Yd direction), perpendicular to sealed end wall.
    # Panel face at X=EQPANEL_X (4874 — v2 corridor-mouth position), ply extends toward sealed end.
    # Equipment protrudes toward open end (lower X).
    ep_face_x = EQPANEL_X                      # 4874 — equipment face
    ep_back_x = ep_face_x + EQPANEL_T          # 4892 — plywood back face
    ep_yd_near = EQPANEL_YD                    # 1046
    ep_yd_far  = EQPANEL_YD + CORRIDOR_W       # 1316
    ep_depth_x = ep_face_x - 130               # deepest protrusion is now the pumps/ACC-01 (~130) — filters relocated to the Pinhole Wall panel

    # Full panel assembly footprint (backing board + equipment depth)
    ax.add_patch(Rectangle(((ep_depth_x), (ep_yd_near)),
                            (ep_back_x - ep_depth_x), (CORRIDOR_W),
                            fc=C_PLY, ec="#A09060", lw=1.5, alpha=0.3, zorder=5))

    # Plywood backing board (thin strip at back)
    ax.add_patch(Rectangle(((ep_face_x), (ep_yd_near)),
                            (EQPANEL_T), (CORRIDOR_W),
                            fc=C_PLY, ec="#A09060", lw=1.5, zorder=6))

    # Leader with panel contents
    leader(ax, (ep_face_x - BB_OD / 2), (ep_yd_near),
           (ep_face_x - 260), (ep_yd_near - 220),
           "CORRIDOR PLUMBING PANEL\n"
           "Backing Board (18mm marine ply)\n"
           "P-01/P-03/P-04/P-05 pumps (Shurflo 2088)\n"
           "ACC-01 accumulator (125 PSI); DV-02 + SV-02\n"
           "(3-stage filter bank → Pinhole Wall panel)",
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
            ax.add_patch(Rectangle(((x - fw / 2), (yd - fh / 2)),
                                    (fw), (fh),
                                    fc=color, ec=C_OUT, lw=1.5,
                                    alpha=0.4, zorder=zo))
        else:  # on vertical pipe
            ax.add_patch(Rectangle(((x - fh / 2), (yd - fw / 2)),
                                    (fh), (fw),
                                    fc=color, ec=C_OUT, lw=1.5,
                                    alpha=0.4, zorder=zo))

    def fill_drop(ax, x, yd, color, zo=10):
        """Fill pipe turning 90° straight DOWN into a tote through a round
        flange in the lid. In this plan (looking down) the vertical drop reads
        as the pipe seen end-on inside a round, bolted fill flange; the elbow is
        the corner where the horizontal Yd run meets the drop. Replaces the flat
        bar flange so a top-fill connection isn't mistaken for a pass-through."""
        flange_r = PIPE_OD * 1.6          # round fill-flange radius (~53mm)
        # 90° elbow shoulder — a short stub on the corridor side of the flange so
        # the down-turn corner is visible (pipe arrives in -/+Yd, turns down).
        elbow_dir = -1 if yd > panel_yd else 1   # corridor side of this tote
        ax.add_patch(Rectangle(((x - PIPE_HW), (yd)),
                                (PIPE_OD), (elbow_dir * flange_r * 0.9),
                                fc=color, ec="none", alpha=0.9, zorder=zo))
        # round fill flange on the tote lid (with bolt circle)
        ax.add_patch(Circle(((x), (yd)), (flange_r),
                            fc=color, ec=C_OUT, lw=1.2, alpha=0.30, zorder=zo + 1))
        bolt_holes(ax, (x), (yd), (flange_r * 0.72), 4, (3.4),
                   color=C_OUT, lw=0.6, zorder=zo + 2)
        # pipe seen end-on — the vertical drop through the flange
        draw_pipe_end(ax, (x), (yd), (PIPE_HW), (PIPE_WALL_T),
                      fc=color, ec=C_OUT, bore_fc="white", zorder=zo + 3)

    def valve_plan(ax, x, yd, orientation, color, label, zo=11):
        """Ball valve bowtie in white circle, plan view. orientation: 'h' or 'v'."""
        vs = 18
        cr = vs * 1.6  # circle radius in mm
        # White circle background
        circ = plt.Circle(((x), (yd)),
                           abs((cr) - (0)),  # radius in data coords
                           fc="white", ec=color, lw=1.5, zorder=zo)
        ax.add_patch(circ)
        if orientation == 'v':  # on a vertical (Yd-direction) pipe
            tri1 = Polygon([((x - vs), (yd - vs)),
                             ((x + vs), (yd - vs)),
                             ((x), (yd))], closed=True,
                            fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=zo + 1)
            tri2 = Polygon([((x - vs), (yd + vs)),
                             ((x + vs), (yd + vs)),
                             ((x), (yd))], closed=True,
                            fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=zo + 1)
        else:  # on a horizontal (X-direction) pipe
            tri1 = Polygon([((x - vs), (yd - vs)),
                             ((x - vs), (yd + vs)),
                             ((x), (yd))], closed=True,
                            fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=zo + 1)
            tri2 = Polygon([((x + vs), (yd - vs)),
                             ((x + vs), (yd + vs)),
                             ((x), (yd))], closed=True,
                            fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=zo + 1)
        ax.add_patch(tri1)
        ax.add_patch(tri2)
        if label:
            ax.text((x), (yd), label,
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
    draw_pipe_end(ax, (bh_x), (panel_yd),
                  (port_r), (3),
                  fc=C_PIPE_BLUE, ec=C_OUT, zorder=12)
    # Color rings for the 4 circuits (concentric, largest = topmost)
    for r_frac, color in [(0.65, C_PIPE_BLUE), (0.45, C_PIPE_BROWN),
                           (0.25, C_PIPE_BLACK)]:
        ax.add_patch(Circle(((bh_x), (panel_yd)),
                     (port_r * r_frac), fc=color, ec="none",
                     zorder=13, alpha=0.8))
    ax.text((bh_x + 40), (panel_yd + 220),
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
                   PIPE_OD, PIPE_WALL_T,
                   fc=C_PIPE_BLACK, ec="#333333", zorder=5)
    flange_plan(ax, drain_x, far_ibc_conn_yd, 'v', C_PIPE_BLACK)
    v4_yd = (far_ibc_conn_yd + panel_yd) / 2
    valve_plan(ax, drain_x, v4_yd, 'v', C_PIPE_BLACK, "V4")
    leader(ax, (drain_x), (far_ibc_conn_yd),
           (drain_x - 180), (far_ibc_conn_yd + 80),
           "X4 ← IBC-4\n(DRAIN, WASTE)\n1\" HDPE",
           fs=5.5, color=C_PIPE_BLACK, ha="right", font=FONT)
    # ── X3: IBC-3 (near, Brown) → bulkhead (above X4) ──────────────────────
    # X3 (Z=400) sits above X4 (Z=200). Covers X4 in the corridor run.
    draw_pipe_path(ax,
                   [drain_x, drain_x, bh_x],
                   [near_ibc_conn_yd, panel_yd, panel_yd],
                   PIPE_OD, PIPE_WALL_T,
                   fc=C_PIPE_BROWN, ec="#5A3020", zorder=6)
    flange_plan(ax, drain_x, near_ibc_conn_yd, 'v', C_PIPE_BROWN)
    v3_yd = (near_ibc_conn_yd + panel_yd) / 2
    valve_plan(ax, drain_x, v3_yd, 'v', C_PIPE_BROWN, "V3")
    leader(ax, (drain_x), (near_ibc_conn_yd),
           (drain_x - 20), (near_ibc_conn_yd - 80),
           "X3 ← IBC-3\n(DRAIN, BROWN)\n1\" HDPE",
           fs=5.5, color=C_PIPE_BROWN, ha="right", font=FONT)
    # ── X1: Bulkhead → fill tee → SIDE-ENTRY into BOTH Blue totes ─────────
    # Matches the 3D: a corridor tee splits the fill to IBC-1 and IBC-2 (no
    # cross-connect); each branch SIDE-ENTERS the tote's corridor face near the
    # top — NO over-the-cap drop (the 1000L direct-stack leaves ~52mm headroom),
    # penetrating 150mm past a flange.
    draw_pipe_path(ax,
                   [bh_x, fill_tee_x],
                   [panel_yd, panel_yd],
                   PIPE_OD, PIPE_WALL_T,
                   fc=C_PIPE_BLUE, ec="#1A4A90", zorder=9)
    fill_pen = 150
    for face_yd in [near_col_r, far_col_l]:
        edir = -1 if face_yd < panel_yd else 1   # penetrate into the tote, away from corridor
        branch_end = face_yd + edir * fill_pen
        draw_pipe_path(ax,
                       [fill_tee_x, fill_tee_x],
                       [panel_yd, branch_end],
                       PIPE_OD, PIPE_WALL_T,
                       fc=C_PIPE_BLUE, ec="#1A4A90", zorder=9)
        flange_plan(ax, fill_tee_x, face_yd, 'v', C_PIPE_BLUE)
    valve_plan(ax, fill_tee_x, (panel_yd + near_col_r) / 2, 'v', C_PIPE_BLUE, "V1")
    leader(ax, (fill_tee_x), (far_col_l),
           (fill_tee_x - 40), (far_col_l + 200),
           "X1 FILL TEE → IBC-1 & IBC-2 (BLUE, 1\" HDPE)\n"
           "SIDE-ENTRY at each tote's corridor face\nnear the top (150mm + flange)",
           fs=5.5, color=C_PIPE_BLUE, ha="right", font=FONT)

    # ── Legend ───────────────────────────────────────────────────────────────
    leg_x = (C_LEN + 270)        # right of the container, in the free margin
    leg_top = (C_WID - 100)
    leg_sp = (33)
    pipe_lw = 2.5

    # Legend background box
    n_leg_items = 7  # 3 pipes + elbow + valve + panel + filter
    leg_box_x = leg_x - (10)
    leg_box_top = leg_top + leg_sp * 0.5
    leg_box_bot = leg_top - n_leg_items * leg_sp + leg_sp * 0.3
    leg_box_w = (1000)
    ax.add_patch(Rectangle((leg_box_x, leg_box_bot), leg_box_w,
                            leg_box_top - leg_box_bot,
                            fc="#F0F0F0", ec=C_OUT, lw=0.6, zorder=14))

    legend_items = [
        (C_PIPE_BLUE,  "BLUE CIRCUIT — Fill side-entry near top + supply (1\" HDPE SDR-11)"),
        (C_PIPE_BROWN, "BROWN CIRCUIT — Recycle: P-04 sump → IBC-3, P-02 → filter; P-05 drain → X3 (1\" HDPE SDR-11)"),
        (C_PIPE_BLACK, "BLACK/WASTE — IBC-4 → P-03 drain pump → X4 (1\" HDPE SDR-11)"),
    ]
    ec_map = {"#2060C0": "#1A4A90", "#8D6E63": "#5A3020", "#505050": "#333333"}
    for i, (color, desc) in enumerate(legend_items):
        y = leg_top - i * leg_sp
        lx0 = leg_x / (1)  # back to mm
        ly0 = y / (1)
        draw_pipe_path(ax, [lx0, lx0 + 60], [ly0, ly0],
                        PIPE_OD * 0.6, PIPE_WALL_T,
                        fc=color, ec=ec_map.get(color, C_OUT), zorder=15)
        ax.text(leg_x + (70), y, desc,
                ha="left", va="center", fontsize=5.5, color=color,
                **FONT, zorder=15)

    # Elbow legend — draw a small sample elbow using draw_pipe_path
    y_el = leg_top - len(legend_items) * leg_sp
    el_x0 = (leg_x) / (1)        # convert back to mm for draw_pipe_path
    el_yd0 = y_el / (1)
    el_size = 20  # mm
    draw_pipe_path(ax,
                   [el_x0, el_x0 + el_size, el_x0 + el_size],
                   [el_yd0 - el_size / 2, el_yd0 - el_size / 2, el_yd0 + el_size / 2],
                   PIPE_OD * 0.6, PIPE_WALL_T,
                   fc="#A0A0A0", ec=C_OUT, zorder=15)
    ax.text(leg_x + (70), y_el,
            "90° ELBOW (Banjo LE100, 1\" HDPE NPT)",
            ha="left", va="center", fontsize=5.5, color=C_DIM,
            **FONT, zorder=15)

    # Valve legend
    y_vl = y_el - leg_sp
    valve_plan(ax, (leg_x + (30)) / (1), y_vl / (1), 'h', C_DIM, "")
    ax.text(leg_x + (70), y_vl,
            "BALL VALVE (Banjo V100FP, 1\" poly, quarter-turn)",
            ha="left", va="center", fontsize=5.5, color=C_DIM,
            **FONT, zorder=15)

    # Equipment panel legend
    y_ep = y_vl - leg_sp
    ax.add_patch(Rectangle((leg_x, y_ep - leg_sp * 0.25),
                            (60), leg_sp * 0.5,
                            fc=C_PLY, ec="#A09060", lw=1.0, zorder=15))
    ax.add_patch(Rectangle((leg_x + (10), y_ep - leg_sp * 0.15),
                            (40), leg_sp * 0.3,
                            fc=C_PUMP, ec=C_OUT, lw=0.5, alpha=0.25,
                            ls="--", zorder=15))
    ax.text(leg_x + (70), y_ep,
            "CORRIDOR PLUMBING PANEL — P-01/P-03/P-04/P-05 pumps + ACC-01 (18mm marine ply)",
            ha="left", va="center", fontsize=5.5, color="#A09060",
            **FONT, zorder=15)

    # Filter relocation note (the 3-stage filter bank is on the Pinhole Wall panel, not here)
    y_fl = y_ep - leg_sp
    ax.text(leg_x + (70), y_fl,
            "3-stage Big Blue filter bank (4.5\"×20\") → on the Pinhole Wall panel",
            ha="left", va="center", fontsize=5.5, color="#2A5A2A",
            **FONT, zorder=15)

    # ── Dimensions ───────────────────────────────────────────────────────────
    # Corridor width
    draw_dim_v(ax, (IBC_COL_X - 80), (near_col_r), (far_col_l),
               f"{CORRIDOR_W}mm\nCORRIDOR", offset=(5), fs=6, font=FONT)

    # IBC depth (near column)
    draw_dim_v(ax, (IBC_COL_X - 80), (BLUE_IBC_Y), (near_col_r),
               f"{IBC_D}mm", offset=(5), fs=5.5, font=FONT)

    # Wall clearance
    draw_dim_v(ax, (IBC_COL_X - 120), (0), (BLUE_IBC_Y),
               f"{BLUE_IBC_Y}mm", offset=(5), fs=5.5, font=FONT)

    # Far column depth
    draw_dim_v(ax, (IBC_COL_X - 80), (IBC_FAR_Y), (IBC_FAR_Y + IBC_D),
               f"{IBC_D}mm", offset=(5), fs=5.5, font=FONT)

    # IBC width (along X)
    draw_dim_h(ax, (IBC_COL_X), (IBC_COL_X + IBC_W),
               (IBC_FAR_Y + IBC_D + 120),
               f"{IBC_W}mm IBC WIDTH", offset=(5), fs=6, font=FONT)

    # Container width (wall to wall)
    draw_dim_v(ax, (C_LEN + 225), (0), (C_WID),
               f"{C_WID}mm (WALL TO WALL)", offset=(10), fs=6, right=True, font=FONT)

    # ── Notes (single block, in the right margin directly under the legend) ──
    notes = [
        "INTERNAL PLUMBING PLAN NOTES:",
        "1. 4x 275-gal (1000L) caged composite IBCs in 2x2 direct-stack",
        "  (Brown/Waste bottom, Blue top). Top tier visible; bottom",
        "  tier shown dashed.",
        "2. All internal pipe 1\" HDPE SDR-11",
        "   (2\" NPT at bulkhead unions).",
        "3. IBC valve faces point toward corridor.",
        "   DN50 butterfly valve (S60×6 thread) at each IBC.",
        "4. S60×6 to 1\" NPT adapters at each IBC (8× total).",
        "5. Ball valves (Banjo V100FP) at each IBC connection.",
        f"6. Pipes routed through {CORRIDOR_W}mm plumbing corridor,",
        "   behind the panel support frame (clear of uprights).",
        "7. X1 fill tees to BOTH Blue totes (IBC-1 & IBC-2), each branch",
        "   SIDE-ENTERING the tote's corridor face near the top (no cap drop).",
        f"8. Corridor plumbing panel (18mm marine ply) at X={EQPANEL_X}: pumps",
        "   P-01/P-03/P-04/P-05 + ACC-01 (filters on the Pinhole Wall panel).",
        f"9. Deep 4-leg box frame: 4 uprights (front X{int(cp.FRONT_X)} + back X{int(cp.BACK_X)})",
        f"   + top/bottom rings + 4 flange feet. ~{FRAME_WEIGHT}kg.",
    ]
    draw_notes(ax, notes, leg_x, leg_box_bot - (55), spacing=(18),
               fs=7, font=FONT, width=850)

    # ── Title block ──────────────────────────────────────────────────────────
    title_block(ax, "SHEET 4 OF 5",
                drawing_title="IBC STACKING & SECURING",
                subtitle="INTERNAL PLUMBING PLAN — IBC LAYOUT, PIPE ROUTING & VALVES",
                scale_note="Axes in mm - VIEW LOOKING DOWN",
                height=0.04)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "ibc-stacking-sheet4.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
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

    # ── Pipe fitting drawing helpers ─────────────────────────────────────────
    PIPE_OD = 33.4    # 1" HDPE SDR-11 outer diameter (mm)
    PIPE_WALL = 3.0   # wall thickness
    PIPE_HW = PIPE_OD / 2  # half-width for double-wall rendering

    def draw_tee_fitting(ax, yd, z, color, zo=9):
        """Draw a tee fitting symbol at a pipe junction.
        1" HDPE NPT equal tee (Banjo TEE100 or equivalent).
        """
        s = PIPE_OD * 0.7
        ax.add_patch(Rectangle(((yd - s), (z - s)),
                                (2 * s), (2 * s),
                                fc=color, ec=C_OUT, lw=1.5,
                                alpha=0.35, zorder=zo))
        ax.text((yd), (z), "T", ha="center", va="center",
                fontsize=4.5, color="white", fontweight="bold",
                **FONT, zorder=zo + 1)

    def draw_flange(ax, yd, z, orientation, color, zo=8):
        """Draw a pipe flange (thick ring) at a connection point.

        orientation: 'h' for horizontal pipe, 'v' for vertical pipe
        """
        fw = 8   # flange width
        fh = PIPE_OD + 20  # flange height (larger than pipe OD)
        if orientation == 'v':
            ax.add_patch(Rectangle(((yd - fh / 2), (z - fw / 2)),
                                    (fh), (fw),
                                    fc=color, ec=C_OUT, lw=1.5,
                                    alpha=0.4, zorder=zo))
        else:
            ax.add_patch(Rectangle(((yd - fw / 2), (z - fh / 2)),
                                    (fw), (fh),
                                    fc=color, ec=C_OUT, lw=1.5,
                                    alpha=0.4, zorder=zo))

    def pipe_stub_x(ax, yd, z, color, label, label_side="right", zo=8, offset=95):
        """Draw a pipe cross-section circle (pipe running in X, into/out of page) with its
        label on a LEADER pointing back at the circle. This sheet's x-axis is INVERTED, so
        a plain offset+ha label flowed back over the circle; route the label to the
        requested SCREEN side and let the arrow carry the association instead."""
        r_out = PIPE_OD / 2
        r_in = r_out - PIPE_WALL
        ax.add_patch(Circle(((yd), (z)), (r_out),
                             fc=color, ec=C_OUT, lw=1.8, alpha=0.3, zorder=zo))
        ax.add_patch(Circle(((yd), (z)), (r_in),
                             fc="white", ec=C_OUT, lw=0.8, alpha=0.7, zorder=zo + 1))
        # Dot at center
        ax.plot((yd), (z), 'o', color=C_OUT, ms=2, zorder=zo + 2)
        # Label on a leader. Screen-right ⟺ smaller data-yd on the inverted axis.
        if label:
            inv = ax.get_xlim()[0] > ax.get_xlim()[1]
            screen_right = (label_side == "right")
            ddir = (-1 if inv else 1) * (1 if screen_right else -1)
            leader(ax, (yd + ddir * r_out), (z),
                   (yd + ddir * offset), (z), label,
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
    ax.set_xlim((YD_LO), (YD_HI))
    ax.invert_xaxis()   # match physical view orientation (see sheet header)
    ax.set_ylim((Z_LO), (Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container shell (cross-section at end wall) ──────────────────────────
    # Floor
    ax.add_patch(Rectangle(((YD_LO), (-30)),
                            (YD_HI - YD_LO), (30),
                            fc=C_FLOOR, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Ceiling
    ax.add_patch(Rectangle(((YD_LO), (C_HGT)),
                            (YD_HI - YD_LO), (30),
                            fc=C_FLOOR, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Near wall (left)
    ax.add_patch(Rectangle(((-30), (0)),
                            (30), (C_HGT),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    # Far wall (right)
    ax.add_patch(Rectangle(((C_WID), (0)),
                            (30), (C_HGT),
                            fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=2))

    # Interior face lines
    ax.plot([(0), (0)], [(0), (C_HGT)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([(C_WID), (C_WID)], [(0), (C_HGT)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([(0), (C_WID)], [(0), (0)], color=C_OUT, lw=2.0, zorder=3)
    ax.plot([(0), (C_WID)], [(C_HGT), (C_HGT)], color=C_OUT, lw=2.0, zorder=3)

    # Wall labels
    ax.text((C_WID / 2), (-45), "CONTAINER FLOOR",
            ha="center", va="top", fontsize=6, color=C_DIM, **FONT)
    ax.text((C_WID / 2), (C_HGT + 45),
            "SEALED END WALL — INTERNAL PLUMBING ELEVATION (FROM INSIDE, LOOKING +X · NEAR/PINHOLE WALL AT RIGHT, FAR WALL AT LEFT)",
            ha="center", va="bottom", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)
    ax.text((-45), (C_HGT / 2), "NEAR\nWALL\n(Yd=0)",
            ha="center", va="center", fontsize=5.5, color=C_DIM, **FONT,
            rotation=90)
    ax.text((C_WID + 45), (C_HGT / 2), "FAR\nWALL\n(Yd=2362)",
            ha="center", va="center", fontsize=5.5, color=C_DIM, **FONT,
            rotation=90)

    # ── End wall face (background — the surface we're looking at) ────────────
    ax.add_patch(Rectangle(((0), (0)),
                            (C_WID), (C_HGT),
                            fc="#F0F0F0", ec="none", lw=0, alpha=0.3, zorder=1))

    # ── IBCs (shown in elevation, flanking the corridor) ─────────────────────
    near_col_r = BLUE_IBC_Y + IBC_D   # 1046
    far_col_l  = IBC_FAR_Y            # 1316
    platform_z = IBC_H_1000             # 1168 - direct-stack junction

    ibc_data = [
        ("IBC-3\nBROWN\n(recycled)", BLUE_IBC_Y, 0, IBC_D, IBC_H_1000, C_BROWN_IBC),
        ("IBC-1\nBLUE\n(clean supply)", BLUE_IBC_Y, platform_z,
         IBC_D, IBC_H_1000, C_BLUE_IBC),
        ("IBC-4\nWASTE", IBC_FAR_Y, 0, IBC_D, IBC_H_1000, C_WASTE_IBC),
        ("IBC-2\nBLUE\n(clean supply)", IBC_FAR_Y, platform_z,
         IBC_D, IBC_H_1000, C_BLUE_IBC),
    ]

    for label, yd, z, d, h, color in ibc_data:
        ax.add_patch(Rectangle(((yd), (z)),
                                (d), (h),
                                fc=color, ec=C_OUT, lw=1.5, alpha=0.25, zorder=4))
        # Cage uprights
        for post_yd in [yd + 15, yd + d - 15]:
            ax.add_patch(Rectangle(((post_yd - CAGE_POST_W / 2), (z)),
                                    (CAGE_POST_W), (h),
                                    fc="none", ec=C_OUT, lw=0.5, zorder=5))
        ax.text((yd + d / 2), (z + h / 2), label,
                ha="center", va="center", fontsize=6.5, color=C_OUT,
                fontweight="bold", **FONT, zorder=10)

    # ── Deep 4-leg box: corridor uprights (front pair, edge-on) tied by rings ──
    #    The totes direct-stack (no deck), so there is NO inter-tier platform beam.
    fr_top_z = IBC_H_STK_1000 - 40           # 2296 — restraint frame top (matches cp.frame)
    for uyd in [near_col_r, far_col_l - FRAME_RHS]:
        ax.add_patch(Rectangle(((uyd), (0)),
                                (FRAME_RHS), (fr_top_z),
                                fc=C_FRAME, ec=C_OUT, lw=1.0, zorder=6, alpha=0.6))
    # top + bottom rings tie the near & far uprights (front ring pair, seen edge-on)
    for rz in (0, fr_top_z - FRAME_RHS):
        ax.add_patch(Rectangle(((near_col_r + FRAME_RHS), (rz)),
                                ((far_col_l - FRAME_RHS) - (near_col_r + FRAME_RHS)), (FRAME_RHS),
                                fc=C_FRAME, ec=C_OUT, lw=1.0, zorder=6, alpha=0.55))

    # ── Corridor shading ────────────────────────────────────────────────────
    corr_l = near_col_r + FRAME_RHS
    corr_r = far_col_l - FRAME_RHS
    ax.add_patch(Rectangle(((corr_l), (0)),
                            (corr_r - corr_l), (C_HGT),
                            fc=C_CL, ec="none", alpha=0.06, zorder=3))

    # Corridor label
    corr_cx = (near_col_r + far_col_l) / 2
    ax.text((corr_cx), (C_HGT - 60),
            f"PLUMBING CORRIDOR",
            ha="center", va="top", fontsize=6, color=C_CL,
            fontweight="bold", **FONT, zorder=10)

    # ── Centerline (vertical) ───────────────────────────────────────────────
    cl_yd = C_WID / 2
    ax.plot([(cl_yd), (cl_yd)], [(-50), (C_HGT + 50)],
            color=C_CL, lw=0.8, ls="--", zorder=3)

    # ── Reinforcing plate on wall interior ───────────────────────────────────
    plate_w = 300
    plate_h = EXT_FILL_1_H - 100 + 100  # spans from below lowest port to above highest
    plate_yd = cl_yd - plate_w / 2
    plate_z = 100
    ax.add_patch(Rectangle(((plate_yd), (plate_z)),
                            (plate_w), (plate_h),
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
        ax.add_patch(Circle(((cl_yd), (port_z)),
                             (bh_outer_r), fc="#D0D0D0", ec=C_OUT,
                             lw=1.8, zorder=8))
        ax.add_patch(Circle(((cl_yd), (port_z)),
                             (port_r), fc=color, ec=C_OUT,
                             lw=1.2, alpha=0.6, zorder=9))
        # tag on a short leader off the union circle (arrow points back at it)
        leader(ax, (cl_yd), (port_z + tdir * bh_outer_r),
               (cl_yd), (port_z + tdir * (bh_outer_r + 55)), tag,
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
    top_ibc_top = platform_z + IBC_H_1000
    fill_conn_z = top_ibc_top - 80   # fill inlet near top of top-tier IBC
    drain_conn_z = 185   # IBC butterfly valve centerline ~175-200mm above floor

    near_ibc_cx = BLUE_IBC_Y + IBC_D / 2   # IBC-1/3 center Yd
    far_ibc_cx  = IBC_FAR_Y + IBC_D / 2    # IBC-2/4 center Yd

    # Side-entry inlet height — near the top of the top-tier totes.  The 1000L
    # direct-stack leaves only ~52mm headroom, so there is NO top-cap access:
    # every tote-top connection penetrates the tote's corridor-facing SIDE
    # ~150mm past a flange, near the top (Z=2156).
    side_entry_z = IBC_H_STK_1000 - 180          # 2156 — side inlet near tote top
    near_side_yd = near_col_r                      # 1046 — near-column corridor face
    far_side_yd  = far_col_l                       # 1316 — far-column corridor face
    side_pen = 150                                 # penetration past the flange

    # ── X1: Bulkhead → corridor header → SIDE-ENTRY into BOTH Blue totes ───
    # A tee at the corridor centerline (fed by the bulkhead) feeds two branches
    # that side-enter each Blue tote near the top.  No cross-connect — both Blue
    # totes fill in parallel and gravity-equalize.
    draw_pipe_path(ax, [cl_yd, cl_yd], [EXT_FILL_1_H, side_entry_z],
                   PIPE_OD, PIPE_WALL, fc=C_PIPE_BLUE, ec="#1A4A90", zorder=7)
    draw_pipe_path(ax, [cl_yd, near_side_yd - side_pen], [side_entry_z, side_entry_z],
                   PIPE_OD, PIPE_WALL, fc=C_PIPE_BLUE, ec="#1A4A90", zorder=7)
    draw_pipe_path(ax, [cl_yd, far_side_yd + side_pen], [side_entry_z, side_entry_z],
                   PIPE_OD, PIPE_WALL, fc=C_PIPE_BLUE, ec="#1A4A90", zorder=7)
    draw_tee_fitting(ax, cl_yd, side_entry_z, C_PIPE_BLUE)
    for syd, fdir in ((near_side_yd, -1), (far_side_yd, +1)):
        draw_flange(ax, syd, side_entry_z, 'v', C_PIPE_BLUE)
        ax.annotate("", xy=((syd + fdir * (side_pen - 30)), (side_entry_z)),
                    xytext=((syd + fdir * 10), (side_entry_z)),
                    arrowprops=dict(arrowstyle="-|>", color=C_PIPE_BLUE, lw=1.5))
    # V1 fill isolation on the vertical drop
    _draw_valve_elev(ax, cl_yd, (EXT_FILL_1_H + side_entry_z) / 2,
                     C_PIPE_BLUE, "V1", text_color="#000000")
    # CV1 check valve on the near branch — prevents tote backflow into the header
    _draw_check_valve_h(ax, (cl_yd + near_side_yd) / 2, side_entry_z,
                        C_PIPE_BLUE, "CV1", text_color="#000000", flow_dir="right")

    # ── X3: IBC-3 (near, bottom) → Bulkhead — BROWN drain ───────────────────
    d3_yd = near_col_r  # corridor-facing edge of near IBC
    # L-shaped path: vertical rise → 90° elbow → horizontal to bulkhead
    draw_pipe_path(ax,
                   [d3_yd, d3_yd, cl_yd + bh_outer_r + 5],
                   [drain_conn_z, EXT_DRAIN_3_H, EXT_DRAIN_3_H],
                   PIPE_OD, PIPE_WALL,
                   fc=C_PIPE_BROWN, ec="#5A3020", zorder=7)
    draw_flange(ax, d3_yd, drain_conn_z, 'v', C_PIPE_BROWN)
    # V3 on vertical run
    _draw_valve_elev(ax, d3_yd,
                     drain_conn_z + (EXT_DRAIN_3_H - drain_conn_z) * 0.45,
                     C_PIPE_BROWN, "V3")
    # No discrete check valve on X3 — the P-05 Shurflo 2088 pump has an integral
    # one-way check, so backflow into IBC-3 is already prevented (CV-3 dropped).
    # Flow arrow toward wall
    ax.annotate("", xy=((cl_yd - 5), (EXT_DRAIN_3_H)),
                xytext=((cl_yd - 70), (EXT_DRAIN_3_H)),
                arrowprops=dict(arrowstyle="-|>", color=C_PIPE_BROWN, lw=1.5))
    # P-05 brown drain pump — on X3 vertical run below elbow
    p05_z = EXT_DRAIN_3_H - 60
    _draw_pump_symbol(ax, d3_yd - 60, p05_z, C_PIPE_BROWN, "P-05")
    # Dashed connection from pump to pipe
    ax.plot([(d3_yd - PIPE_HW), (d3_yd - 60 + 22)],
            [(p05_z), (p05_z)],
            color=C_PIPE_BROWN, lw=1.5, ls="--", zorder=7)

    # ── X4: IBC-4 (far, bottom) → Bulkhead — WASTE drain ────────────────────
    # NOTE: X4 at Z=200mm limits gravity drain — P-03 waste pump evacuates
    # the residual ~120L below X4 height.
    d4_yd = far_col_l  # corridor-facing edge of far IBC
    # L-shaped path: vertical rise → 90° elbow → horizontal to bulkhead
    draw_pipe_path(ax,
                   [d4_yd, d4_yd, cl_yd - bh_outer_r - 5],
                   [drain_conn_z, EXT_DRAIN_4_H, EXT_DRAIN_4_H],
                   PIPE_OD, PIPE_WALL,
                   fc=C_PIPE_BLACK, ec="#333333", zorder=7)
    draw_flange(ax, d4_yd, drain_conn_z, 'v', C_PIPE_BLACK)
    # V4 on vertical run
    _draw_valve_elev(ax, d4_yd,
                     drain_conn_z + (EXT_DRAIN_4_H - drain_conn_z) * 0.45,
                     C_PIPE_BLACK, "V4", lside="left")
    # No discrete check valve on X4 — the P-03 Shurflo 2088 pump has an integral
    # one-way check, so backflow into IBC-4 is already prevented (CV-4 dropped).
    ax.annotate("", xy=((cl_yd + 5), (EXT_DRAIN_4_H)),
                xytext=((cl_yd + 70), (EXT_DRAIN_4_H)),
                arrowprops=dict(arrowstyle="-|>", color=C_PIPE_BLACK, lw=1.5))
    # P-03 waste evacuation pump — on X4 vertical run below elbow
    p03_z = EXT_DRAIN_4_H - 60
    _draw_pump_symbol(ax, d4_yd + 60, p03_z, C_PIPE_BLACK, "P-03")
    # Dashed connection from pump to pipe
    ax.plot([(d4_yd + PIPE_HW), (d4_yd + 60 - 22)],
            [(p03_z), (p03_z)],
            color=C_PIPE_BLACK, lw=1.5, ls="--", zorder=7)

    # ── Blue outflow manifold (X-direction, into the page) ───────────────────
    # Two isolation valves (V-B1, V-B2) — one per IBC outlet — join at tee
    # in corridor, then V-B3 after tee → single pipe to P-01 → spray bar.
    # Blue IBCs use their built-in DN50 butterfly valve (S60×6 thread) on the
    # corridor-facing face, ~185mm above the platform they sit on.
    top_tier_base = platform_z  # floor of top-tier IBCs
    blue_out_z = top_tier_base + drain_conn_z  # drain valve height on top-tier

    # IBC-1 outlet (near column) — at corridor-facing drain valve
    b1_yd = near_col_r  # valve face points toward corridor
    pipe_stub_x(ax, b1_yd, blue_out_z, C_PIPE_BLUE,
                "IBC-1\nOUTLET", label_side="right")
    # Horizontal pipe from IBC-1 toward corridor center
    draw_pipe_path(ax, [b1_yd, corr_l + 10], [blue_out_z, blue_out_z],
                   PIPE_OD, PIPE_WALL,
                   fc=C_PIPE_BLUE, ec="#1A4A90", zorder=7)
    # V-B1 on this horizontal run
    vb1_yd = (b1_yd + corr_l) / 2
    _draw_valve_elev_h(ax, vb1_yd, blue_out_z, C_PIPE_BLUE, "VB1", text_color="#000000")

    # IBC-2 outlet (far column) — at corridor-facing drain valve
    b2_yd = far_col_l  # valve face points toward corridor
    pipe_stub_x(ax, b2_yd, blue_out_z, C_PIPE_BLUE,
                "IBC-2\nOUTLET", label_side="left")
    # Horizontal pipe from IBC-2 toward corridor center
    draw_pipe_path(ax, [corr_r - 10, b2_yd], [blue_out_z, blue_out_z],
                   PIPE_OD, PIPE_WALL,
                   fc=C_PIPE_BLUE, ec="#1A4A90", zorder=7)
    # V-B2 on this horizontal run
    vb2_yd = (b2_yd + corr_r) / 2
    _draw_valve_elev_h(ax, vb2_yd, blue_out_z, C_PIPE_BLUE, "VB2", text_color="#000000")

    # Tee fitting in corridor where both outlets merge
    draw_tee_fitting(ax, corr_cx, blue_out_z, C_PIPE_BLUE)

    # V-B3 after the tee — single merged pipe continues to P-01
    vb3_z = blue_out_z - 60
    draw_pipe_path(ax, [corr_cx, corr_cx], [vb3_z, blue_out_z],
                   PIPE_OD, PIPE_WALL,
                   fc=C_PIPE_BLUE, ec="#1A4A90", zorder=7)
    _draw_valve_elev(ax, corr_cx, vb3_z + 15, C_PIPE_BLUE, "VB3", text_color="#000000")
    # Merged pipe stub (X-direction → P-01 → spray bar)
    pipe_stub_x(ax, corr_cx, vb3_z - 30, C_PIPE_BLUE,
                "P-01 → SPRAY BAR", label_side="right", offset=225)

    # ── Brown IBC-3 inlet ← tray sump (pumped via P-04 → 3W-DV-02) ───────────
    # Water collects in the sump well at the tray low point. P-04 lifts it to
    # IBC-3 via a SIDE-ENTRY near the tote top on its corridor face (no top-cap
    # access — direct-stack leaves ~52mm headroom).
    brown_in_z = IBC_H_1000 - 80  # near top of bottom-tier IBC-3
    pipe_stub_x(ax, near_col_r, brown_in_z, C_PIPE_BROWN,
                "P-04 ← TRAY SUMP\n→ IBC-3 SIDE-ENTRY", label_side="right")
    draw_flange(ax, near_col_r, brown_in_z, 'v', C_PIPE_BROWN)
    # P-04 tray drain transfer pump — on the brown inlet line
    p04_z = brown_in_z + 60
    _draw_pump_symbol(ax, near_col_r - 80, p04_z, C_PIPE_BROWN, "P-04")
    ax.plot([(near_col_r - 80 + 22), (near_col_r - PIPE_OD / 2)],
            [(brown_in_z), (brown_in_z)],
            color=C_PIPE_BROWN, lw=1.5, ls="--", zorder=7)

    # ── Brown IBC-3 outlet → P-02 pump → filter unit ────────────────────────
    # Uses IBC-3's built-in DN50 butterfly valve at corridor-facing face.
    # Offset below X3 horizontal run at Z=400 to avoid pipe crossing.
    brown_out_z = 250
    pipe_stub_x(ax, near_col_r, brown_out_z, C_PIPE_BROWN,
                "IBC-3 VALVE →\nP-02 → FILTER", label_side="right")

    # ── Filter unit return → IBC-2 (cleaned water recycled to supply) ────────
    # 3W-DV-01 routes pH-OK filtrate back to Blue IBC-2 via a SIDE-ENTRY near the
    # top (no top-cap access).
    pipe_stub_x(ax, far_col_l, side_entry_z, C_PIPE_FILTER,
                "FILTER RETURN →\nIBC-2 SIDE-ENTRY\n(recycle to Blue)", label_side="left")
    draw_flange(ax, far_col_l, side_entry_z, 'v', C_PIPE_FILTER)

    # ── Waste IBC-4 inlet ← diverter/bypass (rejected filtrate) ─────────────
    # 3W-DV-01 (pH out of range) / 3W-DV-02 route reject into IBC-4 via a
    # SIDE-ENTRY near the top (no top-cap access).
    waste_in_z = IBC_H_1000 - 80  # near top of bottom-tier IBC-4
    pipe_stub_x(ax, far_col_l, waste_in_z, C_PIPE_BLACK,
                "FILTER REJECT →\nIBC-4 SIDE-ENTRY", label_side="left")
    draw_flange(ax, far_col_l, waste_in_z, 'v', C_PIPE_BLACK)

    # ── Pipe labels for bulkhead connections ─────────────────────────────────
    leader(ax, (near_side_yd), (side_entry_z),
           (BLUE_IBC_Y + IBC_D * 0.4), (side_entry_z + 130),
           "X1 → BLUE SIDE-ENTRY\n(near top, Z=2156)\n150mm + flange · 1\" HDPE",
           color=C_PIPE_BLUE, fs=5.5,
           ha="right", va="bottom", arrow_style="-|>", font=FONT)
    leader(ax, (near_col_r), (drain_conn_z),
           (BLUE_IBC_Y + IBC_D * 0.7), (drain_conn_z - 80),
           "X3 ← IBC-3 VALVE\n(DN50, S60×6, BROWN\nBOTTOM NEAR)\n1\" HDPE",
           color=C_PIPE_BROWN, fs=5.5,
           ha="right", va="top", arrow_style="-|>", font=FONT)
    leader(ax, (far_col_l), (drain_conn_z),
           (IBC_FAR_Y + IBC_D * 0.5), (drain_conn_z - 80),
           "X4 ← IBC-4 VALVE\n(DN50, S60×6, WASTE\nBOTTOM FAR)\n1\" HDPE",
           color=C_PIPE_BLACK, fs=5.5,
           ha="left", va="top", arrow_style="-|>", font=FONT)

    # ── Legend ───────────────────────────────────────────────────────────────
    leg_x = (YD_HI - 200)
    leg_top = (-200)
    leg_spacing = (33)

    # Legend background box
    n_leg_items = 8  # 4 pipes + cross-section + elbow + tee + check valve
    # This sheet's x-axis is INVERTED, so the ha="left" legend text at leg_x+70 renders
    # screen-rightward toward SMALLER data — the box must extend that way too. Anchor it
    # just past the swatch and give it a negative width so it surrounds swatch + text.
    leg_box_x = leg_x + (75)
    leg_box_top = leg_top + leg_spacing * 0.5
    leg_box_bot = leg_top - n_leg_items * leg_spacing + leg_spacing * 0.3
    leg_box_w = -(880)
    ax.add_patch(Rectangle((leg_box_x, leg_box_bot), leg_box_w,
                            leg_box_top - leg_box_bot,
                            fc="#F0F0F0", ec=C_OUT, lw=0.6, zorder=14))

    legend_items = [
        (C_PIPE_BLUE,   "BLUE CIRCUIT — Clean supply (fill side-entry near top, VB1/VB2 → tee → VB3 → P-01 → spray bar)"),
        (C_PIPE_BROWN,  "BROWN CIRCUIT — Recycled (P-04 ← tray sump → IBC-3 side-entry, P-02 → filter unit, P-05 drain pump → X3)"),
        (C_PIPE_FILTER, "FILTER CIRCUIT — DV-01 recycle: filtered return → IBC-2 side-entry"),
        (C_PIPE_BLACK,  "BLACK/WASTE — Reject → IBC-4 side-entry; P-03 drain pump → X4"),
    ]
    ec_map6 = {"#2060C0": "#1A4A90", "#8D6E63": "#5A3020",
               "#E65100": "#B34000", "#505050": "#333333"}
    for i, (color, desc) in enumerate(legend_items):
        y = leg_top - i * leg_spacing
        lx0 = leg_x / (1)  # back to mm
        ly0 = y / (1)
        draw_pipe_path(ax, [lx0, lx0 + 60], [ly0, ly0],
                        PIPE_OD * 0.6, PIPE_WALL,
                        fc=color, ec=ec_map6.get(color, C_OUT), zorder=15)
        ax.text(leg_x + (-10), y, desc,
                ha="left", va="center", fontsize=5.5, color=color,
                **FONT, zorder=15)

    # Cross-section circle legend
    y_cs = leg_top - len(legend_items) * leg_spacing
    r_cs = PIPE_OD / 2 / ((1))  # scaled radius
    w_cs = PIPE_WALL / ((1))
    draw_pipe_end(ax, leg_x + (30), y_cs, (PIPE_OD / 2), (PIPE_WALL),
                  fc="#A0A0A0", ec=C_OUT, zorder=15)
    ax.text(leg_x + (-10), y_cs,
            "PIPE CROSS-SECTION (running in X direction, into page)",
            ha="left", va="center", fontsize=5.5, color=C_DIM,
            **FONT, zorder=15)

    # Elbow fitting legend — draw a small sample elbow
    y_el = y_cs - leg_spacing
    el_x0 = leg_x / (1)
    el_z0 = y_el / (1)
    el_size = 20
    draw_pipe_path(ax,
                   [el_x0, el_x0 + el_size, el_x0 + el_size],
                   [el_z0 - el_size / 2, el_z0 - el_size / 2, el_z0 + el_size / 2],
                   PIPE_OD * 0.6, PIPE_WALL,
                   fc="#A0A0A0", ec=C_OUT, zorder=15)
    ax.text(leg_x + (-10), y_el,
            "90° ELBOW FITTING (1\" HDPE NPT — Banjo LE100 or equiv.)",
            ha="left", va="center", fontsize=5.5, color=C_DIM,
            **FONT, zorder=15)

    # Tee fitting legend
    y_tee = y_el - leg_spacing
    s_el = PIPE_OD * 0.5  # fitting block half-size for tee symbol
    ax.add_patch(Rectangle((leg_x + (30) - (s_el), y_tee - (s_el)),
                            (2 * s_el), (2 * s_el),
                            fc="#A0A0A0", ec=C_OUT, lw=1.2, alpha=0.35, zorder=15))
    ax.text(leg_x + (30), y_tee, "T", ha="center", va="center",
            fontsize=4.5, color="white", fontweight="bold", **FONT, zorder=16)
    ax.text(leg_x + (-10), y_tee,
            "TEE FITTING (1\" HDPE NPT — Banjo TEE100 or equiv.)",
            ha="left", va="center", fontsize=5.5, color=C_DIM,
            **FONT, zorder=15)

    # Check valve legend
    y_cv = y_tee - leg_spacing
    cv_vs = 10
    tri_cv = Polygon([(leg_x + (30 - cv_vs), y_cv - (cv_vs)),
                       (leg_x + (30 - cv_vs), y_cv + (cv_vs)),
                       (leg_x + (30 + cv_vs), y_cv)], closed=True,
                      fc="#A0A0A0", ec=C_OUT, lw=1.0, alpha=0.45, zorder=15)
    ax.add_patch(tri_cv)
    ax.plot([leg_x + (30 - cv_vs), leg_x + (30 - cv_vs)],
            [y_cv - (cv_vs + 3), y_cv + (cv_vs + 3)],
            color=C_OUT, lw=1.8, zorder=16)
    ax.text(leg_x + (-10), y_cv,
            "CHECK VALVE (1\" NPT spring — CV-1 only, on the X1 gravity-fill line)",
            ha="left", va="center", fontsize=5.5, color=C_DIM,
            **FONT, zorder=15)

    # ── Dimensions ───────────────────────────────────────────────────────────
    dim_yd = cl_yd + plate_w / 2 + 100
    for port_z, label in [ (EXT_DRAIN_4_H, f"X4: {EXT_DRAIN_4_H}mm"),
                           (EXT_DRAIN_3_H, f"X3: {EXT_DRAIN_3_H}mm"),
                           (EXT_FILL_1_H, f"X1: {EXT_FILL_1_H}mm"),]:
        draw_dim_v(ax, (dim_yd), (0), (port_z),
                   label, offset=(30), fs=5.5, right=True, font=FONT)
        dim_yd += 50

    # Container interior width
    draw_dim_h(ax, (0), (C_WID), (-80),
               f"{C_WID}mm  INTERIOR WIDTH", offset=(10), above=False, fs=6, font=FONT)

    # Corridor width
    draw_dim_h(ax, (near_col_r), (far_col_l), (C_HGT - 30),
               f"{CORRIDOR_W}mm CORRIDOR", offset=(5), fs=5.5, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        "INTERNAL PLUMBING ELEVATION NOTES:",
        "1. Sealed end wall internal plumbing, from inside looking +X (near/pinhole wall at right, far wall at left). All internal pipe 1\" ",
        "   HDPE SDR-11 (2\" NPT at bulkhead unions).",
        "2. IBC valve faces point toward plumbing corridor. DN50 butterfly valve (S60×6 thread), ~185mm above floor.",
        "3. X1 fill: a corridor header tees to BOTH Blue totes; each branch SIDE-ENTERS the tote's corridor face near the top (Z=2156), penetrating",
        "   150mm past a flange. NO top-cap access — the 1000L direct-stack leaves ~52mm headroom. Filled in parallel — no cross-connect.",
        "4. S60×6 to 1\" NPT adapters (e.g. IBC-S60-1NPT) at each IBC valve connection (8× total).",
        "5. Fill header + drains run in the clear corridor behind the panel support frame (clear of the uprights), matching the 3D model.",
        "6. Blue outflow: IBC-1 valve → VB1 → tee ← VB2 ← IBC-2 valve; after tee → VB3 → P-01 → spray bar.",
        "7. Ball valves: Banjo V100FP 1\" polypropylene full-port, quarter-turn. All hand-operated.",
        "8. Drains are PUMPED: P-05 (Brown) → X3 (Z=400mm), P-03 (Waste) → X4 (Z=200mm) — gravity head is insufficient at these port heights.",
        "9. 90° elbows (Banjo LE100) at all bends. Flanges at all bulkhead and IBC connections.",
        "10. Check valve CV-1 only (1\" NPT spring check) on the X1 gravity-fill line. The X3/X4 drains are pump-driven (P-05/P-03); the Shurflo",
        "    2088 pumps have integral one-way checks, so no discrete CV is fitted there (CV-3/CV-4 dropped).",
        "11. RECYCLE: P-04 draws from the tray sump and feeds IBC-3 (Brown) via a SIDE-ENTRY near the top (3W-DV-02 selects IBC-3 or IBC-4). Brown",
        "    is then pumped (P-02) through the 3-stage filter; 3W-DV-01 recycles pH-OK filtrate to IBC-2 (Blue) via side-entry, else to IBC-4.",
        "12. ALL tote-top connections are SIDE-ENTRY near the top (fill, recycle return, reject, sump) — no top-cap access anywhere (52mm headroom).",
    ]
    draw_notes(ax, notes, (YD_LO + 1530), (-180), spacing=(22),
               fs=7, font=FONT, width=1500)

    # ── Title block ──────────────────────────────────────────────────────────
    title_block(ax, "SHEET 5 OF 5",
                drawing_title="IBC STACKING & SECURING",
                subtitle="INTERNAL PLUMBING ELEVATION — ALL WATER SYSTEM CONNECTIONS",
                scale_note="Axes in mm - VIEW FROM INSIDE",
                height=0.04)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "ibc-stacking-sheet5.png"), dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-stacking-sheet5.png saved")


def _draw_valve_elev(ax, yd, z, color, label, lside="right", text_color=None):
    """Draw a ball valve symbol (bowtie in white circle) in elevation view at (yd, z).
    On a VERTICAL pipe — so the label is leadered out to the SIDE (lside), not buried in
    the symbol. text_color overrides the label colour (default = the pipe colour, which is
    readable on the light background; pass e.g. 'white' if the label sits on a dark fill)."""
    vs = 18  # half-size in mm
    cr = vs * 1.6  # circle radius in mm
    # White circle background
    circ = plt.Circle(((yd), (z)),
                       abs((cr) - (0)),  # radius in data coords
                       fc="white", ec=color, lw=1.5, zorder=11)
    ax.add_patch(circ)
    # Bowtie oriented horizontally (left/right triangles meeting at center)
    tri1 = Polygon([((yd - vs), (z - vs)),
                     ((yd - vs), (z + vs)),
                     ((yd), (z))], closed=True,
                    fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=12)
    tri2 = Polygon([((yd + vs), (z - vs)),
                     ((yd + vs), (z + vs)),
                     ((yd), (z))], closed=True,
                    fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=12)
    ax.add_patch(tri1)
    ax.add_patch(tri2)
    if label:
        # leader the label out to the side (inversion-aware), not white-on-symbol
        inv = ax.get_xlim()[0] > ax.get_xlim()[1]
        screen_right = (lside == "right")
        ddir = (-1 if inv else 1) * (1 if screen_right else -1)
        leader(ax, (yd + ddir * cr), (z),
               (yd + ddir * (cr + 48)), (z), label,
               fs=5, color=text_color or color,
               ha="left" if screen_right else "right",
               va="center", font=FONT)


def _draw_valve_elev_h(ax, yd, z, color, label, lup=True, text_color=None):
    """Draw a ball valve symbol (bowtie in white circle) on a HORIZONTAL pipe in elevation.
    Bowtie axis perpendicular to flow — oriented vertically. The label is leadered ABOVE
    (lup) or below the symbol instead of being buried white inside it. text_color overrides
    the label colour (default = the pipe colour)."""
    vs = 18  # half-size in mm
    cr = vs * 1.6  # circle radius in mm
    # White circle background
    circ = plt.Circle(((yd), (z)),
                       abs((cr) - (0)),  # radius in data coords
                       fc="white", ec=color, lw=1.5, zorder=11)
    ax.add_patch(circ)
    # Top triangle (pointing down)
    tri1 = Polygon([((yd - vs), (z + vs)),
                     ((yd + vs), (z + vs)),
                     ((yd), (z))], closed=True,
                    fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=12)
    # Bottom triangle (pointing up)
    tri2 = Polygon([((yd - vs), (z - vs)),
                     ((yd + vs), (z - vs)),
                     ((yd), (z))], closed=True,
                    fc=color, ec=C_OUT, lw=1.0, alpha=0.5, zorder=12)
    ax.add_patch(tri1)
    ax.add_patch(tri2)
    if label:
        # leader the label above/below the symbol, not white-on-symbol
        zdir = 1 if lup else -1
        leader(ax, (yd), (z + zdir * cr),
               (yd), (z + zdir * (cr + 42)), label,
               fs=5, color=text_color or color, ha="center",
               va="bottom" if lup else "top", font=FONT)


def _draw_check_valve_h(ax, yd, z, color, label, text_color=None, flow_dir="right"):
    """Draw a check valve (non-return valve) on a HORIZONTAL pipe.

    Triangle pointing in flow direction with a perpendicular bar at the
    upstream end (the seat).  flow_dir: 'left' or 'right'.
    """
    vs = 16  # half-size in mm
    if flow_dir == "right":
        # Triangle pointing right  →
        tri = Polygon([((yd - vs), (z - vs)),
                        ((yd - vs), (z + vs)),
                        ((yd + vs), (z))], closed=True,
                       fc=color, ec=C_OUT, lw=1.0, alpha=0.45, zorder=11)
        # Bar at upstream (left) end
        ax.plot([(yd - vs), (yd - vs)], [(z - vs - 4), (z + vs + 4)],
                color=C_OUT, lw=2.0, zorder=12)
    else:
        # Triangle pointing left  ←
        tri = Polygon([((yd + vs), (z - vs)),
                        ((yd + vs), (z + vs)),
                        ((yd - vs), (z))], closed=True,
                       fc=color, ec=C_OUT, lw=1.0, alpha=0.45, zorder=11)
        # Bar at upstream (right) end
        ax.plot([(yd + vs), (yd + vs)], [(z - vs - 4), (z + vs + 4)],
                color=C_OUT, lw=2.0, zorder=12)
    ax.add_patch(tri)
    if label:
        ax.text((yd), (z + vs + 14), label,
                ha="center", va="bottom", fontsize=4.5,
                color=color if text_color == None else text_color,
                fontweight="bold", **FONT, zorder=13)


def _draw_pump_symbol(ax, yd, z, color, label):
    """Draw a pump symbol (circle with arrow) in elevation view."""
    r = 22
    ax.add_patch(Circle(((yd), (z)), (r),
                         fc=color, ec=C_OUT, lw=1.8, alpha=0.3, zorder=11))
    # Triangle inside (flow direction indicator)
    ts = 12
    tri = Polygon([((yd - ts), (z - ts)),
                    ((yd - ts), (z + ts)),
                    ((yd + ts), (z))], closed=True,
                   fc=color, ec=C_OUT, lw=1.0, alpha=0.6, zorder=12)
    ax.add_patch(tri)
    if label:
        ax.text((yd), (z + r + 12), label,
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
    sheet3()  # external bulkhead ports -> ibc-stacking-sheet3.png
    sheet4()  # internal plumbing plan -> ibc-stacking-sheet4.png
    sheet5()  # internal plumbing elevation -> ibc-stacking-sheet5.png
    print("Done.")
