#!/usr/bin/env python3
"""Generate the TBS-001 Film-Plane tilt/swing mechanism — OPTION A (logical model:
film-plane-optA).

Option A keeps the film as a FIXED-SIZE rigid rectangle (FP_W x FP_H) and changes
only its ANGLE. A rigid rotation makes each corner travel along an arc, so each
corner's existing depth rail/leadscrew gains a 2-axis X-Z cross-slide + spherical
rod-end that absorbs the arc travel. This replaces the earlier "stretching"
4-corner scheme (no telescoping frame, no warped muslin).

Per-corner kinematic CHAIN (fixed structure -> rigid frame):
    HGR20 rail (FIXED depth guide)  ->  carriage + drive nut on the leadscrew
    (drives DEPTH / focus)  ->  X cross-slide (blue, absorbs SWING float)  ->
    Z cross-slide (green, absorbs TILT float)  ->  spherical rod-end  ->  frame corner.

Posed at a realistic working angle (tilt 20 deg / swing 15 deg) where all four
carriages stay ON the 2200 mm design rail (corner depths 204..2158, inside the
100..2262 rail span). The full old +-42/+-25.7 envelope is NOT achievable with a
rigid plane — at those angles a corner would sweep ~3.4 m of depth, through both
end walls — so the practical envelope is tilt<=20 / swing<=15 (combined).

REUSES the helpers from the Overview generator (generate_sketchup_model as ov):
ruby_box / ruby_cylinder / ruby_pipe / component / colors / mm. The 3D companion
to the 2D generate_film_plane_mechanism.py corner-bracket sheet.

NOTE: --send builds into the ACTIVE SketchUp document (it clears it first). Open a
NEW blank document before sending so an existing model isn't overwritten, then save
the result as models/film-plane-optA.skp. Scene-tab cameras can mis-frame in some
SketchUp builds — render detail views by setting the camera directly (see the
project notes), then write_image.
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov

# ── Realistic working pose (combined corner depth stays on the 2200 mm rail) ──
TILT_DEG = 20.0
SWING_DEG = 15.0
TILT = math.radians(TILT_DEG)
SWING = math.radians(SWING_DEG)
W, H = ov.FP_W, ov.FP_H                 # 4499 x 2388 — the FIXED film rectangle
CY = (ov.FP_Y_MIN + ov.FP_Y) / 2        # 1181 — centre the plane at mid-rail

C_XSL = "#1F77B4"   # blue  — X cross-slide (SWING float)
C_ZSL = "#2CA02C"   # green — Z cross-slide (TILT float)
C_GHOST = "#9AA6B2"

TAGS = ["Plane", "Mechanism", "Labels"]


# ── rigid-rotation maths ─────────────────────────────────────────────────────
def _rx(v, a):
    x, y, z = v; c, s = math.cos(a), math.sin(a)
    return (x, y * c - z * s, y * s + z * c)


def _rz(v, a):
    x, y, z = v; c, s = math.cos(a), math.sin(a)
    return (x * c - y * s, x * s + y * c, z)


def _pose(v):
    """Centre-relative local vector rotated by tilt (about X width axis) then swing
    (about Z height axis)."""
    return _rz(_rx(v, TILT), SWING)


def corner_data(cx, cy, cz):
    """Per corner: flat rail point (fx,fz = rail line X/Z), carriage depth py,
    posed frame corner (px,py,pz)."""
    loc = {"TL": (-W / 2, 0, H / 2), "TR": (W / 2, 0, H / 2),
           "BR": (W / 2, 0, -H / 2), "BL": (-W / 2, 0, -H / 2)}
    out = {}
    for k, v in loc.items():
        fx, fz = cx + v[0], cz + v[2]
        d = _pose(v); px, py, pz = cx + d[0], cy + d[1], cz + d[2]
        out[k] = dict(fx=fx, fz=fz, px=px, py=py, pz=pz)
    return out


def posed_corners(cx, cy, cz):
    cd = corner_data(cx, cy, cz)
    return {k: (v["px"], v["py"], v["pz"]) for k, v in cd.items()}


def ruby_quad(name, pts, color, alpha):
    """A single planar quad face through 4 points (the posed muslin screen)."""
    p = [f'[{ov.mm(x)},{ov.mm(y)},{ov.mm(z)}]' for (x, y, z) in pts]
    rr, gg, bb = ov.hex_to_rgb(color)
    mat = ov.shared_mat_name(name, color, alpha)
    return '\n'.join([
        f'  # {name}', '  grp = ents.add_group', f'  grp.name = "{name}"',
        '  ge = grp.entities',
        f'  f = ge.add_face({p[0]}, {p[1]}, {p[2]}, {p[3]})',
        f'  mat = model.materials["{mat}"] || model.materials.add("{mat}")',
        f'  mat.color = Sketchup::Color.new({rr}, {gg}, {bb})',
        f'  mat.alpha = {alpha}', '  grp.material = mat', ''])


def joint_ball(name, p, r, color):
    """Small cube standing in for a spherical rod-end / bearing ball."""
    return ov.ruby_box(name, p[0] - r, p[1] - r, p[2] - r, 2 * r, 2 * r, 2 * r, color=color)


def frame(C):
    """Translucent muslin screen + 2" angle frame tubes through the 4 posed corners."""
    parts = [ruby_quad("Film Plane Screen (muslin)",
                       [C["TL"], C["TR"], C["BR"], C["BL"]], ov.C_FILM, 0.22)]
    r = ov.FP_ANGLE_LEG / 2
    for a, b, nm in [("TL", "TR", "Top"), ("BR", "BL", "Bottom"),
                     ("TL", "BL", "Left"), ("TR", "BR", "Right")]:
        parts.append(ov.ruby_pipe(f"FP Frame {nm}", C[a], C[b], r, color=ov.C_STEEL))
    return '\n'.join(parts)


