<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# TBS-001 — Master Shopping List

**Camera:** The Big Shoebox Project — TBS-001  
**Basis:** April 2026. All prices USD. Prices marked † confirmed from supplier listings; others are close estimates.  
**Process assumed:** Cyanotype (lowest cost, no hazmat, no silver). See `chemistry-shopping-list.md` for alternative process costs.  
**Power assumed:** 12V DC off-grid solar + LiFePO4. See `electrical-report.md` for full architecture.

Items are grouped by build area. Source documents are cross-referenced in each section header.

---

## Summary — Estimated Total

| Area | Low | High |
|------|-----|------|
| 1. Container & delivery | $2,300 | $4,300 |
| 2. Interior conversion (light-seal, paint, backing) | $950 | $1,350 |
| 3. Pinhole optics plate | $95 | $240 |
| 4. Film plane mechanism (4-corner, manual) | $2,200 | $2,700 |
| 5. Print washing — water system | $2,661 | $4,020 |
| 6. Electrical — power, circuits, wiring | $1,785 | $1,890 |
| 7. Revolving drum light trap (custom fabrication) | $950 | $1,450 |
| 7a. Panel sliding carriage | $976 | $976 |
| 7b. Perimeter walkway (4 sections, wall-cantilevered) | $570 | $955 |
| 7c. Ceiling rail suspension | $208 | $208 |
| 8. Cooling & ventilation | $340 | $420 |
| 9. Printmaking chemistry — cyanotype, 50 prints | $2,500 | $3,200 |
| 10. Printmaking tools & consumables | $350 | $500 |
| 11. Safety & PPE | $120 | $180 |
| **TOTAL (base build + 50-print run)** | **~$16,120** | **~$21,710** |

*Optional additions: electric film plane actuation (+$827), lens plate (+$400–$1,500), self-haul transport (+$30,000–$40,000).*

---

## 1. Container & Delivery

*Source: `pinhole-camera-construction.md`, `project-cost-breakdown.md`*

| Item | Spec | Supplier | Est. cost |
|------|------|----------|-----------|
| 20ft ISO container — Cargo Worthy grade | CSC-certified, WWT minimum | Container Management / Local container dealers | $2,000–$3,500 |
| Delivery — short haul (<50 miles, tilt-bed) | Commercial hire | Local crane/tilt-bed truck hire | $300–$800 |
| Delivery — long haul (100–300 miles, semi flatbed) | If needed | Commercial freight broker | $1,200–$2,500 |

**Section total: $2,300–$4,300**

---

## 2. Interior Conversion

*Source: `pinhole-camera-construction.md`, `project-cost-breakdown.md`*

### Light-sealing

| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| D-profile foam weatherstripping, 1"×⅜" | Door perimeter seals | 50 ft | Home Depot / Lowe's | $0.50/ft | $25 |
| Black silicone sealant, 11 oz cartridge | Weld seam gaps, corner posts | 5 | Home Depot | $8† | $40 |
| 6-mil black polyethylene sheeting, 10'×100' | Interior lining over persistent seams | 1 roll | Home Depot / Uline | $65† | $65 |
| 2" black Gorilla Tape, 35 yd roll | Secondary sealing | 4 | Home Depot / Target | $12† | $48 |

**Light-seal subtotal: ~$178**

### Interior paint

| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| Flat black latex paint (zero sheen) | Two long walls, two short walls, ceiling (~755 sq ft) | 3 gal | Home Depot / Sherwin-Williams | $25 | $75 |
| Primer (bare steel areas) | One coat on new welds or repairs | 1 gal | Home Depot | $30 | $30 |
| Rollers, brushes, trays | — | 1 kit | Home Depot | $25 | $25 |

**Paint subtotal: ~$130**

### Image-plane flat backing

| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| Dibond ACM panel 4mm | 4'×8' sheets — flat backing surface | 6 | Grimco, City of Industry CA | $85† | $510 |
| Through-bolts + hardware | Into structural ribs every 18" | 1 lot | Fastenal / McMaster-Carr | $40 | $40 |

**Backing subtotal: ~$550**

### Door & access

| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| Door gasket set | OEM-style rubber seal for container cargo doors | 1 | Container parts suppliers | $45 | $45 |
| Miscellaneous hardware (fasteners, steel angle, touchup paint) | — | 1 lot | Home Depot | — | $110 |

**Section total: ~$1,000–$1,350**

---

## 3. Pinhole Optics Plate

