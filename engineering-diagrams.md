<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Engineering Diagrams
## TBS-001 — All Construction Drawings

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*

---

This page collects every engineering drawing produced for TBS-001, organized by subsystem.
Each section links to the report where the drawing is discussed in full.

---

## 1. System Assembly Overview

There are a number of discrete systems, color-coded in the diagram below. This view is shown from the optical axis, looking through the container wall. Each of these sub-systems, has a detailed breakdown of construction, schematic and other diagrams to show how each system it built, installed and used. Briefly these systems are:

- [Electrical system](electrical-report.md)
- [Water system and plumbing](water-system-report.md)
- [Lighttrap & Hinged panel](light-trap-selection.md)
- [Film plane mechanism](film-plane-mechanism-report.md)
- [Processing and Spray Bar](processing-tray-and-spray-bar.md)
- [Pinhole construction](pinhole-optics-report.md)

![TBS-001 — Container Floor Plan](assets/container-floorplan.png)

The container is split into three main areas

- Left: [Lighttrap](light-trap-selection.md), [hinged panel](hinged-panel-report.md)
- Center: Processing tray, film plan mechanism, electrical panels & battery pack
- Right: IBC stacking system, plumbing panel

![TBS-001 — Assembly: Side Elevation — pinhole wall view](assets/assembly-overview.png)

Second view from the film plane wall (Yd = 2,362mm), looking toward the pinhole. X axis
is mirrored (far end at left, cargo door at right). The optical cone, film plane rails,
and carriage are the hero elements in this view.

![TBS-001 — Assembly: Film Plane Side Elevation](assets/assembly-overview-fp.png)

Plan view of the cargo door end showing the stepped panel position
in both transport mode (panel retracted 300mm, ISO doors closed)
and operational mode (panel at X=0, doors open).

![TBS-001 — Cargo Door End Plan View: Transport vs Operational](assets/assembly-overview-plan.png)

---

## 2. Assembly Fabrication Drawings

Multi-view assembly drawing for fabrication and installation reference.

**Sheet 1 — Long-section elevation (1:50)**
All permanent installation positions dimensioned. Callout bubbles ①–⑪ reference
individual subsystem drawings.

![TBS-001 — Assembly Fab Sheet 1: Long-Section Elevation](assets/assembly-fab-sheet1.png)

**Sheet 2 — End elevation, cargo door end (1:20)**
View looking into the container from the cargo door end. Shows hinged panel, revolving
drum, film-plane rail mounting positions, equipment projection footprints, and ventilation.

![TBS-001 — Assembly Fab Sheet 2: End Elevation (Cargo Door)](assets/assembly-fab-sheet2.png)

---

## 2a. Pinhole Wall — Combined Interior Elevation

Coordination drawing showing every system mounted on the pinhole wall (Yd=0),
viewed from inside the container. All equipment drawn as simplified blocks with
their designated colors. Used to verify spatial fit and identify interferences.

Includes: evap duct penetration (Ø200mm, cooler external), external power panel
(flush-mount, exterior face), electrical panel, battery bank, pinhole aperture,
pull-cord switches, cable trunking, near walkway deck and brackets, and chemistry
shelf hanger rods (ghost — shelf at Yd=300). Pump manifold and filter skid are on
the equipment panel at Yd=1,046 (IBC corridor) — shown as ghost outlines.

![TBS-001 — Pinhole Wall Combined Interior Elevation](assets/pinhole-wall-elevation.png)

---

## 3. Container Floor Plan

Top-down floor plan of the full container interior. Equipment positions dimensioned.
Optical axis shown from pinhole (X=2946, Y=0) to film plane (Y=2262 mm).
Source report: [Electrical & Systems Report](electrical-report.md) §5.8.

![TBS-001 — Container Floor Plan](assets/container-floorplan.png)

**Sheet 2 — Cargo door egress detail (panel open 180° outward, operational position)**
![TBS-001 — Cargo Door Egress Detail](assets/container-floorplan-sheet2.png)

---

## 4. Pinhole Aperture Plate

Fabrication drawings for the interchangeable pinhole plate (TBS-P01).
Source report: [Pinhole Fab](fabrication-drawings.md).

**Sheet 1 — Assembly overview and plate dimensions**
![TBS-001 Pinhole Plate — Sheet 1](assets/plate-drawing-sheet1.png)

**Sheet 2 — Detail section and pinhole geometry**
![TBS-001 Pinhole Plate — Sheet 2](assets/plate-drawing-sheet2.png)

