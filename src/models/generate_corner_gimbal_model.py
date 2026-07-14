#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Generate the film-plane CORNER / WHOLE-MECHANISM SketchUp model (film-plane-redesign branch).

One full VERTICAL EDGE of the film plane so the top/bottom rail story is visible:

    floor rail (Y) → BOTTOM corner (bears — COMPRESSION) → ghost film plane
    → TOP corner (hangs — TENSION) → ceiling rail (Y)

SLIDE-AND-CLAMP mechanism (no screws, no handwheels — a pinhole has infinite depth of field, so
this is scene/perspective control, not focus; you push each corner into position and lock it):

  • DEPTH (Y): long friction slide (~2.2 m; sets focus + the swing/tilt depth arc) + cam clamp.
  • VERTICAL (Z): friction slide (~324 mm; sets the tilt vertical component + rise) + cam clamp.
  • HORIZONTAL (X): floating slide (gravity-neutral; absorbs the swing arc; free).
  • JOINT: single U-JOINT (Ruland US12-6-6-SS; through-axis Y → tilt pin = X, swing pin = Z;
    twist locked) → stub mount → film-frame corner.

Friction slides (igus DryLin style) hold the corner when released; the cam clamp locks it hard
for the shot + transport. Nominal stack ≈ 150 mm/corner → FP_H ≈ 2088 mm. ±40° tilt / ±28° swing.

REUSES generate_sketchup_model.py helpers. Open a NEW blank SketchUp doc before --send.

Usage:
    /usr/bin/python3 src/models/generate_corner_gimbal_model.py --save [--send]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov          # ruby helpers + component()

TAGS = ["Bottom Corner", "Top Corner", "Film Plane", "Swing Plan", "Labels"]

C_STEEL = "#B0B0B8"; C_ALUM = "#C8D8E8"; C_XSL = "#B8C8D8"; C_PIN = "#B07010"
C_CROSS = "#8A8A92"; C_FRAME = "#2A6B2A"; C_PANEL = "#1F3B66"; C_CAR = "#C04010"; C_CLAMP = "#3A3A40"

CH = 2388          # container interior height (mm) — local
STACK = 150        # nominal mechanism stack per corner (mm)
FP_H = CH - 2 * STACK   # ≈ 2088


