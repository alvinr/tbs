#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""generate_joint_options.py — corner-joint concept comparison for the film-plane redesign.

The film-plane corner joint must give TWO axes of rotation (tilt + swing) up to ~±45° at each
corner, carry the plane's weight, and mount between the X-Z cross-slide (below) and the frame
corner (above). This sheet compares three ways to do it — a scratch decision aid on the
`film-plane-redesign` branch, NOT (yet) a report figure.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Arc

HERE = os.path.dirname(os.path.abspath(__file__))
DIAGRAMS_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "diagrams"))

BG = "#FFFFFF"
OUT = "#1A1A1A"
STEEL = "#B0B0B8"      # cross-slide (fixed side)
ALUM = "#C8D8E8"       # intermediate / ring / yoke
FRAME = "#2A6B2A"      # film-frame side (green)
PIN = "#B07010"        # pins / bolts (amber)
DIM = "#404040"
FONT = {"family": "monospace"}


def _slide(ax):
    ax.add_patch(Rectangle((8, 4), 84, 13, fc=STEEL, ec=OUT, lw=1.4))
    ax.text(50, 10.5, "X–Z CROSS-SLIDE", color=OUT, fontsize=6.5, ha="center", va="center", **FONT)


def _frame(ax):
    ax.add_patch(Rectangle((8, 83), 84, 13, fc=FRAME, ec=OUT, lw=1.4))
    ax.text(50, 89.5, "FILM-FRAME CORNER", color=BG, fontsize=6.5, ha="center", va="center", **FONT)


def _rot_arrow(ax, cx, cy, r, a0, a1, color, label, lx, ly):
    ax.add_patch(Arc((cx, cy), 2 * r, 2 * r, theta1=a0, theta2=a1, color=color, lw=1.6))
    ax.text(lx, ly, label, color=color, fontsize=6, ha="center", va="center", fontweight="bold", **FONT)


def _pinends(ax, x0, x1, y, horizontal=True):
    if horizontal:
        ax.plot([x0, x1], [y, y], color=PIN, lw=4, solid_capstyle="round", zorder=8)
    else:
        ax.plot([x0, x0], [x1, y], color=PIN, lw=4, solid_capstyle="round", zorder=8)


def _panel(ax, title):
    ax.set_xlim(0, 100)
    ax.set_ylim(-30, 108)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(50, 104, title, color=OUT, fontsize=8.5, ha="center", va="center", fontweight="bold", **FONT)


def _notes(ax, lines):
    for i, (mark, txt) in enumerate(lines):
        c = {"+": "#2A6B2A", "-": "#B03020", "·": DIM}[mark]
        ax.text(2, -6 - i * 6.5, f"{mark} {txt}", color=c, fontsize=6.2, ha="left", va="top", **FONT)


# ── A · GIMBAL ────────────────────────────────────────────────────────────────
def gimbal(ax):
    _panel(ax, "A · GIMBAL")
    _slide(ax)
    _frame(ax)
    # outer yoke on the cross-slide (carries the TILT pin)
    ax.add_patch(Rectangle((24, 17), 7, 22, fc=ALUM, ec=OUT, lw=1.1))
    ax.add_patch(Rectangle((69, 17), 7, 22, fc=ALUM, ec=OUT, lw=1.1))
    # gimbal ring
    ax.add_patch(Circle((50, 50), 15, fc="none", ec=OUT, lw=2.4))
    ax.add_patch(Circle((50, 50), 11, fc="none", ec=OUT, lw=1.0))
    # TILT pin — horizontal, ring↔slide yoke (double shear)
    ax.plot([27, 73], [50, 50], color=PIN, lw=5, solid_capstyle="round", zorder=8)
    ax.add_patch(Circle((27, 50), 2.6, fc=PIN, ec=OUT, lw=0.6, zorder=9))
    ax.add_patch(Circle((73, 50), 2.6, fc=PIN, ec=OUT, lw=0.6, zorder=9))
    # inner yoke on the frame (carries the SWING pin)
    ax.add_patch(Rectangle((46.5, 61), 7, 22, fc=FRAME, ec=OUT, lw=1.1))
    # SWING pin — vertical, ring↔frame yoke (double shear)
    ax.plot([50, 50], [37, 63], color=PIN, lw=5, solid_capstyle="round", zorder=8)
    ax.add_patch(Circle((50, 37), 2.6, fc=PIN, ec=OUT, lw=0.6, zorder=9))
    ax.add_patch(Circle((50, 63), 2.6, fc=PIN, ec=OUT, lw=0.6, zorder=9))
    ax.text(80, 50, "TILT\npin", color=PIN, fontsize=6, ha="center", va="center", fontweight="bold", **FONT)
    ax.text(50, 28, "SWING pin", color=PIN, fontsize=6, ha="center", va="center", fontweight="bold", **FONT)
    _notes(ax, [
        ("+", "Two plain pins, EACH in double shear — strong"),
        ("+", "±45°+ trivially, no clearance games"),
        ("+", "Fabricated from plate; reuses the Ø24 shoulder bolts"),
        ("+", "Drops the rod-end entirely (no exotic part / price)"),
        ("-", "Most parts + a bit taller in the corner stack"),
    ])


