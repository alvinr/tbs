#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Generate the TBS-001 IBC Stack SketchUp model (logical model: ibc-stack).

Focused on the IBC tote stack, its steel support frame, and the plumbing +
plumbing panel. REUSES the helpers and component builders from the Overview
generator (generate_sketchup_model.py) — same component/tag/scene structure,
shared iso camera, and material-sharing-by-color. Subsystem tags grouped into scenes:
    1. IBC Tanks            (the four totes)
    2. IBC Frame            (the steel stacking frame/rack + the 2 right-walkway
                             cantilever arms that attach to the corridor uprights, rev12)
    3. Plumbing & Panel     (plumbing panel + pumps/filters + water plumbing + hookups)
    4. Combined             (all subsystems)

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

TAGS = ["Context", "IBC Tanks", "IBC Frame", "Plumbing & Panel",
        "Walkway Cantilever", "Labels"]


# ── "Labeled" scene callouts (project rule: every .skp gets a Labeled scene) ──
# (instance name, text, leader Δx,Δy,Δz mm). Δy pulls toward the viewer (−Y).
IBC_LABELS = [
    ("IBC Frame", "IBC FRAME\n(restraint front portal)", -250, 750, 650),
    ("Walkway Cantilever Arms", "RIGHT-WALKWAY\nCANTILEVER ARMS\n(off the IBC corridor\nuprights — rev12)", -350, -900, 700),
]
# Point-anchored callouts on specific geometry (totes, drain ports, panel kit).
IBC_POINT_LABELS = [
    # ── Near-column totes — container side (front / door end) ──
    (5284,  538,  579, "BROWN IBC\n(developer)",     -1550,  -900, -500),
    (5284,  538, 1589, "BLUE IBC #1\n(fresh water)", -1550,  -900,  550),
    # ── Far-column totes — pulled out the OTHER (sealed-end) side so they don't
    #    pile onto the near column ──
    (5284, 1824,  579, "WASTE IBC",                   1550,  -250,  250),
    (5284, 1824, 1589, "BLUE IBC #2\n(fresh water)",  1550,  -250,  400),
    # ── Tray sump pickup + Blue spray-bar feed (container side, low front) ──
    (4550,  155,   20, "SUMP PICKUP\n(tray drain)",   -650,  -900,  950),
    (4649,   12,   40, "TO SPRAY BAR",               -1250,  -650, -150),
    # ── Exterior bulkhead ports on the sealed end wall (X = C_LEN) ──
    (5893, 1181, 2250, "X1 (fresh fill)",            1007, -400,  450),
    (5893, 1181,  400, "X3 (Brown drain-out)",       1007, -500,  -50),
    (5893, 1181,  200, "X4 (Waste drain-out)",       1007, -500, -100),
    # NB: the wet-end panel-equipment label anchors (P-01..P-05, F1-F3, ACC-01) were
    # removed with the corridor/pinhole-panel rewire (2026-07-01) — their old positions
    # no longer match cp.equipment()/pw.kit(). Re-anchor to the current part centers if
    # panel-equipment callouts are wanted again.
]


