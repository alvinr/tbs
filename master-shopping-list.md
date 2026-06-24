<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# TBS-001 — Master Shopping List

**Camera:** The Big Shoebox Project — TBS-001
**Basis:** April 2026. All prices USD. Prices marked † confirmed from supplier listings; others are close estimates.
**Process assumed:** Cyanotype (lowest cost, no hazmat, no silver). See `chemistry-shopping-list.md` for alternative process costs.
**Power assumed:** 12V DC off-grid solar + LiFePO4. See `electrical-report.md` for full architecture.

Items are grouped by build area. Source documents are cross-referenced in each section header.

## Summary — Estimated Total
<!-- BEGIN costing:master-summary -->
| Area | Low | High |
|------|-----|------|
| 1. Container & delivery | $2,300 | $4,300 |
| 2. Interior conversion (light-seal, paint, backing) | $950 | $1,350 |
| 3. Pinhole optics plate | $95 | $240 |
| 4. Film plane mechanism (4-corner Option A, manual, incl. wall-seat saddles + cross-slides) | $3,538 | $4,088 |
| 5. Print washing — water system (incl. IBC stacking frame) | $4,211 | $6,297 |
| 6. Electrical — power, circuits, wiring | $2,110 | $2,660 |
| 7. Housed revolving-door light lock (plastic-skin custom fabrication) | $1,385 | $2,070 |
| 7a. Panel swing pivot + fixed door frame (Ø89 post + bearings + cage + wall stays + rail saddles + door frame) | $855 | $1,430 |
| 7b. Perimeter walkway (4 sections + drum-exit punch-out) | $2,000 | $2,975 |
| 7c. Hinged panel structure (stepped frame + PP skins + Al core + EPDM + cam latches + B2 bay + pull handle) | $1,124 | $1,691 |
| 7d. Chemistry prep shelf (fold-down board + steel frame + hinge/stays + TAP-01 trunk extension) | $203 | $203 |
| 8. Cooling & ventilation | $824 | $974 |
| 9. Printmaking chemistry — cyanotype, 50 prints (Low = Lean, High = Rich tier) | $1,210 | $2,980 |
| 10. Printmaking tools & consumables | $350 | $500 |
| 11. Safety & PPE | $120 | $180 |
| **TOTAL (base build + 50-print run)** | **~$21,275** | **~$31,938** |
<!-- END costing:master-summary -->

*Optional additions: electric film plane actuation (+$827), lens plate (+$400–$1,500), self-haul transport (+$30,000–$40,000).*

*Line 9 (printmaking chemistry) is now the **Mike Ware AmFe** recipe with the corrected ~$300 substrate, re-summed into the TOTAL: **Low = Lean ⅓-Ware (~$1,210), High = Rich full-Ware (~$2,980)**, working default Standard ½-Ware (~$1,650). The tier is pinned by the [Sensitizer Trials](sensitizer-trials.md); the TOTAL spans the Lean–Rich range, so it shifts within ±~$1,330 of the §9 line once a tier is locked.*

---

## Procurement BOM — by material type & supplier

*Generated from the parts registry (`src/generators/parts.py`) — the single source of every
purchasable item across all systems. This replaces the old by-system list, which duplicated each
report's own parts list. Procurement reads parts grouped by **type** with quantities summed across
systems, then a **supplier-consolidation** table to place the fewest, largest orders; the per-system
detail lives in each report. Refresh with `python3 src/generators/parts.py --inject`.*

<!-- BEGIN parts:master -->
## Procurement BOM — by material type

### container

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 20 ft ISO container — CW (cargo-worthy) grade | 1 ea | containermgt.com | container | $2,000–$3,500 |
| **container subtotal** | | | | **$2,000–$3,500** |

