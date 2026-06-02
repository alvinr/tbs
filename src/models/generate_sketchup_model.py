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
    WALKWAY_NEAR_WIDE_W, WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_X_R,
    C_WALL, C_PROC_ZONE,
    PH_X, PH_H, PH_D,
    FP_X_L, FP_X_R, FP_W, FP_H, FP_Y, FP_Y_MIN,
    RAIL_X_L, RAIL_X_R, RAIL_LEN, RAIL_OFF, FP_ANGLE_LEG,
    BRACE_RHS, BRACE_Z_BOT, BRACE_Z_TOP,
    BRACE_LEFT_DEMOUNT_Y0, BRACE_LEFT_DEMOUNT_Y1,
    PANEL_CENTER_T, PANEL_FLOOR_GAP,
    PANEL_CORNER_YD_L, PANEL_CORNER_YD_R,
    SPRAY_BAR_BEAM, SPRAY_BAR_Z_BOT,
    BB_OD, BB_H,
    PUMP_X, PUMP_W, PUMP_H_LO, PUMP_H_HI, PUMP_YD, PUMP_YD_SPAN,
    FSKID_X, FSKID_YD, F1_Z, F2_Z, F3_Z,
    EQPANEL_X, EQPANEL_T, EQPANEL_Z_LO, EQPANEL_Z_HI,
    EQPANEL_YD, EQPANEL_YD_SPAN,
    IBC_COL_X, IBC_W, IBC_D, IBC_H_600, IBC_PALLET_H, IBC_BOTTLE_INSET,
    BLUE_IBC_Y, BROWN_IBC_Y, IBC_FAR_Y, WASTE_IBC_Y,
    DRUM_CX, DRUM_CY, DRUM_R, DRUM_H_LT,
    EP_X, EP_W, EP_H_LO, EP_H_HI,
    BA_X, BA_W, BA_H_LO, BA_H_HI, BA_D,
    PWR_PANEL_X, PWR_PANEL_W, PWR_PANEL_H, PWR_PANEL_Z,
    SHELF_X_L, SHELF_X_R, SHELF_W, SHELF_H, SHELF_T, SHELF_DEPTH,
    SHELF_YD_NEAR, SHELF_YD_FAR, SHELF_HANGER_D,
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

# Subsystem → tag map (also drives tag creation order).
TAGS = ["Shell", "Walkways", "Processing Tray",
        "Pinhole", "Optical Cone", "Film Plane",
        "Ceiling Rail", "Spray Bar", "Equipment Panel",
        "IBC Stack", "IBC Rack", "Light Trap", "Electrical", "Shelf"]


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


