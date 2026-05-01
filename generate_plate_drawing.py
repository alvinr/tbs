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

# ── Real dimensions (mm) ─────────────────────────────────────────────────────
PL_OD      = 600      # plate outer dimension (square)
PL_THICK   = 15       # aluminium plate thickness
FR_THICK   = 6        # wall frame steel thickness
FR_APT_D   = 350      # wall frame circular aperture diameter
BOLT_BC    = 540      # bolt circle diameter
BOLT_D     = 13       # bolt hole clearance diameter
BOLT_N     = 8        # bolt count
DWL_D      = 8        # dowel pin diameter
DWL_OFF    = 200      # dowel pin offset ± from centre
SEAL_D     = 420      # neoprene groove centreline diameter
SEAL_W     = 3        # seal groove width
SEAL_DEP   = 3        # seal groove depth
TRAP_SQ    = 490      # light-trap rebate centred square
TRAP_W     = 5        # rebate width
TRAP_DEP   = 5        # rebate depth
# Pinhole plate
PH_BORE    = 90       # light-admission taper bore (exterior face)
PH_CB_D    = 52       # pinhole disc counterbore diameter (interior face)
PH_CB_DEP  = 3        # counterbore depth
PH_DISC_D  = 50       # pinhole disc OD (Lenox Laser supply)
PH_DISC_T  = 0.1      # pinhole disc thickness (SS)
PH_APT     = 2.17     # pinhole aperture
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
C_CL    = '#0055AA'   # centre-line blue
C_DIM   = '#333333'
C_HID   = '#888888'
C_STEEL = '#B0B0B0'
C_ALUM  = '#D8D8D8'
C_GASKT = '#404040'
C_RED   = '#CC0000'   # section-cut arrows

def draw_dim_h(ax, x1, x2, y, text, above=True, fontsize=6, scale=1.0):
    """Horizontal dimension line between x1 and x2 at height y."""
    off = 3 * scale
    dy = off if above else -off
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM,
                                mutation_scale=5*scale))
    mx = (x1 + x2) / 2
    va = 'bottom' if above else 'top'
    ax.text(mx, y + (1.5*scale if above else -1.5*scale), text,
            ha='center', va=va, fontsize=fontsize, color=C_DIM)
    # extension lines
    ax.plot([x1, x1], [y - off*0.3, y + off*0.3], color=C_DIM, lw=0.5)
    ax.plot([x2, x2], [y - off*0.3, y + off*0.3], color=C_DIM, lw=0.5)

def draw_dim_v(ax, x, y1, y2, text, right=True, fontsize=6, scale=1.0):
    """Vertical dimension line."""
    off = 3 * scale
    dx = off if right else -off
    ax.annotate('', xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM,
                                mutation_scale=5*scale))
    my = (y1 + y2) / 2
    ha = 'left' if right else 'right'
    ax.text(x + (1.5*scale if right else -1.5*scale), my, text,
            ha=ha, va='center', fontsize=fontsize, color=C_DIM,
            rotation=90 if not right else 0)
    ax.plot([x - off*0.3, x + off*0.3], [y1, y1], color=C_DIM, lw=0.5)
    ax.plot([x - off*0.3, x + off*0.3], [y2, y2], color=C_DIM, lw=0.5)

def draw_cl(ax, cx, cy, r, horiz=True, vert=True, scale=1.0):
    """Draw centrelines through (cx,cy)."""
    ext = max(r * 1.25, 4 * scale)
    ls = (0, (6, 2, 1, 2))
    if horiz:
        ax.plot([cx - ext, cx + ext], [cy, cy], color=C_CL, lw=LW_THIN,
                linestyle=ls)
    if vert:
        ax.plot([cx, cx], [cy - ext, cy + ext], color=C_CL, lw=LW_THIN,
                linestyle=ls)

def draw_circle(ax, cx, cy, r, lw=LW_THICK, color=C_OUT, ls='-', fill=False, fc='none'):
    c = mpatches.Circle((cx, cy), r, lw=lw, edgecolor=color, facecolor=fc if fill else 'none',
                         linestyle=ls, zorder=4)
    ax.add_patch(c)

def draw_rect(ax, x, y, w, h, lw=LW_THICK, color=C_OUT, fc='white', zorder=3):
    r = mpatches.Rectangle((x, y), w, h, lw=lw, edgecolor=color,
                             facecolor=fc, zorder=zorder)
    ax.add_patch(r)

def leader(ax, xfrom, yfrom, xto, yto, text, fontsize=6, color=C_DIM):
    ax.annotate(text, xy=(xto, yto), xytext=(xfrom, yfrom),
                fontsize=fontsize, color=color,
                arrowprops=dict(arrowstyle='->', color=color, lw=0.7))

def bolt_holes(ax, cx, cy, bc_r, n, d_r, color=C_OUT, lw=LW_MED):
    for i in range(n):
        angle = np.radians(22.5 + i * 360/n)
        bx = cx + bc_r * np.cos(angle)
        by = cy + bc_r * np.sin(angle)
        draw_circle(ax, bx, by, d_r, lw=lw, color=color)

