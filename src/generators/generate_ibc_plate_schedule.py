#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""IBC Support Frame — PLATE FABRICATION SCHEDULE.

Every plate/bracket in the IBC + corridor metal, drawn 1:1 (verify against the 100 mm
scale bar) with its outline dimensions, hole diameters, and hole-center positions from a
datum edge — a shop can cut/drill each from this sheet.

Sheet 1 — flat + folded structural plates: IBC foot, wall-hanger backing, wall-hanger pocket.
Sheet 2 — bar-end cleat (fabricated 8mm-plate L) + welded angle brackets: rear-panel tab, side-panel pipe-run L.

Hole POSITIONS are the diagram-of-record here (per CLAUDE.md: exact coordinates a reader would
verify by measuring belong in the diagram). System-defining sizes reference tbs_constants where
they exist (the foot). The wall-hanger backing/pocket dims are sourced from the CURRENT corridor
model (generate_corridor_water_panel.py tote_restraint) — NOT the FP_CORNER_SEAT_* constants, which are
a SHARED generic wall-bracket/seat spec reused by the film-plane corner (150 wide / 4-bolt) and do
not describe this 2-bolt / 60-wide hanger.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

from tbs_constants import (IBC_FOOT_PLATE, IBC_FOOT_PLATE_T, IBC_FOOT_BOLT_D, IBC_FOOT_BOLT_PCD,
                           IBC_FOOT_BOLT_N, IBC_FRAME_RHS, IBC_FRONT_BAR_D, IBC_FRONT_BAR_W, DIAGRAM_DPI, DIAGRAMS_DIR)
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, draw_notes

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

# Wall-hanger POCKET weldment. Back-plate + seat standardized to 60mm wide (2026-08-15) to REUSE the
# Plate 2 backing stock (was RHS+16≈67 / RHS+8≈59 in the model — model to be reconciled). Seat carries
# ONE centered J7 retention bolt (reverted from 2: redundancy, not strength — the pocket + the fixed 2-bolt
# corridor cleat already stop the bar rotating; 1 centered bolt clears the seat edges cleanly).
POCK_W, POCK_H, POCK_T = 60, 205, 4
POCK_SEAT_W, POCK_SEAT_PROJ = 60, 70
POCK_SEAT_HOLE_D = HOLE_CLR      # Ø14 for the single J7 vertical retention bolt through bar + seat (centered)
POCK_BP_HOLE_EDGE = 18           # J3 holes on the back-plate: 18 from each end (aligns with Plate 2 backing, 169 apart)

# Bar-end cleat — an L-ANGLE, corridor end. Matches the 3D model (generate_corridor_water_panel.py
# tote_restraint: lt=8 plate, llen=90 legs, vertical leg on the bar FRONT −X, IBC_FRAME_RHS+8 tall).
# The 50×20 bar DROPS INTO the L corner; a SINGLE horizontal M12×65 (J2) runs through the vertical leg +
# the bar's TALL 50mm web (so the Ø14 hole gets ~18mm edge, not the 3mm a 20mm-wide face gave). W3 welds
# the L to the upright. (Redesigned to an L + single horizontal bolt — Alvin 2026-08-18.)
CLEAT_LEG   = 90                       # leg length ALONG the bar (Yd)
CLEAT_T     = 8                        # angle thickness
CLEAT_UP    = IBC_FRAME_RHS + CLEAT_T  # vertical-leg height (covers the bar front) = 58
CLEAT_W     = IBC_FRONT_BAR_D          # horizontal-leg reach under the bar (= bar depth) = 20
CLEAT_BOLT_Z = IBC_FRONT_BAR_W / 2     # single horizontal bolt at the bar mid-height (25 → ~18mm edge in the 50mm web)