*Source: `fabrication-drawings.md`, `pinhole-camera-construction.md`*

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Custom laser-drilled pinhole | Ø2.17mm ±0.025mm, SS-302 shim 3"×3", SEM-verified | 1 | Lenox Laser (lenoxlaser.com) | $50–$150 |
| Steel backing plate 6"×6"×⅛" + welded frame | Houses precision insert in wall plate | 1 | Metal Supermarkets SoCal | $20–$40 |
| Shutter plate ⅛" steel, 10"×8" + slide channel | Simple sliding shutter, exterior operation | 1 | Metal Supermarkets / fab | $25–$50 |

**Section total: $95–$240**

---

## 4. Film Plane Mechanism (4-Corner Independent)

*Source: `film-plane-mechanism-report.md`, `project-cost-breakdown.md`*

### Structural & rails

| Item | Spec | Qty | Supplier A | Supplier B | Est. unit |
|------|------|-----|-----------|-----------|-----------|
| Linear guide rail HGR20 | 2,200mm length | 4 | Automation Overstock, Gardena CA | McMaster-Carr #5901T777 | $45 |
| Rail carriage HGH20CA | Flanged block | 8 | Automation Overstock / Amazon | McMaster-Carr | $18 |
| Acme leadscrew ¾"-6 | 8ft length | 4 | Roton Products (LA area) | McMaster-Carr #6289K36 | $95 |
| Acme nut, bronze ¾"-6 | — | 4 | Roton Products | McMaster-Carr #6289K512 | $12 |
| Handwheel 8" dia | ¾" bore, cast aluminium | 4 | Grainger (Anaheim / LA / SD) | McMaster-Carr #6440K64 | $35 |
| Locking collar SS316 | ¾" bore | 4 | McMaster-Carr #6436K12 | Fastenal SoCal | $12 |
| Corner bracket L-plate | ¼" alum. plate, 6"×8" | 4 | Metal Supermarkets SoCal | Online Metals | $20 |
| Rod-end spherical bearing | GIR25-DO or equiv., 25mm bore | 8 | McMaster-Carr #60645K73 | Amazon Industrial | $22 |
| Pivot pin SS316 | 1" dia × 8" long | 8 | McMaster-Carr #98173A150 | Fastenal SoCal | $8 |

**Rails & structural subtotal: ~$1,260**

### Film plane frame & backing

| Item | Spec | Qty | Supplier A | Supplier B | Est. unit |
|------|------|-----|-----------|-----------|-----------|
| Aluminium angle 2"×2"×3/16" | 8ft lengths | 10 | Metal Supermarkets SoCal | Online Metals | $22 |
| Dibond ACM panel 4mm | 4'×8' sheets | 6 | Grimco, City of Industry CA | Signwarehouse | $85 |
| Black EPDM foam tape 1"×½" | 50ft rolls | 3 | McMaster-Carr #8614K84 | Grainger | $28 |
| Rosco Duvetyne blackout fabric | 60" wide, 10 yd | 1 | B&H Photo / Rosco direct | Rose Brand (rosebrand.com, Burbank CA) | $95 |
| Aluminium piano hinge 72" | 2" wide, 1/16" leaf | 2 | McMaster-Carr #1580A51 | Grainger | $28 |
| 6-mil black poly sheeting | 10'×100' roll | 1 | Home Depot | Uline | $65 |
| 2" black Gorilla Tape | 35 yd rolls | 6 | Home Depot / Target | Amazon | $12 |

**Frame subtotal: ~$1,102**

### Optional: electric actuation (add-on)

| Item | Spec | Qty | Supplier | Est. unit |
|------|------|-----|----------|-----------|
| PA-14 linear actuator | 12V, 20" stroke, 150 lb | 4 | Progressive Automations / Amazon | $185 |
| 12V 30A power supply | Enclosed | 1 | Mouser / Digi-Key | $55 |
| DPDT momentary rocker switch | Panel-mount, 20A | 4 | Mouser / Grainger | $8 |

**Electric actuation subtotal: ~$827 (optional)**

**Section total (manual): ~$2,362**

> **4-corner vs original 2-beam design delta:** Removed 2× 80/20 T-slot beams (5,893mm) — saves $416. Added: 2× extra leadscrews +$190, 2× extra handwheels +$70, 4× rod-end spherical bearings +$88, 4× corner L-brackets +$80. Net change: +$12 for significantly greater geometric capability. Excl. fabrication, fasteners, and optional electric actuation.

---

## 5. Print Washing — Water System

*Source: `water-system-report.md`*

### Water storage

| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| IBC tote 275 gal, food-grade, used/rinsed | HDPE cage, 2" ball valve — Blue (×2), Brown (×1), Waste (×1) | 4 | Container Exchanger (containerexchanger.com — CA listings) | $80–$150 | $320–$600 |
| 2" NPT bulkhead fitting, polypropylene | External drain/fill port on waste IBC | 2 | McMaster-Carr / Grainger | $18–$25 | $36–$50 |
| Reinforcing plate, 6mm A36 steel, 150×150mm | Backing plate for external bulkhead ports | 2 | Metal Supermarkets SoCal / Pacific Coast Steel | $8–$12 | $16–$24 |

**Storage subtotal: ~$372–$674**

### Pumps

| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| Shurflo 2088-554-144 pump | 12VDC, 3.5 GPM, 45 PSI, ½" NPSM ports | 2 | Amazon (Shurflo 2088) | $55–$70 | $110–$140 |
| SeaFlo pressure accumulator | 1 gal, 125 PSI, ½" NPT | 1 | Amazon (SeaFlo accumulator) | $25–$45 | $35 |
| Pump mounting bracket (stainless) | For 2088 series | 2 | Amazon | $8–$12 | $20 |

**Pump subtotal: ~$165–$195**

### Filter skid

| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| Big Blue filter housing 4.5"×10" | 1" NPT brass ports, pressure relief | 3 | Amazon (Geekpure Big Blue 10") / Bluonics | $28–$45 | $85–$135 |
| 50-micron sediment cartridge 4.5"×10" | Polypropylene depth filter | 4 + spares | Amazon (Pentair DGD-5005) | $8–$12 | $35–$50 |
| 5-micron sediment cartridge 4.5"×10" | PP wound/pleated | 4 + spares | Amazon (Pentair RFC-BB) | $10–$15 | $45–$60 |
| GAC carbon block 4.5"×10" | Granular activated carbon, 25-micron | 4 + spares | Amazon (Ronaqua Big Blue GAC) | $15–$22 | $65–$90 |
| Filter skid frame | 600×900mm slotted steel angle, DIY | 1 | Home Depot / Lowe's | $25–$40 | $35 |

**Filter subtotal: ~$265–$370**

### Valves, fittings & pipe

| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| Ball valve 1" FNPT, full-bore | Lever handle, HDPE-body or brass | 8 | Amazon / Home Depot / Ferguson Plumbing | $8–$14 | $65–$110 |
| 3-way diverter valve 1" FNPT | L-port or T-port | 2 | Amazon (1" 3-way ball valve) | $18–$30 | $40–$60 |
| 2" camlock fitting pairs M+F | Polypropylene | 6 pairs | Amazon / Grainger | $5–$8/pair | $35–$50 |
| 1" NPT elbows (HDPE) 90° | Street elbow | 12 | Home Depot / Ferguson | $3–$5 | $40–$60 |
| 1" NPT tees (HDPE) | Equal tee | 8 | Home Depot / Ferguson | $4–$6 | $35–$50 |
| 1" NPT unions | Maintenance disconnects | 6 | Ferguson / Amazon | $6–$10 | $40–$60 |
| PTFE thread seal tape | ½" wide, 260" roll | 4 | Home Depot | $2 | $8 |
| 1" SDR-11 HDPE pipe | Food-safe, blue-stripe, 20ft sticks | 5 sticks | Ferguson Plumbing / Winsupply | $12–$18/stick | $60–$90 |
| ¾" SDR-11 HDPE pipe | Spray bar run, 20ft sticks | 2 sticks | Ferguson / Winsupply | $9–$14/stick | $20–$30 |
| ½" ID reinforced braided PVC hose | Pump inlet flexible connection, 6ft per pump | 2 lengths | Home Depot / Amazon | $8–$12/length | $20 |
| 1" polypropylene camlock (Type E × Hose Barb) | Quick-disconnect at IBC and pipe stubs | 4 pairs | Amazon / Grainger | $5–$8/pair | $20–$32 |

**Valves, fittings & pipe subtotal: ~$383–$570**

### Processing tray

| Item | Spec | Qty | Supplier | Unit price | Est. cost |
|------|------|-----|----------|-----------|-----------|
| 304 SS sheet, 16-ga (1.5mm) | #4 brushed, 4'×8' sheets | 4 | Metal Supermarkets / Online Metals | $180–$250/sheet | $720–$1,000 |
| Fabrication (cut, brake, weld) | Two tray halves: 2,229×2,200mm, 50mm rims, 1:200 dual-axis fall | 1 job | Local sheet metal shop | $400–$800 | $400–$800 |
| 1" NPT SS bulkhead union | 304 SS, welded to tray floor at drain | 1 | McMaster-Carr / Grainger | $18–$30 | $25 |
| Silicone gasket strip, FDA grade | 1/16" × 1" × 10 ft, center flange seal | 1 roll | McMaster-Carr / Amazon | $15–$25 | $20 |
| M6×16 SS hex bolts + flange nuts | Center flange, 200mm spacing | 24 | McMaster-Carr / Bolt Depot | $0.50 each | $12 |

