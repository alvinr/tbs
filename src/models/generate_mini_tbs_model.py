#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Generate the TBS-002 (Mini-TBS) classroom-camera SketchUp model (logical model: mini-tbs).

The complete two-box cardboard pinhole camera with the CARDBOARD BOXES GHOSTED
(translucent walls) so the interior reads through them, and THREE clickable dynamic
components (click with the Interact tool — each toggles on click):

  1. Shutter          — lifts off the pinhole to expose (roty about its top hinge).
  2. Extraction flap  — the prep-box end face swings open for daylight print removal
                        (roty about its top hinge); the arm sleeves ride with it.
  3. Film-plane panel — folds DOWN into the prep box to coat / UP to the exposure
                        position facing the pinhole (roty about its bottom hinge).

Plus a translucent LIGHT CONE (pinhole → paper) on its own toggleable tag.

Geometry is single-sourced from src/generators/mini_tbs_constants.py (shared with the
2D diagram generate_mini_tbs_diagram.py) so the drawing and the model can't drift.
Reuses the Overview helpers (generate_sketchup_model as ov): ruby_box / ruby_cylinder /
component / colors / mm / license_note.

NOTE: --send builds into the ACTIVE SketchUp document (it clears it first). Open a NEW
blank document before sending so another model isn't overwritten, then save the result
as models/mini-tbs.skp.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "generators"))
from mini_tbs_constants import (
    BOX_W, BOX_D, BOX_H, WALL_T, PH_D, F_NO,
    PANEL_W, PANEL_H, HINGE_Y_ABS, PAPER_W, PAPER_H,
    SLEEVE_D, SLEEVE_SPACING, PREP_D, TOTAL_D,
)

TAGS = ["Boxes", "Pinhole", "Shutter", "Film Panel", "Extraction Flap",
        "Light Cone", "Labels"]

# ── Derived positions (mm) ───────────────────────────────────────────────────
PH_Y = HINGE_Y_ABS + PANEL_H / 2   # 203 — pinhole / film-plane centre height (= box centre)
CY = BOX_W / 2                     # 228.5 — box centreline (width)
SLEEVE_LEN = 130                   # mm — sleeve tube length shown
GHOST_A = 0.16                     # ghost-wall alpha

# ── Local palette (cardboard/paper/fabric; ov has the metals + film blue) ────
C_CARD = "#D2B48C"     # cardboard tan (matches the 2D C_BOX)
C_PAPER = "#FAF6E8"    # watercolor paper (cream)
C_SHUTTER = "#3A3A3A"  # black card shutter
C_SLEEVE = "#484060"   # black fabric arm sleeve
C_LINER = "#2A2A2A"    # duct-tape drip liner


# ── Static geometry ──────────────────────────────────────────────────────────
def ghost_walls():
    """The two boxes as one long enclosure — thin translucent cardboard walls so the
    interior reads through them. Camera-side junction is open (window removed); the
    end face is the (clickable) extraction flap, so neither is a wall here."""
    a = GHOST_A
    parts = [
        ov.ruby_box("Floor", 0, 0, -WALL_T, TOTAL_D, BOX_W, WALL_T,
                    color=C_CARD, alpha=a, both_sides=True),
        ov.ruby_box("Ceiling", 0, 0, BOX_H, TOTAL_D, BOX_W, WALL_T,
                    color=C_CARD, alpha=a * 0.6, both_sides=True),
        ov.ruby_box("Side wall (near)", 0, -WALL_T, 0, TOTAL_D, WALL_T, BOX_H,
                    color=C_CARD, alpha=a, both_sides=True),
        ov.ruby_box("Side wall (far)", 0, BOX_W, 0, TOTAL_D, WALL_T, BOX_H,
                    color=C_CARD, alpha=a, both_sides=True),
        ov.ruby_box("Pinhole wall", -WALL_T, 0, 0, WALL_T, BOX_W, BOX_H,
                    color=C_CARD, alpha=a, both_sides=True),
        # optional duct-tape drip liner on the prep-box floor
        ov.ruby_box("Duct-tape drip liner (optional)",
                    BOX_D + WALL_T, 60, 0, PREP_D - 2 * WALL_T - 60, BOX_W - 120, 1,
                    color=C_LINER, alpha=0.55),
    ]
    return '\n'.join(parts)


