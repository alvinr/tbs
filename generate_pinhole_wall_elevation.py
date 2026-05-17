#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_pinhole_wall_elevation.py — Combined interior elevation of the
pinhole wall (Yd=0) showing all mounted systems for interference checking.

View: looking at the pinhole wall from inside the container.
Horizontal axis = X (mm), Vertical axis = Z (mm AFF).

Output: diagrams/pinhole-wall-elevation.png
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from tbs_constants import (
    C_LEN, C_WID, C_HGT,
    PH_X, PH_H, PH_D,
    EVAP_X, EVAP_W, EVAP_H,
    PWR_PANEL_X, PWR_PANEL_W, PWR_PANEL_H,
    EP_X, EP_W, EP_H_LO, EP_H_HI,
    BA_X, BA_W, BA_H_LO, BA_H_HI,
    PUMP_X, PUMP_W, PUMP_H_LO, PUMP_H_HI,
    FSKID_X, FSKID_W, FSKID_Z_LO, FSKID_Z_HI,
    F1_X, F2_X, F3_X, BB_OD, BB_H,
    FILT_HEAD_Z, FILT_SUMP_Z, FILT_PIPE_OD,
    TAP_X, TAP_Z,
    SHELF_X_L, SHELF_X_R, SHELF_H, SHELF_T, SHELF_HANGER_N,
    SHELF_YD_NEAR,
    WALKWAY_H, WALKWAY_GRATE_T, WALKWAY_W,
    WALKWAY_BRACKET_H, WALKWAY_BRACKET_T,
    CONTAINER_RIB_SPACING,
    PROC_TRAY_X_L, PROC_TRAY_X_R,
    RAIL_OFF,
    FAN_B_H, FAN_B_YD, FAN_DIAM,
    C_OUT, C_CL, C_DIM,
    C_ALUM, C_STEEL, C_EVAP, C_ELEC, C_BATT, C_PUMP,
    C_PINHOLE_EQ, C_WALL,
    ZONE_R_START,
    DIAGRAMS_DIR,
)
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_cl
from tbs_title_block import title_block

# ── Local constants (computed from tbs_constants) ────────────────────────────
HEADER_Z = FILT_HEAD_Z + 60          # 2000mm — filter header pipe Z
P02_X = 2750                          # pump P-02 center X (from filter skid diagram)
RISER_X = P02_X + 110                 # supply riser X
PH_TEST_X = F3_X + 200               # 3745mm — pH test point X
DV01_X = PH_TEST_X + 150             # 3895mm — diverter valve X
DV01_R = 50                           # DV-01 body radius

# Walkway X range (near walkway = pinhole wall side)
WK_X_L = PROC_TRAY_X_L + WALKWAY_W   # 470mm — near walkway left edge (past left walkway)
WK_X_R = PROC_TRAY_X_R               # 4629mm — near walkway right edge

# Pull-cord switches
PS_X_D = EVAP_X + EVAP_W // 2 - 60   # 1170mm — switch D
PS_X_G = EVAP_X + EVAP_W // 2 + 60   # 1290mm — switch G
PS_Z = C_HGT - 60                     # 2328mm — switch body Z
CORD_HANG_Z = 900                     # pull cord bottom Z

# Cable trunking
TK_H = 25                             # trunking height (mm)
TK_Z = C_HGT - TK_H                  # 2363mm — trunking bottom Z

# Power panel Z (flush-mount, exterior — shown as dashed outline)
PWR_Z_LO = EP_H_LO                   # 900mm — aligned with EP bottom

# Colors
C_FSKID = "#B0A898"   # filter skid frame (warm gray)
C_FILTER = "#4A90D9"  # filter housings (blue)
C_HDPE = "#2A5A2A"    # HDPE pipe (dark green)
C_SHELF = "#C8B06A"   # chemistry shelf (warm gold)
C_TRUNKING = "#808080" # cable trunking

