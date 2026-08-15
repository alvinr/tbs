#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""IBC Support Frame — PLATE FABRICATION SCHEDULE.

Every plate/bracket in the IBC + corridor metal, drawn 1:1 (verify against the 100 mm
scale bar) with its outline dimensions, hole diameters, and hole-center positions from a
datum edge — a shop can cut/drill each from this sheet.

Sheet 1 — flat + folded structural plates: IBC foot, wall-hanger backing, wall-hanger pocket.
Sheet 2 — welded angle brackets: bar-end cleat, rear-panel tab, side-panel pipe-run L.

Hole POSITIONS are the diagram-of-record here (per CLAUDE.md: exact coordinates a reader would
verify by measuring belong in the diagram). System-defining sizes reference tbs_constants where
they exist (the foot). The wall-hanger backing/pocket dims are sourced from the CURRENT corridor
model (generate_corridor_water_panel.py tote_restraint) — NOT the IBC_WBKT_* constants, which are
a SHARED generic wall-bracket/seat spec reused by the film-plane corner (150 wide / 4-bolt) and do
not describe this 2-bolt / 60-wide hanger.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

from tbs_constants import (IBC_FOOT_PLATE, IBC_FOOT_PLATE_T, IBC_FOOT_BOLT_D, IBC_FOOT_BOLT_PCD,
                           IBC_FOOT_BOLT_N, IBC_FRAME_RHS, DIAGRAM_DPI, DIAGRAMS_DIR)
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_notes

# ── Palette (matches generate_ibc_frame_drawing.py) ───────────────────────────
BG      = "#FFFFFF"
C_OUT   = "#1A1A1A"
C_CL    = "#2060A0"
C_DIM   = "#404040"
C_STEEL = "#B0B0B8"
C_FRAME = "#606068"
C_HOLE  = "#FFFFFF"
FONT    = {"fontfamily": "monospace"}

# ── Plate specs (mm) — diagram-of-record; sources cited inline ────────────────
FOOT_W, FOOT_T, FOOT_PCD, FOOT_BOLT_D, FOOT_N = (IBC_FOOT_PLATE, IBC_FOOT_PLATE_T,
                                                 IBC_FOOT_BOLT_PCD, IBC_FOOT_BOLT_D, IBC_FOOT_BOLT_N)
HOLE_CLR = 14          # Ø14 clearance hole for an M12 bolt (all M12 through-holes)

# Wall-hanger EXTERIOR backing plate (corridor model: ext_pw=60 X, ext_ph≈205 Z, ext_pt=8; 2× M12).
BACK_W, BACK_H, BACK_T = 60, 205, 8
BACK_BOLT_PITCH        = 169     # vertical center-to-center (bolt_hi − bolt_lo; ≥50 mm clear of the seat/bar)
BACK_EDGE              = 18      # hole center inset from each end

# Wall-hanger POCKET weldment (corridor model: back-plate S+16≈67 X × 205 Z × 4; seat S+8≈59 × 70 proj × 4).
POCK_W, POCK_H, POCK_T = 67, 205, 4
POCK_SEAT_W, POCK_SEAT_PROJ = 59, 70
POCK_SEAT_HOLE_D = HOLE_CLR      # Ø14 for the J7 vertical retention bolt through bar + seat

# Bar-end cleat (angle, corridor end — J2: 2× M12 down through the bar into the horizontal leg; W3 to upright).
CLEAT_LEG, CLEAT_T, CLEAT_LEN = 50, 6, 100
CLEAT_BOLT_PITCH, CLEAT_EDGE  = 60, 20

# Rear-panel bracket / TAB (angle welded to upright W6; J4: 1× M8 into a tee-nut in the ply).
TAB_LEG, TAB_T, TAB_H = 50, 5, 60
TAB_HOLE_D            = 9         # Ø9 clearance for M8

# Side-panel pipe-run L-bracket (1×1×⅛ angle; J5: 1× ¼-20 up into a captive tee-nut).
PRUN_LEG, PRUN_T, PRUN_LEN = 25.4, 3.2, 120
PRUN_HOLE_D                = 7    # Ø7 clearance for ¼-20