def ruby_box(name, x, y, z, w, d, h, color=None, alpha=None):
    """Generate Ruby to create a named box group inside the `ents` context.

    Parameters are in mm. x, y, z: origin corner (min X, min Yd, min Z).
    w, d, h: width (X), depth (Yd), height (Z). Boxes are added to `ents`,
    the entities collection of the enclosing component definition.
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
        lines.append(f'  mat = model.materials["{name}"] || '
                     f'model.materials.add("{name}")')
        lines.append(f'  mat.color = Sketchup::Color.new({r}, {g}, {b})')
        if alpha is not None:
            lines.append(f'  mat.alpha = {alpha}')
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


def ruby_cylinder(name, cx, cy, cz, radius, height, color=None, alpha=None, n=24):
    """Generate Ruby for a vertical cylinder (axis +Z) in `ents`.

    (cx, cy, cz): center of the base circle. radius/height in mm. Used for
    round bodies (filter housings, accumulator, light-trap drum).
    """
    lines = [
        f'  # {name}',
        f'  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  ge = grp.entities',
        f'  circle = ge.add_circle([{mm(cx)},{mm(cy)},{mm(cz)}], '
        f'[0,0,1], {mm(radius)}, {n})',
        f'  cface = ge.add_face(circle)',
        f'  cface.reverse! if cface.normal.z < 0',
        f'  cface.pushpull({mm(height)})',
    ]
    if color:
        r, g, b = hex_to_rgb(color)
        lines.append(f'  mat = model.materials["{name}"] || '
                     f'model.materials.add("{name}")')
        lines.append(f'  mat.color = Sketchup::Color.new({r}, {g}, {b})')
        if alpha is not None:
            lines.append(f'  mat.alpha = {alpha}')
        lines.append(f'  grp.material = mat')
    lines.append('')
    return '\n'.join(lines)


# ── Container shell ──────────────────────────────────────────────────────────

def container_shell():
    """Container as 5 panels (no cargo door end wall — it's the hinged panel)."""
    parts = []

    parts.append(ruby_box("Container Floor",
                          0, 0, -WALL_T,
                          C_LEN, C_WID, WALL_T,
                          color=C_WALL))

    # Ghosted ceiling — low alpha so the interior is visible from above.
    parts.append(ruby_box("Container Ceiling",
                          0, 0, C_HGT,
                          C_LEN, C_WID, WALL_T,
                          color=C_WALL, alpha=0.2))

    parts.append(ruby_box("Pinhole Wall (Yd=0)",
                          0, -WALL_T, 0,
                          C_LEN, WALL_T, C_HGT,
                          color=C_WALL))

    parts.append(ruby_box("Film Plane Wall (Yd=max)",
                          0, C_WID, 0,
                          C_LEN, WALL_T, C_HGT,
                          color=C_WALL))

    parts.append(ruby_box("Far End Wall (IBC end)",
                          C_LEN, 0, 0,
                          WALL_T, C_WID, C_HGT,
                          color=C_WALL))

    return '\n'.join(parts)


# ── Processing tray ──────────────────────────────────────────────────────────

def processing_tray():
    """Processing tray — simplified as a shallow box with rim."""
    tray_w = PROC_TRAY_X_R - PROC_TRAY_X_L
    tray_d = PROC_TRAY_YD_FAR - PROC_TRAY_YD_NEAR
    sheet_t = 2

    parts = []

    parts.append(ruby_box("Processing Tray Floor",
                          PROC_TRAY_X_L, PROC_TRAY_YD_NEAR, 0,
                          tray_w, tray_d, sheet_t,
                          color=C_PROC_ZONE, alpha=0.5))

    rim_t = 2
    parts.append(ruby_box("Tray Rim Near",
                          PROC_TRAY_X_L, PROC_TRAY_YD_NEAR, sheet_t,
                          tray_w, rim_t, PROC_TRAY_RIM - sheet_t,
                          color=C_WALL))
    parts.append(ruby_box("Tray Rim Far",
                          PROC_TRAY_X_L, PROC_TRAY_YD_FAR - rim_t, sheet_t,
                          tray_w, rim_t, PROC_TRAY_RIM - sheet_t,
                          color=C_WALL))
    parts.append(ruby_box("Tray Rim Left",
                          PROC_TRAY_X_L, PROC_TRAY_YD_NEAR, sheet_t,
                          rim_t, tray_d, PROC_TRAY_RIM - sheet_t,
                          color=C_WALL))
    parts.append(ruby_box("Tray Rim Right",
                          PROC_TRAY_X_R - rim_t, PROC_TRAY_YD_NEAR, sheet_t,
                          rim_t, tray_d, PROC_TRAY_RIM - sheet_t,
                          color=C_WALL))

    return '\n'.join(parts)


# ── Walkways ─────────────────────────────────────────────────────────────────

def walkways():
    """Perimeter walkway sections — LOWERED deck, in place for operation.

    The deck height comes from WALKWAY_H (lowered to 65mm: a 15mm grate at the
    tray-rim level), so the grating sits below the film-frame bottom (Z=100) and
    the film plane travels above the in-place walkway. The LEFT walkway (cargo-
    door side) is a removable lift-out (shown in a distinct color) — taken out
    for transport so the light-trap can slide back.
    """
    grate_z = WALKWAY_H - WALKWAY_GRATE_T   # 50mm — grate bottom at the tray rim
    t = WALKWAY_GRATE_T                      # 15mm — thin grate

    near_x_l = WALKWAY_LEFT_X + WALKWAY_W
    near_x_r = WALKWAY_RIGHT_X
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


# ── Ceiling rail (cargo-door panel suspension) ───────────────────────────────

def ceiling_rail():
    """HGR20 ceiling rails + HGH20CA carriages + brackets + suspended panel.

    Two rails run in X near the cargo-door end (X=0) at the carriage depths
    Yd=756/1606, carrying the movable end panel in its operational position.
    """
    parts = []
    rail_x0, rail_len = -30, 510          # rail spans X=-30..480
    rail_h, rail_w_yd = 30, 20
    rail_z = C_HGT - rail_h               # 2358 — hung from ceiling
    carr_w, carr_d, carr_h = 44, 44, 28
    carr_x = PANEL_CENTER_T / 2 - carr_w / 2   # 38 — centered on panel
    carr_z = rail_z - carr_h              # 2330
    brk_w, brk_d, brk_h = 60, 40, 40
    brk_x = PANEL_CENTER_T / 2 - brk_w / 2     # 30
    brk_z = carr_z - brk_h                # 2290 — panel hangs from here

    for yd, nm in [(PANEL_CORNER_YD_L, "L"), (PANEL_CORNER_YD_R, "R")]:
        parts.append(ruby_box(f"HGR20 Rail {nm}",
                              rail_x0, yd - rail_w_yd / 2, rail_z,
                              rail_len, rail_w_yd, rail_h, color=C_RAIL))
        parts.append(ruby_box(f"Carriage {nm} (HGH20CA)",
                              carr_x, yd - carr_d / 2, carr_z,
                              carr_w, carr_d, carr_h, color=C_CARR))
        parts.append(ruby_box(f"Suspension Bracket {nm}",
                              brk_x, yd - brk_d / 2, brk_z,
                              brk_w, brk_d, brk_h, color=C_STEEL))

    # Suspended cargo-door panel, operational position (X=0), floor gap 80mm.
    parts.append(ruby_box("Cargo Door Panel",
                          0, 0, PANEL_FLOOR_GAP,
                          PANEL_CENTER_T, C_WID, brk_z - PANEL_FLOOR_GAP,
                          color=C_ALUM, alpha=0.6))

    return '\n'.join(parts)


# ── Spray bar (processing-tray wash gantry) ──────────────────────────────────

def spray_bar():
    """40mm AL SHS gantry beam running along X over the tray, with end carriages.

    The beam carries the spray pipe just above the tray floor (Z=10–50) and
    travels in Yd to wash the full tray. Shown at a representative mid-tray
    travel position.
    """
    parts = []
    beam = SPRAY_BAR_BEAM               # 40mm SHS
    bx_l = PROC_TRAY_X_L + 30           # 200
    bx_r = PROC_TRAY_X_R - 30           # 4599
    bz = SPRAY_BAR_Z_BOT                # 10mm above tray floor
    yd = (PROC_TRAY_YD_NEAR + PROC_TRAY_YD_FAR) / 2   # mid-tray (travels in Yd)

    parts.append(ruby_box("Spray Bar Beam",
                          bx_l, yd - beam / 2, bz,
                          bx_r - bx_l, beam, beam, color=C_ALUM))

    # End carriages riding the tray-edge rails (Yd travel).
    cw, cd, ch = 50, 90, 55
    for ex in (bx_l, bx_r - cw):
        parts.append(ruby_box("Spray Bar Carriage",
                              ex, yd - cd / 2, bz - 5,
                              cw, cd, ch, color=C_CARR))

    return '\n'.join(parts)


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
    z_bot = PUMP_H_LO                     # 1320 — bottom pump row
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

    return '\n'.join(parts)


# ── IBC stack (4× totes, 2×2) + support rack ─────────────────────────────────

def ibc_stack():
    """Four IBC totes in a 2×2 stack: pallet base + translucent bottle each.

    Near column (Yd=30): Brown developer below, Blue #1 on top.
    Far column (Yd=1316): Waste below, Blue #2 on top. X spans 4674–5893.
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
                              color=col, alpha=0.55))
    return '\n'.join(parts)


def ibc_rack():
    """Simplified 50×50 RHS portal rack supporting the upper IBC tier.

    Corridor uprights (Yd 1046/1316) at three X stations, longitudinal spine
    beams, and cantilever platform cross-beams under the top totes at Z≈1010.
    """
    parts = []
    s = 50                              # 50×50 RHS
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

    # Cantilever platform cross-beams under both upper totes (along Yd).
    beam_len = (IBC_FAR_Y + IBC_D) - BLUE_IBC_Y
    for xs in x_stations:
        parts.append(ruby_box("Rack Platform Beam",
                              xs, BLUE_IBC_Y, beam_z, s, beam_len, s,
                              color=C_STEEL))

    return '\n'.join(parts)


# ── Film plane mechanism ─────────────────────────────────────────────────────

def film_plane_mechanism():
    """Four corner rails + demountable brace cage + framed muslin screen.

    Rails run in +Y (depth) from the minimum carriage depth, at the four
    corners. A rigid rectangular brace cage (saddle/thumbscrew portals at each
    end) ties the rails into a knock-down box. The left rail's drum-zone
    segment (Yd 806–1556) is demountable so the light-trap drum can rotate.
    The muslin screen sits at the nominal depth FP_Y with a 2" angle frame.
    """
    parts = []
    rail = 40                       # 40×40mm rail tube
    z_bot = RAIL_OFF                # 100mm off the floor
    z_top = C_HGT - RAIL_OFF - rail # 100mm off the ceiling
    x_left = RAIL_X_L               # 150
    x_right = RAIL_X_R - rail       # 4609
    y0 = FP_Y_MIN                   # rails start at min carriage depth
    y_end = y0 + RAIL_LEN           # 2300
    d0, d1 = BRACE_LEFT_DEMOUNT_Y0, BRACE_LEFT_DEMOUNT_Y1   # 806, 1556

    # Right rails — full length, fixed.
    for rz, nm in [(z_bot, "BR"), (z_top, "TR")]:
        parts.append(ruby_box(f"FP Rail {nm}",
                              x_right, y0, rz, rail, RAIL_LEN, rail,
                              color=C_STEEL))

    # Left rails — fixed / DEMOUNTABLE (drum zone) / fixed.
    for rz, nm in [(z_bot, "BL"), (z_top, "TL")]:
        parts.append(ruby_box(f"FP Rail {nm} (fixed near)",
                              x_left, y0, rz, rail, d0 - y0, rail, color=C_STEEL))
        parts.append(ruby_box(f"FP Rail {nm} (DEMOUNTABLE — drum mode)",
                              x_left, d0, rz, rail, d1 - d0, rail, color=C_DEMOUNT))
        parts.append(ruby_box(f"FP Rail {nm} (fixed far)",
                              x_left, d1, rz, rail, y_end - d1, rail, color=C_STEEL))

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
                  color=None, alpha=None, n=48):
    """Hollow curved wall (annular sector, extruded in +Z) with a gap.

    The gap (an opening of `gap_deg` centred on `gap_center_deg`) reads as a
    doorway/entry slot in the cylinder. Built as a closed band polygon (outer
    arc forward + inner arc back) then pushpulled to `height`.
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
    pts_ruby = ', '.join(f'[{mm(round(x, 2))},{mm(round(y, 2))},0]' for x, y in pts)

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
        lines.append(f'  mat = model.materials["{name}"] || '
                     f'model.materials.add("{name}")')
        lines.append(f'  mat.color = Sketchup::Color.new({r_}, {g_}, {b_})')
        if alpha is not None:
            lines.append(f'  mat.alpha = {alpha}')
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
        lines.append(f'  mat = model.materials["{name}"] || '
                     f'model.materials.add("{name}")')
        lines.append(f'  mat.color = Sketchup::Color.new({r_}, {g_}, {b_})')
        if alpha is not None:
            lines.append(f'  mat.alpha = {alpha}')
        lines.append(f'  grp.material = mat')
    lines.append('')
    return '\n'.join(lines)


def light_trap_drum():
    """Revolving light-trap drum at the cargo-door end — hollow Ø750 drum.

    Centered at (X=DRUM_CX=0, Yd=DRUM_CY=1181), Z 0–2200. Two crossed vanes (at
    ±45°) split it into 4 quadrant segments; the shell is walled on 3 segments
    and OPEN on the one segment facing −X (outside the container) — the entry.
    Half sits in the doorway (the entry/−X half protrudes out the cargo end). It
    deliberately overlaps the demountable left-rail segment — that's why that
    segment swings clear ("drum mode").
    """
    parts = []
    r, h = DRUM_R, DRUM_H_LT
    cx, cy = DRUM_CX, DRUM_CY

    # Hollow shell: open one 90° segment centred on −X (180°); walled elsewhere.
    parts.append(ruby_arc_wall("LT Drum Shell (3 segments walled)",
                               cx, cy, r, 12, h,
                               gap_center_deg=180, gap_deg=90,
                               color=C_DRUM, alpha=0.18))

    # Two crossed vanes at ±45° so the open segment (135°–225°) faces straight −X.
    vt = 6
    pa = [(cx + r * math.cos(math.radians(d)), cy + r * math.sin(math.radians(d)))
          for d in (45, 135, 225, 315)]
    parts.append(ruby_panel_z("LT Drum Vane A",
                              pa[0][0], pa[0][1], pa[2][0], pa[2][1],
                              vt, h, color=C_VANE))
    parts.append(ruby_panel_z("LT Drum Vane B",
                              pa[1][0], pa[1][1], pa[3][0], pa[3][1],
                              vt, h, color=C_VANE))

    return '\n'.join(parts)


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

    parts.append(ruby_box("Battery Bank (2x LiFePO4)",
                          BA_X, 0, BA_H_LO,
                          BA_W, BA_D, BA_H_HI - BA_H_LO, color=C_BATT))

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
        component("Ceiling Rail", "Ceiling Rail", ceiling_rail()),
        component("Spray Bar", "Spray Bar", spray_bar()),
        component("Equipment Panel", "Equipment Panel", equipment_panel()),
        component("IBC Stack", "IBC Stack", ibc_stack()),
        component("IBC Rack", "IBC Rack", ibc_rack()),
        component("Light-Trap Drum", "Light Trap", light_trap_drum()),
        component("Electrical", "Electrical", electrical()),
        component("Chemistry Shelf", "Shelf", shelf()),
    ]
    body = '\n'.join(comps)

    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)

    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

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
  (e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance)) &&
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
model.layers.each {{ |l| l.visible = true }}
model.pages.add("Overview")

# Optical Core: hide circulation/processing/structure, keep the optical train.
["Walkways", "Processing Tray", "Ceiling Rail", "Spray Bar", "Equipment Panel", "IBC Stack", "IBC Rack", "Light Trap", "Electrical", "Shelf"].each {{ |n| model.layers[n].visible = false }}
model.pages.add("Optical Core")
model.layers.each {{ |l| l.visible = true }}

model.commit_operation
Sketchup.active_model.active_view.zoom_extents
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

    if not args.save and not args.send:
        print(ruby)
