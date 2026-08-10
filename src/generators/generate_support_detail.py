#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""generate_support_detail.py — pump-run support-board fabrication detail (#29).

The corridor pump risers, drain-riser spine, and filter-skid runs land on three flush
18mm-ply support boards, each recessed in a post window on welded steel L-brackets and
clamped with cushioned P-clips.  The panel-layout elevation shows the boards EDGE-ON only;
this is the dedicated fabrication sheet a shop builds from:

    Sheet 1  BOARD ELEVATIONS   — far / near / near-upper boards, face-on, fully dimensioned
    Sheet 2  MOUNTING DETAILS   — L-bracket flush-mount section + P-clip detail + schedule

Geometry is imported from generate_corridor_water_panel (the model's SB_* constants) so the
drawing tracks the 3D model and cannot drift.
"""
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models"))

from tbs_constants import DIAGRAMS_DIR
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_notes
from tbs_title_block import title_block
import generate_corridor_water_panel as cp

TOTAL_SHEETS = 2
C_BG = "#FAFAFA"
FONT = {"fontfamily": "monospace"}

# palette
C_OUT = "#1A1A1A"
C_DIM = "#404040"
C_STEEL = "#8A8C94"
C_STEEL_D = "#6C6E76"
C_PLY = "#D8B78A"
C_PLY_E = "#A9843F"
C_BLUE = "#2979B8"
C_BROWN = "#8B5E3C"
C_GREY = "#6E7076"
C_CLIP = "#55575E"
C_CUSH = "#2E2E34"
LBL_BG = dict(fc="white", ec="none", alpha=0.85, pad=1)

# ── geometry pulled from the model (no drift) ──────────────────────────────────
X0, X1 = cp.SB_X0, cp.SB_X1                 # board X window (post inner faces): 4704.8 → 5104
BW = X1 - X0                                # 399.2mm board width
EQT = cp.EQT                               # 18mm ply
S = cp.S                                   # 50.8mm post (2×2×0.120 RHS)
RP = cp.RP                                 # 10.5mm  (Ø21 riser)
YD_NEAR, YD_FAR = cp.YD_NEAR, cp.YD_FAR    # 1046 / 1316 corridor side walls
LT, LL, LH = 6, 45, 50                     # bracket leg thickness / landing-leg length / bracket height

# board face-on specs: (title, subtitle, (z0,z1), risers[(x,label,color)], clamp_zs, horizontals[(z,label,color)])
BOARDS = [
    ("FAR BOARD", "film-plane wall (Yd 1298–1316)", cp.SB_FAR_Z,
     [(4873, "DV-01 recycle", C_BROWN), (4900, "P-02 discharge", C_BROWN), (4984, "P-01→ACC-01", C_BLUE)],
     cp.SB_FAR_CLAMP_Z, []),
    ("NEAR BOARD", "walkway wall (Yd 1046–1064)", cp.SB_NEAR_Z,
     [(4825, "P-02 suction", C_BROWN), (5070, "P-05 inlet", C_BROWN)],
     cp.SB_NEAR_CLAMP_Z, []),
    ("NEAR-UPPER BOARD", "walkway wall — backs BV-02 / BV-06", cp.SB_NEAR_UP_Z,
     [(cp.BV_FWD_X, "BV-02 / BV-06 risers", C_BROWN)],
     (1370, 1440, 1770, 1840),
     [(1300, "P-05-inlet brown", C_BROWN), (1902, "P-03 grey", C_GREY)]),
]


def _save(fig, filename):
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    png = os.path.join(DIAGRAMS_DIR, filename)
    fig.savefig(png, dpi=150, bbox_inches="tight", facecolor=C_BG)
    plt.close(fig)
    print(f"  {png} saved")


def _rect(ax, x, y, w, h, fc, ec=C_OUT, lw=1.4, z=3, hatch=None):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z, hatch=hatch))


# ─────────────────────────────────────────────────────────────────────────────
def draw_board(ax, spec):
    """One board, face-on (X across, Z up): ply + 4 L-brackets + risers + P-clips, dimensioned."""
    title, subtitle, (z0, z1), risers, clamp_zs, horizontals = spec
    h = z1 - z0
    mx, mz = 120, 95
    ax.set_xlim(X0 - mx, X1 + mx)
    ax.set_ylim(z0 - mz, z1 + mz + 120)
    ax.set_aspect("equal")
    ax.axis("off")

    # ply board
    _rect(ax, X0, z0, BW, h, C_PLY, ec=C_PLY_E, lw=1.6, z=2)
    cx = (X0 + X1) / 2
    if not any(abs(r[0] - cx) < 60 for r in risers):   # skip the center label if a riser sits on it
        ax.text(cx, z0 + h / 2, "18mm ply", ha="center", va="center",
                fontsize=7, color="#5C4A28", zorder=4, **FONT)

    # 4 L-brackets (steel tabs) at the post inner faces, top & bottom
    for bx in (X0, X1):
        for bz in (z0 + 35, z1 - 35):
            tab_x = bx if bx == X0 else bx - 34
            _rect(ax, tab_x, bz - LH / 2, 34, LH, C_STEEL, ec=C_STEEL_D, lw=1.2, z=5)

    # risers (vertical pipes) + P-clips at each clamp row
    n = len(risers)
    for i, (rx, rlabel, rc) in enumerate(risers):
        ax.add_patch(Rectangle((rx - RP, z0 - 8), 2 * RP, h + 16, facecolor=rc,
                               edgecolor=C_OUT, linewidth=0.9, zorder=6, alpha=0.92))
        for cz in clamp_zs:
            _rect(ax, rx - RP - 5, cz - 8, 2 * RP + 10, 16, C_CLIP, ec=C_OUT, lw=0.8, z=8)
        # fan the labels across the top (spread X + alternate tier) so close risers don't collide
        tx = X0 + (i + 0.5) * BW / n
        ty = z1 + (72 if i % 2 == 0 else 112)
        leader(ax, rx, z1 + 6, tx, ty, rlabel, fs=6.2, color=rc,
               ha="center", va="bottom", font=FONT, bbox=LBL_BG)

    # horizontal runs on the near-upper board
    for hz, hlabel, hc in horizontals:
        ax.add_patch(Rectangle((X0 + 20, hz - RP), BW - 40, 2 * RP, facecolor=hc,
                               edgecolor=C_OUT, linewidth=0.9, zorder=6, alpha=0.92))
        leader(ax, X0 + 40, hz, X0 - 30, hz, hlabel, fs=6.0, color=hc,
               ha="right", va="center", font=FONT, bbox=LBL_BG)

    # dimensions
    draw_dim_h(ax, X0, X1, z1 + 40, f"{BW:.0f}mm", offset=15, fs=6.6, above=True, font=FONT)
    draw_dim_v(ax, X0 - 62, z0, z1, f"{h:.0f}mm", offset=16, fs=6.6, right=False, font=FONT)
    # clamp-row Z dimension (first riser)
    if clamp_zs and risers:
        cz_lo, cz_hi = min(clamp_zs), max(clamp_zs)
        if cz_hi != cz_lo:
            draw_dim_v(ax, X1 + 40, cz_lo, cz_hi, f"{cz_hi - cz_lo:.0f}mm", offset=16, fs=6.2, right=True, font=FONT)

    ax.text((X0 + X1) / 2, z0 - mz - 42, title, ha="center", va="top",
            fontsize=9.5, fontweight="bold", color=C_OUT, zorder=10, **FONT)
    ax.text((X0 + X1) / 2, z0 - mz - 78, subtitle, ha="center", va="top",
            fontsize=6.8, color=C_DIM, zorder=10, **FONT)


def draw_sheet1():
    fig = plt.figure(figsize=(20, 13))
    fig.patch.set_facecolor(C_BG)
    # three panels, bottom-aligned; near-upper is taller so its axes box is taller
    boxes = [(0.045, 0.20, 0.27, 0.52),
             (0.365, 0.20, 0.27, 0.52),
             (0.685, 0.20, 0.27, 0.72)]
    for spec, box in zip(BOARDS, boxes):
        ax = fig.add_axes(box)
        ax.set_facecolor(C_BG)
        draw_board(ax, spec)

    # header
    fig.text(0.5, 0.955, "PUMP-RUN SUPPORT BOARDS — BOARD ELEVATIONS", ha="center",
             fontsize=15, fontweight="bold", color=C_OUT, **FONT)
    fig.text(0.5, 0.925, "Face-on (looking at the corridor side wall) · each board 18mm ply · X–Z · all dims in mm",
             ha="center", fontsize=8.5, color=C_DIM, **FONT)

    ax_n = fig.add_axes([0.045, 0.075, 0.62, 0.09]); ax_n.axis("off")
    draw_notes(ax_n, [
        "NOTES:",
        "1. Board = 18mm exterior BC/ACX plywood, cut 399mm wide to fill the post window (X4705–5104); back face flush with the post wall-side face.",
        "2. Each board carried on 4 welded steel L-brackets (one per post inner face, top + bottom) — see Sheet 2.",
        "3. Risers clamped with cushioned 3/4\" P-clips at the marked rows (2 per riser; the near-upper board takes 4).",
        "4. Steel tab = L-bracket landing leg (face-on); brackets set 35mm in from each board edge.",
    ], 0.0, 1.0, 0.15, fs=7.2, title_fs=7.6, width=1.0, wrap=120, font=FONT)

    ax_tb = fig.add_axes([0.04, 0.008, 0.92, 0.045])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 1 OF {TOTAL_SHEETS}",
                drawing_title="PUMP-RUN SUPPORT DETAIL",
                subtitle="BOARD ELEVATIONS (far / near / near-upper)",
                doc_id="TBS-001 · IBC Plumbing Corridor · #29",
                scale_note="EACH PANEL TO SCALE — ALL DIMS IN mm")
    _save(fig, "support-detail-sheet1.png")


# ─────────────────────────────────────────────────────────────────────────────
def draw_flush_section(ax):
    """L-bracket flush-mount PLAN SECTION (X–Yd, looking down) at one bracket — near-wall corner.

    Shows: post square → weld leg on the post inner X-face → landing leg → 18mm ply seated
    flush with the post wall-side face, with the through-bolt into a back-face tee-nut."""
    # near wall: post inner face (corridor side) at X0; post spans X4654-4704.8 in X, Yd 1046-1096.8.
    # ply back face flush at YD_NEAR (1046); ply corridor face at 1064.
    px1 = X0                    # front-post inner X-face (corridor side of the window)
    px0 = X0 - S                # front-post outer X-face
    yd_back = YD_NEAR           # ply back / post wall-side face
    yd_face = YD_NEAR + EQT     # ply corridor face
    yd_post_far = YD_NEAR + S   # post far Yd face

    ax.set_xlim(px0 - 60, X0 + 180)
    ax.set_ylim(yd_back - 70, yd_post_far + 55)
    ax.set_aspect("equal")
    ax.axis("off")

    # post (50.8 square, section — hatched steel)
    _rect(ax, px0, yd_back, S, S, C_STEEL, ec=C_OUT, lw=1.6, z=3, hatch="////")
    ax.text(px0 + S / 2, yd_back + S / 2, "post\n50.8", ha="center", va="center",
            fontsize=6.4, color="#2A2A2A", zorder=6, **FONT)

    # ply board (18mm), sits in the window (X ≥ X0), back face flush at yd_back
    _rect(ax, px1, yd_back, 150, EQT, C_PLY, ec=C_PLY_E, lw=1.6, z=3)
    ax.text(px1 + 92, yd_back + EQT / 2, "18mm ply", ha="center", va="center",
            fontsize=6.6, color="#5C4A28", zorder=6, **FONT)

    # L-bracket: weld leg (6mm) on the post inner X-face, spanning the ply depth in Yd
    _rect(ax, px1, yd_back, LT, EQT, C_STEEL_D, ec=C_OUT, lw=1.2, z=5)
    # landing leg (45mm long in X, 6mm thick in Yd) behind the ply back face
    _rect(ax, px1, yd_back - LT, LL, LT, C_STEEL_D, ec=C_OUT, lw=1.2, z=5)

    # through-bolt: ply → landing leg into a back-face tee-nut
    bx = px1 + 26
    ax.plot([bx, bx], [yd_back + EQT, yd_back - LT - 8], color=C_CUSH, lw=2.4, zorder=8)
    ax.add_patch(Rectangle((bx - 7, yd_back - LT - 14), 14, 8, facecolor=C_CUSH, edgecolor=C_OUT, lw=0.8, zorder=8))

    # weld symbol at the post/weld-leg join
    ax.plot([px1, px1], [yd_back, yd_back + EQT], color=C_BLUE, lw=3.0, zorder=9, solid_capstyle="round")

    # callouts
    leader(ax, px1 + 3, yd_back + EQT - 3, X0 + 120, yd_post_far + 20,
           "weld leg 6mm\n(fillet-welded to post face)", fs=6.0, color=C_OUT, ha="left", va="center", font=FONT, bbox=LBL_BG)
    leader(ax, px1 + LL - 4, yd_back - LT + 3, X0 + 120, yd_back - 40,
           f"landing leg {LL}mm\n(ply bolts here)", fs=6.0, color=C_OUT, ha="left", va="top", font=FONT, bbox=LBL_BG)
    leader(ax, bx, yd_back - LT - 10, px0 - 10, yd_back - 30,
           "M6 machine screw\n→ back-face tee-nut", fs=6.0, color=C_CUSH, ha="right", va="center", font=FONT, bbox=LBL_BG)
    leader(ax, X0, yd_back, px0 - 10, yd_post_far + 20,
           "ply back face FLUSH\nwith post wall-side face", fs=6.0, color=C_PLY_E, ha="right", va="center", font=FONT, bbox=LBL_BG)

    draw_dim_v(ax, X0 + 165, yd_back, yd_face, f"{EQT}mm", offset=13, fs=6.2, right=True, font=FONT)
    draw_dim_h(ax, px1, px1 + LL, yd_back - LT - 30, f"{LL}mm", offset=12, fs=6.2, above=False, font=FONT)
    ax.text((px0 + X0 + 120) / 2, yd_post_far + 46, "L-BRACKET FLUSH-MOUNT — PLAN SECTION (near wall; far wall mirrored)",
            ha="center", va="bottom", fontsize=8, fontweight="bold", color=C_OUT, **FONT)


def draw_pclip(ax):
    """P-clip cross-section: cushioned clip around the Ø21 riser, bolted to the ply."""
    ax.set_xlim(-70, 95)
    ax.set_ylim(-55, 60)
    ax.set_aspect("equal")
    ax.axis("off")

    # ply slab (edge-on) at left
    _rect(ax, -60, -45, 22, 100, C_PLY, ec=C_PLY_E, lw=1.4, z=2)
    ax.text(-49, 48, "ply", ha="center", va="top", fontsize=6.0, color="#5C4A28", zorder=4, **FONT)

    # riser pipe Ø21 with cushion ring
    ax.add_patch(Circle((18, 5), RP + 3.5, facecolor=C_CUSH, edgecolor="none", zorder=3))   # cushion
    ax.add_patch(Circle((18, 5), RP, facecolor=C_BROWN, edgecolor=C_OUT, lw=1.2, zorder=4))  # pipe

    # P-clip band wrapping the cushion, foot to the ply
    ax.add_patch(Arc((18, 5), 2 * (RP + 6), 2 * (RP + 6), angle=0, theta1=-150, theta2=150,
                     lw=3.0, edgecolor=C_CLIP, zorder=5))
    ax.plot([-38, 3], [-8, -2], color=C_CLIP, lw=3.0, zorder=5)   # foot to ply

    # fastener into the ply
    ax.plot([-52, -20], [-8, -8], color=C_CUSH, lw=2.2, zorder=6)
    ax.add_patch(Rectangle((-62, -12), 6, 8, facecolor=C_CUSH, edgecolor=C_OUT, lw=0.7, zorder=6))

    leader(ax, 18, 5, 70, 40, "Ø21 riser", fs=6.2, color=C_BROWN, ha="left", va="center", font=FONT, bbox=LBL_BG)
    leader(ax, 18 + RP + 3, 5, 70, 12, "EPDM cushion", fs=6.2, color=C_CUSH, ha="left", va="center", font=FONT, bbox=LBL_BG)
    leader(ax, 18, 5 + RP + 6, 70, -18, '3/4" P-clip', fs=6.2, color=C_CLIP, ha="left", va="center", font=FONT, bbox=LBL_BG)
    leader(ax, -56, -8, -30, -42, "machine screw\n→ tee-nut", fs=6.0, color=C_CUSH, ha="center", va="top", font=FONT, bbox=LBL_BG)
    ax.text(15, 55, "P-CLIP DETAIL", ha="center", va="bottom", fontsize=8, fontweight="bold", color=C_OUT, **FONT)


def draw_sheet2():
    fig = plt.figure(figsize=(20, 13))
    fig.patch.set_facecolor(C_BG)

    fig.text(0.5, 0.955, "PUMP-RUN SUPPORT BOARDS — MOUNTING DETAILS", ha="center",
             fontsize=15, fontweight="bold", color=C_OUT, **FONT)
    fig.text(0.5, 0.925, "Flush-mount L-bracket section · P-clip detail · fabrication schedule · all dims in mm",
             ha="center", fontsize=8.5, color=C_DIM, **FONT)

    ax_sec = fig.add_axes([0.05, 0.42, 0.46, 0.46]); ax_sec.set_facecolor(C_BG)
    draw_flush_section(ax_sec)

    ax_clip = fig.add_axes([0.60, 0.50, 0.34, 0.38]); ax_clip.set_facecolor(C_BG)
    draw_pclip(ax_clip)

    # schedule table
    ax_t = fig.add_axes([0.05, 0.10, 0.52, 0.24]); ax_t.axis("off")
    ax_t.set_xlim(0, 1); ax_t.set_ylim(0, 1)
    rows = [
        ("ITEM", "QTY", "SIZE / MATERIAL"),
        ("Support board", "3", "18mm exterior BC/ACX ply, 399mm × (420 / 420 / 690)mm"),
        ("L-bracket", "12", "6mm steel angle, 45mm landing leg × 50mm tall (4 per board)"),
        ("P-clip (cushioned)", "39", '3/4" cushioned pipe clip, EPDM-lined'),
        ("Machine screw + tee-nut", "—", "M6 into back-face 4-prong tee-nut (per clip + bracket)"),
    ]
    y = 0.92
    ax_t.text(0.0, 1.0, "FABRICATION SCHEDULE", fontsize=8.6, fontweight="bold", color=C_OUT, **FONT)
    cols = (0.0, 0.34, 0.44)
    for i, (a, b, c) in enumerate(rows):
        yy = y - i * 0.155
        fw = "bold" if i == 0 else "normal"
        ax_t.text(cols[0], yy, a, fontsize=7.2, fontweight=fw, color=C_OUT, va="top", **FONT)
        ax_t.text(cols[1], yy, b, fontsize=7.2, fontweight=fw, color=C_OUT, va="top", **FONT)
        ax_t.text(cols[2], yy, c, fontsize=7.2, fontweight=fw, color=C_DIM, va="top", **FONT)
        if i == 0:
            ax_t.plot([0.0, 1.0], [yy - 0.055, yy - 0.055], color=C_OUT, lw=0.8)

    ax_nt = fig.add_axes([0.60, 0.085, 0.36, 0.33]); ax_nt.axis("off")
    draw_notes(ax_nt, [
        "NOTES:",
        "1. L-brackets fillet-welded to the post inner faces (rear-panel method); ply back face seats flush with the post wall-side face.",
        "2. Ply is machine-screwed (not lag/wood-screwed) into back-face tee-nuts so a run can be unbolted for service.",
        "3. P-clip cushion (EPDM) isolates the Ø21 riser and takes the pump vibration off the ply.",
        "4. All steel hot-dip galvanized or painted; the splash zone is chloride-free (no 316 needed).",
    ], 0.0, 1.0, 0.10, fs=6.9, title_fs=7.4, width=1.0, wrap=64, font=FONT)

    ax_tb = fig.add_axes([0.04, 0.008, 0.92, 0.045])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 2 OF {TOTAL_SHEETS}",
                drawing_title="PUMP-RUN SUPPORT DETAIL",
                subtitle="FLUSH-MOUNT SECTION + P-CLIP + SCHEDULE",
                doc_id="TBS-001 · IBC Plumbing Corridor · #29",
                scale_note="DETAILS NTS — ALL DIMS IN mm")
    _save(fig, "support-detail-sheet2.png")


if __name__ == "__main__":
    draw_sheet1()
    draw_sheet2()
