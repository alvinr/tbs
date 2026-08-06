# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
tbs_constants.py — Single source of truth for TBS-001 geometry and equipment.

All generator scripts should import from this module:
    from tbs_constants import *

Redesign basis (2026-04-23 rev 2):
  Black-water drums (2× 55-gal) relocated from right end zone to left end zone
  (Y-stacked behind evap cooler).  IBC column right-justified to X=4674–5893mm.
  Film plane widens from 2920mm to 3549mm (X=1100–4649mm).
  Pinhole recenterd to X=2874mm.  Max swing decreases from 36.5° to 31.4°
  (same Y travel over wider 3549mm rail span).

Redesign basis (2026-04-23 rev 3):
  Evap cooler relocated to pinhole wall face (Yd=0) at X=930–1530mm — always
  shadow-free at Yd=0 regardless of X position.
  Drums repositioned to X=20–600mm, Yd=25–605mm (near cargo door end wall,
  Yd range entirely below light trap drum's Yd=806–1556mm band — no X-clearance
  conflict).  Zone left boundary moves from X=1100mm to X=625mm.
  Film plane widens from 3549mm to 4024mm (X=625–4649mm).
  Pinhole recenterd to X=2637mm.  Max swing decreases from 31.4° to 28.3°
  (wider rail span over same Y travel).

Redesign basis (2026-05-03 rev 4):
  Hinged panel redesigned as stepped profile: 40mm corners (18mm ply + 4mm
  steel plate + 18mm ply) flanking 120mm center zone (unchanged RHS frame
  construction housing the light trap drum).  Step transitions at Yd=756mm
  and Yd=1606mm (drum 750mm + 50mm clearance each side).
  Panel + drum SWING ~56° about the Ø89 pivot post for transport (rev10,
  supersedes the HGR20 slide) so the assembly clears the container exterior face,
  allowing standard ISO cargo doors to close. Fixed door frame with EPDM seal at X=0.

Redesign basis (2026-05-06 rev 5):
  Waste drums (2x 55-gal) eliminated.  Replaced by a 4th IBC (waste, 630L)
  in the right end zone.  4 IBCs in 2x2 stack: Blue #1 + Blue #2 on top
  (gravity feeds spray bar), Brown + Waste on bottom (receives by gravity).
  All V-groove dolly tracks, bridge sections, and drum slide mechanisms removed.
  Processing tray (304 SS, 50mm rim) permanently installed in optical zone
  with built-in 1:200 pitch (HDPE shim strips) and sump pickup.  No track/tray conflict.
  IBCs loaded empty via cargo doors; filled/drained remotely through 2" NPT
  bulkhead fittings in the far end wall (X=C_LEN face).
  Left end zone freed up (light trap drum remains in hinge panel).

Redesign basis (2026-05-06 rev 6):
  Film plane extended left from X=625mm to X=150mm (30mm clearance from panel
  center inner face at X=120mm).  Pinhole recentered on wider active plane.
  Width increases from 4024mm to 4499mm (+11.8%).  Active area from 9.61 m²
  to 10.74 m² (103→116 sqft).  Max swing decreases from 28.3° to 25.7°
  (wider rail span, same Y travel).  Left end zone shrinks to X=0–150mm.

Redesign basis (2026-05-20 rev 7 — walkway reorg):
  Near walkway (pinhole wall side) made usable by relocating wall-mounted
  equipment that blocked passage.  Evaporative cooler moved external with
  200mm duct penetration at X=1000, Z=1900.  EP raised to Z=1600–2200.
  Batteries switched to 120mm slim-profile depth.  Pump manifold
  (P-01/P-02/P-04), ACC-01, and 3× filter housings relocated from pinhole
  wall to equipment panel in IBC plumbing corridor (270mm gap between
  near/far IBC columns, Yd=1046–1316).  Panel: 18mm marine ply, 780×1110mm
  at X=4800.  Near walkway widened to 500mm at X=1600–2310.  Corner
  triangle at right walkway/IBC junction.  Tray sump relocated to X=4550,
  Yd=80 (slope to IBC corner).  Filter housings reverted to 3× separate
  4.5"×10" Big Blue (combo unit Purcooflow WHF2045B302 does not fit corridor).

Redesign basis (2026-07-17 — film-plane top rail lowered):
  FP_H 2138→2094 — the film-plane top rail dropped 44mm (via new RAIL_OFF_TOP=144,
  split out of the overloaded RAIL_OFF=100) to win +25mm ceiling clearance for the
  top carriage/fittings.  Active image plane 4499×2138→4499×2094; area 104→101 sqft
  (9.62→9.42 m²).  Cascades IMAGE_AREA_SQFT, CLAMP_N_VERT (15→14) → clip count → parts/
  costing, XSLIDE_Z_TRAVEL (250→245), BRACE_Z_TOP (2288→2244), and chem/muslin consumables.
