#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""generate_corridor_water_panel.py — EXPLORATORY (pinhole-wall-mount branch).

The NEW corridor plumbing panel.  Starts from the deep-box IBC restraint/equipment frame
as it stood at the fork, but with ONLY the REAR (far-wall) panel — the left/waste-wall
panel is gone (the filters moved to the pinhole wall).  The four returned pumps
(P-01/P-03/P-04/P-05) + ACC-01 and the Stage-A tray-drain chain (SV-02 + DV-02) will mount
on the rear panel facing the operator (added next).  Reuses generate_sketchup_model helpers.

    python3 src/models/generate_corridor_water_panel.py --send --save   # build into the ACTIVE (blank) doc, save corridor-panel.skp
"""
import sys, os, argparse
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, _HERE)
import generate_sketchup_model as ov

# ── deep-box frame geometry (from the fork; one source) ──
S       = ov.IBC_FRAME_RHS               # 50×50 RHS
TOP_Z   = 2 * ov.IBC_H_1000 - 40         # 2296 — frame reaches near the stack top
# Equipment-panel top — DROPPED to the underside of the Fan A exhaust baffle so the corridor is
# open across the fan window (Z1900-2100), letting air pass THROUGH the panel to Fan A.  Tied to
# the fan so it can't drift (was DV_Z+DVB=2191, a stale Phase-1 tie to the now-relocated DV-02).
PANEL_TOP_Z = ov.FAN_A_H - ov.DUCT_HEIGHT // 2   # 1900 — fan-baffle underside
YD_NEAR, YD_FAR = 1046, 1316             # plumbing-corridor edges
FRONT_X = ov.IBC_COL_X - 20              # 4654 — front uprights on the wall-bar line
DEPTH   = 450                            # deep box (≈⅓ tote depth)
BACK_X  = FRONT_X + DEPTH                 # 5104 — the REAR panel plane (pumps mount here, face -X)
EQT     = ov.EQPANEL_T                    # 18mm ply
C_BOLT  = "#3A3A42"
C_HANDLE = "#C0202A"                      # red diverter handle

# ── Under-walkway pipe RIBBON (rev11) ────────────────────────────────────────
# The four corridor↔pinhole-wall lines (brown→P-02, blue filter return, brown sump
# pickup, blue→TAP-01) used to stack at different Z in the congested tray↔IBC gap
# (choked by the deep-box feet + the two cantilever arms).  They now run as a FLAT
# RIBBON — side-by-side in X, hugged to the tray's outer/right rim — in the dead space
# UNDER the right-walkway grate.  At the first cantilever (nearest the pinhole wall) each
# lane makes a staggered turn to a grate SLOT on the IBC edge, rises through it, and turns
# into the corridor.  ribbon_run() returns the traverse; callers add each line's end stubs.
RIBBON_Z       = ov.WALKWAY_H - ov.WALKWAY_GRATE_T - ov.PUMP_PIPE_OD / 2   # 104.5 — FLUSH: pipe crown at the
#   deck underside (Z115).  RAISED from the old Z98 so the corridor exit never has to dip toward the tray floor —
#   the whole over-tray run now clears the spray-carriage crown (Z66) by ~28mm the entire way to the corridor.
# 4 flat ribbon lanes, DERIVED to sit evenly in the clear channel BETWEEN the walkway long beams (inner
# outboard face .. outer inboard face). Was hardcoded [4556,4530,4504,4478] for the OLD wider channel;
# F1 shortened the right walkway (outer beam 4629→4574), narrowing the channel to ~143mm, so lanes 0/1
# clashed the moved beam — deriving keeps all 4 clear of BOTH beams for good (Alvin 2026-08-18).
_LANE_R, _LANE_CLR = 10.5, 10                                   # OD21 ribbon radius / min gap from each beam face
_ch_out = ov.RWK_X_R - ov.RWK_BEARER_W - _LANE_CLR - _LANE_R    # outermost lane centre (off the outer-beam inboard face)
_ch_in  = ov.RWK_X_L + ov.RWK_BEARER_W + _LANE_CLR + _LANE_R    # innermost lane centre (off the inner-beam outboard face)
RIBBON_LANE_X  = [round(_ch_out - i * (_ch_out - _ch_in) / 3) for i in range(4)]   # ~[4503,4469,4434,4400], index-matched to RWK_RIBBON_NOTCH_YDS
RIBBON_YD_UP   = 1000                           # up-through-grate Yd — just BEFORE the first cantilever (Yd1046-1086)
RIBBON_YD_DOWN = 1110                           # down-through-grate Yd — just PAST the cantilever (Yd1086); = lane-0 crest far-end (RWK_RIBBON_NOTCH_YDS[0]) so the sump over-crest length matches pipe 1 (Alvin 2026-07-24)
RIBBON_OVER_Z  = ov.WALKWAY_H + 12              # 142 — loop crest, just above the grate (130) / cantilever top (115) — kept low
RIBBON_SUP_YD  = [200, 450, 700, 950]           # welded cross-beam supports along the under-grate ribbon span
# Corridor exit: the flush ribbon crosses the OUTER long beam (X4589-4629, Z80-115) through an OPEN-TOP NOTCH at
# each lane (the beam's grate-bearing web is kept; a shallow slot from the top clears the OD21 pipe at RIBBON_Z),
# stays flush PAST the tray edge, and only THEN drops down the tray-edge↔upright slot (clear of the carriage,
# which ends at X4599) into the corridor.  A flush under-beam crossing is impossible — the carriage crown (Z66)
# to beam soffit (Z80) gap is 14mm < the 21mm pipe — so the beam is notched rather than the pipe dipped.
RIBBON_BEAM_X  = (ov.RWK_X_R - 40, ov.RWK_X_R)  # 4589-4629 — outer long beam span (the notched member)
RIBBON_SLOT_X  = ov.PROC_TRAY_X_R + 12          # 4641 — drop lane in the tray-edge↔upright gap (X4629-4654,
#   clear Z16-150), PAST the carriage travel (X≤4599); each corridor exit drops here, never over the tray.
BLUE_TRUNK_HANDOFF_X = ov.RAIL_X_R + 21         # 4670 — where the corridor blue trunk drops to meet the ribbon:
#   PAST the film-plane bottom rail (a 40×40 tube ending at RAIL_X_R=4649) by a pipe radius + ~10mm, so the
#   vertical drop clears the FP rail (the old X4660 grazed the rail edge by 0.5mm).  ribbon_run(1) picks up here.

def ribbon_run(i, corridor_pt, near_pt, up_yd=None):
    """Waypoints for ribbon lane i (0..3), from the CORRIDOR connection (X in the corridor, past
    the tray edge) to the pinhole-wall (near-rim) connection.  On the corridor side the line stays
    FLUSH under the deck: it comes off its downstream pickup, jogs into the tray-edge↔upright drop
    slot (X4641, clear of the spray-carriage which ends at X4599), RISES to the flush ribbon Z, then
    crosses the OUTER long beam through an OPEN-TOP NOTCH into the lane (never dipping toward the
    tray).  It then LOOPS UP over the first cantilever (never through it — Rule 5), drops back into
    the under-grate ribbon channel, and runs −Yd to the near rim.  corridor_pt Yd must be past the
    cantilever end (>1086).  up_yd (default = corridor_pt Yd) sets where the loop-over rises."""
    lx, oz = RIBBON_LANE_X[i], RIBBON_OVER_Z
    cy, cz = corridor_pt[1], corridor_pt[2]
    uc = up_yd if up_yd is not None else cy        # loop-over rise Yd on the corridor side
    ny = near_pt[1]                                 # this line's own near-end Yd
    pts = [corridor_pt,
           (RIBBON_SLOT_X, cy, cz),                # to the drop slot X, in the corridor PAST the tray edge (still at the pickup Z)
           (RIBBON_SLOT_X, cy, RIBBON_Z),          # RISE up the slot to FLUSH under the deck (X>4599 → clear of the carriage)
           (lx, cy, RIBBON_Z),                     # −X through the OPEN-TOP NOTCH in the outer beam to the lane, at flush
           (lx, uc, RIBBON_Z),                     # −Yd (flush under the grate) to the loop-over rise Yd
           (lx, uc, oz),                           # UP to the over-crest height
           (lx, RIBBON_YD_UP, oz),                 # −Yd OVER the first cantilever to just before it
           (lx, RIBBON_YD_UP, RIBBON_Z),           # DOWN through the grate into the ribbon channel
           (lx, ny, RIBBON_Z),                     # −Yd along the ribbon (under the grate) to the near-end Yd
           (lx, ny, near_pt[2]),                   # to the near-end Z
           near_pt]                                # to this line's pinhole-wall connection
    out = [pts[0]]                                 # drop consecutive duplicates (near_pt may sit on the lane)
    for q in pts[1:]:
        if q != out[-1]:
            out.append(q)
    return out


def ribbon_supports():
    """Welded cross-beams spanning between the two right-walkway long bearers, carrying the
    under-walkway pipe ribbon (the four lines clip to them).  Small flat bars at intervals
    in Yd, their tops just under the ribbon Z."""
    p = []
    x0, x1 = ov.RWK_X_L, ov.RWK_X_R              # bearer span across the walkway (4329..4629)
    ztop = RIBBON_Z - 8                          # ~96 — bar top just under the flush pipes (ribbon Z104.5)
    for yd in RIBBON_SUP_YD:
        p.append(ov.ruby_box("Ribbon support cross-beam (welded 40x10)",
                             x0, yd - 3, ztop - 10, x1 - x0, 6, 10, color=ov.C_STEEL))
    return "\n".join(p)


def _arm(nm, cx, cy, cz, axis, sd, body, L, r, color):
    """One port stub of a fitting — a cylinder from the body face outward along an axis."""
    if axis == "x":
        x0 = cx + body / 2 if sd > 0 else cx - body / 2 - L
        return ov.ruby_cylinder(nm, x0, cy, cz, r, L, color=color, axis="x")
    if axis == "y":
        y0 = cy + body / 2 if sd > 0 else cy - body / 2 - L
        return ov.ruby_cylinder(nm, cx, y0, cz, r, L, color=color, axis="y")
    z0 = cz + body / 2 if sd > 0 else cz - body / 2 - L
    return ov.ruby_cylinder(nm, cx, cy, z0, r, L, color=color, axis="z")


def diverter(name, cx, cy, cz, run="x", branch="z-", handle="y+", color=None, L=10, r=13):
    """3-way diverter = a standard T-port valve (3 coplanar ports, handle perpendicular).
    The 3 pipes lie in a plane (seen face-on as a T); the RED handle projects out of that
    plane toward the operator.  `run` is the through-run axis (both ways); `branch` is the
    divert port as axis+sign (default 'z-' = exits the underside); `handle` is the axis+sign
    the handle projects (default 'y+' for a pinhole-wall mount; use 'x-' on the corridor
    panel, which faces -X).  Valve body kept yellow (color defaults to C_VALVE)."""
    color = color or ov.C_VALVE
    body = 46
    ba, bs = branch[0], (+1 if "+" in branch else -1)
    ha, hs = handle[0], (+1 if "+" in handle else -1)
    p = [ov.ruby_box(f"{name} body", cx - body / 2, cy - body / 2, cz - body / 2, body, body, body, color=color)]
    p.append(_arm(f"{name} run +", cx, cy, cz, run, +1, body, L, r, color))
    p.append(_arm(f"{name} run -", cx, cy, cz, run, -1, body, L, r, color))
    p.append(_arm(f"{name} branch", cx, cy, cz, ba, bs, body, L, r, color))
    # RED handle: stem out along the `handle` axis, lever bar along the run axis at the tip
    p.append(_arm(f"{name} handle stem", cx, cy, cz, ha, hs, body, 42, 6, C_HANDLE))
    tip = {"x": (cx + hs * (body / 2 + 48), cy, cz),
           "y": (cx, cy + hs * (body / 2 + 48), cz),
           "z": (cx, cy, cz + hs * (body / 2 + 48))}[ha]
    lx, ly, lz = tip
    if run == "x":
        p.append(ov.ruby_box(f"{name} handle lever", lx - 32, ly - 8, lz - 7, 64, 16, 14, color=C_HANDLE))
    elif run == "y":
        p.append(ov.ruby_box(f"{name} handle lever", lx - 8, ly - 32, lz - 7, 16, 64, 14, color=C_HANDLE))
    else:
        p.append(ov.ruby_box(f"{name} handle lever", lx - 8, ly - 7, lz - 32, 16, 14, 64, color=C_HANDLE))
    return "\n".join(p)


def frame(part="all"):
    """Deep 4-leg box (uprights + butt-jointed rings + feet) with REAR-panel brackets only.

    part="posts" emits only the vertical skeleton (uprights + feet + rear-panel brackets);
    part="rails" emits only the horizontal ring rails. The construction model installs the
    posts BEFORE the IBC totes and the rails AFTER — the top-ring rails would otherwise trap
    the totes and block the far column going in. part="all" (default) = both, byte-identical
    to the original single-pass output (posts' uprights, then rails, then posts' feet/brackets)."""
    posts = part in ("all", "posts")
    rails = part in ("all", "rails")
    p = []
    ft = ov.IBC_FOOT_PLATE_T                               # foot-plate thickness — uprights SIT ON the plate (bottom at ft), top fixed at TOP_Z
    up_yds = (YD_NEAR, YD_FAR - S)
    box_xs = (FRONT_X, BACK_X)
    if posts:
        for ux in box_xs:                                  # 4 corner uprights
            for yd in up_yds:
                p.append(ov.ruby_box("Frame upright", ux, yd, ft, S, S, TOP_Z - ft, color=ov.C_STEEL))
    if rails:
        for rz in (ft, TOP_Z - S):                         # bottom ring on the plate + top ring, rails BUTT between uprights
            for ux in box_xs:
                p.append(ov.ruby_box("Frame rail (Yd)", ux, YD_NEAR + S, rz, S, (YD_FAR - S) - (YD_NEAR + S), S, color=ov.C_STEEL))
            for yd in up_yds:
                p.append(ov.ruby_box("Frame rail (X)", FRONT_X + S, yd, rz, BACK_X - (FRONT_X + S), S, S, color=ov.C_STEEL))
    if posts:
        # floor feet (150×150×12 plate + 4× M12) under each upright
        fp, bpc = ov.IBC_FOOT_PLATE, ov.IBC_FOOT_BOLT_PCD // 2   # ft hoisted above (uprights sit on the plate)
        for ux in box_xs:
            # FRONT feet shift OUTBOARD (plate + anchors) to clear the processing-tray basin; the upright
            # stays put (still fully on the plate) — plate/anchor spec unchanged, only the X station moves.
            foot_dx = ov.IBC_FRONT_FOOT_DX if ux == FRONT_X else 0.0
            for yd in up_yds:
                cx, cy = ux + S / 2 + foot_dx, yd + S / 2
                p.append(ov.ruby_box("Foot plate", cx - fp / 2, cy - fp / 2, 0, fp, fp, ft, color=ov.C_STEEL))
                for dx in (-bpc, bpc):
                    for dy in (-bpc, bpc):
                        p.append(ov.ruby_bolt("Foot anchor M12", cx + dx, cy + dy, 0, ft + 4, radius=7, axis="z", color=C_BOLT, head="far", nut=None))  # anchor into the floor — hex head at the top
        # REAR-panel mount brackets only (on the back uprights, set back behind the inside face).
        # Drawn as an L-ANGLE (5mm legs, per Plate 5 / Detail D): a horizontal base leg TEK-screwed to the
        # post (J8) + a vertical upstand the rear panel bolts to (J4) — NOT a solid block.
        bw, bproj, bwid, blt = 60, 40, 30, 5      # upstand height, projection, bracket width (X), leg thickness
        for py, pdir in ((YD_NEAR + S, +1), (YD_FAR - S, -1)):
            # top pair dropped from TOP_Z-120 (2176) to sit under the new lowered panel top
            for bz in (120, TOP_Z / 2, PANEL_TOP_Z - 120):
                by0 = py if pdir > 0 else py - bproj
                post_y = by0 if pdir > 0 else by0 + bproj - blt   # thin leg sits flat on the upright INBOARD face
                p.append(ov.ruby_box("Rear-panel bracket post leg", BACK_X, post_y, bz - bw / 2,
                                     EQT + blt, blt, bw, color=ov.C_STEEL))        # vertical leg FLAT on the upright's Yd face — TEK-screwed to the post (J8)
                p.append(ov.ruby_box("Rear-panel bracket upstand", BACK_X + EQT, by0, bz - bw / 2,
                                     blt, bproj, bw, color=ov.C_STEEL))            # vertical upstand parallel to the ply (Yd-Z plane) — the panel bolts THROUGH it (J4)
    return "\n".join(p)


def tote_restraint():
    """Front retaining bars (trap the direct-stacked totes against the side/end walls) + the
    exterior wall anchor plates — ported from the old single-portal ibc_rack (dropped when the
    deep box was forked; ibc_rack now lives only in the archived right-cantilever study).
    Lives with the IBC stack, not the pump frame."""
    p = []
    front_x = ov.IBC_COL_X - 20            # 4654 — bars in the gap just in front of the tote face
    bar_d = ov.IBC_FRONT_BAR_D             # 20 — 50×20×3 RHS, slot-constrained depth in -X
    # TWO bars per tote face (upper + lower), both in the slot → share the forward thrust (EN 12195-1
    # loaded case: 1/tier fails SF 0.79, 2/tier gives SF 1.59 bar-alone / 4.77 with anti-slip mat).
    bar_zs = (500, 950, 1500, 1950)        # bottom tier (500,950) + top tier (1500,1950); each bar has its
    #   OWN hanger, so the pair is spread ~450mm to give each hanger's straddling bolts wrench clearance
    tier_zs = (500, 1500)                  # lower bar of each tier — D-ring reference
    hp_t = 4                               # wall-hanger back-plate thickness (Yd) — bars butt it, not the wall
    # Bars BUTT the corridor uprights (corridor end) AND the wall-hanger back plates (wall end) — each bar
    # ends at its mating face, not overlapping through, so both the cleated + hung joints read as joined.
    for i, (y0, y1) in enumerate(((hp_t, YD_NEAR), (YD_FAR, ov.C_WID - hp_t))):
        cor_yd = y1 if i == 0 else y0          # the bar's CORRIDOR (upright) end
        wdir = -1 if i == 0 else 1             # toward-wall direction the cleat leg extends UNDER the bar
        for bz in bar_zs:
            p.append(ov.ruby_box("Front Retaining Bar", front_x, y0, bz, bar_d, y1 - y0, S, color=ov.C_STEEL))
            # J2/W3 corridor-end connection (Detail B): an L-ANGLE fillet-welded to the upright — a horizontal
            # leg the bar sits on + a vertical leg on the bar's FRONT (−X) face — the bar drops into the corner
            # and a SINGLE horizontal M12 (J2) runs through the vertical leg + the bar's tall (50mm) web, so the
            # hole gets full edge distance and the bolt secures the unsupported direction (Alvin 2026-08-18).
            lt, llen = 8, 90                                                     # leg thickness / reach along the bar (Yd)
            leg_y0 = cor_yd - llen if wdir < 0 else cor_yd
            p.append(ov.ruby_box("Bar cleat leg (J2)", front_x, leg_y0, bz - lt, bar_d, llen, lt, color=ov.C_STEEL))          # horizontal leg UNDER the bar
            p.append(ov.ruby_box("Bar cleat upstand (J2/W3)", front_x - lt, leg_y0, bz - lt, lt, llen, S + lt, color=ov.C_STEEL))  # vertical leg on the bar FRONT (−X), welded to the upright
            p.append(ov.ruby_box("Bar cleat backing plate (J2)", front_x + bar_d, cor_yd + wdir * 45 - 25, bz + 5, lt, 50, 40, color=ov.C_STEEL))  # nut-side spreader on the bar's far web
            p.append(ov.ruby_bolt("IBC Bar Cleat Bolt M12x65 (J2)", front_x - lt, cor_yd + wdir * 45, bz + S / 2,
                                  bar_d + 2 * lt, radius=6, axis="x", color=C_BOLT, head="base", nut="far"))                 # SINGLE horizontal bolt: leg + bar web + backing plate
    # D-ring lashing holders — 4 per tier × 2 tiers = 8 (matches ibc-frame drawing §4.1); on the LOWER
    # bar of each tier (one per tier) so the ring count stays 8 despite the doubled bars.
    # Yd positions clear of the corridor-end cleat legs (near leg 956–1046, far leg 1316–1406) so the
    # D-ring holders don't intersect them (was 520/940/1422/1842 — the 940 + 1422 rings touched the cleats).
    for ydh in (520, 900, 1462, ov.C_WID - 520):
        for bz in tier_zs:
            p.append(ov.ruby_cylinder("D-Ring Holder", front_x - 6, ydh, bz + S / 2, 16, 10,
                                      color=ov.C_STEEL, axis="x"))
    # Wall joist hangers — ONE identical 2-bolt hanger per bar (symmetric pair, fab-identical), each
    # through-bolted (2× M12×65) to its own exterior backing plate. 8 hangers × 2 bolts = 16 wall
    # penetrations (same as the old 4 hangers × 4 bolts); each bar-end carries only ¼ of the tote
    # thrust (~1.8 kN loaded) so a 2-bolt hanger runs SF ~9 (ibc_frame_load.py). The bolt is drawn as
    # a generic through-bolt cylinder; the M12×65 length spec lives in the 2D drawings + parts.py.
    # Backing plate is TALL (rotated 90°): the 2 through-bolts stack VERTICALLY, one ≥50mm BELOW the seat
    # and one ≥50mm ABOVE the bar, so there is wrench clearance to tighten them (the natural joist-hanger
    # pattern). The pocket back-plate + exterior backing plate both grow to span the bolt pair.
    ext_pt, ext_pw = 8, 60                 # backing plate: 8 thick (Yd), 60 wide (X)
    for wall_yd, din in ((0, 1), (ov.C_WID, -1)):
        for bz in bar_zs:                  # 8 identical hangers — one per bar
            ht, dep = hp_t, 70
            bolt_lo = bz - 61             # bottom bolt: 50mm clear GAP below the seat (seat = bz-4..bz)
            bolt_hi = bz + S + 57          # top bolt: 50mm clear GAP above the bar top (bz+S)
            plate_z0 = bolt_lo - 18        # plate spans both bolts + edge margin (~191mm tall)
            ext_ph = (bolt_hi + 18) - plate_z0
            p_y = wall_yd if din > 0 else wall_yd - ht
            s_y = wall_yd if din > 0 else wall_yd - dep
            pocket_w = 60                  # back-plate + seat both 60mm wide — REUSE the exterior backing stock (2026-08-15; was S+16/S+8)
            # Clamp assembly sits on the INSIDE (corridor) side of the bar — its back edge flush with the bar
            # back (= tote front), NOT projecting into the tote (was front_x−8 → +52, 32mm into the tote).
            hx0 = front_x + bar_d - pocket_w                  # inside plate / backing-plate X start
            p.append(ov.ruby_box("Wall Hanger Plate", hx0, p_y, plate_z0, pocket_w, ht, ext_ph, color=ov.C_STEEL))
            # SAME L-cleat as the post end (welded to the inside plate): a horizontal leg the bar sits on +
            # a vertical leg on the bar FRONT, with 1 HORIZONTAL J7 bolt through the leg + the bar's 50mm web.
            lt2 = 8
            p.append(ov.ruby_box("Wall Hanger L-leg (J7)", front_x, s_y, bz - lt2, bar_d, dep, lt2, color=ov.C_STEEL))          # horizontal leg (bar sits on it)
            p.append(ov.ruby_box("Wall Hanger L-upstand (J7/W)", front_x - lt2, s_y, bz - lt2, lt2, dep, S + lt2, color=ov.C_STEEL))  # vertical leg on the bar FRONT
            p.append(ov.ruby_box("Wall Hanger backing plate (J7)", front_x + bar_d, wall_yd + din * 28 - 25, bz + 5, lt2, 50, 40, color=ov.C_STEEL))  # nut-side spreader on the bar's far web
            ecx = hx0 + pocket_w / 2
            plate_y = (-ov.WALL_T - ext_pt) if din > 0 else (ov.C_WID + ov.WALL_T)
            bolt_cy = (-ov.WALL_T - ext_pt) if din > 0 else (ov.C_WID - 10)
            p.append(ov.ruby_box("IBC Wall Backing Plate (ext)",
                                 ecx - ext_pw / 2, plate_y, plate_z0, ext_pw, ext_pt, ext_ph, color=ov.C_STEEL))
            for bolt_z in (bolt_lo, bolt_hi):   # 2 through-bolts, ≥50mm clear of the bar + seat
                p.append(ov.ruby_bolt("IBC Wall Through-Bolt M12", ecx, bolt_cy, bolt_z, 58, radius=7,
                                      axis="y", color=C_BOLT, head="far", nut="base"))  # head outside, nut inside
            # J7 retention bolt: ONE HORIZONTAL M12 through the L's vertical leg + the bar's 50mm web (like J2 at
            # the post) — good edge distance; the L-corner carries the load, the bolt secures the unsupported direction.
            p.append(ov.ruby_bolt("IBC Bar Retention Bolt M12 (J7)", front_x - lt2, wall_yd + din * 28,
                                  bz + S / 2, bar_d + 2 * lt2, radius=6, axis="x", color=C_BOLT, head="base", nut="far"))
    return "\n".join(p)


def rear_panel():
    """The 18mm marine-ply REAR panel (recessed into the back-wall opening, flush with the back
    posts' −X inside face) PLUS the 25mm ply 'shirt' the pumps/ACC clamp to — a backing hard
    behind the bodies (deepest = the ACC), tied back to the rear-frame ring across the chase.
    The pumps' integral cam-clamps grip onto it; only short port→riser connectors penetrate it."""
    pz0, ph = S, PANEL_TOP_Z - S                 # top dropped to PANEL_TOP_Z (1900) for the Fan A air window
    yw = (YD_FAR - S) - (YD_NEAR + S)
    # DRILLED clearance holes — the "round holes" already called out where the port→riser connectors and
    # the Cct-C branches penetrate the ply (a void, not a part), so each reads as passing THROUGH a hole
    # rather than fused into the slab (check_interference.py --pipes).  Centers = (Yd, Z) mirror the pipe
    # waypoints; radius is generous (RP+3 pipe / 7 cable) so a small routing shift stays in the hole —
    # --pipes remains the drift tripwire.  Both X-thin panels cut along X; the spine (Yd-thin) along Y.
    RPH, CBH = RP + 3, 7
    shirt_holes = [(1113, 1210, RPH),    # Blue #1 -> P-01 suction entry
                   (1245, 1502, RPH),    # P-05 -> X3 end-wall port
                   (1196, 1700, RPH),    # X4 Waste (P-03) pickup
                   (CTR_Y, 1030, CBH),   # Cct-C branch -> P-02 (power cable)
                   (CTR_Y, 1430, CBH)]   # Cct-C branch -> P-05 (power cable)
    rear_holes = [(1165, 235, RPH),      # DV-01 -> IBC-4 merge
                  (1194, 65,  RPH),      # DV-02 waste -> IBC-4
                  (1113, 1210, RPH),     # Blue #1 -> P-01 suction entry
                  (1245, 1502, RPH),     # P-05 -> X3 end-wall port
                  (1196, 1700, RPH),     # X4 Waste (P-03) pickup
                  (CTR_Y, 1030, CBH),    # Cct-C branch -> P-02
                  (CTR_Y, 1430, CBH)]    # Cct-C branch -> P-05
    spine_holes = [(5500, 1376, RPH)]    # Blue equalization (IBC-1 <-> IBC-2)  (X, Z) — cut along Y
    p = [ov.ruby_box("Rear panel (18mm exterior ply)", BACK_X, YD_NEAR + S, pz0,
                     EQT, yw, ph, color=ov.C_PLY, holes=rear_holes, hole_axis="x")]
    # 25mm ply pump-mount shirt: front face hard behind the ACC body (the deepest, back ≈ PXC+ACC_R),
    # spanning the pump-column height; sits in the ~56mm chase between the bodies and the rear frame.
    p.append(ov.ruby_box("Pump-mount ply shirt (25mm)", SHIRT_X, YD_NEAR + S, 325,   # SHIRT_X: module constant
                         25, yw, PANEL_TOP_Z - 325, color=ov.C_PLY, holes=shirt_holes, hole_axis="x"))   # top dropped 2191->1900 for the Fan A window (DV-02 is on the skid, Phase 2);
    #   bottom SHORTENED to 325 (was 275) to clear the brown P-05 inlet elbow now RAISED to z298-318; still backs the pumps
    # Spacer/cleat blocks tying the shirt BACK to the rear panel (and thus the frame) across the
    # ~27mm chase — placed at the two Yd edges in the clear Z windows BETWEEN the horizontal X3/X4
    # port runs that cross the chase (those sit at z≈1500 / 1820 / 1900).
    blk_x0, blk_d = SHIRT_X + 25, BACK_X - (SHIRT_X + 25)   # shirt back → rear-panel front
    for byd in (YD_NEAR + S, YD_FAR - S - 40):              # near + far edges, 40mm wide
        for bz in (320, 920, 1560):                        # all clear of the port runs (z1492+)
            p.append(ov.ruby_box("Shirt-to-panel spacer block", blk_x0, byd, bz, blk_d, 40, 120, color=ov.C_PLY))
    # Drain-riser backing SPINE — an 18mm ply fin teeing PERPENDICULAR off the rear panel into the
    # rear corridor (matches the documented marine-ply spine), spanning the two tall back-of-panel
    # risers (X4 waste at x≈5200, blue recycle at x≈5440) so they P-clip to it; tied to the frame
    # top/bottom rings.  Placed at Yd1183 (between the two risers) — clear of the merge (Yd1116) and
    # the X1 cross (x>5470).
    p.append(ov.ruby_box("Drain-riser backing spine (18mm ply)", BACK_X, 1206, 280,
                         5560 - BACK_X, 18, (TOP_Z - S) - 280, color=ov.C_PLY,
                         holes=spine_holes, hole_axis="y"))   # −Yd face at 1206 = the grey
    #   X4-waste riser's far edge, so it CLAMPS to the face; bottom at 280 (clears the low waste pickup
    #   z247-268).  Extended +X to 5560 (past the X1 cross at 5530) and UP to the rear-panel top
    #   (z=TOP_Z−S=2246) to also back the X1 fill cross, Blue equalization tie, and the high fill/recycle runs.
    # (The X3 brown-pipe support shelf was removed — the P-05→X3 discharge now runs behind the panel on
    #  the Yd1245 lane, no longer crossing the rear corridor above the merge, so it needs no shelf.)
    # Spine riser P-clips (#29) — same cushioned-strap method as the side-board clips: hold the three
    # back-of-panel WASTE risers flush to the spine's −Yd face (Yd1206).
    spine_face = 1206
    for rx, ryd, zb, zt in ((5200, 1196, 279, 1679),      # X4 waste (P-03) pickup
                            (5289, 1195, 65, 1209),        # DV-02 waste → IBC-4
                            (5404, 1195, 242, 1230)):      # DV-01 → IBC-4 merge
        for frac in (0.30, 0.70):
            cz = max(300, min(int(zb + (zt - zb) * frac), int(TOP_Z - S - 20)))
            y_lo = min(spine_face, ryd - RP - 2); y_hi = max(spine_face, ryd + RP + 2)
            p.append(ov.ruby_box("Spine riser P-clip", rx - 14, y_lo, cz - 8,
                                 28, y_hi - y_lo, 16, color=C_CLIP))
    # FAR (+Yd) side of the spine — the grey/brown X-port lines run along it toward the end wall:
    # P-05→X3 (brown, Yd1245, Z1502) and P-03→X4 (grey, Yd1235, Z1902). 2 clamps each, to the +Yd face.
    spine_far_face = 1224
    for px, pyd, pz in ((5250, 1245, 1502), (5450, 1245, 1502),     # P-05 → X3 (brown)
                        (5250, 1235, 1902), (5450, 1235, 1902)):    # P-03 → X4 (grey)
        p.append(ov.ruby_box("Spine far-side P-clip", px - 14, spine_far_face, pz - 12,
                             28, (pyd + RP + 2) - spine_far_face, 24, color=C_CLIP))
    return "\n".join(p)


# ── corridor-panel equipment placement (equipment hangs −X off the rear panel) ──
FACE_X = BACK_X                          # 5104 — rear-panel plane; equipment hangs −X toward the mouth
COL_L  = YD_NEAR + 63                    # 1109 — left (Brown-side) pump column
COL_R  = 1235                            # X4 grey waste run + port — clamps to the spine's +Yd face (1224 =
#   spine Yd1206 + 18mm) plus a pipe radius, so the run mounts on the spine instead of floating beside it
CTR_Y  = (YD_NEAR + YD_FAR) / 2          # 1181 — corridor center
RP     = ov.PUMP_PIPE_OD / 2            # 1/2" pipe radius
BV02_YD = YD_NEAR + S - (RP + 8)        # 1077.5 — BV-02 brown-suction riser Yd: the VALVE BARREL
#   (radius RP+8) sits FLUSH against the shirt's −Yd edge (1096) so nothing embeds in the ply (no slot
#   to cut); the thinner pipe then stands ~8mm off and P-clips to the shirt for support.  Single source
#   for the geometry AND the 3D callout anchor, so the label can't drift off the valve.
CDK    = "#3A3A42"                       # dark fittings / motor cans
DVB    = 46                              # diverter body cube
DVL    = 10                              # diverter port socket length — real 1/2" socket 3-way ball valve
#   is 2.62"/66.5mm overall (US Plastics #30667), i.e. ports reach only ~33mm from center (DVB/2+DVL)
C_CHECK = "#8A2BE2"                      # PURPLE — one-way / check valves (vs YELLOW diverters)
# UPRIGHT pump (filter-style): a vertical body + cap with BOTH ports out the TOP, exiting along
# ±X (face dir), offset ±26 in Yd (OUT +Yd, IN −Yd).  All pumps (incl. the wall P-02) conform.
PVB_R, PVB_H, PCAP_H = 50, 180, 30       # vertical body radius / height, head/cap height
PXC     = FACE_X - 120                    # 4984 — pump body center X (upright, in front of the panel)
BV_FWD_X = 4770                           # BV-02/BV-06 forward-loop riser X — pulled toward the walkway edge (near the front post inner face 4704.8) for operator reach (#29)
Z_ACC0  = 1780                            # ACC-01 BOTTOM — raised clear of the pipe runs below it
MERGE4  = (ov.IBC_COL_X + 730, 1195, ov.IBC_PALLET_H + ov.IBC_H_1000 - 106)  # (5404,1195,1230)
                                          # shared IBC-4 waste merge — now SURFACE-MOUNTED on the drain-riser
                                          # spine (Yd1195 ≈ spine −Yd face 1206 − pipe radius), so the DV-01
                                          # riser + DV-02 drop both clamp to the spine and only the tote-entry
                                          # stub leaves it.  DV-01 (wall) + DV-02 join here → one entry.
GAPX  = ov.PROC_TRAY_X_R + 12             # 4641 — in the gap between the tray right edge (4629) and the
                                          # frame upright (4654): the ONLY place to cross between the
                                          # outside-rim strip (Yd<80) and the corridor (Rule 5a, around the
                                          # tray).  Cross HORIZONTALLY here at a z clear of the FP rail (z510).
TRAY_STRIP_Y = 60                         # outside the tray near rim (Yd80): the around-the-rim run lane
GAP_CORR_Y = 1132                         # corridor-side approach Yd — sits in the clear window between the brown P-02
                                          #   inlet riser (Yd≤1111) and the grey DV-01→IBC-4 merge run (shifted +Yd to
                                          #   1165), ~10mm each side; the grey shift toward the film plane opened this lane
BROWN_TAP = (4880, CTR_Y - (PVB_R + 30), ov.IBC_PALLET_H + 140)   # (4880,1101,308) — the SINGLE shared
#   tap RAISED +50mm (was +90/z258) to lift the P-02/P-05 brown inlet runs clear of the blue supply trunk's
#   low-lane crossing (z225-246); the dip tube below is extended +50mm to keep the same in-tote pickup depth
                                          # IBC-3 bottom tap T: run ALONG X (P-02 leaves −X to the
                                          # wall, P-05 leaves +X to the pump), dip on the −Yd branch.
                                          # Feeds BOTH P-02 (wall loop) and P-05 → one tote penetration.


def pump_unit(nm, cx, cy, cz0, axis="x", face=1, color=None):
    """UPRIGHT pump with IN and OUT on OPPOSITE sides near the top — the same pattern as the
    filters (straight-through).  `axis` = the port line ("x": ports along ±X; "y": along ±Yd);
    `face` = the sign of the OUT side (+1 → OUT on +axis / IN on −axis; −1 flips).  Tips via
    pump_in()/pump_out()."""
    color = color or ov.C_PUMP
    top = cz0 + PVB_H
    p = [ov.ruby_cylinder(nm + " body", cx, cy, cz0, PVB_R, PVB_H, color=color, axis="z"),
         ov.ruby_cylinder(nm + " head", cx, cy, top, PVB_R + 3, PCAP_H, color=CDK, axis="z")]
    pz = top - 18                                # ports near the top (like the filter cap ports)
    for tag, sd in (("in", -face), ("out", face)):
        if axis == "x":
            x0 = (cx + PVB_R) if sd > 0 else (cx - PVB_R - 30)
            p.append(ov.ruby_cylinder(f"{nm} {tag} port", x0, cy, pz, RP, 30, color=CDK, axis="x"))
        else:
            y0 = (cy + PVB_R) if sd > 0 else (cy - PVB_R - 30)
            p.append(ov.ruby_cylinder(f"{nm} {tag} port", cx, y0, pz, RP, 30, color=CDK, axis="y"))
    return p


def pump_out(cx, cy, cz0, axis="x", face=1):
    pz = cz0 + PVB_H - 18
    return (cx + face * (PVB_R + 30), cy, pz) if axis == "x" else (cx, cy + face * (PVB_R + 30), pz)
def pump_in(cx, cy, cz0, axis="x", face=1):
    pz = cz0 + PVB_H - 18
    return (cx - face * (PVB_R + 30), cy, pz) if axis == "x" else (cx, cy - face * (PVB_R + 30), pz)


def tee(nm, cx, cy, cz, run="x", branch="z-", color=None):
    """Pipe TEE / T-connector fitting (socket × socket × socket, e.g. a Sch-40 PVC tee): a straight
    RUN (two collinear ports along `run`) + a perpendicular BRANCH (`branch` = axis+sign), one
    fitting body fatter than the pipe, with a raised SOCKET CUFF at each of the 3 ends.  Centered
    on the run/branch intersection (cx,cy,cz)."""
    color = color or "#9AA0A8"            # neutral fitting grey (PVC)
    br, cr, cl = RP + 5, RP + 9, 12       # body radius, socket-cuff radius, cuff length
    half, bl = 30, 36                     # run half-length, branch reach
    ba, bs = branch[0], (1 if "+" in branch else -1)
    p = []
    # RUN body (centered, both ways) + BRANCH body (centre outward)
    run0 = {"x": (cx - half, cy, cz), "y": (cx, cy - half, cz), "z": (cx, cy, cz - half)}[run]
    p.append(ov.ruby_cylinder(nm + " run", run0[0], run0[1], run0[2], br, 2 * half, color=color, axis=run))
    brn0 = {"x": ((cx if bs > 0 else cx - bl), cy, cz),
            "y": (cx, (cy if bs > 0 else cy - bl), cz),
            "z": (cx, cy, (cz if bs > 0 else cz - bl))}[ba]
    p.append(ov.ruby_cylinder(nm + " branch", brn0[0], brn0[1], brn0[2], br, bl, color=color, axis=ba))
    # SOCKET CUFFS at the 3 ends (raised bell sockets the pipe inserts into)
    ends = {"x": [(cx - half, cy, cz, "x"), (cx + half - cl, cy, cz, "x")],
            "y": [(cx, cy - half, cz, "y"), (cx, cy + half - cl, cz, "y")],
            "z": [(cx, cy, cz - half, "z"), (cx, cy, cz + half - cl, "z")]}[run]
    bend = {"x": ((cx + bl - cl) if bs > 0 else (cx - bl), cy, cz, "x"),
            "y": (cx, (cy + bl - cl) if bs > 0 else (cy - bl), cz, "y"),
            "z": (cx, cy, (cz + bl - cl) if bs > 0 else (cz - bl), "z")}[ba]
    for ex, ey, ez, ax in ends + [bend]:
        p.append(ov.ruby_cylinder(nm + " socket cuff", ex, ey, ez, cr, cl, color=color, axis=ax))
    return "\n".join(p)


def cross(nm, cx, cy, cz, a1="x", a2="y", color=None):
    """4-way CROSS fitting: two straight collinear runs (along `a1` and `a2`) intersecting at
    (cx,cy,cz) — four coplanar ports — one fitting body with a raised socket cuff at all 4 ends.
    Same construction as tee() but with a second through-run instead of a single branch."""
    color = color or "#9AA0A8"
    br, cr, cl = RP + 5, RP + 9, 12       # body radius, socket-cuff radius, cuff length
    half = 30                             # run half-length
    p = []
    ends = []
    for ax in (a1, a2):
        a0 = {"x": (cx - half, cy, cz), "y": (cx, cy - half, cz), "z": (cx, cy, cz - half)}[ax]
        p.append(ov.ruby_cylinder(nm + " run", a0[0], a0[1], a0[2], br, 2 * half, color=color, axis=ax))
        ends += {"x": [(cx - half, cy, cz, "x"), (cx + half - cl, cy, cz, "x")],
                 "y": [(cx, cy - half, cz, "y"), (cx, cy + half - cl, cz, "y")],
                 "z": [(cx, cy, cz - half, "z"), (cx, cy, cz + half - cl, "z")]}[ax]
    for ex, ey, ez, ax in ends:
        p.append(ov.ruby_cylinder(nm + " socket cuff", ex, ey, ez, cr, cl, color=color, axis=ax))
    return "\n".join(p)


def check_valve(nm, px, py, pz, axis, color=None):
    """In-line one-way / check valve: a short barrel the pipe runs THROUGH, centered on the pipe
    centerline (px,py,pz) and oriented ALONG the run (`axis`).  Check valves are IN-LINE devices —
    they sit on a STRAIGHT length of pipe, never straddling an elbow."""
    color = color or C_CHECK
    L, r = 48, RP + 7
    if axis == "x": return ov.ruby_cylinder(nm, px - L / 2, py, pz, r, L, color=color, axis="x")
    if axis == "y": return ov.ruby_cylinder(nm, px, py - L / 2, pz, r, L, color=color, axis="y")
    return ov.ruby_cylinder(nm, px, py, pz - L / 2, r, L, color=color, axis="z")


C_BV = "#7A8088"                              # ball-valve body — chrome/steel grey (distinct from
                                              # PURPLE check valves and YELLOW diverters)


def ball_valve(nm, px, py, pz, axis, color=None, hdir="+y"):
    """In-line MANUAL ball valve: a short barrel the pipe runs THROUGH (centered on the pipe
    centerline, oriented ALONG `axis`) plus a clear RED lever handle — a stem out perpendicular
    to the run with a lever bar at its tip (like the diverter handles) so it reads as a hand
    valve.  Like a check valve it sits on a STRAIGHT length of pipe, never on an elbow."""
    color = color or C_BV
    L, r = 44, RP + 8                          # barrel length / radius
    HS, HSr, LV = 28, 6, 48                    # handle stem length / radius, lever-bar length
    p = []
    if axis == "x":                            # horizontal barrel along X — handle sticks UP (+Z)
        p.append(ov.ruby_cylinder(nm, px - L / 2, py, pz, r, L, color=color, axis="x"))
        p.append(ov.ruby_cylinder(nm + " handle stem", px, py, pz + r, HSr, HS, color=C_HANDLE, axis="z"))
        p.append(ov.ruby_box(nm + " handle", px - LV / 2, py - 7, pz + r + HS, LV, 14, 9, color=C_HANDLE))
    elif axis == "y":                          # horizontal barrel along Yd — handle sticks UP (+Z)
        p.append(ov.ruby_cylinder(nm, px, py - L / 2, pz, r, L, color=color, axis="y"))
        p.append(ov.ruby_cylinder(nm + " handle stem", px, py, pz + r, HSr, HS, color=C_HANDLE, axis="z"))
        p.append(ov.ruby_box(nm + " handle", px - 7, py - LV / 2, pz + r + HS, 14, LV, 9, color=C_HANDLE))
    else:                                      # vertical barrel — handle sticks out horizontally toward `hdir`
        p.append(ov.ruby_cylinder(nm, px, py, pz - L / 2, r, L, color=color, axis="z"))
        ux, uy = {"+y": (0, 1), "-y": (0, -1), "+x": (1, 0), "-x": (-1, 0)}[hdir]
        if uy:                                 # stem along Yd, lever a vertical bar at the tip
            p.append(ov.ruby_cylinder(nm + " handle stem", px, (py + r) if uy > 0 else (py - r - HS), pz, HSr, HS, color=C_HANDLE, axis="y"))
            p.append(ov.ruby_box(nm + " handle", px - 7, py + uy * (r + HS) - (0 if uy > 0 else 9), pz - LV / 2, 14, 9, LV, color=C_HANDLE))
        else:                                  # stem along X, lever a vertical bar at the tip
            p.append(ov.ruby_cylinder(nm + " handle stem", (px + r) if ux > 0 else (px - r - HS), py, pz, HSr, HS, color=C_HANDLE, axis="x"))
            p.append(ov.ruby_box(nm + " handle", px + ux * (r + HS) - (0 if ux > 0 else 9), py - 7, pz - LV / 2, 9, 14, LV, color=C_HANDLE))
    return "\n".join(p)


def sample_valve(nm, cx, cy, cz, h=60, color=None, spout="z-"):
    """Sample / test tap: a small valve body + a downturned sample spout + a RED HANDWHEEL on top
    (stem + flat disc) so it clearly reads as a valve.  `cz` = body base Z, `h` = body height.
    `spout`: "z-" drops straight down (default); an axis+sign like "-x" projects the spout OUT to that
    side then turns down — use it when the valve sits in-line on a vertical riser (so the spout clears
    the pipe and a cup fits under it)."""
    color = color or ov.C_VALVE
    p = [ov.ruby_box(nm, cx - 25, cy - 25, cz, 50, 50, h, color=color)]
    if spout == "z-":
        p.append(ov.ruby_cylinder(nm + " spout", cx, cy, cz - 90, 6, 90, color=color, axis="z"))
    else:                                  # project sideways (clear of an in-line riser) then turn DOWN
        sa = "x" if "x" in spout else ("y" if "y" in spout else "z")
        ss = -1 if "-" in spout else 1
        way = {"x": [(cx, cy, cz + 12), (cx + ss * 58, cy, cz + 12), (cx + ss * 58, cy, cz - 60)],
               "y": [(cx, cy, cz + 12), (cx, cy + ss * 58, cz + 12), (cx, cy + ss * 58, cz - 60)]}[sa]
        p.append(ov.ruby_pipe_run(nm + " spout", way, 6, color=color))
    p.append(ov.ruby_cylinder(nm + " handwheel stem", cx, cy, cz + h, 5, 16, color=C_HANDLE, axis="z"))
    p.append(ov.ruby_cylinder(nm + " handwheel", cx, cy, cz + h + 16, 30, 10, color=C_HANDLE, axis="z"))
    return "\n".join(p)


def _flex_jumper(p, nm, flange_pt, approach_pt, col, start=10.0, maxlen=90.0):
    """Draw a corrugated flex jumper on the corridor-side pipe segment between the tote
    flange and the point where the rigid run arrives/turns (approach_pt). The jumper is
    co-linear with that segment and CAPPED inside it (start offset + length ≤ segment),
    so it can never overshoot past the turn into empty space."""
    d = (approach_pt[0] - flange_pt[0], approach_pt[1] - flange_pt[1], approach_pt[2] - flange_pt[2])
    L = (d[0] ** 2 + d[1] ** 2 + d[2] ** 2) ** 0.5
    if L <= start + 20:
        return                                   # segment too short for a jumper
    u = (d[0] / L, d[1] / L, d[2] / L)
    seg = min(maxlen, L - start - 6)
    p0 = tuple(flange_pt[i] + u[i] * start for i in range(3))
    p1 = tuple(flange_pt[i] + u[i] * (start + seg) for i in range(3))
    # Flex connectors draw in BRIGHT yellow (ov.C_FLEX), NOT the pipe's fluid color, so a jumper
    # stands out from the same-color pipe it splices. `col` is kept for call-site intent but ignored.
    p.append(ov.ruby_flex_run(nm + " flex jumper", [p0, p1], RP, color=ov.C_FLEX, elbow_r=6))


def _side_entry(p, nm, approach, x, yface, z, into, col, drop=-150, check=True):
    """Tote side-entry near the top, from the corridor.  `approach` = the FULL leg waypoint
    list UP TO the approach-turn point (x, af, z); this is concatenated with the in-tote
    penetration so the leg + entry is ONE pipe_run (every 90° gets a swept elbow).  Convention:
    the 90° approach turn is 120mm BEFORE the flange (≥75mm), flange on the corridor face,
    150mm penetration + elbow + 150mm vertical leg, ORANGE anti-siphon check valve on approach
    (unless `check=False` — e.g. when a single shared check sits upstream of a fill tee)."""
    af  = yface - into * 120                # approach turn, 120mm before the flange
    yin = yface + into * 150                # 150mm penetration into the tote
    p.append(ov.ruby_pipe_run(nm + " entry", list(approach) + [(x, yin, z), (x, yin, z + drop)], RP, color=col))
    p.append(ov.ruby_cylinder(nm + " flange", x, yface - into * 8, z, 36, 16, color=ov.C_STEEL, axis="y"))
    # flexible jumper — a corrugated section ON the corridor-side approach segment, co-linear
    # with the rigid pipe leaving the flange and CAPPED inside it so it never overshoots the
    # turn (de-couples the fixed tote from the semi-rigid panel — stress relief, 2026-07-29).
    _flex_jumper(p, nm, (x, yface - into * 8, z), approach[-1], col)
    if check:   # in-line on the straight Yd approach, just outside the flange
        p.append(check_valve(nm + " check valve", x, yface - into * 60, z, "y"))
    return af


def _bottom_pickup(p, nm, x, yface, into, col, riser_path):
    """Tote BOTTOM pickup: penetrate the corridor face near the base, the 90° bend points DOWN to
    the FLOOR (dip tube), then back up through the flange and along `riser_path` to the pump inlet
    — ONE pipe_run (elbows everywhere).  Flange (no foot valve — the pump self-primes and has an
    integral check valve, so a dedicated check here is redundant)."""
    z0  = ov.IBC_PALLET_H + 90              # base pickup level (just above the pallet)
    yin = yface + into * 150                # 150mm penetration into the tote
    # after the elbow inside the tote the dip tube descends only 50mm (a short standpipe), NOT to the floor
    wps = [(x, yin, z0 - 50), (x, yin, z0), (x, yface - into * 120, z0)] + list(riser_path)
    p.append(ov.ruby_pipe_run(nm + " pickup", wps, RP, color=col))
    p.append(ov.ruby_cylinder(nm + " pickup flange", x, yface - into * 8, z0, 36, 16, color=ov.C_STEEL, axis="y"))
    # flexible jumper capped inside the corridor-side approach (flange → riser turn)
    _flex_jumper(p, nm, (x, yface - into * 8, z0), (x, yface - into * 120, z0), col)


# Pumps in a SINGLE vertical column (like the filter row) at (PXC, CTR_Y); IN −Yd / OUT +Yd.
# Order bottom → top: [ACC-01 dead-leg], P-01, P-04, P-05, P-03 (ACC sits BELOW P-01 — swapped to
# drop the blue ACC knot to the column foot and lift the P-01 suction clear).
PSTACK = {"P-01": 615, "P-04": 940, "P-05": 1340, "P-03": 1740}  # base Z (P-01 raised +75mm)
PIY, POY = CTR_Y - (PVB_R + 30), CTR_Y + (PVB_R + 30)            # 1101 (IN) / 1261 (OUT) manifold Yd
def _piz(key): return PSTACK[key] + PVB_H - 18                    # port Z for a stack key

# X1 fresh-fill distribution fitting (top of the corridor, near the sealed end): a 4-WAY CROSS —
# +X X1 inlet, ±Yd to both Blue totes (IBC-1/IBC-2), −X the DV-01 blue recycle return.
X1_TEE_X, X1_TEE_Z = 5500, 2250
X1_TEE_Y = 1206 - ov.PUMP_PIPE_OD / 2   # on the spine face, aligned with the blue-recycle riser, so the
#   recycle rises STRAIGHT into the cross (one elbow, no top jog) — fewer connections (see skill_plumbing)

# Shared SURFACE perimeter lane for the two pipes that can't pass under the IBC tote / walkway grate
# (the tray-sump→P-04 suction and the DV-01 blue recycle): both run ON the walkway surface along the
# IBC −X face, STACKED in Z.  The lane sits above the FP bottom rail (z190) and just clear of the
# corridor-frame front upright (x4654).
SUCT_SURF_Z = ov.WALKWAY_H + 75            # 205 — brown suction height; blue recycle stacks +30 above
SUCT_XLANE  = ov.RAIL_X_R - 14             # 4635 — tray–IBC gap lane (−X clear of the blue supply-trunk drop at X4670)
# ── BACK-OF-PANEL routing: LONG vertical risers run BEHIND the rear panel (no pump ports there),
#    penetrating the ply; SHORT interconnects stay on the front.  Each long riser gets a UNIQUE Yd
#    lane, and the Yd-jog onto that lane is done on the FRONT (at x=PXC, unique z per port) BEFORE
#    penetrating, so the penetrations and the back verticals never share a plane. ──
BLANE = BACK_X + EQT + 60                                        # 5182 — back-of-panel riser plane
# Unique Yd lanes spread across the clear back band BETWEEN the corner uprights (near upright
# Yd1046–1096, far upright Yd1296–1346) → keep lanes inside ~1105–1285, ≥30mm apart:
BL_P01, BL_P05, BL_P04 = 1115, 1145, 1175                        # IN-side suction back-lanes
BL_P04OUT, BL_DVBR, BL_DVWST = 1195, 1225, 1250                  # OUT/top back-lanes (clear of far upright Yd1266)
SV_Z   = 1150                              # SV-02 sample tap — low on the P-04 discharge riser, in the gap
                                           # BETWEEN P-04 (top 1120) and P-05 (base 1340), ~1100mm for reach
DV_Z   = 2145                              # 3W-DV-02 center Z — dropped 75mm (room above P-03, top z1950) to
#   shorten the IBC-3 vertical drop; still well under the frame top rail (z2246) and above P-03.
#   PHASE-1 ONLY: in Phase 2 (sump_on_skid, the live water.skp) DV-02 lives on the pinhole-wall skid,
#   NOT here — and the shirt top is now PANEL_TOP_Z=1900, below DV_Z, so it no longer backs a corridor DV-02.
# DV02X is derived from SHIRT_X below (Phase-1 corridor DV-02 front-face X) — both defined after ACC_R.
# ACC-01 — SeaFlo bladder accumulator: a single BOTTOM port, plumbed as a vertical DEAD-LEG teed
# onto the Blue supply line (like the pumps/filters tee in, but the tank's only port is underneath).
ACC_Z0, ACC_R = 355, 63.5                   # ACC-01 base Z (raised +75mm; column FOOT, below P-01 — swapped); Ø127 body
ACC_PZ = ACC_Z0 + 28                        # ACC-01 IN/OUT port Z — at the BOTTOM of the body (the
                                            # SeaFlo's ports are underneath); pump-shaped, ports low
def acc_in():  return (PXC, CTR_Y + ACC_R + 30, ACC_PZ)   # +Yd (from P-01 OUT)
def acc_out(): return (PXC, CTR_Y - ACC_R - 30, ACC_PZ)   # −Yd (to the supply trunk)

SHIRT_X = PXC + ACC_R + 4                   # 5051.5 — pump-mount shirt front face (just clear of the ACC back)
DV02X   = SHIRT_X - DVB / 2                  # 5028.5 — 3W-DV-02 box BACK mounts FLUSH on the (raised) shirt front
#   face, so the shirt SUPPORTS DV-02; its feed + both run legs nudge +X to follow (toward the sealed end)

# ── #29 pump-flex run supports — two 18mm ply boards on the corridor SIDE walls ──────────────
# Each board fills the WINDOW between the front and rear side-posts (X FRONT_X+S..BACK_X), recessed
# FLUSH with the posts' wall-side face (rear-panel method), carried on 4 welded steel L-brackets
# (one leg welded to each post inner face, landing leg behind the ply → ply bolts to it).  The
# pump risers on that wall P-clip to the board.  FAR (film-plane side): DV-01 recycle + P-02
# discharge + P-01→ACC-01.  NEAR: P-02 suction (BV-03 mid) + P-05 inlet.
SB_X0, SB_X1 = FRONT_X + S, BACK_X           # board X span (front post inner +X face → back post inner −X face)
SB_FAR_Z  = (400, 820)                        # far board Z extent (~420, brackets the 2 clamp rows)
SB_NEAR_Z = (480, 900)                        # near board Z extent (~420)
SB_NEAR_UP_Z = (1260, 1950)                   # UPPER near board — backs BV-02 (P-05) + BV-06 (P-03) valves + risers; extended DOWN to the Z1300 P-05-inlet brown horizontal and UP to the Z1902 P-03 grey horizontal
# Riser planes — the pipe back sits ~2.5mm off each board's corridor face (RP + gap), i.e. flush on it.
SB_RISER_YD_FAR  = YD_FAR - EQT - RP - 2.5    # 1285 — far risers (DV-01 re-routed here; P-02 disch/P-01 nudged)
SB_RISER_YD_NEAR = YD_NEAR + EQT + RP + 2.5   # 1077 — near risers (P-02 suction nudged here; P-05 already ~here)
SB_FAR_RISERS_X  = (4873, 4900, 4984)         # DV-01 recycle · P-02 discharge · P-01→ACC-01
SB_NEAR_RISERS_X = (4825, 5070)               # P-02 suction · P-05 inlet
SB_FAR_CLAMP_Z   = (480, 740)                 # 2 clamp rows (far)
SB_NEAR_CLAMP_Z  = (560, 820)                 # 2 clamp rows (near)
C_CLIP = "#55575e"                            # cushioned P-clip strap

def support_boards(sides=("far", "near", "near-upper")):
    """The side-wall ply run-support boards + welded L-brackets + riser P-clips (#29).

    `sides` selects which boards to emit (far / near / near-upper) so the construction
    sequence can stage the FAR board on a later click; defaults to all (overview/water)."""
    p = []
    bw = SB_X1 - SB_X0
    LT, LL, LH = 6, 45, 50                     # bracket leg thickness / landing-leg length / bracket height
    for side, wall_yd, ddir, (z0, z1), ryd, risers_x, clamp_z in (
            ("far",  YD_FAR,  -1, SB_FAR_Z,  SB_RISER_YD_FAR,  SB_FAR_RISERS_X,  SB_FAR_CLAMP_Z),
            ("near", YD_NEAR, +1, SB_NEAR_Z, SB_RISER_YD_NEAR, SB_NEAR_RISERS_X, SB_NEAR_CLAMP_Z),
            # UPPER near board — two X4898 segments: BV-02 (P-05) Z1321-1481 + BV-06 (P-03) Z1721-1881.
            # 2 clip rows land on EACH segment (the 240mm gap between them carries no pipe).
            ("near-upper", YD_NEAR, +1, SB_NEAR_UP_Z, SB_RISER_YD_NEAR, (BV_FWD_X,), (1370, 1440, 1770, 1840))):
        if side not in sides:
            continue
        by = wall_yd - EQT if ddir < 0 else wall_yd        # ply origin Yd (flush with the wall-side post face)
        back_yd = wall_yd                                   # ply back face = the post wall-side face
        face_yd = wall_yd - EQT if ddir < 0 else wall_yd + EQT   # ply CORRIDOR face (clips attach here)
        p.append(ov.ruby_box(f"Pump-run support board ({side}, 18mm ply)",
                             SB_X0, by, z0, bw, EQT, z1 - z0, color=ov.C_PLY))
        for px, xdir in ((SB_X0, +1), (SB_X1, -1)):        # front / back post inner face
            for bz in (z0 + 35, z1 - 35):
                lx = px if xdir > 0 else px - LT           # welded leg — flat on the post inner face
                p.append(ov.ruby_box(f"Support L-bracket weld leg ({side})",
                                     lx, by, bz - LH / 2, LT, EQT, LH, color=ov.C_STEEL))
                ly = back_yd if ddir < 0 else back_yd - LT  # landing leg — behind the ply back face
                lxx = px if xdir > 0 else px - LL
                p.append(ov.ruby_box(f"Support L-bracket landing leg ({side})",
                                     lxx, ly, bz - LH / 2, LL, LT, LH, color=ov.C_STEEL))
        # riser P-clips — one per riser at each clamp row, bridging the riser back to the board face
        for rx in risers_x:
            for cz in clamp_z:
                y_lo = min(face_yd, ryd - RP - 2); y_hi = max(face_yd, ryd + RP + 2)
                p.append(ov.ruby_box(f"Riser P-clip ({side})", rx - 14, y_lo, cz - 8,
                                     28, y_hi - y_lo, 16, color=C_CLIP))
    # near-upper board also backs two HORIZONTALS: P-05-inlet brown (Z1300) + P-03 grey (Z1902)
    if "near-upper" in sides:
        for hx, hz in ((4960, 1300), (5020, 1300), (4945, 1902)):
            p.append(ov.ruby_box("Riser P-clip (near-upper)", hx - 14, YD_NEAR + EQT, hz - 12,
                                 28, (SB_RISER_YD_NEAR + RP + 2) - (YD_NEAR + EQT), 24, color=C_CLIP))
    return "\n".join(p)


def equipment(sump_on_skid=False, boards=("far", "near", "near-upper")):
    """The corridor pump panel: P-01 Blue, [P-04 tray-drain], P-05 Brown-drain, P-03 Waste-drain,
    ACC-01, [SV-02 + 3W-DV-02].  (P-02 + the filters live on the pinhole wall.)  Pumps UPRIGHT.

    sump_on_skid=True (Phase 2 — water.skp): the tray-sump processing (P-04, SV-02, 3W-DV-02) is
    RELOCATED onto the filter skid, so they are OMITTED here and ACC-02 (the recycled-spray
    accumulator) drops into P-04's vacated column slot instead."""
    p = []
    pumps = [("Pump P-01 (Blue supply)", "P-01"),
             ("Pump P-05 (Brown drain)", "P-05"), ("Pump P-03 (Waste drain)", "P-03")]
    if not sump_on_skid:
        pumps.insert(1, ("Pump P-04 (Tray drain)", "P-04"))
    for label, key in pumps:
        p += pump_unit(label, PXC, CTR_Y, PSTACK[key], axis="y")
    # ACC-01 — SeaFlo SFAT-075-125-01 (0.75 L): Ø127 × 200mm overall (per component-dimension-audit).
    # Drawn like the filters/pumps: a vertical body with IN/OUT on OPPOSITE sides (IN +Yd from
    # P-01, OUT −Yd to the trunk), in line on the Blue supply.
    acc_h = 174                                  # body 174 + 26 cap = 200 overall (to spec)
    p.append(ov.ruby_cylinder("ACC-01 Accumulator", PXC, CTR_Y, ACC_Z0, ACC_R, acc_h, color=ov.C_ACC))
    p.append(ov.ruby_cylinder("ACC-01 head", PXC, CTR_Y, ACC_Z0 + acc_h, ACC_R + 2, 26, color=CDK, axis="z"))
    for tag, sd in (("in", +1), ("out", -1)):
        y0 = (CTR_Y + ACC_R) if sd > 0 else (CTR_Y - ACC_R - 30)
        p.append(ov.ruby_cylinder(f"ACC-01 {tag} port", PXC, y0, ACC_PZ, RP, 30, color=CDK, axis="y"))
    if sump_on_skid:
        # P-02 (recycled-spray pump) RELOCATED from the pinhole wall to the corridor column, in P-04's
        # vacated slot — IBC-3 buffer (corridor) → P-02 → ACC-02 (on the filter skid).  Upright like the
        # rest of the column: IN −Yd (from the IBC-3 tap), OUT +Yd (to the ACC-02 cross-panel run).
        p += pump_unit("Pump P-02 (Brown recycle)", PXC, CTR_Y, PSTACK["P-04"], axis="y")
    else:
        # SV-02 sample tap — TEED off the P-04 DISCHARGE RISER low down (the +Yd lane POY+50, between
        # P-04 and P-05 at ~1100mm) out to the −X aisle for reach; spout drops for cup access.
        sv_x = PXC - 95
        sv_y = POY + 50                        # the discharge riser's Yd lane (1311) at this height
        p.append(tee("SV-02 tap tee", PXC, sv_y, SV_Z + 25, run="z", branch="x-"))
        p.append(ov.ruby_pipe_run("SV-02 tap", [(PXC, sv_y, SV_Z + 25), (sv_x + 25, sv_y, SV_Z + 25)], RP, color=ov.C_VALVE))
        p.append(sample_valve("SV-02 sample valve", sv_x, sv_y, SV_Z, h=60))
        # 3W-DV-02 — Stage-A diverter above the stack (input underside; run to Brown −Yd / Waste +Yd)
        p.append(diverter("3W-DV-02", DV02X, CTR_Y, DV_Z, run="y", branch="z-", handle="x-", color=ov.C_VALVE))
    p.append(support_boards(sides=boards))       # #29 — side-wall ply run-support boards + L-brackets
    return "\n".join(p)


def plumbing(part="all", sump_on_skid=False):
    """Stage-A tray-drain chain (P-04 → SV-02 → 3W-DV-02 → IBC-3 Brown / IBC-4 Waste) + the Blue
    supply (Blue #1 → P-01 → ACC-01 → trunk).  Routing rules: every segment is single-axis (no
    diagonals); each pump port leaves with a perpendicular −X stub; each run gets its OWN X depth
    lane so pipes never share a plane (no pipe-through-pipe); horizontal runs sit at Z levels
    clear of the pump bodies (tops ≤ 770).

    part="corridor" omits the over-walkway sump-suction line (the only run that crosses the
    walkway); part="sump" is ONLY that line + its strainer foot; "all" (default) = both, and is
    byte-identical to the original (the sump line was the first thing emitted, so it stays first)."""
    p = []
    sump = []
    def pipe(nm, wp, col): p.append(ov.ruby_pipe_run(nm, wp, RP, color=col))
    # gpipe / spipe: GUARDED builders — no-op when the tray-sump chain is relocated to the skid.
    def gpipe(nm, wp, col):
        if not sump_on_skid: p.append(ov.ruby_pipe_run(nm, wp, RP, color=col))
    def spipe(nm, wp, col):
        if not sump_on_skid: sump.append(ov.ruby_pipe_run(nm, wp, RP, color=col))
    def pin(k):  return (PXC, PIY, _piz(k))              # IN  tip (−Yd manifold side)
    def pout(k): return (PXC, POY, _piz(k))             # OUT tip (+Yd manifold side)
    # ── #29 — braided ½" flex jumper on BOTH ports of every corridor pump (vibration isolation, 2026-08-07).
    #    A short corrugated jumper de-couples each pump from the rigid PVC run so vibration can't fatigue a
    #    solvent-weld joint. IN leaves −Yd, OUT leaves +Yd (manifold convention); _flex_jumper caps it inside
    #    the first segment so it can't overshoot the turn. P-04's suction (1" tray hose) + its discharge
    #    jumper live on the skid (pinhole panel), so only the 4 corridor pumps are jumpered here.
    _p4lbl = "P-02" if sump_on_skid else "P-04"
    for _pk, _sk, _jc in (("P-01", "P-01", ov.C_BLUE), ("P-05", "P-05", ov.C_IBC_BROWN),
                          ("P-03", "P-03", ov.C_IBC_WASTE), (_p4lbl, "P-04", ov.C_IBC_BROWN)):
        _jz = _piz(_sk)
        _flex_jumper(p, f"{_pk} suction jumper",   (PXC, PIY, _jz), (PXC, PIY - 38, _jz), _jc, start=2, maxlen=24)
        _flex_jumper(p, f"{_pk} discharge jumper", (PXC, POY, _jz), (PXC, POY + 38, _jz), _jc, start=2, maxlen=24)
    tip = DVB / 2 + DVL                                  # 78 — diverter port-stub tip
    dvm, dvp = CTR_Y - tip, CTR_Y + tip                  # 1103 / 1259 — DV-02 run−/run+ Yd
    xe  = ov.IBC_COL_X + 300                             # 4974 — tote side-entry X
    bz  = ov.IBC_H_1000 - 38                             # 1130 — Brown entry, threaded into the TOP of the brown
    #   bottle (z168–1148): above the P-04 suction approach (tops at z1102) and below the bottle top.
    #   (The old 1276 sat 128mm ABOVE the brown tote, at the Blue #1 pallet level — looked like the blue IBC.)
    wz  = MERGE4[2]                                       # 1230 — Waste entry
    blz = ov.IBC_H_1000 + ov.IBC_PALLET_H + 64           # 1400 — Blue near top

    # P-04 SUCTION ← processing-tray SUMP (near-right corner).  COMPROMISE: this run can't pass under
    # the IBC tote (it sits on its pallet on the floor — no room under it) and there isn't room under
    # the walkway grate either, so it runs ON the walkway SURFACE around the perimeter: up from the
    # sump, +X to the tray–IBC gap, then +Yd along the IBC −X face into the corridor, across (below the
    # pump bodies) and up into P-04.  The surface run sits ABOVE the FP bottom rail (z190), so it stands
    # ~75mm proud of the deck and the operator steps over it.
    sumpX, sumpY = ov.PROC_TRAY_DRAIN_X, ov.PROC_TRAY_DRAIN_YD + 75          # 2399,155 — center pickup (relocated from the IBC corner; = PROC_TRAY_DRAIN_X)
    sump_foot_z  = ov.PROC_TRAY_FLOOR_Z_LOW - ov.PROC_TRAY_SUMP_Z + 3        # 3 — pickup foot near the sump-well bottom (Z0),
    #   so the suction actually evacuates the 20mm-deep well (was Z20 = the floor lip, above the well)
    z04   = _piz("P-04")
    srz   = SUCT_SURF_Z                  # 205 — surface run: above the deck (130) AND the FP bottom rail (190)
    xlane = SUCT_XLANE                   # 4643 — tray–IBC gap lane, clear of the corridor-frame front upright
    xrise = PXC - 84                    # 4900 — rise lane −X of the pump column / ACC body & blue out-trunk (PXC)
    ybr   = PIY - 4                     # 1097 — port-approach Yd into the −Yd-facing IN port (clear of the P-01 suction Yd1071)
    gapyd = ov.RWK_RIBBON_NOTCH_YDS[2]  # 1194 — the lane-2 outer-beam notch Yd (single-sourced so the pipe crosses
    #   exactly where the beam is slotted); threads the GAP between the DV-01 grey-waste (Yd1147) and blue-recycle
    #   (Yd1241) floor lanes — clear of the P-05 brown feed (Yd1101, z258).
    # Sump pickup (rev 2026-08-03 — CENTER pickup): the foot sits DOWN IN the near-rim gutter's center
    # pickup well at X=sumpX (=PROC_TRAY_DRAIN_X, X2399), with the strainer on it.  The pipe rises STRAIGHT
    # up out of the well, then runs +X UNDER the walkway (flush at RIBBON_Z=104.5 — above the spray-beam top
    # ~Z78 and just under the near-walkway arm soffit Z107) to the IBC-end ribbon lane (slx), where it rejoins
    # the ORIGINAL ribbon path: up-and-over the first cantilever (Rule 5), across the notched outer beam, down
    # the tray-edge slot, and into the P-04 rise/port approach.  (The old routing put the pickup at the CORNER
    # ribbon lane — stale from the pre-relocation dual-axis sump.)
    slx = RIBBON_LANE_X[2]                              # lane-2 X (the IBC-end ribbon lane the suction joins)
    sump_foot = (sumpX, sumpY, sump_foot_z)             # pipe intake == strainer point at the CENTER pickup (X=PROC_TRAY_DRAIN_X); SINGLE SOURCE so the strainer stays welded to the pipe's foot
    spipe("Tray sump -> P-04 suction",
         [sump_foot,                                   # pickup foot DOWN IN the center pickup well — STRAIGHT down, no jog
          (sumpX, sumpY, RIBBON_Z),                    # straight UP out of the center well to flush/under-grate height
          (slx, sumpY, RIBBON_Z),                      # UNDER the walkway: +X along the near rim to the IBC-end ribbon lane (clears the spray beam below, the arm soffit above)
          (slx, RIBBON_YD_UP, RIBBON_Z),               # flat 90° elbow, +Yd along the ribbon lane to just before the first cantilever
          (slx, RIBBON_YD_UP, RIBBON_OVER_Z),           # UP through the grate, OVER the cantilever (Rule 5)
          (slx, RIBBON_YD_DOWN, RIBBON_OVER_Z),         # +Yd over the cantilever, past it
          (slx, RIBBON_YD_DOWN, RIBBON_Z),              # DOWN through the grate into the corridor
          (slx, gapyd, RIBBON_Z),                       # +Yd to the corridor Yd (FLUSH under the grate)
          (RIBBON_SLOT_X, gapyd, RIBBON_Z),             # +X through the OPEN-TOP NOTCH in the outer beam to the drop slot, at flush
          (RIBBON_SLOT_X, gapyd, 65),                   # DOWN the tray-edge↔upright slot (X>4599 → clear of the carriage) to the corridor entry Z
          (xrise, gapyd, 65),                           # +X to the rise lane (existing corridor routing — unchanged from here)
          # ---- ORIGINAL P-04 port approach (rise + port) ----
          (xrise, gapyd, z04),                          # RISE to the IN-port height
          (xrise, ybr, z04),                            # −Yd at the IN-port height to the port-approach lane
          (PXC, ybr, z04), pin("P-04")],                # +X straight into the −Yd-facing IN port
         ov.C_IBC_BROWN)
    if not sump_on_skid:
        sump.append(ov.ruby_cylinder("Tray sump strainer foot", *sump_foot, 14, 36, color=CDK, axis="z"))
    # P-04 DISCHARGE → up the BACK of the panel (clear of the OUT-port stack), back to the front
    # ABOVE the pumps where it's clear → SV-02 (in-line) → DV-02 underside branch.
    # P-04 OUT leaves convention-style: a short +Yd stub straight OUT of the +Yd-facing OUT port to a
    # front riser, up ABOVE the pumps (clear), then back in to SV-02 (in-line) and DV-02.
    gpipe("P-04 -> SV-02 -> DV-02",
         [pout("P-04"), (PXC, POY + 50, z04), (PXC, POY + 50, 2035), (PXC, CTR_Y, 2035),
          (DV02X, CTR_Y, 2035), (DV02X, CTR_Y, DV_Z - tip)],   # jog at z2035 (+75mm, CLEARS the P-03 head
          # top z1950 by ~75mm), -X to the nudged DV-02, then up into it
         ov.C_IBC_BROWN)   # P-04 OUT → up its OWN +Yd lane (POY+50, clear of the pump-discharge lane POY+30)
    #   → jog to the CENTRAL lane (CTR_Y) above the pumps → SV-02 tap → VERTICALLY
    #   into the underside (z−) branch; central lane keeps the feed/SV-02 clear of the ±Yd diverter legs
    # DV-02 → IBC-3 Brown — LEAVE the −Yd run port collinear (a 60mm −Yd lead-out so the first elbow is a
    # clean interior 90°, not a malformed sprout off the port) → +X to the panel → 90° turn +Yd (toward the
    # film-plane wall) INTO the ~27mm SHIRT↔PANEL gap → drop DOWN the gap on the CTR_Y clear lane (Yd1180,
    # BETWEEN the spacer-block columns Yd1096-1136/1226-1266 and clear of the X3/X4 port runs) → at the bottom
    # −Yd along the gap to the entry lane (Yd1073, clears the P-04 head Yd1128 AND −Yd of the shirt edge 1096
    # so the −X exit needs no shirt notch) → −X out to the tote entry.
    cz = 5090   # chase centre X (shirt back 5076.5 ↔ panel front 5104)
    if not sump_on_skid:   # DV-02→IBC-3 recycle — OBSOLETE in the new topology (DV-02 now feeds the filters)
        _side_entry(p, "DV-02 -> IBC-3 (Brown)",   # no CV-3 — P-04 has an integral check valve (check=False)
                    [(DV02X, dvm, DV_Z), (DV02X, dvm - 60, DV_Z),   # leave the −Yd run port collinear (clean elbow), then
                     (cz, dvm - 60, DV_Z), (cz, CTR_Y, DV_Z),       # +X to the panel, then +Yd INTO the gap (toward the film-plane wall)
                     (cz, CTR_Y, bz), (cz, dvm - 30, bz),           # DROP the gap on the clear lane, then −Yd to the entry lane (clears the head + the BV-02→P-05 inlet at Yd1078)
                     (DV02X, dvm - 30, bz)],                        # −X out to the entry approach point
                    DV02X, YD_NEAR, bz, -1, ov.C_IBC_BROWN, check=False, drop=-50)   # short 50mm dip tube inside the tote
    # DV-02 → IBC-4 merge — waste port → drop below the bracket → behind the panel (own lane) → down
    # → +X past the risers to the merge tee (jog to the merge Yd at x=MERGE, clear of the back verticals).
    # leave the +Yd port, turn toward the SEALED END and run 400mm along the top (Yd1229 clears the far
    # upright at 1266 now that the short-port diverter pulled dvp in to 1214), THEN drop and into the merge.
    dvwx = MERGE4[0] - 115                                # drop −x of the tee (top run 75mm shorter) so the
    #   horizontal approach seats on the −x run port as a clear run, not a stub right at the drop
    gpipe("DV-02 -> IBC-4 merge",
         [(DV02X, dvp, DV_Z), (DV02X, dvp + 31, DV_Z), (DV02X, dvp + 31, DV_Z - 45),   # +Yd stub EXTENDED (+40) so the panel
          #   penetration + the +X run clear the spine root (Yd1206-1224) at the panel-spine join, then drop below the rear-panel
          (dvwx, dvp + 31, DV_Z - 45), (dvwx, MERGE4[1], DV_Z - 45),                    # +X, then −Yd to the spine lane
          (dvwx, MERGE4[1], wz), MERGE4], ov.C_IBC_WASTE)   # high (round-hole spine crossing); DROP on the spine, then
    #   a horizontal +x run that SEATS on the merge's −x run port (was dropping inside the tee body)
    # 3-way merge: tote entry on +x (run), DV-02 waste on −x (run), DV-01 waste rises into the z− branch
    p.append(tee("IBC-4 waste merge tee", MERGE4[0], MERGE4[1], MERGE4[2], run="x", branch="z-"))
    xe4 = ov.IBC_COL_X + 830                              # 5504 — entry +130 toward the sealed end
    _side_entry(p, "IBC-4 (Waste)", [MERGE4, (xe4, MERGE4[1], wz)], xe4, YD_FAR, wz, +1, ov.C_IBC_WASTE, check=False)   # no CV-4 — P-02/P-04 have integral check valves

    # BLUE #1 → P-01 suction: P-01 IN → front Yd-jog onto its back-lane → penetrate the panel →
    # vertical riser BEHIND the panel (clear of the pump-port stack) → back to the front → near tote.
    # IN approached convention-style (P-04 reference): −Yd stub straight out of the IN port, around
    # the front of the body, up the threading lane (between body Yd1131+ and the near upright Yd≤1096)
    # behind the panel, to the tote.
    z01 = _piz("P-01")
    # BV-01 must be reachable from the −X WALKWAY, so the suction LOOPS forward to a short vertical section in
    # the corridor front (bvx) — BV-01 at reach height, handle to the walkway — then turns +X BACK through the
    # shirt + panel (round holes) and rises BEHIND the panel, OFF the operator's front zone, before jogging −Yd
    # into Blue #1.  Relocating the tall riser to the rear declutters the front for access to the brown valves.
    bvx, bvy = FRONT_X + 221, YD_NEAR + 67       # 4875 / 1113 — corridor-front access lane (+115 toward the sealed end), clear of the front
    #   upright (Yd≤1096) AND −Yd of the pump bodies (Yd≥1128) the +X return run passes
    beh_x = 5200                                 # behind-panel riser X — flange (r36) clears the near upright (x≤5154)
    #   and the riser/flange sit on the Yd1113/1038 lanes, −Yd-separated from the X4 waste riser's Yd1196 lane
    loopz = 1210                                 # loop top — above BV-01 (z1000) AND the rear-panel bracket (z≤1178),
    #   in the P-04↔P-05 gap; where the line turns +X to the rear
    _side_entry(p, "Blue #1 -> P-01 suction",   # flooded suction + P-01's integral check → no foot valve (check=False)
                [pin("P-01"), (PXC, PIY - 30, z01), (bvx, PIY - 30, z01), (bvx, bvy, z01),
                 (bvx, bvy, loopz),                          # UP the FRONT vertical (BV-01 on it, accessible)
                 (beh_x, bvy, loopz),                        # +X BACK through the shirt + panel (round holes), −Yd of the pumps
                 (beh_x, bvy, blz)],                         # UP the BEHIND-panel riser to the tote-entry height
                beh_x, YD_NEAR, blz, -1, ov.C_BLUE, check=False, drop=-50)   # then −Yd into Blue #1 + 50mm dip tube
    p.append(ball_valve("BV-01 (P-01 suction)", bvx, bvy, 1000, "z", hdir="-x"))   # FRONT vertical section, handle faces the −X walkway operator
    # Blue supply IN LINE through ACC-01 (like a filter in the chain): P-01 OUT → ACC IN (+Yd),
    # ACC OUT (−Yd) → trunk out the mouth to the spray bar.
    # The ACC-IN elbow goes OUT HORIZONTALLY (+Yd into the aisle, clear of the P-01 head below) before
    # dropping to the P-01 OUT blue riser — NOT straight down over the pump.
    inby = SB_RISER_YD_FAR                                 # 1285 — #29: IN riser sits on the FAR support board (flush), still +Yd of the ACC-IN port (1274.5) for a clean drop-in and clear of the Blue #2 IBC near face (1316)
    pipe("P-01 -> ACC-01 (in)",
         [pout("P-01"), (PXC, inby, _piz("P-01")), (PXC, inby, ACC_PZ), acc_in()], ov.C_BLUE)
    # ACC-01 OUT → supply trunk → out to the gap past the tray right edge (GAPX), dropped to z60 ready
    # to cross to the outside-rim strip (tap01_supply continues it AROUND the tray to BV-05/TAP-01).
    # Leave the −Yd OUT port OUTWARD (−Yd), then run +Yd to the gap in the clear band BETWEEN the P-01 head
    # top (z490) and the ACC body bottom (z540) — z515 clears both by ~15mm.  (The old route ran +Yd at the
    # port's z568 and TUNNELED through the ACC body; z490 then grazed the P-01 head top.)
    trz = 235     # corridor-entry crossing height — dropped to DV-01's low lane (DV01_CZ=235) so the trunk is
    #   OUT of the operator's way at the mouth (was z515, mid-shin); −Yd of the ACC/pump bodies so it clears them
    pipe("Blue supply trunk -> spray bar / TAP-01 (off-panel)",
         [acc_out(), (PXC, CTR_Y - ACC_R - 50, ACC_PZ), (PXC, CTR_Y - ACC_R - 50, trz),
          (PXC, GAP_CORR_Y, trz), (BLUE_TRUNK_HANDOFF_X, GAP_CORR_Y, trz),
          (BLUE_TRUNK_HANDOFF_X, GAP_CORR_Y, 60)], ov.C_BLUE)   # drop PAST the FP bottom rail (clears it)
    if part == "sump":
        return "\n".join(sump)
    if part == "corridor":
        return "\n".join(p)
    return "\n".join(sump + p)      # "all" — sump first (original order), then the corridor chains


def end_wall():
    """Faint sealed END WALL slice (X-ports live on it).  Built on the Context layer so it does
    NOT clutter the pipes-only 'Plumbing' scene."""
    return ov.ruby_box("End wall (context)", ov.C_LEN, 0, 0, ov.WALL_T, ov.C_WID, ov.C_HGT,
                       color=ov.C_SHELL, alpha=0.12)


def drains_ports(sump_on_skid=False):
    """The X1/X3/X4 end-wall bulkhead ports + their lines: X1 fresh-fill (single check → tee →
    BOTH Blue totes) and the X3/X4 drains (tote-bottom pickups → panel pumps P-05/P-03 → ports).
    The pumps themselves are on the panel (equipment())."""
    p = []
    def pipe(nm, wp, col): p.append(ov.ruby_pipe_run(nm, wp, RP, color=col))
    ew = ov.C_LEN                                        # 5893 — end wall

    # ── X1 FILL: camlock → in-line one-way valve → STRAIGHT pipe → T-connector → BOTH Blue totes
    #    (IBC-1 / IBC-2).  ONE check on the inlet; no per-branch checks. ──
    x1z, tx, ty = X1_TEE_Z, X1_TEE_X, X1_TEE_Y   # ty: cross on the spine face, aligned with the recycle riser
    p.append(ov.ruby_cylinder("X1 fill camlock (end wall)", ew - 60, ty, x1z, 26, 60, color=ov.C_STEEL, axis="x"))
    p.append(check_valve("X1 one-way valve", ew - 200, ty, x1z, "x"))   # in-line, just after the camlock
    pipe("X1 camlock -> one-way -> cross (straight)", [(ew - 60, ty, x1z), (tx, ty, x1z)], ov.C_BLUE)
    # 4-WAY CROSS: +X X1 inlet, ±Yd to the two Blue totes (IBC-1/IBC-2), −X the DV-01 blue
    # recycle return (rises STRAIGHT up the spine into this −X port — one elbow, no top jog).
    p.append(cross("X1 fill cross", tx, ty, x1z, "x", "y"))
    # each outlet runs STRAIGHT ±Yd off the tee's run port into its tote (no −X detour)
    for yface, into, nm in ((YD_NEAR, -1, "Blue #1 (IBC-1)"), (YD_FAR, +1, "Blue #2 (IBC-2)")):
        _side_entry(p, f"X1 fill -> {nm}", [(tx, ty, x1z)], tx, yface, x1z, into, ov.C_BLUE, check=False)

    # ── Blue EQUALIZATION: a low 1" cross-connect tying the BOTTOMS of the two Blue totes together
    #    so their levels equalize.  Straight across, near the sealed end. ──
    beqz, beqx = ov.IBC_H_1000 + ov.IBC_PALLET_H + 40, 5500   # ~1376 — just above the Blue tote bottoms
    p.append(ov.ruby_pipe_run("Blue equalization (IBC-1 <-> IBC-2)",
        [(beqx, YD_NEAR - 150, beqz), (beqx, YD_FAR + 150, beqz)], 16, color=ov.C_BLUE))   # 1" pipe
    p.append(ov.ruby_cylinder("Blue eq flange (IBC-1)", beqx, YD_NEAR - 8, beqz, 36, 16, color=ov.C_STEEL, axis="y"))
    p.append(ov.ruby_cylinder("Blue eq flange (IBC-2)", beqx, YD_FAR - 8, beqz, 36, 16, color=ov.C_STEEL, axis="y"))

    # ── IBC-3 BROWN: ONE shared bottom tap (dip tube → floor) → T-junction (cp.BROWN_TAP) that
    #    feeds BOTH P-05 (drain) and P-02 (wall filter loop) — a single tote penetration. ──
    tx3, ty3, tz3 = BROWN_TAP
    yin3 = YD_NEAR - 150                                  # 896 — penetration into the Brown tote
    p.append(ov.ruby_pipe_run("IBC-3 (Brown) bottom tap (shared P-02/P-05)",
        [(tx3, yin3, tz3 - 100), (tx3, yin3, tz3), (tx3, ty3 - 36, tz3)], RP, color=ov.C_IBC_BROWN))  # dip tube EXTENDED to tz3-100 (bottom stays z208) — into the tee's −Yd branch end
    p.append(ov.ruby_cylinder("IBC-3 (Brown) tap flange", tx3, YD_NEAR - 8, tz3, 36, 16, color=ov.C_STEEL, axis="y"))
    p.append(tee("IBC-3 (Brown) tap T", tx3, ty3, tz3, run="x", branch="y-"))   # dip on −Yd; P-02 −X / P-05 +X
    # (no check valve at the bottom tap — the shared bottom tap is just the tee feeding P-02/P-05
    #  through BV-03/BV-02; the pumps have integral checks)
    if sump_on_skid:
        # IBC-3 (Brown) tap → P-02 (recycle pump) suction: off the tap's −X port → riser → +X into
        # P-02's −Yd IN port.  P-02 sits in the P-04 column slot; its IN Yd == the tap Yd (both
        # CTR_Y−(PVB_R+30)), so the run is co-planar in Yd — riser then a straight +X into the port.
        p2i = pump_in(PXC, CTR_Y, PSTACK["P-04"], "y", 1)
        pipe("IBC-3 tap -> P-02 suction",
             [(tx3 - 19, ty3, tz3),            # off the tap's −X run port (low, z308)
              (tx3 - 55, ty3, tz3),            # −X nudge (X4825) clear of BV-01 (X4857-4894, the P-01 suction valve on the blue line)
              (tx3 - 55, SB_RISER_YD_NEAR, tz3),    # −Yd onto the NEAR support-board riser plane (Yd1077, flush on the board)
              (tx3 - 55, SB_RISER_YD_NEAR, p2i[2]), # UP the riser on the board
              (PXC, SB_RISER_YD_NEAR, p2i[2]),      # +X to the pump column
              p2i], ov.C_IBC_BROWN)            # +Yd INTO P-02's −Yd IN port (swept elbow at the +X→+Yd vertex)
        p.append(ball_valve("BV-03 (P-02 suction)", tx3 - 55, SB_RISER_YD_NEAR, 950, "z", hdir="-x"))   # isolation on the P-02 suction riser (near board); handle faces −X toward the cargo door
    # P-05 (Brown drain) suction: shared tap T → +X run end → rise to P-05 IN (−Yd manifold)
    p5i = (PXC, PIY, _piz("P-05")); p5o = (PXC, POY, _piz("P-05"))
    z05 = _piz("P-05")
    rx = BV_FWD_X       # BV-02 riser/valve X — pulled to the walkway edge (operator reach)
    shirt_rx = 5070     # shirt riser X (in the 5052-5077 band): the brown still routes +X off the tee and DOWN
    #   the shirt (P-clipped for support) exactly as it did before the b492a2a9 flip; BV-02 then sits on a
    #   FORWARD loop stepped −X off that shirt riser.  (The flip had dropped the shirt run and backtracked the
    #   leg over the tee — this restores the clean tee join AND keeps BV-02 forward.)
    zloop = 1300        # loop level (P-04↔P-05 gap): step −X from the shirt riser to the BV-02 riser, below the valve
    pipe("Brown tap -> P-05 inlet",
         [(tx3 + 30, ty3, tz3), (shirt_rx, ty3, tz3), (shirt_rx, BV02_YD, tz3), (shirt_rx, BV02_YD, zloop),
          (rx, BV02_YD, zloop), (rx, BV02_YD, z05), (PXC, BV02_YD, z05), p5i],
         #   tee +X end → +X to SHIRT riser → −Yd → up the shirt → −X (forward) to the BV-02 riser → up through
         #   BV-02 → +X stub into the IN port
         ov.C_IBC_BROWN)
    p.append(ball_valve("BV-02 (P-05 suction)", rx, BV02_YD, z05 - 85, "z", hdir="+y"))   # handle swings +Yd into the open corridor (clear of the near support board so it can be turned)
    p.append(ov.ruby_cylinder("X3 Brown drain port (end wall)", ew - 60, COL_L, 1700, 22, 60, color=C_CHECK, axis="x"))
    # P-05 OUT → +Yd stub → step onto a clear back lane (between the spine +Yd face 1224 and the far
    # upright 1266; +Yd of the pump body 1231) — the −Yd step is done in the OPEN −X of the shirt, NOT in
    # the chase — then STRAIGHT +X through the shirt + panel (round holes) and behind the panel all the way
    # to the end wall (extending the straight run), then −Yd onto the X3 port lane past the spine, and down.
    x3lane = 1245
    pipe("P-05 -> X3 end-wall port",   # OUT leaves with a +Yd stub straight out of the OUT port
         [p5o, (PXC, POY + 15, p5o[2]), (5030, POY + 15, p5o[2]), (5030, x3lane, p5o[2]),
          (ew - 130, x3lane, p5o[2]), (ew - 130, COL_L, p5o[2]),
          (ew - 130, COL_L, 1700), (ew - 60, COL_L, 1700)], ov.C_IBC_BROWN)

    # ── IBC-4 WASTE: bottom pickup → grey SPINE riser → WRAP back through the panels → BV-06 → P-03 ──
    # BV-06 valve geometry copies BV-02 (riser at rx6/BV02_YD, valve 110 below the port, −X + +Yd stub
    # into the IN port).  Its X4 feed can't cross the chase frame upright on the IN-port lane, so it WRAPS:
    # down off BV-06, −X toward the walkway THROUGH the pump gap (P-05 top z1520 ↔ P-03 base z1740), +Yd
    # to the spine lane (1206, BETWEEN the two uprights 1096/1266), then +X back through the shirt + panel
    # (perpendicular round holes) to the grey X4 pickup riser on the spine.
    p3i = (PXC, PIY, _piz("P-03")); p3o = (PXC, POY, _piz("P-03"))
    z03 = _piz("P-03")
    rx6 = BV_FWD_X                 # BV-06 riser X — pulled to the walkway edge (operator reach), like BV-02
    turn6 = 1700                   # turn partway down the riser below BV-06 — in the pump gap (z1520–1740)
    corr_x = 5020                  # −Yd-jog X — pulled IN close to the shirt face (5051.5), just −X of it, so the
    #   grey loop sits tight to the shirt instead of bulging toward the walkway (jog is in the P-05↔P-03 gap)
    spine_yd = YD_FAR - 120        # 1196 — grey-riser lane CLAMPED to the spine front face (1206); also the
                                   #   bottom-pickup approach Yd, so the riser rises STRAIGHT up the spine
    grey_x = 5200                  # X4 grey pickup riser X (on the spine)
    # yface = YD_FAR so the pickup FLANGE sits on the corridor far face / IBC-4 (NOT the spine lane)
    _bottom_pickup(p, "X4 Waste (P-03)", grey_x, YD_FAR, +1, ov.C_IBC_WASTE,
                   [(grey_x, spine_yd, turn6),                      # ↑ grey spine riser (straight up the spine face) to the wrap level
                    (corr_x, spine_yd, turn6),                      # −X through panel+shirt (pump gap) into the corridor
                    (corr_x, BV02_YD, turn6),                       # −Yd to the BV-06 riser lane (in front of the pumps)
                    (rx6, BV02_YD, turn6),                          # +X back to the BV-06 riser (through the pump gap)
                    (rx6, BV02_YD, z03),                            # ↑ through BV-06 to the IN-port height
                    (PXC, BV02_YD, z03), p3i])                      # −X + short +Yd stub into the IN port
    p.append(ball_valve("BV-06 (P-03 suction)", rx6, BV02_YD, z03 - 110, "z", hdir="+y"))   # handle swings +Yd into the open corridor (clear of the near support board), like BV-02
    p.append(ov.ruby_cylinder("X4 Waste drain port (end wall)", ew - 60, COL_R, 1620, 22, 60, color=C_CHECK, axis="x"))
    pipe("P-03 -> X4 end-wall port",   # OUT leaves with a +Yd stub straight out of the OUT port
         [p3o, (PXC, POY + 30, p3o[2]), (5090, POY + 30, p3o[2]), (5090, COL_R, p3o[2]),
          (ew - 130, COL_R, p3o[2]), (ew - 130, COL_R, 1620), (ew - 60, COL_R, 1620)], ov.C_IBC_WASTE)
    return "\n".join(p)


def context():
    """Ghost of the IBC stack + a floor slice so the corridor frame reads in place."""
    p = []
    p.append(ov.component("IBC Stack", "IBC Stack", ov.ibc_stack(alpha=0.20)))
    x0 = 4300
    p.append(ov.component("Floor (context)", "Context",
             ov.ruby_box("Floor", x0, 0, -ov.WALL_T, ov.C_LEN - x0, ov.C_WID, ov.WALL_T, color=ov.C_SHELL, alpha=0.16)))
    p.append(ov.component("End wall (context)", "Context", end_wall()))
    return "\n".join(p)


def build():
    comps = [context(),
             ov.component("Corridor frame (deep box)", "Frame", frame()),
             ov.component("Rear panel (ply)", "Rear Panel", rear_panel()),
             ov.component("Corridor equipment", "Equipment", equipment()),
             ov.component("Corridor plumbing", "Plumbing", plumbing()),
             ov.component("Corridor drains + X-ports", "Drains", drains_ports())]
    body = "\n".join(comps)
    tags = ["IBC Stack", "Context", "Frame", "Rear Panel", "Equipment", "Plumbing", "Drains"]
    tags_ruby = "".join(f'  model.layers.add({t!r}) unless model.layers[{t!r}]\n' for t in tags)
    return f'''# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("Corridor panel massing", true)
entities = model.active_entities
to_erase = entities.to_a.select {{ |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.materials.purge_unused
model.pages.to_a.each {{ |pg| model.pages.erase(pg) }}
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0
{tags_ruby}{body}
pg = model.pages.add("Corridor panel")
model.commit_operation
{{ ok: true }}.to_json
'''


SKP_PATH = os.path.abspath(os.path.join(_ROOT, "models", "corridor-panel.skp"))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true", help="build into the ACTIVE SketchUp doc (open a blank doc first!)")
    ap.add_argument("--save", action="store_true", help="save the active doc as models/corridor-panel.skp")
    a = ap.parse_args()
    ruby = build()
    if a.send:
        from sketchup_client import send_ruby
        print(send_ruby(ruby))
        if a.save:
            print(send_ruby(f'Sketchup.active_model.save({SKP_PATH!r}) ? "saved {SKP_PATH}" : "FAIL"'))
    else:
        print(ruby[:300])
