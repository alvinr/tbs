<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Component Dependency Map

This document is the operational guide for maintaining consistency across all TBS-001 engineering
diagrams. When any component changes — position, dimension, or specification — consult:

1. **Section 1** to find the controlling constant in `tbs_constants.py`
2. **Section 2** to find which generator scripts use that constant
3. **Section 3** to confirm the exact scripts to re-run and PNGs to regenerate

All shared constants live in `tbs_constants.py`. Change a value there once; re-run the affected
scripts; all diagrams update consistently.

---

## 1. Component Registry

Each subsystem lists its key physical parameters and the `tbs_constants.py` variable(s) that
control it. Scripts should import from `tbs_constants` rather than hardcoding these values.

### 1.1 Container Structure

| Parameter | Value | Constant |
|-----------|-------|----------|
| Interior length (long axis X) | 5893mm | `C_LEN` |
| Interior width (optical depth Y) | 2362mm | `C_WID` |
| Interior height Z | 2388mm | `C_HGT` |

*Components: corrugated steel long walls, short end walls (cargo door end / far end), roof,
bamboo floor, corner castings, corner posts, structural corrugation ribs.*

### 1.2 Optical Aperture

| Parameter | Value | Constant |
|-----------|-------|----------|
| Pinhole X position (long axis) | 2399mm | `PH_X` |
| Pinhole center height | 1194mm | `PH_H` |
| Pinhole diameter | Ø2.17mm | `PH_D` |
| f-number | f/1088 | `PH_FNO` |
| Focal length | 2362mm | `PH_F` (= `C_WID`) |

*Components: wall frame (600×600mm, 6mm steel), pinhole plate (ICP-02 / interchangeable
Ø50mm SS-302 disc, 0.1mm, Lenox Laser laser-drilled), lens plate, shutter plate and channel.*

### 1.3 Film Plane Mechanism

| Parameter | Value | Constant |
|-----------|-------|----------|
| Film plane left edge X | 150mm | `FP_X_L` |
| Film plane right edge X | 4649mm | `FP_X_R` |
| Film plane width | 4499mm | `FP_W` |
| Film plane height | 2388mm | `FP_H` |
| Nominal depth from pinhole wall | 2262mm | `FP_Y` |
| Minimum carriage depth | 100mm | `FP_Y_MIN` |
| Left rail X | 150mm | `RAIL_X_L` |
| Right rail X | 4649mm | `RAIL_X_R` |
| Rail span | 4499mm | `RAIL_SPAN` |
| Rail length (Y travel) | 2200mm | `RAIL_LEN` |
| Max tilt (single-axis, Option A) | ±40° | `MAX_TILT_DEG` |
| Max swing (single-axis, Option A) | ±28° | `MAX_SWING_DEG` |
| Cross-slide Z travel (tilt) | ~280mm | `XSLIDE_Z_TRAVEL` |
| Cross-slide X travel (swing) | ~263mm | `XSLIDE_X_TRAVEL` |
| Cross-slide stroke (spec) | 300mm | `XSLIDE_STROKE` |
| Cross-slides total (2/corner) | 8 | `XSLIDE_N` |

