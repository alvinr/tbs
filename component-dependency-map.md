<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Component Dependency Map

> **Machine source of truth: `dependencies.yml`.** The structured
> `script → output-file` graph (which generator/model writes which PNG / `.skp` / `.rb`) lives there
> — validated by `lint.py` so it can't drift — and the per-constant cascade is **computed** from it
> (`python3 src/generators/lint.py --cascade <CONSTANT>`; enforced at commit time). This document is
> now the **human design rationale** that the YAML can't hold: §1 the component → constant registry,
> §2 the script legend, §3 the subsystem × diagram matrix, and §3.1 the per-model "what it builds and
> why" narrative. The old hand-maintained §4 cascade table was retired into the computed view above.

This document is the design-rationale companion for maintaining consistency across all TBS-001
engineering diagrams. When any component changes — position, dimension, or specification — consult:

1. **Section 1** to find the controlling constant in `tbs_constants.py`
2. **Section 2 / 3** for the subsystem ↔ diagram context
3. **`lint.py --cascade <CONSTANT>`** for the exact scripts to re-run and outputs to regenerate

All shared constants live in `tbs_constants.py`. Change a value there once; re-run the affected
scripts (the cascade command lists them); all diagrams update consistently.

---

## 1. Component Registry

Each subsystem lists its key physical parameters and the `tbs_constants.py` variable(s) that
control it. Scripts should import from `tbs_constants` rather than hardcoding these values.

### 1.1 Container Structure

| Parameter | Value | Constant |
|-----------|-------|----------|
| Interior length (long axis X) | <!-- BEGIN cdm:C_LEN -->5,893<!-- END cdm:C_LEN -->mm | `C_LEN` |
| Interior width (optical depth Y) | <!-- BEGIN cdm:C_WID -->2,362<!-- END cdm:C_WID -->mm | `C_WID` |
| Interior height Z | <!-- BEGIN cdm:C_HGT -->2,388<!-- END cdm:C_HGT -->mm | `C_HGT` |

*Components: corrugated steel long walls, short end walls (cargo door end / far end), roof,
bamboo floor, corner castings, corner posts, structural corrugation ribs.*

*Reports: [Container Basics](container-report.md) Part 4/6/8 (Orientation-B geometry, interior conversion + light-sealing + pinhole-wall prep, structural modification).*

*Diagrams: floor plan (FP), line of sight (LOS), assembly overview (AO), assembly fabrication (AF), film plane mechanism (FPM), electrical wiring (ES), water system (WS), hinged panel (HP), lighttrap (LT), plate drawing (PD), schematic (SC), walkway (WK).*

### 1.2 Optical Aperture

| Parameter | Value | Constant |
|-----------|-------|----------|
| Pinhole X position (long axis) | <!-- BEGIN cdm:PH_X -->2,399<!-- END cdm:PH_X -->mm | `PH_X` |
| Pinhole center height | <!-- BEGIN cdm:PH_H -->1,194<!-- END cdm:PH_H -->mm | `PH_H` |
| Pinhole diameter | Ø<!-- BEGIN cdm:PH_D -->2.17<!-- END cdm:PH_D -->mm | `PH_D` |
| f-number | f/<!-- BEGIN fact:f_number -->1088<!-- END fact:f_number --> | `PH_FNO` |
| Focal length | <!-- BEGIN fact:focal_length_mm -->2,362<!-- END fact:focal_length_mm -->mm | `PH_F` (= `C_WID`) |
| Wall frame / plate outer dim (square) | <!-- BEGIN cdm:PLATE_OD -->600<!-- END cdm:PLATE_OD -->mm | `PLATE_OD` |
| Aluminum plate thickness | <!-- BEGIN cdm:PLATE_THK -->15<!-- END cdm:PLATE_THK -->mm | `PLATE_THK` |
| Wall frame steel thickness | <!-- BEGIN cdm:WALL_FRAME_T -->6<!-- END cdm:WALL_FRAME_T -->mm | `WALL_FRAME_T` |
| Pinhole disc diameter | Ø<!-- BEGIN cdm:PINHOLE_DISC_D -->50<!-- END cdm:PINHOLE_DISC_D -->mm | `PINHOLE_DISC_D` |
| Pinhole disc thickness | <!-- BEGIN cdm:PINHOLE_DISC_T -->0.1<!-- END cdm:PINHOLE_DISC_T -->mm | `PINHOLE_DISC_T` |

*Components: wall frame (S275 steel), interchangeable pinhole plate (ICP-02 / SS-302 disc,
Lenox Laser laser-drilled), lens plate, shutter plate and channel. Frame, plate, and disc
dimensions are single-sourced in the table above (`generate_plate_drawing.py` reads the same constants).*

*Reports: [Pinhole Report](pinhole-report.md) §3/§4/§5/§7 (wall frame, pinhole plate, lens plate, light sealing); [Optics Report](pinhole-optics-report.md) Part 3/11 (optimal-diameter formulas, as-built f/1088 numbers).*

*Diagrams: floor plan (FP), line of sight (LOS), assembly overview (AO), assembly fabrication (AF), film plane mechanism (FPM), tilt-swing board (TSB), plate drawing (PD), schematic (SC).*

### 1.3 Film Plane Mechanism

| Parameter | Value | Constant |
|-----------|-------|----------|
| Film plane left edge X | <!-- BEGIN cdm:FP_X_L -->150<!-- END cdm:FP_X_L -->mm | `FP_X_L` |
| Film plane right edge X | <!-- BEGIN cdm:FP_X_R -->4,649<!-- END cdm:FP_X_R -->mm | `FP_X_R` |
| Film plane width | <!-- BEGIN cdm:FP_W -->4,499<!-- END cdm:FP_W -->mm | `FP_W` |
| Film plane height | <!-- BEGIN cdm:FP_H -->2,094<!-- END cdm:FP_H -->mm | `FP_H` |
| Nominal depth from pinhole wall | <!-- BEGIN cdm:FP_Y -->2,262<!-- END cdm:FP_Y -->mm | `FP_Y` |
| Minimum carriage depth | <!-- BEGIN cdm:FP_Y_MIN -->100<!-- END cdm:FP_Y_MIN -->mm | `FP_Y_MIN` |
| Left rail X | <!-- BEGIN cdm:RAIL_X_L -->150<!-- END cdm:RAIL_X_L -->mm | `RAIL_X_L` |
| Right rail X | <!-- BEGIN cdm:RAIL_X_R -->4,649<!-- END cdm:RAIL_X_R -->mm | `RAIL_X_R` |
| Rail span | <!-- BEGIN cdm:RAIL_SPAN -->4,499<!-- END cdm:RAIL_SPAN -->mm | `RAIL_SPAN` |
| Rail length (Y travel) | <!-- BEGIN cdm:RAIL_LEN -->2,200<!-- END cdm:RAIL_LEN -->mm | `RAIL_LEN` |
| Max tilt (single-axis, Option A) | ±<!-- BEGIN cdm:MAX_TILT_DEG -->40<!-- END cdm:MAX_TILT_DEG -->° | `MAX_TILT_DEG` |
| Max swing (single-axis, Option A) | ±<!-- BEGIN cdm:MAX_SWING_DEG -->28<!-- END cdm:MAX_SWING_DEG -->° | `MAX_SWING_DEG` |
| Cross-slide Z travel (tilt) | ~250mm | `XSLIDE_Z_TRAVEL` |
| Cross-slide X travel (swing) | ~263mm | `XSLIDE_X_TRAVEL` |
| Cross-slide stroke (spec) | <!-- BEGIN cdm:XSLIDE_STROKE -->300<!-- END cdm:XSLIDE_STROKE -->mm | `XSLIDE_STROKE` |
| Cross-slides total (2/corner) | <!-- BEGIN cdm:XSLIDE_N -->8<!-- END cdm:XSLIDE_N --> | `XSLIDE_N` |

*Components (a fixed-size rigid plane on slide-and-clamp corners): 2"×2"×1/8" **plain-6061
aluminum** angle frame (expendable) + corner L-brackets, 4× **3×1.5 6061 Al U-channel** depth rails
(Grainger 795M51, ceiling + floor), 4× **4-wheel acetal skates** (Ø32 load + Ø20 keeper rollers
on Ø10 304 axle pins), **8× 304 flat-bar cross-slides (Z tilt + X swing) on UHMW self-lube pads +
adjustable gibs** (the 2-axis corner stage that absorbs the rigid-rotation arc travel), 4× **Belden
UJ-SS750x375 U-joints** (303/416 SS, booted), 12× cam-lever rail clamps, **single rigid ACM
backing panel**, Duvetyne curtain seals, rail felt light-trap strips, 58× nylon spring clamps
at 150mm centers (muslin attachment). The plane stays a fixed-size flat rectangle — it does not
stretch or twist; single-axis tilt/swing envelope (tilt ±40° / swing ±28°).*

*Reports: [Film Plane Mechanism](film-plane-mechanism-report.md) §4/§5/§7 (mechanism design, tilt/swing configurations, parts list); [Muslin Clamp System](film-clamp-mechanism-report.md) §2/§3 (spring-clip layout + jaw mechanism).*

