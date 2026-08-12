#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Generate the TBS-002 (Mini-TBS) classroom-camera SketchUp model (logical model: mini-tbs).

The complete two-box cardboard pinhole camera with the CARDBOARD BOXES GHOSTED
(translucent walls) so the interior reads through them, the two boxes shown JOINED
with grey tape at the seam, and THREE clickable dynamic components (Interact tool —
each toggles on click):

  1. Shutter          — lifts off the pinhole to expose (roty about its top hinge).
  2. Prep-box top flaps — the boxes are built flaps-UP; the print is removed in
                        daylight by opening the prep box's OWN top flaps (rotx about
                        their top edges), not a custom-cut wall.
  3. Film-plane panel — folds DOWN into the prep box to coat / UP to the exposure
                        position facing the pinhole (roty about its bottom hinge).

Plus the arm sleeves (static, on the end wall — sealed coating access in the dark)
and a translucent LIGHT CONE (pinhole → paper) on its own toggleable tag.

Geometry is single-sourced from src/generators/mini_tbs_constants.py (shared with the
2D diagram generate_mini_tbs_diagram.py) so the drawing and the model can't drift.
Reuses the Overview helpers (generate_sketchup_model as ov).

NOTE: --send builds into the ACTIVE SketchUp document (it clears it first). Open a NEW
blank document before sending, then save the result as models/mini-tbs.skp.
"""
import argparse
import math
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

TAGS = ["Boxes", "Pinhole", "Shutter", "Film Panel", "Prep Top Flaps",
        "Light Cone", "Labels"]

# ── Derived positions (mm) ───────────────────────────────────────────────────
PH_Y = HINGE_Y_ABS + PANEL_H / 2   # 203 — pinhole / film-plane centre height (= box centre)
CY = BOX_W / 2                     # 228.5 — box centreline (width)
SLEEVE_LEN = 130                   # mm — sleeve tube length shown
GHOST_A = 0.16                     # ghost-wall alpha
FLAP_T = 3                         # mm — cardboard flap thickness

# ── Local palette (cardboard/paper/fabric/tape; ov has the metals + film blue) ──
C_CARD = "#D2B48C"     # cardboard tan (matches the 2D C_BOX)
C_PAPER = "#FAF6E8"    # watercolor paper (cream)
C_SHUTTER = "#3A3A3A"  # black card shutter
C_SLEEVE = "#484060"   # black fabric arm sleeve
C_LINER = "#2A2A2A"    # duct-tape drip liner
C_TAPE = "#8A8A8A"     # grey duct tape (box joins + top seams)


# ── Static geometry ──────────────────────────────────────────────────────────
def ghost_walls():
    """The two boxes as one long enclosure — thin translucent cardboard walls so the
    interior reads through them. The camera-side junction is open (window removed); the
    TOP is the box flaps (built separately); the far end is the arm-sleeve wall."""
    a = GHOST_A
    return '\n'.join([
        ov.ruby_box("Floor", 0, 0, -WALL_T, TOTAL_D, BOX_W, WALL_T,
                    color=C_CARD, alpha=a, both_sides=True),
        ov.ruby_box("Pinhole wall", -WALL_T, 0, 0, WALL_T, BOX_W, BOX_H,
                    color=C_CARD, alpha=a, both_sides=True),
        ov.ruby_box("Duct-tape drip liner (optional)",
                    BOX_D + WALL_T, 60, 0, PREP_D - 2 * WALL_T - 60, BOX_W - 120, 1,
                    color=C_LINER, alpha=0.55),
    ])


def internal_walls():
    """The two internal junction walls the film-plane panel is cut from — the camera box's
    back wall (window removed) and the prep box's front wall (the panel is the hinged flap).
    Each is drawn as a border frame around the panel window, a touch more opaque than the
    ghost shell so the hinge panel reads as sitting between them."""
    a = 0.45   # less translucent than the 0.16 ghost, still see-through (not solid)
    y0, y1 = CY - PANEL_W / 2, CY + PANEL_W / 2          # window sides (Y)
    z0, z1 = HINGE_Y_ABS, HINGE_Y_ABS + PANEL_H          # window bottom/top (Z)
    parts = []
    for wx, nm in [(BOX_D - WALL_T, "Camera junction wall"), (BOX_D, "Prep junction wall")]:
        parts += [
            ov.ruby_box(f"{nm} (below window)", wx, 0, 0, WALL_T, BOX_W, z0,
                        color=C_CARD, alpha=a, both_sides=True),
            ov.ruby_box(f"{nm} (above window)", wx, 0, z1, WALL_T, BOX_W, BOX_H - z1,
                        color=C_CARD, alpha=a, both_sides=True),
            ov.ruby_box(f"{nm} (left of window)", wx, 0, z0, WALL_T, y0, z1 - z0,
                        color=C_CARD, alpha=a, both_sides=True),
            ov.ruby_box(f"{nm} (right of window)", wx, y1, z0, WALL_T, BOX_W - y1, z1 - z0,
                        color=C_CARD, alpha=a, both_sides=True),
        ]
    return '\n'.join(parts)


def camera_top():
    """Camera-box top: two flaps folded shut (light-tight) with a grey tape strip down
    the seam. Boxes are built FLAPS-UP; the camera end stays sealed."""
    hw = BOX_W / 2
    a = GHOST_A * 0.9
    return '\n'.join([
        ov.ruby_box("Camera top flap (near)", 0, 0, BOX_H - FLAP_T, BOX_D, hw, FLAP_T,
                    color=C_CARD, alpha=a, both_sides=True),
        ov.ruby_box("Camera top flap (far)", 0, hw, BOX_H - FLAP_T, BOX_D, hw, FLAP_T,
                    color=C_CARD, alpha=a, both_sides=True),
        ov.ruby_box("Camera top tape (seam)", 0, hw - 25, BOX_H, BOX_D, 50, 1.5,
                    color=C_TAPE, alpha=0.85),
    ])


def end_wall():
    """Far end wall (opposite the pinhole) — solid, carrying the two arm sleeves that
    give sealed coating access in the dark. Static (extraction is now the top flaps)."""
    parts = [ov.ruby_box("End wall (arm-sleeve wall)", TOTAL_D - WALL_T, 0, 0,
                         WALL_T, BOX_W, BOX_H, color=C_CARD, alpha=GHOST_A, both_sides=True)]
    for cy in (CY - SLEEVE_SPACING / 2, CY + SLEEVE_SPACING / 2):
        parts.append(ov.ruby_cylinder("Arm sleeve", TOTAL_D, cy, BOX_H / 2,
                                      SLEEVE_D / 2, SLEEVE_LEN, color=C_SLEEVE,
                                      alpha=0.9, axis="x"))
    return '\n'.join(parts)


def join_tape():
    """Grey duct tape wrapping the seam where the two boxes are joined (floor, both
    sides, top) — shows the boxes taped into one enclosure."""
    b = 50
    x0, t = BOX_D - b / 2, 1.5
    return '\n'.join([
        ov.ruby_box("Join tape (floor)", x0, 0, -WALL_T - t, b, BOX_W, t, color=C_TAPE, alpha=0.9),
        ov.ruby_box("Join tape (top)", x0, 0, BOX_H, b, BOX_W, t, color=C_TAPE, alpha=0.9),
        ov.ruby_box("Join tape (near)", x0, -WALL_T - t, 0, b, t, BOX_H, color=C_TAPE, alpha=0.9),
        ov.ruby_box("Join tape (far)", x0, BOX_W + WALL_T, 0, b, t, BOX_H, color=C_TAPE, alpha=0.9),
    ])


def pinhole_parts():
    """Aluminum pinhole plate on the front wall interior + the tiny pinhole marker."""
    return '\n'.join([
        ov.ruby_box("Pinhole plate (aluminum)", 0, CY - 25, PH_Y - 25, 2, 50, 50,
                    color=ov.C_ALUM),
        ov.ruby_cylinder(f"Pinhole Ø{PH_D}mm", -2, CY, PH_Y, 3, 6,
                         color=ov.C_PINHOLE, axis="x"),
    ])


# ── Single-flap DCs (shutter, film panel) — built LOCAL at hinge, placed, roty ──
def _flap_dc(var, disp, code, tag, geom, hinge, driver, label, angle_formula, default=0.0):
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
  e.set_attribute(da, "{driver}", {default})
  e.set_attribute(da, "roty", 0.0)
end
{var}_inst.set_attribute(da, "_{driver}_access", "VIEW")
{var}_inst.set_attribute(da, "_{driver}_label", "{label}")
{var}_inst.set_attribute(da, "_roty_formula", "{angle_formula}")
{var}_inst.set_attribute(da, "onclick", 'ANIMATE("{driver}", 0, 1)')
{var}_inst.set_attribute(da, "_onclick_access", "NONE")
'''


def shutter_dc():
    geom = ov.ruby_box("Shutter flap", 0, -45, -90, 2, 90, 90, color=C_SHUTTER)
    hinge = (-WALL_T - 2, CY, PH_Y + 45)
    # default OPEN (lift=1) so the static Sketchfab view shows the pinhole uncovered
    return _flap_dc("sh", "Shutter", "Shutter", "Shutter", geom, hinge,
                    "lift", "Lift (0 closed / 1 open)", "110*lift", default=1.0)


def panel_dc():
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


def prep_top_flaps_dc():
    """The prep-box TOP flaps — the boxes are built flaps-up, so the finished print is
    removed (in daylight) by opening the box's own two top flaps. One clickable DC: a
    parent 'open' driver; each flap child rotates up (rotx) about its top edge via an
    ancestor-reference formula (cargo-door pattern)."""
    hw = BOX_W / 2
    near = ov.ruby_box("Prep top flap (near)", 0, 0, -FLAP_T, PREP_D, hw, FLAP_T, color=C_CARD)
    far = ov.ruby_box("Prep top flap (far)", 0, -hw, -FLAP_T, PREP_D, hw, FLAP_T, color=C_CARD)
    px, py, pz = (ov.mm(v) for v in (BOX_D, 0, BOX_H))
    fhx, fhy, fhz = (ov.mm(v) for v in (0, BOX_W, 0))
    return f'''
# ═══ Prep-box top flaps — DYNAMIC COMPONENT (click: open the top to extract the print) ═══
pt_defn = model.definitions.add("Prep top flaps")
ents = pt_defn.entities
ptn_defn = model.definitions.add("Prep top flap (near)")
ents = ptn_defn.entities
{near}
ptn_inst = pt_defn.entities.add_instance(ptn_defn, Geom::Transformation.new)
ptn_inst.name = "Prep top flap (near)"
ptf_defn = model.definitions.add("Prep top flap (far)")
ents = ptf_defn.entities
{far}
ptf_inst = pt_defn.entities.add_instance(ptf_defn, Geom::Transformation.translation([{fhx}, {fhy}, {fhz}]))
ptf_inst.name = "Prep top flap (far)"
pt_inst = entities.add_instance(pt_defn, Geom::Transformation.translation([{px}, {py}, {pz}]))
pt_inst.name = "Prep top flaps"
pt_inst.layer = model.layers["Prep Top Flaps"]
da = "dynamic_attributes"
[pt_defn, pt_inst].each do |e|
  e.set_attribute(da, "_name", "PrepTopFlaps")
  e.set_attribute(da, "_lengthunits", "MILLIMETERS")
  e.set_attribute(da, "open", 0.0)
end
pt_inst.set_attribute(da, "_open_access", "VIEW")
pt_inst.set_attribute(da, "_open_label", "Open (0 closed / 1 open)")
pt_inst.set_attribute(da, "onclick", 'ANIMATE("open", 0, 1)')
pt_inst.set_attribute(da, "_onclick_access", "NONE")
[ptn_defn, ptn_inst].each do |e|
  e.set_attribute(da, "_name", "PrepTopFlapNear")
  e.set_attribute(da, "_lengthunits", "MILLIMETERS")
  e.set_attribute(da, "rotx", 0.0)
end
ptn_inst.set_attribute(da, "_rotx_formula", "95*PrepTopFlaps!open")
[ptf_defn, ptf_inst].each do |e|
  e.set_attribute(da, "_name", "PrepTopFlapFar")
  e.set_attribute(da, "_lengthunits", "MILLIMETERS")
  e.set_attribute(da, "rotx", 0.0)
end
ptf_inst.set_attribute(da, "_rotx_formula", "-95*PrepTopFlaps!open")
'''


def light_cone_ruby():
    """A translucent CONE — apex at the pinhole, circular base at the film plane — showing
    the spread of light through the pinhole. Built inline as a group on the Light Cone tag."""
    apex = (0, CY, PH_Y)
    px = BOX_D - WALL_T - 1            # base plane = the film plane (exposure position)
    R = BOX_H / 2 - 6                  # base radius — nearly fills the film-plane height
    N = 32
    pts = [(px, CY + R * math.cos(2 * math.pi * k / N), PH_Y + R * math.sin(2 * math.pi * k / N))
           for k in range(N)]
    p = lambda t: f'Geom::Point3d.new({ov.mm(round(t[0], 2))}, {ov.mm(round(t[1], 2))}, {ov.mm(round(t[2], 2))})'
    base_pts = ', '.join(p(t) for t in pts)
    return f'''
# ── Light cone (pinhole → circular base at the film plane) — translucent teaching aid ──
lc = entities.add_group
lc.name = "Light cone"
lc.layer = model.layers["Light Cone"]
lge = lc.entities
apx = {p(apex)}
base = [{base_pts}]
lge.add_face(base)                                  # circular base at the film plane
base.each_with_index {{ |pt, i| lge.add_face(apx, pt, base[(i + 1) % base.length]) }}  # lateral surface
lcm = model.materials["Light cone"] || model.materials.add("Light cone")
lcm.color = Sketchup::Color.new(74, 144, 217)
lcm.alpha = 0.18
lge.grep(Sketchup::Face).each {{ |f| f.material = lcm; f.back_material = lcm }}
# Soften + smooth + hide the facet edges so the cone reads as one smooth surface
# (no black radial lines) — the sides all render as the uniform cone colour.
lge.grep(Sketchup::Edge).each {{ |e| e.soft = true; e.smooth = true; e.hidden = true }}
'''


# ── "Labeled" scene callouts. Camera looks from −X/−Y/+Z, so Δy<0 / Δz>0 pulls a
#    callout OUT toward the viewer; Δx spreads them apart. ──
LABELS = [
    ("Pinhole", f"PINHOLE  Ø{PH_D}mm  (f/{F_NO})", -70, -110, 80),
    ("Shutter", "SHUTTER\n(click: lift to expose)", -110, -140, 130),
    ("Film-plane panel", "FILM-PLANE PANEL\n(click: fold down / up)", 40, -150, 120),
    ("Prep top flaps", "PREP-BOX TOP FLAPS\n(flaps-up; click: open to extract)", 110, -120, 140),
    ("Cardboard boxes (ghost)", "TWO CARDBOARD BOXES\n(joined with grey tape)", -90, 150, 190),
]
POINT_LABELS = [
    (TOTAL_D + SLEEVE_LEN, CY - SLEEVE_SPACING / 2, BOX_H / 2,
     "ARM SLEEVES\n(coat in the dark)", 130, -90, 90),
    (BOX_D / 2, CY, PH_Y,
     "LIGHT CONE\n(pinhole → paper)", -40, -150, 60),
    (BOX_D, CY, -WALL_T,
     "GREY TAPE\n(joins the boxes)", -50, 130, -80),
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
        ov.component("Junction walls (panel frame)", "Boxes", internal_walls()),
        ov.component("Camera-box top (taped shut)", "Boxes", camera_top()),
        ov.component("End wall + arm sleeves", "Boxes", end_wall()),
        ov.component("Box-join tape", "Boxes", join_tape()),
        ov.component("Pinhole", "Pinhole", pinhole_parts()),
    ])
    tags_ruby = '\n'.join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    hardware = ["Boxes", "Pinhole", "Shutter", "Film Panel", "Prep Top Flaps"]
    scenes = [("Assembled", hardware + ["Light Cone"], None, 0),
              ("No light cone", hardware, None, 0),
              ("Labeled", hardware + ["Light Cone", "Labels"], None, 0)]

    def slit(s):
        name, tags, tgt, so = s
        tg = '[' + ', '.join(f'"{t}"' for t in tags) + ']'
        cam = 'nil' if tgt is None else f'[{ov.mm(tgt[0])}, {ov.mm(tgt[1])}, {ov.mm(tgt[2])}]'
        return f'["{name}", {tg}, {cam}, {so}]'
    scenes_ruby = '[' + ', '.join(slit(s) for s in scenes) + ']'

    sf_meta = ov.sketchfab_meta_ruby(
        "TBS-002",
        "A classroom-ready design for teaching pinhole photography — its process and its craft "
        "— to students from elementary school through college.",
        ov.model_uid("mini-tbs"), "sketchup")

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

{sf_meta}
{tags_ruby}

{body}

# ── Clickable dynamic components ──
{shutter_dc()}
{panel_dc()}
{prep_top_flaps_dc()}

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
model.layers["Labels"].visible = false

model.commit_operation

# Register the DCs AFTER committing (redraw_with_undo opens its own operation).
if defined?($dc_observers) && $dc_observers.respond_to?(:get_latest_class)
  cls = $dc_observers.get_latest_class
  [sh_inst, fp_inst, pt_inst].each {{ |di| cls.redraw_with_undo(di) rescue nil }} if cls
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
