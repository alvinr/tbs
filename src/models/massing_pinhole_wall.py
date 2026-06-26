#!/usr/bin/env python3
"""massing_pinhole_wall.py — EXPLORATORY massing (pinhole-wall-mount branch).

Block massing of the wet end (pumps + ACC + filters) wall-mounted on the PINHOLE
WALL (Yd=0) in the clear band X2700-4674, arranged by the RAKE-BY-DEPTH principle:
the deepest items (Big Blue filters) ride HIGH, the shallow items (pumps, ACC) sit
LOW, keeping the torso band clear.  Includes the (widened) near-walkway deck and a
1750mm person for scale.  No plumbing yet — geometry feasibility only.

    python3 src/models/massing_pinhole_wall.py --send   # build in the live SketchUp doc
"""
import sys, os, argparse
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))   # repo root (src/models -> src -> root)
sys.path.insert(0, _HERE)
import generate_sketchup_model as ov

# ── band + wall ──────────────────────────────────────────────────────────────
X0, X1 = 2700, 4674            # wet-end clear mounting band on the pinhole wall (Yd0)
WALL_X0, WALL_X1 = 0, ov.C_LEN # 0..5893 — the FULL pinhole wall (context spans the whole length)
C_HGT, C_WID = ov.C_HGT, ov.C_WID
DECK_Z = ov.WALKWAY_H          # 130
DECK_W = ov.WALKWAY_W          # 300 — standard near walkway (evaluate whether it fits)
VIEW_DEPTH = DECK_W + 300      # 600 — show from the wall out to 300mm PAST the walkway, then stop

C_PERSON = "#806040"
C_DECK   = "#9C7B4D"


def context():
    """Limited-depth context: the pinhole wall + a floor/ceiling slice only as deep as
    300mm past the walkway (Yd0..VIEW_DEPTH).  No deep-container geometry."""
    bx, bw = WALL_X0, WALL_X1 - WALL_X0          # the FULL pinhole wall length
    p = []
    p.append(ov.ruby_box("Pinhole wall", bx, -ov.WALL_T, 0, bw, ov.WALL_T, C_HGT,
                         color=ov.C_SHELL, alpha=0.30))
    p.append(ov.ruby_box("Floor (to 300 past walkway)", bx, 0, -ov.WALL_T, bw, VIEW_DEPTH, ov.WALL_T,
                         color=ov.C_SHELL, alpha=0.16))
    p.append(ov.ruby_box("Ceiling (to 300 past walkway)", bx, 0, C_HGT, bw, VIEW_DEPTH, ov.WALL_T,
                         color=ov.C_SHELL, alpha=0.08))
    # faint cut plane marking the 300mm-past-walkway depth limit
    p.append(ov.ruby_box("Depth limit (Yd %d)" % VIEW_DEPTH, bx, VIEW_DEPTH - 2, 0, bw, 4, C_HGT,
                         color="#2060A0", alpha=0.10))
    return "\n".join(p)


def deck():
    return ov.ruby_box("Near walkway deck", WALL_X0, 0, DECK_Z - 15,
                       WALL_X1 - WALL_X0, DECK_W, 15, color=C_DECK, alpha=0.9)


# Other equipment ALREADY mounted on the pinhole wall (Yd0) — the wet-end layout has to
# coexist with these.  electrical() = panel + inverter + batteries.
OTHER_WALL_EQUIP = [("Electrical (panel/inverter/batteries)", "electrical")]


def other_equipment():
    p = []
    for _label, fn in OTHER_WALL_EQUIP:
        try:
            p.append(getattr(ov, fn)())
        except Exception as e:
            print(f"  (skip {fn}: {e})", file=sys.stderr)
    return "\n".join(p)


