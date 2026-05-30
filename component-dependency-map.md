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
| Film plane left edge X | 625mm | `FP_X_L` |
| Film plane right edge X | 4649mm | `FP_X_R` |
| Film plane width | 4499mm | `FP_W` |
| Film plane height | 2388mm | `FP_H` |
| Nominal depth from pinhole wall | 2262mm | `FP_Y` |
| Minimum carriage depth | 100mm | `FP_Y_MIN` |
| Left rail X | 150mm | `RAIL_X_L` |
| Right rail X | 4649mm | `RAIL_X_R` |
| Rail span | 4499mm | `RAIL_SPAN` |
| Rail length (Y travel) | 2200mm | `RAIL_LEN` |
| Max tilt | ±42.2° | `MAX_TILT_DEG` |
| Max swing | ±25.7° | `MAX_SWING_DEG` |

*Components: welded aluminum angle frame (2"×2"×3/16"), 4× HGR20 linear rails (ceiling + floor),
8× HGH20CA carriage blocks, 4× ¾"-6 Acme leadscrews, 4× bronze nuts, 4× 8" handwheels,
8× GIR25-DO rod-end spherical bearings, hinged ACM backing panels, Duvetyne curtain seals,
rail felt light-trap strips, 92× cam-lever spring clamps at 150mm centers (muslin attachment).*

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

### 1.5 Light Trap Drum

| Parameter | Value | Constant |
|-----------|-------|----------|
| Drum center X (cargo door end wall) | 0mm | `DRUM_CX` |
| Drum outer diameter | 750mm | `DRUM_D` |
| Drum radius | 375mm | `DRUM_R` |
| Drum height | 2200mm | `DRUM_H_LT` |

*Components: 3mm mild steel rolled shell, 4× internal steel baffle fins (at 22.5°/112.5°/
202.5°/292.5°), 5mm top and bottom caps, 75mm stub shafts (×2), 2× SKF 6215-2RS1 sealed
bearings, upper and lower bearing mounts, 100mm SS interior grab rail, closed-cell neoprene
top/bottom wiper seals + silicone bead, drum-to-panel neoprene compression strip.*

### 1.6 Hinged Cargo-Door Panel

| Parameter | Value | Constant |
|-----------|-------|----------|
| Panel width | 2362mm | `C_WID` |
| Panel height | 2388mm | `C_HGT` |
| Panel thickness | 120mm | — (hardcoded in scripts) |

*Components: 50×50mm RHS steel frame, 18mm plywood skins (both faces), 20mm EPDM compression
gasket in machined channel, 3× 200mm SS ball-bearing piano hinges, 4× Southco C2-33 cam
compression latches, Ø750mm revolving drum aperture.*

### 1.7 Ventilation System

| Parameter | Value | Constant |
|-----------|-------|----------|
| Fan diameter (both fans) | 150mm | `FAN_DIAM` |
| Panel fan body depth | 50mm | `FAN_BODY_D` |
| Fan A center height AFF (low) | 600mm | `FAN_A_H` |
| Fan B center height AFF (high) | 1800mm | `FAN_B_H` |
| Fan A Yd position (near-wall corner) | 75mm | `FAN_A_YD` |
| Fan B Yd position (centered drum–wall) | 1959mm | `FAN_B_YD` |
| Baffle duct depth | 300mm | `DUCT_DEPTH` |
| Baffle duct height | 200mm | `DUCT_HEIGHT` |
| Fan A shadow margin (from cone) | 869mm | `FAN_A_MARGIN` |
| Fan B shadow margin (from cone) | 40mm | `FAN_B_MARGIN` |

*Components: Fan A — 150mm compact axial panel fan, far end wall (X=C_LEN), intake, Circuit A,
low position. Fan B — identical fan, mounted on hinged panel (far corner zone, Yd=1959mm),
exhaust, Circuit B, high position. Fan A mounts on interior face of a 300mm deep light-safe
baffle duct with 2 offset steel baffles (65% height each, S-path); exterior face has a passive
weatherproof louvre grille. Fan B has the same baffle duct protruding from the panel exterior
face — exhausts into the open doorway during operation. Fan B moves with the panel on the
sliding carriage; wiring via flexible coiled cable from fixed door frame (Circuit B).*

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
| Electrical panel left edge X | 2050mm | `EP_X` |
| Panel width | 300mm | `EP_W` |
| Panel height range | 900–1500mm | `EP_H_LO`, `EP_H_HI` |
| Battery bank left edge X | 2050mm | `BA_X` |
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
manifold ball valves VB1/VB2/VB3, check valves CV1/CV3/CV4 on bulkhead lines X1/X3/X4, 2" cross-connect (IBC-1 ↔ IBC-2), Circuit C.
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
| Panel slide travel | 300mm | `PANEL_SLIDE` |
| Panel slide rails | HGR20 × 500mm, 4 rails | — |
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
| Deck height | 100mm | `WALKWAY_H` |
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

*Components: Near/far: 25mm grating on 8mm gusset brackets bolted to corrugated wall ribs.
Right: ceiling-hung — 2× 25×25×5mm steel angle bearers suspended from ceiling by M10
threaded rod hangers (5 pairs — 1st at Yd=320mm, rest at 457mm centers). No floor contact — clears IBC stack entirely.
Left: removable lift-out, 25mm grating resting on butt joints (no brackets —
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
| **FPD** | `generate_film_plane_distortion.py` | `diagrams/film-plane-distortion-c0.png` – `c6.png`<br>`diagrams/film-plane-distortion-summary.png` | 3 (optical simulation) |
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

## 4. Change Propagation Guide

When a constant in `tbs_constants.py` changes, re-run all scripts listed. Then commit the updated
PNGs alongside the constant change.

| Changed constant(s) | Re-run scripts (abbr) | Notes |
|--------------------|----------------------|-------|
| `PH_X`, `PH_H` | FP, LOS, AO, AF, FPM, FPD, TSB, TSD, PD, SC | Pinhole reposition — cone geometry changes everywhere; MAX_SWING_DEG unchanged |
| `PH_D`, `PH_FNO` | TSB, PD, SC | Aperture spec change — layout diagrams unaffected |
| `FP_X_L`, `FP_X_R`, `FP_W` | FP, LOS, AO, AF, FPM, FPD, TSD | Rail span and ZONE boundaries both change; verify `MAX_SWING_DEG` |
| `FP_Y`, `FP_Y_MIN` | FP, LOS, AO, AF, FPM, FPD, TSD | Depth change — also recalculates `MAX_TILT_DEG` and `MAX_SWING_DEG` |
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
3. python3 generate_<affected>.py    # for each affected script (see table above)
4. Visually inspect updated PNGs in diagrams/
5. bash publish.sh --build           # verify zero MkDocs warnings
6. git add tbs_constants.py diagrams/*.png && git commit -m "..."
7. bash publish.sh                   # deploy
```

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