def corner_chain(cid, d):
    """Connected solids for one corner's chain. The cross-slide motion is in world
    X (swing) and Z (tilt) at constant depth Y, so the slides are axis-aligned bars
    that visibly butt together: rail -> carriage -> X-slide -> Z-slide -> rod-end."""
    fx, fz, px, py, pz = d["fx"], d["fz"], d["px"], d["py"], d["pz"]
    dx, dz = px - fx, pz - fz
    y0, rlen = ov.FP_Y_MIN, ov.RAIL_LEN     # true design rail: 100 .. 2300 mm (2200 long)
    p = []
    # 1. HGR20 rail (FIXED) + leadscrew running its length
    p.append(ov.ruby_box(f"HGR20 Rail {cid} (fixed)",
             fx - 12, y0, fz - 8, 24, rlen, 16, color=ov.C_RAIL))
    p.append(ov.ruby_pipe(f"Leadscrew {cid} (depth drive)",
             (fx + 34, y0, fz), (fx + 34, y0 + rlen, fz), 7, color=ov.C_STEEL))
    # 2. carriage straddling the rail at the corner's depth + drive nut on the screw
    p.append(ov.ruby_box(f"Carriage {cid} (HGH20CA)",
             fx - 26, py - 32, fz - 18, 52, 64, 24, color=ov.C_CARR))
    p.append(ov.ruby_box(f"Drive Nut {cid}",
             fx + 20, py - 14, fz - 12, 28, 28, 26, color=ov.C_CARR))
    # 3. X cross-slide (BLUE) — base bar on the carriage top spanning fx..px in X
    x0 = min(fx, px) - 16
    p.append(ov.ruby_box(f"X cross-slide {cid} (SWING)",
             x0, py - 16, fz + 6, abs(dx) + 32, 32, 14, color=C_XSL))
    p.append(ov.ruby_box(f"X slider block {cid}",
             px - 16, py - 20, fz + 4, 32, 40, 20, color=ov.C_CARR))
    # 4. Z cross-slide (GREEN) — base bar on the X slider spanning fz..pz in Z
    z0 = min(fz, pz) - 16
    p.append(ov.ruby_box(f"Z cross-slide {cid} (TILT)",
             px - 9, py - 15, z0, 18, 30, abs(dz) + 32, color=C_ZSL))
    p.append(ov.ruby_box(f"Z slider block {cid}",
             px - 13, py - 18, pz - 16, 26, 36, 32, color=ov.C_CARR))
    # 5. spherical rod-end onto the rigid frame corner
    p.append(joint_ball(f"Rod-End {cid} (-> frame)", (px, py, pz), 17, ov.C_STEEL))
    # 6. faint ghost: where the corner would sit if it stayed ON the rail
    p.append(joint_ball(f"Flat-corner ghost {cid}", (fx, py, fz), 13, C_GHOST))
    return '\n'.join(p)


def mechanism(cx, cy, cz):
    cd = corner_data(cx, cy, cz)
    parts = [corner_chain(cid, cd[cid]) for cid in ("TL", "TR", "BL", "BR")]
    parts.append(ov.ruby_box("Floor (ref)", cx - W / 2 - 400, cy - 1400, -8,
                 W + 800, 3000, 8, color=ov.C_SHELL, alpha=0.16))
    return '\n'.join(parts), cd


