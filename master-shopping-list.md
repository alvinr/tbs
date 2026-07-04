<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# TBS-001 — Master Shopping List (BoM)

**Basis:** April 2026. All prices USD. Prices marked † confirmed from supplier listings; others are close estimates.

Items are grouped by build area. Source documents are cross-referenced in each section header.

## Summary — Estimated Total
<!-- BEGIN costing:master-summary -->
| Area | Low | High |
|------|-----|------|
| 1. Container & delivery | $2,300 | $4,300 |
| 2. Interior conversion (light-seal, paint, backing) | $950 | $1,350 |
| 3. Pinhole optics plate | $95 | $240 |
| 4. Film plane mechanism (4-corner Option A, manual, incl. wall-seat saddles + cross-slides) | $3,454 | $3,914 |
| 5. Print washing — water system (incl. IBC stacking frame) | $4,590 | $6,953 |
| 6. Electrical — power, circuits, wiring | $2,084 | $2,634 |
| 7. Housed revolving-door light lock (plastic-skin custom fabrication) | $1,385 | $2,070 |
| 7a. Panel swing pivot + fixed door frame (Ø89 post + bearings + cage + wall stays + rail saddles + door frame) | $855 | $1,430 |
| 7b. Perimeter walkway (4 sections + drum-exit punch-out) | $2,000 | $2,975 |
| 7c. Hinged panel structure (stepped frame + PP skins + Al core + EPDM + cam latches + B2 bay + pull handle) | $1,124 | $1,691 |
| 7d. Chemistry prep shelf (fold-down board + steel frame + hinge/stays + TAP-01 trunk extension) | $203 | $203 |
| 8. Cooling & ventilation | $824 | $974 |
| 9. Printmaking chemistry — cyanotype, 50 prints (Low = Lean, High = Rich tier) | $1,210 | $2,980 |
| 10. Printmaking tools & consumables | $350 | $500 |
| 11. Safety & PPE | $120 | $180 |
| **TOTAL (base build + 50-print run)** | **~$21,544** | **~$32,394** |
<!-- END costing:master-summary -->

*Optional additions: electric film plane actuation (+$827), lens plate (+$400–$1,500), self-haul transport (+$30,000–$40,000).*

*Line 9 (printmaking chemistry) is the **Mike Ware AmFe** recipe with the corrected ~$300 substrate, re-summed into the TOTAL: **Low = Lean ⅓-Ware (~$1,210), High = Rich full-Ware (~$2,980)**, working default Standard ½-Ware (~$1,650). The tier is pinned by the [Sensitizer Trials](sensitizer-trials.md); the TOTAL spans the Lean–Rich range, so it shifts within ±~$1,330 of the §9 line once a tier is locked.*

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
| 2" black Gorilla Tape | 6 roll | Home Depot | film | $72 |
| Dielectric grease, marine-grade (terminal protection) | 1 ea | Amazon | electrical | $10 |
| Flat black epoxy spray paint | 1 can | Hardware store | shelf | $12 |
| Flat black paint (RAL 9005) | 1 qt | Local fab | panel | $10–$20 |
| Interior matte-black paint | 1 lot | Home Depot | interior | $100–$160 |
| Loctite PL Premium construction adhesive | 2 tube | Home Depot | tray | $15 |
| Matte-black interior finish | 1 ea | Local fab | lightlock | $40–$70 |
| Primer + paint | 1 lot | Hardware store | ibc-frame | $30–$50 |
| Silicone bead sealant (black, UV-stable) | 1 ea | McMaster-Carr | lightlock | $10–$15 |
| Thread seal tape (PTFE) | 4 roll | Home Depot | water | $8 |
| **adhesives-finishes subtotal** | | | | **$307–$432** |

