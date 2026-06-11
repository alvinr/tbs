#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_logo_final.py  — v3
Changes from v2:
  • Container shown as cross-section — long axis horizontal, pinhole in left
    end wall, image projected on right end wall, light rays inside
  • Subject figure larger (sc=1.15)
  • Inverted figure clearly drawn on image plane (upside-down Haring)
  • More vibrant / saturated cyanotype palette
  • Container exterior silhouette with corrugation ribs and corner castings
  • GPC badge repositioned; light-source circle bleeds off top-right corner
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (FancyBboxPatch, Circle, Rectangle,
                                 Ellipse, Arc)
from matplotlib.colors import LinearSegmentedColormap
from tbs_constants import C_WID, PROJECT_ROOT

# ── Vibrant cyanotype palette ─────────────────────────────────────────────────
PRU_INK   = "#081A32"
PRU_DEEP  = "#0F2D5E"
PRU_MID   = "#1755A0"
PRU_LIGHT = "#2E82D4"
CYAN_MID  = "#45B0E8"
CYAN_LITE = "#7ED4F2"
PAPER     = "#E4F4FD"
PAPER_W   = "#F0FAFF"
OUTLINE   = "#060F1E"
LW_H = 3.8
LW_D = 1.8

fig, ax = plt.subplots(figsize=(10, 10))
fig.patch.set_facecolor(PRU_DEEP)
ax.set_facecolor(PRU_DEEP)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_aspect("equal")
ax.axis("off")

# ── Tonal wash ────────────────────────────────────────────────────────────────
np.random.seed(7)
xs, ys = np.linspace(0,100,300), np.linspace(0,100,300)
XX, YY = np.meshgrid(xs, ys)
bg = sum(np.exp(-((XX-cx)**2+(YY-cy)**2)/(2*r**2))
         for cx,cy,r in [(25,75,30),(70,40,38),(50,55,22),(15,30,18),(80,80,28)])
bg = (bg-bg.min())/(bg.max()-bg.min())
cmap_c = LinearSegmentedColormap.from_list(
    "cy", [PRU_INK, PRU_DEEP, PRU_MID, PRU_LIGHT], N=256)
ax.imshow(bg, extent=[0,100,0,100], origin="lower",
          cmap=cmap_c, alpha=0.45, zorder=0, aspect="auto")

# ── Light-source bleed — top-right corner ────────────────────────────────────
for r_, a_, col_ in [(44,0.28,PRU_MID),(32,0.35,PRU_LIGHT),
                      (20,0.42,CYAN_MID),(11,0.50,CYAN_LITE)]:
    ax.add_patch(Circle((98,98), r_, fc=col_, ec=PAPER,
                         lw=0.8, alpha=a_, zorder=2, clip_on=True))
for ang in np.linspace(190, 270, 9):
    rad = np.radians(ang)
    ax.plot([98+44*np.cos(rad), 98+51*np.cos(rad)],
            [98+44*np.sin(rad), 98+51*np.sin(rad)],
            color=PAPER, lw=1.4, alpha=0.5, solid_capstyle="round", zorder=3)

# ── Triple border ─────────────────────────────────────────────────────────────
for ins, col, lw in [(0.8,PAPER,4.0),(2.0,OUTLINE,2.5),(3.2,PAPER,1.0)]:
    ax.add_patch(Rectangle((ins,ins),100-2*ins,100-2*ins,
                            fc="none", ec=col, lw=lw, zorder=9))

# ── Film sprocket strips ──────────────────────────────────────────────────────
for sx in [7.0, 93.0]:
    ax.add_patch(Rectangle((sx-2.8,8),5.6,84,
                            fc=PRU_INK, ec=PAPER, lw=1.5, zorder=3))
    for hy in np.linspace(13,87,11):
        ax.add_patch(FancyBboxPatch((sx-1.6,hy-1.8),3.2,3.6,
                                    boxstyle="round,pad=0.3",
                                    fc=PRU_MID, ec=PAPER, lw=0.8, zorder=4))

# ── Bauhaus triangle ──────────────────────────────────────────────────────────
ax.add_patch(plt.Polygon([(12,8),(30,8),(21,24)],
                          fc=PRU_INK, ec=PAPER, lw=LW_D, zorder=3, alpha=0.8))

# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER CROSS-SECTION — the camera
# Viewed looking ALONG the 20ft length from one end.
# Left/right walls = the 20ft × 8.5ft LONG SIDES (pinhole + image plane).
# Top/bottom bands = floor/ceiling panels. Width C_L→C_R = focal length (~8ft).
# ═══════════════════════════════════════════════════════════════════════════════
C_L  = 36      # interior left  (pinhole wall = 20ft long side, seen edge-on)
C_R  = 62      # interior right (image plane  = 20ft long side, seen edge-on)
C_B  = 44      # interior bottom (floor)  — shifted +8 to clear spec bar
C_T  = 72      # interior top   (ceiling) — shifted +8
# Interior: 26 units wide ≈ 2362mm focal length
#           28 units tall ≈ 2388mm container internal height
WT   = 2.5     # wall thickness
CY   = (C_B + C_T) / 2   # center Y = 50
CX   = (C_L + C_R) / 2   # center X = 49
PH_X = C_L                # pinhole x (left long-side wall inner face)
IP_X = C_R                # image plane x (right long-side wall inner face)

# ── Exterior silhouette (container hull) ──────────────────────────────────────
EX_L = C_L - WT*2    # = 31
EX_R = C_R + WT*2    # = 67
EX_B = C_B - WT*1.5  # ≈ 32.25
EX_T = C_T + WT*1.5  # ≈ 67.75

ax.add_patch(Rectangle((EX_L, EX_B), EX_R-EX_L, EX_T-EX_B,
                        fc=PRU_MID, ec=PAPER, lw=2.8, zorder=4))

# Corrugation ribs on top/bottom hull bands (floor/ceiling, run into page)
for rx in np.arange(EX_L+2, EX_R, 2.8):
    ax.plot([rx,rx],[C_T, EX_T], color=PRU_LIGHT, lw=0.9, alpha=0.65, zorder=5)
    ax.plot([rx,rx],[C_B, EX_B], color=PRU_LIGHT, lw=0.9, alpha=0.65, zorder=5)

# Corrugation detail on left/right exterior wall faces (the 20ft long-side panels)
for ry in np.arange(EX_B+3, EX_T, 3.5):
    ax.plot([EX_L, C_L],[ry, ry], color=PRU_LIGHT, lw=0.8, alpha=0.50, zorder=5)
    ax.plot([C_R, EX_R],[ry, ry], color=PRU_LIGHT, lw=0.8, alpha=0.50, zorder=5)

# Corner castings (ISO container)
for cx_, cy_, cw, ch in [
    (EX_L, EX_B, 3.2, 2.2), (EX_R-3.2, EX_B, 3.2, 2.2),
    (EX_L, EX_T-2.2, 3.2, 2.2), (EX_R-3.2, EX_T-2.2, 3.2, 2.2)]:
    ax.add_patch(Rectangle((cx_,cy_),cw,ch,
                            fc=CYAN_MID, ec=PAPER, lw=1.2, zorder=6))
    ax.add_patch(Ellipse((cx_+cw/2, cy_+ch/2), cw*0.55, ch*0.6,
                          fc=PRU_INK, ec=PAPER, lw=0.6, zorder=7))

# Container ID tag
ax.text((EX_L+EX_R)/2, EX_T-0.7, "TBS-001  ·  20FT  ISO  CAMERA",
        color=PAPER, fontsize=4.8, ha="center", va="top",
        fontfamily="monospace", alpha=0.85, zorder=7)

# ── Interior space ────────────────────────────────────────────────────────────
ax.add_patch(Rectangle((C_L, C_B), C_R-C_L, C_T-C_B,
                        fc=PRU_INK, ec="none", zorder=5))

# ── Left wall (pinhole wall = 20ft long side, seen edge-on) ──────────────────
ax.add_patch(Rectangle((EX_L, C_B), WT*2, C_T-C_B,
                        fc=PRU_MID, ec="none", zorder=5))
ax.add_patch(Rectangle((EX_L, C_B), WT*2, C_T-C_B,
                        fc="none", ec=PAPER, lw=1.5, zorder=6))

# Pinhole — HOLE IN THE WALL
# Outer glow (light leaking through)
for r_, a_ in [(5.5,0.12),(4.0,0.20),(2.8,0.35),(1.8,0.60)]:
    ax.add_patch(Circle((PH_X, CY), r_,
                         fc=PAPER_W, ec="none", alpha=a_, zorder=7))
# The aperture ring
ax.add_patch(Circle((PH_X, CY), 1.8,
                     fc=PRU_LIGHT, ec=PAPER, lw=1.8, zorder=8))
# The actual hole (dark center)
ax.add_patch(Circle((PH_X, CY), 0.7,
                     fc=PRU_INK, ec=PAPER_W, lw=0.8, zorder=9))
