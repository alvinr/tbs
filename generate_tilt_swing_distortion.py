#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_tilt_swing_distortion.py
Combined optical distortion renders: front-board tilt/swing + film-plane tilt/swing
The Big Shoebox Project

Projects a world grid through two stacked transformations:
  1. Front-board rotation (tilts/swings the pinhole pointing direction)
  2. Film-plane tilt/swing (changes the recording surface orientation)

Output: tilt-swing-combined-c0.png … c8.png + tilt-swing-combined-summary.png
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ── Camera constants ──────────────────────────────────────────────────────────
F = 2362          # focal length (container interior width, mm)
FP_W = 3549       # film plane width (mm)  [rev 2: was 2920, was 5893]
FP_H = 2388       # film plane height (mm)

# ── Cyanotype palette (dark background — matches film-plane distortion renders) ─
BG      = '#081A32'
C_NEAR  = '#45B0E8'   # near depth grid — cyan
C_MID   = '#E4F4FD'   # mid depth grid — paper white
C_FAR   = '#6080A0'   # far / horizon — grey-blue
C_HUMAN = '#F5D080'   # human silhouette — warm gold
C_AX    = '#7ED4F2'   # annotation text

# Subject depths from pinhole (mm)
# Container interior is 2362 mm wide; subject is outside (scene side)
# Distances from pinhole: near=5m, mid=20m, far=~100m
D_NEAR  = 5_000 + F    # ~7362 mm from pinhole (5m from container exterior)
D_MID   = 20_000 + F
D_FAR   = 100_000 + F

# ── Projection maths ─────────────────────────────────────────────────────────

def Rx(a):
    """Rotation matrix about X axis (tilt) — angle in radians."""
    c, s = np.cos(a), np.sin(a)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])

def Ry(b):
    """Rotation matrix about Y axis (swing) — angle in radians."""
    c, s = np.cos(b), np.sin(b)
    return np.array([[c,0,s],[0,1,0],[-s,0,c]])

def project_point(W, board_tilt_deg, board_swing_deg,
                  film_tilt_deg, film_swing_deg):
    """
    Project a single world point W=(X,Y,Z) through the combined system.

    Step 1: Rotate world by inverse of board angles (front-board tilt α and swing β)
            W' = Ry(-β) · Rx(-α) · W
    Step 2: Cast ray from pinhole (origin) through W' and intersect tilted film plane.
            Film plane is centred at r0=(0,0,F), tilted by film_tilt θ (about X) and
            film_swing φ (about Y).
            Film plane normal: n = Ry(φ)·Rx(θ)·[0,0,-1]
            (normal points toward subject, i.e. in -Z direction from film)
            Intersection: t = (n·r0)/(n·d);  F_world = t·d
    Step 3: Map world intersection point to 2D film coordinates (U, V).
            The film's own local axes: u_film = Ry(φ)·[1,0,0],
                                       v_film = Rx(θ)·Ry(φ)·[0,1,0] ≈ [0,1,0] for small θ

    Returns (u, v) in mm on the film plane, with (0,0) at film centre.
    Returns None if the ray misses (behind pinhole or parallel to film).
    """
    W = np.asarray(W, dtype=float)
    if W[2] <= 0:
        return None  # behind or at pinhole

    # Step 1 — board rotation
    alpha = np.radians(board_tilt_deg)
    beta  = np.radians(board_swing_deg)
    W_rot = Ry(-beta) @ Rx(-alpha) @ W

    if W_rot[2] <= 0:
        return None

    # Ray direction (unit vector from pinhole to W')
    d = W_rot / np.linalg.norm(W_rot)

    # Step 2 — film plane intersection
    theta = np.radians(film_tilt_deg)
    phi   = np.radians(film_swing_deg)
    # Film plane normal (pointing toward subject = -Z in film-plane local frame)
    n = Ry(phi) @ Rx(theta) @ np.array([0, 0, -1.0])
    # Anchor point at film plane centre
    r0 = np.array([0.0, 0.0, F])

    denom = np.dot(n, d)
    if abs(denom) < 1e-9:
        return None  # ray parallel to film

    t = np.dot(n, r0) / denom
    if t <= 0:
        return None  # intersection behind pinhole

    F_world = t * d  # 3D point on film plane

    # Step 3 — project onto film 2D axes
    # Film's local horizontal axis (u): rotated X axis
    u_axis = Ry(phi) @ np.array([1.0, 0.0, 0.0])
    # Film's local vertical axis (v): rotated Y axis
    v_axis = Rx(theta) @ Ry(phi) @ np.array([0.0, 1.0, 0.0])

    F_offset = F_world - r0
    u = np.dot(F_offset, u_axis)
    v = np.dot(F_offset, v_axis)

    return u, v