### aluminum

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 3mm aluminum plate (1220 × 2,440mm) | 2 ea | Online Metals | panel | $360–$460 |
| 6061-T6 AL plate 3/16" (5mm) | 1 ea | Online Metals | spray | $16–$28 |
| 6061-T6 AL round tube 25mm OD × 2mm wall, 500mm | 1 ea | Online Metals | spray | $6 |
| Aluminum angle 2"×2"×3/16" | 10 ea | Metal Supermarkets | film | $220 |
| Aluminum face plate 340×240×3mm (flush power panel) | 1 ea | Online Metals | electrical | $18 |
| Aluminum U-channel (per meter) | 40 m | Online Metals | panel | $120–$200 |
| Corner bracket L-plate | 4 ea | Metal Supermarkets | film | $80 |
| Cross-slide intermediate plate (Option A) | 4 ea | Metal Supermarkets | film | $60 |
| Telescoping aluminum pool pole, 4–8 ft | 1 ea | Amazon | spray | $15 |
| **aluminum subtotal** | | | | **$895–$1,087** |

### bearings-motion

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Acme leadscrew ¾"-6 | 4 ea | Roton Products | film | $380 |
| Acme nut bronze ¾"-6 | 4 ea | Roton Products | film | $48 |
| Cross-slide carriage HGH15CA (Option A) | 8 ea | Automation Overstock | film | $96 |
| Cross-slide rail HGR15 (Option A) | 8 ea | Automation Overstock | film | $200 |
| Flanged sleeve (journal) bearing, Ø90 bore | 2 ea | McMaster-Carr | swing | $60–$110 |
| Handwheel 8" dia | 4 ea | Grainger | film | $140 |
| Linear guide rail HGR20 | 4 ea | Automation Overstock | film | $180 |
| Locking collar SS316 | 4 ea | McMaster-Carr | film | $48 |
| Nylon skate wheel, 32mm × 20mm, 10mm bore | 4 ea | Amazon | spray | $12–$20 |
| Rail carriage HGH20CA | 8 ea | Automation Overstock | film | $144 |
| Rod-end spherical bearing | 8 ea | McMaster-Carr | film | $176 |
| SKF 6215-2RS1 sealed bearing | 2 ea | Bearing World | lightlock | $90–$130 |
| Turntable thrust bearing, 12″ (Ø305) 1000 lb | 1 ea | VXB | swing | $40–$60 |
| Ø20mm ball joint, zinc socket, M12 stud | 1 ea | Amazon | spray | $12 |
| **bearings-motion subtotal** | | | | **$1,626–$1,744** |

### chemistry-reagents

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Ammonium dichromate | 1 run | Photographers' Formulary | chemistry | $25 |
| Ammonium iron(III) oxalate (AmFe) | 19.5 kg | Photographers' Formulary | chemistry | $1,170 |
| Potassium ferricyanide | 6.5 kg | Bostick & Sullivan | chemistry | $158 |
| **chemistry-reagents subtotal** | | | | **$1,353** |

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
| Evaporative cooler | 1 ea | Hessaire | ventilation | $130 |
| Ventilation (inline fans + light-trap baffles) — interior-conversion allowance | 1 lot | Amazon | interior | $80–$130 |
| Weatherproof duct cap | 1 ea | Home Depot | ventilation | $8 |
| **ducting-ventilation subtotal** | | | | **$316–$366** |

