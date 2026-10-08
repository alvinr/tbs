#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
Pinhole Camera — Portrait Scale Visualization
Option B: 20-ft container, side-to-side
f = 2362mm | d = 2.17mm | f/1088 | ~86° horizontal FOV (active 4389mm film plane)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math
from tbs_constants import DISTORTION_DPI, RAIL_X_L, RAIL_X_R, FP_H, C_LEN, C_WID

# ─────────────────────────────────────────
# Camera constants — the IMAGE PLANE is the ACTIVE FILM PLANE (not the full container wall)
# ─────────────────────────────────────────
F    = float(C_WID)                 # 2362 — focal length = container interior depth, mm
D    =  2.17                        # Rayleigh pinhole Ø, mm
FP_W = float(RAIL_X_R - RAIL_X_L)   # 4389 — active film-plane (image-plane) width, mm
IW   = FP_W                         # image-plane width used for the scale charts
IH   = float(FP_H)                  # 2094 — active film-plane height, mm
PINHOLE_X = RAIL_X_L + FP_W / 2     # 2454.5 — pinhole on the long wall, at the ACTIVE-plane center
H_FOV = 2 * math.degrees(math.atan((IW / 2) / F))   # ~86° — real horizontal field of view
V_FOV = 2 * math.degrees(math.atan((IH / 2) / F))   # ~48° — real vertical field of view

# ─────────────────────────────────────────
# Subject proportions for a 1780mm adult
# (fractions of total height)
# ─────────────────────────────────────────
PH   = 1780.0   # total person height mm

HEAD_H_F  = 0.130   # head height as fraction
NECK_H_F  = 0.045
UTORC_H_F = 0.160   # upper torso
LTORC_H_F = 0.135   # lower torso
HIP_H_F   = 0.080
LEG_H_F   = 0.450   # both legs combined height

SHOULDER_W_F = 0.258   # fraction of total height → shoulder width
HIP_W_F      = 0.213
LEG_W_F      = 0.090
NECK_W_F     = 0.056
HEAD_W_F     = 0.107

# Distances and presentation colors
DISTS_M  = [2.0, 3.0, 5.0, 10.0]
COLOURS  = ['#00D8FF', '#7BFF7B', '#FFB347', '#FF6B9D']
X_CENTS  = [IW*0.105, IW*0.309, IW*0.543, IW*0.857]   # silhouette centers (fractions of active width)


# ─────────────────────────────────────────
# Helper: draw one silhouette
# ─────────────────────────────────────────
def draw_person(ax, cx, y_foot, M, color, alpha=0.88, z=5):
    ph = PH * M

    def h(f): return ph * f
    def w(f): return ph * f

    y = y_foot

    # ── legs ──────────────────────────────
    lw  = w(LEG_W_F)
    lh  = h(LEG_H_F)
    hipw = w(HIP_W_F)
    gap  = hipw * 0.14
    ax.add_patch(mpatches.FancyBboxPatch(
        (cx - hipw/2, y), lw, lh,
        boxstyle="round,pad=0", fc=color, ec='none', alpha=alpha, zorder=z))
    ax.add_patch(mpatches.FancyBboxPatch(
        (cx + hipw/2 - lw, y), lw, lh,
        boxstyle="round,pad=0", fc=color, ec='none', alpha=alpha, zorder=z))
    y += lh

    # ── hips ──────────────────────────────
    hiph = h(HIP_H_F)
    ax.add_patch(mpatches.FancyBboxPatch(
        (cx - hipw/2, y), hipw, hiph,
        boxstyle="round,pad=0", fc=color, ec='none', alpha=alpha, zorder=z))
    y += hiph

    # ── lower torso ───────────────────────
    lth = h(LTORC_H_F)
    ax.add_patch(mpatches.FancyBboxPatch(
        (cx - hipw/2, y), hipw, lth,
        boxstyle="round,pad=0", fc=color, ec='none', alpha=alpha, zorder=z))
    y += lth

    # ── upper torso (trapezoid) ────────────
    uth  = h(UTORC_H_F)
    sw   = w(SHOULDER_W_F)
    tx = [cx - hipw/2, cx + hipw/2, cx + sw/2, cx - sw/2]
    ty = [y,           y,           y + uth,   y + uth  ]
    ax.fill(tx, ty, color=color, alpha=alpha, zorder=z)
    y += uth

    # ── neck ──────────────────────────────
    nh = h(NECK_H_F)
    nw = w(NECK_W_F)
    ax.add_patch(mpatches.FancyBboxPatch(
        (cx - nw/2, y), nw, nh,
        boxstyle="round,pad=0", fc=color, ec='none', alpha=alpha, zorder=z))
    y += nh

    # ── head (ellipse) ────────────────────
    head_h = h(HEAD_H_F)
    head_w = w(HEAD_W_F)
    ax.add_patch(mpatches.Ellipse(
        (cx, y + head_h/2), head_w, head_h,
        fc=color, ec='none', alpha=alpha, zorder=z))
    y += head_h

    return y           # top of head


