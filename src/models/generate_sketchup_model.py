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
  - Re-runs are **idempotent**: prior generated instances are erased and their
    definitions purged before rebuilding. The 'Sree' scale figure (and anything
    not generated here) is preserved.

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
    python3 src/models/generate_sketchup_model.py --save   # write tbs_model.rb
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
    C_WALL, C_PROC_ZONE,
    PH_X, PH_H, PH_D,
    FP_X_L, FP_X_R, FP_W, FP_H, FP_Y, FP_Y_MIN,
    RAIL_X_L, RAIL_X_R, RAIL_LEN, RAIL_OFF, RAIL_OFF_BOT, FP_ANGLE_LEG,
    BRACE_RHS, BRACE_Z_BOT, BRACE_Z_TOP,
    BAY_FRONT_X, BAY_BACK_X, BAY_WALL_T,
    PANEL_CENTER_T, PANEL_FLOOR_GAP, PANEL_SLIDE,
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
    IBC_COL_X, IBC_W, IBC_D, IBC_H_600, IBC_PALLET_H, IBC_BOTTLE_INSET,
    BLUE_IBC_Y, BROWN_IBC_Y, IBC_FAR_Y, WASTE_IBC_Y,
    IBC_FRAME_RHS,
    IBC_FOOT_PLATE, IBC_FOOT_PLATE_T, IBC_FOOT_BOLT_PCD,
    IBC_WBKT_PLATE_W, IBC_WBKT_PLATE_T, IBC_WBKT_SEAT_PROJ,
    IBC_WBKT_SEAT_T, IBC_WBKT_GUSSET_H,
    PANEL_FRAME_X,
    DRUM_CX, DRUM_CY, DRUM_R, DRUM_H_LT,
    LT_HOUSING_R, LT_HOUSING_T, LT_DRUM_OR, LT_DRUM_T, LT_OPENING_DEG,
    EP_X, EP_W, EP_H_LO, EP_H_HI,
    BA_X, BA_W, BA_H_LO, BA_H_HI, BA_D,
    PWR_PANEL_X, PWR_PANEL_W, PWR_PANEL_H, PWR_PANEL_Z,
    SHELF_X_L, SHELF_X_R, SHELF_W, SHELF_H, SHELF_T, SHELF_DEPTH,
    SHELF_YD_NEAR, SHELF_YD_FAR, SHELF_HANGER_D,
    EVAP_W, EVAP_D, EVAP_H, EVAP_DUCT_X, EVAP_DUCT_Z, EVAP_DUCT_D,
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
C_PLY = "#9C7B4D"       # marine ply (equipment panel)
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
        "Pinhole", "Optical Cone", "Film Plane",
        "Pivot Axle", "Spray Bar", "Equipment Panel",
        "IBC Stack", "IBC Rack", "Light Trap", "Electrical", "Shelf",
        "Light Seal", "Lighting", "Evap Cooler", "Water Hookups", "Fans",
        "Water Plumbing", "Labels"]


# Major system components to call out in the "Labeled" scene.
# (component instance name, label text, leader Δx mm, leader Δz mm) — the leader is
# anchored at the component's bounds top-centre and fanned out so labels don't pile up.
# (component name, text, leader Δx, Δy, Δz mm). Δy pulls the label OUT of a wall
# toward the viewer (the camera looks from the −Y / pinhole-wall side).
OVERVIEW_LABELS = [
    ("Pinhole Assembly",      "PINHOLE  Ø2.17mm",                 -200, -1600,  900),
    ("Film Plane Mechanism",  "FILM PLANE\n4-corner tilt/swing",   400,     0, 1250),
    ("Processing Tray",       "PROCESSING TRAY",                  -250,     0,  650),
    ("Spray Bar",             "SPRAY BAR",                         450, -2700, 1300),
    ("Equipment Panel",       "EQUIPMENT PANEL\npump / filter",    500,     0,  820),
    ("IBC Stack",             "IBC WATER STORAGE\n4x tote",        600,     0, 1300),
    ("Light-Trap Drum",       "LIGHT-TRAP DRUM\n(entry)",         -650,     0, 1050),
    ("Electrical",            "ELECTRICAL PANEL",                  500,     0,  560),
    ("Chemistry Shelf",       "CHEMISTRY SHELF",                  -350,     0, 1550),
    ("Evap Cooler & Duct",    "EVAP COOLER",                       300,     0, 1700),
]

