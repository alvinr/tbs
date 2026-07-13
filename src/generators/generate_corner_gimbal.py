#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""generate_corner_gimbal.py — real corner-joint design (film-plane-redesign branch).

Study A developed into a buildable corner gimbal: a 2-axis universal joint (two perpendicular
Ø24 shoulder-bolt pins on an intermediate block, torsion-locked = no twist), each pin in double
shear on acetal/PTFE bushings, bolting the film-frame corner to its FLOATING X–Z cross-slide.

  TILT  = rotation about the horizontal pin (pin 1, on the cross-slide yoke)
  SWING = rotation about the vertical  pin (pin 2, on the frame yoke), offset above pin 1 so the
          two bores don't intersect. Both reach ±45°.

Front + side elevations (dimensioned), 45° articulation checks, parts, and build notes.
~1:1 (1 unit ≈ 1mm). Iteration draft — not a report sheet yet.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Arc

HERE = os.path.dirname(os.path.abspath(__file__))
DIAGRAMS_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "diagrams"))

BG = "#FFFFFF"; OUT = "#1A1A1A"
STEEL = "#B0B0B8"     # cross-slide (fixed side)
ALUM = "#C8D8E8"      # yokes / gimbal block (6061 or 316)
FRAME = "#2A6B2A"     # film-frame side
PIN = "#B07010"       # Ø24 shoulder-bolt pins
BUSH = "#5A3E00"      # acetal/PTFE bushings
DIM = "#404040"
FONT = {"family": "monospace"}

# ── key dimensions (mm) ──
PIN_D = 24          # shoulder diameter (90269A925)
SHOULDER = 70       # shoulder length
BUSH_OD = 30        # acetal bushing OD (Ø24 bore)
LUG_T = 12          # yoke-lug thickness
BLK_W = 40          # gimbal-block width along each pin
OFFSET = 32         # vertical offset between the two pin axes (so Ø30 bores clear)


def dimh(ax, x0, x1, y, txt, fs=5.5):
    ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", color=DIM, lw=0.7))
    ax.text((x0 + x1) / 2, y + 1.5, txt, color=DIM, fontsize=fs, ha="center", va="bottom", **FONT)


def dimv(ax, x, y0, y1, txt, fs=5.5):
    ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<->", color=DIM, lw=0.7))
    ax.text(x - 1.5, (y0 + y1) / 2, txt, color=DIM, fontsize=fs, ha="right", va="center",
            rotation=90, **FONT)


def lead(ax, x0, y0, x1, y1, txt, ha="left", color=OUT, fs=5.6):
    ax.plot([x0, x1], [y0, y1], color=color, lw=0.6)
    ax.text(x1 + (1.5 if ha == "left" else -1.5), y1, txt, color=color, fontsize=fs, ha=ha,
            va="center", **FONT)


def bolt(ax, cx, cy, horizontal, length):
    """A Ø24 shoulder bolt: head + shoulder + nut. cx,cy = shoulder mid."""
    r = PIN_D / 2
    if horizontal:
        ax.add_patch(Rectangle((cx - length / 2, cy - r), length, PIN_D, fc=PIN, ec=OUT, lw=0.8, zorder=9))
        ax.add_patch(Rectangle((cx - length / 2 - 6, cy - r - 3), 6, PIN_D + 6, fc=PIN, ec=OUT, lw=0.8, zorder=9))  # head
        ax.add_patch(Rectangle((cx + length / 2, cy - r - 2), 7, PIN_D + 4, fc=STEEL, ec=OUT, lw=0.8, zorder=9))    # nut
    else:
        ax.add_patch(Rectangle((cx - r, cy - length / 2), PIN_D, length, fc=PIN, ec=OUT, lw=0.8, zorder=9))
        ax.add_patch(Rectangle((cx - r - 3, cy + length / 2), PIN_D + 6, 6, fc=PIN, ec=OUT, lw=0.8, zorder=9))       # head
        ax.add_patch(Rectangle((cx - r - 2, cy - length / 2 - 7), PIN_D + 4, 7, fc=STEEL, ec=OUT, lw=0.8, zorder=9)) # nut