def hatch_rect(ax, x, y, w, h, spacing=3, angle=45, color='#AAAAAA', lw=0.5):
    """Draw diagonal hatching inside a rectangle."""
    import matplotlib.patheffects as pe
    rect = mpatches.Rectangle((x, y), w, h, color='none')
    ax.add_patch(rect)
    ax.set_clip_path(rect)
    angle_r = np.radians(angle)
    diag = np.sqrt(w**2 + h**2)
    n = int(diag / spacing) + 2
    cx = x + w/2
    cy = y + h/2
    for i in range(-n, n+1):
        offset = i * spacing
        dx = diag * np.cos(angle_r)
        dy = diag * np.sin(angle_r)
        px0 = cx + offset * np.cos(angle_r + np.pi/2) - dx/2
        py0 = cy + offset * np.sin(angle_r + np.pi/2) - dy/2
        px1 = px0 + dx
        py1 = py0 + dy
        ax.plot([px0, px1], [py0, py1], color=color, lw=lw,
                clip_path=rect, clip_on=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — FRONT VIEWS
# ═══════════════════════════════════════════════════════════════════════════════

fig1, ax1 = plt.subplots(figsize=(28, 20))
fig1.patch.set_facecolor('white')
ax1.set_facecolor('white')
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_xlim(0, 700)
ax1.set_ylim(0, 500)

SC = 1/8   # 1:8 scale — 600mm plate → 75mm on drawing

def s(mm): return mm * SC

# ── Border and title block ────────────────────────────────────────────────────
draw_rect(ax1, 5, 5, 690, 490, lw=1.5, color='black', fc='white')
draw_rect(ax1, 5, 5, 690, 70, lw=1.0, color='black', fc='#F0F0F0')  # parts list
draw_rect(ax1, 480, 5, 215, 70, lw=1.0, color='black', fc='#F5F5F5')  # title block

# Title block content
ax1.text(587, 68, 'GIANT PINHOLE CAMERA — OPTION B', ha='center', fontsize=9,
         fontweight='bold', color='black')
ax1.text(587, 61, 'INTERCHANGEABLE OPTICAL PLATE SYSTEM', ha='center',
         fontsize=7.5, color='black')
ax1.text(587, 53, 'SHEET 1 OF 2 — PART FRONT VIEWS', ha='center',
         fontsize=7, color='black')
ax1.text(490, 46, 'SCALE:', fontsize=6, color='black')
ax1.text(520, 46, '1:8 (AS NOTED)', fontsize=6, color='black', fontweight='bold')
ax1.text(490, 38, 'MATERIAL:', fontsize=6, color='black')
ax1.text(540, 38, 'Al 6061-T6 (plates) / S275 steel (frame)', fontsize=6, color='black')
ax1.text(490, 30, 'UNITS:', fontsize=6, color='black')
ax1.text(515, 30, 'ALL DIMENSIONS IN mm', fontsize=6, fontweight='bold', color='black')
ax1.text(490, 22, 'TOLERANCE:', fontsize=6, color='black')
ax1.text(530, 22, '±0.5 UNLESS NOTED', fontsize=6, color='black')
ax1.text(490, 14, 'FINISH:', fontsize=6, color='black')
ax1.text(515, 14, 'ALL MACHINED FACES Ra 1.6; BORE H7 Ra 0.8', fontsize=5.5, color='black')

# Parts list
ax1.text(10, 68, 'ITEM', fontsize=6, fontweight='bold', color='black')
ax1.text(30, 68, 'DESCRIPTION', fontsize=6, fontweight='bold', color='black')
ax1.text(200, 68, 'MATERIAL', fontsize=6, fontweight='bold', color='black')
ax1.text(300, 68, 'QTY', fontsize=6, fontweight='bold', color='black')
ax1.text(320, 68, 'NOTES', fontsize=6, fontweight='bold', color='black')

parts = [
    ('1', 'WALL FRAME', 'S275 STEEL PLATE 6mm', '1',
     'Weld to container wall; machine face after welding'),
    ('2', 'PINHOLE PLATE', 'Al 6061-T6, 15mm', '1',
     'Black anodise all faces; interior faces Matt Black'),
    ('3', 'PINHOLE DISC', 'SS-302 0.10mm (Lenox Laser)', '1+',
     'Ø50 disc, Ø2.17 aperture ±0.025mm; order spares'),
    ('4', 'DISC RETAINING RING', 'Al 6061-T6', '1',
     'Ø52 bore × M52×0.75 thread; 3× M4 grub screws'),
    ('5', 'LENS PLATE', 'Al 6061-T6, 15mm', '1',
     'Black anodise; Ø175 bore H7; interior faces Matt Black'),
    ('6', 'LENS TUBE', 'Al 6061-T6', '1',
     'Ø174.5g6 × Ø165 bore × 100L; 3× M8 set screws at 120°'),
    ('7', 'LOCATING DOWEL PIN', 'SS-303 Ø8 m6 × 40L', '2',
     'Press fit to wall frame (H7 reamed holes)'),
    ('8', 'SOCKET HEAD BOLT', 'M12 × 40mm grade 8.8', '8',
     'With M12 flat washer each; torque to 65 Nm'),
    ('9', 'NEOPRENE CORD SEAL', 'Ø4mm neoprene, 70 Shore', '1',
     'Ø420mm loop in 3×3 groove on wall frame face'),
]
for i, (it, desc, mat, qty, note) in enumerate(parts):
    yp = 58 - i * 5.8
    bg = '#FFFFFF' if i % 2 == 0 else '#F8F8F8'
    draw_rect(ax1, 6, yp - 2, 468, 5.5, lw=0, fc=bg, zorder=1)
    ax1.text(10, yp + 0.5, it, fontsize=5.5, color='black', fontweight='bold')
    ax1.text(30, yp + 0.5, desc, fontsize=5.5, color='black')
    ax1.text(200, yp + 0.5, mat, fontsize=5, color='black')
    ax1.text(300, yp + 0.5, qty, fontsize=5.5, color='black')
    ax1.text(320, yp + 0.5, note, fontsize=5, color='#333333')
ax1.plot([6, 474], [65, 65], color='black', lw=0.5)

# ── View titles ───────────────────────────────────────────────────────────────
view_titles = [
    (95, 355, 'ITEM 1 — WALL FRAME (Steel)', '(Interior face shown)'),
    (268, 355, 'ITEM 2 — PINHOLE PLATE (Al)', '(Interior face shown)'),
    (441, 355, 'ITEM 3 — LENS PLATE (Al)', '(Interior face shown)'),
]
for tx, ty, t1, t2 in view_titles:
    ax1.text(tx, ty, t1, ha='center', fontsize=7.5, fontweight='bold', color='black')
    ax1.text(tx, ty - 7, t2, ha='center', fontsize=6, color='#555555', style='italic')

# ══════════════════════════════════════════════════════════
# ITEM 1: WALL FRAME  (centre = 95, 290)
# ══════════════════════════════════════════════════════════
cx1, cy1 = 95, 290

# Outer plate outline
hw = s(PL_OD/2)
draw_rect(ax1, cx1 - hw, cy1 - hw, s(PL_OD), s(PL_OD),
          lw=LW_THICK, color=C_OUT, fc=C_STEEL)

# Central aperture (clear hole)
draw_circle(ax1, cx1, cy1, s(FR_APT_D/2), lw=LW_THICK, color=C_OUT, fc='white', fill=True)

# Seal groove (on interior face — shown as dashed circle)
draw_circle(ax1, cx1, cy1, s(SEAL_D/2), lw=LW_THIN, color=C_HID, ls='--')

# Bolt circle reference circle
draw_circle(ax1, cx1, cy1, s(BOLT_BC/2), lw=0.4, color=C_HID, ls=':')

# Bolt holes
bolt_holes(ax1, cx1, cy1, s(BOLT_BC/2), BOLT_N, s(BOLT_D/2), color=C_OUT, lw=LW_MED)

# Dowel holes
for sign in [-1, 1]:
    dx = cx1 + sign * s(DWL_OFF)
    draw_circle(ax1, dx, cy1, s(DWL_D/2), lw=LW_MED, color=C_OUT)
    # Cross mark
    ax1.plot([dx - s(4), dx + s(4)], [cy1, cy1], color=C_CL, lw=0.5,
             linestyle=(0, (4, 2)))
    ax1.plot([dx, dx], [cy1 - s(4), cy1 + s(4)], color=C_CL, lw=0.5,
             linestyle=(0, (4, 2)))

# Centre lines
draw_cl(ax1, cx1, cy1, hw * 1.1, scale=1.0)

# Section cut line A-A (horizontal through centre)
ax1.plot([cx1 - hw - 8, cx1 + hw + 8], [cy1, cy1],
         color=C_RED, lw=LW_CUT, linestyle=(0, (8, 3)))
for sign in [-1, 1]:
    ax1.annotate('', xy=(cx1 + sign*(hw + 8), cy1 + sign*5),
                 xytext=(cx1 + sign*(hw + 8), cy1),
                 arrowprops=dict(arrowstyle='->', color=C_RED, lw=1.5))
ax1.text(cx1 - hw - 12, cy1 + 3, 'A', ha='center', fontsize=8,
         fontweight='bold', color=C_RED)
ax1.text(cx1 + hw + 12, cy1 + 3, 'A', ha='center', fontsize=8,
         fontweight='bold', color=C_RED)

# ── Dimensions for Wall Frame ─────────────────────────────────────────────────
dim_y_top = cy1 + hw + 14
dim_x_right = cx1 + hw + 18

# Overall width
draw_dim_h(ax1, cx1 - hw, cx1 + hw, dim_y_top, '600', above=True, fontsize=6)
# Overall height
draw_dim_v(ax1, dim_x_right, cy1 - hw, cy1 + hw, '600', right=True, fontsize=6)
# Aperture diameter
leader(ax1, cx1 + 12, cy1 + 10, cx1 + s(FR_APT_D/2)*0.65, cy1 + s(FR_APT_D/2)*0.65,
       'Ø350', fontsize=5.5)
# Bolt circle
leader(ax1, cx1 + 15, cy1 - 18, cx1 + s(BOLT_BC/2)*0.6, cy1 - s(BOLT_BC/2)*0.6,
       'Ø540 B.C.\n8×Ø13', fontsize=5)
# Seal groove
leader(ax1, cx1 - 18, cy1 + 22, cx1 - s(SEAL_D/2)*0.7, cy1 + s(SEAL_D/2)*0.7,
       'Ø420\nSEAL GRV\n3×3 DEEP', fontsize=4.8)
# Dowel hole callout
leader(ax1, cx1 - s(DWL_OFF) - 6, cy1 - 12,
       cx1 - s(DWL_OFF), cy1 - s(DWL_D/2),
       '2×Ø8 H7\nDOWEL\n(±200)', fontsize=4.8)

ax1.text(cx1, cy1 - hw - 10, '1', ha='center', va='center', fontsize=10,
         fontweight='bold', color='white',
         bbox=dict(boxstyle='circle,pad=0.3', fc='black', ec='black'))

# ══════════════════════════════════════════════════════════
# ITEM 2: PINHOLE PLATE  (centre = 268, 290)
# ══════════════════════════════════════════════════════════
cx2, cy2 = 268, 290

draw_rect(ax1, cx2 - hw, cy2 - hw, s(PL_OD), s(PL_OD),
          lw=LW_THICK, color=C_OUT, fc=C_ALUM)

# Light trap rebate outline (shown as hidden square — interior step)
trap_h = s(TRAP_SQ/2)
for sign_x, sign_y in [(-1,-1),(1,-1),(1,1),(-1,1),(-1,-1)]:
    pass
# Draw as dashed square
trap_corners = [
    (cx2 - trap_h, cy2 - trap_h),
    (cx2 + trap_h, cy2 - trap_h),
    (cx2 + trap_h, cy2 + trap_h),
    (cx2 - trap_h, cy2 + trap_h),
    (cx2 - trap_h, cy2 - trap_h),
]
trap_xs = [p[0] for p in trap_corners]
trap_ys = [p[1] for p in trap_corners]
ax1.plot(trap_xs, trap_ys, color=C_HID, lw=LW_THIN, linestyle='--', zorder=5)

# Light-admission bore (visible circle — exterior face visible through plate)
draw_circle(ax1, cx2, cy2, s(PH_BORE/2), lw=LW_THICK, color=C_OUT, fc='white', fill=True)

# Counterbore (interior feature — shown dashed)
draw_circle(ax1, cx2, cy2, s(PH_CB_D/2), lw=LW_THIN, color=C_HID, ls='--')

# Pinhole aperture (tiny — shown as dot + leader)
draw_circle(ax1, cx2, cy2, 0.4, lw=1.5, color=C_OUT, fc=C_OUT, fill=True)

# Bolt holes
bolt_holes(ax1, cx2, cy2, s(BOLT_BC/2), BOLT_N, s(BOLT_D/2), color=C_OUT, lw=LW_MED)

# Bolt circle phantom
draw_circle(ax1, cx2, cy2, s(BOLT_BC/2), lw=0.4, color=C_HID, ls=':')

# Dowel holes
for sign in [-1, 1]:
    dx = cx2 + sign * s(DWL_OFF)
    draw_circle(ax1, dx, cy2, s(DWL_D/2), lw=LW_MED, color=C_OUT)

draw_cl(ax1, cx2, cy2, hw * 1.1)

# ── Dimensions for Pinhole Plate ──────────────────────────────────────────────
dim_y_top2 = cy2 + hw + 14

draw_dim_h(ax1, cx2 - hw, cx2 + hw, dim_y_top2, '600', above=True, fontsize=6)
draw_dim_h(ax1, cx2 - trap_h, cx2 + trap_h, dim_y_top2 - 6,
           '490 (LIGHT TRAP)', above=True, fontsize=5)

# Bore callout
leader(ax1, cx2 + 14, cy2 + 12, cx2 + s(PH_BORE/2)*0.6, cy2 + s(PH_BORE/2)*0.6,
       'Ø90\nBORE THRU', fontsize=5.5)
leader(ax1, cx2 + 16, cy2 - 10, cx2 + s(PH_CB_D/2)*0.6, cy2 - s(PH_CB_D/2)*0.6,
       'Ø52×3\nC\'BORE\n(INT FACE)', fontsize=4.8)
leader(ax1, cx2 - 18, cy2 + 5, cx2, cy2,
       'Ø2.17\nPINHOLE\n(DISC)', fontsize=5.0)
leader(ax1, cx2 - 22, cy2 - 20, cx2 - trap_h, cy2 - trap_h + 2,
       '5×5 REBATE\n(LIGHT TRAP)', fontsize=4.8)

ax1.text(cx2, cy2 - hw - 10, '2', ha='center', va='center', fontsize=10,
         fontweight='bold', color='white',
         bbox=dict(boxstyle='circle,pad=0.3', fc='black', ec='black'))

# ══════════════════════════════════════════════════════════
# ITEM 3: LENS PLATE  (centre = 441, 290)
# ══════════════════════════════════════════════════════════
cx3, cy3 = 441, 290

draw_rect(ax3 := ax1, cx3 - hw, cy3 - hw, s(PL_OD), s(PL_OD),
          lw=LW_THICK, color=C_OUT, fc=C_ALUM)

# Light trap rebate (dashed square)
ax3.plot(
    [cx3 + sign_x*trap_h for sign_x in [-1, 1, 1, -1, -1]],
    [cy3 + sign_y*trap_h for sign_y in [-1, -1, 1, 1, -1]],
    color=C_HID, lw=LW_THIN, linestyle='--', zorder=5)

# Lens bore (large central hole)
draw_circle(ax3, cx3, cy3, s(LB_D/2), lw=LW_THICK, color=C_OUT, fc='white', fill=True)

# Lens tube shown within bore as dashed (tube slides inside)
draw_circle(ax3, cx3, cy3, s(LT_OD/2), lw=LW_THIN, color=C_HID, ls='--')

# Lens tube inner bore
draw_circle(ax3, cx3, cy3, s(LT_ID/2), lw=LW_THIN, color=C_HID, ls=':')

# Set screw positions (3× at 120°)
for angle_deg in [90, 210, 330]:
    angle_r = np.radians(angle_deg)
    sx = cx3 + s(LB_D/2 + 5) * np.cos(angle_r)
    sy = cy3 + s(LB_D/2 + 5) * np.sin(angle_r)
    draw_circle(ax3, sx, sy, 1.2, lw=LW_MED, color=C_OUT)

# Shutter rail mounting holes (4× on horizontal, for sliding shutter option)
for xo in [-s(100), -s(50), s(50), s(100)]:
    ax3.plot([cx3 + xo], [cy3 + hw - s(30)], 'x', color='#888', ms=3, lw=0.7)

# Bolt holes
bolt_holes(ax3, cx3, cy3, s(BOLT_BC/2), BOLT_N, s(BOLT_D/2), color=C_OUT, lw=LW_MED)
draw_circle(ax3, cx3, cy3, s(BOLT_BC/2), lw=0.4, color=C_HID, ls=':')

# Dowel holes
for sign in [-1, 1]:
    dx = cx3 + sign * s(DWL_OFF)
    draw_circle(ax3, dx, cy3, s(DWL_D/2), lw=LW_MED, color=C_OUT)

draw_cl(ax3, cx3, cy3, hw * 1.1)

# ── Dimensions for Lens Plate ─────────────────────────────────────────────────
dim_y_top3 = cy3 + hw + 14
draw_dim_h(ax3, cx3 - hw, cx3 + hw, dim_y_top3, '600', above=True, fontsize=6)

leader(ax3, cx3 + 16, cy3 + 16, cx3 + s(LB_D/2)*0.65, cy3 + s(LB_D/2)*0.65,
       'Ø175 H7\nBORE THRU', fontsize=5.5)
leader(ax3, cx3 + 20, cy3 - 12, cx3 + s(LT_OD/2)*0.65, cy3 - s(LT_OD/2)*0.65,
       'Ø174.5 g6\nLENS TUBE\n(ITEM 6)', fontsize=4.8)
leader(ax3, cx3 - 20, cy3 + 16,
       cx3 + s(LB_D/2 + 5)*np.cos(np.radians(150)),
       cy3 + s(LB_D/2 + 5)*np.sin(np.radians(150)),
       '3×M8\nSET SCREWS\n@ 120°', fontsize=4.8)
leader(ax3, cx3 - 15, cy3 + hw - s(30) + 8, cx3 - s(60), cy3 + hw - s(30),
       'SHUTTER\nRAIL HOLES\n4×Ø6.5', fontsize=4.8)

ax3.text(cx3, cy3 - hw - 10, '3', ha='center', va='center', fontsize=10,
         fontweight='bold', color='white',
         bbox=dict(boxstyle='circle,pad=0.3', fc='black', ec='black'))

# ── Section cut label on plate 3 ─────────────────────────────────────────────
ax3.text(cx3, cy3 + hw + 5, '  ', fontsize=1)  # spacer

# ── Notes block ──────────────────────────────────────────────────────────────
notes_x = 10
notes_y = 175
ax1.text(notes_x, notes_y, 'GENERAL NOTES:', fontsize=7, fontweight='bold', color='black')
notes = [
    '1. ALL DIMENSIONS IN MILLIMETRES. DO NOT SCALE DRAWING.',
    '2. ITEMS 2 AND 3: CRITICAL BORE Ø175 H7 AND DOWEL HOLES Ø8 H7 — MATCH REAM PAIRS.',
    '3. LIGHT TRAP REBATE: 5mm WIDE × 5mm DEEP SQUARE STEP ON MATING (INTERIOR) FACE OF ITEMS 2 & 3.',
    '4. ALL INTERIOR FACES OF ITEMS 1, 2, 3: MATT BLACK FINISH — ITEM 1: CHEMICAL BLACKEN; ITEMS 2&3: BLACK ANODISE.',
    '5. PINHOLE DISC (ITEM 3): PROCURE FROM LENOX LASER (lenoxlaser.com) Ø50mm SS-302, Ø2.17mm ±0.025mm APERTURE.',
    '6. ITEM 1 WELD TO CONTAINER WALL: FULL PERIMETER 6mm FILLET. MACHINE FACE FLAT Ra 1.6 AFTER WELDING.',
    '7. INTERCHANGEABILITY: ALL BOLT AND DOWEL PATTERNS IDENTICAL ON ITEMS 2 & 3 — SWAP IN DARK WITHOUT TOOLS.',
    '8. SHUTTER PROVISION: ITEMS 2 & 3 HAVE 4×Ø6.5 HOLES AT TOP FACE FOR SLIDING SHUTTER RAIL — SEE SHEET 2.',
]
for i, note in enumerate(notes):
    ax1.text(notes_x, notes_y - 7 - i*6, note, fontsize=5.2, color='#222222')

plt.tight_layout(pad=0)
plt.figtext(0.99, 0.005, "© 2026 Alvin Richards — GNU AGPLv3",
            ha="right", va="bottom", fontsize=6.0, color="#888888", style="italic")
out1 = '/Users/alvinrichards/dev/tbs/diagrams/plate-drawing-sheet1.png'
plt.savefig(out1, dpi=150, bbox_inches='tight', facecolor='white')
plt.savefig(str(out1).replace(".png", ".svg"), bbox_inches="tight", facecolor='white')
plt.close()
print(f'Saved sheet 1: {out1}')


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — SECTION A-A + DETAIL VIEWS
# ═══════════════════════════════════════════════════════════════════════════════

fig2, ax2 = plt.subplots(figsize=(28, 20))
fig2.patch.set_facecolor('white')
ax2.set_facecolor('white')
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_xlim(0, 700)
ax2.set_ylim(0, 500)

# Border
draw_rect(ax2, 5, 5, 690, 490, lw=1.5, color='black', fc='white')
draw_rect(ax2, 5, 5, 690, 55, lw=1.0, color='black', fc='#F0F0F0')
draw_rect(ax2, 480, 5, 215, 55, lw=1.0, color='black', fc='#F5F5F5')

ax2.text(587, 53, 'GIANT PINHOLE CAMERA — OPTION B', ha='center', fontsize=9,
         fontweight='bold')
ax2.text(587, 46, 'INTERCHANGEABLE OPTICAL PLATE SYSTEM', ha='center', fontsize=7.5)
ax2.text(587, 39, 'SHEET 2 OF 2 — SECTION A-A & DETAILS', ha='center', fontsize=7)
ax2.text(490, 31, 'SECTION SCALE: 1:4', fontsize=6)
ax2.text(490, 24, 'DETAIL B SCALE: 2:1', fontsize=6)
ax2.text(490, 17, 'DETAIL C SCALE: 2:1', fontsize=6)
ax2.text(490, 10, 'UNITS: mm', fontsize=6, fontweight='bold')

# ──────────────────────────────────────────────────────────────────────────────
# SECTION A-A  (1:4 scale)
# Shows: container wall / wall frame / plate (pinhole plate shown)
# Section cut through horizontal centreline
# ──────────────────────────────────────────────────────────────────────────────

SC4 = 1/4   # 1:4 scale
def ss(mm): return mm * SC4

# Section origin: centre of section at (220, 310)
scx, scy = 160, 310

ax2.text(scx, 465, 'SECTION A-A  (PINHOLE PLATE INSTALLED)', ha='center',
         fontsize=9, fontweight='bold', color='black')
ax2.text(scx, 458, '1:4 SCALE', ha='center', fontsize=7, color='#555')

# ── Container wall (steel, ~2mm thick) ────────────────────────────────────────
# Container wall runs top-to-bottom; section shows it as a thin vertical band
# Wall is to the LEFT of the assembly; inside camera is to the RIGHT
wall_left  = scx - ss(340)   # exterior face of container wall
wall_right = wall_left + ss(WALL_T)

# Draw wall (full height of section) - only partial visible
wall_h = ss(280)
ax2.add_patch(mpatches.Rectangle((wall_left, scy - wall_h/2), ss(WALL_T), wall_h,
              fc=C_STEEL, ec=C_OUT, lw=LW_MED, zorder=3))
# hatch steel
for i in range(int(wall_h/3)+1):
    y0 = scy - wall_h/2 + i*3
    ax2.plot([wall_left, wall_left + ss(WALL_T)], [y0, y0 + ss(WALL_T)],
             color='#888', lw=0.4, clip_on=True)

# Wall aperture (hole in wall) — the Ø360 cut-out
# In section: two horizontal gaps centred at scy
apt_half = ss(WALL_APT/2)
# Redraw wall ABOVE and BELOW the aperture
for region in [(-wall_h/2, -apt_half), (apt_half, wall_h/2)]:
    y_bot = scy + region[0]
    y_top = scy + region[1]
    ax2.add_patch(mpatches.Rectangle((wall_left, y_bot), ss(WALL_T), y_top - y_bot,
                  fc=C_STEEL, ec=C_OUT, lw=LW_MED, zorder=4))
    for i in range(int((y_top-y_bot)/3)+1):
        y0 = y_bot + i*3
        if y_bot <= y0 <= y_top:
            ax2.plot([wall_left, wall_left + ss(WALL_T)], [y0, y0 + ss(WALL_T)],
                     color='#888', lw=0.4)

ax2.text(wall_left - 3, scy-9, 'CONTAINER\nWALL\n(2mm steel)', ha='right',
         va='center', fontsize=5, color='#444')

# ── Wall Frame (steel 6mm plate, item 1) ──────────────────────────────────────
# Frame sits on interior face of wall (right side of wall)
fr_left  = wall_right            # butts against wall interior
fr_right = fr_left + ss(FR_THICK)
fr_half  = ss(PL_OD/2)           # frame is 600mm tall

# Full frame section (above and below aperture)
fr_apt_half = ss(FR_APT_D/2)
for region in [(-fr_half, -fr_apt_half), (fr_apt_half, fr_half)]:
    y_bot = scy + region[0]
    y_top = scy + region[1]
    ax2.add_patch(mpatches.Rectangle((fr_left, y_bot), ss(FR_THICK), y_top - y_bot,
                  fc=C_STEEL, ec=C_OUT, lw=LW_MED, zorder=5))
    # steel hatch
    for i in range(int((y_top-y_bot)/2.5)+1):
        y0 = y_bot + i*2.5
        if y_bot <= y0 <= y_top:
            ax2.plot([fr_left, fr_right], [y0, y0 + ss(FR_THICK)],
                     color='#666', lw=0.4)

# Seal groove (on interior face of frame) — small notch
seal_half = ss(SEAL_D/2)
for sign in [-1, 1]:
    groove_y = scy + sign * seal_half
    ax2.add_patch(mpatches.Rectangle(
        (fr_right - ss(SEAL_W), groove_y - sign*ss(SEAL_W/2)),
        ss(SEAL_W), ss(SEAL_DEP), fc='#AAAAAA', ec=C_OUT, lw=0.5, zorder=6))
    # neoprene in groove
    ax2.add_patch(mpatches.Circle(
        (fr_right - ss(SEAL_W/2), groove_y - sign*ss(SEAL_W/4) + sign*ss(1.5)),
        ss(1.5), fc=C_GASKT, ec='none', zorder=7))

ax2.text(fr_right + 6, scy + fr_half*0.6, 'ITEM 1\nWALL FRAME\n6mm STEEL', ha='left',
         va='center', fontsize=5.5, color='black')
# dim: frame thickness
draw_dim_h(ax2, fr_left, fr_right, scy + fr_half + 8, '6', above=True, fontsize=5.5, scale=0.6)

# ── Pinhole Plate (aluminium, item 2) ─────────────────────────────────────────
pl_left  = fr_right              # plate butts against frame face
pl_right = pl_left + ss(PL_THICK)
pl_half  = ss(PL_OD/2)

# Light trap rebate step (5mm × 5mm step at edge of plate)
trap_half = ss(TRAP_SQ/2)

# Draw plate in two halves (above and below centreline features)
# Above centre: show solid Al with taper bore visible as hidden lines
# Section is symmetric so draw top half features

# Main plate body (two regions: above taper bore and below)
bore_half_top = ss(PH_BORE/2)  # taper bore half
for region in [(-pl_half, -bore_half_top), (bore_half_top, pl_half)]:
    y_bot = scy + region[0]
    y_top = scy + region[1]
    # Light trap step reduces plate edge width by TRAP_W on left side
    # Simplified: full plate width to x_right, with notch
    left_x = pl_left + ss(TRAP_DEP) if abs(region[0]) > trap_half else pl_left
    ax2.add_patch(mpatches.Rectangle((pl_left, y_bot), ss(PL_THICK), y_top - y_bot,
                  fc=C_ALUM, ec=C_OUT, lw=LW_MED, zorder=5))
    # Al hatch
    for i in range(int((y_top - y_bot)/3)+1):
        y0 = y_bot + i*3
        if y_bot <= y0 <= y_top:
            ax2.plot([pl_left, pl_right], [y0, y0 + ss(3)], color='#AAAAAA', lw=0.4)

# Light trap rebate (step on left/mating face of plate)
# The 5mm step is visible at ±TRAP_SQ/2 = ±245mm
for sign in [-1, 1]:
    step_y = scy + sign * trap_half
    ax2.add_patch(mpatches.Rectangle(
        (pl_left, step_y - sign*ss(TRAP_W)),
        ss(TRAP_DEP), sign*ss(TRAP_W) * sign,
        fc='white', ec=C_OUT, lw=LW_MED, zorder=6))

# Counterbore on interior face (right face)
cb_half = ss(PH_CB_D/2)
ax2.add_patch(mpatches.Rectangle(
    (pl_right - ss(PH_CB_DEP), scy - cb_half),
    ss(PH_CB_DEP), ss(PH_CB_D),
    fc='white', ec=C_OUT, lw=LW_MED, zorder=6))

# Taper bore through plate (Ø90 exterior face → Ø52 interior face)
# Draw as tapered opening
ext_bore_half = ss(PH_BORE/2)
int_bore_half = ss(PH_CB_D/2)
for sign in [-1, 1]:
    ax2.plot([pl_left, pl_right - ss(PH_CB_DEP)],
             [scy + sign*ext_bore_half, scy + sign*int_bore_half],
             color=C_OUT, lw=LW_THICK, zorder=7)

# Pinhole disc in counterbore (very thin line)
ax2.add_patch(mpatches.Rectangle(
    (pl_right - ss(PH_CB_DEP), scy - ss(PH_DISC_D/2)),
    ss(PH_DISC_T * 30), ss(PH_DISC_D),   # exaggerated for visibility
    fc='#888', ec=C_OUT, lw=1.2, zorder=8))
ax2.text(pl_right + 3, scy - ss(PH_DISC_D/2) - 5,
         'ITEM 3\nPINHOLE DISC\n(Ø50 × 0.1mm SS)', fontsize=5, color='black',
         ha='left')

# Bolt (one shown schematically)
bolt_y = scy + ss(BOLT_BC/2 * 0.5)   # show at ~45° bolt position projected
bolt_x_fr  = fr_left
bolt_x_end = pl_right + ss(10)
ax2.add_patch(mpatches.Rectangle((bolt_x_fr, bolt_y - ss(6)), ss(PL_THICK + FR_THICK + 10),
              ss(12), fc='#CCCCCC', ec=C_OUT, lw=0.8, zorder=6, alpha=0.6))
ax2.plot([bolt_x_fr, bolt_x_end], [bolt_y, bolt_y], color='#444', lw=0.7, ls='--')
ax2.text(bolt_x_end + 2, bolt_y + 2, 'M12×40\nITEM 8', fontsize=4.5, color='black')

# Dimension: plate thickness
draw_dim_h(ax2, pl_left, pl_right, scy + pl_half + 8, '15', above=True, fontsize=5.5, scale=0.6)

# Dim: plate height
dim_rx = pl_right + 22
draw_dim_v(ax2, dim_rx, scy - pl_half, scy + pl_half, '600', right=True, fontsize=5.5, scale=0.6)

# Dim: frame aperture
ax2.annotate('', xy=(fr_left, scy + fr_apt_half),
             xytext=(fr_left, scy - fr_apt_half),
             arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM, mutation_scale=5))
