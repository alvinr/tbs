"""
tbs_constants.py — Single source of truth for TBS-001 geometry and equipment.

All generator scripts should import from this module:
    from tbs_constants import *

Redesign basis (2026-04-23):
  Film plane reduced from 5,893mm to 2,920mm wide to create provably
  shadow-free end zones.  Pinhole recentred on new film plane.
  Max swing increases from 20.3° to 36.5° (shorter span, same Y travel).
"""

import math

# ── Container interior ────────────────────────────────────────────────────────
C_LEN  = 5893   # interior length, long axis X (mm)
C_WID  = 2362   # interior width = focal length = optical depth Y (mm)
C_HGT  = 2388   # interior height Z (mm)

# ── Film plane (redesigned) ───────────────────────────────────────────────────
FP_W     = 2920   # film plane width (mm)          [was 5,893]
FP_H     = 2388   # film plane height (mm)          [unchanged]
FP_X_L   = 1100   # film plane left edge X (mm)     [was 0]
FP_X_R   = 4019   # film plane right edge X (mm)    [was 5,893]
FP_Y     = 2262   # nominal depth from pinhole wall (mm)  [unchanged]
FP_Y_MIN = 100    # minimum carriage depth (mm)     [unchanged]

# Derived: half-widths for cone calculation
_FP_HL = FP_X_R - FP_X_L   # = 2,919 mm span

# ── Pinhole (recentred on new film plane) ─────────────────────────────────────
PH_X   = FP_X_L + FP_W // 2   # = 2,560 mm  [was 2,946]
PH_H   = 1194                  # height (mm) [unchanged]
PH_D   = 2.17                  # diameter (mm) — Rayleigh, f=2362, λ=550nm [unchanged]
PH_F   = C_WID                 # focal length = container width [unchanged]
PH_FNO = round(PH_F / PH_D)   # f/1088 [unchanged]

# ── Film plane rails ──────────────────────────────────────────────────────────
RAIL_X_L  = FP_X_L   # left rail X  (mm)   [was 200]
RAIL_X_R  = FP_X_R   # right rail X (mm)   [was 5,693]
RAIL_SPAN = RAIL_X_R - RAIL_X_L   # = 2,919 mm  [was 5,493]
RAIL_LEN  = 2200      # rail length  (mm)   [unchanged — same Y travel]
RAIL_OFF  = 100       # floor/ceiling offset (mm)  [unchanged]

# ── Movement ranges ───────────────────────────────────────────────────────────
MAX_TILT_DEG  = math.degrees(math.atan((FP_Y - FP_Y_MIN) / FP_H))
# = arctan(2162/2388) = 42.1°  [unchanged]

MAX_SWING_DEG = math.degrees(math.atan((FP_Y - FP_Y_MIN) / RAIL_SPAN))
# = arctan(2162/2919) = 36.5°  [was 20.3° with 5,493mm span]

# ── Equipment zones ───────────────────────────────────────────────────────────
ZONE_L_END   = FP_X_L    # left zone right boundary X  (= 1,100 mm)
ZONE_R_START = FP_X_R    # right zone left boundary X  (= 4,019 mm)

# ── Optical cone helper ───────────────────────────────────────────────────────
def cone_left(y):
    """X coordinate of cone left boundary at depth y from pinhole wall."""
    return PH_X - (PH_X - FP_X_L) * y / FP_Y

def cone_right(y):
    """X coordinate of cone right boundary at depth y from pinhole wall."""
    return PH_X + (FP_X_R - PH_X) * y / FP_Y

# ── Left end zone equipment (X = 0–1,100 mm, shadow-free at all depths) ──────
DRUM_CX    = 0       # light trap drum centre X (mm) [unchanged]
DRUM_D     = 750     # revolving drum diameter (mm)
DRUM_R     = DRUM_D // 2
DRUM_H_LT  = 2000    # light trap drum height (mm)

EVAP_X     = 400     # evap cooler left edge X (mm)  [was 1,380]
EVAP_W     = 600     # evap cooler width X (mm)
EVAP_Y     = 100     # evap cooler depth from pinhole wall (mm)
EVAP_D     = 350     # evap cooler depth Y (mm)
EVAP_H     = 800     # evap cooler height (mm)

# ── Pinhole wall face (Y = 0, shadow-free) ────────────────────────────────────
EP_X       = 2050    # electrical panel left edge X (mm)
EP_W       = 300     # electrical panel width (mm)
EP_H_LO    = 900     # electrical panel bottom H (mm)
EP_H_HI    = 1500    # electrical panel top H (mm)

BA_X       = 2050    # battery bank left edge X (mm)
BA_W       = 500     # battery bank width (mm)
BA_H_LO    = 0       # battery bank bottom H (mm)
BA_H_HI    = 500     # battery bank top H (mm)

PUMP_X     = 2400    # pump manifold left edge X (mm)
PUMP_W     = 300     # pump manifold width (mm)
PUMP_H_LO  = 200     # pump manifold bottom H (mm)
PUMP_H_HI  = 600     # pump manifold top H (mm)

# ── Right end zone — IBC column Y-stacked (X = 4,044–5,263 mm) ───────────────
IBC_COL_X   = 4044   # IBC column left edge X (mm)  [was split across both wings]
IBC_W       = 1219   # IBC footprint width  (mm)
IBC_D       = 1016   # IBC footprint depth  (mm)
IBC_H_600   = 1010   # 600L IBC height (mm)
IBC_H_STK   = 2020   # 2× stacked height (mm)

BLUE_IBC_Y  = 100    # Blue IBC stack front depth from pinhole wall (mm)
# Blue IBC stack rear: BLUE_IBC_Y + IBC_D = 1,116 mm

BROWN_IBC_Y = 1141   # Brown IBC depth start (mm)  (gap = 25mm after blue stack)
# Brown IBC rear: BROWN_IBC_Y + IBC_D = 2,157 mm  (< C_WID=2,362 ✓)

# ── Right end zone — drum column (X = 5,288–5,868 mm) ────────────────────────
DRUM_COL_X  = 5288   # drum column left edge X (mm)
DRUM_EQ_D   = 580    # 55-gal drum diameter (mm)
DRUM_EQ_H   = 870    # 55-gal drum height (mm)
DRUM1_Y     = 100    # drum 1 depth from pinhole wall (mm)
DRUM2_Y     = 705    # drum 2 depth start (25mm gap after drum 1)
# Drum column right edge: DRUM_COL_X + DRUM_EQ_D = 5,868 mm  (< C_LEN=5,893 ✓)

# ── Output directory ──────────────────────────────────────────────────────────
DIAGRAMS_DIR = "diagrams"

# ── Palette (shared drawing style) ───────────────────────────────────────────
C_OUT   = "#1A1A1A"   # outlines
C_CL    = "#2060A0"   # centre lines
C_DIM   = "#404040"   # dimensions
C_ALUM  = "#C8D8E8"   # aluminium fill
C_STEEL = "#B0B0B8"   # steel fill
C_GASKT = "#5A3020"   # gasket/neoprene

# ── Convenience summary (printed on import in debug mode) ────────────────────
if __name__ == "__main__":
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