def corner(z0, s, tag):
    """One corner's slide-and-clamp stack. z0 = rail-mount Z; s = +1 up (bottom), -1 down (top).
    Build-heights (a,b) are distances from the rail mount along the build direction."""
    P = []

    def bb(name, hx, y0, dy, a, b, color, alpha=1.0):        # symmetric box on X=0
        zmin = z0 + a if s > 0 else z0 - b
        P.append(ov.ruby_box(f"{name} {tag}", -hx, y0, zmin, 2 * hx, dy, b - a, color=color, alpha=alpha))

    def rbx(name, x, w, y0, dy, a, b, color):                # explicit-X box
        zmin = z0 + a if s > 0 else z0 - b
        P.append(ov.ruby_box(f"{name} {tag}", x, y0, zmin, w, dy, b - a, color=color))

    def cz(name, cx, cy, a, b, r, color):                    # cylinder along Z
        base = z0 + a if s > 0 else z0 - b
        P.append(ov.ruby_cylinder(f"{name} {tag}", cx, cy, base, r, b - a, color=color, axis="z"))

    def cxx(name, x0, cy, h, length, r, color):              # cylinder along X at build-height h
        z = z0 + h if s > 0 else z0 - h
        P.append(ov.ruby_cylinder(f"{name} {tag}", x0, cy, z, r, length, color=color, axis="x"))

    def cyY(name, cx, y0, dy, h, r, color):                  # cylinder along Y at build-height h (clamp lever)
        z = z0 + h if s > 0 else z0 - h
        P.append(ov.ruby_cylinder(f"{name} {tag}", cx, y0, z, r, dy, color=color, axis="y"))

    # ── DEPTH friction slide (Y): rail + CAPTIVE carriage that WRAPS it (grip tabs) + cam clamp ──
    bb("Depth slide rail Y (~2.2m)", 10, -1000, 2000, 2, 16, C_STEEL)         # rail core
    bb("Depth carriage body", 22, -30, 60, 16, 32, C_CAR)                    # over the rail
    rbx("Depth grip tab L", -20, 8, -30, 60, 0, 17, C_CAR)                   # hugs rail left  → captive
    rbx("Depth grip tab R", 12, 8, -30, 60, 0, 17, C_CAR)                    # hugs rail right → captive
    rbx("Depth cam clamp body", 22, 14, 30, 14, 20, 34, C_CLAMP)            # clamp body on carriage
    cyY("Depth clamp lever", 28, 44, 58, 27, 4, C_CLAMP)                     # throw-to-lock lever

    # ── VERTICAL friction slide (Z): rail + CAPTIVE carriage that WRAPS it (grip tabs) + cam clamp ──
    rbx("Vertical slide rail Z", -34, 10, -6, 12, 20, 350, C_STEEL)          # rail core (x-34..-24, y-6..6)
    rbx("Vertical carriage body", -44, 26, -12, 24, 150, 182, C_CAR)        # over the rail
    rbx("Vertical grip tab F", -44, 26, -15, 9, 152, 180, C_CAR)            # hugs rail front → captive
    rbx("Vertical grip tab B", -44, 26, 6, 9, 152, 180, C_CAR)             # hugs rail back  → captive
    rbx("Vertical cam clamp body", -47, 14, 26, 14, 158, 172, C_CLAMP)     # clamp body on carriage
    cyY("Vertical clamp lever", -33, 40, 58, 165, 4, C_CLAMP)              # throw-to-lock lever
    rbx("Carriage bracket to X-slide", -30, 34, -8, 16, 154, 166, C_ALUM)

    # ── HORIZONTAL X slide (absorbs SWING foreshortening; gravity-neutral) — the swing counterpart of the
    #    vertical Z slide: rail + captive carriage + cam clamp (floats free, then clamps for shot + transport) ──
    rbx("Horizontal X slide rail", -70, 140, -6, 12, 156, 166, C_STEEL)      # rail runs in X (~260 mm travel)
    rbx("Horizontal X carriage", -20, 40, -11, 22, 158, 178, C_XSL)         # captive; carries the U-joint
    rbx("X grip tab F", -20, 40, -13, 7, 160, 172, C_XSL)                   # hugs rail front → captive
    rbx("X grip tab B", -20, 40, 6, 7, 160, 172, C_XSL)                    # hugs rail back  → captive
    rbx("X cam clamp body", 22, 14, 34, 14, 160, 174, C_CLAMP)
    cyY("X clamp lever", 26, 48, 54, 167, 4, C_CLAMP)

    # ── single U-JOINT (through-axis Y): cross + tilt pin (X) + swing pin (Z) + two yokes ──
    bb("U-joint cross", 10, -10, 20, 172, 192, C_CROSS)
    cxx("Tilt pin X", -26, -4, 182, 52, 5, C_PIN)
    cz("Swing pin Z", 0, 4, 168, 198, 5, C_PIN)
    rbx("Out yoke ear L", -30, 8, -10, 20, 172, 192, C_ALUM)
    rbx("Out yoke ear R", 22, 8, -10, 20, 172, 192, C_ALUM)
    rbx("Out yoke web", -30, 60, 10, 8, 174, 190, C_ALUM)
    rbx("Out yoke stub", -6, 12, 17, 30, 176, 188, C_ALUM)
    rbx("In yoke ear Lo", -9, 18, -9, 18, 164, 176, C_XSL)
    rbx("In yoke ear Hi", -9, 18, -9, 18, 188, 200, C_XSL)
    rbx("In yoke web", -8, 16, -17, 8, 164, 200, C_XSL)
    rbx("Stub-to-frame plate", -10, 70, 40, 10, 160, 220, C_FRAME)
    return "\n".join(P)


def film_plane():
    zb = STACK
    zt = CH - STACK
    return "\n".join([
        ov.ruby_box("Frame angle web", -5, 50, zb, 5, 50, zt - zb, color=C_FRAME),
        ov.ruby_box("Frame angle flange", -5, 50, zb, 50, 5, zt - zb, color=C_FRAME),
        ov.ruby_box("Film plane (ghost)", 0, 53, zb, 620, 4, zt - zb, color=C_PANEL, alpha=0.16),
    ])


def labels():
    L = []
    def txt(s, x, y, z, vx, vy, vz):
        L.append(f'''
tt = entities.add_text("{s}", Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)}), Geom::Vector3d.new({ov.mm(vx)}, {ov.mm(vy)}, {ov.mm(vz)}))
tt.layer = model.layers["Labels"] rescue nil''')
    txt("CEILING rail — TOP corners HANG = TENSION", 0, -170, CH, 40, -60, 30)
    txt("FLOOR rail — BOTTOM corners BEAR = COMPRESSION", 0, -170, 0, 40, -60, -30)
    txt("NO screws / handwheels — PUSH to slide, CAM-CLAMP to lock", 0, 300, CH / 2 + 300, 55, 50, 20)
    txt("Single U-joint (Ruland US12-6-6-SS) — tilt X + swing Z", -30, -4, STACK + 50, -60, -40, 10)
    txt("Depth (Y) slide — produces TILT + SWING (+ focus)", 22, 400, STACK + 6, 55, 45, 0)
    txt("Vertical (Z) slide — absorbs TILT foreshortening", -36, 40, 260, -60, -45, 0)
    txt("Horizontal (X) slide — absorbs SWING foreshortening", 24, 40, STACK + 30, 55, 45, 0)
    txt(f"Film plane 4499 x {FP_H} (mechanism ~{STACK} top + bottom)", 300, 53, CH / 2, 60, 45, 0)
    return "\n".join(L)


