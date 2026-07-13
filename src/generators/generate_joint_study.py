#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""generate_joint_study.py — detailed design studies of the two candidate corner joints.

Film-plane-redesign branch. One sheet each for the GIMBAL and the U-JOINT, each with:
  · FRONT elevation + SIDE elevation (the two perpendicular pivot axes)
  · an ARTICULATED view at 45° (proves it clears)
  · a parts list + build notes
Everything ~1:1 (1 unit ≈ 1mm). Scratch decision aid — not a report figure yet.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Arc, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
DIAGRAMS_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "diagrams"))

BG = "#FFFFFF"; OUT = "#1A1A1A"
STEEL = "#B0B0B8"     # cross-slide (fixed side)
ALUM = "#C8D8E8"      # gimbal ring / yokes / intermediate
FRAME = "#2A6B2A"     # film-frame side
PIN = "#B07010"       # pins / shoulder bolts
BUSH = "#5A3E00"      # bushings
DIM = "#404040"
FONT = {"family": "monospace"}


def dimv(ax, x, y0, y1, txt, off=0):
    ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<->", color=DIM, lw=0.8))
    ax.text(x + off - 2, (y0 + y1) / 2, txt, color=DIM, fontsize=5.5, ha="right", va="center",
            rotation=90, **FONT)


def dimh(ax, x0, x1, y, txt):
    ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", color=DIM, lw=0.8))
    ax.text((x0 + x1) / 2, y + 2, txt, color=DIM, fontsize=5.5, ha="center", va="bottom", **FONT)


def lead(ax, x0, y0, x1, y1, txt, ha="left", color=OUT):
    ax.plot([x0, x1], [y0, y1], color=color, lw=0.6)
    ax.text(x1 + (2 if ha == "left" else -2), y1, txt, color=color, fontsize=5.6, ha=ha, va="center", **FONT)


def panel(ax, xl, yl, title=None):
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect("equal"); ax.axis("off")
    if title:
        ax.text(sum(xl) / 2, yl[1] - 4, title, color=OUT, fontsize=8, ha="center", va="top",
                fontweight="bold", **FONT)


def notes(ax, x, y, header, lines, w=0):
    ax.text(x, y, header, color=OUT, fontsize=7, ha="left", va="top", fontweight="bold", **FONT)
    for i, (m, t) in enumerate(lines):
        c = {"+": "#2A6B2A", "-": "#B03020", "·": DIM, "»": OUT}[m]
        ax.text(x, y - 7 - i * 6.2, f"{m} {t}", color=c, fontsize=5.9, ha="left", va="top", **FONT)


# ═══════════════════════════════════════════════════════════════════════════════
# GIMBAL
# ═══════════════════════════════════════════════════════════════════════════════
def gimbal_front(ax):
    """Front elevation: TILT pin horizontal (in plane), SWING pin end-on (offset above)."""
    panel(ax, (-40, 120), (-20, 190), "FRONT ELEVATION")
    # cross-slide + its yoke (carries the tilt pin, in double shear)
    ax.add_patch(Rectangle((-30, -12), 100, 16, fc=STEEL, ec=OUT, lw=1.2))
    ax.add_patch(Rectangle((2, 4), 12, 40, fc=ALUM, ec=OUT, lw=1.1))     # yoke lug L
    ax.add_patch(Rectangle((54, 4), 12, 40, fc=ALUM, ec=OUT, lw=1.1))    # yoke lug R
    # gimbal ring / block (intermediate)
    ax.add_patch(Rectangle((16, 34), 36, 62, fc=ALUM, ec=OUT, lw=1.4))
    ax.add_patch(Circle((34, 50), 7, fc=BUSH, ec=OUT, lw=0.7))           # tilt-pin bushing (end-on... shown as bore)
    # TILT pin — horizontal through both lugs + ring (double shear)
    ax.add_patch(Rectangle((2, 44), 62, 12, fc=PIN, ec=OUT, lw=0.9, zorder=8))
    ax.add_patch(Rectangle((-4, 46), 8, 8, fc=PIN, ec=OUT, lw=0.9, zorder=8))    # head
    ax.add_patch(Rectangle((64, 46), 7, 8, fc=STEEL, ec=OUT, lw=0.9, zorder=8))  # nut
    # SWING pin end-on (offset above the tilt pin) — a bore in the ring
    ax.add_patch(Circle((34, 80), 12, fc="none", ec=OUT, lw=1.0))
    ax.add_patch(Circle((34, 80), 8, fc=BUSH, ec=OUT, lw=0.8))
    ax.add_patch(Circle((34, 80), 5, fc=PIN, ec=OUT, lw=0.8))
    # frame yoke (holds the swing pin — its lugs are FRONT & BACK here, ghosted)
    ax.add_patch(Rectangle((14, 68), 40, 24, fill=False, ec=DIM, lw=0.9, ls="--"))
    ax.add_patch(Rectangle((-30, 100), 100, 16, fc=FRAME, ec=OUT, lw=1.2))
    ax.add_patch(Rectangle((26, 92), 16, 10, fc=FRAME, ec=OUT, lw=1.0))
    # dims + labels
    dimv(ax, -20, -12, 116, "stack\n~128mm", 0)
    dimh(ax, 2, 64, 30, "Ø24 tilt pin")
    lead(ax, 34, 50, 96, 40, "TILT axis (pin, double shear)", color=PIN)
    lead(ax, 34, 80, 96, 92, "SWING axis (pin end-on here)", color=PIN)
    lead(ax, 34, 65, -14, 70, "GIMBAL RING\n(fab. plate/box)", ha="right", color=OUT)
    lead(ax, 8, 20, -14, 20, "cross-slide\nyoke", ha="right")
    ax.text(20, 108, "FILM FRAME", color=BG, fontsize=5.5, ha="center", **FONT)
    ax.text(20, -4, "CROSS-SLIDE", color=OUT, fontsize=5.5, ha="center", **FONT)


