#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_lighttrap_model.py — Generate Ruby for the TBS-001 "Light Trap"
focus model (models/lighttrap.skp).

A detailed, report-accurate model of the cargo-door end assembly only:
  - the revolving light-trap DRUM (caps, stub shafts, SKF bearings, pull handle),
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
# metal-cap / rim-angle constants imported directly (ov re-exports the rest); keeps this
# model self-contained so a lighttrap re-send doesn't force an edit to the plumbing-bearing
# generate_sketchup_model.py (which would trip the interference-report gate).
from tbs_constants import LT_CAP_TOP_T, LT_CAP_OD, LT_RIM_LEG, LT_RIM_T, LT_EDGE_CHAN_LEG, LT_EDGE_CHAN_T, LT_WIPER_N, LT_WIPER_SPACING, LT_AXLE_BEAM_W, LT_AXLE_BEAM_H, LT_BBEAM_H, LT_BRG_STANDOFF, LT_BEAM_STANDOFF, LT_CAGE_TOP, LT_CAGE_BOT, LT_HOUSING_Z_BOT, LT_HOUSING_Z_TOP, LT_BRG_PLATE_OD, LT_BRG_PLATE_T, LT_BBEAM_Z1, LT_LBRG_Z0, LT_TOPRING_OD, LT_COLLAR_OD, LT_RIVET_PITCH, C_LT_DRUM

# ── pull in shared helpers + constants ───────────────────────────────────────
ruby_box, ruby_cylinder = ov.ruby_box, ov.ruby_cylinder
component = ov.component
C_WID, C_HGT, WALL_T = ov.C_WID, ov.C_HGT, ov.WALL_T
DRUM_CX, DRUM_CY, DRUM_R, DRUM_H = ov.DRUM_CX, ov.DRUM_CY, ov.DRUM_R, ov.DRUM_H_LT
PANEL_CENTER_T = ov.PANEL_CENTER_T            # 120 — center-zone thickness (X)
PANEL_CORNER_T = ov.PANEL_CORNER_T            # corner-zone thickness (report §2.1)
PANEL_FLOOR_GAP = ov.PANEL_FLOOR_GAP          # 130 (rev: +50 walkway raise)
from tbs_constants import PANEL_FLOOR_GAP_SIDE
from tbs_constants import DOOR_FRAME_FACE, DOOR_FRAME_DEPTH
PANEL_FLOOR_GAP_SIDE = PANEL_FLOOR_GAP_SIDE   # 195 — corner-zone stepped bottom (clears the bare walkway cantilever legs; hingepanel Sheet 16)
from tbs_constants import APRON_CAGE_GAP, APRON_IN_L, APRON_IN_R, APRON_FIX_W   # apron inner edges (12mm off the cage sides); vertical strip brushes bridge the gap; far-pivot fixed stub width
YD_L, YD_R = ov.PANEL_CORNER_YD_L, ov.PANEL_CORNER_YD_R   # 653, 1709 step lines
FAN_B_YD, FAN_B_H = ov.FAN_B_YD, ov.FAN_B_H

C_STEEL, C_ALUM, C_PLY = ov.C_STEEL, ov.C_ALUM, ov.C_PLY
C_PLASTIC = ov.C_PLASTIC                       # 1/8″ HDPE panel skins + bay (rev11; C_PLY now = wood fan band only)
C_DRUM, C_GASKT, C_RAIL, C_CARR = ov.C_DRUM, ov.C_GASKT, ov.C_RAIL, ov.C_CARR
# The two seal TYPES render in DISTINCT colors (2026-08-31, Alvin) so they can never be confused
# with each other — nor with the steel-grey structure:
#   C_SEAL  (green)  = the BRUSH seals — the panel edge SWEEPS THROUGH them.
#   C_GASKT (brown)  = the EPDM compression seals that STAY (panel perimeter left/right, the vertical
#                      cut seals, and the housing-surround ring) — the project-standard gasket brown.
# (Both were formerly two shades of GREEN, which read as one thing; brown EPDM + green brush is the
# clear split. The door-frame seal LIPS are NOT C_RAIL steel-grey — that read as structure, 2026-07-18.)
# DELIBERATE OVERLAP: the panel + drum-box top edge intentionally overlaps the top brush seal
# ~30mm and sweeps THROUGH it as the panel swings — a brush, not a compression EPDM (which would
# drag under the sideways sweep). The overlap is by design; do not "fix" it.
C_SEAL  = "#2FA84F"   # BRUSH seals (green)
C_GASKT = ov.C_GASKT  # EPDM compression seals — project-standard gasket brown (#5A3020), distinct from the green brush
C_SHELL, C_VALVE = ov.C_SHELL, ov.C_VALVE

PANEL_Z_BOT = PANEL_FLOOR_GAP                 # 80 — bottom edge (floor gap)
PANEL_Z_TOP = 2300                            # panel top edge (swings about the Ø89 pivot post)
CORNER_BOT = LT_CAGE_BOT + 50                 # 190 — corner-skin/apron split (BOTH sides): dropped from the
#   282 stepped bottom down to the bottom-beam TOP so the beam's rivets land on the fixed corner skin, not
#   the fold-down apron plywood flap (Alvin, 2026-08-31). Far side = HDPE corner; near side = Fan-B ply band.
PLY_T  = 12   # real plywood thickness (12mm exterior BC). Inset on the INTERIOR face of the 40mm frame zone.
PLY_X0 = 40 - PLY_T   # 28 — ply front face (X28..40 = interior 12mm; the 40mm frame zone stays around it)
CHAM   = PLY_T   # plywood↔plywood joint chamfer: 45° across the 12mm ply (hingepanel Sheet 17 Detail E)

# ── Option A — housed revolving-door light lock (Ø800 balanced) ───────────────
# Fixed housing with two opposed 80° openings (exterior + interior-onto-walkway,
# 180° apart) + a single-opening C-shell drum rotating inside. Openings <90° so
# the drum opening can never bridge both at once → light-tight at all rotations.
# All dimensions come from tbs_constants (via ov) — single source of truth.
HOUSING_R = ov.LT_HOUSING_R           # 400 — fixed housing radius (Ø800 OD)
HOUSING_T = ov.LT_HOUSING_T           # 5 — housing wall (UV-HDPE skin)
DRUM_OR = ov.LT_DRUM_OR               # 382 — drum outer radius (Ø764), 13mm running gap
DRUM_T = ov.LT_DRUM_T                 # 3 — drum wall → ~Ø758 bore, ~487mm passage
DRUM_CAP_T = LT_CAP_TOP_T          # 8mm 6061-T6 Al end caps (both identical; carry the bolted stub-shaft hubs into the bearings)
DRUM_CAP_R = LT_CAP_OD / 2         # 377.5 — caps nest inside the shell (shell laps over the rim)
OPENING_DEG = ov.LT_OPENING_DEG       # 80 — each opening arc (<90°)
APERTURE_R = HOUSING_R + 18           # 418 — panel aperture radius around housing
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
# skin left unbacked above the Z1225 ply band); the stile is also the farthest point from
# the pivot (FAR0=2287) → best lever arm for the transport-stay couple.


def _rot_pt(x, y, deg):
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    return PIVOT_X + (x - PIVOT_X) * c - (y - PIVOT_YD) * s, PIVOT_YD + (x - PIVOT_X) * s + (y - PIVOT_YD) * c


SOCKET = _rot_pt(LOCK_BOLT[0], LOCK_BOLT[1], LOCK)  # transport position of the frame hook (1814, 994)