### steel-structural

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| IBC stacking frame — RHS restraint portal + feet + retaining bars + hangers + fab | 1 lot | Metal Supermarkets | water | $955–$1,455 |
| Cantilever bracket — standard (near/far) | 14 ea | Local fab | walkway | $420–$700 |
| Wall-seat saddles ×8 — 8mm steel plate, cut + welded (ICP-11) | 8 ea | local fab | film | $380–$470 |
| Ø89×8 CHS pivot post + machined hub / thrust collar | 1 ea | Metal Supermarkets | swingpivot | $180–$300 |
| Cantilever bracket — widened (near) | 4 ea | Local fab | walkway | $160–$280 |
| 50×50×3mm RHS mild steel — frame perimeter + members (4× 6m) | 4 ea | Metal Supermarkets | panel | $120–$160 |
| Drop-in rail saddles + tapered dowels (×4, removable left film rails) | 4 ea | local fab | swingpivot | $80–$130 |
| Reinforcing plate (exterior) | 18 ea | Local fab | walkway | $75–$130 |
| Canopy frame | 1 lot | Home Depot | ventilation | $120 |
| Drum support cage, 40×40×3mm SHS | 1 lot | local fab | swingpivot | $70–$120 |
| Fixed door frame — 50×50×3 RHS members (×3) | 3 ea | Metal Supermarkets | swingpivot | $90–$120 |
| Floor-leg cantilever bracket (left walkway, ×5) | 5 ea | Local fab | walkway | $55–$95 |
| Fixed door frame — top/bottom seal lips (3mm steel ~110×4m) | 1 lot | Metal Supermarkets | swingpivot | $45–$80 |
| Combined corner plate (right corners) | 2 ea | Local fab | walkway | $50–$80 |
| Shutter plate (⅛ steel 10×8) + slide channel | 1 ea | local fab | optics | $25–$50 |
| 75mm Ø × 150mm steel stub shafts (×2) | 2 ea | steel service center | lightlock | $30–$50 |
| Steel backing plate 6×6×⅛ + welded frame | 1 ea | Metal Supermarkets | optics | $20–$40 |
| Right walkway cantilever frame | 1 lot | Metal Supermarkets | walkway | $28–$40 |
| Wall cleat (left corners) | 2 ea | Local fab | walkway | $20–$35 |
| Baffle duct sheet metal (fans) | 1 lot | Local sheet metal | ventilation | $30 |
| 25×25×3 mm steel SHS | 1 lot | Online Metals | shelf | $30 |
| Baffle duct sheet metal (cooler) | 1 lot | Local sheet metal | ventilation | $20 |
| Wall mounting cleat + anchors | 1 lot | Local fab | shelf | $18 |
| Transition bearing plate | 2 ea | Local fab | walkway | $5–$10 |
| Corner gusset plate, 3 mm | 4 ea | Steel offcut | shelf | $5 |
| **steel-structural subtotal** | | | | **$3,031–$4,568** |

### stainless-sheet

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Processing tray — 304 SS panels + fabrication, shim strips, sump pickup, liner, hardware | 1 lot | Online Metals | water | $1,300–$2,015 |
| Custom laser-drilled pinhole — SS-302/304 shim, 3×3 | 1 ea | Lenox Laser | optics | $50–$150 |
| **stainless-sheet subtotal** | | | | **$1,350–$2,165** |

### aluminum

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 3mm aluminum plate — corner-zone core plates (×2) | 2 ea | Online Metals | panel | $360–$460 |
| Spray bar — beam, LDPE pipe, 26 nozzles, manifold + 7 feed tubes, 4 wheels, ball joint, arm, hose | 1 lot | Online Metals | water | $235–$299 |
| Aluminum angle 2×2×3/16 8 ft (×10) | 10 ea | Online Metals | film | $220 |
| Aluminum U-channel — gasket + PP-skin retention (~40 m) | 40 m | Online Metals | panel | $120–$200 |
| Corner bracket L-plates, ¼" alum 6×8 (×4) | 4 ea | Online Metals | film | $80 |
| Aluminum face plate 340×240×3mm (flush power panel) | 1 ea | Online Metals | electrical | $18 |
| **aluminum subtotal** | | | | **$1,033–$1,277** |

### plastics-sheet

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Molded GRP (fiberglass) grating | 1 lot | McNichols | walkway | $970–$1,260 |
| Image-plane flat backing — Dibond ACM | 1 lot | TAP Plastics | interior | $490–$620 |
| Dibond ACM 4mm 4×8 sheets (×6) — single rigid plane | 6 sheet | TAP Plastics | film | $510 |
| 4mm black PP sheet — panel skins both faces (~12 m², ×4) | 4 sheet | TAP Plastics | panel | $260–$420 |
| 5mm UV-stabilized HDPE — Ø900 housing shell (~7 m²) | 1 lot | TAP Plastics | lightlock | $180–$280 |
| 4mm PP — Ø864 drum shell + top/bottom caps (~7 m²) | 1 lot | TAP Plastics | lightlock | $150–$240 |
| 4mm PP + EPDM lip — B2 punch-out bay (4-wall tube ~890mm) | 1 lot | TAP Plastics | panel | $60–$120 |
| Drum-exit punch-out grating | 1 lot | McNichols | walkway | $50–$65 |
| **plastics-sheet subtotal** | | | | **$2,670–$3,515** |

