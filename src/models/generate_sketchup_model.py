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
from tbs_constants import C_LEN, C_WID, C_HGT, WALL_T, PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR, PROC_TRAY_RIM, PROC_TRAY_FLOOR_Z_LOW, tray_floor_z, WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T, WALKWAY_FAR_YD, WALKWAY_RIGHT_X, WALKWAY_RIGHT_W, WALKWAY_LEFT_X, WALKWAY_BRACKET_T, WALKWAY_BRACKET_H, CONTAINER_RIB_SPACING, WALKWAY_NEAR_WIDE_W, WALKWAY_NEAR_WIDE_X_L, WALKWAY_NEAR_WIDE_X_R, WALKWAY_LEFT_WIDE_W, WALKWAY_LEFT_WIDE_YD_L, WALKWAY_LEFT_WIDE_YD_R, PH_X, PH_H, PH_D, FP_X_L, FP_X_R, FP_H, FP_Y, RAIL_X_R, RAIL_OFF_BOT, FP_RAIL_WEB, FP_RAIL_FLANGE, FP_RAIL_BUILD_BOT, FP_RAIL_GUIDE_GAP, FP_RAIL_ZC_BOT, FP_RAIL_ZC_TOP, FP_FILM_TOP, BAY_FRONT_X, BAY_WALL_T, PANEL_CENTER_T, PANEL_CORNER_T, PANEL_FLOOR_GAP, PANEL_FAN_BAND_Z, PANEL_CORNER_YD_L, PANEL_CORNER_YD_R, PIVOT_X, PIVOT_YD, SWING_LOCK_DEG, PANEL_CUT_YD, FAR_STRIP_YD0, PIVOT_POST_OD, DRUM_CAGE_X0, DRUM_CAGE_X1, DRUM_CAGE_YD_L, DRUM_CAGE_YD_R, WALKWAY_NEAR_LIFTOUT_X_R, BB_OD, BB_H, EQPANEL_T, IBC_COL_X, IBC_H_1000, IBC_PALLET_H, BLUE_IBC_Y, IBC_FRAME_RHS, IBC_FRONT_BAR_D, IBC_FOOT_PLATE, IBC_FOOT_PLATE_T, IBC_FOOT_BOLT_PCD, IBC_FRONT_FOOT_DX, IBC_FRONT_RAIL_H, IBC_FRONT_RAIL_W, FP_CORNER_SEAT_PLATE_T, DRUM_CX, DRUM_CY, DRUM_R, DRUM_H_LT, LT_HOUSING_R, LT_HOUSING_T, LT_DRUM_OR, LT_DRUM_T, LT_OPENING_DEG, EP_X, EP_W, EP_H_LO, EP_H_HI, ENCL_SHELL_D, SOLAR_ARRAY_X, SOLAR_ARRAY_YD, SHELF_X_L, SHELF_X_R, SHELF_W, SHELF_H, SHELF_T, SHELF_DEPTH, SHELF_YD_NEAR, SHELF_YD_FAR, SHELF_STOW_TOP_Z, EVAP_W, EVAP_D, EVAP_H, EVAP_DUCT_X, EVAP_DUCT_Z, EVAP_DUCT_D, INVERTER_X, INVERTER_Z, INVERTER_W, INVERTER_H, INVERTER_D, FAN_BODY_D, FAN_A_YD, FAN_A_H, FAN_B_YD, FAN_B_H, DUCT_DEPTH, DUCT_HEIGHT, BV05_X, TAP_X, TAP_Z, TAP_PIPE_OD, PUMP_PIPE_OD, SPRAY_BAR_FEED_Z, PROC_TRAY_DRAIN_X, PROC_TRAY_SUMP_Z, SUMP_SUCTION_WALL_RUN_Z, PWP_FILTER_X1, PWP_FILTER_X2, PWP_FILTER_X3, PWP_FILTER_TOP_Z, PWP_FILTER_YD, PWP_P02_X, PWP_SV01_X, PWP_WAIST_Z, PWP_SV01_Z, PWP_PANEL_X0, PWP_PANEL_X1, PWP_PANEL_Z0, PWP_SROW_Z0, PWP_ACC2_X, PWP_ACC2_Z0, RWK_X_L, RWK_X_R, RWK_ARM_BOT, RWK_ARM_TOP, RWK_AH, RWK_ARM_W, RWK_BEARER_W, RWK_X_UP, RWK_J6_BOLT_ZS, RWK_J6_EP_H, RWK_RIBBON_NOTCH_YDS, PDH_PLATE_OD, PDH_RING_OD, PDH_PLATE_T, PDH_RING_T, PDH_ADAPT_OD, PDH_ADAPT_T, PDH_MOUNT_BC, PDH_MOUNT_N

