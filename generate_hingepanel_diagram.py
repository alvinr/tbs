#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_hingepanel_diagram.py  —  TBS-001 Hinged Light-Trap Panel

Sheet 1 — Front elevation (exterior view, 1:20):
  Panel dimensions, revolving drum position, hinges, latches, EPDM perimeter seal.

Sheet 2 — Plan cross-section (1:20 equal aspect):
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
DRUM_H  = 2200         # drum height (floor → top bearing, mm)
DRUM_CX = PW / 2       # drum centre X in panel (centred horizontally)
DRUM_CY = DRUM_H / 2  # drum centre Y = 1000 mm from floor

# ── Drawing helpers ───────────────────────────────────────────────────────────
def dim_h(ax, x0, x1, y, label, offset=70, fs=7, col=C_DIM):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9, mutation_scale=7),
                zorder=15)
    ax.text((x0 + x1) / 2, y + offset, label, color=col, fontsize=fs,
            ha="center", va="bottom", zorder=15, **FONT)

def dim_v(ax, x, y0, y1, label, offset=70, fs=7, col=C_DIM):
    ax.annotate("", xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9, mutation_scale=7),
                zorder=15)
    ax.text(x + offset, (y0 + y1) / 2, label, color=col, fontsize=fs,
            ha="left", va="center", zorder=15, **FONT)