### timber-ply

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Phenolic-faced plywood, 18 mm | 1 ea | Home Depot | shelf | $60 |
| 18mm exterior-grade plywood — Fan B mount band (0.5 sheet) | 1 lot | Home Depot | panel | $30–$50 |
| Plywood base plate | 1 ea | Home Depot | ventilation | $8 |
| **timber-ply subtotal** | | | | **$98–$118** |

### fasteners-hardware

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Cam-lever spring clamps, muslin (×92) | 92 ea | Amazon | film | $276–$736 |
| Top + bottom wall stays + 4-bolt anchor plates | 2 set | McMaster-Carr | swingpivot | $90–$160 |
| Saddle fasteners — M12 through-bolts (×36) + M8 thumbscrews (×12) + M8 rail bolts (×12) | 1 lot | McMaster-Carr | film | $150 |
| M12×80mm through-bolt kit | 58 ea | McMaster-Carr | walkway | $87–$145 |
| Misc. conversion hardware | 1 lot | Home Depot | interior | $80–$130 |
| Door & access upgrades | 1 lot | Home Depot | interior | $50–$100 |
| Southco C2-33 cam compression latch (×4) | 4 ea | Southco | panel | $60–$100 |
| Clamp mounting — M5×16 SS bolts/Nylocks (×184+184) + neoprene jaw strip | 1 lot | McMaster-Carr | film | $70 |
| Grating clips | 30 ea | McNichols | walkway | $30–$50 |
| Stainless fasteners + nylon isolation washers (no galvanic couple) | 1 lot | McMaster-Carr | lightlock | $30–$50 |
| M12 through-bolt kit (right walkway) | 24 ea | McMaster-Carr | walkway | $30–$50 |
| M10 wedge floor anchors | 20 ea | McMaster-Carr | walkway | $25–$45 |
| 316 SS D-grab pull handle (~300mm) + 2× M8 + backing plate | 1 ea | McMaster-Carr | panel | $20–$35 |
| 100mm Ø SS grab rail (400mm cut) | 1 ea | McMaster-Carr | lightlock | $15–$25 |
| Folding shelf stays/brackets | 2 ea | Amazon | shelf | $24 |
| Continuous (piano) hinge, 600 mm | 1 ea | McMaster-Carr | shelf | $20 |
| Ratchet straps, 25mm | 2 ea | Home Depot | ventilation | $12 |
| M8 wall bolts + washers/nuts | 12 ea | McMaster-Carr | shelf | $12 |
| Transport latch (over-center/barrel) | 1 ea | Amazon | shelf | $8 |
| M6 bolt+nut+washer set, SS (panel mount) | 4 set | McMaster-Carr | electrical | $5 |
| M5×16 mm CSK screws | 8 ea | McMaster-Carr | shelf | $4 |
| **fasteners-hardware subtotal** | | | | **$1,098–$1,931** |

### bearings-motion

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Acme leadscrews ¾"-6 8 ft (×4) + bronze nuts (×4) | 1 set | McMaster-Carr | film | $428 |
| Option-A cross-slides — HGR15 rails (×8) + HGH15CA (×8) + intermediate plates (×4) | 1 set | Amazon | film | $356 |
| Linear guide rails HGR20 2,200mm (×4) + carriages HGH20CA (×8) | 1 set | Amazon | film | $324 |
| Rod-end spherical bearings GIR25-DO (×8) + pivot pins SS316 (×8) | 1 set | McMaster-Carr | film | $240 |
| Handwheels 8" (×4) + locking collars SS316 (×4) | 1 set | McMaster-Carr | film | $188 |
| SKF 6215-2RS1 sealed bearing (×2) | 2 ea | Bearing World | lightlock | $90–$130 |
| Flanged sleeve (journal) bearings, Ø90 bore (×2) | 2 ea | McMaster-Carr | swingpivot | $60–$110 |
| Turntable thrust bearing, 12″ (Ø305) 1000 lb | 1 ea | VXB | swingpivot | $40–$60 |
| **bearings-motion subtotal** | | | | **$1,726–$1,836** |

### plumbing-fittings

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Valves + fittings — S60×6 adapters, check valves CV1/CV3/CV4 | 1 lot | Amazon | water | $390–$630 |
| Pipe — HDPE, spray-bar feed | 1 lot | Ferguson | water | $100–$140 |
| ½" HDPE pipe (tap relocation) | 1 lot | Irrigation supply | shelf | $10 |
| **plumbing-fittings subtotal** | | | | **$500–$780** |