ax2.text(fr_left - 16, scy+3, 'Ø350\nAPT', ha='center', fontsize=5, color=C_DIM)

# Dim: taper bore
ax2.annotate('', xy=(pl_left, scy + ext_bore_half),
             xytext=(pl_left, scy - ext_bore_half),
             arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM, mutation_scale=5))
ax2.text(pl_left - 10, scy, 'Ø90\nBORE', ha='center', fontsize=5, color=C_DIM)

# Dim counterbore
ax2.annotate('', xy=(pl_right, scy + cb_half),
             xytext=(pl_right, scy - cb_half),
             arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM, mutation_scale=5))
ax2.text(pl_right + 4, scy + 12, 'Ø52\n×3\nDEEP', ha='left', fontsize=5, color=C_DIM)

# Item 2 bubble
ax2.text(pl_left + ss(PL_THICK)*0.5, scy - pl_half + 6, '2', ha='center', va='center',
         fontsize=8, fontweight='bold', color='white',
         bbox=dict(boxstyle='circle,pad=0.25', fc='black', ec='black'))

# Optical axis arrow (pointing right = into camera)
ax2.annotate('', xy=(pl_right + 45, scy), xytext=(wall_left - 20, scy),
             arrowprops=dict(arrowstyle='->', color='#0055BB', lw=1.5))
