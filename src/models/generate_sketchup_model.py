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
import contextlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "generators"))
from tbs_constants import C_LEN, C_WID, C_HGT, WALL_T, PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR, PROC_TRAY_RIM, PROC_TRAY_FLOOR_Z_LOW, tray_floor_z, WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T, WALKWAY_FAR_YD, WALKWAY_RIGHT_X, WALKWAY_RIGHT_W, WALKWAY_LEFT_X, LEFT_WK_CANT_ARM_Z0, WALKWAY_BRACKET_T, WALKWAY_BRACKET_H, CONTAINER_RIB_SPACING, WALKWAY_WIDE_BRACKET_T, WALKWAY_WIDE_BRACKET_H, WALKWAY_NEAR_WIDE_W, WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_X_R, WALKWAY_LEFT_WIDE_W, WALKWAY_LEFT_WIDE_YD_L, WALKWAY_LEFT_WIDE_YD_R, CORRIDOR_YD_NEAR, CORRIDOR_YD_FAR, PH_X, PH_H, PH_D, FP_X_L, FP_X_R, FP_W, FP_H, FP_Y, FP_Y_MIN, RAIL_X_L, RAIL_X_R, RAIL_OFF, RAIL_OFF_TOP, RAIL_OFF_BOT, FP_ANGLE_LEG, BRACE_RHS, BAY_FRONT_X, BAY_BACK_X, BAY_WALL_T, PANEL_CENTER_T, PANEL_CORNER_T, PANEL_FLOOR_GAP, PANEL_FAN_BAND_Z, PANEL_CORNER_YD_L, PANEL_CORNER_YD_R, PIVOT_X, PIVOT_YD, SWING_LOCK_DEG, PANEL_CUT_YD, FAR_STRIP_YD0, PIVOT_POST_OD, DRUM_CAGE_X0, DRUM_CAGE_X1, DRUM_CAGE_YD_L, DRUM_CAGE_YD_R, WALKWAY_NEAR_LIFTOUT_X_R, BB_OD, BB_H, PUMP_H_HI, EQPANEL_X, EQPANEL_T, EQPANEL_Z_HI, EQPANEL_YD, EQPANEL_YD_SPAN, IBC_COL_X, IBC_W, IBC_D, IBC_H_1000, IBC_PALLET_H, IBC_BOTTLE_INSET, BLUE_IBC_Y, BROWN_IBC_Y, IBC_FAR_Y, WASTE_IBC_Y, IBC_FRAME_RHS, IBC_FOOT_PLATE, IBC_FOOT_PLATE_T, IBC_FOOT_BOLT_PCD, IBC_WBKT_PLATE_W, IBC_WBKT_PLATE_T, IBC_WBKT_SEAT_PROJ, IBC_WBKT_SEAT_T, DRUM_CX, DRUM_CY, DRUM_R, DRUM_H_LT, LT_HOUSING_R, LT_HOUSING_T, LT_DRUM_OR, LT_DRUM_T, LT_CAP_T, LT_OPENING_DEG, WALKWAY_MUSLIN_NOTCH_DY, WALKWAY_MUSLIN_NOTCH_YD0, WALKWAY_MUSLIN_NOTCH_L_X0, WALKWAY_MUSLIN_NOTCH_R_X0, WALKWAY_MUSLIN_NOTCH_R_X1, EP_X, EP_W, EP_H_LO, EP_H_HI, ENCL_SHELL_D, PWR_PANEL_X, PWR_PANEL_W, PWR_PANEL_H, PWR_PANEL_Z, SOLAR_PANEL_L, SOLAR_PANEL_W, SOLAR_PANEL_T, SOLAR_N, SOLAR_TILT_DEG, SOLAR_GAP, SOLAR_ARRAY_X, SOLAR_ARRAY_YD, SOLAR_ARRAY_Z, SHELF_X_L, SHELF_X_R, SHELF_W, SHELF_H, SHELF_T, SHELF_DEPTH, SHELF_YD_NEAR, SHELF_YD_FAR, SHELF_STOW_TOP_Z, PULL_CORD_BOTTOM_Z, EVAP_W, EVAP_D, EVAP_H, EVAP_DUCT_X, EVAP_DUCT_Z, EVAP_DUCT_D, INVERTER_X, INVERTER_Z, INVERTER_W, INVERTER_H, INVERTER_D, FAN_DIAM, FAN_BODY_D, FAN_A_YD, FAN_A_H, FAN_B_YD, FAN_B_H, DUCT_DEPTH, DUCT_HEIGHT, BV02_X, BV02_Z, TAP_X, TAP_Z, TAP_PIPE_OD, PUMP_PIPE_OD, SPRAY_BAR_FEED_Z, PROC_TRAY_DRAIN_X, PROC_TRAY_DRAIN_YD, PROC_TRAY_SUMP_Z, PWP_FILTER_X1, PWP_FILTER_X2, PWP_FILTER_X3, PWP_FILTER_TOP_Z, PWP_FILTER_YD, PWP_P02_X, PWP_SV01_X, PWP_WAIST_Z

# Material colors used only by the 3D model (not in tbs_constants).
C_STEEL = "#B0B0B8"     # steel sections (rails, mount plate, brackets, rack)
C_FILM = "#2060A0"      # film plane / muslin screen
C_PINHOLE = "#CC6600"   # pinhole aperture + optical cone
C_RAIL = "#606068"      # HGR20 linear rail
C_CARR = "#C04010"      # HGH20CA carriage block
C_ALUM = "#C8D8E8"      # aluminum (cargo door panel, spray bar beam)
C_PLY = "#9C7B4D"       # marine ply (plumbing panel + hinge-panel Fan B mount band)
C_PLASTIC = "#6E8CA0"   # 1/8″ HDPE plastic sheet (rev11 hinge-panel skins + B2 bay; differentiates from wood C_PLY)
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
        "Pivot Axle", "Spray Bar", "Plumbing Panel",
        "IBC Stack", "IBC Rack", "Light Trap", "Electrical", "Shelf",
        "Light Seal", "Lighting", "Evap Cooler", "Water Hookups", "Fans",
        "Water Plumbing", "Solar Array", "Fan Wiring", "EP Ext Wiring", "Labels"]


