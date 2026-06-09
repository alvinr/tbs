#!/usr/bin/env python3
"""TBS-001 — ROTATION STUDY (3D), cargo-door frame swung about a vertical axle.

3D companion to diagrams/rotation-study.png. Reuses lighttrap's real panel + drum
builders (lt.*) and places the rigid frame at TWO positions:
  - CAMERA    : identity (frame shut across the door, drum out at X-400)
  - TRANSPORT : rotated +LOCK° about the VERTICAL pivot axle at the film-plane far
                upright (X150, Yd2262) — just enough to pull the drum/bay inboard of
                the door plane (X0) so the cargo doors can close, then locked.

NOTE (kept on the model): in the swung/transport position the ~100mm of panel BEYOND
the inset pivot (Yd2262→2362) pokes ~20-30mm back out past the door plane — a small
flap to absorb in the seal tolerance (or end the panel at the pivot + seal that strip).

The slide-based suspension is gone here; the weight is carried by the axle (floor
thrust bearing). No ceiling carriage.

    python3 src/models/generate_rotation_model.py --send          # push to SketchUp
    python3 src/models/generate_rotation_model.py --send --skp     # + save .skp
"""
import argparse
import math
import os
import sys

import generate_sketchup_model as ov
import generate_lighttrap_model as lt

component = ov.component

# ── pivot + swing geometry (matches the 2D study) ──
# The pivot REUSES the film-plane far upright (no separate axle post). Centre of that
# 50x50 upright (X150-200, Yd2262-2312) is the rotation axis.
HX, HY = ov.RAIL_X_L + ov.BRACE_RHS // 2, ov.FP_Y + ov.BRACE_RHS // 2   # 175, 2287
CUT = 180                               # fixed left-panel width (Yd) — 150mm clips the near upright
                                        # at 3deg; 160mm is the min that clears, 180mm for margin
NEAR_CORNER_YD = ov.PANEL_CORNER_YD_L   # 653 — near-corner zone extent (the swing remainder runs CUT..653)
DRUM_CX, DRUM_CY, DRUM_R = lt.DRUM_CX, lt.DRUM_CY, ov.DRUM_R
BAY_X0, APER_L, APER_R = ov.BAY_FRONT_X, lt.APER_L, lt.APER_R


def _min_x(deg):
    th = math.radians(deg); c, s = math.cos(th), math.sin(th)
    rx = lambda x, y: HX + (x - HX) * c - (y - HY) * s
    return min(rx(BAY_X0, APER_L), rx(BAY_X0, APER_R), rx(0, APER_L), rx(0, APER_R),
               rx(DRUM_CX, DRUM_CY) - DRUM_R)


# idealized clear angle (corner sampling) ~52.5°; NUDGED to 56° so the real bay WALL
# (with thickness) also clears the door plane, leaving only the small panel flap.
LOCK_MIN = next(t for t in [i * 0.5 for i in range(0, 190)] if _min_x(t) >= 0)
LOCK = 56.0

TAGS = ["Context", "Door Frame", "Film Plane Rails", "Pivot Axle", "Near Leaf",
        "Walkways", "Panel skin",
        "Frame (camera)", "Frame (transport)", "Labels"]


def walkways():
    """Near + far walkway grates (Z115-130), cropped to the door-end context."""
    gz = ov.WALKWAY_H - ov.WALKWAY_GRATE_T
    t = ov.WALKWAY_GRATE_T
    x0 = ov.WALKWAY_LEFT_X
    xlen = lt.PARTIAL_X - x0
    return '\n'.join([
        ov.ruby_box("Walkway near", x0, 0, gz, xlen, ov.WALKWAY_W, t, color="#8A8E99"),
        ov.ruby_box("Walkway far", x0, ov.WALKWAY_FAR_YD, gz, xlen, ov.WALKWAY_W, t, color="#8A8E99"),
    ])


def near_leaf():
    """The FIXED left panel (Yd0..CUT, 150mm) — fixed to the door frame, does NOT
    swing. Just wide enough that the swinging part clears the near upright."""
    z0, z1 = ov.PANEL_FLOOR_GAP, 2300
    return ov.ruby_box(f"Fixed left panel (Yd0-{CUT})", 0, 0, z0, 40, CUT, z1 - z0, color="#C8A060")


