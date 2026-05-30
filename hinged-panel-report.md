<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Hinged Light-Trap Panel

## 1. Purpose

TBS-001 requires a light-tight seal at the cargo door end of the container that
simultaneously allows personnel access during operation without admitting daylight.
The hinged light-trap panel fills both roles: it seals the full 2362 × 2388mm
cargo door opening as a rigid structural panel, and incorporates a revolving drum
light trap that permits operators to enter and exit the darkened interior at any
time without opening the panel or breaking the light seal. In case of emergency, or to easy loading and unloading of materials, the whole hinged panel can open fully, being locked from the inside.

**Sheet 1 — Front Elevation (1:20): Panel Dimensions, Drum, Hinges, Latches (interior face)**
![TBS-001 Hinged Panel — Sheet 1: Front Elevation](assets/hingepanel-sheet1.png)

**Design goals:**

- 100% light exclusion — no straight-line optical path from exterior to interior
- Single-operator personnel access at any time during exposure
- 180° outward swing for full-width loading access (IBC totes, equipment)
- 300mm inward slide for transport mode — clears ISO container doors
- Emergency egress operable from inside without tools
- Weatherproof for outdoor field deployment (IP44 rated seals)
- Single-person mode conversion (~5 minutes)

---

## 2. Panel Construction

### 2.1 Stepped Profile

The panel has three thickness zones to accommodate the revolving drum in the center
while keeping the corners flush with the container walls.

**Sheet 2 — Plan Cross-Section (1:10 horiz / 1:1 depth): Drum Baffles and S-Path Light Route**
![TBS-001 Hinged Panel — Sheet 2: Plan Cross-Section](assets/hingepanel-sheet2.png)

| Zone | Yd range (mm) | Width (mm) | Thickness (mm) | Construction |
|------|--------------|-----------|---------------|-------------|
| Near corner | 0–756 | 756 | 40 | 18mm ply + 4mm steel plate + 18mm ply |
| Center | 756–1,606 | 850 | 120 | 18mm ply + 84mm RHS frame + 18mm ply |
| Far corner | 1,606–2,362 | 756 | 40 | 18mm ply + 4mm steel plate + 18mm ply |

The 80mm step between corner and center zones occurs at Yd=756mm and
Yd=1606mm. The center zone houses the revolving drum; the corner zones are
flush-faced panels that seal against the fixed door frame.

### 2.2 Frame

| Parameter | Value |
|-----------|-------|
| Frame material | 50 × 50 × 3mm RHS mild steel |
| Outer dimensions | 2362 × 2388mm |
| Skin (each face) | 18mm exterior-grade plywood |
| Interior finish | Flat black (RAL 9005) — optically dead at visible wavelengths |
| Frame perimeter | Welded corners, mitred joints |
| Panel weight (without drum) | ~180 kg (estimated) |

### 2.3 EPDM Perimeter Seal

A 20mm closed-cell EPDM compression gasket runs the full perimeter of the panel,
seated in an extruded aluminum channel. The gasket compresses against a fixed welded
door frame (50 × 50 × 3mm RHS) at X=0 when the four cam latches engage. The seal
provides light-tight compression on all four sides.

---

## 3. Revolving Light-Trap Drum

**Sheet 3 — Drum Vertical Section Elevation (Section A-A): Walking-height orientation confirmation**
![TBS-001 Hinged Panel — Sheet 3: Drum Elevation](assets/hingepanel-sheet3.png)


### 3.1 Specification

| Parameter | Value |
|-----------|-------|
| Type | Vertical-axis revolving drum with internal baffles |
| Drum outer diameter | Ø750mm |
| Drum height | 2200mm (floor to upper bearing) |
| Wall thickness | 3mm mild steel, rolled and seam-welded |
| Interior finish | Shot-blast + flat black powder coat (RAL 9005) |
| Exterior finish | Grey oxide primer + grey topcoat |
| Clear walking height | 1910mm (drum body between bearings) |
| Headroom (1780mm operator) | 130mm |
| Internal baffles | 4 × 3mm steel fins, full height, at 90° spacing |
| Weight | ~60–80 kg (estimated) |

### 3.2 Bearings

