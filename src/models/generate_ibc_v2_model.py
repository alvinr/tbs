#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_ibc_v2_model.py  —  TBS-001 IBC reconfig **v2** study (logical model "ibc-v2")

Focused 3D study of the redesigned IBC end zone for ibc-reconfig-v2:

  • 4× 1000L caged composite totes — Blue on TOP, Brown + Waste on the BOTTOM
    (layout unchanged from main), DIRECT-STACK cage-on-cage (52mm headroom).
  • RESTRAINT-ONLY frame (full-height corridor + front-bay uprights, ties, floor
    feet, front retaining bars + joist hangers + D-ring holders). The FRONT BAY
    also carries the right walkway (retires the old corridor-upright cantilever).
  • Plumbing panel relocated FORWARD to the corridor MOUTH (equipment in the
    front of the corridor, X≥4674) — reach-in service from the walkway. It stays
    clear of the film-plane sweep: a ghost plane at X=4649 marks the no-go line
    (the film plane owns the whole optical zone X<4649, Yd 100..2262, full height).
  • First-pass plumbing: Blue side-fill T (into the tops of the two Blue totes,
    gravity-linked) + corridor trunk indication.

Usage (build into a SketchUp document — see --send note):
    python3 src/models/generate_ibc_v2_model.py --save        # write ibc-v2.rb
    python3 src/models/generate_ibc_v2_model.py --save --send # + send to the ACTIVE doc

NOTE: --send builds into the ACTIVE SketchUp document (it CLEARS it first). Open a
blank doc before sending so overview.skp / other models are not clobbered.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov   # generic helpers + colors (Overview)

from tbs_constants import (
    C_LEN, C_WID, C_HGT,
    IBC_COL_X, IBC_W, IBC_D,
    IBC_H_1000, IBC_H_STK_1000, IBC_PALLET_H,
    BLUE_IBC_Y, IBC_FAR_Y, BROWN_IBC_Y, WASTE_IBC_Y,
    IBC_FRAME_RHS,
    IBC_FOOT_PLATE, IBC_FOOT_PLATE_T, IBC_FOOT_BOLT_PCD,
    CORRIDOR_YD_NEAR, CORRIDOR_YD_FAR,
    RAIL_X_R, FP_Y_MIN, FP_Y,
    WALKWAY_RIGHT_X, WALKWAY_RIGHT_W, WALKWAY_H, WALKWAY_GRATE_T,
    BB_OD, BB_H, PUMP_D, PUMP_H_LO,
    EQPANEL_X, EXT_PANEL_YD, EXT_FILL_1_H, EXT_DRAIN_3_H, EXT_DRAIN_4_H,
    IBC_VALVE_Z,
)

# Plumbing-panel forward slide: keep the EXISTING equipment_panel() design, just
# move it to the validated forward position (face X4874 — equipment tip ~4744,
# clear of the film rail X4649). Applied as a translate on the placed component.
PANEL_FACE_FWD = 4874
PANEL_FWD_DX   = PANEL_FACE_FWD - EQPANEL_X    # = -366mm

TAGS = ["Context", "IBC Tanks", "IBC Frame", "Panel", "Walkway", "Pipes", "Labels"]

WALL_T   = 40
C_PALLET = "#9A9A9A"      # grey pallet base band
S        = IBC_FRAME_RHS  # 50×50 RHS
PLAT_Z   = IBC_H_1000             # 1168 — direct-stack junction (cage-on-cage)
TOP_Z    = IBC_H_STK_1000 - 40    # 2296 — restraint reaches near the stack top
FRONT_X  = IBC_COL_X              # 4674 — front bay / panel mounting plane (IBC front)
YD_N     = CORRIDOR_YD_NEAR       # 1046 — near corridor edge
YD_F     = CORRIDOR_YD_FAR        # 1316 — far corridor edge
UP_YDS   = (YD_N, YD_F - S)       # 1046, 1266 — corridor upright Yd faces
X_STATIONS = [FRONT_X,
              IBC_COL_X + IBC_W / 2 - S / 2,
              IBC_COL_X + IBC_W - 60 - S]