### water-equipment

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Water storage — 4× IBC totes + 3× bulkhead fittings + fill tee | 1 lot | Container Exchanger | water | $395–$720 |
| Filter skid — 3× Big Blue housings + cartridges | 1 lot | Amazon | water | $265–$370 |
| Pumps + accumulator — P-01/P-02/P-04 manifold + P-03 | 1 lot | Amazon | water | $305–$355 |
| **water-equipment subtotal** | | | | **$965–$1,445** |

### electrical-power

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Solar panel, 200W monocrystalline 12V | 3 ea | Renogy | electrical | $399 |
| LiFePO4 battery, 100Ah 12V (Renogy Smart Lithium) | 1 ea | Renogy | electrical | $350 |
| Cooler inverter | 1 ea | Victron | ventilation | $275 |
| Victron SmartSolar MPPT 100/50 charge controller | 1 ea | altE Store | electrical | $200 |
| Victron Blue Smart IP65 12/15 shore backup charger | 1 ea | altE Store | electrical | $150 |
| Solar panel ground-mount tilt frame, 30° | 1 ea | Renogy | electrical | $80 |
| PV array disconnect — DC load-break isolator, 50A/150VDC (NEC 690.13) | 1 ea | AutomationDirect | electrical | $40 |
| **electrical-power subtotal** | | | | **$1,494** |

### electrical-distribution

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Remote battery switch — Blue Sea ML-RBS 500A magnetic-latch (E-stop trip) | 1 ea | West Marine | electrical | $150 |
| Wiring kit — 12/14/16/18 AWG tinned, 50ft/color | 1 kit | Waytek Wire | electrical | $80 |
| Brady M210 wire label kit | 1 ea | Amazon | electrical | $80 |
| 12V LED flat panel 300×600mm, 20W 4000K | 3 ea | Amazon | electrical | $75 |
| IP65 enclosure 300×200×130mm (fuse block + MPPT) | 1 ea | Amazon | electrical | $60 |
| Blue Sea 5026 fuse block, 12-circuit ST-blade | 1 ea | Amazon | electrical | $55 |
| Battery main disconnect — Blue Sea m-Series 300A isolator | 1 ea | West Marine | electrical | $40 |
| Anderson Powerpole 30A connectors, 50 pairs | 1 kit | Powerwerx | electrical | $40 |
| 40×25mm PVC cable trunking, 5m | 4 ea | McMaster-Carr | electrical | $40 |
| Water-system wiring (fuse block in Electrical Report) | 1 lot | Amazon | water | $35 |
| PV cable 10 AWG + MC4 connectors | 1 lot | Amazon | electrical | $30 |
| External emergency cut-off — red mushroom IP66 + control loop | 1 ea | AutomationDirect | electrical | $30 |
| Pump switches (Circuit C) — IP67 sealed rocker 12V 16A | 5 ea | Amazon | electrical | $30 |
| Tinned marine wire 14/16 AWG, ~25ft (wet-zone runs) | 1 lot | Waytek Wire | electrical | $30 |
| 2/0 AWG battery cable, 3ft (battery–fuse–busbar) | 1 lot | Amazon | electrical | $30 |
| Deutsch DT 2-pin connectors, IP67 (exterior penetrations) | 10 set | Waytek Wire | electrical | $30 |
| 10mm corrugated conduit, drop runs (McMaster 7828K48) | 10 m | McMaster-Carr | electrical | $30 |
| NEMA 5-15R weatherproof inlet (flush power panel) | 1 ea | Amazon | electrical | $25 |
| 200A main fuse — MRBF terminal-mount (ABYC E-11) | 1 ea | Amazon | electrical | $25 |
| Interior emergency cut-off — red mushroom IP65 (paralleled to exterior) | 1 ea | AutomationDirect | electrical | $25 |
| Sealed wet-zone connectors — Deutsch DT / adhesive heat-shrink | 1 lot | Waytek Wire | electrical | $25 |
| MC4 bulkhead connector pairs, IP67 panel-mount | 3 pair | Amazon | electrical | $25 |
| Cooler external power cable | 1 ea | Waytek Wire | ventilation | $20 |
| Equipotential bonding kit — 6 AWG + ring lugs | 1 ea | Amazon | electrical | $20 |
| Copper ground stake, 8ft × ⅝" dia | 1 ea | Home Depot | electrical | $20 |
| Pull-cord ceiling switch, 12V 6A SPST | 2 ea | Amazon | electrical | $16 |
| 16 AWG silicone coiled cable | 1 ea | Waytek Wire | ventilation | $15 |
| MPPT charge-line fuse — 60A ANL/MIDI + holder | 1 ea | Blue Sea | electrical | $15 |
| Pump distribution block — 12V DC + / − bus, 6-way | 1 ea | Blue Sea | electrical | $15 |
| Cable grommets / glands — steel-shell penetrations | 1 lot | McMaster-Carr | electrical | $15 |
| 4 AWG ground wire, green/yellow, 3m | 1 lot | Amazon | electrical | $15 |
| Battery terminal covers (pair), insulating boots | 1 pair | Amazon | electrical | $10 |
| Deutsch DT 2-pin connectors | 2 set | Waytek Wire | ventilation | $8 |
| Shore-charger output fuse — 20A inline | 1 ea | Amazon | electrical | $5 |
| **electrical-distribution subtotal** | | | | **$1,164** |

