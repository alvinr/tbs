#!/usr/bin/env python3
"""
generate_film_plane_distortion.py
Simulates pinhole projection onto a tilted film plane.

For each pixel on the tilted film plane, ray-traces back through the pinhole
to find the corresponding scene point. The result shows what the tilted film
records, presented as a flattened image.

Outputs: film-plane-distortion-c0.png … film-plane-distortion-c6.png
         film-plane-distortion-summary.png
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ── Container / camera constants (mm) ────────────────────────────────────────
FILM_L = 5893    # film plane width  (container length)
FILM_H = 2388    # film plane height (container height)
F_NOM  = 2362    # nominal focal length (container width = optical axis)
D_NEAR = 100     # closest carriage position
D_FAR  = F_NOM - 100   # = 2262

# Cyanotype palette for renders
PRU_INK   = np.array([0.031, 0.102, 0.196])
PRU_DEEP  = np.array([0.059, 0.176, 0.369])
PRU_MID   = np.array([0.090, 0.333, 0.627])
PRU_LIGHT = np.array([0.180, 0.510, 0.831])
CYAN_MID  = np.array([0.271, 0.690, 0.910])
CYAN_LITE = np.array([0.494, 0.831, 0.949])
PAPER_W   = np.array([0.941, 0.980, 1.000])

# Tilt configurations: (label, d_top, d_bot, description)
CONFIGS = [
    ("C0", "Flat  0°",           D_FAR,  D_FAR,
     "Reference — no distortion. Film plane flush to far wall."),
    ("C1", "Mild tilt  5.6°",    1800,   D_FAR,
     "Subtle keystone. Top edge 462mm closer. Top of image gently compressed."),
    ("C2", "Strong tilt  17.5°", 800,    D_FAR,
     "Dramatic keystone. Top 1,462mm closer. Top heavily compressed, bottom stretched."),
    ("C3", "Max tilt  41.6°",    D_NEAR, D_FAR,
     "Extreme. Top edge 2,162mm closer than bottom. Radical perspective break."),
    ("C4", "Reverse max  41.6°", D_FAR,  D_NEAR,
     "Inverted max tilt. Bottom rushes forward. Ground-rush effect."),
    ("C5", "Both near  0°",      D_NEAR, D_NEAR,
     "Flat plane 2,162mm closer than nominal. Uniform magnification boost ~2.3×."),
    ("C6", "Compound  41.6°+15°",D_NEAR, D_FAR,
     "Max tilt PLUS 15° swing. Diagonal perspective break — no parallel lines."),
]


# ═══════════════════════════════════════════════════════════════════════════════
# Scene generators — return RGB arrays (H, W, 3) for scene points (P_X, P_Y)
# P_X: world horizontal (mm, +right), P_Y: world vertical (mm, +up)
# ═══════════════════════════════════════════════════════════════════════════════

def checker_scene(P_X, P_Y, cell_mm=600):
    """Alternating checker pattern with centre cross."""
    cx = (np.floor(P_X / cell_mm) % 2).astype(int)
    cy = (np.floor(P_Y / cell_mm) % 2).astype(int)
    checker = (cx ^ cy).astype(float)

    img = np.zeros((*P_X.shape, 3), dtype=np.float32)
    # Dark squares: PRU_INK, light squares: CYAN_LITE
    for c in range(3):
        img[..., c] = checker * CYAN_LITE[c] + (1-checker) * PRU_INK[c]

    # Grid lines every cell_mm
    lx = (P_X % cell_mm) / cell_mm
    ly = (P_Y % cell_mm) / cell_mm
    line_mask = (lx < 0.04) | (ly < 0.04)
    img[line_mask] = PRU_MID

    # Horizon line (Y=0) and vertical centre (X=0)
    h_line = np.abs(P_Y) < 80
    v_line = np.abs(P_X) < 80
    img[h_line] = PAPER_W
    img[v_line] = PAPER_W

    # Concentric rings from centre for scale reference
    r = np.sqrt(P_X**2 + P_Y**2)
    for ring_r in [1000, 2000, 3000, 4000, 5000, 7000, 10000]:
        ring_mask = np.abs(r - ring_r) < 60
        img[ring_mask] = CYAN_MID * 0.85

    return np.clip(img, 0, 1)


def landscape_scene(P_X, P_Y):
    """
    Cityscape + person silhouette scene.
    Sky above horizon (Y>0), ground below (Y<0).
    Several buildings, a person at centre.
    """
    img = np.zeros((*P_X.shape, 3), dtype=np.float32)

    # Sky gradient
    sky_mask = P_Y >= 0
    sky_t = np.clip(P_Y / 8000, 0, 1)
    for c in range(3):
        sky_col = PRU_DEEP[c] + sky_t * (PRU_MID[c] - PRU_DEEP[c])
        img[..., c] = np.where(sky_mask, sky_col, img[..., c])

    # Ground gradient
    gnd_mask = P_Y < 0
    gnd_t = np.clip(-P_Y / 5000, 0, 1)
    for c in range(3):
        gnd_col = PRU_INK[c] + gnd_t * (PRU_DEEP[c] - PRU_INK[c])
        img[..., c] = np.where(gnd_mask, gnd_col, img[..., c])

    # Horizon stripe
    hor_mask = np.abs(P_Y) < 120
    img[hor_mask] = CYAN_MID * 0.6

    # Buildings (defined as x_centre, width, height, each in mm)
    buildings = [
        (-8000, 2800, 6500),
        (-4500, 2000, 8000),
        (-1500, 3000, 5500),
        (2500,  2200, 7000),
        (5500,  2600, 4500),
        (8500,  1800, 9000),
        (-11000, 3500, 5000),
        (11000, 2000, 6000),
    ]
    for bx, bw, bh in buildings:
        bmask = (P_X >= bx - bw/2) & (P_X <= bx + bw/2) & (P_Y >= 0) & (P_Y <= bh)
        # Building fill — slightly lighter than sky
        for c in range(3):
            bld_col = PRU_DEEP[c] * 0.7
            img[..., c] = np.where(bmask, bld_col, img[..., c])
        # Window pattern
        for wy in np.arange(400, bh - 400, 700):
            for wx in np.arange(bx - bw/2 + 350, bx + bw/2 - 200, 500):
                wmask = (np.abs(P_X - wx) < 120) & (np.abs(P_Y - wy) < 150) & bmask
                img[wmask] = CYAN_LITE * 0.8
        # Building outline
        outl = ((np.abs(P_X - (bx-bw/2)) < 60) | (np.abs(P_X - (bx+bw/2)) < 60)) & \
               (P_Y >= 0) & (P_Y <= bh)
        img[outl] = CYAN_MID * 0.5
        top_outl = (P_X >= bx-bw/2) & (P_X <= bx+bw/2) & (np.abs(P_Y - bh) < 60)
        img[top_outl] = CYAN_MID * 0.5

    # Person silhouette at X=0, height 1800mm
    person_w = 380
    # Legs
    leg_mask = (np.abs(P_X) < person_w/2) & (P_Y >= -1500) & (P_Y < 0)
    img[leg_mask] = PAPER_W * 0.9
    # Body
    body_mask = (np.abs(P_X) < person_w*0.65) & (P_Y >= 0) & (P_Y < 1100)
    img[body_mask] = PAPER_W * 0.9
    # Head
    head_r = 280
    head_mask = ((P_X**2 + (P_Y - 1380)**2) < head_r**2)
    img[head_mask] = PAPER_W * 0.9
    # Arms
    arm_mask = (np.abs(P_X) < person_w*1.5) & (np.abs(P_X) > person_w*0.6) & \
               (P_Y > 300) & (P_Y < 800)
    img[arm_mask] = PAPER_W * 0.9

    # Ground grid lines
    for gx in np.arange(-15000, 15001, 1500):
        gline = (np.abs(P_X - gx) < 50) & (P_Y < 0)
        img[gline] = PRU_MID * 0.8

    # Ground perspective lines converging to horizon
    for ang in np.radians(np.arange(-75, 76, 15)):
        # Lines radiating from centre of horizon
        dist = P_X - P_Y * np.tan(ang) if np.cos(ang) != 0 else np.inf
        pline = (np.abs(dist) < 60) & (P_Y < 0)
        img[pline] = PRU_MID * 0.8

    return np.clip(img, 0, 1)


# ═══════════════════════════════════════════════════════════════════════════════
# Core projection engine
# ═══════════════════════════════════════════════════════════════════════════════

def project_onto_tilted_plane(d_top, d_bot, scene_func, D,
                               out_w=900, out_h=600,
                               swing_deg=0.0):
    """
    Backward ray-trace: for each pixel on the tilted film plane,
    compute the scene point seen through the pinhole.

    d_top, d_bot: depth of top/bottom film edge from pinhole (mm)
    D: subject distance (mm)
    swing_deg: additional swing rotation about vertical axis (degrees)
    out_w, out_h: output image dimensions
    """
    # Film plane parameterisation
    # u: 0→1 = left→right (X: -FILM_L/2 → +FILM_L/2)
    # v: 0→1 = bottom→top
    u = np.linspace(0, 1, out_w)[np.newaxis, :]   # (1, W)
    v = np.linspace(0, 1, out_h)[:, np.newaxis]   # (H, 1) — 0=bottom
    v_img = v[::-1, :]                             # flip: row 0 = top of image

    F_X = (u - 0.5) * FILM_L              # (1, W)
    F_Y = (v_img - 0.5) * FILM_H          # (H, 1)
    # Depth of each film point (tilt: varies linearly with v from bot to top)
    F_Z = d_bot + (d_top - d_bot) * v_img  # (H, 1)

    # Apply swing rotation about vertical (Y) axis if requested
    if abs(swing_deg) > 0.001:
        s = np.sin(np.radians(swing_deg))
        swing_offset = F_X * s       # (1, W) — left edge comes closer, right goes back
        F_Z = F_Z + swing_offset     # broadcasts to (H, W)

    # Broadcast all grids to full (out_h, out_w) before projection
    F_X = np.broadcast_to(F_X, (out_h, out_w)).copy()
    F_Y = np.broadcast_to(F_Y, (out_h, out_w)).copy()
    F_Z = np.broadcast_to(F_Z, (out_h, out_w)).copy()

    # Backward ray: film point (F_X, F_Y, F_Z) → pinhole (0,0,0) → scene
    valid = F_Z > 10

    with np.errstate(divide="ignore", invalid="ignore"):
        P_X = np.where(valid, -F_X * D / F_Z, 0.0)
        P_Y = np.where(valid, -F_Y * D / F_Z, 0.0)

    img = scene_func(P_X, P_Y)

    # Mask invalid regions
    img[~valid] = PRU_INK

    # Subtle vignette: nearer film → slightly elevated brightness at image centre
    mag = np.where(valid, F_NOM / np.maximum(F_Z, 1), 0)
    vig = np.clip(1.0 - (mag - 1.0) * 0.06, 0.3, 1.0)
    img = img * vig[..., np.newaxis]

    return np.clip(img, 0, 1)


def annotate_render(ax, label, name, d_top, d_bot, desc, D, swing=0):
    """Add annotation overlay to a rendered image axis."""
    ang = np.degrees(np.arctan2(abs(d_top - d_bot), FILM_H - 120))
    fp_len = int(np.sqrt((d_top-d_bot)**2 + (FILM_H-120)**2))
    area_chg = round((fp_len / (FILM_H-120) - 1) * 100)

    ax.text(0.01, 0.99, f"{label}  ·  {name}",
            transform=ax.transAxes, color=PAPER_W, fontsize=9,
            va="top", fontfamily="monospace", fontweight="bold",
            bbox=dict(fc=PRU_INK*0.8, ec="none", alpha=0.8, pad=3))

    swing_str = f"  +swing {swing:.0f}°" if abs(swing) > 0.1 else ""
    spec = (f"top={d_top}mm  bot={d_bot}mm  θ={ang:.1f}°{swing_str}"
            f"  D={D//1000}m  area+{area_chg}%")
    ax.text(0.01, 0.01, spec,
            transform=ax.transAxes, color=CYAN_LITE, fontsize=7.5,
            va="bottom", fontfamily="monospace",
            bbox=dict(fc=PRU_INK*0.8, ec="none", alpha=0.8, pad=2))

    ax.text(0.99, 0.01, desc,
            transform=ax.transAxes, color=PAPER_W * 0.7, fontsize=7,
            va="bottom", ha="right", fontfamily="monospace",
            bbox=dict(fc=PRU_INK*0.6, ec="none", alpha=0.75, pad=2))

    ax.axis("off")


# ═══════════════════════════════════════════════════════════════════════════════
# Render each configuration
# ═══════════════════════════════════════════════════════════════════════════════

def render_config(cfg_id, label, name, d_top, d_bot, desc,
                  D_scene=8000, swing=0.0):
    """Render a single config — two scenes side by side."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    fig.patch.set_facecolor("white")

    scenes = [
        (checker_scene, "CHECKER GRID  ·  600mm cells  ·  rings @ 1m intervals"),
        (landscape_scene, "CITYSCAPE SCENE  ·  subject @ centre, 1,800mm tall"),
    ]

    for ax, (sfunc, scene_name) in zip(axes, scenes):
        swing_angle = swing if sfunc == landscape_scene else 0.0
        img = project_onto_tilted_plane(d_top, d_bot, sfunc, D_scene,
                                        out_w=840, out_h=560,
                                        swing_deg=swing_angle)
        ax.imshow(img, origin="upper", aspect="auto",
                  extent=[-FILM_L/2, FILM_L/2, -FILM_H/2, FILM_H/2])
        annotate_render(ax, label, name, d_top, d_bot, desc, D_scene, swing_angle)
        ax.set_title(scene_name, color="#222222", fontsize=8,
                     fontfamily="monospace", pad=4)

    fig.suptitle(f"TBS-001 FILM PLANE DISTORTION  ·  {label}: {name}",
                 color="#111111", fontsize=11, fontfamily="monospace",
                 fontweight="bold", y=1.01)
    fig.tight_layout(pad=0.6)

    fname = f"film-plane-distortion-{label.lower()}.png"
    fig.savefig(fname, dpi=120, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print(f"  → {fname}")


def render_summary():
    """3×3 grid comparing all configs on the checker scene."""
    n = len(CONFIGS)
    ncols = 4
    nrows = 2
    fig, axes = plt.subplots(nrows, ncols, figsize=(20, 10))
    fig.patch.set_facecolor("white")

    for i, (label, name, d_top, d_bot, desc) in enumerate(CONFIGS):
        row, col = divmod(i, ncols)
        ax = axes[row][col]
        swing = 15.0 if "Compound" in name else 0.0
        img = project_onto_tilted_plane(d_top, d_bot, checker_scene, 8000,
                                        out_w=560, out_h=373,
                                        swing_deg=swing)
        ax.imshow(img, origin="upper", aspect="auto")
        ax.set_title(f"{label} · {name}", color="#111111",
                     fontsize=8.5, fontfamily="monospace", pad=3)
        ax.text(0.01, 0.03, f"T={d_top} B={d_bot}",
                transform=ax.transAxes, color=PAPER_W * 0.8,
                fontsize=7, fontfamily="monospace",
                bbox=dict(fc=PRU_INK*0.8, ec="none", pad=2))
        ax.axis("off")

    # Hide spare axes
    for j in range(n, nrows * ncols):
        r, c = divmod(j, ncols)
        axes[r][c].axis("off")
        axes[r][c].set_facecolor("white")

    fig.suptitle(
        "TBS-001  ·  FILM PLANE DISTORTION SUMMARY  ·  CHECKER SCENE  ·  D = 8,000 mm",
        color="#111111", fontsize=13, fontfamily="monospace",
        fontweight="bold", y=1.005)
    fig.tight_layout(pad=0.5)
    fig.savefig("film-plane-distortion-summary.png", dpi=120,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  → film-plane-distortion-summary.png")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Rendering film plane distortion configurations...")
    for label, name, d_top, d_bot, desc in CONFIGS:
        swing = 15.0 if "Compound" in name else 0.0
        render_config(label.lower(), label, name, d_top, d_bot, desc,
                      D_scene=8000, swing=swing)
    render_summary()
    print("Done.")