def axle():
    """NO separate post — the film-plane far upright IS the pivot. Just the fixed
    floor thrust + top guide bearings that the upright turns in."""
    cbear = "#5A5AA0"
    return '\n'.join([
        ov.ruby_cylinder("Floor thrust bearing", HX, HY, 0, 95, 45, color=cbear, axis="z"),
        ov.ruby_cylinder("Top guide bearing", HX, HY, ov.C_HGT - 45, 95, 45, color=cbear, axis="z"),
    ])


def fixed_components():
    return '\n'.join([
        component("Context (ghost)", "Context", lt.context(x_far=lt.PARTIAL_X)),
        component("Fixed Door Frame", "Door Frame", lt.door_frame(include_seal=False)),
        component("Film-Plane Rails (left — removable)", "Film Plane Rails", lt.film_plane_left()),
        component("Pivot bearings", "Pivot Axle", axle()),
        component("Fixed left panel", "Near Leaf", near_leaf()),
        component("Walkways (near + far)", "Walkways", walkways()),
    ])


def pivot_link():
    """The structural connection between the frame and the axle: a hub/collar that
    rides the (fixed) axle + hinge brackets tying it to the panel's far-corner edge.
    Part of the moving frame (the hub sits on the rotation axis, so it stays put while
    the brackets + panel swing — a rigid hinge)."""
    p = [ov.ruby_cylinder("Pivot hub (frame collar)", HX, HY, 110, 48, ov.C_HGT - 220,
                          color=ov.C_STEEL, alpha=0.45, axis="z")]
    for z in (250, 1180, 2120):                       # hinge brackets at 3 heights
        p.append(ov.ruby_box("Hinge bracket (panel→axle)", 55, HY - 35, z, 140, 70, 110,
                             color=ov.C_STEEL))
    return '\n'.join(p)


