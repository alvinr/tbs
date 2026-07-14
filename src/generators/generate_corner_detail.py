#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""generate_corner_detail.py — film-plane CORNER mechanism detail (film-plane-redesign branch).

DRAFT sheet 3 for the redesigned film-plane corner: a slide-and-clamp stack carrying a single
off-the-shelf universal joint (no leadscrews/handwheels — a pinhole's infinite DoF makes this
scene control, not focus). Two views:

  A — Corner assembly elevation (side view, Yd × Z): the LOWER (floor) corner stack —
      depth rail + friction carriage → vertical (TILT) slide → horizontal (SWING) slide
      → cam clamps → single U-joint → film-frame corner.
  B — U-joint detail (enlarged): Ruland US12-6-6-SS, the two articulation axes + ±45° range.

Colour code (matches the 3D model): grey = depth rail (drive), red = carriages,
GREEN = vertical (tilt) slide, PURPLE = horizontal (swing) slide, dark = cam clamps.

Iteration draft — dims in mm.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

sys.path.insert(0, os.path.dirname(__file__))
from tbs_constants import DIAGRAMS_DIR
from tbs_drawing import (draw_dim_h, draw_dim_v, leader, draw_rect, draw_circle,
                         draw_notes, draw_cl_v, reset_label_registry)
from tbs_title_block import title_block

C_BG = "#FAFAFA"; OUT = "#1A1A1A"; DIM = "#404040"
C_STEEL = "#B0B0B8"; C_CAR = "#C04010"
C_TILT = "#2E8B57"    # vertical (tilt) slide — green
C_SWING = "#7B5EA7"   # horizontal (swing) slide — purple
C_UJ = "#C8D8E8"; C_PIN = "#B07010"; C_FRAME = "#8FB0C8"; C_PANEL = "#1F3B66"; C_CLAMP = "#3A3A40"
FONT = {"fontfamily": "monospace"}
LBL_BG = dict(fc="white", ec="none", alpha=0.85, pad=1)


def _rect(ax, x, y, w, h, fc, ec=OUT, lw=1.4, z=4, alpha=1.0):
    draw_rect(ax, x, y, w, h, fc=fc, color=ec, lw=lw, zorder=z)
    if alpha < 1.0:
        ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec="none", alpha=alpha, zorder=z - 1))


