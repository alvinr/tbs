# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
tbs_constants.py — Single source of truth for TBS-001 geometry and equipment.

All generator scripts should import from this module:
    from tbs_constants import *

Redesign basis (2026-04-23 rev 2):
  Black-water drums (2× 55-gal) relocated from right end zone to left end zone
  (Y-stacked behind evap cooler).  IBC column right-justified to X=4,674–5,893mm.
  Film plane widens from 2,920mm to 3,549mm (X=1,100–4,649mm).
  Pinhole recentred to X=2,874mm.  Max swing decreases from 36.5° to 31.4°
  (same Y travel over wider 3,549mm rail span).

Redesign basis (2026-04-23 rev 3):
  Evap cooler relocated to pinhole wall face (Yd=0) at X=930–1,530mm — always
  shadow-free at Yd=0 regardless of X position.
  Drums repositioned to X=20–600mm, Yd=25–605mm (near cargo door end wall,
  Yd range entirely below light trap drum's Yd=806–1,556mm band — no X-clearance
  conflict).  Zone left boundary moves from X=1,100mm to X=625mm.
  Film plane widens from 3,549mm to 4,024mm (X=625–4,649mm).
  Pinhole recentred to X=2,637mm.  Max swing decreases from 31.4° to 28.3°
  (wider rail span over same Y travel).

Redesign basis (2026-05-03 rev 4):
  Hinged panel redesigned as stepped profile: 40mm corners (18mm ply + 4mm
  steel plate + 18mm ply) flanking 120mm center zone (unchanged RHS frame
  construction housing the light trap drum).  Step transitions at Yd=756mm
  and Yd=1,606mm (drum 750mm + 50mm clearance each side).
  Panel slides on HGR20 linear rails (300mm travel) so light trap drum clears
  the container exterior face by 5mm, allowing standard ISO cargo doors to close.
  Fixed door frame with EPDM compression seal at X=0.

Redesign basis (2026-05-06 rev 5):
  Waste drums (2x 55-gal) eliminated.  Replaced by a 4th IBC (waste, 600L)
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
  Width increases from 4,024mm to 4,499mm (+11.8%).  Active area from 9.61 m²
  to 10.74 m² (103→116 sqft).  Max swing decreases from 28.3° to 25.7°
  (wider rail span, same Y travel).  Left end zone shrinks to X=0–150mm.
