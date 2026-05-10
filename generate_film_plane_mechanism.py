#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_film_plane_mechanism.py
Moveable film plane mechanism — engineering drawings (4 sheets)
4-CORNER INDEPENDENT DESIGN: TL, TR, BL, BR each driven by its own leadscrew.
Supports full tilt, swing, and compound tilt+swing independently.

Sheet 1 — Plan view (top-down): 4-corner rail layout, example configs
Sheet 2 — Elevations: side elevation (tilt) + plan cross-section (swing)
Sheet 3 — Frame & hardware detail: corner bracket, universal joint, ACM panel
Sheet 4 — Movement specification table & BOM
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Arc, Polygon
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe

from tbs_constants import (
    FP_X_L, FP_X_R, PH_X as PH_X_C, PH_H as PH_H_C,
    MAX_TILT_DEG, MAX_SWING_DEG, RAIL_SPAN, DIAGRAMS_DIR, SVG_DIR, svg_path,
)
from tbs_title_block import title_block
from tbs_drawing import leader

# ── Palette (white engineering style) ────────────────────────────────────────
BG      = "#FFFFFF"   # white background
GRID    = "#FFFFFF"   # container interior (white)
STRUCT  = "#B0B0B8"   # steel section fill (walls)
STRUCT2 = "#C8D8E8"   # aluminium / secondary structure
DIM     = "#404040"   # dimension lines and text (dark grey)
ANNO    = "#1A1A1A"   # annotation text (near black)
WHITE   = "#1A1A1A"   # outlines / text (was white-on-dark; now dark-on-white)
C_FLAT  = "#2060A0"   # flat position line (blue)
C_T1    = "#1A7A1A"   # tilt config (dark green)
C_T2    = "#B07010"   # swing config (amber)
C_T3    = "#CC2020"   # compound config (red)
RAIL    = "#5A3E00"   # rail (dark brown-gold — dark enough for white text labels)
MECH    = "#2A6B2A"   # mechanism/carriage (dark green — dark enough for white text)
PINHOLE = "#CC6600"   # pinhole aperture (orange, visible on white)

# ── Container dimensions (mm) ─────────────────────────────────────────────────
L = 5893   # interior length (film plane spans this direction)
W = 2362   # interior width = optical axis = focal length
H = 2388   # interior height
WALL_T = 40

# Carriage travel limits (100 mm clearance each end)
D_NEAR = 100
D_FAR  = W - 100   # = 2262

# ── 4-corner configs (d_TL, d_TR, d_BL, d_BR) — depths from pinhole wall ─────
# TL=top-left, TR=top-right, BL=bottom-left, BR=bottom-right
# Angle labels computed from geometry so they stay correct after rail span changes.
_tilt_deg  = round(np.degrees(np.arctan2(D_FAR - 800, H)), 1)
_swing_deg = round(np.degrees(np.arctan2(D_FAR - 800, FP_X_R - FP_X_L)), 1)
CONFIGS = [
    ("Flat  0°",                   D_FAR,  D_FAR,  D_FAR,  D_FAR,  C_FLAT, "-"),
    (f"Tilt  {_tilt_deg}°",        800,    800,    D_FAR,  D_FAR,  C_T1,   "--"),
    (f"Swing  {_swing_deg}°",      800,    D_FAR,  800,    D_FAR,  C_T2,   "-."),
    ("Compound\ntilt+swing",       D_NEAR, D_FAR,  D_FAR,  D_NEAR, C_T3,   ":"),
]

FONT = {"fontfamily": "monospace"}

# ── Geometry helpers ──────────────────────────────────────────────────────────
RAIL_X_L = FP_X_L       # left rail X position (mm) — tracks FP_X_L from constants
RAIL_X_R = FP_X_R       # right rail X position (mm) — tracks FP_X_R from constants
RAIL_W   = 60           # rail width in plan view


def dim_line_h(ax, x0, x1, y, text, offset=30, col=DIM, fs=7):
    tick = max(abs(offset) * 0.3, 15)   # minimum 15mm tick
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9, mutation_scale=6))
    ax.plot([x0, x0], [y - tick, y + tick], color=col, lw=0.6)
    ax.plot([x1, x1], [y - tick, y + tick], color=col, lw=0.6)
    ax.text((x0+x1)/2, y+offset, text, color=col, fontsize=fs,
            ha="center", va="bottom", **FONT)