---

## 5. Film Plane Mechanism

Four-corner independent actuation mechanism with muslin clamp system (TBS-FM01, 5 sheets).
Source report: [Film Plane Mechanism](film-plane-mechanism-report.md).

**Sheet 1 — Assembly overview**
![TBS-001 Film Plane Mechanism — Sheet 1](assets/film-plane-sheet1.png)

**Sheet 2 — Corner assembly detail**
![TBS-001 Film Plane Mechanism — Sheet 2](assets/film-plane-sheet2.png)

**Sheet 3 — Drive shaft and handwheel**
![TBS-001 Film Plane Mechanism — Sheet 3](assets/film-plane-sheet3.png)

**Sheet 4 — Full mechanism cross-section**
![TBS-001 Film Plane Mechanism — Sheet 4](assets/film-plane-sheet4.png)

**Sheet 5 — Muslin clamp detail: cam-lever spring clamp cross-section, open/closed positions, plan view of frame attachment, and elevation at 150mm spacing**
![TBS-001 Film Plane Mechanism — Sheet 5](assets/film-plane-sheet5.png)

---

## 6. Film Plane Distortion Renders

Ray-traced distortion renders showing projected image geometry for each film-plane
configuration. Source report: [Film Plane Mechanism](film-plane-mechanism-report.md).

All renders are collected in the [Distortion Renders](distortion-renders.md) document.

---

## 7. Tilt-Swing Front Board

Spherical-pivot tilt/swing board mechanism (TBS-TS01).
Source report: [Tilt-Swing Front Board](tilt-swing-board-report.md).

**Sheet 1 — Assembly and body**
![TBS-001 Tilt-Swing Board — Sheet 1](assets/tilt-swing-board-sheet1.png)

**Sheet 2 — Pivot and adjustment detail**
![TBS-001 Tilt-Swing Board — Sheet 2](assets/tilt-swing-board-sheet2.png)

**Sheet 3 — Mounting interface and stop geometry**
![TBS-001 Tilt-Swing Board — Sheet 3](assets/tilt-swing-board-sheet3.png)

---

## 8. Combined Distortion Renders (Film Plane + Tilt-Swing)

Compound optical projections when both the film plane mechanism and the tilt-swing
front board are active simultaneously.
Source report: [Tilt-Swing Front Board](tilt-swing-board-report.md).

All renders are collected in the [Distortion Renders](distortion-renders.md) document.

---

## 9. Processing (Water) System

Off-grid three-circuit chemical processing system.
Source report: [Processing System](water-system-report.md).

**Sheet 1 — System overview and flow diagram**
![TBS-001 Water System — Sheet 1](assets/water-system-sheet1.png)

**Sheet 2 — Component layout and Bill of Materials**
![TBS-001 Water System — Sheet 2](assets/water-system-sheet2.png)

**Sheet 3 — Processing tray drainage plan (water flow direction, slope, drain)**
![TBS-001 Water System — Sheet 3](assets/water-system-sheet3.png)

**Sheet 4 — Processing tray drain cross-section elevation: Detail A sump well and pickup (~1:2), Section A-A full sump-to-IBC flow path (~1:15)**
![TBS-001 Water System — Sheet 4](assets/water-system-sheet4.png)

---

## 10. Electrical & Power

12V DC power architecture, circuit layout, and system controls.
Source report: [Electrical & Systems](electrical-report.md).

**Sheet 1 — Power distribution and circuit diagram**
![TBS-001 Electrical — Sheet 1](assets/electrical-sheet1.png)

**Sheet 2 — Wiring layout and component positions**
![TBS-001 Electrical — Sheet 2](assets/electrical-sheet2.png)

**Sheet 3 — Pinhole wall interior elevation: equipment mounting heights, cable trunking, drop conduits, pull-cord switches, LED panels**
![TBS-001 Electrical — Sheet 3](assets/electrical-sheet3.png)

---

## 11. Light Trap Vestibule — Revolving Drum (Current Design)

The TBS-001 light trap is a **revolving drum with a vertical axis** — a person
walks through it upright, like a commercial revolving door. The drum is
Ø750mm × 2000mm tall, integrated into the cargo-door hinged panel.

This design supersedes an earlier S-path vestibule concept. The full selection
analysis — including the S-path alternative, revolving drum specification, and
fabrication drawings — is in [Light Trap Selection](light-trap-selection.md).

