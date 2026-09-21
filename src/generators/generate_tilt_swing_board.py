#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_tilt_swing_board.py
Tilt-and-Swing Front Board — The Big Shoebox Project
Drawing series TBS-TSB  (3 sheets)

Sheet 1 — Assembly overview & Outer Adapter Frame (ICP-01)
Sheet 2 — Inner Carrier Plate (ICP-02), Bearing & Adjustment mechanism
Sheet 3 — Light seal (bellows), Locking, Calibration scale & Swap procedure

Style matches generate_plate_drawing.py (white background, same palette & helpers).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
from tbs_constants import DIAGRAMS_DIR, FRONT_BOARD_MAX_DEG, FRONT_BOARD_CLICK_DEG, FRONT_BOARD_DETENTS, FRONT_BOARD_TRAVEL_MM, FRONT_BOARD_SCREW_PITCH
from tbs_title_block import title_block
from tbs_drawing import (draw_dim_h, draw_dim_v, draw_cl, draw_circle,
                         draw_rect, leader, bolt_holes, draw_notes)
from tbs_constants import DIAGRAM_DPI

# ── Dimensions (mm) ──────────────────────────────────────────────────────────
# The tilt-swing geometry is single-sourced in tbs_constants.py (TSB_* — shared with the
# tilt-swing 3D model) and aliased here to the short local names the drawing code uses. The
# rim-kinematic-mount rationale lives with the constants; see tbs_constants.py.
from tbs_constants import (
    TSB_PL_OD as PL_OD, TSB_BOLT_BC as BOLT_BC, TSB_BOLT_D as BOLT_D, TSB_BOLT_N as BOLT_N,
    TSB_DWL_D as DWL_D, TSB_DWL_OFF as DWL_OFF, TSB_SEAL_D as SEAL_D, TSB_TRAP_SQ as TRAP_SQ,
    TSB_PH_CB_D as PH_CB_D, TSB_PH_DISC_D as PH_DISC_D, TSB_PH_BORE as PH_BORE,
    TSB_BORE as TSB01_BORE,
    TSB_LAB_D1 as LAB_D1, TSB_LAB_D2 as LAB_D2, TSB_LAB_D3 as LAB_D3,
    TSB_BELL_OUT_PCD as BELL_OUT_PCD,
    TSB_CARR_OD as CARR_OD, TSB_CARR_THICK as CARR_THICK, TSB_SOCK_PCD as SOCK_PCD,
    TSB_BELL_IN_PCD as BELL_IN_PCD,
    TSB_ADJ_D as ADJ_D, TSB_BALL_D as BALL_D, TSB_KNOB_D as KNOB_D, TSB_KNOB_H as KNOB_H,
    TSB_BUSH_OD as BUSH_OD, TSB_BUSH_L as BUSH_L,
    TSB_BELL_ID as BELL_ID, TSB_BELL_OD as BELL_OD, TSB_BELL_FREE as BELL_FREE,
    TSB_BELL_PLEATS as BELL_PLEATS, TSB_BELL_PLEAT_D as BELL_PLEAT_D,
    TSB_CLAMP_SCR_D as CLAMP_SCR_D,
    TSB_SPR_PCD as SPR_PCD, TSB_RET_RING_ID as RET_RING_ID, TSB_RET_RING_OD as RET_RING_OD,
    TSB_RET_RING_T as RET_RING_T, TSB_RET_BOLT_PCD as RET_BOLT_PCD,
    TSB_RET_BOLT_N as RET_BOLT_N, TSB_RET_BOLT_D as RET_BOLT_D,
)

# ── Drawing helpers (same as generate_plate_drawing.py) ───────────────────────

LW_THICK = 1.8
LW_MED   = 1.0
LW_THIN  = 0.5
LW_CUT   = 2.2
LW_DIM   = 0.7

C_OUT   = '#000000'
C_CL    = '#0055AA'
C_DIM   = '#333333'
C_HID   = '#888888'
C_STEEL = '#B0B0B0'
C_ALUM  = '#D8D8D8'
C_GASKT = '#404040'
C_RED   = '#CC0000'
C_DELR  = '#E8D8A0'   # Delrin/POM color
C_BEAR  = '#C0C8D8'   # bearing / steel blue-gray
C_BELL  = '#303030'   # bellows black

# ── Sheet 1 & 2 dimensions (overall front view + Section A-A master) ───────────
# These sheets were folded in from the former generate_tilt_swing_diagram.py. Their
# constants live here (module-level); ADJ_PCD is the CARRIER ball-contact PCD (260),
# distinct from the frame screw PCD (270) used by Sheets 3-5 above — hence the suffix.
FR_OD, FR_THICK, FR_BORE = 600, 40, 380
FR_LAB_1, FR_LAB_2, FR_LAB_3, FR_LAB_STEP = 382, 390, 400, 5
CR_OD, CR_THICK = 320, 25
CR_CB_D, CR_CB_DEP = 52, 3
BEL_ID, BEL_OD, BEL_FREE, BEL_PLEATS = 290, 430, 60, 4   # truncated cone: Ø290 carrier end → Ø430 frame end
BEL_INNER_PCD, BEL_OUTER_PCD = 306, 420   # bellows clamp-ring screw PCDs (carrier / frame)
ADJ_PCD_CARRIER, ADJ_SCREW, ADJ_BALL, ADJ_BUSHING = 260, 8, 8, 30
PH_APT = 2.17
C_DELRIN, C_BELLOWS, C_BALL = '#C8D8C0', '#2A2A2A', '#E0E0E0'