def project_grid(board_tilt, board_swing, film_tilt, film_swing,
                 depth, grid_range_m=8, grid_step_m=1):
    """Return (u_lines, v_lines) — lists of projected horizontal and vertical grid lines."""
    r = grid_range_m * 1000  # mm
    step = grid_step_m * 1000
    Z = depth

    h_lines = []  # horizontal grid lines (constant Y)
    for Y in np.arange(-r, r + step, step):
        pts = []
        for X in np.linspace(-r, r, 60):
            p = project_point((X, Y, Z), board_tilt, board_swing, film_tilt, film_swing)
            if p is not None:
                pts.append(p)
        if pts:
            h_lines.append(pts)

    v_lines = []  # vertical grid lines (constant X)
    for X in np.arange(-r, r + step, step):
        pts = []
        for Y in np.linspace(-r, r, 60):
            p = project_point((X, Y, Z), board_tilt, board_swing, film_tilt, film_swing)
            if p is not None:
                pts.append(p)
        if pts:
            v_lines.append(pts)

    return h_lines, v_lines


def project_horizon(board_tilt, board_swing, film_tilt, film_swing, depth=D_FAR):
    """Return list of (u,v) for the horizon line (Y=0, very far depth)."""
    pts = []
    for X in np.linspace(-10000, 10000, 120):
        p = project_point((X, 0, depth), board_tilt, board_swing, film_tilt, film_swing)
        if p is not None:
            pts.append(p)
    return pts


def project_human(board_tilt, board_swing, film_tilt, film_swing,
                  cx_m=0, depth=D_NEAR, height_m=1.8):
    """Return list of (u,v) points tracing a simplified human silhouette."""
    cx = cx_m * 1000
    h = height_m * 1000
    # Simple stick figure: head (circle approximated), body, arms, legs
    # All at X=cx, varying Y (height), fixed Z=depth
    points = []
    # body line
    for Y in np.linspace(0, h*0.55, 10):
        p = project_point((cx, Y, depth), board_tilt, board_swing, film_tilt, film_swing)
        if p: points.append(('body', p))
    # head (top)
    for ang in np.linspace(0, 2*np.pi, 20):
        X = cx + h*0.08*np.cos(ang)
        Y = h*0.55 + h*0.1 + h*0.08*np.sin(ang)
        p = project_point((X, Y, depth), board_tilt, board_swing, film_tilt, film_swing)
        if p: points.append(('head', p))
    # arms
    for X in np.linspace(cx - h*0.3, cx + h*0.3, 15):
        p = project_point((X, h*0.45, depth), board_tilt, board_swing, film_tilt, film_swing)
        if p: points.append(('arm', p))
    # legs
    for side in [-1, 1]:
        for Y in np.linspace(0, h*0.45, 8):
            p = project_point((cx + side*Y*0.2, Y, depth),
                              board_tilt, board_swing, film_tilt, film_swing)
            if p: points.append(('leg', p))
    return points


# ── Configuration table ───────────────────────────────────────────────────────