"""

import math
import os

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(_THIS_DIR, "..", ".."))

# ── Container interior ────────────────────────────────────────────────────────
C_LEN  = 5893   # interior length, long axis X (mm)
C_WID  = 2362   # interior width = focal length = optical depth Y (mm)
C_HGT  = 2388   # interior height Z (mm)

# ── Film plane ────────────────────────────────────────────────────────────────
FP_H     = 2094   # film plane height (mm)          [film-plane-redesign: 2388→2138 — active height with the low-profile V-trolley corner (BUILD 140→110); 2138→2094 — top edge lowered 44mm for +25mm ceiling clearance (top rail dropped via RAIL_OFF_TOP); ~C_HGT − RAIL_OFF_TOP(144) − RAIL_OFF_BOT(walkway)]
FP_X_L   = 150    # film plane left edge X (mm)     [rev6: was 625; panel inner face 120mm + 30mm]
FP_X_R   = 4649   # film plane right edge X (mm)    [was 4019 → wider right zone]
FP_W     = FP_X_R - FP_X_L   # = 4499mm          [rev6: was 4024]
FP_Y     = 2262   # nominal depth from pinhole wall (mm)  [unchanged]
FP_Y_MIN = 100    # minimum carriage depth (mm)     [unchanged]

# ── Muslin clamp system ──────────────────────────────────────────────────────
# Off-the-shelf inert NYLON spring clamps (Pittsburgh 69289 — fiberglass body + swivel
# pads, no corrosion in the cyanotype splash zone) at 150mm centers grip the muslin
# against the 2"x2"x1/8" aluminum angle perimeter frame. An inert HDPE FILLER STRIP fills
# the open L channel so the clamp bites a solid full-depth sandwich: the clamp jaw must
# clear the 2" leg + ACM + muslin (~55mm), so a ≥3" clamp is used. The bottom
# (walkway-facing) edge is left UNCLAMPED — no clearance between the raised walkway deck
# and the board (also keeps the swing/tilt envelope clear); the muslin is secured on the
# top + two side edges. Replaced the custom through-bolted bracket + torsion-spring + neoprene
# jaw (2026-07-22). See film-clamp-mechanism-report.md.
FP_ANGLE_LEG  = 50.8   # angle leg size (mm) — 2" = 50.8mm
FP_ANGLE_T    = 3.175  # angle thickness (mm) — 1/8" = 3.175mm
DIBOND_T      = 3      # ACM (Dibond) backing sheet thickness (mm) — 3mm black ACM (Central Coast / TAP)
MUSLIN_T      = 0.5    # muslin fabric thickness (mm, approx)
# Pre-cut muslin is CUT TO FIT THE PROCESSING TRAY (it is washed flat in the tray), so it is NARROWER
# than the film-plane ACM+frame: MUSLIN_CUT_W/H (defined with the tray, below).  It mounts on the ACM
# INSIDE the frame (~70mm/side proud of the muslin edge) and is clamped INBOARD on the ACM face
# (field detail) — NOT captured in the frame's L-channel.  Muslin < tray < film-plane (ACM+frame).
# Loading: the beam parks at the near/pinhole-wall end, the muslin is fed through the far drop-slot and
# pulled across to the beam, then the beam rolls back over the laid muslin to wash (see the tray report).
CLAMP_SPACING = 150    # clamp center-to-center spacing (mm)
CLAMP_FILLER_D = FP_ANGLE_LEG - DIBOND_T - MUSLIN_T - FP_ANGLE_T   # inert HDPE filler depth into the L channel (mm) = 41.5
CLAMP_N_HORIZ = FP_W // CLAMP_SPACING + 1   # clamps per horizontal edge
CLAMP_N_VERT  = FP_H // CLAMP_SPACING + 1   # clamps per vertical edge
CLAMP_N_TOTAL = CLAMP_N_HORIZ + 2 * CLAMP_N_VERT   # top edge + 2 sides; bottom (walkway) edge omitted

# ── Pinhole (recenterd on new film plane) ─────────────────────────────────────
PH_X   = FP_X_L + FP_W // 2   # = 2399mm  [rev6: was 2637]
PH_H   = 1194                  # height (mm) [unchanged]
PH_D   = 2.17                  # diameter (mm) — Rayleigh, f=2362, λ=550nm [unchanged]
PH_F   = C_WID                 # focal length = container width [unchanged]
PH_FNO = round(PH_F / PH_D)   # f/1088 [unchanged]

# ── Pinhole wall frame + interchangeable plate (owned here; generate_plate_drawing.py reads them) ──
PLATE_OD       = 600   # wall frame / plate outer dimension (mm, square)
PLATE_THK      = 15    # aluminum plate thickness (mm)  [PLATE_THK not PLATE_T — avoids the local-var collision in electrical/lighttrap generators]
WALL_FRAME_T   = 6     # wall frame steel thickness (mm, S275)
PINHOLE_DISC_D = 50    # pinhole disc OD (mm, Lenox Laser supply)
PINHOLE_DISC_T = 0.1   # pinhole disc thickness (mm, SS-302)

# ── Film plane rails ──────────────────────────────────────────────────────────
RAIL_X_L  = FP_X_L   # left rail X  (mm)   [rev6: 150mm; was 625]
RAIL_X_R  = FP_X_R   # right rail X (mm)   [was 4019 → now 4649]
RAIL_SPAN = RAIL_X_R - RAIL_X_L   # = 4499mm  [rev6: was 4024]
RAIL_LEN  = 2200      # rail length  (mm)   [unchanged — same Y travel]
RAIL_OFF  = 100       # generic ceiling/floor offset (mm) — floor-standing equipment, drum, schematic rails  [unchanged]
RAIL_OFF_TOP = 144    # film-plane TOP rail ceiling offset (mm) — dropped 44mm from RAIL_OFF(100) to win +25mm ceiling clearance for the top carriage/fittings; drives BRACE_Z_TOP + every film-plane top-rail model site
RAIL_OFF_BOT = 160    # floor (BOTTOM) offset (mm) = WALKWAY_H 140 + 20mm so the film-plane bottom
                      # edge clears the raised Z140 walkway by 20mm as it travels in Yd (was 150 for the
                      # Z130 deck). Costs ~60mm of muslin height (~2.5% of the captured image).

# ── Movement ranges (OPTION A: fixed-size rigid plane on floating-corner slides) ──
# rev7 / Option A (2026-06-06): the film plane is a FIXED-SIZE rigid rectangle that
# rotates RIGIDLY about its centre — it no longer stretches/twists. Each corner's
# depth carriage gains a 2-axis X-Z cross-slide + rod-end that absorbs the rigid-
# rotation arc travel. The earlier ±42°/±25.7° figures were the *stretching*
# mechanism's stops; a rigid plane's limits are different:
#   tilt  — rails allow ~65° (asin(1081/(FP_H/2))); capped at 40° by cross-slide Z.
#   swing — rail-depth limited to asin(1081/(FP_W/2)) ≈ 28.7°; set to 28°.
#   combined tilt+swing is limited (the old C7 compound twist is DROPPED — a rigid
#   plane cannot form a ruled surface, and its corners would sweep ~3.4m of depth).
# (1081 = half the rail travel about the mid-rail centre: (FP_Y - FP_Y_MIN)/2.)
MAX_TILT_DEG  = 40.0   # design max single-axis tilt (cross-slide-Z limited)
MAX_SWING_DEG = 28.0   # design max single-axis swing (≈ rail-depth limit 28.7°)

# Cross-slide strokes that absorb the rigid-rotation arc travel at the corners
# (Option A spec; not yet drawn in the FPM sheets / 3D model):
XSLIDE_Z_TRAVEL = round((FP_H / 2) * (1 - math.cos(math.radians(MAX_TILT_DEG))))   # ≈ 245mm (tilt, FP_H 2094) — reserved
XSLIDE_X_TRAVEL = round((FP_W / 2) * (1 - math.cos(math.radians(MAX_SWING_DEG))))  # ≈ 263mm (swing) — reserved
XSLIDE_STROKE   = 300   # specified linear cross-slide travel (mm) — covers both, with margin — reserved

# ── Tilt-swing front board (spherical-pivot adapter on the pinhole frame) ─────
# The board pivots up to FRONT_BOARD_MAX_DEG in tilt AND swing, set by the screw-shoulder
# hard stop: FRONT_BOARD_TRAVEL_MM of linear travel each way at the FRONT_BOARD_ARM_MM pivot
# arm. Resolution is one knurled-knob detent — FRONT_BOARD_CLICK_DEG/click — from the M8×1.0
# fine-pitch screw (FRONT_BOARD_SCREW_PITCH mm/turn) over FRONT_BOARD_DETENTS detents, via the
# same arm. Both ANGLES are COMPUTED from those physical inputs (was hardcoded ±5.3° / 0.012°
# in the tilt-swing generators — component-dependency-map.md §1.4).
FRONT_BOARD_ARM_MM      = 130    # pivot arm — adjustment screw to pivot centre (mm)
FRONT_BOARD_TRAVEL_MM   = 12     # screw-shoulder hard-stop travel each way (mm)
FRONT_BOARD_SCREW_PITCH = 1.0    # M8×1.0 fine-pitch adjustment screw (mm per turn)
FRONT_BOARD_DETENTS     = 36     # knurled-knob detents per turn
FRONT_BOARD_MAX_DEG   = round(math.degrees(math.atan(FRONT_BOARD_TRAVEL_MM / FRONT_BOARD_ARM_MM)), 1)            # = 5.3
FRONT_BOARD_CLICK_DEG = round(math.degrees(math.atan((FRONT_BOARD_SCREW_PITCH / FRONT_BOARD_DETENTS) / FRONT_BOARD_ARM_MM)), 3)  # = 0.012

# ── Derived display figures (COMPUTED from their inputs so the prose figures can't drift) ────
# These appear hand-computed across many reports; deriving them here (and registering as facts)
# means a focal-length or film-size change ripples to every doc that restates them.
BOARD_TILT_REF_DEG   = 5     # round reference tilt for the image-shift unit-rate illustration
IMAGE_SHIFT_PER_5DEG = round(C_WID * math.tan(math.radians(BOARD_TILT_REF_DEG)))   # = 207mm (focal × tan 5°)
FRONT_BOARD_MAX_SHIFT_MM = round(C_WID * math.tan(math.radians(FRONT_BOARD_MAX_DEG)))   # = 219mm — image shift at the ±5.3° hard stop
IMAGE_AREA_SQFT      = round(FP_W * FP_H / 1e6 * 10.7639)                          # = 101 sq ft (active film plane)
XSLIDE_N        = 8     # 2 cross-slides (X + Z) per corner × 4 corners — reserved

# ── Equipment zones ───────────────────────────────────────────────────────────
ZONE_L_END   = FP_X_L    # left zone right boundary X  (= 150mm)  [rev6: was 625]
ZONE_R_START = FP_X_R    # right zone left boundary X  (= 4649mm) [was 4019]

# ── Optical cone helper ───────────────────────────────────────────────────────
def cone_left(y):
    """X coordinate of cone left boundary at depth y from pinhole wall."""
    return PH_X - (PH_X - FP_X_L) * y / FP_Y

def cone_right(y):
    """X coordinate of cone right boundary at depth y from pinhole wall."""
    return PH_X + (FP_X_R - PH_X) * y / FP_Y

# ── Hinged panel — stepped profile (rev 8: housed revolving-door light lock) ──
# rev 8.1: drum, housing, and corner core plates switched from steel to 3mm
# 5052-H32 ALUMINUM to roughly halve the panel+drum mass (~488 → ~286 kg).
# Steel retained for the center RHS frame, seal lips, and bearing stub shafts.
# rev 11: the panel SKINS switched from 18mm marine plywood to HDPE plastic
# sheet (same material as the drum/housing), set in U-channels on the frame faces.
# The frame ENVELOPE is unchanged (40mm corner / 120mm center); only the skin
# material + thickness change, dropping ~44 kg (see hinged-panel-report §2.4–2.5).
# EXCEPTION: an 18mm plywood band stays on the Fan B corner (bottom up to
# PANEL_FAN_BAND_Z) for rigid fan/duct mounting + screw retention.
# Corner zones (Yd=0–653 and Yd=1709–2362): thin framed panel, HDPE skins.
# Center zone (Yd=653–1709): full RHS frame housing the Ø900 light-trap housing.
# rev (2026-07-22): skin firmed to 1/8" (3.18mm) black HDPE — US Plastics 46684
# (nearest imperial stock; all light-lock plastic now one weld-compatible material).
PANEL_CORNER_T    = 40    # corner zone ENVELOPE thickness (mm) — HDPE skin + 1"×1"×1/8" 6061 Al stiffener grid + HDPE skin on a 40mm frame (was a solid 3mm Al core; SS/weight audit 2026-07-29)
PANEL_CENTER_T    = 120   # center zone ENVELOPE thickness (mm) — HDPE skin + 84mm RHS frame + HDPE skin
PANEL_STEP        = PANEL_CENTER_T - PANEL_CORNER_T  # = 80mm step depth
PANEL_SKIN_T      = 3.18  # panel skin thickness (mm) — 1/8" black HDPE (US Plastics 46684; rev11 was 18mm ply, nom 1/8″ HDPE), U-channel set
PANEL_FAN_PLY_T   = 18    # plywood fan-mount band thickness (mm) — local to the Fan B corner only — reserved (spec; band drawn with a literal)
PANEL_FAN_BAND_Z  = 1125  # ply band top Z (AFF) = FAN_B_H(600) + FAN_DIAM/2(75) + 450; literal — fan consts defined below
PANEL_CORNER_YD_L = 653   # corner-to-center transition, near side (mm) [rev8: widened]
PANEL_CORNER_YD_R = 1709  # center-to-corner transition, far side (mm)  [rev8: widened]
PANEL_CENTER_W    = PANEL_CORNER_YD_R - PANEL_CORNER_YD_L  # = 1056mm center zone width
WALL_T            = 40    # container wall envelope depth (mm) — nominal solid block in the 3D models
# Container side-wall corrugation depth — the grip a wall through-bolt spans (peak-to-valley + skins).
# ISO side walls are ~25mm (1"), 25–30mm range; end walls ~36mm trapezium (1.6/2.0mm sheets). Wall
# through-bolts pass the long SIDE walls → design for the 30mm worst case and pad with flat washers
# if the actual container measures shallower. MEASURE the real container to confirm before ordering.
CONTAINER_CORRUGATION_DEPTH = 30   # mm — side-wall corrugation, conservative max of the 25–30mm ISO range

# ── Rotating cargo-door panel — transport mode (rev 10: supersedes the B2 slide) ──
# The panel + drum + drum-cage assembly ROTATES ~56° about a VERTICAL pivot — the
# film-plane far-left upright, reused as a Ø89 CHS post — swinging the protruding Ø900
# light-trap bay inboard of the door plane so the ISO cargo doors can close. The panel
# is split into THREE zones: a FIXED LEFT strip (Yd0–PANEL_CUT_YD) + the SWINGING part
# (PANEL_CUT_YD→PIVOT_YD) + a FIXED FAR strip (PIVOT_YD→C_WID). The two LEFT film rails
# are removable (drop-in saddles) and the left walkway lifts out before the swing; a
# top+bottom wall-stay locks the swung assembly. Carried by the pivot post on a thrust
# collar + top/bottom hub bearings (no ceiling suspension, no slide).
# See docs/superpowers/specs/2026-06-08-cargo-door-rotating-panel-design.md.
# RETIRED with the slide: PANEL_SLIDE, HGR20 carriage rails, Destaco locks, the ceiling-
# rail suspension, the barrel hinges + swing-support caster.
SWING_LOCK_DEG = 56     # transport swing angle, locked (clears the door plane; the resulting
                        # clearance is computed as SWUNG_DOOR_CLEARANCE_MM, below)
PANEL_CUT_YD   = 180    # fixed-left-panel width / swing cut (mm) — 160 min to clear the near
                        # upright at Yd100, 180 for margin. Swinging part runs PANEL_CUT_YD→PIVOT_YD.
PIVOT_POST_OD  = 89     # Ø89×8 CHS pivot post (mm) — carries the ~3.6kN·m swing cantilever, SF~3.7 (S355)
PIVOT_POST_T   = 8      # pivot post wall thickness (mm)
PANEL_FLOOR_GAP   = 130   # gap between panel bottom edge and floor (mm). NOT tied to WALKWAY_H (deck is
                          # now 140 with the 25mm grate): the swing sweeps the BARE Z115 brackets (walkway
                          # lifted out for transport), so this stays 130. Drum-revolve threshold sill +
                          # swing-arc datum. A ~10mm step to the Z140 deck at the drum exit is accepted
                          # (add a 10mm drum-floor pad later if it matters).
# (Derived swing geometry — PIVOT_X/PIVOT_YD/FAR_STRIP_YD0/DRUM_CAGE_* — is defined just
#  below, after the brace/drum/bay constants it reads from.)
# PANEL_SLIDE (the old 880mm slide travel) is fully retired (rev10) — all generators and
# models have migrated to the swing; no consumer remains.

# ── Left end zone — housed revolving-door light lock (rev 8) ─────────────────
# Personnel light lock in the hinge-panel center zone: a FIXED Ø900 housing with
# two opposed 80° openings (exterior face + interior face onto the walkway) and a
# single-opening C-shell drum (Ø864, ~Ø850 bore) rotating inside on SKF 6215
# bearings. No internal fins — light-tight by geometry (openings <90°, 180° apart,
# so the drum opening can never bridge both at once). Replaces the failed Ø750
# 4-fin drum. See light-trap-selection.md / hinged-panel-report.md §3.
DRUM_CX    = -400    # light-lock center X (mm) [rev9 B2: 0→-400 — offset out via the
                     # hinge-panel punch-out bay so the housing interior edge (+50)
                     # clears the X=150 film-plane left rail by ~100mm]
DRUM_D     = 900     # fixed housing OUTER diameter (mm) [rev8: was Ø750 drum]
                     # rev8: reviewed & KEPT — ~555mm passage (sideways entry), accepted
                     # for occasional single-operator field use; larger Ø deferred
DRUM_R     = DRUM_D // 2                      # 450 — housing radius (visible footprint)
DRUM_H_LT  = 2250    # light-lock TOP Z (mm) — LIFTED +50 with the walkway (was 2200) so the
                     # interior height (DRUM_H_LT − PANEL_FLOOR_GAP = 2120) is PRESERVED: 340mm
                     # headroom over a 1780mm operator standing on the raised (Z130) walkway;
                     # top clears the ceiling (2388) by 138mm.
LT_HOUSING_R   = DRUM_R   # 450 — fixed housing radius
LT_HOUSING_T   = 5        # housing wall (mm) [rev9 B2: 3mm Al → 5mm UV-HDPE plastic skin]
LT_DRUM_OR     = 432      # rotating drum outer radius (Ø864) — 15mm running gap
LT_DRUM_T      = 3.18     # drum wall (mm) [rev9 B2: 3mm Al → 1/8″ HDPE; 2026-07-22: 1/8" HDPE, US Plastics 46684 — weld-compatible with the 3/16" HDPE housing]
LT_CAP_T       = 4.76     # drum top/bottom cap thickness (mm) — 3/16" HDPE, THICKER than the 1/8" shell: the caps carry the steel stub shafts into the SKF 6215 bearings (structural hub load path). Cut from the housing 46685 offcut (no extra sheet).
LT_OPENING_DEG = 80       # each opening arc, degrees (<90° for light-tightness)

# ── B2 punch-out bay (rev9) — the hinge-panel center zone protrudes forward,
# enclosing the offset housing, so the film-plane rails stay internal.
# See docs/superpowers/specs/2026-06-05-lighttrap-punchout-bay-design.md.
BAY_FRONT_X = DRUM_CX - DRUM_R - 40   # -890 — bay outer (exterior) face
BAY_BACK_X  = 0                        # bay meets the panel side-zone door plane
BAY_WALL_T  = 3.18                     # bay box wall thickness (mm) — 1/8" HDPE, US Plastics 46684 (2026-07-22; was 6mm nom); 4-wall corner-welded box + EPDM lip gives the rigidity, not the skin gauge

# ── Film-plane demountable brace cage (rev: rigidity + drum + walkway) ────────
BRACE_RHS   = 50                     # brace member section 50×50×3mm RHS (mm)
BRACE_T     = 3                      # RHS wall thickness (mm)
BRACE_Z_BOT = RAIL_OFF_BOT           # 150mm — bottom cross-beam Z (raised +50 to clear the Z130 walkway)
BRACE_Z_TOP = C_HGT - RAIL_OFF_TOP   # 2244mm — top cross-beam Z (dropped 44mm with the film-plane top rail)
# End portals sit at the rail travel limits (already defined): FP_Y_MIN, FP_Y.

DRUM_CY     = C_WID // 2             # 1181mm — light-lock center in Yd (= container width center)
# B2 (rev9): the drum is offset clear of the X=150 rail (via the punch-out bay), so the
# left film-plane rail is CONTINUOUS (one piece, no demountable mid-segment). rev10: that
# whole left rail pair (TL+BL) is REMOVABLE for transport — it lifts straight up out of
# drop-in saddles so the swinging drum cage can transition the X=150 rail plane, then
# re-seats to the film datum on tapered dowels.

# ── Rotating-panel swing geometry (derived — reads brace/drum/bay above) ─────
# The transport-mode policy constants (SWING_LOCK_DEG, PANEL_CUT_YD, PIVOT_POST_*) are up
# in the hinged-panel block; these are the derived positions.
PIVOT_X        = RAIL_X_L + BRACE_RHS // 2   # 175 — swing axis X (center of the film far-left upright)
PIVOT_YD       = FP_Y + BRACE_RHS // 2       # 2287 — swing axis Yd
FAR_STRIP_YD0  = PIVOT_YD                     # 2287 — fixed FAR strip spans PIVOT_YD..C_WID (~75mm);
                                             # ends the swinging panel AT the pivot so nothing swings
                                             # outboard of the door plane (#10)
# Drum support CAGE — steel box around the Ø900 drum; swings with the assembly and carries
# the drum revolve bearings. Full depth (Z PANEL_FLOOR_GAP..DRUM_H_LT) to react the drum
# overturning moment. Fine hardware (bearing Ø, stay plates/bolts, saddle/dowel dims) lives
# in the lighttrap builder, cited from the design spec.
DRUM_CAGE_X0   = BAY_FRONT_X            # -890 — cage outer face (= bay front)
DRUM_CAGE_X1   = 50                     # cage inner face (just past the panel)
DRUM_CAGE_YD_L = DRUM_CY - DRUM_R - 31  # 700 — cage side ~30mm clear of the Ø900 housing
DRUM_CAGE_YD_R = DRUM_CY + DRUM_R + 31  # 1662

# Transport swung-panel door clearance — the bay front-right corner (BAY_FRONT_X, PANEL_CORNER_YD_R),
# the outermost point of the swept assembly, rotated SWING_LOCK_DEG about the pivot lands at this X.
# Its (positive) value is how far the swung frame sits INBOARD of the closed door plane (X=0) — the
# true minimum clearance. COMPUTED from the swing geometry so it can't drift (was hardcoded +59 in
# labels + ~8 docs). = 59 (precise 58.6).
SWUNG_DOOR_CLEARANCE_MM = round(
    PIVOT_X + (BAY_FRONT_X - PIVOT_X) * math.cos(math.radians(SWING_LOCK_DEG))
            - (PANEL_CORNER_YD_R - PIVOT_YD) * math.sin(math.radians(SWING_LOCK_DEG)))

# Evaporative cooler — external mount (rev 7: was interior on pinhole wall)
# Cooler ground-placed outside container, connected via 200mm flex duct
# through pinhole wall, Z-centered with ext power panel, 150mm gap to its left.
# PRODUCT (dimension-audit resolution): Hessaire MC18M, 120V AC 85W / 1300 CFM
# (run on LOW to match the Ø200 duct), fed by an internal 12V→120V inverter on
# Circuit E.  Replaces the fictional "Portacool Jetstream 110 12V DC". 508×254×711.
EVAP_DUCT_X  = 1000    # duct penetration center X (mm) — 150mm left of ext power panel edge
EVAP_DUCT_Z  = 1900    # duct penetration center Z (mm) — Z-centered with ext power panel
EVAP_DUCT_D  = 200     # duct outer diameter (mm)
# Physical dimensions (used for transport stowage sizing) — real Hessaire MC18M
EVAP_W     = 508     # cooler width along X (mm)  — 20 in
EVAP_D     = 254     # cooler depth along Yd (mm) — 10 in
EVAP_H     = 711     # cooler height (mm)         — 28 in
EVAP_CFM_RATED = 1300  # Hessaire MC18M rated airflow (CFM); run on LOW to match the Ø200 duct
# Transport stowage — on near walkway grating, in the widened section.
# rev10: moved deeper (was 1200) to clear the panel SWING sweep, which reaches
# X≈1395 in the near-walkway Yd band; 1450 gives margin (cooler X1450–2009,
# inside the wide section X1155–2629).  Lighter unit now (16 lb / Hessaire MC18M).
EVAP_STOW_X    = 1450    # stowage left edge X (mm)
EVAP_STOW_YD   = 0       # against pinhole wall (Yd=0)
EVAP_STOW_Z    = 160     # sits on raised grating surface (WALKWAY_H 140 + 20mm pad) [+10 for 25mm grate]

# ── Inverter — Circuit E 12V→120V AC for the evaporative cooler ───────────────
# Victron Phoenix 12/375 (GFCI version): 235×120×72mm, ~2.3kg.  Wall-mounted
# INSIDE the container on the pinhole wall, below the electrical panel (EP) and
# above the battery bank — short DC run to the battery, GFCI AC out to the
# external power panel.  See electrical-report.md §AC isolation & safety.
INVERTER_X   = 1829    # left edge X (mm) — at the EP column left; keep synced with EP_X (defined below, so can't reference it here)
INVERTER_Z   = 760     # bottom Z (mm) — reach re-lay: dropped into the reach zone just above the contactor (724); 235 tall → top 995
INVERTER_W   = 120     # width along X (mm)
INVERTER_H   = 235     # height (mm)
INVERTER_D   = 72      # protrusion from pinhole wall (Yd, mm)

# Circuit E power — the Hessaire MC18M draws 85W AC; on the 12V battery bus through the
# 12V→120V inverter that is 85 ÷ 0.88 efficiency = 97W. COMPUTED so the bus draw can't drift
# (was a literal COOLER_W=97 in calculate_energy_budget + restated raw in ~6 docs).
EVAP_COOLER_W_AC    = 85      # Hessaire MC18M datasheet AC draw (run on low)
INVERTER_EFFICIENCY = 0.88    # Victron Phoenix 12/375 pure-sine efficiency
EVAP_COOLER_W_BUS   = round(EVAP_COOLER_W_AC / INVERTER_EFFICIENCY)   # = 97 (12V-bus draw)

# ── External power panel (pinhole wall exterior, near EP) ─────────────────────
PWR_PANEL_X = 1250   # power panel left edge X (mm) — just left of EP
PWR_PANEL_W = 340    # face plate width (mm)
PWR_PANEL_H = 240    # face plate height (mm)
PWR_PANEL_Z = 1830   # face plate bottom Z (mm) — exterior; kept here (no beam clash). NOTE: the interior
                     # EP DROPPED 150 in rev11 for brace-beam clearance, so it's no longer co-centered.
PWR_PANEL_D = 3      # front-face flange plate thickness (mm) — fabricated steel plate
PWR_PANEL_CUTOUT_W = 280   # wall cutout width (mm) — 30mm flange overlap each side
PWR_PANEL_CUTOUT_H = 180   # wall cutout height (mm)
PWR_PANEL_BOX_D    = 90    # penetration-box shroud depth (mm) — flange face -> interior
                           # opening; spans the corrugated wall + sits slightly proud inside
PWR_PANEL_SHROUD_T = 8     # shroud side-wall thickness (mm)

# ── Pinhole wall face (Y = 0, shadow-free) ────────────────────────────────────
EP_X       = 1829    # electrical panel/column left edge X (mm) — set so the column right edge
                     # (EP_X + EP_COL_W = 2169) sits at the widened-walkway right overhang limit
                     # (cantilever X2069 + 100mm max grate overhang); clears the pinhole (X2399).
                     # The transport-stay anchor follows: `wall_anchors()` clamps its right edge
                     # to ≤ EP_X−15 (X≤1814) so it stays clear of the column. [walkway-punchout fit]
EP_W       = 300     # electrical panel width (mm)
EP_H_LO    = 1150    # IP65 enclosure / fuse-busbar zone bottom Z (mm) — REACH RE-LAY: dropped from 1500
                     # so the Blue Sea 5026 fuse block sits at chest height (serviceable, no stool). The
                     # disconnect cluster is below (EP_DISC_Z), the MPPT above (to EP_H_HI). [was 1500/1650/900]
EP_H_HI    = 1560    # electrical panel top Z (mm) — REACH RE-LAY: MPPT top now no-stool reachable (was 2100)

BA_X       = EP_X    # battery bank left edge X (mm) — in the EP skinny column (= EP_X); the 2 packs STACK vertically (was 1540, 680-wide side-by-side, before the skinny-column reorg)
BA_W       = 260     # battery bank width (mm) — 1× Renogy 100Ah Core (260 long); the 2 packs STACK vertically (BA_STACK_Z2), not side-by-side
BA_H_LO    = 160     # battery bank bottom Z (mm) — sits on a 20mm pad on the Z140 grate deck [+10 for 25mm grate; was 150]
BA_H_HI    = BA_H_LO + 211   # LOWER pack top Z (mm) = 160 + 211 (real Renogy 100Ah Core height); the upper pack stacks above (BA_STACK_TOP)
BA_D       = 169     # battery bank depth from wall (mm) — real Renogy 100Ah Core width (side busbar terminals; the rev7 'slim-profile 120mm' assumption was wrong — see component-dimension-audit.md)

# ── EP skinny-column layout (2026-07-06) — the EP is a tall NARROW column shifted left so it fits
# inside the cantilever-limited widened walkway (column right edge = cantilever X2069 + 100mm = X2169);
# the transport-stay anchor (X≤1814) follows it, the pinhole is at X2399. Packs STACK vertically (BA_W wide).
EP_COL_W     = 340                         # EP column width (mm) — fits one stacked battery pack
BA_STACK_Z2  = BA_H_HI + 16                # 380 — upper (2nd) pack bottom Z (stacked on the lower pack)
BA_STACK_TOP = BA_STACK_Z2 + (BA_H_HI - BA_H_LO)  # 594 — battery stack top Z
EP_POST_Z    = BA_STACK_TOP + 20           # 614 — contactor / MRBF sit above the battery stack
EP_RISE_X_P  = EP_X + 260                  # 2170 — (+) 2/0 cable riser lane (right of the PV disconnect)
EP_RISE_X_M  = EP_X + 140                  # 2050 — (−) 2/0 cable riser lane (inverter ↔ PV disconnect gap)
PV_DISC_X    = EP_X + 165                  # 2075 — PV array-disconnect X (operator-reach switch)
EP_DISC_Z    = 1045                        # disconnect cluster row Z — main + master + PV disconnects grouped, reachable (~chest)
PV_DISC_Z    = EP_DISC_Z                    # PV array-disconnect — in the disconnect cluster row

# ── Solar array — 3× 200W mono on a 30° ground tilt frame (electrical 3D model) ──
# Ground-placed on the pinhole-wall exterior side (Yd<0), toward the door end so the
# right edge (X≈2350) stays clear of the pinhole sightline at X=2399. Panels portrait
# (680 along X), 1480 up the tilt.  Consumed by generate_electrical_model.py.
SOLAR_PANEL_L  = 1480    # panel long dim (mm) — up the tilt
SOLAR_PANEL_W  = 680     # panel short dim (mm) — along X
SOLAR_PANEL_T  = 35      # panel thickness (mm)
SOLAR_N        = 3       # number of panels
SOLAR_TILT_DEG = 30      # tilt from horizontal (facing away from the container)
SOLAR_GAP      = 30      # gap between panels along X (mm)
SOLAR_ARRAY_X  = 250     # array left edge X (mm) — door end; right edge ≈2350 < pinhole 2399
SOLAR_ARRAY_YD = -900    # array near-edge stand-off from the pinhole wall (mm, exterior)
SOLAR_ARRAY_Z  = 0       # array base on the ground

# ── Main enclosure internals — shown in the electrical model's "Power Core" scene ──
# Placed within the EP volume (EP_X..EP_X+EP_W, Yd 0..ENCL_SHELL_D, EP_H_LO..EP_H_HI).
# Sizes only; positions computed in the builder. Consumed by generate_electrical_model.py.
ENCL_SHELL_D   = 165     # ghosted IP65 enclosure depth into the container (Yd, mm)
MPPT_W, MPPT_D, MPPT_H          = 185, 70, 100   # Victron SmartSolar 100/50 MPPT
FUSEBLK_W, FUSEBLK_D, FUSEBLK_H = 164, 39, 84    # Blue Sea 5026: 6.472×1.518×3.315" = 164(X)×39(Yd,proud)×84(Z), 12-circuit, flip cover + neg bus [datasheet]
BUSBAR_L, BUSBAR_W, BUSBAR_H    = 120, 20, 22    # + / − distribution busbars
DISCONNECT_D, DISCONNECT_H      = 70, 60         # Blue Sea m-Series rotary disconnect (knob)
CONTACTOR_W, CONTACTOR_D, CONTACTOR_H = 120, 90, 100  # Blue Sea ML-RBS contactor
MRBF_D, MRBF_H = 40, 38  # terminal-mount MRBF main fuse (on the battery + post)

# ── Equipment panel — IBC plumbing corridor (rev 7: walkway reorg) ───────
# 18mm marine ply panel spanning ACROSS the IBC plumbing corridor (Yd
# direction), perpendicular to the sealed end wall.  Panel face (equipment
# side) faces the open end (lower X = accessible from walkway).  Equipment
# protrudes from panel face toward open end.
# Contains pumps (P-01, P-02, P-04), ACC-01, and 3× Big Blue filter housings.
# Pumps on near-wall side (Yd=1046–1173), filters on far-wall side (Yd=1186–1316).
# Filters at bottom of panel (Z=200–1280), pumps at top (Z=1320–2220).
EQPANEL_X       = 4874    # panel face X (mm) — ibc-reconfig-v2: moved FORWARD (was 5240) to the corridor front for walkway/operator reach-in access; ply X=4874–4892, equipment hangs toward -X (tip ~4744, clear of the film rail X=4649). Mounts on the deep-box corridor frame (front upright ~X4654).
EQPANEL_T       = 18      # panel thickness in X (mm) — ply extends toward sealed end (X=4874–4892)
EQPANEL_Z_LO    = 250     # panel bottom Z (mm) — keeps ~120mm above the raised walkway deck [+50 raise; was 200]
EQPANEL_Z_HI    = 2310    # panel top Z (mm) — in the plumbing corridor (no totes there), below ceiling (2388); IBC stack is 2336mm in the flanking columns
EQPANEL_H       = EQPANEL_Z_HI - EQPANEL_Z_LO   # = 2060mm

# IBC plumbing corridor dimensions (derived from IBC layout: Yd=30+1016=1046 to 1316)
CORRIDOR_YD_NEAR = 1046    # near IBC column far face Yd (mm) — BLUE_IBC_Y + IBC_D
CORRIDOR_YD_FAR  = 1316    # far IBC column near face Yd (mm) — IBC_FAR_Y
CORRIDOR_W       = CORRIDOR_YD_FAR - CORRIDOR_YD_NEAR  # = 270mm

# Panel Yd extent (spans full corridor, perpendicular to container walls)
EQPANEL_YD       = CORRIDOR_YD_NEAR     # = 1046 — near edge Yd
EQPANEL_YD_FAR   = CORRIDOR_YD_FAR      # = 1316 — far edge Yd
EQPANEL_YD_SPAN  = CORRIDOR_W           # = 270mm — panel width in Yd

# Backward-compatible X footprint for elevation views (left-edge + width)
EQPANEL_W       = EQPANEL_T + 130   # = 148mm — total X footprint (ply + max protrusion BB_OD)

# Pump zone — near side of panel face (Yd=1046–1173)
# Pumps protrude from panel face toward open end (lower X).
PUMP_D       = 114     # pump protrusion from panel face in -X direction (mm) — real Shurflo 2088 height (4.5"); was 100
PUMP_YD_SPAN = 127     # pump body width in Yd direction (mm) — Shurflo 2088 width
PUMP_X       = EQPANEL_X - PUMP_D   # = 4900 — pump zone left edge X for elevation views
PUMP_W       = PUMP_D               # = 100 — pump zone width in X for elevation views
PUMP_H_LO    = 1370    # pump zone bottom Z (mm) — above filter stack + 40mm gap [+50 walkway raise; was 1320]
PUMP_H_HI    = 2270    # pump zone top Z (mm) — includes ACC-01 top [+50 walkway raise; was 2220]
PUMP_YD      = CORRIDOR_YD_NEAR  # pump zone near edge Yd (mm) — near side of corridor
# P-01 (Blue supply), P-02 (Brown recycle), P-04 (Tray drain) on equipment panel.
# P-03 (waste evacuation) on X4 drain run in IBC plumbing corridor.
# ACC-01 accumulator mounted adjacent to P-01 on panel.

# ── Chemistry prep shelf — WALL-HINGED FOLD-DOWN (rev13) ──────────────────────
# Mixing-only shelf (cyanotype chemistry, BEFORE exposure), so it need not be
# permanently deployed.  A PIANO HINGE along the BACK edge on the pinhole wall (Yd0)
# carries it: IN USE it folds DOWN to horizontal at work height (Z=SHELF_H), held
# level by a pair of STAYS from the wall above (they carry the shelf + chemistry
# load).  For TRANSPORT / during exposure it folds UP flat against the wall (top at
# SHELF_STOW_TOP_Z).  Because it is only deployed while mixing (film plane parked),
# it is FULLY DECOUPLED from the film-plane swing — retiring the old ceiling-hung
# shelf and its swing/optics constraints.  Located in the WIDENED near walkway,
# LEFT of the battery bank (BA_X=1810); the evap cooler (stow top Z950) slides under
# the deployed shelf (underside Z1050).
SHELF_X_L      = 1180    # shelf left edge X (mm) — widened walkway, left of the batteries
SHELF_X_R      = 1780    # shelf right edge X (mm)
SHELF_W        = 600     # shelf width along X (mm)
SHELF_YD_NEAR  = 0       # back edge — hinged on the pinhole wall (Yd0)
SHELF_DEPTH    = 225     # shelf depth in Yd (deployed projection) — reduced 300→225 for more walk-around clearance at the chem shelf (275mm past the shelf back to the widened deck edge)
SHELF_YD_FAR   = SHELF_YD_NEAR + SHELF_DEPTH   # front edge when deployed (= 225; derived so it can't drift from SHELF_DEPTH)
SHELF_H        = 1075    # deployed work-surface height AFF (mm) — 945mm above the walkway deck
SHELF_T        = 22      # shelf total thickness (mm) — 18mm ply + 4mm frame
SHELF_STAY_N   = 2       # support stays (wall-above to front corners; carry the load)
SHELF_STOW_TOP_Z = SHELF_H + SHELF_DEPTH  # 1375 — folded-up (transport) top; the tap top aligns here

# Ceiling pull-cord (light switches D/G) bottom Z — the cords hang in the chem-shelf
# footprint (X1180–1780), so they end ABOVE the deployed shelf top (SHELF_H + 15 lip)
# with clearance instead of dropping through it. Shared by the overview 3D model + the
# 2D pinhole-wall elevation + electrical Sheet 3 so the cord length stays in sync.
PULL_CORD_BOTTOM_Z = SHELF_H + 105   # 1180 — pull-cord bottom Z (clears the shelf)

# ── Chemistry prep tap (pinhole wall, tees off blue supply line) ─────────────
TAP_X          = 1130    # tap X (mm) — relocated LEFT of the shelf (battery bank is to the right) [rev13; was 3729]
TAP_Z          = 1150    # spout outlet height AFF (mm) — ~75mm above the shelf; the riser tops at SHELF_STOW_TOP_Z (1375)
TAP_PIPE_OD    = 25      # branch pipe OD (mm) — 3/4" PVC Sch-40
TAP_WALL_T     = 3       # branch pipe wall thickness (mm) — reserved (spec; not yet drawn)


# ── Big Blue filter housings — physical dimensions (3× separate units) ──────
# Mounted on the PINHOLE-WALL panel (positions single-sourced in the PWP_* block below).
# Flow: IBC-3 → P-02 → F-01 → F-02 → F-03 → SV-01 → DV-01.

# Big Blue 4.5"×10" housings (physical dimensions — 3× separate units)
BB_OD          = 184     # housing outer diameter (mm) — real Big Blue 4.5x20 housing is Ø7.25"=184 (diameter is the same 10"↔20"; only length changes)
BB_H           = 594     # housing total height (mm) — head + sump bowl (4.5×20 Big Blue = 23⅜"; per component-dimension-audit); was 340 for the 10" housing.
#   Heads are pinned near the ceiling (Z2340), so the extra length hangs DOWN — the sump bottom drops to ~Z1746
#   (~1,616mm walkway headroom, shoulder height for the 1.75m operator). Doubles filter media / interval; revert to 340 if the head clearance becomes an operational issue.

# ── Pinhole Wall Plumbing Panel — wet-end filter loop positions (SINGLE SOURCE) ──────────────
# The pinhole-wall-mount refactor put the filter loop on the PINHOLE WALL (Yd≈0 side): the 3-stage
# Big Blue bank rides HIGH under the ceiling; P-02 sits to its left (low-X, furthest from the IBCs);
# SV-01 drops to waist.  These constants are the ONE home for those X/Z positions — consumed by
# generate_pinhole_water_panel.kit() (3D), generate_panel_layout (pinhole-panel 2D),
# generate_pinhole_wall_elevation (elevation) and generate_electrical_model (P-02 feed tap).
# (The FSKID_X/F1_Z/F2_Z/F3_Z block ABOVE is the OLD corridor layout — still consumed by the overview /
#  assembly-overview / electrical-diagram, which have NOT yet moved to the pinhole-wall design.)
PWP_FILTER_X1     = 3300                        # F-01 center X (mm)
PWP_FILTER_PITCH  = 338                         # F-01 -> F-02 -> F-03 center-to-center X spacing
PWP_FILTER_X2     = PWP_FILTER_X1 + PWP_FILTER_PITCH        # = 3638
PWP_FILTER_X3     = PWP_FILTER_X1 + 2 * PWP_FILTER_PITCH    # = 3976
PWP_FILTER_TOP_Z  = C_HGT - 48                  # = 2340 — filter head top (pinned just under the ceiling)
PWP_FILTER_BOT_Z  = PWP_FILTER_TOP_Z - BB_H     # = 1746 — filter sump bottom
PWP_FILTER_HEAD_Z = PWP_FILTER_TOP_Z - 78       # = 2262 — head/sump split (cap height 78)
PWP_FILTER_CAP_Z  = PWP_FILTER_TOP_Z - 39       # = 2301 — in-line port centerline (cap_h/2)
PWP_FILTER_YD     = BB_OD // 2 + 12             # = 104 — filter center Yd (sump back near the wall)
PWP_P02_X         = PWP_FILTER_X1 - (BB_OD // 2 + 30) - 120  # = 3058 — P-02's old wall center; NOW the ACC-02 anchor (P-02 relocated to the corridor 2026-08-05)
PWP_P02_H         = 180                          # P-02 body height (matches cp.PVB_H)
PWP_P02_Z0        = PWP_FILTER_CAP_Z - (PWP_P02_H - 18)      # reserved — = 2139, P-02's old wall body bottom (P-02 relocated to the corridor 2026-08-05; kept as the vacated-spot reference)
PWP_SV01_X        = 4250                         # SV-01 pH sample tap X
PWP_WAIST_Z       = 1000                         # DV-01 reach height (waist); was also SV-01 before the skid reorg
PWP_SV01_Z        = 1610                          # SV-01 valve-center Z — raised beside F-3 in the 2026-08-04 skid reorg (was PWP_WAIST_Z)
# ── Filter-skid panel layout (2026-08-04 reorg) — single-sourced so the 2D panel diagrams match water.skp ──
PWP_PANEL_X0      = 2780                          # ply left edge (low X)
PWP_PANEL_X1      = 4575                          # ply right edge (high X, walkway side)
PWP_PANEL_Z0      = 920                           # ply bottom edge (Z AFF)
PWP_SROW_Z0       = 1150                          # skid-row base Z (P-04·SV-02·DV-02 under the filters)
PWP_SV02_Z        = PWP_SROW_Z0 + 132             # 1282 — SV-02 valve-center Z (in-line on the P-04→DV-02 row)
PWP_DV02_Z        = PWP_SROW_Z0 + 162             # 1312 — DV-02 valve-center Z (= P-04 OUT / row line)
PWP_ACC2_X        = (PWP_PANEL_X0 + PWP_PANEL_X1) // 2 + 180   # 3857 — ACC-02 (recycle-spray damper) center X
PWP_ACC2_Z0       = PWP_PANEL_Z0                  # 920 — ACC-02 base sits on the panel bottom

# Pump manifold pipe (1/2" PVC Sch-40)
PUMP_PIPE_OD   = 21      # 1/2" nominal HDPE OD (mm)
PUMP_PIPE_WALL = 3       # pipe wall thickness (mm)

# ���─ Right end zone — 4 IBCs in 2×2 stack (rev 5) ────────────────────────────
# Right-justified to far end wall: X=4674–5893mm.
# Layout (view from pinhole wall):
#   TOP    Blue #1 (near)     Blue #2 (far)    ← gravity feeds spray bar
#   BOTTOM Brown   (near)     Waste   (far)    ← receives water by gravity
# Weight migrates top→bottom during session (stability improves).
IBC_COL_X   = ZONE_R_START + 25   # = 4674mm  [right-justified to end wall]
IBC_W       = 1219   # IBC overall width  (mm) — US 48" pallet format, includes cage
IBC_D       = 1016   # IBC overall depth  (mm) — US 40" pallet format, includes cage
IBC_H_600   = 1010   # 640L IBC overall height (mm) — includes pallet base + cage + bottle
IBC_H_STK   = 2020   # 2× stacked height (mm)
# ibc-reconfig-v2 (2026-06): all four positions standardize on the 275-gal (≈1000 L)
# caged composite — the only food-grade, 48×40-footprint tote our supplier (Container
# Exchanger) stocks; a compatible 600 L tote does NOT exist, so "600 L"/"1000 L" are
# FILL LEVELS, not tote sizes. Caged-composite 275-gal = 48×40×46" = 1219×1016×1168 mm
# (NOT the taller 53.75-56" square-stackable poly line). The totes' own cage frames
# DIRECT-STACK cage-on-cage to 2336 mm → only ~52 mm headroom under the 2388 mm ceiling
# (so the support frame is RESTRAINT-ONLY — no load-bearing deck between tiers).
# Layout is UNCHANGED from main: two Blue on top, Brown + Waste on the bottom.
IBC_H_1000  = 1168   # 275-gal (≈1000 L) caged composite overall height (mm) = 46"
IBC_H_STK_1000 = 2 * IBC_H_1000   # 2336 mm 2× stacked
IBC_CEILING_CLEARANCE_MM = C_HGT - IBC_H_STK_1000   # = 52mm — direct-stack ceiling headroom (was restated raw in ~5 docs)

# IBC cage/pallet anatomy (US 48"×40" composite tote)
# Three parts: steel/plastic pallet base, HDPE blow-molded bottle, galvanized wire cage.
IBC_PALLET_H    = 168    # pallet base height including feet/runners (mm)
IBC_CAGE_TUBE_D = 25     # cage corner upright tube OD (mm)
IBC_CAGE_RAIL_W = 25     # cage top rail tube OD (mm)
IBC_CAGE_INSET  = 15     # cage tube center inset from pallet edge (mm)
IBC_BOTTLE_INSET = 30    # bottle wall inset from pallet edge (mm)
IBC_VALVE_Z     = 185    # DN50 butterfly valve CL above IBC base (mm)

# Near column (Yd=30–1046mm): Blue #1 on top, Brown on bottom
BLUE_IBC_Y  = 30     # near column Yd start (mm) — pushed to near wall, 30mm clearance
BROWN_IBC_Y = BLUE_IBC_Y   # Brown is directly below Blue #1 (same Y column)

# Far column (Yd=1316–2332mm): Blue #2 on top, Waste on bottom
IBC_FAR_Y   = 1316   # far column Yd start (mm) — pushed to far wall, 30mm clearance
# Central plumbing corridor: Yd=1046–1316 (270mm wide)
WASTE_IBC_Y = IBC_FAR_Y   # Waste is directly below Blue #2 (same Y column)

# IBC right edge: IBC_COL_X + IBC_W = 4674 + 1219 = 5893mm = C_LEN ✓
# Stack height (v2 1000L direct-stack): 2 × 1168 = 2336mm  (ceiling 2388mm → 52mm headroom ✓)
# (legacy "600L" stack was 2 × 1010 = 2020mm — see IBC_H_600 / IBC_H_STK below)

# ── IBC stacking-frame structural securing (rev 10: simple-span retrofit) ─────
# The upper-tote platform cross-beams are SIMPLY SUPPORTED wall-to-wall: propped
# at the two corridor uprights AND at the container side walls via welded seat
# brackets (no longer cantilevered). Floor flange feet anchor the uprights down.
# These mirror src/models/generate_sketchup_model.py → ibc_rack().
IBC_FRAME_RHS      = 50    # 50×50×3mm RHS section size (mm)
IBC_FRAME_T        = 3     # RHS wall thickness (mm) — reserved (spec; not yet drawn)
# Floor feet — one under each of the 4 corridor uprights
IBC_FOOT_PLATE     = 150   # square floor flange plate side (mm)
IBC_FOOT_PLATE_T   = 12    # flange plate thickness (mm)
IBC_FOOT_BOLT_D    = 12    # M12 floor anchor bolt
IBC_FOOT_BOLT_PCD  = 100   # bolt square pitch on flange (mm) — ±50mm from CL
IBC_FOOT_BOLT_N    = 4     # anchor bolts per foot
# Welded wall seat bracket — props each platform-beam OUTER end at the side wall
IBC_WBKT_PLATE_W   = 150   # back-plate width along X (mm)
IBC_WBKT_PLATE_T   = 8     # back-plate / gusset web thickness (mm)
IBC_WBKT_SEAT_PROJ = 110   # horizontal seat projection into container (mm)
IBC_WBKT_SEAT_T    = 10    # seat plate thickness (mm)
IBC_WBKT_GUSSET_H  = 200   # triangular gusset web depth down the back-plate (mm)
IBC_WBKT_BOLT_D    = 12    # M12 wall anchor bolt
IBC_WBKT_BOLT_N    = 4     # wall bolts per bracket

# Equipment-panel support frame — the wet-end panel is pushed back to butt the
# film-plane (-X) face of the MIDDLE corridor upright station, which is extended
# up to the panel top and closed into a rectangle (two corridor uprights + top
# rail + floor-level beam) that the panel bolts to. Mirrors ibc_rack().
PANEL_FRAME_X      = IBC_COL_X + IBC_W // 2 - IBC_FRAME_RHS // 2  # 5258 — middle corridor X-station (RHS -X edge)
PANEL_FRAME_TOP_Z  = EQPANEL_Z_HI   # 2310 — extended uprights / top rail level
PANEL_FRAME_YD_N   = CORRIDOR_YD_NEAR  # 1046 — near corridor upright — reserved (alias; code uses CORRIDOR_YD_NEAR)
PANEL_FRAME_YD_F   = CORRIDOR_YD_FAR   # 1316 — far corridor upright — reserved (alias; code uses CORRIDOR_YD_FAR)

# ── Processing tray — permanently installed in optical zone (rev 5) ──────────
PROC_TRAY_X_L  = FP_X_L + 20    # = 170mm — 20mm clearance from left rail [rev6: was 645]
PROC_TRAY_X_R  = FP_X_R - 20    # = 4629mm — 20mm clearance from right rail
PROC_TRAY_W    = PROC_TRAY_X_R - PROC_TRAY_X_L   # = 4459mm [rev6: was 3984]
PROC_TRAY_D    = 2200            # depth in Y direction (mm)
PROC_TRAY_YD_NEAR = 80           # tray near edge Yd (mm) — clearance from pinhole wall
PROC_TRAY_YD_FAR  = PROC_TRAY_YD_NEAR + PROC_TRAY_D  # = 2280mm
PROC_TRAY_RIM  = 50              # rim height (mm)
PROC_TRAY_PITCH = 10             # fall over tray depth for drainage (mm), 1:200
# Yd-ONLY drainage slope (rev 2026-08-03): the rigid pan falls 1:200 in Yd only (far rim → near
# rim) and is LEVEL across X.  Level-across-X keeps the full-width spray beam (which rides the
# floor) level so it clears the level walkway support arms — a dual-axis (to-a-corner) fall tilted
# the beam's left end ~24mm into them.  Lateral drainage is not lost: a near-rim GUTTER collects the
# Yd fall and falls 1:200 INWARD to a single center pickup (self-draining, gravity toward the
# operator on the sweep — see the gutter block by PROC_TRAY_GUTTER_*).  The pan sits on tapered HDPE
# shim strips; the near rim is RAISED to Z=PROC_TRAY_SUMP_Z so the pickup well bottom rests on the
# container floor (Z0).  See PROC_TRAY_FLOOR_Z_LOW / tray_floor_z() below (single source).
PROC_TRAY_SHIM_H   = 10         # shim strip max height at far rim (mm) = PITCH
PROC_TRAY_SHIM_W   = 50         # shim strip width (mm) — HDPE flat bar
PROC_TRAY_SHIM_N   = 5          # number of shim strips across tray depth
# Low LINE: the near-rim gutter (full width) collects the Yd-only fall and drains inward to a
# single CENTER pickup well at X=PROC_TRAY_DRAIN_X.  The P-04 suction pops out of the walkway
# above the pickup, then runs UNDER the walkway to the IBC end to rejoin the ribbon lanes.
PROC_TRAY_DRAIN_X  = 2386       # near the center line (PH_X=2399), nudged -13 so the riser lands in a
#                                 clear walkway grate bay, clearing the X2526 cantilever bracket by 50mm
PROC_TRAY_DRAIN_YD = PROC_TRAY_YD_NEAR  # = 80mm — at the near rim (low edge of the Yd fall)

BV02_X             = PH_X         # BV-02 X on pinhole wall — at pinhole centerline, arm's reach from operator during wash pass
BV02_YD            = 0           # BV-02 on pinhole wall (Yd=0) — reserved (spec; not yet drawn)
BV02_Z             = 950         # BV-02 height on pinhole wall (mm AFF) — waist height from the raised walkway deck [+50 raise; was 900]
PROC_TRAY_SUMP_W   = 180        # center pickup well width in X (mm) — a local well at the gutter low point
#   (X=PROC_TRAY_DRAIN_X); hosts the brown P-04 suction strainer, well bottom on the container floor (Z0).
PROC_TRAY_SUMP_D   = 100        # sump well depth in Yd (mm)
PROC_TRAY_SUMP_Z   = 20         # sump well depth below tray floor (mm)

# ── Muslin cut to fit the WASHABLE tray area (it is washed flat in the tray) ─────────
# The muslin is cut NARROWER and SHORTER than the film-plane ACM+frame (see the film-plane §muslin
# note) so it lies flat in the tray clear of the rims AND the near-rim sump well.  Width follows the
# tray minus a wash clearance each side; height spans from just past the sump well (near) to the far
# rim.  Muslin < washable tray area < tray < film plane (ACM+frame).
MUSLIN_TRAY_CLEAR = 50                                                       # wash clearance, each edge (mm)
MUSLIN_CUT_W   = PROC_TRAY_W - 2 * MUSLIN_TRAY_CLEAR                         # = 4359mm
MUSLIN_YD_NEAR = PROC_TRAY_DRAIN_YD + PROC_TRAY_SUMP_D + MUSLIN_TRAY_CLEAR   # = 230mm — clears the sump well (Yd80..180)
MUSLIN_YD_FAR  = PROC_TRAY_YD_FAR - MUSLIN_TRAY_CLEAR                        # = 2230mm
MUSLIN_CUT_H   = MUSLIN_YD_FAR - MUSLIN_YD_NEAR                             # = 2000mm (washable depth, clear of the sump)
MUSLIN_AREA_SQFT = round(MUSLIN_CUT_W * MUSLIN_CUT_H / 1e6 * 10.7639)       # = 94 sq ft (captured print; < the 101 sqft film plane)

# ── Tray floor surface — SINGLE SOURCE for the raised, dual-axis-sloped basin ────────
# The basin floor is NOT flat at Z0.  Its low corner is RAISED to Z=PROC_TRAY_SUMP_Z so the
# sump well bottom rests on the container floor, and from there it rises 1:200 in BOTH X and
# Yd toward the far-left corner.  Every clearance (walkway deck, spray-bar carriage, corridor
# frame foot, hinged panel) must be measured against tray_floor_z(x, yd) — NOT a flat Z0.
PROC_TRAY_FLOOR_Z_LOW = PROC_TRAY_SUMP_Z          # = 20mm — floor top at the low (sump) corner
PROC_TRAY_SLOPE       = 1.0 / 200                  # fall per mm of plan run, EACH axis (1:200)

def tray_floor_z(x, yd):
    """Top-of-floor Z (mm) at plan position (x, yd) for the Yd-only 1:200 drainage slope.
    The surface is LEVEL across X and falls from the far rim (high) to the NEAR rim (low,
    Z=PROC_TRAY_FLOOR_Z_LOW).  Level-across-X keeps the rigid spray beam (which rides the
    floor) level so it clears the level walkway arms.  Lateral drainage is handled OFF the
    surface by the near-rim gutter, which falls 1:200 inward to a single center pickup — see
    the gutter block below and tray_gutter_floor_z().  The pan is rigid, so the rim top tilts
    with it: use tray_rim_top_z(x, yd)."""
    dyd = yd - PROC_TRAY_YD_NEAR          # 0 at the near/low rim, +D toward the far rim
    return PROC_TRAY_FLOOR_Z_LOW + dyd * PROC_TRAY_SLOPE

def tray_rim_top_z(x, yd):
    """Top-of-rim Z (mm) — the rigid pan's 50mm wall rides on the sloped floor."""
    return tray_floor_z(x, yd) + PROC_TRAY_RIM

