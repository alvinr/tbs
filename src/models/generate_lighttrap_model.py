#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_lighttrap_model.py — Generate Ruby for the TBS-001 "Light Trap"
focus model (models/lighttrap.skp).

A detailed, report-accurate model of the cargo-door end assembly only:
  - the revolving light-trap DRUM (caps, stub shafts, SKF bearings, grab rail),
  - the hinged stepped PANEL (3 zones + drum aperture + EPDM seal + latches),
  - the ROTATION transport system (rev10 — supersedes the slide): the panel+drum
    +drum-cage assembly SWINGS 56° about a vertical Ø89 CHS pivot post (the film
    far-left upright) to clear the cargo doors; split panel (fixed left + swinging
    + fixed far), removable left film rails, top/bottom hub bearings, a wall-stay
    lock, and the fixed RHS door frame,
  - Fan B (intake) mounted on the swinging panel — reused from the Overview's
    shared fan_duct() builder so it stays in sync.

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
PANEL_FLOOR_GAP = ov.PANEL_FLOOR_GAP          # 130 (rev: +50 walkway raise)
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

# ── Rotation transport geometry (rev10 — supersedes the slide) ───────────────
PIVOT_X, PIVOT_YD = ov.PIVOT_X, ov.PIVOT_YD       # 175, 2287 — vertical swing axis
LOCK = ov.SWING_LOCK_DEG                           # 56 — transport swing angle
CUT = ov.PANEL_CUT_YD                              # 180 — fixed-left / swing cut
FAR0 = ov.FAR_STRIP_YD0                            # 2287 — fixed-far strip start (= pivot)
WALL_FAR = 2000                                    # context far extent — reaches the stay wall anchor
STAY_Z = (200, 2050)                               # bottom + top transport-stay heights
LOCK_BOLT = (20, 350)                              # stay hook on the swinging frame (good lever arm)


def _rot_pt(x, y, deg):
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    return PIVOT_X + (x - PIVOT_X) * c - (y - PIVOT_YD) * s, PIVOT_YD + (x - PIVOT_X) * s + (y - PIVOT_YD) * c


SOCKET = _rot_pt(LOCK_BOLT[0], LOCK_BOLT[1], LOCK)  # transport position of the frame hook (1694, 1075)

TAGS = ["Context", "Door Frame", "Pivot Axle",
        "Processing Tray", "Walkways", "Film Plane Rails",
        "Near Leaf", "Far Leaf", "Lock anchor", "Panel skin",
        "Panel Swing",        # dynamic-component moving group (the swinging assembly)
        "Cargo Doors",        # dynamic-component swing doors (click to close)
        "Labels"]             # add_text callouts — shown only in the "Labeled" scene