### electrical-distribution

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 10mm corrugated conduit, drop runs (McMaster 7828K48) | 10 m | McMaster-Carr | electrical | $30 |
| 12V LED flat panel 300×600mm, 20W 4000K | 3 ea | Amazon | electrical | $75 |
| 14 AWG duplex marine wire | 1 roll | Amazon | water | $22 |
| 15A blade fuse | 1 ea | Amazon | water | $5 |
| 16 AWG silicone coiled cable | 1 ea | Waytek Wire | ventilation | $15 |
| 2/0 AWG battery cable, 3ft (battery–fuse–busbar) | 1 lot | Amazon | electrical | $30 |
| 200A main fuse — MRBF terminal-mount (ABYC E-11) | 1 ea | Amazon | electrical | $25 |
| 4 AWG ground wire, green/yellow, 3m | 1 lot | Amazon | electrical | $15 |
| 40×25mm PVC cable trunking, 5m | 4 ea | McMaster-Carr | electrical | $40 |
| Anderson Powerpole 30A connectors, 50 pairs | 1 kit | Powerwerx | electrical | $40 |
| Anderson Powerpole connectors 30A | 4 pair | Amazon | water | $8 |
| Battery main disconnect — Blue Sea m-Series 300A isolator | 1 ea | West Marine | electrical | $40 |
| Battery terminal covers (pair), insulating boots | 1 pair | Amazon | electrical | $10 |
| Blue Sea 5026 fuse block, 12-circuit ST-blade | 1 ea | Amazon | electrical | $55 |
| Brady M210 wire label kit | 1 ea | Amazon | electrical | $80 |
| Cable grommets / glands — steel-shell penetrations | 1 lot | McMaster-Carr | electrical | $15 |
| Cooler external power cable | 1 ea | Waytek Wire | ventilation | $20 |
| Copper ground stake, 8ft × ⅝" dia | 1 ea | Home Depot | electrical | $20 |
| Deutsch DT 2-pin connectors | 2 set | Waytek Wire | ventilation | $8 |
| Deutsch DT 2-pin connectors, IP67 (exterior penetrations) | 10 set | Waytek Wire | electrical | $30 |
| Equipotential bonding kit — 6 AWG + ring lugs | 1 ea | Amazon | electrical | $20 |
| External emergency cut-off — red mushroom IP66 + control loop | 1 ea | AutomationDirect | electrical | $30 |
| Interior emergency cut-off — red mushroom IP65 (paralleled to exterior) | 1 ea | AutomationDirect | electrical | $25 |
| IP65 enclosure 300×200×130mm (fuse block + MPPT) | 1 ea | Amazon | electrical | $60 |
| Master pump switch (Circuit C) — IP67 sealed rocker/disconnect 12V 16A | 1 ea | Amazon | electrical | $10 |
| MC4 bulkhead connector pairs, IP67 panel-mount | 3 pair | Amazon | electrical | $25 |
| MPPT charge-line fuse — 60A ANL/MIDI + holder | 1 ea | Blue Sea | electrical | $15 |
| NEMA 5-15R weatherproof inlet (flush power panel) | 1 ea | Amazon | electrical | $25 |
| Pull-cord ceiling switch, 12V 6A SPST | 2 ea | Amazon | electrical | $16 |
| Pump distribution block — 12V DC + / − bus, 6-way | 1 ea | Blue Sea | electrical | $15 |
| PV cable 10 AWG + MC4 connectors | 1 lot | Amazon | electrical | $30 |
| Remote battery switch — Blue Sea ML-RBS 500A magnetic-latch (E-stop trip) | 1 ea | West Marine | electrical | $150 |
| Sealed wet-zone connectors — Deutsch DT / adhesive heat-shrink | 1 lot | Waytek Wire | electrical | $25 |
| Shore-charger output fuse — 20A inline | 1 ea | Amazon | electrical | $5 |
| Tinned marine wire 14/16 AWG, ~25ft (wet-zone runs) | 1 lot | Waytek Wire | electrical | $30 |
| Wiring kit — 12/14/16/18 AWG tinned, 50ft/color | 1 kit | Waytek Wire | electrical | $80 |
| **electrical-distribution subtotal** | | | | **$1,144** |