# ─────────────────────────────────────────
# Figure 1 — full image-plane scale chart
# ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(20, 11))
fig.patch.set_facecolor('#101010')
ax.set_facecolor('#101010')

# Image plane rectangle
ax.add_patch(mpatches.Rectangle(
    (0, 0), IW, IH,
    linewidth=2, edgecolor='#555', facecolor='#1C1915', zorder=0))

# Subtle horizontal grain lines
for yl in np.linspace(0, IH, 48):
    ax.axhline(yl, color='#201E1A', lw=0.4, alpha=0.6, zorder=1)

# Corner crop marks
ck = IW * 0.018
for (ccx, ccy) in [(0,0),(IW,0),(IW,IH),(0,IH)]:
    sx = ck if ccx==0 else -ck
    sy = ck if ccy==0 else -ck
    ax.plot([ccx, ccx+sx],[ccy, ccy], color='#777', lw=1.8, zorder=2)
    ax.plot([ccx, ccx],[ccy, ccy+sy], color='#777', lw=1.8, zorder=2)

# Ground horizon line
GY = IH * 0.13
ax.axhline(GY, color='#303030', lw=1.0, ls='--', zorder=2)

# Portrait sweet-spot highlight (3 m–5 m zone)
sp_x0 = X_CENTS[1] - PH * (F/(3000)) * SHOULDER_W_F * 3.2
sp_x1 = X_CENTS[2] + PH * (F/(5000)) * SHOULDER_W_F * 3.2
ax.add_patch(mpatches.FancyBboxPatch(
    (sp_x0, 0), sp_x1 - sp_x0, IH,
    boxstyle="round,pad=0",
    fc='#FFD70008', ec='#FFD70035', lw=1.5, ls='--', zorder=3))
ax.text((sp_x0+sp_x1)/2, IH*0.975,
        '★  PORTRAIT SWEET SPOT  (3–5 m)  ★',
        ha='center', va='top', fontsize=8, color='#FFD700',
        alpha=0.75, zorder=10)

# ── Draw each silhouette ─────────────────
for u_m, col, xcx in zip(DISTS_M, COLOURS, X_CENTS):
    u_mm = u_m * 1000
    M    = F / u_mm
    B    = D * (1 + F/u_mm)
    ph   = PH * M
    sw   = PH * SHOULDER_W_F * M

    y_foot = GY
    top_y  = draw_person(ax, xcx, y_foot, M, col)

    # Shadow ellipse
    ax.add_patch(mpatches.Ellipse(
        (xcx, GY), sw*1.5, IH*0.016,
        fc='#000', ec='none', alpha=0.45, zorder=4))

    # Height dimension arrow
    ax_arr = xcx + sw/2 + IW*0.008
    ax.annotate('', xy=(ax_arr, y_foot+ph), xytext=(ax_arr, y_foot),
                arrowprops=dict(arrowstyle='<->', color=col, lw=1.4,
                                mutation_scale=9), zorder=9)

    # Blur circle indicator (positioned mid-frame right of figure)
    bx = xcx
    by = IH * 0.70
    ax.add_patch(mpatches.Circle((bx, by), B,
        fc='none', ec=col, lw=1.5, ls='--', alpha=0.7, zorder=6))
    ax.add_patch(mpatches.Circle((bx, by), max(B*0.07,0.5),
        fc=col, ec='none', alpha=1.0, zorder=7))

    # Label block (above image plane)
    ly = IH + IH*0.05
    ax.text(xcx, ly + IH*0.21, f'{u_m:.0f} m  /  {u_m*3.28084:.0f} ft',
            ha='center', fontsize=11.5, color=col, fontweight='bold', zorder=10)
    ax.text(xcx, ly + IH*0.12,
            f'Image height:  {ph:.0f}mm  ({ph/304.8:.2f} ft)',
            ha='center', fontsize=9, color='#cccccc', zorder=10)
    ax.text(xcx, ly + IH*0.04,
            f'Width in frame: {PH*SHOULDER_W_F*M:.0f}mm  '
            f'({PH*SHOULDER_W_F*M/IW*100:.1f}% of image width)',
            ha='center', fontsize=8.5, color='#aaaaaa', zorder=10)
    ax.text(xcx, ly,
            f'M = {M:.3f}×       Blur Ø = {B:.2f}mm',
            ha='center', fontsize=8, color='#888888', zorder=10)

    # Connector dot from top of head to label
    ax.plot([xcx, xcx], [top_y+IH*0.01, ly - IH*0.005],
            color=col, lw=0.6, alpha=0.30, ls=':', zorder=3)