CONFIGS = [
    # (label, board_tilt, board_swing, film_tilt, film_swing, description)
    ('C0', 0,  0,   0,   0,  'Reference\nAll flat'),
    ('C1', 3,  0,   0,   0,  'Board tilt +3°\nFilm flat'),
    ('C2', 0,  0,  20,   0,  'Film tilt +20°\nBoard flat'),
    ('C3', 3,  0,  20,   0,  'Both tilt +\nsame direction\n(amplified)'),
    ('C4', 3,  0, -20,   0,  'Opposing tilt\n(partially cancelled)'),
    ('C5', 0,  3,   0,  15,  'Both swing +\nsame direction'),
    ('C6', 3,  3,   0,   0,  'Compound board\n(tilt+swing)\nflat film'),
    ('C7', 3,  3,  20,  15,  'Full compound\nboth systems\n(max distortion)'),
    ('C8',-3,  3,  20, -15,  'Opposing compound\n(surrealist)'),
]


def draw_render(ax, board_tilt, board_swing, film_tilt, film_swing,
                label, description, film_w=FP_W, film_h=FP_H,
                show_human=True):
    """Render one configuration onto ax."""
    ax.set_facecolor(BG)
    ax.set_aspect('equal')

    # Film plane extent (display window) — show ±60% of film dimensions
    W2 = film_w * 0.6
    H2 = film_h * 0.6
    ax.set_xlim(-W2, W2)
    ax.set_ylim(-H2, H2)
    ax.axis('off')

    # Film plane boundary
    fp = Rectangle((-film_w/2, -film_h/2), film_w, film_h,
                   lw=1.2, edgecolor='#3060A0', facecolor='none', linestyle='--')
    ax.add_patch(fp)

    # Grid at three depths
    for depth, color, lw, zord in [(D_NEAR, C_NEAR, 1.2, 4),
                                    (D_MID,  C_MID,  0.7, 3),
                                    (D_FAR,  C_FAR,  0.5, 2)]:
        step = 2000 if depth == D_FAR else 1000
        rng  = 12 if depth == D_FAR else 8
        h_lines, v_lines = project_grid(board_tilt, board_swing, film_tilt, film_swing,
                                         depth, grid_range_m=rng, grid_step_m=step/1000)
        alpha = 0.55 if depth == D_FAR else 0.8
        for line_pts in h_lines + v_lines:
            if len(line_pts) < 2:
                continue
            us = np.array([p[0] for p in line_pts])
            vs = np.array([p[1] for p in line_pts])
            ax.plot(us, vs, color=color, lw=lw, alpha=alpha, zorder=zord,
                    solid_capstyle='round')

    # Horizon line
    hz = project_horizon(board_tilt, board_swing, film_tilt, film_swing)
    if len(hz) >= 2:
        us = [p[0] for p in hz]
        vs = [p[1] for p in hz]
        ax.plot(us, vs, color='#FF8040', lw=1.0, alpha=0.7, zorder=5,
                linestyle='--', label='horizon')

    # Human figure
    if show_human:
        human_pts = project_human(board_tilt, board_swing, film_tilt, film_swing,
                                  cx_m=-2, depth=D_NEAR)
        for kind, (u, v) in human_pts:
            lw_h = 2.5 if kind == 'head' else (1.8 if kind == 'body' else 1.2)
            m = 'o' if kind == 'head' else '.'
            ax.plot(u, v, marker='.', color=C_HUMAN, ms=lw_h, zorder=6)

    # Compute image-centre shift for annotation
    ref_pt = project_point((0, 0, D_MID), board_tilt, board_swing, film_tilt, film_swing)
    if ref_pt:
        shift_u_mm = ref_pt[0]
        shift_v_mm = ref_pt[1]
        # Mark image centre
        ax.plot(shift_u_mm, shift_v_mm, '+', color='#FF4040', ms=10, lw=1.5, zorder=8)
        ax.plot(0, 0, '+', color='#808080', ms=8, lw=1.0, zorder=7)

    # Title and angle labels
    ax.text(-W2 + 60, H2 - 120, label,
            color='white', fontsize=14, fontweight='bold', va='top', zorder=9,
            fontfamily='monospace')
    ax.text(-W2 + 60, H2 - 280, description,
            color=C_AX, fontsize=8, va='top', zorder=9, linespacing=1.4)

    # Angle table (bottom left)
    ang_lines = [
        f'Board tilt:  {board_tilt:+.0f}°',
        f'Board swing: {board_swing:+.0f}°',
        f'Film tilt:   {film_tilt:+.0f}°',
        f'Film swing:  {film_swing:+.0f}°',
    ]
    for i, line in enumerate(ang_lines):
        ax.text(-W2 + 60, -H2 + 360 - i*110,
                line, color=C_AX, fontsize=7.5, va='bottom', zorder=9,
                fontfamily='monospace')

    # Image shift annotation (bottom right)
    if ref_pt:
        ax.text(W2 - 60, -H2 + 360,
                f'Image centre:\nU={shift_u_mm:+.0f} mm\nV={shift_v_mm:+.0f} mm',
                color='#FF8080', fontsize=7, va='bottom', ha='right', zorder=9,
                fontfamily='monospace')

    # Near/mid/far legend (top right)
    legend_items = [
        (C_NEAR, f'Near  {D_NEAR/1000:.0f} m'),
        (C_MID,  f'Mid   {D_MID/1000:.0f} m'),
        (C_FAR,  f'Far   {D_FAR/1000:.0f} m'),
        ('#FF8040', 'Horizon'),
        (C_HUMAN,  'Figure'),
    ]
    for i, (col, lab) in enumerate(legend_items):
        ax.plot([W2 - 450, W2 - 300], [H2 - 150 - i*110, H2 - 150 - i*110],
                color=col, lw=2.0, zorder=9)
        ax.text(W2 - 280, H2 - 150 - i*110, lab,
                color=col, fontsize=7, va='center', zorder=9, fontfamily='monospace')

    # Film plane boundary label
    ax.text(film_w/2, -film_h/2, 'FILM PLANE BOUNDARY',
            color='#3060A0', fontsize=6, ha='right', va='bottom', alpha=0.8, zorder=9)