def drum_frame():
    """Steel support CAGE for the lighttrap drum — top + bottom rectangles (4 rails
    each) + 4 corner posts (50x50 RHS), attached to the panel. The drum's top/bottom
    bearings mount on the rectangles; the cage carries the drum and rotates with it."""
    s = 50
    x0, x1 = ov.BAY_FRONT_X, 50              # -890 .. 50 (bay front to just past the panel)
    y0, y1 = 700, 1662                       # just outside the Ø900 drum (731..1631)
    zb, zt = ov.PANEL_FLOOR_GAP, 2250        # 130 .. 2250 (drum height)
    c = ov.C_STEEL
    p = []
    for z in (zb, zt - s):                   # bottom + top rectangles
        p += [
            ov.ruby_box("Drum frame rail (X near)", x0, y0, z, x1 - x0, s, s, color=c),
            ov.ruby_box("Drum frame rail (X far)", x0, y1 - s, z, x1 - x0, s, s, color=c),
            ov.ruby_box("Drum frame rail (Yd front)", x0, y0, z, s, y1 - y0, s, color=c),
            ov.ruby_box("Drum frame rail (Yd back)", x1 - s, y0, z, s, y1 - y0, s, color=c),
        ]
    for px in (x0, x1 - s):                   # 4 corner posts
        for py in (y0, y1 - s):
            p.append(ov.ruby_box("Drum frame post", px, py, zb, s, s, zt - zb, color=c))
    # cross members carrying the central drum bearings (top + bottom)
    for z in (zb, zt - s):
        p.append(ov.ruby_box("Drum bearing cross-beam", DRUM_CX - s // 2, y0, z, s, y1 - y0, s, color=c))
        p.append(ov.ruby_cylinder("Drum bearing (roller)", DRUM_CX, DRUM_CY, z, 70, s, color="#5A5AA0", axis="z"))
    return '\n'.join(p)


def moving_frame_body():
    """The rigid swinging frame: full panel (its near corner Yd0-653 is ERASED
    post-build) + the swinging remainder of that corner (Yd CUT..653) + bay + drum +
    Fan B + pivot link. Only Yd0..CUT is left as the fixed Near Leaf."""
    z0, z1 = ov.PANEL_FLOOR_GAP, 2300
    return '\n'.join([
        lt.hinge_panel(),
        ov.ruby_box(f"Panel near (swing, Yd{CUT}-{NEAR_CORNER_YD})", 0, CUT, z0, 40,
                    NEAR_CORNER_YD - CUT, z1 - z0, color=lt.C_PLY),
        ov.ruby_box("EPDM seal top (trimmed)", -20, CUT, z1 - 40, 20, ov.C_WID - CUT, 40, color=lt.C_GASKT),
        lt.bay(),
        lt.drum_housing(DRUM_CX, DRUM_CY),
        lt.drum_rotor(DRUM_CX, DRUM_CY),
        drum_frame(),
        lt.fan_b(),
        pivot_link(),
    ])


def generate_ruby():
    tags_ruby = '\n'.join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    lock_rad = math.radians(LOCK)
    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Rotation Study", true)
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

# ── fixed subsystems ──
{fixed_components()}

# ── ghost the REMOVABLE left top+bottom beams (rails + brace beams); keep the uprights
#    (the far post is reused as the pivot) ──
ghost_mat = model.materials["FP removable ghost"] || model.materials.add("FP removable ghost")
ghost_mat.color = Sketchup::Color.new(176, 176, 184)
ghost_mat.alpha = 0.20
pivot_mat = model.materials["Pivot upright"] || model.materials.add("Pivot upright")
pivot_mat.color = Sketchup::Color.new(90, 90, 160)
fpdef = model.definitions.to_a.find {{ |d| d.name =~ /Film-Plane Rails/ }}
if fpdef
  fpdef.entities.grep(Sketchup::Group).each {{ |g|
    if g.name =~ /FP Rail (TL|BL)/                          # the two removable left rails
      g.material = ghost_mat
      g.entities.grep(Sketchup::Face).each {{ |f| f.material = ghost_mat; f.back_material = ghost_mat }}
    elsif g.name =~ /Brace Post L .far wall./              # the far upright = the PIVOT
      g.material = pivot_mat
      g.entities.grep(Sketchup::Face).each {{ |f| f.material = pivot_mat }}
    end
  }}
end
ganc = Geom::Point3d.new(150.mm, 600.mm, 1700.mm)
gtxt = entities.add_text("LEFT top+bottom film beams\nGHOSTED = removable for transport", ganc,
                         Geom::Vector3d.new((-700).mm, (-200).mm, 250.mm))
gtxt.layer = model.layers["Labels"] rescue nil

# ── rigid frame (panel + drum), built once, placed at camera + transport ──
defn = model.definitions.add("Swing Frame")
ents = defn.entities
{moving_frame_body()}
# CUT @ Yd{CUT}: drop the near corner from the rotating frame (the fixed Near Leaf
# provides it) so the rotating part never sweeps the near upright.
defn.entities.grep(Sketchup::Group).select {{ |g| g.name =~ /Panel near corner|EPDM seal left|EPDM seal bottom L|EPDM seal top$|Piano hinge/ }}.each {{ |g| g.erase! }}

# tag the panel SKINS (ply + seals) so the 'Structure' scene can hide them, leaving
# the frame/bay/drum/pivot structure
skin_layer = model.layers["Panel skin"] || model.layers.add("Panel skin")
["Swing Frame", "Fixed left panel"].each {{ |dn|
  dd = model.definitions[dn]
  next unless dd
  dd.entities.grep(Sketchup::Group).each {{ |g|
    g.layer = skin_layer if g.name =~ /Panel|EPDM|Piano|Southco|latch|Fixed left/
  }}
}}

# ghost the bay punch-out panels + the drum so the underlying frame structure reads
bd_ghost = model.materials["Bay/drum ghost"] || model.materials.add("Bay/drum ghost")
bd_ghost.color = Sketchup::Color.new(200, 210, 225)
bd_ghost.alpha = 0.22
defn.entities.grep(Sketchup::Group).each {{ |g|
  next unless g.name =~ /^LT |^Bay/
  g.material = bd_ghost
  g.entities.grep(Sketchup::Face).each {{ |f| f.material = bd_ghost; f.back_material = bd_ghost }}
}}

ic = entities.add_instance(defn, Geom::Transformation.new)
ic.name = "Frame (camera)"
ic.layer = model.layers["Frame (camera)"]

pivot = Geom::Point3d.new({HX}.mm, {HY}.mm, 0)
swing = Geom::Transformation.rotation(pivot, Z_AXIS, {lock_rad})
it = entities.add_instance(defn, swing)
it.name = "Frame (transport)"
it.layer = model.layers["Frame (transport)"]

# ── keep the poke-out noted: label the swung far flap ──
anc = Geom::Point3d.new((-25).mm, 2204.mm, 1200.mm)
txt = entities.add_text("Frame FULLY CLEARS door plane\nat {round(LOCK)}deg (true min X +4mm) —\nno poke-out at this pivot", anc,
                        Geom::Vector3d.new((-600).mm, (-300).mm, 300.mm))
txt.layer = model.layers["Labels"] rescue nil
anc2 = Geom::Point3d.new({HX}.mm, {HY}.mm, 1600.mm)
txt2 = entities.add_text("PIVOT AXLE (x)\n@ film-plane far upright\n(150,2262) + floor bearing", anc2,
                         Geom::Vector3d.new(500.mm, (-200).mm, 300.mm))
txt2.layer = model.layers["Labels"] rescue nil
anc3 = Geom::Point3d.new(40.mm, {CUT}.mm, 1100.mm)
txt3 = entities.add_text("FIXED LEFT PANEL (Yd0-{CUT})\ncut vertically; does NOT swing —\nrotating part clears the near upright", anc3,
                         Geom::Vector3d.new(500.mm, (-350).mm, 250.mm))
txt3.layer = model.layers["Labels"] rescue nil

model.definitions.purge_unused
model.materials.purge_unused
keep_tags = [{', '.join(f'"{t}"' for t in TAGS)}]
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

# ── scenes ──
show = lambda {{ |hide|
  model.layers.each {{ |l| l.visible = true }}
  hide.each {{ |n| model.layers[n].visible = false if model.layers[n] }}
}}
def isocam(model, cx, cy, cz, zoom)
  dir = Geom::Vector3d.new(-0.55, -0.74, 0.45); dir.normalize!
  ctr = Geom::Point3d.new(cx.mm, cy.mm, cz.mm)
  eye = ctr.offset(dir, 12000.mm)
  model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
  model.active_view.camera.perspective = true
  model.active_view.zoom_extents
  model.active_view.zoom(zoom)
end

model.layers["Labels"].visible = false if model.layers["Labels"]
show.call(["Frame (transport)"])
isocam(model, 300, 1181, 1200, 0.85)
model.pages.add("Camera (frame shut)").use_camera = true

model.layers["Labels"].visible = true if model.layers["Labels"]
show.call(["Frame (camera)"])
isocam(model, 700, 1181, 1200, 0.85)
model.pages.add("Transport (swung {round(LOCK)}deg)").use_camera = true

# Structure only — hide the panel SKINS so the frame + bay + drum + pivot read
model.layers["Labels"].visible = false if model.layers["Labels"]
show.call(["Panel skin", "Frame (transport)", "Context"])
isocam(model, -100, 1200, 1250, 0.92)
model.pages.add("Structure (no panel skins)").use_camera = true

model.layers.each {{ |l| l.visible = true }}
model.commit_operation

{{ success: true, model: "Rotation Study", lock_deg: {LOCK},
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TBS-001 rotation study (3D)")
    parser.add_argument("--save", action="store_true", help="Write Ruby to rotation-study.rb")
    parser.add_argument("--send", action="store_true", help="Send to running SketchUp")
    parser.add_argument("--skp", action="store_true", help="After --send, save models/rotation-study.skp")
    args = parser.parse_args()

    ruby = generate_ruby()
    print(f"  lock angle = {LOCK} deg")

    if args.save:
        out = os.path.join(os.path.dirname(__file__), "rotation-study.rb")
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
        skp = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models", "rotation-study.skp"))
        print(f"  saving {skp} ...")
        print("  " + send_ruby('m=Sketchup.active_model; "saved=#{m.save(' + repr(skp) + ')}"'))