# Convenience extremes (for labels / quick clearance checks):
PROC_TRAY_FLOOR_Z_HIGH = PROC_TRAY_FLOOR_Z_LOW + PROC_TRAY_D * PROC_TRAY_SLOPE  # far rim ≈ 31mm (Yd-only fall)

# ── Near-rim collection gutter — self-draining to a SINGLE center pickup ──────────
# The Yd-only surface sheets to the near rim; a gutter recessed into the near rim collects it
# and falls 1:200 INWARD (from both ends) to one center pickup at X=PROC_TRAY_DRAIN_X.  Fits the
# same 20mm sump budget (floor Z=PROC_TRAY_FLOOR_Z_LOW → container floor Z0).  Gravity runs
# toward the operator on the spray sweep.  See generate_tray_slope_diagram.py.
PROC_TRAY_GUTTER_W        = 100     # gutter width in Yd (mm) — recessed band along the near rim
PROC_TRAY_GUTTER_SLOPE    = 1.0 / 200                                       # inward fall (each side → center)
PROC_TRAY_GUTTER_Z_CENTER = 2       # gutter floor Z at the center pickup (mm) — well drops to Z0 below
_GUTTER_HALF_W            = (PROC_TRAY_X_R - PROC_TRAY_X_L) / 2             # 2229.5mm end→center run
PROC_TRAY_GUTTER_Z_END    = PROC_TRAY_GUTTER_Z_CENTER + _GUTTER_HALF_W * PROC_TRAY_GUTTER_SLOPE  # ≈ 13.1mm (≈7mm deep)

