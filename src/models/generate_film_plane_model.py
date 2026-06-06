#!/usr/bin/env python3
"""Generate the TBS-001 Film-Plane SketchUp model (logical model: film-plane).

Focused on the film plane and its 4-corner tilt/swing mechanism. The framed
muslin screen is posed in an EXAMPLE tilt + swing (the four corners parked at
different depths), and the tilt/swing hardware is shown in detail at each of the
four corners (TL/TR/BL/BR): an HGR20 linear rail + HGH20CA carriage + leadscrew +
drive nut + universal joint + corner bracket. The processing tray and a ghost of
the container are included for context.

REUSES the helpers + builders from the Overview generator
(generate_sketchup_model.py) — same component/tag/scene structure, shared iso
camera, and material-sharing-by-color. The 3D companion to the 2D
generate_film_plane_mechanism.py (Sheet 3 = corner bracket + universal joint).

Usage (build into a SketchUp document — see --send note):
    python3 src/models/generate_film_plane_model.py --save        # write film-plane.rb
    python3 src/models/generate_film_plane_model.py --save --send # + send to the ACTIVE doc

NOTE: --send builds into the ACTIVE SketchUp document (it clears it first). Open a
NEW blank SketchUp document before sending so the Overview model isn't overwritten,
then save the result as models/film-plane.skp.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov   # helpers + component builders (Overview)

TAGS = ["Context", "Film Plane", "Corner Mechanism", "Processing Tray"]

# ── Example tilt + swing pose ────────────────────────────────────────────────
# Each corner is parked at its own DEPTH (Yd) on its rail. Neutral = FP_Y (2262)
# for all four; here the top is tilted back and the left swung back. Depths are
# chosen planar (d_TL + d_BR == d_TR + d_BL) so the screen stays flat — a genuine
# tilt+swing, well inside the ±42° tilt / ±25.7° swing envelope.
D_TL, D_TR, D_BL, D_BR = 2262, 1962, 1862, 1562

RZ_BOT = ov.RAIL_OFF                 # 100  — floor-rail Z (carries BL, BR)
RZ_TOP = ov.C_HGT - ov.RAIL_OFF      # 2288 — ceiling-rail Z (carries TL, TR)

# Corner table: id, X, corner Z, depth, rail Z
CORNERS = [
    ("TL", ov.FP_X_L, ov.FP_H, D_TL, RZ_TOP),
    ("TR", ov.FP_X_R, ov.FP_H, D_TR, RZ_TOP),
    ("BL", ov.FP_X_L, 0,        D_BL, RZ_BOT),
    ("BR", ov.FP_X_R, 0,        D_BR, RZ_BOT),
]
CPT = {cid: (cx, d, cz) for cid, cx, cz, d, rz in CORNERS}   # muslin corner points

import math
# ── Film plane as a DYNAMIC COMPONENT ────────────────────────────────────────
# Click (Interact tool) animates the framed screen between FLAT (pose=0, neutral
# plane at Y=FP_Y) and the example TILT+SWING (pose=1). The real mechanism warps
# the plane (each corner parked at its own depth), which a DC cannot deform — so
# this is the equivalent RIGID rotation about the fixed TL corner: tilt (RotX,
# bottom edge swings forward) + swing (RotZ, right edge swings forward), driven by
# one "pose" attribute (RotX=TILT*pose, RotZ=SWING*pose).
PIVOT = (ov.FP_X_L, D_TL, ov.FP_H)          # TL corner — the Y=2262 corner that stays put
TILT_DEG  =  round(math.degrees(math.atan(((D_TL + D_TR) / 2 - (D_BL + D_BR) / 2) / ov.FP_H)), 2)
SWING_DEG = -round(math.degrees(math.atan(((D_TL + D_BL) / 2 - (D_TR + D_BR) / 2) / ov.FP_W)), 2)
# Flat (neutral) corner points in LOCAL coords relative to the TL pivot.
LOCAL = {"TL": (0, 0, 0), "TR": (ov.FP_W, 0, 0),
         "BL": (0, 0, -ov.FP_H), "BR": (ov.FP_W, 0, -ov.FP_H)}


def ruby_quad(name, pts, color, alpha):
    """A single planar quad face through 4 points (the posed muslin screen)."""
    p = [f'[{ov.mm(x)},{ov.mm(y)},{ov.mm(z)}]' for (x, y, z) in pts]
    rr, gg, bb = ov.hex_to_rgb(color)
    mat_nm = ov.shared_mat_name(name, color, alpha)
    return '\n'.join([
        f'  # {name}',
        '  grp = ents.add_group',
        f'  grp.name = "{name}"',
        '  ge = grp.entities',
        f'  f = ge.add_face({p[0]}, {p[1]}, {p[2]}, {p[3]})',
        f'  mat = model.materials["{mat_nm}"] || model.materials.add("{mat_nm}")',
        f'  mat.color = Sketchup::Color.new({rr}, {gg}, {bb})',
        f'  mat.alpha = {alpha}',
        '  grp.material = mat',
        '',
    ])


def context():
    """Low-alpha ghost of the whole container — floor, ceiling, both side walls
    and the pinhole wall (Yd=0) — so the posed film plane, tray and rails read in
    place without modeling fittings (mirrors the ibc/lighttrap ghost context)."""
    t = ov.WALL_T
    return '\n'.join([
        ov.ruby_box("Floor (context)", 0, 0, -t, ov.C_LEN, ov.C_WID, t,
                    color=ov.C_SHELL, alpha=0.22),
        ov.ruby_box("Ceiling (context)", 0, 0, ov.C_HGT, ov.C_LEN, ov.C_WID, t,
                    color=ov.C_SHELL, alpha=0.08),
        ov.ruby_box("Side Wall near (context)", 0, -t, 0, ov.C_LEN, t, ov.C_HGT,
                    color=ov.C_SHELL, alpha=0.14),
        ov.ruby_box("Side Wall far (context)", 0, ov.C_WID, 0, ov.C_LEN, t, ov.C_HGT,
                    color=ov.C_SHELL, alpha=0.14),
        ov.ruby_box("Pinhole Wall (context)", -t, 0, 0, t, ov.C_WID, ov.C_HGT,
                    color=ov.C_SHELL, alpha=0.16),
    ])


def posed_film_plane():
    """The framed muslin screen posed in tilt+swing: a planar quad through the
    four parked corner points, edged by a 2" steel angle frame (round-tube
    representation along the tilted edges)."""
    P = CPT
    parts = [
        ruby_quad("Film Plane Screen (muslin)",
                  [P["TL"], P["TR"], P["BR"], P["BL"]], ov.C_FILM, 0.3),
    ]
    leg_r = ov.FP_ANGLE_LEG / 2          # 2" angle → ~25mm tube radius
    for a, b, nm in [("TL", "TR", "Top"), ("BR", "BL", "Bottom"),
                     ("TL", "BL", "Left"), ("TR", "BR", "Right")]:
        parts.append(ov.ruby_pipe(f"FP Frame {nm}", P[a], P[b], leg_r,
                                  color=ov.C_STEEL))
    return '\n'.join(parts)


def flat_film_plane_local():
    """The framed muslin screen built FLAT in LOCAL coords relative to the TL
    pivot (TL at the component origin). The DC rotates this about its TL axes to
    reach the tilt+swing pose, so the geometry here is the neutral rectangle."""
    P = LOCAL
    parts = [
        ruby_quad("Film Plane Screen (muslin)",
                  [P["TL"], P["TR"], P["BR"], P["BL"]], ov.C_FILM, 0.3),
    ]
    leg_r = ov.FP_ANGLE_LEG / 2
    for a, b, nm in [("TL", "TR", "Top"), ("BR", "BL", "Bottom"),
                     ("TL", "BL", "Left"), ("TR", "BR", "Right")]:
        parts.append(ov.ruby_pipe(f"FP Frame {nm}", P[a], P[b], leg_r,
                                  color=ov.C_STEEL))
    return '\n'.join(parts)


def dc_film_plane_block():
    """Ruby that builds the Film Plane DYNAMIC COMPONENT: a definition holding the
    flat geometry, instanced at the TL pivot, with a `pose` attribute that drives
    RotX (tilt) + RotZ (swing). Click with the Interact tool → ANIMATE pose 0↔1."""
    tlx, tly, tlz = (ov.mm(v) for v in PIVOT)
    return f'''
# ═══ Film Plane — DYNAMIC COMPONENT (click to tilt+swing) ═══
fp_defn = model.definitions.add("Film Plane")
ents = fp_defn.entities
{flat_film_plane_local()}
fp_inst = entities.add_instance(fp_defn, Geom::Transformation.translation([{tlx}, {tly}, {tlz}]))
fp_inst.name = "Film Plane"
fp_inst.layer = model.layers["Film Plane"]
fda = "dynamic_attributes"
[fp_defn, fp_inst].each do |e|
  e.set_attribute(fda, "_name", "FilmPlane")
  e.set_attribute(fda, "_lengthunits", "MILLIMETERS")
  e.set_attribute(fda, "pose", 0.0)
  e.set_attribute(fda, "rotx", 0.0)
  e.set_attribute(fda, "rotz", 0.0)
end
fp_inst.set_attribute(fda, "_pose_access", "VIEW")
fp_inst.set_attribute(fda, "_pose_label", "Pose (0 flat / 1 tilt+swing)")
fp_inst.set_attribute(fda, "_rotx_formula", "{TILT_DEG}*pose")
fp_inst.set_attribute(fda, "_rotz_formula", "{SWING_DEG}*pose")
fp_inst.set_attribute(fda, "onclick", 'ANIMATE("pose", 0, 1)')
fp_inst.set_attribute(fda, "_onclick_access", "NONE")
'''


def corner_mechanism():
    """Per-corner tilt/swing hardware at TL/TR/BL/BR: HGR20 rail + HGH20CA carriage
    + leadscrew + drive nut + universal joint + corner bracket. The carriage sits
    at the corner's parked DEPTH; the U-joint links it to the (posed) frame corner
    so the screen can articulate as the four depths differ."""
    parts = []
    y0, rlen = ov.FP_Y_MIN, ov.RAIL_LEN          # rail span in depth (Yd)
    rail_w, rail_h = 24, 16                       # HGR20 profile
    cw, cd, ch = 44, 44, 28                       # HGH20CA carriage block
    ls_off = 26                                   # leadscrew offset from rail center (Yd-perp = X)
    for cid, cx, cz, d, rz in CORNERS:
        zc = rz - rail_h / 2                       # rail sits centerd on the rail Z
        # HGR20 linear rail — runs in +Y (depth) at the corner X, near floor/ceiling
        parts.append(ov.ruby_box(f"HGR20 Rail {cid}",
                                 cx - rail_w / 2, y0, zc, rail_w, rlen, rail_h,
                                 color=ov.C_RAIL))
        # leadscrew — Ø16 rod parallel to the rail, with a drive nut on the carriage
        parts.append(ov.ruby_cylinder(f"Leadscrew {cid}",
                                      cx + ls_off, y0, rz, 8, rlen,
                                      color=ov.C_STEEL, axis="y"))
        parts.append(ov.ruby_box(f"Drive Nut {cid}",
                                 cx + ls_off - 11, d - 11, rz - 11, 22, 22, 22,
                                 color=ov.C_CARR))
        # HGH20CA carriage block at the parked depth
        parts.append(ov.ruby_box(f"Carriage {cid} (HGH20CA)",
                                 cx - cw / 2, d - cd / 2, rz - ch / 2, cw, cd, ch,
                                 color=ov.C_CARR))
        # corner bracket plate on the carriage (toward the frame corner)
        bz = cz if cz > rz else cz                 # frame corner Z
        z_lo, z_hi = sorted((rz, cz))
        parts.append(ov.ruby_box(f"Corner Bracket {cid}",
                                 cx - 8, d - 30, z_lo, 16, 60, z_hi - z_lo,
                                 color=ov.C_STEEL, alpha=0.9))
        # universal joint — clevis yoke on the carriage + cross pin + link to the
        # frame corner (lets the frame articulate while the carriage runs straight)
        jz = (rz + cz) / 2
        for ysgn in (-1, 1):                       # two yoke ears straddling the pin
            parts.append(ov.ruby_box(f"UJoint Yoke {cid}",
                                     cx - 14, d + ysgn * 13 - 3, jz - 14, 28, 6, 28,
                                     color=ov.C_STEEL))
        parts.append(ov.ruby_cylinder(f"UJoint Cross Pin {cid}",
                                      cx - 16, d, jz, 4, 32, color="#50505A",
                                      axis="x"))
        parts.append(ov.ruby_cylinder(f"UJoint Spider {cid}",
                                      cx, d, jz, 7, 1, color="#50505A", axis="z"))
        # short link from the joint up/down to the frame corner
        parts.append(ov.ruby_pipe(f"UJoint Link {cid}",
                                  (cx, d, jz), (cx, d, cz), 6, color=ov.C_STEEL))
    return '\n'.join(parts)


def generate_ruby():
    """Build the Ruby script for the Film-Plane model, reusing Overview parts."""
    comps = [
        ov.component("Container (ghost)", "Context", context()),
        ov.component("Processing Tray", "Processing Tray", ov.processing_tray()),
        ov.component("Corner Mechanism", "Corner Mechanism", corner_mechanism()),
    ]
    body = '\n'.join(comps)
    dc_block = dc_film_plane_block()   # the Film Plane Dynamic Component

    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    fp_tags = ["Film Plane", "Corner Mechanism"]
    # scenes: name, visible tags, optional camera target point (mm) for corner zoom
    scenes = [("Combined", TAGS, None),
              ("Processing Tray", ["Processing Tray"], None)]
    for cid, cx, cz, d, rz in CORNERS:
        scenes.append((f"Corner {cid}", fp_tags, (cx, d, cz)))

    def scene_lit(name, tags, tgt):
        tg = '[' + ', '.join(f'"{t}"' for t in tags) + ']'
        if tgt is None:
            cam = 'nil'
        else:
            cam = f'[{ov.mm(tgt[0])}, {ov.mm(tgt[1])}, {ov.mm(tgt[2])}]'
        return f'["{name}", {tg}, {cam}]'
    scenes_ruby = '[' + ', '.join(scene_lit(*s) for s in scenes) + ']'

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Film Plane", true)
entities = model.active_entities

# Display in millimeters (UI readout only).
opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# ── Idempotent rebuild: erase all prior groups/instances so the model frames
# tightly on the film-plane assembly. ──
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

# ── Film Plane (Dynamic Component — click to tilt+swing) ──
{dc_block}

model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier versions ──
keep_tags = {keep_tags_ruby}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

# ── Scenes ── Combined/Tray use one iso extents camera; each corner scene zooms
# its own iso camera onto that corner's mechanism.
model.layers.each {{ |l| l.visible = true }}
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(0.72, -0.7, 0.5); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

{scenes_ruby}.each {{ |name, tags, tgt|
  model.layers.each {{ |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }}
  if tgt
    t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
    e = t.offset(dir, 70.0)        # ~1.8m iso standoff (inches)
    model.active_view.camera = Sketchup::Camera.new(e, t, Z_AXIS)
  else
    model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
    model.active_view.zoom_extents
  end
  page = model.pages.add(name)
  page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}

# Register the Dynamic Component so its formulas evaluate (else pose/RotX/RotZ
# stay inert until first opened in the DC editor).
if defined?($dc_observers) && $dc_observers.respond_to?(:get_latest_class)
  cls = $dc_observers.get_latest_class
  cls.redraw_with_undo(fp_inst) rescue nil if cls
end

model.commit_operation
{{ success: true, model: "Film Plane",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the TBS-001 Film-Plane model")
    parser.add_argument("--save", action="store_true",
                        help="Write Ruby to src/models/film-plane.rb")
    parser.add_argument("--send", action="store_true",
                        help="Send the Ruby to the ACTIVE SketchUp document "
                             "(clears it first - open a NEW doc before sending)")
    args = parser.parse_args()

    ruby = generate_ruby()

    if args.save:
        out = os.path.join(os.path.dirname(__file__), "film-plane.rb")
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