# ── In-model labels ───────────────────────────────────────────────────────────
# (name to match an instance) OR point-anchored callouts.
IBC_POINT_LABELS = [
    # x, y, z, text, dx, dy, dz (leader vector, mm)
    (RAIL_X_R, 60, 1900, "FILM PLANE RIGHT RAIL X=4649\n(everything X<4649 is swept:\nYd 100..2262, full height —\nNO equipment here)", -700, -400, 250),
    (IBC_COL_X, YD_N, IBC_H_STK_1000, "DIRECT STACK — cage-on-cage\n(52mm headroom, no deck)", 250, -150, 250),
    (FRONT_X, (YD_N + YD_F) / 2, 1100, "FORWARD PANEL at corridor mouth\n(equipment X>=4674, reach-in\nservice from the walkway)", -350, 0, 300),
    (WALKWAY_RIGHT_X, 200, WALKWAY_H, "RIGHT WALKWAY — carried off\nthe frame FRONT BAY", -300, -200, 400),
]
IBC_INSTANCE_LABELS = [
    ("Blue #1 contents", "Blue #1 (1000L tote, ~800L)\nclean supply — TOP near", -120, -200, 250),
    ("Brown contents",   "Brown (1000L tote)\nrecycle — BOTTOM near", -120, -200, 250),
    ("Waste contents",   "Waste (1000L tote)\nBOTTOM far", 120, 200, 250),
    ("Blue #2 contents", "Blue #2 (1000L tote, ~800L)\nclean supply — TOP far", 120, 200, 250),
]


def _rb_str(s):
    """Escape a Python string for a Ruby double-quoted literal (a raw " breaks the
    whole eval'd script)."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def ibc_labels():
    rows = []
    for name, text, dx, dy, dz in IBC_INSTANCE_LABELS:
        rows.append(
            f'inst = entities.grep(Sketchup::ComponentInstance).find {{ |i| i.name == "{_rb_str(name)}" }}\n'
            f'if inst\n'
            f'  bb = inst.bounds\n'
            f'  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)\n'
            f'  txt = entities.add_text("{_rb_str(text)}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'  txt.layer = model.layers["Labels"] rescue nil\n'
            f'end')
    for x, y, z, text, dx, dy, dz in IBC_POINT_LABELS:
        rows.append(
            f'anc = Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)})\n'
            f'txt = entities.add_text("{_rb_str(text)}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    return '\n'.join(rows)


# ── Context ───────────────────────────────────────────────────────────────────
def context():
    """Low-alpha container stub around the IBC end (X≈4200..5893) PLUS a ghost plane
    at the film-plane right rail (X=4649) marking the no-go boundary."""
    x0 = 4200
    xlen = C_LEN - x0
    t = WALL_T
    parts = [
        ov.ruby_box("Floor (context)", x0, 0, -t, xlen, C_WID, t, color=ov.C_SHELL, alpha=0.25),
        ov.ruby_box("Ceiling (context)", x0, 0, C_HGT, xlen, C_WID, t, color=ov.C_SHELL, alpha=0.10),
        ov.ruby_box("Side Wall near (context)", x0, -t, 0, xlen, t, C_HGT, color=ov.C_SHELL, alpha=0.16),
        ov.ruby_box("Side Wall far (context)", x0, C_WID, 0, xlen, t, C_HGT, color=ov.C_SHELL, alpha=0.16),
        ov.ruby_box("End Wall sealed (context)", C_LEN, 0, 0, t, C_WID, C_HGT, color=ov.C_SHELL, alpha=0.16),
        # Film-plane right rail (real structure) — two vertical rails at X4649.
        ov.ruby_box("Film Right Rail near", RAIL_X_R, 30, 0, 20, 20, C_HGT, color=ov.C_FILM, alpha=0.6),
        ov.ruby_box("Film Right Rail far", RAIL_X_R, C_WID - 50, 0, 20, 20, C_HGT, color=ov.C_FILM, alpha=0.6),
        # No-go plane: a thin translucent sheet at X4649 spanning width × height.
        ov.ruby_box("Film Plane no-go (X<4649)", RAIL_X_R, 0, 0, 2, C_WID, C_HGT, color=ov.C_FILM, alpha=0.06),
    ]
    return '\n'.join(parts)


# ── IBC totes (Blue on top, Brown/Waste bottom) ──────────────────────────────
def _tote(name, contents_name, yd, z0, color, fill_h):
    x = IBC_COL_X
    parts = [
        # translucent cage box
        ov.ruby_box(f"{name} cage", x, yd, z0, IBC_W, IBC_D, IBC_H_1000, color=ov.C_STEEL, alpha=0.10),
        # grey pallet base band
        ov.ruby_box(f"{name} pallet", x, yd, z0, IBC_W, IBC_D, IBC_PALLET_H, color=C_PALLET, alpha=0.55),
        # liquid contents (named for labels)
        ov.ruby_box(contents_name, x + 40, yd + 40, z0 + IBC_PALLET_H,
                    IBC_W - 80, IBC_D - 80, fill_h, color=color, alpha=0.55),
    ]
    return '\n'.join(parts)


def ibc_totes():
    bottle_full = IBC_H_1000 - IBC_PALLET_H - 20      # ~980mm full bottle column
    blue_fill = bottle_full * 0.80                    # ~800L of 1000
    parts = [
        # Near column: Brown bottom + Blue #1 top
        _tote("Brown", "Brown contents", BROWN_IBC_Y, 0, ov.C_IBC_BROWN, bottle_full),
        _tote("Blue #1", "Blue #1 contents", BLUE_IBC_Y, IBC_H_1000, ov.C_IBC_BLUE, blue_fill),
        # Far column: Waste bottom + Blue #2 top
        _tote("Waste", "Waste contents", WASTE_IBC_Y, 0, ov.C_IBC_WASTE, bottle_full),
        _tote("Blue #2", "Blue #2 contents", IBC_FAR_Y, IBC_H_1000, ov.C_IBC_BLUE, blue_fill),
    ]
    return '\n'.join(parts)


# ── Restraint frame (front bay also carries the right walkway) ────────────────
def _wall_hanger(parts, y_wall, din, bz):
    """Simpson-style U-pocket joist hanger face-bolted to the side wall — the front
    retaining bar's wall end drops into it."""
    ht, dep = 4, 70
    p_y = y_wall if din > 0 else y_wall - ht
    s_y = y_wall if din > 0 else y_wall - dep
    parts.append(ov.ruby_box("Wall Hanger Plate", FRONT_X - 8, p_y, bz - 30, S + 16, ht, S + 70, color=ov.C_STEEL))
    parts.append(ov.ruby_box("Wall Hanger Seat", FRONT_X - 4, s_y, bz - ht, S + 8, dep, ht, color=ov.C_STEEL))


