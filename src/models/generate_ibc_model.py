#!/usr/bin/env python3
"""Generate the TBS-001 IBC Stack SketchUp model (logical model: ibc-stack).

Focused on the IBC tote stack, its steel support frame, and the plumbing +
equipment panel. REUSES the helpers and component builders from the Overview
generator (generate_sketchup_model.py) — same component/tag/scene structure,
shared iso camera, and material-sharing-by-colour. Three subsystem tags grouped
into four scenes:
    1. IBC Tanks            (the four totes)
    2. IBC Frame            (the steel stacking frame/rack)
    3. Plumbing & Panel     (equipment panel + pumps/filters + water plumbing + hookups)
    4. Combined             (all three)

Usage (build into a SketchUp document — see --send note):
    python3 src/models/generate_ibc_model.py --save        # write ibc-stack.rb
    python3 src/models/generate_ibc_model.py --save --send # + send to the ACTIVE SketchUp doc

NOTE: --send builds into the ACTIVE SketchUp document (it clears it first). Open a
NEW blank SketchUp document before sending so the Overview model isn't overwritten,
then save the result as models/ibc-stack.skp.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov   # helpers + component builders (Overview)

TAGS = ["IBC Tanks", "IBC Frame", "Plumbing & Panel"]


def generate_ruby():
    """Build the Ruby script for the IBC Stack model, reusing Overview parts."""
    comps = [
        ov.component("IBC Tanks", "IBC Tanks", ov.ibc_stack(alpha=0.4)),
        ov.component("IBC Frame", "IBC Frame", ov.ibc_rack()),
        ov.component("Equipment Panel", "Plumbing & Panel", ov.equipment_panel()),
        ov.component("Water Plumbing", "Plumbing & Panel", ov.water_plumbing()),
        ov.component("Water/Waste Hookups", "Plumbing & Panel", ov.water_hookups()),
    ]
    body = '\n'.join(comps)

    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    # Four scenes — focused subsystems, then a combined view (per request).
    scenes = [
        ("IBC Tanks", ["IBC Tanks"]),
        ("IBC Frame", ["IBC Frame"]),
        ("Plumbing & Panel", ["Plumbing & Panel"]),
        ("Combined", TAGS),
    ]
    scenes_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags))
        for n, tags in scenes) + ']'

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 IBC Stack", true)
entities = model.active_entities

# Display in millimeters (UI readout only).
opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# ── Idempotent rebuild: erase all prior groups/instances (incl. any template
# scale figure) so this focused model frames tightly on the IBC assembly. ──
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

# ── Remove stale tags from earlier versions ──
keep_tags = {keep_tags_ruby}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

# ── Scenes ── one consistent iso camera, shared by every scene.
model.layers.each {{ |l| l.visible = true }}
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(0.72, -0.7, 0.5); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

{scenes_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == default_layer || tags.include?(l.name)) }}
  page = model.pages.add(name)
  page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}

model.commit_operation
{{ success: true, model: "IBC Stack",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate the TBS-001 IBC Stack SketchUp model")
    parser.add_argument("--save", action="store_true",
                        help="Write Ruby to src/models/ibc-stack.rb")
    parser.add_argument("--send", action="store_true",
                        help="Send the Ruby to the ACTIVE SketchUp document "
                             "(clears it first - open a NEW doc before sending)")
    args = parser.parse_args()

    ruby = generate_ruby()

    if args.save:
        out = os.path.join(os.path.dirname(__file__), "ibc-stack.rb")
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

    if not args.save and not args.send:
        print(ruby)
