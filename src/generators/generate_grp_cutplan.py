#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""GRP walkway grating cut plan — 2× 36"×120" molded-FRP panels.

Nesting layout to yield all walkway pieces from the minimum number of sheets.
Each PHYSICAL piece is drawn as ONE polygon — the near-walkway bump-out and the
left lift-out drum-exit punch-out are INTEGRAL L-tabs (cut in one piece, no
mid-deck joint), matching the 3D model. The only butt joints are the four corner
joins between the near / far / left / right decks and the one unavoidable sheet
seam in the >10ft near/far runs (molded GRP tops out at 3'×10').

Dimensions in INCHES (supplier units). Output: diagrams/grp-cutplan.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

C_KEEP = "#C8D8E8"   # pieces we use
C_OFF = "#EFEFE8"    # usable offcut
C_WASTE = "#D6D6D6"  # trim waste
C_OUT = "#1A1A1A"
C_CUT = "#B00020"    # cut lines (rip/crosscut callouts)

# Panel = 120 long (x) × 36 wide (y).  Each piece: (label, polygon-points, kind).
# Standard deck width 11.8" (300mm); bump-out adds 7.9" (200mm); punch-out adds
# 11.8" (300mm).  Near/far runs are 151.9" (3859mm) → one seam, split 120 + 31.9.
PANEL_A = [
    # Near-A: 120" of the near deck WITH the EP/battery bump-out as an integral tab
    # (baseline 11.8 wide; tab out to 19.7 over x 23.0..84.8 — one L-shaped cut).
    ("Near-A + bump\n(integral L, 120)",
     [(0, 0), (120, 0), (120, 11.8), (84.8, 11.8), (84.8, 19.7),
      (23.0, 19.7), (23.0, 11.8), (0, 11.8)], "keep"),
    ("Far-A\n11.8 × 120", [(0, 19.7), (120, 19.7), (120, 31.5), (0, 31.5)], "keep"),
    ("offcut", [(0, 11.8), (23.0, 11.8), (23.0, 19.7), (0, 19.7)], "off"),
    ("offcut", [(84.8, 11.8), (120, 11.8), (120, 19.7), (84.8, 19.7)], "off"),
    ("waste 4.5 × 120", [(0, 31.5), (120, 31.5), (120, 36), (0, 36)], "waste"),
]
PANEL_B = [
    # Left lift-out: 11.8 × 93 strip with the drum-exit punch-out tab (out to 23.6
    # over x 31.5..61.4) integral, and the muslin-drop notch bitten IN at x 75.3..81.2.
    # baseline 11.8 × 93 (y 0..11.8); drum-exit punch-out tab out to y 23.6 over x 31.5..61.4;
    # muslin notch is a small bite on the inboard edge (called out, area negligible).
    ("Left lift-out + punch-out + notch\n(integral L, 93)",
     [(0, 0), (93, 0), (93, 11.8), (61.4, 11.8), (61.4, 23.6),
      (31.5, 23.6), (31.5, 11.8), (0, 11.8)], "keep"),
    ("Right\n11.8 × 93 (+notch)", [(0, 23.6), (93, 23.6), (93, 35.4), (0, 35.4)], "keep"),
    ("Near-B\n11.8 × 31.9", [(93, 0), (120, 0), (120, 11.8), (93, 11.8)], "keep"),
    ("Far-B\n11.8 × 31.9", [(61.4, 11.8), (93.3, 11.8), (93.3, 23.6), (61.4, 23.6)], "keep"),
    ("offcut", [(0, 11.8), (31.5, 11.8), (31.5, 23.6), (0, 23.6)], "off"),
    ("offcut", [(93.3, 11.8), (120, 11.8), (120, 23.6), (93.3, 23.6)], "off"),
    ("offcut", [(93, 23.6), (120, 23.6), (120, 35.4), (93, 35.4)], "off"),
    ("waste 0.6 × 120", [(0, 35.4), (120, 35.4), (120, 36), (0, 36)], "waste"),
]
FILL = {"keep": C_KEEP, "off": C_OFF, "waste": C_WASTE}


def draw_panel(ax, pieces, title):
    for label, pts, kind in pieces:
        ax.add_patch(Polygon(pts, closed=True, facecolor=FILL[kind],
                             edgecolor=C_OUT, linewidth=1.4,
                             hatch=("////" if kind == "waste" else None)))
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
        if kind != "waste" or (max(xs) - min(xs)) > 20:
            ax.text(cx, cy, label, ha="center", va="center",
                    fontsize=7.2 if kind == "keep" else 6.0,
                    color=C_OUT if kind == "keep" else "#606060",
                    fontweight="bold" if kind == "keep" else "normal")
    # panel border
    ax.add_patch(Rectangle((0, 0), 120, 36, fill=False, edgecolor=C_OUT, linewidth=2.2))
    # rip-line callouts on the left (width) axis
    for w in (11.8, 19.7, 23.6, 31.5, 35.4):
        ax.plot([-4, 0], [w, w], color=C_CUT, linewidth=1.0, clip_on=False)
        ax.text(-5, w, f'{w}"', ha="right", va="center", fontsize=6.2, color=C_CUT)
    for w in (0, 36):
        ax.text(-5, w, f'{w}"', ha="right", va="center", fontsize=6.5, color=C_OUT)
    ax.set_xlim(-14, 124)
    ax.set_ylim(-2, 40)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=10, fontweight="bold", loc="left", pad=6)


def main():
    fig, (axa, axb) = plt.subplots(2, 1, figsize=(11, 6.4))
    draw_panel(axa, PANEL_A, 'PANEL A  —  36" × 120"   (Near+bump L / Far / seam @120)')
    draw_panel(axb, PANEL_B, 'PANEL B  —  36" × 120"   (Left+punch L / Right / Near-B / Far-B tails)')
    fig.suptitle("TBS-001  ·  GRP Walkway Grating Cut Plan  ·  2× 36\"×120\" molded-FRP panels (min sheets)",
                 fontsize=11, fontweight="bold", y=0.99)
    fig.text(0.5, 0.015, 'Length axis = 120" (horizontal) · Width axis = 36" (vertical) · red ticks = rip lines · '
             'blue = used pieces (bump-out & punch-out are INTEGRAL L-cuts), tan = usable offcut, hatched = trim waste',
             ha="center", fontsize=7, color="#505050")
    fig.tight_layout(rect=(0, 0.03, 1, 0.96))
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                       "diagrams", "grp-cutplan.png")
    fig.savefig(out, dpi=150, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main()
