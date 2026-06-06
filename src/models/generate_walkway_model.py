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
  • **Right Hangers** — the ceiling-hung right walkway: two bearer angles + 5
    rod-pairs of M10 threaded rod up to ceiling plates.
  • **Processing Tray** — the SS basin the walkway surrounds (reuses the overview
    builder).
  • **Container** — a low-alpha ghost (floor, ceiling, both long walls) so the
    exterior braces + bolt-throughs show.

Scenes separate the gates (decks) from the cantilevers, plus the right hangers.

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
R_BEARER, R_BEARER_T = k.WALKWAY_RIGHT_BEARER_SIZE, k.WALKWAY_RIGHT_BEARER_T
R_HANGER_D = k.WALKWAY_RIGHT_HANGER_D
R_HANGER_Y1, R_HANGER_N = k.WALKWAY_RIGHT_HANGER_Y1, k.WALKWAY_RIGHT_HANGER_N
R_CEIL_PLATE = k.WALKWAY_RIGHT_CEIL_PLATE          # (100, 60, 6)

# Exterior reinforcing plate (from generate_walkway_diagram.py View C).
REINF_W, REINF_H, REINF_T = 100, 180, 6

C_STEEL, C_TRAY, C_SHELL = ov.C_STEEL, ov.C_TRAY, ov.C_SHELL
C_WALKWAY, C_REMOVABLE, C_ALUM = ov.C_WALKWAY, ov.C_REMOVABLE, ov.C_ALUM
C_BOLT, C_HEX = "#505058", "#3C3C44"

# Left lift-out support dimensions (40×40×3 steel SHS edge beam + 25×25×3 Al SHS legs).
L_BEARER, L_LEG, L_LEG_BASE = k.LEFT_WK_BEARER_SIZE, k.LEFT_WK_LEG_SIZE, k.LEFT_WK_LEG_BASE
L_LEG_N, L_STRIP = k.LEFT_WK_LEG_N, k.LEFT_WK_BEARING_STRIP

GRATE_Z = WK_H - GRATE_T          # 65 — grate underside / arm top

TAGS = ["Container", "Processing Tray", "Walkways", "Cantilevers",
        "Right Hangers", "Left Support"]


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
    near_x_l = WK_LEFT_X + WK_W
    near_x_r = WK_RIGHT_X
    parts = []

    # Near deck — left run, widened zone, right run (Yd 0..width).
    if WK_NEAR_WIDE_XL > near_x_l:
        parts.append(ruby_box("Walkway Near (left)", near_x_l, 0, GRATE_Z,
                              WK_NEAR_WIDE_XL - near_x_l, WK_W, t, color=C_WALKWAY))
    parts.append(ruby_box("Walkway Near (widened)", WK_NEAR_WIDE_XL, 0, GRATE_Z,
                          WK_NEAR_WIDE_XR - WK_NEAR_WIDE_XL, WK_NEAR_WIDE_W, t, color=C_WALKWAY))
    if WK_NEAR_WIDE_XR < near_x_r:
        parts.append(ruby_box("Walkway Near (right)", WK_NEAR_WIDE_XR, 0, GRATE_Z,
                              near_x_r - WK_NEAR_WIDE_XR, WK_W, t, color=C_WALKWAY))

    # Far deck.
    parts.append(ruby_box("Walkway Far", near_x_l, WK_FAR_YD, GRATE_Z,
                          near_x_r - near_x_l, WK_W, t, color=C_WALKWAY))

    # Right deck (IBC end, ceiling-hung — spans the full width).
    parts.append(ruby_box("Walkway Right (IBC end)", WK_RIGHT_X, 0, GRATE_Z,
                          R_W, C_WID, t, color=C_WALKWAY))

    # Left deck — removable lift-out (distinct color) + drum-exit punch-out.
    parts.append(ruby_box("Walkway Left (removable)", WK_LEFT_X, 0, GRATE_Z,
                          WK_W, C_WID, t, color=C_REMOVABLE))
    parts.append(ruby_box("Walkway Left punch-out", WK_LEFT_X + WK_W, WK_LEFT_WIDE_YL,
                          GRATE_Z, WK_LEFT_WIDE_W - WK_W, WK_LEFT_WIDE_YR - WK_LEFT_WIDE_YL,
                          t, color=C_REMOVABLE))
    return '\n'.join(parts)


