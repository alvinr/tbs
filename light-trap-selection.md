<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Revolving Light Trap — Selection & Specification
## TBS-001 Hinged Panel Integration

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*

---

## 1. Context

The cargo door end of TBS-001 is sealed by a hinged panel (2,362mm wide × 2,388mm tall, 50×50mm RHS steel frame, 18mm ply skins). The panel swings 180° outward to clear the full door opening for loading IBC totes and equipment. When closed it is light-sealed at the perimeter by a 20mm EPDM compression gasket.

Personnel access during operation is via a revolving light trap drum built into the panel. Operators can enter or exit at any time without opening the full panel or admitting daylight.

**Sheet 1 — Front Elevation (1:20): Panel Dimensions, Drum, Hinges, Latches (interior face)**
![TBS-001 Hinged Panel — Sheet 1: Front Elevation](assets/hingepanel-sheet1.png)

**Sheet 2 — Plan Cross-Section (1:10 horiz / 1:1 depth): Drum Baffles and S-Path Light Route**
![TBS-001 Hinged Panel — Sheet 2: Plan Cross-Section](assets/hingepanel-sheet2.png)

**Sheet 3 — Drum Vertical Section Elevation (Section A-A): Walking-height orientation confirmation**
![TBS-001 Hinged Panel — Sheet 3: Drum Elevation](assets/hingepanel-sheet3.png)

Full drawings also appear in the [Engineering Diagrams](engineering-diagrams.md) §12.

---

## 2. Requirements

| Requirement | Value |
|-------------|-------|
| Clear passage diameter | ≥ 700mm (minimum comfortable single-person access) |
| Clear passage height | ≥ 1,900mm (full headroom) |
| Light exclusion | 100% — no straight-line optical path from exterior to interior |
| Durability | Repeated field deployment, transport vibration, outdoor exposure |
| Operability | Single operator, no tools required to enter/exit |
| Mounting | Flush-mounted into 120mm panel opening — no permanent wall surround |
| Weatherproofing | Drum top and bottom sealed against rain ingress during setup |

---

## 3. Commercial Options Evaluated

Three categories of commercial product were reviewed against these requirements.

### 3.1 Vario / Octanorm Revolving Darkroom Door

| Parameter | Value |
|-----------|-------|
| Typical product | Vario LT-800, Kaiser RD-800, Kindermann equivalents |
| Clear diameter | 800mm |
| Height | 2,000–2,200mm |
| Approximate price | USD $2,500–$3,500 (import from DE/NL; shipping +$400) |
| Lead time | 4–8 weeks |

**Construction:** Aluminum extrusion frame, ABS drum panels, felt drum seals, floor-mounted bearing with ceiling guide. Designed for permanent installation in a finished interior wall with a framed rectangular opening.

**Assessment — Not recommended for TBS-001.**

The Vario/Kaiser/Kindermann range is designed for permanent darkroom installation in climate-controlled interiors. Key issues for field use:
- **No weatherproofing.** The top gap between drum and ceiling guide is sealed by felt strip only. In outdoor use (rain, dust, wind) this seal fails within one season.
- **Floor bearing.** The base bearing is a stub pivot set into a floor-mount plate anchored to a finished floor. It cannot be adapted to a free-swinging 120mm panel with repeated installation/removal.
- **Transport.** The drum (ABS/aluminum construction) is not rated for transport vibration. The bearing races and alignment tolerances assume static installation.
- **Frame dependency.** The drum relies on its surrounding wall frame for structural rigidity. Removed from that frame, the drum has no self-contained structural integrity.

### 3.2 Porta-Fab Modular Darkroom Panel System

| Parameter | Value |
|-----------|-------|
| Product | Porta-Fab DK series modular panels with revolving door unit |
| Clear diameter | 750–900mm (model-dependent) |
| Height | 2,000mm |
| Approximate price | USD $3,000–$4,500 (direct from supplier; custom spec required) |
| Lead time | 6–10 weeks |

**Construction:** Modular steel-framed panels with light-sealed joining extrusions. The revolving door unit is a self-contained drum on a floor bearing, designed to fit a standard panel-bay opening.

**Assessment — Not recommended for TBS-001.**