def labels_ruby(cd):
    """Screen-anchored text notes (with leaders) on the TR corner, on the Labels
    tag (shown only in the corner-detail scene)."""
    d = cd["TR"]
    fx, fz, px, py, pz = d["fx"], d["fz"], d["px"], d["py"], d["pz"]
    L = 10
    notes = [
        ("HGR20 rail - FIXED (depth guide)", (fx, py - 250, fz), (L, 0, 1.1 * L)),
        ("Leadscrew - DEPTH / focus drive", (fx + 34, py - 700, fz), (0.4 * L, 0, 1.9 * L)),
        ("Carriage + drive nut", (fx - 20, py, fz - 12), (-1.0 * L, 0, -1.5 * L)),
        ("X cross-slide = SWING float (blue)", ((fx + px) / 2, py, fz + 14), (-1.2 * L, 0, 0.4 * L)),
        ("Z cross-slide = TILT float (green)", (px, py, (fz + pz) / 2), (1.7 * L, 0, -1.2 * L)),
        ("Rod-end -> rigid frame corner", (px, py, pz), (1.7 * L, 0, 0.5 * L)),
        ("ghost = corner if it stayed on rail", (fx, py, fz), (-1.7 * L, 0, 1.3 * L)),
    ]
    out = []
    for txt, anc, vec in notes:
        a = f'Geom::Point3d.new({ov.mm(anc[0])},{ov.mm(anc[1])},{ov.mm(anc[2])})'
        v = f'Geom::Vector3d.new({vec[0]},{vec[1]},{vec[2]})'
        out.append(f't=entities.add_text("{txt}", {a}, {v}); '
                   f't.layer=model.layers["Labels"] rescue nil')
    return '\n'.join(out)


def generate_ruby():
    cx = (ov.FP_X_L + ov.FP_X_R) / 2
    cz = H / 2
    mech, cd = mechanism(cx, CY, cz)
    comps = [
        ov.component("Floating-corner mechanism", "Mechanism", mech),
        ov.component("Film Plane (rigid, fixed size)", "Plane",
                     frame(posed_corners(cx, CY, cz))),
    ]
    body = '\n'.join(comps)
    labels = labels_ruby(cd)
    tags_ruby = '\n'.join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    tr = (cd["TR"]["px"], cd["TR"]["py"], cd["TR"]["pz"])
    ar = 1300.0 / 900.0

    def C(p): return f'[{ov.mm(p[0])}, {ov.mm(p[1])}, {ov.mm(p[2])}]'
    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Film Plane Option A", true)
entities = model.active_entities
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0; opts["LengthPrecision"]=1

to_erase = entities.to_a.select {{ |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

{tags_ruby}

{body}

# ── Annotation notes (Labels tag — shown only in the corner-detail scene) ──
{labels}

model.definitions.purge_unused
model.materials.purge_unused
keep_tags = {keep}; dl = model.layers[0]
model.layers.to_a.each {{ |l| next if l==dl||keep_tags.include?(l.name); model.layers.remove(l,true) rescue nil }}

dir = Geom::Vector3d.new(0.55, -0.82, 0.40); dir.normalize!
# Scene 1: full assembly, Labels OFF
model.layers["Labels"].visible = false
ac = Geom::Point3d.new({ov.mm(cx)}, {ov.mm(CY)}, {ov.mm(cz)})
cam = Sketchup::Camera.new(ac.offset(dir,330), ac, Z_AXIS); cam.fov=35; cam.aspect_ratio={ar}
model.active_view.camera = cam
p1 = model.pages.add("Assembly"); p1.use_camera = true
# Scene 2: zoomed TR corner, Labels ON
model.layers["Labels"].visible = true
tc = Geom::Point3d.new(*{C(tr)})
dir2 = Geom::Vector3d.new(0.5, -0.84, 0.38); dir2.normalize!
cam2 = Sketchup::Camera.new(tc.offset(dir2,95), tc, Z_AXIS); cam2.fov=35; cam2.aspect_ratio={ar}
model.active_view.camera = cam2
p2 = model.pages.add("Corner detail (TR)"); p2.use_camera = true

model.commit_operation
{{ success: true, model: "film-plane-optA", scenes: model.pages.count,
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tilt: {TILT_DEG}, swing: {SWING_DEG} }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the TBS-001 Film-Plane Option-A model")
    parser.add_argument("--save", action="store_true",
                        help="Write Ruby to src/models/film-plane-optA.rb")
    parser.add_argument("--send", action="store_true",
                        help="Send to the ACTIVE SketchUp document (clears it first — "
                             "open a NEW doc before sending)")
    args = parser.parse_args()

    ruby = generate_ruby()
    if args.save:
        out = os.path.join(os.path.dirname(__file__), "film-plane-optA.rb")
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
