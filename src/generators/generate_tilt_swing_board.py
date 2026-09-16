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
from tbs_constants import (DIAGRAMS_DIR, FRONT_BOARD_MAX_DEG, FRONT_BOARD_CLICK_DEG,
                           FRONT_BOARD_DETENTS, FRONT_BOARD_TRAVEL_MM, FRONT_BOARD_SCREW_PITCH,
                           FRONT_BOARD_ARM_MM)
from tbs_title_block import title_block
from tbs_drawing import (draw_dim_h, draw_dim_v, draw_cl, draw_circle,
                         draw_rect, leader, bolt_holes, draw_notes)
from tbs_constants import DIAGRAM_DPI

# ── Dimensions (mm) ──────────────────────────────────────────────────────────

# --- existing plate interface (unchanged) ---
PL_OD      = 600      # plate outer dimension (square)
BOLT_BC    = 540      # bolt circle diameter
BOLT_D     = 13       # bolt hole clearance diameter
BOLT_N     = 8
DWL_D      = 8        # dowel pin diameter
DWL_OFF    = 200      # ± horizontal from center
SEAL_D     = 420      # neoprene groove PCD
TRAP_SQ    = 490      # light-trap rebate PCD (square)
FR_APT_D   = 350      # wall frame aperture diameter
PH_CB_D    = 52       # pinhole disc counterbore
PH_CB_DEP  = 3
PH_DISC_D  = 50
PH_BORE    = 90       # exterior taper bore

# --- ICP-01 Outer Adapter Frame ---
TSB01_THICK  = 40     # plate thickness
TSB01_BORE   = 380    # central bore diameter
BRG_SEAT_D   = 80     # bearing outer ring OD / seat bore diameter
BRG_SEAT_DEP = 50     # depth of bearing pocket
ADJ_PCD      = 270    # adjustment screw PCD (in frame)
ADJ_N        = 4      # 4 screws
LAB_D1, LAB_D2, LAB_D3 = 382, 390, 400  # labyrinth step diameters
BELL_OUT_PCD = 420    # bellows outer clamp-ring screw PCD — OUTSIDE the Ø400 labyrinth, on solid frame face

# --- ICP-02 Inner Carrier Plate ---
CARR_OD      = 320    # carrier plate OD
CARR_THICK   = 25     # thickness
BRG_SHANK_D  = 50     # bearing shank diameter (k5)
BRG_SHANK_L  = 35     # shank length
SOCK_PCD     = 260    # ball socket insert PCD
BELL_IN_PCD  = 306    # bellows inner clamp-ring screw PCD — 7mm edge to the Ø320 rim, 8mm to the Ø290 ID

# --- Bearing ICP-03 ---
BRG_OD       = 80
BRG_ID       = 50
BRG_W        = 46     # total width

# --- Adjustment screw ---
ADJ_D        = 8      # M8 screw
ADJ_ARM      = 130    # arm radius (frame ADJ_PCD/2 - a few mm for geometry)
BALL_D       = 8      # chrome steel ball
KNOB_D       = 40
KNOB_H       = 15
BUSH_OD      = 22
BUSH_L       = 35

# --- Bellows (truncated cone: small end on the carrier, large end on the frame) ---
BELL_ID      = 290    # small end (carrier / scene side)
BELL_OD      = 430    # large end (frame / container side) — clears the Ø400 labyrinth to land on frame face
BELL_FREE    = 60     # free length
BELL_PLEATS  = 4
BELL_PLEAT_D = 15     # pleat depth
CLAMP_SCR_D  = 4      # M4 clamp-ring retaining screws (both flanges)
CLAMP_RING_W = 14     # clamp-ring radial band width