### electrical-power

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Cooler inverter | 1 ea | Victron | ventilation | $275 |
| LiFePO4 battery, 100Ah 12V (Renogy Smart Lithium) | 1 ea | Renogy | electrical | $350 |
| PV array disconnect — DC load-break isolator, 50A/150VDC (NEC 690.13) | 1 ea | AutomationDirect | electrical | $40 |
| Solar panel ground-mount tilt frame, 30° | 1 ea | Renogy | electrical | $80 |
| Solar panel, 200W monocrystalline 12V | 3 ea | Renogy | electrical | $399 |
| Victron Blue Smart IP65 12/15 shore backup charger | 1 ea | altE Store | electrical | $150 |
| Victron SmartSolar MPPT 100/50 charge controller | 1 ea | altE Store | electrical | $200 |
| **electrical-power subtotal** | | | | **$1,494** |

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
| 100mm Ø SS grab rail | 1 ea | McMaster-Carr | lightlock | $15–$25 |
| 10mm × 60mm 304 SS axle pin (4-pack) | 1 pack | Amazon | spray | $5 |
| 25mm ratchet strap, 1,100 kg WLL | 4 ea | Amazon | ibc-frame | $30–$50 |
| 25mm welded D-ring | 4 ea | McMaster-Carr | ibc-frame | $20–$35 |
| 304 SS saddle clamp, 10mm (10-pack) | 8 ea | Amazon | spray | $10 |
| 316 SS D-grab pull handle (~300mm) + 2× M8 SS bolts + backing plate, matte-black | 1 ea | McMaster-Carr | panel | $20–$35 |
| Cam-lever spring clamp | 92 ea | McMaster-Carr | clamp | $276–$736 |
| Continuous (piano) hinge, 600 mm | 1 ea | McMaster-Carr | shelf | $20 |
| Corridor panel mount hardware (brackets + fasteners) | 1 lot | Home Depot | water | $25–$50 |
| Cushioned pipe clip | 16 ea | Amazon | water | $16–$32 |
| Door & access upgrades | 1 lot | Home Depot | interior | $50–$100 |
| Folding shelf stays/brackets | 2 ea | Amazon | shelf | $24 |
| Grating clips | 30 ea | McNichols | walkway | $30–$50 |
| M10 wedge floor anchors | 20 ea | McMaster-Carr | walkway | $25–$45 |
| M12 floor anchor (wedge/sleeve, container floor) | 16 ea | McMaster-Carr | ibc-frame | $30–$60 |
| M12 through-bolt kit (right walkway) | 24 ea | McMaster-Carr | walkway | $30–$50 |
| M12 × 40 bolt, Grade 8.8 | 12 ea | McMaster-Carr | ibc-frame | $12–$22 |
| M12×80mm through-bolt kit | 58 ea | McMaster-Carr | walkway | $87–$145 |
| M12×90mm hex through-bolt + nut + washers, SS | 28 ea | McMaster-Carr | film | $70 |
| M5 SS Nylock nut | 184 ea | McMaster-Carr | clamp | $15 |
| M5×16 mm CSK screws | 8 ea | McMaster-Carr | shelf | $4 |
| M5×16 SS socket head bolt | 184 ea | McMaster-Carr | clamp | $46 |
| M6 bolt+nut+washer set, SS (panel mount) | 4 set | McMaster-Carr | electrical | $5 |
| M6 SS hex bolt + nut | 1 ea | McMaster-Carr | spray | $1 |
| M6 SS hex bolts + flange nuts | 12 ea | McMaster-Carr | tray | $12 |
| M6×20 SS bolts + nyloc nuts | 16 ea | McMaster-Carr | spray | $7 |
| M8 hex fixing bolt + nut, SS | 8 ea | McMaster-Carr | film | $16 |
| M8 wall bolts + washers/nuts | 12 ea | McMaster-Carr | shelf | $12 |
| M8×25mm knurled thumbscrew DIN 464 | 12 ea | Amazon | film | $36 |
| Misc. conversion hardware | 1 lot | Home Depot | interior | $80–$130 |
| Nylon zip ties, 200mm | 6 ea | Amazon | spray | $1 |
| Pivot pin SS316 | 8 ea | McMaster-Carr | film | $64 |
| Ratchet straps, 25mm | 2 ea | Home Depot | ventilation | $12 |
| Self-tapping SS screws (8-pack) | 4 ea | McMaster-Carr | spray | $5 |
| Shurflo pump mounting bracket | 5 ea | Amazon | water | $50 |
| Southco C2-33 cam compression latch | 4 ea | Southco | panel | $60–$100 |
| SS beam clamp plates (top + bottom) + spacers (25mm) | 4 ea | McMaster-Carr | spray | $10 |
| SS/nylon retainer clips for 3/4" LDPE | 2 ea | Amazon | spray | $4 |
| Stainless fasteners + nylon isolation washers | 1 lot | McMaster-Carr | lightlock | $30–$50 |
| Top + bottom wall stays + 4-bolt anchor plates | 2 set | McMaster-Carr | swing | $90–$160 |
| Transport latch (over-center/barrel) | 1 ea | Amazon | shelf | $8 |
| **fasteners-hardware subtotal** | | | | **$1,363–$2,312** |

