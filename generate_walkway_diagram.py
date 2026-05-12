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

Sheet 2 — Cross-section through near (pinhole side) walkway:
  Detail view (~5:1) showing grated deck, wall-cantilevered bracket,
  tray rim clearance, and dimensional annotations.
  Section cut looking along X axis.  Wall-cantilevered bracket design:
  triangular gusset brackets bolted to container wall ribs — no legs,
  no beam, no floor contact.  Entire tray is clear for film loading.

Sheet 3 — Detail: Single bracket / wall attachment:
  Close-up of gusset bracket bolted to corrugated wall rib, showing
  reinforcing plate, M12 through-bolts, and grating clip.

Sheet 4 — Detail B: Right walkway bracket on angle iron:
  Bracket bolted to 50x50x5mm angle iron welded to flat end wall.

Sheet 5 — Detail C: Left walkway butt joint and panel clearance:
  View looking along Yd (near wall toward far wall), X horizontal, Z vertical.
  Shows left walkway grating (X=170-470, removable lift-out) meeting near
  walkway bracket arm at butt joint (X=470). Panel transport envelope
  (X=0-420) shown as ghost, confirming 50mm clearance to near walkway.
  Bearing strip and support cradle shown in cross-section.

Sheet 6 — Detail D: Left walkway support system (removable):
  Elevation showing all support elements: floor-standing leg (X=140, on bare
  floor) with cantilever arm, bearer beam (50×50×3mm Al RHS at X=470) spanning
  1,762mm between bracket vertical legs, and bearing strip on tray rim (X=170).
  Zero processing tray contact.

