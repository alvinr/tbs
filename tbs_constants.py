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
  Panel + waste drums mounted on sliding rail systems for transport mode:
  panel on HGR20 linear rails (300mm travel), waste drums on V-groove dolly
  tracks (305mm travel).  In transport position, drums slide inward and panel
  slides inward 300mm so light trap drum clears the container exterior face
  by 5mm, allowing standard ISO cargo doors to close.
  Waste drums repositioned to X=40–620mm (left edge flush with corner panel
  inner face, right edge 5mm inside ZONE_L_END).  Single-person 15–20 min
  mode conversion.  Fixed door frame with EPDM compression seal at X=0.
"""

import math

# ── Container interior ────────────────────────────────────────────────────────
C_LEN  = 5893   # interior length, long axis X (mm)
C_WID  = 2362   # interior width = focal length = optical depth Y (mm)
C_HGT  = 2388   # interior height Z (mm)

# ── Film plane ────────────────────────────────────────────────────────────────
FP_H     = 2388   # film plane height (mm)          [unchanged]
FP_X_L   = 625    # film plane left edge X (mm)     [rev3: was 1,100; set by drum right edge + 25mm]
FP_X_R   = 4649   # film plane right edge X (mm)    [was 4,019 → wider right zone]
FP_W     = FP_X_R - FP_X_L   # = 4,024 mm          [rev3: was 3,549]
FP_Y     = 2262   # nominal depth from pinhole wall (mm)  [unchanged]
FP_Y_MIN = 100    # minimum carriage depth (mm)     [unchanged]

# ── Pinhole (recentred on new film plane) ─────────────────────────────────────
PH_X   = FP_X_L + FP_W // 2   # = 2,637 mm  [rev3: was 2,874]
PH_H   = 1194                  # height (mm) [unchanged]
PH_D   = 2.17                  # diameter (mm) — Rayleigh, f=2362, λ=550nm [unchanged]
PH_F   = C_WID                 # focal length = container width [unchanged]
PH_FNO = round(PH_F / PH_D)   # f/1088 [unchanged]

# ── Film plane rails ──────────────────────────────────────────────────────────
RAIL_X_L  = FP_X_L   # left rail X  (mm)   [rev3: 625mm; was 1,100]
RAIL_X_R  = FP_X_R   # right rail X (mm)   [was 4,019 → now 4,649]
RAIL_SPAN = RAIL_X_R - RAIL_X_L   # = 4,024 mm  [rev3: was 3,549]
RAIL_LEN  = 2200      # rail length  (mm)   [unchanged — same Y travel]
RAIL_OFF  = 100       # floor/ceiling offset (mm)  [unchanged]

# ── Movement ranges ───────────────────────────────────────────────────────────
MAX_TILT_DEG  = math.degrees(math.atan((FP_Y - FP_Y_MIN) / FP_H))
# = arctan(2162/2388) = 42.1°  [unchanged]

MAX_SWING_DEG = math.degrees(math.atan((FP_Y - FP_Y_MIN) / RAIL_SPAN))
# = arctan(2162/4024) = 28.3°  [rev3: was 31.4° with 3,549mm span]

# ── Equipment zones ───────────────────────────────────────────────────────────
ZONE_L_END   = FP_X_L    # left zone right boundary X  (= 625 mm)  [rev3: was 1,100]
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

# ── Sliding rail system — transport mode (rev 4) ─────────────────────────────
# Panel slides inward 300mm on HGR20 linear rails so the light trap drum
# clears the container exterior face, allowing ISO cargo doors to close.
# Waste drums slide inward 305mm on V-groove dolly tracks to clear the panel.
PANEL_SLIDE       = 300   # panel slide travel for transport (mm)
DRUM_SLIDE        = 305   # waste drum slide travel for transport (mm)
DRUM_DOLLY_H      = 30    # dolly track riser height (mm) — clears HGR20 floor rail

# ── Left end zone (X = 0–625 mm, shadow-free at all depths) ──────────────────
DRUM_CX    = 0       # light trap drum center X (mm) [unchanged]
DRUM_D     = 750     # revolving drum diameter (mm)
DRUM_R     = DRUM_D // 2
DRUM_H_LT  = 2200    # light trap drum height (mm) — increased for 330mm headroom at 1780mm operator height

# Black-water drums — LEFT end zone, one per Yd corner (rev 4: on slide dollies)
# Light trap drum Yd=806–1,556mm divides the zone into two clear corners.
# Near drum (pinhole wall corner): Yd=0–580mm   → gap to light trap = 226mm
# Far drum  (far wall corner):     Yd=1,782–2,362mm → gap to light trap = 226mm
# Both share CX=330mm (X=40–620mm).  Left edge flush with corner panel inner face.
# Right edge 5mm inside ZONE_L_END.  Zone boundary 620+5=625mm=FP_X_L ✓
DRUM_EQ_D     = 580    # 55-gal drum diameter (mm)
DRUM_EQ_H     = 870    # 55-gal single drum height (mm)
DRUM_EQ_R     = DRUM_EQ_D // 2    # = 290mm radius
# Near drum (pinhole wall corner) — left edge flush with corner panel inner face
DRUM_LZ_CX    = PANEL_CORNER_T + DRUM_EQ_R        # = 330mm center X (left edge at 40mm)
DRUM_LZ_YD_LO = 0                                 # near drum near edge Yd (flush with wall)
DRUM_LZ_YD    = DRUM_LZ_YD_LO + DRUM_EQ_D // 2   # = 290mm center
DRUM_LZ_YD_HI = DRUM_LZ_YD_LO + DRUM_EQ_D        # = 580mm far edge
# Far drum (far wall corner) — same X as near drum
DRUM_FZ_CX    = DRUM_LZ_CX                        # = 330mm (same X center)
DRUM_FZ_YD_LO = C_WID - DRUM_EQ_D                 # = 1,782mm (flush with far wall)
DRUM_FZ_YD    = DRUM_FZ_YD_LO + DRUM_EQ_R         # = 2,072mm center
DRUM_FZ_YD_HI = DRUM_FZ_YD_LO + DRUM_EQ_D        # = 2,362mm far edge

# Evap cooler — relocated to pinhole wall face (Yd=0), right of drums in X
# At Yd=0 the cone collapses to a point → shadow-free at any X position.
EVAP_X     = 930     # evap cooler left edge X (mm)  [rev4: was 700; clears drum D-1 transport X=925]
EVAP_W     = 600     # evap cooler width X (mm)       [unchanged]
EVAP_Y     = 0       # evap cooler near edge Yd (mm)  [rev3: was 100; now on pinhole wall]
EVAP_D     = 350     # evap cooler depth Y (mm)        [unchanged]
EVAP_H     = 800     # evap cooler height (mm)         [unchanged]

# ── Pinhole wall face (Y = 0, shadow-free) ────────────────────────────────────
EP_X       = 2050    # electrical panel left edge X (mm)
EP_W       = 300     # electrical panel width (mm)
EP_H_LO    = 900     # electrical panel bottom H (mm)
EP_H_HI    = 1500    # electrical panel top H (mm)

BA_X       = 2050    # battery bank left edge X (mm)
BA_W       = 500     # battery bank width (mm)
BA_H_LO    = 100     # battery bank bottom H (mm) — matches RAIL_OFF floor offset
BA_H_HI    = 600     # battery bank top H (mm)

PUMP_X     = 2600    # pump manifold left edge X (mm) — right of battery right edge (2550) + 50mm gap
PUMP_W     = 300     # pump manifold width (mm)
PUMP_H_LO  = 200     # pump manifold bottom H (mm)
PUMP_H_HI  = 600     # pump manifold top H (mm)

# ── Right end zone — IBC column Y-stacked, right-justified (X=4,674–5,893mm) ─
IBC_COL_X   = ZONE_R_START + 25   # = 4,674mm  [was 4,044; right-justified to end wall]
IBC_W       = 1219   # IBC footprint width  (mm)
IBC_D       = 1016   # IBC footprint depth  (mm)
IBC_H_600   = 1010   # 600L IBC height (mm)
IBC_H_STK   = 2020   # 2× stacked height (mm)

BLUE_IBC_Y  = 100    # Blue IBC stack front depth from pinhole wall (mm)
# Blue IBC stack rear: BLUE_IBC_Y + IBC_D = 1,116 mm

BROWN_IBC_Y = 1141   # Brown IBC depth start (mm)  (gap = 25mm after blue stack)
# Brown IBC rear: BROWN_IBC_Y + IBC_D = 2,157 mm  (< C_WID=2,362 ✓)

# IBC right edge: IBC_COL_X + IBC_W = 4,674 + 1,219 = 5,893mm = C_LEN ✓

# ── Ventilation fans (150mm compact axial panel fans, interior-mounted) ───────
# Both fans are identical — one part number, same baffle duct assembly.
# Fan A: intake, far end wall (X = C_LEN face), low position.
# Fan B: exhaust, cargo door end wall (X = 0 face), high position.
FAN_DIAM    = 150    # fan / duct diameter (mm)
FAN_BODY_D  =  50    # panel fan body depth (mm)
FAN_A_H     = 600    # fan A center height AFF (mm — low position)
FAN_B_H     = 1800   # fan B center height AFF (mm — high position)
# Yd (width) positions — cross-ventilation diagonal: intake near-wall corner,
# exhaust far-wall corner.  Clears both waste drum columns (D-1 near, D-2 far)
# with ≥830mm vertical separation even where Yd overlaps.
FAN_A_YD    = FAN_DIAM // 2           # = 75mm  — near-wall corner (X=C_LEN wall)
FAN_B_YD    = C_WID - FAN_DIAM // 2  # = 2287mm — far-wall corner (X=0 wall)

# Baffle duct (one per fan, interior-mounted, welded galvanized steel)
DUCT_DEPTH  = 300    # baffle duct depth into container interior (mm)
DUCT_HEIGHT = 200    # baffle duct opening height (mm)

# Shadow margins — distance from fan assembly to nearest cone edge (at worst depth)
# Fan A right margin: C_LEN − ZONE_R_START − FAN_DIAM/2 − DUCT_DEPTH = 5893−4649−75−300 = 869mm
# Fan B left margin: ZONE_L_END − FAN_DIAM/2 − DUCT_DEPTH = 625−75−300 = 250mm
FAN_A_MARGIN = C_LEN - ZONE_R_START - FAN_DIAM // 2 - DUCT_DEPTH   # = 869 mm ✓
FAN_B_MARGIN = ZONE_L_END - FAN_DIAM // 2 - DUCT_DEPTH              # = 250 mm ✓

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

# ── Convenience summary (printed on import in debug mode) ────────────────────
if __name__ == "__main__":
    _drum_left = DRUM_LZ_CX - DRUM_EQ_R
    _drum_right = DRUM_LZ_CX + DRUM_EQ_R
    print("TBS-001 Constants")
    print(f"  Container:      {C_LEN} × {C_WID} × {C_HGT} mm")
    print(f"  Film plane:     {FP_W} × {FP_H} mm  (X={FP_X_L}–{FP_X_R})")
    print(f"  Pinhole:        X={PH_X}  H={PH_H}  Ø{PH_D}mm  f/{PH_FNO}")
    print(f"  Rails:          X={RAIL_X_L} – {RAIL_X_R}  span={RAIL_SPAN}mm")
    print(f"  Max tilt:       {MAX_TILT_DEG:.1f}°")
    print(f"  Max swing:      {MAX_SWING_DEG:.1f}°")
    print(f"  Left zone:      X=0–{ZONE_L_END}mm")
    print(f"  Right zone:     X={ZONE_R_START}–{C_LEN}mm")
    print(f"  Cone at Y=FP_Y: X={cone_left(FP_Y):.0f} – {cone_right(FP_Y):.0f}")
    print(f"  Panel:          corner={PANEL_CORNER_T}mm  center={PANEL_CENTER_T}mm  step={PANEL_STEP}mm")
    print(f"  Panel zones:    corners Yd=0–{PANEL_CORNER_YD_L} / {PANEL_CORNER_YD_R}–{C_WID}  center Yd={PANEL_CORNER_YD_L}–{PANEL_CORNER_YD_R}")
    print(f"  Panel slide:    {PANEL_SLIDE}mm travel  drum slide: {DRUM_SLIDE}mm travel")
    print(f"  IBC column:     X={IBC_COL_X}–{IBC_COL_X+IBC_W}  (right edge = {IBC_COL_X+IBC_W} vs C_LEN={C_LEN})")
    print(f"  Drum near:      CX={DRUM_LZ_CX}  X={_drum_left}–{_drum_right}  Yd={DRUM_LZ_YD_LO}–{DRUM_LZ_YD_HI}  H={DRUM_EQ_H}")
    print(f"  Drum far:       CX={DRUM_FZ_CX}  X={_drum_left}–{_drum_right}  Yd={DRUM_FZ_YD_LO}–{DRUM_FZ_YD_HI}  H={DRUM_EQ_H}")
    print(f"  Evap cooler:    X={EVAP_X}–{EVAP_X+EVAP_W}  Yd={EVAP_Y} (pinhole wall face)")
    print(f"  Fan A (intake): far end wall  H={FAN_A_H}mm AFF  Ø{FAN_DIAM}mm  margin={FAN_A_MARGIN}mm")
    print(f"  Fan B (exhaust):door end wall H={FAN_B_H}mm AFF  Ø{FAN_DIAM}mm  margin={FAN_B_MARGIN}mm")
    print(f"  Baffle duct:    {DUCT_DEPTH}mm deep × {DUCT_HEIGHT}mm H")
