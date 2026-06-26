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
    """Pinhole wall + a FULL-depth floor/ceiling (so the full IBC tanks sit on it), with
    a faint marker line at the 300mm-past-walkway depth for reference."""
    bx, bw = WALL_X0, WALL_X1 - WALL_X0          # the FULL pinhole wall length
    p = []
    p.append(ov.ruby_box("Pinhole wall", bx, -ov.WALL_T, 0, bw, ov.WALL_T, C_HGT,
                         color=ov.C_SHELL, alpha=0.30))
    p.append(ov.ruby_box("Floor", bx, 0, -ov.WALL_T, bw, C_WID, ov.WALL_T,
                         color=ov.C_SHELL, alpha=0.16))
    p.append(ov.ruby_box("Ceiling", bx, 0, C_HGT, bw, C_WID, ov.WALL_T,
                         color=ov.C_SHELL, alpha=0.08))
    # faint reference line at the 300mm-past-walkway depth
    p.append(ov.ruby_box("Depth ref (Yd %d)" % VIEW_DEPTH, bx, VIEW_DEPTH - 2, 0, bw, 4, C_HGT,
                         color="#2060A0", alpha=0.10))
    return "\n".join(p)


def walkway_full():
    """Real walkway geometry so the cantilevers + brackets read: perimeter decks
    (near with punch-out, stopping at the IBC; left; right — FAR deck erased post-build),
    the wall gusset brackets, and the IBC-end cantilever arms."""
    p = []
    for fn in ("walkways", "walkway_brackets", "ibc_cantilever_arms"):
        try:
            r = getattr(ov, fn)()
            p.append("\n".join(r) if isinstance(r, (list, tuple)) else r)
        except Exception as e:
            print(f"  (skip {fn}: {e})", file=sys.stderr)
    return "\n".join(p)


def film_plane_beams():
    """The four corner SUPPORT BEAMS (40x40 rails) the film plane runs on (each spanning
    the full depth in Yd), plus the 8 wall-seat SADDLE BRACKETS that secure each rail end
    to the container shell."""
    rail = 40
    z_bot = ov.RAIL_OFF_BOT
    z_top = ov.C_HGT - ov.RAIL_OFF - rail
    x_left, x_right = ov.RAIL_X_L, ov.RAIL_X_R - rail
    p = []
    for nm, x in (("L", x_left), ("R", x_right)):
        for zl, rz in (("bot", z_bot), ("top", z_top)):
            p.append(ov.ruby_box(f"FP support beam {nm}-{zl}", x, 0, rz, rail, C_WID, rail,
                                 color=ov.C_STEEL))
    corners = {"TL": (x_left, z_top), "TR": (x_right, z_top),
               "BL": (x_left, z_bot), "BR": (x_right, z_bot)}
    p.append(ov.film_plane_saddles(corners))     # all 8 wall-seat saddle brackets
    return "\n".join(p)


def deck():
    """Near walkway along the pinhole wall — STOPS at the IBC (does not pass it), with
    its punch-out (widened to WALKWAY_NEAR_WIDE_W over X1155-2629)."""
    p = []
    p.append(ov.ruby_box("Near walkway (stops at IBC)", WALL_X0, 0, DECK_Z - 15,
                         ov.IBC_COL_X - WALL_X0, DECK_W, 15, color=C_DECK, alpha=0.9))
    p.append(ov.ruby_box("Near walkway punch-out", ov.WALKWAY_NEAR_WIDE_X_L, DECK_W, DECK_Z - 15,
                         ov.WALKWAY_NEAR_WIDE_X_R - ov.WALKWAY_NEAR_WIDE_X_L,
                         ov.WALKWAY_NEAR_WIDE_W - DECK_W, 15, color=C_DECK, alpha=0.9))
    return "\n".join(p)


def ibc_slice():
    """A thin slice of the near IBC column at its front face (X=IBC_COL_X) — shows the
    space to the LEFT (high X) is taken, so the wet end can't extend past it."""
    return ov.ruby_box("IBC slice (space taken)", ov.IBC_COL_X, ov.BLUE_IBC_Y, 0,
                       120, VIEW_DEPTH - ov.BLUE_IBC_Y, 2 * ov.IBC_H_1000,
                       color=ov.C_IBC_BLUE, alpha=0.30)


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


def _arm(nm, cx, cy, cz, axis, sd, body, L, r, color):
    """One port stub of a fitting — a cylinder from the body face outward along an axis."""
    if axis == "x":
        x0 = cx + body / 2 if sd > 0 else cx - body / 2 - L
        return ov.ruby_cylinder(nm, x0, cy, cz, r, L, color=color, axis="x")
    if axis == "y":
        y0 = cy + body / 2 if sd > 0 else cy - body / 2 - L
        return ov.ruby_cylinder(nm, cx, y0, cz, r, L, color=color, axis="y")
    z0 = cz + body / 2 if sd > 0 else cz - body / 2 - L
    return ov.ruby_cylinder(nm, cx, cy, z0, r, L, color=color, axis="z")