ax2.text(pl_right + 50, scy + 3, 'OPTICAL\nAXIS', ha='left', fontsize=6,
         color='#0055BB', style='italic')

# Interior / Exterior labels
ax2.text(wall_left - 5, scy + pl_half*0.8, 'EXTERIOR\n(SCENE)', ha='right',
         fontsize=6.5, color='#333', style='italic')
ax2.text(pl_right + 10, scy + pl_half*0.8, 'INTERIOR\n(CAMERA)', ha='left',
         fontsize=6.5, color='#333', style='italic')

# Section title
ax2.text(scx - 75, scy - pl_half - 16, 'SECTION A-A', ha='center', fontsize=8,
         fontweight='bold', color=C_RED)
ax2.text(scx - 75, scy - pl_half - 24, '1:4 scale  —  Pinhole Plate (Item 2) installed', ha='center',
         fontsize=6, color='#555')

# ──────────────────────────────────────────────────────────────────────────────
# DETAIL B: Pinhole disc seat  (5:1 scale)
# ──────────────────────────────────────────────────────────────────────────────
SC5 = 2.0   # 2:1 detail (was 5:1; reduced so plate fits within canvas height)
def sb(mm): return mm * SC5

dbx, dby = 490, 360  # centre of detail view

ax2.text(dbx, 465, 'DETAIL B — PINHOLE DISC SEAT', ha='center',
         fontsize=8, fontweight='bold')
