#!/usr/bin/env python3
"""
generate_favicon.py — Renders the GPC badge as a 512×512 PNG favicon.
Output: favicon.png (for docs/assets/)
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.colors import LinearSegmentedColormap

# ── Cyanotype palette (matches logo) ─────────────────────────────────────────
PRU_INK   = "#081A32"
PRU_DEEP  = "#0F2D5E"
PRU_MID   = "#1755A0"
PRU_LIGHT = "#2E82D4"
CYAN_MID  = "#45B0E8"
CYAN_LITE = "#7ED4F2"
PAPER     = "#E4F4FD"
PAPER_W   = "#F0FAFF"

fig, ax = plt.subplots(figsize=(5.12, 5.12), dpi=100)
fig.patch.set_facecolor(PRU_DEEP)
ax.set_facecolor(PRU_DEEP)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

CX, CY = 50, 50  # centre of canvas

# ── Tonal wash ────────────────────────────────────────────────────────────────
np.random.seed(7)
xs, ys = np.linspace(0, 100, 200), np.linspace(0, 100, 200)
XX, YY = np.meshgrid(xs, ys)
bg = sum(np.exp(-((XX-cx)**2+(YY-cy)**2)/(2*r**2))
         for cx,cy,r in [(25,75,30),(70,40,38),(50,55,22),(15,30,18),(80,80,28)])
bg = (bg-bg.min())/(bg.max()-bg.min())
cmap_c = LinearSegmentedColormap.from_list("c", [PRU_INK, PRU_DEEP, PRU_MID])
ax.imshow(bg, extent=[0,100,0,100], origin="lower", cmap=cmap_c,
          alpha=0.55, aspect="auto", zorder=0)

# ── Outer glow ring ───────────────────────────────────────────────────────────
for r, a in [(46, 0.08), (44, 0.14), (42, 0.22)]:
    ax.add_patch(Circle((CX, CY), r, fc="none", ec=CYAN_MID, lw=0.8, alpha=a, zorder=1))

# ── Badge rings ───────────────────────────────────────────────────────────────
ax.add_patch(Circle((CX, CY), 40, fc=PRU_MID,   ec=PAPER,    lw=4.0, zorder=2))
ax.add_patch(Circle((CX, CY), 33, fc=PRU_LIGHT, ec=CYAN_MID, lw=2.0, zorder=3))

# ── Pinhole silhouette inside badge (tiny camera cross-section icon) ──────────
# Container body — rectangular outline
rect_w, rect_h = 36, 16
rect_x = CX - rect_w / 2
rect_y = CY - rect_h / 2 + 4
from matplotlib.patches import FancyBboxPatch
ax.add_patch(FancyBboxPatch((rect_x, rect_y), rect_w, rect_h,
             boxstyle="round,pad=0.5", fc=PRU_DEEP, ec=PAPER_W, lw=2.2, zorder=4))

# Pinhole dot on left wall
ax.add_patch(Circle((rect_x + 1.5, CY + 4), 1.4, fc=PAPER_W, ec="none", zorder=5))

# Light rays
for ang in np.linspace(-28, 28, 5):
    rad = np.radians(ang)
    x_end = rect_x + 1.5 + 14 * np.cos(rad)
    y_end = CY + 4 + 14 * np.sin(rad)
    ax.plot([rect_x + 1.5, x_end], [CY + 4, y_end],
            color=PAPER_W, lw=0.8, alpha=0.5, zorder=5)

# Image plane — right wall vertical line
ax.plot([rect_x + rect_w - 1.5, rect_x + rect_w - 1.5],
        [rect_y + 2, rect_y + rect_h - 2],
        color=CYAN_LITE, lw=2.0, zorder=5)

# Tripod legs (two short lines beneath container)
for tx, ty in [(CX-6, rect_y-7), (CX, rect_y-8), (CX+6, rect_y-7)]:
    ax.plot([CX, tx], [rect_y, ty], color=PAPER, lw=1.6,
            solid_capstyle="round", zorder=4)
ax.plot([CX-10, CX+10], [rect_y-7.5, rect_y-7.5], color=PAPER, lw=1.2, zorder=4)

# ── Text ──────────────────────────────────────────────────────────────────────
ax.text(CX, 18, "TBS", color=PAPER, fontsize=22, ha="center", va="center",
        fontweight="bold", fontfamily="monospace", zorder=6)
ax.text(CX, 12, "No.1", color=CYAN_LITE, fontsize=11, ha="center", va="center",
        fontfamily="monospace", zorder=6)

# ── Save ──────────────────────────────────────────────────────────────────────
out = "favicon.png"
fig.savefig(out, dpi=100, bbox_inches="tight", pad_inches=0,
            facecolor=PRU_DEEP)
plt.close(fig)
print(f"  → {out}  Done.")