### seals-gaskets

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Light-seal set — EPDM tape (×3) + Rosco Duvetyne + 6-mil poly + Gorilla tape (×6) | 1 set | Rosco | film | $316 |
| Light-sealing materials (interior conversion) | 1 lot | McMaster-Carr | interior | $150–$210 |
| 20mm EPDM gasket — perimeter + housing-surround + cut seals (~21 m) | 21 m | McMaster-Carr | panel | $84–$126 |
| Felt/brush wiper + 12mm neoprene (drum↔housing seal) | 1 lot | McMaster-Carr | lightlock | $40–$60 |
| Neoprene gasket 340×240×3mm (panel weatherseal) | 1 ea | McMaster-Carr | electrical | $6 |
| **seals-gaskets subtotal** | | | | **$596–$718** |

### adhesives-finishes

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Interior matte-black paint | 1 lot | Home Depot | interior | $100–$160 |
| Matte-black interior finish | 1 job | local | lightlock | $40–$70 |
| Flat-black paint (RAL 9005) — bay/weld touch-in | 1 lot | local | panel | $10–$20 |
| Silicone bead sealant (bearing housing) | 1 ea | McMaster-Carr | lightlock | $10–$15 |
| Flat black epoxy spray paint | 1 can | Hardware store | shelf | $12 |
| Dielectric grease, marine-grade (terminal protection) | 1 ea | Amazon | electrical | $10 |
| **adhesives-finishes subtotal** | | | | **$182–$287** |

### fabric-textile

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Shade canopy — 80% shade cloth | 1 ea | Amazon | ventilation | $80 |
| **fabric-textile subtotal** | | | | **$80** |

### ducting-ventilation

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Evaporative cooler | 1 ea | Hessaire | ventilation | $130 |
| Ventilation (inline fans + light-trap baffles) — interior-conversion allowance | 1 lot | Amazon | interior | $80–$130 |
| 150×150×50mm axial fans | 2 ea | Amazon | ventilation | $50 |
| 200mm insulated flex duct | 1 ea | Home Depot | ventilation | $22 |
| 200mm 90° duct elbow | 1 ea | Home Depot | ventilation | $14 |
| Duct collar + hose clamp | 1 ea | Home Depot | ventilation | $12 |
| Weatherproof duct cap | 1 ea | Home Depot | ventilation | $8 |
| **ducting-ventilation subtotal** | | | | **$316–$366** |

### tools-safety

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Processing consumables — 6-mil poly, pH meter, citric acid | 1 lot | Amazon | water | $231–$278 |
| **tools-safety subtotal** | | | | **$231–$278** |

### fabrication-labor

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| Plastic fabrication — roll + weld 2 cylinders, fit (16–22 hrs) | 1 job | Local plastic fab | lightlock | $800–$1,150 |
| Delivery — short haul (<50 miles), tilt-bed | 1 job | Commercial tilt-bed hire | container | $300–$800 |
| Fixed door frame — welding/fabrication + wall attachment | 1 job | local fab | swingpivot | $200–$350 |
| **fabrication-labor subtotal** | | | | **$1,300–$2,300** |

## Supplier consolidation (largest orders first)