*Components (**Option A** — a fixed-size rigid plane on floating-corner cross-slides; rev7,
2026-06-06): welded aluminum angle frame (2"×2"×3/16"), 4× HGR20 depth rails (ceiling + floor),
8× HGH20CA carriage blocks, 4× ¾"-6 Acme leadscrews, 4× bronze nuts, 4× 8" handwheels,
**8× HGR15 cross-slide rails + 8× HGH15CA blocks + 4× intermediate plates** (the 2-axis X-Z corner
stage that absorbs the rigid-rotation arc travel), 8× GIR25-DO rod-end spherical bearings,
**single rigid ACM backing panel** (the old folding two-panel piano-hinge system removed),
Duvetyne curtain seals, rail felt light-trap strips, 92× cam-lever spring clamps at 150mm centers
(muslin attachment). The plane stays a fixed-size flat rectangle — it no longer stretches/twists,
so the old ±42°/±25.7° stretch-mechanism stops and the compound-twist config are dropped.*

### 1.4 Tilt-Swing Front Board

| Parameter | Value | Constant |
|-----------|-------|----------|
| Pinhole X (board centers here) | 2399mm | `PH_X` |
| Max tilt/swing | ±5.3° | — (hardcoded in script) |
| Resolution | 0.012°/click | — (hardcoded in script) |

*Components: ICP-01 outer adapter frame (600×600×40mm Al 6061-T6), ICP-02 inner carrier plate
(Ø320×25mm Al 6061-T6), GE50-DO-2RS spherical plain bearing (SKF, PTFE-lined), 4× M8×1.0
adjustment screws, hemispherical ball-socket inserts, 36-detent knurled knobs, ICP-10 neoprene
bellows (4-pleat, Ø290 ID → Ø360 OD).*

### 1.5 Housed Revolving-Door Light Lock (rev 8)

| Parameter | Value | Constant |
|-----------|-------|----------|
| Light-lock center X (cargo door end wall) | 0mm | `DRUM_CX` |
| Fixed housing outer diameter | 900mm | `DRUM_D` |
| Housing radius | 450mm | `DRUM_R` / `LT_HOUSING_R` |
| Drum outer radius (rotating) | 432mm | `LT_DRUM_OR` |
| Opening arc (each) | 80° | `LT_OPENING_DEG` |
| Height | 2200mm | `DRUM_H_LT` |

*Components: fixed Ø900 aluminum housing with two 80° openings (exterior + interior-onto-walkway,
180° apart); single-opening C-shell rotating drum (Ø864, ~Ø850 bore, NO internal fins) — light-tight
by geometry; 5mm top/bottom caps, 75mm stub shafts (×2), 2× SKF 6215-2RS1 sealed bearings, drum↔housing
felt/brush wiper seals (opening edges + top/bottom rings), 100mm SS interior grab rail, housing-to-panel
neoprene compression strip. Replaces the failed Ø750 4-fin drum.*

### 1.6 Hinged Cargo-Door Panel

| Parameter | Value | Constant |
|-----------|-------|----------|
| Panel width | 2362mm | `C_WID` |
| Panel height | 2388mm | `C_HGT` |
| Panel thickness | 120mm | — (hardcoded in scripts) |

*Components: 50×50mm RHS steel frame, 18mm plywood skins (both faces), 20mm EPDM compression
gasket in machined channel, 3× heavy-duty weld-on barrel hinges (rev 9 / B2 — structural
sign-off) + free-edge swing-support caster, 4× Southco C2-33 cam compression latches,
Ø900mm housed revolving-door light-lock aperture in the B2 punch-out bay.*

### 1.7 Ventilation System

| Parameter | Value | Constant |
|-----------|-------|----------|
| Fan diameter (both fans) | 150mm | `FAN_DIAM` |
| Panel fan body depth | 50mm | `FAN_BODY_D` |
| Fan A center height AFF (high, above IBC) | 2200mm | `FAN_A_H` |
| Fan B center height AFF (low) | 600mm | `FAN_B_H` |
| Fan A Yd position (far side, off corner — rev9/B2 swap) | 1996mm | `FAN_A_YD` |
| Fan B Yd position (near pinhole wall, near corner — rev9/B2 swap) | 365mm | `FAN_B_YD` |
| Baffle duct depth | 300mm | `DUCT_DEPTH` |
| Baffle duct height | 200mm | `DUCT_HEIGHT` |
| Fan A shadow margin (from cone) | 869mm | `FAN_A_MARGIN` |
| Fan B shadow margin (from cone) | 40mm | `FAN_B_MARGIN` |

*Components: Fan A — 150mm compact axial panel fan, far end wall (X=C_LEN), exhaust, Circuit A,
high position (Z=2200mm, above the 2020mm IBC stack so the baffle duct clears the totes). Fan B —
identical fan, mounted on hinged panel (near corner zone by the pinhole wall, Yd=365mm — rev9/B2
swap so its conduit runs along the pinhole wall without crossing the suspension rails), intake,
Circuit B, low position. Fan A mounts on interior face of a 300mm deep light-safe baffle duct with 2 offset
steel baffles (65% height each, horizontal S-path); exterior face has a passive weatherproof louvre grille.
Fan B has the same baffle duct protruding from the panel exterior face — draws fresh air from the
open doorway during operation. Fan B moves with the panel on the sliding carriage; wiring via
flexible coiled cable from fixed door frame (Circuit B).*

*Report: [Ventilation & Cooling System](ventilation-report.md) — authoritative specification for fan system, baffle ducts, operating modes, and shade canopy.*

*Diagrams: lighttrap sheet 1 combined elevation (LT), lighttrap sheet 2 ventilation details (LT), electrical sheet 1 wiring (ES), floor plan (FP), assembly overview (AO).*

### 1.8 Evaporative Cooler (External)

| Parameter | Value | Constant |
|-----------|-------|----------|
| Duct penetration X | 1000mm | `EVAP_DUCT_X` |
| Duct penetration Z | 1900mm | `EVAP_DUCT_Z` |
| Duct diameter | 200mm | `EVAP_DUCT_D` |

*Component: Portacool Jetstream 110 or equivalent, 12V DC, ~80W, ~300 CFM, dedicated 20L
water reservoir, Circuit E. Ground-placed outside the container; cooled air enters through
Ø200mm insulated flex duct to a wall penetration with light-safe baffle at Z=1900mm.*

*Report: [Ventilation & Cooling System](ventilation-report.md) §5 — evaporative cooler specification, light-safe intake duct, and transport stowage.*

*Diagrams: lighttrap sheet 1 (LT), electrical sheet 1 wiring (ES), floor plan (FP), assembly overview (AO), assembly fabrication (AF).*

### 1.9 Electrical System

| Parameter | Value | Constant |
|-----------|-------|----------|
| Electrical panel left edge X | 1600mm | `EP_X` |
| Panel width | 300mm | `EP_W` |
| Panel height range | 900–1500mm | `EP_H_LO`, `EP_H_HI` |
| Battery bank left edge X | 1810mm | `BA_X` |
| Battery bank width | 500mm | `BA_W` |
| Battery bank height range | 100–600mm | `BA_H_LO`, `BA_H_HI` |

*Components: 3× 200W monocrystalline solar panels (roof-mounted), Victron SmartSolar MPPT 100/50,
2× 100Ah LiFePO4 batteries (200Ah / 2,400Wh), Victron Blue Smart IP65 shore charger,
NEMA 5-15R weatherproof inlet, Blue Sea 5026 12-circuit fuse block, IP65 enclosure
(300×200×130mm), 200A ANL main fuse, 4 AWG ground wire + 8ft copper stake.*

*Circuits: A — safelight strip (overhead red LED); B — film plane mechanism motors;
C — water pumps P-01–P-04 (P-03 in IBC corridor); D — safelight vestibule; E — evaporative cooler; F — ventilation fans.*

### 1.10 Pump Manifold (Equipment Panel)

| Parameter | Value | Constant |
|-----------|-------|----------|
| Left edge X | 4800mm | `PUMP_X` |
| Width | 780mm | `PUMP_W` |
| Height range | 900–1400mm | `PUMP_H_LO`, `PUMP_H_HI` |
| Depth from pinhole wall | 1046mm | `PUMP_YD` (= `CORRIDOR_YD_NEAR`) |
| Protrusion from panel | 127mm | `PUMP_D` |

*Components: 1" HDPE header + isolation valves, 4× 12V pumps on equipment panel (P-01 Blue spray bar supply,
P-02 Brown recycle via filter, P-03 waste evacuation, P-04 tray sump pickup),
1-gal pressure accumulator ACC-01, DN50 butterfly valves V1–V4 (S60×6 thread) at IBC outlets,
manifold ball valves VB1/VB2/VB3, check valves CV1/CV3/CV4 on bulkhead lines X1/X3/X4, X1 fill tee (splits to IBC-1 & IBC-2), Circuit C.
Mounted on 18mm marine ply equipment panel at Yd=1,046 (near IBC column face), in the IBC plumbing corridor.*