**Processing tray subtotal: ~$1,177–$1,857**

### Water system processing consumables

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| pH meter (waterproof) | 0–14, ±0.1 accuracy | 1 | Amazon (Apera PH20) | $35–$55 |
| pH calibration solution set | pH 4 + pH 7 buffer sachets | 1 set | Amazon | $10 |
| Citric acid, food grade, 5 lb | pH adjustment (acidifier) | 2 bags | Amazon / bulk food supplier | $28 |
| Chemical-resistant GHS labels | For IBC totes | 1 pack | Amazon / Labelmaster | $20 |
| Funnel with filter screen 2" | For IBC filling | 2 | Amazon / Grainger | $18 |

| Containment liner, 6-mil black LDPE | 20' × 10' sheet — secondary spill containment under IBCs and filter skid | 4 | Amazon / US Plastic Corp | $18–$28/sheet | $75–$110 |

**Water consumables subtotal: ~$205–$240**

**Section total: $2,661–$4,020**

---

## 6. Electrical — Power, Circuits & Wiring

*Source: `electrical-report.md`*

### Solar & battery (primary power)

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Solar panels, 200W monocrystalline | 12V nominal | 3 | Renogy (renogy.com) / Amazon | ~$400 total |
| MPPT charge controller | Victron SmartSolar MPPT 100/50 | 1 | altE Store (altestore.com) | ~$200 |
| LiFePO4 battery 100Ah 12V | Battle Born 100Ah or Renogy Smart Lithium | 2 | battleborncotteries.com / renogy.com | ~$700 total |
| Shore backup charger | Victron Blue Smart IP65 12/15 | 1 | altE Store | ~$150 |
| NEMA 5-15R inlet (weatherproof) | Mounted in flush-mount power panel | 1 | Leviton / Amazon | ~$25 |
| Solar panel ground mount frame | Tilt frame, 30° | 1 | Renogy / Amazon | ~$80 |
| PV cable 10 AWG | MC4 connectors | 1 lot | Amazon | ~$30 |
| Aluminum plate 340×240×3mm | Flush-mount face plate, power panel | 1 | McMaster-Carr / Online Metals | ~$18 |
| Neoprene gasket 340×240×3mm | Weatherseal between plate and wall | 1 | McMaster-Carr / Amazon | ~$6 |
| M6 bolt + nut + washer set | Panel mounting hardware, SS | 4 | McMaster-Carr / Home Depot | ~$5 |
| MC4 bulkhead connector pairs | IP67 panel-mount | 3 pairs | Amazon / Renogy | ~$25 |

**Solar & battery subtotal: ~$1,640**

### Distribution & wiring

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Blue Sea 5026 fuse block | 12-circuit ST-blade | 1 | West Marine Torrance CA / Amazon | ~$55 |
| 200A ANL main fuse + holder | Blue Sea ANL fuse block | 1 | Amazon | ~$30 |
| IP65 enclosure 300×200×130mm | Houses fuse block + MPPT | 1 | Polycase / Amazon | ~$60 |
| Wiring kit — 12/14/16/18 AWG | 50ft each colour, tinned copper | 1 kit | Amazon / Waytek Wire (waytekwire.com) | ~$80 |
| 2/0 AWG cable | Battery–fuse–busbar, 3ft | 1 lot | Amazon / Genuine Dealz | ~$30 |
| Anderson Powerpole connectors 30A | 50 pairs | 1 kit | Powerwerx (powerwerx.com) | ~$40 |
| Deutsch DT connectors 2-pin | Exterior penetrations, IP67 | 10 sets | Waytek Wire | ~$30 |
| 40×25mm PVC cable trunking | 5m lengths | 4 | Lowe's / McMaster-Carr | ~$40 |
| 10mm corrugated conduit (grey) | Drop conduits to devices | 10m | McMaster-Carr 7828K48 | ~$30 |
| Brady M210 wire label kit | Wire label cartridge | 1 | McMaster-Carr / Amazon | ~$80 |
| 12V LED flat panel, 300×600mm, 4000K | 20W neutral white, ceiling-mount | 3 | Amazon / superbrightleds.com | ~$75 total |
| Pull-cord ceiling switch, 12V 6A SPST | Inline switch for lighting Ccts D & G | 2 | Amazon / Lowe's | ~$16 total |
| Copper ground stake 8ft × ⅝" dia | Earth connection | 1 | Home Depot | ~$20 |
| 4 AWG ground wire, green/yellow | 3m | 1 | AutoZone / Amazon | ~$15 |