| Supplier | Line items | Types | Est. cost |
|----------|-----------|-------|-----------|
| Amazon | 29 | adhesives-finishes, bearings-motion, ducting-ventilation, electrical-distribution, fabric-textile, fasteners-hardware, plumbing-fittings, tools-safety, water-equipment | $2,935–$3,887 |
| containermgt.com | 1 | container | $2,000–$3,500 |
| Online Metals | 8 | aluminum, stainless-sheet, steel-structural | $2,363–$3,322 |
| McMaster-Carr | 25 | adhesives-finishes, bearings-motion, electrical-distribution, fasteners-hardware, seals-gaskets | $1,849–$2,239 |
| Metal Supermarkets | 7 | steel-structural | $1,438–$2,195 |
| TAP Plastics | 6 | plastics-sheet | $1,650–$2,190 |
| McNichols | 3 | fasteners-hardware, plastics-sheet | $1,050–$1,375 |
| Local fab | 8 | steel-structural | $803–$1,348 |
| Local plastic fab | 1 | fabrication-labor | $800–$1,150 |
| local fab | 5 | fabrication-labor, steel-structural | $755–$1,120 |
| Renogy | 3 | electrical-power | $829 |
| Commercial tilt-bed hire | 1 | fabrication-labor | $300–$800 |
| Container Exchanger | 1 | water-equipment | $395–$720 |
| Home Depot | 13 | adhesives-finishes, ducting-ventilation, electrical-distribution, fasteners-hardware, steel-structural, timber-ply | $536–$716 |
| altE Store | 2 | electrical-power | $350 |
| Rosco | 1 | seals-gaskets | $316 |
| Victron | 1 | electrical-power | $275 |
| Waytek Wire | 7 | electrical-distribution | $208 |
| West Marine | 2 | electrical-distribution | $190 |
| Lenox Laser | 1 | stainless-sheet | $50–$150 |
| Ferguson | 1 | plumbing-fittings | $100–$140 |
| Hessaire | 1 | ducting-ventilation | $130 |
| Bearing World | 1 | bearings-motion | $90–$130 |
| Southco | 1 | fasteners-hardware | $60–$100 |
| AutomationDirect | 3 | electrical-distribution, electrical-power | $95 |
| local | 2 | adhesives-finishes | $50–$90 |
| VXB | 1 | bearings-motion | $40–$60 |
| Local sheet metal | 2 | steel-structural | $50 |
| steel service center | 1 | steel-structural | $30–$50 |
| Powerwerx | 1 | electrical-distribution | $40 |
| Blue Sea | 2 | electrical-distribution | $30 |
| Hardware store | 1 | adhesives-finishes | $12 |
| Irrigation supply | 1 | plumbing-fittings | $10 |
| Steel offcut | 1 | steel-structural | $5 |
<!-- END parts:master -->

## 9. Printmaking Chemistry — Cyanotype (50 prints)
*Source: `chemistry-shopping-list.md`*

**Recommended process.** No silver, no DEA registration, no hazmat shipping, development in plain cold water.

