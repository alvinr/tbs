#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""GRP walkway grating cut plan — molded-FRP 36"×120" panels.

Every walkway grate piece is taken from the SAME outline functions the walkway 3D model builds
from (generate_walkway_model: near_removable_rect, near_fixed_deck_pts, far_deck_rect,
left_liftout_pts, right_grate_sections_pts), so the cut plan follows the model. Integral tabs and
notches (near bump-out, left punch-out, muslin notches) stay part of their piece. A run longer
than a panel (molded GRP tops out at 10 ft) gets one seam at the panel length — the seam must land
over a support bracket (confirm at fab). Pieces are nested bottom-left on their real outlines (both
orientations), so they tuck in beside the integral tabs. Drawn in mm (labels in mm + inches, the supplier's unit).
Output: docs/assets/grp-cutplan.png
"""
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "models"))
import generate_walkway_model as wm                      # noqa: E402
from tbs_constants import DIAGRAM_DPI, DIAGRAMS_DIR, C_OUT  # noqa: E402

IN = 25.4
PANEL_L, PANEL_W = 120 * IN, 36 * IN                     # 3048 × 914.4 mm molded-FRP panel
GAP = 6                                                  # saw kerf + edge allowance between pieces (mm)

C_KEEP = "#C8D8E8"
C_SEAM = "#B00020"


def _norm(pts, swap=False):
    """Move an outline to (0,0) with its long axis along X (the panel length)."""
    if swap:
        pts = [(y, x) for x, y in pts]
    x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts)
    return [(x - x0, y - y0) for x, y in pts]


def _rect(l, d):
    return [(0, 0), (l, 0), (l, d), (0, d)]


def _clip_x(pts, x0, x1):
    """Clip a polygon to x0 ≤ x ≤ x1 (Sutherland–Hodgman on two vertical edges), re-based to x0."""
    def clip(poly, keep, edge):
        out = []
        for i, a in enumerate(poly):
            b = poly[(i + 1) % len(poly)]
            ia, ib = keep(a), keep(b)
            if ia:
                out.append(a)
            if ia != ib:
                t = (edge - a[0]) / (b[0] - a[0])
                out.append((edge, a[1] + t * (b[1] - a[1])))
        return out
    poly = clip(pts, lambda p: p[0] >= x0 - 1e-9, x0)
    poly = clip(poly, lambda p: p[0] <= x1 + 1e-9, x1)
    return [(x - x0, y) for x, y in poly]


def pieces():
    """[(label, outline)] — every grate piece in the walkway, split at the panel length where needed."""
    x, _, l, d = wm.near_removable_rect()
    raw = [("Near — door-end removable band", _rect(l, d))]
    liftout_x = min(wm.ov.WALKWAY_NEAR_LIFTOUT_X_R, wm.WK_NEAR_WIDE_XL)
    raw.append(("Near — fixed, bump-out integral", _norm(wm.near_fixed_deck_pts(liftout_x))))
    _, _, l, d = wm.far_deck_rect()
    raw.append(("Far deck", _rect(l, d)))
    raw.append(("Left lift-out — punch-out + notch integral", _norm(wm.left_liftout_pts(), swap=True)))
    for sfx, pts in wm.right_grate_sections_pts():
        raw.append((f"Right — {sfx}", _norm(pts, swap=True)))
    out = []
    for label, pts in raw:
        length = max(p[0] for p in pts)
        if length <= PANEL_L:
            out.append((label, pts))
            continue
        out.append((f"{label} (A, seam →)", _clip_x(pts, 0, PANEL_L)))
        out.append((f"{label} (B, ← seam)", _clip_x(pts, PANEL_L, length)))
    return out


R = 4                                                    # nesting raster (mm per cell) — 3048 mm = exactly 762 cells


def _mask(pts):
    """Boolean raster of an outline (rows = y, cols = x), plus a copy dilated by the kerf GAP."""
    import numpy as np
    from matplotlib.path import Path
    w, h = max(p[0] for p in pts), max(p[1] for p in pts)
    nx, ny = int(np.ceil(w / R)), int(np.ceil(h / R))
    xs, ys = np.meshgrid((np.arange(nx) + 0.5) * R, (np.arange(ny) + 0.5) * R)
    m = Path(pts).contains_points(np.c_[xs.ravel(), ys.ravel()]).reshape(ny, nx)
    g = max(1, int(round(GAP / R)))
    d = np.zeros((ny + 2 * g, nx + 2 * g), bool)
    for dy in range(2 * g + 1):
        for dx in range(2 * g + 1):
            d[dy:dy + ny, dx:dx + nx] |= m
    return m, d[g:g + ny, g:g + nx]


def _rot180(pts):
    w, h = max(p[0] for p in pts), max(p[1] for p in pts)
    return [(w - x, h - y) for x, y in pts]


def nest(items):
    """Bottom-left nesting on the real outlines (raster at R mm): each piece, largest first, tries both
    orientations at every corner of what is already placed, so pieces tuck in beside the L-tabs.
    Returns [[(label, outline, ox, oy)], ...] per panel."""
    import numpy as np
    cols, rows = int(PANEL_L // R), int(PANEL_W // R)

    def area(pts):
        return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1]
                       for i in range(len(pts)))) / 2
    panels = []                                          # each: [occupancy grid, placed list, candidate corners]
    for label, pts in sorted(items, key=lambda it: -area(it[1])):
        done = False
        for pan in panels + [None]:
            if pan is None:
                pan = [np.zeros((rows, cols), bool), [], {(0, 0)}]
                panels.append(pan)
            occ, placed, corners = pan
            for cx, cy in sorted(corners, key=lambda c: (c[1], c[0])):
                for shape in (pts, _rot180(pts)):
                    m, md = _mask(shape)
                    ny, nx = m.shape
                    if cy + ny > rows or cx + nx > cols or (occ[cy:cy + ny, cx:cx + nx] & md).any():
                        continue
                    occ[cy:cy + ny, cx:cx + nx] |= m
                    placed.append((label, shape, cx * R, cy * R))
                    xs = {cx + int(round(x / R)) + 1 for x, _ in shape} | {cx, 0}
                    ys = {cy + int(round(y / R)) + 1 for _, y in shape} | {cy, 0}
                    corners |= {(x, y) for x in xs for y in ys}
                    done = True
                    break
                if done:
                    break
            if done:
                break
        if not done:
            raise SystemExit(f"cut plan: {label} does not fit a {PANEL_L:.0f} × {PANEL_W:.0f} mm panel")
    return [p[1] for p in panels]


def draw_panel(ax, placed, title, start):
    """Draw one panel; pieces get number tags (keyed beside the panel) starting at `start`."""
    ax.add_patch(Rectangle((0, 0), PANEL_L, PANEL_W, facecolor="#EFEFE8", edgecolor="none", zorder=0))
    key = []
    for n, (label, pts, ox, oy) in enumerate(placed, start):
        poly = [(x + ox, y + oy) for x, y in pts]
        ax.add_patch(Polygon(poly, closed=True, facecolor=C_KEEP, edgecolor=C_OUT, linewidth=1.2, zorder=2))
        xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        ax.text(min(xs) + w / 2, min(ys) + min(h, 290) / 2 + (h - min(h, 290)) * (oy > 0), str(n),
                ha="center", va="center", fontsize=9, fontweight="bold", color=C_OUT, zorder=4,
                bbox=dict(boxstyle="circle,pad=0.25", facecolor="white", edgecolor=C_OUT, linewidth=0.8))
        if "seam" in label:
            sx = max(xs) if "(A" in label else min(xs)
            ax.plot([sx, sx], [min(ys), max(ys)], color=C_SEAM, lw=2.0, zorder=3)
        key.append(f"{n}  {label} — {w:.0f} × {h:.0f} mm ({w / IN:.1f}\" × {h / IN:.1f}\")")
    ax.add_patch(Rectangle((0, 0), PANEL_L, PANEL_W, fill=False, edgecolor=C_OUT, linewidth=2.0, zorder=5))
    ax.text(PANEL_L + 80, PANEL_W, "\n".join(key), ha="left", va="top", fontsize=6.4, color=C_OUT)
    ax.set_xlim(-40, PANEL_L + 2300)
    ax.set_ylim(-40, PANEL_W + 40)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=9, fontweight="bold", loc="left", pad=4)
    return start + len(placed)


def main():
    panels = nest(pieces())
    fig, axes = plt.subplots(len(panels), 1, figsize=(15, 2.6 * len(panels) + 0.6), squeeze=False)
    n = 1
    for i, (ax, placed) in enumerate(zip(axes[:, 0], panels)):
        n = draw_panel(ax, placed, f'PANEL {chr(65 + i)}  —  36" × 120" ({PANEL_W:.0f} × {PANEL_L:.0f} mm)', n)
    fig.suptitle(f"TBS-001  ·  GRP Walkway Grating Cut Plan  ·  {len(panels)}× 36\"×120\" molded-FRP panels",
                 fontsize=11, fontweight="bold", y=0.995)
    fig.text(0.5, 0.008, "Piece outlines come from the walkway 3D model · blue = cut piece (tabs + notches integral) · "
             "tan = offcut · red line = seam at the 10 ft panel length (land it over a support bracket) · "
             "riser holes + ribbon slots are field-cut at fit-up", ha="center", fontsize=6.5, color="#505050")
    fig.tight_layout(rect=(0, 0.02, 1, 0.97))
    out = os.path.join(DIAGRAMS_DIR, "grp-cutplan.png")
    fig.savefig(out, dpi=DIAGRAM_DPI, facecolor="white", bbox_inches="tight")
    print("wrote", out, "—", len(panels), "panels")


if __name__ == "__main__":
    main()
