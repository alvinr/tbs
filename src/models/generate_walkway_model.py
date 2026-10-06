#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_walkway_model.py — TBS-001 perimeter walkway + cantilever focus model
(models/walkway.skp).

A focused 3D model of the processing-tray perimeter walkway and how it is held
up, so the structure reads clearly apart from the decks that sit on top:

  • **Walkways** — the 4 removable grated sections (near, far, right, left +
    the near widened zone + the left drum-exit punch-out). These are the "gates"
    that lift off for tray access.
  • **Cantilevers** — the wall-cantilevered gusset brackets carrying the near &
    far decks, modeled with their EXTERIOR detail: a reinforcing plate on the
    outside wall face + 3× M12 through-bolts (hex heads outside), visible through
    the ghosted container.
  • **Right Cantilever** — the IBC-end right walkway support: a cantilever
    rectangle (2 long + 2 end 2×1×0.120 steel beams) on center arms off the IBC
    uprights + wall cleats + combined corner plates (rev12 — replaced the old
    ceiling-hung bearer/rod hangers). Single-sourced via right_walkway_cantilever().
  • **Processing Tray** — the SS basin the walkway surrounds (reuses the overview
    builder).
  • **Container** — a low-alpha ghost (floor, ceiling, both long walls) so the
    exterior braces + bolt-throughs show.

Scenes separate the gates (decks) from the cantilevers, plus the right cantilever.

Usage
-----
    python3 src/models/generate_walkway_model.py            # print Ruby
    python3 src/models/generate_walkway_model.py --save      # write .rb
    python3 src/models/generate_walkway_model.py --send      # push to SketchUp
    python3 src/models/generate_walkway_model.py --send --skp # + save models/walkway.skp
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov
import tbs_draw as draw                          # shared drawing/material primitives
import tbs_constants as k                       # right-hanger constants ov doesn't re-export
from tbs_constants import (FP_CORNER_SEAT_PLATE_W, FP_RAIL_WEB, FP_RAIL_ZC_BOT, IBC_FOOT_PLATE_T, IBC_FRAME_RHS, NEAR_GRATE_HOLES, RAIL_X_R, RWK_AH, RWK_ARM_BOT, RWK_ARM_TOP, RWK_ARM_W, RWK_BEARER_W, RWK_BEARER_XS, RWK_BEARER_Z0, RWK_CRANK_DX, RWK_CRANK_N0, RWK_CRANK_N1, RWK_CRANK_Y0, RWK_CRANK_Y1, RWK_GRATE_SLOT_X, RWK_GRATE_SLOT_YDS, RWK_GRATE_Z, RWK_HL_POST, RWK_HL_TIP, RWK_J6_BOLT_ZS, RWK_J6_EP_H, RWK_NOTCH_FLOOR, RWK_UP_YDS, RWK_X_L, RWK_X_R, RWK_X_UP, WALKWAY_BRACKET_T, WALKWAY_GRATE_T, WALKWAY_H, WALKWAY_LEFT_WIDE_W, WALKWAY_LEFT_WIDE_YD_L, WALKWAY_LEFT_WIDE_YD_R, WALKWAY_LEFT_X, WALKWAY_MUSLIN_NOTCH_DY, WALKWAY_MUSLIN_NOTCH_L_X0, WALKWAY_MUSLIN_NOTCH_R_X1, WALKWAY_MUSLIN_NOTCH_YD0, WALKWAY_NEAR_WIDE_W, WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_X_R, WALKWAY_RIGHT_W, WALKWAY_RIGHT_X, WALKWAY_W)   # walkway builders (Phase 1, moved from overview)

ruby_box = draw.ruby_box
ruby_cylinder = draw.ruby_cylinder
ruby_bolt = draw.ruby_bolt
ruby_tri = draw.ruby_tri
ruby_prism = draw.ruby_prism
ruby_cone_wire = draw.ruby_cone_wire
component = draw.component

# Spatial constants (single source of truth via tbs_constants, re-exported by ov)
C_WID, C_HGT, C_LEN, WALL_T = ov.C_WID, ov.C_HGT, ov.C_LEN, ov.WALL_T
RIB = ov.CONTAINER_RIB_SPACING
WK_W, WK_H, GRATE_T = ov.WALKWAY_W, ov.WALKWAY_H, ov.WALKWAY_GRATE_T
WK_LEFT_X, WK_RIGHT_X, WK_FAR_YD = ov.WALKWAY_LEFT_X, ov.WALKWAY_RIGHT_X, ov.WALKWAY_FAR_YD
WK_NEAR_WIDE_XL, WK_NEAR_WIDE_XR = ov.WALKWAY_NEAR_WIDE_X_L, ov.WALKWAY_NEAR_WIDE_X_R
WK_NEAR_WIDE_W = ov.WALKWAY_NEAR_WIDE_W
WK_LEFT_WIDE_W, WK_LEFT_WIDE_YL, WK_LEFT_WIDE_YR = (
    ov.WALKWAY_LEFT_WIDE_W, ov.WALKWAY_LEFT_WIDE_YD_L, ov.WALKWAY_LEFT_WIDE_YD_R)
BRK_T, BRK_H = ov.WALKWAY_BRACKET_T, ov.WALKWAY_BRACKET_H
R_X, R_W = ov.WALKWAY_RIGHT_X, k.WALKWAY_RIGHT_W
# (rev12: the ceiling-hung bearer/hanger/ceiling-plate constants are retired —
#  the right walkway is now right_walkway_cantilever().)

# Exterior reinforcing plate (single-sourced in tbs_constants; also drawn by
# generate_walkway_diagram.py View C).
REINF_W, REINF_H, REINF_T = k.WALKWAY_REINF_W, k.WALKWAY_REINF_H, k.WALKWAY_REINF_T

C_STEEL, C_TRAY, C_SHELL = draw.C_STEEL, draw.C_TRAY, draw.C_SHELL
C_WALKWAY, C_REMOVABLE, C_ALUM = draw.C_WALKWAY, draw.C_REMOVABLE, draw.C_ALUM
C_BOLT = "#505058"

# Left lift-out support — FLOOR-LEG CANTILEVER brackets (replaces the edge beam + wall seats).
LC_LEGX, LC_POST, LC_PW = k.LEFT_WK_CANT_LEG_X, k.LEFT_WK_CANT_POST, k.LEFT_WK_CANT_POST_W
LC_FOOT, LC_FX0 = k.LEFT_WK_CANT_FOOT, k.LEFT_WK_CANT_FOOT_X0
LC_FOOT_BOLT_DX, LC_FOOT_BOLT_DY = k.LEFT_WK_CANT_FOOT_BOLT_DX, k.LEFT_WK_CANT_FOOT_BOLT_DY
LC_ARM_Z0, LC_ARM_W, LC_ARM_WW = k.LEFT_WK_CANT_ARM_Z0, k.LEFT_WK_CANT_ARM_W, k.LEFT_WK_CANT_ARM_W_WIDE
LC_STD, LC_WIDE, LC_YDS = k.LEFT_WK_CANT_STD_REACH, k.LEFT_WK_CANT_WIDE_REACH, k.LEFT_WK_CANT_LEG_YDS

GRATE_Z = WK_H - GRATE_T          # 65 — grate underside / arm top

TAGS = ["Container", "Processing Tray", "Walkways", "Cantilevers",
        "Cantilever Types", "Right Cantilever", "Film Plane", "Film Plane Left", "IBC Frame", "Left Support", "Labels"]


def film_plane_beams(side="both"):
    """Film-plane corners — the REAL detailed mechanism reused verbatim from the dedicated model
    (fpm.corner()): web-vertical 3×1.5 U-channel rails (RIGHT = flanged wall-to-wall end-flanges; LEFT =
    drop-in stub + removable section + welded bridge for the transport swing) + skate/rollers + carriage
    plate + cam-brake + green-Z/purple-X cross-slides + U-joint + 304 corner plate. ONE source with
    overview/water (fpm anchors with end-flanges, not the old IBC saddle). The BR corner's COMBINED corner
    plate is drawn separately (right_walkway_cantilever). `side` = 'right' (BR/TR — what the cantilever
    bolts to), 'left' (BL/TL — its own tag so the Right-Cantilever scene can drop it), or 'both'. Late
    import breaks the fpm→ov cycle; fpm.corner() emits ov.ruby_* at the shared absolute coords."""
    import generate_film_plane_mechanism_model as fpm
    out = []
    if side in ("both", "left"):
        out += [fpm.corner("BL", fpm.X_L, fpm.PZ0, fpm.PZ_HB_BOT, +1, "L"),
                fpm.corner("TL", fpm.X_L, fpm.PZ1, fpm.PZ_HB_TOP, +1, "L")]
    if side in ("both", "right"):
        out += [fpm.corner("BR", fpm.X_R, fpm.PZ0, fpm.PZ_HB_BOT, -1, "R"),
                fpm.corner("TR", fpm.X_R, fpm.PZ1, fpm.PZ_HB_TOP, -1, "R")]
    return '\n'.join(out)