def dim_line_v(ax, x, y0, y1, text, offset=30, col=DIM, fs=7):
    tick = max(abs(offset) * 0.3, 15)   # minimum 15mm tick
    ax.annotate("", xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9, mutation_scale=6))
    ax.plot([x - tick, x + tick], [y0, y0], color=col, lw=0.6)
    ax.plot([x - tick, x + tick], [y1, y1], color=col, lw=0.6)
    ax.text(x+offset, (y0+y1)/2, text, color=col, fontsize=fs,
            ha="left", va="center", **FONT)


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — PLAN VIEW (top-down)
# X = container length (left→right, 0→L)
# Y = optical axis depth (0=pinhole wall → W=far wall)
# In this view TILT (height difference) is invisible; SWING is visible as diagonal.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    PAD = 500
    ax.set_xlim(-PAD, L + 1400)
    ax.set_ylim(-1150, W + 750)
    ax.set_aspect("equal")
    ax.axis("off")

    # Container outline
    ax.add_patch(Rectangle((0, 0), L, W, fc=GRID, ec=WHITE, lw=1.8, zorder=2))

    # Wall hatching (structural ribs every 457mm)
    for x in np.arange(80, L, 457):
        ax.plot([x, x], [0, W], color=STRUCT2, lw=0.4, alpha=0.35, zorder=3)

    # Pinhole wall (y=0)
    ax.add_patch(Rectangle((0, -WALL_T), L, WALL_T, fc=STRUCT2, ec=WHITE, lw=1.5, zorder=4))
    ax.text(L/2, -WALL_T/2 - 125, "PINHOLE WALL  (20ft LONG SIDE)",
            color=WHITE, fontsize=7.5, ha="center", va="center", **FONT, zorder=5)

    # Far wall (y=W)
    ax.add_patch(Rectangle((0, W), L, WALL_T, fc=STRUCT, ec=WHITE, lw=1.0, zorder=4))
    ax.text(L/2, W + WALL_T/2, "FAR WALL", color=DIM, fontsize=7,
            ha="center", va="center", **FONT, zorder=5)

    # End walls
    for xw in [(-WALL_T, -WALL_T, WALL_T, W+2*WALL_T), (L, -WALL_T, WALL_T, W+2*WALL_T)]:
        ax.add_patch(Rectangle((xw[0], xw[1]), xw[2], xw[3],
                               fc=STRUCT, ec=WHITE, lw=1.0, zorder=4))

    # Pinhole (X=2874mm in new layout, recentred on new film plane)
    ph_x = PH_X_C
    ax.add_patch(Circle((ph_x, 0), 60, fc=PINHOLE, ec=WHITE, lw=1.5, zorder=6))
    ax.add_patch(Circle((ph_x, 0), 20, fc=BG, ec=WHITE, lw=1.0, zorder=7))
    ax.text(ph_x + 130, 75, f"PINHOLE  X={ph_x}mm  Ø2.17mm", color=PINHOLE, fontsize=7, **FONT)

    # ── 4 INDEPENDENT RAILS — one at each corner ──────────────────────────────
    # Left rails: at X=RAIL_X_L (ceiling = label TL/BL, floor = label TL/BL)
    # Right rails: at X=RAIL_X_R (ceiling = label TR/BR, floor = label TR/BR)
    # In plan view both ceiling and floor rails project to same X position.
    # We show them slightly offset for clarity.
    for (rx, label_side) in [(RAIL_X_L, "LEFT"), (RAIL_X_R, "RIGHT")]:
        # Ceiling rail (slightly inward)
        rx_ceil = rx - RAIL_W//2 - 5
        ax.add_patch(Rectangle((rx_ceil, D_NEAR), RAIL_W*0.8, D_FAR-D_NEAR,
                               fc=RAIL, ec=WHITE, lw=1.0, zorder=5, alpha=0.85))
        # Floor rail (slightly outward)
        rx_floor = rx + 5
        ax.add_patch(Rectangle((rx_floor, D_NEAR), RAIL_W*0.8, D_FAR-D_NEAR,
                               fc=RAIL, ec=WHITE, lw=1.0, zorder=5, alpha=0.65))
        # Labels — 45° leaders outward from rail midpoint
        rail_mid_y = D_NEAR + (D_FAR - D_NEAR) * 0.8
        ldr_off = 150
        if label_side == "LEFT":
            # Leaders go left
            ax.annotate(f"CEILING RAIL  ({label_side})",
                        xy=(rx_ceil + RAIL_W * 0.4, rail_mid_y + 200),
                        xytext=(rx_ceil - ldr_off, rail_mid_y + 200 + ldr_off),
                        fontsize=6.5, color=RAIL, ha="right", va="bottom", **FONT,
                        arrowprops=dict(arrowstyle="-", color=RAIL, lw=0.8),
                        zorder=15)
            ax.annotate(f"FLOOR RAIL  ({label_side})",
                        xy=(rx_floor + RAIL_W * 0.4, rail_mid_y - 200),
                        xytext=(rx_floor - ldr_off, rail_mid_y - 200 - ldr_off),
                        fontsize=6.5, color=RAIL, ha="right", va="top", **FONT,
                        arrowprops=dict(arrowstyle="-", color=RAIL, lw=0.8),
                        zorder=15)
        else:
            # Leaders go right
            ax.annotate(f"CEILING RAIL  ({label_side})",
                        xy=(rx_ceil + RAIL_W * 0.4, rail_mid_y + 200),
                        xytext=(rx_ceil + ldr_off, rail_mid_y + 200 + ldr_off),
                        fontsize=6.5, color=RAIL, ha="left", va="bottom", **FONT,
                        arrowprops=dict(arrowstyle="-", color=RAIL, lw=0.8),
                        zorder=15)
            ax.annotate(f"FLOOR RAIL  ({label_side})",
                        xy=(rx_floor + RAIL_W * 0.4, rail_mid_y - 200),
                        xytext=(rx_floor + ldr_off, rail_mid_y - 200 - ldr_off),
                        fontsize=6.5, color=RAIL, ha="left", va="top", **FONT,
                        arrowprops=dict(arrowstyle="-", color=RAIL, lw=0.8),
                        zorder=15)
        # Rail end stops
        for ry in [D_NEAR, D_FAR]:
            for rx_ in [rx_ceil, rx_floor]:
                ax.add_patch(Rectangle((rx_-15, ry-12), RAIL_W*0.8+30, 24,
                                       fc=WHITE, ec=WHITE, lw=0.5, zorder=6))

    # Travel dim
    tr_x = RAIL_X_L - RAIL_W - 50
    tr_tick = 15
    ax.annotate("", xy=(tr_x, D_FAR-20),
                xytext=(tr_x, D_NEAR+20),
                arrowprops=dict(arrowstyle="<->", color=WHITE, lw=0.8, mutation_scale=5))
    ax.plot([tr_x - tr_tick, tr_x + tr_tick], [D_NEAR+20, D_NEAR+20], color=WHITE, lw=0.6)
    ax.plot([tr_x - tr_tick, tr_x + tr_tick], [D_FAR-20, D_FAR-20], color=WHITE, lw=0.6)
    ax.text(RAIL_X_L - RAIL_W - 150, (D_NEAR+D_FAR)/2,
            f"{D_FAR-D_NEAR}\nmm\ntravel",
            color=WHITE, fontsize=6.5, ha="center", va="center", **FONT)

    # Corner labels
    for (cx, cy, lbl) in [
        (RAIL_X_L, D_FAR,  "TL"),
        (RAIL_X_R, D_FAR,  "TR"),
        (RAIL_X_L, D_NEAR, "BL"),
        (RAIL_X_R, D_NEAR, "BR"),
    ]:
        ax.text(cx, cy + 60, lbl, color=ANNO, fontsize=8, ha="center",
                fontweight="bold", **FONT, zorder=9)

    # ── FILM PLANE POSITIONS — shown as quadrilateral for each config ──────────
    for i, (name, d_TL, d_TR, d_BL, d_BR, col, ls) in enumerate(CONFIGS):
        lw = 2.2 if i == 0 else 1.8
        alpha = 1.0 if i == 0 else 0.88
        z = 8 + i

        # Corners in plan (X, Y=depth)
        pts = [
            (RAIL_X_L, d_TL),  # TL
            (RAIL_X_R, d_TR),  # TR
            (RAIL_X_R, d_BR),  # BR
            (RAIL_X_L, d_BL),  # BL
        ]
        xs = [p[0] for p in pts] + [pts[0][0]]
        ys = [p[1] for p in pts] + [pts[0][1]]

        ax.plot(xs, ys, color=col, lw=lw, ls=ls, alpha=alpha, zorder=z,
                solid_capstyle="round")
        # Corner carriage markers
        for (px, py) in pts:
            ax.add_patch(Circle((px, py), 55, fc=col, ec=WHITE, lw=0.7,
                                alpha=0.55, zorder=z))

        # Label
        cx_label = (RAIL_X_L + RAIL_X_R) / 2
        cy_label = (d_TL + d_TR + d_BL + d_BR) / 4
        ax.text(L + 200, (D_NEAR + D_FAR)/2 - i*220 + 400, name,
                color=col, fontsize=7, va="center", **FONT, zorder=10)
        ax.plot([L+50, L+180], [(D_NEAR+D_FAR)/2 - i*220 + 400,
                                (D_NEAR+D_FAR)/2 - i*220 + 400],
                color=col, lw=2.0, ls=ls, zorder=10)

    # ── Annotations ───────────────────────────────────────────────────────────
    # Swing annotation arrow
    ax.annotate("SWING moves\nthis edge", xy=(RAIL_X_R, 800), xytext=(RAIL_X_R+400, 700),
                color=C_T2, fontsize=6.5, **FONT,
                arrowprops=dict(arrowstyle="-|>", color=C_T2, lw=0.8, mutation_scale=5),
                ha="left")
    ax.annotate("TILT moves\nboth rails\nat same end",
                xy=(RAIL_X_L, (800+D_FAR)/2-800), xytext=(RAIL_X_L-750, (800+D_FAR)/2-800),
                color=C_T1, fontsize=6.5, **FONT,
                arrowprops=dict(arrowstyle="-|>", color=C_T1, lw=0.8, mutation_scale=5),
                ha="right")

    # Dims
    dim_line_h(ax, 0, L, W+150, f"INTERIOR LENGTH  {L} mm  (19 ft 4 in)",
               offset=10, col=DIM, fs=7.5)
    dim_line_v(ax, L+750, 0, W, f"OPTICAL AXIS\n{W} mm  (7 ft 9 in)",
               offset=20, col=DIM)
    dim_line_h(ax, 0, RAIL_X_L, -350, f"{RAIL_X_L} mm\n(left end zone)", col=DIM, fs=6.5)
    dim_line_h(ax, RAIL_X_L, RAIL_X_R, -350, f"Rail span  {RAIL_X_R-RAIL_X_L} mm", col=RAIL, fs=6.5)
    dim_line_h(ax, RAIL_X_R, L, -350, f"{L-RAIL_X_R} mm\n(right end zone)", col=DIM, fs=6.5)

    ax.text(L/2, W+580, "SHEET 1 — PLAN VIEW  (TOP DOWN, LOOKING AT CONTAINER FLOOR)",
            color=WHITE, fontsize=9, ha="center", fontweight="bold", **FONT)
    ax.text(L/2, W+470,
            "4 INDEPENDENT CORNER CARRIAGES  ·  TILT = CEILING vs FLOOR  ·  SWING = LEFT SIDE vs RIGHT SIDE",
            color=DIM, fontsize=7, ha="center", **FONT)
    ax.text(L/2, W+370,
            "IN THIS VIEW: SWING IS VISIBLE AS DIAGONAL  ·  TILT IS HIDDEN (HEIGHT AXIS = INTO PAGE)",
            color=DIM, fontsize=6.5, ha="center", **FONT)

    # Legend box — right side, above title block
    leg_x = L + 200
    leg_y = -250
    ax.text(leg_x + 500, leg_y + 160, "LEGEND", color=WHITE,
            fontsize=8, fontweight="bold", ha="center", **FONT)
    for i, (name, d_TL, d_TR, d_BL, d_BR, col, ls) in enumerate(CONFIGS):
        ly = leg_y - i * 160
        ax.plot([leg_x, leg_x + 400], [ly, ly], color=col, lw=2.0, ls=ls)
        corner_str = f"TL={d_TL}  TR={d_TR}  BL={d_BL}  BR={d_BR}"
        ax.text(leg_x + 440, ly, f"{name}\n  {corner_str}",
                color=col, fontsize=6, va="center", **FONT)

    # Title block
    title_block(ax, "SHEET 1 OF 4",
                drawing_title="MOVEABLE FILM PLANE (4-CORNER)",
                subtitle="Plan view — 4-corner rail layout",
                scale_note="Proportional (mm)",
                doc_id="TBS-FM01 · Film Plane Mechanism")

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet1.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path(f"{DIAGRAMS_DIR}/film-plane-sheet1.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet1.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — TWO ELEVATION VIEWS
# Left panel:  SIDE ELEVATION (section through container centreline)
#              X = optical axis depth, Y = height → shows TILT
# Right panel: PLAN CROSS-SECTION AT CEILING HEIGHT
#              X = container length, Y = optical axis depth → shows SWING
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():
    fig = plt.figure(figsize=(18, 11))
    fig.patch.set_facecolor(BG)

    ax_tilt  = fig.add_axes([0.03, 0.12, 0.44, 0.80])
    ax_swing = fig.add_axes([0.53, 0.12, 0.44, 0.80])
    for ax in [ax_tilt, ax_swing]:
        ax.set_facecolor(BG)
        ax.axis("off")

    # ── LEFT PANEL: SIDE ELEVATION — TILT ─────────────────────────────────────
    ax = ax_tilt
    PADX, PADY = 350, 250
    ax.set_xlim(-PADX, W + PADX)
    ax.set_ylim(-PADY, H + PADY + 80)
    ax.set_aspect("equal")

    # Container walls
    ax.add_patch(Rectangle((-WALL_T, -WALL_T), WALL_T, H+2*WALL_T,
                           fc=STRUCT2, ec=WHITE, lw=2.0, zorder=4))
    ax.add_patch(Rectangle((W, -WALL_T), WALL_T, H+2*WALL_T,
                           fc=STRUCT, ec=WHITE, lw=1.5, zorder=4))
    ax.add_patch(Rectangle((-WALL_T, -WALL_T), W+2*WALL_T, WALL_T,
                           fc=STRUCT, ec=WHITE, lw=1.5, zorder=4))
    ax.add_patch(Rectangle((-WALL_T, H), W+2*WALL_T, WALL_T,
                           fc=STRUCT, ec=WHITE, lw=1.5, zorder=4))
    ax.add_patch(Rectangle((0, 0), W, H, fc=GRID, ec="none", zorder=2))

    ax.text(-WALL_T/2-100, H/2, "PINHOLE\nWALL",
            color=WHITE, fontsize=6.5, ha="center", va="center",
            rotation=90, **FONT, zorder=5)
    ax.text(W+WALL_T/2+100, H/2, "FAR\nWALL",
            color=DIM, fontsize=6.5, ha="center", va="center",
            rotation=90, **FONT, zorder=5)

    # Rails
    RAIL_H = 28
    ax.add_patch(Rectangle((D_NEAR, 0), D_FAR-D_NEAR, RAIL_H,
                           fc=RAIL, ec=WHITE, lw=0.8, zorder=5, alpha=0.9))
    ax.text(W/2, RAIL_H/2, "FLOOR RAIL  HGR20  ×2  (BL  +  BR — independent leadscrews)",
            color=BG, fontsize=5.5, ha="center", va="center", **FONT, zorder=6)
    ax.add_patch(Rectangle((D_NEAR, H-RAIL_H), D_FAR-D_NEAR, RAIL_H,
                           fc=RAIL, ec=WHITE, lw=0.8, zorder=5, alpha=0.9))
    ax.text(W/2, H-RAIL_H/2, "CEILING RAIL  HGR20  ×2  (TL  +  TR — independent leadscrews)",
            color=BG, fontsize=5.5, ha="center", va="center", **FONT, zorder=6)

    CARRIAGE_W = 80
    CARRIAGE_H = 55
    PH_Y = H / 2

    # Tilt configs: use TL for top, BL for bottom (left-side section)
    tilt_configs = [
        ("Flat  0°",    D_FAR,  D_FAR,  C_FLAT, "-"),
        ("Tilt  31.5°", 800,    D_FAR,  C_T1,   "--"),
        ("Tilt  42.1°", D_NEAR, D_FAR,  C_T3,   ":"),
    ]

    for i, (name, d_top, d_bot, col, ls) in enumerate(tilt_configs):
        lw = 2.6 if i == 0 else 2.0
        alpha = 1.0 if i == 0 else 0.88
        zord = 10 + i

        tc_x = d_top - CARRIAGE_W/2
        tc_y = H - RAIL_H - CARRIAGE_H
        ax.add_patch(Rectangle((tc_x, tc_y), CARRIAGE_W, CARRIAGE_H,
                               fc=col, ec=WHITE, lw=0.8, alpha=0.45, zorder=zord))
        ax.text(d_top, tc_y + CARRIAGE_H/2, f"T", color=col,
                fontsize=5.5, ha="center", va="center", **FONT, zorder=zord+1)

        bc_x = d_bot - CARRIAGE_W/2
        bc_y = RAIL_H
        ax.add_patch(Rectangle((bc_x, bc_y), CARRIAGE_W, CARRIAGE_H,
                               fc=col, ec=WHITE, lw=0.8, alpha=0.45, zorder=zord))
        ax.text(d_bot, bc_y + CARRIAGE_H/2, f"B", color=col,
                fontsize=5.5, ha="center", va="center", **FONT, zorder=zord+1)

        fp_top_y = tc_y
        fp_bot_y = bc_y + CARRIAGE_H
        ax.plot([d_top, d_bot], [fp_top_y, fp_bot_y],
                color=col, lw=lw, ls=ls, alpha=alpha, zorder=zord+1,
                solid_capstyle="round")

        # Tilt angle arc — from vertical (flat) to tilt line
        if d_top != d_bot:
            theta = np.degrees(np.arctan2(abs(d_top - d_bot), fp_top_y - fp_bot_y))
            # Stagger radii so arcs don't overlap: i=1 → 200, i=2 → 350
            arc_r = 200 + (i - 1) * 150
            # Arc from 90° (vertical/flat) to 90°+theta (line tilts left)
            ax.add_patch(Arc((d_bot, fp_bot_y), arc_r*2, arc_r*2,
                             angle=0, theta1=90, theta2=90 + theta,
                             color=col, lw=1.2, alpha=0.8, zorder=zord))
            # Label at the midpoint of the arc
            mid_ang = np.radians(90 + theta / 2)
            ax.text(d_bot + (arc_r + 30) * np.cos(mid_ang),
                    fp_bot_y + (arc_r + 30) * np.sin(mid_ang),
                    f"{theta:.1f}°",
                    color=col, fontsize=7, ha="center", va="center",
                    **FONT, zorder=zord+2)

        # Label — to the left of the line at its vertical midpoint
        mid_x = (d_top + d_bot) / 2
        mid_y = (fp_top_y + fp_bot_y) / 2
        ax.text(mid_x - 80, mid_y, name,
                color=col, fontsize=6.5, va="center", ha="right", **FONT, zorder=zord+2)

    # Pinhole
    ax.add_patch(Circle((0, PH_Y), 38, fc=PINHOLE, ec=WHITE, lw=1.5, zorder=12))
    ax.add_patch(Circle((0, PH_Y), 13, fc=BG, ec=WHITE, lw=0.8, zorder=13))
    ax.text(+150, PH_Y, "PINHOLE\nØ2.17mm", color=PINHOLE,
            fontsize=7, ha="center", va="center", **FONT)

    # Focal-length arrow
    fl_y = 50
    fl_tick = 15
    ax.annotate("", xy=(D_FAR, fl_y), xytext=(0, fl_y),
                arrowprops=dict(arrowstyle="<->", color=C_FLAT, lw=1.0, mutation_scale=7))
    ax.plot([0, 0], [fl_y - fl_tick, fl_y + fl_tick], color=C_FLAT, lw=0.6)
    ax.plot([D_FAR, D_FAR], [fl_y - fl_tick, fl_y + fl_tick], color=C_FLAT, lw=0.6)
    ax.text(D_FAR/2, fl_y+35, f"FOCAL LENGTH  {W} mm  (FLAT)",
            color=C_FLAT, fontsize=7, ha="center", **FONT)

    dim_line_h(ax, 0, W, H+100, f"INTERIOR WIDTH (OPTICAL AXIS)  {W} mm",
               offset=0, col=DIM)
    dim_line_v(ax, W+210, 0, H, f"INTERIOR HEIGHT\n{H} mm", offset=20, col=DIM)
    dim_line_h(ax, D_NEAR, D_FAR, -190, f"RAIL TRAVEL  {D_FAR-D_NEAR} mm",
               offset=0, col=RAIL)
    dim_line_h(ax, 0, D_NEAR, -100, f"{D_NEAR}mm", offset=20, col=DIM, fs=6)
    dim_line_h(ax, D_FAR, W, -100, f"{W-D_FAR}mm", offset=20, col=DIM, fs=6)

    ax.text(W/2, H+255, "VIEW A — SIDE ELEVATION  (TILT)",
            color=WHITE, fontsize=9, ha="center", fontweight="bold", **FONT)
    ax.text(W/2, H+215, "Section through centreline  ·  each corner carriage moves independently",
            color=DIM, fontsize=6.5, ha="center", **FONT)

    # ── RIGHT PANEL: PLAN CROSS-SECTION — SWING ───────────────────────────────
    ax = ax_swing
    PAD2 = 300
    ax.set_xlim(-PAD2, L + PAD2)
    ax.set_ylim(-PAD2, W + 500)
    ax.set_aspect("equal")

    # Container outline (plan)
    ax.add_patch(Rectangle((0, 0), L, W, fc=GRID, ec=WHITE, lw=1.8, zorder=2))
    for x in np.arange(80, L, 457):
        ax.plot([x, x], [0, W], color=STRUCT2, lw=0.4, alpha=0.3, zorder=3)

    ax.add_patch(Rectangle((0, -WALL_T), L, WALL_T, fc=STRUCT2, ec=WHITE, lw=1.5, zorder=4))
    ax.text(L/2, -WALL_T/2-100, "PINHOLE WALL",
            color=WHITE, fontsize=7, ha="center", va="center", **FONT, zorder=5)
    ax.add_patch(Rectangle((0, W), L, WALL_T, fc=STRUCT, ec=WHITE, lw=1.0, zorder=4))
    ax.text(L/2, W+WALL_T/2+75, "FAR WALL",
            color=DIM, fontsize=7, ha="center", va="center", **FONT, zorder=5)
    for xw in [(-WALL_T, -WALL_T, WALL_T, W+2*WALL_T), (L, -WALL_T, WALL_T, W+2*WALL_T)]:
        ax.add_patch(Rectangle((xw[0], xw[1]), xw[2], xw[3],
                               fc=STRUCT, ec=WHITE, lw=1.0, zorder=4))

    # Pinhole (recentred at X=2874 on new film plane)
    ax.add_patch(Circle((PH_X_C, 0), 55, fc=PINHOLE, ec=WHITE, lw=1.5, zorder=6))
    ax.add_patch(Circle((PH_X_C, 0), 18, fc=BG, ec=WHITE, lw=1.0, zorder=7))

    # Rails (plan view — ceiling rails projected down)
    RAIL_W_P = 50
    for rx in [RAIL_X_L - RAIL_W_P//2, RAIL_X_R - RAIL_W_P//2]:
        ax.add_patch(Rectangle((rx, D_NEAR), RAIL_W_P, D_FAR-D_NEAR,
                               fc=RAIL, ec=WHITE, lw=0.9, zorder=5, alpha=0.8))
    ax.text(RAIL_X_L, D_NEAR+(D_FAR-D_NEAR)*0.5, "CEIL\nRAIL\nLEFT",
            color=BG, fontsize=5.5, ha="center", va="center", rotation=90,
            **FONT, zorder=7)
    ax.text(RAIL_X_R, D_NEAR+(D_FAR-D_NEAR)*0.5, "CEIL\nRAIL\nRIGHT",
            color=BG, fontsize=5.5, ha="center", va="center", rotation=90,
            **FONT, zorder=7)

    # Swing configs (using ceiling level: TL and TR)
    swing_configs = [
        ("Flat  0°",         D_FAR,  D_FAR,  C_FLAT, "-"),
        ("Swing  22.4°",     800,    D_FAR,  C_T2,   "-."),
        ("Swing  31.3°",     D_NEAR, D_FAR,  C_T3,   ":"),
        ("Swing  symmetric", D_NEAR, D_NEAR, C_T1,   "--"),
    ]

    for i, (name, d_L, d_R, col, ls) in enumerate(swing_configs):
        lw = 2.4 if i == 0 else 1.9
        alpha = 1.0 if i == 0 else 0.85
        zord = 8 + i

        # Film plane line at ceiling level: from (RAIL_X_L, d_L) to (RAIL_X_R, d_R)
        ax.plot([RAIL_X_L, RAIL_X_R], [d_L, d_R],
                color=col, lw=lw, ls=ls, alpha=alpha, zorder=zord+1,
                solid_capstyle="round")
        # Carriage markers
        for (rx, dy) in [(RAIL_X_L, d_L), (RAIL_X_R, d_R)]:
            ax.add_patch(Rectangle((rx-40, dy-40), 80, 80,
                                   fc=col, ec=WHITE, lw=0.7, alpha=0.5, zorder=zord))

        # Swing angle arc — from horizontal (flat) to swing line
        if d_L != d_R:
            ang = np.degrees(np.arctan2(abs(d_L - d_R), RAIL_X_R - RAIL_X_L))
            # Stagger radii: i=1 → 600, i=2 → 900
            arc_r = 600 + (i - 1) * 300
            # Arc at right rail pivot; flat line goes left (180°),
            # swing line goes left-and-down, so sweep from 180°+ang to 180°
            ax.add_patch(Arc((RAIL_X_R, D_FAR), arc_r*2, arc_r*2,
                             angle=0, theta1=180, theta2=180 + ang,
                             color=col, lw=1.2, alpha=0.8, zorder=zord))
            mid_ang = np.radians(180 + ang / 2)
            ax.text(RAIL_X_R + (arc_r + 40) * np.cos(mid_ang),
                    D_FAR + (arc_r + 40) * np.sin(mid_ang),
                    f"{ang:.1f}°",
                    color=col, fontsize=7, ha="center", va="center",
                    **FONT, zorder=zord+2)

        mid_y_sw = (d_L + d_R) / 2
        ax.text(L/2, mid_y_sw + 80,
                name, color=col, fontsize=6.5, ha="center", **FONT, zorder=zord+2)

    dim_line_h(ax, 0, L, W+180, f"INTERIOR LENGTH  {L} mm", offset=0, col=DIM, fs=7)
    dim_line_v(ax, L+230, 0, W, f"OPTICAL AXIS  {W} mm", offset=20, col=DIM, fs=7)
    dim_line_v(ax, RAIL_X_L - 120, D_NEAR, D_FAR,
               f"RAIL\nTRAVEL\n{D_FAR-D_NEAR} mm", offset=-400, col=RAIL, fs=6.5)

    ax.text(L/2, W+455, "VIEW B — CEILING CROSS-SECTION  (SWING)",
            color=WHITE, fontsize=9, ha="center", fontweight="bold", **FONT)
    ax.text(L/2, W+375, "Section at ceiling height  ·  left and right corner carriages move independently",
            color=DIM, fontsize=6.5, ha="center", **FONT)

    # Combined title
    fig.text(0.5, 0.98, "SHEET 2 — TILT ELEVATION (left)  &  SWING CROSS-SECTION (right)",
             color=WHITE, fontsize=11, ha="center", fontweight="bold", **FONT)

    # Title block (full-figure overlay for multi-subplot sheet)
    ax_tb = fig.add_axes([0, 0, 1, 1], facecolor="none")
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 2 OF 4",
                drawing_title="MOVEABLE FILM PLANE (4-CORNER)",
                subtitle="Tilt elevation & Swing cross-section",
                scale_note="Proportional (mm)",
                doc_id="TBS-FM01 · Film Plane Mechanism")

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet2.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path(f"{DIAGRAMS_DIR}/film-plane-sheet2.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet2.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — FRAME & HARDWARE DETAIL (4-corner design)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet3():
    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor(BG)

    positions = [
        (0.04, 0.52, 0.44, 0.42),  # TL — corner carriage bracket
        (0.52, 0.52, 0.44, 0.42),  # TR — rail + carriage cross-section
        (0.04, 0.10, 0.44, 0.36),  # BL — universal joint / rod-end
        (0.52, 0.10, 0.44, 0.36),  # BR — ACM panel arrangement
    ]
    axes = []
    for p in positions:
        a = fig.add_axes(p)
        a.set_facecolor(BG)
        a.axis("off")
        axes.append(a)
    ax_bracket, ax_rail, ax_joint, ax_acm = axes

    # ── TL: Corner carriage bracket assembly ──────────────────────────────────
    ax = ax_bracket
    ax.set_xlim(-100, 550); ax.set_ylim(-200, 400); ax.set_aspect("equal")

    # Rail (running into page — shown as end-on rectangle)
    rl_w = 44; rl_h = 30
    ax.add_patch(FancyBboxPatch((-rl_w/2, 0), rl_w, rl_h,
                               boxstyle="round,pad=2",
                               fc=RAIL, ec=WHITE, lw=1.5, zorder=3))
    ax.text(0, -40, "RAIL\nHGR20", color=RAIL, fontsize=6, ha="center", **FONT)

    # Carriage block (2× per corner)
    cb_w = 63; cb_h = 55
    ax.add_patch(Rectangle((-cb_w/2, rl_h-4), cb_w, cb_h,
                           fc=MECH, ec=WHITE, lw=1.5, zorder=5))
    ax.add_patch(Rectangle((-cb_w/2 + 4, rl_h + cb_h - 2), cb_w-8, cb_h*0.7,
                           fc=MECH, ec=WHITE, lw=1.0, alpha=0.6, zorder=5))
    ax.text(0, rl_h+cb_h/2, "HGH20CA\n×2 per\ncorner",
            color=BG, fontsize=5.5, ha="center", va="center", **FONT, zorder=6)

    # Corner bracket L-plate
    bk_h = 130; bk_w = 80
    ax.add_patch(Rectangle((cb_w/2, rl_h), bk_w, bk_h,
                           fc=STRUCT2, ec=WHITE, lw=1.5, zorder=6))
    # Leadscrew hole through bracket
    ax.add_patch(Circle((cb_w/2 + bk_w/2, rl_h + bk_h*0.6), 12,
                        fc=BG, ec=WHITE, lw=1.0, zorder=7))
    ax.text(cb_w/2 + bk_w/2, rl_h + bk_h*0.6,
            "ACME\nNUT", color=ANNO, fontsize=5, ha="center", va="center", **FONT)

    # Leadscrew
    ls_y0 = rl_h + bk_h*0.6
    ls_x0 = cb_w/2 + bk_w
    ax.add_patch(Rectangle((ls_x0, ls_y0 - 8), 200, 16,
                           fc=RAIL, ec=WHITE, lw=1.0, zorder=6))
    # Thread marks
    for tx in np.arange(ls_x0+10, ls_x0+200, 8):
        ax.plot([tx, tx+4], [ls_y0-8, ls_y0+8], color=BG, lw=0.7, zorder=7)
    ax.text(ls_x0 + 100, ls_y0 + 30, "3/4\"-6 ACME LEADSCREW",
            color=RAIL, fontsize=6, ha="center", **FONT)

    # Handwheel (simplified)
    hw_cx = ls_x0 + 220; hw_cy = ls_y0
    ax.add_patch(Circle((hw_cx, hw_cy), 55, fc=STRUCT, ec=WHITE, lw=1.5,
                        alpha=0.8, zorder=6))
    ax.add_patch(Circle((hw_cx, hw_cy), 8, fc=BG, ec=WHITE, lw=0.8, zorder=7))
    for ang_d in range(0, 360, 45):
        ang_r = np.radians(ang_d)
        ax.plot([hw_cx + 10*np.cos(ang_r), hw_cx + 50*np.cos(ang_r)],
                [hw_cy + 10*np.sin(ang_r), hw_cy + 50*np.sin(ang_r)],
                color=WHITE, lw=1.0, zorder=7)
    ax.text(hw_cx, hw_cy - 75, "8\" HANDWHEEL", color=DIM, fontsize=6,
            ha="center", **FONT)

    leader(ax, cb_w/2+bk_w/2, rl_h+bk_h, cb_w/2+bk_w/2, rl_h+bk_h+80,
           "CORNER\nBRACKET\n(L-PLATE)", color=STRUCT2, ha="center",
           arrow_style="-|>", font=FONT)

    ax.text(200, 370, "CORNER CARRIAGE BRACKET ASSEMBLY\n(ONE PER CORNER — 4 TOTAL)",
            color=WHITE, fontsize=8, ha="center", va="bottom", **FONT)
    ax.text(200, -100,
            "EACH CORNER: HGH20CA ×2  +  L-BRACKET  +  ACME NUT  +  3/4\"-6 LEADSCREW  +  HANDWHEEL",
            color=DIM, fontsize=6, ha="center", **FONT)

    # ── TR: HGR20 + HGH20CA cross-section ────────────────────────────────────
    ax = ax_rail
    ax.set_xlim(-200, 400); ax.set_ylim(-150, 350); ax.set_aspect("equal")

    rl_w = 44; rl_h = 30
    ax.add_patch(FancyBboxPatch((-rl_w/2, 0), rl_w, rl_h,
                               boxstyle="round,pad=2",
                               fc=RAIL, ec=WHITE, lw=1.5, zorder=3))
    for hx in [-16, 16]:
        ax.add_patch(Circle((hx, rl_h/2), 4.5, fc=BG, ec=WHITE, lw=0.8, zorder=4))
    for rx in [-12, 12]:
        ax.add_patch(Circle((rx, rl_h), 5, fc=BG, ec=WHITE, lw=0.7, zorder=4))

    cb_w = 63; cb_h = 55
    ax.add_patch(Rectangle((-cb_w/2, rl_h-5), cb_w, cb_h,
                           fc=MECH, ec=WHITE, lw=1.5, zorder=5))
    for cx_, cy_ in [(-22, rl_h+15), (22, rl_h+15), (-22, rl_h+38), (22, rl_h+38)]:
        ax.add_patch(Circle((cx_, cy_), 4, fc=BG, ec=WHITE, lw=0.7, zorder=6))

    dim_line_h(ax, -rl_w/2, rl_w/2, -50, f"{rl_w} mm", offset=0, col=DIM)
    dim_line_h(ax, -cb_w/2, cb_w/2, rl_h+cb_h+40, f"{cb_w} mm", offset=0, col=DIM)
    dim_line_v(ax, cb_w/2+60, rl_h, rl_h+cb_h, f"{cb_h} mm", offset=15, col=MECH)

    ax.text(0, rl_h+cb_h+120, "RAIL + CARRIAGE CROSS-SECTION\nHIWIN HGR20  +  HGH20CA",
            color=WHITE, fontsize=7.5, ha="center", va="bottom", **FONT)
    ax.text(0, -90,
            "LOAD: 9.7 kN dynamic  ·  4 RAILS  ·  8 CARRIAGES (2 per rail)",
            color=DIM, fontsize=6.5, ha="center", **FONT)
    ax.text(-80, rl_h/2, "HGR20\nRAIL", color=BG, fontsize=6.5,
            ha="center", va="center", rotation=90, **FONT)
    ax.text(0, rl_h+cb_h/2, "HGH20CA\nCARRIAGE", color=BG, fontsize=6.5,
            ha="center", va="center", **FONT)

    # ── BL: Universal joint / rod-end bearing detail ──────────────────────────
    ax = ax_joint
    ax.set_xlim(-200, 500); ax.set_ylim(-200, 280); ax.set_aspect("equal")

    # Bracket end
    bm_w = 100; bm_h = 80
    ax.add_patch(Rectangle((0, 0), bm_w, bm_h, fc=STRUCT2, ec=WHITE, lw=1.5, zorder=3))
    ax.add_patch(Rectangle((10, 10), bm_w-20, bm_h-20, fc=BG, ec="none", zorder=4))
    ax.text(bm_w/2, bm_h/2, "CORNER\nBRACKET", color=DIM, fontsize=5.5,
            ha="center", va="center", **FONT)

    # Rod-end bearing housing
    rod_cx = bm_w + 45
    rod_cy = bm_h / 2
    ax.add_patch(Circle((rod_cx, rod_cy), 30, fc=RAIL, ec=WHITE, lw=1.5, zorder=5))
    ax.add_patch(Circle((rod_cx, rod_cy), 18, fc=MECH, ec=WHITE, lw=1.0, zorder=6))
    ax.add_patch(Circle((rod_cx, rod_cy), 10, fc=BG, ec=WHITE, lw=0.8, zorder=7))
    # Outer race
    ax.add_patch(Circle((rod_cx, rod_cy), 25, fc="none", ec=WHITE, lw=0.5,
                        linestyle="--", zorder=6))

    # Connecting arm to film frame
    ff_w = 130
    ax.add_patch(Rectangle((rod_cx+30, rod_cy-15), ff_w, 30,
                           fc=ANNO, ec=WHITE, lw=1.0, zorder=5, alpha=0.8))
    ax.add_patch(Circle((rod_cx+30+25, rod_cy), 18, fc=BG, ec=WHITE, lw=1.0, zorder=6))
    ax.add_patch(Circle((rod_cx+30+25, rod_cy), 10, fc=MECH, ec=WHITE, lw=0.8, zorder=7))
    ax.text(rod_cx+30+25, rod_cy, "25mm\nPIN", color=DIM, fontsize=4.5,
            ha="center", va="center", **FONT)

    leader(ax, rod_cx, rod_cy+30, rod_cx - 60, rod_cy + 130,
           "ROD-END SPHERICAL\nBEARING (GIR25-DO\nor equiv.)\n±45° ANY AXIS", color=MECH, ha="center",
           arrow_style="-|>", font=FONT)

    # Annotation of freedom axes
    for angle_d in [0, 45, -45]:
        angle_r = np.radians(angle_d)
        ax.annotate("", xy=(rod_cx + 35*np.cos(angle_r), rod_cy + 35*np.sin(angle_r)),
                    xytext=(rod_cx, rod_cy),
                    arrowprops=dict(arrowstyle="-|>", color=C_T2, lw=0.8,
                                   mutation_scale=5), zorder=8)

    dim_line_h(ax, rod_cx-30, rod_cx+30, -80, "60 mm", offset=0, col=DIM)
    ax.text(200, 240, "CORNER JOINT DETAIL — BRACKET TO FILM FRAME\nROD-END SPHERICAL BEARING — ALLOWS TILT + SWING SIMULTANEOUSLY",
            color=WHITE, fontsize=7.5, ha="center", va="bottom", **FONT)
    ax.text(200, -100,
            "REPLACES SIMPLE PIN JOINT — 3-AXIS FREEDOM NEEDED FOR COMPOUND TILT+SWING",
            color=DIM, fontsize=6.5, ha="center", **FONT)

    # ── BR: ACM panel arrangement ─────────────────────────────────────────────
    ax = ax_acm
    ax.set_xlim(-100, 650); ax.set_ylim(-130, 350); ax.set_aspect("equal")

    panel_h = 200; panel_w = 250
    # Flat panel
    ax.add_patch(Rectangle((20, 50), panel_w, panel_h, fc=ANNO, ec=WHITE,
                           lw=1.5, zorder=3, alpha=0.7))
    ax.add_patch(Rectangle((20, 50), panel_w, panel_h/2, fc=DIM, ec=WHITE,
                           lw=1.0, zorder=4, alpha=0.5))
    ax.add_patch(Rectangle((20-5, 50+panel_h/2-6), panel_w+10, 12,
                           fc=RAIL, ec=WHITE, lw=1.0, zorder=5))
    ax.text(20+panel_w/2, 50+panel_h/2, "HINGE", color=BG,
            fontsize=6, ha="center", va="center", **FONT)
    ax.text(20+panel_w/2, 50+panel_h+20, "FLAT  (0°)", color=C_FLAT,
            fontsize=7.5, ha="center", **FONT)
    ax.text(20+panel_w/2, 50-20, "2× Dibond ACM  4mm",
            color=DIM, fontsize=6.5, ha="center", **FONT)
    dim_line_v(ax, 20-60, 50, 50+panel_h, f"{H} mm (schematic)", offset=-70, col=DIM)

    # Tilted panel (folded)
    t_ang = np.radians(30)
    tx0, ty0 = 400, 50
    ax.add_patch(Rectangle((tx0, ty0), panel_w*0.7, panel_h/2,
                           fc=DIM, ec=WHITE, lw=1.5, alpha=0.5, zorder=3))
    fold_len = panel_h / 2
    fold_dx = fold_len * np.sin(t_ang)
    fold_dy = fold_len * np.cos(t_ang)
    pts = np.array([[tx0, ty0+panel_h/2],
                    [tx0+panel_w*0.7, ty0+panel_h/2],
                    [tx0+panel_w*0.7+fold_dx, ty0+panel_h/2+fold_dy],
                    [tx0+fold_dx, ty0+panel_h/2+fold_dy]])
    ax.add_patch(Polygon(pts, fc=ANNO, ec=WHITE, lw=1.5, alpha=0.7, zorder=4))
    ax.add_patch(Rectangle((tx0-5, ty0+panel_h/2-6), panel_w*0.7+10, 12,
                           fc=RAIL, ec=WHITE, lw=1.0, zorder=5))
    ax.text(tx0+panel_w*0.35+fold_dx/2, ty0+panel_h/2+fold_dy/2+20,
            "30° fold", color=C_T2, fontsize=6.5, ha="center", **FONT)
    ax.text(tx0+panel_w*0.35, ty0+panel_h+fold_dy+25, "TILTED (upper folds back)",
            color=C_T2, fontsize=7.5, ha="center", **FONT)

    ax.text(260, 310, "ACM BACKING PANEL ARRANGEMENT\nHINGED AT MIDPOINT — ACCOMMODATES TILT UP TO 42°",
            color=WHITE, fontsize=7.5, ha="center", va="bottom", **FONT)
    ax.text(260, -60, "PANEL: DIBOND 4mm  ·  HINGE: 2\" ALUMINIUM PIANO HINGE  ·  FULL WIDTH",
            color=DIM, fontsize=6.5, ha="center", **FONT)

    fig.text(0.5, 0.97, "SHEET 3 — FRAME & HARDWARE DETAILS  (4-CORNER INDEPENDENT DESIGN)",
             color=WHITE, fontsize=11, ha="center", fontweight="bold", **FONT)

    # Title block (full-figure overlay for multi-subplot sheet)
    ax_tb = fig.add_axes([0, 0, 1, 1], facecolor="none")
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 3 OF 4",
                drawing_title="MOVEABLE FILM PLANE (4-CORNER)",
                subtitle="Frame & hardware details — 4-corner design",
                scale_note="As noted",
                doc_id="TBS-FM01 · Film Plane Mechanism")

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet3.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path(f"{DIAGRAMS_DIR}/film-plane-sheet3.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet3.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 4 — MOVEMENT SPECIFICATION TABLE & BOM (4-corner design)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet4():
    fig, ax = plt.subplots(figsize=(16, 13))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis("off")

    ax.text(0.5, 0.968, "SHEET 4 — MOVEMENT SPECIFICATION",
            transform=ax.transAxes, color=WHITE, fontsize=13, ha="center",
            fontweight="bold", **FONT)
    ax.text(0.5, 0.948, f"TBS-001  ·  MOVEABLE FILM PLANE (4-CORNER)  ·  RAILS: X={RAIL_X_L}–{RAIL_X_R}mm  SPAN={RAIL_X_R-RAIL_X_L}mm  MAX SWING={MAX_SWING_DEG:.1f}deg",
            transform=ax.transAxes, color=DIM, fontsize=8.5, ha="center", **FONT)

    # row_h=0.022 fits 31 rows across 3 tables in the available page height.
    # At figsize height 13in: row height = 0.022×13×72 ≈ 20.6pt — comfortable for 7pt font.
    def draw_table(ax, x0, y0, headers, rows, col_widths, row_h=0.022,
                   hdr_col=STRUCT2, row_cols=(GRID, BG)):
        total_w = sum(col_widths)
        xc = x0
        ax.add_patch(Rectangle((x0, y0), total_w, row_h*1.2,
                               transform=ax.transAxes,
                               fc=hdr_col, ec=WHITE, lw=0.8, zorder=3, clip_on=False))
        for h, cw in zip(headers, col_widths):
            ax.text(xc+cw/2, y0+row_h*0.6, h,
                    transform=ax.transAxes, color=WHITE, fontsize=7.2,
                    ha="center", va="center", fontweight="bold", **FONT)
            xc += cw
        for ri, row in enumerate(rows):
            ry = y0 - (ri+1)*row_h
            fc = row_cols[ri % 2]
            ax.add_patch(Rectangle((x0, ry), total_w, row_h,
                                   transform=ax.transAxes,
                                   fc=fc, ec=GRID, lw=0.5, zorder=2, clip_on=False))
            xc = x0
            for cell, cw in zip(row, col_widths):
                col_text = WHITE if ri == 0 else ANNO
                ax.text(xc+cw/2, ry+row_h*0.5, str(cell),
                        transform=ax.transAxes, color=col_text, fontsize=6.8,
                        ha="center", va="center", **FONT)
                xc += cw

    # ── Table 1: Axis movement summary ────────────────────────────────────────
    # label sits 0.012 above header top: label_y = y0 + row_h*1.2 + 0.012
    # y0=0.895 → header top=0.895+0.026=0.921 → label at 0.933
    ax.text(0.05, 0.933, "TABLE 1 — MOVEMENT AXES  (4-CORNER INDEPENDENT DESIGN)",
            transform=ax.transAxes, color=DIM, fontsize=8, fontweight="bold", **FONT)

    axes_headers = ["AXIS", "DESCRIPTION", "CORNERS\nCONTROLLED", "MAX TRAVEL", "ACTUATOR", "LOCK"]
    axes_rows = [
        ["TILT (top)",    "Both top corners move equally",      "TL + TR together", "0–2,262 mm", "2× leadscrew — turn both", "2 locking collars"],
        ["TILT (bottom)", "Both bottom corners move equally",   "BL + BR together", "0–2,262 mm", "2× leadscrew — turn both", "2 locking collars"],
        ["SWING (left)",  "Both left corners move equally",     "TL + BL together", "0–2,262 mm", "2× leadscrew — turn both", "2 locking collars"],
        ["SWING (right)", "Both right corners move equally",    "TR + BR together", "0–2,262 mm", "2× leadscrew — turn both", "2 locking collars"],
        ["COMPOUND",      "Any/all 4 corners independently",   "TL, TR, BL, BR",   "0–2,262 mm", "4× leadscrews independently","4 locking collars"],
        ["BACK FOCUS",    "All 4 corners together",             "All",              "100–2,262mm","All 4 leadscrews together", "All 4 locks"],
        ["MAX TILT",      "Top=100mm, Bot=2,262mm (or rev.)",  "TL=TR, BL=BR",     f"{MAX_TILT_DEG:.1f}deg",  "Top+top / Bot+bot",        "All 4 locks"],
        ["MAX SWING",     "Left=100mm, Right=2,262mm (or rev.)","TL=BL, TR=BR",    f"{MAX_SWING_DEG:.1f}deg", "Left+left / Right+right",  "All 4 locks"],
    ]
    # y0=0.895; header top=0.895+0.026=0.921; bottom=0.895-8×0.022=0.719
    draw_table(ax, 0.05, 0.895, axes_headers, axes_rows,
               [0.12, 0.22, 0.15, 0.10, 0.22, 0.14])

    # ── Table 2: Config specs ─────────────────────────────────────────────────
    # T1 bottom=0.719; gap=0.025; label=0.694; y0=0.656; bottom=0.656-8×0.022=0.480
    ax.text(0.05, 0.694, "TABLE 2 — EXAMPLE TILT/SWING CONFIGURATION SPECS",
            transform=ax.transAxes, color=DIM, fontsize=8, fontweight="bold", **FONT)

    def tilt_angle(d_a, d_b, span):
        return np.degrees(np.arctan2(abs(d_a-d_b), span))

    def film_len(d_a, d_b, span):
        return round(np.sqrt((d_a-d_b)**2 + span**2))

    eff_H = H - 120

    config_defs = [
        ("Flat",              D_FAR,  D_FAR,  D_FAR,  D_FAR,  "Reference"),
        ("Tilt mild",         1800,   1800,   D_FAR,  D_FAR,  "5.6° tilt, subtle keystone"),
        ("Tilt strong",       800,    800,    D_FAR,  D_FAR,  "31.5° tilt, strong keystone"),
        ("Tilt max",          D_NEAR, D_NEAR, D_FAR,  D_FAR,  "42.1° tilt, extreme"),
        ("Swing mild",        D_FAR,  1800,   D_FAR,  1800,   "swing, diagonal slant"),
        ("Swing strong",      D_FAR,  800,    D_FAR,  800,    "swing (short span = larger angle)"),
        ("Swing max",         D_FAR,  D_NEAR, D_FAR,  D_NEAR, f"{MAX_SWING_DEG:.1f}deg max swing"),
        ("Compound tilt+sw.", D_NEAR, D_FAR,  D_FAR,  D_NEAR, "Both max — twisted plane"),
    ]

    cfg_headers = ["CONFIG", "TL mm", "TR mm", "BL mm", "BR mm",
                   "TILT ANG.", "SWING ANG.", "PRINCIPAL EFFECT"]
    cfg_rows = []
    for (name, d_TL, d_TR, d_BL, d_BR, effect) in config_defs:
        tilt = tilt_angle(d_TL, d_BL, eff_H)  # top vs bottom on same side
        swing = tilt_angle(d_TL, d_TR, RAIL_X_R - RAIL_X_L)  # left vs right — use rail span
        cfg_rows.append([name, d_TL, d_TR, d_BL, d_BR,
                         f"{tilt:.1f}°", f"{swing:.1f}°", effect])

    draw_table(ax, 0.05, 0.656, cfg_headers, cfg_rows,
               [0.13, 0.07, 0.07, 0.07, 0.07, 0.08, 0.09, 0.37])

    # BOM removed — consolidated to master-shopping-list.md §4
    ax.text(0.50, 0.35,
            "Bill of materials: master-shopping-list.md — §4 Film Plane Mechanism",
            transform=ax.transAxes, color=DIM, fontsize=7,
            ha="center", va="center", style="italic", **FONT)

    # Title block
    title_block(ax, "SHEET 4 OF 4",
                drawing_title="MOVEABLE FILM PLANE (4-CORNER)",
                subtitle="Movement specification & BOM",
                scale_note="Not to scale",
                doc_id="TBS-FM01 · Film Plane Mechanism")

    fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheet4.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path(f"{DIAGRAMS_DIR}/film-plane-sheet4.png"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  → {DIAGRAMS_DIR}/film-plane-sheet4.png")


# ── Run all sheets ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os; os.makedirs(SVG_DIR, exist_ok=True)
    print("Generating film plane mechanism drawings (4-corner design)...")
    sheet1()
    sheet2()
    sheet3()
    sheet4()
    print("Done.")
