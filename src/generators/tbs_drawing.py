#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
tbs_drawing.py — Shared drawing helpers for all TBS engineering diagrams.

Provides dimension lines, leader lines, center lines, circles, rectangles,
bolt hole patterns, hatching, and notes blocks.  All functions take an axes
object as the first argument and use keyword defaults matching the TBS palette
in tbs_constants.py.

Usage
-----
    from tbs_drawing import (draw_dim_h, draw_dim_v, leader, draw_cl,
                             draw_circle, draw_rect, bolt_holes, hatch_rect,
                             place_label, register_pipe, reset_label_registry,
                             draw_notes)
"""

import math

import numpy as np
import matplotlib.patches as mpatches

from tbs_constants import C_OUT, C_CL, C_DIM


# ── Dimension lines ─────────────────────────────────────────────────────────

def draw_dim_h(ax, x1, x2, y, label, *, offset=12, fs=6.5, color=C_DIM,
               lw=0.8, tick_lw=0.6, zorder=15, above=True, font=None,
               perpendicular=False):
    """Horizontal dimension line with extension ticks and centered label.

    Parameters
    ----------
    ax            : matplotlib Axes
    x1, x2        : left and right x coordinates
    y             : y position of the dimension line
    label         : dimension text
    offset        : distance from dimension line to label (and tick half-length)
    fs            : font size
    color         : line and text color
    lw            : arrow line weight
    tick_lw       : extension tick line weight
    zorder        : drawing order
    above         : if True label goes above the line, else below
    font          : optional dict e.g. {"fontfamily": "monospace"}
    perpendicular : if True rotate label 90° to the line (vertical text)
    """
    tick = abs(offset) * 0.3
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", color=color, lw=lw),
                zorder=zorder)
    ax.plot([x1, x1], [y - tick, y + tick], color=color, lw=tick_lw,
            zorder=zorder)
    ax.plot([x2, x2], [y - tick, y + tick], color=color, lw=tick_lw,
            zorder=zorder)
    label_y = y + abs(offset) * 0.55 if above else y - abs(offset) * 0.55
    va = "bottom" if above else "top"
    rot = 90 if perpendicular else 0
    kw = font or {}
    ax.text((x1 + x2) / 2, label_y, label, ha="center", va=va,
            fontsize=fs, color=color, rotation=rot, zorder=zorder, **kw)


def draw_dim_v(ax, x, y1, y2, label, *, offset=12, fs=6.5, color=C_DIM,
               lw=0.8, tick_lw=0.6, zorder=15, right=False, font=None,
               perpendicular=False):
    """Vertical dimension line with extension ticks and centered label.

    Parameters
    ----------
    ax            : matplotlib Axes
    x             : x position of the dimension line
    y1, y2        : bottom and top y coordinates
    label         : dimension text
    offset        : distance from dimension line to label (and tick half-length)
    fs            : font size
    color         : line and text color
    lw            : arrow line weight
    tick_lw       : extension tick line weight
    zorder        : drawing order
    right         : if True label goes to the right of the line, else left
    font          : optional dict e.g. {"fontfamily": "monospace"}
    perpendicular : if True rotate label 90° to the line (horizontal text)
    """
    tick = abs(offset) * 0.3
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="<->", color=color, lw=lw),
                zorder=zorder)
    ax.plot([x - tick, x + tick], [y1, y1], color=color, lw=tick_lw,
            zorder=zorder)
    ax.plot([x - tick, x + tick], [y2, y2], color=color, lw=tick_lw,
            zorder=zorder)
    rot = 0 if perpendicular else 90
    if right:
        ax.text(x + abs(offset) * 0.6, (y1 + y2) / 2, label,
                ha="left", va="center", fontsize=fs, color=color,
                rotation=rot, zorder=zorder, **(font or {}))
    else:
        ax.text(x - abs(offset) * 0.6, (y1 + y2) / 2, label,
                ha="right", va="center", fontsize=fs, color=color,
                rotation=rot, zorder=zorder, **(font or {}))


# ── Leader lines ─────────────────────────────────────────────────────────────

def leader(ax, x_tip, y_tip, x_txt, y_txt, label, *, fs=6.5, color=C_OUT,
           ha="left", va="center", arrow_style="-", lw=0.7, zorder=15,
           font=None, rotation=0, bbox=None):
    """Leader line from a point to a text label.

    Parameters
    ----------
    ax              : matplotlib Axes
    x_tip, y_tip    : arrowhead / point-of-interest coordinates
    x_txt, y_txt    : label text coordinates
    label           : annotation text
    fs              : font size
    color           : line and text color
    ha              : horizontal alignment of the label
    va              : vertical alignment of the label
    arrow_style     : "-" for dotted line, "->" or "-|>" for arrowhead
    lw              : leader line weight
    zorder          : drawing order
    font            : optional dict e.g. {"fontfamily": "monospace"}
    rotation        : label text rotation in degrees (0 = horizontal)
    bbox            : optional dict for text background box
    """
    kw = font or {}
    ann_kw = {}
    if bbox is not None:
        ann_kw["bbox"] = bbox
    ax.annotate(label, xy=(x_tip, y_tip), xytext=(x_txt, y_txt),
                fontsize=fs, color=color, ha=ha, va=va, zorder=zorder,
                rotation=rotation,
                arrowprops=dict(arrowstyle=arrow_style, linestyle=":",
                                color=color, lw=lw,
                                connectionstyle="arc3,rad=0.0"),
                **ann_kw, **kw)


# ── Center lines ─────────────────────────────────────────────────────────────

def draw_cl(ax, cx, cy, r, *, horiz=True, vert=True, color=C_CL,
            lw=0.5, ext_factor=1.25, min_ext=4, zorder=2):
    """Draw center lines through (cx, cy).

    Parameters
    ----------
    cx, cy     : center point
    r          : radius or half-size of the feature
    horiz      : draw horizontal center line
    vert       : draw vertical center line
    color      : line color
    lw         : line weight
    ext_factor : extension beyond r (multiplier)
    min_ext    : minimum extension (data units)
    """
    ext = max(r * ext_factor, min_ext)
    ls = (0, (6, 2, 1, 2))  # long-dash–dot
    if horiz:
        ax.plot([cx - ext, cx + ext], [cy, cy], color=color, lw=lw,
                linestyle=ls, zorder=zorder)
    if vert:
        ax.plot([cx, cx], [cy - ext, cy + ext], color=color, lw=lw,
                linestyle=ls, zorder=zorder)


def draw_cl_h(ax, x1, x2, y, *, color=C_CL, lw=0.5, zorder=2):
    """Horizontal center line from x1 to x2 at height y."""
    ax.plot([x1, x2], [y, y], color=color, lw=lw,
            dashes=(8, 3, 2, 3), zorder=zorder)


def draw_cl_v(ax, x, y1, y2, *, color=C_CL, lw=0.5, zorder=2):
    """Vertical center line from y1 to y2 at x."""
    ax.plot([x, x], [y1, y2], color=color, lw=lw,
            dashes=(8, 3, 2, 3), zorder=zorder)


# ── Geometric primitives ────────────────────────────────────────────────────

def draw_circle(ax, cx, cy, r, *, lw=1.8, color=C_OUT, ls="-",
                fill=False, fc="none", zorder=4):
    """Circle with optional fill."""
    c = mpatches.Circle((cx, cy), r, lw=lw, edgecolor=color,
                         facecolor=fc if fill else "none",
                         linestyle=ls, zorder=zorder)
    ax.add_patch(c)


def draw_rect(ax, x, y, w, h, *, lw=1.8, color=C_OUT, fc="white", zorder=3):
    """Rectangle with optional fill."""
    r = mpatches.Rectangle((x, y), w, h, lw=lw, edgecolor=color,
                            facecolor=fc, zorder=zorder)
    ax.add_patch(r)


# ── Bolt holes ───────────────────────────────────────────────────────────────

def bolt_holes(ax, cx, cy, bc_r, n, d_r, *, color=C_OUT, lw=1.0,
               angle_offset=22.5, zorder=4):
    """Draw *n* bolt holes on a pitch-circle of radius *bc_r*.

    Parameters
    ----------
    cx, cy        : center of the bolt circle
    bc_r          : bolt-circle radius (center-to-hole-center)
    n             : number of holes
    d_r           : hole radius
    angle_offset  : angular offset of the first hole (degrees)
    """
    for i in range(n):
        angle = np.radians(angle_offset + i * 360 / n)
        bx = cx + bc_r * np.cos(angle)
        by = cy + bc_r * np.sin(angle)
        draw_circle(ax, bx, by, d_r, lw=lw, color=color, zorder=zorder)


# ── Hatching ─────────────────────────────────────────────────────────────────

# ── Label placement ─────────────────────────────────────────────────────────

# Registry of placed labels and pipe segments for collision avoidance.
# Each entry: (x, y, width_est, height_est).  Populated by place_label().
# Pipe entries: ((x1,y1), (x2,y2)).  Populated by the caller via
# register_pipe() or passed per-call.
_label_registry = []
_pipe_registry  = []


def reset_label_registry():
    """Clear the label and pipe registries (call once per sheet)."""
    _label_registry.clear()
    _pipe_registry.clear()


def register_pipe(x1, y1, x2, y2):
    """Record a pipe segment for collision avoidance."""
    _pipe_registry.append(((x1, y1), (x2, y2)))


def _point_to_segment_dist(px, py, x1, y1, x2, y2):
    """Minimum distance from point (px,py) to line segment (x1,y1)-(x2,y2)."""
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return np.hypot(px - x1, py - y1)
    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    proj_x, proj_y = x1 + t * dx, y1 + t * dy
    return np.hypot(px - proj_x, py - proj_y)


def _score_quadrant(cx, cy, dx, dy, scan_r=0.5):
    """Score a candidate label position — lower is better.

    Counts nearby pipes and existing labels within *scan_r* of the
    candidate point (cx+dx, cy+dy).
    """
    tx, ty = cx + dx, cy + dy
    score = 0.0
    for (x1, y1), (x2, y2) in _pipe_registry:
        d = _point_to_segment_dist(tx, ty, x1, y1, x2, y2)
        if d < scan_r:
            score += (scan_r - d) / scan_r   # closer pipe = higher penalty
    for lx, ly, lw, lh in _label_registry:
        d = np.hypot(tx - lx, ty - ly)
        if d < scan_r:
            score += (scan_r - d) / scan_r
    return score


# Default offset rules derived from hand-tuned label placements.
# Each entry: (dx, dy, ha, va) relative to component center.
_DEFAULTS = {
    #                  dx      dy     ha        va
    'valve':         ( 0.30, -0.03, 'left',   'center'),
    'pump':          ( 0.20, -0.10, 'left',   'center'),
    'diverter':      ( 0.40,  0.00, 'center', 'center'),
    'ext_port':      ( 0.00,  0.30, 'center', 'bottom'),
    'filter':        ( 0.00, -0.20, 'center', 'top'),
    'generic':       ( 0.15, -0.05, 'left',   'center'),
}


def place_label(ax, x, y, label, *,
                component='valve',
                radius=None,
                dx=None, dy=None,
                ha=None, va=None,
                fontsize=6, color=None,
                auto=True,
                zorder=10,
                scan_r=0.5,
                **text_kwargs):
    """Place a label near a schematic component with automatic positioning.

    Parameters
    ----------
    ax          : matplotlib Axes
    x, y        : component center coordinates
    label       : text string (may be multi-line)
    component   : 'valve', 'pump', 'diverter', 'ext_port', 'filter', 'generic'
                  Selects default offset rules.
    radius      : component symbol radius — offsets are measured from the edge,
                  not the center.  If None, uses 0.096 for valve, 0.1125 for
                  pump, 0.12 for diverter, 0.12 for ext_port, 0.0 otherwise.
    dx, dy      : explicit offset override.  If provided, auto-placement is
                  skipped for that axis (set one or both).
    ha, va      : horizontal / vertical alignment override.
    fontsize    : label font size (default 6).
    color       : text color.  If None, inherits from the calling code.
    auto        : if True (default), use quadrant scoring to pick the best
                  side when dx/dy are not supplied.  If False, use the static
                  defaults for the component type without scoring.
    scan_r      : radius for quadrant scoring collision scan (default 0.5).
    zorder      : drawing order for the text.
    **text_kwargs : passed through to ax.text() (e.g. style, fontweight).

    Returns
    -------
    matplotlib.text.Text — the placed text artist, for further tweaking.

    Examples
    --------
    # Auto-place with defaults:
    place_label(ax, 2.4, 7.0, "BV-01", component='valve', color=C_BLUE)

    # Override just the X offset, auto-pick Y:
    place_label(ax, 2.4, 7.0, "BV-01", component='valve', dx=0.35)

    # Full manual placement (auto is effectively bypassed):
    place_label(ax, 2.4, 7.0, "BV-01", dx=-0.2, dy=0.15, ha='right')
    """
    # ── Component radius defaults ────────────────────────────────────────
    _RADII = {
        'valve':    0.096,
        'pump':     0.1125,
        'diverter': 0.12,
        'ext_port': 0.12,
        'filter':   0.0,
        'generic':  0.0,
    }
    r = radius if radius is not None else _RADII.get(component, 0.0)

    # ── Fetch static defaults for this component type ────────────────────
    defs = _DEFAULTS.get(component, _DEFAULTS['generic'])
    d_dx, d_dy, d_ha, d_va = defs

    # ── Auto quadrant scoring ────────────────────────────────────────────
    if auto and (dx is None or dy is None):
        # Candidate offsets: four quadrants plus pure cardinal directions
        candidates = [
            ( abs(d_dx),  abs(d_dy)),   # NE
            (-abs(d_dx),  abs(d_dy)),   # NW
            ( abs(d_dx), -abs(d_dy)),   # SE
            (-abs(d_dx), -abs(d_dy)),   # SW
            ( abs(d_dx),  0.0),         # E
            (-abs(d_dx),  0.0),         # W
            ( 0.0,        abs(d_dy)),   # N
            ( 0.0,       -abs(d_dy)),   # S
        ]
        best_score = float('inf')
        best_cdx, best_cdy = d_dx, d_dy
        for cdx, cdy in candidates:
            # Add radius to offset so label clears the symbol edge
            eff_dx = cdx + (r * np.sign(cdx) if cdx != 0 else 0)
            eff_dy = cdy + (r * np.sign(cdy) if cdy != 0 else 0)
            s = _score_quadrant(x, y, eff_dx, eff_dy, scan_r)
            if s < best_score:
                best_score = s
                best_cdx, best_cdy = eff_dx, eff_dy
        auto_dx, auto_dy = best_cdx, best_cdy
    else:
        auto_dx = d_dx + (r * np.sign(d_dx) if d_dx != 0 else 0)
        auto_dy = d_dy

    # ── Apply overrides ──────────────────────────────────────────────────
    final_dx = dx if dx is not None else auto_dx
    final_dy = dy if dy is not None else auto_dy

    # Alignment: infer from offset direction if not explicitly given
    if ha is None:
        if final_dx > 0.01:
            ha = 'left'
        elif final_dx < -0.01:
            ha = 'right'
        else:
            ha = 'center'
    if va is None:
        va = d_va

    # ── Place the text ───────────────────────────────────────────────────
    tx, ty = x + final_dx, y + final_dy
    kw = dict(ha=ha, va=va, fontsize=fontsize, zorder=zorder)
    if color is not None:
        kw['color'] = color
    kw.update(text_kwargs)
    txt = ax.text(tx, ty, label, **kw)

    # ── Register for future collision checks ─────────────────────────────
    n_lines = label.count('\n') + 1
    est_w = len(max(label.split('\n'), key=len)) * fontsize * 0.008
    est_h = n_lines * fontsize * 0.015
    _label_registry.append((tx, ty, est_w, est_h))

    return txt


def hatch_rect(ax, x, y, w, h, *, color="#AAAAAA", hatch="///",
               edgecolor=C_OUT, lw=0.8, alpha=0.5, zorder=3):
    """Rectangle with built-in matplotlib hatch pattern.

    Uses matplotlib's native hatch parameter for reliable, clipped hatching.
    """
    ax.add_patch(mpatches.Rectangle(
        (x, y), w, h,
        facecolor=color, edgecolor=edgecolor,
        hatch=hatch, linewidth=lw, alpha=alpha, zorder=zorder))

# ── Notes block ────────────────────────────────────────────────────────────

def draw_notes(ax, notes, x, y_top, spacing, *, fs=7, title_fs=None,
               color=C_DIM, title_color=C_OUT, ha="left", pad_x=None,
               pad_y=None, width=None, border_color=C_OUT, border_lw=0.6,
               zorder=15, font=None):
    """Draw a bordered notes block with bold first line.

    Parameters
    ----------
    ax : matplotlib Axes
    notes : list[str]
        Lines of text. First line is rendered bold as the title.
    x, y_top : float
        Top-left anchor of the text block in axes data coordinates.
    spacing : float
        Vertical distance between lines in axes data units.
    fs : float
        Font size for body lines (default 7).
    title_fs : float or None
        Font size for the title line; defaults to *fs* + 0.5.
    color : str
        Body text color.
    title_color : str
        Title (first line) color.
    ha : str
        Horizontal alignment — 'left', 'center', or 'right'.
    pad_x : float or None
        Horizontal padding inside border (data units). Defaults to spacing.
    pad_y : float or None
        Vertical padding inside border (data units). Defaults to spacing * 0.5.
    width : float
        Border width in data units.  The border extends *width* data units
        from the text anchor in the reading direction (rightward on normal
        axes, leftward on mirrored axes).
    border_color : str
        Border rectangle edge color.
    border_lw : float
        Border line width.
    zorder : int
        Drawing layer.
    font : dict or None
        Extra font kwargs (e.g. ``{"fontfamily": "monospace"}``).
    """
    if title_fs is None:
        title_fs = fs + 0.5
    if pad_x is None:
        pad_x = spacing
    if pad_y is None:
        pad_y = spacing * 0.5
    if font is None:
        font = {}

    # Draw text lines in data coords
    for i, line in enumerate(notes):
        is_title = (i == 0)
        y = y_top - i * spacing
        ax.text(x, y, line, ha=ha, va="top",
                fontsize=title_fs if is_title else fs,
                color=title_color if is_title else color,
                fontweight="bold" if is_title else "normal",
                zorder=zorder + 1, **font)

    # Border rectangle in data coords
    if width is None:
        return  # no border when width not specified

    n = len(notes)
    box_top = y_top + pad_y
    box_bot = y_top - (n) * spacing - pad_y
    box_h = box_top - box_bot

    # Handle mirrored (inverted) X axis: width extends in reading direction
    x_inverted = ax.get_xlim()[0] > ax.get_xlim()[1]
    sign = -1 if x_inverted else 1

    if ha == "center":
        box_left_x = x - sign * (width / 2 + pad_x)
    elif ha == "right":
        box_left_x = x - sign * (width + pad_x)
    else:  # left
        box_left_x = x - sign * pad_x
    box_w = sign * (width + 2 * pad_x)

    rect = mpatches.FancyBboxPatch(
        (box_left_x, box_bot), box_w, box_h,
        boxstyle="square,pad=0", fc="white", ec=border_color,
        lw=border_lw, zorder=zorder)
    ax.add_patch(rect)


# ── Legend box ──────────────────────────────────────────────────────────────

def draw_legend(ax, items, x, y, *, row_h=46, swatch_w=32, swatch_h=28,
                pad=20, title="LEGEND", title_fs=7.5, fs=6, cols=1,
                col_w=None, font=None, zorder=14):
    """Draw a boxed legend with color swatches.

    Parameters
    ----------
    items : list of tuples
        Each item is (color, label) or (color, alpha, label) or
        (color, alpha, hatch, label).
    x, y : float
        Top-left corner of the legend box.
    """
    n = len(items)
    rows_per_col = (n + cols - 1) // cols
    if col_w is None:
        col_w = swatch_w + pad + 350
    box_w = cols * col_w + 2 * pad
    box_h = rows_per_col * row_h + 50
    fkw = dict(fontfamily="monospace") if font is None else font

    ax.add_patch(mpatches.Rectangle((x, y - box_h), box_w, box_h,
                                     fc="#FAFAFA", ec=C_DIM, lw=0.8,
                                     zorder=zorder))
    ax.text(x + box_w / 2, y - 16, title,
            color=C_OUT, fontsize=title_fs, ha="center", va="center",
            fontweight="bold", **fkw, zorder=zorder + 1)

    for i, item in enumerate(items):
        if len(item) == 2:
            color, label = item
            alpha, hatch = 1.0, None
        elif len(item) == 3:
            color, alpha, label = item
            hatch = None
        else:
            color, alpha, hatch, label = item

        c = i // rows_per_col
        r = i % rows_per_col
        ix = x + pad + c * col_w
        iy = y - 50 - r * row_h

        ax.add_patch(mpatches.Rectangle((ix, iy - swatch_h / 2), swatch_w,
                                         swatch_h, fc=color, ec=C_OUT,
                                         lw=0.8, alpha=alpha, hatch=hatch,
                                         zorder=zorder + 1))
        ax.text(ix + swatch_w + 10, iy, label, color=C_DIM, fontsize=fs,
                ha="left", va="center", **fkw, zorder=zorder + 1)


# ═════════════════════════════════════════════════════════════════════════
#  PIPE RUNS — canonical implementation (see skills/skill_plumbing_drawing.md)
#
#  Single source of truth for the parallel-wall pipe-run + elbow-fitting
#  geometry that was previously copy-pasted into ~6 generators.  Generators
#  keep a thin local wrapper that injects their own scale functions / default
#  colors and delegates here.  DO NOT re-inline this body into a generator.
# ═════════════════════════════════════════════════════════════════════════

def draw_pipe_path(ax, x_pts, z_pts, od_mm, wall_mm, fc="#B0B0B8", *,
                   ec="#333333", bore_fc="white", elbow_r=None, zorder=8,
                   lw=0.8, sx=None, sz=None):
    """Draw a pipe run with parallel-sided straight sections and elbow fittings.

    Pipes have constant OD with parallel walls.  Direction changes are drawn as
    discrete elbow fittings (concentric arcs), never as gradual curves.
    Supports 90 deg, 45 deg, and arbitrary-angle elbows.

    x_pts, z_pts : waypoint coordinates in mm (before scaling)
    od_mm        : pipe outer diameter in mm
    wall_mm      : pipe wall thickness in mm
    elbow_r      : elbow centerline bend radius in mm (default 1.0 x od_mm)
    sx, sz       : scale functions mm -> data coordinates (default identity)
    """
    _sx = sx if sx is not None else (lambda v: v)
    _sz = sz if sz is not None else (lambda v: v)
    n = len(x_pts)
    if n < 2:
        return
    half_od = od_mm / 2.0
    half_id = half_od - wall_mm
    if elbow_r is None:
        elbow_r = od_mm          # standard short-radius barb elbow

    # ── segment directions ──────────────────────────────────────────────
    segs = []
    for i in range(n - 1):
        dx = x_pts[i + 1] - x_pts[i]
        dz = z_pts[i + 1] - z_pts[i]
        length = max(math.hypot(dx, dz), 1e-6)
        segs.append((dx / length, dz / length, length))

    # ── elbow geometry at each intermediate waypoint ────────────────────
    elbows = []                  # one entry per interior waypoint
    for i in range(1, n - 1):
        d1x, d1z, _ = segs[i - 1]
        d2x, d2z, _ = segs[i]

        cos_a = max(-1.0, min(1.0, d1x * d2x + d1z * d2z))
        alpha = math.acos(cos_a)          # angle between direction vectors
        turn  = math.pi - alpha           # actual bend angle

        if turn < 0.01:                   # nearly straight — skip
            elbows.append(None)
            continue

        # clamp tangent so it never eats more than 40 % of either segment
        tangent = elbow_r * math.tan(turn / 2)
        max_t = 0.4 * min(segs[i - 1][2], segs[i][2])
        if tangent > max_t:
            tangent = max_t               # use a tighter bend radius

        cross = d1x * d2z - d1z * d2x     # +ve = left turn

        # normal toward arc center
        if cross > 0:
            nx_, nz_ = -d1z, d1x
        else:
            nx_, nz_ = d1z, -d1x

        # arc center from the incoming tangent point
        tp_x = x_pts[i] - d1x * tangent
        tp_z = z_pts[i] - d1z * tangent
        # radius may have been clamped — recompute from tangent
        r_eff = tangent / math.tan(turn / 2) if turn > 0.01 else elbow_r
        cx = tp_x + nx_ * r_eff
        cz_e = tp_z + nz_ * r_eff

        start_a = math.atan2(tp_z - cz_e, tp_x - cx)
        sweep   = turn if cross > 0 else -turn

        elbows.append({
            'tangent': tangent,
            'r': r_eff,
            'center': (cx, cz_e),
            'start': start_a,
            'sweep': sweep,
        })

    # ── helper: filled annular-ring rectangle (one straight section) ────
    def _rect(x0, z0, x1, z1, nx, nz, half_r, color, z_ord):
        pts = [(_sx(x0 + nx * half_r), _sz(z0 + nz * half_r)),
               (_sx(x1 + nx * half_r), _sz(z1 + nz * half_r)),
               (_sx(x1 - nx * half_r), _sz(z1 - nz * half_r)),
               (_sx(x0 - nx * half_r), _sz(z0 - nz * half_r))]
        ax.fill([p[0] for p in pts], [p[1] for p in pts],
                fc=color, ec=ec if color != bore_fc else "none",
                lw=lw if color != bore_fc else 0,
                zorder=z_ord)

    # ── draw straight sections (trimmed by tangent lengths) ─────────────
    for i in range(len(segs)):
        dx, dz, seg_len = segs[i]
        nx, nz = -dz, dx          # perpendicular

        trim_s = elbows[i - 1]['tangent'] if (i > 0 and elbows[i - 1]) else 0
        trim_e = elbows[i]['tangent']     if (i < len(elbows) and elbows[i]) else 0

        p0x = x_pts[i]     + dx * trim_s
        p0z = z_pts[i]     + dz * trim_s
        p1x = x_pts[i + 1] - dx * trim_e
        p1z = z_pts[i + 1] - dz * trim_e

        remaining = seg_len - trim_s - trim_e
        if remaining < 0.5:
            continue              # segment fully consumed by elbows

        _rect(p0x, p0z, p1x, p1z, nx, nz, half_od, fc, zorder)
        _rect(p0x, p0z, p1x, p1z, nx, nz, half_id, bore_fc, zorder + 1)

    # ── draw elbow fittings (concentric arcs) ───────────────────────────
    for elb in elbows:
        if elb is None:
            continue
        cx, cz_e = elb['center']
        r_eff  = elb['r']
        sa     = elb['start']
        sw     = elb['sweep']
        n_arc  = max(20, int(abs(sw) / 0.04))
        angles = [sa + sw * t / n_arc for t in range(n_arc + 1)]

        def _arc_ring(r_out, r_in, color, z_ord):
            ox = [_sx(cx + r_out * math.cos(a)) for a in angles]
            oz = [_sz(cz_e + r_out * math.sin(a)) for a in angles]
            ix = [_sx(cx + r_in  * math.cos(a)) for a in angles]
            iz = [_sz(cz_e + r_in  * math.sin(a)) for a in angles]
            ax.fill(ox + ix[::-1], oz + iz[::-1],
                    fc=color,
                    ec=ec if color != bore_fc else "none",
                    lw=lw if color != bore_fc else 0,
                    zorder=z_ord)

        _arc_ring(r_eff + half_od, max(r_eff - half_od, 0.5), fc,      zorder)
        _arc_ring(r_eff + half_id, max(r_eff - half_id, 0.5), bore_fc, zorder + 1)


def draw_pipe_end(ax, cx, cz, r_data, wall_data, fc="#B0B0B8", ec="#333333",
                  bore_fc="white", zorder=5):
    """Draw a pipe end-on at data coords (cx, cz) with radius r_data."""
    ax.add_patch(mpatches.Circle((cx, cz), r_data, fc=fc, ec=ec, lw=1.0,
                                 zorder=zorder))
    ax.add_patch(mpatches.Circle((cx, cz), r_data - wall_data,
                                 fc=bore_fc, ec="none", zorder=zorder + 1))
