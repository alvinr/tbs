#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_lighttrap_transport_model.py — TBS-001 "Light Trap" in the TRANSPORT
position (models/lighttrap-transport.skp).

Exactly the same details as the operating light-trap model
(generate_lighttrap_model, reused wholesale as `lt`), but POSED for transport:
the hinge-panel assembly — panel + Ø900 fixed housing + revolving drum + EPDM
seals + the moving carriage parts (HGH20CA blocks, suspension brackets, left
beam) + Fan B — is slid inward PANEL_SLIDE (550mm) on the ceiling rails so the
housing's exterior overhang retracts behind the cargo-door plane. The carriage
locks at the TRANSPORT Destaco clamp. The two ISO cargo doors are shown CLOSED
to demonstrate the clearance.

Fixed (stay put): container context, fixed RHS door frame, HGR20 rails, both
Destaco lock-points, and the cargo doors. Moving (slid +550mm): hinge panel,
drum, Fan B, and the carriage blocks/brackets/beam.

Usage
-----
    python3 src/models/generate_lighttrap_transport_model.py           # print Ruby
    python3 src/models/generate_lighttrap_transport_model.py --save     # write .rb
    python3 src/models/generate_lighttrap_transport_model.py --send     # push to SketchUp
    python3 src/models/generate_lighttrap_transport_model.py --send --skp   # + save .skp
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov          # helpers, materials, constants
import generate_lighttrap_model as lt          # reuse every operating-pose builder

ruby_box = ov.ruby_box
component = ov.component
C_WID, C_HGT = ov.C_WID, ov.C_HGT
C_STEEL, C_CARR = ov.C_STEEL, ov.C_CARR

SLIDE = ov.PANEL_SLIDE                          # 550 — transport slide travel (mm)

# Components that ride the panel and translate +SLIDE in X for transport. The
# carriage is NOT here — its split (fixed rails/clamps vs moving blocks/brackets/
# beam) is handled inside lt.sliding_carriage(slide=SLIDE) by coordinate offset.
MOVING_TAGS = ["Hinge Panel", "Light Trap", "Fan B"]

TAGS = lt.TAGS + ["Cargo Doors", "Processing Tray", "Walkways"]


# ── Closed ISO cargo doors (transport-only; demonstrate the clearance) ───────

def cargo_doors():
    """Two corrugated steel ISO cargo-door leaves shown CLOSED over the end
    opening, just outside the fixed door frame (frame at X=-50..0). With the
    housing retracted to X≈+100, the leaves at X≈-115..-55 shut freely.

    GHOSTED (translucent) so they read as the doors — distinct from the
    container shell — while you see straight through them to the slid-back
    light-trap details behind. Leaves go lightest; the locking hardware is a
    touch more opaque so it still reads."""
    LEAF_A, HW_A = 0.20, 0.55                   # ghost alphas: leaf vs hardware
    parts = []
    dt = 60                                     # leaf thickness in X
    x0 = -115                                   # exterior face of the closed leaf
    gap = 3                                      # center meeting gap
    half = C_WID / 2
    for nm, y0 in [("R", 0.0), ("L", half + gap)]:
        # right leaf closes first (Yd 0..half), left leaf laps over center
        parts.append(ruby_box(f"Cargo door leaf {nm}", x0, y0, 0,
                              dt, half - gap, C_HGT, color=C_STEEL, alpha=LEAF_A))
        # two vertical locking bars per leaf, on the exterior face
        for f in (0.30, 0.70):
            by = y0 + (half - gap) * f
            parts.append(ruby_box(f"Locking bar {nm}{int(f*10)}", x0 - 18, by - 14,
                                  60, 28, 28, C_HGT - 120, color=C_CARR, alpha=HW_A))
        # cam handle near the center stile
        hy = y0 + (half - gap) * (0.92 if nm == "R" else 0.08)
        parts.append(ruby_box(f"Door handle {nm}", x0 - 30, hy - 12,
                              1050, 26, 24, 240, color=C_CARR, alpha=HW_A))
    return '\n'.join(parts)


# ── Partial cargo-door-end context (tray + near/far walkways) ────────────────
# Reuses the overview's tray/walkway geometry + constants, cropped to the
# cargo-door-end zone: a processing-tray section + the NEAR (pinhole-wall side,
# Yd 0) and FAR walkway decks. The LEFT walkway is the removable lift-out and is
# already taken out for transport — so it is not shown.
PARTIAL_X = 1800        # context extends from the cargo-door end to here (mm)

