#!/usr/bin/env python3
"""generate_walkway_sections.py — LONGITUDINAL sections showing how a pipe threads
BELOW the right walkway (IBC end) and navigates the deck-support hardware.

Companion to the across-width sections: this cut is at 90° to those — an X–Z
elevation looking along +Yd, taken through the near-rim strip (Yd≈62, butted under
the tray near rim) where the ACC-01→spray-bar blue supply and the IBC-3→P-02 brown
return run the length of the container UNDER the walkway grate.  It shows the two
pipes ducking beneath the walkway deck and its support beams and turning up into the
corridor at the tray↔IBC gap — i.e. the vertical clearances a pipe actually has.

    Sheet 1 — SECTION B-B · near-rim strip under the RIGHT walkway (X–Z, look +Yd)

Geometry is single-sourced from tbs_constants.py; pipe positions are the diagram-of-
record detail dims read off the 3D water model (generate_pinhole_water_panel.py
tap01_supply / generate_corridor_water_panel.py P-02 return).

    python3 src/generators/generate_walkway_sections.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader
from tbs_constants import (
    IBC_COL_X, IBC_H_1000,
    WALKWAY_H, WALKWAY_GRATE_T, WALKWAY_RIGHT_X, WALKWAY_RIGHT_W,
    WALKWAY_LEFT_X, WALKWAY_W,
    PROC_TRAY_X_R, PROC_TRAY_X_L, PROC_TRAY_RIM,
    PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR, PROC_TRAY_D,
    PROC_TRAY_SUMP_Z, PROC_TRAY_SUMP_W, PROC_TRAY_DRAIN_X,
    PROC_TRAY_FLOOR_Z_LOW, PROC_TRAY_FLOOR_Z_HIGH, PROC_TRAY_SLOPE,
    tray_floor_z, tray_rim_top_z,
    SPRAY_BAR_WHEEL_DIA, SPRAY_BAR_BEAM_W, SPRAY_BAR_BEAM_H,
    SPRAY_BAR_BEAM_BOT_RISE, SPRAY_BAR_BEAM_TOP_RISE,
    spray_beam_top_z,
    DIAGRAMS_DIR,
)

# ── Palette ────────────────────────────────────────────────────────────────────
BG      = "#FFFFFF"
C_OUT   = "#1A1A1A"
C_DIM   = "#404040"
C_GHOST = "#9AA0A8"
C_FLOOR = "#E0DDD8"
C_STEEL = "#9A9AA2"   # walkway support beams (cut)
C_GRATE = "#8C8C94"   # grate deck
C_TRAY  = "#A6B4A6"
C_IBC_B = "#6B4A2E"
C_BLUE  = "#2979B8"
C_BROWN = "#8A6A3E"
FONT    = {"fontfamily": "monospace"}

OD = 21.0

# Right-walkway support (long beams run in Yd → cut as boxes at these X, Z80-115).
BEAM_XS = [WALKWAY_RIGHT_X, WALKWAY_RIGHT_X + WALKWAY_RIGHT_W - 40]   # 4329, 4589
BEAM_W  = 40
DECK_ZB = WALKWAY_H - WALKWAY_GRATE_T        # 115
GAPX    = PROC_TRAY_X_R + 12                  # 4641 — turn-up in the tray↔IBC gap

# ── Cantilever-zone members (diagram-of-record detail dims, verified against live water.skp) ──
# water.skp restraint = cp.frame() DEEP 4-leg box: FRONT upright X4654, front foot X4604-4754
# (the foot's left edge sits 25mm UNDER the tray right edge X4629).
ARM_X0, ARM_X1, ARM_ZB, ARM_ZT = WALKWAY_RIGHT_X, 4654, 70, 115   # RWK cantilever arm — clamps to the deep-box upright X4654 (reconciled from 4734)
UP_X0, UP_X1 = 4654, 4704            # corridor deep-box FRONT upright (50×50 RHS)
FOOT_X0, FOOT_X1, FOOT_ZT = 4604, 4754, 12                        # front floor foot 150×150×12 — EXTENDS under the tray
M12_XS = [4629, 4729]                # 4× M12 on 100 PCD (cx 4679 ± 50)
BRAIL_X0, BRAIL_X1, BRAIL_Z = 4704, 5104, 50                      # deep-box BOTTOM ring rail (X), Z0-50
RAIL_X0, RAIL_X1, RAIL_ZB, RAIL_ZT = 4654, 4674, 560, 610         # front retaining bar (ring rail) Z560

# Corridor pipe lanes (run in X; their Yd is 1101-1241, Z is 205-235) — ghosted where out of plane.
CORRIDOR_PIPES = [   # (Yd, Z, color, X0, X1, tag)
    (1132, 235, C_BLUE,  4660, 4984, "Blue supply trunk"),
    (1165, 235, "#777777", 4700, 5100, "DV-01 waste"),
    (1194, 205, C_BROWN, 4635, 4900, "tray-sump → P-04 suction"),
    (1241, 235, C_BLUE,  4733, 5100, "DV-01 blue recycle"),
]


def _rect(ax, x, z, w, h, fc, ec=C_OUT, lw=0.9, hatch=None, z0=5, alpha=1.0, ls="-"):
    ax.add_patch(Rectangle((x, z), w, h, facecolor=fc, edgecolor=ec,
                            linewidth=lw, hatch=hatch, zorder=z0, alpha=alpha, linestyle=ls))


def _run(ax, pts, col, z0=11):
    """Pipe run (axis-aligned X–Z waypoints) drawn OD-thick."""
    r = OD / 2
    for (a, b) in zip(pts[:-1], pts[1:]):
        (xa, za), (xb, zb) = a, b
        if za == zb:
            x0, w = min(xa, xb) - r, abs(xb - xa) + OD
            ax.add_patch(Rectangle((x0, za - r), w, OD, facecolor=col, edgecolor=C_OUT, lw=0.7, zorder=z0))
        else:
            z0b, h = min(za, zb) - r, abs(zb - za) + OD
            ax.add_patch(Rectangle((xa - r, z0b), OD, h, facecolor=col, edgecolor=C_OUT, lw=0.7, zorder=z0))


def sheet1():
    """SECTION B-B — near-rim strip under the right walkway (X–Z, looking +Yd)."""
    X_LO, X_HI = 4185, 4770
    Z_LO, Z_HI = -75, 430

    fig = plt.figure(figsize=(13.5, 10.2))
    ax = fig.add_axes([0.07, 0.07, 0.89, 0.86])
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text((X_LO + X_HI) / 2, Z_HI - 6,
            "SECTION B-B · NEAR-RIM STRIP UNDER THE RIGHT WALKWAY",
            ha="center", va="top", fontsize=11, fontweight="bold", color=C_OUT, **FONT)
    ax.text((X_LO + X_HI) / 2, Z_HI - 34,
            "X–Z elevation, looking along +Yd (strip Yd≈56–69, butted under the tray near rim) · 1:1",
            ha="center", va="top", fontsize=7.5, color=C_DIM, **FONT)

    # ── Floor ────────────────────────────────────────────────────────────────
    _rect(ax, X_LO, -40, X_HI - X_LO, 40, C_FLOOR, lw=1.0, hatch="////", z0=2)
    ax.text(X_LO + 12, -52, "container floor", fontsize=6, ha="left", va="top", color=C_DIM, **FONT)

    # ── Processing tray (behind the plane at Yd80 — ghost) ───────────────────
    _rect(ax, X_LO, 0, PROC_TRAY_X_R - X_LO, 2, C_TRAY, ec=C_GHOST, lw=0.7, z0=3, alpha=0.5, ls="--")
    _rect(ax, PROC_TRAY_X_R - 3, 0, 6, PROC_TRAY_RIM, C_TRAY, ec=C_GHOST, lw=0.8, z0=3, alpha=0.6, ls="--")
    ax.text(X_LO + 40, PROC_TRAY_RIM + 6, "processing tray  (behind plane, Yd80+)", fontsize=5.8,
            ha="left", va="bottom", color=C_GHOST, **FONT)

    # ── IBC-3 tote (beyond the gap, X≥4674 — cut here, rises out of frame) ────
    _rect(ax, IBC_COL_X, 0, X_HI - IBC_COL_X, Z_HI - Z_LO, C_IBC_B, ec=C_OUT, lw=1.0, z0=6, alpha=0.42)
    ax.text((IBC_COL_X + X_HI) / 2, 330, "IBC-3\n(Brown)\n↑ tote", fontsize=8, ha="center", va="center",
            color="white", fontweight="bold", zorder=8, **FONT)

    # ── RIGHT WALKWAY grate deck + its two Yd-running support beams (cut) ─────
    _rect(ax, WALKWAY_RIGHT_X, DECK_ZB, WALKWAY_RIGHT_W, WALKWAY_GRATE_T, C_GRATE, lw=1.0, z0=8)
    # grate bar ticks
    xg = WALKWAY_RIGHT_X + 12
    while xg < WALKWAY_RIGHT_X + WALKWAY_RIGHT_W - 6:
        ax.plot([xg, xg], [DECK_ZB + 2, WALKWAY_H - 2], color="#6F6F77", lw=0.5, zorder=9)
        xg += 24
    for bx in BEAM_XS:
        _rect(ax, bx, 80, BEAM_W, DECK_ZB - 80, C_STEEL, lw=0.9, z0=7)
    leader(ax, WALKWAY_RIGHT_X + 150, WALKWAY_H, WALKWAY_RIGHT_X + 150, 300,
           f"RIGHT WALKWAY GRATE DECK\n(X{WALKWAY_RIGHT_X}–{WALKWAY_RIGHT_X + WALKWAY_RIGHT_W} · deck Z{DECK_ZB}–{WALKWAY_H})",
           color=C_OUT, fs=6.4, ha="center", va="bottom", arrow_style="-|>", font=FONT)
    leader(ax, BEAM_XS[1] + BEAM_W / 2, 97, BEAM_XS[1] + 120, 250,
           "40×40 support beam\n(runs in Yd, cut) Z80–115", color=C_DIM, fs=6, ha="left",
           va="center", arrow_style="-|>", font=FONT)

    # ── The two strip pipes threading under the deck ─────────────────────────
    # Blue supply trunk: Yd69, Z40 in X → up to Z60 at the gap → turns into the corridor (out of plane).
    _run(ax, [(X_LO, 40), (GAPX, 40), (GAPX, 60)], C_BLUE)
    _run(ax, [(X_LO, 10), (GAPX, 10)], C_BROWN)   # IBC-3 → P-02 brown return: Yd56, Z10
    for (xx, zz, col) in [(GAPX, 60, C_BLUE), (GAPX, 10, C_BROWN)]:
        ax.add_patch(Circle((xx, zz), OD * 0.21, facecolor="white", edgecolor=col, lw=0.5, zorder=13))
    # end / turn labels
    leader(ax, GAPX, 60, GAPX + 70, 175, "↑ turns up into the\ncorridor → ACC-01",
           color=C_BLUE, fs=5.8, ha="left", va="center", arrow_style="-|>", font=FONT)
    leader(ax, GAPX, 10, GAPX + 70, -50, "↑ up to IBC-3 Brown\ntap (corridor)",
           color=C_BROWN, fs=5.8, ha="left", va="center", arrow_style="-|>", font=FONT)
    ax.annotate("← ACC-01 → spray bar / TAP-01 (Yd69, Z40)", xy=(X_LO + 6, 40), xytext=(X_LO + 90, 40),
                fontsize=6.2, ha="left", va="center", color=C_BLUE, **FONT)
    ax.annotate("← IBC-3 → P-02 return (Yd56, Z10)", xy=(X_LO + 6, 10), xytext=(X_LO + 90, -22),
                fontsize=6.2, ha="left", va="center", color=C_BROWN, **FONT)

    # ── Clearance dimensions (the point of the section) ──────────────────────
    draw_dim_v(ax, BEAM_XS[1] - 26, 40 + OD / 2, 80, f"{80 - int(40 + OD/2)}mm\nunder beam", offset=5, fs=5.4, font=FONT)
    draw_dim_v(ax, X_HI - 40, 0, WALKWAY_H, f"deck\nZ{WALKWAY_H}", offset=5, fs=5.6, font=FONT)
    draw_dim_v(ax, X_LO + 40, 0, 40, "Z40", offset=5, fs=5.4, font=FONT)
    draw_dim_h(ax, PROC_TRAY_X_R, IBC_COL_X, -46, f"{IBC_COL_X - PROC_TRAY_X_R}mm\ngap", offset=4, fs=5.4,
               above=False, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = (
        "SECTION B-B NOTES\n"
        "1. Cut is at 90° to the width sections — an X–Z elevation looking\n"
        "   along +Yd, through the near-rim strip (Yd≈56–69) butted under the\n"
        "   tray near rim, where two pipes run the container length.\n"
        "2. Both thread BELOW the walkway grate deck (Z115) and clear under\n"
        "   its two 40×40 Yd-running support beams (Z80–115).\n"
        "3. At the tray↔IBC gap (X4629–4674) each turns UP out of the plane\n"
        "   into the plumbing corridor (blue → ACC-01; brown → IBC-3 tap).\n"
        "4. To the left the strip continues under the near walkway to the\n"
        "   spray-bar tap (BV-05, X2399) and TAP-01 (X1130) — off-section."
    )
    ax.text(X_LO + 8, Z_HI - 70, notes, fontsize=6.2, ha="left", va="top", color=C_OUT,
            family="monospace", zorder=15,
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=C_DIM, lw=0.7))

    title_block(ax, "SHEET 1 OF 5",
                drawing_title="THE BIG SHOEBOX PROJECT · TBS-001",
                subtitle="WALKWAY ROUTING SECTIONS — B-B NEAR-RIM STRIP")

    out = os.path.join(DIAGRAMS_DIR, "walkway-sections-sheet1.png")
    fig.savefig(out, dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"Walkway section B-B (near-rim strip) → {out}")


def sheet2():
    """SECTION C-C — midway between the pinhole wall and the corridor (Yd≈523), X–Z, looking +Yd.

    The SAME cut as B-B, moved to mid-tray depth.  Here the tray basin is cut and the two
    pipes are no longer running IN the plane — they only CROSS it (in Yd) at the tray↔IBC
    gap, so they read as cross-section circles.  Confirms the routing rule: nothing traverses
    the tray along the length; pipes cross only in the gap past the tray's right edge.
    """
    from tbs_constants import PROC_TRAY_X_R as TXR
    Y_CUT = 523
    X_LO, X_HI = 4185, 4770
    Z_LO, Z_HI = -75, 430

    fig = plt.figure(figsize=(13.5, 10.2))
    ax = fig.add_axes([0.07, 0.07, 0.89, 0.86])
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text((X_LO + X_HI) / 2, Z_HI - 6,
            "SECTION C-C · MIDWAY (PINHOLE WALL ↔ CORRIDOR)",
            ha="center", va="top", fontsize=11, fontweight="bold", color=C_OUT, **FONT)
    ax.text((X_LO + X_HI) / 2, Z_HI - 34,
            f"X–Z elevation, looking along +Yd at Yd≈{Y_CUT} (mid-tray, halfway to the corridor) · 1:1",
            ha="center", va="top", fontsize=7.5, color=C_DIM, **FONT)

    # floor
    _rect(ax, X_LO, -40, X_HI - X_LO, 40, C_FLOOR, lw=1.0, hatch="////", z0=2)
    ax.text(X_LO + 12, -52, "container floor", fontsize=6, ha="left", va="top", color=C_DIM, **FONT)

    # processing tray — CUT here (basin floor + wash water + right end wall)
    _rect(ax, X_LO, 0, TXR - X_LO, 3, C_TRAY, lw=0.9, z0=5)
    _rect(ax, X_LO, 3, TXR - X_LO, 39, "#BFD8EA", ec="none", z0=4, alpha=0.55)          # wash water
    _rect(ax, TXR - 4, 0, 8, PROC_TRAY_RIM, C_TRAY, lw=0.9, z0=6)                        # right end wall
    ax.text(X_LO + 300, 30, "processing tray  (basin CUT here, wash water)", fontsize=6,
            ha="left", va="center", color="#3C5A6E", **FONT)

    # right walkway grate deck + support beams (overhead, same as B-B)
    _rect(ax, WALKWAY_RIGHT_X, DECK_ZB, WALKWAY_RIGHT_W, WALKWAY_GRATE_T, C_GRATE, lw=1.0, z0=8)
    xg = WALKWAY_RIGHT_X + 12
    while xg < WALKWAY_RIGHT_X + WALKWAY_RIGHT_W - 6:
        ax.plot([xg, xg], [DECK_ZB + 2, WALKWAY_H - 2], color="#6F6F77", lw=0.5, zorder=9)
        xg += 24
    for bx in BEAM_XS:
        _rect(ax, bx, 80, BEAM_W, DECK_ZB - 80, C_STEEL, lw=0.9, z0=7)
    leader(ax, WALKWAY_RIGHT_X + 150, WALKWAY_H, WALKWAY_RIGHT_X + 150, 300,
           f"RIGHT WALKWAY GRATE DECK\n(over the tray · X{WALKWAY_RIGHT_X}–{WALKWAY_RIGHT_X + WALKWAY_RIGHT_W})",
           color=C_OUT, fs=6.4, ha="center", va="bottom", arrow_style="-|>", font=FONT)

    # IBC-3 tote (beyond the gap)
    _rect(ax, IBC_COL_X, 0, X_HI - IBC_COL_X, Z_HI - Z_LO, C_IBC_B, ec=C_OUT, lw=1.0, z0=6, alpha=0.42)
    ax.text((IBC_COL_X + X_HI) / 2, 330, "IBC-3\n(Brown)\n↑ tote", fontsize=8, ha="center", va="center",
            color="white", fontweight="bold", zorder=8, **FONT)

    # the two pipes — CROSS-SECTION here (they run in Yd at the gap X4641)
    for (zz, col, tag) in [(60, C_BLUE, "ACC-01 → spray-bar blue supply"),
                           (10, C_BROWN, "IBC-3 → P-02 brown return")]:
        ax.add_patch(Circle((GAPX, zz), OD / 2, facecolor=col, edgecolor=C_OUT, lw=0.8, zorder=11))
        ax.add_patch(Circle((GAPX, zz), OD * 0.21, facecolor="white", edgecolor=col, lw=0.5, zorder=12))
    # Labels pulled LEFT into the clear zone (never over the IBC-3 tote — the
    # crossers only touch the gap; a rightward leader falsely reads as a pipe INTO the tote).
    leader(ax, GAPX, 60, GAPX - 120, 250, "ACC-01 → spray-bar\nblue supply (crosses in Yd)",
           color=C_BLUE, fs=5.8, ha="right", va="center", arrow_style="-|>", font=FONT)
    leader(ax, GAPX, 10, GAPX - 120, 150, "IBC-3 → P-02 brown\nreturn (crosses in Yd)",
           color=C_BROWN, fs=5.8, ha="right", va="center", arrow_style="-|>", font=FONT)

    draw_dim_v(ax, X_HI - 40, 0, WALKWAY_H, f"deck\nZ{WALKWAY_H}", offset=5, fs=5.6, font=FONT)
    draw_dim_h(ax, TXR, IBC_COL_X, -46, f"{IBC_COL_X - TXR}mm\ngap", offset=4, fs=5.4, above=False, font=FONT)

    notes = (
        "SECTION C-C NOTES\n"
        "1. SAME cut as B-B (X–Z, looking +Yd), moved to mid-depth (Yd≈523),\n"
        "   halfway between the pinhole wall and the plumbing corridor.\n"
        "2. Here the plane is INSIDE the processing tray — the basin + wash\n"
        "   water are cut; the walkway deck spans over the tray.\n"
        "3. NO pipe runs along the length at this depth: the tray is a no-route\n"
        "   exclusion zone.  The only pipes are the two that CROSS the plane in\n"
        "   Yd at the tray↔IBC gap (X4641) — so they read as cross-sections.\n"
        "4. Those same two pipes appear as long RUNS in B-B (the Yd≈62 strip);\n"
        "   between the two sheets you can read the whole crossing."
    )
    ax.text(X_LO + 8, Z_HI - 70, notes, fontsize=6.2, ha="left", va="top", color=C_OUT,
            family="monospace", zorder=15,
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=C_DIM, lw=0.7))

    title_block(ax, "SHEET 2 OF 5",
                drawing_title="THE BIG SHOEBOX PROJECT · TBS-001",
                subtitle="WALKWAY ROUTING SECTIONS — C-C MIDWAY")

    out = os.path.join(DIAGRAMS_DIR, "walkway-sections-sheet2.png")
    fig.savefig(out, dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"Walkway section C-C (midway) → {out}")


def sheet3():
    """SECTION D-D — through the NEAR cantilever (Yd≈1066), X–Z looking +Yd.

    Cut through the near cantilever arm + IBC corridor upright + floor foot, to read the
    AVAILABLE SPACE the corridor pipes have: the clear zone above the walkway deck up to
    the IBC ring rail.  The corridor pipe lanes (Yd1101-1241) sit just beyond this plane
    and are ghosted at their heights so the used-vs-free space is legible.
    """
    X_LO, X_HI = 4245, 4880
    Z_LO, Z_HI = -80, 720

    fig = plt.figure(figsize=(12.5, 12.5))
    ax = fig.add_axes([0.07, 0.06, 0.89, 0.87])
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text((X_LO + X_HI) / 2, Z_HI - 8,
            "SECTION D-D · THROUGH THE NEAR CANTILEVER",
            ha="center", va="top", fontsize=11, fontweight="bold", color=C_OUT, **FONT)
    ax.text((X_LO + X_HI) / 2, Z_HI - 40,
            "X–Z elevation, looking along +Yd at Yd≈1066 (near cantilever arm / IBC upright) · 1:1",
            ha="center", va="top", fontsize=7.5, color=C_DIM, **FONT)

    # floor
    _rect(ax, X_LO, -40, X_HI - X_LO, 40, C_FLOOR, lw=1.0, hatch="////", z0=2)

    # processing tray — CUT here (Yd1066 is inside the tray Yd80-2280): basin floor + wash water + RIGHT-END RIM
    tx_l = max(X_LO, PROC_TRAY_X_L)
    _rect(ax, tx_l, 0, PROC_TRAY_X_R - tx_l, 3, C_TRAY, lw=0.9, z0=4)                       # basin floor
    _rect(ax, tx_l, 3, PROC_TRAY_X_R - 4 - tx_l, PROC_TRAY_RIM - 8, "#BFD8EA", ec="none", z0=3, alpha=0.55)  # wash water
    _rect(ax, PROC_TRAY_X_R - 4, 0, 4, PROC_TRAY_RIM, C_TRAY, lw=1.0, z0=5)                 # RIGHT-END RIM (4mm wall, inner face of X4629, Z0-50)
    leader(ax, PROC_TRAY_X_R - 2, PROC_TRAY_RIM, PROC_TRAY_X_R - 150, PROC_TRAY_RIM + 70,
           f"processing tray right-end rim\n(X{PROC_TRAY_X_R}, Z0–{PROC_TRAY_RIM})", color="#3C5A6E",
           fs=5.8, ha="right", va="bottom", arrow_style="-|>", font=FONT)
    # tight clearance: brown crosser edge (X4630.5) ↔ tray edge (X4629) ≈ 1.5mm
    ax.annotate("", xy=(PROC_TRAY_X_R, 25), xytext=(GAPX - OD / 2, 25),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.7, color="#B03030", mutation_scale=5), zorder=14)
    ax.text(GAPX + 16, 25, "≈1.5mm clr\n(pipe ↔ tray rim)", fontsize=5.4, ha="left", va="center",
            color="#B03030", zorder=14, **FONT)

    # IBC-3 tote (behind this plane, Yd≤1046) — ghost
    _rect(ax, IBC_COL_X, 0, X_HI - IBC_COL_X, Z_HI - Z_LO, C_IBC_B, ec=C_GHOST, lw=0.9, z0=1, alpha=0.10, ls="--")
    ax.text((IBC_COL_X + X_HI) / 2, 660, "IBC-3 tote\n(behind, Yd≤1046)", fontsize=6, ha="center",
            va="center", color=C_GHOST, zorder=2, **FONT)

    # ── AVAILABLE ROUTING SPACE — the corridor volume PAST the front upright, above the bottom rail ──
    _rect(ax, UP_X1, BRAIL_Z, X_HI - UP_X1, RAIL_ZB - BRAIL_Z, "#DCEFDD",
          ec="#6FAF72", lw=0.8, z0=3, alpha=0.5, ls=(0, (4, 2)))
    ax.text((UP_X1 + X_HI) / 2, 340, "AVAILABLE ROUTING\nSPACE (corridor,\nX4704→5104 between\nthe frame uprights)",
            fontsize=6.0, ha="center", va="center", color="#3C7A40", fontweight="bold", zorder=4, **FONT)

    # ── Walkway support (cantilever arm + long bearers) + grate deck ─────────
    _rect(ax, ARM_X0, ARM_ZB, ARM_X1 - ARM_X0, ARM_ZT - ARM_ZB, C_STEEL, lw=1.0, z0=6)     # cantilever arm (Z70-115)
    for bx in BEAM_XS:                                                                      # long bearers (Yd-running, cut) Z80-115
        _rect(ax, bx, 80, BEAM_W, DECK_ZB - 80, C_STEEL, ec="#3A3A40", lw=1.0, z0=6, hatch="\\\\\\\\")
    _rect(ax, WALKWAY_RIGHT_X, DECK_ZB, WALKWAY_RIGHT_W, WALKWAY_GRATE_T, C_GRATE, lw=1.0, z0=7)  # deck
    leader(ax, 4500, ARM_ZB, 4358, -58,
           "walkway support: cantilever arm (Z70–115)\n+ long bearers (Z80–115, hatched)\n[arm clamps to the deep-box upright X4654]",
           color="#3A3A40", fs=5.2, ha="left", va="top", arrow_style="-|>", font=FONT)
    leader(ax, WALKWAY_RIGHT_X + 90, WALKWAY_H, 4358, 260, "right walkway grate deck (Z115–130)",
           color=C_OUT, fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)
    # the blue under-deck crosser (Z60) tops out at Z70.5 — it GRAZES the arm soffit (Z70)
    ax.add_patch(Circle((GAPX, 70), 6, facecolor="none", edgecolor="#B03030", lw=1.1, zorder=15))
    leader(ax, GAPX, 70, 4772, 92, "blue crosser (Z60) grazes the\narm soffit (Z70) — verify clash",
           color="#B03030", fs=5.0, ha="left", va="center", arrow_style="-|>", font=FONT)

    # ── Deep-box FRONT upright + front foot (extends UNDER the tray) + M12 + bottom rail + retaining bar ──
    _rect(ax, UP_X0, 0, UP_X1 - UP_X0, Z_HI - Z_LO, C_STEEL, lw=1.0, z0=6)                  # front upright X4654-4704
    _rect(ax, BRAIL_X0, 0, X_HI - BRAIL_X0, BRAIL_Z, C_STEEL, lw=0.9, z0=5)                 # deep-box bottom ring rail (→X5104)
    _rect(ax, FOOT_X0, 0, FOOT_X1 - FOOT_X0, FOOT_ZT, C_STEEL, lw=0.9, z0=8)                # front foot (X4604-4754, under tray)
    for mx in M12_XS:
        _rect(ax, mx - 6, 0, 12, 16, "#6A6A72", lw=0.5, z0=9)
    _rect(ax, RAIL_X0, RAIL_ZB, RAIL_X1 - RAIL_X0, RAIL_ZT - RAIL_ZB, C_STEEL, lw=0.9, z0=7)  # retaining bar Z560
    leader(ax, (UP_X0 + UP_X1) / 2, 500, UP_X1 + 22, 540, "corridor deep-box FRONT upright\n(50×50 RHS, X4654)",
           color=C_DIM, fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)
    leader(ax, FOOT_X0 + 16, FOOT_ZT, PROC_TRAY_X_R - 175, -60,
           "front floor foot 150×150×12 + 4× M12 —\nLEFT EDGE (X4604) EXTENDS 25mm UNDER THE TRAY",
           color="#B03030", fs=5.5, ha="left", va="top", arrow_style="-|>", font=FONT)
    leader(ax, X_HI - 60, BRAIL_Z, X_HI - 40, 92, "bottom ring rail (Z0–50)",
           color=C_DIM, fs=5.6, ha="right", va="center", arrow_style="-|>", font=FONT)
    leader(ax, (RAIL_X0 + RAIL_X1) / 2, RAIL_ZT, RAIL_X1 + 24, RAIL_ZT + 40,
           "retaining bar (ring rail) Z560", color=C_DIM, fs=6, ha="left", va="center",
           arrow_style="-|>", font=FONT)

    # ── ABOVE-deck crossers: the two PERIMETER surface runs cutting THIS plane in Yd at X4635 ──
    # (in-plane here — they run +Yd along the walkway perimeter at X4635, riding ABOVE the deck at
    #  Z205/235, ~75-105mm proud of it; the operator steps over them).
    for (zz, col) in [(235, C_BLUE), (205, C_BROWN)]:
        ax.add_patch(Circle((4635, zz), OD / 2, facecolor=col, edgecolor=C_OUT, lw=0.8, zorder=12))
        ax.add_patch(Circle((4635, zz), OD * 0.21, facecolor="white", edgecolor=col, lw=0.5, zorder=13))
    leader(ax, 4635, 235, 4384, 360, "blue filtered return\n(SV-01 → DV-01, Z235)",
           color=C_BLUE, fs=5.6, ha="left", va="center", arrow_style="-|>", font=FONT)
    leader(ax, 4635, 205, 4384, 305, "brown sump return\n(tray sump → P-04, Z205)",
           color=C_BROWN, fs=5.6, ha="left", va="center", arrow_style="-|>", font=FONT)
    # the corridor lanes (trunk/waste/recycle) run in X past the upright — shown in-plane in E-E
    ax.text((UP_X1 + X_HI) / 2, 235, "(blue trunk, grey waste,\nblue recycle run in X here\n— in-plane in E-E)",
            fontsize=5.0, ha="center", va="center", color=C_DIM, zorder=10, **FONT)

    # ── UNDER-deck crossers threading the TIGHT tray-rim ↔ front-upright gap (X4629↔4654 = 25mm) ──
    for (zz, col) in [(60, C_BLUE), (25, C_BROWN)]:
        ax.add_patch(Circle((GAPX, zz), OD / 2, facecolor=col, edgecolor=C_OUT, lw=0.8, zorder=12))
        ax.add_patch(Circle((GAPX, zz), OD * 0.21, facecolor="white", edgecolor=col, lw=0.5, zorder=13))
    leader(ax, GAPX, 60, 4360, 470, "blue → TAP-01 / spray-bar supply\n(transits the gap in Yd, under-deck)",
           color=C_BLUE, fs=5.6, ha="left", va="center", arrow_style="-|>", font=FONT)
    leader(ax, GAPX, 25, 4360, 405, "brown → P-02 / BV-03 suction\n(transits the gap in Yd, under-deck)",
           color=C_BROWN, fs=5.6, ha="left", va="center", arrow_style="-|>", font=FONT)
    ax.annotate("", xy=(UP_X0, 90), xytext=(GAPX + OD / 2, 90),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.7, color="#B03030", mutation_scale=5), zorder=14)
    ax.text(UP_X0 + 6, 92, "≈2.5mm\nto upright", fontsize=5.2, ha="left", va="center", color="#B03030", zorder=14, **FONT)

    # ── Dimensions ───────────────────────────────────────────────────────────
    draw_dim_v(ax, X_HI - 34, BRAIL_Z, RAIL_ZB, f"{RAIL_ZB - BRAIL_Z}mm\n(rail→rail)", offset=5, fs=5.4, font=FONT)
    draw_dim_v(ax, ARM_X0 - 22, 0, ARM_ZB, f"{ARM_ZB}\nunder arm", offset=5, fs=5.4, font=FONT)
    draw_dim_h(ax, PROC_TRAY_X_R, UP_X0, -30, f"{UP_X0 - PROC_TRAY_X_R}mm gap\n(rim→upright)", offset=4, fs=5.2, above=False, font=FONT)

    notes = (
        "SECTION D-D NOTES  (frame = water.skp deep-box cp.frame())\n"
        "1. X–Z cut through the NEAR cantilever (Yd≈1066).  The corridor\n"
        "   restraint is the DEEP 4-leg box: FRONT upright X4654, front foot\n"
        "   150×150 at X4604–4754 — its LEFT EDGE sits 25mm UNDER the tray.\n"
        "2. FOUR pipes cross this plane in Yd at the perimeter/gap (X4635–4641),\n"
        "   with the deck (Z115–130) between them:\n"
        "     ABOVE deck — blue filtered return SV-01→DV-01 (Z235) + brown\n"
        "       sump return tray→P-04 (Z205), riding proud of the deck;\n"
        "     BELOW deck — blue→TAP-01 (Z60) + brown→P-02/BV-03 (Z25).\n"
        "3. The two LOW crossers thread the TIGHT 25mm tray-rim↔upright gap —\n"
        "   ≈1.5mm (rim) / ≈2.5mm (upright), a pinch the plan views don't show.\n"
        "4. The corridor lanes (blue trunk, grey waste, blue recycle) run in X\n"
        "   past the upright (Yd1101–1241) — in-plane in E-E.\n"
        "5. STATUS: (a) front foot / M12 now CLEARS under the raised tray pan;\n"
        "   (b) RWK cantilever arm reconciled to the deep-box upright (X4654);\n"
        "   (c) blue TAP-01 crosser (Z60, top Z70.5) still GRAZES the arm soffit (Z70) — OPEN."
    )
    ax.text(X_LO + 8, Z_HI - 60, notes, fontsize=6.2, ha="left", va="top", color=C_OUT,
            family="monospace", zorder=15,
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=C_DIM, lw=0.7))

    title_block(ax, "SHEET 3 OF 5",
                drawing_title="THE BIG SHOEBOX PROJECT · TBS-001",
                subtitle="WALKWAY ROUTING SECTIONS — D-D NEAR CANTILEVER")

    out = os.path.join(DIAGRAMS_DIR, "walkway-sections-sheet3.png")
    fig.savefig(out, dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"Walkway section D-D (near cantilever) → {out}")


def sheet4():
    """SECTION E-E — corridor centre (Yd≈1130-1245 slab, the clear span between the frame
    uprights), X–Z looking +Yd.  Here the four corridor lanes the D-D ghosts pointed to run
    as REAL in-plane runs toward the pump column."""
    X_LO, X_HI = 4600, 5185
    Z_LO, Z_HI = -80, 660
    fig = plt.figure(figsize=(15.5, 8.8))
    ax = fig.add_axes([0.05, 0.08, 0.92, 0.82])
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI); ax.set_ylim(Z_LO, Z_HI); ax.set_aspect("equal"); ax.axis("off")
    ax.text((X_LO + X_HI) / 2, Z_HI - 6, "SECTION E-E · CORRIDOR CENTRE (between the frame uprights)",
            ha="center", va="top", fontsize=11, fontweight="bold", color=C_OUT, **FONT)
    ax.text((X_LO + X_HI) / 2, Z_HI - 32, "X–Z elevation, looking +Yd · slab Yd≈1130–1245 (the clear span) · 1:1",
            ha="center", va="top", fontsize=7.5, color=C_DIM, **FONT)

    _rect(ax, X_LO, -40, X_HI - X_LO, 40, C_FLOOR, lw=1.0, hatch="////", z0=2)                 # floor
    _rect(ax, X_LO, DECK_ZB, PROC_TRAY_X_R - X_LO, WALKWAY_GRATE_T, C_GRATE, lw=1.0, z0=7)     # deck right edge
    _rect(ax, BEAM_XS[1], 80, BEAM_W, DECK_ZB - 80, C_STEEL, ec="#3A3A40", lw=1.0, z0=6, hatch="\\\\\\\\")  # long bearer (no arm in this span)
    ax.text(X_LO + 6, WALKWAY_H + 6, "walkway deck (ends X4629) + bearer Z80–115 (no cantilever arm in this span)",
            fontsize=5.2, ha="left", va="bottom", color=C_DIM, **FONT)
    _rect(ax, UP_X0, 0, UP_X1 - UP_X0, 50, C_STEEL, lw=0.9, z0=6)                              # front bottom Yd-rail
    _rect(ax, 5104, 0, 50, 50, C_STEEL, lw=0.9, z0=6)                                          # back bottom Yd-rail
    for ux, tag in ((UP_X0, "front"), (5104, "back")):                                          # uprights (ghost, slab edges)
        _rect(ax, ux, 0, 50, Z_HI - Z_LO, C_GHOST, ec=C_GHOST, lw=0.8, z0=2, alpha=0.16, ls="--")
        ax.text(ux + 25, 600, f"{tag} upright\n(ghost)", fontsize=5, ha="center", va="center", color=C_GHOST, **FONT)
    _rect(ax, 4934, 355, 100, Z_HI - 355, C_GHOST, ec=C_GHOST, lw=0.8, z0=2, alpha=0.12, ls="--")  # pump column ghost
    ax.text(4984, 470, "pump column\n(P-01/04/05/03)\nghost, Yd≤1131", fontsize=4.8, ha="center", va="center", color=C_GHOST, **FONT)

    # ── The four corridor lanes as RUNS (co-planar at Z235 → raised for clarity) ──
    _run(ax, [(4635, 205), (4900, 205), (4900, Z_HI - 24)], C_BROWN)   # P-04 suction + rise into P-04
    _run(ax, [(4660, 235), (4984, 235)], C_BLUE)                       # blue supply trunk (true Z235)
    _run(ax, [(4700, 259), (X_HI - 6, 259)], "#777777")               # grey DV-01 waste (raised +24)
    _run(ax, [(4733, 283), (X_HI - 6, 283)], C_BLUE)                  # blue DV-01 recycle (raised +48)
    ax.annotate("↑ P-04 IN", xy=(4900, Z_HI - 24), xytext=(4915, Z_HI - 70),
                fontsize=5.6, ha="left", va="center", color=C_BROWN, zorder=13, **FONT)
    # legend (identifies the four lanes) — in the clear band below the lanes
    lgx, lgz = 4646, 188
    ax.text(lgx, lgz, "CORRIDOR LANES (→ toward the pumps):", fontsize=6, ha="left", va="top",
            color=C_OUT, fontweight="bold", zorder=14, **FONT)
    for i, (c, t) in enumerate([(C_BROWN, "brown P-04 suction — Z205 (rises into P-04)"),
                                (C_BLUE, "blue supply trunk — Z235"),
                                ("#777777", "grey DV-01 waste — Z235*"),
                                (C_BLUE, "blue DV-01 recycle — Z235*")]):
        zz = lgz - 24 - i * 22
        ax.add_patch(Rectangle((lgx, zz - 7), 30, 13, facecolor=c, edgecolor=C_OUT, lw=0.6, zorder=14))
        ax.text(lgx + 40, zz, t, fontsize=5.4, ha="left", va="center", color=C_OUT, zorder=14, **FONT)
    ax.text(lgx, lgz - 24 - 4 * 22 - 4, "* co-planar at Z235; waste/recycle raised +24/+48mm for clarity",
            fontsize=4.8, ha="left", va="top", color=C_DIM, zorder=14, **FONT)
    draw_dim_v(ax, X_HI - 28, 50, 560, "corridor\nopen\n(no ring\nrail here)", offset=5, fs=5, font=FONT)

    notes = (
        "SECTION E-E NOTES\n"
        "1. Cut in the CLEAR SPAN between the frame uprights (Yd1096–1266); the\n"
        "   uprights + pump column are just outside the slab, ghosted.\n"
        "2. The four corridor lanes run in X here (in-plane), riding Z205–235\n"
        "   toward the pump column — these are the D-D ghost lanes, now real.\n"
        "3. No IBC ring rail crosses this span, so the corridor is open above\n"
        "   the bottom rail (Z50) — the lanes use only the Z205–235 band."
    )
    ax.text(X_LO + 8, Z_HI - 60, notes, fontsize=6.0, ha="left", va="top", color=C_OUT,
            family="monospace", zorder=15, bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=C_DIM, lw=0.7))
    title_block(ax, "SHEET 4 OF 5", drawing_title="THE BIG SHOEBOX PROJECT · TBS-001",
                subtitle="WALKWAY ROUTING SECTIONS — E-E CORRIDOR CENTRE")
    out = os.path.join(DIAGRAMS_DIR, "walkway-sections-sheet4.png")
    fig.savefig(out, dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"Walkway section E-E (corridor centre) → {out}")


def sheet5():
    """SECTION F-F — through the FAR cantilever (Yd≈1286), X–Z looking +Yd.  Mirror of D-D:
    the far cantilever arm + far upright + far foot (also under the tray).  No under-deck
    crossers reach this far; the blue DV-01 recycle lane (Yd1241) is the nearest, just -Yd."""
    X_LO, X_HI = 4245, 4880
    Z_LO, Z_HI = -80, 720
    fig = plt.figure(figsize=(12.5, 12.5))
    ax = fig.add_axes([0.07, 0.06, 0.89, 0.87])
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI); ax.set_ylim(Z_LO, Z_HI); ax.set_aspect("equal"); ax.axis("off")
    ax.text((X_LO + X_HI) / 2, Z_HI - 8, "SECTION F-F · THROUGH THE FAR CANTILEVER",
            ha="center", va="top", fontsize=11, fontweight="bold", color=C_OUT, **FONT)
    ax.text((X_LO + X_HI) / 2, Z_HI - 40, "X–Z elevation, looking along +Yd at Yd≈1286 (far cantilever arm / IBC upright) · 1:1",
            ha="center", va="top", fontsize=7.5, color=C_DIM, **FONT)

    _rect(ax, X_LO, -40, X_HI - X_LO, 40, C_FLOOR, lw=1.0, hatch="////", z0=2)                 # floor
    # tray — CUT here too (Yd1286 is inside the tray Yd80-2280): basin + wash water + right rim
    tx_l = max(X_LO, PROC_TRAY_X_L)
    _rect(ax, tx_l, 0, PROC_TRAY_X_R - 4 - tx_l, 3, C_TRAY, lw=0.9, z0=4)
    _rect(ax, tx_l, 3, PROC_TRAY_X_R - 4 - tx_l, PROC_TRAY_RIM - 8, "#BFD8EA", ec="none", z0=3, alpha=0.55)
    _rect(ax, PROC_TRAY_X_R - 4, 0, 4, PROC_TRAY_RIM, C_TRAY, lw=1.0, z0=5)
    ax.text(tx_l + 60, 30, "processing tray (basin cut) + right-end rim", fontsize=5.6, ha="left", va="center", color="#3C5A6E", **FONT)
    # IBC-4 (Waste, far column) tote just beyond the gap — ghost
    _rect(ax, IBC_COL_X, 0, X_HI - IBC_COL_X, Z_HI - Z_LO, "#777777", ec=C_GHOST, lw=0.9, z0=1, alpha=0.12, ls="--")
    ax.text((IBC_COL_X + X_HI) / 2, 660, "IBC-4 tote\n(behind, Yd≥1316)", fontsize=6, ha="center", va="center", color=C_GHOST, zorder=2, **FONT)
    # available routing space (corridor past the upright)
    _rect(ax, UP_X1, BRAIL_Z, X_HI - UP_X1, RAIL_ZB - BRAIL_Z, "#DCEFDD", ec="#6FAF72", lw=0.8, z0=3, alpha=0.5, ls=(0, (4, 2)))
    ax.text((UP_X1 + X_HI) / 2, 340, "AVAILABLE ROUTING\nSPACE (corridor)", fontsize=6.2, ha="center", va="center", color="#3C7A40", fontweight="bold", zorder=4, **FONT)
    # far cantilever arm + long bearers + deck
    _rect(ax, ARM_X0, ARM_ZB, ARM_X1 - ARM_X0, ARM_ZT - ARM_ZB, C_STEEL, lw=1.0, z0=6)
    for bx in BEAM_XS:
        _rect(ax, bx, 80, BEAM_W, DECK_ZB - 80, C_STEEL, ec="#3A3A40", lw=1.0, z0=6, hatch="\\\\\\\\")
    _rect(ax, WALKWAY_RIGHT_X, DECK_ZB, WALKWAY_RIGHT_W, WALKWAY_GRATE_T, C_GRATE, lw=1.0, z0=7)
    leader(ax, 4500, ARM_ZB, 4358, -58, "walkway support: far cantilever arm (Z70–115)\n+ long bearers (Z80–115, hatched)", color="#3A3A40", fs=5.2, ha="left", va="top", arrow_style="-|>", font=FONT)
    leader(ax, WALKWAY_RIGHT_X + 90, WALKWAY_H, 4358, 250, "right walkway grate deck (Z115–130)", color=C_OUT, fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)
    # far upright + far foot (also under tray) + M12 + bottom rail + retaining bar
    _rect(ax, UP_X0, 0, UP_X1 - UP_X0, Z_HI - Z_LO, C_STEEL, lw=1.0, z0=6)                     # far upright X4654-4704
    _rect(ax, BRAIL_X0, 0, X_HI - BRAIL_X0, BRAIL_Z, C_STEEL, lw=0.9, z0=5)                    # bottom ring rail
    _rect(ax, FOOT_X0, 0, FOOT_X1 - FOOT_X0, FOOT_ZT, C_STEEL, lw=0.9, z0=8)                   # far foot (under tray)
    for mx in M12_XS:
        _rect(ax, mx - 6, 0, 12, 16, "#6A6A72", lw=0.5, z0=9)
    _rect(ax, RAIL_X0, RAIL_ZB, RAIL_X1 - RAIL_X0, RAIL_ZT - RAIL_ZB, C_STEEL, lw=0.9, z0=7)   # retaining bar
    leader(ax, (UP_X0 + UP_X1) / 2, 500, UP_X1 + 22, 540, "corridor deep-box FAR upright\n(50×50 RHS, X4654)", color=C_DIM, fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)
    leader(ax, FOOT_X0 + 16, FOOT_ZT, PROC_TRAY_X_R - 175, -60, "far floor foot 150×150×12 —\nLEFT EDGE EXTENDS 25mm UNDER THE TRAY", color="#B03030", fs=5.5, ha="left", va="top", arrow_style="-|>", font=FONT)
    leader(ax, (RAIL_X0 + RAIL_X1) / 2, RAIL_ZT, RAIL_X1 + 24, RAIL_ZT + 40, "retaining bar (ring rail) Z560", color=C_DIM, fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)
    # nearest corridor lane (blue recycle Yd1241) — ghost, -Yd of this plane
    ax.add_patch(Circle((4772, 235), OD / 2, facecolor="none", edgecolor=C_BLUE, lw=1.4, ls="--", zorder=9))
    ax.text(4772, 219, "blue DV-01 recycle\n(Yd1241, ghost, −Yd)", fontsize=4.8, ha="center", va="top", color=C_BLUE, zorder=10, **FONT)

    notes = (
        "SECTION F-F NOTES\n"
        "1. Far cantilever (Yd≈1286) — mirrors D-D on the far side of the\n"
        "   corridor: arm off the FAR IBC upright (X4654), foot X4604–4754\n"
        "   again extending 25mm UNDER the tray.\n"
        "2. NO under-deck crossers reach this far (they turn up by Yd1132–1170).\n"
        "3. The nearest corridor lane is the blue DV-01 recycle (Yd1241), just\n"
        "   −Yd of this plane — ghosted.  See E-E for the lanes in-plane."
    )
    ax.text(X_LO + 8, Z_HI - 60, notes, fontsize=6.0, ha="left", va="top", color=C_OUT,
            family="monospace", zorder=15, bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=C_DIM, lw=0.7))
    title_block(ax, "SHEET 5 OF 5", drawing_title="THE BIG SHOEBOX PROJECT · TBS-001",
                subtitle="WALKWAY ROUTING SECTIONS — F-F FAR CANTILEVER")
    out = os.path.join(DIAGRAMS_DIR, "walkway-sections-sheet5.png")
    fig.savefig(out, dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"Walkway section F-F (far cantilever) → {out}")


def sheet6():
    """SECTION G-G / H-H — tray drainage slope, welded-pan support, and the
    spray-carriage clearance under the walkway on the raised/sloped floor."""
    EXAG = 6.0                                    # vertical exaggeration (slopes ~1:200)
    def zx(z): return z * EXAG

    fig = plt.figure(figsize=(13.5, 12.0))
    fig.patch.set_facecolor(BG)

    # ── Panel A — LONGITUDINAL Yd–Z along the sump column (slope + support) ──
    axA = fig.add_axes([0.07, 0.55, 0.90, 0.40]); axA.set_facecolor(BG); axA.axis("off")
    YL, YH = -80, 2380
    axA.set_xlim(YL, YH); axA.set_ylim(zx(-30), zx(122))
    Xd = PROC_TRAY_DRAIN_X
    axA.text((YL + YH) / 2, zx(120), "SECTION G-G · TRAY DRAINAGE SLOPE & WELDED-PAN SUPPORT",
             ha="center", va="top", fontsize=10.5, fontweight="bold", color=C_OUT, **FONT)
    axA.text((YL + YH) / 2, zx(110),
             f"longitudinal Yd–Z at the sump column (X≈{Xd}) · vertical exaggeration {EXAG:.0f}× · dual-axis 1:200 fall",
             ha="center", va="top", fontsize=7, color=C_DIM, **FONT)
    axA.add_patch(Rectangle((YL, zx(-25)), YH - YL, zx(25), fc=C_FLOOR, ec=C_OUT, lw=1.0, hatch="////", zorder=2))
    axA.text(YL + 20, zx(-14), "container floor (Z0)", fontsize=6, ha="left", va="center", color=C_DIM, **FONT)
    yds = [PROC_TRAY_YD_NEAR + i * PROC_TRAY_D / 40 for i in range(41)]
    ptop = [tray_floor_z(Xd, y) for y in yds]
    pbot = [t - 2 for t in ptop]
    axA.fill_between(yds, [zx(0)] * len(yds), [zx(b) for b in pbot], fc="#E6E0D2", ec=C_OUT, lw=0.4, hatch="xx", zorder=3)
    axA.fill_between(yds, [zx(b) for b in pbot], [zx(t) for t in ptop], fc=C_TRAY, ec=C_OUT, lw=0.6, zorder=4)
    axA.fill_between(yds, [zx(t) for t in ptop], [zx(t + 4) for t in ptop], fc="#BFD8EA", ec="none", alpha=0.6, zorder=4.1)
    axA.add_patch(Rectangle((PROC_TRAY_YD_NEAR - 6, zx(ptop[0])), 6, zx(PROC_TRAY_RIM), fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=5))
    axA.add_patch(Rectangle((PROC_TRAY_YD_FAR, zx(ptop[-1])), 6, zx(PROC_TRAY_RIM), fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=5))
    axA.add_patch(Rectangle((PROC_TRAY_YD_NEAR, zx(0)), PROC_TRAY_SUMP_W, zx(PROC_TRAY_SUMP_Z),
                            fc="#BFD8EA", ec=C_OUT, lw=1.0, zorder=6))
    leader(axA, PROC_TRAY_YD_NEAR + PROC_TRAY_SUMP_W / 2, zx(4), PROC_TRAY_YD_NEAR + 340, zx(46),
           f"corner SUMP (low point) — well {PROC_TRAY_SUMP_Z}mm deep,\nbottom rests ON the container floor (Z0)",
           color="#2A6", fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)
    leader(axA, 1500, zx(ptop[26] - 1), 1500, zx(ptop[26] - 22),
           "tapered HDPE shim ramp\n(carries the welded pan)", color=C_DIM, fs=6, ha="center", va="top",
           arrow_style="-|>", font=FONT)
    leader(axA, 1900, zx(ptop[33] + 2), 1900, zx(ptop[33] + 34),
           f"welded 304-SS pan floor rises\nZ{PROC_TRAY_FLOOR_Z_LOW:.0f} (near) → Z{tray_floor_z(Xd, PROC_TRAY_YD_FAR):.0f} (far)",
           color="#3C5A6E", fs=6, ha="center", va="bottom", arrow_style="-|>", font=FONT)

    # ── Panel B — CROSS X–Z at the FAR rim: worst spray-carriage clearance ──
    axB = fig.add_axes([0.07, 0.06, 0.90, 0.42]); axB.set_facecolor(BG); axB.axis("off")
    XL, XH = 40, 4780
    axB.set_xlim(XL, XH); axB.set_ylim(zx(-30), zx(155))
    ydc = PROC_TRAY_YD_FAR
    axB.text((XL + XH) / 2, zx(153), "SECTION H-H · SPRAY-CARRIAGE CLEARANCE AT THE FAR RIM (X–Z)",
             ha="center", va="top", fontsize=10.5, fontweight="bold", color=C_OUT, **FONT)
    axB.text((XL + XH) / 2, zx(143),
             f"far rim (Yd{ydc}) — the high corner of the dual slope · vertical exaggeration {EXAG:.0f}×",
             ha="center", va="top", fontsize=7, color=C_DIM, **FONT)
    axB.add_patch(Rectangle((XL, zx(-25)), XH - XL, zx(25), fc=C_FLOOR, ec=C_OUT, lw=1.0, hatch="////", zorder=2))
    xs = [PROC_TRAY_X_L + i * (PROC_TRAY_X_R - PROC_TRAY_X_L) / 60 for i in range(61)]
    ttop = [tray_floor_z(x, ydc) for x in xs]
    tbot = [t - 2 for t in ttop]
    axB.fill_between(xs, [zx(0)] * len(xs), [zx(b) for b in tbot], fc="#E6E0D2", ec=C_OUT, lw=0.4, hatch="xx", zorder=3)
    axB.fill_between(xs, [zx(b) for b in tbot], [zx(t) for t in ttop], fc=C_TRAY, ec=C_OUT, lw=0.6, zorder=4)
    axB.add_patch(Rectangle((PROC_TRAY_X_L, zx(ttop[0])), 6, zx(PROC_TRAY_RIM), fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=5))
    axB.add_patch(Rectangle((PROC_TRAY_X_R - 6, zx(ttop[-1])), 6, zx(PROC_TRAY_RIM), fc=C_TRAY, ec=C_OUT, lw=1.0, zorder=5))
    # level walkway grate decks at both tray edges
    for (wx0, ww) in [(WALKWAY_LEFT_X, WALKWAY_W), (WALKWAY_RIGHT_X, WALKWAY_RIGHT_W)]:
        axB.add_patch(Rectangle((wx0, zx(DECK_ZB)), ww, zx(WALKWAY_GRATE_T), fc=C_GRATE, ec=C_OUT, lw=0.8, zorder=7))
    axB.text(WALKWAY_LEFT_X + WALKWAY_W / 2, zx(DECK_ZB + WALKWAY_GRATE_T + 3), "LEFT WALKWAY GRATE (LEVEL Z%d)" % DECK_ZB,
             fontsize=5.6, ha="center", va="bottom", color=C_DIM, **FONT)
    # spray carriage under the LEFT walkway (worst case) — envelope box floor→beam-top
    cx = WALKWAY_LEFT_X + WALKWAY_W                      # 570 — beam inner end at the walkway edge
    fz = tray_floor_z(cx, ydc)
    top_new = spray_beam_top_z(cx, ydc)
    top_old = fz + 58                                    # old Ø50 / 40×40 assembly
    # old envelope (ghost)
    axB.add_patch(Rectangle((cx - 40, zx(fz)), 150, zx(top_old - fz), fc="none", ec="#B03030",
                            lw=0.9, ls=(0, (4, 2)), zorder=8))
    axB.text(cx + 190, zx(top_old), "old Ø50 / 40×40 carriage\n(top Z%.0f → only %.0fmm clear)" % (top_old, DECK_ZB - top_old),
             fontsize=5.6, ha="left", va="center", color="#B03030", **FONT)
    # new (shrunk) carriage envelope
    axB.add_patch(Rectangle((cx - 40, zx(fz)), 150, zx(top_new - fz), fc="#C9D6E4", ec=C_OUT, lw=1.1, zorder=9))
    axB.text(cx + 55, zx(fz + (top_new - fz) / 2), "Ø32 wheels +\n40×25 SS beam", fontsize=5.6,
             ha="left", va="center", color=C_OUT, **FONT)
    # clearance dimension (new)
    draw_dim_v(axB, cx + 130, zx(top_new), zx(DECK_ZB), f"{DECK_ZB - top_new:.0f}mm CLEAR", offset=3, fs=7, font=FONT)
    leader(axB, PROC_TRAY_X_L + 3, zx(ttop[0] + PROC_TRAY_RIM), PROC_TRAY_X_L + 380, zx(ttop[0] + PROC_TRAY_RIM + 26),
           f"pan/rim highest at the far-left corner\n(floor Z{ttop[0]:.0f}, rim top Z{tray_rim_top_z(PROC_TRAY_X_L, ydc):.0f})",
           color="#3C5A6E", fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)

    axTB = fig.add_axes([0.07, 0.005, 0.90, 0.045])
    axTB.set_xlim(0, 1); axTB.set_ylim(0, 1); axTB.axis("off")
    title_block(axTB, "SHEET 6 OF 6",
                drawing_title="THE BIG SHOEBOX PROJECT · TBS-001",
                subtitle="WALKWAY ROUTING SECTIONS — G-G TRAY SLOPE/SUPPORT · H-H CARRIAGE CLEARANCE")
    out = os.path.join(DIAGRAMS_DIR, "walkway-sections-sheet6.png")
    fig.savefig(out, dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"Walkway section G-G/H-H (tray slope + carriage clearance) → {out}")


def main():
    sheet1()
    sheet2()
    sheet3()
    sheet4()
    sheet5()
    sheet6()


if __name__ == "__main__":
    main()