# ────────────────────────────────────────────────────────────────────────────
def view_a(ax):
    """Corner assembly elevation — LOWER (floor) corner. Yd (horizontal) × Z (vertical), mm.
    Shown at the NOMINAL (flat) pose: the vertical carriage sits LOW, the green rail towers
    above it as the ~280 mm tilt-travel headroom."""
    ax.set_xlim(-60, 500); ax.set_ylim(-60, 400); ax.set_aspect("equal"); ax.axis("off")

    ax.plot([-30, 460], [0, 0], color="#999", lw=0.8, zorder=1)   # floor line

    # depth slide rail (Y, drive) — LOWER/floor rail, shown partial with break marks
    _rect(ax, 30, 0, 430, 18, C_STEEL)
    for bx in (44, 446):
        ax.plot([bx - 6, bx + 6], [-4, 22], color=OUT, lw=0.8, zorder=6)
    # depth friction carriage — captive block; in this side view its near face hooks squarely
    # over the rail edge (down to ~mid-rail), so it reads as gripping, not passing through
    _rect(ax, 226, 4, 96, 40, C_CAR, z=6)
    ax.plot([226, 322], [10, 10], color="#7A2408", lw=0.7, zorder=7)   # hook line under the rail edge
    ax.plot([250, 250], [46, 60], color=OUT, lw=0.6, zorder=8)          # section cut A-A marker
    ax.plot([250, 250], [-14, 4], color=OUT, lw=0.6, zorder=8)
    ax.text(250, 64, "A", fontsize=6.5, ha="center", va="bottom", color=OUT, **FONT)
    ax.text(250, -20, "A", fontsize=6.5, ha="center", va="top", color=OUT, **FONT)
    _rect(ax, 322, 16, 14, 20, C_CLAMP, z=8)                             # depth cam clamp
    ax.plot([336, 360], [30, 22], color=C_CLAMP, lw=2.0, zorder=8)

    # vertical (TILT) slide rail — green; low carriage at nominal, rail = ~280 mm tilt headroom
    _rect(ax, 236, 40, 18, 280, C_TILT)                 # tall rail (travel envelope)
    _rect(ax, 228, 48, 34, 52, C_TILT)                  # vertical friction carriage (LOW = nominal)
    _rect(ax, 262, 60, 14, 20, C_CLAMP)                 # cam clamp body
    ax.plot([276, 306], [70, 62], color=C_CLAMP, lw=2.2, zorder=6)   # clamp lever
    _rect(ax, 262, 86, 44, 12, C_UJ)                    # bracket carriage → corner stack

    # horizontal (SWING) slide — purple, runs into the page (X); shown edge-on
    _rect(ax, 292, 98, 48, 16, C_SWING)

    # single U-joint (Ruland US12-6-6-SS)
    _rect(ax, 300, 114, 32, 30, C_UJ)
    draw_circle(ax, 316, 129, 5.5, color=C_PIN, fill=True, fc=C_PIN, lw=1.0, zorder=6)
    ax.plot([316, 316], [110, 148], color=C_PIN, lw=1.6, zorder=5)

    # film-frame corner (2x2 Al angle) + film plane edge (ghost)
    _rect(ax, 308, 144, 44, 8, C_FRAME)                 # horizontal leg
    _rect(ax, 308, 144, 8, 214, C_FRAME)               # vertical leg
    ax.add_patch(plt.Rectangle((320, 152), 6, 202, fc=C_PANEL, ec="none", alpha=0.16, zorder=2))

    # ── dimensions (both on the left, near the green rail) ──
    draw_dim_v(ax, 8, 18, 144, "~150mm\nnominal\nstack", offset=28, fs=6, color=DIM, font=FONT)
    draw_dim_v(ax, 206, 40, 320, "~280mm\ntilt travel", offset=26, fs=6, color=DIM, font=FONT)

    # ── leaders (green up, drive below, mechanism stacked right) ──
    leader(ax, 90, 9, 40, -44, "DEPTH slide rail (Y) — the DRIVE; ~2.2 m; floor (LOWER) rail",
           ha="left", fs=6.2, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 300, 22, 330, -36, "depth carriage (captive on rail)",
           ha="left", fs=6.2, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 245, 300, 250, 344, "VERTICAL slide (Z, green)\n— TILT accommodation",
           ha="left", fs=6.2, color=C_TILT, font=FONT, bbox=LBL_BG)
    leader(ax, 306, 62, 352, 48, "cam clamp — one per slide\n(push → lock)",
           ha="left", fs=6.2, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 316, 106, 356, 98, "HORIZONTAL slide (X, purple)\n— SWING accom. (into page)",
           ha="left", fs=6.2, color=C_SWING, font=FONT, bbox=LBL_BG)
    leader(ax, 332, 129, 372, 150, "single U-joint\n(Ruland US12-6-6-SS)",
           ha="left", fs=6.2, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 318, 300, 352, 322, "film-frame corner\n(2x2 Al angle) + film",
           ha="left", fs=6.2, color=OUT, font=FONT, bbox=LBL_BG)

    ax.text(-58, 392, "A — CORNER ASSEMBLY ELEVATION  (lower / floor corner; Yd × Z; nominal pose)",
            fontsize=8, fontweight="bold", color=OUT, ha="left", va="top", **FONT)


