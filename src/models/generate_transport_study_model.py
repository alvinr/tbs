#!/usr/bin/env python3
"""TBS-001 — TRANSPORT STUDY (rebuilt FAITHFUL to lighttrap.skp).

This study reuses lighttrap.skp's OWN builders (lt.*) for the real panel + drum +
suspension + doors, and adds only the transport CONTEXT: the film-plane left rails
(the obstacle) and the ghosted container/walkway — all already in lighttrap. The
real moving assembly is built ONCE and placed STATICALLY at two positions:

  - Operating / camera  → identity (drum protrudes out the cargo door, X-400)
  - Transport           → translated +PANEL_SLIDE (panel retracted, drum inboard)

So the cargo-door transport clearance reads against the real geometry — the ceiling
rails stop at the door (X-30..1070, from lt.carriage_fixed), the drum is its real
Ø900 size, the panel is the real stepped hinge panel — with NO drifted design.

The earlier exploratory study (split panel, steel drum frame, removable TL rail,
4-hanger suspension) is preserved in git tag `transport-study-explore`.

NOTE: faithful means we inherit lighttrap's known film-rail Z drift (lt.film_plane_left
uses RAIL_OFF, not RAIL_OFF_BOT) — fix it in lighttrap and this study follows.

    python3 src/models/generate_transport_study_model.py --send          # push to SketchUp
    python3 src/models/generate_transport_study_model.py --send --skp     # + save .skp
"""
import argparse
import os
import sys

import generate_sketchup_model as ov
import generate_lighttrap_model as lt

component = ov.component
PANEL_SLIDE = ov.PANEL_SLIDE                # 880

TAGS = ["Context", "Door Frame", "Carriage Rails", "Film Plane Rails",
        "Assembly (camera)", "Assembly (transport)", "Labels"]


def fixed_components():
    """Subsystems that do NOT move — reused verbatim from lighttrap."""
    return '\n'.join([
        component("Context (ghost)", "Context", lt.context(x_far=lt.PARTIAL_X)),
        component("Fixed Door Frame", "Door Frame", lt.door_frame(include_seal=False)),
        component("Carriage Rails + Locks", "Carriage Rails", lt.carriage_fixed()),
        component("Film-Plane Rails (left)", "Film Plane Rails", lt.film_plane_left()),
    ])


def moving_assembly_body():
    """The real lighttrap moving assembly at slide=0 (operating coords). Built into
    one definition, then placed twice via instance transforms."""
    return '\n'.join([
        lt.hinge_panel(),
        lt.bay(),
        lt.drum_housing(lt.DRUM_CX, lt.DRUM_CY),
        lt.drum_rotor(lt.DRUM_CX, lt.DRUM_CY),
        lt.fan_b(),
        lt.carriage_moving(0),
    ])


def generate_ruby():
    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Transport Study (lighttrap-true)", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

to_erase = entities.to_a.select {{ |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

{tags_ruby}

# ── fixed subsystems (verbatim from lighttrap) ──
{fixed_components()}

# ── the REAL lighttrap moving assembly, built ONCE, placed at camera + transport ──
defn = model.definitions.add("Moving Assembly")
ents = defn.entities
{moving_assembly_body()}

ic = entities.add_instance(defn, Geom::Transformation.new)
ic.name = "Assembly (camera)"
ic.layer = model.layers["Assembly (camera)"]
it = entities.add_instance(defn, Geom::Transformation.translation([{PANEL_SLIDE}.mm, 0, 0]))
it.name = "Assembly (transport)"
it.layer = model.layers["Assembly (transport)"]

model.definitions.purge_unused
model.materials.purge_unused

# drop stale tags left by earlier study builds (keep only ours + default)
keep_tags = [{', '.join(f'"{t}"' for t in TAGS)}]
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

# ── camera + scenes ──
show = lambda {{ |hide|
  model.layers.each {{ |l| l.visible = true }}
  hide.each {{ |n| model.layers[n].visible = false if model.layers[n] }}
}}
def isocam(model, cx, cy, cz, zoom)
  dir = Geom::Vector3d.new(-0.6, -0.72, 0.42); dir.normalize!
  ctr = Geom::Point3d.new(cx.mm, cy.mm, cz.mm)
  eye = ctr.offset(dir, 12000.mm)
  model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
  model.active_view.camera.perspective = true
  model.active_view.zoom_extents
  model.active_view.zoom(zoom)
end

# Operating / camera — assembly deployed, drum protruding out the door
show.call(["Assembly (transport)"])
isocam(model, 200, 1181, 1200, 0.85)
model.pages.add("Operating (camera)").use_camera = true

# Transport — assembly slid inboard +{PANEL_SLIDE}
show.call(["Assembly (camera)"])
isocam(model, 650, 1181, 1200, 0.85)
model.pages.add("Transport").use_camera = true

model.layers.each {{ |l| l.visible = true }}
model.commit_operation

{{ success: true, model: "Transport Study (lighttrap-true)",
   slide_mm: {PANEL_SLIDE},
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TBS-001 transport study (lighttrap-true)")
    parser.add_argument("--save", action="store_true", help="Write Ruby to transport-study.rb")
    parser.add_argument("--send", action="store_true", help="Send to running SketchUp")
    parser.add_argument("--skp", action="store_true", help="After --send, save models/transport-study.skp")
    args = parser.parse_args()

    ruby = generate_ruby()

    if args.save:
        out = os.path.join(os.path.dirname(__file__), "transport-study.rb")
        with open(out, "w") as f:
            f.write(ruby)
        print(f"  {out} saved ({len(ruby)} bytes)")

    if args.send:
        from sketchup_client import send_ruby, SketchupError
        try:
            print(f"  SketchUp: {send_ruby(ruby, timeout=180.0)}")
        except SketchupError as e:
            print(f"  error: {e}", file=sys.stderr)
            sys.exit(1)

    if args.skp:
        if not args.send:
            print("  --skp requires --send", file=sys.stderr)
            sys.exit(1)
        from sketchup_client import send_ruby
        skp = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models", "transport-study.skp"))
        print(f"  saving {skp} ...")
        print("  " + send_ruby('m=Sketchup.active_model; "saved=#{m.save(' + repr(skp) + ')}"'))
