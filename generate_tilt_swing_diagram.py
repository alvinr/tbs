#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
Engineering diagrams: Tilt-Swing Front Board (TSB) Mechanism

Sheet 1: Front view — ICP-01 outer adapter frame + ICP-02 inner carrier (1:4 scale)
Sheet 2: Cross-section A-A — bearing, bellows, adjustment screws (1:4 scale)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
from tbs_constants import DIAGRAMS_DIR, SVG_DIR, svg_path
from tbs_title_block import title_block
from tbs_drawing import (draw_dim_h, draw_dim_v, draw_cl, draw_circle,
                         draw_rect, leader, bolt_holes, hatch_rect, draw_notes)

# ── Real dimensions (mm) ────────────────────────────────────────────────────
# ICP-01 Outer adapter frame
FR_OD       = 600      # outer frame dimension (square)
FR_THICK    = 40       # frame thickness (depth)
FR_BORE     = 380      # central bore diameter
FR_BRG_SEAT = 80       # bearing seat bore Ø80 H7
FR_BRG_DEPTH = 50      # bearing seat pocket depth
FR_LAB_1    = 382      # labyrinth bore step 1
FR_LAB_2    = 390      # labyrinth bore step 2
FR_LAB_3    = 400      # labyrinth bore step 3
FR_LAB_STEP = 5        # labyrinth step depth each

# ICP-02 Inner carrier plate
CR_OD       = 320      # carrier plate outer diameter
CR_THICK    = 25       # carrier plate thickness
CR_SHANK    = 50       # bearing shank Ø50 k5
CR_SHANK_L  = 46       # shank length (= bearing width)
CR_CB_D     = 52       # pinhole disc counterbore
CR_CB_DEP   = 3        # counterbore depth

# ICP-03 GE50-DO-2RS bearing
BRG_BORE    = 50       # bearing bore
BRG_OD      = 80       # bearing outer diameter
BRG_W       = 46       # bearing width

# Bellows ICP-10
BEL_ID      = 290      # bellows inner diameter
BEL_OD      = 360      # bellows outer diameter
BEL_FREE    = 60       # bellows free length
BEL_PLEATS  = 4        # number of pleats
BEL_INNER_PCD = 310    # inner flange PCD
BEL_OUTER_PCD = 375    # outer flange PCD

# Mounting interface (same as standard plate)
BOLT_BC     = 540      # bolt circle diameter
BOLT_D      = 13       # bolt hole clearance diameter
BOLT_N      = 8        # bolt count
DWL_D       = 8        # dowel pin diameter
DWL_OFF     = 200      # dowel pin offset ± from center
SEAL_D      = 420      # neoprene groove centerline diameter

# Adjustment screws
ADJ_PCD     = 260      # adjustment screw contact PCD on carrier
ADJ_SCREW   = 8        # M8 × 1.0 fine pitch
ADJ_BALL    = 8        # Ø8mm chrome steel ball
ADJ_BUSHING = 30       # Delrin bushing OD

# Pinhole
PH_DISC_D   = 50       # pinhole disc OD
PH_APT      = 2.17     # pinhole aperture

# ── Drawing constants ────────────────────────────────────────────────────────
LW_THICK  = 1.8
LW_MED    = 1.0
LW_THIN   = 0.5
LW_CUT    = 2.2
LW_DIM    = 0.7

C_OUT   = '#000000'
C_CL    = '#0055AA'
C_DIM   = '#333333'
C_HID   = '#888888'
C_STEEL = '#B0B0B0'
C_ALUM  = '#D8D8D8'
C_GASKT = '#404040'
C_RED   = '#CC0000'
C_BRG   = '#A0A0B0'
C_DELRIN = '#C8D8C0'
C_BELLOWS = '#2A2A2A'
C_BALL  = '#E0E0E0'


