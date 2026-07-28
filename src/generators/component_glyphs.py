#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Component glyphs — front-elevation drawings of the ACTUAL selected parts.

So the panel diagrams read as manufacturing blueprints: each glyph matches its
real component (Powerwerx MC4 bulkhead, the weatherproof NEMA inlet, the Leviton
W5320 WR duplex under the 5981-UCL in-use cover, the Harfington 22mm mushroom),
not a generic box. Front-view renderings centred on (cx, cy); call from any
diagram generator. All dimensions are drawing units (the caller sets the scale)."""

import numpy as np
import matplotlib.patches as mpatches

C_OUT   = "#1A1A1A"
C_MC4   = "#2D7A2D"
C_AC    = "#A07820"
C_NEMA  = "#FFF0CC"
C_ESTOP = "#C42B1C"
C_RING  = "#F2C200"


def draw_mc4_bulkhead(ax, cx, cy, r=8, positive=True, z=6):
    """Powerwerx MC4 panel-mount bulkhead — hex panel nut + round MC4 face + polarity."""
    col  = C_MC4 if positive else "#606060"
    face = "#C0E8C0" if positive else "#E4E4E4"
    ang  = np.linspace(0, 2 * np.pi, 7) + np.pi / 6      # hex panel nut
    ax.add_patch(mpatches.Polygon(list(zip(cx + r * 1.35 * np.cos(ang),
                                            cy + r * 1.35 * np.sin(ang))),
                 closed=True, fc="#B8B8C0", ec=C_OUT, lw=1.0, zorder=z))
    ax.add_patch(mpatches.Circle((cx, cy), r, fc=face, ec=col, lw=1.4, zorder=z + 0.5))
    ax.text(cx, cy, "+" if positive else "−", ha="center", va="center",
            fontsize=8, fontweight="bold", color=col if positive else C_OUT, zorder=z + 1)


def draw_nema_inlet(ax, cx, cy, w=52, h=52, z=6):
    """NEMA 5-15 weatherproof power INLET (male) — flanged body, a spring flip-lid
    shown flipped OPEN on its hinge (gasketed underside), two flat blades + ground.
    The open sealing lid is what marks it weatherproof vs a bare inlet."""
    # flanged body (the part bolted to the panel)
    ax.add_patch(mpatches.FancyBboxPatch((cx - w / 2, cy - h / 2), w, h * 0.72,
                 boxstyle="round,pad=2,rounding_size=8", fc=C_NEMA, ec=C_AC, lw=1.6, zorder=z))
    # hinge knuckles along the top edge
    hy = cy - h / 2 + h * 0.72
    for hx in (cx - 8, cx, cx + 8):
        ax.add_patch(mpatches.Circle((hx, hy), 2.4, fc="#B8B090", ec=C_AC, lw=0.8, zorder=z + 0.5))
    # weatherproof flip-lid, flipped UP/open above the hinge; inner gasket ring
    lid_cy = hy + h * 0.20
    ax.add_patch(mpatches.FancyBboxPatch((cx - w * 0.40, lid_cy - h * 0.14), w * 0.80, h * 0.28,
                 boxstyle="round,pad=1,rounding_size=6", fc="#DAD2B2", ec=C_AC, lw=1.3, zorder=z + 0.3))
    ax.add_patch(mpatches.FancyBboxPatch((cx - w * 0.30, lid_cy - h * 0.09), w * 0.60, h * 0.18,
                 boxstyle="round,pad=1,rounding_size=4", fc="none", ec="#8A6A2A",
                 lw=0.9, ls=(0, (2, 1.5)), zorder=z + 0.4))          # gasket seal ring
    # face pins: two flat male blades + round ground pin
    for dx in (-7, 7):
        ax.add_patch(mpatches.Rectangle((cx + dx - 1.6, cy - h * 0.10), 3.2, 13,
                     fc="#909098", ec=C_OUT, lw=0.8, zorder=z + 0.6))
    ax.add_patch(mpatches.Circle((cx, cy - h * 0.20), 3.2, fc="#909098", ec=C_OUT, lw=0.8, zorder=z + 0.6))


def draw_wr_duplex_outlet(ax, cx, cy, w=40, h=58, z=6):
    """Leviton W5320 WR duplex receptacle under a 5981-UCL bubble in-use cover."""
    ax.add_patch(mpatches.FancyBboxPatch((cx - w / 2 - 6, cy - h / 2 - 6), w + 12, h + 12,
                 boxstyle="round,pad=2,rounding_size=12", fc="#EAF4FF", ec="#5A7A9A",
                 lw=1.4, alpha=0.6, zorder=z + 1.2))          # bubble in-use cover
    ax.add_patch(mpatches.FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                 boxstyle="round,pad=1,rounding_size=6", fc=C_NEMA, ec=C_AC, lw=1.4, zorder=z))
    for ry in (cy + h * 0.22, cy - h * 0.22):               # two receptacles (duplex)
        ax.add_patch(mpatches.Ellipse((cx, ry), w * 0.62, h * 0.30, fc="white",
                     ec=C_AC, lw=1.0, zorder=z + 0.4))
        for dx in (-5, 5):
            ax.add_patch(mpatches.Rectangle((cx + dx - 1.3, ry - 1), 2.6, 9,
                         fc="#333333", ec="none", zorder=z + 0.6))
        ax.add_patch(mpatches.Circle((cx, ry - 6), 2.2, fc="#333333", ec="none", zorder=z + 0.6))


def draw_estop_22mm(ax, cx, cy, r=20, z=6):
    """Harfington 22mm red mushroom E-stop on a safety-yellow bezel."""
    ax.add_patch(mpatches.Circle((cx, cy), r * 1.3, fc=C_RING, ec=C_OUT, lw=1.4, zorder=z))
    ax.add_patch(mpatches.Circle((cx, cy), r, fc=C_ESTOP, ec="#7A1810", lw=1.4, zorder=z + 0.4))
    ax.add_patch(mpatches.Circle((cx, cy), r * 0.55, fc="#D8382A", ec="none", zorder=z + 0.5))
    ax.text(cx, cy - r - 4, "STOP", ha="center", va="top", fontsize=6.5,
            fontweight="bold", color=C_ESTOP, zorder=z + 1)