C_HANDLE = "#C0202A"   # red diverter handle


def diverter(name, cx, cy, cz, run="x", branch="z-", color=None, L=55, r=13):
    """3-way diverter = a standard T-port valve (3 coplanar ports, handle perpendicular)
    rotated onto a VERTICAL WALL: the 3 pipes lie in the wall plane (seen face-on as a T),
    and the RED handle projects out of the wall (+Yd) toward the operator.  `run` is the
    through-run axis (both ways); `branch` is the divert port as axis+sign, default 'z-'
    (exits the UNDERSIDE).  Valve body kept yellow (color defaults to C_VALVE)."""
    color = color or ov.C_VALVE
    body = 46
    ba, bs = branch[0], (+1 if "+" in branch else -1)
    p = [ov.ruby_box(f"{name} body", cx - body / 2, cy - body / 2, cz - body / 2, body, body, body, color=color)]
    p.append(_arm(f"{name} run +", cx, cy, cz, run, +1, body, L, r, color))
    p.append(_arm(f"{name} run -", cx, cy, cz, run, -1, body, L, r, color))
    p.append(_arm(f"{name} branch", cx, cy, cz, ba, bs, body, L, r, color))
    # RED handle out of the wall plane (+Yd, toward the operator), with a lever bar along the run
    hy = cy + body / 2
    p.append(ov.ruby_cylinder(f"{name} handle stem", cx, hy, cz, 6, 42, color=C_HANDLE, axis="y"))
    p.append(ov.ruby_box(f"{name} handle lever", cx - 32, hy + 38, cz - 7, 64, 16, 14, color=C_HANDLE))
    return "\n".join(p)


