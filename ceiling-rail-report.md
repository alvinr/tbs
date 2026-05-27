<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Ceiling Rail Suspension System
## TBS-001 — Panel Suspension & Transport Slide

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*

---

## 1. Purpose

The hinged light-trap panel must slide 300 mm in the X direction for transport mode
conversion (retracting the revolving drum behind the container door closure plane).
The permanently installed processing tray (304 SS, 50 mm rim) occupies the floor of
the optical zone from X=170 to X=4,629 mm and cannot be removed for each conversion.
The ceiling rail suspension system solves this by hanging the panel from
ceiling-mounted HGR20 linear rails, maintaining an 80 mm gap between the panel bottom
edge and the container floor — clearing the 50 mm tray rim with 30 mm margin.

**Design goals:**

- Support the full panel mass (~180 kg) from the ceiling
- Provide 300 mm X-direction slide travel for transport mode conversion
- Maintain 80 mm floor gap — clearing the 50 mm processing tray rim at all positions
- Zero floor contact — the panel never touches the tray or walkway during slide
- Single-person operation (~5 minutes for full mode conversion)
- Safety factor >10× on all suspension components

---

## 2. System Architecture

### 2.1 Rail Layout

Two HGR20 linear rails are mounted to the container ceiling, one on each side wall
line (Yd ≈ 30 mm near wall, Yd ≈ 2,332 mm far wall). Each rail runs in the
X direction along the ceiling surface at Z=2,388 mm.

| Parameter | Value |
|-----------|-------|
| Rail model | HGR20 (20 mm profile linear guide rail) |
| Rail length | 500 mm |
| Quantity | 2 (near wall + far wall) |
| Mounting height | Z=2,388 mm (container ceiling surface) |
| Rail profile height | 30 mm |
| Rail profile width | 20 mm |
| Mounting | 6 mm steel plate welded to ceiling; rail bolted to plate with M8 hex bolts |

### 2.2 Carriage Blocks

| Parameter | Value |
|-----------|-------|
| Carriage model | HGH20CA (flanged carriage block) |
| Quantity | 4 (2 per rail) |
| Block height | 28 mm |
| Block width | 44 mm |
| Dynamic load rating | 12.7 kN per block |
| Static load rating | 26.5 kN per block |
| Travel | 300 mm (operational ↔ transport) |

### 2.3 Suspension Brackets

Each carriage block connects to the panel top rail via a fabricated mild steel
suspension bracket.

| Parameter | Value |
|-----------|-------|
| Material | 10 mm mild steel plate, folded to inverted-U profile |
| Width | 60 mm |
| Height | 40 mm |
| Quantity | 4 (one per carriage block) |
| Top plate | Bolted to carriage block underside (2× M8 hex bolts) |
| Side plates | 8 mm vertical legs, bolted to panel top rail (2× M10 hex bolts) |

### 2.4 Assembly Stack

From ceiling down, the suspension assembly stacks as follows:

| Layer | Component | Thickness (mm) |
|-------|-----------|---------------|
| 1 | Container ceiling (1.6 mm Corten steel) | 1.6 |
| 2 | Mounting plate (6 mm steel, welded to ceiling) | 6 |
| 3 | HGR20 rail | 30 |
| 4 | Ball bearing gap | 2 |
| 5 | HGH20CA carriage block | 28 |
| 6 | Suspension bracket | 40 |
| 7 | Bolt clearance gap | 5 |
| — | **Total suspension depth** | **~112 mm** |

The panel top edge begins at Z ≈ 2,276 mm (2,388 − 112), and the panel body
extends downward to the floor gap at Z=80 mm — giving a panel height of ~2,196 mm.

---

## 3. Mounting Detail

### 3.1 Ceiling Attachment

The HGR20 rail cannot bolt directly through the 1.6 mm Corten steel ceiling
corrugation — it would buckle under load. Instead, a 6 mm mild steel mounting
plate is continuously fillet-welded to the ceiling surface, spanning at least
two corrugation ribs. The rail bolts to this plate.

| Parameter | Value |
|-----------|-------|
| Plate material | 6 mm A36 mild steel |
| Plate dimensions | 80 × 500 mm (width × length, matching rail) |
| Weld | Continuous 4 mm fillet weld on both long edges to ceiling |
| Rail fasteners | 4× M8 × 30 mm hex bolts per rail, through plate into ceiling structure |
| Thread engagement | M8 tapped into plate (min. 12 mm engagement) |

### 3.2 Panel Connection

The bracket side plates bolt to the panel top rail (50 × 50 × 3 mm RHS mild
steel frame). Bolt holes are drilled through the bracket side plates and the
panel frame top rail.

