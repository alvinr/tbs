<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# TBS-001 — Master Shopping List (BoM)

**Basis:** April 2026, with catalog SKUs re-checked against supplier listings July 2026 (branded/identifiable items updated with citations; quote/fabrication/commodity items remain indicative pending real quotes). All prices USD.

Items are grouped by build area. Source documents are cross-referenced in each section header.

## Summary — Estimated Total
<!-- BEGIN costing:master-summary -->
| Area | Low | High |
|------|-----|------|
| 1. Container & delivery | $2,300 | $4,300 |
| 2. Interior conversion (light-seal, paint, ventilation) | $467 | $698 |
| 3. Pinhole optics plate | $110 | $265 |
| 4. Film plane mechanism (4-corner U-channel + acetal skate + 316 cross-slide + U-joint, incl. wall-seat saddles) | $6,684 | $7,250 |
| 5. Print washing — water system (incl. IBC stacking frame) | $5,424 | $7,949 |
| 6. Electrical — power, circuits, wiring | $2,665 | $3,081 |
| 7. Housed revolving-door light lock (plastic-skin custom fabrication) | $1,437 | $2,101 |
| 7a. Panel swing pivot + fixed door frame (Ø89 post + bearings + cage + wall stays + rail saddles + door frame) | $1,180 | $1,610 |
| 7b. Perimeter walkway (4 sections + drum-exit punch-out) | $2,062 | $2,943 |
| 7c. Hinged panel structure (stepped frame + PP skins + Al core + EPDM + cam latches + B2 bay + pull handle) | $1,130 | $1,676 |
| 7d. Chemistry prep shelf (fold-down board + steel frame + hinge/stays + TAP-01 trunk extension) | $214 | $239 |
| 8. Cooling & ventilation | $757 | $907 |
| 9. Printmaking chemistry — cyanotype, 50 prints (Low = Lean, High = Rich tier) | $1,100 | $2,650 |
| 10. Printmaking tools & consumables | $350 | $500 |
| 11. Safety & PPE | $120 | $180 |
| **TOTAL (base build + 50-print run)** | **~$26,000** | **~$36,349** |
<!-- END costing:master-summary -->

*Optional additions: electric film plane actuation (+$827), lens plate (+$400–$1,500), self-haul transport (+$30,000–$40,000).*

*Line 9 (printmaking chemistry) is the **Mike Ware AmFe** recipe with the corrected ~$300 substrate, re-summed into the TOTAL: **Low = Lean ⅓-Ware (~$1,120), High = Rich full-Ware (~$2,700)**, working default Standard ½-Ware (~$1,520). The tier is pinned by the [Sensitizer Trials](sensitizer-trials.md); the TOTAL spans the Lean–Rich range, so it shifts within ±~$1,330 of the §9 line once a tier is locked.*

---

## Procurement BOM — by material type & supplier

*This is the consolidated **Bill of Materials** for the whole build: every purchasable item grouped
by **material type**, with quantities summed across all systems, followed by a **supplier
consolidation** table so you can place the fewest, largest orders. The *Systems* column shows where
each item is used; the full engineering detail for any item lives in that system's report. Costs are
indicative low–high estimates — get quotes before ordering.

<!-- BEGIN parts:master -->
## Procurement BOM — by material type

### adhesives-finishes

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 2" black Gorilla Tape | 6 roll | Home Depot | film | $54–$78 |
| Dielectric grease, marine-grade (terminal protection) | 1 ea | Amazon | electrical | $10 |
| Flat black epoxy spray paint | 1 can | Hardware store | shelf | $12 |
| Flat black paint (RAL 9005) | 1 qt | Local fab | panel | $10–$20 |
| Interior matte-black paint | 1 lot | Home Depot | interior | $100–$160 |
| Loctite PL Premium construction adhesive | 2 tube | Home Depot | tray | $15 |
| Matte-black interior finish | 1 ea | Local fab | lightlock | $40–$70 |
| Primer + paint | 1 lot | Hardware store | ibc-frame | $30–$50 |
| Silicone bead sealant (black, UV-stable) | 1 ea | Home Depot | lightlock | $6–$10 |
| Thread seal tape (PTFE) | 4 roll | Home Depot | water | $8 |
| **adhesives-finishes subtotal** | | | | **$285–$433** |

