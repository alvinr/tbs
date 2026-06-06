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

TAGS = ["Context", "Door Frame", "Carriage Rails",
        "Processing Tray", "Walkways", "Film Plane Rails",
        "Sliding Assembly",   # dynamic-component moving group (panel slide)
        "Cargo Doors",        # dynamic-component swing doors (click to close)
        "Labels"]             # add_text callouts — shown only in the "Labeled" scene


# ── "Labeled" scene callouts (project rule: every .skp gets a Labeled scene) ──
# (top-level component instance name, text, leader Δx, Δy, Δz mm). Δy pulls a
# callout OUT toward the viewer (camera looks from −X/−Y); keep Δz modest.
LIGHTTRAP_LABELS = [
    ("Fixed Door Frame",                "DOOR FRAME",                    -500, -200,  800),
    ("Carriage Rails + Locks",          "CARRIAGE RAILS\n+ Destaco locks", 200, -300, 1050),
    ("Panel Slide",                     "HINGE PANEL\n(slides for transport)", 550, -100, 1250),
    ("Cargo Doors",                     "CARGO DOORS",                   -100, -1600,  150),
    ("Processing Tray (partial)",       "PROCESSING TRAY",                950,  500,  300),
    ("Walkways (near + far, partial)",  "WALKWAYS",                       300, -500,  480),
    ("Film-Plane Rails (left, partial)","FILM-PLANE RAILS",               700,    0,  900),
]
# Point-anchored (x,y,z,text,Δx,Δy,Δz) — drum + Fan B are nested in the Panel Slide DC.
LIGHTTRAP_POINT_LABELS = [
    (-400, 1181, 1700, "LIGHT-TRAP DRUM\n(revolving door)", -750,    0,  650),
    ( 150,  365,  700, "FAN B (intake)",                    -200, -650, 1000),
]


