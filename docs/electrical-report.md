# Electrical & Systems Report — TBS-001

**Covers:** solar power architecture, battery bank, light trap vestibule, cooling, ventilation upgrade, wiring specification, and electrical diagrams.

See also: [Operating Manual](operating-manual.md) for step-by-step operational procedures.

---

## 1. System Overview

TBS-001 is designed for fully off-grid operation. All power comes from a rooftop/ground-mounted solar array charging a LiFePO4 battery bank. Shore power (mains) is accommodated as an optional backup charging input only — the system operates identically without it.

All loads run at **12V DC**. There is no mains AC distribution inside the container.

```
Solar panels (3 × 200W)
  → Victron SmartSolar MPPT 100/50 charge controller
  → 12V / 200Ah LiFePO4 battery bank ←── Victron IP65 12/15 shore charger (optional)
  → Blue Sea 5026 fuse block
  → Circuits A–F (ventilation, pump, safelight, cooling, actuators)
```

See [Section 8.4](#84-electrical-diagrams) for embedded diagrams.

---

## 2. Power Budget

| Circuit | Device | Peak draw | Duty cycle |
|---------|--------|-----------|-----------|
| A | Ventilation fan — intake (6") | 60W | Continuous during processing |
| B | Ventilation fan — exhaust (6") | 60W | Continuous during processing |
| C | Water pump (12V DC) | 100W | Intermittent (~30 min/print) |
| D | Safelight — interior + vestibule | 15W | Loading phase only (~45 min) |
| E | Evaporative cooler (12V DC) | 80W | Continuous during operation |
| F | Film plane actuators (optional) | 100W peak | Intermittent |
| **Total peak (all on)** | | **415W** | Not all simultaneous |

**Energy per session (one print):** ~3.5 hours active → approximately 1.5–1.8 kWh consumed.

**Battery bank capacity:** 200Ah × 12V = 2,400 Wh (LiFePO4 usable to 100% DoD) → supports 1.3–1.6 full printing sessions from a full charge, with margin.

**Solar recharge:** 600W array × 5.5 peak sun hours (Palm Springs) = 3,300 Wh/day generated → full recharge from flat within one day; maintains charge with daily single-print use.

---

## 3. Solar Array

| Parameter | Specification |
|-----------|--------------|
| Panels | 3 × 200W monocrystalline, 12V nominal |
| Configuration | 3 panels in parallel (12V, 30A combined Isc) |
| Mounting | Ground-mounted tilt frame (30° from horizontal) or roof rack |
| Orientation | Due south (azimuth 180°) |
| Cable | 10 AWG PV cable, MC4 connectors |
| Combiner | 3-way MC4 branch connector + 30A inline fuse per string |
| Approximate cost | ~$400 (panels) + ~$80 (mounting hardware) |

**Siting:** deploy panels on south-facing ground adjacent the container. A 30° tilt is optimal at Palm Springs latitude (33°N) for year-round average. If deploying in summer only, increase tilt to 20° for higher peak output.

---

## 4. Charge Controller and Battery Bank

### 4.1 Charge Controller

| Parameter | Specification |
|-----------|--------------|
| Model | Victron SmartSolar MPPT 100/50 |
| Max PV input | 100V OC, 50A charge current |
| Battery voltage | 12V auto-detect |
| Communication | Bluetooth (Victron Connect app) |
| Mounting | Interior short wall, adjacent main enclosure |
| Approximate cost | ~$200 |

The SmartSolar has a built-in load output (30A) for direct low-power 12V loads. The main high-current loads connect via the Blue Sea fuse block (see Section 7).

### 4.2 Battery Bank

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

### 4.3 Shore Power Backup Charger

| Parameter | Specification |
|-----------|--------------|
| Model | Victron Blue Smart IP65 12/15 |
| Input | 100–240V AC, NEMA 5-15 (standard US outlet) |
| Output | 12V DC, 15A (180W) |
| Full charge time from flat | ~14 hours (200Ah ÷ 15A) |
| Inlet | NEMA 5-15R weatherproof outlet on exterior short wall |
| Approximate cost | ~$150 |

Connect whenever shore power is available at a deployment site (campground hookup, venue power, generator) to top up the battery bank overnight.

---

## 5. Light Trap Vestibule

### 5.1 Function

The vestibule allows a single operator to enter and exit the camera in full daylight during loading and development, without admitting any UV or visible light to the interior. It replaces the "fabric anteroom" approach noted in the construction guide with a permanent, structurally attached enclosure.

### 5.2 Specification

| Parameter | Specification |
|-----------|--------------|
| Footprint (external) | 1,200mm deep × 2,400mm wide × 2,500mm tall |
| Frame | 40 × 40mm RHS steel, hot-dip galvanised |
| Attachment | 8 × M10 bolts to container corner castings — no welding, fully removable |
| Wall/roof cladding | 18mm exterior-grade plywood, painted flat black interior, weatherproof exterior |
| Exterior door | 900 × 2,000mm, outward-opening, compression latch, weatherstripped |
| Interior light seal | 3 layers Rosco Duvetyne (100% blackout, same spec as film plane seal), hung on Velcro tabs — minimum 200mm overlap per layer |
| S-path baffles | 2 × floor-to-ceiling sheet steel baffles (300mm projection from each side wall), painted flat black. Baffles offset so no direct line of sight exists from exterior to container at any angle |
| Safelight | 12V red LED strip (circuit D), 200mm above door frame, switched from inside |
| Ventilation stub | 4" duct stub with weatherproof cap on exterior wall — connects to container ventilation circuit during processing phases; capped during loading |

### 5.3 Construction Sequence

1. Weld the RHS steel frame (or have it pre-fabricated) — four vertical posts, top plate, cross-bracing. Galvanise before installation.
2. Bolt frame to container corner castings using M10 × 50mm hex bolts with flat washers and spring washers.
3. Fix plywood cladding to frame with self-tapping TEK screws. Seal all exterior joints with weatherproof sealant.
4. Paint all interior surfaces flat black (zero-sheen). Two coats.
5. Fit the exterior door with piano hinge (full-length) and compression latch.
6. Install the two internal S-path baffles on opposite walls.
7. Hang Duvetyne blackout curtains on Velcro rails — three layers, each offset 200mm.
8. Wire safelight strip (circuit D branch) — run conduit from main panel through a sealed penetration in the container short wall.

### 5.4 Light-Leak Test

After installation, perform the inspection in Phase 0.7 of the Operating Manual. **Target: zero light visible after 15-minute dark adaptation with outer door closed and container door open.**

### 5.5 Impact on Existing Design

- The vestibule attaches to existing ISO corner castings — no modification to the container structure required.
- Container cargo doors and seals are unchanged.
- The vestibule adds 1,200mm to the container footprint at the door end — confirm this fits the deployment site.
- When transporting, remove the vestibule (8 bolts) and carry flat inside the container or on a separate vehicle.

### 5.6 Light Trap & Ventilation Diagrams

**Sheet 1 — Vestibule Plan (1:100) and S-Path Detail**
![TBS-001 Light Trap — Sheet 1: Vestibule Plan](assets/lighttrap-sheet1.png)

---

**Sheet 2 — Container Ventilation Section and Fan Baffle Detail**
![TBS-001 Light Trap — Sheet 2: Ventilation Section](assets/lighttrap-sheet2.png)

### 5.7 Hinged Panel & Commercial Light Trap Options

The S-path vestibule described in Sections 5.1–5.6 provides a fixed personnel entry. An improved design replaces it with a **hinged panel incorporating a revolving light trap drum** — allowing the full cargo door opening to be cleared for equipment loading, while retaining light-tight personnel access when the panel is closed.

**Hinged panel design:**
The panel (2,362mm × 2,388mm, 50×50mm RHS steel frame, 18mm ply skins, 120mm overall thickness) is hung on three 200mm stainless ball-bearing piano hinges at the left edge of the door opening. Four Southco C2-33 cam compression latches seal the perimeter. A 20mm EPDM compression gasket in a machined aluminium channel provides zero-gap light-seal when the latches are engaged. The panel swings 180° outward to fully clear the opening for IBC tote loading.

A 750mm diameter × 2,000mm tall revolving drum (3mm steel, 4 internal baffles, SKF 6215 sealed bearings top and bottom) is built into the panel centre. Operators push the drum wall to enter, traverse one baffle sector, and exit into the container interior — no tools, no light admission.

**Sheet 1 — Front Elevation (1:20): Panel Dimensions, Drum, Hinges, Latches**
![TBS-001 Hinged Panel — Sheet 1: Front Elevation](assets/hingepanel-sheet1.png)

---

**Sheet 2 — Plan Cross-Section (1:10 horiz / 1:1 depth): Drum Baffles and Light Path**
![TBS-001 Hinged Panel — Sheet 2: Plan Cross-Section](assets/hingepanel-sheet2.png)

---

**Commercial revolving light trap options** are documented and costed in the [Light Trap Selection Report](light-trap-selection.md):

| Option | Diameter | Price (USD) | Recommended? |
|--------|----------|------------|--------------|
| Vario LT-800 / Octanorm type | 800mm | $2,500–$3,500 | No — no weatherproofing, not panel-mount compatible |
| Porta-Fab DK series | 750–900mm | $3,000–$4,500 | No — requires panel-bay frame, cost premium |
| **Custom fabrication (3mm steel, SKF 6215)** | **750mm** | **$950–$1,450** | **Yes — field-rated, IP44, panel bolt-in** |

Custom fabrication is the recommended approach. Full raw material supplier list, bearing specification, and seal specification are in the [Light Trap Selection Report](light-trap-selection.md).

### 5.8 Container Floor Plan — All Systems

Top-down schematic of the full TBS-001 interior at 1:75 scale, showing all systems in their real positions. Equipment occupies provably shadow-free end zones. The optical zone (X=1,100–4,649mm) is completely clear.

![TBS-001 Container Floor Plan — All Systems](assets/container-floorplan.png)

**Left end zone (X=0–1,100mm) — shadow-free at all depths:**
- Light trap drum (Ø750mm, centred at X=0)
- 12V evaporative cooler (X=400–1,000mm, Yd=100–450mm)
- 2 × 55-gal HDPE drums, Z-stacked, X=700mm CX, Yd=475–1,055mm

**Pinhole wall face (Y=0):**
- Electrical enclosure (X=2,050–2,350mm, H=900–1,500mm) — wall-mounted
- LiFePO4 battery bank (X=2,050–2,550mm, H=0–500mm) — wall-mounted
- Pump manifold (X=2,400–2,700mm, H=200–600mm) — wall-mounted

**Optical zone (X=1,100–4,649mm):** Nothing at floor level. Rails only.

**Right end zone (X=4,649–5,893mm) — shadow-free at all depths:**
- 2 × Blue IBC totes (600L each), Y-stacked (front), X=4,674mm
- 1 × Brown IBC tote (600L), Y-stacked (rear), X=4,674mm

All equipment clears the optical cone at every depth — no vignetting. See [Equipment Layout Report](equipment-layout-report.md) for the shadow-free proof.

---

## 6. Cooling System

### 6.1 The Problem

A 20ft ISO steel container in direct Palm Springs summer sun (ambient 40–45°C, direct irradiance 1,000 W/m²) reaches interior temperatures of 65–75°C without intervention. An operator cannot safely work above 40°C interior. Chemistry coating is impaired above 35°C.

### 6.2 Strategy

| Method | Interior ΔT | Cost | Power | Required? |
|--------|------------|------|-------|-----------|
| 80% shade cloth canopy over container | −15 to −20°C | ~$300 | None | **Yes — always** |
| Scheduling (shoot before 09:00 / after 18:00 in summer) | −10 to −15°C effective | $0 | None | Recommended |
| 12V DC evaporative cooler (swamp cooler) | −10 to −15°C additional | ~$300 | 80W | **Yes — in temperatures above 30°C ambient** |

Combined (shade canopy + cooler + scheduling): interior temperature reaches 25–32°C — within operator working range.

> **Why evaporative cooling works in Palm Springs:** Evaporative (swamp) cooling is most effective when ambient relative humidity is low. Palm Springs in summer averages 10–18% RH — optimal for this technology. At 15% RH and 42°C ambient, an evaporative cooler can reduce temperature by 15–18°C, bringing 42°C down to 24–27°C after the shade canopy's contribution. At the same conditions, a standard 9,000 BTU mini-split uses 900W vs. the evaporative cooler's 80W — an 11× power saving.

### 6.3 Evaporative Cooler Specification

| Parameter | Specification |
|-----------|--------------|
| Model | Portacool Jetstream 110 (12V DC version) or equivalent |
| Power draw | ~80W at 12V DC |
| Airflow | ~300 CFM |
| Water consumption | ~3 litres/hour |
| Circuit | E (10A fuse, 14 AWG) |
| Intake | Light-safe baffle (see 6.4) |
| Water source | Dedicated 20-litre reservoir, refilled from Blue circuit IBC tote |

### 6.4 Light-Safe Cooler Intake

The cooler is positioned in the left end zone (X=400–1,000mm, Yd=100–450mm). Its
intake duct must not admit light. Use the same offset-baffle design as the existing ventilation:

- **Duct size:** 6" (150mm) — matches cooler inlet
- **Penetration:** through the container left short end wall (X=0 face), positioned 400mm above floor level (within left end zone)
- **Interior baffles:** two 150 × 150mm flat steel baffles, offset 75mm, mounted inside a 250mm duct stub — breaks the direct light path while allowing unrestricted airflow at 300 CFM
- **Exterior:** weatherproof louvre with mesh screen to exclude insects

---

## 7. Ventilation Upgrade

The original construction guide specifies 2 × 4" (100mm) inline fans. For operator comfort during processing in warm conditions, upgrade to 6" (150mm):

| Parameter | Original | Upgraded |
|-----------|---------|---------|
| Fan diameter | 4" (100mm) | 6" (150mm) |
| Airflow per fan | ~100 CFM | ~200 CFM |
| Total airflow | ~200 CFM | ~400 CFM |
| Power draw (each) | ~30W | ~60W |
| Circuit fuse | 3A | 5A |
| Additional cost | — | ~$60 |

**Installation:** Same light-baffle design as original — L-shaped offset baffles inside a duct stub. Intake fan is low on the vestibule-end short wall (draws in cooler air near floor level). Exhaust fan is high on the far short wall (expels hot air near ceiling). Cross-flow ventilation.

**Operating modes:**

| Mode | Intake | Exhaust |
|------|--------|---------|
| Exposure | OFF | OFF |
| Loading / development | Low speed | Low speed |
| Post-session ventilation | Full speed | Full speed |
| Pre-cooling (before entry) | Full speed | Full speed |

---

## 8. Wiring Specification

### 8.1 Main Enclosure

IP65 weatherproof enclosure, 300 × 200 × 130mm, mounted on the interior short wall adjacent to the vestibule door. Contains:
- Victron MPPT controller (or external, hardwired)
- Blue Sea 5026 12-circuit fuse block with busbars
- Battery positive and negative busbars with 200A main fuse
- Shore charger output terminals

### 8.2 Circuit List

| Circuit | Device | Fuse | Wire gauge | Run length |
|---------|--------|------|-----------|-----------|
| A | Ventilation fan — intake | 5A | 16 AWG | ~3m |
| B | Ventilation fan — exhaust | 5A | 16 AWG | ~8m |
| C | Water pump | 15A | 14 AWG | ~5m |
| D | Safelight (interior + vestibule) | 5A | 18 AWG | ~10m (incl. vestibule branch) |
| E | Evaporative cooler | 10A | 14 AWG | ~4m |
| F | Film plane actuators (optional) | 20A | 12 AWG | ~6m |
| — | Main battery fuse | 200A | 2/0 AWG | ~0.5m (battery to busbar) |

### 8.3 Wiring Construction

**Conduit:** All DC wiring in grey corrugated conduit (Panduit or equivalent). Route in flat-profile cable trunking along the top corner rail of the container (40 × 25mm PVC trunking, UV-stabilised).

**Connectors:**
- Interior connections: Anderson Powerpole 30A (red/black) — tool-free, re-mateable, industry standard for 12V DC
- Exterior penetrations (fans, cooler intake, shore inlet): Deutsch DT series 2-pin weatherproof connectors — IP67 rated

**Grounding:** Bond the container steel body to the battery negative busbar using 4 AWG green/yellow wire at the main enclosure. Drive an 8-foot copper ground stake at the container foundation and connect to the main enclosure earth terminal.

**Labelling:** Brady M210 wire labels at every terminal and every connector. Labels follow the circuit letter scheme (A–F) plus device description. Re-label after any wiring change.

### 8.4 Electrical Diagrams

**Sheet 1 — System One-Line Diagram**

Complete power flow from solar panels through controller, battery bank, fuse block, and out to each circuit. Wire gauges, fuse ratings, and component models labelled.

![TBS-ELEC Sheet 1 — System One-Line Diagram](assets/electrical-sheet1.png)

---

**Sheet 2 — Container Wiring Layout**

Top-down floor plan (1:60 scale) showing all component positions, conduit routes, penetrations, vestibule, and connection points.

![TBS-ELEC Sheet 2 — Container Wiring Layout](assets/electrical-sheet2.png)

---

## 9. Shopping List

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
| RHS steel 40×40mm | 3m lengths for vestibule frame | Metal Supermarkets (Gardena CA) | ~$200 |
| Exterior-grade plywood | 18mm, 4'×8' sheets × 6 | Home Depot | ~$240 |
| Rosco Duvetyne | 60" wide × 5 yards per layer × 3 | Rose Brand (rosebrand.com, Burbank CA) | ~$180 |
| Compression latch | Heavy-duty exterior | McMaster-Carr 1765A12 | ~$45 |
| **Electrical system total** | | | **~$1,740** |
| **Light trap vestibule total** | | | **~$780** |
| **Shade canopy total** | | | **~$200** |
| **Cooling (evap cooler)** | | | **~$280** |
| **Systems grand total** | | | **~$3,000** |

---

## 10. Impact on Existing Design

| Existing element | Change required |
|-----------------|----------------|
| Ventilation fans (4") | Replace with 6" units — same baffle design, same penetration locations |
| 12V fuse block ($50 item in water system BOM) | Superseded by Blue Sea 5026 — consolidates all circuits in one panel |
| Battery-powered safelight | Wired to circuit D — no separate battery required |
| Water pump power | Now circuit C on main fuse block — remove standalone 12V supply listed in water report |
| Container doors | Unchanged — vestibule attaches externally |
