#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_ceiling_rail_diagram.py  —  TBS-001 Ceiling Rail Suspension System

Sheet 1 — Side elevation cross-section (looking along Yd axis):
  Panel suspended from HGR20 ceiling-mounted linear rails, showing:
  - Ceiling rail and carriage block detail
  - Panel in operational position (X=0, sealed to fixed door frame)
  - Panel in transport position (X=300, ghost outline)
  - Processing tray on floor (50mm rim)
  - Floor gap clearance (80mm panel bottom to floor)
  - Container wall, fixed door frame, EPDM seal

Sheet 2 — Detail view of rail/carriage interface:
  Close-up of HGR20 rail mounted to ceiling, HGH20CA carriage block,
  suspension bracket, and panel top connection.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Polygon
from matplotlib.lines import Line2D
import os
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_notes
from tbs_constants import (
    svg_path, SVG_DIR,
    C_LEN, C_WID, C_HGT, WALL_T,
    PANEL_CORNER_T, PANEL_CENTER_T, PANEL_SLIDE, PANEL_FLOOR_GAP,
    PANEL_CORNER_YD_L, PANEL_CORNER_YD_R,
    PROC_TRAY_X_L, PROC_TRAY_RIM,
    DRUM_D, DRUM_R, DRUM_H_LT,
    WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T,
    WALKWAY_BRACKET_H, WALKWAY_BRACKET_T,
)

