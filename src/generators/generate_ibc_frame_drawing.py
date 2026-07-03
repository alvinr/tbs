#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_ibc_frame_drawing.py  —  TBS-001 IBC Support Frame Fabrication Drawings

Three-sheet fabrication drawing set for the welded 50×50×3mm RHS mild steel
IBC stacking frame.  Shows frame structure only — no IBCs, plumbing, or
other container equipment.

Sheet 1 — Front Elevation (looking +X toward sealed end; near/pinhole wall at right, far wall at left)
Sheet 2 — Side Elevation (looking along Yd from near wall)
Sheet 3 — Plan View (looking down at platform level)

Each sheet includes dimensional callouts and assembly detail insets.

Frame concept (ibc-reconfig-v2 — restraint-only deep 4-leg box):
  The 1000L caged totes DIRECT-STACK cage-on-cage (52mm headroom, no load-bearing
  deck), so the frame only RESTRAINS.  It is a DEEP 4-LEG BOX at the corridor mouth:
  a FRONT upright pair (X4654) + a BACK pair 450mm behind (X5104), each column at
  Yd 1046/1266, tied by butt-jointed top + bottom rings.  Each of the 4 legs is
  anchored to the floor by a 150×150×12 flange plate with 4× M12 bolts; the front
  feet reach ~25mm under the tray edge.  The box carries the Corridor pump panel +
  drain-riser spine on its BACK uprights.  Transport restraint is by front retaining
  bars (Z560 + Z1760) whose wall ends drop into Simpson-style joist hangers through-
  bolted to exterior backing plates, plus D-ring lashing.  Geometry matches the 3D
  cp.frame() (generate_corridor_water_panel.py).

  rev 12: the right walkway's 2 support arms cantilever off the corridor uprights
  (at Yd 1046/1266) and project off the FRONT of the frame toward the walkway —
  drawn here (Sheets 2 + 3) as the walkway-support brackets that attach to this
  frame.  Geometry single-sourced with the 3D models via the RWK_* constants
  (ibc_cantilever_arms() in generate_sketchup_model.py).
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch, Circle
import matplotlib.patches as mpatches

from tbs_constants import (
    C_LEN, C_WID, C_HGT,
    IBC_COL_X, IBC_W, IBC_D, IBC_H_1000, IBC_H_STK_1000,
    BLUE_IBC_Y, IBC_FAR_Y,
    IBC_PALLET_H, IBC_CAGE_TUBE_D, IBC_CAGE_RAIL_W,
    IBC_CAGE_INSET, IBC_BOTTLE_INSET, IBC_VALVE_Z,
    IBC_FOOT_PLATE, IBC_FOOT_PLATE_T, IBC_FOOT_BOLT_D,
    IBC_FOOT_BOLT_PCD, IBC_FOOT_BOLT_N,
    IBC_WBKT_PLATE_W, IBC_WBKT_PLATE_T, IBC_WBKT_SEAT_PROJ,
    IBC_WBKT_SEAT_T, IBC_WBKT_GUSSET_H, IBC_WBKT_BOLT_D, IBC_WBKT_BOLT_N,
    PANEL_FRAME_TOP_Z,
    WALKWAY_RIGHT_X, WALKWAY_H, WALKWAY_GRATE_T,
    CORRIDOR_YD_NEAR, CORRIDOR_YD_FAR, IBC_FRAME_RHS,
    DIAGRAMS_DIR,
)
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader, hatch_rect, draw_notes

# ── Palette ──────────────────────────────────────────────────────────────────
BG       = "#FFFFFF"
C_OUT    = "#1A1A1A"       # outlines
C_CL     = "#2060A0"       # center lines (blue, dashed)
C_DIM    = "#404040"       # dimensions
C_STEEL  = "#B0B0B8"       # steel section fill
C_FRAME  = "#606068"       # frame RHS steel (darker)
C_WELD   = "#C04040"       # weld symbols
C_DETAIL = "#E8E0D8"       # detail inset background
FONT     = {"fontfamily": "monospace"}

# ── Frame constants ──────────────────────────────────────────────────────────
FRAME_RHS  = 50            # section size: 50×50×3mm RHS
FRAME_T    = 3             # RHS wall thickness
FRAME_FOOTPRINT_W = C_WID  # 2362mm wall-to-wall
FRAME_FOOTPRINT_D = 450    # depth along X — deep 4-leg box (cp.frame DEPTH: front X4654 → back X5104)
MAT_T      = 12            # anti-slip rubber mat thickness

# Derived positions (Yd, container coordinates)
NEAR_COL_R = BLUE_IBC_Y + IBC_D       # 1046 — near corridor edge
FAR_COL_L  = IBC_FAR_Y                # 1316 — far corridor edge
CORRIDOR_W = FAR_COL_L - NEAR_COL_R   # 270mm

# Corridor post Yd positions (inner faces, where IBC column meets corridor)
POST_NEAR_YD = NEAR_COL_R             # 1046
POST_FAR_YD  = FAR_COL_L - FRAME_RHS  # 1266

# Heights (ibc-reconfig-v2: 1000L direct-stack, restraint-only frame)
PLATFORM_Z = IBC_H_1000                # 1168 — direct-stack junction (cage-on-cage, no deck)
STACK_Z    = IBC_H_STK_1000            # 2336 — stack top
TOP_Z      = IBC_H_STK_1000 - 40       # 2296 — restraint frame top

# Frame X positions (frame-local, 0 = front/IBC-corridor mouth). Deep 4-leg box: a
# FRONT pair (X4654) + a BACK pair 450mm behind (X5104), tied by top + bottom rings.
FX_FRONT = 0
FX_BACK  = FRAME_FOOTPRINT_D          # 450 — back upright pair
FX_MID   = FRAME_FOOTPRINT_D // 2     # legacy alias (unused)
FX_POSTS = [FX_FRONT, FX_BACK]        # front + back upright stations

# Anti-rotation lip
LIP_H = 40    # height above platform
LIP_T = 5     # thickness (steel plate)

# D-ring lashing
DRING_SIZE     = 25
DRING_STANDOFF = 30
DRING_WLL      = 1100

# Access gate
GATE_H      = 300
GATE_BOLT_D = 12
GATE_BOLT_N = 4

# Wall seat bracket (welded: back-plate + seat + triangular gusset web).
# Dimensions are shared with the 3D model via tbs_constants.
BRACKET_L      = IBC_WBKT_SEAT_PROJ   # seat projection into container along Yd (110mm)
BRACKET_T      = IBC_WBKT_PLATE_T     # plate/gusset thickness (8mm)
BRACKET_SEAT_T = IBC_WBKT_SEAT_T      # seat plate thickness (10mm)
BRACKET_GUSSET_H = IBC_WBKT_GUSSET_H  # gusset web depth (200mm)
BRACKET_PLATE_W  = IBC_WBKT_PLATE_W   # back-plate width along X (150mm)
BRACKET_BOLT_D = IBC_WBKT_BOLT_D      # M12 wall anchor bolts
BRACKET_BOLT_N = IBC_WBKT_BOLT_N      # 4 per bracket

