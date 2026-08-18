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

Geometry comes from hinged-panel-report.md and
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
PANEL_CORNER_T = ov.PANEL_CORNER_T            # corner-zone thickness (report §2.1)
PANEL_FLOOR_GAP = ov.PANEL_FLOOR_GAP          # 130 (rev: +50 walkway raise)
YD_L, YD_R = ov.PANEL_CORNER_YD_L, ov.PANEL_CORNER_YD_R   # 653, 1709 step lines
FAN_B_YD, FAN_B_H = ov.FAN_B_YD, ov.FAN_B_H

C_STEEL, C_ALUM, C_PLY = ov.C_STEEL, ov.C_ALUM, ov.C_PLY
C_PLASTIC = ov.C_PLASTIC                       # 1/8″ HDPE panel skins + bay (rev11; C_PLY now = wood fan band only)
C_DRUM, C_GASKT, C_RAIL, C_CARR = ov.C_DRUM, ov.C_GASKT, ov.C_RAIL, ov.C_CARR
# Seal geometry renders GREEN so it's never mistaken for the steel-grey structure — in TWO
# shades so the two seal TYPES read distinctly from each other:
#   C_SEAL  (medium green) = the top/bottom BRUSH seals — the panel edge SWEEPS THROUGH them.
#   C_GASKT (dark green)   = the EPDM compression seals that STAY (panel perimeter left/right,
#                            the vertical cut seals, and the housing-surround ring).
# (The door-frame top/bottom seal LIPS were formerly C_RAIL steel-grey, which read as structure
# and made a clash inspection ambiguous, 2026-07-18.)
# DELIBERATE OVERLAP: the panel + drum-box top edge intentionally overlaps the top brush seal
# ~30mm and sweeps THROUGH it as the panel swings — a brush, not a compression EPDM (which would
# drag under the sideways sweep). The overlap is by design; do not "fix" it.
C_SEAL  = "#2FA84F"   # top/bottom brush seals
C_GASKT = "#14532D"   # EPDM compression seals (perimeter / cut / housing)
C_SHELL, C_VALVE = ov.C_SHELL, ov.C_VALVE

PANEL_Z_BOT = PANEL_FLOOR_GAP                 # 80 — bottom edge (floor gap)
PANEL_Z_TOP = 2300                            # panel top edge (swings about the Ø89 pivot post)

# ── Option A — housed revolving-door light lock (Ø900 balanced) ───────────────
# Fixed housing with two opposed 80° openings (exterior + interior-onto-walkway,
# 180° apart) + a single-opening C-shell drum rotating inside. Openings <90° so
# the drum opening can never bridge both at once → light-tight at all rotations.
# All dimensions come from tbs_constants (via ov) — single source of truth.
HOUSING_R = ov.LT_HOUSING_R           # 450 — fixed housing radius (Ø900 OD)
HOUSING_T = ov.LT_HOUSING_T           # 3 — housing wall
DRUM_OR = ov.LT_DRUM_OR               # 432 — drum outer radius (Ø864), 15mm gap
DRUM_T = ov.LT_DRUM_T                 # 3 — drum wall → ~Ø850 bore, ~555mm passage
DRUM_CAP_T = ov.LT_CAP_T              # 4.76 — 3/16" HDPE end caps (structural: carry the stub shafts into the bearings)
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
STAY_Z = (500, 2050)                               # bottom + top transport-stay heights
# (bottom raised 200→350→500: its anchor plate (Z400–600, X1614–1814) sits LEFT of the EP
#  column/battery (X1829–2159, stacked Z160–604 on the pinhole wall) and clears the walkway
#  deck (Z140) + the wall-cantilever brackets (vertical leg to Z150 std / Z200 widened) it sits over.
#  The 2050↔500 couple arm (1550mm) is still ample for the transport stay.)
LOCK_BOLT = (20, CUT + 25)                         # stay hook on the swinging frame's LEFT
# perimeter 50×50 RHS STILE (Yd≈205, centred on the stile at the swing cut) — STEEL load
# path, not the 1/8″-HDPE skin. Relocated from the mid-corner (Yd350, which the rev11 plastic
# skin left unbacked above the Z1125 ply band); the stile is also the farthest point from
# the pivot (FAR0=2287) → best lever arm for the transport-stay couple.