The Porta-Fab system is modular and more robust than the Vario range, but shares the same fundamental limitations:
- **Cost.** At $3,000–$4,500 for the revolving unit alone, it represents the highest-cost option with no field-durability advantage over custom fabrication.
- **Panel integration.** Porta-Fab drums are designed to fit a standard panel-bay frame (100mm depth). Our panel is 120mm thick — an adapter would be required, adding cost and leak risk.
- **Drum seals.** Top and bottom felt seals, identical in design to the Vario range. Not suitable for outdoor conditions.
- **Bearing.** Stub-shaft floor pivot identical to Vario — not suitable for a removable panel.

### 3.3 Custom Fabrication — Recommended

| Parameter | Value |
|-----------|-------|
| Drum outer diameter | 750mm |
| Drum height | 2,200mm (floor to upper bearing) |
| Wall thickness | 3mm mild steel sheet, formed and welded |
| Surface finish | Shot-blast + flat black powder coat (interior); grey oxide primer (exterior) |
| Baffles | 4 × internal steel fins, 3mm × full height, at 45° angular offset |
| Top bearing | SKF 6215 sealed deep-groove ball bearing on 75mm stub shaft, welded to drum |
| Bottom bearing | SKF 6215 sealed, stub shaft into floor-mount collar, panel-bolted |
| Drum seals (top/bottom) | Two-layer: closed-cell neoprene wiper + silicone bead — IP44 rated |
| Handle | 100mm Ø SS grab rail, interior face only, at 900mm height |
| Finish | Interior: flat black RAL 9005; exterior drum face: grey oxide |
| Approximate cost | USD $800–$1,500 (local metal fabrication shop) |
| Lead time | 2–3 weeks |

**Assessment — Recommended.**

Custom fabrication from 3mm mild steel is the correct choice for a field-deployed, transport-rated camera system. Every specification can be set to exactly what is required — clear bore, panel thickness interface, bearing grade, seal type, drum height. A 3mm steel drum is structurally rigid as a freestanding cylinder without a surrounding wall frame, and can be bolted into the panel opening on 8 × M10 flush bolts.

The SKF 6215 sealed bearing is rated for radial loads to 52.7 kN and operates at 0–120°C — far beyond any field requirement. The neoprene/silicone top seal provides IP44 protection against splash and rain ingress. The flat black powder-coat interior is optically dead at visible wavelengths.

---

## 4. Recommended Specification — Custom Drum

### 4.1 Drum Body

| Item | Specification |
|------|--------------|
| Drum shell | 3mm mild steel, rolled to Ø750mm OD, seam-welded full height |
| Drum height | 2,200mm |
| Internal baffles | 4 × 3mm mild steel fins, welded radially from drum centerline to inner wall, at 22.5°/112.5°/202.5°/292.5° from horizontal — see Sheet 2 for baffle layout and light path |
| Top cap | 5mm steel plate, flanged, welded |
| Bottom cap | 5mm steel plate, flanged, with 75mm stub shaft for lower bearing |
| Upper stub shaft | 75mm Ø × 150mm steel stub, welded to top cap centre |
| Surface treatment | Interior: shot-blast + flat black powder coat; exterior: grey oxide primer + grey topcoat |

### 4.2 Bearings and Mounting

| Item | Specification |
|------|--------------|
| Bearings (×2) | SKF 6215-2RS1 (75mm ID, 130mm OD, 25mm wide, sealed, C3 clearance) |
| Upper bearing mount | Welded steel housing bolted to panel top rail |
| Lower bearing mount | Welded steel floor collar, 8 × M10 bolts into panel bottom rail |
| Axial retention | Circlip on stub shaft each side |

### 4.3 Seals

| Item | Specification |
|------|--------------|
| Top seal | 12mm closed-cell neoprene wiper strip bonded to top cap underside + silicone bead seal against ceiling mount plate |
| Bottom seal | 12mm closed-cell neoprene wiper strip bonded to bottom cap underside + silicone bead seal against floor mount plate |
| Drum-to-panel gap | 15mm radial clearance, closed by 20mm neoprene compression strip bonded to panel drum aperture |

### 4.4 Hardware

| Item | Specification |
|------|--------------|
| Entry handle | 100mm Ø × 400mm SS round grab rail, interior face only, at 900mm height — welded bracket, no through-hole in drum wall |
| Panel bolts | 8 × M10 flush-head hex bolts (lower collar) + 6 × M10 (upper housing), stainless |