SEAL_W   = 3          # neoprene seal groove width
SEAL_DEP = 3          # seal groove depth

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
FR_BRG_SEAT, FR_BRG_DEPTH = 80, 50
FR_LAB_1, FR_LAB_2, FR_LAB_3, FR_LAB_STEP = 382, 390, 400, 5
CR_OD, CR_THICK, CR_SHANK, CR_SHANK_L = 320, 25, 50, 46
CR_CB_D, CR_CB_DEP = 52, 3
BRG_BORE = 50
BEL_ID, BEL_OD, BEL_FREE, BEL_PLEATS = 290, 430, 60, 4   # truncated cone: Ø290 carrier end → Ø430 frame end
BEL_INNER_PCD, BEL_OUTER_PCD = 306, 420   # bellows clamp-ring screw PCDs (carrier / frame)
ADJ_PCD_CARRIER, ADJ_SCREW, ADJ_BALL, ADJ_BUSHING = 260, 8, 8, 30
PH_APT = 2.17
C_BRG, C_DELRIN, C_BELLOWS, C_BALL = '#A0A0B0', '#C8D8C0', '#2A2A2A', '#E0E0E0'


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
    adj_r = s(ADJ_PCD_CARRIER / 2)
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

    # Bellows inner clamp ring (Al) + 4× M4 screws on Ø306 — retains the bellows small end on the carrier
    bel_in_r = s(BEL_INNER_PCD / 2)
    draw_circle(ax, cx, cy, s((BEL_INNER_PCD + 8) / 2), lw=0.5, color=C_HID, ls='--')
    draw_circle(ax, cx, cy, s((BEL_INNER_PCD - 8) / 2), lw=0.5, color=C_HID, ls='--')
    for i in range(4):
        angle = 45 + i * 90
        bx = cx + bel_in_r * np.cos(np.radians(angle))
        by = cy + bel_in_r * np.sin(np.radians(angle))
        draw_circle(ax, bx, by, s(2), lw=0.5, color=C_HID, fc='white', fill=True)

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

    leader(ax, cx + s(FR_BRG_SEAT / 2) * 0.707, cy - s(FR_BRG_SEAT / 2) * 0.707,
           cx + 180, cy - half + 50, 'Ø80 H7 BRG SEAT', fs=5.5)

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
        'ICP-03: GE50-DO-2RS SPHERICAL PLAIN BEARING (SKF). Ø50 BORE × Ø80 OD × 46mm. ±15° MISALIGNMENT.',
        f'ADJUSTMENT: 4× M8×1.0 FINE-PITCH SCREWS. BLACK KNOBS = TILT, SILVER = SWING. {FRONT_BOARD_CLICK_DEG}°/CLICK.',
        'LOCKING: 4× M6 NYLON-TIP SET SCREWS (3mm HEX KEY FROM EXTERIOR FACE).',
        'BELLOWS (ICP-04): TRUNCATED CONE Ø290→Ø430, 4-PLEAT NEOPRENE, CLAMP-RING RETAINED, ZERO-FRICTION LIGHT SEAL.',
    ]
    draw_notes(ax, notes1, 35, cy - half - 70, spacing=10,
               fs=6, width=pw - 70)

    title_block(ax, "SHEET 1 OF 5",
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

    # ── Bellows (ICP-04) ─────────────────────────────────────────────────────
    bel_inner_half = s(BEL_ID / 2)
    bel_outer_half = s(BEL_OD / 2)
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
    adj_arm = s(ADJ_PCD_CARRIER / 2)
    for sign in [-1, 1]:
        screw_y = cy + sign * adj_arm
        # Delrin bushing in frame
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
    arr_y = cy + fr_half + 15
    ax.annotate('EXTERIOR\n(SCENE)', xy=(wall_x, arr_y), xytext=(wall_x - 30, arr_y + 35),
                fontsize=5, color='#333', style='italic', ha='center', va='bottom',
                arrowprops=dict(arrowstyle='->', color='#999', lw=0.6))
    ax.annotate('INTERIOR\n(CAMERA)', xy=(cr_right + disc_t, arr_y), xytext=(cr_right + disc_t + 10, arr_y + 35),
                fontsize=5, color='#333', style='italic', ha='center', va='bottom',
                arrowprops=dict(arrowstyle='->', color='#999', lw=0.6))

    lx_r = cr_right + 40
    leader(ax, (fr_left + fr_right) / 2, cy + fr_half - 10,
           lx_r + 20, cy + fr_half + 20,
           'ICP-01 OUTER FRAME\n600×600×40 AL', fs=5)

    leader(ax, (cr_left + cr_right) / 2, cy + cr_half - 5,
           lx_r + 20, cy + 110,
           'ICP-02 CARRIER Ø320×25 AL', fs=5)

    leader(ax, brg_left + s(BRG_W / 2), cy + brg_outer_half,
           lx_r + 20, cy + brg_outer_half + 60,
           'ICP-03 GE50-DO-2RS\nØ50×Ø80×46', fs=5)

    leader(ax, cr_right + disc_t / 2, cy + disc_half + 3,
           lx_r + 20, cy + disc_half + 40,
           'PINHOLE DISC\nØ50×0.1 SS-302\nØ2.17mm APT', fs=5)

    leader(ax, bel_left + (bel_right - bel_left) / 2, cy - bel_outer_half + 5,
           lx_r + 20, cy - bel_outer_half - 20,
           'ICP-04 BELLOWS\nØ290→Ø430 CONE\nCLAMP-RING BOTH ENDS', fs=5)

    # ── Dimensions ───────────────────────────────────────────────────────────
    draw_dim_h(ax, fr_left, fr_right, cy + fr_half + 10, '40mm',
               above=True, fs=6, offset=8)
    draw_dim_h(ax, cr_left, cr_right, cy - cr_half - 80, '25mm',
               above=False, fs=6, offset=8)
    draw_dim_h(ax, brg_left, brg_left + s(BRG_W), cy - brg_outer_half - 20, '46mm',
               above=False, fs=5.5, offset=6)
    draw_dim_v(ax, fr_left - 50, cy, cy + fr_half, '300mm',
               right=False, fs=6, offset=8)
    draw_dim_v(ax, fr_left - 50, cy - fr_half, cy, '300mm',
               right=False, fs=6, offset=8)
    draw_dim_v(ax, fr_right + 30, cy, cy + bore_half, f'{int(FR_BORE/2)}mm',
               right=True, fs=5.5, offset=6)
    draw_dim_v(ax, cr_right + 30, cy, cy + cr_half, f'{int(CR_OD/2)}mm',
               right=True, fs=5.5, offset=6)

    # Section title — at top of drawing
    ax.text(cx, cy + fr_half + 100, 'SECTION A-A', ha='center', fontsize=8,
            fontweight='bold', color=C_RED)
    ax.text(cx, cy + fr_half + 83, '1:2 SCALE', ha='center', fontsize=6, color='#555')

    # ── Notes ────────────────────────────────────────────────────────────────
    notes2 = [
        'SECTION A-A — TILT-SWING BOARD ASSEMBLY:',
        'VERTICAL SECTION THROUGH CENTER. BEARING SHANK (ICP-02) PASSES THROUGH GE50-DO-2RS INTO FRAME',
        'POCKET. PIVOT POINT AT PINHOLE DISC FACE — TILT ROTATES IMAGE CONE ABOUT PINHOLE, NO PARALLAX.',
        'ADJUSTMENT: OPPOSING M8×1.0 SCREW PAIRS PUSH/PULL CARRIER RIM VIA GRADE-25 Ø8mm BALL CONTACTS.',
        f'ANGULAR RANGE: ±{FRONT_BOARD_MAX_DEG}° (±{FRONT_BOARD_TRAVEL_MM}mm TRAVEL AT {FRONT_BOARD_ARM_MM}mm ARM). RESOLUTION: {FRONT_BOARD_CLICK_DEG}°/CLICK ({FRONT_BOARD_DETENTS}-DETENT KNOBS).',
        'BELLOWS: ZERO-FRICTION LIGHT SEAL. ±13.9mm ASYMMETRIC COMPRESSION AT ±5° TILT.',
        'LABYRINTH BORE: 3-STEP (Ø382/390/400mm, 5mm DEEP EACH) — SECONDARY LIGHT SEAL.',
    ]
    draw_notes(ax, notes2, 25, ph * 0.20, spacing=12, fs=5, width=pw - 50)

    title_block(ax, "SHEET 2 OF 5",
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

title_block(ax1, "SHEET 3 OF 5",
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

# 4 adjustment screw positions (seen as circles on face)
for angle_deg in [90, 0, 270, 180]:
    ax_x = cx_b + s1(ADJ_PCD/2) * np.cos(np.radians(angle_deg))
    ax_y = cy_b + s1(ADJ_PCD/2) * np.sin(np.radians(angle_deg))
    draw_circle(ax1, ax_x, ax_y, s1(BUSH_OD/2), lw=LW_MED, color=C_OUT, fill=True, fc=C_DELR, zorder=5)
    draw_circle(ax1, ax_x, ax_y, s1(ADJ_D/2), lw=0.7, color=C_OUT, fill=True, fc='white', zorder=6)

draw_cl(ax1, cx_b, cy_b, hw*1.15)

# ── Formal dimensions — every feature (Ø + count folded onto the dim line, no leaders) ──
dia_stack(ax1, cx_b, cy_b - hw, [
    (s1(TSB01_BORE), 'Ø380 BORE (THRU)'),
    (s1(SEAL_D),     'Ø420 SEAL GROOVE · 3 WIDE × 3 DEEP'),
    (s1(BOLT_BC),    'Ø540 B.C. · 8× Ø13 CLR (M12) EQUISPACED'),
    (s1(PL_OD),      '600'),
], dirn=-1)
dia_stack(ax1, cx_b, cy_b + hw, [
    (s1(ADJ_PCD), 'Ø270 PCD · 4× M22×1.0 BUSHING (Ø8 SCREW BORE) · 90° APART'),
], dirn=+1)
draw_dim_v(ax1, cx_b - hw - 30, cy_b - hw, cy_b + hw, '600', right=False, fs=5.5, offset=20)
ax1.text(cx_b - hw + 12, cy_b + hw - 14, '6061-T6 · 40 THK', ha='left', va='top',
         fontsize=5, color=C_DIM, style='italic', zorder=10)
# Dowel location — ±200 on the horizontal C/L (Ø8 folded onto the +200 dim)
draw_dim_h(ax1, cx_b - s1(DWL_OFF), cx_b, cy_b, '200', above=True, fs=4.5, offset=13)
draw_dim_h(ax1, cx_b, cx_b + s1(DWL_OFF), cy_b, '200 · 2× Ø8 H7 DOWEL', above=True, fs=4.5, offset=13)

draw_dim_v(ax1, cx_b + hw + 30, cy_b - s1(BOLT_BC/2), cy_b + s1(BOLT_BC/2), 'Ø540 B.C. (8× M12)', right=True, fs=5, offset=16)
ax1.text(cx_b, cy_b - hw - 250, 'PANEL A — ICP-01 EXTERIOR (1:8)\n(Same bolt/dowel/seal interface as standard pinhole plate)',
         ha='center', fontsize=5, color='#333333', style='italic')

# ───────────────────────────────────────────────
# PANEL B: ICP-01 Interior (container-facing) face
# ───────────────────────────────────────────────
cx_c, cy_c = 2350, 1280

p3 = mpatches.Rectangle((cx_c - hw, cy_c - hw), s1(PL_OD), s1(PL_OD),
                         lw=LW_THICK, edgecolor=C_OUT, facecolor=C_ALUM, zorder=3)
ax1.add_patch(p3)

# Central bearing seat (Ø80 H7) — recessed pocket, drawn OPEN (outline, not a filled disc) to match the exterior face
draw_circle(ax1, cx_c, cy_c, s1(BRG_SEAT_D/2), lw=LW_MED, color=C_OUT, fill=True, fc='white', zorder=4)
# Bearing bore (Ø50) — recessed behind the seat (hidden line)
draw_circle(ax1, cx_c, cy_c, s1(BRG_ID/2), lw=LW_THIN, color=C_HID, ls='--', zorder=5)

# Labyrinth steps (3 concentric dashed circles)
for d, ls_str in [(LAB_D1,'--'),(LAB_D2,'-.'),(LAB_D3,':')]:
    draw_circle(ax1, cx_c, cy_c, s1(d/2), lw=LW_THIN, color='#555555', ls=ls_str)

# 4 × M22 adjustment bushing holes (interior side — seen from behind)
for angle_deg in [90, 0, 270, 180]:
    ax_x = cx_c + s1(ADJ_PCD/2) * np.cos(np.radians(angle_deg))
    ax_y = cy_c + s1(ADJ_PCD/2) * np.sin(np.radians(angle_deg))
    draw_circle(ax1, ax_x, ax_y, s1(BUSH_OD/2), lw=LW_MED, color=C_OUT, fill=True, fc=C_DELR, zorder=5)
    draw_circle(ax1, ax_x, ax_y, s1(ADJ_D/2), lw=0.7, color=C_OUT, fill=True, fc='white', zorder=6)

# Bellows outer clamp ring (Al) + 6× M4 retaining screws on Ø420 — OUTSIDE the Ø400 labyrinth, on solid frame face
draw_circle(ax1, cx_c, cy_c, s1((BELL_OUT_PCD+14)/2), lw=LW_MED, color=C_OUT, zorder=5)   # ring OD
draw_circle(ax1, cx_c, cy_c, s1((BELL_OUT_PCD-14)/2), lw=LW_MED, color=C_OUT, zorder=5)   # ring ID (bellows large end seats here)
for i in range(6):
    ang = np.radians(i*60)
    bx = cx_c + s1(BELL_OUT_PCD/2) * np.cos(ang)
    by = cy_c + s1(BELL_OUT_PCD/2) * np.sin(ang)
    draw_circle(ax1, bx, by, s1(CLAMP_SCR_D/2 + 0.5), lw=LW_THIN, color=C_OUT, fill=True, fc='#888888', zorder=6)

draw_cl(ax1, cx_c, cy_c, hw*1.15)

# ── Formal dimensions — every feature ──
dia_stack(ax1, cx_c, cy_c - hw, [
    (s1(BRG_SEAT_D),   'Ø80 H7 BEARING SEAT · 50 DEEP'),
    (s1(BELL_OUT_PCD), 'Ø420 PCD · 6× M4 BELLOWS CLAMP-RING SCREW (OUTSIDE LABYRINTH) · 60° APART'),
    (s1(PL_OD),        '600'),
], dirn=-1)
dia_stack(ax1, cx_c, cy_c + hw, [
    (s1(ADJ_PCD), 'Ø270 PCD · 4× M22 BUSHING BORE · 90° APART'),
    (s1(LAB_D3),  'Ø382 / Ø390 / Ø400 — 3-STEP LABYRINTH · 5 DEEP EACH'),
], dirn=+1)
draw_dim_v(ax1, cx_c + hw + 30, cy_c - hw, cy_c + hw, '600', right=True, fs=5.5, offset=20)
ax1.text(cx_c - hw + 12, cy_c + hw - 14, '6061-T6 · 40 THK', ha='left', va='top',
         fontsize=5, color=C_DIM, style='italic', zorder=10)
draw_dim_h(ax1, cx_c - s1(BRG_ID/2), cx_c + s1(BRG_ID/2), cy_c - s1(BRG_ID/2) - 22,
           'Ø50 BORE', above=False, fs=4.3, offset=11)

draw_dim_v(ax1, cx_c - hw - 30, cy_c - s1(BELL_OUT_PCD/2), cy_c + s1(BELL_OUT_PCD/2), 'Ø420 (CLAMP-RING SCREWS)', right=False, fs=5, offset=16)
# ── identifying leaders ──
leader(ax1, cx_c, cy_c + s1(ADJ_PCD/2), cx_c - 120, cy_c + hw - 30,
       '4× M22 ADJ BUSHING', fs=4.4, color=C_DIM, arrow_style='->', ha='right')
leader(ax1, cx_c + s1(BELL_OUT_PCD/2)*np.cos(np.radians(30)), cy_c + s1(BELL_OUT_PCD/2)*np.sin(np.radians(30)),
       cx_c + 120, cy_c + hw - 20, '6× M4 BELLOWS\nCLAMP-RING SCREW', fs=4.4, color=C_DIM, arrow_style='->', ha='left')

ax1.text(cx_c, cy_c - hw - 250, 'PANEL B — ICP-01 INTERIOR (1:8)\n(Bearing pocket + labyrinth + bellows attach)',
         ha='center', fontsize=5, color='#333333', style='italic')

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

title_block(ax2, "SHEET 4 OF 5",
            drawing_title="TILT-SWING FRONT BOARD",
            subtitle="Inner Carrier, Bearing & Adjustment mechanism",
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

# Taper bore (Ø90)
draw_circle(ax2, cx2a, cy2a, s2(PH_BORE/2), lw=LW_MED, color=C_OUT, fill=True, fc='white', zorder=4)

# Counterbore Ø52
draw_circle(ax2, cx2a, cy2a, s2(PH_CB_D/2), lw=LW_MED, color=C_HID, ls='--', zorder=5)
# Pinhole disc Ø50
draw_circle(ax2, cx2a, cy2a, s2(PH_DISC_D/2), lw=LW_THICK, color=C_OUT, fill=True, fc='#707070', zorder=6)
# Pinhole (tiny)
draw_circle(ax2, cx2a, cy2a, 2.0, lw=0.5, color='white', fill=True, fc='white', zorder=7)

# 4 × Ball socket inserts on Ø260
for angle_deg in [90, 0, 270, 180]:
    sx = cx2a + s2(SOCK_PCD/2) * np.cos(np.radians(angle_deg))
    sy = cy2a + s2(SOCK_PCD/2) * np.sin(np.radians(angle_deg))
    draw_circle(ax2, sx, sy, s2(16/2), lw=LW_MED, color=C_OUT, fill=True, fc=C_BEAR, zorder=5)
    draw_circle(ax2, sx, sy, s2(BALL_D/2), lw=0.7, color=C_OUT, fill=True, fc='#D0D0D0', zorder=6)

# Bellows inner clamp ring (Al) + 4× M4 retaining screws on Ø306 — clamps the bellows small end to the carrier
draw_circle(ax2, cx2a, cy2a, s2((BELL_IN_PCD+8)/2), lw=LW_MED, color=C_OUT, zorder=5)   # ring OD
draw_circle(ax2, cx2a, cy2a, s2((BELL_IN_PCD-8)/2), lw=LW_MED, color=C_OUT, zorder=5)   # ring ID (bellows small end seats here)
for i in range(4):
    ang = np.radians(45 + i*90)
    bx = cx2a + s2(BELL_IN_PCD/2) * np.cos(ang)
    by = cy2a + s2(BELL_IN_PCD/2) * np.sin(ang)
    draw_circle(ax2, bx, by, s2(CLAMP_SCR_D/2 + 0.5), lw=LW_THIN, color=C_OUT, fill=True, fc='#888888', zorder=6)

# Bolt circle ref
draw_circle(ax2, cx2a, cy2a, s2(SOCK_PCD/2), lw=0.4, color=C_HID, ls=':')

draw_cl(ax2, cx2a, cy2a, s2(CARR_OD/2)*1.2)

# ── Formal dimensions — every feature ──
dia_stack(ax2, cx2a, cy2a - s2(CARR_OD/2), [
    (s2(PH_BORE),     'Ø90 CONE BORE (SCENE TAPER)'),
    (s2(SOCK_PCD),    'Ø260 PCD · 4× Ø16 H7 SOCKET INSERT · 90° APART'),
    (s2(BELL_IN_PCD), 'Ø306 PCD · 4× M4 BELLOWS CLAMP-RING SCREW · 90° APART'),
    (s2(CARR_OD),     'Ø320 CARRIER OD'),
], dirn=-1, step=42, fs=4.6, off=13)
dia_stack(ax2, cx2a, cy2a + s2(CARR_OD/2), [
    (s2(PH_CB_D), 'Ø52 × 3 DEEP COUNTERBORE (DISC SEAT)'),
], dirn=+1, step=42, fs=4.6, off=13)
draw_dim_v(ax2, cx2a - s2(CARR_OD/2) - 26, cy2a - s2(CARR_OD/2), cy2a + s2(CARR_OD/2), 'Ø320', right=False, fs=5, offset=16)
ax2.text(cx2a - s2(CARR_OD/2) + 8, cy2a + s2(CARR_OD/2) - 10, '6061-T6 · Ø320 × 25 THK', ha='left', va='top', fontsize=4.6, color=C_DIM, style='italic', zorder=10)
draw_dim_h(ax2, cx2a - s2(PH_DISC_D/2), cx2a + s2(PH_DISC_D/2), cy2a - s2(PH_DISC_D/2) - 12,
           'Ø50 DISC (SS-302 · Ø2.17 APERTURE)', above=False, fs=4.0, offset=8)

draw_dim_v(ax2, cx2a + s2(CARR_OD/2) + 26, cy2a - s2(BELL_IN_PCD/2), cy2a + s2(BELL_IN_PCD/2), 'Ø306 (CLAMP-RING SCREWS)', right=True, fs=5, offset=14)
# ── identifying leaders ──
leader(ax2, cx2a, cy2a + s2(SOCK_PCD/2), cx2a - s2(CARR_OD/2) - 8, cy2a + s2(CARR_OD/2) + 34,
       '4× Ø16 SOCKET INSERT', fs=4.2, color=C_DIM, arrow_style='->', ha='right')
leader(ax2, cx2a + s2(BELL_IN_PCD/2)*0.71, cy2a + s2(BELL_IN_PCD/2)*0.71, cx2a + s2(CARR_OD/2) + 8, cy2a + s2(CARR_OD/2) + 34,
       'BELLOWS INNER CLAMP RING (4× M4)', fs=4.2, color=C_DIM, arrow_style='->', ha='left')

ax2.text(cx2a, cy2a - s2(CARR_OD/2) - 250, 'PANEL A — ICP-02 FRONT FACE (1:2)\nExterior / scene-facing side',
         ha='center', fontsize=5, style='italic', color='#333333')

# ── PANEL B: ICP-02 rear face at 1:2 ─────────────────────────────────────────
ax2.text(770, 1540, 'PANEL B — ICP-02 REAR FACE (1:2)', fontsize=7.5, fontweight='bold')
ax2.plot([770, 1370], [1534, 1534], color='black', lw=0.7)

cx2b, cy2b = 1080, 1230

carr_p2 = mpatches.Circle((cx2b, cy2b), s2(CARR_OD/2),
                           lw=LW_THICK, edgecolor=C_OUT, facecolor='#C0C0C0', zorder=3)
ax2.add_patch(carr_p2)

# Bearing shank boss (Ø50 k5) — raised circular boss on rear face
shank_p = mpatches.Circle((cx2b, cy2b), s2(BRG_SHANK_D/2),
                           lw=LW_THICK, edgecolor=C_OUT, facecolor=C_BEAR, zorder=4)
ax2.add_patch(shank_p)

# M8×1.0 tapped central hole (retention bolt — non-structural; downsized from M16, fine pitch)
draw_circle(ax2, cx2b, cy2b, s2(4), lw=LW_MED, color=C_OUT, fill=True, fc='white', zorder=5)

# 4 × socket insert bores (Ø16 H7) — same PCD
for angle_deg in [90, 0, 270, 180]:
    sx = cx2b + s2(SOCK_PCD/2) * np.cos(np.radians(angle_deg))
    sy = cy2b + s2(SOCK_PCD/2) * np.sin(np.radians(angle_deg))
    draw_circle(ax2, sx, sy, s2(16/2), lw=LW_MED, color=C_OUT, fill=True, fc=C_BEAR, zorder=5)

# Bellows groove Ø290
draw_circle(ax2, cx2b, cy2b, s2(BELL_ID/2), lw=LW_MED, color=C_GASKT, ls='--')

draw_cl(ax2, cx2b, cy2b, s2(CARR_OD/2)*1.2)

# ── Formal dimensions — every feature ──
dia_stack(ax2, cx2b, cy2b - s2(CARR_OD/2), [
    (s2(BRG_SHANK_D), 'Ø50 k5 SHANK BOSS · 35 LONG (BEARING INNER)'),
    (s2(SOCK_PCD),    'Ø260 PCD · 4× Ø16 H7 INSERT BORE · 90° APART'),
    (s2(BELL_ID),     'Ø290 BELLOWS GROOVE · 4 WIDE × 3 DEEP'),
    (s2(CARR_OD),     'Ø320 CARRIER OD'),
], dirn=-1, step=42, fs=4.6, off=13)
draw_dim_v(ax2, cx2b + s2(CARR_OD/2) + 26, cy2b - s2(CARR_OD/2), cy2b + s2(CARR_OD/2), 'Ø320', right=True, fs=5, offset=16)
ax2.text(cx2b - s2(CARR_OD/2) + 8, cy2b + s2(CARR_OD/2) - 10, '6061-T6 · Ø320 × 25 THK', ha='left', va='top', fontsize=4.6, color=C_DIM, style='italic', zorder=10)
draw_dim_h(ax2, cx2b - s2(4), cx2b + s2(4), cy2b + s2(BRG_SHANK_D/2) + 16,
           'M8×1.0 TAPPED (CENTRAL RETENTION)', above=True, fs=4.2, offset=10)

draw_dim_v(ax2, cx2b - s2(CARR_OD/2) - 26, cy2b - s2(SOCK_PCD/2), cy2b + s2(SOCK_PCD/2), 'Ø260 B.C. (4× Ø16 INSERT)', right=False, fs=5, offset=14)
# ── identifying leader ──
leader(ax2, cx2b, cy2b + s2(SOCK_PCD/2), cx2b, cy2b + s2(CARR_OD/2) + 34,
       '4× Ø16 INSERT BORE (H7)', fs=4.2, color=C_DIM, arrow_style='->', ha='center')

ax2.text(cx2b, cy2b - s2(CARR_OD/2) - 250, 'PANEL B — ICP-02 REAR FACE (1:2)\nBearing-side / interior',
         ha='center', fontsize=5, style='italic', color='#333333')

# ── PANEL C: Bearing section detail (1:1) ─────────────────────────────────────
ax2.text(30, 430, 'PANEL C — GE50-DO-2RS BEARING SECTION (1:1)', fontsize=7.5, fontweight='bold')
ax2.plot([30, 690], [424, 424], color='black', lw=0.7)

cx2c, cy2c = 290, 250

SC1 = 1.0
def s1b(mm): return mm * SC1

# Outer ring (in ICP-01 pocket)
or_left = cx2c - s1b(BRG_OD/2)
or_right = cx2c + s1b(BRG_OD/2)
or_bot = cy2c - s1b(BRG_W/2)
or_top = cy2c + s1b(BRG_W/2)
# Outer ring walls (left portion)
out_ring_wall = s1b(6)   # outer ring wall thickness
or_p_l = mpatches.Rectangle((or_left, or_bot), out_ring_wall, s1b(BRG_W),
                              lw=LW_THICK, edgecolor=C_OUT, facecolor=C_BEAR)
or_p_r = mpatches.Rectangle((or_right - out_ring_wall, or_bot), out_ring_wall, s1b(BRG_W),
                              lw=LW_THICK, edgecolor=C_OUT, facecolor=C_BEAR)
ax2.add_patch(or_p_l); ax2.add_patch(or_p_r)

# Outer ring top/bottom
or_cap_h = s1b(4)
or_cap_t = mpatches.Rectangle((or_left, or_top - or_cap_h), s1b(BRG_OD), or_cap_h,
                                lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR)
or_cap_b = mpatches.Rectangle((or_left, or_bot), s1b(BRG_OD), or_cap_h,
                                lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR)
ax2.add_patch(or_cap_t); ax2.add_patch(or_cap_b)

# Inner ring
ir_wall = s1b(5)
ir_outer_r = s1b(BRG_OD/2) - out_ring_wall - s1b(2)
ir_inner_r = s1b(BRG_ID/2)
ir_h = s1b(BRG_W) - 2*or_cap_h
ir_y = or_bot + or_cap_h
ir_l = mpatches.Rectangle((cx2c - ir_outer_r, ir_y), ir_wall, ir_h,
                            lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR)
ir_r = mpatches.Rectangle((cx2c + ir_outer_r - ir_wall, ir_y), ir_wall, ir_h,
                            lw=LW_MED, edgecolor=C_OUT, facecolor=C_BEAR)
ax2.add_patch(ir_l); ax2.add_patch(ir_r)

# PTFE liner gap (vertical lines between inner and outer rings)
ptfe_left_x = cx2c - ir_outer_r + ir_wall + s1b(1)
ptfe_right_x = cx2c + ir_outer_r - ir_wall - s1b(1)
ax2.plot([ptfe_left_x, ptfe_left_x], [ir_y, ir_y + ir_h],
         color=C_GASKT, lw=2.0)
ax2.plot([ptfe_right_x, ptfe_right_x], [ir_y, ir_y + ir_h],
         color=C_GASKT, lw=2.0)

# ICP-01 bore context (frame material either side of bearing)
frame_ctx_w = s1b(20)
fc_l = mpatches.Rectangle((or_left - frame_ctx_w, or_bot), frame_ctx_w, s1b(BRG_W),
                            lw=LW_MED, edgecolor=C_OUT, facecolor=C_ALUM)
fc_r = mpatches.Rectangle((or_right, or_bot), frame_ctx_w, s1b(BRG_W),
                            lw=LW_MED, edgecolor=C_OUT, facecolor=C_ALUM)
ax2.add_patch(fc_l); ax2.add_patch(fc_r)

# ICP-02 shank through bearing
shank_p2 = mpatches.Rectangle((cx2c - s1b(BRG_SHANK_D/2), or_bot - s1b(15)),
                               s1b(BRG_SHANK_D), s1b(BRG_W) + s1b(15),
                               lw=LW_MED, edgecolor=C_OUT, facecolor='#C0C0C0')
ax2.add_patch(shank_p2)

# Seals (EPDM lips each end)
for sy in [or_bot, or_top - s1b(3)]:
    seal_p = mpatches.Rectangle((cx2c - ir_outer_r - s1b(1), sy), s1b(2*ir_outer_r + 2), s1b(3),
                                  lw=0.5, edgecolor=C_OUT, facecolor=C_GASKT)
    ax2.add_patch(seal_p)

# Centerline
ax2.plot([cx2c, cx2c], [or_bot - 40, or_top + 40],
         color=C_CL, lw=LW_THIN, linestyle=(0, (6, 2, 1, 2)))

# Dimensions
draw_dim_h(ax2, or_left - frame_ctx_w, or_right + frame_ctx_w, or_top + 24,
           f'Ø{BRG_OD} OD', above=True, fs=5, offset=7.2)
draw_dim_h(ax2, cx2c - s1b(BRG_ID/2), cx2c + s1b(BRG_ID/2), or_bot - 36,
           f'Ø{BRG_ID} BORE', above=False, fs=5, offset=7.2)
draw_dim_v(ax2, or_right + frame_ctx_w + 20, or_bot, or_top, f'{BRG_W}mm WIDE', right=True, fs=5, offset=7.2)

leader(ax2, ptfe_right_x, cy2c,
       cx2c + 170, cy2c + 50,
       'PTFE COMPOSITE\nLINING (2RS SEALED)\n±15° MISALIGN', fs=4.8, color=C_DIM, arrow_style='->')
leader(ax2, or_left - frame_ctx_w/2, cy2c,
       cx2c - 150, cy2c - 70,
       'ICP-01\nFRAME\nAl 6061', fs=4.8, color=C_DIM, arrow_style='->')
leader(ax2, cx2c - 30, or_bot - s1b(8),
       cx2c - 110, cy2c - 80,
       'ICP-02\nSHANK\nØ50 k5', fs=4.8, color=C_DIM, arrow_style='->')
leader(ax2, cx2c + ir_outer_r, or_bot + s1b(1.5),
       cx2c + 150, cy2c - 90,
       'RUBBER\nSEAL (2RS)', fs=4.8, color=C_DIM, arrow_style='->')
leader(ax2, or_right - out_ring_wall/2, or_top,
       cx2c + 170, cy2c + 84,
       'OUTER RING\n(PRESS-FIT H7/r6)', fs=4.8, color=C_DIM, arrow_style='->')

ax2.text(cx2c, or_bot - 56, 'SKF GE50-DO-2RS  (or INA / Kaydon equivalent)\nPress-fit outer ring H7/r6  •  Ø50 k5 shank',
         ha='center', fontsize=5, style='italic', color='#333333')

# ── PANEL D: Adjustment screw detail (1:1) ────────────────────────────────────
ax2.text(720, 430, 'PANEL D — ADJUSTMENT SCREW DETAIL (1:1)', fontsize=7.5, fontweight='bold')
ax2.plot([720, 1390], [424, 424], color='black', lw=0.7)

cx2d, cy2d = 848, 260

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
           cy2d - s1b(KNOB_D/2) - 24, f'BUSH L={BUSH_L}', above=False, fs=5, offset=7.2)

leader(ax2, cx2d + screw_len + s1b(KNOB_H)/2, cy2d + s1b(KNOB_D/2),
       cx2d + screw_len + s1b(KNOB_H) + 24, cy2d + 20,
       f'Ø40 KNURLED KNOB\n{FRONT_BOARD_DETENTS}-DETENT\n{FRONT_BOARD_CLICK_DEG}°/CLICK', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, cx2d - frame_wall_w + bush_w/2, cy2d + s1b(BUSH_OD/2),
       cx2d - frame_wall_w - 50, cy2d + 28,
       'DELRIN/POM\nGUIDE BUSHING\nM22×1.0 OD', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, ball_x2 - s1b(8), cy2d - s1b(BALL_D/2),
       ball_x2 - s1b(8) - 110, cy2d - 36,
       '440C SS INSERT\nHEMI SOCKET\nRa 0.4 GROUND', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, ball_x2, cy2d + s1b(BALL_D/2),
       ball_x2 + 28, cy2d + 24,
       'Ø8 Gr25\nCHROME\nSTEEL BALL', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, ball_x2 - carrier_rim_w/2, cy2d + s1b(CARR_THICK/2),
       ball_x2 - carrier_rim_w - 70, cy2d + 50,
       'ICP-02\nCARRIER RIM', fs=5, color=C_DIM, arrow_style='->')
leader(ax2, cx2d - frame_wall_w/2, cy2d + s1b(30),
       cx2d - frame_wall_w/2, cy2d + s1b(30) + 20,
       'ICP-01\nFRAME WALL', fs=5, color=C_DIM, arrow_style='->')

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

out2 = os.path.join(DIAGRAMS_DIR, 'tilt-swing-sheet4.png')
fig2.savefig(out2, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white')
plt.close(fig2)
print(f'  → {out2}  Done.')


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — Bellows, Locking, Scale & Swap Procedure
# ═══════════════════════════════════════════════════════════════════════════════

FH3_FIG = int(FH * 1.3)
FW3, FH3 = 1400, 880
fig3, ax3 = plt.subplots(figsize=(FW/25.4*0.9, FH3_FIG/25.4*0.9))
fig3.patch.set_facecolor('white')
ax3.set_facecolor('white')
ax3.set_aspect('equal')
ax3.axis('off')
ax3.set_xlim(0, FW3)
ax3.set_ylim(0, FH3)
S3_UP = 40  # panels fill from the top; fixed (was FH3-FH2, which broke when Sheet 4's FH2 changed)

title_block(ax3, "SHEET 5 OF 5",
            drawing_title="TILT-SWING FRONT BOARD",
            subtitle="Bellows seal, Locking, Calibration scale & Swap procedure",
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

# ── PANEL B: Locking set screw detail (1:1) ──────────────────────────────────
ax3.text(30, 490 + S3_UP, 'PANEL B — LOCKING SET SCREW (1:1)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([30, 400], [484 + S3_UP, 484 + S3_UP], color='black', lw=0.7)

cx3b, cy3b = 160, 350 + S3_UP

# M8 screw shaft (horizontal)
m8_sh = mpatches.Rectangle((cx3b - 80, cy3b - 8), 160, 16,
                             lw=LW_MED, edgecolor=C_OUT, facecolor=C_STEEL)
ax3.add_patch(m8_sh)
# M6 set screw (vertical, crossing M8)
m6_sh = mpatches.Rectangle((cx3b - 8, cy3b + 8), 16, 50,
                              lw=LW_MED, edgecolor=C_OUT, facecolor=C_STEEL, zorder=5)
ax3.add_patch(m6_sh)
# Nylon tip at bottom
ny_p = mpatches.Rectangle((cx3b - 6, cy3b + 8), 12, 10,
                            lw=0.5, edgecolor=C_OUT, facecolor='#F0E080', zorder=6)
ax3.add_patch(ny_p)
# Hex key socket (top of M6)
ax3.plot([cx3b - 5, cx3b + 5], [cy3b + 58, cy3b + 58], color=C_OUT, lw=2.0)
ax3.plot([cx3b - 3, cx3b - 3], [cy3b + 54, cy3b + 58], color=C_OUT, lw=1.0)
ax3.plot([cx3b + 3, cx3b + 3], [cy3b + 54, cy3b + 58], color=C_OUT, lw=1.0)
# Boss context (frame)
fr3b = mpatches.Rectangle((cx3b - 80, cy3b - 24), 160, 16,
                            lw=LW_MED, edgecolor=C_OUT, facecolor=C_ALUM)
ax3.add_patch(fr3b)
fr3bt = mpatches.Rectangle((cx3b - 16, cy3b + 58), 32, 20,
                             lw=LW_MED, edgecolor=C_OUT, facecolor=C_ALUM)
ax3.add_patch(fr3bt)

leader(ax3, cx3b + 8, cy3b + 36,
       cx3b + 60, cy3b + 40,
       'M6×1.0\nNYLON-TIP\nSET SCREW', fs=5, color=C_DIM, arrow_style='->')
leader(ax3, cx3b + 80, cy3b - 4,
       cx3b + 60, cy3b - 4,
       'M8×1.0\nADJ SCREW\nSHANK', fs=5, color=C_DIM, arrow_style='->')
leader(ax3, cx3b - 8, cy3b + 12,
       cx3b - 80, cy3b + 20,
       'NYLON\nTIP', fs=5, color=C_DIM, arrow_style='->')
ax3.text(cx3b + 6, cy3b + 62, '3mm HEX', fontsize=4.5, color='#333333', zorder=10)
ax3.text(cx3b, cy3b - 56, 'Tighten set screw onto adj screw shank\nafter desired angle is set. 4 off (one per axis)',
         ha='center', fontsize=4.8, style='italic', color='#333333', zorder=10)

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
       cx3c + 110, cy3c - 20,
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
           '15 (× 2 THK)', right=True, fs=5, offset=6)
ax3.text(cx3d, cy3d - scale_strip_h/2 - 40,
         '2 off — one for TILT, one for SWING\nLaser-engraved Al 80×15×2mm  •  Mounted on ICP-01 face adjacent to each knob pair',
         ha='center', fontsize=5, style='italic', color='#333333', zorder=10)

S3_E_DN = 0

# ── Separator line between panels B/C/D and panel E ──────────────────────────
ax3.plot([30, 1370], [270 + S3_UP - S3_E_DN, 270 + S3_UP - S3_E_DN], color='#999999', lw=0.5, linestyle='--', zorder=5)

# ── PANEL E: Swap sequence ────────────────────────────────────────────────────
ax3.text(30, 250 + S3_UP - S3_E_DN, 'PANEL E — PLATE SWAP PROCEDURE (TSB ASSY ↔ STANDARD PINHOLE PLATE)', fontsize=7.5, fontweight='bold', zorder=10)
ax3.plot([30, 1390], [244 + S3_UP - S3_E_DN, 244 + S3_UP - S3_E_DN], color='black', lw=0.7)

steps = [
    ('①', 'LOOSEN 4×\nLOCK SCREWS', '3mm hex key\nM6 set screws'),
    ('②', 'ZERO ALL\n4 ADJ KNOBS', 'Return to 0°\nusing scale marks'),
    ('③', 'REMOVE 8×\nM12 BOLTS', 'M12 socket\n65 Nm torque'),
    ('④', 'PULL TSB\nASSEMBLY', 'Dowel pins\nretain alignment'),
    ('⑤', 'FIT STANDARD\nPINHOLE PLATE', 'Locate on same\ndowels — re-bolt'),
]

step_w = 240
step_gap = 30
for i, (num, title, note) in enumerate(steps):
    sx = 40 + i * (step_w + step_gap)
    sy = 120 + S3_UP - S3_E_DN
    draw_rect(ax3, sx, sy, step_w, 110, lw=1.0, color='black', fc='#F0F0F0')
    ax3.text(sx + step_w/2, sy + 96, num, ha='center', fontsize=14,
             fontweight='bold', color='black', zorder=10)
    ax3.text(sx + step_w/2, sy + 64, title, ha='center', fontsize=6.5,
             fontweight='bold', color='black', zorder=10)
    ax3.text(sx + step_w/2, sy + 24, note, ha='center', fontsize=5.5,
             color='#555555', style='italic', zorder=10)
    if i < 4:
        ax3.annotate('', xy=(sx + step_w + 26, sy + 54), xytext=(sx + step_w + 4, sy + 54),
                     arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

ax3.text(1390/2, 90 + S3_UP - S3_E_DN, 'No special tooling required beyond M12 socket and 3mm hex key  •  Swap time: approx. 10 minutes',
         ha='center', fontsize=5.5, color='#333333', style='italic', zorder=10)

out3 = os.path.join(DIAGRAMS_DIR, 'tilt-swing-sheet5.png')
fig3.savefig(out3, dpi=DIAGRAM_DPI, bbox_inches='tight', facecolor='white')
plt.close(fig3)
print(f'  → {out3}  Done.')