# ── Palette (white engineering) ───────────────────────────────────────────────
BG      = "#FFFFFF"
C_OUT   = "#1A1A1A"
C_CL    = "#2060A0"
C_DIM   = "#404040"
C_ALUM  = "#C8D8E8"
C_STEEL = "#B0B0B8"
C_GASKT = "#5A3020"
C_RAIL  = "#606068"
C_CARR  = "#C04010"
C_TRAY  = "#A0B0A0"
C_SEAL  = "#4A2818"
FONT    = {"fontfamily": "monospace"}

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — Side Elevation Cross-Section
#
# View: looking along Yd axis (i.e. from near side toward far wall)
# Horizontal axis = X (container long axis, 0 = cargo door end wall inner face)
# Vertical axis   = Z (height, 0 = floor, C_HGT = ceiling)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():
    import matplotlib.patches as mpatches

    # ── Derived geometry ─────────────────────────────────────────────────────
    PANEL_T = PANEL_CENTER_T     # = 120mm (worst-case thickness for clearance)
    PANEL_H = C_HGT - PANEL_FLOOR_GAP   # panel height (ceiling to bottom edge)

    # Rail geometry
    RAIL_H     = 30     # HGR20 rail height (mm)
    RAIL_W_VIS = 20     # HGR20 rail width in this view (mm)
    CARRIAGE_H = 28     # HGH20CA carriage block height (mm)
    CARRIAGE_W = 44     # carriage block width (mm)
    BRACKET_H  = 40     # suspension bracket height (mm)
    BRACKET_W  = 60     # bracket width (mm)

    # Fixed door frame
    FRAME_W = 50        # 50×50mm RHS frame
    FRAME_H = C_HGT     # floor to ceiling

    # EPDM seal
    SEAL_W = 12
    SEAL_H = C_HGT - 30  # seal runs most of frame height

    # ── Scale: 1mm drawing = 1mm real (plot units = mm) ──────────────────────
    # The container height (2388mm) makes the drawing very tall. Widen the
    # horizontal range so the figure isn't too narrow and the title block
    # has room below the content.
    PAD_L = 350
    PAD_R = 900
    PAD_B = 500
    PAD_T = 250

    X_LO = -WALL_T - PAD_L
    X_HI = PANEL_SLIDE + PANEL_T + PAD_R
    Z_LO = -PAD_B
    Z_HI = C_HGT + PAD_T

    fig, ax = plt.subplots(figsize=(12, 18))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container structure ──────────────────────────────────────────────────
    # Floor
    ax.add_patch(Rectangle((X_LO, -20), X_HI - X_LO, 20,
                            fc="#E0DDD8", ec=C_OUT, lw=1.0, hatch="///", zorder=2))
    ax.text(0, -30, "FLOOR", ha="right", va="center",
            fontsize=6, color=C_DIM, **FONT, zorder=15)

    # Ceiling
    ax.add_patch(Rectangle((X_LO, C_HGT), X_HI - X_LO, 20,
                            fc="#E0DDD8", ec=C_OUT, lw=1.0, hatch="///", zorder=2))
    ax.text(0, C_HGT + 30, "CEILING", ha="right", va="center",
            fontsize=6, color=C_DIM, **FONT, zorder=15)

    # End wall (at X=0, extends from X=-WALL_T to X=0)
    ax.add_patch(Rectangle((-WALL_T, 0), WALL_T, C_HGT,
                            fc=C_STEEL, ec=C_OUT, lw=1.5, hatch="///", zorder=3))
    ax.text(-WALL_T / 2 - 65, C_HGT / 2, f"{WALL_T}mm\nEND\nWALL",
            ha="center", va="center", fontsize=7, color=C_STEEL,
            fontweight="bold", **FONT, zorder=15)

    # ── Fixed door frame (at X=0, 50mm RHS) ─────────────────────────────────
    ax.add_patch(Rectangle((0, 0), FRAME_W, FRAME_H,
                            fc="#D8D0C0", ec=C_OUT, lw=1.2, zorder=4))
    leader(ax, FRAME_W / 2, FRAME_H * 0.85,
           FRAME_W / 2 - 250, FRAME_H * 0.85 + 100,
           "FIXED DOOR FRAME\n50×50mm RHS\n(SEAL LANDING)", color="#806010", fs=6,
           ha="center", arrow_style="-|>", font=FONT)

    # EPDM seal strip on inner face of frame
    ax.add_patch(Rectangle((FRAME_W, 15), SEAL_W, SEAL_H,
                            fc=C_SEAL, ec=C_OUT, lw=0.6, zorder=5))
    leader(ax, FRAME_W + SEAL_W / 2, 400,
           FRAME_W + 100, 300,
           "EPDM PERIMETER\nSEAL", color=C_SEAL, fs=5.5,
           ha="center", arrow_style="-|>", font=FONT)

    # ── Ceiling-mounted HGR20 rail ──────────────────────────────────────────
    # Rail runs from X=-30 to X=PANEL_SLIDE+150 (enough travel + overhang)
    RAIL_X_START = -20
    RAIL_X_END   = PANEL_SLIDE + 180
    rail_z_top   = C_HGT
    rail_z_bot   = C_HGT - RAIL_H

    ax.add_patch(Rectangle((RAIL_X_START, rail_z_bot), RAIL_X_END - RAIL_X_START, RAIL_H,
                            fc=C_RAIL, ec=C_OUT, lw=1.2, zorder=6))
    ax.text((RAIL_X_START + RAIL_X_END) / 2, rail_z_bot + RAIL_H / 2,
            "HGR20 LINEAR RAIL", ha="center", va="center",
            fontsize=6, color="#FFFFFF", fontweight="bold", **FONT, zorder=15)

    # ── Helper: draw panel + carriage at X offset ────────────────────────────
    def draw_panel_assembly(x_off, alpha=1.0, label="", col_panel=C_ALUM):
        """Draw panel cross-section at given X offset."""
        # Carriage block (rides on rail)
        carr_x = x_off + PANEL_T / 2 - CARRIAGE_W / 2
        carr_z = rail_z_bot - CARRIAGE_H
        ax.add_patch(Rectangle((carr_x, carr_z), CARRIAGE_W, CARRIAGE_H,
                                fc=C_CARR, ec=C_OUT, lw=0.8, alpha=alpha, zorder=7))
        if alpha > 0.5:
            leader(ax, carr_x + CARRIAGE_W / 2, carr_z + CARRIAGE_H / 2,
                carr_x + CARRIAGE_W / 2 + 175, carr_z + CARRIAGE_H / 2,
                "HGH20CA", color=C_CARR, fs=5.5,
                ha="center", arrow_style="-|>", font=FONT)

        # Suspension bracket (connects carriage to panel top)
        brk_x = x_off + PANEL_T / 2 - BRACKET_W / 2
        brk_z = carr_z - BRACKET_H
        ax.add_patch(Rectangle((brk_x, brk_z), BRACKET_W, BRACKET_H,
                                fc="#A09080", ec=C_OUT, lw=0.8, alpha=alpha, zorder=7))
        if alpha > 0.5:
            leader(ax, brk_x + BRACKET_W / 2, brk_z + BRACKET_H / 2,
                brk_x + BRACKET_W / 2 + 175, brk_z + BRACKET_H / 2,
                "BRACKET", color="#A09080", fs=5.5,
                ha="center", arrow_style="-|>", font=FONT)

        # Panel body (from bracket bottom down to PANEL_FLOOR_GAP above floor)
        panel_top = brk_z
        panel_bot = PANEL_FLOOR_GAP
        panel_h = panel_top - panel_bot
        ax.add_patch(Rectangle((x_off, panel_bot), PANEL_T, panel_h,
                                fc=col_panel, ec=C_OUT, lw=1.2, alpha=alpha, zorder=5))

        if label:
            ax.text(x_off + PANEL_T / 2, (panel_top + panel_bot) / 2,
                    label, ha="center", va="center",
                    fontsize=8, color=C_OUT, fontweight="bold",
                    **FONT, alpha=alpha, zorder=15, rotation=90)

        return panel_bot

    # ── Draw OPERATIONAL position (solid, X=0) ───────────────────────────────
    op_bot = draw_panel_assembly(0, alpha=0.85, label="OPERATIONAL (X=0)")

    # ── Draw TRANSPORT position (ghost, X=PANEL_SLIDE) ───────────────────────
    tr_bot = draw_panel_assembly(PANEL_SLIDE, alpha=0.20, label="TRANSPORT (X=300)")

    # ── Processing tray on floor ─────────────────────────────────────────────
    # Show tray starting at PROC_TRAY_X_L = 170mm
    TRAY_SHOW_X = PROC_TRAY_X_L   # = 170mm
    TRAY_SHOW_W = 400              # show 400mm of tray width (extends further right)
    # Tray floor plate
    ax.add_patch(Rectangle((TRAY_SHOW_X, 0), TRAY_SHOW_W, 3,
                            fc=C_TRAY, ec=C_OUT, lw=0.8, zorder=4))
    # Left rim (50mm tall)
    ax.add_patch(Rectangle((TRAY_SHOW_X, 0), 3, PROC_TRAY_RIM,
                            fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=5))
    # Show rim extending rightward (just the top edge)
    ax.plot([TRAY_SHOW_X, TRAY_SHOW_X + TRAY_SHOW_W], [PROC_TRAY_RIM, PROC_TRAY_RIM],
            color=C_OUT, lw=0.6, ls="--", zorder=4, alpha=0.5)
    # Right edge (cut line)
    ax.plot([TRAY_SHOW_X + TRAY_SHOW_W, TRAY_SHOW_X + TRAY_SHOW_W],
            [0, PROC_TRAY_RIM + 10],
            color=C_OUT, lw=1.0, ls=(0, (1, 2)), zorder=4)
    # Break lines (zig-zag to indicate continuation)
    bx = TRAY_SHOW_X + TRAY_SHOW_W
    for z in [5, 15, 25, 35, 45]:
        ax.plot([bx - 5, bx + 5], [z - 3, z + 3], color=C_OUT, lw=0.8, zorder=5)

    leader(ax, TRAY_SHOW_X + 80, PROC_TRAY_RIM / 2,
           TRAY_SHOW_X + 75, 180,
           f"PROCESSING TRAY\n304 SS · {PROC_TRAY_RIM}mm RIM\n(PERMANENT)", color=C_TRAY, fs=6,
           ha="center", arrow_style="-|>", font=FONT)

    # ── Left walkway (removable lift-out at X=170) ──────────────────────────
    # In this side elevation, the left walkway appears as a cross-section at
    # X = PROC_TRAY_X_L = 170mm, running across the container width (Yd axis).
    # Shows: grate (Z=75-100mm) sitting on bracket support.
    # This walkway must be removed before panel slides to transport position.
    C_WALKWAY = "#707078"
    BRKT_ARM_Z = WALKWAY_H - WALKWAY_GRATE_T  # = 75mm (top of bracket arm)

    # Bracket arm cross-section (small rectangle at Z=75mm) — ghosted (removed for transport)
    WK_X = TRAY_SHOW_X   # same X as tray left edge (170mm)
    WK_SHOW_W = TRAY_SHOW_W  # show same width as tray for visual consistency
    WK_ALPHA = 0.25  # ghost — this walkway is removed before panel slides
    ax.add_patch(Rectangle((WK_X, BRKT_ARM_Z - WALKWAY_BRACKET_T),
                            WK_SHOW_W, WALKWAY_BRACKET_T,
                            fc=C_WALKWAY, ec=C_OUT, lw=0.8, ls="--",
                            alpha=WK_ALPHA, zorder=5))

    # Grate (Z=75 to 100mm) — ghosted
    ax.add_patch(Rectangle((WK_X, BRKT_ARM_Z), WK_SHOW_W, WALKWAY_GRATE_T,
                            fc="#D0D0D4", ec=C_OUT, lw=0.8, ls="--",
                            hatch="--", alpha=WK_ALPHA, zorder=5))

    # Break lines on right edge (continuation) — ghosted
    for z in [BRKT_ARM_Z - 5, BRKT_ARM_Z + 5, BRKT_ARM_Z + 15]:
        ax.plot([bx - 5, bx + 5], [z - 3, z + 3], color=C_OUT, lw=0.6,
                alpha=WK_ALPHA, zorder=6)

    leader(ax, WK_X + 200, WALKWAY_H + 5,
           WK_X + 400, WALKWAY_H + 100,
           f"LEFT WALKWAY\n{WALKWAY_GRATE_T}mm GRATE · DECK AT {WALKWAY_H}mm\n(REMOVABLE — MUST LIFT OUT\nBEFORE PANEL SLIDES)",
           color=C_WALKWAY, fs=5.5,
           ha="center", arrow_style="-|>", font=FONT)

    # Walkway deck height dimension
    draw_dim_v(ax, WK_X - 30, 0, WALKWAY_H,
              f"{WALKWAY_H}mm\nDECK", offset=15, perpendicular=True, fs=6,
              color=C_WALKWAY, right=False, font=FONT)

    # ── Clearance annotation — the key dimension ─────────────────────────────
    # Show gap between transport panel bottom and tray rim
    # Transport panel inner face is at X = PANEL_SLIDE + PANEL_T = 420mm
    # But overlap zone: tray starts at X=170, panel outer face at X=300
    # The critical clearance is VERTICAL: panel bottom (80mm) vs tray rim (50mm)

    # Dimension: floor to panel bottom (PANEL_FLOOR_GAP)
    gap_dim_x = PANEL_SLIDE + PANEL_T + 60
    draw_dim_v(ax, gap_dim_x, 0, PANEL_FLOOR_GAP,
              f"{PANEL_FLOOR_GAP}mm FLOOR GAP", offset=30, perpendicular=True, fs=7, color=C_CARR,
              right=False, font=FONT)

    # Dimension: floor to tray rim
    tray_dim_x = TRAY_SHOW_X - 40
    draw_dim_v(ax, tray_dim_x + TRAY_SHOW_W + 75, 0, PROC_TRAY_RIM,
              f"{PROC_TRAY_RIM}mm TRAY RIM", offset=90, perpendicular=True, fs=7, color=C_TRAY,
              right=True, font=FONT)

    # Clearance between tray rim top and panel bottom
    clr = PANEL_FLOOR_GAP - PROC_TRAY_RIM
    clr_x = PANEL_SLIDE + PANEL_T / 2
    draw_dim_v(ax, tray_dim_x + TRAY_SHOW_W + 75, PROC_TRAY_RIM, PANEL_FLOOR_GAP,
              f"{clr}mm CLEARANCE", offset=90, perpendicular=True, fs=7, color="#208020",
              right=True, font=FONT)

    # Green highlight of clearance zone
    ax.add_patch(Rectangle((PROC_TRAY_X_L, PROC_TRAY_RIM),
                            PANEL_SLIDE + PANEL_T - PROC_TRAY_X_L + 20,
                            clr,
                            fc="#20C020", ec="none", alpha=0.10, zorder=2))

    # ── Slide arrow ──────────────────────────────────────────────────────────
    arr_z = C_HGT / 2
    ax.annotate("", xy=(PANEL_SLIDE + PANEL_T / 2, arr_z),
                xytext=(PANEL_T / 2, arr_z),
                arrowprops=dict(arrowstyle="->,head_length=0.6,head_width=0.4",
                                color=C_CARR, lw=2.5,
                                connectionstyle="arc3,rad=0.15",
                                mutation_scale=14), zorder=15)
    ax.text((PANEL_T / 2 + PANEL_SLIDE + PANEL_T / 2) / 2, arr_z + 80,
            f"SLIDE {PANEL_SLIDE}mm\n(TRANSPORT MODE)",
            ha="center", va="bottom", fontsize=8, color=C_CARR,
            fontweight="bold", **FONT, zorder=15)

    # ── Container height dimension ───────────────────────────────────────────
    draw_dim_v(ax, X_HI - 80, 0, C_HGT,
              f"{C_HGT}mm INTERIOR HEIGHT", offset=15, fs=7,
              right=False, font=FONT)

    # ── Panel height dimension ───────────────────────────────────────────────
    panel_top_z = C_HGT - RAIL_H - CARRIAGE_H - BRACKET_H
    draw_dim_v(ax, -WALL_T - 80, PANEL_FLOOR_GAP, panel_top_z,
              f"{int(panel_top_z - PANEL_FLOOR_GAP)}mm PANEL HEIGHT", offset=15, fs=6.5,
              right=False, font=FONT)

    # ── Zone labels ──────────────────────────────────────────────────────────
    ax.text(-WALL_T / 2, Z_LO + 40, "EXTERIOR",
            ha="center", va="bottom", fontsize=7, color="#806050",
            fontweight="bold", **FONT, zorder=15, alpha=0.6)
    ax.text(X_HI / 2, Z_HI /2, "INTERIOR (DARKROOM)",
            ha="center", va="top", fontsize=7, color="#205020",
            fontweight="bold", **FONT, zorder=15, alpha=0.6)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        "NOTES:",
        f"1. Panel suspended from HGR20 ceiling rail — bottom edge {PANEL_FLOOR_GAP}mm above floor.",
        f"2. Processing tray rim = {PROC_TRAY_RIM}mm. Clearance above rim = {clr}mm (panel clears in transport).",
        f"3. EPDM perimeter seal engages fixed door frame when panel at X=0 (operational).",
        f"4. Seal NOT engaged during transport — light seal not required for loading/transport.",
        f"5. Panel slide travel = {PANEL_SLIDE}mm on 2× HGR20 rails (ceiling-mounted, near/far walls).",
        f"6. Left walkway (deck at {WALKWAY_H}mm) must be lifted out before panel slides to transport.",
    ]
    draw_notes(ax, notes, X_LO + 30, Z_LO + 30 + (len(notes) - 1) * 22,
               spacing=22, fs=5.5, title_fs=5.5, color=C_DIM,
               title_color=C_DIM, font=FONT,
               width=(X_HI - X_LO) * 0.95)

    # ── Legend ────────────────────────────────────────────────────────────────
    legend_x = X_HI - 240
    legend_top = Z_HI - 50
    swatches = [
        (C_ALUM,  0.85, "Panel (operational)"),
        (C_ALUM,  0.20, "Panel (transport)"),
        (C_RAIL,  1.0,  "HGR20 rail"),
        (C_CARR,  1.0,  "Carriage block"),
        (C_TRAY,  1.0,  "Processing tray"),
        ("#D0D0D4", 0.25, "Walkway grate (removed)"),
        (C_SEAL,  1.0,  "EPDM seal"),
    ]
    for i, (c, a, lbl) in enumerate(swatches):
        sy = legend_top - i * 28
        ax.add_patch(Rectangle((legend_x, sy - 7), 18, 14,
                                fc=c, ec=C_OUT, lw=0.6, alpha=a, zorder=15))
        ax.text(legend_x + 25, sy, lbl,
                ha="left", va="center", fontsize=5.5, color=C_DIM,
                **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 2",
                drawing_title="CEILING RAIL SUSPENSION SYSTEM",
                subtitle="SIDE ELEVATION — CEILING RAIL SUSPENSION",
                scale_note="EQUAL ASPECT · ALL DIMS IN mm · VIEW LOOKING ALONG Yd AXIS (NEAR → FAR)",
                portrait=True, height=0.055)

    fig.savefig("diagrams/ceiling-rail-sheet1.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/ceiling-rail-sheet1.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ceiling-rail-sheet1.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Rail/Carriage Detail View
#
# Close-up of the HGR20/HGH20CA interface, suspension bracket, and panel top.
# Scale approximately 2:1 for clarity.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():
    import matplotlib.patches as mpatches

    # ── Component dimensions (mm, real) ──────────────────────────────────────
    RAIL_H     = 30     # HGR20 profile height
    RAIL_W     = 20     # HGR20 profile width (narrow axis in this view)
    CARRIAGE_H = 28     # HGH20CA block height
    CARRIAGE_W = 44     # block width
    BOLT_D     = 8      # M8 mounting bolts
    BRACKET_H  = 40     # suspension bracket (10mm plate, folded)
    BRACKET_W  = 60     # bracket width
    PANEL_TOP_T = PANEL_CENTER_T  # = 120mm

    # ── Scale 2:1 — drawing units are mm×2 ──────────────────────────────────
    S = 2.0  # scale factor

    # Layout: ceiling at top, panel at bottom
    # Show from ceiling surface down through rail, carriage, bracket, panel top
    CEIL_Z = 0  # ceiling surface reference (top of drawing)

    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    # Drawing extents — extra width on left for component list
    W_RANGE = 200  # mm real, centered on 0
    H_RANGE = 250  # mm real, from ceiling down

    def sx(mm): return mm * S
    def sy(mm): return mm * S

    ax.set_xlim(-W_RANGE * S * 1.6, W_RANGE * S / 2)
    ax.set_ylim(-H_RANGE * S - sy(30), 20 * S)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Ceiling structure (hatched, at Z=0) ──────────────────────────────────
    ceil_w = sx(W_RANGE)
    ceil_h = sy(15)
    ax.add_patch(Rectangle((-ceil_w / 2, 0), ceil_w, ceil_h,
                            fc="#E0DDD8", ec=C_OUT, lw=1.5, hatch="///", zorder=2))
    ax.text(0, sy(7.5), "CONTAINER CEILING (1.6mm CORTEN STEEL)",
            ha="center", va="center", fontsize=7, color=C_DIM,
            fontweight="bold", **FONT, zorder=15)

    # ── Mounting plate (welded to ceiling) ───────────────────────────────────
    plate_w = sx(80)
    plate_h = sy(6)
    plate_z = -plate_h
    ax.add_patch(Rectangle((-plate_w / 2, plate_z), plate_w, plate_h,
                            fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=3))
    leader(ax, sx(4), plate_z + plate_h / 2,
           sx(55), plate_z - plate_h / 2 - sy(25),
           "6mm MOUNTING PLATE\n(WELDED TO CEILING)", color=C_DIM, fs=6,
           ha="center", arrow_style="-|>", font=FONT)

    # ── HGR20 rail profile ───────────────────────────────────────────────────
    rail_w = sx(RAIL_W)
    rail_h = sy(RAIL_H)
    rail_z = plate_z - rail_h
    ax.add_patch(Rectangle((-rail_w / 2, rail_z), rail_w, rail_h,
                            fc=C_RAIL, ec=C_OUT, lw=1.5, zorder=4))
    # Rail profile detail — T-shape grooves (simplified)
    groove_w = sx(3)
    for side in [-1, 1]:
        gx = side * (rail_w / 2 - groove_w / 2)
        ax.add_patch(Rectangle((gx - groove_w / 2, rail_z + sy(8)),
                                groove_w, sy(14),
                                fc="#404048", ec=C_OUT, lw=0.5, zorder=5))
    ax.text(0, rail_z + rail_h / 2, "HGR20",
            ha="center", va="center", fontsize=8, color="#FFFFFF",
            fontweight="bold", **FONT, zorder=15)

    # Mounting bolts (M8, through plate into ceiling)
    for bx in [-sx(25), sx(25)]:
        ax.add_patch(Circle((bx, plate_z + plate_h / 2), sx(BOLT_D / 2),
                            fc="#303030", ec=C_OUT, lw=0.8, zorder=6))

    # ── HGH20CA carriage block ───────────────────────────────────────────────
    carr_w = sx(CARRIAGE_W)
    carr_h = sy(CARRIAGE_H)
    carr_z = rail_z - carr_h - sy(2)  # 2mm gap for ball bearings
    ax.add_patch(Rectangle((-carr_w / 2, carr_z), carr_w, carr_h,
                            fc=C_CARR, ec=C_OUT, lw=1.5, zorder=4))
    ax.text(0, carr_z + carr_h / 2, "HGH20CA\nCARRIAGE",
            ha="center", va="center", fontsize=7, color="#FFFFFF",
            fontweight="bold", **FONT, zorder=15)

    # Ball bearing indication (small circles in gap)
    gap_z = rail_z - sy(1)
    for bx in np.linspace(-rail_w / 2 + sx(3), rail_w / 2 - sx(3), 5):
        ax.add_patch(Circle((bx, gap_z), sx(1.2),
                            fc="#808088", ec=C_OUT, lw=0.4, zorder=6))

    # ── Suspension bracket ───────────────────────────────────────────────────
    brk_w = sx(BRACKET_W)
    brk_h = sy(BRACKET_H)
    brk_z = carr_z - brk_h
    # Draw as an inverted U-shape bracket
    brk_plate = sy(10)
    # Top plate (bolted to carriage)
    ax.add_patch(Rectangle((-brk_w / 2, carr_z - brk_plate),
                            brk_w, brk_plate,
                            fc="#A09080", ec=C_OUT, lw=1.0, zorder=4))
    # Side plates (vertical, connecting to panel)
    side_w = sx(8)
    side_h = brk_h - brk_plate
    for side in [-1, 1]:
        sx_pos = side * (brk_w / 2 - side_w)
        ax.add_patch(Rectangle((sx_pos, brk_z), side_w, side_h,
                                fc="#A09080", ec=C_OUT, lw=1.0, zorder=4))
    # Bracket label
    ax.text(5, brk_z + brk_h / 2,
            "SUSPENSION\nBRACKET\n(10mm MILD STEEL)",
            ha="center", va="center", fontsize=5.5, color=C_OUT,
            **FONT, zorder=15)

    # Carriage bolts
    for bx in [-sx(14), sx(14)]:
        ax.add_patch(Circle((bx, carr_z - brk_plate / 2), sx(3),
                            fc="#303030", ec=C_OUT, lw=0.6, zorder=6))

    # ── Panel top (cross-section) ────────────────────────────────────────────
    panel_w = sx(PANEL_TOP_T)
    panel_vis_h = sy(80)  # show top 80mm of panel
    panel_z = brk_z - sy(5)  # small gap for bolt clearance
    ax.add_patch(Rectangle((-panel_w / 2, panel_z - panel_vis_h),
                            panel_w, panel_vis_h,
                            fc=C_ALUM, ec=C_OUT, lw=1.5, zorder=3))
    # Panel internal structure indication
    ply_w = sx(18)
    ax.add_patch(Rectangle((-panel_w / 2, panel_z - panel_vis_h),
                            ply_w, panel_vis_h,
                            fc="#D8C8A8", ec=C_OUT, lw=0.5, zorder=4, alpha=0.7))
    ax.add_patch(Rectangle((panel_w / 2 - ply_w, panel_z - panel_vis_h),
                            ply_w, panel_vis_h,
                            fc="#D8C8A8", ec=C_OUT, lw=0.5, zorder=4, alpha=0.7))
    ax.text(0, panel_z - panel_vis_h / 2,
            f"{PANEL_CENTER_T}mm\nPANEL\n(CENTER ZONE)",
            ha="center", va="center", fontsize=6.5, color=C_OUT,
            fontweight="bold", **FONT, zorder=15)
    # PLY labels
    ax.text(-panel_w / 2 + ply_w / 2, panel_z - panel_vis_h + sy(12),
            "18mm\nPLY", ha="center", va="bottom", fontsize=5, color=C_DIM,
            **FONT, zorder=15)

    # Panel bolt connection to bracket side plates
    bolt_z = panel_z - sy(15)
    for side in [-1, 1]:
        bx = side * (brk_w / 2 - side_w / 2)
        ax.add_patch(Circle((bx, bolt_z), sx(3),
                            fc="#303030", ec=C_OUT, lw=0.6, zorder=6))

    # ── Break line at panel bottom (indicating continuation) ─────────────────
    break_z = panel_z - panel_vis_h
    pts = []
    for x in np.linspace(-panel_w / 2, panel_w / 2, 20):
        offset = sy(3) * (1 if int((x + panel_w / 2) / sx(12)) % 2 == 0 else -1)
        pts.append([x, break_z + offset])
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=C_OUT, lw=1.5, zorder=10)

    # ── Dimension lines ──────────────────────────────────────────────────────
    # Rail height
    draw_dim_v(ax, sx(W_RANGE / 2 - 20), rail_z, rail_z + rail_h,
              f"{RAIL_H}mm", offset=sx(5), fs=7, right=True, font=FONT)
    # Carriage height
    draw_dim_v(ax, sx(W_RANGE / 2 - 20), carr_z, carr_z + carr_h,
              f"{CARRIAGE_H}mm", offset=sx(5), fs=7, right=True, font=FONT)
    # Bracket height
    draw_dim_v(ax, -sx(W_RANGE / 2 - 20), brk_z, carr_z - brk_plate,
              f"{BRACKET_H}mm", offset=sx(5), fs=7, right=True, font=FONT)
    # Panel width (thickness)
    draw_dim_h(ax, -panel_w / 2, panel_w / 2, panel_z - panel_vis_h - sy(15),
              f"{PANEL_CENTER_T}mm PANEL THICKNESS", offset=sy(5), fs=7,
              above=False, font=FONT)
    # Total assembly depth (ceiling to panel top)
    total_depth = 15 + 6 + RAIL_H + 2 + CARRIAGE_H + BRACKET_H + 5  # = ~161mm
    draw_dim_v(ax, -sx(W_RANGE / 2 - 5), panel_z, 0,
              f"~{total_depth}mm TOTAL SUSPENSION DEPTH", offset=sx(5), fs=6.5,
              right=False, font=FONT)

    # ── Component list (far left, compact) ──────────────────────────────────
    comp_x = -sx(W_RANGE * 1.5)
    comp_top = sy(5)
    LINE_H = sy(6)   # tighter line spacing

    comp_lines = [
        "COMPONENT LIST (PER RAIL):",
        "1× HGR20 rail, 500mm length",
        "2× HGH20CA carriage blocks",
        "2× Suspension brackets (10mm MS)",
        "4× M8×30 hex bolts (rail→plate)",
        "4× M8×25 hex bolts (carriage→bracket)",
        "4× M10×35 hex bolts (bracket→panel)",
        "1× 6mm mounting plate (welded)",
    ]
    draw_notes(ax, comp_lines, comp_x, comp_top, spacing=LINE_H,
               fs=5, title_fs=5.5, color=C_DIM, title_color=C_OUT,
               font=FONT, width=sx(W_RANGE * 0.4))

    note_lines = [
        "NOTES:",
        f"1. 2 rails total (near + far wall)",
        f"2. Load rating: 12.7 kN per block",
        f"3. Panel mass ≈ 180 kg (4 blocks)",
        f"4. Safety factor > 10×",
    ]
    notes_top = comp_top - len(comp_lines) * LINE_H
    draw_notes(ax, note_lines, comp_x, notes_top, spacing=LINE_H,
               fs=5, title_fs=5.5, color=C_DIM, title_color=C_OUT,
               font=FONT, width=sx(W_RANGE * 0.4))

    # ── Scale note ───────────────────────────────────────────────────────────
    ax.text(0, -sy(H_RANGE) + sy(10),
            "SCALE ≈ 2:1  ·  DETAIL VIEW  ·  SECTION THROUGH CENTER ZONE",
            ha="center", va="bottom", fontsize=7, color=C_DIM,
            **FONT, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 2",
                drawing_title="CEILING RAIL SUSPENSION SYSTEM",
                subtitle="DETAIL — RAIL / CARRIAGE / BRACKET ASSEMBLY",
                scale_note="APPROX 2:1 · ALL DIMS IN mm · SECTION THROUGH Yd CENTER ZONE")

    fig.savefig("diagrams/ceiling-rail-sheet2.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path("diagrams/ceiling-rail-sheet2.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ceiling-rail-sheet2.png saved")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs("diagrams", exist_ok=True)
    os.makedirs(SVG_DIR, exist_ok=True)
    print("Generating ceiling rail suspension system diagrams...")
    sheet1()
    sheet2()
    print("Done.")
