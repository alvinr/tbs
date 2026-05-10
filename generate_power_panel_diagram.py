#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_power_panel_diagram.py — TBS-001 External Power Panel

Sheet 1 — Detail drawing of the combined solar + shore power input panel
mounted on the pinhole wall exterior.  Three views:

  A  Front elevation (panel face, ~1:2 scale)
  B  Side section (wall penetration cross-section)
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
    DIAGRAMS_DIR, SVG_DIR, svg_path,
)
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_rect, draw_circle

# ── Palette ──────────────────────────────────────────────────────────────────
C_OUT   = "#1A1A1A"
C_DIM   = "#404040"
C_CL    = "#2060A0"
C_STEEL = "#B0B0B8"
C_ALUM  = "#C8D8E8"
C_BOX   = "#E8E0C8"      # panel enclosure fill
C_NEMA  = "#FFF0CC"       # NEMA inlet fill
C_MC4   = "#2D7A2D"       # MC4 connector color (solar green)
C_AC    = "#A07820"       # AC shore power color
C_WALL  = "#C0C0C8"       # container wall
C_INT   = "#F0FFF0"       # interior zone
FONT    = {"fontfamily": "monospace"}

# ── Panel dimensions (mm) ───────────────────────────────────────────────────
BOX_W   = PWR_PANEL_W     # 300mm
BOX_H   = PWR_PANEL_H     # 200mm
BOX_D   = PWR_PANEL_D     # 120mm
WALL_T  = 3               # container wall thickness (corrugated steel)
GLAND_OD = 32             # M32 cable gland outer diameter
GLAND_ID = 25             # cable gland inner bore
MOUNT_HOLE_D = 6          # mounting bolt hole diameter
MOUNT_INSET  = 15         # mounting hole inset from edge

# MC4 connector layout
MC4_R    = 8              # MC4 bulkhead connector radius
MC4_X    = 70             # MC4 column X from panel left edge
MC4_GAP  = 25             # gap between + and - in a pair
MC4_PITCH = 55            # vertical pitch between pairs

# NEMA inlet
NEMA_W   = 55             # NEMA receptacle width
NEMA_H   = 45             # NEMA receptacle height
NEMA_X   = 195            # NEMA left edge from panel left edge
NEMA_Y   = 77             # NEMA bottom edge from panel bottom edge


