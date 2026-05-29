#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_power_panel_diagram.py — TBS-001 External Power Panel

Sheet 1 — Detail drawing of the flush-mount combined solar + shore power
input panel and cooler DC output on the pinhole wall.  Three views:

  A  Front elevation (panel face, ~2:1 scale)
  B  Cross-section through wall (flush-mount detail)
  C  Simplified wiring schematic
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

from tbs_constants import (
    PWR_PANEL_W, PWR_PANEL_H, PWR_PANEL_D,
    PWR_PANEL_CUTOUT_W, PWR_PANEL_CUTOUT_H,
    DIAGRAMS_DIR, SVG_DIR, svg_path,
)
from tbs_title_block import title_block
from tbs_drawing import (draw_dim_h, draw_dim_v, leader, draw_rect,
                         draw_circle, hatch_rect)

# ── Palette ──────────────────────────────────────────────────────────────────
C_OUT   = "#1A1A1A"
C_DIM   = "#404040"
C_CL    = "#2060A0"
C_STEEL = "#B0B0B8"
C_ALUM  = "#C8D8E8"
C_BOX   = "#E8E0C8"      # panel face plate fill
C_NEMA  = "#FFF0CC"       # NEMA inlet fill
C_MC4   = "#2D7A2D"       # MC4 connector color (solar green)
C_AC    = "#A07820"       # AC shore power color
C_WALL  = "#C0C0C8"       # container wall
C_GASKT = "#5A3020"       # gasket / neoprene
C_INT   = "#F0FFF0"       # interior zone
FONT    = {"fontfamily": "monospace"}

# ── Panel dimensions (mm) ───────────────────────────────────────────────────
PLATE_W  = PWR_PANEL_W         # 300mm face plate
PLATE_H  = PWR_PANEL_H         # 200mm face plate
PLATE_T  = PWR_PANEL_D         # 3mm aluminum plate thickness
CUT_W    = PWR_PANEL_CUTOUT_W  # 280mm wall cutout
CUT_H    = PWR_PANEL_CUTOUT_H  # 180mm wall cutout
WALL_T   = 3                   # container wall thickness (corrugated steel)
GASKET_T = 3                   # neoprene gasket thickness
MOUNT_HOLE_D = 6               # mounting bolt hole diameter
MOUNT_INSET  = 15              # mounting hole inset from plate edge

# MC4 connector layout
MC4_R    = 8              # MC4 bulkhead connector radius
MC4_X    = 70             # MC4 column X from panel left edge
MC4_GAP  = 25             # gap between + and - in a pair
MC4_PITCH = 55            # vertical pitch between pairs
MC4_DEPTH = 40            # MC4 bulkhead protrusion behind plate (mm)

# NEMA inlet
NEMA_W   = 55             # NEMA receptacle width
NEMA_H   = 45             # NEMA receptacle height
NEMA_X   = 195            # NEMA left edge from panel left edge
NEMA_Y   = 77             # NEMA bottom edge from panel bottom edge
NEMA_DEPTH = 45           # NEMA body protrusion behind plate (mm)

# Deutsch DT 2-pin bulkhead (Circuit E — evap cooler DC output)
DT_R     = 10             # connector body radius (mm)
DT_X     = 230            # center X from panel left edge
DT_Y     = 35             # center Y from panel bottom edge
DT_DEPTH = 30             # body protrusion behind plate (mm)
C_DT     = "#E8884A"      # orange — matches pump/cooler circuit color