def gimbal_side(ax):
    """Side elevation (rotated 90°): SWING pin horizontal, TILT pin end-on."""
    panel(ax, (-40, 120), (-20, 190), "SIDE ELEVATION (90°)")
    ax.add_patch(Rectangle((-30, -12), 100, 16, fc=STEEL, ec=OUT, lw=1.2))
    ax.add_patch(Rectangle((16, 4), 36, 46, fc=ALUM, ec=OUT, lw=1.1))   # ring lower (tilt-pin end-on)
    ax.add_patch(Circle((34, 50), 6, fc=PIN, ec=OUT, lw=0.8))           # tilt pin end-on
    ax.add_patch(Circle((34, 50), 10, fc="none", ec=OUT, lw=0.8))
    # swing pin horizontal through the ring + frame yoke lugs
    ax.add_patch(Rectangle((16, 74), 36, 20, fc=ALUM, ec=OUT, lw=1.1))  # ring upper
    ax.add_patch(Rectangle((2, 70), 12, 30, fc=FRAME, ec=OUT, lw=1.1))  # frame lug L
    ax.add_patch(Rectangle((54, 70), 12, 30, fc=FRAME, ec=OUT, lw=1.1)) # frame lug R
    ax.add_patch(Rectangle((2, 78), 62, 12, fc=PIN, ec=OUT, lw=0.9, zorder=8))  # swing pin
    ax.add_patch(Rectangle((-4, 80), 8, 8, fc=PIN, ec=OUT, lw=0.9, zorder=8))
    ax.add_patch(Rectangle((64, 80), 7, 8, fc=STEEL, ec=OUT, lw=0.9, zorder=8))
    ax.add_patch(Rectangle((-30, 100), 100, 16, fc=FRAME, ec=OUT, lw=1.2))
    dimh(ax, 2, 64, 66, "Ø24 swing pin")
    lead(ax, 34, 50, 96, 44, "TILT axis (end-on here)", color=PIN)
    lead(ax, 34, 84, 96, 96, "SWING axis (pin, double shear)", color=PIN)
    ax.text(20, 108, "FILM FRAME", color=BG, fontsize=5.5, ha="center", **FONT)
    ax.text(20, -4, "CROSS-SLIDE", color=OUT, fontsize=5.5, ha="center", **FONT)


def gimbal_artic(ax):
    """Articulated: the frame side swung 45° about the swing axis — clears freely."""
    panel(ax, (-50, 110), (-20, 150), "ARTICULATED · SWING 45°")
    ax.add_patch(Rectangle((-40, -12), 100, 16, fc=STEEL, ec=OUT, lw=1.1))
    ax.add_patch(Rectangle((6, 4), 36, 50, fc=ALUM, ec=OUT, lw=1.0))
    cx, cy = 24, 62
    ax.add_patch(Circle((cx, cy), 6, fc=PIN, ec=OUT, lw=0.8, zorder=6))
    # frame side rotated 45° about (cx,cy)
    th = np.radians(45)
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    pts = np.array([[-34, 0], [66, 0], [66, 16], [-34, 16]]) + np.array([0, 40])   # frame bar local
    pts = (R @ pts.T).T + np.array([cx, cy])
    ax.add_patch(Polygon(pts, closed=True, fc=FRAME, ec=OUT, lw=1.1))
    ax.add_patch(Arc((cx, cy), 60, 60, theta1=45, theta2=90, color=PIN, lw=1.4))
    ax.text(cx + 34, cy + 20, "45°", color=PIN, fontsize=7, ha="center", fontweight="bold", **FONT)
    ax.text(30, -16, "each axis clears ±45° with room to spare", color=DIM, fontsize=5.6,
            ha="center", va="top", **FONT)


