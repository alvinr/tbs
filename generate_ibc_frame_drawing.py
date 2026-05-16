#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_ibc_frame_drawing.py  —  TBS-001 IBC Support Frame Fabrication Drawings

Three-sheet fabrication drawing set for the welded 50×50×3mm RHS mild steel
IBC stacking frame.  Shows frame structure only — no IBCs, plumbing, or
other container equipment.

Sheet 1 — Front Elevation (looking along X toward sealed end wall)
Sheet 2 — Side Elevation (looking along Yd from near wall)
Sheet 3 — Plan View (looking down at platform level)

Each sheet includes dimensional callouts and assembly detail insets.

Frame concept:
  A portal spine along the 270mm plumbing corridor with cantilever platform
  beams supporting upper-tier IBCs.  Three bays along X (front/mid/back
  uprights at 642mm centers).  Wall brackets at near and far container walls
  provide lateral restraint.  No X-end posts — IBCs are loaded from above.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch, Circle
import matplotlib.patches as mpatches

from tbs_constants import (
    svg_path, SVG_DIR,
    C_LEN, C_WID, C_HGT,
    IBC_COL_X, IBC_W, IBC_D, IBC_H_600, IBC_H_STK,
    BLUE_IBC_Y, IBC_FAR_Y,
)
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader, hatch_rect

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
FRAME_FOOTPRINT_W = C_WID  # 2,362mm wall-to-wall
FRAME_FOOTPRINT_D = 1284   # depth along X
MAT_T      = 12            # anti-slip rubber mat thickness

# Derived positions (Yd, container coordinates)
NEAR_COL_R = BLUE_IBC_Y + IBC_D       # 1,046 — near corridor edge
FAR_COL_L  = IBC_FAR_Y                # 1,316 — far corridor edge
CORRIDOR_W = FAR_COL_L - NEAR_COL_R   # 270mm

# Corridor post Yd positions (inner faces, where IBC column meets corridor)
POST_NEAR_YD = NEAR_COL_R             # 1,046
POST_FAR_YD  = FAR_COL_L - FRAME_RHS  # 1,266

# Heights
PLATFORM_Z = IBC_H_600                # 1,010mm
TOP_Z      = IBC_H_STK + FRAME_RHS    # 2,070mm

# Frame X positions (frame-local, 0 = front/cargo-door side)
# Frame extends 65mm past IBC on cargo-door side, flush to end wall on back.
# Three bays: front, mid, back uprights.
FX_FRONT = 0
FX_MID   = FRAME_FOOTPRINT_D // 2     # 642mm
FX_BACK  = FRAME_FOOTPRINT_D          # 1,284mm
FX_POSTS = [FX_FRONT, FX_MID, FX_BACK]

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

# Wall bracket
BRACKET_L   = 150   # bracket leg length along Yd
BRACKET_T   = 8     # bracket plate thickness
BRACKET_BOLT_D = 12 # M12 anchor bolts


# ═══════════════════════════════════════════════════════════════════════════════
# Helper — draw a filled RHS cross-section (cut view)
# ═══════════════════════════════════════════════════════════════════════════════
def _rhs_section(ax, cx, cy, size, sx, sy, *, angle=0, zo=6):
    """Draw a 50×50×3mm RHS cross-section at (cx, cy) in data coords.
    Outer rectangle with inner void, hatched to indicate cut steel."""
    s = size / 2
    t = FRAME_T
    # Outer rectangle
    ax.add_patch(Rectangle((sx(cx - s), sy(cy - s)),
                            sx(size), sy(size),
                            fc=C_STEEL, ec=C_OUT, lw=1.8, zorder=zo,
                            hatch="///", alpha=0.6))
    # Inner void
    ax.add_patch(Rectangle((sx(cx - s + t), sy(cy - s + t)),
                            sx(size - 2 * t), sy(size - 2 * t),
                            fc=BG, ec=C_OUT, lw=0.8, zorder=zo + 1))


def _rhs_rect(ax, x, y, w, h, sx, sy, *, fc=C_FRAME, lw=1.5, zo=5,
              alpha=0.7, hatch=None):
    """Draw a filled rectangle representing an RHS member in elevation."""
    ax.add_patch(Rectangle((sx(x), sy(y)), sx(w), sy(h),
                            fc=fc, ec=C_OUT, lw=lw, zorder=zo,
                            alpha=alpha, hatch=hatch))