# ── Right-walkway cantilever arm (rev12) ──────────────────────────────────────
# The right walkway is carried by 2 arms that cantilever off the corridor uprights
# (at Yd = POST_NEAR_YD / POST_FAR_YD) and reach inward to the walkway long beams.
# Drawn here as the walkway-support brackets that ATTACH TO this frame.
FRAME_X0_GLOBAL = IBC_COL_X - 65          # frame-local X=0 maps to this global X (4609)
ARM_X_UP_L  = (IBC_COL_X + 60) - FRAME_X0_GLOBAL   # arm root at the upright (frame-local X ≈ 125)
ARM_X_TIP_L = WALKWAY_RIGHT_X - FRAME_X0_GLOBAL    # arm tip reaches the walkway left beam (≈ -280)
ARM_Z0      = 70                                   # arm bottom Z
ARM_Z1      = WALKWAY_H - WALKWAY_GRATE_T           # arm top Z (= grate bottom, 115)
ARM_W       = 40                                   # 40×40×3 SHS
ARM_YDS     = (CORRIDOR_YD_NEAR, CORRIDOR_YD_FAR - IBC_FRAME_RHS)  # 1046, 1266 (= POST_NEAR/FAR_YD)
C_ARM       = "#9098A0"                            # walkway-steel (distinct from frame)

# Floor flange foot (under each corridor upright)
FOOT_PLATE   = IBC_FOOT_PLATE     # 150mm square
FOOT_PLATE_T = IBC_FOOT_PLATE_T   # 12mm thick
FOOT_BOLT_D  = IBC_FOOT_BOLT_D    # M12
FOOT_BOLT_PCD = IBC_FOOT_BOLT_PCD # 100mm square pitch
FOOT_BOLT_N  = IBC_FOOT_BOLT_N    # 4 per foot

# ── IBC anatomy derived heights ─────────────────────────────────────────────
# (base constants imported from tbs_constants.py)
IBC_BOTTLE_TOP = IBC_H_1000 - IBC_CAGE_RAIL_W    # bottle top (~985mm)
IBC_BOTTLE_BASE = IBC_PALLET_H                   # bottle starts at pallet top

# Ghost IBC colors
C_PALLET  = "#8B7355"    # pallet base (wood/steel brown)
C_BOTTLE  = "#B8D4E8"    # HDPE bottle (translucent blue)
C_CAGE    = "#707070"    # galvanized cage wire


# ═══════════════════════════════════════════════════════════════════════════════
# Helper — draw a filled RHS cross-section (cut view)
# ═══════════════════════════════════════════════════════════════════════════════
def _rhs_rect(ax, x, y, w, h, *, fc=C_FRAME, lw=1.5, zo=5,
              alpha=0.7, hatch=None):
    """Draw a filled rectangle representing an RHS member in elevation."""
    ax.add_patch(Rectangle(((x), (y)), (w), (h),
                            fc=fc, ec=C_OUT, lw=lw, zorder=zo,
                            alpha=alpha, hatch=hatch))


def _weld_tick(ax, x, y, *, side='right', size=8, zo=10):
    """Draw a small fillet weld symbol (V-tick) at a joint."""
    s = size
    if side == 'right':
        ax.plot([(x), (x + s)], [(y), (y + s)], color=C_WELD,
                lw=1.5, zorder=zo)
        ax.plot([(x), (x + s)], [(y), (y - s)], color=C_WELD,
                lw=1.5, zorder=zo)
    elif side == 'left':
        ax.plot([(x), (x - s)], [(y), (y + s)], color=C_WELD,
                lw=1.5, zorder=zo)
        ax.plot([(x), (x - s)], [(y), (y - s)], color=C_WELD,
                lw=1.5, zorder=zo)
    elif side == 'up':
        ax.plot([(x), (x + s)], [(y), (y + s)], color=C_WELD,
                lw=1.5, zorder=zo)
        ax.plot([(x), (x - s)], [(y), (y + s)], color=C_WELD,
                lw=1.5, zorder=zo)
    elif side == 'down':
        ax.plot([(x), (x + s)], [(y), (y - s)], color=C_WELD,
                lw=1.5, zorder=zo)
        ax.plot([(x), (x - s)], [(y), (y - s)], color=C_WELD,
                lw=1.5, zorder=zo)


# ═══════════════════════════════════════════════════════════════════════════════
# Floor flange foot helpers (anchor each corridor upright to the container floor)
# ═══════════════════════════════════════════════════════════════════════════════
def _foot_elev(ax, c, *, zo=7):
    """Floor flange foot in elevation (edge-on): a wide thin plate just below
    Z=0 plus two anchor-bolt stubs.  `c` = horizontal position (Yd or X)."""
    half = FOOT_PLATE / 2
    _rhs_rect(ax, c - half, -FOOT_PLATE_T, FOOT_PLATE, FOOT_PLATE_T, 
              fc=C_STEEL, lw=1.4, zo=zo)
    for d in (-FOOT_BOLT_PCD / 2, FOOT_BOLT_PCD / 2):
        ax.plot([(c + d), (c + d)],
                [(-FOOT_PLATE_T), (-FOOT_PLATE_T - 28)],
                color=C_OUT, lw=1.8, zorder=zo + 1)
        ax.plot((c + d), (-FOOT_PLATE_T - 28), 'v', color=C_OUT,
                ms=4, mew=0, zorder=zo + 1)


def _foot_plan(ax, cx, cyd, *, zo=7):
    """Floor flange foot in plan (face-on 150×150 square + 4 anchor bolts)."""
    half = FOOT_PLATE / 2
    ax.add_patch(Rectangle(((cx - half), (cyd - half)),
                            (FOOT_PLATE), (FOOT_PLATE),
                            fc=C_STEEL, ec=C_OUT, lw=1.2, alpha=0.5, zorder=zo))
    for dx in (-FOOT_BOLT_PCD / 2, FOOT_BOLT_PCD / 2):
        for dy in (-FOOT_BOLT_PCD / 2, FOOT_BOLT_PCD / 2):
            ax.plot((cx + dx), (cyd + dy), 'o', color=C_OUT, ms=4,
                    mfc='white', mew=1.2, zorder=zo + 1)


