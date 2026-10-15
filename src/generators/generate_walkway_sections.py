#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""generate_walkway_sections.py — LONGITUDINAL sections showing how the corridor↔
pinhole-wall pipes thread BELOW the right walkway (IBC end) as the under-walkway RIBBON.

Companion to the across-width sections: this cut is at 90° to those — an X–Z elevation
looking along +Yd, taken at increasing Yd depths.  The four corridor↔pinhole-wall lines
(IBC-3→P-02, tray-sump→P-04, Blue trunk→TAP-01, filtered return SV-01→DV-01) run TOGETHER
as a flat RIBBON in the dead space UNDER the right-walkway grate, in the clear channel
BETWEEN the two walkway long beams (above the tray rim).  The sections show the ribbon in-
plane over the tray, its loop UP over the first cantilever, and its drop into the corridor
through the OPEN bay between the cantilever arms (the outer beam is omitted over the corridor,
so there is no beam to cross) — i.e. the vertical clearances the ribbon actually has.

    Sheet 1 — SECTION B-B · near-end ribbon transitions under the RIGHT walkway (X–Z)

Geometry is single-sourced: structure from tbs_constants.py; the ribbon lanes/loop-over
from generate_corridor_water_panel.py (module `cp` — RIBBON_LANE_X, RIBBON_Z, RIBBON_OVER_Z,
RIBBON_YD_UP, RIBBON_SUP_YD, ribbon_supports()).

    /usr/bin/python3 src/generators/generate_walkway_sections.py