def sheet_gimbal():
    fig = plt.figure(figsize=(15, 9)); fig.patch.set_facecolor(BG)
    fig.suptitle("CORNER-JOINT DESIGN STUDY — A · GIMBAL  (2 offset through-pins, each double shear)",
                 fontsize=11, fontweight="bold", family="monospace", y=0.97)
    ax1 = fig.add_axes([0.02, 0.30, 0.30, 0.62]); gimbal_front(ax1)
    ax2 = fig.add_axes([0.34, 0.30, 0.30, 0.62]); gimbal_side(ax2)
    ax3 = fig.add_axes([0.66, 0.42, 0.32, 0.50]); gimbal_artic(ax3)
    axn = fig.add_axes([0.66, 0.04, 0.33, 0.34]); axn.axis("off"); axn.set_xlim(0, 100); axn.set_ylim(0, 100)
    notes(axn, 0, 100, "PARTS (per corner ×4):", [
        ("»", "Gimbal ring — 6mm alum plate box, ~36×62, 2 bores"),
        ("»", "2 × Ø24 through-pins (M20 shoulder bolt 90269A925)"),
        ("»", "4 × acetal/bronze flanged bushings (Ø24 bore)"),
        ("»", "Cross-slide yoke (2 lugs) + frame yoke (2 lugs)"),
    ])
    axb = fig.add_axes([0.02, 0.03, 0.62, 0.22]); axb.axis("off"); axb.set_xlim(0, 100); axb.set_ylim(0, 100)
    notes(axb, 0, 100, "WHY / TRADE-OFFS:", [
        ("+", "Both axes are plain through-pins in DOUBLE shear — strong, no cantilever"),
        ("+", "±45°+ on each axis with generous clearance (no spherical-in-fork trap)"),
        ("+", "All 316 SS / acetal — corrosion-safe in the wash; no exotic rod-end"),
        ("+", "Pins = the Ø24 shoulder bolts already sourced; rest is fab from plate"),
        ("-", "Tallest of the three (~128mm stack) + most machined parts"),
        ("·", "Axes offset ~30mm (through-pins can't intersect) — a true gimbal ring, not a cross"),
    ])
    out = os.path.join(DIAGRAMS_DIR, "film-joint-study-gimbal.png")
    fig.savefig(out, dpi=150, facecolor=BG); print(f"  → {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# U-JOINT
# ═══════════════════════════════════════════════════════════════════════════════
def uj_front(ax):
    panel(ax, (-40, 120), (-20, 190), "FRONT ELEVATION")
    ax.add_patch(Rectangle((-30, -12), 100, 16, fc=STEEL, ec=OUT, lw=1.2))
    ax.add_patch(Rectangle((6, 4), 12, 42, fc=ALUM, ec=OUT, lw=1.1))    # slide yoke lug L
    ax.add_patch(Rectangle((50, 4), 12, 42, fc=ALUM, ec=OUT, lw=1.1))   # slide yoke lug R
    # cross journals: horizontal pair (in-plane) + vertical pair (end-on)
    ax.add_patch(Rectangle((6, 44), 56, 10, fc=PIN, ec=OUT, lw=0.9, zorder=8))  # horiz journal
    ax.add_patch(Circle((34, 49), 7, fc=BUSH, ec=OUT, lw=0.7, zorder=9))        # centre body
    ax.add_patch(Circle((34, 74), 9, fc="none", ec=OUT, lw=0.9))               # vert journal end-on
    ax.add_patch(Circle((34, 74), 5, fc=PIN, ec=OUT, lw=0.8))
    ax.add_patch(Rectangle((14, 62), 40, 24, fill=False, ec=DIM, lw=0.9, ls="--"))  # frame yoke ghost
    ax.add_patch(Rectangle((-30, 100), 100, 16, fc=FRAME, ec=OUT, lw=1.2))
    lead(ax, 34, 49, 96, 40, "cross / spider (4 journals)", color=PIN)
    lead(ax, 34, 74, 96, 86, "frame-yoke axis (end-on)", color=PIN)
    dimh(ax, 6, 62, 30, "~56mm across yoke")
    ax.text(20, 108, "FILM FRAME", color=BG, fontsize=5.5, ha="center", **FONT)
    ax.text(20, -4, "CROSS-SLIDE", color=OUT, fontsize=5.5, ha="center", **FONT)


def uj_cross(ax):
    panel(ax, (-45, 45), (-45, 55), "THE CROSS (spider)")
    ax.plot([-32, 32], [0, 0], color=PIN, lw=6, solid_capstyle="round")
    ax.plot([0, 0], [-32, 32], color=PIN, lw=6, solid_capstyle="round")
    for (x, y) in [(-32, 0), (32, 0), (0, -32), (0, 32)]:
        ax.add_patch(Circle((x, y), 6, fc=BUSH, ec=OUT, lw=0.8, zorder=6))   # bearing cap
    ax.add_patch(Circle((0, 0), 7, fc=STEEL, ec=OUT, lw=1.0, zorder=7))
    ax.text(0, -42, "4 journals in caps (needle or plain bush)", color=DIM, fontsize=5.4,
            ha="center", va="top", **FONT)


def uj_artic(ax):
    panel(ax, (-50, 110), (-20, 150), "ARTICULATED · 45°")
    ax.add_patch(Rectangle((-40, -12), 100, 16, fc=STEEL, ec=OUT, lw=1.1))
    ax.add_patch(Rectangle((10, 4), 8, 40, fc=ALUM, ec=OUT, lw=1.0))
    ax.add_patch(Rectangle((44, 4), 8, 40, fc=ALUM, ec=OUT, lw=1.0))
    cx, cy = 31, 50
    ax.add_patch(Circle((cx, cy), 8, fc=BUSH, ec=OUT, lw=0.8, zorder=6))
    th = np.radians(45); R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    pts = (R @ (np.array([[-34, 0], [66, 0], [66, 16], [-34, 16]]) + np.array([0, 32])).T).T + np.array([cx, cy])
    ax.add_patch(Polygon(pts, closed=True, fc=FRAME, ec=OUT, lw=1.1))
    ax.add_patch(Arc((cx, cy), 54, 54, theta1=45, theta2=90, color=PIN, lw=1.4))
    ax.text(cx + 30, cy + 18, "45°", color=PIN, fontsize=7, ha="center", fontweight="bold", **FONT)
    ax.text(30, -16, "~35–45° is the practical bearing limit", color="#B03020", fontsize=5.6,
            ha="center", va="top", **FONT)


def sheet_ujoint():
    fig = plt.figure(figsize=(15, 9)); fig.patch.set_facecolor(BG)
    fig.suptitle("CORNER-JOINT DESIGN STUDY — B · U-JOINT  (cross/spider between two yokes)",
                 fontsize=11, fontweight="bold", family="monospace", y=0.97)
    ax1 = fig.add_axes([0.02, 0.30, 0.31, 0.62]); uj_front(ax1)
    ax2 = fig.add_axes([0.36, 0.45, 0.28, 0.42]); uj_cross(ax2)
    ax3 = fig.add_axes([0.67, 0.42, 0.31, 0.50]); uj_artic(ax3)
    axn = fig.add_axes([0.36, 0.05, 0.28, 0.34]); axn.axis("off"); axn.set_xlim(0, 100); axn.set_ylim(0, 100)
    notes(axn, 0, 100, "PARTS (per corner ×4):", [
        ("»", "1 × U-joint / universal — SS if available, else fab"),
        ("»", "cross + 4 bearing caps (needle or plain bush)"),
        ("»", "2 × yokes (slide side + frame side, 90° apart)"),
        ("·", "Off-the-shelf SS 2-axis units in this size are rare"),
    ])
    axb = fig.add_axes([0.02, 0.03, 0.62, 0.22]); axb.axis("off"); axb.set_xlim(0, 100); axb.set_ylim(0, 100)
    notes(axb, 0, 100, "WHY / TRADE-OFFS:", [
        ("+", "Compact — one unit, both axes intersect at a point (no offset)"),
        ("+", "2 clean axes; torsionally locked (fine — plane never spins)"),
        ("-", "Angle capped ~35–45° by the cross geometry — right at our limit"),
        ("-", "Small journals carry the whole plane load through 4 tiny bearings"),
        ("-", "Needle bearings + the ferricyanide/citric wash = corrosion risk"),
        ("-", "Hard to source SS at size; a fab cross is a lot of precise work"),
    ])
    out = os.path.join(DIAGRAMS_DIR, "film-joint-study-ujoint.png")
    fig.savefig(out, dpi=150, facecolor=BG); print(f"  → {out}")


if __name__ == "__main__":
    sheet_gimbal()
    sheet_ujoint()