def kit():
    p = []
    fr = ov.BB_OD / 2          # 92
    BB_H = ov.BB_H             # 340
    # ── FILTERS — deepest, HIGH (cap-up row near the ceiling); in-line ±X ports chain F1->F2->F3
    f_top = C_HGT - 48         # cap top just under the ceiling
    f_bot = f_top - BB_H       # body bottom ≈ 2000
    for i, fx in enumerate((3120, 3520, 3920)):
        p.append(ov.ruby_cylinder(f"Filter F{i+1} (Ø184)", fx, fr + 10, f_bot, fr, BB_H - 70,
                                  color=ov.C_FILTER))
        p.append(ov.ruby_cylinder(f"Filter F{i+1} cap", fx, fr + 10, f_top - 70, fr + 3, 70,
                                  color="#222228"))
    # ── PUMPS — shallow tier LOW, between ANKLE & KNEE (Z~160-380): heavy water-filled
    # bodies stay low (CG + drip), projection sits below the torso, you step past at
    # lower-leg level.
    pw, pd, ph = ov.PUMP_W, ov.PUMP_YD_SPAN, 218     # 114 x 127 x 218
    pz = 160                                          # body bottom ≈ ankle
    for i, cx in enumerate((2860, 3180, 3500, 3820, 4140)):
        p.append(ov.ruby_box(f"Pump P-0{i+1}", cx - pw / 2, 12, pz, pw, pd, ph, color=ov.C_PUMP))
        p.append(ov.ruby_box(f"Pump P-0{i+1} head", cx - pw / 2, 12, pz + ph, pw, 68, 40,
                             color="#3A3A42"))
    # ── ACC — shallowest, low with the pumps (ankle-knee)
    p.append(ov.ruby_cylinder("ACC-01 (Ø127)", 4430, 127 / 2 + 12, 160, 127 / 2, 200, color=ov.C_ACC))
    return "\n".join(p)


def person():
    # A clearly-human standee for scale (1750 tall) standing on the deck, back to the wall.
    # Stick-ish proportions so it reads as a PERSON, not equipment.
    px, py = 2760, 230
    z = DECK_Z
    pp = []
    # legs
    pp.append(ov.ruby_box("Person legs", px - 80, py, z, 160, 200, 850, color=C_PERSON, alpha=0.55))
    # torso (narrower front-back)
    pp.append(ov.ruby_box("Person torso", px - 150, py + 10, z + 850, 300, 180, 600, color=C_PERSON, alpha=0.55))
    # head
    pp.append(ov.ruby_cylinder("Person head (scale 1.75m)", px, py + 100, z + 1450, 100, 230, color=C_PERSON, alpha=0.6))
    return "\n".join(pp)


def right_walkway():
    """Partial view of the RIGHT walkway (runs in Yd across the container at X≈4329-4629)
    — only the slice within the limited depth (Yd0..VIEW_DEPTH), for spatial context where
    it passes the wet-end's IBC end."""
    return ov.ruby_box("Right walkway (partial)", ov.WALKWAY_RIGHT_X, 0, DECK_Z - 15,
                       ov.WALKWAY_RIGHT_W, VIEW_DEPTH, 15, color=ov.C_WALKWAY, alpha=0.9)


# ── "Labeled" scene callouts (point-anchored on the kit; instance-anchored on pinhole/elec) ──
LABEL_POINTS = [  # (x, y, z, text, leader dx,dy,dz)  — leaders pull +Yd (toward viewer) & up
    (2860, 75, 378, "P-01", 0, 520, 720),
    (3180, 75, 378, "P-02", 0, 520, 980),
    (3500, 75, 378, "P-03", 0, 520, 720),
    (3820, 75, 378, "P-04", 0, 520, 980),
    (4140, 75, 378, "P-05", 0, 520, 720),
    (4430, 75, 360, "ACC-01", 0, 520, 860),
    (3120, 102, 2305, "F1 (50um)", 0, 560, 70),
    (3520, 102, 2305, "F2 (5um)",  0, 560, 70),
    (3920, 102, 2305, "F3 (GAC)",  0, 560, 70),
]
LABEL_INSTANCES = [
    ("Pinhole Assembly", "PINHOLE\n(optical ref)", 0, 700, 350),
    ("Other pinhole-wall equipment", "ELECTRICAL\n(panel/inverter/batteries)", 0, 850, 500),
]


