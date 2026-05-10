#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
tbs_drawing.py — Shared drawing helpers for all TBS engineering diagrams.

Provides dimension lines, leader lines, center lines, circles, rectangles,
bolt hole patterns, and hatching.  All functions take an axes object as the
first argument and use keyword defaults matching the TBS palette in
tbs_constants.py.

Usage
-----
    from tbs_drawing import (draw_dim_h, draw_dim_v, leader, draw_cl,
                             draw_circle, draw_rect, bolt_holes, hatch_rect)
"""

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
           font=None, rotation=0):
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
    """
    kw = font or {}
    ax.annotate(label, xy=(x_tip, y_tip), xytext=(x_txt, y_txt),
                fontsize=fs, color=color, ha=ha, va=va, zorder=zorder,
                rotation=rotation,
                arrowprops=dict(arrowstyle=arrow_style, linestyle=":",
                                color=color, lw=lw,
                                connectionstyle="arc3,rad=0.0"),
                **kw)


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

def hatch_rect(ax, x, y, w, h, *, color="#AAAAAA", hatch="///",
               edgecolor=C_OUT, lw=0.8, alpha=0.5, zorder=3):
    """Rectangle with built-in matplotlib hatch pattern.

    Uses matplotlib's native hatch parameter for reliable, clipped hatching.
    """
    ax.add_patch(mpatches.Rectangle(
        (x, y), w, h,
        facecolor=color, edgecolor=edgecolor,
        hatch=hatch, linewidth=lw, alpha=alpha, zorder=zorder))


def hatch_lines(ax, patch, *, spacing=3, angle=45, color="#AAAAAA",
                lw=0.5):
    """Draw manual diagonal hatch lines clipped to an existing patch.

    Useful when finer control over line spacing and angle is needed
    than matplotlib's built-in hatch parameter provides.
    """
    px, py = patch.get_xy()
    pw = patch.get_width()
    ph = patch.get_height()
    angle_r = np.radians(angle)
    diag = np.sqrt(pw**2 + ph**2) + spacing
    n = int(diag / spacing) + 2
    cx_h, cy_h = px + pw / 2, py + ph / 2
    for i in range(-n, n + 1):
        off = i * spacing
        dx = diag * np.cos(angle_r)
        dy = diag * np.sin(angle_r)
        px0 = cx_h + off * np.cos(angle_r + np.pi / 2) - dx / 2
        py0 = cy_h + off * np.sin(angle_r + np.pi / 2) - dy / 2
        ax.plot([px0, px0 + dx], [py0, py0 + dy],
                color=color, lw=lw, clip_path=patch, clip_on=True)
