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
    ceiling-hung bearer/rod hangers). Single-sourced via ov.right_walkway_cantilever().
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
import generate_sketchup_model as ov          # helpers, materials, constants
import tbs_constants as k                       # right-hanger constants ov doesn't re-export

ruby_box = ov.ruby_box
ruby_cylinder = ov.ruby_cylinder
ruby_tri = ov.ruby_tri
component = ov.component

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
#  the right walkway is now ov.right_walkway_cantilever().)

# Exterior reinforcing plate (from generate_walkway_diagram.py View C).
REINF_W, REINF_H, REINF_T = 100, 180, 6

C_STEEL, C_TRAY, C_SHELL = ov.C_STEEL, ov.C_TRAY, ov.C_SHELL
C_WALKWAY, C_REMOVABLE, C_ALUM = ov.C_WALKWAY, ov.C_REMOVABLE, ov.C_ALUM
C_BOLT, C_HEX = "#505058", "#3C3C44"

# Left lift-out support — FLOOR-LEG CANTILEVER brackets (replaces the edge beam + wall seats).
LC_LEGX, LC_POST, LC_PW = k.LEFT_WK_CANT_LEG_X, k.LEFT_WK_CANT_POST, k.LEFT_WK_CANT_POST_W
LC_FOOT, LC_FX0 = k.LEFT_WK_CANT_FOOT, k.LEFT_WK_CANT_FOOT_X0
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
            f'  txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'  txt.layer = model.layers["Labels"] rescue nil\n'
            f'end')
    for x, y, z, text, dx, dy, dz in WALKWAY_POINT_LABELS:
        rows.append(
            f'anc = Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    return '\n'.join(rows)


# ── Ghost container (floor + ceiling + both long walls) ──────────────────────

def container_ghost():
    """Low-alpha floor, ceiling and the two long side walls, so the exterior
    cantilever reinforcing plates + bolt-throughs read through the near/far
    walls. End walls omitted (they'd clutter this view)."""
    return '\n'.join([
        ruby_box("Floor (ghost)", 0, 0, -WALL_T, C_LEN, C_WID, WALL_T,
                 color=C_SHELL, alpha=0.22),
        ruby_box("Ceiling (ghost)", 0, 0, C_HGT, C_LEN, C_WID, WALL_T,
                 color=C_SHELL, alpha=0.10),
        ruby_box("Side wall near (ghost)", 0, -WALL_T, 0, C_LEN, WALL_T, C_HGT,
                 color=C_SHELL, alpha=0.14),
        ruby_box("Side wall far (ghost)", 0, C_WID, 0, C_LEN, WALL_T, C_HGT,
                 color=C_SHELL, alpha=0.14),
    ])


# ── Walkway grated decks (the removable "gates") ─────────────────────────────

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
    parts.append(ruby_box("Walkway Near (door-end, removable)", near_x_l, BRK_T, GRATE_Z,
                          liftout_x - near_x_l, WK_W - BRK_T, t, color=C_REMOVABLE))
    parts.append(ov.near_fixed_deck_grate("Walkway Near (fixed, bump integral)",
                                          liftout_x, GRATE_Z, t, C_WALKWAY))

    # Far deck.
    parts.append(ruby_box("Walkway Far", near_x_l, WK_FAR_YD, GRATE_Z,
                          near_x_r - near_x_l, WK_W - BRK_T, t, color=C_WALKWAY))

    # (The right grate rides the Walkways tag via ov.right_walkway_grate() — see the
    #  component list — so it shows with the decks but not in the bare Right-Cantilever scene.)

    # Left deck — removable lift-out (distinct color) as ONE continuous piece: drum-exit
    # punch-out tab + muslin-drop notch both integral (no butt-jointed add-on). Shared helper.
    parts.append(ov.left_liftout_grate("Walkway Left (removable)", GRATE_Z, t, C_REMOVABLE))
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
    bt, vh = BRK_T, BRK_H                                   # standard 8mm / 150mm
    btw, vhw = k.WALKWAY_WIDE_BRACKET_T, k.WALKWAY_WIDE_BRACKET_H   # widened 10mm / 200mm
    plate_w = 120
    gusset_reach = 70
    # Bolt patterns (X offset, Z): standard 3 (triangular); widened 4 (rectangular,
    # per Sheet 7: lower pair Z=35, upper pair Z=160, both ±32mm from CL).
    bolt_pat_std  = [(0, vh - 30), (-32, 42), (32, 42)]
    bolt_pat_wide = [(-32, 35), (32, 35), (-32, 160), (32, 160)]

    b   = btw if wide else bt                       # plate/arm/gusset thickness
    v   = vhw if wide else vh                        # vertical leg height
    arm_d = b + 2
    arm_bot = GRATE_Z - arm_d
    rch = WK_NEAR_WIDE_W if wide else reach         # arm reach (500mm widened deck)
    rw  = 120 if wide else REINF_W                  # exterior reinf plate W
    rh  = 220 if wide else REINF_H                  #                       H
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
    parts.append(ruby_box(f"{nm} arm", x - b / 2, y_arm, arm_bot,
                          b, rch - b, arm_d, color=C_STEEL))
    # gusset triangle bracing the arm from below — same X as the arm (directly under
    # it, push −b), and its back edge butts the plate's container-facing face so the
    # gusset→plate joint reads as a clean edge (not passing through the plate)
    xg = x - b / 2
    y_back = wall_yd + sign * b           # plate's container-facing face
    y_far = wall_yd + sign * gusset_reach
    parts.append(ruby_tri(f"{nm} gusset",
                          (xg, y_back, 0), (xg, y_back, arm_bot),
                          (xg, y_far, arm_bot), -b, color=C_STEEL))
    # EXTERIOR reinforcing plate on the outside wall face
    reinf_y0 = (-WALL_T - REINF_T) if sign > 0 else (C_WID + WALL_T)
    parts.append(ruby_box(f"{nm} ext reinf plate", x - rw / 2, reinf_y0,
                          reinf_z0, rw, REINF_T, rh, color=C_STEEL))
    # M12 through-bolts (3× std / 4× widened) + exterior hex heads
    for dx, bz in bolt_pat:
        bx = x + dx
        shank_y0 = (-WALL_T - REINF_T) if sign > 0 else (wall_yd - b)
        parts.append(ruby_cylinder(f"{nm} bolt M12", bx, shank_y0, bz,
                                   6, shank_len, color=C_BOLT, axis="y"))
        hy = (-WALL_T - REINF_T - 6) if sign > 0 else (C_WID + WALL_T + REINF_T)
        parts.append(ruby_box(f"{nm} bolt head", bx - 9, hy, bz - 9,
                              18, 6, 18, color=C_HEX))
    return parts


def cantilevers():
    """Near + far wall-cantilevered gusset brackets IN SITU, each shown with its
    full through-wall detail through the ghosted side walls. STANDARD brackets are
    8mm plate / 150mm leg / 300mm arm with 3× M12 (triangular); the four WIDENED
    brackets in the near EP/battery zone (X 1155–2629) are 10mm plate / 200mm leg /
    500mm arm with 4× M12 (rectangular, matching walkway Sheet 7)."""
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
    """ONE right-walkway CENTER CANTILEVER ARM for the catalog: an IBC-upright stub + the
    40x40 SHS arm cantilevering off it (toward -X) + the upright clamp + an M12 bolt."""
    armb, armt, aw = ov.RWK_ARM_BOT, ov.RWK_ARM_TOP, ov.RWK_ARM_W   # 75, 115, 40 (arm underside now matches the left)
    s = ov.IBC_FRAME_RHS                                            # 50 upright RHS
    reach = ov.RWK_X_UP - ov.RWK_X_L   # 325 (was hardcoded 405, stale from the retired 4734 portal)
    return [
        ov.ruby_box("Type RWk IBC upright (50x50 RHS)", x0, 0, 0, s, s, armt + 220, color=ov.C_STEEL),
        ov.ruby_box("Type RWk cantilever arm (40x40 SHS)", x0 - reach, 0, armb, reach, aw, armt - armb, color=ov.C_STEEL),
        ov.ruby_box("Type RWk upright clamp", x0 - 4, aw + 4, armb - 25, s + 8, 8, (armt - armb) + 55, color=ov.C_STEEL),
        ov.ruby_cylinder("Type RWk upright bolt M12", x0 + s / 2, -12, armb + 6, 6, aw + 24, color=ov.C_STEEL, axis="y"),
    ]


def _floor_cant_type_parts(x0, reach, suffix, target_x):
    """ONE LEFT-walkway FLOOR-LEG CANTILEVER bracket for the type-catalog — foot plate +
    50x50 post to the grate bottom + arm at Z75-115 reaching `reach` mm in — isolated at
    catalog X station `x0`, near wall. Built twice: the STANDARD reach (arm to the grate
    inner edge, X470) and the EXTENDED reach (X770, the 3 brackets on the drum-exit
    punch-out)."""
    foot_l, foot_w, foot_t = LC_FOOT
    az0, az1 = LC_ARM_Z0, GRATE_Z
    return [
        ruby_box(f"Type FloorCant {suffix} foot plate", x0 - foot_l / 2, 0, 0,
                 foot_l, foot_w, foot_t, color=C_STEEL),
        ruby_box(f"Type FloorCant {suffix} post (2x2x0.120 SHS)", x0 - LC_POST / 2, 0, 0,
                 LC_POST, LC_PW, az1, color=C_STEEL),
        ruby_box(f"Type FloorCant {suffix} arm (to X{target_x})", x0 + LC_POST / 2, 0, az0,
                 reach, LC_ARM_W, az1 - az0, color=C_STEEL),
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
    parts += _floor_cant_type_parts(CT_SEAT_X, LC_STD - arm_x0, "short", int(LC_STD))
    parts += _floor_cant_type_parts(CT_SEAT_LONG_X, LC_WIDE - arm_x0, "long", int(LC_WIDE))
    parts += _cantilever_parts("Type Standard", CT_STD_X, 0, +1, WK_W, False)
    parts += _cantilever_parts("Type Widened", CT_WIDE_X, 0, +1, WK_NEAR_WIDE_W, True)
    # rev12 right-walkway support brackets (reuse the single-sourced overview builders):
    parts += ov._rwk_wall_cleat("Type RWk Cleat", CT_RWK_CLEAT_X, 0, 1)
    parts += ov.fp_combined_corner_plate(0, 1, cx=CT_RWK_PLATE_X)
    parts += _rwk_arm_type_parts(CT_RWK_ARM_X)
    return '\n'.join(parts)


def cantilever_type_labels():
    """Ruby: a callout naming each unique bracket type, on the 'Cantilever Types'
    tag so they show only in the 'Cantilevers' scene."""
    labels = [  # left→right: floor-leg short, floor-leg long, standard, widened
        (CT_SEAT_X, 0, GRATE_Z,
         "FLOOR-LEG CANTILEVER — standard reach\n50x50 post on bare floor + arm to the\ngrate inner edge (X=470)",
         -200, -300, 800),
        (CT_SEAT_LONG_X, 0, GRATE_Z,
         "FLOOR-LEG CANTILEVER — extended reach\n3 of the 5 brackets reach to X=770 on\nthe drum-exit punch-out (deeper landing)",
         -200, -300, 800),
        (CT_STD_X, 0, BRK_H,
         "STANDARD CANTILEVER\n8mm plate / 150 leg / 300 arm\n3x M12 (triangular)",
         0, -300, 720),
        (CT_WIDE_X, 0, k.WALKWAY_WIDE_BRACKET_H,
         "WIDENED CANTILEVER (EP / battery zone)\n10mm plate / 200 leg / 500 arm\n4x M12 (rectangular)",
         200, -300, 850),
        (CT_RWK_CLEAT_X, 0, ov.RWK_ARM_TOP,
         "RIGHT WALKWAY — WALL CLEAT (left corners)\n8mm back-plate + ext plate + shelf,\nthe long beam lands on it; M12 through-bolts",
         -150, -300, 800),
        (CT_RWK_PLATE_X, 0, k.FP_RAIL_ZC_BOT,
         "RIGHT WALKWAY — COMBINED CORNER PLATE (right corners)\n10mm, carries the walkway right beam (Z70 seat)\n+ the BR film rail (web-vertical: Z232 seat / Z270 bolt); 4x M12",
         0, -300, 850),
        (CT_RWK_ARM_X, 0, ov.RWK_ARM_TOP,
         "RIGHT WALKWAY — CENTER CANTILEVER ARM\n40x40 SHS off an IBC corridor upright\n(half-lapped at the long beams); M12 clamp",
         150, -300, 820),
    ]
    rows = []
    for x, y, z, text, dx, dy, dz in labels:
        rows.append(
            f'anc = Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'txt.layer = model.layers["Cantilever Types"] rescue nil')
    return '\n'.join(rows)


# ── Right walkway: cantilever rectangle (rev12) ──────────────────────────────
# The ceiling-hung right_hangers() support is retired; the right walkway is now a
# self-supporting cantilever rectangle built by ov.right_walkway_cantilever()
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
        reach = LC_WIDE if wide else LC_STD     # 770 (punch-out) / 470 (standard)
        aw = LC_ARM_WW if wide else LC_ARM_W    # 60 / 40
        parts.append(ruby_box(f"Left cantilever {i} foot plate", LC_FX0, y - foot_w / 2, 0,
                              foot_l, foot_w, foot_t, color=C_STEEL))
        parts.append(ruby_box(f"Left cantilever {i} post (2x2x0.120 SHS)",
                              LC_LEGX - LC_POST / 2, y - LC_PW / 2, 0,
                              LC_POST, LC_PW, az1, color=C_STEEL))
        parts.append(ruby_box(f"Left cantilever {i} arm (to X{int(reach)})", arm_x0,
                              y - aw / 2, az0, reach - arm_x0, aw, az1 - az0, color=C_STEEL))
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

def generate_ruby():
    import generate_corridor_water_panel as cp   # late import (cp imports ov) — current deep-box corridor frame
    comps = [
        component("Container (ghost)", "Container", container_ghost()),
        component("Processing Tray", "Processing Tray", ov.processing_tray()),
        component("Walkway Decks (near/far/left + right grate)", "Walkways",
                  walkway_decks() + "\n" + ov.right_walkway_grate()),
        component("Wall Cantilevers", "Cantilevers", cantilevers()),
        component("Cantilever Types", "Cantilever Types", cantilever_types()),
        component("Right Walkway (cantilever rectangle)", "Right Cantilever",
                  ov.right_walkway_cantilever(include_grate=False)),
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

    sf_meta = ov.sketchfab_meta_ruby(
        "TBS-001 Walkway Model",
        "The perimeter walkway provides dry-foot operator access around all four sides of the "
        "processing tray without wading through chemical solution.",
        ov.model_uid("walkway"), "sketchup")

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

{ov.license_note()}

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
ct_tgt = Geom::Point3d.new({ov.mm(5000)}, {ov.mm(-100)}, {ov.mm(450)})
ct_dir = Geom::Vector3d.new(-0.18, -0.84, 0.38); ct_dir.normalize!
ct_eye = ct_tgt.offset(ct_dir, {ov.mm(8800)})
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