def kit():
    """Pinhole-wall FILTER sub-loop (Stage B, agreed labels).  Chain:
    IBC-3 (Brown buffer) → P-02 → F1 → F2 → F3 → SV-01 (sample) → DV-01 → Blue/Grey IBC.
    Mounted HIGH so the walkway stays clear; PUMP on the side FURTHEST from the IBCs
    (low X); FILTERS shifted toward the IBCs (high X); SV-01 + DV-01 dropped to WAIST for
    easy reach.  Plumbing orthogonal, perpendicular port stubs, routed around the bodies."""
    p = []
    fr = ov.BB_OD / 2          # 92
    BB_H, cap_h = ov.BB_H, 78
    f_top = C_HGT - 48
    f_bot = f_top - BB_H       # 2000 — the high tier
    fcy = fr + 12              # 104 — filter center Yd (sump back near the wall)
    cap_z = f_bot + BB_H - cap_h / 2   # 2301 — filter cap port centerline
    tie = cap_z - 40           # 2261 — filter port tie-in (bottom of the down-elbow)
    rp = ov.PUMP_PIPE_OD / 2   # 10.5
    yL, yS = 230, 295          # feed lane / suction+exit lane (clear of the bodies, Yd ≤ 196)
    waist = 1000               # SV-01 + DV-01 reach height
    cdk = "#222228"

    FX = {"F1": 3300, "F2": 3700, "F3": 4100}                      # filters shifted toward the IBC
    def f_in(nm):  return (FX[nm] - (fr + 30), fcy, tie)           # IN  port (−X)
    def f_out(nm): return (FX[nm] + (fr + 30), fcy, tie)           # OUT port (+X)

    # ── 3 Big Blue filters — F1 50µm / F2 KDF-55 / F3 GAC; in-line ±X 'T' ports, stub→down ──
    for nm, fx in FX.items():
        p.append(ov.ruby_cylinder(f"Filter {nm} sump", fx, fcy, f_bot, fr, BB_H - cap_h, color=ov.C_FILTER))
        p.append(ov.ruby_cylinder(f"Filter {nm} cap", fx, fcy, f_bot + BB_H - cap_h, fr + 3, cap_h, color=cdk))
        for tag, sd in (("in", -1), ("out", +1)):
            p.append(ov.ruby_pipe_run(f"Filter {nm} {tag} port",
                [(fx + sd * (fr - 6), fcy, cap_z), (fx + sd * (fr + 30), fcy, cap_z),
                 (fx + sd * (fr + 30), fcy, tie)], rp, color=cdk))
        p.append(ov.ruby_cylinder(f"Filter {nm} PR button", fx, fcy, f_bot + BB_H, 6, 9, color=ov.C_STEEL))

    # ── P-02 — far side from the IBCs (low X), filter level; head faces +Yd, ports come DOWN ──
    p2x = 2860
    can_r, can_h, hh = 50, 178, 40
    p.append(ov.ruby_cylinder("Pump P-02 body", p2x, 12 + can_r, f_bot, can_r, can_h, color=ov.C_PUMP))
    p.append(ov.ruby_box("Pump P-02 head", p2x - 57, 12, f_bot + can_h, 114, 100, hh, color=cdk))
    p2_pz = f_bot + 218 - 25                                       # 2193
    def p2_port(sd):  return (p2x + sd * 30, 142, p2_pz - 40)
    for tag, sd in (("in", -1), ("out", +1)):
        p.append(ov.ruby_pipe_run(f"Pump P-02 {tag} port",
            [(p2x + sd * 30, 100, p2_pz), (p2x + sd * 30, 142, p2_pz), (p2x + sd * 30, 142, p2_pz - 40)],
            rp, color=cdk))

    # ── SV-01 sample tap + flat-T 3W-DV-01, dropped to WAIST level (easy reach) ──
    svx, dvx = 4250, 4430
    p.append(ov.ruby_box("SV-01 sample valve", svx - 25, yL - 25, waist - 25, 50, 50, 70, color=ov.C_VALVE))
    p.append(ov.ruby_cylinder("SV-01 sample spout", svx, yL, waist - 25 - 90, 6, 90, color=ov.C_VALVE))
    p.append(diverter("3W-DV-01", dvx, yL, waist, run="x", branch="z-", color=ov.C_VALVE))

    # ── PLUMBING ──
    def pipe(nm, wp, col): p.append(ov.ruby_pipe_run(nm, wp, rp, color=col))
    fz = p2_pz - 40                                                # 2153 — pump-port feed height
    # 1. IBC-3 (Brown buffer) suction → P-02 inlet (long run from the stack, on the suction lane)
    pipe("IBC-3 (Brown) -> P-02 inlet",
         [(ov.IBC_COL_X + 80, yS, fz), (p2_port(-1)[0], yS, fz), (p2_port(-1)[0], yL, fz), p2_port(-1)],
         ov.C_IBC_BROWN)
    # 2. P-02 outlet → F1 inlet
    pipe("P-02 -> F1",
         [p2_port(1), (p2_port(1)[0], yL, fz), (f_in("F1")[0], yL, fz), (f_in("F1")[0], yL, tie), f_in("F1")],
         ov.C_IBC_BROWN)
    # 3. filter jumpers F1→F2→F3 (around the bodies)
    for a, b in (("F1", "F2"), ("F2", "F3")):
        pipe(f"{a} out -> {b} in",
             [f_out(a), (f_out(a)[0], yL, tie), (f_in(b)[0], yL, tie), f_in(b)], ov.C_IBC_BROWN)
    # 4. F3 outlet → DOWN to SV-01 (waist) → DV-01
    pipe("F3 -> SV-01 (drop to waist)",
         [f_out("F3"), (f_out("F3")[0], yL, tie), (svx, yL, tie), (svx, yL, waist)], ov.C_FILTER)
    pipe("SV-01 -> DV-01", [(svx, yL, waist), (dvx, yL, waist)], ov.C_FILTER)
    # 5. DV-01 → Blue IBC (run +X) + Brown IBC (off the UNDERSIDE branch).  Each enters its
    #    tank near the TOP via the side-entry convention: flange (outside) + 150mm pipe in +
    #    90° elbow + 150mm drop into the tank.
    xf = ov.IBC_COL_X                            # tote front face (X4674)
    def tank_entry(nm, y, z, col):               # check valve + flange + 150 in + elbow + 150 drop
        # check valve on the approach riser — prevents siphon/back-drain out of the IBC
        p.append(ov.ruby_box(nm + " check valve", xf - 22, y - 20, z - 130, 44, 40, 55, color=ov.C_VALVE))
        p.append(ov.ruby_pipe_run(nm + " entry", [(xf, y, z), (xf + 150, y, z), (xf + 150, y, z - 150)], rp, color=col))
        p.append(ov.ruby_cylinder(nm + " flange", xf - 8, y, z, 36, 16, color=ov.C_STEEL, axis="x"))
    # Blue leg → Blue IBC (top tote), near top
    bz = 2 * ov.IBC_H_1000 - 180                 # ~2156 — Blue tote near-top entry
    pipe("DV-01 -> Blue IBC (IBC-2)", [(dvx, yL, waist), (xf, yL, waist), (xf, yL, bz)], ov.C_BLUE)
    tank_entry("Blue IBC (IBC-2)", yL, bz, ov.C_BLUE)
    # Brown leg (off the underside branch) → Brown IBC (bottom tote), near top
    rz = ov.IBC_H_1000 - 80                      # ~1088 — Brown tote near-top entry
    pipe("DV-01 -> Brown IBC (IBC-3)",
         [(dvx, yL, waist), (dvx, yL, 850), (dvx, yL + 45, 850), (xf, yL + 45, 850), (xf, yL + 45, rz)], ov.C_IBC_BROWN)
    tank_entry("Brown IBC (IBC-3)", yL + 45, rz, ov.C_IBC_BROWN)
    return "\n".join(p)