def _weld_tick(ax, x, y, sx, sy, *, side='right', size=8, zo=10):
    """Draw a small fillet weld symbol (V-tick) at a joint."""
    s = size
    if side == 'right':
        ax.plot([sx(x), sx(x + s)], [sy(y), sy(y + s)], color=C_WELD,
                lw=1.5, zorder=zo)
        ax.plot([sx(x), sx(x + s)], [sy(y), sy(y - s)], color=C_WELD,
                lw=1.5, zorder=zo)
    elif side == 'left':
        ax.plot([sx(x), sx(x - s)], [sy(y), sy(y + s)], color=C_WELD,
                lw=1.5, zorder=zo)
        ax.plot([sx(x), sx(x - s)], [sy(y), sy(y - s)], color=C_WELD,
                lw=1.5, zorder=zo)
    elif side == 'up':
        ax.plot([sx(x), sx(x + s)], [sy(y), sy(y + s)], color=C_WELD,
                lw=1.5, zorder=zo)
        ax.plot([sx(x), sx(x - s)], [sy(y), sy(y + s)], color=C_WELD,
                lw=1.5, zorder=zo)
    elif side == 'down':
        ax.plot([sx(x), sx(x + s)], [sy(y), sy(y - s)], color=C_WELD,
                lw=1.5, zorder=zo)
        ax.plot([sx(x), sx(x - s)], [sy(y), sy(y - s)], color=C_WELD,
                lw=1.5, zorder=zo)


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — Front Elevation
#
# Looking along X toward the sealed end wall.  Shows full container width
# (Yd axis horizontal, Z axis vertical).  Frame members only.
#
# Visible members:
#   - 2 corridor uprights (front bay, cut section)
#   - 3 transverse beams per level (near col, corridor, far col)
#   - Wall brackets at near and far walls
#   - Anti-rotation lip on platform
#   - D-ring lashing points
#   - Access gates on corridor face
#   - Behind: mid and back bay uprights shown dashed
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():
    """Sheet 1 — Front elevation of IBC support frame."""
    S = 2.8

    def sx(mm): return mm * S
    def sy(mm): return mm * S

    YD_LO = -300
    YD_HI = FRAME_FOOTPRINT_W + 300
    Z_LO  = -400
    Z_HI  = TOP_Z + 300

    fig, ax = plt.subplots(figsize=(20, 18))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(sx(YD_LO), sx(YD_HI))
    ax.set_ylim(sy(Z_LO), sy(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Title ────────────────────────────────────────────────────────────────
    ax.text(sx(FRAME_FOOTPRINT_W / 2), sy(TOP_Z + 200),
            "FRONT ELEVATION — LOOKING ALONG X TOWARD SEALED END WALL",
            ha="center", va="bottom", fontsize=9, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── Base beams (Z=0, transverse — Yd direction) ─────────────────────────
    # Near column base beam: from near wall bracket to corridor
    _rhs_rect(ax, BLUE_IBC_Y - FRAME_RHS, 0,
              NEAR_COL_R - BLUE_IBC_Y + 2 * FRAME_RHS, FRAME_RHS, sx, sy)
    # Far column base beam: from corridor to far wall bracket
    _rhs_rect(ax, POST_FAR_YD, 0,
              IBC_FAR_Y + IBC_D - POST_FAR_YD + FRAME_RHS, FRAME_RHS, sx, sy)
    # Corridor cross-beam at base
    _rhs_rect(ax, NEAR_COL_R, 0,
              FAR_COL_L - NEAR_COL_R, FRAME_RHS, sx, sy, alpha=0.5)

    # ── Corridor uprights (front bay — shown as solid, cut section) ─────────
    # Near corridor upright
    _rhs_rect(ax, POST_NEAR_YD, 0, FRAME_RHS, TOP_Z, sx, sy,
              alpha=0.8, hatch="///")
    # Far corridor upright
    _rhs_rect(ax, POST_FAR_YD, 0, FRAME_RHS, TOP_Z, sx, sy,
              alpha=0.8, hatch="///")

    # ── Behind uprights (mid & back bays — shown lighter) ───────────────────
    for uyd in [POST_NEAR_YD, POST_FAR_YD]:
        for _ in range(2):  # mid and back bays
            ax.add_patch(Rectangle((sx(uyd + 5), sy(5)),
                                    sx(FRAME_RHS - 10), sy(TOP_Z - 10),
                                    fc="none", ec=C_DIM, lw=0.5, ls="--",
                                    zorder=4))

    # ── Platform beams (Z=PLATFORM_Z, transverse) ───────────────────────────
    # Near column platform beam
    _rhs_rect(ax, BLUE_IBC_Y - FRAME_RHS, PLATFORM_Z,
              NEAR_COL_R - BLUE_IBC_Y + 2 * FRAME_RHS, FRAME_RHS, sx, sy)
    # Far column platform beam
    _rhs_rect(ax, POST_FAR_YD, PLATFORM_Z,
              IBC_FAR_Y + IBC_D - POST_FAR_YD + FRAME_RHS, FRAME_RHS, sx, sy)
    # Corridor cross-beam at platform
    _rhs_rect(ax, NEAR_COL_R, PLATFORM_Z,
              FAR_COL_L - NEAR_COL_R, FRAME_RHS, sx, sy, alpha=0.5)

    # ── Top beams (Z=TOP_Z - FRAME_RHS, transverse) ────────────────────────
    top_beam_z = TOP_Z - FRAME_RHS
    # Near column top beam
    _rhs_rect(ax, BLUE_IBC_Y - FRAME_RHS, top_beam_z,
              NEAR_COL_R - BLUE_IBC_Y + 2 * FRAME_RHS, FRAME_RHS, sx, sy)
    # Far column top beam
    _rhs_rect(ax, POST_FAR_YD, top_beam_z,
              IBC_FAR_Y + IBC_D - POST_FAR_YD + FRAME_RHS, FRAME_RHS, sx, sy)
    # Corridor cross-beam at top
    _rhs_rect(ax, NEAR_COL_R, top_beam_z,
              FAR_COL_L - NEAR_COL_R, FRAME_RHS, sx, sy, alpha=0.5)

    # ── Anti-rotation lip on platform ───────────────────────────────────────
    lip_z = PLATFORM_Z + FRAME_RHS
    # Near column lip (corridor side)
    _rhs_rect(ax, POST_NEAR_YD + FRAME_RHS - LIP_T, lip_z,
              LIP_T, LIP_H, sx, sy, fc=C_WELD, alpha=0.5, lw=1.0)
    # Near column lip (wall side)
    _rhs_rect(ax, BLUE_IBC_Y - FRAME_RHS, lip_z,
              LIP_T, LIP_H, sx, sy, fc=C_WELD, alpha=0.5, lw=1.0)
    # Far column lip (corridor side)
    _rhs_rect(ax, POST_FAR_YD, lip_z,
              LIP_T, LIP_H, sx, sy, fc=C_WELD, alpha=0.5, lw=1.0)
    # Far column lip (wall side)
    _rhs_rect(ax, IBC_FAR_Y + IBC_D + FRAME_RHS - LIP_T, lip_z,
              LIP_T, LIP_H, sx, sy, fc=C_WELD, alpha=0.5, lw=1.0)

    # ── Rubber mat on platform ──────────────────────────────────────────────
    mat_z = PLATFORM_Z + FRAME_RHS
    # Near column mat
    _rhs_rect(ax, BLUE_IBC_Y, mat_z,
              IBC_D, MAT_T, sx, sy, fc=C_OUT, alpha=0.3, lw=0.8)
    # Far column mat
    _rhs_rect(ax, IBC_FAR_Y, mat_z,
              IBC_D, MAT_T, sx, sy, fc=C_OUT, alpha=0.3, lw=0.8)

    # ── Wall brackets ───────────────────────────────────────────────────────
    for wall_yd, side in [(0, 'near'), (FRAME_FOOTPRINT_W, 'far')]:
        for bz in [PLATFORM_Z, top_beam_z]:
            # Horizontal leg along wall
            if side == 'near':
                bx = wall_yd
                bw = BRACKET_L
            else:
                bx = wall_yd - BRACKET_L
                bw = BRACKET_L
            _rhs_rect(ax, bx, bz, bw, BRACKET_T, sx, sy,
                      fc=C_STEEL, alpha=0.5, lw=1.2)
            # Vertical leg
            if side == 'near':
                _rhs_rect(ax, bx, bz, BRACKET_T, FRAME_RHS, sx, sy,
                          fc=C_STEEL, alpha=0.5, lw=1.2)
            else:
                _rhs_rect(ax, bx + bw - BRACKET_T, bz, BRACKET_T, FRAME_RHS,
                          sx, sy, fc=C_STEEL, alpha=0.5, lw=1.2)
            # Gusset triangle
            if side == 'near':
                tri = Polygon([
                    (sx(bx + BRACKET_T), sy(bz + FRAME_RHS)),
                    (sx(bx + BRACKET_L), sy(bz + BRACKET_T)),
                    (sx(bx + BRACKET_T), sy(bz + BRACKET_T)),
                ], closed=True, fc=C_STEEL, ec=C_OUT, lw=0.8,
                   alpha=0.4, zorder=6)
            else:
                tri = Polygon([
                    (sx(bx + bw - BRACKET_T), sy(bz + FRAME_RHS)),
                    (sx(bx), sy(bz + BRACKET_T)),
                    (sx(bx + bw - BRACKET_T), sy(bz + BRACKET_T)),
                ], closed=True, fc=C_STEEL, ec=C_OUT, lw=0.8,
                   alpha=0.4, zorder=6)
            ax.add_patch(tri)
            # Bolt symbol
            bolt_yd = bx + 20 if side == 'near' else bx + bw - 20
            for bh in [bz + FRAME_RHS * 0.3, bz + FRAME_RHS * 0.7]:
                ax.plot(sx(bolt_yd), sy(bh), 'x', color=C_OUT,
                        ms=5, mew=1.5, zorder=8)

    # ── D-ring lashing points ───────────────────────────────────────────────
    dring_positions = []
    for uyd in [POST_NEAR_YD, POST_FAR_YD + FRAME_RHS]:
        for dz in [DRING_STANDOFF + DRING_SIZE,
                    PLATFORM_Z + DRING_STANDOFF + DRING_SIZE]:
            dring_positions.append((uyd, dz))

    for dyd, dz in dring_positions:
        # Mounting plate
        plate_w = DRING_SIZE + 20
        plate_h = DRING_SIZE + 20
        _rhs_rect(ax, dyd - plate_w / 2, dz - plate_h / 2,
                  plate_w, plate_h, sx, sy, fc=C_STEEL, alpha=0.4, lw=1.0)
        # D-ring (half-circle + horizontal base)
        r = DRING_SIZE / 2
        theta = np.linspace(0, np.pi, 30)
        ring_x = dyd + r * np.cos(theta)
        ring_y = dz + r * np.sin(theta)
        ax.plot([sx(v) for v in ring_x], [sy(v) for v in ring_y],
                color=C_OUT, lw=2.0, zorder=8)
        ax.plot([sx(dyd - r), sx(dyd + r)], [sy(dz), sy(dz)],
                color=C_OUT, lw=2.0, zorder=8)

    # ── Access gates (corridor face, H=0-300mm) ────────────────────────────
    for gate_yd in [POST_NEAR_YD + FRAME_RHS, POST_FAR_YD]:
        gate_w = -80 if gate_yd == POST_FAR_YD else 80
        # Gate outline (dashed = removable)
        ax.add_patch(Rectangle(
            (sx(min(gate_yd, gate_yd + gate_w)), sy(FRAME_RHS)),
            sx(abs(gate_w)), sy(GATE_H - FRAME_RHS),
            fc="none", ec=C_DIM, lw=1.5, ls="--", zorder=7))
        # Bolt positions
        for bz in [FRAME_RHS + 30, GATE_H - 30]:
            ax.plot(sx(gate_yd + gate_w / 2), sy(bz), 'o',
                    color=C_OUT, ms=4, mfc="white", mew=1.2, zorder=8)

    # Label access gates
    ax.text(sx(POST_NEAR_YD + FRAME_RHS + 90), sy(GATE_H / 2),
            "ACCESS\nGATE\n(REMOVABLE)",
            ha="left", va="center", fontsize=5.5, color=C_DIM,
            **FONT, zorder=10)

    # ── Weld symbols at key joints ──────────────────────────────────────────
    # Platform to upright joints
    for uyd in [POST_NEAR_YD + FRAME_RHS / 2, POST_FAR_YD + FRAME_RHS / 2]:
        _weld_tick(ax, uyd + FRAME_RHS / 2 + 3, PLATFORM_Z + FRAME_RHS / 2,
                   sx, sy, side='right')
    # Base joints
    for uyd in [POST_NEAR_YD + FRAME_RHS / 2, POST_FAR_YD + FRAME_RHS / 2]:
        _weld_tick(ax, uyd + FRAME_RHS / 2 + 3, FRAME_RHS / 2,
                   sx, sy, side='right')

    # ── Centerlines ─────────────────────────────────────────────────────────
    cl_yd = FRAME_FOOTPRINT_W / 2
    ax.plot([sx(cl_yd), sx(cl_yd)], [sy(Z_LO + 50), sy(TOP_Z + 100)],
            color=C_CL, lw=0.6, ls=(0, (8, 4, 2, 4)), zorder=3)
    ax.text(sx(cl_yd), sy(Z_LO + 40), "CL", ha="center", va="top",
            fontsize=6, color=C_CL, **FONT)

    # ── Dimensions ──────────────────────────────────────────────────────────
    # Overall width
    draw_dim_h(ax, sx(0), sx(FRAME_FOOTPRINT_W), sy(-120),
               f"{FRAME_FOOTPRINT_W}mm  FRAME WIDTH (WALL-TO-WALL)",
               offset=sy(5), fs=6, font=FONT)

    # Near column
    draw_dim_h(ax, sx(BLUE_IBC_Y), sx(NEAR_COL_R), sy(-60),
               f"{IBC_D}mm  IBC DEPTH",
               offset=sy(5), fs=5.5, font=FONT)

    # Corridor
    draw_dim_h(ax, sx(NEAR_COL_R), sx(FAR_COL_L), sy(-60),
               f"{CORRIDOR_W}mm\nCORRIDOR",
               offset=sy(5), fs=5.5, font=FONT)

    # Far column
    draw_dim_h(ax, sx(IBC_FAR_Y), sx(IBC_FAR_Y + IBC_D), sy(-60),
               f"{IBC_D}mm  IBC DEPTH",
               offset=sy(5), fs=5.5, font=FONT)

    # Heights (right side)
    dim_yd = IBC_FAR_Y + IBC_D + FRAME_RHS + 80
    draw_dim_v(ax, sx(dim_yd), sy(0), sy(PLATFORM_Z),
               f"{PLATFORM_Z}mm\nBOTTOM TIER",
               offset=sx(5), fs=5.5, right=True, font=FONT)
    draw_dim_v(ax, sx(dim_yd + 80), sy(0), sy(PLATFORM_Z + FRAME_RHS),
               f"{PLATFORM_Z + FRAME_RHS}mm\nPLATFORM TOP",
               offset=sx(5), fs=5.5, right=True, font=FONT)
    draw_dim_v(ax, sx(dim_yd + 160), sy(0), sy(TOP_Z),
               f"{TOP_Z}mm\nFRAME TOP",
               offset=sx(5), fs=5.5, right=True, font=FONT)

    # RHS member size
    draw_dim_h(ax, sx(POST_NEAR_YD), sx(POST_NEAR_YD + FRAME_RHS),
               sy(TOP_Z + 60),
               f"{FRAME_RHS}mm", offset=sy(5), fs=5.5, font=FONT)

    # Gate height
    draw_dim_v(ax, sx(BLUE_IBC_Y - FRAME_RHS - 60), sy(0), sy(GATE_H),
               f"{GATE_H}mm\nGATE",
               offset=sx(5), fs=5.5, font=FONT)

    # Lip height
    draw_dim_v(ax, sx(POST_NEAR_YD - 30), sy(PLATFORM_Z + FRAME_RHS),
               sy(PLATFORM_Z + FRAME_RHS + LIP_H),
               f"{LIP_H}mm\nLIP",
               offset=sx(5), fs=5.5, font=FONT)

    # ── Member labels ───────────────────────────────────────────────────────
    leader(ax, sx(NEAR_COL_R + FRAME_RHS / 2), sy(TOP_Z / 2),
           sx(NEAR_COL_R + 180), sy(TOP_Z / 2 + 150),
           "CORRIDOR UPRIGHT\n50×50×3 RHS\n(×6 TOTAL, 3 PER SIDE)",
           color=C_OUT, fs=5.5, ha="left", va="bottom",
           arrow_style="-|>", font=FONT)

    leader(ax, sx(BLUE_IBC_Y + IBC_D / 2), sy(PLATFORM_Z + FRAME_RHS / 2),
           sx(BLUE_IBC_Y - 100), sy(PLATFORM_Z + 200),
           "PLATFORM BEAM\n50×50×3 RHS\n(×6, 3 PER COLUMN)",
           color=C_OUT, fs=5.5, ha="right", va="bottom",
           arrow_style="-|>", font=FONT)

    leader(ax, sx(0), sy(PLATFORM_Z + FRAME_RHS / 2),
           sx(-100), sy(PLATFORM_Z + 300),
           "WALL BRACKET\n8mm PLATE + GUSSET\nM12 ANCHOR BOLTS\n(×4 PER WALL, ×8 TOTAL)",
           color=C_OUT, fs=5.5, ha="right", va="bottom",
           arrow_style="-|>", font=FONT)

    leader(ax, sx(POST_NEAR_YD + FRAME_RHS - LIP_T / 2),
           sy(PLATFORM_Z + FRAME_RHS + LIP_H / 2),
           sx(POST_NEAR_YD + 180), sy(PLATFORM_Z + FRAME_RHS + LIP_H + 100),
           "ANTI-ROTATION LIP\n5mm PLATE × 40mm HIGH\nFILLET WELDED TO PLATFORM",
           color=C_OUT, fs=5.5, ha="left", va="bottom",
           arrow_style="-|>", font=FONT)

    leader(ax, sx(POST_NEAR_YD), sy(DRING_STANDOFF + DRING_SIZE),
           sx(POST_NEAR_YD - 180), sy(DRING_STANDOFF + DRING_SIZE + 100),
           "D-RING LASHING\n25mm, 1,100kg WLL\n6mm PLATE, WELDED\n(×8 TOTAL, 4 PER TIER)",
           color=C_OUT, fs=5.5, ha="right", va="bottom",
           arrow_style="-|>", font=FONT)

    leader(ax, sx(NEAR_COL_R + CORRIDOR_W / 2), sy(FRAME_RHS / 2),
           sx(NEAR_COL_R + CORRIDOR_W / 2), sy(-180),
           f"CORRIDOR CROSS-BEAM\n50×50×3 RHS\n(×9, 3 PER LEVEL)",
           color=C_OUT, fs=5.5, ha="center", va="top",
           arrow_style="-|>", font=FONT)

    # ── Material note ───────────────────────────────────────────────────────
    mat_note_y = sy(Z_LO + 300)
    notes = [
        "MATERIAL & FABRICATION NOTES:",
        "",
        f"1. All RHS members: 50×50×3mm mild steel, A500 Grade B.",
        f"2. All joints fillet welded (5mm leg), continuous. Grind flush where noted.",
        f"3. Anti-rotation lip: 5mm × 40mm flat plate, fillet welded to platform beam top face.",
        f"4. Wall brackets: 8mm mild steel plate, triangular gusset. M12 anchor bolts to container wall ribs.",
        f"5. D-ring mounting: 6mm plate fillet welded to upright face. D-ring 25mm, WLL 1,100 kg (McMaster #3641T29).",
        f"6. Access gates: 300mm × 916mm clear, M12 bolts (×4 per gate). Two gates — one per column, corridor face.",
        f"7. Surface finish: grey oxide primer + flat black powder coat.",
        f"8. Anti-slip rubber mat: 12mm thick, 1,016 × 1,219mm (one per column on platform).",
        f"9. Total frame weight: ~90 kg.",
    ]
    for i, line in enumerate(notes):
        bold = i == 0
        ax.text(sx(YD_LO + 20), mat_note_y - i * sy(18), line,
                ha="left", va="top", fontsize=6.5 if bold else 5.5,
                color=C_OUT if bold else C_DIM,
                fontweight="bold" if bold else "normal",
                **FONT, zorder=15)

    # ── Title block ─────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 3",
                drawing_title="IBC SUPPORT FRAME",
                subtitle="FRONT ELEVATION — FRAME ASSEMBLY",
                scale_note="SCALE ~ 2.8:1 — ALL DIMS IN mm — VIEW ALONG X",
                height=0.05)

    fig.savefig("diagrams/ibc-frame-sheet1.png", dpi=130,
                bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/ibc-frame-sheet1.png"),
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
    S = 2.8

    def sx(mm): return mm * S
    def sy(mm): return mm * S

    X_LO = -300
    X_HI = FRAME_FOOTPRINT_D + 300
    Z_LO = -400
    Z_HI = TOP_Z + 300

    fig, ax = plt.subplots(figsize=(16, 18))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(sx(X_LO), sx(X_HI))
    ax.set_ylim(sy(Z_LO), sy(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text(sx(FRAME_FOOTPRINT_D / 2), sy(TOP_Z + 200),
            "SIDE ELEVATION — LOOKING ALONG Yd FROM NEAR WALL",
            ha="center", va="bottom", fontsize=9, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── Uprights (3 bays: front, mid, back) ─────────────────────────────────
    for fx in FX_POSTS:
        _rhs_rect(ax, fx, 0, FRAME_RHS, TOP_Z, sx, sy, alpha=0.8)

    # ── Longitudinal beams (connecting uprights at 3 levels) ────────────────
    beam_levels = [0, PLATFORM_Z, TOP_Z - FRAME_RHS]
    for bz in beam_levels:
        _rhs_rect(ax, FX_FRONT, bz, FRAME_FOOTPRINT_D, FRAME_RHS, sx, sy,
                  alpha=0.5)

    # ── Diagonal X-braces (bottom tier, both bays) ──────────────────────────
    for x1, x2 in [(FX_FRONT + FRAME_RHS, FX_MID),
                    (FX_MID + FRAME_RHS, FX_BACK)]:
        # Forward diagonal
        ax.plot([sx(x1), sx(x2)], [sy(FRAME_RHS), sy(PLATFORM_Z)],
                color=C_FRAME, lw=2.0, ls="-", alpha=0.5, zorder=4)
        # Backward diagonal
        ax.plot([sx(x1), sx(x2)], [sy(PLATFORM_Z), sy(FRAME_RHS)],
                color=C_FRAME, lw=2.0, ls="-", alpha=0.5, zorder=4)

    # ── Platform surface ────────────────────────────────────────────────────
    plat_z = PLATFORM_Z + FRAME_RHS
    # Rubber mat
    _rhs_rect(ax, FRAME_RHS, plat_z,
              FRAME_FOOTPRINT_D - 2 * FRAME_RHS, MAT_T, sx, sy,
              fc=C_OUT, alpha=0.3, lw=0.8)

    # ── Anti-rotation lip (front and back edges of platform) ────────────────
    # Front lip
    _rhs_rect(ax, FX_FRONT, plat_z, LIP_T, LIP_H, sx, sy,
              fc=C_WELD, alpha=0.5, lw=1.0)
    # Back lip
    _rhs_rect(ax, FRAME_FOOTPRINT_D - LIP_T, plat_z, LIP_T, LIP_H, sx, sy,
              fc=C_WELD, alpha=0.5, lw=1.0)

    # ── D-ring lashing points (on corridor upright face) ────────────────────
    for fx in [FX_FRONT, FX_BACK]:
        for dz_base in [DRING_STANDOFF, PLATFORM_Z + DRING_STANDOFF]:
            dz = dz_base + DRING_SIZE
            dx = fx + FRAME_RHS / 2
            # Mounting plate
            pw = DRING_SIZE + 20
            ph = DRING_SIZE + 20
            _rhs_rect(ax, dx - pw / 2, dz - ph / 2, pw, ph, sx, sy,
                      fc=C_STEEL, alpha=0.4, lw=1.0)
            # D-ring
            r = DRING_SIZE / 2
            theta = np.linspace(0, np.pi, 30)
            ring_x = dx + r * np.cos(theta)
            ring_y = dz + r * np.sin(theta)
            ax.plot([sx(v) for v in ring_x], [sy(v) for v in ring_y],
                    color=C_OUT, lw=2.0, zorder=8)
            ax.plot([sx(dx - r), sx(dx + r)], [sy(dz), sy(dz)],
                    color=C_OUT, lw=2.0, zorder=8)

    # ── Access gate outline (front bay, corridor face) ──────────────────────
    ax.add_patch(Rectangle((sx(FX_FRONT), sy(FRAME_RHS)),
                            sx(FRAME_RHS), sy(GATE_H - FRAME_RHS),
                            fc="none", ec=C_DIM, lw=1.5, ls="--", zorder=7))
    ax.text(sx(FX_FRONT + FRAME_RHS + 15), sy(GATE_H / 2),
            "ACCESS GATE", ha="left", va="center", fontsize=5.5,
            color=C_DIM, **FONT, zorder=10)

    # ── Weld symbols at upright/beam joints ─────────────────────────────────
    for fx in FX_POSTS:
        for bz in [FRAME_RHS, PLATFORM_Z + FRAME_RHS]:
            _weld_tick(ax, fx + FRAME_RHS + 3, bz, sx, sy, side='right')

    # ── Dimensions ──────────────────────────────────────────────────────────
    # Overall depth
    draw_dim_h(ax, sx(FX_FRONT), sx(FX_BACK + FRAME_RHS), sy(-120),
               f"{FRAME_FOOTPRINT_D}mm  FRAME DEPTH",
               offset=sy(5), fs=6, font=FONT)

    # Bay spacing
    draw_dim_h(ax, sx(FX_FRONT), sx(FX_MID), sy(-60),
               f"{FX_MID}mm", offset=sy(5), fs=5.5, font=FONT)
    draw_dim_h(ax, sx(FX_MID), sx(FX_BACK), sy(-60),
               f"{FX_BACK - FX_MID}mm", offset=sy(5), fs=5.5, font=FONT)

    # Heights (right side)
    dim_x = FRAME_FOOTPRINT_D + 80
    draw_dim_v(ax, sx(dim_x), sy(0), sy(PLATFORM_Z),
               f"{PLATFORM_Z}mm", offset=sx(5), fs=5.5, right=True, font=FONT)
    draw_dim_v(ax, sx(dim_x + 60), sy(PLATFORM_Z), sy(TOP_Z),
               f"{TOP_Z - PLATFORM_Z}mm", offset=sx(5), fs=5.5,
               right=True, font=FONT)
    draw_dim_v(ax, sx(dim_x + 120), sy(0), sy(TOP_Z),
               f"{TOP_Z}mm\nTOTAL", offset=sx(5), fs=5.5,
               right=True, font=FONT)

    # ── Member labels ───────────────────────────────────────────────────────
    leader(ax, sx(FX_MID + FRAME_RHS / 2), sy(TOP_Z / 2),
           sx(FX_MID + 200), sy(TOP_Z / 2 + 200),
           "CORRIDOR UPRIGHT\n50×50×3 RHS\nFLOOR TO TOP",
           color=C_OUT, fs=5.5, ha="left", va="bottom",
           arrow_style="-|>", font=FONT)

    leader(ax, sx(FRAME_FOOTPRINT_D / 2), sy(PLATFORM_Z + FRAME_RHS / 2),
           sx(FRAME_FOOTPRINT_D / 2 + 200), sy(PLATFORM_Z + 200),
           "LONGITUDINAL BEAM\n50×50×3 RHS\n(3 LEVELS × 2 = 6 TOTAL)",
           color=C_OUT, fs=5.5, ha="left", va="bottom",
           arrow_style="-|>", font=FONT)

    brace_cx = (FX_FRONT + FRAME_RHS + FX_MID) / 2
    brace_cz = (FRAME_RHS + PLATFORM_Z) / 2
    leader(ax, sx(brace_cx), sy(brace_cz),
           sx(brace_cx + 200), sy(brace_cz - 200),
           "X-BRACE\n50×50×3 RHS\n(×4 TOTAL,\n2 PER BAY,\nBOTTOM TIER ONLY)",
           color=C_OUT, fs=5.5, ha="left", va="top",
           arrow_style="-|>", font=FONT)

    # ── Notes ───────────────────────────────────────────────────────────────
    notes_y = sy(Z_LO + 300)
    notes = [
        "SIDE ELEVATION NOTES:",
        "",
        "1. Three upright bays at 642mm centers. X-braces in bottom-tier bays for racking resistance.",
        f"2. Platform at Z={PLATFORM_Z}mm supports upper-tier IBCs. 12mm rubber mat on top.",
        f"3. Frame depth {FRAME_FOOTPRINT_D}mm: 65mm overhang on cargo-door side, flush to end wall.",
        "4. D-ring lashing points at front and back uprights, both tiers (4 visible this side).",
        f"5. Access gate (300mm × 916mm clear opening) at front bay, corridor face only.",
        "6. Behind: second corridor upright row (identical) at 270mm offset toward far wall.",
    ]
    for i, line in enumerate(notes):
        bold = i == 0
        ax.text(sx(X_LO + 20), notes_y - i * sy(18), line,
                ha="left", va="top", fontsize=6.5 if bold else 5.5,
                color=C_OUT if bold else C_DIM,
                fontweight="bold" if bold else "normal",
                **FONT, zorder=15)

    # ── Title block ─────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 3",
                drawing_title="IBC SUPPORT FRAME",
                subtitle="SIDE ELEVATION — CORRIDOR STRUCTURE & X-BRACING",
                scale_note="SCALE ~ 2.8:1 — ALL DIMS IN mm — VIEW ALONG Yd",
                height=0.05)

    fig.savefig("diagrams/ibc-frame-sheet2.png", dpi=130,
                bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/ibc-frame-sheet2.png"),
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
    S = 2.8

    def px(mm): return mm * S
    def py(mm): return mm * S

    X_LO = -300
    X_HI = FRAME_FOOTPRINT_D + 300
    YD_LO = -300
    YD_HI = FRAME_FOOTPRINT_W + 300

    fig, ax = plt.subplots(figsize=(16, 20))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(px(X_LO), px(X_HI))
    ax.set_ylim(py(YD_LO), py(YD_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text(px(FRAME_FOOTPRINT_D / 2), py(FRAME_FOOTPRINT_W + 200),
            "PLAN VIEW — LOOKING DOWN AT PLATFORM LEVEL (Z=1,060mm)",
            ha="center", va="bottom", fontsize=9, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── Platform beams (cut at platform level) ──────────────────────────────
    # Longitudinal beams along X at corridor edges
    for post_yd in [POST_NEAR_YD, POST_FAR_YD]:
        _rhs_rect(ax, FX_FRONT, post_yd, FRAME_FOOTPRINT_D, FRAME_RHS,
                  px, py, alpha=0.7, hatch="///")

    # Transverse beams at each upright position
    for fx in FX_POSTS:
        # Near column beam (wall bracket to corridor)
        near_beam_start = BLUE_IBC_Y - FRAME_RHS
        near_beam_end_yd = POST_NEAR_YD + FRAME_RHS
        _rhs_rect(ax, fx, near_beam_start,
                  FRAME_RHS, near_beam_end_yd - near_beam_start,
                  px, py, alpha=0.6)

        # Far column beam (corridor to wall bracket)
        far_beam_start_yd = POST_FAR_YD
        far_beam_end_yd = IBC_FAR_Y + IBC_D + FRAME_RHS
        _rhs_rect(ax, fx, far_beam_start_yd,
                  FRAME_RHS, far_beam_end_yd - far_beam_start_yd,
                  px, py, alpha=0.6)

        # Corridor cross-beam
        _rhs_rect(ax, fx, POST_NEAR_YD + FRAME_RHS,
                  FRAME_RHS, POST_FAR_YD - POST_NEAR_YD - FRAME_RHS,
                  px, py, alpha=0.4)

    # ── Anti-rotation lip outline (perimeter of each platform bay) ──────────
    # Near column lip
    near_lip_x1 = FX_FRONT
    near_lip_x2 = FRAME_FOOTPRINT_D
    near_lip_y1 = BLUE_IBC_Y - FRAME_RHS
    near_lip_y2 = POST_NEAR_YD + FRAME_RHS
    ax.add_patch(Rectangle((px(near_lip_x1), py(near_lip_y1)),
                            px(near_lip_x2 - near_lip_x1),
                            py(near_lip_y2 - near_lip_y1),
                            fc="none", ec=C_WELD, lw=1.5, ls="-",
                            zorder=8))
    # Far column lip
    far_lip_y1 = POST_FAR_YD
    far_lip_y2 = IBC_FAR_Y + IBC_D + FRAME_RHS
    ax.add_patch(Rectangle((px(near_lip_x1), py(far_lip_y1)),
                            px(near_lip_x2 - near_lip_x1),
                            py(far_lip_y2 - far_lip_y1),
                            fc="none", ec=C_WELD, lw=1.5, ls="-",
                            zorder=8))

    # Label lips
    ax.text(px(FRAME_FOOTPRINT_D / 2), py(near_lip_y1 - 15),
            "ANTI-ROTATION LIP (5mm × 40mm PLATE, RED OUTLINE)",
            ha="center", va="top", fontsize=5, color=C_WELD, **FONT, zorder=10)

    # ── Rubber mats (dashed rectangles inside lip perimeter) ────────────────
    # Near column mat: IBC footprint on platform
    mat_x = FX_FRONT + FRAME_RHS  # inboard of front upright
    mat_w = FRAME_FOOTPRINT_D - 2 * FRAME_RHS
    near_mat_yd = BLUE_IBC_Y
    far_mat_yd = IBC_FAR_Y
    for mat_yd in [near_mat_yd, far_mat_yd]:
        ax.add_patch(Rectangle((px(mat_x), py(mat_yd)),
                                px(mat_w), py(IBC_D),
                                fc=C_OUT, ec=C_DIM, lw=1.0, ls="--",
                                alpha=0.1, zorder=6))
        ax.text(px(mat_x + mat_w / 2), py(mat_yd + IBC_D / 2),
                "12mm RUBBER MAT\n1,016 × 1,219mm",
                ha="center", va="center", fontsize=5.5, color=C_DIM,
                **FONT, zorder=10, alpha=0.7)

    # ── IBC footprint ghost outlines ────────────────────────────────────────
    for mat_yd in [near_mat_yd, far_mat_yd]:
        ibc_x = (FRAME_FOOTPRINT_D - IBC_W) / 2 + FX_FRONT  # centered in frame
        ax.add_patch(Rectangle((px(ibc_x), py(mat_yd)),
                                px(IBC_W), py(IBC_D),
                                fc="none", ec=C_CL, lw=0.8, ls=(0, (5, 5)),
                                alpha=0.4, zorder=7))

    # ── Corridor opening ────────────────────────────────────────────────────
    corr_x1 = FX_FRONT + FRAME_RHS
    corr_x2 = FRAME_FOOTPRINT_D - FRAME_RHS
    corr_y1 = POST_NEAR_YD + FRAME_RHS
    corr_y2 = POST_FAR_YD
    ax.add_patch(Rectangle((px(corr_x1), py(corr_y1)),
                            px(corr_x2 - corr_x1), py(corr_y2 - corr_y1),
                            fc=C_CL, ec="none", alpha=0.06, zorder=3))
    ax.text(px(FRAME_FOOTPRINT_D / 2), py((corr_y1 + corr_y2) / 2),
            f"CORRIDOR OPENING\n{CORRIDOR_W - 2 * FRAME_RHS}mm CLEAR",
            ha="center", va="center", fontsize=6, color=C_CL,
            fontweight="bold", **FONT, zorder=10)

    # ── Wall brackets (at near and far walls) ───────────────────────────────
    for fx in FX_POSTS:
        for wall_yd, side in [(0, 'near'), (FRAME_FOOTPRINT_W, 'far')]:
            if side == 'near':
                by = wall_yd
                bh = BRACKET_L
            else:
                by = wall_yd - BRACKET_L
                bh = BRACKET_L
            _rhs_rect(ax, fx, by, FRAME_RHS, bh, px, py,
                      fc=C_STEEL, alpha=0.4, lw=1.2)
            # Bolt positions
            bolt_x = fx + FRAME_RHS / 2
            for bolt_yd in [by + 25, by + bh - 25]:
                ax.plot(px(bolt_x), py(bolt_yd), 'x', color=C_OUT,
                        ms=5, mew=1.5, zorder=8)

    # ── Dimensions ──────────────────────────────────────────────────────────
    # Overall depth
    draw_dim_h(ax, px(FX_FRONT), px(FRAME_FOOTPRINT_D), py(-120),
               f"{FRAME_FOOTPRINT_D}mm  FRAME DEPTH",
               offset=py(5), fs=6, font=FONT)

    # Bay spacing
    draw_dim_h(ax, px(FX_FRONT), px(FX_MID), py(-60),
               f"{FX_MID}mm", offset=py(5), fs=5.5, font=FONT)
    draw_dim_h(ax, px(FX_MID), px(FX_BACK), py(-60),
               f"{FX_BACK - FX_MID}mm", offset=py(5), fs=5.5, font=FONT)

    # Overall width
    dim_x = FRAME_FOOTPRINT_D + 80
    draw_dim_v(ax, px(dim_x), py(0), py(FRAME_FOOTPRINT_W),
               f"{FRAME_FOOTPRINT_W}mm\nFRAME WIDTH",
               offset=px(5), fs=6, right=True, font=FONT)

    # Near column depth
    draw_dim_v(ax, px(dim_x + 80), py(BLUE_IBC_Y), py(NEAR_COL_R),
               f"{IBC_D}mm", offset=px(5), fs=5.5, right=True, font=FONT)

    # Corridor
    draw_dim_v(ax, px(dim_x + 80), py(NEAR_COL_R), py(FAR_COL_L),
               f"{CORRIDOR_W}mm", offset=px(5), fs=5.5, right=True, font=FONT)

    # Far column depth
    draw_dim_v(ax, px(dim_x + 80), py(IBC_FAR_Y), py(IBC_FAR_Y + IBC_D),
               f"{IBC_D}mm", offset=px(5), fs=5.5, right=True, font=FONT)

    # RHS member size
    draw_dim_h(ax, px(FX_FRONT), px(FX_FRONT + FRAME_RHS),
               py(FRAME_FOOTPRINT_W + 80),
               f"{FRAME_RHS}mm", offset=py(5), fs=5.5, font=FONT)

    # ── Detail inset: Corner Joint ──────────────────────────────────────────
    det_x = px(X_LO + 20)
    det_y = py(YD_LO + 10)
    det_w = px(350)
    det_h = py(280)
    ax.add_patch(Rectangle((det_x, det_y), det_w, det_h,
                            fc=C_DETAIL, ec=C_OUT, lw=1.5, zorder=12))
    ax.text(det_x + det_w / 2, det_y + det_h - py(10),
            "DETAIL A: TYPICAL CORNER JOINT (≈5:1)",
            ha="center", va="top", fontsize=6, color=C_OUT,
            fontweight="bold", **FONT, zorder=13)

    # Draw enlarged corner joint
    dsx = 4.0  # detail scale
    dcx = det_x + det_w * 0.4  # detail center X
    dcy = det_y + det_h * 0.45

    # Upright (vertical member, going up out of page — shown as cross-section)
    u_size = FRAME_RHS * dsx
    ax.add_patch(Rectangle((dcx - px(FRAME_RHS / 2 * dsx / S),
                             dcy - py(FRAME_RHS / 2 * dsx / S)),
                            px(FRAME_RHS * dsx / S),
                            py(FRAME_RHS * dsx / S),
                            fc=C_STEEL, ec=C_OUT, lw=1.8, zorder=13,
                            hatch="///", alpha=0.6))
    # Inner void
    ax.add_patch(Rectangle((dcx - px((FRAME_RHS / 2 - FRAME_T) * dsx / S),
                             dcy - py((FRAME_RHS / 2 - FRAME_T) * dsx / S)),
                            px((FRAME_RHS - 2 * FRAME_T) * dsx / S),
                            py((FRAME_RHS - 2 * FRAME_T) * dsx / S),
                            fc=BG, ec=C_OUT, lw=0.8, zorder=14))

    # Beam stub (horizontal, going right)
    beam_l = FRAME_RHS * 2 * dsx / S
    beam_h = FRAME_RHS * dsx / S
    beam_x = dcx + px(FRAME_RHS / 2 * dsx / S)
    beam_y = dcy - py(FRAME_RHS / 2 * dsx / S)
    ax.add_patch(Rectangle((beam_x, beam_y), px(beam_l), py(beam_h),
                            fc=C_STEEL, ec=C_OUT, lw=1.8, zorder=13,
                            hatch="\\\\\\", alpha=0.5))

    # Weld symbol
    wx = beam_x
    wy = dcy
    ax.plot([wx, wx + px(12)], [wy, wy + py(12)],
            color=C_WELD, lw=2.5, zorder=15)
    ax.plot([wx, wx + px(12)], [wy, wy - py(12)],
            color=C_WELD, lw=2.5, zorder=15)
    ax.text(wx + px(16), wy, "FILLET WELD\n5mm LEG\nCONTINUOUS",
            ha="left", va="center", fontsize=4.5, color=C_WELD,
            **FONT, zorder=15)

    # Labels
    ax.text(dcx, dcy + py(FRAME_RHS / 2 * dsx / S) + py(8),
            "UPRIGHT\n(CUT SECTION)", ha="center", va="bottom",
            fontsize=4.5, color=C_DIM, **FONT, zorder=15)
    ax.text(beam_x + px(beam_l / 2), beam_y - py(8),
            "BEAM", ha="center", va="top",
            fontsize=4.5, color=C_DIM, **FONT, zorder=15)

    # ── Detail inset: D-ring Mounting ───────────────────────────────────────
    det2_x = det_x + det_w + px(20)
    det2_y = det_y
    det2_w = px(350)
    det2_h = py(280)
    ax.add_patch(Rectangle((det2_x, det2_y), det2_w, det2_h,
                            fc=C_DETAIL, ec=C_OUT, lw=1.5, zorder=12))
    ax.text(det2_x + det2_w / 2, det2_y + det2_h - py(10),
            "DETAIL B: D-RING LASHING POINT (≈4:1)",
            ha="center", va="top", fontsize=6, color=C_OUT,
            fontweight="bold", **FONT, zorder=13)

    # Mounting plate
    d_dsx = 3.5
    d_cx = det2_x + det2_w * 0.5
    d_cy = det2_y + det2_h * 0.40
    plate_w_d = (DRING_SIZE + 30) * d_dsx / S
    plate_h_d = (DRING_SIZE + 30) * d_dsx / S
    ax.add_patch(Rectangle((d_cx - px(plate_w_d / 2), d_cy - py(plate_h_d / 2)),
                            px(plate_w_d), py(plate_h_d),
                            fc=C_STEEL, ec=C_OUT, lw=1.8, zorder=13,
                            alpha=0.5))

    # D-ring
    d_r = DRING_SIZE / 2 * d_dsx / S
    theta = np.linspace(0, np.pi, 40)
    d_ring_x = [d_cx + px(d_r * np.cos(t)) for t in theta]
    d_ring_y = [d_cy + py(d_r * np.sin(t)) for t in theta]
    ax.plot(d_ring_x, d_ring_y, color=C_OUT, lw=3.0, zorder=14)
    ax.plot([d_cx - px(d_r), d_cx + px(d_r)], [d_cy, d_cy],
            color=C_OUT, lw=3.0, zorder=14)

    # Pin hole
    ax.add_patch(Circle((d_cx, d_cy), px(3 * d_dsx / S),
                         fc=C_OUT, ec=C_OUT, lw=1.0, zorder=15))

    # Labels
    ax.text(d_cx, d_cy + py(d_r) + py(12),
            f"D-RING 25mm\nWLL {DRING_WLL} kg",
            ha="center", va="bottom", fontsize=4.5, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)
    ax.text(d_cx, d_cy - py(plate_h_d / 2) - py(8),
            "6mm MOUNTING PLATE\nFILLET WELDED TO UPRIGHT",
            ha="center", va="top", fontsize=4.5, color=C_DIM,
            **FONT, zorder=15)

    # ── Notes ───────────────────────────────────────────────────────────────
    notes_x = px(X_LO + 20)
    notes_y = py(YD_LO + 260)
    notes = [
        "PLAN VIEW NOTES:",
        "",
        "1. Plan cut at platform level (Z=1,060mm). All beams shown in cross-section (hatched).",
        "2. Longitudinal beams (along X) at corridor edges are continuous — front to back.",
        "3. Transverse beams (along Yd) at each upright bay: cantilever from corridor to wall bracket.",
        "4. Wall brackets bolted to container wall corrugation ribs (M12 anchor bolts, 2 per bracket).",
        "5. Anti-rotation lip (red outline): 5mm plate fillet welded to beam top face, full perimeter of each bay.",
        f"6. Rubber mat: 12mm anti-slip, trimmed to IBC footprint ({IBC_D} × {IBC_W}mm).",
        "7. Ghost outline (blue dashed): IBC cage footprint for reference.",
    ]
    for i, line in enumerate(notes):
        bold = i == 0
        ax.text(notes_x, notes_y - i * py(18), line,
                ha="left", va="top", fontsize=6.5 if bold else 5.5,
                color=C_OUT if bold else C_DIM,
                fontweight="bold" if bold else "normal",
                **FONT, zorder=15)

    # ── Title block ─────────────────────────────────────────────────────────
    title_block(ax, "SHEET 3 OF 3",
                drawing_title="IBC SUPPORT FRAME",
                subtitle="PLAN VIEW — PLATFORM BEAM LAYOUT & DETAILS",
                scale_note="SCALE ~ 2.8:1 — ALL DIMS IN mm — VIEW LOOKING DOWN",
                height=0.05)

    fig.savefig("diagrams/ibc-frame-sheet3.png", dpi=130,
                bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/ibc-frame-sheet3.png"),
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-frame-sheet3.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    os.makedirs("diagrams", exist_ok=True)
    print("Generating IBC support frame drawings...")
    sheet1()
    sheet2()
    sheet3()
    print("Done.")