def pinhole_parts():
    """Aluminum pinhole plate on the front wall interior + the tiny pinhole marker."""
    return '\n'.join([
        ov.ruby_box("Pinhole plate (aluminum)", 0, CY - 25, PH_Y - 25, 2, 50, 50,
                    color=ov.C_ALUM),
        ov.ruby_cylinder(f"Pinhole Ø{PH_D}mm", -2, CY, PH_Y, 3, 6,
                         color=ov.C_PINHOLE, axis="x"),
    ])


# ── Dynamic components — each built LOCAL at its hinge, placed at the hinge, roty ─
def _flap_dc(var, disp, code, tag, geom, hinge, driver, label, angle_formula):
    """Ruby for one clickable flap DC: geometry built with its origin ON the hinge line,
    the instance placed back at the hinge, and roty driven 0→1 by a click (ANIMATE).
    Rotating about roty pivots the whole assembly about that hinge edge (world = local,
    since the instance is placed by pure translation)."""
    hx, hy, hz = (ov.mm(v) for v in hinge)
    return f'''
# ═══ {disp} — DYNAMIC COMPONENT (click to move) ═══
{var}_defn = model.definitions.add("{disp}")
ents = {var}_defn.entities
{geom}
{var}_inst = entities.add_instance({var}_defn, Geom::Transformation.translation([{hx}, {hy}, {hz}]))
{var}_inst.name = "{disp}"
{var}_inst.layer = model.layers["{tag}"]
da = "dynamic_attributes"
[{var}_defn, {var}_inst].each do |e|
  e.set_attribute(da, "_name", "{code}")
  e.set_attribute(da, "_lengthunits", "MILLIMETERS")
  e.set_attribute(da, "{driver}", 0.0)
  e.set_attribute(da, "roty", 0.0)
end
{var}_inst.set_attribute(da, "_{driver}_access", "VIEW")
{var}_inst.set_attribute(da, "_{driver}_label", "{label}")
{var}_inst.set_attribute(da, "_roty_formula", "{angle_formula}")
{var}_inst.set_attribute(da, "onclick", 'ANIMATE("{driver}", 0, 1)')
{var}_inst.set_attribute(da, "_onclick_access", "NONE")
'''


def shutter_dc():
    # A card flap just outside the pinhole wall, hinged at its TOP edge; hangs down over
    # the pinhole (closed). Local origin at the hinge; flap in -Z. roty lifts it up/out.
    geom = ov.ruby_box("Shutter flap", 0, -45, -90, 2, 90, 90, color=C_SHUTTER)
    hinge = (-WALL_T - 2, CY, PH_Y + 45)
    return _flap_dc("sh", "Shutter", "Shutter", "Shutter", geom, hinge,
                    "lift", "Lift (0 closed / 1 open)", "110*lift")


def extraction_dc():
    # The prep-box END face, hinged at its TOP edge; swings up/out. The two arm sleeves
    # are mounted IN the flap (they ride with it). Local origin at the top hinge.
    parts = [ov.ruby_box("Extraction flap", 0, 0, -BOX_H, WALL_T, BOX_W, BOX_H, color=C_CARD)]
    for cy in (CY - SLEEVE_SPACING / 2, CY + SLEEVE_SPACING / 2):
        parts.append(ov.ruby_cylinder("Arm sleeve", WALL_T, cy, -BOX_H / 2,
                                      SLEEVE_D / 2, SLEEVE_LEN, color=C_SLEEVE,
                                      alpha=0.9, axis="x"))
    hinge = (TOTAL_D - WALL_T, 0, BOX_H)
    return _flap_dc("ef", "Extraction flap", "ExtractionFlap", "Extraction Flap",
                    '\n'.join(parts), hinge, "open",
                    "Open (0 closed / 1 open)", "-110*open")