def tray_gutter_floor_z(x):
    """Gutter floor Z (mm) along the near rim — falls 1:200 inward from each end to the center pickup."""
    cx = PROC_TRAY_DRAIN_X
    return PROC_TRAY_GUTTER_Z_CENTER + abs(x - cx) * PROC_TRAY_GUTTER_SLOPE

# ── Water throughput — prints per resupply (COMPUTED, never transcribed) ──────
# "~13 prints per resupply" (and the ~32 gal/print, ~121 L/print, ~4.4 days figures derived from it)
# is restated across the docs and was independently re-declared in calculate_energy_budget.py. Rather
# than copy any of those literals, derive them here from named inputs so they can't drift. The chain
# mirrors water-system-report.md §"Per-print water requirement" / §"Storage capacity vs. print count"
# EXACTLY, including the report's documented per-wash rounding (15.6 gal ≈ 16 gal), so every
# downstream published number stays stable:
#   tray flood at TRAY_FLOOD_DEPTH_MM over the real footprint -> ~15.6 gal, ROUNDED to 16 gal/wash
#   wash 1 + wash 3 draw clean Blue (wash 2 recycles Brown) -> BLUE_WASHES_PER_PRINT × 16 = 32 gal
#   usable Blue supply / Blue-per-print -> prints between resupply runs (floor)
# facts.yml references PRINTS_PER_RESUPPLY via `constant:`; energy-budget imports these (one source).
L_PER_GAL             = 3.78541
BLUE_SUPPLY_L         = 1800    # usable clean-water (Blue) volume — 2× 900L gravity fill (~476 gal)
TRAY_FLOOD_DEPTH_MM   = 6       # one process flood depth (¼") over the tray footprint
BLUE_WASHES_PER_PRINT = 2       # washes 1 & 3 draw Blue; wash 2 recycles from Brown
TRAY_FLOOD_GAL        = round(PROC_TRAY_W * PROC_TRAY_D * TRAY_FLOOD_DEPTH_MM / 1e6 / L_PER_GAL)  # 15.6 → 16
BLUE_PER_PRINT_GAL    = BLUE_WASHES_PER_PRINT * TRAY_FLOOD_GAL   # = 32 gal net Blue/print
BLUE_PER_PRINT_L      = BLUE_PER_PRINT_GAL * L_PER_GAL           # ≈ 121 L
PRINTS_PER_RESUPPLY   = int(BLUE_SUPPLY_L / BLUE_PER_PRINT_L)    # = 14
BLUE_SUPPLY_GAL       = round(BLUE_SUPPLY_L / L_PER_GAL)         # = 476 gal (Blue supply in gallons)