def draw_sheet1():
    """Sheet 1: Front view of TSB assembly (overall design) at 1:2 scale."""
    SC = 2.0
    fig_w, fig_h = 8, 7.2
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_aspect('equal')
    ax.axis('off')

    pw = fig_w * 80
    ph = fig_h * 80
    ax.set_xlim(0, pw)
    ax.set_ylim(0, ph)

    draw_rect(ax, 15, 15, pw - 30, ph - 30, lw=1.5, color='black', fc='white')

    cx = pw / 2
    cy = ph / 2 + 55

    def s(mm):
        return mm / SC

    # ICP-01 outer frame (square)
    half = s(FR_OD / 2)
    draw_rect(ax, cx - half, cy - half, 2 * half, 2 * half,
              lw=LW_THICK, color=C_OUT, fc=C_ALUM)

    # Central bore (Ø380)
    bore_r = s(FR_BORE / 2)
    draw_circle(ax, cx, cy, bore_r, lw=LW_THICK, color=C_OUT, fc='white', fill=True)

    # Labyrinth bore steps (hidden lines — visible from interior face)
    for lab_d in [FR_LAB_1, FR_LAB_2, FR_LAB_3]:
        draw_circle(ax, cx, cy, s(lab_d / 2), lw=LW_THIN, color=C_HID, ls='--')

    # (No central bearing seat — the carrier is rim-supported; the optical axis is clear.)

    # ICP-02 carrier plate (Ø320, visible through bore)
    cr_r = s(CR_OD / 2)
    draw_circle(ax, cx, cy, cr_r, lw=LW_THICK, color=C_OUT, fc='#E8E8E8', fill=True)

    # Bellows attachment — inner flange PCD (hidden)
    draw_circle(ax, cx, cy, s(BEL_INNER_PCD / 2), lw=0.4, color=C_HID, ls=(0, (2, 3)))

    # Bellows attachment — outer flange PCD (hidden)
    draw_circle(ax, cx, cy, s(BEL_OUTER_PCD / 2), lw=0.4, color=C_HID, ls=(0, (2, 3)))

    # Pinhole disc (Ø50, center of carrier)
    ph_r = s(PH_DISC_D / 2)
    draw_circle(ax, cx, cy, ph_r, lw=LW_MED, color=C_OUT, fc='#555555', fill=True)

    # Pinhole aperture (tiny dot)
    ax.add_patch(plt.Circle((cx, cy), s(PH_APT / 2) * 3, fc='white', ec=C_OUT, lw=0.5, zorder=20))

    # Counterbore (Ø52, hidden)
    draw_circle(ax, cx, cy, s(CR_CB_D / 2), lw=LW_THIN, color=C_HID, ls=':')

    # Center lines
    cl_ext = half + 30
    draw_cl(ax, cx - cl_ext, cx + cl_ext, cy, lw=LW_THIN, color=C_CL)
    ax.plot([cx, cx], [cy - cl_ext, cy + cl_ext],
            color=C_CL, lw=LW_THIN, ls=(0, (8, 3, 1, 3)), zorder=2)

    # Bolt holes (8× M12 on Ø540 PCD)
    bolt_r = s(BOLT_BC / 2)
    draw_circle(ax, cx, cy, bolt_r, lw=0.4, color=C_CL, ls=(0, (4, 4)))
    for i in range(BOLT_N):
        angle = i * 360 / BOLT_N + 22.5
        bx = cx + bolt_r * np.cos(np.radians(angle))
        by = cy + bolt_r * np.sin(np.radians(angle))
        draw_circle(ax, bx, by, s(BOLT_D / 2), lw=LW_MED, color=C_OUT, fc='white', fill=True)

    # Dowel pins (2× Ø8 at ±200mm from center, on horizontal axis)
    for sign in [-1, 1]:
        dx = cx + sign * s(DWL_OFF)
        draw_circle(ax, dx, cy, s(DWL_D / 2), lw=LW_MED, color=C_OUT, fc=C_STEEL, fill=True)

    # Seal groove (Ø420 centerline, hidden)
    draw_circle(ax, cx, cy, s(SEAL_D / 2), lw=0.5, color=C_GASKT, ls='--')

    # 4× Adjuster positions on carrier rim (Ø260 PCD). The knobs + bracket ring are on the REAR
    # (interior/camera) face — HIDDEN in this scene-side view — so draw them dashed, no fill.
    adj_r = s(ADJ_PCD_CARRIER / 2)
    adj_labels = ['SWING+', 'TILT+', 'SWING−', 'TILT−']
    adj_colors = ['#A0A0A0', '#333333', '#A0A0A0', '#333333']
    for i, (label, kc) in enumerate(zip(adj_labels, adj_colors)):
        angle = i * 90
        ax_pos = cx + adj_r * np.cos(np.radians(angle))
        ay_pos = cy + adj_r * np.sin(np.radians(angle))
        knob_r = s(ADJ_BUSHING / 2)
        draw_circle(ax, ax_pos, ay_pos, knob_r, lw=0.7, color=kc, ls='--')       # knob (rear — hidden)
        draw_circle(ax, ax_pos, ay_pos, s(ADJ_BALL / 2), lw=0.5, color=C_HID, ls=':')  # ball/seat behind
        # Label
        lx = cx + (adj_r + 40) * np.cos(np.radians(angle))
        ly = cy + (adj_r + 40) * np.sin(np.radians(angle))
        ha = 'left' if np.cos(np.radians(angle)) > 0.1 else ('right' if np.cos(np.radians(angle)) < -0.1 else 'center')
        va = 'bottom' if np.sin(np.radians(angle)) > 0.1 else ('top' if np.sin(np.radians(angle)) < -0.1 else 'center')
        ax.text(lx, ly, label, fontsize=5.5, fontweight='bold', color=kc,
                ha=ha, va=va, zorder=15)

    # 4× M6 locking set screws (small crosses near each adj screw)
    for i in range(4):
        angle = i * 90 + 15
        lx = cx + (adj_r - 12) * np.cos(np.radians(angle + 30))
        ly = cy + (adj_r - 12) * np.sin(np.radians(angle + 30))
        sz_lock = 3
        ax.plot([lx - sz_lock, lx + sz_lock], [ly, ly], color=C_OUT, lw=0.5, zorder=12)
        ax.plot([lx, lx], [ly - sz_lock, ly + sz_lock], color=C_OUT, lw=0.5, zorder=12)

    # Bellows inner clamp ring (Al) + 4× M4 screws on Ø306 — retains the bellows small end on the carrier
    bel_in_r = s(BEL_INNER_PCD / 2)
    draw_circle(ax, cx, cy, s((BEL_INNER_PCD + 8) / 2), lw=0.5, color=C_HID, ls='--')
    draw_circle(ax, cx, cy, s((BEL_INNER_PCD - 8) / 2), lw=0.5, color=C_HID, ls='--')
    for i in range(4):
        angle = 45 + i * 90
        bx = cx + bel_in_r * np.cos(np.radians(angle))
        by = cy + bel_in_r * np.sin(np.radians(angle))
        draw_circle(ax, bx, by, s(2), lw=0.5, color=C_HID, fc='white', fill=True)

    # Section cut line A-A — vertical cutting plane through the center. The two end-arrows point
    # the SAME way (the direction of sight for SECTION A-A on Sheet 2: looking toward the interior/
    # camera side, so the section reads exterior-left / interior-right). Both ends labeled 'A'.
    cut_ext = half + 50
    ax.plot([cx, cx], [cy - cut_ext, cy + cut_ext], color=C_RED, lw=LW_THIN,
            ls=(0, (10, 4, 2, 4)), zorder=19)                         # cutting-plane trace
    for yy in [cy + cut_ext, cy - cut_ext]:
        ax.plot([cx - 11, cx + 11], [yy, yy], color=C_RED, lw=LW_CUT, zorder=20)   # end mark
        ax.annotate('', xy=(cx + 40, yy), xytext=(cx + 11, yy),
                    arrowprops=dict(arrowstyle='-|>', color=C_RED, lw=1.7), zorder=20)  # sight direction
        ax.text(cx + 52, yy, 'A', fontsize=9, fontweight='bold', color=C_RED,
                ha='left', va='center', zorder=21)

    # ── Dimensions ───────────────────────────────────────────────────────────
    # Frame outer dimension
    draw_dim_h(ax, cx - half, cx + half, cy - half - 30, '600mm', above=False, fs=6, offset=8)

    # Right-side leaders (top to bottom)
    leader(ax, cx + bolt_r * 0.924, cy + bolt_r * 0.383,
           cx + 180, cy + 30, 'Ø540 PCD\n8× M12', fs=5.5)

    leader(ax, cx + bore_r * 0.707, cy + bore_r * 0.707,
           cx + 180, cy + half - 50, 'Ø380 BORE', fs=5.5)

    leader(ax, cx + cr_r * 0.6, cy + cr_r * 0.8,
           cx + 180, cy + half - 80, 'Ø320 CARRIER (ICP-02)', fs=5.5)

    leader(ax, cx + s(DWL_OFF) + s(DWL_D / 2), cy + 5,
           cx + 180, cy + 10, '2× Ø8 DOWEL', fs=5.5)

    leader(ax, cx - s(30), cy + s(30),
           cx - half - 80, cy + 55, 'CLEAR CENTER\n(no bearing — rim mount)', fs=5.5, ha='right')

    # Left-side leaders
    leader(ax, cx - s(SEAL_D / 2) * 0.707, cy - s(SEAL_D / 2) * 0.707,
           cx - half - 80, cy - half + 50, 'Ø420 SEAL GROOVE', fs=5.5)

    # Bottom leaders
    leader(ax, cx + ph_r, cy - ph_r * 0.8,
           cx + 180, cy - cr_r + 50, 'Ø50 PINHOLE DISC\nØ2.17mm APERTURE', fs=5.5)

    leader(ax, cx + adj_r * 0.383, cy - adj_r * 0.924,
           cx + 180, cy - cr_r - 65, 'Ø260 PCD\n4× M8×1.0 ADJ SCREWS', fs=5.5)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes1 = [
        'FRONT VIEW — TILT-SWING BOARD (TSB):',
        'VIEW FROM EXTERIOR (SCENE SIDE). CARRIER (ICP-02) VISIBLE THROUGH Ø380 BORE.',
        'ICP-01: 600×600×40mm AL 6061-T6 OUTER FRAME. SAME M12/540PCD/Ø8 DOWEL INTERFACE AS ALL PLATES.',
        'ICP-02: Ø320×25mm AL 6061-T6 CARRIER. CARRIES Ø50mm PINHOLE DISC (LENOX LASER SS-302).',
        'ICP-03: WAVE SPRING (in the frame counterbore) seats the carrier on the 4 adjuster balls (rim kinematic',
        'mount — 1 cone / 1 vee / 2 flat seats). NO central bearing: the optical axis is completely clear.',
        f'ADJUSTMENT: 4× M8×1.0 SCREWS on an INTERIOR BRACKET RING — KNOBS ON THE REAR (dashed), SET FROM INSIDE.',
        f'BLACK KNOBS = TILT, SILVER = SWING · {FRONT_BOARD_CLICK_DEG}°/CLICK. LOCKING: 4× M6 NYLON-TIP SET SCREWS (3mm HEX, INTERIOR SIDE).',
        'BELLOWS (ICP-04): TRUNCATED CONE Ø290→Ø430, 4-PLEAT NEOPRENE, CLAMP-RING RETAINED, ZERO-FRICTION LIGHT SEAL.',
    ]
    draw_notes(ax, notes1, 35, cy - half - 70, spacing=10,
               fs=6, width=pw - 70)

    title_block(ax, "SHEET 1 OF 7",
                drawing_title="TILT-SWING FRONT BOARD",
                subtitle="OVERALL DESIGN — FRONT VIEW (SCENE SIDE) — ICP-01 + ICP-02",
                scale_note="SCALE 1:2 · AXES IN mm",
                height=0.040,
                doc_id="TBS-TSB · Tilt-Swing Board")

    plt.tight_layout(pad=0)
    out1 = f'{DIAGRAMS_DIR}/tilt-swing-sheet1.png'
    fig.savefig(out1, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  → tilt-swing-sheet1.png  Done.')


def draw_sheet2():
    """Sheet 2: Cross-section A-A through TSB assembly (sectional master) at 1:2 scale."""
    SC = 2.0
    fig_w, fig_h = 8, 8   # widened from 5 → 8 to open a right-hand column for DETAIL Z
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_aspect('equal')
    ax.axis('off')

    pw = fig_w * 80
    ph = fig_h * 80
    ax.set_xlim(0, pw)
    ax.set_ylim(0, ph)

    draw_rect(ax, 15, 15, pw - 30, ph - 30, lw=1.5, color='black', fc='white')

    def s(mm):
        return mm / SC

    # Section center: carrier center / pinhole plane. cx pinned toward the left third so the
    # widened sheet leaves a clear right-hand column (x > ~410) for the DETAIL Z inset.
    cx = pw * 0.28
    cy = ph / 2 + 20

    # ── ICP-01 Outer adapter frame (cross-section) ───────────────────────────
    fr_left = cx - s(FR_THICK)

    # ── Corrugated container END wall + flat wall-frame adapter plate + enlarged aperture ──
    # The pinhole (nose) end wall is corrugated steel — a precision mount can't seat on it directly.
    # A flat wall-frame ADAPTER PLATE is welded/bolted over the corrugation to give ICP-01 a flat
    # datum, and the aperture is cut LARGER than the Ø380 bore straight through the corrugation.
    wall_half = s(FR_OD / 2) + 30
    apt_half  = s(FR_BORE / 2 + 20)          # enlarged aperture (~Ø420) cut through the wall + plate
    adap_r    = fr_left - s(4)                # adapter-plate interior face — ICP-01 bolts to it
    adap_l    = adap_r - s(10)               # 10mm flat steel adapter plate
    corr_r    = adap_l                        # corrugation crests bear on the adapter
    corr_amp  = s(28)                         # container-wall corrugation depth
    corr_l    = corr_r - corr_amp
    wall_x    = corr_l                        # exterior-most face (centerline / label refs below)
    pitch     = s(80)
    for y0, y1 in [(cy + apt_half, cy + wall_half), (cy - wall_half, cy - apt_half)]:
        # flat adapter plate segment
        ax.add_patch(mpatches.Rectangle((adap_l, y0), adap_r - adap_l, y1 - y0,
                     fc=C_STEEL, ec=C_OUT, lw=LW_MED, zorder=5, hatch='...'))
        # corrugated wall segment — trapezoidal square-wave outer profile, filled band
        edge_x, edge_y = [], []
        yc = y0
        crest = True
        while yc < y1:
            yn = min(yc + pitch / 2, y1)
            x = corr_r if crest else corr_l
            edge_x += [x, x]; edge_y += [yc, yn]
            yc = yn; crest = not crest
        poly = list(zip(edge_x, edge_y)) + [(corr_r, y1), (corr_r, y0)]
        ax.add_patch(mpatches.Polygon(poly, closed=True, fc=C_STEEL, ec=C_OUT,
                     lw=LW_MED, zorder=3, hatch='///'))
        # one wall-frame through-bolt (adapter → corrugation crest) per segment
        by = (y0 + y1) / 2
        ax.plot([corr_r - s(20), adap_r + s(3)], [by, by], color=C_OUT, lw=1.3, zorder=6)
    ax.text(corr_l - s(4), cy + wall_half - s(20), 'CORRUGATED\nCONTAINER\nEND WALL',
            ha='right', va='top', fontsize=4.4, color=C_DIM, style='italic')
    ax.text(corr_l - s(4), cy - wall_half + s(20), 'FLAT WALL-FRAME\nADAPTER PLATE\n(over corrugation)',
            ha='right', va='bottom', fontsize=4.4, color=C_DIM, style='italic')
    ax.annotate('ENLARGED APERTURE\n(cut through wall, > Ø380 bore)',
                xy=(corr_r, cy + apt_half), xytext=(corr_l - s(6), cy + apt_half + s(28)),
                fontsize=4.2, color=C_DIM, style='italic', ha='right', va='bottom',
                arrowprops=dict(arrowstyle='->', color='#999', lw=0.5))
    fr_right = cx
    fr_half = s(FR_OD / 2)
    bore_half = s(FR_BORE / 2)

    # Upper frame section (above bore)
    ax.add_patch(mpatches.Rectangle(
        (fr_left, cy + bore_half), s(FR_THICK), fr_half - bore_half,
        fc=C_ALUM, ec=C_OUT, lw=LW_THICK, zorder=5))
    # Lower frame section (below bore)
    ax.add_patch(mpatches.Rectangle(
        (fr_left, cy - fr_half), s(FR_THICK), fr_half - bore_half,
        fc=C_ALUM, ec=C_OUT, lw=LW_THICK, zorder=5))

    # Cross-hatching for aluminum
    for section_bot, section_top in [(cy + bore_half, cy + fr_half),
                                     (cy - fr_half, cy - bore_half)]:
        for i in range(80):
            y0 = section_bot + i * 4
            if y0 < section_top:
                y1 = min(y0 + 4, section_top)
                ax.plot([fr_left, fr_left + min(s(FR_THICK), y1 - y0)],
                        [y0, y1], color='#AAAAAA', lw=0.3, zorder=6,
                        clip_on=True)

    # ── ICP-02 Carrier plate (cross-section) — RIM-SUPPORTED; adjust from the INTERIOR ──
    # Rim kinematic mount: the carrier is pushed toward the frame (−A) by 4 adjuster balls seating in
    # kinematic seats on its REAR (camera-side) face, and pushed back (+A) by a peripheral WAVE SPRING
    # in a counterbore in the frame's interior face. The adjusters mount on an interior BRACKET RING so
    # the knobs face into the container (accessible). Optical axis clear — only the Ø2.17 pinhole.
    sp_gap = s(30)                          # wave-spring working gap (frame face ↔ carrier exterior face)
    cr_half = s(CR_OD / 2)
    cr_left = cx + sp_gap                   # carrier exterior (scene) face — the spring bears here
    cr_right = cr_left + s(CR_THICK)        # carrier interior (camera) face — the adjuster balls contact here

    ax.add_patch(mpatches.Rectangle((cr_left, cy - cr_half), s(CR_THICK), 2 * cr_half,
                 fc='#E0E0E0', ec=C_OUT, lw=LW_THICK, zorder=5))
    for i in range(90):        # cross-hatching, full height
        y0 = cy - cr_half + i * 4
        if y0 < cy + cr_half:
            y1 = min(y0 + 4, cy + cr_half)
            ax.plot([cr_left, cr_left + min(s(CR_THICK), y1 - y0)],
                    [y0, y1], color='#AAAAAA', lw=0.3, zorder=6)
    ax.plot([cr_left, cr_right], [cy, cy], color='white', lw=1.3, zorder=7)  # Ø2.17 pinhole bore

    # ── Pinhole disc (on carrier interior/camera face) ──
    disc_half = s(PH_DISC_D / 2)
    disc_t = s(0.1) * 20
    ax.add_patch(mpatches.Rectangle((cr_right, cy - disc_half), disc_t, s(PH_DISC_D),
                 fc='#666666', ec=C_OUT, lw=LW_MED, zorder=8))
    cb_half = s(CR_CB_D / 2); cb_dep = s(CR_CB_DEP)
    ax.add_patch(mpatches.Rectangle((cr_right - cb_dep, cy - cb_half), cb_dep, s(CR_CB_D),
                 fc='white', ec=C_OUT, lw=0.5, zorder=7))

    # ── Bellows (ICP-04) — in the frame↔carrier gap (exterior side), clamp-ring both ends ──
    bel_inner_half = s(BEL_ID / 2)
    bel_outer_half = s(BEL_OD / 2)
    bel_left = cx
    bel_right = cr_left
    for sign in [-1, 1]:
        y_inner = cy + sign * bel_inner_half
        y_outer = cy + sign * bel_outer_half
        y_mid = (y_inner + y_outer) / 2
        pleat_xs = np.linspace(bel_left, bel_right, BEL_PLEATS * 2 + 1)
        pleat_ys = [(y_mid + (sign if j % 2 == 0 else -sign) * (y_outer - y_mid) * 0.3)
                    for j in range(len(pleat_xs))]
        ax.plot(pleat_xs, pleat_ys, color=C_BELLOWS, lw=1.2, zorder=4)

    def _clamp_ring(cxr, cyr):
        ax.add_patch(mpatches.Rectangle((cxr - s(3), cyr - s(7)), s(6), s(14),
                     fc=C_ALUM, ec=C_OUT, lw=LW_MED, zorder=8))
        ax.add_patch(plt.Circle((cxr, cyr), s(2), fc='#888888', ec=C_OUT, lw=0.4, zorder=9))
    for sgn in [-1, 1]:
        _clamp_ring(bel_left + s(4),  cy + sgn * bel_outer_half)   # frame end (outer, Ø420 clamp)
        _clamp_ring(bel_right - s(4), cy + sgn * bel_inner_half)   # carrier end (inner, Ø306 clamp)

    # ── Preload wave spring (ICP-03): in a frame-face counterbore, pushes the carrier +A ──
    for sgn in [-1, 1]:
        sy = cy + sgn * s(SPR_PCD / 2)
        wx = np.linspace(cx, cr_left, 9)
        wy = [sy + (s(3) if k % 2 else -s(3)) for k in range(len(wx))]
        wy[0] = wy[-1] = sy
        ax.plot(wx, wy, color=C_STEEL, lw=1.3, zorder=7)
        ax.add_patch(mpatches.Rectangle((cx - s(4), sy - s(6)), s(4), s(12),   # counterbore recess
                     fc='white', ec=C_OUT, lw=0.5, zorder=6))

    # ── Adjuster bracket ring (interior) + 4 adjusters — knobs face INTO the container ──
    adj_arm = s(ADJ_PCD_CARRIER / 2)
    ring_x0 = cr_right + s(26)
    ring_x1 = ring_x0 + s(RET_RING_T)
    r_in = adj_arm - s(8)                   # ring reaches in to the adjusters
    r_out = s(RET_BOLT_PCD / 2) + s(8)      # …out to the standoffs
    for sgn in [-1, 1]:
        ax.add_patch(mpatches.Rectangle((ring_x0, cy + sgn * r_in), ring_x1 - ring_x0, sgn * (r_out - r_in),
                     fc=C_ALUM, ec=C_OUT, lw=LW_MED, hatch='\\\\\\', zorder=6))
        by = cy + sgn * s(RET_BOLT_PCD / 2)                      # standoff: frame → bracket ring
        ax.plot([fr_right, ring_x0], [by, by], color=C_OUT, lw=1.4, zorder=6)
    for sign in [-1, 1]:
        screw_y = cy + sign * adj_arm
        ax.add_patch(mpatches.Rectangle((ring_x0, screw_y - s(ADJ_SCREW/2) - 2),   # Delrin bushing in ring
                     ring_x1 - ring_x0, s(ADJ_SCREW) + 4, fc=C_DELRIN, ec=C_OUT, lw=0.5, zorder=9))
        ax.plot([cr_right - 3, ring_x1 + s(16)], [screw_y, screw_y], color=C_OUT, lw=1.5, zorder=10)  # screw
        ball_r = s(ADJ_BALL / 2)
        ax.add_patch(plt.Circle((cr_right - 3, screw_y), ball_r, fc=C_BALL, ec=C_OUT, lw=0.5, zorder=11))  # ball
        ax.add_patch(plt.Circle((cr_right, screw_y), ball_r + 1, fc='#D0D0D0', ec=C_OUT, lw=0.5, zorder=10))  # seat
        knob_w = s(15); knob_half = s(10)                       # knob — interior (into the container)
        ax.add_patch(mpatches.Rectangle((ring_x1 + s(16), screw_y - knob_half), knob_w, 2*knob_half,
                     fc='#333333' if sign != 0 else '#A0A0A0', ec=C_OUT, lw=LW_MED, zorder=10))
        ax.text(ring_x1 + s(16) + knob_w + 8, screw_y, 'TILT+' if sign > 0 else 'TILT−',
                ha='left', va='center', fontsize=5, fontweight='bold', color='#333333')

    # ── Centerline ───────────────────────────────────────────────────────────
    cl_left = wall_x - 20
    cl_right = cr_right + disc_t + 40
    ax.plot([cl_left, cl_right], [cy, cy],
            color=C_CL, lw=LW_THIN, ls=(0, (8, 3, 1, 3)), zorder=2)

    # ── Labels ───────────────────────────────────────────────────────────────
    knob_far = ring_x1 + s(16) + s(15)      # interior-most point (knob outer face)
    arr_y = cy + fr_half + 15
    ax.annotate('EXTERIOR\n(SCENE)', xy=(wall_x, arr_y), xytext=(wall_x - 30, arr_y + 35),
                fontsize=5, color='#333', style='italic', ha='center', va='bottom',
                arrowprops=dict(arrowstyle='->', color='#999', lw=0.6))
    ax.annotate('INTERIOR (CAMERA)\n— adjust from here', xy=(knob_far, arr_y), xytext=(knob_far - 10, arr_y + 35),
                fontsize=5, color='#333', style='italic', ha='center', va='bottom',
                arrowprops=dict(arrowstyle='->', color='#999', lw=0.6))

    lx_r = knob_far + s(40)                  # component-label column, clear of the interior knobs
    leader(ax, (fr_left + fr_right) / 2, cy + fr_half - 10, lx_r + 20, cy + fr_half + 20,
           'ICP-01 OUTER FRAME\n600×600×40 AL', fs=5)
    leader(ax, (cr_left + cr_right) / 2, cy + cr_half - 5, lx_r + 20, cy + 130,
           'ICP-02 CARRIER Ø320×25 AL', fs=5)
    leader(ax, ring_x1 + s(23), cy + adj_arm, lx_r + 20, cy + 75,
           'M8 ADJUSTER + KNOB on an INTERIOR\nBRACKET RING — set from inside', fs=5)
    leader(ax, cr_right + disc_t / 2, cy + disc_half + 3, lx_r + 20, cy + 30,
           'PINHOLE DISC Ø50×0.1\nØ2.17mm APT SS-302', fs=5)
    leader(ax, bel_left + (bel_right - bel_left) / 2, cy - bel_outer_half + 5, lx_r + 20, cy - 110,
           'ICP-04 BELLOWS\nØ290→Ø430 CONE\nCLAMP-RING BOTH ENDS', fs=5)

    # left-side callout: wave spring (frame counterbore). The kinematic seats are shown in DETAIL Z
    # + the notes + Sheet 4, so they are not re-called-out here to keep the interior side readable.
    leader(ax, cx - s(2), cy - s(SPR_PCD / 2), fr_left - 34, cy - s(SPR_PCD / 2) - 70,
           'ICP-03 WAVE SPRING —\nin a frame counterbore,\npushes the carrier onto\nthe adjuster balls', fs=4.6, ha='right')

    # ── Dimensions ───────────────────────────────────────────────────────────
    draw_dim_h(ax, fr_left, fr_right, cy + fr_half + 10, '40mm',
               above=True, fs=6, offset=8)
    draw_dim_h(ax, cr_left, cr_right, cy - cr_half - 80, '25mm',
               above=False, fs=6, offset=8)
    draw_dim_v(ax, fr_left - 50, cy, cy + fr_half, '300mm',
               right=False, fs=6, offset=8)
    draw_dim_v(ax, fr_left - 50, cy - fr_half, cy, '300mm',
               right=False, fs=6, offset=8)
    # (bore Ø380 / carrier Ø320 radii are fully dimensioned on Sheets 3 & 4 — omitted here to keep the
    #  component leaders clear on the sectional master)

    # Section title — at top of drawing
    ax.text(cx, cy + fr_half + 100, 'SECTION A-A', ha='center', fontsize=8,
            fontweight='bold', color=C_RED)
    ax.text(cx, cy + fr_half + 83, '1:2 SCALE', ha='center', fontsize=6, color='#555')

    # ── Notes ────────────────────────────────────────────────────────────────
    notes2 = [
        'SECTION A-A — TILT-SWING BOARD ASSEMBLY:',
        'RIM KINEMATIC MOUNT — the carrier is located ONLY at its rim; the optical axis is fully clear (no central',
        'shank/bearing). The 4 adjuster balls seat in kinematic seats on the carrier REAR face (1 cone / 1 V-groove /',
        '2 flat → in-plane + spin fixed) and push it toward the frame; a peripheral WAVE SPRING in a frame counterbore',
        'pushes it back → zero backlash. Adjusters mount on an interior BRACKET RING so the KNOBS are set from INSIDE.',
        f'ADJUSTMENT: M8×1.0 pairs set TILT (N/S) & SWING (E/W) via Gr-25 Ø8mm balls. RANGE ±{FRONT_BOARD_MAX_DEG}°, {FRONT_BOARD_CLICK_DEG}°/click ({FRONT_BOARD_DETENTS}-detent).',
        'PIVOT ~one carrier-thickness behind the pinhole → pinhole shifts ~2.3mm at ±5.3° (<1.5% parallax).',
        f'BELLOWS (non-structural light seal): clamp-ring both ends. LABYRINTH bore Ø{LAB_D1}/{LAB_D2}/{LAB_D3}, 5 deep — secondary seal.',
    ]
    draw_notes(ax, notes2, 25, ph * 0.185, spacing=12, fs=4.6, width=430)

    # ── DETAIL Z — enlarged rim-mount inset (how the carrier is HELD, not floating) ──
    # Circle a rim joint on the section, draw the enlargement in the right-hand column.
    zc_x, zc_y = cr_right + s(10), cy - s(150)
    ax.add_patch(plt.Circle((zc_x, zc_y), 34, fill=False, ec=C_RED, lw=0.9, zorder=13))
    ax.text(zc_x - 44, zc_y, 'Z', fontsize=7, color=C_RED, fontweight='bold', ha='center', va='center', zorder=13)
    ax.annotate('', xy=(zc_x + 34, zc_y), xytext=(430, 300),
                arrowprops=dict(arrowstyle='-', color=C_RED, lw=0.6, ls=':'), zorder=12)

    bx0, by0, bw, bh = 430, 150, 190, 310
    ax.add_patch(mpatches.Rectangle((bx0, by0), bw, bh, fill=False, ec=C_OUT, lw=0.9, zorder=11))
    ax.text(bx0 + bw / 2, by0 + bh - 16, 'DETAIL Z — RIM MOUNT (4:1)', ha='center', fontsize=5.6,
            fontweight='bold', color=C_RED, zorder=13)
    ax.text(bx0 + bw / 2, by0 + bh - 30, 'how the carrier is held — no central bearing',
            ha='center', fontsize=4.2, style='italic', color='#555', zorder=13)

    def zi(mm): return mm * 1.6                      # inset local scale
    xi, yi = bx0 + 78, by0 + bh / 2 - 12             # carrier center-x, joint center-y
    exf = xi - zi(6)                                 # carrier exterior (left) face — spring bears here
    inx = xi + zi(6)                                 # carrier interior (right) face — ball contacts here
    ax.add_patch(mpatches.Rectangle((exf, yi - zi(52)), zi(12), zi(104),
                 fc='#E0E0E0', ec=C_OUT, lw=1.0, hatch='///', zorder=12))                # carrier rim
    # frame (far left) with a counterbore holding the wave spring
    fbx = bx0 + 8
    ax.add_patch(mpatches.Rectangle((fbx, yi - zi(34)), zi(11), zi(68),
                 fc=C_ALUM, ec=C_OUT, lw=0.7, hatch='\\\\\\', zorder=11))
    ax.add_patch(mpatches.Rectangle((fbx + zi(11) - zi(3), yi - zi(6)), zi(3), zi(12),
                 fc='white', ec=C_OUT, lw=0.5, zorder=12))                               # spring counterbore
    sx = np.linspace(fbx + zi(11), exf, 11)                                              # wave spring
    sy = [yi + (zi(4) if k % 2 else -zi(4)) for k in range(len(sx))]
    sy[0] = sy[-1] = yi
    ax.plot(sx, sy, color=C_STEEL, lw=1.3, zorder=12)
    # Ø8 ball in kinematic seat on the carrier interior (right) face
    ax.add_patch(plt.Circle((inx + zi(4.5), yi), zi(4.5), fc=C_BALL, ec=C_OUT, lw=0.7, zorder=13))
    ax.plot([inx, inx - zi(4), inx], [yi - zi(5), yi, yi + zi(5)], color=C_OUT, lw=0.9, zorder=13)  # cone (opens right)
    # adjuster shank → bracket ring → knob (interior)
    rx = inx + zi(22)
    ax.plot([inx + zi(9), rx], [yi, yi], color=C_OUT, lw=1.6, zorder=12)                 # shank
    ax.add_patch(mpatches.Rectangle((rx, yi - zi(44)), zi(7), zi(88),
                 fc=C_ALUM, ec=C_OUT, lw=1.0, hatch='\\\\\\', zorder=12))                # bracket ring
    ax.add_patch(mpatches.Rectangle((rx + zi(7), yi - zi(5.5)), zi(11), zi(11),
                 fc='#333333', ec=C_OUT, lw=0.8, zorder=13))                             # knob (interior)
    ax.plot([fbx + zi(11), rx], [yi + zi(38), yi + zi(38)], color=C_HID, lw=0.6, ls='--', zorder=10)  # standoff frame→ring
    # bellows lip + clamp ring on the carrier exterior rim (top, in the frame gap)
    ax.add_patch(mpatches.Rectangle((exf, yi + zi(52)), zi(12), zi(4),
                 fc=C_BELL, ec=C_OUT, lw=0.5, zorder=13))
    ax.add_patch(mpatches.Rectangle((exf + zi(1), yi + zi(56)), zi(10), zi(7),
                 fc=C_ALUM, ec=C_OUT, lw=0.8, hatch='\\\\\\', zorder=13))
    ax.plot([exf - zi(2), exf - zi(8)], [yi + zi(54), yi + zi(64)], color=C_BELL, lw=1.2, zorder=12)
    # ── inset labels ──
    ax.text(fbx - zi(2), yi + zi(20), 'WAVE SPRING\n(frame c\'bore)', ha='left', va='top', fontsize=4.0, color=C_DIM, zorder=13)
    ax.text(xi, yi - zi(56), 'CARRIER RIM', ha='center', va='top', fontsize=4.0, color=C_DIM, zorder=13)
    ax.text(inx + zi(3), yi + zi(16), 'Ø8 BALL\nIN SEAT', ha='center', va='top', fontsize=4.0, color=C_DIM, zorder=13)
    ax.text(rx + zi(4), yi - zi(14), 'M8 ADJUSTER\n+ KNOB (interior)', ha='center', va='bottom', fontsize=4.0, color=C_DIM, zorder=13)
    ax.text(exf - zi(6), yi + zi(66), 'BELLOWS LIP\n+ CLAMP RING', ha='right', va='bottom', fontsize=4.0, color=C_DIM, zorder=13)
    ax.text(bx0 + bw / 2, by0 + 10,
            'carrier CLAMPED between the wave spring (push →) and the\nadjuster ball (← push-back); knobs set from the interior',
            ha='center', va='bottom', fontsize=4.0, style='italic', color='#444', zorder=13)

    title_block(ax, "SHEET 2 OF 7",
                drawing_title="TILT-SWING FRONT BOARD",
                subtitle="SECTION A-A (SECTIONAL MASTER)",
                scale_note="1:2 · mm",
                doc_id="TBS-TSB · Tilt-Swing Board",
                portrait=True)

    plt.tight_layout(pad=0)
    out2 = f'{DIAGRAMS_DIR}/tilt-swing-sheet2.png'
    fig.savefig(out2, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  → tilt-swing-sheet2.png  Done.')


draw_sheet1()
draw_sheet2()


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — ICP-01 Outer Adapter Frame (exterior + interior faces)
# ═══════════════════════════════════════════════════════════════════════════════

FW, FH = 700, 500
FW1, FH1 = 3400, 2320
fig1, ax1 = plt.subplots(figsize=(FW*0.9/25.4, FH*0.9/25.4))
fig1.patch.set_facecolor('white')
ax1.set_facecolor('white')
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_xlim(0, FW1)
ax1.set_ylim(0, FH1)

title_block(ax1, "SHEET 3 OF 7",
            drawing_title="TILT-SWING FRONT BOARD",
            subtitle="ICP-01 Outer Adapter Frame — exterior + interior faces · fully dimensioned",
            scale_note="AXES IN mm",
            doc_id="TBS-TSB · Tilt-Swing Board")

# ── Section header lines ──────────────────────────────────────────────────────
def section_label(ax, x, y, text):
    ax.text(x, y, text, fontsize=7.5, fontweight='bold', color='black')
    ax.plot([x, x+1100], [y-24, y-24], color='black', lw=0.7)

# ── Stacked concentric-diameter dimensions (formal): one dim_h per Ø, progressively
# offset away from the plate so nothing overlaps. dirn=-1 stacks BELOW, +1 ABOVE. ──
def dia_stack(ax, cx, edge_y, dias_labels, dirn, step=52, fs=5, off=16):
    for i, (d, lbl) in enumerate(dias_labels):
        y = edge_y + dirn * (30 + i * step)
        draw_dim_h(ax, cx - d/2, cx + d/2, y, lbl, above=(dirn > 0), fs=fs, offset=off)

section_label(ax1, 560, 1930, 'PANEL A — ICP-01 EXTERIOR FACE (1:8)')
section_label(ax1, 2010, 1930, 'PANEL B — ICP-01 INTERIOR FACE (1:8)')

SC = 1
def s1(mm): return mm * SC
hw = s1(PL_OD/2)

# ───────────────────────────────────────────────
# PANEL A: ICP-01 Exterior (container-wall-facing) face
# ───────────────────────────────────────────────
cx_b, cy_b = 900, 1280

p2 = mpatches.Rectangle((cx_b - hw, cy_b - hw), s1(PL_OD), s1(PL_OD),
                         lw=LW_THICK, edgecolor=C_OUT, facecolor=C_ALUM, zorder=3)
ax1.add_patch(p2)

# Central bore (larger — Ø380)
draw_circle(ax1, cx_b, cy_b, s1(TSB01_BORE/2), lw=LW_THICK, color=C_OUT, fill=True, fc='white', zorder=4)

# Seal groove Ø420
draw_circle(ax1, cx_b, cy_b, s1(SEAL_D/2), lw=LW_MED, color=C_GASKT, ls='--')
# Light-trap rebate (dashed square)
tr = s1(TRAP_SQ/2)
ax1.plot([cx_b-tr, cx_b+tr, cx_b+tr, cx_b-tr, cx_b-tr],
         [cy_b-tr, cy_b-tr, cy_b+tr, cy_b+tr, cy_b-tr],
         color=C_HID, lw=LW_THIN, ls='--')

# Bolt circle
draw_circle(ax1, cx_b, cy_b, s1(BOLT_BC/2), lw=0.4, color=C_HID, ls=':')
bolt_holes(ax1, cx_b, cy_b, s1(BOLT_BC/2), BOLT_N, s1(BOLT_D/2))

# Dowel holes
for sign in [-1, 1]:
    draw_circle(ax1, cx_b + sign*s1(DWL_OFF), cy_b, s1(DWL_D/2), lw=LW_MED, color=C_OUT)

# (The adjusters are NOT in the frame — they mount on the interior bracket ring. The exterior
#  face is the clean plate interface, identical to the standard pinhole plate.)

draw_cl(ax1, cx_b, cy_b, hw*1.15)

# ── Formal dimensions — every feature (Ø + count folded onto the dim line, no leaders) ──
dia_stack(ax1, cx_b, cy_b - hw, [
    (s1(TSB01_BORE), 'Ø380 BORE (THRU)'),
    (s1(SEAL_D),     'Ø420 SEAL GROOVE · 3mm WIDE × 3mm DEEP'),
    (s1(BOLT_BC),    'Ø540 B.C. · 8× Ø13 CLR (M12) EQUISPACED'),
    (s1(PL_OD),      '600mm'),
], dirn=-1)
draw_dim_v(ax1, cx_b - hw - 30, cy_b - hw, cy_b + hw, '600mm', right=False, fs=5.5, offset=20)
ax1.text(cx_b - hw + 12, cy_b + hw - 14, '6061-T6 · 40mm THK', ha='left', va='top',
         fontsize=5, color=C_DIM, style='italic', zorder=10)
# Dowel location — ±200 on the horizontal C/L (Ø8 folded onto the +200 dim)
draw_dim_h(ax1, cx_b - s1(DWL_OFF), cx_b, cy_b, '200mm', above=True, fs=4.5, offset=13)
draw_dim_h(ax1, cx_b, cx_b + s1(DWL_OFF), cy_b, '200 · 2× Ø8 H7 DOWEL', above=True, fs=4.5, offset=13)

draw_dim_v(ax1, cx_b + hw + 30, cy_b - s1(BOLT_BC/2), cy_b + s1(BOLT_BC/2), 'Ø540 B.C. (8× M12)', right=True, fs=5, offset=16)

# ── identifying leaders for the non-obvious features (the seal groove + bolt/dowel are
#    already named on their dimension lines; the top-left corner is left for the material note) ──
leader(ax1, cx_b + s1(TRAP_SQ/2), cy_b + s1(TRAP_SQ/2),
       cx_b + hw + 10, cy_b + hw + 120, 'Ø490 SQ\nLIGHT-TRAP REBATE', fs=4.4, color=C_DIM, arrow_style='->', ha='left')
leader(ax1, cx_b + s1(BOLT_BC/2)*np.cos(np.radians(-45)), cy_b + s1(BOLT_BC/2)*np.sin(np.radians(-45)),
       cx_b + hw - 6, cy_b - hw - 30, '8× Ø13 CLR (M12)\nCONTAINER-PLATE BOLTS', fs=4.4, color=C_DIM, arrow_style='->', ha='left')

ax1.text(cx_b, cy_b - hw - 250, 'PANEL A — ICP-01 EXTERIOR (1:8)\n(Same bolt/dowel/seal interface as standard pinhole plate)',
         ha='center', fontsize=5, color='#333333', style='italic')

# ───────────────────────────────────────────────
# PANEL B: ICP-01 Interior (container-facing) face
# ───────────────────────────────────────────────
cx_c, cy_c = 2350, 1280

p3 = mpatches.Rectangle((cx_c - hw, cy_c - hw), s1(PL_OD), s1(PL_OD),
                         lw=LW_THICK, edgecolor=C_OUT, facecolor=C_ALUM, zorder=3)
ax1.add_patch(p3)

# Ø380 through-bore — CLEAR (no central bearing seat; the carrier is rim-supported)
draw_circle(ax1, cx_c, cy_c, s1(TSB01_BORE/2), lw=LW_MED, color=C_OUT, fill=True, fc='white', zorder=4)

# Labyrinth steps (3 concentric dashed circles)
for d, ls_str in [(LAB_D1,'--'),(LAB_D2,'-.'),(LAB_D3,':')]:
    draw_circle(ax1, cx_c, cy_c, s1(d/2), lw=LW_THIN, color='#555555', ls=ls_str)

# Wave-spring counterbore (Ø300 annular groove) — the ICP-03 preload spring seats here
draw_circle(ax1, cx_c, cy_c, s1((SPR_PCD + 14)/2), lw=LW_MED, color='#777777', ls='--', zorder=5)
draw_circle(ax1, cx_c, cy_c, s1((SPR_PCD - 14)/2), lw=LW_MED, color='#777777', ls='--', zorder=5)

# Bellows outer clamp ring (Al) + 6× M4 retaining screws on Ø420 — OUTSIDE the Ø400 labyrinth, on solid frame face
draw_circle(ax1, cx_c, cy_c, s1((BELL_OUT_PCD+14)/2), lw=LW_MED, color=C_OUT, zorder=5)   # ring OD
draw_circle(ax1, cx_c, cy_c, s1((BELL_OUT_PCD-14)/2), lw=LW_MED, color=C_OUT, zorder=5)   # ring ID (bellows large end seats here)
for i in range(6):
    ang = np.radians(i*60)
    bx = cx_c + s1(BELL_OUT_PCD/2) * np.cos(ang)
    by = cy_c + s1(BELL_OUT_PCD/2) * np.sin(ang)
    draw_circle(ax1, bx, by, s1(CLAMP_SCR_D/2 + 0.5), lw=LW_THIN, color=C_OUT, fill=True, fc='#888888', zorder=6)

# Adjuster-bracket-ring standoff holes (6× M5 tapped) on Ø450 — carry the ICP-03 bracket ring
for i in range(RET_BOLT_N):
    ang = np.radians(30 + i * 60)
    rx = cx_c + s1(RET_BOLT_PCD/2) * np.cos(ang)
    ry = cy_c + s1(RET_BOLT_PCD/2) * np.sin(ang)
    draw_circle(ax1, rx, ry, s1(RET_BOLT_D/2), lw=0.7, color=C_OUT, fill=True, fc='white', zorder=6)

draw_cl(ax1, cx_c, cy_c, hw*1.15)

# ── Formal dimensions — every feature ──
dia_stack(ax1, cx_c, cy_c - hw, [
    (s1(TSB01_BORE),   'Ø380 BORE (THRU) — CLEAR, no central bearing'),
    (s1(BELL_OUT_PCD), 'Ø420 PCD · 6× M4 BELLOWS CLAMP-RING SCREW (OUTSIDE LABYRINTH) · 60° APART'),
    (s1(RET_BOLT_PCD), 'Ø450 PCD · 6× M5 ADJUSTER-BRACKET-RING STANDOFF (TAPPED) · 60° APART'),
    (s1(PL_OD),        '600mm'),
], dirn=-1)
dia_stack(ax1, cx_c, cy_c + hw, [
    (s1(SPR_PCD), 'Ø300 WAVE-SPRING COUNTERBORE (14mm WIDE × 4mm DEEP)'),
    (s1(LAB_D3),  f'Ø{LAB_D1} / Ø{LAB_D2} / Ø{LAB_D3} — 3-STEP LABYRINTH · 5mm DEEP EACH'),
], dirn=+1)
draw_dim_v(ax1, cx_c + hw + 30, cy_c - hw, cy_c + hw, '600mm', right=True, fs=5.5, offset=20)
ax1.text(cx_c - hw + 12, cy_c + hw - 14, '6061-T6 · 40mm THK', ha='left', va='top',
         fontsize=5, color=C_DIM, style='italic', zorder=10)

draw_dim_v(ax1, cx_c - hw - 30, cy_c - s1(BELL_OUT_PCD/2), cy_c + s1(BELL_OUT_PCD/2), 'Ø420 (CLAMP-RING SCREWS)', right=False, fs=5, offset=16)
# ── identifying leaders ──
leader(ax1, cx_c, cy_c + s1(SPR_PCD/2), cx_c - 120, cy_c + hw - 30,
       'Ø300 WAVE-SPRING\nCOUNTERBORE', fs=4.4, color=C_DIM, arrow_style='->', ha='right')
leader(ax1, cx_c + s1(BELL_OUT_PCD/2)*np.cos(np.radians(30)), cy_c + s1(BELL_OUT_PCD/2)*np.sin(np.radians(30)),
       cx_c + 120, cy_c + hw - 20, '6× M4 BELLOWS\nCLAMP-RING SCREW', fs=4.4, color=C_DIM, arrow_style='->', ha='left')
leader(ax1, cx_c + s1(RET_BOLT_PCD/2)*np.cos(np.radians(-30)), cy_c + s1(RET_BOLT_PCD/2)*np.sin(np.radians(-30)),
       cx_c + 120, cy_c - hw + 30, '6× M5 ADJUSTER-RING\nSTANDOFF (ICP-03)', fs=4.4, color=C_DIM, arrow_style='->', ha='left')

ax1.text(cx_c, cy_c - hw - 250, 'PANEL B — ICP-01 INTERIOR (1:8)\n(Clear bore + labyrinth + bellows + spring c\'bore + adjuster-ring mounts)',
         ha='center', fontsize=5, color='#333333', style='italic')

ax1.text(FW1/2, FH1 - 60,
         'ASSEMBLY KEY — Sheet 2 (Section A-A):  ICP-01 is the OUTER FRAME — the exterior / scene-side plate.\n'
         'The Ø380 bore passes the carrier; the interior face carries the wave-spring counterbore, the 6× bracket-ring\n'
         'standoffs (ICP-03), the bellows outer clamp ring, and the 3-step labyrinth.',
         ha='center', va='top', fontsize=6, style='italic', color='#444',
         bbox=dict(boxstyle='round,pad=0.5', fc='#F4F4F4', ec='#BBBBBB', lw=0.6))

out1 = os.path.join(DIAGRAMS_DIR, 'tilt-swing-sheet3.png')
fig1.savefig(out1, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white')
plt.close(fig1)
print(f'  → {out1}  Done.')


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Carrier Plate, Bearing & Adjustment Mechanism
# ═══════════════════════════════════════════════════════════════════════════════

FW2, FH2 = 1500, 1560
fig2, ax2 = plt.subplots(figsize=(FW*0.9/25.4, FH*0.9/25.4))
fig2.patch.set_facecolor('white')
ax2.set_facecolor('white')
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_xlim(0, FW2)
ax2.set_ylim(0, FH2)

title_block(ax2, "SHEET 4 OF 7",
            drawing_title="TILT-SWING FRONT BOARD",
            subtitle="Inner Carrier, Preload & Adjustment mechanism",
            scale_note="AXES IN mm",
            doc_id="TBS-TSB · Tilt-Swing Board")

SC2 = 1
def s2(mm): return mm * SC2

# ── PANEL A: ICP-02 front (exterior) face at 1:2 ──────────────────────────────
ax2.text(30, 1540, 'PANEL A — ICP-02 FRONT FACE (1:2)', fontsize=7.5, fontweight='bold')
ax2.plot([30, 660], [1534, 1534], color='black', lw=0.7)

cx2a, cy2a = 330, 1230

# Circular carrier plate
carr_p = mpatches.Circle((cx2a, cy2a), s2(CARR_OD/2),
                          lw=LW_THICK, edgecolor=C_OUT, facecolor=C_ALUM, zorder=3)
ax2.add_patch(carr_p)

# Taper bore (Ø90 scene taper) — scene light converges through here to the pinhole
draw_circle(ax2, cx2a, cy2a, s2(PH_BORE/2), lw=LW_MED, color=C_OUT, fill=True, fc='white', zorder=4)

# Wave-spring bearing land (Ø300 annular) — the ICP-03 preload spring bears on THIS (scene) face
draw_circle(ax2, cx2a, cy2a, s2((SPR_PCD + 14)/2), lw=0.7, color='#777777', ls='--', zorder=4)
draw_circle(ax2, cx2a, cy2a, s2((SPR_PCD - 14)/2), lw=0.7, color='#777777', ls='--', zorder=4)

# Bellows inner clamp ring (Al) + 4× M4 on Ø306 — clamps the bellows small end (bellows on this face)
draw_circle(ax2, cx2a, cy2a, s2((BELL_IN_PCD+8)/2), lw=LW_MED, color=C_OUT, zorder=5)
draw_circle(ax2, cx2a, cy2a, s2((BELL_IN_PCD-8)/2), lw=LW_MED, color=C_OUT, zorder=5)
for i in range(4):
    ang = np.radians(45 + i*90)
    bx = cx2a + s2(BELL_IN_PCD/2) * np.cos(ang)
    by = cy2a + s2(BELL_IN_PCD/2) * np.sin(ang)
    draw_circle(ax2, bx, by, s2(CLAMP_SCR_D/2 + 0.5), lw=LW_THIN, color=C_OUT, fill=True, fc='#888888', zorder=6)

draw_cl(ax2, cx2a, cy2a, s2(CARR_OD/2)*1.2)

# ── Formal dimensions — every feature ──
dia_stack(ax2, cx2a, cy2a - s2(CARR_OD/2), [
    (s2(PH_BORE),     'Ø90 CONE BORE (SCENE TAPER)'),
    (s2(SPR_PCD),     'Ø300 WAVE-SPRING BEARING LAND'),
    (s2(BELL_IN_PCD), 'Ø306 PCD · 4× M4 BELLOWS CLAMP-RING SCREW · 90° APART'),
    (s2(CARR_OD),     'Ø320 CARRIER OD'),
], dirn=-1, step=42, fs=4.6, off=13)
draw_dim_v(ax2, cx2a - s2(CARR_OD/2) - 26, cy2a - s2(CARR_OD/2), cy2a + s2(CARR_OD/2), 'Ø320', right=False, fs=5, offset=16)
ax2.text(cx2a - s2(CARR_OD/2) + 8, cy2a + s2(CARR_OD/2) - 10, '6061-T6 · Ø320 × 25mm THK', ha='left', va='top', fontsize=4.6, color=C_DIM, style='italic', zorder=10)

draw_dim_v(ax2, cx2a + s2(CARR_OD/2) + 26, cy2a - s2(BELL_IN_PCD/2), cy2a + s2(BELL_IN_PCD/2), 'Ø306 (CLAMP-RING SCREWS)', right=True, fs=5, offset=14)
# ── identifying leaders ──
leader(ax2, cx2a - s2(SPR_PCD/2), cy2a, cx2a - s2(CARR_OD/2) - 12, cy2a + s2(CARR_OD/2) + 60,
       'Ø300 WAVE-SPRING\nBEARING LAND', fs=4.2, color=C_DIM, arrow_style='->', ha='center')
leader(ax2, cx2a + s2(BELL_IN_PCD/2)*0.71, cy2a + s2(BELL_IN_PCD/2)*0.71, cx2a + s2(CARR_OD/2) + 8, cy2a + s2(CARR_OD/2) + 34,
       'BELLOWS INNER CLAMP RING (4× M4)', fs=4.2, color=C_DIM, arrow_style='->', ha='left')

ax2.text(cx2a, cy2a - s2(CARR_OD/2) - 250, 'PANEL A — ICP-02 FRONT FACE (1:2)\nExterior / scene side — spring land + bellows',
         ha='center', fontsize=5, style='italic', color='#333333')

# ── PANEL B: ICP-02 rear face at 1:2 ─────────────────────────────────────────
ax2.text(770, 1540, 'PANEL B — ICP-02 REAR FACE (1:2)', fontsize=7.5, fontweight='bold')
ax2.plot([770, 1370], [1534, 1534], color='black', lw=0.7)

cx2b, cy2b = 1080, 1230

carr_p2 = mpatches.Circle((cx2b, cy2b), s2(CARR_OD/2),
                           lw=LW_THICK, edgecolor=C_OUT, facecolor='#C0C0C0', zorder=3)
ax2.add_patch(carr_p2)

# Counterbore Ø52 + pinhole disc Ø50 + pinhole — the disc mounts on THIS (camera) face
draw_circle(ax2, cx2b, cy2b, s2(PH_CB_D/2), lw=LW_MED, color=C_HID, ls='--', zorder=4)
draw_circle(ax2, cx2b, cy2b, s2(PH_DISC_D/2), lw=LW_THICK, color=C_OUT, fill=True, fc='#707070', zorder=5)
draw_circle(ax2, cx2b, cy2b, 2.0, lw=0.5, color='white', fill=True, fc='white', zorder=6)

# 4 × kinematic-seat inserts on Ø260 (cone/vee/flat) — the adjuster balls contact THIS (camera) face
_seat = {90: 'CONE', 0: 'VEE', 270: 'FLAT', 180: 'FLAT'}
for angle_deg in [90, 0, 270, 180]:
    sx = cx2b + s2(SOCK_PCD/2) * np.cos(np.radians(angle_deg))
    sy = cy2b + s2(SOCK_PCD/2) * np.sin(np.radians(angle_deg))
    draw_circle(ax2, sx, sy, s2(16/2), lw=LW_MED, color=C_OUT, fill=True, fc=C_BEAR, zorder=5)
    t = _seat[angle_deg]
    if t == 'CONE':
        draw_circle(ax2, sx, sy, s2(BALL_D/2), lw=0.7, color=C_OUT, fill=True, fc='#D0D0D0', zorder=6)
        draw_circle(ax2, sx, sy, s2(BALL_D/2)*0.45, lw=0.5, color=C_OUT, zorder=7)
    elif t == 'VEE':
        ax2.add_patch(mpatches.Rectangle((sx - s2(8), sy - s2(1.6)), s2(16), s2(3.2),
                      angle=angle_deg, rotation_point=(sx, sy), fc='#D0D0D0', ec=C_OUT, lw=0.6, zorder=6))
    else:
        draw_circle(ax2, sx, sy, s2(BALL_D/2), lw=0.7, color=C_OUT, fill=True, fc='#E8E8E8', zorder=6)
    ax2.text(sx, sy - s2(11), t, ha='center', va='top', fontsize=3.6, color=C_DIM, zorder=8)

draw_cl(ax2, cx2b, cy2b, s2(CARR_OD/2)*1.2)

# ── Formal dimensions — every feature ──
dia_stack(ax2, cx2b, cy2b - s2(CARR_OD/2), [
    (s2(PH_DISC_D),  'Ø50 PINHOLE DISC (SS-302 · Ø2.17 APT)'),
    (s2(SOCK_PCD),   'Ø260 PCD · 4× Ø16 H7 KINEMATIC SEAT (1 cone/1 vee/2 flat) · 90° APART'),
    (s2(CARR_OD),    'Ø320 CARRIER OD'),
], dirn=-1, step=42, fs=4.6, off=13)
dia_stack(ax2, cx2b, cy2b + s2(CARR_OD/2), [
    (s2(PH_CB_D), 'Ø52 × 3mm DEEP COUNTERBORE (DISC SEAT)'),
], dirn=+1, step=42, fs=4.6, off=13)
draw_dim_v(ax2, cx2b + s2(CARR_OD/2) + 26, cy2b - s2(CARR_OD/2), cy2b + s2(CARR_OD/2), 'Ø320', right=True, fs=5, offset=16)
ax2.text(cx2b - s2(CARR_OD/2) + 8, cy2b + s2(CARR_OD/2) - 10, '6061-T6 · Ø320 × 25mm THK', ha='left', va='top', fontsize=4.6, color=C_DIM, style='italic', zorder=10)

draw_dim_v(ax2, cx2b - s2(CARR_OD/2) - 26, cy2b - s2(SOCK_PCD/2), cy2b + s2(SOCK_PCD/2), 'Ø260 B.C. (4× Ø16 INSERT)', right=False, fs=5, offset=14)
# ── identifying leaders ──
leader(ax2, cx2b, cy2b + s2(SOCK_PCD/2), cx2b, cy2b + s2(CARR_OD/2) + 34,
       '4× KINEMATIC SEAT (ball contact)\n(1 cone / 1 vee / 2 flat)', fs=4.2, color=C_DIM, arrow_style='->', ha='center')
leader(ax2, cx2b + s2(PH_DISC_D/2)*0.7, cy2b - s2(PH_DISC_D/2)*0.7, cx2b + s2(CARR_OD/2) + 8, cy2b - 60,
       'Ø50 PINHOLE DISC\n(Ø2.17 aperture)', fs=4.2, color=C_DIM, arrow_style='->', ha='left')

ax2.text(cx2b, cy2b - s2(CARR_OD/2) - 250, 'PANEL B — ICP-02 REAR FACE (1:2)\nInterior / camera side — pinhole disc + kinematic seats',
         ha='center', fontsize=5, style='italic', color='#333333')

# ── PANEL C: Preload & kinematic-seat section (2:1) ───────────────────────────
ax2.text(30, 430, 'PANEL C — PRELOAD & KINEMATIC-SEAT SECTION (2:1)', fontsize=7.5, fontweight='bold')
ax2.plot([30, 690], [424, 424], color='black', lw=0.7)

cxc, cyc = 300, 215
def sc(mm): return mm * 1.5                          # panel-C local scale

# carrier rim (vertical, sectioned) — exterior (scene) face left, interior (camera) face right
cf_l = cxc - sc(6)
cf_r = cxc + sc(6)
ax2.add_patch(mpatches.Rectangle((cf_l, cyc - sc(58)), sc(12), sc(116),
              fc='#E0E0E0', ec=C_OUT, lw=LW_THICK, hatch='///', zorder=5))
# frame (far left) with a counterbore holding the wave spring
fr_x = cf_l - sc(42)
ax2.add_patch(mpatches.Rectangle((fr_x, cyc - sc(34)), sc(30), sc(68),
              fc=C_ALUM, ec=C_OUT, lw=LW_MED, hatch='\\\\\\', zorder=4))
ax2.add_patch(mpatches.Rectangle((fr_x + sc(30) - sc(6), cyc - sc(6)), sc(6), sc(12),
              fc='white', ec=C_OUT, lw=0.5, zorder=5))                      # spring counterbore
wx = np.linspace(fr_x + sc(30), cf_l, 11)                                   # wave spring
wy = [cyc + (sc(4) if k % 2 else -sc(4)) for k in range(len(wx))]
wy[0] = wy[-1] = cyc
ax2.plot(wx, wy, color=C_STEEL, lw=1.4, zorder=6)
# Ø8 ball in kinematic seat on the carrier interior (right) face
ax2.add_patch(plt.Circle((cf_r + sc(4), cyc), sc(4), fc=C_BALL, ec=C_OUT, lw=0.7, zorder=8))
ax2.plot([cf_r, cf_r - sc(4), cf_r], [cyc - sc(4.5), cyc, cyc + sc(4.5)], color=C_OUT, lw=0.9, zorder=8)  # cone (opens right)
# adjuster shank → Delrin bushing in the bracket ring → knob (interior)
rr_l = cf_r + sc(22)
ax2.add_patch(mpatches.Rectangle((cf_r + sc(8), cyc - sc(2.5)), (rr_l + sc(8)) - (cf_r + sc(8)), sc(5),
              fc=C_STEEL, ec=C_OUT, lw=0.6, zorder=7))                      # M8 adjuster shank
ax2.add_patch(mpatches.Rectangle((rr_l, cyc - sc(46)), sc(8), sc(92),
              fc=C_ALUM, ec=C_OUT, lw=LW_THICK, hatch='\\\\\\', zorder=6))  # adjuster bracket ring
ax2.add_patch(mpatches.Rectangle((rr_l, cyc - sc(6)), sc(8), sc(12),
              fc=C_DELR, ec=C_OUT, lw=0.6, zorder=8))                       # Delrin bushing in ring
ax2.add_patch(mpatches.Rectangle((rr_l + sc(8), cyc - sc(7)), sc(14), sc(14),
              fc='#333333', ec=C_OUT, lw=0.8, zorder=9))                    # knob (interior)
ax2.plot([fr_x + sc(30), rr_l], [cyc + sc(40), cyc + sc(40)], color=C_HID, lw=0.6, ls='--', zorder=4)  # standoff frame→ring
# bellows lip + clamp ring at the carrier exterior rim (top)
ax2.add_patch(mpatches.Rectangle((cf_l, cyc + sc(58)), sc(12), sc(4), fc=C_BELL, ec=C_OUT, lw=0.5, zorder=7))
ax2.add_patch(mpatches.Rectangle((cf_l + sc(1), cyc + sc(62)), sc(10), sc(7), fc=C_ALUM, ec=C_OUT, lw=0.8, hatch='\\\\\\', zorder=7))

# centerline (optical axis) — the carrier center is far below this rim joint
ax2.plot([fr_x - sc(6), fr_x + sc(8)], [cyc - sc(84), cyc - sc(84)], color=C_CL, lw=LW_THIN, ls=(0, (6, 2, 1, 2)), zorder=2)
ax2.text(fr_x - sc(6), cyc - sc(82), '↓ optical axis (Ø130 arm away)', fontsize=3.8, color='#777', style='italic', zorder=8)

# ── leaders (spread clear of the geometry) ──
leader(ax2, fr_x + sc(20), cyc + sc(4), fr_x - 8, cyc + sc(40), 'WAVE SPRING\n(frame counterbore)', fs=4.4, color=C_DIM, arrow_style='->', ha='right')
leader(ax2, cf_r + sc(4), cyc - sc(4), fr_x - 8, cyc - sc(44), 'Ø8 Gr-25 BALL\nIN 60° CONE SEAT (rear face)', fs=4.4, color=C_DIM, arrow_style='->', ha='right')
leader(ax2, rr_l + sc(15), cyc + sc(3), rr_l + sc(22), cyc - sc(70), 'M8 ADJUSTER + KNOB\n(interior — set from inside)', fs=4.4, color=C_DIM, arrow_style='->', ha='center')
leader(ax2, rr_l + sc(4), cyc - sc(30), rr_l + sc(20), cyc + sc(54), 'Al ADJUSTER BRACKET\nRING @ Ø450 · 6× M5', fs=4.4, color=C_DIM, arrow_style='->', ha='left')
leader(ax2, cf_l + sc(6), cyc + sc(64), cf_l - sc(10), cyc + sc(74), 'BELLOWS LIP\n+ CLAMP RING', fs=4.4, color=C_DIM, arrow_style='->', ha='right')

ax2.text(cxc + sc(6), cyc - sc(88), 'RIM MOUNT — carrier clamped between the frame WAVE SPRING (left) and the Ø8\n'
         'adjuster BALL on the interior bracket ring (right). No central bearing; axis clear; knobs set from inside.',
         ha='center', fontsize=4.4, style='italic', color='#333333')

# ── PANEL D: Adjustment screw detail (1:1) ────────────────────────────────────
ax2.text(720, 430, 'PANEL D — ADJUSTMENT SCREW DETAIL (1:1)', fontsize=7.5, fontweight='bold')
ax2.plot([720, 1390], [424, 424], color='black', lw=0.7)

cx2d, cy2d = 848, 260

def s1b(mm): return mm            # Panel D local scale (1:1)

# Frame boss (outer adapter frame wall in section)
frame_wall_w = s1b(35)
frame_wall_p = mpatches.Rectangle((cx2d - frame_wall_w, cy2d - s1b(30)),
                                   frame_wall_w, s1b(60),
                                   lw=LW_MED, edgecolor=C_OUT, facecolor=C_ALUM)
ax2.add_patch(frame_wall_p)

# Delrin bushing (M22×1.0 OD × M8 bore)
bush_w = s1b(BUSH_L)
bush_p = mpatches.Rectangle((cx2d - frame_wall_w, cy2d - s1b(BUSH_OD/2)),
                              bush_w, s1b(BUSH_OD),
                              lw=LW_MED, edgecolor=C_OUT, facecolor=C_DELR, zorder=4)
ax2.add_patch(bush_p)
# M8 bore through bushing
bore_p = mpatches.Rectangle((cx2d - frame_wall_w, cy2d - s1b(ADJ_D/2)),
                              bush_w, s1b(ADJ_D),
                              lw=0, facecolor='white')
ax2.add_patch(bore_p)
ax2.plot([cx2d - frame_wall_w, cx2d - frame_wall_w + bush_w],
         [cy2d - s1b(ADJ_D/2), cy2d - s1b(ADJ_D/2)], color=C_OUT, lw=LW_THIN)
ax2.plot([cx2d - frame_wall_w, cx2d - frame_wall_w + bush_w],
         [cy2d + s1b(ADJ_D/2), cy2d + s1b(ADJ_D/2)], color=C_OUT, lw=LW_THIN)

# M8 adjustment screw shaft
screw_len = s1b(80)
screw_p = mpatches.Rectangle((cx2d, cy2d - s1b(ADJ_D/2)),
                               screw_len, s1b(ADJ_D),
                               lw=LW_MED, edgecolor=C_OUT, facecolor=C_STEEL, zorder=5)
ax2.add_patch(screw_p)
# Thread representation (dashed lines)
for i in range(1, 9):
    tx = cx2d + i * screw_len/9
    ax2.plot([tx, tx], [cy2d - s1b(ADJ_D/2) - 2, cy2d + s1b(ADJ_D/2) + 2],
             color=C_HID, lw=0.4, ls='--')

# Knob at right end
knob_p = mpatches.Rectangle((cx2d + screw_len, cy2d - s1b(KNOB_D/2)),
                              s1b(KNOB_H), s1b(KNOB_D),
                              lw=LW_MED, edgecolor=C_OUT, facecolor='#797979')
ax2.add_patch(knob_p)
# Knurling lines
for i in range(6):
    ky = cy2d - s1b(KNOB_D/2) + i*s1b(KNOB_D/5) + s1b(KNOB_D/10)
    ax2.plot([cx2d + screw_len + s1b(1), cx2d + screw_len + s1b(KNOB_H) - s1b(1)],
             [ky, ky], color='#888888', lw=0.5)

# Ball at left end of screw
ball_x2 = cx2d - s1b(BALL_D/2) - s1b(2)
draw_circle(ax2, ball_x2, cy2d, s1b(BALL_D/2), fill=True, fc=C_BEAR, lw=LW_MED, color=C_OUT, zorder=6)

# Carrier plate rim (socket side)
carrier_rim_w = s1b(25)
carrier_p2 = mpatches.Rectangle((ball_x2 - carrier_rim_w, cy2d - s1b(CARR_THICK/2)),
                                  carrier_rim_w, s1b(CARR_THICK),
                                  lw=LW_THICK, edgecolor=C_OUT, facecolor='#C0C0C0', zorder=3)
ax2.add_patch(carrier_p2)
# Socket insert
sock_p = mpatches.Circle((ball_x2 - s1b(8), cy2d), s1b(8),
                           lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR, zorder=5)
ax2.add_patch(sock_p)
# Hemispherical pocket (dashed semicircle)
theta = np.linspace(0, np.pi, 30)
ax2.plot(ball_x2 - s1b(8) + s1b(BALL_D/2)*np.cos(theta),
         cy2d + s1b(BALL_D/2)*np.sin(theta),
         color=C_HID, lw=0.8, ls='--', zorder=7)

# Horizontal centerline through screw
ax2.plot([cx2d - frame_wall_w - 10, cx2d + screw_len + s1b(KNOB_H) + 10],
         [cy2d, cy2d], color=C_CL, lw=LW_THIN, linestyle=(0, (6, 2, 1, 2)))

# Dims and leaders
draw_dim_h(ax2, cx2d, cx2d + screw_len, cy2d + s1b(KNOB_D/2) + 24,
           'M8 × 1.0 × 80 SCREW', above=True, fs=5, offset=7.2)
draw_dim_h(ax2, cx2d - frame_wall_w, cx2d - frame_wall_w + bush_w,
           cy2d - s1b(KNOB_D/2) - 24, f'BUSH L={BUSH_L}mm', above=False, fs=5, offset=7.2)

leader(ax2, cx2d + screw_len + s1b(KNOB_H)/2, cy2d + s1b(KNOB_D/2),
       cx2d + screw_len + s1b(KNOB_H) + 24, cy2d + 20,
       f'Ø40 KNURLED KNOB (INTERIOR)\n{FRONT_BOARD_DETENTS}-DETENT\n{FRONT_BOARD_CLICK_DEG}°/CLICK', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, cx2d - frame_wall_w + bush_w/2, cy2d + s1b(BUSH_OD/2),
       cx2d - frame_wall_w - 58, cy2d - 2,
       'DELRIN/POM\nGUIDE BUSHING\nM22×1.0 OD', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, ball_x2 - s1b(8), cy2d - s1b(BALL_D/2),
       ball_x2 - s1b(8) - 110, cy2d - 36,
       '440C SS KINEMATIC SEAT\n(cone / vee / flat)\nRa 0.4 GROUND', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, ball_x2, cy2d + s1b(BALL_D/2),
       ball_x2 + 28, cy2d + 24,
       'Ø8 Gr25\nCHROME\nSTEEL BALL', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, ball_x2 - carrier_rim_w/2, cy2d + s1b(CARR_THICK/2),
       ball_x2 - carrier_rim_w - 100, cy2d + 100,
       'ICP-02\nCARRIER RIM', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, cx2d - frame_wall_w/2, cy2d - s1b(30),
       cx2d - frame_wall_w - 40, cy2d - s1b(30) - 30,
       'ICP-03 ADJUSTER\nBRACKET RING', fs=5, color=C_DIM, arrow_style='->', ha='right')

# Angular resolution table — top right of Panel D
tbl_x, tbl_y = 1160, 414
ax2.text(tbl_x, tbl_y, 'ANGULAR RESOLUTION', fontsize=6, fontweight='bold', color='black')
rows = [
    ('Arm radius (pivot→ball)', '130mm'),
    ('Screw pitch', f'{FRONT_BOARD_SCREW_PITCH}mm / turn'),
    ('Linear travel ÷ arm', '1/130 rad/mm = 0.0077°/mm'),
    ('Resolution per turn', '0.44° / turn'),
    ('Detents per turn', f'{FRONT_BOARD_DETENTS}'),
    ('Resolution per click', f'{FRONT_BOARD_CLICK_DEG}° / click'),
    ('Full ±5° range', '~410 clicks (11.4 turns)'),
    ('Hard stop travel', f'±{FRONT_BOARD_TRAVEL_MM}mm = ±{FRONT_BOARD_MAX_DEG}°'),
]
for i, (k, v) in enumerate(rows):
    ry = tbl_y - 20 - i*18
    bg = '#F8F8F8' if i%2==0 else 'white'
    draw_rect(ax2, tbl_x - 4, ry - 14, 220, 18, lw=0.15, color='#DDDDDD', fc=bg, zorder=1)
    ax2.text(tbl_x, ry, k, fontsize=4.5, color='black', zorder=10)
    ax2.text(tbl_x + 136, ry, v, fontsize=4.5, color='black', fontweight='bold', zorder=10)

ax2.text(FW2/2, 640,
         'ASSEMBLY KEY — Sheet 2 (Section A-A):  the ICP-02 carrier sits in the Ø380 bore.  FRONT / scene face (Panel A) =\n'
         'wave-spring land + bellows;  REAR / camera face (Panel B) = pinhole disc + the 4 kinematic seats.  ICP-03 = the wave\n'
         'spring in the frame counterbore (scene side) + the interior adjuster bracket ring that carries the knobs (Panels C / D).',
         ha='center', va='center', fontsize=5.6, style='italic', color='#444',
         bbox=dict(boxstyle='round,pad=0.5', fc='#F4F4F4', ec='#BBBBBB', lw=0.6))

out2 = os.path.join(DIAGRAMS_DIR, 'tilt-swing-sheet4.png')
fig2.savefig(out2, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white')
plt.close(fig2)
print(f'  → {out2}  Done.')


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 5 — Bellows seal, Locking & Calibration scale
# ═══════════════════════════════════════════════════════════════════════════════

FH3_FIG = int(FH * 1.3)
FW3, FH3 = 1400, 880
fig3, ax3 = plt.subplots(figsize=(FW/25.4*0.9, FH3_FIG/25.4*0.9))
fig3.patch.set_facecolor('white')
ax3.set_facecolor('white')
ax3.set_aspect('equal')
ax3.axis('off')
ax3.set_xlim(0, FW3)
# Lower bound raised to ~190 (was 0) so the title block — anchored in axes-fraction at the
# bottom — re-seats just under Panels B/C/D now that Panel E (the swap procedure) is gone;
# tight-bbox then crops the former Panel E band.
ax3.set_ylim(190, FH3)
S3_UP = 40  # panels fill from the top; fixed (was FH3-FH2, which broke when Sheet 4's FH2 changed)

title_block(ax3, "SHEET 5 OF 7",
            drawing_title="TILT-SWING FRONT BOARD",
            subtitle="Bellows seal, Locking & Calibration scale",
            scale_note="AXES IN mm",
            doc_id="TBS-TSB · Tilt-Swing Board")

# ── PANEL A: Bellows section at 0° and 5° tilt ────────────────────────────────
ax3.text(30, 760 + S3_UP, 'PANEL A — BELLOWS SECTION: NEUTRAL (solid) & 5° TILT (dashed) (1:2)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([30, 960], [754 + S3_UP, 754 + S3_UP], color='black', lw=0.7)

cx3a, cy3a = 400, 640 + S3_UP

def draw_bellows_section(ax, cx, cy, tilt_deg, lw_style='-', alpha=1.0):
    """Draw bellows accordion cross-section for given tilt angle."""
    tilt = np.radians(tilt_deg)
    # Bellows geometry: outer attach at ±BELL_OD/2 radius, inner attach at ±BELL_ID/2
    # Free length BELL_FREE mm, drawn at 1:2 scale
    sc_b = 0.5
    r_out = s2(BELL_OD/2)
    r_in  = s2(BELL_ID/2)
    L     = s2(BELL_FREE)
    # At tilt angle, inner plate (bottom of bellows) tilts:
    # left side of inner: cx - r_in, compresses; right side: cx + r_in, extends
    delta = r_in * np.tan(tilt)  # asymmetric vertical offset at inner radius
    # Draw outline of bellows cross-section as two mirrored accordion strips
    for side in [-1, 1]:  # left and right
        x_out = cx + side * r_out  # fixed outer attachment
        x_in  = cx + side * r_in   # tilted inner attachment
        # Inner Y position offset by tilt
        y_inner = cy - L + side * delta
        n_p = BELL_PLEATS
        # Pleat points: alternating between outer and inner radii
        pts_x, pts_y = [x_out], [cy]
        for j in range(n_p):
            frac = (j + 0.5) / n_p
            y_mid = cy - frac * L
            if j % 2 == 0:
                pts_x.append(x_out + side * s2(BELL_PLEAT_D))
            else:
                pts_x.append(x_out - side * s2(BELL_PLEAT_D * 0.5))
            pts_y.append(y_mid + side * delta * frac * 0.5)
        pts_x.append(x_in)
        pts_y.append(y_inner)
        col = C_BELL if lw_style == '-' else '#808080'
        ax.plot(pts_x, pts_y, color=col, lw=1.5 if lw_style=='-' else 1.0,
                linestyle=lw_style, alpha=alpha)
    # Top attachment line (outer frame edge)
    ax.plot([cx - r_out, cx + r_out], [cy, cy], color='black', lw=1.5 if lw_style=='-' else 1.0,
            linestyle=lw_style, alpha=alpha)
    # Bottom attachment line (carrier plate, tilted)
    y_left  = cy - L - delta
    y_right = cy - L + delta
    ax.plot([cx - r_in, cx + r_in], [y_left, y_right],
            color='black', lw=1.5 if lw_style=='-' else 1.0, linestyle=lw_style, alpha=alpha)

# 0° (solid)
draw_bellows_section(ax3, cx3a, cy3a, 0, lw_style='-')
# 5° (dashed)
draw_bellows_section(ax3, cx3a, cy3a, 5, lw_style='--', alpha=0.7)

# Context: outer frame and carrier plate in section
frame_bar_h = s2(10)
draw_rect(ax3, cx3a - s2(BELL_OD/2) - 30, cy3a, 30 + s2(BELL_OD) + 30, frame_bar_h,
          lw=LW_MED, color=C_OUT, fc=C_ALUM)
ax3.text(cx3a, cy3a + frame_bar_h/2, 'ICP-01 OUTER FRAME', ha='center', va='center', fontsize=4.5, color='black', zorder=10)

carr_bar_h = s2(10)
# Neutral position carrier
draw_rect(ax3, cx3a - s2(BELL_ID/2) - 20, cy3a - s2(BELL_FREE) - carr_bar_h,
          s2(BELL_ID) + 40, carr_bar_h, lw=LW_MED, color=C_OUT, fc='#C0C0C0')
ax3.text(cx3a, cy3a - s2(BELL_FREE) - carr_bar_h/2,
         'ICP-02 CARRIER (NEUTRAL)', ha='center', va='center', fontsize=4.5, color='black', zorder=10)

# Dimensions
draw_dim_v(ax3, cx3a + s2(BELL_OD/2) + 30, cy3a - s2(BELL_FREE), cy3a,
           f'{BELL_FREE}mm FREE LEN', right=True, fs=5, offset=9)
draw_dim_h(ax3, cx3a - s2(BELL_OD/2), cx3a + s2(BELL_OD/2), cy3a + frame_bar_h + 28,
           f'Ø{BELL_OD} FRAME END (clamps outside labyrinth)', above=True, fs=5, offset=9)
draw_dim_h(ax3, cx3a - s2(BELL_ID/2), cx3a + s2(BELL_ID/2),
           cy3a - s2(BELL_FREE) - carr_bar_h - 28, f'Ø{BELL_ID} CARRIER END', above=False, fs=5, offset=9)

ax3.text(cx3a + s2(BELL_OD/2) + 104, cy3a - s2(BELL_FREE*0.5),
         '——— NEUTRAL (0°)\n- - - - 5° TILT\n(asymmetric compression\nleft side: −13.9mm\nright side: +13.9mm)',
         fontsize=5, va='center', color='#333333', zorder=10)

ax3.text(cx3a, cy3a - s2(BELL_FREE) - carr_bar_h - 60,
         'BELLOWS ICP-04: Matte black neoprene/nylon  •  truncated cone Ø290→Ø430  •  0.5mm wall  •  4 pleats  •  15mm pleat depth\nBoth ends CLAMP-RING retained (Al ring + M4 screws) onto a Ø3mm neoprene cord gasket — carrier @ Ø306, frame @ Ø420 (outside the labyrinth)',
         ha='center', fontsize=5, style='italic', color='#333333', zorder=10)

# ── PANEL B: Adjustment-screw lock detail (2:1) ──────────────────────────────
# The M6 nylon-tip set screw jams the M8 ADJUSTMENT screw's thread so a set angle can't
# back off. It locks the SCREW, not the plates — the carrier is held by the central bearing.
ax3.text(30, 490 + S3_UP, 'PANEL B — ADJUSTMENT-SCREW LOCK (2:1)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([30, 400], [484 + S3_UP, 484 + S3_UP], color='black', lw=0.7)

cx3b, cy3b = 175, 375 + S3_UP
def sb(mm): return mm * 2.0

# ICP-01 frame boss (aluminum, sectioned) — the M8 threads through it via the Delrin bushing
boss_l, boss_r = cx3b - sb(20), cx3b + sb(18)
boss_b, boss_t = cy3b - sb(20), cy3b + sb(22)
ax3.add_patch(mpatches.Rectangle((boss_l, boss_b), boss_r - boss_l, boss_t - boss_b,
              lw=LW_THICK, edgecolor=C_OUT, facecolor=C_ALUM, hatch='///', zorder=3))

# Delrin bushing (M22 OD, internally M8×1.0) carrying the adjustment screw thread
ax3.add_patch(mpatches.Rectangle((boss_l, cy3b - sb(11)), (cx3b + sb(4)) - boss_l, sb(22),
              lw=LW_MED, edgecolor=C_OUT, facecolor=C_DELRIN, zorder=4))

# M8 adjustment screw — horizontal shank, steel, with thread crests (dashed, set convention)
m8_l, m8_r = cx3b - sb(46), cx3b + sb(36)
ax3.add_patch(mpatches.Rectangle((m8_l, cy3b - sb(4)), m8_r - m8_l, sb(8),
              lw=LW_MED, edgecolor=C_OUT, facecolor=C_STEEL, zorder=6))
for tx in np.arange(m8_l + sb(3), m8_r, sb(3)):     # thread crests ⟂ to the screw axis
    ax3.plot([tx, tx], [cy3b - sb(4) - 1.5, cy3b + sb(4) + 1.5], color=C_HID, lw=0.4, ls='--', zorder=6)
# knob stub (exterior end) + carrier ball (interior end)
ax3.add_patch(mpatches.Rectangle((m8_l - sb(9), cy3b - sb(9)), sb(9), sb(18),
              lw=LW_MED, edgecolor=C_OUT, facecolor='#797979', zorder=6))
draw_circle(ax3, m8_r + sb(3), cy3b, sb(4), fill=True, fc=C_BEAR, lw=LW_MED, color=C_OUT, zorder=7)

# M6 nylon-tip set screw — vertical, in a tapped cross-hole in the boss, tip jamming the M8 thread
m6_x = cx3b - sb(2)
ax3.add_patch(mpatches.Rectangle((m6_x - sb(3), cy3b + sb(4)), sb(6), sb(24),
              lw=LW_MED, edgecolor=C_OUT, facecolor=C_STEEL, zorder=8))
for ty in np.arange(cy3b + sb(7), cy3b + sb(22), sb(3)):   # set-screw thread crests
    ax3.plot([m6_x - sb(3) - 1.5, m6_x + sb(3) + 1.5], [ty, ty], color=C_HID, lw=0.4, ls='--', zorder=8)
ax3.add_patch(mpatches.Rectangle((m6_x - sb(2.5), cy3b + sb(4)), sb(5), sb(4),
              lw=0.5, edgecolor=C_OUT, facecolor='#F0E080', zorder=9))   # nylon tip on the M8 thread
# 3mm hex socket in the set-screw top
ax3.add_patch(mpatches.Rectangle((m6_x - sb(1.6), cy3b + sb(24) - sb(3)), sb(3.2), sb(3),
              lw=0.4, edgecolor=C_OUT, facecolor='white', zorder=10))

# ── leaders — right-stacked, ordered by feature height so the leader lines don't cross ──
LBX = m8_r + sb(20)                                 # common label column, clear of the ball
leader(ax3, m6_x + sb(2), cy3b + sb(22), LBX, cy3b + sb(30),
       'M6×1.0 NYLON-TIP\nSET SCREW (3mm hex)', fs=4.6, color=C_DIM, arrow_style='->', ha='left')
leader(ax3, m6_x, cy3b + sb(6), LBX, cy3b + sb(10),
       'NYLON TIP —\njams the M8 thread', fs=4.6, color=C_DIM, arrow_style='->', ha='left')
leader(ax3, m8_r + sb(3), cy3b, LBX, cy3b - sb(10),
       'M8×1.0 ADJUSTMENT SCREW\n→ carrier ball contact', fs=4.6, color=C_DIM, arrow_style='->', ha='left')
leader(ax3, boss_r - sb(3), boss_b + sb(4), LBX, cy3b - sb(30),
       'ICP-01 FRAME BOSS\n(Delrin M8 bushing, green)', fs=4.6, color=C_DIM, arrow_style='->', ha='left')

ax3.text(cx3b, cy3b - sb(42),
         'Set the angle with the knob, then tighten the M6 set screw — its nylon tip grips the M8 thread\n'
         '(threaded through the Delrin bushing) and locks the screw against back-off; nylon does not mar the\n'
         'thread. 4 off, one per axis. This locks the SET ANGLE only — the carrier is held to the frame by the\n'
         'central bearing (Panel A / Sheet 2), not by these screws.',
         ha='center', va='top', fontsize=4.6, style='italic', color='#333333', zorder=10)

# ── PANEL C: Knob detail (2:1) ────────────────────────────────────────────────
ax3.text(430, 490 + S3_UP, 'PANEL C — KNOB DETAIL (2:1)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([430, 840], [484 + S3_UP, 484 + S3_UP], color='black', lw=0.7)

cx3c, cy3c = 610, 350 + S3_UP
SC_knob = 4.0
def sk(mm): return mm * SC_knob

# Knob in section view
knob_rec = mpatches.Rectangle((cx3c - sk(KNOB_H/2), cy3c - sk(KNOB_D/2)),
                                sk(KNOB_H), sk(KNOB_D),
                                lw=LW_THICK, edgecolor=C_OUT, facecolor='#797979')
ax3.add_patch(knob_rec)
# M8 bore through knob
knob_bore = mpatches.Rectangle((cx3c - sk(KNOB_H/2), cy3c - sk(ADJ_D/2)),
                                 sk(KNOB_H), sk(ADJ_D),
                                 lw=0, facecolor='white')
ax3.add_patch(knob_bore)
ax3.plot([cx3c - sk(KNOB_H/2), cx3c + sk(KNOB_H/2)], [cy3c - sk(ADJ_D/2)]*2, color=C_OUT, lw=LW_THIN)
ax3.plot([cx3c - sk(KNOB_H/2), cx3c + sk(KNOB_H/2)], [cy3c + sk(ADJ_D/2)]*2, color=C_OUT, lw=LW_THIN)
# Flat/keyway on bore (anti-rotation)
flat_p = mpatches.Rectangle((cx3c - sk(KNOB_H/2), cy3c + sk(ADJ_D/2 - 1.5)),
                              sk(KNOB_H), sk(1.5),
                              lw=0, facecolor='#797979')
ax3.add_patch(flat_p)
# Detent ball pocket (one shown)
det_x = cx3c + sk(KNOB_H/2) - sk(2)
draw_circle(ax3, det_x, cy3c + sk(KNOB_D/2) - sk(2), sk(1.5),
            fill=True, fc='white', lw=LW_THIN, color=C_OUT)
# Knurling on OD
for i in range(8):
    kang = np.radians(i * 22.5)
    kx = cx3c + sk(KNOB_H/2 - 1.5) * np.cos(kang)
    ky = cy3c + sk(KNOB_D/2 - 1.5) * np.sin(kang)
    # just line marks on top/bottom
for ky_off in np.linspace(-sk(KNOB_D/2)*0.9, sk(KNOB_D/2)*0.9, 10):
    ax3.plot([cx3c - sk(KNOB_H/2) + sk(1), cx3c + sk(KNOB_H/2) - sk(1)],
             [cy3c + ky_off, cy3c + ky_off], color='#888888', lw=0.4)
# Label engraved on face (top)
ax3.text(cx3c, cy3c + sk(KNOB_D/2) + 10, '"TILT +"', fontsize=5, ha='center',
         color='#333333', style='italic', zorder=10)

draw_dim_h(ax3, cx3c - sk(KNOB_H/2), cx3c + sk(KNOB_H/2),
           cy3c - sk(KNOB_D/2) - 24, f'{KNOB_H}mm WIDE', above=False, fs=5, offset=6)
draw_dim_v(ax3, cx3c + sk(KNOB_H/2) + 24, cy3c - sk(KNOB_D/2), cy3c + sk(KNOB_D/2),
           f'Ø{KNOB_D}', right=True, fs=5, offset=6)

leader(ax3, det_x, cy3c + sk(KNOB_D/2) - sk(2),
       cx3c + 110, cy3c + 24,
       '36-DETENT\nSPRING BALL\n(5° PER CLICK)', fs=5, color=C_DIM, arrow_style='->')
leader(ax3, cx3c + sk(3), cy3c + sk(ADJ_D/2 - 1.5),
       cx3c + 120, cy3c - 46,
       'FLAT/KEYWAY\n(ANTI-SPIN)', fs=5, color=C_DIM, arrow_style='->')

ax3.text(cx3c, cy3c - sk(KNOB_D/2) - 56,
         'Black anodize = TILT axis  |  Natural anodize = SWING axis\nEngraved label on knob face: TILT+ / TILT− / SWING+ / SWING−',
         ha='center', fontsize=5, style='italic', color='#333333', zorder=10)

# ── PANEL D: Angular scale layout ─────────────────────────────────────────────
ax3.text(860, 490 + S3_UP, 'PANEL D — ANGULAR CALIBRATION SCALE (1:1)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([860, 1390], [484 + S3_UP, 484 + S3_UP], color='black', lw=0.7)

cx3d, cy3d = 1060, 350 + S3_UP
arm = 130  # mm arm radius
scale_w_mm = 80  # scale total width in mm

ax3.text(cx3d, 480 + S3_UP, 'Non-linear (tangent) scale: position = 80 × tan(θ)/tan(5°) mm',
         ha='center', fontsize=5, color='#333333', style='italic', zorder=10)

# Draw the scale strip
scale_strip_w = 160
scale_strip_h = 24
draw_rect(ax3, cx3d - scale_strip_w/2, cy3d - scale_strip_h/2,
          scale_strip_w, scale_strip_h, lw=LW_MED, color=C_OUT, fc='#F8F8F8')

# Tick marks (tan-scale)
for deg in np.arange(-5, 5.5, 0.5):
    x_pos = cx3d + scale_strip_w/2 * (np.tan(np.radians(deg)) / np.tan(np.radians(5)))
    is_major = (deg == round(deg))
    tick_h = scale_strip_h * 0.6 if is_major else scale_strip_h * 0.3
    ax3.plot([x_pos, x_pos],
             [cy3d + scale_strip_h/2 - tick_h, cy3d + scale_strip_h/2],
             color='black', lw=1.0 if is_major else 0.5)
    if is_major:
        ax3.text(x_pos, cy3d - scale_strip_h/2 - 6, f'{deg:+.0f}°',
                 ha='center', va='top', fontsize=4.5, color='black', zorder=10)

ax3.text(cx3d, cy3d, '0', ha='center', va='center', fontsize=6, fontweight='bold', color=C_RED, zorder=10)
ax3.plot([cx3d, cx3d], [cy3d - scale_strip_h/2, cy3d + scale_strip_h/2],
         color=C_RED, lw=1.0)

draw_dim_h(ax3, cx3d - scale_strip_w/2, cx3d + scale_strip_w/2,
           cy3d + scale_strip_h/2 + 20, '80mm TOTAL', above=True, fs=5, offset=6)
draw_dim_v(ax3, cx3d + scale_strip_w/2 + 24, cy3d - scale_strip_h/2, cy3d + scale_strip_h/2,
           '15mm (× 2mm THK)', right=True, fs=5, offset=6)
ax3.text(cx3d, cy3d - scale_strip_h/2 - 40,
         '2 off — one for TILT, one for SWING\nLaser-engraved Al 80×15×2mm  •  Mounted on ICP-01 face adjacent to each knob pair',
         ha='center', fontsize=5, style='italic', color='#333333', zorder=10)

# The plate-swap procedure is an operating step, not a fabrication feature — it lives as
# the numbered §8 "Plate Swap Procedure" in tilt-swing-board-report.md, not on this sheet.

# ── Pointer to the operating procedure (keeps the swap discoverable from the drawing set) ──
ax3.text(30, 250 + S3_UP, 'PLATE SWAP: see §8 "Plate Swap Procedure" in the Tilt-Swing Front Board report',
         fontsize=6, style='italic', color='#555555', zorder=10)

ax3.text(FW3/2, 855,
         'ASSEMBLY KEY — Sheet 2 (Section A-A):  the ICP-04 bellows spans the frame↔carrier rim gap on the scene side; the M6 '
         'locking set screws sit on the interior\nadjuster bracket ring (ICP-03); the laser-engraved calibration scales mount on '
         'the ICP-01 interior face beside each knob pair.',
         ha='center', va='top', fontsize=5.6, style='italic', color='#444',
         bbox=dict(boxstyle='round,pad=0.5', fc='#F4F4F4', ec='#BBBBBB', lw=0.6), zorder=12)

out3 = os.path.join(DIAGRAMS_DIR, 'tilt-swing-sheet5.png')
fig3.savefig(out3, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white')
plt.close(fig3)
print(f'  → {out3}  Done.')


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 6 — Bellows Attachment (clamp-ring joint details)
# ═══════════════════════════════════════════════════════════════════════════════

FW6, FH6 = 3400, 2320
fig4, ax4 = plt.subplots(figsize=(FW*0.9/25.4, FH*0.9/25.4))
fig4.patch.set_facecolor('white')
ax4.set_facecolor('white')
ax4.set_aspect('equal')
ax4.axis('off')
ax4.set_xlim(0, FW6)
ax4.set_ylim(0, FH6)

title_block(ax4, "SHEET 6 OF 7",
            drawing_title="TILT-SWING FRONT BOARD",
            subtitle="Bellows attachment — clamp-ring joint details (enlarged sections)",
            scale_note="AXES IN mm",
            doc_id="TBS-TSB · Tilt-Swing Board")

section_label(ax4, 560, 2050, 'DETAIL A — FRAME-END CLAMP JOINT (4:1)')
section_label(ax4, 2010, 2050, 'DETAIL B — CARRIER-END CLAMP JOINT (4:1)')


def draw_clamp_joint(ax, ox, oy, sc, plate_ident, tap_deep,
                     show_labyrinth, pcd_note, inboard_note):
    """Enlarged radial section through one bellows clamp-ring joint.

    ox,oy = M4 screw axis × plate interior (bellows-side) face. The plate is drawn
    broken-off below (partial section) so the clamp sandwich is the visual focus.
    Left = inboard (toward the optical aperture); right = outboard (toward the rim).
    Order across the face: [aperture side] · cord gasket · M4 screw · lip edge · [rim].
    """
    def u(mm): return mm * sc  # mm → axis units at this detail's scale

    face = oy
    show = 15  # mm of plate shown before the break line
    x_in, x_out = ox - u(30), ox + u(16)
    # ── plate body, broken off below (partial section, hatched aluminum) ──
    zig = []
    nz = 10
    for k in range(nz + 1):
        zig.append((x_out - (x_out - x_in) * k / nz, face - u(show) + (6 if k % 2 else -6)))
    ax.add_patch(mpatches.Polygon([(x_in, face), (x_out, face)] + zig, closed=True,
                 lw=LW_THICK, edgecolor=C_OUT, facecolor='white', hatch='///', zorder=3))

    # ── labyrinth teeth (frame) or nothing (carrier), inboard of the lip ──
    if show_labyrinth:
        for k in range(3):
            gx = ox - u(15) - k * u(5)
            ax.add_patch(mpatches.Rectangle((gx - u(3), face - u(5)), u(3), u(5),
                         lw=LW_THIN, edgecolor=C_OUT, facecolor='white', zorder=4))
    # bellows accordion continues inboard (first pleat rising away from the flat lip)
    px = ox - u(12)
    ax.plot([px, px - u(4), px - u(1), px - u(5)],
            [face + u(2), face + u(7), face + u(12), face + u(17)],
            color=C_BELL, lw=1.6, zorder=6)

    # ── Ø3 neoprene cord gasket, in a groove in the plate face, inboard of the screw ──
    gx = ox - u(7)
    ax.add_patch(mpatches.Rectangle((gx - u(1.6), face - u(1.6)), u(3.2), u(1.6),
                 lw=LW_THIN, edgecolor=C_OUT, facecolor='white', zorder=4))
    ax.add_patch(mpatches.Circle((gx, face + u(0.2)), u(1.5),
                 lw=LW_THIN, edgecolor=C_OUT, facecolor=C_GASKT, zorder=7))

    # ── bellows flat lip (neoprene), draped over the gasket onto the face ──
    lip_l, lip_r = ox - u(12), ox + u(11)
    ax.add_patch(mpatches.Rectangle((lip_l, face), lip_r - lip_l, u(2),
                 lw=LW_MED, edgecolor=C_OUT, facecolor=C_BELL, zorder=5))

    # ── aluminum clamp ring on top of the lip ──
    ring_l, ring_r = ox - u(7), ox + u(7)
    ax.add_patch(mpatches.Rectangle((ring_l, face + u(2)), ring_r - ring_l, u(8),
                 lw=LW_THICK, edgecolor=C_OUT, facecolor=C_ALUM, hatch='\\\\\\', zorder=6))

    # ── M4 SHCS in section — filled shank + dashed thread lines across the engaged length
    #    (same convention as the M8 screw on Sheet 4 Panel D), socket-head cap with a hex-socket
    #    recess. The tapped hole is drilled ~2mm deeper than the thread (standard blind-tap). ──
    sh = u(2)                                         # M4 shank half-width
    shank_top = face + u(10)                          # underside of the cap head (proud of the ring)
    ax.add_patch(mpatches.Rectangle((ox - sh, face - u(tap_deep)), 2 * sh, u(tap_deep) + (shank_top - face),
                 lw=LW_MED, edgecolor=C_OUT, facecolor=C_STEEL, zorder=8))
    for t in range(1, tap_deep + 1):                  # thread crests — dashed, ⟂ to the screw axis
        yy = face - u(t)
        ax.plot([ox - sh - u(0.5), ox + sh + u(0.5)], [yy, yy], color=C_HID, lw=0.4, ls='--', zorder=8)
    # drilled-deeper relief below the last thread
    ax.add_patch(mpatches.Rectangle((ox - sh, face - u(tap_deep) - u(2)), 2 * sh, u(2),
                 lw=LW_THIN, edgecolor=C_OUT, facecolor='white', zorder=7))
    # socket-head cap (1.75·D wide × D tall) with the hex-socket recess shown
    ax.add_patch(mpatches.Rectangle((ox - u(3.5), shank_top), u(7), u(4),
                 lw=LW_THICK, edgecolor=C_OUT, facecolor=C_STEEL, zorder=9))
    ax.add_patch(mpatches.Rectangle((ox - u(1.6), shank_top + u(1.2)), u(3.2), u(2.8),
                 lw=LW_THIN, edgecolor=C_OUT, facecolor='white', zorder=10))  # hex socket recess

    # ── leaders (spread so leader lines don't cross) ──
    leader(ax, ox + u(3.5), face + u(12), ox + u(30), face + u(42),
           'M4×0.7 SHCS\n(SS A2-70)', fs=4.8, color=C_DIM, arrow_style='->', ha='left')
    leader(ax, ox + u(9), face + u(1), ox + u(26), face + u(9),
           'ICP-04 BELLOWS LIP\n(neoprene · clamped flat)', fs=4.8, color=C_DIM, arrow_style='->', ha='left')
    leader(ax, ox - u(5), face + u(6), ox - u(26), face + u(28),
           '6061 CLAMP RING\n14mm WIDE × 8mm THK', fs=4.8, color=C_DIM, arrow_style='->', ha='right')
    leader(ax, gx, face + u(0.2), ox - u(31), face + u(7),
           'Ø3 NEOPRENE CORD\nGASKET — LIGHT SEAL', fs=4.8, color=C_DIM, arrow_style='->', ha='right')
    leader(ax, ox + u(2), face - u(tap_deep), ox + u(24), face - u(tap_deep) - u(4),
           f'M4×0.7 TAPPED\n{tap_deep} DEEP', fs=4.8, color=C_DIM, arrow_style='->', ha='left')
    lbox = dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none')
    if show_labyrinth:
        leader(ax, ox - u(19), face - u(2), ox - u(33), face - u(16),
               f'3-STEP LABYRINTH\nØ{LAB_D1}/{LAB_D2}/{LAB_D3} · 5mm DEEP\n(secondary light seal)', fs=4.6, color=C_DIM, arrow_style='->', ha='right', bbox=lbox)
    else:
        leader(ax, px, face - u(1), ox - u(33), face - u(16),
               inboard_note, fs=4.6, color=C_DIM, arrow_style='->', ha='right', bbox=lbox)

    # ── identity + PCD notes under the broken plate ──
    ax.text(ox - u(7), face - u(show) - 24, plate_ident, ha='center', va='top',
            fontsize=5.2, color='black', fontweight='bold', zorder=11)
    ax.text(ox - u(7), face - u(show) - 78, pcd_note, ha='center', va='top',
            fontsize=4.8, color='#333333', style='italic', zorder=11)


SC6 = 15  # units per mm (4:1 enlarged joint)
draw_clamp_joint(ax4, 820, 1300, SC6,
                 'ICP-01 FRAME — 6061-T6 · 40mm THK', 8, True,
                 '6× M4 @ Ø420 PCD · 60° APART\n(on solid face, outside the Ø400 labyrinth)', '')
draw_clamp_joint(ax4, 2280, 1300, SC6,
                 'ICP-02 CARRIER — 6061-T6 · 25mm THK', 8, False,
                 '4× M4 @ Ø306 PCD · 90° APART\n(8 to Ø290 bellows ID · 7 to Ø320 rim)',
                 'Ø290 BELLOWS ID\n(aperture side)')

# ── Exploded assembly stack (bottom-left) ─────────────────────────────────────
section_label(ax4, 560, 830, 'ASSEMBLY STACK (exploded, frame end)')
esx = 760
layers = [
    (150, C_STEEL, '////', 'M4×0.7 SHCS (SS A2-70) — 2.5 N·m'),
    (110, C_ALUM,  '\\\\\\\\', '6061 clamp ring · 14 wide × 8 thk'),
    (70,  C_BELL,  '',      'ICP-04 bellows neoprene lip'),
    (34,  C_GASKT, '',      'Ø3 neoprene cord gasket (light seal)'),
    (-40, C_ALUM,  '////', 'ICP-01 frame face — M4×0.7 tapped 8 deep'),
]
bar_w = 240
for ly, fc, ht, lbl in layers:
    yb = 620 + ly
    h = 34 if ly >= 0 else 60
    ax4.add_patch(mpatches.Rectangle((esx - bar_w/2, yb), bar_w, h,
                  lw=LW_MED, edgecolor=C_OUT, facecolor=fc, hatch=ht, zorder=5))
    ax4.text(esx + bar_w/2 + 24, yb + h/2, lbl, ha='left', va='center',
             fontsize=5, color='#222222', zorder=10)
ax4.annotate('', xy=(esx, 600), xytext=(esx, 800),
             arrowprops=dict(arrowstyle='-|>', color=C_HID, lw=1.4, ls=(0, (4, 3))))

# ── Assembly notes (bottom-right) ─────────────────────────────────────────────
section_label(ax4, 2010, 830, 'ATTACHMENT NOTES')
notes = [
    '1.  Both bellows ends land on a FLAT face — the frame lip sits outside the',
    '     Ø400 labyrinth, the carrier lip between the Ø290 ID and the Ø320 rim.',
    '2.  Ø3 neoprene cord gasket seats in a 3-wide × 1.5-deep groove INBOARD of',
    '     the screw ring, so the light seal is unbroken by the fasteners.',
    '3.  Clamp ring compresses the neoprene lip ~30% onto the cord — do not over-',
    '     torque (2.5 N·m); the seal is compression, not thread, sealed.',
    '4.  Screws: frame 6× M4 @ Ø420 (60° apart) · carrier 4× M4 @ Ø306 (90° apart),',
    '     SS A2-70 SHCS into M4×0.7 tapped holes, 8 deep, blind (no through-holes).',
    '5.  Clamp rings 6061-T6, laser/water-jet from 8mm plate; deburr bore edge that',
    '     contacts the neoprene lip.',
]
for i, ln in enumerate(notes):
    ax4.text(2030, 760 - i * 58, ln, ha='left', va='top', fontsize=5.2, color='#222222', zorder=10)

ax4.text(FW6/2, FH6 - 60,
         'ASSEMBLY KEY — Sheet 2 (Section A-A):  these are the two ICP-04 bellows clamp joints — the FRAME end (Ø420,\n'
         'outside the labyrinth) and the CARRIER end (Ø306) — both in the frame↔carrier gap on the scene side.',
         ha='center', va='top', fontsize=6, style='italic', color='#444',
         bbox=dict(boxstyle='round,pad=0.5', fc='#F4F4F4', ec='#BBBBBB', lw=0.6), zorder=12)

out4 = os.path.join(DIAGRAMS_DIR, 'tilt-swing-sheet6.png')
fig4.savefig(out4, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white')
plt.close(fig4)
print(f'  → {out4}  Done.')


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 7 — Adjuster Bracket Ring (ICP-03) + Kinematic-Seat Inserts (ICP-05)
# ═══════════════════════════════════════════════════════════════════════════════

FW7, FH7 = 3400, 2320
fig5, ax5 = plt.subplots(figsize=(FW*0.9/25.4, FH*0.9/25.4))
fig5.patch.set_facecolor('white')
ax5.set_facecolor('white')
ax5.set_aspect('equal')
ax5.axis('off')
ax5.set_xlim(0, FW7)
ax5.set_ylim(0, FH7)

title_block(ax5, "SHEET 7 OF 7",
            drawing_title="TILT-SWING FRONT BOARD",
            subtitle="Adjuster bracket ring (ICP-03) + kinematic-seat inserts (ICP-05) — fabrication",
            scale_note="AXES IN mm",
            doc_id="TBS-TSB · Tilt-Swing Board")

section_label(ax5, 560, 2050, 'PANEL A — ADJUSTER BRACKET RING (ICP-03) (1:3)')
section_label(ax5, 2210, 2050, 'PANEL B — KINEMATIC-SEAT INSERTS (ICP-05) (4:1)')

# ── PANEL A: adjuster bracket ring — face view (fabrication) ──
rcx, rcy = 900, 1180
def s7(mm): return mm * 1.15
r_od = s7(RET_RING_OD / 2)
r_id = s7(RET_RING_ID / 2)
draw_circle(ax5, rcx, rcy, r_od, lw=LW_THICK, color=C_OUT)
draw_circle(ax5, rcx, rcy, r_id, lw=LW_THICK, color=C_OUT, fill=True, fc='white')
for i, lbl in enumerate(['SWING+', 'TILT+', 'SWING−', 'TILT−']):
    a = np.radians(i * 90)
    bx = rcx + s7(SOCK_PCD / 2) * np.cos(a); by = rcy + s7(SOCK_PCD / 2) * np.sin(a)
    draw_circle(ax5, bx, by, s7(BUSH_OD / 2), lw=LW_MED, color=C_OUT, fill=True, fc=C_DELR)   # M22 Delrin bushing bore
    draw_circle(ax5, bx, by, s7(ADJ_D / 2), lw=0.7, color=C_OUT, fill=True, fc='white')       # M8 adjuster thread
    la = a + np.radians(15)                                                                   # M6 lock hole, offset
    lx = rcx + s7(SOCK_PCD / 2) * np.cos(la); ly = rcy + s7(SOCK_PCD / 2) * np.sin(la)
    draw_circle(ax5, lx, ly, s7(3), lw=0.6, color=C_OUT, fill=True, fc='#888888')
    ax5.text(bx, by - s7(19), lbl, ha='center', va='top', fontsize=5, color=C_DIM, fontweight='bold', zorder=10)
for i in range(RET_BOLT_N):                                                                  # 6× M5 standoff clearance
    a = np.radians(30 + i * 60)
    sx = rcx + s7(RET_BOLT_PCD / 2) * np.cos(a); sy = rcy + s7(RET_BOLT_PCD / 2) * np.sin(a)
    draw_circle(ax5, sx, sy, s7(RET_BOLT_D / 2 + 0.5), lw=0.7, color=C_OUT, fill=True, fc='white')
draw_cl(ax5, rcx, rcy, r_od * 1.12)
dia_stack(ax5, rcx, rcy - r_od, [
    (2 * r_id,                    'Ø240 BORE (clears the pinhole / center)'),
    (2 * s7(SOCK_PCD / 2),        'Ø260 PCD · 4× M22×1.0 BUSHING BORE (Ø8 adjuster thread) · 90° APART'),
    (2 * s7(RET_BOLT_PCD / 2),    'Ø450 PCD · 6× Ø5.5 CLR (M5 STANDOFF) · 60° APART'),
    (2 * r_od,                    'Ø470 OD'),
], dirn=-1, step=50, fs=5, off=16)
ax5.text(rcx - r_od + 12, rcy + r_od - 14, '6061-T6 · 8mm THK\n(black anodize)', ha='left', va='top', fontsize=5, color=C_DIM, style='italic', zorder=10)
leader(ax5, rcx + s7(SOCK_PCD / 2) * np.cos(np.radians(60)), rcy + s7(SOCK_PCD / 2) * np.sin(np.radians(60)),
       rcx + r_od + 40, rcy + r_od - 60, '4× M6 NYLON-TIP\nLOCK, TANGENTIAL', fs=4.6, color=C_DIM, arrow_style='->', ha='left')
leader(ax5, rcx + s7(RET_BOLT_PCD / 2) * np.cos(np.radians(-30)), rcy + s7(RET_BOLT_PCD / 2) * np.sin(np.radians(-30)),
       rcx + r_od + 40, rcy - r_od + 60, '6× M5 STANDOFF\nTO ICP-01', fs=4.6, color=C_DIM, arrow_style='->', ha='left')
ax5.text(rcx, rcy - r_od - 300, 'PANEL A — ADJUSTER BRACKET RING (ICP-03) — face view\nMounts on ICP-01 interior face; carries the 4 adjuster knobs (set from inside) + reacts the wave-spring preload',
         ha='center', fontsize=5, style='italic', color='#333333')

# ── PANEL B: kinematic-seat inserts (ICP-05) — the 3 seat forms, side section + plan ──
def si(mm): return mm * 7.0
forms = [('CONE  (×1 · N)', 'cone', 'ball located in 2 axes'),
         ('V-GROOVE  (×1 · E)', 'vee', 'ball located in 1 axis — groove RADIAL'),
         ('FLAT  (×2 · S/W)', 'flat', 'axial contact only')]
icx = 2450
for j, (title, form, note) in enumerate(forms):
    iy = 1620 - j * 440
    bw, bh = si(16), si(12)
    ax5.add_patch(mpatches.Rectangle((icx - bw / 2, iy - bh / 2), bw, bh, fc=C_BEAR, ec=C_OUT, lw=LW_THICK, hatch='///', zorder=4))
    top = iy + bh / 2
    if form == 'cone':
        ax5.add_patch(mpatches.Polygon([(icx - si(4), top), (icx, top - si(4)), (icx + si(4), top)],
                      closed=True, fc='white', ec=C_OUT, lw=LW_MED, zorder=5))
    elif form == 'vee':
        ax5.add_patch(mpatches.Polygon([(icx - si(5), top), (icx, top - si(3.5)), (icx + si(5), top)],
                      closed=True, fc='white', ec=C_OUT, lw=LW_MED, zorder=5))
    # flat: nothing cut
    ax5.add_patch(plt.Circle((icx, top + si(4)), si(4), fc=C_BALL, ec=C_OUT, lw=0.7, zorder=6))   # Ø8 ball resting
    # plan symbol (top-view) to the right
    px = icx + si(16)
    draw_circle(ax5, px, iy, si(8), lw=LW_MED, color=C_OUT)
    if form == 'cone':
        draw_circle(ax5, px, iy, si(3), lw=0.7, color=C_OUT)
    elif form == 'vee':
        ax5.add_patch(mpatches.Rectangle((px - si(8), iy - si(2)), si(16), si(4), fc='#EEEEEE', ec=C_OUT, lw=0.7, zorder=5))
    ax5.text(icx - bw / 2 - 24, iy + si(6), title, ha='right', va='center', fontsize=5.6, fontweight='bold', color=C_DIM, zorder=10)
    ax5.text(icx - bw / 2 - 24, iy - si(4), note, ha='right', va='center', fontsize=4.2, style='italic', color='#555555', zorder=10)
    ax5.text(px + si(11), iy, 'PLAN', ha='left', va='center', fontsize=4.0, color='#888888', zorder=10)
# common insert dims (on the FLAT, bottom one)
fy = 1620 - 2 * 440
draw_dim_h(ax5, icx - si(8), icx + si(8), fy - si(9), 'Ø16 h6', above=False, fs=5, offset=8)
draw_dim_v(ax5, icx + si(20), fy - si(6), fy + si(6), '12mm', right=True, fs=5, offset=8)
ax5.text(icx, 1720, '4 off · 440C SS · Ra 0.4 ground · press-fit into the carrier Ø16 H7 rear-face bores (Loctite 638)',
         ha='center', fontsize=5, style='italic', color='#333333', zorder=10)
ax5.text(icx, 300, 'PANEL B — KINEMATIC-SEAT INSERTS (ICP-05)\nThe 3 forms make an exact-constraint coupling: 1 cone + 1 V-groove + 2 flat → carrier in-plane position + spin fixed',
         ha='center', fontsize=5, style='italic', color='#333333', zorder=10)

ax5.text(FW7 / 2, FH7 - 60,
         'ASSEMBLY KEY — Sheet 2 (Section A-A):  the bracket ring is the interior (camera-side) plate carrying the knobs; '
         'the seat inserts press into the\ncarrier REAR face at Ø260 and receive the adjuster balls.  Fabrication blueprints '
         'for the two machined ICP-03 / ICP-05 parts.',
         ha='center', va='top', fontsize=6, style='italic', color='#444',
         bbox=dict(boxstyle='round,pad=0.5', fc='#F4F4F4', ec='#BBBBBB', lw=0.6), zorder=12)

out5 = os.path.join(DIAGRAMS_DIR, 'tilt-swing-sheet7.png')
fig5.savefig(out5, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white')
plt.close(fig5)
print(f'  → {out5}  Done.')
