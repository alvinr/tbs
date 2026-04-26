#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
Top-down schematic showing container camera geometry and subject distances.
Option B: side-to-side orientation.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

F  = 2362.0   # focal length (container interior width), mm
IW = 5893.0   # image plane width, mm (19'4")
IH = 2388.0   # image plane height, mm (not used in top-down)

PH = 1780.0   # person height mm
SHOULDER_W_F = 0.258

DISTS_M  = [2.0, 3.0, 5.0, 10.0]
COLOURS  = ['#00D8FF', '#7BFF7B', '#FFB347', '#FF6B9D']

# ── Layout ────────────────────────────────────────────────────────────────────
# Top-down view:
#   • Container runs LEFT–RIGHT (its length = IW = 5893 mm)
#   • Container depth = F = 2362 mm  (the focal length / camera width)
#   • Pinhole is on the BOTTOM long wall (y = 0), centred at x = IW/2
#   • Image plane is on the TOP long wall  (y = F)
#   • Subjects stand BELOW the pinhole wall (y < 0) at various distances

MAX_DIST_MM = 11500   # how far below to show (covers 10 m subject)
MARGIN_X    = 1800
MARGIN_TOP  = 800
MARGIN_BOT  = 1500

fig, ax = plt.subplots(figsize=(20, 14))
fig.patch.set_facecolor('#0D0D0D')
ax.set_facecolor('#0D0D0D')

# ── Container body ────────────────────────────────────────────────────────────
ax.add_patch(mpatches.Rectangle(
    (0, 0), IW, F,
    lw=2, edgecolor='#555', facecolor='#161412', zorder=2))

# Interior label
ax.text(IW/2, F/2,
        '20-FT CONTAINER  (interior)',
        ha='center', va='center', fontsize=12, color='#3A3530',
        fontweight='bold', zorder=3)
ax.text(IW/2, F/2 - 250,
        f'focal length  f = {F:.0f} mm  (7′ 9″)',
        ha='center', va='center', fontsize=9, color='#2E2B27', zorder=3)

# Focal length dimension arrow (inside, vertical)
fl_x = IW * 0.05
ax.annotate('', xy=(fl_x, F), xytext=(fl_x, 0),
            arrowprops=dict(arrowstyle='<->', color='#444', lw=1.5,
                            mutation_scale=9), zorder=4)
ax.text(fl_x - 180, F/2, f'{F:.0f} mm\n= focal\nlength',
        ha='right', va='center', fontsize=8, color='#555', zorder=4)

# ── Image plane (top wall) ────────────────────────────────────────────────────
ax.plot([0, IW], [F, F], color='#00D8FF', lw=5, solid_capstyle='butt',
        zorder=5, label='Image plane')
ax.text(IW/2, F + 200, 'IMAGE PLANE  (photosensitive surface)',
        ha='center', fontsize=10.5, color='#00D8FF', fontweight='bold', zorder=6)
ax.text(IW/2, F + 420,
        f'19′ 4″  ×  7′ 10″   (5,893 × 2,388 mm)',
        ha='center', fontsize=9, color='#00A8CC', zorder=6)

# Width dimension of image plane
ax.annotate('', xy=(IW, F + 650), xytext=(0, F + 650),
            arrowprops=dict(arrowstyle='<->', color='#336677', lw=1.3,
                            mutation_scale=9), zorder=4)
ax.text(IW/2, F + 700, f'{IW:.0f} mm  (19′ 4″)',
        ha='center', va='bottom', fontsize=8, color='#336677', zorder=4)

# ── Pinhole wall (bottom wall) ────────────────────────────────────────────────
ax.plot([0, IW], [0, 0], color='#FF6B35', lw=4, solid_capstyle='butt', zorder=5)
ax.text(IW/2, -320, 'PINHOLE WALL',
        ha='center', fontsize=9, color='#FF6B35', fontweight='bold', zorder=6)

# Pinhole dot
PX = IW / 2   # pinhole x centre
ax.add_patch(mpatches.Circle((PX, 0), 80, fc='#FF6B35', ec='#FF9900', lw=2.5, zorder=7))
ax.text(PX + 280, 0, f' ⌀ 2.17 mm\n f/1088',
        va='center', fontsize=8.5, color='#FF9900', zorder=7)

# ── FOV cone ─────────────────────────────────────────────────────────────────
# The 102° horizontal FOV means ±51° from the axis (perpendicular to pinhole wall)
# The cone opens DOWNWARD (toward the scene / subject space)
half_angle = np.radians(51)
cone_depth  = MAX_DIST_MM
cone_half_w = cone_depth * np.tan(half_angle)

cone_left  = [PX, PX - cone_half_w]
cone_right = [PX, PX + cone_half_w]
cone_y     = [0,  -cone_depth]

ax.fill_betweenx(cone_y,
                 [PX, PX - cone_half_w],
                 [PX, PX + cone_half_w],
                 color='#FF6B35', alpha=0.04, zorder=1)
ax.plot(cone_left,  cone_y, color='#FF6B3540', lw=1.2, ls='--', zorder=2)
ax.plot(cone_right, cone_y, color='#FF6B3540', lw=1.2, ls='--', zorder=2)

# FOV angle label
ax.text(PX + cone_half_w * 0.35, -cone_depth * 0.12,
        '102° H-FOV', fontsize=9, color='#FF6B3560', ha='center', zorder=3)

# ── Subject positions & figures ───────────────────────────────────────────────
# Spread subjects across the width so they don't overlap
SUBJ_X = [IW * 0.18, IW * 0.38, IW * 0.60, IW * 0.80]