| Parameter | Value |
|-----------|-------|
| Fasteners | 4× M10 × 35 mm hex bolts per bracket (2 per side plate) |
| Thread engagement | Through-bolt with nyloc nut |
| Hole clearance | 11 mm clearance hole in bracket, 11 mm in panel rail |

---

## 4. Load Analysis

### 4.1 Panel Mass

| Component | Mass (kg) |
|-----------|----------|
| Panel structure (frame + plywood skins) | ~100 |
| Revolving drum + baffles + bearings | ~60–80 |
| **Total panel mass** | **~180** |

### 4.2 Carriage Load Distribution

The panel hangs from 4 carriage blocks (2 per rail). Assuming equal load sharing:

| Parameter | Value |
|-----------|-------|
| Total gravitational load | 180 kg × 9.81 m/s² = 1,766 N |
| Load per block | 1,766 / 4 = 441 N |
| HGH20CA dynamic rating | 12,700 N per block |
| **Safety factor per block** | **12,700 / 441 = 28.8×** |

Even with unequal loading (worst case: 2 blocks carrying 70% of the load), the
safety factor remains above 15×. The HGR20/HGH20CA system is conservatively
oversized for this application.

### 4.3 Ceiling Plate Weld

The 4 mm continuous fillet weld along both long edges of each 500 mm mounting
plate has a throat area of approximately 2,800 mm². At a conservative 100 MPa
shear allowable for E70XX electrode on A36 plate, each plate sustains ~280 kN —
far exceeding the 883 N half-panel load it carries. The Corten ceiling itself
is stiffened by corrugation ribs at 100–150 mm spacing, preventing local
buckling under the distributed plate load.

---

## 5. Clearance Analysis

### 5.1 Critical Dimensions

| Dimension | Value (mm) | Source |
|-----------|-----------|--------|
| Container floor to ceiling (Z range) | 0–2,388 | Interior height |
| Panel bottom edge (Z) | 80 | PANEL_FLOOR_GAP |
| Processing tray rim top (Z) | 50 | PROC_TRAY_RIM |
| **Clearance: panel bottom to tray rim** | **30** | 80 − 50 |
| Tray left edge (X) | 170 | PROC_TRAY_X_L |
| Panel outer face in transport (X) | 300 | PANEL_SLIDE |
| Panel inner face in transport (X) | 420 | 300 + 120 (PANEL_CENTER_T) |

### 5.2 Overlap Zone

In the transport position (panel slid 300 mm inward), the panel center zone
(120 mm thick) occupies X=300–420 mm. The processing tray starts at X=170 mm.
The horizontal overlap is therefore 250 mm (420 − 170). In this overlap zone,
the vertical clearance between the panel bottom edge (Z=80 mm) and the tray
rim (Z=50 mm) is the critical 30 mm gap.

This 30 mm margin accommodates:

- Container floor deflection under load (±3 mm typical)
- Rail/carriage manufacturing tolerance (±0.5 mm)
- Panel hang plumb tolerance (±2 mm)
- Tray rim flatness tolerance (±1 mm)

### 5.3 Left Walkway Interaction

The left walkway (removable lift-out section) has a deck height of 100 mm at
X=170 mm — above the panel bottom edge at Z=80 mm. The left walkway must be
removed before the panel slides to the transport position; otherwise the panel
edge would collide with the walkway grating.

**Operating procedure:** Lift out the left walkway section before sliding the
panel inward. Replace the walkway after sliding the panel back to the
operational position. See [Walkway System](walkway-report.md) §5 for lift-out
procedure.

---

## 6. Panel Positions

| Position | Panel corner inner face X (mm) | Drum exterior edge X (mm) | Tray clearance | Container doors clear? |
|----------|-------------------------------|--------------------------|---------------|----------------------|
| Operational (X=0) | 40 | −295 | N/A — panel outboard of tray | No (drum protrudes 295 mm) |
| Transport (X=300) | 340 | +5 | 30 mm vertical gap | Yes (drum clears by 5 mm) |

### 6.1 Locking

| Lock position | Method | Quantity |
|--------------|--------|---------|
| Operational (X=0) | Destaco 207-U toggle clamp | 2 |
| Transport (X=300) | Destaco 207-U toggle clamp | 2 |

The toggle clamps are mounted to the fixed door frame and engage keepers on
the panel frame at both end-of-travel positions.

---

## 7. Fixed Door Frame Interface

The HGR20 rails pass through the fixed welded door frame (50 × 50 × 3 mm RHS
at X=0) at ceiling level on both walls. Each rail penetration is a slot
machined into the top rail of the door frame, sized for the rail profile plus
2 mm clearance on each side.

| Parameter | Value |
|-----------|-------|
| Door frame material | 50 × 50 × 3 mm RHS mild steel |
| Rail slot size | 24 × 34 mm (rail 20 × 30 mm + 2 mm clearance each side) |
| Light seal | 10 mm closed-cell neoprene compression pad (50 × 30 mm) bonded to frame face around each rail penetration |
| Seal engagement | Carriage block housing compresses against pad when panel locked at X=0 |