### Chemistry — Mike Ware New Cyanotype (3:1 AmFe : ferricyanide + dichromate contrast)
| Item | Per print (Standard) | × 50 prints | Supplier | Unit | Units | Unit price | Total |
|------|-----------|-------------|---------|------|-------|-----------|-------|
| [Ammonium iron(III) oxalate (AmFe)](https://www.bostick-sullivan.com/product/ammonium-ferric-oxalate/) | <!-- BEGIN costing:om-amfe-g-standard -->390<!-- END costing:om-amfe-g-standard -->g | <!-- BEGIN costing:om-amfe-kg-standard -->19.5<!-- END costing:om-amfe-kg-standard --> kg | [Bostick & Sullivan](https://www.bostick-sullivan.com/product/ammonium-ferric-oxalate/) | 500g | 39 | ~$30† | ~$1,170 |
| [Potassium ferricyanide (3:1 ratio)](https://www.bostick-sullivan.com/product/potassium-ferricyanide-250gm/) | 130g | 6.5 kg | [Bostick & Sullivan](https://www.bostick-sullivan.com/product/potassium-ferricyanide-250gm/) | 1,000g | 7 | $24.29† | ~$158 |
| [Ammonium dichromate (contrast, 0.1–0.4%)](https://stores.photoformulary.com/ammonium-dichromate-class-5-1-bichromate-ground-ups-only-choose-ups-ground-at-checkout/) | ~1–4g | ~0.2 kg | [Photographers' Formulary](https://stores.photoformulary.com) | 100g | 3 | ~$12 | ~$25 |
| Distilled water | ~2.6 L | ~130 L | Tap water + DI filter adequate | — | — | — | ~$0 |

> **Ware-AmFe note:** Mike Ware New Cyanotype uses **ammonium iron(III) oxalate (AmFe), not the old ferric ammonium citrate** — 3:1 AmFe:ferricyanide by weight + ammonium dichromate for contrast, applied as **two wet-on-wet coats** over the 10.74 m² active plane. Quantities above are the **Standard ½-Ware** tier (the working default); the leanest/richest viable strength — and the final order — is set by the [Sensitizer Trials](sensitizer-trials.md), giving the tier range below. Matches [cost breakdown §7](project-cost-breakdown.md).
**Chemistry subtotal (Standard): ~$1,353  ·  tier range ~$910 (Lean ⅓-Ware) – ~$2,681 (Rich full-Ware)**

### Substrate
| Item | Qty | Supplier | Unit | Units | Unit price | Total |
|------|-----|---------|------|-------|-----------|-------|
| [Unbleached cotton muslin, 60" wide](https://www.fabricdirect.com) | ~445 linear yards | [Fabric Direct](https://www.fabricdirect.com) | 150-yd roll | 3 | ~$100 | ~$300 |
| OR [unbleached cotton muslin by the yard](https://www.fabricwholesaledirect.com) | ~445 yd | [Fabric Wholesale Direct](https://www.fabricwholesaledirect.com) | per yard | 445 | $0.80–$1.20/yd | $360–$540 |

> **Muslin note:** Pre-wash all fabric twice in hot water, no detergent, to remove sizing. Sizing repels water-based sensitisers. 60" width requires 3 strips per print to cover the 4,499mm width (each 2,388mm tall) — or source 120" (theatrical/backdrop) width to eliminate vertical seams.
> **Muslin correction (2026-06-18):** the prior "1,650 yd / 11 rolls / $1,100" over-counted the fabric ~3.7× (a feet-as-yards error — see [chemistry-shopping-list.md](chemistry-shopping-list.md) Shared Item: Substrate Fabric). Real need is ~445 yd = 3 × 150-yd rolls ≈ **$300**.
**Substrate subtotal: ~$300**

**Section total: ~$1,650 (Standard ½-Ware default)**, range **~$1,210 (Lean) – ~$2,980 (Rich)** per 50-print run (chemistry + $300 substrate; ~$24–60/print) — tier pinned by the [Sensitizer Trials](sensitizer-trials.md). The summary table maps Low = Lean, High = Rich.

## 10. Printmaking Tools & Consumables
*Source: `operating-manual.md`, `chemistry-shopping-list.md`*

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Foam roller 18" wide | For sensitiser application | 3 | Home Depot / art supply | ~$30 |
| Foam brush 4" wide | Detail/edge work | 6 | Home Depot / art supply | ~$15 |
| UV-blocking safety glasses | Mandatory during sensitiser handling | 2 pairs | Amazon / safety supply | ~$20 |
| Nitrile gloves, box of 100 | Size M/L, for chemistry handling | 3 boxes | Amazon / Home Depot | ~$40 |
| Chemical-resistant apron | Full-length | 2 | Amazon / safety supply | ~$30 |
| Red LED safelight headlamp | Loading operations inside container | 2 | Amazon | ~$30 |
| Red LED strip light 12V | Interior safelight — Circuit D | 1 (5m roll) | Amazon | ~$15 |
| Digital timer | Exposure timing | 1 | Amazon / camera store | ~$15 |
| Folding step stool | Reaching top of image plane | 1 | Home Depot | ~$25 |
| [Cam-lever spring clamps](https://www.amazon.com/s?k=over+center+cam+toggle+clamp+small) | Muslin attachment — over-center cam, neoprene jaw, ~5N | 92 | Amazon / McMaster-Carr | ~$3–8 ea |
| [M5×16 SS socket head bolt + Nylock nut](https://www.mcmaster.com/91292A128) | Clamp base plate mounting (2 per clamp) | 184 + 184 | McMaster-Carr #91292A128 | ~$55 |
| [Neoprene strip 60A, 35mm × 6mm](https://www.mcmaster.com/8614K44) | Jaw pads (self-adhesive, cut to 35×12mm) | 1 roll (10m) | McMaster-Carr #8614K44 | ~$15 |
| Spray bottle (1 liter) | Humidity/misting in low-RH conditions | 2 | Amazon / garden supply | ~$15 |
| pH test strips | Quick wash water check | 1 pack | Amazon | ~$10 |
| 6-mil black poly sheeting, 10'×100' | Container floor protection during development | 1 roll | Home Depot / Uline | ~$80 |
**Section total: ~$650–1,100** (range depends on generic vs Destaco-equivalent clamps)

## 11. Safety & PPE
*Source: `operating-manual.md`, `electrical-report.md`*

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
| Supplier | Category | URL / Location |
|---------|---------|----------------|
| **[Photographers' Formulary](https://stores.photoformulary.com)** | FAC, potassium ferricyanide, darkroom chemicals | Condon, MT |
| **[Bostick & Sullivan](https://bostick-sullivan.com)** | Cyanotype, VDB, platinum/palladium chemistry | Santa Fe, NM |
| **[Fabric Direct](https://www.fabricdirect.com)** | Unbleached cotton muslin, 150-yd rolls | Online |
| **[Fabric Wholesale Direct](https://www.fabricwholesaledirect.com)** | Unbleached muslin by yard or bolt | Online |
| **[Rose Brand](https://www.rosebrand.com)** | Rosco Duvetyne blackout fabric | Burbank CA |
| **[Metal Supermarkets](https://www.metalsupermarkets.com)** | Steel, aluminum, cut-to-length | Anaheim · Van Nuys · San Diego |
| **[Grimco](https://www.grimco.com)** | Dibond ACM panels (sign industry) | City of Industry CA |
| **Automation Overstock** | Linear guides, carriages, surplus motion components | Gardena CA (walk-in) |
| **[Roton Products](https://www.roton.com)** | Acme leadscrews and nuts, cut to length | Ships from LA area |
| **[Renogy](https://www.renogy.com)** | Solar panels, MPPT controllers, LiFePO4 batteries | Online |
| **[altE Store](https://www.altestore.com)** | Victron MPPT, Victron chargers, off-grid power | Online |
| **[Battle Born Batteries](https://battlebornbatteries.com)** | 100Ah LiFePO4 12V | Online |
| **[Powerwerx](https://powerwerx.com)** | Anderson Powerpole connectors and tools | Online |
| **[Waytek Wire](https://www.waytekwire.com)** | Deutsch DT connectors, automotive wire | Online |
| **[West Marine](https://www.westmarine.com)** | Blue Sea fuse blocks, marine DC wiring | Torrance CA |
| **[Container Exchanger](https://containerexchanger.com)** | Used IBC totes, food-grade — CA listings | Online |
| **[Ferguson Plumbing](https://www.ferguson.com)** | HDPE pipe, valves, fittings | Multiple SoCal branches |
| **Pacific Coast Steel** | Hot-rolled A36 sheet, round bar, structural steel | Santa Fe Springs CA |
| **[Amazon](https://www.amazon.com)** | Pumps, filters, valves, fittings, electrical, consumables | Online |
| **[McMaster-Carr](https://www.mcmaster.com)** | Fasteners, bearings, seals, neoprene, cable trunking | Online / Ships from LA |
| **[Online Metals](https://www.onlinemetals.com)** | SS sheet, aluminum sheet/angle | Online |
| **[McNichols](https://www.mcnichols.com)** | Molded GRP (fiberglass) grating, FRP hold-down clips | Online / Multiple branches |
| **[Grating Pacific](https://gratingpacific.com)** | Molded FRP grating (vinyl-ester, grit top) | Los Angeles CA (SoCal) |
| **[Purcooflow](https://www.purcooflow.com)** | 3-stage combo filter units, replacement cartridges | Online |
| **[Grainger](https://www.grainger.com)** | Industrial supply — local branches throughout SoCal | Multiple SoCal branches |
| **[Lenox Laser](https://www.lenoxlaser.com)** | Custom precision laser-drilled pinholes | Glen Arm, MD |
| **[Hessaire](https://hessaire.com)** | 120V AC evaporative (swamp) coolers | Online |
| **[Victron / Amazon](https://www.victronenergy.com)** | Phoenix pure-sine inverters (Circuit E) | Online |
| **[Progressive Automations](https://www.progressiveautomations.com)** | Linear actuators (PA-14 series) | Online |
| **[Mouser Electronics](https://www.mouser.com)** | Power supplies, switches, electronic components | Online |

## See Also
- [Electrical & Systems Report](electrical-report.md) — full wiring specification, circuit fuse ratings, solar architecture
- [Chemistry Shopping List](chemistry-shopping-list.md) — detailed chemistry quantities for all alternative processes (gum bichromate, Van Dyke Brown, salt print)
- [Film Plane Mechanism Report](film-plane-mechanism-report.md) — engineering drawings for the 4-corner actuation system
- [Processing Water System](water-system-report.md) — three-circuit water system with filter skid design
- [Cost Breakdown](project-cost-breakdown.md) — full itemized build cost across three deployment scenarios
- [Funding Proposal](funding-proposal.md) — grant-ready budget summary at three funding levels
- [Operating Manual](operating-manual.md) — step-by-step single-operator workflow from chemistry prep to cleanup