**Distribution & wiring subtotal: ~$600**

**Section total: ~$1,785–$1,890**  
*Note: water pump wiring now included in this section via main fuse block — remove the standalone 12V supply listed in older versions of the water system BOM.*

---

## 7. Revolving Drum Light Trap — Custom Fabrication

*Source: `light-trap-selection.md` § 3.3 & § 4. Custom-fabricated 750mm steel drum built into the hinged cargo-door panel. Replaces a fixed S-path vestibule; allows single-operator entry/exit at any time during operation without admitting daylight.*

### Drum body and baffles

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 3mm mild steel sheet, 1,200×2,400mm | Hot-rolled A36 — drum shell and internal baffles | 2 sheets | Pacific Coast Steel — Santa Fe Springs CA | ~$80/sheet → ~$160 |
| 5mm steel plate (offcut) | Top and bottom drum caps, flanged | ~0.5m² | Pacific Coast Steel / Metal Supermarkets SoCal | ~$40 |
| 75mm Ø solid round bar, cut to 150mm | Upper and lower stub shafts (×2) | 2 pieces | Pacific Coast Steel or any steel service centre | ~$30 |

### Bearings

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| SKF 6215-2RS1 sealed deep-groove ball bearing | 75mm ID × 130mm OD × 25mm wide, C3 clearance | 2 | Bearing World — Anaheim CA; or Applied Industrial Technologies | ~$45–$65 each → ~$90–$130 |
| Circlip for 75mm shaft | DIN 471, shaft circlip | 4 | McMaster-Carr #98541A113 | ~$10 |

### Seals

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 12mm closed-cell neoprene wiper strip, PSA-backed | Top and bottom drum cap wiper seals; 3m total | 1 pack (3m) | McMaster-Carr #93855K6 | ~$22 |
| 20mm neoprene compression strip, PSA-backed | Drum-to-panel gap seal, bonded to panel aperture surround | 2.4m | McMaster-Carr #8635K31 or equivalent | ~$20 |
| Black UV-stable silicone sealant | Bead seal at top and bottom mount plates | 2 tubes | McMaster-Carr #7587A3 or equivalent | ~$18 |

### Hardware

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| SS round grab rail, 100mm Ø × 400mm | Interior face only, welded bracket — no through-hole in drum wall | 1 | McMaster-Carr #4530T37 (cut to length) | ~$20 |
| M10 × 40mm hex bolt, stainless + flat washer | Lower bearing collar — 8 off into panel bottom rail | 1 lot | McMaster-Carr / Fastenal | ~$20 |
| M10 × 35mm hex bolt, stainless + flat washer | Upper bearing housing — 6 off into panel top rail | 1 lot | McMaster-Carr / Fastenal | ~$15 |

### Surface treatment

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Flat black powder coat — interior drum surfaces | RAL 9005 matte; shot-blast prep + coat | 1 job | Local powder coat shop (SoCal) | ~$120–$180 |
| Grey oxide primer + grey topcoat — exterior drum face | Standard exterior steel finish | 1 job | Included with powder coat job above, or rattle-can | ~$0–$30 |

### Fabrication labour

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Metal fabrication — drum rolling, seam weld, baffle welding, cap welding, stub shaft welding | 16–20 hrs at local metal fab shop | 1 job | Local fabrication shop (SoCal) — get 2–3 quotes | ~$800–$1,200 |

**Section total: ~$950–$1,450**

*Note: This is for the drum body only. The hinged panel that the drum mounts into (50×50mm RHS frame, 18mm ply skins, EPDM perimeter gasket) is covered in § 2 (Interior Conversion) above. See [light-trap-selection.md](light-trap-selection.md) for full specification and supplier notes.*

---

## 7a. Panel Sliding Carriage

*Source: `equipment-layout-report.md` § 6.1. Enables transport mode: panel slides inward 300mm, clearing container doors for closure. Single-person operation (~5 min, panel slide only).*

### Panel slide system

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| HGR20 linear rail, 500mm | Both walls, floor + ceiling, X-direction | 4 | Automation Overstock, Gardena CA / Amazon | ~$88 |
| HGH20CA carriage blocks | Flanged, 2 per rail | 8 | Automation Overstock / Amazon | ~$144 |
| Carriage beam, 60×60×3mm SHS | 2,400mm tall, mild steel | 1 | Pacific Coast Steel / Metal Supermarkets | ~$35 |
| Hinge mounting plates, 6mm steel | 220×80mm | 3 | Local fab | ~$30 |
| Rail mounting brackets, 8mm angle | Both walls, floor + ceiling | 8 | Local fab | ~$64 |
| Destaco 207-U toggle clamps | 2 per position × 2 positions | 4 | McMaster-Carr / Grainger | ~$100 |
| Strike pins, 16mm hardened dowel | Pressed into carriage base | 4 | McMaster-Carr | ~$12 |