ax2.text(dbx, 458, '2:1 SCALE (dimensions in mm)', ha='center', fontsize=6, color='#555')

# Draw 5:1 cross-section of the counterbore region
# Show: plate interior face (right face), counterbore Ø52×3, disc, retaining ring groove
thick_show = ss(PH_CB_DEP + 2) * SC5/SC4  # just show near the interior face
face_x = dbx   # interior face (right face of plate in section A-A)

# Plate cross-section near the bore
SHOWN_W = 40  # mm of plate shown at 5:1
plate_show_left = face_x - sb(SHOWN_W)
plate_show_right = face_x

# Plate body (Al)
ax2.add_patch(mpatches.Rectangle(
    (plate_show_left, dby - sb(PH_CB_D/2 + 10)),
    sb(SHOWN_W), sb(PH_CB_D + 20),
    fc=C_ALUM, ec=C_OUT, lw=LW_MED, zorder=3))
# Al hatch
for i in range(30):
    y0 = dby - sb(PH_CB_D/2 + 10) + i * 5
    ax2.plot([plate_show_left, plate_show_right], [y0, y0 + 5],
             color='#AAAAAA', lw=0.4, clip_on=True)

# Counterbore recess (Ø52 × 3mm deep)
cb_show_half = sb(PH_CB_D/2)
ax2.add_patch(mpatches.Rectangle(
    (face_x - sb(PH_CB_DEP), dby - cb_show_half),
    sb(PH_CB_DEP), sb(PH_CB_D),
    fc='white', ec=C_OUT, lw=LW_MED, zorder=5))