def ibc_frame():
    """Single FRONT PORTAL — one frame at the front of the corridor. It restrains
    the totes at the front, gives the proven walkway cantilever arms their clamp
    point (X4734), mounts the panel, and anchors the D-ring lashing. The totes are
    non-removable, direct-stacked and trapped by the side + end walls, so the deep
    mid/back corridor stations are dropped — transport restraint is the front
    portal + retaining bars + lashing."""
    parts = []
    c_bolt = "#3A3A42"
    fx = ov.RWK_X_UP                  # 4734 — front portal uprights (walkway arms clamp here)

    # Two full-height front uprights at the corridor edges + a top tie.
    for yd in UP_YDS:
        parts.append(ov.ruby_box("Front Portal Upright", fx, yd, 0, S, S, TOP_Z, color=ov.C_STEEL))
    parts.append(ov.ruby_box("Front Portal Top Tie", fx, YD_N, TOP_Z - S, S, YD_F - YD_N, S, color=ov.C_STEEL))

    # Floor feet under the two front uprights.
    fp, ft, bpc = IBC_FOOT_PLATE, IBC_FOOT_PLATE_T, IBC_FOOT_BOLT_PCD // 2
    for yd in UP_YDS:
        cx, cy = fx + S / 2, yd + S / 2
        parts.append(ov.ruby_box("Foot Flange Plate", cx - fp / 2, cy - fp / 2, 0, fp, fp, ft, color=ov.C_STEEL))
        for dx in (-bpc, bpc):
            for dy in (-bpc, bpc):
                parts.append(ov.ruby_cylinder("Foot Anchor M12", cx + dx, cy + dy, 0, 7, ft + 4, color=c_bolt, axis="z"))

    # Front retaining bars at the IBC front face (slide-stop + lash), tied back to
    # the portal uprights with short stubs.
    bar_zs = (560, 1760)
    for y0, y1 in ((0, YD_N + S), (YD_F - S, C_WID)):
        for bz in bar_zs:
            parts.append(ov.ruby_box("Front Retaining Bar", FRONT_X, y0, bz, S, y1 - y0, S, color=ov.C_STEEL))
    for yd in UP_YDS:
        for bz in bar_zs:
            parts.append(ov.ruby_box("Front Bar Stub", FRONT_X, yd, bz, fx - FRONT_X + S, S, S, color=ov.C_STEEL))

    # D-ring lashing holders on the front bars.
    for ydh in (520, C_WID - 520):
        for bz in bar_zs:
            parts.append(ov.ruby_cylinder("D-Ring Holder", FRONT_X - 6, ydh, bz + S / 2, 16, 10, color=ov.C_STEEL, axis="x"))
    # Wall joist hangers at each bar wall end.
    for bz in bar_zs:
        _wall_hanger(parts, 0, 1, bz)
        _wall_hanger(parts, C_WID, -1, bz)
    return '\n'.join(parts)