# ── Scale bar (1 m on image plane) ───────
sb_x0 = IW * 0.80
sb_x1 = sb_x0 + 1000
sb_y  = GY * 0.50
ax.plot([sb_x0, sb_x1],[sb_y, sb_y], color='#666', lw=2.5, solid_capstyle='butt', zorder=8)
for ssx in [sb_x0, sb_x1]:
    ax.plot([ssx,ssx],[sb_y-IH*0.012, sb_y+IH*0.012], color='#666', lw=1.8, zorder=8)
ax.text((sb_x0+sb_x1)/2, sb_y+IH*0.025, '1 m  (on image plane)',
        ha='center', fontsize=8, color='#666', zorder=8)

# ── Blur legend note ─────────────────────
ax.text(IW*0.5, IH*0.80,
        'Dashed ring = blur circle diameter on photographic surface',
        ha='center', fontsize=8, color='#555', style='italic', zorder=10)

# ── Image plane label ────────────────────
ax.text(IW/2, IH - IH*0.025,
        "ACTIVE FILM PLANE  —  14′ 5″ × 6′ 10″  (4,389 × 2,094mm)",
        ha='center', va='top', fontsize=9, color='#444', zorder=10,
        fontfamily='monospace')

# ── Title ────────────────────────────────
ax.text(IW/2, IH + IH*0.60,
        'OPTION B PINHOLE CAMERA  —  PORTRAIT RENDERING AT SCALE',
        ha='center', fontsize=14, color='#FFFFFF', fontweight='bold', zorder=10)
ax.text(IW/2, IH + IH*0.48,
        f'Subject: 5′ 10″  (1780mm)  ·  f = 2362mm  ·  Pinhole d = 2.17mm  ·  f/1088  ·  {H_FOV:.0f}° H-FOV × {V_FOV:.0f}° V-FOV',
        ha='center', fontsize=9.5, color='#888', zorder=10)

# ── Inversion note ───────────────────────
ax.text(IW/2, -IH*0.14,
        '* The actual pinhole image is optically inverted (upside-down, mirror-reversed). '
        'Shown right-side-up here for legibility.',
        ha='center', fontsize=8, color='#484848', style='italic', zorder=10)

ax.set_xlim(-IW*0.02, IW*1.02)
ax.set_ylim(-IH*0.22, IH*0.90 + IH*0.65)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout(pad=0.3)

out1 = '/Users/alvinrichards/dev/tbs/diagrams/portrait-scale-comparison.png'
plt.savefig(out1, dpi=DISTORTION_DPI, bbox_inches='tight', facecolor='#101010')
plt.close()
print(f'Saved: {out1}')


# ─────────────────────────────────────────
# Figure 2 — top-down schematic
# (camera footprint + subject distances)
# ─────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(14, 8))
fig2.patch.set_facecolor('#101010')
ax2.set_facecolor('#0D0D0D')

# Camera container footprint (20 ft × 8 ft)
# Orient so image plane faces "up" in the diagram
CONT_L_MM = float(C_LEN)   # 5893 — container interior length
CONT_W_MM = float(C_WID)   # 2362 — container interior depth = focal length