# Pinhole disc (very thin — exaggerated for visibility)
disc_shown_t = sb(0.8)   # exaggerated for clarity
disc_half = sb(PH_DISC_D/2)
ax2.add_patch(mpatches.Rectangle(
    (face_x - sb(PH_CB_DEP), dby - disc_half),
    disc_shown_t, sb(PH_DISC_D),
    fc='#555', ec=C_OUT, lw=1.0, zorder=6))

# Pinhole aperture (tiny hole at centre of disc)
ph_r = sb(PH_APT/2)
ax2.add_patch(mpatches.Rectangle(
    (face_x - sb(PH_CB_DEP), dby - ph_r),
    disc_shown_t, sb(PH_APT),
    fc='white', ec='white', lw=0, zorder=7))

# Retaining ring groove (M52×0.75 thread shown schematically)
ring_half = sb(PH_CB_D/2 + 1.5)
ring_depth = sb(3)
for sign in [-1, 1]:
    ax2.add_patch(mpatches.Rectangle(
        (face_x - ring_depth, dby + sign*sb(PH_CB_D/2)),
        ring_depth, sign*sb(3),
        fc='#CCCCCC', ec=C_OUT, lw=0.8, zorder=6))

# Dimensions
draw_dim_h(ax2, face_x - sb(PH_CB_DEP), face_x, dby + cb_show_half + 6,
           '3.0 DEEP', above=True, fontsize=5.5, scale=0.5)