# ── FRONT ELEVATION: tilt pin (horizontal) as through-pin; swing pin end-on ──
def front(ax):
    ax.set_xlim(-70, 90); ax.set_ylim(-25, 165); ax.set_aspect("equal"); ax.axis("off")
    ax.text(20, 160, "FRONT ELEVATION", color=OUT, fontsize=8, ha="center", fontweight="bold", **FONT)
    p1y = 40           # tilt-pin height
    p2y = p1y + OFFSET # swing-pin height (end-on here)
    # floating cross-slide
    ax.add_patch(Rectangle((-55, -18), 100, 18, fc=STEEL, ec=OUT, lw=1.2))
    ax.text(-5, -9, "X–Z CROSS-SLIDE  (floats — absorbs arc travel)", color=OUT, fontsize=5, ha="center", **FONT)
    # cross-slide yoke: two lugs (L/R) carrying the tilt pin
    ax.add_patch(Rectangle((-34, 0), LUG_T, p1y + 6, fc=ALUM, ec=OUT, lw=1.0))
    ax.add_patch(Rectangle((22, 0), LUG_T, p1y + 6, fc=ALUM, ec=OUT, lw=1.0))
    # gimbal block
    ax.add_patch(Rectangle((-20, p1y - 20), 40, OFFSET + 40, fc=ALUM, ec=OUT, lw=1.3))
    # bushings for the tilt pin (in each lug + block faces)
    for bx in (-24, 20):
        ax.add_patch(Rectangle((bx, p1y - BUSH_OD / 2), 4, BUSH_OD, fc=BUSH, ec=OUT, lw=0.6, zorder=7))
    # tilt pin (horizontal, double shear)
    bolt(ax, -2, p1y, True, 62)
    # swing pin, END-ON in this view (a bore up in the block)
    ax.add_patch(Circle((0, p2y), BUSH_OD / 2, fc=BUSH, ec=OUT, lw=0.7, zorder=7))
    ax.add_patch(Circle((0, p2y), PIN_D / 2, fc=PIN, ec=OUT, lw=0.8, zorder=8))
    # frame yoke (its lugs are front/back here → ghosted) + frame
    ax.add_patch(Rectangle((-16, p2y - 16), 32, 40, fill=False, ec=DIM, lw=0.8, ls="--"))
    ax.add_patch(Rectangle((-55, 118), 100, 16, fc=FRAME, ec=OUT, lw=1.2))
    ax.text(-5, 126, "FILM-FRAME CORNER  (2×2 angle)", color=BG, fontsize=5, ha="center", **FONT)
    ax.add_patch(Rectangle((-6, p2y + 10), 12, 118 - (p2y + 10), fc=FRAME, ec=OUT, lw=1.0))  # riser to frame
    # dims + labels
    dimh(ax, -34, 34, p1y - 30, "Ø24 tilt pin (shoulder bolt) — DOUBLE SHEAR")
    dimv(ax, -46, -18, 118, "stack ~150")
    lead(ax, 20, p1y, 60, p1y - 8, "TILT axis (horizontal pin)", color=PIN)
    lead(ax, 0, p2y, 55, p2y + 16, "SWING axis (vertical pin, end-on)", color=PIN)
    lead(ax, 20, p1y + 18, 58, p1y + 40, "GIMBAL BLOCK\n(316 SS / 6061, 2 offset bores)", color=OUT)
    lead(ax, -24, p1y - 8, -50, p1y - 20, "acetal bushing\n(Ø24, self-lube)", ha="right", color=BUSH)
    lead(ax, -34, 24, -52, 40, "cross-slide\nyoke (2 lugs)", ha="right")


