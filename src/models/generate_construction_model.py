#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Generate the TBS-001 phased CONSTRUCTION model (logical model: construction).

Validates the BUILD ORDER (see construction-report.md). REUSES the Overview component
builders (generate_sketchup_model.py + corridor/pinhole water panels + walkway model) —
each build STEP is drawn on its own tag, and one SCENE per PHASE shows the model built up
CUMULATIVELY through that phase. Stepping the scenes 1→5 walks the install; toggling a
phase's step-tags on in order shows each step drop in.

v1 granularity note: several Overview builders draw more than one report-step's worth of
geometry and don't (yet) take a per-wall/subset argument (e.g. `ibc_stack()` draws all four
totes; `walkway_brackets()` draws near+far together; `film_plane_mechanism()` draws the rails
AND the moving plane). Where that happens the affected report-steps are GROUPED onto one
step-tag (noted in STEPS). Finer per-step splitting + the click-to-build Dynamic Component are
the next iteration.

Phase 2 (re-measure) adds no geometry — its scene shows the Phase-1 state (what you measure).

Usage:
    python3 src/models/generate_construction_model.py --save         # write construction.rb
    python3 src/models/generate_construction_model.py --save --send  # + send to the ACTIVE doc

NOTE: --send clears the ACTIVE SketchUp document. Open a NEW blank doc before sending, then
save the result as models/construction.skp.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov            # Overview helpers + component builders
import generate_corridor_water_panel as cp      # IBC corridor frame + plumbing
import generate_pinhole_water_panel as pw        # pinhole-wall kit + spray supply
import generate_walkway_model as wm              # left floor-leg cantilevers


def _join(*parts):
    return '\n'.join(p if isinstance(p, str) else '\n'.join(p) for p in parts)