# Container rectangle (left edge at x=0, bottom at y=0)
ax2.add_patch(mpatches.Rectangle(
    (0, 0), CONT_L_MM, CONT_W_MM,
    linewidth=2, edgecolor='#777', facecolor='#1A1A1A', zorder=2))
ax2.text(CONT_L_MM/2, CONT_W_MM/2,
         '20-FT CONTAINER\n(camera interior)',
         ha='center', va='center', fontsize=10, color='#555',
         fontweight='bold', zorder=3)

# Image-plane wall (top of container). The full wall is faint; the ACTIVE FILM PLANE
# (X = RAIL_X_L..RAIL_X_R) is the bright photosensitive span — offset toward the cargo-door end.
ax2.plot([0, CONT_L_MM],[CONT_W_MM, CONT_W_MM],
         color='#2A3A3A', lw=4, solid_capstyle='butt', zorder=4)
ax2.plot([RAIL_X_L, RAIL_X_R],[CONT_W_MM, CONT_W_MM],
         color='#00D8FF', lw=5, solid_capstyle='butt', zorder=4, label='Active film plane')
ax2.text((RAIL_X_L+RAIL_X_R)/2, CONT_W_MM + 120,
         'ACTIVE FILM PLANE  (4,389mm photosensitive span)',
         ha='center', fontsize=9, color='#00D8FF', zorder=5)

# Pinhole wall (bottom of container in diagram) — pinhole at the ACTIVE-plane center X (not container center)
ax2.plot([0, CONT_L_MM],[0, 0],
         color='#FF6B35', lw=4, solid_capstyle='butt', zorder=4)
ax2.add_patch(mpatches.Circle(
    (PINHOLE_X, 0), 60,
    fc='#FF6B35', ec='#FF9900', lw=2, zorder=5))
ax2.text(PINHOLE_X, -350,
         f'PINHOLE  ⌀ {D}mm  (f/{F/D:.0f})  ·  X={PINHOLE_X:.0f}mm',
         ha='center', fontsize=9.5, color='#FF6B35', fontweight='bold', zorder=5)

# Light rays from the pinhole to the edges of the ACTIVE film plane (the real captured cone)
for iy in np.linspace(RAIL_X_L, RAIL_X_R, 8):
    ax2.plot([PINHOLE_X, iy],[0, CONT_W_MM],
             color='#FF6B3530', lw=0.8, zorder=1)

# Subjects sit BELOW the pinhole wall (y = −distance). Bound the view to the actual content —
# subjects down to the farthest distance, labels up to just above the image-plane stack — so the
# drawing fills the frame instead of floating under a tall empty top margin.
_label_top = CONT_W_MM + 500 + (len(DISTS_M) - 1) * 620   # top image-height label row
_subj_bot  = -max(DISTS_M) * 1000                          # farthest subject (10 m)
_title_y   = _label_top + 700
_sub_y     = _label_top + 400

ax2.set_xlim(-1500, CONT_L_MM + 1500)
ax2.set_ylim(_subj_bot - 600, _title_y + 450)
ax2.set_aspect('equal')
ax2.axis('off')