### 1.11 Water System — Blue Circuit

| Parameter | Value | Constant |
|-----------|-------|----------|
| IBC column left edge X | 4674mm | `IBC_COL_X` |
| IBC footprint width | 1219mm | `IBC_W` |
| IBC footprint depth | 1016mm | `IBC_D` |
| Stacked height (2× Blue IBC) | 2020mm | `IBC_H_STK` |
| Blue stack front depth from pinhole wall | 30mm | `BLUE_IBC_Y` |

*Components: 2× 600L food-grade HDPE IBC totes (Y-stacked in right end zone), stacking
frame (50×50×3mm RHS steel), 1" SDR-11 HDPE blue supply pipe, spray bar (¾" HDPE,
600mm spacing), camlock fill inlet, low-level float switch.*

### 1.12 Water System — Brown Circuit

| Parameter | Value | Constant |
|-----------|-------|----------|
| Brown IBC front depth | 30mm | `BROWN_IBC_Y` |
| IBC dimensions | same as Blue | `IBC_W`, `IBC_D`, `IBC_H_600` |

*Components: 1× 600L food-grade HDPE IBC (Y-stacked behind Blue stack, right end zone),
DN50 butterfly valve (S60×6) + S60×6-to-1" NPT adapter at drain outlet,
filter skid with 3-stage Big Blue housing (50μm → 5μm → GAC carbon), Shurflo P-02,
3-way diverter valves 3W-DV-01 and 3W-DV-02, pH test point.
Filled via DN150 top fill cap from P-04 tray sump pickup pump.*

### 1.13 Water System — Black Circuit (Waste)

| Parameter | Value | Constant |
|-----------|-------|----------|
| Waste IBC front depth | 1316mm | `WASTE_IBC_Y` |
| IBC far column start Y | 1316mm | `IBC_FAR_Y` |
| Waste IBC color code | Black | `C_WASTE_IBC` |

*Components: 1× 600L food-grade HDPE IBC tote (4th IBC in 2×2 stack, right end zone),
DN50 butterfly valve (S60×6) + S60×6-to-1" NPT adapter at drain outlet,
2" NPT bulkhead fittings for external drain/fill (X4), reinforcing plates for external ports,
P-03 waste evacuation pump (mounted in IBC plumbing corridor on X4 drain run). Filled via DN150 top fill cap from filter reject line.*

### 1.14 Equipment Zones

| Parameter | Value | Constant |
|-----------|-------|----------|
| Left end zone boundary (right edge) | X = 150mm | `ZONE_L_END` |
| Right end zone boundary (left edge) | X = 4649mm | `ZONE_R_START` |
| Optical cone left at depth Y | `PH_X − (PH_X − FP_X_L) × Y / FP_Y` | `cone_left(y)` |
| Optical cone right at depth Y | `PH_X + (FP_X_R − PH_X) × Y / FP_Y` | `cone_right(y)` |

*Derived rule: any equipment with X < ZONE_L_END is shadow-free at all depths.
Any equipment with X > ZONE_R_START is shadow-free at all depths.
Equipment at Yd = 0 (pinhole wall face) is always shadow-free.
Equipment in the IBC corridor (X > ZONE_R_START) at any Yd is shadow-free.*

### 1.15 Panel Sliding Carriage

| Parameter | Value | Constant |
|-----------|-------|----------|
| Panel slide travel | 880mm | `PANEL_SLIDE` |
| Panel slide rails | HGR20 × 1200mm, 2 rails (B2 — span the 880mm slide) | — |
| Lock mechanism | Destaco 207-U toggle clamp (×4) | — |

*Components: HGR20 linear rails (both walls, floor + ceiling), HGH20CA carriage blocks (×8),
carriage beam (60×60×3mm SHS, 2400mm tall), Destaco 207-U toggle clamps (×4),
hinge mounting plates, rail mounting brackets.*

*Diagrams: container floor plan (FP), assembly overview plan view (AO), hinged panel sheet 4 (HP).*

### 1.16 Processing Tray

| Parameter | Value | Constant |
|-----------|-------|----------|
| Tray left edge X | 170mm | `PROC_TRAY_X_L` |
| Tray right edge X | 4629mm | `PROC_TRAY_X_R` |
| Tray width | 4459mm | `PROC_TRAY_W` |
| Tray depth | 2200mm | `PROC_TRAY_D` |
| Tray near edge Yd | 80mm | `PROC_TRAY_YD_NEAR` |
| Tray far edge Yd | 2280mm | `PROC_TRAY_YD_FAR` |
| Rim height | 50mm | `PROC_TRAY_RIM` |
| Dual-axis pitch | 1:200 (10mm fall) | `PROC_TRAY_PITCH` |
| Sump X | 2399mm | `PROC_TRAY_DRAIN_X` |
| Sump Yd | 80mm | `PROC_TRAY_DRAIN_YD` |
| Sump dimensions | 150 x 100 x 20mm | `PROC_TRAY_SUMP_W/D/Z` |

