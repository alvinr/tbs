#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_sketchup_model.py — Generate Ruby code for the TBS-001 "Overview"
SketchUp model.

Reads spatial constants from tbs_constants.py and builds Ruby that creates the
model via the SketchUp MCP plugin (eval_ruby / sketchup_client).

Organization (chosen build convention):
  - Each subsystem is a **ComponentDefinition** placed as one instance.
  - Each instance lives on its own **Tag** (layer) for show/hide.
  - **Scenes** (pages) capture useful visibility states.
  - Re-runs are **idempotent**: ALL prior instances (groups, components, text) are
    erased and their definitions purged before rebuilding — including any manually
    placed 'Sree' scale figure (the person is no longer preserved).

Subsystems / tags:
  Container Shell      → Shell            (ceiling ghosted)
  Walkways             → Walkways
  Processing Tray      → Processing Tray
  Pinhole Assembly     → Pinhole          (mount plate + Ø2.17 aperture)
  Optical Axis         → Optical Axis     (pinhole → film-plane center)
  Film Plane Mechanism → Film Plane       (rails + framed muslin screen)

Usage
-----
    python3 src/models/generate_sketchup_model.py          # print Ruby
    python3 src/models/generate_sketchup_model.py --save   # write overview.rb
    python3 src/models/generate_sketchup_model.py --send    # push to SketchUp