# ── Top-down PLAN view of SWING (the horizontal twin of the vertical-edge tilt view) ──
# Real X-Y layout: pinhole at (X=2399, Y=0); film width X=150..4649 at depth Y=2262. Swing = rotate the
# panel 20° about the vertical centre axis → left end moves FORWARD in depth + toward centre in X; right
# end moves BACK + toward centre. The depth rails stay at fixed X (150 / 4649); the DEPTH slide drives the
# corner forward/back, and the X SLIDE absorbs the sideways foreshortening.
PL_FPY = 2262       # film depth
PL_L = (286, 1493)  # left end swung (20°): X 150→286 (toward centre), Y 2262→1493 (fwd)
PL_R = (4512, 3031)  # right end swung: X 4649→4512, Y 2262→3031 (back)


def swing_plan():
    P = []

    def pbox(name, x, y, w, d, color, alpha=None, h=40, z=0):
        P.append(ov.ruby_box(f"{name} [plan]", x, y, z, w, d, h, color=color, alpha=alpha))

    pbox("Pinhole wall", 0, -40, 5893, 40, C_STEEL, h=70)
    pbox("Pinhole", 2379, -46, 40, 52, "#101014", h=95)
    # neutral (flat) film plane + neutral carriages — ghost, for before/after comparison
    pbox("Film neutral (ghost)", 150, PL_FPY - 16, 4499, 32, C_PANEL, alpha=0.15)
    pbox("L carriage neutral (ghost)", 125, PL_FPY - 25, 55, 50, C_CAR, alpha=0.22)
    pbox("R carriage neutral (ghost)", 4649 - 30, PL_FPY - 25, 55, 50, C_CAR, alpha=0.22)
    # LEFT corner (swung): fixed-X depth rail, carriage (moved fwd in Y), X-slide arm, U-joint
    pbox("L depth rail (fixed X)", 144, 1300, 12, 1120, C_STEEL)
    pbox("L carriage (friction)", 125, PL_L[1] - 25, 55, 50, C_CAR)
    pbox("L X-slide (swing accom.)", 150, PL_L[1] - 9, PL_L[0] - 150, 18, C_XSL)
    pbox("L U-joint", PL_L[0] - 11, PL_L[1] - 11, 22, 22, C_CROSS)
    # RIGHT corner (swung)
    pbox("R depth rail (fixed X)", 4644, 2020, 12, 1120, C_STEEL)
    pbox("R carriage (friction)", 4649 - 30, PL_R[1] - 25, 55, 50, C_CAR)
    pbox("R X-slide (swing accom.)", PL_R[0], PL_R[1] - 9, 4649 - PL_R[0], 18, C_XSL)
    pbox("R U-joint", PL_R[0] - 11, PL_R[1] - 11, 22, 22, C_CROSS)
    # swung film plane (angled) — explicit thin quad face in `ents`
    P.append(f'''  # Film swung [plan]
  begin
    grp = ents.add_group
    grp.name = "Film swung [plan]"
    a = Geom::Point3d.new({ov.mm(PL_L[0])}, {ov.mm(PL_L[1])}, {ov.mm(8)})
    b = Geom::Point3d.new({ov.mm(PL_R[0])}, {ov.mm(PL_R[1])}, {ov.mm(8)})
    dir = a.vector_to(b); dir.normalize!
    perp = Geom::Vector3d.new(-dir.y, dir.x, 0)
    hw = {ov.mm(17)}
    f = grp.entities.add_face(a.offset(perp, hw), a.offset(perp, -hw), b.offset(perp, -hw), b.offset(perp, hw))
    f.pushpull({ov.mm(40)})
    mat = model.materials["swung_film"] || model.materials.add("swung_film")
    mat.color = Sketchup::Color.new(31, 59, 102); mat.alpha = 1.0
    grp.material = mat
  rescue => e
  end
''')
    return "\n".join(P)