# ── SIDE ELEVATION (90°): swing pin (vertical) through-pin; tilt pin end-on ──
def side(ax):
    ax.set_xlim(-70, 90); ax.set_ylim(-25, 165); ax.set_aspect("equal"); ax.axis("off")
    ax.text(20, 160, "SIDE ELEVATION (90°)", color=OUT, fontsize=8, ha="center", fontweight="bold", **FONT)
    p1y = 40; p2y = p1y + OFFSET
    ax.add_patch(Rectangle((-55, -18), 100, 18, fc=STEEL, ec=OUT, lw=1.2))
    # gimbal block + tilt pin END-ON (lower)
    ax.add_patch(Rectangle((-20, p1y - 20), 40, OFFSET + 40, fc=ALUM, ec=OUT, lw=1.3))
    ax.add_patch(Circle((0, p1y), BUSH_OD / 2, fc=BUSH, ec=OUT, lw=0.7, zorder=7))
    ax.add_patch(Circle((0, p1y), PIN_D / 2, fc=PIN, ec=OUT, lw=0.8, zorder=8))
    # cross-slide yoke (front/back here → ghost) at the tilt pin
    ax.add_patch(Rectangle((-30, p1y - 16), 60, 32, fill=False, ec=DIM, lw=0.8, ls="--"))
    # frame yoke: two lugs (above/below) carrying the swing pin
    ax.add_patch(Rectangle((-34, p2y - 6), LUG_T, 40, fc=FRAME, ec=OUT, lw=1.0))
    ax.add_patch(Rectangle((22, p2y - 6), LUG_T, 40, fc=FRAME, ec=OUT, lw=1.0))
    for by in (-24, 20):
        ax.add_patch(Rectangle((by, p2y - BUSH_OD / 2), 4, BUSH_OD, fc=BUSH, ec=OUT, lw=0.6, zorder=7))
    bolt(ax, -2, p2y, True, 62)   # swing pin shown horizontal in THIS orthogonal view
    ax.add_patch(Rectangle((-55, 118), 100, 16, fc=FRAME, ec=OUT, lw=1.2))
    ax.add_patch(Rectangle((-6, p2y + 22), 12, 118 - (p2y + 22), fc=FRAME, ec=OUT, lw=1.0))
    dimh(ax, -34, 34, p2y - 20, "Ø24 swing pin — DOUBLE SHEAR")
    lead(ax, 0, p1y, 55, p1y - 14, "TILT axis (end-on here)", color=PIN)
    lead(ax, 20, p2y, 58, p2y + 8, "SWING axis (vertical pin)", color=PIN)
    lead(ax, -34, p2y + 20, -52, 118, "frame yoke\n(2 lugs, ⟂ to slide yoke)", ha="right", color=OUT)


# ── articulation checks ──
def artic(ax, axis_name, color):
    ax.set_xlim(-55, 55); ax.set_ylim(-15, 95); ax.set_aspect("equal"); ax.axis("off")
    ax.text(0, 90, f"{axis_name} 45°", color=OUT, fontsize=6.5, ha="center", fontweight="bold", **FONT)
    ax.add_patch(Rectangle((-40, -12), 80, 12, fc=STEEL, ec=OUT, lw=0.9))
    ax.add_patch(Rectangle((-16, 0), 32, 36, fc=ALUM, ec=OUT, lw=0.9))
    cx, cy = 0, 44
    ax.add_patch(Circle((cx, cy), PIN_D / 2 - 4, fc=PIN, ec=OUT, lw=0.7, zorder=6))
    th = np.radians(45); R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    pts = (R @ (np.array([[-30, 0], [50, 0], [50, 13], [-30, 13]]) + np.array([0, 26])).T).T + np.array([cx, cy])
    ax.add_patch(Polygon(pts, closed=True, fc=FRAME, ec=OUT, lw=1.0))
    ax.add_patch(Arc((cx, cy), 50, 50, theta1=45, theta2=90, color=color, lw=1.3))
    ax.text(cx + 28, cy + 16, "45°", color=color, fontsize=6, ha="center", fontweight="bold", **FONT)


