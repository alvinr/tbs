#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_floorplan_diagram.py  —  TBS-001 Container Floor Plan (redesigned 2026-04-23 rev 2)

Top-down schematic of the full container interior, showing all systems
in their real positions with space constraints respected.

Coordinate system (all mm):
  X = 0 → 5893  (container interior length — long axis)
           X=0: cargo door short end (hinged panel / light trap)
           X=5893: sealed short end
  Y = 0 → 2362  (container interior width = optical axis depth)
           Y=0:    pinhole long wall
           Y=2362: far long wall (image plane / film fabric)

Equipment layout — end-zone design rev 3 (evap cooler to pinhole wall, drums near end wall):
  Left end zone  (X=0–625):    light trap drum + 55-gal drums (stacked, Yd=25–605mm)
  Pinhole wall   (Yd=0 face):  evap cooler (X=700–1300) + electrical panel + pump manifold
  Optical zone   (X=625–4649): film plane rails only — floor clear
  Right end zone (X=4649–5893): IBC tanks only (Y-stacked, right-justified to end wall)

  Every item in the end zones is provably shadow-free at all depths:
    cone left boundary  >= 625mm  at any Y <= 2262  ✓
    cone right boundary <= 4649mm  at any Y <= 2262  ✓
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Arc
from matplotlib.lines import Line2D
import matplotlib.patches

from tbs_constants import *

# ── Palette ───────────────────────────────────────────────────────────────────
BG            = "#FFFFFF"
C_WALL        = "#B0B0B8"
C_RAIL        = "#5A3E00"
C_FILM        = "#2060A0"
C_PINHOLE     = "#CC6600"
C_OPT         = "#2060A0"
C_BLUE_IBC    = "#4A7CB0"
C_BROWN_IBC   = "#8B5E3C"
C_DRUM_EQ     = "#607060"
C_COOLER      = "#40A090"
C_ELEC_COL    = "#806010"
C_PUMP_COL    = "#A04040"
C_ZONE_L      = "#FFF3E8"   # left zone tint
C_ZONE_R      = "#E8F3FF"   # right zone tint
C_ZONE_OPT    = "#F0F8F0"   # optical zone tint
C_DEV_ZONE    = "#F0F0FF"
FONT          = {"fontfamily": "monospace"}

WALL  = 40   # schematic wall thickness

def dim_h(ax, x0, x1, y, label, offset=80, fs=6.5, col=C_DIM):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9, mutation_scale=7))
    ax.text((x0 + x1) / 2, y + offset, label, color=col, fontsize=fs,
            ha="center", va="bottom", **FONT)

def dim_v(ax, x, y0, y1, label, offset=80, fs=6.5, col=C_DIM):
    ax.annotate("", xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9, mutation_scale=7))
    ax.text(x + offset, (y0 + y1) / 2, label, color=col, fontsize=fs,
            ha="left", va="center", **FONT)

def equip_rect(ax, x, y, w, h, col, label, zorder=6, alpha=0.88):
    ax.add_patch(Rectangle((x, y), w, h, fc=col, ec=C_OUT, lw=1.2, alpha=alpha, zorder=zorder))
    ax.text(x + w/2, y + h/2, label, color="#FFFFFF", fontsize=6,
            ha="center", va="center", **FONT, fontweight="bold", zorder=zorder+1)

def penetration(ax, x, y, r=60, col=C_OUT, label="", label_offset=(0, 80)):
    ax.add_patch(Circle((x, y), r, fc="#FFE0A0", ec=col, lw=1.5, zorder=8))
    ax.plot([x-r, x+r], [y, y], color=col, lw=0.8, zorder=9)
    ax.plot([x, x], [y-r, y+r], color=col, lw=0.8, zorder=9)
    if label:
        ax.text(x + label_offset[0], y + label_offset[1], label,
                color=col, fontsize=6, ha="center", va="bottom", **FONT, zorder=9)