# ── "Labeled" scene callouts (project rule: every .skp gets a Labeled scene) ──
# (top-level component instance name, text, leader Δx, Δy, Δz mm). Δy pulls a
# callout OUT toward the viewer (camera looks from −X/−Y); keep Δz modest.
LIGHTTRAP_LABELS = [
    ("Fixed Door Frame",                "DOOR FRAME",                    -500, -200,  800),
    ("Panel Swing",                     "HINGE PANEL\n(swings 56° for transport)", 550, -100, 1250),
    ("Cargo Doors",                     "CARGO DOORS",                   -100, -1600,  150),
    ("Processing Tray (partial)",       "PROCESSING TRAY",                950,  500,  300),
]
# Point-anchored (x,y,z,text,Δx,Δy,Δz). Used for parts nested in a DC (drum, Fan B)
# AND for components whose bounds-CENTRE lands between paired parts (walkways) or off
# the rail (film-plane rails) — anchor on the actual near member.
LIGHTTRAP_POINT_LABELS = [
    (-400, 1181, 1700, "LIGHT-TRAP DRUM\n(revolving door)", -750,    0,  650),
    ( 150,  365,  700, "FAN B (intake)",                    -200, -650, 1000),
    ( 175, 2287, 1600, "PIVOT POST Ø89 CHS\n(= film far-left post)", 550, -200, 700),  # the swing axis
    (1035,  150,   73, "WALKWAYS",                           250, -750,  900),    # near walkway strip
    ( 170, 1181, 2268, "FILM-PLANE RAILS\n(left pair removable)", 1400, 0, 300),  # top-left FP rail
    (SOCKET[0], 0, 1075, "TRANSPORT STAY anchor\n(bolted plates; rod→wall when swung)", 300, -300, 700),
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


# ── Rotation transport system (rev10 — supersedes the slide carriage) ────────
# The pivot AXLE is fixed; the hub + panel + cage swing about it. Geometry came from the
# rotation design study (now folded in here — this model IS the production version) and is
# parameterised on the tbs_constants swing values via `ov`. Design spec:
# docs/superpowers/specs/2026-06-08-cargo-door-rotating-panel-design.md

def axle():
    """FIXED pivot: a Ø89×8 CHS post (the film far-left upright reused), floor-to-roof,
    bolted at both ends + a thrust collar the assembly rests on. Carries the swing
    cantilever (σ~95 MPa, SF~3.7 on S355)."""
    c = C_STEEL
    r = ov.PIVOT_POST_OD / 2.0                       # 44.5
    return '\n'.join([
        ruby_cylinder("Pivot post (Ø89 CHS)", PIVOT_X, PIVOT_YD, 0, r, C_HGT, color=c, axis="z"),
        ruby_cylinder("Pivot floor mount plate", PIVOT_X, PIVOT_YD, 0, 110, 20, color=c, axis="z"),
        ruby_cylinder("Pivot roof mount plate", PIVOT_X, PIVOT_YD, C_HGT - 20, 110, 20, color=c, axis="z"),
        ruby_cylinder("Pivot thrust collar", PIVOT_X, PIVOT_YD, 130, 75, 25, color=c, axis="z"),
    ])


def pivot_link():
    """MOVING hub riding the fixed post: thrust bearing (assembly weight ~330 kg) +
    top/bottom radial bearings (react the overturning couple) + 3 hinge brackets tying
    the hub to the panel. Swings with the frame."""
    cbear = "#5A5AA0"
    p = [
        ruby_cylinder("Hub tube", PIVOT_X, PIVOT_YD, 180, 58, 2050 - 180, color=C_STEEL, alpha=0.4, axis="z"),
        ruby_cylinder("Hub thrust bearing", PIVOT_X, PIVOT_YD, 155, 70, 25, color=cbear, axis="z"),
        ruby_cylinder("Hub radial bearing (bottom)", PIVOT_X, PIVOT_YD, 220, 60, 55, color=cbear, axis="z"),
        ruby_cylinder("Hub radial bearing (top)", PIVOT_X, PIVOT_YD, 2050, 60, 55, color=cbear, axis="z"),
    ]
    for z in (300, 1180, 2000):
        p.append(ruby_box("Hinge bracket (panel→hub)", 55, PIVOT_YD - 35, z, 140, 70, 110, color=C_STEEL))
    return '\n'.join(p)


def near_leaf():
    """FIXED LEFT panel (Yd0..CUT) — does NOT swing; covers the near-wall strip past the
    near upright. Own perimeter EPDM + the vertical cut seal the swinging panel butts."""
    z0, z1 = PANEL_FLOOR_GAP, PANEL_Z_TOP
    gw, gt = 40, 20
    return '\n'.join([
        ruby_box(f"Fixed left panel (Yd0-{CUT})", 0, 0, z0, 40, CUT, z1 - z0, color="#C8A060"),
        ruby_box("EPDM fixed-panel top", -gt, 0, z1 - gw, gt, CUT, gw, color=C_GASKT),
        ruby_box("EPDM fixed-panel bottom", -gt, 0, z0, gt, CUT, gw, color=C_GASKT),
        ruby_box("EPDM fixed-panel left", -gt, 0, z0, gt, gw, z1 - z0, color=C_GASKT),
        ruby_box("EPDM cut seal (fixed-swing joint)", 0, CUT - 6, z0, 40, 12, z1 - z0, color=C_GASKT),
    ])


def far_leaf():
    """FIXED FAR strip (Yd FAR0..C_WID, ~75mm) at the pivot side — ends the swinging panel
    AT the pivot so nothing swings outboard of the door plane (#10). Own perimeter EPDM +
    the vertical cut seal at the pivot line."""
    z0, z1 = PANEL_FLOOR_GAP, PANEL_Z_TOP
    w = C_WID - FAR0
    gw, gt = 40, 20
    return '\n'.join([
        ruby_box(f"Fixed far panel strip (Yd{FAR0}-{C_WID})", 0, FAR0, z0, 40, w, z1 - z0, color="#C8A060"),
        ruby_box("EPDM fixed-far top", -gt, FAR0, z1 - gw, gt, w, gw, color=C_GASKT),
        ruby_box("EPDM fixed-far bottom", -gt, FAR0, z0, gt, w, gw, color=C_GASKT),
        ruby_box("EPDM fixed-far right (far wall)", -gt, C_WID - gw, z0, gt, gw, z1 - z0, color=C_GASKT),
        ruby_box("EPDM far cut seal (swing-fixed joint)", 0, FAR0 - 6, z0, 40, 12, z1 - z0, color=C_GASKT),
    ])


def drum_frame():
    """Steel support CAGE around the Ø900 drum (top+bottom rectangles + 4 posts, full
    depth Z130..DRUM_H) carrying the central drum REVOLVE bearings: bottom = Ø220 flush
    thrust slew pad recessed to the Z130 sill (step-over, no trip); top = Ø120 radial
    guide journal. Swings with the assembly."""
    s = 50
    x0, x1 = ov.DRUM_CAGE_X0, ov.DRUM_CAGE_X1
    y0, y1 = ov.DRUM_CAGE_YD_L, ov.DRUM_CAGE_YD_R
    zb, zt = PANEL_FLOOR_GAP, DRUM_H
    c, cb = C_STEEL, "#5A5AA0"
    p = []
    for z in (zb, zt - s):
        p += [
            ruby_box("Drum frame rail (X near)", x0, y0, z, x1 - x0, s, s, color=c),
            ruby_box("Drum frame rail (X far)", x0, y1 - s, z, x1 - x0, s, s, color=c),
            ruby_box("Drum frame rail (Yd front)", x0, y0, z, s, y1 - y0, s, color=c),
            ruby_box("Drum frame rail (Yd back)", x1 - s, y0, z, s, y1 - y0, s, color=c),
        ]
    for px in (x0, x1 - s):
        for py in (y0, y1 - s):
            p.append(ruby_box("Drum frame post", px, py, zb, s, s, zt - zb, color=c))
    p.append(ruby_box("Drum bearing cross-beam (top)", DRUM_CX - s // 2, y0, zt - s, s, y1 - y0, s, color=c))
    p.append(ruby_cylinder("Drum top radial journal (Ø120 guide)", DRUM_CX, DRUM_CY, zt - s, 60, s, color=cb, axis="z"))
    p.append(ruby_cylinder("Drum top pivot pin", DRUM_CX, DRUM_CY, zt - s - 70, 22, 80, color=c, axis="z"))
    p.append(ruby_box("Drum bearing cross-beam (bottom, recessed)", DRUM_CX - s // 2, y0, zb - s, s, y1 - y0, s, color=c))
    p.append(ruby_cylinder("Drum bottom thrust bearing (Ø220 flush slew pad)", DRUM_CX, DRUM_CY, zb - 22, 110, 22, color=cb, axis="z"))
    p.append(ruby_box("Drum threshold sill (flush, chamfered step-over)", DRUM_CX - 240, DRUM_CY - 320, zb - 8, 250, 640, 8, color="#7A7A82"))
    return '\n'.join(p)


def frame_hooks():
    """Hook brackets on the swinging frame (top + bottom) that the wall stays engage."""
    bx, by = LOCK_BOLT
    return '\n'.join(
        ruby_box("Stay hook (frame)", bx - 30, by - 30, z - 35, 60, 60, 70, color=C_STEEL)
        for z in STAY_Z)


# Permanent bolted wall anchors for the transport stays (top+bottom): the near wall can't
# be welded to, so the stay eye reacts into an inside + outside plate pair bolted through
# the wall (4× M16). Stays put even when the rod is removed.
PLATE_HW, PLATE_T, BOLT_OFF, BOLT_D = 100, 12, 70, 16


def wall_anchors():
    hx = SOCKET[0]                                   # 1694
    wt = WALL_T
    p = []
    for z in STAY_Z:
        p += [
            ruby_box("Stay inside plate", hx - PLATE_HW, 0, z - PLATE_HW, 2 * PLATE_HW, PLATE_T, 2 * PLATE_HW, color=C_STEEL),
            ruby_box("Stay outside plate", hx - PLATE_HW, -wt - PLATE_T, z - PLATE_HW, 2 * PLATE_HW, PLATE_T, 2 * PLATE_HW, color=C_STEEL),
            ruby_box("Stay eye", hx - 15, PLATE_T, z - 15, 30, 55, 30, color=C_STEEL),
        ]
        for dx in (-BOLT_OFF, BOLT_OFF):
            for dz in (-BOLT_OFF, BOLT_OFF):
                p.append(ruby_box("Stay bolt M16", hx + dx - BOLT_D // 2, -wt - PLATE_T - 6, z + dz - BOLT_D // 2,
                                  BOLT_D, wt + 2 * PLATE_T + 12, BOLT_D, color=C_STEEL))
    return '\n'.join(p)


def _rail_saddle(ys, z):
    """Drop-in U-saddle cradling a removable 40×40 rail end: shelf + X-side cheeks +
    tapered locating dowel (to the film datum) + a removable clamp bar."""
    c, cclamp, cdowel = C_STEEL, "#7A7A82", "#9A9AA2"
    return '\n'.join([
        ruby_box("Rail saddle shelf", 133, ys, z - 14, 74, 80, 14, color=c),
        ruby_box("Rail saddle cheek -X", 133, ys, z, 12, 80, 44, color=c),
        ruby_box("Rail saddle cheek +X", 195, ys, z, 12, 80, 44, color=c),
        ruby_box("Rail clamp bar (removable)", 133, ys + 22, z + 40, 74, 36, 14, color=cclamp),
        ruby_cylinder("Rail locating dowel (taper)", 170, ys + 40, z - 14, 5, 22, color=cdowel, axis="z"),
    ])


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
    """The NEAR (pinhole-wall side, Yd 0) and FAR walkway decks, cropped to the cargo-door-end
    zone — all LEVEL (Z130). The near deck's door-end band (X 470..WALKWAY_NEAR_LIFTOUT_X_R) is
    a REMOVABLE lift-out for transport (the swing sweeps it) — shown installed here (operating)
    in a distinct color. The FAR deck is not swept; the left walkway also lifts out (omitted)."""
    t = ov.WALKWAY_GRATE_T
    full_z = ov.WALKWAY_H - t                    # grate-bottom Z (level, Z130 top)
    x0 = ov.WALKWAY_LEFT_X + ov.WALKWAY_W        # = 470 — where the long decks begin
    liftout_x = ov.WALKWAY_NEAR_LIFTOUT_X_R      # ~900 — swept door-end band end
    w = PARTIAL_X - x0
    return '\n'.join([
        ruby_box("Walkway Near (door-end, removable)", x0, 0, full_z,
                 liftout_x - x0, ov.WALKWAY_W, t, color=ov.C_REMOVABLE),
        ruby_box("Walkway Near (partial)", liftout_x, 0, full_z,
                 PARTIAL_X - liftout_x, ov.WALKWAY_W, t, color=ov.C_WALKWAY),
        ruby_box("Walkway Far (partial)", x0, ov.WALKWAY_FAR_YD, full_z,
                 w, ov.WALKWAY_W, t, color=ov.C_WALKWAY),
    ])


def film_plane_left():
    """LEFT (cargo-door) end of the film-plane rail mechanism. The left RAIL PAIR (TL+BL,
    X=RAIL_X_L) is REMOVABLE for transport — it lifts straight up out of drop-in U-saddles
    (shelf + cheeks + tapered datum dowel + clamp bar) at each end so the swinging drum cage
    can transition the X=150 rail plane, then re-seats to the film datum. The brace-cage
    beams (upper+lower, run to the container/walkway far extent) + the near-wall corner post
    stay; the FAR post is the Ø89 pivot (the original 50×50 far post is struck post-build)."""
    rail = 40
    s = ov.BRACE_RHS                            # 50
    xL = ov.RAIL_X_L                            # 150
    z_bot = ov.RAIL_OFF                         # 100
    z_top = ov.C_HGT - ov.RAIL_OFF - rail       # 2248
    yN, yF = ov.FP_Y_MIN, ov.FP_Y               # 100, 2262
    blen = WALL_FAR - xL                         # beams run X150..WALL_FAR (match container/walkway)
    C = ov.C_STEEL
    parts = [
        ruby_box("FP Rail BL (lower left)", xL, yN, z_bot, rail, yF - yN, rail, color=C),
        ruby_box("FP Rail TL (upper left)", xL, yN, z_top, rail, yF - yN, rail, color=C),
    ]
    for py, pn in [(yN, "near wall"), (yF, "far wall")]:
        parts.append(ruby_box(f"FP Brace Beam Lower ({pn})", xL, py, z_bot, blen, s, s, color=C))
        parts.append(ruby_box(f"FP Brace Beam Upper ({pn})", xL, py, z_top, blen, s, s, color=C))
        parts.append(ruby_box(f"FP Brace Post L ({pn})", xL, py, z_bot, s, s, z_top - z_bot, color=C))
    for ys in (yN, yF - 80):                     # drop-in saddles just inside each rail end
        parts.append(_rail_saddle(ys, z_bot))
        parts.append(_rail_saddle(ys, z_top))
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
    # Fixed subsystems (do NOT swing). Context reaches WALL_FAR so the near wall carries
    # the transport-stay anchor (X≈1694, beyond the PARTIAL_X tray/walkway crop).
    static_comps = [
        component("Context", "Context", context(x_far=WALL_FAR)),
        # include_seal=False — the housing-surround EPDM ring is bonded to the moving
        # housing, so it must NOT also be drawn on the fixed frame.
        component("Fixed Door Frame", "Door Frame", door_frame(include_seal=False)),
        component("Pivot Axle (Ø89 post + bearings)", "Pivot Axle", axle()),
        component("Fixed left panel", "Near Leaf", near_leaf()),
        component("Fixed far strip", "Far Leaf", far_leaf()),
        component("Processing Tray (partial)", "Processing Tray", processing_tray_partial()),
        component("Walkways (near + far, partial)", "Walkways", walkways_partial()),
        component("Film-Plane Rails (left, removable)", "Film Plane Rails", film_plane_left()),
        component("Transport stay wall anchors", "Lock anchor", wall_anchors()),
    ]
    static_body = '\n'.join(static_comps)

    # Moving assembly → the Panel Swing DC. Everything that swings lives here: the SPLIT
    # panel (trimmed to PANEL_CUT..PIVOT, the corners/full seals erased below) + bay +
    # housing + drum cage + Fan B + the moving hub + stay hooks.
    dc_body = '\n'.join([
        hinge_panel(),
        ruby_box(f"Panel near (swing, Yd{CUT}-{NEW_YD_L})", 0, CUT, PANEL_Z_BOT, 40,
                 NEW_YD_L - CUT, PANEL_Z_TOP - PANEL_Z_BOT, color=C_PLY),
        ruby_box("EPDM seal top (trimmed)", -20, CUT, PANEL_Z_TOP - 40, 20, PIVOT_YD - CUT, 40, color=C_GASKT),
        ruby_box("EPDM seal bottom L (trimmed)", -20, CUT, PANEL_Z_BOT, 20,
                 (DRUM_CY - HOUSING_R - 15) - CUT, 40, color=C_GASKT),
        ruby_box("Panel far corner (trimmed)", 0, NEW_YD_R, PANEL_Z_BOT, 40,
                 PIVOT_YD - NEW_YD_R, PANEL_Z_TOP - PANEL_Z_BOT, color=C_PLY),
        ruby_box("EPDM seal bottom R (trimmed)", -20, DRUM_CY + HOUSING_R + 15, PANEL_Z_BOT, 20,
                 PIVOT_YD - (DRUM_CY + HOUSING_R + 15), 40, color=C_GASKT),
        bay(),
        drum_housing(DRUM_CX, DRUM_CY),   # housing + rotor are static geometry in the swing
        drum_rotor(DRUM_CX, DRUM_CY),     # def, so they swing rigidly at the correct position
        drum_frame(),
        fan_b(),
        pivot_link(),
        frame_hooks(),
    ])

    # Cargo-door leaves (local-origin geometry for the swing DC). NB renamed to avoid
    # colliding with the near_leaf()/far_leaf() PANEL builders above.
    door_near = door_leaf_local("near")
    door_far = door_leaf_local("far")
    cwid = ov.C_WID

    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Light Trap (dynamic swing)", true)
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

# Strike the original 50×50 far brace post — the Ø89 pivot post replaces it.
fpdef = model.definitions.to_a.find {{ |d| d.name =~ /Film-Plane Rails/ }}
fpdef.entities.grep(Sketchup::Group).each {{ |g| g.erase! if g.name =~ /FP Brace Post L .far wall./ }} if fpdef

# ═══ Panel Swing — DYNAMIC COMPONENT (the swinging assembly) ═══
# Interact tool → click to ANIMATE the panel 0→{LOCK}° about the vertical pivot. The whole
# assembly (panel + bay + housing + drum rotor + cage + Fan B + hub) is STATIC geometry in
# this def — it all swings rigidly as one. (The old nested drum-revolve DC reset its own
# position on redraw, so the rotor is now baked into the swing assembly at the correct place.)
defn = model.definitions.add("Panel Swing")
ents = defn.entities
{dc_body}
# Trim to the 3-zone split: erase the un-split corners + full-width seals + piano hinges
# (the fixed left/far leaves + the trimmed swing seals provide the rest).
defn.entities.grep(Sketchup::Group).select {{ |g| g.name =~ /Panel near corner|Panel far corner .40mm.|EPDM seal left|EPDM seal right|EPDM seal bottom L$|EPDM seal bottom R$|EPDM seal top$|Piano hinge/ }}.each {{ |g| g.erase! }}

# Shift the moving def by -pivot so the def origin sits at the pivot — then the instance's
# RotZ swings the assembly about the pivot (same origin-at-rotation-point pattern the
# cargo-door leaves use).
shift = Geom::Transformation.translation([(-{PIVOT_X}).mm, (-{PIVOT_YD}).mm, 0])
defn.entities.transform_entities(shift, defn.entities.to_a)

inst = entities.add_instance(defn, Geom::Transformation.translation([{PIVOT_X}.mm, {PIVOT_YD}.mm, 0]))
inst.name = "Panel Swing"
inst.layer = model.layers["Panel Swing"]
da = "dynamic_attributes"
[defn, inst].each do |e|
  e.set_attribute(da, "_name", "PanelSwing")
  e.set_attribute(da, "_lengthunits", "MILLIMETERS")
  e.set_attribute(da, "swing", 0.0)
end
inst.set_attribute(da, "_swing_access", "VIEW")
inst.set_attribute(da, "_swing_label", "Swing")
inst.set_attribute(da, "rotz", 0.0)
inst.set_attribute(da, "_rotz_formula", "{LOCK}*swing")
inst.set_attribute(da, "onclick", 'ANIMATE("swing", 0, 1)')
inst.set_attribute(da, "_onclick_access", "NONE")
dc_inst = inst

# ═══ Cargo Doors — DYNAMIC COMPONENT (click to close) ═══
# Parent "Cargo Doors" holds two leaf children whose RotZ is driven by the
# parent's "shut" attribute (0 = open / ±180°, 1 = closed / 0°). Click the parent
# with the Interact tool → ANIMATE shut 0↔1 swings both leaves together.
doors_defn = model.definitions.add("Cargo Doors")
doors_ents = doors_defn.entities

near_defn = model.definitions.add("Cargo Door Leaf Near")
ents = near_defn.entities
{door_near}
near_inst = doors_ents.add_instance(near_defn, Geom::Transformation.translation([{DOOR_HINGE_X}.mm, 0, 0]))
near_inst.name = "Leaf Near"

far_defn = model.definitions.add("Cargo Door Leaf Far")
ents = far_defn.entities
{door_far}
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

# ── Camera + scenes (the swing is interactive; plus a "Labeled" callout scene) ──
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
page = model.pages.add("Light Trap — click panel to swing")
page.use_camera = true
# Labeled — same view + component callouts.
model.layers["Labels"].visible = true if model.layers["Labels"]
lpage = model.pages.add("Labeled"); lpage.use_camera = true
model.layers["Labels"].visible = false if model.layers["Labels"]

model.commit_operation

# Register the DC attributes with the Dynamic Components engine so the Interact tool
# drives the swing (skipped if the extension isn't loaded).
dc_ready = false
if defined?($dc_observers) && $dc_observers.respond_to?(:get_latest_class)
  cls = $dc_observers.get_latest_class
  if cls
    [dc_inst, doors_inst].each {{ |di| cls.redraw_with_undo(di) rescue nil }}
    dc_ready = true
  end
end

{{ success: true, model: "Light Trap (dynamic swing)",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   dynamic_engine: dc_ready, swing_deg: {LOCK},
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