**Panel slide subtotal: ~$473**

### Fixed door frame + seals

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 50×50×3mm RHS welded frame | Full door perimeter ~9.5m | 1 | Pacific Coast Steel / Metal Supermarkets | ~$120 |
| Seal landing machining | Mill flat on all frame faces | 1 | Local fab | ~$80 |
| Brush seal strip (doubled nylon bristle) | Left carriage beam slot, 2,400mm × 2 layers | 2 | McMaster-Carr | ~$50 |
| Brush seal strip (doubled nylon bristle) | Right guide slot, 2,400mm × 2 layers | 2 | McMaster-Carr | ~$50 |
| EPDM gasket (existing spec) | 20×15mm, ~9.5m | 1 | McMaster-Carr #8635K31 | ~$45 |
| Neoprene backup strip, 10×10mm | Self-adhesive, ~9.5m | 1 | McMaster-Carr | ~$22 |
| Neoprene rail channel pads, 10mm | 50×30mm, closed-cell, 4 rail penetrations | 4 | McMaster-Carr | ~$8 |
| EPDM edge strips, 15mm | Self-adhesive, 2,400mm × 2 sides, panel edge clearance seal | 2 | McMaster-Carr | ~$18 |
| Fasteners, misc | M10/M12 stainless, assorted | 1 lot | McMaster-Carr / Fastenal | ~$60 |
| Flat black paint | Touch-up, 1 qt | 1 | Home Depot | ~$15 |
| Fan B flex cable (coiled, 16AWG 2-cond, silicone) | 1m coiled, Deutsch DT 2-pin connectors each end | 1 | Waytek Wire / McMaster-Carr | ~$35 |

**Door frame subtotal: ~$503**

**Section total (materials): ~$976**
**Fabrication labor: ~12–16 hrs × $80–$100/hr = $960–$1,600**

---

## 7b. Perimeter Walkway

*Source: `generate_walkway_diagram.py`, `engineering-diagrams.md` §14. Four removable grated walkway sections around the processing tray. Wall-cantilevered bracket design (rev 9): near/far walkways bracket to corrugated wall ribs, right walkway brackets to angle iron on flat end wall, left walkway is a removable lift-out (panel conflict — no brackets). No legs, no beam, no floor contact — entire tray interior completely clear for film loading. Deck height 100mm (75mm bracket arm + 25mm grate).*

### Walkway sections (4 off)

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Press-locked steel grating, 25mm (30×3mm bars) | Galvanized, 30mm pitch. Cut to size: 2× 4,459×300mm (near/far), 1× 2,362×300mm (right), 1× 2,362×300mm (left — removable lift-out) | ~4.1 m² | McNichols / Metal Supermarkets SoCal | ~$260–$390 |
| Wall brackets, 8mm steel plate gusset | Triangular gusset: 150mm vertical leg × 300mm horizontal arm, diagonal brace welded. Hot-dip galvanized. | 25 | Local fab / Metal Supermarkets SoCal | ~$200–$300 |
| Angle iron mounting rail, 50×50×5mm L-angle | Mild steel, hot-dip galvanized. Welded horizontally along right end wall interior. 1× 2,362mm length. | 1 | Metal Supermarkets / Pacific Coast Steel | ~$15–$25 |
| Reinforcing plates, 80×180×6mm mild steel | Welded to exterior wall face behind each bracket position (near/far walls only) | 20 | Metal Supermarkets / Pacific Coast Steel | ~$40–$60 |
| M12×60mm hex bolts, nuts, flat washers | Grade 8.8, galvanized. 2 per bracket through wall rib + reinforcing plate. | 50 | McMaster-Carr / Bolt Depot | ~$50–$75 |
| Grating clips | Slide-on clips to secure grating to bracket arms — removable without tools | 35 | McNichols / McMaster-Carr | ~$15–$25 |
| Fabrication + installation | Cut/weld/galvanize 25 brackets, weld angle iron + reinforcing plates, drill wall ribs, install | 1 job | Local fab / metal shop | ~$250–$400 |

**Walkway subtotal: ~$570–$955**

*Near/far/right grating lifts onto bracket arms and clips in place. Left walkway is a lift-out section resting on near/far butt joint ends — must be removed before sliding the hinged panel to transport position. Left corners use butt joints (no miter) so near/far walkways clear the panel envelope. No floor contact — entire tray interior clear.*