# ═══════════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════════
def _panel(ax, x0, y0, w, h, title, sub):
    """A titled sub-box for one plate."""
    ax.add_patch(Rectangle((x0, y0), w, h, fc="none", ec=C_OUT, lw=1.6, zorder=3))
    ax.text(x0 + 10, y0 + h - 16, title, fontsize=8.5, fontweight="bold", **FONT, zorder=6)
    ax.text(x0 + 10, y0 + h - 33, sub, fontsize=6, color=C_DIM, **FONT, zorder=6)


def _hole(ax, cx, cy, d, *, cl=14):
    """A drilled hole (circle) with short center marks."""
    r = d / 2
    ax.add_patch(Circle((cx, cy), r, fc=C_HOLE, ec=C_OUT, lw=1.3, zorder=8))
    ax.plot([cx - cl, cx + cl], [cy, cy], color=C_CL, lw=0.5, zorder=7)
    ax.plot([cx, cx], [cy - cl, cy + cl], color=C_CL, lw=0.5, zorder=7)


def _specbox(ax, x, y, lines):
    for i, ln in enumerate(lines):
        ax.text(x, y - i * 15, ln, fontsize=6.2, **FONT, zorder=6)


def _scale_bar(ax, x, y):
    """A 100 mm scale bar (1:1 — the drawing IS full size in data units)."""
    ax.plot([x, x + 100], [y, y], color=C_OUT, lw=2, zorder=6)
    for xx in (x, x + 50, x + 100):
        ax.plot([xx, xx], [y - 4, y + 4], color=C_OUT, lw=1.2, zorder=6)
    ax.text(x + 50, y - 16, "0        50       100 mm", fontsize=5.6, ha="center", color=C_DIM, **FONT, zorder=6)
    ax.text(x + 50, y + 8, "SCALE 1:1", fontsize=6, ha="center", fontweight="bold", **FONT, zorder=6)