| Item | Specification |
|------|--------------|
| Bearing model (×2) | SKF 6215-2RS1 sealed deep-groove ball bearing |
| Bore | 75mm ID, 130mm OD, 25mm wide |
| Clearance | C3 |
| Radial load rating | 52.7 kN (static) |
| Operating temperature | 0–120°C |
| Stub shafts | 75mm Ø × 150mm steel, welded to drum top and bottom caps |
| Axial retention | Circlip on stub shaft each side |
| Upper mount | Welded steel housing bolted to panel top rail (6 × M10 SS) |
| Lower mount | Welded steel floor collar bolted to panel bottom rail (8 × M10 SS) |
| Bearing housing height | 45mm (each) |

### 3.3 Light Path Verification

The 4-baffle arrangement eliminates any straight-line path from exterior to
interior. Four radial fins at 90° spacing create quarter-circle sectors. A person
entering from the exterior must navigate an S-path through at least one full
sector (minimum 45° rotation) before reaching the interior face.

At Ø750mm diameter with 4 baffles, the shortest possible S-path through the drum
is 590mm — significantly longer than the 120mm panel thickness. No line of sight
is possible at any incidence angle within ±30° of normal.

See [Light Trap Selection](light-trap-selection.md) §5 for full verification.

### 3.4 Drum Seals

| Location | Seal method |
|----------|------------|
| Top | 12mm closed-cell neoprene wiper strip bonded to top cap underside + silicone bead seal against ceiling mount plate |
| Bottom | 12mm closed-cell neoprene wiper strip bonded to bottom cap underside + silicone bead seal against floor mount plate |
| Drum-to-panel gap | 15mm radial clearance, closed by 20mm neoprene compression strip bonded to panel drum aperture |
| Weather rating | IP44 (splash and rain protection) |

### 3.5 Handle

A 100mm Ø × 400mm stainless steel grab rail is mounted on the interior face
only at 900mm height. The handle is attached by a welded bracket — no through-bolt
penetration of the drum wall on the exterior face. This eliminates a potential
light leak path. The operator enters by pushing the bare exterior drum wall, then
uses the interior grab rail to pull the drum closed and brace during exit.

---

## 4. Hinges and Latches

### 4.1 Hinges

| Parameter | Value |
|-----------|-------|
| Type | 200mm stainless steel ball-bearing piano hinge |
| Quantity | 3 |
| Positions (from floor) | 220mm, 1190mm, 2158mm |
| Mounting | Left edge of panel (exterior view) |
| Swing | 180° outward — clears full door opening and all interior equipment |

### 4.2 Cam Latches

| Parameter | Value |
|-----------|-------|
| Model | Southco C2-33 cam compression latch |
| Quantity | 4 (one at each corner) |
| Positions | 210mm and 2152mm from side edges, 220mm and 2168mm from floor |
| Mounting face | **Interior** — deliberate safety design for emergency egress |
| Seal compression | Compresses EPDM perimeter gasket against fixed door frame |

**Emergency egress:** If the revolving drum jams and prevents normal egress, an
operator inside the container can release all four interior-mounted cam latches
independently and push the panel open outward. The panel swings 180° clear of all
interior equipment.

---

## 5. Sliding Carriage System

The entire panel (including the drum) slides 300mm in the X direction on linear
rails for transport mode conversion. This slide retracts the drum's exterior
overhang behind the container door closure plane.

**Sheet 1 — Side elevation cross-section: Panel suspended from ceiling rail, operational and transport positions, processing tray clearance**
![TBS-001 Ceiling Rail — Sheet 1: Side Elevation](assets/ceiling-rail-sheet1.png)

See [Ceiling Rail Design](ceiling-rail-report.md) for full details.

### 5.1 Panel Positions

**Sheet 4 — Sliding rail transport system: HGR20 rails, operational vs. transport positions**
![TBS-001 Hinged Panel — Sheet 4: Transport System](assets/hingepanel-sheet4.png)

| Position | Panel corner inner face X | Drum exterior edge X | Container doors clear? |
|----------|--------------------------|---------------------|----------------------|
| Operational | 40mm | −295mm | No (drum protrudes 295mm beyond exterior face) |
| Transport | 340mm | −35mm → +5mm | Yes (drum clears exterior face by 5mm) |

### 5.2 Locking

| Lock position | Method |
|--------------|--------|
| Operational (X=0) | 2 × Destaco 207-U toggle clamps |
| Transport (X=300) | 2 × Destaco 207-U toggle clamps |