# Major system components to call out in the "Labeled" scene.
# (component instance name, label text, leader Δx mm, leader Δz mm) — the leader is
# anchored at the component's bounds top-centre and fanned out so labels don't pile up.
# (component name, text, leader Δx, Δy, Δz mm). Δy pulls the label OUT of a wall
# toward the viewer (the camera looks from the −Y / pinhole-wall side).
OVERVIEW_LABELS = [
    ("Pinhole Assembly",      "PINHOLE  Ø2.17mm",                 -140, -1120,  630),
    ("Processing Tray",       "PROCESSING TRAY",                  -250,     0,  650),
    ("Corridor Equipment",    "CORRIDOR PLUMBING PANEL",          520,     0,  820),
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
    (2399, 2400, 1200, "FILM PLANE\ntilt / swing", 0, 600, 400),  # tip ON the plane; label OUTSIDE far wall (Yd>2410)
    (PWP_FILTER_X2, PWP_FILTER_YD, 1670, "3-STAGE FILTER SKID", -300, -750, 350),  # ON the middle filter (kit bounds-center missed it)
    (SOLAR_ARRAY_X + 700, SOLAR_ARRAY_YD - 500, 450, "SOLAR ARRAY\n3× 200W (30° tilt)",
     -200, -700, 700),
    (5618, 1181, 2000, "FAN A\n(exhaust, IBC end)",  400,    0,  450),
    (275,   365,  680, "FAN B\n(intake, door end)", -820, -200,   80),  # out the cargo-door end (⊥ door), clear of drum
    (2060,   60,  600, "BATTERY 1× 100Ah\n(2nd pack ghosted = plug-in)",    -300, -600,  900),
    # Cct-E inverter lives inside the "Evap Cooler & Duct" component (interior, on the
    # pinhole wall below the EP), so it needs an explicit-point label. Anchor at its
    # top-centre; fan up-left + pulled toward the viewer, clear of the battery/E-stop.
    (INVERTER_X + INVERTER_W // 2, INVERTER_D // 2, INVERTER_Z + INVERTER_H,
     "CCT-E INVERTER\n12->120V AC (cooler)", -430, -820, 480),
    (1420,  -90, 1950, "EMERGENCY E-STOP\n(external panel — kills all DC)", -550, -450,  350),
    (EP_X + EP_W // 2, ENCL_SHELL_D + 38, EP_H_LO + 80,
     "INTERIOR E-STOP\n(EP face — parallel)", 360, -500, -180),
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


# Near-identical colors collapsed onto ONE representative each (tight greys/near-blacks at Δ≤6, plus a
# few same-hue grey/blue/yellow pairs at Δ≤10 — all imperceptible) so they SHARE a material.  Holds the
# overview's unique-material count near ~87 (from 100), well under Sketchfab's upload ceiling.
_CANON_RGB = {
    # tight greys / near-blacks (Δ≤6)
    (32, 32, 32): (26, 26, 26),
    (34, 34, 40): (26, 26, 26), (34, 34, 34): (26, 26, 26),
    (43, 43, 48): (42, 42, 42), (44, 44, 44): (42, 42, 42),
    (58, 58, 58): (51, 52, 58), (58, 58, 66): (51, 52, 58),
    (80, 80, 88): (80, 80, 90),
    (96, 96, 104): (88, 96, 112),
    (122, 128, 136): (128, 128, 138),
    (126, 126, 118): (119, 119, 119), (128, 128, 128): (119, 119, 119),
    (154, 160, 160): (154, 160, 166), (154, 160, 168): (154, 160, 166),
    (192, 192, 200): (184, 188, 196),
    (200, 176, 106): (200, 176, 112),
    (216, 207, 188): (216, 208, 188),
    # same-hue color pairs (Δ≤10) — blue / yellow, imperceptible
    (41, 128, 185): (41, 121, 184),
    (245, 197, 24): (241, 196, 15),
}


def hex_to_rgb(h):
    """Convert '#RRGGBB' to (r, g, b), collapsing near-identical colors to a canonical value so
    they share a material (holds the Sketchfab material count down)."""
    h = h.lstrip("#")
    rgb = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    return _CANON_RGB.get(rgb, rgb)


# Neutral that muted "context" colors blend toward — a light blue-grey matching the
# GhostEquip ghost so faded context reads as a quiet wash, not a saturated volume.
MUTE_NEUTRAL = (190, 190, 195)

GHOST_HEX = "#8C929B"   # single neutral blue-gray for ALL forced-ghost context (construction prior phases)


def mute_hex(h, f, neutral=MUTE_NEUTRAL):
    """Blend a '#RRGGBB' color a fraction `f` toward `neutral` (0 = unchanged, 1 = full
    neutral).  Used to desaturate ghosted context (e.g. IBC tanks) so strong circuit
    colors don't bury the key components — matches the muted feel of overview.skp.
    Under a forced-muted (ghost) context, ALL colors collapse to the single GHOST_HEX so the
    faded prior-phase context reads as one uniform gray (easiest to read against the current
    phase's full-color additions) and shares ONE material (Sketchfab caps materials at ~100)."""
    if _CTX_FORCE:
        return GHOST_HEX
    if not f:
        return h
    r, g, b = hex_to_rgb(h)
    nr, ng, nb = neutral
    blend = lambda c, n: round(c * (1 - f) + n * f)
    return "#%02X%02X%02X" % (blend(r, nr), blend(g, ng), blend(b, nb))


# Web viewers (e.g. Sketchfab) cap material count at ~100. Dozens of elements
# share a color, so materials are keyed by color+alpha and reused — the first
# group to use a given color+alpha names the shared material. This collapses
# ~130 per-element materials down to the number of distinct color+alpha combos.
_MAT_BY_COLOR = {}


def shared_mat_name(name, color, alpha):
    """Return a material name shared by every element of the same CANONICAL color + alpha.
    Under a forced-muted (ghost) context the name is namespaced ('ghost ' prefix) and keyed
    separately, so a ghosted static copy never collides on the same material as its full-color
    live twin (same group name, different color/alpha). Outside a forced context this is
    byte-identical to before (the key gains a constant False prefix; the returned name is unchanged)."""
    key = (_CTX_FORCE, hex_to_rgb(color), alpha if alpha is not None else 1.0)
    return _MAT_BY_COLOR.setdefault(key, ("ghost " + name) if _CTX_FORCE else name)


# Build-time MUTE CONTEXT.  Every drawing helper below takes `mute`/`alpha` that DEFAULT to `None`
# and resolve against the current muted() context (below) — so wrapping a builder in
# `with muted(MUTE_DESAT, MUTE_ALPHA): ...` builds all its geometry desaturated + translucent AT
# SOURCE (color run through mute_hex(color, mute)).  Outside a context the defaults are 0.0 / opaque,
# byte-identical to before.  This replaces the old post-build "mute_groups" re-coloring pass +
# MUTE_TAGS allow-list that generate_pinhole_water_panel.py used to maintain.
_CTX_MUTE, _CTX_ALPHA, _CTX_FORCE = 0.0, None, False


@contextlib.contextmanager
def muted(mute, alpha, force=False):
    """Within this block, drawing helpers build muted CONTEXT/backdrop geometry at source.
    force=True makes the context's mute/alpha WIN over whatever the caller passes — so builders
    that hardcode their own alpha/mute (e.g. ibc_stack(alpha=0.85)) are still fully ghosted."""
    global _CTX_MUTE, _CTX_ALPHA, _CTX_FORCE
    prev = (_CTX_MUTE, _CTX_ALPHA, _CTX_FORCE)
    _CTX_MUTE, _CTX_ALPHA, _CTX_FORCE = mute, alpha, force
    try:
        yield
    finally:
        _CTX_MUTE, _CTX_ALPHA, _CTX_FORCE = prev


def _mute_ctx(mute, alpha):
    """Resolve a helper's mute/alpha against the current muted() context (idempotent).
    Under force, the context values override the caller's; otherwise the caller's explicit
    (non-None) values win, so outside a muted() block this is byte-identical to passing them through."""
    if _CTX_FORCE:
        return (_CTX_MUTE, _CTX_ALPHA if _CTX_ALPHA is not None else alpha)
    return (_CTX_MUTE if mute is None else mute, _CTX_ALPHA if alpha is None else alpha)


def ruby_box(name, x, y, z, w, d, h, color=None, alpha=None, both_sides=False, mute=None):
    """Generate Ruby to create a named box group inside the `ents` context.

    Parameters are in mm. x, y, z: origin corner (min X, min Yd, min Z).
    w, d, h: width (X), depth (Yd), height (Z). Boxes are added to `ents`,
    the entities collection of the enclosing component definition.
    `both_sides` paints the back faces too (so interior + exterior read the
    same — used for the container shell).
    """
    mute, alpha = _mute_ctx(mute, alpha)
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
        color = mute_hex(color, mute)
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


def ruby_prism(name, pts, z, h, color=None, alpha=None, mute=None):
    """A vertical prism from an arbitrary polygon (list of (x, y) mm points) at height z,
    pushpulled up by h. Same material handling as ruby_box. Used for NOTCHED grates so the deck
    is ONE continuous piece (a bite cut out of one edge), not separate sections needing support."""
    mute, alpha = _mute_ctx(mute, alpha)
    z0, h_mm = mm(z), mm(h)
    face_pts = ", ".join(f"[{mm(px)},{mm(py)},{z0}]" for px, py in pts)
    lines = [
        f'  # {name}',
        f'  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  face = grp.entities.add_face({face_pts})',
        f'  face.reverse! if face.normal.z < 0',
        f'  face.pushpull({h_mm})',
    ]
    if color:
        color = mute_hex(color, mute)
        r, g, b = hex_to_rgb(color)
        mat_nm = shared_mat_name(name, color, alpha)
        lines.append(f'  mat = model.materials["{mat_nm}"] || model.materials.add("{mat_nm}")')
        lines.append(f'  mat.color = Sketchup::Color.new({r}, {g}, {b})')
        lines.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        lines.append(f'  grp.material = mat')
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


def sketchfab_meta_ruby(title, description, model_id, tags="tbs sketchup", force_name=False):
    """Ruby that stamps the Sketchfab upload metadata onto the active model so a
    `--send` regen carries its identity — the `sketchfab` attribute dict (title,
    description, tags, and the stable `model_id`) plus model.name/description.

    Setting `model_id` is what makes the manual Sketchfab re-upload REUSE the same
    model (stable UID → the embedded iframe never has to change); without it a fresh
    doc uploads as a brand-new model and the name/description come up empty.

    `force_name=True` sets model.name/description UNCONDITIONALLY (the generator is the
    source of truth for the model's identity). Use it for models whose on-disk .skp keeps
    coming back with a blank/filename name so fill-if-blank never re-stamps it (water.skp).
    The sketchfab attribute dict below stays fill-if-blank regardless, so the stable
    model_id and any Sketchfab-UI edits to the dict are never clobbered.
    """
    import json
    t, d, mid, tg = (json.dumps(x) for x in (title, description, model_id, tags))
    # NON-DESTRUCTIVE by default: fill each field ONLY if blank, so a regen / re-send (or even a
    # mis-directed send) NEVER overwrites metadata you've edited. A fresh blank doc still gets the full
    # identity + the stable model_id for the manual re-upload; an existing doc keeps whatever it has.
    name_guard = "" if force_name else " if model.name.to_s.strip.empty?"
    desc_guard = "" if force_name else " if model.description.to_s.strip.empty?"
    return ("# ── Sketchfab metadata — sketchfab dict fill-only-if-blank; name/desc forced when requested ──\n"
            f"model.name = {t}{name_guard}\n"
            f"model.description = {d}{desc_guard}\n"
            f'model.set_attribute("sketchfab", "model_title", {t}) if model.get_attribute("sketchfab", "model_title").to_s.strip.empty?\n'
            f'model.set_attribute("sketchfab", "model_description", {d}) if model.get_attribute("sketchfab", "model_description").to_s.strip.empty?\n'
            f'model.set_attribute("sketchfab", "model_id", {mid}) if model.get_attribute("sketchfab", "model_id").to_s.strip.empty?\n'
            f'model.set_attribute("sketchfab", "model_tags", {tg}) if model.get_attribute("sketchfab", "model_tags").to_s.strip.empty?\n')


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
                  n=24, axis="z", mute=None):
    """Generate Ruby for a cylinder in `ents`, axis along +x/+y/+z.

    (cx, cy, cz): center of the base circle. radius/height in mm. Used for
    round bodies (filters, drum, ducts, pipe stubs, fans).
    """
    mute, alpha = _mute_ctx(mute, alpha)
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
        color = mute_hex(color, mute)
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
    """Container as 4 panels — floor + 3 walls (NO ceiling: removed for clear top-down
    orbiting; also no cargo-door end wall — that's the hinged light-trap panel).

    Off-white shell so the systems and their placement read clearly against it.
    """
    w = C_SHELL
    parts = []

    parts.append(ruby_box("Container Floor",
                          0, 0, -WALL_T,
                          C_LEN, C_WID, WALL_T,
                          color=w, both_sides=True))

    # (Container ceiling intentionally omitted — cleaner top-down orbiting without it.)

    # Three shell walls — translucent so the systems read
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
    """Processing tray — RAISED, dual-axis-sloped 304 SS welded pan (tilted floor + rim)
    on a tapered HDPE shim base, holding a translucent chemistry bath.  The low corner
    (near-right / IBC side = the sump) sits at Z=PROC_TRAY_FLOOR_Z_LOW so the sump bottom
    rests on the container floor; the pan rises 1:200 in BOTH axes to the far-left corner
    (see tray_floor_z / tray_rim_top_z)."""
    xl, xr = PROC_TRAY_X_L, PROC_TRAY_X_R
    yn, yf = PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR
    tray_w, tray_d = xr - xl, yf - yn
    sheet_t, rim_t = 2, 2
    zc = PROC_TRAY_FLOOR_Z_LOW                       # low-corner floor top = shim base top

    parts = []
    # Tapered HDPE shim base — raises the pan so the 20mm sump well bottom rests on Z0
    parts.append(ruby_box("Tray Shim Base",
                          xl, yn, 0, tray_w, tray_d, zc - sheet_t,
                          color="#D8CFBC", alpha=0.9))
    # Welded pan FLOOR — dual-axis-tilted plane (two triangles at the true corner Z's)
    c_nl = [xl, yn, tray_floor_z(xl, yn)]
    c_nr = [xr, yn, tray_floor_z(xr, yn)]
    c_fr = [xr, yf, tray_floor_z(xr, yf)]
    c_fl = [xl, yf, tray_floor_z(xl, yf)]
    parts.append(ruby_tri("Processing Tray Floor A", c_nl, c_nr, c_fr, -sheet_t, color=C_TRAY))
    parts.append(ruby_tri("Processing Tray Floor B", c_nl, c_fr, c_fl, -sheet_t, color=C_TRAY))
    # Rims — walls on the raised, tilted pan (each placed at the local floor Z for its edge)
    znr = tray_floor_z((xl + xr) / 2, yn); zfr = tray_floor_z((xl + xr) / 2, yf)
    zlr = tray_floor_z(xl, (yn + yf) / 2); zrr = tray_floor_z(xr, (yn + yf) / 2)
    parts.append(ruby_box("Tray Rim Near", xl, yn, znr, tray_w, rim_t, PROC_TRAY_RIM, color=C_TRAY))
    parts.append(ruby_box("Tray Rim Far",  xl, yf - rim_t, zfr, tray_w, rim_t, PROC_TRAY_RIM, color=C_TRAY))
    parts.append(ruby_box("Tray Rim Left", xl, yn, zlr, rim_t, tray_d, PROC_TRAY_RIM, color=C_TRAY))
    parts.append(ruby_box("Tray Rim Right", xr - rim_t, yn, zrr, rim_t, tray_d, PROC_TRAY_RIM, color=C_TRAY))
    # Translucent chemistry bath inside the rims (at the raised level)
    zb = tray_floor_z((xl + xr) / 2, (yn + yf) / 2)
    parts.append(ruby_box("Chemistry Bath",
                          xl + rim_t, yn + rim_t, zb,
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
RWK_ARM_BOT, RWK_ARM_TOP = LEFT_WK_CANT_ARM_Z0, RWK_GRATE_Z   # arm underside Z93 (matches the LEFT arm; single-sourced) — ≥15mm over the full-width 1½ spray beam
RWK_AH = RWK_ARM_TOP - RWK_ARM_BOT                     # 22 (2×⅞in section, ⅞in deep)
RWK_ARM_W = 50.8                                       # 2in — arm width in Yd (2×⅞in section)
RWK_HL = 95                                           # half-lap line
RWK_BEARER_W = 50.8                                    # 2in — long-beam width in X (2×⅞in section)
RWK_BEARER_XS = (RWK_X_L, RWK_X_R - RWK_BEARER_W)      # long-beam left edges
RWK_BEARER_Z0 = RWK_ARM_TOP - 22                       # 93 — long-beam soffit (2×⅞in, ⅞in deep) — shaved for the ≥15mm beam clearance; needs a mid-span support (added arm) for stiffness — see TODO walkway-support flex
RWK_X_UP = IBC_COL_X - 20                              # 4654 — deep-box FRONT upright (= cp.FRONT_X); reconciled from the stale +60/4734 portal (flag 4)
RWK_UP_YDS = (CORRIDOR_YD_NEAR, CORRIDOR_YD_FAR - IBC_FRAME_RHS)   # 1046, 1266
# Outer long beam (X4589) OPEN-TOP NOTCHES — one per under-walkway ribbon lane where the FLUSH pipe crosses
# the beam into the corridor.  The carriage crown (Z66) to beam soffit (Z80) gap is too tight for the pipe to
# pass under, so the beam's top web is slotted instead (Z92-115), leaving the Z80-92 bottom web intact.  These
# Yds are the single source the corridor pipe routing (cp.ribbon_run / the sump line) reads back for its
# crossing Yd, so the notches and the pipes can't drift apart.
RWK_RIBBON_NOTCH_YDS = [1110, 1132, 1194, 1241]        # lanes 0,1,2,3 corridor-crossing Yd (index-matched to cp.RIBBON_LANE_X)
RWK_RIBBON_NOTCH_W   = 34                              # Yd width per notch (pipe OD 21 + clearance)
RWK_NOTCH_FLOOR      = RWK_GRATE_Z - PUMP_PIPE_OD - 2  # 92 — notch floor, 2mm below the flush pipe soffit (Z94)

# Inner long beam is CRANKED outboard around the muslin-drop rod slot: the rigid muslin batten drops
# straight down at the tray edge (X=RWK_X_L), which sits over the inner beam — so over the notch Yd the
# beam is jogged outboard by the full notch depth (its inboard face moves R_X0→R_X1) with angled ramps,
# vacating the entire notch footprint for the rod while the beam stays ONE continuous (uncut) member.
# Right walkway only — the left notch falls between floor-leg brackets, no beam under it. Tied to the
# muslin-notch constants so the crank can't drift from the notch it clears.
RWK_CRANK_N0   = WALKWAY_MUSLIN_NOTCH_YD0                              # 1912 — notch Yd start
RWK_CRANK_N1   = WALKWAY_MUSLIN_NOTCH_YD0 + WALKWAY_MUSLIN_NOTCH_DY    # 2062 — notch Yd end
RWK_CRANK_DX   = WALKWAY_MUSLIN_NOTCH_R_X1 - WALKWAY_MUSLIN_NOTCH_R_X0 # 100 — jog = notch depth (clears the full notch)
RWK_CRANK_RAMP = 100                                                  # angled ramp Yd length each side
RWK_CRANK_Y0   = RWK_CRANK_N0 - RWK_CRANK_RAMP                        # 1812 — ramp-out start
RWK_CRANK_Y1   = RWK_CRANK_N1 + RWK_CRANK_RAMP                        # 2162 — ramp-in end


def _yd_split(y0, y1, cuts):
    """Sub-intervals of [y0,y1] with each (cy0,cw) in `cuts` removed (used to segment a long
    beam around arm half-laps and pipe notches)."""
    segs, ys = [], y0
    for cy0, cw in sorted(cuts):
        if cy0 > ys:
            segs.append((ys, cy0))
        ys = max(ys, cy0 + cw)
    if ys < y1:
        segs.append((ys, y1))
    return segs


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


def _rwk_long_beam(x, cross_ranges, notches=(), y0=0, y1=C_WID):
    """Yd long beam half-lapped at the arms it crosses (cross_ranges = (yd0, w)): continuous UPPER
    half + LOWER half cut away at each crossing.  `notches` = (yd0, w) OPEN-TOP pipe slots (outer beam
    only): the UPPER web is cut away and the lower web dropped to RWK_NOTCH_FLOOR so a flush ribbon pipe
    crosses through the top of the beam.  `y0..y1` restricts the run to a Yd sub-range (used to build the
    STRAIGHT portions of the cranked inner beam either side of the muslin-rod jog)."""
    out = []
    # UPPER half (Z95-115): full Yd, minus the pipe notches (an open-top notch removes the upper web)
    for s0, s1 in _yd_split(y0, y1, list(notches)):
        out.append(ruby_box(f"RWk Long beam X{int(x)} upper", x, s0, RWK_HL, RWK_BEARER_W, s1 - s0, RWK_ARM_TOP - RWK_HL, color=C_STEEL))
    # LOWER web (Z80-95): removed at arm half-laps AND at notches (a reduced-height web fills the notch below)
    for s0, s1 in _yd_split(y0, y1, list(cross_ranges) + list(notches)):
        out.append(ruby_box(f"RWk Long beam X{int(x)} lower", x, s0, RWK_BEARER_Z0, RWK_BEARER_W, s1 - s0, RWK_HL - RWK_BEARER_Z0, color=C_STEEL))
    # at each notch: the surviving Z80-NOTCH_FLOOR bottom web (skip where an arm half-lap already removed it)
    for n0, nw in notches:
        for s0, s1 in _yd_split(n0, n0 + nw, list(cross_ranges)):
            out.append(ruby_box(f"RWk Long beam X{int(x)} notch web", x, s0, RWK_BEARER_Z0, RWK_BEARER_W, s1 - s0, RWK_NOTCH_FLOOR - RWK_BEARER_Z0, color=C_STEEL))
    return out


def _rwk_inner_beam_cranked(x, cross_ranges):
    """The inner right-walkway long beam, CRANKED outboard by RWK_CRANK_DX over the muslin-drop notch
    (Yd RWK_CRANK_N0..N1) with angled ramps, so the rigid muslin rod drops straight down at the tray
    edge (X=x) clear of the beam — while the beam stays ONE continuous (uncut) member. Built as: the
    straight run before the crank (carries the arm half-laps) + a ramp-out prism + the jogged straight
    segment + a ramp-in prism + the straight run after. The crank zone has no arms/pipe-notches."""
    w, z0, h, dx = RWK_BEARER_W, RWK_BEARER_Z0, RWK_ARM_TOP - RWK_BEARER_Z0, RWK_CRANK_DX
    out = []
    out += _rwk_long_beam(x, cross_ranges, y0=0, y1=RWK_CRANK_Y0)                 # straight (arms)
    out.append(ruby_prism("RWk Long beam inner ramp-out",                        # angled ramp X→X+dx
                          [(x, RWK_CRANK_Y0), (x + w, RWK_CRANK_Y0),
                           (x + dx + w, RWK_CRANK_N0), (x + dx, RWK_CRANK_N0)], z0, h, color=C_STEEL))
    out += _rwk_long_beam(x + dx, (), y0=RWK_CRANK_N0, y1=RWK_CRANK_N1)           # jogged clear of notch
    out.append(ruby_prism("RWk Long beam inner ramp-in",                         # angled ramp X+dx→X
                          [(x + dx, RWK_CRANK_N1), (x + dx + w, RWK_CRANK_N1),
                           (x + w, RWK_CRANK_Y1), (x, RWK_CRANK_Y1)], z0, h, color=C_STEEL))
    out += _rwk_long_beam(x, cross_ranges, y0=RWK_CRANK_Y1, y1=C_WID)            # straight run after
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


def _notch_grate(name, gx0, z, gw, t, color, nx0, nx1, alpha=None):
    """Full-width (Yd 0..C_WID) walkway grate with a MUSLIN-DROP notch bitten out of its INBOARD
    (open-tray-facing) edge at the far end: X [nx0,nx1], Yd [WALKWAY_MUSLIN_NOTCH_YD0 .. +DY].
    ONE continuous notched deck (a bite cut out of the inboard edge) — NOT split sections, so no
    extra support/join is introduced. Grate-only."""
    gx1 = gx0 + gw
    ny0 = WALKWAY_MUSLIN_NOTCH_YD0
    ny1 = ny0 + WALKWAY_MUSLIN_NOTCH_DY
    if nx1 >= gx1:   # notch bitten out of the RIGHT (inboard) edge, x=gx1, over Yd ny0..ny1
        pts = [(gx0, 0), (gx1, 0), (gx1, ny0), (nx0, ny0), (nx0, ny1), (gx1, ny1), (gx1, C_WID), (gx0, C_WID)]
    else:            # notch bitten out of the LEFT (inboard) edge, x=gx0
        pts = [(gx0, 0), (gx1, 0), (gx1, C_WID), (gx0, C_WID), (gx0, ny1), (nx1, ny1), (nx1, ny0), (gx0, ny0)]
    return ruby_prism(name, pts, z, t, color=color, alpha=alpha)


def near_fixed_deck_grate(name, x0, z, t, color, alpha=None):
    """The FIXED near-walkway deck as ONE continuous piece: a WALKWAY_W-deep strip from x0 to
    WALKWAY_RIGHT_X with the EP/battery bump-out (WALKWAY_NEAR_WIDE_W deep, over
    [WALKWAY_NEAR_WIDE_X_L .. _X_R]) as an INTEGRAL inboard tab — not a separate butt-jointed
    section. The wall edge is inset one standard bracket-plate thickness (the 2mm-heavier wide
    plate is absorbed under the tab). The removable door-end lift-out band (near_x_l..X950) is a
    SEPARATE piece by design (it lifts out for transport) and is drawn by the caller."""
    bt = WALKWAY_BRACKET_T
    xr = WALKWAY_RIGHT_X
    wxl, wxr, ww = WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_X_R, WALKWAY_NEAR_WIDE_W
    # Wall edge at Yd=bt; inboard edge at Yd=WALKWAY_W, stepping out to Yd=ww over the bump span.
    pts = [(x0, bt), (xr, bt), (xr, WALKWAY_W),
           (wxr, WALKWAY_W), (wxr, ww), (wxl, ww), (wxl, WALKWAY_W),
           (x0, WALKWAY_W)]
    return ruby_prism(name, pts, z, t, color=color, alpha=alpha)


def left_liftout_grate(name, z, t, color, alpha=None):
    """The removable LEFT lift-out deck as ONE continuous piece: a WALKWAY_W-wide strip
    (X WALKWAY_LEFT_X..+WALKWAY_W, Yd 0..C_WID) with BOTH widenings integral — the drum-exit
    punch-out tab (out to WALKWAY_LEFT_WIDE_W over Yd [_YD_L.._YD_R]) and the muslin-drop notch
    (bitten IN to WALKWAY_MUSLIN_NOTCH_L_X0 over Yd [_YD0 .. +_DY]) — so no butt joint or extra
    support is introduced at either feature. Both sit on the same inboard (tray-facing) edge."""
    lx0 = WALKWAY_LEFT_X
    lx1 = lx0 + WALKWAY_W                                   # inboard edge
    tab_x1 = lx1 + (WALKWAY_LEFT_WIDE_W - WALKWAY_W)        # punch-out tab outer edge
    pyl, pyr = WALKWAY_LEFT_WIDE_YD_L, WALKWAY_LEFT_WIDE_YD_R
    nyd0 = WALKWAY_MUSLIN_NOTCH_YD0
    nyd1 = nyd0 + WALKWAY_MUSLIN_NOTCH_DY
    nx0 = WALKWAY_MUSLIN_NOTCH_L_X0                         # notch bites in to here
    pts = [(lx0, 0), (lx0, C_WID), (lx1, C_WID),
           (lx1, nyd1), (nx0, nyd1), (nx0, nyd0), (lx1, nyd0),   # muslin notch (in)
           (lx1, pyr), (tab_x1, pyr), (tab_x1, pyl), (lx1, pyl),  # drum-exit punch-out (out)
           (lx1, 0)]
    return ruby_prism(name, pts, z, t, color=color, alpha=alpha)


def right_walkway_grate():
    """Just the right walkway grate deck (cantilevered). Factored out so it can be put on
    the Walkways tag — letting the walkway-model 'Right Cantilever' scene show the bare
    beams + brackets while the grate still reads with the other decks."""
    return _notch_grate("Right walkway grate (cantilevered)", RWK_X_L, RWK_GRATE_Z,
                        WALKWAY_RIGHT_W, WALKWAY_GRATE_T, C_WALKWAY, WALKWAY_MUSLIN_NOTCH_R_X0, WALKWAY_MUSLIN_NOTCH_R_X1)


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
    notch_ranges = [(cy - RWK_RIBBON_NOTCH_W / 2, RWK_RIBBON_NOTCH_W) for cy in RWK_RIBBON_NOTCH_YDS]
    parts += _rwk_inner_beam_cranked(lx, arm_ranges)          # inner beam — CRANKED around the muslin-rod slot (uncut)
    parts += _rwk_long_beam(rx, arm_ranges, notch_ranges)     # outer beam — open-top notch at each ribbon lane
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


def walkways(include_right=True, include_right_hangers=None, grates_only=False):
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
    bt = WALKWAY_BRACKET_T                    # 8mm  — standard bracket plate (wall-edge inset)

    near_x_l = WALKWAY_LEFT_X + WALKWAY_W
    near_x_r = WALKWAY_RIGHT_X
    # The near/far grates run along the side walls from the left-walkway inner edge
    # (X=near_x_l). The floor-leg cantilever redesign has no kerb beam to cut around.
    near_len = near_x_r - near_x_l

    parts = []

    # Near deck — ONE continuous fixed piece with the EP/battery bump-out integral (no butt
    # joints at the widening). The whole-system view doesn't split off the removable door-end
    # band (walkway.skp does); the >10ft sheet splice is a cut-plan detail, not modeled here.
    parts.append(near_fixed_deck_grate("Walkway Near (fixed, bump integral)",
                                       near_x_l, grate_z, t, C_WALKWAY))

    # far deck: inset the FAR (wall) edge by the standard plate thickness; near edge unchanged
    parts.append(ruby_box("Walkway Far",
                          near_x_l, WALKWAY_FAR_YD, grate_z,
                          near_len, WALKWAY_W - bt, t, color=C_WALKWAY))

    if include_right:
        if include_right_hangers and not grates_only:
            # rev12: full CANTILEVER-rectangle support (+ grate), replaces the ceiling hangers.
            # The combined corner plates are drawn separately (own tag) so they also show in
            # the Film-Plane scene, so omit them here.
            parts.append(right_walkway_cantilever(include_combined=False))
        else:
            parts.append(_notch_grate("Walkway Right (IBC end)",
                                      WALKWAY_RIGHT_X, grate_z, WALKWAY_RIGHT_W, t,
                                      C_WALKWAY, WALKWAY_MUSLIN_NOTCH_R_X0, WALKWAY_MUSLIN_NOTCH_R_X1))

    # Left walkway — removable lift-out for transport (distinct color). ONE continuous piece:
    # drum-exit punch-out tab + muslin-drop notch both integral (no butt-jointed add-on).
    parts.append(left_liftout_grate("Walkway Left (REMOVABLE — transport)",
                                    grate_z, t, C_REMOVABLE))

    # grates_only (construction model): the brackets + left floor-leg cantilevers are their own
    # install steps, so skip the supports here and draw only the decks.
    if not grates_only:
        # Wall-cantilevered gusset brackets that actually hold the near & far decks up.
        parts.append(walkway_brackets())

        # Left walkway support: floor-leg cantilever brackets. Reuse the walkway model's
        # shared builder so the support design can't drift between the two models.
        import generate_walkway_model as wm
        parts.append('\n'.join(wm.left_floor_cantilevers()))

    # Right walkway support is now the cantilever rectangle (right_walkway_cantilever, above),
    # built with the grate when include_right_hangers — the ceiling hangers are retired (rev12).

    return '\n'.join(parts)


def walkway_brackets(which="both"):
    """Wall-cantilevered gusset brackets carrying the NEAR and FAR walkway grates.
    `which`: "both" (default), "near", or "far" — the construction model installs the far+right
    brackets before the tray and the near brackets after it.

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
    if which == "near":
        sides = [sides[0]]
    elif which == "far":
        sides = [sides[1]]

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
    # Cargo-door panel, operational position (X=0). rev11: 1/8″ HDPE plastic skins
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
    overview stays in sync with models/spraybar.skp: 40×25 304-SS RHS beam (laid flat)
    with a SIDE-mounted 3/4" LDPE manifold + 39 side-tapped 90° down-jet nozzles, two-wheel
    Ø32 carriages (curved saddle axle clamps + top/bottom beam clamp plates), flange-base
    ball joint, a single center feed into the manifold, and the push pole bound
    to the supply hose with zip ties. The tray-floor ref patch is omitted (overview has
    its own tray)."""
    import generate_spraybar_model as sb
    return '\n'.join([sb.build_beam(),
                      sb.build_carriages(include_floor=False),
                      sb.build_feed_pole()])


# ── Plumbing panel (pumps · filters · accumulator) ──────────────────────────
#
# RESOLVED (2026-07-01): overview + ibc-stack were rewired in generate_ruby() to reuse
# the CURRENT water builders — cp.frame/tote_restraint/rear_panel/equipment/plumbing/
# drains_ports + pw.kit/other_equipment/tap01_supply (the water.skp source) — so they
# now render the split Corridor / Pinhole-Wall panel design and stay in sync with
# water.skp.  The OLD pre-corridor-refactor builders (equipment_panel / water_hookups /
# spray_bar_plumbing / water_plumbing) + the legacy FSKID_X/F1_Z/F2_Z/F3_Z corridor-filter
# constants were DELETED 2026-07-05.  ibc_rack() (old single-portal frame, X4734) is now referenced
# ONLY by the ARCHIVED right-cantilever study (src/models/archive/) — the live models use the
# deep-box cp.frame() (X4654); kept so the archived study still imports, but effectively dead.


# ── IBC stack (4× totes, 2×2) + support rack ─────────────────────────────────

def ibc_stack(alpha=0.55, mute=0.0, cols="both"):
    """Four IBC totes in a 2×2 stack: pallet base + translucent bottle each.

    Near column (Yd=30): Brown developer below, Blue #1 on top.
    Far column (Yd=1316): Waste below, Blue #2 on top. X spans 4674–5893.
    ibc-reconfig-v2: 1000L caged composite totes (1168mm), direct-stacked to 2336mm.
    `alpha` sets the bottle translucency (lower = more transparent).
    `mute` (0–1) desaturates the bottle/pallet colors toward neutral so the stack
    reads as quiet CONTEXT (a faint tint) rather than saturated volumes — used where
    the IBC stack is a backdrop to other key systems (e.g. the corridor plumbing view).
    `cols`: "both" (default), "near" (pinhole-wall column only), or "far" (far column only)
    — used by the construction model to install the two columns as separate build steps.
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
    if cols == "near":
        totes = totes[:2]     # near / pinhole-wall column (Brown + Blue #1)
    elif cols == "far":
        totes = totes[2:]     # far column (Waste + Blue #2)
    for nm, yd, z0, col in totes:
        parts.append(ruby_box(f"{nm} pallet",
                              IBC_COL_X, yd, z0, IBC_W, IBC_D, pal,
                              color=mute_hex(C_PALLET, mute), alpha=(alpha if mute else None)))
        parts.append(ruby_box(f"{nm} bottle",
                              IBC_COL_X + inset, yd + inset, z0 + pal,
                              IBC_W - 2 * inset, IBC_D - 2 * inset, bottle_h,
                              color=mute_hex(col, mute), alpha=alpha))
    return '\n'.join(parts)


def ruby_tri(name, p1, p2, p3, thick, color=None, alpha=None, mute=None):
    """Triangular plate: a face through p1,p2,p3 pushpulled by `thick` along its
    normal (used for gusset plates)."""
    mute, alpha = _mute_ctx(mute, alpha)
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
        color = mute_hex(color, mute)
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


def film_plane_mechanism(part="all"):
    """Four corner rails + 8 wall-seat saddles + framed muslin screen.
    `part`: "all" (default), "beams" (the 4 corner rails + wall-seat saddles — the structural
    support installed in the hard-install phase), or "plane" (the muslin screen + 2" angle frame
    — the film plane installed in the photo-system phase).

    Rails run in +Y (depth), now full-width saddle-to-saddle, at the four corners.
    rev11: the demountable brace cage is RETIRED — each rail end anchors to the
    container with an IBC-style wall-seat saddle (the shell carries the rigidity);
    right rails bolted, left rails thumb-screw drop-in for the drum swing. The
    muslin screen sits at the nominal depth FP_Y with a 2" angle frame.
    """
    parts = []
    rail = 40                       # 40×40mm rail tube
    z_bot = RAIL_OFF_BOT            # 150mm off the floor (raised +50 to clear the Z130 walkway)
    z_top = C_HGT - RAIL_OFF_TOP - rail # 144mm off the ceiling (film-plane top rail dropped 44mm)
    x_left = RAIL_X_L               # 150
    x_right = RAIL_X_R - rail       # 4609
    # All four corner rails CONTINUOUS, now spanning the full width SADDLE-TO-SADDLE
    # (Yd 0 → C_WID) so each end lands on its wall-seat saddle with no gap (rev11).
    if part in ("all", "beams"):
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

    if part in ("all", "plane"):
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
                  color=None, alpha=None, n=48, z0=0, mute=0.0):
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
        color = mute_hex(color, mute)
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

def tilted_slab(name, x, y_near, z_base, w, length, t, tilt_deg, color, alpha=None, mute=0.0):
    """Flat slab tilted up from its near-bottom edge, rising in +Z and -Y (faces
    away from the container, toward the sun). length runs up the tilt."""
    th = math.radians(tilt_deg)
    dy, dz = -length * math.cos(th), length * math.sin(th)
    corners = [(x, y_near, z_base), (x + w, y_near, z_base),
               (x + w, y_near + dy, z_base + dz), (x, y_near + dy, z_base + dz)]
    pts = ', '.join(f'[{mm(px)},{mm(py)},{mm(pz)}]' for px, py, pz in corners)
    color = mute_hex(color, mute)
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
                             SOLAR_PANEL_T, SOLAR_TILT_DEG, "#1B3A6B", alpha=0.3))
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
    # A PV feed is a +/- PAIR, drawn as a BONDED ("siamese") pair of curly coil cords: the two
    # conductors run together (coiled, ~16mm apart with a tightened curl so they read as one
    # twisted pair, not a tangle) for the whole length, and FAN OUT only at the ends — straight
    # stubs at the array terminals and to the panel's two MC4 columns (+ at _px 0.192, - at 0.275).
    # The short end-legs fall under ruby_coil_cord's straight-stub threshold, so the fans render as
    # clean straight leads while the long middle legs coil. Coil cords mark the SOFT connector (vs
    # the rigid orthogonal conduit); the bonded run drapes DIAGONALLY up to the panel so it stays
    # right of + clear of the evap cooler (X720-1280) — an angle a rigid conduit can't take.
    jx = SOLAR_ARRAY_X + span / 2
    mc4_z = PWR_PANEL_Z + PWR_PANEL_H * 0.225          # land on the BOTTOM MC4 pair (PV1)
    pmid = PWR_PANEL_X + 0.2335 * PWR_PANEL_W          # midpoint of the two MC4 columns
    PAIR, FAN = 8, 18                                  # bonded half-spacing / array-end fan-out
    for s, panel_uf, col, sym in ((-1, 0.192, "#2D7A2D", "+"),     # (+) -> left MC4 column, green
                                  (+1, 0.275, "#1A1A1A", "-")):    # (-) -> right MC4 column, black
        p.append(ruby_coil_cord(f"PV cord ({sym}) (array -> panel MC4, bonded pair)",
                                [(jx + s * FAN,  SOLAR_ARRAY_YD - 20, SOLAR_ARRAY_Z + 60),  # array terminal (fanned)
                                 (jx + s * PAIR, SOLAR_ARRAY_YD - 50, SOLAR_ARRAY_Z + 60),  # converge into the pair
                                 (jx + s * PAIR, -WALL_T - 30,        SOLAR_ARRAY_Z + 60),  # bonded run toward panel
                                 (pmid + s * PAIR, -WALL_T - 30,      mc4_z),               # bonded, diagonal up
                                 (PWR_PANEL_X + panel_uf * PWR_PANEL_W, -WALL_T - 30, mc4_z)],  # split to its MC4 column
                                r=5, coil_r=13, color=col))
    return '\n'.join(p)


# ── Electrical (panel + battery, pinhole wall) ───────────────────────────────

def electrical():
    """EP + battery bank + external power panel. DELEGATES to the electrical model's builders
    (generate_electrical_model.power_core / battery / external_panel) so the overview's EP is IDENTICAL
    to electrical.skp by construction — no more hand-maintained duplicate that drifts (the skinny-column
    reorg made two copies untenable). The Cct-E inverter stays a SEPARATE overview component (below)."""
    import generate_electrical_model as em
    return '\n'.join([em.power_core(external_links=False), em.battery(), em.external_panel()])


def ep_external_wiring():
    """The two EP circuits that run OUT to the external panel — green PV feed (-> array/MPPT) and
    grey E-stop link (interior -> exterior). A SEPARATE component on the 'EP Ext Wiring' tag so the
    Ventilation scene can hide them and show only the evap-cooler (Cct E) circuit at the panel."""
    import generate_electrical_model as em
    return em.power_core(links_only=True)


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
    """Ceiling cable trunking + white LED strips (Cct G) + red safelight strips
    (Cct D) + pull-cord switches + conduit drops.

    Trunking runs the pinhole-wall ceiling line (Yd≈0, outside the optical
    cone); white strips run parallel to the two cargo-door-side safelights +
    over the plumbing panel; safelights span the width; pull switches hang from
    the pinhole wall near the EP.
    """
    parts = []
    cz = C_HGT                                 # ceiling

    # Cable trunking — 40×25 PVC along the pinhole wall ceiling, full length.
    parts.append(ruby_box("Cable Trunking (40x25 PVC)",
                          0, 0, cz - 25, C_LEN, 40, 25, color=C_TRUNK))

    # White LED strips (Cct G) — 3× 12V COB strips (in 981 channels): 2 run PARALLEL to
    # the two DRUM/cargo-door-side red strips (X≈520/2270, offset +80mm) over the tray;
    # the 3rd is rotated 90° to run the IBC/plumbing CORRIDOR length (X) and light the
    # plumbing panel. Ghosted (translucent) — they read as light sources.
    for wx in (600, 2350):     # parallel to the drum-side reds (X=520, 2270)
        parts.append(ruby_box("White LED Strip (Cct G)",
                              wx, 100, cz - 25, 40, C_WID - 200, 18,
                              color=C_LED_W, alpha=0.4))
    # 3rd: rotated 90°, runs X along the IBC corridor over the plumbing panel (Yd≈1046)
    parts.append(ruby_box("White LED Strip (Cct G, IBC corridor)",
                          IBC_COL_X, EQPANEL_YD - 20, cz - 25, C_LEN - IBC_COL_X - 43, 40, 18,
                          color=C_LED_W, alpha=0.4))

    # Red safelight strips (Cct D) — 3× N–S runs cut from ONE 5m COB reel → ~1,667mm
    # each (in 981 channels). (Was full-width C_WID-200; trimmed to fit the single reel.)
    for sx in (500, 2250, 4150):
        parts.append(ruby_box("Safelight Strip (Cct D)",
                              sx, 100, cz - 25, 40, 1667, 18,
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
    # are co-located at X≈1910–2240 (the EP column stacks above the battery). A single drop at
    # X2060 runs down the EP center face (Z1500–2100) and continues to the battery top.
    # (rev: the old second drop at X1750 was removed — the EP moved to X1910, leaving
    #  that drop orphaned over the swing-panel transport-lock stay plate.)
    for cxc, zbot in ((2060, 600),):
        parts.append(ruby_box("Conduit Drop (10mm)",
                              cxc, 8, zbot, 10, 10, (cz - 25) - zbot, color=C_TRUNK))

    # Conduit runs along the ceiling from the trunking out to each fixture.
    cr, czc = 7, cz - 38
    for wx in (600, 2350):    # → parallel white LED strips (Cct G)
        parts.append(ruby_cylinder("Conduit to White Strip (Cct G)",
                                   wx + 20, 40, czc, cr, 60,
                                   color=C_TRUNK, axis="y"))
    # → IBC-corridor strip: conduit from the wall trunking out to its Yd position
    parts.append(ruby_cylinder("Conduit to White Strip (Cct G)",
                               IBC_COL_X + 60, 40, czc, cr, EQPANEL_YD - 40,
                               color=C_TRUNK, axis="y"))
    for sx in (500, 2250, 4150):     # → red safelight strips (Cct D)
        parts.append(ruby_cylinder("Conduit to Safelight (Cct D)",
                                   sx + 20, 40, czc, cr, 60,
                                   color=C_TRUNK, axis="y"))

    # Circuit C — feed to the pump/filter plumbing panel (IBC corridor).
    # Branch off the ceiling trunking (Yd≈0) across to the panel center
    # (Yd≈1181), then drop to the top of the pump zone (Z=PUMP_H_HI) at the
    # panel face (X=EQPANEL_X). Runs at ceiling height (Z=2350), clearing the IBC stack top (Z=2336).
    pc_yd = EQPANEL_YD + EQPANEL_YD_SPAN / 2
    parts.append(ruby_cylinder("Conduit to Plumbing Panel (Cct C)",
                               EQPANEL_X, 40, czc, cr, pc_yd - 40,
                               color=C_TRUNK, axis="y"))
    parts.append(ruby_box("Conduit Drop to Pumps (Cct C)",
                          EQPANEL_X - 5, pc_yd - 5, PUMP_H_HI, 10, 10,
                          (cz - 25) - PUMP_H_HI, color=C_TRUNK))

    return '\n'.join(parts)


def fan_wiring(which="both", a_to_ep=False):
    """Power conduits to the two ventilation fans — Cct-A rigid run to Fan A (exhaust, far end)
    and Cct-B rigid run + wall box + flexible jumper to Fan B (intake, near end). On its OWN tag
    so the Ventilation scene shows the fan cables without the rest of the Lighting & Wiring.
    `which`: "both" (default), "A", or "B" — the construction model installs Fan A's conduit early
    (with Fan A, before the far IBC column) and Fan B's later. The shared EP feeds are drawn only
    for "both" (they connect back to the EP, installed in the electrical phase).
    a_to_ep=True (construction Phase 1, which="A"): also run Cct-A along the pinhole-wall ceiling
    trunk and DOWN to the EP drop point, so it's pre-run and waiting for the Phase-4 EP."""
    parts = []
    cz = C_HGT
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
    if which in ("both", "A"):
        parts.append(ruby_pipe_run("Conduit to Fan A (exhaust, Cct A)",
                                   [(fa_x, 20, czr),
                                    (fa_x, FAN_A_YD, czr),
                                    (fa_x, FAN_A_YD, fa_top)],
                                   fcr, color=C_TRUNK))
    if which == "A" and a_to_ep:
        # Pre-run Cct-A along the pinhole-wall ceiling trunk from the Fan A tap to the EP column,
        # then DOWN the pinhole wall to the EP drop point (the EP itself lands in Phase 4).
        ep_x = 2060
        parts.append(ruby_pipe_run("Fan A feed (Fan A tap -> pinhole-wall trunk to EP, Cct A)",
                                   [(fa_x, 20, czr), (ep_x, 20, czr)], fcr, color=C_TRUNK))
        parts.append(ruby_pipe_run("Fan A EP drop (down the pinhole wall to the EP, Cct A)",
                                   [(ep_x, 20, czr), (ep_x, 20, EP_H_HI)], fcr, color=C_TRUNK))
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
    if which in ("both", "B"):
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

    if which == "both":
        # ── Feed from the EP fan breakers up to the ceiling trunk, then along the trunk line to each
        #    fan tap — so Cct-A / Cct-B visibly connect back to their power source (the EP) in the
        #    Ventilation scene (the real trunking + EP drop are on the hidden Lighting tag). ──
        ep_x = 2060                                      # EP column X (matches the lighting conduit drop)
        parts.append(ruby_pipe_run("Fan feed riser (EP -> ceiling trunk, Cct A/B)",
                                   [(ep_x, 20, EP_H_HI), (ep_x, 20, czr)], fcr, color=C_TRUNK))
        parts.append(ruby_pipe_run("Fan A feed (EP -> Fan A tap, Cct A)",
                                   [(ep_x, 20, czr), (fa_x, 20, czr)], fcr, color=C_TRUNK))
        parts.append(ruby_pipe_run("Fan B feed (EP -> Fan B tap, Cct B)",
                                   [(ep_x, 20, czr), (fb_drop_x, fb_wall_yd, czr)], fcr, color=C_TRUNK))
    return '\n'.join(parts)


# ── Evaporative cooler + vent duct (exterior) ────────────────────────────────

def evap_cooler():
    """External evaporative cooler + supply duct through the pinhole wall.

    The cooler sits on the exterior of the pinhole wall; a Ø200 duct passes
    through the wall penetration (X=1000, Z=1900) into the container.
    """
    parts = []
    ext = -WALL_T
    cw, cd, ch = EVAP_W, EVAP_D, EVAP_H          # 508 × 254 × 711 (Hessaire MC18M)
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


# ── Ventilation fans (cargo-door end wall) ───────────────────────────────────

def fans(which="both"):
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
    # `which`: "both" (default), "A", or "B" — the construction model installs Fan A early
    # (before the far IBC column buries it) and Fan B later.
    out = []
    if which in ("both", "A"):
        out += fan_duct("Fan A (exhaust)", C_LEN, +1, FAN_A_YD, FAN_A_H)
    if which in ("both", "B"):
        out += fan_duct("Fan B (intake)", 0, -1, FAN_B_YD, FAN_B_H)
    return '\n'.join(out)


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


# ── Water / waste plumbing network ───────────────────────────────────────────

def ruby_pipe(name, p1, p2, r, color=None, alpha=None, n=16, mute=0.0):
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
        color = mute_hex(color, mute)
        rr, gg, bb = hex_to_rgb(color)
        mat_nm = shared_mat_name(name, color, alpha)
        lines.append(f'  mat = model.materials["{mat_nm}"] || '
                     f'model.materials.add("{mat_nm}")')
        lines.append(f'  mat.color = Sketchup::Color.new({rr}, {gg}, {bb})')
        lines.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        lines.append(f'  grp.material = mat')
    lines.append('')
    return '\n'.join(lines)


def ruby_flex_duct(name, p1, p2, r, color=None, alpha=None, ribs=None, mute=0.0):
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
        out.append(ruby_pipe(name, a, b, rr, color=color, alpha=alpha, n=14, mute=mute))
    return '\n'.join(out)


def ruby_coil_cord(name, waypoints, r=5.0, color=None, alpha=None,
                   coil_r=None, pitch=None, pts_per_turn=8, mute=0.0):
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
        out.append(ruby_pipe(name, a, p0, r, color=color, alpha=alpha, n=10, mute=mute))
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
                out.append(ruby_pipe(name, prev, pt, r, color=color, alpha=alpha, n=6, mute=mute))
                prev = pt
            p1 = _vadd(p0, _vscale(d, coil_L))              # coil end (back on axis)
            out.append(ruby_pipe(name, prev, p1, r, color=color, alpha=alpha, n=8, mute=mute))
            out.append(ruby_pipe(name, p1, b, r, color=color, alpha=alpha, n=10, mute=mute))
        else:
            out.append(ruby_pipe(name, p0, b, r, color=color, alpha=alpha, n=10, mute=mute))
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
               color=None, alpha=None, n=16, seg=8, mute=0.0):
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
        # followme leaves the arc CENTERLINE behind as loose edges (no face) — they render as stray
        # dashed/"perspective" lines all over the model. Drop them (they're inside the swept tube).
        '  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }',
    ]
    if color:
        color = mute_hex(color, mute)
        rr, gg, bb = hex_to_rgb(color)
        mat_nm = shared_mat_name(name, color, alpha)
        out.append(f'  mat = model.materials["{mat_nm}"] || model.materials.add("{mat_nm}")')
        out.append(f'  mat.color = Sketchup::Color.new({rr}, {gg}, {bb})')
        out.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        out.append('  grp.material = mat')
    out.append('')
    return '\n'.join(out)