*Components: 304 SS sheet (16-ga, 1.5mm), 2 panels field-bolted at center flange,
pressed sump well (150x100x20mm), 5x tapered HDPE shim strips (50mm wide, 0-10mm),
1" SS foot valve w/ strainer, 1" reinforced suction hose, silicone gasket strip,
M6x16 SS fasteners. No penetration of tray or container floor.
Permanently installed — no removal for transport mode conversion.*

*Diagrams: water system sheets 3-4 (WS), container floor plan (FP), assembly overview (AO), walkway sheet 2 (WK).*

### 1.17 Perimeter Walkway

| Parameter | Value | Constant |
|-----------|-------|----------|
| Walkway width | 300mm | `WALKWAY_W` |
| Deck height | 80mm | `WALKWAY_H` |
| Grate thickness (all sections) | 25mm | `WALKWAY_GRATE_T` |
| Bracket vertical leg | 150mm | `WALKWAY_BRACKET_H` |
| Bracket plate thickness | 8mm | `WALKWAY_BRACKET_T` |
| Bracket spacing | 457mm | `WALKWAY_BRACKET_SPACING` |
| Container rib spacing | 457mm | `CONTAINER_RIB_SPACING` |
| Angle iron mounting rail | 50×50×5mm | `WALKWAY_ANGLE_IRON` |
| Near walkway Yd | 0mm | `WALKWAY_NEAR_YD` |
| Far walkway Yd | 2062mm | `WALKWAY_FAR_YD` |
| Left walkway X | 170mm | `WALKWAY_LEFT_X` |
| Left walkway unsupported span | 1762mm | `WALKWAY_LEFT_SPAN` |
| Right walkway X | 4329mm | `WALKWAY_RIGHT_X` |

*Components: Near/far: 15mm grating on 8mm gusset brackets bolted to corrugated wall ribs.
Right: ceiling-hung — 2× 25×25×5mm steel angle bearers suspended from ceiling by M10
threaded rod hangers (5 pairs — 1st at Yd=320mm, rest at 457mm centers). No floor contact — clears IBC stack entirely.
Left: removable lift-out, 15mm grating resting on butt joints (no brackets —
panel conflict, must remove before panel slides to transport). No floor contact on
any section. 4 removable sections.*

*Diagrams: walkway sheet 1 cross-section (WK), walkway sheet 2 plan view (WK), container floor plan (FP).*

### 1.18 Ceiling Rail Suspension

| Parameter | Value | Constant |
|-----------|-------|----------|
| Panel floor gap | 80mm | `PANEL_FLOOR_GAP` |

*Components: HGR20 ceiling-mounted linear rails (×2, 500mm), HGH20CA carriage blocks (×4),
ceiling mounting brackets, drop rods / hanging brackets. Suspends hinged panel with 80mm
floor gap to clear processing tray rim (50mm) during transport slide.*

*Diagrams: ceiling rail sheet 1 side elevation (CR), ceiling rail sheet 2 detail (CR), hinged panel sheet 4 (HP).*

---

## 2. Script and Diagram Index

Every generator script, its output PNGs, and the subsystems it renders.

| Abbr | Generator script | PNG files produced | Subsystems drawn |
|------|-----------------|-------------------|-----------------|
| **FP** | `generate_floorplan_diagram.py` | `diagrams/container-floorplan.png` | 1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 13, 14 |
| **LOS** | `generate_line_of_sight.py` | `diagrams/line-of-sight.png` | 1, 2, 3, 5, 8, 9, 10, 11, 12, 13, 14 |
| **AO** | `generate_assembly_overview.py` | `diagrams/assembly-overview.png`<br>`diagrams/assembly-overview-fp.png`<br>`diagrams/assembly-overview-plan.png` | 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13 |
| **AF** | `generate_assembly_fabrication.py` | `diagrams/assembly-fab-sheet1.png`<br>`diagrams/assembly-fab-sheet2.png` | 1, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13 |
| **FPM** | `generate_film_plane_mechanism.py` | `diagrams/film-plane-sheet1.png`<br>`diagrams/film-plane-sheet2.png`<br>`diagrams/film-plane-sheet3.png`<br>`diagrams/film-plane-sheet4.png` | 1, 2, 3 |
| **FPD** | `generate_film_plane_distortion.py` | `diagrams/film-plane-distortion-c0.png` – `c5.png`<br>`diagrams/film-plane-distortion-summary.png` | 3 (optical simulation) |
| **ES** | `generate_electrical_diagram.py` | `diagrams/electrical-sheet1.png`<br>`diagrams/electrical-sheet2.png` | 1, 7, 8, 9, 10 |
| **WS** | `generate_water_system.py` | `diagrams/water-system-sheet1.png`<br>`diagrams/water-system-sheet2.png` | 1, 10, 11, 12, 13 |
| **HP** | `generate_hingepanel_diagram.py` | `diagrams/hingepanel-sheet1.png`<br>`diagrams/hingepanel-sheet2.png`<br>`diagrams/hingepanel-sheet3.png`<br>`diagrams/hingepanel-sheet4.png` | 1, 5, 6, 17 |
| **LT** | `generate_lighttrap_diagram.py` | `diagrams/lighttrap-sheet1.png`<br>`diagrams/lighttrap-sheet2.png` | 1, 5, 6, 7, 8 |
| **TSB** | `generate_tilt_swing_board.py` | `diagrams/tilt-swing-board-sheet1.png`<br>`diagrams/tilt-swing-board-sheet2.png`<br>`diagrams/tilt-swing-board-sheet3.png` | 2, 4 |
| **TSD** | `generate_tilt_swing_distortion.py` | `diagrams/tilt-swing-combined-c0.png` – `c8.png`<br>`diagrams/tilt-swing-combined-summary.png` | 3, 4 (optical simulation) |
| **PD** | `generate_plate_drawing.py` | `diagrams/plate-drawing-sheet1.png`<br>`diagrams/plate-drawing-sheet2.png` | 1, 2 |
| **WK** | `generate_walkway_diagram.py` | `diagrams/walkway-sheet1.png`<br>`diagrams/walkway-sheet2.png`<br>`diagrams/walkway-sheet3.png`<br>`diagrams/walkway-sheet4.png`<br>`diagrams/walkway-sheet5.png`<br>`diagrams/walkway-sheet6.png` | 1, 16, 17 |
| **CR** | `generate_ceiling_rail_diagram.py` | `diagrams/ceiling-rail-sheet1.png`<br>`diagrams/ceiling-rail-sheet2.png` | 1, 6, 15, 16, 17, 18 |
| **SC** | `generate_schematic.py`<br>`generate_portrait_viz.py` | `diagrams/portrait-camera-schematic.png`<br>`diagrams/portrait-optimal-3m.png`<br>`diagrams/portrait-scale-comparison.png` | 1, 2 (optical visualization) |