### plastics-sheet

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 4mm black polypropylene sheet | 1 lot | TAP Plastics | lightlock | $150–$240 |
| 4mm black PP plastic sheet (1220 × 2,440mm) | 4 sheet | TAP Plastics | panel | $260–$420 |
| 4mm black PP sheet + EPDM lip | 1 lot | TAP Plastics | panel | $60–$120 |
| 5mm UV-stabilized HDPE sheet (black) | 1 lot | TAP Plastics | lightlock | $180–$280 |
| Dibond ACM panel 4mm | 6 sheet | Grimco | film | $510 |
| Drum-exit punch-out grating | 1 lot | McNichols | walkway | $50–$65 |
| HDPE flat bar, 50mm wide | 5 ea | Online Metals | tray | $40–$75 |
| Image-plane flat backing — Dibond ACM | 1 lot | TAP Plastics | interior | $490–$620 |
| Molded GRP (fiberglass) grating | 1 lot | McNichols | walkway | $965–$1,250 |
| **plastics-sheet subtotal** | | | | **$2,705–$3,580** |

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
| 1/2" ID reinforced braided PVC hose | 2 length | Amazon | water | $20 |
| 1/2" NPT 90° elbow polypropylene | 14 ea | Amazon | water | $28–$56 |
| 1/2" NPT polypropylene tee | 6 ea | Amazon | water | $12–$24 |
| 1/2" NPT polypropylene union | 6 ea | Amazon | water | $24–$36 |
| 1/2" reinforced braided PVC hose, 15 ft | 1 ea | Amazon | spray | $15 |
| 1/2" SDR-11 HDPE pipe | 4 stick | Ferguson | water | $24–$40 |
| 1/2"×1" NPT bushing reducer | 1 ea | Amazon | water | $3–$5 |
| 1/4" irrigation poly tube | 1 ea | Amazon | spray | $6 |
| 2" polypropylene camlock pairs (M+F) | 4 pair | Amazon | water | $20–$32 |
| 3-way diverter valve 1" FNPT | 1 ea | Amazon | water | $18–$30 |
| 3-way diverter valve 1/2" FNPT | 1 ea | Amazon | water | $12–$22 |
| 3/4" LDPE irrigation poly pipe, 15 ft | 1 ea | Amazon | spray | $10 |
| 3/4" SDR-11 HDPE pipe | 2 stick | Ferguson | water | $20–$30 |
| Banjo EL100-90 elbow 1" NPT | 4 ea | Amazon | water | $12–$20 |
| Banjo TEE100 equal tee 1" NPT | 3 ea | Amazon | water | $12–$18 |
| Banjo TEE100 equal tee, 1" HDPE NPT | 1 ea | Amazon | water | $4–$6 |
| Banjo V050FP ball valve 1/2" FNPT | 3 ea | Amazon | water | $18–$30 |
| Banjo V050FP ball valve 1/2" FNPT | 1 ea | Amazon | water | $6–$10 |
| Banjo V050FP ball valve 1/2" FNPT | 2 ea | Amazon | water | $12–$20 |
| Banjo V100FP ball valve 1" FNPT | 6 ea | Amazon | water | $60–$96 |
| Barbed tees, tube into the side poly manifold | 7 ea | Amazon | spray | $10 |
| Bulkhead fitting 2" NPT (304 SS) | 3 ea | McMaster-Carr | water | $75–$120 |
| Distribution manifold, 1/2" → 7 barb outlets | 1 ea | Amazon | spray | $12 |
| Flat-fan irrigation spray nozzles, barbed | 26 ea | Amazon | spray | $30–$50 |
| pH sample tap (SV-01) — 1/2" PP ball valve + barb spout + branch tee | 1 ea | Amazon | water | $10–$18 |
| pH sample tap (SV-02) — 1/2" PP ball valve + barb spout + branch tee | 1 ea | Amazon | water | $10–$18 |
| S60×6 to 1" NPT adapter | 8 ea | Amazon | water | $64–$120 |
| ½" HDPE pipe (tap relocation) | 1 lot | Irrigation supply | shelf | $10 |
| **plumbing-fittings subtotal** | | | | **$654–$1,025** |