# ── Render individual configs ─────────────────────────────────────────────────

for cfg in CONFIGS:
    label, bt, bs, ft, fs, desc = cfg
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(BG)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.05)

    draw_render(ax, bt, bs, ft, fs, label, desc)

    # Title bar
    fig.text(0.5, 0.97,
             'THE BIG SHOEBOX PROJECT — Combined Board+Film Plane Distortion',
             ha='center', va='top', fontsize=9, color='#E4F4FD', fontfamily='monospace')

    fig.text(0.99, 0.005, "© 2026 Alvin Richards — GNU AGPLv3",
             ha="right", va="bottom", fontsize=6, color="#667788", style="italic")
    out = f'diagrams/tilt-swing-combined-{label.lower()}.png'
    fig.savefig(out, dpi=120, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'  → {out}  Done.')


# ── Summary grid (3×3) ────────────────────────────────────────────────────────

fig_s, axes = plt.subplots(3, 3, figsize=(24, 18))
fig_s.patch.set_facecolor(BG)
fig_s.subplots_adjust(left=0.02, right=0.98, top=0.93, bottom=0.02,
                      wspace=0.04, hspace=0.08)

fig_s.text(0.5, 0.965,
           'THE BIG SHOEBOX PROJECT — Combined Front-Board & Film-Plane Distortion',
           ha='center', fontsize=14, color='#E4F4FD', fontfamily='monospace', fontweight='bold')
fig_s.text(0.5, 0.947,
           'Rows: board tilt variations  |  Cols: board swing + compound   |  '
           'Red + = image centre  |  Grey + = nominal centre  |  Horizon = orange dashed',
           ha='center', fontsize=9, color=C_AX, fontfamily='monospace')

for idx, (cfg, ax) in enumerate(zip(CONFIGS, axes.flat)):
    label, bt, bs, ft, fs, desc = cfg
    draw_render(ax, bt, bs, ft, fs, label, desc, show_human=True)

fig_s.text(0.99, 0.005, "© 2026 Alvin Richards — GNU AGPLv3",
           ha="right", va="bottom", fontsize=6, color="#667788", style="italic")
out_s = 'diagrams/tilt-swing-combined-summary.png'
fig_s.savefig(out_s, dpi=100, bbox_inches='tight', facecolor=BG)
plt.close(fig_s)
print(f'  → {out_s}  Done.')
print()
print('All renders complete.')
