#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_lighttrap_model.py — Generate Ruby for the TBS-001 "Light Trap"
focus model (models/lighttrap.skp).

A detailed, report-accurate model of the cargo-door end assembly only:
  - the revolving light-trap DRUM (caps, stub shafts, SKF bearings, grab rail),
  - the hinged stepped PANEL (3 zones + drum aperture + EPDM seal + hinges +
    cam latches),
  - the SLIDING carriage system (HGR20 ceiling rails, HGH20CA blocks,
    suspension brackets, left carriage beam, Destaco toggle clamps, fixed RHS
    door frame),
  - Fan B (intake) mounted on the panel — reused from the Overview's shared
    fan_duct() builder so it stays in sync.

Geometry comes from hinged-panel-report.md, ceiling-rail-report.md and
light-trap-selection.md. Helpers, materials and spatial constants are imported
from generate_sketchup_model (`ov`) — single source of truth.

Usage
-----
    python3 src/models/generate_lighttrap_model.py           # print Ruby
    python3 src/models/generate_lighttrap_model.py --save     # write lighttrap.rb
    python3 src/models/generate_lighttrap_model.py --send     # push to SketchUp
    python3 src/models/generate_lighttrap_model.py --send --skp   # + save .skp
"""

import os
import sys
import math
import argparse

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov   # helpers, materials, constants

# ── pull in shared helpers + constants ───────────────────────────────────────
ruby_box, ruby_cylinder = ov.ruby_box, ov.ruby_cylinder
component = ov.component
C_WID, C_HGT, WALL_T = ov.C_WID, ov.C_HGT, ov.WALL_T
DRUM_CX, DRUM_CY, DRUM_R, DRUM_H = ov.DRUM_CX, ov.DRUM_CY, ov.DRUM_R, ov.DRUM_H_LT
PANEL_CENTER_T = ov.PANEL_CENTER_T            # 120 — center-zone thickness (X)
PANEL_CORNER_T = 40                           # corner-zone thickness (report §2.1)
PANEL_FLOOR_GAP = ov.PANEL_FLOOR_GAP          # 80
YD_L, YD_R = ov.PANEL_CORNER_YD_L, ov.PANEL_CORNER_YD_R   # 653, 1709 step lines
FAN_B_YD, FAN_B_H = ov.FAN_B_YD, ov.FAN_B_H

C_STEEL, C_ALUM, C_PLY = ov.C_STEEL, ov.C_ALUM, ov.C_PLY
C_DRUM, C_GASKT, C_RAIL, C_CARR = ov.C_DRUM, ov.C_GASKT, ov.C_RAIL, ov.C_CARR
C_SHELL, C_VALVE = ov.C_SHELL, ov.C_VALVE

PANEL_Z_BOT = PANEL_FLOOR_GAP                 # 80 — bottom edge (floor gap)
PANEL_Z_TOP = 2300                            # hung from ceiling rail (rail above)

# ── Option A — housed revolving-door light lock (Ø900 balanced) ───────────────
# Fixed housing with two opposed 80° openings (exterior + interior-onto-walkway,
# 180° apart) + a single-opening C-shell drum rotating inside. Openings <90° so
# the drum opening can never bridge both at once → light-tight at all rotations.
# All dimensions come from tbs_constants (via ov) — single source of truth.
HOUSING_R = ov.LT_HOUSING_R           # 450 — fixed housing radius (Ø900 OD)
HOUSING_T = ov.LT_HOUSING_T           # 3 — housing wall
DRUM_OR = ov.LT_DRUM_OR               # 432 — drum outer radius (Ø864), 15mm gap
DRUM_T = ov.LT_DRUM_T                 # 3 — drum wall → ~Ø850 bore, ~555mm passage
OPENING_DEG = ov.LT_OPENING_DEG       # 80 — each opening arc (<90°)
APERTURE_R = HOUSING_R + 18           # 468 — panel aperture radius around housing
NEW_YD_L = YD_L                       # 653 — widened center-zone step lines
NEW_YD_R = YD_R                       # 1709  (PANEL_CORNER_YD_L/R from constants)
APER_L = DRUM_CY - APERTURE_R         # 713 — aperture edge (near)
APER_R = DRUM_CY + APERTURE_R         # 1649 — aperture edge (far)

TAGS = ["Context", "Door Frame", "Hinge Panel", "Light Trap",
        "Sliding Carriage", "Fan B"]


# ── Ghosted container context (end opening only) ─────────────────────────────

def context():
    """Low-alpha stub of floor, ceiling and both side walls near X=0 so the
    assembly reads in place without modeling the whole container."""
    x0, xlen = -400, 2000
    return '\n'.join([
        ruby_box("Floor (context)", x0, 0, -WALL_T, xlen, C_WID, WALL_T,
                 color=C_SHELL, alpha=0.25),
        ruby_box("Ceiling (context)", x0, 0, C_HGT, xlen, C_WID, WALL_T,
                 color=C_SHELL, alpha=0.10),
        ruby_box("Side Wall near (context)", x0, -WALL_T, 0, xlen, WALL_T, C_HGT,
                 color=C_SHELL, alpha=0.16),
        ruby_box("Side Wall far (context)", x0, C_WID, 0, xlen, WALL_T, C_HGT,
                 color=C_SHELL, alpha=0.16),
        # Ghosted left walkway (the surface the operator steps onto from the
        # drum's interior opening): grating deck at X 170–470, Z 65–80, spanning
        # the full container width to match the ghost-container footprint.
        ruby_box("Left walkway (ghost)", ov.WALKWAY_LEFT_X,
                 0, ov.WALKWAY_H - ov.WALKWAY_GRATE_T,
                 ov.WALKWAY_W, C_WID, ov.WALKWAY_GRATE_T,
                 color="#808080", alpha=0.28),
        # Drum-exit PUNCH-OUT — deepened landing in front of the drum opening so
        # the operator has somewhere to step out (the 300mm deck leaves only 20mm).
        ruby_box("Left walkway punch-out (ghost)",
                 ov.WALKWAY_LEFT_X + ov.WALKWAY_W, ov.WALKWAY_LEFT_WIDE_YD_L,
                 ov.WALKWAY_H - ov.WALKWAY_GRATE_T,
                 ov.WALKWAY_LEFT_WIDE_W - ov.WALKWAY_W,
                 ov.WALKWAY_LEFT_WIDE_YD_R - ov.WALKWAY_LEFT_WIDE_YD_L,
                 ov.WALKWAY_GRATE_T, color="#808080", alpha=0.34),
    ])


# ── Fixed RHS door frame (seal landing, X just outboard of the panel) ────────

def door_frame():
    """50×50×3 RHS welded frame lining the cargo-door opening at X≈0. Sits
    just exterior of the panel (X=-50..0); the EPDM gasket seals against it."""
    s = 50
    x0 = -s
    # threshold rail runs full width — the suspended drum no longer reaches the
    # floor, so the doorway sill needs no notch.
    parts = [
        ruby_box("Door Frame threshold", x0, 0, 0, s, C_WID, s, color=C_RAIL),
        ruby_box("Door Frame top", x0, 0, C_HGT - s, s, C_WID, s, color=C_RAIL),
        ruby_box("Door Frame left stile", x0, 0, 0, s, s, C_HGT, color=C_RAIL),
        ruby_box("Door Frame right stile", x0, C_WID - s, 0, s, s, C_HGT,
                 color=C_RAIL),
    ]
    # Bottom seal lip — an upstand rising from the threshold to just above the
    # panel bottom edge (Z=110), exterior of the EPDM (X=-32..-20). It closes the
    # 80mm floor gap as a continuous wall; the panel bottom edge recedes behind it
    # and the EPDM bottom seal compresses against it when the cam latches engage
    # (operational only — release to slide to transport). Now that the drum is
    # SUSPENDED (its bottom hangs at Z=80, not on the floor), the floor gap is
    # uniform full-width, so this lip runs CONTINUOUS with no notch — like the top.
    lt, lz = 12, 110
    parts.append(ruby_box("Door Frame bottom seal lip", -20 - lt, 0, 0,
                          lt, C_WID, lz, color=C_RAIL))
    # Top seal lip — the mirror of the bottom: a downstand from the frame top
    # rail to just below the panel top edge (Z=2270), exterior of the EPDM. It
    # closes the gap between the panel top and the frame as a continuous wall;
    # the panel top edge recedes behind it and the EPDM top seal compresses
    # against it under the upper cam latches. The drum doesn't reach the top
    # (its shaft stops below the lip), so this lip runs the FULL width as one
    # continuous member — no notch — and meets across the center.
    tz0 = PANEL_Z_TOP - 30                 # 2270 — lip reaches 30mm past panel top
    th = C_HGT - tz0                       # up to the frame top / ceiling
    parts.append(ruby_box("Door Frame top seal lip", -20 - lt, 0, tz0,
                          lt, C_WID, th, color=C_RAIL))
    return '\n'.join(parts)


# ── Hinged stepped panel (3 zones, drum aperture, seal, hinges, latches) ─────

def hinge_panel():
    h = PANEL_Z_TOP - PANEL_Z_BOT                  # panel skin height
    tc, tk = PANEL_CORNER_T, PANEL_CENTER_T        # 40 corner, 120 center
    parts = []

    # Near corner (hinge side) and far corner (Fan B side) — flush 40mm zones.
    # The center zone is WIDENED (step lines at NEW_YD_L/R) to frame the Ø900 housing.
    parts.append(ruby_box("Panel near corner (40mm)",
                          0, 0, PANEL_Z_BOT, tc, NEW_YD_L, h, color=C_PLY))
    parts.append(ruby_box("Panel far corner (40mm)",
                          0, NEW_YD_R, PANEL_Z_BOT, tc, C_WID - NEW_YD_R, h, color=C_PLY))

    # Center zone (120mm) framed around the housing aperture: two jambs + header.
    parts.append(ruby_box("Panel center jamb L (120mm)",
                          0, NEW_YD_L, PANEL_Z_BOT, tk, APER_L - NEW_YD_L, h, color=C_PLY))
    parts.append(ruby_box("Panel center jamb R (120mm)",
                          0, APER_R, PANEL_Z_BOT, tk, NEW_YD_R - APER_R, h, color=C_PLY))
    parts.append(ruby_box("Panel header over housing (120mm)",
                          0, NEW_YD_L, DRUM_H, tk, NEW_YD_R - NEW_YD_L,
                          PANEL_Z_TOP - DRUM_H, color=C_PLY))

    # 20mm neoprene compression strip lining the housing aperture (jamb inner faces).
    parts.append(ruby_box("Housing aperture seal L", 0, APER_L, PANEL_Z_BOT,
                          tk, 20, DRUM_H, color=C_GASKT))
    parts.append(ruby_box("Housing aperture seal R", 0, APER_R - 20, PANEL_Z_BOT,
                          tk, 20, DRUM_H, color=C_GASKT))

    # EPDM perimeter gasket — 20mm strips on the panel exterior face, compressed
    # against the door frame (and the top/bottom seal lips) by the cam latches.
    gw, gt = 40, 20
    z0, z1 = PANEL_Z_BOT, PANEL_Z_TOP
    dg0, dg1 = DRUM_CY - HOUSING_R - 15, DRUM_CY + HOUSING_R + 15  # clear housing aperture
    # bottom + top strips run on the panel edges, notched around the housing
    parts.append(ruby_box("EPDM seal bottom L", -gt, 0, z0, gt, dg0, gw, color=C_GASKT))
    parts.append(ruby_box("EPDM seal bottom R", -gt, dg1, z0, gt, C_WID - dg1, gw,
                          color=C_GASKT))
    # top strip runs continuously full-width (panel top edge is the solid header)
    parts.append(ruby_box("EPDM seal top", -gt, 0, z1 - gw, gt, C_WID, gw, color=C_GASKT))
    parts.append(ruby_box("EPDM seal left", -gt, 0, z0, gt, gw, z1 - z0, color=C_GASKT))
    parts.append(ruby_box("EPDM seal right", -gt, C_WID - gw, z0, gt, gw, z1 - z0,
                          color=C_GASKT))

    # 3 × 200mm SS piano hinges on the left edge (Yd=0), exterior, per report §4.1.
    hd, hw, hh = 60, 30, 200
    for hz in (220, 1190, 2158):
        parts.append(ruby_box("Piano hinge", -hd / 2, 0, hz, hd, hw, hh, color=C_STEEL))

    # 4 × Southco cam latches — interior face, corners (report §4.2).
    lw, ld, lh = 55, 70, 50
    for ly in (210, C_WID - 210):
        for lz in (220, 2168):
            parts.append(ruby_box("Southco cam latch", tc, ly - ld / 2, lz - lh / 2,
                                  lw, ld, lh, color=C_VALVE))
    return '\n'.join(parts)


# ── Revolving light-trap drum (detailed) ─────────────────────────────────────

def drum():
    """Option A — housed revolving-door light lock (Ø900 balanced).

    A FIXED housing with two opposed 80° openings — one facing the exterior
    (cargo-door side), one facing the interior/walkway, 180° apart — and a
    single-opening C-shell DRUM rotating inside it on SKF 6215 bearings. NO
    internal fins. Light-tight by geometry: the housing's solid wall always
    covers whichever opening the drum opening is not aligned with, so there is
    no straight path at any rotation (verified in the top-down renders). Shown at
    the ENTER position (drum opening at the exterior). ~Ø850 bore, ~555mm
    passage (sideways entry); emergency egress is the whole panel swinging open."""
    cx, cy, H = DRUM_CX, DRUM_CY, DRUM_H
    ZB = PANEL_Z_BOT                 # 80 — housing/drum SUSPENDED with the panel
    od = OPENING_DEG                 # (80mm floor gap → clears the tray rim in transport)
    parts = []

    # Fixed HOUSING — two solid arcs (each 180−od = 100° wide) leaving two od=80°
    # openings centered on +X (interior→walkway, 0°) and −X (exterior, 180°).
    # Suspended: spans Z 80..2200 (bottom hangs at the panel bottom rail).
    parts.append(ov.ruby_arc_wall("LT Housing arc (near Yd)", cx, cy, HOUSING_R,
                                  HOUSING_T, H - ZB, gap_center_deg=270, gap_deg=180 + od,
                                  color=C_ALUM, alpha=0.42, z0=ZB))  # rev8.1 aluminum
    parts.append(ov.ruby_arc_wall("LT Housing arc (far Yd)", cx, cy, HOUSING_R,
                                  HOUSING_T, H - ZB, gap_center_deg=90, gap_deg=180 + od,
                                  color=C_ALUM, alpha=0.42, z0=ZB))  # rev8.1 aluminum

    # Rotating DRUM — single od=80° opening (C-shell). ENTER position: opening at
    # the exterior (180°); the solid 280° arc faces the interior (0°).
    parts.append(ov.ruby_arc_wall("LT Drum C-shell", cx, cy, DRUM_OR, DRUM_T, H - ZB,
                                  gap_center_deg=180, gap_deg=od,
                                  color=C_ALUM, alpha=0.85, z0=ZB))  # rev8.1 aluminum drum

    # Drum caps (top at 2200, bottom at the suspended Z=80), top stub shaft +
    # upper SKF 6215 bearing, lower bearing collar on the panel bottom rail (Z=80).
    parts.append(ruby_cylinder("LT Drum top cap", cx, cy, H - 5, DRUM_OR, 5,
                               color=C_ALUM, axis="z"))
    parts.append(ruby_cylinder("LT Drum bottom cap", cx, cy, ZB, DRUM_OR, 5,
                               color=C_ALUM, axis="z"))
    parts.append(ruby_cylinder("LT Drum top shaft", cx, cy, H, 37.5, 65,
                               color=C_STEEL, axis="z"))
    parts.append(ruby_cylinder("LT Upper bearing (SKF 6215)", cx, cy, H, 65, 45,
                               color=C_STEEL, axis="z"))
    parts.append(ruby_cylinder("LT Lower bearing collar", cx, cy, ZB, 75, 45,
                               color=C_STEEL, axis="z"))
    parts.append(ruby_box("LT Lower bearing mount plate", cx - 120, cy - 120, ZB,
                          240, 240, 12, color=C_STEEL))

    # Interior grab rail on the drum's solid +X wall (operator pulls the drum).
    inner = cx + DRUM_OR - DRUM_T
    gx = cx + DRUM_OR - 75
    parts.append(ruby_cylinder("LT Grab rail", gx, cy, 700, 15, 400,
                               color=C_STEEL, axis="z"))
    for bz in (720, 1080):
        parts.append(ruby_box("LT Grab rail standoff", gx, cy - 6, bz,
                              inner - gx, 12, 12, color=C_STEEL))

    # ── Rotating drum↔housing light seal ──────────────────────────────────────
    # Felt/brush wiper strips on the two vertical edges of the drum opening sweep
    # against the housing inner wall as the drum turns, blocking light leaking
    # around the opening; top + bottom felt wiper rings close the annular gap.
    felt = "#7E7E76"
    seal_r = (DRUM_OR + HOUSING_R - HOUSING_T) / 2          # mid of running gap
    for edge in (180 - od / 2, 180 + od / 2):               # opening edges (enter pos.)
        bx = cx + seal_r * math.cos(math.radians(edge))
        by = cy + seal_r * math.sin(math.radians(edge))
        parts.append(ruby_cylinder("LT Drum opening brush seal", bx, by, ZB, 7, H - ZB,
                                   color=felt, axis="z"))
    parts.append(ruby_cylinder("LT Drum top felt seal", cx, cy, H - 8,
                               HOUSING_R - HOUSING_T - 1, 8, color=felt, axis="z"))
    parts.append(ruby_cylinder("LT Drum bottom felt seal", cx, cy, ZB,
                               HOUSING_R - HOUSING_T - 1, 8, color=felt, axis="z"))
    return '\n'.join(parts)


# ── Sliding carriage system (transport-mode slide) ──────────────────────────
# Slide travel LENGTHENED to ~500mm so the deeper Ø900 housing (exterior overhang
# ~450mm) fully retracts behind the door closure plane for transport. Rails at the
# widened center-zone step lines (NEW_YD_L/R). NB: the longer retraction carries
# the housing into the left-walkway / near-tray zone — tray-end clearance during
# transport is an open detail to confirm.
TRANSPORT_SLIDE = ov.PANEL_SLIDE        # 550 — from constants

def sliding_carriage():
    """HGR20 ceiling rails + HGH20CA blocks + suspension brackets + left
    carriage beam + Destaco toggle clamps (operational & transport locks)."""
    parts = []
    rail_x0, rail_len = -30, 760                    # allows the ~500mm transport slide
    rail_w, rail_h = 20, 30
    rail_z = C_HGT - rail_h                          # 2358 — hung from ceiling
    carr_w, carr_d, carr_h = 44, 44, 28
    brk_w, brk_d, brk_h = 60, 40, 30

    for yd, nm in [(NEW_YD_L, "L"), (NEW_YD_R, "R")]:
        parts.append(ruby_box(f"HGR20 rail {nm}", rail_x0, yd - rail_w / 2, rail_z,
                              rail_len, rail_w, rail_h, color=C_RAIL))
        parts.append(ruby_box(f"HGH20CA carriage {nm}", 18, yd - carr_d / 2,
                              rail_z - carr_h, carr_w, carr_d, carr_h, color=C_CARR))
        parts.append(ruby_box(f"Suspension bracket {nm}", 15, yd - brk_d / 2,
                              PANEL_Z_TOP, brk_w, brk_d, rail_z - carr_h - PANEL_Z_TOP,
                              color=C_STEEL))

    # Left-side carriage beam — vertical 60×60 SHS in the fixed-frame slot.
    parts.append(ruby_box("Left carriage beam (60×60 SHS)", 0, 0, PANEL_Z_BOT,
                          60, 60, PANEL_Z_TOP - PANEL_Z_BOT, color=C_STEEL))

    # Destaco 207-U toggle clamps — operational lock (X≈0) + transport lock (X≈500).
    for cx, lock in [(-10, "operational"), (TRANSPORT_SLIDE - 10, "transport")]:
        for yd in (NEW_YD_L, NEW_YD_R):
            parts.append(ruby_box(f"Destaco clamp ({lock}) base", cx, yd - 18,
                                  rail_z - 70, 60, 36, 24, color=C_STEEL))
            parts.append(ruby_box(f"Destaco clamp ({lock}) handle", cx + 10, yd - 6,
                                  rail_z - 46, 70, 12, 12, color=C_CARR))
    return '\n'.join(parts)


# ── Fan B on the hinge panel (reused from Overview's shared builder) ─────────

def fan_b():
    return '\n'.join(ov.fan_duct("Fan B (intake)", 0, -1, FAN_B_YD, FAN_B_H))


# ── Assemble the Ruby script ─────────────────────────────────────────────────

def generate_ruby():
    comps = [
        component("Context", "Context", context()),
        component("Fixed Door Frame", "Door Frame", door_frame()),
        component("Hinged Light-Trap Panel", "Hinge Panel", hinge_panel()),
        component("Revolving Light-Trap Drum", "Light Trap", drum()),
        component("Sliding Carriage System", "Sliding Carriage", sliding_carriage()),
        component("Fan B (intake)", "Fan B", fan_b()),
    ]
    body = '\n'.join(comps)

    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    scene_groups = [
        ("Light-Trap Drum", ["Light Trap", "Hinge Panel"]),
        ("Hinge Panel & Seal", ["Hinge Panel", "Door Frame"]),
        ("Sliding Carriage", ["Sliding Carriage", "Hinge Panel"]),
        ("Fan B", ["Fan B", "Hinge Panel"]),
    ]
    scene_groups_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags))
        for n, tags in scene_groups) + ']'

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Light Trap", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild: erase ALL prior instances (no scale figure in this model).
to_erase = entities.to_a.select {{ |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance)
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

# ── Remove stale tags from earlier generator versions ──
keep_tags = {keep_tags_ruby}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

# ── Scenes — one shared iso camera; scenes only toggle visibility ──
model.layers.each {{ |l| l.visible = true }}
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(-0.6, -0.72, 0.45); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

model.pages.add("Overview")
{scene_groups_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }}
  page = model.pages.add(name)
  page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}

model.commit_operation
{{ success: true, model: "Light Trap",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Ruby for the TBS-001 Light Trap focus model")
    parser.add_argument("--save", action="store_true",
                        help="Write Ruby to src/models/lighttrap.rb")
    parser.add_argument("--send", action="store_true",
                        help="Send the Ruby straight to the running SketchUp")
    parser.add_argument("--skp", action="store_true",
                        help="After --send, save models/lighttrap.skp")
    args = parser.parse_args()

    ruby = generate_ruby()

    if args.save:
        out = os.path.join(os.path.dirname(__file__), "lighttrap.rb")
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

    if args.skp:
        if not args.send:
            print("  --skp requires --send", file=sys.stderr)
            sys.exit(1)
        from sketchup_client import send_ruby
        skp = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           "..", "..", "models", "lighttrap.skp"))
        print(f"  saving {skp} ...")
        print("  " + send_ruby('m=Sketchup.active_model; "saved=#{m.save(' + repr(skp) + ')}"'))

    if not args.save and not args.send:
        print(ruby)