def title_block(ax):
    ax.text(0.01, 0.022, "THE BIG SHOEBOX PROJECT  ·  TBS-001",
            transform=ax.transAxes, color=C_DIM, fontsize=7, **FONT)
    ax.text(0.01, 0.010, "CONTAINER FLOOR PLAN — END-ZONE LAYOUT  (TOP-DOWN VIEW)",
            transform=ax.transAxes, color=C_OUT, fontsize=8, fontweight="bold", **FONT)
    ax.text(0.99, 0.022, "SCALE 1:75 (APPROX)  ·  SHEET 1 OF 1",
            transform=ax.transAxes, color=C_DIM, fontsize=7, ha="right", **FONT)
    ax.text(0.99, 0.010, "ALL DIMS IN mm",
            transform=ax.transAxes, color=C_DIM, fontsize=7, ha="right", **FONT)
    ax.text(0.50, 0.002, "© 2026 Alvin Richards — GNU AGPLv3",
            transform=ax.transAxes, color=C_DIM, fontsize=6.0, ha="center",
            style="italic", **FONT)


def floor_plan():
    DEV_DEPTH = 700
    PAD_L = 600; PAD_R = 800; PAD_B = DEV_DEPTH + 200; PAD_T = 500

    X_LO = -PAD_L; X_HI = C_LEN + PAD_R
    Y_LO = -PAD_B; Y_HI = C_WID + PAD_T

    FIG_W = 24.0
    FIG_H = FIG_W * (Y_HI - Y_LO) / (X_HI - X_LO)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=130)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Y_LO, Y_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Zone highlights ───────────────────────────────────────────────────────
    # Left end zone (X=0–ZONE_L_END, all depths)
    ax.add_patch(Rectangle((0, 0), ZONE_L_END, C_WID,
                            fc=C_ZONE_L, ec="none", zorder=1))
    ax.text(ZONE_L_END/1.8, C_WID*0.65,
            f"LEFT END ZONE\nX=0–{ZONE_L_END}mm\n(shadow-free,\nall depths)",
            color="#C07030", fontsize=6.5, ha="center", va="center",
            **FONT, alpha=0.7, fontweight="bold", zorder=2)

    # Optical / film plane zone (X=ZONE_L_END–ZONE_R_START, all depths)
    ax.add_patch(Rectangle((ZONE_L_END, 0), ZONE_R_START - ZONE_L_END, C_WID,
                            fc=C_ZONE_OPT, ec="none", zorder=1))
    ax.text((ZONE_L_END + ZONE_R_START)/2.5, C_WID*0.5,
            f"OPTICAL ZONE  (X={ZONE_L_END}–{ZONE_R_START}mm)\nFILM PLANE RAILS ONLY — FLOOR CLEAR",
            color="#4A8040", fontsize=8, ha="center", va="center",
            **FONT, alpha=0.45, fontweight="bold", zorder=2)

    # Right end zone (X=ZONE_R_START–C_LEN, all depths)
    ax.add_patch(Rectangle((ZONE_R_START, 0), C_LEN - ZONE_R_START, C_WID,
                            fc=C_ZONE_R, ec="none", zorder=1))
    ax.text(ZONE_R_START + (C_LEN - ZONE_R_START)/2, C_WID*0.5,
            f"RIGHT END ZONE\nX={ZONE_R_START}–{C_LEN}mm\n(shadow-free,\nall depths)",
            color="#3060A0", fontsize=6.5, ha="center", va="center",
            **FONT, alpha=0.7, fontweight="bold", zorder=2)

    # Zone boundary lines
    for bx, lbl in [(ZONE_L_END, f"X={ZONE_L_END}"), (ZONE_R_START, f"X={ZONE_R_START}")]:
        ax.plot([bx, bx], [0, C_WID], color=C_DIM, lw=1.2, ls="--", zorder=4, alpha=0.7)
        ax.text(bx, C_WID + 60, lbl, color=C_DIM, fontsize=6.5,
                ha="center", va="bottom", **FONT)

    # ── Optical cone boundary lines (plan view) ───────────────────────────────
    # Left ray: PH_X,0 → FP_X_L,FP_Y
    ax.plot([PH_X, FP_X_L], [0, FP_Y],
            color="#C07000", lw=1.0, ls=(0, (4, 3)), zorder=4, alpha=0.7)
    # Right ray: PH_X,0 → FP_X_R,FP_Y
    ax.plot([PH_X, FP_X_R], [0, FP_Y],
            color="#C07000", lw=1.0, ls=(0, (4, 3)), zorder=4, alpha=0.7)
    ax.text(PH_X - 1220, FP_Y * 0.75, "OPTICAL CONE\n(dashed)",
            color="#C07000", fontsize=6, ha="right", va="center", **FONT, alpha=0.8)

    # ── Container outline ─────────────────────────────────────────────────────
    ax.add_patch(Rectangle((0, 0), C_LEN, C_WID,
                            fc="none", ec=C_OUT, lw=2.5, zorder=3))

    # Container walls
    for patch in [
        (-WALL, -WALL, C_LEN + 2*WALL, WALL),   # pinhole wall
        (-WALL, C_WID, C_LEN + 2*WALL, WALL),   # far wall
        (-WALL, -WALL, WALL, C_WID + 2*WALL),   # left short wall (cargo door)
        (C_LEN, -WALL, WALL, C_WID + 2*WALL),   # right short wall
    ]:
        ax.add_patch(Rectangle((patch[0], patch[1]), patch[2], patch[3],
                                fc=C_WALL, ec=C_OUT, lw=1.5, zorder=3))

    # Wall labels
    ax.text(C_LEN/2, -WALL/2, "PINHOLE WALL  (20ft LONG SIDE)",
            color=C_OUT, fontsize=7, ha="center", va="center", **FONT, zorder=4)
    ax.text(C_LEN/2, C_WID + WALL/2, "FAR WALL — IMAGE PLANE SIDE  (20ft LONG SIDE)",
            color=C_OUT, fontsize=7, ha="center", va="center", **FONT, zorder=4)
    ax.text(-WALL/2, C_WID/2, "CARGO\nDOOR\nEND", color=C_OUT, fontsize=6,
            ha="center", va="center", **FONT, rotation=90, zorder=4)
    ax.text(C_LEN + WALL/2, C_WID/2, "SEALED\nEND", color=C_OUT, fontsize=6,
            ha="center", va="center", **FONT, rotation=90, zorder=4)

    # Structural ribs
    for x_rib in np.arange(200, C_LEN, 600):
        ax.plot([x_rib, x_rib], [0, C_WID], color=C_WALL, lw=0.4, alpha=0.35, zorder=2)

    # ── Film plane rails (floor/ceiling, from RAIL_X_L to RAIL_X_R) ──────────
    RAIL_W = 35
    ax.plot([RAIL_X_L, RAIL_X_R], [FP_Y, FP_Y],
            color=C_RAIL, lw=2.5, zorder=5)
    ax.plot([RAIL_X_L, RAIL_X_L], [FP_Y_MIN, FP_Y + RAIL_W], color=C_RAIL, lw=2.0, zorder=5)
    ax.plot([RAIL_X_R, RAIL_X_R], [FP_Y_MIN, FP_Y + RAIL_W], color=C_RAIL, lw=2.0, zorder=5)
    ax.text(RAIL_X_R + 80, FP_Y, f"FILM PLANE RAILS\n(X={RAIL_X_L}–{RAIL_X_R}mm)",
            color=C_RAIL, fontsize=6.5, ha="left", va="center", **FONT)

    # ── Film fabric / muslin ──────────────────────────────────────────────────
    ax.plot([FP_X_L, FP_X_R], [FP_Y, FP_Y],
            color=C_FILM, lw=4.0, zorder=5, alpha=0.9)
    for hx in np.arange(FP_X_L + 100, FP_X_R, 200):
        ax.plot([hx, hx + 60], [FP_Y, FP_Y], color=C_FILM, lw=1.5, zorder=5, alpha=0.5)
    ax.text(PH_X, FP_Y + 110,
            f"MUSLIN IMAGE PLANE  ({FP_W}×{FP_H}mm)  Y={FP_Y}mm",
            color=C_FILM, fontsize=7, ha="center", va="bottom", **FONT)

    # ── Pinhole ───────────────────────────────────────────────────────────────
    penetration(ax, PH_X, 0, r=80, col=C_PINHOLE,
                label=f"PINHOLE\nX={PH_X}mm\nØ{PH_D}mm",
                label_offset=(0, -250))

    # Optical axis arrow
    ax.annotate("", xy=(PH_X, FP_Y - 40), xytext=(PH_X, 80),
                arrowprops=dict(arrowstyle="->", color=C_OPT, lw=1.5,
                                mutation_scale=10, ls="--"))
    ax.text(PH_X + 80, C_WID/2, f"OPTICAL AXIS\n{C_WID}mm",
            color=C_OPT, fontsize=7, ha="left", va="center", **FONT)

    # ── LEFT END ZONE — equipment ─────────────────────────────────────────────
    # Hinged panel label
    ax.text(-WALL - 350, C_WID/5,
            "HINGED PANEL\n+ REVOLVING\nDRUM INLET",
            color=C_PINHOLE, fontsize=6.5, ha="right", va="center", **FONT, zorder=5)

    # Drum footprint in plan (semicircle inside container)
    DRUM_FP_CY = C_WID / 2   # centred on container Y
    drum_fp = matplotlib.patches.Wedge(
        (0, DRUM_FP_CY), DRUM_R, -90, 90,
        fc="#FFE8D0", ec=C_PINHOLE, lw=1.2, alpha=0.6, zorder=5)
    ax.add_patch(drum_fp)
    ax.text(DRUM_R + 60, DRUM_FP_CY,
            f"DRUM footprint\nØ{DRUM_D}mm",
            color=C_PINHOLE, fontsize=5.5, ha="left", va="center", **FONT, zorder=6)
    penetration(ax, 0, DRUM_FP_CY, r=80,
                col=C_PINHOLE, label="DRUM\nINLET", label_offset=(-200, 0))

    # Evap cooler — on pinhole wall face (Yd=0), X=700–1300mm
    equip_rect(ax, EVAP_X, EVAP_Y, EVAP_W, EVAP_D, C_COOLER,
               f"EVAP\nCOOLER\n{EVAP_W}×{EVAP_D}", zorder=6)
    ax.text(EVAP_X + EVAP_W/2, EVAP_Y + EVAP_D + 55,
            "▲ 800mm tall", color=C_COOLER, fontsize=5.5,
            ha="center", va="bottom", **FONT, zorder=7)

    # Black-water drums — 2× 55-gal, one per Yd corner (unstacked, rev 4)
    for drum_cy, label, ann_dir in [
        (DRUM_LZ_YD, "DRUM D-1\n208L", +1),   # near corner (pinhole wall side)
        (DRUM_FZ_YD, "DRUM D-2\n208L", -1),   # far corner (far wall side)
    ]:
        ax.add_patch(Circle((DRUM_LZ_CX, drum_cy), DRUM_EQ_R,
                            fc=C_DRUM_EQ, ec=C_OUT, lw=1.2, alpha=0.88, zorder=6))
        ax.plot(DRUM_LZ_CX, drum_cy, '+', color="#FFFFFF", ms=6, mew=1.0, zorder=7)
        ax.text(DRUM_LZ_CX, drum_cy,
                label, color="#FFFFFF", fontsize=5.5, ha="center", va="center",
                **FONT, fontweight="bold", zorder=7)
        ax.text(DRUM_LZ_CX, drum_cy + ann_dir * (DRUM_EQ_R + 55),
                f"▲ {DRUM_EQ_H}mm H", color=C_DRUM_EQ, fontsize=5.5,
                ha="center", va="bottom" if ann_dir > 0 else "top", **FONT, zorder=7)

    # ── PINHOLE WALL (Y=0 face) — wall-mounted items ──────────────────────────
    # Electrical panel + battery (thin strip at Y=0)
    equip_rect(ax, EP_X, 0, EP_W, 80, C_ELEC_COL,
               "ELEC+\nBATT.", zorder=7, alpha=0.95)
    # Pump manifold
    equip_rect(ax, PUMP_X, 0, PUMP_W, 80, C_PUMP_COL,
               "PUMP\nMFD.", zorder=7, alpha=0.95)

    # ── RIGHT END ZONE — fluid tanks ──────────────────────────────────────────
    # IBC column — Y-stacked: Blue IBCs (front) then Brown IBC (rear)
    equip_rect(ax, IBC_COL_X, BLUE_IBC_Y, IBC_W, IBC_D, C_BLUE_IBC,
               f"BLUE IBC ×2\n(STACKED)\n2×600L\nY={BLUE_IBC_Y}–{BLUE_IBC_Y+IBC_D}",
               zorder=6)
    ax.text(IBC_COL_X + IBC_W/2, BLUE_IBC_Y + IBC_D + 55,
            "▲ 2020mm tall", color=C_BLUE_IBC, fontsize=5.5,
            ha="center", va="bottom", **FONT, zorder=7)

    equip_rect(ax, IBC_COL_X, BROWN_IBC_Y, IBC_W, IBC_D, C_BROWN_IBC,
               f"BROWN IBC ×1\n600L\nY={BROWN_IBC_Y}–{BROWN_IBC_Y+IBC_D}",
               zorder=6)
    ax.text(IBC_COL_X + IBC_W/2, BROWN_IBC_Y + IBC_D + 55,
            "▲ 1010mm tall", color=C_BROWN_IBC, fontsize=5.5,
            ha="center", va="bottom", **FONT, zorder=7)

    # (drums relocated to left end zone — no drum column in right zone)

    # ── Wall penetrations ─────────────────────────────────────────────────────
    # Fan A — INTAKE: far end wall (X=C_LEN), near-wall corner (Yd=FAN_A_YD=75mm), LOW (H=600mm)
    penetration(ax, C_LEN, FAN_A_YD, r=55, col=C_DIM, label="FAN\nIN", label_offset=(140, 0))
    # Fan B — EXHAUST: cargo door end wall (X=0), far-wall corner (Yd=FAN_B_YD=2287mm), HIGH (H=1800mm)
    penetration(ax, 0, FAN_B_YD, r=55, col=C_DIM, label="FAN\nOUT", label_offset=(-140, 0))

    # ── Hinged panel swing arc ────────────────────────────────────────────────
    ax.add_patch(Rectangle((-WALL - 200, 0), 120, C_WID,
                            fc="none", ec=C_DIM, lw=1.0, ls=(0, (6, 4)),
                            zorder=4, alpha=0.5))
    ax.text(-WALL - 80, C_WID/2, "PANEL\n(OPEN)",
            color=C_DIM, fontsize=6, ha="center", va="center",
            **FONT, rotation=90, alpha=0.5, zorder=5)
    swing_arc = Arc((-WALL, C_WID/2), 2*320, 2*320,
                    angle=0, theta1=180, theta2=360,
                    color=C_DIM, lw=0.9, ls=(0, (4, 3)), zorder=4, alpha=0.5)
    ax.add_patch(swing_arc)

    # ── Development area (outside) ────────────────────────────────────────────
    DEV_X0 = FP_X_L; DEV_X1 = FP_X_R
    DEV_Y0 = -DEV_DEPTH; DEV_Y1 = -WALL - 60
    ax.add_patch(Rectangle((DEV_X0, DEV_Y0), DEV_X1 - DEV_X0, DEV_Y1 - DEV_Y0,
                            fc=C_DEV_ZONE, ec=C_DIM, lw=1.5, ls=(0, (5, 3)), zorder=2))
    for hx in np.arange(DEV_X0, DEV_X1, 250):
        ax.plot([hx, hx+200], [DEV_Y0, DEV_Y1], color=C_DIM, lw=0.4, alpha=0.3, zorder=3)
    ax.text((DEV_X0+DEV_X1)/2, (DEV_Y0+DEV_Y1)/2,
            "DEVELOPMENT AREA  (OUTSIDE — IN FRONT OF PINHOLE WALL)\n"
            "Fabric lowered from image plane for water wash.",
            color=C_DIM, fontsize=7, ha="center", va="center", **FONT, zorder=4)
    ax.annotate("", xy=(PH_X, DEV_Y1+10), xytext=(PH_X, 0),
                arrowprops=dict(arrowstyle="->", color=C_DIM, lw=1.0,
                                mutation_scale=8, ls="--", alpha=0.7))

    # ── Dimension annotations ─────────────────────────────────────────────────
    dim_h(ax, 0, C_LEN, C_WID + 300, f"{C_LEN}mm  ({C_LEN/304.8:.1f}ft)  INTERIOR LENGTH")
    dim_v(ax, C_LEN + 200, 0, C_WID,
          f"{C_WID}mm\nINTERIOR\nWIDTH\n(=FOCAL\nLENGTH)", offset=55)
    dim_h(ax, 0, ZONE_L_END, -PAD_B + 200, f"{ZONE_L_END}mm\nLEFT ZONE", offset=40, fs=6)
    dim_h(ax, ZONE_L_END, ZONE_R_START, -PAD_B + 200, f"{ZONE_R_START-ZONE_L_END}mm\nOPTICAL ZONE", offset=40, fs=6)
    dim_h(ax, ZONE_R_START, C_LEN, -PAD_B + 200, f"{C_LEN-ZONE_R_START}mm\nRIGHT ZONE", offset=40, fs=6)
    dim_h(ax, FP_X_L, FP_X_R, -PAD_B + 400, f"{FP_W}mm  FILM PLANE WIDTH", offset=40, fs=6)
    dim_v(ax, -PAD_L + 100, 0, FP_Y, f"Y={FP_Y}mm\nFILM PLANE\nDEPTH", offset=55, fs=6)

    # ── Shadow-free proof callout ─────────────────────────────────────────────
    proof_x = C_LEN/2
    proof_y = -DEV_DEPTH + 80
    ax.text(proof_x, proof_y - 300,
            f"SHADOW-FREE PROOF:  cone left ≥ {FP_X_L}mm at all Y  ✓     "
            f"cone right ≤ {FP_X_R}mm at all Y  ✓     "
            "pinhole wall Y=0: outside cone ✓",
            color="#204020", fontsize=6.5, ha="center", va="bottom",
            **FONT, style="italic",
            bbox=dict(boxstyle="round,pad=0.3", fc="#E8F8E8", ec="#408040", lw=0.8),
            zorder=10)

    # ── Legend ────────────────────────────────────────────────────────────────
    LEG_X = C_LEN + 90; LEG_Y_TOP = C_WID - 2500
    legend_items = [
        (C_BLUE_IBC,  "Blue IBC ×2 stacked (2×600L)"),
        (C_BROWN_IBC, "Brown IBC ×1 (600L)"),
        (C_DRUM_EQ,   "55-gal HDPE drums ×2"),
        (C_COOLER,    "Evaporative cooler"),
        (C_ELEC_COL,  "Electrical panel + battery bank"),
        (C_PUMP_COL,  "Pump manifold"),
        (C_FILM,      f"Muslin image plane ({FP_W}×{FP_H}mm)"),
        (C_PINHOLE,   f"Pinhole Ø{PH_D}mm"),
        (C_OPT,       "Optical axis (2362mm focal length)"),
        (C_PINHOLE,   "Revolving light-trap drum"),
        (C_DEV_ZONE,  "Development area (outside container)"),
    ]
    box_w = 780; box_h = len(legend_items) * 52 + 40  # box_w fixed: sized to contain text, not tied to PAD_R
    ax.add_patch(Rectangle((LEG_X - 70, LEG_Y_TOP - box_h), box_w, box_h,
                            fc="#FAFAFA", ec=C_DIM, lw=0.8, zorder=8))
    ax.text(LEG_X + box_w/2, LEG_Y_TOP - 12, "LEGEND",
            color=C_OUT, fontsize=7.5, ha="center", va="center",
            fontweight="bold", **FONT, zorder=9)
    for i, (col, txt) in enumerate(legend_items):
        iy = LEG_Y_TOP - 50 - i * 52
        ax.add_patch(Rectangle((LEG_X + 12, iy - 16), 36, 32,
                                fc=col, ec=C_OUT, lw=0.8, zorder=9, alpha=0.9))
        ax.text(LEG_X + 58, iy, txt, color=C_DIM, fontsize=6,
                ha="left", va="center", **FONT, zorder=9)

    title_block(ax)

    import os; os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    out = f"{DIAGRAMS_DIR}/container-floorplan.png"
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(str(out).replace(".png", ".svg"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  {out} saved")


if __name__ == "__main__":
    print("Generating container floor plan...")
    floor_plan()
    print("Done.")
