#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_sketchup_model.py — Generate Ruby code for TBS-001 SketchUp 3D model.

Reads spatial constants from tbs_constants.py and builds Ruby code strings
that create the 3D model via the SketchUp MCP plugin (eval_ruby).

Phase 1: Container shell + walkways + processing tray.

Usage
-----
    python3 src/models/generate_sketchup_model.py          # print Ruby to stdout
    python3 src/models/generate_sketchup_model.py --save   # write to src/models/tbs_model.rb
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
)


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
    """Generate Ruby code to create a named box group.

    Parameters are in mm — converted to inches internally.
    x, y, z: origin corner (min X, min Yd, min Z).
    w, d, h: width (X), depth (Yd), height (Z).
    """
    # Sum in millimeters first, then render each corner with the `.mm` suffix.
    x0, y0, z0 = mm(x), mm(y), mm(z)
    x1, y1 = mm(x + w), mm(y + d)
    h_mm = mm(h)

    lines = [
        f'  # {name}',
        f'  grp = entities.add_group',
        f'  grp.name = "{name}"',
        f'  face = grp.entities.add_face('
        f'[{x0},{y0},{z0}], [{x1},{y0},{z0}], '
        f'[{x1},{y1},{z0}], [{x0},{y1},{z0}])',
        f'  face.reverse! if face.normal.z < 0',
        f'  face.pushpull({h_mm})',
    ]

    if color:
        r, g, b = hex_to_rgb(color)
        lines.append(f'  mat = model.materials.add("{name}")')
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

    parts.append(ruby_box("Container Ceiling",
                           0, 0, C_HGT,
                           C_LEN, C_WID, WALL_T,
                           color=C_WALL))

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


# ── Assemble full Ruby script ────────────────────────────────────────────────

def generate_ruby():
    """Build the complete Ruby script for Phase 1."""
    sections = [
        container_shell(),
        processing_tray(),
        walkways(),
    ]

    body = '\n'.join(sections)

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Phase 1", true)
entities = model.active_entities

# Display in millimeters (LengthUnit 2 = mm, LengthFormat 0 = decimal).
# SketchUp stores geometry in inches internally; this only sets the UI readout.
opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

{body}

model.commit_operation
Sketchup.active_model.active_view.zoom_extents
{{ success: true, phase: "Phase 1 — Container + Walkways + Tray" }}.to_json
'''


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Ruby code for TBS-001 SketchUp model")
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