# ── "Labeled" scene callouts (project rule: every .skp gets a Labeled scene) ──
# (instance name, text, leader Δx,Δy,Δz mm). Δy pulls toward the viewer (−Y).
WALKWAY_LABELS = [
    ("Processing Tray", "PROCESSING TRAY", 400, -700, 700),
]
# Point-anchored — the decks, cantilevers and supports are paired/perimeter
# parts whose bounds-centre lands in the empty middle, so anchor on a real member.
WALKWAY_POINT_LABELS = [
    (2400,  150,   73, "NEAR WALKWAY",                    0, -900,  550),
    ( 710,  150,  140, "NEAR LIFT-OUT\n(removable for transport)", -350, -800, 700),  # amber door-end band
    (2400, 2212,   73, "FAR WALKWAY",                   300,  500,  900),
    (4479, 1181,   73, "RIGHT WALKWAY",                 750, -200,  650),
    ( 320, 1181,   73, "LEFT WALKWAY\n(removable)",    -800, -300,  800),
    (2298,   30,  150, "NEAR/FAR CANTILEVERS",         -300, -1000, 450),
    # rev12: the ceiling-hung right hangers are RETIRED — the right walkway is now a
    # cantilever rectangle (Z70–115). Anchor on the inner long beam, not the old ceiling.
    (k.PROC_TRAY_X_R,  400,   90, "RIGHT CANTILEVER\n(IBC-end support)", 700, -300,  700),
    ( 140, 1181,  100, "LEFT SUPPORT\n(floor-leg cantilevers)", -850, -200, 600),
]