# ── X1/X3/X4 external lines + Blue side-fill T ───────────────────────────────
def _flange(parts, name, x, y, z, color, axis="y"):
    parts.append(ov.ruby_cylinder(name, x, y, z, 38, 20, color=color, axis=axis))


def plumbing_firstpass():
    """X1/X3/X4 external bulkhead lines (sealed end wall, X=C_LEN, Yd=1181):
      • X1 (fill, Z2250) → trunk in to a T placed NEAR X1 → side entries near the
        TOP of both Blue totes (corridor faces Yd1046 / Yd1316), gravity-linked.
      • X3 (Brown drain): IBC-3 valve → P-05 pump → X3 port (PUMP-DRIVEN).
      • X4 (Waste drain): IBC-4 valve → P-03 pump → X4 port (PUMP-DRIVEN).
    Drains are pumped, not gravity (water-system §5 P&ID). Orthogonal runs,
    perpendicular tote entries + flanges (plumbing skill). First pass — iterates."""
    parts = []
    r = 24
    yc = EXT_PANEL_YD                       # 1181 — end-wall port centerline
    fz = EXT_FILL_1_H                        # 2250 — X1 fill height
    tee_x = C_LEN - 240                      # T near X1 (just in from the end wall)
    entry_z = IBC_H_STK_1000 - 180           # ~2156 — side entry near the top

    # ── X1 Blue fill: end-wall trunk in to the T, then branch to each Blue tote ──
    parts.append(ov.ruby_pipe_run("X1 Blue Fill Trunk",
                 [(C_LEN, yc, fz), (tee_x, yc, fz)], r, color=ov.C_BLUE))
    # Branch to Blue #1 (near column, corridor face Yd=YD_N), entering near the top.
    parts.append(ov.ruby_pipe_run("Blue #1 Fill Branch",
                 [(tee_x, yc, fz), (tee_x, yc, entry_z), (tee_x, YD_N, entry_z),
                  (tee_x, YD_N - 60, entry_z)], r, color=ov.C_BLUE))
    _flange(parts, "Blue #1 Fill Flange", tee_x, YD_N, entry_z, ov.C_BLUE)
    # Branch to Blue #2 (far column, corridor face Yd=YD_F), entering near the top.
    parts.append(ov.ruby_pipe_run("Blue #2 Fill Branch",
                 [(tee_x, yc, entry_z), (tee_x, YD_F, entry_z),
                  (tee_x, YD_F + 60, entry_z)], r, color=ov.C_BLUE))
    _flange(parts, "Blue #2 Fill Flange", tee_x, YD_F, entry_z, ov.C_BLUE)

    # ── X3/X4 drains are PUMP-DRIVEN (water-system §5 P&ID — gravity is not enough):
    #    Brown: IBC-3 valve → P-05 → X3.   Waste: IBC-4 valve → P-03 → X4.
    #    P-05/P-03 are on the (forward) panel, right pump column. ──
    px = EQPANEL_X - PUMP_D / 2 + PANEL_FWD_DX    # ≈4824 — pump column X (translated)
    p_yd = YD_F - 63                              # 1253 — right pump column Yd
    p03_z = PUMP_H_LO + 218 + 40 + 109            # P-03 (waste evac) body center
    p05_z = PUMP_H_LO + 2 * 218 + 40 + 150 + 109  # P-05 (brown drain) body center

    # Brown: suction from the IBC-3 corridor-face valve up to P-05, then discharge to X3.
    bvx = IBC_COL_X + 226
    parts.append(ov.ruby_pipe_run("Brown drain suction (IBC-3 -> P-05)",
                 [(bvx, YD_N - 60, IBC_VALVE_Z), (bvx, YD_N, IBC_VALVE_Z),
                  (bvx, YD_N, p05_z), (px, YD_N, p05_z), (px, p_yd, p05_z)],
                 r, color=ov.C_IBC_BROWN))
    _flange(parts, "Brown Drain Flange", bvx, YD_N, IBC_VALVE_Z, ov.C_IBC_BROWN)
    parts.append(ov.ruby_pipe_run("Brown drain discharge (P-05 -> X3)",
                 [(px, p_yd, p05_z + 130), (px + 600, p_yd, p05_z + 130),
                  (px + 600, yc, p05_z + 130), (px + 600, yc, EXT_DRAIN_3_H),
                  (C_LEN, yc, EXT_DRAIN_3_H)], r, color=ov.C_IBC_BROWN))

    # Waste: suction from the IBC-4 corridor-face valve up to P-03, then discharge to X4.
    wvx = IBC_COL_X + 300
    parts.append(ov.ruby_pipe_run("Waste drain suction (IBC-4 -> P-03)",
                 [(wvx, YD_F + 60, IBC_VALVE_Z), (wvx, YD_F, IBC_VALVE_Z),
                  (wvx, YD_F, p03_z), (px, YD_F, p03_z), (px, p_yd, p03_z)],
                 r, color=ov.C_IBC_WASTE))
    _flange(parts, "Waste Drain Flange", wvx, YD_F, IBC_VALVE_Z, ov.C_IBC_WASTE)
    parts.append(ov.ruby_pipe_run("Waste drain discharge (P-03 -> X4)",
                 [(px, p_yd, p03_z - 130), (px + 720, p_yd, p03_z - 130),
                  (px + 720, yc, p03_z - 130), (px + 720, yc, EXT_DRAIN_4_H),
                  (C_LEN, yc, EXT_DRAIN_4_H)], r, color=ov.C_IBC_WASTE))
    return '\n'.join(parts)