def lighttrap_labels():
    """Ruby that adds an in-model text callout (with leader) for each major component
    on the 'Labels' tag — instance-anchored at bounds top-centre, plus point-anchored
    for parts nested inside a DC."""
    rows = []
    for name, text, dx, dy, dz in LIGHTTRAP_LABELS:
        rows.append(
            f'inst = entities.grep(Sketchup::ComponentInstance).find {{ |i| i.name == "{name}" }}\n'
            f'if inst\n'
            f'  bb = inst.bounds\n'
            f'  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)\n'
            f'  txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'  txt.layer = model.layers["Labels"] rescue nil\n'
            f'end')
    for x, y, z, text, dx, dy, dz in LIGHTTRAP_POINT_LABELS:
        rows.append(
            f'anc = Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    return '\n'.join(rows)


# ── Ghosted container context (end opening only) ─────────────────────────────

def context(left_walkway=True, x_far=None):
    """Low-alpha stub of floor, ceiling and both side walls near X=0 so the
    assembly reads in place without modeling the whole container.

    left_walkway: include the ghosted left walkway deck + drum-exit punch-out
    (default True = operating; byte-identical). The transport model passes False —
    the left walkway is the removable lift-out, taken out for transport.
    x_far: far (+X) edge of the stub (default None = operating extent, X=1600,
    byte-identical). The transport model passes a value so the container crops to
    the same plane as its tray / walkway / rail partials."""
    # The container's cargo-door end is at X=0, so the ghost stub starts there.
    # The B2 punch-out bay, drum and cargo doors protrude BEYOND it (X<0) — the
    # stub must NOT extend past the door plane or it reads as a misalignment.
    x0 = 0
    xlen = (x_far - x0) if x_far is not None else 2000
    parts = [
        ruby_box("Floor (context)", x0, 0, -WALL_T, xlen, C_WID, WALL_T,
                 color=C_SHELL, alpha=0.25),
        ruby_box("Ceiling (context)", x0, 0, C_HGT, xlen, C_WID, WALL_T,
                 color=C_SHELL, alpha=0.10),
        ruby_box("Side Wall near (context)", x0, -WALL_T, 0, xlen, WALL_T, C_HGT,
                 color=C_SHELL, alpha=0.16),
        ruby_box("Side Wall far (context)", x0, C_WID, 0, xlen, WALL_T, C_HGT,
                 color=C_SHELL, alpha=0.16),
    ]
    if left_walkway:
        # Ghosted left walkway (the surface the operator steps onto from the
        # drum's interior opening): grating deck at X 170–470, Z 65–80, spanning
        # the full container width to match the ghost-container footprint.
        parts.append(ruby_box("Left walkway (ghost)", ov.WALKWAY_LEFT_X,
                     0, ov.WALKWAY_H - ov.WALKWAY_GRATE_T,
                     ov.WALKWAY_W, C_WID, ov.WALKWAY_GRATE_T,
                     color="#808080", alpha=0.28))
        # Drum-exit PUNCH-OUT — deepened landing in front of the drum opening so
        # the operator has somewhere to step out (the 300mm deck leaves only 20mm).
        parts.append(ruby_box("Left walkway punch-out (ghost)",
                     ov.WALKWAY_LEFT_X + ov.WALKWAY_W, ov.WALKWAY_LEFT_WIDE_YD_L,
                     ov.WALKWAY_H - ov.WALKWAY_GRATE_T,
                     ov.WALKWAY_LEFT_WIDE_W - ov.WALKWAY_W,
                     ov.WALKWAY_LEFT_WIDE_YD_R - ov.WALKWAY_LEFT_WIDE_YD_L,
                     ov.WALKWAY_GRATE_T, color="#808080", alpha=0.34))
    return '\n'.join(parts)


# ── Fixed RHS door frame (seal landing, X just outboard of the panel) ────────

def housing_surround_seal():
    """Interface-2 EPDM ring sealing the Ø900 housing surround to the frame, all
    the way around the aperture (concentric inboard of the panel-perimeter seal,
    interface 1). Exterior door plane (X=-20..0), housing footprint (Yd
    APER_L..APER_R, Z floor-gap..housing-top). Bonded to the housing, so it
    RETRACTS WITH THE HOUSING — the transport model builds it on the moving
    housing rather than on the fixed frame."""
    gw_h, gt_h = 40, 20                    # gasket face width, X-thickness
    hx0 = -gt_h                            # exterior face (X=-20..0)
    hz0, hz1 = PANEL_FLOOR_GAP, DRUM_H     # housing footprint Z (80..2200)
    parts = [
        ruby_box("Housing surround seal bottom", hx0, APER_L, hz0,
                 gt_h, APER_R - APER_L, gw_h, color=C_GASKT),
        ruby_box("Housing surround seal top", hx0, APER_L, hz1 - gw_h,
                 gt_h, APER_R - APER_L, gw_h, color=C_GASKT),
        ruby_box("Housing surround seal left", hx0, APER_L, hz0,
                 gt_h, gw_h, hz1 - hz0, color=C_GASKT),
        ruby_box("Housing surround seal right", hx0, APER_R - gw_h, hz0,
                 gt_h, gw_h, hz1 - hz0, color=C_GASKT),
    ]
    return '\n'.join(parts)


def door_frame(include_seal=True):
    """50×50×3 RHS welded frame lining the cargo-door opening at X≈0. Sits
    just exterior of the panel (X=-50..0); the EPDM gasket seals against it.

    include_seal: append the interface-2 housing-surround EPDM ring (default True
    = operating; byte-identical). The transport model passes False and rebuilds
    that ring on the MOVING housing instead, so the seal retracts with it."""
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

    # ── Interface 2: drum-housing surround → frame EPDM ring (built by
    # housing_surround_seal()). It is bonded to the housing, so the transport
    # model passes include_seal=False and rebuilds it on the moving housing. ──
    if include_seal:
        parts.append(housing_surround_seal())
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

    # (Housing-aperture neoprene lining strips omitted in this model — they read
    # as distracting brown bands flanking the drum opening.)

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

def drum_housing(cx, cy):
    """FIXED part of the housed revolving door: the Ø900 housing (two opposed
    80° openings — exterior + interior/walkway, 180° apart) + SKF 6215 bearings
    + lower bearing mount plate + top/bottom annular felt rings. Translates with
    the panel but does NOT revolve, so it sits in the moving assembly OUTSIDE the
    rotating Drum Rotor sub-component."""
    H, ZB, od = DRUM_H, PANEL_Z_BOT, OPENING_DEG
    parts = []
    # Fixed HOUSING — two solid arcs leaving two od=80° openings (exterior 180° +
    # interior 0°). Suspended: spans Z 80..2200 (bottom at the panel bottom rail).
    parts.append(ov.ruby_arc_wall("LT Housing arc (near Yd)", cx, cy, HOUSING_R,
                                  HOUSING_T, H - ZB, gap_center_deg=270, gap_deg=180 + od,
                                  color=C_ALUM, alpha=0.42, z0=ZB))
    parts.append(ov.ruby_arc_wall("LT Housing arc (far Yd)", cx, cy, HOUSING_R,
                                  HOUSING_T, H - ZB, gap_center_deg=90, gap_deg=180 + od,
                                  color=C_ALUM, alpha=0.42, z0=ZB))
    parts.append(ruby_cylinder("LT Upper bearing (SKF 6215)", cx, cy, H, 65, 45,
                               color=C_STEEL, axis="z"))
    # (Lower bearing collar + mount plate omitted in this model — the drum is
    # top-suspended, and the bottom hardware read as a plate sitting on the floor
    # as the panel slides. Below the drum is just floor.)
    # (Top/bottom annular felt gap-seal rings omitted too — the bottom ring read
    # as a grey bar cutting across the drum bottom.)
    return '\n'.join(parts)


def drum_rotor(cx=0, cy=0):
    """ROTATING part of the revolving door: the single-opening C-shell drum +
    caps + top stub shaft + interior grab rail + opening brush seals. Built
    relative to (cx, cy) so it can live in a NESTED Dynamic Component whose RotZ
    revolves it (the revolving-door action). Pass (0,0) for the DC sub-component
    (origin on the drum axis); drum() passes the absolute drum center for the
    static overview build. Shown at the ENTER position (opening at exterior 180°)."""
    H, ZB, od = DRUM_H, PANEL_Z_BOT, OPENING_DEG
    felt = "#7E7E76"
    parts = []
    parts.append(ov.ruby_arc_wall("LT Drum C-shell", cx, cy, DRUM_OR, DRUM_T, H - ZB,
                                  gap_center_deg=180, gap_deg=od,
                                  color=C_ALUM, alpha=0.85, z0=ZB))
    parts.append(ruby_cylinder("LT Drum top cap", cx, cy, H - 5, DRUM_OR, 5,
                               color=C_ALUM, axis="z"))
    parts.append(ruby_cylinder("LT Drum bottom cap", cx, cy, ZB, DRUM_OR, 5,
                               color=C_ALUM, axis="z"))
    parts.append(ruby_cylinder("LT Drum top shaft", cx, cy, H, 37.5, 65,
                               color=C_STEEL, axis="z"))
    # Interior grab rail on the drum's solid +X wall (operator pulls the drum).
    inner = cx + DRUM_OR - DRUM_T
    gx = cx + DRUM_OR - 75
    parts.append(ruby_cylinder("LT Grab rail", gx, cy, 700, 15, 400,
                               color=C_STEEL, axis="z"))
    for bz in (720, 1080):
        parts.append(ruby_box("LT Grab rail standoff", gx, cy - 6, bz,
                              inner - gx, 12, 12, color=C_STEEL))
    # Felt/brush wiper strips on the two vertical edges of the drum opening.
    seal_r = (DRUM_OR + HOUSING_R - HOUSING_T) / 2
    for edge in (180 - od / 2, 180 + od / 2):
        bx = cx + seal_r * math.cos(math.radians(edge))
        by = cy + seal_r * math.sin(math.radians(edge))
        parts.append(ruby_cylinder("LT Drum opening brush seal", bx, by, ZB, 7, H - ZB,
                                   color=felt, axis="z"))
    return '\n'.join(parts)


def drum():
    """Full housed revolving door = fixed housing + rotating C-shell drum, at the
    absolute drum center (DRUM_CX, DRUM_CY). Used by the overview (static). The
    light-trap model uses drum_housing() + a rotating Drum Rotor DC instead."""
    return drum_housing(DRUM_CX, DRUM_CY) + "\n" + drum_rotor(DRUM_CX, DRUM_CY)


# ── Sliding carriage system (transport-mode slide) ──────────────────────────
# Slide travel LENGTHENED to ~500mm so the deeper Ø900 housing (exterior overhang
# ~450mm) fully retracts behind the door closure plane for transport. Rails at the
# widened center-zone step lines (NEW_YD_L/R). NB: the longer retraction carries
# the housing into the left-walkway / near-tray zone — tray-end clearance during
# transport is an open detail to confirm.
TRANSPORT_SLIDE = ov.PANEL_SLIDE        # 880 — from constants (rev 9 / B2)

def carriage_fixed():
    """FIXED part of the sliding carriage: the two HGR20 ceiling rails + both
    Destaco toggle-clamp lock points (operational X≈0 + transport X≈TRANSPORT_SLIDE).
    These do NOT travel with the panel, so they live outside the dynamic-component
    moving group."""
    parts = []
    rail_x0, rail_len = -30, TRANSPORT_SLIDE + 220  # spans the full B2 transport slide
    rail_w, rail_h = 20, 30
    rail_z = C_HGT - rail_h                          # 2358 — hung from ceiling
    for yd, nm in [(NEW_YD_L, "L"), (NEW_YD_R, "R")]:
        parts.append(ruby_box(f"HGR20 rail {nm}", rail_x0, yd - rail_w / 2, rail_z,
                              rail_len, rail_w, rail_h, color=C_RAIL))
    # Destaco 207-U toggle clamps — operational lock (X≈0) + transport lock (X≈TRANSPORT_SLIDE).
    for cx, lock in [(-10, "operational"), (TRANSPORT_SLIDE - 10, "transport")]:
        for yd in (NEW_YD_L, NEW_YD_R):
            parts.append(ruby_box(f"Destaco clamp ({lock}) base", cx, yd - 18,
                                  rail_z - 70, 60, 36, 24, color=C_STEEL))
            parts.append(ruby_box(f"Destaco clamp ({lock}) handle", cx + 10, yd - 6,
                                  rail_z - 46, 70, 12, 12, color=C_CARR))
    return '\n'.join(parts)


def carriage_moving(slide=0):
    """MOVING part of the sliding carriage: the HGH20CA blocks + suspension
    brackets + left 60×60 SHS carriage beam. These travel with the hinge panel,
    so in the dynamic-component model they go INSIDE the moving group (slide=0,
    the DC handles the translation)."""
    parts = []
    rail_h = 30
    rail_z = C_HGT - rail_h
    carr_w, carr_d, carr_h = 44, 44, 28
    brk_w, brk_d, brk_h = 60, 40, 30
    for yd, nm in [(NEW_YD_L, "L"), (NEW_YD_R, "R")]:
        parts.append(ruby_box(f"HGH20CA carriage {nm}", 18 + slide, yd - carr_d / 2,
                              rail_z - carr_h, carr_w, carr_d, carr_h, color=C_CARR))
        parts.append(ruby_box(f"Suspension bracket {nm}", 15 + slide, yd - brk_d / 2,
                              PANEL_Z_TOP, brk_w, brk_d, rail_z - carr_h - PANEL_Z_TOP,
                              color=C_STEEL))
    parts.append(ruby_box("Left carriage beam (60×60 SHS)", 0 + slide, 0, PANEL_Z_BOT,
                          60, 60, PANEL_Z_TOP - PANEL_Z_BOT, color=C_STEEL))
    return '\n'.join(parts)


def sliding_carriage(slide=0):
    """Full carriage = fixed rails/clamps + moving blocks/brackets/beam."""
    return carriage_fixed() + "\n" + carriage_moving(slide)


# Cargo-door hinge X (vertical hinge axis, at the leaf-thickness centerline just
# outside the door frame). Each leaf is built in LOCAL coords with its origin at
# this hinge so a Dynamic-Component RotZ swings it open/closed.
DOOR_HINGE_X = -85


def door_leaf_local(side):
    """One ghosted ISO cargo-door leaf in LOCAL coords, origin at its vertical
    hinge. side 'near' (extends +Yd from the Yd=0 corner) or 'far' (extends -Yd
    from the Yd=C_WID corner). At RotZ=0 the leaf lies CLOSED across the opening;
    the DC swings it to ±180° (fully open, flat in the door-frame plane)."""
    dt = 60                                   # leaf thickness (X at closed)
    leaf_len = ov.C_WID / 2 - 3               # half width minus the center meeting gap
    y0 = 0 if side == "near" else -leaf_len
    return ruby_box(f"Cargo door leaf {side}", -dt / 2, y0, 0,
                    dt, leaf_len, ov.C_HGT, color=C_STEEL, alpha=0.25)


# ── Fan B on the hinge panel (reused from Overview's shared builder) ─────────

def fan_b():
    return '\n'.join(ov.fan_duct("Fan B (intake)", 0, -1, FAN_B_YD, FAN_B_H))


# ── Shared cargo-door-end context (tray + walkways + film-plane rails) ───────
# Cropped to a common +X plane so the static context reads in place around the
# moving Dynamic-Component assembly. Reuses the overview's tray / walkway / rail
# geometry + constants via `ov`.
PARTIAL_X = 1600        # common +X crop plane — container stub, tray, walkways and
                        # film-plane beams all end here so their cut faces align


def processing_tray_partial():
    """A cropped section of the processing-tray basin at the cargo-door end."""
    x0 = ov.PROC_TRAY_X_L
    yN, yF = ov.PROC_TRAY_YD_NEAR, ov.PROC_TRAY_YD_FAR
    w, d = PARTIAL_X - x0, yF - yN
    st, rt, rim = 2, 2, ov.PROC_TRAY_RIM
    return '\n'.join([
        ruby_box("Processing Tray Floor (partial)", x0, yN, 0, w, d, st, color=ov.C_TRAY),
        ruby_box("Tray Rim Near (partial)", x0, yN, st, w, rt, rim - st, color=ov.C_TRAY),
        ruby_box("Tray Rim Far (partial)", x0, yF - rt, st, w, rt, rim - st, color=ov.C_TRAY),
        ruby_box("Tray Rim Left (cargo end)", x0, yN, st, rt, d, rim - st, color=ov.C_TRAY),
        ruby_box("Chemistry Bath (partial)", x0 + rt, yN + rt, st,
                 w - 2 * rt, d - 2 * rt, rim - st - 8, color=ov.C_BATH, alpha=0.45),
    ])


def walkways_partial():
    """The NEAR (pinhole-wall side, Yd 0) and FAR walkway decks, cropped to the
    cargo-door-end zone. (The left walkway is the removable lift-out — shown as a
    ghost in the operating context, omitted entirely for transport.)"""
    grate_z = ov.WALKWAY_H - ov.WALKWAY_GRATE_T
    t = ov.WALKWAY_GRATE_T
    x0 = ov.WALKWAY_LEFT_X + ov.WALKWAY_W       # = 470 — where the long decks begin
    w = PARTIAL_X - x0
    return '\n'.join([
        ruby_box("Walkway Near (partial)", x0, 0, grate_z,
                 w, ov.WALKWAY_W, t, color=ov.C_WALKWAY),
        ruby_box("Walkway Far (partial)", x0, ov.WALKWAY_FAR_YD, grate_z,
                 w, ov.WALKWAY_W, t, color=ov.C_WALKWAY),
    ])


def film_plane_left():
    """Partial of the film-plane rail mechanism at the LEFT (cargo-door) end.

    The film plane rides 4 corner rails running in Yd (depth). This shows the LEFT
    pair — upper (TL) and lower (BL) at X=RAIL_X_L, now CONTINUOUS (rev9 B2: the
    drum is offset clear of the X=150 rail via the panel bay, so there is no
    demountable segment) — plus the brace-cage beams (upper + lower) + corner posts
    tying them at the near-wall (Yd≈100) and far-wall (Yd≈2262) ends. Fixed (no
    slide); the whole left rails are struck for transport (transport model)."""
    rail = 40
    s = ov.BRACE_RHS                            # 50 — brace RHS
    xL = ov.RAIL_X_L                            # 150 — left rail X
    z_bot = ov.RAIL_OFF                         # 100 — lower rail Z
    z_top = ov.C_HGT - ov.RAIL_OFF - rail       # 2248 — upper rail Z
    yN, yF = ov.FP_Y_MIN, ov.FP_Y               # 100 (near-wall end), 2262 (far-wall end)
    bx = PARTIAL_X - xL                          # brace-beam length (cropped)
    C = ov.C_STEEL
    parts = [
        ruby_box("FP Rail BL (lower left)", xL, yN, z_bot, rail, yF - yN, rail, color=C),
        ruby_box("FP Rail TL (upper left)", xL, yN, z_top, rail, yF - yN, rail, color=C),
    ]
    for py, pn in [(yN, "near wall"), (yF, "far wall")]:
        parts.append(ruby_box(f"FP Brace Beam Lower ({pn})", xL, py, z_bot, bx, s, s, color=C))
        parts.append(ruby_box(f"FP Brace Beam Upper ({pn})", xL, py, z_top, bx, s, s, color=C))
        parts.append(ruby_box(f"FP Brace Post L ({pn})", xL, py, z_bot, s, s, z_top - z_bot, color=C))
    return '\n'.join(parts)


def bay():
    """B2 punch-out bay — the hinge-panel center zone as a forward box (X from
    BAY_FRONT_X to the panel face) enclosing the offset Ø900 housing. A 4-wall
    rectangular tube (Yd = center-zone step lines, Z = floor-gap..panel-top), open
    at the exterior end (entrance) and the interior end (exit onto the walkway)."""
    yL, yR = ov.PANEL_CORNER_YD_L, ov.PANEL_CORNER_YD_R   # 653, 1709
    z0, z1 = PANEL_FLOOR_GAP, PANEL_Z_TOP                 # 80, 2300
    xf = ov.BAY_FRONT_X                                    # -890
    t = ov.BAY_WALL_T                                      # 6
    depth = ov.BAY_BACK_X - xf                             # 890 — bay X span
    h = z1 - z0
    return '\n'.join([
        ruby_box("Bay wall near (Yd)", xf, yL, z0, depth, t, h, color=C_PLY),
        ruby_box("Bay wall far (Yd)", xf, yR - t, z0, depth, t, h, color=C_PLY),
        ruby_box("Bay wall top", xf, yL, z1 - t, depth, yR - yL, t, color=C_PLY),
        ruby_box("Bay wall bottom", xf, yL, z0, depth, yR - yL, t, color=C_PLY),
    ])


# ── Assemble the Ruby script ─────────────────────────────────────────────────

def generate_ruby():
    # Fixed subsystems (do not travel with the panel).
    static_comps = [
        component("Context", "Context", context(x_far=PARTIAL_X)),
        # include_seal=False — the housing-surround EPDM ring is bonded to the
        # moving housing (built in the DC below via housing_surround_seal()), so it
        # must NOT also be drawn on the fixed frame or a copy is left behind on slide.
        component("Fixed Door Frame", "Door Frame", door_frame(include_seal=False)),
        component("Carriage Rails + Locks", "Carriage Rails", carriage_fixed()),
        component("Processing Tray (partial)", "Processing Tray", processing_tray_partial()),
        component("Walkways (near + far, partial)", "Walkways", walkways_partial()),
        component("Film-Plane Rails (left, partial)", "Film Plane Rails", film_plane_left()),
    ]
    static_body = '\n'.join(static_comps)

    # Moving assembly → the Dynamic Component. Click it with the Interact tool to
    # slide between operating (X=0) and transport (X=TRANSPORT_SLIDE). Everything
    # that travels with the panel lives here: panel + bay + drum + housing seal +
    # Fan B + the carriage blocks/brackets/beam (all at slide=0; the DC translates).
    dc_body = '\n'.join([
        hinge_panel(),
        bay(),
        drum_housing(DRUM_CX, DRUM_CY),   # fixed housing (the rotor is a nested DC, below)
        # housing_surround_seal() omitted — the interface-2 EPDM ring read as a
        # distracting band flanking the drum opening; not needed in this view.
        fan_b(),
        carriage_moving(),
    ])
    rotor_body = drum_rotor(0, 0)         # local-origin geometry for the revolve DC

    # Cargo-door leaves (local-origin geometry for the swing DC).
    near_leaf = door_leaf_local("near")
    far_leaf = door_leaf_local("far")
    cwid = ov.C_WID
    drum_cx, drum_cy = DRUM_CX, DRUM_CY

    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Light Trap (dynamic slide)", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild: erase ALL prior instances.
to_erase = entities.to_a.select {{ |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

# ── Tags (layers) ──
{tags_ruby}

# ── Fixed subsystems ──
{static_body}

# ═══ Panel Slide — DYNAMIC COMPONENT (the moving assembly) ═══
# Interact tool → click to ANIMATE the panel between operating (0) and
# transport ({TRANSPORT_SLIDE}mm).
defn = model.definitions.add("Panel Slide")
ents = defn.entities
{dc_body}

# Drum Rotor geometry nested INSIDE Panel Slide so it travels with the slide.
rotor_defn = model.definitions.add("Drum Rotor")
ents = rotor_defn.entities
{rotor_body}
rotor_inst = defn.entities.add_instance(rotor_defn, Geom::Transformation.translation([{drum_cx}.mm, {drum_cy}.mm, 0]))
rotor_inst.name = "Drum Rotor"
rotor_inst.layer = model.layers["Sliding Assembly"]

inst = entities.add_instance(defn, Geom::Transformation.new)
inst.name = "Panel Slide"
inst.layer = model.layers["Sliding Assembly"]
da = "dynamic_attributes"
[defn, inst].each do |e|
  e.set_attribute(da, "_name", "PanelSlide")
  e.set_attribute(da, "_lengthunits", "MILLIMETERS")
  e.set_attribute(da, "x", 0.0)
end
inst.set_attribute(da, "_x_access", "VIEW")
inst.set_attribute(da, "_x_label", "Slide")
inst.set_attribute(da, "onclick", 'ANIMATE("x", 0, {TRANSPORT_SLIDE})')
inst.set_attribute(da, "_onclick_access", "NONE")
dc_inst = inst

# Drum Rotor — nested, so it travels with the slide. Its RotZ is DRIVEN by the
# slide via a formula on the parent's x (the same child-reads-parent pattern the
# cargo doors use, which DOES update during the parent's animation): as the panel
# slides 0→{TRANSPORT_SLIDE}mm the drum revolves 0→180° so the opening swings from
# the exterior round to face the INTERIOR (open on the inside in transport). No
# onclick on the drum, so clicking it still cleanly slides the panel.
rotor_inst.set_attribute(da, "_name", "DrumRotor")
rotor_inst.set_attribute(da, "_lengthunits", "MILLIMETERS")
rotor_inst.set_attribute(da, "rotz", 0.0)
rotor_inst.set_attribute(da, "_rotz_formula", "180*PanelSlide!x/{TRANSPORT_SLIDE}")

# ═══ Cargo Doors — DYNAMIC COMPONENT (click to close) ═══
# Parent "Cargo Doors" holds two leaf children whose RotZ is driven by the
# parent's "shut" attribute (0 = open / ±180°, 1 = closed / 0°). Click the parent
# with the Interact tool → ANIMATE shut 0↔1 swings both leaves together.
doors_defn = model.definitions.add("Cargo Doors")
doors_ents = doors_defn.entities

near_defn = model.definitions.add("Cargo Door Leaf Near")
ents = near_defn.entities
{near_leaf}
near_inst = doors_ents.add_instance(near_defn, Geom::Transformation.translation([{DOOR_HINGE_X}.mm, 0, 0]))
near_inst.name = "Leaf Near"

far_defn = model.definitions.add("Cargo Door Leaf Far")
ents = far_defn.entities
{far_leaf}
far_inst = doors_ents.add_instance(far_defn, Geom::Transformation.translation([{DOOR_HINGE_X}.mm, {cwid}.mm, 0]))
far_inst.name = "Leaf Far"

doors_inst = entities.add_instance(doors_defn, Geom::Transformation.new)
doors_inst.name = "Cargo Doors"
doors_inst.layer = model.layers["Cargo Doors"]

dda = "dynamic_attributes"
doors_inst.set_attribute(dda, "_name", "CargoDoors")
doors_inst.set_attribute(dda, "shut", 0.0)
doors_inst.set_attribute(dda, "_shut_access", "VIEW")
doors_inst.set_attribute(dda, "_shut_label", "Shut")
doors_inst.set_attribute(dda, "onclick", 'ANIMATE("shut", 0, 1)')
doors_inst.set_attribute(dda, "_onclick_access", "NONE")
near_inst.set_attribute(dda, "_name", "LeafNear")
near_inst.set_attribute(dda, "rotz", 180.0)
near_inst.set_attribute(dda, "_rotz_formula", "180*(1-CargoDoors!shut)")
far_inst.set_attribute(dda, "_name", "LeafFar")
far_inst.set_attribute(dda, "rotz", -180.0)
far_inst.set_attribute(dda, "_rotz_formula", "-180*(1-CargoDoors!shut)")

# ── "Labeled" scene callouts (Labels tag — shown only in the "Labeled" scene) ──
{lighttrap_labels()}

model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier generator versions ──
keep_tags = {keep_tags_ruby}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

# ── Camera + scenes (the slide is interactive; plus a "Labeled" callout scene) ──
model.layers.each {{ |l| l.visible = true }}
model.layers["Labels"].visible = false if model.layers["Labels"]  # frame geometry, not labels
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(-0.6, -0.72, 0.45); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents
model.active_view.zoom(0.62)   # pull back so callouts have margin (and read larger)
# Main interactive scene — Labels OFF.
page = model.pages.add("Light Trap — click panel to slide")
page.use_camera = true
# Labeled — same view + component callouts.
model.layers["Labels"].visible = true if model.layers["Labels"]
lpage = model.pages.add("Labeled"); lpage.use_camera = true
model.layers["Labels"].visible = false if model.layers["Labels"]

model.commit_operation

# Register the DC attributes with the Dynamic Components engine so the Interact
# tool drives the slide (skipped if the extension isn't loaded).
dc_ready = false
if defined?($dc_observers) && $dc_observers.respond_to?(:get_latest_class)
  cls = $dc_observers.get_latest_class
  if cls
    [dc_inst, doors_inst].each {{ |di| cls.redraw_with_undo(di) rescue nil }}
    dc_ready = true
  end
end

{{ success: true, model: "Light Trap (dynamic slide)",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   dynamic_engine: dc_ready, slide_mm: {TRANSPORT_SLIDE},
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
