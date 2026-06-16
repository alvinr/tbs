#!/usr/bin/env python3
"""Generate the TBS-001 Film-Plane SketchUp model (logical model: film-plane).

OPTION A design (chosen 2026-06-06): the film is a FIXED-SIZE rigid rectangle that
only changes ANGLE. The framed muslin screen is a clickable DYNAMIC COMPONENT —
click with the Interact tool to animate it between FLAT (pose 0) and an example
TILT+SWING (pose 1, tilt 20 / swing 15). Because Option A's plane motion is a
genuine RIGID rotation, the DC reproduces it exactly (unlike the old stretching
4-corner scheme). The per-corner carriages + rod-ends travel WITH the plane; the
HGR20 rails + leadscrews stay fixed.

The NON-rigid part of Option A — the X-Z cross-slides that absorb the arc travel —
cannot be animated by a single rigid DC, so it is shown statically (with labels)
in the non-interactive "Corner detail (TR)" scene.

REUSES the helpers from the Overview generator (generate_sketchup_model as ov):
ruby_box / ruby_cylinder / ruby_pipe / component / processing_tray / colors / mm.

NOTE: --send builds into the ACTIVE SketchUp document (it clears it first). Open a
NEW blank document before sending so another model isn't overwritten, then save the
result as models/film-plane.skp. Scene-tab cameras can mis-frame in some SketchUp
builds — render detail views by setting the camera directly, then write_image.
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov

TAGS = ["Context", "Film Plane", "Corner Mechanism", "Processing Tray",
        "Walkways", "IBC Cantilever", "Corner Detail", "Labels"]

# ── Geometry of the fixed-size rigid plane ───────────────────────────────────
TILT_DEG = 20.0
SWING_DEG = 15.0
TILT = math.radians(TILT_DEG)
SWING = math.radians(SWING_DEG)

W = ov.FP_W                                  # 4499 — plane width (X)
RZ_BOT = ov.RAIL_OFF_BOT                     # 150  — bottom rail RAISED +50 (clears the Z130 walkway)
RZ_TOP = ov.C_HGT - ov.RAIL_OFF              # 2288 — top rail Z (under ceiling)
HF = RZ_TOP - RZ_BOT                         # 2188 — frame height, rail-to-rail
CX = (ov.FP_X_L + ov.FP_X_R) / 2             # 2399.5 — plane centre X
CZ = (RZ_BOT + RZ_TOP) / 2                   # 1194   — plane centre Z
CY = (ov.FP_Y_MIN + ov.FP_Y) / 2             # 1181   — flat plane depth (mid-rail)

C_XSL = "#1F77B4"   # blue  — X cross-slide (SWING float)
C_ZSL = "#2CA02C"   # green — Z cross-slide (TILT float)
C_GHOST = "#9AA6B2"

# Local corner coords about the plane centre (DC pivot): x=width, y=depth, z=height
LOCAL = {"TL": (-W / 2, 0, HF / 2), "TR": (W / 2, 0, HF / 2),
         "BL": (-W / 2, 0, -HF / 2), "BR": (W / 2, 0, -HF / 2)}
# World rail line (fixed X/Z) per corner
RAILS = {"TL": (ov.FP_X_L, RZ_TOP), "TR": (ov.FP_X_R, RZ_TOP),
         "BL": (ov.FP_X_L, RZ_BOT), "BR": (ov.FP_X_R, RZ_BOT)}


# ── rigid-rotation maths (for the static posed corner-detail) ────────────────
def _rx(v, a):
    x, y, z = v; c, s = math.cos(a), math.sin(a)
    return (x, y * c - z * s, y * s + z * c)


def _rz(v, a):
    x, y, z = v; c, s = math.cos(a), math.sin(a)
    return (x * c - y * s, x * s + y * c, z)


def _pose(v):
    return _rz(_rx(v, TILT), SWING)


def joint_ball(name, p, r, color):
    return ov.ruby_box(name, p[0] - r, p[1] - r, p[2] - r, 2 * r, 2 * r, 2 * r, color=color)


def context():
    """Low-alpha ghost of the whole container."""
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


# ── Dynamic Component: the rigid plane + travelling corner hardware ──────────
def dc_geometry_local():
    """Frame + muslin screen + per-corner carriage/drive-nut/rod-end, built FLAT in
    LOCAL coords about the plane centre. The DC rotates this rigidly (RotX=tilt,
    RotZ=swing) so the plane AND its corner hardware travel together on click.

    Screen is a thin SOLID slab (not a single face) so the Interact tool picks it
    across its whole area."""
    parts = []
    t = 12
    parts.append(ov.ruby_box("Film Plane Screen (muslin)",
                 -W / 2, -t / 2, -HF / 2, W, t, HF, color=ov.C_FILM, alpha=0.3))
    leg = ov.FP_ANGLE_LEG / 2
    P = LOCAL
    for a, b, nm in [("TL", "TR", "Top"), ("BR", "BL", "Bottom"),
                     ("TL", "BL", "Left"), ("TR", "BR", "Right")]:
        parts.append(ov.ruby_pipe(f"FP Frame {nm}", P[a], P[b], leg, color=ov.C_STEEL))
    # travelling corner hardware (carriage + drive nut + rod-end), flat = on rails
    for cid, (lx, ly, lz) in LOCAL.items():
        parts.append(ov.ruby_box(f"Carriage {cid} (HGH20CA)",
                     lx - 26, -32, lz - 12, 52, 64, 24, color=ov.C_CARR))
        parts.append(ov.ruby_box(f"Drive Nut {cid}",
                     lx + 20, -14, lz - 13, 28, 28, 26, color=ov.C_CARR))
        parts.append(joint_ball(f"Rod-End {cid}", (lx, 0, lz), 16, ov.C_STEEL))
    return '\n'.join(parts)


def assembly_block():
    """Ruby for the Film-Plane ASSEMBLY dynamic component. The WHOLE assembly is the
    clickable target: an outer 'Film Plane Assembly' DC carries the `pose` driver +
    the single onclick, and CONTAINS both the moving plane (inner 'Film Plane', which
    reads the parent's pose via formula) AND the fixed rails / leadscrews / saddles.
    So a click ANYWHERE on the assembly — screen, frame, carriage, or even a fixed
    rail/leadscrew that happens to be frontmost — bubbles up to the parent onclick and
    tilts+swings the plane. The guides stay put (no rotation formula of their own); the
    inner plane rotates about its own origin at the plane centre, so the rigid tilt/swing
    is unchanged. Proven pattern: pose driver + ancestor-reference RotX/RotZ formulas on
    the child, a SINGLE valid onclick on the parent, and redraw_with_undo AFTER commit."""
    pvx, pvy, pvz = (ov.mm(v) for v in (CX, CY, CZ))
    return f'''
# ═══ Film Plane Assembly — outer DYNAMIC COMPONENT (click ANYWHERE to tilt+swing) ═══
asm_defn = model.definitions.add("Film Plane Assembly")
asm_ents = asm_defn.entities

# inner MOVING plane: muslin screen + 2" frame + travelling corner hardware
fp_defn = model.definitions.add("Film Plane")
ents = fp_defn.entities
{dc_geometry_local()}
fp_inst = asm_ents.add_instance(fp_defn, Geom::Transformation.translation([{pvx}, {pvy}, {pvz}]))
fp_inst.name = "Film Plane"
fp_inst.layer = model.layers["Film Plane"]

# fixed guides INSIDE the assembly (clickable, but NO rotation formula -> they don't move)
ents = asm_defn.entities
{static_rails()}
{saddles()}
asm_ents.to_a.each {{ |e| next if e == fp_inst; e.layer = model.layers["Corner Mechanism"] rescue nil }}

asm_inst = entities.add_instance(asm_defn, Geom::Transformation.new)
asm_inst.name = "Film Plane Assembly"
asm_inst.layer = model.layers["Film Plane"]

fda = "dynamic_attributes"
[asm_defn, asm_inst].each do |e|
  e.set_attribute(fda, "_name", "FilmPlaneAssembly")
  e.set_attribute(fda, "_lengthunits", "MILLIMETERS")
  e.set_attribute(fda, "pose", 0.0)
end
asm_inst.set_attribute(fda, "_pose_access", "VIEW")
asm_inst.set_attribute(fda, "_pose_label", "Pose (0 flat / 1 tilt+swing)")
asm_inst.set_attribute(fda, "onclick", 'ANIMATE("pose", 0, 1)')
asm_inst.set_attribute(fda, "_onclick_access", "NONE")

[fp_defn, fp_inst].each do |e|
  e.set_attribute(fda, "_name", "FilmPlane")
  e.set_attribute(fda, "_lengthunits", "MILLIMETERS")
  e.set_attribute(fda, "rotx", 0.0)
  e.set_attribute(fda, "rotz", 0.0)
end
fp_inst.set_attribute(fda, "_rotx_formula", "{TILT_DEG}*FilmPlaneAssembly!pose")
fp_inst.set_attribute(fda, "_rotz_formula", "{SWING_DEG}*FilmPlaneAssembly!pose")
'''


def saddles():
    """Wall-seat saddles at the rail ends — single-sourced from the overview so the models
    can't drift. rev12: the bottom-RIGHT (BR) corner is the COMBINED plate shared with the
    right walkway (fp_combined_corner_plate), so BR is skipped here and the combined plate is
    drawn at the near + far walls."""
    parts = [ov.film_plane_saddles(RAILS, skip={"BR"}),
             '\n'.join(ov.fp_combined_corner_plate(0, 1)),
             '\n'.join(ov.fp_combined_corner_plate(ov.C_WID, -1))]
    return '\n'.join(parts)


def near_wall_ghost():
    """Low-alpha ghosts of the near (pinhole, Yd0) wall INTERIOR equipment, so the
    wall-fastening clearance reads in the Combined view: the Electrical Panel (high,
    Z1650–2250) + the battery bank (low, Z150–650) + the flush power-panel face. The
    near-wall ties deliberately straddle this X1700–2710 cluster (gaps only)."""
    a = 0.28
    parts = [ov.ruby_box("Electrical Panel (EP) [ghost]",
                         ov.EP_X, 0, ov.EP_H_LO, ov.EP_W, 160, ov.EP_H_HI - ov.EP_H_LO,
                         color=ov.C_ELEC, alpha=a)]
    bw = (ov.BA_W - 20) / 2
    for i, bx in enumerate((ov.BA_X, ov.BA_X + bw + 20)):
        parts.append(ov.ruby_box(f"Battery {i + 1} [ghost]",
                     bx, 0, ov.BA_H_LO, bw, ov.BA_D, ov.BA_H_HI - ov.BA_H_LO,
                     color=ov.C_BATT, alpha=a))
    parts.append(ov.ruby_box("Power panel (interior face) [ghost]",
                 ov.PWR_PANEL_X, 0, ov.PWR_PANEL_Z, ov.PWR_PANEL_W, 20, ov.PWR_PANEL_H,
                 color=ov.C_ELEC, alpha=a))
    return '\n'.join(parts)


def static_rails():
    """The FIXED guides: 4 HGR20 rails + leadscrews along depth (Yd). The carriages
    (in the DC) run along these. The RAILS now span the full width saddle-to-saddle
    (Yd 0 → C_WID) so each end lands on its wall-seat saddle with no gap; the leadscrew
    (the drive) stays within the carriage-travel band (FP_Y_MIN..+RAIL_LEN)."""
    parts = []
    y0, rlen = ov.FP_Y_MIN, ov.RAIL_LEN              # leadscrew / carriage travel band
    for cid, (cxr, czr) in RAILS.items():
        parts.append(ov.ruby_box(f"HGR20 Rail {cid}",
                     cxr - 12, 0, czr - 8, 24, ov.C_WID, 16, color=ov.C_RAIL))  # saddle→saddle
        parts.append(ov.ruby_pipe(f"Leadscrew {cid}",
                     (cxr + 34, y0, czr), (cxr + 34, y0 + rlen, czr), 7,
                     color=ov.C_STEEL))
    return '\n'.join(parts)


# ── Static, labeled corner-detail (the cross-slide story a DC can't animate) ──
def corner_detail():
    """The full Option-A chain at the POSED TR corner, static — including the X/Z
    cross-slides that absorb the arc travel. Shown only in the corner-detail scene."""
    cz = CZ
    lx, ly, lz = LOCAL["TR"]
    fx, fz = CX + lx, cz + lz                 # flat rail point
    d = _pose((lx, ly, lz)); px, py, pz = CX + d[0], CY + d[1], cz + d[2]
    dx, dz = px - fx, pz - fz
    y0, rlen = ov.FP_Y_MIN, ov.RAIL_LEN
    p = []
    p.append(ov.ruby_box("Detail Rail TR", fx - 12, y0, fz - 8, 24, rlen, 16, color=ov.C_RAIL))
    p.append(ov.ruby_pipe("Detail Leadscrew TR", (fx + 34, y0, fz), (fx + 34, y0 + rlen, fz),
             7, color=ov.C_STEEL))
    p.append(ov.ruby_box("Detail Carriage TR", fx - 26, py - 32, fz - 18, 52, 64, 24, color=ov.C_CARR))
    p.append(ov.ruby_box("Detail Drive Nut TR", fx + 20, py - 14, fz - 12, 28, 28, 26, color=ov.C_CARR))
    x0 = min(fx, px) - 16
    p.append(ov.ruby_box("Detail X cross-slide TR (SWING)", x0, py - 16, fz + 6,
             abs(dx) + 32, 32, 14, color=C_XSL))
    p.append(ov.ruby_box("Detail X slider TR", px - 16, py - 20, fz + 4, 32, 40, 20, color=ov.C_CARR))
    z0 = min(fz, pz) - 16
    p.append(ov.ruby_box("Detail Z cross-slide TR (TILT)", px - 9, py - 15, z0, 18, 30,
             abs(dz) + 32, color=C_ZSL))
    p.append(ov.ruby_box("Detail Z slider TR", px - 13, py - 18, pz - 16, 26, 36, 32, color=ov.C_CARR))
    p.append(joint_ball("Detail Rod-End TR", (px, py, pz), 17, ov.C_STEEL))
    p.append(joint_ball("Detail Flat-corner ghost TR", (fx, py, fz), 13, C_GHOST))
    return '\n'.join(p), (px, py, pz), (fx, fz)


def cantilever_label_ruby():
    """A callout for the IBC-attached right-walkway cantilever arms, placed on the
    'IBC Cantilever' tag so it shows wherever the arms show (the Combined view).
    The arms (ov.ibc_cantilever_arms) come off the IBC corridor uprights and share
    the combined corner plate with the film plane's bottom-right (BR) rail."""
    ax_ = (ov.RWK_X_L + ov.RWK_X_UP) / 2     # mid-arm X
    ay_ = ov.RWK_UP_YDS[0]                    # near arm Yd
    az_ = ov.RWK_ARM_TOP                      # arm top Z
    anc = f'Geom::Point3d.new({ov.mm(ax_)},{ov.mm(ay_)},{ov.mm(az_)})'
    txt = ("RIGHT-WALKWAY CANTILEVER ARMS\\n"
           "(off the IBC corridor uprights -\\n"
           "share the BR combined corner plate)")
    return (f't=entities.add_text("{txt}", {anc}, '
            f'Geom::Vector3d.new(-18, -16, 22)); '
            f't.layer=model.layers["IBC Cantilever"] rescue nil')


def labels_ruby(tr_world, flat_xz):
    px, py, pz = tr_world
    fx, fz = flat_xz
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
        out.append(f't=entities.add_text("{txt}", {a}, {v}); t.layer=model.layers["Labels"] rescue nil')
    return '\n'.join(out)


def generate_ruby():
    detail, tr_world, flat_xz = corner_detail()
    comps = [
        ov.component("Container (ghost)", "Context", context()),
        ov.component("Near-wall equipment (ghost)", "Context", near_wall_ghost()),
        ov.component("Processing Tray", "Processing Tray", ov.processing_tray()),
        # NB: the fixed rails/leadscrews/saddles ("Corner Mechanism" tag) now live INSIDE
        # the Film Plane Assembly DC (see assembly_block) so they're part of the click
        # target — they are no longer a separate top-level component here.
        ov.component("Walkways", "Walkways",
                     ov.walkways(include_right=True, include_right_hangers=False)),
        ov.component("IBC Cantilever Arms", "IBC Cantilever",
                     '\n'.join(ov.ibc_cantilever_arms())),
        ov.component("Corner Detail (TR)", "Corner Detail", detail),
    ]
    body = '\n'.join(comps)
    labels = labels_ruby(tr_world, flat_xz)
    cant_label = cantilever_label_ruby()
    tags_ruby = '\n'.join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    # scenes: name, visible tags, target point (mm) or None, standoff(inches) or 0=extents
    main = ["Context", "Film Plane", "Corner Mechanism", "Processing Tray", "Walkways", "IBC Cantilever"]
    noghost = ["Film Plane", "Corner Mechanism", "Processing Tray"]
    scenes = [("Combined", main, None, 0),
              ("No Container", noghost, None, 0),
              ("Corner detail (TR)", ["Corner Detail", "Labels"], tr_world, 95)]

    def slit(s):
        name, tags, tgt, so = s
        tg = '[' + ', '.join(f'"{t}"' for t in tags) + ']'
        cam = 'nil' if tgt is None else f'[{ov.mm(tgt[0])}, {ov.mm(tgt[1])}, {ov.mm(tgt[2])}]'
        return f'["{name}", {tg}, {cam}, {so}]'
    scenes_ruby = '[' + ', '.join(slit(s) for s in scenes) + ']'

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Film Plane (Option A)", true)
entities = model.active_entities
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0; opts["LengthPrecision"]=1

to_erase = entities.to_a.select {{ |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

{tags_ruby}

{body}

# ── Film Plane Assembly (Dynamic Component — click anywhere to tilt+swing) ──
{assembly_block()}

# ── Corner-detail callouts (Labels tag — shown only in the corner-detail scene) ──
{labels}

# ── IBC cantilever-arm callout (IBC Cantilever tag — shown in the Combined view) ──
{cant_label}

{ov.license_note()}

model.definitions.purge_unused
model.materials.purge_unused
keep_tags = {keep}; dl = model.layers[0]
model.layers.to_a.each {{ |l| next if l==dl||keep_tags.include?(l.name); model.layers.remove(l,true) rescue nil }}

model.layers.each {{ |l| l.visible = true }}
bb = model.bounds; ctr = bb.center
dir = Geom::Vector3d.new(0.6, -0.74, 0.42); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.4)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

{scenes_ruby}.each {{ |name, tags, tgt, so|
  model.layers.each {{ |l| l.visible = (l == dl || tags.include?(l.name)) }}
  if tgt
    t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
    cam = Sketchup::Camera.new(t.offset(dir, so), t, Z_AXIS); cam.fov = 35
    model.active_view.camera = cam
  else
    model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
    model.active_view.zoom_extents
  end
  page = model.pages.add(name); page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}
model.layers["Corner Detail"].visible = false
model.layers["Labels"].visible = false

model.commit_operation

# Register the DC AFTER committing (redraw_with_undo opens its own operation).
if defined?($dc_observers) && $dc_observers.respond_to?(:get_latest_class)
  cls = $dc_observers.get_latest_class
  cls.redraw_with_undo(asm_inst) rescue nil if cls
end

{{ success: true, model: "film-plane", scenes: model.pages.count,
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tilt: {TILT_DEG}, swing: {SWING_DEG} }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the TBS-001 Film-Plane model (Option A)")
    parser.add_argument("--save", action="store_true", help="Write Ruby to src/models/film-plane.rb")
    parser.add_argument("--send", action="store_true",
                        help="Send to the ACTIVE SketchUp document (clears it first)")
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