"""

import math

# ── Container interior ────────────────────────────────────────────────────────
C_LEN  = 5893   # interior length, long axis X (mm)
C_WID  = 2362   # interior width = focal length = optical depth Y (mm)
C_HGT  = 2388   # interior height Z (mm)

# ── Film plane ────────────────────────────────────────────────────────────────
FP_H     = 2388   # film plane height (mm)          [unchanged]
FP_X_L   = 150    # film plane left edge X (mm)     [rev6: was 625; panel inner face 120mm + 30mm]
FP_X_R   = 4649   # film plane right edge X (mm)    [was 4,019 → wider right zone]
FP_W     = FP_X_R - FP_X_L   # = 4,499 mm          [rev6: was 4,024]
FP_Y     = 2262   # nominal depth from pinhole wall (mm)  [unchanged]
FP_Y_MIN = 100    # minimum carriage depth (mm)     [unchanged]

# ── Muslin clamp system ──────────────────────────────────────────────────────
# Cam-lever spring clamps bolted to the perpendicular leg of the 2"x2"x3/16"
# aluminum angle frame at 150mm centers. Jaw presses muslin hem against the
# pinhole-facing leg. Torsion spring biases clamp closed at any tilt angle.
FP_ANGLE_LEG  = 50.8   # angle leg size (mm) — 2" = 50.8mm
FP_ANGLE_T    = 4.8    # angle thickness (mm) — 3/16" = 4.76mm ≈ 4.8mm
CLAMP_SPACING = 150    # clamp center-to-center spacing (mm)
CLAMP_BASE_W  = 40     # base plate width along frame edge (mm)
CLAMP_BASE_H  = 50     # base plate height on perpendicular leg (mm)
CLAMP_BASE_T  = 3      # base plate thickness (mm)
CLAMP_LEVER_L = 60     # cam lever length (mm)
CLAMP_JAW_W   = 35     # rubber jaw pad width (mm)
CLAMP_JAW_H   = 12     # rubber jaw pad height (mm)
CLAMP_JAW_T   = 6      # rubber jaw pad thickness (mm — 60A neoprene)
CLAMP_OPEN_GAP = 15    # jaw clearance from frame face when open (mm)
CLAMP_SPRING_F = 5     # nominal clamping force per clamp (N)
CLAMP_N_HORIZ = FP_W // CLAMP_SPACING + 1   # = 30 per horizontal edge
CLAMP_N_VERT  = FP_H // CLAMP_SPACING + 1   # = 16 per vertical edge
CLAMP_N_TOTAL = 2 * CLAMP_N_HORIZ + 2 * CLAMP_N_VERT  # = 92

# ── Pinhole (recentred on new film plane) ─────────────────────────────────────
PH_X   = FP_X_L + FP_W // 2   # = 2,399 mm  [rev6: was 2,637]
PH_H   = 1194                  # height (mm) [unchanged]
PH_D   = 2.17                  # diameter (mm) — Rayleigh, f=2362, λ=550nm [unchanged]
PH_F   = C_WID                 # focal length = container width [unchanged]
PH_FNO = round(PH_F / PH_D)   # f/1088 [unchanged]

# ── Film plane rails ──────────────────────────────────────────────────────────
RAIL_X_L  = FP_X_L   # left rail X  (mm)   [rev6: 150mm; was 625]
RAIL_X_R  = FP_X_R   # right rail X (mm)   [was 4,019 → now 4,649]
RAIL_SPAN = RAIL_X_R - RAIL_X_L   # = 4,499 mm  [rev6: was 4,024]
RAIL_LEN  = 2200      # rail length  (mm)   [unchanged — same Y travel]
RAIL_OFF  = 100       # floor/ceiling offset (mm)  [unchanged]

# ── Movement ranges ───────────────────────────────────────────────────────────
MAX_TILT_DEG  = math.degrees(math.atan((FP_Y - FP_Y_MIN) / FP_H))
# = arctan(2162/2388) = 42.1°  [unchanged]

MAX_SWING_DEG = math.degrees(math.atan((FP_Y - FP_Y_MIN) / RAIL_SPAN))
# = arctan(2162/4499) = 25.7°  [rev6: was 28.3° with 4,024mm span]

# ── Equipment zones ───────────────────────────────────────────────────────────
ZONE_L_END   = FP_X_L    # left zone right boundary X  (= 150 mm)  [rev6: was 625]
ZONE_R_START = FP_X_R    # right zone left boundary X  (= 4,649 mm) [was 4,019]

# ── Optical cone helper ───────────────────────────────────────────────────────
def cone_left(y):
    """X coordinate of cone left boundary at depth y from pinhole wall."""
    return PH_X - (PH_X - FP_X_L) * y / FP_Y

def cone_right(y):
    """X coordinate of cone right boundary at depth y from pinhole wall."""
    return PH_X + (FP_X_R - PH_X) * y / FP_Y

# ── Hinged panel — stepped profile (rev 4) ───────────────────────────────────
# Corner zones (Yd=0–756 and Yd=1,606–2,362): thin sandwich panel.
# Center zone (Yd=756–1,606): full RHS frame housing light trap drum.
PANEL_CORNER_T    = 40    # corner zone thickness (mm) — 18mm ply + 4mm plate + 18mm ply
PANEL_CENTER_T    = 120   # center zone thickness (mm) — 18mm ply + 84mm RHS + 18mm ply
PANEL_STEP        = PANEL_CENTER_T - PANEL_CORNER_T  # = 80mm step depth
PANEL_CORNER_YD_L = 756   # corner-to-center transition, near side (mm)
PANEL_CORNER_YD_R = 1606  # center-to-corner transition, far side (mm)
PANEL_CENTER_W    = PANEL_CORNER_YD_R - PANEL_CORNER_YD_L  # = 850mm center zone width
WALL_T            = 40    # container end-wall steel thickness (mm)

# ── Sliding rail system — transport mode (rev 4, updated rev 6) ──────────────
# Panel slides inward 300mm on HGR20 ceiling-mounted linear rails so the light
# trap drum clears the container exterior face, allowing ISO cargo doors to close.
# Panel is suspended from ceiling — bottom edge clears floor-mounted processing tray.
PANEL_SLIDE       = 300   # panel slide travel for transport (mm)
PANEL_FLOOR_GAP   = 80    # gap between panel bottom edge and floor (mm)
                          # Must exceed PROC_TRAY_RIM (50mm) for transport clearance

# ── Left end zone (X = 0–150 mm, shadow-free at all depths) ──────────────────
# Light trap drum in hinge panel center zone.  Zone shrunk in rev 6 as film
# plane extended left from X=625 to X=150mm.  Only the panel thickness
# (40/120mm) occupies this zone now.
DRUM_CX    = 0       # light trap drum center X (mm) [unchanged]
DRUM_D     = 750     # revolving drum diameter (mm)
DRUM_R     = DRUM_D // 2
DRUM_H_LT  = 2200    # light trap drum height (mm) — increased for 330mm headroom at 1780mm operator height

# Evap cooler — relocated to pinhole wall face (Yd=0), right of drums in X
# At Yd=0 the cone collapses to a point → shadow-free at any X position.
EVAP_X     = 930     # evap cooler left edge X (mm)  [rev3: 930; on pinhole wall face]
EVAP_W     = 600     # evap cooler width X (mm)       [unchanged]
EVAP_Y     = 0       # evap cooler near edge Yd (mm)  [rev3: was 100; now on pinhole wall]
EVAP_D     = 350     # evap cooler depth Y (mm)        [unchanged]
EVAP_H     = 800     # evap cooler height (mm)         [unchanged]

# ── External power panel (pinhole wall exterior, near EP) ─────────────────────
PWR_PANEL_X = 1250   # power panel left edge X (mm) — just left of EP
PWR_PANEL_W = 340    # face plate width (mm)
PWR_PANEL_H = 240    # face plate height (mm)
PWR_PANEL_D = 3      # face plate thickness (mm) — flush-mount, no protrusion
PWR_PANEL_CUTOUT_W = 280   # wall cutout width (mm) — 30mm overlap each side
PWR_PANEL_CUTOUT_H = 180   # wall cutout height (mm)

# ── Pinhole wall face (Y = 0, shadow-free) ────────────────────────────────────
EP_X       = 1600    # electrical panel left edge X (mm)  [rev6b: moved left, away from pinhole]
EP_W       = 300     # electrical panel width (mm)
EP_H_LO    = 900     # electrical panel bottom H (mm)
EP_H_HI    = 1500    # electrical panel top H (mm)

BA_X       = 1810    # battery bank left edge X (mm)  [rev6: was 2050; shifted left to clear cone]
BA_W       = 500     # battery bank width (mm)  → right edge 2310, clears cone left (2319)
BA_H_LO    = 100     # battery bank bottom H (mm) — matches RAIL_OFF floor offset
BA_H_HI    = 600     # battery bank top H (mm)

PUMP_X     = 2500    # pump manifold left edge X (mm) — right of cone right boundary (2479) + 21mm gap
PUMP_W     = 500     # pump manifold width (mm) — 127mm body incl. ports, 150mm gap
PUMP_H_LO  = 200     # pump manifold bottom H (mm)
PUMP_H_HI  = 600     # pump manifold top H (mm)

# ── Chemistry prep shelf (ceiling-suspended, right corner) ────────────────────
# Single ceiling-hung shelf for mixing cyanotype chemistry, coating muslin, and
# materials staging.  Suspended from 4x M10 threaded rod hangers in the
# processing area corner, just inside the right walkway and near walkway.
# Does not overlap any walkway — all walkways clear for passage.
# Rotated 90°: long axis along X (parallel to walkway), short axis into tray.
# Shadow-free: cone right boundary at Yd=450 is X=3,021mm; shelf at
# X=3,729+ is >700mm outside cone.
SHELF_X_L      = 3729    # shelf left edge X (mm) — 600mm left of right walkway
SHELF_X_R      = 4329    # shelf right edge X (mm) — flush with right walkway inner edge
SHELF_W        = 600     # shelf width in X direction (mm) — long axis along walkway
SHELF_YD_NEAR  = 300     # shelf near edge Yd (mm) — at near walkway outer edge
SHELF_YD_FAR   = 600     # shelf far edge Yd (mm)
SHELF_DEPTH    = 300     # shelf depth in Yd direction (mm) — short axis into tray
SHELF_H        = 1025    # work surface height AFF (mm) — 925mm above walkway deck
SHELF_T        = 22      # shelf total thickness (mm) — 18mm ply + 4mm frame
SHELF_HANGER_D = 10      # hanger threaded rod diameter (mm) — M10 (matches right walkway)
SHELF_HANGER_N = 4       # number of hanger rods (4 corners)

# ── Chemistry prep tap (pinhole wall, tees off blue supply line) ─────────────
TAP_X          = 3729    # tap X position (mm) — at shelf left edge
TAP_Z          = 1150    # tap spout height AFF (mm) — 125mm above shelf surface
TAP_PIPE_OD    = 25      # branch pipe OD (mm) — 3/4" HDPE
TAP_WALL_T     = 3       # branch pipe wall thickness (mm)


# ── Filter skid (pinhole wall, right of pump manifold) ─────────────────────
# 900×600mm slotted steel angle frame, wall-mounted on pinhole wall (Yd=0).
# Three Geekpure Big Blue 4.5"×10" housings, vertical mount, heads at top.
# Flow: IBC-3 → P-02 → F1 → F2 → F3 → pH test → DV-01.
FSKID_X        = 2850    # frame left edge X (mm) — 50mm right of pump manifold
FSKID_W        = 900     # frame width (mm)
FSKID_Z_LO     = 1410    # frame bottom Z above floor (mm) — raised for walkway clearance
FSKID_Z_HI     = 2010    # frame top Z above floor (mm)
FSKID_H        = 600     # frame height (mm)

# Big Blue 4.5"×10" housings (physical dimensions)
BB_OD          = 130     # housing outer diameter incl bracket (mm) — 4.5"=114mm + clamp
BB_H           = 340     # housing total height (mm) — head + sump bowl
BB_HEAD_H      = 70      # head height (mm) — where 1" NPT ports are
BB_PORT_SEP    = 90      # center-to-center distance between IN/OUT ports (mm)

# Filter center X positions (equally spaced within 850mm inner frame)
# 3 housings × 130mm OD = 390mm; remaining 460mm ÷ 4 gaps = 115mm each
F1_X           = 3055    # F1 center X (mm) — 50μ sediment
F2_X           = 3300    # F2 center X (mm) — 5μ sediment
F3_X           = 3545    # F3 center X (mm) — GAC carbon
FILT_HEAD_Z    = 1940    # filter head top Z (mm) — ports at this height
FILT_SUMP_Z    = 1600    # filter sump bottom Z (mm) — eye level for cartridge inspection

# Filter pipe (1" HDPE Sch40)
FILT_PIPE_OD   = 33      # 1" nominal HDPE OD (mm)
FILT_PIPE_WALL = 4       # pipe wall thickness (mm)

# Pump manifold pipe (1/2" HDPE Sch40)
PUMP_PIPE_OD   = 21      # 1/2" nominal HDPE OD (mm)
PUMP_PIPE_WALL = 3       # pipe wall thickness (mm)

# ���─ Right end zone — 4 IBCs in 2×2 stack (rev 5) ────────────────────────────
# Right-justified to far end wall: X=4,674–5,893mm.
# Layout (view from pinhole wall):
#   TOP    Blue #1 (near)     Blue #2 (far)    ← gravity feeds spray bar
#   BOTTOM Brown   (near)     Waste   (far)    ← receives water by gravity
# Weight migrates top→bottom during session (stability improves).
IBC_COL_X   = ZONE_R_START + 25   # = 4,674mm  [right-justified to end wall]
IBC_W       = 1219   # IBC overall width  (mm) — US 48" pallet format, includes cage
IBC_D       = 1016   # IBC overall depth  (mm) — US 40" pallet format, includes cage
IBC_H_600   = 1010   # 640L IBC overall height (mm) — includes pallet base + cage + bottle
IBC_H_STK   = 2020   # 2× stacked height (mm)

# IBC cage/pallet anatomy (US 48"×40" composite tote)
# Three parts: steel/plastic pallet base, HDPE blow-molded bottle, galvanized wire cage.
IBC_PALLET_H    = 168    # pallet base height including feet/runners (mm)
IBC_CAGE_TUBE_D = 25     # cage corner upright tube OD (mm)
IBC_CAGE_RAIL_W = 25     # cage top rail tube OD (mm)
IBC_CAGE_INSET  = 15     # cage tube center inset from pallet edge (mm)
IBC_BOTTLE_INSET = 30    # bottle wall inset from pallet edge (mm)
IBC_VALVE_Z     = 185    # DN50 butterfly valve CL above IBC base (mm)

# Near column (Yd=30–1,046mm): Blue #1 on top, Brown on bottom
BLUE_IBC_Y  = 30     # near column Yd start (mm) — pushed to near wall, 30mm clearance
BROWN_IBC_Y = BLUE_IBC_Y   # Brown is directly below Blue #1 (same Y column)

# Far column (Yd=1,316–2,332mm): Blue #2 on top, Waste on bottom
IBC_FAR_Y   = 1316   # far column Yd start (mm) — pushed to far wall, 30mm clearance
# Central plumbing corridor: Yd=1,046–1,316 (270mm wide)
WASTE_IBC_Y = IBC_FAR_Y   # Waste is directly below Blue #2 (same Y column)

# IBC right edge: IBC_COL_X + IBC_W = 4,674 + 1,219 = 5,893mm = C_LEN ✓
# Stack height: 2 × 1,010 = 2,020mm  (ceiling 2,388mm → 368mm headroom ✓)

# ── Processing tray — permanently installed in optical zone (rev 5) ──────────
PROC_TRAY_X_L  = FP_X_L + 20    # = 170mm — 20mm clearance from left rail [rev6: was 645]
PROC_TRAY_X_R  = FP_X_R - 20    # = 4,629mm — 20mm clearance from right rail
PROC_TRAY_W    = PROC_TRAY_X_R - PROC_TRAY_X_L   # = 4,459mm [rev6: was 3,984]
PROC_TRAY_D    = 2200            # depth in Y direction (mm)
PROC_TRAY_YD_NEAR = 80           # tray near edge Yd (mm) — clearance from pinhole wall
PROC_TRAY_YD_FAR  = PROC_TRAY_YD_NEAR + PROC_TRAY_D  # = 2,280mm
PROC_TRAY_RIM  = 50              # rim height (mm)
PROC_TRAY_PITCH = 10             # fall over tray depth for drainage (mm), 1:200
# Dual-axis pitch: tray slopes toward the low corner (near-pinhole, X-center).
# Primary slope: Yd direction, falling toward Yd=0 (pinhole wall).
# Secondary slope: X direction, falling toward X-center from both ends.
# Slope is achieved by tapered HDPE shim strips bonded to container floor
# under the tray (high end ~10mm thick, feathered to zero at drain end).
PROC_TRAY_SHIM_H   = 10         # shim strip max height at far rim (mm) = PITCH
PROC_TRAY_SHIM_W   = 50         # shim strip width (mm) — HDPE flat bar
PROC_TRAY_SHIM_N   = 5          # number of shim strips across tray depth
# Low point: sump well pressed into tray floor at near rim center.
# P-04 suction pickup tube sits in sump — no penetration of tray or container floor.
PROC_TRAY_DRAIN_X  = PH_X       # = 2,399mm — sump at X-center of tray (aligned with pinhole)
PROC_TRAY_DRAIN_YD = PROC_TRAY_YD_NEAR  # = 80mm — at near rim (low point of Yd slope)
PROC_TRAY_SUMP_W   = 150        # sump well width in X (mm)
PROC_TRAY_SUMP_D   = 100        # sump well depth in Yd (mm)
PROC_TRAY_SUMP_Z   = 20         # sump well depth below tray floor (mm)

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
# Deck height 100mm (75mm bracket arm + 25mm grate) clears the 50mm tray rim.
# Material: galvanized press-locked steel grating, 25mm thick (all 4 sections).
#
# Mounting varies by wall type:
#   Near/far walkways (long walls): brackets bolt to corrugated wall ribs.
#   Right walkway (IBC end):        floor-mounted posts bolted through container
#       floor at X≈4,640mm (just outside tray rim).  Cantilever arms reach back
#       over tray rim to support walkway.  34mm clearance to IBC stack.
#       Zero tray contact — posts on bare floor outside tray.
#   Left walkway (cargo door end):  REMOVABLE LIFT-OUT — no wall brackets.
#       Panel (hinged door) occupies the end wall at X=0 and slides inward
#       300mm for transport.  Left walkway must be removed before panel slides.
#       Left corners use butt joints (no miter) so near/far walkways start at
#       X=470 — entirely past the panel transport envelope (max X=420).
#       Only the left walkway (X=170–470) needs removal for transport.
#       Supported at ends by near/far walkway bracket arms at butt joints.
#       Processing tray side (X=470): removable bearer beam (50×50×3mm Al RHS)
#       runs along Yd, bolted to near/far bracket vertical legs, spanning
#       1,762mm.  Beam top flush at Z=75mm (grate bottom).
#       Cargo door side (X=170): 3 floor-standing support legs at X≈140 on
#       bare container floor (outside tray), plus a bearing strip (25×25×3mm
#       Al angle) on the processing tray rim (Z=50→75mm).
#       Zero processing tray contact — all supports outside or above tray.
#       Right corners use standard 45° miters (no panel conflict).
WALKWAY_W       = 300    # walkway width (mm) — bracket arm cantilever distance
WALKWAY_H       = 100    # deck height above floor (mm) — 75mm bracket arm + 25mm grate
WALKWAY_GRATE_T = 25     # grating thickness (mm) — standard press-locked (all 4 sections)
# Container structural rib spacing (ISO standard 20ft container)
CONTAINER_RIB_SPACING = 457   # mm (18 inches) — vertical corrugation flanges
# Wall-mounted cantilever brackets
WALKWAY_BRACKET_H = 150  # bracket vertical leg height on wall (mm)
WALKWAY_BRACKET_T = 8    # bracket plate thickness (mm)
WALKWAY_BRACKET_SPACING = CONTAINER_RIB_SPACING  # bracket spacing along walkway (mm)
# Right walkway (IBC end) — ceiling-hung design.
# No floor contact, no box beam.  Two longitudinal steel angle bearers
# (50×50×5mm) running full container width along Yd, suspended from ceiling
# corrugations by M10 threaded rod hangers at 457mm centers.  Grating spans
# 300mm between bearers.  Near/far ends bear on adjacent walkway brackets.
# All hangers placed at Yd < 2,025mm — clear of optical cone.
WALKWAY_RIGHT_W = WALKWAY_W  # 300mm — same width as near/far
WALKWAY_RIGHT_BEARER_SIZE = 25   # bearer angle leg (mm) — 25×25×5mm steel L-angle
WALKWAY_RIGHT_BEARER_T   = 5    # bearer angle thickness (mm)
WALKWAY_RIGHT_HANGER_D   = 10   # hanger threaded rod diameter (mm) — M10
WALKWAY_RIGHT_HANGER_N   = 5    # number of hanger pairs along Yd
WALKWAY_RIGHT_HANGER_Y1  = 320  # first pair Yd (mm) — shifted 20% toward film plane
                                # to clear shelf hanger zone (was 228.5mm = half-spacing)
WALKWAY_RIGHT_HANGER_L   = C_HGT - (WALKWAY_H - WALKWAY_GRATE_T)  # 2388 - 75 = 2313mm rod length
WALKWAY_RIGHT_CEIL_PLATE  = (100, 60, 6)  # ceiling bracket plate (L×W×T mm)
# Near walkway (pinhole side): X=tray_L to tray_R, Yd=0 to WALKWAY_W
WALKWAY_NEAR_YD = 0                          # near edge against pinhole wall
# Far walkway (film plane side): X=tray_L to tray_R, Yd=C_WID-WALKWAY_W to C_WID
WALKWAY_FAR_YD  = C_WID - WALKWAY_W         # = 1,962mm
# Left walkway (cargo door end): X=tray_L to tray_L+WALKWAY_W, Yd=0 to C_WID
# REMOVABLE — must be lifted out before sliding panel to transport position.
# Span between near/far bracket arms: C_WID - 2×WALKWAY_W = 1,762mm.
# Supported by: (a) bearer beam along Yd at X=470 (processing tray side),
# bolted to near/far bracket vertical legs, spanning 1,762mm; and
# (b) 3 floor-standing support legs at X≈140 (cargo door side, outside tray)
# plus a bearing strip on the processing tray rim (X=170).
# Zero processing tray contact — all supports outside or above tray.
WALKWAY_LEFT_X  = PROC_TRAY_X_L             # = 170mm (starts at tray left edge)
WALKWAY_LEFT_SPAN = C_WID - 2 * WALKWAY_W   # = 1,762mm span between bracket arms
# Left walkway intermediate support
LEFT_WK_BEARER_SIZE  = 50    # bearer beam section (mm) — 50×50×3mm Al RHS
LEFT_WK_BEARER_T     = 3     # bearer beam wall thickness (mm)
LEFT_WK_LEG_N        = 3     # number of floor-standing support legs (cargo door side)
LEFT_WK_LEG_SIZE     = 25    # support leg tube size (mm) — 25×25×3mm Al SHS
LEFT_WK_LEG_T        = 3     # support leg wall thickness (mm)
LEFT_WK_LEG_BASE     = 60    # foot plate size (mm) — 60×60×3mm with rubber pad
LEFT_WK_BEARING_STRIP = 25   # bearing strip height (mm) — 25×25×3mm Al angle on tray rim
# Right walkway (IBC end): ceiling-hung, same 300mm width as near/far
WALKWAY_RIGHT_X = PROC_TRAY_X_R - WALKWAY_RIGHT_W  # = 4,329mm (grating inner edge)
# Open processing area (center, clear of walkways):
PROC_OPEN_X_L  = WALKWAY_LEFT_X + WALKWAY_W   # = 570mm
PROC_OPEN_X_R  = WALKWAY_RIGHT_X              # = 4,429mm
PROC_OPEN_YD_N = WALKWAY_W                    # = 300mm
PROC_OPEN_YD_F = WALKWAY_FAR_YD               # = 1,962mm
PROC_OPEN_AREA = (PROC_OPEN_X_R - PROC_OPEN_X_L) * (PROC_OPEN_YD_F - PROC_OPEN_YD_N) / 1e6
                                               # = 6.42 m² open processing area

# ── External fill/drain ports — far end wall bulkhead fittings (rev 5) ───────
# 2" NPT bulkhead unions through container far end wall (X=C_LEN face).
# Flat steel reinforcing plate welded over corrugation before drilling.
# External plumbing panel — 4 ports stacked vertically on end wall centerline
EXT_PANEL_YD = C_WID // 2   # = 1,181mm — panel centered on container width
EXT_FILL_1_H = 2250    # fill Blue IBC-1 port height (mm) — above top-tier IBC top (2,082mm), gravity feed
EXT_FILL_2_H = 2150    # fill Blue IBC-2 port height (mm) — above top-tier IBC top, staggered for camlock clearance
EXT_DRAIN_3_H = 400    # drain Brown IBC-3 port height (mm) — bottom tier near
EXT_DRAIN_4_H = 200    # drain Waste IBC-4 port height (mm) — bottom tier far
# Legacy aliases for downstream code
EXT_FILL_H   = EXT_FILL_1_H
EXT_FILL_YD  = EXT_PANEL_YD
EXT_DRAIN_H  = EXT_DRAIN_4_H
EXT_DRAIN_YD = EXT_PANEL_YD

# ── Ventilation fans (150mm compact axial panel fans, interior-mounted) ───────
# Both fans are identical — one part number, same baffle duct assembly.
# Fan A: intake, far end wall (X = C_LEN face), low position.
#         Baffle duct extends 300mm into container interior from X=C_LEN wall.
# Fan B: exhaust, mounted on hinged panel (far corner zone), high position.
#         Baffle duct protrudes 300mm from panel EXTERIOR face.
#         Moves with panel on sliding carriage. In operational mode (panel at
#         X=0) duct extends into open doorway (X=0 to -300). In transport mode
#         (panel at X=300) duct occupies X=0 to 300 — inside container, clears
#         ISO doors. Wiring via flexible cable loop from fixed door frame.
FAN_DIAM    = 150    # fan / duct diameter (mm)
FAN_BODY_D  =  50    # panel fan body depth (mm)
FAN_A_H     = 600    # fan A center height AFF (mm — low position)
FAN_B_H     = 1800   # fan B center height AFF (mm — high position)
# Yd (width) positions — cross-ventilation diagonal: intake near-wall corner,
# exhaust far-wall corner.
FAN_A_YD    = FAN_DIAM // 2           # = 75mm  — near-wall corner (X=C_LEN wall)
FAN_B_YD    = C_WID - FAN_DIAM // 2  # = 2287mm — far-wall corner (panel face)

# Baffle duct (one per fan, welded galvanized steel)
# Fan A: duct extends into container interior from wall
# Fan B: duct protrudes from panel exterior face (into open doorway / container)
DUCT_DEPTH  = 300    # baffle duct depth (mm)
DUCT_HEIGHT = 200    # baffle duct opening height (mm)

# Shadow margins — distance from fan assembly to nearest cone edge (at worst depth)
# Fan A: duct extends inward from X=C_LEN wall
FAN_A_MARGIN = C_LEN - ZONE_R_START - FAN_DIAM // 2 - DUCT_DEPTH   # = 869 mm ✓
# Fan B: mounted on panel — intake grille on panel inner face, no duct on interior side.
# Shadow margin is panel inner face to ZONE_L_END = 40mm (corner zone thickness).
# Fan at Yd=2287mm: cone at Yd=2287 is well above X=625, so no cone intrusion.
FAN_B_MARGIN = PANEL_CORNER_T   # = 40 mm (fan flush with panel inner face)

# ── Output directories ────────────────────────────────────────────────────────
DIAGRAMS_DIR = "diagrams"
SVG_DIR      = "diagrams/svg"

def svg_path(png_path):
    """Convert a diagrams/*.png path to diagrams/svg/*.svg."""
    import os
    base = os.path.basename(png_path).replace(".png", ".svg")
    return os.path.join(SVG_DIR, base)

# ── Palette (shared drawing style) ───────────────────────────────────────────
C_OUT   = "#1A1A1A"   # outlines
C_CL    = "#2060A0"   # centre lines
C_DIM   = "#404040"   # dimensions
C_ALUM  = "#C8D8E8"   # aluminium fill
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
C_HINGE_PANEL  = "#C8C8C0"   # hinge panel body
C_FILM         = "#2060A0"   # film plane / muslin
C_PINHOLE_EQ   = "#CC6600"   # pinhole aperture
C_FAN          = "#A0A0A8"   # fans (A and B)
C_PROC_ZONE    = "#E8F5E9"   # processing tray zone

# ── Convenience summary (printed on import in debug mode) ────────────────────
if __name__ == "__main__":
    print("TBS-001 Constants (rev 5)")
    print(f"  Container:      {C_LEN} × {C_WID} × {C_HGT} mm")
    print(f"  Film plane:     {FP_W} × {FP_H} mm  (X={FP_X_L}–{FP_X_R})")
    print(f"  Muslin clamps:  {CLAMP_N_TOTAL} cam-lever clamps at {CLAMP_SPACING}mm centers")
    print(f"  Pinhole:        X={PH_X}  H={PH_H}  Ø{PH_D}mm  f/{PH_FNO}")
    print(f"  Rails:          X={RAIL_X_L} – {RAIL_X_R}  span={RAIL_SPAN}mm")
    print(f"  Max tilt:       {MAX_TILT_DEG:.1f}°")
    print(f"  Max swing:      {MAX_SWING_DEG:.1f}°")
    print(f"  Left zone:      X=0–{ZONE_L_END}mm (light trap drum only)")
    print(f"  Right zone:     X={ZONE_R_START}–{C_LEN}mm")
    print(f"  Cone at Y=FP_Y: X={cone_left(FP_Y):.0f} – {cone_right(FP_Y):.0f}")
    print(f"  Panel:          corner={PANEL_CORNER_T}mm  center={PANEL_CENTER_T}mm  step={PANEL_STEP}mm")
    print(f"  Panel zones:    corners Yd=0–{PANEL_CORNER_YD_L} / {PANEL_CORNER_YD_R}–{C_WID}  center Yd={PANEL_CORNER_YD_L}–{PANEL_CORNER_YD_R}")
    print(f"  Panel slide:    {PANEL_SLIDE}mm travel  floor gap={PANEL_FLOOR_GAP}mm (tray rim={PROC_TRAY_RIM}mm)")
    print(f"  IBC 2x2 stack:  X={IBC_COL_X}–{IBC_COL_X+IBC_W}  near Yd={BLUE_IBC_Y}  far Yd={IBC_FAR_Y}")
    print(f"  IBC stack H:    {IBC_H_STK}mm  (ceiling {C_HGT}mm → headroom {C_HGT - IBC_H_STK}mm)")
    print(f"  Proc tray:      X={PROC_TRAY_X_L}–{PROC_TRAY_X_R}  Yd={PROC_TRAY_YD_NEAR}–{PROC_TRAY_YD_FAR}  rim={PROC_TRAY_RIM}mm")
    print(f"  Walkway:        all={WALKWAY_W}mm  deck H={WALKWAY_H}mm  grate={WALKWAY_GRATE_T}mm")
    print(f"  Right walkway:  CEILING-HUNG  {WALKWAY_RIGHT_HANGER_N} hanger pairs  M{WALKWAY_RIGHT_HANGER_D} rod  {WALKWAY_RIGHT_BEARER_SIZE}×{WALKWAY_RIGHT_BEARER_SIZE}×{WALKWAY_RIGHT_BEARER_T}mm bearers")
    print(f"  Left walkway:   REMOVABLE LIFT-OUT  span={WALKWAY_LEFT_SPAN}mm  (bearer beam + {LEFT_WK_LEG_N} floor legs)")
    print(f"  Walkway open:   X={PROC_OPEN_X_L}–{PROC_OPEN_X_R}  Yd={PROC_OPEN_YD_N}–{PROC_OPEN_YD_F}  area={PROC_OPEN_AREA:.2f} m²")
    print(f"  Ext fill port:  H={EXT_FILL_H}mm  Yd={EXT_FILL_YD}mm")
    print(f"  Ext drain port: H={EXT_DRAIN_H}mm  Yd={EXT_DRAIN_YD}mm")
    print(f"  Evap cooler:    X={EVAP_X}–{EVAP_X+EVAP_W}  Yd={EVAP_Y} (pinhole wall face)")
    print(f"  Fan A (intake): far end wall  H={FAN_A_H}mm AFF  Ø{FAN_DIAM}mm  margin={FAN_A_MARGIN}mm")
    print(f"  Fan B (exhaust):door end wall H={FAN_B_H}mm AFF  Ø{FAN_DIAM}mm  margin={FAN_B_MARGIN}mm")
    print(f"  Baffle duct:    {DUCT_DEPTH}mm deep × {DUCT_HEIGHT}mm H")
