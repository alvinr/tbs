#!/usr/bin/env python3
"""
generate_logo_final.py
Combo of Options 2 + 3 in cyanotype colour treatment.
Haring-bold outlines, IBM Research Division composition,
Bauhaus geometry — all in Prussian blue / paper-white cyanotype palette.

Output: logo-final.png  (1200×1200 px @ 150 dpi)
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Ellipse, Arc, Wedge
from matplotlib.path import Path
import matplotlib.patheffects as pe

# ── Cyanotype palette ─────────────────────────────────────────────────────────
PRU_INK   = "#0B1F3A"   # darkest — fully exposed (ink)
PRU_DEEP  = "#0D2B55"   # deep prussian blue
PRU_MID   = "#1A4A7A"   # mid prussian blue
PRU_LIGHT = "#2E6EA6"   # lighter blue
CYAN_MID  = "#4A90C4"   # cyanotype highlight blue
CYAN_LITE = "#8ABFD6"   # light cyanotype
PAPER     = "#E8F3F8"   # near-white — unexposed paper
PAPER_W   = "#F4FAFC"   # brightest white
OUTLINE   = PRU_INK     # Haring outline colour

LW_H  = 4.5   # Haring line weight (figures)
LW_D  = 2.2   # detail line weight

def save(fig, fname, dpi=150):
    fig.savefig(fname, dpi=dpi, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  → {fname}")

# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(10, 10))
fig.patch.set_facecolor(PRU_DEEP)
ax.set_facecolor(PRU_DEEP)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_aspect("equal")
ax.axis("off")

# ── Tonal background wash — suggests cyanotype unevenness ──
from matplotlib.colors import LinearSegmentedColormap
bg_data = np.zeros((200, 200))
np.random.seed(42)
for _ in range(60):
    cx_, cy_ = np.random.uniform(10, 90, 2)
    r_ = np.random.uniform(8, 35)
    for i in range(200):
        for j in range(200):
            pass  # skip slow loop — use vectorised below
xs = np.linspace(0, 100, 200)
ys = np.linspace(0, 100, 200)
XX, YY = np.meshgrid(xs, ys)
bg = np.zeros_like(XX)
for _ in range(8):
    cx_, cy_ = np.random.uniform(20, 80, 2)
    r_ = np.random.uniform(15, 40)
    bg += np.exp(-((XX - cx_)**2 + (YY - cy_)**2) / (2 * r_**2))
bg = (bg - bg.min()) / (bg.max() - bg.min())

cmap_cyan = LinearSegmentedColormap.from_list(
    "cyanotype", [PRU_INK, PRU_DEEP, PRU_MID, PRU_LIGHT], N=256)
ax.imshow(bg, extent=[0, 100, 0, 100], origin="lower", cmap=cmap_cyan,
          alpha=0.55, zorder=0, aspect="auto")

# ── Outer border — triple rule (cyanotype contact-print style) ──
for inset, col, lw in [(1, PAPER, 4), (2.5, PRU_INK, 2.5), (3.8, PAPER, 1.2)]:
    ax.add_patch(Rectangle((inset, inset), 100 - 2*inset, 100 - 2*inset,
                            fc="none", ec=col, lw=lw, zorder=8))

# ── Film sprocket strips — sides ──
for sx in [7.5, 92.5]:
    ax.add_patch(Rectangle((sx - 2.8, 8), 5.6, 84,
                            fc=PRU_INK, ec=PAPER, lw=1.5, zorder=3))
    for hy in np.linspace(14, 86, 10):
        ax.add_patch(FancyBboxPatch((sx - 1.6, hy - 1.8), 3.2, 3.6,
                                    boxstyle="round,pad=0.3",
                                    fc=PRU_MID, ec=PAPER, lw=0.8, zorder=4))

# ── Bauhaus geometry — background shapes in tonal blues ──
# Large exposed circle (sun / light source)
ax.add_patch(Circle((72, 70), 24, fc=PRU_LIGHT, ec=PAPER, lw=2.5, alpha=0.55, zorder=2))
ax.add_patch(Circle((72, 70), 18, fc=CYAN_MID, ec=PAPER, lw=1.5, alpha=0.4, zorder=2))
ax.add_patch(Circle((72, 70), 10, fc=CYAN_LITE, ec=PAPER, lw=1.2, alpha=0.35, zorder=2))

# Bauhaus triangle (bottom left — deep shadow zone)
tri = plt.Polygon([(12, 10), (34, 10), (23, 30)],
                  fc=PRU_INK, ec=PAPER, lw=LW_D, zorder=3, alpha=0.8)
ax.add_patch(tri)

# ── CAMERA BODY — bold geometric (centre) ──
# Body rectangle
ax.add_patch(FancyBboxPatch((36, 44), 28, 18,
                            boxstyle="round,pad=1.2",
                            fc=PRU_INK, ec=PAPER, lw=LW_H, zorder=6))
# Pinhole face (left)
ax.add_patch(Circle((36, 53), 6.5, fc=PRU_MID, ec=PAPER, lw=LW_H, zorder=7))
ax.add_patch(Circle((36, 53), 1.2, fc=PAPER, ec=PAPER, lw=1, zorder=8))

# Haring radiant marks from pinhole (left-side rays — light entering)
for ang in np.linspace(130, 230, 7):
    rad = np.radians(ang)
    x0 = 36 + 8.5 * np.cos(rad)
    y0 = 53 + 8.5 * np.sin(rad)
    x1 = 36 + 15  * np.cos(rad)
    y1 = 53 + 15  * np.sin(rad)
    ax.plot([x0, x1], [y0, y1], color=PAPER, lw=LW_D * 1.2,
            solid_capstyle="round", zorder=7)

# Image plane face (right) — hatched to suggest exposed surface
ax.add_patch(Circle((64, 53), 6.5, fc=CYAN_LITE, ec=PAPER, lw=LW_H, zorder=7))
for i in range(6):
    ang_r = np.radians(30 * i)
    ax.plot([64 + 0, 64 + 5*np.cos(ang_r)],
            [53 + 0, 53 + 5*np.sin(ang_r)],
            color=PRU_INK, lw=1.2, zorder=8, alpha=0.7)

# f-number label on camera body
ax.text(50, 57, "f/1088", color=PAPER, fontsize=8.5, ha="center", va="center",
        fontweight="bold", fontfamily="monospace", zorder=8)
ax.text(50, 53, "Ø 2.17 mm", color=CYAN_LITE, fontsize=6.5, ha="center", va="center",
        fontfamily="monospace", zorder=8)

# Camera tripod
for tx, ty in [(44, 32), (50, 31), (56, 32)]:
    ax.plot([50, tx], [44, ty], color=PAPER, lw=LW_D * 1.5,
            solid_capstyle="round", zorder=5)
ax.plot([42, 58], [31.5, 31.5], color=PAPER, lw=LW_D, zorder=5)


# ── HARING-STYLE FIGURE — SCIENTIST LEFT ──────────────────────────────────────
def scientist(ax, cx, cy, sc=1.0, facing="right",
              body_col=PAPER, head_col=PAPER, detail_col=CYAN_LITE,
              clipboard=False):
    lw = LW_H * sc
    flip = 1 if facing == "right" else -1

    # Lab coat body — Haring bold fill
    ax.add_patch(FancyBboxPatch((cx - 6*sc, cy - 14*sc), 12*sc, 18*sc,
                                boxstyle=f"round,pad={0.8*sc:.2f}",
                                fc=body_col, ec=OUTLINE, lw=lw, zorder=6))
    # Lapels
    ax.plot([cx - 6*sc, cx - 1.5*sc], [cy + 4*sc, cy - 4*sc],
            color=PRU_MID, lw=lw*0.6, zorder=7)
    ax.plot([cx + 6*sc, cx + 1.5*sc], [cy + 4*sc, cy - 4*sc],
            color=PRU_MID, lw=lw*0.6, zorder=7)

    # Pocket protector
    px = cx - 4.5*sc * flip
    ax.add_patch(Rectangle((px - 1.8*sc, cy - 9*sc), 3.6*sc, 5*sc,
                            fc=PRU_MID, ec=OUTLINE, lw=lw*0.5, zorder=7))
    for pi, pxi in enumerate([px - 1.0*sc, px + 0.0*sc, px + 1.0*sc]):
        ax.plot([pxi, pxi], [cy - 9*sc, cy - 4.5*sc],
                color=PAPER if pi != 1 else CYAN_LITE,
                lw=lw * 0.7, zorder=8, solid_capstyle="round")

    # Head
    ax.add_patch(Circle((cx, cy + 9*sc), 5.5*sc,
                         fc=head_col, ec=OUTLINE, lw=lw, zorder=6))
    # Glasses — Haring style (bold circles)
    for gx in [cx - 2.3*sc, cx + 1.5*sc]:
        ax.add_patch(Circle((gx, cy + 9.5*sc), 2*sc,
                             fc=CYAN_LITE, ec=OUTLINE, lw=lw*0.7, alpha=0.6, zorder=7))
        ax.add_patch(Circle((gx, cy + 9.5*sc), 2*sc,
                             fc="none", ec=OUTLINE, lw=lw*0.7, zorder=8))
    ax.plot([cx - 0.3*sc, cx + 1.5*sc - 2*sc],
            [cy + 9.5*sc, cy + 9.5*sc],
            color=OUTLINE, lw=lw*0.6, zorder=8)
    # Hair (Haring — bold arc)
    ax.add_patch(Arc((cx, cy + 10*sc), 11*sc, 8*sc,
                     theta1=0, theta2=180, color=OUTLINE, lw=lw*1.2, zorder=8))

    # Arms
    if clipboard:
        # Right arm holds clipboard
        ax.plot([cx + 6*sc, cx + 12*sc, cx + 13*sc],
                [cy + 2*sc, cy - 2*sc, cy - 6*sc],
                color=OUTLINE, lw=lw*1.6, solid_capstyle="round",
                solid_joinstyle="round", zorder=5)
        ax.plot([cx + 6*sc, cx + 12*sc, cx + 13*sc],
                [cy + 2*sc, cy - 2*sc, cy - 6*sc],
                color=body_col, lw=lw*1.0, solid_capstyle="round",
                solid_joinstyle="round", zorder=6)
        # Clipboard
        ax.add_patch(FancyBboxPatch((cx + 11*sc, cy - 10*sc), 9*sc, 11*sc,
                                    boxstyle="round,pad=0.4",
                                    fc=PAPER, ec=OUTLINE, lw=lw*0.8, zorder=7))
        ax.add_patch(Rectangle((cx + 13.5*sc, cy + 0.5*sc), 3.5*sc, 1.2*sc,
                                fc=PRU_MID, ec=OUTLINE, lw=0.8, zorder=8))
        for ly in [cy - 2*sc, cy - 4*sc, cy - 6.5*sc]:
            ax.plot([cx + 11.8*sc, cx + 19.2*sc], [ly, ly],
                    color=PRU_MID, lw=0.8, zorder=8, alpha=0.7)
        # Left arm pointing at camera
        ax.plot([cx - 6*sc, cx - 12*sc],
                [cy + 2*sc, cy + 0*sc],
                color=OUTLINE, lw=lw*1.6, solid_capstyle="round", zorder=5)
        ax.plot([cx - 6*sc, cx - 12*sc],
                [cy + 2*sc, cy + 0*sc],
                color=body_col, lw=lw*1.0, solid_capstyle="round", zorder=6)
    else:
        # Left arm raised towards camera/pinhole
        ax.plot([cx - 6*sc, cx - 14*sc, cx - 18*sc],
                [cy + 2*sc, cy + 6*sc, cy + 4*sc],
                color=OUTLINE, lw=lw*1.6, solid_capstyle="round",
                solid_joinstyle="round", zorder=5)
        ax.plot([cx - 6*sc, cx - 14*sc, cx - 18*sc],
                [cy + 2*sc, cy + 6*sc, cy + 4*sc],
                color=body_col, lw=lw*1.0, solid_capstyle="round",
                solid_joinstyle="round", zorder=6)
        # Right arm down / gesturing
        ax.plot([cx + 6*sc, cx + 10*sc],
                [cy + 2*sc, cy - 4*sc],
                color=OUTLINE, lw=lw*1.6, solid_capstyle="round", zorder=5)
        ax.plot([cx + 6*sc, cx + 10*sc],
                [cy + 2*sc, cy - 4*sc],
                color=body_col, lw=lw*1.0, solid_capstyle="round", zorder=6)

    # Legs — striding Haring pose
    leg_L = np.array([[cx - 2*sc, cy - 14*sc],
                      [cx - 5*sc, cy - 22*sc],
                      [cx - 3*sc, cy - 28*sc]])
    leg_R = np.array([[cx + 2*sc, cy - 14*sc],
                      [cx + 6*sc, cy - 21*sc],
                      [cx + 7*sc, cy - 28*sc]])
    for pts in [leg_L, leg_R]:
        ax.plot(pts[:, 0], pts[:, 1], color=OUTLINE, lw=lw*1.6,
                solid_capstyle="round", solid_joinstyle="round", zorder=5)
        ax.plot(pts[:, 0], pts[:, 1], color=body_col, lw=lw*1.0,
                solid_capstyle="round", solid_joinstyle="round", zorder=6)
    # Shoes — Haring bold blobs
    for sx_, sy_ in [(cx - 3*sc, cy - 28*sc), (cx + 7*sc, cy - 28*sc)]:
        ax.add_patch(Ellipse((sx_, sy_ - 1*sc), 6*sc, 3*sc,
                              fc=PRU_INK, ec=OUTLINE, lw=lw*0.7, zorder=7))

    # Haring radiant dashes around head (energy/excitement)
    for ang in np.linspace(20, 160, 5):
        rad = np.radians(ang)
        r0, r1 = 6.5*sc, 9.5*sc
        ax.plot([cx + r0*np.cos(rad), cx + r1*np.cos(rad)],
                [cy + 9*sc + r0*np.sin(rad), cy + 9*sc + r1*np.sin(rad)],
                color=PAPER, lw=lw*0.6, solid_capstyle="round",
                zorder=5, alpha=0.8)


# Left scientist — facing camera, arm extended toward pinhole
scientist(ax, 22, 52, sc=0.92, facing="right",
          body_col=PAPER, head_col=PAPER, clipboard=False)

# Right scientist — clipboard, observing
scientist(ax, 78, 52, sc=0.92, facing="left",
          body_col=PAPER, head_col=PAPER, clipboard=True)

# ── TITLE BAND ────────────────────────────────────────────────────────────────
# Top black bar — IBM-style
ax.add_patch(Rectangle((12, 90.5), 76, 7.5,
                        fc=PRU_INK, ec=PAPER, lw=1.8, zorder=8))
# Double hairline rule below title
ax.add_patch(Rectangle((12, 89.5), 76, 0.8, fc=PAPER, ec="none", zorder=8))
ax.add_patch(Rectangle((12, 88.5), 76, 0.4, fc=CYAN_MID, ec="none", zorder=8))

ax.text(50, 94.5, "GIANT  PINHOLE  CAMERA",
        color=PAPER, fontsize=14.5, ha="center", va="center",
        fontweight="bold", zorder=9)

# Subtitle (typewriter-style, IBM monospace)
ax.text(50, 87, "CAMERA  RESEARCH  DIVISION  ·  FIELD  UNIT  No.1  ·  CYANOTYPE",
        color=CYAN_LITE, fontsize=6.8, ha="center", va="center",
        fontfamily="monospace", zorder=8)

# ── BOTTOM SPEC BAR ───────────────────────────────────────────────────────────
ax.add_patch(Rectangle((12, 6.5), 76, 6.5,
                        fc=PRU_INK, ec=PAPER, lw=1.5, zorder=8))
ax.add_patch(Rectangle((12, 12.8), 76, 0.6, fc=PAPER, ec="none", zorder=9))
ax.add_patch(Rectangle((12, 12.0), 76, 0.35, fc=CYAN_MID, ec="none", zorder=9))

specs = ("f = 2,362 mm   ·   d = 2.17 mm   ·   f/1088   ·   "
         "IMAGE PLANE  5,893 × 2,388 mm   ·   λ = 550 nm")
ax.text(50, 9.8, specs,
        color=PAPER, fontsize=6.5, ha="center", va="center",
        fontfamily="monospace", fontweight="bold", zorder=9)

# ── GPC MONOGRAM BADGE ────────────────────────────────────────────────────────
ax.add_patch(Circle((50, 20), 7.5, fc=PRU_MID, ec=PAPER, lw=2.5, zorder=6))
ax.add_patch(Circle((50, 20), 6.5, fc=PRU_LIGHT, ec=CYAN_MID, lw=1, zorder=7))
ax.text(50, 20.5, "GPC", color=PAPER, fontsize=9, ha="center", va="center",
        fontweight="bold", zorder=8)
ax.text(50, 17.5, "No.1", color=CYAN_LITE, fontsize=5.5, ha="center", va="center",
        fontfamily="monospace", zorder=8)

# ── Cyanotype "sun" radiant from light source — top of circle ──
for ang in np.linspace(30, 150, 9):
    rad = np.radians(ang)
    x0 = 72 + 26*np.cos(rad)
    y0 = 70 + 26*np.sin(rad)
    x1 = 72 + 32*np.cos(rad)
    y1 = 70 + 32*np.sin(rad)
    ax.plot([x0, x1], [y0, y1], color=PAPER, lw=1.8,
            solid_capstyle="round", zorder=5, alpha=0.7)

# ── Subtle "CYANOTYPE PROCESS" text running vertically along left sprocket ──
ax.text(5.5, 50, "CYANOTYPE  PROCESS", color=PAPER, fontsize=5.5,
        ha="center", va="center", rotation=90,
        fontfamily="monospace", alpha=0.8, zorder=5)
ax.text(94.5, 50, "GIANT  PINHOLE  CAMERA", color=PAPER, fontsize=5.5,
        ha="center", va="center", rotation=270,
        fontfamily="monospace", alpha=0.8, zorder=5)

# ── Corner registration marks (cyanotype contact print style) ──
for cx_, cy_, rot in [(14, 14, 0), (86, 14, 90), (14, 86, 270), (86, 86, 180)]:
    for dx, dy in [(0, 3.5), (3.5, 0)]:
        sign_x = 1 if cx_ < 50 else -1
        sign_y = 1 if cy_ < 50 else -1
        ax.plot([cx_, cx_ + dx*sign_x], [cy_, cy_ + dy*sign_y],
                color=PAPER, lw=1.5, alpha=0.7, zorder=8)

save(fig, "logo-final.png")
print("Done.")