# ────────────────────────────────────────────────────────────────────────────
def view_b(ax):
    """U-joint detail (enlarged ~2:1). Ruland US12-6-6-SS; through-axis horizontal."""
    ax.set_xlim(0, 200); ax.set_ylim(-10, 150); ax.set_aspect("equal"); ax.axis("off")
    cy = 70
    # through-axis centre line
    ax.plot([8, 192], [cy, cy], color="#2060A0", lw=0.6, dashes=(8, 3, 2, 3), zorder=2)

    # input shaft stub + hub (carrier side, left)
    _rect(ax, 10, cy - 9, 26, 18, C_STEEL)
    # input yoke — two ears (top + bottom) opening right, holding the vertical (SWING) pin
    _rect(ax, 40, cy + 14, 40, 16, C_UJ); _rect(ax, 40, cy - 30, 40, 16, C_UJ)
    ax.plot([70, 70], [cy - 34, cy + 34], color=C_PIN, lw=2.4, zorder=6)          # swing pin (vertical)
    draw_circle(ax, 70, cy + 22, 4, color=C_PIN, fill=True, fc=C_PIN, lw=0.8, zorder=7)
    draw_circle(ax, 70, cy - 22, 4, color=C_PIN, fill=True, fc=C_PIN, lw=0.8, zorder=7)
    # cross / spider block
    _rect(ax, 62, cy - 14, 30, 28, "#9AA0A8")
    # output yoke — ears opening left (perpendicular, into page → ghost), holding the tilt pin
    _rect(ax, 84, cy + 12, 40, 14, C_UJ, ec="#7A8290", lw=1.0)
    _rect(ax, 84, cy - 26, 40, 14, C_UJ, ec="#7A8290", lw=1.0)
    draw_circle(ax, 90, cy, 5, color=C_PIN, fill=True, fc=C_PIN, lw=0.8, zorder=7)  # tilt pin (into page)
    # output shaft stub (frame side, right)
    _rect(ax, 128, cy - 9, 26, 18, C_STEEL)

    # ±45° articulation arc on the through-axis (schematic)
    ax.add_patch(Arc((70, cy), 150, 150, angle=0, theta1=-45, theta2=45, color=DIM, lw=0.9, zorder=5))
    for ang in (45, -45):
        import math
        ex = 70 + 75 * math.cos(math.radians(ang)); ey = cy + 75 * math.sin(math.radians(ang))
        ax.plot([70, ex], [cy, ey], color=DIM, lw=0.5, dashes=(4, 3), zorder=4)
    ax.text(150, cy + 40, "±45°\nmax swivel", fontsize=6, color=DIM, ha="left", va="center", **FONT)

    # dims
    draw_dim_h(ax, 10, 154, cy - 44, "68mm overall", offset=12, fs=6, color=DIM, above=False, font=FONT)
    draw_dim_v(ax, 176, cy - 9, cy + 9, "19mm OD", offset=13, fs=6, color=DIM, right=True,
               perpendicular=True, font=FONT)

    # callouts
    leader(ax, 70, cy + 30, 30, cy + 46, "SWING axis (vertical pin)", ha="left", fs=6, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 90, cy, 120, cy + 30, "TILT axis (perpendicular pin, into page)", ha="left", fs=6, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 23, cy - 9, 20, cy - 30, "to carrier / cross-slide", ha="left", fs=6, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 141, cy + 9, 120, cy - 30, "to film-frame corner", ha="left", fs=6, color=OUT, font=FONT, bbox=LBL_BG)

    ax.text(0, 146, "B — U-JOINT DETAIL  (Ruland US12-6-6-SS, enlarged)",
            fontsize=8, fontweight="bold", color=OUT, ha="left", va="top", **FONT)


# ────────────────────────────────────────────────────────────────────────────
def section_aa(ax):
    """SECTION A-A — X-Z cut through a depth rail + friction carriage, showing the captive wrap."""
    ax.set_xlim(-14, 74); ax.set_ylim(-16, 46); ax.set_aspect("equal"); ax.axis("off")
    # profile rail (grey): base + rib with a groove on each flank
    _rect(ax, 12, 0, 36, 8, C_STEEL)                    # wide base
    _rect(ax, 18, 8, 24, 15, C_STEEL)                   # rib
    ax.add_patch(plt.Rectangle((15, 10), 4, 5, fc="white", ec=OUT, lw=0.7, zorder=6))   # L groove
    ax.add_patch(plt.Rectangle((41, 10), 4, 5, fc="white", ec=OUT, lw=0.7, zorder=6))   # R groove
    # carriage (red) C-profile wrapping the rail; retention lugs reach into the grooves = captive
    _rect(ax, 6, 23, 48, 10, C_CAR, z=5)                # top web
    _rect(ax, 6, 6, 9, 17, C_CAR, z=5)                  # left wall
    _rect(ax, 45, 6, 9, 17, C_CAR, z=5)                 # right wall
    _rect(ax, 13, 10, 6, 5, C_CAR, z=7)                 # left retention lug (into groove)
    _rect(ax, 41, 10, 6, 5, C_CAR, z=7)                 # right retention lug
    leader(ax, 16, 12, -14, -6, "retention lug in rail groove\n= captive (can't lift off)",
           ha="left", fs=5.6, color=OUT, font=FONT, bbox=LBL_BG)
    ax.text(-14, 44, "SECTION A-A  (X × Z) — captive carriage wraps the rail",
            fontsize=7.5, fontweight="bold", color=OUT, ha="left", va="top", **FONT)


