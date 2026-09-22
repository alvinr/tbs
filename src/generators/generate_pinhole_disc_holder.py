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
    PDH_PLATE_OD, PDH_PLATE_T, PDH_APERTURE, PDH_TAPER_BORE, PDH_DISC_OD,
    PDH_DISC_SEAT_D, PDH_DISC_SEAT_DEP, PDH_WASHER_OD, PDH_WASHER_ID, PDH_WASHER_T,
    PDH_RING_OD, PDH_RING_ID, PDH_RING_T, PDH_TS_N, PDH_TS_PCD, PDH_TS_D, PDH_PINHOLE_D,
    PDH_MOUNT_BC as BOLT_BC, PDH_MOUNT_D as BOLT_D, PDH_MOUNT_N as BOLT_N,
    PDH_SEAL_D as SEAL_D,
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
    fig, (axf, axs) = plt.subplots(1, 2, figsize=(11, 6.4))
    for ax in (axf, axs):
        ax.set_aspect('equal'); ax.axis('off')
    fig.patch.set_facecolor('white')
    fig.subplots_adjust(bottom=0.18, wspace=0.05, left=0.02, right=0.98, top=0.98)

    # ── Front view (scene side), 2:1 ──
    SC = 0.5
    def s(mm): return mm / SC
    pw, ph = 520, 560
    axf.set_xlim(0, pw); axf.set_ylim(0, ph)
    cx, cy = pw / 2, ph / 2 + 8

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

    # A-A cutting plane (horizontal through center)
    axf.plot([cx - r - 16, cx + r + 16], [cy, cy], color=C_CUT_BLUE, lw=0.7, ls=(0, (10, 4, 2, 4)), zorder=1)
    for xx, dx in ((cx - r - 16, 12), (cx + r + 16, -12)):
        axf.annotate('', xy=(xx + dx, cy), xytext=(xx, cy), arrowprops=dict(arrowstyle='-|>', color=C_CUT_BLUE, lw=1.2))
        axf.text(xx, cy + 12, 'A', fontsize=8, fontweight='bold', color=C_CUT_BLUE, ha='center')

    dia_stack(axf, cx, cy - r, [
        (s(PDH_RING_OD), f'Ø{PDH_RING_OD} RETAINING RING'),
        (s(PDH_TS_PCD),  f'Ø{PDH_TS_PCD} B.C. · {PDH_TS_N}× M{PDH_TS_D} THUMB SCREW'),
        (s(BOLT_BC),     f'Ø{BOLT_BC} B.C. · {BOLT_N}× M6 MOUNT BOLT'),
        (s(PDH_PLATE_OD), f'Ø{PDH_PLATE_OD}'),
    ], dirn=-1, step=s(26))
    draw_dim_v(axf, cx + r + 18, cy - r, cy + r, f'Ø{PDH_PLATE_OD}', right=True, fs=5, offset=12)
    leader(axf, cx + s(PDH_TS_PCD / 2) * 0.71, cy + s(PDH_TS_PCD / 2) * 0.71, cx + r + 4, cy + r * 0.7,
           f'{PDH_TS_N}× M{PDH_TS_D} KNURLED\nTHUMB SCREW @ Ø{PDH_TS_PCD}', fs=4.6, color=C_DIM, arrow_style='->', ha='left')
    leader(axf, cx - s(PDH_RING_ID / 2) + 1, cy + 2, cx - r - 6, cy + 95, 'Ø2.17 PINHOLE\n(in the disc)', fs=4.6, color=C_DIM, arrow_style='->', ha='right')
    axf.text(cx, cy - r - 130, 'FRONT VIEW — SCENE SIDE (2:1)', ha='center', fontsize=6, style='italic', color='#333')

    # ── Section A-A (broken-out central stack) — optical axis horizontal ──
    # Thin plate: axial (thickness) scale EXAGGERATED vs radial so the disc stack reads.
    def sx(mm): return mm * 1.7          # horizontal / axial (thickness) — exaggerated
    def sy(mm): return mm / 2.2          # vertical / radial — compressed
    sw, sh = 720, 720
    axs.set_xlim(0, sw); axs.set_ylim(0, sh)
    ax0 = 210                            # scene face x
    axc = ax0 + sx(PDH_PLATE_T)          # camera face x
    ry = sh / 2 + 10                     # optical-axis line y
    rad = sy(80)                         # show ±80mm of radius (broken-out; plate is Ø180)
    apt = sy(PDH_APERTURE / 2)
    seat_x = axc - sx(PDH_DISC_SEAT_DEP)

    # plate body (two halves, split by the Ø40 aperture) — hatched
    for sgn in (-1, 1):
        axs.add_patch(mpatches.Rectangle((ax0, ry + sgn * apt if sgn > 0 else ry - rad),
                      sx(PDH_PLATE_T), rad - apt, fc=C_ALUM, ec=C_OUT, lw=LW_THICK, hatch='///', zorder=3))
        # scene-side taper (Ø90 → Ø40), indicative angled wall
        axs.plot([ax0, ax0 + sx(6)], [ry + sgn * sy(PDH_TAPER_BORE / 2), ry + sgn * apt], color=C_OUT, lw=LW_MED, zorder=4)
        # disc-seat counterbore notch on the camera face
        axs.add_patch(mpatches.Rectangle((seat_x, ry + sgn * apt if sgn > 0 else ry - sy(PDH_DISC_SEAT_D / 2)),
                      sx(PDH_DISC_SEAT_DEP), sy(PDH_DISC_SEAT_D / 2) - apt, fc='white', ec=C_OUT, lw=0.5, zorder=4))
        # neoprene washer at the seat floor
        y_lo, y_hi = ry + sgn * sy(PDH_WASHER_ID / 2), ry + sgn * sy(PDH_WASHER_OD / 2)
        axs.add_patch(mpatches.Rectangle((seat_x, min(y_lo, y_hi)), sx(PDH_WASHER_T), abs(y_hi - y_lo),
                      fc=C_GASKT, ec=C_OUT, lw=0.4, zorder=6))
        # retaining ring clamping the disc rim, on the camera face
        y_lo, y_hi = ry + sgn * sy(PDH_RING_ID / 2), ry + sgn * sy(PDH_RING_OD / 2)
        axs.add_patch(mpatches.Rectangle((axc, min(y_lo, y_hi)), sx(PDH_RING_T), abs(y_hi - y_lo),
                      fc=C_ALUM, ec=C_OUT, lw=LW_MED, hatch='\\\\', zorder=7))
        # thumb screw through ring into plate + knurled head
        ty = ry + sgn * sy(PDH_TS_PCD / 2)
        axs.plot([axc + sx(PDH_RING_T) + sx(10), ax0 + sx(6)], [ty, ty], color=C_OUT, lw=1.8, zorder=9)
        axs.add_patch(mpatches.Rectangle((axc + sx(PDH_RING_T), ty - sy(9)), sx(10), sy(18),
                      fc='#404040', ec=C_OUT, lw=0.5, zorder=9))

    # disc (thin — exaggerated) seated on the washer
    disc_x = seat_x + sx(PDH_WASHER_T)
    axs.add_patch(mpatches.Rectangle((disc_x, ry - sy(PDH_DISC_OD / 2)), sx(1.2), sy(PDH_DISC_OD),
                  fc=C_DISC, ec=C_OUT, lw=LW_MED, zorder=8))
    axs.plot([disc_x, disc_x + sx(1.2)], [ry, ry], color='white', lw=1.0, zorder=9)   # Ø2.17 pinhole

    # optical-axis centre line + light-path arrow
    axs.plot([ax0 - sx(45), axc + sx(PDH_RING_T) + sx(45)], [ry, ry], color=C_CUT_BLUE, lw=LW_THIN, ls=(0, (8, 3, 1, 3)), zorder=2)
    axs.annotate('', xy=(disc_x + sx(30), ry), xytext=(ax0 - sx(38), ry), arrowprops=dict(arrowstyle='-|>', color='#CC7722', lw=1.4))
    axs.text(ax0 - sx(38), ry + 12, 'LIGHT →', fontsize=5, color='#CC7722', ha='left')

    axs.annotate('SCENE\n(exterior)', xy=(ax0, ry + rad + 14), xytext=(ax0 - 34, ry + rad + 78),
                 fontsize=5, color='#333', ha='center', va='bottom', arrowprops=dict(arrowstyle='->', color='#999', lw=0.6))
    axs.annotate('CAMERA\n(interior)', xy=(axc + sx(PDH_RING_T) + sx(10), ry + rad + 14),
                 xytext=(axc + 30, ry + rad + 78), fontsize=5, color='#333', ha='center', va='bottom',
                 arrowprops=dict(arrowstyle='->', color='#999', lw=0.6))

    # short part-name callouts on the assembly section — full fab dims are on Sheet 2
    lx = axc + sx(PDH_RING_T) + 70
    leader(axs, disc_x + sx(0.6), ry + sy(PDH_DISC_OD / 2) * 0.6, lx, ry + 150,
           'ICP-02 DISC\n(pinhole / lens)', fs=4.8, color=C_DIM, arrow_style='->', ha='left')
    leader(axs, seat_x + sx(PDH_WASHER_T / 2), ry + sy(PDH_WASHER_OD / 2) * 0.85, lx, ry + 58,
           'NEOPRENE WASHER\n(light seal)', fs=4.8, color=C_DIM, arrow_style='->', ha='left')
    leader(axs, axc + sx(PDH_RING_T / 2), ry - sy(PDH_RING_OD / 2) * 0.9, lx, ry - 58,
           'ICP-03 RETAINING\nRING', fs=4.8, color=C_DIM, arrow_style='->', ha='left')
    leader(axs, ax0 + sx(PDH_PLATE_T / 2), ry - sy(60), lx, ry - 150,
           'ICP-01 FRONT PLATE', fs=4.8, color=C_DIM, arrow_style='->', ha='left')
    axs.text((ax0 + axc) / 2, ry - rad - 60, 'SECTION A-A — axial ×1.7 / radial 1:2.2 (thickness exaggerated)', ha='center', fontsize=5.5, style='italic', color='#333')

    tb = fig.add_axes([0.03, 0.02, 0.94, 0.115]); tb.axis('off'); tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    title_block(tb, "SHEET 1 OF 2", drawing_title="PINHOLE DISC HOLDER — ASSEMBLY",
                subtitle="Front plate · washer · disc · retaining ring · thumb screws",
                scale_note="FRONT 1:2 / SECTION A-A (thickness exaggerated)", doc_id="TBS-PDH-01", height=0.82)

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
    leader(axd, dx, dy, dx + s3(PDH_DISC_OD / 2) + 6, dy - 60, f'Ø{PDH_PINHOLE_D} PINHOLE\n(SS-302 · 0.1 thk)', fs=5, color=C_DIM, arrow_style='->', ha='left')
    axd.text(dx, dy - s3(PDH_DISC_OD / 2) - 70,
             'PANEL C — ICP-02 DISC (2:1)\nInterchangeable: Ø2.17 (std) · Ø1.5 (sharper) · Ø3.0 (brighter) · or a lens cell',
             ha='center', fontsize=5, style='italic', color='#333')

    tb = fig.add_axes([0.03, 0.02, 0.94, 0.13]); tb.axis('off'); tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    title_block(tb, "SHEET 2 OF 2", drawing_title="PINHOLE DISC HOLDER — FABRICATION",
                subtitle="Front plate · retaining ring · interchangeable disc",
                scale_note="A 1:3 / B 1:1.5 / C 2:1", doc_id="TBS-PDH-02", height=0.82)

    out = os.path.join(DIAGRAMS_DIR, 'pinhole-disc-holder-sheet2.png')
    fig.savefig(out, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  → {out}  Done.")


draw_sheet1()
draw_sheet2()
