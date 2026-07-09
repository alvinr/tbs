#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_tilt_swing_board_distortion.py
Tilt-swing front board ONLY distortion renders (film plane flat).

Projects a world grid through the front-board tilt/swing transformation
with the film plane held flat at the far wall. Shows the isolated effect
of the spherical-pivot pinhole steering mechanism.

Output: tilt-swing-board-distortion-c0.png … c6.png
        tilt-swing-board-distortion-summary.png
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
from tbs_constants import (
    C_WID,
    FP_W as _FP_W, FP_H as _FP_H,
    DIAGRAMS_DIR,
    FRONT_BOARD_MAX_DEG as FB,
)
from tbs_title_block import title_block
from tbs_constants import DISTORTION_DPI

# ── Camera constants ──────────────────────────────────────────────────────────
F = C_WID         # focal length (container interior depth, mm) = 2362
FP_W = _FP_W      # film plane width (mm) — from tbs_constants (4499mm)
FP_H = _FP_H      # film plane height (mm) = 2388
SHIFT = round(F * np.tan(np.radians(FB)))   # full image shift at the ±FB° hard stop = 219mm (was hardcoded 207, the 5° value)

# ── Cyanotype palette (dark background — matches combined distortion renders) ─
BG      = '#081A32'
C_NEAR  = '#45B0E8'
C_MID   = '#E4F4FD'
C_FAR   = '#6080A0'
C_HUMAN = '#F5D080'
C_AX    = '#7ED4F2'

D_NEAR  = 5_000 + F
D_MID   = 20_000 + F
D_FAR   = 100_000 + F

# ── Projection maths ─────────────────────────────────────────────────────────

def Rx(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])

def Ry(b):
    c, s = np.cos(b), np.sin(b)
    return np.array([[c,0,s],[0,1,0],[-s,0,c]])

def project_point(W, board_tilt_deg, board_swing_deg):
    """
    Project a world point through board rotation only (film plane flat).
    Board tilts/swings the pinhole direction; film plane stays at Z=F, flat.
    Returns (u, v) in mm on film plane, (0,0) at center. None if missed.
    """
    W = np.asarray(W, dtype=float)
    if W[2] <= 0:
        return None

    alpha = np.radians(board_tilt_deg)
    beta  = np.radians(board_swing_deg)
    W_rot = Ry(-beta) @ Rx(-alpha) @ W

    if W_rot[2] <= 0:
        return None

    t = F / W_rot[2]
    u = t * W_rot[0]
    v = t * W_rot[1]

    return u, v


def project_grid(board_tilt, board_swing,
                 depth, grid_range_m=8, grid_step_m=1):
    r = grid_range_m * 1000
    step = grid_step_m * 1000
    Z = depth

    h_lines = []
    for Y in np.arange(-r, r + step, step):
        pts = []
        for X in np.linspace(-r, r, 60):
            p = project_point((X, Y, Z), board_tilt, board_swing)
            if p is not None:
                pts.append(p)
        if pts:
            h_lines.append(pts)

    v_lines = []
    for X in np.arange(-r, r + step, step):
        pts = []
        for Y in np.linspace(-r, r, 60):
            p = project_point((X, Y, Z), board_tilt, board_swing)
            if p is not None:
                pts.append(p)
        if pts:
            v_lines.append(pts)

    return h_lines, v_lines


def project_horizon(board_tilt, board_swing, depth=D_FAR):
    pts = []
    for X in np.linspace(-10000, 10000, 120):
        p = project_point((X, 0, depth), board_tilt, board_swing)
        if p is not None:
            pts.append(p)
    return pts


def project_human(board_tilt, board_swing,
                  cx_m=0, depth=D_NEAR, height_m=1.8):
    cx = cx_m * 1000
    h = height_m * 1000
    points = []
    for Y in np.linspace(0, h*0.55, 10):
        p = project_point((cx, Y, depth), board_tilt, board_swing)
        if p: points.append(('body', p))
    for ang in np.linspace(0, 2*np.pi, 20):
        X = cx + h*0.08*np.cos(ang)
        Y = h*0.55 + h*0.1 + h*0.08*np.sin(ang)
        p = project_point((X, Y, depth), board_tilt, board_swing)
        if p: points.append(('head', p))
    for X in np.linspace(cx - h*0.3, cx + h*0.3, 15):
        p = project_point((X, h*0.45, depth), board_tilt, board_swing)
        if p: points.append(('arm', p))
    for side in [-1, 1]:
        for Y in np.linspace(0, h*0.45, 8):
            p = project_point((cx + side*Y*0.2, Y, depth),
                              board_tilt, board_swing)
            if p: points.append(('leg', p))
    return points