### seals-gaskets

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 20mm EPDM gasket (per meter, closed-cell) | 21 m | McMaster-Carr | panel | $84–$126 |
| Black EPDM foam tape 1"×½" | 3 roll | McMaster-Carr | film | $84 |
| Felt/brush wiper strip + 12mm closed-cell neoprene | 1 lot | McMaster-Carr | lightlock | $40–$60 |
| Light-sealing materials (interior conversion) | 1 lot | McMaster-Carr | interior | $150–$210 |
| Neoprene gasket 340×240×3mm (panel weatherseal) | 1 ea | McMaster-Carr | electrical | $6 |
| Neoprene strip 60A | 1 roll | McMaster-Carr | clamp | $15 |
| Silicone gasket strip | 1 ea | McMaster-Carr | tray | $20 |
| **seals-gaskets subtotal** | | | | **$399–$521** |

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
| 304 SS RHS 40×25×3mm, 8 ft * | 2 ea | Online Metals | spray | $96–$144 |
| 3mm steel plate/angle (~110mm × ~4 m) | 1 lot | Metal Supermarkets | door | $45–$80 |
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
| Drop-in rail saddles + tapered dowels | 4 ea | Local fab | swing | $80–$130 |
| Drum support cage, 40 × 40 × 3mm SHS | 1 lot | Local fab | swing | $70–$120 |
| Floor-leg cantilever bracket (left walkway, ×5) | 5 ea | Local fab | walkway | $55–$95 |
| Mild steel plate 8mm (laser/plasma cut + welded) | 6 ea | Metal Supermarkets | film | $318 |
| Reinforcing plate (exterior) | 18 ea | Local fab | walkway | $75–$130 |
| Right walkway cantilever frame | 1 lot | Metal Supermarkets | walkway | $28–$40 |
| Shutter plate (⅛ steel 10×8) + slide channel | 1 ea | Local fab | optics | $25–$50 |
| Steel backing plate 6×6×⅛ + welded frame | 1 ea | Metal Supermarkets | optics | $20–$40 |
| Steel flat bar 25×3mm — ribbon support cross-brace | 4 ea | Home Depot | water | $8–$16 |
| Transition bearing plate | 2 ea | Local fab | walkway | $5–$10 |
| Wall cleat (left corners) | 2 ea | Local fab | walkway | $20–$35 |
| Wall mounting cleat + anchors | 1 lot | Local fab | shelf | $18 |
| Ø89×8mm CHS pivot post + machined hub / thrust collar | 1 ea | Metal Supermarkets | swing | $180–$300 |
| **steel-structural subtotal** | | | | **$2,288–$3,391** |

### substrate-fabric

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Unbleached muslin, 60" wide | 3 roll | Fabric Direct | chemistry | $300 |
| **substrate-fabric subtotal** | | | | **$300** |

### timber-ply

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Corridor plumbing-panel marine ply (18mm) | 1 sheet | marine plywood supplier | water | $120–$200 |
| Exterior-grade plywood (Fan B mount band) | 1 2'×4' ¾" panel | Home Depot | panel | $30–$50 |
| Phenolic-faced plywood (work surface) | 1 4'×8' ¾" sheet | Home Depot | shelf | $60 |
| Plywood base plate (cooler stowage) | 1 2'×4' ½" panel | Home Depot | ventilation | $8 |
| Pump-mount shirt marine ply (25mm) | 1 piece | marine plywood supplier | water | $70–$130 |
| **timber-ply subtotal** | | | | **$288–$448** |