### 5.3 Floor Gap

The panel is suspended from the ceiling HGR20 rails with an 80mm gap between the
panel bottom edge and the container floor. This gap clears the 50mm processing tray
rim with 30mm margin, allowing the panel to slide freely in both directions without
contacting the tray.

---

## 6. Light Seal Design

The sliding mechanism introduces five potential light ingress paths that must be
sealed when the panel is in the operational position.

| # | Light path | Seal method |
|---|-----------|-------------|
| 1 | Panel perimeter → door frame | 20mm EPDM gasket in aluminum channel, compressed by 4 × Southco C2-33 cam latches against fixed door frame at X=0 |
| 2 | Left carriage beam slot | Doubled nylon brush strip (~70 × 2400mm slot), bristles inward from both sides, bonded to frame slot edges |
| 3 | Right guide slot | Matching doubled nylon brush strip (~70 × 2400mm slot), same treatment as left slot |
| 4 | Rail channels at floor/ceiling (×4) | 10mm closed-cell neoprene compression pad (50 × 30mm) bonded to frame face around each rail penetration |
| 5 | Panel edge-to-wall clearance gaps | 15mm closed-cell EPDM strips (self-adhesive, full panel height) bonded to fixed door frame inner face at each side |

**Seal verification:** After mode conversion, the operator performs a 5-minute
dark-adaptation check inside the container with all seals engaged. Any visible light
points are marked with gaffer tape for re-sealing.

---

## 7. Fixed Door Frame

A fixed welded door frame provides the seal landing surface and structural anchor
for the sliding carriage.

| Parameter | Value |
|-----------|-------|
| Material | 50 × 50 × 3mm RHS mild steel |
| Position | X=0 (container end wall inner face) |
| Function | EPDM seal landing, carriage beam slot housing, rail mounting |
| Attachment | Welded to container end wall structural members |
| Slots | 2 × vertical (~70 × 2400mm) for carriage beam and right-side guide |
| Rail penetrations | 4 × (floor and ceiling, both walls) sealed by neoprene pads |

---

## 8. Parts List

### 8.1 Panel Structure

| Item | Specification | Qty | Est. cost (USD) |
|------|--------------|-----|----------------|
| 50 × 50 × 3mm RHS mild steel (6 m lengths) | Frame perimeter + internal members | 4 | $120–$160 |
| 18mm exterior-grade plywood (1220 × 2440mm sheets) | Panel skins (both faces) | 6 | $180–$300 |
| 4mm steel plate (1220 × 2440mm) | Corner zone core plates | 2 | $80–$120 |
| 20mm EPDM gasket (per meter, closed-cell) | Perimeter seal — ~10 m required | 10 m | $40–$60 |
| Aluminum U-channel (per meter) | Gasket retainer — ~10 m required | 10 m | $30–$50 |
| 200mm SS ball-bearing piano hinge | Left-edge hinges | 3 | $45–$75 |
| Southco C2-33 cam compression latch | Interior-mounted corner latches | 4 | $60–$100 |
| Flat black paint (RAL 9005) | Interior face | 2 qt | $20–$30 |
| **Panel subtotal** | | | **$575–$895** |

### 8.2 Revolving Drum

| Item | Specification | Qty | Est. cost (USD) |
|------|--------------|-----|----------------|
| 3mm mild steel sheet (1200 × 2400mm, A36) | Drum body + baffles | 2 | $140–$180 |
| 5mm steel plate | Top and bottom caps | 1 | $40–$60 |
| SKF 6215-2RS1 sealed bearing | Top and bottom bearings | 2 | $90–$130 |
| 75mm Ø × 150mm steel stub shaft | Bearing shafts | 2 | $30–$50 |
| 12mm closed-cell neoprene strip (3 m) | Top and bottom drum seals | 1 | $20–$25 |
| Silicone bead sealant (black, UV-stable) | Bearing housing seal | 1 | $10–$15 |
| 100mm Ø SS grab rail | Interior handle, 400mm cut length | 1 | $15–$25 |
| Flat black powder coat (drum interior) | Local powder coat service | 1 | $120–$180 |
| Metal fabrication (rolling, welding, fitting) | 16–20 hrs labor | 1 | $800–$1,200 |
| **Drum subtotal** | | | **$1,265–$1,865** |