# ── Scale and layout ────────────────────────────────────────────────────────
# S maps mm → figure inches.  Container 5893×2388 must fit comfortably.
# Available drawing area ≈ 22" wide × 8" tall (in a 26×12" figure).
S = 0.00335   # mm → inches  (≈1:7.6 at screen DPI, ≈1:20 at 300dpi print)
FW, FH = 26.0, 12.0
OX = 2.5    # drawing origin X offset (inches)
OZ = 2.5    # drawing origin Z offset (inches) — room for notes below

def sx(x_mm):
    """Convert X position (mm) to drawing x coordinate.
    Mirrored: viewing from inside container toward pinhole wall,
    high X (IBC end) is on the LEFT, low X (cargo door) on the RIGHT."""
    return OX + (C_LEN - x_mm) * S

def sz(z_mm):
    """Convert Z position (mm) to drawing y coordinate."""
    return OZ + z_mm * S

# ── Figure setup ────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(FW, FH), dpi=150)
ax.set_xlim(0, FW)
ax.set_ylim(0, FH)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

FONT = {"fontfamily": "monospace"}

# ── Helper: filled, labeled equipment block ─────────────────────────────────
def equip_block(x_mm, z_mm, w_mm, h_mm, label, fc, *,
                ec=C_OUT, lw=1.0, zorder=5, ls="-", alpha=0.85,
                label_fs=5.5, label_color=C_OUT):
    """Draw a filled rectangle with centered label."""
    # sx() is mirrored, so sx(x_mm + w_mm) < sx(x_mm) — use the left corner
    x_draw = sx(x_mm + w_mm)
    w_draw = sx(x_mm) - sx(x_mm + w_mm)  # positive width in drawing space
    rect = mpatches.FancyBboxPatch(
        (x_draw, sz(z_mm)), w_draw, h_mm * S,
        boxstyle="square,pad=0", facecolor=fc, edgecolor=ec,
        linewidth=lw, linestyle=ls, alpha=alpha, zorder=zorder)
    ax.add_patch(rect)
    # Centered label
    cx = sx(x_mm + w_mm / 2)
    cz = sz(z_mm + h_mm / 2)
    ax.text(cx, cz, label, ha="center", va="center",
            fontsize=label_fs, color=label_color, zorder=zorder + 1,
            **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 1. CONTAINER OUTLINE
# ═══════════════════════════════════════════════════════════════════════════
# Outer rectangle — sx() is mirrored, so sx(C_LEN) < sx(0)
wall_left = sx(C_LEN)   # left edge of container in drawing space
wall_right = sx(0)       # right edge
wall_w = wall_right - wall_left
ax.add_patch(mpatches.Rectangle(
    (wall_left, sz(0)), wall_w, C_HGT * S,
    facecolor="white", edgecolor=C_OUT, linewidth=2.0, zorder=1))

# Floor line (thicker)
ax.plot([wall_left, wall_right], [sz(0), sz(0)], color=C_OUT, lw=2.5, zorder=2)
# Ceiling line
ax.plot([wall_left, wall_right], [sz(C_HGT), sz(C_HGT)], color=C_OUT, lw=2.0, zorder=2)
# Left wall line
ax.plot([wall_left, wall_left], [sz(0), sz(C_HGT)], color=C_OUT, lw=2.0, zorder=2)
# Right wall line
ax.plot([wall_right, wall_right], [sz(0), sz(C_HGT)], color=C_OUT, lw=2.0, zorder=2)

# ── Corrugation ribs (faint vertical dashed lines) ─────────────────────────
rib_x = CONTAINER_RIB_SPACING
while rib_x < C_LEN:
    ax.plot([sx(rib_x), sx(rib_x)], [sz(0), sz(C_HGT)],
            color="#D0D0D0", lw=0.3, ls="--", zorder=1)
    rib_x += CONTAINER_RIB_SPACING

# ═══════════════════════════════════════════════════════════════════════════
# 2. CABLE TRUNKING (ceiling, full length)
# ═══════════════════════════════════════════════════════════════════════════
equip_block(0, TK_Z, C_LEN, TK_H, "", C_TRUNKING,
            lw=0.5, zorder=3, alpha=0.5, label_fs=4)
ax.text(sx(C_LEN / 2), sz(TK_Z + TK_H / 2), "CABLE TRUNKING (40×25mm PVC)",
        ha="center", va="center", fontsize=4, color="white", zorder=4, **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 3. WALKWAY DECK (near walkway along pinhole wall)
# ═══════════════════════════════════════════════════════════════════════════
# Grating deck
deck_z_bot = WALKWAY_H - WALKWAY_GRATE_T  # 75mm
equip_block(WK_X_L, deck_z_bot, WK_X_R - WK_X_L, WALKWAY_GRATE_T,
            "", C_STEEL, lw=0.6, zorder=4, alpha=0.4)
# Grating hatch marks
for gx in range(int(WK_X_L), int(WK_X_R), 80):
    ax.plot([sx(gx), sx(gx + 40)], [sz(deck_z_bot), sz(WALKWAY_H)],
            color=C_STEEL, lw=0.2, zorder=4, alpha=0.3)

# Label
ax.text(sx((WK_X_L + WK_X_R) / 2), sz(WALKWAY_H + 15),
        "NEAR WALKWAY DECK (Z=100mm)", ha="center", va="bottom",
        fontsize=4.5, color=C_DIM, zorder=10, **FONT)

# ── Walkway brackets (triangular gussets at rib positions) ──────────────────
bx = WK_X_L
while bx <= WK_X_R:
    # Find nearest rib
    nearest_rib = round(bx / CONTAINER_RIB_SPACING) * CONTAINER_RIB_SPACING
    if WK_X_L <= nearest_rib <= WK_X_R:
        # Small triangle: vertical leg on wall, horizontal arm
        tri_x = [sx(nearest_rib), sx(nearest_rib), sx(nearest_rib + WALKWAY_W * 0.15)]
        tri_z = [sz(0), sz(deck_z_bot), sz(0)]
        ax.fill(tri_x, tri_z, color=C_STEEL, alpha=0.5, zorder=3)
        ax.plot(tri_x + [tri_x[0]], tri_z + [tri_z[0]],
                color=C_OUT, lw=0.4, zorder=3)
    bx += CONTAINER_RIB_SPACING

# ── Zone labels for empty areas ───────────────────────────────────────────
# Left end zone (X=0–150mm, cargo door / hinged panel)
ax.text(sx(75), sz(C_HGT / 2), "CARGO DOOR\nEND\n(HINGED PANEL)",
        ha="center", va="center", fontsize=5, color="#AAAAAA",
        style="italic", zorder=2, **FONT)

# Right end zone (X=4649–5893mm, IBC stack)
ax.text(sx(ZONE_R_START + (C_LEN - ZONE_R_START) / 2), sz(C_HGT / 2),
        "IBC STACK\nZONE", ha="center", va="center",
        fontsize=5, color="#AAAAAA", style="italic", zorder=2, **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 4. EQUIPMENT BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

# ── Evaporative cooler ──────────────────────────────────────────────────────
equip_block(EVAP_X, RAIL_OFF, EVAP_W, EVAP_H,
            "EVAPORATIVE\nCOOLER", C_EVAP, label_fs=6)

# ── External power panel (flush-mount, exterior — dashed outline) ──────────
equip_block(PWR_PANEL_X, PWR_Z_LO, PWR_PANEL_W, PWR_PANEL_H,
            "EXT. POWER\nPANEL\n(FLUSH)", C_ALUM,
            ls="--", alpha=0.4, label_fs=4.5)

# ── Electrical panel (EP) ──────────────────────────────────────────────────
equip_block(EP_X, EP_H_LO, EP_W, EP_H_HI - EP_H_LO,
            "ELECTRICAL\nPANEL (EP)", C_ELEC, label_fs=5)

# ── Battery bank (BAT) ────────────────────────────────────────────────────
equip_block(BA_X, BA_H_LO, BA_W, BA_H_HI - BA_H_LO,
            "BATTERY\nBANK\n(2× LiFePO4)", C_BATT, label_fs=4.5, label_color="white")

# ── Pinhole aperture ──────────────────────────────────────────────────────
ph_r = 15  # drawing radius (exaggerated for visibility)
draw_cl(ax, sx(PH_X), sz(PH_H), ph_r * S,
        horiz=True, vert=True, color=C_CL, lw=0.6, ext_factor=3.0)
ax.add_patch(plt.Circle((sx(PH_X), sz(PH_H)), ph_r * S,
             fill=True, facecolor=C_PINHOLE_EQ, edgecolor=C_OUT,
             linewidth=1.2, zorder=8))
ax.text(sx(PH_X), sz(PH_H - 80), "PINHOLE\nØ2.17mm",
        ha="center", va="top", fontsize=5, color=C_PINHOLE_EQ,
        zorder=10, **FONT)

# ── Pump manifold ─────────────────────────────────────────────────────────
equip_block(PUMP_X, PUMP_H_LO, PUMP_W, PUMP_H_HI - PUMP_H_LO,
            "PUMP\nMANIFOLD", C_PUMP, label_fs=5)

# ── Filter skid frame ────────────────────────────────────────────────────
equip_block(FSKID_X, FSKID_Z_LO, FSKID_W, FSKID_Z_HI - FSKID_Z_LO,
            "", C_FSKID, alpha=0.35, lw=1.2)
ax.text(sx(FSKID_X + FSKID_W / 2), sz(FSKID_Z_HI - 30),
        "FILTER SKID FRAME", ha="center", va="top",
        fontsize=4.5, color=C_DIM, zorder=10, **FONT)

# ── Filter housings F1, F2, F3 ───────────────────────────────────────────
for fx, flabel in [(F1_X, "F1"), (F2_X, "F2"), (F3_X, "F3")]:
    # Housing body (simplified rectangle)
    hx = fx - BB_OD / 2
    hz = FILT_SUMP_Z
    hh = FILT_HEAD_Z - FILT_SUMP_Z
    equip_block(hx, hz, BB_OD, hh, flabel, C_FILTER,
                lw=0.8, zorder=6, alpha=0.8, label_fs=5.5, label_color="white")

# ── Header pipe (single line at this scale) ──────────────────────────────
ax.plot([sx(RISER_X), sx(DV01_X)], [sz(HEADER_Z), sz(HEADER_Z)],
        color=C_HDPE, lw=1.5, zorder=5)

# ── Supply riser ─────────────────────────────────────────────────────────
ax.plot([sx(RISER_X), sx(RISER_X)], [sz(PUMP_H_HI), sz(HEADER_Z)],
        color=C_HDPE, lw=1.5, zorder=5)
# Annotation
ax.annotate("", xy=(sx(RISER_X), sz(PUMP_H_HI + 80)),
            xytext=(sx(RISER_X), sz(PUMP_H_HI)),
            arrowprops=dict(arrowstyle="-|>", color=C_HDPE, lw=1.2), zorder=10)

# ── pH test point ────────────────────────────────────────────────────────
ax.plot([sx(PH_TEST_X), sx(PH_TEST_X)],
        [sz(HEADER_Z), sz(HEADER_Z + 40)],
        color=C_HDPE, lw=1.5, zorder=5)
ax.add_patch(plt.Circle((sx(PH_TEST_X), sz(HEADER_Z + 50)), 10 * S,
             fill=True, facecolor="white", edgecolor=C_OUT,
             linewidth=0.8, zorder=6))
ax.text(sx(PH_TEST_X), sz(HEADER_Z + 50), "pH",
        ha="center", va="center", fontsize=3.5, color=C_OUT, zorder=7, **FONT)

# ── DV-01 diverter valve ─────────────────────────────────────────────────
ax.add_patch(plt.Circle((sx(DV01_X), sz(HEADER_Z)), DV01_R * S,
             fill=True, facecolor="white", edgecolor=C_OUT,
             linewidth=1.0, zorder=6))
ax.text(sx(DV01_X), sz(HEADER_Z), "DV-01",
        ha="center", va="center", fontsize=3.5, color=C_OUT, zorder=7, **FONT)

# ── Chemistry tap TAP-01 ─────────────────────────────────────────────────
# Small symbol on wall
tap_w, tap_h = 30, 60
equip_block(TAP_X - tap_w / 2, TAP_Z - tap_h / 2, tap_w, tap_h,
            "", C_HDPE, lw=0.6, zorder=6, alpha=0.7)
leader(ax, sx(TAP_X), sz(TAP_Z),
       sx(TAP_X + 120), sz(TAP_Z + 80),
       "TAP-01\n(BV-06)", fs=4.5, color=C_DIM, zorder=10)

# ── Pull-cord switches ───────────────────────────────────────────────────
for psx, plabel in [(PS_X_D, "D"), (PS_X_G, "G")]:
    # Switch body (small rectangle at ceiling)
    sw_w, sw_h = 30, 30
    equip_block(psx - sw_w / 2, PS_Z - sw_h / 2, sw_w, sw_h,
                plabel, "#F0E0C0", lw=0.5, zorder=6, alpha=0.7, label_fs=4)
    # Pull cord (dashed line)
    ax.plot([sx(psx), sx(psx)], [sz(PS_Z - sw_h / 2), sz(CORD_HANG_Z)],
            color=C_DIM, lw=0.4, ls=":", zorder=5)

# ── Shelf hanger rods (ghost — shelf is at Yd=300, not on wall face) ─────
# Show the 4 hanger rod positions as thin dashed vertical lines
hanger_xs = [SHELF_X_L, SHELF_X_R]  # 2 pairs at shelf corners
for hx in hanger_xs:
    ax.plot([sx(hx), sx(hx)], [sz(SHELF_H), sz(TK_Z)],
            color=C_SHELF, lw=0.5, ls="--", zorder=3, alpha=0.5)

# Shelf ghost outline (dashed, it's behind the walkway plane at Yd=300)
equip_block(SHELF_X_L, SHELF_H - SHELF_T, SHELF_X_R - SHELF_X_L, SHELF_T,
            "", C_SHELF, ls="--", alpha=0.3, lw=0.6, zorder=3)
ax.text(sx((SHELF_X_L + SHELF_X_R) / 2), sz(SHELF_H - SHELF_T - 30),
        "CHEM SHELF (Yd=300, BEHIND)", ha="center", va="top",
        fontsize=4, color=C_SHELF, style="italic", zorder=10, **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 5. DIMENSION LINES — key clearances and positions
# ═══════════════════════════════════════════════════════════════════════════

# Right-side vertical dims (cargo door end = X=0 = right side after mirror)
rx0 = sx(0) + 0.15        # first dim line
rx1 = rx0 + 0.5           # second

# Full container height
draw_dim_v(ax, rx0, sz(0), sz(C_HGT),
           f"{C_HGT}mm", offset=0.2, fs=5, right=True)

# Walkway deck height
draw_dim_v(ax, rx1, sz(0), sz(WALKWAY_H),
           f"{WALKWAY_H}", offset=0.2, fs=5, right=True)

# Filter skid Z range
draw_dim_v(ax, rx1, sz(FSKID_Z_LO), sz(FSKID_Z_HI),
           f"{FSKID_Z_HI - FSKID_Z_LO}", offset=0.2, fs=5, right=True)

# Left-side vertical dims (IBC end = X=C_LEN = left side after mirror)
lx0 = sx(C_LEN) - 0.15
lx1 = lx0 - 0.5

# Pinhole height
draw_dim_v(ax, lx0, sz(0), sz(PH_H),
           f"{PH_H}mm", offset=0.2, fs=5)

# ── Horizontal dims below floor ─────────────────────────────────────────────
# Row 1: equipment widths
row1_z = sz(0) - 0.20
row2_z = row1_z - 0.25

# Key gap dimensions
evap_r = EVAP_X + EVAP_W
pump_r = PUMP_X + PUMP_W
ba_r = BA_X + BA_W

# Evap → EP gap
draw_dim_h(ax, sx(evap_r), sx(EP_X), row1_z,
           f"{EP_X - evap_r}mm", offset=0.15, fs=4.5, above=False)

# BAT right → Pinhole
draw_dim_h(ax, sx(ba_r), sx(PH_X), row1_z,
           f"{PH_X - ba_r}mm", offset=0.15, fs=4.5, above=False)

# Pump → Filter skid gap
draw_dim_h(ax, sx(pump_r), sx(FSKID_X), row1_z,
           f"{FSKID_X - pump_r}mm", offset=0.15, fs=4.5, above=False)

# Full container length (below all)
draw_dim_h(ax, sx(0), sx(C_LEN), row2_z,
           f"{C_LEN}mm", offset=0.15, fs=5, above=False)

# ── Clearance leaders ──────────────────────────────────────────────────────
fskid_clr = TK_Z - FSKID_Z_HI
leader(ax, sx(FSKID_X + FSKID_W / 2), sz(FSKID_Z_HI),
       sx(FSKID_X + FSKID_W + 250), sz(FSKID_Z_HI + 250),
       f"SKID TOP → TRUNKING: {fskid_clr}mm", fs=4.5, color=C_DIM, zorder=10)

ep_clr = C_HGT - EP_H_HI
leader(ax, sx(EP_X + EP_W / 2), sz(EP_H_HI),
       sx(EP_X - 300), sz(EP_H_HI + 300),
       f"EP TOP → CEILING: {ep_clr}mm", fs=4.5, color=C_DIM, zorder=10)

# ═══════════════════════════════════════════════════════════════════════════
# 6. X-POSITION ANNOTATIONS (absolute positions along top)
# ═══════════════════════════════════════════════════════════════════════════
ann_y = sz(C_HGT) + 0.15
items = [
    (EVAP_X, "EVAP\nX=930"),
    (EP_X, "EP\nX=1600"),
    (BA_X, "BAT\nX=1810"),
    (PH_X, "PH\nX=2399"),
    (PUMP_X, "PUMP\nX=2500"),
    (FSKID_X, "FSKID\nX=2850"),
    (TAP_X, "TAP\nX=3729"),
]
for ix_mm, ilabel in items:
    ax.plot([sx(ix_mm), sx(ix_mm)], [sz(C_HGT), ann_y],
            color=C_DIM, lw=0.3, ls=":", zorder=1)
    ax.text(sx(ix_mm), ann_y + 0.05, ilabel, ha="center", va="bottom",
            fontsize=3.5, color=C_DIM, zorder=10, **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 7. INTERFERENCE NOTES
# ═══════════════════════════════════════════════════════════════════════════
notes = [
    "1. All pipe: 1\" HDPE Sch40 (OD=33mm), single-line representation at this scale.",
    "2. Ext. power panel (dashed) is flush-mount on EXTERIOR face — no interior conflict with evap cooler.",
    "3. Chemistry shelf (dashed) is ceiling-hung at Yd=300mm — behind near walkway plane, not on wall face.",
    "4. Shelf hanger rods pass through cable trunking zone — requires grommets/slots in trunking lid.",
    "5. Pump manifold → filter skid gap: 50mm. Riser pipe bridges this gap vertically.",
    "6. Battery right edge (X=2310) clears pinhole cone left boundary (X=2319 at Yd=0) by 9mm.",
]
note_y = 0.06
for i, note in enumerate(notes):
    ax.text(0.01, note_y + i * 0.018, note, transform=ax.transAxes,
            fontsize=4.5, color=C_DIM, va="bottom", **FONT)

# ═══════════════════════════════════════════════════════════════════════════
# 8. TITLE BLOCK
# ═══════════════════════════════════════════════════════════════════════════
title_block(ax, "SHEET 1 OF 1",
            drawing_title="PINHOLE WALL — COMBINED INTERIOR ELEVATION",
            subtitle="ALL SYSTEMS · INTERFERENCE CHECK",
            scale_note="SCALE 1:20  ·  ALL DIMS IN mm",
            doc_id="TBS-001 · Pinhole Wall")

# ── Save ────────────────────────────────────────────────────────────────────
os.makedirs(DIAGRAMS_DIR, exist_ok=True)
out = os.path.join(DIAGRAMS_DIR, "pinhole-wall-elevation.png")
fig.savefig(out, dpi=150, facecolor="white", edgecolor="none")
plt.close(fig)
print(f"Pinhole wall elevation → {out}")