# ── Assemble the Ruby ────────────────────────────────────────────────────────
def generate_ruby():
    comps = [
        ov.component("Container (ghost)", "Context", context()),
        ov.component("IBC Tanks", "IBC Tanks", ibc_totes()),
        ov.component("IBC Frame", "IBC Frame", ibc_frame()),
        # Proven rev12 walkway: closed rectangle + BOTTOM cantilever arms (Z70-115)
        # clamped to the front-portal uprights at X4734 — "the design we know works".
        ov.component("Right Walkway", "Walkway", ov.right_walkway_cantilever()),
        # EXISTING equipment-panel design reused verbatim, slid forward (below).
        ov.component("Equipment Panel", "Panel", ov.equipment_panel()),
        ov.component("Water Hookups X1/X3/X4", "Pipes", ov.water_hookups()),
        ov.component("Plumbing (first pass)", "Pipes", plumbing_firstpass()),
    ]
    body = '\n'.join(comps)

    # Slide the (verbatim) equipment panel forward to the validated film-safe
    # position — translate the placed instance by PANEL_FWD_DX in X.
    panel_shift = (
        'pinst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Equipment Panel" }\n'
        f'pinst.transform!(Geom::Transformation.translation([{ov.mm(PANEL_FWD_DX)},0,0])) if pinst'
    )

    tags_ruby = '\n'.join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    comp_tags = [t for t in TAGS if t != "Labels"]
    scenes = [
        ("IBC Tanks", ["IBC Tanks"]),
        ("IBC Frame + Walkway", ["IBC Frame", "Walkway"]),
        ("Forward Panel", ["Panel", "IBC Frame"]),
        ("Plumbing", ["Pipes", "IBC Tanks"]),
        ("Combined", comp_tags),
        ("Labeled", TAGS),
    ]
    scenes_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags)) for n, tags in scenes) + ']'

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 IBC v2 study", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# ── Idempotent rebuild ──
to_erase = entities.to_a.select {{ |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

# ── Tags ──
{tags_ruby}

# ── Subsystems ──
{body}

# ── Slide the existing equipment panel forward to the film-safe position ──
{panel_shift}

# ── In-model labels (Labels tag; visible in the "Labeled" scene) ──
{ibc_labels()}

{ov.license_note()}

model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags ──
keep_tags = {keep_tags_ruby}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

# ── Scenes — one shared iso camera, framed on geometry (Labels hidden for extents) ──
model.layers.each {{ |l| l.visible = (l.name != "Labels") }}
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(0.72, -0.7, 0.5); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

{scenes_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }}
  page = model.pages.add(name)
  page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}

model.commit_operation
{{ success: true, model: "IBC v2 study",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the TBS-001 IBC v2 study SketchUp model")
    parser.add_argument("--save", action="store_true", help="Write Ruby to src/models/ibc-v2.rb")
    parser.add_argument("--send", action="store_true",
                        help="Send to the ACTIVE SketchUp doc (clears it first — open a BLANK doc)")
    args = parser.parse_args()

    ruby = generate_ruby()

    if args.save:
        out = os.path.join(os.path.dirname(__file__), "ibc-v2.rb")
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