def processing_tray_partial():
    """A cropped section of the processing-tray basin at the cargo-door end."""
    x0 = ov.PROC_TRAY_X_L
    yN, yF = ov.PROC_TRAY_YD_NEAR, ov.PROC_TRAY_YD_FAR
    w, d = PARTIAL_X - x0, yF - yN
    st, rt, rim = 2, 2, ov.PROC_TRAY_RIM
    p = [
        ruby_box("Processing Tray Floor (partial)", x0, yN, 0, w, d, st, color=ov.C_TRAY),
        ruby_box("Tray Rim Near (partial)", x0, yN, st, w, rt, rim - st, color=ov.C_TRAY),
        ruby_box("Tray Rim Far (partial)", x0, yF - rt, st, w, rt, rim - st, color=ov.C_TRAY),
        ruby_box("Tray Rim Left (cargo end)", x0, yN, st, rt, d, rim - st, color=ov.C_TRAY),
        ruby_box("Chemistry Bath (partial)", x0 + rt, yN + rt, st,
                 w - 2 * rt, d - 2 * rt, rim - st - 8, color=ov.C_BATH, alpha=0.45),
    ]
    return '\n'.join(p)

def walkways_partial():
    """The NEAR (pinhole-wall side, Yd 0) and FAR walkway decks, cropped to the
    cargo-door-end zone. The left walkway (removable lift-out) is out for
    transport, so it is not shown."""
    grate_z = ov.WALKWAY_H - ov.WALKWAY_GRATE_T
    t = ov.WALKWAY_GRATE_T
    x0 = ov.WALKWAY_LEFT_X + ov.WALKWAY_W       # = 470 — where the long decks begin
    w = PARTIAL_X - x0
    return '\n'.join([
        ruby_box("Walkway Near (partial)", x0, 0, grate_z,
                 w, ov.WALKWAY_W, t, color=ov.C_WALKWAY),
        ruby_box("Walkway Far (partial)", x0, ov.WALKWAY_FAR_YD, grate_z,
                 w, ov.WALKWAY_W, t, color=ov.C_WALKWAY),
    ])


# ── Assemble the Ruby script (mirrors lt.generate_ruby + the transport pose) ──

def generate_ruby():
    comps = [
        component("Context", "Context", lt.context()),
        component("Fixed Door Frame", "Door Frame", lt.door_frame(include_seal=False)),
        component("Closed Cargo Doors", "Cargo Doors", cargo_doors()),
        component("Hinged Light-Trap Panel", "Hinge Panel", lt.hinge_panel()),
        # The housing-surround EPDM (interface 2) rides the housing, so it goes in
        # the Light Trap component and retracts +SLIDE with it (panel-perimeter
        # EPDM / interface 1 is already inside hinge_panel() → also moves).
        component("Revolving Light-Trap Drum", "Light Trap",
                  lt.drum() + "\n" + lt.housing_surround_seal()),
        component("Sliding Carriage System", "Sliding Carriage",
                  lt.sliding_carriage(slide=SLIDE)),
        component("Fan B (intake)", "Fan B", lt.fan_b()),
        component("Processing Tray (partial)", "Processing Tray", processing_tray_partial()),
        component("Walkways (near + far, partial)", "Walkways", walkways_partial()),
    ]
    body = '\n'.join(comps)

    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'
    moving_ruby = '[' + ', '.join(f'"{t}"' for t in MOVING_TAGS) + ']'

    scene_groups = [
        ("Transport — All", TAGS),
        ("Over Tray & Walkway", ["Hinge Panel", "Light Trap", "Sliding Carriage",
                                 "Processing Tray", "Walkways"]),
        ("Through the Doors", ["Cargo Doors", "Hinge Panel", "Light Trap", "Door Frame"]),
        ("Light-Trap Drum", ["Light Trap", "Hinge Panel"]),
    ]
    scene_groups_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags))
        for n, tags in scene_groups) + ']'

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Light Trap (Transport)", true)
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

# ── Transport pose: slide the panel-mounted components inward {SLIDE}mm in X ──
# (the carriage's own moving parts are already offset via lt.sliding_carriage).
slide_tf = Geom::Transformation.translation([{SLIDE}.mm, 0, 0])
moving_tags = {moving_ruby}
entities.grep(Sketchup::ComponentInstance).each {{ |ci|
  ci.transform!(slide_tf) if moving_tags.include?(ci.layer.name)
}}

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
{{ success: true, model: "Light Trap (Transport)",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Ruby for the TBS-001 Light Trap TRANSPORT model")
    parser.add_argument("--save", action="store_true",
                        help="Write Ruby to src/models/lighttrap-transport.rb")
    parser.add_argument("--send", action="store_true",
                        help="Send the Ruby straight to the running SketchUp")
    parser.add_argument("--skp", action="store_true",
                        help="After --send, save models/lighttrap-transport.skp")
    args = parser.parse_args()

    ruby = generate_ruby()

    if args.save:
        out = os.path.join(os.path.dirname(__file__), "lighttrap-transport.rb")
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
                                           "..", "..", "models", "lighttrap-transport.skp"))
        print(f"  saving {skp} ...")
        print("  " + send_ruby('m=Sketchup.active_model; "saved=#{m.save(' + repr(skp) + ')}"'))

    if not args.save and not args.send:
        print(ruby)