def person():
    # 1.75m scale figure standing ON the near walkway, FACING the IBC totes (+X):
    # depth (front-back) along X, shoulders along Yd.
    px, py = 3050, 150          # on the near walkway deck (Yd 0-300)
    z = DECK_Z
    pp = []
    pp.append(ov.ruby_box("Person legs", px - 100, py - 80, z, 200, 160, 850, color=C_PERSON, alpha=0.55))
    pp.append(ov.ruby_box("Person torso", px - 90, py - 150, z + 850, 180, 300, 600, color=C_PERSON, alpha=0.55))
    pp.append(ov.ruby_cylinder("Person head (scale 1.75m)", px, py, z + 1450, 100, 230, color=C_PERSON, alpha=0.6))
    return "\n".join(pp)


def right_walkway():
    """Partial view of the RIGHT walkway (runs in Yd across the container at X≈4329-4629)
    — only the slice within the limited depth (Yd0..VIEW_DEPTH), for spatial context where
    it passes the wet-end's IBC end."""
    return ov.ruby_box("Right walkway (partial)", ov.WALKWAY_RIGHT_X, 0, DECK_Z - 15,
                       ov.WALKWAY_RIGHT_W, VIEW_DEPTH, 15, color=ov.C_WALKWAY, alpha=0.9)


# ── "Labeled" scene callouts (point-anchored on the kit; instance-anchored on pinhole/elec) ──
LABEL_POINTS = [  # (x, y, z, text, leader dx,dy,dz)  — the pinhole-wall FILTER sub-loop
    (2860, 95, 2218, "P-02\n(filter feed)", 0, 520, 250),
    (3300, 102, 2305, "F1 (50um)",   0, 560, 80),
    (3700, 102, 2305, "F2 (KDF-55)", 0, 560, 80),
    (4100, 102, 2305, "F3 (GAC)",    0, 560, 80),
    (4250, 230, 1000, "SV-01\n(sample)", 0, 430, 520),
    (4430, 230, 1000, "DV-01\n(3-way)",  0, 430, 740),
]
LABEL_INSTANCES = [
    ("Pinhole Assembly", "PINHOLE\n(optical ref)", 0, 700, 350),
    ("Other pinhole-wall equipment", "ELECTRICAL\n(panel/inverter/batteries)", 0, 850, 500),
    ("IBC Tanks (full)", "IBCs\n(space NOT available)", -300, 900, 300),
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
    for name, tag, b in [("Context", "Context", context()),
                         ("Walkways + cantilevers + brackets", "Walkway", walkway_full()),
                         ("Film-plane support beams", "Film Plane", film_plane_beams()),
                         ("IBC Tanks (full)", "IBC", ov.ibc_stack()),
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
# remove the FAR walkway deck AND its cantilever brackets (not wanted in this view)
model.definitions.each {{ |d| d.entities.grep(Sketchup::Group).each {{ |g| g.erase! if g.valid? && g.name =~ /^Walkway Far/ }} }}
# in-model callout labels on the 'Labels' tag (shown only in the Labeled scene)
{labels_ruby()}
v = model.active_view
v.camera = Sketchup::Camera.new(Geom::Point3d.new(800.mm, 6000.mm, 2300.mm), Geom::Point3d.new(2950.mm, 200.mm, 1100.mm), Geom::Vector3d.new(0,0,1), false, 52)
def scene(model, name, on)
  model.layers.each {{ |l| l.visible = (l.name == "Layer0" || l == model.layers[0] || on.include?(l.name)) }}
  pg = model.pages.add(name); pg.use_hidden_layers = true rescue nil; pg
end
scene(model, "Pinhole-wall wet end", ["Context","Walkway","Film Plane","IBC","Pinhole","Kit","Scale"])
scene(model, "Other pinhole-wall equipment", ["Context","Walkway","Film Plane","IBC","Pinhole","Pinhole Equipment"])
scene(model, "Overall", ["Context","Walkway","Film Plane","IBC","Pinhole","Kit","Scale","Pinhole Equipment"])
scene(model, "Labeled", ["Context","Walkway","Film Plane","IBC","Pinhole","Kit","Scale","Pinhole Equipment","Labels"])
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
