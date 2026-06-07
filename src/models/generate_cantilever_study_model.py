"""generate_cantilever_study_model.py — TBS-001 LEFT-walkway cantilever clearance study.

A focused, throw-away-able STUDY model (not yet a cascaded design) to work through
replacing the left removable walkway's deflecting full-width edge beam with a row of
FLOOR-ROOTED CANTILEVER BRACKETS, and to prove the clearances the redesign must respect:

  • floor legs bolted OUTSIDE the tray (X<170 = bare floor — no tray/lip penetration);
  • cantilever arms carrying the grate inner edge at X=470, depth-limited to Z52–65
    (spray bar sweeps Z20–60 below, grate sits Z65–80 above);
  • the drum-exit PUNCH-OUT (X470–770) — the "wider section" — sits OVER the open tray
    + spray-bar sweep, so it can only be a cantilevered grate extension (no support below);
  • the hinge light-trap PANEL sliding to its transport position (X+880, riding Z80) must
    clear every permanent bracket (tops at Z65 → 15mm gap), with the grate lifted out;
  • the film plane (all Z≥100) travels above everything (brackets top at Z65 → 35mm).

Standing rules encoded: can't penetrate the tray or its lip; can't block the panel in
transport; can't block the film-plane travel; the grate is a one-person lift-out.

Reuses generate_sketchup_model (`ov`) helpers + constants. Mirrors the IBC model scaffold
(component-per-tag, shared iso camera, scene-toggled tags). NOT a Dynamic Component — the
panel is shown statically at its transport position plus a faded swept-path envelope.

Usage:
    python3 src/models/generate_cantilever_study_model.py --save        # write the .rb
    python3 src/models/generate_cantilever_study_model.py --save --send # + send to ACTIVE doc
NOTE: --send clears the ACTIVE SketchUp document. Open a BLANK doc first, then save as
models/cantilever-study.skp.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov   # helpers + colors + most constants (Overview)
import tbs_constants as k              # constants ov doesn't re-export

# ── Walkway / grate ──
WK_LX, WK_W = ov.WALKWAY_LEFT_X, ov.WALKWAY_W          # 170, 300
GRATE_T = ov.WALKWAY_GRATE_T                           # 15
GRATE_Z = ov.WALKWAY_H - GRATE_T                       # 65 — grate bottom (= bracket-arm top)
C_WID = ov.C_WID                                       # 2362
INNER_X = WK_LX + WK_W                                 # 470 — grate inner edge / open-tray edge
WIDE_W = ov.WALKWAY_LEFT_WIDE_W                        # 600
WIDE_YL, WIDE_YR = ov.WALKWAY_LEFT_WIDE_YD_L, ov.WALKWAY_LEFT_WIDE_YD_R  # 800, 1560
PUNCH_X = WK_LX + WIDE_W                               # 770 — punch-out inner edge (over the tray)

# ── Processing tray / spray bar ──
TRAY_XL = ov.PROC_TRAY_X_L                             # 170
TRAY_YN, TRAY_YF = ov.PROC_TRAY_YD_NEAR, ov.PROC_TRAY_YD_FAR  # 80, 2280
RIM = ov.PROC_TRAY_RIM                                 # 50
OPEN_XL = k.PROC_OPEN_X_L                              # 470 — spray-bar sweep starts here
SB_ZB, SB_ZT, SB_BEAM = ov.SPRAY_BAR_Z_BOT, k.SPRAY_BAR_Z_TOP, ov.SPRAY_BAR_BEAM  # 20,60,40
SB_WHEEL = k.SPRAY_BAR_WHEEL_DIA                       # 50
SB_AXLE = k.SPRAY_BAR_AXLE_Z                           # 27 — wheel axle Z

# ── Hinge panel (light-trap) transport position ──
PANEL_GAP = ov.PANEL_FLOOR_GAP                         # 80 — panel rides this far off the floor
PANEL_ZTOP = 2300                                      # matches lighttrap PANEL_Z_TOP
PANEL_CT, PANEL_KT = k.PANEL_CORNER_T, ov.PANEL_CENTER_T   # 40, 120
PANEL_YL, PANEL_YR = ov.PANEL_CORNER_YD_L, ov.PANEL_CORNER_YD_R  # 653, 1709
SLIDE = ov.PANEL_SLIDE                                 # 880 — transport slide travel

# ── Film-plane left rail envelope ──
RAIL_XL = ov.RAIL_X_L                                  # 150
BRACE_ZB, BRACE_ZT = ov.BRACE_Z_BOT, ov.BRACE_Z_TOP   # 100, 2288

# ── Study extents + cantilever-bracket dimensions (STUDY values; cascade later if approved) ──
PARTIAL_X = ov.PROC_TRAY_X_R   # 4629 — full tray length (= far rim); spray bar spans lip-to-lip
LEG_X = WK_LX - 30         # 140 — floor leg centreline (bare floor, outside tray X=170)
# Leg layout (Yd): 3 land on the punch-out (800/1180/1560) to support the widened
# section via EXTENDED arms; the 2 outers give ~550mm max clear span for the grate.
LEG_YDS = [250, 800, 1180, 1560, 2110]
SB_END_GAP = 25            # carriage-to-tray-lip clearance (beam stops short of the rim wall)
POST = 50                  # 50×50 SHS leg/post section (mm)
BW = 60                    # bracket Yd width (mm)
FOOT_X0, FOOT_X1, FOOT_T = 38, 166, 8   # foot plate X span (all < 170) + thickness

C_CANT = "#C8781E"         # cantilever brackets — distinct accent
C_SWEEP = "#3070C0"        # panel swept-path envelope (faded blue)

# ── WALKWAY RAISE under evaluation — lift the whole walkway + brackets + panel + drum ──
RAISE = 50                          # mm — walkway lift being studied
GZ = GRATE_Z + RAISE                # 115 — raised grate bottom (= bracket-arm top)
ARM_ZB2 = SB_ZT + 15                # 75 — arm bottom: 15mm above the spray bar top (comfortable clearance)
PANEL_Z0R = PANEL_GAP + RAISE       # 130 — panel floor gap, lifted with the walkway
PANEL_Z1R = PANEL_ZTOP + RAISE      # 2350 — panel top (lifted → panel height preserved)
FILM_B2 = BRACE_ZB + RAISE          # 150 — film bottom, lifted to keep its 20mm walkway margin
# Light-trap drum — LIFTED by RAISE so its interior height is preserved (not reduced).
DRUM_CX, DRUM_CY, DRUM_R = ov.DRUM_CX, ov.DRUM_CY, ov.DRUM_R  # -400, 1181, 450
BAY_X0 = ov.BAY_FRONT_X             # -890 — bay outer face (so the drum reads under the ceiling)
DRUM_Z0 = PANEL_GAP + RAISE         # 130 — drum bottom (lifted)
DRUM_Z1 = ov.DRUM_H_LT + RAISE      # 2250 — drum top (lifted; door-aperture top = C_HGT 2388)

TAGS = ["Context", "Processing Tray", "Film Plane Rails", "Spray Bar",
        "Cantilevers", "Grate (lift-out)", "Hinge Panel (transport)",
        "Light-trap Drum", "Labels"]


# ── Geometry builders ────────────────────────────────────────────────────────

def context():
    """Low-alpha container stub at the cargo-door end. Floor + ceiling extend out
    over the bay (X BAY_X0..PARTIAL_X) so the lifted drum reads under the door-
    aperture-height ceiling (showing the spare to Z=C_HGT)."""
    t = ov.WALL_T
    xl = PARTIAL_X - BAY_X0
    return '\n'.join([
        ov.ruby_box("Floor (context)", BAY_X0, 0, -t, xl, C_WID, t,
                    color=ov.C_SHELL, alpha=0.25),
        ov.ruby_box("Ceiling / aperture top (context)", BAY_X0, 0, ov.C_HGT, xl, C_WID, t,
                    color=ov.C_SHELL, alpha=0.08),
        ov.ruby_box("Side Wall near (context)", 0, -t, 0, PARTIAL_X, t, ov.C_HGT,
                    color=ov.C_SHELL, alpha=0.14),
        ov.ruby_box("Side Wall far (context)", 0, C_WID, 0, PARTIAL_X, t, ov.C_HGT,
                    color=ov.C_SHELL, alpha=0.14),
        ov.ruby_box("Door plane (context)", -t, 0, 0, t, C_WID, ov.C_HGT,
                    color=ov.C_SHELL, alpha=0.10),
    ])


def tray_partial():
    """Processing tray (floor + rims + bath), cropped to X TRAY_XL..PARTIAL_X."""
    s = 2
    w = PARTIAL_X - TRAY_XL
    d = TRAY_YF - TRAY_YN
    return '\n'.join([
        ov.ruby_box("Processing Tray Floor", TRAY_XL, TRAY_YN, 0, w, d, s, color=ov.C_TRAY),
        ov.ruby_box("Tray Rim Near", TRAY_XL, TRAY_YN, s, w, s, RIM - s, color=ov.C_TRAY),
        ov.ruby_box("Tray Rim Far", TRAY_XL, TRAY_YF - s, s, w, s, RIM - s, color=ov.C_TRAY),
        ov.ruby_box("Tray Rim Left", TRAY_XL, TRAY_YN, s, s, d, RIM - s, color=ov.C_TRAY),
        ov.ruby_box("Tray Rim Right", PARTIAL_X - s, TRAY_YN, s, s, d, RIM - s, color=ov.C_TRAY),
        ov.ruby_box("Chemistry Bath", TRAY_XL + s, TRAY_YN + s, s,
                    w - 2 * s, d - 2 * s, RIM - s - 8, color=ov.C_BATH, alpha=0.40),
    ])


def film_rails():
    """The film-plane LEFT rail + a ghost of the travelling left edge. With the raise
    the film bottom lifts to FILM_B2 (keeping its 20mm walkway margin) — the cost in
    image height the lift buys."""
    return '\n'.join([
        ov.ruby_box("Film rail left (bottom, Yd-run)", RAIL_XL, TRAY_YN, FILM_B2,
                    40, TRAY_YF - TRAY_YN, 40, color=ov.C_RAIL),
        ov.ruby_box("Film plane left edge (ghost)", RAIL_XL, 600, FILM_B2,
                    12, 1162, BRACE_ZT - FILM_B2, color=ov.C_RAIL, alpha=0.18),
    ])


def grate():
    """Left removable walkway grate (X170–470, full Yd) + drum-exit punch-out
    (X470–770, Yd 800–1560) — the lift-out, removed for transport."""
    return '\n'.join([
        ov.ruby_box("Walkway Left (removable)", WK_LX, 0, GZ,
                    WK_W, C_WID, GRATE_T, color=ov.C_REMOVABLE),
        ov.ruby_box("Walkway Left punch-out (on extended arms)", INNER_X, WIDE_YL, GZ,
                    PUNCH_X - INNER_X, WIDE_YR - WIDE_YL, GRATE_T, color=ov.C_REMOVABLE),
    ])


def _bracket(i, y, reach):
    """One floor-rooted cantilever bracket at Yd=y: foot plate (bare floor) + post
    (X≈140, Z0→raised grate bottom) + arm (Z75–115, 40mm deep, 15mm above the spray
    bar) reaching to `reach`. Standard arms stop at the grate inner edge (X=470);
    punch-out arms EXTEND to X=770 (the widened section) — possible only because the
    raise lifted the arm clear of the spray bar, so it can pass over the open tray."""
    wide = reach > INNER_X
    aw = 60 if wide else 40          # widened arm runs a bit beefier in Yd
    arm_x0 = LEG_X + POST / 2
    return '\n'.join([
        ov.ruby_box(f"Cantilever {i} foot plate", FOOT_X0, y - BW / 2, 0,
                    FOOT_X1 - FOOT_X0, BW, FOOT_T, color=ov.C_STEEL),
        ov.ruby_box(f"Cantilever {i} post (50x50 SHS)", LEG_X - POST / 2, y - BW / 2, 0,
                    POST, BW, GZ, color=C_CANT),
        ov.ruby_box(f"Cantilever {i} arm (to X{int(reach)}{' WIDENED' if wide else ''})",
                    arm_x0, y - aw / 2, ARM_ZB2, reach - arm_x0, aw, GZ - ARM_ZB2, color=C_CANT),
    ])


def cantilevers():
    """Floor-rooted cantilever brackets at LEG_YDS. Standard brackets carry the grate
    inner edge (X=470); brackets landing on the punch-out (Yd 800–1560) get EXTENDED
    arms to X=770 so the widened section is supported, not cantilevered."""
    parts = []
    for i, y in enumerate(LEG_YDS, 1):
        reach = PUNCH_X if WIDE_YL <= y <= WIDE_YR else INNER_X
        parts.append(_bracket(i, y, reach))
    return '\n'.join(parts)


def spray_bar():
    """Spray-bar beam at a representative Yd (drum centre, in the punch-out). The carriage
    wheels ride the tray RIM rails, so the beam spans LIP-to-LIP — X170→4629 (tray rim to
    tray rim) — passing UNDER the left walkway to wash the full film width. Z20–60, with a
    wheel riding each rim rail."""
    y = (WIDE_YL + WIDE_YR) // 2   # 1180 ~ drum centre
    x0 = TRAY_XL + 2 + SB_END_GAP            # carriage stops SB_END_GAP short of the rim wall
    x1 = (PARTIAL_X - 2) - SB_END_GAP
    return '\n'.join([
        ov.ruby_box("Spray Bar beam (40x40, Z20-60)", x0, y - SB_BEAM / 2, SB_ZB,
                    x1 - x0, SB_BEAM, SB_BEAM, color=ov.C_ALUM),
        ov.ruby_cylinder("Spray Bar wheel (left)", x0, y - SB_BEAM / 2 - 10,
                         SB_AXLE, SB_WHEEL / 2, 20, axis="y", color=ov.C_STEEL),
        ov.ruby_cylinder("Spray Bar wheel (right)", x1, y - SB_BEAM / 2 - 10,
                         SB_AXLE, SB_WHEEL / 2, 20, axis="y", color=ov.C_STEEL),
    ])


def panel_transport():
    """The stepped hinge panel at its TRANSPORT position (slid +SLIDE). Lifted with
    the walkway (rides PANEL_Z0R = floor-gap+RAISE) so it still clears the raised
    bracket tops by the same 15mm. Corner zones 40mm, centre 120mm. Faded swept-path
    band shows the clearance strip."""
    z0, h = PANEL_Z0R, PANEL_Z1R - PANEL_Z0R
    return '\n'.join([
        ov.ruby_box("Panel corner near (40mm)", SLIDE, 0, z0,
                    PANEL_CT, PANEL_YL, h, color=ov.C_PLY),
        ov.ruby_box("Panel centre (120mm)", SLIDE, PANEL_YL, z0,
                    PANEL_KT, PANEL_YR - PANEL_YL, h, color=ov.C_PLY),
        ov.ruby_box("Panel corner far (40mm)", SLIDE, PANEL_YR, z0,
                    PANEL_CT, C_WID - PANEL_YR, h, color=ov.C_PLY),
        ov.ruby_box("Panel swept path (clearance band)", 0, 0, z0,
                    SLIDE + PANEL_KT, C_WID, 60, color=C_SWEEP, alpha=0.12),
    ])


def drum():
    """Light-trap drum LIFTED by RAISE (top Z2250) so its interior standing height is
    PRESERVED (not reduced). Shown under the door-aperture-height ceiling (C_HGT 2388)
    so the remaining spare (~138mm) reads. Translucent cylinder + a base disc."""
    return '\n'.join([
        ov.ruby_cylinder("Light-trap drum (lifted +%dmm)" % RAISE,
                         DRUM_CX, DRUM_CY, DRUM_Z0, DRUM_R, DRUM_Z1 - DRUM_Z0,
                         axis="z", color=ov.C_DRUM, alpha=0.30),
        ov.ruby_cylinder("Drum base disc", DRUM_CX, DRUM_CY, DRUM_Z0, DRUM_R, 12,
                         axis="z", color=ov.C_STEEL),
    ])


# ── "Labeled" scene callouts (project rule) — reflect the +RAISE state ──
POINT_LABELS = [
    (LEG_X, 197, GZ, "FLOOR-LEG CANTILEVER\nbolted to bare floor (X<170,\noutside tray) — replaces edge beam",
     -700, -700, 500),
    (INNER_X, 984, ARM_ZB2, "ARM 40mm deep (was 13)\nbottom Z75 clears spray bar (Z60) by 15mm",
     520, -650, 320),
    (PUNCH_X, 1180, GZ, "PUNCH-OUT now SUPPORTED:\nextended arm to X770 (Z75-115)\nover the spray bar (15mm clear)",
     650, -300, 450),
    (OPEN_XL, 1180, SB_ZT, "SPRAY BAR fixed at Z20-60\n(does NOT rise) — gap opens up",
     -300, 600, -250),
    (SLIDE + PANEL_KT, 1180, PANEL_Z0R, "PANEL lifted +%dmm (rides Z%d)\nstill clears brackets by 15mm" % (RAISE, PANEL_Z0R),
     500, -500, 700),
    (DRUM_CX, DRUM_CY, DRUM_Z1, "DRUM LIFTED +%dmm -> top Z%d\ninterior height PRESERVED;\n%dmm spare to aperture top" % (RAISE, DRUM_Z1, ov.C_HGT - DRUM_Z1),
     -300, -250, 250),
]


def labels():
    rows = []
    for x, y, z, text, dx, dy, dz in POINT_LABELS:
        rows.append(
            f'anc = Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    return '\n'.join(rows)


def generate_ruby():
    comps = [
        ov.component("Container (ghost)", "Context", context()),
        ov.component("Processing Tray (partial)", "Processing Tray", tray_partial()),
        ov.component("Film-Plane Rails (left)", "Film Plane Rails", film_rails()),
        ov.component("Spray Bar (at drum Yd)", "Spray Bar", spray_bar()),
        ov.component("Cantilever Brackets", "Cantilevers", cantilevers()),
        ov.component("Grate (lift-out)", "Grate (lift-out)", grate()),
        ov.component("Hinge Panel (transport)", "Hinge Panel (transport)", panel_transport()),
        ov.component("Light-trap Drum (lifted)", "Light-trap Drum", drum()),
    ]
    body = '\n'.join(comps)

    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    comp_tags = [t for t in TAGS if t != "Labels"]
    scenes = [
        # Operating: walkway raised on the cantilevers, spray bar + film rails; panel out.
        ("Operating", ["Processing Tray", "Film Plane Rails", "Spray Bar",
                       "Cantilevers", "Grate (lift-out)"]),
        # Transport: grate lifted out, panel + drum lifted — show clearances hold.
        ("Transport clearance", ["Processing Tray", "Film Plane Rails",
                                 "Cantilevers", "Hinge Panel (transport)", "Light-trap Drum"]),
        # Spray-bar clearance — the gap the raise opens up under the grate.
        ("Spray-bar clearance", ["Processing Tray", "Spray Bar",
                                 "Cantilevers", "Grate (lift-out)"]),
        # Drum lift — interior height preserved, spare to the aperture top.
        ("Drum lift", ["Processing Tray", "Cantilevers", "Hinge Panel (transport)",
                       "Light-trap Drum"]),
        ("Combined", comp_tags),
        ("Labeled", TAGS),
    ]
    scenes_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags))
        for n, tags in scenes) + ']'

    return f'''model = Sketchup.active_model
# Clear pages BEFORE start_operation — erase applies immediately here (inside an
# operation it is deferred, so a count-loop would spin forever). Bounded to_a.each.
model.pages.to_a.each {{ |p| model.pages.erase(p) }}
model.start_operation("TBS-001 Cantilever Study", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild.
to_erase = entities.to_a.select {{ |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused

# ── Tags ──
{tags_ruby}

# ── Subsystems ──
{body}

# ── Labels (Labels tag; visible only in "Labeled") ──
{labels()}

model.definitions.purge_unused
model.materials.purge_unused

keep_tags = {keep_tags_ruby}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

# ── Scenes — shared iso camera framed on the CARGO-DOOR END (the study focus). The
# tray + spray bar now run the full length toward the IBC end, so a bounds/zoom_extents
# camera would shrink the detail; use a fixed cargo-door-end framing instead. ──
model.layers.each {{ |l| l.visible = (l.name != "Labels") }}
ctr = Geom::Point3d.new(700.mm, 1100.mm, 500.mm)
dir = Geom::Vector3d.new(0.58, -0.80, 0.48); dir.normalize!
eye = ctr.offset(dir, 4600.mm)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)

{scenes_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }}
  page = model.pages.add(name)
  page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}

model.commit_operation
{{ success: true, model: "Cantilever Study",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate the TBS-001 left-walkway cantilever clearance study model")
    parser.add_argument("--save", action="store_true",
                        help="Write Ruby to src/models/cantilever-study.rb")
    parser.add_argument("--send", action="store_true",
                        help="Send to the ACTIVE SketchUp doc (clears it — open a BLANK doc first)")
    args = parser.parse_args()

    ruby = generate_ruby()

    if args.save:
        out = os.path.join(os.path.dirname(__file__), "cantilever-study.rb")
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
