#!/usr/bin/env python3
"""Generate the TBS-001 Film-Plane SketchUp model (logical model: film-plane).

OPTION A design (chosen 2026-06-06): the film is a FIXED-SIZE rigid rectangle that
only changes ANGLE. The framed muslin screen is a clickable DYNAMIC COMPONENT —
click with the Interact tool to animate it between FLAT (pose 0) and a SWUNG pose
(pose 1): a simple SWING about the plane's vertical centre axis that carries the
LEFT edge forward (toward the pinhole wall) and the RIGHT edge back. The DC is kept
deliberately simple — a single top-level RotZ swing (no tilt). A pure swing never
changes Z, so the bottom edge stays at rail height and the plane can't drop through
the floor; the corners travel along the rails in depth. The per-corner carriages +
rod-ends travel WITH the plane; the HGR20 rails + leadscrews stay fixed.

The FULL chain — tilt AND swing plus the X-Z cross-slides that absorb the arc travel
— is shown statically (with labels) in the non-interactive "Corner detail (TR)" scene,
since a single rigid DC can't animate the cross-slides.

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


def dc_block():
    """Ruby for the Film Plane DYNAMIC COMPONENT — a SIMPLE SWING (no tilt). Click to swing
    the rigid plane about its vertical centre axis: the LEFT edge moves forward (toward the
    pinhole wall, -Y) and the RIGHT edge moves back (+Y). A TOP-LEVEL component placed at the
    plane centre, so RotZ pivots about the centre. A pure swing never changes Z, so the bottom
    edge stays at rail height and the plane can't drop through the floor; the corners travel
    along the rails in depth. (Kept top-level on purpose: a nested rotating DC child resets its
    position to the parent origin on redraw — that snapped the plane to (0,0,0) and through the
    floor.) Proven pattern: pose driver + same-component RotZ formula + a single onclick +
    redraw_with_undo AFTER commit. The full tilt+swing chain still lives in the static
    'Corner detail (TR)' scene."""
    pvx, pvy, pvz = (ov.mm(v) for v in (CX, CY, CZ))
    return f'''
# ═══ Film Plane — DYNAMIC COMPONENT (click to swing: left forward / right back) ═══
fp_defn = model.definitions.add("Film Plane")
ents = fp_defn.entities
{dc_geometry_local()}
fp_inst = entities.add_instance(fp_defn, Geom::Transformation.translation([{pvx}, {pvy}, {pvz}]))
fp_inst.name = "Film Plane"
fp_inst.layer = model.layers["Film Plane"]
fda = "dynamic_attributes"
[fp_defn, fp_inst].each do |e|
  e.set_attribute(fda, "_name", "FilmPlane")
  e.set_attribute(fda, "_lengthunits", "MILLIMETERS")
  e.set_attribute(fda, "pose", 0.0)
  e.set_attribute(fda, "rotz", 0.0)
end
fp_inst.set_attribute(fda, "_pose_access", "VIEW")
fp_inst.set_attribute(fda, "_pose_label", "Pose (0 flat / 1 swung)")
fp_inst.set_attribute(fda, "_rotz_formula", "{SWING_DEG}*pose")
fp_inst.set_attribute(fda, "onclick", 'ANIMATE("pose", 0, 1)')
fp_inst.set_attribute(fda, "_onclick_access", "NONE")
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
CORNER_SLIDE_TRAVEL = -400      # carriage slide along the rail on click (-Y, toward the near end)


def corner_detail(ox=0):
    """The full Option-A chain at the POSED TR corner. The FIXED guide (rail +
    leadscrew) is static; the CARRIAGE ASSEMBLY (carriage + drive nut + cross-slides +
    sliders + rod-end + flat-corner ghost) is returned separately so generate_ruby can
    build it as a DYNAMIC COMPONENT that slides along the rail in depth (the leadscrew
    drive — click to run it). The X/Z cross-slide float is still rigid within the slide.
    Shown only in the corner-detail scene. Returns (static_ruby, slide_ruby, rod_end_world,
    flat_xz)."""
    cz = CZ
    lx, ly, lz = LOCAL["TR"]
    fx, fz = CX + lx + ox, cz + lz            # flat rail point (offset in X for layout)
    d = _pose((lx, ly, lz)); px, py, pz = CX + d[0] + ox, CY + d[1], cz + d[2]
    dx, dz = px - fx, pz - fz
    y0, rlen = ov.FP_Y_MIN, ov.RAIL_LEN
    # ── fixed guide (static) ──
    static = [
        ov.ruby_box("Detail Rail TR", fx - 12, y0, fz - 8, 24, rlen, 16, color=ov.C_RAIL),
        ov.ruby_pipe("Detail Leadscrew TR", (fx + 34, y0, fz), (fx + 34, y0 + rlen, fz),
                     7, color=ov.C_STEEL),
    ]
    # ── moving carriage assembly (the DC — slides along the rail in Y on click) ──
    x0 = min(fx, px) - 16
    z0 = min(fz, pz) - 16
    slide = [
        ov.ruby_box("Detail Carriage TR", fx - 26, py - 32, fz - 18, 52, 64, 24, color=ov.C_CARR),
        ov.ruby_box("Detail Drive Nut TR", fx + 20, py - 14, fz - 12, 28, 28, 26, color=ov.C_CARR),
        ov.ruby_box("Detail X cross-slide TR (SWING)", x0, py - 16, fz + 6,
                    abs(dx) + 32, 32, 14, color=C_XSL),
        ov.ruby_box("Detail X slider TR", px - 16, py - 20, fz + 4, 32, 40, 20, color=ov.C_CARR),
        ov.ruby_box("Detail Z cross-slide TR (TILT)", px - 9, py - 15, z0, 18, 30,
                    abs(dz) + 32, color=C_ZSL),
        ov.ruby_box("Detail Z slider TR", px - 13, py - 18, pz - 16, 26, 36, 32, color=ov.C_CARR),
        joint_ball("Detail Rod-End TR", (px, py, pz), 17, ov.C_STEEL),
        joint_ball("Detail Flat-corner ghost TR", (fx, py, fz), 13, C_GHOST),
    ]
    return '\n'.join(static), '\n'.join(slide), (px, py, pz), (fx, fz)


def corner_slide_block(slide_ruby):
    """Ruby for the Corner Slide TR DYNAMIC COMPONENT — the carriage assembly built at its
    posed home, as a TOP-LEVEL translation DC: a `slide` driver (0→1) translates it along
    the rail in Y (the leadscrew depth drive). Top-level + pure translation, so no rotation
    pivot or nested-position reset (see the swing-DC notes). On the Corner Detail tag, so it
    shows in the corner-detail scene with the static rail/leadscrew."""
    return f'''
# ═══ Corner Slide TR — DYNAMIC COMPONENT (click: carriage slides along the rail) ═══
cd_defn = model.definitions.add("Corner Slide TR")
ents = cd_defn.entities
{slide_ruby}
cd_inst = entities.add_instance(cd_defn, Geom::Transformation.new)
cd_inst.name = "Corner Slide TR"
cd_inst.layer = model.layers["Corner Detail"]
cda = "dynamic_attributes"
[cd_defn, cd_inst].each do |e|
  e.set_attribute(cda, "_name", "CornerSlideTR")
  e.set_attribute(cda, "_lengthunits", "MILLIMETERS")
  e.set_attribute(cda, "slide", 0.0)
  e.set_attribute(cda, "x", 0.0)
  e.set_attribute(cda, "y", 0.0)
  e.set_attribute(cda, "z", 0.0)
end
cd_inst.set_attribute(cda, "_slide_access", "VIEW")
cd_inst.set_attribute(cda, "_slide_label", "Slide carriage on rail")
cd_inst.set_attribute(cda, "_y_formula", "{CORNER_SLIDE_TRAVEL}*slide")
cd_inst.set_attribute(cda, "onclick", 'ANIMATE("slide", 0, 1)')
cd_inst.set_attribute(cda, "_onclick_access", "NONE")
'''


def corner_plane_ghost():
    """Partial ghost of the rigid film plane at the TR corner — a corner chunk of the muslin
    screen + the two 2in-angle frame edges meeting at TR, built in the plane's LOCAL frame
    (centre at origin). generate_ruby poses it with the same tilt+swing transform as the
    plane, so its TR corner lands on the rod-end — context for the plane this corner carries."""
    t = 12
    plen = 900                                    # partial extent from TR along each plane edge
    leg = ov.FP_ANGLE_LEG / 2
    x1, z1 = W / 2, HF / 2                         # TR corner (local)
    x0, z0 = W / 2 - plen, HF / 2 - plen
    ptr, ptl, pbr = (x1, 0, z1), (x0, 0, z1), (x1, 0, z0)
    return '\n'.join([
        ov.ruby_box("Film Plane (partial ghost)", x0, -t / 2, z0, plen, t, plen,
                    color=ov.C_FILM, alpha=0.16),
        ov.ruby_pipe("FP Frame ghost (top)", ptr, ptl, leg, color=ov.C_STEEL, alpha=0.35),
        ov.ruby_pipe("FP Frame ghost (right)", ptr, pbr, leg, color=ov.C_STEEL, alpha=0.35),
    ])


def corner_plane_ghost_block(ghost_ruby, ox):
    """Ruby placing the partial-plane ghost, posed by the same tilt+swing as the plane
    (translate ∘ RotZ(swing) ∘ RotX(tilt) about the plane centre + the diagram's X offset ox)
    so its TR corner lands on the rod-end, and NESTED inside the Corner Slide DC (cd_defn) so
    it RIDES the carriage when it slides — the corner stays attached to the plane. It carries
    no DC attributes (plain geometry), so it moves rigidly with the parent, no DC reset."""
    return f'''
# ── Partial film-plane ghost at the rail-slide corner (posed + offset ox; nested in the slide
#    DC so it rides the carriage — the plane corner stays attached to the rail as it slides) ──
cg_defn = model.definitions.add("Corner Plane Ghost TR")
ents = cg_defn.entities
{ghost_ruby}
cg_t = Geom::Transformation.translation([{ov.mm(CX + ox)}, {ov.mm(CY)}, {ov.mm(CZ)}]) *
       Geom::Transformation.rotation(ORIGIN, Z_AXIS, ({SWING_DEG}).degrees) *
       Geom::Transformation.rotation(ORIGIN, X_AXIS, ({TILT_DEG}).degrees)
cg_inst = cd_defn.entities.add_instance(cg_defn, cg_t)
cg_inst.name = "Corner Plane Ghost TR"
cg_inst.layer = model.layers["Corner Detail"]
'''


def corner_swing_detail(ox):
    """A corner detail (offset −X) showing the SWING ARC: the corner assembly built FLAT (on
    the rail), split so the CARRIAGE rides the rail in Y while the SLIDER FLOATS in X — both
    driven by one `swing` attribute via SIN/COS formulas (carriage Y = (W/2)·sin θ, X float =
    (W/2)·(cos θ−1)), so the rod-end traces the arc the corner takes as the plane swings.
    Returns (static_ruby, parent_ruby, child_ruby, rod_world)."""
    lx, ly, lz = LOCAL["TR"]
    fx, fz = CX + lx + ox, CZ + lz            # flat rail point (offset −X), top-rail height
    cy = CY                                    # flat depth (on the rail)
    y0, rlen = ov.FP_Y_MIN, ov.RAIL_LEN
    # fixed guide
    static = [
        ov.ruby_box("Swing Rail TR", fx - 12, y0, fz - 8, 24, rlen, 16, color=ov.C_RAIL),
        ov.ruby_pipe("Swing Leadscrew TR", (fx + 34, y0, fz), (fx + 34, y0 + rlen, fz), 7, color=ov.C_STEEL),
    ]
    # parent — carriage rides the rail (moves in Y); carries the X cross-slide channel
    parent = [
        ov.ruby_box("Swing Carriage TR", fx - 26, cy - 32, fz - 18, 52, 64, 24, color=ov.C_CARR),
        ov.ruby_box("Swing Drive Nut TR", fx + 20, cy - 14, fz - 12, 28, 28, 26, color=ov.C_CARR),
        ov.ruby_box("Swing X cross-slide TR (SWING float)", fx - 100, cy - 16, fz + 6, 130, 32, 14, color=C_XSL),
    ]
    # child — the slider floats in X (cross-slide); carries the Z stub + rod-end
    child = [
        ov.ruby_box("Swing X slider TR", fx - 16, cy - 20, fz + 4, 32, 40, 20, color=ov.C_CARR),
        ov.ruby_box("Swing Z cross-slide TR", fx - 9, cy - 15, fz - 9, 18, 30, 50, color=C_ZSL),
        ov.ruby_box("Swing Z slider TR", fx - 13, cy - 18, fz - 16, 26, 36, 32, color=ov.C_CARR),
        joint_ball("Swing Rod-End TR", (fx, cy, fz), 17, ov.C_STEEL),
    ]
    # partial film-plane ghost at the corner (flat, extends toward TL/-X and BR/-Z), nested in
    # the float child so it rides the corner along the arc — same faint look as the other two.
    pl = 1100
    leg = ov.FP_ANGLE_LEG / 2
    child += [
        ov.ruby_box("Swing Plane (partial ghost)", fx - pl, cy - 6, fz - pl, pl, 12, pl, color=ov.C_FILM, alpha=0.16),
        ov.ruby_pipe("Swing FP Frame (top)", (fx, cy, fz), (fx - pl, cy, fz), leg, color=ov.C_STEEL, alpha=0.35),
        ov.ruby_pipe("Swing FP Frame (right)", (fx, cy, fz), (fx, cy, fz - pl), leg, color=ov.C_STEEL, alpha=0.35),
    ]
    return '\n'.join(static), '\n'.join(parent), '\n'.join(child), (fx, cy, fz)


def corner_swing_block(parent_ruby, child_ruby, anchor):
    """Ruby for the SWING-ARC dynamic component: a parent 'Corner Swing' (carriage, moves in Y
    by (W/2)·SIN θ) with a NESTED child 'Corner Swing Float' (slider, moves in X by
    (W/2)·(COS θ−1)). One `swing` driver; the child reads it by ancestor reference so it
    re-evaluates as the parent animates. Both built FLAT at world coords + identity instances
    (home baked in the geometry), so the SIN/COS formulas translate from flat — no DC reset.
    A callout flags it clickable. Corner Detail tag (shows in the corner-detail scene)."""
    wh = W / 2
    return f'''
# ═══ Corner Swing — DYNAMIC COMPONENT (click: corner traces the swing arc) ═══
cs_defn = model.definitions.add("Corner Swing")
ents = cs_defn.entities
{parent_ruby}
cs_inst = entities.add_instance(cs_defn, Geom::Transformation.new)
cs_inst.name = "Corner Swing"
cs_inst.layer = model.layers["Corner Detail"]
csa = "dynamic_attributes"
# nested child — the floating slider (built flat, world coords)
cf_defn = model.definitions.add("Corner Swing Float")
ents = cf_defn.entities
{child_ruby}
cf_inst = cs_defn.entities.add_instance(cf_defn, Geom::Transformation.new)
cf_inst.name = "Corner Swing Float"
cf_inst.layer = model.layers["Corner Detail"]
[cs_defn, cs_inst].each do |e|
  e.set_attribute(csa, "_name", "CornerSwing")
  e.set_attribute(csa, "_lengthunits", "MILLIMETERS")
  e.set_attribute(csa, "swing", 0.0)
  e.set_attribute(csa, "x", 0.0); e.set_attribute(csa, "y", 0.0); e.set_attribute(csa, "z", 0.0)
end
cs_inst.set_attribute(csa, "_swing_access", "VIEW")
cs_inst.set_attribute(csa, "_swing_label", "Swing (corner arc)")
cs_inst.set_attribute(csa, "_y_formula", "{wh}*SIN({SWING_DEG}*swing)")
cs_inst.set_attribute(csa, "onclick", 'ANIMATE("swing", 0, 1)')
cs_inst.set_attribute(csa, "_onclick_access", "NONE")
[cf_defn, cf_inst].each do |e|
  e.set_attribute(csa, "_name", "CornerSwingFloat")
  e.set_attribute(csa, "_lengthunits", "MILLIMETERS")
  e.set_attribute(csa, "x", 0.0); e.set_attribute(csa, "y", 0.0); e.set_attribute(csa, "z", 0.0)
end
cf_inst.set_attribute(csa, "_x_formula", "{wh}*(COS({SWING_DEG}*CornerSwing!swing)-1)")
ts = entities.add_text("SWING ARC\\n(carriage in Y + X float; click to animate)", Geom::Point3d.new({ov.mm(anchor[0])}, {ov.mm(anchor[1])}, {ov.mm(anchor[2])}), Geom::Vector3d.new({ov.mm(-250)}, {ov.mm(-700)}, {ov.mm(350)}))
ts.layer = model.layers["Corner Detail"] rescue nil
'''


# Corner-detail diagram X offsets — LEFT→RIGHT order (screen-right is +X, so left = most −X):
#   1. labelled (static)  2. cross-slide (swing arc)  3. rail slide  4. plane swing (rotate)
OFF_LABELED = -5250      # 1. static, no-DC, carries the labels   (1750mm spacing, +25%)
OFF_CROSS   = -3500      # 2. swing-arc (cross-slide) DC
OFF_RAIL    = -1750      # 3. carriage rail-slide DC
OFF_PLANE   = 0          # 4. rail + partial plane that rotates on click


def corner_static_labeled(ox):
    """A STATIC (no DC) posed corner detail at offset ox — the full Option-A chain at the
    posed tilt+swing, as a clean LABELLED reference (the labels anchor to it). Same geometry
    as the slide detail, but it never moves. Returns (ruby, rod_world, flat_xz)."""
    cz = CZ
    lx, ly, lz = LOCAL["TR"]
    fx, fz = CX + lx + ox, cz + lz
    d = _pose((lx, ly, lz)); px, py, pz = CX + d[0] + ox, CY + d[1], cz + d[2]
    dx, dz = px - fx, pz - fz
    x0 = min(fx, px) - 16
    z0 = min(fz, pz) - 16
    y0, rlen = ov.FP_Y_MIN, ov.RAIL_LEN
    parts = [
        ov.ruby_box("Static Rail TR", fx - 12, y0, fz - 8, 24, rlen, 16, color=ov.C_RAIL),
        ov.ruby_pipe("Static Leadscrew TR", (fx + 34, y0, fz), (fx + 34, y0 + rlen, fz), 7, color=ov.C_STEEL),
        ov.ruby_box("Static Carriage TR", fx - 26, py - 32, fz - 18, 52, 64, 24, color=ov.C_CARR),
        ov.ruby_box("Static Drive Nut TR", fx + 20, py - 14, fz - 12, 28, 28, 26, color=ov.C_CARR),
        ov.ruby_box("Static X cross-slide TR (SWING)", x0, py - 16, fz + 6, abs(dx) + 32, 32, 14, color=C_XSL),
        ov.ruby_box("Static X slider TR", px - 16, py - 20, fz + 4, 32, 40, 20, color=ov.C_CARR),
        ov.ruby_box("Static Z cross-slide TR (TILT)", px - 9, py - 15, z0, 18, 30, abs(dz) + 32, color=C_ZSL),
        ov.ruby_box("Static Z slider TR", px - 13, py - 18, pz - 16, 26, 36, 32, color=ov.C_CARR),
        joint_ball("Static Rod-End TR", (px, py, pz), 17, ov.C_STEEL),
        joint_ball("Static Flat-corner ghost TR", (fx, py, fz), 13, C_GHOST),
    ]
    return '\n'.join(parts), (px, py, pz), (fx, fz)


def corner_rotate_plane(ox):
    """A diagram (offset ox): a rail + a partial film plane whose TR corner sits on the rail,
    with a DC that ROTATES the plane (tilt+swing) about that corner on click. The partial plane
    is built in LOCAL coords with its corner at the origin (the pivot). Returns
    (rail_ruby, plane_ruby, corner_world)."""
    lx, ly, lz = LOCAL["TR"]
    fx, fz = CX + lx + ox, CZ + lz
    cy = CY
    y0, rlen = ov.FP_Y_MIN, ov.RAIL_LEN
    rail = [
        ov.ruby_box("Rotate Rail TR", fx - 12, y0, fz - 8, 24, rlen, 16, color=ov.C_RAIL),
        ov.ruby_box("Rotate Carriage TR", fx - 26, cy - 32, fz - 18, 52, 64, 24, color=ov.C_CARR),
        joint_ball("Rotate Rod-End TR", (fx, cy, fz), 16, ov.C_STEEL),
    ]
    t = 12
    plen = 1100
    leg = ov.FP_ANGLE_LEG / 2
    plane = [
        # ghosted to match the rail-slide partial-plane ghost (screen 0.16, frame 0.35)
        ov.ruby_box("Rotate Plane (partial)", -plen, -t / 2, -plen, plen, t, plen, color=ov.C_FILM, alpha=0.16),
        ov.ruby_pipe("Rotate Frame (top)", (0, 0, 0), (-plen, 0, 0), leg, color=ov.C_STEEL, alpha=0.35),
        ov.ruby_pipe("Rotate Frame (right)", (0, 0, 0), (0, 0, -plen), leg, color=ov.C_STEEL, alpha=0.35),
    ]
    return '\n'.join(rail), '\n'.join(plane), (fx, cy, fz)


def corner_rotate_block(plane_ruby, corner):
    """Ruby for the rail+plane ROTATE diagram: the partial plane is a top-level DC placed with
    its corner on the rail, rotating (RotX=tilt, RotZ=swing about that corner) on click — so it
    shows the plane angling relative to its corner rail. Top-level rotation about the placed
    origin (the corner), so no through-floor / nested reset. Corner Detail tag; a callout flags it."""
    cx_, cy_, cz_ = (ov.mm(v) for v in corner)
    return f'''
# ═══ Rotate Plane — DYNAMIC COMPONENT (click: partial plane rotates about its corner) ═══
rp_defn = model.definitions.add("Rotate Plane")
ents = rp_defn.entities
{plane_ruby}
rp_inst = entities.add_instance(rp_defn, Geom::Transformation.translation([{cx_}, {cy_}, {cz_}]))
rp_inst.name = "Rotate Plane"
rp_inst.layer = model.layers["Corner Detail"]
rpa = "dynamic_attributes"
[rp_defn, rp_inst].each do |e|
  e.set_attribute(rpa, "_name", "RotatePlane")
  e.set_attribute(rpa, "_lengthunits", "MILLIMETERS")
  e.set_attribute(rpa, "rotate", 0.0)
  e.set_attribute(rpa, "rotx", 0.0)
  e.set_attribute(rpa, "rotz", 0.0)
end
rp_inst.set_attribute(rpa, "_rotate_access", "VIEW")
rp_inst.set_attribute(rpa, "_rotate_label", "Rotate (0 flat / 1 tilt+swing)")
rp_inst.set_attribute(rpa, "_rotx_formula", "{TILT_DEG}*rotate")
rp_inst.set_attribute(rpa, "_rotz_formula", "{SWING_DEG}*rotate")
rp_inst.set_attribute(rpa, "onclick", 'ANIMATE("rotate", 0, 1)')
rp_inst.set_attribute(rpa, "_onclick_access", "NONE")
tr = entities.add_text("RAIL + PLANE\\n(click: plane rotates about its corner)", Geom::Point3d.new({cx_}, {cy_}, {cz_}), Geom::Vector3d.new({ov.mm(220)}, {ov.mm(-700)}, {ov.mm(350)}))
tr.layer = model.layers["Corner Detail"] rescue nil
'''


# ── "Labeled" scene callouts (project rule: every .skp gets a Labeled scene) ──
# (top-level component instance name, text, leader Δx, Δy, Δz mm). The camera looks from
# +X/−Y/+Z, so Δy<0 / Δz>0 pulls a callout OUT toward the viewer; Δx spreads them apart.
FILM_PLANE_LABELS = [
    ("Film Plane",       "FILM PLANE\n(rigid screen — click to swing:\nleft fwd / right back)", 0,  -1200,  800),
    ("Corner Mechanism", "HGR20 RAILS + LEADSCREWS\n(4 fixed corner depth-guides)",            1600,  -300,  550),
    ("Processing Tray",  "PROCESSING TRAY",                                                     -800,   650,  450),
    ("Walkways",         "WALKWAYS",                                                            -1600,  -450,  700),
]
# Point-anchored (x,y,z,text,Δx,Δy,Δz) — for a part whose bounds-centre lands off the
# member (the cantilever arms come off the IBC corridor uprights).
FILM_PLANE_POINT_LABELS = [
    ((ov.RWK_X_L + ov.RWK_X_UP) / 2, ov.RWK_UP_YDS[0], ov.RWK_ARM_TOP,
     "RIGHT-WALKWAY CANTILEVER ARMS\n(off the IBC corridor uprights —\nshare the BR combined corner plate)",
     -700, -350, 650),
]


def film_plane_labels():
    """Ruby adding an in-model text callout (with leader) for each major component on the
    'Labels' tag — instance-anchored at bounds top-centre, plus a point-anchored one for
    the IBC cantilever arms. Shown only in the 'Labeled' scene (mirrors lighttrap_labels)."""
    rows = []
    for name, text, dx, dy, dz in FILM_PLANE_LABELS:
        rows.append(
            f'inst = entities.grep(Sketchup::ComponentInstance).find {{ |i| i.name == "{name}" }}\n'
            f'if inst\n'
            f'  bb = inst.bounds\n'
            f'  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)\n'
            f'  txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'  txt.layer = model.layers["Labels"] rescue nil\n'
            f'end')
    for x, y, z, text, dx, dy, dz in FILM_PLANE_POINT_LABELS:
        rows.append(
            f'anc = Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    return '\n'.join(rows)


def labels_ruby(tr_world, flat_xz):
    px, py, pz = tr_world
    fx, fz = flat_xz
    L = 10
    notes = [
        ("HGR20 rail - FIXED (depth guide)", (fx, py - 250, fz), (L, 0, 1.1 * L)),
        ("Leadscrew - DEPTH / focus drive", (fx + 34, py - 700, fz), (0.4 * L, 0, 1.9 * L)),
        ("Carriage + drive nut\n(click: slides on rail)", (fx - 20, py, fz - 12), (-1.0 * L, 0, -1.5 * L)),
        ("X cross-slide = SWING float (blue)", ((fx + px) / 2, py, fz + 14), (-1.2 * L, 0, 0.4 * L)),
        ("Z cross-slide = TILT float (green)", (px, py, (fz + pz) / 2), (1.7 * L, 0, -1.2 * L)),
        ("Rod-end -> rigid frame corner", (px, py, pz), (1.7 * L, 0, 0.5 * L)),
        ("ghost = corner if it stayed on rail", (fx, py, fz), (-1.7 * L, 0, 1.3 * L)),
    ]
    out = []
    for txt, anc, vec in notes:
        a = f'Geom::Point3d.new({ov.mm(anc[0])},{ov.mm(anc[1])},{ov.mm(anc[2])})'
        v = f'Geom::Vector3d.new({vec[0]},{vec[1]},{vec[2]})'
        out.append(f't=entities.add_text("{txt}", {a}, {v}); t.layer=model.layers["Corner Detail"] rescue nil')
    return '\n'.join(out)


def generate_ruby():
    cd_static, cd_slide, tr_world, flat_xz = corner_detail(OFF_RAIL)
    sw_static, sw_parent, sw_child, sw_world = corner_swing_detail(OFF_CROSS)
    st_ruby, st_world, st_flat = corner_static_labeled(OFF_LABELED)
    rp_rail, rp_plane, rp_corner = corner_rotate_plane(OFF_PLANE)
    comps = [
        ov.component("Container (ghost)", "Context", context()),
        ov.component("Near-wall equipment (ghost)", "Context", near_wall_ghost()),
        ov.component("Processing Tray", "Processing Tray", ov.processing_tray()),
        ov.component("Corner Mechanism", "Corner Mechanism",
                     static_rails() + "\n" + saddles()),
        ov.component("Walkways", "Walkways",
                     ov.walkways(include_right=True, include_right_hangers=False)),
        ov.component("IBC Cantilever Arms", "IBC Cantilever",
                     '\n'.join(ov.ibc_cantilever_arms())),
        ov.component("Corner Detail (TR)", "Corner Detail", cd_static),
        ov.component("Corner Detail Swing (TR)", "Corner Detail", sw_static),
        ov.component("Corner Detail Static (TR)", "Corner Detail", st_ruby),
        ov.component("Rotate Rail (TR)", "Corner Detail", rp_rail),
    ]
    body = '\n'.join(comps)
    labels = labels_ruby(st_world, st_flat)   # labels annotate the STATIC (no-DC) detail
    flabels = film_plane_labels()
    tags_ruby = '\n'.join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    # Corner-detail camera: aim at the centroid of all FOUR diagrams so they all frame
    _worlds = [tr_world, sw_world, st_world, rp_corner]
    cd_tgt = tuple(sum(w[i] for w in _worlds) / len(_worlds) for i in range(3))

    # scenes: name, visible tags, target point (mm) or None, standoff(inches) or 0=extents
    main = ["Context", "Film Plane", "Corner Mechanism", "Processing Tray", "Walkways", "IBC Cantilever"]
    noghost = ["Film Plane", "Corner Mechanism", "Processing Tray"]
    scenes = [("Combined", main, None, 0),
              ("Labeled", main + ["Labels"], None, 0),
              ("No Container", noghost, None, 0),
              ("Corner detail (TR)", ["Corner Detail"], cd_tgt, 315)]

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

# ── Film Plane (Dynamic Component — click to swing: left forward / right back) ──
{dc_block()}

# ── Corner Slide TR (Dynamic Component — click: carriage slides along the rail) ──
{corner_slide_block(cd_slide)}

# ── Partial film-plane ghost at the TR corner (static, posed) ──
{corner_plane_ghost_block(corner_plane_ghost(), OFF_RAIL)}

# ── Corner Swing (2nd detail — click: corner traces the swing arc; carriage Y + X float) ──
{corner_swing_block(sw_parent, sw_child, sw_world)}

# ── Rotate Plane (4th diagram — rail + partial plane; click rotates the plane about its corner) ──
{corner_rotate_block(rp_plane, rp_corner)}

# ── Corner-detail callouts (Corner Detail tag — shown on the STATIC detail) ──
{labels}

# ── Component callouts (Labels tag — shown only in the "Labeled" scene) ──
{flabels}

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
  cls.redraw_with_undo(fp_inst) rescue nil if cls
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