---

## 8. EPDM Perimeter Seal

When the panel is locked at the operational position (X=0), the 20 mm EPDM
perimeter gasket on the panel compresses against the fixed door frame,
providing a light-tight seal. The ceiling rail suspension allows the panel to
float on the carriage blocks, self-aligning against the seal landing surface
as the cam latches draw the panel tight.

The seal is not engaged during transport mode — the panel is retracted 300 mm
from the door frame. Light sealing is not required during transport or loading.

---

## 9. Engineering Drawings

Two construction drawings cover the ceiling rail suspension system:

**Sheet 1 — Side elevation cross-section: Panel suspended from ceiling rail, operational and transport positions, processing tray clearance**
![TBS-001 Ceiling Rail — Sheet 1: Side Elevation](assets/ceiling-rail-sheet1.png)

**Sheet 2 — Detail view (≈2:1): Rail/carriage/bracket assembly, mounting plate, ball bearings, panel connection**
![TBS-001 Ceiling Rail — Sheet 2: Rail Detail](assets/ceiling-rail-sheet2.png)

Full drawings also appear in [Engineering Overview](engineering-diagrams.md) §13.

---

## 10. Parts List

| Item | Specification | Qty | Est. cost (USD) |
|------|--------------|-----|----------------|
| HGR20 linear guide rail, 500 mm | 20 mm profile, hardened steel | 2 | $40–$55 |
| HGH20CA carriage block | Flanged, sealed, preloaded | 4 | $60–$90 |
| 6 mm A36 steel plate (80 × 500 mm) | Mounting plate, welded to ceiling | 2 | $15–$25 |
| 10 mm mild steel plate | Suspension bracket blanks (cut + fold) | 4 | $20–$30 |
| M8 × 30 hex bolt (grade 8.8) | Rail-to-plate fasteners | 8 | $8–$12 |
| M8 × 25 hex bolt (grade 8.8) | Carriage-to-bracket fasteners | 8 | $8–$12 |
| M10 × 35 hex bolt (grade 8.8) + nyloc nut | Bracket-to-panel fasteners | 8+8 | $12–$18 |
| Destaco 207-U toggle clamp | Position locks (operational + transport) | 4 | $60–$100 |
| 10 mm neoprene pad (50 × 30 mm) | Rail penetration light seals | 4 | $8–$12 |
| Welding (fillet weld, mounting plates to ceiling) | 2× 1 m continuous fillet weld | — | $60–$100 |
| **Total** | | | **$291–$454** |

---

## 11. Maintenance Schedule

| Interval | Task |
|----------|------|
| Every mode conversion | Visually confirm panel bottom clears tray rim during slide |
| Every 20 conversions | Check Destaco toggle clamp engagement and spring tension at both positions |
| Every 6 months | Inspect neoprene rail penetration pads for compression set; replace if permanently deformed |
| Annually | Clean and re-lubricate HGR20 rails and HGH20CA carriage blocks per manufacturer specification (lithium grease) |
| Annually | Inspect suspension bracket bolts (M8 + M10) for torque — retorque to spec if loosened |
| Annually | Check mounting plate welds for cracks (visual inspection) |
| Every 2 years | Replace neoprene rail penetration pads regardless of condition |
| As needed | Replace carriage blocks if bearing roughness detected during slide |

---

## 12. Sources

| Item | Source |
|------|--------|
| HGR20 / HGH20CA linear guide system | [HIWIN equivalent](https://www.hiwin.com/linear-guideways/hg-series/) — generic 20 mm profile, 12.7 kN dynamic load rating per block |
| Destaco 207-U toggle clamp | [Destaco catalog](https://www.destaco.com/207-u.html) — horizontal hold-down clamp, 375 lb capacity |
| Neoprene compression pad | [McMaster-Carr](https://www.mcmaster.com/neoprene-rubber-sheets) — closed-cell, UV-stable, pressure-sensitive adhesive |
| Panel construction and mass estimate | See [Hinged Light-Trap Panel](hinged-panel-report.md) §2 and §5 |
| Processing tray specification | See [Processing Tray & Spray Bar](processing-tray-and-spray-bar.md) §2 |
| Left walkway lift-out procedure | See [Walkway System](walkway-report.md) §5 |
| Ceiling rail construction drawings | See [Engineering Overview](engineering-diagrams.md) §13 — Sheets 1–2 |
| Container ceiling structure | [ISO 668](https://www.iso.org/standard/76912.html) / [ISO 1496-1](https://www.iso.org/standard/59672.html) — Corten steel corrugated panel, 1.6 mm nominal |