# ═══════════════════════════════════════════════════════════════════════════════
# Ghost IBC helpers — show cage/pallet anatomy as context for frame interface
# ═══════════════════════════════════════════════════════════════════════════════
def _ghost_ibc_elev(ax, yd, z_base, width, *, label="", zo=2.5):
    """Draw a ghost IBC in elevation view showing pallet, bottle, cage anatomy.

    yd      — left edge Yd position
    z_base  — bottom of pallet (Z=0 for bottom tier, Z=platform for top tier)
    width   — IBC width in this view direction (IBC_D for front, IBC_W for side)
    """
    # Pallet base
    ax.add_patch(Rectangle(((yd), (z_base)),
                            (width), (IBC_PALLET_H),
                            fc=C_PALLET, ec=C_CAGE, lw=0.8, alpha=0.15,
                            zorder=zo))
    # Fork pocket slots (2 openings on each side)
    fork_w = width * 0.25
    for fx_off in [width * 0.15, width * 0.60]:
        ax.add_patch(Rectangle(((yd + fx_off), (z_base + 20)),
                                (fork_w), (IBC_PALLET_H - 40),
                                fc=BG, ec=C_CAGE, lw=0.4, alpha=0.3,
                                zorder=zo + 0.1))

    # HDPE bottle (inner container)
    bottle_z = z_base + IBC_BOTTLE_BASE
    bottle_top = z_base + IBC_BOTTLE_TOP
    bottle_h = bottle_top - bottle_z
    bi = IBC_BOTTLE_INSET
    ax.add_patch(Rectangle(((yd + bi), (bottle_z)),
                            (width - 2 * bi), (bottle_h),
                            fc=C_BOTTLE, ec=C_CAGE, lw=0.5, alpha=0.12,
                            zorder=zo + 0.2))

    # Cage top rail
    rail_z = z_base + IBC_BOTTLE_TOP
    ax.add_patch(Rectangle(((yd), (rail_z)),
                            (width), (IBC_CAGE_RAIL_W),
                            fc=C_CAGE, ec=C_CAGE, lw=0.8, alpha=0.2,
                            zorder=zo + 0.3))

    # Cage corner tubes (shown as vertical strips at edges)
    ci = IBC_CAGE_INSET
    for tube_yd in [yd + ci, yd + width - ci]:
        ax.add_patch(Rectangle(((tube_yd - IBC_CAGE_TUBE_D / 2),
                                 (z_base + IBC_PALLET_H - 28)),
                                (IBC_CAGE_TUBE_D),
                                (IBC_H_1000 - IBC_PALLET_H + 28),
                                fc=C_CAGE, ec=C_CAGE, lw=0.6, alpha=0.15,
                                zorder=zo + 0.3))

    # Cage horizontal mid-rail (wire mesh represented by a single mid line)
    mid_z = z_base + IBC_PALLET_H + (IBC_H_1000 - IBC_PALLET_H) / 2
    ax.plot([(yd + ci), (yd + width - ci)],
            [(mid_z), (mid_z)],
            color=C_CAGE, lw=0.5, alpha=0.25, zorder=zo + 0.2)

    # Drain valve position (corridor-facing side — on the right edge for near
    # column, left edge for far column; caller can adjust)
    valve_z = z_base + IBC_VALVE_Z
    # Small circle representing valve
    ax.add_patch(Circle(((yd + width - IBC_CAGE_INSET), (valve_z)),
                         (15), fc=C_CAGE, ec=C_CAGE, lw=0.8,
                         alpha=0.25, zorder=zo + 0.4))

    # Label
    if label:
        ax.text((yd + width / 2), (z_base + IBC_H_1000 / 2), label,
                ha="center", va="center", fontsize=5.5, color=C_CAGE,
                alpha=0.5, **FONT, zorder=zo + 0.5)


def _ghost_ibc_elev_far(ax, yd, z_base, width, *, label="", zo=2.5):
    """Ghost IBC for far column — drain valve on LEFT (corridor) side."""
    _ghost_ibc_elev(ax, yd, z_base, width, label=label, zo=zo)
    # Override valve position to left side
    valve_z = z_base + IBC_VALVE_Z
    # Remove the default right-side valve by drawing over it, then draw on left
    ax.add_patch(Circle(((yd + IBC_CAGE_INSET), (valve_z)),
                         (15), fc=C_CAGE, ec=C_CAGE, lw=0.8,
                         alpha=0.25, zorder=zo + 0.4))


