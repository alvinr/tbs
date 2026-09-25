#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_pinhole_disc_holder.py — Pinhole Disc Holder (front board), drawing series TBS-PDH.

(The former tilt-swing mechanism was retired — tilting a pinhole board is optically inert;
perspective is the film-plane's job. This generator now draws the simple quick-change disc holder:
a front plate + light-seal washer + interchangeable disc + circular retaining ring + 4 thumb screws.
File/output rename to pinhole-disc-holder happens in the registration pass.)

Sheet 1 — Assembly: front view (scene side) + Section A-A through the disc stack.
Sheet 2 — Fabrication: front plate (ICP-01), retaining ring (ICP-03), disc (ICP-02).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
from tbs_constants import (
    DIAGRAMS_DIR, DIAGRAM_DPI,
    PDH_PLATE_OD, PDH_PLATE_T, PDH_APERTURE, PDH_TAPER_BORE, PDH_DISC_OD, PDH_DISC_T,
    PDH_DISC_SEAT_D, PDH_DISC_SEAT_DEP, PDH_WASHER_OD, PDH_WASHER_ID, PDH_WASHER_T,
    PDH_RING_OD, PDH_RING_ID, PDH_RING_T, PDH_TS_N, PDH_TS_PCD, PDH_TS_D, PDH_PINHOLE_D,
    PDH_MOUNT_BC as BOLT_BC, PDH_MOUNT_D as BOLT_D, PDH_MOUNT_N as BOLT_N,
    PDH_SEAL_D as SEAL_D,
    PDH_ADAPT_OD, PDH_ADAPT_T, PDH_ADAPT_APT, PDH_WALL_APT,
    PDH_LENS_COPAL0, PDH_LENS_COPAL1, PDH_LENS_COPAL3,
)
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, draw_cl, draw_circle, leader

# ── Style ─────────────────────────────────────────────────────────────────────
LW_THICK, LW_MED, LW_THIN, LW_CUT = 1.8, 1.0, 0.5, 2.2
C_OUT   = '#000000'
C_HID   = '#888888'
C_DIM   = '#333333'
C_ALUM  = '#D8D8D8'
C_STEEL = '#B0B0B0'
C_GASKT = '#5A3020'   # neoprene washer
C_DISC  = '#707070'   # SS-302 disc
C_PIN   = '#101010'   # pinhole aperture
C_CUT_BLUE = '#2060A0' # section cutting-plane / centre line


def dia_stack(ax, cx, edge_y, dias_labels, dirn, step=48, fs=5, off=14):
    """Stacked concentric-Ø dimensions, progressively offset so nothing overlaps."""
    for i, (d, lbl) in enumerate(dias_labels):
        y = edge_y + dirn * (30 + i * step)
        draw_dim_h(ax, cx - d / 2, cx + d / 2, y, lbl, above=(dirn > 0), fs=fs, offset=off)


def _thumb_screw_positions(cx, cy, pcd, s):
    for i in range(PDH_TS_N):
        a = np.radians(45 + i * 360.0 / PDH_TS_N)
        yield cx + s(pcd / 2) * np.cos(a), cy + s(pcd / 2) * np.sin(a)