# ── B · U-JOINT ───────────────────────────────────────────────────────────────
def ujoint(ax):
    _panel(ax, "B · U-JOINT (cross/spider)")
    _slide(ax)
    _frame(ax)
    # lower yoke (slide side)
    ax.add_patch(Rectangle((30, 17), 8, 20, fc=ALUM, ec=OUT, lw=1.1))
    ax.add_patch(Rectangle((62, 17), 8, 20, fc=ALUM, ec=OUT, lw=1.1))
    # upper yoke (frame side, rotated 90°)
    ax.add_patch(Rectangle((30, 63), 40, 8, fc=FRAME, ec=OUT, lw=1.1))
    ax.add_patch(Rectangle((30, 63), 8, 20, fc=FRAME, ec=OUT, lw=1.1))
    ax.add_patch(Rectangle((62, 63), 8, 20, fc=FRAME, ec=OUT, lw=1.1))
    # the cross / spider
    ax.plot([34, 66], [50, 50], color=PIN, lw=5, solid_capstyle="round", zorder=8)
    ax.plot([50, 50], [42, 58], color=PIN, lw=5, solid_capstyle="round", zorder=8)
    for (cx, cy) in [(34, 50), (66, 50), (50, 42), (50, 58)]:
        ax.add_patch(Circle((cx, cy), 3, fc=PIN, ec=OUT, lw=0.6, zorder=9))
    ax.text(50, 50, "cross", color=OUT, fontsize=5.5, ha="center", va="center", **FONT, zorder=10)
    _notes(ax, [
        ("+", "Compact, one bought unit, 2 clean axes"),
        ("-", "Small cross-bearings — angle (~35–45°) + load limited"),
        ("-", "Awkward to mate to a flat corner + the cross-slide"),
        ("-", "Torsionally locked (fine) but needle brgs dislike wash"),
        ("·", "Best only if a suitably-sized SS unit is found"),
    ])


# ── C · SINGLE-LUG SPHERICAL ──────────────────────────────────────────────────
def single_lug(ax):
    _panel(ax, "C · SINGLE-LUG SPHERICAL")
    _slide(ax)
    _frame(ax)
    # rod-end: shank up from the slide, ball at the top
    ax.add_patch(Rectangle((46, 17), 8, 20, fc=FRAME, ec=OUT, lw=1.1))   # shank (into slide)
    ax.add_patch(Circle((50, 50), 15, fc=ALUM, ec=OUT, lw=1.8))          # housing/eye
    ax.add_patch(Circle((50, 50), 9, fc=STEEL, ec=OUT, lw=1.0))          # ball
    ax.add_patch(Circle((50, 50), 4, fc=BG, ec=OUT, lw=0.8))             # bore
    # ONE lug from the frame, pin cantilevers into the ball (single shear)
    ax.add_patch(Rectangle((44, 63, ), 12, 20, fc=FRAME, ec=OUT, lw=1.1))
    ax.plot([50, 50], [50, 74], color=PIN, lw=5, solid_capstyle="round", zorder=8)
    ax.add_patch(Circle((50, 74), 2.8, fc=PIN, ec=OUT, lw=0.6, zorder=9))
    # free-swing cone
    ax.add_patch(FancyArrowPatch((36, 30), (64, 30), connectionstyle="arc3,rad=-0.5",
                 arrowstyle="<->", color=DIM, lw=1.2, mutation_scale=8))
    ax.text(50, 22, "body swings free ±47°", color=DIM, fontsize=5.6, ha="center", va="center", **FONT)
    _notes(ax, [
        ("+", "Simplest — the rod-end body swings free (no fork)"),
        ("+", "Fewest parts; the ball gives all axes at once"),
        ("-", "SINGLE shear — pin cantilevers (weaker)"),
        ("·", "Workable IF the lug + pin are sized up for the load"),
        ("·", "= the beefed-up version of what we had"),
    ])


def main():
    fig, axes = plt.subplots(1, 3, figsize=(15, 8))
    fig.patch.set_facecolor(BG)
    gimbal(axes[0]); ujoint(axes[1]); single_lug(axes[2])
    fig.suptitle("FILM-PLANE CORNER JOINT — CONCEPT OPTIONS  (2 axes · ±45° · carries the plane)",
                 fontsize=11, fontweight="bold", family="monospace", y=0.97)
    fig.text(0.5, 0.05,
             "All three give tilt + swing to ±45°.  Recommendation: A (gimbal) — strongest, "
             "double-shear on both axes, fabricable, and it retires the rod-end.",
             ha="center", fontsize=8, family="monospace", color=DIM)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.1, wspace=0.08)
    out = os.path.join(DIAGRAMS_DIR, "film-joint-options.png")
    fig.savefig(out, dpi=150, facecolor=BG)
    print(f"  → {out}")


if __name__ == "__main__":
    main()
