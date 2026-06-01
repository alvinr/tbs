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
    """Convert mm to inches (SketchUp default unit)."""
    return val / 25.4


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
    xi, yi, zi = mm(x), mm(y), mm(z)
    wi, di, hi = mm(w), mm(d), mm(h)

    lines = [
        f'  # {name}',
        f'  grp = entities.add_group',
        f'  grp.name = "{name}"',
        f'  face = grp.entities.add_face('
        f'[{xi},{yi},{zi}], [{xi+wi},{yi},{zi}], '
        f'[{xi+wi},{yi+di},{zi}], [{xi},{yi+di},{zi}])',
        f'  face.reverse! if face.normal.z < 0',
        f'  face.pushpull({hi})',
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
    args = parser.parse_args()

    ruby = generate_ruby()

    if args.save:
        out = os.path.join(os.path.dirname(__file__), "tbs_model.rb")
        with open(out, "w") as f:
            f.write(ruby)
        print(f"  {out} saved ({len(ruby)} bytes)")
    else:
        print(ruby)