*Diagrams: floor plan (FP), line of sight (LOS), assembly overview (AO), assembly fabrication (AF), film plane mechanism (FPM), film plane distortion (FPD), tilt-swing distortion (TSD).*

### 1.4 Tilt-Swing Front Board

| Parameter | Value | Constant |
|-----------|-------|----------|
| Pinhole X (board centers here) | <!-- BEGIN cdm:PH_X -->2,399<!-- END cdm:PH_X -->mm | `PH_X` |
| Max tilt/swing | ±<!-- BEGIN cdm:FRONT_BOARD_MAX_DEG -->5.3<!-- END cdm:FRONT_BOARD_MAX_DEG -->° | `FRONT_BOARD_MAX_DEG` (computed from arm + travel) |
| Resolution | <!-- BEGIN fact:front_board_click_deg -->0.012<!-- END fact:front_board_click_deg -->°/click | `FRONT_BOARD_CLICK_DEG` (computed from screw + detents) |

*Components: ICP-01 outer adapter frame (600×600×40mm Al 6061-T6), ICP-02 inner carrier plate
(Ø320×25mm Al 6061-T6), GE50-DO-2RS spherical plain bearing (SKF, PTFE-lined), 4× M8×1.0
adjustment screws, hemispherical ball-socket inserts, 36-detent knurled knobs, ICP-10 neoprene
bellows (4-pleat, Ø290 ID → Ø360 OD).*

*Reports: [Tilt-Swing Front Board](tilt-swing-board-report.md) §2/§4/§5/§6/§12 (mechanism overview, pivot bearing, adjustment, light sealing/bellows, parts list).*

*Diagrams: tilt-swing board (TSB), tilt-swing distortion (TSD).*

### 1.5 Housed Revolving-Door Light Lock (rev 8)

| Parameter | Value | Constant |
|-----------|-------|----------|
| Light-lock center X (cargo door end wall) | <!-- BEGIN cdm:DRUM_CX -->-400<!-- END cdm:DRUM_CX -->mm | `DRUM_CX` |
| Fixed housing outer diameter | <!-- BEGIN cdm:DRUM_D -->900<!-- END cdm:DRUM_D -->mm | `DRUM_D` |
| Housing radius | 450mm | `DRUM_R` / `LT_HOUSING_R` |
| Drum outer radius (rotating) | <!-- BEGIN cdm:LT_DRUM_OR -->432<!-- END cdm:LT_DRUM_OR -->mm | `LT_DRUM_OR` |
| Opening arc (each) | <!-- BEGIN cdm:LT_OPENING_DEG -->80<!-- END cdm:LT_OPENING_DEG -->° | `LT_OPENING_DEG` |
| Top Z (walkway-lifted) | <!-- BEGIN cdm:DRUM_H_LT -->2,250<!-- END cdm:DRUM_H_LT -->mm | `DRUM_H_LT` |

*Components: fixed Ø900 aluminum housing with two 80° openings (exterior + interior-onto-walkway,
180° apart); single-opening C-shell rotating drum (Ø864, ~Ø850 bore, NO internal fins) — light-tight
by geometry; 5mm top/bottom caps, 75mm stub shafts (×2), 2× SKF 6215-2RS1 sealed bearings, drum↔housing
felt/brush wiper seals (opening edges + top/bottom rings), 100mm SS interior grab rail, housing-to-panel
neoprene compression strip. Replaces the failed Ø750 4-fin drum.*

*Reports: [Light Trap Selection](light-trap-selection.md) §4/§5 (housed revolving-door specification, light-path verification); [Hinged Light-Trap Panel](hinged-panel-report.md) §3 (as-integrated light lock: spec, bearings, drum seals).*

*Diagrams: floor plan (FP), line of sight (LOS), assembly overview (AO), assembly fabrication (AF), hinged panel (HP), lighttrap (LT).*

### 1.6 Hinged Cargo-Door Panel

| Parameter | Value | Constant |
|-----------|-------|----------|
| Panel width | <!-- BEGIN cdm:C_WID -->2,362<!-- END cdm:C_WID -->mm | `C_WID` |
| Panel height | <!-- BEGIN cdm:C_HGT -->2,388<!-- END cdm:C_HGT -->mm | `C_HGT` |
| Panel thickness | 120mm | — (hardcoded in scripts) |

*Components: 2×2×0.120in steel frame, 1/8" HDPE plastic skins (both faces; 18mm-ply Fan-B mount band), 20mm EPDM compression
gasket in machined channel + 2× vertical cut seals (Yd180/2287), vertical **Ø89×8mm CHS pivot
post** (rev10 — the reused film far-left upright, on a thrust collar + top/bottom hub bearings;
structural sign-off) carrying the ~56° transport swing, 4× Southco C2-33 cam compression latches,
top + bottom wall stays (transport lock), Ø900mm housed revolving-door light-lock aperture in the
B2 punch-out bay.*

*Reports: [Hinged Light-Trap Panel](hinged-panel-report.md) §2/§4/§5/§7/§8 (panel construction, hinges + Southco cam latches, rotating transport swing, fixed door frame, parts list).*

*Diagrams: assembly overview (AO), assembly fabrication (AF), hinged panel (HP), lighttrap (LT).*

### 1.7 Ventilation System

| Parameter | Value | Constant |
|-----------|-------|----------|
| Fan diameter (both fans) | <!-- BEGIN cdm:FAN_DIAM -->150<!-- END cdm:FAN_DIAM -->mm | `FAN_DIAM` |
| Panel fan body depth | <!-- BEGIN cdm:FAN_BODY_D -->50<!-- END cdm:FAN_BODY_D -->mm | `FAN_BODY_D` |
| Fan A center height AFF (below X1, in corridor) | <!-- BEGIN cdm:FAN_A_H -->2,000<!-- END cdm:FAN_A_H -->mm | `FAN_A_H` |
| Fan B center height AFF (low) | <!-- BEGIN cdm:FAN_B_H -->600<!-- END cdm:FAN_B_H -->mm | `FAN_B_H` |
| Fan A Yd position (below the X1 fill port, plumbing corridor) | <!-- BEGIN cdm:FAN_A_YD -->1,181<!-- END cdm:FAN_A_YD -->mm | `FAN_A_YD` |
| Fan B Yd position (near pinhole wall, near corner — rev9/B2 swap) | <!-- BEGIN cdm:FAN_B_YD -->365<!-- END cdm:FAN_B_YD -->mm | `FAN_B_YD` |
| Baffle duct depth | <!-- BEGIN cdm:DUCT_DEPTH -->300<!-- END cdm:DUCT_DEPTH -->mm | `DUCT_DEPTH` |
| Baffle duct height | <!-- BEGIN cdm:DUCT_HEIGHT -->200<!-- END cdm:DUCT_HEIGHT -->mm | `DUCT_HEIGHT` |
| Fan A shadow margin (from cone) | <!-- BEGIN cdm:FAN_A_MARGIN -->869<!-- END cdm:FAN_A_MARGIN -->mm | `FAN_A_MARGIN` |
| Fan B shadow margin (from cone) | <!-- BEGIN cdm:FAN_B_MARGIN -->40<!-- END cdm:FAN_B_MARGIN -->mm | `FAN_B_MARGIN` |

*Components: Fan A — 150mm compact axial panel fan, sealed end wall, exhaust, Circuit A,
in the 270mm plumbing corridor directly **below the X1 fill port** — the only
full-height clear channel past the 1,000L direct-stack. Fan B —
identical fan, mounted on hinged panel (near corner zone by the pinhole wall,
 so its conduit runs along the pinhole wall near the pivot side), intake,
Circuit B, low position. Fan A mounts on interior face of a 300mm deep light-safe baffle duct with 2 offset
steel baffles (65% height each, horizontal S-path); exterior face has a passive weatherproof louvre grille.
Fan B has the same baffle duct protruding from the panel exterior face — draws fresh air from the
open doorway during operation. Fan B swings with the panel about the pivot; wiring via
flexible coiled cable (with swing slack) from the fixed door frame (Circuit B).*

*Report: [Ventilation & Cooling System](ventilation-report.md) — authoritative specification for fan system, baffle ducts, operating modes, and shade canopy.*

*Reports: [Ventilation & Cooling](ventilation-report.md) §4/§7/§8 (fans A/B + baffle ducts, operating modes, electrical integration); [Electrical](electrical-report.md) §7.2 (Circuit F ventilation fans).*

*Diagrams: lighttrap sheet 1 combined elevation (LT), lighttrap sheet 2 ventilation details (LT), electrical sheet 1 wiring (ES), floor plan (FP), assembly overview (AO).*

### 1.8 Evaporative Cooler (External)