# ── Configuration table ───────────────────────────────────────────────────────

CONFIGS = [
    # (label, board_tilt, board_swing, description)
    ('C0', 0,    0,    'Reference — board neutral, no image shift'),
    ('C1', 2,    0,    'Mild tilt +2° — subtle vertical image steering'),
    ('C2', FB,   0,    f'Max tilt +{FB}° — full vertical image shift ({SHIFT}mm)'),
    ('C3', -FB,  0,    f'Max tilt -{FB}° — full downward image shift ({SHIFT}mm)'),
    ('C4', 0,    2,    'Mild swing +2° — subtle horizontal image steering'),
    ('C5', 0,    FB,   f'Max swing +{FB}° — full horizontal image shift'),
    ('C6', 3,    3,    'Compound +3° tilt, +3° swing — diagonal steering'),
]


def draw_render(ax, board_tilt, board_swing,
                label, description, film_w=FP_W, film_h=FP_H,
                show_human=True):
    ax.set_facecolor(BG)
    ax.set_aspect('equal')

    W2 = film_w * 0.6
    H2 = film_h * 0.6
    ax.set_xlim(-W2, W2)
    ax.set_ylim(-H2, H2)
    ax.axis('off')

    fp = Rectangle((-film_w/2, -film_h/2), film_w, film_h,
                   lw=1.2, edgecolor='#3060A0', facecolor='none', linestyle='--')
    ax.add_patch(fp)

    for depth, color, lw, zord in [(D_NEAR, C_NEAR, 1.2, 4),
                                    (D_MID,  C_MID,  0.7, 3),
                                    (D_FAR,  C_FAR,  0.5, 2)]:
        step = 2000 if depth == D_FAR else 1000
        rng  = 12 if depth == D_FAR else 8
        h_lines, v_lines = project_grid(board_tilt, board_swing,
                                         depth, grid_range_m=rng,
                                         grid_step_m=step/1000)
        alpha = 0.55 if depth == D_FAR else 0.8
        for line_pts in h_lines + v_lines:
            if len(line_pts) < 2:
                continue
            us = np.array([p[0] for p in line_pts])
            vs = np.array([p[1] for p in line_pts])
            ax.plot(us, vs, color=color, lw=lw, alpha=alpha, zorder=zord,
                    solid_capstyle='round')

    hz = project_horizon(board_tilt, board_swing)
    if len(hz) >= 2:
        us = [p[0] for p in hz]
        vs = [p[1] for p in hz]
        ax.plot(us, vs, color='#FF8040', lw=1.0, alpha=0.7, zorder=5,
                linestyle='--', label='horizon')

    if show_human:
        human_pts = project_human(board_tilt, board_swing,
                                  cx_m=-2, depth=D_NEAR)
        for kind, (u, v) in human_pts:
            lw_h = 2.5 if kind == 'head' else (1.8 if kind == 'body' else 1.2)
            ax.plot(u, v, marker='.', color=C_HUMAN, ms=lw_h, zorder=6)

    ref_pt = project_point((0, 0, D_MID), board_tilt, board_swing)
    if ref_pt:
        shift_u_mm = ref_pt[0]
        shift_v_mm = ref_pt[1]
        ax.plot(shift_u_mm, shift_v_mm, '+', color='#FF4040', ms=10, lw=1.5, zorder=8)
        ax.plot(0, 0, '+', color='#808080', ms=8, lw=1.0, zorder=7)

    ax.text(-W2 + 60, H2 - 120, label,
            color='white', fontsize=14, fontweight='bold', va='top', zorder=9,
            fontfamily='monospace')
    ax.text(-W2 + 60, H2 - 280, description,
            color=C_AX, fontsize=8, va='top', zorder=9, linespacing=1.4)

    ang_lines = [
        f'Board tilt:  {board_tilt:+.1f}°',
        f'Board swing: {board_swing:+.1f}°',
        f'Film plane:  flat (0°)',
    ]
    for i, line in enumerate(ang_lines):
        ax.text(-W2 + 60, -H2 + 360 - i*110,
                line, color=C_AX, fontsize=7.5, va='bottom', zorder=9,
                fontfamily='monospace')

    if ref_pt:
        ax.text(W2 - 60, -H2 + 360,
                f'Image center:\nU={shift_u_mm:+.0f}mm\nV={shift_v_mm:+.0f}mm',
                color='#FF8080', fontsize=7, va='bottom', ha='right', zorder=9,
                fontfamily='monospace')

    legend_items = [
        (C_NEAR, f'Near  {D_NEAR/1000:.0f}m'),
        (C_MID,  f'Mid   {D_MID/1000:.0f}m'),
        (C_FAR,  f'Far   {D_FAR/1000:.0f}m'),
        ('#FF8040', 'Horizon'),
        (C_HUMAN,  'Figure'),
    ]
    for i, (col, lab) in enumerate(legend_items):
        ax.plot([W2 - 450, W2 - 300], [H2 - 150 - i*110, H2 - 150 - i*110],
                color=col, lw=2.0, zorder=9)
        ax.text(W2 - 280, H2 - 150 - i*110, lab,
                color=col, fontsize=7, va='center', zorder=9, fontfamily='monospace')

    ax.text(film_w/2, -film_h/2, 'FILM PLANE BOUNDARY',
            color='#3060A0', fontsize=6, ha='right', va='bottom', alpha=0.8, zorder=9)


