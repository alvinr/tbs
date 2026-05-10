#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_walkway_diagram.py  —  TBS-001 Perimeter Walkway

Sheet 1 — Cross-section through near (pinhole side) walkway:
  Detail view (~5:1) showing grated deck, support frame, legs, tray rim
  clearance, and dimensional annotations.  Section cut looking along X axis.

Sheet 2 — Plan view of walkway leg layout:
  Top-down view showing all 4 walkway sections with leg positions marked.
  Leg spacing, corner connections, and lifting points annotated.
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
    FRAME_W    = 30    # frame channel width (30×30mm angle)
    FRAME_T    = 3     # frame angle thickness
    LEG_W      = 25    # leg SHS width (25×25mm)
    LEG_T      = 2     # leg wall thickness
    FOOT_W     = 50    # rubber foot pad width
    FOOT_H     = 5     # rubber foot pad height
    TRAY_WALL  = 3     # tray wall thickness (SS)
    TRAY_FLOOR = 2     # tray floor thickness (SS)

    # Positions (mm real)
    WALL_THICK = 5     # show a sliver of container wall at Yd=0 (schematic)
    TRAY_RIM_YD = PROC_TRAY_YD_NEAR  # = 80mm from wall

    # Frame rail Yd positions (set here so legs align to them)
    OUTER_RAIL_YD = 12             # outer frame rail starts here (foot clears wall)
    INNER_RAIL_YD = WALKWAY_W - FRAME_W - 5  # inner frame rail starts here (= 365mm)

    # Leg positions — centered directly under each frame rail
    LEG_OUTER_YD = OUTER_RAIL_YD + FRAME_W / 2   # = 20mm (centered under outer rail)
    LEG_INNER_YD = INNER_RAIL_YD + FRAME_W / 2   # = 380mm (centered under inner rail)

    # ── Figure ───────────────────────────────────────────────────────────────
    # Show Yd from -30 to WALKWAY_W+100 (= 500mm), Z from -30 to WALKWAY_H+WALKWAY_GRATE_T+60
    YD_LO = -60
    YD_HI = WALKWAY_W + 180
    Z_LO  = -40
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
    leader(ax, sx(TRAY_RIM_YD - 1), sy(PROC_TRAY_RIM / 2),
           sx(TRAY_RIM_YD - 25), sy(PROC_TRAY_RIM + 10),
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

    # ── Support frame (30×30mm angle iron perimeter) ─────────────────────────
    frame_top = WALKWAY_H   # top of frame = deck height
    frame_bot = WALKWAY_H - FRAME_W  # bottom of frame

    # Outer frame rail (near wall side) — legs sit directly under this
    ax.add_patch(Rectangle((sx(OUTER_RAIL_YD), sy(frame_bot)),
                            sx(FRAME_W), sy(FRAME_W),
                            fc=C_FRAME, ec=C_OUT, lw=1.0, zorder=6))
    # Inner frame rail (tray side) — legs sit directly under this
    ax.add_patch(Rectangle((sx(INNER_RAIL_YD), sy(frame_bot)),
                            sx(FRAME_W), sy(FRAME_W),
                            fc=C_FRAME, ec=C_OUT, lw=1.0, zorder=6))
    # Cross-member (connects outer and inner rails — shown as thin bar)
    ax.add_patch(Rectangle((sx(OUTER_RAIL_YD + FRAME_W), sy(frame_top - FRAME_T)),
                            sx(INNER_RAIL_YD - OUTER_RAIL_YD - FRAME_W), sy(FRAME_T),
                            fc=C_FRAME, ec=C_OUT, lw=0.6, zorder=6))

    # Frame labels
    leader(ax, sx(OUTER_RAIL_YD + FRAME_W / 2), sy(frame_bot + FRAME_W / 2),
           sx(OUTER_RAIL_YD - 35), sy(frame_bot - 10),
           "30×30×3mm\nGALV ANGLE", color=C_FRAME, fs=5.5,
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

    ax.text(sx(WALKWAY_W / 2), sy(grate_top + 5),
            f"PRESS-LOCKED STEEL GRATING\n{WALKWAY_GRATE_T}mm THICK · GALVANIZED",
            ha="center", va="bottom", fontsize=7, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)

    # ── Legs ─────────────────────────────────────────────────────────────────
    def draw_leg(yd, stands_on_tray=False):
        """Draw a leg (25×25mm SHS) from frame bottom to floor/tray-floor."""
        leg_top = frame_bot
        floor_z = TRAY_FLOOR if stands_on_tray else 0
        leg_h = leg_top - floor_z - FOOT_H

        # SHS leg
        ax.add_patch(Rectangle((sx(yd - LEG_W / 2), sy(floor_z + FOOT_H)),
                                sx(LEG_W), sy(leg_h),
                                fc=C_LEG, ec=C_OUT, lw=1.0, zorder=5))
        # Hollow center indication
        ax.add_patch(Rectangle((sx(yd - LEG_W / 2 + LEG_T), sy(floor_z + FOOT_H + 2)),
                                sx(LEG_W - 2 * LEG_T), sy(leg_h - 4),
                                fc="#909098", ec="none", zorder=5, alpha=0.3))
        # Rubber foot pad
        ax.add_patch(Rectangle((sx(yd - FOOT_W / 2), sy(floor_z)),
                                sx(FOOT_W), sy(FOOT_H),
                                fc="#303030", ec=C_OUT, lw=0.8, zorder=5))

    # Outer leg (on container floor, between wall and tray)
    draw_leg(LEG_OUTER_YD, stands_on_tray=False)
    ax.text(sx(LEG_OUTER_YD), sy(-20),
            "OUTER LEG\n(ON FLOOR)",
            ha="center", va="top", fontsize=5.5, color=C_LEG,
            fontweight="bold", **FONT, zorder=15)

    # Inner leg (on tray floor, inside rim)
    draw_leg(LEG_INNER_YD, stands_on_tray=True)
    ax.text(sx(LEG_INNER_YD), sy(-20),
            "INNER LEG\n(ON TRAY FLOOR)",
            ha="center", va="top", fontsize=5.5, color=C_LEG,
            fontweight="bold", **FONT, zorder=15)

    # Leg label
    leader(ax, sx(LEG_OUTER_YD + LEG_W / 2), sy(frame_bot / 2),
           sx(LEG_OUTER_YD + 55), sy(frame_bot / 2 - 10),
           f"25×25×2mm SHS\nGALV STEEL\n+ RUBBER FOOT PAD", color=C_LEG, fs=5.5,
           ha="center", va="center", arrow_style="-|>", font=FONT)

    # ── Dimension lines ──────────────────────────────────────────────────────
    # Walkway width
    draw_dim_h(ax, sx(0), sx(WALKWAY_W), sy(grate_top + 25),
               f"{WALKWAY_W}mm WALKWAY WIDTH", offset=sy(8), fs=7, font=FONT)

    # Deck height (floor to grate top)
    draw_dim_v(ax, sx(WALKWAY_W + 20), sy(0), sy(grate_bot),
               f"{WALKWAY_H}mm\nDECK H", offset=sx(8), fs=7, right=True, font=FONT)

    # Grate thickness
    draw_dim_v(ax, sx(WALKWAY_W + 20), sy(grate_bot), sy(grate_top),
               f"{WALKWAY_GRATE_T}mm", offset=sx(8), fs=6.5, right=True, font=FONT)

    # Tray rim height
    draw_dim_v(ax, sx(TRAY_RIM_YD + 15), sy(0), sy(PROC_TRAY_RIM),
               f"{PROC_TRAY_RIM}mm", offset=sx(8), fs=6.5, right=True,
               color=C_TRAY, font=FONT)

    # Clearance above rim
    clr = WALKWAY_H - PROC_TRAY_RIM
    draw_dim_v(ax, sx(TRAY_RIM_YD + 15), sy(PROC_TRAY_RIM), sy(WALKWAY_H),
               f"{clr}mm\nCLR", offset=sx(8), fs=6.5, right=True,
               color="#208020", font=FONT)

    # Wall to outer leg center
    draw_dim_h(ax, sx(0), sx(LEG_OUTER_YD), sy(-22),
               f"{LEG_OUTER_YD:.0f}mm", offset=sy(7), fs=6, above=False, font=FONT)

    # Outer leg center to inner leg center
    leg_span = LEG_INNER_YD - LEG_OUTER_YD
    draw_dim_h(ax, sx(LEG_OUTER_YD), sx(LEG_INNER_YD), sy(-22),
               f"{leg_span:.0f}mm", offset=sy(7), fs=6, above=False, font=FONT)

    # ── Person silhouette (standing on walkway, for scale) ───────────────────
    # Simple stick figure, shoe at grate_top
    shoe_yd = WALKWAY_W / 2
    shoe_z = grate_top
    # Shoe
    ax.add_patch(Rectangle((sx(shoe_yd - 15), sy(shoe_z)),
                            sx(30), sy(5),
                            fc="#404040", ec=C_OUT, lw=0.5, zorder=10, alpha=0.4))
    leader(ax, sx(shoe_yd - 10), sy(shoe_z),
           sx(45), sy(shoe_z)*1.5,
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
        f"2. Frame: 30×30×3mm galvanized angle iron,",
        f"   perimeter + cross-members at 600mm centers.",
        f"3. Legs: 25×25×2mm galvanized SHS,",
        f"   pairs at 600mm centers along walkway length.",
        f"4. Feet: 50×50×5mm EPDM rubber pads",
        f"   (non-slip, protects tray floor).",
        f"5. Grating clips to frame — no permanent fixings.",
        f"6. Each section lifts out for tray access / transport.",
        f"7. Near + far walkways: 4,459mm long × 400mm wide.",
        f"8. Left + right walkways: 2,362mm long × 400mm wide.",
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

    # ── Leg spacing ──────────────────────────────────────────────────────────
    LEG_SPACING = 600   # leg pair spacing along walkway length (mm)

    # ── Figure ───────────────────────────────────────────────────────────────
    PAD_X = 300
    PAD_Y_BOT = 500   # extra room below for notes + title block
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
    ax.text(C_LEN / 2, C_WID + 40, "FAR WALL (Yd=2362)",
            ha="center", va="bottom", fontsize=6, color=C_DIM, **FONT, zorder=15)
    ax.text(-40, C_WID / 2, "CARGO DOOR\nEND (X=0)",
            ha="right", va="center", fontsize=6, color=C_DIM,
            **FONT, zorder=15, rotation=90)
    ax.text(C_LEN + 40, C_WID / 2, "FAR END\n(X=5893)",
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

    # ── Draw walkway sections ────────────────────────────────────────────────
    C_WK = "#D0C8B8"
    WK_ALPHA = 0.6

    # Walkway section definitions: (x, y, w, h, label, is_long_axis)
    sections = [
        ("NEAR", PROC_TRAY_X_L, WALKWAY_NEAR_YD, PROC_TRAY_W, WALKWAY_W, True),
        ("FAR",  PROC_TRAY_X_L, WALKWAY_FAR_YD,  PROC_TRAY_W, WALKWAY_W, True),
        ("LEFT", WALKWAY_LEFT_X, 0,               WALKWAY_W,   C_WID,     False),
        ("RIGHT", WALKWAY_RIGHT_X, 0,             WALKWAY_W,   C_WID,     False),
    ]

    for name, wx, wy, ww, wh, is_x_axis in sections:
        # Walkway fill
        ax.add_patch(Rectangle((wx, wy), ww, wh,
                                fc=C_WK, ec=C_OUT, lw=1.0, hatch="xx",
                                alpha=WK_ALPHA, zorder=4))

        # Leg positions (pairs of circles)
        if is_x_axis:
            # Long walkways (near/far): legs spaced along X
            n_legs = int(ww / LEG_SPACING) + 1
            leg_xs = np.linspace(wx + 50, wx + ww - 50, n_legs)
            for lx in leg_xs:
                # Outer leg (near wall side for NEAR, far wall side for FAR)
                if name == "NEAR":
                    outer_yd = wy + 40
                    inner_yd = wy + WALKWAY_W - 60
                else:
                    outer_yd = wy + WALKWAY_W - 40
                    inner_yd = wy + 60
                ax.plot(lx, outer_yd, 'o', color=C_LEG, markersize=4,
                        markeredgecolor=C_OUT, markeredgewidth=0.5, zorder=6)
                ax.plot(lx, inner_yd, 'o', color=C_LEG, markersize=4,
                        markeredgecolor=C_OUT, markeredgewidth=0.5, zorder=6)
        else:
            # Short walkways (left/right): legs in the middle section only.
            # Corner miter zones are supported by shared diagonal legs (below).
            leg_yd_lo = WALKWAY_W + 50            # clear of near miter zone
            leg_yd_hi = WALKWAY_FAR_YD - 50       # clear of far miter zone
            n_legs = int((leg_yd_hi - leg_yd_lo) / LEG_SPACING) + 1
            leg_yds = np.linspace(leg_yd_lo, leg_yd_hi, n_legs)
            for lyd in leg_yds:
                # Place legs at 1/4 and 3/4 across walkway width for clear centering
                outer_x = wx + WALKWAY_W * 0.25
                inner_x = wx + WALKWAY_W * 0.75
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
    # Where long (near/far) and short (left/right) walkways meet, a 45° miter
    # prevents overlap while keeping all panels at the same deck level.
    W = WALKWAY_W
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
    leader(ax, mx, my, mx - 350, my - 250,
           "45° MITER JOINT\nW/ SHARED LEGS (TYP.)", color=C_OUT, fs=6,
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
               f"{WALKWAY_W}mm", offset=200, fs=6, right=False, font=FONT)

    # Leg spacing callout
    # Pick two adjacent legs on the near walkway for dimensioning
    n_near = int(PROC_TRAY_W / LEG_SPACING) + 1
    near_xs = np.linspace(PROC_TRAY_X_L + 50, PROC_TRAY_X_R - 50, n_near)
    if len(near_xs) >= 2:
        lx0, lx1 = near_xs[0], near_xs[1]
        draw_dim_h(ax, lx0, lx1, -40,
                   f"{int(lx1 - lx0)}mm LEG SPACING (TYP.)", offset=50, fs=6,
                   above=False, font=FONT)

    # ── Legend ────────────────────────────────────────────────────────────────
    legend_x = C_LEN + 60
    legend_top = C_WID - 50
    swatches = [
        (C_WK,      WK_ALPHA, "xx",  "o", "Walkway (grated deck)"),
        ("#E8F0FF",  0.3,      None,  "o", "Processing tray"),
        (C_LEG,      1.0,     None,  "o", "Leg position (25mm SHS)"),
        ("#505058",  1.0,     None,  "s", "Shared miter leg"),
    ]
    for i, (c, a, h, marker, lbl) in enumerate(swatches):
        sy_pos = legend_top - i * 50
        if h:
            ax.add_patch(Rectangle((legend_x, sy_pos - 10), 30, 20,
                                    fc=c, ec=C_OUT, lw=0.6, alpha=a,
                                    hatch=h, zorder=15))
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
        f"2. Leg pairs at ~{LEG_SPACING}mm centers. Outer legs on container floor, inner legs on tray floor.",
        f"3. Total walkway area: 2×({PROC_TRAY_W}×{WALKWAY_W}) + 2×({C_WID}×{WALKWAY_W}) = "
        f"{2*(PROC_TRAY_W*WALKWAY_W + C_WID*WALKWAY_W)/1e6:.1f} m².",
        f"4. Open processing area: {PROC_OPEN_AREA:.1f} m² ({open_w}×{open_h}mm).",
        f"5. Each section weighs ≈25–35 kg. Single-person lift with handles.",
    ]
    for i, note in enumerate(notes):
        ax.text(-PAD_X + 30, -PAD_Y_BOT + 200 + (len(notes) - 1 - i) * 35, note,
                ha="left", va="bottom", fontsize=5.5, color=C_DIM,
                **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 2",
                drawing_title="PERIMETER WALKWAY",
                subtitle="PLAN VIEW — WALKWAY LEG LAYOUT",
                scale_note=f"SCALE ≈ 1:25 · ALL DIMS IN mm · LEGS AT ~{LEG_SPACING}mm CENTERS")

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
