#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_lighttrap_model.py — Generate Ruby for the TBS-001 "Light Trap"
focus model (models/lighttrap.skp).

A detailed, report-accurate model of the cargo-door end assembly only:
  - the revolving light-trap DRUM (caps, stub shafts, SKF bearings, grab rail),
  - the hinged stepped PANEL (3 zones + drum aperture + EPDM seal + hinges +
    cam latches),
  - the SLIDING carriage system (HGR20 ceiling rails, HGH20CA blocks,
    suspension brackets, left carriage beam, Destaco toggle clamps, fixed RHS
    door frame),
  - Fan B (intake) mounted on the panel — reused from the Overview's shared
    fan_duct() builder so it stays in sync.

Geometry comes from hinged-panel-report.md, ceiling-rail-report.md and
light-trap-selection.md. Helpers, materials and spatial constants are imported
from generate_sketchup_model (`ov`) — single source of truth.

Usage
-----
    python3 src/models/generate_lighttrap_model.py           # print Ruby
    python3 src/models/generate_lighttrap_model.py --save     # write lighttrap.rb
    python3 src/models/generate_lighttrap_model.py --send     # push to SketchUp
    python3 src/models/generate_lighttrap_model.py --send --skp   # + save .skp
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov   # helpers, materials, constants

# ── pull in shared helpers + constants ───────────────────────────────────────
ruby_box, ruby_cylinder = ov.ruby_box, ov.ruby_cylinder
component = ov.component
C_WID, C_HGT, WALL_T = ov.C_WID, ov.C_HGT, ov.WALL_T
DRUM_CX, DRUM_CY, DRUM_R, DRUM_H = ov.DRUM_CX, ov.DRUM_CY, ov.DRUM_R, ov.DRUM_H_LT
PANEL_CENTER_T = ov.PANEL_CENTER_T            # 120 — center-zone thickness (X)
PANEL_CORNER_T = 40                           # corner-zone thickness (report §2.1)
PANEL_FLOOR_GAP = ov.PANEL_FLOOR_GAP          # 80
YD_L, YD_R = ov.PANEL_CORNER_YD_L, ov.PANEL_CORNER_YD_R   # 756, 1606 step lines
FAN_B_YD, FAN_B_H = ov.FAN_B_YD, ov.FAN_B_H

C_STEEL, C_ALUM, C_PLY = ov.C_STEEL, ov.C_ALUM, ov.C_PLY
C_DRUM, C_GASKT, C_RAIL, C_CARR = ov.C_DRUM, ov.C_GASKT, ov.C_RAIL, ov.C_CARR
C_SHELL, C_VALVE = ov.C_SHELL, ov.C_VALVE

PANEL_Z_BOT = PANEL_FLOOR_GAP                 # 80 — bottom edge (floor gap)
PANEL_Z_TOP = 2300                            # hung from ceiling rail (rail above)

TAGS = ["Context", "Door Frame", "Hinge Panel", "Light Trap",
        "Sliding Carriage", "Fan B"]


# ── Ghosted container context (end opening only) ─────────────────────────────

def context():
    """Low-alpha stub of floor, ceiling and both side walls near X=0 so the
    assembly reads in place without modeling the whole container."""
    x0, xlen = -400, 2000
    return '\n'.join([
        ruby_box("Floor (context)", x0, 0, -WALL_T, xlen, C_WID, WALL_T,
                 color=C_SHELL, alpha=0.25),
        ruby_box("Ceiling (context)", x0, 0, C_HGT, xlen, C_WID, WALL_T,
                 color=C_SHELL, alpha=0.10),
        ruby_box("Side Wall near (context)", x0, -WALL_T, 0, xlen, WALL_T, C_HGT,
                 color=C_SHELL, alpha=0.16),
        ruby_box("Side Wall far (context)", x0, C_WID, 0, xlen, WALL_T, C_HGT,
                 color=C_SHELL, alpha=0.16),
    ])


# ── Fixed RHS door frame (seal landing, X just outboard of the panel) ────────

