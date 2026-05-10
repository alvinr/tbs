#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_assembly_fabrication.py

Generates two-sheet assembly fabrication drawing for TBS-001
(redesigned film-plane-reduction layout).

  Sheet 1 — Long-section elevation  (1:50)
    View along short axis (+Y), horizontal = long axis X 0–5893mm,
    vertical = height H 0–2388mm.
    Three zones: left end zone (shadow-free), optical zone, right end zone.

  Sheet 2 — End elevation, cargo door end  (1:20)
    View from the short end wall (X=0), looking into the container (+X).
    Horizontal = container width CW 0–2362mm,  vertical = height H 0–2388mm.
    Drum Ø750mm appears as a rectangle centred at CW/2.

ASPECT RATIO RULE: figsize always derived from data limits.
                   ax.set_aspect("equal") always set.
"""

import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, draw_cl_h, draw_cl_v, hatch_rect
from tbs_constants import (
    C_LEN, C_WID, C_HGT,
    FP_X_L, FP_X_R, FP_Y,
    PH_X, PH_H,
    ZONE_L_END, ZONE_R_START,
    DRUM_CX, DRUM_D, DRUM_R, DRUM_H_LT,
    EVAP_X, EVAP_Y, EVAP_W, EVAP_D, EVAP_H,
    EP_X, EP_W, EP_H_LO, EP_H_HI,
    BA_X, BA_W, BA_H_LO, BA_H_HI,
    PUMP_X, PUMP_W, PUMP_H_LO, PUMP_H_HI,
    PWR_PANEL_X, PWR_PANEL_W, PWR_PANEL_H,
    IBC_COL_X, IBC_W, IBC_H_STK, IBC_H_600,
    IBC_FAR_Y,
    PANEL_CORNER_T, PANEL_CENTER_T,
    RAIL_X_L, RAIL_X_R,
    FAN_A_H, FAN_B_H, FAN_A_YD, FAN_B_YD, FAN_DIAM, DUCT_HEIGHT,
    DIAGRAMS_DIR, SVG_DIR, svg_path,
    C_OUT, C_CL, C_DIM,
    C_WASTE_IBC, C_LT_DRUM, C_BLUE_IBC, C_BROWN_IBC,
    C_EVAP, C_ELEC, C_BATT, C_PUMP,
)

os.makedirs(DIAGRAMS_DIR, exist_ok=True)
os.makedirs(SVG_DIR, exist_ok=True)

RAIL_OFF   = 100       # floor/ceiling offset for all equipment (mm)
DRUM_H_ELV = DRUM_H_LT  # 2000mm — drum height in elevation view
DRUM_CY    = C_WID // 2  # drum centre in Y direction = container width centre = 1181mm

# ── Palette ───────────────────────────────────────────────────────────────────
BG          = "#FFFFFF"
C_ALUM      = "#C8D8E8"
C_STEEL     = "#B0B0B8"
C_GASKT     = "#5A3020"
C_HATCH     = "#909090"
C_FILL_INT  = "#F4F4F4"

C_ZONE_L    = "#FFF0E0"
C_ZONE_O    = "#F0FFF0"
C_ZONE_R    = "#E8F0FF"


FS_SM = 7.0
FS_MD = 8.5
FS_LG = 10.0


# ── Shared helpers ─────────────────────────────────────────────────────────────
def callout(ax, cx, cy, number, r=60, fs=FS_SM - 0.5):
    ax.add_patch(plt.Circle((cx, cy), r, facecolor="white", edgecolor=C_OUT,
                             linewidth=0.8, zorder=8))
    ax.text(cx, cy, str(number), ha="center", va="center",
            fontsize=fs, color=C_OUT, fontweight="bold", zorder=9)

def equip_blk(ax, x, y, w, h, fc, ec=C_OUT, lw=0.6, alpha=0.75, zorder=3):
    ax.add_patch(mpatches.Rectangle((x, y), w, h,
                 facecolor=fc, edgecolor=ec, linewidth=lw, alpha=alpha, zorder=zorder))


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — LONG-SECTION ELEVATION  (1:50)
# ═══════════════════════════════════════════════════════════════════════════════

def sheet1():
    X_LO, X_HI = -600, 8400   # right edge must clear ref table: C_LEN+800+1380+200 = 8273
    Y_LO, Y_HI = -700, 3200

    FIG_W = 26.0
    FIG_H = FIG_W * (Y_HI - Y_LO) / (X_HI - X_LO)
    DPI = 150

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Y_LO, Y_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Zone fills ────────────────────────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle((0, 0), ZONE_L_END, C_HGT,
                 facecolor=C_ZONE_L, edgecolor="none", alpha=0.6, zorder=0))
    ax.add_patch(mpatches.Rectangle((ZONE_L_END, 0), ZONE_R_START-ZONE_L_END, C_HGT,
                 facecolor=C_ZONE_O, edgecolor="none", alpha=0.5, zorder=0))
    ax.add_patch(mpatches.Rectangle((ZONE_R_START, 0), C_LEN-ZONE_R_START, C_HGT,
                 facecolor=C_ZONE_R, edgecolor="none", alpha=0.6, zorder=0))

    # Zone boundary lines
    for xb in [ZONE_L_END, ZONE_R_START]:
        ax.plot([xb, xb], [0, C_HGT], color=C_DIM, lw=0.8, ls="--",
                dashes=(6, 4), zorder=4)

    # Zone labels
    ax.text(ZONE_L_END/2,          C_HGT+200, f"LEFT END ZONE\nX=0–{ZONE_L_END}mm",
            ha="center", va="top", fontsize=FS_SM-0.5, color="#805000",
            fontweight="bold", zorder=5)
    ax.text((ZONE_L_END+ZONE_R_START)/2, C_HGT+200,
            f"OPTICAL ZONE\nX={ZONE_L_END}–{ZONE_R_START}mm",
            ha="center", va="top", fontsize=FS_SM-0.5, color="#006000",
            fontweight="bold", zorder=5)
    ax.text((ZONE_R_START+C_LEN)/2, C_HGT+200,
            f"RIGHT END ZONE\nX={ZONE_R_START}–{C_LEN}mm",
            ha="center", va="top", fontsize=FS_SM-0.5, color="#004080",
            fontweight="bold", zorder=5)

    # ── Container walls (hatched) and outline ─────────────────────────────────
    WALL_T = 80
    hatch_rect(ax, -WALL_T, -WALL_T, C_LEN+2*WALL_T, WALL_T, color=C_STEEL, hatch="///")
    hatch_rect(ax, -WALL_T, C_HGT,   C_LEN+2*WALL_T, WALL_T, color=C_STEEL, hatch="///")
    hatch_rect(ax, -WALL_T, -WALL_T, WALL_T, C_HGT+2*WALL_T, color=C_STEEL, hatch="///")
    hatch_rect(ax, C_LEN,   -WALL_T, WALL_T, C_HGT+2*WALL_T, color=C_STEEL, hatch="///")
    ax.add_patch(mpatches.Rectangle((0, 0), C_LEN, C_HGT,
                 facecolor="none", edgecolor=C_OUT, linewidth=1.6, zorder=5))

    # ── Film-plane rail reference lines ───────────────────────────────────────
    for xl in [RAIL_X_L, RAIL_X_R]:
        ax.plot([xl, xl], [0, C_HGT], color=C_CL, lw=0.7, ls="--",
                dashes=(10, 3), zorder=4, alpha=0.6)
    ax.plot([RAIL_X_L, RAIL_X_R], [RAIL_OFF, RAIL_OFF],
            color=C_CL, lw=1.0, ls="--", dashes=(8, 3), zorder=5)
    ax.plot([RAIL_X_L, RAIL_X_R], [C_HGT-RAIL_OFF, C_HGT-RAIL_OFF],
            color=C_CL, lw=1.0, ls="--", dashes=(8, 3), zorder=5)

    # ── Pinhole symbol ────────────────────────────────────────────────────────
    ph_r = 50
    ax.add_patch(plt.Circle((PH_X, PH_H), ph_r,
                 facecolor="white", edgecolor=C_OUT, linewidth=1.2, zorder=7))
    ax.plot([PH_X-150, PH_X+150], [PH_H, PH_H], color=C_OUT, lw=0.8, zorder=8)
    ax.plot([PH_X, PH_X], [PH_H-150, PH_H+150], color=C_OUT, lw=0.8, zorder=8)
    draw_cl_h(ax, 0, C_LEN, PH_H)
    ax.text(PH_X+120, PH_H+120,
            f"Pinhole\nX={PH_X}mm\nH={PH_H}mm",
            ha="left", va="bottom", fontsize=FS_SM-1, color=C_OUT, zorder=8)

    # ── LEFT END ZONE — hinged panel + drum + evap ────────────────────────────
    # Hinged panel — stepped profile (rev 4): 40mm corners, 120mm center
    # Corner zone (40mm) shown as solid, center zone (120mm) as dashed outline
    ax.add_patch(mpatches.Rectangle((0, 0), PANEL_CORNER_T, C_HGT,
                 facecolor=C_ALUM, edgecolor=C_OUT, linewidth=0.8, alpha=0.7, zorder=4))
    ax.add_patch(mpatches.Rectangle((0, 0), PANEL_CENTER_T, C_HGT,
                 facecolor="none", edgecolor=C_OUT, linewidth=0.6, ls=(0, (4, 3)),
                 alpha=0.5, zorder=4))

    # Revolving drum: centre at X=0, bottom at RAIL_OFF
    equip_blk(ax, -DRUM_R, RAIL_OFF, DRUM_D, DRUM_H_ELV, C_LT_DRUM, lw=1.0, alpha=0.9, zorder=5)
    draw_cl_v(ax, DRUM_CX, RAIL_OFF, RAIL_OFF+DRUM_H_ELV+150)
    ax.text(DRUM_CX, RAIL_OFF+DRUM_H_ELV/2+175,
            f"REVOLVING DRUM\nVERTICAL AXIS\nO{DRUM_D}x{DRUM_H_ELV}mm H",
            ha="center", va="center", fontsize=FS_SM-1.5, color=C_OUT,
            style="italic", zorder=6)

    # Evap cooler: X=400-1000, bottom at RAIL_OFF
    equip_blk(ax, EVAP_X, RAIL_OFF, EVAP_W, EVAP_H, C_EVAP, zorder=4)
    ax.text(EVAP_X+EVAP_W/2, RAIL_OFF+EVAP_H/2,
            "EVAP\nCOOLER", ha="center", va="center",
            fontsize=FS_SM-1.5, color="white", zorder=5)

    # 55-gal drums ×2 — one per Yd corner (near wall + far wall), both at CX=330mm.
    # (waste drums eliminated in rev 5 — left zone is light trap only)

    # ── PINHOLE WALL EQUIPMENT (flush on near long wall) ──────────────────────
    # Electrical panel
    equip_blk(ax, EP_X, EP_H_LO, EP_W, EP_H_HI-EP_H_LO, C_ELEC, lw=0.8, zorder=4)
    ax.text(EP_X+EP_W/2, (EP_H_LO+EP_H_HI)/2, "ELEC\nPANEL",
            ha="center", va="center", fontsize=FS_SM-2, color=C_OUT, zorder=5)
    # Battery bank
    equip_blk(ax, BA_X, BA_H_LO, BA_W, BA_H_HI-BA_H_LO, C_BATT, zorder=4)
    ax.text(BA_X+BA_W/2, (BA_H_LO+BA_H_HI)/2, "BATT",
            ha="center", va="center", fontsize=FS_SM-2, color="white", zorder=5)
    # Pump manifold
    equip_blk(ax, PUMP_X, PUMP_H_LO, PUMP_W, PUMP_H_HI-PUMP_H_LO, C_PUMP, zorder=4)
    ax.text(PUMP_X+PUMP_W/2, (PUMP_H_LO+PUMP_H_HI)/2, "PUMP",
            ha="center", va="center", fontsize=FS_SM-2, color="white", zorder=5)

    # ── External power panel (flush-mount in pinhole wall — ghost) ──────────
    # Side elevation: panel is flush in the pinhole wall (bottom wall, Y=0).
    # Show the aluminum face plate as a ghost rectangle on the wall face,
    # and the cutout as a lighter dashed rectangle inside it.
    # Height: centered at same level as electrical panel (~900–1100mm).
    from tbs_constants import PWR_PANEL_CUTOUT_W, PWR_PANEL_CUTOUT_H
    PP_CTR_H = (EP_H_LO + EP_H_HI) / 2   # center at same height as EP
    PP_PLATE_BOT = PP_CTR_H - PWR_PANEL_H / 2
    PP_CUT_BOT   = PP_CTR_H - PWR_PANEL_CUTOUT_H / 2

    # Aluminum face plate (ghost outline on exterior wall face)
    ax.add_patch(mpatches.Rectangle(
        (PWR_PANEL_X, PP_PLATE_BOT), PWR_PANEL_W, PWR_PANEL_H,
        facecolor="none", edgecolor=C_ALUM, linewidth=1.5,
        ls=(0, (5, 3)), alpha=0.7, zorder=6))
    # Wall cutout (dashed, inside plate)
    cut_x = PWR_PANEL_X + (PWR_PANEL_W - PWR_PANEL_CUTOUT_W) / 2
    ax.add_patch(mpatches.Rectangle(
        (cut_x, PP_CUT_BOT), PWR_PANEL_CUTOUT_W, PWR_PANEL_CUTOUT_H,
        facecolor="none", edgecolor=C_DIM, linewidth=0.8,
        ls=(0, (3, 2)), alpha=0.5, zorder=6))
    ax.text(PWR_PANEL_X + PWR_PANEL_W / 2, PP_CTR_H,
            "EXT PWR\nPANEL",
            ha="center", va="center", fontsize=FS_SM - 2,
            color=C_ALUM, style="italic", fontweight="bold",
            alpha=0.7, zorder=7)

    # ── RIGHT END ZONE — IBC column + drum column ─────────────────────────────
    # Blue IBC stack x2 (front in depth, 2020mm tall)
    equip_blk(ax, IBC_COL_X, RAIL_OFF, IBC_W, IBC_H_STK, C_BLUE_IBC, zorder=5)
    # Stacking interface line
    ax.plot([IBC_COL_X, IBC_COL_X+IBC_W], [RAIL_OFF+IBC_H_600, RAIL_OFF+IBC_H_600],
            color="white", lw=0.8, ls="--", alpha=0.7, zorder=6)
    ax.text(IBC_COL_X+IBC_W/2, RAIL_OFF+IBC_H_STK/2+175,
            "BLUE IBC x2\nSTACKED (FRONT)\n2x600L H=2020mm",
            ha="center", va="center", fontsize=FS_SM-1.5, color="white", zorder=6)

    # Brown IBC x1 (behind Blue, Y-depth stacked — draw at same X, dimmer)
    equip_blk(ax, IBC_COL_X, RAIL_OFF, IBC_W, IBC_H_600,
              C_BROWN_IBC, alpha=0.45, zorder=3)

    # (drums relocated to left zone — no drum column in right zone)

    # ── Processing tray (304 SS, optical zone floor) ─────────────────────────
    TRAY_X0 = RAIL_X_L + 20     # 645mm — 20mm clearance inside rail
    TRAY_X1 = RAIL_X_R - 20     # 4629mm
    TRAY_H  = 50                # 50mm rim height
    ax.add_patch(mpatches.Rectangle((TRAY_X0, 0), TRAY_X1 - TRAY_X0, TRAY_H,
                 facecolor=C_STEEL, edgecolor=C_OUT, linewidth=0.8,
                 alpha=0.6, zorder=4))
    ax.text((TRAY_X0 + TRAY_X1) / 2, TRAY_H / 2,
            "PROCESSING TRAY (304 SS)  —  50mm rim  —  2 panels bolted at center",
            ha="center", va="center", fontsize=FS_SM - 2, color=C_OUT,
            style="italic", zorder=5)

    # ── Fans — shown on their correct end walls at correct heights ───────────────
    # Fan B (exhaust): cargo door end wall (X=0), HIGH H=FAN_B_H=1800mm
    # Fan A (intake):  far end wall (X=C_LEN),   LOW  H=FAN_A_H=600mm
    FAN_HH = DUCT_HEIGHT   # hatch block height = duct opening height (200mm)
    hatch_rect(ax, -WALL_T, FAN_B_H - FAN_HH//2, WALL_T, FAN_HH, color=C_ALUM, hatch="xx", alpha=0.6)  # Fan B left wall
    hatch_rect(ax, C_LEN,   FAN_A_H - FAN_HH//2, WALL_T, FAN_HH, color=C_ALUM, hatch="xx", alpha=0.6)  # Fan A right wall

    # ── Callout bubbles ───────────────────────────────────────────────────────
    CALL_R = 80
    callouts_s1 = [
        (PH_X,                    PH_H+350,              "1"),  # Pinhole
        (RAIL_X_L,                C_HGT-RAIL_OFF-200,    "2"),  # Rails (left)
        (RAIL_X_R,                RAIL_OFF+200,           "3"),  # Film plane mechanism
        (EVAP_X+EVAP_W/2,         RAIL_OFF+EVAP_H/2,     "4"),  # Evap cooler
        (EP_X+EP_W/2,             (EP_H_LO+EP_H_HI)/2,   "5"),  # Electrical
        (DRUM_CX,                 RAIL_OFF+DRUM_H_ELV/2,  "6"),  # Drum + panel
        (IBC_COL_X+IBC_W/2,      RAIL_OFF+IBC_H_STK/2,  "7"),  # IBCs (4× 2×2 stack)
        (PUMP_X+PUMP_W/2,         (PUMP_H_LO+PUMP_H_HI)/2, "8"),  # Pump
        (-WALL_T/2, FAN_B_H,      "9"),  # Fan B exhaust (door end, HIGH)
        (C_LEN+WALL_T/2, FAN_A_H, "10"),  # Fan A intake (far end, LOW)
        ((TRAY_X0+TRAY_X1)/2,     TRAY_H+180, "11"),  # Processing tray
        (PWR_PANEL_X - 120, PP_CTR_H, "12"),  # Ext power panel
    ]
    for (cx, cy, num) in callouts_s1:
        callout(ax, cx, cy, num, r=CALL_R)

    # ── Dimensions ────────────────────────────────────────────────────────────
    DIM_TOP  = C_HGT + 400
    DIM_BOT  = -350
    DIM_LEFT = -450

    draw_dim_h(ax, 0, C_LEN, DIM_TOP, f"Container interior  {C_LEN}mm",
               offset=107, fs=FS_SM)
    draw_dim_h(ax, ZONE_L_END, ZONE_R_START, DIM_TOP+220,
               f"Optical zone (film plane rail span)  {ZONE_R_START-ZONE_L_END}mm",
               offset=107, fs=FS_SM, color=C_CL)
    draw_dim_h(ax, 0, ZONE_L_END, DIM_BOT,
               f"Left zone\n{ZONE_L_END}mm", offset=80, fs=FS_SM, color="#805000")
    draw_dim_h(ax, ZONE_R_START, C_LEN, DIM_BOT,
               f"Right zone\n{C_LEN-ZONE_R_START}mm", offset=80, fs=FS_SM, color="#004080")
    draw_dim_h(ax, 0, PH_X, DIM_BOT-220,
               f"Pinhole X={PH_X}mm", offset=80, fs=FS_SM)
    draw_dim_v(ax, C_LEN+400, 0, C_HGT, f"H={C_HGT}mm", offset=107, fs=FS_SM)
    draw_dim_v(ax, C_LEN+700, 0, RAIL_OFF, f"Rail offset\n{RAIL_OFF}mm", offset=80, fs=FS_SM)
    draw_dim_v(ax, DIM_LEFT, 0, PH_H, f"PH H={PH_H}mm", offset=80, fs=FS_SM)

    # ── Reference table ───────────────────────────────────────────────────────
    REF_X  = C_LEN + 800
    REF_Y  = C_HGT - 80
    REF_DY = 115
    REF_W  = 1380
    REF_H  = 13 * REF_DY + 80

    ax.add_patch(mpatches.Rectangle((REF_X, REF_Y-REF_H), REF_W, REF_H,
                 facecolor="#F8F8FA", edgecolor=C_OUT, linewidth=0.8, zorder=5))
    ax.text(REF_X+REF_W/2, REF_Y-25, "DRAWING REFERENCE",
            ha="center", va="top", fontsize=FS_SM, color=C_OUT,
            fontweight="bold", zorder=6)
    refs = [
        ("1",  "Pinhole aperture plate",            "TBS-P01"),
        ("2",  "Film plane rails x4",               "TBS-FM01"),
        ("3",  "Film plane mechanism",               "TBS-FM01"),
        ("4",  "Evaporative cooler",                 "TBS-EL01"),
        ("5",  "Electrical panel + battery bank",    "TBS-EL01"),
        ("6",  "Hinged panel + revolving drum",      "TBS-LT01"),
        ("7",  "4× IBC 2×2 stack (right zone — Blue ×2 top, Brown + Waste bottom)","TBS-WS01"),
        ("8",  "Pump manifold",                      "TBS-WS01"),
        ("9",  "Exhaust fan",                        "TBS-EL01"),
        ("10", "Intake fan",                         "TBS-EL01"),
        ("11", "Processing tray (304 SS, 2 panels)", "TBS-WS01"),
        ("12", "Ext power panel (flush-mount, exterior)", "TBS-EL01"),
    ]
    for i, (num, desc, ref) in enumerate(refs):
        yy = REF_Y - 75 - i*REF_DY
        ax.text(REF_X+25,        yy, num,  ha="left",  va="center",
                fontsize=FS_SM,   color=C_OUT, fontweight="bold", zorder=6)
        ax.text(REF_X+110,       yy, desc, ha="left",  va="center",
                fontsize=FS_SM-0.5, color=C_OUT, zorder=6)
        ax.text(REF_X+REF_W-20, yy, ref,  ha="right", va="center",
                fontsize=FS_SM-1, color=C_DIM, zorder=6)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 2",
                drawing_title="ASSEMBLY — LONG SECTION ELEVATION",
                subtitle="View: along +Y, horizontal=X long axis, vertical=height",
                scale_note="1:50",
                doc_id="TBS-001 · Assembly Fabrication")

    # ── Save ──────────────────────────────────────────────────────────────────
    out = f"{DIAGRAMS_DIR}/assembly-fab-sheet1.png"
    fig.tight_layout(pad=0)
    plt.savefig(out, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
    plt.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Saved: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — END ELEVATION, CARGO DOOR END  (1:20)
# ═══════════════════════════════════════════════════════════════════════════════

def sheet2():
    """
    View from X=0 short end wall, looking INTO the container (+X direction).
      Horizontal = container width CW = 2362mm  (= optical depth Y direction)
      Vertical   = container height H = 2388mm
      Depth (into page) = container length X = 5893mm

    Drum Ø750mm: vertical axis, centred at CW/2=1181mm, appears as rectangle.
    Equipment at depth in background (dashed outlines).
    """
    X_LO2, X_HI2 = -500, 3100
    Y_LO2, Y_HI2 = -600, 3000

    FIG_W2 = 16.0
    FIG_H2 = FIG_W2 * (Y_HI2-Y_LO2) / (X_HI2-X_LO2)
    DPI = 150

    fig, ax = plt.subplots(figsize=(FIG_W2, FIG_H2), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO2, X_HI2)
    ax.set_ylim(Y_LO2, Y_HI2)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Container walls (cross-section, hatched) ──────────────────────────────
    WALL_T2 = 80
    hatch_rect(ax, -WALL_T2, -WALL_T2, C_WID+2*WALL_T2, WALL_T2, color=C_STEEL, hatch="///")
    hatch_rect(ax, -WALL_T2, C_HGT,    C_WID+2*WALL_T2, WALL_T2, color=C_STEEL, hatch="///")
    hatch_rect(ax, -WALL_T2, -WALL_T2, WALL_T2, C_HGT+2*WALL_T2, color=C_STEEL, hatch="///")
    hatch_rect(ax, C_WID,    -WALL_T2, WALL_T2, C_HGT+2*WALL_T2, color=C_STEEL, hatch="///")

    # ── Interior fill ─────────────────────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle((0, 0), C_WID, C_HGT,
                 facecolor=C_FILL_INT, edgecolor="none", alpha=0.7, zorder=0))

    # ── Container outline ─────────────────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle((0, 0), C_WID, C_HGT,
                 facecolor="none", edgecolor=C_OUT, linewidth=1.6, zorder=5))

    # ── Hinged panel — stepped profile (fills end opening) ──────────────────
    # Corner zones: Yd=0-756 and Yd=1606-2362, 40mm thick
    # Center zone: Yd=756-1606, 120mm thick (drum housing)
    ax.add_patch(mpatches.Rectangle((0, 0), C_WID, C_HGT,
                 facecolor=C_ALUM, edgecolor=C_OUT, linewidth=1.0,
                 alpha=0.30, zorder=3))
    # Step transition lines
    from tbs_constants import PANEL_CORNER_YD_L, PANEL_CORNER_YD_R
    for yd in [PANEL_CORNER_YD_L, PANEL_CORNER_YD_R]:
        ax.plot([yd, yd], [0, C_HGT], color="#C04010", lw=1.0,
                ls=(0, (5, 3)), alpha=0.7, zorder=4)
    ax.text(C_WID*0.12, C_HGT*0.93,
            f"HINGED PANEL (STEPPED)\n{C_WID}x{C_HGT}mm\nCorner: {PANEL_CORNER_T}mm  Center: {PANEL_CENTER_T}mm",
            ha="left", va="top", fontsize=FS_SM, color=C_DIM, zorder=6)

    # ── Revolving drum (vertical axis, centred at CW/2) ───────────────────────
    # In this end elevation: horizontal axis = Y (container width = optical depth).
    # Drum centred at CW/2=1181mm; vertical axis drum Ø750mm appears as rectangle.
    DRUM_LEFT  = DRUM_CY - DRUM_R   # = 1181 - 375 = 806mm
    DRUM_RIGHT = DRUM_CY + DRUM_R   # = 1181 + 375 = 1556mm

    equip_blk(ax, DRUM_LEFT, RAIL_OFF, DRUM_D, DRUM_H_ELV,
              C_LT_DRUM, ec=C_OUT, lw=1.2, alpha=0.80, zorder=6)

    # Drum axis centre line
    draw_cl_v(ax, DRUM_CY, RAIL_OFF, RAIL_OFF+DRUM_H_ELV+150)

    # Baffle slot lines
    for h_baff in [RAIL_OFF+500, RAIL_OFF+1000, RAIL_OFF+1500]:
        ax.plot([DRUM_LEFT+40, DRUM_RIGHT-40], [h_baff, h_baff],
                color=C_OUT, lw=0.6, ls="--", alpha=0.5, zorder=7)

    # Entry threshold bar at floor level
    ax.plot([DRUM_LEFT, DRUM_RIGHT], [RAIL_OFF, RAIL_OFF],
            color=C_OUT, lw=1.5, zorder=7)

    ax.text(DRUM_CY, RAIL_OFF+DRUM_H_ELV/2,
            f"REVOLVING DRUM\nVERTICAL AXIS\nO{DRUM_D}x{DRUM_H_ELV}mm H",
            ha="center", va="center", fontsize=FS_SM-0.5, color=C_OUT,
            style="italic", zorder=7)

    # ── Film plane (dashed inset — behind this view, at X=1100–4649 depth) ────
    # In this end elevation the film plane spans the full container height but
    # only the range Y=0–CW in the horizontal axis here. Indicate with dashed rect.
    ax.add_patch(mpatches.Rectangle((50, 50), C_WID-100, C_HGT-100,
                 facecolor="none", edgecolor=C_CL,
                 linewidth=0.7, linestyle="--", alpha=0.6, zorder=3))
    ax.text(C_WID/2, 30,
            f"Film plane — X={FP_X_L}–{FP_X_R}mm x {C_HGT}mm H  "
            f"(at Yd={FP_Y}mm depth from pinhole wall)",
            ha="center", va="top", fontsize=FS_SM-0.5, color=C_CL,
            style="italic", zorder=6)

    # ── Film-plane rail mounts (4 corners in this end view) ───────────────────
    # Rails run along X (long axis = depth into page). Rail mount positions in
    # the Y (horizontal here) and H (vertical) plane: at Y edges and RAIL_OFF height.
    # The 4 rail slots visible in this view are at (near wall, floor), (near, ceiling),
    # (far wall, floor), (far wall, ceiling) — represented as circles.
    RAIL_Y_NEAR = RAIL_OFF          # floor rail height
    RAIL_Y_FAR  = C_HGT - RAIL_OFF  # ceiling rail height
    for ry_h, ry_v in [(RAIL_OFF, RAIL_Y_NEAR), (C_WID-RAIL_OFF, RAIL_Y_NEAR),
                        (RAIL_OFF, RAIL_Y_FAR),   (C_WID-RAIL_OFF, RAIL_Y_FAR)]:
        ax.add_patch(plt.Circle((ry_h, ry_v), 38,
                     facecolor=C_STEEL, edgecolor=C_OUT, linewidth=0.7, zorder=6))
    ax.text(RAIL_OFF-60, RAIL_Y_NEAR, "Rail", ha="right", va="center",
            fontsize=FS_SM-1, color=C_DIM, zorder=6)

    # ── Evap cooler projection (pinhole wall face, background) ───────────────
    # Rev 4: evap cooler is at Yd=0–350mm (pinhole wall face), X=930–1530mm (depth into page).
    # In this end elevation horizontal axis = Yd → cooler spans Yd=EVAP_Y to EVAP_Y+EVAP_D.
    # Height: 0–800mm. Show as ghost outline.
    ax.add_patch(mpatches.Rectangle((EVAP_Y, RAIL_OFF), EVAP_D, EVAP_H,
                 facecolor=C_EVAP, edgecolor="#1A8A76",
                 linewidth=0.7, linestyle="--", alpha=0.20, zorder=2))
    ax.text(EVAP_Y + EVAP_D/2, RAIL_OFF + EVAP_H/2, "Evap\n(behind)", ha="center", va="center",
            fontsize=FS_SM-2, color="#1A8A76", alpha=0.8, zorder=3)

    # (waste drums eliminated in rev 5 — left zone is light trap only)

    # ── Safelight ─────────────────────────────────────────────────────────────
    ax.plot([100, C_WID-100], [C_HGT-100, C_HGT-100],
            color="#FFD700", lw=2.0, ls="--", dashes=(8, 4), alpha=0.7, zorder=4)
    ax.text(C_WID/2, C_HGT-60, "Safelight strip (Circuit D)",
            ha="center", va="bottom", fontsize=FS_SM-1, color="#B8960A")

    # ── Ventilation — Fan B (exhaust) only: this is the cargo door end wall (X=0) ──
    # Fan A (intake) is on the opposite end wall (X=C_LEN) — not shown in this view.
    # Fan B: far-wall corner (Yd=FAN_B_YD=2287mm), HIGH position (H=FAN_B_H=1800mm).
    FAN_R2 = FAN_DIAM // 2
    ax.add_patch(plt.Circle((FAN_B_YD, FAN_B_H), FAN_R2,
                 facecolor=C_FILL_INT, edgecolor=C_DIM, linewidth=1.0,
                 linestyle="--", zorder=5))
    ax.text(FAN_B_YD, FAN_B_H, "B", ha="center", va="center",
            fontsize=FS_SM-1, color=C_DIM, fontweight="bold", zorder=6)
    ax.text(FAN_B_YD + FAN_R2 + 130, FAN_B_H,
            f"FAN B\nEXHAUST\n(HIGH H={FAN_B_H}mm)\nYd={FAN_B_YD}mm",
            ha="left", va="center", fontsize=FS_SM-1.5, color=C_DIM, zorder=6)

    # ── Dimensions ────────────────────────────────────────────────────────────
    DIM_TOP  = C_HGT + 350
    DIM_LEFT = -330
    DIM_R    = C_WID + 330

    draw_dim_h(ax, 0, C_WID, DIM_TOP, f"Panel / container width  {C_WID}mm",
               offset=107, fs=FS_SM)
    draw_dim_h(ax, DRUM_LEFT, DRUM_RIGHT, -200,
               f"Drum O{DRUM_D}mm", offset=80, fs=FS_SM)
    draw_dim_h(ax, 0, DRUM_CY, DIM_TOP-250,
               f"Drum centre  {DRUM_CY}mm (= CW/2)", offset=80, fs=FS_SM)

    draw_dim_v(ax, DIM_R, 0, C_HGT, f"H={C_HGT}mm", offset=107, fs=FS_SM)
    draw_dim_v(ax, DIM_R+300, RAIL_OFF, RAIL_OFF+DRUM_H_ELV,
               f"Drum H  {DRUM_H_ELV}mm", offset=80, fs=FS_SM)
    draw_dim_v(ax, DIM_LEFT, 0, RAIL_OFF, f"Rail offset\n{RAIL_OFF}mm",
               offset=80, fs=FS_SM)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 2",
                drawing_title="ASSEMBLY — END ELEVATION",
                subtitle="View: from X=0, looking +X into container",
                scale_note="1:20",
                doc_id="TBS-001 · Assembly Fabrication")

    # ── Save ──────────────────────────────────────────────────────────────────
    out = f"{DIAGRAMS_DIR}/assembly-fab-sheet2.png"
    fig.tight_layout(pad=0)
    plt.savefig(out, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
    plt.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Saved: {out}")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sheet1()
    sheet2()