for u_m, col in zip(DISTS_M, COLOURS):
    u_mm = u_m * 1000
    M    = F / u_mm
    B    = D * (1 + F/u_mm)
    ph   = PH * M
    sw   = PH * SHOULDER_W_F * M

    # Subject position in diagram: below the pinhole (y = -u_mm), centered on the pinhole X
    sy = -u_mm
    sx = PINHOLE_X

    # Figure (simple vertical bar + head)
    fig_h_diag = 300   # fixed display size for subject in this diagram
    ax2.add_patch(mpatches.Rectangle(
        (sx - 80, sy), 160, fig_h_diag * 0.78,
        fc=col, ec='none', alpha=0.80, zorder=5))
    ax2.add_patch(mpatches.Ellipse(
        (sx, sy + fig_h_diag * 0.78 + 80), 120, 160,
        fc=col, ec='none', alpha=0.80, zorder=5))

    # Distance annotation
    ax2.annotate('',
                 xy=(sx + 900, sy),
                 xytext=(sx + 900, 0),
                 arrowprops=dict(arrowstyle='<->', color=col, lw=1.4,
                                 mutation_scale=9), zorder=9)
    ax2.text(sx + 1200, sy + fig_h_diag / 2,
             f'{u_m:.0f} m  ({u_m*3.28084:.0f} ft)',
             va='center', ha='left', fontsize=9, color=col, fontweight='bold', zorder=10)

    # Sight lines from subject to pinhole
    ax2.plot([sx, PINHOLE_X],[sy + fig_h_diag/2, 0],
             color=col, lw=0.7, ls='--', alpha=0.35, zorder=3)

    # Image height label on image plane
    img_x_center = PINHOLE_X
    img_x_offset = img_x_center - ph/2
    ax2.plot([img_x_offset, img_x_offset + ph],
             [CONT_W_MM + 50, CONT_W_MM + 50],
             color=col, lw=3, solid_capstyle='butt', alpha=0.7, zorder=5)
    ax2.text(CONT_L_MM*0.62, CONT_W_MM + 500 + DISTS_M.index(u_m)*620,
             f'{u_m:.0f}m → image {ph:.0f}mm tall  ·  M = {M:.3f}×  ·  Blur Ø {B:.2f}mm',
             ha='left', fontsize=8.5, color=col, zorder=10)

# Title (just above the image-plane label stack — no empty top margin)
ax2.text(CONT_L_MM/2, _title_y,
         'TOP-DOWN SCHEMATIC  —  CAMERA + SUBJECT DISTANCES',
         ha='center', fontsize=13, color='#FFFFFF', fontweight='bold', zorder=10)
ax2.text(CONT_L_MM/2, _sub_y,
         'Diagram is to scale in mm. Container interior view. Subject outside, facing pinhole wall.',
         ha='center', fontsize=9, color='#777', zorder=10)

plt.tight_layout(pad=0.3)

out2 = '/Users/alvinrichards/dev/tbs/diagrams/portrait-camera-schematic.png'
plt.savefig(out2, dpi=DISTORTION_DPI, bbox_inches='tight', facecolor='#101010')
plt.close()
print(f'Saved: {out2}')


# ─────────────────────────────────────────
# Figure 3 — optimal portrait close-up
# Shows exactly what 3 m looks like on the
# full image plane with real proportions
# ─────────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(18, 7.5))
fig3.patch.set_facecolor('#101010')
ax3.set_facecolor('#101010')

# Image plane
ax3.add_patch(mpatches.Rectangle(
    (0, 0), IW, IH,
    lw=2, edgecolor='#555', facecolor='#1A1815', zorder=0))
for yl in np.linspace(0, IH, 40):
    ax3.axhline(yl, color='#1F1D1A', lw=0.35, alpha=0.6, zorder=1)

# Corner marks
ck = IW * 0.015
for (ccx, ccy) in [(0,0),(IW,0),(IW,IH),(0,IH)]:
    sx2 = ck if ccx==0 else -ck
    sy2 = ck if ccy==0 else -ck
    ax3.plot([ccx,ccx+sx2],[ccy,ccy], color='#888', lw=1.5, zorder=2)
    ax3.plot([ccx,ccx],[ccy,ccy+sy2], color='#888', lw=1.5, zorder=2)

# Draw person at 3 m, centerd horizontally
u_opt = 3.0
M_opt = F / (u_opt * 1000)
B_opt = D * (1 + F/(u_opt*1000))
ph_opt = PH * M_opt            # ~1401mm
sw_opt = PH * SHOULDER_W_F * M_opt

cx_opt = IW / 2
GY3    = (IH - ph_opt) / 2    # vertically center the figure

top3 = draw_person(ax3, cx_opt, GY3, M_opt, '#7BFF7B', alpha=0.92)

# Ground line
ax3.axhline(GY3, color='#2A2A2A', lw=0.8, ls='--', zorder=2)

# Height annotation
hax = cx_opt + sw_opt/2 + IW*0.008
ax3.annotate('', xy=(hax, GY3+ph_opt), xytext=(hax, GY3),
             arrowprops=dict(arrowstyle='<->', color='#7BFF7B', lw=1.5,
                             mutation_scale=10), zorder=9)
