#!/usr/bin/env python3
"""
generate_floorplan_diagram.py  —  TBS-001 Container Floor Plan

Top-down schematic of the full container interior, showing all systems
in their real positions with space constraints respected.

Coordinate system (all mm):
  X = 0 → 5893  (container interior length — long axis)
           X=0: cargo door short end (hinged panel, equipment cluster)
           X=5893: sealed short end
  Y = 0 → 2362  (container interior width = optical axis depth)
           Y=0:    pinhole long wall
           Y=2362: far long wall (image plane / film fabric)

Equipment layout — "pinhole wall colonnade":
  All equipment within Y=0–1220mm of the pinhole wall.
  Two wings flank the pinhole in X: LEFT (X=0–2380) and RIGHT (X=3900–5893).
  Central zone X=2380–3900 is clear at all depths.
  Optical clear zone: Y=1220–2362mm (full container width).
Image plane (muslin): at Y≈2262, spanning full X.
Development/washing area shown OUTSIDE container (below Y=0 long wall).
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Polygon
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe
import matplotlib.patches

# ── Palette ───────────────────────────────────────────────────────────────────
BG       = "#FFFFFF"
C_OUT    = "#1A1A1A"   # outlines / main text
C_DIM    = "#404040"   # dimension lines + labels
C_WALL   = "#B0B0B8"   # container wall fill (steel)
C_FLOOR  = "#F0F4F8"   # container interior floor
C_RAIL   = "#5A3E00"   # floor/ceiling rails
C_FILM   = "#2060A0"   # image plane / film fabric line (blue)
C_PINHOLE= "#CC6600"   # pinhole (orange)
C_OPT    = "#2060A0"   # optical axis arrow

# Equipment colours
C_BLUE_IBC = "#4A7CB0"   # Blue IBC totes (wash water)
C_BROWN_IBC= "#8B5E3C"   # Brown IBC tote (fix/waste)
C_DRUM     = "#607060"   # 55-gal HDPE drums
C_COOLER   = "#40A090"   # evaporative cooler
C_PUMP     = "#A04040"   # pump manifold
C_ELEC     = "#806010"   # electrical enclosure

C_EQUIP_ZONE = "#FFF8EE"  # equipment zone highlight
C_OPT_ZONE   = "#F0F8F0"  # optical clear zone highlight
C_DEV_ZONE   = "#F0F0FF"  # development area (outside)

FONT = {"fontfamily": "monospace"}

# ── Container dimensions (mm) ─────────────────────────────────────────────────
L     = 5893   # interior length (X axis)
W     = 2362   # interior width  (Y axis) = focal length = optical axis
WALL  = 40     # wall thickness (shown in cross-section)

D_FAR  = W - 100   # film plane position (muslin) = 2262mm from pinhole wall
PINHOLE_X = L / 2  # pinhole centred on long wall (X = 2946.5mm)

COLONNADE_Y = 1220  # equipment depth limit (Y from pinhole wall) — colonnade layout

# ── Equipment footprints — PINHOLE WALL COLONNADE (all mm, X=0 cargo door end) ─
# All equipment within Y=0–1220mm of the pinhole wall (Y=0).
# Optical cone is narrow near Y=0; equipment clears the cone at these positions.
# Cone left  boundary at depth Y: X_left(Y)  = PINHOLE_X*(1 - Y/D_FAR)
# Cone right boundary at depth Y: X_right(Y) = PINHOLE_X + (L-PINHOLE_X)*(Y/D_FAR)

IBC_S = 1016   # IBC short footprint dim (Y direction)
IBC_L = 1219   # IBC long footprint dim  (X direction)
# 600L IBC: same footprint, h=1010mm. Two stacked: 2020mm (368mm ceiling clearance).

# ── LEFT WING (X=0–2380mm, Y=0–1220mm) ───────────────────────────────────────
# Blue IBCs ×2 stacked (600L each): X=100–1319, Y=100–1116.
#   Cone left at Y=1116: X_left=1494mm. Right edge 1319mm < 1494mm ✓ CLEAR.
BLUE_STACK = dict(x=100, y=100, w=IBC_L, h=IBC_S, label="BLUE IBC ×2\n(STACKED)\n2×600L", col=C_BLUE_IBC)

# Evap cooler: X=1380–1980, Y=100–450.
#   Cone left at Y=450: X_left=2360mm. Right edge 1980mm < 2360mm ✓ CLEAR.
COOLER = dict(x=1380, y=100, w=600, h=350, label="EVAP\nCOOLER", col=C_COOLER)

# Pump manifold: X=1980–2380, Y=100–400.
#   Cone left at Y=400: X_left=2424mm. Right edge 2380mm < 2424mm ✓ CLEAR.
PUMP = dict(x=1980, y=100, w=400, h=300, label="PUMP\nMANIFOLD", col=C_PUMP)

# Electrical enclosure + battery bank — mounted ON pinhole wall face (Y=0–80).
ELEC = dict(x=2050, y=0, w=300, h=80, label="ELEC +\nBATT.", col=C_ELEC)

# ── RIGHT WING (X=3900–5893mm, Y=0–1220mm) ───────────────────────────────────
# 55-gal drums ×2 stacked: X=3900–4480, Y=100–680.
#   Cone right at Y=680: X_right=3831mm. Left edge 3900mm > 3831mm ✓ CLEAR.
DRUM_STACK = dict(x=3900, y=100, w=580, h=580, label="55gal DRUM\n×2 STACKED", col=C_DRUM)

# Brown IBC ×1 (600L): X=4674–5893, Y=100–1116.
#   Cone right at Y=1116: X_right=4400mm. Left edge 4674mm > 4400mm ✓ CLEAR.
BROWN = dict(x=4674, y=100, w=IBC_L, h=IBC_S, label="BROWN IBC\n×1\n600L", col=C_BROWN_IBC)


# ── Helpers ───────────────────────────────────────────────────────────────────
def dim_h(ax, x0, x1, y, label, offset=80, fs=6.5, col=C_DIM):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9, mutation_scale=7))
    ax.text((x0 + x1) / 2, y + offset, label, color=col, fontsize=fs,
            ha="center", va="bottom", **FONT)

def dim_v(ax, x, y0, y1, label, offset=80, fs=6.5, col=C_DIM):
    ax.annotate("", xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9, mutation_scale=7))
    ax.text(x + offset, (y0 + y1) / 2, label, color=col, fontsize=fs,
            ha="left", va="center", **FONT)

def draw_equip_rect(ax, d, alpha=0.85, zorder=6):
    """Draw a rectangular equipment piece with label."""
    ax.add_patch(Rectangle((d["x"], d["y"]), d["w"], d["h"],
                            fc=d["col"], ec=C_OUT, lw=1.2,
                            alpha=alpha, zorder=zorder))
    cx = d["x"] + d["w"] / 2
    cy = d["y"] + d["h"] / 2
    ax.text(cx, cy, d["label"], color=BG, fontsize=6, ha="center", va="center",
            **FONT, fontweight="bold", zorder=zorder + 1)

def draw_equip_circle(ax, d, alpha=0.85, zorder=6):
    """Draw a circular equipment piece with label."""
    ax.add_patch(Circle((d["cx"], d["cy"]), d["r"],
                         fc=d["col"], ec=C_OUT, lw=1.2,
                         alpha=alpha, zorder=zorder))
    ax.text(d["cx"], d["cy"], d["label"], color=BG, fontsize=6,
            ha="center", va="center", **FONT, fontweight="bold", zorder=zorder + 1)

def penetration(ax, x, y, r=60, col=C_OUT, label="", label_offset=(0, 80)):
    """Draw a wall penetration (circle with cross)."""
    ax.add_patch(Circle((x, y), r, fc="#FFE0A0", ec=col, lw=1.5, zorder=8))
    ax.plot([x - r, x + r], [y, y], color=col, lw=0.8, zorder=9)
    ax.plot([x, x], [y - r, y + r], color=col, lw=0.8, zorder=9)
    if label:
        ax.text(x + label_offset[0], y + label_offset[1],
                label, color=col, fontsize=6, ha="center", va="bottom",
                **FONT, zorder=9)

def title_block(ax):
    ax.text(0.01, 0.022, "THE BIG SHOEBOX PROJECT  ·  TBS-001",
            transform=ax.transAxes, color=C_DIM, fontsize=7, **FONT)
    ax.text(0.01, 0.010, "CONTAINER FLOOR PLAN — PINHOLE WALL COLONNADE LAYOUT (TOP-DOWN VIEW)",
            transform=ax.transAxes, color=C_OUT, fontsize=8, fontweight="bold", **FONT)
    ax.text(0.99, 0.022, "SCALE 1:75 (APPROX)  ·  SHEET 1 OF 1",
            transform=ax.transAxes, color=C_DIM, fontsize=7, ha="right", **FONT)
    ax.text(0.99, 0.010, "ALL DIMS IN mm",
            transform=ax.transAxes, color=C_DIM, fontsize=7, ha="right", **FONT)


# ═══════════════════════════════════════════════════════════════════════════════
# FLOOR PLAN
# ═══════════════════════════════════════════════════════════════════════════════
def floor_plan():
    fig, ax = plt.subplots(figsize=(22, 10))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    # Drawing bounds: include dev area (below Y=0) and margins
    DEV_DEPTH = 700   # development area depth below container (outside Y=0 wall)
    PAD_L = 600; PAD_R = 500; PAD_B = DEV_DEPTH + 200; PAD_T = 500

    ax.set_xlim(-PAD_L, L + PAD_R)
    ax.set_ylim(-PAD_B, W + PAD_T)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Zone highlights — PINHOLE WALL COLONNADE layout ───────────────────────
    # Equipment wing zone (Y=0 to COLONNADE_Y) — shallow strip near pinhole wall
    ax.add_patch(Rectangle((0, 0), L, COLONNADE_Y,
                            fc=C_EQUIP_ZONE, ec="none", zorder=1))
    ax.text(L / 2, COLONNADE_Y / 2, "EQUIPMENT COLONNADE  (Y = 0–1220mm, PINHOLE WALL SIDE)",
            color="#C0A060", fontsize=8, ha="center", va="center",
            **FONT, alpha=0.6, fontweight="bold", zorder=2)

    # Optical clear zone (Y=COLONNADE_Y to D_FAR)
    ax.add_patch(Rectangle((0, COLONNADE_Y), L, D_FAR - COLONNADE_Y,
                            fc=C_OPT_ZONE, ec="none", zorder=1))
    ax.text(L / 2, COLONNADE_Y + (D_FAR - COLONNADE_Y) / 2,
            "OPTICAL CLEAR ZONE  (Y = 1220–2262mm)",
            color="#4A8040", fontsize=8, ha="center", va="center",
            **FONT, alpha=0.5, fontweight="bold", zorder=2)

    # Colonnade depth boundary line
    ax.plot([0, L], [COLONNADE_Y, COLONNADE_Y],
            color="#C08040", lw=1.5, ls="--", zorder=4, alpha=0.9)
    ax.text(L + 30, COLONNADE_Y, f"COLONNADE LIMIT\nY={COLONNADE_Y}mm",
            color="#C08040", fontsize=6.5, ha="left", va="center", **FONT)

    # ── Optical cone boundary lines (plan view) ───────────────────────────────
    # Left ray: pinhole (PINHOLE_X, 0) → left-wall corner (0, D_FAR)
    ax.plot([PINHOLE_X, 0], [0, D_FAR],
            color="#C07000", lw=1.0, ls=(0, (4, 3)), zorder=4, alpha=0.7)
    # Right ray: pinhole (PINHOLE_X, 0) → right-wall corner (L, D_FAR)
    ax.plot([PINHOLE_X, L], [0, D_FAR],
            color="#C07000", lw=1.0, ls=(0, (4, 3)), zorder=4, alpha=0.7)
    ax.text(PINHOLE_X - 200, D_FAR * 0.55, "OPTICAL CONE\n(dashed boundary)",
            color="#C07000", fontsize=6, ha="right", va="center", **FONT, alpha=0.8)

    # ── Container interior floor ───────────────────────────────────────────────
    ax.add_patch(Rectangle((0, 0), L, W,
                            fc="none", ec=C_OUT, lw=2.5, zorder=3))

    # ── Container walls (shown as thick rectangles) ────────────────────────────
    # Pinhole long wall (Y=0, bottom)
    ax.add_patch(Rectangle((-WALL, -WALL), L + 2 * WALL, WALL,
                            fc=C_WALL, ec=C_OUT, lw=1.5, zorder=3))
    # Far long wall (Y=W, top)
    ax.add_patch(Rectangle((-WALL, W), L + 2 * WALL, WALL,
                            fc=C_WALL, ec=C_OUT, lw=1.5, zorder=3))
    # Left short end wall (X=0, cargo door)
    ax.add_patch(Rectangle((-WALL, -WALL), WALL, W + 2 * WALL,
                            fc=C_WALL, ec=C_OUT, lw=1.5, zorder=3))
    # Right short end wall (X=L, sealed)
    ax.add_patch(Rectangle((L, -WALL), WALL, W + 2 * WALL,
                            fc=C_WALL, ec=C_OUT, lw=1.5, zorder=3))

    # ── Wall labels ────────────────────────────────────────────────────────────
    ax.text(L / 2, -WALL / 2, "PINHOLE WALL  (20ft LONG SIDE)",
            color=C_OUT, fontsize=7, ha="center", va="center", **FONT, zorder=4)
    ax.text(L / 2, W + WALL / 2, "FAR WALL — IMAGE PLANE SIDE  (20ft LONG SIDE)",
            color=C_OUT, fontsize=7, ha="center", va="center", **FONT, zorder=4)
    ax.text(-WALL / 2, W / 2, "CARGO\nDOOR\nEND", color=C_OUT, fontsize=6,
            ha="center", va="center", **FONT, rotation=90, zorder=4)
    ax.text(L + WALL / 2, W / 2, "SEALED\nEND", color=C_OUT, fontsize=6,
            ha="center", va="center", **FONT, rotation=90, zorder=4)

    # ── Structural ribs on walls (every 600mm) ─────────────────────────────────
    for x_rib in np.arange(200, L, 600):
        ax.plot([x_rib, x_rib], [0, W], color=C_WALL, lw=0.4, alpha=0.4, zorder=2)

    # ── Film plane rails (ceiling + floor, full length) ────────────────────────
    RAIL_W = 35
    for rail_y in [D_FAR - RAIL_W // 2, D_FAR + RAIL_W // 2]:
        ax.plot([0, L], [rail_y, rail_y],
                color=C_RAIL, lw=2.0, zorder=4)
    ax.text(L + 120, D_FAR, "FILM PLANE\nRAILS", color=C_RAIL,
            fontsize=6.5, ha="left", va="center", **FONT)

    # ── Film fabric / muslin (image plane) ────────────────────────────────────
    ax.plot([0, L], [D_FAR, D_FAR], color=C_FILM, lw=3.5, zorder=5, alpha=0.9)
    # Hatching to indicate fabric (short dashes)
    for hx in np.arange(200, L, 300):
        ax.plot([hx, hx + 80], [D_FAR, D_FAR], color=C_FILM, lw=1.5, zorder=5, alpha=0.5)

    ax.text(200, D_FAR + 120,
            f"COTTON MUSLIN IMAGE PLANE  (Y = {D_FAR}mm)",
            color=C_FILM, fontsize=7, ha="left", va="bottom", **FONT)

    # ── Pinhole ────────────────────────────────────────────────────────────────
    penetration(ax, PINHOLE_X, 0, r=80, col=C_PINHOLE, label="PINHOLE\nØ2.17mm",
                label_offset=(0, -160))

    # ── Optical axis arrow (pinhole → image plane) ────────────────────────────
    ax.annotate("", xy=(PINHOLE_X, D_FAR - 40),
                xytext=(PINHOLE_X, 80),
                arrowprops=dict(arrowstyle="->", color=C_OPT, lw=1.5,
                                mutation_scale=10, ls="--"))
    ax.text(PINHOLE_X + 80, W / 2, f"OPTICAL AXIS\n{W}mm",
            color=C_OPT, fontsize=7, ha="left", va="center", **FONT)

    # ── No-go zone annotation (central forbidden band near pinhole) ──────────
    # At COLONNADE_Y depth, cone spans X_left to X_right — mark this in dim line
    x_left_col = PINHOLE_X * (1 - COLONNADE_Y / D_FAR)   # ≈ 1494mm
    x_right_col = PINHOLE_X + (L - PINHOLE_X) * (COLONNADE_Y / D_FAR)  # ≈ 4398mm
    ax.annotate("", xy=(x_right_col, COLONNADE_Y + 60),
                xytext=(x_left_col, COLONNADE_Y + 60),
                arrowprops=dict(arrowstyle="<->", color="#C07000", lw=0.8, mutation_scale=7))
    ax.text((x_left_col + x_right_col) / 2, COLONNADE_Y + 140,
            f"CONE WIDTH AT Y={COLONNADE_Y}mm\n({int(x_right_col - x_left_col)}mm — NO EQUIP. AT THIS DEPTH)",
            color="#C07000", fontsize=6, ha="center", va="bottom", **FONT)

    # ── Hinged panel (at X=0 short wall) ─────────────────────────────────────
    # Closed position: panel is against X=0 wall (shown as thicker left wall)
    # Open position (ghost): panel swings 180° outward, shown as dashed line at X<0
    PANEL_W = W   # panel width = container interior width
    PANEL_T = 120

    # Ghost of open panel position (parallel to Y=0 or Y=W long wall)
    ax.add_patch(Rectangle((-WALL - PANEL_T - 200, 0), PANEL_T, PANEL_W,
                            fc="none", ec=C_DIM, lw=1.0, ls=(0, (6, 4)),
                            zorder=4, alpha=0.6))
    ax.text(-WALL - PANEL_T / 2 - 200, W / 2, "PANEL\n(OPEN)",
            color=C_DIM, fontsize=6, ha="center", va="center",
            **FONT, rotation=90, alpha=0.6, zorder=5)

    # Swing arc (180° open)
    swing_arc = matplotlib.patches.Arc(
        (-WALL, W / 2), 2 * (PANEL_T + 200), 2 * (PANEL_T + 200),
        angle=0, theta1=180, theta2=360,
        color=C_DIM, lw=0.9, ls=(0, (4, 3)), zorder=4, alpha=0.6)
    ax.add_patch(swing_arc)

    # Drum symbol on left wall (closed panel)
    DRUM_SYM_R = 100
    penetration(ax, -WALL / 2, W / 2, r=DRUM_SYM_R,
                col=C_PINHOLE, label="DRUM\nINLET",
                label_offset=(-260, 0))
    ax.text(-WALL - 350, W / 2,
            "HINGED PANEL\n+ REVOLVING\nDRUM INLET",
            color=C_PINHOLE, fontsize=6.5, ha="right", va="center",
            **FONT, zorder=5)

    # ── Wall penetrations ─────────────────────────────────────────────────────
    # Cooler intake duct — moved to pinhole wall (Y=0), X aligned with new cooler position
    penetration(ax, 1680, 0, r=75, col=C_COOLER, label="COOLER\nINTAKE",
                label_offset=(0, -110))
    # Fan intake (left short wall, low position)
    penetration(ax, 0, 300, r=55, col=C_DIM, label="FAN IN\n(LOW)",
                label_offset=(-140, 0))
    # Fan exhaust (right short wall, high position)
    penetration(ax, L, 2000, r=55, col=C_DIM, label="FAN OUT\n(HIGH)",
                label_offset=(140, 0))

    # ── Equipment — PINHOLE WALL COLONNADE ────────────────────────────────────
    draw_equip_rect(ax, BLUE_STACK, zorder=6)
    draw_equip_rect(ax, COOLER,     zorder=6)
    draw_equip_rect(ax, PUMP,       zorder=6)
    draw_equip_rect(ax, ELEC,       zorder=7)   # wall-mounted (thin strip)
    draw_equip_rect(ax, DRUM_STACK, zorder=6)
    draw_equip_rect(ax, BROWN,      zorder=6)
    # Stacking annotations
    ax.text(BLUE_STACK["x"] + BLUE_STACK["w"] / 2,
            BLUE_STACK["y"] + BLUE_STACK["h"] + 60,
            "▲ 2020mm tall (stacked)", color=C_BLUE_IBC, fontsize=5.5,
            ha="center", va="bottom", **FONT, zorder=7)
    ax.text(DRUM_STACK["x"] + DRUM_STACK["w"] / 2,
            DRUM_STACK["y"] + DRUM_STACK["h"] + 60,
            "▲ 1740mm tall (stacked)", color=C_DRUM, fontsize=5.5,
            ha="center", va="bottom", **FONT, zorder=7)

    # ── Development / washing area (OUTSIDE container, below Y=0 wall) ────────
    DEV_X0 = 800; DEV_X1 = 4500; DEV_Y0 = -DEV_DEPTH; DEV_Y1 = -WALL - 60
    ax.add_patch(Rectangle((DEV_X0, DEV_Y0), DEV_X1 - DEV_X0, DEV_Y1 - DEV_Y0,
                            fc=C_DEV_ZONE, ec=C_DIM, lw=1.5, ls=(0, (5, 3)),
                            zorder=2))
    # Hatching
    for hx in np.arange(DEV_X0, DEV_X1, 250):
        ax.plot([hx, hx + 200], [DEV_Y0, DEV_Y1], color=C_DIM, lw=0.4, alpha=0.3, zorder=3)
    ax.text((DEV_X0 + DEV_X1) / 2, (DEV_Y0 + DEV_Y1) / 2,
            "DEVELOPMENT AREA  (OUTSIDE — IN FRONT OF PINHOLE WALL)\n"
            "Fabric lowered from image plane to floor-level trough for water wash.\n"
            "Three-circuit water system drains to grey-water IBC inside container.",
            color=C_DIM, fontsize=7, ha="center", va="center", **FONT, zorder=4)

    # Arrow: fabric travels from image plane out through pinhole wall
    ax.annotate("", xy=(L / 3, DEV_Y1 + 10),
                xytext=(L / 3, 0),
                arrowprops=dict(arrowstyle="->", color=C_DIM, lw=1.0,
                                mutation_scale=8, ls="--", alpha=0.7))

    # ── Dimension annotations ─────────────────────────────────────────────────
    # Container length
    dim_h(ax, 0, L, W + 300, f"{L} mm  ({L/304.8:.1f}ft)  INTERIOR LENGTH")
    # Container width (= focal length)
    dim_v(ax, L + 200, 0, W, f"{W} mm\nINTERIOR\nWIDTH\n(= FOCAL LENGTH)", offset=55)
    # Equipment colonnade depth
    dim_v(ax, -PAD_L + 100, 0, COLONNADE_Y, f"{COLONNADE_Y}mm", offset=55)
    ax.text(-PAD_L + 100 + 60, COLONNADE_Y / 2, "EQUIPMENT\nCOLONNADE\nDEPTH",
            color="#C08040", fontsize=6.5, ha="left", va="center", **FONT)
    # Optical clear zone depth
    dim_v(ax, -PAD_L + 100, COLONNADE_Y, D_FAR, f"{D_FAR - COLONNADE_Y}mm", offset=55)
    ax.text(-PAD_L + 100 + 60, COLONNADE_Y + (D_FAR - COLONNADE_Y) / 2,
            "OPTICAL\nCLEAR\nDEPTH",
            color="#4A8040", fontsize=6.5, ha="left", va="center", **FONT)
    # Film plane position
    dim_v(ax, -PAD_L + 100, 0, D_FAR, f"", offset=55)
    ax.text(-PAD_L + 100 + 60, D_FAR - 80, "FILM PLANE\nY=2262mm",
            color=C_DIM, fontsize=6.5, ha="left", va="top", **FONT)

    # ── Legend ────────────────────────────────────────────────────────────────
    LEG_X = L + 60; LEG_Y_TOP = W - 20
    legend_items = [
        (C_BLUE_IBC, "Blue IBC totes ×2 stacked (2×600L = 1,200L) — LEFT WING"),
        (C_BROWN_IBC,"Brown IBC tote ×1 (600L) — RIGHT WING"),
        (C_DRUM,     "55-gal HDPE drums ×2 stacked (2×208L) — RIGHT WING"),
        (C_COOLER,   "12V evaporative cooler — LEFT WING"),
        (C_PUMP,     "Pump manifold — LEFT WING"),
        (C_ELEC,     "Electrical enclosure + LiFePO4 battery (pinhole wall, wall-mount)"),
        (C_FILM,     "Cotton muslin image plane (Y = 2262mm)"),
        (C_PINHOLE,  "Pinhole Ø2.17mm (centred on long wall)"),
        (C_OPT,      "Optical axis (2362mm focal length)"),
        (C_PINHOLE,  "Revolving light-trap drum inlet"),
        (C_DEV_ZONE, "Development area (outside container)"),
    ]
    box_w = PAD_R - 60; box_h = len(legend_items) * 52 + 40
    ax.add_patch(Rectangle((LEG_X, LEG_Y_TOP - box_h), box_w, box_h,
                            fc="#FAFAFA", ec=C_DIM, lw=0.8, zorder=8))
    ax.text(LEG_X + box_w / 2, LEG_Y_TOP - 12, "LEGEND",
            color=C_OUT, fontsize=7.5, ha="center", va="center", fontweight="bold",
            **FONT, zorder=9)
    for i, (col, txt) in enumerate(legend_items):
        iy = LEG_Y_TOP - 50 - i * 52
        ax.add_patch(Rectangle((LEG_X + 12, iy - 16), 36, 32,
                                fc=col, ec=C_OUT, lw=0.8, zorder=9, alpha=0.9))
        ax.text(LEG_X + 58, iy, txt, color=C_DIM, fontsize=6,
                ha="left", va="center", **FONT, zorder=9)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax)

    fig.savefig("container-floorplan.png", dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  container-floorplan.png saved")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import matplotlib
    print("Generating container floor plan...")
    floor_plan()
    print("Done.")