"""
import os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader, draw_notes, draw_pipe_path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "models"))
import generate_corridor_water_panel as cp   # ribbon geometry (single source)
import generate_pinhole_water_panel as pw    # P-02/DV-01/SV-01 + ribbon corridor ends (water.skp build)
from tbs_constants import IBC_COL_X, WALKWAY_H, WALKWAY_GRATE_T, WALKWAY_RIGHT_X, WALKWAY_RIGHT_W, WALKWAY_LEFT_X, WALKWAY_W, PROC_TRAY_X_R, PROC_TRAY_X_L, PROC_TRAY_RIM, PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR, PROC_TRAY_D, PROC_TRAY_SUMP_Z, PROC_TRAY_SUMP_W, PROC_TRAY_DRAIN_X, PROC_TRAY_FLOOR_Z_LOW, tray_floor_z, tray_rim_top_z, spray_beam_top_z, DIAGRAMS_DIR
from tbs_constants import DIAGRAM_DPI

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
C_WASTE = "#8A8A90"   # gray — DV-02 waste → IBC-4 merge line
FONT    = {"fontfamily": "monospace"}

LBL_BG   = dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.0)

OD = 21.0
PIPE_WALL = 2.5   # OD21 HDPE wall for draw_pipe_path (parallel-sided pipe + elbow fittings)
CORR_X_LO, CORR_X_HI = 4580, 5480   # E-E corridor-elevation X window (pump column + end-wall ports)

# Right-walkway support (long beams run in Yd → cut as boxes at these X, Z80-115).
BEAM_XS = [WALKWAY_RIGHT_X, WALKWAY_RIGHT_X + WALKWAY_RIGHT_W - 40]   # 4329, 4589
BEAM_W  = 40
BEAM_Z_BOT = 80                              # long-beam underside (beams span Z80–DECK_ZB)
DECK_ZB = WALKWAY_H - WALKWAY_GRATE_T        # 115
GAPX    = PROC_TRAY_X_R + 12                  # 4641 — under-beam crossing in the tray↔IBC gap

# ── Under-walkway pipe RIBBON (single-sourced from generate_corridor_water_panel `cp`) ──
# Four lanes side-by-side in X (26mm pitch) in the clear channel BETWEEN the two long beams,
# at Z=cp.RIBBON_Z (104.5 — FLUSH: pipe crown at the deck underside) under the grate (Z115-130),
# above the tray rim (Z50).  The middle two lanes were SWAPPED (blue TAP-01 trunk ↔ brown tray-sump)
# so the blue/brown lines alternate and no longer cross on the way into the corridor.  Lane order
# (from the outer/IBC beam inward) + which line each carries + its color.
RIBBON_LANES = [   # (X, color, tag)  — index-matched to cp.RIBBON_LANE_X
    (cp.RIBBON_LANE_X[0], C_BROWN, "IBC-3 → P-02"),
    (cp.RIBBON_LANE_X[1], C_BLUE,  "Blue trunk → TAP-01"),
    (cp.RIBBON_LANE_X[2], C_BROWN, "tray sump → P-04"),
    (cp.RIBBON_LANE_X[3], C_BLUE,  "SV-01 → DV-01 return"),
]
RIBBON_Z      = cp.RIBBON_Z            # 104.5 — FLUSH under the grate (pipe crown at deck underside Z115)
RIBBON_OVER_Z = cp.RIBBON_OVER_Z       # 142 — loop crest just above the grate (over the cantilever)
RIBBON_YD_UP  = cp.RIBBON_YD_UP        # 1000 — where the ribbon rises to loop over the first cantilever
CHAN_X0 = BEAM_XS[0] + BEAM_W          # 4369 — inner edge of the channel (inner beam)
CHAN_X1 = BEAM_XS[1]                   # 4534 — outer edge of the channel (outer beam)
# Outer-beam Yd extent: the beam is in TWO runs that stop at the cantilever arms, leaving the
# corridor bay (Yd RWK_UP_YDS[0]+arm .. RWK_UP_YDS[1], ~1097-1266) OPEN — the ribbon lanes cross
# there in the clear (no beam, no notch).
UNDER_BEAM_Z = 65                      # corridor-entry Z where the EXISTING corridor routing picks up (reached
#                                        via the tray-edge slot drop from the flush ribbon)


def _ribbon_circles(ax, z=None, r=None, z0=12, label=False, fs=5.4):
    """Draw the four ribbon lanes end-on (cross-section circles) at height z (default RIBBON_Z)."""
    z = RIBBON_Z if z is None else z
    r = OD / 2 if r is None else r
    for (xx, col, tag) in RIBBON_LANES:
        ax.add_patch(Circle((xx, z), r, facecolor=col, edgecolor=C_OUT, lw=0.8, zorder=z0))
        ax.add_patch(Circle((xx, z), r * 0.42, facecolor="white", edgecolor=col, lw=0.5, zorder=z0 + 1))

# ── Cantilever-zone members (diagram-of-record detail dims, verified against live water.skp) ──
# water.skp restraint = cp.frame() DEEP 4-leg box: FRONT upright X4654, front foot X4604-4754
# (the foot's left edge sits 25mm UNDER the tray right edge X4629).
ARM_X0, ARM_X1, ARM_ZB, ARM_ZT = WALKWAY_RIGHT_X, 4654, 70, 115   # RWK cantilever arm — clamps to the deep-box upright X4654 (reconciled from 4734)
UP_X0, UP_X1 = 4654, 4704            # corridor deep-box FRONT upright (50×50 RHS)
FOOT_X0, FOOT_X1, FOOT_ZT = 4604, 4754, 12                        # front floor foot 150×150×12 — EXTENDS under the tray
M12_XS = [4629, 4729]                # 4× M12 on 100 PCD (cx 4679 ± 50)
BRAIL_X0, BRAIL_X1, BRAIL_Z = 4704, 5104, 50                      # deep-box BOTTOM ring rail (X), Z0-50
RAIL_X0, RAIL_X1, RAIL_ZB, RAIL_ZT = 4654, 4674, 560, 610         # front retaining bar (ring rail) Z560


def _rect(ax, x, z, w, h, fc, ec=C_OUT, lw=0.9, hatch=None, z0=5, alpha=1.0, ls="-"):
    ax.add_patch(Rectangle((x, z), w, h, facecolor=fc, edgecolor=ec,
                            linewidth=lw, hatch=hatch, zorder=z0, alpha=alpha, linestyle=ls))


def _crossing_gaps(a, b, obstacles, gap):
    """Scalar gap-intervals along the axis-aligned segment a->b where a (perpendicular)
    obstacle segment crosses its interior — the rear pipe breaks here (plumbing skill)."""
    horiz = a[1] == b[1]
    out = []
    for oa, ob in obstacles:
        if (oa[1] == ob[1]) == horiz:
            continue                                    # parallel runs don't cross
        if horiz:
            hz, (hx0, hx1) = a[1], sorted((a[0], b[0]))
            vx, (vz0, vz1) = oa[0], sorted((oa[1], ob[1]))
            if hx0 < vx < hx1 and vz0 < hz < vz1:
                out.append((vx - gap, vx + gap))
        else:
            vx, (vz0, vz1) = a[0], sorted((a[1], b[1]))
            hz, (hx0, hx1) = oa[1], sorted((oa[0], ob[0]))
            if vz0 < hz < vz1 and hx0 < vx < hx1:
                out.append((hz - gap, hz + gap))
    return out


def _merge_gaps(ivals, slack):
    """Coalesce gap intervals that are closer than *slack* (drops sub-OD visible stubs)."""
    out = []
    for lo, hi in sorted(ivals):
        if out and lo <= out[-1][1] + slack:
            out[-1][1] = max(out[-1][1], hi)
        else:
            out.append([lo, hi])
    return out


def _split_run(pts, obstacles, gap):
    """Break a polyline into contiguous sub-polylines wherever a front obstacle crosses it,
    preserving its real corners (so each sub-run still draws its elbow fittings)."""
    subs, cur = [], [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        horiz = a[1] == b[1]
        s0, s1 = (a[0], b[0]) if horiz else (a[1], b[1])
        lo, hi, fwd = min(s0, s1), max(s0, s1), s1 > s0
        mk = (lambda s: (s, a[1])) if horiz else (lambda s: (a[0], s))
        gaps = _merge_gaps([(max(g0, lo), min(g1, hi)) for g0, g1 in
                            _crossing_gaps(a, b, obstacles, gap) if lo < (g0 + g1) / 2 < hi], OD)
        for g0, g1 in sorted(gaps, reverse=not fwd):
            near, far = (g0, g1) if fwd else (g1, g0)
            cur.append(mk(near))
            if len(cur) >= 2:
                subs.append(cur)
            cur = [mk(far)]
        cur.append(b)
    if len(cur) >= 2:
        subs.append(cur)
    return subs


def _draw_lanes(ax, runs):
    """Draw pipe runs with elbow fittings AND legible over/under crossings: runs are listed
    BACK->FRONT, each rear run breaks flush at every front run's wall (house crossing convention,
    gray->brown->blue layering)."""
    segs = [list(zip(pts[:-1], pts[1:])) for pts, _ in runs]
    for i, (pts, col) in enumerate(runs):
        obstacles = [s for j in range(i + 1, len(runs)) for s in segs[j]]   # higher index = in front
        for sub in _split_run(pts, obstacles, OD / 2):
            draw_pipe_path(ax, [p[0] for p in sub], [p[1] for p in sub], OD, PIPE_WALL,
                           fc=col, ec=C_OUT, bore_fc=col, zorder=8 + 2 * i)


# ── Faithful corridor routing: the REAL 3D pipe paths, projected into the E-E X–Z plane ──────────
# Captured LIVE from the water.skp builders (generate_corridor_water_panel + generate_pinhole_water_panel,
# the sump_on_skid=True config the water model is built with) so the section can never drift from the 3D.
# Each 3D waypoint (X,Yd,Z) projects to (X,Z); pure-Yd moves collapse (they're "into the page").
_LAYER = {"#777777": 0, "#8A8A90": 0,                      # gray waste → back
          "#6B4A2E": 1, "#8A6A3E": 1,                      # brown → middle
          "#2979B8": 2, "#3A6EA5": 2, "#2060A0": 2}        # blue / filtered-blue → front
_CORRIDOR_COL = {"#6B4A2E": C_BROWN, "#8A6A3E": C_BROWN,
                 "#2979B8": C_BLUE, "#3A6EA5": C_BLUE, "#2060A0": C_BLUE,
                 "#777777": C_WASTE, "#8A8A90": C_WASTE, "#B8B840": "#B8B840"}


def _project_xz(way):
    """3D (X,Yd,Z) waypoints → X–Z polyline with pure-Yd (into-page) moves collapsed."""
    out = []
    for x, _yd, z in way:
        p = (round(x, 1), round(z, 1))
        if not out or p != out[-1]:
            out.append(p)
    return out


def _capture_corridor_pipes():
    """Run the water.skp pipe builders with a capturing shim and return the corridor runs as
    (name, xz_pts, matplotlib_color), ordered BACK->FRONT (gray, brown, blue) for _draw_lanes."""
    cap = []
    orig = cp.draw.ruby_pipe_run                                   # draw is shared by cp + pw
    cp.draw.ruby_pipe_run = lambda nm, way, *a, **k: (
        cap.append((nm, [tuple(c for c in p) for p in way], k.get("color"))) or "")
    try:
        for fn in (lambda: cp.plumbing(sump_on_skid=True),
                   lambda: cp.drains_ports(sump_on_skid=True),
                   lambda: cp.equipment(sump_on_skid=True),
                   pw.tap01_supply, lambda: pw.kit(p02_on_corridor=True),
                   pw.skid_row, pw.skid_plumbing, pw.other_equipment):
            try:
                fn()
            except Exception:
                pass                                              # a builder we don't need may need SU; skip it
    finally:
        cp.draw.ruby_pipe_run = orig
    # IBC tote-top FILL + equalization lines belong to the IBC stack (ghosted here) and the
    # IBC-stacking diagram — they'd only float sparse tags in the upper band, so omit them from
    # the corridor pump-bay elevation.
    SKIP = ("x1 ", "equalization")
    seen, runs = set(), []
    for nm, way, col in cap:
        key = (nm, tuple(way))
        if key in seen or any(s in nm.lower() for s in SKIP):
            continue
        seen.add(key)
        xz = _project_xz(way)
        if len(xz) < 2 or max(p[0] for p in xz) < CORR_X_LO:       # fully off toward the pinhole wall
            continue
        runs.append((nm, xz, col))
    runs.sort(key=lambda r: _LAYER.get(r[2], 1))                   # gray → brown → blue (back → front)
    return runs


def sheet1():
    """SECTION B-B — near-end ribbon transitions under the right walkway (X–Z, looking +Yd)."""
    X_CUT = 62
    X_LO, X_HI = 4185, 4770
    Z_LO, Z_HI = -75, 475   # taller header band so the notes box clears the centered subtitle

    fig = plt.figure(figsize=(13.5, 10.2))
    ax = fig.add_axes([0.07, 0.07, 0.89, 0.86])
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text((X_LO + X_HI) / 2, Z_HI - 6,
            "SECTION B-B · NEAR-END RIBBON UNDER THE RIGHT WALKWAY",
            ha="center", va="top", fontsize=11, fontweight="bold", color=C_OUT, **FONT)
    ax.text((X_LO + X_HI) / 2, Z_HI - 34,
            f"X–Z elevation, looking along +Yd at Yd≈{X_CUT} (near the pinhole-wall end of the ribbon) · 1:1",
            ha="center", va="top", fontsize=7.5, color=C_DIM, **FONT)

    # ── Floor ────────────────────────────────────────────────────────────────
    _rect(ax, X_LO, -40, X_HI - X_LO, 40, C_FLOOR, lw=1.0, hatch="////", z0=2)
    ax.text(X_LO + 12, -52, "container floor", fontsize=6, ha="left", va="top", color=C_DIM, **FONT)

    # ── Processing tray near rim (basin behind the plane at Yd80 — ghost) ─────
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
        _rect(ax, bx, BEAM_Z_BOT, BEAM_W, DECK_ZB - BEAM_Z_BOT, C_STEEL, lw=0.9, z0=7)
    leader(ax, WALKWAY_RIGHT_X + 150, WALKWAY_H, WALKWAY_RIGHT_X + 150, 200,
           f"RIGHT WALKWAY GRATE DECK",
           color=C_OUT, fs=6.4, ha="center", va="bottom", arrow_style="-|>", font=FONT)
    leader(ax, BEAM_XS[0] + BEAM_W / 2, 97, BEAM_XS[0] + 60, 40,
           f"40×40 long beam\n(runs in Yd, cut) Z{BEAM_Z_BOT}–{DECK_ZB}", color=C_DIM, fs=6, ha="right",
           va="center", arrow_style="-|>", font=FONT)

    # ── Ribbon support cross-brace (welded 40×10 between the beams, top Z90) ──
    _rect(ax, CHAN_X0, RIBBON_Z - 18, CHAN_X1 - CHAN_X0, 10, C_STEEL, lw=0.7, z0=6)
    leader(ax, (CHAN_X0 + CHAN_X1) / 2, RIBBON_Z - 18, (CHAN_X0 + CHAN_X1) / 2 + 70, +60,
           "ribbon support cross-brace\n(welded 40×10, top Z90 — carries the ribbon)",
           color=C_DIM, fs=5.6, ha="right", va="top", arrow_style="-|>", font=FONT)

    # ── The four ribbon lanes IN-PLANE here, in the channel between the beams (Z104.5, flush) ──
    # At the near end the lines are still in the ribbon; each drops off-section to its wall feature.
    _ribbon_circles(ax, z=RIBBON_Z, z0=12)
    for (xx, col, tag), lz in zip(RIBBON_LANES, (225, 190, 155, 122)):
        cn = "blue" if col == C_BLUE else "brown"
        leader(ax, xx, RIBBON_Z, CHAN_X0 - 30, lz, f"{tag} ({cn})", color=col, fs=5.6,
               ha="right", va="center", arrow_style="-|>", font=FONT)
    ax.text((CHAN_X0 + CHAN_X1) / 2, RIBBON_Z + 40,
            f"4-lane ribbon\n(26mm pitch, Z{RIBBON_Z:g} — flush)", fontsize=5.4, ha="center", va="bottom",
            color=C_OUT, zorder=13, **FONT)

    # ── Clearance dimensions (the point of the section) ──────────────────────
    # pipe crown sits at the deck underside (flush) — a leader, not a dim (label rule 7).
    leader(ax, CHAN_X1 - 6, (RIBBON_Z + OD / 2 + DECK_ZB) / 2, CHAN_X1, 175,
           "pipe crown FLUSH\nwith deck underside (Z%d)" % DECK_ZB, color=C_DIM, fs=5.4,
           ha="left", va="center", arrow_style="-|>", font=FONT)
    draw_dim_v(ax, X_HI - 105, 0, WALKWAY_H, f"{WALKWAY_H}mm", offset=5, fs=5.6, font=FONT)
    draw_dim_v(ax, PROC_TRAY_X_R, PROC_TRAY_RIM, BEAM_Z_BOT, f"{BEAM_Z_BOT - PROC_TRAY_RIM}mm",
               offset=5, fs=5.4, font=FONT)
    draw_dim_h(ax, PROC_TRAY_X_R+3, IBC_COL_X, 20, f"{IBC_COL_X - PROC_TRAY_X_R}mm", offset=4, fs=5.4,
               above=False, font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        "SECTION B-B NOTES",
        "1. X–Z elevation looking +Yd near the pinhole-wall END of the ribbon (Yd≈62), where the four corridor↔pinhole-wall lines run TOGETHER as a flat ribbon under the right-walkway grate.",
        "2. The four lanes (26mm pitch, Z104.5 — FLUSH, pipe crown at the deck underside Z115) sit in the clear channel BETWEEN the two 40×40 long beams (X4369–4589), above the tray rim (Z50), tucked under the grate.",
        "3. A welded 40×10 cross-brace between the beams (top Z90) carries the ribbon at each support station.",
        "4. The two middle lanes were SWAPPED (blue TAP-01 trunk ↔ brown tray-sump) so blue/brown alternate and no longer cross into the corridor.",
        "5. Off-section (−Yd) each lane drops to its wall feature: the two blue lanes to TAP-01 / the SV-01 filtered return, the two brown lanes on toward the near-rim taps.",
    ]
    draw_notes(ax, notes, X_LO + 8, Z_HI - 60, 6.6, fs=6.2,
               font=FONT, width=225, wrap=72, border_color=C_DIM, border_lw=0.7)

    title_block(ax, "SHEET 1 OF 6",
                drawing_title="THE BIG SHOEBOX PROJECT · TBS-001",
                subtitle="WALKWAY ROUTING SECTIONS — B-B NEAR-END RIBBON")

    out = os.path.join(DIAGRAMS_DIR, "walkway-sections-sheet1.png")
    fig.savefig(out, dpi=DIAGRAM_DPI, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"Walkway section B-B (near-end ribbon) → {out}")


def sheet2():
    """SECTION C-C — midway between the pinhole wall and the corridor (Yd≈450), X–Z, looking +Yd.

    The SAME cut as B-B, moved to mid-tray depth, at a ribbon support station (Yd450).  The
    four ribbon lanes run IN-PLANE here (four cross-section circles in the channel between the
    walkway long beams, at Z104.5 (FLUSH, crown at the deck underside) — above the tray/wash water, under the grate), carried by a
    welded cross-brace.  Confirms the sanctioned routing: the ribbon passes ABOVE the tray,
    under the grate, clear of the print/water — it never sits in the basin.
    """
    from tbs_constants import PROC_TRAY_X_R as TXR
    Y_CUT = 450   # on a ribbon support station (cp.RIBBON_SUP_YD)
    X_LO, X_HI = 4185, 4770
    Z_LO, Z_HI = -75, 475   # taller header band so the notes box clears the centered subtitle

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
        _rect(ax, bx, BEAM_Z_BOT, BEAM_W, DECK_ZB - BEAM_Z_BOT, C_STEEL, lw=0.9, z0=7)
    leader(ax, WALKWAY_RIGHT_X + 150, WALKWAY_H, WALKWAY_RIGHT_X + 150, 200,
           f"RIGHT WALKWAY GRATE DECK",
           color=C_OUT, fs=6.4, ha="center", va="bottom", arrow_style="-|>", font=FONT)

    # IBC-3 tote (beyond the gap)
    _rect(ax, IBC_COL_X, 0, X_HI - IBC_COL_X, Z_HI - Z_LO, C_IBC_B, ec=C_OUT, lw=1.0, z0=6, alpha=0.42)
    ax.text((IBC_COL_X + X_HI) / 2, 330, "IBC-3\n(Brown)\n↑ tote", fontsize=8, ha="center", va="center",
            color="white", fontweight="bold", zorder=8, **FONT)

    # ── Ribbon support cross-brace (welded 40×10 between the beams, top Z90 — this cut is on a station) ──
    _rect(ax, CHAN_X0, RIBBON_Z - 18, CHAN_X1 - CHAN_X0, 10, C_STEEL, lw=0.7, z0=6)
    leader(ax, (CHAN_X0 + CHAN_X1) / 2, RIBBON_Z - 18, (CHAN_X0 + CHAN_X1) / 2 + 70, +60,
           "ribbon support cross-brace\n(welded 40×10, top Z90 — carries the ribbon)",
           color=C_DIM, fs=5.6, ha="right", va="top", arrow_style="-|>", font=FONT)

    # ── The four ribbon lanes IN-PLANE here (they run the length under the grate) ──
    _ribbon_circles(ax, z=RIBBON_Z, z0=12)
    # Labels pulled LEFT into the clear zone above the tray, never over the IBC-3 tote.
    for (xx, col, tag), lz in zip(RIBBON_LANES, (225, 190, 155, 122)):
        cn = "blue" if col == C_BLUE else "brown"
        leader(ax, xx, RIBBON_Z, CHAN_X0 - 30, lz, f"{tag} ({cn})", color=col, fs=5.6,
               ha="right", va="center", arrow_style="-|>", font=FONT)
    ax.text((CHAN_X0 + CHAN_X1) / 2, RIBBON_Z + 40,
            f"4-lane ribbon\n(26mm pitch, Z{RIBBON_Z:g} — flush)", fontsize=5.4, ha="center", va="bottom",
            color=C_OUT, zorder=13, **FONT)

    # pipe crown sits at the deck underside (flush) — a leader, not a dim (label rule 7).
    leader(ax, CHAN_X1 - 6, (RIBBON_Z + OD / 2 + DECK_ZB) / 2, CHAN_X1, 175,
           "pipe crown FLUSH\nwith deck underside (Z%d)" % DECK_ZB, color=C_DIM, fs=5.4,
           ha="left", va="center", arrow_style="-|>", font=FONT)
    draw_dim_v(ax, PROC_TRAY_X_R, PROC_TRAY_RIM, BEAM_Z_BOT, f"{BEAM_Z_BOT - PROC_TRAY_RIM}mm",
               offset=5, fs=5.4, font=FONT)
    draw_dim_v(ax, X_HI - 105, 0, WALKWAY_H, f"{WALKWAY_H}mm", offset=5, fs=5.6, font=FONT)
    draw_dim_h(ax, TXR+3, IBC_COL_X, 20, f"{IBC_COL_X - TXR}mm", offset=4, fs=5.4, above=False, font=FONT)

    notes = [
        "SECTION C-C NOTES",
        "1. SAME cut as B-B (X–Z, looking +Yd), moved to mid-depth (Yd≈450), halfway between the pinhole wall and the plumbing corridor, at a ribbon support station.",
        "2. Here the plane is INSIDE the processing tray — the basin + wash water are cut; the walkway deck spans over the tray.",
        "3. The four ribbon lanes (Z104.5 flush, 26mm pitch) run IN-PLANE here, in channel BETWEEN the long beams (X4369–4589) — a SANCTIONED pass ABOVE the tray rim, under the grate, clear of the print/water.",
        "4. A welded 40×10 cross-brace (top Z90) carries the ribbon at this station.  The lanes read as RUNS the length of B-B → C-C → D-D.",
    ]
    draw_notes(ax, notes, X_LO + 8, Z_HI - 66, 6.6, fs=6.2,
               font=FONT, width=225, wrap=72, border_color=C_DIM, border_lw=0.7)

    title_block(ax, "SHEET 2 OF 6",
                drawing_title="THE BIG SHOEBOX PROJECT · TBS-001",
                subtitle="WALKWAY ROUTING SECTIONS — C-C MIDWAY")

    out = os.path.join(DIAGRAMS_DIR, "walkway-sections-sheet2.png")
    fig.savefig(out, dpi=DIAGRAM_DPI, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
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

    # Here the deep-box uprights + IBC ghost rise to the top of the drawing area, so an
    # in-axes title (at Z_HI) would be overlapped by the geometry. Place title/subtitle in
    # the figure margin ABOVE the axes instead (axes top = 0.06 + 0.87 = 0.93).
    _tcx = 0.07 + 0.89 / 2   # horizontal center of the axes in figure coords
    fig.text(_tcx, 0.972, "SECTION D-D · THROUGH THE NEAR CANTILEVER",
             ha="center", va="top", fontsize=11, fontweight="bold", color=C_OUT, **FONT)
    fig.text(_tcx, 0.945, "X–Z elevation, looking along +Yd at Yd≈1066 (near cantilever arm / IBC upright) · 1:1",
             ha="center", va="top", fontsize=7.5, color=C_DIM, **FONT)

    # floor
    _rect(ax, X_LO, -40, X_HI - X_LO, 40, C_FLOOR, lw=1.0, hatch="////", z0=2)

    # processing tray — CUT here (Yd1066 is inside the tray Yd80-2280): basin floor + wash water + RIGHT-END RIM
    tx_l = max(X_LO, PROC_TRAY_X_L)
    _rect(ax, tx_l, 0, PROC_TRAY_X_R - tx_l, 3, C_TRAY, lw=0.9, z0=4)                       # basin floor
    _rect(ax, tx_l, 3, PROC_TRAY_X_R - 4 - tx_l, PROC_TRAY_RIM - 8, "#BFD8EA", ec="none", z0=3, alpha=0.55)  # wash water
    _rect(ax, PROC_TRAY_X_R - 4, 0, 4, PROC_TRAY_RIM, C_TRAY, lw=1.0, z0=5)                 # RIGHT-END RIM (4mm wall, inner face of X4629, Z0-50)
    leader(ax, PROC_TRAY_X_R - 2, PROC_TRAY_RIM, PROC_TRAY_X_R - 25, PROC_TRAY_RIM + 10,
           f"processing tray right-end rim", color="#3C5A6E",
           fs=5.8, ha="right", va="bottom", arrow_style="-|>", font=FONT)

    # IBC-3 tote (behind this plane, Yd≤1046) — ghost
    _rect(ax, IBC_COL_X, 0, X_HI - IBC_COL_X, Z_HI - Z_LO, C_IBC_B, ec=C_GHOST, lw=0.9, z0=1, alpha=0.10, ls="--")
    ax.text((IBC_COL_X + X_HI) / 2, 660, "IBC-3 tote", fontsize=6, ha="center",
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
    leader(ax, 4500, ARM_ZB, 4358, 55,
           "walkway support: cantilever arm (Z70–115)\n+ long bearers (Z80–115, hatched)\n[arm clamps to the deep-box upright X4654]",
           color="#3A3A40", fs=5.2, ha="left", va="top", arrow_style="-|>", font=FONT)
    leader(ax, WALKWAY_RIGHT_X + 90, WALKWAY_H, 4200, 210, "right walkway grate deck",
           color=C_OUT, fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)

    # ── Deep-box FRONT upright + front foot (extends UNDER the tray) + M12 + bottom rail + retaining bar ──
    _rect(ax, UP_X0, 0, UP_X1 - UP_X0, Z_HI - Z_LO, C_STEEL, lw=1.0, z0=6)                  # front upright X4654-4704
    _rect(ax, BRAIL_X0, 0, X_HI - BRAIL_X0, BRAIL_Z, C_STEEL, lw=0.9, z0=5)                 # deep-box bottom ring rail (→X5104)
    _rect(ax, FOOT_X0, 0, FOOT_X1 - FOOT_X0, FOOT_ZT, C_STEEL, lw=0.9, z0=8)                # front foot (X4604-4754, under tray)
    for mx in M12_XS:
        _rect(ax, mx - 6, 0, 12, 16, "#6A6A72", lw=0.5, z0=9)
    _rect(ax, RAIL_X0, RAIL_ZB, RAIL_X1 - RAIL_X0, RAIL_ZT - RAIL_ZB, C_STEEL, lw=0.9, z0=7)  # retaining bar Z560
    leader(ax, (UP_X0 + UP_X1) / 2, 500, UP_X1 + 22, 540, "corridor deep-box FRONT upright\n(50×50 RHS, X4654)",
           color=C_DIM, fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)
    leader(ax, FOOT_X0 + 16, FOOT_ZT, PROC_TRAY_X_R - 175, 35,
           "front floor foot 150×150×12 + 4× M12 —\nLEFT EDGE (X4604) EXTENDS 25mm UNDER THE TRAY",
           color="#B03030", fs=5.5, ha="left", va="top", arrow_style="-|>", font=FONT)
    leader(ax, X_HI - 60, BRAIL_Z, X_HI - 40, 92, "bottom ring rail (Z0–50)",
           color=C_DIM, fs=5.6, ha="right", va="center", arrow_style="-|>", font=FONT)
    leader(ax, (RAIL_X0 + RAIL_X1) / 2, RAIL_ZT, RAIL_X1 + 24, RAIL_ZT + 40,
           "retaining bar (ring rail) Z560", color=C_DIM, fs=6, ha="left", va="center",
           arrow_style="-|>", font=FONT)

    # ── The RIBBON LOOPS UP OVER the cantilever here — 4 lanes at the crest (Z142), clearing the arm ──
    # At Yd≈1066 (mid-cantilever) the ribbon has risen through the grate (at Yd1000) and crests at
    # RIBBON_OVER_Z, passing OVER the arm top (Z115) / grate (Z130) — never through the steel (Rule 5).
    _ribbon_circles(ax, z=RIBBON_OVER_Z, z0=12)
    ax.text((CHAN_X0 + CHAN_X1) / 2, RIBBON_OVER_Z + OD, "4-lane ribbon LOOPING OVER\nthe cantilever (crest Z142)",
            fontsize=5.6, ha="center", va="bottom", color=C_OUT, fontweight="bold", zorder=13, **FONT)
    for (xx, col, tag), lz in zip(RIBBON_LANES, (430, 390, 300, 260)):
        cn = "blue" if col == C_BLUE else "brown"
        leader(ax, xx, RIBBON_OVER_Z, CHAN_X0 + 30, lz - 100, f"{tag} ({cn})", color=col, fs=5.4,
               ha="right", va="center", arrow_style="-|>", font=FONT)
    # crest clears the arm top
    draw_dim_v(ax, CHAN_X1 + 60, ARM_ZT, RIBBON_OVER_Z - OD / 2, f"{int(RIBBON_OVER_Z - OD/2 - ARM_ZT)}mm\nover arm top",
               offset=5, fs=5.2, font=FONT)
    # past the cantilever each lane comes back to FLUSH and crosses the OPEN corridor bay (no outer beam) into the corridor
    ax.text((UP_X1 + X_HI) / 2, 235, "(past the cantilever the lanes stay\nFLUSH, cross the OPEN corridor bay\n(no outer beam between the arms),\nthen drop the tray-edge slot — in-plane in E-E)",
            fontsize=5.0, ha="center", va="center", color=C_DIM, zorder=10, **FONT)

    # ── Dimensions ───────────────────────────────────────────────────────────
    draw_dim_v(ax, X_HI - 34, BRAIL_Z, RAIL_ZB, f"{RAIL_ZB - BRAIL_Z}mm\n(rail→rail)", offset=5, fs=5.4, font=FONT)
    draw_dim_v(ax, ARM_X0 - 22, 0, ARM_ZB, f"{ARM_ZB}mm\nunder arm", offset=5, fs=5.4, font=FONT)
    draw_dim_h(ax, PROC_TRAY_X_R, UP_X0, 30, f"{UP_X0 - PROC_TRAY_X_R}mm gap\n(rim→upright)", offset=4, fs=5.2, above=False, font=FONT)

    notes = [
        "SECTION D-D NOTES  (frame = water.skp deep-box cp.frame())",
        "1. X–Z cut through the NEAR cantilever (Yd≈1066).  The corridor restraint is the DEEP 4-leg box: FRONT upright X4654, front foot 150×150 at X4604–4754 — its LEFT EDGE sits 25mm UNDER the tray.",
        "2. The four-lane ribbon LOOPS UP OVER the cantilever here: it rose through the grate at Yd1000 and crests at Z142 (RIBBON_OVER_Z), passing OVER the arm top (Z115) and grate (Z130) — never through the steel (Rule 5).  It drops back through the grate past Yd1120.",
        "3. No pipe threads the tray-rim↔upright gap at this plane — the old low-crosser pinch is designed out by the loop-over.",
        "4. Past the cantilever each lane stays FLUSH (Z104.5) and crosses the OPEN corridor bay (Yd~1097–1266) — the outer beam is omitted between the two cantilever arms, so there is no beam to cross — then drops the tray-edge slot (X4629–4654, clear of the carriage) into the corridor — in-plane in E-E.",
        "5. STATUS: (a) front foot / M12 CLEARS under the raised tray pan; (b) RWK cantilever arm reconciled to the deep-box upright (X4654); (c) the ribbon crest clears the arm top — no soffit graze; (d) the flush ribbon clears the spray-carriage crown (Z66) by ~28mm.",
    ]
    draw_notes(ax, notes, X_LO + 8, Z_HI - 60, 7.6, fs=6.2,
               font=FONT, width=285, wrap=72, border_color=C_DIM, border_lw=0.7)

    title_block(ax, "SHEET 3 OF 6",
                drawing_title="THE BIG SHOEBOX PROJECT · TBS-001",
                subtitle="WALKWAY ROUTING SECTIONS — D-D NEAR CANTILEVER")

    out = os.path.join(DIAGRAMS_DIR, "walkway-sections-sheet3.png")
    fig.savefig(out, dpi=DIAGRAM_DPI, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"Walkway section D-D (near cantilever) → {out}")


def _clean_name(nm):
    """Tidy a captured 3D pipe name for the legend."""
    nm = nm.replace(" (off-panel)", "").replace(" entry", "").replace(" (in)", " IN")
    nm = nm.replace(" -> ", " → ").replace("(single filtered line)", "(filtered)")
    return nm.strip()


def sheet4():
    """CORRIDOR PLUMBING ELEVATION E-E — the REAL 3D corridor routing (every pipe in the pump-column
    bay) projected into the X–Z plane, looking +Yd.  Paths are captured LIVE from the water.skp
    builders, so the elevation can never drift from the 3D model; pure-Yd (into-page) moves collapse."""
    X_LO, X_HI = CORR_X_LO, CORR_X_HI
    runs = _capture_corridor_pipes()                                     # REAL 3D paths, projected (captured live)
    _zmax = max(p[1] for _n, xz, _c in runs for p in xz)
    Z_LO, Z_HI = -60, _zmax + 110      # floor hatch at −40..0; top margin above the tallest riser (the title block sits in its own full-width strip below, not reserved inside the drawing)
    fig = plt.figure(figsize=(16.5, 12.0))
    ax = fig.add_axes([0.035, 0.11, 0.60, 0.84])     # drawing on the left; legend/notes in the right margin; a full-width title-block strip spans below both
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI); ax.set_ylim(Z_LO, Z_HI); ax.set_aspect("equal"); ax.axis("off")
    fig.text(0.035, 0.975, "ELEVATION E-E · CORRIDOR PLUMBING (pump-column bay)",
             ha="left", va="top", fontsize=13, fontweight="bold", color=C_OUT, **FONT)
    fig.text(0.035, 0.955, "X–Z projection looking +Yd · every real corridor run, captured from the 3D model · 1:1",
             ha="left", va="top", fontsize=8, color=C_DIM, **FONT)

    # ── structural context ──
    _rect(ax, X_LO, -40, X_HI - X_LO, 40, C_FLOOR, lw=1.0, hatch="////", z0=2)                 # floor
    _rect(ax, X_LO, DECK_ZB, PROC_TRAY_X_R - X_LO, WALKWAY_GRATE_T, C_GRATE, lw=1.0, z0=3)      # walkway deck edge (−X)
    _BASE, _RHS = cp.FRAME_BASE_Z, cp.ov.IBC_FRAME_RHS
    _FRW, _FRH = cp.ov.IBC_FRONT_RAIL_W, cp.ov.IBC_FRONT_RAIL_H
    _rect(ax, cp.FRONT_RAIL_CX - _FRW / 2, _BASE, _FRW, _FRH, C_STEEL, lw=0.9, z0=4)            # front bottom Yd-rail (top Z55)
    _rect(ax, cp.BACK_X, _BASE, _RHS, _RHS, C_STEEL, lw=0.9, z0=4)                              # back bottom Yd-rail (top Z70.8)
    # frame uprights + rear panel + pump column, ghosted (just outside / behind the pipes)
    for ux in (UP_X0, cp.BACK_X):
        _rect(ax, ux, _BASE, _RHS, Z_HI - 120 - _BASE, C_GHOST, ec=C_GHOST, lw=0.8, z0=1, alpha=0.14, ls="--")
    _ghost_top = Z_HI - 110
    _rect(ax, cp.BACK_X, _BASE, 18, _ghost_top - _BASE, C_GHOST, ec="none", z0=1, alpha=0.08)   # rear panel ply
    _rect(ax, 4934, _BASE, 100, _ghost_top - _BASE, C_GHOST, ec=C_GHOST, lw=0.8, z0=1, alpha=0.10, ls="--")  # pump column (P-01/04/05/03 + ACC)
    ax.text(4984, _ghost_top - 70, "pump column\n(P-01·P-04·P-05·P-03\n+ ACC-01) ghost", fontsize=5.0,
            ha="center", va="top", color=C_GHOST, zorder=2, **FONT)
    ax.text(UP_X0 - 4, _ghost_top, "front\nupright", fontsize=4.8, ha="right", va="top", color=C_GHOST, **FONT)
    ax.text(cp.BACK_X + 60, _ghost_top, "back upright\n+ rear panel", fontsize=4.8, ha="left", va="top", color=C_GHOST, **FONT)

    # ── the REAL corridor pipe routing, projected from the 3D (captured live) ──
    _draw_lanes(ax, [(xz, _CORRIDOR_COL.get(col, C_DIM)) for _nm, xz, col in runs])

    # number runs in LEGEND order (blue → brown → gray) so both the tags and the legend read 1..N
    order = {C_BLUE: 0, C_BROWN: 1, C_WASTE: 2}
    leg = sorted(range(len(runs)), key=lambda j: (order.get(_CORRIDOR_COL.get(runs[j][2], C_DIM), 3), j))
    numof = {j: k + 1 for k, j in enumerate(leg)}

    # numbered callouts: anchor each tag at the MIDPOINT of its run's longest in-window segment
    # (its most prominent length), falling back to shorter segments if that collides with a placed tag
    placed = []
    for j, (nm, xz, col) in enumerate(runs):
        segs = sorted(zip(xz[:-1], xz[1:]),
                      key=lambda s: -((s[0][0] - s[1][0]) ** 2 + (s[0][1] - s[1][1]) ** 2))
        mids = [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in segs
                if X_LO + 14 <= (a[0] + b[0]) / 2 <= X_HI - 14] or [xz[len(xz) // 2]]
        anchor = next((m for m in mids if all((m[0] - q[0]) ** 2 + (m[1] - q[1]) ** 2 > 30 ** 2 for q in placed)), mids[0])
        placed.append(anchor)
        ax.text(anchor[0], anchor[1], str(numof[j]), fontsize=5.0, ha="center", va="center", zorder=30,
                color="white", fontweight="bold",
                bbox=dict(boxstyle="circle,pad=0.16", fc=_CORRIDOR_COL.get(col, C_DIM), ec="white", lw=0.5), **FONT)

    # ── legend (right margin): numbered 1..N, grouped by color/system ──
    lx = 0.555
    fig.text(lx, 0.93, "CORRIDOR RUNS (→ pump column / end wall)", fontsize=8.5,
             fontweight="bold", color=C_OUT, **FONT)
    y = 0.905
    for j in leg:
        nm, xz, col = runs[j]
        mc = _CORRIDOR_COL.get(col, C_DIM)
        fig.text(lx, y, "●", fontsize=8, color=mc, va="center", **FONT)
        fig.text(lx + 0.016, y, f"{numof[j]}. {_clean_name(nm)}", fontsize=6.3, color=C_OUT, va="center", **FONT)
        y -= 0.0185
    y -= 0.010
    for line in [
        "HOW TO READ THIS SHEET",
        "• X–Z projection looking +Yd: a run going INTO the page (a pure-Yd",
        "  move, e.g. a riser stepping to its port lane) collapses to a point,",
        "  so a vertical here is a real Z rise and a horizontal a real X run.",
        "• Crossings read as over/unders (rear pipe breaks at the front wall);",
        "  blue in front, then brown, then gray waste — a drawing convention,",
        "  NOT a depth statement (true depth is the Yd the projection drops).",
        "• Captured live from the water.skp builders — this elevation tracks",
        "  the 3D model automatically and cannot drift from it.",
        "• The pump column, uprights + rear panel are ghosted context; the",
        "  bottom Yd-rails float on the Z20 sub-plate + foot-plate stack.",
    ]:
        bold = not line.startswith("•")
        fig.text(lx, y, line, fontsize=7.2 if bold else 6.4, fontweight="bold" if bold else "normal",
                 color=C_OUT if bold else C_DIM, va="top", **FONT)
        y -= 0.019 if bold else 0.016

    # Title block on its OWN full-width strip so it spans the used width (drawing + legend),
    # rather than shrinking to the tall-narrow drawing axes and stranding the key beside it.
    tb_ax = fig.add_axes([0.035, 0.015, 0.825, 0.075]); tb_ax.axis("off")
    tb_ax.set_xlim(0, 1); tb_ax.set_ylim(0, 1)
    title_block(tb_ax, "SHEET 4 OF 6", drawing_title="THE BIG SHOEBOX PROJECT · TBS-001",
                subtitle="WALKWAY ROUTING SECTIONS — E-E CORRIDOR PLUMBING ELEVATION", height=0.62)
    out = os.path.join(DIAGRAMS_DIR, "walkway-sections-sheet4.png")
    fig.savefig(out, dpi=DIAGRAM_DPI, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"Walkway elevation E-E (corridor plumbing) → {out}")


def sheet5():
    """SECTION F-F — through the FAR cantilever (Yd≈1286), X–Z looking +Yd.  Mirror of D-D:
    the far cantilever arm + far upright + far foot (also under the tray).  The ribbon loops
    over the NEAR cantilever only; the blue SV-01 → DV-01 return corridor lane (Yd1241) is the
    nearest line, ghosted just -Yd."""
    X_LO, X_HI = 4245, 4880
    Z_LO, Z_HI = -80, 720
    fig = plt.figure(figsize=(12.5, 12.5))
    ax = fig.add_axes([0.07, 0.06, 0.89, 0.87])
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI); ax.set_ylim(Z_LO, Z_HI); ax.set_aspect("equal"); ax.axis("off")
    # Far upright + IBC ghost rise to the top of the drawing area, so place the title/
    # subtitle in the figure margin ABOVE the axes (axes top = 0.06 + 0.87 = 0.93).
    _tcx = 0.07 + 0.89 / 2   # horizontal center of the axes in figure coords
    fig.text(_tcx, 0.972, "SECTION F-F · THROUGH THE FAR CANTILEVER",
             ha="center", va="top", fontsize=11, fontweight="bold", color=C_OUT, **FONT)
    fig.text(_tcx, 0.945, "X–Z elevation, looking along +Yd at Yd≈1286 (far cantilever arm / IBC upright) · 1:1",
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
    ax.text((IBC_COL_X + X_HI) /2, 680, "IBC-4 tote", fontsize=6, ha="center", va="center", color=C_GHOST, zorder=2, **FONT)
    # available routing space (corridor past the upright)
    _rect(ax, UP_X1, BRAIL_Z, X_HI - UP_X1, RAIL_ZB - BRAIL_Z, "#DCEFDD", ec="#6FAF72", lw=0.8, z0=3, alpha=0.5, ls=(0, (4, 2)))
    ax.text((UP_X1 + X_HI) / 2, 340, "AVAILABLE ROUTING\nSPACE (corridor)", fontsize=6.2, ha="center", va="center", color="#3C7A40", fontweight="bold", zorder=4, **FONT)
    # far cantilever arm + long bearers + deck
    _rect(ax, ARM_X0, ARM_ZB, ARM_X1 - ARM_X0, ARM_ZT - ARM_ZB, C_STEEL, lw=1.0, z0=6)
    for bx in BEAM_XS:
        _rect(ax, bx, 80, BEAM_W, DECK_ZB - 80, C_STEEL, ec="#3A3A40", lw=1.0, z0=6, hatch="\\\\\\\\")
    _rect(ax, WALKWAY_RIGHT_X, DECK_ZB, WALKWAY_RIGHT_W, WALKWAY_GRATE_T, C_GRATE, lw=1.0, z0=7)
    leader(ax, 4500, ARM_ZB, 4358, 60, "walkway support: far cantilever arm (Z70–115)\n+ long bearers (Z80–115, hatched)", color="#3A3A40", fs=5.2, ha="left", va="top", arrow_style="-|>", font=FONT)
    leader(ax, WALKWAY_RIGHT_X + 90, WALKWAY_H, 4358, 175, "right walkway grate deck (Z115–130)", color=C_OUT, fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)
    # far upright + far foot (also under tray) + M12 + bottom rail + retaining bar
    _rect(ax, UP_X0, 0, UP_X1 - UP_X0, Z_HI - Z_LO, C_STEEL, lw=1.0, z0=6)                     # far upright X4654-4704
    _rect(ax, BRAIL_X0, 0, X_HI - BRAIL_X0, BRAIL_Z, C_STEEL, lw=0.9, z0=5)                    # bottom ring rail
    _rect(ax, FOOT_X0, 0, FOOT_X1 - FOOT_X0, FOOT_ZT, C_STEEL, lw=0.9, z0=8)                   # far foot (under tray)
    for mx in M12_XS:
        _rect(ax, mx - 6, 0, 12, 16, "#6A6A72", lw=0.5, z0=9)
    _rect(ax, RAIL_X0, RAIL_ZB, RAIL_X1 - RAIL_X0, RAIL_ZT - RAIL_ZB, C_STEEL, lw=0.9, z0=7)   # retaining bar
    leader(ax, (UP_X0 + UP_X1) / 2, 500, UP_X1 + 22, 540, "corridor deep-box FAR upright\n(50×50 RHS)", color=C_DIM, fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)
    leader(ax, FOOT_X0 + 16, FOOT_ZT, PROC_TRAY_X_R - 150, 35, "far floor foot 150×150×12 —\nLEFT EDGE EXTENDS 25mm UNDER THE TRAY", color="#B03030", fs=5.5, ha="left", va="top", arrow_style="-|>", font=FONT)
    leader(ax, (RAIL_X0 + RAIL_X1) / 2, RAIL_ZT, RAIL_X1 + 54, RAIL_ZT + 40, "retaining bar (ring rail)", color=C_DIM, fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)
    # nearest corridor lane (blue SV-01 → DV-01 return, Yd1241) — ghost, -Yd of this plane
    ax.add_patch(Circle((4772, 235), OD / 2, facecolor="none", edgecolor=C_BLUE, lw=1.4, ls="--", zorder=9))
    ax.text(4772, 219, "blue SV-01 → DV-01 return\n(Yd1241, ghost, −Yd)", fontsize=4.8, ha="center", va="top", color=C_BLUE, zorder=10, **FONT)

    notes = [
        "SECTION F-F NOTES",
        "1. Far cantilever (Yd≈1286) — mirrors D-D on the far side of the corridor: arm off the FAR IBC upright (X4654), foot X4604–4754 again extending 25mm UNDER the tray.",
        "2. The ribbon loops over the NEAR cantilever only and drops into the corridor by Yd1120 — no line crosses this far cantilever.",
        "3. The nearest corridor lane is the blue SV-01 → DV-01 return (Yd1241), just −Yd of this plane — ghosted.  See E-E for the lanes in-plane.",
    ]
    draw_notes(ax, notes, X_LO + 8, Z_HI - 60, 7.4, fs=6.0,
               font=FONT, width=280, wrap=72, border_color=C_DIM, border_lw=0.7)
    title_block(ax, "SHEET 5 OF 6", drawing_title="THE BIG SHOEBOX PROJECT · TBS-001",
                subtitle="WALKWAY ROUTING SECTIONS — F-F FAR CANTILEVER")
    out = os.path.join(DIAGRAMS_DIR, "walkway-sections-sheet5.png")
    fig.savefig(out, dpi=DIAGRAM_DPI, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
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
    axA.text(YL + 20, zx(-14), "container floor", fontsize=6, ha="left", va="center", color=C_DIM, bbox=LBL_BG, **FONT)
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
    leader(axA, PROC_TRAY_YD_NEAR + PROC_TRAY_SUMP_W / 2, zx(4), PROC_TRAY_YD_NEAR + 20, zx(46),
           f"corner SUMP (low point) — well {PROC_TRAY_SUMP_Z}mm deep,\nbottom rests ON the container floor (Z0)",
           color="#2A6", fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)
    leader(axA, 1500, zx(ptop[26] - 1), 1500, zx(ptop[26] + 22),
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
    axB.add_patch(Rectangle((cx - 40, zx(fz)), 150, zx(top_new - fz), fc="#C9D6E4", ec=C_OUT, lw=1.1, zorder=9))
    axB.text(cx + 125, zx(fz + (top_new - fz) / 2), "Ø32 wheels +\n40×25 SS beam", fontsize=5.6,
             ha="left", va="center", color=C_OUT, **FONT)
    # clearance dimension (new)
    draw_dim_v(axB, cx, zx(top_new), zx(DECK_ZB), f"{DECK_ZB - top_new:.0f}mm CLEAR", offset=3, fs=7, right=True, font=FONT)
    leader(axB, PROC_TRAY_X_L + 3, zx(ttop[0] + PROC_TRAY_RIM), PROC_TRAY_X_L + 480, zx(ttop[0] + PROC_TRAY_RIM + 26),
           f"pan/rim highest at the far-left corner\n(floor Z{ttop[0]:.0f}, rim top Z{tray_rim_top_z(PROC_TRAY_X_L, ydc):.0f})",
           color="#3C5A6E", fs=6, ha="left", va="center", arrow_style="-|>", font=FONT)

    axTB = fig.add_axes([0.07, 0.005, 0.90, 0.05])
    axTB.set_xlim(0, 1); axTB.set_ylim(0, 1); axTB.axis("off")
    # title_block's `height` is an axes-FRACTION; this is a dedicated thin axes, so fill it
    # (default 0.045 would be 0.045 of an already-thin axes and collapse the block).
    title_block(axTB, "SHEET 6 OF 6", height=0.9,
                drawing_title="THE BIG SHOEBOX PROJECT · TBS-001",
                subtitle="WALKWAY ROUTING SECTIONS — G-G TRAY SLOPE/SUPPORT · H-H CARRIAGE CLEARANCE")
    out = os.path.join(DIAGRAMS_DIR, "walkway-sections-sheet6.png")
    fig.savefig(out, dpi=DIAGRAM_DPI, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
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