def leader(ax, xy, xytext, text, col=C_DIM, fs=6.5):
    ax.annotate(text, xy=xy, xytext=xytext, color=col, fontsize=fs,
                ha="center", va="center", **FONT,
                arrowprops=dict(arrowstyle="-|>", color=col, lw=0.8, mutation_scale=6),
                zorder=15)

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
    t = ax.transAxes
    # White box with black border spanning full width at bottom
    ax.add_patch(FancyBboxPatch((0.005, 0.003), 0.99, 0.045,
                 boxstyle="square,pad=0", fc="white", ec=C_OUT, lw=1.2,
                 transform=t, zorder=20))
    # Vertical dividers at 30% and 75%
    ax.plot([0.30, 0.30], [0.003, 0.048], color=C_OUT, lw=0.6,
            transform=t, zorder=21)
    ax.plot([0.75, 0.75], [0.003, 0.048], color=C_OUT, lw=0.6,
            transform=t, zorder=21)
    # Left cell: project info
    ax.text(0.152, 0.037, "THE BIG SHOEBOX PROJECT",
            transform=t, color=C_OUT, fontsize=7.5, fontweight="bold",
            ha="center", va="center", zorder=21, **FONT)
    ax.text(0.152, 0.025, "TBS-001  ·  Hinged Light-Trap Panel",
            transform=t, color=C_DIM, fontsize=6.5, ha="center", va="center",
            zorder=21, **FONT)
    ax.text(0.152, 0.012, "© 2026 Alvin Richards — GNU AGPLv3",
            transform=t, color=C_DIM, fontsize=5.5, ha="center", va="center",
            style="italic", zorder=21, **FONT)
    # Centre cell: drawing title
    ax.text(0.525, 0.037, f"HINGED LIGHT-TRAP PANEL — {sheet_label}",
            transform=t, color=C_OUT, fontsize=8, fontweight="bold",
            ha="center", va="center", zorder=21, **FONT)
    ax.text(0.525, 0.020, subtitle,
            transform=t, color=C_DIM, fontsize=6.5, ha="center", va="center",
            zorder=21, **FONT)
    ax.text(0.525, 0.009, f"Scale: {scale_note}" if scale_note else "ALL DIMS IN mm",
            transform=t, color=C_DIM, fontsize=6.5, ha="center", va="center",
            zorder=21, **FONT)
    # Right cell: sheet number + units
    ax.text(0.875, 0.035, sheet_label,
            transform=t, color=C_OUT, fontsize=9, fontweight="bold",
            ha="center", va="center", zorder=21, **FONT)
    ax.text(0.875, 0.015, "ALL DIMS IN mm",
            transform=t, color=C_DIM, fontsize=6.5, ha="center", va="center",
            zorder=21, **FONT)


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
            color=C_DIM, fontsize=6.5, ha="center", va="center", **FONT, zorder=15, alpha=0.7)

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
                color=C_OUT, fontsize=5.5, ha="center", va="center", **FONT, zorder=15)

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
            ha="center", va="bottom", **FONT, zorder=15)

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
            ha="left", va="center", **FONT, zorder=15)

    # Handle bar — interior face only, shown as hidden (dashed) line inside drum body.
    # The handle is on the inner curved surface of the drum; from the exterior elevation
    # it is fully hidden behind the exterior drum wall — shown dashed per convention.
    HY = DY_BOT + DRUM_H * 0.45   # handle Y centre (~900mm)
    HW = 110; HH = 42  # handle footprint
    # Place handle inside the drum body rectangle, 20mm clear of the interior drum wall.
    hx_handle = DX + DRUM_D - HW - 20
    ax.add_patch(Rectangle((hx_handle, HY - HH / 2), HW, HH,
                            fc="none", ec=C_OUT, lw=1.2, ls=(0, (4, 3)), zorder=7))
    leader(ax, (hx_handle + HW / 2, HY), (DX + DRUM_D + 200, HY + 300),
           "100mm PULL HANDLE\n(INTERIOR FACE — HIDDEN)\nWelded bracket\nno through-hole")

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
            color=C_CL, fontsize=6.5, ha="center", va="bottom", **FONT, zorder=15)

    leader(ax, (-HINGE_W / 2, HINGE_YS[1]),
           (-HINGE_W - 280, HINGE_YS[1] + 300),
           "3 × 200mm S.S.\nBALL-BEARING PIANO HINGE")

    # ── Southco C2-33 cam latches (4 corners) — INTERIOR FACE ───────────────
    # Latches are mounted on the INTERIOR face of the panel.
    # From this exterior view they are hidden features — shown dashed per
    # engineering convention for features on the far/hidden face.
    # Interior mounting enables emergency egress: if the revolving drum jams,
    # operators inside the container can release the latches and push the panel
    # open outward without requiring access to the exterior face.
    LATCH_XS = [210, PW - 210]
    LATCH_YS = [220, PH - 220]
    for lx in LATCH_XS:
        for ly in LATCH_YS:
            ax.add_patch(Rectangle((lx - 35, ly - 35), 70, 70,
                                    fc="none", ec=C_DIM, lw=0.9,
                                    ls=(0, (4, 2)), zorder=6))
            ax.plot([lx - 22, lx + 22], [ly - 22, ly + 22],
                    color=C_DIM, lw=0.9, ls=(0, (4, 2)), zorder=7)
            ax.plot([lx - 22, lx + 22], [ly + 22, ly - 22],
                    color=C_DIM, lw=0.9, ls=(0, (4, 2)), zorder=7)
    leader(ax, (LATCH_XS[1], LATCH_YS[0]),
           (PW + 300, LATCH_YS[0] - 120),
           "SOUTHCO C2-33 CAM LATCH (×4)\nINTERIOR FACE — shown dashed\nEMERGENCY EGRESS:\noperate from inside if drum jams")

    # ── Outward-opening annotation ────────────────────────────────────────────
    # Panel hinges on left (X=0); right edge is the free edge.
    # Opens outward — away from interior camera equipment.
    ax.annotate("",
                xy=(PW + 55, PH * 0.36),
                xytext=(PW, PH * 0.36),
                arrowprops=dict(arrowstyle="-|>", color="#204080", lw=1.3,
                                mutation_scale=9))
    ax.text(PW + 65, PH * 0.36 + 55,
            "OPENS OUTWARD\n(180° SWING —\nCLEAR OF INTERIOR\nEQUIPMENT)",
            color="#204080", fontsize=6.5, ha="left", va="bottom",
            fontweight="bold", **FONT, zorder=15)

    # ── Emergency egress safety note ──────────────────────────────────────────
    ax.text(PW / 2, -240,
            "SAFETY: Interior-mounted cam latches (×4) allow emergency panel release from inside — "
            "operate if revolving drum jams. Panel opens outward, clear of all equipment.",
            color="#C04010", fontsize=6.5, ha="center", va="center",
            fontweight="bold", **FONT, zorder=15)

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
                ha="right", va="center", **FONT, zorder=15)
    ax.text(-HINGE_W - 90, -180, "HINGE CL HEIGHT\nFROM FLOOR (mm)",
            color=C_DIM, fontsize=6, ha="right", va="top", **FONT, zorder=15)

    # ── Section A-A cut indicator (at H=1000mm — corresponds to Sheet 2 plan cut)
    AA_H = 1000   # height of plan section cut
    ax.plot([-PAD_L, PW + PAD_R], [AA_H, AA_H],
            color=C_CL, lw=0.8, ls=(0, (10, 4, 2, 4)), zorder=4, alpha=0.7)
    ax.text(-PAD_L + 20, AA_H + 40, "A", color=C_CL, fontsize=9,
            fontweight="bold", ha="left", va="bottom", **FONT, zorder=15)
    ax.text(-PAD_L + 20, AA_H - 40, "A", color=C_CL, fontsize=9,
            fontweight="bold", ha="left", va="top", **FONT, zorder=15)
    ax.text(PW + PAD_R - 20, AA_H + 40, "A", color=C_CL, fontsize=9,
            fontweight="bold", ha="right", va="bottom", **FONT, zorder=15)
    ax.text(PW + PAD_R - 20, AA_H - 40, "A", color=C_CL, fontsize=9,
            fontweight="bold", ha="right", va="top", **FONT, zorder=15)
    ax.text(PW / 2, AA_H + 80,
            "SECTION A-A  (Plan cross-section — Sheet 2)",
            color=C_CL, fontsize=6.5, ha="center", va="bottom", **FONT, alpha=0.8, zorder=15)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 3", "FRONT ELEVATION — EXTERIOR VIEW", "SCALE 1:20")

    fig.savefig("diagrams/hingepanel-sheet1.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig("diagrams/hingepanel-sheet1.svg", bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet1.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2  —  Plan Cross-Section at drum mid-height (looking down)
# Equal aspect — all coordinates in real mm.
# X = panel width direction.
# Y = depth direction (0 = container exterior face, positive into container).
#
# The drum (Ø750mm) is much larger than the panel depth (120mm + 40mm wall).
# In plan, the drum circle overhangs both panel faces — this is physically
# correct: the drum is secured by top/bottom bearings, not by the panel depth.
# The plan section shows this clearly.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():
    # ── Key dimensions (mm) ──────────────────────────────────────────────────
    WALL_T = 40     # container end-wall steel thickness
    PLY_T  = 18     # ply skin thickness (each face)
    PT     = 120    # panel overall thickness (frame + 2 × ply)
    FRAME_T = PT - 2 * PLY_T   # = 84mm RHS frame depth

    # Y positions (from exterior face of container wall)
    Y0_W  = 0            # exterior face
    Y1_W  = WALL_T       # = 40  (inner face of wall / outer face of panel)
    Y0_PL = Y1_W         # outer ply starts
    Y1_PL = Y1_W + PLY_T # = 58
    Y0_FR = Y1_PL        # frame starts = 58
    Y1_FR = Y0_FR + FRAME_T  # = 142
    Y0_PL2 = Y1_FR       # inner ply = 142
    Y1_PL2 = Y0_PL2 + PLY_T  # = 160  (panel inner face)

    Y_EXT = Y0_W         # exterior face = 0
    Y_INT = Y1_PL2       # interior face = 160

    # Drum geometry — axis is vertical; plan section shows horizontal circle
    D_CX = PW / 2        # drum centre X: centred in panel width = 1181mm
    D_CY = (Y_EXT + Y_INT) / 2   # drum centre Y: centre of wall+panel depth = 80mm
    DR   = DRUM_R        # = 375mm

    # Drum Y extents
    D_YB = D_CY - DR     # exterior overhang bottom = 80 - 375 = -295mm
    D_YT = D_CY + DR     # interior overhang top    = 80 + 375 = 455mm

    # Drum X extents
    D_XL = D_CX - DR    # = 806mm
    D_XR = D_CX + DR    # = 1556mm

    # ── Crop window (zoomed to drum zone + margin) ────────────────────────────
    PAD_X  = 320   # horizontal margin each side
    PAD_YB = 300   # bottom margin (exterior zone + title block space)
    PAD_YT = 180   # top margin (interior zone)

    X_LO = D_XL - PAD_X          # = 486mm
    X_HI = D_XR + PAD_X + 580    # extra right for labels
    Y_LO = D_YB - PAD_YB         # = -445mm
    Y_HI = D_YT + PAD_YT         # = 635mm

    # Content range: ~2166 × 1080mm → ratio 2.0 : 1
    # Figure: (16, 8), ratio 2.0 : 1  → fills well with equal aspect

    fig, ax = plt.subplots(figsize=(16, 8))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Y_LO, Y_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Background zones ──────────────────────────────────────────────────────
    # Exterior zone (Y < 0)
    ax.add_patch(Rectangle((X_LO, Y_LO), X_HI - X_LO, Y_EXT - Y_LO,
                            fc="#EEF2F8", ec="none", zorder=1))
    ax.text(D_CX - PAD_X / 2, (Y_LO + Y_EXT) / 2,
            "EXTERIOR", color="#5060A0", fontsize=9, ha="center", va="center",
            **FONT, fontweight="bold", alpha=0.55, zorder=15)

    # Interior zone (Y > Y_INT)
    ax.add_patch(Rectangle((X_LO, Y_INT), X_HI - X_LO, Y_HI - Y_INT,
                            fc="#EEF6EE", ec="none", zorder=1))
    ax.text(D_CX - PAD_X / 2, (Y_INT + Y_HI) / 2,
            "INTERIOR", color="#407040", fontsize=9, ha="center", va="center",
            **FONT, fontweight="bold", alpha=0.55, zorder=15)

    # ── Container end-wall cross-section (Y=0→40) ─────────────────────────────
    # Left of drum opening
    ax.add_patch(Rectangle((X_LO, Y0_W), D_XL - X_LO, WALL_T,
                            fc=C_STEEL, ec=C_OUT, lw=1.0, hatch="///", zorder=3))
    # Right of drum opening
    ax.add_patch(Rectangle((D_XR, Y0_W), X_HI - D_XR, WALL_T,
                            fc=C_STEEL, ec=C_OUT, lw=1.0, hatch="///", zorder=3))
    ax.text(X_LO + 20, Y0_W + WALL_T / 2,
            f"CONTAINER END WALL  ({WALL_T}mm STEEL)",
            color=C_OUT, fontsize=6.5, ha="left", va="center", **FONT, zorder=15)

    # ── Panel outer ply (Y=40→58) ─────────────────────────────────────────────
    for x, w in [(X_LO, D_XL - X_LO), (D_XR, X_HI - D_XR)]:
        ax.add_patch(Rectangle((x, Y0_PL), w, PLY_T,
                                fc=C_ALUM, ec=C_OUT, lw=0.8, zorder=3))
    ax.text(X_LO + 20, Y0_PL + PLY_T / 2,
            f"OUTER PLY  ({PLY_T}mm)",
            color=C_OUT, fontsize=6.5, ha="left", va="center", **FONT, zorder=15)

    # ── Panel RHS frame (Y=58→142) ────────────────────────────────────────────
    for x, w in [(X_LO, D_XL - X_LO), (D_XR, X_HI - D_XR)]:
        ax.add_patch(Rectangle((x, Y0_FR), w, FRAME_T,
                                fc=C_STEEL, ec=C_OUT, lw=0.8, hatch="\\\\", zorder=3))
    ax.text(X_LO + 20, Y0_FR + FRAME_T / 2,
            f"50×50mm RHS STEEL FRAME  ({FRAME_T}mm)",
            color=C_OUT, fontsize=6.5, ha="left", va="center", **FONT, zorder=15)

    # ── Panel inner ply (Y=142→160) ───────────────────────────────────────────
    for x, w in [(X_LO, D_XL - X_LO), (D_XR, X_HI - D_XR)]:
        ax.add_patch(Rectangle((x, Y0_PL2), w, PLY_T,
                                fc=C_ALUM, ec=C_OUT, lw=0.8, zorder=3))
    ax.text(X_LO + 20, Y0_PL2 + PLY_T / 2,
            f"INNER PLY — FLAT BLACK  ({PLY_T}mm)",
            color=C_OUT, fontsize=6.5, ha="left", va="center", **FONT, zorder=15)

    # ── EPDM seal strip at panel left edge ────────────────────────────────────
    SEAL_W = 20
    ax.add_patch(Rectangle((X_LO, Y0_PL), SEAL_W, PT,
                            fc=C_GASKT, ec=C_OUT, lw=1.0, zorder=6, alpha=0.9))
    leader(ax, (X_LO + SEAL_W / 2, Y0_PL + PT / 2),
           (X_LO - 160, Y0_PL + PT / 2 + 100),
           "20mm EPDM GASKET\n(PERIMETER SEAL)", fs=6.5)

    # ── Drum: draw filled circle on top to cut out the drum hole ─────────────
    # First stamp BG colour over wall/panel where drum sits, then draw drum ring
    drum_bg = Circle((D_CX, D_CY), DR, fc=BG, ec="none", zorder=7)
    ax.add_patch(drum_bg)

    # Drum wall ring (3mm thick steel)
    drum_ring = Circle((D_CX, D_CY), DR, fc="none", ec=C_OUT, lw=2.5, zorder=9)
    ax.add_patch(drum_ring)
    drum_inner = Circle((D_CX, D_CY), DR - 3,
                         fc="#F8F4EC", ec=C_DIM, lw=0.6, ls="--", zorder=8)
    ax.add_patch(drum_inner)

    # ── Drum label ────────────────────────────────────────────────────────────
    ax.text(D_CX, D_CY + 55,
            f"Ø{DRUM_D}mm REVOLVING DRUM",
            color=C_OUT, fontsize=8, ha="center", va="center",
            **FONT, fontweight="bold", zorder=15)
    ax.text(D_CX, D_CY - 35,
            "3mm MILD STEEL  ·  FLAT BLACK POWDER COAT",
            color=C_DIM, fontsize=6.5, ha="center", va="center", **FONT, zorder=15)

    # ── 4 internal baffles (fins at 0°, 90°, 180°, 270°) ─────────────────────
    # 4 fins at cardinal angles → 4 quarter-circle sectors
    # Openings between sectors at 45°, 135°, 225°, 315°
    FIN_ANGLES_DEG = [0, 90, 180, 270]
    for ang_deg in FIN_ANGLES_DEG:
        rad = np.radians(ang_deg)
        fx  = D_CX + DR * np.cos(rad)
        fy  = D_CY + DR * np.sin(rad)
        # Draw fin (solid bar, 4mm wide)
        ax.plot([D_CX, fx], [D_CY, fy], color=C_OUT, lw=3.0, zorder=10,
                solid_capstyle="round")

    # Sector labels (two visible sectors)
    for ang_deg, lbl in [(45, "SECTOR\n(ENTRY)"), (225, "SECTOR\n(TRANSIT)")]:
        rad = np.radians(ang_deg)
        tx = D_CX + DR * 0.55 * np.cos(rad)
        ty = D_CY + DR * 0.55 * np.sin(rad)
        ax.text(tx, ty, lbl, color=C_DIM, fontsize=6, ha="center", va="center",
                **FONT, alpha=0.75, zorder=15)

    # Fin label with leader
    fin_pt_x = D_CX + DR * np.cos(np.radians(0)) * 0.55
    fin_pt_y = D_CY + DR * np.sin(np.radians(0)) * 0.55
    leader(ax, (fin_pt_x, fin_pt_y),
           (D_XR + 250, D_CY + DR * 0.5),
           "4 × INTERNAL BAFFLES\n(90° SECTORS)\n3mm STEEL · FLAT BLACK", fs=6.5)

    # ── Centre lines ──────────────────────────────────────────────────────────
    CL_EXT = 55
    ax.plot([D_CX - DR - CL_EXT, D_CX + DR + CL_EXT], [D_CY, D_CY],
            color=C_CL, lw=0.8, ls="--", zorder=7, alpha=0.6)
    ax.plot([D_CX, D_CX], [D_CY - DR - CL_EXT, D_CY + DR + CL_EXT],
            color=C_CL, lw=0.8, ls="--", zorder=7, alpha=0.6)
    ax.text(D_CX + DR + CL_EXT + 15, D_CY, "CL",
            color=C_CL, fontsize=7, ha="left", va="center", **FONT, zorder=15)

    # ── S-path light route ────────────────────────────────────────────────────
    # Fins at 0° and 90° block any direct exterior→interior path.
    # The route navigates one sector: enters at ~315° gap (lower-right),
    # curves around the 0° fin, exits at ~135° gap (upper-left) into interior.
    C_PATH = "#C08010"
    path_x = np.array([
        D_CX + DR * 0.42,    # exterior start (right of centre)
        D_CX + DR * 0.60,    # approach lower-right gap (315°)
        D_CX + DR * 0.68,    # inside drum, right of fin-0°
        D_CX + DR * 0.30,    # curving left around fin-0°
        D_CX - DR * 0.25,    # crossing to left half
        D_CX - DR * 0.62,    # approaching upper-left gap (135°)
        D_CX - DR * 0.42,    # interior exit (left of centre)
    ])
    path_y = np.array([
        D_YB - 90,           # exterior start
        D_CY - DR * 0.72,    # lower-right drum entry
        D_CY - DR * 0.22,    # inside lower-right sector
        D_CY + DR * 0.10,    # mid drum
        D_CY + DR * 0.35,    # upper-left sector
        D_CY + DR * 0.72,    # upper-left drum exit
        D_YT + 90,           # interior exit
    ])
    ax.plot(path_x, path_y, color=C_PATH, lw=2.5, ls="--", zorder=12, alpha=0.9)
    ax.annotate("", xy=(path_x[-1], path_y[-1]),
                xytext=(path_x[-2], path_y[-2]),
                arrowprops=dict(arrowstyle="->", color=C_PATH, lw=2.2, mutation_scale=10))
    # Entry / exit tags
    ax.text(path_x[0] + 35, path_y[0],
            "ENTRY (FROM EXTERIOR)", color=C_PATH, fontsize=6.5, ha="left", va="center", **FONT, zorder=15)
    ax.text(path_x[-1] + 35, path_y[-1],
            "EXIT (TO INTERIOR)", color=C_PATH, fontsize=6.5, ha="left", va="center", **FONT, zorder=15)
    # Route label
    ax.text(D_XR + 250, D_CY - DR * 0.4,
            "S-ROUTE — NO STRAIGHT-LINE\nSIGHT FROM EXTERIOR\nTO INTERIOR POSSIBLE",
            color=C_PATH, fontsize=7, ha="left", va="center", **FONT, zorder=15)

    # ── Dimension lines ────────────────────────────────────────────────────────
    DIM_X_R = D_XR + PAD_X * 0.35   # right-side dim column

    # Drum diameter (horizontal)
    dim_h(ax, D_XL, D_XR, D_YT + PAD_YT * 0.55,
          f"Ø{DRUM_D} mm  DRUM DIAMETER", fs=7)

    # Container wall thickness
    dim_v(ax, DIM_X_R, Y0_W, Y1_W,
          f"  {WALL_T}mm\n  WALL", offset=20, fs=6.5)

    # Panel overall thickness
    dim_v(ax, DIM_X_R, Y1_W, Y1_PL2,
          f"  {PT}mm\n  PANEL", offset=20, fs=6.5)

    # Exterior drum overhang
    dim_v(ax, D_XL - 180, D_YB, Y0_W,
          f"  {int(Y0_W - D_YB)}mm\n  EXT. OVERHANG", offset=25, fs=6)

    # Interior drum overhang
    dim_v(ax, D_XL - 180, Y1_PL2, D_YT,
          f"  {int(D_YT - Y1_PL2)}mm\n  INT. OVERHANG", offset=25, fs=6)

    # ── Panel extent note ─────────────────────────────────────────────────────
    ax.annotate("", xy=(D_XL, Y0_FR + FRAME_T / 2),
                xytext=(X_LO + 10, Y0_FR + FRAME_T / 2),
                arrowprops=dict(arrowstyle="<-", color=C_DIM, lw=0.8, mutation_scale=6))
    ax.text(X_LO + 15, Y0_FR + FRAME_T / 2 - 30,
            f"← PANEL CONTINUES {int(D_XL)}mm TO LEFT EDGE",
            color=C_DIM, fontsize=6, ha="left", va="center", **FONT, zorder=15)

    # ── Scale and note ────────────────────────────────────────────────────────
    ax.text((X_LO + X_HI) / 2, Y_HI - 20,
            "EQUAL ASPECT  ·  SCALE 1:20 (APPROX)  ·  VIEW CROPPED TO DRUM ZONE  ·  "
            "DRUM OVERHANGS PANEL ON BOTH FACES — SECURED BY BEARINGS AT TOP AND BOTTOM",
            color=C_DIM, fontsize=6.5, ha="center", va="top", **FONT, zorder=15)

    # ── Orientation clarification box ─────────────────────────────────────────
    # Small inset box top-right, making the viewing direction explicit
    OB_X = D_XR + 30
    OB_Y = D_YT - 160
    OB_W = 550
    OB_H = 280
    import matplotlib.patches as mpatches
    ax.add_patch(mpatches.FancyBboxPatch((OB_X, OB_Y), OB_W, OB_H,
                 boxstyle="round,pad=8",
                 facecolor="#FFFBF0", edgecolor="#806010", linewidth=1.0, zorder=12))
    ax.text(OB_X + OB_W / 2, OB_Y + OB_H - 25,
            "ORIENTATION NOTE",
            ha="center", va="top", fontsize=7, color="#806010",
            fontweight="bold", **FONT, zorder=15)
    ax.text(OB_X + OB_W / 2, OB_Y + OB_H * 0.5,
            "DRUM AXIS IS VERTICAL.\nPERSONNEL WALK THROUGH\nIN AN UPRIGHT POSITION.\nSee Sheet 3 for elevation view.",
            ha="center", va="center", fontsize=6.5, color="#403000",
            **FONT, zorder=15)

    # ── Interior latch safety note ─────────────────────────────────────────────
    # Small note below orientation box (latches are outside the drum-zone crop
    # in this view but their presence and position is relevant to egress design)
    ax.text(OB_X + OB_W / 2, OB_Y - 45,
            "PANEL LATCHES (×4, SOUTHCO C2-33):\nMOUNTED ON INTERIOR FACE —\nEGRESS OPERABLE FROM INSIDE",
            ha="center", va="top", fontsize=6, color="#C04010",
            fontweight="bold", **FONT, zorder=15)

    # ── Title block ────────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 3",
                "PLAN CROSS-SECTION (SECTION A-A AT H=1000mm) — DRUM BAFFLES & S-PATH LIGHT ROUTE",
                "EQUAL ASPECT  ·  SCALE 1:20 (APPROX)  ·  ALL DIMS IN mm")

    fig.savefig("diagrams/hingepanel-sheet2.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig("diagrams/hingepanel-sheet2.svg", bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet2.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3  —  Drum Vertical Section (Section A-A, looking along panel width)
#
# This view shows the drum in ELEVATION — makes clear it is a VERTICAL cylinder
# 2200mm tall that personnel walk through upright.
#
# Horizontal axis = DEPTH direction (exterior → interior, same as Sheet 2 Y axis)
# Vertical axis   = HEIGHT (0 → 2200mm, floor → top bearing)
#
# ASPECT RATIO: figsize derived from data limits. set_aspect("equal") always set.
# ═══════════════════════════════════════════════════════════════════════════════
def sheet3():
    # ── Key dimensions (re-use Sheet 2 depth constants) ──────────────────────
    WALL_T  = 40    # container end-wall steel thickness
    PLY_T   = 18    # ply skin thickness each face
    PT      = 120   # panel overall thickness
    FRAME_T = PT - 2 * PLY_T   # = 84mm

    # Depth positions (horizontal axis in this view)
    Y0_W   = 0           # exterior face of container wall
    Y1_W   = WALL_T      # = 40
    Y0_PL  = Y1_W        # outer ply
    Y1_PL  = Y1_W + PLY_T  # = 58
    Y0_FR  = Y1_PL       # frame start = 58
    Y1_FR  = Y0_FR + FRAME_T  # = 142
    Y0_PL2 = Y1_FR       # inner ply = 142
    Y1_PL2 = Y0_PL2 + PLY_T  # = 160  (panel interior face)

    # Drum geometry in this view
    D_CX_DEPTH = (Y0_W + Y1_PL2) / 2   # drum centre in depth = 80mm
    D_HALF_W   = DRUM_R                 # drum radius = 375mm (in depth axis)

    D_DEPTH_L  = D_CX_DEPTH - D_HALF_W   # = 80 - 375 = -295mm (exterior overhang)
    D_DEPTH_R  = D_CX_DEPTH + D_HALF_W   # = 80 + 375 = 455mm  (interior overhang)

    # Height positions (vertical axis in this view)
    H_FLOOR    = 0
    H_BRG_BOT  = 100          # lower bearing base
    H_BRG_HT   = 45           # bearing housing height
    H_DRUM_BOT = H_BRG_BOT + H_BRG_HT   # = 145mm (drum body starts)
    H_DRUM_TOP = H_DRUM_BOT + (DRUM_H - 2 * H_BRG_HT)  # = 145 + 1910 = 2055mm
    H_BRG_TOP  = H_DRUM_TOP + H_BRG_HT  # = 2100mm
    H_HANDLE   = H_BRG_BOT + DRUM_H * 0.45  # handle height = ~1000mm

    # ── Data range → figure size ──────────────────────────────────────────────
    PAD_L, PAD_R = 300, 700   # depth-axis margins
    PAD_B, PAD_T = 350, 350   # height-axis margins (bottom includes title block space)

    X_LO = D_DEPTH_L - PAD_L   # = -595mm
    X_HI = D_DEPTH_R + PAD_R   # = 1155mm  → width 1750mm
    Y_LO = H_FLOOR - PAD_B     # = -150mm
    Y_HI = H_BRG_TOP + PAD_T   # = 2450mm  → height 2600mm

    # Data ratio: 1750 : 2600 = 0.673 : 1
    FIG_H = 14.0
    FIG_W = FIG_H * (X_HI - X_LO) / (Y_HI - Y_LO)  # = 14 * 1750/2600 = 9.42in

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=130)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Y_LO, Y_HI)
    ax.set_aspect("equal")   # MANDATORY
    ax.axis("off")

    # ── Background zones ──────────────────────────────────────────────────────
    # Exterior zone (depth < 0)
    ax.add_patch(plt.Rectangle((X_LO, Y_LO), Y0_W - X_LO, Y_HI - Y_LO,
                                fc="#EEF2F8", ec="none", zorder=1))
    ax.text((X_LO + Y0_W) / 2, Y_HI - 80, "EXTERIOR",
            color="#5060A0", fontsize=9, ha="center", va="top", **FONT,
            fontweight="bold", alpha=0.55, zorder=15)

    # Interior zone (depth > panel interior face)
    ax.add_patch(plt.Rectangle((Y1_PL2, Y_LO), X_HI - Y1_PL2, Y_HI - Y_LO,
                                fc="#EEF6EE", ec="none", zorder=1))
    ax.text((Y1_PL2 + X_HI) / 2, Y_HI - 80, "INTERIOR\n(DARKROOM)",
            color="#407040", fontsize=9, ha="center", va="top", **FONT,
            fontweight="bold", alpha=0.55, zorder=15)

    # ── Container end wall (depth 0→40, full height) ──────────────────────────
    ax.add_patch(plt.Rectangle((Y0_W, H_FLOOR), WALL_T, H_BRG_TOP + 100,
                                fc=C_STEEL, ec=C_OUT, lw=0.8, hatch="///", zorder=3))
    ax.text(Y0_W + WALL_T / 2, H_BRG_TOP + 180,
            f"{WALL_T}mm\nWALL", ha="center", va="bottom",
            fontsize=6, color=C_DIM, **FONT, zorder=15)

    # ── Panel outer ply (depth 40→58) ────────────────────────────────────────
    ax.add_patch(plt.Rectangle((Y0_PL, H_FLOOR), PLY_T, H_BRG_TOP + 80,
                                fc=C_ALUM, ec=C_OUT, lw=0.6, zorder=3))

    # ── Panel RHS frame (depth 58→142) ────────────────────────────────────────
    ax.add_patch(plt.Rectangle((Y0_FR, H_FLOOR), FRAME_T, H_BRG_TOP + 80,
                                fc=C_STEEL, ec=C_OUT, lw=0.6, hatch="\\\\", zorder=3))

    # ── Panel inner ply (depth 142→160) ───────────────────────────────────────
    ax.add_patch(plt.Rectangle((Y0_PL2, H_FLOOR), PLY_T, H_BRG_TOP + 80,
                                fc=C_ALUM, ec=C_OUT, lw=0.6, zorder=3))

    # ── Floor (ground plane) ──────────────────────────────────────────────────
    ax.add_patch(plt.Rectangle((X_LO, H_FLOOR - PAD_B), X_HI - X_LO, PAD_B,
                                fc="#D8D0C0", ec="none", zorder=2))
    ax.plot([X_LO, X_HI], [H_FLOOR, H_FLOOR], color=C_OUT, lw=1.5, zorder=4)
    ax.text(X_LO + 30, H_FLOOR - PAD_B * 0.5, "FLOOR LEVEL",
            ha="left", va="center", fontsize=7, color=C_DIM, **FONT, zorder=15)

    # ── Lower bearing housing ─────────────────────────────────────────────────
    ax.add_patch(plt.Rectangle((D_DEPTH_L - 35, H_BRG_BOT),
                                DRUM_D + 70, H_BRG_HT,
                                fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=6))
    ax.text(D_CX_DEPTH, H_BRG_BOT + H_BRG_HT / 2,
            "SKF 6215  LOWER BEARING", ha="center", va="center",
            fontsize=5.5, color=C_OUT, **FONT, zorder=15)

    # ── Upper bearing housing ─────────────────────────────────────────────────
    ax.add_patch(plt.Rectangle((D_DEPTH_L - 35, H_DRUM_TOP),
                                DRUM_D + 70, H_BRG_HT,
                                fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=6))
    ax.text(D_CX_DEPTH, H_DRUM_TOP + H_BRG_HT / 2,
            "SKF 6215  UPPER BEARING", ha="center", va="center",
            fontsize=5.5, color=C_OUT, **FONT, zorder=15)

    # ── Drum body (tall rectangle, depth D_DEPTH_L→D_DEPTH_R, H_DRUM_BOT→H_DRUM_TOP)
    # This is the key visual: a tall vertical rectangle showing the drum is vertical
    ax.add_patch(plt.Rectangle((D_DEPTH_L, H_DRUM_BOT),
                                DRUM_D, H_DRUM_TOP - H_DRUM_BOT,
                                fc="#F5F0E8", ec=C_OUT, lw=2.0, zorder=5))

    # Drum wall thickness lines (3mm each side)
    DRUM_WALL_T = 3
    ax.plot([D_DEPTH_L + DRUM_WALL_T, D_DEPTH_L + DRUM_WALL_T],
            [H_DRUM_BOT, H_DRUM_TOP], color=C_DIM, lw=0.6, ls="--", zorder=6)
    ax.plot([D_DEPTH_R - DRUM_WALL_T, D_DEPTH_R - DRUM_WALL_T],
            [H_DRUM_BOT, H_DRUM_TOP], color=C_DIM, lw=0.6, ls="--", zorder=6)

    # ── 4 baffles (radial fins — shown as dashed lines at mid-depth in elevation)
    # Baffles run full height inside the drum.  In this elevation view they
    # appear as vertical dashed lines at their mid-chord depth positions.
    # Baffles are at 0°, 90°, 180°, 270° from horizontal (plan view).
    # In this elevation (looking along panel width = X axis in plan), the fins
    # at 0° and 180° appear at the drum wall, and 90° and 270° at drum centre.
    for fin_depth in [D_DEPTH_L, D_CX_DEPTH, D_DEPTH_R]:
        ax.plot([fin_depth, fin_depth], [H_DRUM_BOT + 20, H_DRUM_TOP - 20],
                color=C_OUT, lw=1.2, ls=(0, (5, 3)), zorder=7, alpha=0.7)

    ax.text(D_CX_DEPTH, H_DRUM_BOT + (H_DRUM_TOP - H_DRUM_BOT) * 0.5,
            "4 × INTERNAL BAFFLES\n(FULL HEIGHT)\nFlat black powder coat",
            ha="center", va="center", fontsize=6.5, color=C_DIM,
            **FONT, alpha=0.7, zorder=15)

    # ── Handle bar — interior face only, welded bracket (no through-hole) ────────
    # Handle projects INWARD from the drum wall into the hollow of the drum.
    # D_DEPTH_R is the interior drum wall face; handle runs D_DEPTH_R-110 → D_DEPTH_R.
    HH = 42
    hx = D_DEPTH_R - 110
    ax.add_patch(plt.Rectangle((hx, H_HANDLE - HH / 2), 110, HH,
                                fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=7))
    ax.text(hx + 55, H_HANDLE - HH / 2 - 40, "INT. HANDLE\n(welded bracket\nno through-hole)",
            ha="center", va="top", fontsize=5.5, color=C_DIM, **FONT, zorder=15)

    # ── Person silhouette — standing inside drum, feet at drum floor (H_DRUM_BOT) ──
    PERSON_H = 1780   # mm — operator height with shoes
    HEAD_R   = 80     # head circle radius
    # Place person inside drum toward the interior wall, clear of centreline text
    PERSON_X = D_DEPTH_R - 130
    P_FOOT   = H_DRUM_BOT          # feet on drum floor (145mm above container floor)
    P_HEAD   = P_FOOT + PERSON_H   # head top = 145 + 1780 = 1925mm

    # Drum floor level indicator (thin horizontal line across drum base)
    ax.plot([D_DEPTH_L, D_DEPTH_R], [H_DRUM_BOT, H_DRUM_BOT],
            color="#A06020", lw=0.8, ls="--", zorder=6, alpha=0.7)
    ax.text(D_DEPTH_L - 15, H_DRUM_BOT,
            f"DRUM FLOOR  H={H_DRUM_BOT}mm",
            ha="right", va="center", fontsize=6, color="#A06020", **FONT, zorder=15)

    # Person body (line) and head (circle)
    ax.plot([PERSON_X, PERSON_X], [P_FOOT, P_HEAD],
            color="#606060", lw=3.0, zorder=8, solid_capstyle="round")
    ax.add_patch(plt.Circle((PERSON_X, P_HEAD + HEAD_R), HEAD_R,
                             fc="#909090", ec="#505050", lw=1.0, zorder=8))

    # Headroom gap: person head top → drum body ceiling
    drum_body_h    = H_DRUM_TOP - H_DRUM_BOT
    headroom_1780  = drum_body_h - PERSON_H
    GAP_X = PERSON_X + HEAD_R + 20
    ax.annotate("", xy=(GAP_X, H_DRUM_TOP), xytext=(GAP_X, P_HEAD + 2 * HEAD_R),
                arrowprops=dict(arrowstyle="<->", color="#20A020", lw=1.0,
                                mutation_scale=7), zorder=9)
    ax.text(GAP_X - 125, (H_DRUM_TOP + P_HEAD + 2 * HEAD_R) / 2,
            f"{headroom_1780}mm\nHEADROOM",
            ha="left", va="center", fontsize=6, color="#20A020", fontweight="bold", **FONT, zorder=15)

    # Label alongside person
    ax.text(PERSON_X - HEAD_R - 15, P_FOOT + PERSON_H / 2,
            f"{PERSON_H}mm\noperator\n(shoes)",
            ha="right", va="center", fontsize=6, color="#505050", **FONT, zorder=15)

    # ── Drum body ceiling line ────────────────────────────────────────────────
    ax.plot([D_DEPTH_L - 50, D_DEPTH_R + 50], [H_DRUM_TOP, H_DRUM_TOP],
            color="#20A020", lw=1.2, ls="--", zorder=6)
    ax.text(X_LO + 80, H_DRUM_TOP + 60,
            f"DRUM BODY TOP  H={H_DRUM_TOP}mm  |  CLEAR WALKING HT={drum_body_h}mm",
            ha="left", va="bottom", fontsize=6.5, color="#20A020", **FONT, zorder=15)

    # ── Section A-A indicator ─────────────────────────────────────────────────
    ax.text(X_LO + 20, Y_HI - 200,
            "SECTION A-A\n(looking along panel width direction)",
            ha="left", va="top", fontsize=7, color=C_CL, **FONT,
            fontweight="bold", zorder=15)

    # ── Centre line (vertical drum axis) ──────────────────────────────────────
    ax.plot([D_CX_DEPTH, D_CX_DEPTH], [H_FLOOR - 80, H_BRG_TOP + 120],
            color=C_CL, lw=0.9, ls="--", zorder=6)
    ax.text(D_CX_DEPTH + 280, H_BRG_TOP + 140, "CL\nDRUM AXIS\n(VERTICAL)",
            ha="left", va="bottom", fontsize=6.5, color=C_CL, **FONT, zorder=15)

    # ── Entry / exit arrows ───────────────────────────────────────────────────
    # Person enters from EXTERIOR, pushes drum, exits to INTERIOR
    EAR_Y = H_FLOOR + DRUM_H * 0.4
    ax.annotate("", xy=(D_DEPTH_L - 20, EAR_Y),
                xytext=(X_LO + 60, EAR_Y),
                arrowprops=dict(arrowstyle="->", color="#C06010", lw=1.5,
                                mutation_scale=10))
    ax.text(X_LO + 60, EAR_Y + 50, "ENTER\n(from exterior)",
            ha="left", va="bottom", fontsize=7, color="#C06010", **FONT, zorder=15)

    ax.annotate("", xy=(D_DEPTH_R + 60, EAR_Y),
                xytext=(D_DEPTH_R + 20, EAR_Y),
                arrowprops=dict(arrowstyle="->", color="#20A060", lw=1.5,
                                mutation_scale=10))
    ax.text(D_DEPTH_R + 80, EAR_Y + 130, "EXIT\n(to interior / darkroom)",
            ha="left", va="bottom", fontsize=7, color="#20A060", **FONT, zorder=15)

    ax.text(D_CX_DEPTH, H_FLOOR + DRUM_H * 0.2,
            "DRUM ROTATES\nARROUND VERTICAL\nAXIS — PUSH WALL\nTO ENTER/EXIT",
            ha="center", va="center", fontsize=6.5, color=C_DIM,
            **FONT, alpha=0.75, zorder=15)

    # ── Dimension callouts ────────────────────────────────────────────────────
    DIM_R = D_DEPTH_R + PAD_R * 0.55

    # Drum height
    dim_v(ax, DIM_R, H_DRUM_BOT, H_DRUM_TOP,
          f"{DRUM_H} mm DRUM HEIGHT\n(CLEAR WALKING HEIGHT)", offset=30, fs=7)

    # Drum diameter (horizontal) — placed below top bearing to avoid CL label clash
    dim_h(ax, D_DEPTH_L, D_DEPTH_R, H_DRUM_TOP + 130,
          f"Ø{DRUM_D} mm DRUM DIAMETER", offset=35, fs=7)

    # Panel thickness (horizontal) — offset above bearing top
    dim_h(ax, Y0_W, Y1_PL2, H_BRG_TOP + 250,
          f"{PT}mm PANEL", offset=35, fs=6.5)

    # Wall thickness (horizontal) — placed in floor zone with larger offset
    dim_h(ax, Y0_W, Y1_W, H_BRG_BOT - 160,
          f"{WALL_T}mm WALL", offset=50, fs=6.5)

    # Exterior overhang (horizontal)
    dim_h(ax, D_DEPTH_L, Y0_W, H_FLOOR - 60,
          f"{abs(int(D_DEPTH_L))}mm EXT. OVERHANG", offset=35, fs=6)

    # Interior overhang (horizontal)
    dim_h(ax, Y1_PL2, D_DEPTH_R, H_FLOOR - 60,
          f"{int(D_DEPTH_R - Y1_PL2)}mm INT. OVERHANG", offset=35, fs=6)

    # Handle height
    ax.plot([D_DEPTH_L - 145, D_DEPTH_L - 260], [H_HANDLE, H_HANDLE],
            color=C_DIM, lw=0.6, ls="--", zorder=3)
    ax.text(D_DEPTH_L - 270, H_HANDLE,
            f"{int(H_HANDLE)}mm\nHANDLE HT",
            ha="right", va="center", fontsize=6, color=C_DIM, **FONT, zorder=15)

    # ── Title block ────────────────────────────────────────────────────────────
    title_block(ax, "SHEET 3 OF 3",
                "DRUM ELEVATION — SECTION A-A (VIEW ALONG PANEL WIDTH): VERTICAL DRUM, WALKING HEIGHT",
                "EQUAL ASPECT  ·  SCALE 1:20 (APPROX)  ·  ALL DIMS IN mm")

    fig.savefig("diagrams/hingepanel-sheet3.png", dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig("diagrams/hingepanel-sheet3.svg", bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/hingepanel-sheet3.png saved")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating hinged light-trap panel drawings...")
    sheet1()
    sheet2()
    sheet3()
    print("Done.")
