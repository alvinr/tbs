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
  with built-in 1:200 pitch for gravity drainage.  No track/tray conflict.
  IBCs loaded empty via cargo doors; filled/drained remotely through 2" NPT
  bulkhead fittings in the far end wall (X=C_LEN face).
  Left end zone freed up (light trap drum remains in hinge panel).
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
PANEL_SLIDE       = 300   # panel slide travel for transport (mm)

# ── Left end zone (X = 0–625 mm, shadow-free at all depths) ──────────────────
# Light trap drum in hinge panel center zone.  Waste drums removed in rev 5
# (replaced by waste IBC in right end zone).  Left zone now contains only
# the light trap drum and is available for future use (e.g. film prep area).
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

# ── Right end zone — 4 IBCs in 2×2 stack (rev 5) ────────────────────────────
# Right-justified to far end wall: X=4,674–5,893mm.
# Layout (view from pinhole wall):
#   TOP    Blue #1 (near)     Blue #2 (far)    ← gravity feeds spray bar
#   BOTTOM Brown   (near)     Waste   (far)    ← receives water by gravity
# Weight migrates top→bottom during session (stability improves).
IBC_COL_X   = ZONE_R_START + 25   # = 4,674mm  [right-justified to end wall]
IBC_W       = 1219   # IBC footprint width  (mm)
IBC_D       = 1016   # IBC footprint depth  (mm)
IBC_H_600   = 1010   # 600L IBC height (mm)
IBC_H_STK   = 2020   # 2× stacked height (mm)

# Near column (Yd=100–1,116mm): Blue #1 on top, Brown on bottom
BLUE_IBC_Y  = 100    # near column Yd start (mm)
BROWN_IBC_Y = BLUE_IBC_Y   # Brown is directly below Blue #1 (same Y column)

# Far column (Yd=1,141–2,157mm): Blue #2 on top, Waste on bottom
IBC_FAR_Y   = 1141   # far column Yd start (mm)  (25mm gap after near column)
WASTE_IBC_Y = IBC_FAR_Y   # Waste is directly below Blue #2 (same Y column)

# IBC right edge: IBC_COL_X + IBC_W = 4,674 + 1,219 = 5,893mm = C_LEN ✓
# Stack height: 2 × 1,010 = 2,020mm  (ceiling 2,388mm → 368mm headroom ✓)

# ── Processing tray — permanently installed in optical zone (rev 5) ──────────
PROC_TRAY_X_L  = FP_X_L + 20    # = 645mm — 20mm clearance from left rail
PROC_TRAY_X_R  = FP_X_R - 20    # = 4,629mm — 20mm clearance from right rail
PROC_TRAY_W    = PROC_TRAY_X_R - PROC_TRAY_X_L   # = 3,984mm
PROC_TRAY_D    = 2200            # depth in Y direction (mm)
PROC_TRAY_RIM  = 50              # rim height (mm)
PROC_TRAY_PITCH = 10             # fall over panel length for drainage (mm), 1:200

# ── External fill/drain ports — far end wall bulkhead fittings (rev 5) ───────
# 2" NPT bulkhead unions through container far end wall (X=C_LEN face).
# Flat steel reinforcing plate welded over corrugation before drilling.
EXT_FILL_H   = 1800    # fill port center height AFF (mm) — feeds top of Blue IBCs
EXT_FILL_YD  = BLUE_IBC_Y + IBC_D // 2   # = 608mm — centered on near column
EXT_DRAIN_H  = 200     # drain port center height AFF (mm) — bottom of Waste IBC
EXT_DRAIN_YD = IBC_FAR_Y + IBC_D // 2    # = 1,649mm — centered on far column

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
    print(f"  Pinhole:        X={PH_X}  H={PH_H}  Ø{PH_D}mm  f/{PH_FNO}")
    print(f"  Rails:          X={RAIL_X_L} – {RAIL_X_R}  span={RAIL_SPAN}mm")
    print(f"  Max tilt:       {MAX_TILT_DEG:.1f}°")
    print(f"  Max swing:      {MAX_SWING_DEG:.1f}°")
    print(f"  Left zone:      X=0–{ZONE_L_END}mm (light trap drum only)")
    print(f"  Right zone:     X={ZONE_R_START}–{C_LEN}mm")
    print(f"  Cone at Y=FP_Y: X={cone_left(FP_Y):.0f} – {cone_right(FP_Y):.0f}")
    print(f"  Panel:          corner={PANEL_CORNER_T}mm  center={PANEL_CENTER_T}mm  step={PANEL_STEP}mm")
    print(f"  Panel zones:    corners Yd=0–{PANEL_CORNER_YD_L} / {PANEL_CORNER_YD_R}–{C_WID}  center Yd={PANEL_CORNER_YD_L}–{PANEL_CORNER_YD_R}")
    print(f"  Panel slide:    {PANEL_SLIDE}mm travel")
    print(f"  IBC 2x2 stack:  X={IBC_COL_X}–{IBC_COL_X+IBC_W}  near Yd={BLUE_IBC_Y}  far Yd={IBC_FAR_Y}")
    print(f"  IBC stack H:    {IBC_H_STK}mm  (ceiling {C_HGT}mm → headroom {C_HGT - IBC_H_STK}mm)")
    print(f"  Proc tray:      X={PROC_TRAY_X_L}–{PROC_TRAY_X_R}  W={PROC_TRAY_W}mm  rim={PROC_TRAY_RIM}mm")
    print(f"  Ext fill port:  H={EXT_FILL_H}mm  Yd={EXT_FILL_YD}mm")
    print(f"  Ext drain port: H={EXT_DRAIN_H}mm  Yd={EXT_DRAIN_YD}mm")
    print(f"  Evap cooler:    X={EVAP_X}–{EVAP_X+EVAP_W}  Yd={EVAP_Y} (pinhole wall face)")
    print(f"  Fan A (intake): far end wall  H={FAN_A_H}mm AFF  Ø{FAN_DIAM}mm  margin={FAN_A_MARGIN}mm")
    print(f"  Fan B (exhaust):door end wall H={FAN_B_H}mm AFF  Ø{FAN_DIAM}mm  margin={FAN_B_MARGIN}mm")
    print(f"  Baffle duct:    {DUCT_DEPTH}mm deep × {DUCT_HEIGHT}mm H")
