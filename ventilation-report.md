<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Ventilation & Cooling

## 1. Purpose

TBS-001 requires active ventilation and cooling to maintain safe operator working conditions and acceptable chemistry coating temperatures inside a sealed steel container. This report consolidates the complete ventilation and cooling specification: thermal analysis, fan system, evaporative cooler, light-safe duct penetrations, shade canopy, and operating modes.

All ventilation and cooling components run at 12V DC from the solar/battery power system. See [Electrical Report](electrical-report.md) for circuit assignments and wiring.

---

## 2. Thermal Problem

A 20ft ISO steel container in direct Palm Springs summer sun (ambient 40–45°C, direct irradiance 1,000 W/m²) reaches interior temperatures of 65–75°C without intervention. Two constraints drive the cooling design:

| Constraint | Limit | Source |
|-----------|-------|--------|
| Operator safety | Interior < 40°C | OSHA heat illness prevention guidelines |
| Chemistry coating | Interior < 35°C | Cyanotype sensitizer application window |

Without any mitigation, the container is unusable in summer daytime. The system uses three complementary strategies to bring the interior within working range.

---

## 3. Cooling Strategy

| Method | Interior ΔT | Cost | Power | Required? |
|--------|------------|------|-------|-----------|
| 80% shade cloth canopy over container | −15 to −20°C | ~$300 | None | **Yes — always** |
| Scheduling (shoot before 09:00 / after 18:00 in summer) | −10 to −15°C effective | $0 | None | Recommended |
| 12V DC evaporative cooler (swamp cooler) | −10 to −15°C additional | ~$300 | 80W | **Yes — in temperatures above 30°C ambient** |

Combined (shade canopy + cooler + scheduling): interior temperature reaches 25–32°C — within operator working range.

> **Why evaporative cooling works in hot climates (e.g. Palm Springs):** Evaporative (swamp) cooling is most effective when ambient relative humidity is low. Palm Springs in summer averages 10–18% RH — optimal for this technology. At 15% RH and 42°C ambient, an evaporative cooler can reduce temperature by 15–18°C, bringing 42°C down to 24–27°C after the shade canopy's contribution. At the same conditions, a standard 9,000 BTU mini-split uses 900W vs. the evaporative cooler's 80W — an 11× power saving.

---

## 4. Ventilation Fans

For operator comfort during processing in warm conditions, but also to ensure there is fresh air exchange within the space.

Longitudinal section showing the cross-flow ventilation path: Fan B intake at the cargo door panel (low position), diagonal airflow up through the container volume, Fan A exhaust at the far end wall (high position, above the IBC stack). Evaporative cooler intake duct on the pinhole wall.

**Sheet 1 — Container Ventilation Section**
![TBS-001 Ventilation — Sheet 1: Container Longitudinal Section](assets/lighttrap-sheet1.png)


| Parameter | Specification |
|-----------|---------|
| Fan diameter |  6" (150mm) |
| Airflow per fan |  ~200 CFM |
| Total airflow | ~400 CFM |
| Power draw (each) |  ~60W |
| Circuit fuse | 5A |
| Cost  | ~$60 |

### 4.1 Fan Positions

| Fan | Position | Mounting | Function |
|-----|----------|----------|----------|
| Fan B (intake) | Hinged panel, near corner zone by the pinhole wall (Yd=365mm, Z=600mm — rev9/B2 swap) | Flush-mounted in 40mm corner zone panel | Fresh air intake — draws cooler air near floor level |
| Fan A (exhaust) | Far end wall (X=5893mm), high position (Z=2200mm, above IBC stack) | Flush-mounted in wall penetration | Exhaust warm, humid air during processing and drying |

Both fans are 6" (150mm) diameter, 12V DC (AC Infinity S6 or equivalent). Fan bodies do not protrude beyond either panel face. Cross-flow ventilation runs diagonally: **low intake at the cargo door end → high exhaust at the far end** — fresh air enters near the floor, sweeps the working volume, and warm air discharges high.

> **Why this layout:** The intake was relocated to the cargo door panel (low) and the exhaust to the far end wall (high) because the near IBC tote column sits flush against the far end wall up to Z=2020mm. A low fan there would drive its 300mm baffle duct straight into the tote; mounting the exhaust at Z=2200mm clears the stack top with room to spare while preserving the diagonal low-in / high-out flow.

