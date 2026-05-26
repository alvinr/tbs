#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_walkway_diagram.py  —  TBS-001 Perimeter Walkway

Sheet 1 — Plan view of walkway layout:
  Top-down view showing all 4 walkway sections with bracket positions.
  Left walkway shown as removable lift-out (no brackets — panel conflict).
  Right walkway brackets on angle iron welded to flat end wall.
  Panel transport envelope shown as dashed red zone.

Sheet 2 — Cross-section + bolt pattern (near walkway bracket):
  View A: Detail cross-section (~5:1) showing grated deck, wall-cantilevered
  bracket, tray rim clearance, and dimensional annotations.  Section cut
  looking along X axis.  Triangular gusset brackets bolted to container wall
  ribs — no legs, no beam, no floor contact.  Entire tray clear for film.
  View B: Plate face showing triangular 3× M12 bolt pattern.

Sheet 3 — Detail A: Right walkway ceiling-hung support (IBC end):
  300mm wide, same as near/far.  No floor contact — suspended from ceiling
  corrugations by M10 threaded rod hangers at 457mm centers.  Two 50×50×5mm
  steel angle bearers run full container width along Yd at X=4,329 and
  X=4,629.  Grating spans 300mm between bearers at Z=75mm (deck 100mm).
  5 hanger pairs, all at Yd < 2,025mm — clear of optical cone.  Near/far
  ends bear on adjacent walkway brackets.  Zero tray contact, zero floor
  contact.

Sheet 4 — Detail B: Left walkway butt joint and panel clearance:
  View looking along Yd (near wall toward far wall), X horizontal, Z vertical.
  Shows left walkway grating (X=170-470, removable lift-out) meeting near
  walkway bracket arm at butt joint (X=470). Panel transport envelope
  (X=0-420) shown as ghost, confirming 50mm clearance to near walkway.
  Bearing strip and support cradle shown in cross-section.

Sheet 5 — Detail C: Left walkway support system (removable):
  Elevation showing all support elements: floor-standing leg (X=140, on bare
  floor) with cantilever arm, bearer beam (50×50×3mm Al RHS at X=470) spanning
  1,762mm between bracket vertical legs, and bearing strip on tray rim (X=170).
  Zero processing tray contact.

Sheet 6 — Detail D: Bearer beam to bracket connection:
  Elevation at bracket showing how the bearer beam bolts to the bracket
  vertical leg via a welded end plate and 2× M10 wing bolts.  View looking
  along X (same as sheet 1).  Wing bolts allow tool-free removal.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Polygon