For construction drawings of the hinged panel and drum, see
[§12 — Hinged Panel & Revolving Drum](#12-hinged-panel-revolving-drum) below.

---

## 12. Hinged Panel & Revolving Drum

Cargo-door hinged panel (2362 × 2388 mm) with integrated revolving light-trap drum.
Source report: [Light Trap Selection](light-trap-selection.md).

**Sheet 1 — Front elevation (1:20): Panel dimensions, drum, hinges, latches**
![TBS-001 Hinged Panel — Sheet 1: Front Elevation](assets/hingepanel-sheet1.png)

**Sheet 2 — Plan cross-section (1:20): Drum baffles and S-path light route**
![TBS-001 Hinged Panel — Sheet 2: Plan Cross-Section](assets/hingepanel-sheet2.png)

**Sheet 3 — Drum vertical section elevation (Section A-A): Confirms walking-height vertical drum orientation**
![TBS-001 Hinged Panel — Sheet 3: Drum Elevation](assets/hingepanel-sheet3.png)

**Sheet 4 — Sliding rail transport system (plan view): Panel slide, operational vs transport positions**
![TBS-001 Hinged Panel — Sheet 4: Sliding Rail Transport](assets/hingepanel-sheet4.png)

---

## 13. Ceiling Rail Suspension System

Panel suspension from HGR20 ceiling-mounted linear rails. Panel bottom edge clears
the permanently installed processing tray (50mm rim) during transport slide.

**Sheet 1 — Side elevation: Panel hanging from ceiling rails, processing tray clearance**
![TBS-001 Ceiling Rail — Sheet 1: Side Elevation](assets/ceiling-rail-sheet1.png)

**Sheet 2 — Detail: Rail/carriage/bracket assembly (≈2:1)**
![TBS-001 Ceiling Rail — Sheet 2: Rail Detail](assets/ceiling-rail-sheet2.png)

---

## 14. Perimeter Walkway

Removable grated walkway sections around all 4 sides of the processing tray. Provides
dry-foot access to valves, electrical panel, film plane, and tilt-swing adjusters
without wading through the wet processing tray. 300mm wide, 100mm deck height (75mm
bracket arm + 25mm grate).

Mounting varies by side:

- **Near/far walkways** (long walls): 8mm steel plate triangular gusset brackets bolted
  to corrugated wall structural ribs at 457mm (18") centers. Wall-cantilevered —
  no legs, no floor contact.
- **Right walkway** (IBC end): ceiling-hung design — no floor contact. Two 25×25×5mm
  steel angle bearers run full container width (2,362mm along Yd) at X=4,329mm and
  X=4,629mm. Suspended from ceiling corrugations by M10 threaded rod hangers at
  457mm centers (5 pairs — 1st at Yd=320mm, rest at 457mm centers; all at Yd ≤ 2,057mm — clear of optical cone). 300mm wide
  grating spans between bearers. Near/far ends bear on adjacent walkway bracket
  structures. Deck height 100mm (level with all sides). Zero tray contact, zero
  floor contact — clears IBC stack entirely.
- **Left walkway** (cargo door end): removable lift-out section with no wall brackets.
  The hinged panel occupies this end wall and slides 300mm inward for transport —
  left walkway must be removed first. Supported by: (a) bearer beam (50x50x3mm Al
  RHS) at X=470 spanning 1,762mm between near/far bracket vertical legs; (b) 3
  floor-standing support legs at X=140 on bare floor outside tray; (c) bearing
  strip (25x25x3mm Al angle) on the processing tray rim. Zero tray contact.

**Sheet 1 — Plan view: All 4 sections with bracket positions and panel transport envelope**
![TBS-001 Walkway — Sheet 1: Plan View](assets/walkway-sheet1.png)

**Sheet 2 — Cross-section through near walkway with bracket detail: Grate, cantilever bracket, corrugated wall rib attachment, tray rim clearance (≈5:1)**
![TBS-001 Walkway — Sheet 2: Cross-Section with Bracket Detail](assets/walkway-sheet2.png)

**Sheet 3 — Detail A: Right walkway ceiling-hung support at IBC end (≈3:1)**
![TBS-001 Walkway — Sheet 3: Ceiling-Hung Support](assets/walkway-sheet3.png)

**Sheet 4 — Detail B: Left walkway removable lift-out resting on butt joint (≈2:1)**
![TBS-001 Walkway — Sheet 4: Lift-Out at Butt Joint](assets/walkway-sheet4.png)

**Sheet 5 — Detail C: Left walkway support system — bearer beam, floor legs, bearing strip (≈3.5:1)**
![TBS-001 Walkway — Sheet 5: Support System Detail](assets/walkway-sheet5.png)

**Sheet 6 — Detail D: Bearer beam anti-slip restraint — lip pocket, lock block with slotted bolt (≈4:1)**
![TBS-001 Walkway — Sheet 6: Bearer Beam Connection](assets/walkway-sheet6.png)

---

## 15. IBC Stacking & Securing

2×2 IBC stack in the right end zone (X=4,674–5,893mm). Four 600L Schutz Ecobulk
MX totes held in a welded 50×50×3mm RHS mild steel stacking frame with D-ring
lashing points, anti-rotation lip, and removable access gates.
Source report: [Equipment Layout](equipment-layout-report.md) §5,
[Water System](water-system-report.md) §5.

**Sheet 1 — Cross-section elevation (looking along X): 2-tier stack, frame, D-rings, ceiling clearance**
![TBS-001 IBC Stacking — Sheet 1: Cross-Section Elevation](assets/ibc-stacking-sheet1.png)

**Sheet 2 — Fastening details: D-ring lashing, anti-rotation lip, access gate, strap routing**
![TBS-001 IBC Stacking — Sheet 2: Fastening Details](assets/ibc-stacking-sheet2.png)

**Sheet 3 — External plumbing panel elevation: View from outside the container sealed end wall. 3× 2" NPT bulkhead unions stacked vertically on container centerline — fill port X1 (Blue IBC-1 at 2,250mm) above IBC tops for gravity feed (IBC-2 self-levels via 2" cross-connect), drain ports X3 (Brown IBC-3 at 400mm) and X4 (Waste IBC-4 at 200mm) at bottom. Reinforcing plate, camlock fittings, height dimensions**
![TBS-001 IBC Stacking — Sheet 3: External Plumbing Panel Elevation](assets/ibc-stacking-sheet3.png)

**Sheet 4 — Internal plumbing plan view with IBC layout: Looking down at IBC zone showing 4 IBCs in 2×2 arrangement (top tier solid, bottom tier dashed), portal frame structure, D-ring lashing points, 270mm central plumbing corridor. IBC valve faces point toward corridor (DN50 butterfly valve, S60×6 thread). X1 fill pipe routes from end-wall bulkhead through corridor to IBC-1. 2" cross-connect between IBC-1 and IBC-2 (self-leveling, no valve). Ball valves (V1/V3/V4) at IBC connections. Equipment panel with pumps and filters. All internal pipes 1" HDPE SDR-11**
![TBS-001 IBC Stacking — Sheet 4: Internal Plumbing Plan View](assets/ibc-stacking-sheet4.png)

**Sheet 5 — Internal plumbing elevation: View from inside the container looking at the sealed end wall. Shows 3 bulkhead unions (X1/X3/X4) on centerline with pipe routing to flanking IBCs. X1 fill pipe routes horizontally from upper bulkhead through corridor, drops through IBC-1 fill cap (DN150). 2" cross-connect between IBC-1 and IBC-2 at valve height (self-leveling, no valve). Drain pipes (X3/X4) connect at IBC DN50 butterfly valves (~185mm above floor, corridor-facing), rise to bulkhead height, route horizontally to wall. Blue outflow manifold (VB1/VB2 → tee → VB3 → P-01). P-03 waste evacuation pump on X4**
![TBS-001 IBC Stacking — Sheet 5: Internal Plumbing Elevation](assets/ibc-stacking-sheet5.png)

---

## 16. Optical Line-of-Sight Clearance

Two-panel optical clearance diagram. Confirms which equipment items fall within the
optical cone from the pinhole (X=2946mm, H=1194mm) to the film plane (depth=2262mm).
Equipment items intersecting the cone are highlighted as potential shadow sources.
See [Construction Guide](pinhole-camera-construction.md) §4 for layout context.

![TBS-001 — Optical Line-of-Sight Clearance](assets/line-of-sight.png)

---

## 17. IBC Support Frame Fabrication

Welded 50×50×3mm RHS mild steel stacking frame for the 2×2 IBC stack in the
right end zone. Portal spine along the 270mm plumbing corridor with cantilever
platform beams, X-bracing, wall brackets, D-ring lashing points, anti-rotation
lip, and removable access gates. Frame only — no IBCs or other components shown.
Source report: [Equipment Layout](equipment-layout-report.md) §5,
[Water System](water-system-report.md) §5.

**Sheet 1 — Front elevation (looking along X toward sealed end wall): Full container width showing corridor uprights (×6, 3 per side), three levels of transverse beams (base/platform/top), wall brackets with M12 anchor bolts and gusset plates, anti-rotation lip (5mm × 40mm plate), D-ring lashing points (×8, WLL 1,100 kg), access gates (×2, 300mm × 916mm clear)**
![TBS-001 IBC Frame — Sheet 1: Front Elevation](assets/ibc-frame-sheet1.png)

**Sheet 2 — Side elevation (looking along Yd from near wall): Frame depth (1,284mm) showing three upright bays at 642mm centers, longitudinal beams at three levels, X-bracing in bottom-tier bays for racking resistance, D-ring positions, access gate outline**
![TBS-001 IBC Frame — Sheet 2: Side Elevation](assets/ibc-frame-sheet2.png)

**Sheet 3 — Plan view at platform level (Z=1,060mm): Beam layout in cross-section showing longitudinal corridor beams, transverse cantilever beams, corridor opening, wall bracket positions and bolt pattern, anti-rotation lip perimeter, rubber mat positions. Detail A: typical welded corner joint (≈5:1). Detail B: D-ring lashing point mounting (≈4:1)**
![TBS-001 IBC Frame — Sheet 3: Plan View](assets/ibc-frame-sheet3.png)

---

## 18. Equipment Panel — IBC Corridor Mounting

Front elevation of the 18mm marine plywood equipment panel spanning the 270mm IBC
plumbing corridor (Yd=1,046–1,316), perpendicular to the sealed end wall at X=5,000.
All pumps, filters, accumulator, diverter valve, and isolation valves mount on this
panel. Full plumbing routing shown with pipe crossings, gap-breaks, and flow arrows.
Cross-section strip shows panel/walkway/wall relationship. Detail B: filter mounting.

Source reports: [Water System](water-system-report.md) §3,
[Equipment Layout](equipment-layout-report.md) §4.

![TBS-001 — Equipment Panel Layout](assets/panel-layout.png)

---

### 19. Spray Bar Assembly — Sheet 1: Gantry Elevation

X-Z gantry elevation viewed from the film plane showing the full beam span
(40×40×3mm AL SHS with 1" PVC pipe inside), BV-02 ball valve on the pinhole
wall at waist height, flex hose to center feed, telescoping pole through a
30mm walkway slit, and operator silhouette. 4× vertical exaggeration.

Source report: [Water System](water-system-report.md) §6.

![TBS-001 — Spray Bar Gantry Elevation](assets/spray-bar-sheet1.png)

---

### 20. Spray Bar Assembly — Sheet 2: Cross Section

Composite Yd-Z cross section looking along X at 1:1 scale, combining carriage
mechanics (Ø50mm nylon wheels, fork brackets, L-bracket, U-clamp), ball joint
arm attachment, and handle tube with zip-tied hose.

![TBS-001 — Spray Bar Cross Section](assets/spray-bar-sheet2.png)

---

### 21. Spray Bar Assembly — Sheet 3: Plan View

Container floor plan (X-Yd, looking down) showing walkway positions, slit
locations on near and far walkways for pole passage, beam example position,
and travel range.

![TBS-001 — Spray Bar Plan View](assets/spray-bar-sheet3.png)

---

### 22. Spray Bar Assembly — Sheet 4: Detail A — Beam End

Longitudinal section at 2:1 scale through the open beam end showing 1" PVC
pipe extending past the AL SHS, socket cap solvent-welded to pipe end, and
engagement dimensions.

![TBS-001 — Spray Bar Detail A](assets/spray-bar-sheet4.png)

---

### 23. Spray Bar Assembly — Sheet 5: Detail C — Wheel Attachment

Section along axle centerline at 2:1 scale showing fork bracket arms, nylon
wheel bore, Ø10mm axle pin, snap-ring retention, and M5 through-bolt
connection to L-bracket horizontal arm.

![TBS-001 — Spray Bar Detail C](assets/spray-bar-sheet5.png)

---

### 24. Spray Bar Assembly — Sheet 6: Detail D — Wheel Plan

Plan view (X-Yd, looking down) of the carriage showing beam, L-bracket arm,
U-clamp with flared legs, fork brackets, and Ø50mm nylon wheel footprints
with 200mm spacing.

![TBS-001 — Spray Bar Detail D](assets/spray-bar-sheet6.png)
