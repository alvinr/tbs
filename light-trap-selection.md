<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Revolving Light Trap — Selection & Specification

## 1. Purpose

Personnel access during operation is via a revolving light trap drum built into the panel. Operators can enter or exit at any time without opening the full panel or admitting daylight — for example, between coating of the photosensitive material, or while the exposure is being made.

The cargo door end of TBS-001 is sealed by a stepped hinged panel (2362mm wide × 2388mm tall, 50×50mm RHS steel frame, 18mm ply skins). The panel has a stepped profile: 40mm thick at the corner zones (Yd=0–653mm and Yd=1709–2362mm) and 120mm thick at the center zone (Yd=653–1709mm) where the Ø900 housed revolving-door light lock is permanently mounted. The panel swings open about its pivot to clear the door opening for loading IBC totes and equipment. When closed it is light-sealed at the perimeter by a 20mm EPDM compression gasket against a fixed welded door frame at X=0.

Under rev 9 (B2) the Ø900 housing sits in a **punch-out bay** that offsets the drum to X=−400, clearing the X=150 film-plane rail (which is now continuous in operation). For transport (rev10) the panel + drum **SWING ~56° about a vertical Ø89×8mm CHS pivot post** (the reused film-plane far-left upright at X=175, Yd=2287) — carrying the punch-out bay inboard of the door plane (true min X +59mm) so the cargo doors close. The two left film rails (TL + BL) lift out before the swing so the drum cage can transition the X=150 rail plane, then re-seat to the film datum. The housing/drum ride with the panel at Z=130, so they pass over the processing-tray rim (and the Z115 walkway brackets) rather than fouling them. Single-person operation (the swing is assisted, ~5 minutes per mode conversion). See [Equipment Layout Report](equipment-layout-report.md) §6 for the swing-mechanism specification.

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
| Wall thickness | Hybrid plastic skin (rev 9 / B2): 5mm UV-HDPE housing + 4mm PP drum, rolled and extrusion-welded (was 3mm aluminum 5052-H32) |
| Surface finish | Black-pigmented sheet + flat-black touch-in at welds (interior); UV-stabilized sheet (exterior) — no primer |
| Baffles | None — two 80° housing openings 180° apart + single-opening C-shell drum (see §4, §5) |
| Top bearing | SKF 6215 sealed deep-groove ball bearing on 75mm steel stub shaft, bolted to the drum cap via a nylon-isolated hub |
| Bottom bearing | SKF 6215 sealed, stub shaft into floor-mount collar, panel-bolted |
| Drum seals (top/bottom) | Two-layer: closed-cell neoprene wiper + silicone bead — IP44 rated |
| Handle | 100mm Ø SS grab rail, interior face only, at 900mm height |
| Finish | Interior: flat black RAL 9005; exterior drum face: gray oxide |
| Approximate cost | USD $1,465–$2,160 (local plastic fabrication shop) |
| Lead time | 2–3 weeks |

**Assessment — Recommended (hybrid plastic skin, rev 9 / B2).**

Custom fabrication is the correct choice for a field-deployed, transport-rated camera system — every specification can be set to exactly what is required (clear bore, panel-thickness interface, bearing grade, seal type, drum height). **rev 9 switches the shell material from 3mm aluminum (5052-H32) to a hybrid plastic skin: a 5mm UV-stabilized HDPE fixed housing and a 4mm polypropylene revolving drum.** Three things drive the change:

