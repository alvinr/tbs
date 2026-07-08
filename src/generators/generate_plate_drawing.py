#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
Fabrication drawings: Interchangeable Optical Plate System
Giant Pinhole Camera — Option B

Sheet 1: Front views — Wall Frame, Pinhole Plate, Lens Plate (1:8 scale)
Sheet 2: Assembly section A-A + detail views (1:4 and 2:1)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
from tbs_constants import (DIAGRAMS_DIR, PH_D,
                           PLATE_OD, PLATE_THK, WALL_FRAME_T, PINHOLE_DISC_D, PINHOLE_DISC_T)
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, draw_cl, draw_circle, draw_rect, leader, bolt_holes, draw_notes

# ── Real dimensions (mm) ─────────────────────────────────────────────────────
PL_OD      = PLATE_OD        # plate outer dimension (square) — tbs_constants
PL_THICK   = PLATE_THK       # aluminum plate thickness — tbs_constants
FR_THICK   = WALL_FRAME_T    # wall frame steel thickness — tbs_constants
FR_APT_D   = 350      # wall frame circular aperture diameter
BOLT_BC    = 540      # bolt circle diameter
BOLT_D     = 13       # bolt hole clearance diameter
BOLT_N     = 8        # bolt count
DWL_D      = 8        # dowel pin diameter
DWL_OFF    = 200      # dowel pin offset ± from center
SEAL_D     = 420      # neoprene groove centerline diameter
SEAL_W     = 3        # seal groove width
SEAL_DEP   = 3        # seal groove depth
TRAP_SQ    = 490      # light-trap rebate centered square
TRAP_W     = 5        # rebate width
TRAP_DEP   = 5        # rebate depth
# Pinhole plate
PH_BORE    = 90       # light-admission taper bore (exterior face)
PH_CB_D    = 52       # pinhole disc counterbore diameter (interior face)
PH_CB_DEP  = 3        # counterbore depth
PH_DISC_D  = PINHOLE_DISC_D  # pinhole disc OD (Lenox Laser supply) — tbs_constants
PH_DISC_T  = PINHOLE_DISC_T  # pinhole disc thickness (SS) — tbs_constants
PH_APT     = PH_D            # pinhole aperture — tbs_constants (= PH_D)
# Lens plate
LB_D       = 175      # lens bore diameter (H7)
LT_OD      = 174.5    # lens tube OD (g6 fit)
LT_ID      = 165      # lens tube inner bore
LT_L       = 100      # lens tube length
LT_TRAVEL  = 40       # ±40mm rack travel
# Container wall
WALL_T     = 2.0      # container steel wall thickness (nominal)
WALL_APT   = 360      # hole cut through container wall (≥ frame aperture)

# ── Drawing helpers ───────────────────────────────────────────────────────────
LW_THICK  = 1.8
LW_MED    = 1.0
LW_THIN   = 0.5
LW_CUT    = 2.2
LW_DIM    = 0.7

C_OUT   = '#000000'
C_CL    = '#0055AA'   # center-line blue
C_DIM   = '#333333'
C_HID   = '#888888'
C_STEEL = '#B0B0B0'
C_ALUM  = '#D8D8D8'
C_GASKT = '#404040'
C_RED   = '#CC0000'   # section-cut arrows


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — FRONT VIEWS
# ═══════════════════════════════════════════════════════════════════════════════