# Crosshair
for ddx, ddy in [(0,2.5),(0,-2.5),(2.5,0),(-2.5,0)]:
    ax.plot([PH_X, PH_X+ddx*0.5], [CY, CY+ddy*0.5],
            color=PAPER, lw=0.8, alpha=0.6, zorder=9)

ax.text(PH_X, C_B-1.5, "Ø 2.17mm",
        color=CYAN_LITE, fontsize=4.8, ha="center", va="top",
        fontfamily="monospace", zorder=7)

# ── Right wall (image plane = 20ft long side, seen edge-on) ──────────────────
# Image plane wall — lighter to suggest exposed/printing-out surface
ax.add_patch(Rectangle((C_R, C_B), WT*2, C_T-C_B,
                        fc=CYAN_LITE, ec=PAPER, lw=1.8, zorder=5, alpha=0.75))

# "EXPOSED" texture on image plane
for ry in np.arange(C_B+1, C_T, 1.6):
    ax.plot([C_R, C_R+WT*1.5],[ry,ry],
            color=PRU_MID, lw=0.5, alpha=0.4, zorder=6)

ax.text(IP_X+WT*1.0, C_B-1.5, "IMAGE PLANE",
        color=CYAN_LITE, fontsize=4.8, ha="center", va="top",
        fontfamily="monospace", zorder=7)

# ── INVERTED FIGURE on image plane ────────────────────────────────────────────
# Drawn upside-down in PRU_INK against the lighter wall — clearly visible
def haring_inverted(ax, cx, cy, sc):
    """True upside-down mirror of haring_upright: every dy → -dy, every dx → -dx."""
    lw = 2.8*sc
    col = PRU_INK
    # Head at BOTTOM  (was cy+6 → cy-6)
    ax.add_patch(Circle((cx, cy-6*sc), 2.5*sc,
                         fc=col, ec=PAPER, lw=lw*0.7, zorder=11))
    # Body  (was cy+3 → cy-3.5  →  now cy-3 → cy+3.5)
    ax.plot([cx, cx], [cy-3.0*sc, cy+3.5*sc],
            color=PAPER, lw=lw*2.0, solid_capstyle="round", zorder=10)
    ax.plot([cx, cx], [cy-3.0*sc, cy+3.5*sc],
            color=col, lw=lw*1.3, solid_capstyle="round", zorder=11)
    # Arms — Λ shape pointing DOWN  (upright has V pointing up at cy+1.5→cy+3.5)
    ax.plot([cx-4.5*sc, cx, cx+4.5*sc],
            [cy-1.5*sc, cy-3.5*sc, cy-1.5*sc],
            color=PAPER, lw=lw*2.0, solid_capstyle="round",
            solid_joinstyle="round", zorder=10)
    ax.plot([cx-4.5*sc, cx, cx+4.5*sc],
            [cy-1.5*sc, cy-3.5*sc, cy-1.5*sc],
            color=col, lw=lw*1.3, solid_capstyle="round",
            solid_joinstyle="round", zorder=11)
    # Legs pointing UP  (was pointing down to cy-8.5 → now up to cy+8.5)
    # Both legs start at body center cx — same as upright figure hip point
    for lx in [-2*sc, 2*sc]:
        ax.plot([cx, cx+lx*1.3], [cy+3.5*sc, cy+8.5*sc],
                color=PAPER, lw=lw*2.0, solid_capstyle="round", zorder=10)
        ax.plot([cx, cx+lx*1.3], [cy+3.5*sc, cy+8.5*sc],
                color=col, lw=lw*1.3, solid_capstyle="round", zorder=11)
    # Radiant marks below head (was above: 30–155° → now below: 210–335°)
    for ang in np.linspace(210, 335, 5):
        rad_ = np.radians(ang)
        r0, r1 = 3.0*sc, 5.0*sc
        ax.plot([cx+r0*np.cos(rad_), cx+r1*np.cos(rad_)],
                [cy-6*sc+r0*np.sin(rad_), cy-6*sc+r1*np.sin(rad_)],
                color=PAPER, lw=1.0, alpha=0.6, solid_capstyle="round", zorder=11)

haring_inverted(ax, IP_X+WT*1.0, CY, sc=0.72)

# ── Light rays inside container: subject→pinhole→image plane ─────────────────
SUBJ_X = 18.0   # clear of sprocket strip (right edge ≈ 9.8 + arm reach 5.2 = needs ≥16)
SUBJ_H = 9.0   # subject half-height for ray origin points (spans ~2/3 container height)