def notes(ax, x, y, header, lines):
    ax.text(x, y, header, color=OUT, fontsize=7, ha="left", va="top", fontweight="bold", **FONT)
    for i, (m, t) in enumerate(lines):
        c = {"+": "#2A6B2A", "-": "#B03020", "·": DIM, "»": OUT}[m]
        ax.text(x, y - 6.5 - i * 5.8, f"{m} {t}", color=c, fontsize=5.8, ha="left", va="top", **FONT)


def main():
    fig = plt.figure(figsize=(15, 9)); fig.patch.set_facecolor(BG)
    fig.suptitle("FILM-PLANE CORNER GIMBAL — DESIGN A  (2-axis universal joint · no twist · ±45° · ×4 corners)",
                 fontsize=10.5, fontweight="bold", family="monospace", y=0.975)
    ax1 = fig.add_axes([0.01, 0.30, 0.31, 0.63]); front(ax1)
    ax2 = fig.add_axes([0.33, 0.30, 0.31, 0.63]); side(ax2)
    axa = fig.add_axes([0.66, 0.62, 0.16, 0.30]); artic(axa, "TILT", PIN)
    axb = fig.add_axes([0.83, 0.62, 0.16, 0.30]); artic(axb, "SWING", PIN)
    axp = fig.add_axes([0.66, 0.30, 0.33, 0.28]); axp.axis("off"); axp.set_xlim(0, 100); axp.set_ylim(0, 100)
    notes(axp, 0, 100, "PARTS  (per corner · ×4):", [
        ("»", "1 × gimbal block — 316 SS or 6061, ~50×70×44, 2 offset Ø30 bores"),
        ("»", "2 × Ø24 shoulder bolt, 70mm shoulder, M20 (McMaster 90269A925)"),
        ("»", "4 × acetal/PTFE flanged bushing, Ø24 bore × Ø30 OD (igus iglidur)"),
        ("»", "1 × cross-slide yoke + 1 × frame yoke (6061, 2 lugs each, 90° apart)"),
        ("»", "2 × M20 nyloc nut, 316 SS"),
    ])
    axn = fig.add_axes([0.02, 0.02, 0.62, 0.25]); axn.axis("off"); axn.set_xlim(0, 100); axn.set_ylim(0, 100)
    notes(axn, 0, 100, "WHY / GROUNDING:", [
        ("+", "2 perpendicular pins = a universal joint: tilt + swing, TORSION-LOCKED (enforces 'no twist')"),
        ("+", "Each pin in DOUBLE shear on acetal bushings — strong, self-lubricating, corrosion-immune (wet)"),
        ("+", "Axes offset 32mm so the two Ø30 bores clear; each pin independently reaches ±45°+"),
        ("+", "Pins = the Ø24 shoulder bolts already sourced; retires the rod-end (couldn't do ±45°)"),
        ("·", "Sits on the FLOATING X–Z cross-slide → the arc travel is absorbed, no over-constraint"),
    ])
    axr = fig.add_axes([0.66, 0.02, 0.33, 0.25]); axr.axis("off"); axr.set_xlim(0, 100); axr.set_ylim(0, 100)
    notes(axr, 0, 100, "OPEN / TO ITERATE:", [
        ("·", "Block bore offset (32) vs stack height — tune"),
        ("·", "±45° tilt clearance of block vs cross-slide body"),
        ("·", "Yoke → cross-slide plate + frame-angle weld detail"),
        ("·", "Bushing length / flange vs the 70mm shoulder budget"),
        ("·", "Which pin gets tilt vs swing (yaw-free: tilt lower)"),
    ])
    out = os.path.join(DIAGRAMS_DIR, "film-corner-gimbal.png")
    fig.savefig(out, dpi=150, facecolor=BG); print(f"  → {out}")


if __name__ == "__main__":
    main()