ax3.text(hax + IW*0.005, GY3 + ph_opt/2,
         f'{ph_opt:.0f}mm\n({ph_opt/304.8:.2f} ft)',
         va='center', fontsize=9, color='#7BFF7B', zorder=10)

# Width annotation
way = GY3 - IH*0.06
ax3.annotate('', xy=(cx_opt+sw_opt/2, way), xytext=(cx_opt-sw_opt/2, way),
             arrowprops=dict(arrowstyle='<->', color='#7BFF7B', lw=1.5,
                             mutation_scale=9), zorder=9)
ax3.text(cx_opt, way - IH*0.03,
         f'Shoulder width: {sw_opt:.0f}mm  ({sw_opt/IW*100:.1f}% of image width)',
         ha='center', fontsize=9, color='#7BFF7B', zorder=10)

# Frame fills annotation
ax3.text(IW*0.5, IH + IH*0.07,
         f'At 3 m (9.8 ft):  person fills {ph_opt/IH*100:.0f}% of frame height  ·  '
         f'{sw_opt/IW*100:.1f}% of frame width',
         ha='center', fontsize=10.5, color='#7BFF7B', fontweight='bold', zorder=10)

# Blur circle indicator
bx3 = IW*0.88
by3 = IH*0.50
ax3.add_patch(mpatches.Circle((bx3, by3), B_opt,
    fc='none', ec='#7BFF7B', lw=2, ls='--', alpha=0.8, zorder=6))
ax3.add_patch(mpatches.Circle((bx3, by3), max(B_opt*0.07, 0.5),
    fc='#7BFF7B', ec='none', zorder=7))
ax3.text(bx3, by3 - B_opt*2.5,
         f'Blur circle\nØ = {B_opt:.2f}mm',
         ha='center', fontsize=8, color='#7BFF7B', alpha=0.8, zorder=10)

# Actual size scale bar = 500mm on image
sb3_y  = IH * 0.06
sb3_x0 = IW * 0.03
sb3_x1 = sb3_x0 + 500
ax3.plot([sb3_x0,sb3_x1],[sb3_y,sb3_y], color='#888', lw=2.5, solid_capstyle='butt', zorder=8)
for ssx3 in [sb3_x0, sb3_x1]:
    ax3.plot([ssx3,ssx3],[sb3_y-IH*0.01,sb3_y+IH*0.01], color='#888', lw=2, zorder=8)
ax3.text((sb3_x0+sb3_x1)/2, sb3_y+IH*0.025,
         '500mm on image plane', ha='center', fontsize=8, color='#888', zorder=8)

# Image plane label
ax3.text(IW/2, IH-IH*0.025,
         "ACTIVE FILM PLANE  —  14′ 5″ × 6′ 10″",
         ha='center', va='top', fontsize=9, color='#444', zorder=10,
         fontfamily='monospace')

# Title
ax3.text(IW/2, IH + IH*0.22,
         f'OPTIMAL PORTRAIT DISTANCE  —  3 m  ({u_opt*3.28:.1f} ft)  from pinhole wall',
         ha='center', fontsize=13, color='#FFFFFF', fontweight='bold', zorder=10)
ax3.text(IW/2, IH + IH*0.13,
         f'M = {M_opt:.3f}×  ·  Blur Ø = {B_opt:.2f}mm  ·  Magnification: image is {M_opt:.0%} of subject size',
         ha='center', fontsize=9, color='#888', zorder=10)
ax3.text(IW/2, -IH*0.10,
         '* Image is inverted in the camera. Shown right-side-up here.',
         ha='center', fontsize=8, color='#484848', style='italic', zorder=10)

ax3.set_xlim(-IW*0.02, IW*1.02)
ax3.set_ylim(-IH*0.18, IH + IH*0.34)
ax3.set_aspect('equal')
ax3.axis('off')

plt.tight_layout(pad=0.3)

out3 = '/Users/alvinrichards/dev/tbs/diagrams/portrait-optimal-3m.png'
plt.savefig(out3, dpi=DISTORTION_DPI, bbox_inches='tight', facecolor='#101010')
plt.close()
print(f'Saved: {out3}')

print('\nAll three images written to /Users/alvinrichards/dev/tbs/')