---

## 7c. Ceiling Rail Suspension

*Source: `generate_ceiling_rail_diagram.py`, `engineering-diagrams.md` §13. HGR20 ceiling-mounted linear rails suspend the hinged panel with 80mm floor gap, clearing the 50mm processing tray rim during transport slide.*

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| HGR20 linear rail, 500mm | Ceiling-mounted, both walls, X-direction | 2 | Automation Overstock, Gardena CA / Amazon | ~$44 |
| HGH20CA carriage blocks | Flanged, 2 per rail | 4 | Automation Overstock / Amazon | ~$72 |
| Ceiling mounting brackets, 8mm angle | Welded to container ceiling ribs | 4 | Local fab | ~$32 |
| Drop rod / hanging bracket, 6mm steel | Connects carriage block to panel top rail | 4 | Local fab | ~$40 |
| Fasteners, misc | M10 stainless | 1 lot | McMaster-Carr / Fastenal | ~$20 |

**Ceiling rail subtotal: ~$208**

*Note: The panel sliding carriage (§7a) uses 4 rails at floor + ceiling on both walls. This section covers the 2 additional ceiling rails that provide panel suspension and floor gap clearance.*

---

## 8. Cooling & Ventilation

*Source: `electrical-report.md`*

### Ventilation fans (upgrade from original 4" spec)

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 6" (150mm) inline DC fan | 12V, ~200 CFM (e.g. AC Infinity S6) | 2 | Amazon (AC Infinity) | ~$120 total |
| 6" duct stub fittings | Wall penetration collars | 2 | Amazon / HVAC supply | ~$20 |
| Fan baffle plates (3mm mild steel) | 2 baffles per fan, offset S-path | 1 lot | Metal Supermarkets SoCal / cut-to-size | ~$40 |

**Ventilation subtotal: ~$180**

### Shade canopy

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 80% shade cloth 20×10ft | UV-stabilised, over container roof | 1 | Amazon / Farm supply | ~$80 |
| Canopy frame | 1.5" EMT conduit + T-fittings | 1 lot | Home Depot | ~$120 |

**Shade canopy subtotal: ~$200**

### Evaporative cooler

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 12V DC evaporative cooler | ~80W, ~300 CFM (e.g. Portacool Jetstream 110 12V) | 1 | Portacool / Amazon | ~$280 |
| 150mm duct collar + baffles (cooler intake) | Light-safe baffled intake through bottom wall | 1 lot | McMaster-Carr / metal fab | ~$30 |

**Cooler subtotal: ~$310**

**Section total: ~$690**  
*Note: fans wired to Circuits A & B, cooler to Circuit E — all from main fuse block. No separate power supply required.*

---

## 9. Printmaking Chemistry — Cyanotype (50 prints)

*Source: `chemistry-shopping-list.md`*

**Recommended process.** No silver, no DEA registration, no hazmat shipping, development in plain cold water.

### Chemistry

| Item | Per print | × 50 prints | Supplier | Unit | Units | Unit price | Total |
|------|-----------|-------------|---------|------|-------|-----------|-------|
| Ferric ammonium citrate (FAC), green grade, 1 lb | 224g | 11.2 kg | Photographers' Formulary (stores.photoformulary.com) | 454g (1 lb) | 27 | ~$30† | ~$810 |
| Potassium ferricyanide, 1 kg | 91g | 4.55 kg | Bostick & Sullivan (bostick-sullivan.com) | 1,000g | 5 | $24.29† | $121 |
| Distilled water | ~2 L | ~100 L | Tap water + DI filter adequate | — | — | — | ~$0 |

> **FAC note:** Order green grade only (Fe³⁺). Brown grade (Fe²⁺) is not light-sensitive for cyanotype. Photographers' Formulary and Bostick & Sullivan both specify green grade.

**Chemistry subtotal: ~$931**

### Substrate

| Item | Qty | Supplier | Unit | Units | Unit price | Total |
|------|-----|---------|------|-------|-----------|-------|
| Unbleached cotton muslin, 60" wide | 1,650 linear yards | Fabric Direct (fabricdirect.com) | 150-yd roll | 11 | ~$100 | ~$1,100 |
| OR unbleached cotton muslin by the yard | 1,650 yd | Fabric Wholesale Direct (fabricwholesaledirect.com) | per yard | 1,650 | $0.80–$1.20/yd | $1,320–$1,980 |

> **Muslin note:** Pre-wash all fabric twice in hot water, no detergent, to remove sizing. Sizing repels water-based sensitisers. 60" width requires 5 strips per print — or source 120" (theatrical/backdrop) width to eliminate vertical seams.