Sheet 7 — Detail E: Bearer beam to bracket connection:
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
from tbs_drawing import draw_dim_h, draw_dim_v, leader
from tbs_constants import (
    svg_path, SVG_DIR,
    C_LEN, C_WID, C_HGT,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_W, PROC_TRAY_D,
    PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR, PROC_TRAY_RIM,
    WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T,
    WALKWAY_BRACKET_H, WALKWAY_BRACKET_T, WALKWAY_BRACKET_SPACING,
    WALKWAY_ANGLE_IRON, WALKWAY_ANGLE_IRON_T, WALKWAY_LEFT_SPAN,
    CONTAINER_RIB_SPACING,
    WALKWAY_NEAR_YD, WALKWAY_FAR_YD, WALKWAY_LEFT_X, WALKWAY_RIGHT_X,
    PROC_OPEN_X_L, PROC_OPEN_X_R, PROC_OPEN_YD_N, PROC_OPEN_YD_F,
    PROC_OPEN_AREA,
    PANEL_SLIDE, PANEL_CENTER_T, PANEL_FLOOR_GAP,
    LEFT_WK_BEARER_SIZE, LEFT_WK_BEARER_T,
    LEFT_WK_LEG_N, LEFT_WK_LEG_SIZE, LEFT_WK_LEG_T, LEFT_WK_LEG_BASE,
    LEFT_WK_BEARING_STRIP,
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
# SHEET 1 — Cross-Section Through Near Walkway
#
# View: looking along X axis (into the container).  Section cut through
# the near (pinhole side) walkway at a bracket position.
# Horizontal = Yd (0 = pinhole wall, positive toward far wall)
# Vertical   = Z  (0 = floor, positive up)
# Scale ≈ 5:1 for clarity.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():
    S = 5.0   # scale factor

    def sx(mm): return mm * S
    def sy(mm): return mm * S

    # ── Structural dimensions (mm real) ──────────────────────────────────────
    TRAY_WALL  = 3     # tray wall thickness (SS)
    TRAY_FLOOR = 2     # tray floor thickness (SS)
    CORR_DEPTH = 38    # corrugation depth (mm)
    WALL_T     = 1.6   # wall steel thickness (mm)
    BRKT_ARM_H = WALKWAY_H - WALKWAY_GRATE_T  # = 75mm (bracket arm top Z)
    BRKT_T     = WALKWAY_BRACKET_T  # 8mm plate thickness
    BRKT_VERT  = WALKWAY_BRACKET_H  # 150mm vertical leg on wall
    REINF_W    = 80    # reinforcing plate width behind wall
    REINF_H    = 180   # reinforcing plate height
    REINF_T    = 6     # reinforcing plate thickness

    # Positions (mm real)
    TRAY_RIM_YD = PROC_TRAY_YD_NEAR  # = 80mm from wall

    # ── Figure ───────────────────────────────────────────────────────────────
    YD_LO = -100
    YD_HI = WALKWAY_W + 180
    Z_LO  = -70
    Z_HI  = WALKWAY_H + WALKWAY_GRATE_T + 80

    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(sx(YD_LO), sx(YD_HI))
    ax.set_ylim(sy(Z_LO), sy(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

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
    z_lo, z_hi = 0, TRAY_FLOOR * S
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

    # Through-bolts (2× M12) — horizontal shanks through wall + bracket
    # Matching sheet 3 convention: reinf plate → ext panel → air gap → rib → bracket → nut
    BOLT_D    = 12
    BOLT_R    = BOLT_D / 2
    BOLT_HEAD = 8    # hex head height (Yd direction)
    NUT_H     = 10   # nut height (Yd direction)
    WASHER_T  = 3
    C_BOLT    = "#505058"
    bolt_z1   = 30
    bolt_z2   = 120

    for bz in [bolt_z1, bolt_z2]:
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

    # Bolt label
    leader(ax, sx(reinf_yd - BOLT_HEAD - 2), sy(bolt_z1),
           sx(reinf_yd - 30), sy(bolt_z1 + 20),
           "2\u00d7 M12 THROUGH-\nBOLTS\nHEAD \u2192 REINF PLATE \u2192\nWALL \u2192 RIB \u2192\nBRACKET \u2192 NUT",
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
    draw_dim_v(ax, sx(WALKWAY_W + 35), sy(grate_bot), sy(grate_top),
               f"{WALKWAY_GRATE_T}mm\nDECK HEIGHT", offset=sx(8), fs=6.5, right=True, font=FONT)

    # Bracket vertical leg height
    draw_dim_v(ax, sx(reinf_yd - BOLT_HEAD - 45), sy(0), sy(BRKT_VERT),
               f"{BRKT_VERT}mm\nVERT LEG", offset=sx(8), fs=6.5, right=False, font=FONT)

    # Bracket arm height
    draw_dim_v(ax, sx(WALKWAY_W + 90), sy(0), sy(brkt_arm_z),
               f"{brkt_arm_z}mm\nARM TOP", offset=sx(8), fs=6.5, right=True, font=FONT)

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
               f"{CORR_DEPTH}mm\nCORR", offset=sy(14), fs=6, above=False, font=FONT)

    # Wall to tray rim
    draw_dim_h(ax, sx(0), sx(TRAY_RIM_YD), sy(-45),
               f"{TRAY_RIM_YD}mm", offset=sy(14), fs=6, above=False, font=FONT)

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
    notes_x = sx(WALKWAY_W + 60)
    notes_top = sy(Z_HI - 10)
    notes = [
        "CONSTRUCTION NOTES:",
        "",
        f"1. Grating: {WALKWAY_GRATE_T}mm press-locked galvanized steel,",
        f"   30\u00d73mm bearing bars at 34.2mm pitch.",
        f"2. Cantilever brackets: {BRKT_T}mm steel plate gusset,",
        f"   bolted to wall ribs at {WALKWAY_BRACKET_SPACING}mm centers.",
        f"3. NO legs, NO beam — entire tray floor clear",
        f"   for film loading. Zero tray contact.",
        f"4. 2\u00d7 M12 through-bolts per bracket, with",
        f"   reinforcing plate behind corrugated wall.",
        f"5. Grating clips to bracket arms — removable.",
        f"6. Right walkway: brackets on angle iron",
        f"   welded to flat end wall (no ribs).",
        f"7. Left walkway: REMOVABLE LIFT-OUT —",
        f"   no brackets (panel conflict). Rests on",
        f"   near/far butt joints. {WALKWAY_GRATE_T}mm grating.",
    ]
    for i, line in enumerate(notes):
        bold = i == 0
        ax.text(notes_x, notes_top - i * sy(6.5), line,
                ha="left", va="top", fontsize=5.5 if not bold else 6,
                color=C_OUT if bold else C_DIM,
                fontweight="bold" if bold else "normal",
                **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 7",
                drawing_title="PERIMETER WALKWAY",
                subtitle="CROSS-SECTION \u2014 NEAR WALKWAY (LOOKING ALONG X AXIS)",
                scale_note=f"SCALE \u2248 5:1 \u00b7 ALL DIMS IN mm \u00b7 SECTION AT BRACKET POSITION",
                height=0.07)

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
def sheet2():
    import matplotlib.patches as mpatches

    BRKT_MARK_W = 30   # bracket marker width in plan view (mm, visual)
    BRKT_MARK_D = 20   # bracket marker depth in plan view (mm, visual)

    # ── Figure ───────────────────────────────────────────────────────────────
    PAD_X = 300
    PAD_Y_BOT = 750   # extra room below for notes + title block
    PAD_Y_TOP = 300
    fig, ax = plt.subplots(figsize=(18, 12))
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
    # Left corners: BUTT JOINT (no miter) — near/far walkways start at X=LXR (470)
    # so they clear the panel transport envelope (max X=420).
    # Right corners: 45° miter as before (no panel conflict on right side).
    C_WK = "#D0C8B8"
    WK_ALPHA = 0.6
    W = WALKWAY_W

    LX  = WALKWAY_LEFT_X;   LXR = LX + W
    RX  = WALKWAY_RIGHT_X;  RXR = RX + W
    NY  = WALKWAY_NEAR_YD;  NYI = NY + W
    FY  = WALKWAY_FAR_YD;   FYO = FY + W
    TL  = PROC_TRAY_X_L;   TR = TL + PROC_TRAY_W

    # Near/far: butt joint at left (X=LXR), 45° miter at right (X=RX)
    # Left: simple rectangle (no miters)
    # Right: 45° miters both corners
    near_len = TR - LXR   # near/far walkway length (from butt joint to tray right)
    walkway_polys = [
        ("NEAR",  [(LXR, NY), (TR, NY), (RX, NYI), (LXR, NYI)],
         LXR, NY, near_len, W, True),
        ("FAR",   [(LXR, FYO), (TR, FYO), (RX, FY), (LXR, FY)],
         LXR, FY, near_len, W, True),
        ("LEFT",  [(LX, NY), (LX, FYO), (LXR, FYO), (LXR, NY)],
         LX, 0, W, C_WID, False),
        ("RIGHT", [(RXR, NY), (RXR, FYO), (RX, FY), (RX, NYI)],
         RX, 0, W, C_WID, False),
    ]

    for name, verts, wx, wy, ww, wh, is_x_axis in walkway_polys:
        # Walkway fill — polygon with mitered corners
        ax.add_patch(Polygon(verts, closed=True,
                             fc=C_WK, ec=C_OUT, lw=1.0, hatch="xx",
                             alpha=WK_ALPHA, zorder=4))

        # Wall bracket positions — small rectangles at wall edge
        if is_x_axis:
            # Near/far walkways: brackets along the long wall (Yd=0 or Yd=C_WID)
            # Bracket spacing along X axis at container rib positions
            x_start = wx
            x_end = wx + ww
            # Generate bracket X positions at rib spacing
            brkt_xs = np.arange(x_start + WALKWAY_BRACKET_SPACING / 2,
                                x_end, WALKWAY_BRACKET_SPACING)
            for bx in brkt_xs:
                if name == "NEAR":
                    # Brackets on pinhole wall (Yd=0), projecting inward
                    ax.add_patch(Rectangle((bx - BRKT_MARK_W / 2, NY),
                                 BRKT_MARK_W, BRKT_MARK_D,
                                 fc=C_BRKT, ec=C_OUT, lw=0.6, zorder=6))
                else:
                    # Brackets on far wall (Yd=C_WID), projecting inward
                    ax.add_patch(Rectangle((bx - BRKT_MARK_W / 2, FYO - BRKT_MARK_D),
                                 BRKT_MARK_W, BRKT_MARK_D,
                                 fc=C_BRKT, ec=C_OUT, lw=0.6, zorder=6))
        elif name == "RIGHT":
            # Right walkway: brackets on angle iron welded to far end wall
            yd_start = wy
            yd_end = wy + wh
            brkt_yds = np.arange(yd_start + WALKWAY_BRACKET_SPACING / 2,
                                 yd_end, WALKWAY_BRACKET_SPACING)
            for by in brkt_yds:
                ax.add_patch(Rectangle((RXR - BRKT_MARK_D, by - BRKT_MARK_W / 2),
                             BRKT_MARK_D, BRKT_MARK_W,
                             fc=C_BRKT, ec=C_OUT, lw=0.6, zorder=6))
        # LEFT walkway: NO brackets — removable lift-out section

        # Section label
        cx = wx + ww / 2
        cy = wy + wh / 2
        rot = 0 if is_x_axis else 90
        length = ww if is_x_axis else wh
        if name == "LEFT":
            lbl = f"LEFT WALKWAY\n{int(length)}\u00d7{WALKWAY_W}mm\nREMOVABLE LIFT-OUT"
        else:
            lbl = f"{name} WALKWAY\n{int(length)}\u00d7{WALKWAY_W}mm"
        ax.text(cx, cy, lbl,
                ha="center", va="center", fontsize=6, color=C_OUT,
                backgroundcolor="#FFFFFF",
                fontweight="bold", **FONT, zorder=7, rotation=rot)

    # ── Corner joints ────────────────────────────────────────────────────────
    # Right corners: 45° miter joints (near-right & far-right)
    right_miters = [
        (PROC_TRAY_X_R, 0, PROC_TRAY_X_R - W, W),
        (PROC_TRAY_X_R, C_WID, PROC_TRAY_X_R - W, C_WID - W),
    ]
    for x1, y1, x2, y2 in right_miters:
        ax.plot([x1, x2], [y1, y2], color=C_OUT, lw=1.5, zorder=8)

    # Left corners: butt joints (vertical line at X=LXR)
    # Near/far walkways start at X=LXR = 470, left walkway ends at X=LXR
    ax.plot([LXR, LXR], [NY, NYI], color=C_OUT, lw=1.5, zorder=8)   # near-left butt
    ax.plot([LXR, LXR], [FY, FYO], color=C_OUT, lw=1.5, zorder=8)   # far-left butt

    # Label one butt joint (bottom-left)
    leader(ax, LXR, W / 2, LXR - 350, W / 2 - 350,
           f"BUTT JOINT AT X={LXR}\n(LEFT WALKWAY LIFTS OUT\nCLEARS PANEL TRANSPORT\nENVELOPE AT X\u2264420)",
           color=C_OUT, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # Label one right miter
    mx_r = PROC_TRAY_X_R - W / 2
    leader(ax, mx_r, W / 2, mx_r + 350, W / 2 - 350,
           "45\u00b0 MITER JOINT", color=C_OUT, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

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
    ax.text(beam_x + 18, (NYI + FY) / 2,
            f"BEARER BEAM\n{LEFT_WK_BEARER_SIZE}\u00d7{LEFT_WK_BEARER_SIZE}"
            f"\u00d7{LEFT_WK_BEARER_T}mm\nAl RHS\n(REMOVABLE)",
            ha="left", va="center", fontsize=4.5, color=C_SUPPORT,
            fontweight="bold", **FONT, zorder=15, rotation=90)

    # Bearing strip on tray rim (X=170, continuous along Yd)
    strip_yd_start = NYI   # start at near walkway inner edge (Yd=300)
    strip_yd_end   = FY    # end at far walkway inner edge (Yd=1,962)
    ax.plot([LX, LX], [strip_yd_start, strip_yd_end],
            color=C_SUPPORT, lw=3.0, zorder=8, solid_capstyle="butt")
    ax.text(LX - 15, (strip_yd_start + strip_yd_end) / 2,
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
           leg_x - 200, c1_yd + leg_sz / 2 + 200,
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
    legend_x = C_LEN * 4 / 5
    legend_top = C_WID + 225
    swatches = [
        (C_WK,      WK_ALPHA, "xx",  "o", "Walkway (grated deck)"),
        ("#E8F0FF",  0.3,      None,  "o", "Processing tray"),
        (C_BRKT,     1.0,      None,  "r", f"Wall bracket ({WALKWAY_BRACKET_T}mm gusset)"),
        (C_SUPPORT,  0.8,      None,  "r", f"Support cradle / bearing strip (removable)"),
    ]
    for i, (c, a, h, marker, lbl) in enumerate(swatches):
        sy_pos = legend_top - i * 50
        if h:
            ax.add_patch(Rectangle((legend_x, sy_pos - 10), 30, 20,
                                    fc=c, ec=C_OUT, lw=0.6, alpha=a,
                                    hatch=h, zorder=15))
        elif marker == "r":
            ax.add_patch(Rectangle((legend_x, sy_pos - 10), 30, 20,
                                    fc=c, ec=C_OUT, lw=0.6, alpha=a, zorder=15))
        else:
            ax.add_patch(Rectangle((legend_x, sy_pos - 10), 30, 20,
                                    fc=c, ec=C_DIM, lw=0.6, alpha=a,
                                    ls="--", zorder=15))
        ax.text(legend_x + 40, sy_pos, lbl,
                ha="left", va="center", fontsize=5.5, color=C_DIM,
                **FONT, zorder=15)

    # ── Notes ────────────────────────────────────────────────────────────────
    n_brackets_near = len(np.arange(LXR + WALKWAY_BRACKET_SPACING / 2,
                                     TR, WALKWAY_BRACKET_SPACING))
    n_brackets_right = len(np.arange(
        WALKWAY_BRACKET_SPACING / 2, C_WID, WALKWAY_BRACKET_SPACING))
    n_brackets_total = n_brackets_near * 2 + n_brackets_right  # no left brackets
    notes = [
        f"1. 4 removable grated sections. Right corners: 45\u00b0 miter. Left corners: butt joint.",
        f"2. Near/far: wall-cantilevered brackets ({WALKWAY_BRACKET_T}mm gussets) bolted to corrugated wall ribs at {WALKWAY_BRACKET_SPACING}mm centers.",
        f"   Start at X={LXR} (butt joint) \u2014 entirely past panel transport envelope (X\u2264420).",
        f"3. Right: brackets on {WALKWAY_ANGLE_IRON}\u00d7{WALKWAY_ANGLE_IRON}\u00d7{WALKWAY_ANGLE_IRON_T}mm angle iron welded to flat end wall.",
        f"4. Left: REMOVABLE LIFT-OUT \u2014 bearer beam ({LEFT_WK_BEARER_SIZE}\u00d7{LEFT_WK_BEARER_SIZE}\u00d7{LEFT_WK_BEARER_T}mm Al RHS) at X={LXR}",
        f"   spans {WALKWAY_LEFT_SPAN}mm between bracket legs. {LEFT_WK_LEG_N} floor legs + bearing strip (cargo door side).",
        f"5. ZERO tray contact \u2014 all supports outside or above tray. Open area: {PROC_OPEN_AREA:.1f} m\u00b2.",
        f"6. ~{n_brackets_total} wall brackets (near + far + right). Each grating section lifts off for tray access.",
    ]
    for i, note in enumerate(notes):
        ax.text(C_LEN * 3 / 5 + PAD_X, -PAD_Y_BOT + 250 + (len(notes) - 1 - i) * 35, note,
                ha="left", va="bottom", fontsize=5.5, color=C_DIM,
                **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 7",
                drawing_title="PERIMETER WALKWAY",
                subtitle="PLAN VIEW \u2014 BRACKET LAYOUT + LEFT WALKWAY SUPPORT",
                scale_note=f"SCALE \u2248 1:25 \u00b7 ALL DIMS IN mm \u00b7 BRACKETS AT {WALKWAY_BRACKET_SPACING}mm CENTERS",
                height=0.06)

    fig.savefig("diagrams/walkway-sheet1.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet1.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet1.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — Detail: Near/Far Bracket on Corrugated Wall Rib
#
# Elevation cross-section looking along the walkway (X axis).
# Shows the bolt sandwich: reinforcing plate → wall steel → rib → bracket plate.
# The bolt is drawn as a horizontal bar passing through the layered materials.
# Scale ≈ 3:1 for clarity.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet3():
    S = 3.0

    def sx(mm): return mm * S
    def sy(mm): return mm * S

    # ── Structural dimensions ────────────────────────────────────────────────
    CORR_DEPTH = 38    # corrugation depth (mm)
    WALL_T     = 1.6   # wall steel thickness
    REINF_W    = 80    # reinforcing plate width behind wall
    REINF_H    = 180   # reinforcing plate height
    REINF_T    = 6     # reinforcing plate thickness
    BRKT_T     = WALKWAY_BRACKET_T  # 8mm
    BRKT_VERT  = WALKWAY_BRACKET_H  # 150mm
    BRKT_ARM_Z = WALKWAY_H - WALKWAY_GRATE_T  # = 75mm
    BOLT_D     = 12    # M12 bolt diameter
    BOLT_R     = BOLT_D / 2
    TRAY_WALL  = 3
    TRAY_FLOOR_T = 2
    TRAY_RIM_YD = PROC_TRAY_YD_NEAR  # = 80mm

    # Bolt assembly dimensions (in the through-thickness direction = Yd axis)
    WASHER_T   = 3     # flat washer thickness
    NUT_H      = 10    # M12 nut height
    BOLT_HEAD  = 8     # hex head height

    # ── Figure ───────────────────────────────────────────────────────────────
    YD_LO = -100
    YD_HI = WALKWAY_W + 100
    Z_LO  = -50
    Z_HI  = WALKWAY_H + WALKWAY_GRATE_T + 80

    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(sx(YD_LO), sx(YD_HI))
    ax.set_ylim(sy(Z_LO), sy(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container floor ──────────────────────────────────────────────────────
    ax.add_patch(Rectangle((sx(YD_LO), sy(-15)), sx(YD_HI - YD_LO), sy(15),
                            fc=C_FLOOR, ec=C_OUT, lw=1.0, hatch="///", zorder=2))

    # ── Corrugated wall (cross-section through rib — HOLLOW profile) ─────────
    # The corrugation is a trapezoidal fold in the sheet steel, NOT solid.
    # At a rib cross-section, we see:
    #   - Exterior panel (1.6mm steel, at Yd = -CORR_DEPTH - WALL_T)
    #   - Two rib side walls (1.6mm each, connecting exterior panel to rib face)
    #   - Rib interior face/flange (1.6mm, at Yd = 0)
    #   - Air gap between exterior panel and rib face
    # The bolt passes through: rib face → AIR GAP → exterior panel → reinf plate.
    RIB_FLANGE_W = 20  # rib face flange width (flat part, approx)

    ext_panel_yd = -CORR_DEPTH - WALL_T

    # Exterior wall steel panel (full height)
    ax.add_patch(Rectangle((sx(ext_panel_yd), sy(0)),
                            sx(WALL_T), sy(Z_HI),
                            fc="#909098", ec=C_OUT, lw=1.2, zorder=3,
                            hatch="///"))

    # Rib side walls (1.6mm steel, connecting exterior panel to rib face)
    # These are the sloped sides of the trapezoid — shown as vertical strips
    # at the edges of the rib (simplified; real profile is sloped)
    rib_side_yd_top = -WALL_T  # near the rib face
    rib_side_yd_bot = -CORR_DEPTH  # near the exterior panel
    # Left rib wall
    ax.add_patch(Rectangle((sx(-CORR_DEPTH), sy(0)),
                            sx(WALL_T), sy(Z_HI),
                            fc="#909098", ec=C_OUT, lw=0.8, zorder=3,
                            hatch="///"))

    # Rib interior face (flange — where bracket bolts on)
    ax.add_patch(Rectangle((sx(-WALL_T), sy(0)),
                            sx(WALL_T), sy(Z_HI),
                            fc="#909098", ec=C_OUT, lw=1.2, zorder=3,
                            hatch="///"))

    # Air gap inside the rib (light fill to show it's hollow)
    ax.add_patch(Rectangle((sx(-CORR_DEPTH + WALL_T), sy(0)),
                            sx(CORR_DEPTH - 2 * WALL_T), sy(Z_HI),
                            fc="#F0F0F0", ec="none", lw=0, zorder=2))
    # Dashed outline of air gap
    ax.add_patch(Rectangle((sx(-CORR_DEPTH + WALL_T), sy(0)),
                            sx(CORR_DEPTH - 2 * WALL_T), sy(Z_HI),
                            fc="none", ec=C_DIM, lw=0.5, ls="--", zorder=3))

    # Air gap label
    ax.text(sx(-CORR_DEPTH / 2), sy(Z_HI * 0.45),
            "AIR\nGAP",
            ha="center", va="center", fontsize=6, color=C_DIM,
            **FONT, zorder=15, style="italic")

    # Rib face (interior surface at Yd=0)
    ax.plot([sx(0), sx(0)], [sy(0), sy(Z_HI)],
            color=C_OUT, lw=2.0, zorder=4)

    ax.text(sx(-CORR_DEPTH / 2), sy(Z_HI - 8),
            "CORRUGATED\nWALL RIB\n(1.6mm CORTEN\nHOLLOW PROFILE)",
            ha="center", va="top", fontsize=5.5, color=C_DIM,
            fontweight="bold", **FONT, zorder=15)

    # ── Reinforcing plate (bonded to exterior wall face) ─────────────────────
    reinf_yd = ext_panel_yd - REINF_T
    ax.add_patch(Rectangle((sx(reinf_yd), sy(0)),
                            sx(REINF_T), sy(REINF_H),
                            fc="#C08040", ec=C_OUT, lw=1.0, zorder=4))
    leader(ax, sx(reinf_yd - 1), sy(REINF_H * 0.9),
           sx(reinf_yd - 20), sy(REINF_H * 0.9 + 30),
           f"REINFORCING\nPLATE\n{REINF_W}\u00d7{REINF_H}\n\u00d7{REINF_T}mm\n(EXTERIOR)",
           color="#C08040", fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Bracket mounting plate (flat against rib interior face) ──────────────
    ax.add_patch(Rectangle((sx(0), sy(0)),
                            sx(BRKT_T), sy(BRKT_VERT),
                            fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=6, alpha=0.85))

    # ── Through-bolts (cross-section: horizontal bars) ───────────────────────
    # The bolt passes horizontally through: reinf plate → wall → rib → bracket
    # Shown in cross-section as a horizontal rectangle (bolt shank)
    # with a hex head on the exterior and a nut on the interior.
    bolt_z1 = 30
    bolt_z2 = 120
    C_BOLT = "#505058"

    for bz in [bolt_z1, bolt_z2]:
        # Bolt shank — horizontal bar from reinf plate through to bracket face
        shank_left = reinf_yd
        shank_right = BRKT_T
        shank_hw = BOLT_R * 0.4  # half-width of shank in Z (cross-section)
        ax.add_patch(Rectangle((sx(shank_left), sy(bz - shank_hw)),
                                sx(shank_right - shank_left), sy(shank_hw * 2),
                                fc=C_BOLT, ec=C_OUT, lw=0.8, zorder=10))

        # Hex head on exterior side (left of reinforcing plate)
        head_left = reinf_yd - BOLT_HEAD
        ax.add_patch(Rectangle((sx(head_left), sy(bz - BOLT_R)),
                                sx(BOLT_HEAD), sy(BOLT_D),
                                fc=C_BOLT, ec=C_OUT, lw=1.0, zorder=10))
        # Washer under head
        ax.add_patch(Rectangle((sx(reinf_yd - WASHER_T), sy(bz - BOLT_R - 1)),
                                sx(WASHER_T), sy(BOLT_D + 2),
                                fc="#808080", ec=C_OUT, lw=0.5, zorder=9))

        # Nut on interior side (right of bracket plate)
        nut_left = BRKT_T
        ax.add_patch(Rectangle((sx(nut_left), sy(bz - BOLT_R)),
                                sx(NUT_H), sy(BOLT_D),
                                fc=C_BOLT, ec=C_OUT, lw=1.0, zorder=10))
        # Washer under nut
        ax.add_patch(Rectangle((sx(nut_left), sy(bz - BOLT_R - 1)),
                                sx(WASHER_T), sy(BOLT_D + 2),
                                fc="#808080", ec=C_OUT, lw=0.5, zorder=9))

    # Bolt label with layer callout
    leader(ax, sx(BRKT_T + NUT_H + 2), sy(bolt_z1),
           sx(BRKT_T + 15), sy(bolt_z1 - 20),
           f"M{BOLT_D} \u00d7 80mm THROUGH-BOLT\nHEAD (EXT) \u2192 REINF PLATE \u2192\nEXT PANEL \u2192 AIR GAP \u2192 RIB\nFACE \u2192 BRACKET \u2192 NUT (INT)\n2 PER BRACKET",
           color=C_DIM, fs=5.5,
           ha="left", va="center", arrow_style="-|>", font=FONT)

    # ── Horizontal arm ───────────────────────────────────────────────────────
    ARM_DEPTH = BRKT_T + 2
    arm_bot = BRKT_ARM_Z - ARM_DEPTH
    GUSSET_REACH = 70

    ax.add_patch(Rectangle((sx(0), sy(arm_bot)),
                            sx(WALKWAY_W), sy(ARM_DEPTH),
                            fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=6, alpha=0.85))
    ax.plot([sx(0), sx(WALKWAY_W)], [sy(BRKT_ARM_Z), sy(BRKT_ARM_Z)],
            color=C_OUT, lw=2.0, zorder=7)

    # ── Gusset underneath ────────────────────────────────────────────────────
    gusset_verts = [
        (sx(0), sy(0)),
        (sx(0), sy(arm_bot)),
        (sx(GUSSET_REACH), sy(arm_bot)),
    ]
    ax.add_patch(Polygon(gusset_verts, closed=True,
                         fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=5, alpha=0.85))
    ax.plot([sx(0), sx(GUSSET_REACH)], [sy(0), sy(arm_bot)],
            color=C_OUT, lw=1.5, zorder=6)

    # Weld symbols
    for wx_pos, wz_pos in [(GUSSET_REACH / 3, arm_bot), (BRKT_T / 2, BRKT_ARM_Z * 0.4)]:
        ax.plot([sx(wx_pos - 4), sx(wx_pos), sx(wx_pos + 4)],
                [sy(wz_pos), sy(wz_pos - 5), sy(wz_pos)],
                color="#CC4400", lw=1.5, zorder=8)

    # Bracket label
    leader(ax, sx(WALKWAY_W * 0.4), sy(BRKT_ARM_Z + 1),
           sx(WALKWAY_W * 0.55), sy(BRKT_VERT * 0.8),
           f"CANTILEVER BRACKET\n{BRKT_T}mm STEEL PLATE\n(NEAR/FAR WALKWAYS)",
           color=C_BRKT, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Processing tray ──────────────────────────────────────────────────────
    ax.add_patch(Rectangle((sx(TRAY_RIM_YD - TRAY_WALL), sy(0)),
                            sx(TRAY_WALL), sy(PROC_TRAY_RIM),
                            fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=4))
    tray_floor_end = YD_HI - 20
    ax.add_patch(Rectangle((sx(TRAY_RIM_YD), sy(0)),
                            sx(tray_floor_end - TRAY_RIM_YD), sy(TRAY_FLOOR_T),
                            fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))

    # ── Grated deck ──────────────────────────────────────────────────────────
    # Grating sits on bracket arm: bottom at BRKT_ARM_Z (75mm), top at WALKWAY_H (100mm)
    grate_bot = BRKT_ARM_Z  # = 75mm
    grate_top = grate_bot + WALKWAY_GRATE_T  # = 100mm
    ax.add_patch(Rectangle((sx(0), sy(grate_bot)),
                            sx(WALKWAY_W), sy(WALKWAY_GRATE_T),
                            fc=C_GRATE, ec=C_OUT, lw=1.2, zorder=7))
    bar_spacing = 34.2
    bar_w = 3
    for yd in np.arange(bar_w, WALKWAY_W - bar_w, bar_spacing):
        ax.add_patch(Rectangle((sx(yd), sy(grate_bot)),
                                sx(bar_w), sy(WALKWAY_GRATE_T),
                                fc="#909098", ec=C_OUT, lw=0.3, zorder=8))

    # ── Grating clip ─────────────────────────────────────────────────────────
    clip_yd = WALKWAY_W * 0.6
    clip_w = 8
    clip_below = 12   # extends below arm top
    clip_above = 5    # extends above grate top
    clip_bot = BRKT_ARM_Z - clip_below
    clip_top = grate_top + clip_above
    ax.add_patch(Rectangle((sx(clip_yd), sy(clip_bot)),
                            sx(clip_w), sy(clip_top - clip_bot),
                            fc="#505058", ec=C_OUT, lw=0.8, zorder=9))
    leader(ax, sx(clip_yd + clip_w), sy(BRKT_ARM_Z),
           sx(clip_yd + 50), sy(BRKT_ARM_Z + 35),
           "GRATING CLIP\n(REMOVABLE)", color="#505058", fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Dimension lines ──────────────────────────────────────────────────────
    draw_dim_v(ax, sx(reinf_yd - 15), sy(0), sy(BRKT_VERT),
               f"{BRKT_VERT}mm VERT", offset=sx(6), fs=6.5, right=True, font=FONT)
    draw_dim_h(ax, sx(0), sx(WALKWAY_W), sy(grate_top + 60),
               f"{WALKWAY_W}mm CANTILEVER ARM", offset=sy(6), fs=7, font=FONT)
    draw_dim_v(ax, sx(WALKWAY_W + 15), sy(0), sy(grate_top),
               f"{WALKWAY_H}mm\nDECK", offset=sx(6), fs=6.5, right=True, font=FONT)
    draw_dim_v(ax, sx(WALKWAY_W + 50), sy(grate_bot), sy(grate_top),
               f"{WALKWAY_GRATE_T}mm", offset=sx(6), fs=6, right=True, font=FONT)
    draw_dim_h(ax, sx(-CORR_DEPTH), sx(0), sy(-20),
               f"{CORR_DEPTH}mm CORR", offset=sy(10), fs=6, above=False, font=FONT)
    draw_dim_v(ax, sx(BRKT_T - 80), sy(bolt_z1), sy(bolt_z2),
               f"{bolt_z2 - bolt_z1}mm BOLT CENTERS", offset=sx(6), fs=6, right=True, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes_x = sx(WALKWAY_W + 50)
    notes_top = sy(Z_HI - 10)
    notes = [
        "NEAR/FAR WALKWAY \u2014 CORRUGATED WALL BRACKET:",
        "",
        f"1. Rib is HOLLOW — bolt bridges the air gap.",
        f"   Path: head \u2192 reinf plate \u2192 ext panel",
        f"   \u2192 air gap \u2192 rib face \u2192 bracket \u2192 nut.",
        f"2. Reinforcing plate ({REINF_W}\u00d7{REINF_H}\u00d7{REINF_T}mm)",
        f"   welded to exterior panel face. Provides",
        f"   bearing surface for bolt head + washer.",
        f"3. Bracket spacing: {WALKWAY_BRACKET_SPACING}mm",
        f"   (every structural wall rib).",
        f"4. Gusset ({GUSSET_REACH}mm reach) stops before",
        f"   tray rim at {TRAY_RIM_YD}mm.",
    ]
    for i, line in enumerate(notes):
        bold = i == 0
        ax.text(notes_x, notes_top - i * sy(6), line,
                ha="left", va="top", fontsize=5.5 if not bold else 6,
                color=C_OUT if bold else C_DIM,
                fontweight="bold" if bold else "normal",
                **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 3 OF 7",
                drawing_title="PERIMETER WALKWAY",
                subtitle="DETAIL A \u2014 NEAR/FAR BRACKET ON CORRUGATED WALL RIB",
                scale_note=f"SCALE \u2248 3:1 \u00b7 ALL DIMS IN mm \u00b7 ELEVATION THROUGH RIB",
                height=0.07)

    fig.savefig("diagrams/walkway-sheet3.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet3.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet3.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 4 — Detail: Right Walkway Bracket on Angle Iron (Flat End Wall)
#
# Elevation cross-section looking along the walkway (Yd axis).
# The far end wall is flat 1.6mm steel — no corrugation ribs.
# A 50×50×5mm angle iron is welded horizontally along the interior face
# to provide a structural mounting surface for the cantilever brackets.
# Scale ≈ 3:1 for clarity.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet4():
    S = 3.0

    def sx(mm): return mm * S
    def sy(mm): return mm * S

    WALL_T     = 1.6
    ANGLE_LEG  = WALKWAY_ANGLE_IRON    # 50mm
    ANGLE_T    = WALKWAY_ANGLE_IRON_T  # 5mm
    BRKT_T     = WALKWAY_BRACKET_T     # 8mm
    BRKT_VERT  = WALKWAY_BRACKET_H     # 150mm
    BRKT_ARM_Z = WALKWAY_H - WALKWAY_GRATE_T  # 75mm
    BOLT_D     = 12
    BOLT_R     = BOLT_D / 2
    TRAY_WALL  = 3
    TRAY_FLOOR_T = 2

    # ── Coordinate system (wall on RIGHT) ────────────────────────────────────────
    # Interior face of flat end wall at Yd = WALKWAY_W.
    # Bracket/arm/grating project LEFT (toward container interior).
    WALL_YD = WALKWAY_W  # 300 — interior face of end wall

    YD_LO = -100
    YD_HI = WALL_YD + WALL_T + 60
    Z_LO  = -50
    Z_HI  = WALKWAY_H + WALKWAY_GRATE_T + 80

    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(sx(YD_LO), sx(YD_HI))
    ax.set_ylim(sy(Z_LO), sy(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container floor ──────────────────────────────────────────────────────────
    ax.add_patch(Rectangle((sx(YD_LO), sy(-15)), sx(YD_HI - YD_LO), sy(15),
                            fc=C_FLOOR, ec=C_OUT, lw=1.0, hatch="///", zorder=2))

    # ── Flat end wall (RIGHT side) ───────────────────────────────────────────
    # Interior face at WALL_YD, exterior face at WALL_YD + WALL_T.
    ax.add_patch(Rectangle((sx(WALL_YD), sy(0)),
                            sx(WALL_T), sy(Z_HI),
                            fc=C_WALL, ec=C_OUT, lw=1.5, zorder=3))
    # Hatching beyond wall exterior
    ax.add_patch(Rectangle((sx(WALL_YD + WALL_T), sy(0)),
                            sx(15), sy(Z_HI),
                            fc="#E0DDD8", ec=C_OUT, lw=0.5, hatch="///", zorder=2))

    ax.text(sx(WALL_YD + WALL_T + 7), sy(Z_HI - 8),
            "FLAT END\nWALL\n(1.6mm CORTEN\nNO RIBS)",
            ha="center", va="top", fontsize=5.5, color=C_DIM,
            fontweight="bold", **FONT, zorder=15)

    # ── Angle iron (welded to interior face of end wall) ─────────────────────
    # L-angle: vertical leg against wall, horizontal leg on floor, both project LEFT.
    # Vertical leg: Yd = WALL_YD - ANGLE_T to WALL_YD, Z = 0 to ANGLE_LEG
    # Horizontal leg: Yd = WALL_YD - ANGLE_LEG to WALL_YD, Z = 0 to ANGLE_T
    C_ANGLE = "#B08040"

    # Vertical leg of angle iron (against wall)
    ax.add_patch(Rectangle((sx(WALL_YD - ANGLE_T), sy(0)),
                            sx(ANGLE_T), sy(ANGLE_LEG),
                            fc=C_ANGLE, ec=C_OUT, lw=1.2, zorder=5))
    # Horizontal leg of angle iron (on floor)
    ax.add_patch(Rectangle((sx(WALL_YD - ANGLE_LEG), sy(0)),
                            sx(ANGLE_LEG), sy(ANGLE_T),
                            fc=C_ANGLE, ec=C_OUT, lw=1.2, zorder=5))
    # Weld symbol at angle iron to wall junction
    ax.plot([sx(WALL_YD + 1), sx(WALL_YD - 2), sx(WALL_YD - 5)],
            [sy(ANGLE_LEG * 0.7), sy(ANGLE_LEG * 0.7 - 5), sy(ANGLE_LEG * 0.7)],
            color="#CC4400", lw=1.5, zorder=8)

    leader(ax, sx(WALL_YD - ANGLE_LEG / 2), sy(ANGLE_T + 3),
           sx(WALL_YD - ANGLE_LEG - 30), sy(ANGLE_T + 20),
           f"ANGLE IRON\n{ANGLE_LEG}\u00d7{ANGLE_LEG}\u00d7{ANGLE_T}mm\nL-ANGLE\n(WELDED TO\nEND WALL)",
           color=C_ANGLE, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Bracket (bolted to angle iron vertical leg) ──────────────────────────
    # Bracket mounting plate sits against the LEFT face of angle iron vertical leg.
    brkt_yd_r = WALL_YD - ANGLE_T       # right edge of bracket plate
    brkt_yd_l = brkt_yd_r - BRKT_T      # left edge of bracket plate
    ax.add_patch(Rectangle((sx(brkt_yd_l), sy(0)),
                            sx(BRKT_T), sy(BRKT_VERT),
                            fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=6, alpha=0.85))

    # Through-bolts: bracket plate + angle iron vertical leg
    bolt_z1 = 20
    bolt_z2 = 40    # both bolts within the 50mm angle leg height
    C_BOLT = "#505058"
    NUT_H  = 10
    BOLT_HEAD = 8

    REINF_T = 6  # reinforcing plate behind wall exterior

    for bz in [bolt_z1, bolt_z2]:
        shank_hw = BOLT_R * 0.4
        # Shank through: reinf plate + wall + angle iron vert leg + bracket plate
        ax.add_patch(Rectangle((sx(brkt_yd_l), sy(bz - shank_hw)),
                                sx(BRKT_T + ANGLE_T + WALL_T + REINF_T), sy(shank_hw * 2),
                                fc=C_BOLT, ec=C_OUT, lw=0.8, zorder=10))
        # Head on interior side (left of bracket)
        ax.add_patch(Rectangle((sx(brkt_yd_l - BOLT_HEAD), sy(bz - BOLT_R)),
                                sx(BOLT_HEAD), sy(BOLT_D),
                                fc=C_BOLT, ec=C_OUT, lw=1.0, zorder=10))
        # Nut on exterior side (right of wall + reinforcing plate)
        ax.add_patch(Rectangle((sx(WALL_YD + WALL_T), sy(bz - BOLT_R)),
                                sx(NUT_H), sy(BOLT_D),
                                fc=C_BOLT, ec=C_OUT, lw=1.0, zorder=10))
        # Reinforcing plate (small rectangle on wall exterior)
        ax.add_patch(Rectangle((sx(WALL_YD + WALL_T), sy(bz - BOLT_R - 4)),
                                sx(REINF_T), sy(BOLT_D + 8),
                                fc="#A0A0A8", ec=C_OUT, lw=0.6, zorder=9))

    leader(ax, sx(brkt_yd_l - BOLT_HEAD - 2), sy(bolt_z1),
           sx(brkt_yd_l - BOLT_HEAD - 60), sy(bolt_z1 - 18),
           f"M{BOLT_D} THROUGH-BOLT\nBRACKET + ANGLE IRON\n+ WALL + REINF PLATE\n(2 PER BRACKET)",
           color=C_DIM, fs=5.5,
           ha="right", va="center", arrow_style="-|>", font=FONT)

    # ── Horizontal arm (projects LEFT from bracket) ──────────────────────────
    ARM_DEPTH = BRKT_T + 2
    arm_bot = BRKT_ARM_Z - ARM_DEPTH
    GUSSET_REACH = 70
    arm_left = brkt_yd_r - WALKWAY_W  # arm extends WALKWAY_W left from bracket

    ax.add_patch(Rectangle((sx(arm_left), sy(arm_bot)),
                            sx(WALKWAY_W), sy(ARM_DEPTH),
                            fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=6, alpha=0.85))
    ax.plot([sx(arm_left), sx(arm_left + WALKWAY_W)],
            [sy(BRKT_ARM_Z), sy(BRKT_ARM_Z)],
            color=C_OUT, lw=2.0, zorder=7)

    # ── Gusset underneath ──────────────────────────────────────────────────────
    gusset_verts = [
        (sx(brkt_yd_r), sy(ANGLE_T)),               # top of angle horiz leg
        (sx(brkt_yd_r), sy(arm_bot)),                # arm bottom at bracket
        (sx(brkt_yd_r - GUSSET_REACH), sy(arm_bot)), # 70mm out to left
    ]
    ax.add_patch(Polygon(gusset_verts, closed=True,
                         fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=5, alpha=0.85))
    ax.plot([sx(brkt_yd_r), sx(brkt_yd_r - GUSSET_REACH)],
            [sy(ANGLE_T), sy(arm_bot)],
            color=C_OUT, lw=1.5, zorder=6)

    # Bracket label
    leader(ax, sx(arm_left + WALKWAY_W * 0.4), sy(BRKT_ARM_Z + 3),
           sx(arm_left + WALKWAY_W * 0.3), sy(BRKT_VERT + 15),
           f"CANTILEVER BRACKET\n{BRKT_T}mm STEEL PLATE\n(RIGHT WALKWAY)",
           color=C_BRKT, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Processing tray (for reference) ──────────────────────────────────────────
    tray_rim_yd = arm_left + WALKWAY_W - PROC_TRAY_YD_NEAR
    ax.add_patch(Rectangle((sx(tray_rim_yd), sy(0)),
                            sx(TRAY_WALL), sy(PROC_TRAY_RIM),
                            fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=4))
    tray_floor_start = YD_LO + 20
    ax.add_patch(Rectangle((sx(tray_floor_start), sy(0)),
                            sx(tray_rim_yd - tray_floor_start), sy(TRAY_FLOOR_T),
                            fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))

    # ── Grated deck ──────────────────────────────────────────────────────────
    # Grating sits on bracket arm: bottom at BRKT_ARM_Z (75mm), top at WALKWAY_H (100mm)
    grate_bot = BRKT_ARM_Z  # = 75mm
    grate_top = grate_bot + WALKWAY_GRATE_T  # = 100mm
    ax.add_patch(Rectangle((sx(arm_left), sy(grate_bot)),
                            sx(WALKWAY_W), sy(WALKWAY_GRATE_T),
                            fc=C_GRATE, ec=C_OUT, lw=1.2, zorder=7))
    bar_spacing = 34.2
    bar_w = 3
    for yd in np.arange(bar_w, WALKWAY_W - bar_w, bar_spacing):
        ax.add_patch(Rectangle((sx(arm_left + yd), sy(grate_bot)),
                                sx(bar_w), sy(WALKWAY_GRATE_T),
                                fc="#909098", ec=C_OUT, lw=0.3, zorder=8))

    # ── Grating clip ─────────────────────────────────────────────────────────
    clip_yd = arm_left + WALKWAY_W * 0.4
    clip_w = 8
    clip_below = 12   # extends below arm top
    clip_above = 5    # extends above grate top
    clip_bot = BRKT_ARM_Z - clip_below
    clip_top = grate_top + clip_above
    ax.add_patch(Rectangle((sx(clip_yd), sy(clip_bot)),
                            sx(clip_w), sy(clip_top - clip_bot),
                            fc="#505058", ec=C_OUT, lw=0.8, zorder=9))
    leader(ax, sx(clip_yd + clip_w), sy(BRKT_ARM_Z),
           sx(clip_yd - 40), sy(BRKT_ARM_Z + 35),
           "GRATING CLIP\n(REMOVABLE)", color="#505058", fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Dimension lines ──────────────────────────────────────────────────────
    draw_dim_v(ax, sx(WALL_YD + WALL_T + 20), sy(0), sy(BRKT_VERT),
               f"{BRKT_VERT}mm\nVERT", offset=sx(6), fs=6.5, right=True, font=FONT)
    draw_dim_h(ax, sx(arm_left), sx(arm_left + WALKWAY_W), sy(grate_top + 20),
               f"{WALKWAY_W}mm CANTILEVER ARM", offset=sy(6), fs=7, font=FONT)
    draw_dim_v(ax, sx(arm_left - 15), sy(0), sy(grate_top),
               f"{WALKWAY_H}mm\nDECK", offset=sx(6), fs=6.5, right=False, font=FONT)
    draw_dim_v(ax, sx(WALL_YD), sy(0), sy(ANGLE_LEG),
               f"{ANGLE_LEG}mm", offset=sx(15), fs=6, right=True, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes_x = sx(YD_LO + 10)
    notes_top = sy(Z_HI - 10)
    notes = [
        "RIGHT WALKWAY \u2014 FLAT END WALL:",
        "",
        f"1. Far end wall is flat 1.6mm steel \u2014 no",
        f"   corrugation ribs for direct bracket mounting.",
        f"2. {ANGLE_LEG}\u00d7{ANGLE_LEG}\u00d7{ANGLE_T}mm L-angle welded",
        f"   horizontally along wall interior provides",
        f"   structural mounting surface.",
        f"3. M12 through-bolts penetrate bracket + angle",
        f"   iron + wall + reinforcing plate (exterior).",
        f"4. Bracket spacing: {WALKWAY_BRACKET_SPACING}mm along Yd.",
        f"5. Angle iron continuous weld to wall steel",
        f"   distributes load across flat panel.",
    ]
    for i, line in enumerate(notes):
        bold = i == 0
        ax.text(notes_x, notes_top - i * sy(6), line,
                ha="left", va="top", fontsize=5.5 if not bold else 6,
                color=C_OUT if bold else C_DIM,
                fontweight="bold" if bold else "normal",
                **FONT, zorder=15)

    # ── Title block ─────────────────────────────────────────────────────────
    title_block(ax, "SHEET 4 OF 7",
                drawing_title="PERIMETER WALKWAY",
                subtitle="DETAIL B \u2014 RIGHT WALKWAY BRACKET ON ANGLE IRON (FLAT END WALL)",
                scale_note=f"SCALE \u2248 3:1 \u00b7 ALL DIMS IN mm",
                height=0.07)

    fig.savefig("diagrams/walkway-sheet4.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet4.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet4.png saved")

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 5 — Detail: Left Walkway Lift-Out at Butt Joint
#
# Elevation showing the left walkway grating sitting on the near/far walkway
# bracket arms at the butt joint (X=470).  Left corners are NOT mitered —
# butt joints keep the near/far walkways entirely past the panel transport
# envelope (X≤420), so only the left walkway needs to be removed for transport.
# No brackets on the left walkway itself — it's a removable lift-out section.
# Scale ≈ 2:1 for clarity.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet5():
    S = 2.5   # scale factor

    def sx(mm): return mm * S
    def sy(mm): return mm * S

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
    z_lo, z_hi = 0, TRAY_FLOOR_T * S
    zz = np.linspace(z_lo, z_hi, 5)
    ax.plot([bx - 3, bx + 3, bx - 3, bx + 3, bx - 3],
            zz, color=C_OUT, lw=1.0, zorder=5)
    # Tray rim label
    leader(ax, sx(tray_x - 5), sy(PROC_TRAY_RIM / 2 + 10),
           sx(tray_x - 30), sy(PROC_TRAY_RIM + 15),
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
    # Foot plate
    ax.add_patch(Rectangle((sx(OUTER_LEG_X - base / 2), sy(-3)),
                            sx(base), sy(3),
                            fc=C_SUPPORT, ec=C_OUT, lw=0.6, alpha=0.5, zorder=4))
    # Cantilever arm from leg to walkway edge
    ax.add_patch(Rectangle((sx(OUTER_LEG_X - LEG_W / 2), sy(LEG_TOP - 5)),
                            sx(tray_x + 20 - OUTER_LEG_X + LEG_W / 2), sy(5),
                            fc=C_SUPPORT, ec=C_OUT, lw=0.6, alpha=0.5, zorder=5))
    # Leg label
    leader(ax, sx(OUTER_LEG_X - LEG_W), sy(LEG_TOP / 2),
           sx(OUTER_LEG_X - 45), sy(LEG_TOP / 2 - 15),
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
           sx(LEFT_WK_R + BEAM_SZ / 2 + 40), sy(beam_bot - 5),
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

    leader(ax, sx(LEFT_WK_R), sy(arm_bot - 2),
           sx(LEFT_WK_R), sy(arm_bot - 22),
           f"NEAR WALKWAY\nBRACKET ARM\n(CROSS-SECTION)\nAT X={LEFT_WK_R}mm",
           color=C_BRKT, fs=5.5,
           ha="center", va="top", arrow_style="-|>", font=FONT)

    # ── Contact point: left grating rests on bracket arm ─────────────────────
    ax.plot([sx(LEFT_WK_R - 15), sx(LEFT_WK_R + 15)],
            [sy(BRKT_ARM_Z), sy(BRKT_ARM_Z)],
            color="#CC4400", lw=3.0, zorder=10)
    leader(ax, sx(LEFT_WK_R - 10), sy(BRKT_ARM_Z),
           sx(LEFT_WK_R - 60), sy(BRKT_ARM_Z - 18),
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

    # ── Grating clip on near walkway ─────────────────────────────────────────
    clip_x = near_wk_start + 80
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
    draw_dim_v(ax, sx(dim_x), sy(0), sy(grate_top),
               f"{int(grate_top)}mm\nDECK", offset=sx(6), fs=6, right=True, font=FONT)
    # Arm height
    draw_dim_v(ax, sx(dim_x), sy(0), sy(BRKT_ARM_Z),
               f"{BRKT_ARM_Z}mm\nARM", offset=sx(30), fs=6, right=True, font=FONT)
    # Tray rim
    draw_dim_v(ax, sx(tray_x + 20), sy(0), sy(PROC_TRAY_RIM),
               f"{PROC_TRAY_RIM}mm", offset=sx(6), fs=6, right=True,
               color=C_TRAY, font=FONT)
    # Panel bottom
    draw_dim_v(ax, sx(LEFT_WK_L - 20), sy(0), sy(PANEL_FLOOR_GAP),
               f"{PANEL_FLOOR_GAP}mm\nPANEL\nBOTTOM", offset=sx(6), fs=5.5, right=False,
               color="#CC4422", font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes_x = sx(near_wk_end + 80)
    notes_top = sy(Z_HI - 5)
    leg_spacing = int(WALKWAY_LEFT_SPAN / (LEFT_WK_LEG_N + 1))
    notes = [
        "LEFT WALKWAY \u2014 REMOVABLE LIFT-OUT:",
        "",
        f"1. NO wall brackets \u2014 panel occupies end wall.",
        f"2. Processing tray side (X={LEFT_WK_R}):",
        f"   bearer beam {LEFT_WK_BEARER_SIZE}\u00d7{LEFT_WK_BEARER_SIZE}\u00d7{LEFT_WK_BEARER_T}mm",
        f"   Al RHS spans {WALKWAY_LEFT_SPAN}mm (sheet 6).",
        f"3. Cargo door side (X={LEFT_WK_L}): bearing",
        f"   strip + {LEFT_WK_LEG_N} floor legs at {leg_spacing}mm ctrs.",
        f"4. ZERO tray contact \u2014 all supports",
        f"   outside or above processing tray.",
        f"5. {CLEARANCE}mm clearance: panel (X={PANEL_INNER}) to",
        f"   near walkway bracket (X={LEFT_WK_R}).",
        f"6. Remove cradles + grating before panel slides.",
    ]
    for i, line in enumerate(notes):
        bold = i == 0
        ax.text(notes_x, notes_top - i * sy(6), line,
                ha="left", va="top", fontsize=5.5 if not bold else 6,
                color=C_OUT if bold else C_DIM,
                fontweight="bold" if bold else "normal",
                **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 5 OF 7",
                drawing_title="PERIMETER WALKWAY",
                subtitle="DETAIL C \u2014 LEFT WALKWAY BUTT JOINT AND PANEL CLEARANCE",
                scale_note=f"SCALE \u2248 2.5:1 \u00b7 ALL DIMS IN mm \u00b7 VIEW ALONG Yd (NEAR \u2192 FAR)",
                height=0.07)

    fig.savefig("diagrams/walkway-sheet5.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet5.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet5.png saved")

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 6 — Detail D: Left Walkway Support System
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
def sheet6():
    S = 3.5   # scale factor

    def sx(mm): return mm * S
    def sy(mm): return mm * S

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

    # Floor leg geometry (cargo door side)
    OUTER_LEG_X = tray_x - 30      # = 140mm (on bare floor, outside tray)
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
    z_lo, z_hi = 0, TRAY_FLOOR_T * S
    zz = np.linspace(z_lo, z_hi, 5)
    ax.plot([bx - 3, bx + 3, bx - 3, bx + 3, bx - 3],
            zz, color=C_OUT, lw=1.0, zorder=5)
    # Label tray rim
    leader(ax, sx(tray_x - TRAY_WALL / 2), sy(PROC_TRAY_RIM / 2),
           sx(tray_x - 25), sy(PROC_TRAY_RIM + 20),
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
    leader(ax, sx(tray_x + STRIP_H / 2), sy(strip_bot + STRIP_H / 2),
           sx(tray_x + STRIP_H / 2 - 40), sy(strip_bot + STRIP_H + 18),
           f"BEARING STRIP\n25\u00d725\u00d73mm Al ANGLE\nON TRAY RIM\n(REMOVABLE)",
           color=C_SUPPORT, fs=6,
           ha="center", va="bottom", arrow_style="-|>", font=FONT)

    # ── Floor-standing support leg (cargo door side) ─────────────────────────
    # Vertical post
    ax.add_patch(Rectangle((sx(OUTER_LEG_X - LEG_W / 2), sy(BASE_T)),
                            sx(LEG_W), sy(LEG_TOP - ARM_T - BASE_T),
                            fc=C_SUPPORT, ec=C_OUT, lw=1.2, zorder=6))
    # Hollow tube detail
    ax.add_patch(Rectangle((sx(OUTER_LEG_X - LEG_W / 2 + LEG_T), sy(BASE_T + LEG_T)),
                            sx(LEG_W - 2 * LEG_T),
                            sy(LEG_TOP - ARM_T - BASE_T - 2 * LEG_T),
                            fc="#F0E0C8", ec=C_OUT, lw=0.4, zorder=7))
    # Foot plate
    ax.add_patch(Rectangle((sx(OUTER_LEG_X - BASE_W / 2), sy(0)),
                            sx(BASE_W), sy(BASE_T),
                            fc=C_SUPPORT, ec=C_OUT, lw=1.0, zorder=6))
    # Rubber pad
    ax.add_patch(Rectangle((sx(OUTER_LEG_X - BASE_W / 2), sy(-2)),
                            sx(BASE_W), sy(2),
                            fc="#333333", ec=C_OUT, lw=0.6, zorder=6))
    # Cantilever arm (from leg top to past tray rim)
    ax.add_patch(Rectangle((sx(OUTER_LEG_X - LEG_W / 2), sy(LEG_TOP - ARM_T)),
                            sx(ARM_END - OUTER_LEG_X + LEG_W / 2), sy(ARM_T),
                            fc=C_SUPPORT, ec=C_OUT, lw=1.0, zorder=8))

    # Leg label
    leader(ax, sx(OUTER_LEG_X), sy(LEG_TOP / 2 - 5),
           sx(OUTER_LEG_X - 40), sy(LEG_TOP / 2 - 20),
           f"FLOOR LEG\n{LEG_W}\u00d7{LEG_W}\u00d7{LEG_T}mm Al SHS\n"
           f"(\u00d7{LEFT_WK_LEG_N}, ON BARE FLOOR)\n"
           f"WITH CANTILEVER ARM",
           color=C_SUPPORT, fs=5.5,
           ha="center", va="top", arrow_style="-|>", font=FONT)
    ax.text(sx(OUTER_LEG_X), sy(-5),
            "RUBBER PAD", ha="center", va="top", fontsize=4.5,
            color="#333333", **FONT, zorder=15)

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
           sx(LEFT_WK_R + BEAM_SZ / 2 + 45), sy(beam_bot + BEAM_SZ / 2 - 15),
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
    draw_dim_h(ax, sx(LEFT_WK_L), sx(LEFT_WK_R), sy(grate_top + 30),
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
    draw_dim_v(ax, sx(dim_x_r), sy(0), sy(grate_top),
               f"{int(grate_top)}mm\nDECK", offset=sx(6), fs=6, right=True, font=FONT)
    draw_dim_v(ax, sx(dim_x_r), sy(0), sy(beam_top),
               f"{beam_top}mm\nBEAM\nTOP", offset=sx(30), fs=5.5, right=True, font=FONT)
    draw_dim_v(ax, sx(dim_x_r), sy(0), sy(beam_bot),
               f"{beam_bot}mm\nBEAM\nBOT", offset=sx(55), fs=5.5, right=True, font=FONT)

    # Tray rim height (left side)
    draw_dim_v(ax, sx(tray_x + STRIP_H + 8), sy(0), sy(PROC_TRAY_RIM),
               f"{PROC_TRAY_RIM}mm\nRIM",
               offset=sx(6), fs=5.5, right=True, color=C_TRAY, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    leg_spacing = int(WALKWAY_LEFT_SPAN / (LEFT_WK_LEG_N + 1))
    notes_x = sx(X_HI - 5)
    notes_top = sy(Z_HI - 3)
    notes = [
        "LEFT WALKWAY SUPPORT SYSTEM:",
        "",
        f"1. BEARER BEAM ({BEAM_SZ}\u00d7{BEAM_SZ}\u00d7{BEAM_T}mm",
        f"   Al RHS) at X={LEFT_WK_R}mm spans",
        f"   {WALKWAY_LEFT_SPAN}mm along Yd. Bolted to",
        f"   near/far bracket vertical legs.",
        f"2. {LEFT_WK_LEG_N} FLOOR LEGS at X={OUTER_LEG_X}mm",
        f"   ({leg_spacing}mm centers) on bare floor",
        f"   outside processing tray.",
        f"3. BEARING STRIP (25\u00d725\u00d73mm Al angle)",
        f"   on tray rim at X={LEFT_WK_L}mm.",
        f"4. ZERO tray contact \u2014 all supports",
        f"   outside or above processing tray.",
        f"5. All supports removable \u2014 lift out",
        f"   with grating before panel transport.",
    ]
    for i, line in enumerate(notes):
        bold = i == 0
        ax.text(notes_x, notes_top - i * sy(5), line,
                ha="right", va="top", fontsize=5.5 if not bold else 6,
                color=C_OUT if bold else C_DIM,
                fontweight="bold" if bold else "normal",
                **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 6 OF 7",
                drawing_title="PERIMETER WALKWAY",
                subtitle="DETAIL D \u2014 LEFT WALKWAY SUPPORT SYSTEM (REMOVABLE)",
                scale_note=f"SCALE \u2248 3.5:1 \u00b7 ALL DIMS IN mm \u00b7 VIEW ALONG Yd (NEAR \u2192 FAR)",
                height=0.07)

    fig.savefig("diagrams/walkway-sheet6.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet6.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet6.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 7 — Detail E: Bearer Beam to Bracket Connection
#
# Elevation showing how the bearer beam (50×50×3mm Al RHS) bolts to the
# near walkway bracket vertical leg at the butt joint.  View looking along
# X axis (same direction as sheet 1).
# Horizontal = Yd (0 = pinhole wall, positive toward far wall)
# Vertical   = Z  (0 = floor, positive up)
# Shows: bracket vertical leg + gusset on wall, beam end plate bolted to
# the bracket vertical leg, beam running along Yd.  Removable connection
# using wing bolts for tool-free disassembly.
# Scale ≈ 4:1 for clarity.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet7():
    S = 4.0   # scale factor

    def sx(mm): return mm * S
    def sy(mm): return mm * S

    # ── Structural dimensions ────────────────────────────────────────────────
    CORR_DEPTH = 38    # corrugation depth (mm)
    WALL_T     = 1.6   # wall steel thickness
    BRKT_T     = WALKWAY_BRACKET_T   # 8mm plate thickness
    BRKT_VERT  = WALKWAY_BRACKET_H   # 150mm vertical leg
    BRKT_ARM_Z = WALKWAY_H - WALKWAY_GRATE_T  # 75mm (arm top)
    ARM_DEPTH  = BRKT_T + 2          # arm visual thickness
    arm_bot    = BRKT_ARM_Z - ARM_DEPTH
    GUSSET_REACH = 70

    # Bearer beam
    BEAM_SZ = LEFT_WK_BEARER_SIZE   # 50mm
    BEAM_T  = LEFT_WK_BEARER_T      # 3mm
    beam_bot = BRKT_ARM_Z - BEAM_SZ  # Z = 25mm
    beam_top = BRKT_ARM_Z            # Z = 75mm

    # End plate
    EP_W = 60    # end plate width (visible face, in Z direction)
    EP_T = 5     # end plate thickness (in Yd direction)
    ep_bot = beam_bot - 5   # end plate extends 5mm below beam
    ep_top = beam_top + 5   # end plate extends 5mm above beam

    # Bolts (M10 wing bolts for tool-free removal)
    BOLT_D = 10
    BOLT_R = BOLT_D / 2
    bolt_z1 = beam_bot + 12   # = 37mm
    bolt_z2 = beam_top - 12   # = 63mm

    # Grating
    grate_bot = BRKT_ARM_Z
    grate_top = grate_bot + WALKWAY_GRATE_T

    # Show beam extending 250mm into view (along Yd)
    BEAM_SHOW = 250

    # ── Figure ───────────────────────────────────────────────────────────────
    YD_LO = -60
    YD_HI = BEAM_SHOW + 80
    Z_LO  = -30
    Z_HI  = BRKT_VERT + 30

    fig, ax = plt.subplots(figsize=(18, 12))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(sx(YD_LO), sx(YD_HI))
    ax.set_ylim(sy(Z_LO), sy(Z_HI))
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container floor ──────────────────────────────────────────────────────
    ax.add_patch(Rectangle((sx(YD_LO), sy(-12)), sx(YD_HI - YD_LO), sy(12),
                            fc=C_FLOOR, ec=C_OUT, lw=1.0, hatch="///", zorder=2))

    # ── Container wall (corrugated, at Yd=0) ─────────────────────────────────
    wall_z_top = Z_HI
    ax.add_patch(Rectangle((sx(-CORR_DEPTH - 5), sy(0)),
                            sx(CORR_DEPTH + 5), sy(wall_z_top),
                            fc=C_WALL, ec=C_OUT, lw=1.2, hatch="///", zorder=3))
    # Corrugation rib at section cut
    rib_w = 12
    ax.add_patch(Rectangle((sx(-rib_w / 2), sy(0)),
                            sx(rib_w), sy(wall_z_top),
                            fc="#A8A8B0", ec=C_OUT, lw=1.0, zorder=3))
    ax.text(sx(-CORR_DEPTH / 2 - 5), sy(wall_z_top - 10),
            "CONTAINER\nWALL",
            ha="center", va="top", fontsize=6, color=C_DIM,
            fontweight="bold", **FONT, zorder=15)

    # ── Bracket vertical leg ─────────────────────────────────────────────────
    ax.add_patch(Rectangle((sx(-BRKT_T / 2), sy(0)),
                            sx(BRKT_T), sy(BRKT_VERT),
                            fc=C_BRKT, ec=C_OUT, lw=1.5, zorder=6))
    # Label vertical leg
    leader(ax, sx(BRKT_T / 2 + 2), sy(BRKT_VERT - 10),
           sx(BRKT_T / 2 + 50), sy(BRKT_VERT + 10),
           f"BRACKET VERTICAL LEG\n{BRKT_T}mm PLATE \u00d7 {BRKT_VERT}mm\n(BOLTED TO WALL RIB)",
           color=C_BRKT, fs=5.5,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # ── Bracket arm (projects inward, ghost — continues out of view) ─────────
    # Show just the start of the arm near the wall
    arm_show = 120
    ax.add_patch(Rectangle((sx(0), sy(arm_bot)),
                            sx(arm_show), sy(ARM_DEPTH),
                            fc=C_BRKT, ec=C_OUT, lw=1.0, alpha=0.4,
                            ls="--", zorder=5))
    # Arm top line
    ax.plot([sx(0), sx(arm_show)], [sy(BRKT_ARM_Z), sy(BRKT_ARM_Z)],
            color=C_OUT, lw=1.5, alpha=0.5, ls="--", zorder=6)
    # Sawtooth break line on bracket arm
    bx_arm = sx(arm_show)
    z_lo_arm, z_hi_arm = sy(arm_bot - 1), sy(BRKT_ARM_Z + 1)
    zz_arm = np.linspace(z_lo_arm, z_hi_arm, 7)
    ax.plot([bx_arm - 3, bx_arm + 3, bx_arm - 3, bx_arm + 3,
             bx_arm - 3, bx_arm + 3, bx_arm - 3],
            zz_arm, color=C_OUT, lw=1.0, zorder=7)
    ax.text(sx(arm_show / 2), sy(BRKT_ARM_Z + 4),
            f"BRACKET ARM\n(CONTINUES {WALKWAY_W}mm\nALONG Yd \u2014 GHOST)",
            ha="center", va="bottom", fontsize=5, color=C_BRKT,
            alpha=0.6, **FONT, zorder=15)

    # ── Gusset triangle ──────────────────────────────────────────────────────
    gusset_verts = [
        (sx(0), sy(0)),
        (sx(0), sy(arm_bot)),
        (sx(GUSSET_REACH), sy(arm_bot)),
    ]
    ax.add_patch(Polygon(gusset_verts, closed=True,
                         fc=C_BRKT, ec=C_OUT, lw=1.2, zorder=5, alpha=0.85))
    ax.plot([sx(0), sx(GUSSET_REACH)], [sy(0), sy(arm_bot)],
            color=C_OUT, lw=1.5, zorder=6)

    # Bracket bolt holes (2× M12, through wall rib)
    brkt_bolt_z1 = 30
    brkt_bolt_z2 = 120
    for bz in [brkt_bolt_z1, brkt_bolt_z2]:
        ax.add_patch(Circle((sx(0), sy(bz)), sx(6),
                     fc=BG, ec=C_OUT, lw=1.0, zorder=8))
        ax.plot([sx(-3), sx(3)], [sy(bz), sy(bz)], color=C_OUT, lw=0.5, zorder=9)
        ax.plot([sx(0), sx(0)], [sy(bz - 3), sy(bz + 3)], color=C_OUT, lw=0.5, zorder=9)

    # ── End plate (welded to beam end) ───────────────────────────────────────
    C_SUPPORT = "#D08020"
    ep_yd = BRKT_T / 2   # end plate sits against bracket outer face
    ax.add_patch(Rectangle((sx(ep_yd), sy(ep_bot)),
                            sx(EP_T), sy(ep_top - ep_bot),
                            fc=C_SUPPORT, ec=C_OUT, lw=1.5, zorder=7))
    leader(ax, sx(ep_yd + EP_T / 2), sy(ep_top + 2),
           sx(ep_yd + EP_T / 2 + 50), sy(ep_top + 20),
           f"END PLATE\n{EP_W}\u00d7{BEAM_SZ}\u00d7{EP_T}mm\n(WELDED TO BEAM)",
           color=C_SUPPORT, fs=5.5,
           ha="left", va="bottom", arrow_style="-|>", font=FONT)

    # ── Bearer beam (50×50×3mm Al RHS, running along Yd) ─────────────────────
    beam_yd_start = ep_yd + EP_T  # beam starts after end plate
    ax.add_patch(Rectangle((sx(beam_yd_start), sy(beam_bot)),
                            sx(BEAM_SHOW - beam_yd_start), sy(BEAM_SZ),
                            fc=C_SUPPORT, ec=C_OUT, lw=1.5, zorder=7))
    # Hollow interior
    ax.add_patch(Rectangle((sx(beam_yd_start + BEAM_T), sy(beam_bot + BEAM_T)),
                            sx(BEAM_SHOW - beam_yd_start - 2 * BEAM_T),
                            sy(BEAM_SZ - 2 * BEAM_T),
                            fc="#F0E0C8", ec=C_OUT, lw=0.5, zorder=8))
    # Sawtooth break line at far end (beam continues)
    bx_beam = sx(BEAM_SHOW)
    z_lo_beam, z_hi_beam = sy(beam_bot + 2), sy(beam_top - 2)
    zz_beam = np.linspace(z_lo_beam, z_hi_beam, 7)
    ax.plot([bx_beam - 3, bx_beam + 3, bx_beam - 3, bx_beam + 3,
             bx_beam - 3, bx_beam + 3, bx_beam - 3],
            zz_beam, color=C_OUT, lw=1.0, zorder=9)
    # Beam label
    ax.text(sx((beam_yd_start + BEAM_SHOW) / 2), sy(beam_bot - 3),
            f"BEARER BEAM\n{BEAM_SZ}\u00d7{BEAM_SZ}\u00d7{BEAM_T}mm Al RHS\n"
            f"(SPANS {WALKWAY_LEFT_SPAN}mm TO FAR BRACKET)",
            ha="center", va="top", fontsize=6, color=C_SUPPORT,
            fontweight="bold", **FONT, zorder=15)

    # ── Wing bolts (M10, 2×) through end plate + bracket vertical leg ────────
    C_BOLT = "#404050"
    for bz in [bolt_z1, bolt_z2]:
        # Bolt shaft through vertical leg + end plate
        shaft_start = -BRKT_T / 2 - 8   # bolt head behind bracket
        shaft_end = ep_yd + EP_T + 3     # bolt tip past end plate
        ax.plot([sx(shaft_start), sx(shaft_end)],
                [sy(bz), sy(bz)],
                color=C_BOLT, lw=3.0, zorder=10)
        # Bolt head (behind bracket, hex head)
        head_w = 8
        ax.add_patch(Rectangle((sx(shaft_start - head_w), sy(bz - 4)),
                                sx(head_w), sy(8),
                                fc=C_BOLT, ec=C_OUT, lw=0.8, zorder=10))
        # Wing nut (on end plate side)
        wing_yd = ep_yd + EP_T + 2
        # Nut body
        ax.add_patch(Rectangle((sx(wing_yd), sy(bz - 3)),
                                sx(5), sy(6),
                                fc=C_BOLT, ec=C_OUT, lw=0.8, zorder=10))
        # Wings (two small triangles)
        wing_h = 10
        wing_w = 3
        # Top wing
        wing_verts_t = [
            (sx(wing_yd + 2), sy(bz + 3)),
            (sx(wing_yd + 2 - wing_w), sy(bz + 3 + wing_h)),
            (sx(wing_yd + 2 + wing_w), sy(bz + 3 + wing_h)),
        ]
        ax.add_patch(Polygon(wing_verts_t, closed=True,
                             fc=C_BOLT, ec=C_OUT, lw=0.6, zorder=10))
        # Bottom wing
        wing_verts_b = [
            (sx(wing_yd + 2), sy(bz - 3)),
            (sx(wing_yd + 2 - wing_w), sy(bz - 3 - wing_h)),
            (sx(wing_yd + 2 + wing_w), sy(bz - 3 - wing_h)),
        ]
        ax.add_patch(Polygon(wing_verts_b, closed=True,
                             fc=C_BOLT, ec=C_OUT, lw=0.6, zorder=10))
        # Hole in end plate
        ax.add_patch(Circle((sx(ep_yd + EP_T / 2), sy(bz)), sx(BOLT_R / 2),
                     fc=C_BOLT, ec=C_OUT, lw=0.5, zorder=11))
        # Hole in bracket vertical leg
        ax.add_patch(Circle((sx(0), sy(bz)), sx(BOLT_R / 2),
                     fc=C_BOLT, ec=C_OUT, lw=0.5, zorder=11))

    # Label the bolts
    leader(ax, sx(ep_yd + EP_T + 12), sy(bolt_z1),
           sx(ep_yd + EP_T + 55), sy(bolt_z1 - 15),
           f"M{BOLT_D} WING BOLT\n(\u00d72, TOOL-FREE\nREMOVAL)",
           color=C_BOLT, fs=5.5,
           ha="left", va="top", arrow_style="-|>", font=FONT)

    # ── Grating resting on beam + arm (ghost) ────────────────────────────────
    C_LEFT_WK = "#A8C8A8"
    # Grating shown as ghost spanning across the beam top
    ax.add_patch(Rectangle((sx(-15), sy(grate_bot)),
                            sx(BEAM_SHOW + 30), sy(WALKWAY_GRATE_T),
                            fc=C_LEFT_WK, ec=C_OUT, lw=0.8, ls="--",
                            alpha=0.25, zorder=4))
    ax.text(sx(BEAM_SHOW / 2), sy(grate_top + 3),
            f"GRATING (GHOST) \u2014 Z={grate_bot}\u2013{grate_top}mm",
            ha="center", va="bottom", fontsize=5.5, color="#206020",
            **FONT, alpha=0.5, zorder=15)

    # ── Contact highlight: beam top flush with arm ───────────────────────────
    ax.plot([sx(beam_yd_start), sx(BEAM_SHOW)],
            [sy(beam_top), sy(beam_top)],
            color="#CC4400", lw=2.5, zorder=9)
    ax.text(sx(beam_yd_start + 30), sy(beam_top + 1),
            f"BEAM TOP FLUSH WITH\nBRACKET ARM (Z={beam_top}mm)",
            ha="left", va="bottom", fontsize=5, color="#CC4400",
            **FONT, zorder=15)

    # ── Dimension lines ──────────────────────────────────────────────────────
    # Beam section size (vertical)
    draw_dim_v(ax, sx(BEAM_SHOW + 15), sy(beam_bot), sy(beam_top),
               f"{BEAM_SZ}mm", offset=sx(6), fs=6, right=True, font=FONT)

    # Beam top from floor
    draw_dim_v(ax, sx(BEAM_SHOW + 15), sy(0), sy(beam_top),
               f"{beam_top}mm", offset=sx(30), fs=5.5, right=True, font=FONT)

    # End plate thickness
    draw_dim_h(ax, sx(ep_yd), sx(ep_yd + EP_T), sy(ep_top + 5),
               f"{EP_T}mm", offset=sy(3), fs=5.5, font=FONT)

    # Bolt spacing
    draw_dim_v(ax, sx(-BRKT_T / 2 - 18), sy(bolt_z1), sy(bolt_z2),
               f"{bolt_z2 - bolt_z1}mm", offset=sx(6), fs=5.5, right=False, font=FONT)

    # Bracket vertical leg height
    draw_dim_v(ax, sx(-CORR_DEPTH - 10), sy(0), sy(BRKT_VERT),
               f"{BRKT_VERT}mm\nVERT LEG", offset=sx(6), fs=5.5, right=False, font=FONT)

    # ── Weld symbol between end plate and beam ───────────────────────────────
    weld_yd = ep_yd + EP_T
    # Small V marks to indicate fillet welds
    for wz in [beam_bot, beam_top]:
        ax.plot([sx(weld_yd - 2), sx(weld_yd), sx(weld_yd + 2)],
                [sy(wz), sy(wz - 4 if wz == beam_bot else wz + 4), sy(wz)],
                color="#CC4400", lw=1.5, zorder=11)
    ax.text(sx(weld_yd + 8), sy(beam_top + 6),
            "FILLET WELD\n(TYP.)", ha="left", va="bottom",
            fontsize=4.5, color="#CC4400", **FONT, zorder=15)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes_x = sx(YD_HI - 5)
    notes_top = sy(Z_HI - 3)
    notes = [
        "BEARER BEAM CONNECTION:",
        "",
        f"1. End plate ({EP_W}\u00d7{BEAM_SZ}\u00d7{EP_T}mm)",
        f"   fillet-welded to beam end.",
        f"2. 2\u00d7 M{BOLT_D} wing bolts through",
        f"   end plate + bracket vertical leg.",
        f"3. Wing nuts for TOOL-FREE removal.",
        f"4. Beam top flush with bracket arm",
        f"   top at Z={beam_top}mm.",
        f"5. Same connection at both ends",
        f"   (near + far bracket).",
        f"6. Remove wing bolts to disconnect",
        f"   beam before lifting grating.",
    ]
    for i, line in enumerate(notes):
        bold = i == 0
        ax.text(notes_x, notes_top - i * sy(5), line,
                ha="right", va="top", fontsize=5.5 if not bold else 6,
                color=C_OUT if bold else C_DIM,
                fontweight="bold" if bold else "normal",
                **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 7 OF 7",
                drawing_title="PERIMETER WALKWAY",
                subtitle="DETAIL E \u2014 BEARER BEAM TO BRACKET CONNECTION",
                scale_note=f"SCALE \u2248 4:1 \u00b7 ALL DIMS IN mm \u00b7 VIEW ALONG X (LOOKING INTO CONTAINER)",
                height=0.07)

    fig.savefig("diagrams/walkway-sheet7.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet7.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet7.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    os.makedirs("diagrams", exist_ok=True)
    print("Generating perimeter walkway diagrams...")
    sheet2()  # plan view → sheet1.png
    sheet1()  # cross-section → sheet2.png
    sheet3()
    sheet4()
    sheet5()
    sheet6()
    sheet7()
    print("Done.")