def panel_dc():
    # The cut-cardboard film-plane panel at the junction, hinged at its BOTTOM edge.
    # Default UP = exposure (paper faces the pinhole); click folds it DOWN (+X) into the
    # prep box for coating. Paper mounted on the camera-facing side, centred on the panel.
    parts = [
        ov.ruby_box("Panel board", -WALL_T, -PANEL_W / 2, 0, WALL_T, PANEL_W, PANEL_H,
                    color=C_CARD),
        ov.ruby_box("Coated paper", -WALL_T - 1, -PAPER_W / 2, (PANEL_H - PAPER_H) / 2,
                    1, PAPER_W, PAPER_H, color=C_PAPER),
    ]
    hinge = (BOX_D, CY, HINGE_Y_ABS)
    return _flap_dc("fp", "Film-plane panel", "FilmPanel", "Film Panel",
                    '\n'.join(parts), hinge, "fold",
                    "Fold (0 exposure up / 1 coating down)", "90*fold")


def light_cone_ruby():
    """A translucent pyramid from the pinhole (apex) to the paper (base, exposure
    position). Built inline as a top-level group on the Light Cone tag."""
    apex = (0, CY, PH_Y)
    px = BOX_D - WALL_T - 1        # paper front face, exposure position
    base = [(px, CY - PAPER_W / 2, PH_Y - PAPER_H / 2),
            (px, CY + PAPER_W / 2, PH_Y - PAPER_H / 2),
            (px, CY + PAPER_W / 2, PH_Y + PAPER_H / 2),
            (px, CY - PAPER_W / 2, PH_Y + PAPER_H / 2)]
    p = lambda t: f'Geom::Point3d.new({ov.mm(t[0])}, {ov.mm(t[1])}, {ov.mm(t[2])})'
    return f'''
# ── Light cone (pinhole → paper) — translucent teaching aid, own tag ──
lc = entities.add_group
lc.name = "Light cone"
lc.layer = model.layers["Light Cone"]
lge = lc.entities
apx = {p(apex)}
p0 = {p(base[0])}; p1 = {p(base[1])}; p2 = {p(base[2])}; p3 = {p(base[3])}
lge.add_face(apx, p0, p1)
lge.add_face(apx, p1, p2)
lge.add_face(apx, p2, p3)
lge.add_face(apx, p3, p0)
lge.add_face(p0, p1, p2, p3)
lcm = model.materials["Light cone"] || model.materials.add("Light cone")
lcm.color = Sketchup::Color.new(74, 144, 217)
lcm.alpha = 0.12
lge.grep(Sketchup::Face).each {{ |f| f.material = lcm; f.back_material = lcm }}
'''


# ── "Labeled" scene callouts (project rule: every .skp gets a Labeled scene) ──
# (instance name, text, leader Δx, Δy, Δz mm). Camera looks from −X/−Y/+Z, so
# Δy<0 / Δz>0 pulls a callout OUT toward the viewer; Δx spreads them apart.
LABELS = [
    ("Pinhole", f"PINHOLE  Ø{PH_D}mm  (f/{F_NO})", -200, -300, 250),
    ("Shutter", "SHUTTER\n(click: lift to expose)", -300, -350, 350),
    ("Film-plane panel", "FILM-PLANE PANEL\n(click: fold down to coat / up to expose)", 120, -450, 450),
    ("Extraction flap", "EXTRACTION FLAP\n(click: swing open — daylight print removal)", 400, -300, 300),
    ("Cardboard boxes (ghost)", "TWO CARDBOARD BOXES\n(camera + prep — ghosted)", -120, 520, 560),
]
# Point-anchored (x,y,z,text,Δx,Δy,Δz) — for parts that ride inside a DC.
POINT_LABELS = [
    (TOTAL_D + SLEEVE_LEN, CY - SLEEVE_SPACING / 2, BOX_H / 2,
     "ARM SLEEVES\n(reach in to mix + coat in the dark)", 300, -200, 250),
    (BOX_D / 2, CY, PH_Y,
     "LIGHT CONE\n(pinhole → paper)", -150, -420, 300),
]