ax2.annotate('', xy=(face_x, dby + cb_show_half),
             xytext=(face_x, dby - cb_show_half),
             arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM, mutation_scale=5))
ax2.text(face_x + 5, dby, 'Ø52.0', ha='left', fontsize=5.5, color=C_DIM)

# Disc thickness leader
ax2.annotate('DISC t=0.10mm\n(SS-302)', xy=(face_x - sb(PH_CB_DEP) + disc_shown_t/2, dby + disc_half),
             xytext=(face_x - sb(PH_CB_DEP) - 25, dby + disc_half + 12),
             fontsize=5.5, color='black',
             arrowprops=dict(arrowstyle='->', color='black', lw=0.7))

# Pinhole leader
ax2.annotate('Ø2.17 ±0.025\nPINHOLE', xy=(face_x - sb(PH_CB_DEP) + disc_shown_t/2, dby),
             xytext=(face_x + 15, dby + 15),
             fontsize=5.5, color='black',
             arrowprops=dict(arrowstyle='->', color='black', lw=0.7))

# Ra callout on counterbore face
ax2.text(face_x - sb(PH_CB_DEP)/2, dby - cb_show_half - 8,
         '√ Ra 0.8', ha='center', fontsize=5.5, color='black')

ax2.text(dbx, dby - sb(PH_CB_D/2 + 10) - 12,
         'DETAIL B — DISC SEAT (2:1)', ha='center', fontsize=6.5,
         fontweight='bold', color=C_RED)

# ──────────────────────────────────────────────────────────────────────────────
# DETAIL C: Light trap rebate cross-section  (10:1 scale)
# ──────────────────────────────────────────────────────────────────────────────
SC10 = 10/1
def sc(mm): return mm * SC10

# dcx, dcy = 490, 190  # centre of detail C
dcx, dcy = 490, 130  # centre of detail C

ax2.text(dcx, 225, 'DETAIL C — LIGHT TRAP REBATE', ha='center',
         fontsize=8, fontweight='bold')
ax2.text(dcx, 258, '10:1 SCALE (dimensions in mm)  —  Applies to Items 2 & 3', ha='center',
         fontsize=6, color='#555')

# Show the step rebate in cross-section
# Wall frame face on the left (shown as line), plate on right, step at top
frame_face_x = dcx - 30
step_depth    = sc(TRAP_DEP)   # depth into plate = 5mm
step_width    = sc(TRAP_W)     # height of step = 5mm

# Wall frame (thin plate shown as filled region)
ax2.add_patch(mpatches.Rectangle((frame_face_x - 12, dcy - 35), 12, 70,
              fc=C_STEEL, ec=C_OUT, lw=LW_MED, zorder=3))
for i in range(10):
    ax2.plot([frame_face_x - 12, frame_face_x], [dcy - 35 + i*7, dcy - 35 + i*7 + 12],
             color='#888', lw=0.4)

ax2.text(frame_face_x - 6, dcy - 35 - 6, 'ITEM 1\n(FRAME)', ha='center', fontsize=5)

# The gap at the interface — neoprene seal area (above trap) and gap (below trap)
# Plate body (right side of interface)
plate_x = frame_face_x + sc(0.5)   # 0.5mm seal compression gap
plate_body_right = plate_x + 50

# Plate above the trap step (full contact zone)
ax2.add_patch(mpatches.Rectangle((plate_x, dcy + step_width), 50, 25,
              fc=C_ALUM, ec=C_OUT, lw=LW_MED, zorder=4))
for i in range(8):
    y0 = dcy + step_width + i*3
    ax2.plot([plate_x, plate_x+50], [y0, y0+3], color='#AAAAAA', lw=0.4)

# Plate below the trap step
ax2.add_patch(mpatches.Rectangle((plate_x + step_depth, dcy - 25), 50 - step_depth, 25,
              fc=C_ALUM, ec=C_OUT, lw=LW_MED, zorder=4))

# The step itself (rebate)
step_pts_x = [plate_x, plate_x, plate_x + step_depth, plate_x + step_depth]
step_pts_y = [dcy + step_width, dcy, dcy, dcy - 25]
ax2.plot(step_pts_x[:3], step_pts_y[:3], color=C_OUT, lw=LW_THICK, zorder=5)

# Light trap void (the recessed area — shown light grey)
ax2.add_patch(mpatches.Rectangle((plate_x, dcy - 25), step_depth, step_width + 25,
              fc='#F5F5F5', ec='none', lw=0, zorder=3))

# Neoprene cord seal in wall frame groove (shown as circle in the seal groove)
ax2.add_patch(mpatches.Circle((frame_face_x - sc(SEAL_W/2), dcy + step_width + 8),
              sc(1.5), fc=C_GASKT, ec='none', zorder=6))
ax2.text(frame_face_x - 20, dcy + step_width + 25, 'NEOPRENE\nSEAL Ø4\n(ITEM 9)',
         ha='center', fontsize=5, color=C_GASKT)

# Light path arrow (showing no light path through the labyrinth)
ax2.annotate('', xy=(plate_x + step_depth/2, dcy - 10),
             xytext=(frame_face_x, dcy - 10),
             arrowprops=dict(arrowstyle='->', color='#CC0000', lw=1.0))
ax2.text(plate_x + step_depth + 2, dcy - 10, 'NO LIGHT\nPATH', ha='left',
         fontsize=4.8, color='#CC0000')

# Dimensions
draw_dim_h(ax2, plate_x, plate_x + step_depth, dcy - 30, '5.0', above=False,
           fontsize=5.5, scale=0.5)
draw_dim_v(ax2, plate_x + step_depth + 8, dcy, dcy + step_width, '5.0',
           right=True, fontsize=5.5, scale=0.5)

ax2.text(dcx, dcy - 38, 'DETAIL C — LIGHT TRAP (10:1)', ha='center', fontsize=6.5,
         fontweight='bold', color=C_RED)

# ──────────────────────────────────────────────────────────────────────────────
# DETAIL D: Lens Tube in Bore (section, 1:2 scale)
# ──────────────────────────────────────────────────────────────────────────────
SC2 = 1/2
def sd(mm): return mm * SC2

ddx, ddy = 340, 200   # centre — moved right to avoid Section A-A overlap

ax2.text(ddx+5, ddy + 130, 'DETAIL D — LENS PLATE SECTION  (1:2)', ha='center',
         fontsize=8, fontweight='bold')
ax2.text(ddx, ddy + 123, 'Shows lens tube focuser detail', ha='center', fontsize=6, color='#555')

# Lens plate cross-section (showing the Ø175 H7 bore with lens tube)
pl_left_d = ddx - sd(PL_THICK/2)
pl_right_d = ddx + sd(PL_THICK/2)
bore_half_d = sd(LB_D/2)
tube_od_half = sd(LT_OD/2)
tube_id_half = sd(LT_ID/2)
plate_half_d = sd(PL_OD/2 * 0.4)   # show partial plate height

