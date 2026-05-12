#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_walkway_diagram.py  —  TBS-001 Perimeter Walkway

Sheet 1 — Cross-section through near (pinhole side) walkway:
  Detail view (~5:1) showing grated deck, wall-cantilevered bracket,
  tray rim clearance, and dimensional annotations.
  Section cut looking along X axis.  Wall-cantilevered bracket design:
  triangular gusset brackets bolted to container wall ribs — no legs,
  no beam, no floor contact.  Entire tray is clear for film loading.

Sheet 2 — Plan view of walkway layout:
  Top-down view showing all 4 walkway sections with bracket positions.

Sheet 3 — Detail: Single bracket / wall attachment:
  Close-up of gusset bracket bolted to corrugated wall rib, showing
  reinforcing plate, M12 through-bolts, and grating clip.
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
    CONTAINER_RIB_SPACING,
    WALKWAY_NEAR_YD, WALKWAY_FAR_YD, WALKWAY_LEFT_X, WALKWAY_RIGHT_X,
    PROC_OPEN_X_L, PROC_OPEN_X_R, PROC_OPEN_YD_N, PROC_OPEN_YD_F,
    PROC_OPEN_AREA,
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

    # Positions (mm real)
    TRAY_RIM_YD = PROC_TRAY_YD_NEAR  # = 80mm from wall

    # ── Figure ───────────────────────────────────────────────────────────────
    YD_LO = -80
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

    # ── Container wall (pinhole wall, at Yd=0) with corrugation ─────────────
    # Show corrugated wall profile — wall face at Yd=0, corrugation extends
    # inward (positive Yd) by CORR_DEPTH.  Draw a simplified corrugation.
    wall_z_top = Z_HI
    # Flat wall panel (exterior face at Yd ~ -CORR_DEPTH, interior rib at Yd=0)
    ax.add_patch(Rectangle((sx(-CORR_DEPTH - 5), sy(0)),
                            sx(CORR_DEPTH + 5), sy(wall_z_top),
                            fc=C_WALL, ec=C_OUT, lw=1.2, hatch="///", zorder=3))
    # Corrugation rib at section cut (this is where bracket bolts to)
    # Show the rib as a thicker vertical strip at Yd=0
    rib_w = 12  # rib flange width at section
    ax.add_patch(Rectangle((sx(-rib_w / 2), sy(0)),
                            sx(rib_w), sy(wall_z_top),
                            fc="#A8A8B0", ec=C_OUT, lw=1.0, zorder=3))
    ax.text(sx(-CORR_DEPTH / 2 - 5), sy(wall_z_top - 15), "PINHOLE\nWALL\n(CORRUGATED)",
            ha="center", va="top", fontsize=6, color=C_DIM,
            fontweight="bold", **FONT, zorder=15)

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
           sx(TRAY_RIM_YD - 15), sy(PROC_TRAY_RIM + 10),
           f"TRAY RIM\n{PROC_TRAY_RIM}mm\n(304 SS, 3mm)", color=C_TRAY, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)
    # Break line on tray floor (continues right)
    bx = sx(tray_floor_end)
    for z_val in np.linspace(0, TRAY_FLOOR * S, 3):
        ax.plot([bx - 3, bx + 3], [z_val - 2, z_val + 2], color=C_OUT, lw=0.8, zorder=5)

    # Tray "water level" indication (wavy line at ~15mm)
    water_h = 15
    wave_x = np.linspace(sx(TRAY_RIM_YD + 5), sx(tray_floor_end - 10), 40)
    wave_y = sy(water_h) + 3 * np.sin(wave_x * 0.08)
    ax.plot(wave_x, wave_y, color="#4080C0", lw=1.0, alpha=0.6, zorder=4)
    ax.text(sx(TRAY_RIM_YD + 60), sy(water_h + 5),
            "PROCESS WATER\n(~15mm depth)",
            ha="left", va="bottom", fontsize=5.5, color="#4080C0",
            **FONT, alpha=0.7, zorder=15)

    # ── Cantilever bracket (triangular gusset) ───────────────────────────────
    # Bracket profile: right-triangle gusset bolted to wall rib
    # - Vertical leg: from Z=0 to Z=BRKT_VERT (150mm) on wall face
    # - Horizontal arm: from Yd=0 to Yd=WALKWAY_W (300mm) at Z=BRKT_ARM_H (75mm)
    # - Diagonal brace: from (0, BRKT_VERT) to (WALKWAY_W, BRKT_ARM_H)
    # Draw as a filled triangle with plate thickness shown

    brkt_arm_z = BRKT_ARM_H  # = 75mm (top of horizontal arm = grate support)

    # Outer triangle (bracket profile)
    tri_verts = [
        (sx(0), sy(0)),                          # bottom at wall
        (sx(0), sy(BRKT_VERT)),                  # top of vertical leg on wall
        (sx(WALKWAY_W), sy(brkt_arm_z)),          # tip of horizontal arm
    ]
    ax.add_patch(Polygon(tri_verts, closed=True,
                         fc=C_BRKT, ec=C_OUT, lw=1.5, zorder=6, alpha=0.8))

    # Horizontal arm top surface (where grate sits) — emphasize with thicker line
    ax.plot([sx(0), sx(WALKWAY_W)], [sy(brkt_arm_z), sy(brkt_arm_z)],
            color=C_OUT, lw=2.0, zorder=7)

    # Plate thickness indication — inner triangle (cutout to show it's plate, not solid)
    inset = BRKT_T * 2  # visual inset for clarity
    inner_verts = [
        (sx(inset), sy(inset + 10)),
        (sx(inset), sy(BRKT_VERT - inset)),
        (sx(WALKWAY_W - inset * 3), sy(brkt_arm_z)),
    ]
    ax.add_patch(Polygon(inner_verts, closed=True,
                         fc="#8890A0", ec="none", zorder=6, alpha=0.3))

    # Bolt holes on vertical leg (2× M12, centered on rib)
    bolt_z1 = 30
    bolt_z2 = 120
    bolt_r = 6   # M12 hole radius
    for bz in [bolt_z1, bolt_z2]:
        ax.add_patch(Circle((sx(0), sy(bz)), sx(bolt_r),
                     fc=BG, ec=C_OUT, lw=1.0, zorder=8))
        # Cross marks
        ax.plot([sx(-3), sx(3)], [sy(bz), sy(bz)], color=C_OUT, lw=0.5, zorder=9)
        ax.plot([sx(0), sx(0)], [sy(bz - 3), sy(bz + 3)], color=C_OUT, lw=0.5, zorder=9)

    # Bracket label
    leader(ax, sx(WALKWAY_W * 0.4), sy(brkt_arm_z - 15),
           sx(WALKWAY_W * 0.4 + 50), sy(brkt_arm_z - 40),
           f"CANTILEVER BRACKET\n{BRKT_T}mm STEEL PLATE\nGUSSET (TYP.)",
           color=C_BRKT, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # Bolt label
    leader(ax, sx(5), sy(bolt_z1),
           sx(-40), sy(bolt_z1 - 20),
           "2× M12 THROUGH-\nBOLTS TO WALL RIB\n(W/ REINFORCING\nPLATE BEHIND)",
           color=C_DIM, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Grated deck ──────────────────────────────────────────────────────────
    grate_bot = WALKWAY_H
    grate_top = WALKWAY_H + WALKWAY_GRATE_T
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

    ax.text(sx(WALKWAY_W / 2), sy(grate_top + 5),
            f"PRESS-LOCKED STEEL GRATING\n{WALKWAY_GRATE_T}mm THICK · GALVANIZED",
            ha="center", va="bottom", fontsize=7, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

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
    draw_dim_h(ax, sx(0), sx(WALKWAY_W), sy(grate_top + 25),
               f"{WALKWAY_W}mm WALKWAY WIDTH", offset=sy(8), fs=7, font=FONT)

    # Deck height (floor to grate bottom)
    draw_dim_v(ax, sx(WALKWAY_W + 20), sy(0), sy(grate_bot),
               f"{WALKWAY_H}mm\nDECK H", offset=sx(8), fs=7, right=True, font=FONT)

    # Grate thickness
    draw_dim_v(ax, sx(WALKWAY_W + 20), sy(grate_bot), sy(grate_top),
               f"{WALKWAY_GRATE_T}mm", offset=sx(8), fs=6.5, right=True, font=FONT)

    # Bracket vertical leg height
    draw_dim_v(ax, sx(-CORR_DEPTH - 15), sy(0), sy(BRKT_VERT),
               f"{BRKT_VERT}mm\nVERT LEG", offset=sx(8), fs=6.5, right=False, font=FONT)

    # Bracket arm height
    draw_dim_v(ax, sx(WALKWAY_W + 55), sy(0), sy(brkt_arm_z),
               f"{brkt_arm_z}mm\nARM", offset=sx(8), fs=6.5, right=True, font=FONT)

    # Tray rim height
    draw_dim_v(ax, sx(TRAY_RIM_YD + 15), sy(0), sy(PROC_TRAY_RIM),
               f"{PROC_TRAY_RIM}mm", offset=sx(8), fs=6.5, right=True,
               color=C_TRAY, font=FONT)

    # Clearance above rim (grate bottom to rim top)
    clr = WALKWAY_H - PROC_TRAY_RIM
    draw_dim_v(ax, sx(TRAY_RIM_YD + 15), sy(PROC_TRAY_RIM), sy(WALKWAY_H),
               f"{clr}mm\nCLR", offset=sx(8), fs=6.5, right=True,
               color="#208020", font=FONT)

    # Corrugation depth
    draw_dim_h(ax, sx(-CORR_DEPTH), sx(0), sy(-22),
               f"{CORR_DEPTH}mm\nCORR", offset=sy(14), fs=6, above=False, font=FONT)

    # Wall to tray rim
    draw_dim_h(ax, sx(0), sx(TRAY_RIM_YD), sy(-45),
               f"{TRAY_RIM_YD}mm", offset=sy(14), fs=6, above=False, font=FONT)

    # ── Person silhouette ────────────────────────────────────────────────────
    shoe_yd = WALKWAY_W / 2
    shoe_z = grate_top
    ax.add_patch(Rectangle((sx(shoe_yd - 15), sy(shoe_z)),
                            sx(30), sy(5),
                            fc="#404040", ec=C_OUT, lw=0.5, zorder=10, alpha=0.4))
    leader(ax, sx(shoe_yd - 15), sy(shoe_z + 5),
           sx(95), sy(shoe_z) * 1.5,
           "OPERATOR\n(STANDING SHOE)", color=C_TRAY, fs=6,
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
        f"6. Each section lifts off brackets for tray access.",
        f"7. Near + far: {PROC_TRAY_W}\u00d7{WALKWAY_W}mm.  Left + right: {C_WID}\u00d7{WALKWAY_W}mm.",
    ]
    for i, line in enumerate(notes):
        bold = i == 0
        ax.text(notes_x, notes_top - i * sy(6.5), line,
                ha="left", va="top", fontsize=5.5 if not bold else 6,
                color=C_OUT if bold else C_DIM,
                fontweight="bold" if bold else "normal",
                **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 3",
                drawing_title="PERIMETER WALKWAY",
                subtitle="CROSS-SECTION \u2014 NEAR WALKWAY (LOOKING ALONG X AXIS)",
                scale_note=f"SCALE \u2248 5:1 \u00b7 ALL DIMS IN mm \u00b7 SECTION AT BRACKET POSITION",
                height=0.07)

    fig.savefig("diagrams/walkway-sheet1.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet1.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet1.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Plan View of Walkway Layout
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

    # ── Draw walkway sections (polygon patches with 45° mitered corners) ────
    C_WK = "#D0C8B8"
    WK_ALPHA = 0.6
    W = WALKWAY_W

    LX  = WALKWAY_LEFT_X;   LXR = LX + W
    RX  = WALKWAY_RIGHT_X;  RXR = RX + W
    NY  = WALKWAY_NEAR_YD;  NYI = NY + W
    FY  = WALKWAY_FAR_YD;   FYO = FY + W
    TL  = PROC_TRAY_X_L;   TR = TL + PROC_TRAY_W

    walkway_polys = [
        ("NEAR",  [(TL, NY), (TR, NY), (RX, NYI), (LXR, NYI)],
         TL, NY, PROC_TRAY_W, W, True),
        ("FAR",   [(TL, FYO), (TR, FYO), (RX, FY), (LXR, FY)],
         TL, FY, PROC_TRAY_W, W, True),
        ("LEFT",  [(LX, NY), (LX, FYO), (LXR, FY), (LXR, NYI)],
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
        else:
            # Left/right walkways: brackets along end walls
            yd_start = wy
            yd_end = wy + wh
            brkt_yds = np.arange(yd_start + WALKWAY_BRACKET_SPACING / 2,
                                 yd_end, WALKWAY_BRACKET_SPACING)
            for by in brkt_yds:
                if name == "LEFT":
                    ax.add_patch(Rectangle((LX, by - BRKT_MARK_W / 2),
                                 BRKT_MARK_D, BRKT_MARK_W,
                                 fc=C_BRKT, ec=C_OUT, lw=0.6, zorder=6))
                else:
                    ax.add_patch(Rectangle((RXR - BRKT_MARK_D, by - BRKT_MARK_W / 2),
                                 BRKT_MARK_D, BRKT_MARK_W,
                                 fc=C_BRKT, ec=C_OUT, lw=0.6, zorder=6))

        # Section label
        cx = wx + ww / 2
        cy = wy + wh / 2
        rot = 0 if is_x_axis else 90
        length = ww if is_x_axis else wh
        ax.text(cx, cy, f"{name} WALKWAY\n{int(length)}\u00d7{WALKWAY_W}mm",
                ha="center", va="center", fontsize=6, color=C_OUT,
                backgroundcolor="#FFFFFF",
                fontweight="bold", **FONT, zorder=7, rotation=rot)

    # ── 45° miter joints at corners ────────────────────────────────────────────
    corners = [
        (PROC_TRAY_X_L, 0, PROC_TRAY_X_L + W, W),
        (PROC_TRAY_X_R, 0, PROC_TRAY_X_R - W, W),
        (PROC_TRAY_X_L, C_WID, PROC_TRAY_X_L + W, C_WID - W),
        (PROC_TRAY_X_R, C_WID, PROC_TRAY_X_R - W, C_WID - W),
    ]
    for x1, y1, x2, y2 in corners:
        ax.plot([x1, x2], [y1, y2], color=C_OUT, lw=1.5, zorder=8)

    # Label one miter (bottom-left)
    mx = PROC_TRAY_X_L + W / 2
    my = W / 2
    leader(ax, mx, my, mx - 350, my - 350,
           "45\u00b0 MITER JOINT\n(BRACKETS ON BOTH\nADJOINING WALLS)", color=C_OUT, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

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
    n_brackets_near = len(np.arange(TL + WALKWAY_BRACKET_SPACING / 2,
                                     TR, WALKWAY_BRACKET_SPACING))
    n_brackets_total = n_brackets_near * 2 + len(np.arange(
        WALKWAY_BRACKET_SPACING / 2, C_WID, WALKWAY_BRACKET_SPACING)) * 2
    notes = [
        f"1. 4 removable grated sections. 45\u00b0 miter joints at corners.",
        f"2. Wall-cantilevered brackets: {WALKWAY_BRACKET_T}mm steel plate gussets bolted to wall ribs at {WALKWAY_BRACKET_SPACING}mm centers.",
        f"3. NO legs on tray floor \u2014 entire tray interior clear for film loading. Zero floor contact.",
        f"4. Open processing area: {PROC_OPEN_AREA:.1f} m\u00b2 ({open_w}\u00d7{open_h}mm).",
        f"5. ~{n_brackets_total} brackets total. Each section lifts off brackets for tray access.",
    ]
    for i, note in enumerate(notes):
        ax.text(C_LEN * 3 / 5 + PAD_X, -PAD_Y_BOT + 250 + (len(notes) - 1 - i) * 35, note,
                ha="left", va="bottom", fontsize=5.5, color=C_DIM,
                **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 3",
                drawing_title="PERIMETER WALKWAY",
                subtitle="PLAN VIEW \u2014 WALL-CANTILEVERED BRACKET LAYOUT",
                scale_note=f"SCALE \u2248 1:25 \u00b7 ALL DIMS IN mm \u00b7 BRACKETS AT {WALKWAY_BRACKET_SPACING}mm CENTERS",
                height=0.06)

    fig.savefig("diagrams/walkway-sheet2.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet2.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet2.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — Detail: Bracket / Wall Attachment
#
# View: looking along X axis at a single bracket bolted to the corrugated
# wall.  Shows corrugation profile, reinforcing plate behind wall,
# M12 through-bolts, gusset bracket, and grating sitting on arm.
# Scale ≈ 3:1 for clarity.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet3():
    S = 3.0

    def sx(mm): return mm * S
    def sy(mm): return mm * S

    # ── Structural dimensions ────────────────────────────────────────────────
    CORR_DEPTH = 38    # corrugation depth (mm)
    CORR_PITCH = 152   # corrugation center-to-center pitch (mm)
    WALL_T     = 1.6   # wall steel thickness
    REINF_W    = 80    # reinforcing plate width behind wall
    REINF_H    = 180   # reinforcing plate height
    REINF_T    = 6     # reinforcing plate thickness
    BRKT_T     = WALKWAY_BRACKET_T  # 8mm
    BRKT_VERT  = WALKWAY_BRACKET_H  # 150mm
    BRKT_ARM_Z = WALKWAY_H - WALKWAY_GRATE_T  # = 75mm
    BOLT_D     = 12    # M12 bolt diameter
    TRAY_WALL  = 3
    TRAY_FLOOR_T = 2

    TRAY_RIM_YD = PROC_TRAY_YD_NEAR  # = 80mm

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

    # ── Corrugated wall profile ──────────────────────────────────────────────
    # Show the corrugation as a trapezoidal profile in cross-section
    # Rib flange at Yd=0, panel recedes to Yd=-CORR_DEPTH
    # At the section cut we're at a rib (where the bracket bolts on)
    rib_flange_w = 25   # rib top flange width (flat part)

    # Draw corrugated wall — simplified profile
    # Exterior panel (behind corrugation)
    ax.add_patch(Rectangle((sx(-CORR_DEPTH - WALL_T), sy(0)),
                            sx(WALL_T), sy(Z_HI),
                            fc="#A0A0A8", ec=C_OUT, lw=0.8, zorder=3))
    # Corrugation rib (at section cut) — trapezoidal
    rib_verts = [
        (sx(-CORR_DEPTH), sy(0)),
        (sx(-CORR_DEPTH), sy(Z_HI)),
        (sx(0), sy(Z_HI)),
        (sx(0), sy(0)),
    ]
    # Simplified: draw rib as a rectangle with hatching
    ax.add_patch(Rectangle((sx(-CORR_DEPTH), sy(0)),
                            sx(CORR_DEPTH), sy(Z_HI),
                            fc=C_WALL, ec=C_OUT, lw=1.0, hatch="///", zorder=3))
    # Rib face (where bracket mates)
    ax.add_patch(Rectangle((sx(-2), sy(0)),
                            sx(rib_flange_w + 2), sy(Z_HI),
                            fc="#B0B0B8", ec=C_OUT, lw=0.8, zorder=3))

    ax.text(sx(-CORR_DEPTH / 2), sy(Z_HI - 10), "CONTAINER\nWALL\n(1.6mm CORTEN\nCORRUGATED)",
            ha="center", va="top", fontsize=5.5, color=C_DIM,
            fontweight="bold", **FONT, zorder=15)

    # ── Reinforcing plate (behind wall, at bolt positions) ───────────────────
    reinf_z0 = 0
    ax.add_patch(Rectangle((sx(-CORR_DEPTH - WALL_T - REINF_T), sy(reinf_z0)),
                            sx(REINF_T), sy(REINF_H),
                            fc="#C08040", ec=C_OUT, lw=1.0, zorder=4))
    leader(ax, sx(-CORR_DEPTH - WALL_T - REINF_T / 2), sy(REINF_H),
           sx(-CORR_DEPTH - 30), sy(REINF_H + 25),
           f"REINFORCING PLATE\n{REINF_W}\u00d7{REINF_H}\u00d7{REINF_T}mm\nMILD STEEL",
           color="#C08040", fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Processing tray ──────────────────────────────────────────────────────
    ax.add_patch(Rectangle((sx(TRAY_RIM_YD - TRAY_WALL), sy(0)),
                            sx(TRAY_WALL), sy(PROC_TRAY_RIM),
                            fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=4))
    tray_floor_end = YD_HI - 20
    ax.add_patch(Rectangle((sx(TRAY_RIM_YD), sy(0)),
                            sx(tray_floor_end - TRAY_RIM_YD), sy(TRAY_FLOOR_T),
                            fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))
    leader(ax, sx(TRAY_RIM_YD + 5), sy(PROC_TRAY_RIM),
           sx(TRAY_RIM_YD + 50), sy(PROC_TRAY_RIM + 20),
           f"TRAY RIM {PROC_TRAY_RIM}mm", color=C_TRAY, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Bracket (triangular gusset) ──────────────────────────────────────────
    tri_verts = [
        (sx(0), sy(0)),
        (sx(0), sy(BRKT_VERT)),
        (sx(WALKWAY_W), sy(BRKT_ARM_Z)),
    ]
    ax.add_patch(Polygon(tri_verts, closed=True,
                         fc=C_BRKT, ec=C_OUT, lw=1.5, zorder=6, alpha=0.85))

    # Plate thickness indication
    inset = BRKT_T * 2
    inner_verts = [
        (sx(inset), sy(inset + 10)),
        (sx(inset), sy(BRKT_VERT - inset)),
        (sx(WALKWAY_W - inset * 3), sy(BRKT_ARM_Z)),
    ]
    ax.add_patch(Polygon(inner_verts, closed=True,
                         fc="#8890A0", ec="none", zorder=6, alpha=0.3))

    # Horizontal arm top surface
    ax.plot([sx(0), sx(WALKWAY_W)], [sy(BRKT_ARM_Z), sy(BRKT_ARM_Z)],
            color=C_OUT, lw=2.0, zorder=7)

    # Weld symbol on diagonal brace (simplified — triangle at joint)
    # Show small weld marks where diagonal meets vertical and horizontal
    weld_sz = 5
    for wx_pos, wz_pos in [(5, 10), (WALKWAY_W * 0.15, BRKT_ARM_Z)]:
        ax.plot([sx(wx_pos - weld_sz), sx(wx_pos), sx(wx_pos + weld_sz)],
                [sy(wz_pos), sy(wz_pos + weld_sz), sy(wz_pos)],
                color="#CC4400", lw=1.5, zorder=8)

    # Bolt holes
    bolt_z1 = 30
    bolt_z2 = 120
    bolt_r = 6
    for bz in [bolt_z1, bolt_z2]:
        ax.add_patch(Circle((sx(rib_flange_w / 2), sy(bz)), sx(bolt_r),
                     fc=BG, ec=C_OUT, lw=1.2, zorder=8))
        # Bolt head / washer (exterior side)
        ax.add_patch(Rectangle((sx(-CORR_DEPTH - WALL_T - REINF_T - 5),
                                 sy(bz - 8)), sx(5), sy(16),
                     fc="#606060", ec=C_OUT, lw=0.8, zorder=5))
        # Nut (interior side, on bracket face)
        ax.add_patch(Rectangle((sx(rib_flange_w / 2 + bolt_r + 1),
                                 sy(bz - 6)), sx(8), sy(12),
                     fc="#606060", ec=C_OUT, lw=0.8, zorder=8))

    # Bolt label
    leader(ax, sx(rib_flange_w / 2 + bolt_r + 10), sy(bolt_z1),
           sx(rib_flange_w + 60), sy(bolt_z1 - 25),
           f"M{BOLT_D} \u00d7 60mm\nHEX BOLT + NUT\n+ FLAT WASHER\n(2 PER BRACKET)",
           color=C_DIM, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # Bracket label
    leader(ax, sx(WALKWAY_W * 0.35), sy(BRKT_ARM_Z - 15),
           sx(WALKWAY_W * 0.5), sy(BRKT_ARM_Z - 45),
           f"GUSSET BRACKET\n{BRKT_T}mm STEEL PLATE\n{BRKT_VERT}mm VERT \u00d7 {WALKWAY_W}mm ARM",
           color=C_BRKT, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Grated deck ──────────────────────────────────────────────────────────
    grate_bot = WALKWAY_H
    grate_top = WALKWAY_H + WALKWAY_GRATE_T
    ax.add_patch(Rectangle((sx(0), sy(grate_bot)),
                            sx(WALKWAY_W), sy(WALKWAY_GRATE_T),
                            fc=C_GRATE, ec=C_OUT, lw=1.2, zorder=7))
    bar_spacing = 34.2
    bar_w = 3
    for yd in np.arange(bar_w, WALKWAY_W - bar_w, bar_spacing):
        ax.add_patch(Rectangle((sx(yd), sy(grate_bot)),
                                sx(bar_w), sy(WALKWAY_GRATE_T),
                                fc="#909098", ec=C_OUT, lw=0.3, zorder=8))

    # Grating clip detail (small L-bracket securing grate to bracket arm)
    clip_yd = WALKWAY_W * 0.6
    clip_w = 10
    clip_h = 15
    ax.add_patch(Rectangle((sx(clip_yd), sy(BRKT_ARM_Z - clip_h)),
                            sx(clip_w), sy(clip_h + WALKWAY_GRATE_T + 5),
                            fc="#505058", ec=C_OUT, lw=0.8, zorder=9))
    leader(ax, sx(clip_yd + clip_w), sy(BRKT_ARM_Z),
           sx(clip_yd + 50), sy(BRKT_ARM_Z + 35),
           "GRATING CLIP\n(REMOVABLE)", color="#505058", fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Dimension lines ──────────────────────────────────────────────────────
    # Bracket vertical leg
    draw_dim_v(ax, sx(-CORR_DEPTH - WALL_T - REINF_T - 20), sy(0), sy(BRKT_VERT),
               f"{BRKT_VERT}mm\nVERT", offset=sx(6), fs=6.5, right=False, font=FONT)

    # Bracket arm (horizontal projection)
    draw_dim_h(ax, sx(0), sx(WALKWAY_W), sy(grate_top + 20),
               f"{WALKWAY_W}mm CANTILEVER ARM", offset=sy(6), fs=7, font=FONT)

    # Deck height
    draw_dim_v(ax, sx(WALKWAY_W + 15), sy(0), sy(grate_bot),
               f"{WALKWAY_H}mm\nDECK", offset=sx(6), fs=6.5, right=True, font=FONT)

    # Grate thickness
    draw_dim_v(ax, sx(WALKWAY_W + 15), sy(grate_bot), sy(grate_top),
               f"{WALKWAY_GRATE_T}mm", offset=sx(6), fs=6, right=True, font=FONT)

    # Corrugation depth
    draw_dim_h(ax, sx(-CORR_DEPTH), sx(0), sy(-25),
               f"{CORR_DEPTH}mm CORR", offset=sy(10), fs=6, above=False, font=FONT)

    # Bolt spacing (vertical)
    draw_dim_v(ax, sx(rib_flange_w + 30), sy(bolt_z1), sy(bolt_z2),
               f"{bolt_z2 - bolt_z1}mm", offset=sx(6), fs=6, right=True, font=FONT)

    # Clear air under bracket arm
    gap = BRKT_ARM_Z - TRAY_FLOOR_T
    clr_x = sx(WALKWAY_W * 0.75)
    ax.annotate("", xy=(clr_x, sy(TRAY_FLOOR_T + 1)), xytext=(clr_x, sy(BRKT_ARM_Z - 1)),
                arrowprops=dict(arrowstyle="<->", color="#208020", lw=1.2, mutation_scale=8))
    ax.text(clr_x + sx(5), sy((TRAY_FLOOR_T + BRKT_ARM_Z) / 2),
            f"{gap:.0f}mm CLEAR\n(ZERO TRAY\nCONTACT)",
            ha="left", va="center", fontsize=5.5, color="#208020",
            fontweight="bold", **FONT, zorder=15, alpha=0.8)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes_x = sx(WALKWAY_W + 50)
    notes_top = sy(Z_HI - 10)
    notes = [
        "BRACKET ATTACHMENT DETAIL:",
        "",
        f"1. Outer bolt hole center is {rib_flange_w / 2:.0f}mm from rib face.",
        f"   Bolts pass through bracket + rib + reinforcing plate.",
        f"2. Reinforcing plate ({REINF_W}\u00d7{REINF_H}\u00d7{REINF_T}mm) welded or",
        f"   bonded to exterior wall face before drilling.",
        f"3. Weld symbol: fillet weld on diagonal brace to",
        f"   vertical and horizontal legs (both sides).",
        f"4. Grating clips slide over bracket arm top \u2014",
        f"   removable without tools for tray access.",
        f"5. Bracket spacing: {WALKWAY_BRACKET_SPACING}mm (every wall rib).",
    ]
    for i, line in enumerate(notes):
        bold = i == 0
        ax.text(notes_x, notes_top - i * sy(6), line,
                ha="left", va="top", fontsize=5.5 if not bold else 6,
                color=C_OUT if bold else C_DIM,
                fontweight="bold" if bold else "normal",
                **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 3 OF 3",
                drawing_title="PERIMETER WALKWAY",
                subtitle="DETAIL \u2014 WALL BRACKET ATTACHMENT",
                scale_note=f"SCALE \u2248 3:1 \u00b7 ALL DIMS IN mm \u00b7 SECTION AT WALL RIB",
                height=0.07)

    fig.savefig("diagrams/walkway-sheet3.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet3.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet3.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    os.makedirs("diagrams", exist_ok=True)
    print("Generating perimeter walkway diagrams...")
    sheet1()
    sheet2()
    sheet3()
    print("Done.")