### 4.5 Raw Material Suppliers (US / SoCal)

| Item | Supplier | Part / Notes |
|------|----------|-------------|
| 3mm mild steel sheet (1,200 × 2,400mm) | Pacific Coast Steel — Santa Fe Springs CA | Hot-rolled A36; price ~$80/sheet; 2 sheets required |
| SKF 6215-2RS1 bearing (×2) | Bearing World — Anaheim CA; or Applied Industrial Technologies | ~$45–$65 each |
| 75mm × 150mm steel stub shaft (×2) | Pacific Coast Steel or any steel service centre | 75mm Ø solid round bar, cut to length |
| Closed-cell neoprene strip 12mm (3m) | McMaster-Carr #93855K6 | Closed-cell, pressure-sensitive adhesive back; ~$22 |
| Silicone bead sealant | McMaster-Carr #7587A3 or equivalent | Black, UV-stable |
| SS grab rail 100mm Ø (×1) | McMaster-Carr #4530T37 | 1" nominal; 400mm cut to length; interior face only |
| Flat black powder coat | Local powder coat shop | Standard service; ~$150 for drum |
| Metal fabrication (rolling, welding, fitting) | Estimate 16–20 hrs labour at local shop | $800–$1,200 depending on shop rate |

**Total custom drum estimate: $950–$1,450.**

---

## 5. Light Path Verification

The 4-baffle arrangement eliminates any straight-line path from exterior to interior. To verify:

A ray entering at any point on the exterior drum face must rotate at least 45° (one baffle sector) before exiting on the interior face. At 750mm drum diameter and 4 baffles at 45° offset, the shortest possible S-path through the drum is 590mm — significantly longer than the 120mm panel thickness, ensuring no line of sight is possible at any incidence angle within ±30° of normal incidence.

See Sheet 2 of the hinged panel engineering drawings for the baffle cross-section and S-path trace.

---

## 6. Comparison Summary

| | Vario LT-800 | Porta-Fab DK | **Custom (recommended)** |
|---|---|---|---|
| Clear diameter | 800mm | 750–900mm | **750mm** |
| Height | 2,000–2,200mm | 2,000mm | **2,200mm** |
| Price (USD) | $2,500–$3,500 | $3,000–$4,500 | **$950–$1,450** |
| Weatherproofing | None | None | **IP44 (neoprene/silicone)** |
| Panel integration | Requires surround wall | Requires panel-bay frame | **Direct bolt-in (120mm panel)** |
| Transport-rated | No | No | **Yes (3mm steel, sealed bearings)** |
| Lead time | 4–8 weeks | 6–10 weeks | **2–3 weeks** |
| Field repairability | Low (ABS/extrusion parts) | Low | **High (standard steel + off-shelf bearings)** |
| **Recommendation** | ✗ | ✗ | **✓** |

Custom fabrication saves $1,550–$3,050 over commercial alternatives while providing superior weatherproofing, transport durability, and field repairability.

---

## 7. Integration Notes

- The drum is installed into the hinged panel before the panel is hung. Panel + drum combined weight: approximately 220–260kg — requires two people and a panel hoist or engine crane for hanging.
- The lower bearing collar is bolted to the panel bottom rail with 8 × M10 stainless bolts. The upper bearing housing is bolted to the panel top rail with 6 × M10. Both connections can be disassembled with standard hex keys for maintenance.
- The drum rotates freely in both directions; there is no rotation limit. The exterior face carries no handle — the operator pushes the bare drum wall to enter. An interior grab rail (100mm Ø SS, welded bracket, no through-hole) at 900mm height allows the operator to pull the drum closed from inside and brace during exit. This eliminates any through-bolt penetration of the drum wall on the exterior face, removing a potential light leak path.
- Interior safelight (Circuit D, per [Electrical Report](electrical-report.md)) illuminates the drum interior during loading operations, allowing operators to orient themselves in darkness.
- **Panel latches (×4 Southco C2-33 cam compression latches) are mounted on the interior face of the panel.** This is a deliberate safety design: if the revolving drum jams and prevents normal egress, an operator inside the container can release all four latches independently from the inside and push the panel open outward. The panel swings 180° on its left-edge hinges, clearing all interior equipment. Latches appear as hidden (dashed) features in the exterior elevation drawing (Sheet 1).