### tools-safety

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 6-mil black LDPE sheet, 10 ft × 8 ft | 1 ea | Home Depot | tray | $8 |
| 6-mil black LDPE sheeting | 1 roll | Home Depot | water | $100 |
| 6-mil black poly sheeting | 1 roll | Home Depot | film | $65 |
| Apera Instruments AI311 PH60 pH meter | 1 ea | Amazon | water | $55 |
| Chemical-resistant labels (GHS) | 1 pack | Amazon | water | $20 |
| Citric acid, food grade, 5 lb | 2 bag | Amazon | water | $28 |
| Nitrile gloves, box of 100 | 2 box | Amazon | water | $28 |
| pH calibration solution set | 1 set | Amazon | water | $10 |
| **tools-safety subtotal** | | | | **$314** |

### water-equipment

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Big Blue filter housing 4.5"×20" (separate) | 3 ea | Amazon | water | $114–$186 |
| CTO carbon block cartridge 4.5"×20" | 2 ea | Amazon | water | $32–$60 |
| HDPE spacer blocks 25mm (filter skid) | 1 lot | McMaster-Carr | water | $12–$22 |
| IBC tote (1,000 L caged) | 4 ea | Container Exchanger | water | $320–$600 |
| KDF-55 heavy-metal cartridge 4.5"×20" | 1 ea | Amazon | water | $40–$70 |
| MPP 5-micron sediment cartridge 4.5"×20" | 2 ea | Amazon | water | $24–$40 |
| SeaFlo accumulator (0.75 L) | 1 ea | Amazon | water | $35 |
| Shurflo 2088-554-144 pump (P-01 Blue supply) | 1 ea | Amazon | water | $55–$70 |
| Shurflo 2088-554-144 pump (P-02 filter loop) | 1 ea | Amazon | water | $55–$70 |
| Shurflo 2088-554-144 pump (P-03 waste evacuation) | 1 ea | Amazon | water | $65 |
| Shurflo 2088-554-144 pump (P-04 tray drain transfer) | 1 ea | Amazon | water | $65 |
| Shurflo 2088-554-144 pump (P-05 Brown drain) | 1 ea | Amazon | water | $65 |
| Slotted steel angle frame 25×25×3mm (filter skid) | 1 lot | Home Depot | water | $25–$45 |
| Steel U-bracket (filter housing) | 3 ea | McMaster-Carr | water | $21–$30 |
| **water-equipment subtotal** | | | | **$928–$1,423** |

## Supplier consolidation (largest orders first)

