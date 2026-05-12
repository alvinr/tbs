#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_walkway_diagram.py  —  TBS-001 Perimeter Walkway

Sheet 1 — Cross-section through near (pinhole side) walkway:
  Detail view (~5:1) showing grated deck, outer frame rail, spanning beam
  (75×75×4mm RHS), tray rim clearance, and dimensional annotations.
  Section cut looking along X axis.  Spanning beam design: no intermediate
  legs on tray floor — legs only at walkway ends (miter corners).

Sheet 2 — Plan view of walkway layout:
  Top-down view showing all 4 walkway sections with end-only leg positions.
  Spanning beam paths, corner connections, and lifting points annotated.
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
    WALKWAY_BEAM_W, WALKWAY_BEAM_H, WALKWAY_BEAM_T,
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
C_LEG   = "#707078"
C_WALL  = "#C0C0C8"
FONT    = {"fontfamily": "monospace"}



# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — Cross-Section Through Near Walkway
#
# View: looking along X axis (into the container).  Section cut through
# the near (pinhole side) walkway at an arbitrary X position.
# Horizontal = Yd (0 = pinhole wall, positive toward far wall)
# Vertical   = Z  (0 = floor, positive up)
# Scale ≈ 5:1 for clarity.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():
    S = 5.0   # scale factor

    def sx(mm): return mm * S
    def sy(mm): return mm * S

    # ── Structural dimensions (mm real) ──────────────────────────────────────
    FRAME_W    = 30    # outer frame channel width (30×30mm angle)
    FRAME_T    = 3     # outer frame angle thickness
    LEG_W      = 25    # end leg SHS width (25×25mm)
    LEG_T      = 2     # end leg wall thickness
    FOOT_W     = 50    # rubber foot pad width
    FOOT_H     = 5     # rubber foot pad height
    TRAY_WALL  = 3     # tray wall thickness (SS)
    TRAY_FLOOR = 2     # tray floor thickness (SS)
    BEAM_W     = WALKWAY_BEAM_W   # 75mm spanning beam width
    BEAM_H     = WALKWAY_BEAM_H   # 75mm spanning beam height
    BEAM_T     = WALKWAY_BEAM_T   # 4mm beam wall thickness

    # Positions (mm real)
    WALL_THICK = 5     # show a sliver of container wall at Yd=0 (schematic)
    TRAY_RIM_YD = PROC_TRAY_YD_NEAR  # = 80mm from wall

    # Outer frame rail — near wall side, on container floor
    OUTER_RAIL_YD = 12             # outer frame rail starts here (foot clears wall)
    LEG_OUTER_YD = OUTER_RAIL_YD + FRAME_W / 2   # = 27mm (centered under outer rail)

    # Spanning beam — inner side, sits on tray floor at walkway inner edge
    # Beam inner face aligns with walkway inner edge (Yd = WALKWAY_W)
    BEAM_YD = WALKWAY_W - BEAM_W   # = 325mm (beam outer face Yd position)

    # ── Figure ───────────────────────────────────────────────────────────────
    # Show Yd from -30 to WALKWAY_W+100 (= 500mm), Z from -30 to WALKWAY_H+WALKWAY_GRATE_T+60
    YD_LO = -60
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

    # ── Container wall (pinhole wall, at Yd=0) ──────────────────────────────
    ax.add_patch(Rectangle((sx(-10), sy(0)), sx(10), sy(Z_HI),
                            fc=C_WALL, ec=C_OUT, lw=1.2, hatch="///", zorder=3))
    ax.text(sx(-20), sy(Z_HI - 15), "PINHOLE\nWALL",
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

    # ── Outer frame rail (30×30mm angle, near wall side) ───────────────────
    frame_top = WALKWAY_H   # top of frame = deck height (100mm)
    frame_bot = WALKWAY_H - FRAME_W  # bottom of outer frame (70mm)

    # Outer frame rail — supported by end legs on container floor
    ax.add_patch(Rectangle((sx(OUTER_RAIL_YD), sy(frame_bot)),
                            sx(FRAME_W), sy(FRAME_W),
                            fc=C_FRAME, ec=C_OUT, lw=1.0, zorder=6))

    # ── Spanning beam (75×75×4mm RHS, inner side) ────────────────────────
    # Beam sits on tray floor, spans full walkway length (legs at ends only)
    beam_floor_z = TRAY_FLOOR   # beam sits on tray floor surface
    beam_top = beam_floor_z + BEAM_H   # = 77mm (just under grating at 100mm)
    ax.add_patch(Rectangle((sx(BEAM_YD), sy(beam_floor_z)),
                            sx(BEAM_W), sy(BEAM_H),
                            fc=C_FRAME, ec=C_OUT, lw=1.2, zorder=6))
    # Hollow interior indication
    ax.add_patch(Rectangle((sx(BEAM_YD + BEAM_T), sy(beam_floor_z + BEAM_T)),
                            sx(BEAM_W - 2 * BEAM_T), sy(BEAM_H - 2 * BEAM_T),
                            fc="#A0A0A8", ec="none", zorder=6, alpha=0.3))

    # Cross-member (connects outer rail to beam top — thin bar)
    xmem_y = beam_top - FRAME_T   # cross-member sits on beam top
    ax.add_patch(Rectangle((sx(OUTER_RAIL_YD + FRAME_W), sy(xmem_y)),
                            sx(BEAM_YD - OUTER_RAIL_YD - FRAME_W), sy(FRAME_T),
                            fc=C_FRAME, ec=C_OUT, lw=0.6, zorder=6))

    # Frame labels
    leader(ax, sx(OUTER_RAIL_YD + FRAME_W / 2), sy(frame_bot - 2),
           sx(OUTER_RAIL_YD - 55), sy(frame_bot - 15),
           "30×30×3mm\nGALV ANGLE\n(OUTER RAIL)", color=C_FRAME, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)
    leader(ax, sx(BEAM_YD + BEAM_W / 2), sy(beam_floor_z + BEAM_H / 2),
           sx(BEAM_YD + BEAM_W + 50), sy(beam_floor_z + BEAM_H / 2 + 20),
           f"{BEAM_W}×{BEAM_H}×{BEAM_T}mm RHS\nGALV STEEL\n(SPANNING BEAM)", color=C_LEG, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Grated deck ──────────────────────────────────────────────────────────
    # Main grate rectangle
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

    ax.text(sx(WALKWAY_W * 4/5), sy(grate_top + 5),
            f"PRESS-LOCKED STEEL GRATING\n{WALKWAY_GRATE_T}mm THICK · GALVANIZED",
            ha="center", va="bottom", fontsize=7, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── Outer end leg (on container floor — shown as ghost, section is mid-span)
    # At mid-span the outer leg is absent (legs at ends only).
    # Draw ghost outline to show where end legs sit.
    leg_top = frame_bot
    leg_h = leg_top - FOOT_H
    ax.add_patch(Rectangle((sx(LEG_OUTER_YD - LEG_W / 2), sy(FOOT_H)),
                            sx(LEG_W), sy(leg_h),
                            fc="none", ec=C_LEG, lw=1.0, ls=(0, (4, 3)),
                            alpha=0.4, zorder=5))
    ax.add_patch(Rectangle((sx(LEG_OUTER_YD - FOOT_W / 2), sy(0)),
                            sx(FOOT_W), sy(FOOT_H),
                            fc="none", ec=C_LEG, lw=0.8, ls=(0, (4, 3)),
                            alpha=0.4, zorder=5))
    ax.text(sx(LEG_OUTER_YD), sy(leg_top / 2),
            "END LEG\n(AT ENDS\nONLY)",
            ha="center", va="center", fontsize=5, color=C_LEG,
            fontweight="bold", **FONT, zorder=15, alpha=0.6)
    leader(ax, sx(LEG_OUTER_YD + LEG_W), sy(leg_top / 2),
           sx(LEG_OUTER_YD + 60), sy(leg_top / 2 - 15),
           f"25×25×2mm SHS\nGALV STEEL\n+ RUBBER FOOT PAD\n(ENDS ONLY — NOT\nAT THIS SECTION)",
           color=C_LEG, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Clear tray floor annotation ──────────────────────────────────────────
    # Arrow showing clear tray floor under the spanning beam
    clr_x = sx(TRAY_RIM_YD + (BEAM_YD - TRAY_RIM_YD) / 2)
    ax.annotate("", xy=(clr_x, sy(TRAY_FLOOR + 1)), xytext=(clr_x, sy(beam_floor_z + BEAM_H - 5)),
                arrowprops=dict(arrowstyle="<->", color="#208020", lw=1.0, mutation_scale=8))
    ax.text(clr_x, sy((beam_floor_z + BEAM_H) / 2),
            "CLEAR\nTRAY\nFLOOR",
            ha="center", va="center", fontsize=5, color="#208020",
            fontweight="bold", **FONT, zorder=15, alpha=0.8)

    # ── Dimension lines ──────────────────────────────────────────────────────
    # Walkway width
    draw_dim_h(ax, sx(0), sx(WALKWAY_W), sy(grate_top + 25),
               f"{WALKWAY_W}mm WALKWAY WIDTH", offset=sy(8), fs=7, font=FONT)

    # Deck height (floor to grate bottom = beam + spacer)
    draw_dim_v(ax, sx(WALKWAY_W + 20), sy(0), sy(grate_bot),
               f"{WALKWAY_H}mm\nDECK H", offset=sx(8), fs=7, right=True, font=FONT)

    # Grate thickness
    draw_dim_v(ax, sx(WALKWAY_W + 20), sy(grate_bot), sy(grate_top),
               f"{WALKWAY_GRATE_T}mm", offset=sx(8), fs=6.5, right=True, font=FONT)

    # Beam height
    draw_dim_v(ax, sx(BEAM_YD - 10), sy(beam_floor_z), sy(beam_floor_z + BEAM_H),
               f"{BEAM_H}mm\nBEAM", offset=sx(8), fs=6.5, right=False, font=FONT)

    # Tray rim height
    draw_dim_v(ax, sx(TRAY_RIM_YD + 15), sy(0), sy(PROC_TRAY_RIM),
               f"{PROC_TRAY_RIM}mm", offset=sx(8), fs=6.5, right=True,
               color=C_TRAY, font=FONT)

    # Clearance above rim (grate bottom to rim top)
    clr = WALKWAY_H - PROC_TRAY_RIM
    draw_dim_v(ax, sx(TRAY_RIM_YD + 15), sy(PROC_TRAY_RIM), sy(WALKWAY_H),
               f"{clr}mm\nCLR", offset=sx(8), fs=6.5, right=True,
               color="#208020", font=FONT)

    # Wall to outer rail
    draw_dim_h(ax, sx(0), sx(OUTER_RAIL_YD), sy(-22),
               f"{OUTER_RAIL_YD}mm", offset=sy(14), fs=6, above=False, font=FONT)

    # Beam position from wall
    draw_dim_h(ax, sx(OUTER_RAIL_YD), sx(BEAM_YD), sy(-22),
               f"{BEAM_YD - OUTER_RAIL_YD}mm", offset=sy(14), fs=6, above=False, font=FONT)

    # ── Person silhouette (standing on walkway, for scale) ───────────────────
    # Simple stick figure, shoe at grate_top
    shoe_yd = WALKWAY_W / 2
    shoe_z = grate_top
    # Shoe
    ax.add_patch(Rectangle((sx(shoe_yd - 15), sy(shoe_z)),
                            sx(30), sy(5),
                            fc="#404040", ec=C_OUT, lw=0.5, zorder=10, alpha=0.4))
    leader(ax, sx(shoe_yd - 15), sy(shoe_z+5),
           sx(95), sy(shoe_z)*1.5,
           f"OPERATOR\n(STANDING SHOE)", color=C_TRAY, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ax.text(sx(shoe_yd + 25), sy(shoe_z + 3),
    #         "OPERATOR\n(STANDING SHOE)",
    #         ha="left", va="center", fontsize=5, color=C_DIM,
    #         **FONT, alpha=0.5, zorder=15)

    # ── Axis labels ──────────────────────────────────────────────────────────
    ax.text(sx(YD_HI / 2), sy(Z_LO + 5),
            "Yd  (container width, 0 = pinhole wall)  →",
            ha="center", va="bottom", fontsize=6.5, color=C_DIM,
            **FONT, zorder=15, style="italic")

    # ── Notes ────────────────────────────────────────────────────────────────
    notes_x = sx(WALKWAY_W + 60)
    notes_top = sy(Z_HI - 10)
    notes = [
        "CONSTRUCTION NOTES:",
        "",
        f"1. Grating: {WALKWAY_GRATE_T}mm press-locked galvanized steel,",
        f"   30×3mm bearing bars at 34.2mm pitch.",
        f"2. Outer rail: 30×30×3mm galvanized angle iron.",
        f"3. Inner beam: {BEAM_W}×{BEAM_H}×{BEAM_T}mm galv RHS — spans full",
        f"   walkway length. Legs at ENDS ONLY (miter corners).",
        f"4. No intermediate legs on tray floor — full tray",
        f"   interior clear for film loading.",
        f"5. Feet: 50×50×5mm EPDM rubber pads.",
        f"6. Grating clips to frame — no permanent fixings.",
        f"7. Each section lifts out for tray access / transport.",
        f"8. Near + far: {PROC_TRAY_W}mm × {WALKWAY_W}mm.  Left + right: {C_WID}mm × {WALKWAY_W}mm.",
    ]
    for i, line in enumerate(notes):
        bold = i == 0
        ax.text(notes_x, notes_top - i * sy(6.5), line,
                ha="left", va="top", fontsize=5.5 if not bold else 6,
                color=C_OUT if bold else C_DIM,
                fontweight="bold" if bold else "normal",
                **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 2",
                drawing_title="PERIMETER WALKWAY",
                subtitle="CROSS-SECTION — NEAR WALKWAY (LOOKING ALONG X AXIS)",
                scale_note="SCALE ≈ 5:1 · ALL DIMS IN mm · SECTION THROUGH PINHOLE SIDE WALKWAY",
                height=0.07)

    fig.savefig("diagrams/walkway-sheet1.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet1.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet1.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Plan View of Walkway Leg Layout
#
# Top-down view showing all 4 walkway sections with leg positions.
# Horizontal = X (container long axis)
# Vertical   = Yd (container width)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():
    import matplotlib.patches as mpatches

    # ── Spanning beam design — legs at ends only ───────────────────────────
    BEAM_W = WALKWAY_BEAM_W   # 75mm beam section width
    END_LEG_INSET = 50        # end leg inset from walkway ends (mm)

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
            f"PROCESSING TRAY\n{PROC_TRAY_W}×{PROC_TRAY_D}mm",
            ha="center", va="center", fontsize=8, color=C_DIM,
            alpha=0.4, **FONT, zorder=3)

    # ── Draw walkway sections (polygon patches with 45° mitered corners) ────
    C_WK = "#D0C8B8"
    WK_ALPHA = 0.6
    W = WALKWAY_W

    # Polygon vertices for each walkway panel — mitered at corners to avoid
    # overlapping hatching where near/far and left/right panels meet.
    LX  = WALKWAY_LEFT_X;   LXR = LX + W        # left walkway X range
    RX  = WALKWAY_RIGHT_X;  RXR = RX + W        # right walkway X range
    NY  = WALKWAY_NEAR_YD;  NYI = NY + W         # near walkway Yd range
    FY  = WALKWAY_FAR_YD;   FYO = FY + W         # far walkway Yd range
    TL  = PROC_TRAY_X_L;   TR = TL + PROC_TRAY_W  # near/far X span

    walkway_polys = [
        # Near walkway: full X span, mitered at both ends
        ("NEAR",  [(TL, NY), (TR, NY), (RX, NYI), (LXR, NYI)],
         TL, NY, PROC_TRAY_W, W, True),
        # Far walkway: full X span, mitered at both ends
        ("FAR",   [(TL, FYO), (TR, FYO), (RX, FY), (LXR, FY)],
         TL, FY, PROC_TRAY_W, W, True),
        # Left walkway: full Yd span, mitered at both ends
        ("LEFT",  [(LX, NY), (LX, FYO), (LXR, FY), (LXR, NYI)],
         LX, 0, W, C_WID, False),
        # Right walkway: full Yd span, mitered at both ends
        ("RIGHT", [(RXR, NY), (RXR, FYO), (RX, FY), (RX, NYI)],
         RX, 0, W, C_WID, False),
    ]

    for name, verts, wx, wy, ww, wh, is_x_axis in walkway_polys:
        # Walkway fill — polygon with mitered corners
        ax.add_patch(Polygon(verts, closed=True,
                             fc=C_WK, ec=C_OUT, lw=1.0, hatch="xx",
                             alpha=WK_ALPHA, zorder=4))

        # Spanning beam centerline (dashed line along inner edge)
        if is_x_axis:
            beam_yd = (wy + WALKWAY_W - BEAM_W / 2) if name == "NEAR" else (wy + BEAM_W / 2)
            ax.plot([wx + END_LEG_INSET, wx + ww - END_LEG_INSET],
                    [beam_yd, beam_yd],
                    color=C_FRAME, lw=2.5, ls=(0, (8, 4)), alpha=0.7, zorder=5)
        else:
            beam_x = (wx + WALKWAY_W - BEAM_W / 2) if name == "RIGHT" else (wx + BEAM_W / 2)
            ax.plot([beam_x, beam_x],
                    [wy + END_LEG_INSET, wy + wh - END_LEG_INSET],
                    color=C_FRAME, lw=2.5, ls=(0, (8, 4)), alpha=0.7, zorder=5)

        # End legs — only at the two ends of each section (near miter corners)
        if is_x_axis:
            for lx in [wx + END_LEG_INSET, wx + ww - END_LEG_INSET]:
                if name == "NEAR":
                    outer_yd = wy + 40
                    inner_yd = wy + WALKWAY_W - BEAM_W / 2
                else:
                    outer_yd = wy + WALKWAY_W - 40
                    inner_yd = wy + BEAM_W / 2
                ax.plot(lx, outer_yd, 'o', color=C_LEG, markersize=4,
                        markeredgecolor=C_OUT, markeredgewidth=0.5, zorder=6)
                ax.plot(lx, inner_yd, 'o', color=C_LEG, markersize=4,
                        markeredgecolor=C_OUT, markeredgewidth=0.5, zorder=6)
        else:
            for lyd in [wy + END_LEG_INSET, wy + wh - END_LEG_INSET]:
                outer_x = wx + 40
                inner_x = wx + WALKWAY_W - BEAM_W / 2
                ax.plot(outer_x, lyd, 'o', color=C_LEG, markersize=4,
                        markeredgecolor=C_OUT, markeredgewidth=0.5, zorder=6)
                ax.plot(inner_x, lyd, 'o', color=C_LEG, markersize=4,
                        markeredgecolor=C_OUT, markeredgewidth=0.5, zorder=6)

        # Section label
        cx = wx + ww / 2
        cy = wy + wh / 2
        rot = 0 if is_x_axis else 90
        length = ww if is_x_axis else wh
        ax.text(cx, cy, f"{name} WALKWAY\n{int(length)}×{WALKWAY_W}mm",
                ha="center", va="center", fontsize=6, color=C_OUT,
                backgroundcolor="#FFFFFF",
                fontweight="bold", **FONT, zorder=7, rotation=rot)

    # ── 45° miter joints at corners ────────────────────────────────────────────
    # Miter lines drawn on top of polygon edges for emphasis.
    corners = [
        # (x_outer, y_outer) = corner of the container; diagonal goes to inner corner
        # Bottom-left: near × left
        (PROC_TRAY_X_L,            0,          PROC_TRAY_X_L + W, W),
        # Bottom-right: near × right
        (PROC_TRAY_X_R,            0,          PROC_TRAY_X_R - W, W),
        # Top-left: far × left
        (PROC_TRAY_X_L,            C_WID,      PROC_TRAY_X_L + W, C_WID - W),
        # Top-right: far × right
        (PROC_TRAY_X_R,            C_WID,      PROC_TRAY_X_R - W, C_WID - W),
    ]
    for x1, y1, x2, y2 in corners:
        ax.plot([x1, x2], [y1, y2], color=C_OUT, lw=1.5, zorder=8)
        # Shared legs on the miter diagonal — support both panels at the joint.
        # Two legs per diagonal at 1/3 and 2/3 positions.
        for t in (1/3, 2/3):
            lx = x1 + t * (x2 - x1)
            ly = y1 + t * (y2 - y1)
            ax.plot(lx, ly, 's', color="#505058", markersize=5,
                    markeredgecolor=C_OUT, markeredgewidth=0.7, zorder=9)
    # Label one miter (bottom-left) — typical for all four
    mx = PROC_TRAY_X_L + W / 2
    my = W / 2
    leader(ax, mx, my, mx - 350, my - 350,
           "45° MITER JOINT\nW/ SHARED END LEGS (TYP.)", color=C_OUT, fs=6,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Lifting point indicators (one per section, centered) ─────────────────
    lift_positions = [
        (PROC_TRAY_X_L + PROC_TRAY_W / 2, WALKWAY_NEAR_YD + WALKWAY_W / 2),
        (PROC_TRAY_X_L + PROC_TRAY_W / 2, WALKWAY_FAR_YD + WALKWAY_W / 2),
        (WALKWAY_LEFT_X + WALKWAY_W / 2, C_WID / 2),
        (WALKWAY_RIGHT_X + WALKWAY_W / 2, C_WID / 2),
    ]

    # ── Open processing area outline ─────────────────────────────────────────
    open_w = PROC_OPEN_X_R - PROC_OPEN_X_L
    open_h = PROC_OPEN_YD_F - PROC_OPEN_YD_N
    ax.add_patch(Rectangle((PROC_OPEN_X_L, PROC_OPEN_YD_N),
                            open_w, open_h,
                            fc="none", ec="#208020", lw=1.5, ls=(0, (6, 3)),
                            zorder=5))
    ax.text(PROC_OPEN_X_L + open_w / 2, PROC_OPEN_YD_N + open_h / 2.25,
            f"OPEN PROCESSING AREA\n{open_w}×{open_h}mm = {PROC_OPEN_AREA:.1f} m²",
            ha="center", va="center", fontsize=7, color="#208020",
            **FONT, zorder=5, alpha=0.6)

    # ── Dimension lines ──────────────────────────────────────────────────────
    # Walkway width dimension (near walkway)
    draw_dim_v(ax, PROC_TRAY_X_L - 40, WALKWAY_NEAR_YD, WALKWAY_NEAR_YD + WALKWAY_W,
               f"{WALKWAY_W}mm", offset=50, fs=6, right=False, font=FONT)

    # Beam span callout (full near walkway length)
    lx0 = PROC_TRAY_X_L + END_LEG_INSET
    lx1 = PROC_TRAY_X_R - END_LEG_INSET
    draw_dim_h(ax, lx0, lx1, -40,
               f"{int(lx1 - lx0)}mm BEAM SPAN (NEAR/FAR)",
               offset=50, fs=6, above=False, font=FONT)

    # ── Legend ────────────────────────────────────────────────────────────────
    legend_x = C_LEN * 4/5
    legend_top = C_WID + 225
    swatches = [
        (C_WK,      WK_ALPHA, "xx",  "o", "Walkway (grated deck)"),
        ("#E8F0FF",  0.3,      None,  "o", "Processing tray"),
        (C_FRAME,    0.7,     None,  "-", f"Spanning beam ({BEAM_W}×{BEAM_W}×{WALKWAY_BEAM_T}mm RHS)"),
        (C_LEG,      1.0,     None,  "o", "End leg position (25mm SHS)"),
        ("#505058",  1.0,     None,  "s", "Shared miter leg"),
    ]
    for i, (c, a, h, marker, lbl) in enumerate(swatches):
        sy_pos = legend_top - i * 50
        if h:
            ax.add_patch(Rectangle((legend_x, sy_pos - 10), 30, 20,
                                    fc=c, ec=C_OUT, lw=0.6, alpha=a,
                                    hatch=h, zorder=15))
        elif marker == "-":
            ax.plot([legend_x, legend_x + 30], [sy_pos, sy_pos],
                    color=c, lw=2.5, ls=(0, (8, 4)), alpha=a, zorder=15)
        elif marker == "s":
            ax.plot(legend_x + 15, sy_pos, 's', color=c, markersize=6,
                    markeredgecolor=C_OUT, markeredgewidth=0.5, zorder=15)
        elif c == C_LEG:
            ax.plot(legend_x + 15, sy_pos, 'o', color=c, markersize=6,
                    markeredgecolor=C_OUT, markeredgewidth=0.5, zorder=15)
        else:
            ax.add_patch(Rectangle((legend_x, sy_pos - 10), 30, 20,
                                    fc=c, ec=C_DIM, lw=0.6, alpha=a,
                                    ls="--", zorder=15))
        ax.text(legend_x + 40, sy_pos, lbl,
                ha="left", va="center", fontsize=5.5, color=C_DIM,
                **FONT, zorder=15)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        f"1. 4 removable sections. 45° miter joints at corners keep all panels level.",
        f"2. Spanning beam design: {BEAM_W}×{BEAM_W}×{WALKWAY_BEAM_T}mm RHS spans full walkway length. Legs at ENDS ONLY.",
        f"3. No intermediate legs on tray floor — full tray interior clear for film loading.",
        f"4. Open processing area: {PROC_OPEN_AREA:.1f} m² ({open_w}×{open_h}mm).",
        f"5. Each section weighs ≈30–40 kg (heavier beam). Two-person lift recommended.",
    ]
    for i, note in enumerate(notes):
        ax.text(C_LEN * 3/5 + PAD_X, -PAD_Y_BOT + 250 + (len(notes) - 1 - i) * 35, note,
                ha="left", va="bottom", fontsize=5.5, color=C_DIM,
                **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 2",
                drawing_title="PERIMETER WALKWAY",
                subtitle="PLAN VIEW — SPANNING BEAM LAYOUT",
                scale_note=f"SCALE ≈ 1:25 · ALL DIMS IN mm · LEGS AT ENDS ONLY",
                height=0.06)

    fig.savefig("diagrams/walkway-sheet2.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/walkway-sheet2.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/walkway-sheet2.png saved")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs("diagrams", exist_ok=True)
    os.makedirs(SVG_DIR, exist_ok=True)
    print("Generating perimeter walkway diagrams...")
    sheet1()
    sheet2()
    print("Done.")
