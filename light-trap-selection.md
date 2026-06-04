<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Revolving Light Trap — Selection & Specification

## 1. Purpose

Personnel access during operation is via a revolving light trap drum built into the panel. Operators can enter or exit at any time without opening the full panel or admitting daylight — for example, between coating of the photosensitive material, or while the exposure is being made.

The cargo door end of TBS-001 is sealed by a stepped hinged panel (2362mm wide × 2388mm tall, 50×50mm RHS steel frame, 18mm ply skins). The panel has a stepped profile: 40mm thick at the corner zones (Yd=0–653mm and Yd=1709–2362mm) and 120mm thick at the center zone (Yd=653–1709mm) where the Ø900 housed revolving-door light lock is permanently mounted. The panel swings 180° outward to clear the full door opening for loading IBC totes and equipment. When closed it is light-sealed at the perimeter by a 20mm EPDM compression gasket against a fixed welded door frame at X=0.

The entire panel slides ~500mm in the X direction on HGR20 linear rails mounted to both container walls at floor and ceiling level (4 rails, 8 carriage blocks). The left (hinge) side rides via a vertical carriage beam (60×60×3mm SHS, 2400mm tall); the right (latch) side rides directly on blocks attached to the panel frame. For transport, the panel slides inward ~500mm — clearing the container doors for closure. Single-person operation, ~5 minutes per mode conversion. See [Equipment Layout Report](equipment-layout-report.md) §6 for sliding carriage specification.

**Sheet 1 — Front Elevation (1:20): Panel Dimensions, Drum, Hinges, Latches (interior face)**
![TBS-001 Hinged Panel — Sheet 1: Front Elevation](assets/hingepanel-sheet1.png)

**Sheet 2 — Plan Cross-Section: Housed Revolving Door — Housing, Drum & Light-Tight Geometry**
![TBS-001 Hinged Panel — Sheet 2: Plan Cross-Section](assets/hingepanel-sheet2.png)

**Sheet 3 — Drum Vertical Section Elevation (Section A-A): Walking-height orientation confirmation**
![TBS-001 Hinged Panel — Sheet 3: Drum Elevation](assets/hingepanel-sheet3.png)

Full drawings also appear in the [Engineering Diagrams](engineering-diagrams.md) §12.

---

## 2. Requirements

| Requirement | Value |
|-------------|-------|
| Clear passage diameter | ≥ 700mm (minimum comfortable single-person access) |
| Clear passage height | ≥ 1900mm (full headroom) |
| Light exclusion | 100% — no straight-line optical path from exterior to interior |
| Durability | Repeated field deployment, transport vibration, outdoor exposure |
| Operability | Single operator, no tools required to enter/exit |
| Mounting | Flush-mounted into 120mm center zone of stepped panel — no permanent wall surround |
| Weatherproofing | Drum top and bottom sealed against rain ingress during setup |

---

## 3. Commercial Options Evaluated

Three categories of commercial product were reviewed against these requirements.

### 3.1 Vario / Octanorm Revolving Darkroom Door

| Parameter | Value |
|-----------|-------|
| Typical product | Vario LT-800, Kaiser RD-800, Kindermann equivalents |
| Clear diameter | 800mm |
| Height | 2000–2200mm |
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
| Height | 2000mm |
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
| Housing outer diameter | Ø900mm (fixed) + Ø864mm rotating drum, ~Ø850mm bore |
| Height | 2200mm (floor to upper bearing) |
| Wall thickness | 3mm mild steel sheet, formed and welded (housing + drum) |
| Surface finish | Shot-blast + flat black powder coat (interior); grey oxide primer (exterior) |
| Baffles | None — two 80° housing openings 180° apart + single-opening C-shell drum (see §4, §5) |
| Top bearing | SKF 6215 sealed deep-groove ball bearing on 75mm stub shaft, welded to drum |
| Bottom bearing | SKF 6215 sealed, stub shaft into floor-mount collar, panel-bolted |
| Drum seals (top/bottom) | Two-layer: closed-cell neoprene wiper + silicone bead — IP44 rated |
| Handle | 100mm Ø SS grab rail, interior face only, at 900mm height |
| Finish | Interior: flat black RAL 9005; exterior drum face: grey oxide |
| Approximate cost | USD $1,785–$2,460 (local metal fabrication shop) |
| Lead time | 2–3 weeks |