def plan_labels():
    L = []
    def txt(s, x, y, z, vx, vy, vz):
        L.append(f'''
tt = entities.add_text("{s}", Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)}), Geom::Vector3d.new({ov.mm(vx)}, {ov.mm(vy)}, {ov.mm(vz)}))
tt.layer = model.layers["Swing Plan"] rescue nil''')
    txt("PLAN (top-down) — SWING", 1900, 3350, 60, 60, 40, 0)
    txt("Pinhole", 2399, 0, 95, 45, -55, 0)
    txt("Neutral film plane (flat, ghost)", 3100, PL_FPY, 50, 45, 45, 0)
    txt("Swung film plane (20deg)", 3500, 2760, 55, 45, 45, 0)
    txt("LEFT corner: DEPTH drive fwd ~770mm; X-slide takes ~136mm sideways", 286, 1493, 70, -50, -45, 0)
    txt("RIGHT corner: DEPTH drive back; X-slide takes up sideways", 4512, 3031, 70, 45, 45, 0)
    txt("Depth rail stays at fixed X=150", 150, 1340, 60, -55, -30, 0)
    return "\n".join(L)


def generate_ruby():
    comps = [
        ov.component("Bottom Corner", "Bottom Corner", corner(0, +1, "(bot)")),
        ov.component("Top Corner", "Top Corner", corner(CH, -1, "(top)")),
        ov.component("Film Plane", "Film Plane", film_plane()),
        ov.component("Swing Plan", "Swing Plan", swing_plan()),
    ]
    body = "\n".join(comps)
    tags_ruby = "\n".join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep = "[" + ", ".join(f'"{t}"' for t in TAGS) + "]"
    full = ["Bottom Corner", "Top Corner", "Film Plane"]
    scenes = [
        ("Overview", full, (0, 0, CH / 2, 3200)),
        ("Bottom Corner", ["Bottom Corner", "Film Plane"], (0, 0, STACK, 360)),
        ("Top Corner", ["Top Corner", "Film Plane"], (0, 0, CH - STACK, 360)),
        ("Labeled", full + ["Labels"], (300, 0, CH / 2, 3600)),
    ]

    def scene_lit(n, tags, tgt):
        tg = "[" + ", ".join(f'"{t}"' for t in tags) + "]"
        cam = "nil" if tgt is None else f"[{ov.mm(tgt[0])}, {ov.mm(tgt[1])}, {ov.mm(tgt[2])}, {ov.mm(tgt[3])}]"
        return f'["{n}", {tg}, {cam}]'
    scenes_ruby = "[" + ", ".join(scene_lit(*s) for s in scenes) + "]"

    return f'''# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/generate_corner_gimbal_model.py — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("Film-Plane Corner Mechanism", true)
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

{body}

# ── "Labeled" scene callouts (Labels tag) ──
{labels()}

# ── "Swing (plan)" callouts (Swing Plan tag) ──
{plan_labels()}

{ov.license_note()}

model.definitions.purge_unused
model.materials.purge_unused

keep_tags = {keep}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

dir = Geom::Vector3d.new(0.55, -0.72, 0.30); dir.normalize!
{scenes_ruby}.each {{ |name, tags, tgt|
  model.layers.each {{ |l| l.visible = (l == default_layer || tags.include?(l.name)) }}
  if tgt
    t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
    cdir = Geom::Vector3d.new(0.55, -0.72, 0.30); cdir.normalize!
    model.active_view.camera = Sketchup::Camera.new(t.offset(cdir, tgt[3]), t, Z_AXIS)
  else
    ctr = model.bounds.center
    eye = ctr.offset(dir, model.bounds.diagonal * 1.4)
    model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
    model.active_view.zoom_extents
  end
  page = model.pages.add(name)
  page.use_camera = true
}}

# ── Swing (plan) scene — top-down camera, only the Swing Plan tag visible ──
model.layers.each {{ |l| l.visible = (l == default_layer || l.name == "Swing Plan") }}
pc = Geom::Point3d.new({ov.mm(2399)}, {ov.mm(2000)}, 0)
pe = Geom::Point3d.new({ov.mm(2399)}, {ov.mm(2000)}, {ov.mm(9500)})
model.active_view.camera = Sketchup::Camera.new(pe, pc, Y_AXIS)
psc = model.pages.add("Swing (plan)")
psc.use_camera = true

model.layers.each {{ |l| l.visible = true }}

model.commit_operation
{{ success: true, model: "Film-Plane Corner Mechanism",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the film-plane corner / whole-mechanism SketchUp model")
    parser.add_argument("--save", action="store_true", help="Write Ruby to src/models/corner-gimbal.rb")
    parser.add_argument("--send", action="store_true", help="Send to the ACTIVE SketchUp doc (open a NEW doc first)")
    args = parser.parse_args()

    ruby = generate_ruby()
    if args.save:
        out = os.path.join(os.path.dirname(__file__), "corner-gimbal.rb")
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
