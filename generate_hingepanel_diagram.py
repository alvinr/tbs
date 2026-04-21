#!/usr/bin/env python3
"""
generate_hingepanel_diagram.py  —  TBS-001 Hinged Light-Trap Panel

Sheet 1 — Front elevation (exterior view, 1:20):
  Panel dimensions, revolving drum position, hinges, latches, EPDM perimeter seal.

Sheet 2 — Plan cross-section (1:10 horizontal / 1:1 depth — depth exaggerated):
  Panel thickness, drum cross-section with 4 baffles, S-path light route,
  container wall interface, EPDM gasket engagement, latch detail.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Arc, Polygon
from matplotlib.lines import Line2D

# ── Palette (white engineering) ───────────────────────────────────────────────
BG      = "#FFFFFF"   # white background
C_OUT   = "#1A1A1A"   # outlines
C_CL    = "#2060A0"   # centre lines (blue, dashed)
C_DIM   = "#404040"   # dimensions / annotation text
C_ALUM  = "#C8D8E8"   # aluminium / ply fill
C_STEEL = "#B0B0B8"   # steel section fill
C_GASKT = "#5A3020"   # EPDM gasket fill
C_LIGHT = "#FFE0A0"   # light-path indication (amber)
FONT    = {"fontfamily": "monospace"}

# ── Panel dimensions (mm) ─────────────────────────────────────────────────────
PW = 2362   # panel width  (= container interior short-axis width)
PH = 2388   # panel height (= container interior height)
PT = 120    # panel overall thickness (50×50 RHS frame + 18mm ply each face)

# Drum
DRUM_D  = 750          # drum outer diameter (mm)
DRUM_R  = DRUM_D / 2  # = 375 mm
DRUM_H  = 2000         # drum height (floor → top bearing, mm)
DRUM_CX = PW / 2       # drum centre X in panel (centred horizontally)
DRUM_CY = DRUM_H / 2  # drum centre Y = 1000 mm from floor

# ── Drawing helpers ───────────────────────────────────────────────────────────
def dim_h(ax, x0, x1, y, label, offset=70, fs=7, col=C_DIM):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9, mutation_scale=7))
    ax.text((x0 + x1) / 2, y + offset, label, color=col, fontsize=fs,
            ha="center", va="bottom", **FONT)

def dim_v(ax, x, y0, y1, label, offset=70, fs=7, col=C_DIM):
    ax.annotate("", xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9, mutation_scale=7))
    ax.text(x + offset, (y0 + y1) / 2, label, color=col, fontsize=fs,
            ha="left", va="center", **FONT)

def leader(ax, xy, xytext, text, col=C_DIM, fs=6.5):
    ax.annotate(text, xy=xy, xytext=xytext, color=col, fontsize=fs,
                ha="center", va="center", **FONT,
                arrowprops=dict(arrowstyle="-|>", color=col, lw=0.8, mutation_scale=6))

def hatch_rect(ax, x, y, w, h, col, angle=45, lw=0.6, alpha=0.7, zorder=3):
    rect = Rectangle((x, y), w, h, fc=col, ec=C_OUT, lw=0.8, zorder=zorder)
    ax.add_patch(rect)
    # Cross-hatch lines
    step = max(w, h) / 12
    for i in np.arange(-max(w, h), max(w, h), step):
        if angle == 45:
            ax.plot([x + i, x + i + h], [y + h, y], color=C_OUT,
                    lw=lw, alpha=alpha, clip_on=True, zorder=zorder + 1)
        else:
            ax.plot([x + i, x + i + h], [y, y + h], color=C_OUT,
                    lw=lw, alpha=alpha, clip_on=True, zorder=zorder + 1)

def title_block(ax, sheet_label, subtitle, scale_note=""):
    ax.text(0.01, 0.022, "THE BIG SHOEBOX PROJECT  ·  TBS-001",
            transform=ax.transAxes, color=C_DIM, fontsize=7, **FONT)
    ax.text(0.01, 0.010, f"HINGED LIGHT-TRAP PANEL — {sheet_label}: {subtitle}",
            transform=ax.transAxes, color=C_OUT, fontsize=8, fontweight="bold", **FONT)
    if scale_note:
        ax.text(0.99, 0.022, scale_note,
                transform=ax.transAxes, color=C_DIM, fontsize=7, ha="right", **FONT)
    ax.text(0.99, 0.010, "ALL DIMS IN mm",
            transform=ax.transAxes, color=C_DIM, fontsize=7, ha="right", **FONT)


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1  —  Front Elevation (Exterior View)
# X = panel width (0 → 2362 mm),  Y = panel height (0 → 2388 mm)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():
    fig, ax = plt.subplots(figsize=(18, 14))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    PAD_L = 550; PAD_R = 650; PAD_B = 500; PAD_T = 450
    ax.set_xlim(-PAD_L, PW + PAD_R)
    ax.set_ylim(-PAD_B, PH + PAD_T)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Panel body ────────────────────────────────────────────────────────────
    # Outer steel frame (50mm wide)
    ax.add_patch(Rectangle((0, 0), PW, PH, fc=C_STEEL, ec=C_OUT, lw=2.5, zorder=2))
    # Ply skin area (inset of frame, shown slightly lighter)
    FR = 55  # visible frame width at face
    ax.add_patch(Rectangle((FR, FR), PW - 2 * FR, PH - 2 * FR,
                            fc=C_ALUM, ec=C_OUT, lw=0.8, zorder=3))
    ax.text(PW / 4, PH / 2,
            "18mm EXT-GRADE PLY\nFLAT BLACK INTERIOR",
            color=C_DIM, fontsize=6.5, ha="center", va="center", **FONT, zorder=4, alpha=0.7)

    # ── EPDM perimeter seal (dashed inner contour) ────────────────────────────
    S = 30  # seal inset
    epdm = plt.Polygon([(S, S), (PW - S, S), (PW - S, PH - S), (S, PH - S)],
                       closed=True, fill=False, ec=C_GASKT, lw=2.0, ls=(0, (4, 3)),
                       zorder=5)
    ax.add_patch(epdm)

    # ── Revolving drum ────────────────────────────────────────────────────────
    DX = DRUM_CX - DRUM_R   # drum left edge in panel
    DY_BOT = 100             # drum bottom clearance from panel bottom edge
    DY_TOP = DY_BOT + DRUM_H  # = 2100

    BRG_H = 45  # bearing housing height

    # Top + bottom bearing housings
    for by, label in [(DY_BOT, "LOWER BEARING"), (DY_TOP - BRG_H, "UPPER BEARING")]:
        ax.add_patch(Rectangle((DX - 35, by), DRUM_D + 70, BRG_H,
                                fc=C_STEEL, ec=C_OUT, lw=1.3, zorder=6))
        ax.text(DRUM_CX, by + BRG_H / 2, f"SKF 6215  {label}",
                color=C_OUT, fontsize=5.5, ha="center", va="center", **FONT, zorder=7)

    # Drum body (shown as tall rectangle in elevation)
    drum_body_y0 = DY_BOT + BRG_H
    drum_body_h  = DRUM_H - 2 * BRG_H
    ax.add_patch(Rectangle((DX, drum_body_y0), DRUM_D, drum_body_h,
                            fc="#F5F0E8", ec=C_OUT, lw=2.0, zorder=5))

    # Arc lines indicating cylindrical form (top and bottom ellipses in elevation)
    for arc_y, angle1, angle2 in [(drum_body_y0, 0, 180), (drum_body_y0 + drum_body_h, 180, 360)]:
        arc = Arc((DRUM_CX, arc_y), DRUM_D, 60,
                  angle=0, theta1=angle1, theta2=angle2,
                  color=C_OUT, lw=1.2, zorder=7)
        ax.add_patch(arc)

    # Drum centre line (vertical)
    ax.plot([DRUM_CX, DRUM_CX], [DY_BOT - 80, DY_TOP + 80],
            color=C_CL, lw=0.9, ls="--", zorder=6)
    ax.text(DRUM_CX, DY_TOP + 110, "CL", color=C_CL, fontsize=7,
            ha="center", va="bottom", **FONT)

    # Rotation arrows (inside drum body)
    for ry_offset in [-350, 0, 350]:
        ry = drum_body_y0 + drum_body_h / 2 + ry_offset
        ax.annotate("", xy=(DRUM_CX + DRUM_R * 0.6, ry + 120),
                    xytext=(DRUM_CX + DRUM_R * 0.6, ry - 120),
                    arrowprops=dict(arrowstyle="->", color=C_DIM, lw=0.9,
                                    connectionstyle="arc3,rad=0.5", mutation_scale=8))

    ax.text(DRUM_CX + DRUM_R * 0.6 + 70,
            drum_body_y0 + drum_body_h / 2,
            "DRUM\nROTATES", color=C_DIM, fontsize=6,
            ha="left", va="center", **FONT)

    # Handle bars (left and right of drum, at waist height)
    HY = DY_BOT + DRUM_H * 0.45   # handle Y centre
    HW = 110; HH = 42  # handle footprint
    for hx in [DX - HW, DX + DRUM_D]:
        ax.add_patch(Rectangle((hx, HY - HH / 2), HW, HH,
                                fc=C_STEEL, ec=C_OUT, lw=1.2, zorder=7))
    leader(ax, (DX - HW / 2, HY), (DX - HW - 200, HY - 220),
           "100mm PULL HANDLE\n(BOTH SIDES)")

    # ── Hinges (3 × left edge from exterior view) ────────────────────────────
    HINGE_YS = [220, 1190, PH - 230]
    HINGE_W = 85; HINGE_L = 220
    for hy in HINGE_YS:
        # Hinge leaf (exterior face)
        ax.add_patch(Rectangle((-HINGE_W, hy - HINGE_L // 2), HINGE_W, HINGE_L,
                                fc=C_ALUM, ec=C_OUT, lw=1.2, zorder=6))
        ax.add_patch(Circle((-HINGE_W / 2, hy), 22, fc=C_OUT, ec=BG, lw=0.8, zorder=7))
        # Extension line to hinge pin axis
        ax.plot([-HINGE_W / 2, -HINGE_W / 2], [hy - 8, hy + 8],
                color=BG, lw=1.5, zorder=8)

    # Hinge pin axis line
    ax.plot([-HINGE_W / 2, -HINGE_W / 2], [-60, PH + 80],
            color=C_CL, lw=0.9, ls="--", zorder=4)
    ax.text(-HINGE_W / 2, PH + 100, "HINGE PIN AXIS — 180° SWING",
            color=C_CL, fontsize=6.5, ha="center", va="bottom", **FONT)

    leader(ax, (-HINGE_W / 2, HINGE_YS[1]),
           (-HINGE_W - 280, HINGE_YS[1] + 300),
           "3 × 200mm S.S.\nBALL-BEARING PIANO HINGE")

    # ── Southco C2-33 cam latches (4 corners) ────────────────────────────────
    LATCH_XS = [210, PW - 210]
    LATCH_YS = [220, PH - 220]
    for lx in LATCH_XS:
        for ly in LATCH_YS:
            ax.add_patch(Rectangle((lx - 35, ly - 35), 70, 70,
                                    fc="#E8E0D0", ec=C_OUT, lw=1.2, zorder=6))
            ax.plot([lx - 22, lx + 22], [ly - 22, ly + 22],
                    color=C_OUT, lw=1.2, zorder=7)
            ax.plot([lx - 22, lx + 22], [ly + 22, ly - 22],
                    color=C_OUT, lw=1.2, zorder=7)
    leader(ax, (LATCH_XS[1], LATCH_YS[0]),
           (PW + 300, LATCH_YS[0] - 120),
           "SOUTHCO C2-33\nCAM LATCH (×4)")

    # ── EPDM seal leader ─────────────────────────────────────────────────────
    leader(ax, (PW - S, PH / 2),
           (PW + 320, PH / 2 + 300),
           "20mm EPDM GASKET\nIN ALUMINIUM CHANNEL\n(PERIMETER, ALL SIDES)")

    # ── Dimension lines ───────────────────────────────────────────────────────
    # Panel width
    dim_h(ax, 0, PW, PH + 230, f"{PW} mm  (CONTAINER INTERIOR WIDTH)")
    # Panel height
    dim_v(ax, PW + 150, 0, PH, f"{PH} mm", offset=55)
    # Drum diameter
    dim_h(ax, DX, DX + DRUM_D, DY_TOP + 130, f"Ø{DRUM_D} mm DRUM")
    # Drum clear height
    dim_v(ax, DX - 200, DY_BOT, DY_TOP, f"{DRUM_H} mm\nCLEAR HEIGHT", offset=55)
    # Drum centre from left
    dim_h(ax, 0, DRUM_CX, DY_BOT - 200, f"{int(DRUM_CX)} mm  (PANEL CL — CENTRED)")
    # Hinge positions from floor
    for hy in HINGE_YS:
        ax.plot([-HINGE_W - 10, -HINGE_W - 80], [hy, hy],
                color=C_DIM, lw=0.6, ls="--", zorder=3)
        ax.text(-HINGE_W - 90, hy, f"{hy}", color=C_DIM, fontsize=6,
                ha="right", va="center", **FONT)
    ax.text(-HINGE_W - 90, -180, "HINGE CL HEIGHT\nFROM FLOOR (mm)",
            color=C_DIM, fontsize=6, ha="right", va="top", **FONT)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 2", "FRONT ELEVATION — EXTERIOR VIEW", "SCALE 1:20")

    fig.savefig("hingepanel-sheet1.png", dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  hingepanel-sheet1.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2  —  Plan Cross-Section  (horizontal cut at drum mid-height)
# Looking DOWN through the panel — shows drum interior, 4 baffles, S-path.
# Different scales: 1:10 horizontal (panel width), 1:1 vertical (panel depth).
# Horizontal axis: panel width direction (0 → 2362 mm → drawn as 0 → 236.2 units)
# Vertical axis: depth through panel (real mm, 0=exterior, downward into container)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():
    # Scale functions
    def sx(mm): return mm / 10.0   # 1:10 horizontal
    def sy(mm): return mm * 1.0    # 1:1  vertical (depth, exaggerated for clarity)

    # Key depth positions (mm, from exterior face of container wall)
    WALL_T  = 40    # container end-wall steel thickness
    SEAL_T  = 20    # EPDM gasket compressed thickness
    PANEL_T = 120   # panel overall thickness (frame + skins)
    # Exterior face of container at y_depth=0
    # Container wall: 0 → WALL_T = 40
    # Panel outer face against wall: WALL_T = 40
    # Panel inner face: WALL_T + PANEL_T = 160
    # Container interior: > 160

    Y_EXT  = 0                    # exterior face
    Y_WI   = WALL_T               # container wall inner face / panel outer face
    Y_PI   = WALL_T + PANEL_T     # panel inner face = 160
    Y_INT  = Y_PI + 50            # container interior start (50mm shown)

    total_depth = Y_PI + 120      # total drawing depth range
    DRUM_CX_D = sx(PW / 2)        # drum centre in drawing X units

    fig, ax = plt.subplots(figsize=(18, 8))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    PAD_L = sx(500); PAD_R = sx(400); PAD_B = 50; PAD_T = 120
    ax.set_xlim(-PAD_L, sx(PW) + PAD_R)
    ax.set_ylim(-PAD_B, total_depth + PAD_T)
    ax.axis("off")
    # Note: NO equal aspect — horizontal is 1:10, vertical is 1:1

    # ── Container end wall (exterior left) ────────────────────────────────────
    hatch_rect(ax, 0, Y_EXT, sx(PW), WALL_T, C_STEEL, zorder=3)
    ax.text(sx(PW / 2), WALL_T / 2, "CONTAINER END-WALL STEEL  (40mm)",
            color=C_OUT, fontsize=7, ha="center", va="center", **FONT, zorder=4)

    # ── Panel body (inside container end-wall) ────────────────────────────────
    # Outer ply skin
    PLY_T = 18
    ax.add_patch(Rectangle((0, Y_WI), sx(PW), PLY_T,
                            fc=C_ALUM, ec=C_OUT, lw=1.0, zorder=3))
    ax.text(sx(PW / 2), Y_WI + PLY_T / 2, "18mm PLY SKIN",
            color=C_OUT, fontsize=6.5, ha="center", va="center", **FONT, zorder=4)

    # 50×50 RHS steel frame members (schematic positions)
    FRAME_T = sy(50)
    FRAME_Y = Y_WI + PLY_T
    # Frame: one wide band representing cross-section through frame
    ax.add_patch(Rectangle((0, FRAME_Y), sx(PW), FRAME_T,
                            fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=3))
    ax.text(sx(PW / 2), FRAME_Y + FRAME_T / 2,
            "50×50 RHS STEEL FRAME (WELDED, HOT-DIP GALVANISED)",
            color=C_OUT, fontsize=6.5, ha="center", va="center", **FONT, zorder=4)

    # Inner ply skin
    PLY_Y2 = FRAME_Y + FRAME_T
    ax.add_patch(Rectangle((0, PLY_Y2), sx(PW), PLY_T,
                            fc=C_ALUM, ec=C_OUT, lw=1.0, zorder=3))
    ax.text(sx(PW / 2), PLY_Y2 + PLY_T / 2, "18mm PLY SKIN (FLAT BLACK INTERIOR)",
            color=C_OUT, fontsize=6.5, ha="center", va="center", **FONT, zorder=4)

    Y_PI_actual = PLY_Y2 + PLY_T   # panel inner face

    # ── EPDM gasket strip (at panel left and right edges, both sides) ─────────
    GASKT_W = sx(SEAL_T)
    for edge_x in [0, sx(PW) - GASKT_W]:
        ax.add_patch(Rectangle((edge_x, Y_WI), GASKT_W, Y_PI_actual - Y_WI,
                                fc=C_GASKT, ec=C_OUT, lw=0.8, zorder=5, alpha=0.8))
    leader(ax, (0 + GASKT_W / 2, Y_WI + (Y_PI_actual - Y_WI) / 2),
           (sx(-280), Y_WI + 25),
           "20mm EPDM GASKET\n(BOTH EDGES)", fs=6.5)

    # ── Drum cross-section (circle in plan view) ──────────────────────────────
    DRUM_R_D = sx(DRUM_R)  # drum radius in drawing units
    drum_centre_y = (Y_WI + Y_PI_actual) / 2  # centre vertically in panel depth

    # Drum opening through container wall
    ax.add_patch(Rectangle((DRUM_CX_D - DRUM_R_D, Y_EXT), 2 * DRUM_R_D, WALL_T,
                            fc=BG, ec=C_OUT, lw=1.0, zorder=6))

    # Drum circle (cross-section)
    drum_circle = Circle((DRUM_CX_D, drum_centre_y), DRUM_R_D,
                          fc="#F8F4EC", ec=C_OUT, lw=2.0, zorder=6)
    ax.add_patch(drum_circle)
    ax.text(DRUM_CX_D, drum_centre_y, f"Ø{DRUM_D}mm DRUM",
            color=C_DIM, fontsize=7, ha="center", va="center", **FONT, zorder=8)

    # ── 4 internal baffles (fins at 45° rotation from cardinal) ──────────────
    # Fins at 22.5°, 112.5°, 202.5°, 292.5° from horizontal
    FIN_ANGLES = [22.5, 112.5, 202.5, 292.5]
    for ang in FIN_ANGLES:
        rad = np.radians(ang)
        fx = DRUM_CX_D + DRUM_R_D * np.cos(rad)
        fy = drum_centre_y + DRUM_R_D * np.sin(rad)
        ax.plot([DRUM_CX_D, fx], [drum_centre_y, fy],
                color=C_OUT, lw=2.2, zorder=8)

    # Fin label
    leader(ax, (DRUM_CX_D + DRUM_R_D * np.cos(np.radians(22.5)) * 0.65,
                drum_centre_y + DRUM_R_D * np.sin(np.radians(22.5)) * 0.65),
           (DRUM_CX_D + DRUM_R_D + sx(180), drum_centre_y - 30),
           "4 × INTERNAL BAFFLES\n(45° OFFSET)\nFLAT BLACK PAINT", fs=6.5)

    # ── S-shaped light path through drum ─────────────────────────────────────
    # Exterior opening: bottom of drum facing exterior (Y=0)
    # Interior opening: top of drum facing interior
    # Light tries to enter at exterior bottom, curves around a fin, exits at interior top.
    # In cross-section: show dashed S-curved arrow from outside → drum entry →
    # around baffle → drum exit → inside.
    EXT_ENTRY = DRUM_CX_D - DRUM_R_D * 0.45   # offset entry point
    INT_EXIT  = DRUM_CX_D + DRUM_R_D * 0.45   # offset exit point

    # Light path arrow (curved, dashed)
    arrow_xs = [DRUM_CX_D - DRUM_R_D * 0.4,
                DRUM_CX_D - DRUM_R_D * 0.25,
                DRUM_CX_D + DRUM_R_D * 0.1,
                DRUM_CX_D + DRUM_R_D * 0.4]
    arrow_ys = [Y_EXT - 25,
                drum_centre_y - DRUM_R_D * 0.5,
                drum_centre_y + DRUM_R_D * 0.5,
                Y_PI_actual + 25]
    ax.plot(arrow_xs, arrow_ys, color=C_LIGHT, lw=2.5, ls="--", zorder=9, alpha=0.85)
    ax.annotate("", xy=(arrow_xs[-1], arrow_ys[-1]),
                xytext=(arrow_xs[-2], arrow_ys[-2]),
                arrowprops=dict(arrowstyle="->", color=C_LIGHT, lw=2.0, mutation_scale=9))
    ax.text(DRUM_CX_D + DRUM_R_D + sx(170), drum_centre_y + DRUM_R_D * 0.6,
            "LIGHT PATH — NO STRAIGHT LINE\nOF SIGHT POSSIBLE",
            color="#B07010", fontsize=6.5, ha="left", va="center", **FONT, zorder=9)

    # ── Container interior zone ───────────────────────────────────────────────
    INT_H = 55
    ax.add_patch(Rectangle((0, Y_PI_actual), sx(PW), INT_H,
                            fc="#F0F4F8", ec=C_OUT, lw=0.8, ls="--", zorder=3))
    ax.text(sx(PW / 2), Y_PI_actual + INT_H / 2, "← CONTAINER INTERIOR →",
            color=C_DIM, fontsize=7, ha="center", va="center", **FONT, zorder=4)

    # ── Dimension lines ────────────────────────────────────────────────────────
    # Container wall thickness
    dim_v(ax, sx(PW) + sx(120), Y_EXT, WALL_T, f"{WALL_T}mm WALL", offset=sx(30), fs=6.5)
    # Panel thickness
    dim_v(ax, sx(PW) + sx(120), Y_WI, Y_PI_actual,
          f"{PANEL_T}mm PANEL", offset=sx(30), fs=6.5)
    # Drum diameter (horizontal)
    dim_h(ax, DRUM_CX_D - DRUM_R_D, DRUM_CX_D + DRUM_R_D,
          -PAD_B + 12, f"Ø{DRUM_D} mm", offset=10, fs=7)
    # Panel width
    dim_h(ax, 0, sx(PW), total_depth + 60, f"{PW} mm PANEL WIDTH", offset=15, fs=7)
    # Drum centre from left
    dim_h(ax, 0, DRUM_CX_D, -PAD_B + 12 + 40,
          f"{int(DRUM_CX_D * 10)} mm → DRUM CL", offset=10, fs=6.5)

    # ── Scale annotation ───────────────────────────────────────────────────────
    ax.text(sx(PW / 2), total_depth + 90,
            "HORIZONTAL SCALE 1:10  /  VERTICAL (DEPTH) SCALE 1:1 — depth exaggerated for clarity",
            color=C_DIM, fontsize=6.5, ha="center", va="bottom", **FONT)

    # ── Direction labels ───────────────────────────────────────────────────────
    ax.text(sx(-380), (Y_WI + Y_PI_actual) / 2 - 10,
            "EXTERIOR\n←", color=C_DIM, fontsize=7, ha="right", va="center", **FONT)
    ax.text(sx(PW) + sx(280), (Y_WI + Y_PI_actual) / 2 - 10,
            "EXTERIOR\n→", color=C_DIM, fontsize=7, ha="left", va="center", **FONT)
    ax.text(sx(-380), Y_PI_actual + INT_H / 2,
            "INTERIOR →", color=C_DIM, fontsize=7, ha="right", va="center", **FONT)
    ax.text(sx(PW) + sx(280), Y_PI_actual + INT_H / 2,
            "← INTERIOR", color=C_DIM, fontsize=7, ha="left", va="center", **FONT)
    ax.text(sx(-50), Y_EXT + WALL_T / 2,
            "CONTAINER\nWALL", color=C_DIM, fontsize=6.5, ha="right", va="center", **FONT)

    # ── Title block ────────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 2",
                "PLAN SECTION AT DRUM MID-HEIGHT — DRUM CROSS-SECTION + LIGHT PATH",
                "HORIZ 1:10  /  VERT 1:1 (DEPTH EXAGGERATED)")

    fig.savefig("hingepanel-sheet2.png", dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  hingepanel-sheet2.png saved")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating hinged light-trap panel drawings...")
    sheet1()
    sheet2()
    print("Done.")
