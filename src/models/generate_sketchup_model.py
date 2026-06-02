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
)

# Material colors used only by the 3D model (not in tbs_constants).
C_STEEL = "#B0B0B8"     # steel sections (rails, mount plate)
C_FILM = "#2060A0"      # film plane / muslin screen
C_PINHOLE = "#CC6600"   # pinhole aperture + optical axis

# Subsystem → tag map (also drives tag creation order).
TAGS = ["Shell", "Walkways", "Processing Tray",
        "Pinhole", "Optical Axis", "Film Plane"]


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
    """Four perimeter walkway sections as flat plates at deck height."""
    grate_z = WALKWAY_H - WALKWAY_GRATE_T
    t = WALKWAY_GRATE_T
    color = "#808080"

    near_x_l = WALKWAY_LEFT_X + WALKWAY_W
    near_x_r = WALKWAY_RIGHT_X
    near_len = near_x_r - near_x_l

    parts = []

    # Near walkway — standard width section (left of widened)
    if WALKWAY_NEAR_WIDE_X_L > near_x_l:
        seg_len = WALKWAY_NEAR_WIDE_X_L - near_x_l
        parts.append(ruby_box("Walkway Near (left section)",
                              near_x_l, 0, grate_z,
                              seg_len, WALKWAY_W, t,
                              color=color))

    # Near walkway — widened section
    wide_len = WALKWAY_NEAR_WIDE_X_R - WALKWAY_NEAR_WIDE_X_L
    parts.append(ruby_box("Walkway Near (widened)",
                          WALKWAY_NEAR_WIDE_X_L, 0, grate_z,
                          wide_len, WALKWAY_NEAR_WIDE_W, t,
                          color=color))

    # Near walkway — standard width section (right of widened)
    if WALKWAY_NEAR_WIDE_X_R < near_x_r:
        seg_len = near_x_r - WALKWAY_NEAR_WIDE_X_R
        parts.append(ruby_box("Walkway Near (right section)",
                              WALKWAY_NEAR_WIDE_X_R, 0, grate_z,
                              seg_len, WALKWAY_W, t,
                              color=color))

    # Far walkway
    parts.append(ruby_box("Walkway Far",
                          near_x_l, WALKWAY_FAR_YD, grate_z,
                          near_len, WALKWAY_W, t,
                          color=color))

    # Right walkway (IBC end)
    parts.append(ruby_box("Walkway Right (IBC end)",
                          WALKWAY_RIGHT_X, 0, grate_z,
                          WALKWAY_RIGHT_W, C_WID, t,
                          color=color))

    # Left walkway (cargo door end)
    parts.append(ruby_box("Walkway Left (cargo door)",
                          WALKWAY_LEFT_X, 0, grate_z,
                          WALKWAY_W, C_WID, t,
                          color=color))

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


# ── Optical axis ─────────────────────────────────────────────────────────────

def optical_axis():
    """Thin tube marking the optical axis: pinhole (Yd=0) → film plane (Yd=FP_Y)."""
    s = 6  # 6mm square tube — visible without dominating
    return ruby_box("Optical Axis (pinhole → film plane)",
                    PH_X - s / 2, 0, PH_H - s / 2,
                    s, FP_Y, s,
                    color=C_PINHOLE)


# ── Film plane mechanism ─────────────────────────────────────────────────────

def film_plane_mechanism():
    """Four corner rails (Y travel) + a framed translucent muslin screen.

    Rails run in +Y (depth) from the minimum carriage depth, at the four
    corners (left/right rail X, floor/ceiling offset RAIL_OFF). The muslin
    screen sits at the nominal depth FP_Y with a 2" steel angle frame.
    """
    parts = []
    rail = 40                       # 40×40mm rail tube
    z_bot = RAIL_OFF                # 100mm off the floor
    z_top = C_HGT - RAIL_OFF - rail # 100mm off the ceiling
    x_left = RAIL_X_L               # 150
    x_right = RAIL_X_R - rail       # 4609
    y0 = FP_Y_MIN                   # rails start at min carriage depth

    for rx, rz, nm in [(x_left, z_bot, "BL"), (x_right, z_bot, "BR"),
                       (x_left, z_top, "TL"), (x_right, z_top, "TR")]:
        parts.append(ruby_box(f"FP Rail {nm}",
                              rx, y0, rz,
                              rail, RAIL_LEN, rail,
                              color=C_STEEL))

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


# ── Assemble full Ruby script ────────────────────────────────────────────────

def generate_ruby():
    """Build the complete Ruby script for the Overview model."""
    comps = [
        component("Container Shell", "Shell", container_shell()),
        component("Walkways", "Walkways", walkways()),
        component("Processing Tray", "Processing Tray", processing_tray()),
        component("Pinhole Assembly", "Pinhole", pinhole_assembly()),
        component("Optical Axis", "Optical Axis", optical_axis()),
        component("Film Plane Mechanism", "Film Plane", film_plane_mechanism()),
    ]
    body = '\n'.join(comps)

    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)

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

# ── Subsystems (each a component on its tag) ──
{body}

model.definitions.purge_unused
model.materials.purge_unused

# ── Scenes ──
model.layers.each {{ |l| l.visible = true }}
model.pages.add("Overview")

# Optical Core: hide circulation/processing, keep shell + optical train.
["Walkways", "Processing Tray"].each {{ |n| model.layers[n].visible = false }}
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
        out = os.path.join(os.path.dirname(__file__), "tbs_model.rb")
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
