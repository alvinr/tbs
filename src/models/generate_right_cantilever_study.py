#!/usr/bin/env python3
"""STUDY model — right walkway cantilevered off the IBC frame (replaces the ceiling
hangers, which clashed the film plane). Focused on the right-end zone so the new
support can be reviewed in context before it's adopted into the walkway/overview models.

Shows: the IBC stacking frame (the cantilever anchor), the processing-tray right end +
the low spray bar (clearance below), the film-plane right rail + its near/far wall-seat
saddles (clearance the OLD ceiling rods violated), and the new CANTILEVER right walkway —
4 arms reaching 345mm back from the frame face (X4674) to the deck (X4329) at the frame's
Yd uprights (0/1046/1316/2362), 2 longitudinal bearers, and the grate. NO ceiling rods.

Usage:
    python3 src/models/generate_right_cantilever_study.py --save        # write .rb
    python3 src/models/generate_right_cantilever_study.py --save --send # build into the ACTIVE (blank) doc
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "generators"))
import generate_sketchup_model as ov
import tbs_constants as k   # geometry constants (ov doesn't re-export them all)

ruby_box, ruby_cylinder, component = ov.ruby_box, ov.ruby_cylinder, ov.component
C = ov  # constants live on the ov module
R_X_L = k.WALKWAY_RIGHT_X                       # 4329 — deck left edge
R_X_R = k.WALKWAY_RIGHT_X + k.WALKWAY_RIGHT_W  # 4629 — deck right edge
FRAME_X = k.IBC_COL_X                           # 4674 — IBC frame near face (anchor)
GRATE_Z = k.WALKWAY_H - k.WALKWAY_GRATE_T      # 115 — grate bottom
ARM_YDS = [0, k.CORRIDOR_YD_NEAR, k.CORRIDOR_YD_FAR, k.C_WID]   # 0, 1046, 1316, 2362
ARM_BOT, ARM_TOP = 70, GRATE_Z                   # arm Z70..115 (clears spray bar top Z60 by 10mm)
ARM_W = 40                                       # arm section width in Yd (40×45 SHS)

TAGS = ["Context", "IBC Frame", "Tray + Spray", "Film Rail + Saddle",
        "Cantilever Walkway", "Grate", "Labels"]


def context():
    """Right-end container ghost: floor, ceiling, near/far walls (X 3900..C_LEN)."""
    x0, t = 3900, k.WALL_T
    xl = k.C_LEN - x0
    return '\n'.join([
        ruby_box("Floor (context)", x0, 0, -t, xl, k.C_WID, t, color=ov.C_SHELL, alpha=0.22),
        ruby_box("Ceiling (context)", x0, 0, k.C_HGT, xl, k.C_WID, t, color=ov.C_SHELL, alpha=0.10),
        ruby_box("Near wall (context)", x0, -t, 0, xl, t, k.C_HGT, color=ov.C_SHELL, alpha=0.14),
        ruby_box("Far wall (context)", x0, k.C_WID, 0, xl, t, k.C_HGT, color=ov.C_SHELL, alpha=0.14),
    ])


def tray_and_spray():
    """Processing-tray right end (rim) + the low spray-bar gantry (the clearance below)."""
    parts = []
    # tray right end (a stub of the real tray — rim band X 3900..4629)
    parts.append(ruby_box("Processing tray (right end)",
                          3900, k.PROC_TRAY_YD_NEAR, 0,
                          k.PROC_TRAY_X_R - 3900, k.PROC_TRAY_D, k.PROC_TRAY_RIM,
                          color=ov.C_PROC_ZONE, alpha=0.5))
    # spray bar gantry beam — LOW (Z20..60), spans the tray in X, drawn at mid-travel Yd
    sy = k.PROC_TRAY_YD_NEAR + k.PROC_TRAY_D / 2
    parts.append(ruby_box("Spray bar beam (Z20-60, sweeps Yd)",
                          3900, sy - k.SPRAY_BAR_BEAM / 2, k.SPRAY_BAR_Z_BOT,
                          k.PROC_TRAY_X_R - 3900, k.SPRAY_BAR_BEAM, k.SPRAY_BAR_BEAM,
                          color=ov.C_ALUM, alpha=0.6))
    return '\n'.join(parts)


def film_rail_saddle():
    """The film-plane RIGHT rail (X4649) + its near/far wall-seat saddles — the
    clearance the old ceiling rods violated. Reuses the shared saddle builder."""
    parts = []
    rz_bot, rz_top = k.RAIL_OFF_BOT, k.C_HGT - k.RAIL_OFF      # 150, 2288
    RW = 40                                                    # rail section
    # Draw the rail CENTERED on (RAIL_X_R, rz) so the beam lines up with the saddle plate
    # (which is also centered there) — fixes the off-center near plate.
    for nm, rz in (("TR", rz_top), ("BR", rz_bot)):
        parts.append(ruby_box(f"FP Rail {nm} (X{k.RAIL_X_R})",
                              k.RAIL_X_R - RW // 2, 0, rz - RW // 2, RW, k.C_WID, RW,
                              color=ov.C_STEEL, alpha=0.85))
    # right-corner saddles only (TR/BR), shared builder
    parts.append(ov.film_plane_saddles({"TR": (k.RAIL_X_R, rz_top),
                                         "BR": (k.RAIL_X_R, rz_bot)}))
    # ghost slab of the film plane at its right edge (Yd2262) so the sweep zone reads
    parts.append(ruby_box("Film plane (right edge, ghost)",
                          k.RAIL_X_R - 320, k.FP_Y, rz_bot, 320, 16, rz_top - rz_bot,
                          color=ov.C_FILM, alpha=0.18))
    return '\n'.join(parts)


X_UP = k.IBC_COL_X + 60                          # 4734 — IBC frame first corridor-upright X station
S = k.IBC_FRAME_RHS                              # 50 — frame member size
UP_YDS = (k.CORRIDOR_YD_NEAR, k.CORRIDOR_YD_FAR - S)   # 1046, 1266 — actual upright Yd lines
AH = ARM_TOP - ARM_BOT                           # arm depth (45)
HL = 95                                          # half-lap line: arm lower 70-95 / bearer upper 95-115
BEARER_W = 40
BEARER_XS = (R_X_L, R_X_R - BEARER_W)            # 4329, 4589 (left edge; each 40 wide)
BEARER_Z0 = ARM_TOP - 35                         # 80 — bearer bottom
LEDGE_XR = k.RAIL_X_R - k.IBC_WBKT_PLATE_W // 2  # 4574 — ledger BUTTS the saddle near face (closes corner)


def _xbeam_notched(name, yd, x0, x1):
    """X-beam (arm/ledger) HALF-LAPPED at each bearer it crosses: a continuous LOWER half
    (Z70..HL) + an UPPER half (HL..115) cut away where a 40-wide bearer drops in."""
    out = [ruby_box(f"{name} lower", x0, yd, ARM_BOT, x1 - x0, ARM_W, HL - ARM_BOT, color=ov.C_STEEL)]
    xs, segs = x0, []
    for bx in sorted(b for b in BEARER_XS if x0 - 1 < b < x1):
        if bx > xs:
            segs.append((xs, bx))
        xs = bx + BEARER_W
    if xs < x1:
        segs.append((xs, x1))
    for s0, s1 in segs:
        out.append(ruby_box(f"{name} upper", s0, yd, HL, s1 - s0, ARM_W, ARM_TOP - HL, color=ov.C_STEEL))
    return out


def _bearer_notched(x, cross_ranges):
    """Yd-bearer HALF-LAPPED at the arms/ledgers it crosses: a continuous UPPER half
    (HL..115) + a LOWER half (80..HL) cut away at each crossing (cross_ranges = (yd0,w))."""
    out = [ruby_box(f"Bearer X{int(x)} upper", x, 0, HL, BEARER_W, k.C_WID, ARM_TOP - HL, color=ov.C_STEEL)]
    ys, segs = 0, []
    for cy0, cw in sorted(cross_ranges):
        if cy0 > ys:
            segs.append((ys, cy0))
        ys = cy0 + cw
    if ys < k.C_WID:
        segs.append((ys, k.C_WID))
    for s0, s1 in segs:
        out.append(ruby_box(f"Bearer X{int(x)} lower", x, s0, BEARER_Z0, BEARER_W, s1 - s0, HL - BEARER_Z0, color=ov.C_STEEL))
    return out


def _wall_cleat(tag, x, wall_yd, din):
    """L-cleat the ledger seats onto: a vertical back-plate THROUGH-BOLTED to the wall
    (interior + exterior plate, 2 bolts) + a horizontal SHELF the beam lands on + welds to."""
    piy = wall_yd if din > 0 else wall_yd - 8
    poy = -k.WALL_T - 8 if din > 0 else k.C_WID + k.WALL_T
    shelf_y = wall_yd if din > 0 else wall_yd - 55
    out = [
        ruby_box(f"Wall cleat back-plate ({tag}) X{int(x)}", x - 45, piy, ARM_BOT - 10, 90, 8, AH + 20, color=ov.C_STEEL),
        ruby_box(f"Wall cleat ext. plate ({tag}) X{int(x)}", x - 45, poy, ARM_BOT - 10, 90, 8, AH + 20, color=ov.C_STEEL),
        ruby_box(f"Wall cleat shelf ({tag}) X{int(x)}", x - 45, shelf_y, ARM_BOT - 10, 90, 55, 10, color=ov.C_STEEL),
    ]
    blo, bhi = min(piy, poy), max(piy, poy) + 8
    for bz in (ARM_BOT + 6, ARM_TOP - 6):
        out.append(ruby_cylinder(f"Wall bolt ({tag}) X{int(x)} Z{int(bz)}", x, blo, bz, 5, bhi - blo, color=ov.C_STEEL, axis="y"))
    return out


def right_cantilever():
    """The proposed support — a HYBRID anchor (the IBC frame only has uprights at the
    corridor, so the perimeter arms can't grab it):
      • 2 INNER arms cantilever off the IBC corridor uprights (U-clamp + 2× M12), HALF-LAPPED
        where the bearers cross.
      • 2 OUTER wall ledgers seat on L-CLEATS (back-plate through-bolted to the wall + shelf),
        butt the film-rail SADDLE at the right corner so the saddle becomes the shared corner
        node joining the ledger + the IBC-side bearer.
      • 2 longitudinal bearers HALF-LAPPED at every crossing; grate (separate tag) on top.
    Everything at Z70-115 — above the spray bar (Z60), below the film frame (Z150)."""
    parts = []
    # ── 2 INNER cantilever arms off the IBC corridor uprights ──
    for yd in UP_YDS:
        parts += _xbeam_notched(f"Cantilever arm (off IBC upright) Yd{yd}", yd, R_X_L, X_UP)
        for pf in (yd - 8, yd + ARM_W):
            parts.append(ruby_box(f"Upright clamp plate Yd{yd} Y{int(pf)}",
                                  X_UP - 4, pf, ARM_BOT - 25, S + 8, 8, AH + 55, color=ov.C_STEEL))
        for bz in (ARM_BOT + 6, ARM_TOP + 18):
            parts.append(ruby_cylinder(f"Upright bolt M12 Yd{yd} Z{int(bz)}",
                                       X_UP + S / 2, yd - 12, bz, 6, ARM_W + 24, color=ov.C_STEEL, axis="y"))
    # ── 2 OUTER wall ledgers on L-cleats; corner closed via the film-rail saddle ──
    for wall_yd, din, tag in ((0, 1, "near"), (k.C_WID, -1, "far")):
        by = wall_yd if din > 0 else wall_yd - ARM_W
        parts += _xbeam_notched(f"Wall ledger ({tag} wall)", by, R_X_L, LEDGE_XR)   # butts the saddle
        for bx in (R_X_L + 70, LEDGE_XR - 70):
            parts += _wall_cleat(tag, bx, wall_yd, din)
        # RIGHT (IBC-side) bearer end: shelf bolted to the film-rail saddle — same corner node
        shy = wall_yd if din > 0 else wall_yd - 70
        parts.append(ruby_box(f"R-bearer saddle shelf ({tag})",
                              R_X_R - BEARER_W - 10, shy, ARM_BOT, (k.RAIL_X_R + 10) - (R_X_R - BEARER_W - 10), 70, 12,
                              color=ov.C_STEEL))
    # ── 2 longitudinal bearers, half-lapped at every crossing ──
    arm_ranges = [(yd, ARM_W) for yd in UP_YDS]                       # arms at Yd1046/1266
    ledger_ranges = [(0, ARM_W), (k.C_WID - ARM_W, ARM_W)]            # ledgers at Yd0/2322
    for bx in BEARER_XS:
        parts += _bearer_notched(bx, arm_ranges + (ledger_ranges if bx < LEDGE_XR else []))
    return '\n'.join(parts)


def right_grate():
    """The walkway grate — its OWN tag so the Anchors scene can hide it and show the
    support structure underneath."""
    return ruby_box("Right walkway grate (cantilevered — NO ceiling rods)",
                    R_X_L, 0, GRATE_Z, k.WALKWAY_RIGHT_W, k.C_WID, k.WALKWAY_GRATE_T,
                    color=ov.C_WALKWAY)


POINT_LABELS = [
    (X_UP, k.CORRIDOR_YD_NEAR, 900, "IBC CORRIDOR UPRIGHT (X4734)\n← INNER arms U-clamp here (2× M12)", 400, -350, 600),
    ((R_X_L + X_UP) / 2, k.CORRIDOR_YD_NEAR, GRATE_Z, "INNER CANTILEVER ARM ×2\noff the IBC corridor uprights", -300, -650, 650),
    (R_X_L + 130, 40, ARM_TOP, "NEAR-WALL LEDGER (left bearer)\nplates centered; stops clear of saddle", -250, -650, 700),
    (k.RAIL_X_R - 20, 40, ARM_TOP, "RIGHT bearer end → SHELF on the\nfilm-rail saddle (shared corner anchor)", 250, -600, 650),
    (R_X_L + 130, k.C_WID - 40, ARM_TOP, "FAR-WALL LEDGER (left bearer)", -250, 650, 700),
    (R_X_L + 150, 600, k.WALKWAY_H, "RIGHT WALKWAY GRATE\n(no ceiling rods)", -250, -700, 800),
    (k.RAIL_X_R, 1700, 1200, "FILM-PLANE RIGHT RAIL + SADDLES\n(old rods used to clash here)", 400, -300, 500),
    (4200, 1181, k.SPRAY_BAR_Z_TOP, "SPRAY BAR (Z20-60, low)\n55mm clear under the grate", -200, -750, 850),
]


def labels_ruby():
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
        ov.component("IBC Frame", "IBC Frame", ov.ibc_rack()),
        ov.component("Tray + Spray bar", "Tray + Spray", tray_and_spray()),
        ov.component("Film Rail + Saddles", "Film Rail + Saddle", film_rail_saddle()),
        ov.component("Cantilever Right Walkway", "Cantilever Walkway", right_cantilever()),
        ov.component("Walkway Grate", "Grate", right_grate()),
    ]
    body = '\n'.join(comps)
    tags_ruby = '\n'.join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'
    comp_tags = [t for t in TAGS if t != "Labels"]
    scenes = [("Combined", comp_tags),
              ("Anchors (frame + walls)", ["Cantilever Walkway", "IBC Frame", "Context"]),
              ("Clearance (film + spray)", ["Cantilever Walkway", "Film Rail + Saddle", "Tray + Spray"]),
              ("Labeled", TAGS)]
    scenes_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags)) for n, tags in scenes) + ']'

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Right Cantilever Study", true)
entities = model.active_entities
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0; opts["LengthPrecision"]=1
to_erase = entities.to_a.select {{ |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

{tags_ruby}

{body}

{labels_ruby()}

{ov.license_note()}

model.definitions.purge_unused
model.materials.purge_unused
keep_tags = {keep}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l| model.layers.remove(l, true) rescue nil unless l == default_layer || keep_tags.include?(l.name) }}

model.layers.each {{ |l| l.visible = (l.name != "Labels") }}
bb = model.bounds; ctr = bb.center
dir = Geom::Vector3d.new(-0.6, -0.7, 0.45); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.4)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents
{scenes_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == default_layer || tags.include?(l.name)) }}
  page = model.pages.add(name); page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}
model.commit_operation
{{ success: true, model: "Right Cantilever Study",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--save", action="store_true")
    p.add_argument("--send", action="store_true")
    args = p.parse_args()
    ruby = generate_ruby()
    if args.save:
        out = os.path.join(os.path.dirname(__file__), "right-cantilever-study.rb")
        open(out, "w").write(ruby)
        print(f"  {out} saved ({len(ruby)} bytes)")
    if args.send:
        from sketchup_client import send_ruby, SketchupError
        try:
            print(f"  SketchUp: {send_ruby(ruby)}")
        except SketchupError as e:
            print(f"  error: {e}", file=sys.stderr); sys.exit(1)
    if not args.save and not args.send:
        print(ruby)