TAGS = ["Context", "Door Frame", "Pivot Axle",
        "Processing Tray", "Walkways", "Film Plane Rails",
        "Near Leaf", "Far Leaf", "Lock anchor", "Panel skin",
        "Plywood",            # fixed leaf plywood — split off the leaf steel so scenes can drop it
        "Panel Swing",        # dynamic-component moving group (the swinging assembly)
        "Fan B",              # Fan B body/duct/ply band — taggable so scenes can hide it
        "Drum shell",         # Ø800 housing arcs + rotating C-shell — taggable for hiding
        "Cargo Doors",        # dynamic-component swing doors (click to close)
        "Fan B Cable",        # child DC: orange coil shown only when the door is closed
        "Drum Revolve",       # standalone interactive drum+frame sub-assembly (its own scene); hidden elsewhere
        "Bottom Apron",       # fold-down light aprons (up/folded child DCs) + fixed center baffle
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
    """Interface-2 EPDM ring sealing the Ø800 housing surround to the frame, all
    the way around the aperture (concentric inboard of the panel-perimeter seal,
    interface 1). Exterior door plane (X=-20..0), housing footprint (Yd
    APER_L..APER_R, Z floor-gap..housing-top). Bonded to the housing, so it
    RETRACTS WITH THE HOUSING — the transport model builds it on the moving
    housing rather than on the fixed frame."""
    gw_h, gt_h = 40, 20                    # gasket face width, X-thickness
    hx0 = -gt_h                            # exterior face (X=-20..0)
    hz0, hz1 = PANEL_FLOOR_GAP, DRUM_H     # housing footprint Z (130..2100)
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
    FW, FD = DOOR_FRAME_FACE, DOOR_FRAME_DEPTH   # 50 seal-landing FACE (X0 plane) × 20 DEPTH into container
    x0 = -FD
    # threshold rail runs full width — the suspended drum no longer reaches the
    # floor, so the doorway sill needs no notch. 50×20×3 RHS (was 2×2×0.120): no longer weight-bearing
    # (pivot post carries the panel) — only seal-compression + latch load. 50mm face keeps the seal landing.
    parts = [
        ruby_box("Door Frame threshold (50×20×3)", x0, 0, 0, FD, C_WID, FW, color=C_RAIL),
        ruby_box("Door Frame top (50×20×3)", x0, 0, C_HGT - FW, FD, C_WID, FW, color=C_RAIL),
        ruby_box("Door Frame left stile (50×20×3)", x0, 0, 0, FD, FW, C_HGT, color=C_RAIL),
        ruby_box("Door Frame right stile (50×20×3)", x0, C_WID - FW, 0, FD, FW, C_HGT, color=C_RAIL),
    ]
    # BOLTED to the container's steel cargo-door opening — M10 @ ~300mm, heads on the interior face (through
    # the frame into the container). Reversible; no hot work on the container. (Left stile also carries the
    # welded U-frame / opening-edge channel — see near_leaf.)
    for zc in range(300, int(C_HGT) - 200, 300):
        for yc in (FW / 2, C_WID - FW / 2):
            parts.append(ruby_cylinder("Door frame anchor M10", x0, yc, zc, 6, FD + 6, axis="x", n=8, color="#40444A"))
    # Bottom seal — the OLD full-width bottom brush (which sealed the previous Z130 leaf bottom)
    # is RETIRED. The 217mm floor gap is now closed by the FOLD-DOWN APRONS + fixed center baffle
    # (bottom_apron(), hingepanel Sheet 17); the apron's own TOP brush is the leaf interface, so a
    # threshold brush here would be redundant.
    lt = 12
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

def cam_latch(yl, zl):
    """Lift-and-turn cam latch (McMaster 1619A74): a barrel THROUGH the panel edge (along X) + an
    L-SHAPED handle on the interior face — a stem out along X with the grip BENT UP 90° (along Z),
    so the operator lifts + turns it to swing the cam behind the fixed jamb and hook the strike plate
    on the jamb's vertical short-end face (hingepanel Sheet 13 Detail A). Olive-yellow C_VALVE."""
    r, L = 20, 32                    # latch body barrel (Ø40) through the opening-edge zone, along X
    HSr, HS, GRIP = 6, 44, 60        # handle-arm radius + arm length (out interior) + grip length (bent up)
    x0 = PANEL_CORNER_T              # 40 — interior face of the opening-edge zone
    xarm = x0 + L - 10 + HS          # tip of the handle arm, where the grip bends up
    return '\n'.join([
        ov.ruby_cylinder("Cam latch 1619A74", x0 - 10, yl, zl, r, L, axis="x", color=C_VALVE),
        ov.ruby_cylinder("Cam latch handle arm", x0 + L - 10, yl, zl, HSr, HS, axis="x", color=C_VALVE),
        ov.ruby_cylinder("Cam latch grip (bent up)", xarm, yl, zl, HSr, GRIP, axis="z", color=C_VALVE),
    ])


def hinge_panel():
    h = PANEL_Z_TOP - PANEL_Z_BOT                  # panel skin height (center zone, low bottom)
    hs = PANEL_Z_TOP - PANEL_FLOOR_GAP_SIDE        # corner-zone height — bottom STEPPED UP
    tc, tk = PANEL_CORNER_T, PANEL_CENTER_T        # 40 corner, 120 center
    parts = []

    # Near corner (hinge side) and far corner (Fan B side) — flush 40mm zones. Their bottoms STEP UP
    # to PANEL_FLOOR_GAP_SIDE to clear the bare walkway cantilever bracket legs when the walkway is
    # lifted out for transport (hingepanel Sheet 16); the center zone keeps the low bottom over the tray.
    # The center zone is WIDENED (step lines at NEW_YD_L/R) to frame the Ø800 housing.
    parts.append(ruby_box("Panel near corner (40mm)",
                          0, 0, PANEL_FLOOR_GAP_SIDE, tc, NEW_YD_L, hs, color=C_PLASTIC, alpha=0.5))
    parts.append(ruby_box("Panel far corner (40mm)",
                          0, NEW_YD_R, PANEL_FLOOR_GAP_SIDE, tc, C_WID - NEW_YD_R, hs, color=C_PLASTIC, alpha=0.5))

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
    zs = PANEL_FLOOR_GAP_SIDE     # left/right side seals sit in the stepped corner zones (raised bottom)
    parts.append(ruby_box("EPDM seal left", -gt, 0, zs, gt, gw, z1 - zs, color=C_GASKT, alpha=0.5))
    parts.append(ruby_box("EPDM seal right", -gt, C_WID - gw, zs, gt, gw, z1 - zs,
                          color=C_GASKT, alpha=0.5))

    # 3 × 200mm SS piano hinges on the left edge (Yd=0), exterior, per report §4.1.
    hd, hw, hh = 60, 30, 200
    for hz in (220, 1190, 2158):
        parts.append(ruby_box("Piano hinge", -hd / 2, 0, hz, hd, hw, hh, color=C_STEEL))

    # 2 × lift-and-turn cam latches (McMaster 1619A74) — interior face, OPENING edge only
    # (the pivot edge is hinged; a frame stop takes the outward direction — report §4.2).
    # Heights set for comfortable standing operation: top LOWERED, bottom RAISED (2026-08-31, Alvin).
    for lz in (500, 1900):
        parts.append(cam_latch(210, lz))

    # Interior pull handle — off-the-shelf McMaster 1871A65 round pull handle (the SAME part as the
    # drum handle; ~308mm grip, 52mm standoff), screwed into 1/4"-20 rivet-nuts in the structural
    # FRAME: the left drum-aperture jamb (the 120mm center-zone stud just left of the Ø800 housing),
    # NOT the 1/8″ HDPE skin. Interior face. The swing pivots on the FAR edge, so this near-of-center
    # jamb keeps good leverage while landing the load on steel right beside the drum (report §4.3).
    hy = (NEW_YD_L + APER_L) // 2                         # ≈683 — center of the left drum jamb
    hz0, hz1 = 1146, 1454                                 # ~308mm grip span (1871A65)
    xf = PANEL_CENTER_T                                   # 120 — interior face of the frame zone
    ho = 52                                               # standoff (1871A65)
    for hz in (hz0 + 18, hz1 - 18):                       # two standoff posts off the frame face
        parts.append(ruby_box("Pull-handle standoff", xf, hy - 7, hz - 8, ho, 14, 16,
                              color="#202020"))
    parts.append(ruby_box("Pull-handle grip (1871A65)", xf + ho, hy - 7, hz0,
                          14, 14, hz1 - hz0, color="#202020"))
    return '\n'.join(parts)


# ── Revolving light-trap drum (detailed) ─────────────────────────────────────

def drum_housing(cx, cy):
    """FIXED part of the housed revolving door: the Ø800 housing (two opposed
    80° openings — exterior + interior/walkway, 180° apart) + the 4 opening-edge
    U-channels. Translates with the panel but does NOT revolve, so it sits in the
    moving assembly OUTSIDE the rotating Drum Rotor sub-component. The SKF 6215
    bearings live with the axle beams in drum_frame() (they carry the drum, not the
    housing skin)."""
    H, ZB, od = DRUM_H, PANEL_Z_BOT, OPENING_DEG
    HZB, HZT = LT_HOUSING_Z_BOT, LT_HOUSING_Z_TOP   # housing spans BEAM-to-BEAM (93..2167), past the drum
    HH = HZT - HZB
    parts = []
    # Fixed HOUSING — two solid arcs leaving two od=80° openings (exterior 180° +
    # interior 0°). Spans Z HZB..HZT (bottom-beam top → top-beam under face) so it laps
    # to rim-angle on both axle beams and skirts the two hub gaps (light seal).
    parts.append(ov.ruby_arc_wall("LT Housing arc (near Yd)", cx, cy, HOUSING_R,
                                  HOUSING_T, HH, gap_center_deg=270, gap_deg=180 + od,
                                  color=C_ALUM, alpha=0.5, z0=HZB))
    parts.append(ov.ruby_arc_wall("LT Housing arc (far Yd)", cx, cy, HOUSING_R,
                                  HOUSING_T, HH, gap_center_deg=90, gap_deg=180 + od,
                                  color=C_ALUM, alpha=0.5, z0=HZB))
    # SILL + HEADER solid bands — CLOSE the two openings in the skirt zones (below the bottom cap /
    # above the top cap) so no light passes over or under the drum. Solid arc segments fill each
    # opening angle at those Z bands; the drum-region opening stays open. Matches 2D Sheet-2
    # sill/header (80 / 150mm). Without these the full-height opening leaks over/under the drum.
    for zb_band, hb in ((HZB, 80), (HZT - 150, 150)):
        for oc in (0, 180):                             # fill the INT (0°) + EXT (180°) opening angles solid
            parts.append(ov.ruby_arc_wall("LT Housing sill/header band", cx, cy, HOUSING_R,
                                          HOUSING_T, hb, gap_center_deg=(oc + 180) % 360,
                                          gap_deg=360 - od, color=C_ALUM, alpha=0.5, z0=zb_band))
    # Opening-edge stiffeners — a bonded Al U-channel caps each of the 4 free HDPE
    # edges (2 openings × 2 edges), replacing the old steel jamb posts. Each is a
    # vertical U prism wrapping the wall: base across the edge + two legs (length
    # LEG) running tangentially into the material arc. Slot faces the material.
    Ro, Ri = HOUSING_R, HOUSING_R - HOUSING_T          # wall outer / inner face radii
    CT, LG = LT_EDGE_CHAN_T, LT_EDGE_CHAN_LEG
    for oc in (0, 180):                                 # INT (0°) + EXT (180°) openings
        for e, sgn in ((oc - od / 2, -1), (oc + od / 2, +1)):  # -oh / +oh edges (sgn = into material)
            a = math.radians(e)
            cr, sr = math.cos(a), math.sin(a)
            # U cross-section in (radial R, tangential S) — S positive = into material
            uv = [(Ri - CT, -CT), (Ro + CT, -CT), (Ro + CT, LG), (Ro, LG),
                  (Ro, 0), (Ri, 0), (Ri, LG), (Ri - CT, LG)]
            pts = [(cx + R * cr - sgn * Sc * sr, cy + R * sr + sgn * Sc * cr) for R, Sc in uv]
            parts.append(ov.ruby_prism(f"LT Housing edge channel ({e:.0f}°)", pts, HZB, HH,
                                       color=C_ALUM))
    # (Bearings + axle beams are built in drum_frame(); the housing here is just the
    # fixed outer skin + edge channels. Top/bottom annular felt gap-seal rings omitted —
    # they read as a grey bar cutting across the drum bottom.)
    return '\n'.join(parts)


def drum_rotor(cx=0, cy=0):
    """ROTATING part of the revolving door: the single-opening C-shell drum +
    caps + top stub shaft + interior pull handle + running-gap wiper brushes. Built
    relative to (cx, cy) so it can live in a NESTED Dynamic Component whose RotZ
    revolves it (the revolving-door action). Pass (0,0) for the DC sub-component
    (origin on the drum axis); drum() passes the absolute drum center for the
    static overview build. Shown at the ENTER position (opening at exterior 180°)."""
    H, ZB, od = DRUM_H, PANEL_Z_BOT, OPENING_DEG
    felt = "#7E7E76"
    parts = []
    parts.append(ov.ruby_arc_wall("LT Drum C-shell", cx, cy, DRUM_OR, DRUM_T, H - ZB,
                                  gap_center_deg=180, gap_deg=od,
                                  color=C_LT_DRUM, alpha=0.6, z0=ZB))   # warm tan — distinct from the cool housing skin
    parts.append(ruby_cylinder("LT Drum top cap", cx, cy, H - DRUM_CAP_T, DRUM_CAP_R, DRUM_CAP_T,
                               color=C_ALUM, axis="z"))
    parts.append(ruby_cylinder("LT Drum bottom cap", cx, cy, ZB, DRUM_CAP_R, DRUM_CAP_T,
                               color=C_ALUM, axis="z"))
    # Rolled 25×25×3 Al rim-angle lip at each cap rim (280° C-shell arc — NOT a full
    # ring; the 80° opening has no shell/rim). The shell laps + rivets to it.
    for zc in (ZB, H - LT_RIM_LEG):
        parts.append(ov.ruby_arc_wall("LT Rim-angle lip", cx, cy, DRUM_CAP_R, LT_RIM_T,
                                      LT_RIM_LEG, gap_center_deg=180, gap_deg=od,
                                      color=C_ALUM, z0=zc))
    # Top stub shaft — Ø75, rises from the cap up through the upper bearing (H+30..H+55) to just
    # under the top axle beam; the drum HANGS from it (end-retainer at the top, 2D Sheet 10/11).
    parts.append(ruby_cylinder("LT Drum top shaft", cx, cy, H, 37.5, LT_BEAM_STANDOFF - 3,
                               color=C_STEEL, axis="z"))
    # Bottom stub shaft — SHORT (Ø75), drops from the bottom cap into the lower (floating) bearing
    # (ZB-25..ZB); it only locates, carries no hang (2D LOWER hub).
    parts.append(ruby_cylinder("LT Drum bottom stub", cx, cy, ZB - 25, 37.5, 33,
                               color=C_STEEL, axis="z"))
    # Ø160 steel stub-shaft FLANGE at each cap — welded to the stub, bolted to the cap (4×M10 on Ø120
    # PCD); carries the stub into the cap (2D Sheet 5/6). Top flange above the top cap; bottom below.
    parts.append(ruby_cylinder("LT Drum top stub flange (Ø160)", cx, cy, H, 80, 15, color=C_STEEL, axis="z"))
    parts.append(ruby_cylinder("LT Drum bottom stub flange (Ø160)", cx, cy, ZB - 15, 80, 15, color=C_STEEL, axis="z"))
    # Ø90×4 END-RETAINER PLATE bolted to the UPPER stub-shaft end — its rim clamps the bearing inner
    # race so the drum's hang runs through a bolted member, not a lone circlip (2D Sheet 5/6).
    parts.append(ruby_cylinder("LT Drum end-retainer plate (Ø90×4)", cx, cy, H + LT_BEAM_STANDOFF - 7, 45, 4, color="#9AA0A8", axis="z"))
    # Interior pull handle on a steel STILE spanning the two caps — the operator's pull load lands
    # in the structural Al caps, NOT the thin HDPE wall. Stile bolted to each cap (2D Sheet 1).
    STILE_W = 40
    stile_x = cx + DRUM_OR - DRUM_T - STILE_W                # against the interior wall, just inboard
    z_stile0, z_stile1 = ZB + DRUM_CAP_T, H - DRUM_CAP_T     # between the two caps
    parts.append(ruby_box("LT Handle stile", stile_x, cy - STILE_W / 2, z_stile0,
                          STILE_W, STILE_W, z_stile1 - z_stile0, color=C_STEEL))
    # Off-the-shelf 12" round pull handle (McMaster 1871A65, Ø0.5" bar), BOLTED at both feet to the stile.
    gx = stile_x - 52                                        # grip standoff (2.06"), inboard of the stile
    g0, g1 = 900 - 154, 900 + 154                            # 308mm (12") overall, centered at 900
    parts.append(ruby_cylinder("LT Pull handle (McMaster 1871A65)", gx, cy, g0, 6.35, g1 - g0, color=C_STEEL, axis="z"))
    for bz in (g0, g1):                                      # 2 feet → arm to the stile, BOLTED (1/4", no welds)
        parts.append(ruby_box("LT Pull-handle arm", gx, cy - 6.35, bz - 6.35,
                              stile_x - gx, 12.7, 12.7, color=C_STEEL))
    # Running-gap light-seal WIPER — N vertical #4 (3/16") nylon strip brushes, each snapped into
    # an anodized-Al straight-flange holder whose flange rivets to the drum OD (rivets clear of the
    # brush). Bristles reach across the gap to the fixed housing bore. Spaced 93° on the 280° wall
    # (from the opening edge) so ≥1 always sits in each 100° housing arc at every rotation → the
    # annular gap can never carry light (see 2D Sheets 4 & 7).
    brz = HOUSING_R - HOUSING_T                  # housing bore — bristle tips reach here
    hw = 3.0                                     # tangential half-width of a strip
    hold_d = 6.0                                 # Al holder radial depth at the drum OD
    for k in range(LT_WIPER_N):
        sa = math.radians(180 + od / 2 + k * LT_WIPER_SPACING)
        cr, sr = math.cos(sa), math.sin(sa)
        huv = [(DRUM_OR, -hw * 1.6), (DRUM_OR + hold_d, -hw * 1.6),
               (DRUM_OR + hold_d, hw * 1.6), (DRUM_OR, hw * 1.6)]        # Al flange holder on the OD
        hpts = [(cx + R * cr - S * sr, cy + R * sr + S * cr) for R, S in huv]
        parts.append(ov.ruby_prism("LT Drum wiper holder (Al flange)", hpts, ZB, H - ZB, color="#C8D8E8"))
        uv = [(DRUM_OR + hold_d, -hw), (brz, -hw), (brz, hw), (DRUM_OR + hold_d, hw)]  # nylon bristles → bore
        pts = [(cx + R * cr - S * sr, cy + R * sr + S * cr) for R, S in uv]
        parts.append(ov.ruby_prism(f"LT Drum wiper brush ({math.degrees(sa) % 360:.0f}°)",
                                   pts, ZB, H - ZB, color=felt))
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
    # brackets ALIGNED with the leaf pivot-edge stile (Yd PIVOT_YD−50..PIVOT_YD, 50 RHS) so they weld flush
    # to it — matches Sheet 15 (was offset ±35 straddling the pivot).
    for z in (300, 1180, 2000):
        p.append(ruby_box("Hinge bracket (panel→hub)", 55, PIVOT_YD - 50, z, 140, 50, 110, color=C_STEEL))
    return '\n'.join(p)


def near_leaf():
    """FIXED LEFT panel (Yd0..CUT) — does NOT swing; covers the near-wall strip past the
    near upright. Own perimeter EPDM + the vertical cut seal the swinging panel butts."""
    z0, z1 = CORNER_BOT, PANEL_Z_TOP   # bottom aligned to the adjacent swing corner + apron flap top (CORNER_BOT
    #                                    190), NOT the higher PANEL_FLOOR_GAP_SIDE — else the jamb floats above the
    #                                    plywood (Alvin 2026-09-03: grey jamb left a gap to the plywood)
    gw, gt = 40, 20
    # The fixed opening-edge member is a WELDED BOX SECTION (thin plate), not a solid block: an exterior +
    # interior flange (the HDPE + plywood skins rivet to these) and a swing-facing WEB carrying the cam-latch
    # STRIKE PLATES; the open (container-wall) side welds to the door frame stile. Runs parallel to the swing
    # panel's opening-edge stile. FWT = wall thickness.
    FWT = 4
    box = [
        ruby_box("Fixed left box exterior flange", 0, 0, z0, FWT, CUT, z1 - z0, color=C_STEEL, alpha=1.0),
        ruby_box("Fixed left box interior flange", PLY_X0 - FWT, 0, z0, FWT, CUT, z1 - z0, color=C_STEEL, alpha=1.0),
        ruby_box("Fixed left box web (strike face)", 0, CUT - FWT, z0, PLY_X0, FWT, z1 - z0, color=C_STEEL, alpha=1.0),
    ]
    # cam-latch STRIKE PLATES on the web, at the 2 latch heights (swing panel latches at Z500/1900)
    for lz in (500, 1900):
        box.append(ruby_box("Cam-latch strike plate", 0, CUT - 4, lz - 35, PLY_X0, 10, 70, color="#8890A0"))
    return '\n'.join(box + [
        # 12mm ply with a 45° chamfered inboard edge (Yd CUT) — the swing panel butts + the cut EPDM seals it.
        ov.ruby_prism(f"Fixed left ply (Yd0-{CUT})", [(PLY_X0, 0), (PLY_X0, CUT), (40, CUT - CHAM), (40, 0)],
                      z0, z1 - z0, color="#C8A060", alpha=1.0),
        ruby_box("EPDM fixed-panel top", -gt, 0, z1 - gw, gt, CUT, gw, color=C_GASKT),
        # bottom EPDM dropped — the fold-down apron + its top brush now seal the leaf-bottom interface.
        ruby_box("EPDM fixed-panel left", -gt, 0, z0, gt, gw, z1 - z0, color=C_GASKT),
        ruby_box("EPDM cut seal (fixed-swing joint)", 0, CUT - 6, z0, 40, 12, z1 - z0, color=C_GASKT),
    ])


def far_leaf():
    """NO fixed jamb at the pivot (2026-08-31, Alvin): the pivot-corner plywood TRAVELS with the swinging
    leaf (built in the swing DC by pivot_corner_leaf()), wrapping to the Ø89 post with a clearance notch so
    the leaf swings as one piece. This static part keeps only the container far-WALL vertical EPDM the
    closed leaf edge seals against + a short fixed corner seal past the pivot line (Yd PIVOT_YD..C_WID)."""
    gw, gt = 40, 20
    z0, z1 = PANEL_FLOOR_GAP, PANEL_Z_TOP
    return '\n'.join([
        ruby_box("EPDM fixed-far right (far wall)", -gt, C_WID - gw, z0, gt, gw, z1 - z0, color=C_GASKT),
        ruby_box("EPDM pivot-corner seal (past pivot)", -gt, PIVOT_YD, z1 - gw, gt, C_WID - PIVOT_YD, gw, color=C_GASKT),
    ])


def pivot_corner_leaf():
    """The pivot-corner LEAF EDGE — just the structural pivot-edge stile the hub brackets weld to. NO
    separate ply/frame panel here (removed 2026-08-31, Alvin: it read as a redundant plywood panel jammed
    between the stile and the post). The door FACE at the pivot corner is already skinned by the panel
    FAR-corner HDPE (hinge_panel, X0..40, Yd NEW_YD_R..C_WID, which spans this Yd 2162..2287 zone), so the
    joint is clean steel: leaf stile → hub brackets → post. TRAVELS with the swinging leaf."""
    y1 = PIVOT_YD                                      # pivot line (2287)
    z0, z1 = 12, PANEL_Z_TOP
    # LEAF PIVOT-EDGE STILE (2×2/50 RHS) at the pivot edge, just inboard of the HDPE skin — the 3 hub hinge
    # brackets (pivot_link, X55..195) LAND on this stile and are fillet-welded to it, so leaf+hub+cage swing
    # as one weldment (hingepanel Sheet 15). Travels with the leaf.
    return ruby_box("Leaf pivot-edge stile (50 RHS)", PLY_X0, y1 - 50, z0, 50, 50, z1 - z0,
                    color=C_STEEL, alpha=1.0)


def drum_frame():
    """Steel support CAGE around the Ø800 drum: top+bottom perimeter rectangles + 4 posts,
    plus a central 50×50 RHS AXLE BEAM top and bottom spanning Yd at the drum axis. Each beam
    carries an SKF 6215 (Ø130) via a Ø240 steel MOUNT PLATE welded across it (the bearing ring's
    Ø165 bolt circle is far wider than the 50mm beam, so it bolts to the plate, not the beam wall):
    the UPPER bearing hangs BELOW the top beam so the drum is suspended; the LOWER floats ABOVE the
    bottom beam (radial locate). Per the 2D (Sheets 8/10). Fixed with the assembly."""
    s = 50
    x0, x1 = ov.DRUM_CAGE_X0, ov.DRUM_CAGE_X1
    y0, y1 = ov.DRUM_CAGE_YD_L, ov.DRUM_CAGE_YD_R
    BW, BH = LT_AXLE_BEAM_W, LT_AXLE_BEAM_H     # 50×50 RHS axle beams (carry the SKF 6215s via a mount plate)
    PR = LT_BRG_PLATE_OD / 2                     # bearing mount-plate radius (Ø240) — the ring bolts to this, not the beam
    z_tbeam = DRUM_H + LT_BEAM_STANDOFF          # TOP axle-beam UNDERSIDE (2167): upper bearing hangs below it
    zt = LT_CAGE_TOP                             # cage/beam TOP (2267) — clears the 2388 ceiling by 121mm
    z_bbeam = LT_CAGE_BOT                        # BOTTOM axle-beam bottom: sits in the floor gap, below the Z130 sill
    zb = z_bbeam
    c, cb = C_STEEL, "#5A5AA0"
    p = []
    # perimeter rails: top flush with the top-beam top, bottom flush with the bottom-beam bottom
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
    ca = C_ALUM   # isolated Al top ring
    RTr = LT_TOPRING_OD / 2 - 65   # ring wall: Ø240 OD down to the Ø130 bearing seat
    RCr = LT_COLLAR_OD / 2 - 65
    # TOP hub — the isolated Al bearing RING (Ø240) seats the SKF 6215 + bolts UP (Ø200 CSK circle,
    # clear of the Ø160 flange) to a Ø240 steel MOUNT PLATE welded under the beam; drum hangs (2D Sheet 5/10).
    p.append(ruby_box("Drum top axle beam (50×50 RHS)", DRUM_CX - BW // 2, y0, z_tbeam, BW, y1 - y0, BH, color=c))
    p.append(ruby_cylinder("Drum top bearing mount plate (Ø240×12)", DRUM_CX, DRUM_CY, z_tbeam - LT_BRG_PLATE_T, PR, LT_BRG_PLATE_T, color=c, axis="z"))
    p.append(ov.ruby_arc_wall("Drum upper bearing ring (Ø240 Al, isolated)", DRUM_CX, DRUM_CY, LT_TOPRING_OD / 2, RTr,
                              (z_tbeam - LT_BRG_PLATE_T) - (DRUM_H + LT_BRG_STANDOFF), gap_center_deg=0, gap_deg=0, color=ca, z0=DRUM_H + LT_BRG_STANDOFF))
    p.append(ruby_cylinder("Drum upper bearing (SKF 6215)", DRUM_CX, DRUM_CY, DRUM_H + LT_BRG_STANDOFF, 65, 25, color=cb, axis="z"))
    # BOTTOM hub — mirror: the steel bearing COLLAR (Ø240) seats the SKF 6215 + bolts DOWN to a Ø240
    # mount plate on the bottom beam; locates/floats (radial only — no hang) (per 2D LOWER hub).
    p.append(ruby_box("Drum bottom axle beam (50×40 RHS)", DRUM_CX - BW // 2, y0, z_bbeam, BW, y1 - y0, LT_BBEAM_H, color=c))
    p.append(ruby_cylinder("Drum bottom bearing mount plate (Ø240×12)", DRUM_CX, DRUM_CY, LT_BBEAM_Z1, PR, LT_BRG_PLATE_T, color=c, axis="z"))
    p.append(ov.ruby_arc_wall("Drum lower bearing collar (Ø240 steel)", DRUM_CX, DRUM_CY, LT_COLLAR_OD / 2, RCr,
                              (LT_LBRG_Z0 + 25) - LT_LBRG_Z0, gap_center_deg=0, gap_deg=0, color=c, z0=LT_LBRG_Z0))
    p.append(ruby_cylinder("Drum lower bearing (SKF 6215, floating)", DRUM_CX, DRUM_CY, LT_LBRG_Z0, 65, 25, color=cb, axis="z"))
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
    BAY_FRONT_X to the panel face) enclosing the offset Ø800 housing. A 4-wall
    rectangular tube (Yd = center-zone step lines, Z = floor-gap..panel-top), open
    at the exterior end (entrance) and the interior end (exit onto the walkway)."""
    # HDPE walls sit ON the drum-cage faces (Yd = cage sides), riveted flush with NO gap (2026-08-31 review)
    # — not the wider panel-zone step lines, which left a 47mm slot to the cage.
    yL, yR = ov.DRUM_CAGE_YD_L, ov.DRUM_CAGE_YD_R        # 700, 1662 — cage near/far faces
    # The side/bottom walls run DOWN to the cage bottom beams (LT_CAGE_BOT), not just the Z217 floor gap,
    # so no light slot under the drum. The side walls STOP at the top beams (LT_CAGE_TOP) — no HDPE above
    # them — and the ROOF HDPE lies on the top beams and rivets down to them (2026-09-02, Alvin).
    z0, zc = LT_CAGE_BOT, LT_CAGE_TOP                     # 140 → 2217 (cage/beam top)
    xf = ov.BAY_FRONT_X                                    # -890
    t = ov.BAY_WALL_T                                      # 3.18 (1/8" HDPE)
    depth = ov.DRUM_CAGE_X1 - xf                           # 940 — stretched to the BACK cage beams (was BAY_BACK_X)
    hs = zc - z0                                           # side-wall height — capped at the top beams
    return '\n'.join([
        ruby_box("Bay wall near (Yd)", xf, yL, z0, depth, t, hs, color=C_PLASTIC, alpha=0.5),
        ruby_box("Bay wall far (Yd)", xf, yR - t, z0, depth, t, hs, color=C_PLASTIC, alpha=0.5),
        ruby_box("Bay wall top (roof, riveted to the top beams)", xf, yL, zc - t, depth, yR - yL, t, color=C_PLASTIC, alpha=0.5),
        ruby_box("Bay wall bottom", xf, yL, z0, depth, yR - yL, t, color=C_PLASTIC, alpha=0.5),
    ])


def cage_face_rivets():
    """Blind-rivet rows tying the ROOF + FLOOR HDPE to the drum-cage top/bottom perimeter rails — the same
    fixing the side panels show (Sheet 2: HDPE riveted straight to the cage). Full perimeter on each face."""
    yL, yR = ov.DRUM_CAGE_YD_L, ov.DRUM_CAGE_YD_R
    x0, x1 = ov.BAY_FRONT_X, ov.DRUM_CAGE_X1
    zc, z0 = LT_CAGE_TOP, LT_CAGE_BOT
    rr = 5
    p = []
    # near/far edges — rivet rows running in X (along the near/far cage rails)
    nx = int((x1 - x0 - 80) // LT_RIVET_PITCH)
    for i in range(nx + 1):
        xc = x0 + 40 + i * LT_RIVET_PITCH
        for yd in (yL + 8, yR - 8):
            p.append(ov.ruby_cylinder("Cage roof rivet", xc, yd, zc, rr, 6, axis="z", n=8, color="#C9CCD2"))
            p.append(ov.ruby_cylinder("Cage floor rivet", xc, yd, z0 - 6, rr, 6, axis="z", n=8, color="#C9CCD2"))
    # front/back edges — rivet rows running in Yd (along the front/back cage rails)
    ny = int((yR - yL - 80) // LT_RIVET_PITCH)
    for i in range(ny + 1):
        yc = yL + 40 + i * LT_RIVET_PITCH
        for xd in (x0 + 8, x1 - 8):
            p.append(ov.ruby_cylinder("Cage roof rivet", xd, yc, zc, rr, 6, axis="z", n=8, color="#C9CCD2"))
            p.append(ov.ruby_cylinder("Cage floor rivet", xd, yc, z0 - 6, rr, 6, axis="z", n=8, color="#C9CCD2"))
    return '\n'.join(p)


def bay_wall_cage_rivets():
    """Vertical rivet rows fixing the NEAR + FAR bay HDPE side walls to the FRONT + BACK cage posts
    (Sheet 2: HDPE riveted straight to the cage posts). Item 1, 2026-09-02."""
    yL, yR = ov.DRUM_CAGE_YD_L, ov.DRUM_CAGE_YD_R
    z0, z1 = LT_CAGE_BOT, LT_CAGE_TOP
    x_front, x_back = ov.DRUM_CAGE_X0 + 25, ov.DRUM_CAGE_X1 - 25   # centered on the front + back cage posts
    rr = 5
    p = []
    nz = int((z1 - z0 - 120) // LT_RIVET_PITCH)
    for i in range(nz + 1):
        zc = z0 + 60 + i * LT_RIVET_PITCH
        for xc in (x_front, x_back):
            p.append(ov.ruby_cylinder("Near wall cage rivet", xc, yL - 6, zc, rr, 6, axis="y", n=8, color="#C9CCD2"))
            p.append(ov.ruby_cylinder("Far wall cage rivet", xc, yR + 6, zc, rr, 6, axis="y", n=8, color="#C9CCD2"))
    # horizontal rows along the TOP + BOTTOM edge of each side wall (into the top/bottom cage rails)
    nx = int((ov.DRUM_CAGE_X1 - ov.DRUM_CAGE_X0 - 80) // LT_RIVET_PITCH)
    for i in range(nx + 1):
        xc = ov.DRUM_CAGE_X0 + 40 + i * LT_RIVET_PITCH
        for zc in (z0 + 30, z1 - 30):
            p.append(ov.ruby_cylinder("Near wall cage rivet", xc, yL - 6, zc, rr, 6, axis="y", n=8, color="#C9CCD2"))
            p.append(ov.ruby_cylinder("Far wall cage rivet", xc, yR + 6, zc, rr, 6, axis="y", n=8, color="#C9CCD2"))
    return '\n'.join(p)


def slot_l_strips():
    """L-angle strips fixed on the center-zone frame jambs (Yd NEW_YD_L/R) that secure the panel corner
    HDPE where it now BUTTS the bay walls (Alvin 2026-09-02, item 3). Base leg flat on the interior face
    over the closed slot + an upstand at the jamb the HDPE rivets to."""
    yL, yR = ov.DRUM_CAGE_YD_L, ov.DRUM_CAGE_YD_R
    jL, jR = NEW_YD_L, NEW_YD_R
    z0, z1 = PANEL_FLOOR_GAP, PANEL_Z_TOP
    LT, UP, xf = 3, 40, 40                      # angle wall / upstand leg / interior face of the 40mm panel zone
    c = C_ALUM
    return '\n'.join([
        # NEAR: base leg on the interior face over the closed slot (jL..yL), upstand rising at the jamb
        ruby_box("Slot L-strip near base", xf, jL, z0, LT, yL - jL, z1 - z0, color=c),
        ruby_box("Slot L-strip near upstand", xf, jL, z0, UP, LT, z1 - z0, color=c),
        # FAR: mirror (yR..jR), upstand at the far jamb
        ruby_box("Slot L-strip far base", xf, yR, z0, LT, jR - yR, z1 - z0, color=c),
        ruby_box("Slot L-strip far upstand", xf, jR - LT, z0, UP, LT, z1 - z0, color=c),
    ])


def drum_side_light_seals():
    """Vertical LIGHT-SEAL baffles at the drum-center plane (X=DRUM_CX) closing the open gap between the
    fixed housing OUTER skin and the inner face of each cage/bay side wall. At X=DRUM_CX the round housing
    spans the full Yd width (DRUM_CY±HOUSING_R = 781..1581), so these two strips complete a light-tight
    cross-section and block the straight-down-the-side light leak past the drum (Alvin 2026-09-03)."""
    yL, yR = ov.DRUM_CAGE_YD_L, ov.DRUM_CAGE_YD_R
    z0, z1 = LT_CAGE_BOT + 50, LT_CAGE_TOP - 50           # BETWEEN the top/bottom cage beams (190..2167) — the
    #                                                       beams seal the ends; the baffle must not run through them
    t = ov.BAY_WALL_T
    yhn, yhf = DRUM_CY - HOUSING_R, DRUM_CY + HOUSING_R    # 781 / 1581 — housing outer surface, near / far
    xw = 20
    x0 = DRUM_CX - xw / 2
    c = C_GASKT
    return '\n'.join([
        ruby_box("Drum side light seal (near)", x0, yL + t, z0, xw, yhn - (yL + t), z1 - z0, color=c),
        ruby_box("Drum side light seal (far)", x0, yhf, z0, xw, (yR - t) - yhf, z1 - z0, color=c),
    ])


def surround_rivets():
    """Blind-rivet line tying the HDPE bay surround to the steel center-zone frame at
    the panel-plane lap (Yd = the two center-zone step lines). Rivet heads shown as small
    steel discs @ LT_RIVET_PITCH so the surround reads as FASTENED to the frame, not
    floating. Section detail: hingepanel Sheet 8; flat patterns: hingepanel Sheet 7."""
    yL, yR = ov.DRUM_CAGE_YD_L, ov.DRUM_CAGE_YD_R          # rivets follow the bay onto the cage faces
    z0, z1 = PANEL_FLOOR_GAP, PANEL_Z_TOP
    rr, xr = 6, -7                                        # head Ø exaggerated for visibility; just exterior of panel plane
    n = int((z1 - z0 - 120) // LT_RIVET_PITCH) + 1
    parts = []
    for yd in (yL + 8, yR - 8):                            # the two bay-wall ↔ cage-face lap lines
        for i in range(n):
            zc = z0 + 60 + i * LT_RIVET_PITCH
            parts.append(ruby_cylinder("Surround rivet", xr, yd, zc, rr, 6,
                                       axis="x", n=8, color="#C9CCD2"))
    return '\n'.join(parts)


# (bay_l_angles removed 2026-09-02 — the HDPE bay walls now blind-rivet STRAIGHT to the cage posts,
#  matching hingepanel Sheet 2; the L-angle standoff scheme is retired.)


def far_bay_wall_frame():
    """FAR bay HDPE wall (Yd yR = the drum-passage wall on the pivot / far-container-wall / film-plane side).
    Detailed frame-by-frame per Alvin (2026-08-31):
      1+2 the HDPE reaches out to the frame at the panel plane (the center jamb R) and rivets to it —
          rivet line down the panel-plane edge (X0);
      3   at the MOUTH edge the HDPE blind-rivets STRAIGHT into the front cage post (50 RHS) — no L-angle
          standoff (aligns with hingepanel Sheet 2: skin flat on the post, riveted through);
      4+5 a TOP rail and a BOTTOM rail (50×50 RHS) run the tunnel depth on the cage line, extending the
          door-plane frame back to the drum cage so the wall's top/bottom edges land on steel and rivet."""
    yR = ov.DRUM_CAGE_YD_R                 # 1662 — far cage face / far-wall Yd
    yf = PIVOT_YD                          # 2287 — pivot frame (the beams reach it)
    xf, xb = ov.BAY_FRONT_X, 0             # -890 .. 0 — tunnel depth (mouth → panel plane)
    z0, z1 = LT_CAGE_BOT, LT_CAGE_TOP      # 140 .. 2217 — the HDPE wall stops at the top beams
    t = ov.BAY_WALL_T
    xb2 = 0                                # FLUSH-FRONT with the cage post + frame jambs (door plane X0);
    #                                        full 50mm lap onto the cage, skin laps the beam like the jambs
    RS, rr = 50, 5
    c = C_STEEL
    zt = LT_CAGE_TOP - RS                  # top beam Z2217..2267 (sits on the cage top)
    zb = LT_CAGE_BOT                       # bottom beam Z140..190 (cage bottom)
    p = [
        # (4/5) TOP + BOTTOM beams running in Yd from the drum cage across to the pivot frame — the visible
        #       horizontal beams of Sheet 9; the far HDPE top/bottom edges rivet to them. Just inboard of
        #       the skin (xb2), lapping the far cage-post top/bottom so they tie the wall to the drum cage.
        ruby_box("Far bay top beam (50 RHS)", xb2, yR, zt, RS, yf - yR, RS, color=c),
        ruby_box("Far bay bottom beam (50 RHS)", xb2, yR, zb, RS, yf - yR, RS, color=c),
        # (3) at the MOUTH edge the HDPE blind-rivets STRAIGHT into the front cage post — no L-angle (Sheet 2)
    ]
    # rivet heads on the door skin (exterior face) along the top + bottom beams (in Yd) — point 5
    ny = int((yf - yR - 80) // LT_RIVET_PITCH)
    for i in range(ny + 1):
        yc = yR + 40 + i * LT_RIVET_PITCH
        for zc in (zt + RS / 2, CORNER_BOT + 20):   # bottom row in the HDPE just above the beam top
            p.append(ov.ruby_cylinder("Far bay rivet", -6, yc, zc, rr, 6, axis="x", n=8, color="#C9CCD2"))
    # rivet line down the drum-side edge STRAIGHT into the front cage post — point 2/3
    nz = int((z1 - z0 - 120) // LT_RIVET_PITCH)
    for i in range(nz + 1):
        zc = z0 + 60 + i * LT_RIVET_PITCH
        p.append(ov.ruby_cylinder("Far wall rivet", xf + 20, yR - t - 6, zc, rr, 6, axis="y", n=8, color="#C9CCD2"))
    return '\n'.join(p)


def near_bay_wall_frame():
    """NEAR bay wall (pinhole side / right) — mirror of the far wall: top + bottom 50×50 beams (cage → near
    frame edge), and rivet lines. At the mouth edge the HDPE blind-rivets STRAIGHT into the near cage post
    (no L-angle — aligns with hingepanel Sheet 2). The near corner's bottom section is the Fan-B ply band
    (extended down to CORNER_BOT to match the left side); rivets land on it + the HDPE above."""
    yL = ov.DRUM_CAGE_YD_L                 # 700 — near cage face
    yn = CUT                               # 180 — near frame edge (left swing stile)
    xf = ov.BAY_FRONT_X                    # -890 — bay mouth
    z0, z1 = LT_CAGE_BOT, LT_CAGE_TOP      # 140 .. 2217 — the HDPE wall stops at the top beams
    t = ov.BAY_WALL_T
    xb2 = 0                                # FLUSH-FRONT with the cage post + frame jambs (door plane X0)
    RS, rr = 50, 5
    c = C_STEEL
    zt = LT_CAGE_TOP - RS                  # top beam Z2217..2267 (cage top)
    zb = LT_CAGE_BOT                       # bottom beam Z140..190 (cage bottom)
    p = [
        ruby_box("Near bay top beam (50 RHS)", xb2, yn, zt, RS, yL - yn, RS, color=c),
        ruby_box("Near bay bottom beam (50 RHS)", xb2, yn, zb, RS, yL - yn, RS, color=c),
        # VERTICAL opening-edge stile (Sheet 9 "left swing stile") tying the top + bottom beams at the near
        # frame edge — the far wall's equivalent is the pivot post/stile; the near side had none.
        ruby_box("Near opening-edge stile (50 RHS)", xb2, yn, zb, RS, RS, (zt + RS) - zb, color=c),
        # at the MOUTH edge the HDPE blind-rivets STRAIGHT into the near cage post — no L-angle (Sheet 2)
    ]
    # rivet heads on the door skin (exterior face) along the top + bottom beams (in Yd)
    ny = int((yL - yn - 80) // LT_RIVET_PITCH)
    for i in range(ny + 1):
        yc = yn + 40 + i * LT_RIVET_PITCH
        for zc in (zt + RS / 2, CORNER_BOT + 20):   # bottom row on the Fan-B ply band just above the beam
            p.append(ov.ruby_cylinder("Near bay rivet", -6, yc, zc, rr, 6, axis="x", n=8, color="#C9CCD2"))
    # rivet line down the drum-side edge STRAIGHT into the near cage post
    nz = int((z1 - z0 - 120) // LT_RIVET_PITCH)
    for i in range(nz + 1):
        zc = z0 + 60 + i * LT_RIVET_PITCH
        p.append(ov.ruby_cylinder("Near wall rivet", xf + 20, yL + t + 6, zc, rr, 6, axis="y", n=8, color="#C9CCD2"))
    return '\n'.join(p)


# The FAR apron's last APRON_FIX_W (Yd C_WID−200 .. C_WID) is a FIXED stub, not a fold-down: the folding
# flap would foul the Ø89 pivot post + its Ø220 floor mount plate (near edge PIVOT_YD−110 = Yd2177).
# (APRON_FIX_W now single-sourced from tbs_constants.)

# Each fold-down apron is ONE notched plywood panel spanning the door corner INBOARD to a brush gap off
# the drum-cage side (APRON_IN_L/R = cage ∓ APRON_CAGE_GAP). It crosses the center-zone step line (YD_L/R),
# so its TOP steps down from the raised corner leaf bottom (PANEL_FLOOR_GAP_SIDE) to the lower center leaf
# bottom (PANEL_FLOOR_GAP) — a single stepped cut, hinged as one about the threshold. HZ = hinge Z (12).
_AHZ = 12
# UP profiles — (Yd, Z) polygon in the door plane, extruded APRON_T mm in +X.
# Profile TOPS are pulled down CHAM (12mm): the flap body stops 12mm short of the leaf bottom, and a 45°
# top-edge chamfer prism (apron_top_chamfers) fills back to it — the moving flap's scarf sweeps off the
# EPDM on the fixed leaf face (Sheet 17 Detail E). Corner top = 282, center-ext top = 217.
_CT_LOW = CORNER_BOT - CHAM           # corner body top (178) — BOTH sides: dropped to meet the lowered
#                                       corner-skin bottom (CORNER_BOT) so the apron reads shorter, fixed
#                                       skin below it (far = HDPE, near = Fan-B ply band)
_CC   = PANEL_FLOOR_GAP - CHAM        # center-ext body top (205)
_APRON_UP_NEAR = [(0, _AHZ), (APRON_IN_L, _AHZ), (APRON_IN_L, _CC),
                  (YD_L, _CC), (YD_L, _CT_LOW), (0, _CT_LOW)]
_APRON_UP_FAR  = [(APRON_IN_R, _AHZ), (C_WID - APRON_FIX_W, _AHZ), (C_WID - APRON_FIX_W, _CT_LOW),
                  (YD_R, _CT_LOW), (YD_R, _CC), (APRON_IN_R, _CC)]
APRON_T = PLY_T   # fold-down flap = 12mm plywood, on the interior face (X28..40)


def _apron_vpanel(name, prof, color, alpha):
    """One vertical 12mm-ply panel from a (Yd, Z) polygon on the interior face (X=PLY_X0), pushpulled PLY_T in +X."""
    pts = ", ".join(f"[{ov.mm(PLY_X0)},{ov.mm(y)},{ov.mm(z)}]" for (y, z) in prof)
    r, g, b = ov.hex_to_rgb(color)
    mat = ov.shared_mat_name(name, color, alpha)
    return '\n'.join([
        f'  grp = ents.add_group', f'  grp.name = "{name}"',
        f'  face = grp.entities.add_face({pts})',
        f'  face.reverse! if face.normal.x < 0',
        f'  face.pushpull({ov.mm(PLY_T)})',
        f'  mat = model.materials["{mat}"] || model.materials.add("{mat}")',
        f'  mat.color = Sketchup::Color.new({r}, {g}, {b})',
        f'  mat.alpha = {alpha}', f'  grp.material = mat', ''])


def _prism_xz(name, xz, y0, ylen, color, alpha=1.0):
    """Prism from an (X,Z) polygon in the plane Yd=y0, pushpulled ylen in +Yd. Used for top-edge chamfers."""
    pts = ", ".join(f"[{ov.mm(x)},{ov.mm(y0)},{ov.mm(z)}]" for (x, z) in xz)
    r, g, b = ov.hex_to_rgb(color)
    mat = ov.shared_mat_name(name, color, alpha)
    return '\n'.join([
        '  grp = ents.add_group', f'  grp.name = "{name}"',
        f'  face = grp.entities.add_face({pts})',
        f'  face.reverse! if face.normal.y < 0',
        f'  face.pushpull({ov.mm(ylen)})',
        f'  mat = model.materials["{mat}"] || model.materials.add("{mat}")',
        f'  mat.color = Sketchup::Color.new({r}, {g}, {b})',
        f'  mat.alpha = {alpha}', '  grp.material = mat', ''])


def apron_top_chamfers():
    """45° chamfer along each apron TOP edge (the moving-flap scarf that sweeps off the fixed leaf's EPDM,
    Detail E): a triangular X-Z prism per top segment — outer face (X28) rises the full CHAM to the leaf
    bottom, inner face (X40) stays CHAM lower. One segment per step (corner→282, center-ext→217)."""
    segs = [(0, YD_L, CORNER_BOT), (YD_L, APRON_IN_L, PANEL_FLOOR_GAP),
            (APRON_IN_R, YD_R, PANEL_FLOOR_GAP), (YD_R, C_WID - APRON_FIX_W, CORNER_BOT)]
    return '\n'.join(_prism_xz("Fold-down apron top chamfer",
                               [(PLY_X0, top - CHAM), (40, top - CHAM), (PLY_X0, top)], y0, y1 - y0, C_PLY, 0.85)
                     for (y0, y1, top) in segs)


def apron_up_geom():
    """The fold-down light aprons in the UP (operational, sealing) position — ONE notched plywood panel per
    side (stepped top: corner→PANEL_FLOOR_GAP_SIDE, center ext→PANEL_FLOOR_GAP), bottom-hinged to the
    threshold, extended inboard to a brush gap off the cage. Top + far edges 45°-chamfered (moving-flap
    scarf; Detail E). CHILD of the Panel Swing DC: SHOWN when closed / HIDDEN when swung."""
    # Far edge is 45°-chamfered to mate the full-height far strip's scarf: a plywood wedge adds material
    # inboard-inner (X40) from the square edge (Yd2162) to the scarf (Yd2202) over the corner-zone height.
    yf = C_WID - APRON_FIX_W
    far_wedge = ov.ruby_prism("Fold-down apron (far, UP) chamfer",
                              [(PLY_X0, yf), (40, yf), (40, yf + CHAM)], _AHZ, _CT_LOW - _AHZ, color=C_PLY, alpha=0.85)
    # FIXED (non-folding) plywood stub closing the corner gap between the far apron's far edge
    # (C_WID−APRON_FIX_W) and the pivot post: a fold-down flap here would foul the Ø89 post + its Ø220 floor
    # plate, but this piece stays fixed and at X28..40 it clears both (post X131+, plate X65+).
    stub = ruby_box("Fold-down apron (far) fixed stub", PLY_X0, C_WID - APRON_FIX_W, _AHZ, PLY_T,
                    PIVOT_YD - (C_WID - APRON_FIX_W), CORNER_BOT - _AHZ, color=C_PLY, alpha=0.85)
    return (_apron_vpanel("Fold-down apron (near, UP)", _APRON_UP_NEAR, C_PLY, 0.85) +
            _apron_vpanel("Fold-down apron (far, UP)",  _APRON_UP_FAR,  C_PLY, 0.85) +
            far_wedge + apron_top_chamfers() + stub)


def apron_folded_geom():
    """The aprons FOLDED FLAT into the container for transport (hinged down 90° about the threshold) — ONE
    notched panel per side, laid flat (the panel LENGTH steps 270/205 with the top). Drawn in the
    folded-at-door-plane pose; the swing-DC child gets a −LOCK pre-rotation so the parent's +LOCK lands it
    here at swing=1. SHOWN when swung / HIDDEN closed."""
    # folded outline in (X, Yd) at Z=_AHZ, extruded APRON_T up in Z. X = _AHZ + (leaf_top − _AHZ) reach.
    near = [(_AHZ, 0), (CORNER_BOT, 0), (CORNER_BOT, YD_L), (PANEL_FLOOR_GAP, YD_L),
            (PANEL_FLOOR_GAP, APRON_IN_L), (_AHZ, APRON_IN_L)]
    far  = [(_AHZ, APRON_IN_R), (PANEL_FLOOR_GAP, APRON_IN_R), (PANEL_FLOOR_GAP, YD_R),
            (CORNER_BOT, YD_R), (CORNER_BOT, C_WID - APRON_FIX_W), (_AHZ, C_WID - APRON_FIX_W)]
    return (ov.ruby_prism("Fold-down apron (near, FOLDED)", near, _AHZ, APRON_T, color=C_PLY, alpha=0.6) +
            ov.ruby_prism("Fold-down apron (far, FOLDED)",  far,  _AHZ, APRON_T, color=C_PLY, alpha=0.6))


def apron_edge_brushes():
    """Vertical strip brushes on the two fold-down apron inner edges (Yd APRON_IN_L / APRON_IN_R), reaching
    APRON_CAGE_GAP across to the cage sides — a light-tight bristle wall closing the residual side slot
    (baffle top → center leaf bottom). CHILD of the swing DC (rides + hides with the aprons)."""
    z0, z1 = LT_CAGE_BOT - 10, PANEL_FLOOR_GAP            # 130 → 217 (baffle top to center leaf bottom)
    parts = [
        ruby_box("Apron edge brush (near)", 0, APRON_IN_L,     z0, 30, 2, z1 - z0, color=C_SEAL),
        ruby_box("Apron edge brush (far)",  0, APRON_IN_R - 2, z0, 30, 2, z1 - z0, color=C_SEAL),
    ]
    for i in range(int((z1 - z0) // 8)):
        zc = z0 + 4 + i * 8
        parts.append(ruby_box("Apron brush bristle", 8, APRON_IN_L + 2,                  zc, 2, APRON_CAGE_GAP, 2, color="#141414"))  # near → +Yd to cage
        parts.append(ruby_box("Apron brush bristle", 8, APRON_IN_R - 2 - APRON_CAGE_GAP, zc, 2, APRON_CAGE_GAP, 2, color="#141414"))  # far → −Yd to cage
    return '\n'.join(parts)


def fixed_bottom_geom():
    """FIXED bottom closure (does NOT fold): the center light baffle under the drum bay — trimmed to the
    apron inner edges (APRON_IN_L..APRON_IN_R) so it butts the extended aprons — capped 10mm below the cage
    bottom, with a horizontal strip brush on its top edge sweeping the swinging cage bottom. (The far-pivot
    fixed panel is no longer a separate stub — it's the bottom of the now full-height far_leaf strip.)"""
    baf_top = LT_CAGE_BOT - 10                           # 130
    cgL, cgR = ov.DRUM_CAGE_YD_L, ov.DRUM_CAGE_YD_R       # 700, 1662 — cage width the top brush spans
    parts = [
        # 12mm ply baffle with 45° chamfered ENDS (Yd) where the fold-down apron inner edges meet it —
        # the apron scarf laps the chamfer, the apron edge brush seals above (Detail E). X-Yd prism.
        ov.ruby_prism("Center light baffle (fixed)",
                      [(PLY_X0, APRON_IN_L), (40, APRON_IN_L + CHAM), (40, APRON_IN_R - CHAM), (PLY_X0, APRON_IN_R)],
                      51, baf_top - 51, color=C_PLY, alpha=1.0),
        # Horizontal strip brush on the baffle top edge — bristles reach the 10mm up to the swinging cage
        # bottom (Z140) over the cage width; the side corners are sealed by apron_edge_brushes().
        ruby_box("Baffle top brush", -1, cgL, baf_top, 30, cgR - cgL, LT_CAGE_BOT - baf_top, color=C_SEAL),
    ]
    for i in range(int((cgR - cgL) // 12)):
        yc = cgL + 6 + i * 12
        parts.append(ruby_box("Baffle brush bristle", 8, yc, baf_top, 2, 2, LT_CAGE_BOT - baf_top, color="#141414"))
    return '\n'.join(parts)


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
        # Film-plane left rig is wired as a SWING-DC CHILD below (fpl_inst) so it HIDES in transport — a
        # root-level hidden_formula doesn't recompute when the parent DC animates (only children do).
        component("Transport stay wall anchors", "Lock anchor", wall_anchors()),
        component("Fan B electrical box", "Fan B Cable", fan_b_box()),
        component("Fixed bottom closures (baffle + pivot stub)", "Bottom Apron", fixed_bottom_geom()),
    ]
    static_body = '\n'.join(static_comps)

    # Moving assembly → the Panel Swing DC. Everything that swings lives here: the SPLIT
    # panel (trimmed to PANEL_CUT..PIVOT, the corners/full seals erased below) + bay +
    # housing + drum cage + Fan B + the moving hub + stay hooks.
    dc_body = '\n'.join([
        hinge_panel(),
        # Fan B corner: 18mm PLYWOOD mount band (bottom up to PANEL_FAN_BAND_Z) for
        # rigid fan/duct mounting; 1/8″ HDPE skin above. (rev11 material differentiation.)
        # Near corner is a STEPPED zone: its bottom rises to PANEL_FLOOR_GAP_SIDE (282) like the frame +
        # aprons, so the fold-down flap top meets it flush (no overlap) and it clears the walkway cantilever.
        # near corner skins EXTENDED inboard from NEW_YD_L (653) to the near bay wall / cage face
        # (DRUM_CAGE_YD_L 700) so the panel HDPE BUTTS the bay wall — no 47mm slot (Alvin 2026-09-02, item 2).
        ruby_box("Fan B mount band (18mm ply)", 0, CUT, CORNER_BOT, 40,
                 ov.DRUM_CAGE_YD_L - CUT, ov.PANEL_FAN_BAND_Z - CORNER_BOT, color=C_PLY, alpha=0.5),
        ruby_box(f"Panel near (swing, Yd{CUT}-{ov.DRUM_CAGE_YD_L})", 0, CUT, ov.PANEL_FAN_BAND_Z, 40,
                 ov.DRUM_CAGE_YD_L - CUT, PANEL_Z_TOP - ov.PANEL_FAN_BAND_Z, color=C_PLASTIC, alpha=0.5),
        # swing panel + its top seal now run to the PIVOT line (the pivot-corner plywood travels with it).
        ruby_box("EPDM seal top (trimmed)", -20, CUT, PANEL_Z_TOP - 40, 20, PIVOT_YD - CUT, 40, color=C_GASKT, alpha=0.5),
        # panel bottom EPDM (L/R, trimmed) dropped — superseded by the fold-down apron + its top brush.
        # Far corner is a STEPPED zone: bottom rises to PANEL_FLOOR_GAP_SIDE (282) so the fold-down flap top
        # meets it flush (fixes the flap↔leaf overlap) and it clears the walkway cantilever in the swing.
        # The HDPE skin runs CONTINUOUSLY to the PIVOT LINE (2026-08-31) — no separate pivot ply panel; the
        # pivot-edge stile (pivot_corner_leaf) sits behind it and ties the leaf to the hub brackets.
        # far corner skin EXTENDED inboard from NEW_YD_R (1709) to the far bay wall / cage face
        # (DRUM_CAGE_YD_R 1662) so the panel HDPE BUTTS the bay wall — no 47mm slot (Alvin 2026-09-02, item 2).
        ruby_box("Panel far corner (trimmed)", 0, ov.DRUM_CAGE_YD_R, CORNER_BOT, 40,
                 PIVOT_YD - ov.DRUM_CAGE_YD_R, PANEL_Z_TOP - CORNER_BOT, color=C_PLASTIC, alpha=0.5),
        pivot_corner_leaf(),   # pivot-edge STILE (the hub brackets weld to it) — travels with the leaf
        bay(),
        far_bay_wall_frame(),             # FAR wall (pivot side): rails to cage + rivets STRAIGHT to the post
        near_bay_wall_frame(),            # NEAR wall (pinhole side): top + bottom beams + rivets to the post
        surround_rivets(),                # blind rivets tying the bay surround to the frame (Sheet 8)
        cage_face_rivets(),               # roof + floor HDPE riveted to the cage rails (like the side panels)
        bay_wall_cage_rivets(),           # near/far side-wall HDPE riveted to the front+back cage posts (item 1)
        slot_l_strips(),                  # L-angle on the jambs securing the extended panel HDPE (item 3)
        drum_side_light_seals(),          # baffles closing the housing↔side-wall side gap (light seal)
        drum_housing(DRUM_CX, DRUM_CY),   # housing + rotor are static geometry in the swing
        drum_rotor(DRUM_CX, DRUM_CY),     # def, so they swing rigidly at the correct position
        drum_frame(),
        fan_b(),
        pivot_link(),
        # (door-plane pivot_connect beams removed — the frame→post connection is the inboard hub + 3 hinge
        #  brackets landing on the leaf pivot-edge stile; see pivot_corner_leaf + pivot_link, Sheet 15.)
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

    # ── Standalone interactive drum+frame sub-assembly (its own "Drum revolve" scene) ──
    # The FIXED frame (housing + cage + upper bearing) is one static component; the ROTOR is a
    # TOP-LEVEL Dynamic Component built at LOCAL origin (so its axis is the drum axis) + instanced
    # at the drum center — click it to ANIMATE 90°/step through the revolving-door positions.
    revolve_frame_comp = component("Drum Revolve — Frame (housing · cage · bearing)",
                                   "Drum Revolve",
                                   drum_housing(DRUM_CX, DRUM_CY) + "\n" + drum_frame()
                                   + "\n" + drum_side_light_seals())
    revolve_rotor_body = drum_rotor(0, 0)          # local origin → the DC's RotZ revolves about the drum axis

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

# ── Film-plane left FIXED rig — as a SWING-DC CHILD so it HIDES in transport (a root component's
#    hidden_formula does not recompute when the parent DC animates; only children do). The shared-pivot
#    film-plane hardware (parked carriage + stub + saddles + fixing plates) is not the light-trap door and
#    read as floating plates once the panel swings. Built at world coords; visibility-swaps on the swing. ──
fpl_defn = model.definitions.add("Film-Plane Rails (left, removable)")
ents = fpl_defn.entities
{film_plane_left()}
ents = defn.entities
fpl_inst = ents.add_instance(fpl_defn, Geom::Transformation.new)
fpl_inst.name = "Film-Plane Rails (left, removable)"
fpl_inst.layer = model.layers["Film Plane Rails"]
fpl_inst.set_attribute("dynamic_attributes", "_name", "FilmPlaneLeftFixed")
fpl_inst.set_attribute("dynamic_attributes", "hidden", 0.0)
fpl_inst.set_attribute("dynamic_attributes", "_hidden_formula", "PanelSwing!swing>0.5")

# ── Fold-down light aprons — CHILD DC components inside the swing def. UP (sealing) is SHOWN when the
#    door is CLOSED and HIDDEN once the panel swings; FOLDED (flat into the container) is the mirror,
#    built in the folded-at-door-plane pose with a −LOCK pre-rotation so the parent's +LOCK lands it
#    there at swing=1. Same visibility-swap pattern as the transport stay rods. ──
au_defn = model.definitions.add("Fold-down Aprons (up)")
ents = au_defn.entities
{apron_up_geom()}
{apron_edge_brushes()}
ents = defn.entities
au_inst = ents.add_instance(au_defn, Geom::Transformation.new)
au_inst.name = "Fold-down Aprons (up)"
au_inst.layer = model.layers["Bottom Apron"]
au_inst.set_attribute("dynamic_attributes", "_name", "FoldApronsUp")
au_inst.set_attribute("dynamic_attributes", "hidden", 0.0)
au_inst.set_attribute("dynamic_attributes", "_hidden_formula", "PanelSwing!swing>0.5")

af_defn = model.definitions.add("Fold-down Aprons (folded)")
ents = af_defn.entities
{apron_folded_geom()}
ents = defn.entities
af_tr = Geom::Transformation.rotation([{PIVOT_X}.mm, {PIVOT_YD}.mm, 0], Z_AXIS, (-{LOCK}).degrees)
af_inst = ents.add_instance(af_defn, af_tr)
af_inst.name = "Fold-down Aprons (folded)"
af_inst.layer = model.layers["Bottom Apron"]
af_inst.set_attribute("dynamic_attributes", "_name", "FoldApronsFolded")
af_inst.set_attribute("dynamic_attributes", "hidden", 1.0)
af_inst.set_attribute("dynamic_attributes", "_hidden_formula", "PanelSwing!swing<0.5")

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

# ═══ Drum Revolve — standalone interactive sub-assembly (its own scene) ═══
# A SEPARATE copy of the drum + fixed frame on the "Drum Revolve" tag (hidden in every other
# scene). The FIXED frame is one static component; the DRUM is a TOP-LEVEL Dynamic Component —
# NOT nested in the swing (that nesting reset the old drum-revolve DC on redraw). Click the drum
# with the Interact tool → ANIMATE the drum 90°/step: opening↔EXTERIOR (enter) → solid wall
# (sealed) → opening↔INTERIOR (exit) → sealed → back. The stile + pull handle revolve with it.
{revolve_frame_comp}
rev_defn = model.definitions.add("Drum Rotor (revolve)")
ents = rev_defn.entities
{revolve_rotor_body}
revolve_inst = entities.add_instance(rev_defn, Geom::Transformation.translation([{DRUM_CX}.mm, {DRUM_CY}.mm, 0]))
revolve_inst.name = "Drum Rotor (revolve)"
revolve_inst.layer = model.layers["Drum Revolve"]
rda = "dynamic_attributes"
[rev_defn, revolve_inst].each do |e|
  e.set_attribute(rda, "_name", "DrumRevolve")
  e.set_attribute(rda, "_lengthunits", "MILLIMETERS")
  e.set_attribute(rda, "pos", 0.0)
end
revolve_inst.set_attribute(rda, "_pos_access", "VIEW")
revolve_inst.set_attribute(rda, "_pos_label", "Revolve step")
revolve_inst.set_attribute(rda, "rotz", 0.0)
revolve_inst.set_attribute(rda, "_rotz_formula", "90*pos")
revolve_inst.set_attribute(rda, "onclick", 'ANIMATE("pos", 0, 1, 2, 3)')
revolve_inst.set_attribute(rda, "_onclick_access", "NONE")

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

# ── Tag the FIXED leaf PLYWOOD ("Fixed left ply", inside the Near-Leaf steel component) onto its own
#    "Plywood" layer, so the steel scene can drop the ply while keeping the leaf's U-frame + strikes. ──
ply_l = model.layers["Plywood"]
if ply_l
  model.definitions.each do |d|
    d.entities.grep(Sketchup::Group).each do |g|
      nm = g.name.to_s
      g.layer = ply_l if nm.include?("ply") && !nm.include?("mount band") && !nm.downcase.include?("apron")
    end
  end
end

# ── Camera + scenes (the swing is interactive; plus a "Labeled" callout scene) ──
model.layers.each {{ |l| l.visible = true }}
model.layers["Labels"].visible = false if model.layers["Labels"]  # frame geometry, not labels
model.layers["Drum Revolve"].visible = false if model.layers["Drum Revolve"]  # interactive copy → its own scene only
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

# ── "Steel · Pivot · Frame · Cage" scene — isolate the STRUCTURAL STEEL (Ø89 pivot post, hinge-panel
#    frame, drum cage + the far-wall/near-wall beams) by HIDING the HDPE skins, EPDM, Fan-B and the
#    drum shell, so the framing reads clearly for review. (Hide-specific, so Layer0 steel stays on.) ──
model.layers.each {{ |l| l.visible = true }}
["Panel skin", "Fan B", "Drum shell", "Labels", "Drum Revolve", "Walkways", "Bottom Apron", "Plywood"].each {{ |n|
  model.layers[n].visible = false if model.layers[n] }}
sc_eye = Geom::Point3d.new(2600, 3300, 2000)     # 3/4 from the interior / far-Yd side
sc_tgt = Geom::Point3d.new(-300, 1750, 1150)     # look at the far-wall / pivot region
model.active_view.camera = Sketchup::Camera.new(sc_eye, sc_tgt, Z_AXIS)
sc_focus = model.entities.grep(Sketchup::ComponentInstance).select {{ |i|
  ["Door Frame", "Pivot Axle", "Panel Swing"].include?(i.layer.name) }}
model.active_view.zoom(sc_focus) unless sc_focus.empty?
model.active_view.zoom(0.85)
scpage = model.pages.add("Steel · Pivot · Frame · Cage"); scpage.use_camera = true
model.layers.each {{ |l| l.visible = true }}      # restore for the default state
model.layers["Labels"].visible = false if model.layers["Labels"]
model.layers["Drum Revolve"].visible = false if model.layers["Drum Revolve"]

# ── "Drum revolve" scene — isolate the standalone drum + frame; click the drum
#    to ANIMATE it 90°/step through the revolving-door positions. Only the "Drum Revolve" tag
#    shows here; it is hidden in every other scene. ──
model.layers.each {{ |l| l.visible = false }}
model.layers["Drum Revolve"].visible = true if model.layers["Drum Revolve"]
dr_focus = model.entities.grep(Sketchup::ComponentInstance).select {{ |i| i.layer.name == "Drum Revolve" }}
unless dr_focus.empty?
  fb = Geom::BoundingBox.new
  dr_focus.each {{ |i| fb.add(i.bounds) }}
  fctr = fb.center
  dr_dir = Geom::Vector3d.new(0.6, -0.72, 0.45); dr_dir.normalize!
  dr_eye = fctr.offset(dr_dir, fb.diagonal * 1.6)
  model.active_view.camera = Sketchup::Camera.new(dr_eye, fctr, Z_AXIS)
  model.active_view.zoom(dr_focus)
  model.active_view.zoom(0.85)
end
drpage = model.pages.add("Drum revolve"); drpage.use_camera = true
model.layers.each {{ |l| l.visible = true }}
model.layers["Labels"].visible = false if model.layers["Labels"]
model.layers["Drum Revolve"].visible = false if model.layers["Drum Revolve"]  # its own scene only

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
    [dc_inst, doors_inst, revolve_inst].each {{ |di| cls.redraw_with_undo(di) rescue nil }}
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