**Substrate subtotal: ~$1,100**

**Section total: ~$2,031–$2,842** (per 50-print run, ~$57/print)

---

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
| Cam-lever spring clamps | Muslin attachment — over-center cam, neoprene jaw, ~5N | 92 | McMaster-Carr (Destaco equiv.) / Amazon (generic toggle) | ~$3-8 ea |
| M5×16 SS socket head bolt + Nylock nut | Clamp base plate mounting (2 per clamp) | 184 + 184 | McMaster-Carr #91292A128 / Bolt Depot | ~$55 |
| Neoprene strip 60A, 35mm × 6mm | Jaw pads (self-adhesive, cut to 35×12mm) | 1 roll (10m) | McMaster-Carr #8614K44 / Grainger | ~$15 |
| Spray bottle (1 litre) | Humidity/misting in low-RH conditions | 2 | Amazon / garden supply | ~$15 |
| pH test strips | Quick wash water check | 1 pack | Amazon | ~$10 |
| 6-mil black poly sheeting, 10'×100' | Container floor protection during development | 1 roll | Home Depot / Uline | ~$80 |

**Section total: ~$650–1,100** (range depends on generic vs Destaco-equivalent clamps)

---

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

---

## Supplier Directory

| Supplier | Category | URL / Location |
|---------|---------|----------------|
| **Photographers' Formulary** | FAC, potassium ferricyanide, darkroom chemicals | stores.photoformulary.com |
| **Bostick & Sullivan** | Cyanotype, VDB, platinum/palladium chemistry | bostick-sullivan.com |
| **Fabric Direct** | Unbleached cotton muslin, 150-yd rolls | fabricdirect.com |
| **Fabric Wholesale Direct** | Unbleached muslin by yard or bolt | fabricwholesaledirect.com |
| **Rose Brand** | Rosco Duvetyne blackout fabric | rosebrand.com · Burbank CA |
| **Metal Supermarkets** | Steel, aluminium, cut-to-length | Anaheim · Van Nuys · San Diego |
| **Grimco** | Dibond ACM panels (sign industry) | grimco.com · City of Industry CA |
| **Automation Overstock** | Linear guides, carriages, surplus motion components | Gardena CA (walk-in) |
| **Roton Products** | Acme leadscrews and nuts, cut to length | roton.com · ships from LA area |
| **Renogy** | Solar panels, MPPT controllers, LiFePO4 batteries | renogy.com |
| **altE Store** | Victron MPPT, Victron chargers, off-grid power | altestore.com |
| **Battle Born Batteries** | 100Ah LiFePO4 12V | battleborncotteries.com |
| **Powerwerx** | Anderson Powerpole connectors and tools | powerwerx.com |
| **Waytek Wire** | Deutsch DT connectors, automotive wire | waytekwire.com |
| **West Marine** | Blue Sea fuse blocks, marine DC wiring (Torrance CA) | westmarine.com |
| **Container Exchanger** | Used IBC totes, food-grade — CA listings | containerexchanger.com |
| **BASCO USA** | HDPE drums, containers, UN-rated | bascousa.com |
| **Ferguson Plumbing** | HDPE pipe, valves, fittings | ferguson.com |
| **Pacific Coast Steel** | Hot-rolled A36 sheet, round bar, structural steel | Santa Fe Springs CA |
| **Bearing World** | SKF bearings, same-day availability | Anaheim CA |
| **Applied Industrial Technologies** | SKF bearings, industrial supply | Multiple SoCal branches |
| **McMaster-Carr** | Fasteners, bearings, cable trunking, seals, neoprene strip | mcmaster.com |
| **Grainger** | Industrial supply — local branches throughout SoCal | grainger.com |
| **Lenox Laser** | Custom precision laser-drilled pinholes | lenoxlaser.com |
| **Portacool** | 12V DC evaporative coolers | portacool.com |
| **AC Infinity** | 6" inline DC fans (S6 series) | acinfinity.com / Amazon |

---

## See Also

- [Electrical & Systems Report](electrical-report.md) — full wiring specification, circuit fuse ratings, solar architecture
- [Chemistry Shopping List](chemistry-shopping-list.md) — detailed chemistry quantities for all alternative processes (gum bichromate, Van Dyke Brown, salt print)
- [Film Plane Mechanism Report](film-plane-mechanism-report.md) — engineering drawings for the 4-corner actuation system
- [Processing Water System](water-system-report.md) — three-circuit water system with filter skid design
- [Cost Breakdown](project-cost-breakdown.md) — full itemised build cost across three deployment scenarios
- [Operating Manual](operating-manual.md) — step-by-step single-operator workflow from chemistry prep to cleanup