# ═══════════════════════════════════════════════════════════════════════════════
# Sheet 1 — structural plates (foot / backing / pocket)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():
    fig, ax = plt.subplots(figsize=(16.5, 7.2))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(-20, 1360); ax.set_ylim(-120, 430); ax.set_aspect("equal"); ax.axis("off")
    ax.text(670, 405, "PLATE FABRICATION SCHEDULE — STRUCTURAL PLATES", fontsize=12,
            fontweight="bold", ha="center", **FONT)

    # ── PLATE 1 — IBC FLOOR FOOT (150×150×12, 4× Ø14 @ 100 sq PCD) ──
    _panel(ax, 20, 40, 420, 340, "PLATE 1 — IBC FLOOR FOOT", "A36 · 12 mm · ×4")
    cx, cy = 170, 200
    ax.add_patch(Rectangle((cx - FOOT_W/2, cy - FOOT_W/2), FOOT_W, FOOT_W, fc=C_STEEL, ec=C_OUT, lw=1.6, zorder=4))
    ax.add_patch(Rectangle((cx - IBC_FRAME_RHS/2, cy - IBC_FRAME_RHS/2), IBC_FRAME_RHS, IBC_FRAME_RHS,
                           fc="none", ec=C_CL, lw=0.9, ls=(0, (5, 3)), zorder=5))     # upright weld footprint
    ax.text(cx, cy, "upright\nweld", fontsize=5, ha="center", va="center", color=C_CL, **FONT, zorder=6)
    for sx in (-1, 1):
        for sy in (-1, 1):
            _hole(ax, cx + sx*FOOT_PCD/2, cy + sy*FOOT_PCD/2, FOOT_BOLT_D + 2)
    draw_dim_h(ax, cx - FOOT_W/2, cx + FOOT_W/2, cy + FOOT_W/2 + 22, f"{FOOT_W}mm", fs=6, font=FONT)
    draw_dim_v(ax, cx + FOOT_W/2 + 22, cy - FOOT_W/2, cy + FOOT_W/2, f"{FOOT_W}mm", fs=6, font=FONT)
    draw_dim_h(ax, cx - FOOT_PCD/2, cx + FOOT_PCD/2, cy - FOOT_W/2 - 20, f"{FOOT_PCD}mm PCD", fs=6, font=FONT, above=False)
    draw_dim_v(ax, cx - FOOT_W/2 - 22, cy - FOOT_PCD/2, cy + FOOT_PCD/2, f"{FOOT_PCD}mm", fs=6, font=FONT)
    _specbox(ax, 300, 300, [f"4× Ø{FOOT_BOLT_D+2} (M{FOOT_BOLT_D})",
                            f"@ {FOOT_PCD}×{FOOT_PCD} sq PCD", "(±50 from each CL)",
                            "corner marks = CL", "weld upright to center"])

    # ── PLATE 2 — WALL-HANGER BACKING (60×205×8, 2× Ø14) ──
    _panel(ax, 460, 40, 420, 340, "PLATE 2 — WALL-HANGER BACKING", "A36 · 8 mm · ×8 (exterior)")
    bx, by = 590, 130
    ax.add_patch(Rectangle((bx, by), BACK_W, BACK_H, fc=C_STEEL, ec=C_OUT, lw=1.6, zorder=4))
    hx = bx + BACK_W/2
    for hy in (by + BACK_EDGE, by + BACK_H - BACK_EDGE):
        _hole(ax, hx, hy, HOLE_CLR)
    draw_dim_h(ax, bx, bx + BACK_W, by - 20, f"{BACK_W}mm", fs=6, font=FONT, above=False)   # below the plate — clear of the panel title
    draw_dim_v(ax, bx + BACK_W + 22, by, by + BACK_H, f"{BACK_H}mm", fs=6, font=FONT)
    draw_dim_v(ax, bx - 22, by + BACK_EDGE, by + BACK_H - BACK_EDGE, f"{BACK_BOLT_PITCH}mm", fs=6, font=FONT)   # 18mm end-inset is in the spec box (sub-30mm — not dimensioned, P7)
    _specbox(ax, 720, 300, [f"2× Ø{HOLE_CLR} (M12) —", "vertical CL,", f"{BACK_BOLT_PITCH} apart,", f"{BACK_EDGE} from each end",
                            "J3 wall through-bolts", "(hex heads OUTSIDE)"])

    # ── PLATE 3 — WALL-HANGER POCKET (folded 4mm: back-plate + seat) ──
    _panel(ax, 900, 40, 440, 340, "PLATE 3 — WALL-HANGER POCKET", "A36 · 4 mm folded · ×8")
    px, py = 1010, 120
    ax.add_patch(Rectangle((px, py), POCK_T, POCK_H, fc=C_FRAME, ec=C_OUT, lw=1.5, zorder=5))   # back-plate (edge)
    seat_z = py + 70
    ax.add_patch(Rectangle((px + POCK_T, seat_z), POCK_SEAT_PROJ, POCK_SEAT_T if False else 4,
                           fc=C_FRAME, ec=C_OUT, lw=1.5, zorder=5))                             # seat (folded 90°)
    for shx in (px + POCK_T + 22, px + POCK_T + 50):                            # 2× J7 retention holes in the seat
        _hole(ax, shx, seat_z + 2, POCK_SEAT_HOLE_D, cl=10)
    # the 2 J3 holes pass through the back-plate too (shared with the backing plate)
    for hy in (py + BACK_EDGE, py + POCK_H - BACK_EDGE):
        ax.plot([px, px + POCK_T], [hy, hy], color=C_CL, lw=0.8, zorder=7)
        ax.add_patch(Circle((px + POCK_T/2, hy), HOLE_CLR/2, fc=C_HOLE, ec=C_OUT, lw=1.0, zorder=8))
    draw_dim_v(ax, px - 22, py, py + POCK_H, f"{POCK_H}mm", fs=6, font=FONT)
    draw_dim_h(ax, px + POCK_T, px + POCK_T + POCK_SEAT_PROJ, seat_z - 16, f"seat {POCK_SEAT_PROJ}", fs=6, font=FONT, above=False)
    leader(ax, px + POCK_T + 36, seat_z + 2, px + POCK_T + 60, seat_z - 42,
           f"2× Ø{POCK_SEAT_HOLE_D} — J7 bolts\n(bar → seat)", fs=5.8, font=FONT, ha="left")
    leader(ax, px + POCK_T/2, py + POCK_H - BACK_EDGE, px + 30, py + POCK_H + 22,
           "2× Ø14 (J3)\nalign Plate 2", fs=5.8, font=FONT, ha="left")
    _specbox(ax, 1150, 300, [f"back {POCK_W}×{POCK_H}×{POCK_T}", f"seat {POCK_SEAT_W}×{POCK_SEAT_PROJ}×{POCK_T}",
                             "fold 90° at seat line", "welds W5 (seat↔plate)", "section view (X–Z)"])

    _scale_bar(ax, 60, -70)
    draw_notes(ax, [
        "• All holes Ø14 = M12 clearance except Plate 5 (Ø9/M8) + Plate 6 (Ø7/¼-20). Deburr both faces. A36 mild-steel plate.",
        "• Datums / tolerances: hole centers ±1 mm, PCD ±0.5 mm (sheet 1 + report §3.6). Backing (2) + pocket (3) J3 holes must line up through the wall.",
    ], 470, -40, spacing=18, fs=6.2, font=FONT, width=880)

    title_block(ax, "PLATE SHEET 1 OF 2", drawing_title="IBC SUPPORT FRAME",
                subtitle="PLATE FABRICATION SCHEDULE — STRUCTURAL PLATES",
                scale_note="1:1 — verify vs the 100 mm scale bar; dims in mm", height=0.05)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "ibc-plate-schedule-sheet1.png"), dpi=DIAGRAM_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-plate-schedule-sheet1.png saved")