# Water balance — of the Blue consumed per run, ~31 L/print is open-process loss (muslin carryout +
# evaporation + unrecovered residual; water-system-report §4); the rest is recovered into Brown+Waste.
# All COMPUTED so a supply/print change (e.g. the 1,600→1,800 L revision) re-derives them everywhere.
LOSS_PER_PRINT_L      = 31                                             # design est. — see water-system §4
RECOVERED_PER_PRINT_L = round(BLUE_PER_PRINT_L) - LOSS_PER_PRINT_L     # ≈ 90 L recovered/print
RECOVERED_L           = PRINTS_PER_RESUPPLY * RECOVERED_PER_PRINT_L    # = 1260 L (Brown+Waste at exhaustion)
COLLECTION_FILL_L     = RECOVERED_L // 2                              # = 630 L per collection tote
LOST_L                = PRINTS_PER_RESUPPLY * LOSS_PER_PRINT_L         # = 434 L lost over a run

# ── Perimeter walkway — removable grated sections around processing tray ─────
# 4 sections form a rectangular perimeter walk so the operator can access all
# working parts (valves, electrical panel, film plane, tilt-swing adjusters)
# without wading through the wet processing tray.
#
# Wall-cantilevered bracket design (rev 8, updated rev 9): triangular gusset
# brackets bolted to container wall structural ribs at 457mm (18") centers.
# Each bracket is an 8mm steel plate right-triangle gusset: 150mm vertical leg
# bolted to wall rib, 300mm horizontal arm projecting inward, diagonal brace
# welded between.  Grating sits directly on bracket arms.  NO legs, NO beam,
# NO floor contact.  Entire tray interior is completely clear for film loading.
# Deck height 140mm (115mm bracket arm + 25mm grate) clears the 50mm tray rim.
# Material: molded GRP (fiberglass) grating, 15mm, vinyl-ester + grit top (all 4
# sections) — corrosion-proof in the chemistry zone; 15mm depth keeps the deck.
#
# Mounting varies by wall type:
#   Near/far walkways (long walls): brackets bolt to corrugated wall ribs.
#   Right walkway (IBC end):        floor-mounted posts bolted through container
#       floor at X≈4640mm (just outside tray rim).  Cantilever arms reach back
#       over tray rim to support walkway.  34mm clearance to IBC stack.
#       Zero tray contact — posts on bare floor outside tray.
#   Left walkway (cargo door end):  REMOVABLE LIFT-OUT — no wall brackets.
#       Panel (hinged door) occupies the end wall at X=0 and SWINGS ~56° about
#       the pivot for transport.  Left walkway must be removed before the swing.
#       Left corners use butt joints (no miter) so near/far walkways start at
#       X=470 — clear of the door-end panel swing sweep.
#       Only the left walkway (X=170–470) needs removal for transport.
#       Supported at ends by near/far walkway bracket arms at butt joints.
#       Processing tray side (X=470): removable bearer beam (50×50×3mm Al RHS)
#       runs along Yd, bolted to near/far bracket vertical legs, spanning
#       1762mm.  Beam top flush at Z=75mm (grate bottom).
#       Cargo door side (X=170): 3 floor-standing support legs at X≈140 on
#       bare container floor (outside tray), plus a bearing strip (25×25×3mm
#       Al angle) on the processing tray rim (Z=50→75mm).
#       Zero processing tray contact — all supports outside or above tray.
#       Right corners use standard 45° miters (no panel conflict).
WALKWAY_W       = 300    # walkway width (mm) — bracket arm cantilever distance
WALKWAY_H       = 140    # deck height above floor (mm) = grate-underside Z115 + 25mm grate.
#       The 25mm MS-S-100 grate sits on the SAME Z115 arm (grate bottom Z115, deck top Z140).
#       The floor-leg cantilever arm (Z=75–115, 40mm deep) clears the 50mm tray rim AND the Z=54
#       spray-bar top by 21mm — UNCHANGED (only the grate got 10mm thicker on top). The tray, bath
#       and spray bar do NOT rise. Panel swing sweeps the bare Z115 brackets (walkway lifted out for
#       transport) → PANEL_FLOOR_GAP is NOT tied to this. Costs ~60mm film-plane bottom (was 130/15mm).
WALKWAY_GRATE_T = 25     # grating thickness (mm) — 1" McNichols MS-S-100 molded FRP (real product min; 15mm molded FRP doesn't exist, 2.60 lb/sf). Sits on the SAME Z115 arm → deck top 140.
WALKWAY_H_PREV  = 100    # original deck height (pre-lowering) — reserved (history; kept for reference)
WALKWAY_NEAR_LIFTOUT_X_R = 950  # the NEAR deck's door-end band (X≈470–950, Yd0–300) is a
                         # REMOVABLE lift-out for transport — the swing sweeps this band to X≈896
                         # (over Yd0–300), so the lift-out runs to 950 for a ~50mm margin; it lifts
                         # out (with the left walkway)
                         # rather than dropping the grate (the walkway stays LEVEL at Z130). The FAR
                         # deck is NOT swept (swept points stay short of the X470 deck start).