1. **Weight / center of gravity.** The plastic skin cuts the drum/housing shell mass from ~99 kg (aluminum) to ~60 kg (the steel shaft, bearings and grab rail set a floor the shell can't drop below). Because the whole assembly hangs off the swinging leaf and revolves ~56° about the pivot post for transport, lowering its mass reduces the swing cantilever moment on the pivot and keeps the container CG shift small.
2. **No galvanic couple.** An aluminum shell bolted to the steel panel frame and steel bearing hardware needs a full nylon-isolation kit and is a perennial outdoor-corrosion risk. Plastic-to-steel has no galvanic couple — isolation reduces to plain nylon washers at the shaft only.
3. **Cost and fabrication.** UV-HDPE / PP sheet is cheaper than 5052 aluminum, and hot-air / extrusion welding of a Ø900 cylinder is less skilled labor than aluminum TIG seam welding. Net build cost drops from ~$2,300–$3,150 to ~$1,465–$2,160.

A 4–5mm plastic cylinder, edge-stiffened along the opening, is rigid as a freestanding shell without a surrounding wall frame, and bolts into the panel opening on 8 × M10 flush bolts (stainless, nylon-isolated). UV-stabilized HDPE/PP is inherently weatherproof and needs no primer or anodize; the drum is in the dry walk-through entry zone, not the chemistry zone, so only ambient/outdoor exposure applies. The trade-off is a higher coefficient of thermal expansion than aluminum, accommodated by the 15mm running gap between drum and housing.

The SKF 6215 sealed bearing is rated for radial loads to 52.7 kN and operates at 0–120°C — far beyond any field requirement. The neoprene/silicone top seal provides IP44 protection against splash and rain ingress. Black-pigmented sheet with flat-black touch-in at the welds is optically dead at visible wavelengths.

---

## 4. Recommended Specification — Custom Housed Revolving Door (rev 9 / B2)

> Replaces the earlier Ø750mm drum with **internal baffles**, which failed both
> personnel-fit and rotation light-tightness. The light lock is now a **fixed
> housing + single-opening C-shell drum** (no fins) — light-tight by geometry.

### 4.1 Housing + Drum Body

| Item | Specification |
|------|--------------|
| Fixed housing shell | 5mm UV-HDPE (LT_HOUSING_T), rolled to **Ø900mm OD**, extrusion-welded full height; bolted (isolated) into the panel center zone, set in the B2 punch-out bay |
| Housing openings | Two, **80° arc each, 180° apart** (full height) — one facing the exterior, one facing the interior/walkway |
| Rotating drum | 4mm PP C-shell (LT_DRUM_T), **Ø864mm OD** (~Ø850mm bore), single **80° opening**, edge-stiffened, rotates inside the housing on a 15mm running gap |
| Internal baffles | **None** — light-tightness is by the fixed-housing geometry (openings <90°, 180° apart; see §5) |
| Drum/housing height | 2200mm |
| Top cap | 5mm PP plate, flanged, welded to the drum; steel hub insert for the stub shaft |
| Bottom cap | 5mm PP plate, flanged, steel hub insert with 75mm stub shaft for lower bearing |
| Upper stub shaft | 75mm Ø × 150mm steel stub, into the drum top-cap steel hub (nylon-isolated) |
| Surface treatment | Interior: black-pigmented sheet + flat-black at welds; exterior: UV-stabilized sheet (no primer) |

### 4.2 Bearings and Mounting

| Item | Specification |
|------|--------------|
| Bearings (×2) | SKF 6215-2RS1 (75mm ID, 130mm OD, 25mm wide, sealed, C3 clearance) |
| Upper bearing mount | Aluminum housing top ring bolted to panel top rail (isolated) |
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
| 5mm UV-HDPE sheet (housing, ~7 m²) + 4mm PP sheet (drum, ~7 m²) | [TAP Plastics](https://www.tapplastics.com/) / Curbell Plastics (SoCal); or Online Metals plastics | ~$330–$520 total (was 4 × aluminum sheet) |
| SKF 6215-2RS1 bearing (×2) | Bearing World — Anaheim CA; or Applied Industrial Technologies | ~$45–$65 each |
| 75mm × 150mm steel stub shaft (×2) | Pacific Coast Steel or any steel service center | 75mm Ø solid round bar, cut to length |
| Closed-cell neoprene strip 12mm (3m) | McMaster-Carr #93855K6 | Closed-cell, pressure-sensitive adhesive back; ~$22 |
| Silicone bead sealant | McMaster-Carr #7587A3 or equivalent | Black, UV-stable |
| SS grab rail 100mm Ø (×1) | McMaster-Carr #4530T37 | 1" nominal; 400mm cut to length; interior face only |
| Matte-black interior finish | Black-pigmented sheet; rattle-can / local shop | Touch-in at welds; ~$40–$70 |
| Plastic fabrication (rolling, hot-air / extrusion welding, fitting) | Estimate 16–22 hrs labour at local plastic shop | $800–$1,150 depending on shop rate |

**Total custom housing+drum estimate: $1,465–$2,160.**

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
space and the 80° opening gives a **~555mm passage** (sideways entry). The Ø850 bore
meets the §2 standing-space intent; the opening itself is tighter than the nominal
≥700mm and was accepted (rev 8) for occasional single-operator field use. Emergency egress remains the
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
| Clear bore / passage | 800mm | 750–900mm | **Ø850mm bore / ~555mm passage** |
| Height | 2000–2200mm | 2000mm | **2200mm** |
| Price (USD) | $2,500–$3,500 | $3,000–$4,500 | **$1,465–$2,160** |
| Weatherproofing | None | None | **IP44 (neoprene/silicone)** |
| Panel integration | Requires surround wall | Requires panel-bay frame | **Direct bolt-in (120mm panel)** |
| Transport-rated | No | No | **Yes (plastic skin, sealed bearings)** |
| Lead time | 4–8 weeks | 6–10 weeks | **2–3 weeks** |
| Field repairability | Low (ABS/extrusion parts) | Low | **High (weldable plastic + off-shelf bearings)** |
| **Recommendation** | ✗ | ✗ | **✓** |

Custom fabrication is comparable to or below commercial alternatives while providing superior weatherproofing, transport durability, and field repairability.

---

## 7. Integration Notes

- The drum is installed into the hinged panel before the panel is hung. Panel + drum combined weight: approximately **281 kg** (first-principles: steel-framed stepped sandwich with 3mm-aluminum corner plates ~196 kg + plastic-skin Ø900 housing + C-shell drum ~60 kg + 6mm-ply B2 punch-out bay ~25 kg). The Ø89 pivot post + bearings + cage (~38 kg) are separate transport hardware, not carried in the panel+drum lift. Still requires an engine crane or gantry hoist for hanging (beyond a two-person lift). See [Weight Distribution §3.2](weight-distribution-report.md) and [Hinged Panel Report §2.4](hinged-panel-report.md).
- The lower bearing collar is bolted to the panel bottom rail with 8 × M10 stainless bolts. The upper bearing housing is bolted to the panel top rail with 6 × M10. Both connections can be disassembled with standard hex keys for maintenance.
- The drum rotates freely in both directions; there is no rotation limit. The exterior face carries no handle — the operator pushes the bare drum wall to enter. An interior grab rail (100mm Ø SS, welded bracket, no through-hole) at 900mm height allows the operator to pull the drum closed from inside and brace during exit. This eliminates any through-bolt penetration of the drum wall on the exterior face, removing a potential light leak path.
- Interior safelight (Circuit D, per [Electrical Report](electrical-report.md)) illuminates the drum interior during loading operations, allowing operators to orient themselves in darkness.
- **Panel latches (×4 Southco C2-33 cam compression latches) are mounted on the interior face of the panel.** This is a deliberate safety design: if the revolving drum jams and prevents normal egress, an operator inside the container can release all four latches independently from the inside and push the panel open outward. The panel swings open about its left-edge pivot post, clearing the door opening. Latches appear as hidden (dashed) features in the exterior elevation drawing (Sheet 1).
- **Stepped panel construction:** The panel has three thickness zones — 40mm at corners (18mm ply + 3mm aluminum plate + 18mm ply) and 120mm at center (18mm ply + 84mm steel RHS frame + 18mm ply). The step transitions occur at Yd=653mm and Yd=1709mm. The 120mm center zone houses the drum; the 40mm corner zones are flush with the container walls.
- **Swing pivot:** For transport the panel + drum revolve ~56° about a vertical Ø89×8mm CHS pivot post (the reused film-plane far-left upright at X=175, Yd=2287) on a thrust collar + top/bottom hub bearings. The vertical axis is balanced at any angle (no gravity torque). Locked at the swung position by top + bottom wall stays (hook + eye + turnbuckle). A fixed welded door frame (50×50×3mm RHS) at X=0 provides the EPDM seal landing for the perimeter + cut + lip seals, compressed by the cam latches in the closed position.
- **Transport mode conversion** (single person, ~5 minutes, swing assisted): park + pin the drum → lift out the left walkway + door-end near-deck → strike the two left film rails (TL + BL) → release the cam latches → swing the frame ~56° inboard about the pivot → engage the top + bottom wall stays → close the container doors (they clear the swung frame by +59mm; the door-end walkway brackets are cleared at Z, not struck). See [Equipment Layout Report](equipment-layout-report.md) §6 for full specification.

---

## 8. Source References

1. [SKF 6215-2RS1 datasheet](https://www.skf.com/group/products/rolling-bearings/ball-bearings/deep-groove-ball-bearings/productid-6215-2RS1) — Sealed deep-groove ball bearing specifications.
2. [Hinged Panel Report](hinged-panel-report.md) — Panel construction, pivot, latch, and swing-mechanism specification.
3. [Equipment Layout Report](equipment-layout-report.md) — Panel transport mode and swing clearance analysis.
4. [Electrical Report](electrical-report.md) — Circuit D safelight specification for drum interior.

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