def ruby_pipe_run(name, waypoints, r, color=None, alpha=None,
                  elbow_r=None, n=16, seg=8, mute=0.0):
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
                out.append(ruby_pipe(name, start, V[i], r, color, alpha, n, mute=mute))
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
            out.append(ruby_pipe(name, start, A, r, color, alpha, n, mute=mute))
        out.append(ruby_elbow(name + " elbow", A, O, Rc, normal, d_in, theta,
                              r, color, alpha, n, seg, mute=mute))
        start = B
    return '\n'.join(out)


def ruby_flex_run(name, waypoints, r, color=None, alpha=None,
                  elbow_r=None, n=16, seg=8, mute=0.0):
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
                out.append(ruby_flex_duct(name, start, V[i], r, color, alpha, mute=mute))
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
            out.append(ruby_flex_duct(name, start, A, r, color, alpha, mute=mute))
        out.append(ruby_elbow(name + " elbow", A, O, Rc, normal, d_in, theta,
                              r, color, alpha, n, seg, mute=mute))
        start = B
    return '\n'.join(out)


def ruby_tee(name, node, run_dir, branch_dir, r, color=None, alpha=None, n=16, mute=0.0):
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
    return '\n'.join([ruby_pipe(name, a, b, rt, color, alpha, n, mute=mute),
                      ruby_pipe(name, node, c, rt, color, alpha, n, mute=mute)])