# Three source points on subject, three inverted destination points on image plane
ray_pairs = [
    ((SUBJ_X, CY+SUBJ_H), (IP_X+0.5, CY-SUBJ_H*0.65)),  # top→bottom (inverted)
    ((SUBJ_X, CY),         (IP_X+0.5, CY)),               # center→center
    ((SUBJ_X, CY-SUBJ_H), (IP_X+0.5, CY+SUBJ_H*0.65)),  # bottom→top (inverted)
]
for (sx,sy),(ix,iy) in ray_pairs:
    # Incoming ray: source → pinhole (outside container, in scene space)
    ax.annotate("", xy=(PH_X, CY), xytext=(sx, sy),
                arrowprops=dict(arrowstyle="-|>", color=CYAN_MID,
                                lw=1.0, mutation_scale=7, alpha=0.80), zorder=5)
    # Interior ray: pinhole → image plane (dashed, inside container)
    ax.plot([PH_X, ix],[CY, iy],
            color=CYAN_LITE, lw=1.0, ls="--", alpha=0.65, zorder=6,
            dash_capstyle="round")
    # Dot at image plane intersection
    ax.add_patch(Circle((ix, iy), 0.4, fc=CYAN_LITE, ec="none", zorder=7, alpha=0.9))

# Interior glow from pinhole (light entering)
for ang in np.linspace(-45, 45, 7):
    rad = np.radians(ang)
    ax.plot([PH_X, PH_X+6*np.cos(rad)],[CY, CY+6*np.sin(rad)],
            color=PAPER_W, lw=0.7, alpha=0.25, zorder=6,
            solid_capstyle="round")

# Camera tripod — centerd under container at CX=49
for tx,ty in [(43,30),(49,29),(55,30)]:
    ax.plot([CX,tx],[EX_B,ty], color=PAPER, lw=LW_D*1.4, solid_capstyle="round", zorder=5)
ax.plot([40,58],[29.5,29.5], color=PAPER, lw=LW_D, zorder=5)

# Focal length arrow inside container
fl_y = C_B+1.5
ax.annotate("", xy=(C_R, fl_y), xytext=(C_L, fl_y),
            arrowprops=dict(arrowstyle="<->", color=CYAN_MID, lw=0.9,
                            mutation_scale=7), zorder=7)
ax.text((C_L+C_R)/2, fl_y+1.2, f"FOCAL LENGTH  {C_WID}mm",
        color=CYAN_MID, fontsize=5.0, ha="center", va="bottom",
        fontfamily="monospace", zorder=7)

# ── GPC BADGE — lower center, below tripod ────────────────────────────────────
ax.add_patch(Circle((CX, 21), 6.0, fc=PRU_MID, ec=PAPER, lw=2.2, zorder=8))
ax.add_patch(Circle((CX, 21), 5.0, fc=PRU_LIGHT, ec=CYAN_MID, lw=0.9, zorder=9))
ax.text(CX, 21.5, "TBS", color=PAPER, fontsize=8.5, ha="center", va="center",
        fontweight="bold", fontfamily="monospace", zorder=10)
ax.text(CX, 18.8, "No.1", color=CYAN_LITE, fontsize=4.8, ha="center", va="center",
        fontfamily="monospace", zorder=10)

# ═══════════════════════════════════════════════════════════════════════════════
# SUBJECT — larger Haring figure, far left
# ═══════════════════════════════════════════════════════════════════════════════
def haring_upright(ax, cx, cy, sc, col=PAPER):
    """Upright Haring figure — arms raised classic pose."""
    lw = 3.0*sc
    # Head
    ax.add_patch(Circle((cx, cy+6*sc), 2.8*sc,
                         fc=col, ec=OUTLINE, lw=lw*0.8, zorder=8))
    # Body
    ax.plot([cx,cx],[cy+3.0*sc, cy-3.5*sc],
            color=OUTLINE, lw=lw*2.0, solid_capstyle="round", zorder=7)
    ax.plot([cx,cx],[cy+3.0*sc, cy-3.5*sc],
            color=col, lw=lw*1.3, solid_capstyle="round", zorder=8)
    # Arms raised
    ax.plot([cx-4.5*sc, cx, cx+4.5*sc],
            [cy+1.5*sc, cy+3.5*sc, cy+1.5*sc],
            color=OUTLINE, lw=lw*2.0, solid_capstyle="round",
            solid_joinstyle="round", zorder=7)
    ax.plot([cx-4.5*sc, cx, cx+4.5*sc],
            [cy+1.5*sc, cy+3.5*sc, cy+1.5*sc],
            color=col, lw=lw*1.3, solid_capstyle="round",
            solid_joinstyle="round", zorder=8)
    # Legs
    for lx in [-2*sc, 2*sc]:
        ax.plot([cx, cx+lx*1.3],[cy-3.5*sc, cy-8.5*sc],
                color=OUTLINE, lw=lw*2.0, solid_capstyle="round", zorder=7)
        ax.plot([cx, cx+lx*1.3],[cy-3.5*sc, cy-8.5*sc],
                color=col, lw=lw*1.3, solid_capstyle="round", zorder=8)
    # Radiant marks
    for ang in np.linspace(30, 155, 5):
        rad_ = np.radians(ang)
        r0,r1 = 4.0*sc, 6.5*sc
        ax.plot([cx+r0*np.cos(rad_), cx+r1*np.cos(rad_)],
                [cy+6*sc+r0*np.sin(rad_), cy+6*sc+r1*np.sin(rad_)],
                color=col, lw=1.2, alpha=0.8, solid_capstyle="round", zorder=7)