# Container structural rib spacing (ISO standard 20ft container)
CONTAINER_RIB_SPACING = 457   # mm (18 inches) — vertical corrugation flanges
# Wall-mounted cantilever brackets
WALKWAY_BRACKET_H = 150  # bracket vertical leg height on wall (mm)
WALKWAY_BRACKET_T = 8    # bracket plate thickness (mm)
WALKWAY_BRACKET_SPACING = CONTAINER_RIB_SPACING  # bracket spacing along walkway (mm)
# rev10: the panel + drum SWING ~56° about the pivot for transport and the swinging cage
# rides the Z130 floor gap — its underside passes OVER the Z115 door-end bracket tops, so
# NO walkway bracket is struck for transport (the old WALKWAY_BRACKET_DEMOUNT_X is retired).
# Right walkway (IBC end) — CANTILEVER RECTANGLE (rev 12).
# A closed 40×40×3mm SHS frame (2 long beams at X=4329/4629 + 2 end beams) picked
# up at mid-span by 2 arms cantilevering off the IBC corridor uprights (half-lapped
# where the long beams cross), on wall cleats at the left corners and combined
# corner plates (shared with the bottom film rail BR) at the right corners.  The
# geometry is single-sourced in src/models/generate_sketchup_model.py
# (right_walkway_cantilever() / fp_combined_corner_plate(), RWK_* constants) and the
# 2D plan in generate_walkway_diagram.py sheet3().  No floor contact, no roof
# penetrations.  The prior ceiling-hung bearer/hanger/ceiling-plate constants
# (WALKWAY_RIGHT_BEARER_*, _HANGER_*, _CEIL_*) are RETIRED.
WALKWAY_RIGHT_W = WALKWAY_W  # 300mm — same width as near/far
# Near walkway (pinhole side): X=tray_L to tray_R, Yd=0 to WALKWAY_W
WALKWAY_NEAR_YD = 0                          # near edge against pinhole wall
# Far walkway (film plane side): X=tray_L to tray_R, Yd=C_WID-WALKWAY_W to C_WID
WALKWAY_FAR_YD  = C_WID - WALKWAY_W         # = 2062mm
# Left walkway (cargo door end): X=tray_L to tray_L+WALKWAY_W, Yd=0 to C_WID
# REMOVABLE — must be lifted out before the panel swings to its transport position.
# Supported by FLOOR-LEG CANTILEVER brackets on the cargo-door side (rev 2026-06-07,
# replaces the edge-beam-on-wall-seats): see the LEFT_WK_CANT_* block below + Sheet 5/6.
# Zero processing tray contact — all supports outside or above the tray/bath.
WALKWAY_LEFT_X  = PROC_TRAY_X_L             # = 170mm (starts at tray left edge)
WALKWAY_LEFT_SPAN = C_WID - 2 * WALKWAY_W   # = 1762mm — floor-leg span (outer edge)
# Left walkway DRUM-EXIT punch-out (rev 8): the operator steps out of the
# revolving drum at X=450, but the 300mm walkway ends at X=470 — only 20mm of
# landing. Deepen the walkway to 600mm over the drum-opening Yd span + stepping
# margin. Verified clear of the optical cone (door-end; cone left edge is X≈914+
# at this depth, punch-out reaches only X=770). Needs an extra bearer + support
# leg under the deeper section (it cantilevers ~300mm further over the tray).
WALKWAY_LEFT_WIDE_W    = 600    # deepened walkway width here (mm) vs 300 normal
WALKWAY_LEFT_WIDE_YD_L = 800    # punch-out Yd start (near the drum opening)
WALKWAY_LEFT_WIDE_YD_R = 1560   # punch-out Yd end