def draw_sheet1():
    fig = plt.figure(figsize=(22, 15))
    fig.patch.set_facecolor("white")

    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1], height_ratios=[3, 1.2],
                          hspace=0.25, wspace=0.3,
                          left=0.05, right=0.95, top=0.92, bottom=0.08)

    # ═════════════════════════════════════════════════════════════════════════
    # VIEW A — Front Elevation (panel face, exterior view)
    # ═════════════════════════════════════════════════════════════════════════
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.set_aspect("equal")
    ax_a.axis("off")

    def sx(mm): return mm
    def sy(mm): return mm

    pad = 80
    ax_a.set_xlim(sx(-pad), sx(PLATE_W + pad))
    ax_a.set_ylim(sy(-pad), sy(PLATE_H + pad))

    # Face plate outline (aluminum, flat — no rounded box since it's a plate)
    draw_rect(ax_a, sx(0), sy(0), sx(PLATE_W), sy(PLATE_H),
              fc=C_ALUM, color=C_OUT, lw=2.0, zorder=3)

    # Wall cutout visible behind plate (dashed, centered)
    cut_off_x = (PLATE_W - CUT_W) / 2
    cut_off_y = (PLATE_H - CUT_H) / 2
    ax_a.add_patch(mpatches.Rectangle(
        (sx(cut_off_x), sy(cut_off_y)), sx(CUT_W), sy(CUT_H),
        fc="none", ec=C_DIM, lw=1.0, ls="--", zorder=4))
    ax_a.text(sx(PLATE_W - cut_off_x - 5), sy(cut_off_y + 5),
              "WALL CUTOUT\n(HIDDEN)", ha="right", va="bottom",
              fontsize=5.5, color=C_DIM, style="italic", **FONT, zorder=4)

    # Mounting holes (4 corners)
    for mx, my in [(MOUNT_INSET, MOUNT_INSET),
                   (PLATE_W - MOUNT_INSET, MOUNT_INSET),
                   (MOUNT_INSET, PLATE_H - MOUNT_INSET),
                   (PLATE_W - MOUNT_INSET, PLATE_H - MOUNT_INSET)]:
        draw_circle(ax_a, sx(mx), sy(my), sx(MOUNT_HOLE_D / 2),
                     lw=0.8, color=C_DIM, zorder=5)

    # MC4 bulkhead connectors — 3 pairs on left side
    mc4_y_base = PLATE_H / 2 - MC4_PITCH
    for i in range(3):
        cy = mc4_y_base + i * MC4_PITCH
        cx_pos = MC4_X - MC4_GAP / 2
        draw_circle(ax_a, sx(cx_pos), sy(cy), sx(MC4_R),
                     lw=1.5, color=C_MC4, fill=True, fc="#C0E8C0", zorder=5)
        ax_a.text(sx(cx_pos), sy(cy), "+", ha="center", va="center",
                  fontsize=8, fontweight="bold", color=C_MC4, zorder=6)
        cx_neg = MC4_X + MC4_GAP / 2
        draw_circle(ax_a, sx(cx_neg), sy(cy), sx(MC4_R),
                     lw=1.5, color=C_MC4, fill=True, fc="#E0E0E0", zorder=5)
        ax_a.text(sx(cx_neg), sy(cy), "−", ha="center", va="center",
                  fontsize=8, fontweight="bold", color=C_DIM, zorder=6)
        ax_a.text(sx(MC4_X + MC4_GAP / 2 + MC4_R + 8), sy(cy),
                  f"PV{i + 1}", ha="left", va="center",
                  fontsize=7, color=C_MC4, fontweight="bold", **FONT, zorder=6)

    # NEMA 5-15R inlet — right side
    nema_cx = NEMA_X + NEMA_W / 2
    nema_cy = NEMA_Y + NEMA_H / 2
    ax_a.add_patch(mpatches.FancyBboxPatch(
        (sx(NEMA_X), sy(NEMA_Y)), sx(NEMA_W), sy(NEMA_H),
        boxstyle="round,pad=3", fc=C_NEMA, ec=C_OUT, lw=1.5, zorder=5))
    slot_w, slot_h = 4, 14
    slot_gap = 18
    for dx in [-slot_gap / 2, slot_gap / 2]:
        ax_a.add_patch(mpatches.Rectangle(
            (sx(nema_cx + dx - slot_w / 2), sy(nema_cy + 2)),
            sx(slot_w), sy(slot_h),
            fc="white", ec=C_OUT, lw=1.0, zorder=6))
    ground_r = 5
    theta = np.linspace(np.pi, 2 * np.pi, 20)
    gx = sx(nema_cx) + sx(ground_r) * np.cos(theta)
    gy = sy(nema_cy - 6) + sx(ground_r) * np.sin(theta)
    ax_a.plot(gx, gy, color=C_OUT, lw=1.0, zorder=6)

    # Deutsch DT 2-pin bulkhead — Circuit E (evap cooler DC output)
    draw_circle(ax_a, sx(DT_X), sy(DT_Y), sx(DT_R),
                 lw=1.5, color=C_DT, fill=True, fc="#FFE0C0", zorder=5)
    ax_a.text(sx(DT_X), sy(DT_Y), "E", ha="center", va="center",
              fontsize=7, fontweight="bold", color=C_DT, zorder=6)

    # Title
    ax_a.text(sx(PLATE_W / 2), sy(PLATE_H + 55),
              "VIEW A — FRONT ELEVATION (EXTERIOR FACE)",
              ha="center", va="bottom", fontsize=9, fontweight="bold",
              color=C_OUT, **FONT)

    # Dimensions
    draw_dim_h(ax_a, sx(0), sx(PLATE_W), sy(-30),
               f"{PLATE_W}mm", offset=sy(8), fs=7, above=False, font=FONT)
    draw_dim_v(ax_a, sx(-30), sy(0), sy(PLATE_H),
               f"{PLATE_H}mm", offset=sx(8), fs=7, font=FONT)

    # Leaders
    leader(ax_a, sx(MC4_X), sy(mc4_y_base + 2 * MC4_PITCH + MC4_R + 5),
           sx(MC4_X - 25), sy(PLATE_H + 35),
           "MC4 BULKHEAD\nCONNECTORS (×3 PAIRS)\nIP67 PANEL-MOUNT",
           fs=6.5, color=C_MC4, ha="center", arrow_style="-|>", font=FONT)

    leader(ax_a, sx(NEMA_X + NEMA_W + 5), sy(NEMA_Y + NEMA_H / 2),
           sx(nema_cx + NEMA_W * 3), sy(NEMA_Y - 10),
           "NEMA 5-15R\nWEATHERPROOF INLET\n120V AC SHORE POWER",
           fs=6.5, color=C_AC, ha="center", va="top", arrow_style="-|>", font=FONT)

    leader(ax_a, sx(DT_X + DT_R + 3), sy(DT_Y),
           sx(PLATE_W + 25), sy(DT_Y - 15),
           "DEUTSCH DT 2-PIN\nBULKHEAD (IP67)\nCIRCUIT E — COOLER",
           fs=6, color=C_DT, ha="left", arrow_style="-|>", font=FONT)

    leader(ax_a, sx(PLATE_W - MOUNT_INSET + MOUNT_HOLE_D),
           sy(PLATE_H - MOUNT_INSET),
           sx(PLATE_W + 25), sy(PLATE_H + 30),
           f"M{MOUNT_HOLE_D} MOUNTING\nBOLTS (×4)",
           fs=6, color=C_DIM, arrow_style="-|>", font=FONT)

    # ═════════════════════════════════════════════════════════════════════════
    # VIEW B — Cross-Section Through Wall (flush-mount detail)
    # ═════════════════════════════════════════════════════════════════════════
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.set_aspect("equal")
    ax_b.axis("off")

    # Depth axis values are intentionally exaggerated for readability
    def bx(mm): return mm
    def by(mm): return mm

    # All vertical dimensions use a consistent mm_unit so that the plate
    # (3mm thick on depth axis), bolts (M6 = 6mm shaft), cutout (180mm),
    # and plate height (200mm) are all proportionally correct.
    #
    # Depth axis (horizontal) is exaggerated for readability:
    #   plate_t_draw and wall_thick are NOT to the same scale as height.

    wall_x = 100          # wall exterior face X position
    wall_thick = 40       # exaggerated wall thickness (depth axis)
    plate_t_draw = 12     # exaggerated plate thickness (depth axis)
    gasket_t_draw = 6     # exaggerated gasket thickness (depth axis)
    conn_depth = 50       # connector body protrusion (depth axis)

    # Vertical scale: 1 mm_v = real mm in the height direction
    mm_v = 0.7            # drawing units per real mm (height axis)

    # Derived vertical positions from real dimensions
    plate_h_draw = PLATE_H * mm_v         # 200mm plate height
    cut_h_draw = CUT_H * mm_v             # 180mm cutout height
    plate_bot = 0                          # plate bottom edge
    plate_top = plate_h_draw               # plate top edge
    cut_bot = (plate_h_draw - cut_h_draw) / 2   # cutout centered in plate
    cut_top = cut_bot + cut_h_draw
    mount_inset_draw = MOUNT_INSET * mm_v  # 15mm bolt inset from plate edge

    # Bolt positions (15mm from plate edge = well within plate)
    bolt_positions = [plate_bot + mount_inset_draw,
                      plate_top - mount_inset_draw]

    # Bolt dimensions (proportional to plate via mm_v)
    bolt_shaft_h = 6 * mm_v      # M6 = 6mm diameter
    bolt_head_w = 4 * mm_v * (plate_t_draw / (3 * mm_v))  # depth-axis exaggerated
    bolt_head_h = 10 * mm_v      # 10mm across-flats
    nut_w = 5 * mm_v * (plate_t_draw / (3 * mm_v))        # depth-axis exaggerated
    nut_h = 10 * mm_v            # 10mm across-flats

    sec_h = plate_h_draw
    ext_pad = 80
    int_pad = 180
    ax_b.set_xlim(bx(-ext_pad), bx(wall_x + wall_thick + int_pad))
    ax_b.set_ylim(by(-40), by(sec_h + 80))

    # Interior zone fill
    ax_b.add_patch(mpatches.Rectangle(
        (bx(wall_x + wall_thick), by(-20)), bx(int_pad), by(sec_h + 80),
        fc=C_INT, ec="none", alpha=0.3, zorder=1))

    # Container wall — top section (above cutout)
    hatch_rect(ax_b, bx(wall_x), by(cut_top), bx(wall_thick),
               by(sec_h - cut_top + 20),
               color=C_WALL, edgecolor=C_OUT, lw=1.5, alpha=1.0, zorder=3)
    # Container wall — bottom section (below cutout)
    hatch_rect(ax_b, bx(wall_x), by(-20), bx(wall_thick),
               by(cut_bot + 20),
               color=C_WALL, edgecolor=C_OUT, lw=1.5, alpha=1.0, zorder=3)

    # Cutout opening (clear)
    draw_rect(ax_b, bx(wall_x), by(cut_bot), bx(wall_thick),
              by(cut_h_draw),
              fc="white", color=C_OUT, lw=1.0, zorder=2)

    # Gasket (between plate and wall exterior face, around cutout perimeter)
    gasket_x = wall_x - gasket_t_draw
    gasket_strip_h = (plate_h_draw - cut_h_draw) / 2 + 3 * mm_v  # overlap cutout edge
    # Top gasket strip
    draw_rect(ax_b, bx(gasket_x), by(cut_top - 3 * mm_v),
              bx(gasket_t_draw), by(gasket_strip_h),
              fc=C_GASKT, color=C_GASKT, lw=0.8, zorder=5)
    # Bottom gasket strip
    draw_rect(ax_b, bx(gasket_x), by(cut_bot - (gasket_strip_h - 3 * mm_v)),
              bx(gasket_t_draw), by(gasket_strip_h),
              fc=C_GASKT, color=C_GASKT, lw=0.8, zorder=5)

    # Face plate (flush with exterior wall face)
    plate_x = gasket_x - plate_t_draw
    draw_rect(ax_b, bx(plate_x), by(plate_bot), bx(plate_t_draw),
              by(plate_h_draw),
              fc=C_ALUM, color=C_OUT, lw=1.5, zorder=6)

    # Connector bodies protruding through cutout into interior
    mc4_spacing = cut_h_draw / 4
    for i in range(3):
        cy = cut_bot + mc4_spacing * (i + 0.5)
        draw_rect(ax_b, bx(wall_x - 5), by(cy - 4 * mm_v),
                  bx(wall_thick + conn_depth + 5), by(8 * mm_v),
                  fc="#C0E8C0", color=C_MC4, lw=1.0, zorder=4)
        ax_b.plot([bx(wall_x + wall_thick + conn_depth),
                   bx(wall_x + wall_thick + int_pad - 30)],
                  [by(cy), by(cy)],
                  color=C_MC4, lw=1.5, zorder=5)

    # NEMA body through cutout
    nema_cy = cut_bot + mc4_spacing * 3.2
    draw_rect(ax_b, bx(wall_x - 5), by(nema_cy - 5 * mm_v),
              bx(wall_thick + conn_depth + 5), by(10 * mm_v),
              fc=C_NEMA, color=C_AC, lw=1.0, zorder=4)
    ax_b.plot([bx(wall_x + wall_thick + conn_depth),
               bx(wall_x + wall_thick + int_pad - 30)],
              [by(nema_cy), by(nema_cy)],
              color=C_AC, lw=1.5, ls="--", zorder=5)

    # Deutsch DT body through cutout (Circuit E — cooler DC output)
    dt_cy = cut_bot + 6 * mm_v
    draw_rect(ax_b, bx(wall_x - 5), by(dt_cy - 3 * mm_v),
              bx(wall_thick + DT_DEPTH + 5), by(6 * mm_v),
              fc="#FFE0C0", color=C_DT, lw=1.0, zorder=4)
    ax_b.plot([bx(wall_x + wall_thick + DT_DEPTH),
               bx(wall_x + wall_thick + int_pad - 30)],
              [by(dt_cy), by(dt_cy)],
              color=C_DT, lw=1.5, zorder=5)
    ax_b.plot([bx(wall_x - 5), bx(-ext_pad + 10)],
              [by(dt_cy), by(dt_cy)],
              color=C_DT, lw=1.5, ls="--", zorder=5)

    # Mounting bolts (through plate + gasket + wall, nut clamped against wall)
    washer_w = 1.5 * mm_v * (plate_t_draw / (3 * mm_v))  # washer thickness
    washer_h = 12 * mm_v     # washer OD ~12mm
    for by_pos in bolt_positions:
        # Bolt shaft — from bolt head through plate, gasket, wall to nut
        shaft_start = plate_x - bolt_head_w
        shaft_end = wall_x + wall_thick + washer_w + nut_w
        draw_rect(ax_b, bx(shaft_start),
                  by(by_pos - bolt_shaft_h / 2),
                  bx(shaft_end - shaft_start),
                  by(bolt_shaft_h),
                  fc=C_STEEL, color=C_OUT, lw=0.6, zorder=7)
        # Bolt head (exterior side of plate)
        draw_rect(ax_b, bx(plate_x - bolt_head_w),
                  by(by_pos - bolt_head_h / 2),
                  bx(bolt_head_w), by(bolt_head_h),
                  fc=C_STEEL, color=C_OUT, lw=0.8, zorder=8)
        # Washer (against interior face of wall)
        draw_rect(ax_b, bx(wall_x + wall_thick),
                  by(by_pos - washer_h / 2),
                  bx(washer_w), by(washer_h),
                  fc="#E0E0E0", color=C_OUT, lw=0.6, zorder=8)
        # Nut (clamped against washer, flush with interior wall face)
        draw_rect(ax_b, bx(wall_x + wall_thick + washer_w),
                  by(by_pos - nut_h / 2),
                  bx(nut_w), by(nut_h),
                  fc=C_STEEL, color=C_OUT, lw=0.8, zorder=8)

    # Interior destination labels
    int_label_x = wall_x + wall_thick + int_pad - 25
    ax_b.text(bx(int_label_x), by(cut_bot + mc4_spacing + 16),
              "→ MPPT", ha="left", va="center", fontsize=7,
              color=C_MC4, fontweight="bold", **FONT, zorder=7)
    ax_b.text(bx(int_label_x), by(nema_cy),
              "→ CHARGER", ha="left", va="center", fontsize=7,
              color=C_AC, fontweight="bold", **FONT, zorder=7)
    ax_b.text(bx(int_label_x), by(dt_cy),
              "← CCT E", ha="left", va="center", fontsize=7,
              color=C_DT, fontweight="bold", **FONT, zorder=7)
    ax_b.text(bx(-ext_pad + 8), by(dt_cy + 5),
              "→ COOLER", ha="left", va="bottom", fontsize=7,
              color=C_DT, fontweight="bold", **FONT, zorder=7)

    # Zone labels
    ax_b.text(bx(plate_x - 30), by(sec_h + 55),
              "EXTERIOR", ha="center", va="bottom", fontsize=9,
              fontweight="bold", color=C_DIM, **FONT)
    ax_b.text(bx(wall_x + wall_thick + int_pad / 2), by(sec_h + 55),
              "INTERIOR", ha="center", va="bottom", fontsize=9,
              fontweight="bold", color=C_DIM, **FONT)

    # Title
    ax_b.text(bx((wall_x + wall_thick + int_pad) / 2), by(sec_h + 70),
              "VIEW B — CROSS-SECTION (FLUSH-MOUNT DETAIL)",
              ha="center", va="bottom", fontsize=9, fontweight="bold",
              color=C_OUT, **FONT)

    # Dimensions
    draw_dim_h(ax_b, bx(plate_x), bx(plate_x + plate_t_draw), by(-25),
               f"{PLATE_T}mm\nPLATE", offset=by(5), fs=6, above=False, font=FONT)
    draw_dim_h(ax_b, bx(wall_x), bx(wall_x + wall_thick), by(-25),
               "WALL", offset=by(5), fs=6, above=False, font=FONT)
    draw_dim_v(ax_b, bx(wall_x + wall_thick + 8), by(cut_bot), by(cut_top),
               f"{CUT_H}mm\nCUTOUT", offset=bx(5), fs=6, right=True, font=FONT)

    # Leader labels
    leader(ax_b, bx(gasket_x - gasket_t_draw / 2 + 3),
           by(cut_top + 5),
           bx(gasket_x - 60), by(cut_top - 5),
           "NEOPRENE GASKET\n3mm — WEATHERSEAL",
           fs=6, color=C_GASKT, ha="center", arrow_style="-|>", font=FONT)

    leader(ax_b, bx(plate_x + PLATE_T / 2), by(cut_top + 23),
           bx(plate_x - 25), by(sec_h + 40),
           f"ALUMINUM FACE PLATE\n{PLATE_W}×{PLATE_H}×{PLATE_T}mm\nFLUSH WITH WALL",
           fs=6, color=C_OUT, ha="center", arrow_style="-|>", font=FONT)

    leader(ax_b, bx(wall_x + wall_thick / 2), by(-15),
           bx(wall_x + wall_thick / 2), by(-35),
           "CONTAINER WALL\n(CORRUGATED STEEL)",
           fs=6, color=C_WALL, ha="center", va="top", arrow_style="-|>", font=FONT)

    leader(ax_b, bx(wall_x + wall_thick + 5), by(bolt_positions[1]),
           bx(wall_x + wall_thick + 25), by(bolt_positions[1] + 25),
           "M6 BOLT + NUT\nW/ WASHER (×4)",
           fs=6, color=C_DIM, ha="left", arrow_style="-|>", font=FONT)

    # ═════════════════════════════════════════════════════════════════════════
    # VIEW C — Simplified Wiring Schematic
    # ═════════════════════════════════════════════════════════════════════════
    ax_c = fig.add_subplot(gs[1, :])
    ax_c.set_aspect("equal")
    ax_c.axis("off")
    ax_c.set_xlim(0, 22)
    ax_c.set_ylim(-1.2, 4.5)

    ax_c.text(8.75, 4.6, "VIEW C — WIRING SCHEMATIC",
              ha="center", va="bottom", fontsize=9, fontweight="bold",
              color=C_OUT, **FONT)

    def sbox(ax, x, y, w, h, label, sublabel="", fc="white", tc=C_OUT):
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                     boxstyle="round,pad=0.06", fc=fc, ec=C_OUT, lw=1.2, zorder=3))
        ax.text(x + w / 2, y + h / 2 + (0.12 if sublabel else 0), label,
                ha="center", va="center", fontsize=7.5, fontweight="bold",
                color=tc, **FONT, zorder=4)
        if sublabel:
            ax.text(x + w / 2, y + h / 2 - 0.15, sublabel,
                    ha="center", va="center", fontsize=6, color=C_DIM,
                    **FONT, zorder=4)

    def sarrow(ax, x1, y, x2, col=C_OUT, lw=1.8):
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=lw), zorder=3)

    row_bot = 0.8
    row_top = 2.8

    # Solar path (top row)
    sbox(ax_c, 0.5, row_top, 2.8, 0.9,
         "SOLAR PANELS", "3×200W  12V", fc="#E8F5E8", tc=C_MC4)
    sarrow(ax_c, 3.3, row_top + 0.45, 4.5, col=C_MC4)
    ax_c.text(3.9, row_top + 0.65, "MC4", fontsize=6, color=C_MC4,
              ha="center", **FONT)

    sbox(ax_c, 4.5, row_top, 3.0, 0.9,
         "FLUSH-MOUNT PANEL", "MC4 bulkhead ×3", fc=C_ALUM)
    sarrow(ax_c, 7.5, row_top + 0.45, 10.0, col=C_MC4)
    ax_c.text(8.75, row_top + 0.65, "10 AWG PV", fontsize=6, color=C_MC4,
              ha="center", **FONT)

    sbox(ax_c, 10.0, row_top, 3.2, 0.9,
         "MPPT CONTROLLER", "Victron 100/50", fc="#FFF3CC")
    sarrow(ax_c, 13.2, row_top + 0.45, 14.5, col=C_CL)
    sbox(ax_c, 14.5, row_top - 0.3, 3.0, 1.5,
         "BATTERY BANK", "2×100Ah LiFePO4", fc="#E0E8F8")

    # Shore power path (bottom row)
    sbox(ax_c, 0.5, row_bot, 2.8, 0.9,
         "SHORE POWER", "120V AC mains", fc=C_NEMA, tc=C_AC)
    sarrow(ax_c, 3.3, row_bot + 0.45, 4.5, col=C_AC)
    ax_c.text(3.9, row_bot + 0.65, "AC cord", fontsize=6, color=C_AC,
              ha="center", **FONT)

    sbox(ax_c, 4.5, row_bot, 3.0, 0.9,
         "FLUSH-MOUNT PANEL", "NEMA 5-15R inlet", fc=C_ALUM)
    sarrow(ax_c, 7.5, row_bot + 0.45, 10.0, col=C_AC)

    sbox(ax_c, 10.0, row_bot, 3.2, 0.9,
         "SHORE CHARGER", "Victron IP65 12/15", fc="#F5EDD0", tc=C_AC)
    # Continuous line from shore charger to battery bank
    bat_cx = 16.0
    ax_c.plot([13.2, bat_cx], [row_bot + 0.45, row_bot + 0.45],
              color=C_AC, lw=1.8, zorder=3)
    ax_c.annotate("", xy=(bat_cx, row_top - 0.3), xytext=(bat_cx, row_bot + 0.45),
                  arrowprops=dict(arrowstyle="-|>", color=C_AC, lw=1.8,
                                  connectionstyle="arc3,rad=0"), zorder=3)
    ax_c.text(bat_cx + 0.15, (row_top + row_bot) / 2 + 0.3, "12V DC\ncharge",
              fontsize=6, color=C_AC, ha="left", va="center", **FONT)

    # Cooler DC output path (bottom row — reverse direction: interior → exterior)
    row_cool = -0.4
    sbox(ax_c, 0.5, row_cool, 2.8, 0.9,
         "EVAP COOLER", "12V DC  80W", fc="#FFE0C0", tc=C_DT)
    sarrow(ax_c, 4.5, row_cool + 0.45, 3.3, col=C_DT)
    ax_c.text(3.9, row_cool + 0.65, "DT 2-pin", fontsize=6, color=C_DT,
              ha="center", **FONT)

    sbox(ax_c, 4.5, row_cool, 3.0, 0.9,
         "FLUSH-MOUNT PANEL", "DT bulkhead ×1", fc=C_ALUM)
    sarrow(ax_c, 10.0, row_cool + 0.45, 7.5, col=C_DT)
    ax_c.text(8.75, row_cool + 0.65, "14 AWG Cct E", fontsize=6, color=C_DT,
              ha="center", **FONT)

    sbox(ax_c, 10.0, row_cool, 3.2, 0.9,
         "FUSE BLOCK", "Cct E — 10A", fc="#FFF3CC", tc=C_DT)
    sarrow(ax_c, 14.5, row_cool + 0.45, 13.2, col=C_DT)
    ax_c.plot([14.5, bat_cx], [row_cool + 0.45, row_cool + 0.45],
              color=C_DT, lw=1.8, zorder=3)
    ax_c.annotate("", xy=(bat_cx, row_top - 0.3), xytext=(bat_cx, row_cool + 0.45),
                  arrowprops=dict(arrowstyle="-|>", color=C_DT, lw=1.0,
                                  connectionstyle="arc3,rad=0"), zorder=2)

    # Container wall indicator — single line (flush mount, no gland)
    wall_x_sch = 7.45
    ax_c.plot([wall_x_sch, wall_x_sch],
              [row_cool - 0.5, row_top + 1.0],
              color=C_WALL, lw=4, zorder=1)
    ax_c.text(wall_x_sch, row_cool - 0.7, "CONTAINER\nWALL",
              ha="center", va="top", fontsize=6, color=C_WALL,
              fontweight="bold", **FONT)
    ax_c.text(wall_x_sch + 0.15, row_cool - 0.45, "(flush-mount\n panel)",
              ha="left", va="top", fontsize=5, color=C_DIM, **FONT)

    # Zone labels
    ax_c.text(wall_x_sch / 2, row_top + 1.35, "EXTERIOR",
              ha="center", va="bottom", fontsize=8, fontweight="bold",
              color=C_DIM, **FONT)
    ax_c.text((wall_x_sch + 22) / 2, row_top + 1.35, "CONTAINER INTERIOR",
              ha="center", va="bottom", fontsize=8, fontweight="bold",
              color=C_DIM, **FONT)

    # ═════════════════════════════════════════════════════════════════════════
    # Title block
    # ═════════════════════════════════════════════════════════════════════════
    ax_tb = fig.add_axes([0.05, 0.0, 0.9, 0.08])
    ax_tb.set_xlim(0, 1)
    ax_tb.set_ylim(0, 1)
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 1 OF 1",
                drawing_title="EXTERNAL POWER PANEL — FLUSH MOUNT",
                subtitle="SOLAR + SHORE INPUT · COOLER DC OUTPUT · WIRING SCHEMATIC",
                scale_note="AXES IN mm",
                height=0.85)

    fig.savefig(f"{DIAGRAMS_DIR}/power-panel-sheet1.png",
                dpi=150, bbox_inches="tight", facecolor="white")
    fig.savefig(svg_path(f"{DIAGRAMS_DIR}/power-panel-sheet1.png"),
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  → power-panel-sheet1.png  Done.")


if __name__ == "__main__":
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    os.makedirs(SVG_DIR, exist_ok=True)
    print("Generating TBS-001 External Power Panel diagram...")
    draw_sheet1()
    print("Done.")