from matplotlib.lines import Line2D
import os
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_notes, draw_legend
from tbs_constants import (
    svg_path, SVG_DIR,
    C_LEN, C_WID, C_HGT,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_W, PROC_TRAY_D,
    PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR, PROC_TRAY_RIM,
    WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T, WALKWAY_RIGHT_W,
    WALKWAY_BRACKET_H, WALKWAY_BRACKET_T, WALKWAY_BRACKET_SPACING,
    WALKWAY_RIGHT_BEARER_SIZE, WALKWAY_RIGHT_BEARER_T,
    WALKWAY_RIGHT_HANGER_D, WALKWAY_RIGHT_HANGER_N, WALKWAY_RIGHT_HANGER_Y1, WALKWAY_RIGHT_HANGER_L,
    WALKWAY_RIGHT_CEIL_PLATE,
    WALKWAY_LEFT_SPAN, IBC_COL_X, IBC_W, IBC_H_600,
    CONTAINER_RIB_SPACING,
    WALKWAY_NEAR_YD, WALKWAY_FAR_YD, WALKWAY_LEFT_X, WALKWAY_RIGHT_X,
    PROC_OPEN_X_L, PROC_OPEN_X_R, PROC_OPEN_YD_N, PROC_OPEN_YD_F,
    PROC_OPEN_AREA,
    PANEL_SLIDE, PANEL_CENTER_T, PANEL_FLOOR_GAP,
    LEFT_WK_BEARER_SIZE, LEFT_WK_BEARER_T,
    LEFT_WK_LEG_N, LEFT_WK_LEG_SIZE, LEFT_WK_LEG_T, LEFT_WK_LEG_BASE,
    LEFT_WK_BEARING_STRIP,
    WALKWAY_NEAR_WIDE_W, WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_X_R,
    SPRAY_BAR_SLIT_W,
    EP_X, EP_W, BA_X, BA_W,
    EVAP_W, EVAP_D, EVAP_H, EVAP_STOW_X, EVAP_STOW_YD,
)

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
C_BRKT  = "#707888"   # bracket fill
FONT    = {"fontfamily": "monospace"}


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Cross-Section + Bolt Pattern
#
# Two-panel layout:
#   VIEW A (left): Cross-section looking along X at a bracket position.
#     Horizontal = Yd (0 = pinhole wall, positive toward far wall)
#     Vertical   = Z  (0 = floor, positive up)
#   VIEW B (right): Plate face looking along −Yd — shows triangular
#     bolt pattern on vertical mounting plate with gusset footprint.
# Scale ≈ 5:1 for clarity.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():
    def sx(mm): return mm
    def sy(mm): return mm

    # ── Structural dimensions (mm real) ──────────────────────────────────────
    TRAY_WALL  = 3     # tray wall thickness (SS)
    TRAY_FLOOR = 2     # tray floor thickness (SS)
    CORR_DEPTH = 38    # corrugation depth (mm)
    WALL_T     = 1.6   # wall steel thickness (mm)
    BRKT_ARM_H = WALKWAY_H - WALKWAY_GRATE_T  # = 75mm (bracket arm top Z)
    BRKT_T     = WALKWAY_BRACKET_T  # 8mm plate thickness
    BRKT_VERT  = WALKWAY_BRACKET_H  # 150mm vertical leg on wall
    REINF_W    = 100   # reinforcing plate width (covers triangular bolt pattern)
    REINF_H    = 180   # reinforcing plate height
    REINF_T    = 6     # reinforcing plate thickness

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
    ax.set_xlim(sx(YD_LO), sx(YD_HI))
    ax.set_ylim(sy(Z_LO), sy(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # View A title
    ax.text(sx(YD_HI / 2), sy(Z_HI - 5),
            "VIEW A — CROSS-SECTION AT BRACKET (LOOKING ALONG X)",
            ha="center", va="top", fontsize=8, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── Container floor ──────────────────────────────────────────────────────
    ax.add_patch(Rectangle((sx(YD_LO), sy(-15)), sx(YD_HI - YD_LO), sy(15),
                            fc=C_FLOOR, ec=C_OUT, lw=1.0, hatch="///", zorder=2))

    # ── Corrugated wall (cross-section through rib — HOLLOW profile) ─────────
    # Matching sheet 3 convention: exterior panel, air gap, rib side walls, rib face
    wall_z_top = Z_HI
    ext_panel_yd = -CORR_DEPTH - WALL_T

    # Exterior wall steel panel (full height)
    ax.add_patch(Rectangle((sx(ext_panel_yd), sy(0)),
                            sx(WALL_T), sy(wall_z_top),
                            fc="#909098", ec=C_OUT, lw=1.2, zorder=3,
                            hatch="///"))
    # Rib side wall (connecting exterior panel to rib face)
    ax.add_patch(Rectangle((sx(-CORR_DEPTH), sy(0)),
                            sx(WALL_T), sy(wall_z_top),
                            fc="#909098", ec=C_OUT, lw=0.8, zorder=3,
                            hatch="///"))
    # Rib interior face (flange — where bracket bolts on)
    ax.add_patch(Rectangle((sx(-WALL_T), sy(0)),
                            sx(WALL_T), sy(wall_z_top),
                            fc="#909098", ec=C_OUT, lw=1.2, zorder=3,
                            hatch="///"))
    # Air gap inside the rib (light fill to show it's hollow)
    ax.add_patch(Rectangle((sx(-CORR_DEPTH + WALL_T), sy(0)),
                            sx(CORR_DEPTH - 2 * WALL_T), sy(wall_z_top),
                            fc="#F0F0F0", ec="none", lw=0, zorder=2))
    ax.add_patch(Rectangle((sx(-CORR_DEPTH + WALL_T), sy(0)),
                            sx(CORR_DEPTH - 2 * WALL_T), sy(wall_z_top),
                            fc="none", ec=C_DIM, lw=0.5, ls="--", zorder=3))
    ax.text(sx(-CORR_DEPTH / 2), sy(wall_z_top * 0.45),
            "AIR\nGAP",
            ha="center", va="center", fontsize=6, color=C_DIM,
            **FONT, zorder=15, style="italic")
    # Rib face (interior surface at Yd=0)
    ax.plot([sx(0), sx(0)], [sy(0), sy(wall_z_top)],
            color=C_OUT, lw=2.0, zorder=4)
    ax.text(sx(-CORR_DEPTH / 2), sy(wall_z_top - 8),
            "CORRUGATED\nWALL RIB\n(1.6mm CORTEN\nHOLLOW PROFILE)",
            ha="center", va="top", fontsize=5.5, color=C_DIM,
            fontweight="bold", **FONT, zorder=15)

    # ── Reinforcing plate (bonded to exterior wall face) ─────────────────────
    reinf_yd = ext_panel_yd - REINF_T
    ax.add_patch(Rectangle((sx(reinf_yd), sy(0)),
                            sx(REINF_T), sy(REINF_H),
                            fc="#C08040", ec=C_OUT, lw=1.0, zorder=4))
    leader(ax, sx(reinf_yd - 1), sy(REINF_H * 0.8),
           sx(reinf_yd - 25), sy(REINF_H),
           f"REINFORCING\nPLATE\n{REINF_W}\u00d7{REINF_H}\n\u00d7{REINF_T}mm\n(EXTERIOR)",
           color="#C08040", fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Processing tray ──────────────────────────────────────────────────────
    # Tray near rim (vertical wall at Yd=TRAY_RIM_YD)
    ax.add_patch(Rectangle((sx(TRAY_RIM_YD - TRAY_WALL), sy(0)),
                            sx(TRAY_WALL), sy(PROC_TRAY_RIM),
                            fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=4))
    # Tray floor (extends inward from rim)
    tray_floor_start = TRAY_RIM_YD
    tray_floor_end = YD_HI - 20
    ax.add_patch(Rectangle((sx(tray_floor_start), sy(0)),
                            sx(tray_floor_end - tray_floor_start), sy(TRAY_FLOOR),
                            fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))
    # Tray rim label
    leader(ax, sx(TRAY_RIM_YD - 5), sy(PROC_TRAY_RIM / 2 + 20),
           sx(TRAY_RIM_YD - 20), sy(PROC_TRAY_RIM - 20),
           f"TRAY RIM\n{PROC_TRAY_RIM}mm\n(304 SS, 3mm)", color=C_TRAY, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)
    # Sawtooth break line on tray floor (continues right)
    bx = sx(tray_floor_end)
    z_lo, z_hi = 0, TRAY_FLOOR
    zz = np.linspace(z_lo, z_hi, 5)
    ax.plot([bx - 3, bx + 3, bx - 3, bx + 3, bx - 3],
            zz, color=C_OUT, lw=1.0, zorder=5)

    # Tray "water level" indication (wavy line at ~15mm)
    water_h = 15
    wave_x = np.linspace(sx(TRAY_RIM_YD + 5), sx(tray_floor_end - 10), 40)
    wave_y = sy(water_h) + 3 * np.sin(wave_x * 0.08)
    ax.plot(wave_x, wave_y, color="#4080C0", lw=1.0, alpha=0.6, zorder=4)
    ax.text(sx(TRAY_RIM_YD + 60), sy(water_h + 5),
            "PROCESS WATER\n(~15mm depth)",
            ha="left", va="bottom", fontsize=5.5, color="#4080C0",
            **FONT, alpha=0.7, zorder=15)

    # ── Cantilever bracket (3-piece: vertical plate + arm + gusset underneath) ─
    # The bracket is three welded pieces:
    #   1. Vertical mounting plate: flat against wall, Z=0 to BRKT_VERT (150mm)
    #      — bolted to wall rib, does NOT project into tray zone
    #   2. Horizontal arm: welded to vertical plate at Z=BRKT_ARM_H (75mm),
    #      projects inward 300mm — ABOVE the 50mm tray rim
    #   3. Gusset underneath the arm: right triangle bracing the arm from below,
    #      extends 70mm from wall (stops before tray rim at Yd=80mm).
    #      Vertices: wall/floor (0,0), wall/arm-bottom (0, arm_bot), (70, arm_bot).

    brkt_arm_z = BRKT_ARM_H  # = 75mm (top of horizontal arm = grate support)
    ARM_DEPTH  = BRKT_T + 2  # arm cross-section depth shown (visual thickness)
    arm_bot    = brkt_arm_z - ARM_DEPTH  # bottom of arm
    GUSSET_REACH = 70  # gusset extends 70mm from wall (< 80mm tray rim position)

    # 1. Vertical mounting plate (flat against rib interior face, Yd=0 to BRKT_T)
    ax.add_patch(Rectangle((sx(0), sy(0)),
                            sx(BRKT_T), sy(BRKT_VERT),
                            fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=6, alpha=0.85))

    # 2. Horizontal arm (projects inward at Z=brkt_arm_z)
    ax.add_patch(Rectangle((sx(0), sy(arm_bot)),
                            sx(WALKWAY_W), sy(ARM_DEPTH),
                            fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=6, alpha=0.85))
    # Arm top surface (where grate sits) — emphasize
    ax.plot([sx(0), sx(WALKWAY_W)], [sy(brkt_arm_z), sy(brkt_arm_z)],
            color=C_OUT, lw=2.0, zorder=7)

    # 3. Gusset UNDERNEATH the arm — right triangle bracing from below
    # Stops at Yd=70mm, before the tray rim at Yd=80mm
    gusset_verts = [
        (sx(0), sy(0)),                   # wall at floor level
        (sx(0), sy(arm_bot)),             # wall at arm bottom
        (sx(GUSSET_REACH), sy(arm_bot)),  # 70mm out along arm bottom
    ]
    ax.add_patch(Polygon(gusset_verts, closed=True,
                         fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=5, alpha=0.85))
    # Diagonal edge emphasis (hypotenuse)
    ax.plot([sx(0), sx(GUSSET_REACH)], [sy(0), sy(arm_bot)],
            color=C_OUT, lw=1.5, zorder=6)

    # Weld symbol at gusset-to-arm joint
    weld_x = GUSSET_REACH / 3
    ax.plot([sx(weld_x - 4), sx(weld_x), sx(weld_x + 4)],
            [sy(arm_bot), sy(arm_bot - 5), sy(arm_bot)],
            color="#CC4400", lw=1.5, zorder=8)
    ax.text(sx(weld_x), sy(arm_bot - 7), "WELD",
            ha="center", va="top", fontsize=4.5, color="#CC4400",
            **FONT, zorder=15)

    # Through-bolts (3× M12) — horizontal shanks through wall + bracket
    # Triangular pattern: 2× at Z=35 (flanking gusset in X), 1× at Z=120 (centered)
    # In this side view (along X), the two Z=35 bolts overlap — shown as one + "2×" label
    BOLT_D    = 12
    BOLT_R    = BOLT_D / 2
    BOLT_HEAD = 8    # hex head height (Yd direction)
    NUT_H     = 10   # nut height (Yd direction)
    WASHER_T  = 3
    C_BOLT    = "#505058"
    bolt_z_lo = 35   # lower pair — flanking gusset in X, ±27mm from CL
    bolt_z_hi = 120  # upper single — above grating deck (Z=100), on gusset CL

    for bz in [bolt_z_lo, bolt_z_hi]:
        shank_hw = BOLT_R * 0.4  # half-width of shank in Z
        # Bolt shank — from reinf plate through to bracket face
        ax.add_patch(Rectangle((sx(reinf_yd), sy(bz - shank_hw)),
                                sx(BRKT_T - reinf_yd), sy(shank_hw * 2),
                                fc=C_BOLT, ec=C_OUT, lw=0.8, zorder=10))
        # Hex head on exterior side (left of reinforcing plate)
        ax.add_patch(Rectangle((sx(reinf_yd - BOLT_HEAD), sy(bz - BOLT_R)),
                                sx(BOLT_HEAD), sy(BOLT_D),
                                fc=C_BOLT, ec=C_OUT, lw=1.0, zorder=10))
        # Washer under head
        ax.add_patch(Rectangle((sx(reinf_yd - WASHER_T), sy(bz - BOLT_R - 1)),
                                sx(WASHER_T), sy(BOLT_D + 2),
                                fc="#808080", ec=C_OUT, lw=0.5, zorder=9))
        # Nut on interior side (right of bracket plate)
        ax.add_patch(Rectangle((sx(BRKT_T), sy(bz - BOLT_R)),
                                sx(NUT_H), sy(BOLT_D),
                                fc=C_BOLT, ec=C_OUT, lw=1.0, zorder=10))
        # Washer under nut
        ax.add_patch(Rectangle((sx(BRKT_T), sy(bz - BOLT_R - 1)),
                                sx(WASHER_T), sy(BOLT_D + 2),
                                fc="#808080", ec=C_OUT, lw=0.5, zorder=9))

    # Bracket label — point at the arm
    leader(ax, sx(WALKWAY_W * 0.4), sy(brkt_arm_z - 5),
           sx(WALKWAY_W * 0.4 + 50), sy(brkt_arm_z - 30),
           f"CANTILEVER BRACKET\n{BRKT_T}mm STEEL PLATE\n(VERT PLATE + ARM\n+ GUSSET UNDER)",
           color=C_BRKT, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # Gusset label
    leader(ax, sx(GUSSET_REACH / 2), sy(arm_bot / 2 - 5),
           sx(GUSSET_REACH-20), sy(arm_bot / 2 - 25),
           f"GUSSET ({GUSSET_REACH}mm)\nSTOPS BEFORE\nTRAY RIM",
           color=C_BRKT, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # Bolt labels
    leader(ax, sx(reinf_yd - BOLT_HEAD - 2), sy(bolt_z_lo),
           sx(reinf_yd - 30), sy(bolt_z_lo + 20),
           f"2\u00d7 M12 AT Z={bolt_z_lo}\n(STRADDLE GUSSET\nIN X \u2014 SEE VIEW B)",
           color=C_DIM, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)
    leader(ax, sx(reinf_yd - BOLT_HEAD - 2), sy(bolt_z_hi),
           sx(reinf_yd - 30), sy(bolt_z_hi + 20),
           f"1\u00d7 M12 AT Z={bolt_z_hi}\n(ON GUSSET CL\nIN X \u2014 SEE VIEW B)",
           color=C_DIM, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Grated deck ──────────────────────────────────────────────────────────
    # Grating sits on bracket arm: bottom at BRKT_ARM_H (75mm), top at WALKWAY_H (100mm)
    grate_bot = brkt_arm_z  # = 75mm
    grate_top = grate_bot + WALKWAY_GRATE_T  # = 100mm = WALKWAY_H
    ax.add_patch(Rectangle((sx(0), sy(grate_bot)),
                            sx(WALKWAY_W), sy(WALKWAY_GRATE_T),
                            fc=C_GRATE, ec=C_OUT, lw=1.2, zorder=7))
    # Grate pattern (vertical bars in cross-section)
    bar_spacing = 34.2  # ~34mm bearing bar pitch (standard)
    bar_w = 3           # bearing bar thickness
    for yd in np.arange(bar_w, WALKWAY_W - bar_w, bar_spacing):
        ax.add_patch(Rectangle((sx(yd), sy(grate_bot)),
                                sx(bar_w), sy(WALKWAY_GRATE_T),
                                fc="#909098", ec=C_OUT, lw=0.3, zorder=8))
    # Cross bars (twist-locked — shown as small rectangles at mid-height)
    cross_h = 3
    for yd in np.arange(bar_spacing / 2, WALKWAY_W, bar_spacing):
        ax.add_patch(Rectangle((sx(yd - 1), sy(grate_bot + WALKWAY_GRATE_T / 2 - cross_h / 2)),
                                sx(2), sy(cross_h),
                                fc="#808088", ec="none", zorder=9, alpha=0.7))

    leader(ax, sx(WALKWAY_W / 4), sy((grate_bot + grate_top) / 2),
           sx(WALKWAY_W / 4 - 30), sy(grate_top + 40),
           f"PRESS-LOCKED STEEL GRATING\n{WALKWAY_GRATE_T}mm THICK \u00b7 GALVANIZED",
           color=C_OUT, fs=6, ha="center", va="center",
           arrow_style="-|>", font=FONT)

    # ── Grating clip (innermost edge, closest to processing tray) ──────────
    clip_yd = WALKWAY_W - 20
    clip_w = 8
    clip_below = 12   # extends below arm top
    clip_above = 5    # extends above grate top
    clip_bot = brkt_arm_z - clip_below
    clip_top = grate_top + clip_above
    ax.add_patch(Rectangle((sx(clip_yd), sy(clip_bot)),
                            sx(clip_w), sy(clip_top - clip_bot),
                            fc="#505058", ec=C_OUT, lw=0.8, zorder=9))
    leader(ax, sx(clip_yd + clip_w), sy(brkt_arm_z),
           sx(clip_yd + 30), sy(brkt_arm_z + 55),
           "GRATING CLIP\n(REMOVABLE)", color="#505058", fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Clear tray area annotation ───────────────────────────────────────────
    # Arrow showing clear air under the entire walkway — no legs, no beam
    clr_x = sx(WALKWAY_W * 0.7)
    ax.annotate("", xy=(clr_x, sy(TRAY_FLOOR + 1)), xytext=(clr_x, sy(brkt_arm_z - 1)),
                arrowprops=dict(arrowstyle="<->", color="#208020", lw=1.2, mutation_scale=8))
    gap_mm = brkt_arm_z - TRAY_FLOOR
    ax.text(clr_x + sx(5), sy((TRAY_FLOOR + brkt_arm_z) / 2),
            f"{gap_mm:.0f}mm\nCLEAR AIR\n(NO LEGS,\nNO BEAM —\nFILM LAYS\nFLAT HERE)",
            ha="left", va="center", fontsize=5, color="#208020",
            fontweight="bold", **FONT, zorder=15, alpha=0.8)

    # ── Dimension lines ──────────────────────────────────────────────────────
    # Walkway width (= bracket arm cantilever)
    draw_dim_h(ax, sx(0), sx(WALKWAY_W), sy(grate_top + 55),
               f"{WALKWAY_W}mm WALKWAY WIDTH", offset=sy(8), fs=7, font=FONT)

    # Deck height (floor to grate top)
    draw_dim_v(ax, sx(WALKWAY_W + 20), sy(0), sy(grate_top),
               f"{WALKWAY_H}mm\nDECK TOP", offset=sx(8), fs=7, right=True, font=FONT)

    # Grate thickness
    draw_dim_v(ax, sx(WALKWAY_W + 5), sy(grate_bot), sy(grate_top),
               f"{WALKWAY_GRATE_T}mm DECK\nHEIGHT", offset=sx(8), fs=6.5, right=True, font=FONT)

    # Bracket vertical leg height
    draw_dim_v(ax, sx(reinf_yd - BOLT_HEAD - 45), sy(0), sy(BRKT_VERT),
               f"{BRKT_VERT}mm\nVERT LEG", offset=sx(8), fs=6.5, right=False, font=FONT)

    # Bracket arm height
    draw_dim_v(ax, sx(WALKWAY_W + 5), sy(0), sy(brkt_arm_z),
               f"{brkt_arm_z}mm ARM TOP", offset=sx(8), fs=6.5, right=True, font=FONT)

    # Tray rim height
    draw_dim_v(ax, sx(TRAY_RIM_YD + 15), sy(0), sy(PROC_TRAY_RIM),
               f"{PROC_TRAY_RIM}mm", offset=sx(8), fs=6.5, right=True,
               color=C_TRAY, font=FONT)

    # Clearance above rim (grate bottom to rim top)
    clr = grate_bot - PROC_TRAY_RIM
    draw_dim_v(ax, sx(TRAY_RIM_YD + 15), sy(PROC_TRAY_RIM), sy(grate_bot),
               f"{clr}mm\nCLR", offset=sx(8), fs=6.5, right=True,
               color="#208020", font=FONT)

    # Corrugation depth
    draw_dim_h(ax, sx(-CORR_DEPTH), sx(0), sy(-22),
               f"{CORR_DEPTH}mm\nCORR", offset=sy(10), fs=6, above=False, font=FONT)

    # Wall to tray rim
    draw_dim_h(ax, sx(0), sx(TRAY_RIM_YD), sy(-35),
               f"{TRAY_RIM_YD}mm", offset=sy(10), fs=6, above=False, font=FONT)

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
            (sx(s_yd), sy(shoe_z)), sx(SHOE_W), sy(SHOE_H),
            fc="#FFD700", ec="#B89600", lw=0.6,
            zorder=10, alpha=0.3, ls="--"))

    # Shoe length annotation (into-page dimension, since shoes point along X)
    ax.text(sx(WALKWAY_W / 2), sy(shoe_z + SHOE_H + 6),
            "US 9 SHOE PAIR\n(270mm LONG \u00d7 100mm WIDE)",
            ha="center", va="bottom", fontsize=5.5, color="#404040",
            **FONT, zorder=15, alpha=0.7)
    leader(ax, sx(shoe_start + SHOE_W / 2), sy(shoe_z + SHOE_H),
           sx(95), sy(shoe_z + SHOE_H + 15),
           "OPERATOR\nSTANDING", color=C_TRAY, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Axis labels ──────────────────────────────────────────────────────────
    ax.text(sx(YD_HI / 2), sy(Z_LO + 5),
            "Yd  (container width, 0 = pinhole wall)  \u2192",
            ha="center", va="bottom", fontsize=6.5, color=C_DIM,
            **FONT, zorder=15, style="italic")

    # ── Notes ────────────────────────────────────────────────────────────────
    notes_x = sx(WALKWAY_W + 40)
    notes_top = sy(Z_HI - 10)
    notes = [
        "CONSTRUCTION NOTES:",
        "",
        f"1. Grating: {WALKWAY_GRATE_T}mm press-locked galvanized steel,",
        f"   30\u00d73mm bearing bars at 34.2mm pitch.",
        f"2. Cantilever brackets: {BRKT_T}mm steel plate gusset,",
        f"   bolted to wall ribs at {WALKWAY_BRACKET_SPACING}mm centers.",
        f"3. Rib is HOLLOW — bolt bridges the air gap.",
        f"   Path: head \u2192 reinf plate \u2192 ext panel",
        f"   \u2192 air gap \u2192 rib face \u2192 bracket \u2192 nut.",
        f"4. Reinforcing plate welded to exterior panel",
        f"   face. Bearing surface for bolt head + washer.",
        f"5. Gusset reach stops before tray rim at",
        f"   {PROC_TRAY_YD_NEAR}mm.",
        f"6. NO legs, NO beam — entire tray floor clear",
        f"   for film loading. Zero tray contact.",
        f"7. Grating clips to bracket arms — removable.",
        f"8. Right walkway: CEILING-HUNG from M{WALKWAY_RIGHT_HANGER_D}",
        f"   threaded rod hangers. See Sheet 3.",
        f"9. Left walkway: REMOVABLE LIFT-OUT —",
        f"   no brackets (panel conflict). Rests on",
        f"   near/far butt joints. {WALKWAY_GRATE_T}mm grating.",
    ]
    draw_notes(ax, notes, notes_x, notes_top, spacing=sy(6), fs=7, width=sx(130), font=FONT)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 6",
                drawing_title="PERIMETER WALKWAY",
                subtitle="CROSS-SECTION + BOLT PATTERN \u2014 NEAR WALKWAY BRACKET DETAIL",
                scale_note="AXES IN mm \u00b7 VIEW A: SECTION ALONG X / VIEW B: PLATE FACE (\u2212Yd)",
                height=0.07)

    # ══════════════════════════════════════════════════════════════════════════
    # VIEW B — Plate face (looking along −Yd, toward wall)
    # Horizontal = X (bracket width), Vertical = Z (height)
    # Shows triangular bolt pattern on the vertical mounting plate
    # ══════════════════════════════════════════════════════════════════════════
    ax2.set_facecolor(BG)

    BOLT_X_OFF = 27
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

    ax2.add_patch(Rectangle((pl2, arm_bot), REINF_W, ARM_DEPTH,
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
           pl2 - 8, bolt_z_lo - 10,
           f"BOLT 1\nM12 ({HOLE_D}mm CLR)",
           color=C_BOLT, fs=5.5,
           ha="right", va="top", arrow_style="-|>", font=FONT)
    leader(ax2, BOLT_X_OFF + HOLE_R_B + 1, bolt_z_lo,
           pr2 + 8, bolt_z_lo - 10,
           f"BOLT 2\nM12 ({HOLE_D}mm CLR)",
           color=C_BOLT, fs=5.5,
           ha="left", va="top", arrow_style="-|>", font=FONT)
    leader(ax2, 0, bolt_z_hi + HOLE_R_B + 1,
           0, bolt_z_hi + 25,
           f"BOLT 3 — M12 ({HOLE_D}mm CLR)\nON GUSSET CL",
           color=C_BOLT, fs=5.5,
           ha="center", va="bottom", arrow_style="-|>", font=FONT)

    dim_x2 = pl2 - 30
    draw_dim_v(ax2, dim_x2, 0, bolt_z_lo,
               f"{bolt_z_lo}mm", offset=8, fs=6.5, right=False, font=FONT)
    draw_dim_v(ax2, dim_x2, bolt_z_lo, bolt_z_hi,
               f"{bolt_z_hi - bolt_z_lo}mm", offset=8, fs=6.5, right=False, font=FONT)
    draw_dim_v(ax2, dim_x2, bolt_z_hi, BRKT_VERT,
               f"{BRKT_VERT - bolt_z_hi}mm", offset=8, fs=6.5, right=False, font=FONT)

    draw_dim_h(ax2, -BOLT_X_OFF, BOLT_X_OFF, bolt_z_lo - 22,
               f"{BOLT_X_OFF * 2}mm", offset=6, fs=6.5, above=False, font=FONT)

    draw_dim_h(ax2, pl2, pr2, -28,
               f"{REINF_W}mm PLATE", offset=6, fs=6, above=False, font=FONT)
    draw_dim_v(ax2, dim_x2 - 18, 0, BRKT_VERT,
               f"{BRKT_VERT}mm", offset=8, fs=6, right=False, font=FONT)

    ax2.text(cx2, BRKT_VERT + 8,
             f"MOUNTING PLATE\n{BRKT_T}mm STEEL · {REINF_W}×{BRKT_VERT}mm",
             ha="center", va="bottom", fontsize=6.5, color=C_BRKT,
             fontweight="bold", **FONT, zorder=15)

    notes_b = [
        "BOLT PATTERN NOTES:",
        f"1. Triangular pattern: 2 lower + 1 upper.",
        f"2. Lower pair at Z={bolt_z_lo}mm, X=±{BOLT_X_OFF}mm",
        f"   from CL — centered between plate edge",
        f"   and {BRKT_T}mm gusset.",
        f"3. Upper bolt at Z={bolt_z_hi}mm (above grating",
        f"   deck Z=100), centered on gusset CL.",
        f"4. All holes {HOLE_D}mm clearance for M12.",
        f"5. Head on exterior 6mm reinforcing plate,",
        f"   nut on interior bracket face.",
        f"6. See View A for bolt cross-section.",
    ]
    draw_notes(ax2, notes_b, PL_X_LO + 5, -5,
               spacing=9, fs=5.5, title_fs=6, color=C_DIM,
               title_color=C_OUT, font=FONT,
               width=PL_X_HI - PL_X_LO - 10)

    fig.savefig("diagrams/walkway-sheet2.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet2.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet2.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — Plan View of Walkway Layout
#
# Top-down view showing all 4 walkway sections with bracket positions.
# Horizontal = X (container long axis)
# Vertical   = Yd (container width)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():
    import matplotlib.patches as mpatches

    BRKT_MARK_W = 30   # bracket marker width in plan view (mm, visual)
    BRKT_MARK_D = 20   # bracket marker depth in plan view (mm, visual)

    # ── Figure ───────────────────────────────────────────────────────────────
    PAD_X = 300
    PAD_Y_BOT = 1100  # extra room below for notes + title block
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
    ax.text(C_LEN / 2, -40, "PINHOLE WALL (Yd=0)",
            ha="center", va="top", fontsize=6, color=C_DIM, **FONT, zorder=15)
    ax.text(C_LEN / 2, C_WID + 40, f"FAR WALL (Yd={C_WID})",
            ha="center", va="bottom", fontsize=6, color=C_DIM, **FONT, zorder=15)
    ax.text(-40, C_WID / 2, "CARGO DOOR\nEND (X=0)",
            ha="right", va="center", fontsize=6, color=C_DIM,
            **FONT, zorder=15, rotation=90)
    ax.text(C_LEN + 40, C_WID / 2, f"FAR END\n(X={C_LEN})",
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
    # so they clear the panel transport envelope (max X=420).
    # Right corners: BUTT JOINT — right walkway is ceiling-hung (same 300mm width).
    C_WK = "#D0C8B8"
    WK_ALPHA = 0.6
    W = WALKWAY_W

    LX  = WALKWAY_LEFT_X;   LXR = LX + W
    RX  = WALKWAY_RIGHT_X;  RXR = RX + W      # right walkway inner/outer edges
    NY  = WALKWAY_NEAR_YD;  NYI = NY + W
    FY  = WALKWAY_FAR_YD;   FYO = FY + W
    TL  = PROC_TRAY_X_L;   TR = TL + PROC_TRAY_W

    # Near walkway: L-shaped polygon with bump-out at X=1600-2310
    near_len = TR - LXR   # near/far walkway length (from butt joint to tray right)
    WXL = WALKWAY_NEAR_WIDE_X_L  # 1600
    WXR = WALKWAY_NEAR_WIDE_X_R  # 2310
    WW  = WALKWAY_NEAR_WIDE_W    # 500
    near_verts = [
        (LXR, NY), (TR, NY), (TR, NYI),
        (WXR, NYI), (WXR, WW), (WXL, WW), (WXL, NYI),
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
                if name == "NEAR":
                    ax.add_patch(Rectangle((bx - BRKT_MARK_W / 2, NY),
                                 BRKT_MARK_W, BRKT_MARK_D,
                                 fc=C_BRKT, ec=C_OUT, lw=0.6, zorder=6))
                else:
                    ax.add_patch(Rectangle((bx - BRKT_MARK_W / 2, FYO - BRKT_MARK_D),
                                 BRKT_MARK_W, BRKT_MARK_D,
                                 fc=C_BRKT, ec=C_OUT, lw=0.6, zorder=6))
        elif name == "RIGHT":
            # Right walkway: ceiling-hung — show hanger positions as + marks
            hanger_yds = np.array([WALKWAY_RIGHT_HANGER_Y1] + list(
                np.arange(WALKWAY_BRACKET_SPACING / 2 + WALKWAY_BRACKET_SPACING,
                           C_WID, WALKWAY_BRACKET_SPACING)))[:WALKWAY_RIGHT_HANGER_N]
            hgr_sz = 12  # half-size of + mark
            for by in hanger_yds:
                # Inner bearer hanger (X = RX)
                for hx in [RX + 15, RXR - 15]:
                    ax.plot([hx - hgr_sz, hx + hgr_sz], [by, by],
                            color="#606068", lw=1.2, zorder=8)
                    ax.plot([hx, hx], [by - hgr_sz, by + hgr_sz],
                            color="#606068", lw=1.2, zorder=8)
                    ax.add_patch(Circle((hx, by), WALKWAY_RIGHT_HANGER_D / 2 * 1.5,
                                 fc="none", ec="#606068", lw=0.8, zorder=8))
        # LEFT walkway: NO brackets — removable lift-out section

        # Section label
        cx = wx + ww * 0.55
        cy = wy + wh / 2
        rot = 0 if is_x_axis else 90
        length = ww if is_x_axis else wh
        if name == "LEFT":
            lbl = f"LEFT WALKWAY\n{int(length)}\u00d7{WALKWAY_W}mm\nREMOVABLE LIFT-OUT"
        elif name == "RIGHT":
            lbl = f"RIGHT WALKWAY\n{int(length)}\u00d7{WALKWAY_W}mm\nCEILING-HUNG"
        elif name == "NEAR":
            lbl = f"NEAR WALKWAY\n{int(length)}\u00d7{WALKWAY_W}mm\n(WIDENED TO {WALKWAY_NEAR_WIDE_W}mm\nAT EP/BATT ZONE)"
        else:
            lbl = f"{name} WALKWAY\n{int(length)}\u00d7{WALKWAY_W}mm"
        ax.text(cx, cy, lbl,
                ha="center", va="center", fontsize=6, color=C_OUT,
                backgroundcolor="#FFFFFF",
                fontweight="bold", **FONT, zorder=7, rotation=rot)

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

    # Label right walkway hanger detail
    hanger_lbl_x = RX + W / 2
    leader(ax, hanger_lbl_x + 120, W / 2 + 90,
           hanger_lbl_x + 450, W / 2 + 350,
           f"CEILING HANGERS\nM{WALKWAY_RIGHT_HANGER_D} THREADED ROD\n"
           f"({WALKWAY_RIGHT_HANGER_N} PAIRS — 1st AT {WALKWAY_RIGHT_HANGER_Y1}mm,\nREST AT {WALKWAY_BRACKET_SPACING}mm CTR)",
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
    draw_dim_h(ax, WXL, WXR, WW + 30,
               f"{WXR - WXL}mm BUMP-OUT", offset=50, fs=6, font=FONT)

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
            fontsize=5, color=C_EQUIP_GHOST, **FONT, zorder=6, alpha=0.6)

    # ── Spray bar slit in near & far walkways ──────────────────────────────────
    slit_cx = (PROC_OPEN_X_L + PROC_OPEN_X_R) / 2
    slit_w = SPRAY_BAR_SLIT_W
    C_SLIT = "#CC0000"

    # Near walkway slit
    ax.add_patch(Rectangle((slit_cx - slit_w / 2, NY),
                 slit_w, W,
                 fc="#FF4444", ec=C_SLIT, lw=1.5, alpha=0.6, zorder=7))
    # Far walkway slit
    ax.add_patch(Rectangle((slit_cx - slit_w / 2, FY),
                 slit_w, W,
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
    ax.text(EVAP_STOW_X + EVAP_W + 40, EVAP_STOW_YD + EVAP_D / 2,
            "RATCHET\nSTRAPS (×2)\nTO WALL\nBRACKETS",
            ha="left", va="center", fontsize=4.5, color="#CC6600",
            **FONT, zorder=8)

    # ── Panel transport envelope (dashed red) ────────────────────────────────
    # Show the zone swept by the panel when sliding to transport position.
    # Left walkway must be removed before panel slides.
    panel_transport_x = PANEL_SLIDE + 120  # panel center zone inner face in transport
    ax.add_patch(Rectangle((0, 0), panel_transport_x, C_WID,
                            fc="#FF0000", ec="#CC0000", lw=1.5, ls=(0, (4, 3)),
                            alpha=0.06, zorder=3))
    ax.plot([panel_transport_x, panel_transport_x], [0, C_WID],
            color="#CC0000", lw=1.2, ls=(0, (4, 3)), zorder=5)
    ax.text(panel_transport_x / 2, C_WID / 2 + 450,
            f"PANEL TRANSPORT\nENVELOPE\n(X=0\u2013{panel_transport_x}mm)",
            ha="center", va="center", fontsize=6, color="#CC0000",
            fontweight="bold", **FONT, zorder=15, alpha=0.8,
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

    # ── Left walkway support — bearer beam + floor legs + bearing strip ────
    C_SUPPORT = "#D08020"   # orange for support elements

    # Bearer beam along Yd at X=470 (processing tray side)
    # Spans from near bracket arm (Yd=NYI) to far bracket arm (Yd=FY)
    beam_x = LXR   # = 470mm
    beam_w_vis = 12  # visual width in plan view (beam is 50mm deep, seen from above)
    ax.plot([beam_x, beam_x], [NYI, FY],
            color=C_SUPPORT, lw=4.0, zorder=8, solid_capstyle="butt")
    ax.text(beam_x + 24, (NYI + FY) / 2,
            f"BEARER BEAM\n{LEFT_WK_BEARER_SIZE}\u00d7{LEFT_WK_BEARER_SIZE}"
            f"\u00d7{LEFT_WK_BEARER_T}mm\nAl RHS\n(REMOVABLE)",
            ha="left", va="center", fontsize=4.5, color=C_SUPPORT,
            fontweight="bold", **FONT, zorder=15, rotation=90)

    # Bearing strip on tray rim (X=170, continuous along Yd)
    strip_yd_start = NYI   # start at near walkway inner edge (Yd=300)
    strip_yd_end   = FY    # end at far walkway inner edge (Yd=1,962)
    ax.plot([LX, LX], [strip_yd_start, strip_yd_end],
            color=C_SUPPORT, lw=3.0, zorder=8, solid_capstyle="butt")
    ax.text(LX - 20, (strip_yd_start + strip_yd_end) * 0.6,
            f"BEARING\nSTRIP\n(Al 25\u00d725)",
            ha="right", va="center", fontsize=4.5, color=C_SUPPORT,
            fontweight="bold", **FONT, zorder=15, rotation=90)

    # Floor-standing support legs (cargo door side, X < tray rim)
    leg_spacing = WALKWAY_LEFT_SPAN / (LEFT_WK_LEG_N + 1)
    leg_x = LX - 30  # X=140 (on bare floor, outside tray)
    leg_sz = 18
    for i in range(LEFT_WK_LEG_N):
        cy = NYI + leg_spacing * (i + 1)  # Yd position
        # Leg marker (small square)
        ax.add_patch(Rectangle((leg_x - leg_sz / 2, cy - leg_sz / 2),
                     leg_sz, leg_sz,
                     fc=C_SUPPORT, ec=C_OUT, lw=0.8, zorder=9))
        # Cantilever arm to walkway edge
        ax.plot([leg_x, LX + 20], [cy, cy],
                color=C_SUPPORT, lw=1.5, zorder=8)
    # Label first leg
    c1_yd = NYI + leg_spacing
    leader(ax, leg_x, c1_yd + leg_sz / 2 + 5,
           leg_x - 300, c1_yd + leg_sz / 2 + 180,
           f"FLOOR LEG (\u00d7{LEFT_WK_LEG_N})\n{int(leg_spacing)}mm SPACING\nON BARE FLOOR\n(OUTSIDE TRAY)",
           color=C_SUPPORT, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Dimension lines ──────────────────────────────────────────────────────
    # Walkway width dimension (near walkway)
    draw_dim_v(ax, PROC_TRAY_X_L - 40, WALKWAY_NEAR_YD, WALKWAY_NEAR_YD + WALKWAY_W,
               f"{WALKWAY_W}mm", offset=50, fs=6, right=False, font=FONT)

    # Bracket spacing callout
    # Find two adjacent bracket positions on near walkway for dimensioning
    brkt_x0 = TL + WALKWAY_BRACKET_SPACING / 2
    brkt_x1 = brkt_x0 + WALKWAY_BRACKET_SPACING
    draw_dim_h(ax, brkt_x0, brkt_x1, -40,
               f"{WALKWAY_BRACKET_SPACING}mm BRACKET SPACING (TYP.)",
               offset=50, fs=6, above=False, font=FONT)

    # ── Legend ────────────────────────────────────────────────────────────────
    draw_legend(ax, [
        (C_WK,       WK_ALPHA, "xx",  "Walkway (grated deck)"),
        ("#E8F0FF",  0.3,      None,  "Processing tray"),
        (C_BRKT,     1.0,      None,  f"Wall bracket ({WALKWAY_BRACKET_T}mm gusset)"),
        (C_SUPPORT,  0.8,      None,  f"Support cradle / bearing strip (removable)"),
        ("#3DAA96",  0.35,     None,  f"Evap cooler transport stowage ({EVAP_W}×{EVAP_D}mm)"),
        ("#FF4444",  0.6,      None,  f"Spray bar slit ({SPRAY_BAR_SLIT_W}mm, near + far)"),
        ("#FF0000",  0.06,     None,  "Panel transport envelope"),
        ("#CC6600",  0.7,      None,  "Ratchet strap (transport securing)"),
    ], C_LEN - 1225, C_WID + PAD_Y_TOP - 2850, pad=25, col_w=1100, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    n_brackets_near = len(np.arange(LXR + WALKWAY_BRACKET_SPACING / 2,
                                     TR, WALKWAY_BRACKET_SPACING))
    n_brackets_total = n_brackets_near * 2  # near + far only (no right brackets)
    notes = [
        "CONSTRUCTION NOTES:",
        f"1. 4 removable grated sections, {WALKWAY_W}mm wide standard. Butt joints at all corners.",
        f"2. Near walkway WIDENED to {WALKWAY_NEAR_WIDE_W}mm at X={WXL}\u2013{WXR} (clears EP + battery bank).",
        f"   Deeper cantilever brackets ({WALKWAY_NEAR_WIDE_W}mm arm) with heavier gussets in bump-out zone.",
        f"3. Near/far: wall-cantilevered brackets ({WALKWAY_BRACKET_T}mm gussets) at {WALKWAY_BRACKET_SPACING}mm centers.",
        f"   Start at X={LXR} (butt joint) \u2014 past panel transport envelope (X\u2264420).",
        f"4. Right: CEILING-HUNG \u2014 {WALKWAY_RIGHT_HANGER_N} pairs M{WALKWAY_RIGHT_HANGER_D} rod hangers.",
        f"5. Left: REMOVABLE LIFT-OUT \u2014 bearer beam ({LEFT_WK_BEARER_SIZE}\u00d7{LEFT_WK_BEARER_SIZE}\u00d7{LEFT_WK_BEARER_T}mm Al RHS) at X={LXR},",
        f"   spans {WALKWAY_LEFT_SPAN}mm. {LEFT_WK_LEG_N} floor legs + bearing strip.",
        f"6. ZERO tray contact \u2014 all supports outside or above tray. Open area: {PROC_OPEN_AREA:.1f} m\u00b2.",
        f"7. ~{n_brackets_total} wall brackets (near + far). Each grating section lifts off for tray access.",
        f"8. SPRAY BAR SLIT: {SPRAY_BAR_SLIT_W}mm slot at beam center X={int((PROC_OPEN_X_L + PROC_OPEN_X_R) / 2)} in near + far walkway",
        f"   grating for telescoping pole passage. See Spray Bar Assembly drawings.",
        f"9. EVAP COOLER TRANSPORT: stow on near walkway (X={EVAP_STOW_X}–{EVAP_STOW_X + EVAP_W}mm),",
        f"   ply base plate on grating, 2× ratchet straps to wall brackets. ~20 kg dry.",
    ]
    draw_notes(ax, notes, 1500,
               -PAD_Y_BOT + 350 + (len(notes) - 1) * 44,
               spacing=44, fs=7, width=2500, font=FONT)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 6",
                drawing_title="PERIMETER WALKWAY",
                subtitle="PLAN VIEW \u2014 BRACKET LAYOUT + LEFT WALKWAY SUPPORT",
                scale_note=f"Axes in mm \u00b7 BRACKETS AT {WALKWAY_BRACKET_SPACING}mm CENTERS",
                height=0.06)

    fig.savefig("diagrams/walkway-sheet1.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet1.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet1.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — Detail A: Right Walkway Ceiling-Hung Support (IBC End)
#
# Elevation cross-section looking along the walkway (Yd axis).
# The far end wall is flat 1.6mm steel — no corrugation ribs.
# A 25×25×5mm angle iron is welded horizontally along the interior face
# to provide a structural mounting surface for the cantilever brackets.
# Scale ≈ 3:1 for clarity.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet3():
    """Right walkway — ceiling-hung hanger detail.

    Split view: top detail (ceiling attachment) and bottom detail (bearer/grating)
    with a break in between to cut out the featureless rod section.
    Cross-section looking along Yd.  Horizontal = X, Vertical = Z.
    """
    def sx(mm): return mm
    def sy(mm): return mm

    # ── Structural dimensions ────────────────────────────────────────────────
    FLOOR_T      = 3
    TRAY_WALL    = 3
    TRAY_FLOOR_T = 2
    CEIL_T       = 2
    CEIL_CORR_H  = 30

    BEARER_S = WALKWAY_RIGHT_BEARER_SIZE   # 50mm leg
    BEARER_T = WALKWAY_RIGHT_BEARER_T      # 5mm
    HANGER_D = WALKWAY_RIGHT_HANGER_D      # M10
    HANGER_R = HANGER_D / 2
    DECK_H   = WALKWAY_H                   # 100mm
    BEARER_TOP = DECK_H - WALKWAY_GRATE_T  # 75mm
    BEARER_BOT = BEARER_TOP - BEARER_S     # 25mm

    BOLT_D   = 10
    BOLT_R   = BOLT_D / 2
    WASHER_T = 3
    NUT_H    = 10

    # ── Right walkway geometry ───────────────────────────────────────────────
    TRAY_RIM_X = PROC_TRAY_X_R
    IBC_X      = IBC_COL_X
    WK_LEFT_X  = WALKWAY_RIGHT_X
    WK_RIGHT_X = WK_LEFT_X + WALKWAY_W

    CP_L, CP_W, CP_T = WALKWAY_RIGHT_CEIL_PLATE

    # ── Coordinate system ────────────────────────────────────────────────────
    # Split view: bottom zone Z = -40 to 200, top zone Z = C_HGT-100 to C_HGT+60
    # Mapped into drawing coordinates with a break gap between them.
    BOT_Z_LO = -40
    BOT_Z_HI = 200      # bottom detail range
    TOP_Z_LO = C_HGT - 100   # top detail range
    TOP_Z_HI = C_HGT + CEIL_CORR_H + 40
    BREAK_GAP = 80       # visual gap for break lines (in drawing mm)

    BOT_RANGE = BOT_Z_HI - BOT_Z_LO   # 240mm
    TOP_RANGE = TOP_Z_HI - TOP_Z_LO   # ~170mm

    def zy_bot(z):
        """Map real Z in bottom zone to drawing Y."""
        return z - BOT_Z_LO

    def zy_top(z):
        """Map real Z in top zone to drawing Y."""
        return BOT_RANGE + BREAK_GAP + (z - TOP_Z_LO)

    DRAW_H = BOT_RANGE + BREAK_GAP + TOP_RANGE

    DRAW_CENTER_X = (WK_LEFT_X + WK_RIGHT_X) / 2
    X_OFFSET = DRAW_CENTER_X - 250
    def rx(real_x):
        return real_x - X_OFFSET

    WK_L  = rx(WK_LEFT_X)
    WK_R  = rx(WK_RIGHT_X)
    TRAY_DX = rx(TRAY_RIM_X)
    IBC_DX  = rx(IBC_X)
    BR_IN_X  = WK_L + 15
    BR_OUT_X = WK_R - BEARER_S - 15

    X_LO = WK_L - 100
    X_HI = IBC_DX + 200

    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(sx(X_LO), sx(X_HI))
    ax.set_ylim(sy(-10), sy(DRAW_H + 10))
    ax.set_aspect("equal")
    ax.axis("off")

    # ════════════════════════════════════════════════════════════════════════
    # BOTTOM DETAIL — floor, tray, bearers, grating (Z = -40 to 200)
    # ════════════════════════════════════════════════════════════════════════

    # Container floor
    ax.add_patch(Rectangle((sx(X_LO), sy(zy_bot(-FLOOR_T))),
                            sx(TRAY_DX - X_LO), sy(FLOOR_T),
                            fc=C_FLOOR, ec=C_OUT, lw=1.0, zorder=3))
    ax.add_patch(Rectangle((sx(TRAY_DX), sy(zy_bot(-FLOOR_T))),
                            sx(X_HI - TRAY_DX), sy(FLOOR_T),
                            fc="#D0C8B8", ec=C_OUT, lw=1.0, zorder=3))
    ax.plot([sx(X_LO), sx(X_HI)], [sy(zy_bot(0)), sy(zy_bot(0))],
            color=C_OUT, lw=1.5, zorder=4)
    # Ground hatching
    ax.add_patch(Rectangle((sx(X_LO), sy(zy_bot(-FLOOR_T - 15))),
                            sx(X_HI - X_LO), sy(15),
                            fc="#E0DDD8", ec=C_OUT, lw=0.5, hatch="///", zorder=2))

    leader(ax, sx((TRAY_DX + IBC_DX) / 2), sy(zy_bot(-FLOOR_T / 2)),
           sx(IBC_DX + 60), sy(zy_bot(-25)),
           "BARE FLOOR\n(NO CONTACT)",
           color="#604020", fs=5.5,
           ha="left", va="center", arrow_style="-|>", font=FONT)

    # Processing tray rim
    ax.add_patch(Rectangle((sx(TRAY_DX - TRAY_WALL), sy(zy_bot(0))),
                            sx(TRAY_WALL), sy(PROC_TRAY_RIM),
                            fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=4))
    tray_floor_left = X_LO + 15
    ax.add_patch(Rectangle((sx(tray_floor_left), sy(zy_bot(0))),
                            sx(TRAY_DX - TRAY_WALL - tray_floor_left), sy(TRAY_FLOOR_T),
                            fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))
    bx_tray = sx(tray_floor_left)
    zz_t = np.linspace(sy(zy_bot(0)), sy(zy_bot(TRAY_FLOOR_T)), 5)
    ax.plot([bx_tray - 3, bx_tray + 3, bx_tray - 3, bx_tray + 3, bx_tray - 3],
            zz_t, color=C_OUT, lw=1.0, zorder=5)
    leader(ax, sx(TRAY_DX - TRAY_WALL / 2), sy(zy_bot(PROC_TRAY_RIM)),
           sx(TRAY_DX - 55), sy(zy_bot(PROC_TRAY_RIM - 30)),
           f"TRAY RIM\n{PROC_TRAY_RIM}mm",
           color=C_TRAY, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # IBC ghost — 2×2 stack (bottom zone + through break + into top zone)
    # Cross-section looking along Yd: horizontal = X, vertical = Z
    # IBC inner face at IBC_DX, extends IBC_W = 1219mm to the right
    IBC_SHOW_W = min(IBC_W, X_HI - IBC_DX - 10)  # clip to drawing width
    C_IBC = "#B08040"
    IBC_A = 0.20   # ghost alpha

    # Bottom IBC (Z=0 to IBC_H_600) — only bottom zone visible
    ax.add_patch(Rectangle((sx(IBC_DX), sy(zy_bot(0))),
                            sx(IBC_SHOW_W), sy(BOT_Z_HI - 10),
                            fc="#FFE8C0", ec=C_IBC, lw=1.0, ls="--",
                            zorder=2, alpha=IBC_A))
    # IBC cage vertical posts at inner face
    post_w = 8
    ax.add_patch(Rectangle((sx(IBC_DX), sy(zy_bot(0))),
                            sx(post_w), sy(BOT_Z_HI - 10),
                            fc=C_IBC, ec=C_IBC, lw=0.5,
                            zorder=2, alpha=IBC_A * 1.5))
    # IBC cage bottom rail
    ax.add_patch(Rectangle((sx(IBC_DX), sy(zy_bot(0))),
                            sx(IBC_SHOW_W), sy(post_w),
                            fc=C_IBC, ec=C_IBC, lw=0.5,
                            zorder=2, alpha=IBC_A * 1.5))

    # Continuation through break zone (dashed vertical lines)
    for edge_x in [IBC_DX, IBC_DX + IBC_SHOW_W]:
        ax.plot([sx(edge_x), sx(edge_x)],
                [sy(zy_bot(BOT_Z_HI - 10)), sy(zy_top(TOP_Z_LO + 10))],
                color=C_IBC, lw=0.8, ls=(0, (4, 4)), alpha=0.3, zorder=1)

    # Stacking frame line (at Z = IBC_H_600 = 1010mm) — annotated in break
    frame_label_y = (zy_bot(BOT_Z_HI) + zy_top(TOP_Z_LO)) / 2 + 10
    ax.plot([sx(IBC_DX), sx(IBC_DX + IBC_SHOW_W)],
            [sy(frame_label_y), sy(frame_label_y)],
            color=C_IBC, lw=1.5, ls="--", alpha=0.5, zorder=1)
    ax.text(sx(IBC_DX + IBC_SHOW_W / 2), sy(frame_label_y + 5),
            f"STACKING FRAME\n(Z={IBC_H_600}mm)",
            ha="center", va="bottom", fontsize=5, color=C_IBC,
            **FONT, zorder=15, alpha=0.6)

    # Labels
    ax.text(sx(IBC_DX + IBC_SHOW_W / 2), sy(zy_bot(BOT_Z_HI - 20)),
            f"BOTTOM IBC\n(GHOST)",
            ha="center", va="top", fontsize=5.5, color=C_IBC,
            fontweight="bold", **FONT, zorder=15, alpha=0.7)
    ax.text(sx(IBC_DX + IBC_SHOW_W / 2), sy(frame_label_y + 30),
            f"TOP IBC\n(GHOST)",
            ha="center", va="bottom", fontsize=5.5, color=C_IBC,
            fontweight="bold", **FONT, zorder=15, alpha=0.7)
    # Stack annotation
    ax.text(sx(IBC_DX + IBC_SHOW_W + 5), sy(zy_bot(BOT_Z_HI / 2)),
            f"2\u00d72 IBC STACK\n{IBC_H_600}\u00d72 = {IBC_H_600*2}mm",
            ha="left", va="center", fontsize=5, color=C_IBC,
            **FONT, zorder=15, alpha=0.6)

    # Bearer angles
    for br_x in [BR_IN_X, BR_OUT_X]:
        ax.add_patch(Rectangle((sx(br_x), sy(zy_bot(BEARER_BOT))),
                                sx(BEARER_T), sy(BEARER_S),
                                fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=8, alpha=0.85))
        ax.add_patch(Rectangle((sx(br_x), sy(zy_bot(BEARER_TOP - BEARER_T))),
                                sx(BEARER_S), sy(BEARER_T),
                                fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=8, alpha=0.85))

    leader(ax, sx(BR_IN_X + BEARER_S * 0.4), sy(zy_bot(BEARER_BOT + 5)),
           sx(BR_IN_X + 35), sy(zy_bot(BEARER_BOT - 25)),
           f"BEARER ANGLE\n{BEARER_S}\u00d7{BEARER_S}\u00d7{BEARER_T}mm\nSTEEL L-ANGLE\n"
           f"(SPANS {C_WID}mm ALONG Yd)",
           color=C_BRKT, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # Grated deck
    grate_bot = BEARER_TOP
    grate_top = grate_bot + WALKWAY_GRATE_T
    ax.add_patch(Rectangle((sx(WK_L), sy(zy_bot(grate_bot))),
                            sx(WK_R - WK_L), sy(WALKWAY_GRATE_T),
                            fc=C_GRATE, ec=C_OUT, lw=1.2, zorder=10))
    bar_spacing = 34.2
    bar_w = 3
    for xb in np.arange(bar_w, WK_R - WK_L - bar_w, bar_spacing):
        ax.add_patch(Rectangle((sx(WK_L + xb), sy(zy_bot(grate_bot))),
                                sx(bar_w), sy(WALKWAY_GRATE_T),
                                fc="#909098", ec=C_OUT, lw=0.3, zorder=11))

    # Grating clips
    for clip_x in [WK_L + 12, WK_R - 20]:
        ax.add_patch(Rectangle((sx(clip_x), sy(zy_bot(grate_bot - 4))),
                                sx(8), sy(WALKWAY_GRATE_T + 9),
                                fc="#505058", ec=C_OUT, lw=0.8, zorder=12))
    leader(ax, sx(WK_L + 16), sy(zy_bot(grate_top + 5)),
           sx(WK_L - 25), sy(zy_bot(grate_top + 30)),
           "GRATING CLIP", color="#505058", fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # Hanger rod stubs (extending up from bearer into break zone)
    C_ROD = "#606068"
    rod_hw = HANGER_R * 0.4
    # Rod passes through the horizontal flange of the L-angle.
    # Nut + washer below the horizontal flange, nut + washer above.
    FLANGE_BOT = BEARER_TOP - BEARER_T   # bottom of horizontal flange
    for br_x in [BR_IN_X + BEARER_S / 2, BR_OUT_X + BEARER_S / 2]:
        # Bottom nut + washer (below horizontal flange)
        ax.add_patch(Rectangle((sx(br_x - HANGER_R - 1), sy(zy_bot(FLANGE_BOT - WASHER_T))),
                                sx(HANGER_D + 2), sy(WASHER_T),
                                fc="#808080", ec=C_OUT, lw=0.5, zorder=7))
        ax.add_patch(Rectangle((sx(br_x - HANGER_R), sy(zy_bot(FLANGE_BOT - WASHER_T - NUT_H))),
                                sx(HANGER_D), sy(NUT_H),
                                fc="#505058", ec=C_OUT, lw=0.8, zorder=7))
        # Top nut + washer (above horizontal flange)
        ax.add_patch(Rectangle((sx(br_x - HANGER_R - 1), sy(zy_bot(BEARER_TOP))),
                                sx(HANGER_D + 2), sy(WASHER_T),
                                fc="#808080", ec=C_OUT, lw=0.5, zorder=7))
        ax.add_patch(Rectangle((sx(br_x - HANGER_R), sy(zy_bot(BEARER_TOP + WASHER_T))),
                                sx(HANGER_D), sy(NUT_H),
                                fc="#505058", ec=C_OUT, lw=0.8, zorder=7))
        # Rod stub up to top of bottom zone
        ax.add_patch(Rectangle((sx(br_x - rod_hw), sy(zy_bot(FLANGE_BOT - WASHER_T - NUT_H))),
                                sx(rod_hw * 2), sy(BOT_Z_HI - FLANGE_BOT + WASHER_T + NUT_H),
                                fc=C_ROD, ec=C_OUT, lw=0.8, zorder=5))

    # Bottom detail dimensions
    draw_dim_h(ax, sx(WK_L), sx(WK_R), sy(zy_bot(grate_top + 15)),
               f"{WALKWAY_W}mm WALKWAY", offset=sy(8), fs=7, font=FONT)
    draw_dim_v(ax, sx(WK_L - 15), sy(zy_bot(0)), sy(zy_bot(grate_top)),
               f"{DECK_H}mm\nDECK", offset=sx(8), fs=6.5, right=False, font=FONT)
    draw_dim_v(ax, sx(BR_IN_X - 10), sy(zy_bot(BEARER_BOT)), sy(zy_bot(BEARER_TOP)),
               f"{BEARER_S}", offset=sx(6), fs=5.5, right=False, font=FONT)
    draw_dim_h(ax, sx(WK_R), sx(IBC_DX), sy(zy_bot(PROC_TRAY_RIM + 15)),
               f"{int(IBC_X - WK_RIGHT_X)}mm\nTO IBC", offset=sy(6), fs=6, font=FONT)

    # ════════════════════════════════════════════════════════════════════════
    # BREAK LINES (sawtooth between bottom and top details)
    # ════════════════════════════════════════════════════════════════════════
    break_y_bot = zy_bot(BOT_Z_HI)
    break_y_top = break_y_bot + BREAK_GAP
    for side_x in [X_LO, X_HI]:
        pass  # no side break lines needed
    # Sawtooth across full width
    n_teeth = 12
    xs = np.linspace(X_LO, X_HI, n_teeth * 2 + 1)
    for break_y in [break_y_bot, break_y_top]:
        teeth_y = [break_y + (8 if i % 2 == 1 else -8) for i in range(len(xs))]
        ax.plot([sx(x) for x in xs], [sy(y) for y in teeth_y],
                color=C_OUT, lw=1.2, zorder=15)

    # Rod continuation through break (dashed)
    for br_x in [BR_IN_X + BEARER_S / 2, BR_OUT_X + BEARER_S / 2]:
        ax.plot([sx(br_x), sx(br_x)],
                [sy(break_y_bot + 8), sy(break_y_top - 8)],
                color=C_ROD, lw=1.5, ls=(0, (4, 3)), zorder=14)

    # Break label
    ax.text(sx((X_LO + X_HI) / 2), sy((break_y_bot + break_y_top) / 2),
            f"M{HANGER_D} THREADED ROD \u2014 {WALKWAY_RIGHT_HANGER_L}mm\n"
            f"({WALKWAY_RIGHT_HANGER_N} PAIRS — 1st AT Yd={WALKWAY_RIGHT_HANGER_Y1}mm, REST AT {WALKWAY_BRACKET_SPACING}mm CTR)",
            ha="center", va="center", fontsize=7, color=C_ROD,
            fontweight="bold", **FONT, zorder=16,
            bbox=dict(boxstyle="round,pad=0.3", fc=BG, ec=C_ROD, lw=0.8, alpha=0.9))

    # ════════════════════════════════════════════════════════════════════════
    # TOP DETAIL — ceiling attachment (Z = C_HGT-100 to C_HGT+60)
    # ════════════════════════════════════════════════════════════════════════

    # Ceiling panel
    ax.add_patch(Rectangle((sx(X_LO), sy(zy_top(C_HGT))),
                            sx(X_HI - X_LO), sy(CEIL_T),
                            fc="#B0B0B8", ec=C_OUT, lw=1.5, zorder=3))
    ax.add_patch(Rectangle((sx(X_LO), sy(zy_top(C_HGT + CEIL_T))),
                            sx(X_HI - X_LO), sy(CEIL_CORR_H),
                            fc="#C0C0C8", ec=C_OUT, lw=0.8, zorder=2, hatch=".."))

    # Ceiling bracket plates + bolts
    C_BOLT = "#505058"
    for br_x in [BR_IN_X + BEARER_S / 2, BR_OUT_X + BEARER_S / 2]:
        plate_left = br_x - CP_L / 2
        ax.add_patch(Rectangle((sx(plate_left), sy(zy_top(C_HGT - CP_T))),
                                sx(CP_L), sy(CP_T),
                                fc=C_BRKT, ec=C_OUT, lw=1.0, zorder=6, alpha=0.85))
        for boff in [-CP_L * 0.25, CP_L * 0.25]:
            bx = br_x + boff
            ax.add_patch(Rectangle((sx(bx - HANGER_R * 0.4), sy(zy_top(C_HGT - CP_T))),
                                    sx(HANGER_R * 0.8), sy(CP_T + CEIL_T + 8),
                                    fc=C_BOLT, ec=C_OUT, lw=0.5, zorder=7))
            ax.add_patch(Rectangle((sx(bx - BOLT_R), sy(zy_top(C_HGT + CEIL_T))),
                                    sx(BOLT_D), sy(NUT_H),
                                    fc=C_BOLT, ec=C_OUT, lw=0.8, zorder=7))

        # Rod stub down from ceiling plate into break zone
        ax.add_patch(Rectangle((sx(br_x - rod_hw), sy(zy_top(TOP_Z_LO))),
                                sx(rod_hw * 2), sy(C_HGT - CP_T - TOP_Z_LO),
                                fc=C_ROD, ec=C_OUT, lw=0.8, zorder=5))

    leader(ax, sx(BR_IN_X + BEARER_S / 2 - CP_L / 2 - 2), sy(zy_top(C_HGT - CP_T / 2)),
           sx(BR_IN_X - 55), sy(zy_top(C_HGT - 60)),
           f"CEILING BRACKET PLATE\n{CP_L}\u00d7{CP_W}\u00d7{CP_T}mm STEEL\n"
           f"2\u00d7 M{BOLT_D} THROUGH CEILING",
           color=C_BRKT, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes_x = sx(X_HI - 210)
    notes_top = sy(zy_top(C_HGT - CEIL_CORR_H + 20))
    notes = [
        "RIGHT WALKWAY \u2014 CEILING-HUNG:",
        "",
        f"1. 2\u00d7 {BEARER_S}\u00d7{BEARER_S}\u00d7{BEARER_T}mm steel angle bearers",
        f"   span full container width ({C_WID}mm) along Yd.",
        f"2. Suspended from ceiling corrugations by M{HANGER_D}",
        f"   threaded rod (1st at Yd={WALKWAY_RIGHT_HANGER_Y1}mm, rest {WALKWAY_BRACKET_SPACING}mm ctr).",
        f"3. {WALKWAY_RIGHT_HANGER_N} hanger pairs \u2014 all at Yd \u2264 2,057mm",
        f"   (clear of optical cone).",
        f"4. Near/far ends bear on adjacent walkway brackets.",
        f"5. Deck {DECK_H}mm \u2014 level with all 4 sides.",
        f"6. ZERO floor contact \u2014 clears IBC stack entirely.",
    ]
    draw_notes(ax, notes, notes_x, notes_top, spacing=sy(8), fs=7, width=sx(200), font=FONT)

    # ── Title block ─────────────────────────────────────────────────────────
    title_block(ax, "SHEET 3 OF 6",
                drawing_title="PERIMETER WALKWAY",
                subtitle="DETAIL A \u2014 RIGHT WALKWAY CEILING-HUNG SUPPORT (IBC END)",
                scale_note=f"Axes in mm \u00b7 SECTION LOOKING ALONG Yd",
                height=0.07)

    fig.savefig("diagrams/walkway-sheet3.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet3.png"), bbox_inches="tight", facecolor=BG)
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
    def sx(mm): return mm
    def sy(mm): return mm

    # ── Key geometry ─────────────────────────────────────────────────────────
    BRKT_ARM_Z = WALKWAY_H - WALKWAY_GRATE_T  # 75mm (bracket arm top = grate bottom)
    ARM_DEPTH  = WALKWAY_BRACKET_T + 2         # arm visual thickness
    arm_bot    = BRKT_ARM_Z - ARM_DEPTH
    TRAY_WALL  = 3       # tray wall thickness (SS)
    TRAY_FLOOR_T = 2     # tray floor thickness

    # X positions (horizontal axis in this view — looking along Yd)
    LEFT_WK_L = WALKWAY_LEFT_X                    # = 170mm (left walkway left edge)
    LEFT_WK_R = WALKWAY_LEFT_X + WALKWAY_W        # = 470mm (butt joint / near walkway start)
    PANEL_INNER = PANEL_SLIDE + PANEL_CENTER_T    # = 420mm (panel transport inner face)
    CLEARANCE = LEFT_WK_R - PANEL_INNER           # = 50mm
    NEAR_WK_SHOW = 200   # show 200mm of near walkway past butt joint

    grate_bot = BRKT_ARM_Z   # = 75mm
    grate_top = BRKT_ARM_Z + WALKWAY_GRATE_T  # = 100mm

    # ── Figure ───────────────────────────────────────────────────────────────
    # View: looking along Yd axis (from near wall toward far wall).
    # X = horizontal axis (0 = cargo door end wall, positive into container)
    # Z = vertical axis (0 = floor)
    X_LO = -50
    X_HI = LEFT_WK_R + NEAR_WK_SHOW + 350  # room for near walkway + notes
    Z_LO = -40
    Z_HI = WALKWAY_H + 110

    fig, ax = plt.subplots(figsize=(18, 10))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(sx(X_LO), sx(X_HI))
    ax.set_ylim(sy(Z_LO), sy(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container floor ──────────────────────────────────────────────────────
    ax.add_patch(Rectangle((sx(X_LO), sy(-15)), sx(X_HI - X_LO), sy(15),
                            fc=C_FLOOR, ec=C_OUT, lw=1.0, hatch="///", zorder=2))

    # ── Processing tray rim (at X = PROC_TRAY_X_L = 170mm) ──────────────────
    tray_x = PROC_TRAY_X_L   # = 170mm (same as LEFT_WK_L)
    # Tray left rim (vertical wall)
    ax.add_patch(Rectangle((sx(tray_x - TRAY_WALL), sy(0)),
                            sx(TRAY_WALL), sy(PROC_TRAY_RIM),
                            fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=4))
    # Tray floor extending right
    tray_floor_end = X_HI - 200
    ax.add_patch(Rectangle((sx(tray_x), sy(0)),
                            sx(tray_floor_end - tray_x), sy(TRAY_FLOOR_T),
                            fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))
    # Sawtooth break line on tray floor
    bx = sx(tray_floor_end)
    z_lo, z_hi = 0, TRAY_FLOOR_T
    zz = np.linspace(z_lo, z_hi, 5)
    ax.plot([bx - 3, bx + 3, bx - 3, bx + 3, bx - 3],
            zz, color=C_OUT, lw=1.0, zorder=5)
    # Tray rim label
    leader(ax, sx(tray_x - 5), sy(PROC_TRAY_RIM / 2 + 10),
           sx(tray_x - 70), sy(PROC_TRAY_RIM + 15),
           f"TRAY RIM\n{PROC_TRAY_RIM}mm\n(304 SS)", color=C_TRAY, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Bearing strip on tray rim (25×25mm Al angle) ─────────────────────────
    C_SUPPORT = "#D08020"
    STRIP_H = LEFT_WK_BEARING_STRIP   # = 25mm
    strip_bot = PROC_TRAY_RIM         # = 50mm (sits on rim top)
    strip_top = strip_bot + STRIP_H   # = 75mm (= grate bottom)
    ax.add_patch(Rectangle((sx(tray_x - TRAY_WALL), sy(strip_bot)),
                            sx(STRIP_H + TRAY_WALL), sy(STRIP_H),
                            fc=C_SUPPORT, ec=C_OUT, lw=1.0, zorder=5))
    leader(ax, sx(tray_x + STRIP_H / 2), sy(strip_bot + STRIP_H / 2),
           sx(tray_x + STRIP_H / 2 - 45), sy(strip_bot + STRIP_H + 12),
           f"BEARING STRIP\n25\u00d725\u00d73mm Al ANGLE\nON TRAY RIM\n(REMOVABLE)",
           color=C_SUPPORT, fs=5,
           ha="center", va="bottom", arrow_style="-|>", font=FONT)

    # ── Floor-standing support leg (cargo door side, X≈140) ────────────────
    OUTER_LEG_X = tray_x - 30   # = 140mm (on bare floor, outside tray)
    LEG_W = LEFT_WK_LEG_SIZE    # = 25mm
    LEG_TOP = strip_top          # = 75mm (cantilever arm top = grate bottom)
    base = LEFT_WK_LEG_BASE     # 60mm
    # Leg post
    ax.add_patch(Rectangle((sx(OUTER_LEG_X - LEG_W / 2), sy(0)),
                            sx(LEG_W), sy(LEG_TOP),
                            fc=C_SUPPORT, ec=C_OUT, lw=0.8, alpha=0.5, zorder=4))
    # Foot plate (sits on floor)
    ax.add_patch(Rectangle((sx(OUTER_LEG_X - base / 2), sy(0)),
                            sx(base), sy(3),
                            fc=C_SUPPORT, ec=C_OUT, lw=0.6, alpha=0.5, zorder=4))
    # Cantilever arm from leg to walkway edge
    ax.add_patch(Rectangle((sx(OUTER_LEG_X - LEG_W / 2), sy(LEG_TOP - 5)),
                            sx(tray_x + 20 - OUTER_LEG_X + LEG_W / 2), sy(5),
                            fc=C_SUPPORT, ec=C_OUT, lw=0.6, alpha=0.5, zorder=5))
    # Leg label
    leader(ax, sx(OUTER_LEG_X - LEG_W/2), sy(LEG_TOP / 2),
           sx(OUTER_LEG_X - 55), sy(LEG_TOP / 2),
           f"FLOOR LEG\n(\u00d7{LEFT_WK_LEG_N}, REMOVABLE)\nON BARE FLOOR\nSEE SHEET 6",
           color=C_SUPPORT, fs=5,
           ha="center", va="top", arrow_style="-|>", font=FONT)

    # ── Bearer beam cross-section at X=470 (processing tray side) ────────────
    # Beam runs along Yd, bolted to near/far bracket vertical legs.
    # In this view (along Yd), the beam extends into the page — shown as
    # a cross-section rectangle at X=470.
    BEAM_SZ = LEFT_WK_BEARER_SIZE  # = 50mm
    beam_bot = grate_bot - BEAM_SZ   # Z = 75 - 50 = 25mm
    ax.add_patch(Rectangle((sx(LEFT_WK_R - BEAM_SZ / 2), sy(beam_bot)),
                            sx(BEAM_SZ), sy(BEAM_SZ),
                            fc=C_SUPPORT, ec=C_OUT, lw=1.2, alpha=0.5, zorder=5))
    # Hollow interior
    ax.add_patch(Rectangle((sx(LEFT_WK_R - BEAM_SZ / 2 + LEFT_WK_BEARER_T),
                             sy(beam_bot + LEFT_WK_BEARER_T)),
                            sx(BEAM_SZ - 2 * LEFT_WK_BEARER_T),
                            sy(BEAM_SZ - 2 * LEFT_WK_BEARER_T),
                            fc="#F0E0C8", ec=C_OUT, lw=0.4, alpha=0.5, zorder=6))
    leader(ax, sx(LEFT_WK_R + BEAM_SZ / 2 + 2), sy(beam_bot + BEAM_SZ / 2),
           sx(LEFT_WK_R + BEAM_SZ / 2 + 40), sy(beam_bot + 20),
           f"BEARER BEAM\n{BEAM_SZ}\u00d7{BEAM_SZ}\u00d7{LEFT_WK_BEARER_T}mm\nAl RHS\n"
           f"SPANS {WALKWAY_LEFT_SPAN}mm\nALONG Yd\n(REMOVABLE)",
           color=C_SUPPORT, fs=5,
           ha="left", va="top", arrow_style="-|>", font=FONT)

    # ── Panel transport envelope (ghost) ─────────────────────────────────────
    # Panel sweeps X=0 to X=420, bottom at Z=80mm (PANEL_FLOOR_GAP)
    PANEL_Z_TOP = 250   # show enough of panel to be visible (not full height)
    ax.add_patch(Rectangle((sx(0), sy(PANEL_FLOOR_GAP)),
                            sx(PANEL_INNER), sy(PANEL_Z_TOP - PANEL_FLOOR_GAP),
                            fc="#CC4422", ec="#CC4422", lw=1.5, ls="--",
                            alpha=0.08, zorder=3))
    ax.add_patch(Rectangle((sx(0), sy(PANEL_FLOOR_GAP)),
                            sx(PANEL_INNER), sy(PANEL_Z_TOP - PANEL_FLOOR_GAP),
                            fc="none", ec="#CC4422", lw=1.5, ls="--",
                            alpha=0.5, zorder=8))
    # Panel bottom line (Z=80mm)
    ax.plot([sx(0), sx(PANEL_INNER)], [sy(PANEL_FLOOR_GAP), sy(PANEL_FLOOR_GAP)],
            color="#CC4422", lw=2.0, ls="--", alpha=0.6, zorder=8)
    ax.text(sx(PANEL_INNER / 2), sy(PANEL_Z_TOP - 10),
            f"PANEL TRANSPORT\nENVELOPE\n(X=0\u2013{PANEL_INNER}mm)\nBOTTOM AT Z={PANEL_FLOOR_GAP}mm",
            ha="center", va="top", fontsize=6, color="#CC4422",
            fontweight="bold", **FONT, alpha=0.7, zorder=15)

    # ── Left walkway grating (X=170 to X=470, removable lift-out) ────────────
    C_LEFT_WK = "#A8C8A8"   # green tint for removable section
    ax.add_patch(Rectangle((sx(LEFT_WK_L), sy(grate_bot)),
                            sx(WALKWAY_W), sy(WALKWAY_GRATE_T),
                            fc=C_LEFT_WK, ec=C_OUT, lw=1.5, zorder=7))
    # Bearing bars
    bar_spacing = 34.2
    bar_w = 3
    for x in np.arange(LEFT_WK_L + bar_w, LEFT_WK_R - bar_w, bar_spacing):
        ax.add_patch(Rectangle((sx(x), sy(grate_bot)),
                                sx(bar_w), sy(WALKWAY_GRATE_T),
                                fc="#8AAA8A", ec=C_OUT, lw=0.3, zorder=8))
    ax.text(sx((LEFT_WK_L + LEFT_WK_R) / 2), sy(grate_top + 4),
            f"LEFT WALKWAY GRATING\n({WALKWAY_GRATE_T}mm) \u2014 REMOVABLE LIFT-OUT",
            ha="center", va="bottom", fontsize=6.5, color="#206020",
            fontweight="bold", **FONT, zorder=15)

    # ── Near walkway bracket at butt joint (X=470) ───────────────────────────
    # This bracket is mounted on the near container wall (Yd=0). In this view
    # (looking along Yd), we see the bracket arm in cross-section. The vertical
    # leg is on the wall (perpendicular to view — shown as a narrow strip).
    BRKT_T = WALKWAY_BRACKET_T  # 8mm
    BRKT_VERT = WALKWAY_BRACKET_H  # 150mm vertical leg
    GUSSET_REACH = 70
    GHOST_A = 0.20
    GHOST_C = C_BRKT

    # Ghost outline: bracket arm extends 300mm in Yd (into the page).
    # Show as a wider dashed rectangle at arm level to represent depth.
    ARM_GHOST_W = 40  # visual width representing the arm projecting into page
    ax.add_patch(Rectangle((sx(LEFT_WK_R - ARM_GHOST_W / 2), sy(arm_bot)),
                            sx(ARM_GHOST_W), sy(ARM_DEPTH),
                            fc=C_BRKT, ec=C_OUT, lw=0.8, ls="--",
                            alpha=GHOST_A, zorder=4))
    leader(ax, sx(LEFT_WK_R - ARM_GHOST_W / 2), sy(arm_bot + ARM_DEPTH / 2),
           sx(LEFT_WK_R - ARM_GHOST_W / 2 - 35), sy(arm_bot - 10),
           f"BRACKET ARM\n{WALKWAY_W}mm INTO PAGE\n(GHOST)",
           color=C_BRKT, fs=5,
           ha="center", va="top", arrow_style="-|>", font=FONT)

    # Bracket arm cross-section at X=470 (solid — the cut face)
    ax.add_patch(Rectangle((sx(LEFT_WK_R - BRKT_T / 2), sy(arm_bot)),
                            sx(BRKT_T), sy(ARM_DEPTH),
                            fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=6, alpha=0.85))
    # Arm top surface highlight
    ax.plot([sx(LEFT_WK_R - BRKT_T / 2), sx(LEFT_WK_R + BRKT_T / 2)],
            [sy(BRKT_ARM_Z), sy(BRKT_ARM_Z)],
            color=C_OUT, lw=2.0, zorder=7)

    # Ghost outline: bracket vertical leg + gusset (perpendicular to view,
    # projecting along Yd into the page — shown as dashed ghost to indicate
    # how the bracket is mounted to the near container wall).
    # Vertical leg (Z=0 to 150mm, centered on X=470)
    ax.add_patch(Rectangle((sx(LEFT_WK_R - BRKT_T / 2), sy(0)),
                            sx(BRKT_T), sy(BRKT_VERT),
                            fc=GHOST_C, ec=C_OUT, lw=0.8, ls="--",
                            alpha=GHOST_A, zorder=4))
    # Gusset triangle (wall/floor to arm bottom)
    gusset_verts = [
        (sx(LEFT_WK_R - BRKT_T / 2), sy(0)),
        (sx(LEFT_WK_R - BRKT_T / 2), sy(arm_bot)),
        (sx(LEFT_WK_R - BRKT_T / 2 + GUSSET_REACH), sy(arm_bot)),
    ]
    ax.add_patch(Polygon(gusset_verts, closed=True,
                         fc=GHOST_C, ec=C_OUT, lw=0.8, ls="--",
                         alpha=GHOST_A, zorder=4))
    leader(ax, sx(LEFT_WK_R + BRKT_T / 2 + 2), sy(BRKT_VERT - 10),
           sx(LEFT_WK_R + 45), sy(BRKT_VERT + 5),
           f"BRACKET VERT LEG\n{BRKT_VERT}mm (GHOST \u2014\nPERPENDICULAR\nTO VIEW)",
           color=C_BRKT, fs=5,
           ha="left", va="center", arrow_style="-|>", font=FONT)

    leader(ax, sx(LEFT_WK_R + 20), sy(arm_bot + ARM_DEPTH / 2),
           sx(LEFT_WK_R + 130), sy(arm_bot - 25),
           f"NEAR WALKWAY\nBRACKET ARM\n(CROSS-SECTION)\nAT X={LEFT_WK_R}mm",
           color=C_BRKT, fs=5.5,
           ha="left", va="center", arrow_style="-|>", font=FONT)

    # ── Contact point: left grating rests on bracket arm ─────────────────────
    ax.plot([sx(LEFT_WK_R - 15), sx(LEFT_WK_R + 15)],
            [sy(BRKT_ARM_Z), sy(BRKT_ARM_Z)],
            color="#CC4400", lw=3.0, zorder=10)
    leader(ax, sx(LEFT_WK_R - 10), sy(BRKT_ARM_Z),
           sx(LEFT_WK_R - 120), sy(BRKT_ARM_Z - 18),
           f"GRATING RESTS ON\nBRACKET ARM TOP\n(Z={BRKT_ARM_Z}mm)\nNO FASTENERS \u2014\nLIFT TO REMOVE",
           color="#CC4400", fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Near walkway grating (X=470 onward, standard gray) ───────────────────
    near_wk_start = LEFT_WK_R
    near_wk_end = near_wk_start + NEAR_WK_SHOW
    ax.add_patch(Rectangle((sx(near_wk_start), sy(grate_bot)),
                            sx(NEAR_WK_SHOW), sy(WALKWAY_GRATE_T),
                            fc=C_GRATE, ec=C_OUT, lw=1.2, zorder=7))
    # Bearing bars
    for x in np.arange(near_wk_start + bar_w, near_wk_end - bar_w, bar_spacing):
        ax.add_patch(Rectangle((sx(x), sy(grate_bot)),
                                sx(bar_w), sy(WALKWAY_GRATE_T),
                                fc="#909098", ec=C_OUT, lw=0.3, zorder=8))
    # Sawtooth break line on right edge (near walkway continues)
    bx = sx(near_wk_end)
    z_lo, z_hi = sy(grate_bot - 2), sy(grate_top + 2)
    zz = np.linspace(z_lo, z_hi, 7)
    ax.plot([bx - 3, bx + 3, bx - 3, bx + 3, bx - 3, bx + 3, bx - 3],
            zz, color=C_OUT, lw=1.0, zorder=10)
    ax.text(sx(near_wk_start + NEAR_WK_SHOW / 2), sy(grate_top + 4),
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
    ax.add_patch(Rectangle((sx(clip_x), sy(clip_bot_z)),
                            sx(clip_w), sy(clip_top_z - clip_bot_z),
                            fc="#505058", ec=C_OUT, lw=0.8, zorder=9))
    leader(ax, sx(clip_x + clip_w + 2), sy(grate_top),
           sx(clip_x + 50), sy(grate_top + 20),
           "GRATING CLIP", color="#505058", fs=5.5,
           ha="left", va="center", arrow_style="-|>", font=FONT)

    # ── Butt joint line at X=470 ─────────────────────────────────────────────
    ax.plot([sx(LEFT_WK_R), sx(LEFT_WK_R)], [sy(-5), sy(grate_top + 3)],
            color=C_OUT, lw=2.0, ls=(0, (5, 3)), zorder=9)
    ax.text(sx(LEFT_WK_R), sy(-8),
            f"BUTT JOINT\nX={LEFT_WK_R}mm",
            ha="center", va="top", fontsize=6, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── 50mm clearance dimension (X=420 to X=470) ────────────────────────────
    clr_z = PANEL_FLOOR_GAP + 5
    draw_dim_h(ax, sx(PANEL_INNER), sx(LEFT_WK_R), sy(grate_top + 45),
               f"{CLEARANCE}mm\nCLEARANCE", offset=sy(5), fs=7,
               color="#208020", font=FONT)
    # Vertical guide lines for clearance
    ax.plot([sx(PANEL_INNER), sx(PANEL_INNER)], [sy(0), sy(grate_top + 55)],
            color="#208020", lw=0.6, ls=":", alpha=0.5, zorder=3)
    ax.plot([sx(LEFT_WK_R), sx(LEFT_WK_R)], [sy(grate_top + 5), sy(grate_top + 55)],
            color="#208020", lw=0.6, ls=":", alpha=0.5, zorder=3)

    # ── Left walkway span dimension ──────────────────────────────────────────
    draw_dim_h(ax, sx(LEFT_WK_L), sx(LEFT_WK_R), sy(grate_top + 70),
               f"{WALKWAY_W}mm LEFT WALKWAY", offset=sy(5), fs=7, font=FONT)

    # ── Height dimensions (right side) ───────────────────────────────────────
    dim_x = near_wk_end + 40
    # Grate top
    draw_dim_v(ax, sx(dim_x-30), sy(0), sy(grate_top),
               f"{int(grate_top)}mm\nDECK", offset=sx(6), fs=6, right=True, font=FONT)
    # Arm height
    draw_dim_v(ax, sx(dim_x), sy(0), sy(BRKT_ARM_Z),
               f"{BRKT_ARM_Z}mm\nARM", offset=sx(30), fs=6, right=True, font=FONT)
    # Tray rim
    draw_dim_v(ax, sx(tray_x + 20), sy(0), sy(PROC_TRAY_RIM),
               f"{PROC_TRAY_RIM}mm", offset=sx(6), fs=6, right=True,
               color=C_TRAY, font=FONT)
    # Panel bottom
    draw_dim_v(ax, sx(LEFT_WK_L - 120), sy(0), sy(PANEL_FLOOR_GAP),
               f"{PANEL_FLOOR_GAP}mm\nPANEL\nBOTTOM", offset=sx(6), fs=5.5, right=False,
               color="#CC4422", font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes_x = sx(LEFT_WK_R + 120)
    notes_top = sy(Z_HI - 5)
    leg_spacing = int(WALKWAY_LEFT_SPAN / (LEFT_WK_LEG_N + 1))
    notes = [
        "LEFT WALKWAY \u2014 REMOVABLE LIFT-OUT:",
        f"1. NO wall brackets \u2014 panel occupies end wall.",
        f"2. Processing tray side (X={LEFT_WK_R}): bearer beam {LEFT_WK_BEARER_SIZE}\u00d7{LEFT_WK_BEARER_SIZE}\u00d7{LEFT_WK_BEARER_T}mm Al RHS spans {WALKWAY_LEFT_SPAN}mm (sheet 6).",
        f"3. Cargo door side (X={LEFT_WK_L}): bearing strip + {LEFT_WK_LEG_N} floor legs at {leg_spacing}mm ctrs.",
        f"4. ZERO tray contact \u2014 all supports outside or above processing tray.",
        f"5. {CLEARANCE}mm clearance: panel (X={PANEL_INNER}) to near walkway bracket (X={LEFT_WK_R}).",
        f"6. Remove cradles + grating before panel slides.",
    ]
    draw_notes(ax, notes, notes_x, notes_top, spacing=sy(8), fs=7, width=sx(400), font=FONT)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 4 OF 6",
                drawing_title="PERIMETER WALKWAY",
                subtitle="DETAIL B \u2014 LEFT WALKWAY BUTT JOINT AND PANEL CLEARANCE",
                scale_note=f"Axes in mm \u00b7 VIEW ALONG Yd (NEAR \u2192 FAR)",
                height=0.10)

    fig.savefig("diagrams/walkway-sheet4.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet4.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet4.png saved")

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 5 — Detail C: Left Walkway Support System
#
# Elevation cross-section showing both support elements for the left walkway:
#   (a) Floor-standing support leg (cargo door side, X=140, on bare floor)
#       with cantilever arm to walkway edge.
#   (b) Bearer beam (50×50×3mm Al RHS) at X=470 (processing tray side),
#       spanning 1,762mm along Yd between near/far bracket vertical legs.
#   (c) Bearing strip (25×25×3mm Al angle) on tray rim at X=170.
# View: looking along Yd (same as sheets 1, 3, 5).
# Zero processing tray contact — all supports outside or above tray.
# Scale ≈ 3.5:1 for clarity.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet5():
    def sx(mm): return mm
    def sy(mm): return mm

    # ── Key geometry ─────────────────────────────────────────────────────────
    TRAY_WALL  = 3     # tray wall thickness (SS)
    TRAY_FLOOR_T = 2   # tray floor thickness
    tray_x = PROC_TRAY_X_L   # = 170mm
    LEG_W  = LEFT_WK_LEG_SIZE    # = 25mm tube
    LEG_T  = LEFT_WK_LEG_T       # = 3mm wall
    BASE_W = LEFT_WK_LEG_BASE    # = 60mm foot plate
    BASE_T = 3   # foot plate thickness

    LEFT_WK_L = WALKWAY_LEFT_X                 # = 170mm
    LEFT_WK_R = WALKWAY_LEFT_X + WALKWAY_W     # = 470mm

    BRKT_ARM_Z = WALKWAY_H - WALKWAY_GRATE_T  # = 75mm
    grate_bot = BRKT_ARM_Z   # = 75mm
    grate_top = BRKT_ARM_Z + WALKWAY_GRATE_T  # = 100mm

    # Floor leg geometry (cargo door side — butts up to tray outer wall)
    RUBBER_T = 2                     # rubber pad thickness
    OUTER_LEG_X = tray_x - TRAY_WALL - BASE_W / 2  # leg centered so foot right edge = tray outer wall
    LEG_TOP = grate_bot             # = 75mm (cantilever arm top = grate bottom)

    # Bearer beam geometry (processing tray side)
    BEAM_SZ = LEFT_WK_BEARER_SIZE   # = 50mm
    BEAM_T  = LEFT_WK_BEARER_T     # = 3mm
    beam_bot = grate_bot - BEAM_SZ  # Z = 25mm (beam bottom)
    beam_top = grate_bot            # Z = 75mm (beam top = grate bottom)

    # Bearing strip
    STRIP_H = LEFT_WK_BEARING_STRIP  # = 25mm
    strip_bot = PROC_TRAY_RIM       # = 50mm
    strip_top = strip_bot + STRIP_H  # = 75mm

    # Cantilever arm from floor leg to walkway edge
    ARM_T = 5    # cantilever arm thickness (mm)
    ARM_END = tray_x + 30   # arm extends past tray rim to X=200

    # ── Figure ───────────────────────────────────────────────────────────────
    X_LO = OUTER_LEG_X - 80
    X_HI = LEFT_WK_R + BEAM_SZ / 2 + 150
    Z_LO = -30
    Z_HI = grate_top + 80

    fig, ax = plt.subplots(figsize=(18, 11))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(sx(X_LO), sx(X_HI))
    ax.set_ylim(sy(Z_LO), sy(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container floor ──────────────────────────────────────────────────────
    ax.add_patch(Rectangle((sx(X_LO), sy(-12)), sx(X_HI - X_LO), sy(12),
                            fc=C_FLOOR, ec=C_OUT, lw=1.0, hatch="///", zorder=2))

    # ── Processing tray ──────────────────────────────────────────────────────
    # Tray left rim (vertical wall)
    ax.add_patch(Rectangle((sx(tray_x - TRAY_WALL), sy(0)),
                            sx(TRAY_WALL), sy(PROC_TRAY_RIM),
                            fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=4))
    # Tray floor extending right
    tray_floor_end = X_HI - 40
    ax.add_patch(Rectangle((sx(tray_x), sy(0)),
                            sx(tray_floor_end - tray_x), sy(TRAY_FLOOR_T),
                            fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))
    # Sawtooth break line on tray floor
    bx = sx(tray_floor_end)
    z_lo, z_hi = 0, TRAY_FLOOR_T
    zz = np.linspace(z_lo, z_hi, 5)
    ax.plot([bx - 3, bx + 3, bx - 3, bx + 3, bx - 3],
            zz, color=C_OUT, lw=1.0, zorder=5)
    # Label tray rim
    leader(ax, sx(tray_x - TRAY_WALL / 2), sy(PROC_TRAY_RIM / 2),
           sx(tray_x + 45), sy(PROC_TRAY_RIM + 5),
           f"TRAY RIM\n{PROC_TRAY_RIM}mm (304 SS)",
           color=C_TRAY, fs=5.5,
           ha="center", va="bottom", arrow_style="-|>", font=FONT)

    # ── Bearing strip (25×25mm Al angle on tray rim) ─────────────────────────
    C_SUPPORT = "#D08020"
    ax.add_patch(Rectangle((sx(tray_x - TRAY_WALL), sy(strip_bot)),
                            sx(STRIP_H + TRAY_WALL), sy(STRIP_H),
                            fc=C_SUPPORT, ec=C_OUT, lw=1.2, zorder=6))
    # Cross-hatch for aluminum
    for dz in range(3, STRIP_H, 5):
        ax.plot([sx(tray_x - TRAY_WALL + 1), sx(tray_x + STRIP_H - 1)],
                [sy(strip_bot + dz), sy(strip_bot + dz - 3)],
                color=C_OUT, lw=0.3, alpha=0.4, zorder=7)
    leader(ax, sx(tray_x - STRIP_H * 0.7), sy(strip_bot + STRIP_H / 2 + 12),
           sx(tray_x + STRIP_H / 2 - 40), sy(strip_bot + STRIP_H + 18),
           f"BEARING STRIP\n25\u00d725\u00d73mm Al ANGLE\nON TRAY RIM\n(REMOVABLE)",
           color=C_SUPPORT, fs=6,
           ha="center", va="bottom", arrow_style="-|>", font=FONT)

    # ── Floor-standing support leg (cargo door side) ─────────────────────────
    # Rubber pad on floor
    ax.add_patch(Rectangle((sx(OUTER_LEG_X - BASE_W / 2), sy(0)),
                            sx(BASE_W), sy(RUBBER_T),
                            fc="#333333", ec=C_OUT, lw=0.6, zorder=6))
    # Foot plate on rubber pad
    foot_bot = RUBBER_T
    foot_top = foot_bot + BASE_T
    ax.add_patch(Rectangle((sx(OUTER_LEG_X - BASE_W / 2), sy(foot_bot)),
                            sx(BASE_W), sy(BASE_T),
                            fc=C_SUPPORT, ec=C_OUT, lw=1.0, zorder=6))
    # Vertical post on foot plate
    ax.add_patch(Rectangle((sx(OUTER_LEG_X - LEG_W / 2), sy(foot_top)),
                            sx(LEG_W), sy(LEG_TOP - ARM_T - foot_top),
                            fc=C_SUPPORT, ec=C_OUT, lw=1.2, zorder=6))
    # Hollow tube detail
    ax.add_patch(Rectangle((sx(OUTER_LEG_X - LEG_W / 2 + LEG_T), sy(foot_top + LEG_T)),
                            sx(LEG_W - 2 * LEG_T),
                            sy(LEG_TOP - ARM_T - foot_top - 2 * LEG_T),
                            fc="#F0E0C8", ec=C_OUT, lw=0.4, zorder=7))
    # Cantilever arm (from leg top to past tray rim)
    ax.add_patch(Rectangle((sx(OUTER_LEG_X - LEG_W / 2), sy(LEG_TOP - ARM_T)),
                            sx(ARM_END - OUTER_LEG_X + LEG_W / 2), sy(ARM_T),
                            fc=C_SUPPORT, ec=C_OUT, lw=1.0, zorder=8))

    # Leg label
    leader(ax, sx(OUTER_LEG_X), sy(LEG_TOP / 2 - 5),
           sx(OUTER_LEG_X - 40), sy(LEG_TOP * 0.85),
           f"FLOOR LEG\n{LEG_W}\u00d7{LEG_W}\u00d7{LEG_T}mm Al SHS\n"
           f"(\u00d7{LEFT_WK_LEG_N}, ON BARE FLOOR)\n"
           f"WITH CANTILEVER ARM",
           color=C_SUPPORT, fs=5.5,
           ha="center", va="top", arrow_style="-|>", font=FONT)
    leader(ax, sx(OUTER_LEG_X), sy(RUBBER_T / 2),
           sx(OUTER_LEG_X - 50), sy(-15),
           "RUBBER PAD", color="#333333", fs=5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Bearer beam (processing tray side, X=470) ────────────────────────────
    # Cross-section of 50×50×3mm Al RHS at X=470
    ax.add_patch(Rectangle((sx(LEFT_WK_R - BEAM_SZ / 2), sy(beam_bot)),
                            sx(BEAM_SZ), sy(BEAM_SZ),
                            fc=C_SUPPORT, ec=C_OUT, lw=1.5, zorder=8))
    # Hollow interior
    ax.add_patch(Rectangle((sx(LEFT_WK_R - BEAM_SZ / 2 + BEAM_T), sy(beam_bot + BEAM_T)),
                            sx(BEAM_SZ - 2 * BEAM_T), sy(BEAM_SZ - 2 * BEAM_T),
                            fc="#F0E0C8", ec=C_OUT, lw=0.5, zorder=9))
    # Beam label
    leader(ax, sx(LEFT_WK_R + BEAM_SZ / 2 + 2), sy(beam_bot + BEAM_SZ / 2),
           sx(LEFT_WK_R + BEAM_SZ / 2 + 45), sy(beam_bot + BEAM_SZ * 1.15),
           f"BEARER BEAM\n{BEAM_SZ}\u00d7{BEAM_SZ}\u00d7{BEAM_T}mm Al RHS\n"
           f"SPANS {WALKWAY_LEFT_SPAN}mm ALONG Yd\n"
           f"BOLTED TO NEAR/FAR\n"
           f"BRACKET VERT LEGS\n"
           f"(REMOVABLE)",
           color=C_SUPPORT, fs=5.5,
           ha="left", va="top", arrow_style="-|>", font=FONT)

    # ── Grating resting on supports (ghost) ──────────────────────────────────
    C_LEFT_WK = "#A8C8A8"
    ax.add_patch(Rectangle((sx(LEFT_WK_L), sy(grate_bot)),
                            sx(WALKWAY_W), sy(WALKWAY_GRATE_T),
                            fc=C_LEFT_WK, ec=C_OUT, lw=1.2, ls="--",
                            alpha=0.4, zorder=10))
    # Bearing bars in grating
    bar_spacing = 34.2
    bar_w_vis = 3
    for x in np.arange(LEFT_WK_L + bar_w_vis, LEFT_WK_R - bar_w_vis, bar_spacing):
        ax.add_patch(Rectangle((sx(x), sy(grate_bot)),
                                sx(bar_w_vis), sy(WALKWAY_GRATE_T),
                                fc="#8AAA8A", ec=C_OUT, lw=0.3, alpha=0.4, zorder=11))
    ax.text(sx((LEFT_WK_L + LEFT_WK_R) / 2), sy(grate_top + 3),
            f"LEFT WALKWAY GRATING ({WALKWAY_GRATE_T}mm)\nREMOVABLE LIFT-OUT",
            ha="center", va="bottom", fontsize=6.5, color="#206020",
            fontweight="bold", **FONT, zorder=15)

    # ── Contact highlights ───────────────────────────────────────────────────
    # Grating rests on bearer beam top (Z=75mm)
    ax.plot([sx(LEFT_WK_R - BEAM_SZ / 2 + 3), sx(LEFT_WK_R + BEAM_SZ / 2 - 3)],
            [sy(beam_top), sy(beam_top)],
            color="#CC4400", lw=3.0, zorder=12)
    # Grating rests on cantilever arm top
    ax.plot([sx(OUTER_LEG_X - LEG_W / 2), sx(ARM_END)],
            [sy(LEG_TOP), sy(LEG_TOP)],
            color="#CC4400", lw=2.5, zorder=12)
    # Grating rests on bearing strip top
    ax.plot([sx(tray_x - TRAY_WALL), sx(tray_x + STRIP_H)],
            [sy(strip_top), sy(strip_top)],
            color="#CC4400", lw=2.0, zorder=12)

    # ── "NO TRAY CONTACT" annotation ─────────────────────────────────────────
    # Arrow pointing to clear gap above tray floor
    gap_x = (tray_x + 50 + LEFT_WK_R - BEAM_SZ / 2) / 2
    ax.annotate("ZERO TRAY\nCONTACT",
                xy=(sx(gap_x), sy(TRAY_FLOOR_T + 3)),
                xytext=(sx(gap_x), sy(TRAY_FLOOR_T + 25)),
                ha="center", va="bottom", fontsize=6, color="#208020",
                fontweight="bold", fontfamily="monospace",
                arrowprops=dict(arrowstyle="-|>", color="#208020", lw=1.2),
                zorder=15)

    # ── Dimension lines ──────────────────────────────────────────────────────
    # Full walkway width
    draw_dim_h(ax, sx(LEFT_WK_L), sx(LEFT_WK_R), sy(grate_top + 18),
               f"{WALKWAY_W}mm WALKWAY WIDTH",
               offset=sy(5), fs=6.5, font=FONT)

    # Outer leg position from tray rim
    draw_dim_h(ax, sx(OUTER_LEG_X), sx(tray_x), sy(-18),
               f"{int(tray_x - OUTER_LEG_X)}mm",
               offset=sy(3), fs=5.5, above=False, font=FONT)

    # Cantilever arm reach
    draw_dim_h(ax, sx(OUTER_LEG_X - LEG_W / 2), sx(ARM_END), sy(LEG_TOP + 5),
               f"{int(ARM_END - OUTER_LEG_X + LEG_W / 2)}mm ARM",
               offset=sy(3), fs=5.5, font=FONT)

    # Bearer beam section size
    draw_dim_h(ax, sx(LEFT_WK_R - BEAM_SZ / 2), sx(LEFT_WK_R + BEAM_SZ / 2),
               sy(beam_bot - 8),
               f"{BEAM_SZ}mm",
               offset=sy(3), fs=5.5, above=False, font=FONT)

    # Height dimensions (right side)
    dim_x_r = LEFT_WK_R + BEAM_SZ / 2 + 30
    draw_dim_v(ax, sx(dim_x_r + 5), sy(0), sy(grate_top),
               f"{int(grate_top)}mm DECK", offset=sx(6), fs=6, right=True, font=FONT)
    draw_dim_v(ax, sx(dim_x_r - 5), sy(0), sy(beam_top),
               f"{beam_top}mm BEAM TOP", offset=sx(6), fs=5.5, right=True, font=FONT)
    draw_dim_v(ax, sx(dim_x_r - 20), sy(0), sy(beam_bot),
               f"{beam_bot}mm\nBEAM\nBOT", offset=sx(6), fs=5.5, right=True, font=FONT)

    # Tray rim height (left side)
    draw_dim_v(ax, sx(tray_x + STRIP_H + 25), sy(0), sy(PROC_TRAY_RIM),
               f"{PROC_TRAY_RIM}mm\nRIM",
               offset=sx(6), fs=5.5, right=True, color=C_TRAY, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    leg_spacing = int(WALKWAY_LEFT_SPAN / (LEFT_WK_LEG_N + 1))
    notes_x = sx(X_LO + 5)
    notes_top = sy(Z_HI - 3)
    notes = [
        "LEFT WALKWAY SUPPORT SYSTEM:",
        "",
        f"1. BEARER BEAM ({BEAM_SZ}\u00d7{BEAM_SZ}\u00d7{BEAM_T}mm Al RHS) at X={LEFT_WK_R}mm spans {WALKWAY_LEFT_SPAN}mm along Yd. Bolted to near/far bracket vertical legs.",
        f"2. {LEFT_WK_LEG_N} FLOOR LEGS at X={OUTER_LEG_X}mm ({leg_spacing}mm centers) on bare floor outside processing tray.",
        f"3. BEARING STRIP (25\u00d725\u00d73mm Al angle) on tray rim at X={LEFT_WK_L}mm.",
        f"4. ZERO tray contact \u2014 all supports outside or above processing tray.",
        f"5. All supports removable \u2014 lift out with grating before panel transport.",
    ]
    draw_notes(ax, notes, notes_x, notes_top, spacing=sy(6.5), fs=7, ha="left", width=sx(280), font=FONT)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 5 OF 6",
                drawing_title="PERIMETER WALKWAY",
                subtitle="DETAIL C \u2014 LEFT WALKWAY SUPPORT SYSTEM (REMOVABLE)",
                scale_note=f"Axes in mm \u00b7 VIEW ALONG Yd (NEAR \u2192 FAR)",
                height=0.07)

    fig.savefig("diagrams/walkway-sheet5.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet5.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet5.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 6 — Detail D: Bearer Beam Anti-Slip Restraint
#
# Two views of how the bearer beam (50×50×3mm Al RHS) sits on the
# near walkway bracket arm and is restrained against sliding in X.
#
# VIEW A — Side elevation looking along X (into container):
#   Horizontal = Yd (wall at left), Vertical = Z.
#   Corrugated wall rib, through-bolts, bracket vertical leg, gusset,
#   bracket arm with flat plate.  Beam extends from wall along Yd.
#   Lip (ghost — behind beam in X) and lock block (visible — in front).
#
# VIEW B — Plan view looking down (top right):
#   Horizontal = Yd (wall at left, interior at right), Vertical = X.
#   Shows flat plate on bracket arm, lip, beam, lock.
#   Beam extends from wall bracket in one direction only.
#
# Scale ≈ 4:1 for clarity.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet6():
    def sx(mm): return mm
    def sy(mm): return mm

    # ── Wall / bracket structural dimensions ─────────────────────────────────
    CORR_DEPTH = 38    # corrugation depth (mm)
    WALL_T     = 1.6   # wall steel thickness
    REINF_T    = 6     # reinforcing plate thickness
    REINF_H    = 180   # reinforcing plate height
    BRKT_T     = WALKWAY_BRACKET_T   # 8mm plate thickness
    BRKT_VERT  = WALKWAY_BRACKET_H   # 150mm vertical leg
    GUSSET_REACH = 70
    BOLT_D     = 12
    BOLT_R     = BOLT_D / 2
    WASHER_T   = 3
    NUT_H      = 10
    BOLT_HEAD  = 8

    # Bearer beam
    BEAM_SZ = LEFT_WK_BEARER_SIZE   # 50mm
    BEAM_T  = LEFT_WK_BEARER_T      # 3mm

    # Flat plate on bracket arm — wide enough for lip + beam + lock
    PLATE_T = 5       # plate thickness (mm)
    LIP_H   = 20      # lip height above plate surface (mm)
    LIP_T   = 5       # lip thickness (same stock as plate)
    LOCK_W  = 20      # lock block width in X (mm)
    LOCK_H  = 20      # lock block height above plate (mm)
    GAP     = 2       # clearance between beam and lock block
    THUMB_D = 8       # M8 thumb screw
    PLATE_W = LIP_T + BEAM_SZ + GAP + LOCK_W + 3   # ≈80mm

    # Z coordinates
    BRKT_ARM_Z = WALKWAY_H - WALKWAY_GRATE_T  # 75mm (arm top = beam top)
    beam_bot   = BRKT_ARM_Z - BEAM_SZ          # Z=25mm
    beam_top   = BRKT_ARM_Z                     # Z=75mm
    plate_top  = beam_bot                        # Z=25mm (plate supports beam)
    plate_bot  = plate_top - PLATE_T             # Z=20mm
    lip_top    = plate_top + LIP_H               # Z=45mm
    ARM_DEPTH  = BRKT_T + 2                      # 10mm arm visual depth
    arm_bot    = plate_bot - ARM_DEPTH           # arm is below plate
    grate_bot  = beam_top                         # Z=75mm
    grate_top  = grate_bot + WALKWAY_GRATE_T      # Z=100mm

    # Show beam extending 250mm from wall
    BEAM_SHOW = 250

    # ── Figure ───────────────────────────────────────────────────────────────
    YD_LO = -100
    YD_HI = BEAM_SHOW + 200
    Z_LO  = -60
    Z_HI  = BRKT_VERT + 220   # tightened to match lowered Views B/C

    fig, ax = plt.subplots(figsize=(18, 15))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(sx(YD_LO), sx(YD_HI))
    ax.set_ylim(sy(Z_LO), sy(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ══════════════════════════════════════════════════════════════════════════
    # VIEW A — Side elevation looking along X (into container)
    # Horizontal = Yd (wall at left), Vertical = Z
    # ══════════════════════════════════════════════════════════════════════════

    # View A title (above content, below Views B/C)
    ax.text(sx(YD_LO + 50), sy(BRKT_VERT + 135),
            "VIEW A \u2014 SIDE ELEVATION\n(LOOKING ALONG X INTO CONTAINER)",
            ha="left", va="top", fontsize=7, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── Container floor ──────────────────────────────────────────────────────
    ax.add_patch(Rectangle((sx(YD_LO), sy(-12)),
                            sx(BEAM_SHOW + 100 - YD_LO), sy(12),
                            fc=C_FLOOR, ec=C_OUT, lw=1.0, hatch="///", zorder=2))

    # ── Processing tray (ghost — for consistency with other sheets) ─────────
    TRAY_RIM_YD = PROC_TRAY_YD_NEAR   # = 80mm from wall
    TRAY_FLOOR_S = 2                   # tray floor thickness
    TRAY_WALL_S  = 3                   # tray wall thickness
    # Tray floor (extends from rim toward interior)
    ax.add_patch(Rectangle((sx(TRAY_RIM_YD), sy(0)),
                            sx(BEAM_SHOW - TRAY_RIM_YD + 30), sy(TRAY_FLOOR_S),
                            fc=C_TRAY, ec=C_OUT, lw=0.6, alpha=0.4, zorder=3))
    # Tray rim (vertical wall at Yd = 80mm)
    ax.add_patch(Rectangle((sx(TRAY_RIM_YD - TRAY_WALL_S), sy(0)),
                            sx(TRAY_WALL_S), sy(PROC_TRAY_RIM),
                            fc=C_TRAY, ec=C_OUT, lw=0.8, alpha=0.5, zorder=4))
    leader(ax, sx(TRAY_RIM_YD - TRAY_WALL_S / 2), sy(PROC_TRAY_RIM),
           sx(TRAY_RIM_YD + 30), sy(PROC_TRAY_RIM + 15),
           f"TRAY RIM\n{PROC_TRAY_RIM}mm",
           color=C_TRAY, fs=5,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # ── Corrugated wall (hollow rib profile — matching sheet 3) ──────────────
    ext_panel_yd = -CORR_DEPTH - WALL_T
    reinf_yd = ext_panel_yd - REINF_T
    wall_z_top = BRKT_VERT + 100  # 100mm above bracket top, then break line

    # Exterior wall steel panel
    ax.add_patch(Rectangle((sx(ext_panel_yd), sy(0)),
                            sx(WALL_T), sy(wall_z_top),
                            fc="#909098", ec=C_OUT, lw=1.2, zorder=3, hatch="///"))
    # Rib side wall (left)
    ax.add_patch(Rectangle((sx(-CORR_DEPTH), sy(0)),
                            sx(WALL_T), sy(wall_z_top),
                            fc="#909098", ec=C_OUT, lw=0.8, zorder=3, hatch="///"))
    # Rib interior face (at Yd=0)
    ax.add_patch(Rectangle((sx(-WALL_T), sy(0)),
                            sx(WALL_T), sy(wall_z_top),
                            fc="#909098", ec=C_OUT, lw=1.2, zorder=3, hatch="///"))
    # Air gap
    ax.add_patch(Rectangle((sx(-CORR_DEPTH + WALL_T), sy(0)),
                            sx(CORR_DEPTH - 2 * WALL_T), sy(wall_z_top),
                            fc="#F0F0F0", ec=C_DIM, lw=0.5, ls="--", zorder=2))
    ax.text(sx(-CORR_DEPTH / 2), sy(wall_z_top * 0.45),
            "AIR\nGAP", ha="center", va="center", fontsize=5, color=C_DIM,
            **FONT, zorder=15, style="italic")
    ax.plot([sx(0), sx(0)], [sy(0), sy(wall_z_top)],
            color=C_OUT, lw=2.0, zorder=4)
    # Sawtooth break line at top of wall (wall continues upward)
    n_teeth = 5
    brk_span = (WALL_T) - (ext_panel_yd - REINF_T)
    xs_brk = np.linspace(ext_panel_yd - REINF_T - brk_span * 0.10, WALL_T, n_teeth * 2 + 1)
    teeth_y = [wall_z_top + (3 if i % 2 == 1 else -3) for i in range(len(xs_brk))]
    ax.plot([sx(x) for x in xs_brk], [sy(y) for y in teeth_y],
            color=C_OUT, lw=1.2, zorder=15)
    ax.text(sx(-CORR_DEPTH / 2), sy(wall_z_top - 5),
            "CORRUGATED\nWALL RIB", ha="center", va="top", fontsize=5, color=C_DIM,
            fontweight="bold", **FONT, zorder=15)

    # Reinforcing plate (exterior)
    ax.add_patch(Rectangle((sx(reinf_yd), sy(0)),
                            sx(REINF_T), sy(REINF_H),
                            fc="#C08040", ec=C_OUT, lw=1.0, zorder=4))

    # ── Bracket vertical leg ─────────────────────────────────────────────────
    ax.add_patch(Rectangle((sx(0), sy(0)),
                            sx(BRKT_T), sy(BRKT_VERT),
                            fc=C_BRKT, ec=C_OUT, lw=1.5, zorder=6))
    leader(ax, sx(BRKT_T + 2), sy(BRKT_VERT - 10),
           sx(BRKT_T + 50), sy(BRKT_VERT + 10),
           f"BRACKET VERTICAL LEG\n{BRKT_T}mm PLATE \u00d7 {BRKT_VERT}mm\n(BOLTED TO WALL RIB)",
           color=C_BRKT, fs=5.5,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # ── Through-bolts (horizontal shanks — matching sheet 2) ─────────────────
    # Triangular pattern: 2× at Z=35 (flanking gusset in X), 1× at Z=120 (centered)
    # In this side view, the two Z=35 bolts overlap
    C_BOLT = "#505058"
    bolt_z_lo = 35
    bolt_z_hi = 120
    for bz in [bolt_z_lo, bolt_z_hi]:
        shank_left = reinf_yd
        shank_right = BRKT_T
        shank_hw = BOLT_R * 0.4
        ax.add_patch(Rectangle((sx(shank_left), sy(bz - shank_hw)),
                                sx(shank_right - shank_left), sy(shank_hw * 2),
                                fc=C_BOLT, ec=C_OUT, lw=0.8, zorder=10))
        # Hex head (exterior)
        ax.add_patch(Rectangle((sx(reinf_yd - BOLT_HEAD), sy(bz - BOLT_R)),
                                sx(BOLT_HEAD), sy(BOLT_D),
                                fc=C_BOLT, ec=C_OUT, lw=1.0, zorder=10))
        ax.add_patch(Rectangle((sx(reinf_yd - WASHER_T), sy(bz - BOLT_R - 1)),
                                sx(WASHER_T), sy(BOLT_D + 2),
                                fc="#808080", ec=C_OUT, lw=0.5, zorder=9))
        # Nut (interior)
        ax.add_patch(Rectangle((sx(BRKT_T), sy(bz - BOLT_R)),
                                sx(NUT_H), sy(BOLT_D),
                                fc=C_BOLT, ec=C_OUT, lw=1.0, zorder=10))
        ax.add_patch(Rectangle((sx(BRKT_T), sy(bz - BOLT_R - 1)),
                                sx(WASHER_T), sy(BOLT_D + 2),
                                fc="#808080", ec=C_OUT, lw=0.5, zorder=9))

    # ── Gusset triangle ──────────────────────────────────────────────────────
    # Gusset connects bracket vertical leg to underside of flat plate
    gusset_verts = [
        (sx(0), sy(0)),
        (sx(0), sy(plate_bot)),
        (sx(GUSSET_REACH), sy(plate_bot)),
    ]
    ax.add_patch(Polygon(gusset_verts, closed=True,
                         fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=5, alpha=0.85))
    ax.plot([sx(0), sx(GUSSET_REACH)], [sy(0), sy(plate_bot)],
            color=C_OUT, lw=1.5, zorder=6)

    # ── Flat plate (ghost — extends in X perpendicular to view) ──────────────
    # Shown as a thicker arm top surface (the plate sits on the arm)
    C_PLATE = "#A0A0B0"
    plate_show = 130   # show plate extending along Yd
    ax.add_patch(Rectangle((sx(0), sy(plate_bot)),
                            sx(plate_show), sy(PLATE_T),
                            fc=C_PLATE, ec=C_OUT, lw=1.2, alpha=0.5,
                            ls="--", zorder=5))
    leader(ax, sx(plate_show * 0.8), sy(plate_bot + PLATE_T / 2),
           sx(plate_show + 40), sy(plate_bot - 5),
           f"FLAT PLATE ({PLATE_T}mm \u00d7 {PLATE_W}mm WIDE)\n(GHOST \u2014 EXTENDS {PLATE_W}mm IN X)",
           color=C_PLATE, fs=5.5,
           ha="left", va="top", arrow_style="-|>", font=FONT)

    # ── Stop lip (solid — in front of beam, door side in X) ────────────────
    # The lip is in front of the beam in this view direction (looking along X).
    lip_yd_start = BRKT_T / 2
    lip_show_w = 80
    ax.add_patch(Rectangle((sx(lip_yd_start), sy(plate_top)),
                            sx(lip_show_w), sy(LIP_H),
                            fc=C_PLATE, ec=C_OUT, lw=1.5,
                            zorder=10))
    leader(ax, sx(lip_yd_start + lip_show_w / 2), sy(lip_top),
           sx(lip_yd_start + lip_show_w / 2), sy(lip_top + 15),
           f"STOP LIP {LIP_T}\u00d7{LIP_H}mm\nBENT UP FROM PLATE\nFORMS POCKET WITH BASE",
           color=C_PLATE, fs=5.5,
           ha="center", va="bottom", arrow_style="-|>", font=FONT)

    # ── Bearer beam (extends from wall along Yd) ─────────────────────────────
    C_SUPPORT = "#D08020"
    beam_yd_start = BRKT_T / 2
    ax.add_patch(Rectangle((sx(beam_yd_start), sy(beam_bot)),
                            sx(BEAM_SHOW - beam_yd_start), sy(BEAM_SZ),
                            fc=C_SUPPORT, ec=C_OUT, lw=1.5, zorder=7))
    # Hollow interior
    ax.add_patch(Rectangle((sx(beam_yd_start + BEAM_T), sy(beam_bot + BEAM_T)),
                            sx(BEAM_SHOW - beam_yd_start - 2 * BEAM_T),
                            sy(BEAM_SZ - 2 * BEAM_T),
                            fc="#F0E0C8", ec=C_OUT, lw=0.5, zorder=8))
    # Sawtooth break line at far end
    bx_beam = sx(BEAM_SHOW)
    z_lo_beam, z_hi_beam = sy(beam_bot + 2), sy(beam_top - 2)
    zz_beam = np.linspace(z_lo_beam, z_hi_beam, 7)
    ax.plot([bx_beam - 3, bx_beam + 3, bx_beam - 3, bx_beam + 3,
             bx_beam - 3, bx_beam + 3, bx_beam - 3],
            zz_beam, color=C_OUT, lw=1.0, zorder=9)
    ax.text(sx((beam_yd_start + BEAM_SHOW) * 0.7), sy(beam_bot * 1.5),
            f"BEARER BEAM {BEAM_SZ}\u00d7{BEAM_SZ}\u00d7{BEAM_T}mm Al RHS\n"
            f"(SPANS {WALKWAY_LEFT_SPAN}mm TO FAR BRACKET)",
            ha="center", va="top", fontsize=6, color=C_SUPPORT,
            fontweight="bold", **FONT, zorder=15)

    # ── Lock block (ghost — behind beam, interior/wall side in X) ──────────────
    # The lock is behind the beam in this view.
    # Lock slides on a 50mm slot in the plate; secured with bolt + washer below.
    SLOT_L = 50       # slot length along Yd (mm)
    BOLT_DIA = 8      # M8 bolt
    WASHER_DIA = 16   # washer outer diameter
    NUT_H_LOCK = 6    # nut height
    lock_yd_mid = beam_yd_start + 60
    # Lock block (ghost)
    ax.add_patch(Rectangle((sx(lock_yd_mid - LOCK_W / 2), sy(plate_top)),
                            sx(LOCK_W), sy(LOCK_H),
                            fc=C_BOLT, ec=C_OUT, lw=1.0, ls="--",
                            zorder=6, alpha=0.3))
    # Bolt shank through block and slot (ghost)
    ax.add_patch(Rectangle((sx(lock_yd_mid - 2), sy(plate_bot - NUT_H_LOCK)),
                            sx(4), sy(PLATE_T + LOCK_H + NUT_H_LOCK),
                            fc=C_BOLT, ec=C_OUT, lw=0.4, ls="--",
                            zorder=5, alpha=0.3))
    # Washer + nut below plate (ghost)
    ax.add_patch(Rectangle((sx(lock_yd_mid - WASHER_DIA / 2),
                             sy(plate_bot - NUT_H_LOCK)),
                            sx(WASHER_DIA), sy(NUT_H_LOCK),
                            fc=C_BOLT, ec=C_OUT, lw=0.5, ls="--",
                            zorder=5, alpha=0.25))
    leader(ax, sx(lock_yd_mid + LOCK_W / 2 + 2), sy(plate_top + LOCK_H / 2),
           sx(lock_yd_mid + 60), sy(plate_top + LOCK_H + 10),
           f"LOCK BLOCK {LOCK_W}\u00d7{LOCK_H}mm\n(GHOST \u2014 BEHIND BEAM)\nM{BOLT_DIA} BOLT THROUGH\n{SLOT_L}mm SLOT \u2014 SEE VIEW C",
           color=C_BOLT, fs=5.5,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # ── Grating (ghost) ─────────────────────────────────────────────────────
    C_LEFT_WK = "#A8C8A8"
    ax.add_patch(Rectangle((sx(-15), sy(grate_bot)),
                            sx(WALKWAY_W + 20), sy(WALKWAY_GRATE_T),
                            fc=C_LEFT_WK, ec=C_OUT, lw=0.8, ls="--",
                            alpha=0.25, zorder=4))
    # ── Grating clip (innermost edge, toward processing tray) ──────────
    clip_yd = WALKWAY_W - 20
    clip_w = 8
    clip_below = 12
    clip_above = 5
    clip_bot_z = grate_bot - clip_below
    clip_top_z = grate_top + clip_above
    ax.add_patch(Rectangle((sx(clip_yd), sy(clip_bot_z)),
                            sx(clip_w), sy(clip_top_z - clip_bot_z),
                            fc="#505058", ec=C_OUT, lw=0.8, zorder=9))
    leader(ax, sx(clip_yd + clip_w + 2), sy(grate_top),
           sx(clip_yd + 40), sy(grate_top + 15),
           "GRATING CLIP\n(REMOVABLE)", color="#505058", fs=5.5,
           ha="left", va="center", arrow_style="-|>", font=FONT)
    ax.text(sx(WALKWAY_W / 2), sy(grate_top + 3),
            f"GRATING (GHOST) \u2014 Z={grate_bot}\u2013{grate_top}mm",
            ha="center", va="bottom", fontsize=5.5, color="#206020",
            **FONT, alpha=0.5, zorder=15)

    # ── Dimension lines (side elevation) ─────────────────────────────────────
    draw_dim_v(ax, sx(BEAM_SHOW + 15), sy(beam_bot), sy(beam_top),
               f"{BEAM_SZ}mm", offset=sx(6), fs=6, right=True, font=FONT)
    draw_dim_v(ax, sx(BEAM_SHOW + 25), sy(0), sy(grate_top),
               f"{int(grate_top)}mm DECK", offset=sx(6), fs=5.5,
               right=True, font=FONT)
    draw_dim_v(ax, sx(-CORR_DEPTH - 20), sy(0), sy(BRKT_VERT),
               f"{BRKT_VERT}mm VERT LEG", offset=sx(6), fs=5.5,
               right=False, font=FONT)

    # ══════════════════════════════════════════════════════════════════════════
    # VIEW B — Plan view (looking down) — top middle of page
    # Horizontal = Yd (wall at left), Vertical = X (interior at top,
    # door at bottom).  Beam extends one direction only (from wall inward).
    # ══════════════════════════════════════════════════════════════════════════
    PV_OX = 60
    PV_OY = BRKT_VERT + 65
    PV_S  = 0.8125   # nested magnification (was 3.25 / S where S=4.0)
    def px(mm): return sx(PV_OX + mm * PV_S)
    def py(mm): return sy(PV_OY + mm * PV_S)

    ax.text(px(60), py(115), "VIEW B \u2014 PLAN (LOOKING DOWN)",
            ha="center", va="bottom", fontsize=7, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # Axis labels
    ax.text(px(-15), py(90), "\u2190 INT.\n(WALL\nSIDE)", ha="center", va="center",
            fontsize=5.5, color=C_DIM, **FONT, zorder=15)
    ax.text(px(-15), py(10), "DOOR\nSIDE \u2192", ha="center", va="center",
            fontsize=5.5, color=C_DIM, **FONT, zorder=15)

    # Wall stub at Yd=0 (left edge)
    wall_pv_w = 5   # wall thickness in plan
    ax.add_patch(Rectangle((px(-wall_pv_w), py(0)),
                            px(0) - px(-wall_pv_w),
                            py(100) - py(0),
                            fc="#909098", ec=C_OUT, lw=1.2, zorder=3, hatch="///"))
    ax.text(px(-wall_pv_w / 2), py(105),
            "WALL", ha="center", va="bottom", fontsize=5.5, color=C_DIM,
            fontweight="bold", **FONT, zorder=15)

    # Bracket vertical leg stub (at wall)
    brkt_pv_depth = 15  # visual depth in Yd
    brkt_pv_x_ctr = 50  # center in X coords
    ax.add_patch(Rectangle((px(0), py(brkt_pv_x_ctr - 8)),
                            px(brkt_pv_depth) - px(0),
                            py(brkt_pv_x_ctr + 8) - py(brkt_pv_x_ctr - 8),
                            fc=C_BRKT, ec=C_OUT, lw=1.0, zorder=5))

    # Flat plate (extends in X from bracket, shown as wide rectangle)
    plate_pv_yd_start = brkt_pv_depth   # starts at end of bracket stub
    plate_pv_yd_w = 40                  # plate length along Yd (short — just at bracket)
    plate_pv_x_start = brkt_pv_x_ctr - PLATE_W / 2
    plate_pv_x_end   = brkt_pv_x_ctr + PLATE_W / 2
    ax.add_patch(Rectangle((px(plate_pv_yd_start), py(plate_pv_x_start)),
                            px(plate_pv_yd_start + plate_pv_yd_w) - px(plate_pv_yd_start),
                            py(plate_pv_x_end) - py(plate_pv_x_start),
                            fc=C_PLATE, ec=C_OUT, lw=1.0, zorder=4, alpha=0.3))
    ax.text(px(plate_pv_yd_start + plate_pv_yd_w / 2),
            py(plate_pv_x_start - 3),
            f"FLAT PLATE\n({PLATE_W}mm WIDE)", ha="center", va="top",
            fontsize=5, color=C_PLATE, **FONT, zorder=15, alpha=0.6)

    # Slot in plate (50mm long along Yd, visible through plate)
    slot_pv_yd_start = plate_pv_yd_start + (plate_pv_yd_w - SLOT_L) / 2
    slot_pv_w = BOLT_DIA + 2   # slot width in X (just wider than bolt)
    slot_pv_x_ctr = plate_pv_x_end - LOCK_W / 2 - GAP  # aligned with lock center
    ax.add_patch(Rectangle((px(slot_pv_yd_start), py(slot_pv_x_ctr - slot_pv_w / 2)),
                            px(slot_pv_yd_start + SLOT_L) - px(slot_pv_yd_start),
                            py(slot_pv_x_ctr + slot_pv_w / 2) - py(slot_pv_x_ctr - slot_pv_w / 2),
                            fc="white", ec=C_OUT, lw=1.0, zorder=6))
    ax.text(px(slot_pv_yd_start + SLOT_L + 2), py(slot_pv_x_ctr),
            f"{SLOT_L}mm\nSLOT", ha="left", va="center", fontsize=4.5, color=C_DIM,
            **FONT, zorder=15)

    # Lock block (interior/wall side = high X = top in plan view)
    lock_pv_x = plate_pv_x_end - LOCK_W
    lock_pv_yd_ctr = plate_pv_yd_start + plate_pv_yd_w / 2
    ax.add_patch(Rectangle((px(lock_pv_yd_ctr - LOCK_W / 2), py(lock_pv_x)),
                            px(lock_pv_yd_ctr + LOCK_W / 2) - px(lock_pv_yd_ctr - LOCK_W / 2),
                            py(lock_pv_x + LOCK_W) - py(lock_pv_x),
                            fc=C_BOLT, ec=C_OUT, lw=1.0, zorder=8))
    # Bolt circle (through slot)
    ax.add_patch(Circle((px(lock_pv_yd_ctr), py(lock_pv_x + LOCK_W / 2)),
                         (px(BOLT_DIA / 2 + 1) - px(0)),
                         fc=C_BOLT, ec=C_OUT, lw=0.8, zorder=9))
    ax.text(px(plate_pv_yd_start + plate_pv_yd_w + 20), py(lock_pv_x + LOCK_W / 2),
            f"LOCK + M{BOLT_DIA}\nBOLT", ha="left", va="center", fontsize=5, color=C_BOLT,
            fontweight="bold", **FONT, zorder=15)

    # Beam (extends from bracket outward along Yd — ONE direction only)
    beam_pv_w = 120   # show 120mm of beam extending from bracket
    beam_pv_x = lock_pv_x - GAP - BEAM_SZ   # beam below lock (door side)
    ax.add_patch(Rectangle((px(plate_pv_yd_start), py(beam_pv_x)),
                            px(plate_pv_yd_start + beam_pv_w) - px(plate_pv_yd_start),
                            py(beam_pv_x + BEAM_SZ) - py(beam_pv_x),
                            fc=C_SUPPORT, ec=C_OUT, lw=1.2, zorder=6))
    # Hollow
    ax.add_patch(Rectangle((px(plate_pv_yd_start + BEAM_T), py(beam_pv_x + BEAM_T)),
                            px(plate_pv_yd_start + beam_pv_w - BEAM_T) - px(plate_pv_yd_start + BEAM_T),
                            py(beam_pv_x + BEAM_SZ - BEAM_T) - py(beam_pv_x + BEAM_T),
                            fc="#F0E0C8", ec=C_OUT, lw=0.5, zorder=7))
    ax.text(px(plate_pv_yd_start + beam_pv_w / 2), py(beam_pv_x + BEAM_SZ / 2),
            "BEAM", ha="center", va="center", fontsize=6.5, color=C_SUPPORT,
            fontweight="bold", **FONT, zorder=15)
    # Break line at far end (beam continues to far bracket)
    bx_far = px(plate_pv_yd_start + beam_pv_w)
    zz_brk = np.linspace(py(beam_pv_x + 2), py(beam_pv_x + BEAM_SZ - 2), 5)
    ax.plot([bx_far - 2, bx_far + 2, bx_far - 2, bx_far + 2, bx_far - 2],
            zz_brk, color=C_OUT, lw=0.8, zorder=10)

    # Lip (door side = low X = bottom in plan view)
    lip_pv_x = beam_pv_x - LIP_T   # lip below beam
    ax.add_patch(Rectangle((px(plate_pv_yd_start), py(lip_pv_x)),
                            px(plate_pv_yd_start + plate_pv_yd_w) - px(plate_pv_yd_start),
                            py(lip_pv_x + LIP_T) - py(lip_pv_x),
                            fc=C_PLATE, ec=C_OUT, lw=1.2, zorder=8))
    ax.text(px(plate_pv_yd_start + plate_pv_yd_w + 3), py(lip_pv_x + LIP_T / 2),
            "LIP", ha="left", va="center", fontsize=5, color=C_PLATE,
            fontweight="bold", **FONT, zorder=15)

    # Plan view border
    pv_border_bot = lip_pv_x - 12
    pv_border_top = lock_pv_x + LOCK_W + 12
    ax.add_patch(Rectangle((px(-wall_pv_w - 3), py(pv_border_bot)),
                            px(plate_pv_yd_start + beam_pv_w + 5) - px(-wall_pv_w - 3),
                            py(pv_border_top) - py(pv_border_bot),
                            fc="none", ec=C_DIM, lw=0.8, ls="--", zorder=4))

    # ══════════════════════════════════════════════════════════════════════════
    # VIEW C — Lock block detail (cross-section looking along Yd) — top right of page
    # Horizontal = X, Vertical = Z.  Shows slot in plate, lock block,
    # bolt through slot, washer + nut underneath.
    # ══════════════════════════════════════════════════════════════════════════
    VC_OX = 300
    VC_OY = BRKT_VERT + 108   # bottom-aligned with View B
    VC_S  = 0.975   # nested magnification (was 3.9 / S where S=4.0)
    def cx(mm): return sx(VC_OX + mm * VC_S)
    def cy(mm): return sy(VC_OY + mm * VC_S)

    ax.text(cx(35), cy(65), "VIEW C \u2014 LOCK DETAIL\n(SECTION ALONG Yd)",
            ha="center", va="bottom", fontsize=7, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)
    ax.text(cx(35), cy(60),
            "\u2190 INT.         DOOR \u2192",
            ha="center", va="top", fontsize=5.5, color=C_DIM,
            **FONT, zorder=15)

    # Flat plate cross-section with slot
    # Plate extends across view; slot is a gap in the plate
    plate_cx_left = 0
    plate_cx_right = 70
    slot_cx_ctr = 35   # slot center in X coords
    slot_cx_w = BOLT_DIA + 2   # slot width = 10mm
    slot_left = slot_cx_ctr - slot_cx_w / 2
    slot_right = slot_cx_ctr + slot_cx_w / 2

    # Plate left of slot
    ax.add_patch(Rectangle((cx(plate_cx_left), cy(0)),
                            cx(slot_left) - cx(plate_cx_left), cy(PLATE_T) - cy(0),
                            fc=C_PLATE, ec=C_OUT, lw=1.5, hatch="///", zorder=6))
    # Plate right of slot
    ax.add_patch(Rectangle((cx(slot_right), cy(0)),
                            cx(plate_cx_right) - cx(slot_right), cy(PLATE_T) - cy(0),
                            fc=C_PLATE, ec=C_OUT, lw=1.5, hatch="///", zorder=6))
    # Slot opening (white gap)
    ax.add_patch(Rectangle((cx(slot_left), cy(0)),
                            cx(slot_right) - cx(slot_left), cy(PLATE_T) - cy(0),
                            fc="white", ec=C_OUT, lw=0.8, zorder=5))
    ax.text(cx(plate_cx_right + 3), cy(PLATE_T / 2),
            f"FLAT PLATE\n({PLATE_T}mm)", ha="left", va="center",
            fontsize=5.5, color=C_PLATE, **FONT, zorder=15)

    # Lock block on top of plate
    lock_cx_left = slot_cx_ctr - LOCK_W / 2
    lock_cx_right = slot_cx_ctr + LOCK_W / 2
    ax.add_patch(Rectangle((cx(lock_cx_left), cy(PLATE_T)),
                            cx(lock_cx_right) - cx(lock_cx_left),
                            cy(PLATE_T + LOCK_H) - cy(PLATE_T),
                            fc=C_BOLT, ec=C_OUT, lw=1.5, hatch="///", zorder=8))
    ax.text(cx(slot_cx_ctr), cy(PLATE_T + LOCK_H / 2),
            f"LOCK\nBLOCK", ha="center", va="center",
            fontsize=6.5, color="white", fontweight="bold",
            **FONT, zorder=15)

    # Bolt shank (through block, through slot, extends below plate)
    bolt_shank_w = BOLT_DIA * 0.5   # visual width of shank
    ax.add_patch(Rectangle((cx(slot_cx_ctr - bolt_shank_w / 2),
                             cy(-NUT_H_LOCK)),
                            cx(slot_cx_ctr + bolt_shank_w / 2) - cx(slot_cx_ctr - bolt_shank_w / 2),
                            cy(PLATE_T + LOCK_H) - cy(-NUT_H_LOCK),
                            fc=C_BOLT, ec=C_OUT, lw=0.8, zorder=7))

    # Bolt head on top of lock block
    bolt_head_h = 5
    bolt_head_w = BOLT_DIA * 1.8
    ax.add_patch(Rectangle((cx(slot_cx_ctr - bolt_head_w / 2),
                             cy(PLATE_T + LOCK_H)),
                            cx(slot_cx_ctr + bolt_head_w / 2) - cx(slot_cx_ctr - bolt_head_w / 2),
                            cy(PLATE_T + LOCK_H + bolt_head_h) - cy(PLATE_T + LOCK_H),
                            fc=C_BOLT, ec=C_OUT, lw=1.0, zorder=10))
    leader(ax, cx(slot_cx_ctr + bolt_head_w / 2 + 1), cy(PLATE_T + LOCK_H + bolt_head_h / 2),
           cx(slot_cx_ctr + 30), cy(PLATE_T + LOCK_H + 20),
           f"M{BOLT_DIA} HEX BOLT",
           color=C_BOLT, fs=6.5,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # Washer below plate
    washer_t = 2
    ax.add_patch(Rectangle((cx(slot_cx_ctr - WASHER_DIA / 2),
                             cy(-washer_t)),
                            cx(slot_cx_ctr + WASHER_DIA / 2) - cx(slot_cx_ctr - WASHER_DIA / 2),
                            cy(0) - cy(-washer_t),
                            fc="#808080", ec=C_OUT, lw=1.0, zorder=8))

    # Nut below washer
    nut_w = BOLT_DIA * 1.6
    ax.add_patch(Rectangle((cx(slot_cx_ctr - nut_w / 2),
                             cy(-washer_t - NUT_H_LOCK)),
                            cx(slot_cx_ctr + nut_w / 2) - cx(slot_cx_ctr - nut_w / 2),
                            cy(-washer_t) - cy(-washer_t - NUT_H_LOCK),
                            fc=C_BOLT, ec=C_OUT, lw=1.0, zorder=8))
    leader(ax, cx(slot_cx_ctr + nut_w / 2 + 1), cy(-washer_t - NUT_H_LOCK / 2),
           cx(slot_cx_ctr + 30), cy(-washer_t - NUT_H_LOCK - 10),
           f"M{BOLT_DIA} NUT\n+ WASHER",
           color=C_BOLT, fs=6.5,
           ha="left", va="top", arrow_style="-|>", font=FONT)

    # Slot dimension
    draw_dim_h(ax, cx(slot_left), cx(slot_right),
               cy(-washer_t - NUT_H_LOCK - 18),
               f"{slot_cx_w}mm\nSLOT WIDTH", offset=cy(3) - cy(0), fs=5.5, font=FONT)
    # Lock block width
    draw_dim_h(ax, cx(lock_cx_left), cx(lock_cx_right),
               cy(PLATE_T + LOCK_H + bolt_head_h + 5),
               f"{LOCK_W}mm", offset=cy(3) - cy(0), fs=5.5, font=FONT)
    # Lock height
    draw_dim_v(ax, cx(plate_cx_right + 2), cy(PLATE_T), cy(PLATE_T + LOCK_H),
               f"{LOCK_H}", offset=cx(3) - cx(0), fs=5.5, right=True, font=FONT)

    # Slot length note (into page)
    ax.text(cx(slot_cx_ctr), cy(-washer_t - NUT_H_LOCK - 28),
            f"SLOT LENGTH: {SLOT_L}mm ALONG Yd\n(ALLOWS POSITION ADJUSTMENT)",
            ha="center", va="top", fontsize=5.5, color=C_DIM,
            **FONT, zorder=15)

    # View C border
    ax.add_patch(Rectangle((cx(-8), cy(-washer_t - NUT_H_LOCK - 35)),
                            cx(plate_cx_right + 10) - cx(-8),
                            cy(PLATE_T + LOCK_H + bolt_head_h + 15) - cy(-washer_t - NUT_H_LOCK - 35),
                            fc="none", ec=C_DIM, lw=0.8, ls="--", zorder=4))

    # ── Notes (right of View A) ─────────────────────────────────────────────
    notes_x = sx(YD_HI/2)
    notes_top = sy(BRKT_VERT + 20)
    notes = [
        "BEARER BEAM CONNECTION:",
        f"1. Flat plate ({PLATE_T}mm \u00d7 {PLATE_W}mm wide) welded to bracket arm.",
        f"2. Lip ({LIP_T}\u00d7{LIP_H}mm) bent up from plate edge \u2014 forms pocket.",
        f"3. Beam ({BEAM_SZ}\u00d7{BEAM_SZ}\u00d7{BEAM_T}mm Al RHS) sits in pocket, against lip.",
        f"4. Lock block + M{BOLT_DIA} bolt through {SLOT_L}mm slot in plate. Washer + nut below plate.",
        f"5. Slot allows position adjustment along Yd. Spanner removal.",
        f"6. Same at both ends (near + far bracket).",
    ]
    draw_notes(ax, notes, notes_x, notes_top, spacing=sy(6.5), fs=7, ha="left", width=sx(180), font=FONT)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 6 OF 6",
                drawing_title="PERIMETER WALKWAY",
                subtitle="DETAIL D \u2014 BEARER BEAM ANTI-SLIP RESTRAINT",
                scale_note="Axes in mm \u00b7 VIEWS A/B/C",
                height=0.07)

    fig.savefig("diagrams/walkway-sheet6.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet6.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet6.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    os.makedirs("diagrams", exist_ok=True)
    print("Generating perimeter walkway diagrams...")
    sheet1()  # plan view → sheet1.png
    sheet2()  # cross-section → sheet2.png
    sheet3()  # ceiling-hung → sheet3.png
    sheet4()  # butt joint → sheet4.png
    sheet5()  # left support → sheet5.png
    sheet6()  # bearer beam → sheet6.png
    print("Done.")
