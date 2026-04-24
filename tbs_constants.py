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
  Evap cooler relocated to pinhole wall face (Yd=0) at X=700–1,300mm — always
  shadow-free at Yd=0 regardless of X position.
  Drums repositioned to X=20–600mm, Yd=25–605mm (near cargo door end wall,
  Yd range entirely below light trap drum's Yd=806–1,556mm band — no X-clearance
  conflict).  Zone left boundary moves from X=1,100mm to X=625mm.
  Film plane widens from 3,549mm to 4,024mm (X=625–4,649mm).
  Pinhole recentred to X=2,637mm.  Max swing decreases from 31.4° to 28.3°
  (wider rail span over same Y travel).
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

# ── Left end zone (X = 0–625 mm, shadow-free at all depths) ──────────────────
DRUM_CX    = 0       # light trap drum centre X (mm) [unchanged]
DRUM_D     = 750     # revolving drum diameter (mm)
DRUM_R     = DRUM_D // 2
DRUM_H_LT  = 2000    # light trap drum height (mm)

# Black-water drums — near cargo door end wall, Yd band below light trap drum
# Light trap drum Yd centre ≈ C_WID/2 = 1,181mm, radius 375mm → Yd=806–1,556mm.
# Drums placed at Yd=25–605mm to avoid any Yd overlap → X clearance irrelevant.
DRUM_EQ_D      = 580    # 55-gal drum diameter (mm)
DRUM_EQ_H      = 870    # 55-gal single drum height (mm)
DRUM_EQ_R      = DRUM_EQ_D // 2    # = 290mm radius
DRUM_STACKED_H = 2 * DRUM_EQ_H    # = 1,740mm (2 drums stacked)
DRUM_LZ_CX     = 310               # centre X (mm)  [rev3: was 700; near cargo door wall]
DRUM_LZ_YD_LO  = 25                # near edge Yd   [rev3: was 475; just off pinhole wall]
DRUM_LZ_YD     = DRUM_LZ_YD_LO + DRUM_EQ_D // 2   # = 315mm centre
DRUM_LZ_YD_HI  = DRUM_LZ_YD_LO + DRUM_EQ_D        # = 605mm far edge
# Drum footprint: X=20–600mm, Yd=25–605mm — zone boundary = 600+25 = 625mm = FP_X_L ✓

# Evap cooler — relocated to pinhole wall face (Yd=0), right of drums in X
# At Yd=0 the cone collapses to a point → shadow-free at any X position.
EVAP_X     = 700     # evap cooler left edge X (mm)  [rev3: was 400; right of drums]
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
BA_H_LO    = 0       # battery bank bottom H (mm)
BA_H_HI    = 500     # battery bank top H (mm)

PUMP_X     = 2400    # pump manifold left edge X (mm)
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
    print(f"  IBC column:     X={IBC_COL_X}–{IBC_COL_X+IBC_W}  (right edge = {IBC_COL_X+IBC_W} vs C_LEN={C_LEN})")
    print(f"  Drums (left):   CX={DRUM_LZ_CX}  Yd={DRUM_LZ_YD_LO}–{DRUM_LZ_YD_HI}  stacked H={DRUM_STACKED_H}")
    print(f"  Evap cooler:    X={EVAP_X}–{EVAP_X+EVAP_W}  Yd={EVAP_Y} (pinhole wall face)")