**Assessment — Recommended.**

Custom fabrication from 3mm mild steel is the correct choice for a field-deployed, transport-rated camera system. Every specification can be set to exactly what is required — clear bore, panel thickness interface, bearing grade, seal type, drum height. A 3mm steel drum is structurally rigid as a freestanding cylinder without a surrounding wall frame, and can be bolted into the panel opening on 8 × M10 flush bolts.

The SKF 6215 sealed bearing is rated for radial loads to 52.7 kN and operates at 0–120°C — far beyond any field requirement. The neoprene/silicone top seal provides IP44 protection against splash and rain ingress. The flat black powder-coat interior is optically dead at visible wavelengths.

---

## 4. Recommended Specification — Custom Housed Revolving Door (rev 8)

> Replaces the earlier Ø750mm drum with **internal baffles**, which failed both
> personnel-fit and rotation light-tightness. The light lock is now a **fixed
> housing + single-opening C-shell drum** (no fins) — light-tight by geometry.

### 4.1 Housing + Drum Body

| Item | Specification |
|------|--------------|
| Fixed housing shell | 3mm mild steel, rolled to **Ø900mm OD**, seam-welded full height; built into the panel center zone |
| Housing openings | Two, **80° arc each, 180° apart** (full height) — one facing the exterior, one facing the interior/walkway |
| Rotating drum | 3mm mild steel C-shell, **Ø864mm OD** (~Ø850mm bore), single **80° opening**, rotates inside the housing on a 15mm running gap |
| Internal baffles | **None** — light-tightness is by the fixed-housing geometry (openings <90°, 180° apart; see §5) |
| Drum/housing height | 2200mm |
| Top cap | 5mm steel plate, flanged, welded to the drum |
| Bottom cap | 5mm steel plate, flanged, with 75mm stub shaft for lower bearing |
| Upper stub shaft | 75mm Ø × 150mm steel stub, welded to drum top cap centre |
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
| 3mm mild steel sheet (1200 × 2400mm) | Pacific Coast Steel — Santa Fe Springs CA | Hot-rolled A36; price ~$80/sheet; 2 sheets required |
| SKF 6215-2RS1 bearing (×2) | Bearing World — Anaheim CA; or Applied Industrial Technologies | ~$45–$65 each |
| 75mm × 150mm steel stub shaft (×2) | Pacific Coast Steel or any steel service centre | 75mm Ø solid round bar, cut to length |
| Closed-cell neoprene strip 12mm (3m) | McMaster-Carr #93855K6 | Closed-cell, pressure-sensitive adhesive back; ~$22 |
| Silicone bead sealant | McMaster-Carr #7587A3 or equivalent | Black, UV-stable |
| SS grab rail 100mm Ø (×1) | McMaster-Carr #4530T37 | 1" nominal; 400mm cut to length; interior face only |
| Flat black powder coat | Local powder coat shop | Standard service; ~$150 for drum |
| Metal fabrication (rolling, welding, fitting) | Estimate 16–20 hrs labour at local shop | $800–$1,200 depending on shop rate |

**Total custom housing+drum estimate: $1,785–$2,460.**

---

## 5. Light Path Verification

The fixed-housing geometry eliminates any straight-line path from exterior to
interior **at every rotation angle**, and the open bore fits a single operator.

**Light-tightness.** The housing has two openings, each **80° of arc and 180°
apart**; the drum has a single **80° opening**. Because each opening is narrower
than 90° and the two housing openings are 180° apart, the drum opening can never
align with both housing openings simultaneously. So the housing's solid wall always
covers whichever opening the drum opening is not facing — daylight entering the bore
through the exterior opening is blocked by the drum's solid wall before reaching the
interior opening. **Enter:** exterior open, interior covered → light into the bore,
no exit. **Transit:** both housing openings covered → fully sealed. **Exit:**
exterior covered → no daylight enters.

**Access.** With no internal fins, the whole **~Ø850mm bore** is clear standing
space and the 80° opening gives a **~625mm passage** — meeting the §2 requirement
(≥700mm clear passage diameter; the bore is Ø850). Emergency egress remains the
whole panel swinging open.

See **Sheet 5** of the hinged-panel drawings (enter / transit / exit verification)
and [Hinged Panel Report](hinged-panel-report.md) §3.3 / §3.6.