# ═══════════════════════════════════════════════════════════════════════════════
# Sheet 2 — welded angle brackets (cleat / tab / pipe-run L)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():
    fig, ax = plt.subplots(figsize=(16.5, 7.2))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(-20, 1360); ax.set_ylim(-120, 430); ax.set_aspect("equal"); ax.axis("off")
    ax.text(670, 405, "PLATE FABRICATION SCHEDULE — ANGLE BRACKETS", fontsize=12,
            fontweight="bold", ha="center", **FONT)

    # ── PLATE 4 — BAR-END CLEAT (angle 50×50×6, 2× Ø14 in the horizontal leg) ──
    _panel(ax, 20, 40, 420, 340, "PLATE 4 — BAR-END CLEAT", "A36 angle 50×50×6 · L100 · ×8")
    cx, cy = 120, 150
    ax.add_patch(Rectangle((cx, cy), CLEAT_T, CLEAT_LEG, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=5))      # vertical leg (to upright)
    ax.add_patch(Rectangle((cx, cy), CLEAT_LEG, CLEAT_T, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=5))      # horizontal leg (bar sits on)
    ax.text(cx - 6, cy + CLEAT_LEG + 10, "vertical leg\n(weld W3 to upright)", fontsize=5, **FONT, zorder=6)
    # face view of the horizontal (drilled) leg — to the right, showing the 2 holes along the L100 length
    fx, fy = 240, 150
    ax.add_patch(Rectangle((fx, fy), CLEAT_LEN, CLEAT_LEG, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=4))
    for hx in (fx + CLEAT_EDGE, fx + CLEAT_EDGE + CLEAT_BOLT_PITCH):
        _hole(ax, hx, fy + CLEAT_LEG/2, HOLE_CLR)
    draw_dim_h(ax, fx, fx + CLEAT_LEN, fy + CLEAT_LEG + 20, f"{CLEAT_LEN}mm", fs=6, font=FONT)
    draw_dim_h(ax, fx + CLEAT_EDGE, fx + CLEAT_EDGE + CLEAT_BOLT_PITCH, fy - 18, f"{CLEAT_BOLT_PITCH}mm", fs=6, font=FONT, above=False)
    draw_dim_v(ax, fx + CLEAT_LEN + 20, fy, fy + CLEAT_LEG, f"{CLEAT_LEG}mm", fs=6, font=FONT)
    ax.text(290, 100, "horizontal (drilled) leg — face", fontsize=5, ha="center", color=C_DIM, **FONT, zorder=6)
    _specbox(ax, 60, 320, [f"2× Ø{HOLE_CLR} (M12) — J2 bar bolts, {CLEAT_BOLT_PITCH} pitch, {CLEAT_EDGE} from each end",
                           "left = L-section end · right = drilled-leg face"])

    # ── PLATE 5 — REAR-PANEL TAB (angle 50×50×5, 1× Ø9/M8) ──
    _panel(ax, 460, 40, 420, 340, "PLATE 5 — REAR-PANEL TAB", "A36 angle 50×50×5 · ×6")
    tx, ty = 560, 130
    ax.add_patch(Rectangle((tx, ty), TAB_LEG, TAB_T, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=5))          # horizontal leg (weld to upright)
    ax.add_patch(Rectangle((tx + TAB_LEG, ty), TAB_T, TAB_H, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=5))  # vertical TAB
    ax.text(tx - 4, ty - 14, "weld leg (W6 → upright)", fontsize=5, **FONT, zorder=6)
    # face of the TAB (with its Ø9 hole) — to the right
    fx2, fy2 = 720, 130
    ax.add_patch(Rectangle((fx2, fy2), TAB_LEG, TAB_H, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=4))
    _hole(ax, fx2 + TAB_LEG/2, fy2 + TAB_H - 25, TAB_HOLE_D, cl=10)
    draw_dim_v(ax, fx2 + TAB_LEG + 20, fy2, fy2 + TAB_H, f"{TAB_H}mm", fs=6, font=FONT)
    draw_dim_h(ax, fx2, fx2 + TAB_LEG, fy2 + TAB_H + 18, f"{TAB_LEG}mm", fs=6, font=FONT)
    draw_dim_v(ax, fx2 - 20, fy2 + TAB_H - 25, fy2 + TAB_H, "25mm", fs=5.5, font=FONT)
    ax.text(fx2 + TAB_LEG/2, fy2 - 16, "TAB face", fontsize=5, ha="center", color=C_DIM, **FONT, zorder=6)
    _specbox(ax, 560, 320, [f"1× Ø{TAB_HOLE_D} (M8) — J4 bolt into a tee-nut in the ply",
                            "25 from the tab top; centered on the 50 leg"])

    # ── PLATE 6 — PIPE-RUN L-BRACKET (1×1×⅛ angle, 1× Ø7/¼-20) ──
    _panel(ax, 900, 40, 440, 340, "PLATE 6 — PIPE-RUN L-BRACKET", "1×1×⅛ angle (25×25×3.2) · L120 · ×12")
    lx, ly = 1000, 150
    ax.add_patch(Rectangle((lx, ly), PRUN_T, PRUN_LEG, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=5))        # weld leg (to post)
    ax.add_patch(Rectangle((lx, ly), PRUN_LEG, PRUN_T, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=5))        # landing leg
    ax.text(lx - 6, ly + PRUN_LEG + 8, "weld leg\n(W7 → post)", fontsize=5, **FONT, zorder=6)
    fx3, fy3 = 1070, 150
    ax.add_patch(Rectangle((fx3, fy3), PRUN_LEN, PRUN_LEG, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=4))
    _hole(ax, fx3 + PRUN_LEN/2, fy3 + PRUN_LEG/2, PRUN_HOLE_D, cl=8)
    draw_dim_h(ax, fx3, fx3 + PRUN_LEN, fy3 + PRUN_LEG + 18, f"{PRUN_LEN}mm", fs=6, font=FONT)
    draw_dim_h(ax, fx3, fx3 + PRUN_LEN/2, fy3 - 16, f"{int(PRUN_LEN/2)}mm", fs=5.5, font=FONT, above=False)
    ax.text(fx3 + PRUN_LEN/2, fy3 - 45, "landing (drilled) leg — face", fontsize=5, ha="center", color=C_DIM, **FONT, zorder=6)
    _specbox(ax, 1000, 320, [f"1× Ø{PRUN_HOLE_D} (¼-20) — J5 board fixing (mid-length)",
                             "cut from 1×1×⅛ angle offcuts"])

    _scale_bar(ax, 60, -70)
    draw_notes(ax, [
        "• Angles cut square, deburr all edges. Weld leg lengths are minimums — trim to suit the weld run in §3.5.",
        "• Plate 4 shown twice: L-section end (left) + drilled-leg face (right). Same for 5 (weld leg + tab face) and 6.",
    ], 470, -40, spacing=18, fs=6.2, font=FONT, width=880)

    title_block(ax, "PLATE SHEET 2 OF 2", drawing_title="IBC SUPPORT FRAME",
                subtitle="PLATE FABRICATION SCHEDULE — ANGLE BRACKETS",
                scale_note="1:1 — verify vs the 100 mm scale bar; dims in mm", height=0.05)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "ibc-plate-schedule-sheet2.png"), dpi=DIAGRAM_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/ibc-plate-schedule-sheet2.png saved")


if __name__ == "__main__":
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    print("Generating IBC plate fabrication schedule...")
    sheet1()
    sheet2()
    print("Done.")
