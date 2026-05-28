<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Electrical & Systems Report

## 1. Purpose

This report specifies the complete electrical and environmental control systems for TBS-001: solar power architecture, battery bank, light trap vestibule, cooling, ventilation, interior lighting, and wiring. All systems run at 12V DC from a rooftop/ground-mounted solar array with optional shore power backup, enabling fully off-grid operation.

See also: [Operating Manual](operating-manual.md) for step-by-step operational procedures.

---

## 2. System Overview
TBS-001 is designed for fully off-grid operation. All power comes from a rooftop/ground-mounted solar array charging a LiFePO4 battery bank. Shore power (mains) is accommodated as an optional backup charging input only — the system operates identically without it.

All loads run at **12V DC**. There is no mains AC distribution inside the container.

```
Solar panels (3 × 200W)
  → Victron SmartSolar MPPT 100/50 charge controller
  → 12V / 200Ah LiFePO4 battery bank ←── Victron IP65 12/15 shore charger (optional)
  → Blue Sea 5026 fuse block
  → Circuits A–G (ventilation, pump, safelight, cooling, actuators, lighting)
```

See [Section 10.4](#104-electrical-diagrams) for embedded diagrams.

## 3. Power Budget
| Circuit | Device | Peak draw | Duty cycle |
|---------|--------|-----------|-----------|
| A | Ventilation fan — intake (6") | 60W | Continuous during processing |
| B | Ventilation fan — exhaust (6") | 60W | Continuous during processing |
| C | Water pumps P-01–P-04 (12V DC; P-03 in IBC corridor) | 100W | Intermittent (~30 min/print) |
| D | Safelight — interior + vestibule | 15W | Loading phase only (~45 min) |
| E | Evaporative cooler (12V DC) | 80W | Continuous during operation |
| F | Film plane actuators (optional) | 100W peak | Intermittent |
| G | White LED panels (general lighting) | 60W | Non-operational periods only |
| **Total peak (all on)** | | **475W** | Not all simultaneous |

**Energy per session (one print):** ~3.5 hours active → approximately 1.5–1.8 kWh consumed.

**Battery bank capacity:** 200Ah × 12V = 2,400 Wh (LiFePO4 usable to 100% DoD) → supports 1.3–1.6 full printing sessions from a full charge, with margin.

**Solar recharge:** 600W array × 5.5 peak sun hours (Palm Springs) = 3,300 Wh/day generated → full recharge from flat within one day; maintains charge with daily single-print use.

## 4. Solar Array
| Parameter | Specification |
|-----------|--------------|
| Panels | 3 × 200W monocrystalline, 12V nominal |
| Configuration | 3 panels in parallel (12V, 30A combined Isc) |
| Mounting | Ground-mounted tilt frame (30° from horizontal) or roof rack |
| Orientation | Due south (azimuth 180°) |
| Cable | 10 AWG PV cable, MC4 connectors |
| Combiner | 3-way MC4 branch connector + 30A inline fuse per string |
| Wall entry | Via flush-mount power panel (shared with shore power) — 280×180mm wall cutout |
| Approximate cost | ~$400 (panels) + ~$80 (mounting hardware) |

**Siting:** deploy panels on south-facing ground adjacent the container. Fro example, 30° tilt is optimal at Palm Springs latitude (33°N) for year-round average. If deploying in summer only, increase tilt to 20° for higher peak output.

## 5. Charge Controller and Battery Bank

### 5.1 Charge Controller
| Parameter | Specification |
|-----------|--------------|
| Model | Victron SmartSolar MPPT 100/50 |
| Max PV input | 100V OC, 50A charge current |
| Battery voltage | 12V auto-detect |
| Communication | Bluetooth (Victron Connect app) |
| Mounting | Interior short wall, adjacent main enclosure |
| Approximate cost | ~$200 |

The SmartSolar has a built-in load output (30A) for direct low-power 12V loads. The main high-current loads connect via the Blue Sea fuse block (see Section 10).

### 5.2 Battery Bank
| Parameter | Specification |
|-----------|--------------|
| Chemistry | LiFePO4 (lithium iron phosphate) |
| Configuration | 2 × 100Ah 12V in parallel (200Ah total) |
| Usable energy | 2,400 Wh (100% DoD — LiFePO4 does not require 50% reserve like lead-acid) |
| Temperature rating | −20°C to +60°C operating — suitable for interior of steel container in summer |
| Cycle life | 3,000–5,000 cycles to 80% capacity |
| BMS | Internal per-cell BMS (standard on Battle Born, Renogy LiFePO4 units) |
| Recommended brands | Battle Born 100Ah, Renogy 100Ah Smart Lithium |
| Approximate cost | ~$700 (two units) |

**Why LiFePO4 and not NMC or lead-acid:**
- LiFePO4 does not exhibit thermal runaway — safe in an enclosed steel container that may reach 60°C interior
- Full 100% depth of discharge usable (vs. 50% for lead-acid, 80% for NMC)
- 3,000+ cycle life supports frequent deployments without degradation
- No outgassing — can be used in an enclosed space without ventilation dedicated to the battery

### 5.3 Shore Power Backup Charger
| Parameter | Specification |
|-----------|--------------|
| Model | Victron Blue Smart IP65 12/15 |
| Input | 100–240V AC, NEMA 5-15 (standard US outlet) |
| Output | 12V DC, 15A (180W) |
| Full charge time from flat | ~14 hours (200Ah ÷ 15A) |
| Inlet | NEMA 5-15R weatherproof inlet in external power panel (pinhole wall exterior) |
| Approximate cost | ~$150 |

Connect whenever shore power is available at a deployment site (campground hookup, venue power, generator) to top up the battery bank overnight.

### 5.4 External Power Panel
The solar PV inputs and shore power inlet share a single **flush-mount power panel** set into a cutout in the pinhole wall, close to the electrical panel and battery bank inside.

| Parameter | Specification |
|-----------|--------------|
| Face plate | 3mm aluminum, 340×240mm |
| Wall cutout | 280×180mm (30mm overlap each side for secure bolting) |
| Weatherseal | 3mm neoprene gasket between plate and wall |
| Solar inputs | 3 × MC4 bulkhead connector pairs (IP67 panel-mount) |
| Shore power | 1 × NEMA 5-15R weatherproof inlet |
| Mounting | 4 × M6 bolts through plate, gasket, and wall |
| Location | Pinhole wall, X ≈ 1,250–1,550mm (just left of EP) |
| Approximate cost | ~$50 (plate $15 + gasket $5 + hardware $5 + MC4 bulkheads $25) |

The panel face sits flush with the exterior wall surface. A 280×180mm cutout allows all connector bodies to protrude directly into the container interior — no cable gland or junction box is needed. PV cables route to the MPPT charge controller; AC cable routes to the shore charger. The IP67 MC4 connectors and weatherproof NEMA inlet, combined with the perimeter neoprene gasket, provide a fully sealed exterior face. See the power panel detail drawing below.

![External Power Panel Detail](assets/power-panel-sheet1.png)

## 6. Light Trap — Revolving Drum

### 6.1 Function
The light trap allows a single operator to enter and exit the camera in full daylight during loading and development, without admitting any UV or visible light to the interior. TBS-001 uses a **revolving drum built into a hinged panel** — the full cargo door opening clears for IBC tote loading when the panel is swung open, and light-tight personnel access is retained when the panel is closed.

### 6.2 Hinged Panel Specification
| Parameter | Specification |
|-----------|--------------|
| Panel size | 2,362mm × 2,388mm |
| Frame | 50 × 50mm RHS steel, 120mm overall thickness |
| Skins | 18mm exterior-grade plywood each face, painted flat black interior |
| Hinges | 3 × 200mm stainless ball-bearing piano hinges — left edge of door opening |
| Latches | 4 × Southco C2-33 cam compression latches — perimeter |
| Perimeter seal | 20mm EPDM compression gasket in machined aluminum channel — zero-gap when latches engaged |
| Swing clearance | 180° outward — fully clears opening for IBC tote loading |

### 6.3 Revolving Drum Specification
| Parameter | Specification |
|-----------|--------------|
| Drum diameter | 750mm |
| Drum height | 2,000mm |
| Shell | 3mm mild steel, rolled and seam-welded |
| Baffles | 4 internal baffles at 45° offset — no direct line of sight at any rotation angle |
| Bearings | SKF 6215-2RS1, 75mm ID, top and bottom stub shafts |
| Seals | 12mm neoprene wiper seals (top/bottom); 20mm compression strip at drum-to-panel gap |
| Safelight | 12V red LED strip (circuit D), 3× ceiling strips + drum interior |
| Surface treatment | RAL 9005 matte powder coat — all interior surfaces |
| Fabrication | Custom — local metal fab shop. Full BOM in [Master Shopping List](master-shopping-list.md) §7 |

Operation: operator pushes the drum wall to enter, traverses one baffle sector, exits into the container interior — no tools, no light admission.

### 6.4 Fabrication Drawings
**Sheet 1 — Front Elevation (1:20): Panel Dimensions, Drum, Hinges, Latches**
![TBS-001 Hinged Panel — Sheet 1: Front Elevation](assets/hingepanel-sheet1.png)

**Sheet 2 — Plan Cross-Section (1:10 horiz / 1:1 depth): Drum Baffles and Light Path**
![TBS-001 Hinged Panel — Sheet 2: Plan Cross-Section](assets/hingepanel-sheet2.png)

**Sheet 3 — Drum Vertical Section Elevation (Section A-A)**
![TBS-001 Hinged Panel — Sheet 3: Drum Elevation](assets/hingepanel-sheet3.png)

### 6.5 Light-Leak Test
After installation, perform the inspection in Phase 0.7 of the Operating Manual. **Target: zero light visible after 15-minute dark adaptation with drum in service position and panel latched.**

### 6.6 Commercial Light Trap Options (Reference)
Custom fabrication is the recommended approach. Commercial revolving doors are not weatherproof or transport-rated for field deployment:

| Option | Diameter | Price (USD) | Recommended? |
|--------|----------|------------|--------------|
| Vario LT-800 / Octanorm type | 800mm | $2,500–$3,500 | No — no weatherproofing, not panel-mount compatible |
| Porta-Fab DK series | 750–900mm | $3,000–$4,500 | No — requires panel-bay frame, cost premium |
| **Custom fabrication (3mm steel, SKF 6215)** | **750mm** | **$950–$1,450** | **Yes — field-rated, IP44, panel bolt-in** |

Full raw material supplier list, bearing specification, and seal specification are in the [Light Trap Selection Report](light-trap-selection.md).

### 6.7 Ventilation Diagrams
**Sheet 1 — Container Ventilation Section**
![TBS-001 Ventilation — Sheet 1: Container Longitudinal Section](assets/lighttrap-sheet1.png)

**Sheet 2 — Fan & Baffle Duct Assembly**
![TBS-001 Ventilation — Sheet 2: Fan & Baffle Duct Assembly](assets/lighttrap-sheet2.png)

### 6.8 Container Floor Plan — All Systems
Top-down schematic of the full TBS-001 interior at 1:75 scale, showing all systems in their real positions. Equipment occupies provably shadow-free end zones. The optical zone (X=150–4,649mm) contains the processing tray and perimeter walkways at floor level.

![TBS-001 Container Floor Plan — All Systems](assets/container-floorplan.png)

**Left end zone (X=0–150mm) — shadow-free at all depths:**
- Light trap drum (Ø750mm, centered at X=0, Yd=806–1,556mm)

**Pinhole wall face (Yd=0):**
- Evap duct penetration (Ø200mm at X=1,200mm, Z=2,100mm) — cooler is external
- Electrical enclosure (X=1,600–1,900mm, H=900–1,500mm) — wall-mounted
- LiFePO4 battery bank (X=1,600–2,100mm, H=0–500mm) — wall-mounted

**Equipment panel (Yd=1,046, IBC corridor):**
- Pump manifold (X=4,800–5,580mm, Z=900–1,400mm) — panel-mounted

**Optical zone (X=150–4,649mm):** Processing tray (permanent, X=170–4,629mm) and perimeter walkway (removable, 300mm wide around all 4 sides) at floor level. Rails at X=150 and X=4,649.

**Right end zone (X=4,649–5,893mm) — shadow-free at all depths:**
- 2 × Blue IBC totes (600L each), Y-stacked (front), X=4,674mm
- 1 × Brown IBC tote (600L), Y-stacked (rear), X=4,674mm

All equipment clears the optical cone at every depth — no vignetting. See [Equipment Layout Report](equipment-layout-report.md) for the shadow-free proof.

## 7. Cooling System

> **Full specification:** See [Ventilation & Cooling Report](ventilation-report.md) for the complete consolidated system design, parts list, and maintenance schedule.

### 7.1 The Problem
A 20ft ISO steel container in direct Palm Springs summer sun (ambient 40–45°C, direct irradiance 1,000 W/m²) reaches interior temperatures of 65–75°C without intervention. An operator cannot safely work under 40°C interior. Chemistry coating is impaired above 35°C.

### 7.2 Strategy
| Method | Interior ΔT | Cost | Power | Required? |
|--------|------------|------|-------|-----------|
| 80% shade cloth canopy over container | −15 to −20°C | ~$300 | None | **Yes — always** |
| Scheduling (shoot before 09:00 / after 18:00 in summer) | −10 to −15°C effective | $0 | None | Recommended |
| 12V DC evaporative cooler (swamp cooler) | −10 to −15°C additional | ~$300 | 80W | **Yes — in temperatures above 30°C ambient** |

Combined (shade canopy + cooler + scheduling): interior temperature reaches 25–32°C — within operator working range.

> **Why evaporative cooling works in Hot Climates (e.g. Palm Springs):** Evaporative (swamp) cooling is most effective when ambient relative humidity is low. Palm Springs in summer averages 10–18% RH — optimal for this technology. At 15% RH and 42°C ambient, an evaporative cooler can reduce temperature by 15–18°C, bringing 42°C down to 24–27°C after the shade canopy's contribution. At the same conditions, a standard 9,000 BTU mini-split uses 900W vs. the evaporative cooler's 80W — an 11× power saving.

### 7.3 Evaporative Cooler Specification
| Parameter | Specification |
|-----------|--------------|
| Model | Portacool Jetstream 110 (12V DC version) or equivalent |
| Power draw | ~80W at 12V DC |
| Airflow | ~300 CFM |
| Water consumption | ~3 liters/hour |
| Circuit | E (10A fuse, 14 AWG) |
| Intake | Light-safe baffle (see 7.4) |
| Water source | Dedicated 20-liter reservoir, refilled from Blue circuit IBC tote |

### 7.4 Light-Safe Cooler Intake
The cooler is mounted externally on the pinhole wall exterior. Cooled air enters through a Ø200mm insulated duct penetration at X=1,200mm, Z=2,100mm. The penetration includes a light-safe baffle to prevent light ingress:

- **Duct size:** 200mm (8") — sized for ~300 CFM at low velocity
- **Penetration:** through the pinhole wall (Yd=0 face) at X=1,200mm, Z=2,100mm
- **Interior baffles:** two 200 × 200mm flat steel baffles, offset 100mm, mounted inside a 300mm duct stub — breaks the direct light path while allowing unrestricted airflow
- **Exterior:** cooler unit direct-coupled to duct with weatherproof housing

## 8. Ventilation Upgrade

> **Full specification:** See [Ventilation & Cooling Report](ventilation-report.md) for fan positions, baffle duct construction, operating modes, and panel integration details.

The original construction guide specifies 2 × 4" (100mm) inline fans. For operator comfort during processing in warm conditions, upgrade to 6" (150mm):

| Parameter | Original | Upgraded |
|-----------|---------|---------|
| Fan diameter | 4" (100mm) | 6" (150mm) |
| Airflow per fan | ~100 CFM | ~200 CFM |
| Total airflow | ~200 CFM | ~400 CFM |
| Power draw (each) | ~30W | ~60W |
| Circuit fuse | 3A | 5A |
| Additional cost | — | ~$60 |

**Installation:** Same light-baffle design as original — L-shaped offset baffles inside a duct stub. Fan A (intake) is low on the far end wall (X=C_LEN, draws in cooler air near floor level). Fan B (exhaust) is mounted on the hinged panel (far corner zone, Yd=2,287mm, H=1,800mm) with its baffle duct protruding from the panel exterior face. During operation the cargo doors are open (personnel access is via the revolving light trap drum), so the exhaust discharges directly into the open doorway. Fan B moves with the panel on the sliding carriage; wiring uses a flexible coiled cable from the fixed door frame (see §10.3). Cross-flow ventilation diagonal: low intake at far end → high exhaust at cargo door end.

**Operating modes:**
| Mode | Intake | Exhaust |
|------|--------|---------|
| Exposure | OFF | OFF |
| Loading / development | Low speed | Low speed |
| Post-session ventilation | Full speed | Full speed |
| Pre-cooling (before entry) | Full speed | Full speed |

## 9. Interior Lighting

### 9.1 Two-Circuit Lighting Design
TBS-001 requires two mutually exclusive lighting modes:

- **Safelight (Circuit D):** Three red LED strips ceiling-mounted running north–south (across the container width) at X≈600mm, X≈1,800mm, and X≈4,100mm, plus a strip on the inner drum face. Each strip runs from Yd=0 (pinhole wall) and is shortened to stay clear of the optical cone at its X position: the near-door strip (X=600) stops at Yd≈1,800mm; the other two stop at Yd≈2,100mm. Used during loading and development when photosensitive material is present. 15W, always available.
- **White light (Circuit G):** General-purpose white/natural LED panels for setup, maintenance, cleaning, and any non-operational work. 60W total. Must be switched off before any photosensitive material is exposed.

The two circuits are independently switched — they are **not** interlocked, so the operator is responsible for ensuring Circuit G is off during operational phases. The pull-cord switches are positioned side by side for easy identification.

### 9.2 White LED Panel Specification
| Parameter | Specification |
|-----------|--------------|
| Type | 12V DC LED flat panel, 4000K neutral white |
| Quantity | 3 panels |
| Power per panel | 20W |
| Total power | 60W |
| Luminous output | ~1,800 lumens per panel (5,400 lm total) |
| Size | ~300 × 600 mm |
| Mounting | Ceiling-mounted, centered across container width (Yd ≈ 1,181mm) |
| Positions | X ≈ 1,000mm, X ≈ 2,900mm, X ≈ 4,800mm (evenly spaced along length) |
| Circuit | G (10A fuse, 16 AWG) |
| Approximate cost | ~$25 each, ~$75 total |

Three panels at ~1,800 lumens each provide 5,400 lumens total across the ~14 m² floor area — approximately 385 lux, comparable to a well-lit workshop. The panels are wired in parallel from Circuit G via the ceiling cable trunking.

### 9.3 Pull-Cord Switches
Two ceiling-mounted pull-cord switches are installed on the pinhole wall side of the container, accessible from the near walkway. Each switch controls one lighting circuit.

| Parameter | Specification |
|-----------|--------------|
| Type | 12V DC SPST pull-cord ceiling switch, 6A rated |
| Quantity | 2 |
| Position | Pinhole wall face (Yd ≈ 0), X ≈ 1,750mm (near electrical panel), ceiling height |
| Switch 1 | Circuit D — safelight (red). Cord labeled "RED" |
| Switch 2 | Circuit G — white light. Cord labeled "WHITE" |
| Wire | Inline on respective circuit, between fuse block and load |
| Approximate cost | ~$8 each, ~$16 total |

The switches are positioned near the electrical panel, accessible from the near walkway. Pull-cord length is set so the cord hangs at approximately 1,500mm above the walkway deck — reachable without stretching.

## 10. Wiring Specification

### 10.1 Main Enclosure
IP65 weatherproof enclosure, 300 × 200 × 130mm, mounted on the interior pinhole wall face (Y=0, X≈2,050–2,350mm). Contains:
- Victron MPPT controller (or external, hardwired)
- Blue Sea 5026 12-circuit fuse block with busbars
- Battery positive and negative busbars with 200A main fuse
- Shore charger output terminals

### 10.2 Circuit List
| Circuit | Device | Fuse | Wire gauge | Run length |
|---------|--------|------|-----------|-----------|
| A | Ventilation fan — intake | 5A | 16 AWG | ~3m |
| B | Ventilation fan — exhaust (panel-mounted) | 5A | 16 AWG | ~8m + flex connector |
| C | Water pumps P-01–P-04 (P-03 in IBC corridor, longer run) | 15A | 14 AWG | ~5m (manifold) / ~8m (P-03) |
| D | Safelight (3× ceiling strips + drum) | 5A | 18 AWG | ~15m (3 branches + drum) |
| E | Evaporative cooler | 10A | 14 AWG | ~4m |
| F | Film plane actuators (optional) | 20A | 12 AWG | ~6m |
| G | White LED panels (general lighting) | 10A | 16 AWG | ~12m (3 branches) |
| — | Main battery fuse | 200A | 2/0 AWG | ~0.5m (battery to busbar) |

### 10.3 Wiring Construction
**Conduit:** All DC wiring in grey corrugated conduit (Panduit or equivalent). Route in flat-profile cable trunking along the top corner rail of the container (40 × 25mm PVC trunking, UV-stabilized).

**Connectors:**
- Interior connections: Anderson Powerpole 30A (red/black) — tool-free, industry standard for 12V DC
- Exterior penetrations (fans, cooler intake, shore inlet): Deutsch DT series 2-pin weatherproof connectors — IP67 rated
- **Circuit B flex connector (panel-mounted exhaust fan):** Fan B is mounted on the sliding hinged panel. The wire run from the fuse block routes along the ceiling trunking to the fixed door frame, then crosses to the panel via a 1m coiled cable (16 AWG, 2-conductor, silicone-jacketed) with Deutsch DT 2-pin connectors at each end. The coiled cable must accommodate 300mm of panel slide travel plus 180° panel swing without binding. Anchor the fixed end to the door frame top rail; anchor the panel end to the carriage beam. Service loop hangs in the ceiling zone above H=2,200mm.

**Grounding:** Bond the container steel body to the battery negative busbar using 4 AWG green/yellow wire at the main enclosure. Drive an 8-foot copper ground stake at the container foundation and connect to the main enclosure earth terminal.

**Labelling:** Brady M210 wire labels at every terminal and every connector. Labels follow the circuit letter scheme (A–G) plus device description. Re-label after any wiring change.

### 10.4 Electrical Diagrams
**Sheet 1 — System One-Line Diagram**
Complete power flow from solar panels through controller, battery bank, fuse block, and out to each circuit. Wire gauges, fuse ratings, and component models labelled.

![TBS-ELEC Sheet 1 — System One-Line Diagram](assets/electrical-sheet1.png)

**Sheet 2 — Container Wiring Layout**
Top-down floor plan (1:60 scale) showing all component positions, conduit routes, penetrations, drum panel, and connection points.

![TBS-ELEC Sheet 2 — Container Wiring Layout](assets/electrical-sheet2.png)

**Sheet 3 — Pinhole Wall Interior Elevation**
Interior elevation of the pinhole wall face (Yd=0), looking from inside the container. Shows equipment mounting heights, cable trunking at the ceiling corner rail, drop conduits to each device, pull-cord switch positions with cord lengths, and ceiling-mounted LED panel locations.

![TBS-ELEC Sheet 3 — Pinhole Wall Interior Elevation](assets/electrical-sheet3.png)

## 11. Parts List
All US/SoCal sources. Prices approximate as of 2026.

| Item | Spec | Source | Est. cost |
|------|------|--------|-----------|
| Solar panels | 200W mono × 3 | Renogy (renogy.com), Amazon | ~$400 |
| MPPT charge controller | Victron SmartSolar MPPT 100/50 | altE Store (altestore.com) | ~$200 |
| LiFePO4 battery × 2 | 100Ah 12V (Battle Born or Renogy) | battleborncotteries.com / renogy.com | ~$700 |
| Shore backup charger | Victron Blue Smart IP65 12/15 | altE Store | ~$150 |
| Fuse block | Blue Sea 5026 ST Blade 12-circuit | West Marine (Torrance CA) / Amazon | ~$55 |
| 200A main fuse + holder | Blue Sea ANL fuse block | Amazon | ~$30 |
| Wiring kit | 14/16/18 AWG, 50ft each colour | Amazon / Waytek Wire (waytekwire.com) | ~$80 |
| Anderson Powerpole connectors | 30A kit, 50 pairs | Powerwerx (powerwerx.com) | ~$40 |
| Deutsch DT connectors | DT 2-pin, 10 sets | Waytek Wire | ~$30 |
| Cable trunking | 40 × 25mm PVC, 5m lengths × 4 | Lowe's / McMaster-Carr | ~$40 |
| Corrugated conduit | Grey, 10mm ID, 10m | McMaster-Carr 7828K48 | ~$30 |
| IP65 enclosure | 300 × 200 × 130mm | Polycase / Amazon | ~$60 |
| Brady label kit | M210 with wire label cartridge | McMaster-Carr / Amazon | ~$80 |
| NEMA 5-15R inlet | Weatherproof outlet box | Leviton / Amazon | ~$25 |
| Copper ground stake | 8ft × 5/8" diameter | Home Depot | ~$20 |
| 4 AWG ground wire | Green/yellow, 3m | AutoZone / Amazon | ~$15 |
| Evaporative cooler | 12V DC, ~300 CFM | Portacool / Amazon | ~$280 |
| Shade canopy | 80% shade cloth, 20 × 10ft | Amazon / Farm supply | ~$80 |
| Canopy frame | 1.5" EMT conduit + fittings | Home Depot | ~$120 |
| 6" inline fans × 2 | 12V DC, ~200 CFM each | Amazon (AC Infinity S6) | ~$120 |
| 12V LED flat panel, 300×600mm, 4000K | 20W, neutral white, ceiling-mount | Amazon / superbrightleds.com | ~$75 (×3) |
| Pull-cord ceiling switch, 12V 6A SPST | Inline switch for lighting circuits D & G | Amazon / Lowe's | ~$16 (×2) |
| **Electrical system total** | | | **~$1,830** |
| **Shade canopy total** | | | **~$200** |
| **Cooling (evap cooler)** | | | **~$280** |
| **Systems grand total** | | | **~$2,310** |

## 12. Impact on Existing Design
| Existing element | Change required |
|-----------------|----------------|
| Ventilation fans (4") | Replace with 6" units — same baffle design, same penetration locations |
| 12V fuse block ($50 item in water system BOM) | Superseded by Blue Sea 5026 — consolidates all circuits in one panel |
| Battery-powered safelight | Wired to circuit D — no separate battery required |
| Water pump power (P-01–P-04; P-03 relocated to IBC corridor) | Now circuit C on main fuse block — remove standalone 12V supply listed in water report. P-03 wire run is longer (~8m to IBC corridor) |
| Container doors | Replaced by hinged drum panel — cargo doors removed from their hinges for transport |

---

## 13. Maintenance

| Interval | Task |
|----------|------|
| Before each session | Check battery state of charge via Victron Connect app |
| Before each session | Verify all circuit fuses are intact on Blue Sea 5026 fuse block |
| Before each session | Test safelight (Circuit D) and white light (Circuit G) switches |
| Monthly | Inspect Anderson Powerpole connections for corrosion or looseness |
| Monthly | Check cable trunking clips and conduit routing for chafe |
| Monthly | Inspect Deutsch DT weatherproof connectors at fan and cooler penetrations |
| Every 6 months | Clean solar panel surfaces; check MC4 connector seals |
| Every 6 months | Inspect EPDM gasket on external power panel for compression set |
| Annually | Test battery BMS function (charge/discharge cycle under monitoring) |
| Annually | Inspect ground stake connection and measure earth resistance |
| Annually | Check pull-cord switch mechanisms for wear |
| Before transport | Disconnect evaporative cooler and stow per [Equipment Layout](equipment-layout-report.md) §6.2 |
| Before transport | Verify all circuit breakers/fuses are off except safelight standby |

---

## 14. Source References

1. [Victron SmartSolar MPPT 100/50](https://www.victronenergy.com/solar-charge-controllers/smartsolar-mppt-100-50) — MPPT charge controller specifications.
2. [Victron Blue Smart IP65 12/15](https://www.victronenergy.com/chargers/blue-smart-ip65-charger) — Shore power backup charger specifications.
3. [Blue Sea 5026 ST Blade Fuse Block](https://www.bluesea.com/products/5026/ST_Blade_Fuse_Block_-_12_Circuits_with_Negative_Bus_and_Cover) — 12-circuit fuse block specifications.
4. [Battle Born 100Ah LiFePO4](https://battlebornbatteries.com/product/100ah-12v-lifepo4-deep-cycle-battery/) — LiFePO4 battery specifications.
5. [Light Trap Selection Report](light-trap-selection.md) — Revolving drum specification and commercial options evaluation.
6. [Hinged Panel Report](hinged-panel-report.md) — Panel construction, hinge, latch, and sliding carriage specification.
7. [Water System Report](water-system-report.md) — Pump circuits and water system electrical integration.
8. [Equipment Layout Report](equipment-layout-report.md) — Component positions and shadow-free zone verification.

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*