def labels_ruby():
    rows = []
    for x, y, z, text, dx, dy, dz in LABEL_POINTS:
        rows.append(
            f'anc = Geom::Point3d.new({ov.mm(x)},{ov.mm(y)},{ov.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)},{ov.mm(dy)},{ov.mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    for name, text, dx, dy, dz in LABEL_INSTANCES:
        rows.append(
            f'inst = entities.grep(Sketchup::ComponentInstance).find {{ |i| i.name == "{name}" }}\n'
            f'if inst\n'
            f'  bb = inst.bounds\n'
            f'  anc = Geom::Point3d.new(bb.center.x, bb.min.y, bb.center.z)\n'
            f'  txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)},{ov.mm(dy)},{ov.mm(dz)}))\n'
            f'  txt.layer = model.layers["Labels"] rescue nil\n'
            f'end')
    return '\n'.join(rows)


def build():
    # Limited-depth view of the FULL pinhole wall: the wet-end kit + the OTHER wall-mounted
    # equipment (own layer/scene) + a shallow context slice (wall + floor/ceiling out to
    # 300mm past the walkway) + scale figure.  Two scenes: wet end / other equipment.
    comps, tags = [], set()
    for name, tag, b in [("Context (limited depth)", "Context", context()),
                         ("Near walkway deck", "Deck", deck()),
                         ("Right walkway (partial)", "Walkway", right_walkway()),
                         ("Pinhole Assembly", "Pinhole", ov.pinhole_assembly()),
                         ("Wet-end kit (raked)", "Kit", kit()),
                         ("Person (scale)", "Scale", person()),
                         ("Other pinhole-wall equipment", "Pinhole Equipment", other_equipment())]:
        comps.append(ov.component(name, tag, b)); tags.add(tag)
    tags.add("Labels")
    body = "\n".join(comps)
    tags_ruby = "".join(f'  model.layers.add({t!r}) unless model.layers[{t!r}]\n' for t in sorted(tags))
    return f'''model = Sketchup.active_model
model.start_operation("Pinhole-wall layout", true)
entities = model.active_entities
to_erase = entities.to_a.select {{ |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |pg| model.pages.erase(pg) }}
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0
{tags_ruby}{body}
# in-model callout labels on the 'Labels' tag (shown only in the Labeled scene)
{labels_ruby()}
v = model.active_view
v.camera = Sketchup::Camera.new(Geom::Point3d.new(800.mm, 6000.mm, 2300.mm), Geom::Point3d.new(2950.mm, 200.mm, 1100.mm), Geom::Vector3d.new(0,0,1), false, 52)
def scene(model, name, on)
  model.layers.each {{ |l| l.visible = (l.name == "Layer0" || l == model.layers[0] || on.include?(l.name)) }}
  pg = model.pages.add(name); pg.use_hidden_layers = true rescue nil; pg
end
WET = ["Context","Deck","Walkway","Pinhole","Kit","Scale"]
scene(model, "Pinhole-wall wet end", WET)
scene(model, "Other pinhole-wall equipment", ["Context","Deck","Walkway","Pinhole","Pinhole Equipment"])
scene(model, "Overall", ["Context","Deck","Walkway","Pinhole","Kit","Scale","Pinhole Equipment"])
scene(model, "Labeled", ["Context","Deck","Walkway","Pinhole","Kit","Scale","Pinhole Equipment","Labels"])
model.layers.each {{ |l| l.visible = true }}
model.commit_operation
{{ ok: true }}.to_json
'''


SKP_PATH = os.path.abspath(os.path.join(_ROOT, "models", "pinhole-wall.skp"))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true", help="build into the ACTIVE SketchUp doc (open a blank doc first!)")
    ap.add_argument("--save", action="store_true", help="after building, save the active doc as models/pinhole-wall.skp")
    a = ap.parse_args()
    ruby = build()
    if a.send:
        from sketchup_client import send_ruby
        print(send_ruby(ruby))
        if a.save:
            print(send_ruby(f'Sketchup.active_model.save({SKP_PATH!r}) ? "saved {SKP_PATH}" : "FAIL"'))
    else:
        print(ruby[:400])