def door_frame():
    """50×50×3 RHS welded frame lining the cargo-door opening at X≈0. Sits
    just exterior of the panel (X=-50..0); the EPDM gasket seals against it."""
    s = 50
    x0 = -s
    # threshold rail is notched around the drum (it rotates down to the floor)
    dg0, dg1 = DRUM_CY - DRUM_R - 15, DRUM_CY + DRUM_R + 15
    parts = [
        ruby_box("Door Frame threshold L", x0, 0, 0, s, dg0, s, color=C_RAIL),
        ruby_box("Door Frame threshold R", x0, dg1, 0, s, C_WID - dg1, s, color=C_RAIL),
        ruby_box("Door Frame top", x0, 0, C_HGT - s, s, C_WID, s, color=C_RAIL),
        ruby_box("Door Frame left stile", x0, 0, 0, s, s, C_HGT, color=C_RAIL),
        ruby_box("Door Frame right stile", x0, C_WID - s, 0, s, s, C_HGT,
                 color=C_RAIL),
    ]
    return '\n'.join(parts)


# ── Hinged stepped panel (3 zones, drum aperture, seal, hinges, latches) ─────

def hinge_panel():
    h = PANEL_Z_TOP - PANEL_Z_BOT                  # panel skin height
    tc, tk = PANEL_CORNER_T, PANEL_CENTER_T        # 40 corner, 120 center
    jw = DRUM_CY - DRUM_R - YD_L                   # left/right jamb width (≈50)
    parts = []

    # Near corner (hinge side) and far corner (Fan B side) — flush 40mm zones.
    parts.append(ruby_box("Panel near corner (40mm)",
                          0, 0, PANEL_Z_BOT, tc, YD_L, h, color=C_PLY))
    parts.append(ruby_box("Panel far corner (40mm)",
                          0, YD_R, PANEL_Z_BOT, tc, C_WID - YD_R, h, color=C_PLY))

    # Center zone (120mm) framed around the Ø750 drum aperture: two jambs + header.
    parts.append(ruby_box("Panel center jamb L (120mm)",
                          0, YD_L, PANEL_Z_BOT, tk, jw, h, color=C_PLY))
    parts.append(ruby_box("Panel center jamb R (120mm)",
                          0, YD_R - jw, PANEL_Z_BOT, tk, jw, h, color=C_PLY))
    parts.append(ruby_box("Panel header over drum (120mm)",
                          0, YD_L, DRUM_H, tk, YD_R - YD_L, PANEL_Z_TOP - DRUM_H,
                          color=C_PLY))

    # 20mm neoprene compression strip lining the drum aperture (jamb inner faces).
    parts.append(ruby_box("Drum aperture seal L", 0, YD_L + jw, PANEL_Z_BOT,
                          tk, 20, DRUM_H, color=C_GASKT))
    parts.append(ruby_box("Drum aperture seal R", 0, YD_R - jw - 20, PANEL_Z_BOT,
                          tk, 20, DRUM_H, color=C_GASKT))

    # EPDM perimeter gasket — 20mm strips on the exterior face, seal to door frame.
    gw, gt = 40, 20
    z0, z1 = PANEL_Z_BOT, C_HGT - PANEL_Z_BOT
    dg0, dg1 = DRUM_CY - DRUM_R - 15, DRUM_CY + DRUM_R + 15   # clear the drum aperture
    parts.append(ruby_box("EPDM seal bottom L", -gt, 0, z0, gt, dg0, gw, color=C_GASKT))
    parts.append(ruby_box("EPDM seal bottom R", -gt, dg1, z0, gt, C_WID - dg1, gw,
                          color=C_GASKT))
    parts.append(ruby_box("EPDM seal top", -gt, 0, z1 - gw, gt, C_WID, gw, color=C_GASKT))
    parts.append(ruby_box("EPDM seal left", -gt, 0, z0, gt, gw, z1 - z0, color=C_GASKT))
    parts.append(ruby_box("EPDM seal right", -gt, C_WID - gw, z0, gt, gw, z1 - z0,
                          color=C_GASKT))

    # 3 × 200mm SS piano hinges on the left edge (Yd=0), exterior, per report §4.1.
    hd, hw, hh = 60, 30, 200
    for hz in (220, 1190, 2158):
        parts.append(ruby_box("Piano hinge", -hd / 2, 0, hz, hd, hw, hh, color=C_STEEL))

    # 4 × Southco cam latches — interior face, corners (report §4.2).
    lw, ld, lh = 55, 70, 50
    for ly in (210, C_WID - 210):
        for lz in (220, 2168):
            parts.append(ruby_box("Southco cam latch", tc, ly - ld / 2, lz - lh / 2,
                                  lw, ld, lh, color=C_VALVE))
    return '\n'.join(parts)