# ── Assemble full Ruby script ────────────────────────────────────────────────

def generate_ruby():
    """Build the complete Ruby script for the Overview model."""
    # Reuse the CURRENT water-system builders (water.skp source) so overview stays in
    # sync with the corridor + pinhole-wall panel design (late import — cp/pw import ov).
    import generate_corridor_water_panel as cp
    import generate_pinhole_water_panel as pw
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
        component("Corridor Frame (deep box)", "IBC Rack", cp.frame()),
        component("IBC Tote Restraint", "IBC Rack", cp.tote_restraint()),
        component("Corridor Rear Panel", "Plumbing Panel", cp.rear_panel()),
        component("Corridor Equipment", "Plumbing Panel", cp.equipment()),
        component("Pinhole-Wall Kit", "Plumbing Panel", pw.kit()),
        component("IBC Stack", "IBC Stack", ibc_stack()),
        component("Light-Trap Drum", "Light Trap", light_trap_drum()),
        component("Light-Trap Bay", "Light Trap", light_trap_bay()),
        component("Electrical", "Electrical", electrical()),
        component("EP External Wiring (PV + E-stop)", "EP Ext Wiring", ep_external_wiring()),
        component("Corridor Pump Wiring (Cct C)", "Lighting", pw.panel_power(include_switch=False)),
        component("Solar Array", "Solar Array", solar_array()),
        component("Chemistry Shelf", "Shelf", shelf()),
        component("Light-Trap Door Frame", "Light Seal", light_trap_frame()),
        component("Light Seal & Hinges", "Light Seal", light_seal()),
        component("Lighting & Wiring", "Lighting", lighting_wiring()),
        component("Fan Wiring", "Fan Wiring", fan_wiring()),
        component("Evap Cooler & Duct", "Evap Cooler", evap_cooler()),
        component("Corridor Drains + X-ports", "Water Hookups", cp.drains_ports()),
        component("Fans A & B", "Fans", fans()),
        component("TAP-01 + Spray Supply", "Spray Bar", pw.tap01_supply()),
        component("Corridor Plumbing", "Water Plumbing", cp.plumbing()),
        component("Ribbon Support Cross-beams", "Water Plumbing", cp.ribbon_supports()),
    ]
    body = '\n'.join(comps)

    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)

    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    # Grouped scenes — related subsystems together (Shell shown as context).
    scene_groups = [
        ("Film Plane & Pinhole", ["Pinhole", "Optical Cone", "Film Plane", "Combined Plate"]),
        ("Water Systems", ["Processing Tray", "Spray Bar", "Plumbing Panel",
                           "IBC Stack", "IBC Rack", "Shelf", "Water Hookups",
                           "Water Plumbing"]),
        ("Electrical Systems", ["Electrical", "Lighting", "Solar Array", "Fan Wiring", "EP Ext Wiring"]),
        ("Hinge Panel & Drum", ["Light Trap", "Light Seal", "Pivot Axle"]),
        ("Ventilation", ["Evap Cooler", "Fans", "Electrical", "Fan Wiring"]),
        ("Walkways", ["Walkways", "Combined Plate"]),
    ]
    scene_groups_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags))
        for n, tags in scene_groups) + ']'

    sf_meta = sketchfab_meta_ruby(
        "TBS-001 Overview",
        "A fully operational pinhole camera built inside a standard 20-foot ISO shipping "
        "container. It makes photographs — real, large-format photographs — on contact-scale "
        "cyanotype prints measuring approximately 15 feet wide by 8 feet tall. It is transportable, "
        "deployable in remote locations, and self-sufficient for water and processing. It is not an "
        "installation that resembles a camera. It is a camera.",
        "e624e210bf3d4de08b1a7b7261a66c45", "sketchup")

    return f'''# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
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

{sf_meta}
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

# Overview — everything visible, Labels OFF; listed first.
model.layers["Labels"].visible = false if model.layers["Labels"]
ovp = model.pages.add("Overview"); ovp.use_camera = true

# Grouped scenes — translucent Shell (context) + the group's subsystems.
{scene_groups_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == default_layer || l.name == "Shell" || tags.include?(l.name)) }}
  page = model.pages.add(name)
  page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}

# Labeled — Overview view + callouts on the major system components, listed LAST.
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents
model.layers["Labels"].visible = true if model.layers["Labels"]
olp = model.pages.add("Labeled"); olp.use_camera = true
model.layers["Labels"].visible = false if model.layers["Labels"]

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