# ══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — Assembly: front view + Section A-A
# ══════════════════════════════════════════════════════════════════════════════
def draw_sheet1():
    fig, axf = plt.subplots(1, 1, figsize=(7.8, 8.6))
    axf.set_aspect('equal'); axf.axis('off')
    fig.patch.set_facecolor('white')
    fig.subplots_adjust(bottom=0.12, left=0.04, right=0.96, top=0.98)

    # ── Front view (scene side), 2:1 ──
    SC = 0.5
    def s(mm): return mm / SC
    pw, ph = 560, 680
    axf.set_xlim(0, pw); axf.set_ylim(0, ph)
    cx, cy = pw / 2, ph / 2 + 70

    r = s(PDH_PLATE_OD / 2)
    draw_circle(axf, cx, cy, r, lw=LW_THICK, color=C_OUT, fill=True, fc=C_ALUM)          # round plate
    draw_circle(axf, cx, cy, s(SEAL_D / 2), lw=LW_THIN, color=C_HID, ls='--')            # perimeter seal groove
    for i in range(BOLT_N):                                                              # 4× M6 mount bolts @ Ø150 (45°)
        a = np.radians(45 + i * 360.0 / BOLT_N)
        draw_circle(axf, cx + s(BOLT_BC / 2) * np.cos(a), cy + s(BOLT_BC / 2) * np.sin(a),
                    s(BOLT_D / 2), lw=LW_MED, color=C_OUT, fill=True, fc='white')
    # taper bore (hidden, behind the ring) + retaining ring + disc + pinhole + thumb screws
    draw_circle(axf, cx, cy, s(PDH_TAPER_BORE / 2), lw=LW_THIN, color=C_HID, ls='--')
    draw_circle(axf, cx, cy, s(PDH_RING_OD / 2), lw=LW_THICK, color=C_OUT, fill=True, fc=C_ALUM)   # ring OD
    draw_circle(axf, cx, cy, s(PDH_RING_ID / 2), lw=LW_MED, color=C_OUT, fill=True, fc=C_DISC)     # ring bore → disc shows
    draw_circle(axf, cx, cy, s(PDH_PINHOLE_D / 2) + 1.5, lw=0.6, color=C_OUT, fill=True, fc=C_PIN)  # pinhole (enlarged to read)
    for tx, ty in _thumb_screw_positions(cx, cy, PDH_TS_PCD, s):
        draw_circle(axf, tx, ty, s(PDH_TS_D / 2) + 0.6, lw=LW_MED, color=C_OUT, fill=True, fc='#404040')
    draw_cl(axf, cx, cy, r * 1.1)

    dia_stack(axf, cx, cy - r, [
        (s(PDH_RING_OD), f'Ø{PDH_RING_OD} RETAINING RING'),
        (s(PDH_TS_PCD),  f'Ø{PDH_TS_PCD} B.C. · {PDH_TS_N}× M{PDH_TS_D} THUMB SCREW'),
        (s(BOLT_BC),     f'Ø{BOLT_BC} B.C. · {BOLT_N}× M6 MOUNT BOLT'),
    ], dirn=-1, step=s(26))
    draw_dim_v(axf, cx + r + 18, cy - r, cy + r, f'Ø{PDH_PLATE_OD}', right=True, fs=5, offset=12)
    leader(axf, cx + s(PDH_TS_PCD / 2) * 0.71, cy + s(PDH_TS_PCD / 2) * 0.71, cx + r - 100, cy + r * 1.1,
           f'{PDH_TS_N}× M{PDH_TS_D} KNURLED\nTHUMB SCREW @ Ø{PDH_TS_PCD}', fs=4.6, color=C_DIM, arrow_style='->', ha='left')
    leader(axf, cx - s(PDH_RING_ID / 2) + 1, cy + 2, cx - r - 6, cy + 95, 'Ø2.17 PINHOLE\n(in the disc)', fs=4.6, color=C_DIM, arrow_style='->', ha='right')
    axf.text(cx, cy - r - 182, 'FRONT VIEW — SCENE SIDE (2:1)\nSection through the mount is on Sheet 3', ha='center', fontsize=6.5, style='italic', color='#333')

    tb = fig.add_axes([0.04, 0.02, 0.92, 0.10]); tb.axis('off'); tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    title_block(tb, "SHEET 1 OF 4", drawing_title="PINHOLE DISC HOLDER — GENERAL ARRANGEMENT",
                subtitle="Front plate · washer · carrier · retaining ring · thumb screws (section on Sheet 3)",
                scale_note="FRONT VIEW 2:1", doc_id="TBS-PDH-01", height=0.82)

    out = os.path.join(DIAGRAMS_DIR, 'pinhole-disc-holder-sheet1.png')
    fig.savefig(out, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  → {out}  Done.")


# ══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Fabrication: front plate, retaining ring, disc
# ══════════════════════════════════════════════════════════════════════════════
def draw_sheet2():
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.4))
    for ax in axes:
        ax.set_aspect('equal'); ax.axis('off')
    fig.patch.set_facecolor('white')
    fig.subplots_adjust(bottom=0.20, wspace=0.06, left=0.02, right=0.98, top=0.98)
    axp, axr, axd = axes

    # ── Panel A: front plate (ICP-01) round Ø180, ~1:1.3 ──
    S = 1.15
    def s(mm): return mm / S
    axp.set_xlim(0, 300); axp.set_ylim(0, 330)
    cx, cy = 140, 195
    r = s(PDH_PLATE_OD / 2)
    draw_circle(axp, cx, cy, r, lw=LW_THICK, color=C_OUT)                             # round plate
    draw_circle(axp, cx, cy, s(SEAL_D / 2), lw=LW_THIN, color=C_HID, ls='--')         # seal groove
    for i in range(BOLT_N):
        a = np.radians(45 + i * 360.0 / BOLT_N)
        draw_circle(axp, cx + s(BOLT_BC / 2) * np.cos(a), cy + s(BOLT_BC / 2) * np.sin(a), s(BOLT_D / 2), lw=0.7, color=C_OUT)
    draw_circle(axp, cx, cy, s(PDH_DISC_SEAT_D / 2), lw=LW_MED, color=C_OUT)          # disc seat
    draw_circle(axp, cx, cy, s(PDH_TAPER_BORE / 2), lw=LW_THIN, color=C_HID, ls='--')  # taper bore (scene face)
    draw_circle(axp, cx, cy, s(PDH_APERTURE / 2), lw=LW_MED, color=C_OUT)             # Ø40 aperture
    for tx, ty in _thumb_screw_positions(cx, cy, PDH_TS_PCD, s):
        draw_circle(axp, tx, ty, s(PDH_TS_D / 2), lw=0.7, color=C_OUT)
    draw_cl(axp, cx, cy, r * 1.08)
    dia_stack(axp, cx, cy - r, [
        (s(PDH_APERTURE),    f'Ø{PDH_APERTURE} LIGHT APERTURE (THRU)'),
        (s(PDH_DISC_SEAT_D), f'Ø{PDH_DISC_SEAT_D} × {PDH_DISC_SEAT_DEP} DISC SEAT (CAMERA FACE)'),
        (s(PDH_TS_PCD),      f'Ø{PDH_TS_PCD} B.C. · {PDH_TS_N}× M{PDH_TS_D} TAP (THUMB SCREWS)'),
    ], dirn=-1, step=s(20), fs=4.4)
    draw_dim_v(axp, cx + r + 16, cy - r, cy + r, f'Ø{PDH_PLATE_OD} OD', right=True, fs=5, offset=12)
    draw_dim_v(axp, cx + r + 44, cy - s(BOLT_BC / 2), cy + s(BOLT_BC / 2), f'Ø{BOLT_BC} ({BOLT_N}× M6 MOUNT)', right=True, fs=4.6, offset=12)
    axp.text(cx, cy - r - 108, f'PANEL A — ICP-01 FRONT PLATE\n6061-T6 · Ø{PDH_PLATE_OD} × {PDH_PLATE_T}mm · Ø{PDH_TAPER_BORE} scene taper',
             ha='center', fontsize=5, style='italic', color='#333')

    # ── Panel B: retaining ring (ICP-03) 1:1.5 ──
    S2 = 1.5
    def s2(mm): return mm / S2
    axr.set_xlim(0, 220); axr.set_ylim(0, 300)
    rx, ry = 110, 175
    draw_circle(axr, rx, ry, s2(PDH_RING_OD / 2), lw=LW_THICK, color=C_OUT)
    draw_circle(axr, rx, ry, s2(PDH_RING_ID / 2), lw=LW_MED, color=C_OUT)
    for tx, ty in _thumb_screw_positions(rx, ry, PDH_TS_PCD, s2):
        draw_circle(axr, tx, ty, s2(PDH_TS_D / 2 + 0.5), lw=0.7, color=C_OUT)   # M5 clearance
    draw_cl(axr, rx, ry, s2(PDH_RING_OD / 2) * 1.1)
    dia_stack(axr, rx, ry - s2(PDH_RING_OD / 2), [
        (s2(PDH_RING_ID), f'Ø{PDH_RING_ID} BORE (clamps disc rim)'),
        (s2(PDH_TS_PCD),  f'Ø{PDH_TS_PCD} B.C. · {PDH_TS_N}× Ø{PDH_TS_D + 1} CLR'),
        (s2(PDH_RING_OD), f'Ø{PDH_RING_OD} OD'),
    ], dirn=-1, step=s2(30), fs=4.6)
    axr.text(rx, ry - s2(PDH_RING_OD / 2) - 130, f'PANEL B — ICP-03 RETAINING RING (1:1.5)\n6061-T6 · Ø{PDH_RING_OD} × {PDH_RING_T}mm THK',
             ha='center', fontsize=5, style='italic', color='#333')

    # ── Panel C: disc (ICP-02) 2:1 ──
    S3 = 0.5
    def s3(mm): return mm / S3
    axd.set_xlim(0, 220); axd.set_ylim(0, 300)
    dx, dy = 110, 175
    draw_circle(axd, dx, dy, s3(PDH_DISC_OD / 2), lw=LW_THICK, color=C_OUT, fill=True, fc='#EDEDED')
    draw_circle(axd, dx, dy, 4.0, lw=0.8, color=C_OUT, fill=True, fc=C_PIN)   # pinhole (enlarged to read)
    draw_cl(axd, dx, dy, s3(PDH_DISC_OD / 2) * 1.15)
    draw_dim_v(axd, dx + s3(PDH_DISC_OD / 2) + 14, dy - s3(PDH_DISC_OD / 2), dy + s3(PDH_DISC_OD / 2),
               f'Ø{PDH_DISC_OD}', right=True, fs=5, offset=12)
    leader(axd, dx, dy, dx + s3(PDH_DISC_OD * 0.4), dy - 120, f'Ø{PDH_PINHOLE_D} PINHOLE\n(SS-302 shim over a central bore)', fs=5, color=C_DIM, arrow_style='->', ha='left')
    axd.text(dx, dy - s3(PDH_DISC_OD / 2) - 70,
             f'PANEL C — ICP-02 CARRIER (2:1) · 6061-T6 Ø{PDH_DISC_OD} × {PDH_DISC_T:.0f}mm\nInterchangeable: Ø2.17 (std) · Ø1.5 (sharper) · Ø3.0 (brighter) · or a Copal/Compur lens board (Sheet 4)',
             ha='center', fontsize=5, style='italic', color='#333')

    tb = fig.add_axes([0.03, 0.02, 0.94, 0.13]); tb.axis('off'); tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    title_block(tb, "SHEET 2 OF 4", drawing_title="PINHOLE DISC HOLDER — FABRICATION",
                subtitle="Front plate · retaining ring · interchangeable disc",
                scale_note="A 1:3 / B 1:1.5 / C 2:1", doc_id="TBS-PDH-02", height=0.82)

    out = os.path.join(DIAGRAMS_DIR, 'pinhole-disc-holder-sheet2.png')
    fig.savefig(out, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  → {out}  Done.")


def _tol_block(fig, rect, title="GENERAL TOLERANCES (unless noted)"):
    """A CNC-shop tolerance/notes block placed at `rect` [l,b,w,h] on the figure."""
    ax = fig.add_axes(rect); ax.axis('off'); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.add_patch(mpatches.Rectangle((0, 0), 1, 1, fc='#F7F7F7', ec=C_OUT, lw=0.8))
    rows = [
        f"{title}",
        "Linear ≤6mm ±0.1 · ≤30 ±0.2 · >30 ±0.3    Angular ±0.5°",
        f"Bores: Ø{PDH_DISC_SEAT_D} disc seat H7 (+0.035/0) · Ø{PDH_APERTURE} aperture +0.2/0 · Ø{PDH_RING_ID} ring bore ±0.1",
        f"PCDs (Ø{BOLT_BC} mount · Ø{PDH_TS_PCD} tap) ±0.15 positional · tapped holes ⊥ to face 0.1",
        "Surfaces: mating/seal faces Ra 1.6 · bores Ra 3.2 · others Ra 6.3 · break sharp edges 0.3×45°",
        "Datum A = plate camera face · B = Ø82 seat axis · finish: black hard-anodize (Al) after machining",
    ]
    y = 0.90
    for i, t in enumerate(rows):
        ax.text(0.02, y, t, fontsize=4.6 if i else 5.2, fontweight='bold' if i == 0 else 'normal',
                va='center', ha='left', color=C_OUT, family='monospace' if i else 'sans-serif')
        y -= 0.155


# ══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — Wall-frame adapter + section through the container wall
# ══════════════════════════════════════════════════════════════════════════════
def draw_sheet3():
    fig, (axa, axsec) = plt.subplots(1, 2, figsize=(14, 6.6), gridspec_kw={'width_ratios': [1, 2.0]})
    for ax in (axa, axsec):
        ax.set_aspect('equal'); ax.axis('off')
    fig.patch.set_facecolor('white')
    fig.subplots_adjust(bottom=0.24, wspace=0.05, left=0.02, right=0.98, top=0.98)

    # ── Panel A: wall-frame adapter, front view 1:2 ──
    S = 2.0
    def s(mm): return mm / S
    axa.set_xlim(0, 200); axa.set_ylim(0, 300)
    cx, cy = 100, 175
    r = s(PDH_ADAPT_OD / 2)
    draw_circle(axa, cx, cy, r, lw=LW_THICK, color=C_OUT)
    draw_circle(axa, cx, cy, s(PDH_ADAPT_APT / 2), lw=LW_MED, color=C_OUT)
    draw_circle(axa, cx, cy, s(PDH_WALL_APT / 2), lw=LW_THIN, color=C_HID, ls='--')
    for i in range(BOLT_N):
        a = np.radians(45 + i * 360.0 / BOLT_N)
        tx, ty = cx + s(BOLT_BC / 2) * np.cos(a), cy + s(BOLT_BC / 2) * np.sin(a)
        draw_circle(axa, tx, ty, s(3.4), lw=0.7, color=C_OUT)
        axa.plot([tx - s(6), tx + s(6)], [ty, ty], color=C_OUT, lw=0.4)
        axa.plot([tx, tx], [ty - s(6), ty + s(6)], color=C_OUT, lw=0.4)
    draw_cl(axa, cx, cy, r * 1.12)
    dia_stack(axa, cx, cy - r, [
        (s(PDH_ADAPT_APT), f'Ø{PDH_ADAPT_APT} APERTURE'),
        (s(BOLT_BC),       f'Ø{BOLT_BC} B.C. · {BOLT_N}× M6 TAP'),
        (s(PDH_ADAPT_OD),  f'Ø{PDH_ADAPT_OD} OD'),
    ], dirn=-1, step=s(22), fs=4.6)
    axa.text(cx, cy - r - 88, f'PANEL A — WALL-FRAME ADAPTER (1:2)\nS275 steel · Ø{PDH_ADAPT_OD} × {PDH_ADAPT_T}mm · welded to the corrugation',
             ha='center', fontsize=5, style='italic', color='#333')

    # ── Panel B: SECTION through the container wall (scene ← left, interior → right) ──
    def sx(mm): return mm * 3.0      # through-wall (axial) — exaggerated
    def sy(mm): return mm / 1.35     # radial — compressed
    axsec.set_xlim(0, 760); axsec.set_ylim(0, 400)
    ry = 200
    rad = sy(130)
    xw0 = 190; wt = sx(2)                       # corrugated wall
    xa0 = xw0 + wt; at = sx(PDH_ADAPT_T)        # adapter (welded on the interior face)
    xp0 = xa0 + at; pt = sx(PDH_PLATE_T)        # disc-holder plate, bolted to the adapter
    apt = sy(PDH_APERTURE / 2)
    for sgn in (-1, 1):
        # corrugated wall (Ø150 aperture)
        y0, y1 = (ry + sgn * sy(PDH_WALL_APT / 2), ry + sgn * rad)
        axsec.add_patch(mpatches.Rectangle((xw0, min(y0, y1)), wt, abs(y1 - y0), fc='#C9C9C9', ec=C_OUT, lw=1.0, hatch='xx', zorder=3))
        # adapter (Ø120 aperture) — steel, welded
        y0, y1 = (ry + sgn * sy(PDH_ADAPT_APT / 2), ry + sgn * sy(PDH_ADAPT_OD / 2))
        axsec.add_patch(mpatches.Rectangle((xa0, min(y0, y1)), at, abs(y1 - y0), fc=C_STEEL, ec=C_OUT, lw=1.2, hatch='///', zorder=3))
        axsec.add_patch(mpatches.Polygon([(xa0, ry + sgn * sy(PDH_ADAPT_OD / 2)), (xa0 + sx(3), ry + sgn * sy(PDH_ADAPT_OD / 2)),
                        (xa0, ry + sgn * (sy(PDH_ADAPT_OD / 2) - sy(10)))], closed=True, fc=C_OUT, ec=C_OUT, zorder=5))
        # disc-holder plate (Ø72 aperture; Ø110 scene taper on the wall side)
        y0, y1 = (ry + sgn * apt, ry + sgn * sy(PDH_PLATE_OD / 2))
        axsec.add_patch(mpatches.Rectangle((xp0, min(y0, y1)), pt, abs(y1 - y0), fc=C_ALUM, ec=C_OUT, lw=1.4, hatch='\\\\', zorder=3))
        axsec.plot([xp0, xp0 + sx(8)], [ry + sgn * sy(PDH_TAPER_BORE / 2), ry + sgn * apt], color=C_OUT, lw=0.9, zorder=4)
        # carrier + washer + ring on the interior face
        seat0 = xp0 + pt - sx(PDH_DISC_SEAT_DEP)
        yws = (ry + sgn * sy(PDH_WASHER_ID / 2), ry + sgn * sy(PDH_WASHER_OD / 2))
        axsec.add_patch(mpatches.Rectangle((seat0, min(yws)), sx(PDH_WASHER_T), abs(yws[1] - yws[0]), fc=C_GASKT, ec=C_OUT, lw=0.5, zorder=6))
        ycar = (ry + sgn * sy(2), ry + sgn * sy(PDH_DISC_OD / 2))
        axsec.add_patch(mpatches.Rectangle((seat0 + sx(PDH_WASHER_T), min(ycar)), sx(PDH_DISC_T), abs(ycar[1] - ycar[0]), fc=C_DISC, ec=C_OUT, lw=0.6, zorder=7))
        yrg = (ry + sgn * sy(PDH_RING_ID / 2), ry + sgn * sy(PDH_RING_OD / 2))
        axsec.add_patch(mpatches.Rectangle((xp0 + pt, min(yrg)), sx(PDH_RING_T), abs(yrg[1] - yrg[0]), fc=C_ALUM, ec=C_OUT, lw=0.9, hatch='\\\\', zorder=6))
        # M6 thumb screw holding the ring to the plate (Ø_TS_PCD) — to scale, as Sheet 1
        yts = ry + sgn * sy(PDH_TS_PCD / 2)
        axsec.add_patch(mpatches.Rectangle((xp0 + pt - sx(10), yts - sy(PDH_TS_D / 2)), sx(10) + sx(PDH_RING_T), sy(PDH_TS_D),
                        fc=C_STEEL, ec=C_OUT, lw=0.5, zorder=8))                     # Ø6 shaft (plate tap → through ring)
        axsec.add_patch(mpatches.Rectangle((xp0 + pt + sx(PDH_RING_T), yts - sy(6)), sx(8), sy(12),
                        fc='#404040', ec=C_OUT, lw=0.4, zorder=8))                   # Ø12 knurled head
        # M6 mount bolt through plate into adapter (at Ø150)
        yb0 = ry + sgn * sy(BOLT_BC / 2)
        axsec.add_patch(mpatches.Rectangle((xp0 + pt, yb0 - sy(5)), sx(3), sy(10), fc='#3B3B42', ec=C_OUT, lw=0.4, zorder=8))
        axsec.add_patch(mpatches.Rectangle((xa0, yb0 - sy(3)), (xp0 + pt) - xa0, sy(6), fc='#3B3B42', ec=C_OUT, lw=0.3, zorder=8))
    axsec.plot([xw0 - 80, xp0 + pt + 170], [ry, ry], color=C_CUT_BLUE, lw=0.7, ls=(0, (10, 4, 2, 4)), zorder=1)
    axsec.annotate('', xy=(xw0 - 14, ry), xytext=(xw0 - 84, ry), arrowprops=dict(arrowstyle='-|>', color='#C08000', lw=1.7))
    axsec.text(xw0 - 86, ry + 24, 'LIGHT\n(scene)', fontsize=5, color='#8a5a00', ha='left')
    leader(axsec, xw0 + wt / 2, ry + sy(PDH_WALL_APT / 2) + 8, xw0 - 30, ry + rad + 8, f'CORRUGATED WALL\nØ{PDH_WALL_APT} CUT', fs=4.8, color=C_DIM, arrow_style='->', ha='right')
    leader(axsec, xa0 + at / 2, ry + sy(PDH_ADAPT_OD / 2) - 8, xa0 + 46, ry + rad + 22, f'WALL-FRAME ADAPTER (welded)\nØ{PDH_ADAPT_APT} apt · 4× M6 TAP @ Ø{BOLT_BC}', fs=4.8, color=C_DIM, arrow_style='->', ha='left')
    leader(axsec, xp0 + pt, ry - sy(BOLT_BC / 2), xp0 + pt + 120, ry - rad - 6, f'{BOLT_N}× M6×{PDH_PLATE_T + 6} SHCS\n(plate → adapter)', fs=4.8, color=C_DIM, arrow_style='->', ha='left')
    leader(axsec, xp0 + pt + sx(PDH_RING_T), ry + sy(PDH_RING_ID / 2), xp0 + pt + 140, ry + rad + 8, 'RETAINING RING + CARRIER\n(pinhole / lens · swapped from inside)', fs=4.8, color=C_DIM, arrow_style='->', ha='left')
    leader(axsec, xp0 + pt + sx(PDH_RING_T) + sx(4), ry - sy(PDH_TS_PCD / 2), xp0 + pt + 150, ry - rad + 34, f'{PDH_TS_N}× M{PDH_TS_D} THUMB SCREW\n(ring → plate tap @ Ø{PDH_TS_PCD})', fs=4.8, color=C_DIM, arrow_style='->', ha='left')
    axsec.text((xw0 + xp0) / 2 + 30, ry - rad - 46, 'PANEL B — SECTION THROUGH THE PINHOLE WALL\n(axial scale exaggerated · scene left → interior right)', ha='center', fontsize=5.5, style='italic', color='#333')

    _tol_block(fig, [0.05, 0.09, 0.90, 0.135])
    tb = fig.add_axes([0.05, 0.025, 0.90, 0.055]); tb.axis('off'); tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    title_block(tb, "SHEET 3 OF 4", drawing_title="PINHOLE DISC HOLDER — WALL-FRAME ADAPTER & WALL SECTION",
                subtitle="Adapter fab · container-wall interface · mount + weld", scale_note="A 1:2 · B exagg.", doc_id="TBS-PDH-03", height=0.9)
    out = os.path.join(DIAGRAMS_DIR, 'pinhole-disc-holder-sheet3.png')
    fig.savefig(out, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white'); plt.close(fig)
    print(f"  → {out}  Done.")


# ══════════════════════════════════════════════════════════════════════════════
# SHEET 4 — Copal / Compur lens board (interchangeable carrier)
# ══════════════════════════════════════════════════════════════════════════════
def draw_sheet4():
    fig, (axb, axsec) = plt.subplots(1, 2, figsize=(13.5, 6.2), gridspec_kw={'width_ratios': [1, 1.55]})
    for ax in (axb, axsec):
        ax.set_aspect('equal'); ax.axis('off')
    fig.patch.set_facecolor('white')
    fig.subplots_adjust(bottom=0.20, wspace=0.05, left=0.02, right=0.98, top=0.98)

    # ── Panel A: lens board front view (Ø80) — ONE real drilled hole (Copal 1 shown) + alternates ──
    S = 0.9
    def s(mm): return mm / S
    axb.set_xlim(0, 240); axb.set_ylim(0, 320)
    cx, cy = 120, 200
    draw_circle(axb, cx, cy, s(PDH_DISC_OD / 2), lw=LW_THICK, color=C_OUT, fill=True, fc='#EDEDED')          # Ø80 board
    draw_circle(axb, cx, cy, s(PDH_LENS_COPAL1 / 2), lw=LW_MED, color=C_OUT, fill=True, fc='white')          # the actual drilled hole (open bore)
    draw_circle(axb, cx, cy, s(PDH_LENS_COPAL0 / 2), lw=LW_THIN, color=C_HID, ls='--')                       # alt: Copal 0
    draw_circle(axb, cx, cy, s(PDH_LENS_COPAL3 / 2), lw=LW_THIN, color=C_HID, ls='--')                       # alt: Copal 3
    draw_cl(axb, cx, cy, s(PDH_DISC_OD / 2) * 1.15)
    draw_dim_v(axb, cx + s(PDH_DISC_OD / 2) + 16, cy - s(PDH_DISC_OD / 2), cy + s(PDH_DISC_OD / 2), f'Ø{PDH_DISC_OD} CARRIER', right=True, fs=5, offset=12)
    dia_stack(axb, cx, cy - s(PDH_DISC_OD / 2), [
        (s(PDH_LENS_COPAL0), f'Ø{PDH_LENS_COPAL0} COPAL 0'),
        (s(PDH_LENS_COPAL1), f'Ø{PDH_LENS_COPAL1} COPAL 1 (shown)'),
        (s(PDH_LENS_COPAL3), f'Ø{PDH_LENS_COPAL3} COPAL 3'),
    ], dirn=-1, step=s(19), fs=4.4)
    axb.text(cx, cy - s(PDH_DISC_OD / 2) - 122, f'PANEL A — LENS BOARD · drill ONE hole to suit the shutter\n6061-T6 Ø{PDH_DISC_OD} × {PDH_DISC_T:.0f}mm — same carrier envelope as a pinhole board (fills the seat)',
             ha='center', fontsize=5, style='italic', color='#333')

    # ── Panel B: SECTION — how the Copal/Compur shutter is FIXED to the board ──
    # (front lens cell + shutter body flange on the SUBJECT face; threaded barrel through the hole;
    #  the retaining ring screws on from the FILM side and clamps the board — per S.K. Grimes.)
    def sx(mm): return mm * 5.1
    def sy(mm): return mm / 1.0
    axsec.set_xlim(90, 790); axsec.set_ylim(60, 410)
    ry = 235; bx = 430; bt = sx(4)
    br = sy(PDH_LENS_COPAL1 / 2)                    # barrel radius = board-hole radius (straight tube through the hole)
    fr = sy(PDH_LENS_COPAL1 / 2 + 13)              # flange / retaining-ring OD (wider than the hole)
    od = sy(PDH_DISC_OD / 2)
    wallt = sy(2.5)
    xfe = bx - sx(26)                              # front element — LEFT end of the barrel (subject)
    xre = bx + bt + sx(11)                         # rear element — RIGHT end, past the ring (film)
    for s1 in (-1, 1):
        # lens board (hole → OD) — hatched
        axsec.add_patch(mpatches.Rectangle((bx, min(ry + s1 * br, ry + s1 * od)), bt, abs(od - br),
                        fc='#EDEDED', ec=C_OUT, lw=1.3, hatch='\\\\', zorder=4))
        # LENS BARREL with an INTEGRAL FLANGE (one piece): the straight tube wall + the subject-side
        # shoulder that seats on the board front face
        axsec.add_patch(mpatches.Polygon([
            (xfe, ry + s1 * (br - wallt)), (xfe, ry + s1 * br), (bx - sx(3), ry + s1 * br),
            (bx - sx(3), ry + s1 * fr), (bx, ry + s1 * fr), (bx, ry + s1 * br),
            (xre, ry + s1 * br), (xre, ry + s1 * (br - wallt))],
            closed=True, fc='#C7CCD2', ec=C_OUT, lw=0.9, zorder=5))
        # RETAINING RING on the FILM face (half the flange thickness) — threads onto the barrel, clamps the board
        axsec.add_patch(mpatches.Rectangle((bx + bt, ry + s1 * br), sx(1.5), s1 * (fr - br), fc='#7A8088', ec=C_OUT, lw=0.6, zorder=5))
    # front + rear lens ELEMENTS (biconvex glass at the barrel ends; rear protrudes past the opening)
    axsec.add_patch(mpatches.Ellipse((xfe + sx(4), ry), width=sx(3.2), height=sy(34), fc='#BFE0FF', ec=C_OUT, lw=1.0, alpha=0.75, zorder=6))
    axsec.add_patch(mpatches.Ellipse((xre, ry), width=sx(2.6), height=sy(30), fc='#BFE0FF', ec=C_OUT, lw=1.0, alpha=0.75, zorder=6))
    axsec.text(xfe + sx(4), ry - sy(17) - 8, 'FRONT\nELEMENT', fontsize=5.2, ha='center', va='top', color='#2060A0')
    axsec.text(xre, ry - sy(15) - 8, 'REAR\nELEMENT', fontsize=5.2, ha='center', va='top', color='#2060A0')
    axsec.text((xfe + bx) / 2, ry - br - sy(5), 'LENS BARREL', fontsize=5.4, ha='center', va='top', color='#333')
    # optical axis (light) — subject → film
    axsec.annotate('', xy=(xre + sx(6), ry), xytext=(xfe - sx(8), ry), arrowprops=dict(arrowstyle='-|>', color='#C08000', lw=1.4))
    axsec.text(xfe - sx(8), ry + 40, 'SUBJECT', fontsize=6.0, color='#8a5a00', ha='left')
    axsec.text(xre + sx(4), ry + 40, 'FILM', fontsize=6.0, color='#8a5a00', ha='right')
    leader(axsec, bx - sx(3), ry + fr, bx - 150, ry + od + 46, 'BARREL FLANGE —\nseats on the SUBJECT face', fs=5.2, color=C_DIM, arrow_style='->', ha='right')
    leader(axsec, bx + bt / 2, ry - br + sy(1), bx - 40, ry - od - 34, f'Ø{PDH_LENS_COPAL1} board hole\n(barrel through)', fs=5.2, color=C_DIM, arrow_style='->', ha='right')
    leader(axsec, bx + bt + sx(2), ry + fr, bx + 150, ry + od + 46, 'RETAINING RING — threads on\nfrom the BACK, clamps the board', fs=5.2, color=C_DIM, arrow_style='->', ha='left')
    leader(axsec, bx + bt / 2, ry - od, bx + 96, ry - od - 52, "board (Ø80) then seats + clamps in the\nholder's Ø82 counterbore (Sheets 1/2)", fs=5.0, color=C_DIM, arrow_style='->', ha='left')
    axsec.text((xfe + xre) / 2, ry - od - 84, 'PANEL B — LENS CROSS-SECTION (Copal 1 shown · straight barrel · flange + retaining ring clamp the board)', ha='center', fontsize=6.0, style='italic', color='#333')
    axsec.text((xfe + xre) / 2, ry - od - 108, 'FRONT / REAR ELEMENT = the glass lens elements at the ends of the barrel', ha='center', fontsize=5.2, color='#555')

    tb = fig.add_axes([0.05, 0.03, 0.90, 0.11]); tb.axis('off'); tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    title_block(tb, "SHEET 4 OF 4", drawing_title="PINHOLE DISC HOLDER — COPAL/COMPUR LENS BOARD",
                subtitle="Interchangeable Ø80 lens board · 0/1/3 hole options · shutter mount", scale_note="A 1:0.9 · B exagg.", doc_id="TBS-PDH-04", height=0.82)
    out = os.path.join(DIAGRAMS_DIR, 'pinhole-disc-holder-sheet4.png')
    fig.savefig(out, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white'); plt.close(fig)
    print(f"  → {out}  Done.")


draw_sheet1()
draw_sheet2()
draw_sheet3()
draw_sheet4()