# ── Left walkway support — FLOOR-LEG CANTILEVERS (rev 2026-06-07: supersedes the edge beam) ──
# A row of brackets bolted to the bare floor OUTSIDE the tray (X<170): each = foot plate +
# vertical post (to the grate bottom) + a cantilever arm reaching IN under the grate, ABOVE the
# floor-level spray bar (possible only after the +50 walkway raise lifted the grate). Standard
# brackets carry the grate inner edge (X=470); brackets on the drum-exit punch-out (Yd 800-1560)
# get EXTENDED arms to X=770 so the widened section is supported, not cantilevered. Zero tray
# contact; grate + brackets lift out for transport. Validated in the cantilever-study exploration (retired 2026-06-07).
LEFT_WK_CANT_LEG_X    = WALKWAY_LEFT_X - 30           # = 140 — leg centreline (bare floor, outside tray X=170)
LEFT_WK_CANT_LEG_YDS  = (250, 800, 1180, 1560, 2110)  # 5 brackets; 3 land on the punch-out (800/1180/1560)
LEFT_WK_CANT_POST     = 50    # post section (mm) — 50×50×3 steel SHS
LEFT_WK_CANT_POST_T   = 3     # post wall thickness (mm)
LEFT_WK_CANT_POST_W   = 60    # bracket width in Yd (mm)
LEFT_WK_CANT_FOOT     = (128, 60, 8)  # foot plate L(X)×W(Yd)×T (mm) — spans X≈38..166 (outboard of tray rim)
LEFT_WK_CANT_FOOT_X0  = 38    # foot plate left edge X (mm) — all < 170 (bare floor)
LEFT_WK_CANT_FOOT_BOLT_N = 4  # M10 floor anchors per foot (sealed penetrations)
LEFT_WK_CANT_ARM_Z0   = 93    # arm underside Z (mm) — ≥15mm above the full-width 1½ spray-bar top (Z78 at the far-left); top = grate bottom (115) => 22mm deep (2×⅞in). Also single-sources the RIGHT frame arm (RWK_ARM_BOT).
LEFT_WK_CANT_ARM_W    = 50.8  # standard arm width in Yd (mm) — 2in of the 2×⅞in section (⅞in is the Z-depth)
LEFT_WK_CANT_ARM_W_WIDE = 50.8  # widened (punch-out) arm — same 2×⅞in section
LEFT_WK_CANT_STD_REACH  = WALKWAY_LEFT_X + WALKWAY_W            # = 470 — standard arm tip (grate inner edge)
LEFT_WK_CANT_WIDE_REACH = WALKWAY_LEFT_X + WALKWAY_LEFT_WIDE_W  # = 770 — widened arm tip (punch-out inner edge)
# Right walkway (IBC end): ceiling-hung, same 300mm width as near/far
WALKWAY_RIGHT_X = PROC_TRAY_X_R - WALKWAY_RIGHT_W  # = 4329mm (grating inner edge)
# Near walkway widened section — 500mm-wide access band for the chem shelf + EP column + spray-bar
# operating room. CANTILEVER-LIMITED: the grate may overhang the outer widened brackets by at most
# WALKWAY_MAX_OVERHANG. rev 2026-07-23b: extended a SECOND rib toward the IBC (cantilever X2983+100 =
# 3083) so the operator has a full bay of standing room past the spray bar / pinhole (X2399) on the IBC
# side. It now runs X1055–3083 (cantilever X1155−100 to X2983+100). This reclassifies the X2983 near
# bracket std→widened (wide 4→5, near-std 4→3). The EP column right edge (EP_X + EP_COL_W = 2169) sits
# INSIDE the band; the chem shelf (X1180-1780) sits inside with a 125mm margin on its left. The slit
# cuts only to the tray lip (Yd=80), not the full depth.
WALKWAY_NEAR_WIDE_W   = 500             # widened section width (mm)
WALKWAY_MAX_OVERHANG  = 100             # max grate cantilever past an end bracket (deflection to be checked)
_NX0 = WALKWAY_LEFT_X + WALKWAY_W                       # near walkway start = 470
_CANT0 = _NX0 + CONTAINER_RIB_SPACING // 2             # first cantilever station ≈ 698
_SLIT_CX = (_NX0 + WALKWAY_RIGHT_X) // 2                # spray bar slit center X ≈ 2399
SPRAY_BEAM_X_L  = PROC_TRAY_X_L + 30                    # = 200mm — beam left end (30mm off the tray rim)
SPRAY_BEAM_X_R  = PROC_TRAY_X_R - 30                    # = 4599mm — beam right end
SPRAY_BEAM_SPAN = SPRAY_BEAM_X_R - SPRAY_BEAM_X_L       # = 4399mm — spray beam runs the FULL tray width; nozzles span it end-to-end (90° down-jets clear the overhead grate)
WALKWAY_NEAR_WIDE_X_L = _CANT0 + CONTAINER_RIB_SPACING - WALKWAY_MAX_OVERHANG      # 1055 = cantilever 1155 − 100
WALKWAY_NEAR_WIDE_X_R = _CANT0 + 5 * CONTAINER_RIB_SPACING + WALKWAY_MAX_OVERHANG  # 3083 = cantilever 2983 + 100 (rev 2026-07-23b: +2nd rib toward the IBC)
WALKWAY_WIDE_BRACKET_T = 10             # widened bracket plate thickness (mm) — heavier than std 8mm
WALKWAY_WIDE_BRACKET_H = 200            # widened bracket vertical leg height (mm) — taller for 4-bolt pattern
# ── Muslin-drop notches (rev 2026-07-23) ──
# A grate notch bitten out of the INBOARD (open-tray-facing) edge of the LEFT and RIGHT walkways,
# at the far end (near the image plane), so the exposed muslin can be slid off the image plane
# (far wall) and dropped into the open wash tray. GRATE-ONLY — brackets, beams, and the shared
# film-rail corner plate are untouched.
WALKWAY_MUSLIN_NOTCH_DX = 100   # depth into the walkway from the tray-facing (inboard) edge (X, mm)
WALKWAY_MUSLIN_NOTCH_DY = 150   # width along the tray-facing edge (Yd, mm)
WALKWAY_MUSLIN_NOTCH_YD0 = WALKWAY_FAR_YD - WALKWAY_MUSLIN_NOTCH_DY                 # 1912 — notch Yd start (far end of the open zone, just inboard of the far walkway)
WALKWAY_MUSLIN_NOTCH_L_X1 = WALKWAY_LEFT_X + WALKWAY_W                              # 470 — left walkway INBOARD (tray) edge
WALKWAY_MUSLIN_NOTCH_L_X0 = WALKWAY_MUSLIN_NOTCH_L_X1 - WALKWAY_MUSLIN_NOTCH_DX     # 370 — left notch cut in from X470
WALKWAY_MUSLIN_NOTCH_R_X0 = WALKWAY_RIGHT_X                                        # 4329 — right walkway INBOARD (tray) edge
WALKWAY_MUSLIN_NOTCH_R_X1 = WALKWAY_MUSLIN_NOTCH_R_X0 + WALKWAY_MUSLIN_NOTCH_DX     # 4429 — right notch cut in from X4329
# Open processing area (center, clear of walkways):
PROC_OPEN_X_L  = WALKWAY_LEFT_X + WALKWAY_W   # = 470mm
PROC_OPEN_X_R  = WALKWAY_RIGHT_X              # = 4329mm
PROC_OPEN_YD_N = WALKWAY_W                    # = 300mm
PROC_OPEN_YD_F = WALKWAY_FAR_YD               # = 2062mm
PROC_OPEN_AREA = (PROC_OPEN_X_R - PROC_OPEN_X_L) * (PROC_OPEN_YD_F - PROC_OPEN_YD_N) / 1e6
                                               # = 6.80 m² open processing area

# ── Spray bar — gantry design: full-width 1½in-square beam (rev 11) ─────────
# The beam runs the FULL tray width (SPRAY_BEAM_X_L..X_R, 4,399mm) so its 90°
# down-jet nozzles cover the print edge-to-edge; wheel carriages roll on the tray
# floor beneath the walkway grating.  Section is 1½×1½×0.062in 304-SS SQUARE tube
# — the depth needed so the full-width span sags only ~11mm (L/395, flattened by
# ~12mm pre-camber), where the old 40×25 sagged 25mm.  The poly manifold is
# side-mounted on the beam's inboard face with the barbed 90° down-jets tapping it.
# Ø32 nylon wheels keep the carriage low.  Beam-top-vs-walkway-arm clearance is
# resolved by the Yd-only tray slope (see spray-tray-redesign-plan.md / Commit B).
SPRAY_BAR_SPAN       = SPRAY_BEAM_SPAN  # nozzle span = full beam width (4,399mm); 90° down-jets fire down onto the print, so the overhead grate is no obstruction
SPRAY_BAR_BEAM_W     = 38.1        # beam footprint in Yd (mm) — 1½×1½×0.062in 304-SS SQUARE tube
SPRAY_BAR_BEAM_H     = 38.1        # beam HEIGHT in Z (mm) — 1½in square; deep enough that the full-width 4,399mm span sags only ~11mm (L/395), flattened by ~12mm pre-camber
SPRAY_BAR_BEAM       = SPRAY_BAR_BEAM_W   # legacy alias → the square section (38.1)
SPRAY_BAR_BEAM_T     = 1.575       # wall thickness (mm) — 0.062in; single 17ft4in Metals Depot stick (no butt weld); wall barely affects sag (self-weight-dominated)
SPRAY_BAR_BORE       = SPRAY_BAR_BEAM_W - 2 * SPRAY_BAR_BEAM_T  # = 34mm internal bore (poly no longer housed here)
SPRAY_BAR_POLY_OD    = 25          # 3/4" LDPE irrigation poly pipe OD (mm) — SIDE-mounted on the beam's inboard face
SPRAY_BAR_POLY_ID    = 19          # poly pipe ID (mm)
SPRAY_BAR_WHEEL_DIA  = 32          # nylon wheel diameter (mm) — shrunk from 50 for grate clearance on the raised tray
SPRAY_BAR_WHEEL_W    = 20          # wheel width (mm)
SPRAY_BAR_WHEELS_PER_SIDE = 2      # wheels per carriage (spaced in Yd direction) — reserved (spec; 2D/3D draw wheels via WHEEL_SP)
SPRAY_BAR_WHEEL_SP   = 200         # wheel center-to-center spacing in Yd (mm)
SPRAY_BAR_TRAY_FLOOR = 2           # tray sheet metal thickness on container floor (mm)
# Carriage vertical stack is now FLOOR-RELATIVE: the wheels ride the LOCAL (sloped) floor,
# so absolute Z = tray_floor_z(x, yd) + rise.  Use spray_beam_bot_z / spray_beam_top_z.
SPRAY_BAR_AXLE_RISE    = SPRAY_BAR_WHEEL_DIA // 2                        # = 16mm — axle CL above the local floor
SPRAY_BAR_BRACKET_DROP = 7                                              # axle CL to beam bottom (mm)
SPRAY_BAR_BEAM_BOT_RISE = SPRAY_BAR_AXLE_RISE - SPRAY_BAR_BRACKET_DROP  # = 9mm — beam bottom above the local floor
SPRAY_BAR_BEAM_TOP_RISE = SPRAY_BAR_BEAM_BOT_RISE + SPRAY_BAR_BEAM_H    # = 34mm — beam top above the local floor

def spray_beam_bot_z(x, yd): return tray_floor_z(x, yd) + SPRAY_BAR_BEAM_BOT_RISE
def spray_beam_top_z(x, yd): return tray_floor_z(x, yd) + SPRAY_BAR_BEAM_TOP_RISE