# ── Revolving light-trap drum (detailed) ─────────────────────────────────────

def drum():
    """Shell + 4-baffle turnstile (reused from the Overview) plus caps, stub
    shafts, SKF 6215 bearings, mount/collar plates and the interior grab rail."""
    cx, cy = DRUM_CX, DRUM_CY
    r = DRUM_R
    parts = [ov.light_trap_drum()]                 # shell (3 walled) + 2 crossed vanes

    # Top + bottom caps (5mm steel plate).
    parts.append(ruby_cylinder("LT Drum top cap", cx, cy, DRUM_H - 5, r, 5,
                               color=C_DRUM, axis="z"))
    parts.append(ruby_cylinder("LT Drum bottom cap", cx, cy, 0, r, 5,
                               color=C_DRUM, axis="z"))
    # Stub shafts (Ø75 × 150) welded to each cap.
    parts.append(ruby_cylinder("LT Drum top shaft", cx, cy, DRUM_H, 37.5, 150,
                               color=C_STEEL, axis="z"))
    # SKF 6215 bearings (Ø130 OD) — upper in the panel header, lower in the
    # floor collar. The drum rests ON the floor (Z=0); nothing extends below it.
    parts.append(ruby_cylinder("LT Upper bearing (SKF 6215)", cx, cy, DRUM_H, 65, 45,
                               color=C_STEEL, axis="z"))
    parts.append(ruby_cylinder("LT Lower bearing collar", cx, cy, 0, 75, 45,
                               color=C_STEEL, axis="z"))
    # Upper mount plate (to panel header) + lower floor collar flange (on floor).
    parts.append(ruby_box("LT Upper mount plate", cx - 110, cy - 110, DRUM_H + 45,
                          220, 220, 20, color=C_STEEL))
    parts.append(ruby_box("LT Floor collar plate", cx - 120, cy - 120, 0,
                          240, 240, 12, color=C_STEEL))

    # Interior grab rail (Ø30 × 400 vertical tube, Z 700–1100) mounted on the
    # INSIDE of the drum's +X interior-face wall — operator grabs it from within
    # the drum to pull it closed. Standoffs bridge the inner wall surface to the
    # rail; nothing penetrates the exterior wall (no light-leak path) per report §3.5.
    wall_t = 12                                 # drum shell wall thickness
    inner = cx + r - wall_t                      # inner wall surface on the +X side
    gx = cx + r - 75                             # rail sits inside the drum
    parts.append(ruby_cylinder("LT Grab rail", gx, cy, 700, 15, 400,
                               color=C_STEEL, axis="z"))
    for bz in (720, 1080):
        parts.append(ruby_box("LT Grab rail standoff", gx, cy - 6, bz,
                              inner - gx, 12, 12, color=C_STEEL))
    return '\n'.join(parts)


# ── Sliding carriage system (transport-mode 300mm slide) ─────────────────────