# Rear-panel bracket / TAB (angle TEK-screwed to the post, J8; J4: 1× M8 into a tee-nut in the ply).
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
    draw_dim_h(ax, bx, bx + BACK_W, by - 20, f"{BACK_W}mm", fs=6, font=FONT, above=False)   # plate width, below
    draw_dim_h(ax, bx, hx, by - 44, f"{int(BACK_W/2)}mm", fs=5.5, font=FONT, above=False)    # hole-center CL from the left edge (centered)
    draw_dim_v(ax, bx + BACK_W + 22, by, by + BACK_H, f"{BACK_H}mm", fs=6, font=FONT)
    draw_dim_v(ax, bx - 22, by + BACK_EDGE, by + BACK_H - BACK_EDGE, f"{BACK_BOLT_PITCH}mm", fs=6, font=FONT)   # 18mm end-inset is in the spec box (sub-30mm — not dimensioned, P7)
    _specbox(ax, 720, 300, [f"2× Ø{HOLE_CLR} (M12) —", "vertical CL,", f"{BACK_BOLT_PITCH} apart,", f"{BACK_EDGE} from each end",
                            "J3 wall through-bolts", "(hex heads OUTSIDE)"])

    # ── PLATE 3 — WALL-HANGER POCKET (folded 4mm: two FACE views — back-plate + seat/fillet, holes spec'd) ──
    _panel(ax, 900, 40, 440, 340, "PLATE 3 — WALL-HANGER POCKET", "A36 · 4 mm folded · ×8")
    # (1) BACK-PLATE face (60×205) — 2× J3 holes on the vertical CL, SAME stock as Plate 2
    bpx, bpy = 950, 110
    ax.add_patch(Rectangle((bpx, bpy), POCK_W, POCK_H, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=4))
    hbx = bpx + POCK_W/2
    for hy in (bpy + POCK_BP_HOLE_EDGE, bpy + POCK_H - POCK_BP_HOLE_EDGE):
        _hole(ax, hbx, hy, HOLE_CLR)
    draw_dim_v(ax, bpx + POCK_W + 16, bpy, bpy + POCK_H, f"{POCK_H}mm", fs=5.5, font=FONT)
    draw_dim_h(ax, bpx, bpx + POCK_W, bpy - 16, f"{POCK_W}mm", fs=5.5, font=FONT, above=False)
    draw_dim_v(ax, bpx - 16, bpy + POCK_BP_HOLE_EDGE, bpy + POCK_H - POCK_BP_HOLE_EDGE, f"{BACK_BOLT_PITCH}mm", fs=5.5, font=FONT)
    ax.text(bpx + POCK_W/2, bpy + POCK_H + 12, "BACK-PLATE FACE", fontsize=6.5, ha="center", fontweight="bold", **FONT, zorder=6)
    ax.text(bpx + POCK_W/2, bpy - 40, "2× Ø14 (J3) — same stock as Plate 2", fontsize=5, ha="center", color=C_DIM, **FONT, zorder=6)
    # (2) SEAT / FILLET face (60×70) — ONE centered J7 hole (reverted from 2: redundancy, not strength)
    spx, spy = 1170, 158
    ax.add_patch(Rectangle((spx, spy), POCK_SEAT_W, POCK_SEAT_PROJ, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=4))
    hsx, hsy = spx + POCK_SEAT_W/2, spy + POCK_SEAT_PROJ/2
    _hole(ax, hsx, hsy, POCK_SEAT_HOLE_D, cl=12)
    draw_dim_h(ax, spx, spx + POCK_SEAT_W, spy - 16, f"{POCK_SEAT_W}mm", fs=5.5, font=FONT, above=False)
    draw_dim_v(ax, spx + POCK_SEAT_W + 16, spy, spy + POCK_SEAT_PROJ, f"{POCK_SEAT_PROJ}mm", fs=5.5, font=FONT)
    draw_dim_v(ax, spx - 16, spy, hsy, f"{int(POCK_SEAT_PROJ/2)}mm", fs=5.5, font=FONT)                 # hole center from the near edge
    draw_dim_h(ax, spx, hsx, spy - 36, f"{int(POCK_SEAT_W/2)}mm", fs=5, font=FONT, above=False)          # hole center from the side edge
    ax.text(spx + POCK_SEAT_W/2, spy + POCK_SEAT_PROJ + 22, "SEAT (FILLET) FACE", fontsize=6.5, ha="center", fontweight="bold", **FONT, zorder=6)
    ax.text(spx + POCK_SEAT_W/2, spy + POCK_SEAT_PROJ + 10, f"1× Ø{POCK_SEAT_HOLE_D} (J7) — bar bolts down, centered", fontsize=5, ha="center", color=C_DIM, **FONT, zorder=6)
    ax.text(1120, 62, "folded 90° at the seat/back-plate join (W5)", fontsize=5, ha="center", color=C_CL, **FONT, zorder=6)

    _scale_bar(ax, 60, -70)
    draw_notes(ax, [
        "• All holes Ø14 = M12 clearance (Plates 1–3). Deburr both faces. A36 mild-steel plate.",
        "• Datums: hole centers ±1 mm, PCD ±0.5 mm (§3.6). Backing (2) + pocket (3) share the 60mm stock; their J3 holes align through the wall.",
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

    # ── PLATE 4 — BAR-END L-CLEAT (angle; the bar DROPS INTO the corner, 1× horizontal M12 through the tall web) ──
    _panel(ax, 20, 40, 420, 340, "PLATE 4 — BAR-END L-CLEAT", f"A36 8mm L-angle · {CLEAT_LEG} long · bar drops in · 1× M12 horizontal · ×8")
    barW, barH = CLEAT_W, IBC_FRONT_BAR_W                                                              # bar 20 (X) × 50 (Z)
    # END SECTION (looking along the bar): the L corner + the 50×20 bar dropped in + the horizontal bolt
    cx, cy = 120, 120
    ax.add_patch(Rectangle((cx, cy), CLEAT_T, CLEAT_UP, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=6))        # vertical leg (bar FRONT − welded to the upright, W3)
    ax.add_patch(Rectangle((cx, cy), CLEAT_T + barW, CLEAT_T, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=6))  # horizontal leg (bar sits on)
    ax.add_patch(Rectangle((cx + CLEAT_T, cy + CLEAT_T), barW, barH, fc=C_FRAME, ec=C_OUT, lw=1.0, alpha=0.35, zorder=5))  # bar, dropped in (ghost)
    ax.text(cx + CLEAT_T + barW/2, cy + CLEAT_T + barH/2, "bar\n50×20\ndrops in", fontsize=4.6, ha="center", va="center", color=C_DIM, **FONT, zorder=7)
    bz_ = cy + CLEAT_T + CLEAT_BOLT_Z                                                                  # bolt at the bar mid-height
    ax.add_patch(Rectangle((cx - 10, bz_ - 8), 10, 16, fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=8))         # hex head (front)
    ax.add_patch(Rectangle((cx, bz_ - 4), CLEAT_T + barW + 6, 8, fc="#D8D8DC", ec=C_OUT, lw=0.8, zorder=8))  # shank through the leg + bar
    ax.add_patch(Rectangle((cx + CLEAT_T + barW + 6, bz_ - 7), 5, 14, fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=8))  # nut (back)
    draw_dim_v(ax, cx - 24, cy, cy + CLEAT_UP, f"{CLEAT_UP:.0f}mm", fs=5.5, font=FONT)                  # vertical-leg height
    draw_dim_h(ax, cx, cx + CLEAT_T + barW, cy - 16, f"{CLEAT_T + barW}mm", fs=5.5, font=FONT, above=False)   # horizontal-leg reach
    ax.text(cx - 6, cy + CLEAT_UP + 26, "END SECTION — bar drops into the L;\nvertical leg welds to the upright (W3)", fontsize=4.8, ha="left", color=C_DIM, **FONT, zorder=7)
    ax.text(cx + CLEAT_T + barW + 16, bz_, "1× M12×65 (J2)\nhorizontal", fontsize=4.8, ha="left", va="center", color=C_DIM, **FONT, zorder=8)
    # FACE view of the vertical (drilled) leg — 90 long × 58 tall, 1 hole at the bar mid-height
    fx, fy = 290, 120
    ax.add_patch(Rectangle((fx, fy), CLEAT_LEG, CLEAT_UP, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=4))
    hxc, hyc = fx + CLEAT_LEG/2, fy + CLEAT_T + CLEAT_BOLT_Z                                            # hole at mid-length, bar mid-height
    _hole(ax, hxc, hyc, HOLE_CLR, cl=10)
    draw_dim_h(ax, fx, fx + CLEAT_LEG, fy + CLEAT_UP + 16, f"{CLEAT_LEG}mm", fs=6, font=FONT)
    draw_dim_v(ax, fx + CLEAT_LEG + 18, fy, fy + CLEAT_UP, f"{CLEAT_UP:.0f}mm", fs=6, font=FONT)
    draw_dim_v(ax, fx - 16, fy + CLEAT_T, hyc, f"{int(CLEAT_BOLT_Z)}mm", fs=5.5, font=FONT)             # hole up from the bar seat (→ 18mm edge in the 50 web)
    ax.text(fx + CLEAT_LEG/2, fy - 16, "vertical (drilled) leg — face", fontsize=5, ha="center", color=C_DIM, **FONT, zorder=6)
    # PLAN VIEW (top-down) — the L's vertical leg ALSO welds to the corridor upright (Yd along +x, X depth along +y)
    px0, pyb = 130, 58
    ax.add_patch(Rectangle((px0 + CLEAT_LEG, pyb - 5), 24, barW + CLEAT_T + 10, fc=C_FRAME, ec=C_OUT, alpha=0.5, lw=1.0, zorder=4))  # upright (corridor end)
    ax.text(px0 + CLEAT_LEG + 12, pyb + barW/2, "upright", fontsize=4.2, ha="center", va="center", color=C_DIM, rotation=90, **FONT, zorder=7)
    ax.add_patch(Rectangle((px0, pyb + CLEAT_T), CLEAT_LEG, barW, fc=C_FRAME, ec=C_OUT, alpha=0.35, lw=1.0, zorder=5))   # bar on the horizontal leg (90 Yd × 20 X)
    ax.add_patch(Rectangle((px0, pyb), CLEAT_LEG, CLEAT_T, fc=C_STEEL, ec=C_OUT, lw=1.2, zorder=6))                      # vertical leg (front strip)
    bxp = px0 + CLEAT_LEG * 0.5
    ax.add_patch(Rectangle((bxp - 4, pyb - 6), 8, CLEAT_T + barW + 10, fc="#D8D8DC", ec=C_OUT, lw=0.7, zorder=8))        # horizontal bolt (along X → vertical here)
    ax.add_patch(Rectangle((bxp - 7, pyb - 6), 14, 5, fc=C_STEEL, ec=C_OUT, lw=0.8, zorder=9))                          # head
    ax.text(px0 + CLEAT_LEG/2, pyb - 15, "PLAN (top-down) — L also welds to the upright (W3)", fontsize=4.4, ha="center", color=C_DIM, **FONT, zorder=7)
    _specbox(ax, 40, 306, [f"1× Ø{HOLE_CLR} (M12×65) — J2, HORIZONTAL through",
                           "the leg + the bar's 50mm web (~18mm edge)",
                           "end section (L) · drilled leg face (R) · plan (below)"])

    # ── PLATE 5 — REAR-PANEL TAB (angle 50×50×5, 1× Ø9/M8) ──
    _panel(ax, 460, 40, 420, 340, "PLATE 5 — REAR-PANEL TAB", "A36 angle 50×50×5 · ×6")
    tx, ty = 560, 130
    ax.add_patch(Rectangle((tx, ty), TAB_LEG, TAB_T, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=5))          # horizontal leg (weld to upright)
    ax.add_patch(Rectangle((tx + TAB_LEG, ty), TAB_T, TAB_H, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=5))  # vertical TAB
    ax.text(tx - 4, ty - 14, "screw leg — 2× #14 TEK to post (J8)", fontsize=5, **FONT, zorder=6)
    draw_dim_v(ax, tx + TAB_LEG + TAB_T + 24, ty, ty + TAB_H, f"{TAB_H}mm", fs=5.5, font=FONT)          # vertical TAB (leg) outside length (label clear of the TAB; thickness is in the subtitle)
    draw_dim_h(ax, tx, tx + TAB_LEG, ty + 18, f"{TAB_LEG}mm", fs=5.5, font=FONT)                        # horizontal weld-leg outside length (in the L opening)
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
    ax.text(lx - 6, ly + PRUN_LEG + 8, "screw leg\n2× TEK (J9)", fontsize=5, **FONT, zorder=6)
    draw_dim_v(ax, lx - 13, ly, ly + PRUN_LEG, f"{int(PRUN_LEG)}mm", fs=5.5, font=FONT)                 # vertical weld-leg outside length
    draw_dim_h(ax, lx, lx + PRUN_LEG, ly - 13, f"{int(PRUN_LEG)}mm", fs=5.5, font=FONT, above=False)    # horizontal landing-leg outside length
    fx3, fy3 = 1070, 150
    ax.add_patch(Rectangle((fx3, fy3), PRUN_LEN, PRUN_LEG, fc=C_STEEL, ec=C_OUT, lw=1.5, zorder=4))
    _hole(ax, fx3 + PRUN_LEN/2, fy3 + PRUN_LEG/2, PRUN_HOLE_D, cl=8)
    draw_dim_h(ax, fx3, fx3 + PRUN_LEN, fy3 + PRUN_LEG + 18, f"{PRUN_LEN}mm", fs=6, font=FONT)
    draw_dim_h(ax, fx3, fx3 + PRUN_LEN/2, fy3 - 16, f"{int(PRUN_LEN/2)}mm", fs=5.5, font=FONT, above=False)
    draw_dim_v(ax, fx3 - 14, fy3, fy3 + PRUN_LEG/2, f"{int(round(PRUN_LEG/2))}mm", fs=5.5, font=FONT)   # hole-center height (centered on the leg)
    ax.text(fx3 + PRUN_LEN/2, fy3 - 45, "landing (drilled) leg — face", fontsize=5, ha="center", color=C_DIM, **FONT, zorder=6)
    _specbox(ax, 1000, 320, [f"1× Ø{PRUN_HOLE_D} (¼-20) — J5 board fixing (mid-length)",
                             "cut from 1×1×⅛ angle offcuts"])

    _scale_bar(ax, 60, -70)
    draw_notes(ax, [
        "• Holes: Plate 4 Ø14 (M12×65), Plate 5 Ø9 (M8), Plate 6 Ø7 (¼-20). Cut square, deburr all edges. A36.",
        "• Each plate shown twice: L-section end + drilled-leg face. Attach: Plate 4 upstand welds to the upright (W3); Plates 5/6 TEK-screw to the post (J8/J9) — no weld.",
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
