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

High-level schematic side-elevation of the container interior showing how all systems
relate spatially. Color-coded by subsystem. Optical axis is perpendicular to the page.

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

Four-corner independent actuation mechanism (TBS-FM01).
Source report: [Film Plane Mechanism](film-plane-mechanism-report.md).

**Sheet 1 — Assembly overview**
![TBS-001 Film Plane Mechanism — Sheet 1](assets/film-plane-sheet1.png)

**Sheet 2 — Corner assembly detail**
![TBS-001 Film Plane Mechanism — Sheet 2](assets/film-plane-sheet2.png)

**Sheet 3 — Drive shaft and handwheel**
![TBS-001 Film Plane Mechanism — Sheet 3](assets/film-plane-sheet3.png)

**Sheet 4 — Full mechanism cross-section**
![TBS-001 Film Plane Mechanism — Sheet 4](assets/film-plane-sheet4.png)

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

---

## 10. Electrical & Power

12V DC power architecture, circuit layout, and system controls.
Source report: [Electrical & Systems](electrical-report.md).

**Sheet 1 — Power distribution and circuit diagram**
![TBS-001 Electrical — Sheet 1](assets/electrical-sheet1.png)

**Sheet 2 — Wiring layout and component positions**
![TBS-001 Electrical — Sheet 2](assets/electrical-sheet2.png)

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
bracket arm + 25mm grate). No legs, no beam, no floor contact — entire tray interior
completely clear for film loading.

Mounting varies by wall type:

- **Near/far walkways** (long walls): 8mm steel plate triangular gusset brackets bolted
  to corrugated wall structural ribs at 457mm (18") centers.
- **Right walkway** (far end wall): same brackets bolted to 50×50×5mm angle iron
  mounting rail welded along the flat end wall interior (no corrugation ribs).
- **Left walkway** (cargo door end): removable lift-out section with no brackets.
  The hinged panel occupies this end wall and slides 300mm inward for transport —
  left walkway must be removed first. Supported at each end by near/far walkway
  miter corners. Heavy-duty grating (40×5mm bars) spans the 1,762mm unsupported gap.

**Sheet 1 — Cross-section through near walkway: Grate, cantilever bracket, tray rim clearance (≈5:1)**
![TBS-001 Walkway — Sheet 1: Cross-Section](assets/walkway-sheet1.png)

**Sheet 2 — Plan view: All 4 sections with bracket positions and panel transport envelope**
![TBS-001 Walkway — Sheet 2: Plan View](assets/walkway-sheet2.png)

**Sheet 3 — Detail A: Near/far bracket through-bolted to corrugated wall rib (≈3:1)**
![TBS-001 Walkway — Sheet 3: Corrugated Wall Bracket](assets/walkway-sheet3.png)

**Sheet 4 — Detail B: Right walkway bracket on angle iron welded to flat end wall (≈3:1)**
![TBS-001 Walkway — Sheet 4: Angle Iron Bracket](assets/walkway-sheet4.png)

**Sheet 5 — Detail C: Left walkway removable lift-out resting on butt joint (≈2:1)**
![TBS-001 Walkway — Sheet 5: Lift-Out at Butt Joint](assets/walkway-sheet5.png)

---

## 15. Optical Line-of-Sight Clearance

Two-panel optical clearance diagram. Confirms which equipment items fall within the
optical cone from the pinhole (X=2946mm, H=1194mm) to the film plane (depth=2262mm).
Equipment items intersecting the cone are highlighted as potential shadow sources.
See [Construction Guide](pinhole-camera-construction.md) §4 for layout context.

![TBS-001 — Optical Line-of-Sight Clearance](assets/line-of-sight.png)