# ── Build steps, in install order ──────────────────────────────────────────────
# (phase, step_id, tag, label, body-thunk). tag == the step's own layer; the scene for
# phase N shows every tag whose phase <= N (cumulative). Report §4–§8 step ids in [].
STEPS = [
    # ── Phase 1 — Geometry set-out ──
    (1, "1.1", "P1 Near IBCs",     "IBC totes — pinhole wall (near column)",   # [1.1]
        lambda: ov.ibc_stack(alpha=0.85, cols="near")),
    (1, "1.2", "P1 IBC Frame",     "IBC restraint frame (deep box)",           # [1.2]
        lambda: _join(cp.frame(), cp.tote_restraint())),
    (1, "1.3", "P1 IBC Plumbing",  "IBC corridor plumbing + drains",           # [1.3 (+ finalize plumbing grouped here)]
        lambda: _join(cp.plumbing(), cp.drains_ports())),
    (1, "1.4", "P1 Fan A",         "Fan A (exhaust) + its Cct-A electrical — pinhole wall",  # NEW — before the far IBCs bury it
        lambda: _join(ov.fans(which="A"), ov.fan_wiring(which="A"))),
    (1, "1.5", "P1 Corridor Wiring", "Corridor pump wiring (Cct C) to the pinhole wall",     # NEW — before the far IBCs block the wall
        lambda: pw.panel_power(include_switch=True)),
    (1, "1.6", "P1 Far IBCs",      "IBC totes — far wall (far column)",        # was 1.4 — second-to-last
        lambda: ov.ibc_stack(alpha=0.85, cols="far")),
    (1, "1.7", "P1 Hinge Panel",   "Hinge panel (excl. light-trap drum)",      # was 1.5 — last
        lambda: _join(ov.light_trap_frame(), ov.light_seal(), ov.panel_pivot())),

    # ── Phase 3 — Hard install (Phase 2 = re-measure, no geometry) ──
    (3, "3.1", "P3 Far+Right Cantilevers", "Cantilevers — far wall + right-end rectangle",   # [3.1]
        lambda: _join(ov.walkway_brackets(which="far"),
                      ov.right_walkway_cantilever(include_combined=True, include_grate=False))),
    (3, "3.2", "P3 Processing Tray",   "Processing tray + spray bar",       # [3.2]
        lambda: _join(ov.processing_tray(), ov.spray_bar())),
    (3, "3.3", "P3 Near Cantilevers",  "Cantilevers — near wall",           # [3.3]
        lambda: ov.walkway_brackets(which="near")),
    (3, "3.4", "P3 Pinhole Plumbing",  "Extend plumbing to the pinhole-wall panel",  # [3.4]
        lambda: pw.tap01_supply()),
    (3, "3.5", "P3 Filter Skid",       "Pinhole filter skid (F-1..F-3 + pumps + ACC)",  # [3.5]
        lambda: pw.kit()),
    (3, "3.6", "P3 Film-Plane Beams",  "Film-plane beams (corner rails + wall-seat saddles)",  # [3.6]
        lambda: ov.film_plane_mechanism(part="beams")),
    (3, "3.7", "P3 Left Cantilevers",  "Left-walkway floor-leg cantilevers",  # [3.7]
        lambda: '\n'.join(wm.left_floor_cantilevers())),
    (3, "3.8", "P3 Walkway",           "Walkway grating (all sections)",     # [3.8] — grates only; supports are 3.1/3.3/3.7
        lambda: ov.walkways(include_right=True, include_right_hangers=False, grates_only=True)),

    # ── Phase 4 — Electrical ──
    (4, "4.1", "P4 Electrical Panel",  "Interior electrical panel + batteries",  # [4.1]
        lambda: ov.electrical()),
    (4, "4.2", "P4 External Panel",    "External power panel (PV + E-stop)",     # [4.2]
        lambda: ov.ep_external_wiring()),
    (4, "4.3", "P4 Lights",            "Lights",                                 # [4.3]
        lambda: ov.lighting_wiring()),
    (4, "4.4", "P4 Wiring + Fit-out",  "Fan B + its Cct-B wiring + shelf",  # [4.4] (Fan A + Cct-A + Cct-C corridor wiring moved to Phase 1; external cooler/solar excluded)
        lambda: _join(ov.fans(which="B"), ov.fan_wiring(which="B"), ov.shelf())),

    # ── Phase 5 — Photo system ──
    (5, "5.1", "P5 Film Plane",        "Film plane + carriages (screen + frame)",  # [5.1] — beams already in 3.6
        lambda: ov.film_plane_mechanism(part="plane")),
    (5, "5.2", "P5 Pinhole",           "Pinhole mechanism",                       # [5.2]
        lambda: ov.pinhole_assembly()),
    (5, "5.3", "P5 Light Trap",        "Light-trap drum + bay",                   # [5.3]
        lambda: _join(ov.light_trap_drum(), ov.light_trap_bay())),
]

PHASE_NAMES = {
    1: "Phase 1 — Geometry Set-Out",
    2: "Phase 2 — Re-measure",
    3: "Phase 3 — Hard Install",
    4: "Phase 4 — Electrical",
    5: "Phase 5 — Photo System",
}

SF_TITLE = "TBS-001 Construction Sequence"
SF_DESC = ("The TBS-001 build order — one scene per install phase (geometry set-out → IBC "
           "plumbing → hard install → electrical → photo system), each phase shown built up "
           "cumulatively, to validate the assembly sequence.")
SF_ID = "dcc54fb3d02e46c3ab070dd49adc5d1e"   # stable Sketchfab UID — re-uploads REPLACE this model
SF_TAGS = "sketchup"


def context():
    """Minimal container datum so the build reads in place but stays easy to orbit — just the
    FLOOR. The roof, both side walls, and the (right) sealed end wall are omitted so nothing
    encloses the model or blocks the orbit."""
    t = ov.WALL_T
    return ov.ruby_box("Floor (context)", 0, 0, -t, ov.C_LEN, ov.C_WID, t, color=ov.C_SHELL, alpha=0.18)


