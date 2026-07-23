#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""GRP walkway grating cut plan — 2× 36"×120" molded-FRP panels.

Nesting layout to yield all walkway pieces from the minimum number of sheets.
Dimensions in INCHES (supplier units). Fixed layout — no tbs_constants inputs.
Output: diagrams/grp-cutplan.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

C_KEEP = "#C8D8E8"   # pieces we use
C_OFF = "#EFEFE8"    # usable offcut
C_WASTE = "#D6D6D6"  # trim waste
C_OUT = "#1A1A1A"
C_CUT = "#B00020"    # cut lines (rip/crosscut callouts)

# (label, x0, x1 [length], y0, y1 [width], kind)  — panel is 120 long × 36 wide
PANEL_A = [
    ("Near-A\n11.8 × 120", 0, 120, 0, 11.8, "keep"),
    ("Far-A\n11.8 × 120", 0, 120, 11.8, 23.6, "keep"),
    ("Right\n11.8 × 93", 0, 93, 23.6, 35.4, "keep"),
    ("offcut\n11.8 × 27", 93, 120, 23.6, 35.4, "off"),
    ("waste 0.6 × 120", 0, 120, 35.4, 36, "waste"),
]
PANEL_B = [
    ("Left\n11.8 × 93", 0, 93, 0, 11.8, "keep"),
    ("offcut\n11.8 × 27", 93, 120, 0, 11.8, "off"),
    ("Near-B\n11.8 × 43.7", 0, 43.7, 11.8, 23.6, "keep"),
    ("Far-B\n11.8 × 43.7", 43.7, 87.4, 11.8, 23.6, "keep"),
    ("offcut\n11.8 × 32.6", 87.4, 120, 11.8, 23.6, "off"),
    ("Left-wide\n11.8 × 29.9", 0, 29.9, 23.6, 35.4, "keep"),
    ("Near-wide\n7.9 × 61.8", 29.9, 91.7, 23.6, 31.5, "keep"),
    ("scrap", 29.9, 91.7, 31.5, 35.4, "waste"),
    ("scrap", 91.7, 120, 23.6, 35.4, "waste"),
    ("waste 0.6 × 120", 0, 120, 35.4, 36, "waste"),
]
FILL = {"keep": C_KEEP, "off": C_OFF, "waste": C_WASTE}


def draw_panel(ax, pieces, title):
    for label, x0, x1, y0, y1, kind in pieces:
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=FILL[kind],
                               edgecolor=C_OUT, linewidth=1.4,
                               hatch=("////" if kind == "waste" else None)))
        if kind != "waste" or (x1 - x0) > 20:
            ax.text((x0 + x1) / 2, (y0 + y1) / 2, label, ha="center", va="center",
                    fontsize=7.5 if kind == "keep" else 6.2,
                    color=C_OUT if kind == "keep" else "#606060",
                    fontweight="bold" if kind == "keep" else "normal")
    # panel border
    ax.add_patch(Rectangle((0, 0), 120, 36, fill=False, edgecolor=C_OUT, linewidth=2.2))
    # rip-line callouts on the left (width) axis
    for w in (11.8, 23.6, 35.4):
        ax.plot([-4, 0], [w, w], color=C_CUT, linewidth=1.0, clip_on=False)
        ax.text(-5, w, f'{w}"', ha="right", va="center", fontsize=6.5, color=C_CUT)
    for w in (0, 36):
        ax.text(-5, w, f'{w}"', ha="right", va="center", fontsize=6.5, color=C_OUT)
    ax.set_xlim(-14, 124)
    ax.set_ylim(-2, 40)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=10, fontweight="bold", loc="left", pad=6)


def main():
    fig, (axa, axb) = plt.subplots(2, 1, figsize=(11, 6.2))
    draw_panel(axa, PANEL_A, 'PANEL A  —  36" × 120"   (rip @ 11.8 / 23.6 / 35.4;  crosscut @ 93)')
    draw_panel(axb, PANEL_B, 'PANEL B  —  36" × 120"   (rip @ 11.8 / 23.6 / 35.4;  crosscuts @ 43.7 / 87.4 / 93 / 29.9 / 73.8)')
    fig.suptitle("TBS-001  ·  GRP Walkway Grating Cut Plan  ·  2× 36\"×120\" molded-FRP panels (min sheets)",
                 fontsize=11, fontweight="bold", y=0.99)
    fig.text(0.5, 0.015, 'Length axis = 120" (horizontal) · Width axis = 36" (vertical) · red ticks = rip lines · '
             'blue = used pieces, tan = usable offcut, hatched = trim waste', ha="center", fontsize=7, color="#505050")
    fig.tight_layout(rect=(0, 0.03, 1, 0.96))
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                       "diagrams", "grp-cutplan.png")
    fig.savefig(out, dpi=150, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main()