def _ghost_ibc_plan(ax, x, yd, w, d, *, label="", zo=2.5):
    """Draw a ghost IBC in plan view showing pallet footprint, cage tubes,
    and bottle outline.

    x, yd — bottom-left corner in plan coordinates
    w     — width along X axis
    d     — depth along Yd axis
    """
    # Pallet footprint
    ax.add_patch(Rectangle(((x), (yd)), (w), (d),
                            fc=C_PALLET, ec=C_CAGE, lw=0.8, alpha=0.08,
                            zorder=zo))

    # Bottle outline (inset from pallet)
    bi = IBC_BOTTLE_INSET
    ax.add_patch(Rectangle(((x + bi), (yd + bi)),
                            (w - 2 * bi), (d - 2 * bi),
                            fc=C_BOTTLE, ec=C_CAGE, lw=0.5, alpha=0.08,
                            zorder=zo + 0.2))

    # Cage corner tubes (4 circles at corners)
    ci = IBC_CAGE_INSET
    r = IBC_CAGE_TUBE_D / 2
    for cx, cy in [(x + ci, yd + ci),
                   (x + w - ci, yd + ci),
                   (x + ci, yd + d - ci),
                   (x + w - ci, yd + d - ci)]:
        ax.add_patch(Circle(((cx), (cy)), (r),
                             fc=C_CAGE, ec=C_CAGE, lw=0.6,
                             alpha=0.25, zorder=zo + 0.3))

    # Pallet runner lines (2 runners along X, typical for US format)
    for runner_yd in [yd + d * 0.25, yd + d * 0.75]:
        ax.plot([(x + 20), (x + w - 20)],
                [(runner_yd), (runner_yd)],
                color=C_PALLET, lw=1.5, alpha=0.2, zorder=zo + 0.1)

    if label:
        ax.text((x + w / 2), (yd + d / 2), label,
                ha="center", va="center", fontsize=5.5, color=C_CAGE,
                alpha=0.5, **FONT, zorder=zo + 0.5)


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — Front Elevation
#
# Looking along X toward the sealed end wall.  Shows full container width
# (Yd axis horizontal, Z axis vertical).  Frame members and ghost IBC
# outlines showing cage/pallet anatomy.
#
# Visible members:
#   - 2 corridor uprights (front bay, cut section)
#   - 3 transverse beams per level (near col, corridor, far col)
#   - Wall brackets at near and far walls
#   - Anti-rotation lip on platform
#   - D-ring lashing points
#   - Access gates on corridor face
#   - Ghost IBC outlines showing pallet/cage/bottle interface
#   - Behind: mid and back bay uprights shown dashed
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():
    """Sheet 1 — Front elevation of IBC support frame."""

    YD_LO = -300
    YD_HI = FRAME_FOOTPRINT_W + 300
    Z_LO  = -400
    Z_HI  = TOP_Z + 700

    fig, ax = plt.subplots(figsize=(20, 22))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim((YD_LO), (YD_HI))
    ax.invert_xaxis()   # looking +X toward sealed end -> near/pinhole wall at right
    ax.set_ylim((Z_LO), (Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Title ────────────────────────────────────────────────────────────────
    ax.text((FRAME_FOOTPRINT_W * 0.5), (TOP_Z + 680),
            "FRONT ELEVATION — LOOKING +X TOWARD SEALED END (NEAR/PINHOLE WALL AT RIGHT, FAR WALL AT LEFT)",
            ha="center", va="bottom", fontsize=9, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── Ghost IBC outlines (cage/pallet anatomy) — v2 layout: Brown/Waste bottom,
    #    Blue on top; DIRECT-STACK so the top tier sits at the junction (no deck). ──
    plat_top = PLATFORM_Z                       # 1168 — top tier bears directly on the lower tote
    _ghost_ibc_elev(ax, BLUE_IBC_Y, 0, IBC_D, 
                    label="IBC-3\n(BROWN, BOT NEAR)")
    _ghost_ibc_elev_far(ax, IBC_FAR_Y, 0, IBC_D, 
                        label="IBC-4\n(WASTE, BOT FAR)")
    # Top tier (direct-stack)
    _ghost_ibc_elev(ax, BLUE_IBC_Y, plat_top, IBC_D, 
                    label="IBC-1\n(BLUE, TOP NEAR)")
    _ghost_ibc_elev_far(ax, IBC_FAR_Y, plat_top, IBC_D, 
                        label="IBC-2\n(BLUE, TOP FAR)")

    # ── Front pair of the deep 4-leg box — two full-height corridor uprights.
    #    A matching BACK pair sits 450mm behind (occluded in this front view). ──
    for uyd in (POST_NEAR_YD, POST_FAR_YD):
        _rhs_rect(ax, uyd, 0, FRAME_RHS, TOP_Z, alpha=0.85, hatch="///")

    # Top + bottom rings tie the near & far uprights across the corridor (front ring pair).
    for rz in (0, TOP_Z - FRAME_RHS):
        _rhs_rect(ax, POST_NEAR_YD + FRAME_RHS, rz,
                  POST_FAR_YD - (POST_NEAR_YD + FRAME_RHS), FRAME_RHS,
                  fc=C_FRAME, alpha=0.7, lw=1.2, zo=6)

    # Floor flange feet under the two uprights.
    for uyd in (POST_NEAR_YD, POST_FAR_YD):
        _foot_elev(ax, uyd + FRAME_RHS / 2)

    # Direct-stack junction line (totes bear cage-on-cage — no deck, 52mm headroom).
    for col_l, col_r in [(BLUE_IBC_Y, NEAR_COL_R), (IBC_FAR_Y, IBC_FAR_Y + IBC_D)]:
        ax.plot([(col_l), (col_r)], [(PLATFORM_Z)] * 2,
                color=C_OUT, lw=2.0, zorder=8)

    # Front retaining bars (foreground, at the IBC front) + wall joist hangers +
    # D-ring lashing holders. Two bars per column at the lower/upper tote mids.
    for bz in (560, 1760):
        for y0, y1 in ((0, NEAR_COL_R + FRAME_RHS), (FAR_COL_L - FRAME_RHS, C_WID)):
            _rhs_rect(ax, y0, bz, y1 - y0, FRAME_RHS, 
                      fc=C_STEEL, alpha=0.55, lw=1.0, zo=9)
        for wyd, din in ((0, 1), (C_WID, -1)):   # wall joist hangers (U-pocket)
            _rhs_rect(ax, min(wyd, wyd + din * 60), bz - 8, 60, FRAME_RHS + 16, 
                      fc=C_STEEL, lw=1.0, zo=10)
    for ydh in (520, C_WID - 520):               # D-ring lashing holders
        for bz in (560, 1760):
            ax.add_patch(Circle(((ydh), (bz + FRAME_RHS / 2)), (15),
                                fc="none", ec=C_STEEL, lw=2.0, zorder=11))

    # ── Weld symbols at key joints ──────────────────────────────────────────
    # Platform to upright joints
    for uyd in [POST_NEAR_YD + FRAME_RHS / 2, POST_FAR_YD + FRAME_RHS / 2]:
        _weld_tick(ax, uyd + FRAME_RHS / 2 + 3, PLATFORM_Z + FRAME_RHS / 2,
                   side='right')
    # Base joints
    for uyd in [POST_NEAR_YD + FRAME_RHS / 2, POST_FAR_YD + FRAME_RHS / 2]:
        _weld_tick(ax, uyd + FRAME_RHS / 2 + 3, FRAME_RHS / 2,
                   side='right')

    # ── Centerlines ─────────────────────────────────────────────────────────
    cl_yd = FRAME_FOOTPRINT_W / 2
    ax.plot([(cl_yd), (cl_yd)], [(Z_LO + 50), (TOP_Z + 100)],
            color=C_CL, lw=0.6, ls=(0, (8, 4, 2, 4)), zorder=3)
    ax.text((cl_yd), (Z_LO + 40), "CL", ha="center", va="top",
            fontsize=6, color=C_CL, **FONT)

    # ── Dimensions ──────────────────────────────────────────────────────────
    # Overall width
    draw_dim_h(ax, (0), (FRAME_FOOTPRINT_W), (-80),
               f"{FRAME_FOOTPRINT_W}mm  FRAME WIDTH (WALL-TO-WALL)",
               offset=(9), fs=6, font=FONT, above=False)

    # Near column
    draw_dim_h(ax, (BLUE_IBC_Y), (NEAR_COL_R), (-50),
               f"{IBC_D}mm  IBC DEPTH",
               offset=(9), fs=5.5, font=FONT)

    # Corridor
    draw_dim_h(ax, (NEAR_COL_R), (FAR_COL_L), (-50),
               f"{CORRIDOR_W}mm\nCORRIDOR",
               offset=(9), fs=5.5, font=FONT)

    # Far column
    draw_dim_h(ax, (IBC_FAR_Y), (IBC_FAR_Y + IBC_D), (-50),
               f"{IBC_D}mm  IBC DEPTH",
               offset=(9), fs=5.5, font=FONT)

    # Heights (right side): direct-stack junction, 2x stack, ceiling clearance.
    dim_yd = IBC_FAR_Y + IBC_D + FRAME_RHS + 80
    draw_dim_v(ax, (dim_yd), (0), (PLATFORM_Z),
               f"{PLATFORM_Z}mm JUNCTION",
               offset=(32), fs=5.5, right=True, font=FONT)
    draw_dim_v(ax, (dim_yd + 60), (0), (STACK_Z),
               f"{STACK_Z}mm 2x STACK",
               offset=(32), fs=5.5, right=True, font=FONT)
    draw_dim_v(ax, (dim_yd + 120), (STACK_Z), (C_HGT),
               f"{C_HGT - STACK_Z}mm CLEARANCE",
               offset=(32), fs=5.5, right=True, font=FONT)

    # RHS member size
    draw_dim_h(ax, (POST_NEAR_YD), (POST_NEAR_YD + FRAME_RHS),
               (TOP_Z + 60),
               f"{FRAME_RHS}mm", offset=(32), fs=5.5, font=FONT)

    # IBC anatomy dimensions (left side of near column)
    anat_yd = BLUE_IBC_Y - FRAME_RHS - 90
    draw_dim_v(ax, (anat_yd), (0), (IBC_PALLET_H),
               f"{IBC_PALLET_H}mm PALLET",
               offset=(32), fs=5, font=FONT)
    draw_dim_v(ax, (anat_yd), (IBC_PALLET_H), (IBC_BOTTLE_TOP),
               f"{IBC_BOTTLE_TOP - IBC_PALLET_H}mm BOTTLE",
               offset=(32), fs=5, font=FONT)
    draw_dim_v(ax, (anat_yd + 40), (IBC_BOTTLE_TOP), (IBC_H_1000),
               f"{IBC_CAGE_RAIL_W}mm RAIL",
               offset=(42), fs=5, font=FONT)
    # Valve height
    draw_dim_v(ax, (anat_yd - 60), (0), (IBC_VALVE_Z),
               f"{IBC_VALVE_Z}mm VALVE CL",
               offset=(32), fs=5, font=FONT)

    # ── Member labels (restraint frame — lighter callouts) ──────────────────
    leader(ax, (NEAR_COL_R + FRAME_RHS / 2), (TOP_Z * 0.7),
           (NEAR_COL_R - 70), (TOP_Z * 0.7 + 30),
           "DEEP-BOX UPRIGHTS\n50×50×3 RHS (front pair ×2;\nmatching back pair 450mm behind)",
           color=C_OUT, fs=5.5, ha="left", va="bottom",
           arrow_style="-|>", font=FONT)

    leader(ax, (POST_NEAR_YD - FRAME_RHS * 0.3), (FOOT_PLATE_T / 2),
           (POST_NEAR_YD - 220), (140),
           "FLOOR FLANGE FOOT\n150×150×12, 4× M12\n(×4, one per leg)",
           color=C_OUT, fs=5.5, ha="left", va="top",
           arrow_style="-|>", font=FONT)

    leader(ax, (NEAR_COL_R + FRAME_RHS), (1760 + FRAME_RHS / 2),
           (NEAR_COL_R - 70), (1900),
           "FRONT RETAINING BAR (×4)\n50×20×3 RHS at IBC front\n(25mm gap), Z560 + Z1760 — slide-stop\n+ D-ring lash points",
           color=C_OUT, fs=5.5, ha="left", va="bottom",
           arrow_style="-|>", font=FONT)

    leader(ax, (30), (1760 + FRAME_RHS / 2),
           (330), (1500),
           "WALL JOIST HANGER (×4)\nSimpson U-pocket, through-bolted\n(4× M12) to a 100×135×8 EXTERIOR\nbacking plate (hex heads outside)",
           color=C_OUT, fs=5.5, ha="left", va="top",
           arrow_style="-|>", font=FONT)

    # ── IBC anatomy labels ──────────────────────────────────────────────────
    leader(ax, (BLUE_IBC_Y + IBC_D / 2), (IBC_PALLET_H / 2),
           (BLUE_IBC_Y + IBC_D / 2 - 70), (IBC_PALLET_H + 60),
           "PALLET BASE\n168mm (STEEL/PLASTIC)\nFORK POCKETS",
           color=C_PALLET, fs=5, ha="right", va="bottom",
           arrow_style="-|>", font=FONT)

    # Pull the valve callout into the bottom-tier face just left of the valve
    # (short leader, rule 67), clear above the PALLET BASE callout below it.
    leader(ax, (BLUE_IBC_Y + IBC_D - IBC_CAGE_INSET), (IBC_VALVE_Z),
           (BLUE_IBC_Y + IBC_D - 80), (IBC_VALVE_Z + 75),
           f"DN50 VALVE (S60×6)\nZ={IBC_VALVE_Z}mm\nCORRIDOR FACE",
           color=C_CAGE, fs=5, ha="left", va="bottom",
           arrow_style="-|>", font=FONT)

    leader(ax, (BLUE_IBC_Y + IBC_CAGE_INSET), (IBC_H_1000 - 50),
           (BLUE_IBC_Y + 75), (IBC_H_1000 + 100),
           f"CAGE TOP RAIL\n{IBC_CAGE_TUBE_D}mm Ø TUBE\nLASHING STRAP BEARS HERE",
           color=C_CAGE, fs=5, ha="right", va="bottom",
           arrow_style="-|>", font=FONT)

    leader(ax, (IBC_FAR_Y + IBC_D / 2),
           (plat_top + IBC_PALLET_H / 2),
           (IBC_FAR_Y + IBC_D * 0.5),
           (plat_top + IBC_PALLET_H / 2 + 140),
           "UPPER TOTE BEARS DIRECTLY\nON THE LOWER TOTE CAGE\n(direct stack, no deck)",
           color=C_PALLET, fs=5, ha="center", va="bottom",
           arrow_style="-|>", font=FONT)

    # ── Material note ───────────────────────────────────────────────────────
    notes = [
        "MATERIAL & FABRICATION NOTES (RESTRAINT-ONLY FRAME):",
        f"1. All RHS members: 50×50×3mm mild steel, A500 Grade B. Joints fillet welded (5mm leg), continuous.",
        f"2. RESTRAINT, not load-bearing: the 1000L caged totes DIRECT-STACK cage-on-cage (52mm headroom — no deck between tiers).",
        f"   A DEEP 4-LEG BOX (front + back upright pairs, 450mm apart, tied by top + bottom rings) at the IBC front restrains them.",
        f"3. Floor flange feet (×4): 150×150×12mm plate fillet welded to each leg base; 4× M12 anchors into the floor (uplift + lateral restraint). Front feet reach ~25mm under the tray edge.",
        f"4. Front retaining bars (×4, Z560 + Z1760): stop the totes sliding out the front; each bar's wall end drops into a Simpson-style wall joist",
        f"   hanger (×4), through-bolted (4× M12) to a 100×135×8mm EXTERIOR backing plate (hex heads outside) that spreads the load into the thin corrugated wall.",
        f"5. D-ring lashing holders on the front bars (1,100 kg WLL); ratchet straps over each stack tie down to them.",
        f"6. Surface finish: gray oxide primer + flat black powder coat.",
        f"7. IBC anatomy: US 48\"×40\" caged composite tote (1000L, 1168mm) — {IBC_PALLET_H}mm pallet base + HDPE bottle + galvanized wire cage.",
        f"   v2 layout: Brown/Waste bottom, Blue on top.",
        f"8. Cage top rail ({IBC_CAGE_TUBE_D}mm Ø tube) is the highest point; lashing straps bear on it.",
        f"9. IBC valve face (DN50, S60×6) points toward the corridor. Valve CL at Z={IBC_VALVE_Z}mm above each tote base.",
        f"10. Total frame weight: ~90 kg (incl. 4 feet + rings + front bars + hangers + exterior wall plates + rear-panel brackets).",
    ]
    draw_notes(ax, notes, (2500), (TOP_Z + 600), spacing=(23),
               fs=7, font=FONT, width=(1800))

    # ── Title block ─────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 3",
                drawing_title="IBC SUPPORT FRAME",
                subtitle="FRONT ELEVATION — FRAME ASSEMBLY",
                scale_note="Axes in mm — VIEW ALONG X",
                height=0.04)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "ibc-frame-sheet1.png"), dpi=130,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-frame-sheet1.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Side Elevation
#
# Looking along Yd from the near wall.  Shows frame depth along X
# (horizontal) and height Z (vertical).  One column of the corridor
# structure visible — the other column is directly behind.
#
# Visible:
#   - 3 uprights (front, mid, back) at one corridor edge
#   - 3 levels of longitudinal beams connecting them
#   - Diagonal X-braces in bottom tier bays
#   - Platform surface, anti-rotation lip, rubber mat
#   - D-ring positions
#   - Access gate
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():
    """Sheet 2 — Side elevation of IBC support frame."""

    X_LO = -300
    X_HI = FRAME_FOOTPRINT_D + 300
    Z_LO = -400
    Z_HI = PANEL_FRAME_TOP_Z + 360

    fig, ax = plt.subplots(figsize=(16, 19))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim((X_LO), (X_HI))
    ax.set_ylim((Z_LO), (Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text((FRAME_FOOTPRINT_D / 2), (PANEL_FRAME_TOP_Z + 300),
            "SIDE ELEVATION — LOOKING ALONG Yd FROM NEAR WALL",
            ha="center", va="bottom", fontsize=9, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── Ghost IBC outlines (cage/pallet anatomy) ──────────────────────────────
    # In side elevation, IBC width = IBC_W = 1219mm along X.
    # IBC is centered in frame depth: offset = (FRAME_FOOTPRINT_D - IBC_W)/2
    ibc_x_offset = (FRAME_FOOTPRINT_D - IBC_W) / 2 + 200# ~32.5mm
    plat_top = PLATFORM_Z + FRAME_RHS + MAT_T
    # Bottom tier
    _ghost_ibc_elev(ax, ibc_x_offset, 0, IBC_W, 
                    label="BOTTOM TIER\n(IBC-3 OR IBC-4)")
    # Top tier
    _ghost_ibc_elev(ax, ibc_x_offset, plat_top, IBC_W, 
                    label="TOP TIER\n(IBC-1 OR IBC-2)")

    # ── Uprights (deep 4-leg box: front pair + back pair, 450mm apart) ───────
    for fx in FX_POSTS:
        _rhs_rect(ax, fx, 0, FRAME_RHS, TOP_Z, alpha=0.8)

    # ── Top + bottom rings tying the front and back uprights (butt-jointed) ──
    for rz in (0, TOP_Z - FRAME_RHS):
        _rhs_rect(ax, FX_FRONT + FRAME_RHS, rz, FRAME_FOOTPRINT_D - FRAME_RHS, FRAME_RHS,
                  fc=C_FRAME, alpha=0.5, lw=1.2, zo=4)

    # ── Floor flange feet under each upright ─────────────────────────────────
    for fx in FX_POSTS:
        _foot_elev(ax, fx + FRAME_RHS / 2)

    # ── Direct-stack junction line (totes bear cage-on-cage — no deck) ──────
    ax.plot([(ibc_x_offset), (ibc_x_offset + IBC_W)], [(PLATFORM_Z)] * 2,
            color=C_OUT, lw=2.0, zorder=8)

    # ── Front retaining bars (end-on at the IBC front, both tiers) ──────────
    for bz in (560, 1760):
        _rhs_rect(ax, FX_FRONT, bz, FRAME_RHS, FRAME_RHS, 
                  fc=C_STEEL, alpha=0.6, lw=1.0, zo=8)

    # ── Weld symbols at upright/beam joints ─────────────────────────────────
    for fx in FX_POSTS:
        for bz in [FRAME_RHS, PLATFORM_Z + FRAME_RHS]:
            _weld_tick(ax, fx + FRAME_RHS + 3, bz, side='right')

    # ── Right-walkway cantilever arm (rev12) — attaches to the front corridor
    # upright and projects off the front of the frame toward the walkway.  In side
    # elevation (along Yd) the 2 arms (Yd 1046/1266) overlap into one bar. ──
    _rhs_rect(ax, ARM_X_TIP_L, ARM_Z0, FRAME_RHS - ARM_X_TIP_L, ARM_Z1 - ARM_Z0,
              fc=C_ARM, alpha=0.9, zo=7)
    # upright clamp wrapping the front corridor upright + 2 M12 bolts
    _rhs_rect(ax, FX_FRONT - 4, ARM_Z0 - 25, FRAME_RHS + 8, (ARM_Z1 - ARM_Z0) + 55,
              fc=C_ARM, alpha=0.45, zo=6)
    for bz in (ARM_Z0 + 6, ARM_Z1 + 14):
        ax.add_patch(Circle(((FX_FRONT + FRAME_RHS / 2), (bz)), (6),
                            fc=C_OUT, ec=C_OUT, lw=0.5, zorder=9))
    # Rewrapped to narrow lines (rule 66) so the block stays in the left margin
    # instead of spilling across the upright + X-brace; full text is in note 9.
    leader(ax, (ARM_X_TIP_L + 40), (ARM_Z1),
           (ARM_X_TIP_L - 10), (ARM_Z1 + 90),
           "RIGHT-WALKWAY\nCANTILEVER ARM\n40×40×3 SHS (×2)\n(see note 9)",
           color=C_ARM, fs=5.5, ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # ── Dimensions ──────────────────────────────────────────────────────────
    # Overall depth
    draw_dim_h(ax, (FX_FRONT), (FX_BACK + FRAME_RHS), (-160),
               f"{FRAME_FOOTPRINT_D}mm  FRAME DEPTH",
               offset=(10), fs=6, font=FONT, above=False)


    # Heights (right side)
    dim_x = FRAME_FOOTPRINT_D + 80
    draw_dim_v(ax, (dim_x), (0), (PLATFORM_Z),
               f"{PLATFORM_Z}mm", offset=(10), fs=5.5, right=True, font=FONT)
    draw_dim_v(ax, (dim_x + 60), (PLATFORM_Z), (TOP_Z),
               f"{TOP_Z - PLATFORM_Z}mm", offset=(10), fs=5.5,
               right=True, font=FONT)
    draw_dim_v(ax, (dim_x + 120), (0), (TOP_Z),
               f"{TOP_Z}mm TOTAL", offset=(10), fs=5.5,
               right=True, font=FONT)

    # ── Member labels ───────────────────────────────────────────────────────
    # Short leader into the open upper-tier face just right of the post (rule 67).
    leader(ax, (FX_FRONT + FRAME_RHS), (TOP_Z * 0.62),
           (FX_FRONT + FRAME_RHS + 55), (TOP_Z * 0.62 + 25),
           "DEEP-BOX UPRIGHTS\n50×50×3 RHS, floor to top\n(front + back pair, ×2 across Yd = 4 legs)",
           color=C_OUT, fs=5.5, ha="left", va="bottom",
           arrow_style="-|>", font=FONT)

    leader(ax, (FX_FRONT + FRAME_RHS), (1760),
           (FX_FRONT + FRAME_RHS + 70), (1760 + 120),
           "FRONT RETAINING BARS\n(end-on) — Z560 + Z1760,\nslide-stop + lashing",
           color=C_OUT, fs=5.5, ha="left", va="bottom",
           arrow_style="-|>", font=FONT)

    # ── Notes ───────────────────────────────────────────────────────────────
    notes = [
        "SIDE ELEVATION NOTES (RESTRAINT-ONLY FRAME):",
         "1. DEEP 4-LEG BOX at the IBC front: a FRONT upright pair at the corridor",
        f"   mouth + a BACK pair {FRAME_FOOTPRINT_D}mm behind, tied by top + bottom",
         "   rings. It carries the Corridor pump panel + drain-riser spine on the",
         "   back uprights; the direct-stacked totes need only restraint.",
        f"2. Totes DIRECT-STACK cage-on-cage at Z={PLATFORM_Z}mm (no deck, 52mm",
         "   headroom). Restraint = box + front retaining bars + lashing.",
         "3. Each upright base (×4): 150×150×12mm floor flange plate, 4× M12 anchors;",
         "   the front feet reach ~25mm under the tray edge.",
         "4. Front retaining bars (Z560 + Z1760) stop the totes sliding out the",
         "   front; wall ends drop into Simpson-style joist hangers.",
        f"5. RIGHT-WALKWAY CANTILEVER ARMS (rev12): 2× 40×40×3 SHS clamp to the",
         "   FRONT box uprights and project off the front to carry the walkway.",
    ]
    draw_notes(ax, notes, (X_LO + 20), (Z_HI - 100), spacing=(20),
               fs=6.5, font=FONT, width=(825))

    # ── Title block ─────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 3",
                drawing_title="IBC SUPPORT FRAME",
                subtitle="SIDE ELEVATION — DEEP 4-LEG BOX (RESTRAINT)",
                scale_note="Axes in mm — VIEW ALONG Yd",
                height=0.04)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "ibc-frame-sheet2.png"), dpi=130,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-frame-sheet2.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — Plan View (at platform level)
#
# Looking down.  X horizontal (depth), Yd vertical (width).
# Shows beam layout, corridor opening, wall brackets, anti-rotation lip,
# rubber mat positions, and IBC footprints as ghost outlines.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet3():
    """Sheet 3 — Plan view of IBC support frame at platform level."""

    X_LO = -300
    X_HI = IBC_W + 320                 # totes extend back past the 450mm box, at the corridor mouth
    YD_LO = -750
    YD_HI = FRAME_FOOTPRINT_W + 300

    fig, ax = plt.subplots(figsize=(16, 24))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim((X_LO), (X_HI))
    ax.set_ylim((YD_LO), (YD_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text((IBC_W / 2), (FRAME_FOOTPRINT_W + 200),
            "PLAN VIEW — LOOKING DOWN (DEEP 4-LEG BOX + RETAINING BARS)",
            ha="center", va="bottom", fontsize=9, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── Deep 4-leg box (plan): 4 uprights (front + back × near/far Yd) tied by
    #    top/bottom rings (shown as the box perimeter) + front retaining bars. ──
    near_mat_yd = BLUE_IBC_Y
    far_mat_yd = IBC_FAR_Y
    # ring perimeter (top + bottom rings project together): X-rails front↔back + Yd-rails near↔far
    for post_yd in (POST_NEAR_YD, POST_FAR_YD):
        _rhs_rect(ax, FX_FRONT + FRAME_RHS, post_yd, FRAME_FOOTPRINT_D - FRAME_RHS, FRAME_RHS,
                  fc=C_FRAME, alpha=0.4, lw=1.0, zo=4)
    for fx in FX_POSTS:
        _rhs_rect(ax, fx, POST_NEAR_YD + FRAME_RHS, FRAME_RHS, POST_FAR_YD - (POST_NEAR_YD + FRAME_RHS),
                  fc=C_FRAME, alpha=0.4, lw=1.0, zo=4)
    # 4 uprights at the box corners
    for fx in FX_POSTS:
        for post_yd in (POST_NEAR_YD, POST_FAR_YD):
            _rhs_rect(ax, fx, post_yd, FRAME_RHS, FRAME_RHS,
                      fc=C_FRAME, alpha=0.85, lw=1.4)
    # Front retaining bars run in Yd at the IBC front (wall -> upright per column).
    for y0, y1 in ((0, POST_NEAR_YD + FRAME_RHS), (POST_FAR_YD, FRAME_FOOTPRINT_W)):
        _rhs_rect(ax, FX_FRONT, y0, FRAME_RHS, y1 - y0, 
                  fc=C_STEEL, alpha=0.55, lw=1.0)

    # ── IBC footprint ghost outlines (with cage/pallet anatomy) ──────────────
    ibc_x = FX_FRONT + 20              # tote front ~20mm behind the box front (corridor mouth); totes extend back
    _ghost_ibc_plan(ax, ibc_x, near_mat_yd, IBC_W, IBC_D, 
                    label="IBC PALLET\nFOOTPRINT")
    _ghost_ibc_plan(ax, ibc_x, far_mat_yd, IBC_W, IBC_D, 
                    label="IBC PALLET\nFOOTPRINT")

    # ── Corridor opening ────────────────────────────────────────────────────
    corr_x1 = FX_FRONT + FRAME_RHS
    corr_x2 = FRAME_FOOTPRINT_D - FRAME_RHS
    corr_y1 = POST_NEAR_YD + FRAME_RHS
    corr_y2 = POST_FAR_YD
    ax.add_patch(Rectangle(((corr_x1), (corr_y1)),
                            (corr_x2 - corr_x1), (corr_y2 - corr_y1),
                            fc=C_CL, ec="none", alpha=0.06, zorder=3))
    ax.text((FRAME_FOOTPRINT_D / 2), ((corr_y1 + corr_y2) / 2),
            f"CORRIDOR OPENING\n{CORRIDOR_W - 2 * FRAME_RHS}mm CLEAR",
            ha="center", va="center", fontsize=6, color=C_CL,
            fontweight="bold", **FONT, zorder=10)

    # ── Right-walkway cantilever arms (rev12) — off the corridor uprights ──────
    # Each arm cantilevers off a corridor upright (Yd 1046/1266) toward -X (off the
    # front of the frame) to carry the right walkway's left long beam.
    for post_yd in [POST_NEAR_YD, POST_FAR_YD]:
        _rhs_rect(ax, ARM_X_TIP_L, post_yd, (FX_FRONT + FRAME_RHS) - ARM_X_TIP_L, ARM_W,
                  fc=C_ARM, alpha=0.9, zo=7)
    # Rewrapped to narrow lines (rule 66) + short leader (rule 67) so the block
    # stays in the left margin instead of spilling over the frame footprint.
    leader(ax, (ARM_X_TIP_L + 60), (POST_NEAR_YD + ARM_W / 2),
           (ARM_X_TIP_L - 10), (POST_NEAR_YD - 110),
           "RIGHT-WALKWAY\nCANTILEVER ARMS (×2)\n40×40×3 SHS\n(off-frame, toward −X)",
           color=C_ARM, fs=5.5, ha="left", va="top", arrow_style="-|>", font=FONT)

    # ── Floor flange feet (projected, under the 4 box legs: front + back) ────
    for fx in FX_POSTS:
        for post_yd in [POST_NEAR_YD, POST_FAR_YD]:
            _foot_plan(ax, fx + FRAME_RHS / 2, post_yd + FRAME_RHS / 2)

    # ── Dimensions ──────────────────────────────────────────────────────────
    # Overall depth
    draw_dim_h(ax, (FX_FRONT), (FRAME_FOOTPRINT_D), (-120),
               f"{FRAME_FOOTPRINT_D}mm  FRAME DEPTH",
               offset=(8), fs=6, font=FONT)

    # Overall width
    dim_x = IBC_W + 60                 # right of the tote footprints (box is only 450 deep)
    draw_dim_v(ax, (dim_x + 50), (0), (FRAME_FOOTPRINT_W),
               f"{FRAME_FOOTPRINT_W}mm FRAME WIDTH",
               offset=(8), fs=6, right=True, font=FONT)

    # Near column depth
    draw_dim_v(ax, (dim_x + 80), (BLUE_IBC_Y), (NEAR_COL_R),
               f"{IBC_D}mm", offset=(8), fs=5.5, right=True, font=FONT)

    # Corridor
    draw_dim_v(ax, (dim_x + 80), (NEAR_COL_R), (FAR_COL_L),
               f"{CORRIDOR_W}mm", offset=(8), fs=5.5, right=True, font=FONT)

    # Far column depth
    draw_dim_v(ax, (dim_x + 80), (IBC_FAR_Y), (IBC_FAR_Y + IBC_D),
               f"{IBC_D}mm", offset=(8), fs=5.5, right=True, font=FONT)

    # RHS member size
    draw_dim_h(ax, (FX_FRONT), (FX_FRONT + FRAME_RHS),
               (FRAME_FOOTPRINT_W + 80),
               f"{FRAME_RHS}mm", offset=(8), fs=5.5, font=FONT)

    # ── Detail inset: Corner Joint ──────────────────────────────────────────
    det_x = (X_LO + 20)
    det_y = (YD_LO + 240)
    det_w = (350)
    det_h = (280)
    ax.add_patch(Rectangle((det_x, det_y), det_w, det_h,
                            fc="white", ec=C_OUT, lw=1.5, zorder=12))
    ax.text(det_x + det_w / 2, det_y + det_h - (10),
            "DETAIL A: TYPICAL CORNER JOINT (≈5:1)",
            ha="center", va="top", fontsize=6, color=C_OUT,
            fontweight="bold", **FONT, zorder=13)

    # Draw enlarged corner joint
    dsx = 10 / 7  # detail magnification (was 4.0 / S where S=2.8)
    dcx = det_x + det_w * 0.4  # detail center X
    dcy = det_y + det_h * 0.45

    # Upright (vertical member, going up out of page — shown as cross-section)
    ax.add_patch(Rectangle((dcx - (FRAME_RHS / 2 * dsx),
                             dcy - (FRAME_RHS / 2 * dsx)),
                            (FRAME_RHS * dsx),
                            (FRAME_RHS * dsx),
                            fc=C_STEEL, ec=C_OUT, lw=1.8, zorder=13,
                            hatch="///", alpha=0.6))
    # Inner void
    ax.add_patch(Rectangle((dcx - ((FRAME_RHS / 2 - FRAME_T) * dsx),
                             dcy - ((FRAME_RHS / 2 - FRAME_T) * dsx)),
                            ((FRAME_RHS - 2 * FRAME_T) * dsx),
                            ((FRAME_RHS - 2 * FRAME_T) * dsx),
                            fc=BG, ec=C_OUT, lw=0.8, zorder=14))

    # Beam stub (horizontal, going right)
    beam_l = FRAME_RHS * 2 * dsx
    beam_h = FRAME_RHS * dsx
    beam_x = dcx + (FRAME_RHS / 2 * dsx)
    beam_y = dcy - (FRAME_RHS / 2 * dsx)
    ax.add_patch(Rectangle((beam_x, beam_y), (beam_l), (beam_h),
                            fc=C_STEEL, ec=C_OUT, lw=1.8, zorder=13,
                            hatch="\\\\\\", alpha=0.5))

    # Weld symbol
    wx = beam_x
    wy = dcy
    ax.plot([wx, wx + (12)], [wy, wy + (12)],
            color=C_WELD, lw=2.5, zorder=15)
    ax.plot([wx, wx + (12)], [wy, wy - (12)],
            color=C_WELD, lw=2.5, zorder=15)
    # Lift the weld note off the hatched beam into the open space above it
    # (rule 62); the red chevron already marks the weld location.
    ax.text(beam_x + (beam_l * 0.45), dcy + (beam_h / 2 + 16),
            "FILLET WELD\n5mm LEG\nCONTINUOUS",
            ha="center", va="bottom", fontsize=4.5, color=C_WELD,
            **FONT, zorder=15)

    # Labels
    ax.text(dcx, dcy + (FRAME_RHS / 2 * dsx) + (8),
            "UPRIGHT\n(CUT SECTION)", ha="center", va="bottom",
            fontsize=4.5, color=C_DIM, **FONT, zorder=15)
    ax.text(beam_x + (beam_l / 2), beam_y - (8),
            "BEAM", ha="center", va="top",
            fontsize=4.5, color=C_DIM, **FONT, zorder=15)

    # ── Detail inset: D-ring Mounting ───────────────────────────────────────
    det2_x = det_x + det_w + (40)
    det2_y = det_y
    det2_w = (350)
    det2_h = (280)
    ax.add_patch(Rectangle((det2_x, det2_y), det2_w, det2_h,
                            fc="white", ec=C_OUT, lw=1.5, zorder=12))
    ax.text(det2_x + det2_w / 2, det2_y + det2_h - (10),
            "DETAIL B: D-RING LASHING POINT (≈4:1)",
            ha="center", va="top", fontsize=6, color=C_OUT,
            fontweight="bold", **FONT, zorder=13)

    # Mounting plate
    d_dsx = 1.25  # detail magnification (was 3.5 / S where S=2.8)
    d_cx = det2_x + det2_w * 0.5
    d_cy = det2_y + det2_h * 0.40
    plate_w_d = (DRING_SIZE + 30) * d_dsx
    plate_h_d = (DRING_SIZE + 30) * d_dsx
    ax.add_patch(Rectangle((d_cx - (plate_w_d / 2), d_cy - (plate_h_d / 2)),
                            (plate_w_d), (plate_h_d),
                            fc=C_STEEL, ec=C_OUT, lw=1.8, zorder=13,
                            alpha=0.5))

    # D-ring
    d_r = DRING_SIZE / 2 * d_dsx
    theta = np.linspace(0, np.pi, 40)
    d_ring_x = [d_cx + (d_r * np.cos(t)) for t in theta]
    d_ring_y = [d_cy + (d_r * np.sin(t)) for t in theta]
    ax.plot(d_ring_x, d_ring_y, color=C_OUT, lw=3.0, zorder=14)
    ax.plot([d_cx - (d_r), d_cx + (d_r)], [d_cy, d_cy],
            color=C_OUT, lw=3.0, zorder=14)

    # Pin hole
    ax.add_patch(Circle((d_cx, d_cy), (3 * d_dsx),
                         fc=C_OUT, ec=C_OUT, lw=1.0, zorder=15))

    # Labels
    ax.text(d_cx, d_cy + (d_r) + (30),
            f"D-RING 25mm WLL {DRING_WLL} kg",
            ha="center", va="bottom", fontsize=4.5, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)
    ax.text(d_cx, d_cy - (plate_h_d / 2) - (8),
            "6mm MOUNTING PLATE\nFILLET WELDED TO UPRIGHT",
            ha="center", va="top", fontsize=4.5, color=C_DIM,
            **FONT, zorder=15)

    # ── Notes ───────────────────────────────────────────────────────────────
    notes = [
        "PLAN VIEW NOTES (RESTRAINT-ONLY FRAME):",
        "1. DEEP 4-LEG BOX: 4 uprights (front + back pair, 450mm apart) at Yd 1046/1266 on",
        "150×150×12 floor flange feet (4× M12 each), tied by top + bottom rings. It carries the",
        "Corridor pump panel + drain-riser spine on the back uprights; totes need only restraint.",
        "2. Front retaining bars run in Yd at the IBC front (wall -> upright per column) — they",
        "stop the totes sliding out the front; wall ends drop into Simpson-style joist hangers.",
        "3. 270mm plumbing corridor (Yd 1046-1316) stays clear between the IBC columns.",
        f"4. IBC ghost outline shows pallet footprint (brown), bottle inset (blue), cage corner",
        f"tubes ({IBC_CAGE_TUBE_D}mm Ø, gray circles). v2 layout: Brown/Waste bottom, Blue top.",
        "5. RIGHT-WALKWAY CANTILEVER ARMS (rev12): 2× 40×40×3 SHS clamp to the FRONT box",
        "uprights (Yd 1046/1266), projecting off the front (−X) to carry the right walkway.",
    ]
    draw_notes(ax, notes, (X_HI * 0.32), (YD_LO + 510), spacing=(20),
               fs=7, font=FONT, width=(1040))

    # ── Title block ─────────────────────────────────────────────────────────
    title_block(ax, "SHEET 3 OF 3",
                drawing_title="IBC SUPPORT FRAME",
                subtitle="PLAN VIEW — DEEP 4-LEG BOX + RETAINING BARS",
                scale_note="Axes in mm — VIEW LOOKING DOWN",
                height=0.04)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "ibc-frame-sheet3.png"), dpi=130,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-frame-sheet3.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    print("Generating IBC support frame drawings...")
    sheet1()
    sheet2()
    sheet3()
    print("Done.")