def draw_sheet1():
    """Sheet 1: Front view of TSB assembly at 1:2 scale."""
    SC = 2.0
    fig_w, fig_h = 8, 10
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
    cy = ph / 2 + 60

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

    # Bearing seat (Ø80 H7, hidden — on interior face)
    draw_circle(ax, cx, cy, s(FR_BRG_SEAT / 2), lw=LW_THIN, color=C_HID, ls=':')

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

    # 4× Adjustment screws on carrier rim (on PCD Ø260, at 0°/90°/180°/270°)
    adj_r = s(ADJ_PCD / 2)
    adj_labels = ['SWING+', 'TILT+', 'SWING−', 'TILT−']
    adj_colors = ['#A0A0A0', '#333333', '#A0A0A0', '#333333']
    for i, (label, kc) in enumerate(zip(adj_labels, adj_colors)):
        angle = i * 90
        ax_pos = cx + adj_r * np.cos(np.radians(angle))
        ay_pos = cy + adj_r * np.sin(np.radians(angle))
        # Knob circle
        knob_r = s(ADJ_BUSHING / 2)
        ax.add_patch(plt.Circle((ax_pos, ay_pos), knob_r,
                     fc=kc, ec=C_OUT, lw=LW_MED, zorder=12))
        # Ball center
        ax.add_patch(plt.Circle((ax_pos, ay_pos), s(ADJ_BALL / 2),
                     fc=C_BALL, ec=C_OUT, lw=0.5, zorder=13))
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

    # Bellows inner flange bolts (6× M6 on Ø310 PCD)
    bel_in_r = s(BEL_INNER_PCD / 2)
    for i in range(6):
        angle = i * 60 + 30
        bx = cx + bel_in_r * np.cos(np.radians(angle))
        by = cy + bel_in_r * np.sin(np.radians(angle))
        draw_circle(ax, bx, by, s(3), lw=0.5, color=C_HID, fc='white', fill=True)

    # Section cut line A-A (vertical through center)
    cut_ext = half + 50
    for yy, arrow_dir in [(cy + cut_ext, -1), (cy - cut_ext, 1)]:
        ax.plot([cx - 8, cx + 8], [yy, yy], color=C_RED, lw=LW_CUT, zorder=20)
        ax.annotate('', xy=(cx + 20 * arrow_dir, yy),
                    xytext=(cx, yy),
                    arrowprops=dict(arrowstyle='->', color=C_RED, lw=1.5))
        ax.text(cx - 15, yy, 'A', fontsize=9, fontweight='bold', color=C_RED,
                ha='center', va='center', zorder=21)

    # ── Dimensions ───────────────────────────────────────────────────────────
    # Frame outer dimension
    draw_dim_h(ax, cx - half, cx + half, cy - half - 30, '600', above=False, fs=6, offset=8)

    # Right-side leaders (top to bottom)
    leader(ax, cx + bolt_r * 0.924, cy + bolt_r * 0.383,
           cx + half + 40, cy + half - 10, 'Ø540 PCD\n8× M12', fs=5.5)

    leader(ax, cx + bore_r * 0.707, cy + bore_r * 0.707,
           cx + half + 40, cy + half - 50, 'Ø380 BORE', fs=5.5)

    leader(ax, cx + cr_r * 0.6, cy + cr_r * 0.8,
           cx + half + 40, cy + half - 80, 'Ø320 CARRIER (ICP-02)', fs=5.5)

    leader(ax, cx + s(DWL_OFF) + s(DWL_D / 2), cy + 5,
           cx + half + 40, cy + 10, '2× Ø8 DOWEL', fs=5.5)

    leader(ax, cx + s(FR_BRG_SEAT / 2) * 0.707, cy - s(FR_BRG_SEAT / 2) * 0.707,
           cx + half + 40, cy - half + 60, 'Ø80 H7 BRG SEAT', fs=5.5)

    # Left-side leaders
    leader(ax, cx - s(SEAL_D / 2) * 0.707, cy - s(SEAL_D / 2) * 0.707,
           cx - half - 40, cy - half + 50, 'Ø420 SEAL GROOVE', fs=5.5)

    # Bottom leaders
    leader(ax, cx + ph_r, cy - ph_r * 0.8,
           cx + 80, cy - cr_r - 30, 'Ø50 PINHOLE DISC\nØ2.17mm APERTURE', fs=5.5)

    leader(ax, cx + adj_r * 0.383, cy - adj_r * 0.924,
           cx + 80, cy - cr_r - 65, 'Ø260 PCD\n4× M8×1.0 ADJ SCREWS', fs=5.5)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes1 = [
        'FRONT VIEW — TILT-SWING BOARD (TSB):',
        'VIEW FROM EXTERIOR (SCENE SIDE). CARRIER (ICP-02) VISIBLE THROUGH Ø380 BORE.',
        'ICP-01: 600×600×40mm AL 6061-T6 OUTER FRAME. SAME M12/540PCD/Ø8 DOWEL INTERFACE AS ALL PLATES.',
        'ICP-02: Ø320×25mm AL 6061-T6 CARRIER. CARRIES Ø50mm PINHOLE DISC (LENOX LASER SS-302).',
        'ICP-03: GE50-DO-2RS SPHERICAL PLAIN BEARING (SKF). Ø50 BORE × Ø80 OD × 46mm. ±15° MISALIGNMENT.',
        'ADJUSTMENT: 4× M8×1.0 FINE-PITCH SCREWS. BLACK KNOBS = TILT, SILVER = SWING. 0.012°/CLICK.',
        'LOCKING: 4× M6 NYLON-TIP SET SCREWS (3mm HEX KEY FROM EXTERIOR FACE).',
        'BELLOWS (ICP-10): Ø290 ID × Ø360 OD, 4-PLEAT NEOPRENE, ZERO-FRICTION LIGHT SEAL.',
    ]
    draw_notes(ax, notes1, 30, cy - half - 60, spacing=16,
               fs=6, width=pw - 70)

    title_block(ax, "SHEET 1 OF 2",
                drawing_title="TILT-SWING FRONT BOARD",
                subtitle="FRONT VIEW (SCENE SIDE) — ICP-01 + ICP-02",
                scale_note="SCALE 1:2 · AXES IN mm",
                doc_id="TBS-001 · Interchangeable Plates")

    plt.tight_layout(pad=0)
    out1 = f'{DIAGRAMS_DIR}/tilt-swing-sheet1.png'
    fig.savefig(out1, dpi=150, bbox_inches='tight', facecolor='white')
    fig.savefig(svg_path(out1), bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  → tilt-swing-sheet1.png  Done.')


def draw_sheet2():
    """Sheet 2: Cross-section A-A through TSB assembly at 1:2 scale."""
    SC = 2.0
    fig_w, fig_h = 5, 8
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

    # Section center: carrier center / pinhole plane
    cx = pw * 0.45
    cy = ph / 2 + 20

    # Horizontal axis: depth (X direction, scene left, interior right)
    # Vertical axis: height (Y, radial from center)
    # Section cuts vertically through center, viewer looks from top

    # ── Container wall ───────────────────────────────────────────────────────
    wall_t = s(2.0)
    wall_x = cx - s(FR_THICK) - wall_t - s(6)  # wall frame sits against wall
    wall_half = s(FR_OD / 2) + 30
    ax.add_patch(mpatches.Rectangle(
        (wall_x, cy - wall_half), wall_t, 2 * wall_half,
        fc=C_STEEL, ec=C_OUT, lw=LW_THICK, zorder=3,
        hatch='///'))
    ax.text(wall_x - 15, cy, 'CONTAINER\nWALL', ha='right', va='center',
            fontsize=5, color=C_DIM, style='italic', rotation=90)

    # Wall aperture (Ø360 hole)
    wall_apt_half = s(360 / 2)

    # ── ICP-01 Outer adapter frame (cross-section) ───────────────────────────
    fr_left = cx - s(FR_THICK)
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

    # ── Bearing seat pocket (interior face of ICP-01) ────────────────────────
    brg_seat_half = s(BRG_OD / 2)
    brg_seat_x = cx - s(FR_BRG_DEPTH)
    # Upper seat cutout
    ax.add_patch(mpatches.Rectangle(
        (brg_seat_x, cy + brg_seat_half - s(BRG_W / 2)),
        s(FR_BRG_DEPTH), s(BRG_W / 2) - (bore_half - brg_seat_half),
        fc='white', ec=C_OUT, lw=LW_MED, zorder=6))
    # Lower seat cutout
    ax.add_patch(mpatches.Rectangle(
        (brg_seat_x, cy - brg_seat_half),
        s(FR_BRG_DEPTH), s(BRG_W / 2) - (bore_half - brg_seat_half),
        fc='white', ec=C_OUT, lw=LW_MED, zorder=6))

    # ── ICP-03 Bearing (GE50-DO-2RS) ────────────────────────────────────────
    brg_left = cx - s(BRG_W)
    brg_outer_half = s(BRG_OD / 2)
    brg_inner_half = s(BRG_BORE / 2)

    # Outer ring
    for sign in [-1, 1]:
        ax.add_patch(mpatches.Rectangle(
            (brg_left, cy + sign * brg_inner_half),
            s(BRG_W), sign * (brg_outer_half - brg_inner_half),
            fc=C_BRG, ec=C_OUT, lw=LW_MED, zorder=7))

    # Inner ring (on carrier shank)
    brg_ir_half = s(BRG_BORE / 2 + 5)
    for sign in [-1, 1]:
        ax.add_patch(mpatches.Rectangle(
            (brg_left + s(3), cy + sign * brg_inner_half),
            s(BRG_W - 6), sign * 5,
            fc='#8888A0', ec=C_OUT, lw=0.5, zorder=8))

    # ── ICP-02 Carrier plate (cross-section) ─────────────────────────────────
    cr_half = s(CR_OD / 2)
    cr_left = cx
    cr_right = cx + s(CR_THICK)

    # Upper carrier section (above shank)
    shank_half = s(CR_SHANK / 2)
    ax.add_patch(mpatches.Rectangle(
        (cr_left, cy + shank_half), s(CR_THICK), cr_half - shank_half,
        fc='#E0E0E0', ec=C_OUT, lw=LW_THICK, zorder=5))
    # Lower carrier section
    ax.add_patch(mpatches.Rectangle(
        (cr_left, cy - cr_half), s(CR_THICK), cr_half - shank_half,
        fc='#E0E0E0', ec=C_OUT, lw=LW_THICK, zorder=5))

    # Cross-hatching
    for section_bot, section_top in [(cy + shank_half, cy + cr_half),
                                     (cy - cr_half, cy - shank_half)]:
        for i in range(60):
            y0 = section_bot + i * 4
            if y0 < section_top:
                y1 = min(y0 + 4, section_top)
                ax.plot([cr_left, cr_left + min(s(CR_THICK), y1 - y0)],
                        [y0, y1], color='#AAAAAA', lw=0.3, zorder=6)

    # Carrier shank into bearing
    ax.add_patch(mpatches.Rectangle(
        (brg_left + s(3), cy - shank_half), s(CR_SHANK_L - 3) + s(CR_THICK), s(CR_SHANK),
        fc='#E0E0E0', ec=C_OUT, lw=LW_MED, zorder=6))

    # ── Pinhole disc (on carrier interior face) ──────────────────────────────
    disc_half = s(PH_DISC_D / 2)
    disc_t = s(0.1) * 20  # exaggerated for visibility
    ax.add_patch(mpatches.Rectangle(
        (cr_right, cy - disc_half), disc_t, s(PH_DISC_D),
        fc='#666666', ec=C_OUT, lw=LW_MED, zorder=8))

    # Counterbore
    cb_half = s(CR_CB_D / 2)
    cb_dep = s(CR_CB_DEP)
    ax.add_patch(mpatches.Rectangle(
        (cr_right - cb_dep, cy - cb_half), cb_dep, s(CR_CB_D),
        fc='white', ec=C_OUT, lw=0.5, zorder=7))

    # ── Bellows (ICP-10) ─────────────────────────────────────────────────────
    bel_inner_half = s(BEL_ID / 2)
    bel_outer_half = s(BEL_OD / 2)
    # Bellows spans from frame interior face to carrier exterior face
    bel_left = cx
    bel_right = cx + s(BEL_FREE * 0.7)

    # Draw pleated bellows as zigzag connecting frame to carrier
    for sign in [-1, 1]:
        y_inner = cy + sign * bel_inner_half
        y_outer = cy + sign * bel_outer_half
        y_mid = (y_inner + y_outer) / 2
        pleat_xs = np.linspace(bel_left, bel_right, BEL_PLEATS * 2 + 1)
        pleat_ys = []
        for j, px in enumerate(pleat_xs):
            if j % 2 == 0:
                pleat_ys.append(y_mid + sign * (y_outer - y_mid) * 0.3)
            else:
                pleat_ys.append(y_mid - sign * (y_outer - y_mid) * 0.3)
        ax.plot(pleat_xs, pleat_ys, color=C_BELLOWS, lw=1.2, zorder=4)

    # ── Adjustment screws (top and bottom in this section) ───────────────────
    adj_arm = s(ADJ_PCD / 2)
    for sign in [-1, 1]:
        screw_y = cy + sign * adj_arm
        # Delrin bushing in frame
        bush_half = s(ADJ_BUSHING / 2)
        ax.add_patch(mpatches.Rectangle(
            (fr_left - s(5), screw_y - s(ADJ_SCREW / 2) - 2),
            s(FR_THICK + 5), s(ADJ_SCREW) + 4,
            fc=C_DELRIN, ec=C_OUT, lw=0.5, zorder=9))
        # Screw shaft
        ax.plot([fr_left - s(15), cr_left + 3], [screw_y, screw_y],
                color=C_OUT, lw=1.5, zorder=10)
        # Ball at tip
        ball_r = s(ADJ_BALL / 2)
        ax.add_patch(plt.Circle((cr_left + 3, screw_y), ball_r,
                     fc=C_BALL, ec=C_OUT, lw=0.5, zorder=11))
        # Hemispherical socket in carrier
        ax.add_patch(plt.Circle((cr_left, screw_y), ball_r + 1,
                     fc='#D0D0D0', ec=C_OUT, lw=0.5, zorder=10))
        # Knob (exterior)
        knob_w = s(15)
        knob_half = s(10)
        ax.add_patch(mpatches.Rectangle(
            (fr_left - s(15) - knob_w, screw_y - knob_half),
            knob_w, 2 * knob_half,
            fc='#333333' if sign != 0 else '#A0A0A0', ec=C_OUT, lw=LW_MED, zorder=10))
        # Label
        label = 'TILT+' if sign > 0 else 'TILT−'
        ax.text(fr_left - s(15) - knob_w - 8, screw_y, label,
                ha='right', va='center', fontsize=5, fontweight='bold', color='#333333')

    # ── Centerline ───────────────────────────────────────────────────────────
    cl_left = wall_x - 20
    cl_right = cr_right + disc_t + 40
    ax.plot([cl_left, cl_right], [cy, cy],
            color=C_CL, lw=LW_THIN, ls=(0, (8, 3, 1, 3)), zorder=2)

    # ── Labels ───────────────────────────────────────────────────────────────
    # Scene / Interior arrows at top of section
    arr_y = cy + fr_half + 15
    ax.annotate('EXTERIOR\n(SCENE)', xy=(wall_x, arr_y), xytext=(wall_x - 10, arr_y + 35),
                fontsize=5, color='#333', style='italic', ha='center', va='bottom',
                arrowprops=dict(arrowstyle='->', color='#999', lw=0.6))
    ax.annotate('INTERIOR\n(CAMERA)', xy=(cr_right + disc_t, arr_y), xytext=(cr_right + disc_t + 10, arr_y + 35),
                fontsize=5, color='#333', style='italic', ha='center', va='bottom',
                arrowprops=dict(arrowstyle='->', color='#999', lw=0.6))

    # Component labels with leaders — staggered vertically
    lx_r = cr_right + 40
    leader(ax, (fr_left + fr_right) / 2, cy + fr_half - 10,
           lx_r, cy + fr_half + 20,
           'ICP-01 OUTER FRAME\n600×600×40 AL', fs=5)

    leader(ax, (cr_left + cr_right) / 2, cy + cr_half - 5,
           lx_r, cy + 20,
           'ICP-02 CARRIER Ø320×25 AL', fs=5)

    leader(ax, brg_left + s(BRG_W / 2), cy + brg_outer_half,
           brg_left - 10, cy + brg_outer_half + 50,
           'ICP-03 GE50-DO-2RS\nØ50×Ø80×46', fs=5)

    leader(ax, cr_right + disc_t / 2, cy + disc_half + 3,
           lx_r, cy + disc_half + 40,
           'PINHOLE DISC\nØ50×0.1 SS-302\nØ2.17mm APT', fs=5)

    leader(ax, bel_left + (bel_right - bel_left) / 2, cy - bel_outer_half + 5,
           lx_r, cy - bel_outer_half - 20,
           'ICP-10 BELLOWS Ø290–Ø360', fs=5)

    # ── Dimensions ───────────────────────────────────────────────────────────
    # Frame thickness
    draw_dim_h(ax, fr_left, fr_right, cy + fr_half + 60, '40',
               above=True, fs=6, offset=8)

    # Carrier thickness
    draw_dim_h(ax, cr_left, cr_right, cy - cr_half - 30, '25',
               above=False, fs=6, offset=8)

    # Bearing width
    draw_dim_h(ax, brg_left, brg_left + s(BRG_W), cy - brg_outer_half - 20, '46',
               above=False, fs=5.5, offset=6)

    # Frame height (half)
    draw_dim_v(ax, fr_left - 30, cy, cy + fr_half, '300',
               right=False, fs=6, offset=8)
    draw_dim_v(ax, fr_left - 30, cy - fr_half, cy, '300',
               right=False, fs=6, offset=8)

    # Bore half
    draw_dim_v(ax, fr_right + 10, cy, cy + bore_half, f'{int(FR_BORE/2)}',
               right=True, fs=5.5, offset=6)

    # Carrier radius
    draw_dim_v(ax, cr_right + 15, cy, cy + cr_half, f'{int(CR_OD/2)}',
               right=True, fs=5.5, offset=6)

    # Section title — at top of drawing
    ax.text(cx, cy + fr_half + 100, 'SECTION A-A', ha='center', fontsize=8,
            fontweight='bold', color=C_RED)
    ax.text(cx, cy + fr_half + 83, '1:2 SCALE', ha='center', fontsize=6, color='#555')

    # ── Notes ────────────────────────────────────────────────────────────────
    notes2 = [
        'SECTION A-A — TILT-SWING BOARD ASSEMBLY:',
        'VERTICAL SECTION THROUGH CENTER. BEARING SHANK (ICP-02) PASSES THROUGH GE50-DO-2RS INTO FRAME POCKET.',
        'PIVOT POINT AT PINHOLE DISC FACE — TILT ROTATES IMAGE CONE ABOUT PINHOLE, NO PARALLAX.',
        'ADJUSTMENT: OPPOSING M8×1.0 SCREW PAIRS PUSH/PULL CARRIER RIM VIA GRADE-25 Ø8mm BALL CONTACTS.',
        'ANGULAR RANGE: ±5.3° (±12mm TRAVEL AT 130mm ARM). RESOLUTION: 0.012°/CLICK (36-DETENT KNOBS).',
        'BELLOWS: ZERO-FRICTION LIGHT SEAL. ±13.9mm ASYMMETRIC COMPRESSION AT ±5° TILT.',
        'LABYRINTH BORE: 3-STEP (Ø382/390/400mm, 5mm DEEP EACH) — SECONDARY LIGHT SEAL.',
    ]
    draw_notes(ax, notes2, 25, ph * 0.20, spacing=14, fs=5, width=pw - 50)

    title_block(ax, "SHEET 2 OF 2",
                drawing_title="TILT-SWING FRONT BOARD",
                subtitle="SECTION A-A",
                scale_note="1:2 · mm",
                doc_id="TBS-001",
                portrait=True)

    plt.tight_layout(pad=0)
    out2 = f'{DIAGRAMS_DIR}/tilt-swing-sheet2.png'
    fig.savefig(out2, dpi=150, bbox_inches='tight', facecolor='white')
    fig.savefig(svg_path(out2), bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  → tilt-swing-sheet2.png  Done.')


if __name__ == "__main__":
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    os.makedirs(SVG_DIR, exist_ok=True)
    print("Generating TBS-001 Tilt-Swing Front Board diagrams...")
    draw_sheet1()
    draw_sheet2()
    print("Done.")
