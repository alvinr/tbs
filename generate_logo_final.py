#!/usr/bin/env python3
"""
generate_logo_final.py  — v2
Cyanotype + Haring + IBM Research Division combo logo.
Changes from v1:
  • Lighter prussian palette
  • Camera body larger and more prominent
  • Dynamic scientist poses (individual code per figure)
  • Small subject figure (far left) with light-ray inversion diagram
  • Inverted figure on image plane inside camera
  • GPC badge repositioned inside camera
  • Light-source circle bleeds off top-right corner
  • All type in monospace
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (FancyBboxPatch, Circle, Rectangle,
                                 Ellipse, Arc, Wedge, FancyArrowPatch)
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as pe

# ── Cyanotype palette — shifted ~15% lighter than v1 ─────────────────────────
PRU_INK   = "#0E2647"
PRU_DEEP  = "#1A3F6F"   # main background
PRU_MID   = "#2A5C90"
PRU_LIGHT = "#3F7DB5"
CYAN_MID  = "#5FA3D0"
CYAN_LITE = "#A0CCDF"
PAPER     = "#EBF4F9"   # unexposed paper white
PAPER_W   = "#F6FBFD"
OUTLINE   = "#091D36"   # Haring outline
LW_H = 4.0              # Haring figure stroke
LW_D = 2.0

# ─────────────────────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(10, 10))
fig.patch.set_facecolor(PRU_DEEP)
ax.set_facecolor(PRU_DEEP)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_aspect("equal")
ax.axis("off")

# ── Cyanotype tonal wash ──────────────────────────────────────────────────────
np.random.seed(7)
xs = np.linspace(0, 100, 300)
ys = np.linspace(0, 100, 300)
XX, YY = np.meshgrid(xs, ys)
bg = np.zeros_like(XX)
seeds = [(25,75,30), (70,40,35), (50,55,20), (15,30,18), (80,80,25)]
for cx_,cy_,r_ in seeds:
    bg += np.exp(-((XX-cx_)**2+(YY-cy_)**2)/(2*r_**2))
bg = (bg - bg.min()) / (bg.max() - bg.min())
cmap_c = LinearSegmentedColormap.from_list(
    "cy", [PRU_INK, PRU_DEEP, PRU_MID, PRU_LIGHT], N=256)
ax.imshow(bg, extent=[0,100,0,100], origin="lower",
          cmap=cmap_c, alpha=0.50, zorder=0, aspect="auto")

# ── Light-source circle — BLEEDS off top-right corner ────────────────────────
for r_, a_ in [(38, 0.35), (28, 0.40), (18, 0.45), (10, 0.40)]:
    ax.add_patch(Circle((96, 96), r_,
                         fc=PRU_LIGHT if r_ > 20 else CYAN_MID,
                         ec=PAPER, lw=1.2, alpha=a_, zorder=2,
                         clip_on=True))
# Radiant dashes from circle
for ang in np.linspace(185, 270, 8):
    rad = np.radians(ang)
    ax.plot([96+40*np.cos(rad), 96+46*np.cos(rad)],
            [96+40*np.sin(rad), 96+46*np.sin(rad)],
            color=PAPER, lw=1.5, alpha=0.55, zorder=3,
            solid_capstyle="round")

# ── Triple border ─────────────────────────────────────────────────────────────
for ins, col, lw in [(1.0, PAPER, 3.5), (2.2, OUTLINE, 2.0), (3.2, PAPER, 1.0)]:
    ax.add_patch(Rectangle((ins, ins), 100-2*ins, 100-2*ins,
                            fc="none", ec=col, lw=lw, zorder=9))

# ── Film sprocket strips ──────────────────────────────────────────────────────
for sx in [7.2, 92.8]:
    ax.add_patch(Rectangle((sx-2.8, 8), 5.6, 84,
                            fc=PRU_INK, ec=PAPER, lw=1.5, zorder=3))
    for hy in np.linspace(13, 87, 11):
        ax.add_patch(FancyBboxPatch((sx-1.6, hy-1.8), 3.2, 3.6,
                                    boxstyle="round,pad=0.3",
                                    fc=PRU_MID, ec=PAPER, lw=0.8, zorder=4))

# ── Bauhaus triangle — bottom-left ───────────────────────────────────────────
ax.add_patch(plt.Polygon([(12,8),(30,8),(21,24)],
                          fc=PRU_INK, ec=PAPER, lw=LW_D, zorder=3, alpha=0.7))

# ═══════════════════════════════════════════════════════════════════════════════
# CAMERA — prominent, centred
# ═══════════════════════════════════════════════════════════════════════════════
CAM_CX, CAM_CY = 50, 54
CAM_W, CAM_H   = 38, 22

# Camera body
ax.add_patch(FancyBboxPatch((CAM_CX - CAM_W/2, CAM_CY - CAM_H/2),
                             CAM_W, CAM_H,
                             boxstyle="round,pad=1.0",
                             fc=PRU_INK, ec=PAPER, lw=LW_H, zorder=6))

# ── Pinhole face (left wall of camera) ───────────────────────────────────────
PH_X, PH_Y = CAM_CX - CAM_W/2, CAM_CY
ax.add_patch(Circle((PH_X, PH_Y), 7.5,
                     fc=PRU_MID, ec=PAPER, lw=LW_H, zorder=7))
ax.add_patch(Circle((PH_X, PH_Y), 4.5,
                     fc=PRU_LIGHT, ec=PAPER, lw=LW_D, zorder=8))
ax.add_patch(Circle((PH_X, PH_Y), 1.4,
                     fc=PAPER, ec=PAPER, lw=1, zorder=9))
# Crosshair on pinhole
for dx,dy in [(5,0),(-5,0),(0,5),(0,-5)]:
    ax.plot([PH_X, PH_X+dx*0.7], [PH_Y, PH_Y+dy*0.7],
            color=PAPER, lw=0.9, alpha=0.6, zorder=9)

# Haring radiant marks — outside pinhole, left side (incoming light)
for ang in np.linspace(135, 225, 8):
    rad = np.radians(ang)
    ax.plot([PH_X+9.5*np.cos(rad), PH_X+14*np.cos(rad)],
            [PH_Y+9.5*np.sin(rad), PH_Y+14*np.sin(rad)],
            color=PAPER, lw=LW_D*0.9, solid_capstyle="round",
            zorder=7, alpha=0.85)

# ── Focal length arrow inside camera ─────────────────────────────────────────
ax.annotate("", xy=(CAM_CX+CAM_W/2-2, CAM_CY-7),
            xytext=(CAM_CX-CAM_W/2+2, CAM_CY-7),
            arrowprops=dict(arrowstyle="<->", color=CYAN_LITE, lw=1.0,
                            mutation_scale=8), zorder=8)
ax.text(CAM_CX, CAM_CY-9.5, "f = 2,362 mm",
        color=CYAN_LITE, fontsize=5.5, ha="center", va="center",
        fontfamily="monospace", zorder=8)

# ── f/number label ────────────────────────────────────────────────────────────
ax.text(CAM_CX, CAM_CY+4, "f / 1088",
        color=PAPER, fontsize=9.5, ha="center", va="center",
        fontweight="bold", fontfamily="monospace", zorder=8)
ax.text(CAM_CX, CAM_CY+0.5, "d = 2.17 mm",
        color=CYAN_LITE, fontsize=6.0, ha="center", va="center",
        fontfamily="monospace", zorder=8)

# ── GPC BADGE — inside camera body ───────────────────────────────────────────
ax.add_patch(Circle((CAM_CX, CAM_CY-3.5), 5.5,
                     fc=PRU_MID, ec=PAPER, lw=1.8, zorder=8))
ax.add_patch(Circle((CAM_CX, CAM_CY-3.5), 4.5,
                     fc=PRU_LIGHT, ec=CYAN_MID, lw=0.8, zorder=9))
ax.text(CAM_CX, CAM_CY-3.0, "GPC",
        color=PAPER, fontsize=7, ha="center", va="center",
        fontweight="bold", fontfamily="monospace", zorder=10)
ax.text(CAM_CX, CAM_CY-5.5, "No.1",
        color=CYAN_LITE, fontsize=4.5, ha="center", va="center",
        fontfamily="monospace", zorder=10)

# ── Image plane face (right wall) ────────────────────────────────────────────
IP_X, IP_Y = CAM_CX + CAM_W/2, CAM_CY
ax.add_patch(Circle((IP_X, IP_Y), 7.5,
                     fc=CYAN_LITE, ec=PAPER, lw=LW_H, zorder=7, alpha=0.85))
# Hatching lines on image plane
for i in range(7):
    ang_r = np.radians(i * 25)
    ax.plot([IP_X, IP_X+6.5*np.cos(ang_r)],
            [IP_Y, IP_Y+6.5*np.sin(ang_r)],
            color=PRU_MID, lw=1.0, zorder=8, alpha=0.6)

# ── INVERTED SUBJECT FIGURE on image plane ────────────────────────────────────
# Tiny upside-down Haring figure rendered in PRU_INK on the CYAN_LITE circle
def tiny_haring(ax, cx, cy, sc, col, inverted=False):
    """Minimal Haring stick figure, optionally upside-down."""
    lw = 2.2 * sc
    flip = -1 if inverted else 1
    # Head
    ax.add_patch(Circle((cx, cy + flip*5.5*sc), 2.2*sc,
                         fc=col, ec=OUTLINE, lw=lw*0.8, zorder=11))
    # Body
    ax.plot([cx, cx], [cy + flip*3.2*sc, cy - flip*2.5*sc],
            color=col, lw=lw*1.6, solid_capstyle="round", zorder=10)
    ax.plot([cx, cx], [cy + flip*3.2*sc, cy - flip*2.5*sc],
            color=OUTLINE, lw=lw*2.0, solid_capstyle="round", zorder=9)
    # Arms raised (Haring classic)
    ax.plot([cx-3.5*sc, cx, cx+3.5*sc],
            [cy+flip*1.0*sc, cy+flip*1.5*sc, cy+flip*1.0*sc],
            color=OUTLINE, lw=lw*1.8, solid_capstyle="round", zorder=9,
            solid_joinstyle="round")
    ax.plot([cx-3.5*sc, cx, cx+3.5*sc],
            [cy+flip*1.0*sc, cy+flip*1.5*sc, cy+flip*1.0*sc],
            color=col, lw=lw*1.2, solid_capstyle="round", zorder=10,
            solid_joinstyle="round")
    # Legs
    for lx, la in [(-1.5, -3.0), (1.5, -3.0)]:
        ax.plot([cx, cx+lx*sc], [cy-flip*2.5*sc, cy-flip*la*sc],
                color=OUTLINE, lw=lw*1.8, solid_capstyle="round", zorder=9)
        ax.plot([cx, cx+lx*sc], [cy-flip*2.5*sc, cy-flip*la*sc],
                color=col, lw=lw*1.2, solid_capstyle="round", zorder=10)

# Inverted figure on image plane
tiny_haring(ax, IP_X, IP_Y, sc=0.55, col=PRU_INK, inverted=True)

# Label
ax.text(IP_X, IP_Y-10, "IMAGE\nPLANE\n(INVERTED)",
        color=CYAN_LITE, fontsize=4.8, ha="center", va="top",
        fontfamily="monospace", zorder=8)

# ── Camera tripod ─────────────────────────────────────────────────────────────
for tx,ty in [(43,32),(50,31),(57,32)]:
    ax.plot([50,tx],[CAM_CY-CAM_H/2,ty],
            color=PAPER, lw=LW_D*1.4, solid_capstyle="round", zorder=5)
ax.plot([40,60],[31.5,31.5], color=PAPER, lw=LW_D, zorder=5)

# ═══════════════════════════════════════════════════════════════════════════════
# SUBJECT — small Haring figure far left, being photographed
# ═══════════════════════════════════════════════════════════════════════════════
SUBJ_X, SUBJ_Y = 12, 56
tiny_haring(ax, SUBJ_X, SUBJ_Y, sc=0.80, col=PAPER, inverted=False)

ax.text(SUBJ_X, SUBJ_Y-13, "SUBJECT\n3,440 mm",
        color=CYAN_LITE, fontsize=4.8, ha="center", va="top",
        fontfamily="monospace", zorder=8)

# ── Light rays: subject → pinhole (three rays: top, centre, bottom) ───────────
subject_pts = [(SUBJ_X-2.5, SUBJ_Y+8), (SUBJ_X, SUBJ_Y+1), (SUBJ_X+2.5, SUBJ_Y-8)]
image_pts   = [(IP_X, IP_Y-5.5), (IP_X, IP_Y), (IP_X, IP_Y+5.5)]   # inverted on plane

for (sx,sy), (ix,iy) in zip(subject_pts, image_pts):
    # Subject → pinhole
    ax.annotate("", xy=(PH_X, PH_Y), xytext=(sx, sy),
                arrowprops=dict(arrowstyle="-|>", color=CYAN_MID,
                                lw=1.1, mutation_scale=7, alpha=0.80),
                zorder=5)
    # Pinhole → image plane (inverted — cross over)
    ax.annotate("", xy=(ix, iy), xytext=(PH_X, PH_Y),
                arrowprops=dict(arrowstyle="-|>", color=CYAN_LITE,
                                lw=1.1, mutation_scale=7,
                                linestyle="dashed", alpha=0.75),
                zorder=5)

# ═══════════════════════════════════════════════════════════════════════════════
# SCIENTIST LEFT — dynamic: leaning forward, arm fully extended to pinhole
# ═══════════════════════════════════════════════════════════════════════════════
SL_X, SL_Y = 23, 54

# Lab coat — body slightly tilted (shifted top-right)
ax.add_patch(FancyBboxPatch((SL_X-5.5, SL_Y-13), 11, 17,
                            boxstyle=f"round,pad={0.7:.2f}",
                            fc=PAPER, ec=OUTLINE, lw=LW_H, zorder=6))
# Lapels
ax.plot([SL_X-5.5, SL_X-1.0], [SL_Y+4,  SL_Y-3], color=PRU_MID, lw=1.5, zorder=7)
ax.plot([SL_X+5.5, SL_X+1.0], [SL_Y+4,  SL_Y-3], color=PRU_MID, lw=1.5, zorder=7)
# Pocket protector
ax.add_patch(Rectangle((SL_X-4.5, SL_Y-8), 3.8, 4.8,
                        fc=PRU_MID, ec=OUTLINE, lw=0.9, zorder=7))
for pi,pxi in enumerate([SL_X-3.8, SL_X-2.6, SL_X-1.4]):
    ax.plot([pxi,pxi],[SL_Y-8,SL_Y-4.0],
            color=PAPER if pi!=1 else CYAN_LITE, lw=1.6, zorder=8,
            solid_capstyle="round")

# Head — tilted forward
ax.add_patch(Circle((SL_X+1.5, SL_Y+9.5), 5.2,
                     fc=PAPER, ec=OUTLINE, lw=LW_H, zorder=6))
# Glasses
for gx in [SL_X-0.8, SL_X+2.8]:
    ax.add_patch(Circle((gx, SL_Y+10), 1.9,
                         fc=CYAN_LITE, ec=OUTLINE, lw=1.3, alpha=0.5, zorder=7))
    ax.add_patch(Circle((gx, SL_Y+10), 1.9,
                         fc="none", ec=OUTLINE, lw=1.3, zorder=8))
ax.plot([SL_X+0.9, SL_X+2.8-1.9], [SL_Y+10,SL_Y+10],
        color=OUTLINE, lw=1.0, zorder=8)
# Hair arc
ax.add_patch(Arc((SL_X+1.5, SL_Y+11), 10.5, 7,
                  theta1=0, theta2=180, color=OUTLINE, lw=LW_H*0.8, zorder=8))

# RIGHT ARM — reaching fully toward pinhole (dynamic, high angle)
arm_r = np.array([[SL_X+5.5, SL_Y+3],
                  [SL_X+10,  SL_Y+8],
                  [PH_X-1.5, PH_Y+1.5]])  # almost touches pinhole
ax.plot(arm_r[:,0], arm_r[:,1], color=OUTLINE, lw=LW_H*1.5,
        solid_capstyle="round", solid_joinstyle="round", zorder=5)
ax.plot(arm_r[:,0], arm_r[:,1], color=PAPER, lw=LW_H*0.95,
        solid_capstyle="round", solid_joinstyle="round", zorder=6)

# LEFT ARM — swung back for balance
arm_l = np.array([[SL_X-5.5, SL_Y+3],
                  [SL_X-11,  SL_Y+8],
                  [SL_X-14,  SL_Y+5]])
ax.plot(arm_l[:,0], arm_l[:,1], color=OUTLINE, lw=LW_H*1.5,
        solid_capstyle="round", solid_joinstyle="round", zorder=5)
ax.plot(arm_l[:,0], arm_l[:,1], color=PAPER, lw=LW_H*0.95,
        solid_capstyle="round", solid_joinstyle="round", zorder=6)

# LEGS — wide stride: right leg lunging forward toward camera
for pts, col in [
    (np.array([[SL_X+2, SL_Y-13],[SL_X+8, SL_Y-22],[SL_X+6, SL_Y-28]]), PAPER),
    (np.array([[SL_X-2, SL_Y-13],[SL_X-7, SL_Y-22],[SL_X-9, SL_Y-28]]), PAPER),
]:
    ax.plot(pts[:,0], pts[:,1], color=OUTLINE, lw=LW_H*1.5,
            solid_capstyle="round", solid_joinstyle="round", zorder=5)
    ax.plot(pts[:,0], pts[:,1], color=col, lw=LW_H*0.95,
            solid_capstyle="round", solid_joinstyle="round", zorder=6)
# Shoes
for sx_,sy_ in [(SL_X+6, SL_Y-28),(SL_X-9, SL_Y-28)]:
    ax.add_patch(Ellipse((sx_,sy_-1.2),7,2.8,
                          fc=PRU_INK, ec=OUTLINE, lw=LW_H*0.6, zorder=7))

# Radiant dashes around left scientist head
for ang in np.linspace(30, 175, 6):
    rad = np.radians(ang)
    r0,r1 = 7.0, 10.5
    ax.plot([SL_X+1.5+r0*np.cos(rad), SL_X+1.5+r1*np.cos(rad)],
            [SL_Y+9.5+r0*np.sin(rad), SL_Y+9.5+r1*np.sin(rad)],
            color=PAPER, lw=1.3, alpha=0.75, solid_capstyle="round", zorder=5)

# Label
ax.text(SL_X, SL_Y-33, "OPERATOR  A",
        color=CYAN_LITE, fontsize=5.2, ha="center",
        fontfamily="monospace", fontweight="bold")

# ═══════════════════════════════════════════════════════════════════════════════
# SCIENTIST RIGHT — dynamic: wide stance, clipboard raised, leaning back
# ═══════════════════════════════════════════════════════════════════════════════
SR_X, SR_Y = 77, 54

# Lab coat
ax.add_patch(FancyBboxPatch((SR_X-5.5, SR_Y-13), 11, 17,
                            boxstyle=f"round,pad={0.7:.2f}",
                            fc=PAPER, ec=OUTLINE, lw=LW_H, zorder=6))
ax.plot([SR_X-5.5, SR_X-1.0],[SR_Y+4,SR_Y-3], color=PRU_MID, lw=1.5, zorder=7)
ax.plot([SR_X+5.5, SR_X+1.0],[SR_Y+4,SR_Y-3], color=PRU_MID, lw=1.5, zorder=7)
# Pocket protector (right side)
ax.add_patch(Rectangle((SR_X+0.8, SR_Y-8), 3.8, 4.8,
                        fc=PRU_MID, ec=OUTLINE, lw=0.9, zorder=7))
for pi,pxi in enumerate([SR_X+1.5, SR_X+2.7, SR_X+3.9]):
    ax.plot([pxi,pxi],[SR_Y-8,SR_Y-4.0],
            color=PAPER if pi!=0 else CYAN_LITE, lw=1.6, zorder=8,
            solid_capstyle="round")

# Head — tilted back (excited reaction)
ax.add_patch(Circle((SR_X-1.5, SR_Y+10), 5.2,
                     fc=PAPER, ec=OUTLINE, lw=LW_H, zorder=6))
for gx in [SR_X-3.6, SR_X+0.0]:
    ax.add_patch(Circle((gx, SR_Y+10.5), 1.9,
                         fc=CYAN_LITE, ec=OUTLINE, lw=1.3, alpha=0.5, zorder=7))
    ax.add_patch(Circle((gx, SR_Y+10.5), 1.9,
                         fc="none", ec=OUTLINE, lw=1.3, zorder=8))
ax.plot([SR_X-1.7, SR_X+0.0-1.9],[SR_Y+10.5,SR_Y+10.5],
        color=OUTLINE, lw=1.0, zorder=8)
ax.add_patch(Arc((SR_X-1.5, SR_Y+11.5), 10.5, 7,
                  theta1=0, theta2=180, color=OUTLINE, lw=LW_H*0.8, zorder=8))

# LEFT ARM — raised high holding clipboard above head
clip_x, clip_y = SR_X+6, SR_Y+10
arm_rl = np.array([[SR_X+5.5, SR_Y+3],
                   [SR_X+10,  SR_Y+9],
                   [clip_x,   clip_y]])
ax.plot(arm_rl[:,0], arm_rl[:,1], color=OUTLINE, lw=LW_H*1.5,
        solid_capstyle="round", solid_joinstyle="round", zorder=5)
ax.plot(arm_rl[:,0], arm_rl[:,1], color=PAPER, lw=LW_H*0.95,
        solid_capstyle="round", solid_joinstyle="round", zorder=6)
# Clipboard
ax.add_patch(FancyBboxPatch((clip_x-0.5, clip_y), 8, 10.5,
                            boxstyle="round,pad=0.3",
                            fc=PAPER, ec=OUTLINE, lw=LW_H*0.7, zorder=7))
ax.add_patch(Rectangle((clip_x+2, clip_y+9.5), 3.5, 1.2,
                        fc=PRU_MID, ec=OUTLINE, lw=0.8, zorder=8))
for ly in [clip_y+7.5, clip_y+5.5, clip_y+3.0]:
    ax.plot([clip_x+0.5, clip_x+7], [ly,ly],
            color=PRU_MID, lw=0.8, zorder=8, alpha=0.7)

# RIGHT ARM — pointing toward camera (leaning away, arm outstretched)
arm_rr = np.array([[SR_X-5.5, SR_Y+3],
                   [SR_X-10,  SR_Y+2],
                   [IP_X+1.5, IP_Y+1.5]])
ax.plot(arm_rr[:,0], arm_rr[:,1], color=OUTLINE, lw=LW_H*1.5,
        solid_capstyle="round", solid_joinstyle="round", zorder=5)
ax.plot(arm_rr[:,0], arm_rr[:,1], color=PAPER, lw=LW_H*0.95,
        solid_capstyle="round", solid_joinstyle="round", zorder=6)

# LEGS — wide splayed stance
for pts in [
    np.array([[SR_X-3, SR_Y-13],[SR_X-10, SR_Y-20],[SR_X-14, SR_Y-27]]),
    np.array([[SR_X+3, SR_Y-13],[SR_X+8,  SR_Y-19],[SR_X+9,  SR_Y-27]]),
]:
    ax.plot(pts[:,0], pts[:,1], color=OUTLINE, lw=LW_H*1.5,
            solid_capstyle="round", solid_joinstyle="round", zorder=5)
    ax.plot(pts[:,0], pts[:,1], color=PAPER, lw=LW_H*0.95,
            solid_capstyle="round", solid_joinstyle="round", zorder=6)
for sx_,sy_ in [(SR_X-14, SR_Y-27),(SR_X+9, SR_Y-27)]:
    ax.add_patch(Ellipse((sx_,sy_-1.2),7,2.8,
                          fc=PRU_INK, ec=OUTLINE, lw=LW_H*0.6, zorder=7))

# Radiant dashes around right scientist head
for ang in np.linspace(5, 150, 6):
    rad = np.radians(ang)
    r0,r1 = 7.0, 10.5
    ax.plot([SR_X-1.5+r0*np.cos(rad), SR_X-1.5+r1*np.cos(rad)],
            [SR_Y+10+r0*np.sin(rad),  SR_Y+10+r1*np.sin(rad)],
            color=PAPER, lw=1.3, alpha=0.75, solid_capstyle="round", zorder=5)

ax.text(SR_X, SR_Y-33, "OPERATOR  B",
        color=CYAN_LITE, fontsize=5.2, ha="center",
        fontfamily="monospace", fontweight="bold")

# ═══════════════════════════════════════════════════════════════════════════════
# TYPOGRAPHY — all monospace
# ═══════════════════════════════════════════════════════════════════════════════

# Title bar
ax.add_patch(Rectangle((12, 90.8), 76, 7.0,
                        fc=PRU_INK, ec=PAPER, lw=2.0, zorder=8))
ax.add_patch(Rectangle((12, 90.0), 76, 0.7, fc=PAPER,    ec="none", zorder=8))
ax.add_patch(Rectangle((12, 89.3), 76, 0.4, fc=CYAN_MID, ec="none", zorder=8))

ax.text(50, 94.4, "GIANT  PINHOLE  CAMERA",
        color=PAPER, fontsize=14.5, ha="center", va="center",
        fontweight="bold", fontfamily="monospace", zorder=9)

ax.text(50, 88.0,
        "CAMERA  RESEARCH  DIVISION  ·  FIELD  UNIT  No.1  ·  CYANOTYPE  PROCESS",
        color=CYAN_LITE, fontsize=6.2, ha="center", va="center",
        fontfamily="monospace", zorder=8)

# Spec bar — bottom
ax.add_patch(Rectangle((12, 6.5), 76, 6.3,
                        fc=PRU_INK, ec=PAPER, lw=1.8, zorder=8))
ax.add_patch(Rectangle((12, 12.6), 76, 0.6, fc=PAPER,    ec="none", zorder=9))
ax.add_patch(Rectangle((12, 11.9), 76, 0.4, fc=CYAN_MID, ec="none", zorder=9))

ax.text(50, 9.6,
        "f = 2,362 mm   ·   d = 2.17 mm   ·   f/1088   ·   "
        "IMAGE  PLANE  5,893 × 2,388 mm   ·   λ = 550 nm",
        color=PAPER, fontsize=6.2, ha="center", va="center",
        fontfamily="monospace", fontweight="bold", zorder=9)

# Side strip text
ax.text(5.2, 50, "CYANOTYPE  PROCESS",
        color=PAPER, fontsize=5.2, ha="center", va="center",
        rotation=90, fontfamily="monospace", alpha=0.75, zorder=5)
ax.text(94.8, 50, "GIANT  PINHOLE  CAMERA",
        color=PAPER, fontsize=5.2, ha="center", va="center",
        rotation=270, fontfamily="monospace", alpha=0.75, zorder=5)

# Corner marks
for cx_,cy_ in [(14,14),(86,14),(14,86),(86,86)]:
    sx_ = 1 if cx_ < 50 else -1
    sy_ = 1 if cy_ < 50 else -1
    ax.plot([cx_, cx_+3.5*sx_], [cy_, cy_],     color=PAPER, lw=1.4, alpha=0.65, zorder=9)
    ax.plot([cx_, cx_],         [cy_, cy_+3.5*sy_], color=PAPER, lw=1.4, alpha=0.65, zorder=9)

# ── Save ──────────────────────────────────────────────────────────────────────
fig.savefig("logo-final.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close(fig)
print("  → logo-final.png")
print("Done.")