### 8.3 Sliding Carriage

| Item | Specification | Qty | Est. cost (USD) |
|------|--------------|-----|----------------|
| HGR20 linear guide rail (500mm) | Floor/ceiling rails, both walls | 4 | $80–$120 |
| HGH20CA carriage block | 2 per rail | 8 | $120–$200 |
| 60 × 60 × 3mm SHS mild steel (2400mm) | Left-side carriage beam | 1 | $25–$40 |
| Destaco 207-U toggle clamp | Operational + transport locks | 4 | $60–$100 |
| Nylon brush strip (doubled, per meter) | Carriage beam slot seals — ~5 m each side | 10 m | $40–$60 |
| 10mm closed-cell neoprene pad (50 × 30mm) | Rail channel seals | 4 | $10–$15 |
| 15mm EPDM strip (self-adhesive, per meter) | Panel edge-to-wall clearance seals — ~5 m each side | 10 m | $30–$50 |
| **Carriage subtotal** | | | **$365–$585** |

### 8.4 Fixed Door Frame

| Item | Specification | Qty | Est. cost (USD) |
|------|--------------|-----|----------------|
| 50 × 50 × 3mm RHS mild steel (6 m lengths) | Frame members | 3 | $90–$120 |
| Welding / fabrication | Frame assembly + wall attachment | 1 | $200–$350 |
| **Door frame subtotal** | | | **$290–$470** |

### 8.5 Cost Summary

| Assembly | Low estimate | High estimate |
|----------|------------|--------------|
| Panel structure | $575 | $895 |
| Revolving drum | $1,265 | $1,865 |
| Sliding carriage | $365 | $585 |
| Fixed door frame | $290 | $470 |
| **Total** | **$2,495** | **$3,815** |

---

## 9. Maintenance

| Interval | Task |
|----------|------|
| Every use | Dark-adaptation light seal check (5 min) — mark any light points with gaffer tape |
| Every 20 mode conversions | Inspect doubled nylon brush strips at carriage beam slots for wear |
| Every 6 months | Inspect EPDM perimeter gasket compression; replace if permanently deformed |
| Every 6 months | Inspect neoprene drum seals (top/bottom) for wear and adhesion |
| Annually | Replace brush strips (all carriage/guide slots) |
| Annually | Lubricate HGR20 rails and carriage blocks per manufacturer spec |
| Annually | Check SKF 6215 bearings for roughness — sealed for life, replace only if failed |
| Annually | Inspect Destaco toggle clamps for latch engagement and spring tension |
| Annually | Inspect Southco cam latches for compression force; adjust or replace striker |
| Every 2 years | Re-seal drum top/bottom neoprene wiper strips and silicone bead |
| As needed | Re-apply flat black interior paint where scuffed or worn |

---

## 10. Source References

| Item | Source |
|------|--------|
| SKF 6215-2RS1 bearing specification | [SKF Product Catalog](https://www.skf.com/group/products/rolling-bearings/ball-bearings/deep-groove-ball-bearings/productid-6215-2RS1) — radial load 52.7 kN static, sealed, C3 clearance |
| Southco C2-33 cam latch | [Southco catalog](https://southco.com/en_us_int/c2-33-11) — flush-mount cam compression latch |
| Destaco 207-U toggle clamp | [Destaco catalog](https://www.destaco.com/207-u.html) — horizontal hold-down clamp, 375 lb capacity |
| HGR20 / HGH20CA linear guide | [HIWIN equivalent](https://hiwin.com/products/linear-guideways/) — generic 20mm profile linear rail system |
| EPDM gasket material | [McMaster-Carr](https://www.mcmaster.com/epdm-rubber-sheets) — closed-cell EPDM, UV-stable |
| Neoprene wiper strip | [McMaster-Carr #93855K6](https://www.mcmaster.com/93855K6) — closed-cell, pressure-sensitive adhesive |
| Revolving drum light trap design | See [Light Trap Selection](light-trap-selection.md) for full commercial comparison and custom specification |
| Sliding carriage specification | See [Equipment Layout Report](equipment-layout-report.md) §6 for clearance analysis and light seal design |
| Panel construction drawings | See [Engineering Diagrams](engineering-diagrams.md) §12 — Sheets 1–4 |

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