### aluminum

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 3mm aluminum plate (1220 × 2,440mm) | 2 ea | Online Metals | panel | $360–$460 |
| 6061-T6 AL plate 3/16" (5mm) | 1 ea | Online Metals | spray | $16–$28 |
| 6061-T6 AL round tube 25mm OD × 2mm wall, 500mm | 1 ea | Online Metals | spray | $6 |
| [Aluminum angle 2"×2"×3/16" (6061-T6, anodized)](https://www.mcmaster.com/8982K509-8982K479/) | 10 ea | Metal Supermarkets | film | $1,163 |
| [Aluminum face plate 340×240×3mm (flush power panel)](https://www.onlinemetals.com) | 1 ea | Online Metals | electrical | $18 |
| Aluminum U-channel (per meter) | 40 m | Online Metals | panel | $120–$200 |
| Arm-to-stud adapter, turned 6061-T6 AL (anodized) | 1 ea | Local machine shop | spray | $12–$18 |
| Disc retaining ring (Al 6061-T6, M52×0.75) | 1 ea | Local fab | optics | $15–$25 |
| Telescoping aluminum pool pole, 4–8 ft | 1 ea | Amazon | spray | $15 |
| **aluminum subtotal** | | | | **$1,725–$1,933** |

### bearings-motion

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [1-1/4" OD acetal load rollers — Delrin rod (cut ×8)](https://www.mcmaster.com/8576K23-8576K232/) (8576K23) | 1 1 ft rod | McMaster-Carr | film | $11 |
| [3/4" OD acetal keeper rollers — Delrin rod (cut ×8)](https://www.mcmaster.com/8497K276-8497K273/) (8497K276) | 1 4 ft rod | McMaster-Carr | film | $15 |
| [Acetal roller wheels ×4 (Delrin rod stock, Ø32×20, Ø10 bore)](https://www.mcmaster.com/8576K23/) (8576K23) | 1 1 ft rod | McMaster-Carr | spray | $11 |
| [iglide J flange bushing, Ø90 bore (JFM-9095-100)](https://www.igus.com/iglide-ibh/flange-bearings/product-details/iglide-j-m?artnr=JFM-9095-100) (JFM-9095-100) | 2 ea | igus | swing | $261 |
| [McMaster 4040N12 304 shaft support](https://www.mcmaster.com/4040N12/) (4040N12) | 4 ea | McMaster-Carr | film | $232 |
| [Ruland USKC12-6-6-SS U-joint (keyway+clamp, 303 SS)](https://www.ruland.com/us12-6-6-ss.html) (USKC12-6-6-SS) | 4 ea | Ruland | film | $1,104 |
| [SKF 6215-2RS1 sealed bearing](https://bearingsdirect.com/6215-2rs-ball-bearing-75x130x25-sealed-6215-2nse/) (6215-2RS) | 2 ea | Bearings Direct | lightlock | $121 |
| [Thrust ball bearing, 51118 (Ø90 bore, single-direction)](https://bearingsdirect.com/51118-thrust-ball-bearing-90x120x22-grooved-ubc-usbc/) (51118) | 1 ea | Bearings Direct | swing | $80 |
| Ø20mm ball joint, zinc socket, M12 stud | 1 ea | Amazon | spray | $12 |
| **bearings-motion subtotal** | | | | **$1,847** |

### chemistry-reagents

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Ammonium dichromate | 1 run | Photographers' Formulary | chemistry | $25 |
| [Ammonium iron(III) oxalate (AmFe)](https://stores.photoformulary.com/ammonium-ferric-oxalate/) | 17.1 kg | Photographers' Formulary | chemistry | $1,026 |
| [Potassium ferricyanide](https://www.bostick-sullivan.com/product/potassium-ferricyanide-250gm/) | 5.7 kg | Bostick & Sullivan | chemistry | $138 |
| **chemistry-reagents subtotal** | | | | **$1,189** |

### container

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 20 ft ISO container — CW (cargo-worthy) grade | 1 ea | containermgt.com | container | $2,000–$3,500 |
| **container subtotal** | | | | **$2,000–$3,500** |

### ducting-ventilation

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 150×150×50mm axial fans | 2 ea | Amazon | ventilation | $50 |
| 200mm 90° duct elbow | 1 ea | Home Depot | ventilation | $14 |
| 200mm insulated flex duct | 1 ea | Home Depot | ventilation | $22 |
| Duct collar + hose clamp | 1 ea | Home Depot | ventilation | $12 |
| [Evaporative cooler](https://hessaire.com/mobile-cooling/1300-cfm-mobile-cooler) | 1 ea | Hessaire | ventilation | $185–$230 |
| Ventilation (inline fans + light-trap baffles) — interior-conversion allowance | 1 lot | Amazon | interior | $80–$130 |
| Weatherproof duct cap | 1 ea | Home Depot | ventilation | $8 |
| **ducting-ventilation subtotal** | | | | **$371–$466** |

### electrical-distribution

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [10mm split corrugated wire loom, drop runs](https://www.amazon.com/Split-Wire-Loom-Tubing-Polyethylene/dp/B017L3GWIW) (B017L3GWIW) | 10 m | Amazon | electrical | $25 |
| 12V LED flat panel 300×600mm, 20W 4000K | 3 ea | Amazon | electrical | $75 |
| 14 AWG duplex marine wire | 1 roll | Amazon | water | $22 |
| 15A blade fuse | 1 ea | Amazon | water | $5 |
| 16 AWG silicone coiled cable | 1 ea | Waytek Wire | ventilation | $15 |
| 2/0 AWG battery cable, 3ft (battery–fuse–busbar) | 1 lot | Amazon | electrical | $30 |
| 200A main fuse — MRBF terminal-mount (ABYC E-11) | 1 ea | Amazon | electrical | $23–$27 |
| 4 AWG ground wire, green/yellow, 3m | 1 lot | Amazon | electrical | $15 |
| [40×25mm PVC cable trunking, 5m](https://www.amazon.com/GenSDH-Raceway-Speaker-Concealer-Coffee-Width/dp/B0DK6GMHGL) (B0DK6GMHGL) | 4 ea | Amazon | electrical | $74 |
| [Anderson Powerpole 30A connectors, 50 pairs](https://powerwerx.com) | 1 kit | Powerwerx | electrical | $40 |
| Anderson Powerpole connectors 30A | 5 pair | Amazon | water | $10 |
| Battery main disconnect — Blue Sea m-Series 300A isolator | 1 ea | West Marine | electrical | $33–$42 |
| Battery terminal covers (pair), insulating boots | 1 pair | Amazon | electrical | $10 |
| Blue Sea 5026 fuse block, 12-circuit ST-blade | 1 ea | Amazon | electrical | $55–$77 |
| Brady M210 wire label kit | 1 ea | Cable Master | electrical | $199–$211 |
| [Cable grommets / glands — steel-shell penetrations](https://www.amazon.com/YUFANNET-Assortment-Grommets-Automotive-Electrical/dp/B09K5GNFHF) (B09K5GNFHF) | 1 lot | Amazon | electrical | $28 |
| Cooler external power cable | 1 ea | Waytek Wire | ventilation | $20 |
| Copper ground stake, 8ft × ⅝" dia | 1 ea | Home Depot | electrical | $25–$30 |
| Deutsch DT 2-pin connectors | 2 set | Waytek Wire | ventilation | $8 |
| Deutsch DT 2-pin connectors, IP67 (exterior penetrations) | 10 set | Waytek Wire | electrical | $30 |
| Equipotential bonding kit — 6 AWG + ring lugs | 1 ea | Amazon | electrical | $20 |
| External emergency cut-off — red mushroom IP66 + control loop | 1 ea | AutomationDirect | electrical | $18–$30 |
| Interior emergency cut-off — red mushroom IP65 (paralleled to exterior) | 1 ea | AutomationDirect | electrical | $18–$25 |
| IP65 enclosure ~200×220×140mm (fuse block + busbars, on the plywood) | 1 ea | Polycase | electrical | $60 |
| Master pump switch (Circuit C) — IP67 sealed rocker/disconnect 12V 16A | 1 ea | Amazon | electrical | $10 |
| MC4 bulkhead connector pairs, IP67 panel-mount | 3 pair | Amazon | electrical | $25 |
| MPPT charge-line fuse — 60A ANL/MIDI + holder | 1 ea | Blue Sea | electrical | $15 |
| NEMA 5-15R weatherproof inlet (flush power panel) | 1 ea | Amazon | electrical | $25 |
| Pull-cord ceiling switch, 12V 6A SPST | 2 ea | Amazon | electrical | $16 |
| Pump distribution block — 12V DC + / − bus, 6-way | 1 ea | Blue Sea | electrical | $15 |
| PV cable 10 AWG + MC4 connectors | 1 lot | Amazon | electrical | $30 |
| Remote battery switch — Blue Sea ML-RBS 500A magnetic-latch (E-stop trip) | 1 ea | West Marine | electrical | $280–$396 |
| Sealed wet-zone connectors — Deutsch DT / adhesive heat-shrink | 1 lot | Waytek Wire | electrical | $25 |
| Shore-charger output fuse — 20A inline | 1 ea | Amazon | electrical | $5 |
| Tinned marine wire 14/16 AWG, ~25ft (wet-zone runs) | 1 lot | Waytek Wire | electrical | $30 |
| Wiring kit — 12/14/16/18 AWG tinned, 50ft/color | 1 kit | Waytek Wire | electrical | $80 |
| **electrical-distribution subtotal** | | | | **$1,413–$1,601** |

### electrical-power

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Cooler inverter | 1 ea | Victron | ventilation | $153–$275 |
| [LiFePO4 battery, 100Ah 12V (Renogy Smart Lithium)](https://www.renogy.com/12v-100ah-smart-lithium-iron-phosphate-battery/) | 1 ea | Renogy | electrical | $350–$430 |
| [PV array disconnect — DC load-break isolator, 50A/150VDC (NEC 690.13)](https://www.automationdirect.com/) | 1 ea | AutomationDirect | electrical | $40 |
| [Solar panel ground-mount tilt frame, 30°](https://www.renogy.com) | 1 ea | Renogy | electrical | $33–$50 |
| [Solar panel, 200W monocrystalline 12V](https://www.renogy.com/200-watt-12-volt-monocrystalline-solar-panel/) | 3 ea | Renogy | electrical | $450–$495 |
| [Victron Blue Smart IP65 12/15 shore backup charger](https://www.altestore.com) | 1 ea | altE Store | electrical | $160–$180 |
| [Victron SmartSolar MPPT 100/50 charge controller](https://www.altestore.com) | 1 ea | altE Store | electrical | $185–$230 |
| **electrical-power subtotal** | | | | **$1,371–$1,700** |

### fabric-textile

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Rosco Duvetyne | 1 ea | B&H Photo | film | $95 |
| Shade canopy — 80% shade cloth | 1 ea | Amazon | ventilation | $80 |
| **fabric-textile subtotal** | | | | **$175** |

### fabrication-labor

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Delivery — short haul (<50 miles), tilt-bed | 1 job | Commercial tilt-bed hire | container | $300–$800 |
| Fabrication (cut, brake, weld, press sump) | 1 lot | Local sheet metal | tray | $450–$850 |
| Plastic fabrication (roll 2 cylinders, hot-air / extrusion weld, fit, bearings) | 1 lot | Local plastic fab | lightlock | $800–$1,150 |
| Welding / fabrication | 1 lot | Local fab | door | $200–$350 |
| Welding / fabrication (frame assembly) | 1 lot | Local fab | ibc-frame | $688–$1,018 |
| **fabrication-labor subtotal** | | | | **$2,438–$4,168** |

### fasteners-hardware

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [M5×16 countersunk screw, A2-70 SS](https://www.mcmaster.com/91420A326/) (91420A326) | 8 ea | McMaster-Carr | shelf | $1 |
| [M6×1.0 × 16 hex bolt, 316 SS — tray center-seam lap joint](https://www.mcmaster.com/93635A210/) (93635A210) | 12 ea | McMaster-Carr | tray | $8 |
| [M6×1.0 × 20 hex bolt, Grade 8.8 zinc](https://www.mcmaster.com/91280A330/) (91280A330) | 20 ea | McMaster-Carr | electrical, spray | $4 |
| [M8×1.25 × 25 hex bolt, Grade 8.8 zinc — right-rail end fixing (ICP-14)](https://www.mcmaster.com/91280A534/) (91280A534) | 8 ea | McMaster-Carr | film | $3 |
| [M8×1.25 × 25 hex bolt, Grade 8.8 zinc — shelf cleat + stay mount](https://www.mcmaster.com/91280A534/) (91280A534) | 12 ea | McMaster-Carr | shelf | $4 |
| [M12×40 hex bolt, Grade 8.8](https://www.fmwfasteners.com/products/m12-1-75-x-40-hex-cap-screw-8-8-din-933-zinc-plated-fully-threaded) (1634027) | 12 ea | FMW Fasteners | ibc-frame | $9–$17 |
| [M12×65 hex through-bolt, Grade 8.8 zinc, partial-thread](https://www.mcmaster.com/91280A728/) (91280A728) | 86 ea | McMaster-Carr | film, walkway | $137 |
| [M12×70 hex through-bolt, Grade 8.8 zinc, partial-thread](https://www.mcmaster.com/91280A732/) (91280A732) | 24 ea | McMaster-Carr | walkway | $42 |
| [M6 flat washer, SS](https://www.mcmaster.com/91455a120/) (91455A120) | 8 ea | McMaster-Carr | electrical | $0 |
| [M8 flat washer, SS](https://www.mcmaster.com/91166A270/) (91166A270) | 12 ea | McMaster-Carr | shelf | $0 |
| [M12 flat washer, zinc](https://www.mcmaster.com/91166a290/) (91166A290) | 440 ea | McMaster-Carr | film, walkway | $43 |
| [M12 split lock washer, zinc](https://www.mcmaster.com/91202A246/) (91202A246) | 110 ea | McMaster-Carr | film, walkway | $13 |
| [M6×1.0 flange nut, serrated SS](https://www.mcmaster.com/96194A101/) (96194A101) | 12 ea | McMaster-Carr | tray | $1 |
| [M6×1.0 hex nut, nyloc SS](https://www.mcmaster.com/90576A115/) (90576A115) | 16 ea | McMaster-Carr | spray | $1 |
| [M6×1.0 hex nut, plain SS](https://www.mcmaster.com/90591A151/) (90591A151) | 4 ea | McMaster-Carr | electrical | $0 |
| [M8×1.25 hex nut, plain SS](https://www.mcmaster.com/90591A161/) (90591A161) | 20 ea | McMaster-Carr | film, shelf | $2 |
| [M12 hex nut, plain](https://www.mcmaster.com/90591A181/) (90591A181) | 110 ea | McMaster-Carr | film, walkway | $28 |
| M8×25mm knurled thumbscrew DIN 464 | 12 ea | Amazon | film | $36 |
| Corridor panel mount hardware (brackets + fasteners) | 1 lot | Home Depot | water | $25–$50 |
| Door & access upgrades | 1 lot | Home Depot | interior | $50–$100 |
| SS lag/wood screws — filter housings to ply backing | 6 ea | Home Depot | water | $3–$9 |
| Cam-lever rail brake (skate lock) | 12 ea | McMaster-Carr | film | $96–$180 |
| [10mm × 60mm 304 SS axle pins (4-pack) — skate axles](https://www.amazon.com/uxcell-Single-Hole-Clevis-Pins/dp/B0816MQ5T6) (B0816MQ5T6) | 4 pack | Amazon | film | $20 |
| [Weld-on lashing ring, 1½" ID](https://www.mcmaster.com/3028t31/) (3028T31) | 8 ea | McMaster-Carr | ibc-frame | $40 |
| [Self-drilling structural screw, #14×3¼″ winged, 410 SS](https://www.fastenersplus.com/products/14-x-3-1-4-self-drilling-flat-head-screw-with-wings-410-stainless-steel-pkg-100) (F14C325FDC) | 16 ea | Fasteners Plus | ibc-frame | $16 |
| 25mm ratchet strap, 1,100 kg WLL | 4 ea | Amazon | ibc-frame | $30–$50 |
| [Stainless fasteners + nylon isolation washers](https://www.usplastic.com/catalog/item.aspx?itemid=155501) (92674) | 1 lot | US Plastic + Amazon | lightlock | $45–$60 |
| [100mm Ø SS grab rail](https://www.marinefiberglassdirect.com/products/16-stainless-steel-safety-grab-bar-bolt-on-for-marine-dock-deck-boat-pool-hot-tub) | 1 ea | Marine Fiberglass Direct | lightlock | $25–$45 |
| Misc. conversion hardware | 1 lot | Home Depot | interior | $80–$130 |
| [Nylon spring clamp, 3½″ (Pittsburgh 69289)](https://www.harborfreight.com/3-12-in-nylon-spring-clamp-69289.html) (69289) | 58 ea | Harbor Freight | clamp | $174–$232 |
| [304 SS D-grab pull handle (~300mm) + 2× M8 SS bolts + backing plate, matte-black](https://www.strongarhardware.com/pro-line-series-ladder-pull-handle-back-to-back-matte-black-powder-coated-finish-316-exterior-grade-stainless-steel-alloy/) | 1 ea | StrongAr Hardware | panel | $70–$90 |
| Southco C2-33 cam compression latch | 4 ea | Southco | panel | $76–$104 |
| Ratchet straps, 25mm | 2 ea | Home Depot | ventilation | $12 |
| Cushioned pipe clip | 16 ea | Amazon | water | $16–$32 |
| Folding shelf stays/brackets | 2 ea | Amazon | shelf | $24 |
| [Continuous (piano) hinge, 600 mm](https://wurthlac.com/product/165974/) (LSN8-32-600) | 1 ea | Wurth LAC | shelf | $23–$36 |
| Transport latch (over-center/barrel) | 1 ea | Amazon | shelf | $8 |
| Shurflo pump mounting bracket | 5 ea | Amazon | water | $50 |
| [Top + bottom wall stays + 4-bolt anchor plates](https://www.fastenersplus.com/products/5-8-x-6-jaw-eye-galvanized-turnbuckle) (JETBGV58X6) | 2 set | Fasteners Plus | swing | $90–$120 |
| [Clamp-style shaft collar, 25mm/1" bore, SS](https://www.ruland.com/cl-16-st.html) (CL-16-ST) | 1 ea | Ruland | spray | $28–$33 |
| [M12×1.75 jam nut, SS](https://www.amazon.com/M12-1-75-Plain-Finish-Stainless-Steel/dp/B007IA07PS) (B007IA07PS) | 1 ea | Amazon | spray | $1 |
| [10mm × 60mm 304 SS axle pin (4-pack)](https://www.amazon.com/uxcell-Single-Hole-Clevis-Pins/dp/B0816MQ5T6) | 1 pack | Amazon | spray | $5 |
| [SS beam clamp plates (top + bottom) + spacers (25mm)](https://www.bobcometal.com/stainless-steel-flat-bar-304-1-4-inch-x-2-inch.html) (SS04FB.250X2.00) | 4 ea | Bobco Metals | spray | $40–$60 |
| SS/nylon retainer clips for 3/4" LDPE | 2 ea | Amazon | spray | $4 |
| [Axle saddle clamps ×8 (304 SS flat-bar stock)](https://www.mcmaster.com/8992K794/) (8992K794) | 1 2 ft bar | McMaster-Carr | spray | $10 |
| [Self-tapping SS screws (8-pack)](https://www.lowes.com/pd/Hillman-25-Count-10-x-1-in-Stainless-Steel-Self-Drilling-Interior-Exterior-Sheet-Metal-Screws/3691866) (3691866) | 4 ea | Lowe's (Hillman) | spray | $2–$3 |
| Nylon zip ties, 200mm | 6 ea | Amazon | spray | $1 |
| [Self-drilling structural screw, #14×2″ HWH, 410 SS](https://www.bridgefasteners.com/products/14-x-2-hex-washer-head-self-drilling-screws-410-stainless-steel-self-tapping-full-thread) | 20 ea | Bridge Fasteners | walkway | $7–$11 |
| Grating clips | 30 ea | McNichols | walkway | $30–$50 |
| **fasteners-hardware subtotal** | | | | **$1,431–$1,924** |

### plastics-sheet

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 4mm black polypropylene sheet | 1 lot | TAP Plastics | lightlock | $150–$240 |
| 4mm black PP plastic sheet (1220 × 2,440mm) | 4 sheet | TAP Plastics | panel | $260–$420 |
| 4mm black PP sheet + EPDM lip | 1 lot | TAP Plastics | panel | $60–$120 |
| 5mm UV-stabilized HDPE sheet (black) | 1 lot | TAP Plastics | lightlock | $180–$280 |
| [Dibond ACM panel 4mm (black), 4×8 sheet](https://www.curbellplastics.com/product-category/material/aluminum-composite-material-acm/dibond-panels/) | 4 sheet | Curbell Plastics | film | $380 |
| Drum-exit punch-out grating | 1 lot | McNichols | walkway | $50–$65 |
| HDPE filler strip (L-channel packer) | 1 lot | TAP Plastics | clamp | $30–$70 |
| HDPE flat bar, 50mm wide | 5 ea | Online Metals | tray | $40–$75 |
| Molded GRP (fiberglass) grating | 1 lot | McNichols | walkway | $965–$1,250 |
| **plastics-sheet subtotal** | | | | **$2,115–$2,900** |

### plumbing-fittings

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 1" bulkhead tank-body fittings (Blue equalization cross-tie) | 2 ea | Amazon | water | $12–$24 |
| 1" HDPE inter-housing jumpers | 1 lot | Ferguson | water | $18–$32 |
| 1" NPT 4-way cross fitting | 1 ea | Amazon | water | $8–$14 |
| 1" NPT spring check valve (CV1 — X1 gravity fill) | 1 ea | Amazon | water | $8–$14 |
| 1" reinforced suction hose, 6 ft | 1 ea | Amazon | tray | $15 |
| 1" SDR-11 HDPE pipe | 1 stick | Ferguson | water | $12–$18 |
| 1" SS foot valve with strainer screen | 1 ea | Amazon | tray | $20 |
| 1/2" barb × 1/2" hose barb, brass | 1 ea | Amazon | spray | $4 |
| 1/2" ID reinforced braided PVC hose | 2 length | Amazon | water | $24–$48 |
| 1/2" NPT 90° elbow polypropylene | 14 ea | Amazon | water | $28–$56 |
| 1/2" NPT polypropylene tee | 6 ea | Amazon | water | $12–$24 |
| 1/2" NPT polypropylene union | 6 ea | Amazon | water | $24–$36 |
| 1/2" reinforced braided PVC hose, 15 ft | 1 ea | Amazon | spray | $15 |
| [1/2" SDR-11 HDPE pipe](https://www.ferguson.com) | 4 stick | Ferguson | water | $24–$40 |
| 1/2"×1" NPT bushing reducer | 1 ea | Amazon | water | $3–$5 |
| 1/4" irrigation poly tube | 1 ea | Amazon | spray | $6 |
| 2" polypropylene camlock pairs (M+F) | 4 pair | Amazon | water | $20–$32 |
| 3-way diverter valve 1" FNPT | 1 ea | Amazon | water | $18–$30 |
| 3-way diverter valve 1/2" FNPT | 1 ea | Amazon | water | $12–$22 |
| 3/4" LDPE irrigation poly pipe, 15 ft | 1 ea | Amazon | spray | $10 |
| 3/4" SDR-11 HDPE pipe | 2 stick | Ferguson | water | $20–$30 |
| Banjo EL100-90 elbow 1" NPT | 4 ea | Barn Door Ag | water | $16–$24 |
| Banjo TEE100 equal tee 1" NPT | 3 ea | Barn Door Ag | water | $15–$21 |
| Banjo TEE100 equal tee, 1" HDPE NPT | 1 ea | Barn Door Ag | water | $5–$7 |
| Banjo V050FP ball valve 1/2" FNPT | 3 ea | Barn Door Ag | water | $90–$135 |
| Banjo V050FP ball valve 1/2" FNPT | 1 ea | Barn Door Ag | water | $30–$45 |
| Banjo V050FP ball valve 1/2" FNPT | 2 ea | Barn Door Ag | water | $60–$90 |
| Banjo V100FP ball valve 1" FNPT | 6 ea | Barn Door Ag | water | $198–$330 |
| Barbed tees, tube into the side poly manifold | 7 ea | Amazon | spray | $10 |
| [Bulkhead fitting 2" NPT (304 SS)](https://www.mcmaster.com/4464K115) (4464K115) | 3 ea | McMaster-Carr | water | $410 |
| Distribution manifold, 1/2" → 7 barb outlets | 1 ea | Amazon | spray | $12 |
| Flat-fan irrigation spray nozzles, barbed | 26 ea | Amazon | spray | $30–$50 |
| pH sample tap (SV-01) — 1/2" PP ball valve + barb spout + branch tee | 1 ea | Amazon | water | $10–$18 |
| pH sample tap (SV-02) — 1/2" PP ball valve + barb spout + branch tee | 1 ea | Amazon | water | $10–$18 |
| [S60×6 female-buttress → 2" NPT + 2→1" bushing](https://us.cpp.parts/collections/fits-s60x6) (HMFN/20UD/027) | 8 ea | CPP.parts | water | $112–$144 |
| ½" HDPE pipe (tap relocation) | 1 lot | Irrigation supply | shelf | $10 |
| **plumbing-fittings subtotal** | | | | **$1,331–$1,819** |

### seals-gaskets

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [20mm EPDM gasket (per meter, closed-cell)](https://www.amazon.com/dp/B089GJQ96Z) (B089GJQ96Z) | 21 m | Amazon (OKAYASU) | panel | $24–$52 |
| [Black EPDM foam tape 1"×½"](https://www.mcmaster.com/8694K88/) (8694K88) | 2 roll | McMaster-Carr | film | $45 |
| [Felt/brush wiper strip + 12mm closed-cell neoprene](https://www.doitbest.com/product/146005/) (BP17A) | 1 lot | Frost King + Canal Rubber | lightlock | $40–$75 |
| Light-sealing materials (interior conversion) | 1 lot | Amazon (bundle) | interior | $157–$178 |
| [Neoprene gasket 340×240×3mm (panel weatherseal)](https://presbond.com/products/2c1-closed-cell-neoprene-foam-sheet-12-x-12-acrylic-adhesive) (NE4112-12X12-XFV) | 1 ea | Pres-Bond | electrical | $21–$42 |
| [Ruland UBOOT12/19-NI-KIT nitrile boot](https://www.ruland.com/uboot12-19-ni-kit.html) (UBOOT12/19-NI-KIT) | 4 ea | Ruland | film | $122 |
| [Silicone gasket strip](https://www.countrymax.com/aqueon-silicone-clear-aquarium-sealant-10oz-bottle/) (015952) | 1 ea | CountryMax (Aqueon) | tray | $17–$25 |
| [Tight-seal nylon strip brush + aluminum holder (~4.7 m, top + bottom)](https://www.mcmaster.com/74405T12-74405T126/) (74405T12) | 1 lot | McMaster-Carr | door | $129 |
| **seals-gaskets subtotal** | | | | **$555–$668** |

### stainless-sheet

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 304 SS sheet, 16-gauge (1.5mm), #4 brushed | 2 ea | Online Metals | tray | $720–$1,000 |
| Custom laser-drilled pinhole — SS-302/304 shim, 3×3 | 1 ea | Lenox Laser | optics | $50–$150 |
| **stainless-sheet subtotal** | | | | **$770–$1,150** |

### steel-structural

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 12mm steel plate, 150 × 150 cut | 4 ea | Metal Supermarkets | ibc-frame | $20–$40 |
| 25×25×3 mm steel SHS | 1 lot | Online Metals | shelf | $30 |
| [3/8" 304/304L SS rod — U-joint stub shafts (1× 3 ft)](https://www.mcmaster.com/89535K87/) (89535K87) | 1 lot | McMaster-Carr | film | $13 |
| 304 SS RHS 40×25×3mm, 8 ft * | 2 ea | Online Metals | spray | $96–$144 |
| [304 U-channel depth rail 3×1½" (76×38mm)](https://www.mcmaster.com/1262T41-1262T21/) (1262T41) | 6 ea | McMaster-Carr | film | $2,173 |
| 316 flat-bar Z (tilt) + X (swing) cross-slides + UHMW pad + gib | 4 set | Metal Supermarkets | film | $180–$380 |
| 4mm folded plate | 4 ea | Local fab | ibc-frame | $30–$50 |
| 50 × 50 × 3mm RHS mild steel (6 m lengths) | 4 ea | Metal Supermarkets | ibc-frame | $120–$180 |
| 50 × 50 × 3mm RHS mild steel (6 m lengths) | 3 ea | Metal Supermarkets | door | $90–$120 |
| 50 × 50 × 3mm RHS mild steel (6 m lengths) | 4 ea | Metal Supermarkets | panel | $120–$160 |
| 75mm Ø × 150mm steel stub shaft | 2 ea | Steel service center | lightlock | $30–$50 |
| Baffle duct sheet metal (cooler) | 1 lot | Local sheet metal | ventilation | $20 |
| Baffle duct sheet metal (fans) | 1 lot | Local sheet metal | ventilation | $30 |
| Canopy frame | 1 lot | Home Depot | ventilation | $120 |
| Cantilever bracket — standard (near/far) | 14 ea | Local fab | walkway | $420–$700 |
| Cantilever bracket — widened (near) | 4 ea | Local fab | walkway | $160–$280 |
| Combined corner plate (right corners) | 2 ea | Local fab | walkway | $50–$80 |
| Corner gusset plate, 3 mm | 4 ea | Steel offcut | shelf | $5 |
| Corner plate 304 SS (U-joint mount) | 4 ea | Metal Supermarkets | film | $152–$208 |
| Drop-in rail saddles + tapered dowels | 4 ea | Local fab | swing | $80–$130 |
| Drum support cage, 40 × 40 × 3mm SHS | 1 lot | Local fab | swing | $70–$120 |
| Floor-leg cantilever bracket (left walkway, ×5) | 5 ea | Local fab | walkway | $55–$95 |
| Mild steel plate 8mm (laser/plasma cut + welded) | 6 ea | Metal Supermarkets | film | $318 |
| Power-panel raised mounting frame, 8mm steel (welded) | 1 ea | Local fab | electrical | $15–$25 |
| Reinforcing plate (exterior) | 18 ea | Local fab | walkway | $75–$130 |
| Right walkway cantilever frame | 1 lot | Metal Supermarkets | walkway | $28–$40 |
| Shelf mount backing plates, 8mm steel (welded, ×3) | 3 ea | Local fab | shelf | $18–$30 |
| Shutter plate (⅛ steel 10×8) + slide channel | 1 ea | Local fab | optics | $25–$50 |
| Skate carriage plate (×4) — fab | 4 ea | Local fab | film | $136–$236 |
| Steel backing plate 6×6×⅛ + welded frame | 1 ea | Metal Supermarkets | optics | $20–$40 |
| Steel flat bar 25×3mm — ribbon support cross-brace | 4 ea | Home Depot | water | $8–$16 |
| Transition bearing plate | 2 ea | Local fab | walkway | $5–$10 |
| Wall cleat (left corners) | 2 ea | Local fab | walkway | $20–$35 |
| Wall mounting cleat + anchors | 1 lot | Local fab | shelf | $18 |
| Ø89×8mm CHS pivot post + machined hub / thrust collar | 1 ea | Metal Supermarkets | swing | $180–$300 |
| **steel-structural subtotal** | | | | **$4,930–$6,376** |

### substrate-fabric

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [Unbleached muslin, 60" wide](https://www.fabricdirect.com/shop/craft-fabric/broadcloth-and-muslin-fabric/essence-60-medium-weight-muslin-fabric-unbleached-150-yard-roll/) | 3 roll | Fabric Direct | chemistry | $300 |
| **substrate-fabric subtotal** | | | | **$300** |

### timber-ply

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Corridor plumbing-panel marine ply (18mm) | 1 sheet | marine plywood supplier | water | $120–$200 |
| EP plywood backing panel (18mm, ~700×2000mm) | 1 sheet | Home Depot | electrical | $60 |
| Exterior-grade plywood (Fan B mount band) | 1 2'×4' ¾" panel | Home Depot | panel | $30–$50 |
| Phenolic-faced plywood (work surface) | 1 4'×8' ¾" sheet | Home Depot | shelf | $60 |
| Plywood base plate (cooler stowage) | 1 2'×4' ½" panel | Home Depot | ventilation | $8 |
| Pump-mount shirt marine ply (25mm) | 1 piece | marine plywood supplier | water | $70–$130 |
| **timber-ply subtotal** | | | | **$348–$508** |

### tools-safety

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 6-mil black LDPE sheet, 10 ft × 8 ft | 1 ea | Home Depot | tray | $8 |
| 6-mil black LDPE sheeting | 1 roll | Home Depot | water | $66–$70 |
| 6-mil black poly sheeting | 1 roll | Home Depot | film | $66–$70 |
| [Apera Instruments AI311 PH60 pH meter](https://www.amazon.com/Apera-Instruments-AI311-Replaceable-2-00-16-00/dp/B01ENFOIQE) | 1 ea | Apera Instruments | water | $100–$110 |
| Chemical-resistant labels (GHS) | 1 pack | Amazon | water | $20 |
| Citric acid, food grade, 5 lb | 2 bag | Amazon | water | $28 |
| Nitrile gloves, box of 100 | 2 box | Amazon | water | $18–$40 |
| pH calibration solution set | 1 set | Amazon | water | $10 |
| **tools-safety subtotal** | | | | **$316–$356** |

### water-equipment

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Big Blue filter housing 4.5"×20" (separate) | 3 ea | AllFilters | water | $114–$186 |
| CTO carbon block cartridge 4.5"×20" | 2 ea | RonAqua | water | $32–$60 |
| HDPE spacer blocks 25mm (filter skid) | 1 lot | McMaster-Carr | water | $12–$22 |
| [IBC tote (1,000 L caged)](https://containerexchanger.com/geo-sale-ads/us-ca/bulk-containers/ibc-totes-for-sale) | 4 ea | Container Exchanger | water | $320–$600 |
| KDF-55 heavy-metal cartridge 4.5"×20" | 1 ea | FilterWay | water | $65–$95 |
| MPP 5-micron sediment cartridge 4.5"×20" | 2 ea | Amazon | water | $24–$40 |
| [SeaFlo accumulator (0.75 L)](https://www.amazon.com/Seaflo-Accumulator-Control-Internal-Bladder/dp/B01MUYL8F8) (SFAT-075-125-01) | 1 ea | Environmental Marine | water | $30–$41 |
| [Shurflo 2088-554-144 pump (P-01 Blue supply)](https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C) | 1 ea | Fresh Water Systems | water | $80–$89 |
| [Shurflo 2088-554-144 pump (P-02 filter loop)](https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C) | 1 ea | Fresh Water Systems | water | $80–$89 |
| Shurflo 2088-554-144 pump (P-03 waste evacuation) | 1 ea | Fresh Water Systems | water | $80–$89 |
| Shurflo 2088-554-144 pump (P-04 tray drain transfer) | 1 ea | Fresh Water Systems | water | $80–$89 |
| Shurflo 2088-554-144 pump (P-05 Brown drain) | 1 ea | Fresh Water Systems | water | $80–$89 |
| Slotted steel angle frame 25×25×3mm (filter skid) | 1 lot | Home Depot | water | $25–$45 |
| **water-equipment subtotal** | | | | **$1,022–$1,534** |

## Supplier consolidation (largest orders first)

| Supplier | Line items | Types | Est. cost |
|----------|-----------|-------|-----------|
| McMaster-Carr | 38 | bearings-motion, fasteners-hardware, plumbing-fittings, seals-gaskets, steel-structural, water-equipment | $3,482–$3,576 |
| containermgt.com | 1 | container | $2,000–$3,500 |
| Local fab | 20 | adhesives-finishes, aluminum, fabrication-labor, steel-structural | $2,130–$3,472 |
| Metal Supermarkets | 11 | aluminum, steel-structural | $2,391–$2,949 |
| Online Metals | 9 | aluminum, plastics-sheet, stainless-sheet, steel-structural | $1,406–$1,961 |
| Amazon | 63 | adhesives-finishes, aluminum, bearings-motion, ducting-ventilation, electrical-distribution, fabric-textile, fasteners-hardware, plumbing-fittings, tools-safety, water-equipment | $1,355–$1,677 |
| McNichols | 3 | fasteners-hardware, plastics-sheet | $1,045–$1,365 |
| Ruland | 3 | bearings-motion, fasteners-hardware, seals-gaskets | $1,254–$1,259 |
| Home Depot | 25 | adhesives-finishes, ducting-ventilation, electrical-distribution, fasteners-hardware, steel-structural, timber-ply, tools-safety, water-equipment | $885–$1,165 |
| Local plastic fab | 1 | fabrication-labor | $800–$1,150 |
| TAP Plastics | 5 | plastics-sheet | $680–$1,130 |
| Photographers' Formulary | 2 | chemistry-reagents | $1,051 |
| Renogy | 3 | electrical-power | $833–$975 |
| Local sheet metal | 3 | fabrication-labor, steel-structural | $500–$900 |
| Commercial tilt-bed hire | 1 | fabrication-labor | $300–$800 |
| Barn Door Ag | 7 | plumbing-fittings | $414–$652 |
| Container Exchanger | 1 | water-equipment | $320–$600 |
| Fresh Water Systems | 5 | water-equipment | $400–$445 |
| West Marine | 2 | electrical-distribution | $313–$438 |
| altE Store | 2 | electrical-power | $345–$410 |
| Curbell Plastics | 1 | plastics-sheet | $380 |
| marine plywood supplier | 2 | timber-ply | $190–$330 |
| Fabric Direct | 1 | substrate-fabric | $300 |
| Victron | 1 | electrical-power | $153–$275 |
| igus | 1 | bearings-motion | $261 |
| Harbor Freight | 1 | fasteners-hardware | $174–$232 |
| Hessaire | 1 | ducting-ventilation | $185–$230 |
| Cable Master | 1 | electrical-distribution | $199–$211 |
| Waytek Wire | 7 | electrical-distribution | $208 |
| Bearings Direct | 2 | bearings-motion | $201 |
| AllFilters | 1 | water-equipment | $114–$186 |
| Amazon (bundle) | 1 | seals-gaskets | $157–$178 |
| Lenox Laser | 1 | stainless-sheet | $50–$150 |
| CPP.parts | 1 | plumbing-fittings | $112–$144 |
| Bostick & Sullivan | 1 | chemistry-reagents | $138 |
| Fasteners Plus | 2 | fasteners-hardware | $106–$136 |
| Ferguson | 4 | plumbing-fittings | $74–$120 |
| Apera Instruments | 1 | tools-safety | $100–$110 |
| Southco | 1 | fasteners-hardware | $76–$104 |
| FilterWay | 1 | water-equipment | $65–$95 |
| AutomationDirect | 3 | electrical-distribution, electrical-power | $75–$95 |
| B&H Photo | 1 | fabric-textile | $95 |
| StrongAr Hardware | 1 | fasteners-hardware | $70–$90 |
| Frost King + Canal Rubber | 1 | seals-gaskets | $40–$75 |
| Hardware store | 2 | adhesives-finishes | $42–$62 |
| RonAqua | 1 | water-equipment | $32–$60 |
| Bobco Metals | 1 | fasteners-hardware | $40–$60 |
| Polycase | 1 | electrical-distribution | $60 |
| US Plastic + Amazon | 1 | fasteners-hardware | $45–$60 |
| Amazon (OKAYASU) | 1 | seals-gaskets | $24–$52 |
| Steel service center | 1 | steel-structural | $30–$50 |
| Marine Fiberglass Direct | 1 | fasteners-hardware | $25–$45 |
| Pres-Bond | 1 | seals-gaskets | $21–$42 |
| Environmental Marine | 1 | water-equipment | $30–$41 |
| Powerwerx | 1 | electrical-distribution | $40 |
| Wurth LAC | 1 | fasteners-hardware | $23–$36 |
| Blue Sea | 2 | electrical-distribution | $30 |
| CountryMax (Aqueon) | 1 | seals-gaskets | $17–$25 |
| Local machine shop | 1 | aluminum | $12–$18 |
| FMW Fasteners | 1 | fasteners-hardware | $9–$17 |
| Bridge Fasteners | 1 | fasteners-hardware | $7–$11 |
| Irrigation supply | 1 | plumbing-fittings | $10 |
| Steel offcut | 1 | steel-structural | $5 |
| Lowe's (Hillman) | 1 | fasteners-hardware | $2–$3 |
<!-- END parts:master -->

## 9. Printmaking Chemistry — Cyanotype (50 prints)
*Source: `chemistry-shopping-list.md`. **Procurement** — reagent order quantities, per-tier costs,
suppliers, and the muslin substrate — is in the Procurement BOM above (`chemistry-reagents` +
`substrate-fabric`) and the [Cyanotype Shopping List](chemistry-shopping-list.md). This section is the
**recipe + per-print basis** only.*

**Mike Ware New Cyanotype** — 3:1 ammonium iron(III) oxalate (AmFe) : potassium ferricyanide by weight
+ ammonium dichromate for contrast, applied as **two wet-on-wet coats** over the 9.42 m² active plane.

| Reagent | Per print (Standard ½-Ware) | × 50 prints |
|---------|-----------------------------|-------------|
| Ammonium iron(III) oxalate (AmFe) | <!-- BEGIN costing:om-amfe-g-standard -->342<!-- END costing:om-amfe-g-standard -->g | <!-- BEGIN costing:om-amfe-kg-standard -->17.1<!-- END costing:om-amfe-kg-standard --> kg |
| Potassium ferricyanide (3:1) | 130g | 6.5 kg |
| Ammonium dichromate (contrast, 0.1–0.4%) | ~1–4g | ~0.2 kg |
| Distilled water | ~2.6 L | ~130 L |

Standard ½-Ware is the working default; the leanest/richest viable strength — and the final order — is
pinned by the [Sensitizer Trials](sensitizer-trials.md). **Run cost ~$1,520 (Standard), range ~$1,120
(Lean) – ~$2,700 (Rich)** per 50-print run (~$22–54/print), incl. ~$300 muslin substrate — ~399 linear
yards of 60" unbleached cotton (pre-wash twice in hot water, no detergent, to remove sizing). The
summary table maps Low = Lean, High = Rich.

## 10. Printmaking Tools & Consumables
*Source: `operating-manual.md`, `chemistry-shopping-list.md`*

*Printmaking-specific tools only. Items shared with other systems are **not** repeated here — they
roll up in the Procurement BOM above and are itemized in their owning system: the muslin clamps +
mounting in the [film-clamp BOM](film-clamp-mechanism-report.md), nitrile gloves + 6-mil floor poly
in the [water BOM](water-system-report.md), and the Circuit-D red safelight strips in the
[electrical BOM](electrical-report.md).*

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Foam roller 18" wide | For sensitiser application | 3 | Home Depot / art supply | ~$30 |
| Foam brush 4" wide | Detail/edge work | 6 | Home Depot / art supply | ~$15 |
| UV-blocking safety glasses | Mandatory during sensitiser handling | 2 pairs | Amazon / safety supply | ~$20 |
| Chemical-resistant apron | Full-length | 2 | Amazon / safety supply | ~$30 |
| Red LED safelight headlamp | Loading operations inside container (wearable; not the Circuit-D strips) | 2 | Amazon | ~$30 |
| Digital timer | Exposure timing | 1 | Amazon / camera store | ~$15 |
| Folding step stool | Reaching top of image plane | 1 | Home Depot | ~$25 |
| Spray bottle (1 liter) | Humidity/misting in low-RH conditions | 2 | Amazon / garden supply | ~$15 |
| pH test strips | Quick wash water check | 1 pack | Amazon | ~$10 |
**Listed tools total: ~$190.** *(The Section 10 budget in the summary above — $350–$500 — adds consumable-replacement contingency for rollers/brushes/gloves used up each session.)*

## 11. Safety & PPE
*Source: `operating-manual.md`, `electrical-report.md`*

*General / operator safety + electrical-work tools — none of these belong to a system BOM, so nothing
here is repeated above. Related safety items live with their use: chemistry-handling PPE (nitrile
gloves in the [water BOM](water-system-report.md), UV glasses + apron in §10); the **built-in**
electrical-safety hardware (terminal-mount fuse, disconnect, two E-stops, terminal covers, bonding) is
in the electrical BOM and the [Electrical Safety Report](electrical-safety-report.md) §5.*

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| First aid kit | ANSI Class A, for remote deployment | 1 | Amazon / Safety supply | ~$35 |
| Fire extinguisher (ABC) | 5 lb, for electrical and general fire | 1 | Home Depot / Costco | ~$40 |
| GFCI outlet tester | Verify GFCI protection on any shore power | 1 | Home Depot / Amazon | ~$12 |
| Non-contact voltage tester | Before any electrical work | 1 | Fluke / Amazon | ~$25 |
| Sunscreen SPF50+, pump bottle | Exterior deployment, hot climate | 2 | Pharmacy / Costco | ~$20 |
| Insulated drinking water jug (1 gal) | Palm Springs heat — operator hydration | 2 | REI / Amazon | ~$30 |
**Section total: ~$162**

## Supplier Directory

*Contact reference (URL / location) for the suppliers used in the build. The **full** supplier list
with order quantities and $ totals is the **Supplier consolidation** table in the Procurement BOM
above — this directory adds where-to-buy detail and omits alternative/optional-only sources.*

| Supplier | Category | URL / Location |
|---------|---------|----------------|
| **[Photographers' Formulary](https://stores.photoformulary.com)** | Ammonium iron(III) oxalate (AmFe), ammonium dichromate | Condon, MT |
| **[Bostick & Sullivan](https://bostick-sullivan.com)** | Potassium ferricyanide + AmFe (cyanotype reagents) | Santa Fe, NM |
| **[Fabric Direct](https://www.fabricdirect.com)** | Unbleached cotton muslin, 150-yd rolls | Online |
| **[Fabric Wholesale Direct](https://www.fabricwholesaledirect.com)** | Unbleached muslin by yard or bolt | Online |
| **[Metal Supermarkets](https://www.metalsupermarkets.com)** | Steel, aluminum, cut-to-length | Anaheim · Van Nuys · San Diego |
| **[Grimco](https://www.grimco.com)** | Dibond ACM panels (sign industry) | City of Industry CA |
| **Automation Overstock** | Linear guides, carriages, surplus motion components | Gardena CA (walk-in) |
| **[Ruland](https://www.ruland.com)** | USKC12-6-6-SS universal joints + nitrile boots | Ships nationally |
| **[Renogy](https://www.renogy.com)** | Solar panels, LiFePO4 battery, tilt mount | Online |
| **[altE Store](https://www.altestore.com)** | Victron MPPT, Victron chargers, off-grid power | Online |
| **[Powerwerx](https://powerwerx.com)** | Anderson Powerpole connectors and tools | Online |
| **[Waytek Wire](https://www.waytekwire.com)** | Deutsch DT connectors, automotive wire | Online |
| **[West Marine](https://www.westmarine.com)** | Blue Sea fuse blocks, marine DC wiring | Torrance CA |
| **[Container Exchanger](https://containerexchanger.com)** | Used IBC totes, food-grade — CA listings | Online |
| **[Ferguson Plumbing](https://www.ferguson.com)** | HDPE pipe, valves, fittings | Multiple SoCal branches |
| **Pacific Coast Steel** | Hot-rolled A36 sheet, round bar, structural steel | Santa Fe Springs CA |
| **[TAP Plastics](https://www.tapplastics.com)** | UV-HDPE / PP / acrylic sheet + plastic fabrication | Multiple SoCal stores |
| **[Curbell Plastics](https://www.curbellplastics.com)** | PP / engineering plastic sheet | Online / SoCal |
| **[AutomationDirect](https://www.automationdirect.com)** | DC load-break isolators, E-stop push-buttons | Online |
| **[B&H Photo](https://www.bhphotovideo.com)** | Rosco Duvetyne, photographic supplies | Online / NYC |
| **[Amazon](https://www.amazon.com)** | Pumps, filters, valves, fittings, electrical, consumables | Online |
| **[McMaster-Carr](https://www.mcmaster.com)** | Fasteners, bearings, seals, neoprene, cable trunking | Online / Ships from LA |
| **[Online Metals](https://www.onlinemetals.com)** | SS sheet, aluminum sheet/angle, steel, Dibond ACM | Online |
| **[McNichols](https://www.mcnichols.com)** | Molded GRP (fiberglass) grating, FRP hold-down clips | Online / Multiple branches |
| **[Grating Pacific](https://gratingpacific.com)** | Molded FRP grating (vinyl-ester, grit top) | Los Angeles CA (SoCal) |
| **[Grainger](https://www.grainger.com)** | Industrial supply — local branches throughout SoCal | Multiple SoCal branches |
| **[Lenox Laser](https://www.lenoxlaser.com)** | Custom precision laser-drilled pinholes | Glen Arm, MD |
| **[Hessaire](https://hessaire.com)** | 120V AC evaporative (swamp) coolers | Online |
| **[Victron / Amazon](https://www.victronenergy.com)** | Phoenix pure-sine inverters (Circuit E) | Online |

## See Also
- [Electrical & Systems Report](electrical-report.md) — full wiring specification, circuit fuse ratings, solar architecture
- [Chemistry Shopping List](chemistry-shopping-list.md) — detailed chemistry quantities for all alternative processes (gum bichromate, Van Dyke Brown, salt print)
- [Film Plane Mechanism Report](film-plane-mechanism-report.md) — engineering drawings for the 4-corner actuation system
- [Processing Water System](water-system-report.md) — three-circuit water system with filter skid design
- [Cost Breakdown](project-cost-breakdown.md) — full itemized build cost across three deployment scenarios
- [Funding Proposal](funding-proposal.md) — grant-ready budget summary at three funding levels
- [Operating Manual](operating-manual.md) — step-by-step single-operator workflow from chemistry prep to cleanup