# ── Render individual configs ─────────────────────────────────────────────────

if __name__ == '__main__':
    print("Rendering tilt-swing board-only distortion configurations...")

    for cfg in CONFIGS:
        label, bt, bs, desc = cfg
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor(BG)
        fig.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.05)

        draw_render(ax, bt, bs, label, desc)

        ax_tb = fig.add_axes([0, 0, 1, 1], facecolor="none")
        ax_tb.axis("off")
        title_block(ax_tb, f"{label}",
                    drawing_title="TILT-SWING BOARD DISTORTION",
                    subtitle=f"Board only (film flat) — {desc}",
                    scale_note="Ray-traced projection",
                    doc_id="TBS-TS01 · Board Distortion")
        out = os.path.join(DIAGRAMS_DIR, f'tilt-swing-board-distortion-{label.lower()}.png')
        fig.savefig(out, dpi=DISTORTION_DPI, bbox_inches='tight', facecolor=BG)
        plt.close(fig)
        print(f'  → {out}')

    # ── Summary grid (2×4) ────────────────────────────────────────────────────
    n = len(CONFIGS)
    ncols = 4
    nrows = 2
    fig_s, axes = plt.subplots(nrows, ncols, figsize=(24, 12))
    fig_s.patch.set_facecolor(BG)
    fig_s.subplots_adjust(left=0.02, right=0.98, top=0.93, bottom=0.02,
                          wspace=0.04, hspace=0.08)

    for idx, cfg in enumerate(CONFIGS):
        label, bt, bs, desc = cfg
        row, col = divmod(idx, ncols)
        ax = axes[row][col]
        draw_render(ax, bt, bs, label, desc, show_human=True)

    for j in range(n, nrows * ncols):
        r, c = divmod(j, ncols)
        axes[r][c].axis('off')
        axes[r][c].set_facecolor(BG)

    ax_tb = fig_s.add_axes([0, 0, 1, 1], facecolor="none")
    ax_tb.axis("off")
    title_block(ax_tb, "SUMMARY",
                drawing_title="TILT-SWING BOARD DISTORTION",
                subtitle="Board only (film flat) — all 7 configurations",
                scale_note="Ray-traced projection",
                doc_id="TBS-TS01 · Board Distortion")
    out_s = os.path.join(DIAGRAMS_DIR, 'tilt-swing-board-distortion-summary.png')
    fig_s.savefig(out_s, dpi=DISTORTION_DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig_s)
    print(f'  → {out_s}')
    print('Done.')