def sliding_carriage():
    """HGR20 ceiling rails + HGH20CA blocks + suspension brackets + left
    carriage beam + Destaco toggle clamps (operational & transport locks)."""
    parts = []
    rail_x0, rail_len = -30, 510                    # allows the 300mm transport slide
    rail_w, rail_h = 20, 30
    rail_z = C_HGT - rail_h                          # 2358 — hung from ceiling
    carr_w, carr_d, carr_h = 44, 44, 28
    brk_w, brk_d, brk_h = 60, 40, 30

    for yd, nm in [(YD_L, "L"), (YD_R, "R")]:
        parts.append(ruby_box(f"HGR20 rail {nm}", rail_x0, yd - rail_w / 2, rail_z,
                              rail_len, rail_w, rail_h, color=C_RAIL))
        parts.append(ruby_box(f"HGH20CA carriage {nm}", 18, yd - carr_d / 2,
                              rail_z - carr_h, carr_w, carr_d, carr_h, color=C_CARR))
        parts.append(ruby_box(f"Suspension bracket {nm}", 15, yd - brk_d / 2,
                              PANEL_Z_TOP, brk_w, brk_d, rail_z - carr_h - PANEL_Z_TOP,
                              color=C_STEEL))

    # Left-side carriage beam — vertical 60×60 SHS in the fixed-frame slot.
    parts.append(ruby_box("Left carriage beam (60×60 SHS)", 0, 0, PANEL_Z_BOT,
                          60, 60, PANEL_Z_TOP - PANEL_Z_BOT, color=C_STEEL))

    # Destaco 207-U toggle clamps — operational lock (X≈0) + transport lock (X≈300).
    for cx, lock in [(-10, "operational"), (290, "transport")]:
        for yd in (YD_L, YD_R):
            parts.append(ruby_box(f"Destaco clamp ({lock}) base", cx, yd - 18,
                                  rail_z - 70, 60, 36, 24, color=C_STEEL))
            parts.append(ruby_box(f"Destaco clamp ({lock}) handle", cx + 10, yd - 6,
                                  rail_z - 46, 70, 12, 12, color=C_CARR))
    return '\n'.join(parts)


# ── Fan B on the hinge panel (reused from Overview's shared builder) ─────────

def fan_b():
    return '\n'.join(ov.fan_duct("Fan B (intake)", 0, -1, FAN_B_YD, FAN_B_H))


# ── Assemble the Ruby script ─────────────────────────────────────────────────

def generate_ruby():
    comps = [
        component("Context", "Context", context()),
        component("Fixed Door Frame", "Door Frame", door_frame()),
        component("Hinged Light-Trap Panel", "Hinge Panel", hinge_panel()),
        component("Revolving Light-Trap Drum", "Light Trap", drum()),
        component("Sliding Carriage System", "Sliding Carriage", sliding_carriage()),
        component("Fan B (intake)", "Fan B", fan_b()),
    ]
    body = '\n'.join(comps)

    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    scene_groups = [
        ("Light-Trap Drum", ["Light Trap", "Hinge Panel"]),
        ("Hinge Panel & Seal", ["Hinge Panel", "Door Frame"]),
        ("Sliding Carriage", ["Sliding Carriage", "Hinge Panel"]),
        ("Fan B", ["Fan B", "Hinge Panel"]),
    ]
    scene_groups_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags))
        for n, tags in scene_groups) + ']'

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Light Trap", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild: erase ALL prior instances (no scale figure in this model).
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
dir = Geom::Vector3d.new(-0.6, -0.72, 0.45); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

model.pages.add("Overview")
{scene_groups_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }}
  page = model.pages.add(name)
  page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}

model.commit_operation
{{ success: true, model: "Light Trap",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Ruby for the TBS-001 Light Trap focus model")
    parser.add_argument("--save", action="store_true",
                        help="Write Ruby to src/models/lighttrap.rb")
    parser.add_argument("--send", action="store_true",
                        help="Send the Ruby straight to the running SketchUp")
    parser.add_argument("--skp", action="store_true",
                        help="After --send, save models/lighttrap.skp")
    args = parser.parse_args()

    ruby = generate_ruby()

    if args.save:
        out = os.path.join(os.path.dirname(__file__), "lighttrap.rb")
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
                                           "..", "..", "models", "lighttrap.skp"))
        print(f"  saving {skp} ...")
        print("  " + send_ruby('m=Sketchup.active_model; "saved=#{m.save(' + repr(skp) + ')}"'))

    if not args.save and not args.send:
        print(ruby)