"""

import os
import sys
import math
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "generators"))
from tbs_constants import (
    C_LEN, C_WID, C_HGT, WALL_T,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR,
    PROC_TRAY_RIM,
    WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T,
    WALKWAY_FAR_YD, WALKWAY_RIGHT_X, WALKWAY_RIGHT_W,
    WALKWAY_LEFT_X,
    WALKWAY_BRACKET_T, WALKWAY_BRACKET_H, CONTAINER_RIB_SPACING,
    WALKWAY_WIDE_BRACKET_T, WALKWAY_WIDE_BRACKET_H,
    WALKWAY_NEAR_WIDE_W, WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_X_R,
    WALKWAY_LEFT_WIDE_W, WALKWAY_LEFT_WIDE_YD_L, WALKWAY_LEFT_WIDE_YD_R,
    CORRIDOR_YD_NEAR, CORRIDOR_YD_FAR,
    C_WALL, C_PROC_ZONE,
    PH_X, PH_H, PH_D,
    FP_X_L, FP_X_R, FP_W, FP_H, FP_Y, FP_Y_MIN,
    RAIL_X_L, RAIL_X_R, RAIL_LEN, RAIL_OFF, RAIL_OFF_BOT, FP_ANGLE_LEG,
    BRACE_RHS, BRACE_Z_BOT, BRACE_Z_TOP,
    BAY_FRONT_X, BAY_BACK_X, BAY_WALL_T,
    PANEL_CENTER_T, PANEL_CORNER_T, PANEL_FLOOR_GAP, PANEL_FAN_BAND_Z,
    PANEL_CORNER_YD_L, PANEL_CORNER_YD_R,
    PIVOT_X, PIVOT_YD, SWING_LOCK_DEG, PANEL_CUT_YD, FAR_STRIP_YD0,
    PIVOT_POST_OD, PIVOT_POST_T,
    DRUM_CAGE_X0, DRUM_CAGE_X1, DRUM_CAGE_YD_L, DRUM_CAGE_YD_R,
    WALKWAY_NEAR_LIFTOUT_X_R,
    SPRAY_BAR_BEAM, SPRAY_BAR_Z_BOT,
    BB_OD, BB_H,
    PUMP_X, PUMP_W, PUMP_H_LO, PUMP_H_HI, PUMP_YD, PUMP_YD_SPAN,
    FSKID_X, FSKID_YD, F1_Z, F2_Z, F3_Z,
    EQPANEL_X, EQPANEL_T, EQPANEL_Z_LO, EQPANEL_Z_HI,
    EQPANEL_YD, EQPANEL_YD_SPAN,
    IBC_COL_X, IBC_W, IBC_D, IBC_H_1000, IBC_PALLET_H, IBC_BOTTLE_INSET,
    BLUE_IBC_Y, BROWN_IBC_Y, IBC_FAR_Y, WASTE_IBC_Y,
    IBC_FRAME_RHS,
    IBC_FOOT_PLATE, IBC_FOOT_PLATE_T, IBC_FOOT_BOLT_PCD,
    IBC_WBKT_PLATE_W, IBC_WBKT_PLATE_T, IBC_WBKT_SEAT_PROJ,
    IBC_WBKT_SEAT_T, IBC_WBKT_GUSSET_H,
    PANEL_FRAME_X,
    DRUM_CX, DRUM_CY, DRUM_R, DRUM_H_LT,
    LT_HOUSING_R, LT_HOUSING_T, LT_DRUM_OR, LT_DRUM_T, LT_OPENING_DEG,
    EP_X, EP_W, EP_H_LO, EP_H_HI,
    ENCL_SHELL_D, MPPT_W, MPPT_D, MPPT_H, FUSEBLK_W, FUSEBLK_D, FUSEBLK_H,
    BUSBAR_L, BUSBAR_W, BUSBAR_H, DISCONNECT_D, DISCONNECT_H, CONTACTOR_W, MRBF_D, MRBF_H,
    BA_X, BA_W, BA_H_LO, BA_H_HI, BA_D,
    PWR_PANEL_X, PWR_PANEL_W, PWR_PANEL_H, PWR_PANEL_Z,
    SOLAR_PANEL_L, SOLAR_PANEL_W, SOLAR_PANEL_T, SOLAR_N, SOLAR_TILT_DEG,
    SOLAR_GAP, SOLAR_ARRAY_X, SOLAR_ARRAY_YD, SOLAR_ARRAY_Z,
    SHELF_X_L, SHELF_X_R, SHELF_W, SHELF_H, SHELF_T, SHELF_DEPTH,
    SHELF_YD_NEAR, SHELF_YD_FAR, SHELF_STOW_TOP_Z, PULL_CORD_BOTTOM_Z,
    EVAP_W, EVAP_D, EVAP_H, EVAP_DUCT_X, EVAP_DUCT_Z, EVAP_DUCT_D,
    INVERTER_X, INVERTER_Z, INVERTER_W, INVERTER_H, INVERTER_D,
    EXT_FILL_H, EXT_FILL_YD, EXT_DRAIN_H, EXT_DRAIN_3_H, EXT_DRAIN_YD,
    FAN_DIAM, FAN_BODY_D, FAN_A_YD, FAN_A_H, FAN_B_YD, FAN_B_H,
    DUCT_DEPTH, DUCT_HEIGHT,
    BV02_X, BV02_Z, TAP_X, TAP_Z, TAP_PIPE_OD, PUMP_PIPE_OD,
    SPRAY_BAR_FEED_Z,
    EQPANEL_YD_FAR, IBC_VALVE_Z,
    PROC_TRAY_DRAIN_X, PROC_TRAY_DRAIN_YD, PROC_TRAY_SUMP_Z,
)

# Material colors used only by the 3D model (not in tbs_constants).
C_STEEL = "#B0B0B8"     # steel sections (rails, mount plate, brackets, rack)
C_FILM = "#2060A0"      # film plane / muslin screen
C_PINHOLE = "#CC6600"   # pinhole aperture + optical cone
C_RAIL = "#606068"      # HGR20 linear rail
C_CARR = "#C04010"      # HGH20CA carriage block
C_ALUM = "#C8D8E8"      # aluminum (cargo door panel, spray bar beam)
C_PLY = "#9C7B4D"       # marine ply (equipment panel + hinge-panel Fan B mount band)
C_PLASTIC = "#6E8CA0"   # 4mm PP plastic sheet (rev11 hinge-panel skins + B2 bay; differentiates from wood C_PLY)
C_PUMP = "#454552"      # pump bodies (Shurflo 2088)
C_ACC = "#5A9ACC"       # ACC-01 accumulator
C_FILTER = "#3A6EA5"    # Big Blue filter housings
C_DEMOUNT = "#E0902A"   # demountable left-rail segment (swings clear for drum)
C_WALKWAY = "#808080"   # walkway grating (lowered deck, in place for operation)
C_REMOVABLE = "#C06000" # left walkway — removable lift-out for transport
C_PALLET = "#3A3A3A"    # IBC pallet base
C_IBC_BLUE = "#2E6DB4"  # Blue circuit IBC contents
C_IBC_BROWN = "#6B4A2E" # Brown (developer) IBC contents
C_IBC_WASTE = "#777777" # Waste IBC contents
C_DRUM = "#E8E0D0"      # light-trap drum shell (cream)
C_VANE = "#778088"      # drum turnstile vanes
C_ELEC = "#F5C518"      # electrical panel (EP)
C_BATT = "#6A5ACD"      # battery bank (LiFePO4)
C_SHELF = "#C8B06A"     # chemistry prep shelf (warm gold)
C_GASKT = "#5A3020"     # EPDM perimeter light seal
C_TRUNK = "#9AA0A0"     # PVC cable trunking + conduit
C_LED_W = "#FFFFE0"     # white LED panel (Cct G)
C_SAFE = "#CC2222"      # red safelight strip (Cct D)
C_SWITCH = "#D8D8F0"    # pull-cord switch
C_CORD = "#3A3A3A"      # pull cord
C_EVAP = "#3DAA96"      # evaporative cooler (teal)
C_DUCT = "#8090A0"      # vent ducting
C_FAN = "#606060"       # ventilation fans
C_BLUE = "#2979B8"      # Blue circuit supply pipe
C_VALVE = "#B8B840"     # valves / taps (brass)
C_SHELL = "#EFEDE4"     # container shell — off-white (shows systems clearly)
C_TRAY = "#9FB8C8"      # processing tray — 304 SS basin
C_BATH = "#2E6FA0"      # processing chemistry (translucent bath)

# Subsystem → tag map (also drives tag creation order).
TAGS = ["Shell", "Walkways", "Processing Tray",
        "Pinhole", "Optical Cone", "Film Plane", "Combined Plate",
        "Pivot Axle", "Spray Bar", "Equipment Panel",
        "IBC Stack", "IBC Rack", "Light Trap", "Electrical", "Shelf",
        "Light Seal", "Lighting", "Evap Cooler", "Water Hookups", "Fans",
        "Water Plumbing", "Solar Array", "Labels"]


# Major system components to call out in the "Labeled" scene.
# (component instance name, label text, leader Δx mm, leader Δz mm) — the leader is
# anchored at the component's bounds top-centre and fanned out so labels don't pile up.
# (component name, text, leader Δx, Δy, Δz mm). Δy pulls the label OUT of a wall
# toward the viewer (the camera looks from the −Y / pinhole-wall side).
OVERVIEW_LABELS = [
    ("Pinhole Assembly",      "PINHOLE  Ø2.17mm",                 -140, -1120,  630),
    ("Film Plane Mechanism",  "FILM PLANE\n4-corner tilt/swing",   400,     0, 1250),
    ("Processing Tray",       "PROCESSING TRAY",                  -250,     0,  650),
    ("Equipment Panel",       "EQUIPMENT PANEL\npump / filter",    500,     0,  820),
    ("IBC Stack",             "IBC WATER STORAGE\n4x tote",        600,     0, 1300),
    ("Light-Trap Drum",       "LIGHT-TRAP DRUM\n(entry)",         -650,     0, 1050),
    ("Electrical",            "ELECTRICAL PANEL",                  500,     0,  560),
    ("Evap Cooler & Duct",    "EVAP COOLER",                       300,     0, 1700),
    # rev13: the fold-down shelf lost its ceiling hanger rods, so a bounds-top anchor
    # now lands on the shelf assembly (not the roof) — anchor on the component so the
    # leader TRACKS the shelf wherever it's positioned (was a stale explicit point).
    ("Chemistry Shelf",       "CHEMISTRY SHELF",                  -200,  -850,  700),
]

# Labels anchored at an explicit point (mm) — for items NOT represented by a single
# component instance: the two fans live in one "Fans A & B" component that spans both
# ends of the container (so its bounds-centre lands in the empty middle), and the
# battery bank lives inside the "Electrical" component.
# (x, y, z, text, leader Δx, Δy, Δz mm)
OVERVIEW_POINT_LABELS = [
    (SOLAR_ARRAY_X + 700, SOLAR_ARRAY_YD - 500, 450, "SOLAR ARRAY\n3× 200W (30° tilt)",
     -200, -700, 700),
    (5618, 1181, 2000, "FAN A\n(exhaust, IBC end)",  400,    0,  450),
    (275,   365,  680, "FAN B\n(intake, door end)", -350,    0, 1250),
    (2060,   60,  600, "BATTERY 1× 100Ah\n(2nd pack ghosted = plug-in)",    -300, -600,  900),
    # Cct-E inverter lives inside the "Evap Cooler & Duct" component (interior, on the
    # pinhole wall below the EP), so it needs an explicit-point label. Anchor at its
    # top-centre; fan up-left + pulled toward the viewer, clear of the battery/E-stop.
    (INVERTER_X + INVERTER_W // 2, INVERTER_D // 2, INVERTER_Z + INVERTER_H,
     "CCT-E INVERTER\n12->120V AC (cooler)", -430, -820, 480),
    (1420,  -90, 1950, "EMERGENCY E-STOP\n(external panel — kills all DC)", -550, -450,  350),
    # Walkways span paired/perimeter parts, so their bounds-centre would land in the
    # empty middle — anchor on the actual NEAR member instead.
    (2400,  150,   65, "WALKWAYS",                   -200, -850,  750),  # near walkway strip
    # Spray Bar: the push pole inflates the component bbox up to Z~970, so a bounds
    # top-centre anchor floats the leader tip into mid-air above the beam (reads as the
    # tray below). Anchor on the beam itself — top-centre at the print centre X=2400,
    # gantry Yd=1180, beam top Z=60. Leader is 30% shorter than the prior version.
    (2400, 1180,   60, "SPRAY BAR",                   315, -1890,  910),
    ( 175, 2287, 1700, "PIVOT POST Ø89\n(panel swing axis)", 500, -200, 600),  # the swing pivot
]


def overview_labels():
    """Ruby that adds an in-model text callout (with leader) for each major system
    component, on the 'Labels' tag. Component labels anchor at the instance's bounds
    top-centre (tracking the geometry), but if a thin tall outrigger (push pole,
    hanger rod) has inflated the bbox so that top-centre floats >400mm above the
    component's actual geometry, a downward raytest snaps the anchor back onto the
    real top surface (kills the recurring "tip floats in empty space" bug). Point
    labels anchor at an explicit coordinate (for parts with no single representative
    instance, e.g. paired/perimeter members where even the snap has nothing at centre).
    The leader (Δx,Δy,Δz) fans the text out above/clear of the model."""
    rows = []
    for name, text, dx, dy, dz in OVERVIEW_LABELS:
        rows.append(
            f'inst = entities.grep(Sketchup::ComponentInstance).find {{ |i| i.name == "{name}" }}\n'
            f'if inst\n'
            f'  bb = inst.bounds\n'
            f'  cx = bb.center.x; cy = bb.center.y; mz = bb.max.z\n'
            f'  anc = Geom::Point3d.new(cx, cy, mz)\n'
            f'  # Guard the recurring "leader tip floats in empty space" bug: a thin tall\n'
            f'  # outrigger (push pole, hanger rod) inflates the bbox so bb.max.z hovers\n'
            f'  # well above the actual mass at the centre. Cast straight down from the\n'
            f'  # bbox top; if THIS component\'s own geometry there sits far (>400mm) below,\n'
            f'  # snap the anchor onto it. Small floats (e.g. a tray rim) stay put.\n'
            f'  hit = model.raytest([Geom::Point3d.new(cx, cy, mz + 1.mm), Geom::Vector3d.new(0, 0, -1)])\n'
            f'  if hit && hit[1] && hit[1].include?(inst) && (mz - hit[0].z) > 400.mm\n'
            f'    anc = hit[0]\n'
            f'  end\n'
            f'  txt = entities.add_text("{text}", anc, Geom::Vector3d.new({mm(dx)}, {mm(dy)}, {mm(dz)}))\n'
            f'  txt.layer = model.layers["Labels"] rescue nil\n'
            f'end')
    for x, y, z, text, dx, dy, dz in OVERVIEW_POINT_LABELS:
        rows.append(
            f'anc = Geom::Point3d.new({mm(x)}, {mm(y)}, {mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({mm(dx)}, {mm(dy)}, {mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    return '\n'.join(rows)


# In-model copyright + license credit — matches the 2D drawing/title-block footer and
# the SPDX header. © 2026 Alvin Richards, GNU AGPLv3.
LICENSE_TEXT = "© 2026 Alvin Richards\nLicensed under GNU AGPLv3\nalvinr.github.io/tbs"


def license_note(out=400):
    """Ruby: a leaderless © + license credit anchored at the model's front-bottom-left
    (offset `out` mm outboard of the near wall, toward the viewer), left on the DEFAULT
    layer so it shows in every scene. Emit AFTER all geometry (it reads model.bounds);
    the idempotent rebuild erases prior Text, so it re-adds cleanly each run.
    Shared via the `ov` module so every model gets the same credit."""
    return '\n'.join([
        '# ── In-model © + license credit (default layer → shown in every scene) ──',
        'lbb = model.bounds',
        f'lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - {mm(out)}, lbb.min.z)',
        f'entities.add_text("{LICENSE_TEXT}", lanc)',
    ])


def mm(val):
    """Render a millimeter value as a Ruby literal carrying the `.mm` suffix.

    SketchUp's geometry database is always inches internally, but the Ruby API
    converts on input: `2362.mm` yields the correct inch value. Emitting `.mm`
    keeps the generated Ruby readable in the project's native millimeters and
    lets SketchUp do the conversion, rather than baking in pre-divided floats.
    """
    # Drop a trailing ".0" so whole numbers read as 2362.mm, not 2362.0.mm.
    if isinstance(val, float) and val.is_integer():
        val = int(val)
    return f"{val}.mm"


def hex_to_rgb(h):
    """Convert '#RRGGBB' to (r, g, b) tuple."""
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


# Web viewers (e.g. Sketchfab) cap material count at ~100. Dozens of elements
# share a color, so materials are keyed by color+alpha and reused — the first
# group to use a given color+alpha names the shared material. This collapses
# ~130 per-element materials down to the number of distinct color+alpha combos.
_MAT_BY_COLOR = {}


def shared_mat_name(name, color, alpha):
    """Return a material name shared by every element of the same color+alpha."""
    key = (color, alpha if alpha is not None else 1.0)
    return _MAT_BY_COLOR.setdefault(key, name)


def ruby_box(name, x, y, z, w, d, h, color=None, alpha=None, both_sides=False):
    """Generate Ruby to create a named box group inside the `ents` context.

    Parameters are in mm. x, y, z: origin corner (min X, min Yd, min Z).
    w, d, h: width (X), depth (Yd), height (Z). Boxes are added to `ents`,
    the entities collection of the enclosing component definition.
    `both_sides` paints the back faces too (so interior + exterior read the
    same — used for the container shell).
    """
    # Sum in millimeters first, then render each corner with the `.mm` suffix.
    x0, y0, z0 = mm(x), mm(y), mm(z)
    x1, y1 = mm(x + w), mm(y + d)
    h_mm = mm(h)

    lines = [
        f'  # {name}',
        f'  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  face = grp.entities.add_face('
        f'[{x0},{y0},{z0}], [{x1},{y0},{z0}], '
        f'[{x1},{y1},{z0}], [{x0},{y1},{z0}])',
        f'  face.reverse! if face.normal.z < 0',
        f'  face.pushpull({h_mm})',
    ]

    if color:
        r, g, b = hex_to_rgb(color)
        # Reuse the material if it already exists so re-sends don't pile up
        # "Container Ceiling2", "Container Ceiling3", … duplicates.
        mat_nm = shared_mat_name(name, color, alpha)
        lines.append(f'  mat = model.materials["{mat_nm}"] || '
                     f'model.materials.add("{mat_nm}")')
        lines.append(f'  mat.color = Sketchup::Color.new({r}, {g}, {b})')
        # Always set alpha (default opaque) so a reused material can't keep a
        # stale translucency from an earlier run.
        lines.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        lines.append(f'  grp.material = mat')
        if both_sides:
            lines.append(f'  grp.entities.grep(Sketchup::Face).each '
                         f'{{ |f| f.material = mat; f.back_material = mat }}')

    lines.append('')
    return '\n'.join(lines)


def component(defn_name, tag, body):
    """Wrap a body of ruby_box calls into a ComponentDefinition + instance.

    The body builds geometry into `ents`; we then place one instance and put
    it on `tag`.
    """
    return f'''  # ═══ {defn_name} ═══
  defn = model.definitions.add("{defn_name}")
  ents = defn.entities
{body}
  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "{defn_name}"
  inst.layer = model.layers["{tag}"]
'''


def ruby_cone_wire(name, apex, base, tag):
    """Generate Ruby for a wireframe pyramid (edges only) in `ents`.

    apex: (x, y, z). base: 4 (x, y, z) corners. The edges are assigned to
    `tag`, whose line style is set to dashed in the main script — so the cone
    reads as dashed guidance geometry rather than a solid system.
    """
    a = f'[{mm(apex[0])},{mm(apex[1])},{mm(apex[2])}]'
    b = [f'[{mm(p[0])},{mm(p[1])},{mm(p[2])}]' for p in base]
    return '\n'.join([
        f'  # {name}',
        f'  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  ge = grp.entities',
        f'  apex = {a}',
        f'  b0 = {b[0]}; b1 = {b[1]}; b2 = {b[2]}; b3 = {b[3]}',
        f'  edges = []',
        f'  edges.concat(ge.add_edges(b0, b1, b2, b3, b0))',
        f'  edges << ge.add_line(apex, b0)',
        f'  edges << ge.add_line(apex, b1)',
        f'  edges << ge.add_line(apex, b2)',
        f'  edges << ge.add_line(apex, b3)',
        f'  lyr = model.layers["{tag}"]',
        f'  edges.each {{ |e| e.layer = lyr if e.is_a?(Sketchup::Edge) }}',
        '',
    ])


def ruby_cylinder(name, cx, cy, cz, radius, height, color=None, alpha=None,
                  n=24, axis="z"):
    """Generate Ruby for a cylinder in `ents`, axis along +x/+y/+z.

    (cx, cy, cz): center of the base circle. radius/height in mm. Used for
    round bodies (filters, drum, ducts, pipe stubs, fans).
    """
    normal = {"z": "[0,0,1]", "y": "[0,1,0]", "x": "[1,0,0]"}[axis]
    lines = [
        f'  # {name}',
        f'  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  ge = grp.entities',
        f'  circle = ge.add_circle([{mm(cx)},{mm(cy)},{mm(cz)}], '
        f'{normal}, {mm(radius)}, {n})',
        f'  cface = ge.add_face(circle)',
        f'  cface.reverse! if cface.normal.{axis} < 0',
        f'  cface.pushpull({mm(height)})',
    ]
    if color:
        r, g, b = hex_to_rgb(color)
        mat_nm = shared_mat_name(name, color, alpha)
        lines.append(f'  mat = model.materials["{mat_nm}"] || '
                     f'model.materials.add("{mat_nm}")')
        lines.append(f'  mat.color = Sketchup::Color.new({r}, {g}, {b})')
        lines.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        lines.append(f'  grp.material = mat')
    lines.append('')
    return '\n'.join(lines)


# ── Container shell ──────────────────────────────────────────────────────────

def container_shell():
    """Container as 5 panels (no cargo door end wall — it's the hinged panel).

    Off-white shell so the systems and their placement read clearly against it.
    """
    w = C_SHELL
    parts = []

    parts.append(ruby_box("Container Floor",
                          0, 0, -WALL_T,
                          C_LEN, C_WID, WALL_T,
                          color=w, both_sides=True))

    # Ghosted ceiling — low alpha so the interior is visible from above.
    parts.append(ruby_box("Container Ceiling",
                          0, 0, C_HGT,
                          C_LEN, C_WID, WALL_T,
                          color=w, alpha=0.2, both_sides=True))

    # Three shell walls — translucent (like the ceiling) so the systems read
    # through them from any side.
    parts.append(ruby_box("Pinhole Wall (Yd=0)",
                          0, -WALL_T, 0,
                          C_LEN, WALL_T, C_HGT,
                          color=w, alpha=0.2, both_sides=True))

    parts.append(ruby_box("Film Plane Wall (Yd=max)",
                          0, C_WID, 0,
                          C_LEN, WALL_T, C_HGT,
                          color=w, alpha=0.2, both_sides=True))

    parts.append(ruby_box("Far End Wall (IBC end)",
                          C_LEN, 0, 0,
                          WALL_T, C_WID, C_HGT,
                          color=w, alpha=0.2, both_sides=True))

    return '\n'.join(parts)


# ── Processing tray ──────────────────────────────────────────────────────────

def processing_tray():
    """Processing tray — 304 SS basin (floor + rim) holding a translucent
    chemistry bath, so it reads clearly against the off-white shell."""
    tray_w = PROC_TRAY_X_R - PROC_TRAY_X_L
    tray_d = PROC_TRAY_YD_FAR - PROC_TRAY_YD_NEAR
    sheet_t = 2
    rim_t = 2

    parts = []

    parts.append(ruby_box("Processing Tray Floor",
                          PROC_TRAY_X_L, PROC_TRAY_YD_NEAR, 0,
                          tray_w, tray_d, sheet_t, color=C_TRAY))

    parts.append(ruby_box("Tray Rim Near",
                          PROC_TRAY_X_L, PROC_TRAY_YD_NEAR, sheet_t,
                          tray_w, rim_t, PROC_TRAY_RIM - sheet_t, color=C_TRAY))
    parts.append(ruby_box("Tray Rim Far",
                          PROC_TRAY_X_L, PROC_TRAY_YD_FAR - rim_t, sheet_t,
                          tray_w, rim_t, PROC_TRAY_RIM - sheet_t, color=C_TRAY))
    parts.append(ruby_box("Tray Rim Left",
                          PROC_TRAY_X_L, PROC_TRAY_YD_NEAR, sheet_t,
                          rim_t, tray_d, PROC_TRAY_RIM - sheet_t, color=C_TRAY))
    parts.append(ruby_box("Tray Rim Right",
                          PROC_TRAY_X_R - rim_t, PROC_TRAY_YD_NEAR, sheet_t,
                          rim_t, tray_d, PROC_TRAY_RIM - sheet_t, color=C_TRAY))

    # Translucent chemistry bath inside the rims.
    parts.append(ruby_box("Chemistry Bath",
                          PROC_TRAY_X_L + rim_t, PROC_TRAY_YD_NEAR + rim_t, sheet_t,
                          tray_w - 2 * rim_t, tray_d - 2 * rim_t,
                          PROC_TRAY_RIM - sheet_t - 8, color=C_BATH, alpha=0.45))

    return '\n'.join(parts)


# ── Walkways ─────────────────────────────────────────────────────────────────

# ── Right walkway — CANTILEVER-RECTANGLE support (rev12; replaces the ceiling hangers) ──
# A closed rectangle (2 long beams + 2 end beams) under the deck, supported at mid-span by 2
# CENTER cantilever arms off the IBC corridor uprights (half-lapped where the long beams cross).
# LEFT corners on wall cleats; RIGHT corners on a COMBINED plate shared with the bottom film
# rail. Single-sourced here; the focused walkway + film-plane study models reuse these.
RWK_X_L = WALKWAY_RIGHT_X                              # 4329 — deck left edge
RWK_X_R = WALKWAY_RIGHT_X + WALKWAY_RIGHT_W            # 4629 — deck right edge
RWK_GRATE_Z = WALKWAY_H - WALKWAY_GRATE_T              # 115 — grate bottom
RWK_ARM_BOT, RWK_ARM_TOP = 70, RWK_GRATE_Z            # arm/beam Z70..115 (above spray bar 60, below film frame 150)
RWK_AH = RWK_ARM_TOP - RWK_ARM_BOT                     # 45
RWK_ARM_W = 40
RWK_HL = 95                                           # half-lap line
RWK_BEARER_W = 40
RWK_BEARER_XS = (RWK_X_L, RWK_X_R - RWK_BEARER_W)      # 4329, 4589 — long-beam left edges
RWK_BEARER_Z0 = RWK_ARM_TOP - 35                       # 80 — beam bottom
RWK_X_UP = IBC_COL_X + 60                              # 4734 — IBC corridor upright X station
RWK_UP_YDS = (CORRIDOR_YD_NEAR, CORRIDOR_YD_FAR - IBC_FRAME_RHS)   # 1046, 1266


def _rwk_xbeam(name, yd, x0, x1):
    """X-beam (arm) half-lapped at each long beam it crosses: continuous LOWER half + UPPER
    half cut away where a long beam (40 wide) drops in."""
    out = [ruby_box(f"{name} lower", x0, yd, RWK_ARM_BOT, x1 - x0, RWK_ARM_W, RWK_HL - RWK_ARM_BOT, color=C_STEEL)]
    xs, segs = x0, []
    for bx in sorted(b for b in RWK_BEARER_XS if x0 - 1 < b < x1):
        if bx > xs:
            segs.append((xs, bx))
        xs = bx + RWK_BEARER_W
    if xs < x1:
        segs.append((xs, x1))
    for s0, s1 in segs:
        out.append(ruby_box(f"{name} upper", s0, yd, RWK_HL, s1 - s0, RWK_ARM_W, RWK_ARM_TOP - RWK_HL, color=C_STEEL))
    return out


def _rwk_long_beam(x, cross_ranges):
    """Yd long beam half-lapped at the arms it crosses: continuous UPPER half + LOWER half cut
    away at each crossing (cross_ranges = (yd0, w))."""
    out = [ruby_box(f"RWk Long beam X{int(x)} upper", x, 0, RWK_HL, RWK_BEARER_W, C_WID, RWK_ARM_TOP - RWK_HL, color=C_STEEL)]
    ys, segs = 0, []
    for cy0, cw in sorted(cross_ranges):
        if cy0 > ys:
            segs.append((ys, cy0))
        ys = cy0 + cw
    if ys < C_WID:
        segs.append((ys, C_WID))
    for s0, s1 in segs:
        out.append(ruby_box(f"RWk Long beam X{int(x)} lower", x, s0, RWK_BEARER_Z0, RWK_BEARER_W, s1 - s0, RWK_HL - RWK_BEARER_Z0, color=C_STEEL))
    return out


def _rwk_wall_cleat(tag, x, wall_yd, din):
    """L-cleat the LEFT long beam seats on: back-plate through-bolted to the wall (interior +
    exterior plate, 2 bolts) + a horizontal shelf the beam lands on/welds to."""
    piy = wall_yd if din > 0 else wall_yd - 8
    poy = -WALL_T - 8 if din > 0 else C_WID + WALL_T
    shelf_y = wall_yd if din > 0 else wall_yd - 55
    out = [
        ruby_box(f"RWk wall cleat plate ({tag})", x - 45, piy, RWK_ARM_BOT - 10, 90, 8, RWK_AH + 20, color=C_STEEL),
        ruby_box(f"RWk wall cleat ext plate ({tag})", x - 45, poy, RWK_ARM_BOT - 10, 90, 8, RWK_AH + 20, color=C_STEEL),
        ruby_box(f"RWk wall cleat shelf ({tag})", x - 45, shelf_y, RWK_ARM_BOT - 10, 90, 55, 10, color=C_STEEL),
    ]
    blo, bhi = min(piy, poy), max(piy, poy) + 8
    for bz in (RWK_ARM_BOT + 6, RWK_ARM_TOP - 6):
        out.append(ruby_cylinder(f"RWk wall bolt ({tag}) Z{int(bz)}", x, blo, bz, 5, bhi - blo, color=C_STEEL, axis="y"))
    return out


def fp_combined_corner_plate(wall_yd, din, cx=None):
    """ONE plate at the near/far-RIGHT corner securing BOTH the bottom film rail (BR) and the
    walkway's right beam — through-bolted to the wall (interior + exterior plate). Spans Z58..225:
    the right beam lands on it at Z70-115, the BR rail seats on it at Z150. 150mm wide.
    `cx` overrides the X station (used to isolate it for the walkway bracket-type catalog)."""
    pw, rz = IBC_WBKT_PLATE_W, RAIL_OFF_BOT                 # 150, 150
    if cx is None:
        cx = RAIL_X_R                                      # 4649 (real BR corner)
    tag = "near" if wall_yd == 0 else "far"
    piy = wall_yd if din > 0 else wall_yd - 10
    poy = -WALL_T - 10 if din > 0 else C_WID + WALL_T
    sy = wall_yd if din > 0 else wall_yd - 55
    z0, z1 = RWK_ARM_BOT - 12, rz + 75
    out = [
        ruby_box(f"FP combined corner plate ({tag})", cx - pw / 2, piy, z0, pw, 10, z1 - z0, color=C_STEEL),
        ruby_box(f"FP combined corner ext plate ({tag})", cx - pw / 2, poy, z0, pw, 10, z1 - z0, color=C_STEEL),
        ruby_box(f"FP combined right-beam seat ({tag})", cx - pw / 2, sy, RWK_ARM_BOT - 12, pw, 55, 12, color=C_STEEL),
        ruby_box(f"FP combined BR rail seat ({tag})", cx - 30, sy, rz - 12, 60, 55, 12, color=C_STEEL),
    ]
    blo, bhi = min(piy, poy), max(piy, poy) + 10
    for bx in (cx - 50, cx + 50):
        for bz in (RWK_ARM_BOT + 14, rz + 28):
            out.append(ruby_cylinder(f"FP combined bolt M12 ({tag}) X{int(bx)} Z{int(bz)}", bx, blo, bz, 6, bhi - blo, color=C_STEEL, axis="y"))
    return out


def ibc_cantilever_arms(x_to=None):
    """The 2 walkway cantilever arms that ATTACH TO THE IBC corridor uprights (rev12):
    each arm cantilevers off an upright (Yd 1046/1266, X≈4734) toward the walkway long
    beams, with 2 upright clamps + 2 M12 through-bolts wrapping the upright. Single-
    sourced so the overview/walkway models and the focused IBC model stay in register.
    `x_to` is how far the arm reaches inward (default RWK_X_L — the left long beam)."""
    x_to = RWK_X_L if x_to is None else x_to
    parts = []
    for yd in RWK_UP_YDS:
        parts += _rwk_xbeam(f"RWk center cantilever Yd{yd}", yd, x_to, RWK_X_UP)
        for pf in (yd - 8, yd + RWK_ARM_W):
            parts.append(ruby_box(f"RWk upright clamp Yd{yd} Y{int(pf)}", RWK_X_UP - 4, pf, RWK_ARM_BOT - 25, IBC_FRAME_RHS + 8, 8, RWK_AH + 55, color=C_STEEL))
        for bz in (RWK_ARM_BOT + 6, RWK_ARM_TOP + 18):
            parts.append(ruby_cylinder(f"RWk upright bolt M12 Yd{yd} Z{int(bz)}", RWK_X_UP + IBC_FRAME_RHS / 2, yd - 12, bz, 6, RWK_ARM_W + 24, color=C_STEEL, axis="y"))
    return parts


def fp_combined_corner_plates():
    """Both right-corner COMBINED plates (near + far) — the shared anchor for the film
    plane's bottom-right (BR) rail AND the walkway right beam. Factored out so the
    overview can put it on its own tag (visible in BOTH the Film-Plane and Walkway scenes)."""
    parts = []
    for wall_yd, din in ((0, 1), (C_WID, -1)):
        parts += fp_combined_corner_plate(wall_yd, din)
    return '\n'.join(parts)


def right_walkway_grate():
    """Just the right walkway grate deck (cantilevered). Factored out so it can be put on
    the Walkways tag — letting the walkway-model 'Right Cantilever' scene show the bare
    beams + brackets while the grate still reads with the other decks."""
    return ruby_box("Right walkway grate (cantilevered)", RWK_X_L, 0, RWK_GRATE_Z,
                    WALKWAY_RIGHT_W, C_WID, WALKWAY_GRATE_T, color=C_WALKWAY)


def right_walkway_cantilever(include_combined=True, include_grate=True):
    """The right walkway support: a CLOSED rectangle (left+right long beams + 2 end beams) +
    2 center cantilever arms off the IBC corridor uprights (half-lapped at the long beams).
    LEFT corners on wall cleats; RIGHT corners on the COMBINED plate (rail + right beam).
    `include_combined=False` omits the combined plates (the overview draws them on their own
    tag so they show in the Film-Plane scene too; walkway.skp keeps them inline).
    `include_grate=False` omits the grate (walkway.skp draws it on the Walkways tag so the
    'Right Cantilever' scene shows the bare structure)."""
    parts = []
    lx, rx = RWK_X_L, RWK_X_R - RWK_BEARER_W
    arm_ranges = [(yd, RWK_ARM_W) for yd in RWK_UP_YDS]
    parts += _rwk_long_beam(lx, arm_ranges)
    parts += _rwk_long_beam(rx, arm_ranges)
    for ey in (0, C_WID - RWK_BEARER_W):
        parts.append(ruby_box(f"RWk end beam Yd{int(ey)}", lx, ey, RWK_BEARER_Z0, (rx + RWK_BEARER_W) - lx, RWK_BEARER_W, RWK_ARM_TOP - RWK_BEARER_Z0, color=C_STEEL))
    parts += ibc_cantilever_arms()
    for wall_yd, din, tag in ((0, 1, "near"), (C_WID, -1, "far")):
        parts += _rwk_wall_cleat(tag, lx + RWK_BEARER_W // 2, wall_yd, din)
        if include_combined:
            parts += fp_combined_corner_plate(wall_yd, din)
    if include_grate:
        parts.append(right_walkway_grate())
    return '\n'.join(parts)


def walkways(include_right=True, include_right_hangers=None):
    """Perimeter walkway sections — LOWERED deck, in place for operation.

    include_right=False omits the right (IBC-end) deck grate. include_right_hangers
    (defaults to include_right) independently controls the ceiling hangers — the
    focused film-plane model shows the right grate but NOT the hangers.

    The deck height comes from WALKWAY_H (lowered to 65mm: a 15mm grate at the
    tray-rim level), so the grating sits below the film-frame bottom (Z=100) and
    the film plane travels above the in-place walkway. The LEFT walkway (cargo-
    door side) is a removable lift-out (shown in a distinct color) — taken out
    for transport before the panel + drum swing inboard.
    """
    if include_right_hangers is None:
        include_right_hangers = include_right
    grate_z = WALKWAY_H - WALKWAY_GRATE_T   # 115mm — grate bottom (raised +50)
    t = WALKWAY_GRATE_T                      # 15mm — thin grate
    # The near/far decks rest on the gusset-bracket ARMS, which start at the plate's inner
    # face (y_arm = wall_yd + bracket_t). Inset each deck's WALL edge by the plate thickness
    # so the grate sits on the INSIDE of those plates instead of being drawn through them.
    bt = WALKWAY_BRACKET_T                    # 8mm  — standard bracket plate
    btw = WALKWAY_WIDE_BRACKET_T              # 10mm — widened bracket plate (near EP/battery zone)

    near_x_l = WALKWAY_LEFT_X + WALKWAY_W
    near_x_r = WALKWAY_RIGHT_X
    # The near/far grates run along the side walls from the left-walkway inner edge
    # (X=near_x_l). The floor-leg cantilever redesign has no kerb beam to cut around.
    near_len = near_x_r - near_x_l

    parts = []

    if WALKWAY_NEAR_WIDE_X_L > near_x_l:
        seg_len = WALKWAY_NEAR_WIDE_X_L - near_x_l
        parts.append(ruby_box("Walkway Near (left section)",
                              near_x_l, bt, grate_z,
                              seg_len, WALKWAY_W - bt, t, color=C_WALKWAY))

    wide_len = WALKWAY_NEAR_WIDE_X_R - WALKWAY_NEAR_WIDE_X_L
    parts.append(ruby_box("Walkway Near (widened)",
                          WALKWAY_NEAR_WIDE_X_L, btw, grate_z,
                          wide_len, WALKWAY_NEAR_WIDE_W - btw, t, color=C_WALKWAY))

    if WALKWAY_NEAR_WIDE_X_R < near_x_r:
        seg_len = near_x_r - WALKWAY_NEAR_WIDE_X_R
        parts.append(ruby_box("Walkway Near (right section)",
                              WALKWAY_NEAR_WIDE_X_R, bt, grate_z,
                              seg_len, WALKWAY_W - bt, t, color=C_WALKWAY))

    # far deck: inset the FAR (wall) edge by the standard plate thickness; near edge unchanged
    parts.append(ruby_box("Walkway Far",
                          near_x_l, WALKWAY_FAR_YD, grate_z,
                          near_len, WALKWAY_W - bt, t, color=C_WALKWAY))

    if include_right:
        if include_right_hangers:
            # rev12: full CANTILEVER-rectangle support (+ grate), replaces the ceiling hangers.
            # The combined corner plates are drawn separately (own tag) so they also show in
            # the Film-Plane scene, so omit them here.
            parts.append(right_walkway_cantilever(include_combined=False))
        else:
            parts.append(ruby_box("Walkway Right (IBC end)",
                                  WALKWAY_RIGHT_X, 0, grate_z,
                                  WALKWAY_RIGHT_W, C_WID, t, color=C_WALKWAY))

    # Left walkway — removable lift-out for transport (distinct color).
    parts.append(ruby_box("Walkway Left (REMOVABLE — transport)",
                          WALKWAY_LEFT_X, 0, grate_z,
                          WALKWAY_W, C_WID, t, color=C_REMOVABLE))
    # Drum-exit punch-out — deepened landing in front of the revolving-door exit.
    parts.append(ruby_box("Walkway Left punch-out (drum exit)",
                          WALKWAY_LEFT_X + WALKWAY_W, WALKWAY_LEFT_WIDE_YD_L, grate_z,
                          WALKWAY_LEFT_WIDE_W - WALKWAY_W,
                          WALKWAY_LEFT_WIDE_YD_R - WALKWAY_LEFT_WIDE_YD_L,
                          t, color=C_REMOVABLE))

    # Wall-cantilevered gusset brackets that actually hold the near & far decks up.
    parts.append(walkway_brackets())

    # Left walkway support: floor-leg cantilever brackets. Reuse the walkway model's
    # shared builder so the support design can't drift between the two models.
    import generate_walkway_model as wm
    parts.append('\n'.join(wm.left_floor_cantilevers()))

    # Right walkway support is now the cantilever rectangle (right_walkway_cantilever, above),
    # built with the grate when include_right_hangers — the ceiling hangers are retired (rev12).

    return '\n'.join(parts)


def walkway_brackets():
    """Wall-cantilevered gusset brackets carrying the NEAR and FAR walkway grates.

    Triangular-gusset steel brackets bolted to the long side-wall ribs at
    CONTAINER_RIB_SPACING (457mm / 18") centers — the cantilevers the decks rest
    on. STANDARD brackets are 8mm plate / 150mm leg / 300mm arm with 3× M12
    (triangular: 2 lower + 1 upper); the four WIDENED brackets in the near
    EP/battery zone (X 1155–2629) are 10mm plate / 200mm leg / 500mm arm with
    4× M12 (2×2 rectangular), per walkway Sheet 7. The RIGHT walkway is
    ceiling-hung and the LEFT walkway is a removable lift-out, so neither is
    wall-cantilevered — they get no brackets here.

    LEVEL OF DETAIL (intentional, signed off 2026-06): this whole-system view models
    each bracket simplified — interior plate + arm + gusset + short interior bolt studs.
    The dedicated walkway model's `_cantilever_parts()` (generate_walkway_model.py) is the
    full-fab version: it adds the EXTERIOR reinforcing plates and the full-length M12
    through-bolts. The two intentionally differ in detail (not in the load-bearing
    dimensions); `lint.py --duplication` lists the gap as EXPECTED, not drift.
    """
    grate_z = WALKWAY_H - WALKWAY_GRATE_T   # arm top = grate underside
    bt = WALKWAY_BRACKET_T                    # 8 — standard plate thickness
    vh = WALKWAY_BRACKET_H                    # 150 — standard vertical leg
    btw = WALKWAY_WIDE_BRACKET_T              # 10 — widened plate thickness
    vhw = WALKWAY_WIDE_BRACKET_H              # 200 — widened vertical leg
    plate_w = 120                             # mounting-plate footprint along the run (X)
    gusset_reach = 70                         # gusset depth from wall (< tray rim at Yd=80)

    # Bracket X stations along the long walls: 457mm centers across the near deck span.
    near_x_l = WALKWAY_LEFT_X + WALKWAY_W
    near_x_r = WALKWAY_RIGHT_X
    stations = []
    xs = near_x_l + CONTAINER_RIB_SPACING // 2
    while xs < near_x_r:
        stations.append(xs)
        xs += CONTAINER_RIB_SPACING

    # side: (label, wall Yd, inward sign, arm reach under that side's grate)
    sides = [
        ("Near", 0,     +1, WALKWAY_W),                 # grate Yd 0..300
        ("Far",  C_WID, -1, C_WID - WALKWAY_FAR_YD),    # grate inner edge .. far wall
    ]

    parts = []
    for label, wall_yd, sign, reach in sides:
        for i, x in enumerate(stations, 1):
            wide = (label == "Near"
                    and WALKWAY_NEAR_WIDE_X_L <= x <= WALKWAY_NEAR_WIDE_X_R)
            b = btw if wide else bt
            v = vhw if wide else vh
            arm_d = b + 2
            arm_bot = grate_z - arm_d
            rch = WALKWAY_NEAR_WIDE_W if wide else reach
            # 3× M12 triangular (std) or 4× M12 2×2 rectangular (widened), (X off, Z)
            bolts = ([(-35, 40), (35, 40), (-35, v - 40), (35, v - 40)] if wide
                     else [(0, v - 30), (-35, 40), (35, 40)])
            nm = f"Walkway {label} bracket {i}" + (" (widened)" if wide else "")
            # 1. vertical mounting plate flat on the wall rib
            y_plate = wall_yd if sign > 0 else wall_yd - b
            parts.append(ruby_box(f"{nm} plate", x - plate_w / 2, y_plate, 0,
                                  plate_w, b, v, color=C_STEEL))
            # 2. M12 anchor bolts through the plate — Ø12 shanks
            for dx, bz in bolts:
                parts.append(ruby_cylinder(f"{nm} bolt M12",
                              x + dx, y_plate - 6, bz, 6, b + 12,
                              color="#505058", axis="y"))
            # 3. horizontal cantilever arm at grate level (deck rests on it) — its
            #    back end butts the plate face so the arm→plate joint draws an edge
            y_arm = (wall_yd + b) if sign > 0 else (wall_yd - rch)
            parts.append(ruby_box(f"{nm} arm", x - b / 2, y_arm, arm_bot,
                                  b, rch - b, arm_d, color=C_STEEL))
            # 4. gusset triangle bracing the arm from below — directly UNDER the arm
            #    (push −b), back edge butted to the plate face for a clean joint
            xg = x - b / 2
            y_back = wall_yd + sign * b
            y_far = wall_yd + sign * gusset_reach
            parts.append(ruby_tri(f"{nm} gusset",
                                  (xg, y_back, 0),
                                  (xg, y_back, arm_bot),
                                  (xg, y_far, arm_bot),
                                  -b, color=C_STEEL))
    return '\n'.join(parts)


# ── Pinhole assembly ─────────────────────────────────────────────────────────

def pinhole_assembly():
    """Pinhole mount plate on the wall inner face + the Ø2.17 aperture marker.

    The aperture is true-scale (2.17mm) so it is dimensionally honest; the
    orange optical-axis tube makes its location findable at overview scale.
    """
    parts = []
    plate, t = 100, 3  # 100×100mm SS mount plate, 3mm proud of the wall

    parts.append(ruby_box("Pinhole Mount Plate",
                          PH_X - plate / 2, 0, PH_H - plate / 2,
                          plate, t, plate,
                          color=C_STEEL))

    a = PH_D  # 2.17mm aperture, shown as a true-size orange nub on the plate face
    parts.append(ruby_box("Pinhole Aperture (Ø2.17)",
                          PH_X - a / 2, t, PH_H - a / 2,
                          a, 1, a,
                          color=C_PINHOLE))

    # Exterior tilt-swing front standard (holds the pinhole plate, ±5.3°).
    ext = -WALL_T                      # exterior wall face
    base = 340
    parts.append(ruby_box("TS Base Plate (wall mount)",
                          PH_X - base / 2, ext - 12, PH_H - base / 2,
                          base, 12, base, color=C_STEEL))
    bd = 280
    parts.append(ruby_box("Pinhole Tilt-Swing Board",
                          PH_X - bd / 2, ext - 40, PH_H - bd / 2,
                          bd, 16, bd, color=C_ALUM))
    # Tilt knob (bottom) + swing knob (right edge).
    parts.append(ruby_box("TS Tilt Knob",
                          PH_X - 15, ext - 60, PH_H - bd / 2 - 25,
                          30, 25, 30, color=C_STEEL))
    parts.append(ruby_box("TS Swing Knob",
                          PH_X + bd / 2, ext - 60, PH_H - 15,
                          25, 25, 30, color=C_STEEL))

    return '\n'.join(parts)


# ── Optical cone ─────────────────────────────────────────────────────────────

def optical_cone():
    """Ghosted projection cone: pinhole apex → full film-plane rectangle.

    The rectangular pyramid from the pinhole (Yd=0) expanding to the film plane
    (Yd=FP_Y) shows the light cone filling the container interior. Kept very
    faint — it is guidance geometry, not a hard system.
    """
    apex = (PH_X, 0, PH_H)
    base = [(FP_X_L, FP_Y, 0), (FP_X_R, FP_Y, 0),
            (FP_X_R, FP_Y, FP_H), (FP_X_L, FP_Y, FP_H)]
    return ruby_cone_wire("Optical Cone", apex, base, "Optical Cone")


# ── Cargo-door panel + swing pivot (rev10 — supersedes the ceiling-rail slide) ─

def panel_pivot():
    """Cargo-door panel + its vertical SWING pivot.

    The panel + drum assembly rotates ~56° about a Ø89 CHS post (the film-plane
    far-left upright, REUSED — geometry single-sourced from the light-trap model,
    lt.axle()) to clear the cargo doors for transport. The old HGR20 ceiling-rail
    suspension + HGH20CA carriages are retired. Shown here shut at X=0 (operating);
    the detailed swing mechanism (3-zone split, hub bearings, wall stays, removable
    rails) lives in models/lighttrap.skp.
    """
    import generate_lighttrap_model as lt
    parts = [lt.axle()]
    # Cargo-door panel, operational position (X=0). rev11: 4mm PP plastic skins
    # (C_PLASTIC), with an 18mm PLYWOOD (C_PLY) mount band on the Fan B corner.
    parts.append(ruby_box("Cargo Door Panel",
                          0, 0, PANEL_FLOOR_GAP,
                          PANEL_CENTER_T, C_WID, 2300 - PANEL_FLOOR_GAP,
                          color=C_PLASTIC, alpha=0.6))
    parts.append(ruby_box("Fan B mount band (18mm ply)",
                          0, 0, PANEL_FLOOR_GAP,
                          PANEL_CENTER_T, PANEL_CORNER_YD_L, PANEL_FAN_BAND_Z - PANEL_FLOOR_GAP,
                          color=C_PLY, alpha=0.6))
    # Transport-lock support brackets (top + bottom): the near-wall stay anchors
    # (sandwiched inside/outside plates + eye + 4× M16) and the frame-side stay hooks.
    # The stay ROD/turnbuckle itself is left out — only the permanent brackets are shown.
    parts.append(lt.wall_anchors())
    parts.append(lt.frame_hooks())
    return '\n'.join(parts)


# ── Spray bar (processing-tray wash gantry) ──────────────────────────────────

def spray_bar():
    """Spray-bar gantry — reuses the detailed spray-bar model builders so the
    overview stays in sync with models/spraybar.skp: 40×40 SHS beam housing a 3/4"
    LDPE pipe + 26 flat-fan nozzles, two-wheel carriages (curved saddle axle clamps
    + top/bottom beam clamp plates), flange-base ball joint, distribution manifold
    + 7 irrigation feed tubes, and the push pole bound to the supply hose with
    zip ties. The tray-floor ref patch is omitted (overview has its own tray)."""
    import generate_spraybar_model as sb
    return '\n'.join([sb.build_beam(),
                      sb.build_carriages(include_floor=False),
                      sb.build_feed_pole()])


# ── Equipment panel (pumps · filters · accumulator) ──────────────────────────

def equipment_panel():
    """18mm marine-ply panel in the IBC corridor carrying the wet end.

    Layout follows the panel-layout diagram: equipment mounts on the panel
    face (X=EQPANEL_X) protruding toward the open end (-X). Two pump columns
    (left Yd≈1109, right Yd≈1253), three rows (P-01/P-02, P-04/P-03,
    ACC-01/P-05), and three Big Blue filters centered below the pump zone.
    """
    parts = []
    face_x = EQPANEL_X                    # panel face — equipment hangs in -X

    parts.append(ruby_box("Equipment Panel (ply)",
                          face_x, EQPANEL_YD, EQPANEL_Z_LO,
                          EQPANEL_T, EQPANEL_YD_SPAN, EQPANEL_Z_HI - EQPANEL_Z_LO,
                          color=C_PLY))

    # Pump grid — two columns, body 100(X) × 127(Yd) × 218(Z), 40mm row gap.
    pump_d, pump_face, pump_h, gap = PUMP_W, PUMP_YD_SPAN, 218, 40
    col_l = EQPANEL_YD + 63               # PUMP_COL — left column Yd center
    col_r = EQPANEL_YD + (EQPANEL_YD_SPAN - 63)  # right column Yd center
    z_bot = PUMP_H_LO                     # 1370 — bottom pump row
    z_mid = z_bot + pump_h + gap          # 1578 — upper pump row
    z_top = z_mid + pump_h + 150          # 1946 — ACC-01 / P-05 row

    def pump(nm, yd_c, z):
        return ruby_box(nm, face_x - pump_d, yd_c - pump_face / 2, z,
                        pump_d, pump_face, pump_h, color=C_PUMP)

    parts.append(pump("Pump P-01 (Blue)", col_l, z_bot))
    parts.append(pump("Pump P-02 (Brown)", col_r, z_bot))
    parts.append(pump("Pump P-04 (Tray drain)", col_l, z_mid))
    parts.append(pump("Pump P-03 (Waste evac)", col_r, z_mid))
    parts.append(pump("Pump P-05 (Brown drain)", col_r, z_top))

    # ACC-01 accumulator — Ø127 × 200 cylinder (real SeaFlo 0.75L ≈ 200×127×125), left column.
    parts.append(ruby_cylinder("ACC-01 Accumulator",
                               face_x - 63, col_l, z_top, 127 / 2, 200,
                               color=C_ACC))

    # Three Big Blue filters, centered on the panel, stacked F3→F2→F1.
    fr = BB_OD / 2
    fcx = face_x - fr
    fcy = EQPANEL_YD + EQPANEL_YD_SPAN / 2          # centered in the corridor
    for nm, fz in [("F1 (50µ)", F1_Z), ("F2 (5µ)", F2_Z), ("F3 (GAC)", F3_Z)]:
        parts.append(ruby_cylinder(f"Filter {nm}",
                                   fcx, fcy, fz, fr, BB_H, color=C_FILTER))

    # ── Drain-riser backing spine (rev 8.1) ──────────────────────────────────
    # 18mm marine-ply spine teed perpendicular off the panel (a T in plan), into
    # the corridor gap, so the X3/X4 drain risers (Brown @ X=5400, Waste @ X=5340,
    # both Yd=col_r) clamp to it instead of free-hanging.  Sits in the clear
    # corridor (Yd 1046-1316) — no tote contact.  Rises to the full panel height
    # (v2: the over-the-top Blue fill trunk this spine used to carry is gone — the
    # Blue fill now SIDE-ENTERS near the top, so no shelf/saddle is needed).
    sp_t  = EQPANEL_T                              # 18mm ply
    sp_x0, sp_x1 = face_x, 5420                     # butts the panel rear → past the X3 riser
    sp_y  = col_r - 30                              # spine board Yd (near-face just off the risers)
    spine_top = EQPANEL_Z_HI                        # 2310 — full panel height
    parts.append(ruby_box("Drain-riser spine (ply)", sp_x0, sp_y, EQPANEL_Z_LO,
                          sp_x1 - sp_x0, sp_t, spine_top - EQPANEL_Z_LO,
                          color=C_PLY))
    # Stiffening flange along the spine's rear edge → T cross-section.
    parts.append(ruby_box("Drain-riser spine flange (ply)", sp_x1 - sp_t,
                          col_r - 27, EQPANEL_Z_LO, sp_t, 54,
                          spine_top - EQPANEL_Z_LO, color=C_PLY))
    # SS pipe clamps (P-clips) holding each riser to the spine face, ~400mm centers.
    clamp_face = sp_y + sp_t                        # spine face the pipes sit against
    for rx, ztop in ((5340, 1578), (5400, 1946)):   # X4 Waste, X3 Brown risers
        cz = 500
        while cz < ztop - 80:
            parts.append(ruby_box("Riser pipe clamp", rx - 16, clamp_face, cz,
                                  32, 30, 22, color=C_STEEL))
            cz += 400

    return '\n'.join(parts)


# ── IBC stack (4× totes, 2×2) + support rack ─────────────────────────────────

def ibc_stack(alpha=0.55):
    """Four IBC totes in a 2×2 stack: pallet base + translucent bottle each.

    Near column (Yd=30): Brown developer below, Blue #1 on top.
    Far column (Yd=1316): Waste below, Blue #2 on top. X spans 4674–5893.
    ibc-reconfig-v2: 1000L caged composite totes (1168mm), direct-stacked to 2336mm.
    `alpha` sets the bottle translucency (lower = more transparent).
    """
    parts = []
    pal = IBC_PALLET_H
    inset = IBC_BOTTLE_INSET
    bottle_h = IBC_H_1000 - pal - 20   # leave 20mm for the cage top

    totes = [
        ("IBC Brown (developer)", BROWN_IBC_Y, 0, C_IBC_BROWN),
        ("IBC Blue #1", BLUE_IBC_Y, IBC_H_1000, C_IBC_BLUE),
        ("IBC Waste", WASTE_IBC_Y, 0, C_IBC_WASTE),
        ("IBC Blue #2", IBC_FAR_Y, IBC_H_1000, C_IBC_BLUE),
    ]
    for nm, yd, z0, col in totes:
        parts.append(ruby_box(f"{nm} pallet",
                              IBC_COL_X, yd, z0, IBC_W, IBC_D, pal,
                              color=C_PALLET))
        parts.append(ruby_box(f"{nm} bottle",
                              IBC_COL_X + inset, yd + inset, z0 + pal,
                              IBC_W - 2 * inset, IBC_D - 2 * inset, bottle_h,
                              color=col, alpha=alpha))
    return '\n'.join(parts)


def ruby_tri(name, p1, p2, p3, thick, color=None, alpha=None):
    """Triangular plate: a face through p1,p2,p3 pushpulled by `thick` along its
    normal (used for gusset plates)."""
    face = ', '.join(f'[{mm(p[0])},{mm(p[1])},{mm(p[2])}]' for p in (p1, p2, p3))
    out = [
        f'  # {name}',
        '  grp = ents.add_group',
        f'  grp.name = "{name}"',
        '  ge = grp.entities',
        f'  f = ge.add_face({face})',
        f'  f.pushpull({mm(thick)})',
    ]
    if color:
        rr, gg, bb = hex_to_rgb(color)
        mat_nm = shared_mat_name(name, color, alpha)
        out.append(f'  mat = model.materials["{mat_nm}"] || model.materials.add("{mat_nm}")')
        out.append(f'  mat.color = Sketchup::Color.new({rr}, {gg}, {bb})')
        out.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        out.append('  grp.material = mat')
    out.append('')
    return '\n'.join(out)


def ibc_rack():
    """ibc-reconfig-v2 RESTRAINT frame — a SINGLE FRONT PORTAL.

    The 1000L caged totes DIRECT-STACK (no load-bearing deck — 52mm headroom), are
    non-removable, and are trapped by the side + sealed-end walls. So restraint is
    the front portal + front retaining bars + D-ring lashing; the deep mid/back
    corridor stations of the old load-bearing rack are dropped. The portal (at
    RWK_X_UP=4734) also gives the right-walkway cantilever arms their clamp point
    and mounts the (forward) wet-end panel.
    """
    parts = []
    s = IBC_FRAME_RHS                   # 50×50 RHS
    top_z = 2 * IBC_H_1000 - 40         # 2296 — restraint reaches near the stack top
    yd_near, yd_far = 1046, 1316        # plumbing-corridor edges
    up_yds = (yd_near, yd_far - s)
    fx = RWK_X_UP                       # 4734 — front portal uprights (walkway arms clamp here)
    front_x = IBC_COL_X - 20            # 4654 — front bars seated in the 25mm gap, just in front of the tote face (clear of the film rail at 4649)
    bar_d = 20                          # bar depth in X (50×20×3 RHS — fits the gap; a full 50×50 would cut into the totes)
    c_bolt = "#3A3A42"

    # Front portal: two full-height uprights + top tie + floor beam.
    for yd in up_yds:
        parts.append(ruby_box("Front Portal Upright", fx, yd, 0, s, s, top_z, color=C_STEEL))
    parts.append(ruby_box("Front Portal Top Tie", fx, yd_near, top_z - s, s, yd_far - yd_near, s, color=C_STEEL))
    parts.append(ruby_box("Front Portal Floor Beam", fx, yd_near, 0, s, yd_far - yd_near, s, color=C_STEEL))
    # Panel-mount rail tying the (forward) panel face back to the portal at the top.
    parts.append(ruby_box("Panel Mount Rail", fx, yd_near, EQPANEL_Z_HI - s,
                          (EQPANEL_X + EQPANEL_T) - fx, yd_far - yd_near, s, color=C_STEEL))

    # Floor feet under the two front uprights (150×150×12 plate + 4× M12 anchors).
    fp, ft, bpc = IBC_FOOT_PLATE, IBC_FOOT_PLATE_T, IBC_FOOT_BOLT_PCD // 2
    for yd in up_yds:
        cx, cy = fx + s / 2, yd + s / 2
        parts.append(ruby_box("Foot Flange Plate", cx - fp / 2, cy - fp / 2, 0, fp, fp, ft, color=C_STEEL))
        for dx in (-bpc, bpc):
            for dy in (-bpc, bpc):
                parts.append(ruby_cylinder("Foot Anchor Bolt M12", cx + dx, cy + dy, 0, 7, ft + 4, color=c_bolt, axis="z"))

    # Front retaining bars (50×20×3 RHS) seated in the gap just in front of the tote
    # face, both tiers, tied back to the portal.
    bar_zs = (560, 1760)
    for y0, y1 in ((0, yd_near + s), (yd_far - s, C_WID)):
        for bz in bar_zs:
            parts.append(ruby_box("Front Retaining Bar", front_x, y0, bz, bar_d, y1 - y0, s, color=C_STEEL))
    for yd in up_yds:
        for bz in bar_zs:
            parts.append(ruby_box("Front Bar Stub", front_x, yd, bz, fx - front_x + s, s, s, color=C_STEEL))

    # D-ring lashing holders on the front bars.
    for ydh in (520, C_WID - 520):
        for bz in bar_zs:
            parts.append(ruby_cylinder("D-Ring Holder", front_x - 6, ydh, bz + s / 2, 16, 10, color=C_STEEL, axis="x"))

    # Wall joist hangers (Simpson U-pocket) at each front-bar wall end, through-bolted
    # to an EXTERIOR backing plate (load-spreading, hex heads outside — the thin
    # corrugated wall would otherwise pull through under the totes' transport thrust).
    ext_pt, ext_pw, ext_ph = 8, 100, 135        # exterior plate: 100(X) × 135(Z) × 8 thick
    for wall_yd, din in ((0, 1), (C_WID, -1)):
        for bz in bar_zs:
            ht, dep = 4, 70
            p_y = wall_yd if din > 0 else wall_yd - ht
            s_y = wall_yd if din > 0 else wall_yd - dep
            parts.append(ruby_box("Wall Hanger Plate", front_x - 8, p_y, bz - 30, s + 16, ht, s + 70, color=C_STEEL))
            parts.append(ruby_box("Wall Hanger Seat", front_x - 4, s_y, bz - ht, s + 8, dep, ht, color=C_STEEL))
            # Exterior backing plate just outside the container wall + 4 M12 through-bolts.
            ecx = front_x - 8 + (s + 16) / 2     # plate center X (on the hanger)
            ecz = bz + s / 2                      # plate center Z (on the bar)
            plate_y = (-WALL_T - ext_pt) if din > 0 else (C_WID + WALL_T)
            bolt_cy = (-WALL_T - ext_pt) if din > 0 else (C_WID - 10)
            parts.append(ruby_box("IBC Wall Backing Plate (ext)",
                                  ecx - ext_pw / 2, plate_y, ecz - ext_ph / 2,
                                  ext_pw, ext_pt, ext_ph, color=C_STEEL))
            for dx in (-ext_pw / 2 + 18, ext_pw / 2 - 18):
                for dz in (-ext_ph / 2 + 22, ext_ph / 2 - 22):
                    parts.append(ruby_cylinder("IBC Wall Through-Bolt M12",
                                               ecx + dx, bolt_cy, ecz + dz, 7, 58,
                                               color=c_bolt, axis="y"))

    return '\n'.join(parts)


# ── Film plane mechanism ─────────────────────────────────────────────────────

def film_plane_saddles(corners, skip=()):
    """IBC-style wall-seat saddle at each of the film-plane rail ends (the `corners`
    {id:(x,z)} × near/far wall). Each = interior back-plate + horizontal seat + triangular
    gusset, THROUGH-BOLTED to an EXTERIOR plate (4-bolt) — dims from the IBC wall seats.
    RIGHT rails permanently bolted; LEFT rails thumb-screw drop-in. `skip` omits corner ids
    (rev12: BR is skipped — its corner is the COMBINED plate shared with the right walkway,
    fp_combined_corner_plate). Single-sourced — the film-plane focus model reuses it."""
    pw, pt = IBC_WBKT_PLATE_W, IBC_WBKT_PLATE_T          # 150 plate, 8 thick
    proj, st = IBC_WBKT_SEAT_PROJ, IBC_WBKT_SEAT_T       # 110 seat projection, 10 thick
    gh, wt, sw = 120, WALL_T, 24 + 24                    # gusset, wall, seat width
    parts = []
    for cid, (x, z) in corners.items():
        if cid in skip:
            continue
        left = (x == RAIL_X_L)
        for wall_yd in (0, C_WID):
            near = (wall_yd == 0)
            din = 1 if near else -1
            tag = f"{cid} {'near' if near else 'far'}"
            by_in = 0 if near else C_WID - pt
            by_out = -wt - pt if near else C_WID + wt
            sy0 = min(wall_yd, wall_yd + din * proj)
            yt = wall_yd + din * proj
            parts.append(ruby_box(f"Saddle back-plate {tag}",
                         x - pw / 2, by_in, z - pw / 2, pw, pt, pw, color=C_STEEL))
            parts.append(ruby_box(f"Saddle OUTSIDE plate {tag}",
                         x - pw / 2, by_out, z - pw / 2, pw, pt, pw, color=C_STEEL))
            parts.append(ruby_box(f"Saddle seat {tag}",
                         x - sw / 2, sy0, z - st, sw, proj, st, color=C_STEEL))
            parts.append(ruby_tri(f"Saddle gusset {tag}",
                         (x, yt, z - st), (x, wall_yd, z - st), (x, wall_yd, z - st - gh),
                         8, color=C_STEEL))
            blo, bhi = min(by_in, by_out), max(by_in, by_out) + pt
            for bx in (x - 50, x + 50):
                for bz in (z - 50, z + 50):
                    parts.append(ruby_cylinder(f"Saddle wall bolt M12 {tag}",
                                 bx, blo, bz, 6, bhi - blo, color=C_STEEL, axis="y"))
            hold_c = C_VALVE if left else C_STEEL
            hold_nm = "Thumb screw" if left else "Rail fixing bolt"
            for hy in (sy0 + 25, sy0 + proj - 25):
                parts.append(ruby_cylinder(f"{hold_nm} {tag}",
                             x, hy, z, 5, 36, color=hold_c, axis="z"))
    return '\n'.join(parts)


def film_plane_mechanism():
    """Four corner rails + 8 wall-seat saddles + framed muslin screen.

    Rails run in +Y (depth), now full-width saddle-to-saddle, at the four corners.
    rev11: the demountable brace cage is RETIRED — each rail end anchors to the
    container with an IBC-style wall-seat saddle (the shell carries the rigidity);
    right rails bolted, left rails thumb-screw drop-in for the drum swing. The
    muslin screen sits at the nominal depth FP_Y with a 2" angle frame.
    """
    parts = []
    rail = 40                       # 40×40mm rail tube
    z_bot = RAIL_OFF_BOT            # 150mm off the floor (raised +50 to clear the Z130 walkway)
    z_top = C_HGT - RAIL_OFF - rail # 100mm off the ceiling
    x_left = RAIL_X_L               # 150
    x_right = RAIL_X_R - rail       # 4609
    # All four corner rails CONTINUOUS, now spanning the full width SADDLE-TO-SADDLE
    # (Yd 0 → C_WID) so each end lands on its wall-seat saddle with no gap (rev11).
    for rz, nm in [(z_bot, "BR"), (z_top, "TR"), (z_bot, "BL"), (z_top, "TL")]:
        x = x_right if nm.endswith("R") else x_left
        parts.append(ruby_box(f"FP Rail {nm}",
                              x, 0, rz, rail, C_WID, rail, color=C_STEEL))

    # rev11: the demountable brace cage is RETIRED — each of the 8 rail ends is
    # anchored to the container with an IBC-style wall-seat saddle instead (the
    # container shell carries the rigidity). Right rails bolted, left thumb-screw.
    corners = {"TL": (x_left, z_top), "TR": (x_right, z_top),
               "BL": (x_left, z_bot), "BR": (x_right, z_bot)}
    # rev12: BR corner is the COMBINED plate (built by the right walkway, fp_combined_corner_plate),
    # so skip it here to avoid a duplicate saddle.
    parts.append(film_plane_saddles(corners, skip={"BR"}))

    # Muslin screen — translucent panel at the nominal film-plane depth.
    board_t = 20
    parts.append(ruby_box("Film Plane Screen (muslin)",
                          FP_X_L, FP_Y, 0,
                          FP_W, board_t, FP_H,
                          color=C_FILM, alpha=0.3))

    # 2" steel angle frame around the screen, on the pinhole-facing side.
    leg = FP_ANGLE_LEG  # 50.8mm
    fy = FP_Y - leg
    parts.append(ruby_box("FP Frame Bottom",
                          FP_X_L, fy, 0, FP_W, leg, leg, color=C_STEEL))
    parts.append(ruby_box("FP Frame Top",
                          FP_X_L, fy, FP_H - leg, FP_W, leg, leg, color=C_STEEL))
    parts.append(ruby_box("FP Frame Left",
                          FP_X_L, fy, 0, leg, leg, FP_H, color=C_STEEL))
    parts.append(ruby_box("FP Frame Right",
                          FP_X_R - leg, fy, 0, leg, leg, FP_H, color=C_STEEL))

    return '\n'.join(parts)


# ── Light-trap drum (revolving entry) ────────────────────────────────────────

def ruby_arc_wall(name, cx, cy, r, wall_t, height, gap_center_deg, gap_deg,
                  color=None, alpha=None, n=48, z0=0):
    """Hollow curved wall (annular sector, extruded in +Z) with a gap.

    The gap (an opening of `gap_deg` centerd on `gap_center_deg`) reads as a
    doorway/entry slot in the cylinder. Built as a closed band polygon (outer
    arc forward + inner arc back) at base height `z0` then pushpulled `height`.
    """
    ri = r - wall_t
    a0 = math.radians(gap_center_deg + gap_deg / 2.0)
    a1 = math.radians(gap_center_deg + 360.0 - gap_deg / 2.0)
    pts = []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    for i in range(n, -1, -1):
        a = a0 + (a1 - a0) * i / n
        pts.append((cx + ri * math.cos(a), cy + ri * math.sin(a)))
    pts_ruby = ', '.join(f'[{mm(round(x, 2))},{mm(round(y, 2))},{mm(z0)}]' for x, y in pts)

    lines = [
        f'  # {name}',
        f'  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  ge = grp.entities',
        f'  face = ge.add_face([{pts_ruby}])',
        f'  face.reverse! if face.normal.z < 0',
        f'  face.pushpull({mm(height)})',
    ]
    if color:
        r_, g_, b_ = hex_to_rgb(color)
        mat_nm = shared_mat_name(name, color, alpha)
        lines.append(f'  mat = model.materials["{mat_nm}"] || '
                     f'model.materials.add("{mat_nm}")')
        lines.append(f'  mat.color = Sketchup::Color.new({r_}, {g_}, {b_})')
        lines.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        lines.append(f'  grp.material = mat')
    lines.append('')
    return '\n'.join(lines)

def light_trap_drum():
    """Housed revolving-door light lock at the cargo-door end (rev 8).

    Reuses the detailed builder from the dedicated Light-Trap model so the two
    models stay in sync (same pattern as spray_bar()): a FIXED Ø900 housing with
    two opposed 80° openings (exterior + interior-onto-walkway, 180° apart) and a
    single-opening C-shell drum (~Ø850 bore) rotating inside on SKF 6215 bearings.
    No internal fins — light-tight by geometry. Centered at (DRUM_CX=0, DRUM_CY).
    Replaces the failed Ø750 4-fin drum (see light-trap-selection.md §3)."""
    import generate_lighttrap_model as lt
    return lt.drum()


def light_trap_frame():
    """Cargo-door RHS frame (50×50×3 RHS) + the top & bottom seal lips.

    Reused from the Light-Trap model (same pattern as light_trap_drum) so the
    overview stays in sync. The bottom seal lip closes the 80mm floor gap and the
    top seal lip closes the panel-top gap — together they block light top and
    bottom; the EPDM perimeter seal (light_seal) compresses against them."""
    import generate_lighttrap_model as lt
    return lt.door_frame()


def light_trap_bay():
    """B2 punch-out bay — reused from the Light-Trap model so it stays in sync."""
    import generate_lighttrap_model as lt
    return lt.bay()


# ── Solar array (ground tilt frame, exterior) ────────────────────────────────

def tilted_slab(name, x, y_near, z_base, w, length, t, tilt_deg, color, alpha=None):
    """Flat slab tilted up from its near-bottom edge, rising in +Z and -Y (faces
    away from the container, toward the sun). length runs up the tilt."""
    th = math.radians(tilt_deg)
    dy, dz = -length * math.cos(th), length * math.sin(th)
    corners = [(x, y_near, z_base), (x + w, y_near, z_base),
               (x + w, y_near + dy, z_base + dz), (x, y_near + dy, z_base + dz)]
    pts = ', '.join(f'[{mm(px)},{mm(py)},{mm(pz)}]' for px, py, pz in corners)
    r, g, b = hex_to_rgb(color)
    mat_nm = shared_mat_name(name, color, alpha)
    return '\n'.join([
        f'  # {name}',
        '  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  face = grp.entities.add_face({pts})',
        f'  face.pushpull({mm(t)})',
        f'  mat = model.materials["{mat_nm}"] || model.materials.add("{mat_nm}")',
        f'  mat.color = Sketchup::Color.new({r}, {g}, {b})',
        f'  mat.alpha = {alpha if alpha is not None else 1.0}',
        '  grp.material = mat', ''])


def solar_array():
    """3x 200W panels on a 30deg ground tilt frame, exterior of the pinhole wall,
    door-end so the right edge clears the pinhole sightline; + PV run to the panel.
    Shared with the focused electrical model (generate_electrical_model.py)."""
    p = []
    th = math.radians(SOLAR_TILT_DEG)
    pitch = SOLAR_PANEL_W + SOLAR_GAP
    for i in range(SOLAR_N):
        x = SOLAR_ARRAY_X + i * pitch
        p.append(tilted_slab(f"Solar Panel {i + 1} (200W)", x, SOLAR_ARRAY_YD,
                             SOLAR_ARRAY_Z + 120, SOLAR_PANEL_W, SOLAR_PANEL_L,
                             SOLAR_PANEL_T, SOLAR_TILT_DEG, "#1B3A6B"))
    span = (SOLAR_N - 1) * pitch + SOLAR_PANEL_W
    back_yd = SOLAR_ARRAY_YD - SOLAR_PANEL_L * math.cos(th)
    top_z = SOLAR_ARRAY_Z + 120 + SOLAR_PANEL_L * math.sin(th)
    p.append(ruby_box("Tilt Frame front rail", SOLAR_ARRAY_X, SOLAR_ARRAY_YD - 20,
                      SOLAR_ARRAY_Z, span, 40, 120, color=C_STEEL))
    p.append(ruby_box("Tilt Frame back rail", SOLAR_ARRAY_X, back_yd - 20,
                      SOLAR_ARRAY_Z, span, 40, 60, color=C_STEEL))
    for x in (SOLAR_ARRAY_X, SOLAR_ARRAY_X + span - 40):
        p.append(ruby_box("Tilt Frame back leg", x, back_yd - 20, SOLAR_ARRAY_Z,
                          40, 40, top_z - SOLAR_ARRAY_Z, color=C_STEEL))
    # PV run: array junction -> up to the external power panel MC4 bulkheads.
    jx = SOLAR_ARRAY_X + span / 2
    panel = (PWR_PANEL_X + 70, -WALL_T - 30, PWR_PANEL_Z + PWR_PANEL_H * 0.5)
    # Flexible PV lead (array -> panel MC4) — a SOFT connector, drawn as a curly coil
    # cord (ruby_coil_cord) to distinguish it from the rigid orthogonal conduit. Thinner
    # conductor (r=5 vs the conduit's 10) reinforces the soft/hard read. The final leg
    # drapes DIAGONALLY from the ground up to the panel (not a straight vertical rise) so
    # it stays right of and clear of the evap cooler (X720-1280) — a flexible cord can take
    # the angle a rigid orthogonal conduit can't.
    p.append(ruby_coil_cord("PV cord (array -> panel, flexible)",
                            [(jx, SOLAR_ARRAY_YD - 20, SOLAR_ARRAY_Z + 60),
                             (jx, -WALL_T - 30, SOLAR_ARRAY_Z + 60),
                             panel],
                            r=5, color="#2D7A2D"))
    return '\n'.join(p)


# ── Electrical (panel + battery, pinhole wall) ───────────────────────────────

def electrical():
    """Electrical panel (EP) + battery bank on the pinhole wall (Yd=0), plus the
    flush-mount external power panel on the exterior face.

    EP mounts high (Z 1600–2200); the slim battery bank low (Z 100–600). Both
    protrude into the container from the pinhole wall. The external power panel
    is flush in the exterior face (ghosted) — no interior conflict.
    """
    parts = []

    # ── EP internals — detail ported from the electrical model's "Power Core"
    # (generate_electrical_model.py power_core()); DUPLICATED geometry, keep the two
    # in sync (cf. the walkway-bracket duplication). The old single solid EP box is
    # replaced by a ghosted IP65 enclosure exposing the MPPT, the Blue Sea 5026 fuse
    # stack (7 blades A–G, one per circuit), the +/- busbars and the rotary main
    # disconnect — so the overview's EP conforms to the electrical schematic. ────────
    ez, eh = EP_H_LO, EP_H_HI - EP_H_LO

    # circuit color + fuse rating per branch A–G (matches generate_electrical_model CCT)
    ep_cct = {"A": "#C0392B", "B": "#E67E22", "C": "#2980B9", "D": "#8E44AD",
              "E": "#16A085", "F": "#7F8C8D", "G": "#F1C40F"}
    ep_load = {"A": "exhaust fan", "B": "intake fan", "C": "water pumps", "D": "safelight",
               "E": "cooler / inverter", "F": "actuators (spare)", "G": "white LED"}
    ep_fuse_order = ["A", "B", "C", "D", "E", "F", "G"]
    ep_fuse_rating = {"A": "5A", "B": "5A", "C": "15A", "D": "5A",
                      "E": "40A", "F": "20A", "G": "10A"}

    # fuse-stack geometry (mirrors the electrical model's module constants)
    fblk_x0, fblk_yd, fblk_z0, fbase_h = EP_X + 15, 25, ez + 270, 28
    fuse_w, fuse_t, fuse_h = 13, 9, 42
    fuse_pitch = FUSEBLK_W / len(ep_fuse_order)
    fuse_yd = fblk_yd + (FUSEBLK_D - fuse_t) / 2

    # Ghosted IP65 enclosure (was the solid "Electrical Panel (EP)" box).
    parts.append(ruby_box("Electrical Panel (EP enclosure, IP65)",
                          EP_X - 12, 0, ez - 12,
                          EP_W + 24, ENCL_SHELL_D + 6, eh + 24, color=C_ELEC, alpha=0.14))
    # Victron SmartSolar 100/50 MPPT (top of the enclosure).
    parts.append(ruby_box("MPPT Controller (Victron 100/50)",
                          EP_X + 15, 25, EP_H_HI - MPPT_H - 30,
                          MPPT_W, MPPT_D, MPPT_H, color="#3A5BA0"))
    # Blue Sea 5026 block base + a standing row of 7 blade fuses, coloured per circuit.
    parts.append(ruby_box("Fuse Block base (Blue Sea 5026)",
                          fblk_x0, fblk_yd, fblk_z0, FUSEBLK_W, FUSEBLK_D, fbase_h,
                          color="#2B2B30"))
    for i, c in enumerate(ep_fuse_order):
        cx = fblk_x0 + (i + 0.5) * fuse_pitch
        parts.append(ruby_box(f"Fuse {c} ({ep_fuse_rating[c]} — {ep_load[c]})",
                              cx - fuse_w / 2, fuse_yd, fblk_z0 + fbase_h,
                              fuse_w, fuse_t, fuse_h, color=ep_cct[c]))
    # +/- distribution busbars.
    parts.append(ruby_box("Busbar (+)", EP_X + 15, 30, ez + 205,
                          BUSBAR_L, BUSBAR_W, BUSBAR_H, color="#C0392B"))
    parts.append(ruby_box("Busbar (-)", EP_X + 15, 30, ez + 175,
                          BUSBAR_L, BUSBAR_W, BUSBAR_H, color="#2C2C2C"))
    # Rotary main disconnect — knob on the enclosure face (Yd).
    disc_x = EP_X + 240
    parts.append(ruby_cylinder("Main Disconnect (Blue Sea m-Series)",
                               disc_x, ENCL_SHELL_D, ez + 120,
                               DISCONNECT_D / 2, DISCONNECT_H, color="#D43A2F", axis="y"))
    # Disconnect LOAD terminal → busbar(+) link (so the bank isolates when the knob is OFF).
    parts.append(ruby_pipe_run("Main feed (disconnect -> busbar +)",
                               [(disc_x, 130, ez + 155), (disc_x, 45, ez + 155),
                                (disc_x, 45, ez + 205), (EP_X + 15 + BUSBAR_L, 45, ez + 205)],
                               11, color="#8B1A1A"))

    # Battery bank — the standard build fits 1× LiFePO4 (cost). The 2nd position is
    # provisioned (the busbar/conduit below already serve it) and shown GHOSTED as a
    # plug-in expansion: drop a 2nd pack in and parallel it onto the busbar, no rewiring.
    bw = (BA_W - 20) / 2
    bat_specs = [
        (BA_X,            "Battery 1 (12V 100Ah LiFePO4)",                      1.0),
        (BA_X + bw + 20,  "Battery 2 (optional 2nd pack — plug-in, ghosted)",   0.28),
    ]
    for bx, nm, al in bat_specs:
        parts.append(ruby_box(nm, bx, 0, BA_H_LO,
                              bw, BA_D, BA_H_HI - BA_H_LO, color=C_BATT, alpha=al))

    # External power panel — flush in the exterior face (Yd<0), shown ghosted.
    parts.append(ruby_box("Ext. Power Panel (exterior)",
                          PWR_PANEL_X, -WALL_T - 25, PWR_PANEL_Z,
                          PWR_PANEL_W, 25, PWR_PANEL_H, color=C_ALUM, alpha=0.5))
    # It penetrates the wall — interior face rectangle matching the exterior.
    parts.append(ruby_box("Ext. Power Panel (interior face)",
                          PWR_PANEL_X, 0, PWR_PANEL_Z,
                          PWR_PANEL_W, 20, PWR_PANEL_H, color=C_ELEC))

    # Battery contactor (Blue Sea ML-RBS) — magnetic-latch switch in the battery (+)
    # feed, sitting on top of Battery 1. Tripped by the external E-stop below.
    parts.append(ruby_box("Battery Contactor (ML-RBS, in + feed)",
                          BA_X + 20, 15, BA_H_HI,
                          120, 90, 100, color="#C42B1C"))

    # Battery main DC cables — without these the bank reads as floating. Ported from the
    # electrical model's battery() so the EP internals are actually fed:
    #   (+) post -> contactor -> MRBF main fuse -> main disconnect LINE terminal (the
    #   disconnect -> busbar(+) link lives in the EP internals, so the whole bank isolates
    #   when the knob is OFF);  (-) post -> busbar(-).
    # The (+) riser threads up at X≈1715 (between the lower stay-anchor bolts, Yd 45 clears
    # the anchor eye); the (-) riser starts at X≈1760, clear (right) of the contactor/MRBF.
    disc_x, disc_z = EP_X + 240, EP_H_LO + 120          # main disconnect centre (matches EP internals)
    parts.append(ruby_box("MRBF Main Fuse (on + post)",
                          BA_X + CONTACTOR_W + 35, 20, BA_H_HI,
                          MRBF_D, MRBF_D, MRBF_H, color="#222222"))
    parts.append(ruby_pipe_run("Battery + cable (2/0 AWG, MRBF -> main disconnect)",
                               [(BA_X + CONTACTOR_W + 55, 45, BA_H_HI + MRBF_H),
                                (BA_X + CONTACTOR_W + 55, 45, disc_z - 35),
                                (disc_x, 45, disc_z - 35),
                                (disc_x, 130, disc_z - 35)],
                               11, color="#8B1A1A"))
    parts.append(ruby_pipe_run("Battery - cable (2/0 AWG -> busbar -)",
                               [(BA_X + 220, 60, BA_H_HI),
                                (BA_X + 220, 60, EP_H_LO + 186),
                                (EP_X + 35, 60, EP_H_LO + 186)],
                               11, color="#202020"))

    # External emergency cut-off (E-stop) — red mushroom on a yellow collar, on the
    # exterior face of the power panel (Yd<0), so all DC can be killed from outside.
    es_cx = PWR_PANEL_X + PWR_PANEL_W / 2
    es_cz = PWR_PANEL_Z + PWR_PANEL_H / 2
    face_y = -WALL_T - 25
    parts.append(ruby_cylinder("E-stop collar (safety yellow)",
                               es_cx, face_y - 12, es_cz, 35, 12,
                               color="#F2C200", axis="y"))
    parts.append(ruby_cylinder("E-stop button (red mushroom)",
                               es_cx, face_y - 40, es_cz, 26, 28,
                               color="#C42B1C", axis="y"))

    # Low-current control loop: contactor → external E-stop (2× 18 AWG through a gland).
    # Route the riser LEFT of the chem shelf (X1180-1780): going right is boxed in by the
    # transport-stay wall anchors (X≈1695-1895, plates at Z400-600 & 1950-2150) and the EP
    # (X1910). Left of the shelf the corridor is clear top-to-bottom — cross left past the
    # shelf's left edge at contactor height, rise, then over to the panel above the shelf.
    estop_riser_x = SHELF_X_L - 60                   # 1120 — clear of shelf, stay anchor & EP
    parts.append(ruby_pipe_run("E-stop control wire (2x 18 AWG)",
                               [(BA_X + 80, 60, BA_H_HI + 100),
                                (estop_riser_x, 60, BA_H_HI + 100),
                                (estop_riser_x, 60, es_cz),
                                (es_cx, 60, es_cz),
                                (es_cx, 10, es_cz)],
                               5, color="#6A3DA8"))

    # Remaining panel-face hardware — matches the 2D power-panel detail (View A):
    # MC4 PV bulkheads (3 pairs, left), NEMA 5-15R inlet (top-right), Deutsch DT
    # cooler bulkhead (bottom-right). Positions are panel-local fractions, protruding
    # from the same exterior face as the E-stop.
    def _px(uf): return PWR_PANEL_X + uf * PWR_PANEL_W
    def _pz(vf): return PWR_PANEL_Z + vf * PWR_PANEL_H

    for i, vf in enumerate((0.225, 0.5, 0.775)):
        z = _pz(vf)
        parts.append(ruby_cylinder(f"MC4 PV{i + 1} (+)", _px(0.192), face_y - 20, z,
                                   8, 20, color="#2D7A2D", axis="y"))
        parts.append(ruby_cylinder(f"MC4 PV{i + 1} (-)", _px(0.275), face_y - 20, z,
                                   8, 20, color="#9AA0A6", axis="y"))

    parts.append(ruby_box("NEMA 5-15R inlet (panel)",
                          _px(0.742) - 30, face_y - 30, _pz(0.878) - 22,
                          60, 30, 45, color="#FFF0CC"))

    parts.append(ruby_cylinder("GFCI AC outlet (Cct E cooler)",
                               _px(0.767), face_y - 20, _pz(0.325),
                               10, 20, color="#E8884A", axis="y"))

    # PV interior feed: MC4 bulkheads (panel interior face) -> MPPT PV input. The exterior
    # PV run (solar_array()) lands on the MC4 connectors; this is the conductor from their
    # interior side into the MPPT. Crosses UNDER the upper transport-stay anchor (X1695-1895,
    # Z1950-2150) at the bottom MC4 height (Z≈1884) and over the fuse block (top Z≈1840),
    # then rises into the MPPT at Yd 85 (clear of the fuse block at Yd 25-70). Duplicated in
    # the electrical model's power_core() — keep in sync.
    mc4_x = _px(0.23)                          # between the MC4 (+)/(-) columns
    mc4_z = _pz(0.225)                         # bottom MC4 pair (below the stay anchor)
    mppt_in_x = EP_X + 40
    mppt_in_z = EP_H_HI - MPPT_H - 32          # just under the MPPT bottom (PV input)
    parts.append(ruby_pipe_run("PV feed (MC4 bulkheads -> MPPT)",
                               [(mc4_x, 22, mc4_z),
                                (mc4_x, 85, mc4_z),
                                (mppt_in_x, 85, mc4_z),
                                (mppt_in_x, 85, mppt_in_z)],
                               9, color="#2D7A2D"))

    return '\n'.join(parts)


# ── Chemistry prep shelf (ceiling-hung) ──────────────────────────────────────

def shelf():
    """Chemistry prep shelf — WALL-HINGED FOLD-DOWN, shown DEPLOYED (rev13).

    A 600×300mm board hinged on the pinhole wall (Yd0) at work height Z=SHELF_H, in
    the widened walkway LEFT of the batteries. A piano hinge along the back edge + 2
    stays from the wall above hold it level (the stays carry the load). It folds UP
    flat against the wall for transport (top Z=SHELF_STOW_TOP_Z); only deployed while
    mixing (film plane parked), so it never meets the film-plane swing.
    """
    parts = []
    z0 = SHELF_H - SHELF_T
    parts.append(ruby_box("Chem Shelf (board, deployed)",
                          SHELF_X_L, SHELF_YD_NEAR, z0,
                          SHELF_W, SHELF_DEPTH, SHELF_T, color=C_SHELF))
    # spill lip — front edge + two ends
    lip = 15
    parts.append(ruby_box("Chem Shelf lip (front)",
                          SHELF_X_L, SHELF_YD_FAR - 6, SHELF_H, SHELF_W, 6, lip, color=C_SHELF))
    for ex in (SHELF_X_L, SHELF_X_R - 6):
        parts.append(ruby_box("Chem Shelf lip (end)",
                              ex, SHELF_YD_NEAR, SHELF_H, 6, SHELF_DEPTH, lip, color=C_SHELF))
    # piano hinge along the back edge on the pinhole wall
    parts.append(ruby_cylinder("Chem Shelf piano hinge",
                               SHELF_X_L, SHELF_YD_NEAR, SHELF_H - 6, 6, SHELF_W,
                               color=C_STEEL, axis="x"))
    # two stays from the wall above the hinge to the front corners — carry the load
    stay_z = SHELF_H + 230
    for sx in (SHELF_X_L + 25, SHELF_X_R - 25):
        parts.append(ruby_pipe("Chem Shelf stay",
                               (sx, SHELF_YD_NEAR, stay_z), (sx, SHELF_YD_FAR - 10, SHELF_H),
                               6, color=C_STEEL))
        parts.append(ruby_box("Chem Shelf stay anchor",
                              sx - 12, SHELF_YD_NEAR, stay_z - 12, 24, 8, 24, color=C_STEEL))
    return '\n'.join(parts)


# ── Light sealing (EPDM perimeter seal + hinges) ─────────────────────────────

def light_seal():
    """EPDM perimeter light seal + hinges for the cargo-door light-trap panel.

    The hinged panel (cargo-door end, X≈0, with the revolving drum in its
    center) light-seals against the container opening. The EPDM gasket runs as
    a frame around the opening perimeter on the panel's EXTERIOR face,
    SANDWICHED against the fixed door frame (interface 1 — hinge panel → frame,
    compressed by the cam latches); matches the light-trap model. (rev10: the
    panel pivots on the Ø89 post — no left-edge barrel hinges.)
    """
    parts = []
    gw, gt = 40, 20                    # gasket face width, thickness in X
    x0 = -gt                           # -20 — panel EXTERIOR face, gasket X=-20..0,
                                       # sandwiched against the door frame (X=-50..0)
    z_bot, z_top = PANEL_FLOOR_GAP, C_HGT   # 80 … 2388 opening
    yd_max = C_WID                     # 2362

    # Perimeter gasket frame — 4 strips around the opening (YZ plane at X≈0,
    # panel exterior face).
    parts.append(ruby_box("EPDM Seal Bottom",
                          x0, 0, z_bot, gt, yd_max, gw, color=C_GASKT))
    parts.append(ruby_box("EPDM Seal Top",
                          x0, 0, z_top - gw, gt, yd_max, gw, color=C_GASKT))
    parts.append(ruby_box("EPDM Seal Left",
                          x0, 0, z_bot, gt, gw, z_top - z_bot, color=C_GASKT))
    parts.append(ruby_box("EPDM Seal Right",
                          x0, yd_max - gw, z_bot, gt, gw, z_top - z_bot,
                          color=C_GASKT))

    # (rev10: the left-edge barrel hinges + swing-support caster are retired — the panel
    # now pivots on the Ø89 post at the far-left upright, see panel_pivot(). Only the
    # cam-latch-compressed EPDM perimeter seal remains here.)

    return '\n'.join(parts)


# ── Lighting & wiring (trunking, LEDs, safelights, switches, conduit) ─────────

def lighting_wiring():
    """Ceiling cable trunking + white LED panels (Cct G) + red safelight strips
    (Cct D) + pull-cord switches + conduit drops.

    Trunking runs the pinhole-wall ceiling line (Yd≈0, outside the optical
    cone); LED panels are centered across the width; safelights span the width
    in the gaps; pull switches hang from the pinhole wall near the EP.
    """
    parts = []
    cz = C_HGT                                 # ceiling

    # Cable trunking — 40×25 PVC along the pinhole wall ceiling, full length.
    parts.append(ruby_box("Cable Trunking (40x25 PVC)",
                          0, 0, cz - 25, C_LEN, 40, 25, color=C_TRUNK))

    # White LED panels (Cct G) — 3× 600×300, ceiling-surface, centered in Yd.
    # Ghosted (translucent) — they read as light sources, not solid blocks.
    led_w, led_d = 600, 300
    led_yd = C_WID / 2 - led_d / 2
    for lx in (1000, 2900):
        parts.append(ruby_box("White LED Panel (Cct G)",
                              lx, led_yd, cz - 40, led_w, led_d, 40,
                              color=C_LED_W, alpha=0.4))
    # Right-hand panel rotated 90° (300 X × 600 Yd) and shifted clear of the
    # equipment-panel conduits: its IBC-end edge sits 150mm left of the panel
    # face (X=EQPANEL_X), so its feed conduit no longer crosses Circuit C.
    rled_x0 = EQPANEL_X - 150 - led_d      # 4550 — span X 4550–4850
    rled_y0 = C_WID / 2 - led_w / 2        # 881  — span Yd 881–1481, centered
    parts.append(ruby_box("White LED Panel (Cct G)",
                          rled_x0, rled_y0, cz - 40, led_d, led_w, 40,
                          color=C_LED_W, alpha=0.4))

    # Red safelight strips (Cct D) — 3× N–S across the width, in the panel gaps.
    for sx in (500, 2250, 4150):
        parts.append(ruby_box("Safelight Strip (Cct D)",
                              sx, 100, cz - 25, 40, C_WID - 200, 18,
                              color=C_SAFE, alpha=0.4))

    # Pull-cord switches (D, G) — CEILING-mounted, in the ~80mm clear band ahead
    # of the pinhole wall (film carriage starts at Yd=100) and left of the EP
    # (X<1910) + the transport-stay anchor (X1594–1794) so they clear both.
    sw_yd = 45                         # off the wall, past the trunking, clear of carriage
    for swx in (1450, 1530):
        parts.append(ruby_box("Pull Switch (ceiling)",
                              swx, sw_yd, cz - 40, 40, 40, 40, color=C_SWITCH))
        # beaded-chain pull cord: alternating bead radii read it as a flexible
        # cord (the 3D analogue of the 2D cord hatching) + a pull knob at the end
        cordx, cordy = swx + 20, sw_yd + 20
        # bottom clears the deployed chem shelf below it (X1180-1780, top Z≈1090): both
        # cords hang inside the shelf footprint, so they end just above it (shared constant).
        z0, z1 = PULL_CORD_BOTTOM_Z, cz - 40
        nb = max(8, int((z1 - z0) / 20))
        bh = (z1 - z0) / nb
        for k in range(nb):
            rr = 3.5 if k % 2 == 0 else 2.0
            parts.append(ruby_cylinder("Pull Cord", cordx, cordy, z0 + k * bh,
                                       rr, bh, color=C_CORD, axis="z", n=8))
        parts.append(ruby_cylinder("Pull Cord Knob", cordx, cordy, z0 - 16,
                                   6, 16, color=C_CORD, axis="z", n=10))

    # Conduit drop (10mm) from trunking down to the stacked battery bank + EP, which
    # are co-located at X≈1810–2310 (the EP sits above the battery). A single drop at
    # X2060 runs down the EP center face (Z1500–2100) and continues to the battery top.
    # (rev: the old second drop at X1750 was removed — the EP moved to X1910, leaving
    #  that drop orphaned over the swing-panel transport-lock stay plate.)
    for cxc, zbot in ((2060, 600),):
        parts.append(ruby_box("Conduit Drop (10mm)",
                              cxc, 8, zbot, 10, 10, (cz - 25) - zbot, color=C_TRUNK))

    # Conduit runs along the ceiling from the trunking out to each fixture.
    cr, czc = 7, cz - 38
    for lx in (1000, 2900):    # → white LED panels (Cct G)
        # (rev13: the +150 middle-conduit shift is retired — the chem shelf is now a
        #  WALL-HINGED fold-down with no ceiling hanger rods to clear.)
        parts.append(ruby_cylinder("Conduit to LED Panel (Cct G)",
                                   lx + led_w / 2, 40, czc, cr, led_yd - 40,
                                   color=C_TRUNK, axis="y"))
    # → rotated right-hand LED panel: conduit to its near Yd edge (no longer
    #   running alongside the equipment-panel / Circuit C conduits)
    parts.append(ruby_cylinder("Conduit to LED Panel (Cct G)",
                               rled_x0 + led_d / 2, 40, czc, cr, rled_y0 - 40,
                               color=C_TRUNK, axis="y"))
    for sx in (500, 2250, 4150):     # → red safelight strips (Cct D)
        parts.append(ruby_cylinder("Conduit to Safelight (Cct D)",
                                   sx + 20, 40, czc, cr, 60,
                                   color=C_TRUNK, axis="y"))

    # Circuit C — feed to the pump/filter equipment panel (IBC corridor).
    # Branch off the ceiling trunking (Yd≈0) across to the panel center
    # (Yd≈1181), then drop to the top of the pump zone (Z=PUMP_H_HI) at the
    # panel face (X=EQPANEL_X). Runs at ceiling height (Z=2350), clearing the IBC stack top (Z=2336).
    pc_yd = EQPANEL_YD + EQPANEL_YD_SPAN / 2
    parts.append(ruby_cylinder("Conduit to Equipment Panel (Cct C)",
                               EQPANEL_X, 40, czc, cr, pc_yd - 40,
                               color=C_TRUNK, axis="y"))
    parts.append(ruby_box("Conduit Drop to Pumps (Cct C)",
                          EQPANEL_X - 5, pc_yd - 5, PUMP_H_HI, 10, 10,
                          (cz - 25) - PUMP_H_HI, color=C_TRUNK))

    # Conduits to the ventilation fans (orthogonal runs off the ceiling trunking,
    # per skill_plumbing_drawing — ruby_pipe_run with elbows, right-angle entry).
    fcr = 7                                          # conduit radius (Ø14)
    czr = cz - 30                                    # conduit ceiling run height (2358)
    # → Fan A (exhaust, Cct A): fixed on the far/sealed end wall (now far-Yd side,
    #   rev9/B2 swap), high near the ceiling. Tap the trunking, cross in Yd over the
    #   IBC stack (no moving parts at the sealed end), drop onto the fan-frame top
    #   (perpendicular entry). Rigid all the way — Fan A doesn't move.
    fa_x = (C_LEN - DUCT_DEPTH) + FAN_BODY_D / 2     # fan-body center X (5618)
    fa_top = FAN_A_H + DUCT_HEIGHT / 2               # fan-housing top Z (2300)
    parts.append(ruby_pipe_run("Conduit to Fan A (exhaust, Cct A)",
                               [(fa_x, 20, czr),
                                (fa_x, FAN_A_YD, czr),
                                (fa_x, FAN_A_YD, fa_top)],
                               fcr, color=C_TRUNK))
    # → Fan B (intake, Cct B): in the NEAR corner by the pinhole wall (rev9/B2 swap).
    #   The rigid conduit taps the ceiling trunking and DROPS STRAIGHT DOWN THE PINHOLE
    #   WALL (Yd≈18) at X≈300 (near the door end, by Fan B) to a wall-mounted electrical
    #   box at the fan's height (FAN_B_H). Cct B terminates in that box — on the FIXED
    #   wall, clear of the swing arc. A short FLEXIBLE CONNECTOR jumps from the box to
    #   Fan B on the swing panel (electrical-report §Circuit B, Deutsch DT — NOT
    #   modeled); it is UNPLUGGED before the panel swings ~56° for transport, so no
    #   wiring crosses the moving joint.
    fb_drop_x = 300                                  # near the door end, by Fan B
    fb_wall_yd = 18                                  # conduit hugs the pinhole wall
    fb_box_z = FAN_B_H                               # wall electrical box at the fan's height
    parts.append(ruby_pipe_run("Conduit to Fan B (intake, Cct B)",
                               [(fb_drop_x, fb_wall_yd, czr),
                                (fb_drop_x, fb_wall_yd, fb_box_z + 45)],
                               fcr, color=C_TRUNK))
    parts.append(ruby_box("Fan B electrical box (Cct B — flex connector to fan, unplugged for swing)",
                          fb_drop_x - 40, 0, fb_box_z - 45, 80, 60, 90, color=C_SWITCH))
    # The short FLEXIBLE CONNECTOR from the fixed wall box out to Fan B on the swing panel —
    # now drawn (a SOFT cord) as a curly coil, distinguishing it from the rigid Cct B conduit
    # feeding the box. This is the jumper that is unplugged before the panel swings.
    parts.append(ruby_coil_cord("Fan B flex connector (box -> fan, Cct B)",
                                [(fb_drop_x, 55, fb_box_z),
                                 (60, FAN_B_YD, FAN_B_H)],
                                r=5, color="#E67E22"))

    return '\n'.join(parts)


# ── Evaporative cooler + vent duct (exterior) ────────────────────────────────

def evap_cooler():
    """External evaporative cooler + supply duct through the pinhole wall.

    The cooler sits on the exterior of the pinhole wall; a Ø200 duct passes
    through the wall penetration (X=1000, Z=1900) into the container.
    """
    parts = []
    ext = -WALL_T
    cw, cd, ch = EVAP_W, EVAP_D, EVAP_H          # 559 × 305 × 711 (Hessaire MC18M)
    # Cooler unit standing on the GROUND outside the pinhole wall.
    parts.append(ruby_box("Evap Cooler (on ground)",
                          EVAP_DUCT_X - cw / 2, ext - cd - 100, 0,
                          cw, cd, ch, color=C_EVAP))

    # Circuit-E inverter (Victron Phoenix 12/375 GFCI) — INTERIOR, wall-mounted on
    # the pinhole wall below the EP / above the battery; converts 12V→120V for the
    # cooler.  See electrical-report.md §7.6 (AC isolation & safety).
    parts.append(ruby_box("Cct E Inverter (12->120V AC)",
                          INVERTER_X, 0, INVERTER_Z,
                          INVERTER_W, INVERTER_D, INVERTER_H, color="#404848"))

    # Cct E 120V AC line: inverter output -> the external panel's GFCI outlet (interior
    # face), which then runs the cooler cord outside. Ported from the electrical model's
    # inverter(); routed LEFT under the EP enclosure at the inverter-top height (Z≈1415,
    # below the busbars/fuses and the upper stay anchor), then up to the GFCI on the panel.
    gfci_x = PWR_PANEL_X + 0.767 * PWR_PANEL_W
    gfci_z = PWR_PANEL_Z + 0.325 * PWR_PANEL_H
    inv_top = INVERTER_Z + INVERTER_H
    parts.append(ruby_pipe_run("Cct E AC line (inverter -> panel GFCI)",
                               [(INVERTER_X + INVERTER_W / 2, 30, inv_top),
                                (gfci_x, 30, inv_top),
                                (gfci_x, 30, gfci_z),
                                (gfci_x, 18, gfci_z)],
                               7, color="#E8884A"))

    # Cct E cooler power cord (panel GFCI -> cooler) — a SOFT flexible connector, drawn as a
    # curly coil that DRAPES DIAGONALLY from the GFCI outlet down to the cooler-top inlet
    # (not a straight drop), so it angles clear of the cooler body until the straight
    # terminating stub plugs in.
    cooler_inlet = (EVAP_DUCT_X + cw / 2 - 80, ext - cd / 2 - 100, ch - 70)
    parts.append(ruby_coil_cord("Cct E cooler cord (panel GFCI -> cooler, flexible)",
                                [(gfci_x, ext - 30, gfci_z), cooler_inlet],
                                r=5, color="#E8884A"))

    # Cold-air duct inlet — a Ø200 circle through the wall (axis into container).
    parts.append(ruby_cylinder("Cold-Air Duct Inlet (Ø200)",
                               EVAP_DUCT_X, ext - 5, EVAP_DUCT_Z,
                               EVAP_DUCT_D / 2, WALL_T + 10,
                               color=C_DUCT, axis="y"))

    # Ø200 corrugated flex duct: vertical riser off the cooler outlet, right-angle
    # elbow, then horizontal into the wall inlet (orthogonal, per pipe convention).
    cooler_top = (EVAP_DUCT_X, ext - 100 - cd / 2, ch)
    elbow_pt = (EVAP_DUCT_X, ext - 100 - cd / 2, EVAP_DUCT_Z)
    wall_mouth = (EVAP_DUCT_X, ext - 5, EVAP_DUCT_Z)
    parts.append(ruby_flex_run("Evap Flex Duct",
                               [cooler_top, elbow_pt, wall_mouth],
                               EVAP_DUCT_D / 2, color=C_DUCT))

    return '\n'.join(parts)


# ── Water / waste hookups (IBC-end wall, exterior) ───────────────────────────

def water_hookups():
    """Remote water-fill + waste-drain hookups on the IBC-end wall (exterior).

    2" NPT bulkhead fittings centered in Yd on the X=C_LEN end wall: fill high,
    two waste drains low. IBCs fill/drain remotely through these.
    """
    parts = []
    wx = C_LEN          # IBC-end wall
    yd = EXT_FILL_YD    # 1181 — centered
    r = 30              # ~2" NPT stub
    hooks = [("Water Fill Hookup (2in NPT)", EXT_FILL_H, C_IBC_BLUE),
             ("Waste Drain Hookup (2in NPT)", EXT_DRAIN_3_H, C_IBC_BROWN),
             ("Waste Drain Hookup (2in NPT)", EXT_DRAIN_H, C_IBC_WASTE)]
    for nm, hz, col in hooks:
        parts.append(ruby_cylinder(nm, wx, yd, hz, r, 120, color=col, axis="x"))

    return '\n'.join(parts)


# ── Ventilation fans (cargo-door end wall) ───────────────────────────────────

def fans():
    """Cross-ventilation fans + light-safe baffle ducts on OPPOSITE end walls,
    diagonal low-in / high-out:
      Fan A (exhaust) — sealed/IBC end wall (X=C_LEN), in the plumbing corridor
        directly BELOW the X1 fill port (Yd=1181, Z=2000) — the only full-height
        clear channel past the 1000L direct-stack.
      Fan B (intake)  — cargo-door panel (X=0, left), low (Z=600).

    Each fan sits at the INTERIOR mouth of a box-section baffle duct bolted to
    the wall interior: DUCT_DEPTH (300mm, along the fan axis) x DUCT_W (200mm,
    Yd) x DUCT_HEIGHT (200mm, Z), translucent galvanized steel. Inside, two
    150x150mm flat baffle plates are offset top/bottom at 1/3 and 2/3 depth to
    break the line of sight (light-safe S-path) while passing full airflow.
    """
    # Fan A: far end wall (X=C_LEN, exterior on +X); duct projects -X into container.
    # Fan B: cargo-door panel (X=0, exterior on -X); duct projects +X into container.
    return '\n'.join(
        fan_duct("Fan A (exhaust)", C_LEN, +1, FAN_A_YD, FAN_A_H) +
        fan_duct("Fan B (intake)", 0, -1, FAN_B_YD, FAN_B_H))


def fan_duct(tag, wall_x, ext, yc, zc):
    """One axial panel fan + light-safe baffle duct opening into the container.

    `ext` = +1 if the exterior is on +X, -1 on -X. The duct projects from the
    wall interior face into the container; the fan sits at the interior mouth.
    Returns a list of ruby strings. Shared single source of truth for the
    Overview fans() and the focused Light-Trap model (Fan B on the hinge panel).
    """
    r, bd = FAN_DIAM / 2, FAN_BODY_D          # Ø150, 50mm fan body
    dd, dh = DUCT_DEPTH, DUCT_HEIGHT          # 300 deep (axis), 200 tall (Z)
    dw = DUCT_HEIGHT                          # 200 wide (Yd) — square section
    bf, bft = 125, 8                          # baffle plates: FULL height (Z, welded top +
                                              # bottom) × 125 wide (Yd) — leaves a 75mm airflow
                                              # gap on one SIDE; the two plates take opposite
                                              # sides so air winds left↔right (horizontal S-path)
                                              # while the overlap blocks the line of sight
    flo, flt = 30, 5                          # flange overhang past the duct, + plate thickness
    gld, glh = 40, int(dh * 0.65)             # louvre grille depth + height

    if True:
        mouth_x = wall_x - ext * dd
        x0 = min(wall_x, mouth_x)
        out = [ruby_box(f"{tag} baffle duct", x0, yc - dw / 2, zc - dh / 2,
                        dd, dw, dh, color=C_DUCT, alpha=0.5)]
        # baffle plates — full height (welded top + bottom), offset left/right in Yd,
        # leaving a 75mm airflow gap on one side each (horizontal S-path)
        out.append(ruby_box(f"{tag} baffle plate 1", x0 + dd / 3 - bft / 2,
                            yc - dw / 2, zc - dh / 2, bft, bf, dh, color=C_FAN))
        out.append(ruby_box(f"{tag} baffle plate 2", x0 + 2 * dd / 3 - bft / 2,
                            yc + dw / 2 - bf, zc - dh / 2, bft, bf, dh, color=C_FAN))
        # ── axial panel fan at the interior mouth (matches 2D Sheet 2):
        #    square housing frame around the Ø150 bore + motor hub + 4-blade
        #    impeller, body set inside the duct ──
        fan_x = mouth_x if ext > 0 else mouth_x - bd   # interior face of fan body
        fr_y0, fr_y1 = yc - dw / 2, yc + dw / 2
        fr_z0, fr_z1 = zc - dh / 2, zc + dh / 2
        out.append(ruby_box(f"{tag} fan frame top", fan_x, fr_y0, zc + r,
                            bd, dw, fr_z1 - (zc + r), color=C_FAN))
        out.append(ruby_box(f"{tag} fan frame bottom", fan_x, fr_y0, fr_z0,
                            bd, dw, (zc - r) - fr_z0, color=C_FAN))
        out.append(ruby_box(f"{tag} fan frame left", fan_x, fr_y0, zc - r,
                            bd, (yc - r) - fr_y0, 2 * r, color=C_FAN))
        out.append(ruby_box(f"{tag} fan frame right", fan_x, yc + r, zc - r,
                            bd, fr_y1 - (yc + r), 2 * r, color=C_FAN))
        hub_r = r * 0.26
        out.append(ruby_cylinder(f"{tag} fan hub", fan_x, yc, zc, hub_r, bd,
                                 color=C_STEEL, axis="x"))
        bt, bw = 6, 30                                 # impeller blade thickness/width
        bx, bl = fan_x + bd * 0.45, r * 0.88 - hub_r   # blade plane + length
        out.append(ruby_box(f"{tag} fan blade up", bx, yc - bw / 2, zc + hub_r,
                            bt, bw, bl, color=C_ALUM))
        out.append(ruby_box(f"{tag} fan blade down", bx, yc - bw / 2,
                            zc - hub_r - bl, bt, bw, bl, color=C_ALUM))
        out.append(ruby_box(f"{tag} fan blade left", bx, yc - hub_r - bl,
                            zc - bw / 2, bt, bl, bw, color=C_ALUM))
        out.append(ruby_box(f"{tag} fan blade right", bx, yc + hub_r,
                            zc - bw / 2, bt, bl, bw, color=C_ALUM))
        # ── wall mounting flange: 5mm plate on the interior wall face, overhanging
        #    the duct opening, with 4 M10 bolts into the wall ──
        out.append(ruby_box(f"{tag} wall flange",
                            wall_x - (flt if ext > 0 else 0), yc - dw / 2 - flo,
                            zc - dh / 2 - flo, flt, dw + 2 * flo, dh + 2 * flo,
                            color=C_STEEL))
        for fy in (yc - dw / 2 - flo / 2, yc + dw / 2 + flo / 2):
            for fz in (zc - dh / 2 - flo / 2, zc + dh / 2 + flo / 2):
                out.append(ruby_cylinder(f"{tag} flange bolt M10",
                            wall_x - (flt + 8) / 2, fy, fz, 5, flt + 8,
                            color="#3A3A42", axis="x"))
        # ── weatherproof louvre grille on the exterior wall face (slatted) ──
        gx0 = wall_x if ext > 0 else wall_x - gld
        out.append(ruby_box(f"{tag} louvre grille", gx0, yc - dw / 2,
                            zc - glh / 2, gld, dw, glh, color=C_DUCT, alpha=0.55))
        for s in range(5):
            sz = zc - glh / 2 + (s + 0.5) * glh / 5
            out.append(ruby_box(f"{tag} louvre slat", gx0 + 2, yc - dw / 2 + 4,
                                sz - 1.5, gld - 4, dw - 8, 3, color=C_STEEL))
        return out


# ── Spray-bar plumbing (Blue supply + BV-02 + TAP-01) ────────────────────────

def spray_bar_plumbing():
    """Blue ½" supply trunk along the pinhole wall (Z=30) feeding the spray bar,
    with the BV-02 isolation valve riser and the TAP-01 chemistry tap branch.
    """
    parts = []
    yd = 12                          # just off the pinhole wall
    fz = SPRAY_BAR_FEED_Z            # 30 — supply trunk height
    pr = PUMP_PIPE_OD / 2            # ½" HDPE

    # Blue supply trunk — horizontal along the pinhole wall. It enters at RAIL_X_R
    # (riser from the filters), feeds BV-02 (spray-bar isolation, at the pinhole
    # centerline), and now CONTINUES LEFT to TAP-01 (the chem tap, relocated to
    # X=TAP_X in the widened walkway, rev13).
    x_l, x_r = TAP_X, RAIL_X_R
    parts.append(ruby_cylinder("Blue Supply Trunk (1/2in HDPE)",
                               x_l, yd, fz, pr, x_r - x_l, color=C_BLUE, axis="x"))

    # BV-02 isolation valve riser + body, at the pinhole centerline.
    parts.append(ruby_cylinder("BV-02 Riser",
                               BV02_X, yd, fz, pr, BV02_Z - fz, color=C_BLUE, axis="z"))
    parts.append(ruby_box("BV-02 (ball valve)",
                          BV02_X - 25, yd - 25, BV02_Z - 25, 50, 50, 50,
                          color=C_VALVE))

    # TAP-01 chemistry tap branch (¾") — relocated LEFT of the chem shelf. The riser
    # tops at the stowed-shelf height (SHELF_STOW_TOP_Z); the spout reaches out over
    # the shelf and dispenses at TAP_Z. BV-06 isolates the branch.
    tr = TAP_PIPE_OD / 2
    # One orthogonal run — riser up, out over the shelf, then down to the spout —
    # so BOTH 90° turns get a swept-torus elbow fitting (per skill_plumbing_drawing).
    # Was a riser cylinder + two butt-jointed spout pipes with no elbows at the corners.
    parts.append(ruby_pipe_run("TAP-01 Branch (3/4in)",
                               [(TAP_X, yd, fz),
                                (TAP_X, yd, SHELF_STOW_TOP_Z),
                                (TAP_X, yd + 100, SHELF_STOW_TOP_Z),
                                (TAP_X, yd + 100, TAP_Z)],
                               tr, color=C_BLUE))
    parts.append(ruby_box("BV-06 (chem tap isolation)",
                          TAP_X - 18, yd - 8, 1010, 36, 36, 40, color=C_VALVE))

    return '\n'.join(parts)


# ── Water / waste plumbing network ───────────────────────────────────────────

def ruby_pipe(name, p1, p2, r, color=None, alpha=None, n=16):
    """Straight cylindrical pipe between two arbitrary points p1, p2 (mm)."""
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    lines = [
        f'  # {name}',
        f'  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  ge = grp.entities',
        f'  vec = Geom::Vector3d.new({mm(x2 - x1)}, {mm(y2 - y1)}, {mm(z2 - z1)})',
        f'  circle = ge.add_circle([{mm(x1)},{mm(y1)},{mm(z1)}], vec, {mm(r)}, {n})',
        f'  pf = ge.add_face(circle)',
        f'  pf.reverse! if pf.normal.dot(vec) < 0',
        f'  pf.pushpull(vec.length)',
    ]
    if color:
        rr, gg, bb = hex_to_rgb(color)
        mat_nm = shared_mat_name(name, color, alpha)
        lines.append(f'  mat = model.materials["{mat_nm}"] || '
                     f'model.materials.add("{mat_nm}")')
        lines.append(f'  mat.color = Sketchup::Color.new({rr}, {gg}, {bb})')
        lines.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        lines.append(f'  grp.material = mat')
    lines.append('')
    return '\n'.join(lines)


def ruby_flex_duct(name, p1, p2, r, color=None, alpha=None, ribs=None):
    """Corrugated flex duct between p1 and p2 — a run of short pipe segments with
    alternating crest/valley radii so it reads as a ribbed flexible duct."""
    L = math.sqrt(sum((p2[i] - p1[i]) ** 2 for i in range(3)))
    if ribs is None:
        ribs = max(8, int(L / (r * 0.7)))            # rib pitch ≈ 0.7·r
    out = []
    for i in range(ribs):
        t0, t1 = i / ribs, (i + 1) / ribs
        a = tuple(p1[k] + (p2[k] - p1[k]) * t0 for k in range(3))
        b = tuple(p1[k] + (p2[k] - p1[k]) * t1 for k in range(3))
        rr = r if i % 2 == 0 else r * 0.8            # crest / valley
        out.append(ruby_pipe(name, a, b, rr, color=color, alpha=alpha, n=14))
    return '\n'.join(out)


def ruby_coil_cord(name, waypoints, r=5.0, color=None, alpha=None,
                   coil_r=None, pitch=None, pts_per_turn=8):
    """A 'soft' flexible cord — the visual opposite of the rigid `ruby_pipe_run`:
    a thin conductor that runs as a HELICAL COIL ('curly cord') along each straight
    leg, with short straight stubs at the ends / at each waypoint for termination.
    Color still encodes the circuit; the coiled geometry marks it as a flexible
    connector (the soft-connector analogue of the beaded pull-cord + corrugated
    flex-duct helpers). Tune `coil_r` (curl radius), `pitch` (axial advance per turn),
    and `r` (conductor radius — keep it thinner than the rigid conduit it replaces)."""
    coil_r = coil_r if coil_r is not None else 5.6 * r      # curl radius (~28 @ r=5, tightened 20%)
    pitch = pitch if pitch is not None else 18.0 * r        # axial advance/turn (~90 @ r=5)
    V = [tuple(float(c) for c in p) for p in waypoints]
    out = []
    for i in range(1, len(V)):
        a, b = V[i - 1], V[i]
        axis = _vsub(b, a)
        L = _vlen(axis)
        if L < 1e-3:
            continue
        d = _vscale(axis, 1.0 / L)
        stub = min(max(0.10 * L, 3.0 * r), 0.30 * L)        # straight termination ends
        coil_L = L - 2.0 * stub
        p0 = _vadd(a, _vscale(d, stub))                     # coil start (on axis)
        out.append(ruby_pipe(name, a, p0, r, color=color, alpha=alpha, n=10))
        if coil_L > pitch * 0.5:
            ref = (0.0, 0.0, 1.0) if abs(d[2]) < 0.9 else (1.0, 0.0, 0.0)
            u = _vunit(_vcross(d, ref))                      # perpendicular frame
            w = _vcross(d, u)
            turns = coil_L / pitch
            npts = max(8, int(round(turns * pts_per_turn)))
            prev = p0
            for k in range(1, npts + 1):
                t = k / npts
                ang = 2.0 * math.pi * turns * t
                axial = _vadd(p0, _vscale(d, coil_L * t))
                pt = _vadd(axial, _vadd(_vscale(u, coil_r * math.cos(ang)),
                                        _vscale(w, coil_r * math.sin(ang))))
                out.append(ruby_pipe(name, prev, pt, r, color=color, alpha=alpha, n=6))
                prev = pt
            p1 = _vadd(p0, _vscale(d, coil_L))              # coil end (back on axis)
            out.append(ruby_pipe(name, prev, p1, r, color=color, alpha=alpha, n=8))
            out.append(ruby_pipe(name, p1, b, r, color=color, alpha=alpha, n=10))
        else:
            out.append(ruby_pipe(name, p0, b, r, color=color, alpha=alpha, n=10))
    return '\n'.join(out)


# ── Orthogonal pipe routing with swept-torus elbow fittings ──────────────────
def _vsub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def _vadd(a, b): return (a[0]+b[0], a[1]+b[1], a[2]+b[2])
def _vscale(a, s): return (a[0]*s, a[1]*s, a[2]*s)
def _vdot(a, b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def _vcross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def _vlen(a): return math.sqrt(_vdot(a, a))
def _vunit(a):
    L = _vlen(a)
    return (a[0]/L, a[1]/L, a[2]/L) if L > 1e-9 else (0.0, 0.0, 0.0)


def ruby_elbow(name, A, O, Rc, normal, d_in, theta, r,
               color=None, alpha=None, n=16, seg=8):
    """Swept-torus elbow fitting: a pipe cross-section circle (radius r) at A is
    swept along an arc (centerline radius Rc, center O, plane normal `normal`,
    sweep `theta` rad) — a real 90deg/45deg elbow body, not a butt corner."""
    xa = _vunit(_vsub(A, O))
    out = [
        f'  # {name}',
        '  grp = ents.add_group',
        f'  grp.name = "{name}"',
        '  ge = grp.entities',
        (f'  arc = ge.add_arc([{mm(O[0])},{mm(O[1])},{mm(O[2])}], '
         f'[{xa[0]:.6f},{xa[1]:.6f},{xa[2]:.6f}], '
         f'[{normal[0]:.6f},{normal[1]:.6f},{normal[2]:.6f}], '
         f'{mm(Rc)}, 0.0, {theta:.6f}, {seg})'),
        (f'  circle = ge.add_circle([{mm(A[0])},{mm(A[1])},{mm(A[2])}], '
         f'[{d_in[0]:.6f},{d_in[1]:.6f},{d_in[2]:.6f}], {mm(r)}, {n})'),
        '  f = ge.add_face(circle)',
        '  f.followme(arc)',
    ]
    if color:
        rr, gg, bb = hex_to_rgb(color)
        mat_nm = shared_mat_name(name, color, alpha)
        out.append(f'  mat = model.materials["{mat_nm}"] || model.materials.add("{mat_nm}")')
        out.append(f'  mat.color = Sketchup::Color.new({rr}, {gg}, {bb})')
        out.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        out.append('  grp.material = mat')
    out.append('')
    return '\n'.join(out)


def ruby_pipe_run(name, waypoints, r, color=None, alpha=None,
                  elbow_r=None, n=16, seg=8):
    """Pipe run through axis-aligned `waypoints`: straight segments joined by a
    swept-torus elbow fitting at every interior vertex (short-radius elbow,
    centerline radius = 1x pipe diameter per skill_plumbing_drawing). Direction
    changes happen only at fittings — no diagonals, no butt corners."""
    R = elbow_r if elbow_r is not None else 2.0 * r
    V = [tuple(float(c) for c in p) for p in waypoints]
    out = []
    start = V[0]
    for i in range(1, len(V)):
        if i == len(V) - 1:
            if _vlen(_vsub(V[i], start)) > 0.5:
                out.append(ruby_pipe(name, start, V[i], r, color, alpha, n))
            break
        d_in = _vunit(_vsub(V[i], V[i-1]))
        d_out = _vunit(_vsub(V[i+1], V[i]))
        theta = math.acos(max(-1.0, min(1.0, _vdot(d_in, d_out))))
        if theta < 1e-3:                 # collinear — keep running straight
            continue
        T = R * math.tan(theta / 2.0)
        T = min(T, _vlen(_vsub(V[i], start)) * 0.49,
                _vlen(_vsub(V[i+1], V[i])) * 0.49)
        Rc = T / math.tan(theta / 2.0)
        A = _vadd(V[i], _vscale(d_in, -T))
        B = _vadd(V[i], _vscale(d_out, T))
        n_in = _vunit(_vsub(d_out, _vscale(d_in, _vdot(d_out, d_in))))
        O = _vadd(A, _vscale(n_in, Rc))
        normal = _vunit(_vcross(d_in, d_out))
        if _vlen(_vsub(A, start)) > 0.5:
            out.append(ruby_pipe(name, start, A, r, color, alpha, n))
        out.append(ruby_elbow(name + " elbow", A, O, Rc, normal, d_in, theta,
                              r, color, alpha, n, seg))
        start = B
    return '\n'.join(out)


def ruby_flex_run(name, waypoints, r, color=None, alpha=None,
                  elbow_r=None, n=16, seg=8):
    """Like ruby_pipe_run but the straight legs are corrugated flex duct
    (ruby_flex_duct); bends use the same swept-torus elbow fitting so the run
    stays orthogonal (per skill_plumbing_drawing) — right-angle connections."""
    R = elbow_r if elbow_r is not None else 2.0 * r
    V = [tuple(float(c) for c in p) for p in waypoints]
    out = []
    start = V[0]
    for i in range(1, len(V)):
        if i == len(V) - 1:
            if _vlen(_vsub(V[i], start)) > 0.5:
                out.append(ruby_flex_duct(name, start, V[i], r, color, alpha))
            break
        d_in = _vunit(_vsub(V[i], V[i-1]))
        d_out = _vunit(_vsub(V[i+1], V[i]))
        theta = math.acos(max(-1.0, min(1.0, _vdot(d_in, d_out))))
        if theta < 1e-3:
            continue
        T = R * math.tan(theta / 2.0)
        T = min(T, _vlen(_vsub(V[i], start)) * 0.49,
                _vlen(_vsub(V[i+1], V[i])) * 0.49)
        Rc = T / math.tan(theta / 2.0)
        A = _vadd(V[i], _vscale(d_in, -T))
        B = _vadd(V[i], _vscale(d_out, T))
        n_in = _vunit(_vsub(d_out, _vscale(d_in, _vdot(d_out, d_in))))
        O = _vadd(A, _vscale(n_in, Rc))
        normal = _vunit(_vcross(d_in, d_out))
        if _vlen(_vsub(A, start)) > 0.5:
            out.append(ruby_flex_duct(name, start, A, r, color, alpha))
        out.append(ruby_elbow(name + " elbow", A, O, Rc, normal, d_in, theta,
                              r, color, alpha, n, seg))
        start = B
    return '\n'.join(out)


def ruby_tee(name, node, run_dir, branch_dir, r, color=None, alpha=None, n=16):
    """Tee fitting body at a branch point: a fat run-through stub (along
    run_dir) plus a fat branch stub (along branch_dir), OD slightly larger than
    the pipe — a real tee, not a butt junction. The three pipe runs plug into
    its ports."""
    rt = r * 1.35
    L = r * 1.9
    ru = _vunit(run_dir)
    bu = _vunit(branch_dir)
    a = _vadd(node, _vscale(ru, -L))
    b = _vadd(node, _vscale(ru, L))
    c = _vadd(node, _vscale(bu, L))
    return '\n'.join([ruby_pipe(name, a, b, rt, color, alpha, n),
                      ruby_pipe(name, node, c, rt, color, alpha, n)])


def water_plumbing():
    """Water/waste plumbing routed orthogonally with swept-torus elbow fittings
    at every bend (per skill_plumbing_drawing), kept clear of the IBC footprint
    (X 4674-5893, Y 30-1046 & 1316-2332, Z 0-2336): ALL runs stay in the clear
    corridor (Y 1046-1316) — the direct-stack totes leave only 52mm headroom, so
    EVERY tote-top connection (fill, recycle returns, reject) is SIDE-ENTRY near
    the top; the drains/suctions run in separate corridor lanes; P-01 → spray bar
    drops to the floor and leaves the IBC zone (X<4674) before traversing.
    KEEPS the recycle loop (matches generate_panel_layout.py): tray sump → P-04 →
    DV-02 → IBC-3 (Brown); IBC-3 → P-02 → filters → DV-01 → IBC-2 (Blue recycle);
    off-spec → IBC-4 (Waste). Blue=fresh/process, brown=recycled, gray=waste."""
    pr = 12
    nearX = IBC_COL_X + IBC_W / 2           # 5283 — IBC column center X
    nY = BLUE_IBC_Y + IBC_D / 2            # 538  — near col center (Blue #1 fill)
    fY = IBC_FAR_Y + IBC_D / 2            # 1824 — far col center (Blue #2 fill)
    topZ = 2 * IBC_H_1000                  # 2336 — IBC stack top (direct-stack, 52mm headroom)
    pumpZ = PUMP_H_LO                      # 1370 — pump inlet bottom
    pumpX = EQPANEL_X - 50                  # pump inlet X — tracks panel
    cc = 1181                              # corridor centerline Y
    floor = 60                             # floor-run height
    upVZ = IBC_H_1000 + IBC_VALVE_Z        # 1353 — upper-tier valve Z (Blue totes)
    loVZ = IBC_VALVE_Z                     # 185  — lower-tier valve Z (Brown/Waste)
    # Pump inlets (per equipment_panel): left col Y=1109 → P-01/P-04, right col
    # Y=1253 → P-02/P-03; rows Z=1370 (bottom) / 1628 (upper). Two riser X-lanes
    # per column (rxA/rxB) so the four suction risers never overlap.
    manX = EQPANEL_X + 100                 # Blue manifold header X (corridor) — tracks panel
    pyL, pyR = 1109, 1253                  # left / right pump-column Y
    pZ1, pZ2 = PUMP_H_LO, PUMP_H_LO + 258  # bottom / upper pump-row Z
    rxA, rxB = EQPANEL_X - 60, EQPANEL_X - 20  # two riser X-lanes per column (track panel)
    parts = []
    def pipe(nm, wp, col):
        parts.append(ruby_pipe_run(nm, wp, pr, color=col))

    # Exterior Blue FILL (gravity) — into the SIDES of the two Blue totes NEAR THE
    # TOP, NOT the caps (only 52mm headroom — no top-cap access). The X1 trunk runs
    # in the clear corridor to a tee placed NEAR X1, then a branch enters each Blue
    # tote's corridor-facing side near the top; both are gravity-linked (fed from
    # the same tee at the same height, so they equalize at ~800L each).
    fillTeeX = C_LEN - 240                 # 5653 — tee near X1 (just in from the sealed wall)
    entryZ   = topZ - 180                  # 2156 — side entry near the top of the Blue totes
    pipe("X1 Blue Fill Trunk",
         [(C_LEN, EXT_FILL_YD, EXT_FILL_H), (fillTeeX, cc, EXT_FILL_H)], C_BLUE)
    parts.append(ruby_tee("Blue Fill Tee", (fillTeeX, cc, EXT_FILL_H),
                          (0, 1, 0), (0, 0, -1), pr, color=C_BLUE))
    # Branch into Blue #1 (near col, corridor face EQPANEL_YD) near the top — the
    # pipe penetrates 150mm into the tote past the flange (note: 150mm + flange).
    pipe("Fill → Blue #1 side",
         [(fillTeeX, cc, EXT_FILL_H), (fillTeeX, cc, entryZ),
          (fillTeeX, EQPANEL_YD, entryZ), (fillTeeX, EQPANEL_YD - 150, entryZ)], C_BLUE)
    # Branch into Blue #2 (far col, corridor face EQPANEL_YD_FAR) near the top.
    pipe("Fill → Blue #2 side",
         [(fillTeeX, cc, entryZ), (fillTeeX, EQPANEL_YD_FAR, entryZ),
          (fillTeeX, EQPANEL_YD_FAR + 150, entryZ)], C_BLUE)
    # Round fill flange on each Blue tote's corridor face where the branch enters.
    flange_r, flange_h = 36, 16
    parts.append(ruby_cylinder("Fill Flange Blue #1", fillTeeX, EQPANEL_YD - flange_h / 2,
                               entryZ, flange_r, flange_h, color=C_STEEL, axis="y"))
    parts.append(ruby_cylinder("Fill Flange Blue #2", fillTeeX, EQPANEL_YD_FAR - flange_h / 2,
                               entryZ, flange_r, flange_h, color=C_STEEL, axis="y"))

    # Exterior DRAIN PORTS X3/X4 are fed from the DRAIN PUMPS (not straight off the
    # totes): P-05 (Brown drain) → X3, P-03 (Waste evac) → X4.  Each run leaves the
    # pump discharge, drops a riser behind the panel frame, and runs out to the
    # end-wall port along the clear corridor.  Two riser X-lanes (drnA/drnB) keep
    # the Brown and Waste runs from overlapping.
    drnA = 5400                            # Brown riser X (behind panel frame 5258-5308)
    drnB = 5340                            # Waste riser X (offset lane)
    pZ3  = PUMP_H_LO + 626                  # 1946 — P-05 (Brown drain) pump row
    pipe("P-05 → X3 (Brown drain-out)",
         [(rxB, pyR, pZ3), (drnA, pyR, pZ3), (drnA, pyR, EXT_DRAIN_3_H),
          (drnA, EXT_DRAIN_YD, EXT_DRAIN_3_H), (C_LEN, EXT_DRAIN_YD, EXT_DRAIN_3_H)],
         C_IBC_BROWN)
    pipe("P-03 → X4 (Waste drain-out)",
         [(rxB, pyR, pZ2), (drnB, pyR, pZ2), (drnB, pyR, EXT_DRAIN_H),
          (drnB, EXT_DRAIN_YD, EXT_DRAIN_H), (C_LEN, EXT_DRAIN_YD, EXT_DRAIN_H)],
         C_IBC_WASTE)

    # IBC valves → their own pumps. Each suction ENTERS its tote perpendicular at
    # the panel X (penetrating 150mm past a flange — note 1), then turns once and
    # rises to the pump — no long run along the tote side (reduced pipe lines).
    def tote_flange(nm, x, y, z, col):
        parts.append(ruby_cylinder(nm, x, y - 9, z, 36, 18, color=C_STEEL, axis="y"))

    # Blue: tap BOTH top-tier Blue totes perpendicular at the panel, tee to P-01.
    parts.append(ruby_tee("Blue Manifold Tee", (rxA, cc, upVZ), (0, 1, 0), (-1, 0, 0), pr, color=C_BLUE))
    pipe("Blue #1 → manifold", [(rxA, EQPANEL_YD - 150, upVZ), (rxA, cc, upVZ)], C_BLUE)
    pipe("Blue #2 → manifold", [(rxA, EQPANEL_YD_FAR + 150, upVZ), (rxA, cc, upVZ)], C_BLUE)
    pipe("Manifold → P-01", [(rxA, cc, upVZ), (rxA, pyL, upVZ), (rxA, pyL, pZ1)], C_BLUE)
    tote_flange("Blue #1 Suction Flange", rxA, EQPANEL_YD, upVZ, C_BLUE)
    tote_flange("Blue #2 Suction Flange", rxA, EQPANEL_YD_FAR, upVZ, C_BLUE)

    # Brown: enter IBC-3 (near corridor face) directly at the panel, 90° up to P-02.
    pipe("Brown → P-02",
         [(rxA, EQPANEL_YD - 150, loVZ), (rxA, EQPANEL_YD, loVZ),
          (rxA, pyR, loVZ), (rxA, pyR, pZ1)], C_IBC_BROWN)
    tote_flange("Brown Suction Flange", rxA, EQPANEL_YD, loVZ, C_IBC_BROWN)

    # Waste: enter IBC-4 (far corridor face) directly at the panel, 90° up to P-03.
    pipe("Waste → P-03",
         [(rxB, EQPANEL_YD_FAR + 150, loVZ), (rxB, EQPANEL_YD_FAR, loVZ),
          (rxB, pyR, loVZ), (rxB, pyR, pZ2)], C_IBC_WASTE)
    tote_flange("Waste Suction Flange", rxB, EQPANEL_YD_FAR, loVZ, C_IBC_WASTE)

    # Processing-tray sump (per water-system Detail A): pickup riser UP through
    # the cantilevered near-walkway grate to the valve above deck, back DOWN
    # through the grate, then routed UNDERNEATH at floor level (Z=30 — below the
    # cantilever beams (Z80-115) AND the bottom film rail (Z150)) through the
    # tray–IBC gap into the corridor and up to the pump.
    # rev12: the return riser drops in the GRATE GAP between the two walkway long
    # beams (X<4589) — the old X+70 drop (X4620) fell on the right long beam
    # (X4589-4629). And it TWISTS in Yd at valve height so the return leg lands at a
    # different depth than the pickup riser (they were both at Yd80 → stacked into one
    # pipe). The return drops in the clear strip in FRONT of the tray (Yd past the
    # Yd0-40 end beam, before the tray near edge Yd80), then the Z30 floor run heads
    # to the gap — clearing the beam + bottom film rail.
    gapX = (PROC_TRAY_X_R + IBC_COL_X) / 2     # 4651.5 — centered in the 45mm gap
    valveZ = WALKWAY_H + 65                     # 195 — valve body above the deck
    dropX = PROC_TRAY_DRAIN_X - 70              # 4480 — return riser in the grate gap
    dropY = RWK_BEARER_W + 10                   # 50 — offset depth: clear of the Yd0-40 end beam
    sumpY = PROC_TRAY_DRAIN_YD + 75             # 155 — pickup moved 75mm off the pinhole wall (clear of the near rim wall)
    pipe("Tray Sump → P-04",
         [(PROC_TRAY_DRAIN_X, sumpY, PROC_TRAY_SUMP_Z),   # sump pickup
          (PROC_TRAY_DRAIN_X, sumpY, valveZ),             # up to the valve
          (dropX, sumpY, valveZ),                         # over in X (valve body)
          (dropX, dropY, valveZ),                         # TWIST: jog in Yd
          (dropX, dropY, 30),                             # return riser (offset)
          (gapX, dropY, 30),                              # floor run out to the gap
          (gapX, cc, 30), (IBC_COL_X, cc, 30),            # along to the IBC front (clear of cantilevers X<4674)
          (IBC_COL_X, cc, 90),                            # rise to clear the frame FLOOR BEAM (X4734-4784, Z0-50)
          (rxB, cc, 90), (rxB, pyL, 90), (rxB, pyL, pZ2)],  # OVER the beam, then up to P-04
         C_IBC_WASTE)

    # ── Recycle loop (matches generate_panel_layout.py — the canonical routing) ──
    # KEEP the recycle loop: the tray sump feeds the Brown buffer (IBC-3), Brown is
    # filtered and recycled back to Blue (IBC-2), and Blue feeds the spray bar.  All
    # tote-top connections are SIDE-ENTRY near the top (no top-cap access, 52mm
    # headroom).  3-way diverters DV-02 (after P-04) and DV-01 (after the filters)
    # send off-spec water to the Waste tote (IBC-4) instead.
    ibc3_in_z = IBC_H_1000 - 80                   # 1088 — IBC-3 (Brown) side-entry near top
    ibc4_in_z = IBC_H_1000 - 80                   # 1088 — IBC-4 (Waste) side-entry near top
    ibc2_in_z = 2 * IBC_H_1000 - 180              # 2156 — IBC-2 (Blue) side-entry near top
    fcx = EQPANEL_X - BB_OD / 2                    # 4809 — filter column X (per equipment_panel)
    f_out_z = F3_Z + BB_H / 2                      # filter-stack outlet (top of F3)

    # (1) Blue supply → P-01 → spray bar (the wash/rinse feed).  The drop stops at
    # Z250 (clear ABOVE the Brown→P-02 suction at Z185), jogs in X OVER the frame
    # floor beam, then drops to the floor on the gap side (X<4734) — so it neither
    # crosses the brown suction nor passes through the frame.
    pipe("P-01 → Spray Bar",
         [(rxA, pyL, pZ1), (rxA, pyL, 250), (IBC_COL_X, pyL, 250),
          (IBC_COL_X, pyL, floor), (RAIL_X_R, pyL, floor),
          (RAIL_X_R, 12, floor), (RAIL_X_R, 12, SPRAY_BAR_FEED_Z)], C_BLUE)

    # (2) Tray-sump recycle: P-04 → 3W-DV-02 → IBC-3 (Brown) side-entry near top.
    # The discharge leaves P-04 on its OWN Yd-lane (dvY) so it doesn't run back down
    # collinear with the sump riser that feeds the pump.
    dvY = pyL - 50
    parts.append(ruby_tee("3W-DV-02 Diverter", (rxB, dvY, ibc3_in_z), (0, -1, 0), (0, 0, 1), pr, color=C_VALVE))
    pipe("P-04 → DV-02", [(rxB, pyL, pZ2), (rxB, dvY, pZ2), (rxB, dvY, ibc3_in_z)], C_IBC_BROWN)
    pipe("DV-02 → IBC-3 side-entry",
         [(rxB, dvY, ibc3_in_z), (rxB, EQPANEL_YD, ibc3_in_z),
          (rxB, EQPANEL_YD - 150, ibc3_in_z)], C_IBC_BROWN)
    tote_flange("IBC-3 Recycle Flange", rxB, EQPANEL_YD, ibc3_in_z, C_IBC_BROWN)

    # (3) Brown recycle: P-02 → F1/F2/F3 → 3W-DV-01 → IBC-2 (Blue) side-entry.
    pipe("P-02 → Filters", [(rxA, pyR, pZ1), (fcx, cc, pZ1), (fcx, cc, F1_Z)], C_IBC_BROWN)
    parts.append(ruby_tee("3W-DV-01 Diverter", (fcx, cc, ibc2_in_z), (0, 1, 0), (0, 0, -1), pr, color=C_VALVE))
    pipe("Filters → DV-01 → IBC-2 side-entry",
         [(fcx, cc, f_out_z), (fcx, cc, ibc2_in_z),
          (fcx, EQPANEL_YD_FAR, ibc2_in_z), (fcx, EQPANEL_YD_FAR + 150, ibc2_in_z)], C_FILTER)
    tote_flange("IBC-2 Recycle Flange", fcx, EQPANEL_YD_FAR, ibc2_in_z, C_FILTER)

    # (4) DV-01 reject (pH out of range) → IBC-4 (Waste) side-entry near top.  It
    # jogs onto its OWN X-lane (rejX) at the DV-01 junction, drops in the CORRIDOR
    # to below the Blue tote, then enters IBC-4 from the side — NOT up-and-through
    # the Blue tote (IBC-2) that sits directly above IBC-4.
    rejX = fcx + 35
    pipe("DV-01 → IBC-4 reject",
         [(fcx, cc, ibc2_in_z), (rejX, cc, ibc2_in_z), (rejX, cc, ibc4_in_z),
          (rejX, EQPANEL_YD_FAR, ibc4_in_z), (rejX, EQPANEL_YD_FAR + 150, ibc4_in_z)],
         C_IBC_WASTE)
    tote_flange("IBC-4 Reject Flange", rejX, EQPANEL_YD_FAR, ibc4_in_z, C_IBC_WASTE)

    return '\n'.join(parts)


# ── Assemble full Ruby script ────────────────────────────────────────────────

def generate_ruby():
    """Build the complete Ruby script for the Overview model."""
    comps = [
        component("Container Shell", "Shell", container_shell()),
        component("Walkways", "Walkways", walkways()),
        component("Processing Tray", "Processing Tray", processing_tray()),
        component("Pinhole Assembly", "Pinhole", pinhole_assembly()),
        component("Optical Cone", "Optical Cone", optical_cone()),
        component("Film Plane Mechanism", "Film Plane", film_plane_mechanism()),
        component("FP Combined Corner Plates", "Combined Plate", fp_combined_corner_plates()),
        component("Panel & Pivot Axle", "Pivot Axle", panel_pivot()),
        component("Spray Bar", "Spray Bar", spray_bar()),
        component("Equipment Panel", "Equipment Panel", equipment_panel()),
        component("IBC Stack", "IBC Stack", ibc_stack()),
        component("IBC Rack", "IBC Rack", ibc_rack()),
        component("Light-Trap Drum", "Light Trap", light_trap_drum()),
        component("Light-Trap Bay", "Light Trap", light_trap_bay()),
        component("Electrical", "Electrical", electrical()),
        component("Solar Array", "Solar Array", solar_array()),
        component("Chemistry Shelf", "Shelf", shelf()),
        component("Light-Trap Door Frame", "Light Seal", light_trap_frame()),
        component("Light Seal & Hinges", "Light Seal", light_seal()),
        component("Lighting & Wiring", "Lighting", lighting_wiring()),
        component("Evap Cooler & Duct", "Evap Cooler", evap_cooler()),
        component("Water/Waste Hookups", "Water Hookups", water_hookups()),
        component("Fans A & B", "Fans", fans()),
        component("Spray Bar Plumbing", "Spray Bar", spray_bar_plumbing()),
        component("Water Plumbing", "Water Plumbing", water_plumbing()),
    ]
    body = '\n'.join(comps)

    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)

    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    # Grouped scenes — related subsystems together (Shell shown as context).
    scene_groups = [
        ("Film Plane & Pinhole", ["Pinhole", "Optical Cone", "Film Plane", "Combined Plate"]),
        ("Water Systems", ["Processing Tray", "Spray Bar", "Equipment Panel",
                           "IBC Stack", "IBC Rack", "Shelf", "Water Hookups",
                           "Water Plumbing"]),
        ("Electrical Systems", ["Electrical", "Lighting", "Solar Array"]),
        ("Hinge Panel & Drum", ["Light Trap", "Light Seal", "Pivot Axle"]),
        ("Ventilation", ["Evap Cooler", "Fans"]),
        ("Walkways", ["Walkways", "Combined Plate"]),
    ]
    scene_groups_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags))
        for n, tags in scene_groups) + ']'

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Overview", true)
entities = model.active_entities

# Display in millimeters (LengthUnit 2 = mm, LengthFormat 0 = decimal).
# SketchUp stores geometry in inches internally; this only sets the UI readout.
opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# ── Idempotent rebuild: erase ALL prior instances (incl. any 'Sree' scale figure —
# the person is no longer kept), then purge unused definitions so names don't collide.
to_erase = entities.to_a.select {{ |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

# ── Tags (layers) ──
{tags_ruby}

# Dashed line style for the optical cone wireframe (guidance, not a solid).
begin
  ds = model.line_styles["Dash"] || model.line_styles["Dot"]
  model.layers["Optical Cone"].line_style = ds if ds
rescue StandardError
end

# ── Subsystems (each a component on its tag) ──
{body}

# rev11: the brace cage is retired (rail ends now sit on wall-seat saddles), so the old
# "FP Brace Vert L (film)" duplicate-strike for the Ø89 swing pivot post is no longer needed.

# ── Major-component callouts (Labels tag — shown only in the "Labeled" scene) ──
{overview_labels()}

{license_note()}

model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier generator versions ──
keep_tags = {keep_tags_ruby}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

# ── Scenes ──
# One consistent iso camera, shared by every scene — switching scenes only
# toggles visibility, never the viewpoint.
model.layers.each {{ |l| l.visible = true }}
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(0.72, -0.7, 0.5); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

# Overview — everything visible, Labels OFF.
model.layers["Labels"].visible = false if model.layers["Labels"]
ovp = model.pages.add("Overview"); ovp.use_camera = true

# Labeled — same view + callouts on the major system components.
model.layers["Labels"].visible = true if model.layers["Labels"]
olp = model.pages.add("Labeled"); olp.use_camera = true
model.layers["Labels"].visible = false if model.layers["Labels"]

# Grouped scenes — translucent Shell (context) + the group's subsystems.
{scene_groups_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == default_layer || l.name == "Shell" || tags.include?(l.name)) }}
  page = model.pages.add(name)
  page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}

model.commit_operation
{{ success: true, model: "Overview",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Ruby code for the TBS-001 Overview SketchUp model")
    parser.add_argument("--save", action="store_true",
                        help="Write Ruby to src/models/overview.rb")
    parser.add_argument("--send", action="store_true",
                        help="Send the Ruby straight to the running SketchUp")
    parser.add_argument("--sketchfab", nargs="?", const="overview", default=None,
                        metavar="MODEL",
                        help="MANUAL/opt-in: after --send, save the .skp and push the "
                             "live model to Sketchfab as a NEW model (consumes a "
                             "Sketchfab upload + resets viewer settings), updating the "
                             "embed + registry. Logical model name, default: overview")
    args = parser.parse_args()

    ruby = generate_ruby()

    if args.save:
        out = os.path.join(os.path.dirname(__file__), "overview.rb")
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

    if args.sketchfab:
        if not args.send:
            print("  --sketchfab requires --send", file=sys.stderr)
            sys.exit(1)
        import subprocess
        from sketchup_client import send_ruby
        skp = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           "..", "..", "models", f"{args.sketchfab}.skp"))
        print(f"  saving {skp} ...")
        send_ruby('m=Sketchup.active_model; "saved=#{m.save(' + repr(skp) + ')}"')
        subprocess.run([sys.executable,
                        os.path.join(os.path.dirname(__file__), "push_sketchfab.py"),
                        args.sketchfab], check=True)

    if not args.save and not args.send:
        print(ruby)