# Labels anchored at an explicit point (mm) — for items NOT represented by a single
# component instance: the two fans live in one "Fans A & B" component that spans both
# ends of the container (so its bounds-centre lands in the empty middle), and the
# battery bank lives inside the "Electrical" component.
# (x, y, z, text, leader Δx, Δy, Δz mm)
OVERVIEW_POINT_LABELS = [
    (5618, 1996, 2250, "FAN A\n(exhaust, IBC end)",  400,    0,  450),
    (275,   365,  680, "FAN B\n(intake, door end)", -350,    0, 1250),
    (2060,   60,  600, "BATTERY BANK\n(LiFePO4)",    -300, -600,  900),
    # Walkways span paired/perimeter parts, so their bounds-centre would land in the
    # empty middle — anchor on the actual NEAR member instead.
    (2400,  150,   65, "WALKWAYS",                   -200, -850,  750),  # near walkway strip
    ( 175, 2287, 1700, "PIVOT POST Ø89\n(panel swing axis)", 500, -200, 600),  # the swing pivot
]


def overview_labels():
    """Ruby that adds an in-model text callout (with leader) for each major system
    component, on the 'Labels' tag. Component labels anchor at the instance's bounds
    top-centre (tracking the geometry); point labels anchor at an explicit coordinate.
    The leader (Δx,Δy,Δz) fans the text out above/clear of the model."""
    rows = []
    for name, text, dx, dy, dz in OVERVIEW_LABELS:
        rows.append(
            f'inst = entities.grep(Sketchup::ComponentInstance).find {{ |i| i.name == "{name}" }}\n'
            f'if inst\n'
            f'  bb = inst.bounds\n'
            f'  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)\n'
            f'  txt = entities.add_text("{text}", anc, Geom::Vector3d.new({mm(dx)}, {mm(dy)}, {mm(dz)}))\n'
            f'  txt.layer = model.layers["Labels"] rescue nil\n'
            f'end')
    for x, y, z, text, dx, dy, dz in OVERVIEW_POINT_LABELS:
        rows.append(
            f'anc = Geom::Point3d.new({mm(x)}, {mm(y)}, {mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({mm(dx)}, {mm(dy)}, {mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    return '\n'.join(rows)


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

def walkways():
    """Perimeter walkway sections — LOWERED deck, in place for operation.

    The deck height comes from WALKWAY_H (lowered to 65mm: a 15mm grate at the
    tray-rim level), so the grating sits below the film-frame bottom (Z=100) and
    the film plane travels above the in-place walkway. The LEFT walkway (cargo-
    door side) is a removable lift-out (shown in a distinct color) — taken out
    for transport before the panel + drum swing inboard.
    """
    grate_z = WALKWAY_H - WALKWAY_GRATE_T   # 115mm — grate bottom (raised +50)
    t = WALKWAY_GRATE_T                      # 15mm — thin grate

    near_x_l = WALKWAY_LEFT_X + WALKWAY_W
    near_x_r = WALKWAY_RIGHT_X
    # The near/far grates run along the side walls from the left-walkway inner edge
    # (X=near_x_l). The floor-leg cantilever redesign has no kerb beam to cut around.
    near_len = near_x_r - near_x_l

    parts = []

    if WALKWAY_NEAR_WIDE_X_L > near_x_l:
        seg_len = WALKWAY_NEAR_WIDE_X_L - near_x_l
        parts.append(ruby_box("Walkway Near (left section)",
                              near_x_l, 0, grate_z,
                              seg_len, WALKWAY_W, t, color=C_WALKWAY))

    wide_len = WALKWAY_NEAR_WIDE_X_R - WALKWAY_NEAR_WIDE_X_L
    parts.append(ruby_box("Walkway Near (widened)",
                          WALKWAY_NEAR_WIDE_X_L, 0, grate_z,
                          wide_len, WALKWAY_NEAR_WIDE_W, t, color=C_WALKWAY))

    if WALKWAY_NEAR_WIDE_X_R < near_x_r:
        seg_len = near_x_r - WALKWAY_NEAR_WIDE_X_R
        parts.append(ruby_box("Walkway Near (right section)",
                              WALKWAY_NEAR_WIDE_X_R, 0, grate_z,
                              seg_len, WALKWAY_W, t, color=C_WALKWAY))

    parts.append(ruby_box("Walkway Far",
                          near_x_l, WALKWAY_FAR_YD, grate_z,
                          near_len, WALKWAY_W, t, color=C_WALKWAY))

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
    # Cargo-door panel, operational position (X=0). Ply sandwich (bay/hinge-panel color).
    parts.append(ruby_box("Cargo Door Panel",
                          0, 0, PANEL_FLOOR_GAP,
                          PANEL_CENTER_T, C_WID, 2300 - PANEL_FLOOR_GAP,
                          color=C_PLY, alpha=0.6))
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

    # ACC-01 accumulator — Ø127 × 150 vertical cylinder, left column.
    parts.append(ruby_cylinder("ACC-01 Accumulator",
                               face_x - 63, col_l, z_top, 127 / 2, 150,
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
    # corridor (Yd 1046-1316) — no tote contact.  The top is LOWERED and capped
    # with a horizontal ply shelf that the Blue fill trunk rests on (supported
    # at the T) rather than the spine standing proud past the pipe.
    sp_t  = EQPANEL_T                              # 18mm ply
    sp_x0, sp_x1 = face_x, 5420                     # butts the panel rear → past the X3 riser
    sp_y  = col_r - 30                              # spine board Yd (near-face just off the risers)
    blue_z   = 2 * IBC_H_600 + 230                  # 2250 — Blue fill trunk centerline (overZ)
    cap_top  = blue_z - 12                          # 2238 — shelf top = fill-pipe underside (pr=12)
    spine_top = cap_top - sp_t                      # 2220 — lowered web top (was EQPANEL_Z_HI=2260)
    parts.append(ruby_box("Drain-riser spine (ply)", sp_x0, sp_y, EQPANEL_Z_LO,
                          sp_x1 - sp_x0, sp_t, spine_top - EQPANEL_Z_LO,
                          color=C_PLY))
    # Stiffening flange along the spine's rear edge → T cross-section.
    parts.append(ruby_box("Drain-riser spine flange (ply)", sp_x1 - sp_t,
                          col_r - 27, EQPANEL_Z_LO, sp_t, 54,
                          spine_top - EQPANEL_Z_LO, color=C_PLY))
    # Top shelf — horizontal ply cap sitting on the lowered web, cantilevering
    # toward the Blue trunk (Yd≈1181) so the fill pipe is supported at the T.
    cap_y0 = 1160                                   # reaches under the Blue trunk
    parts.append(ruby_box("Drain-riser spine top shelf (ply)", sp_x0, cap_y0,
                          spine_top, sp_x1 - sp_x0 + 40, (sp_y + sp_t) - cap_y0,
                          sp_t, color=C_PLY))
    # Saddle clamp holding the Blue fill trunk down onto the shelf.
    parts.append(ruby_box("Blue fill pipe clamp", 5420, 1181 - 16, cap_top,
                          36, 32, 20, color=C_STEEL))
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
    `alpha` sets the bottle translucency (lower = more transparent).
    """
    parts = []
    pal = IBC_PALLET_H
    inset = IBC_BOTTLE_INSET
    bottle_h = IBC_H_600 - pal - 20   # leave 20mm for the cage top

    totes = [
        ("IBC Brown (developer)", BROWN_IBC_Y, 0, C_IBC_BROWN),
        ("IBC Blue #1", BLUE_IBC_Y, IBC_H_600, C_IBC_BLUE),
        ("IBC Waste", WASTE_IBC_Y, 0, C_IBC_WASTE),
        ("IBC Blue #2", IBC_FAR_Y, IBC_H_600, C_IBC_BLUE),
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
    """Simplified 50×50 RHS portal rack supporting the upper IBC tier.

    Corridor uprights (Yd 1046/1316) at three X stations, longitudinal spine
    beams, and cantilever platform cross-beams under the top totes at Z≈1010.
    """
    parts = []
    s = IBC_FRAME_RHS                   # 50×50 RHS
    plat_z = IBC_H_600                  # 1010 — top tier rests here
    beam_z = plat_z - s                 # cross-beams top flush with 1010
    yd_near, yd_far = 1046, 1316        # plumbing-corridor edges
    x_stations = [IBC_COL_X + 60,
                  IBC_COL_X + IBC_W / 2 - s / 2,
                  IBC_COL_X + IBC_W - 60 - s]

    # Uprights at the two corridor edges, three X stations.
    for xs in x_stations:
        for yd in (yd_near, yd_far - s):
            parts.append(ruby_box("Rack Upright",
                                  xs, yd, 0, s, s, plat_z, color=C_STEEL))

    # Longitudinal spine beams tying the upright tops (along X).
    spine_len = x_stations[-1] + s - x_stations[0]
    for yd in (yd_near, yd_far - s):
        parts.append(ruby_box("Rack Spine",
                              x_stations[0], yd, beam_z, spine_len, s, s,
                              color=C_STEEL))

    # Platform cross-beams (along Yd) — now SIMPLY SUPPORTED: propped at the
    # corridor uprights AND at the container walls (via the wall brackets below),
    # so the upper totes are no longer cantilevered. Span wall-to-wall.
    near_end, far_end = BLUE_IBC_Y, IBC_FAR_Y + IBC_D   # 30 .. 2332 (beam outer ends)
    for xs in x_stations:
        parts.append(ruby_box("Rack Platform Beam",
                              xs, near_end, beam_z, s, far_end - near_end, s,
                              color=C_STEEL))

    # ── Equipment-panel support frame: extend the MIDDLE corridor station up to
    # the panel top (EQPANEL_Z_HI) and close it into a rectangle the wet-end panel
    # bolts to — two corridor uprights + top rail + floor-level beam. The panel
    # butts the film-plane (-X) face of this station. ──
    mid_xs = x_stations[1]
    for yd in (yd_near, yd_far - s):
        parts.append(ruby_box("Panel Frame Upright",
                              mid_xs, yd, plat_z, s, s, EQPANEL_Z_HI - plat_z,
                              color=C_STEEL))
    parts.append(ruby_box("Panel Frame Top Rail",
                          mid_xs, yd_near, EQPANEL_Z_HI - s, s, yd_far - yd_near, s,
                          color=C_STEEL))
    parts.append(ruby_box("Panel Frame Floor Beam",
                          mid_xs, yd_near, 0, s, yd_far - yd_near, s,
                          color=C_STEEL))

    c_bolt = "#3A3A42"

    # ── Floor feet: 150×150×12 base flange plate ON the floor + 4 M12 anchor
    # bolts through the plate into the slab under each corridor upright — fixes
    # the frame down (vertical + uplift restraint). ──
    fp, ft, bpc = IBC_FOOT_PLATE, IBC_FOOT_PLATE_T, IBC_FOOT_BOLT_PCD // 2
    for xs in x_stations:
        for yd in (yd_near, yd_far - s):
            cx, cy = xs + s / 2, yd + s / 2
            parts.append(ruby_box("Foot Flange Plate",
                                  cx - fp / 2, cy - fp / 2, 0, fp, fp, ft,
                                  color=C_STEEL))
            for dx in (-bpc, bpc):
                for dy in (-bpc, bpc):
                    parts.append(ruby_cylinder("Foot Anchor Bolt M12",
                                               cx + dx, cy + dy, 0, 7, ft + 4,
                                               color=c_bolt, axis="z"))

    # ── Load-bearing wall seat brackets: a welded knee bracket props each
    # platform-beam OUTER end at the near (Yd=0) and far (Yd=C_WID) walls,
    # turning the cantilever into a simple span. Each bracket is ONE welded
    # fabrication (Simpson-style shelf bracket): a vertical back-plate M12-bolted
    # to the wall, a horizontal seat the beam end lands on, and a triangular
    # gusset web welded between the two. ~110 kg per bracket. ──
    wpw, wpt = IBC_WBKT_PLATE_W, IBC_WBKT_PLATE_T          # back-plate 150(X) × 8(thick)
    proj, seat_t, gh = IBC_WBKT_SEAT_PROJ, IBC_WBKT_SEAT_T, IBC_WBKT_GUSSET_H  # seat projection, thickness, gusset depth
    sw = s + 20                         # seat width in X (beam + 10 each side)
    for xs in x_stations:
        gx = xs + s / 2 - 4             # gusset web (8mm) centerd on the beam
        for wall_yd, dir_in in ((0, 1), (C_WID, -1)):
            tip = wall_yd + dir_in * proj            # seat outer tip, under the beam end
            seat_y0 = min(wall_yd, tip)
            plate_y0 = wall_yd if dir_in > 0 else wall_yd - wpt
            # vertical back-plate bolted to the wall
            parts.append(ruby_box("Wall Bracket Plate",
                                  xs - 50, plate_y0, beam_z - gh - 10,
                                  wpw, wpt, gh + seat_t + 60, color=C_STEEL))
            # horizontal seat the beam end rests on
            parts.append(ruby_box("Wall Bracket Seat",
                                  xs - 10, seat_y0, beam_z - seat_t,
                                  sw, proj, seat_t, color=C_STEEL))
            # triangular gusset web welded between back-plate and seat tip
            parts.append(ruby_tri("Wall Bracket Gusset",
                                  (gx, tip, beam_z - seat_t),
                                  (gx, wall_yd, beam_z - seat_t),
                                  (gx, wall_yd, beam_z - seat_t - gh),
                                  8, color=C_STEEL))
            # 4× M12 wall anchor bolts through the back-plate (clear of the web)
            for bx in (xs - 30, xs + 80):
                for bz in (beam_z - gh + 30, beam_z - seat_t + 25):
                    parts.append(ruby_cylinder("Bracket Anchor Bolt M12",
                                               bx, plate_y0 - 10, bz, 7, wpt + 20,
                                               color=c_bolt, axis="y"))

    return '\n'.join(parts)


# ── Film plane mechanism ─────────────────────────────────────────────────────

def film_plane_mechanism():
    """Four corner rails + demountable brace cage + framed muslin screen.

    Rails run in +Y (depth) from the minimum carriage depth, at the four
    corners. A rigid rectangular brace cage (saddle/thumbscrew portals at each
    end) ties the rails into a knock-down box. The left rail's drum-zone
    segment (Yd 731–1631) is demountable so the light-trap drum can rotate.
    The muslin screen sits at the nominal depth FP_Y with a 2" angle frame.
    """
    parts = []
    rail = 40                       # 40×40mm rail tube
    z_bot = RAIL_OFF_BOT            # 150mm off the floor (raised +50 to clear the Z130 walkway)
    z_top = C_HGT - RAIL_OFF - rail # 100mm off the ceiling
    x_left = RAIL_X_L               # 150
    x_right = RAIL_X_R - rail       # 4609
    y0 = FP_Y_MIN                   # rails start at min carriage depth
    y_end = y0 + RAIL_LEN           # 2300
    # All four corner rails CONTINUOUS, full length (rev9 B2: the drum is offset
    # clear of the X=150 left rail via the panel bay — no demountable segment).
    for rz, nm in [(z_bot, "BR"), (z_top, "TR"), (z_bot, "BL"), (z_top, "TL")]:
        x = x_right if nm.endswith("R") else x_left
        parts.append(ruby_box(f"FP Rail {nm}",
                              x, y0, rz, rail, RAIL_LEN, rail, color=C_STEEL))

    # Demountable brace cage — rectangular portal at each end (50×50 RHS).
    s = BRACE_RHS
    for py, pn in [(FP_Y_MIN, "pinhole"), (FP_Y, "film")]:
        parts.append(ruby_box(f"FP Brace Vert L ({pn})",
                              RAIL_X_L, py, BRACE_Z_BOT,
                              s, s, BRACE_Z_TOP - BRACE_Z_BOT, color=C_STEEL))
        parts.append(ruby_box(f"FP Brace Vert R ({pn})",
                              RAIL_X_R - s, py, BRACE_Z_BOT,
                              s, s, BRACE_Z_TOP - BRACE_Z_BOT, color=C_STEEL))
        parts.append(ruby_box(f"FP Brace Beam Bottom ({pn})",
                              RAIL_X_L, py, BRACE_Z_BOT,
                              RAIL_X_R - RAIL_X_L, s, s, color=C_STEEL))
        parts.append(ruby_box(f"FP Brace Beam Top ({pn})",
                              RAIL_X_L, py, BRACE_Z_TOP - s,
                              RAIL_X_R - RAIL_X_L, s, s, color=C_STEEL))

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


def ruby_panel_z(name, ax_, ay, bx, by, thickness, height, color=None, alpha=None):
    """Thin vertical panel (wall) from point A to point B, extruded in +Z."""
    dx, dy = bx - ax_, by - ay
    length = math.hypot(dx, dy)
    px, py = -dy / length, dx / length          # unit perpendicular
    hw = thickness / 2.0
    c = [(ax_ + px * hw, ay + py * hw), (bx + px * hw, by + py * hw),
         (bx - px * hw, by - py * hw), (ax_ - px * hw, ay - py * hw)]
    pts_ruby = ', '.join(f'[{mm(round(x, 2))},{mm(round(y, 2))},0]' for x, y in c)
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


# ── Electrical (panel + battery, pinhole wall) ───────────────────────────────

def electrical():
    """Electrical panel (EP) + battery bank on the pinhole wall (Yd=0), plus the
    flush-mount external power panel on the exterior face.

    EP mounts high (Z 1600–2200); the slim battery bank low (Z 100–600). Both
    protrude into the container from the pinhole wall. The external power panel
    is flush in the exterior face (ghosted) — no interior conflict.
    """
    parts = []
    ep_d = 160   # EP enclosure depth into the container (Yd)

    parts.append(ruby_box("Electrical Panel (EP)",
                          EP_X, 0, EP_H_LO,
                          EP_W, ep_d, EP_H_HI - EP_H_LO, color=C_ELEC))

    # Battery bank — 2× LiFePO4 side by side.
    bw = (BA_W - 20) / 2
    for i, bx in enumerate((BA_X, BA_X + bw + 20)):
        parts.append(ruby_box(f"Battery {i + 1} (12V 100Ah LiFePO4)",
                              bx, 0, BA_H_LO,
                              bw, BA_D, BA_H_HI - BA_H_LO, color=C_BATT))

    # External power panel — flush in the exterior face (Yd<0), shown ghosted.
    parts.append(ruby_box("Ext. Power Panel (exterior)",
                          PWR_PANEL_X, -WALL_T - 25, PWR_PANEL_Z,
                          PWR_PANEL_W, 25, PWR_PANEL_H, color=C_ALUM, alpha=0.5))
    # It penetrates the wall — interior face rectangle matching the exterior.
    parts.append(ruby_box("Ext. Power Panel (interior face)",
                          PWR_PANEL_X, 0, PWR_PANEL_Z,
                          PWR_PANEL_W, 20, PWR_PANEL_H, color=C_ELEC))

    return '\n'.join(parts)


# ── Chemistry prep shelf (ceiling-hung) ──────────────────────────────────────

def shelf():
    """Chemistry prep shelf — ceiling-hung at Yd 300–600, suspended by 4 rods.

    A 600×300mm board at Z=1025 near the pinhole wall (behind the near walkway),
    hung from the ceiling by four Ø10 rods at the corners.
    """
    parts = []
    parts.append(ruby_box("Chem Shelf",
                          SHELF_X_L, SHELF_YD_NEAR, SHELF_H - SHELF_T,
                          SHELF_W, SHELF_DEPTH, SHELF_T, color=C_SHELF))

    rr = SHELF_HANGER_D / 2.0
    rod_h = C_HGT - SHELF_H
    inset = 20
    for hx in (SHELF_X_L + inset, SHELF_X_R - inset):
        for hy in (SHELF_YD_NEAR + inset, SHELF_YD_FAR - inset):
            parts.append(ruby_cylinder("Shelf Hanger Rod",
                                       hx, hy, SHELF_H, rr, rod_h,
                                       color=C_STEEL, n=12))

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
    # (X<1600) so they clear the electrical panel + batteries.
    sw_yd = 45                         # off the wall, past the trunking, clear of carriage
    for swx in (1450, 1530):
        parts.append(ruby_box("Pull Switch (ceiling)",
                              swx, sw_yd, cz - 40, 40, 40, 40, color=C_SWITCH))
        # beaded-chain pull cord: alternating bead radii read it as a flexible
        # cord (the 3D analogue of the 2D cord hatching) + a pull knob at the end
        cordx, cordy = swx + 20, sw_yd + 20
        z0, z1 = 900, cz - 40
        nb = max(8, int((z1 - z0) / 20))
        bh = (z1 - z0) / nb
        for k in range(nb):
            rr = 3.5 if k % 2 == 0 else 2.0
            parts.append(ruby_cylinder("Pull Cord", cordx, cordy, z0 + k * bh,
                                       rr, bh, color=C_CORD, axis="z", n=8))
        parts.append(ruby_cylinder("Pull Cord Knob", cordx, cordy, z0 - 16,
                                   6, 16, color=C_CORD, axis="z", n=10))

    # Conduit drops (10mm) from trunking down to EP and the battery bank.
    for cxc, zbot in ((1750, 2200), (2060, 600)):
        parts.append(ruby_box("Conduit Drop (10mm)",
                              cxc, 8, zbot, 10, 10, (cz - 25) - zbot, color=C_TRUNK))

    # Conduit runs along the ceiling from the trunking out to each fixture.
    cr, czc = 7, cz - 38
    for lx in (1000, 2900):    # → white LED panels (Cct G)
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
    # panel face (X=EQPANEL_X). Runs above the IBC stack (top Z=2020).
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
    # → Fan B (intake, Cct B): now in the NEAR corner by the pinhole wall (rev9/B2
    #   swap), so the rigid conduit RUNS ALONG THE PINHOLE WALL (Yd≈20) to the door
    #   end and then hops a short distance in +Yd to a fixed anchor on the
    #   door-frame top rail — staying in the near corner zone (Yd<653). A 1m coiled
    #   flex whip (electrical-report §Circuit B, Deutsch DT connectors — NOT modeled)
    #   drops from the anchor down the swinging panel to the low fan, taking up the
    #   ~56° transport swing.
    fb_anchor = (60, FAN_B_YD, czr)                  # fixed end on the door-frame top rail
    parts.append(ruby_pipe_run("Conduit to Fan B (intake, Cct B)",
                               [(300, 20, czr),
                                (60, 20, czr),
                                fb_anchor],
                               fcr, color=C_TRUNK))
    parts.append(ruby_box("Fan B Flex Anchor (door-frame top rail — flex whip not shown)",
                          40, FAN_B_YD - 25, czr - 25, 45, 50, 50, color=C_SWITCH))

    return '\n'.join(parts)


# ── Evaporative cooler + vent duct (exterior) ────────────────────────────────

def evap_cooler():
    """External evaporative cooler + supply duct through the pinhole wall.

    The cooler sits on the exterior of the pinhole wall; a Ø200 duct passes
    through the wall penetration (X=1000, Z=1900) into the container.
    """
    parts = []
    ext = -WALL_T
    cw, cd, ch = EVAP_W, EVAP_D, EVAP_H          # 600 × 350 × 800
    # Cooler unit standing on the GROUND outside the pinhole wall.
    parts.append(ruby_box("Evap Cooler (on ground)",
                          EVAP_DUCT_X - cw / 2, ext - cd - 100, 0,
                          cw, cd, ch, color=C_EVAP))

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
      Fan A (exhaust) — far/IBC end wall (X=C_LEN, right), high (Z=2200, above IBC stack).
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

    # Blue supply trunk — horizontal along the pinhole wall.
    x_l, x_r = PROC_TRAY_X_L + 300, RAIL_X_R
    parts.append(ruby_cylinder("Blue Supply Trunk (1/2in HDPE)",
                               x_l, yd, fz, pr, x_r - x_l, color=C_BLUE, axis="x"))

    # BV-02 isolation valve riser + body, at the pinhole centerline.
    parts.append(ruby_cylinder("BV-02 Riser",
                               BV02_X, yd, fz, pr, BV02_Z - fz, color=C_BLUE, axis="z"))
    parts.append(ruby_box("BV-02 (ball valve)",
                          BV02_X - 25, yd - 25, BV02_Z - 25, 50, 50, 50,
                          color=C_VALVE))

    # TAP-01 chemistry tap branch (¾") + spout.
    tr = TAP_PIPE_OD / 2
    parts.append(ruby_cylinder("TAP-01 Riser (3/4in)",
                               TAP_X, yd, fz, tr, TAP_Z - fz, color=C_BLUE, axis="z"))
    parts.append(ruby_box("TAP-01 (chem tap)",
                          TAP_X - 15, yd, TAP_Z, 30, 130, 40, color=C_VALVE))

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
    (X 4674-5893, Y 30-1046 & 1316-2332, Z 0-2020): fill runs over the tote tops
    (Z>2020); drain/suction runs stay in the clear corridor (Y 1046-1316) in
    separate lanes; the tray-pickup and spray runs drop to the floor and leave
    the IBC zone (X<4674) before traversing. Blue=fresh/process, brown=developer,
    gray=waste."""
    pr = 12
    nearX = IBC_COL_X + IBC_W / 2           # 5283 — IBC column center X
    nY = BLUE_IBC_Y + IBC_D / 2            # 538  — near col center (Blue #1 fill)
    fY = IBC_FAR_Y + IBC_D / 2            # 1824 — far col center (Blue #2 fill)
    topZ = 2 * IBC_H_600                   # 2020 — IBC stack top
    overZ = topZ + 230                     # 2250 — clear height over the totes
    pumpZ = PUMP_H_LO                      # 1370 — pump inlet bottom
    pumpX = EQPANEL_X - 50                  # pump inlet X — tracks panel
    cc = 1181                              # corridor centerline Y
    floor = 60                             # floor-run height
    upVZ = IBC_H_600 + IBC_VALVE_Z         # 1195 — upper-tier valve Z
    loVZ = IBC_VALVE_Z                     # 185  — lower-tier valve Z
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

    # Exterior FILL (blue): trunk runs in along the corridor centerline from the
    # sealed wall to a tee set BACK behind the panel-frame top rail; the cross-arm
    # runs in Yd directly over each Blue tote and drops STRAIGHT down into it.
    # Moving the tee back clears the new top rail (X 5258-5308, Z 2210-2260) and
    # removes the long forward over-the-top run on each side.
    fillTeeX = PANEL_FRAME_X + 150         # 5408 — behind the top rail
    pipe("Fill Trunk", [(C_LEN, EXT_FILL_YD, overZ), (fillTeeX, cc, overZ)], C_BLUE)
    parts.append(ruby_tee("Fill Tee", (fillTeeX, cc, overZ),
                          (0, 1, 0), (1, 0, 0), pr, color=C_BLUE))
    # Drop ENDS BELOW the stack top (topZ=2*IBC_H_600) so the pipe penetrates the
    # tote's top cap and reads as connected — ending at topZ+20 left it hovering
    # ~40mm above the bottle, looking disconnected from Blue #1/#2.
    fill_in_z = topZ - 170                 # ~1850 — penetrates the Blue tote's top cap
    pipe("Fill → Blue #1",
         [(fillTeeX, cc, overZ), (fillTeeX, nY, overZ), (fillTeeX, nY, fill_in_z)],
         C_BLUE)
    pipe("Fill → Blue #2",
         [(fillTeeX, cc, overZ), (fillTeeX, fY, overZ), (fillTeeX, fY, fill_in_z)],
         C_BLUE)

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

    # IBC valves → their own pumps, so circuits never share a crossing path.
    # The two Blue totes feed a PARALLEL suction manifold (Z=upVZ). The valve taps
    # are set back 250mm toward the sealed wall — BEHIND the panel frame — so the
    # straight header sits clear behind the uprights (no elbow in the frame); the
    # center feed to P-01 passes forward through the clear gap between the uprights
    # (Yd 1096-1266). Brown (P-02) and Waste (P-03) run low (Z=loVZ) and cross
    # cleanly UNDER the Blue header before rising to the right column.
    blueTapX = nearX + 250                  # 5533 — Blue valve tap behind the frame, nearer the sealed wall
    tap_in = 80                             # extend each end into the tote to meet the IBC valve/body
    pipe("Blue Suction Manifold",
         [(blueTapX, EQPANEL_YD - tap_in, upVZ),
          (blueTapX, EQPANEL_YD_FAR + tap_in, upVZ)], C_BLUE)
    parts.append(ruby_tee("Blue Manifold Tee", (blueTapX, cc, upVZ),
                          (0, 1, 0), (-1, 0, 0), pr, color=C_BLUE))
    pipe("Manifold → P-01",
         [(blueTapX, cc, upVZ), (rxA, cc, upVZ), (rxA, pyL, upVZ), (rxA, pyL, pZ1)],
         C_BLUE)
    pipe("Brown → P-02",
         [(nearX, EQPANEL_YD, loVZ), (rxA, EQPANEL_YD, loVZ),
          (rxA, pyR, loVZ), (rxA, pyR, pZ1)], C_IBC_BROWN)
    pipe("Waste → P-03",
         [(nearX, EQPANEL_YD_FAR, loVZ), (rxB, EQPANEL_YD_FAR, loVZ),
          (rxB, pyR, loVZ), (rxB, pyR, pZ2)], C_IBC_WASTE)

    # Processing-tray sump (per water-system Detail A): pickup riser UP through
    # the cantilevered near-walkway grate to the valve above deck, back DOWN
    # through the grate, then routed UNDERNEATH at floor level (Z=30 — below the
    # 50mm grate AND the Z=100 film-plane rails) through the tray–IBC gap into
    # the corridor and up to the pump. Keeps the film-plane structure clear.
    gapX = (PROC_TRAY_X_R + IBC_COL_X) / 2     # 4651.5 — centered in the 45mm gap
    valveZ = WALKWAY_H + 65                     # 130 — valve body above the deck
    pipe("Tray Sump → P-04",
         [(PROC_TRAY_DRAIN_X, PROC_TRAY_DRAIN_YD, PROC_TRAY_SUMP_Z),
          (PROC_TRAY_DRAIN_X, PROC_TRAY_DRAIN_YD, valveZ),
          (PROC_TRAY_DRAIN_X + 70, PROC_TRAY_DRAIN_YD, valveZ),
          (PROC_TRAY_DRAIN_X + 70, PROC_TRAY_DRAIN_YD, 30),
          (gapX, PROC_TRAY_DRAIN_YD, 30),
          (gapX, cc, 30), (rxB, cc, 30), (rxB, pyL, 30), (rxB, pyL, pZ2)],
         C_IBC_WASTE)

    # Pump → filters → spray-bar Blue trunk.
    pipe("Pump → Filters", [(pumpX, cc, pumpZ), (pumpX, cc, 700)], C_BLUE)
    pipe("Filters → Spray Trunk",
         [(pumpX, cc, 700), (pumpX, cc, floor), (RAIL_X_R, cc, floor),
          (RAIL_X_R, 12, floor), (RAIL_X_R, 12, SPRAY_BAR_FEED_Z)], C_BLUE)

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
        component("Panel & Pivot Axle", "Pivot Axle", panel_pivot()),
        component("Spray Bar", "Spray Bar", spray_bar()),
        component("Equipment Panel", "Equipment Panel", equipment_panel()),
        component("IBC Stack", "IBC Stack", ibc_stack()),
        component("IBC Rack", "IBC Rack", ibc_rack()),
        component("Light-Trap Drum", "Light Trap", light_trap_drum()),
        component("Light-Trap Bay", "Light Trap", light_trap_bay()),
        component("Electrical", "Electrical", electrical()),
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
        ("Film Plane & Pinhole", ["Pinhole", "Optical Cone", "Film Plane"]),
        ("Water Systems", ["Processing Tray", "Spray Bar", "Equipment Panel",
                           "IBC Stack", "IBC Rack", "Shelf", "Water Hookups",
                           "Water Plumbing"]),
        ("Electrical Systems", ["Electrical", "Lighting"]),
        ("Hinge Panel & Drum", ["Light Trap", "Light Seal", "Pivot Axle"]),
        ("Ventilation", ["Evap Cooler", "Fans"]),
        ("Walkways", ["Walkways"]),
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

# ── Idempotent rebuild: erase prior generated instances (keep 'Sree'), then
# purge their now-unused definitions so names don't collide on re-add.
to_erase = entities.to_a.select {{ |e|
  (e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)) &&
  !(e.is_a?(Sketchup::ComponentInstance) && e.definition.name == "Sree")
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

# rev10: the Ø89 swing pivot post (panel_pivot) reuses the film-plane far-left upright,
# so strike the original 50×50 "FP Brace Vert L (film)" post to avoid a duplicate.
fpdef = model.definitions.to_a.find {{ |d| d.name =~ /Film Plane Mechanism/ }}
fpdef.entities.grep(Sketchup::Group).each {{ |g| g.erase! if g.name == "FP Brace Vert L (film)" }} if fpdef

# ── Major-component callouts (Labels tag — shown only in the "Labeled" scene) ──
{overview_labels()}

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
                        help="Write Ruby to src/models/tbs_model.rb")
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