def draw_sheet1():
    fig = plt.figure(figsize=(22, 15))
    fig.patch.set_facecolor("white")

    # Use gridspec for three views
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1], height_ratios=[3, 1.2],
                          hspace=0.25, wspace=0.3,
                          left=0.05, right=0.95, top=0.92, bottom=0.08)

    # ═════════════════════════════════════════════════════════════════════════
    # VIEW A — Front Elevation (panel face, exterior view)
    # ═════════════════════════════════════════════════════════════════════════
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.set_aspect("equal")
    ax_a.axis("off")

    S = 2.0  # scale: 1 drawing unit = 0.5mm → 2:1 scale
    def sx(mm): return mm * S
    def sy(mm): return mm * S

    pad = 80
    ax_a.set_xlim(sx(-pad), sx(BOX_W + pad))
    ax_a.set_ylim(sy(-pad), sy(BOX_H + pad))

    # Panel enclosure outline
    ax_a.add_patch(mpatches.FancyBboxPatch(
        (sx(0), sy(0)), sx(BOX_W), sy(BOX_H),
        boxstyle="round,pad=6", fc=C_BOX, ec=C_OUT, lw=2.0, zorder=3))

    # Mounting holes (4 corners)
    for mx, my in [(MOUNT_INSET, MOUNT_INSET),
                   (BOX_W - MOUNT_INSET, MOUNT_INSET),
                   (MOUNT_INSET, BOX_H - MOUNT_INSET),
                   (BOX_W - MOUNT_INSET, BOX_H - MOUNT_INSET)]:
        draw_circle(ax_a, sx(mx), sy(my), sx(MOUNT_HOLE_D / 2),
                     lw=0.8, color=C_DIM, zorder=4)

    # MC4 bulkhead connectors — 3 pairs on left side
    mc4_y_base = BOX_H / 2 - MC4_PITCH  # center the 3 pairs vertically
    for i in range(3):
        cy = mc4_y_base + i * MC4_PITCH
        # Positive connector
        cx_pos = MC4_X - MC4_GAP / 2
        draw_circle(ax_a, sx(cx_pos), sy(cy), sx(MC4_R),
                     lw=1.5, color=C_MC4, fill=True, fc="#C0E8C0", zorder=5)
        ax_a.text(sx(cx_pos), sy(cy), "+", ha="center", va="center",
                  fontsize=8, fontweight="bold", color=C_MC4, zorder=6)
        # Negative connector
        cx_neg = MC4_X + MC4_GAP / 2
        draw_circle(ax_a, sx(cx_neg), sy(cy), sx(MC4_R),
                     lw=1.5, color=C_MC4, fill=True, fc="#E0E0E0", zorder=5)
        ax_a.text(sx(cx_neg), sy(cy), "−", ha="center", va="center",
                  fontsize=8, fontweight="bold", color=C_DIM, zorder=6)
        # Pair label
        ax_a.text(sx(MC4_X + MC4_GAP / 2 + MC4_R + 8), sy(cy),
                  f"PV{i + 1}", ha="left", va="center",
                  fontsize=7, color=C_MC4, fontweight="bold", **FONT, zorder=6)

    # NEMA 5-15R inlet — right side
    nema_cx = NEMA_X + NEMA_W / 2
    nema_cy = NEMA_Y + NEMA_H / 2
    ax_a.add_patch(mpatches.FancyBboxPatch(
        (sx(NEMA_X), sy(NEMA_Y)), sx(NEMA_W), sy(NEMA_H),
        boxstyle="round,pad=3", fc=C_NEMA, ec=C_OUT, lw=1.5, zorder=5))
    # NEMA slot symbol (simplified: two vertical slots + ground)
    slot_w, slot_h = 4, 14
    slot_gap = 18
    for dx in [-slot_gap / 2, slot_gap / 2]:
        ax_a.add_patch(mpatches.Rectangle(
            (sx(nema_cx + dx - slot_w / 2), sy(nema_cy + 2)),
            sx(slot_w), sy(slot_h),
            fc="white", ec=C_OUT, lw=1.0, zorder=6))
    # Ground slot (half-circle at bottom)
    ground_r = 5
    theta = np.linspace(np.pi, 2 * np.pi, 20)
    gx = sx(nema_cx) + sx(ground_r) * np.cos(theta)
    gy = sy(nema_cy - 6) + sx(ground_r) * np.sin(theta)
    ax_a.plot(gx, gy, color=C_OUT, lw=1.0, zorder=6)

    # Labels
    ax_a.text(sx(BOX_W / 2), sy(BOX_H + 15),
              "VIEW A — FRONT ELEVATION (EXTERIOR FACE)",
              ha="center", va="bottom", fontsize=9, fontweight="bold",
              color=C_OUT, **FONT)

    # Dimension lines
    draw_dim_h(ax_a, sx(0), sx(BOX_W), sy(-30),
               f"{BOX_W}mm", offset=sy(8), fs=7, above=False, font=FONT)
    draw_dim_v(ax_a, sx(-30), sy(0), sy(BOX_H),
               f"{BOX_H}mm", offset=sx(8), fs=7, font=FONT)

    # Leader labels
    leader(ax_a, sx(MC4_X), sy(mc4_y_base + 2 * MC4_PITCH + MC4_R + 5),
           sx(MC4_X - 25), sy(BOX_H + 45),
           "MC4 BULKHEAD\nCONNECTORS (×3 PAIRS)\nIP67 PANEL-MOUNT",
           fs=6.5, color=C_MC4, ha="center", arrow_style="-|>", font=FONT)

    leader(ax_a, sx(nema_cx), sy(NEMA_Y - 5),
           sx(nema_cx + NEMA_W * 2), sy(NEMA_Y - 10),
           "NEMA 5-15R\nWEATHERPROOF INLET\n120V AC SHORE POWER",
           fs=6.5, color=C_AC, ha="center", va="top", arrow_style="-|>", font=FONT)

    leader(ax_a, sx(BOX_W - MOUNT_INSET + MOUNT_HOLE_D), sy(BOX_H - MOUNT_INSET),
           sx(BOX_W + 25), sy(BOX_H + 30),
           f"M{MOUNT_HOLE_D} MOUNTING\nBOLTS (×4)",
           fs=6, color=C_DIM, arrow_style="-|>", font=FONT)

    # ═════════════════════════════════════════════════════════════════════════
    # VIEW B — Side Section (wall penetration cross-section)
    # ═════════════════════════════════════════════════════════════════════════
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.set_aspect("equal")
    ax_b.axis("off")

    # Scale: exaggerate wall thickness for clarity
    # Horizontal: depth axis. Vertical: height.
    # Layout: exterior (left) | wall | interior (right)
    Sb = 1.5  # scale factor
    def bx(mm): return mm * Sb
    def by(mm): return mm * Sb

    wall_x = 180       # wall left face X position in drawing
    wall_w = 50        # exaggerated wall thickness for visibility
    ext_pad = 60
    int_pad = 200

    ax_b.set_xlim(bx(-ext_pad), bx(wall_x + wall_w + int_pad))
    ax_b.set_ylim(by(-60), by(BOX_H + 80))

    # Container wall (hatched)
    ax_b.add_patch(mpatches.Rectangle(
        (bx(wall_x), by(-30)), bx(wall_w), by(BOX_H + 100),
        fc=C_WALL, ec=C_OUT, lw=1.5, hatch="///", zorder=3))

    # Panel box (exterior side, attached to wall)
    panel_left = wall_x - BOX_D
    panel_bot = (BOX_H - BOX_H) / 2  # centered vertically (= 0)
    ax_b.add_patch(mpatches.Rectangle(
        (bx(panel_left), by(panel_bot)), bx(BOX_D), by(BOX_H),
        fc=C_BOX, ec=C_OUT, lw=1.5, zorder=4))

    # Cable gland through wall
    gland_cy = BOX_H / 2
    gland_left = wall_x - 10
    gland_right = wall_x + wall_w + 10
    # Gland body
    ax_b.add_patch(mpatches.Rectangle(
        (bx(gland_left), by(gland_cy - GLAND_OD / 2)),
        bx(gland_right - gland_left), by(GLAND_OD),
        fc="#D0D0D0", ec=C_OUT, lw=1.2, zorder=5))
    # Gland bore (cables pass through)
    ax_b.add_patch(mpatches.Rectangle(
        (bx(gland_left - 5), by(gland_cy - GLAND_ID / 2)),
        bx(gland_right - gland_left + 10), by(GLAND_ID),
        fc="white", ec=C_DIM, lw=0.6, ls="--", zorder=5))

    # Cables through gland — PV (green) and AC (brown), parallel
    cable_ext = panel_left + BOX_D * 0.3  # start inside box
    cable_int = wall_x + wall_w + 80      # end inside container

    # PV cables (3, parallel, slightly offset vertically)
    for off in [-6, 0, 6]:
        ax_b.plot([bx(cable_ext), bx(cable_int)],
                  [by(gland_cy + off), by(gland_cy + off)],
                  color=C_MC4, lw=1.5, zorder=6)
    # AC cable (parallel, offset above PV bundle)
    ax_b.plot([bx(cable_ext), bx(cable_int)],
              [by(gland_cy + 10), by(gland_cy + 10)],
              color=C_AC, lw=1.5, ls="--", zorder=6)

    # Interior destination labels
    ax_b.text(bx(cable_int + 5), by(gland_cy),
              "→ MPPT CHARGE CONTROLLER",
              ha="left", va="center", fontsize=7, color=C_MC4,
              fontweight="bold", **FONT, zorder=7)
    ax_b.text(bx(cable_int + 5), by(gland_cy + 10),
              "→ SHORE CHARGER",
              ha="left", va="center", fontsize=7, color=C_AC,
              fontweight="bold", **FONT, zorder=7)

    # Zone labels
    ax_b.text(bx(panel_left - 20), by(BOX_H + 50),
              "EXTERIOR", ha="center", va="bottom", fontsize=9,
              fontweight="bold", color=C_DIM, **FONT)
    ax_b.text(bx(wall_x + wall_w + int_pad / 2), by(BOX_H + 50),
              "INTERIOR", ha="center", va="bottom", fontsize=9,
              fontweight="bold", color=C_DIM, **FONT)

    # Interior zone fill
    ax_b.add_patch(mpatches.Rectangle(
        (bx(wall_x + wall_w), by(-30)), bx(int_pad), by(BOX_H + 100),
        fc=C_INT, ec="none", alpha=0.3, zorder=1))

    # Title
    ax_b.text(bx((wall_x + wall_w + int_pad) / 2), by(BOX_H + 70),
              "VIEW B — SIDE SECTION (WALL PENETRATION)",
              ha="center", va="bottom", fontsize=9, fontweight="bold",
              color=C_OUT, **FONT)

    # Dimension: box depth
    draw_dim_h(ax_b, bx(panel_left), bx(wall_x), by(-35),
               f"{BOX_D}mm DEPTH", offset=by(7), fs=6.5, above=False, font=FONT)
    # Dimension: wall thickness
    draw_dim_h(ax_b, bx(wall_x), bx(wall_x + wall_w), by(-35),
               f"WALL", offset=by(7), fs=6, above=False, font=FONT)
    # Dimension: gland OD
    draw_dim_v(ax_b, bx(gland_right + 15), by(gland_cy - GLAND_OD / 2),
               by(gland_cy + GLAND_OD / 2),
               f"M{GLAND_OD}", offset=bx(6), fs=6.5, right=True, font=FONT)

    # Leader labels
    leader(ax_b, bx(wall_x + wall_w / 2), by(-25),
           bx(wall_x + wall_w / 2), by(-50),
           "CONTAINER WALL\n(CORRUGATED STEEL)",
           fs=6, color=C_WALL, ha="center", va="top", arrow_style="-|>", font=FONT)

    leader(ax_b, bx((gland_left + gland_right) / 2), by(gland_cy + GLAND_OD / 2 + 3),
           bx(wall_x - 40), by(gland_cy + 60),
           "IP68 CABLE GLAND\nM32 SEALED\nPENETRATION",
           fs=6.5, color=C_DIM, ha="center", arrow_style="-|>", font=FONT)

    leader(ax_b, bx(panel_left + BOX_D / 2), by(BOX_H + 3),
           bx(panel_left - 30), by(BOX_H + 40),
           f"IP65 JUNCTION BOX\n{BOX_W}×{BOX_H}×{BOX_D}mm",
           fs=6.5, color=C_OUT, ha="center", arrow_style="-|>", font=FONT)

    # ═════════════════════════════════════════════════════════════════════════
    # VIEW C — Simplified Wiring Schematic
    # ═════════════════════════════════════════════════════════════════════════
    ax_c = fig.add_subplot(gs[1, :])
    ax_c.set_aspect("equal")
    ax_c.axis("off")
    ax_c.set_xlim(0, 22)
    ax_c.set_ylim(0, 4.5)

    ax_c.text(11, 4.2, "VIEW C — WIRING SCHEMATIC",
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

    # Row positions
    row_bot = 0.8
    row_top = 2.8
    sbox(ax_c, 0.5, row_top, 2.8, 0.9,
         "SOLAR PANELS", "3×200W  12V", fc="#E8F5E8", tc=C_MC4)
    sarrow(ax_c, 3.3, row_top + 0.45, 4.5, col=C_MC4)
    ax_c.text(3.9, row_top + 0.65, "MC4", fontsize=6, color=C_MC4,
              ha="center", **FONT)

    sbox(ax_c, 4.5, row_top, 3.0, 0.9,
         "EXT POWER PANEL", "MC4 bulkhead ×3", fc=C_BOX)
    sarrow(ax_c, 7.5, row_top + 0.45, 9.0, col=C_MC4)
    ax_c.text(8.25, row_top + 0.65, "10 AWG PV", fontsize=6, color=C_MC4,
              ha="center", **FONT)

    # Cable gland spans both rows
    gland_x = 9.0
    gland_w = 1.5
    gland_bot = row_bot
    gland_top = row_top + 0.9
    sbox(ax_c, gland_x, gland_bot, gland_w, gland_top - gland_bot,
         "CABLE\nGLAND", "M32 IP68", fc="#D0D0D0")

    sarrow(ax_c, 10.5, row_top + 0.45, 12.0, col=C_MC4)
    sbox(ax_c, 12.0, row_top, 3.2, 0.9,
         "MPPT CONTROLLER", "Victron 100/50", fc="#FFF3CC")
    sarrow(ax_c, 15.2, row_top + 0.45, 16.5, col=C_CL)
    sbox(ax_c, 16.5, row_top - 0.3, 3.0, 1.5,
         "BATTERY BANK", "2×100Ah LiFePO4", fc="#E0E8F8")

    # Shore power path (bottom row)
    sbox(ax_c, 0.5, row_bot, 2.8, 0.9,
         "SHORE POWER", "120V AC mains", fc=C_NEMA, tc=C_AC)
    sarrow(ax_c, 3.3, row_bot + 0.45, 4.5, col=C_AC)
    ax_c.text(3.9, row_bot + 0.65, "AC cord", fontsize=6, color=C_AC,
              ha="center", **FONT)

    sbox(ax_c, 4.5, row_bot, 3.0, 0.9,
         "EXT POWER PANEL", "NEMA 5-15R inlet", fc=C_BOX)
    sarrow(ax_c, 7.5, row_bot + 0.45, 9.0, col=C_AC)

    sarrow(ax_c, 10.5, row_bot + 0.45, 12.0, col=C_AC)
    sbox(ax_c, 12.0, row_bot, 3.2, 0.9,
         "SHORE CHARGER", "Victron IP65 12/15", fc="#F5EDD0", tc=C_AC)
    sarrow(ax_c, 15.2, row_bot + 0.45, 16.5, col=C_AC)

    # Arrow from shore charger up to battery
    ax_c.annotate("", xy=(18.0, row_top - 0.3), xytext=(18.0, row_bot + 0.9),
                  arrowprops=dict(arrowstyle="-|>", color=C_AC, lw=1.5,
                                  connectionstyle="arc3,rad=0"), zorder=3)
    ax_c.text(18.15, (row_top + row_bot) / 2 + 0.3, "12V DC\ncharge",
              fontsize=6, color=C_AC, ha="left", va="center", **FONT)

    # Container wall indicator
    wall_x_sch = 9.0
    ax_c.plot([wall_x_sch - 0.1, wall_x_sch - 0.1],
              [row_bot - 0.2, row_top + 1.0],
              color=C_WALL, lw=3, zorder=1)
    ax_c.plot([10.6, 10.6],
              [row_bot - 0.2, row_top + 1.0],
              color=C_WALL, lw=3, zorder=1)
    ax_c.text(9.75, gland_bot - 0.55, "CONTAINER\nWALL",
              ha="center", va="bottom", fontsize=6, color=C_WALL,
              fontweight="bold", **FONT)

    # ═════════════════════════════════════════════════════════════════════════
    # Title block (use the full figure axes)
    # ═════════════════════════════════════════════════════════════════════════
    # Create a spanning axes for the title block
    ax_tb = fig.add_axes([0.05, 0.0, 0.9, 0.08])
    ax_tb.set_xlim(0, 1)
    ax_tb.set_ylim(0, 1)
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 1 OF 1",
                drawing_title="EXTERNAL POWER PANEL",
                subtitle="FRONT ELEVATION · WALL SECTION · WIRING SCHEMATIC",
                scale_note="VIEWS A/B ≈ 2:1 · ALL DIMS IN mm",
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