| Supplier | Line items | Types | Est. cost |
|----------|-----------|-------|-----------|
| containermgt.com | 1 | container | $2,000–$3,500 |
| Local fab | 16 | adhesives-finishes, fabrication-labor, steel-structural | $1,946–$3,156 |
| McMaster-Carr | 42 | adhesives-finishes, bearings-motion, electrical-distribution, fasteners-hardware, plumbing-fittings, seals-gaskets, water-equipment | $1,808–$2,777 |
| Amazon | 80 | adhesives-finishes, aluminum, bearings-motion, ducting-ventilation, electrical-distribution, fabric-textile, fasteners-hardware, plumbing-fittings, tools-safety, water-equipment | $2,145–$2,695 |
| Online Metals | 9 | aluminum, plastics-sheet, stainless-sheet, steel-structural | $1,406–$1,961 |
| TAP Plastics | 5 | plastics-sheet | $1,140–$1,680 |
| Metal Supermarkets | 12 | aluminum, steel-structural | $1,301–$1,638 |
| McNichols | 3 | fasteners-hardware, plastics-sheet | $1,045–$1,365 |
| Photographers' Formulary | 2 | chemistry-reagents | $1,195 |
| Local plastic fab | 1 | fabrication-labor | $800–$1,150 |
| Home Depot | 22 | adhesives-finishes, ducting-ventilation, electrical-distribution, fasteners-hardware, steel-structural, timber-ply, tools-safety, water-equipment | $862–$1,095 |
| Local sheet metal | 3 | fabrication-labor, steel-structural | $500–$900 |
| Renogy | 3 | electrical-power | $829 |
| Commercial tilt-bed hire | 1 | fabrication-labor | $300–$800 |
| Automation Overstock | 4 | bearings-motion | $620 |
| Container Exchanger | 1 | water-equipment | $320–$600 |
| Grimco | 1 | plastics-sheet | $510 |
| Roton Products | 2 | bearings-motion | $428 |
| altE Store | 2 | electrical-power | $350 |
| marine plywood supplier | 2 | timber-ply | $190–$330 |
| Fabric Direct | 1 | substrate-fabric | $300 |
| Victron | 1 | electrical-power | $275 |
| Waytek Wire | 7 | electrical-distribution | $208 |
| West Marine | 2 | electrical-distribution | $190 |
| Bostick & Sullivan | 1 | chemistry-reagents | $158 |
| Lenox Laser | 1 | stainless-sheet | $50–$150 |
| Grainger | 1 | bearings-motion | $140 |
| Hessaire | 1 | ducting-ventilation | $130 |
| Bearing World | 1 | bearings-motion | $90–$130 |
| Ferguson | 4 | plumbing-fittings | $74–$120 |
| Southco | 1 | fasteners-hardware | $60–$100 |
| AutomationDirect | 3 | electrical-distribution, electrical-power | $95 |
| B&H Photo | 1 | fabric-textile | $95 |
| Hardware store | 2 | adhesives-finishes | $42–$62 |
| VXB | 1 | bearings-motion | $40–$60 |
| Steel service center | 1 | steel-structural | $30–$50 |
| Powerwerx | 1 | electrical-distribution | $40 |
| Blue Sea | 2 | electrical-distribution | $30 |
| Irrigation supply | 1 | plumbing-fittings | $10 |
| Steel offcut | 1 | steel-structural | $5 |
<!-- END parts:master -->

## 9. Printmaking Chemistry — Cyanotype (50 prints)
*Source: `chemistry-shopping-list.md`. **Procurement** — reagent order quantities, per-tier costs,
suppliers, and the muslin substrate — is in the Procurement BOM above (`chemistry-reagents` +
`substrate-fabric`) and the [Cyanotype Shopping List](chemistry-shopping-list.md). This section is the
**recipe + per-print basis** only.*

**Mike Ware New Cyanotype** — 3:1 ammonium iron(III) oxalate (AmFe) : potassium ferricyanide by weight
+ ammonium dichromate for contrast, applied as **two wet-on-wet coats** over the 10.74 m² active plane.

| Reagent | Per print (Standard ½-Ware) | × 50 prints |
|---------|-----------------------------|-------------|
| Ammonium iron(III) oxalate (AmFe) | <!-- BEGIN costing:om-amfe-g-standard -->390<!-- END costing:om-amfe-g-standard -->g | <!-- BEGIN costing:om-amfe-kg-standard -->19.5<!-- END costing:om-amfe-kg-standard --> kg |
| Potassium ferricyanide (3:1) | 130g | 6.5 kg |
| Ammonium dichromate (contrast, 0.1–0.4%) | ~1–4g | ~0.2 kg |
| Distilled water | ~2.6 L | ~130 L |

Standard ½-Ware is the working default; the leanest/richest viable strength — and the final order — is
pinned by the [Sensitizer Trials](sensitizer-trials.md). **Run cost ~$1,650 (Standard), range ~$1,210
(Lean) – ~$2,980 (Rich)** per 50-print run (~$24–60/print), incl. ~$300 muslin substrate — ~445 linear
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
| **[Roton Products](https://www.roton.com)** | Acme leadscrews and nuts, cut to length | Ships from LA area |
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