haring_upright(ax, SUBJ_X, CY, sc=1.15, col=PAPER)
ax.text(SUBJ_X, CY-22, "SUBJECT\n3440mm",
        color=CYAN_LITE, fontsize=4.8, ha="center", va="top",
        fontfamily="monospace")

# ═══════════════════════════════════════════════════════════════════════════════
# OPERATOR A — left of container, dynamic lean toward pinhole
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════
# TYPOGRAPHY
# ═══════════════════════════════════════════════════════════════════════════════
# Title
ax.add_patch(Rectangle((12,91),76,6.8, fc=PRU_INK,ec=PAPER,lw=2.2,zorder=8))
ax.add_patch(Rectangle((12,90.2),76,0.7, fc=PAPER,ec="none",zorder=8))
ax.add_patch(Rectangle((12,89.5),76,0.4, fc=CYAN_MID,ec="none",zorder=8))
ax.text(50, 94.5, "THE  BIG  SHOEBOX  PROJECT",
        color=PAPER, fontsize=13.0, ha="center", va="center",
        fontweight="bold", fontfamily="monospace", zorder=9)
ax.text(50, 88.2,
        "CAMERA  RESEARCH  DIVISION  ·  FIELD  UNIT  No.1  ·  CYANOTYPE  PROCESS",
        color=CYAN_LITE, fontsize=6.0, ha="center", va="center",
        fontfamily="monospace", zorder=8)

# Spec bar — two lines to fit all specs
ax.add_patch(Rectangle((12,5.5),76,7.5, fc=PRU_INK,ec=PAPER,lw=1.8,zorder=8))
ax.add_patch(Rectangle((12,12.8),76,0.6, fc=PAPER,ec="none",zorder=9))
ax.add_patch(Rectangle((12,12.1),76,0.4, fc=CYAN_MID,ec="none",zorder=9))
ax.text(50, 10.6,
        "f = 2362mm   ·   d = 2.17mm   ·   f/1088   ·   λ = 550 nm",
        color=PAPER, fontsize=5.8, ha="center", va="center",
        fontfamily="monospace", fontweight="bold", zorder=9)
ax.text(50, 7.5,
        "IMAGE  PLANE  5893 × 2388mm   ·   MIN. FOCUS DIST.  5000mm",
        color=CYAN_LITE, fontsize=5.8, ha="center", va="center",
        fontfamily="monospace", fontweight="bold", zorder=9)

# Side strips
ax.text(4.8, 50, "CYANOTYPE  PROCESS",
        color=PAPER, fontsize=5.0, ha="center", va="center",
        rotation=90, fontfamily="monospace", alpha=0.75, zorder=5)
ax.text(95.2, 50, "THE  BIG  SHOEBOX  PROJECT",
        color=PAPER, fontsize=5.0, ha="center", va="center",
        rotation=270, fontfamily="monospace", alpha=0.75, zorder=5)

# Corner registration marks
for cx_,cy_ in [(14,14),(86,14),(14,86),(86,86)]:
    sx_,sy_ = (1 if cx_<50 else -1), (1 if cy_<50 else -1)
    ax.plot([cx_,cx_+3.5*sx_],[cy_,cy_], color=PAPER,lw=1.4,alpha=0.6,zorder=9)
    ax.plot([cx_,cx_],[cy_,cy_+3.5*sy_], color=PAPER,lw=1.4,alpha=0.6,zorder=9)

_out = os.path.join(PROJECT_ROOT, "logo-final.png")
fig.savefig(_out, dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close(fig)
print(f"  → {_out}  Done.")