> **Note.** This replaces the earlier Ø750 / 4-fin drum, whose static "S-path"
> argument did not survive the two operational realities (a person could not fit a
> 90° sector, and a finned drum with a person-sized opening bridged exterior and
> interior at the transit angles). The fixed housing resolves both.

---

## 6. Comparison Summary

| | Vario LT-800 | Porta-Fab DK | **Custom (recommended)** |
|---|---|---|---|
| Clear bore / passage | 800mm | 750–900mm | **Ø850mm bore / ~625mm passage** |
| Height | 2000–2200mm | 2000mm | **2200mm** |
| Price (USD) | $2,500–$3,500 | $3,000–$4,500 | **$1,785–$2,460** |
| Weatherproofing | None | None | **IP44 (neoprene/silicone)** |
| Panel integration | Requires surround wall | Requires panel-bay frame | **Direct bolt-in (120mm panel)** |
| Transport-rated | No | No | **Yes (3mm steel, sealed bearings)** |
| Lead time | 4–8 weeks | 6–10 weeks | **2–3 weeks** |
| Field repairability | Low (ABS/extrusion parts) | Low | **High (standard steel + off-shelf bearings)** |
| **Recommendation** | ✗ | ✗ | **✓** |

Custom fabrication is comparable to or below commercial alternatives while providing superior weatherproofing, transport durability, and field repairability.

---

## 7. Integration Notes

- The drum is installed into the hinged panel before the panel is hung. Panel + drum combined weight: approximately 220–260kg — requires two people and a panel hoist or engine crane for hanging.
- The lower bearing collar is bolted to the panel bottom rail with 8 × M10 stainless bolts. The upper bearing housing is bolted to the panel top rail with 6 × M10. Both connections can be disassembled with standard hex keys for maintenance.
- The drum rotates freely in both directions; there is no rotation limit. The exterior face carries no handle — the operator pushes the bare drum wall to enter. An interior grab rail (100mm Ø SS, welded bracket, no through-hole) at 900mm height allows the operator to pull the drum closed from inside and brace during exit. This eliminates any through-bolt penetration of the drum wall on the exterior face, removing a potential light leak path.
- Interior safelight (Circuit D, per [Electrical Report](electrical-report.md)) illuminates the drum interior during loading operations, allowing operators to orient themselves in darkness.
- **Panel latches (×4 Southco C2-33 cam compression latches) are mounted on the interior face of the panel.** This is a deliberate safety design: if the revolving drum jams and prevents normal egress, an operator inside the container can release all four latches independently from the inside and push the panel open outward. The panel swings 180° on its left-edge hinges, clearing all interior equipment. Latches appear as hidden (dashed) features in the exterior elevation drawing (Sheet 1).
- **Stepped panel construction:** The panel has three thickness zones — 40mm at corners (18mm ply + 4mm steel plate + 18mm ply) and 120mm at center (18mm ply + 84mm RHS frame + 18mm ply). The step transitions occur at Yd=756mm and Yd=1606mm. The 120mm center zone houses the drum; the 40mm corner zones are flush with the container walls.
- **Sliding carriage:** The entire panel slides ~500mm in the X direction on HGR20 linear rails mounted to both container walls at floor and ceiling level (4 rails total, 8 HGH20CA carriage blocks). The left (hinge) side rides via a vertical carriage beam (60×60×3mm SHS, 2400mm tall); the right (latch) side rides directly on blocks attached to the panel frame. Locked by Destaco 207-U toggle clamps at both operational and transport positions. A fixed welded door frame (50×50×3mm RHS) at X=0 provides the EPDM seal landing — the sliding mechanism is transparent to the seal.
- **Transport mode conversion** (single person, ~5 minutes): release cam latches → slide panel inward 300mm → lock → close container doors. See [Equipment Layout Report](equipment-layout-report.md) §6 for full specification.

---

## 8. Source References

1. [SKF 6215-2RS1 datasheet](https://www.skf.com/group/products/rolling-bearings/ball-bearings/deep-groove-ball-bearings/productid-6215-2RS1) — Sealed deep-groove ball bearing specifications.
2. [Hinged Panel Report](hinged-panel-report.md) — Panel construction, hinge, latch, and sliding carriage specification.
3. [Equipment Layout Report](equipment-layout-report.md) — Panel transport mode and sliding carriage clearance analysis.
4. [Electrical Report](electrical-report.md) — Circuit D safelight specification for drum interior.

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