def ibc_labels():
    """Ruby that adds an in-model text callout (with leader) for each major part on
    the 'Labels' tag — instance-anchored at bounds top-centre + point-anchored."""
    rows = []
    for name, text, dx, dy, dz in IBC_LABELS:
        rows.append(
            f'inst = entities.grep(Sketchup::ComponentInstance).find {{ |i| i.name == "{name}" }}\n'
            f'if inst\n'
            f'  bb = inst.bounds\n'
            f'  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)\n'
            f'  txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'  txt.layer = model.layers["Labels"] rescue nil\n'
            f'end')
    for x, y, z, text, dx, dy, dz in IBC_POINT_LABELS:
        rows.append(
            f'anc = Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    return '\n'.join(rows)


def context():
    """Low-alpha stub of the container around the IBC end zone (X≈4300–5893):
    floor + both side walls only — so the stack, frame and plumbing read in place
    without modeling the whole container (mirrors the lighttrap ghost context).
    The CEILING (roof) and the sealed END WALL are omitted: they boxed the model in
    and blocked a smooth Sketchfab orbit (Alvin 2026-08-17); the fill/drain ports
    (X1/X3/X4) are their own geometry and still read at X=C_LEN."""
    x0 = 4300
    xlen = ov.C_LEN - x0
    t = ov.WALL_T
    return '\n'.join([
        ov.ruby_box("Floor (context)", x0, 0, -t, xlen, ov.C_WID, t,
                    color=ov.C_SHELL, alpha=0.25),
        ov.ruby_box("Side Wall near (context)", x0, -t, 0, xlen, t, ov.C_HGT,
                    color=ov.C_SHELL, alpha=0.16),
        ov.ruby_box("Side Wall far (context)", x0, ov.C_WID, 0, xlen, t, ov.C_HGT,
                    color=ov.C_SHELL, alpha=0.16),
    ])


def spray_wall_trunk():
    """The blue spray-bar supply continuing LEFT along the pinhole wall (Yd≈0) from the
    right film rail toward the spray bar — drawn to the IBC-view edge (X=4300) so the
    feed doesn't appear to stop at the rail. (In the overview this run is the spray-bar
    supply trunk; here it's added only for the IBC-end view.)"""
    fz = ov.SPRAY_BAR_FEED_Z
    return ov.ruby_pipe("Blue Supply Trunk (along pinhole wall)",
                        (ov.RAIL_X_R, 12, fz), (4300, 12, fz),
                        ov.PUMP_PIPE_OD / 2, color=ov.C_BLUE)


def generate_ruby():
    """Build the Ruby script for the IBC Stack model, reusing Overview parts."""
    # Current water-system builders (water.skp source) — corridor + pinhole-wall panels
    import generate_corridor_water_panel as cp
    import generate_pinhole_water_panel as pw
    comps = [
        ov.component("Container (ghost)", "Context", context()),
        ov.component("IBC Tanks", "IBC Tanks", ov.ibc_stack(alpha=0.25)),
        ov.component("Corridor Frame (deep box)", "IBC Frame", cp.frame()),
        ov.component("IBC Tote Restraint", "IBC Frame", cp.tote_restraint()),
        ov.component("Corridor Rear Panel", "Plumbing & Panel", cp.rear_panel()),
        ov.component("Corridor Equipment", "Plumbing & Panel", cp.equipment(sump_on_skid=True)),
        ov.component("Wall backing (ply)", "Plumbing & Panel", pw.backing()),
        ov.component("Pinhole-Wall Kit", "Plumbing & Panel", pw.kit(p02_on_corridor=True)),
        ov.component("Skid row (P-04 · SV-02 · DV-02)", "Plumbing & Panel", pw.skid_row()),
        ov.component("Skid plumbing", "Plumbing & Panel", pw.skid_plumbing()),
        # NB: "Pinhole-Wall Equipment" (ov.electrical() — EP + external power panel + batteries)
        #     removed from this model — electrical is not of interest in the IBC/plumbing view.
        ov.component("Corridor Plumbing", "Plumbing & Panel", cp.plumbing(sump_on_skid=True)),
        ov.component("Corridor Drains + X-ports", "Plumbing & Panel", cp.drains_ports(sump_on_skid=True)),
        ov.component("TAP-01 + Spray Supply", "Plumbing & Panel", pw.tap01_supply()),
        # NB: "Ribbon Support Cross-beams" (cp.ribbon_supports() — the 4 welded under-grate
        #     cross-beams) removed — not of interest in this model.
        ov.component("Walkway Cantilever Arms", "Walkway Cantilever",
                     '\n'.join(ov.ibc_cantilever_arms())),
    ]
    body = '\n'.join(comps)

    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    # Focused subsystems, a combined view, then a fully-labeled view (per rule).
    comp_tags = [t for t in TAGS if t != "Labels"]
    scenes = [
        ("Overview", comp_tags),  # combined view of all subsystems — listed first
        ("IBC Tanks", ["IBC Tanks"]),
        ("IBC Frame", ["IBC Frame", "Walkway Cantilever"]),  # frame + the attached walkway cantilever arms
        ("Plumbing & Panel", ["Plumbing & Panel"]),
        ("Labeled", TAGS),  # all components + the Labels tag
    ]
    scenes_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags))
        for n, tags in scenes) + ']'

    sf_meta = ov.sketchfab_meta_ruby(
        "TBS-001 IBC Model",
        "Details of the IBC stack, frame and plumbing panel.",
        ov.model_uid("ibc-stack"), "sketchup")

    return f'''# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
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

# ── In-model labels (on the 'Labels' tag; visible only in the "Labeled" scene) ──
{ibc_labels()}

{ov.license_note()}

model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier versions ──
keep_tags = {keep_tags_ruby}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

# ── Scenes ── opening camera looks at the FILTER SKID PANEL (pinhole wall) from INSIDE the container.
# Frame on geometry only — hide the Labels tag so Text bounds don't skew extents.
model.layers.each {{ |l| l.visible = (l.name != "Labels") }}
# Frame the CONTAINER/IBC mass DIRECTLY — not model.bounds + zoom_extents. The TAP-01/spray-supply
# run + the skid plumbing reach far toward the pinhole wall, so the full extent is much wider than the
# dense mass; zoom_extents then centers that wide extent and pushes the container off to the side.
# Aiming at the Container-ghost bounds with a fixed fit keeps the container centered (the thin supply
# run just extends into the margin).
cont = model.entities.grep(Sketchup::ComponentInstance).find {{ |i| i.name == "Container (ghost)" }}
fb = cont ? cont.bounds : model.bounds
ctr = fb.center
dir = Geom::Vector3d.new(0.5, 0.72, 0.45); dir.normalize!   # corner iso, eye on the IBC (+X) side
eye = ctr.offset(dir, fb.diagonal * 1.45)
cam = Sketchup::Camera.new(eye, ctr, Z_AXIS); cam.fov = 38
model.active_view.camera = cam

{scenes_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }}
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