### 4.2 Fan A — Far End Wall Exhaust

Fan A is flush-mounted in a wall penetration at the far end wall (X=5893mm), high position (Z=2200mm AFF, Yd=1996mm — far side, off the corner; rev9/B2 swapped it to the far side so Fan B's conduit can run along the pinhole wall) — above the 2020mm-tall IBC stack so its baffle duct projects into clear space above the totes. The fan body sits inside a light-safe baffle duct (see §4.4) bolted to the interior face of the wall. A weatherproof louvre grille on the exterior face protects the penetration from rain and debris. The fan, duct, and grille are permanently installed — no removal is required for mode conversion or transport.

**Wiring:** Fan A's wire run routes from the fuse block along the ceiling cable trunking to the far end wall, then drops a short distance to the fan near the ceiling. The entire run is inside the container — no flex cable or weatherproof connectors are needed.

### 4.3 Fan B — Panel-Mounted Intake

Fan B is mounted low on the sliding hinged panel, which moves with the panel during mode conversion (300mm slide travel + 180° swing). The fan and baffle duct are interior-mounted (same as Fan A); a weatherproof louvre grille on the panel exterior face is the only external component. During operation, the cargo doors are open (personnel access is via the revolving light trap drum), so fresh outside air is drawn in through the grille near floor level.

**Wiring:** Fan B's wire run routes from the fuse block along the ceiling cable trunking to the fixed door frame, then crosses to the panel via a 1m coiled cable (16 AWG, 2-conductor, silicone-jacketed) with Deutsch DT 2-pin weatherproof connectors at each end. The coiled cable accommodates 300mm of panel slide travel plus 180° panel swing without binding. The fixed end anchors to the door frame top rail; the panel end anchors to the carriage beam. The service loop hangs in the ceiling zone above Z=2200mm; the wire drops down the panel to the low fan.

### 4.4 Light-Safe Baffle Ducts

Both fan penetrations include L-shaped offset baffles inside a duct stub to prevent light ingress while allowing unrestricted airflow:

- **Construction:** Black sheet metal, L-shaped offset — two flat baffle plates, each the **full 200mm duct height** (welded to the duct top and bottom so no light passes over or under them) × 125mm wide, set one against each side wall so each leaves a **75mm airflow gap** on the opposite side; air winds left↔right on a horizontal S-path while the overlap blocks the line of sight, inside a 300mm deep duct stub
- **Light path:** No straight line of sight from exterior to interior at any incidence angle — the full-height plates block top/bottom, the left/right offset blocks the center (horizontal S-path)
- **Airflow resistance:** Minimal — the L-path increases duct length by ~150mm but maintains full 150mm diameter cross-section at each turn

**Sheet 2 — Fan & Baffle Duct Assembly**
Detail views of the L-shaped light-safe baffle duct construction for both the 6" ventilation fans and the 8" cooler intake duct. Shows offset baffle geometry, duct stub dimensions, and light path verification.

![TBS-001 Ventilation — Sheet 2: Fan & Baffle Duct Assembly](assets/lighttrap-sheet2.png)

The baffle design is identical for both fans. Fan A's baffle duct is fixed to the end wall interior; Fan B's baffle duct is fixed to the hinged panel interior. Both fans and ducts are fully interior-mounted — only the weatherproof louvre grille is on the exterior face.

---

## 5. Evaporative Cooler

### 5.1 Specification

| Parameter | Specification |
|-----------|--------------|
| Model | Portacool Jetstream 110 (12V DC version) or equivalent |
| Dimensions | ~600 × 350 × 800mm |
| Weight | ~20 kg dry |
| Power draw | ~80W at 12V DC |
| Airflow | ~300 CFM |
| Water consumption | ~3 liters/hour |
| Circuit | E (10A fuse, 14 AWG) |
| Water source | Dedicated 20-liter reservoir, refilled from Blue circuit IBC tote |

### 5.2 Light-Safe Cooler Intake

The cooler sits on the ground outside the container, adjacent to the pinhole wall. A Ø200mm flexible insulated duct rises vertically from the cooler outlet and turns through a 90° elbow into the wall penetration (Z=1900mm), so it meets both the cooler and the wall stub at right angles. The penetration carries light-safe baffles. Power (Circuit E, 12V DC) is supplied via a Deutsch DT 2-pin bulkhead connector on the external power panel — the same flush-mount panel that carries the solar and shore power inputs. A 1.5m external cable connects the panel to the cooler; both the cable and flex duct are disconnected and stowed inside the container for transport. See [Electrical Report](electrical-report.md) §7.3 for the full wire path.

This arrangement requires no permanent external mounting — the cooler is simply placed, connected (duct + power), and removed each session.

| Parameter | Value |
|-----------|-------|
| Duct size | 200mm (8") — sized for ~300 CFM at low velocity |
| Penetration location | Pinhole wall (Yd=0 face) at X=1000mm, Z=1900mm |
| Flexible duct | Ø200mm insulated flex, ~1.2m length, aluminum foil jacket |
| Elbow | Ø200mm (8") 90° galvanized elbow — vertical riser to horizontal wall entry |
| Interior baffles | Two 200 × 200mm flat steel baffles, offset 100mm, inside a 300mm duct stub |
| Light path | Broken by offset baffles — no direct line of sight |
| Exterior coupling | Ø200mm duct collar on wall stub; flex duct secured with hose clamp |
| Exterior cap | Removable weatherproof cap on wall stub when cooler is not connected |

### 5.3 Transport Stowage

The cooler is stowed inside the container for transport. See [Equipment Layout Report](equipment-layout-report.md) §6.2 for the full stowage specification.

From the walkway design, the location of the cooler (green rectangle) can be seen for transportation, secured by straps and D-rings.

![TBS-001 Walkway — Sheet 1: Equipment Location](assets/walkway-sheet1.png)

| Parameter | Value |
|-----------|-------|
| Stowage zone | Near walkway wide section, X=1200–1800mm, Yd=0–500mm |
| Base plate | 12mm plywood, 600 × 350mm (load distribution) |
| Securing | 2 × 25mm ratchet straps to cantilever bracket arms |
| Clearance to panel transport envelope | 780mm (panel max X=420mm, cooler starts X=1200mm) |

---

## 6. Shade Canopy

| Parameter | Specification |
|-----------|--------------|
| Material | 80% shade cloth, 20 × 10 ft |
| Frame | 1.5" EMT conduit + fittings |
| Installation | Erected over the container before solar noon |
| Temperature reduction | −15 to −20°C interior |
| Power requirement | None |
| Approximate cost | ~$200 (cloth $80 + frame $120) |

The shade canopy is the most effective single mitigation — it eliminates direct solar irradiance on the container roof and walls, reducing the primary heat source before any active cooling is applied. It is required at all deployments regardless of season.

---

## 7. Operating Modes

| Mode | Intake (Fan B) | Exhaust (Fan A) | Evap cooler | Shade |
|------|---------------|----------------|-------------|-------|
| Pre-cooling (before entry) | Full speed | Full speed | ON (30 min minimum) | Erected |
| Loading / coating (safelight) | Low speed | Low speed | ON | Erected |
| Exposure | OFF | OFF | OFF or standby | Erected |
| Development / washing | Low speed | Low speed | ON if > 30°C | Erected |
| Post-session ventilation | Full speed | Full speed | OFF | — |

**Minimum ventilation requirement for darkroom chemistry:** Cyanotype chemistry includes ammonium iron(III) oxalate and potassium ferricyanide, which produce low-level fumes during mixing and application. OSHA permissible exposure limits require forced ventilation during chemistry use. The 400 CFM combined airflow (2 × 200 CFM) provides approximately 16 air changes per hour in the container volume (~25 m³) — exceeding the OSHA minimum for darkroom operations.

---

## 8. Electrical Integration

| Circuit | Device | Fuse | Wire gauge | Run length |
|---------|--------|------|-----------|-----------|
| A | Ventilation fan — exhaust (6", far end wall, high) | 5A | 16 AWG | ~2.5m |
| B | Ventilation fan — intake (6", panel-mounted, low) | 5A | 16 AWG | ~8m + flex connector |
| E | Evaporative cooler | 10A | 14 AWG | ~4m |

All circuits originate from the Blue Sea 5026 fuse block in the main electrical enclosure. See [Electrical Report](electrical-report.md) §10 for full wiring specification.

---

## 9. Parts List

| Item | Spec | Source | Est. cost |
|------|------|--------|-----------|
| 6" inline fans × 2 | 12V DC, ~200 CFM each | Amazon (AC Infinity S6) | ~$120 |
| Evaporative cooler | 12V DC, ~300 CFM | Portacool / Amazon | ~$280 |
| Shade canopy — 80% shade cloth | 20 × 10 ft | Amazon / Farm supply | ~$80 |
| Canopy frame | 1.5" EMT conduit + fittings | Home Depot | ~$120 |
| Baffle duct sheet metal (fans) | 22 ga galvanized, 2 × 300mm stubs | Local sheet metal / Home Depot | ~$30 |
| Baffle duct sheet metal (cooler) | 22 ga galvanized, 1 × 300mm stub, Ø200mm | Local sheet metal / Home Depot | ~$20 |
| 200mm insulated flex duct | Ø200mm × 1.2m, aluminum foil jacket | Home Depot / McMaster-Carr | ~$22 |
| 200mm 90° duct elbow | Ø200mm (8") galvanized, cooler riser to wall stub | Home Depot | ~$14 |
| Duct collar + hose clamp | Ø200mm, galvanized | Home Depot | ~$12 |
| Weatherproof duct cap | Ø200mm, removable | Home Depot | ~$8 |
| Deutsch DT 2-pin connectors | Fan B flex connector (×2 sets) | Waytek Wire (waytekwire.com) | ~$8 |
| 16 AWG silicone coiled cable | 1m, 2-conductor (Fan B flex) | Amazon / Waytek Wire | ~$15 |
| Cooler external power cable | 1.5m, 14 AWG 2-cond, Deutsch DT 2-pin plugs each end | Waytek Wire / Amazon | ~$20 |
| Ratchet straps, 25mm × 2 | Cooler stowage | Home Depot / Amazon | ~$12 |
| Plywood base plate | 12mm, 600 × 350mm (cooler stowage) | Lumber yard / Home Depot | ~$8 |
| **Ventilation & cooling total** | | | **~$769** |

---

## 10. Maintenance

| Interval | Task |
|----------|------|
| Before each session | Confirm Fan A and Fan B airflow (tissue deflection test at duct stubs) |
| Before each session | Check evaporative cooler reservoir level; refill from Blue circuit |
| Before each session | Inspect shade canopy for tears or collapsed frame sections |
| Monthly | Clean fan blades and baffle duct interiors (dust accumulation reduces airflow) |
| Monthly | Inspect Deutsch DT connectors at Fan B flex cable for corrosion |
| Every 6 months | Check cooler pad condition — replace if mineral buildup reduces airflow |
| Every 6 months | Inspect baffle duct welds for cracking or corrosion |
| Annually | Replace evaporative cooler pads regardless of condition |
| Annually | Inspect shade cloth for UV degradation; replace if shade factor drops below 70% |
| Before transport | Drain cooler reservoir completely; stow cooler per §5.3 |
| Before transport | Cap all exterior duct stubs to prevent rain ingress |

---

## 11. Source References

1. [AC Infinity CLOUDLINE S6](https://acinfinity.com/cloudline-s6-quiet-inline-fan-6-with-speed-controller/) — 6" inline duct fan specifications.
2. [Portacool Jetstream 110](https://www.portacool.com/) — 12V DC evaporative cooler specifications.
3. [OSHA Heat Illness Prevention](https://www.osha.gov/heat-exposure) — Workplace heat exposure guidelines and permissible limits.
4. [Electrical Report](electrical-report.md) — Circuit assignments (A, B, E), wiring specification, and fuse block layout.
5. [Hinged Panel Report](hinged-panel-report.md) — Panel corner zone construction and Fan B mounting.
6. [Equipment Layout Report](equipment-layout-report.md) — Evaporative cooler position and transport stowage specification.
7. [Operating Manual](operating-manual.md) — Ventilation and cooling operational procedures (Phase 1.6).

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