| Parameter | Value | Constant |
|-----------|-------|----------|
| Duct penetration X | <!-- BEGIN cdm:EVAP_DUCT_X -->1,000<!-- END cdm:EVAP_DUCT_X -->mm | `EVAP_DUCT_X` |
| Duct penetration Z | <!-- BEGIN cdm:EVAP_DUCT_Z -->1,900<!-- END cdm:EVAP_DUCT_Z -->mm | `EVAP_DUCT_Z` |
| Duct diameter | <!-- BEGIN cdm:EVAP_DUCT_D -->200<!-- END cdm:EVAP_DUCT_D -->mm | `EVAP_DUCT_D` |
| Cooler body W×D×H | 508×254×711mm | `EVAP_W`/`EVAP_D`/`EVAP_H` |
| Stow left edge X | <!-- BEGIN cdm:EVAP_STOW_X -->1,450<!-- END cdm:EVAP_STOW_X -->mm | `EVAP_STOW_X` |
| Inverter mount X / Z | 1910 / 1,180mm | `INVERTER_X`/`INVERTER_Z` |
| Inverter W×H×D | 120×235×72mm | `INVERTER_W`/`INVERTER_H`/`INVERTER_D` |

*Component: **Hessaire MC18M** evaporative cooler (120V AC, <!-- BEGIN fact:evap_cooler_w_ac -->85<!-- END fact:evap_cooler_w_ac -->W, 1,300 CFM run on low, 4.8 gal
reservoir), ground-placed outside on Circuit E. Powered by an **interior 12V→120V pure-sine
inverter (Victron Phoenix 12/375 GFCI)** wall-mounted below the EP; ~<!-- BEGIN fact:evap_cooler_w_bus -->97<!-- END fact:evap_cooler_w_bus -->W on the 12V bus. Cooled
air enters through a Ø200mm insulated flex duct to a wall penetration with light-safe baffle.
AC isolation/GFCI/equipotential-bonding: [Electrical §7.6](electrical-report.md#ac-safety).*

*Reports: [Ventilation & Cooling](ventilation-report.md) §5 (cooler spec + duct + stowage); [Electrical](electrical-report.md) §3/§5.4/§7.6 (Circuit E inverter, power panel AC outlet, AC safety).*

*Diagrams: lighttrap sheet 1 (LT), electrical sheet 1 wiring (ES), floor plan (FP), assembly overview (AO), assembly fabrication (AF).*

### 1.9 Electrical System

| Parameter | Value | Constant |
|-----------|-------|----------|
| Electrical panel left edge X | <!-- BEGIN cdm:EP_X -->1,829<!-- END cdm:EP_X -->mm | `EP_X` |
| Panel width | <!-- BEGIN cdm:EP_W -->300<!-- END cdm:EP_W -->mm | `EP_W` |
| Panel height range | 900–1,500mm | `EP_H_LO`, `EP_H_HI` |
| Battery bank left edge X | <!-- BEGIN cdm:BA_X -->1,829<!-- END cdm:BA_X -->mm | `BA_X` |
| Battery bank width | <!-- BEGIN cdm:BA_W -->260<!-- END cdm:BA_W -->mm | `BA_W` |
| Battery bank height range | 100–600mm | `BA_H_LO`, `BA_H_HI` |

*Components: 3× 200W monocrystalline solar panels (roof-mounted), Victron SmartSolar MPPT 100/50,
1× 100Ah LiFePO4 battery (1,200Wh standard; 2nd pack ghosted = plug-in → 200Ah / 2,400Wh),
Victron Blue Smart IP65 shore charger, NEMA 5-15R weatherproof inlet, Blue Sea 5026 12-circuit
fuse block, IP65 enclosure (300×200×130mm). Battery protection chain: 200A MRBF terminal fuse →
ML-RBS remote contactor → m-Series main disconnect; external emergency E-stop on the power-panel
face trips the contactor (kills all DC from outside). 4 AWG ground wire + 8ft copper stake.*

*Circuits: A — safelight strip (overhead red LED); B — film plane mechanism motors;
C — water pumps P-01–P-05 (P-04 on the pinhole-wall filter skid, others in the IBC corridor); D — safelight vestibule; E — evaporative cooler; F — ventilation fans.*

*Reports: [Electrical](electrical-report.md) §4/§5/§7 (solar array, charge controller + battery + shore charger + external panel, wiring/enclosure/protection); [Electrical Safety](electrical-safety-report.md) §3/§5 (design controls, cascaded improvements).*

*Diagrams: floor plan (FP), line of sight (LOS), assembly overview (AO), assembly fabrication (AF), electrical wiring (ES).*

### 1.10 Pump Manifold (Plumbing Panel)

| Parameter | Value | Constant |
|-----------|-------|----------|
| Left edge X | <!-- BEGIN cdm:PUMP_X -->4,760<!-- END cdm:PUMP_X -->mm | `PUMP_X` |
| Pump-zone width (X, elevation) | <!-- BEGIN cdm:PUMP_W -->114<!-- END cdm:PUMP_W -->mm | `PUMP_W` |
| Height range | 900–1,400mm | `PUMP_H_LO`, `PUMP_H_HI` |
| Depth from pinhole wall | 1,046mm | `PUMP_YD` (= `CORRIDOR_YD_NEAR`) |
| Protrusion from panel | <!-- BEGIN cdm:PUMP_D -->114<!-- END cdm:PUMP_D -->mm | `PUMP_D` |

*Components: 1" PVC header + isolation valves, 4× 12V pumps on plumbing panel (P-01 Blue spray bar supply,
P-02 Brown recycle via filter, P-03 waste evacuation, P-04 tray sump pickup),
two 0.75 L pressure accumulators — ACC-01 (corridor, damps the main filter loop) and ACC-02 (on the filter skid, damps the recycle-spray pump P-02), DN50 butterfly valves V1–V4 (S60×6 thread) at IBC outlets,
manifold ball valves VB1/VB2/VB3, check valves CV1/CV3/CV4 on bulkhead lines X1/X3/X4, X1 fill tee (splits to IBC-1 & IBC-2), Circuit C.
Mounted on 18mm marine ply plumbing panel (near IBC column face), in the IBC plumbing corridor.*

*Reports: [Plumbing](plumbing-report.md) §3.2/§3.3/§4/§7 (corridor pump zone P-01/P-02/P-03/P-05, accumulator ACC-01, valves, panel mounting); [Processing System](water-system-report.md) §7 (equipment layout).*

*Diagrams: floor plan (FP), line of sight (LOS), assembly overview (AO), assembly fabrication (AF), electrical wiring (ES), water system (WS).*

### 1.11 Water System — Blue Circuit

| Parameter | Value | Constant |
|-----------|-------|----------|
| IBC column left edge X | <!-- BEGIN cdm:IBC_COL_X -->4,674<!-- END cdm:IBC_COL_X -->mm | `IBC_COL_X` |
| IBC footprint width | <!-- BEGIN cdm:IBC_W -->1,219<!-- END cdm:IBC_W -->mm | `IBC_W` |
| IBC footprint depth | <!-- BEGIN cdm:IBC_D -->1,016<!-- END cdm:IBC_D -->mm | `IBC_D` |
| Single tote height (1,000L caged) | <!-- BEGIN cdm:IBC_H_1000 -->1,168<!-- END cdm:IBC_H_1000 -->mm | `IBC_H_1000` |
| Stacked height (2× 1,000L, direct-stack) | <!-- BEGIN cdm:IBC_H_STK_1000 -->2,336<!-- END cdm:IBC_H_STK_1000 -->mm | `IBC_H_STK_1000` |
| Near-column front depth from pinhole wall | <!-- BEGIN cdm:BLUE_IBC_Y -->30<!-- END cdm:BLUE_IBC_Y -->mm | `BLUE_IBC_Y` |
| Far-column front depth from pinhole wall | <!-- BEGIN cdm:IBC_FAR_Y -->1,316<!-- END cdm:IBC_FAR_Y -->mm | `IBC_FAR_Y` |