def _rot_pt(x, y, deg):
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    return PIVOT_X + (x - PIVOT_X) * c - (y - PIVOT_YD) * s, PIVOT_YD + (x - PIVOT_X) * s + (y - PIVOT_YD) * c


SOCKET = _rot_pt(LOCK_BOLT[0], LOCK_BOLT[1], LOCK)  # transport position of the frame hook (1814, 994)

TAGS = ["Context", "Door Frame", "Pivot Axle",
        "Processing Tray", "Walkways", "Film Plane Rails",
        "Near Leaf", "Far Leaf", "Lock anchor", "Panel skin",
        "Panel Swing",        # dynamic-component moving group (the swinging assembly)
        "Fan B",              # Fan B body/duct/ply band — taggable so scenes can hide it
        "Drum shell",         # Ø900 housing arcs + rotating C-shell — taggable for hiding
        "Cargo Doors",        # dynamic-component swing doors (click to close)
        "Fan B Cable",        # child DC: orange coil shown only when the door is closed
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
    # Roof (ceiling) + both side walls REMOVED (2026-08-11) — they boxed in the corner mechanism and
    # made orbiting awkward. Keep only the floor as a ground reference; the corner clash detail reads open.
    parts = [
        ruby_box("Floor (context)", x0, 0, -WALL_T, xlen, C_WID, WALL_T,
                 color=C_SHELL, alpha=0.25),
    ]
    # The left walkway + drum-exit punch-out (the amber lift-out decks) are now built by
    # liftout_walkways() as a CHILD of the Panel Swing DC so they HIDE when the panel
    # swings open (lifted out for transport). `left_walkway` is retained for the API.
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
    hz0, hz1 = PANEL_FLOOR_GAP, DRUM_H     # housing footprint Z (130..2250)
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


def _brush_bristles(z0, zlen, n=176):
    """Thin near-black vertical bristle lines annotating a top/bottom strip-brush seal across
    the door-frame width (Z=z0..z0+zlen), drawn on BOTH long faces of the 12mm strip — outer
    face (X≈-32) and inner/panel face (X≈-20) — so the green seal strip reads as a brush the
    panel edge sweeps through. n lines per face → 2n total."""
    step = C_WID / n
    out = []
    for i in range(n):
        y = step * (i + 0.5)
        out.append(ruby_box("Brush bristle", -33, y, z0, 2, 2, zlen, color="#141414"))  # outer face
        out.append(ruby_box("Brush bristle", -21, y, z0, 2, 2, zlen, color="#141414"))  # inner face
    return out


def door_frame(include_seal=True):
    """2×2×0.120in steel SHS welded frame lining the cargo-door opening at X≈0. Sits
    just exterior of the panel (X=-50.8..0); the EPDM gasket seals against it. #26: was
    50×50×3 nominal — re-specced to 2in stock (the same sp-door-frame-rhs the parts registry carries).

    include_seal: append the interface-2 housing-surround EPDM ring (default True
    = operating; byte-identical). The transport model passes False and rebuilds
    that ring on the MOVING housing instead, so the seal retracts with it."""
    s = 50.8
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
    # Bottom BRUSH seal — a filament strip on the frame (X=-32..-20) rising from the
    # threshold to just above the panel bottom edge (Z=110). It closes the 80mm floor gap
    # as a light-tight bristle wall the panel bottom edge SWEEPS THROUGH as the panel swings
    # (a compression EPDM would drag under the sideways sweep). Now that the drum is
    # SUSPENDED (its bottom hangs at Z=80, not on the floor), the floor gap is uniform
    # full-width, so this brush runs CONTINUOUS with no notch — like the top.
    lt, lz = 12, 110
    parts.append(ruby_box("Door Frame bottom brush seal", -20 - lt, 0, 0,
                          lt, C_WID, lz, color=C_SEAL))
    parts.extend(_brush_bristles(40, 70))          # bristles rise to the panel bottom edge
    # Top BRUSH seal — the mirror of the bottom: a filament strip on the frame top rail
    # reaching to just below the panel top edge (Z=2270). It closes the panel-top↔frame gap
    # as a light-tight bristle wall the panel + drum-box top edge SWEEPS THROUGH as the panel
    # swings. The drum shaft stops below it, so the brush runs the FULL width as one
    # continuous member — no notch — and meets across the center.
    tz0 = PANEL_Z_TOP - 30                 # 2270 — brush reaches 30mm past panel top; the panel +
                                           # drum-box top edge DELIBERATELY overlaps this ~30mm
                                           # (sweeps THROUGH the bristles, not a clash — see C_SEAL note)
    th = C_HGT - tz0                       # up to the frame top / ceiling
    parts.append(ruby_box("Door Frame top brush seal", -20 - lt, 0, tz0,
                          lt, C_WID, th, color=C_SEAL))
    parts.extend(_brush_bristles(2270, 70))        # bristles hang down to the panel top edge

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
                          0, 0, PANEL_Z_BOT, tc, NEW_YD_L, h, color=C_PLASTIC, alpha=0.5))
    parts.append(ruby_box("Panel far corner (40mm)",
                          0, NEW_YD_R, PANEL_Z_BOT, tc, C_WID - NEW_YD_R, h, color=C_PLASTIC, alpha=0.5))

    # Center zone (120mm) — the structural FRAME around the housing aperture: two jambs +
    # header. Colored STEEL (vs the blue HDPE skin) so the frame reads distinctly from the
    # flat corner panels — and it's the member the interior pull handle bolts to.
    parts.append(ruby_box("Panel center jamb L (120mm frame)",
                          0, NEW_YD_L, PANEL_Z_BOT, tk, APER_L - NEW_YD_L, h, color=C_STEEL))
    parts.append(ruby_box("Panel center jamb R (120mm frame)",
                          0, APER_R, PANEL_Z_BOT, tk, NEW_YD_R - APER_R, h, color=C_STEEL))
    parts.append(ruby_box("Panel header over housing (120mm frame)",
                          0, NEW_YD_L, DRUM_H, tk, NEW_YD_R - NEW_YD_L,
                          PANEL_Z_TOP - DRUM_H, color=C_STEEL))

    # (Housing-aperture neoprene lining strips omitted in this model — they read
    # as distracting brown bands flanking the drum opening.)

    # EPDM perimeter gasket — 20mm strips on the panel exterior face, compressed
    # against the door frame (and the top/bottom seal lips) by the cam latches.
    gw, gt = 40, 20
    z0, z1 = PANEL_Z_BOT, PANEL_Z_TOP
    dg0, dg1 = DRUM_CY - HOUSING_R - 15, DRUM_CY + HOUSING_R + 15  # clear housing aperture
    # bottom + top strips run on the panel edges, notched around the housing
    parts.append(ruby_box("EPDM seal bottom L", -gt, 0, z0, gt, dg0, gw, color=C_GASKT, alpha=0.5))
    parts.append(ruby_box("EPDM seal bottom R", -gt, dg1, z0, gt, C_WID - dg1, gw,
                          color=C_GASKT, alpha=0.5))
    # top strip runs continuously full-width (panel top edge is the solid header)
    parts.append(ruby_box("EPDM seal top", -gt, 0, z1 - gw, gt, C_WID, gw, color=C_GASKT, alpha=0.5))
    parts.append(ruby_box("EPDM seal left", -gt, 0, z0, gt, gw, z1 - z0, color=C_GASKT, alpha=0.5))
    parts.append(ruby_box("EPDM seal right", -gt, C_WID - gw, z0, gt, gw, z1 - z0,
                          color=C_GASKT, alpha=0.5))

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

    # Interior pull handle (matte-black 316 SS D-grab) — through-bolted to the panel's
    # structural FRAME: the left drum-aperture jamb (the 120mm center-zone stud just left
    # of the Ø900 housing), NOT the 1/8″ HDPE skin. Mounted on the interior face. The transport
    # swing pivots on the FAR edge, so this near-of-center jamb keeps good leverage while
    # landing the load on steel right beside the drum (report §4.3).
    hy = (NEW_YD_L + APER_L) // 2                         # ≈683 — center of the left drum jamb
    hz0, hz1 = 1150, 1450
    xf = PANEL_CENTER_T                                   # 120 — interior face of the frame zone
    for hz in (hz0 + 18, hz1 - 18):                       # two standoff posts off the frame face
        parts.append(ruby_box("Pull-handle standoff", xf, hy - 10, hz - 8, 28, 20, 16,
                              color="#202020"))
    parts.append(ruby_box("Pull-handle grip (matte black)", xf + 28, hy - 12, hz0,
                          24, 24, hz1 - hz0, color="#202020"))
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
    # interior 0°). Suspended: spans Z 130..2250 (bottom at the panel bottom rail).
    parts.append(ov.ruby_arc_wall("LT Housing arc (near Yd)", cx, cy, HOUSING_R,
                                  HOUSING_T, H - ZB, gap_center_deg=270, gap_deg=180 + od,
                                  color=C_ALUM, alpha=0.5, z0=ZB))
    parts.append(ov.ruby_arc_wall("LT Housing arc (far Yd)", cx, cy, HOUSING_R,
                                  HOUSING_T, H - ZB, gap_center_deg=90, gap_deg=180 + od,
                                  color=C_ALUM, alpha=0.5, z0=ZB))
    parts.append(ruby_cylinder("LT Upper bearing (SKF 6215)", cx, cy, H, 65, 25,
                               color=C_STEEL, axis="z"))   # Ø130 OD (r65) × 25mm B — SKF 6215 datasheet
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
                                  color=C_ALUM, alpha=0.5, z0=ZB))
    parts.append(ruby_cylinder("LT Drum top cap", cx, cy, H - DRUM_CAP_T, DRUM_OR, DRUM_CAP_T,
                               color=C_ALUM, axis="z"))
    parts.append(ruby_cylinder("LT Drum bottom cap", cx, cy, ZB, DRUM_OR, DRUM_CAP_T,
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
# Wall-anchor X: inboard of the hook's transport X, but CLAMPED so the plate right edge
# clears the electrical panel (EP) on the same pinhole wall — the relocated top stay
# (hooks on the perimeter stile) would otherwise overlap the EP left edge by a few mm.
# The small resulting rod angle (~1°) the turnbuckle stay absorbs. Shared by stay_rods().
ANCHOR_X = min(SOCKET[0], ov.EP_X - PLATE_HW - 15)   # ≤1714 → plate right edge ≤1814 < EP 1829


def wall_anchors():
    hx = ANCHOR_X
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


# Transport STAY RODS — the M16 turnbuckle stays themselves (top + bottom), drawn in the
# TRANSPORT (swung) pose: a straight rod from each frame hook (at SOCKET) down to its wall-
# anchor eye, with a turnbuckle barrel mid-span. Built here in transport (axis-aligned along
# Yd) coords; generate_ruby adds it as a Panel-Swing DC CHILD with a -LOCK° pre-rotation so
# the parent's +LOCK°·swing cancels it at swing=1 (rod meets hook + eye exactly), and HIDES
# it until swung — the stays are engaged AFTER the swing and removed before the swing-back.
ROD_R, TURN_R = 8, 14                                 # Ø16 M16 rod, Ø28 turnbuckle barrel


def stay_rods():
    sx = ANCHOR_X                                     # rod X — hook (SOCKET[0]) & eye share this X
    y_eye = PLATE_T + 48                              # pin just past the wall eye (Yd≈60)
    y_hook = SOCKET[1] - 30                           # pin at the hook's inner face (Yd≈1045)
    cR, cT = "#8A8A92", "#6A6A72"                     # rod / turnbuckle barrel
    TURN_L = 120
    p = []
    for z in STAY_Z:
        y_barrel0 = y_eye + (y_hook - y_eye) * 0.45
        p += [
            ruby_box("Stay clevis (eye end)", sx - 12, y_eye - 18, z - 12, 24, 24, 24, color=C_STEEL),
            ruby_cylinder("Stay rod (eye side)", sx, y_eye, z, ROD_R, y_barrel0 - y_eye, color=cR, axis="y"),
            ruby_cylinder("Turnbuckle barrel", sx, y_barrel0, z, TURN_R, TURN_L, color=cT, axis="y"),
            ruby_cylinder("Stay rod (hook side)", sx, y_barrel0 + TURN_L, z, ROD_R, y_hook - (y_barrel0 + TURN_L), color=cR, axis="y"),
            ruby_box("Stay clevis (hook end)", sx - 12, y_hook, z - 12, 24, 24, 24, color=C_STEEL),
        ]
    return '\n'.join(p)


def _rail_clamp_bar(ys, z):
    """The removable clamp bar that holds a 40×40 rail end down in its U-saddle. Part of
    the LIFT-OUT — it comes out with the rail for transport, so it's built into
    liftout_film_rail() (a Panel-Swing DC child that HIDES on swing), not the static cradle."""
    return ruby_box("Rail clamp bar (removable)", 133, ys + 22, z + 40, 74, 36, 14, color="#7A7A82")


def _rail_saddle(ys, z):
    """Drop-in U-saddle CRADLE for a removable 40×40 rail end: shelf + X-side cheeks +
    tapered locating dowel (to the film datum). STAYS put — the rail + its clamp bar (the
    lift-out) come out for transport (see liftout_film_rail() / _rail_clamp_bar())."""
    c, cdowel = C_STEEL, "#9A9AA2"
    return '\n'.join([
        ruby_box("Rail saddle shelf", 133, ys, z - 14, 74, 80, 14, color=c),
        ruby_box("Rail saddle cheek -X", 133, ys, z, 12, 80, 44, color=c),
        ruby_box("Rail saddle cheek +X", 195, ys, z, 12, 80, 44, color=c),
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


def fan_b_cable():
    """Fan B flexible connector (orange curly coil) — wall plug -> Fan B on the swing panel.
    The SOFT jumper that is plugged in when the door is CLOSED and unplugged before the panel
    swings open; lives in a child DC shown only at swing≈0. Reuses the shared ov.ruby_coil_cord
    (Cct B colour), matching the overview/electrical models."""
    return ov.ruby_coil_cord("Fan B flex connector (box -> fan, Cct B)",
                             [(300, 18, FAN_B_H), (60, FAN_B_YD, FAN_B_H)],
                             r=5, color="#E67E22")


def fan_b_box():
    """Fan B electrical box (Cct B termination) on the FIXED near wall — the plug point the
    swing-gated coil cable runs to when the door is closed. It is STATIC (stays put when the
    panel swings; only the cable unplugs/hides). Matches the overview's box."""
    return ruby_box("Fan B electrical box (Cct B — flex connector to fan, unplugged for swing)",
                    260, 0, FAN_B_H - 45, 80, 60, 90, color=ov.C_SWITCH)


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
    zc = ov.tray_floor_z(x0 + w / 2, (yN + yF) / 2)      # representative RAISED floor top at the cargo-door end
    return '\n'.join([
        ruby_box("Tray Shim Base (partial)", x0, yN, 0, w, d, zc - st, color="#D8CFBC", alpha=0.6),
        ruby_box("Processing Tray Floor (partial)", x0, yN, zc - st, w, d, st, color=ov.C_TRAY),
        ruby_box("Tray Rim Near (partial)", x0, yN, zc, w, rt, rim - st, color=ov.C_TRAY),
        ruby_box("Tray Rim Far (partial)", x0, yF - rt, zc, w, rt, rim - st, color=ov.C_TRAY),
        ruby_box("Tray Rim Left (cargo end)", x0, yN, zc, rt, d, rim - st, color=ov.C_TRAY),
        ruby_box("Chemistry Bath (partial)", x0 + rt, yN + rt, zc,
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
    liftout_x = ov.WALKWAY_NEAR_LIFTOUT_X_R      # 950 — door-end band end (sweep X≈896 + 50mm)
    w = PARTIAL_X - x0
    return '\n'.join([
        # (the door-end lift-out band moved to liftout_walkways() — a Panel Swing DC child
        #  that hides on swing; only the FIXED partial decks stay here)
        ruby_box("Walkway Near (partial)", liftout_x, 0, full_z,
                 PARTIAL_X - liftout_x, ov.WALKWAY_W, t, color=ov.C_WALKWAY),
        ruby_box("Walkway Far (partial)", x0, ov.WALKWAY_FAR_YD, full_z,
                 w, ov.WALKWAY_W, t, color=ov.C_WALKWAY),
    ])


def liftout_walkways():
    """The amber REMOVABLE lift-out decks — left walkway (full width) + drum-exit punch-out
    + the near door-end band. Built at WORLD coords; placed as a CHILD of the Panel Swing
    DC so they HIDE when the panel swings open (lifted out for the transport swing)."""
    import generate_walkway_model as wm
    t = ov.WALKWAY_GRATE_T
    full_z = ov.WALKWAY_H - t
    return '\n'.join([
        # ONE continuous lift-out piece: drum-exit punch-out tab + muslin notch both integral.
        ov.left_liftout_grate("Left walkway (removable)", full_z, t, ov.C_REMOVABLE, alpha=0.6),
        # door-end removable near band — OWNED by the walkway model (wm), ghosted here as context
        # (was a copy that drew it full-width, not bracket-inset like the real deck).
        wm.near_removable_deck(alpha=0.6),
    ])


def film_plane_left():
    """LEFT (cargo-door) end of the film-plane corner mechanism — the STATIC parts that STAY, reused
    verbatim from the dedicated model (fpm.corner(..., keep='fixed')): the fixed parking STUB + the
    detailed skate/rollers + carriage plate + cam-brake + green-Z/purple-X cross-slides + U-joint + 304
    corner plate + pinhole-wall gusset + length splice. The REMOVABLE rail section + its welded bridge
    are the LIFT-OUT — built by liftout_film_rail() (keep='removable') as a Panel-Swing DC child that
    HIDES when swung, so the swinging drum surround can transition the X=150 rail plane in transport.
    One source with overview (fpm.corner emits ov.ruby_* at the shared coords; late import breaks the cycle)."""
    import generate_film_plane_mechanism_model as fpm
    return '\n'.join([
        fpm.corner("BL", fpm.X_L, fpm.PZ0, fpm.PZ_HB_BOT, +1, "L", keep="fixed"),
        fpm.corner("TL", fpm.X_L, fpm.PZ1, fpm.PZ_HB_TOP, +1, "L", keep="fixed"),
    ])


def liftout_film_rail():
    """The REMOVABLE left film-plane rail — the LIFT-OUT: the detailed removable U-channel rail section +
    its welded bridge, reused from the dedicated model (fpm.corner(..., keep='removable')) so it matches
    film-plane-mechanism.skp. Placed as a CHILD of the Panel Swing DC so it HIDES when the panel swings
    open (removed for the transport swing) — the same child-DC + hidden-formula pattern as the lift-out
    walkways. As a swing child it also rides rigidly with the drum surround through the animation."""
    import generate_film_plane_mechanism_model as fpm
    return '\n'.join([
        fpm.corner("BL", fpm.X_L, fpm.PZ0, fpm.PZ_HB_BOT, +1, "L", keep="removable"),
        fpm.corner("TL", fpm.X_L, fpm.PZ1, fpm.PZ_HB_TOP, +1, "L", keep="removable"),
    ])


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
        ruby_box("Bay wall near (Yd)", xf, yL, z0, depth, t, h, color=C_PLASTIC, alpha=0.5),
        ruby_box("Bay wall far (Yd)", xf, yR - t, z0, depth, t, h, color=C_PLASTIC, alpha=0.5),
        ruby_box("Bay wall top", xf, yL, z1 - t, depth, yR - yL, t, color=C_PLASTIC, alpha=0.5),
        ruby_box("Bay wall bottom", xf, yL, z0, depth, yR - yL, t, color=C_PLASTIC, alpha=0.5),
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
        component("Fan B electrical box", "Fan B Cable", fan_b_box()),
    ]
    static_body = '\n'.join(static_comps)

    # Moving assembly → the Panel Swing DC. Everything that swings lives here: the SPLIT
    # panel (trimmed to PANEL_CUT..PIVOT, the corners/full seals erased below) + bay +
    # housing + drum cage + Fan B + the moving hub + stay hooks.
    dc_body = '\n'.join([
        hinge_panel(),
        # Fan B corner: 18mm PLYWOOD mount band (bottom up to PANEL_FAN_BAND_Z) for
        # rigid fan/duct mounting; 1/8″ HDPE skin above. (rev11 material differentiation.)
        ruby_box("Fan B mount band (18mm ply)", 0, CUT, PANEL_Z_BOT, 40,
                 NEW_YD_L - CUT, ov.PANEL_FAN_BAND_Z - PANEL_Z_BOT, color=C_PLY, alpha=0.5),
        ruby_box(f"Panel near (swing, Yd{CUT}-{NEW_YD_L})", 0, CUT, ov.PANEL_FAN_BAND_Z, 40,
                 NEW_YD_L - CUT, PANEL_Z_TOP - ov.PANEL_FAN_BAND_Z, color=C_PLASTIC, alpha=0.5),
        ruby_box("EPDM seal top (trimmed)", -20, CUT, PANEL_Z_TOP - 40, 20, PIVOT_YD - CUT, 40, color=C_GASKT, alpha=0.5),
        ruby_box("EPDM seal bottom L (trimmed)", -20, CUT, PANEL_Z_BOT, 20,
                 (DRUM_CY - HOUSING_R - 15) - CUT, 40, color=C_GASKT, alpha=0.5),
        ruby_box("Panel far corner (trimmed)", 0, NEW_YD_R, PANEL_Z_BOT, 40,
                 PIVOT_YD - NEW_YD_R, PANEL_Z_TOP - PANEL_Z_BOT, color=C_PLASTIC, alpha=0.5),
        ruby_box("EPDM seal bottom R (trimmed)", -20, DRUM_CY + HOUSING_R + 15, PANEL_Z_BOT, 20,
                 PIVOT_YD - (DRUM_CY + HOUSING_R + 15), 40, color=C_GASKT, alpha=0.5),
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

    sf_meta = ov.sketchfab_meta_ruby(
        "TBS-001 Lighttrap Model",
        "Personnel access during operation is via a revolving light trap drum built into the panel. "
        "Operators can enter or exit at any time without opening the full panel or admitting daylight "
        "— for example, between coating of the photosensitive material, or while the exposure is being made.",
        ov.model_uid("lighttrap"), "sketchup")

    return f'''# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
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

{sf_meta}
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

# ── Lift-out walkways — a CHILD DC component inside the swing def: HIDDEN when the panel
#    swings (lifted out for transport). Built at world coords, then shifted with the rest
#    of the def below so the instance's +pivot translate restores the world position. The
#    child's `_hidden_formula` reads the parent Panel Swing's `swing` attribute. ──
lw_defn = model.definitions.add("Lift-out Walkways")
ents = lw_defn.entities
{liftout_walkways()}
ents = defn.entities
lw_inst = ents.add_instance(lw_defn, Geom::Transformation.new)
lw_inst.name = "Lift-out Walkways"
lw_inst.layer = model.layers["Walkways"]
lw_inst.set_attribute("dynamic_attributes", "_name", "LiftoutWalkways")
lw_inst.set_attribute("dynamic_attributes", "hidden", 0.0)
lw_inst.set_attribute("dynamic_attributes", "_hidden_formula", "PanelSwing!swing>0.5")

# ── Transport stay rods — a CHILD DC component inside the swing def: SHOWN only when the
#    panel is swung open (the M16 turnbuckle stays are engaged AFTER the swing). Built in
#    TRANSPORT (swung) coords, then added with a -LOCK° pre-rotation about the pivot so the
#    parent's +LOCK°·swing cancels it at swing=1 → the rod lands exactly on the frame hook
#    (which also swings to SOCKET) and the static wall-anchor eye. A child, so its
#    `_hidden_formula` (ancestor ref PanelSwing!swing) re-evaluates as the panel animates. ──
sr_defn = model.definitions.add("Transport Stay Rods")
ents = sr_defn.entities
{stay_rods()}
ents = defn.entities
sr_tr = Geom::Transformation.rotation([{PIVOT_X}.mm, {PIVOT_YD}.mm, 0], Z_AXIS, (-{LOCK}).degrees)
sr_inst = ents.add_instance(sr_defn, sr_tr)
sr_inst.name = "Transport Stay Rods"
sr_inst.layer = model.layers["Lock anchor"]
sr_inst.set_attribute("dynamic_attributes", "_name", "TransportStayRods")
sr_inst.set_attribute("dynamic_attributes", "hidden", 1.0)
sr_inst.set_attribute("dynamic_attributes", "_hidden_formula", "PanelSwing!swing<0.5")

# ── Fan B flexible connector — a CHILD DC component inside the swing def: SHOWN when the
#    door is CLOSED (plugged in), HIDDEN when the panel swings open (the jumper is unplugged
#    before transport). Built at world (closed) coords; the orange coil follows Fan B and
#    hides past swing 0.5. Same child-DC + hidden-formula pattern as the lift-out walkways. ──
fbc_defn = model.definitions.add("Fan B Cable")
ents = fbc_defn.entities
{fan_b_cable()}
ents = defn.entities
fbc_inst = ents.add_instance(fbc_defn, Geom::Transformation.new)
fbc_inst.name = "Fan B Cable"
fbc_inst.layer = model.layers["Fan B Cable"]
fbc_inst.set_attribute("dynamic_attributes", "_name", "FanBCable")
fbc_inst.set_attribute("dynamic_attributes", "hidden", 0.0)
fbc_inst.set_attribute("dynamic_attributes", "_hidden_formula", "PanelSwing!swing>0.5")

# ── Lift-out film rail — a CHILD DC component inside the swing def: HIDDEN when the panel
#    swings (the removable left rail pair + clamp bars are lifted out for transport, clearing
#    the X=150 rail plane for the swinging drum surround). Built at world coords; same child-DC
#    + hidden-formula pattern as the lift-out walkways. As a swing child it also rides rigidly
#    with the surround through the animation, so it never sweeps into it. ──
lfr_defn = model.definitions.add("Lift-out Film Rail")
ents = lfr_defn.entities
{liftout_film_rail()}
ents = defn.entities
lfr_inst = ents.add_instance(lfr_defn, Geom::Transformation.new)
lfr_inst.name = "Lift-out Film Rail"
lfr_inst.layer = model.layers["Film Plane Rails"]
lfr_inst.set_attribute("dynamic_attributes", "_name", "LiftoutFilmRail")
lfr_inst.set_attribute("dynamic_attributes", "hidden", 0.0)
lfr_inst.set_attribute("dynamic_attributes", "_hidden_formula", "PanelSwing!swing>0.5")

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

{ov.license_note()}

model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier generator versions ──
keep_tags = {keep_tags_ruby}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

# ── Tag the Panel Swing's skin / EPDM-seal / Fan-B sub-parts onto hideable tags (they
#    default to the always-on untagged layer, so the "Handle · Frame · Pivot" scene can't
#    drop them otherwise). The frame jambs/header, handle, hinges, latches, drum stay. ──
ps_defn = model.definitions["Panel Swing"]
if ps_defn
  skin_l = model.layers["Panel skin"]
  fan_l  = model.layers["Fan B"]
  drum_l = model.layers["Drum shell"]
  ps_defn.entities.grep(Sketchup::Group).each do |g|
    nm = g.name.to_s
    if nm.include?("corner") || nm.include?("near (swing") || nm.include?("EPDM") || nm.include?("Bay wall") || nm.include?("mount band")
      g.layer = skin_l if skin_l
    elsif nm.include?("Fan B")
      g.layer = fan_l if fan_l
    elsif nm.include?("C-shell") || nm.include?("Housing arc")
      g.layer = drum_l if drum_l
    end
  end
end

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
# Overview — main interactive scene (Labels OFF), listed first.
page = model.pages.add("Overview")
page.use_camera = true

# ── "Handle · Frame · Pivot" scene — isolate the swinging panel (frame + interior pull
#    handle) and the Ø89 pivot post, hiding the container/tray/walkway clutter so the
#    handle-to-frame mounting reads clearly. Per-page tag visibility is captured on add. ──
hf_keep = ["Door Frame", "Pivot Axle", "Panel Swing"]
model.layers.each {{ |l| l.visible = false }}
hf_keep.each {{ |n| model.layers[n].visible = true if model.layers[n] }}
# drum panels + the blue/brown panel skins stay visible here at 50% opacity for context
# (Fan B stays hidden); the steel frame + handle read solid on top.
model.layers["Drum shell"].visible = true if model.layers["Drum shell"]
model.layers["Panel skin"].visible = true if model.layers["Panel skin"]
# 3/4 view from the interior side (high X), near-Yd corner, slightly above — sets the
# viewing DIRECTION; the zoom-to-fit below then frames it (the old fixed eye read zoomed-out).
hf_eye = Geom::Point3d.new(3200, 250, 1950)
hf_tgt = Geom::Point3d.new(120, 1150, 1080)
model.active_view.camera = Sketchup::Camera.new(hf_eye, hf_tgt, Z_AXIS)
hf_focus = model.entities.grep(Sketchup::ComponentInstance).select {{ |i|
  hf_keep.include?(i.layer.name) }}
model.active_view.zoom(hf_focus) unless hf_focus.empty?   # fit the isolated panel + pivot
model.active_view.zoom(0.9)                               # small margin around the assembly
hfpage = model.pages.add("Handle · Frame · Pivot"); hfpage.use_camera = true
model.layers.each {{ |l| l.visible = true }}      # restore for the default state
model.layers["Labels"].visible = false if model.layers["Labels"]

# Labeled — Overview view + component callouts, listed LAST (project rule: every .skp gets a Labeled scene).
model.active_view.zoom_extents
model.active_view.zoom(0.62)
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
