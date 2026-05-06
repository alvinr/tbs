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
  Pinhole wall   (Yd=0 face):  evap cooler (X=930–1530) + electrical panel + pump manifold
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
    tick = abs(offset) * 0.3
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9, mutation_scale=7))
    ax.plot([x0, x0], [y - tick, y + tick], color=col, lw=0.6)
    ax.plot([x1, x1], [y - tick, y + tick], color=col, lw=0.6)
    ax.text((x0 + x1) / 2, y + offset, label, color=col, fontsize=fs,
            ha="center", va="bottom", **FONT)

def dim_v(ax, x, y0, y1, label, offset=80, fs=6.5, col=C_DIM):
    tick = abs(offset) * 0.3
    ax.annotate("", xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9, mutation_scale=7))
    ax.plot([x - tick, x + tick], [y0, y0], color=col, lw=0.6)
    ax.plot([x - tick, x + tick], [y1, y1], color=col, lw=0.6)
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
    ax.text(ZONE_L_END/1.8, C_WID*1.06,
            f"LEFT END ZONE\nX=0–{ZONE_L_END}mm\n(shadow-free,\nall depths)",
            color="#C07030", fontsize=6.5, ha="center", va="center",
            **FONT, alpha=0.7, fontweight="bold", zorder=2)

    # Optical / film plane zone (X=ZONE_L_END–ZONE_R_START, all depths)
    ax.add_patch(Rectangle((ZONE_L_END, 0), ZONE_R_START - ZONE_L_END, C_WID,
                            fc=C_ZONE_OPT, ec="none", zorder=1))
    ax.text((ZONE_L_END + ZONE_R_START)/2, C_WID*1.06,
            f"OPTICAL ZONE  (X={ZONE_L_END}–{ZONE_R_START}mm)\nFILM PLANE RAILS ONLY — FLOOR CLEAR",
            color="#4A8040", fontsize=8, ha="center", va="center",
            **FONT, alpha=0.45, fontweight="bold", zorder=2)

    # Right end zone (X=ZONE_R_START–C_LEN, all depths)
    ax.add_patch(Rectangle((ZONE_R_START, 0), C_LEN - ZONE_R_START, C_WID,
                            fc=C_ZONE_R, ec="none", zorder=1))
    ax.text(ZONE_R_START + (C_LEN - ZONE_R_START)/2, C_WID*1.06,
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
    ax.text(PH_X, FP_Y + 30,
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

    # Evap cooler — on pinhole wall face (Yd=0), X=930–1530mm
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

    # ── V-groove dolly tracks (drum slide rails) ───────────────────────────────
    C_TRACK   = "#8B7355"    # permanent track color (brown)
    C_BRIDGE  = "#4A90D9"    # bridge section color (blue)
    TRACK_W   = 8            # track visual width in plan
    for drum_yd in [DRUM_LZ_YD, DRUM_FZ_YD]:
        for offset in [-80, 80]:  # two parallel tracks per drum
            ty = drum_yd + offset
            # Permanent section (X = PANEL_CORNER_T to PERM_TRACK_END)
            ax.add_patch(Rectangle(
                (PANEL_CORNER_T, ty - TRACK_W/2), PERM_TRACK_END - PANEL_CORNER_T, TRACK_W,
                facecolor=C_TRACK, edgecolor=C_OUT, linewidth=0.3,
                alpha=0.5, zorder=4))
            # Bridge section (X = BRIDGE_TRACK_START to BRIDGE_TRACK_END) — dashed
            ax.add_patch(Rectangle(
                (BRIDGE_TRACK_START, ty - TRACK_W/2), BRIDGE_TRACK_END - BRIDGE_TRACK_START, TRACK_W,
                facecolor=C_BRIDGE, edgecolor=C_OUT, linewidth=0.3,
                alpha=0.45, zorder=4, linestyle="--"))
    # Track label
    ax.text(PERM_TRACK_END / 2, DRUM_LZ_YD + DRUM_EQ_R + 120,
            f"V-GROOVE DOLLY TRACKS\n(perm X={PANEL_CORNER_T}–{PERM_TRACK_END}, "
            f"bridge X={BRIDGE_TRACK_START}–{BRIDGE_TRACK_END})",
            color=C_TRACK, fontsize=5, ha="center", va="bottom", **FONT, zorder=7)

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

    # ── Hinged panel swing arc (stepped profile visible in plan) ────────────
    # Open position: panel swings outward 180° on left-edge hinges.
    # Show stepped outline: 40mm corners, 120mm center.
    # Corner zones (Yd=0-756 and Yd=1606-2362)
    ax.add_patch(Rectangle((-WALL - 200, 0), PANEL_CORNER_T, PANEL_CORNER_YD_L,
                            fc="none", ec=C_DIM, lw=1.0, ls=(0, (6, 4)),
                            zorder=4, alpha=0.5))
    ax.add_patch(Rectangle((-WALL - 200, PANEL_CORNER_YD_R), PANEL_CORNER_T,
                            C_WID - PANEL_CORNER_YD_R,
                            fc="none", ec=C_DIM, lw=1.0, ls=(0, (6, 4)),
                            zorder=4, alpha=0.5))
    # Center zone (Yd=756-1606)
    ax.add_patch(Rectangle((-WALL - 200, PANEL_CORNER_YD_L), PANEL_CENTER_T,
                            PANEL_CORNER_YD_R - PANEL_CORNER_YD_L,
                            fc="none", ec=C_DIM, lw=1.0, ls=(0, (6, 4)),
                            zorder=4, alpha=0.5))
    ax.text(-WALL - 80, C_WID/2, "PANEL\n(OPEN)\nSTEPPED",
            color=C_DIM, fontsize=5.5, ha="center", va="center",
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
    ax.text((DEV_X0+DEV_X1)/2, (DEV_Y0+DEV_Y1)/2+50,
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
    dim_h(ax, 0, ZONE_L_END, -PAD_B + 150, f"{ZONE_L_END}mm\nLEFT ZONE", offset=60, fs=6)
    dim_h(ax, ZONE_L_END, ZONE_R_START, -PAD_B + 150, f"{ZONE_R_START-ZONE_L_END}mm\nOPTICAL ZONE", offset=60, fs=6)
    dim_h(ax, ZONE_R_START, C_LEN, -PAD_B + 150, f"{C_LEN-ZONE_R_START}mm\nRIGHT ZONE", offset=40, fs=6)
    dim_h(ax, FP_X_L, FP_X_R, -PAD_B + 400, f"{FP_W}mm  FILM PLANE WIDTH", offset=60, fs=6)
    dim_v(ax, PAD_L + 100, 0, FP_Y+100, f"Y={FP_Y}mm\nFILM PLANE\nDEPTH", offset=25, fs=6)

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
    LEG_X = C_LEN + 110; LEG_Y_TOP = C_WID - 2410
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
        ("#8B7355",   "V-groove dolly track (permanent)"),
        ("#4A90D9",   "V-groove bridge section (removable)"),
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

    # ── Egress path annotation ─────────────────────────────────────────────────
    # When panel opens 180°, the light trap drum swings out with it.
    # Clear passage between the two waste drums: Yd=580–1782 = 1202mm.
    EGRESS_GAP_LO = DRUM_LZ_YD_HI     # 580mm
    EGRESS_GAP_HI = DRUM_FZ_YD_LO     # 1782mm
    EGRESS_GAP    = EGRESS_GAP_HI - EGRESS_GAP_LO  # 1202mm
    EGRESS_MID_Y  = (EGRESS_GAP_LO + EGRESS_GAP_HI) / 2
    EGRESS_ARROW_X = DRUM_LZ_CX       # 330mm — center of drum zone

    # Dashed green arrow showing egress direction (interior → door)
    ax.annotate("", xy=(-WALL - 60, EGRESS_MID_Y),
                xytext=(ZONE_L_END - 60, EGRESS_MID_Y),
                arrowprops=dict(arrowstyle="->", color="#20A020", lw=2.0,
                                linestyle=":", mutation_scale=12),
                zorder=10)
    ax.text(EGRESS_ARROW_X, EGRESS_MID_Y + 60,
            f"EGRESS PATH — {EGRESS_GAP}mm CLEAR",
            color="#20A020", fontsize=6.5, ha="center", va="bottom",
            fontweight="bold", **FONT, zorder=10)
    ax.text(EGRESS_ARROW_X, EGRESS_MID_Y - 60,
            "(panel open 180°, drum swings out)",
            color="#20A020", fontsize=5.5, ha="center", va="top",
            **FONT, alpha=0.8, zorder=10)

    # Dimension line showing 1202mm gap between drums
    dim_v(ax, -180, EGRESS_GAP_LO, EGRESS_GAP_HI,
          f"{EGRESS_GAP}mm\nEGRESS\nGAP", offset=-180, fs=6, col="#20A020")

    title_block(ax)

    import os; os.makedirs(DIAGRAMS_DIR, exist_ok=True); os.makedirs(SVG_DIR, exist_ok=True)
    out = f"{DIAGRAMS_DIR}/container-floorplan.png"
    fig.savefig(out, dpi=130, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  {out} saved")


def egress_detail():
    """Sheet 2 — Cargo door end egress detail.

    Zoomed plan view of X=-500 to X=1200, full Yd width.
    Shows:
      • Panel swung 180° inward (into container)
      • Waste drums slid to transport position (305mm inward)
      • Egress paths with clearance dimensions
    """
    # ── Layout constants ─────────────────────────────────────────────────────
    PAD = 350
    X_LO, X_HI = -500, 1400
    Y_LO, Y_HI = -PAD, C_WID + PAD
    FIG_W = 18.0
    FIG_H = FIG_W * (Y_HI - Y_LO) / (X_HI - X_LO)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Y_LO, Y_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    C_EGRESS = "#20A020"
    C_GHOST  = "#9090C0"

    # ── Zone tints ───────────────────────────────────────────────────────────
    ax.add_patch(Rectangle((0, 0), ZONE_L_END, C_WID,
                            fc=C_ZONE_L, ec="none", zorder=1))
    ax.add_patch(Rectangle((ZONE_L_END, 0), X_HI - ZONE_L_END, C_WID,
                            fc=C_ZONE_OPT, ec="none", zorder=1))
    ax.plot([ZONE_L_END, ZONE_L_END], [0, C_WID],
            color=C_DIM, lw=1.0, ls="--", zorder=3, alpha=0.5)
    ax.text(ZONE_L_END, C_WID + 60, f"X={ZONE_L_END}",
            color=C_DIM, fontsize=7, ha="center", va="bottom", **FONT)

    # ── Container walls ──────────────────────────────────────────────────────
    # Interior outline (partial — only the visible portion)
    ax.plot([0, X_HI], [0, 0], color=C_OUT, lw=2.5, zorder=3)       # pinhole wall
    ax.plot([0, X_HI], [C_WID, C_WID], color=C_OUT, lw=2.5, zorder=3)  # far wall
    ax.plot([0, 0], [0, C_WID], color=C_OUT, lw=2.0, zorder=3)      # cargo door face

    # Wall thickness hatching
    for patch in [
        (0, -WALL, X_HI, WALL),          # pinhole wall
        (0, C_WID, X_HI, WALL),          # far wall
        (-WALL, -WALL, WALL, C_WID + 2*WALL),  # left short wall
    ]:
        ax.add_patch(Rectangle((patch[0], patch[1]), patch[2], patch[3],
                                fc=C_WALL, ec=C_OUT, lw=1.2, zorder=3))

    ax.text(-WALL/2, C_WID/2, "CARGO\nDOOR\nEND",
            color=C_OUT, fontsize=7, ha="center", va="center",
            **FONT, rotation=90, zorder=4)
    ax.text(X_HI/2, -WALL/2, "PINHOLE WALL",
            color=C_OUT, fontsize=6.5, ha="center", va="center", **FONT, zorder=4)
    ax.text(X_HI/2, C_WID + WALL/2, "FAR WALL",
            color=C_OUT, fontsize=6.5, ha="center", va="center", **FONT, zorder=4)

    # ── Door frame opening ───────────────────────────────────────────────────
    FRAME = 50  # 50×50mm RHS fixed frame
    ax.add_patch(Rectangle((0, 0), FRAME, FRAME,
                            fc=C_WALL, ec=C_OUT, lw=0.8, zorder=5))
    ax.add_patch(Rectangle((0, C_WID - FRAME), FRAME, FRAME,
                            fc=C_WALL, ec=C_OUT, lw=0.8, zorder=5))

    # ── Drums in TRANSPORT position (slid 305mm inward) ──────────────────────
    DRUM_TX = DRUM_LZ_CX + DRUM_SLIDE   # 330 + 305 = 635mm
    drum_left_x  = DRUM_TX - DRUM_EQ_R   # 345mm
    drum_right_x = DRUM_TX + DRUM_EQ_R   # 925mm

    for drum_cy, label in [
        (DRUM_LZ_YD, "D-1\n(SLID)"),
        (DRUM_FZ_YD, "D-2\n(SLID)"),
    ]:
        ax.add_patch(Circle((DRUM_TX, drum_cy), DRUM_EQ_R,
                            fc=C_DRUM_EQ, ec=C_OUT, lw=1.5, alpha=0.7, zorder=6))
        ax.text(DRUM_TX, drum_cy, label, color="#FFFFFF", fontsize=7,
                ha="center", va="center", fontweight="bold", **FONT, zorder=7)

    # Ghost outlines: drums in operational position
    for drum_cy in [DRUM_LZ_YD, DRUM_FZ_YD]:
        ax.add_patch(Circle((DRUM_LZ_CX, drum_cy), DRUM_EQ_R,
                            fc="none", ec=C_GHOST, lw=1.2, ls=(0, (4, 3)),
                            alpha=0.5, zorder=4))
    ax.text(DRUM_LZ_CX, DRUM_LZ_YD + DRUM_EQ_R + 50,
            "operational\nposition", color=C_GHOST, fontsize=5.5,
            ha="center", va="bottom", **FONT, alpha=0.6, zorder=5)

    # Slide arrows (operational → transport)
    for drum_cy in [DRUM_LZ_YD, DRUM_FZ_YD]:
        ax.annotate("", xy=(DRUM_TX, drum_cy),
                    xytext=(DRUM_LZ_CX, drum_cy),
                    arrowprops=dict(arrowstyle="->", color=C_GHOST, lw=1.2,
                                    linestyle=":", mutation_scale=10),
                    zorder=5)
    ax.text((DRUM_LZ_CX + DRUM_TX)/2, DRUM_FZ_YD - DRUM_EQ_R - 50,
            f"SLIDE {DRUM_SLIDE}mm",
            color=C_GHOST, fontsize=6, ha="center", va="top",
            fontweight="bold", **FONT, zorder=5)

    # ── V-groove dolly tracks ────────────────────────────────────────────────
    C_TRACK  = "#8B7355"
    C_BRIDGE = "#4A90D9"
    TRACK_W  = 10
    for drum_yd in [DRUM_LZ_YD, DRUM_FZ_YD]:
        for offset in [-80, 80]:
            ty = drum_yd + offset
            ax.add_patch(Rectangle(
                (PANEL_CORNER_T, ty - TRACK_W/2),
                PERM_TRACK_END - PANEL_CORNER_T, TRACK_W,
                fc=C_TRACK, ec=C_OUT, lw=0.3, alpha=0.4, zorder=4))
            ax.add_patch(Rectangle(
                (BRIDGE_TRACK_START, ty - TRACK_W/2),
                BRIDGE_TRACK_END - BRIDGE_TRACK_START, TRACK_W,
                fc=C_BRIDGE, ec=C_OUT, lw=0.3, alpha=0.35,
                zorder=4, linestyle="--"))

    # ── Panel swung 180° INWARD ──────────────────────────────────────────────
    # Hinge axis at X=0, Yd=0 (pinhole wall corner). Panel swings INTO container.
    # At 180° inward, the panel lies along the pinhole wall (Yd=0) interior face,
    # extending from X=0 in the +X direction.
    #
    # Corner zones: 40mm thick → extend to Yd = PANEL_CORNER_T = 40mm
    # Center zone:  120mm thick → extend to Yd = PANEL_CENTER_T = 120mm
    # Panel width (= C_WID = 2362mm) now lies along X axis.

    # Stepped panel outline (open 180° inward — lies along pinhole wall)
    # Near corner zone: was Yd=0–756, now X=0–756, depth=40mm into Yd
    ax.add_patch(Rectangle((0, 0), PANEL_CORNER_YD_L, PANEL_CORNER_T,
                            fc="#E0D0C0", ec=C_PINHOLE, lw=1.5,
                            alpha=0.55, zorder=5))
    # Center zone: was Yd=756–1606, now X=756–1606, depth=120mm into Yd
    ax.add_patch(Rectangle((PANEL_CORNER_YD_L, 0), PANEL_CENTER_W, PANEL_CENTER_T,
                            fc="#E0D0C0", ec=C_PINHOLE, lw=1.5,
                            alpha=0.55, zorder=5))
    # Far corner zone: was Yd=1606–2362, now X=1606–2362, depth=40mm into Yd
    ax.add_patch(Rectangle((PANEL_CORNER_YD_R, 0), C_WID - PANEL_CORNER_YD_R, PANEL_CORNER_T,
                            fc="#E0D0C0", ec=C_PINHOLE, lw=1.5,
                            alpha=0.55, zorder=5))

    # Light trap drum in open panel — center zone, now at X=1181, Yd=DRUM_R
    DRUM_OPEN_CX = (PANEL_CORNER_YD_L + PANEL_CORNER_YD_R) / 2  # 1181mm
    ax.add_patch(Circle((DRUM_OPEN_CX, 0), DRUM_R,
                         fc="#FFE8D0", ec=C_PINHOLE, lw=1.2, alpha=0.5,
                         zorder=5, clip_on=True))
    ax.text(DRUM_OPEN_CX, PANEL_CENTER_T + 30,
            f"LIGHT TRAP DRUM\n(in open panel)\nØ{DRUM_D}mm",
            color=C_PINHOLE, fontsize=6, ha="center", va="bottom",
            **FONT, zorder=8)

    # Hinge pin marker
    ax.plot(0, 0, "o", color=C_PINHOLE, ms=8, zorder=8)
    ax.text(-30, -60, "HINGE\nPIN", color=C_PINHOLE, fontsize=5.5,
            ha="center", va="top", fontweight="bold", **FONT, zorder=8)

    # Swing arc (90° from closed to open)
    swing_r = C_WID * 0.35  # representative arc radius
    swing_arc = Arc((0, 0), 2*swing_r, 2*swing_r,
                    angle=0, theta1=0, theta2=90,
                    color=C_PINHOLE, lw=1.0, ls=(0, (4, 3)),
                    zorder=4, alpha=0.5)
    ax.add_patch(swing_arc)
    ax.annotate("", xy=(swing_r * 0.25, swing_r * 0.97),
                xytext=(swing_r * 0.05, swing_r * 1.02),
                arrowprops=dict(arrowstyle="->", color=C_PINHOLE, lw=1.0,
                                mutation_scale=8), zorder=5)
    ax.text(swing_r * 0.55, swing_r * 0.85, "180° INWARD\nSWING",
            color=C_PINHOLE, fontsize=6, ha="center", va="center",
            **FONT, alpha=0.7, zorder=5)

    # Ghost outline of panel in CLOSED position (at X=0, across full Yd width)
    # Corner zones
    ax.add_patch(Rectangle((0, 0), PANEL_CORNER_T, PANEL_CORNER_YD_L,
                            fc="none", ec=C_GHOST, lw=1.0, ls=(0, (4, 3)),
                            alpha=0.4, zorder=4))
    ax.add_patch(Rectangle((0, PANEL_CORNER_YD_R), PANEL_CORNER_T,
                            C_WID - PANEL_CORNER_YD_R,
                            fc="none", ec=C_GHOST, lw=1.0, ls=(0, (4, 3)),
                            alpha=0.4, zorder=4))
    # Center zone
    ax.add_patch(Rectangle((0, PANEL_CORNER_YD_L), PANEL_CENTER_T, PANEL_CENTER_W,
                            fc="none", ec=C_GHOST, lw=1.0, ls=(0, (4, 3)),
                            alpha=0.4, zorder=4))
    ax.text(PANEL_CENTER_T + 30, C_WID/2, "CLOSED\nPOSITION",
            color=C_GHOST, fontsize=5.5, ha="left", va="center",
            **FONT, alpha=0.5, zorder=5, rotation=90)

    # ── Fan B penetration ────────────────────────────────────────────────────
    penetration(ax, 0, FAN_B_YD, r=55, col=C_DIM,
                label="FAN B\n(EXHAUST)", label_offset=(-140, 0))

    # ── Evap cooler (just visible at right edge of view) ─────────────────────
    evap_vis_w = min(EVAP_W, X_HI - EVAP_X)
    if evap_vis_w > 0:
        equip_rect(ax, EVAP_X, EVAP_Y, evap_vis_w, EVAP_D, C_COOLER,
                   "EVAP\nCOOLER", zorder=6)

    # ── EGRESS PATHS ─────────────────────────────────────────────────────────
    # With panel open inward and drums slid back, three egress paths exist:
    # Path 1: Between drum D-1 and the open panel (Yd = 40mm to 345mm)
    # Path 2: Between the two drums (Yd = 580+305=885 to 1782+305=2087 → gap = 1202mm)
    # Path 3: Between drum D-2 and far wall (Yd = 2087+580=2652 → clipped at far wall)

    # The drums have slid 305mm in X, but their Yd positions are unchanged.
    # Key egress path is between the two drums: Yd = 580 to 1782 = 1202mm clear.

    EGRESS_GAP_LO = DRUM_LZ_YD_HI   # 580mm
    EGRESS_GAP_HI = DRUM_FZ_YD_LO   # 1782mm
    EGRESS_GAP    = EGRESS_GAP_HI - EGRESS_GAP_LO  # 1202mm
    EGRESS_MID_Y  = (EGRESS_GAP_LO + EGRESS_GAP_HI) / 2

    # Primary egress arrow (between drums, through door)
    ax.annotate("", xy=(-WALL - 30, EGRESS_MID_Y),
                xytext=(drum_right_x + 80, EGRESS_MID_Y),
                arrowprops=dict(arrowstyle="->", color=C_EGRESS, lw=2.5,
                                linestyle=":", mutation_scale=14),
                zorder=10)
    ax.text((drum_right_x + 80) / 2, EGRESS_MID_Y + 55,
            f"PRIMARY EGRESS — {EGRESS_GAP}mm CLEAR",
            color=C_EGRESS, fontsize=8, ha="center", va="bottom",
            fontweight="bold", **FONT, zorder=10)

    # Secondary egress arrows (between each drum and wall)
    # Near side: between pinhole wall and drum D-1 near edge
    near_gap_lo = PANEL_CORNER_T  # 40mm (panel corner inner face, when panel is open this is clear)
    # When panel is open inward, the near wall at Yd=0 is clear above the panel.
    # But the open panel lies along Yd=0–40mm. Egress at Yd=0 corner is blocked by open panel.
    # Far side: between drum D-2 far edge and far wall
    far_gap = C_WID - DRUM_FZ_YD_HI  # 2362 - 2362 = 0mm (drum flush with wall)
    # So there's no secondary egress on far side.

    # The only clear secondary path is above the open panel's corner zone (40mm thick)
    # at Yd=40 to Yd=DRUM_LZ_YD_LO (=0). Since drum D-1 is flush with pinhole wall,
    # there's no gap on that side either.

    # ── Egress dimension line ────────────────────────────────────────────────
    dim_v(ax, -220, EGRESS_GAP_LO, EGRESS_GAP_HI,
          f"{EGRESS_GAP}mm\nEGRESS\nGAP", offset=-200, fs=7, col=C_EGRESS)

    # ── Drum transport position dimension ────────────────────────────────────
    dim_h(ax, drum_left_x, drum_right_x, C_WID + 200,
          f"DRUM Ø{DRUM_EQ_D}mm\n(transport X={drum_left_x}–{drum_right_x})",
          offset=80, fs=6)

    # ── Panel dimension along X when open ────────────────────────────────────
    dim_h(ax, 0, C_WID, -PAD + 60,
          f"PANEL {C_WID}mm (open inward along pinhole wall)",
          offset=60, fs=6, col=C_PINHOLE)

    # ── Clearance note ───────────────────────────────────────────────────────
    note_x = (ZONE_L_END + X_HI) / 2
    note_y = C_WID * 0.55
    ax.text(note_x, note_y,
            "EGRESS CLEARANCE SUMMARY\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Gap between drums (Yd):  {EGRESS_GAP}mm (47.3\")\n"
            f"Avg. male shoulder width:  460mm (18\")\n"
            f"Emergency egress min:  610mm (24\")\n"
            f"Standard doorway min:  762mm (30\")\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Margin over emergency min:  {EGRESS_GAP - 610}mm\n"
            "Face-forward egress: YES",
            color=C_OUT, fontsize=7, ha="center", va="center",
            **FONT, zorder=10,
            bbox=dict(boxstyle="round,pad=0.5", fc="#F0FFF0",
                      ec=C_EGRESS, lw=1.2))

    # ── Title block ──────────────────────────────────────────────────────────
    ax.text(0.01, 0.022, "THE BIG SHOEBOX PROJECT  ·  TBS-001",
            transform=ax.transAxes, color=C_DIM, fontsize=7, **FONT)
    ax.text(0.01, 0.010, "CARGO DOOR EGRESS DETAIL — PANEL OPEN 180° INWARD, DRUMS SLID TO TRANSPORT",
            transform=ax.transAxes, color=C_OUT, fontsize=8, fontweight="bold", **FONT)
    ax.text(0.99, 0.022, "SCALE ~1:20  ·  SHEET 2 OF 2",
            transform=ax.transAxes, color=C_DIM, fontsize=7, ha="right", **FONT)
    ax.text(0.99, 0.010, "ALL DIMS IN mm",
            transform=ax.transAxes, color=C_DIM, fontsize=7, ha="right", **FONT)
    ax.text(0.50, 0.002, "© 2026 Alvin Richards — GNU AGPLv3",
            transform=ax.transAxes, color=C_DIM, fontsize=6.0, ha="center",
            style="italic", **FONT)

    import os; os.makedirs(DIAGRAMS_DIR, exist_ok=True); os.makedirs(SVG_DIR, exist_ok=True)
    out = f"{DIAGRAMS_DIR}/container-floorplan-sheet2.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG)
    fig.savefig(svg_path(out), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  {out} saved")


if __name__ == "__main__":
    print("Generating container floor plan...")
    floor_plan()
    egress_detail()
    print("Done.")