# Legacy ABSOLUTE Z references, evaluated at the LOW (sump) corner (floor = PROC_TRAY_FLOOR_Z_LOW).
# The beam actually rides the local floor — these are the low-corner values for context/labels.
SPRAY_BAR_AXLE_Z     = PROC_TRAY_FLOOR_Z_LOW + SPRAY_BAR_AXLE_RISE      # = 36mm (was 27)
SPRAY_BAR_Z_BOT      = PROC_TRAY_FLOOR_Z_LOW + SPRAY_BAR_BEAM_BOT_RISE  # = 29mm beam bottom @ low corner (was 20)
SPRAY_BAR_Z_TOP      = PROC_TRAY_FLOOR_Z_LOW + SPRAY_BAR_BEAM_TOP_RISE  # = 54mm beam top @ low corner (was 60)
SPRAY_BAR_TRAVEL     = PROC_TRAY_D  # = 2200mm (Yd travel, near rim to far rim)
SPRAY_BAR_HOLE_DIA   = 8           # nozzle barb bore (mm) — side-tap into the poly manifold (was a beam-wall through-hole)
SPRAY_BAR_NOZZLE_PITCH = 100       # nozzle center-to-center pitch along the beam (mm) — 90° down-jets: a 90° cone at the ~50mm nozzle height gives a ~100mm footprint, so 100mm pitch = edge-to-edge along-beam coverage (was 150 for 180° flat-fans)
SPRAY_BAR_N_NOZZLES  = int(SPRAY_BEAM_SPAN // SPRAY_BAR_NOZZLE_PITCH) + 1  # = 44 @ 100mm (full beam width)
SPRAY_BAR_HOLE_SP    = SPRAY_BAR_NOZZLE_PITCH  # legacy hole-pitch ref (mm)
SPRAY_BAR_HOSE_L     = 4000        # flexible hose length BV-02 to bar (mm) — reserved (spec; shopping-list ref)
SPRAY_BAR_FEED_Z     = SPRAY_BAR_Z_BOT + SPRAY_BAR_BEAM_H // 2  # = 41mm — feed end cap center @ low corner
SPRAY_BAR_SLIT_W     = 30          # walkway slit width for pole passage (mm)

# ── External fill/drain ports — far end wall bulkhead fittings (rev 5) ───────
# 2" NPT bulkhead unions through container far end wall (X=C_LEN face).
# Flat steel reinforcing plate welded over corrugation before drilling.
# External bulkhead ports — 3 ports (X1/X3/X4) stacked vertically on end wall centerline
# X1 fill tees internally to BOTH Blue totes (parallel fill, no X2 port, no cross-connect)
EXT_PANEL_YD = C_WID // 2   # = 1181mm — panel centered on container width
EXT_FILL_1_H = 2250    # X1: Blue fill port height (mm) — feeds the Blue side-entry T near the top of both top-tier totes (~Z2150), gravity feed; gravity-linked across the corridor
EXT_DRAIN_3_H = 400    # X3: drain Brown IBC-3 port height (mm) — bottom tier near
EXT_DRAIN_4_H = 200    # X4: drain Waste IBC-4 port height (mm) — bottom tier far
# Legacy aliases for downstream code
EXT_FILL_H   = EXT_FILL_1_H
EXT_FILL_YD  = EXT_PANEL_YD
EXT_DRAIN_H  = EXT_DRAIN_4_H
EXT_DRAIN_YD = EXT_PANEL_YD

# ── Ventilation fans (150mm compact axial panel fans, interior-mounted) ───────
# Both fans are identical — one part number, same baffle duct assembly.
# Fan A: exhaust, sealed end wall (X = C_LEN face), in the 270mm plumbing corridor
#         directly BELOW the X1 fill port (Yd=1181, Z=2000) — the only full-height
#         clear channel past the v2 1000L direct-stack (totes reach Z=2336 in both
#         flanking columns). Baffle duct extends 300mm into the corridor from X=C_LEN.
# Fan B: intake, mounted on the swinging panel (near corner zone, Yd=365 — outboard of
#         the PANEL_CUT_YD swing cut, so it rides the swinging part), LOW position.
#         Baffle duct protrudes 300mm from the panel EXTERIOR face. Self-contained wall fan
#         (louvre+baffle+fan in the panel) — nothing to disconnect when the panel swings.
#         Operational mode (panel shut at the door): duct draws outside air through the open
#         cargo doorway. Transport mode: swings ~56° inboard with the panel (X≈1838, fan off).
#         Wiring via a flexible cable loop from the fixed door frame.
FAN_DIAM    = 150    # fan / duct diameter (mm)
FAN_BODY_D  =  50    # panel fan body depth (mm)
FAN_A_H     = 2000   # fan A center height AFF (mm) — below the X1 fill port (Z2250) on the sealed end wall, in the clear plumbing corridor (was 2200, which the taller 1000L stack would have buried)
FAN_B_H     = 600    # fan B center height AFF (mm — LOW; intake near floor)
# Yd (width) positions — cross-ventilation diagonal: low intake (cargo-door
# panel) to high exhaust (far end wall), diagonally across the volume.
# rev 9 / B2: Fan A and Fan B SWAP sides (mirror about the centerline) so the
# intake fan (Fan B, on the swinging panel) sits in the NEAR corner by the pinhole
# wall — its conduit then runs along that wall; only a flex whip (with swing slack)
# bridges to the swinging panel so it follows the ~56° transport rotation.
FAN_A_YD    = EXT_FILL_YD  # = 1181mm — directly BELOW the X1 fill port, in the 270mm plumbing corridor (clear full-height of the 1000L stack; relocated from Yd1996, which the taller 1000L totes buried — see ibc-reconfig-v2)
FAN_B_YD    = (C_WID // 2 - DRUM_R) // 2          # = 365mm — near the pinhole wall, in the near corner zone clear of the drum (near edge Yd≈731)

# Baffle duct (one per fan, welded galvanized steel)
# Fan A: duct extends into container interior from wall
# Fan B: duct protrudes from panel exterior face (into open doorway / container)
DUCT_DEPTH  = 300    # baffle duct depth (mm)
DUCT_HEIGHT = 200    # baffle duct opening height (mm)

# Shadow margins — distance from fan assembly to nearest cone edge (at worst depth)
# Fan A: duct extends inward from X=C_LEN wall
FAN_A_MARGIN = C_LEN - ZONE_R_START - FAN_DIAM // 2 - DUCT_DEPTH   # = 869mm ✓
# Fan B: mounted on panel — intake grille on panel inner face, no duct on interior side.
# Shadow margin is panel inner face to ZONE_L_END = 40mm (corner zone thickness).
# Fan at Yd=365mm (rev9/B2 swap, near pinhole wall): still at X=0, behind the
# X=150–4649 active image-plane zone, so no cone intrusion (and still in a 40mm
# corner zone — now the NEAR corner instead of the far one).
FAN_B_MARGIN = PANEL_CORNER_T   # = 40mm (fan flush with panel inner face)

# ── Output directories ────────────────────────────────────────────────────────
DIAGRAMS_DIR = os.environ.get("TBS_DIAGRAMS_DIR") or os.path.join(PROJECT_ROOT, "diagrams")  # env override: lint regenerates to a temp dir to byte-diff the cascade

# ── Raster resolution (savefig dpi) ───────────────────────────────────────────
# One knob for the whole diagram set so it can't drift across ~90 savefig calls.
DIAGRAM_DPI    = 300   # engineering diagrams — high DPI so text stays sharp when zoomed
DISTORTION_DPI = 150   # override for the dark full-bleed distortion renders (no fine text; keeps files smaller)

# ── Palette (shared drawing style) ───────────────────────────────────────────
C_OUT   = "#1A1A1A"   # outlines
C_CL    = "#2060A0"   # center lines
C_DIM   = "#404040"   # dimensions
C_ALUM  = "#C8D8E8"   # aluminum fill
C_STEEL = "#B0B0B8"   # steel fill
C_GASKT = "#5A3020"   # gasket/neoprene

# ── Unified component color palette ──────────────────────────────────────────
# Single source of truth for equipment colors across all diagrams.
C_LT_DRUM      = "#E8E0D0"   # light trap revolving drum
C_BLUE_IBC     = "#4A90D9"   # blue IBC tanks
C_BROWN_IBC    = "#9C7A3C"   # brown IBC tank
C_WASTE_IBC    = "#7A6B5A"   # waste IBC (rev 5: replaces C_WASTE_DRUM)
C_EVAP         = "#3DAA96"   # evaporative cooler
C_ELEC         = "#F5C518"   # electrical panel
C_BATT         = "#6A5ACD"   # battery bank
C_PUMP         = "#E8884A"   # pump manifold
C_WALL         = "#B0B0B8"   # container walls / structural steel
C_HINGE_PANEL  = "#C8C8C0"   # hinge panel body (generic / schematic block)
C_WOOD         = "#C9A36B"   # plywood — fan-mount band + equipment panel (rev11 material legend)
C_PLASTIC      = "#6E8CA0"   # 1/8″ HDPE panel skins + B2 bay (rev11; differentiates plastic from wood)
C_FILM         = "#2060A0"   # film plane / muslin
C_PINHOLE_EQ   = "#CC6600"   # pinhole aperture
C_FAN          = "#A0A0A8"   # fans (A and B)
C_PROC_ZONE    = "#E8F5E9"   # processing tray zone

# ── Convenience summary (printed on import in debug mode) ────────────────────
if __name__ == "__main__":
    print("TBS-001 Constants (rev 7)")
    print(f"  Container:      {C_LEN} × {C_WID} × {C_HGT}mm")
    print(f"  Film plane:     {FP_W} × {FP_H}mm  (X={FP_X_L}–{FP_X_R})")
    print(f"  Muslin clamps:  {CLAMP_N_TOTAL} nylon spring clamps at {CLAMP_SPACING}mm centers (top + 2 sides; filler {CLAMP_FILLER_D:g}mm)")
    print(f"  Pinhole:        X={PH_X}  H={PH_H}  Ø{PH_D}mm  f/{PH_FNO}")
    print(f"  Rails:          X={RAIL_X_L} – {RAIL_X_R}  span={RAIL_SPAN}mm")
    print(f"  Max tilt:       {MAX_TILT_DEG:.1f}°")
    print(f"  Max swing:      {MAX_SWING_DEG:.1f}°")
    print(f"  Left zone:      X=0–{ZONE_L_END}mm (light trap drum only)")
    print(f"  Right zone:     X={ZONE_R_START}–{C_LEN}mm")
    print(f"  Cone at Y=FP_Y: X={cone_left(FP_Y):.0f} – {cone_right(FP_Y):.0f}")
    print(f"  Hinge panel:    corner={PANEL_CORNER_T}mm  center={PANEL_CENTER_T}mm  step={PANEL_STEP}mm")
    print(f"  Panel zones:    corners Yd=0–{PANEL_CORNER_YD_L} / {PANEL_CORNER_YD_R}–{C_WID}  center Yd={PANEL_CORNER_YD_L}–{PANEL_CORNER_YD_R}")
    print(f"  Panel swing:    {SWING_LOCK_DEG}° about pivot (X={PIVOT_X}, Yd={PIVOT_YD})  cut Yd={PANEL_CUT_YD}  far strip Yd={FAR_STRIP_YD0}-{C_WID}")
    print(f"  Panel floor gap:{PANEL_FLOOR_GAP}mm (tray rim={PROC_TRAY_RIM}mm)  pivot post=Ø{PIVOT_POST_OD}×{PIVOT_POST_T}  drum cage Yd={DRUM_CAGE_YD_L}-{DRUM_CAGE_YD_R}")
    print(f"  IBC 2x2 stack:  X={IBC_COL_X}–{IBC_COL_X+IBC_W}  near Yd={BLUE_IBC_Y}  far Yd={IBC_FAR_Y}")
    print(f"  IBC corridor:   Yd={CORRIDOR_YD_NEAR}–{CORRIDOR_YD_FAR}  width={CORRIDOR_W}mm")
    print(f"  IBC stack H:    {IBC_H_STK}mm  (ceiling {C_HGT}mm → headroom {C_HGT - IBC_H_STK}mm)")
    print(f"  Eq panel:       face X={EQPANEL_X}  T={EQPANEL_T}mm  Z={EQPANEL_Z_LO}–{EQPANEL_Z_HI}  Yd={EQPANEL_YD}–{EQPANEL_YD_FAR} (spans corridor)")
    print(f"  Pumps on panel: X={PUMP_X}–{EQPANEL_X}  Z={PUMP_H_LO}–{PUMP_H_HI}  Yd={PUMP_YD}  depth={PUMP_D}mm  Yd_span={PUMP_YD_SPAN}mm")
    print(f"  Filters:        F1 Z={F1_Z}  F2 Z={F2_Z}  F3 Z={F3_Z}  Yd={FSKID_YD}  X protrusion={BB_OD}mm")
    print(f"  Filter housing: OD={BB_OD}mm  H={BB_H}mm (4.5\"×10\")")
    print(f"  Proc tray:      X={PROC_TRAY_X_L}–{PROC_TRAY_X_R}  Yd={PROC_TRAY_YD_NEAR}–{PROC_TRAY_YD_FAR}  rim={PROC_TRAY_RIM}mm")
    print(f"  Tray sump:      X={PROC_TRAY_DRAIN_X}  Yd={PROC_TRAY_DRAIN_YD}")
    print(f"  Walkway:        std={WALKWAY_W}mm  wide={WALKWAY_NEAR_WIDE_W}mm (X={WALKWAY_NEAR_WIDE_X_L}–{WALKWAY_NEAR_WIDE_X_R})")
    print(f"  Right walkway:  CANTILEVER RECTANGLE  (40×40 SHS frame + 2 IBC-upright arms + combined corner plates)")
    print(f"  Left walkway:   REMOVABLE LIFT-OUT  span={WALKWAY_LEFT_SPAN}mm  ({len(LEFT_WK_CANT_LEG_YDS)} floor-leg cantilevers)")
    print(f"  Walkway open:   X={PROC_OPEN_X_L}–{PROC_OPEN_X_R}  Yd={PROC_OPEN_YD_N}–{PROC_OPEN_YD_F}  area={PROC_OPEN_AREA:.2f} m²")
    print(f"  Evap cooler:    EXTERNAL — duct Ø{EVAP_DUCT_D}mm at X={EVAP_DUCT_X} Z={EVAP_DUCT_Z}")
    print(f"  EP:             X={EP_X}–{EP_X+EP_W}  Z={EP_H_LO}–{EP_H_HI} [rev7: raised]")
    print(f"  Battery:        X={BA_X}–{BA_X+BA_W}  Z={BA_H_LO}–{BA_H_HI}  depth={BA_D}mm [rev7: slim]")
    print(f"  Spray bar:      GANTRY  span={SPRAY_BAR_SPAN}mm  beam Z={SPRAY_BAR_Z_BOT}–{SPRAY_BAR_Z_TOP}  wheels Ø{SPRAY_BAR_WHEEL_DIA}  {SPRAY_BAR_N_NOZZLES} nozzles @ {SPRAY_BAR_NOZZLE_PITCH}mm")
    print(f"  Ext fill port:  H={EXT_FILL_H}mm  Yd={EXT_FILL_YD}mm")
    print(f"  Ext drain port: H={EXT_DRAIN_H}mm  Yd={EXT_DRAIN_YD}mm")
    print(f"  Fan A (exhaust):far end wall  H={FAN_A_H}mm AFF  Ø{FAN_DIAM}mm  margin={FAN_A_MARGIN}mm")
    print(f"  Fan B (intake): door panel    H={FAN_B_H}mm AFF  Ø{FAN_DIAM}mm  margin={FAN_B_MARGIN}mm")
    print(f"  Baffle duct:    {DUCT_DEPTH}mm deep × {DUCT_HEIGHT}mm H")