from tbs_draw import *            # shared drawing/material primitives (Phase 0 extraction)


# Subsystem → tag map (also drives tag creation order).
TAGS = ["Shell", "Shell Far", "Walkways", "Processing Tray",
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
    (5146, 1181, 1268, "12V DIST BLOCK\n(Cct C)", 300, 0, 450),  # rear-of-corridor-panel Circuit-C distribution block (behind the pump column; center = BACK_X+EQT+24, CTR_Y, pump-column mid Z)
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






# Near-identical colors collapsed onto ONE representative each (tight greys/near-blacks at Δ≤6, plus a
# few same-hue grey/blue/yellow pairs at Δ≤10 — all imperceptible) so they SHARE a material.  Holds the
# overview's unique-material count near ~87 (from 100), well under Sketchfab's upload ceiling.




# Neutral that muted "context" colors blend toward — a light blue-grey matching the
# GhostEquip ghost so faded context reads as a quiet wash, not a saturated volume.





# Web viewers (e.g. Sketchfab) cap material count at ~100. Dozens of elements
# share a color, so materials are keyed by color+alpha and reused — the first
# group to use a given color+alpha names the shared material. This collapses
# ~130 per-element materials down to the number of distinct color+alpha combos.




# Build-time MUTE CONTEXT.  Every drawing helper below takes `mute`/`alpha` that DEFAULT to `None`
# and resolve against the current muted() context (below) — so wrapping a builder in
# `with muted(MUTE_DESAT, MUTE_ALPHA): ...` builds all its geometry desaturated + translucent AT
# SOURCE (color run through mute_hex(color, mute)).  Outside a context the defaults are 0.0 / opaque,
# byte-identical to before.  This replaces the old post-build "mute_groups" re-coloring pass +
# MUTE_TAGS allow-list that generate_pinhole_water_panel.py used to maintain.






















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

    # (Film Plane Wall (Yd=max) — the wall OPPOSITE the pinhole — lives in its own component/tag
    #  (far_wall / "Shell Far") so a scene can hide it; the overview camera sits on the far-wall side
    #  looking in, so it otherwise occludes whatever is on the pinhole wall, e.g. the electrical panel.)

    parts.append(ruby_box("Far End Wall (IBC end)",
                          C_LEN, 0, 0,
                          WALL_T, C_WID, C_HGT,
                          color=w, alpha=0.2, both_sides=True))

    return '\n'.join(parts)


def far_wall():
    """The container wall OPPOSITE the pinhole (Film Plane Wall, Yd=max), on its own 'Shell Far' tag
    so the Electrical scene can hide it — the overview camera looks in from the far-wall side, so this
    wall sits between the camera and the pinhole-wall-mounted electrical panel."""
    return ruby_box("Film Plane Wall (Yd=max)",
                    0, C_WID, 0, C_LEN, WALL_T, C_HGT,
                    color=C_SHELL, alpha=0.2, both_sides=True)


# ── Processing tray ──────────────────────────────────────────────────────────



# ── Walkways ─────────────────────────────────────────────────────────────────

# ── Right walkway — CANTILEVER-RECTANGLE support (rev12; replaces the ceiling hangers) ──
# The right-walkway geometry constants (RWK_*) were PROMOTED to tbs_constants.py (Phase 1,
# 2026-08-18) and are imported above — so the 2D fab drawings dimension the right walkway from
# the SAME source as this builder (no more hardcoded ARM_X / edge literals in the diagram).
# A closed rectangle (2 long beams + 2 end beams) under the deck, supported at mid-span by 2
# CENTER cantilever arms off the IBC corridor uprights; LEFT corners on wall cleats, RIGHT corners
# on a COMBINED plate shared with the bottom film rail.  The builder below reads the RWK_* imports.




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

    # Exterior pinhole disc holder (front board): a Ø240 steel wall-frame ADAPTER welded over the
    # corrugation, the Ø180 disc-holder plate BOLTED to it (4× M6 @ Ø150), and the retaining ring.
    ext = -WALL_T                      # exterior wall face
    parts.append(ruby_cylinder("Wall-frame adapter (welded)", PH_X, ext - PDH_ADAPT_T, PH_H,
                               PDH_ADAPT_OD / 2, PDH_ADAPT_T, axis="y", color=C_STEEL))
    plate_out = ext - PDH_ADAPT_T      # adapter outer face — the plate seats here
    parts.append(ruby_cylinder("Pinhole disc-holder plate", PH_X, plate_out - PDH_PLATE_T, PH_H,
                               PDH_PLATE_OD / 2, PDH_PLATE_T, axis="y", color=C_ALUM))
    parts.append(ruby_cylinder("Disc-holder retaining ring", PH_X, plate_out - PDH_PLATE_T - PDH_RING_T, PH_H,
                               PDH_RING_OD / 2, PDH_RING_T, axis="y", color=C_STEEL))
    # 4× M6 mount bolts through the plate into the adapter (heads proud on the plate outer face)
    for i in range(PDH_MOUNT_N):
        a = math.radians(45 + i * 360.0 / PDH_MOUNT_N)
        bx = PH_X + (PDH_MOUNT_BC / 2) * math.cos(a)
        bz = PH_H + (PDH_MOUNT_BC / 2) * math.sin(a)
        parts.append(ruby_cylinder(f"M6 mount bolt {i+1}", bx, plate_out - PDH_PLATE_T - 3, bz,
                                   5, PDH_PLATE_T + PDH_ADAPT_T + 3, axis="y", color="#3B3B42"))

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



# ── Spray bar (processing-tray wash gantry) ──────────────────────────────────

# spray_bar() moved to generate_spraybar_model.py (sb.spray_bar()) — the single owner; overview,
# water, and construction all draw it via sb.spray_bar() (was duplicated here + in pw).


# ── Plumbing panel (pumps · filters · accumulator) ──────────────────────────
#
# RESOLVED (2026-07-01): overview + ibc-stack were rewired in generate_ruby() to reuse
# the CURRENT water builders — cp.frame/tote_restraint/rear_panel/equipment/plumbing/
# drains_ports + pw.kit/other_equipment/tap01_supply (the water.skp source) — so they
# now render the split Corridor / Pinhole-Wall panel design and stay in sync with
# water.skp.  The OLD pre-corridor-refactor builders (equipment_panel / water_hookups /
# spray_bar_plumbing / water_plumbing) + the legacy FSKID_X/F1_Z/F2_Z/F3_Z corridor-filter
# constants were DELETED 2026-07-05.  ibc_rack() (old single-portal frame, X4734) was RELOCATED
# 2026-08-17 out of this live module into its sole consumer, the ARCHIVED right-cantilever study
# (src/models/archive/generate_right_cantilever_study.py), so the live module can't accidentally
# re-wire it — the live models use the deep-box cp.frame() (X4654).


# ── IBC stack (4× totes, 2×2) + support rack ─────────────────────────────────

# ibc_stack() moved to generate_ibc_model.py (its owner); overview draws it via ib.ibc_stack().


# ── Film plane mechanism ─────────────────────────────────────────────────────





# ── Light-trap drum (revolving entry) ────────────────────────────────────────










# ── Solar array (ground tilt frame, exterior) ────────────────────────────────





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
    """Chemistry prep shelf — WALL-HINGED FOLD-DOWN, shown DEPLOYED (ply-primary redesign 2026-09-07).

    An 18mm plywood board (600×225mm) hinged on the pinhole wall (Yd0) at work height
    Z=SHELF_H, in the widened walkway LEFT of the batteries. PLY-PRIMARY: no steel frame;
    a bolt-on piano hinge along the back edge (into ply tee-nuts) + 2 SS chain stays from
    wall eye bolts above the hinge down to eye bolts at the front corners hold it level in
    tension. It folds UP flat against the wall for transport (top Z=SHELF_STOW_TOP_Z);
    only deployed while mixing (film plane parked), so it never meets the film-plane swing.
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
    # two SS chain stays — wall eye bolt (above the hinge) down to a front-corner eye bolt (tension)
    stay_z = SHELF_H + 230
    for sx in (SHELF_X_L + 30, SHELF_X_R - 30):
        parts.append(ruby_pipe("Chem Shelf chain stay (SS)",
                               (sx, SHELF_YD_NEAR, stay_z), (sx, SHELF_YD_FAR - 10, SHELF_H),
                               2.5, color=C_STEEL))
        parts.append(ruby_box("Chem Shelf chain wall anchor (M8 eye bolt)",
                              sx - 10, SHELF_YD_NEAR, stay_z - 10, 20, 8, 20, color=C_STEEL))
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

    # Cable trunking — 40×25 PVC ceiling channel. OWNED by the electrical model (em.cable_trunking),
    # which fits it to the circuit range (no dead-end stub past the last drop); call it so the trunk
    # can't diverge between overview + electrical (was a full-length copy here).
    import generate_electrical_model as em
    parts.append(em.cable_trunking())

    # White LED strips (Cct G) + red safelight strips (Cct D) + the two ceiling pull-cord switches.
    # SINGLE OWNER — em.light_fixtures() (from the shared LED_PANELS/SAFE_XS/PULL_SW_* data), so the
    # fixtures can't drift between overview + electrical.
    parts.append(em.light_fixtures())

    # Colour-coded branch circuits — OWNED by the electrical model (em's per-circuit routing), so the
    # overview matches electrical.skp instead of re-drawing grey conduits. Each circuit leaves the TOP of
    # its own coloured fuse and routes to its load. D (safelight) + G (white LED) are the ceiling-lighting
    # circuits; A/B (fans) are on the Fan-Wiring tag, C (pumps) via the master switch + pw.panel_power,
    # E (cooler/inverter) on the Electrical tag.
    parts.append(em._multi_run("G", em.LED_ENDS))      # 3× white LED
    parts.append(em._multi_run("D", em.SAFE_ENDS))     # 3× safelight
    # Cct C: connect fuse C DOWN to the master switch (the switched feed onward to the pumps is drawn by
    # pw.panel_power), so fuse C isn't left unconnected. SINGLE OWNER — shared with the electrical model.
    parts.append(em.cct_c_feed())

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
    ffy = 31                                         # ceiling-run Yd OFF the near wall — threads the narrow clear gap
    #   between the top film-plane saddle-bolt nuts (TL/TR near, protrude to Yd≈18) and the Cct-C feed riser at the
    #   master switch (Yd46): >28 clears the nuts, <32 stays >14mm off the riser (2026-08-19 / retuned); every
    #   EP↔fan-tap ceiling feed runs at this Yd and only returns to the wall at a bolt-free X
    # → Fan A (exhaust, Cct A): fixed on the far/sealed end wall (now far-Yd side,
    #   rev9/B2 swap), high near the ceiling. Tap the trunking, cross in Yd over the
    #   IBC stack (no moving parts at the sealed end), drop onto the fan-frame top
    #   (perpendicular entry). Rigid all the way — Fan A doesn't move.
    fa_x = (C_LEN - DUCT_DEPTH) + FAN_BODY_D / 2     # fan-body center X (5618)
    fa_top = FAN_A_H + DUCT_HEIGHT / 2               # fan-housing top Z (2300)
    if which == "A":   # construction phase draws the grey load-side conduit; the overview ("both") uses em._run("A")
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
                                   [(fa_x, 20, czr), (fa_x, ffy, czr), (ep_x, ffy, czr), (ep_x, 20, czr)], fcr, color=C_TRUNK))   # jog to ffy across the ceiling so it clears the TR saddle-bolt nuts; return to the wall at the bolt-free EP column X
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
    import generate_electrical_model as em           # em owns the Cct-B box + flex — single-source off it
    fb_drop_x = em._FANB_BOX_X                        # 420 — box X, shifted to clear the film-plane beams (em is the single source)
    fb_wall_yd = 18                                  # conduit hugs the pinhole wall
    fb_box_z = FAN_B_H                               # wall electrical box at the fan's height
    if which in ("both", "B"):
        if which == "B":   # construction: the rigid Cct-B conduit to the wall box (overview uses em._run("B"))
            parts.append(ruby_pipe_run("Conduit to Fan B (intake, Cct B)",
                                       [(fb_drop_x, fb_wall_yd, czr),
                                        (fb_drop_x, fb_wall_yd, fb_box_z + 45)],
                                       fcr, color=C_TRUNK))
        import generate_lighttrap_model as lt
        parts.append(lt.fan_b_box())   # OWNED by lighttrap (the cargo-door end)
        # The short FLEXIBLE CONNECTOR from the fixed wall box out to Fan B on the swing panel —
        # a SOFT coil cord (the jumper unplugged before the panel swings). SINGLE-SOURCED from em
        # (the Cct-B owner): was a drifting copy here (overview at 420, em at 300 → disconnected).
        parts.append(em.fan_b_flex())

    if which == "both":
        # Overview: the full colour-coded Cct-A / Cct-B circuits from their fuses to the fans —
        # OWNED by the electrical model (em's per-circuit routing), matching electrical.skp.
        parts.append(em._run("A", em.LOADS["A"]))   # fuse A -> ceiling trunk -> Fan A (end wall)
        parts.append(em._run("B", em.LOADS["B"]))   # fuse B -> ceiling trunk -> Fan B wall box
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
    # Cct-E chain — all SINGLE-SOURCED from the electrical model (em), so the overview can't drift
    # from electrical.skp. (It HAD drifted: the overview's copy ran the AC line + cooler cord to a
    # stale GFCI height 0.325·PWR_PANEL_H vs em's _OUTLET_VF, so they didn't reach the real outlet.)
    import generate_electrical_model as em
    parts.append(em.inverter())    # inverter box + Cct-E 120V AC line (inverter -> panel GFCI)
    parts.append(em.cct_e_feed())  # Cct-E DC feed (fuse E -> inverter)
    parts.append(em.cooler())      # cooler body + Cct-E cooler cord (panel GFCI -> cooler)

    # Ø200 supply duct — cooler outlet, through the pinhole-wall penetration into the container.
    # OVERVIEW-OWNED (no ventilation sub-model draws it).
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





# ── Spray-bar plumbing (Blue supply + BV-05 + TAP-01) ────────────────────────


# ── Water / waste plumbing network ───────────────────────────────────────────







# ── Orthogonal pipe routing with swept-torus elbow fittings ──────────────────











# ── Assemble full Ruby script ────────────────────────────────────────────────

def generate_ruby():
    """Build the complete Ruby script for the Overview model."""
    # Reuse the CURRENT water-system builders (water.skp source) so overview stays in
    # sync with the corridor + pinhole-wall panel design (late import — cp/pw import ov).
    import generate_corridor_water_panel as cp
    import generate_pinhole_water_panel as pw
    import generate_ibc_model as ib                 # owns ibc_stack() (Phase 1)
    import generate_spraybar_model as sb            # owns spray_bar() (Phase 1)
    import generate_walkway_model as wm             # owns walkways/cantilever/combined-plates (Phase 1)
    import generate_film_plane_mechanism_model as fp  # owns film_plane_mechanism/saddles (Phase 1)
    import generate_lighttrap_model as lt           # owns panel_pivot() (Phase 1)
    import generate_electrical_model as em          # owns fans()/fan_duct() (Phase 1)
    comps = [
        component("Container Shell", "Shell", container_shell()),
        component("Container Far Wall", "Shell Far", far_wall()),
        component("Walkways", "Walkways", wm.walkways()),
        component("Processing Tray", "Processing Tray", pw.processing_tray()),
        component("Pinhole Assembly", "Pinhole", pinhole_assembly()),
        component("Optical Cone", "Optical Cone", optical_cone()),
        component("Film Plane Mechanism", "Film Plane", fp.film_plane_mechanism()),
        component("FP Combined Corner Plates", "Combined Plate", wm.fp_combined_corner_plates()),
        component("Panel & Pivot Axle", "Pivot Axle", lt.panel_pivot()),
        component("Spray Bar", "Spray Bar", sb.spray_bar()),
        component("Corridor Frame (deep box)", "IBC Rack", cp.frame()),
        component("IBC Tote Restraint", "IBC Rack", cp.tote_restraint()),
        component("Corridor Rear Panel", "Plumbing Panel", cp.rear_panel()),
        component("Corridor Equipment", "Plumbing Panel", cp.equipment(sump_on_skid=True)),
        component("Wall backing (ply)", "Plumbing Panel", pw.backing()),
        component("Pinhole-Wall Kit", "Plumbing Panel", pw.kit(p02_on_corridor=True)),
        component("Skid row (P-04 · SV-02 · DV-02)", "Plumbing Panel", pw.skid_row()),
        component("Skid plumbing", "Plumbing Panel", pw.skid_plumbing()),
        component("IBC Stack", "IBC Stack", ib.ibc_stack()),
        component("Light-Trap Cage", "Light Trap", lt.drum_frame()),
        component("Light-Trap Drum", "Light Trap", lt.drum()),
        component("Light-Trap Bay", "Light Trap", lt.light_trap_bay()),
        component("Electrical", "Electrical", electrical()),
        component("EP External Wiring (PV + E-stop)", "EP Ext Wiring", ep_external_wiring()),
        component("Corridor Pump Wiring (Cct C)", "Lighting", pw.panel_power(include_switch=False)),
        component("Solar Array", "Solar Array", em.solar_array()),
        component("Chemistry Shelf", "Shelf", shelf()),
        component("Light-Trap Door Frame", "Light Seal", lt.door_frame()),
        component("Light Seal & Hinges", "Light Seal", light_seal()),
        component("Lighting & Wiring", "Lighting", lighting_wiring()),
        component("Fan Wiring", "Fan Wiring", fan_wiring()),
        component("Evap Cooler & Duct", "Evap Cooler", evap_cooler()),
        component("Corridor Drains + X-ports", "Water Hookups", cp.drains_ports(sump_on_skid=True)),
        component("Fans A & B", "Fans", em.fans()),
        component("TAP-01 + Spray Supply", "Spray Bar", pw.tap01_supply()),
        component("Corridor Plumbing", "Water Plumbing", cp.plumbing(sump_on_skid=True)),
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
        model_uid("overview"), "sketchup")

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
dir = Geom::Vector3d.new(-0.72, 0.7, 0.5); dir.normalize!   # turned 180° about vertical — eye on the FAR-WALL side, looking INTO the container
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

# Overview — everything visible, Labels OFF; listed first.
model.layers["Labels"].visible = false if model.layers["Labels"]
ovp = model.pages.add("Overview"); ovp.use_camera = true

# Grouped scenes — translucent Shell (context) + the group's subsystems.
{scene_groups_ruby}.each {{ |name, tags|
  # "Shell" is always shown as context; the far wall ("Shell Far") too EXCEPT in the Electrical scene,
  # where it sits between the far-side camera and the pinhole-wall electrical panel and occludes it.
  model.layers.each {{ |l| l.visible = (l == default_layer || l.name == "Shell" ||
                                        (l.name == "Shell Far" && name != "Electrical Systems") ||
                                        tags.include?(l.name)) }}
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