def _phase_dc_ruby(pnum, p_steps):
    """Ruby for a phase's CLICK-TO-BUILD Dynamic Component: a parent 'Phase N Build' DC whose
    `onclick` cycles a `step` counter (ANIMATE 1→N→1); each sub-step is a child instance HIDDEN
    until `step` reaches its index, so clicking the assembly reveals the steps in install order
    (then wraps back to the first). `step` DEFAULTS TO N (fully built), so every scene shows all
    prior + current phases complete — this is what makes a later phase "start at the end point of"
    the phases before it. To replay a phase's build, click its DC: the first click resets it to
    step 1 (its first sub-step) while prior phases stay complete, then each click adds the next.
    Since every sub-step is nested inside this parent onclick DC, clicking anywhere on the shown
    assembly advances it. Returns (ruby, parent_instance_var_name)."""
    da = "dynamic_attributes"
    n = len(p_steps)
    ref = f"Phase{pnum}Build"                       # ancestor-ref name used in child formulas
    var = f"p{pnum}_inst"
    L = [f'# ═══ Phase {pnum} Build — CLICK-TO-BUILD Dynamic Component ═══',
         f'p{pnum}_defn = model.definitions.add("Phase {pnum} Build")']
    for i, (sid, tag, label, body) in enumerate(p_steps, start=1):
        cdef = f'P{pnum}Step{sid.replace(".", "_")}'
        L += [f'child = model.definitions.add("{cdef}")',
              'ents = child.entities',
              body(),
              f'ci = p{pnum}_defn.entities.add_instance(child, Geom::Transformation.new)',
              f'ci.name = "Step {sid} — {label}"',
              f'ci.layer = model.layers["{tag}"]',
              f'ci.set_attribute("{da}", "_name", "{cdef}")',
              f'ci.set_attribute("{da}", "hidden", 1.0)',
              f'ci.set_attribute("{da}", "_hidden_formula", "{ref}!step<{i}")']
    anim = ",".join(str(k) for k in range(1, n + 1))   # 1,2,...,N (never 0 → always ≥1 sub-step drawn)
    L += [f'{var} = entities.add_instance(p{pnum}_defn, Geom::Transformation.new)',
          f'{var}.name = "Phase {pnum} Build"',
          f'{var}.set_attribute("{da}", "_name", "{ref}")',
          f'{var}.set_attribute("{da}", "step", {float(n)})',   # default = fully built
          f'{var}.set_attribute("{da}", "_step_access", "VIEW")',
          f'{var}.set_attribute("{da}", "_step_label", "Build step")',
          f'''{var}.set_attribute("{da}", "onclick", 'ANIMATE("step",{anim})')''',
          f'{var}.set_attribute("{da}", "_onclick_access", "NONE")']
    return '\n'.join(L), var


DC_PHASES = (1, 3)          # phases rendered as click-to-build Dynamic Components
SCENE_PHASES = (1, 3, 4, 5)  # Phase 2 (re-measure) has no geometry → no scene