def walkway_labels():
    """Ruby that adds an in-model text callout (with leader) for each major part on
    the 'Labels' tag — instance-anchored at bounds top-centre, plus point-anchored
    for paired/perimeter parts (decks, cantilevers, hangers, support)."""
    rows = []
    for name, text, dx, dy, dz in WALKWAY_LABELS:
        rows.append(
            f'inst = entities.grep(Sketchup::ComponentInstance).find {{ |i| i.name == "{name}" }}\n'
            f'if inst\n'
            f'  bb = inst.bounds\n'
            f'  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)\n'
            f'  txt = entities.add_text("{text}", anc, Geom::Vector3d.new({draw.mm(dx)}, {draw.mm(dy)}, {draw.mm(dz)}))\n'
            f'  txt.layer = model.layers["Labels"] rescue nil\n'
            f'end')
    for x, y, z, text, dx, dy, dz in WALKWAY_POINT_LABELS:
        rows.append(
            f'anc = Geom::Point3d.new({draw.mm(x)}, {draw.mm(y)}, {draw.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({draw.mm(dx)}, {draw.mm(dy)}, {draw.mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    return '\n'.join(rows)


# ── Ghost container (floor + ceiling + both long walls) ──────────────────────

def container_ghost():
    """Low-alpha floor + the FAR (film-plane) side wall only. The roof (ceiling) and the NEAR
    (pinhole) side wall are omitted so the model orbits freely without the view boxing in
    (2026-08-18); the far cantilever reinforcing plates + bolt-throughs still read against
    the far wall. End walls were already omitted."""
    return '\n'.join([
        ruby_box("Floor (ghost)", 0, 0, -WALL_T, C_LEN, C_WID, WALL_T,
                 color=C_SHELL, alpha=0.22),
        ruby_box("Side wall far (ghost)", 0, C_WID, 0, C_LEN, WALL_T, C_HGT,
                 color=C_SHELL, alpha=0.14),
    ])


# ── Walkway grated decks (the removable "gates") ─────────────────────────────

def far_deck(alpha=None):
    """The FAR walkway deck grate (WALL edge inset by the bracket plate thickness). SINGLE OWNER —
    the overview model calls this so the far deck can't drift from the walkway model."""
    near_x_l = WK_LEFT_X + WK_W
    return ruby_box("Walkway Far", near_x_l, WK_FAR_YD, GRATE_Z,
                    WK_RIGHT_X - near_x_l, WK_W - BRK_T, GRATE_T, color=C_WALKWAY, alpha=alpha)


def near_removable_deck(alpha=None):
    """The door-end REMOVABLE band of the NEAR walkway (lifts out for transport, distinct color).
    SINGLE OWNER — the light-trap model draws it (ghosted) as door-end context."""
    near_x_l = WK_LEFT_X + WK_W
    liftout_x = min(ov.WALKWAY_NEAR_LIFTOUT_X_R, WK_NEAR_WIDE_XL)   # X950 (sweep X≈896 +50mm)
    return ruby_box("Walkway Near (door-end, removable)", near_x_l, BRK_T, GRATE_Z,
                    liftout_x - near_x_l, WK_W - BRK_T, GRATE_T, color=C_REMOVABLE, alpha=alpha)


def walkway_decks():
    """The four grated walkway sections that lift off for tray access — the
    'gates'. Geometry mirrors the overview's walkways() (minus the brackets,
    which are their own tag here)."""
    t = GRATE_T
    # Inset each deck's WALL edge by the bracket plate thickness so the grate sits on the
    # INSIDE of the gusset-bracket plates (which mount flat on the wall) instead of through
    # them — matches the overview fix.
    # Near/far grates start at the left-walkway inner edge (X = WK_LEFT_X+WK_W). With the
    # floor-leg cantilever redesign there is no full-width kerb beam to cut around.
    near_x_l = WK_LEFT_X + WK_W
    near_x_r = WK_RIGHT_X
    parts = []

    # Near deck — left run, widened zone, right run (Yd 0..width). The walkway stays LEVEL
    # (Z130); the door-end band of the left run (near_x_l..~X900) is a REMOVABLE lift-out for
    # transport (distinct color) — the panel/cage underside sweeps the near deck there, so it
    # lifts out with the left walkway rather than dropping the grate (#8). The rest is fixed.
    # Removable door-end band (near_x_l..X950) lifts out for transport — its own piece by design.
    # The rest of the near deck is ONE continuous fixed piece with the EP/battery bump-out
    # integral (no butt joints at the widening) — shared helper so it can't drift from overview.
    liftout_x = min(ov.WALKWAY_NEAR_LIFTOUT_X_R, WK_NEAR_WIDE_XL)   # X950 (sweep X≈896 +50mm)
    parts.append(near_removable_deck())
    parts.append(near_fixed_deck_grate("Walkway Near (fixed, bump integral)",
                                          liftout_x, GRATE_Z, t, C_WALKWAY))

    # Far deck.
    parts.append(far_deck())

    # (The right grate rides the Walkways tag via right_walkway_grate() — see the
    #  component list — so it shows with the decks but not in the bare Right-Cantilever scene.)

    # Left deck — removable lift-out (distinct color) as ONE continuous piece: drum-exit
    # punch-out tab + muslin-drop notch both integral (no butt-jointed add-on). Shared helper.
    parts.append(left_liftout_grate("Walkway Left (removable)", GRATE_Z, t, C_REMOVABLE))
    return '\n'.join(parts)


# ── Wall cantilever brackets, with the EXTERIOR brace + bolt-throughs ────────

def _cantilever_parts(nm, x, wall_yd, sign, reach, wide):
    """Geometry for ONE wall-cantilever bracket: interior mounting plate + arm +
    under-gusset, an EXTERIOR reinforcing plate, and the M12 through-bolts (hex
    heads outside). `wide` selects the widened EP/battery-zone spec.

    This is the FULL-FAB version. The overview's `walkway_brackets()`
    (generate_sketchup_model.py) intentionally simplifies it for the whole-system view —
    it omits the exterior reinforcing plates and the full-length through-bolts (modeling
    short interior studs instead). The difference is level-of-detail only, not the
    load-bearing dimensions; `lint.py --duplication` reports it as EXPECTED, not drift."""
    bt, vh = BRK_T, BRK_H                                   # standard 8mm / 180mm
    btw, vhw = k.WALKWAY_WIDE_BRACKET_T, k.WALKWAY_WIDE_BRACKET_H   # widened 10mm / 200mm
    # interior mounting plate width = the exterior reinforcing-plate width per type, so the two
    # plates that sandwich the wall are the SAME footprint (100 std / 120 widened; 2026-08-19).
    plate_w = k.WALKWAY_REINF_W_WIDE if wide else REINF_W
    gusset_reach = k.WALKWAY_GUSSET_REACH
    # Bolt patterns (X offset, Z): standard 3 (triangular, ±WALKWAY_BRACKET_BOLT_DX = 27 — Sheet 2 View B);
    # widened 4 (rectangular, ±WALKWAY_BRACKET_BOLT_DX_WIDE = 32 — Sheet 7 View B).
    _ubz = k.WALKWAY_BRACKET_UPPER_BOLT_Z   # 155 — upper bolt clears the grate deck (SHARED std + widened)
    _dx  = k.WALKWAY_BRACKET_BOLT_DX          # 27 — STANDARD wall-bolt X offset (Sheet 2 View B)
    _dxw = k.WALKWAY_BRACKET_BOLT_DX_WIDE     # 32 — WIDENED wall-bolt X offset (Sheet 7 View B)
    bolt_pat_std  = [(0, _ubz), (-_dx, k.WALKWAY_BRACKET_BOLT_Z_LO), (_dx, k.WALKWAY_BRACKET_BOLT_Z_LO)]
    bolt_pat_wide = [(-_dxw, k.WALKWAY_BRACKET_BOLT_Z_LO_WIDE), (_dxw, k.WALKWAY_BRACKET_BOLT_Z_LO_WIDE), (-_dxw, _ubz), (_dxw, _ubz)]

    b   = btw if wide else bt                       # plate/gusset thickness
    v   = vhw if wide else vh                        # vertical leg height
    # ARM = a steel TUBE (redesigned to IBC/OSHA — was an 8mm×10mm plate edge that yielded at ~25 lbf):
    # std 2×1×0.120 (50.8 wide), widened 3×1×0.120 (76.2 wide), both 25.4 deep (spray-bar-capped),
    # underside Z89.6.  Sized by walkway_load.py (300 lbf tip: SF 2.10 std / 1.83 widened).
    arm_w = k.WALKWAY_BRACKET_ARM_W_WIDE if wide else k.WALKWAY_BRACKET_ARM_W   # 76.2 / 50.8 (X)
    arm_d = k.WALKWAY_BRACKET_ARM_H                 # 25.4 (Z depth)
    arm_bot = k.WALKWAY_BRACKET_ARM_Z0             # 89.6 (grate bottom − arm depth)
    rch = WK_NEAR_WIDE_W if wide else reach         # arm reach (500mm widened deck)
    rw  = k.WALKWAY_REINF_W_WIDE if wide else REINF_W   # exterior reinf plate W
    rh  = k.WALKWAY_REINF_H_WIDE if wide else REINF_H   #                       H
    bolt_pat = bolt_pat_wide if wide else bolt_pat_std
    shank_len = WALL_T + REINF_T + b
    reinf_z0 = max(0, (v - rh) // 2)

    parts = []
    # interior mounting plate, flat on the wall inner face
    y_plate = wall_yd if sign > 0 else wall_yd - b
    parts.append(ruby_box(f"{nm} plate", x - plate_w / 2, y_plate, 0,
                          plate_w, b, v, color=C_STEEL))
    # horizontal cantilever arm at grate level (deck rests on it) — its back end
    # butts the plate's container-facing face so the arm→plate joint draws an edge
    y_arm = (wall_yd + b) if sign > 0 else (wall_yd - rch)   # plate front .. outboard
    parts.append(ruby_box(f"{nm} arm", x - arm_w / 2, y_arm, arm_bot,
                          arm_w, rch - b, arm_d, color=C_STEEL))
    # gusset triangle bracing the arm from below — same X as the arm (directly under
    # it, push −b), and its back edge butts the plate's container-facing face so the
    # gusset→plate joint reads as a clean edge (not passing through the plate)
    # xg is sign-aware so the gusset lands CENTERED under the arm on BOTH walls: ruby_tri pushpulls along
    # the (winding-dependent) face normal, which flips near↔far, so a fixed xg would offset the far gusset
    # by one plate thickness. x − sign·b/2 cancels that → gusset spans [x−b/2, x+b/2] both sides (2026-08-18).
    xg = x - sign * b / 2
    y_back = wall_yd + sign * b           # plate's container-facing face
    y_far = wall_yd + sign * gusset_reach
    parts.append(ruby_tri(f"{nm} gusset",
                          (xg, y_back, 0), (xg, y_back, arm_bot),
                          (xg, y_far, arm_bot), -b, color=C_STEEL))
    # EXTERIOR reinforcing plate on the outside wall face
    reinf_y0 = (-WALL_T - REINF_T) if sign > 0 else (C_WID + WALL_T)
    parts.append(ruby_box(f"{nm} ext reinf plate", x - rw / 2, reinf_y0,
                          reinf_z0, rw, REINF_T, rh, color=C_STEEL))
    # M12 through-bolts (3× std / 4× widened) — hex head (exterior) + hex nut (interior)
    for dx, bz in bolt_pat:
        bx = x + dx
        shank_y0 = (-WALL_T - REINF_T) if sign > 0 else (wall_yd - b)
        parts.append(ruby_bolt(f"{nm} bolt M12", bx, shank_y0, bz, shank_len, radius=6,
                               axis="y", color=C_BOLT, head="base", nut="far"))
    return parts


def cantilevers(which="both"):
    """Near + far wall-cantilevered gusset brackets IN SITU, each shown with its
    full through-wall detail through the ghosted side walls. STANDARD brackets are
    8mm plate / 170mm leg / 300mm arm with 3× M12 (triangular); the four WIDENED
    brackets in the near EP/battery zone (X 1155–2629) are 10mm plate / 200mm leg /
    500mm arm with 4× M12 (rectangular, matching walkway Sheet 7). `which` = "both"
    (default) / "near" / "far" — this is the SINGLE bracket builder (the overview's
    `walkway_brackets()` delegates here so the two can't diverge)."""
    near_x_l = WK_LEFT_X + WK_W
    near_x_r = WK_RIGHT_X
    stations = []
    xs = near_x_l + RIB // 2
    while xs < near_x_r:
        stations.append(xs)
        xs += RIB

    # (label, wall Yd, inward sign, arm reach under that side's grate)
    sides = [("Near", 0, +1, WK_W),
             ("Far", C_WID, -1, C_WID - WK_FAR_YD)]
    if which == "near":
        sides = [sides[0]]
    elif which == "far":
        sides = [sides[1]]

    parts = []
    for label, wall_yd, sign, reach in sides:
        for i, x in enumerate(stations, 1):
            wide = (label == "Near" and WK_NEAR_WIDE_XL <= x <= WK_NEAR_WIDE_XR)
            nm = f"Cantilever {label} {i}" + (" (widened)" if wide else "")
            parts += _cantilever_parts(nm, x, wall_yd, sign, reach, wide)
    return '\n'.join(parts)


# Near-wall X positions for the isolated type-catalog ("Cantilevers" scene), ordered
# left→right: floor-leg cantilever SHORT (to X470), floor-leg LONG (to X770, punch-out),
# standard wall cantilever, widened wall cantilever.
CT_SEAT_X, CT_SEAT_LONG_X, CT_STD_X, CT_WIDE_X = 2000, 3000, 4000, 5000
# rev12 right-walkway cantilever-rectangle support brackets (added to the catalog):
CT_RWK_CLEAT_X, CT_RWK_PLATE_X, CT_RWK_ARM_X = 6000, 7000, 8000


def _rwk_arm_type_parts(x0):
    """ONE right-walkway CENTER CANTILEVER ARM for the catalog, mirroring the CURRENT design
    (ibc_cantilever_arms): an IBC-upright stub + a SOLID 2×1 flat-bar arm cantilevering off it
    (toward -X) + the J6 BEARING-TYPE connection — a welded END-PLATE + a REAR backing plate +
    2× M12 through-bolts, both above the arm. (Was an old 40×40 SHS arm + single-bolt clamp.)"""
    armb, armt, aw, ah = ov.RWK_ARM_BOT, ov.RWK_ARM_TOP, ov.RWK_ARM_W, ov.RWK_AH   # 89.6, 115, 50.8, 25.4
    s = ov.IBC_FRAME_RHS                                            # 50.8 upright RHS
    reach = ov.RWK_X_UP - ov.RWK_X_L                               # 325 — upright front → inner long beam
    ep_t, ep_w, ep_h = 8, 65, ov.RWK_J6_EP_H                        # end-plate thickness / Yd width / Z height (155)
    ac_z = (armb + armt) / 2.0
    ep_bz = ac_z - 65.0                                            # end-plate bottom Z37 (mirrors the real builder)
    bp_bz = ov.IBC_FOOT_PLATE_T + ov.IBC_FRAME_RHS                  # rear backing-plate bottom (butts the bottom rail)
    bp_h = (ep_bz + ep_h) - bp_bz
    ac_y = aw / 2.0                                                # arm centre in Yd
    parts = [
        draw.ruby_box("Type RWk IBC upright (50x50 RHS)", x0, 0, 0, s, s, armt + 220, color=draw.C_STEEL),
        draw.ruby_box("Type RWk cantilever arm (solid 2x1 flat bar)", x0 - reach, 0, armb, reach - ep_t, aw, ah, color=draw.C_STEEL),
        draw.ruby_box("Type RWk J6 end-plate (welded to arm)", x0 - ep_t, ac_y - ep_w / 2, ep_bz, ep_t, ep_w, ep_h, color=draw.C_STEEL),
        draw.ruby_box("Type RWk J6 backing plate (rear)", x0 + s, ac_y - ep_w / 2, bp_bz, ep_t, ep_w, bp_h, color=draw.C_STEEL),
    ]
    for bz in ov.RWK_J6_BOLT_ZS:                                    # 2× M12, both above the arm (bearing-type)
        parts.append(draw.ruby_bolt("Type RWk J6 bolt M12", x0 - ep_t, ac_y, bz, s + 2 * ep_t + 8,
                                  radius=6, axis="x", color="#3A3A42", head="base", nut="far"))
    return parts


def _floor_cant_type_parts(x0, reach, suffix, target_x, arm_w):
    """ONE LEFT-walkway FLOOR-LEG CANTILEVER bracket for the type-catalog — foot plate +
    50x50 post to the grate bottom + arm at Z89.6-115 reaching `reach` mm in — isolated at
    catalog X station `x0`, near wall. Built twice: the STANDARD reach (arm to the grate
    inner edge, X580, 2×1 arm) and the EXTENDED reach (X880, the 3 drum-exit punch-out
    brackets, 4×1 arm — IBC/OSHA). `arm_w` is the arm's Yd width per type."""
    foot_l, foot_w, foot_t = LC_FOOT
    az0, az1 = LC_ARM_Z0, GRATE_Z
    return [
        ruby_box(f"Type FloorCant {suffix} foot plate", x0 - foot_l / 2, 0, 0,
                 foot_l, foot_w, foot_t, color=C_STEEL),
        ruby_box(f"Type FloorCant {suffix} post (2x2x0.120 SHS)", x0 - LC_POST / 2, 0, 0,
                 LC_POST, LC_PW, az1, color=C_STEEL),
        ruby_box(f"Type FloorCant {suffix} arm (to X{target_x})", x0 + LC_POST / 2, -arm_w / 2, az0,
                 reach, arm_w, az1 - az0, color=C_STEEL),
    ]


def cantilever_types():
    """ONE of each unique walkway-support bracket, isolated side-by-side for the
    "Cantilevers" scene:
      • FLOOR-LEG CANTILEVER, two reaches — the LEFT removable walkway's support (a 50x50
        post on bare floor + arm): the STANDARD reach to the grate inner edge (X470) and
        the EXTENDED reach (X770) on the 3 drum-exit punch-out brackets;
      • STANDARD wall cantilever — 8mm/150/300, 3× M12 (typical near/far deck bracket);
      • WIDENED  wall cantilever — 10mm/200/500, 4× M12 (the four EP/battery-zone brackets);
      • the rev12 RIGHT-WALKWAY cantilever-rectangle supports — WALL CLEAT (left corners),
        COMBINED CORNER PLATE (right corners, shared with the BR film rail), and the
        CENTER CANTILEVER ARM off the IBC corridor uprights."""
    arm_x0 = LC_LEGX + LC_POST / 2                  # 165 — arm starts at the post inner face
    parts = []
    parts += _floor_cant_type_parts(CT_SEAT_X, LC_STD - arm_x0, "short", int(LC_STD), LC_ARM_W)
    parts += _floor_cant_type_parts(CT_SEAT_LONG_X, LC_WIDE - arm_x0, "long", int(LC_WIDE), LC_ARM_WW)
    parts += _cantilever_parts("Type Standard", CT_STD_X, 0, +1, WK_W, False)
    parts += _cantilever_parts("Type Widened", CT_WIDE_X, 0, +1, WK_NEAR_WIDE_W, True)
    # rev12 right-walkway support brackets (reuse the single-sourced overview builders):
    parts += _rwk_wall_cleat("Type RWk Cleat", CT_RWK_CLEAT_X, 0, 1)
    parts += fp_combined_corner_plate(0, 1, cx=CT_RWK_PLATE_X)
    parts += _rwk_arm_type_parts(CT_RWK_ARM_X)
    return '\n'.join(parts)


def cantilever_type_labels():
    """Ruby: a callout naming each unique bracket type, on the 'Cantilever Types'
    tag so they show only in the 'Cantilevers' scene."""
    labels = [  # left→right: floor-leg short, floor-leg long, standard, widened
        (CT_SEAT_X, 0, GRATE_Z,
         f"FLOOR-LEG CANTILEVER — standard reach\n2x2 post on bare floor + 2x1 arm to the\ngrate inner edge (X={int(LC_STD)})",
         -200, -300, 800),
        (CT_SEAT_LONG_X, 0, GRATE_Z,
         f"FLOOR-LEG CANTILEVER — extended reach\n3 of the 5 brackets reach to X={int(LC_WIDE)} on a\n4x1 arm (drum-exit punch-out; IBC/OSHA SF 1.99)",
         -200, -300, 800),
        (CT_STD_X, 0, BRK_H,
         "STANDARD CANTILEVER\n8mm plate / 180 leg / 2x1 tube arm\n3x M12 (triangular)",
         0, -300, 720),
        (CT_WIDE_X, 0, k.WALKWAY_WIDE_BRACKET_H,
         "WIDENED CANTILEVER (EP / battery zone)\n10mm plate / 200 leg / 3x1 tube arm\n4x M12 (rectangular)",
         200, -300, 850),
        (CT_RWK_CLEAT_X, 0, ov.RWK_ARM_TOP,
         "RIGHT WALKWAY — WALL CLEAT (left corners)\n8mm back-plate + ext plate + shelf,\nthe long beam lands on it; M12 through-bolts",
         -150, -300, 800),
        (CT_RWK_PLATE_X, 0, k.FP_RAIL_ZC_BOT,
         "RIGHT WALKWAY — COMBINED CORNER PLATE (right corners)\n10mm, carries the walkway right beam (Z70 seat)\n+ the BR film rail (web-vertical: Z232 seat / Z270 bolt); 4x M12",
         0, -300, 850),
        (CT_RWK_ARM_X, 0, ov.RWK_ARM_TOP,
         "RIGHT WALKWAY — CENTER CANTILEVER ARM\nsolid 2x1 flat bar off an IBC corridor upright\n(half-lapped at the long beams); J6 end-plate, 2x M12",
         150, -300, 820),
    ]
    rows = []
    for x, y, z, text, dx, dy, dz in labels:
        rows.append(
            f'anc = Geom::Point3d.new({draw.mm(x)}, {draw.mm(y)}, {draw.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({draw.mm(dx)}, {draw.mm(dy)}, {draw.mm(dz)}))\n'
            f'txt.layer = model.layers["Cantilever Types"] rescue nil')
    return '\n'.join(rows)


# ── Right walkway: cantilever rectangle (rev12) ──────────────────────────────
# The ceiling-hung right_hangers() support is retired; the right walkway is now a
# self-supporting cantilever rectangle built by right_walkway_cantilever()
# (single-sourced in the overview), assembled as the "Right Cantilever" component
# in generate_ruby() below.


# ── Left walkway: removable lift-out support (floor-leg cantilever brackets) ────

def left_floor_cantilevers():
    """The left walkway's removable lift-out support: a row of FLOOR-LEG CANTILEVER
    brackets bolted to bare floor OUTSIDE the tray (X<170). Each = foot plate + 50x50
    post (to the grate bottom) + an arm (Z75-115, 40mm deep, ABOVE the floor-level
    spray bar) reaching IN to carry the grate inner edge (X=470). Brackets on the
    drum-exit punch-out (Yd 800-1560) get EXTENDED arms (to X=770) so the widened
    section is supported, not cantilevered. Zero tray contact. Returns a list of ruby
    parts — SHARED by left_support() and the overview so the two never diverge."""
    foot_l, foot_w, foot_t = LC_FOOT           # 128 x 60 x 8
    az0, az1 = LC_ARM_Z0, GRATE_Z              # 75 .. 115 (grate bottom)
    arm_x0 = LC_LEGX + LC_POST / 2             # 165 — arm starts at the post inner face
    parts = []
    for i, y in enumerate(LC_YDS, 1):
        wide = WK_LEFT_WIDE_YL <= y <= WK_LEFT_WIDE_YR
        reach = LC_WIDE if wide else LC_STD     # 880 (punch-out) / 580 (standard) tip X
        aw = LC_ARM_WW if wide else LC_ARM_W    # 101.6 (4×1, IBC/OSHA) / 50.8 (2×1) arm width in Yd
        parts.append(ruby_box(f"Left cantilever {i} foot plate", LC_FX0, y - foot_w / 2, 0,
                              foot_l, foot_w, foot_t, color=C_STEEL))
        parts.append(ruby_box(f"Left cantilever {i} post (2x2x0.120 SHS)",
                              LC_LEGX - LC_POST / 2, y - LC_PW / 2, foot_t,   # sits ON the foot plate (butt, not sunk in — the weld is not modeled)
                              LC_POST, LC_PW, az1 - foot_t, color=C_STEEL))
        parts.append(ruby_box(f"Left cantilever {i} arm (to X{int(reach)})", arm_x0,
                              y - aw / 2, az0, reach - arm_x0, aw, az1 - az0, color=C_STEEL))
        # Floor anchors — 4× #14 SS self-drillers through the foot plate into the ply-over-steel
        # floor, in the INBOARD outrigger clear of the post (F3, 2026-08-18). Hex head at the top;
        # nut=None (self-drilling, no back nut).
        for dx in LC_FOOT_BOLT_DX:
            for dy in (-LC_FOOT_BOLT_DY, LC_FOOT_BOLT_DY):
                parts.append(ruby_bolt(f"Left cantilever {i} floor anchor",
                                       LC_FX0 + dx, y + dy, 0, foot_t + 4, radius=4,
                                       axis="z", color=C_BOLT, head="far", nut=None))
    return parts


def left_support():
    """The LEFT walkway is a removable lift-out, carried by a row of FLOOR-LEG
    CANTILEVER brackets (see left_floor_cantilevers) — bolted to bare floor outside the
    tray, arms reaching in over the floor-level spray bar to the grate inner edge (and
    extended to X=770 on the drum-exit punch-out). Replaces the former edge-beam-on-
    wall-seats: the +50 walkway raise lifted the grate clear of the spray bar, so a
    floor-rooted arm can pass over the open tray. Zero tray contact; brackets + grate
    lift out for transport (before the panel + drum swing inboard — see lighttrap.skp)."""
    return '\n'.join(left_floor_cantilevers())


# ── Assemble the Ruby script ─────────────────────────────────────────────────

def _yd_split(y0, y1, cuts):
    """Sub-intervals of [y0,y1] with each (cy0,cw) in `cuts` removed (used to segment a long
    beam around arm half-laps and pipe notches)."""
    segs, ys = [], y0
    for cy0, cw in sorted(cuts):
        if cy0 > ys:
            segs.append((ys, cy0))
        ys = max(ys, cy0 + cw)
    if ys < y1:
        segs.append((ys, y1))
    return segs


def _rwk_xbeam(name, yd, x0, x1):
    """Arm = SOLID 2×1 flat bar, half-lapped at each long beam it crosses. The notch is REBALANCED to
    the moment: DEEP at the tip (low moment → arm keeps 5.4, RWK_HL_TIP) and SHALLOW at the post end
    (high moment → arm keeps 16, RWK_HL_POST → the OUTER beam takes the deep notch). Built as solid
    X-segments, each a box from the bar bottom up to its local top (RWK_ARM_TOP, or the split at a crossing)."""
    def _split_at(bx):
        return RWK_HL_TIP if bx <= RWK_X_L + 1 else RWK_HL_POST
    crossings = sorted((bx, bx + RWK_BEARER_W, _split_at(bx))
                       for bx in RWK_BEARER_XS if x0 - 1 < bx < x1)
    out, cursor = [], x0
    for cx0, cx1, split in crossings:
        if cx0 > cursor:
            out.append(ruby_box(f"{name} full", cursor, yd, RWK_ARM_BOT, cx0 - cursor, RWK_ARM_W, RWK_ARM_TOP - RWK_ARM_BOT, color=C_STEEL))
        out.append(ruby_box(f"{name} notch", cx0, yd, RWK_ARM_BOT, cx1 - cx0, RWK_ARM_W, split - RWK_ARM_BOT, color=C_STEEL))
        cursor = cx1
    if cursor < x1:
        out.append(ruby_box(f"{name} full", cursor, yd, RWK_ARM_BOT, x1 - cursor, RWK_ARM_W, RWK_ARM_TOP - RWK_ARM_BOT, color=C_STEEL))
    return out


def _rwk_long_beam(x, cross_ranges, notches=(), y0=0, y1=C_WID, split=None):
    """Yd long beam half-lapped at the arms it crosses (cross_ranges = (yd0, w)): continuous UPPER
    part (split..TOP) + LOWER part cut away at each crossing.  `split` = the half-lap line (Z of the
    kept upper part's bottom): RWK_HL_TIP for the inner beam (keeps 20), RWK_HL_POST for the outer beam
    (keeps 9.4 — the arm takes the thick side at the post end).  `notches` = (yd0, w) OPEN-TOP pipe slots
    (outer beam only): the UPPER web is cut away and the lower web dropped to RWK_NOTCH_FLOOR so a flush
    ribbon pipe crosses through the top.  `y0..y1` restricts the run to a Yd sub-range (the cranked inner
    beam's straight portions either side of the muslin-rod jog)."""
    if split is None:
        split = RWK_HL_TIP
    out = []
    # UPPER part (split..TOP): full Yd, minus the pipe notches (an open-top notch removes the upper web)
    for s0, s1 in _yd_split(y0, y1, list(notches)):
        out.append(ruby_box(f"RWk Long beam X{int(x)} upper", x, s0, split, RWK_BEARER_W, s1 - s0, RWK_ARM_TOP - split, color=C_STEEL))
    # LOWER part (BEARER_Z0..split): removed at arm half-laps AND at notches (a reduced-height web fills the notch below)
    for s0, s1 in _yd_split(y0, y1, list(cross_ranges) + list(notches)):
        out.append(ruby_box(f"RWk Long beam X{int(x)} lower", x, s0, RWK_BEARER_Z0, RWK_BEARER_W, s1 - s0, split - RWK_BEARER_Z0, color=C_STEEL))
    # at each notch: the surviving Z80-NOTCH_FLOOR bottom web (skip where an arm half-lap already removed it)
    for n0, nw in notches:
        for s0, s1 in _yd_split(n0, n0 + nw, list(cross_ranges)):
            out.append(ruby_box(f"RWk Long beam X{int(x)} notch web", x, s0, RWK_BEARER_Z0, RWK_BEARER_W, s1 - s0, RWK_NOTCH_FLOOR - RWK_BEARER_Z0, color=C_STEEL))
    return out


def _rwk_inner_beam_cranked(x, cross_ranges, y_inset=0):
    """The inner right-walkway long beam, CRANKED outboard by RWK_CRANK_DX over the muslin-drop notch
    (Yd RWK_CRANK_N0..N1) with angled ramps, so the rigid muslin rod drops straight down at the tray
    edge (X=x) clear of the beam — while the beam stays ONE continuous (uncut) member. Built as: the
    straight run before the crank (carries the arm half-laps) + a ramp-out prism + the jogged straight
    segment + a ramp-in prism + the straight run after. The crank zone has no arms/pipe-notches."""
    w, z0, h, dx = RWK_BEARER_W, RWK_BEARER_Z0, RWK_ARM_TOP - RWK_BEARER_Z0, RWK_CRANK_DX
    out = []
    out += _rwk_long_beam(x, cross_ranges, y0=y_inset, y1=RWK_CRANK_Y0)           # straight (arms) — butts the near plate
    out.append(ruby_prism("RWk Long beam inner ramp-out",                        # angled ramp X→X+dx
                          [(x, RWK_CRANK_Y0), (x + w, RWK_CRANK_Y0),
                           (x + dx + w, RWK_CRANK_N0), (x + dx, RWK_CRANK_N0)], z0, h, color=C_STEEL))
    out += _rwk_long_beam(x + dx, (), y0=RWK_CRANK_N0, y1=RWK_CRANK_N1)           # jogged clear of notch
    out.append(ruby_prism("RWk Long beam inner ramp-in",                         # angled ramp X+dx→X
                          [(x + dx, RWK_CRANK_N1), (x + dx + w, RWK_CRANK_N1),
                           (x + w, RWK_CRANK_Y1), (x, RWK_CRANK_Y1)], z0, h, color=C_STEEL))
    out += _rwk_long_beam(x, cross_ranges, y0=RWK_CRANK_Y1, y1=C_WID - y_inset)   # straight run after — butts the far plate
    return out


def _rwk_wall_cleat(tag, x, wall_yd, din):
    """Plate 2 — the tray-facing walkway long-beam bracket. The beam RESTS on a horizontal SHELF and is
    locked down by a TEK screw; the plate is through-bolted to the wall by 2 HORIZONTAL bolts placed
    CLEAR of the beam (one below the shelf, one above the beam) so the wall anchors don't foul the beam
    edge (2026-08-18). Interior + exterior plate sandwich the wall."""
    bt = 8                                                   # plate thickness (Yd)
    shelf_top = RWK_ARM_BOT                                  # beam bottom = shelf top (89.6)
    bolt_lo = shelf_top - 10 - 30                            # 30mm below the shelf underside
    bolt_hi = RWK_ARM_TOP + 30                               # 30mm above the beam top — both clear of the beam
    pz0, pz1 = bolt_lo - 18, bolt_hi + 18                    # plate spans both bolts + ≥1.5·D edge margin
    piy = wall_yd if din > 0 else wall_yd - bt
    poy = -WALL_T - bt if din > 0 else C_WID + WALL_T
    shelf_y = wall_yd if din > 0 else wall_yd - 55
    out = [
        ruby_box(f"RWk wall cleat plate ({tag})", x - 45, piy, pz0, 90, bt, pz1 - pz0, color=C_STEEL),
        ruby_box(f"RWk wall cleat ext plate ({tag})", x - 45, poy, pz0, 90, bt, pz1 - pz0, color=C_STEEL),
        ruby_box(f"RWk wall cleat shelf ({tag})", x - 45, shelf_y, shelf_top - 10, 90, 55, 10, color=C_STEEL),
    ]
    blo, bhi = min(piy, poy), max(piy, poy) + bt
    for bz in (bolt_lo, bolt_hi):                            # 2 HORIZONTAL wall bolts, both CLEAR of the beam
        out.append(ruby_bolt(f"RWk wall bolt ({tag}) Z{int(bz)}", x, blo, bz, bhi - blo, radius=5, axis="y", color=C_STEEL, head="base", nut="far"))
    # TEK screw locking the beam DOWN onto the shelf — vertical self-driller through the shelf + beam.
    out.append(ruby_bolt(f"RWk beam TEK screw ({tag})", x, shelf_y + 27, shelf_top - 10,
                         (RWK_ARM_TOP + 4) - (shelf_top - 10), radius=3, axis="z", color="#3A3A42", head="far", nut=None))
    return out


def fp_combined_corner_plate(wall_yd, din, cx=None):
    """ONE plate at the near/far-RIGHT corner securing BOTH the bottom film rail (BR) and the
    walkway's right beam — through-bolted to the wall (interior + exterior plate). Spans Z58..313:
    the right beam lands on it at Z70-115; the BR rail is the web-vertical U-channel (web-centre
    FP_RAIL_ZC_BOT=270, box 232-308) — its bottom seats at Z232 and a wall bolt passes through it at
    the web centre (Z270). 150mm wide. `cx` overrides the X station (walkway bracket-type catalog)."""
    pw = FP_CORNER_SEAT_PLATE_W                                   # 150 plate
    rail_c = FP_RAIL_ZC_BOT                                 # 270 — BR rail web-centre (single-sourced)
    rail_bot = rail_c - FP_RAIL_WEB / 2                     # 232 — rail box bottom (seat sits just under it)
    rail_top = rail_c + FP_RAIL_WEB / 2                     # 308 — rail box top (plate backs the end flange)
    if cx is None:
        cx = RAIL_X_R                                      # 4649 (real BR corner)
    tag = "near" if wall_yd == 0 else "far"
    piy = wall_yd if din > 0 else wall_yd - 10
    poy = -WALL_T - 10 if din > 0 else C_WID + WALL_T
    sy = wall_yd + 10 if din > 0 else wall_yd - 10 - 55   # shelves PROJECT from the plate inboard face (Yd10) so they BUTT the plate (a seam shows), not bury into it
    # Plate WIDENED inboard by one bearer width (to x_in) so the walkway beam — pulled inboard to X4523
    # by F1 — is BACKED by the plate. The beam rests on the WELDED SHELF (right-beam seat) and is locked
    # by 2 TEK screws (not bolted through). The plate's 4 wall through-bolts sit at the plate CORNERS, the
    # LOW pair dropped BELOW the beam so they don't foul it; the outboard region carries the BR film rail
    # (seated + end-flanged). (F2 rework, 2026-08-18.)
    x_in = cx - pw / 2 - RWK_BEARER_W                      # 4523.2 — plate inboard edge (= walkway beam inboard edge)
    x_out = cx + pw / 2                                    # 4724 — plate outboard edge
    plate_w = pw + RWK_BEARER_W                            # 200.8 — widened plate width
    beam_cx = x_in + RWK_BEARER_W / 2                      # 4548.6 — walkway beam centre
    z0, z1 = RWK_ARM_BOT - 48, rail_top + 5                 # plate bottom dropped so the LOW corner bolts clear the beam; top backs the rail end flange
    out = [
        ruby_box(f"FP combined corner plate ({tag})", x_in, piy, z0, plate_w, 10, z1 - z0, color=C_STEEL),
        ruby_box(f"FP combined corner ext plate ({tag})", x_in, poy, z0, plate_w, 10, z1 - z0, color=C_STEEL),
        ruby_box(f"FP combined right-beam seat ({tag})", x_in, sy, RWK_ARM_BOT - 12, RWK_BEARER_W, 55, 12, color=C_STEEL),   # SHELF — only under the beam footprint (not full plate width)
        ruby_box(f"FP combined beam upstand ({tag})", x_in + RWK_BEARER_W, sy + 8, RWK_ARM_BOT, 8, 40, RWK_AH, color=C_STEEL),  # VERTICAL leg the beam bolts to (IBC bar-cleat pattern)
        ruby_box(f"FP combined BR rail seat ({tag})", cx - 30, sy, rail_bot - 12, 60, 55, 12, color=C_STEEL),
    ]
    blo, bhi = min(piy, poy), max(piy, poy) + 10
    # 4 wall through-bolts at the plate CORNERS — LOW pair BELOW the beam, HIGH pair near the top.
    for bx in (x_in + 20, x_out - 20):
        for bz in (RWK_ARM_BOT - 30, rail_top - 15):
            out.append(ruby_bolt(f"FP combined bolt M12 ({tag}) X{int(bx)} Z{int(bz)}", bx, blo, bz, bhi - blo, radius=6, axis="y", color=C_STEEL, head="base", nut="far"))
    # Beam locked to the upstand by 1 HORIZONTAL TEK screw (axis X) through the beam web + the upstand.
    out.append(ruby_bolt(f"FP combined beam TEK screw ({tag})", x_in - 4, sy + 28, (RWK_ARM_BOT + RWK_ARM_TOP) / 2,
                         RWK_BEARER_W + 16, radius=3, axis="x", color="#3A3A42", head="base", nut=None))
    return out


def ibc_cantilever_arms(x_to=None):
    """The 2 walkway cantilever arms that ATTACH TO THE IBC corridor uprights (rev12): each arm (a SOLID
    2×1 flat bar) cantilevers off a front upright (Yd 1046/1266) toward the walkway long beams. J6 joint =
    an END-PLATE welded to the arm end, bolted through the upright (4× M12) to a REAR backing plate — a
    bolted moment connection (mirrors the container-wall cantilever detail). Single-sourced so the
    overview/walkway models and the focused IBC model stay in register.
    `x_to` is how far the arm reaches inward (default RWK_X_L — the inner long beam)."""
    x_to = RWK_X_L if x_to is None else x_to
    ac_z, ep_t, ep_w, ep_h = (RWK_ARM_BOT + RWK_ARM_TOP) / 2.0, 8, 65, RWK_J6_EP_H   # arm mid-Z / end-plate thickness, width(Yd = arm 50.8 + weld toe) / height(Z, taller for bolts above)
    ep_bz = ac_z - 65.0                                                     # end-plate (FRONT) bottom Z37 — covers the arm weld + bears against the upright front face (clear of any rail)
    # The REAR backing plate sits in the box-interior corner, where the corridor bottom-ring X-rail also
    # starts — so its bottom is raised to BUTT the rail top (no interpenetration, no fused seam). The bolt
    # group is at Z140/170, so the shorter plate still fully spreads it. (J6 rail clash fix, 2026-08-17.)
    bp_bz = IBC_FOOT_PLATE_T + IBC_FRAME_RHS                                 # 62.8 — corridor bottom-ring X-rail TOP; backing plate rests on it
    bp_h  = (ep_bz + ep_h) - bp_bz                                          # keep the plate TOP at Z185.3
    c_bolt = "#3A3A42"                                                       # dark — bolts/screws must read distinct from the steel (as the foot anchors do)
    parts = []
    for yd in RWK_UP_YDS:
        parts += _rwk_xbeam(f"RWk center cantilever Yd{yd}", yd, x_to, RWK_X_UP - ep_t)   # arm ends SHORT so the end-plate isn't buried in it
        ac_y = yd + RWK_ARM_W / 2.0
        parts.append(ruby_box(f"RWk J6 end-plate Yd{yd}", RWK_X_UP - ep_t, ac_y - ep_w/2, ep_bz, ep_t, ep_w, ep_h, color=C_STEEL))       # welded to arm end (between arm + upright)
        parts.append(ruby_box(f"RWk J6 backing plate Yd{yd}", RWK_X_UP + IBC_FRAME_RHS, ac_y - ep_w/2, bp_bz, ep_t, ep_w, bp_h, color=C_STEEL))  # rear backing plate — BUTTS the bottom rail (bp_bz)
        for bz in RWK_J6_BOLT_ZS:                                           # 2 M12 — CENTRAL column (Yd 0), BOTH above the arm (bearing-type); clears the rail AND the welded arm
            bx0 = RWK_X_UP - ep_t                                           # shank start = end-plate front (−X) face
            blen = IBC_FRAME_RHS + 2*ep_t + 8                               # 74 — through end-plate + upright + backing plate, protruding
            parts.append(ruby_bolt(f"RWk J6 bolt M12 Yd{yd}", bx0, ac_y, bz, blen, radius=6, axis="x", color=c_bolt, head="base", nut="far"))  # hex head (front) + hex nut (back)
        # half-lap HOLD-DOWN: 1 #14 TEK screw per crossing (from the underside, through the beam into the arm)
        for bx in sorted(b for b in RWK_BEARER_XS if x_to - 1 < b < RWK_X_UP):
            parts.append(ruby_bolt(f"RWk half-lap TEK screw Yd{yd} X{int(bx)}", bx + RWK_BEARER_W / 2.0, ac_y, RWK_ARM_BOT, RWK_AH, radius=3, axis="z", color=c_bolt, head="base", nut=None))  # self-drilling — hex head seats FLUSH on the arm underside (head top at RWK_ARM_BOT), shank through arm + beam to the top face
    return parts


def fp_combined_corner_plates():
    """Both right-corner COMBINED plates (near + far) — the shared anchor for the film
    plane's bottom-right (BR) rail AND the walkway right beam. Factored out so the
    overview can put it on its own tag (visible in BOTH the Film-Plane and Walkway scenes)."""
    parts = []
    for wall_yd, din in ((0, 1), (C_WID, -1)):
        parts += fp_combined_corner_plate(wall_yd, din)
    return '\n'.join(parts)


def near_fixed_deck_grate(name, x0, z, t, color, alpha=None):
    """The FIXED near-walkway deck as ONE continuous piece: a WALKWAY_W-deep strip from x0 to
    WALKWAY_RIGHT_X with the EP/battery bump-out (WALKWAY_NEAR_WIDE_W deep, over
    [WALKWAY_NEAR_WIDE_X_L .. _X_R]) as an INTEGRAL inboard tab — not a separate butt-jointed
    section. The wall edge is inset one standard bracket-plate thickness (the 2mm-heavier wide
    plate is absorbed under the tab). The removable door-end lift-out band (near_x_l..X950) is a
    SEPARATE piece by design (it lifts out for transport) and is drawn by the caller."""
    bt = WALKWAY_BRACKET_T
    xr = WALKWAY_RIGHT_X
    wxl, wxr, ww = WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_X_R, WALKWAY_NEAR_WIDE_W
    # Wall edge at Yd=bt; inboard edge at Yd=WALKWAY_W, stepping out to Yd=ww over the bump span.
    pts = [(x0, bt), (xr, bt), (xr, WALKWAY_W),
           (wxr, WALKWAY_W), (wxr, ww), (wxl, ww), (wxl, WALKWAY_W),
           (x0, WALKWAY_W)]
    return ruby_prism(name, pts, z, t, color=color, alpha=alpha, holes=NEAR_GRATE_HOLES)   # sump / TAP-01 / BV-05 riser clearances


def left_liftout_grate(name, z, t, color, alpha=None):
    """The removable LEFT lift-out deck as ONE continuous piece: a WALKWAY_W-wide strip
    (X WALKWAY_LEFT_X..+WALKWAY_W, Yd 0..C_WID) with BOTH widenings integral — the drum-exit
    punch-out tab (out to WALKWAY_LEFT_WIDE_W over Yd [_YD_L.._YD_R]) and the muslin-drop notch
    (bitten IN to WALKWAY_MUSLIN_NOTCH_L_X0 over Yd [_YD0 .. +_DY]) — so no butt joint or extra
    support is introduced at either feature. Both sit on the same inboard (tray-facing) edge."""
    lx0 = WALKWAY_LEFT_X
    lx1 = lx0 + WALKWAY_W                                   # inboard edge
    tab_x1 = lx1 + (WALKWAY_LEFT_WIDE_W - WALKWAY_W)        # punch-out tab outer edge
    pyl, pyr = WALKWAY_LEFT_WIDE_YD_L, WALKWAY_LEFT_WIDE_YD_R
    nyd0 = WALKWAY_MUSLIN_NOTCH_YD0
    nyd1 = nyd0 + WALKWAY_MUSLIN_NOTCH_DY
    nx0 = WALKWAY_MUSLIN_NOTCH_L_X0                         # notch bites in to here
    pts = [(lx0, 0), (lx0, C_WID), (lx1, C_WID),
           (lx1, nyd1), (nx0, nyd1), (nx0, nyd0), (lx1, nyd0),   # muslin notch (in)
           (lx1, pyr), (tab_x1, pyr), (tab_x1, pyl), (lx1, pyl),  # drum-exit punch-out (out)
           (lx1, 0)]
    return ruby_prism(name, pts, z, t, color=color, alpha=alpha)


def right_walkway_grate(name="Right walkway grate (cantilevered)"):
    """The right walkway deck in THREE butt-jointed sections, split at the cantilever-arm CENTERS
    (Yd RWK_UP_YDS + RWK_ARM_W/2): a NEAR section (wall→near-arm center), a CENTER section that
    BRIDGES the beam-free IBC-corridor bay (near-arm→far-arm center), and a FAR section (far-arm
    center→wall) carrying the muslin-drop notch. Each joint lands on a cantilever arm, so the
    center section's own rigidity spans the ~170mm open bay where the outer beam is omitted (the
    ribbon pipes cross clear beneath it). Factored out so it can sit on the Walkways tag."""
    gx0, gx1 = RWK_X_L, RWK_X_L + WALKWAY_RIGHT_W
    z, t = RWK_GRATE_Z, WALKWAY_GRATE_T
    jn = RWK_UP_YDS[0] + RWK_ARM_W / 2.0                  # near-arm center — joint 1
    jf = RWK_UP_YDS[1] + RWK_ARM_W / 2.0                  # far-arm center  — joint 2
    ny0 = WALKWAY_MUSLIN_NOTCH_YD0                        # muslin-drop notch (far section)
    ny1 = ny0 + WALKWAY_MUSLIN_NOTCH_DY
    nx1 = WALKWAY_MUSLIN_NOTCH_R_X1                       # notch bites IN from the inboard (left/tray) edge x=gx0
    # Ribbon pipe-clearance SLOTS (ruby_prism holes=) drilled into whichever section contains each band:
    sx0, sx1 = RWK_GRATE_SLOT_X
    def _slots_in(y_lo, y_hi):
        return [(sx0, b0, sx1, b1) for (b0, b1) in RWK_GRATE_SLOT_YDS if y_lo <= b0 and b1 <= y_hi]
    out = []
    out.append(ruby_prism(f"{name} near", [(gx0, 0), (gx1, 0), (gx1, jn), (gx0, jn)], z, t, color=C_WALKWAY,
                          holes=_slots_in(0, jn)))
    out.append(ruby_prism(f"{name} center (corridor bridge)", [(gx0, jn), (gx1, jn), (gx1, jf), (gx0, jf)], z, t, color=C_WALKWAY,
                          holes=_slots_in(jn, jf)))
    out.append(ruby_prism(f"{name} far", [(gx0, jf), (gx1, jf), (gx1, C_WID), (gx0, C_WID),
                                          (gx0, ny1), (nx1, ny1), (nx1, ny0), (gx0, ny0)], z, t, color=C_WALKWAY,
                          holes=_slots_in(jf, C_WID)))
    return '\n'.join(out)


def right_walkway_cantilever(include_combined=True, include_grate=True):
    """The right walkway support: a CLOSED rectangle (left+right long beams + 2 end beams) +
    2 center cantilever arms off the IBC corridor uprights (half-lapped at the long beams).
    LEFT corners on wall cleats; RIGHT corners on the COMBINED plate (rail + right beam).
    `include_combined=False` omits the combined plates (the overview draws them on their own
    tag so they show in the Film-Plane scene too; walkway.skp keeps them inline).
    `include_grate=False` omits the grate (walkway.skp draws it on the Walkways tag so the
    'Right Cantilever' scene shows the bare structure)."""
    parts = []
    lx, rx = RWK_X_L, RWK_X_R - RWK_BEARER_W
    arm_ranges = [(yd, RWK_ARM_W) for yd in RWK_UP_YDS]
    parts += _rwk_inner_beam_cranked(lx, arm_ranges, y_inset=8)   # inner beam — CRANKED around the muslin slot; ends BUTT the cleat plates (Yd8..C_WID-8)
    # OUTER beam in TWO simply-supported runs that STOP at the cantilever arms, leaving the IBC-corridor
    # bay (Yd RWK_UP_YDS[0]+arm .. RWK_UP_YDS[1], ~170mm) OPEN — no beam over the corridor, so the ribbon
    # pipes cross there in the clear (no notch). Each run bears on a combined corner plate (wall end) and
    # half-laps a cantilever arm (corridor end). The grate's CENTER section bridges the open bay (see
    # right_walkway_grate). Supersedes the pipe-notched continuous beam — an open-top notch gutted the 2×1
    # section to a 2.4mm web; breaking the outer beam over the low-load corridor bay is the cleaner fix.
    parts += _rwk_long_beam(rx, [(RWK_UP_YDS[0], RWK_ARM_W)], split=RWK_HL_POST, y0=10, y1=RWK_UP_YDS[0] + RWK_ARM_W)   # near run: combined plate → near cantilever arm
    parts += _rwk_long_beam(rx, [(RWK_UP_YDS[1], RWK_ARM_W)], split=RWK_HL_POST, y0=RWK_UP_YDS[1], y1=C_WID - 10)       # far run: far cantilever arm → combined plate
    for ey in (0, C_WID - 10 - RWK_BEARER_W):
        # end beam BUTTS between the two long beams (X lx+W .. rx) instead of overlapping them at the
        # corners — the closed rectangle is welded, but the weld is not modeled, so a clean butt reads
        # as two distinct members meeting rather than one fused corner (check_interference.py --solids).
        # NEAR end beam kept at Yd0 (NOT inset to the plate face) so it clears the SV-01/DV-02 near-corner
        # ribbon risers (the Yd10 inset speared them — water F1 fix #2 / option A, 2026-08-18).
        parts.append(ruby_box(f"RWk end beam Yd{int(ey)}", lx + RWK_BEARER_W, ey, RWK_BEARER_Z0, rx - (lx + RWK_BEARER_W), RWK_BEARER_W, RWK_ARM_TOP - RWK_BEARER_Z0, color=C_STEEL))
    parts += ibc_cantilever_arms()
    for wall_yd, din, tag in ((0, 1, "near"), (C_WID, -1, "far")):
        parts += _rwk_wall_cleat(tag, lx + RWK_BEARER_W // 2, wall_yd, din)
        if include_combined:
            parts += fp_combined_corner_plate(wall_yd, din)
    if include_grate:
        parts.append(right_walkway_grate())
    return '\n'.join(parts)


def walkways(include_right=True, include_right_hangers=None, grates_only=False):
    """Perimeter walkway sections — LOWERED deck, in place for operation.

    include_right=False omits the right (IBC-end) deck grate. include_right_hangers
    (defaults to include_right) independently controls the ceiling hangers — the
    focused film-plane model shows the right grate but NOT the hangers.

    The deck height comes from WALKWAY_H (lowered to 65mm: a 15mm grate at the
    tray-rim level), so the grating sits below the film-frame bottom (Z=100) and
    the film plane travels above the in-place walkway. The LEFT walkway (cargo-
    door side) is a removable lift-out (shown in a distinct color) — taken out
    for transport before the panel + drum swing inboard.
    """
    if include_right_hangers is None:
        include_right_hangers = include_right
    grate_z = WALKWAY_H - WALKWAY_GRATE_T   # 115mm — grate bottom (raised +50)
    t = WALKWAY_GRATE_T                      # 15mm — thin grate
    # The near/far decks rest on the gusset-bracket ARMS, which start at the plate's inner
    # face (y_arm = wall_yd + bracket_t). Inset each deck's WALL edge by the plate thickness
    # so the grate sits on the INSIDE of those plates instead of being drawn through them.
    bt = WALKWAY_BRACKET_T                    # 8mm  — standard bracket plate (wall-edge inset)

    near_x_l = WALKWAY_LEFT_X + WALKWAY_W
    near_x_r = WALKWAY_RIGHT_X
    # The near/far grates run along the side walls from the left-walkway inner edge
    # (X=near_x_l). The floor-leg cantilever redesign has no kerb beam to cut around.
    near_len = near_x_r - near_x_l

    parts = []

    # Near deck — ONE continuous fixed piece with the EP/battery bump-out integral (no butt
    # joints at the widening). The whole-system view doesn't split off the removable door-end
    # band (walkway.skp does); the >10ft sheet splice is a cut-plan detail, not modeled here.
    parts.append(near_fixed_deck_grate("Walkway Near (fixed, bump integral)",
                                       near_x_l, grate_z, t, C_WALKWAY))

    # far deck — OWNED by the walkway model (far_deck), which insets the wall edge by the plate
    # thickness; call it so the two models can't diverge (was an in-sync copy here).
    parts.append(far_deck())

    if include_right:
        if include_right_hangers and not grates_only:
            # rev12: full CANTILEVER-rectangle support (+ grate), replaces the ceiling hangers.
            # The combined corner plates are drawn separately (own tag) so they also show in
            # the Film-Plane scene, so omit them here.
            parts.append(right_walkway_cantilever(include_combined=False))
        else:
            parts.append(right_walkway_grate("Walkway Right (IBC end)"))

    # Left walkway — removable lift-out for transport (distinct color). ONE continuous piece:
    # drum-exit punch-out tab + muslin-drop notch both integral (no butt-jointed add-on).
    parts.append(left_liftout_grate("Walkway Left (REMOVABLE — transport)",
                                    grate_z, t, C_REMOVABLE))

    # grates_only (construction model): the brackets + left floor-leg cantilevers are their own
    # install steps, so skip the supports here and draw only the decks.
    if not grates_only:
        # Wall-cantilevered gusset brackets that actually hold the near & far decks up.
        parts.append(walkway_brackets())

        # Left walkway support: floor-leg cantilever brackets. Reuse the walkway model's
        # shared builder so the support design can't drift between the two models.
        parts.append('\n'.join(left_floor_cantilevers()))

    # Right walkway support is now the cantilever rectangle (right_walkway_cantilever, above),
    # built with the grate when include_right_hangers — the ceiling hangers are retired (rev12).

    return '\n'.join(parts)


def walkway_brackets(which="both"):
    """Wall-cantilevered gusset brackets carrying the NEAR and FAR walkway grates.
    `which`: "both" (default), "near", or "far" — the construction model installs the far+right
    brackets before the tray and the near brackets after it.

    Triangular-gusset steel brackets bolted to the long side-wall ribs at
    CONTAINER_RIB_SPACING (457mm / 18") centers — the cantilevers the decks rest
    on. STANDARD brackets are 8mm plate / 170mm leg / 300mm arm with 3× M12
    (triangular: 2 lower + 1 upper); the four WIDENED brackets in the near
    EP/battery zone (X 1155–2629) are 10mm plate / 200mm leg / 500mm arm with
    4× M12 (2×2 rectangular), per walkway Sheet 7. The RIGHT walkway is a
    cantilever-rectangle and the LEFT walkway is a removable lift-out, so neither is
    wall-cantilevered — they get no brackets here.

    SINGLE-SOURCED (2026-08-18): this delegates to the walkway model's full-fab bracket
    builder (`generate_walkway_model.cantilevers()`) — plate + arm + gusset + EXTERIOR reinforcing
    plate + full-length M12 through-bolts — so the overview and the dedicated walkway model can NEVER
    diverge (was a simplified duplicate that had to be hand-kept-in-sync). Late import breaks the
    wm→ov import cycle.
    """
    return cantilevers(which)


def generate_ruby():
    import generate_pinhole_water_panel as pw   # late: breaks wm<->pw cycle
    import generate_corridor_water_panel as cp   # late import (cp imports ov) — current deep-box corridor frame
    comps = [
        component("Container (ghost)", "Container", container_ghost()),
        component("Processing Tray", "Processing Tray", pw.processing_tray()),
        component("Walkway Decks (near/far/left + right grate)", "Walkways",
                  walkway_decks() + "\n" + right_walkway_grate()),
        component("Wall Cantilevers", "Cantilevers", cantilevers()),
        component("Cantilever Types", "Cantilever Types", cantilever_types()),
        component("Right Walkway (cantilever rectangle)", "Right Cantilever",
                  right_walkway_cantilever(include_grate=False)),
        # Film-plane right support beams the cantilever bolts to — real position (X4609-4649),
        # single-sourced with overview/water so it stays consistent (was a ghost at 4629-4669
        # that intersected the corridor frame).
        component("Film-Plane Support Beams (right)", "Film Plane", film_plane_beams(side="right")),
        # LEFT (cargo-door end) corners on their OWN tag so the Right-Cantilever scene can drop them.
        component("Film-Plane Support Beams (left)", "Film Plane Left", film_plane_beams(side="left")),
        # The real deep-box corridor frame the right walkway cantilevers off (solid, current
        # design — front uprights X4654 → back X5104; the tote-retaining bars are intentionally
        # omitted from this walkway-detail model).
        component("IBC Corridor Frame (deep box)", "IBC Frame", cp.frame()),
        component("Left Walkway Support", "Left Support", left_support()),
    ]
    body = '\n'.join(comps)

    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    # Scenes — Container stays on as context; scenes toggle the rest.
    scene_groups = [
        ("Walkway", ["Walkways", "Right Cantilever", "Film Plane", "Film Plane Left", "IBC Frame", "Processing Tray"]),
        ("Near/Far Cantilevers", ["Cantilevers", "Processing Tray"]),
        ("Left Support", ["Left Support", "Processing Tray"]),
        # Right Cantilever — the cantilever-rectangle support + combined corner plate + the deep-box
        # frame it mounts off. The film-plane beams (top TR + bottom BR) are HIDDEN here to declutter —
        # the combined corner plate (on the "Right Cantilever" tag) stays as the focus.
        ("Right Cantilever", ["Right Cantilever", "IBC Frame", "Processing Tray"]),
    ]
    scene_groups_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags))
        for n, tags in scene_groups) + ']'

    sf_meta = draw.sketchfab_meta_ruby(
        "TBS-001 Walkway Model",
        "The perimeter walkway provides dry-foot operator access around all four sides of the "
        "processing tray without wading through chemical solution.",
        draw.model_uid("walkway"), "sketchup")

    return f'''# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("TBS-001 Walkway + Cantilevers", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild: erase ALL prior instances.
to_erase = entities.to_a.select {{ |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

{sf_meta}
# ── Tags (layers) ──
{tags_ruby}

# ── Subsystems (each a component on its tag) ──
{body}

# ── "Labeled" scene callouts (Labels tag — shown only in the "Labeled" scene) ──
{walkway_labels()}

{draw.license_note()}

# ── Type callouts for the "Cantilevers" scene (on the Cantilever Types tag) ──
{cantilever_type_labels()}

model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier generator versions ──
keep_tags = {keep_tags_ruby}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

# ── Scenes — one shared iso camera; scenes only toggle visibility ──
model.layers.each {{ |l| l.visible = true }}
model.layers["Labels"].visible = false if model.layers["Labels"]  # frame geometry, not labels
model.layers["Cantilever Types"].visible = false if model.layers["Cantilever Types"]  # catalog shows only in its own scene
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(-0.55, -0.7, 0.45); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.4)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents
model.active_view.zoom(0.72)   # pull back so callouts have margin (and read larger)

# Overview — all subsystems, Labels + type-catalog OFF; listed first.
model.pages.add("Overview")
{scene_groups_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == default_layer || l.name == "Container" || tags.include?(l.name)) }}
  page = model.pages.add(name)
  page.use_camera = true
}}

# ── "Cantilevers" — one of each UNIQUE bracket type, isolated side-by-side with a
#    close-up camera (the only scene showing the Cantilever Types catalog tag; the
#    wall is hidden so the full bracket — plate, arm, gusset, bolts — reads) ──
model.layers.each {{ |l| l.visible = (l.name == "Cantilever Types") }}
ct_tgt = Geom::Point3d.new({draw.mm(5000)}, {draw.mm(-100)}, {draw.mm(450)})
ct_dir = Geom::Vector3d.new(-0.18, -0.84, 0.38); ct_dir.normalize!
ct_eye = ct_tgt.offset(ct_dir, {draw.mm(8800)})
ct_cam = Sketchup::Camera.new(ct_eye, ct_tgt, Z_AXIS)
ct_cam.perspective = true
ct_cam.fov = 46
model.active_view.camera = ct_cam
ctp = model.pages.add("Cantilevers")
ctp.use_camera = true

model.layers.each {{ |l| l.visible = true }}
model.layers["Cantilever Types"].visible = false if model.layers["Cantilever Types"]

# Labeled — Overview view + callouts on the major parts, listed LAST (project rule).
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents
model.active_view.zoom(0.72)
model.layers["Labels"].visible = true if model.layers["Labels"]
lpage = model.pages.add("Labeled"); lpage.use_camera = true
model.layers["Labels"].visible = false if model.layers["Labels"]

model.commit_operation
{{ success: true, model: "Walkway + Cantilevers",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Ruby for the TBS-001 Walkway + Cantilever model")
    parser.add_argument("--save", action="store_true",
                        help="Write Ruby to src/models/walkway.rb")
    parser.add_argument("--send", action="store_true",
                        help="Send the Ruby straight to the running SketchUp")
    parser.add_argument("--skp", action="store_true",
                        help="After --send, save models/walkway.skp")
    args = parser.parse_args()

    ruby = generate_ruby()

    if args.save:
        out = os.path.join(os.path.dirname(__file__), "walkway.rb")
        with open(out, "w") as f:
            f.write(ruby)
        print(f"  {out} saved ({len(ruby)} bytes)")

    if args.send:
        from sketchup_client import send_ruby, SketchupError
        try:
            print(f"  SketchUp: {send_ruby(ruby)}")
        except SketchupError as e:
            print(f"  error: {e}", file=sys.stderr)
            sys.exit(1)

    if args.skp:
        if not args.send:
            print("  --skp requires --send", file=sys.stderr)
            sys.exit(1)
        from sketchup_client import send_ruby
        skp = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           "..", "..", "models", "walkway.skp"))
        print(f"  saving {skp} ...")
        print("  " + send_ruby('m=Sketchup.active_model; "saved=#{m.save(' + repr(skp) + ')}"'))

    if not args.save and not args.send:
        print(ruby)