> **FPM / FPD redrawn for Option A (2026-06-06):** the film-plane mechanism sheets and optical-distortion renders now show the **fixed-size rigid plane on floating-corner cross-slides** — **axis tilt/swing** about the plane centre (foreshortening, not growth), tilt ±40° / swing ±28°, single rigid ACM backing, cross-slides at each corner, and the compound twist dropped (FPD now C0–C5). `generate_film_plane_mechanism.py` uses `rigid_corners3d`/`tilt_edge`/`swing_edge` (asin, not atan) and reads `MAX_TILT_DEG`/`MAX_SWING_DEG` from `tbs_constants.py`. Consistent with `film-plane-mechanism-report.md`, `master-shopping-list.md`, `project-cost-breakdown.md`, and `models/film-plane.skp`.

---

## 3. Dependency Matrix

✓ = this subsystem is drawn in this diagram group. Re-run all ✓ scripts when the subsystem changes.

| Subsystem | FP | LOS | AO | AF | FPM | FPD | ES | WS | HP | LT | TSB | TSD | PD | SC | WK | CR |
|-----------|:--:|:---:|:--:|:--:|:---:|:---:|:--:|:--:|:--:|:--:|:---:|:---:|:--:|:--:|:--:|:--:|
| **1** Container | ✓ | ✓ | ✓ | ✓ | ✓ | | ✓ | ✓ | ✓ | ✓ | | | ✓ | ✓ | ✓ | ✓ |
| **2** Optical Aperture | ✓ | ✓ | ✓ | ✓ | ✓ | | | | | | ✓ | | ✓ | ✓ | | |
| **3** Film Plane Mech | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | | | | | ✓ | | | | |
| **4** Tilt-Swing Board | | | | | | | | | | | ✓ | ✓ | | | | |
| **5** Light Trap Drum | ✓ | ✓ | ✓ | ✓ | | | | | ✓ | ✓ | | | | | | |
| **6** Hinged Panel | | | ✓ | ✓ | | | | | ✓ | ✓ | | | | | | ✓ |
| **7** Ventilation | ✓ | | ✓ | | | | ✓ | | | ✓ | | | | | | |
| **8** Evap Cooler | ✓ | ✓ | ✓ | ✓ | | | ✓ | | | ✓ | | | | | | |
| **9** Electrical | ✓ | ✓ | ✓ | ✓ | | | ✓ | | | | | | | | | |
| **10** Pump Manifold | ✓ | ✓ | ✓ | ✓ | | | ✓ | ✓ | | | | | | | | |
| **11** Blue Water (IBCs) | ✓ | ✓ | ✓ | ✓ | | | | ✓ | | | | | | | | |
| **12** Brown Water (IBC) | ✓ | ✓ | ✓ | ✓ | | | | ✓ | | | | | | | | |
| **13** Black Water (waste IBC) | ✓ | ✓ | ✓ | ✓ | | | | ✓ | | | | | | | | |
| **14** Zones / Layout | ✓ | ✓ | ✓ | | | | | | | | | | | | | |
| **15** Panel Slide Carriage | ✓ | | ✓ | | | | | | ✓ | | | | | | | ✓ |
| **16** Processing Tray | ✓ | | ✓ | | | | | | | | | | | | ✓ | ✓ |
| **17** Perimeter Walkway | | | | | | | | | ✓ | | | | | | ✓ | ✓ |
| **18** Ceiling Rail Susp. | | | | | | | | | | | | | | | | ✓ |

---

## 3.1 SketchUp 3D models

Each subsystem is also built in the SketchUp 3D model(s). When a subsystem's
constants change, **re-run the model(s) that contain it** (in addition to the 2D
scripts) so the 3D models stay in sync with the drawings — see the Workflow below.