*Components: **4× 1,000L caged composite IBC totes** (1219×1016×1168), **direct-stacked**
cage-on-cage in two columns (near: Brown developer + Blue #1; far: Waste + Blue #2) — Blue-on-top layout
kept. Held by a **restraint DEEP 4-LEG BOX** at the corridor mouth (2×2×0.120in steel SHS front + back upright pairs
450mm apart tied by rings + 50×20×3 front retaining bars in the 25mm tote↔film-rail gap + Simpson wall
joist-hangers + D-ring lashing + 4 floor feet) —
NOT a load-bearing platform; the totes carry their own stack load. 1" PVC Sch-40 blue supply pipe, spray bar
(¾" PVC), Blue fill = gravity **side-entry near the top** (X1, shared T), Brown/Waste drains pumped (X3/X4).
Legacy `IBC_H_600`=1010 / `IBC_H_STK`=2020 constants are the superseded "600L fill-level" values — kept only
for the few generators not yet repointed (overview Blue-trunk shelf, walkway/weight context imports).*

*Reports: [Processing System](water-system-report.md) §3/§4.1 (storage capacity, Blue clean-water supply); [IBC Stacking System](ibc-stacking-report.md) §2/§3 (tote spec/layout, restraint deep 4-leg box); [Plumbing](plumbing-report.md) §6.1 (Blue supply flow path).*

*Diagrams: floor plan (FP), line of sight (LOS), assembly overview (AO), assembly fabrication (AF), water system (WS).*

### 1.12 Water System — Brown Circuit

| Parameter | Value | Constant |
|-----------|-------|----------|
| Brown IBC front depth | <!-- BEGIN cdm:BROWN_IBC_Y -->30<!-- END cdm:BROWN_IBC_Y -->mm | `BROWN_IBC_Y` |
| IBC dimensions | same as Blue | `IBC_W`, `IBC_D`, `IBC_H_600` |

*Components: 1× 1,000L caged composite IBC (Y-stacked behind Blue stack, right end zone),
DN50 butterfly valve (S60×6) + S60×6-to-1" NPT adapter at drain outlet,
3-stage Big Blue filter bank (5μm sediment → KDF-55 → carbon, wall-mounted on the filter skid), Shurflo P-04 (tray drain),
3-way diverter valves 3W-DV-01 and 3W-DV-02, SV-01 pH sample tap.
Filled via side-entry near the top from the P-04 tray-sump pickup pump (no top-cap access — <!-- BEGIN fact:ibc_ceiling_clearance_mm -->52<!-- END fact:ibc_ceiling_clearance_mm -->mm headroom).*

*Reports: [Processing System](water-system-report.md) §4.2 (Brown used-water recycling); [Plumbing](plumbing-report.md) §3.1/§4.2/§4.4/§6.2 (filter skid + P-02, diverter valves, SV-01 pH sample tap, Brown flow path).*

*Diagrams: floor plan (FP), line of sight (LOS), assembly overview (AO), assembly fabrication (AF), water system (WS).*

### 1.13 Water System — Black Circuit (Waste)

| Parameter | Value | Constant |
|-----------|-------|----------|
| Waste IBC front depth | <!-- BEGIN cdm:WASTE_IBC_Y -->1,316<!-- END cdm:WASTE_IBC_Y -->mm | `WASTE_IBC_Y` |
| IBC far column start Y | <!-- BEGIN cdm:IBC_FAR_Y -->1,316<!-- END cdm:IBC_FAR_Y -->mm | `IBC_FAR_Y` |
| Waste IBC color code | Black | `C_WASTE_IBC` |

*Components: 1× 1,000L caged composite IBC tote (4th IBC in 2×2 stack, right end zone),
DN50 butterfly valve (S60×6) + S60×6-to-1" NPT adapter at drain outlet,
2" NPT bulkhead fittings for external drain/fill (X4), reinforcing plates for external ports,
P-03 waste evacuation pump (mounted in IBC plumbing corridor on X4 drain run). Filled via side-entry near the top from the filter reject line (no top-cap access).*

*Reports: [Processing System](water-system-report.md) §4.3 (Black waste containment); [Plumbing](plumbing-report.md) §3.2/§6.3 (P-03 corridor waste pump, Black flow path); [IBC Stacking System](ibc-stacking-report.md) §6 (external bulkhead ports, X4 drain/fill).*

*Diagrams: floor plan (FP), line of sight (LOS), assembly overview (AO), assembly fabrication (AF), water system (WS).*

### 1.14 Equipment Zones

| Parameter | Value | Constant |
|-----------|-------|----------|
| Left end zone boundary (right edge) | X = <!-- BEGIN cdm:ZONE_L_END -->150<!-- END cdm:ZONE_L_END -->mm | `ZONE_L_END` |
| Right end zone boundary (left edge) | X = <!-- BEGIN cdm:ZONE_R_START -->4,649<!-- END cdm:ZONE_R_START -->mm | `ZONE_R_START` |
| Optical cone left at depth Y | `PH_X − (PH_X − FP_X_L) × Y / FP_Y` | `cone_left(y)` |
| Optical cone right at depth Y | `PH_X + (FP_X_R − PH_X) × Y / FP_Y` | `cone_right(y)` |

*Derived rule: any equipment with X < ZONE_L_END is shadow-free at all depths.
Any equipment with X > ZONE_R_START is shadow-free at all depths.
Equipment at pinhole wall face - always shadow-free.
Equipment in the IBC corridor is shadow-free.*

*Reports: [Equipment Layout](equipment-layout-report.md) §1/§2/§3 (shadow-free zone definitions + optical cone, equipment positions, floor-plan & line-of-sight diagrams).*

*Diagrams: floor plan (FP), line of sight (LOS), assembly overview (AO).*

### 1.15 Panel Swing Pivot

| Parameter | Value | Constant |
|-----------|-------|----------|
| Transport swing angle | <!-- BEGIN cdm:SWING_LOCK_DEG -->56<!-- END cdm:SWING_LOCK_DEG -->° | `SWING_LOCK_DEG` |
| Pivot post position | X=175mm, Yd=2,287mm | `PIVOT_X`, `PIVOT_YD` |
| Pivot post | Ø89×8mm CHS (reused film far-left upright) | `PIVOT_POST_OD`, `PIVOT_POST_T` |
| Lock mechanism | top + bottom wall stays (hook + eye + turnbuckle) | — |
| Swung door clearance | +<!-- BEGIN fact:swung_door_clearance_mm -->59<!-- END fact:swung_door_clearance_mm -->mm (true min X, bay front-right corner) | — |

*Components: Ø89×8mm CHS pivot post on a thrust collar + top/bottom hub bearings (Ø220 thrust +
2× Ø90 journal), drum support cage (1.5×1.5×0.120in steel SHS), top + bottom wall stays + 4-bolt wall anchor
plates, 4× drop-in rail saddles + tapered dowels (for the removable left film rails).*

*Reports: [Hinged Light-Trap Panel](hinged-panel-report.md) §5/§8.3 (rotating transport system + locking wall stays, swing-pivot hardware); [Equipment Layout](equipment-layout-report.md) §6.1 (stepped panel & swing pivot, transport mode).*

*Diagrams: container floor plan (FP), assembly overview plan view (AO), hinged panel sheet 4 (HP).*

### 1.16 Processing Tray

| Parameter | Value | Constant |
|-----------|-------|----------|
| Tray left edge X | <!-- BEGIN cdm:PROC_TRAY_X_L -->170<!-- END cdm:PROC_TRAY_X_L -->mm | `PROC_TRAY_X_L` |
| Tray right edge X | <!-- BEGIN cdm:PROC_TRAY_X_R -->4,629<!-- END cdm:PROC_TRAY_X_R -->mm | `PROC_TRAY_X_R` |
| Tray width | <!-- BEGIN cdm:PROC_TRAY_W -->4,459<!-- END cdm:PROC_TRAY_W -->mm | `PROC_TRAY_W` |
| Tray depth | <!-- BEGIN cdm:PROC_TRAY_D -->2,200<!-- END cdm:PROC_TRAY_D -->mm | `PROC_TRAY_D` |
| Tray near edge Yd | <!-- BEGIN cdm:PROC_TRAY_YD_NEAR -->80<!-- END cdm:PROC_TRAY_YD_NEAR -->mm | `PROC_TRAY_YD_NEAR` |
| Tray far edge Yd | <!-- BEGIN cdm:PROC_TRAY_YD_FAR -->2,280<!-- END cdm:PROC_TRAY_YD_FAR -->mm | `PROC_TRAY_YD_FAR` |
| Rim height | <!-- BEGIN cdm:PROC_TRAY_RIM -->50<!-- END cdm:PROC_TRAY_RIM -->mm | `PROC_TRAY_RIM` |
| Dual-axis pitch | 1:200 (<!-- BEGIN cdm:PROC_TRAY_PITCH -->10<!-- END cdm:PROC_TRAY_PITCH -->mm fall) | `PROC_TRAY_PITCH` |
| Sump X | <!-- BEGIN cdm:PROC_TRAY_DRAIN_X -->2,386<!-- END cdm:PROC_TRAY_DRAIN_X -->mm | `PROC_TRAY_DRAIN_X` |
| Sump Yd | <!-- BEGIN cdm:PROC_TRAY_DRAIN_YD -->80<!-- END cdm:PROC_TRAY_DRAIN_YD -->mm | `PROC_TRAY_DRAIN_YD` |
| Sump dimensions | 150 x 100 x 20mm | `PROC_TRAY_SUMP_W/D/Z` |

*Components: 304 SS sheet (16-ga, 1.5mm), 2 panels field-bolted at center flange,
pressed sump well (150x100x20mm), 5x tapered HDPE shim strips (50mm wide, 0-10mm),
1" SS foot valve w/ strainer, 1" reinforced suction hose, silicone gasket strip,
M6x16 SS fasteners. No penetration of tray or container floor.
Permanently installed — no removal for transport mode conversion.*

*Reports: [Processing Tray & Spray Bar](processing-tray-and-spray-bar.md) §2/§6.1 (tray specification, HDPE shim slope, sump well, permanent installation, parts); [Processing System](water-system-report.md) §4.4 (processing tray & spray bar).*

*Diagrams: water system sheets 3-4 (WS), container floor plan (FP), assembly overview (AO), walkway sheet 2 (WK).*

### 1.17 Perimeter Walkway

| Parameter | Value | Constant |
|-----------|-------|----------|
| Walkway width | <!-- BEGIN cdm:WALKWAY_W -->300<!-- END cdm:WALKWAY_W -->mm | `WALKWAY_W` |
| Deck height | <!-- BEGIN cdm:WALKWAY_H -->140<!-- END cdm:WALKWAY_H -->mm | `WALKWAY_H` |
| Grate thickness (all sections) | <!-- BEGIN cdm:WALKWAY_GRATE_T -->25<!-- END cdm:WALKWAY_GRATE_T -->mm | `WALKWAY_GRATE_T` |
| Bracket vertical leg | <!-- BEGIN cdm:WALKWAY_BRACKET_H -->150<!-- END cdm:WALKWAY_BRACKET_H -->mm | `WALKWAY_BRACKET_H` |
| Bracket plate thickness | <!-- BEGIN cdm:WALKWAY_BRACKET_T -->8<!-- END cdm:WALKWAY_BRACKET_T -->mm | `WALKWAY_BRACKET_T` |
| Bracket spacing | <!-- BEGIN cdm:WALKWAY_BRACKET_SPACING -->457<!-- END cdm:WALKWAY_BRACKET_SPACING -->mm | `WALKWAY_BRACKET_SPACING` |
| Container rib spacing | <!-- BEGIN cdm:CONTAINER_RIB_SPACING -->457<!-- END cdm:CONTAINER_RIB_SPACING -->mm | `CONTAINER_RIB_SPACING` |
| Right-walkway L-angle grate bearer | 1×1×3/16in steel angle | prose — [walkway-report §4.4](walkway-report.md); no constant (#26) |
| Near walkway Yd | <!-- BEGIN cdm:WALKWAY_NEAR_YD -->0<!-- END cdm:WALKWAY_NEAR_YD -->mm | `WALKWAY_NEAR_YD` |
| Far walkway Yd | <!-- BEGIN cdm:WALKWAY_FAR_YD -->2,062<!-- END cdm:WALKWAY_FAR_YD -->mm | `WALKWAY_FAR_YD` |
| Left walkway X | <!-- BEGIN cdm:WALKWAY_LEFT_X -->170<!-- END cdm:WALKWAY_LEFT_X -->mm | `WALKWAY_LEFT_X` |
| Left walkway unsupported span | <!-- BEGIN cdm:WALKWAY_LEFT_SPAN -->1,762<!-- END cdm:WALKWAY_LEFT_SPAN -->mm | `WALKWAY_LEFT_SPAN` |
| Right walkway X | <!-- BEGIN cdm:WALKWAY_RIGHT_X -->4,329<!-- END cdm:WALKWAY_RIGHT_X -->mm | `WALKWAY_RIGHT_X` |

*Components: Near/far: 25mm grating on 8mm gusset brackets bolted to corrugated wall ribs.

Right: cantilever rectangle — a closed 2×1×0.120in steel frame (2 long beams at X=4329/4629 +
2 end beams) picked up at mid-span by 2 arms cantilevering off the IBC corridor uprights (half-lapped
where the long beams cross), on wall cleats at the left corners and combined corner plates (shared with
the bottom film rail BR) at the right corners. No floor contact, no roof penetrations — clears IBC stack entirely.

Left: removable lift-out, 25mm grating resting on butt joints (no brackets —
panel conflict, must remove before the panel swings to transport). No floor contact on
any section. 4 removable sections.*

*Reports: [Walkway](walkway-report.md) §3/§4/§5/§8 (near/far wall-cantilevered, right cantilever rectangle, left removable lift-out, grating spec); [Right Walkway Cantilever](right-walkway-cantilever-study.md) §3/§7 (hybrid-anchor design, rev12).*

*Diagrams: walkway sheet 1 cross-section (WK), walkway sheet 2 plan view (WK), container floor plan (FP), hinged panel (HP).*

---

## 2. Script and Diagram Index

Every generator script, its output PNGs, and the subsystems it renders.

| Abbr | Generator script | PNG files produced | Subsystems drawn |
|------|-----------------|-------------------|-----------------|
| **FP** | `generate_floorplan_diagram.py` | `diagrams/container-floorplan.png` | 1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 17 |
| **LOS** | `generate_line_of_sight.py` | `diagrams/line-of-sight.png` | 1, 2, 3, 5, 9, 10, 11, 12, 13, 14 |
| **AO** | `generate_assembly_overview.py` | `diagrams/assembly-overview.png`<br>`diagrams/assembly-overview-fp.png`<br>`diagrams/assembly-overview-plan.png` | 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13 |
| **AF** | `generate_assembly_fabrication.py` | `diagrams/assembly-fab-sheet1.png`<br>`diagrams/assembly-fab-sheet2.png` | 1, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13 |
| **FPM** | `generate_film_plane_mechanism.py` | `diagrams/film-plane-sheet1.png`<br>`diagrams/film-plane-sheet2.png`<br>`diagrams/film-plane-sheet3.png`<br>`diagrams/film-plane-sheet4.png` | 1, 2, 3 |
| **FPD** | `generate_film_plane_distortion.py` | `diagrams/film-plane-distortion-c0.png` – `c5.png`<br>`diagrams/film-plane-distortion-summary.png` | 3 (optical simulation) |
| **ES** | `generate_electrical_diagram.py` | `diagrams/electrical-sheet1.png`<br>`diagrams/electrical-sheet2.png` | 1, 7, 8, 9, 10 |
| **WS** | `generate_water_system.py` | `diagrams/water-system-sheet1.png`<br>`diagrams/water-system-sheet2.png`<br>`diagrams/water-system-sheet3.png`<br>`diagrams/water-system-sheet4.png` | 1, 10, 11, 12, 13, 16 |
| **HP** | `generate_hingepanel_diagram.py` | `diagrams/hingepanel-sheet1.png`<br>`diagrams/hingepanel-sheet2.png`<br>`diagrams/hingepanel-sheet3.png`<br>`diagrams/hingepanel-sheet4.png` | 1, 5, 6, 17 |
| **LT** | `generate_lighttrap_diagram.py` | `diagrams/lighttrap-sheet1.png`<br>`diagrams/lighttrap-sheet2.png` | 1, 5, 6, 7, 8 |
| **TSB** | `generate_tilt_swing_board.py` | `diagrams/tilt-swing-board-sheet1.png`<br>`diagrams/tilt-swing-board-sheet2.png`<br>`diagrams/tilt-swing-board-sheet3.png` | 2, 4 |
| **TSD** | `generate_tilt_swing_distortion.py` | `diagrams/tilt-swing-combined-c0.png` – `c8.png`<br>`diagrams/tilt-swing-combined-summary.png` | 3, 4 (optical simulation) |
| **PD** | `generate_plate_drawing.py` | `diagrams/plate-drawing-sheet1.png`<br>`diagrams/plate-drawing-sheet2.png` | 1, 2 |
| **WK** | `generate_walkway_diagram.py` | `diagrams/walkway-sheet1.png`<br>`diagrams/walkway-sheet2.png`<br>`diagrams/walkway-sheet3.png`<br>`diagrams/walkway-sheet4.png`<br>`diagrams/walkway-sheet5.png`<br>`diagrams/walkway-sheet6.png` | 1, 16, 17 |
| **SC** | `generate_schematic.py`<br>`generate_portrait_viz.py` | `diagrams/portrait-camera-schematic.png`<br>`diagrams/portrait-optimal-3m.png`<br>`diagrams/portrait-scale-comparison.png` | 1, 2 (optical visualization) |

> **FPM / FPD — rigid-plane slide-and-clamp corners:** the film-plane mechanism sheets and optical-distortion renders show the **fixed-size rigid plane on slide-and-clamp corners** — **axis tilt/swing** about the plane center (foreshortening, not growth), tilt ±40° / swing ±28°, single rigid ACM backing, a 304 flat-bar Z/X cross-slide at each corner, and a single-axis envelope (FPD C0–C5). `generate_film_plane_mechanism.py` uses `rigid_corners3d`/`tilt_edge`/`swing_edge` (asin, not atan) and reads `MAX_TILT_DEG`/`MAX_SWING_DEG` from `tbs_constants.py`. Consistent with `film-plane-mechanism-report.md`, `master-shopping-list.md`, `project-cost-breakdown.md`, and `models/film-plane-mechanism.skp`.

---

## 3. Dependency Matrix

✓ = this subsystem is drawn in this diagram group. Re-run all ✓ scripts when the subsystem changes.

| Subsystem | FP | LOS | AO | AF | FPM | FPD | ES | WS | HP | LT | TSB | TSD | PD | SC | WK |
|-----------|:--:|:---:|:--:|:--:|:---:|:---:|:--:|:--:|:--:|:--:|:---:|:---:|:--:|:--:|:--:|
| **1** Container | ✓ | ✓ | ✓ | ✓ | ✓ | | ✓ | ✓ | ✓ | ✓ | | | ✓ | ✓ | ✓ |
| **2** Optical Aperture | ✓ | ✓ | ✓ | ✓ | ✓ | | | | | | ✓ | | ✓ | ✓ | |
| **3** Film Plane Mech | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | | | | | ✓ | | | |
| **4** Tilt-Swing Board | | | | | | | | | | | ✓ | ✓ | | | |
| **5** Light Trap Drum | ✓ | ✓ | ✓ | ✓ | | | | | ✓ | ✓ | | | | | |
| **6** Hinged Panel | | | ✓ | ✓ | | | | | ✓ | ✓ | | | | | |
| **7** Ventilation | ✓ | | ✓ | | | | ✓ | | | ✓ | | | | | |
| **8** Evap Cooler | ✓ | | ✓ | ✓ | | | ✓ | | | ✓ | | | | | |
| **9** Electrical | ✓ | ✓ | ✓ | ✓ | | | ✓ | | | | | | | | |
| **10** Pump Manifold | ✓ | ✓ | ✓ | ✓ | | | ✓ | ✓ | | | | | | | |
| **11** Blue Water (IBCs) | ✓ | ✓ | ✓ | ✓ | | | | ✓ | | | | | | | |
| **12** Brown Water (IBC) | ✓ | ✓ | ✓ | ✓ | | | | ✓ | | | | | | | |
| **13** Black Water (waste IBC) | ✓ | ✓ | ✓ | ✓ | | | | ✓ | | | | | | | |
| **14** Zones / Layout | ✓ | ✓ | ✓ | | | | | | | | | | | | |
| **15** Panel Swing Pivot | ✓ | | ✓ | | | | | | ✓ | | | | | | |
| **16** Processing Tray | ✓ | | ✓ | | | | | ✓ | | | | | | | ✓ |
| **17** Perimeter Walkway | ✓ | | | | | | | | ✓ | | | | | | ✓ |

---

## 3.1 SketchUp 3D models

Each subsystem is also built in the SketchUp 3D model(s). When a subsystem's
constants change, **re-run the model(s) that contain it** (in addition to the 2D
scripts) so the 3D models stay in sync with the drawings — see the Workflow below.

| Model | Script | Output | Subsystems contained |
|---|---|---|---|
| **overview** | `src/models/generate_sketchup_model.py` | `models/overview.skp` + `src/models/overview.rb` | **1–18 (all)** — built as 25 tagged components (incl. lighting/wiring, spray-bar plumbing, fans, water hookups, the **ground solar array** (`solar_array()` + `tilted_slab()` — shared with the electrical model on a `Solar Array` tag), the `Combined Plate` tag). Its `spray_bar()` **reuses the spray-bar model's builders** (`generate_spraybar_model.build_beam/build_carriages/build_feed_pole`), and `light_trap_drum()` + `light_trap_frame()` **reuse the light-trap model's `lt.drum()` + `lt.door_frame()`** (the door frame + top/bottom seal lips that block light) — so all stay in sync; rebuild overview whenever the spray-bar **or** light-trap model changes. Its `walkways()` includes the wall-cantilevered **gusset brackets** (`walkway_brackets()`: near & far long walls at 457mm rib centers — standard 8mm/150mm-leg/300mm-arm with 3× M12, the five widened EP/battery-zone brackets 10mm/200mm-leg/500mm-arm with 4× M12, per Sheet 7) that carry the near/far decks, AND the **left floor-leg cantilever brackets** (foot + 2×2 post + arm to X470, 3 extended to X770 on the punch-out), added by **reusing the walkway model's shared `left_floor_cantilevers()`** (lazy import) so the support design can't drift between the two models. **NB:** `walkway_brackets()` is still a parallel copy of the walkway model's `_cantilever_parts()` — keep the two in sync (see [[project-walkway-bracket-duplication]]). **NB2:** `electrical()` now draws the **EP enclosure internals** (ghosted IP65 shell + MPPT + Blue Sea 5026 fuse stack A–G + +/− busbars + m-Series disconnect + disconnect→busbar link) as a **parallel copy of the electrical model's `power_core()`** — keep the two in sync. The **BR film-plane rail anchor** (combined corner plate, shared with the walkway right beam) is drawn ONCE on its own **`Combined Plate`** tag (`fp_combined_corner_plates()`) and included in BOTH the **Film Plane & Pinhole** and **Walkways** scenes — so it reads with either subsystem without duplicating/z-fighting; in the overview `walkways()` calls `right_walkway_cantilever(include_combined=False)` to omit it there, while walkway.skp keeps it inline. **Scenes:** Overview (all, labels off) + **Labeled** — same view with in-model `add_text` callouts on the major system components (`overview_labels()`: 10 anchored to each instance's bounds top-center + 6 **point-anchored** via `OVERVIEW_POINT_LABELS` for items not a single instance — **SOLAR ARRAY** (exterior), **FAN A** (IBC end), **FAN B** (door end) [the two live in one "Fans A & B" component spanning both ends], the **BATTERY BANK** [inside the Electrical component], and the **CCT-E INVERTER**; on a `Labels` tag shown only in this scene; see [[feedback-3d-model-labels]]). The leader format is `(Δx,Δy,Δz)` mm so wall-mounted callouts (pinhole, spray bar) pull OUT toward the viewer clear of the container — keep Δz modest so the label isn't clipped past the geometry-framed camera. Plus 6 grouped subsystem scenes (labels off). |
| **spray-bar** | `src/models/generate_spraybar_model.py` | `models/spraybar.skp` + `src/models/spraybar.rb` | Spray-bar gantry detail — beam (**spans the full tray width, `PROC_TRAY_X±30`, matching the 2D `generate_spray_bar_diagram.py`; bugfix 2026-06-06 — the 3D beam had used the narrower `PROC_OPEN_X` print zone**) + side-mounted ¾" LDPE manifold + 39 90° down-jet nozzles (100mm pitch, in the open zone), wheel carriages (2 wheels/carriage, curved saddle axle clamps, top/bottom beam clamp plates), feed pole + ball joint with a **single center feed** into the side manifold, **processing tray** (floor + rim + sump). The two carriages are on their own **Carriage L / Carriage R** tags, and the small tray-floor reference patch is on its own **Tray Ref** tag (shown only in the carriage-only scenes — the Combined / Processing-Tray scenes have the real tray, so the ref patch no longer doubles up under the beam). **7 scenes:** Beam, Carriage Assembly, **One Carriage** (Carriage L only — no beam/tray, with a perpendicular close-up camera — `cdir`/standoff, not zoom_extents), Pole & Ball Joint, Processing Tray, Combined, **Labeled** (`spraybar_labels()` — `add_text` callouts; beam/carriage/nozzles/pole/manifold point-anchored; see [[feedback-3d-model-labels]]). The scene loop takes an optional `[x,y,z,standoff]` close-up target. **NB: avoid `"` in label text** — an unescaped quote closes the emitted Ruby string and silently corrupts the whole rebuild (hangs the send). Reads `SPRAY_BAR_*` and `PROC_TRAY_*` constants. |
| **ibc-stack** | `src/models/generate_ibc_model.py` | `models/ibc-stack.skp` + `src/models/ibc-stack.rb` | **v2 (`ibc-reconfig-v2`) — REBUILT 2026-06-14:** this is **THE canonical IBC 3D model** (the Sketchfab embed in `ibc-stacking-report.md`). Because it reuses the `ov` builders it now carries the full v2 design — `cp.frame()` = restraint DEEP 4-LEG BOX + exterior wall backing plates (was `ov.ibc_rack()`, a single front portal; before that a load-bearing platform), `ov.equipment_panel()` pulled **forward** to the corridor mouth (film-safe, X>4649), and `ov.water_plumbing()` = Blue **side-entry** fill + the full recycle loop (sump→IBC-3, filter→IBC-2, reject→IBC-4, all side-entry near the top) + pumped X3/X4 drains. Re-sent + **`.skp` saved 2026-06-14** (the `ibc_labels()` panel-equipment anchors were moved forward to X≈4814–4854 to track the panel; Sketchfab re-upload is the manual step). IBC tote stacking arrangement at the IBC end. Reuses Overview builders: `ov.ibc_stack()` (4× 1,000L totes), `cp.frame()` (v2 restraint deep 4-leg box), `ov.equipment_panel()` (pump/filter), `ov.water_plumbing()`, `ov.water_hookups()` (exterior wall). Container is a low-alpha ghost. 5 tags (Context / IBC Tanks / IBC Frame / Plumbing & Panel / **Walkway Cantilever**) + a `Labels` tag. The **Walkway Cantilever** component (`ov.ibc_cantilever_arms()` — the 2 right-walkway support arms + upright clamps + M12 bolts that attach to the corridor uprights, rev12; single-sourced with the overview/walkway models). **5 scenes:** IBC Tanks, **IBC Frame** (the frame + the attached walkway cantilever arms — the `Walkway Cantilever` tag rides in this scene), Plumbing & Panel, Combined, **Labeled** (`ibc_labels()` — `add_text` callouts on the `Labels` tag, shown only in this scene; 19 callouts split by side. **Container/front side:** the near-column totes (BROWN developer + BLUE #1), the **SUMP PICKUP** riser, the **TO SPRAY BAR** Blue feed, **IBC FRAME**, and the **wet-end panel equipment** pulled out the front laid out as the panel reads — two pump columns (left ACC-01/P-04/P-01, right P-05/P-03/P-02) + three filters F1/F2/F3 below (pumps/filters/accumulator only, no pipes/valves). **Sealed-end side** (right-hand column): the far-column totes (WASTE + BLUE #2) plus the exterior bulkhead ports **X1** (fresh fill), **X3** (Brown drain-out), **X4** (Waste drain-out). Per the project rule every .skp gets a Labeled scene — see [[feedback-3d-model-labels]]). Rebuild whenever those `ov` builders or the IBC/plumbing constants change. |
| **walkway** | `src/models/generate_walkway_model.py` | `models/walkway.skp` + `src/models/walkway.rb` | Processing-tray **perimeter walkway + how it's held up**, separated so the structure reads apart from the decks. 6 tagged components: **Walkways** (near + widened + far + left removable decks + drum-exit punch-out + the **right walkway grate** — `ov.right_walkway_grate()`, moved onto this tag so the Right Cantilever scene reads as bare structure); **Right Cantilever** (the IBC-end cantilever rectangle — `ov.right_walkway_cantilever(include_grate=False)`: closed 2×1×0.120in steel frame (2 long + 2 end beams) + 2 center arms off the IBC corridor uprights (half-lapped at the long beams) + wall cleats at the left corners + combined corner plates at the right corners shared with the bottom film rail BR (`ov.fp_combined_corner_plate`), with a ghost of the IBC uprights + BR rail for context — the GRATE is on the Walkways tag, not here); **Cantilevers** (near/far wall-cantilevered gusset brackets carrying the near/far decks, with the **exterior** detail — reinforcing plate + through-bolts, hex heads outside; standard brackets 8mm/150mm-leg/300mm-arm with **3× M12** triangular, the five widened EP/battery-zone brackets (near, X 1155–2983) 10mm/200mm-leg/500mm-arm with **4× M12** rectangular — matching Sheet 7); **Left Support** (removable lift-out grate on **5 floor-leg cantilever brackets** bolted to bare floor outside the tray — foot + 2×2 post + arm Z75–115 to X470, 3 extended to X770 on the punch-out, passing 15mm over the spray bar; enabled by the +50mm walkway raise); **Processing Tray** (reuses `ov.processing_tray()`); plus a **Cantilever Types** tag/component — ONE of each unique wall-support bracket built side-by-side on the near wall by `cantilever_types()`: STANDARD + WIDENED cantilevers (reuse the extracted `_cantilever_parts()` helper that also builds the in-situ `cantilevers()`) and the **FLOOR-LEG CANTILEVER** (`_floor_cant_type_parts()`, the same bracket `left_support()` builds — the left removable walkway's support, **rev 2026-06-07**: a foot plate + 2×2×0.120in steel SHS post on bare floor outside the tray + an arm (Z75–115, 40mm deep) reaching the grate inner edge X470, extended to X770 on the 3 punch-out brackets, passing 15mm over the floor-level spray bar — enabled by the +50mm walkway raise. Geometry from `LEFT_WK_CANT_*` constants; matches 2D walkway Sheet 6 / Detail D). **PLUS the rev12 right-walkway support brackets** (catalog stations X6000/7000/8000): the **WALL CLEAT** (`ov._rwk_wall_cleat`, left corners), the **COMBINED CORNER PLATE** (`ov.fp_combined_corner_plate` with a `cx` override, right corners — shared with the BR film rail), and the **CENTER CANTILEVER ARM** (`_rwk_arm_type_parts`, off an IBC corridor upright). Shown only in the Cantilevers scene. Container is a low-alpha ghost so the exterior braces + bolt-throughs show. **7 scenes:** **Combined**, **Labeled** (`walkway_labels()` — `add_text` callouts on a `Labels` tag, decks/cantilevers/support point-anchored since they're paired/perimeter; camera pulls back `zoom(0.72)`; see [[feedback-3d-model-labels]]), **Walkway** (all decks), **Near/Far Cantilevers** (the brackets in situ), **Right Cantilever** (only the right walkway support — near/far/left `Walkways` tag off), **Left Support**, and **Cantilevers** (one of each unique bracket type isolated with the wall hidden + a per-scene close-up camera + type-spec callouts on the `Cantilever Types` tag, ordered left→right: the left removable walkway's **floor-leg cantilever** (2×2 post on bare floor + arm Z75–115 to X470, extended to X770 on the punch-out), the **standard** cantilever (8mm/150/300/3×M12), the **widened** cantilever (10mm/200/500/4×M12), and the three rev12 **right-walkway brackets** — wall cleat, combined corner plate, center cantilever arm — with the camera re-centered + pulled back to frame the full row). Reads `WALKWAY_*`, `PROC_TRAY_*`, `LEFT_WK_*`. The floor-leg cantilever design (rev 2026-06-07, with the +50mm walkway raise + panel/drum + film-plane-bottom raise) is fully propagated to both 3D models (re-sent), the 2D `generate_walkway_diagram.py` (Sheets 1/4/5/6/9), master-shopping-list, and project-cost-breakdown. |
| **film-plane-mechanism** | `src/models/generate_film_plane_mechanism_model.py` | `models/film-plane-mechanism.skp` + `src/models/film-plane-mechanism.rb` | The **built single-corner mechanism in fabrication detail** (renamed from `corner-gimbal` 2026-07; Sketchfab UID 572b4aaa…). One corner's full load path: 6061 angle frame → **304 SS corner plate** → **Belden UJ-SS750x375 U-joint** (input stub clamped to the X/swing slide by a **McMaster 4040N12 304 shaft support**; output stub to the plate by a countersunk cap screw) → **304 flat-bar X (swing) + Z (tilt) slides** → **acetal 4-wheel skate** (Ø32 wheels) → **6061-Al U-channel rail**. Both rail pairs (bottom 3×1.5 web-vertical (weight), top 3×1.5 flat for guide); left rail = **transport drop-in** (stub + welded bridge ON TOP + flush locating pin + bottom support bridge + pinhole gusset), right = flanged wall-to-wall. Top rail dropped 44mm (local `PZ_HB_TOP`) for 25mm ceiling clearance; corner plate raised to 25mm walkway clearance. Reads `tbs_constants` geometry (`C_HGT`, `RAIL_OFF_BOT`, `CD/CW_*`). **3D detail companion to 2D Sheets 3/4/5/8/9** — this is now the SOLE dedicated film-plane 3D model (the older whole-plane `film-plane.skp` was retired 2026-07-20; `overview.skp` still carries the film-plane geometry inline at container scale). Scenes with per-part `add_text` labels. |
| **lighttrap** | `src/models/generate_lighttrap_model.py` | `models/lighttrap.skp` + `src/models/lighttrap.rb` | **Single interactive cargo-door-end model** (rev10 — the cargo panel + drum SWING 56° about a vertical Ø89 CHS pivot post; consolidates the former separate operating + transport models into one .skp via Dynamic Components). **Static parts:** ghosted container stub (ends at the door plane X=0 so the bay/drum/doors read as protruding beyond it), fixed RHS **door frame** (`door_frame()` + housing-surround EPDM), the **fixed pivot axle** (`axle()` — Ø89 CHS post + thrust collar + Ø220 thrust / Ø120 journal bearings), the two **FIXED panel strips** (`near_leaf()` Yd0–180 + `far_leaf()` at the pivot, each with perimeter EPDM + the vertical cut seal), the **removable left film-plane rails** on drop-in **saddles** (`_rail_saddle()`), **wall anchors** + stay eyes (`wall_anchors()`), and partial **processing tray**. **Two Dynamic Components** (click with SketchUp's Interact tool): **(1) Panel Swing** — the swinging assembly (the swinging center+corner panel leaves + `pivot_link()` hub + 4 Southco latches, B2 **punch-out bay** `bay()` offsetting the drum to X=−400, the **housed revolving-door light lock** Ø900 housing + C-shell drum [the rotor is **baked static** as `drum_rotor()` so the nested DC doesn't reset] + seals + grab rail, **Fan B**, the **drum support cage** `drum_frame()`, the stay hooks `frame_hooks()`, **plus a nested "Lift-out Walkways" child** — `liftout_walkways()` builds the amber removable left walkway + drum-exit punch-out + near door-end band at world coords, carrying `_hidden_formula = "PanelSwing!swing>0.5"` so the lift-out decks **disappear once the panel swings past half-open** (lifted out for transport) and reappear when closed; these were moved out of the static `context()`/`walkways_partial()` so they draw once) animates **RotZ 0↔56°** about the pivot (operating↔transport); **(2) Cargo Doors** — a parent DC whose `shut` attribute drives two leaf children's `RotZ` (`door_leaf_local()`), swinging both ISO leaves 0↔±180° (closed↔open). Fan B **reuses the Overview's shared `fan_duct()`**, and its **flexible connector** is shown: a **static** wall box (`fan_b_box()`, Cct B termination — stays put when the panel swings) plus an orange **curly coil cable** (`fan_b_cable()` → `ov.ruby_coil_cord`) that lives in a **third child DC ("Fan B Cable")** carrying `_hidden_formula = "PanelSwing!swing>0.5"`, so the coil is **shown only when the door is closed** (plugged box→fan) and **hides when the panel swings open** (unplugged for transport) — same soft-cord convention as the overview/electrical models. Reads `DRUM_*`, `PANEL_*`, `FAN_B_*`, `BAY_*`, `PIVOT_X`/`PIVOT_YD`, `SWING_LOCK_DEG`, `PANEL_CUT_YD`. **Requires the Dynamic Components extension** for the click behavior — it does **not** carry to Sketchfab web embeds (those render a static pose). Static parts + 2 DCs, **2 scenes**: the interactive swing scene + a **Labeled** scene (`lighttrap_labels()` / `LIGHTTRAP_LABELS` + `LIGHTTRAP_POINT_LABELS` — `add_text` callouts on a `Labels` tag, drum/Fan B point-anchored since they're nested in the Panel Swing DC; the camera pulls back `zoom(0.62)` so callouts have margin). Per the project rule, every new .skp gets a Labeled scene — see [[feedback-3d-model-labels]]. **Rebuild whenever those constants or the shared builders change.** |

| **electrical** | `src/models/generate_electrical_model.py` | `models/electrical.skp` + `src/models/electrical.rb` | **Power-system focused model** (the missing subsystem) — solar generation → storage → distribution → loads. A **ghosted IP65 enclosure with distinct internals** (`power_core()`: MPPT 100/50, Blue Sea 5026 fuse block, +/− busbars, m-Series rotary main disconnect) — this internals geometry is now **DUPLICATED into the overview's `ov.electrical()`** (keep the two in sync; the overview omits the battery main cables + circuit routing this model adds), the **battery** (`battery()`: 100Ah pack + ghosted 2nd + ML-RBS contactor + MRBF main fuse), the **external power panel** (`external_panel()`: MC4 PV ×3, NEMA shore inlet, **GFCI cooler outlet**, exterior E-stop), the **Circuit-E inverter** (`inverter()`, reuses `INVERTER_*`), the **ground solar array** (reuses **`ov.solar_array()`** + `ov.tilted_slab()` — 3×200W on a 30° tilt frame, exterior/door-end clear of the pinhole sightline, + PV run to the panel; now shared with the overview), and **`circuit_runs()`** — the 40×25 ceiling trunking spine + **7 color-coded circuits A–G** routed fuse-block→trunking→each load. `context()` is a full-length ghost container + faint ghost loads (Fan A/B, pump cluster, 3× LED, 3× safelight) that anchor the circuit runs. Reuses `ov` helpers (`ruby_box`/`ruby_cylinder`/`ruby_pipe_run`/**`ruby_coil_cord`**/`component`/`mm`/`hex_to_rgb`/`shared_mat_name`/colors) + the scene/camera/send scaffold. **Soft-vs-hard convention:** rigid conduit/wiring uses `ruby_pipe_run` (smooth orthogonal tube + elbows); FLEXIBLE connectors use the shared **`ruby_coil_cord`** helper (thin helical "curly cord", color still encodes the circuit) — applied to the PV lead (array→panel, via `ov.solar_array`), the Cct-E cooler cord, and the Fan B box→fan jumper in BOTH models; keep the two in sync. 8 tags (Context / Solar Array / Power Core / Battery / External Panel / Inverter / Circuit Runs / **Labels**). **5 scenes:** Combined, **Power Core** (enclosure internals + battery, per-scene zoom camera), **Distribution** (circuit runs + core + battery), **External Panel** (panel + solar, per-scene zoom), **Labeled** (`elec_labels()` — point-anchored `add_text` callouts on the Labels tag; see [[feedback-3d-model-labels]]). Reads `EP_*`, `BA_*`, `PWR_PANEL_*`, `INVERTER_*`, the new `SOLAR_*` + enclosure-internals constants (`ENCL_SHELL_D`/`MPPT_*`/`FUSEBLK_*`/`BUSBAR_*`/`DISCONNECT_*`/`CONTACTOR_*`/`MRBF_*`), and load positions (`FAN_A_*`/`FAN_B_*`/`EQPANEL_X`). Rebuild whenever those constants change. 3D companion to the 2D `generate_electrical_diagram.py` (Sheet 6 is the external power panel, folded in from the retired `generate_power_panel_diagram.py`). |

| **construction** | `src/models/generate_construction_model.py` | `models/construction.skp` + `src/models/construction.rb` | **Phased BUILD-ORDER validation model** (Sketchfab UID `dcc54fb3d02e46c3ab070dd49adc5d1e`; the embed in [construction-report.md](construction-report.md) §9). REUSES the Overview + panel + walkway builders (`ov`/`cp`/`pw`/`wm`/`em`) staged by install order — a single `STEPS` list (phase, step-id, tag, label, body-thunk) drives everything; a scene per phase shows the model built up cumulatively through that phase. **Four phases are click-to-build Dynamic Components** (`DC_PHASES = 1,3,4,5`; Phase 2 = re-measure, no geometry). With the Interact tool each phase scene opens showing only its **first (minimal) step**, with every prior phase drawn as an inert **ghosted static copy** (`P{n}-static` tags, `onclick=nil`); each click reveals the next sub-step in order. Prior-phase context is ghosted via `ov.muted(mute, alpha, force=True)` — the `force` mode makes the context's mute/alpha WIN over builders that hardcode their own (e.g. `ibc_stack(alpha=0.85)`), and `mute_hex` collapses ALL ghost colors to one `GHOST_HEX` gray so the faded context shares essentially ONE material (keeps the model under Sketchfab's ~100-material cap — full per-part ghosts blew it to 144). **Per-step granularity comes from builder splits that all default to byte-identical output, so overview.skp + water are untouched:** `ibc_stack(cols=near/far)`, `fans(which=A/B)`, `fan_wiring(which=A/B, a_to_ep=)`, `walkway_brackets(which=near/far)`, `film_plane_mechanism(part=beams/plane)`, `cp.frame(part=posts/rails)`, `cp.plumbing(part=corridor/sump)`, `pw.kit(part=skid/recycle/waste/brown_ribbon)`, `pw.panel_power(include_switch=, part=corridor/ep_link)`, `em.external_panel(include_estop=, include_disconnect=)` + `external_estop()`/`pv_disconnect()`. These splits encode the build order — cross-corridor lines (blue recycle, grey waste, brown-suction ribbon) and the purple Cct-C wiring + Fan A's Cct-A cable are **pre-run to the pinhole wall / EP drop in Phase 1**, connected in their later phases. The model builds **every Overview component EXCEPT four deliberate omissions** that would only obstruct the build view: the **container shell** (floor-only context, for orbit access), the **optical cone** (non-physical guidance geometry), the **solar array**, and the **evap cooler**. **Requires the Dynamic Components extension** for click behavior (Sketchfab web embeds render a static pose). Rebuild whenever any reused builder, the `STEPS` list, or the install order changes. Operational note: verifying a DC by setting its `step` via `eval_ruby` mutates the live model — always `--send` clean afterward (see [[reference_dc_step_walking_pollutes_live_model]]). |

*As more models are added, list them here with the subsystems each contains, so a
constants change re-runs only the affected models.*

---

## 4. Change Propagation Guide

When a constant in `tbs_constants.py` changes, re-run every script that reads it
**and re-run any SketchUp model that contains the affected subsystem**, then commit
the updated PNGs and `*.skp`/`*.rb` alongside the constant change.

> **This used to be a hand-maintained `constant → scripts` table — it is now COMPUTED, so it
> can't drift.** The machine source is **`dependencies.yml`** (the validated `script → output-file`
> graph; `deps.py` loads it, `lint.py` validates it). To see what a given constant change cascades to:
>
> ```bash
> python3 src/generators/lint.py --cascade <CONSTANT_NAME>   # e.g. PROC_TRAY_X_R
> ```
>
> It greps every script that reads the constant and lists the exact PNGs / `.skp` / `.rb` each writes.
> And the **pre-commit linter enforces it**: stage a `tbs_constants.py` change without the regenerated
> outputs and the *missing-cascade* check names the specific files you still need to regenerate + stage
> (see `drift-reduction-plan.md`). So you no longer read a table to find the cascade — the tooling computes it.

### Workflow

```
1. Edit tbs_constants.py
2. python3 tbs_constants.py          # verify no errors, check derived values in summary
2b. python3 src/generators/lint.py --cascade <CONSTANT>   # lists the exact scripts + outputs to re-run
3. python3 generate_<affected>.py    # for each affected 2D script the cascade named
4. Re-run affected SketchUp model(s) (§3.1):
     python3 src/models/generate_sketchup_model.py --save --send
   # regenerates overview.rb + re-sends to SketchUp; save the .skp
5. Visually inspect updated PNGs in diagrams/ AND the SketchUp model
6. bash publish.sh --build           # verify zero MkDocs warnings
7. git add tbs_constants.py diagrams/*.png models/*.skp src/models/overview.rb && git commit -m "..."
8. bash publish.sh                   # deploy
```