# Plate body
for sign in [-1, 1]:
    y_start = scy + sign * bore_half_d if False else ddy + sign * bore_half_d
    ax2.add_patch(mpatches.Rectangle(
        (pl_left_d, ddy + sign*bore_half_d),
        sd(PL_THICK), sign * plate_half_d,
        fc=C_ALUM, ec=C_OUT, lw=LW_MED, zorder=3))
    for i in range(12):
        y0 = ddy + sign*bore_half_d + sign*i*sd(5)
        if 0 < sign*(y0 - (ddy + sign*bore_half_d)) < plate_half_d:
            ax2.plot([pl_left_d, pl_right_d], [y0, y0 + sd(3)*sign], color='#AAAAAA', lw=0.4)

# Bore outline (H7 is the datum)
ax2.plot([pl_left_d, pl_right_d], [ddy + bore_half_d, ddy + bore_half_d], color=C_OUT, lw=LW_THICK)
ax2.plot([pl_left_d, pl_right_d], [ddy - bore_half_d, ddy - bore_half_d], color=C_OUT, lw=LW_THICK)

# Lens tube body (Al) — shown extending to left (exterior) and right (interior)
tube_extend_l = sd(80)  # extends 80mm to exterior
tube_extend_r = sd(60)  # extends 60mm to interior
ax2.add_patch(mpatches.Rectangle(
    (pl_left_d - tube_extend_l, ddy + bore_half_d),
    tube_extend_l + sd(PL_THICK) + tube_extend_r, sd(LT_OD - LB_D)/2,
    fc='#BBBBBB', ec=C_OUT, lw=LW_MED, zorder=4))  # top wall
ax2.add_patch(mpatches.Rectangle(
    (pl_left_d - tube_extend_l, ddy - bore_half_d - sd(LT_OD - LB_D)/2),
    tube_extend_l + sd(PL_THICK) + tube_extend_r, sd(LT_OD - LB_D)/2,
    fc='#BBBBBB', ec=C_OUT, lw=LW_MED, zorder=4))  # bottom wall

# Lens tube hollow bore (the clear aperture Ø165)
ax2.add_patch(mpatches.Rectangle(
    (pl_left_d - tube_extend_l, ddy - tube_id_half),
    tube_extend_l + sd(PL_THICK) + tube_extend_r, sd(LT_ID),
    fc='white', ec='none', lw=0, zorder=5))
ax2.plot([pl_left_d - tube_extend_l, pl_right_d + tube_extend_r], [ddy + tube_id_half]*2,
         color=C_OUT, lw=LW_THICK, zorder=6)
ax2.plot([pl_left_d - tube_extend_l, pl_right_d + tube_extend_r], [ddy - tube_id_half]*2,
         color=C_OUT, lw=LW_THICK, zorder=6)

# Set screws (3 shown in projection, only top one visible in section)
ss_x = pl_left_d + sd(PL_THICK/2)
ss_y = ddy + bore_half_d + sd((LT_OD - LB_D)/4)
ax2.add_patch(mpatches.Circle((ss_x, ss_y + sd(3)), sd(4), fc='#CCCCCC', ec=C_OUT, lw=LW_MED, zorder=7))
ax2.text(ss_x + sd(10), ss_y + sd(7), 'M8 SET SCREW\n(3× AT 120°)', fontsize=5, color='black')

# H7/g6 fit label
ax2.annotate('Ø175 H7/g6\nSLIDING FIT', xy=(pl_right_d, ddy - bore_half_d),
             xytext=(pl_right_d + 12, ddy - bore_half_d - 15),
             fontsize=5.5, color='black',
             arrowprops=dict(arrowstyle='->', color='black', lw=0.7))

# Optical axis
ax2.plot([pl_left_d - tube_extend_l - 10, pl_right_d + tube_extend_r + 20],
         [ddy, ddy], color=C_CL, lw=LW_THIN, linestyle=(0, (6, 2, 1, 2)))

# Travel annotation
ax2.annotate('', xy=(pl_left_d - tube_extend_l, ddy + tube_od_half + 8),
             xytext=(pl_left_d - tube_extend_l + sd(80), ddy + tube_od_half + 8),
             arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM, mutation_scale=5))
ax2.text(pl_left_d - tube_extend_l + sd(40), ddy + tube_od_half + 12,
         '±40mm FOCUS\nTRAVEL', ha='center', fontsize=5, color=C_DIM)

# Dims
ax2.annotate('', xy=(pl_right_d, ddy + bore_half_d),
             xytext=(pl_right_d, ddy - bore_half_d),
             arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM, mutation_scale=5))
ax2.text(pl_right_d + 5, ddy, 'Ø175\nBORE', ha='left', fontsize=5.5, color=C_DIM)

ax2.annotate('', xy=(pl_right_d, ddy + tube_od_half),
             xytext=(pl_right_d, ddy - tube_od_half),
             arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=LW_DIM, mutation_scale=5))
ax2.text(pl_right_d + 18, ddy, 'Ø174.5\nTUBE OD', ha='left', fontsize=5.5, color=C_DIM)

draw_dim_h(ax2, pl_left_d, pl_right_d, ddy - tube_od_half - 12, '15', above=False,
           fontsize=5.5, scale=0.5)

ax2.text(ddx - 30, ddy - tube_od_half - 24, 'DETAIL D — LENS FOCUSER (1:2)', ha='center',
         fontsize=6.5, fontweight='bold', color=C_RED)

# ── Sheet 2 notes ─────────────────────────────────────────────────────────────
notes2 = [
    'FOCUS ADJUSTMENT: SLIDE LENS TUBE (ITEM 6) WITHIN PLATE BORE (ITEM 3/ITEM 5) AND LOCK WITH 3×M8 SET SCREWS.',
    'AT 3.4m SUBJECT DISTANCE: POSITION LENS TUBE SO LENS PRINCIPAL PLANE IS 1,400mm FROM PINHOLE WALL INTERIOR FACE.',
    'AT 5.0m SUBJECT DISTANCE: RETRACT TUBE TO 1,604mm. MARK TUBE AT BOTH POSITIONS WITH SCRIBED LINES.',
    'INTERCHANGEABLE OPERATION: RELEASE 8×M12 BOLTS; WITHDRAW PLATE FROM DARK SIDE OF CAMERA; INSERT SECOND PLATE; RE-TORQUE BOLTS.',
    'SHUTTER (LENS PLATE ONLY): SLIDE BLACK Al PANEL (175mm × 55mm × 3mm) IN GUIDE RAILS — SPRING-LOADED TO CLOSED.',
    'PROCUREMENT: LENOX LASER (lenoxlaser.com) FOR PINHOLE DISCS — SPECIFY: SS-302 Ø50mm, APERTURE Ø2.17mm ±0.025mm.',
]
ax2.text(10, 55, 'OPERATIONAL NOTES:', fontsize=7, fontweight='bold')
for i, n in enumerate(notes2):
    ax2.text(10, 48 - i*6, n, fontsize=5.0, color='#222')

plt.tight_layout(pad=0)
plt.figtext(0.99, 0.005, "© 2026 Alvin Richards — GNU AGPLv3",
            ha="right", va="bottom", fontsize=6.0, color="#888888", style="italic")
out2 = '/Users/alvinrichards/dev/tbs/diagrams/plate-drawing-sheet2.png'
plt.savefig(out2, dpi=150, bbox_inches='tight', facecolor='white')
plt.savefig(str(out2).replace(".png", ".svg"), bbox_inches="tight", facecolor='white')
plt.close()
print(f'Saved sheet 2: {out2}')