| Model | Script | Output | Subsystems contained |
|---|---|---|---|
| **overview** | `src/models/generate_sketchup_model.py` | `models/overview.skp` + `src/models/overview.rb` | **1–18 (all)** — built as 22 tagged components (incl. lighting/wiring, spray-bar plumbing, fans, water hookups). Its `spray_bar()` **reuses the spray-bar model's builders** (`generate_spraybar_model.build_beam/build_carriages/build_feed_pole`), and `light_trap_drum()` + `light_trap_frame()` **reuse the light-trap model's `lt.drum()` + `lt.door_frame()`** (the door frame + top/bottom seal lips that block light) — so all stay in sync; rebuild overview whenever the spray-bar **or** light-trap model changes. Its `walkways()` includes the wall-cantilevered **gusset brackets** (`walkway_brackets()`: near & far long walls at 457mm rib centers — standard 8mm/150mm-leg/300mm-arm with 3× M12, the four widened EP/battery-zone brackets 10mm/200mm-leg/500mm-arm with 4× M12, per Sheet 7) that carry the near/far decks. **Scenes:** Overview (all, labels off) + **Labeled** — same view with in-model `add_text` callouts on the major system components (`overview_labels()`: 10 anchored to each instance's bounds top-centre + 5 **point-anchored** via `OVERVIEW_POINT_LABELS` for items not a single instance — **FAN A** (IBC end), **FAN B** (door end) [the two live in one "Fans A & B" component spanning both ends], and the **BATTERY BANK** [inside the Electrical component]; on a `Labels` tag shown only in this scene; see [[feedback-3d-model-labels]]). The leader format is `(Δx,Δy,Δz)` mm so wall-mounted callouts (pinhole, spray bar) pull OUT toward the viewer clear of the container — keep Δz modest so the label isn't clipped past the geometry-framed camera. Plus 6 grouped subsystem scenes (labels off). |
| **spray-bar** | `src/models/generate_spraybar_model.py` | `models/spraybar.skp` + `src/models/spraybar.rb` | Spray-bar gantry detail — beam (**spans the full tray width, `PROC_TRAY_X±30`, matching the 2D `generate_spray_bar_diagram.py`; bugfix 2026-06-06 — the 3D beam had used the narrower `PROC_OPEN_X` print zone**) + housed ¾" LDPE pipe + 26 flat-fan nozzles (150mm pitch, in the open zone), wheel carriages (2 wheels/carriage, curved saddle axle clamps, top/bottom beam clamp plates), feed pole + ball joint with **distribution manifold + 7 irrigation feed tubes** into the poly pipe, **processing tray** (floor + rim + sump). The two carriages are on their own **Carriage L / Carriage R** tags, and the small tray-floor reference patch is on its own **Tray Ref** tag (shown only in the carriage-only scenes — the Combined / Processing-Tray scenes have the real tray, so the ref patch no longer doubles up under the beam). **7 scenes:** Beam, Carriage Assembly, **One Carriage** (Carriage L only — no beam/tray, with a perpendicular close-up camera — `cdir`/standoff, not zoom_extents), Pole & Ball Joint, Processing Tray, Combined, **Labeled** (`spraybar_labels()` — `add_text` callouts; beam/carriage/nozzles/pole/manifold point-anchored; see [[feedback-3d-model-labels]]). The scene loop takes an optional `[x,y,z,standoff]` close-up target. **NB: avoid `"` in label text** — an unescaped quote closes the emitted Ruby string and silently corrupts the whole rebuild (hangs the send). Reads `SPRAY_BAR_*` and `PROC_TRAY_*` constants. |
| **ibc-stack** | `src/models/generate_ibc_model.py` | `models/ibc-stack.skp` + `src/models/ibc-stack.rb` | IBC tote stacking arrangement at the IBC end. Reuses Overview builders: `ov.ibc_stack()` (4× 1000L totes), `ov.ibc_rack()` (steel frame), `ov.equipment_panel()` (pump/filter), `ov.water_plumbing()`, `ov.water_hookups()` (exterior wall). Container is a low-alpha ghost. 4 tags (Context / IBC Tanks / IBC Frame / Plumbing & Panel) + a `Labels` tag. **5 scenes:** IBC Tanks, IBC Frame, Plumbing & Panel, Combined, **Labeled** (`ibc_labels()` — `add_text` callouts on the `Labels` tag, shown only in this scene; 19 callouts split by side. **Container/front side:** the near-column totes (BROWN developer + BLUE #1), the **SUMP PICKUP** riser, the **TO SPRAY BAR** Blue feed, **IBC FRAME**, and the **wet-end panel equipment** pulled out the front laid out as the panel reads — two pump columns (left ACC-01/P-04/P-01, right P-05/P-03/P-02) + three filters F1/F2/F3 below (pumps/filters/accumulator only, no pipes/valves). **Sealed-end side** (right-hand column): the far-column totes (WASTE + BLUE #2) plus the exterior bulkhead ports **X1** (fresh fill), **X3** (Brown drain-out), **X4** (Waste drain-out). Per the project rule every .skp gets a Labeled scene — see [[feedback-3d-model-labels]]). Rebuild whenever those `ov` builders or the IBC/plumbing constants change. |
| **walkway** | `src/models/generate_walkway_model.py` | `models/walkway.skp` + `src/models/walkway.rb` | Processing-tray **perimeter walkway + how it's held up**, separated so the structure reads apart from the decks. 6 tagged components: **Walkways** (near + widened + far + left removable decks + drum-exit punch-out — the right deck is split onto its own **Walkway Right** tag so the Right Hangers scene can show it alone); **Walkway Right** (the IBC-end ceiling-hung deck); **Cantilevers** (near/far wall-cantilevered gusset brackets carrying the near/far decks, with the **exterior** detail — reinforcing plate + through-bolts, hex heads outside; standard brackets 8mm/150mm-leg/300mm-arm with **3× M12** triangular, the four widened EP/battery-zone brackets (near, X 1155–2629) 10mm/200mm-leg/500mm-arm with **4× M12** rectangular — matching Sheet 7); **Right Hangers** (ceiling-hung right walkway — 2 bearer angles + 5 rod-pairs of M10 rod to ceiling plates); **Left Support** (removable lift-out — a **full-width steel edge beam** on **bolt-through wall seats** [IBC-style, see [`spec`](docs/superpowers/specs/2026-06-05-left-walkway-edge-beam-support.md)] + bearing strip + 3 floor legs); **Processing Tray** (reuses `ov.processing_tray()`); plus a **Cantilever Types** tag/component — ONE of each unique bracket type (standard, widened, and bearer-support), built side-by-side on the near wall by `cantilever_types()` (all reuse the extracted `_cantilever_parts()` helper that also builds the in-situ `cantilevers()`; the bearer-support entry is a standard bracket plus a stub of the right-walkway 25×25×5 L-angle bearer resting on its arm), shown only in the Cantilevers scene. Container is a low-alpha ghost so the exterior braces + bolt-throughs show. **7 scenes:** **Combined**, **Labeled** (`walkway_labels()` — `add_text` callouts on a `Labels` tag, decks/cantilevers/hangers/support point-anchored since they're paired/perimeter; camera pulls back `zoom(0.72)`; see [[feedback-3d-model-labels]]), **Walkway** (all decks), **Near/Far Cantilevers** (the brackets in situ), **Right Hangers** (only the right deck — near/far/left `Walkways` tag off), **Left Support**, and **Cantilevers** (one of each unique bracket type isolated with the wall hidden + a per-scene close-up camera + type-spec callouts on the `Cantilever Types` tag — standard 8mm/150/300/3×M12, widened 10mm/200/500/4×M12, and bearer-support = a standard bracket carrying the right-walkway 25×25×5 L-angle bearer at the X=4329/4629 butt joint). Reads `WALKWAY_*`, `PROC_TRAY_*`, `LEFT_WK_*`. The edge-beam-on-wall-seats design is fully propagated to the 2D `generate_walkway_diagram.py` (Sheets 1/4/5/6/9), walkway-report §5, master-shopping-list, and project-cost-breakdown. |
| **film-plane** | `src/models/generate_film_plane_model.py` | `models/film-plane.skp` + `src/models/film-plane.rb` | Film plane + **tilt/swing mechanism — OPTION A** (chosen 2026-06-06; replaced the old stretching/U-joint 4-corner DC). The film is a **FIXED-SIZE rigid rectangle** (FP_W wide × HF=2188 rail-to-rail) that only changes ANGLE; each corner's existing **HGR20 rail + leadscrew** (depth/focus) gains a **2-axis X-Z cross-slide + spherical rod-end** that absorbs the rigid-rotation arc travel. **DYNAMIC COMPONENT** "Film Plane": click (Interact tool) → `ANIMATE("pose",0,1)` between **FLAT** (pose 0, vertical at mid-rail depth) and **TILT 20°/SWING 15°** (pose 1). Option A's plane motion *is* a genuine rigid rotation, so the DC reproduces it **exactly** (single component, geometry direct, custom `pose` + same-component `_rotx_formula="20*pose"`/`_rotz_formula="15*pose"`, single `onclick`, `redraw_with_undo` AFTER commit). The **carriages + rod-ends travel WITH the plane** (built into the DC); the **rails + leadscrews stay static** — at the posed extreme the carriages necessarily leave the rails (the rigid-DC can't keep them on AND extend the slides; the default flat state reads connected). **The X/Z cross-slides are the NON-rigid part a DC can't animate**, so they're shown **statically with labels** in the non-interactive **"Corner detail (TR)"** scene (in-model `add_text` callouts on a `Labels` tag — see [[feedback-3d-model-labels]]). **Design note:** a rigid plane can't reach the old ±42°/±25.7° stops — at those angles a corner sweeps ~3.4 m of depth (through both end walls); practical envelope **tilt≤20°/swing≤15° combined**. **NB: DC interactivity is SketchUp-app only — does NOT carry to Sketchfab embeds; scene-tab cameras mis-frame in some builds → render via direct camera.** Reuses `ov.processing_tray()` + helpers; ghost-container context. Reads `FP_*`, `RAIL_*`, `FP_ANGLE_LEG`, `PROC_TRAY_*`; the example DC pose (20°/15°) is **local** to the generator, but the Option-A envelope (`MAX_TILT_DEG`=40 / `MAX_SWING_DEG`=28) + cross-slide constants, the 2D `generate_film_plane_mechanism.py` sheets, the film-plane report, master-shopping-list and project-cost-breakdown were all **cascaded (done 2026-06-06)**. 3 scenes (Combined, No Container, Corner detail TR). 3D companion to 2D `generate_film_plane_mechanism.py`. |
| **lighttrap** | `src/models/generate_lighttrap_model.py` | `models/lighttrap.skp` + `src/models/lighttrap.rb` | **Single interactive cargo-door-end model** (rev 9 / B2 — consolidates the former separate operating + transport models into one .skp via Dynamic Components). **Static parts:** ghosted container stub (ends at the door plane X=0 so the bay/drum/doors read as protruding beyond it), fixed RHS **door frame** (`door_frame(include_seal=False)` — the housing-surround EPDM rides the moving housing), fixed **carriage rails + Destaco locks** (`carriage_fixed()`), partial **processing tray**, near/far **walkways**, and the continuous left **film-plane rails**. **Two Dynamic Components** (click with SketchUp's Interact tool): **(1) Panel Slide** — the moving assembly (hinged stepped panel + 3 barrel hinges + 4 Southco latches, B2 **punch-out bay** `bay()` offsetting the drum to X=−400, the **housed revolving-door light lock** Ø900 housing + C-shell drum + seals + grab rail, **Fan B**, and the moving carriage blocks/brackets/beam via `carriage_moving()`) animates X between operating (0) and transport (`TRANSPORT_SLIDE`≈880mm); **(2) Cargo Doors** — a parent DC whose `shut` attribute drives two leaf children's `RotZ` (`door_leaf_local()`), swinging both ISO leaves 0↔±180° (closed↔open). Fan B **reuses the Overview's shared `fan_duct()`**. Reads `DRUM_*`, `PANEL_*`, `FAN_B_*`, `BAY_*`, `PANEL_SLIDE`. **Requires the Dynamic Components extension** for the click behavior — it does **not** carry to Sketchfab web embeds (those render a static pose). 8 components (6 static + 2 DCs), **2 scenes**: the interactive slide scene + a **Labeled** scene (`lighttrap_labels()` / `LIGHTTRAP_LABELS` + `LIGHTTRAP_POINT_LABELS` — `add_text` callouts on a `Labels` tag, drum/Fan B point-anchored since they're nested in the Panel Slide DC; the camera pulls back `zoom(0.62)` so callouts have margin). Per the project rule, every new .skp gets a Labeled scene — see [[feedback-3d-model-labels]]. **Rebuild whenever those constants or the shared builders change.** |

*As more models are added, list them here with the subsystems each contains, so a
constants change re-runs only the affected models.*

---

## 4. Change Propagation Guide

When a constant in `tbs_constants.py` changes, re-run all 2D scripts listed below
**and re-run any SketchUp model (§3.1) that contains the affected subsystem.**
Then commit the updated PNGs and `*.skp`/`*.rb` alongside the constant change.

| Changed constant(s) | Re-run scripts (abbr) | Notes |
|--------------------|----------------------|-------|
| `PH_X`, `PH_H` | FP, LOS, AO, AF, FPM, FPD, TSB, TSD, PD, SC | Pinhole reposition — cone geometry changes everywhere; MAX_SWING_DEG unchanged |
| `PH_D`, `PH_FNO` | TSB, PD, SC | Aperture spec change — layout diagrams unaffected |
| `FP_X_L`, `FP_X_R`, `FP_W` | FP, LOS, AO, AF, FPM, FPD, TSD | Rail span + ZONE boundaries change (Option A: `MAX_SWING_DEG` is now a fixed design value, not derived from `FP_W`) |
| `FP_Y`, `FP_Y_MIN` | FP, LOS, AO, AF, FPM, FPD, TSD | Depth / rail-travel change (Option A: `MAX_TILT_DEG`/`MAX_SWING_DEG` are now fixed design values, not auto-derived) |
| `MAX_TILT_DEG`, `MAX_SWING_DEG`, `XSLIDE_*` | FPM, FPD | Option A tilt/swing envelope + cross-slide travel — **design values** (hardcoded, not derived); FPM sheets + FPD distortion renders redraw on change |
| `RAIL_LEN` | FPM | Rail length only — no layout impact |
| `C_LEN` | FP, LOS, AO, AF, FPM, ES, WS, HP, LT, PD, SC | Container resize — rare |
| `C_WID` | FP, LOS, AO, AF, FPM, ES, WS, HP, LT, PD, SC | Changes focal length and cone geometry |
| `C_HGT` | FP, LOS, AO, AF, ES, HP, LT | Height change |
| `EVAP_DUCT_X`, `EVAP_DUCT_Z`, `EVAP_DUCT_D` | FP, AO, AF, ES | Evap duct penetration (cooler external) |
| `EP_X`, `EP_W`, `EP_H_LO`, `EP_H_HI` | FP, LOS, AO, AF, ES | Electrical panel on pinhole wall |
| `BA_X`, `BA_W`, `BA_H_LO`, `BA_H_HI` | FP, LOS, AO, AF, ES | Battery bank on pinhole wall |
| `PUMP_X`, `PUMP_W`, `PUMP_H_LO`, `PUMP_H_HI` | FP, LOS, AO, AF, ES, WS | Pump manifold on equipment panel (Yd=1046) |
| `IBC_COL_X`, `BLUE_IBC_Y`, `BROWN_IBC_Y` | FP, LOS, AO, AF, WS | Right end zone IBC stack |
| `WASTE_IBC_Y`, `IBC_FAR_Y`, `C_WASTE_IBC` | FP, LOS, AO, AF, WS | Right end zone waste IBC (4th tote in 2×2 stack) |
| `PANEL_SLIDE` | FP, AO, HP | Panel sliding carriage travel |
| `DRUM_CX`, `DRUM_D`, `DRUM_H_LT` | FP, LOS, AO, AF, HP, LT | Light trap drum; check `ZONE_L_END` |
| `ZONE_L_END`, `ZONE_R_START` | FP, LOS, AO, ES | Zone boundaries — these are derived from `FP_X_L`/`FP_X_R`, so change those instead |
| `FAN_A_H`, `FAN_B_H`, `FAN_DIAM`, `FAN_BODY_D` | LT, ES | Ventilation fan height or size |
| `DUCT_DEPTH`, `DUCT_HEIGHT` | LT | Baffle duct only — lighttrap sheets |
| `WALKWAY_W`, `WALKWAY_H`, `WALKWAY_GRATE_T` | WK, CR, HP | Walkway deck dimensions — affects clearance annotations in CR |
| `WALKWAY_BRACKET_H`, `WALKWAY_BRACKET_T`, `WALKWAY_BRACKET_SPACING` | WK, CR, HP | Bracket geometry |
| `WALKWAY_ANGLE_IRON`, `WALKWAY_ANGLE_IRON_T` | WK | Right walkway angle iron mounting (flat end wall only) |
| `PROC_TRAY_X_L`, `PROC_TRAY_X_R`, `PROC_TRAY_RIM` | FP, AO, WK, CR | Processing tray position and rim — walkway alignment and panel clearance |
| `PANEL_FLOOR_GAP` | CR, HP | Panel bottom clearance — must exceed `PROC_TRAY_RIM` |

### Workflow

```
1. Edit tbs_constants.py
2. python3 tbs_constants.py          # verify no errors, check derived values in summary
3. python3 generate_<affected>.py    # for each affected 2D script (see table above)
4. Re-run affected SketchUp model(s) (§3.1):
     python3 src/models/generate_sketchup_model.py --save --send
   # regenerates overview.rb + re-sends to SketchUp; save the .skp
5. Visually inspect updated PNGs in diagrams/ AND the SketchUp model
6. bash publish.sh --build           # verify zero MkDocs warnings
7. git add tbs_constants.py diagrams/*.png models/*.skp src/models/overview.rb && git commit -m "..."
8. bash publish.sh                   # deploy
```

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