def draw_sheet1():
    fig, ax1 = plt.subplots(figsize=(12.54, 11.2))
    fig.patch.set_facecolor('white')
    ax1.set_facecolor('white')
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_xlim(0, 2509)
    ax1.set_ylim(0, 2240)

    SC = 1
    def s(mm): return mm * SC

    # ── Border and title block ────────────────────────────────────────────────
    draw_rect(ax1, 18, 32, 2473, 2176, lw=1.5, color='black', fc='white')

    title_block(ax1, "SHEET 1 OF 2",
                drawing_title="OPTICAL PLATE SYSTEM",
                subtitle="Part front views — Al 6061-T6 / S275 steel",
                scale_note="AXES IN mm (views at 1:8)",
                doc_id="TBS-001 · Interchangeable Plates", height=0.04)

    # ── Parts list (notes block) ──────────────────────────────────────────────
    parts_notes = [
        'PARTS LIST:',
        '1. WALL FRAME          • S275 steel 6mm (×1)              • weld to container wall; machine face after welding',
        '2. PINHOLE PLATE       • Al 6061-T6, 15mm (×1)            • black anodize all faces; interior faces matt black',
        '3. PINHOLE DISC        • SS-302 0.10mm, Lenox Laser (×1+) • Ø50 disc, Ø2.17 aperture ±0.025mm; order spares',
        '4. DISC RETAINING RING • Al 6061-T6 (×1)                  • Ø52 bore × M52×0.75 thread; 3× M4 grub screws',
        '5. LENS PLATE          • Al 6061-T6, 15mm (×1)            • black anodize; Ø175 bore H7; interior faces matt black',
        '6. LENS TUBE           • Al 6061-T6 (×1)                  • Ø174.5g6 × Ø165 bore × 100L; 3× M8 set screws at 120°',
        '7. LOCATING DOWEL PIN  • SS-303 Ø8 m6 × 40L (×2)          • press fit to wall frame (H7 reamed holes)',
        '8. SOCKET HEAD BOLT    • M12 × 40mm A2-70 stainless (×8)  • with M12 flat washer each; torque to 43 Nm',
        '9. NEOPRENE CORD SEAL  • Ø3mm neoprene, 70 Shore (×1)     •  Ø420mm loop in 3×3 groove on wall frame face',
    ]
    draw_notes(ax1, parts_notes, 550, 550, spacing=38, fs=7, width=1400,
               font={"fontfamily": "monospace"})

    # ── View titles ───────────────────────────────────────────────────────────
    view_titles = [
        (410, 2020, 'ITEM 1 — WALL FRAME (Steel)', '(Interior face shown)'),
        (1230, 2020, 'ITEM 2 — PINHOLE PLATE (Al)', '(Interior face shown)'),
        (2050, 2020, 'ITEM 3 — LENS PLATE (Al)', '(Interior face shown)'),
    ]
    for tx, ty, t1, t2 in view_titles:
        ax1.text(tx, ty, t1, ha='center', fontsize=7.5, fontweight='bold', color='black')
        ax1.text(tx, ty - 45, t2, ha='center', fontsize=6, color='#555555', style='italic')

    # ══════════════════════════════════════════════════════════
    # ITEM 1: WALL FRAME
    # ══════════════════════════════════════════════════════════
    cx1, cy1 = 410, 1500
    hw = s(PL_OD/2)
    draw_rect(ax1, cx1 - hw, cy1 - hw, s(PL_OD), s(PL_OD),
              lw=LW_THICK, color=C_OUT, fc=C_STEEL)
    draw_circle(ax1, cx1, cy1, s(FR_APT_D/2), lw=LW_THICK, color=C_OUT, fc='white', fill=True)
    draw_circle(ax1, cx1, cy1, s(SEAL_D/2), lw=LW_THIN, color=C_HID, ls='--')
    draw_circle(ax1, cx1, cy1, s(BOLT_BC/2), lw=0.4, color=C_HID, ls=':')
    bolt_holes(ax1, cx1, cy1, s(BOLT_BC/2), BOLT_N, s(BOLT_D/2), color=C_OUT, lw=LW_MED)

    for sign in [-1, 1]:
        dx = cx1 + sign * s(DWL_OFF)
        draw_circle(ax1, dx, cy1, s(DWL_D/2), lw=LW_MED, color=C_OUT)
        ax1.plot([dx - s(4), dx + s(4)], [cy1, cy1], color=C_CL, lw=0.5,
                 linestyle=(0, (4, 2)))
        ax1.plot([dx, dx], [cy1 - s(4), cy1 + s(4)], color=C_CL, lw=0.5,
                 linestyle=(0, (4, 2)))

    draw_cl(ax1, cx1, cy1, hw * 1.1)

    # Section cut line A-A
    ax1.plot([cx1 - hw - 64, cx1 + hw + 64], [cy1, cy1],
             color=C_RED, lw=LW_CUT, linestyle=(0, (8, 3)))
    for sign in [-1, 1]:
        ax1.annotate('', xy=(cx1 + sign*(hw + 54), cy1 + sign*40),
                     xytext=(cx1 + sign*(hw + 54), cy1),
                     arrowprops=dict(arrowstyle='->', color=C_RED, lw=1.5))
    ax1.text(cx1 - hw - 75, cy1 + 24, 'A', ha='center', fontsize=8,
             fontweight='bold', color=C_RED)
    ax1.text(cx1 + hw + 75, cy1 + 24, 'A', ha='center', fontsize=8,
             fontweight='bold', color=C_RED)

    # Dimensions
    dim_y_top = cy1 + hw + 112
    dim_x_right = cx1 + hw + 144
    draw_dim_h(ax1, cx1 - hw, cx1 + hw, dim_y_top, '600mm', above=True, fs=6, offset=64)
    draw_dim_v(ax1, dim_x_right, cy1 - hw, cy1 + hw, '600mm', right=True, fs=6, offset=64)
    leader(ax1, cx1 + s(FR_APT_D/2)*0.65, cy1 + s(FR_APT_D/2)*0.65,
           cx1 + 96, cy1 + 80, 'Ø350', fs=5.5, color=C_DIM)
    leader(ax1, cx1 + s(BOLT_BC/2)*0.6, cy1 - s(BOLT_BC/2)*0.6,
           cx1 + 120, cy1 - 144, 'Ø540 B.C.\n8×Ø13', fs=5, color=C_DIM)
    leader(ax1, cx1 - s(SEAL_D/2)*0.7, cy1 + s(SEAL_D/2)*0.7,
           cx1 - 144, cy1 + 176, 'Ø420\nSEAL GRV\n3×3 DEEP', fs=4.8, color=C_DIM)
    leader(ax1, cx1 - s(DWL_OFF), cy1 - s(DWL_D/2),
           cx1 - s(DWL_OFF) - 48, cy1 - 96,
           '2×Ø8 H7\nDOWEL\n(±200)', fs=4.8, color=C_DIM)

    ax1.text(cx1, cy1 - hw - 80, '1', ha='center', va='center', fontsize=10,
             fontweight='bold', color='white',
             bbox=dict(boxstyle='circle,pad=0.3', fc='black', ec='black'))

    # ══════════════════════════════════════════════════════════
    # ITEM 2: PINHOLE PLATE
    # ══════════════════════════════════════════════════════════
    cx2, cy2 = 1230, 1500
    draw_rect(ax1, cx2 - hw, cy2 - hw, s(PL_OD), s(PL_OD),
              lw=LW_THICK, color=C_OUT, fc=C_ALUM)

    trap_h = s(TRAP_SQ/2)
    trap_corners = [
        (cx2 - trap_h, cy2 - trap_h),
        (cx2 + trap_h, cy2 - trap_h),
        (cx2 + trap_h, cy2 + trap_h),
        (cx2 - trap_h, cy2 + trap_h),
        (cx2 - trap_h, cy2 - trap_h),
    ]
    ax1.plot([p[0] for p in trap_corners], [p[1] for p in trap_corners],
             color=C_HID, lw=LW_THIN, linestyle='--', zorder=5)

    draw_circle(ax1, cx2, cy2, s(PH_BORE/2), lw=LW_THICK, color=C_OUT, fc='white', fill=True)
    draw_circle(ax1, cx2, cy2, s(PH_CB_D/2), lw=LW_THIN, color=C_HID, ls='--')
    draw_circle(ax1, cx2, cy2, 3.2, lw=1.5, color=C_OUT, fc=C_OUT, fill=True)
    bolt_holes(ax1, cx2, cy2, s(BOLT_BC/2), BOLT_N, s(BOLT_D/2), color=C_OUT, lw=LW_MED)
    draw_circle(ax1, cx2, cy2, s(BOLT_BC/2), lw=0.4, color=C_HID, ls=':')

    for sign in [-1, 1]:
        dx = cx2 + sign * s(DWL_OFF)
        draw_circle(ax1, dx, cy2, s(DWL_D/2), lw=LW_MED, color=C_OUT)

    draw_cl(ax1, cx2, cy2, hw * 1.1)

    dim_y_top2 = cy2 + hw + 112
    draw_dim_h(ax1, cx2 - hw, cx2 + hw, dim_y_top2, '600mm', above=True, fs=6, offset=64)
    draw_dim_h(ax1, cx2 - trap_h, cx2 + trap_h, dim_y_top2 - 48,
               '490 (LIGHT TRAP)', above=True, fs=5, offset=64)

    leader(ax1, cx2 + s(PH_BORE/2)*0.6, cy2 + s(PH_BORE/2)*0.6,
           cx2 + 112, cy2 + 96, 'Ø90\nBORE THRU', fs=5.5, color=C_DIM)
    leader(ax1, cx2 + s(PH_CB_D/2)*0.6, cy2 - s(PH_CB_D/2)*0.6,
           cx2 + 128, cy2 - 80, 'Ø52×3 C\'BORE\nM52×0.75 THD\n(RING ITEM 4)', fs=4.8, color=C_DIM)
    leader(ax1, cx2, cy2,
           cx2 - 144, cy2 + 40, 'Ø2.17\nPINHOLE\n(DISC)', fs=5.0, color=C_DIM)
    leader(ax1, cx2 - trap_h, cy2 - trap_h + 16,
           cx2 - 176, cy2 - 160, '5×5 REBATE\n(LIGHT TRAP)', fs=4.8, color=C_DIM)

    ax1.text(cx2, cy2 - hw - 80, '2', ha='center', va='center', fontsize=10,
             fontweight='bold', color='white',
             bbox=dict(boxstyle='circle,pad=0.3', fc='black', ec='black'))

    # ══════════════════════════════════════════════════════════
    # ITEM 3: LENS PLATE
    # ══════════════════════════════════════════════════════════
    cx3, cy3 = 2050, 1500
    draw_rect(ax1, cx3 - hw, cy3 - hw, s(PL_OD), s(PL_OD),
              lw=LW_THICK, color=C_OUT, fc=C_ALUM)

    ax1.plot(
        [cx3 + sign_x*trap_h for sign_x in [-1, 1, 1, -1, -1]],
        [cy3 + sign_y*trap_h for sign_y in [-1, -1, 1, 1, -1]],
        color=C_HID, lw=LW_THIN, linestyle='--', zorder=5)

    draw_circle(ax1, cx3, cy3, s(LB_D/2), lw=LW_THICK, color=C_OUT, fc='white', fill=True)
    draw_circle(ax1, cx3, cy3, s(LT_OD/2), lw=LW_THIN, color=C_HID, ls='--')
    draw_circle(ax1, cx3, cy3, s(LT_ID/2), lw=LW_THIN, color=C_HID, ls=':')

    for angle_deg in [90, 210, 330]:
        angle_r = np.radians(angle_deg)
        ssx = cx3 + s(LB_D/2 + 5) * np.cos(angle_r)
        ssy = cy3 + s(LB_D/2 + 5) * np.sin(angle_r)
        draw_circle(ax1, ssx, ssy, 9.6, lw=LW_MED, color=C_OUT)

    for xo in [-s(100), -s(50), s(50), s(100)]:
        ax1.plot([cx3 + xo], [cy3 + hw - s(30)], 'x', color='#888', ms=4, lw=0.7)

    bolt_holes(ax1, cx3, cy3, s(BOLT_BC/2), BOLT_N, s(BOLT_D/2), color=C_OUT, lw=LW_MED)
    draw_circle(ax1, cx3, cy3, s(BOLT_BC/2), lw=0.4, color=C_HID, ls=':')

    for sign in [-1, 1]:
        dx = cx3 + sign * s(DWL_OFF)
        draw_circle(ax1, dx, cy3, s(DWL_D/2), lw=LW_MED, color=C_OUT)

    draw_cl(ax1, cx3, cy3, hw * 1.1)

    dim_y_top3 = cy3 + hw + 112
    draw_dim_h(ax1, cx3 - hw, cx3 + hw, dim_y_top3, '600mm', above=True, fs=6, offset=64)

    leader(ax1, cx3 + s(LB_D/2)*0.65, cy3 + s(LB_D/2)*0.65,
           cx3 + 128, cy3 + 128, 'Ø175 H7\nBORE THRU', fs=5.5, color=C_DIM)
    leader(ax1, cx3 + s(LT_OD/2)*0.65, cy3 - s(LT_OD/2)*0.65,
           cx3 + 160, cy3 - 96, 'Ø174.5 g6\nLENS TUBE\n(ITEM 6)', fs=4.8, color=C_DIM)
    leader(ax1, cx3 + s(LB_D/2 + 5)*np.cos(np.radians(150)),
           cy3 + s(LB_D/2 + 5)*np.sin(np.radians(150)),
           cx3 - 160, cy3 + 128, '3×M8\nSET SCREWS\n@ 120°', fs=4.8, color=C_DIM)
    leader(ax1, cx3 - s(60), cy3 + hw - s(30),
           cx3 - 120, cy3 + hw - s(30) + 64, 'SHUTTER\nRAIL HOLES\n4×Ø6.5', fs=4.8, color=C_DIM)

    ax1.text(cx3, cy3 - hw - 80, '3', ha='center', va='center', fontsize=10,
             fontweight='bold', color='white',
             bbox=dict(boxstyle='circle,pad=0.3', fc='black', ec='black'))

    # ── Notes block ───────────────────────────────────────────────────────────
    notes = [
        'GENERAL NOTES:',
        '1. ALL DIMENSIONS IN MILLIMETERS. DO NOT SCALE DRAWING.',
        '2. ITEMS 2 AND 3: CRITICAL BORE Ø175 H7 AND DOWEL HOLES Ø8 H7 — MATCH REAM PAIRS.',
        '3. LIGHT TRAP REBATE: 5mm WIDE × 5mm DEEP SQUARE STEP ON MATING (INTERIOR) FACE OF ITEMS 2 & 3.',
        '4. ALL INTERIOR FACES OF ITEMS 1, 2, 3: MATT BLACK FINISH — ITEM 1: CHEMICAL BLACKEN; ITEMS 2&3: BLACK ANODIZE.',
        '5. PINHOLE DISC (ITEM 3): PROCURE FROM LENOX LASER (lenoxlaser.com) Ø50mm SS-302, Ø2.17mm ±0.025mm APERTURE.',
        '6. ITEM 1 WELD TO CONTAINER WALL: FULL PERIMETER 6mm FILLET. MACHINE FACE FLAT Ra 1.6 AFTER WELDING.',
        '7. INTERCHANGEABILITY: ALL BOLT AND DOWEL PATTERNS IDENTICAL ON ITEMS 2 & 3 — SWAP IN DARK WITHOUT TOOLS.',
        '8. SHUTTER PROVISION: ITEMS 2 & 3 HAVE 4×Ø6.5 HOLES AT TOP FACE FOR SLIDING SHUTTER RAIL — SEE SHEET 2.',
    ]
    draw_notes(ax1, notes, 550, 1000, spacing=38, fs=7, width=1400)

    plt.tight_layout(pad=0)
    out1 = f'{DIAGRAMS_DIR}/plate-drawing-sheet1.png'
    fig.savefig(out1, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  → plate-drawing-sheet1.png  Done.')


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — SECTION A-A + DETAIL VIEWS
# ═══════════════════════════════════════════════════════════════════════════════

def draw_sheet2():
    fig, ax2 = plt.subplots(figsize=(14, 16))
    fig.patch.set_facecolor('white')
    ax2.set_facecolor('white')
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_xlim(0, 1400)
    ax2.set_ylim(0, 1600)

    # Border
    draw_rect(ax2, 20, 20, 1360, 1560, lw=1.5, color='black', fc='white')

    title_block(ax2, "SHEET 2 OF 2",
                drawing_title="OPTICAL PLATE SYSTEM",
                subtitle="Section A-A & details (1:4 / 2:1)",
                scale_note="AXES IN mm (as noted)",
                doc_id="TBS-001 · Interchangeable Plates")

    # ──────────────────────────────────────────────────────────────────────────
    # SECTION A-A  (1:4 scale)
    # ──────────────────────────────────────────────────────────────────────────
    SC4 = 1
    def ss(mm): return mm * SC4

    scx, scy = 472, 1200

    ax2.text(scx, scy + 340, 'SECTION A-A', ha='center',
             fontsize=9, fontweight='bold', color='black')
    ax2.text(scx, scy + 316, '(Pinhole Plate installed)  1:4 SCALE', ha='center',
             fontsize=7, color='#555')

    # Container wall
    wall_left  = scx - ss(340)
    wall_right = wall_left + ss(WALL_T)
    wall_h = ss(280)
    ax2.add_patch(mpatches.Rectangle((wall_left, scy - wall_h/2), ss(WALL_T), wall_h,
                  fc=C_STEEL, ec=C_OUT, lw=LW_MED, zorder=3))
    for i in range(int(wall_h/12)+1):
        y0 = scy - wall_h/2 + i*12
        ax2.plot([wall_left, wall_left + ss(WALL_T)], [y0, y0 + ss(WALL_T)],
                 color='#888', lw=0.4, clip_on=True)

    apt_half = ss(WALL_APT/2)
    for region in [(-wall_h/2, -apt_half), (apt_half, wall_h/2)]:
        y_bot = scy + region[0]
        y_top = scy + region[1]
        ax2.add_patch(mpatches.Rectangle((wall_left, y_bot), ss(WALL_T), y_top - y_bot,
                      fc=C_STEEL, ec=C_OUT, lw=LW_MED, zorder=4))
        for i in range(int((y_top-y_bot)/12)+1):
            y0 = y_bot + i*12
            if y_bot <= y0 <= y_top:
                ax2.plot([wall_left, wall_left + ss(WALL_T)], [y0, y0 + ss(WALL_T)],
                         color='#888', lw=0.4)

    ax2.text(wall_left - 12, scy-36, 'CONTAINER\nWALL\n(2mm steel)', ha='right',
             va='center', fontsize=5, color='#444')

    # Wall Frame
    fr_left  = wall_right
    fr_right = fr_left + ss(FR_THICK)
    fr_half  = ss(PL_OD/2)
    fr_apt_half = ss(FR_APT_D/2)
    for region in [(-fr_half, -fr_apt_half), (fr_apt_half, fr_half)]:
        y_bot = scy + region[0]
        y_top = scy + region[1]
        ax2.add_patch(mpatches.Rectangle((fr_left, y_bot), ss(FR_THICK), y_top - y_bot,
                      fc=C_STEEL, ec=C_OUT, lw=LW_MED, zorder=5))
        for i in range(int((y_top-y_bot)/10)+1):
            y0 = y_bot + i*10
            if y_bot <= y0 <= y_top:
                ax2.plot([fr_left, fr_right], [y0, y0 + ss(FR_THICK)],
                         color='#666', lw=0.4)

    seal_half = ss(SEAL_D/2)
    for sign in [-1, 1]:
        groove_y = scy + sign * seal_half
        ax2.add_patch(mpatches.Rectangle(
            (fr_right - ss(SEAL_W), groove_y - sign*ss(SEAL_W/2)),
            ss(SEAL_W), ss(SEAL_DEP), fc='#AAAAAA', ec=C_OUT, lw=0.5, zorder=6))
        ax2.add_patch(mpatches.Circle(
            (fr_right - ss(SEAL_W/2), groove_y - sign*ss(SEAL_W/4) + sign*ss(1.5)),
            ss(1.5), fc=C_GASKT, ec='none', zorder=7))

    ax2.text(fr_right + 24, scy + fr_half*0.6, 'ITEM 1\nWALL FRAME\n6mm STEEL', ha='left',
             va='center', fontsize=5.5, color='black')
    draw_dim_h(ax2, fr_left, fr_right, scy + fr_half + 32, '6', above=True, fs=5.5, offset=7.2)

    # Pinhole Plate
    pl_left  = fr_right
    pl_right = pl_left + ss(PL_THICK)
    pl_half  = ss(PL_OD/2)
    trap_half = ss(TRAP_SQ/2)

    bore_half_top = ss(PH_BORE/2)
    for region in [(-pl_half, -bore_half_top), (bore_half_top, pl_half)]:
        y_bot = scy + region[0]
        y_top = scy + region[1]
        ax2.add_patch(mpatches.Rectangle((pl_left, y_bot), ss(PL_THICK), y_top - y_bot,
                      fc=C_ALUM, ec=C_OUT, lw=LW_MED, zorder=5))
        for i in range(int((y_top - y_bot)/12)+1):
            y0 = y_bot + i*12
            if y_bot <= y0 <= y_top:
                ax2.plot([pl_left, pl_right], [y0, y0 + ss(3)], color='#AAAAAA', lw=0.4)

    for sign in [-1, 1]:
        step_y = scy + sign * trap_half
        ax2.add_patch(mpatches.Rectangle(
            (pl_left, step_y - sign*ss(TRAP_W)),
            ss(TRAP_DEP), sign*ss(TRAP_W) * sign,
            fc='white', ec=C_OUT, lw=LW_MED, zorder=6))

    cb_half = ss(PH_CB_D/2)
    ax2.add_patch(mpatches.Rectangle(
        (pl_right - ss(PH_CB_DEP), scy - cb_half),
        ss(PH_CB_DEP), ss(PH_CB_D),
        fc='white', ec=C_OUT, lw=LW_MED, zorder=6))

    ext_bore_half = ss(PH_BORE/2)
    int_bore_half = ss(PH_CB_D/2)
    for sign in [-1, 1]:
        ax2.plot([pl_left, pl_right - ss(PH_CB_DEP)],
                 [scy + sign*ext_bore_half, scy + sign*int_bore_half],
                 color=C_OUT, lw=LW_THICK, zorder=7)

    ax2.add_patch(mpatches.Rectangle(
        (pl_right - ss(PH_CB_DEP), scy - ss(PH_DISC_D/2)),
        ss(PH_DISC_T * 30), ss(PH_DISC_D),
        fc='#888', ec=C_OUT, lw=1.2, zorder=8))
    ax2.text(pl_right + 12, scy - ss(PH_DISC_D/2) - 20,
             'ITEM 3\nPINHOLE DISC\n(Ø50 × 0.1mm SS)', fontsize=5, color='black',
             ha='left')

    bolt_y = scy + ss(BOLT_BC/2 * 0.5)
    bolt_x_fr  = fr_left
    bolt_x_end = pl_right + ss(10)
    ax2.add_patch(mpatches.Rectangle((bolt_x_fr, bolt_y - ss(6)), ss(PL_THICK + FR_THICK + 10),
                  ss(12), fc='#CCCCCC', ec=C_OUT, lw=0.8, zorder=6, alpha=0.6))
    ax2.plot([bolt_x_fr, bolt_x_end], [bolt_y, bolt_y], color='#444', lw=0.7, ls='--')
    ax2.text(bolt_x_end + 8, bolt_y + 8, 'M12×40\nITEM 8', fontsize=4.5, color='black')

    draw_dim_h(ax2, pl_left, pl_right, scy + pl_half + 32, '15\nmm', above=True, fs=5.5, offset=7.2)

    dim_rx = pl_right + 88
    draw_dim_v(ax2, dim_rx, scy - pl_half, scy + pl_half, '600mm', right=True, fs=5.5, offset=7.2)

    ax2.annotate('', xy=(fr_left, scy + fr_apt_half),
                 xytext=(fr_left, scy - fr_apt_half),
                 arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM, mutation_scale=5))
    ax2.text(fr_left - 64, scy+12, 'Ø350\nAPT', ha='center', fontsize=5, color=C_DIM)

    ax2.annotate('', xy=(pl_left, scy + ext_bore_half),
                 xytext=(pl_left, scy - ext_bore_half),
                 arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM, mutation_scale=5))
    ax2.text(pl_left - 40, scy, 'Ø90\nBORE', ha='center', fontsize=5, color=C_DIM)

    ax2.annotate('', xy=(pl_right, scy + cb_half),
                 xytext=(pl_right, scy - cb_half),
                 arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM, mutation_scale=5))
    ax2.text(pl_right + 16, scy + 48, 'Ø52×3 DEEP\nM52×0.75\nTHD', ha='left', fontsize=5, color=C_DIM)

    ax2.text(pl_left + ss(PL_THICK)*0.5, scy - pl_half + 24, '2', ha='center', va='center',
             fontsize=8, fontweight='bold', color='white',
             bbox=dict(boxstyle='circle,pad=0.25', fc='black', ec='black'))

    ax2.annotate('', xy=(pl_right + 180, scy), xytext=(wall_left - 80, scy),
                 arrowprops=dict(arrowstyle='->', color='#0055BB', lw=1.5))
    ax2.text(pl_right + 200, scy + 12, 'OPTICAL\nAXIS', ha='left', fontsize=6,
             color='#0055BB', style='italic')

    ax2.text(wall_left - 20, scy + pl_half*0.8, 'EXTERIOR\n(SCENE)', ha='right',
             fontsize=6.5, color='#333', style='italic')
    ax2.text(pl_right + 40, scy + pl_half*0.8, 'INTERIOR\n(CAMERA)', ha='left',
             fontsize=6.5, color='#333', style='italic')

    ax2.text(scx, scy - pl_half - 48, 'SECTION A-A', ha='center', fontsize=8,
             fontweight='bold', color=C_RED)
    ax2.text(scx, scy - pl_half - 72, '1:4 scale', ha='center',
             fontsize=6, color='#555')

    # ──────────────────────────────────────────────────────────────────────────
    # DETAIL B: Pinhole disc seat  (2:1 scale)
    # ──────────────────────────────────────────────────────────────────────────
    SC5 = 8.0
    def sb(mm): return mm * SC5

    dbx, dby = 800, 1200

    ax2.text(dbx, dby + 340, 'DETAIL B — DISC SEAT', ha='center',
             fontsize=8, fontweight='bold')
    ax2.text(dbx, dby + 316, '2:1 SCALE', ha='center', fontsize=6, color='#555')

    SHOWN_W = 40
    face_x = dbx
    plate_show_left = face_x - sb(SHOWN_W)

    ax2.add_patch(mpatches.Rectangle(
        (plate_show_left, dby - sb(PH_CB_D/2 + 10)),
        sb(SHOWN_W), sb(PH_CB_D + 20),
        fc=C_ALUM, ec=C_OUT, lw=LW_MED, zorder=3))
    for i in range(30):
        y0 = dby - sb(PH_CB_D/2 + 10) + i * 20
        ax2.plot([plate_show_left, face_x], [y0, y0 + 20],
                 color='#AAAAAA', lw=0.4, clip_on=True)

    cb_show_half = sb(PH_CB_D/2)
    ax2.add_patch(mpatches.Rectangle(
        (face_x - sb(PH_CB_DEP), dby - cb_show_half),
        sb(PH_CB_DEP), sb(PH_CB_D),
        fc='white', ec=C_OUT, lw=LW_MED, zorder=5))

    disc_shown_t = sb(0.8)
    disc_half = sb(PH_DISC_D/2)
    ax2.add_patch(mpatches.Rectangle(
        (face_x - sb(PH_CB_DEP), dby - disc_half),
        disc_shown_t, sb(PH_DISC_D),
        fc='#555', ec=C_OUT, lw=1.0, zorder=6))

    ph_r = sb(PH_APT/2)
    ax2.add_patch(mpatches.Rectangle(
        (face_x - sb(PH_CB_DEP), dby - ph_r),
        disc_shown_t, sb(PH_APT),
        fc='white', ec='white', lw=0, zorder=7))

    ring_half = sb(PH_CB_D/2 + 1.5)
    ring_depth = sb(3)
    for sign in [-1, 1]:
        ax2.add_patch(mpatches.Rectangle(
            (face_x - ring_depth, dby + sign*sb(PH_CB_D/2)),
            ring_depth, sign*sb(3),
            fc='#CCCCCC', ec=C_OUT, lw=0.8, zorder=6))

    draw_dim_h(ax2, face_x - sb(PH_CB_DEP), face_x, dby + cb_show_half + 24,
               '3.0 DEEP', above=True, fs=5.5, offset=6)
    ax2.annotate('', xy=(face_x, dby + cb_show_half),
                 xytext=(face_x, dby - cb_show_half),
                 arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM, mutation_scale=5))
    ax2.text(face_x + 20, dby, 'Ø52.0', ha='left', fontsize=5.5, color=C_DIM)

    ax2.annotate('DISC t=0.10mm\n(SS-302)', xy=(face_x - sb(PH_CB_DEP) + disc_shown_t/2, dby + disc_half),
                 xytext=(face_x - sb(PH_CB_DEP) - 100, dby + disc_half + 48),
                 fontsize=5.5, color='black',
                 arrowprops=dict(arrowstyle='->', color='black', lw=0.7))

    ax2.annotate('Ø2.17 ±0.025\nPINHOLE', xy=(face_x - sb(PH_CB_DEP) + disc_shown_t/2, dby),
                 xytext=(face_x + 60, dby + 60),
                 fontsize=5.5, color='black',
                 arrowprops=dict(arrowstyle='->', color='black', lw=0.7))

    ax2.text(face_x - sb(PH_CB_DEP)/2, dby - cb_show_half - 32,
             '√ Ra 0.8', ha='center', fontsize=5.5, color='black')

    ax2.text(dbx, dby - sb(PH_CB_D/2 + 10) - 48,
             'DETAIL B — DISC SEAT (2:1)', ha='center', fontsize=6.5,
             fontweight='bold', color=C_RED)

    # ──────────────────────────────────────────────────────────────────────────
    # DETAIL C: Light trap rebate cross-section  (10:1 scale)
    # ──────────────────────────────────────────────────────────────────────────
    SC10 = 40
    def sc(mm): return mm * SC10

    dcx, dcy = 1120, 1200

    ax2.text(dcx, dcy + 340, 'DETAIL C — LIGHT TRAP', ha='center',
             fontsize=8, fontweight='bold')
    ax2.text(dcx, dcy + 316, '10:1 SCALE  —  Items 2 & 3', ha='center',
             fontsize=6, color='#555')

    frame_face_x = dcx - 120
    step_depth    = sc(TRAP_DEP)
    step_width    = sc(TRAP_W)

    ax2.add_patch(mpatches.Rectangle((frame_face_x - 48, dcy - 140), 48, 280,
                  fc=C_STEEL, ec=C_OUT, lw=LW_MED, zorder=3))
    for i in range(10):
        ax2.plot([frame_face_x - 48, frame_face_x], [dcy - 140 + i*28, dcy - 140 + i*28 + 48],
                 color='#888', lw=0.4)

    ax2.text(frame_face_x - 24, dcy - 140 - 24, 'ITEM 1\n(FRAME)', ha='center', fontsize=5)

    plate_x = frame_face_x + sc(0.5)
    plate_body_right = plate_x + 200

    ax2.add_patch(mpatches.Rectangle((plate_x, dcy + step_width), 200, 100,
                  fc=C_ALUM, ec=C_OUT, lw=LW_MED, zorder=4))
    for i in range(8):
        y0 = dcy + step_width + i*12
        ax2.plot([plate_x, plate_x+200], [y0, y0+12], color='#AAAAAA', lw=0.4)

    ax2.add_patch(mpatches.Rectangle((plate_x + step_depth, dcy - 100), 200 - step_depth, 100,
                  fc=C_ALUM, ec=C_OUT, lw=LW_MED, zorder=4))

    step_pts_x = [plate_x, plate_x, plate_x + step_depth, plate_x + step_depth]
    step_pts_y = [dcy + step_width, dcy, dcy, dcy - 100]
    ax2.plot(step_pts_x[:3], step_pts_y[:3], color=C_OUT, lw=LW_THICK, zorder=5)

    ax2.add_patch(mpatches.Rectangle((plate_x, dcy - 100), step_depth, step_width + 100,
                  fc='#F5F5F5', ec='none', lw=0, zorder=3))

    ax2.add_patch(mpatches.Circle((frame_face_x - sc(SEAL_W/2), dcy + step_width + 32),
                  sc(1.5), fc=C_GASKT, ec='none', zorder=6))
    ax2.text(frame_face_x - 80, dcy + step_width + 100, 'NEOPRENE\nSEAL Ø4\n(ITEM 9)',
             ha='center', fontsize=5, color=C_GASKT)

    ax2.annotate('', xy=(plate_x + step_depth/2, dcy - 40),
                 xytext=(frame_face_x, dcy - 40),
                 arrowprops=dict(arrowstyle='->', color='#CC0000', lw=1.0))
    ax2.text(plate_x + step_depth + 8, dcy - 40, 'NO LIGHT\nPATH', ha='left',
             fontsize=4.8, color='#CC0000')

    draw_dim_h(ax2, plate_x, plate_x + step_depth, dcy - 120, '5.0', above=False,
               fs=5.5, offset=6)
    draw_dim_v(ax2, plate_x + step_depth + 32, dcy, dcy + step_width, '5.0',
               right=True, fs=5.5, offset=6)

    ax2.text(dcx, dcy - 152, 'DETAIL C — LIGHT TRAP (10:1)', ha='center', fontsize=6.5,
             fontweight='bold', color=C_RED)

    # ──────────────────────────────────────────────────────────────────────────
    # DETAIL D: Lens Tube in Bore (section, 1:2 scale)
    # ──────────────────────────────────────────────────────────────────────────
    SC2 = 2
    def sd(mm): return mm * SC2

    ddx, ddy = 700, 620

    ax2.text(ddx, ddy + 420, 'DETAIL D — LENS FOCUSER  (1:2)', ha='center',
             fontsize=8, fontweight='bold')

    pl_left_d = ddx - sd(PL_THICK/2)
    pl_right_d = ddx + sd(PL_THICK/2)
    bore_half_d = sd(LB_D/2)
    tube_od_half = sd(LT_OD/2)
    tube_id_half = sd(LT_ID/2)
    plate_half_d = sd(PL_OD/2 * 0.15)

    for sign in [-1, 1]:
        ax2.add_patch(mpatches.Rectangle(
            (pl_left_d, ddy + sign*bore_half_d),
            sd(PL_THICK), sign * plate_half_d,
            fc=C_ALUM, ec=C_OUT, lw=LW_MED, zorder=3))
        for i in range(12):
            y0 = ddy + sign*bore_half_d + sign*i*sd(5)
            if 0 < sign*(y0 - (ddy + sign*bore_half_d)) < plate_half_d:
                ax2.plot([pl_left_d, pl_right_d], [y0, y0 + sd(3)*sign], color='#AAAAAA', lw=0.4)

    brk_amp = 8
    brk_w = sd(PL_THICK)
    for sign in [-1, 1]:
        brk_y = ddy + sign * (bore_half_d + plate_half_d)
        xs = np.array([pl_left_d - 4, pl_left_d + brk_w*0.25,
                       pl_left_d + brk_w*0.5, pl_left_d + brk_w*0.75,
                       pl_right_d + 4])
        ys = np.array([brk_y, brk_y + brk_amp, brk_y - brk_amp,
                       brk_y + brk_amp, brk_y])
        ax2.plot(xs, ys, color=C_OUT, lw=LW_MED, zorder=10)
        ax2.plot([pl_left_d, pl_left_d], [brk_y - brk_amp - 2, brk_y + brk_amp + 2],
                 color='white', lw=3, zorder=9)
        ax2.plot([pl_right_d, pl_right_d], [brk_y - brk_amp - 2, brk_y + brk_amp + 2],
                 color='white', lw=3, zorder=9)

    ax2.plot([pl_left_d, pl_right_d], [ddy + bore_half_d, ddy + bore_half_d], color=C_OUT, lw=LW_THICK)
    ax2.plot([pl_left_d, pl_right_d], [ddy - bore_half_d, ddy - bore_half_d], color=C_OUT, lw=LW_THICK)

    tube_extend_l = sd(80)
    tube_extend_r = sd(60)
    ax2.add_patch(mpatches.Rectangle(
        (pl_left_d - tube_extend_l, ddy + bore_half_d),
        tube_extend_l + sd(PL_THICK) + tube_extend_r, sd(LT_OD - LB_D)/2,
        fc='#BBBBBB', ec=C_OUT, lw=LW_MED, zorder=4))
    ax2.add_patch(mpatches.Rectangle(
        (pl_left_d - tube_extend_l, ddy - bore_half_d - sd(LT_OD - LB_D)/2),
        tube_extend_l + sd(PL_THICK) + tube_extend_r, sd(LT_OD - LB_D)/2,
        fc='#BBBBBB', ec=C_OUT, lw=LW_MED, zorder=4))

    ax2.add_patch(mpatches.Rectangle(
        (pl_left_d - tube_extend_l, ddy - tube_id_half),
        tube_extend_l + sd(PL_THICK) + tube_extend_r, sd(LT_ID),
        fc='white', ec='none', lw=0, zorder=5))
    ax2.plot([pl_left_d - tube_extend_l, pl_right_d + tube_extend_r], [ddy + tube_id_half]*2,
             color=C_OUT, lw=LW_THICK, zorder=6)
    ax2.plot([pl_left_d - tube_extend_l, pl_right_d + tube_extend_r], [ddy - tube_id_half]*2,
             color=C_OUT, lw=LW_THICK, zorder=6)

    ss_x = pl_left_d + sd(PL_THICK/2)
    ss_y = ddy + bore_half_d + sd((LT_OD - LB_D)/4)
    ax2.add_patch(mpatches.Circle((ss_x, ss_y + sd(3)), sd(4), fc='#CCCCCC', ec=C_OUT, lw=LW_MED, zorder=7))
    ax2.text(ss_x + sd(10), ss_y + sd(7), 'M8 SET SCREW\n(3× AT 120°)', fontsize=5, color='black')

    ax2.annotate('Ø175 H7/g6\nSLIDING FIT', xy=(pl_right_d, ddy - bore_half_d),
                 xytext=(pl_right_d + 48, ddy - bore_half_d - 60),
                 fontsize=5.5, color='black',
                 arrowprops=dict(arrowstyle='->', color='black', lw=0.7))

    ax2.plot([pl_left_d - tube_extend_l - 40, pl_right_d + tube_extend_r + 80],
             [ddy, ddy], color=C_CL, lw=LW_THIN, linestyle=(0, (6, 2, 1, 2)))

    ax2.annotate('', xy=(pl_left_d - tube_extend_l, ddy + tube_od_half + 32),
                 xytext=(pl_left_d - tube_extend_l + sd(80), ddy + tube_od_half + 32),
                 arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM, mutation_scale=5))
    ax2.text(pl_left_d - tube_extend_l + sd(40), ddy + tube_od_half + 48,
             '±40mm FOCUS\nTRAVEL', ha='center', fontsize=5, color=C_DIM)

    draw_dim_v(ax2, pl_right_d + 40, ddy - tube_id_half, ddy + tube_id_half,
               'Ø165\nTUBE ID', right=True, fs=5.5, offset=6)

    ax2.annotate('', xy=(pl_right_d, ddy + tube_od_half),
                 xytext=(pl_right_d, ddy - tube_od_half),
                 arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM, mutation_scale=5))
    ax2.text(pl_right_d + 72, ddy, 'Ø174.5\nTUBE OD', ha='left', fontsize=5.5, color=C_DIM)

    draw_dim_h(ax2, pl_left_d, pl_right_d, ddy - tube_od_half - 48, '15\nmm', above=False,
               fs=5.5, offset=6)

    ax2.text(ddx - 120, ddy - tube_od_half - 96, 'Ø175 H7 BORE / Ø174.5 g6 TUBE', ha='center',
             fontsize=6.5, fontweight='bold', color=C_RED)

    # ── Sheet 2 notes ─────────────────────────────────────────────────────────
    notes2 = [
        'OPERATIONAL NOTES:',
        'FOCUS ADJUSTMENT: SLIDE LENS TUBE (ITEM 6) WITHIN PLATE BORE (ITEM 3/ITEM 5) AND LOCK WITH 3×M8 SET SCREWS.',
        'AT 3.4m SUBJECT DISTANCE: POSITION LENS TUBE SO LENS PRINCIPAL PLANE IS 1400mm FROM PINHOLE WALL INTERIOR FACE.',
        'AT 5.0m SUBJECT DISTANCE: RETRACT TUBE TO 1604mm. MARK TUBE AT BOTH POSITIONS WITH SCRIBED LINES.',
        'INTERCHANGEABLE OPERATION: RELEASE 8×M12 BOLTS; WITHDRAW PLATE FROM DARK SIDE OF CAMERA; INSERT SECOND PLATE; RE-TORQUE BOLTS.',
        'SHUTTER (LENS PLATE ONLY): SLIDE BLACK Al PANEL (175mm × 55mm × 3mm) IN GUIDE RAILS — SPRING-LOADED TO CLOSED.',
        'PROCUREMENT: LENOX LASER (lenoxlaser.com) FOR PINHOLE DISCS — SPECIFY: SS-302 Ø50mm, APERTURE Ø2.17mm ±0.025mm.',
    ]
    draw_notes(ax2, notes2, 40, 280, spacing=20, fs=7, width=1300)

    plt.tight_layout(pad=0)
    out2 = f'{DIAGRAMS_DIR}/plate-drawing-sheet2.png'
    fig.savefig(out2, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  → plate-drawing-sheet2.png  Done.')


if __name__ == "__main__":
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    print("Generating TBS-001 Optical Plate System diagrams...")
    draw_sheet1()
    draw_sheet2()
    print("Done.")