def labels_ruby():
    rows = []
    for name, text, dx, dy, dz in LABELS:
        rows.append(
            f'inst = entities.grep(Sketchup::ComponentInstance).find {{ |i| i.name == "{name}" }}\n'
            f'if inst\n'
            f'  bb = inst.bounds\n'
            f'  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)\n'
            f'  txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'  txt.layer = model.layers["Labels"] rescue nil\n'
            f'end')
    for x, y, z, text, dx, dy, dz in POINT_LABELS:
        rows.append(
            f'anc = Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    return '\n'.join(rows)


def generate_ruby():
    body = '\n'.join([
        ov.component("Cardboard boxes (ghost)", "Boxes", ghost_walls()),
        ov.component("Pinhole", "Pinhole", pinhole_parts()),
    ])
    tags_ruby = '\n'.join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    # scenes: name, visible tags, (unused target) None, standoff 0 = zoom-extents
    hardware = ["Boxes", "Pinhole", "Shutter", "Film Panel", "Extraction Flap"]
    scenes = [("Assembled", hardware, None, 0),
              ("Light path", hardware + ["Light Cone"], None, 0),
              ("Labeled", hardware + ["Light Cone", "Labels"], None, 0)]

    def slit(s):
        name, tags, tgt, so = s
        tg = '[' + ', '.join(f'"{t}"' for t in tags) + ']'
        cam = 'nil' if tgt is None else f'[{ov.mm(tgt[0])}, {ov.mm(tgt[1])}, {ov.mm(tgt[2])}]'
        return f'["{name}", {tg}, {cam}, {so}]'
    scenes_ruby = '[' + ', '.join(slit(s) for s in scenes) + ']'

    return f'''# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("TBS-002 Mini-TBS (ghosted boxes + clickable flaps)", true)
entities = model.active_entities
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0; opts["LengthPrecision"]=1

to_erase = entities.to_a.select {{ |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

{tags_ruby}

{body}

# ── Clickable dynamic components ──
{shutter_dc()}
{panel_dc()}
{extraction_dc()}

# ── Light cone (translucent teaching aid) ──
{light_cone_ruby()}

# ── Component callouts (Labels tag — shown only in the "Labeled" scene) ──
{labels_ruby()}

{ov.license_note()}

model.definitions.purge_unused
model.materials.purge_unused
keep_tags = {keep}; dl = model.layers[0]
model.layers.to_a.each {{ |l| next if l==dl||keep_tags.include?(l.name); model.layers.remove(l,true) rescue nil }}

model.layers.each {{ |l| l.visible = true }}
bb = model.bounds; ctr = bb.center
dir = Geom::Vector3d.new(-0.4, -0.8, 0.45); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.4)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

{scenes_ruby}.each {{ |name, tags, tgt, so|
  model.layers.each {{ |l| l.visible = (l == dl || tags.include?(l.name)) }}
  model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
  model.active_view.zoom_extents
  page = model.pages.add(name); page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}
model.layers["Light Cone"].visible = false
model.layers["Labels"].visible = false

model.commit_operation

# Register the DCs AFTER committing (redraw_with_undo opens its own operation).
if defined?($dc_observers) && $dc_observers.respond_to?(:get_latest_class)
  cls = $dc_observers.get_latest_class
  [sh_inst, fp_inst, ef_inst].each {{ |di| cls.redraw_with_undo(di) rescue nil }} if cls
end

{{ success: true, model: "mini-tbs", scenes: model.pages.count,
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   focal_mm: {BOX_D}, f_number: {F_NO} }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the TBS-002 Mini-TBS model")
    parser.add_argument("--save", action="store_true", help="Write Ruby to src/models/mini-tbs.rb")
    parser.add_argument("--send", action="store_true",
                        help="Send to the ACTIVE SketchUp document (clears it first)")
    args = parser.parse_args()

    ruby = generate_ruby()
    if args.save:
        out = os.path.join(os.path.dirname(__file__), "mini-tbs.rb")
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