def view_c(ax):
    """C — SWING slide face-on (X, at the corner): the horizontal slide + carriage + cam clamp."""
    ax.set_xlim(-50, 330); ax.set_ylim(-70, 90); ax.set_aspect("equal"); ax.axis("off")
    # horizontal (swing) slide rail — runs in X, ~260 mm travel
    _rect(ax, 0, 20, 280, 12, "#B7A6D0")                # rail (light purple)
    for bx in ():
        pass
    # carriage at the OUTBOARD end (neutral); shifts toward panel centre as the plane swings
    _rect(ax, 4, 12, 52, 28, C_SWING)                   # swing friction carriage
    _rect(ax, 60, 18, 12, 16, C_CLAMP)                  # cam clamp
    ax.plot([72, 96], [26, 20], color=C_CLAMP, lw=2.0, zorder=6)
    _rect(ax, 16, 40, 28, 16, C_UJ)                     # U-joint mount on the carriage
    # motion arrow (toward centre)
    ax.annotate("", xy=(150, 50), xytext=(70, 50),
                arrowprops=dict(arrowstyle="->", color=DIM, lw=1.0), zorder=6)
    ax.text(150, 58, "shifts toward panel centre\nas the plane SWINGS", fontsize=6, color=DIM,
            ha="left", va="bottom", **FONT)
    draw_dim_h(ax, 0, 280, -20, "~260mm swing travel", offset=14, fs=6, color=DIM, above=False, font=FONT)
    leader(ax, 30, 26, -46, -2, "swing friction carriage\n(neutral = outboard)", ha="left", fs=6,
           color=C_SWING, font=FONT, bbox=LBL_BG)
    leader(ax, 30, 48, -20, 74, "U-joint mounts here", ha="left", fs=6, color=OUT, font=FONT, bbox=LBL_BG)
    leader(ax, 66, 20, 96, 12, "cam clamp", ha="left", fs=6, color=OUT, font=FONT, bbox=LBL_BG)
    ax.text(-50, 86, "C — SWING SLIDE  (face-on; horizontal X slide at the corner)",
            fontsize=8, fontweight="bold", color=OUT, ha="left", va="top", **FONT)


# ────────────────────────────────────────────────────────────────────────────
def draw_sheet():
    reset_label_registry()
    fig = plt.figure(figsize=(18, 13))
    fig.patch.set_facecolor(C_BG)

    ax_a = fig.add_axes([0.03, 0.42, 0.45, 0.55]); ax_a.set_facecolor(C_BG)
    ax_b = fig.add_axes([0.52, 0.68, 0.45, 0.29]); ax_b.set_facecolor(C_BG)
    ax_sec = fig.add_axes([0.52, 0.45, 0.24, 0.20]); ax_sec.set_facecolor(C_BG)
    ax_c = fig.add_axes([0.03, 0.10, 0.45, 0.28]); ax_c.set_facecolor(C_BG)
    view_a(ax_a)
    view_b(ax_b)
    section_aa(ax_sec)
    view_c(ax_c)

    # notes block
    ax_n = fig.add_axes([0.52, 0.09, 0.45, 0.32]); ax_n.set_xlim(0, 100); ax_n.set_ylim(0, 100)
    ax_n.axis("off")
    draw_notes(ax_n, [
        "CORNER MECHANISM — ONE OF FOUR:",
        "1. A pinhole has infinite depth of field, so the plane is positioned for scene control "
        "(tilt / swing / rise), not focus — hence slide-and-clamp, not leadscrews.",
        "2. Three friction slides per corner: DEPTH (Y) is the drive (a top-bottom depth "
        "difference = tilt, left-right = swing); VERTICAL (Z, green) absorbs the tilt "
        "foreshortening (~280mm); HORIZONTAL (X, purple) absorbs the swing foreshortening (~260mm).",
        "3. Push each slide into position; the adjustable-friction slide holds it, then throw the "
        "cam clamp to lock for the shot and for transport.",
        "4. The U-joint (Ruland US12-6-6-SS, 303 SS, self-lube sintered-bronze, grease-free) gives "
        "tilt + swing and locks twist so the flat plane stays square. Upper (ceiling) corners hang "
        "in tension; lower (floor) corners bear in compression — the captive carriages take both.",
    ], 2, 96, 6.2, fs=7, title_fs=7.5, color=DIM, width=96, wrap=64, font=FONT)

    ax_tb = fig.add_axes([0.03, 0.008, 0.94, 0.06])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, "SHEET 3 OF 6  (DRAFT)",
                drawing_title="FILM-PLANE CORNER MECHANISM",
                subtitle="SLIDE-AND-CLAMP + SINGLE U-JOINT — CORNER DETAIL",
                scale_note="DRAFT (film-plane-redesign) — DIMS IN mm")

    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    png = os.path.join(DIAGRAMS_DIR, "film-corner-detail.png")
    fig.savefig(png, dpi=150, bbox_inches="tight", facecolor=C_BG)
    plt.close(fig)
    print(f"  {png} saved")


if __name__ == "__main__":
    draw_sheet()