# ── Wall cantilever brackets, with the EXTERIOR brace + bolt-throughs ────────

def cantilevers():
    """Near + far wall-cantilevered gusset brackets, each shown with its full
    through-wall detail: interior mounting plate + arm + gusset, an EXTERIOR
    reinforcing plate, and the through-bolts (hex heads outside) — all visible
    through the ghosted side walls. STANDARD brackets are 8mm plate / 150mm leg /
    300mm arm with 3× M12 in a triangular pattern; the four WIDENED brackets in
    the near EP/battery zone (X 1155–2629) are 10mm plate / 200mm leg / 500mm arm
    with 4× M12 in a rectangular pattern (matching walkway Sheet 7)."""
    bt, vh = BRK_T, BRK_H                                   # standard 8mm / 150mm
    btw, vhw = k.WALKWAY_WIDE_BRACKET_T, k.WALKWAY_WIDE_BRACKET_H   # widened 10mm / 200mm
    plate_w = 120
    gusset_reach = 70

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

    # Bolt patterns (X offset, Z): standard 3 (triangular); widened 4 (rectangular,
    # per Sheet 7: lower pair Z=35, upper pair Z=160, both ±32mm from CL).
    bolt_pat_std  = [(0, vh - 30), (-32, 42), (32, 42)]
    bolt_pat_wide = [(-32, 35), (32, 35), (-32, 160), (32, 160)]

    parts = []
    for label, wall_yd, sign, reach in sides:
        for i, x in enumerate(stations, 1):
            wide = (label == "Near" and WK_NEAR_WIDE_XL <= x <= WK_NEAR_WIDE_XR)
            b   = btw if wide else bt                       # plate/arm/gusset thickness
            v   = vhw if wide else vh                       # vertical leg height
            arm_d = b + 2
            arm_bot = GRATE_Z - arm_d
            rch = WK_NEAR_WIDE_W if wide else reach         # arm reach (500mm widened deck)
            rw  = 120 if wide else REINF_W                  # exterior reinf plate W
            rh  = 220 if wide else REINF_H                  #                       H
            bolt_pat = bolt_pat_wide if wide else bolt_pat_std
            shank_len = WALL_T + REINF_T + b
            reinf_z0 = max(0, (v - rh) // 2)
            nm = f"Cantilever {label} {i}" + (" (widened)" if wide else "")
            # interior mounting plate, flat on the wall inner face
            y_plate = wall_yd if sign > 0 else wall_yd - b
            parts.append(ruby_box(f"{nm} plate", x - plate_w / 2, y_plate, 0,
                                  plate_w, b, v, color=C_STEEL))
            # horizontal cantilever arm at grate level (deck rests on it)
            y_arm = wall_yd if sign > 0 else wall_yd - rch
            parts.append(ruby_box(f"{nm} arm", x - b / 2, y_arm, arm_bot,
                                  b, rch, arm_d, color=C_STEEL))
            # gusset triangle bracing the arm from below
            xg = x - b / 2
            y_far = wall_yd + sign * gusset_reach
            parts.append(ruby_tri(f"{nm} gusset",
                                  (xg, wall_yd, 0), (xg, wall_yd, arm_bot),
                                  (xg, y_far, arm_bot), b, color=C_STEEL))
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
    return '\n'.join(parts)


# ── Right walkway: ceiling-hung bearers + rod hangers + ceiling plates ───────

def right_hangers():
    """The ceiling-hung right walkway support: two bearer angles (X=4329/4629)
    running the full width at deck level, and 5 rod-pairs of M10 threaded rod up
    to ceiling plates (the deck rests on the bearers; no floor contact)."""
    pw, pl, pth = R_CEIL_PLATE                  # 100 × 60 × 6
    bearer_xs = (R_X, R_X + R_W)                # 4329, 4629
    # 5 hanger pairs: 1st at HANGER_Y1, rest on rib centers (matches the 2D diagram).
    hanger_yds = [R_HANGER_Y1] + list(range(RIB, C_WID, RIB))
    hanger_yds = hanger_yds[:R_HANGER_N]   # [320, 457, 914, 1371, 1828]

    parts = []
    for bx in bearer_xs:
        parts.append(ruby_box(f"Right bearer (25x25x5 L) X{bx}",
                              bx - R_BEARER / 2, 0, GRATE_Z - R_BEARER,
                              R_BEARER, C_WID, R_BEARER, color=C_STEEL))
        for yd in hanger_yds:
            parts.append(ruby_cylinder(f"Right hanger rod M10 X{bx} Y{yd}",
                                       bx, yd, GRATE_Z, R_HANGER_D / 2,
                                       C_HGT - GRATE_Z, color=C_STEEL, axis="z"))
            parts.append(ruby_box(f"Right ceiling plate X{bx} Y{yd}",
                                  bx - pw / 2, yd - pl / 2, C_HGT - pth,
                                  pw, pl, pth, color=C_STEEL))
    return '\n'.join(parts)


# ── Left walkway: removable lift-out support (bearer beam + legs + strip) ────

def left_support():
    """The LEFT walkway is a removable lift-out. Its INNER edge is carried by a
    full-width STEEL 40×40×3 SHS EDGE BEAM at X≈470 that stands in the bath→
    film-frame envelope (Z≈52..92, ~12mm proud of the deck as a toe-board/kerb) so
    it clears the chemistry bath (top Z≈42), the film-frame bottom (Z=100), AND the
    near/far tray rims (Z50) it crosses at Yd≈80/2280 — the 40mm section sits 2mm
    above the rim (a 50mm beam at Z45 fouled it).
    It is SIMPLY SUPPORTED wall-to-wall on IBC-style seat brackets BOLTED THROUGH
    the corrugated wall at each end (not cantilevered) — demountable for transport
    (the through-bolt + exterior plate can stay; the interior seat lifts off). The
    OUTER edge rests on a 15mm Al bearing strip on the tray rim + three floor legs
    at X=140 on bare floor outside the tray."""
    lxr = WK_LEFT_X + WK_W                     # 470 — inner deck edge
    lx = WK_LEFT_X                             # 170 — tray rim (bearing strip)
    leg_x = lx - 30                            # 140 — floor legs (outside tray)
    nyi, fy = WK_W, WK_FAR_YD
    span_legs = fy - nyi
    leg_yds = [round(nyi + span_legs / (L_LEG_N + 1) * (i + 1)) for i in range(L_LEG_N)]
    bath_top = k.PROC_TRAY_RIM - 8             # 42
    bz0, bz1 = k.LEFT_WK_BEAM_Z0, k.LEFT_WK_BEAM_Z1   # 52..92 — 40mm deep; bottom clears tray rim (Z50) by 2mm, top clears film frame (Z100) by 8mm
    beam_w = L_BEARER                          # 40 — section
    bt = 8                                     # seat plate thickness

    parts = []
    # Full-width STEEL edge beam (kerb), simply supported wall-to-wall.
    # 40x40 (not 50) + raised to Z52 so it clears the near/far tray rims it crosses.
    parts.append(ruby_box("Left edge beam (40x40x3 steel SHS, full width)",
                          lxr, 0, bz0, beam_w, C_WID, bz1 - bz0, color=C_STEEL))

    # IBC-style wall-seat brackets (bolt-through), one at each wall end.
    for label, wall_yd, sign in [("near", 0, +1), ("far", C_WID, -1)]:
        cxm = lxr + beam_w / 2
        y_plate = wall_yd if sign > 0 else wall_yd - bt
        parts.append(ruby_box(f"Left wall-seat plate {label}",
                              lxr - 10, y_plate, 30, beam_w + 20, bt, bz1 - 30, color=C_STEEL))
        reinf_y0 = (-WALL_T - REINF_T) if sign > 0 else (C_WID + WALL_T)
        parts.append(ruby_box(f"Left wall-seat ext plate {label}",
                              cxm - REINF_W / 2, reinf_y0, (bz0 + bz1) / 2 - REINF_H / 2,
                              REINF_W, REINF_T, REINF_H, color=C_STEEL))
        shank_y0 = (-WALL_T - REINF_T) if sign > 0 else (wall_yd - bt)
        shank_len = WALL_T + REINF_T + bt
        zc = (bz0 + bz1) / 2
        for dx, dz in [(0, 22), (-28, -16), (28, -16)]:
            bx = cxm + dx
            parts.append(ruby_cylinder(f"Left wall-seat bolt {label}",
                                       bx, shank_y0, zc + dz, 6, shank_len, color=C_BOLT, axis="y"))
            hy = (-WALL_T - REINF_T - 6) if sign > 0 else (C_WID + WALL_T + REINF_T)
            parts.append(ruby_box(f"Left wall-seat head {label}",
                                  bx - 9, hy, zc + dz - 9, 18, 6, 18, color=C_HEX))

    # Outer edge: bearing strip on the tray rim + 3 floor legs on bare floor.
    parts.append(ruby_box("Left bearing strip (Al)",
                          lx, nyi, GRATE_Z - L_STRIP, L_LEG, span_legs, L_STRIP, color=C_ALUM))
    for i, yd in enumerate(leg_yds, 1):
        parts.append(ruby_box(f"Left leg {i} (25x25x3 SHS)",
                              leg_x - L_LEG / 2, yd - L_LEG / 2, 0, L_LEG, L_LEG, GRATE_Z, color=C_ALUM))
        parts.append(ruby_box(f"Left leg {i} foot plate",
                              leg_x - L_LEG_BASE / 2, yd - L_LEG_BASE / 2, 0,
                              L_LEG_BASE, L_LEG_BASE, 3, color=C_ALUM))
        parts.append(ruby_box(f"Left leg {i} arm",
                              leg_x, yd - L_LEG / 2, GRATE_Z - 10,
                              (lx + 20) - leg_x, L_LEG, 10, color=C_ALUM))
    return '\n'.join(parts)


# ── Assemble the Ruby script ─────────────────────────────────────────────────

def generate_ruby():
    comps = [
        component("Container (ghost)", "Container", container_ghost()),
        component("Processing Tray", "Processing Tray", ov.processing_tray()),
        component("Walkway Decks (gates)", "Walkways", walkway_decks()),
        component("Wall Cantilevers", "Cantilevers", cantilevers()),
        component("Right Walkway Hangers", "Right Hangers", right_hangers()),
        component("Left Walkway Support", "Left Support", left_support()),
    ]
    body = '\n'.join(comps)

    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    # Scenes — Container stays on as context; scenes toggle the rest.
    scene_groups = [
        ("Gates (walkway decks)", ["Walkways", "Processing Tray"]),
        ("Cantilevers (+ exterior braces/bolts)", ["Cantilevers", "Processing Tray"]),
        ("Right Hangers", ["Right Hangers", "Walkways", "Processing Tray"]),
        ("Left Support (bearer + legs)", ["Left Support", "Cantilevers", "Processing Tray"]),
        ("Processing Tray", ["Processing Tray"]),
    ]
    scene_groups_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags))
        for n, tags in scene_groups) + ']'

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Walkway + Cantilevers", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild: erase ALL prior instances.
to_erase = entities.to_a.select {{ |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance)
}}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

# ── Tags (layers) ──
{tags_ruby}

# ── Subsystems (each a component on its tag) ──
{body}

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
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(-0.55, -0.7, 0.45); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.4)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

model.pages.add("Combined")
{scene_groups_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == default_layer || l.name == "Container" || tags.include?(l.name)) }}
  page = model.pages.add(name)
  page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}

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