for (u_m, col, sx) in zip(DISTS_M, COLOURS, SUBJ_X):
    u_mm = u_m * 1000
    M    = F / u_mm
    B    = 2.17 * (1 + F/u_mm)
    ph   = PH * M
    sw   = PH * SHOULDER_W_F * M

    sy_feet = -u_mm          # y position of subject's feet in diagram

    # ── Person figure (simple, fixed display scale) ───────────────────────────
    FIG_H = 600    # display height in mm (fixed, for readability)
    FIG_W = 220
    HEAD_D = 160

    # Body rectangle
    ax.add_patch(mpatches.FancyBboxPatch(
        (sx - FIG_W/2, sy_feet), FIG_W, FIG_H * 0.78,
        boxstyle="round,pad=0", fc=col, ec='none', alpha=0.85, zorder=6))
    # Head
    ax.add_patch(mpatches.Ellipse(
        (sx, sy_feet + FIG_H * 0.78 + HEAD_D/2),
        FIG_W * 0.80, HEAD_D, fc=col, ec='none', alpha=0.85, zorder=6))

    # ── Sight lines from subject to pinhole ──────────────────────────────────
    ax.plot([sx, PX], [sy_feet + FIG_H/2, 0],
            color=col, lw=0.9, ls=':', alpha=0.45, zorder=3)

    # ── Distance arrow (to the right of the rightmost subject) ───────────────
    arr_x = IW + MARGIN_X * 0.25
    ax.annotate('', xy=(arr_x, sy_feet), xytext=(arr_x, 0),
                arrowprops=dict(arrowstyle='<->', color=col, lw=1.5,
                                mutation_scale=10), zorder=9)
    ax.text(arr_x + 200, sy_feet/2,
            f'{u_m:.0f} m\n({u_m*3.2808:.0f} ft)',
            va='center', fontsize=9, color=col, fontweight='bold', zorder=10)

    # ── Image result bar (on image plane, showing projected height) ───────────
    # The projected image of the subject is centred on the image plane
    img_bar_cx = IW/2   # image is always centred (pinhole is centred)
    img_bar_y  = F + 900 + DISTS_M.index(u_m) * 230
    bar_half   = ph / 2
    # Clamp bar to IW/2 for display
    ax.plot([img_bar_cx - min(bar_half, IW/2 * 0.9),
             img_bar_cx + min(bar_half, IW/2 * 0.9)],
            [img_bar_y, img_bar_y],
            color=col, lw=7, solid_capstyle='butt', alpha=0.80, zorder=6)
    ax.text(img_bar_cx + min(bar_half, IW/2*0.9) + 150, img_bar_y,
            f'  {u_m:.0f} m → height {ph:.0f} mm ({ph/304.8:.2f} ft)  '
            f'M={M:.3f}×  Blur Ø{B:.1f} mm',
            va='center', fontsize=8.5, color=col, zorder=7)

    # Dot connector: figure head → line to image bar (just visual)
    ax.plot([sx, img_bar_cx], [sy_feet + FIG_H + HEAD_D, img_bar_y],
            color=col, lw=0.5, alpha=0.15, zorder=1)

# ── Image plane bars: header ─────────────────────────────────────────────────
ax.text(-MARGIN_X * 0.02, F + 900 + 4 * 230 * 0.30,
        'Resulting image heights\n(on photosensitive surface):',
        ha='right', va='center', fontsize=8.5, color='#666', style='italic', zorder=7)

# ── Scale bar ────────────────────────────────────────────────────────────────
sb_x0 = IW * 0.02
sb_x1 = sb_x0 + 1000
sb_y  = -MAX_DIST_MM + MARGIN_BOT * 0.35
ax.plot([sb_x0, sb_x1], [sb_y, sb_y], color='#666', lw=3,
        solid_capstyle='butt', zorder=8)
for ssx in [sb_x0, sb_x1]:
    ax.plot([ssx, ssx], [sb_y-150, sb_y+150], color='#666', lw=2, zorder=8)
ax.text((sb_x0+sb_x1)/2, sb_y-320,
        '1,000 mm (3.3 ft)\nscale bar',
        ha='center', fontsize=8, color='#666', zorder=8)

# ── North arrow / orientation note ───────────────────────────────────────────
ax.text(IW * 0.97, -MAX_DIST_MM + MARGIN_BOT * 0.4,
        '← SCENE (subject space)',
        ha='right', fontsize=9, color='#444', style='italic', zorder=8)
ax.text(IW * 0.97, F + 150,
        'CAMERA INTERIOR →',
        ha='right', fontsize=9, color='#444', style='italic', zorder=8)

# ── Title ─────────────────────────────────────────────────────────────────────
ax.text(IW/2, F + MARGIN_TOP * 0.82,
        'OPTION B  —  TOP-DOWN SCHEMATIC  (to scale in mm)',
        ha='center', fontsize=14, color='#FFFFFF', fontweight='bold', zorder=10)
ax.text(IW/2, F + MARGIN_TOP * 0.60,
        'Pinhole centred on long wall  ·  102° H-FOV  ·  f = 2,362 mm  ·  Subjects outside, facing camera',
        ha='center', fontsize=9.5, color='#777', zorder=10)

# ── Axes ──────────────────────────────────────────────────────────────────────
ax.set_xlim(-MARGIN_X, IW + MARGIN_X * 1.1)
ax.set_ylim(-MAX_DIST_MM - MARGIN_BOT * 0.2, F + MARGIN_TOP)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout(pad=0.3)
out = '/Users/alvinrichards/dev/tbs/diagrams/portrait-camera-schematic.png'
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='#0D0D0D')
plt.close()
print(f'Saved: {out}')