def generate_ruby():
    step_tags = [tag for (_p, _s, tag, _l, _b) in STEPS]
    # Each DC phase also gets a STATIC (flat, non-clickable) copy on its own tag, shown as built
    # context in LATER scenes — so clicking a later phase can only ever hit that later phase's DC.
    static_tag = {pn: f"P{pn}-static" for pn in DC_PHASES}
    TAGS = ["Context"] + step_tags + [static_tag[pn] for pn in DC_PHASES]

    comps = [ov.component("Container (ghost)", "Context", context())]
    dc_blocks, dc_vars, dc_info = [], [], []
    for pn in SCENE_PHASES:
        p_steps = [(sid, tag, label, body) for (p, sid, tag, label, body) in STEPS if p == pn]
        if pn in DC_PHASES:
            block, var = _phase_dc_ruby(pn, p_steps)
            dc_blocks.append(block)
            dc_vars.append(var)
            dc_info.append((var, len(p_steps)))
            # static built copy (non-clickable) for use as prior context in later scenes
            for (sid, tag, label, body) in p_steps:
                comps.append(ov.component(f"[built] Step {sid} — {label}", static_tag[pn], body()))
        else:
            for (sid, tag, label, body) in p_steps:
                comps.append(ov.component(f"Step {sid} — {label}", tag, body()))
    body_ruby = '\n'.join(comps) + '\n' + '\n'.join(dc_blocks)
    dc_redraw = ''.join(f'    cls.redraw_with_undo({v}) rescue nil\n' for v in dc_vars)
    # The ANIMATE-onclick redraw above resets the first DC's `step` to its first value; re-assert
    # the fully-built default AFTER the redraw (step = max, every sub-step shown). A live Interact
    # click still re-evaluates the hidden formulas, so click-to-replay is unaffected.
    dc_fixup = ''.join(
        f'{v}.set_attribute("dynamic_attributes", "step", {float(n)})\n'
        f'{v}.definition.entities.grep(Sketchup::ComponentInstance).each {{ |c| '
        f'c.set_attribute("dynamic_attributes", "hidden", 0.0); c.visible = true }}\n'
        for (v, n) in dc_info)

    tags_ruby = '\n'.join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    # Scenes: for phase N show Context + the CURRENT phase's clickable geometry + every PRIOR phase
    # as built context (DC phases → their static tag; flat phases → their step tags).
    def scene_tags(N):
        vis = ["Context"]
        for pk in SCENE_PHASES:
            if pk > N:
                continue
            ptags = [tag for (p, _s, tag, _l, _b) in STEPS if p == pk]
            if pk == N:
                vis += ptags                       # current phase: clickable DC (or flat) tags
            elif pk in DC_PHASES:
                vis.append(static_tag[pk])         # prior DC phase: static built copy
            else:
                vis += ptags                       # prior flat phase: its step tags
        return vis
    scenes = [(PHASE_NAMES[pn], scene_tags(pn)) for pn in SCENE_PHASES]
    scenes_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags)) for n, tags in scenes) + ']'

    sf_meta = ov.sketchfab_meta_ruby(SF_TITLE, SF_DESC, SF_ID, SF_TAGS, force_name=True)

    return f'''# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("TBS-001 Construction Sequence", true)
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

{sf_meta}
# ── Tags (one per build step) ──
{tags_ruby}

# ── Steps (each on its own tag, drawn in install order) ──
{body_ruby}

# ── Drop the external evap cooler UNIT + its cord (ov.electrical() draws them) — not part of
#    the container construction. The panel provisions (Fuse E, Cct-E GFCI outlet) stay.
model.definitions.each {{ |d| d.entities.grep(Sketchup::Group).each {{ |g| g.erase! if g.valid? && g.name =~ /Evap Cooler|cooler cord/ }} }}

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

# ── Camera: one shared iso, framed on the whole container ──
model.layers.each {{ |l| l.visible = true }}
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(0.72, -0.7, 0.5); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

# ── Cumulative phase scenes ──
{scenes_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == default_layer || tags.include?(l.name)) }}
  page = model.pages.add(name)
  page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}

model.commit_operation

# Register the phase click-to-build DCs with the Dynamic Components engine so the Interact tool
# drives them (skipped silently if the DC extension isn't loaded).
if defined?($dc_observers) && $dc_observers.respond_to?(:get_latest_class)
  cls = $dc_observers.get_latest_class
  if cls
{dc_redraw}  end
end

# Re-assert the fully-built default (the ANIMATE redraw above resets the first DC's step).
{dc_fixup}
{{ success: true, model: "Construction Sequence",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the TBS-001 phased construction model")
    parser.add_argument("--save", action="store_true", help="Write Ruby to src/models/construction.rb")
    parser.add_argument("--send", action="store_true", help="Send to the ACTIVE SketchUp doc (clears it first — open a NEW doc)")
    args = parser.parse_args()

    ruby = generate_ruby()

    if args.save:
        out = os.path.join(os.path.dirname(__file__), "construction.rb")
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
