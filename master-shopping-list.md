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
| 2. Interior conversion (light-seal, paint, ventilation) | $526 | $693 |
| 3. Pinhole optics plate | $100 | $215 |
| 4. Film plane mechanism (4-corner U-channel + acetal skate + 304 cross-slide + U-joint, incl. wall-seat saddles) | $4,271 | $4,673 |
| 5. Print washing — water system (incl. IBC stacking frame) | $6,708 | $7,955 |
| 6. Electrical — power, circuits, wiring | $3,431 | $3,496 |
| 7. Housed revolving-door light lock (plastic-skin custom fabrication) | $2,046 | $2,516 |
| 7a. Panel swing pivot + fixed door frame (Ø89 post + bearings + cage + wall stays + rail saddles + door frame) | $1,180 | $1,610 |
| 7b. Perimeter walkway (4 sections + drum-exit punch-out) | $2,086 | $2,948 |
| 7c. Hinged panel structure (stepped frame + HDPE skins + Al core + EPDM + cam latches + B2 bay + pull handle) | $1,278 | $1,484 |
| 7d. Chemistry prep shelf (fold-down board + steel frame + hinge/stays + TAP-01 trunk extension) | $223 | $235 |
| 8. Cooling & ventilation | $748 | $898 |
| 9. Printmaking chemistry — cyanotype, 50 prints (Low = Lean, High = Rich tier) | $1,250 | $3,100 |
| 10. Printmaking tools & consumables | $350 | $500 |
| 11. Safety & PPE | $120 | $180 |
| **TOTAL (base build + 50-print run)** | **~$26,617** | **~$34,803** |
<!-- END costing:master-summary -->

*Optional additions: electric film plane actuation (+$827), lens plate (+$400–$1,500), self-haul transport (+$30,000–$40,000).*

*Line 9 (printmaking chemistry) is the **Mike Ware New Cyanotype** recipe (ferric ammonium oxalate sensitizer) with the corrected ~$300 substrate, re-summed into the TOTAL: **Low = Lean ⅓-Ware (~$1,250), High = Rich full-Ware (~$3,100)**, working default Standard ½-Ware (~$1,710). The tier is pinned by the [Sensitizer Trials](sensitizer-trials.md); the TOTAL spans that Lean–Rich range ($1,250–$3,100), narrowing once a tier is locked.*

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
| [2" black Gorilla Tape](https://www.homedepot.com/p/316372144) (106718) | 6 roll | Home Depot | film | $60 |
| [Dielectric grease, marine-grade (terminal protection)](https://www.amazon.com/dp/B0D6R543V2) (B0D6R543V2) | 1 ea | Amazon | electrical | $9 |
| Door perimeter weatherstrip + threshold | 1 lot | Home Depot | interior | $10–$22 |
| Flat black epoxy spray paint | 1 can | Hardware store | shelf | $12 |
| Flat black paint (RAL 9005) | 1 qt | Local fab | panel | $10–$20 |
| GRP grating edge-seal kit | 1 kit | Fibergrate | walkway | $40–$60 |
| [Interior matte-black paint](https://www.homedepot.com/p/316173659) (PR31301) | 5 gal | Home Depot | interior | $125 |
| [Loctite PL Premium construction adhesive](https://www.homedepot.com/p/319654545) (1390595) | 2 tube | Home Depot | tray | $12 |
| Matte-black interior finish | 1 ea | Local fab | lightlock | $40–$70 |
| Primer + paint | 1 lot | Hardware store | ibc-frame | $30–$50 |
| [Silicone bead sealant (black, UV-stable)](https://www.homedepot.com/p/331895623) (RDX1001bl) | 1 ea | Home Depot | lightlock | $20 |
| Thread seal tape (PTFE) | 4 roll | Home Depot | water | $8 |
| **adhesives-finishes subtotal** | | | | **$375–$467** |

### aluminum

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [1"×1"×1/8" Al angle, 8 ft — corner-zone stiffener grid](https://www.grainger.com/product/2EYP1) (2EYP1) | 4 ea | Grainger | panel | $49 |
| [6061-T6 AL plate 3/16" (5mm)](https://www.metalsupermarkets.com/product/aluminum-sheet-6061/) (6061-sheet-12x20x0.1875) | 1 ea | Metal Supermarkets | spray | $125 |
| [6061-T6 AL round tube 25mm OD × 2mm wall, 8 ft](https://www.mcmaster.com/9056K36-9056K122/) (9056K36) | 1 ea | McMaster-Carr | spray | $64 |
| [6061-T6 Al U-channel depth rail 3×1½"×0.2" (76×38mm), 8 ft](https://www.grainger.com/product/795M51) (795M51) | 4 ea | Grainger | film | $328 |
| [Aluminum angle 2"×2"×1/8" (6061-T6, plain) — 16 ft lengths](https://www.onlinemetals.com/en/buy/aluminum/2-x-2-x-0-125-aluminum-angle-6061-t6/pid/987) | 3 16 ft length | Metal Supermarkets | film | $528 |
| Aluminum U-channel, 1/8-panel (per meter) | 40 m | Online Metals | panel | $120–$200 |
| Arm-to-stud adapter, turned 6061-T6 AL (anodized) | 1 ea | Local machine shop | spray | $12–$18 |
| Disc retaining ring (Al 6061-T6, M52×0.75) | 1 ea | Local fab | optics | $15–$25 |
| [Telescoping aluminum pool pole, 4–8 ft](https://www.amazon.com/dp/B0FHPSPD4T) (B0FHPSPD4T) | 1 ea | Amazon | spray | $15 |
| **aluminum subtotal** | | | | **$1,256–$1,352** |

### bearings-motion

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [1-1/4" OD acetal load rollers — Delrin rod (cut ×8)](https://www.mcmaster.com/8576K23-8576K232/) (8576K23) | 1 1 ft rod | McMaster-Carr | film | $11 |
| [3/4" OD acetal keeper rollers — Delrin rod (cut ×8)](https://www.mcmaster.com/8497K276-8497K273/) (8497K276) | 1 4 ft rod | McMaster-Carr | film | $15 |
| [Acetal roller wheels ×4 (Delrin rod stock, Ø32×20, Ø10 bore)](https://www.mcmaster.com/8576K23/) (8576K23) | 1 1 ft rod | McMaster-Carr | spray | $11 |
| [Belden SSNBUJ750x3/8KB needle-bearing U-joint (3/8" keyway bore, 45deg, SS, booted)](https://www.grainger.com/product/BELDEN-Universal-Joint-Stainless-41D816) (41D816) | 4 ea | Grainger | film | $1,009 |
| [iglide J flange bushing, Ø90 bore (JFM-9095-100)](https://www.igus.com/iglide-ibh/flange-bearings/product-details/iglide-j-m?artnr=JFM-9095-100) (JFM-9095-100) | 2 ea | igus | swing | $261 |
| [M12 rod-end bearing (uxcell SA12TK, 4-pack)](https://www.amazon.com/uxcell-SA12TK-Bearing-M12x1-75-Self-Lubricating/dp/B0C7N16RQ9) (B0C7N16RQ9) | 1 4-pack | Amazon | spray | $20 |
| [McMaster 4040N12 304 shaft support](https://www.mcmaster.com/4040N12/) (4040N12) | 4 ea | McMaster-Carr | film | $232 |
| [SKF 6215-2RS1 sealed bearing](https://bearingsdirect.com/6215-2rs-ball-bearing-75x130x25-sealed-6215-2nse/) (6215-2RS) | 2 ea | Bearings Direct | lightlock | $121 |
| [Thrust ball bearing, 51118 (Ø90 bore, single-direction)](https://bearingsdirect.com/51118-thrust-ball-bearing-90x120x22-grooved-ubc-usbc/) (51118) | 1 ea | Bearings Direct | swing | $80 |
| **bearings-motion subtotal** | | | | **$1,759** |

### chemistry-reagents

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [Ammonium dichromate](https://artcraftchemicals.com/products/ammonium-bi-dichromate-part-1022) | 1 run | Artcraft Chemicals | chemistry | $25 |
| [Ferric ammonium oxalate (AmFe)](https://artcraftchemicals.com/products/ferric-ammonium-oxalate-part-1684?variant=42896857825527) | 17.1 kg | Artcraft Chemicals | chemistry | $1,098 |
| [Potassium ferricyanide](https://artcraftchemicals.com/products/potassium-ferricyanide-part-1275) | 5.7 kg | Artcraft Chemicals | chemistry | $291 |
| **chemistry-reagents subtotal** | | | | **$1,414** |

### container

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 20 ft ISO container — CW (cargo-worthy) grade | 1 ea | containermgt.com | container | $2,000–$3,500 |
| **container subtotal** | | | | **$2,000–$3,500** |

### ducting-ventilation

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [150×150×50mm axial fans (12V DC)](https://www.amazon.com/dp/B091BTFBD9) (B091BTFBD9) | 2 ea | Amazon | ventilation | $50 |
| [200mm 90° duct elbow](https://www.homedepot.com/p/100187427) (MF-90E8) | 1 ea | Home Depot | ventilation | $15 |
| [200mm insulated flex duct](https://www.homedepot.com/p/314398619) (23-183-08-25) | 1 coil | Home Depot | ventilation | $63 |
| [Duct collar + hose clamp](https://www.homedepot.com/p/100211540) (DSCF8) | 1 set | Home Depot | ventilation | $16 |
| [Evaporative cooler](https://www.homedepot.com/p/321429692) (MC18MT) | 1 ea | Home Depot | ventilation | $109 |
| Ventilation (inline fans + light-trap baffles) — interior-conversion allowance | 1 lot | Amazon | interior | $80–$130 |
| [Weatherproof duct cap](https://www.homedepot.com/p/100396923) (8DC) | 1 ea | Home Depot | ventilation | $12 |
| **ducting-ventilation subtotal** | | | | **$345–$395** |

### electrical-distribution

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [10mm split corrugated wire loom, drop runs](https://www.amazon.com/Split-Wire-Loom-Tubing-Polyethylene/dp/B017L3GWIW) (B017L3GWIW) | 10 m | Amazon | electrical | $25 |
| [12 AWG tinned hook-up wire, black — 100ft (Circuit F)](https://www.waytekwire.com/product/wrt12-0-hook-up-wire-tinned-copper) (WRT12-0) | 1 spool | Waytek Wire | electrical | $13 |
| [12 AWG tinned hook-up wire, red — 100ft (Circuit F)](https://www.waytekwire.com/product/wrt12-2-hook-up-wire-tinned-copper) (WRT12-2) | 1 spool | Waytek Wire | electrical | $13 |
| [14 AWG duplex marine wire](https://www.waytekwire.com/product/multi-conductor-marine-cable-mcb14-2) (MCB14-2) | 25 ft | Waytek Wire | water | $17 |
| [14 AWG tinned hook-up wire, black — 100ft (Circuit C feed / AC)](https://www.waytekwire.com/product/wrt14-0-hook-up-wire-tinned-copper) (WRT14-0) | 1 spool | Waytek Wire | electrical | $14 |
| [14 AWG tinned hook-up wire, red — 100ft (Circuit C feed / AC)](https://www.waytekwire.com/product/wrt14-2-hook-up-wire-tinned-copper) (WRT14-2) | 1 spool | Waytek Wire | electrical | $14 |
| [15A blade fuse](https://www.amazon.com/dp/B07WP5FWJJ) (B07WP5FWJJ) | 1 pack | Amazon | water | $8 |
| [16 AWG coiled (retractile) cable, 2-cond](https://www.amazon.com/dp/B0GYFNXM9Z) (B0GYFNXM9Z) | 1 ea | Amazon | ventilation | $26 |
| [16 AWG tinned hook-up wire, black — 100ft (Circuits A/B/G + branches)](https://www.waytekwire.com/product/wrt16-0-hook-up-wire-tinned-copper) (WRT16-0) | 1 spool | Waytek Wire | electrical | $16 |
| [16 AWG tinned hook-up wire, red — 100ft (Circuits A/B/G + branches)](https://www.waytekwire.com/product/wrt16-2-hook-up-wire-tinned-copper) (WRT16-2) | 1 spool | Waytek Wire | electrical | $16 |
| [18 AWG tinned hook-up wire, black — 100ft (Circuit D + E-stop)](https://www.waytekwire.com/product/wqt18-0-hook-up-wire-tinned-copper) (WQT18-0) | 1 spool | Waytek Wire | electrical | $12 |
| [18 AWG tinned hook-up wire, red — 100ft (Circuit D + E-stop)](https://www.waytekwire.com/product/wqt18-2-hook-up-wire-tinned-copper) (WQT18-2) | 1 spool | Waytek Wire | electrical | $12 |
| [2/0 AWG battery cable, 3ft (battery–fuse–busbar)](https://www.amazon.com/dp/B0B3HD7CWP) (B0B3HD7CWP) | 1 lot | Amazon | electrical | $26 |
| [200A main fuse (Blue Sea 5187) + single MRBF holder (5191)](https://defender.com/en_us/blue-sea-systems-single-mrbf-terminal-fuse-block-5191) (5187+5191) | 1 ea | Blue Sea | electrical | $46 |
| [4 AWG ground wire, green/yellow, 20ft](https://www.automationdirect.com/adc/shopping/catalog/bulk_wire_-a-_cable/single_conductor_wire_-a-_cable/mtw4gyl-1) (MTW4GYL-1) | 1 lot | AutomationDirect | electrical | $52 |
| [40×25mm PVC cable trunking, 5m](https://www.amazon.com/GenSDH-Raceway-Speaker-Concealer-Coffee-Width/dp/B0DK6GMHGL) (B0DK6GMHGL) | 4 ea | Amazon | electrical | $74 |
| [Anderson Powerpole 30A connectors, 50 pairs (unassembled)](https://powerwerx.com/1327bk-anderson-powerpole-housing-red) (1327) | 1 kit | Powerwerx | electrical | $55 |
| [Anderson Powerpole connectors 30A](https://powerwerx.com/anderson-powerpole-connectors-30amp-unassembled) | 5 pair | Powerwerx | water | $6 |
| [Battery main disconnect — Blue Sea 6006 m-Series (300A)](https://offgridstores.com/products/blue-sea-6006-m-series-mini-battery-switch-single-circuit-on-off-red) (6006) | 1 ea | Off Grid Stores | electrical | $36 |
| [Battery terminal covers (pair), insulating boots](https://www.waytekwire.com/product/23501-straight-in-battery) (23501) | 1 pair | Waytek Wire | electrical | $3 |
| [Blue Sea 5026 fuse block, 12-circuit ST-blade](https://offgridstores.com/products/blue-sea-5026-st-blade-fuse-block-w-cover-12-circuit-w-negative-bus) (5026) | 1 ea | Off Grid Stores | electrical | $59 |
| [Brady M210 wire label printer kit](https://www.digikey.com/en/products/detail/brady-corporation/M210-KIT/16643735) (M210-KIT) | 1 ea | Amazon | electrical | $194 |
| [Cable grommets / glands — steel-shell penetrations](https://www.amazon.com/YUFANNET-Assortment-Grommets-Automotive-Electrical/dp/B09K5GNFHF) (B09K5GNFHF) | 1 lot | Amazon | electrical | $28 |
| [Cooler AC outlet — WR duplex receptacle + in-use cover](https://www.homedepot.com/p/202078774) (W5320-T0W) | 1 set | Home Depot | electrical | $25 |
| Cooler external power cable | 1 ea | Waytek Wire | ventilation | $20 |
| [Copper-bonded ground rod, 8ft × ⅝" + acorn clamp](https://www.homedepot.com/p/ERICO-5-8-in-x-8-ft-Copper-Ground-Rod-615880UPC/202195738) (615880UPC) | 1 lot | Home Depot | electrical | $27 |
| [Deutsch DT 2-pin connectors (Amphenol AT2PS-CKIT)](https://www.waytekwire.com/product/amphenol-sine-systems-at2ps-ckit-2-pin) (AT2PS-CKIT) | 2 set | Waytek Wire | ventilation | $8 |
| [Deutsch DT 2-pin connectors, IP67 (exterior penetrations)](https://www.waytekwire.com/product/amphenol-sine-systems-at2ps-ckit-2-pin) (AT2PS-CKIT) | 10 set | Waytek Wire | electrical | $30 |
| [Equipotential bonding kit — 6 AWG jumper + ring lugs](https://www.grainger.com/product/PANDUIT-Grounding-Jumper-Wire-Kit-21WJ56) (21WJ56) | 1 ea | Grainger | electrical | $96 |
| [External emergency cut-off — red mushroom switch](https://www.harfington.com/products/p-1071142) (a19061100ux1510) | 1 ea | Harfington | electrical | $13 |
| [HitLights 12V COB LED strip 4000K, 16.4ft reel (Circuit G, ×2)](https://hitlights.com/products/premium-12v-cob-led-strip-light-single-color-ul-listed-16-4ft-ip-20-white-pcb) (L2712V-40D3-1630-U) | 2 reel | HitLights | electrical | $75–$85 |
| [Interior emergency cut-off — red mushroom switch (paralleled to exterior)](https://www.harfington.com/products/p-1071142) (a19061100ux1510) | 1 ea | Harfington | electrical | $13 |
| [IP65 enclosure 213×213×133mm (fuse block + busbars, on the plywood)](https://www.polycase.com/zh-080804) (ZH-080804) | 1 ea | Polycase | electrical | $47 |
| [LED Profiles 981 slimline channel + diffuser, 8 ft (×6)](https://ledprofiles.com/collections/all-led-channels/products/slimline-ultra-low-profile-led-channel-981-series) (981ASL) | 6 8ft length | LED Profiles | electrical | $162 |
| [LED strip connectors + 12V PWM dimmers (Circuits G + D)](https://www.superbrightleds.com/ldk-8a-12-24-volt-dc-single-color-led-dimmer) (LDK-8A) | 1 lot | Super Bright LEDs | electrical | $32 |
| [Master pump switch (Circuit C) — IP67 sealed rocker/disconnect 12V 16A](https://www.amazon.com/dp/B0GF2ZBD1W) (B0GF2ZBD1W) | 1 ea | Amazon | electrical | $8 |
| [MC4 bulkhead passthrough pairs, IP67 panel-mount](https://powerwerx.com/mc4-bulkhead-passthrough-solar-input) (MC4-Bulkhead) | 3 pair | Powerwerx | electrical | $9 |
| [MPPT charge-line fuse — 60A ANL + holder](https://powerwerx.com/blue-sea-5005-anl-fuse-block-cover) (5005-BSS) | 1 ea | Powerwerx | electrical | $43 |
| [NEMA 5-15R weatherproof inlet (flush power panel)](https://www.amazon.com/dp/B0CLDC8X5J) (B0CLDC8X5J) | 1 ea | Amazon | electrical | $10 |
| [Pull-cord ceiling switch, 12V 6A SPST](https://americandoorsupply.com/products/ceiling-pull-switch-spst-nema-4-w-rotg-pivoting-cam) (CPM-1) | 2 ea | americandoorsupply | electrical | $244 |
| [Pump distribution block — 12V DC common busbar, 10-gang](https://www.bluesea.com/products/2300) (2300) | 1 ea | Blue Sea | electrical | $15 |
| [PV cable 10 AWG + MC4 connectors (11 ft extension pair)](https://signaturesolar.com/11ft-10awg-pv-wire-extension-black-red/) (1534034) | 1 lot | Signature Solar | electrical | $30 |
| [Remote battery switch — Blue Sea ML-RBS 500A magnetic-latch (E-stop trip)](https://www.invertersupply.com/index.php?main_page=product_info&products_id=5288) (7700) | 1 ea | Inverter Supply | electrical | $264 |
| [SBL COB 12V red LED safelight strip, 5m reel (Circuit D)](https://www.superbrightleds.com/led-strips-and-bars/5m-rgb-single-color-cob-led-strip-light-cob-series-led-tape-light-ip20-24v-red-green-blue+color-red+volts-12~vdc) (STN-B-BRED-O12A-08F5M-12V) | 1 reel | Super Bright LEDs | electrical | $90 |
| [Sealed wet-zone connectors — 6× Deutsch DT 2-pin pairs (pump circuits)](https://www.buydeutsch.com/collections/dt-series/products/dt06-2s) (DT06-2S) | 1 lot | buyDeutsch | electrical | $27 |
| [Shore-charger output fuse — 20A inline (sealed holder + fuse)](https://www.waytekwire.com/product/sealed-ato-atc-fuse-holder-assembly-46047) (46047) | 1 ea | Waytek Wire | electrical | $7 |
| **electrical-distribution subtotal** | | | | **$2,059–$2,069** |

### electrical-power

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [Cooler inverter — Victron Phoenix 12/375 GFCI](https://www.invertersupply.com/index.php?main_page=product_info&products_id=200695) (PIN123750510) | 1 ea | Inverter Supply | ventilation | $133 |
| [LiFePO4 battery, 100Ah 12V (Renogy Core Series)](https://offgridstores.com/products/renogy-12v-100ah-core-series-deep-cycle-lithium-iron-phosphate-battery) (RBT12100LFP-US) | 1 ea | Off Grid Stores | electrical | $306 |
| [PV array disconnect — Blue Sea 6006 DC battery switch (NEC 690.13)](https://www.waytekwire.com/product/blue-sea-systems-6006-m-series-battery-switch) (6006) | 1 ea | Waytek Wire | electrical | $34 |
| [Solar panel adjustable tilt mount set (per panel)](https://www.amazon.com/Renogy-Adjustable-Solar-Panel-Brackets/dp/B07CSKFWK7) (RNG-MTS-TMB-G1-US) | 3 ea | Amazon | electrical | $108 |
| [Solar panel, 200W monocrystalline 12V (Renogy RSP200D)](https://offgridstores.com/products/renogy-200-watt-12-volt-monocrystalline-solar-panel) (RSP200D-US) | 3 ea | Off Grid Stores | electrical | $510 |
| [Victron Blue Smart IP65 12/15 shore backup charger](https://inverterservicecenter.com/blue-smart-ip65-charger-12-15-1-victron-bpc121531104r) (BPC121531104R) | 1 ea | Inverter Service Center | electrical | $152 |
| [Victron SmartSolar MPPT 100/50 charge controller](https://powerwerx.com/victron-scc110050210-smartsolar-mppt-10050) (SCC110050210) | 1 ea | Powerwerx | electrical | $194 |
| **electrical-power subtotal** | | | | **$1,437** |

### fabric-textile

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [Impact 9oz Duvetyne 57" × 10yd (B&H)](https://www.bhphotovideo.com/c/product/1775270-REG/impact_dr9_10_9_oz_duvetyne_10.html) (1775270) | 1 ea | B&H Photo | film | $69 |
| [Shade cloth — 70% (10×20 ft)](https://www.amazon.com/dp/B075J93DTJ) (B075J93DTJ) | 1 ea | Amazon | ventilation | $30 |
| **fabric-textile subtotal** | | | | **$100** |

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
| [M6×1.0 × 20 hex bolt, 304 SS (A2-70)](https://www.mcmaster.com/91287A137/) (91287A137) | 20 ea | McMaster-Carr | electrical, spray | $7 |
| [M8×1.25 × 25 hex bolt, 304 SS (A2-70) — right-rail end fixing (ICP-14)](https://www.mcmaster.com/91310A535/) (91310A535) | 8 ea | McMaster-Carr | film | $2 |
| [M8×1.25 × 25 hex bolt, Grade 8.8 zinc — shelf cleat + stay mount](https://www.mcmaster.com/91280A534/) (91280A534) | 12 ea | McMaster-Carr | shelf | $4 |
| [M12×40 hex bolt, 18-8 SS](https://www.mcmaster.com/92314A744/) (92314A744) | 24 ea | McMaster-Carr | ibc-frame | $35 |
| [M12×65 hex through-bolt, Grade 8.8 zinc, partial-thread](https://www.mcmaster.com/91280A728/) (91280A728) | 103 ea | McMaster-Carr | film, ibc-frame, walkway | $164 |
| [M12×70 hex through-bolt, Grade 8.8 zinc, partial-thread](https://www.mcmaster.com/91280A732/) (91280A732) | 24 ea | McMaster-Carr | walkway | $42 |
| [M6 flat washer, SS](https://www.mcmaster.com/91455a120/) (91455A120) | 8 ea | McMaster-Carr | electrical | $0 |
| [M8 flat washer, SS](https://www.mcmaster.com/91166A270/) (91166A270) | 12 ea | McMaster-Carr | shelf | $0 |
| [M12 flat washer, zinc](https://www.mcmaster.com/91166a290/) (91166A290) | 508 ea | McMaster-Carr | film, ibc-frame, walkway | $49 |
| [M12 split lock washer, zinc](https://www.mcmaster.com/91202A246/) (91202A246) | 127 ea | McMaster-Carr | film, ibc-frame, walkway | $15 |
| [M6×1.0 flange nut, serrated SS](https://www.mcmaster.com/96194A101/) (96194A101) | 12 ea | McMaster-Carr | tray | $1 |
| [M6×1.0 hex nut, nyloc SS](https://www.mcmaster.com/90576A115/) (90576A115) | 16 ea | McMaster-Carr | spray | $1 |
| [M6×1.0 hex nut, plain SS](https://www.mcmaster.com/90591A151/) (90591A151) | 4 ea | McMaster-Carr | electrical | $0 |
| [M8×1.25 hex nut, plain SS](https://www.mcmaster.com/90591A161/) (90591A161) | 20 ea | McMaster-Carr | film, shelf | $2 |
| [M12 hex nut, plain](https://www.mcmaster.com/90591A181/) (90591A181) | 127 ea | McMaster-Carr | film, ibc-frame, walkway | $32 |
| [M8×25mm knurled thumbscrew DIN 464](https://www.mcmaster.com/92581A540/) (92581A540) | 12 ea | McMaster-Carr | film | $142 |
| 6× steel angle brackets (corridor panel → IBC uprights) | 6 ea | Home Depot | water | $15–$39 |
| Corridor panel mount fasteners (shirt-to-panel screws + lag bolts) | 1 lot | Home Depot | water | $10–$11 |
| [Door pull handle + misc mounting hardware](https://www.mcmaster.com/3570N12/) (3570N12) | 1 ea | McMaster-Carr | interior | $39 |
| Personnel-door hinges (heavy-duty, ×3) | 3 ea | Home Depot | interior | $15–$24 |
| Weatherproof door latch/lock set | 1 ea | Home Depot | interior | $20–$45 |
| [Zinc machine screws — filter housings to ply tee-nuts](https://www.homedepot.com/p/Everbilt-5-16-in-18-x-2-1-2-in-Phillips-Slotted-Round-Head-Machine-Screw-831121/317478933) (831121) | 8 ea | Home Depot | water | $13 |
| [McMaster 5128A63 low-profile hold-down toggle clamp (rail brake)](https://www.mcmaster.com/5128A63/) (5128A63) | 12 ea | McMaster-Carr | film | $155 |
| [10mm × 60mm 304 SS axle pins (4-pack) — skate axles](https://www.amazon.com/uxcell-Single-Hole-Clevis-Pins/dp/B0816MQ5T6) (B0816MQ5T6) | 4 pack | Amazon | film | $20 |
| 3/32" sq × 3/64 SS machine keys (×8) — U-joint keyway | 1 lot | McMaster-Carr | film | $6–$10 |
| [#20 stainless hose clamp (10-pack)](https://www.homedepot.com/p/330548109) (IDL0410PK) | 2 10-pack | Home Depot | water | $37 |
| [Weld-on lashing ring, 1½" ID](https://www.mcmaster.com/3028t31/) (3028T31) | 8 ea | McMaster-Carr | ibc-frame | $40 |
| [Self-drilling structural screw, #14×3¼″ winged, 410 SS](https://www.fastenersplus.com/products/14-x-3-1-4-self-drilling-flat-head-screw-with-wings-410-stainless-steel-pkg-100) (F14C325FDC) | 16 ea | Fasteners Plus | ibc-frame | $16 |
| [2" (50mm) ratchet strap, 3,333 lb WLL](https://www.homedepot.com/p/331257450) (82827) | 4 ea | Home Depot | ibc-frame | $68 |
| [Stainless fasteners + nylon isolation washers](https://www.usplastic.com/catalog/item.aspx?itemid=155501) (92674) | 1 lot | US Plastic + Amazon | lightlock | $45–$60 |
| [100mm Ø SS grab rail](https://www.marinefiberglassdirect.com/products/16-stainless-steel-safety-grab-bar-bolt-on-for-marine-dock-deck-boat-pool-hot-tub) | 1 ea | Marine Fiberglass Direct | lightlock | $25–$45 |
| Misc. conversion hardware (contingency buffer) | 1 lot | Home Depot | interior | $80–$130 |
| [Nylon spring clamp, 3½″ (Pittsburgh 69289)](https://www.harborfreight.com/3-12-in-nylon-spring-clamp-69289.html) (69289) | 58 ea | Harbor Freight | clamp | $115–$173 |
| [304 SS D-grab pull handle (~300mm) + 2× M8 SS bolts + backing plate, matte-black](https://www.strongarhardware.com/pro-line-series-ladder-pull-handle-back-to-back-matte-black-powder-coated-finish-316-exterior-grade-stainless-steel-alloy/) | 1 ea | StrongAr Hardware | panel | $70–$90 |
| [1/4"-20 zinc machine screws (ply-mount interfaces)](https://www.homedepot.com/p/Everbilt-1-4-in-20-x-1-in-Combo-Truss-Head-Zinc-Plated-Machine-Screw-4-Pack-826771/317479749) (826771) | 10 4-pack | Home Depot | water | $16 |
| Southco C2-33 cam compression latch | 4 ea | Southco | panel | $76–$104 |
| 39× cushioned pipe P-clips (3/4" pipe) | 39 ea | Home Depot | water | $21–$37 |
| [1/2"–1 1/4" SS hose clamp (pump flex jumpers)](https://www.homedepot.com/p/Everbilt-1-2-1-1-4-in-Stainless-Steel-Hose-Clamp-10-Pack-671255E/202262870) (202262870) | 2 10-pack | Home Depot | water | $36 |
| 12× welded steel L-brackets (side-panel pipe-run boards) + 4 skid standoff clamps | 1 lot | Metal Supermarkets | water | $12–$24 |
| [Ratchet straps, 25mm](https://www.homedepot.com/p/312994495) (FH0829) | 1 4-pack | Home Depot | ventilation | $10 |
| [Cushioned pipe clip](https://www.amazon.com/dp/B01HPE188Q) (B01HPE188Q) | 16 ea | Amazon | water | $8 |
| Folding shelf stays/brackets, zinc | 2 ea | Amazon | shelf | $24 |
| [Continuous (piano) hinge, 600 mm](https://wurthbaersupply.com/product/711558/1-1-4-WELD-ON-PIANO-HINGE-23-5-8-L-LSN8-32-600) (LSN8-32-600) | 1 ea | Wurth Baer Supply | shelf | $24 |
| Transport latch (over-center/barrel), zinc | 1 ea | Amazon | shelf | $8 |
| [Top + bottom wall stays + 4-bolt anchor plates](https://www.fastenersplus.com/products/5-8-x-6-jaw-eye-galvanized-turnbuckle) (JETBGV58X6) | 2 set | Fasteners Plus | swing | $90–$120 |
| [Clamp-style shaft collar, 25mm/1" bore, SS](https://www.ruland.com/cl-16-st.html) (CL-16-ST) | 1 ea | Ruland | spray | $28–$33 |
| [M12×1.75 jam nut, SS](https://www.mcmaster.com/90381A102/) (90381A102) | 1 ea | McMaster-Carr | spray | $1 |
| [10mm × 60mm 304 SS axle pin (4-pack)](https://www.amazon.com/uxcell-Single-Hole-Clevis-Pins/dp/B0816MQ5T6) (B0816MQ5T6) | 1 pack | Amazon | spray | $5 |
| [SS beam clamp plates (4, cut from 1× 2 ft 304 flat bar)](https://www.mcmaster.com/8992K512/) (8992K512) | 1 2 ft bar | McMaster-Carr | spray | $35 |
| [Figure-8 end clamps, 3/4in poly](https://www.dripdepot.com/figure-8-tubing-end-clamp-size-three-quarter-inch) | 1 10-pack | DripDepot | spray | $4 |
| [Axle saddle clamps ×8 (304 SS flat-bar stock)](https://www.mcmaster.com/8992K794/) (8992K794) | 1 2 ft bar | McMaster-Carr | spray | $10 |
| [Self-tapping SS screws (8-pack)](https://www.lowes.com/pd/Hillman-25-Count-10-x-1-in-Stainless-Steel-Self-Drilling-Interior-Exterior-Sheet-Metal-Screws/3691866) (3691866) | 4 ea | Lowe's (Hillman) | spray | $2–$3 |
| [Nylon zip ties, 8in (200mm)](https://www.harborfreight.com/8-inch-black-cable-ties-pack-of-100-34635.html) (34635) | 1 100-pack | Harbor Freight | spray | $3 |
| [5/16"-18 pronged tee-nut (filter housings)](https://www.homedepot.com/p/Everbilt-5-16-in-18-Zinc-Plated-Tee-Nut-4-Pack-825091/317478996) (825091) | 2 4-pack | Home Depot | water | $3 |
| [1/4"-20 pronged tee-nut (ply-mount interfaces)](https://www.homedepot.com/p/Everbilt-1-4-in-20-Zinc-Plated-Tee-Nut-4-Pack-825001/317478995) (825001) | 10 4-pack | Home Depot | water | $16 |
| [Self-drilling structural screw, #14×2″ HWH, 410 SS](https://www.bridgefasteners.com/products/14-x-2-hex-washer-head-self-drilling-screws-410-stainless-steel-self-tapping-full-thread) | 20 ea | Bridge Fasteners | walkway | $7–$11 |
| Grating clips | 30 ea | McNichols | walkway | $30–$50 |
| **fasteners-hardware subtotal** | | | | **$1,763–$2,105** |

### plastics-sheet

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [1/8" black HDPE sheet (48×96)](https://www.usplastic.com/catalog/item.aspx?itemid=136961&catid=705) (46684) | 4 sheet | US Plastics | panel | $493 |
| [1/8" black HDPE sheet (48×96, ×2)](https://www.usplastic.com/catalog/item.aspx?itemid=136961&catid=705) (46684) | 2 sheet | US Plastics | panel | $247 |
| [1/8" black HDPE sheet — 48×96 (×3)](https://www.usplastic.com/catalog/item.aspx?itemid=136961&catid=705) (46684) | 3 sheet | US Plastics | lightlock | $370 |
| [3/16" UV-stab HDPE sheet, black — 48×96 (×3)](https://www.usplastic.com/catalog/item.aspx?itemid=136962&catid=705) (46685) | 3 sheet | US Plastics | lightlock | $555 |
| Dibond ACM panel 3mm (black), 4×8 sheet | 4 sheet | Central Coast Plastics | film | $380 |
| Drum-exit punch-out grating | 1 lot | McNichols | walkway | $50–$65 |
| HDPE filler strip (L-channel packer) | 1 lot | TAP Plastics | clamp | $30–$70 |
| [HDPE sheet, laminated to 1-1/4" (slope shims)](https://www.usplastic.com/catalog/item.aspx?itemid=31840) (46039+42591) | 1 lot | US Plastic Corp | tray | $296 |
| Molded GRP grating (American Grating, cut-to-size) | 1 lot | American Grating | walkway | $830–$1,050 |
| **plastics-sheet subtotal** | | | | **$3,251–$3,526** |

### plumbing-fittings

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [1" brass foot valve with SS filter](https://www.misterworker.com/en-us/meclube/f1-brass-foot-valve-with-stainless-steel-filter/95953.html) (95953) | 1 ea | misterworker | tray | $14 |
| [1" bulkhead tank-body fittings (Blue equalization cross-tie)](https://www.usplastic.com/catalog/item.aspx?itemid=32194) (32194) | 2 ea | US Plastic Corp | water | $25 |
| [1" FNPT × 1" hose barb (Banjo)](https://www.usplastic.com/catalog/item.aspx?itemid=135154) (31544) | 8 ea | US Plastic Corp | water | $24 |
| [1" MNPT × 1" hose barb (Banjo HB100)](https://www.usplastic.com/catalog/item.aspx?itemid=135135) (31527) | 8 ea | US Plastic Corp | water | $14 |
| [1" NPT spring check valve (CV1 — X1 gravity fill)](https://www.usplastic.com/catalog/item.aspx?itemid=31415) (31415) | 1 ea | US Plastic Corp | water | $24 |
| [1" PVC 4-way cross fitting](https://www.amazon.com/dp/B0CGGV74MB) (B0CGGV74MB) | 1 ea | Amazon | water | $6 |
| [1" PVC Sch-40 pressure pipe](https://www.homedepot.com/p/319692953) (22405) | 4 stick | Home Depot | water | $35 |
| [1" PVC Sch-40 slip 90° elbow](https://www.homedepot.com/p/203812125) (PVC023001000HD) | 4 ea | Home Depot | water | $6 |
| [1" PVC Sch-40 slip tee](https://www.homedepot.com/p/203812199) (PVC024001000HD) | 3 ea | Home Depot | water | $6 |
| [1" PVC slip×MNPT male adapter](https://www.homedepot.com/p/203811640) (PVC021091000HD) | 26 ea | Home Depot | water | $30 |
| [1" reinforced PVC suction hose, 25 ft](https://www.homedepot.com/p/310837595) (6213100025) | 1 25ft coil | Home Depot | tray | $66 |
| [1/2" barbed coupling (pump flex jumpers)](https://www.homedepot.com/p/Rain-Bird-1-2-in-Barbed-Couplings-for-Drip-Tubing-Brown-20-Pack-BC50-20/318470443) (318470443) | 1 20-pack | Home Depot | water | $12 |
| [1/2" ID reinforced braided PVC hose](https://www.usplastic.com/catalog/item.aspx?itemid=60703) (60703) | 3 length | US Plastic Corp | water | $18 |
| [1/2" PVC barbed tee (flex hose → manifold center feed)](https://www.dripdepot.com/barb-tubing-tee-size-half-inch) (1084) | 1 5-pack | DripDepot | spray | $3 |
| [1/2" PVC Sch-40 pipe](https://www.homedepot.com/p/319692959) (30-05010HD) | 8 stick | Home Depot | water | $38 |
| [1/2" PVC Sch-40 slip 90° elbow](https://www.homedepot.com/p/203812033) (PVC023000600HD) | 14 ea | Home Depot | water | $10 |
| [1/2" PVC Sch-40 slip coupling](https://www.homedepot.com/p/203811331) (PVC021000600HD) | 4 ea | Home Depot | water | $3 |
| [1/2" PVC Sch-40 slip tee](https://www.homedepot.com/p/203812195) (PVC024000600HD) | 6 ea | Home Depot | water | $5 |
| [1/2" PVC slip×MNPT male adapter](https://www.homedepot.com/p/203811636) (PVC021090600HD) | 24 ea | Home Depot | water | $19 |
| [1/2" PVC union (serviceable break)](https://www.homedepot.com/p/317901071) (PVCU12F) | 2 ea | Home Depot | water | $10 |
| [1/2" reinforced braided PVC hose, ~15 ft](https://www.homedepot.com/p/304185193) (T12006003) | 1 10ft roll | Home Depot | spray | $13 |
| [1/2"×1" NPT bushing reducer](https://www.homedepot.com/p/204836713) (PVC021121800HD) | 1 ea | Home Depot | water | $3 |
| [2" polypropylene camlock pairs (M+F)](https://www.usplastic.com/catalog/item.aspx?itemid=30754) (30754) | 4 pair | US Plastic Corp | water | $92 |
| [2"→1" PVC Sch-80 reducing coupling (FNPT×FNPT)](https://www.homedepot.com/p/203811533) (PVC021071300HD) | 8 ea | Home Depot | water | $26 |
| [3-way diverter valve 1" FNPT](https://www.usplastic.com/catalog/item.aspx?itemid=31268) (31268) | 1 ea | US Plastic Corp | water | $61 |
| [3-way diverter valve 1/2" FNPT](https://www.usplastic.com/catalog/item.aspx?itemid=22365) (22365) | 2 ea | US Plastic Corp | water | $48 |
| [3/4" LDPE irrigation poly pipe, 100 ft](https://www.dripdepot.com/polyethylene-tubing-size-three-quarter-inch-0-820-inch-inside-diameter-by-0-940-inch-od-length-100-feet) (3552) | 1 100ft roll | DripDepot | spray | $31 |
| [3/4" PVC Sch-40 pipe](https://www.homedepot.com/p/100348472) (PVC-04007-0600) | 2 stick | Home Depot | water | $12 |
| [90° spray jets, barbed](https://www.homedepot.com/p/302581648) (110B) | 5 10-pack | Home Depot | spray | $17 |
| [Banjo V050FP ball valve 1/2" FNPT](https://www.grainger.com/product/803HZ1) (803HZ1) | 3 ea | Grainger | water | $72 |
| [Banjo V050FP ball valve 1/2" FNPT](https://www.grainger.com/product/803HZ1) (803HZ1) | 1 ea | Grainger | water | $24 |
| [Banjo V050FP ball valve 1/2" FNPT](https://www.grainger.com/product/803HZ1) (803HZ1) | 2 ea | Grainger | water | $48 |
| [Banjo V100FP ball valve 1" FNPT](https://www.usplastic.com/catalog/item.aspx?itemid=30653) (30653) | 6 ea | US Plastic Corp | water | $297 |
| [Bulkhead fitting 2" NPT (polypropylene)](https://www.usplastic.com/catalog/item.aspx?itemid=32200) (32200) | 3 ea | US Plastic Corp | water | $63 |
| [pH sample tap (SV-01) — 1/2" PP ball valve + barb spout + branch tee](https://www.usplastic.com/catalog/item.aspx?itemid=36903) (36903) | 1 ea | US Plastic Corp | water | $19 |
| [pH sample tap (SV-02) — 1/2" PP ball valve + barb spout + branch tee](https://www.usplastic.com/catalog/item.aspx?itemid=36903) (36903) | 1 ea | US Plastic Corp | water | $19 |
| [S60×6 female buttress → 2" MNPT IBC tote adapter](https://www.amazon.com/Granatan-Adapter-Buttress-Fittings-Connector/dp/B095SCHBC6) (B095SCHBC6) | 8 ea | Amazon | water | $80 |
| [½" PVC Sch-40 pipe (tap relocation)](https://www.homedepot.com/p/319692959) (30-05010HD) | 1 stick | Home Depot | shelf | $5 |
| **plumbing-fittings subtotal** | | | | **$1,300** |

### seals-gaskets

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [20mm EPDM gasket (per meter, closed-cell)](https://www.amazon.com/dp/B089GJQ96Z) (B089GJQ96Z) | 21 m | Amazon (OKAYASU) | panel | $24–$52 |
| [Black EPDM foam tape 1"×½"](https://www.mcmaster.com/8694K88/) (8694K88) | 2 roll | McMaster-Carr | film | $45 |
| Certified anti-slip cargo matting (μ≥0.6) | 4 ea | Uline / cargo-securing supplier | ibc-frame | $40–$80 |
| [Felt/brush wiper strip + 12mm closed-cell neoprene](https://www.doitbest.com/product/146005/) (BP17A) | 1 lot | Frost King + Canal Rubber | lightlock | $40–$75 |
| Light-sealing materials (interior conversion) | 1 lot | Amazon (bundle) | interior | $157–$178 |
| Ribbed-wall flashing + silicone (power-panel box seal) | 1 lot | Hardware store | electrical | $15–$30 |
| [Silicone gasket strip](https://www.countrymax.com/aqueon-silicone-clear-aquarium-sealant-10oz-bottle/) (015952) | 1 ea | CountryMax (Aqueon) | tray | $17–$25 |
| [Tight-seal nylon strip brush + aluminum holder (~4.7 m, top + bottom)](https://www.mcmaster.com/74405T12-74405T126/) (74405T12) | 1 lot | McMaster-Carr | door | $129 |
| **seals-gaskets subtotal** | | | | **$466–$613** |

### stainless-sheet

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| 304 SS sheet, 16-gauge (1.5mm), 2B mill finish | 2 ea | Online Metals | tray | $610–$850 |
| [Custom laser-drilled pinhole — SS-302/304 shim, 3×3](https://lenoxlaser.com/shop/optical-apertures/standard-apertures/standard-aperture/) (SS-3/8-DISC) | 1 ea | Lenox Laser | optics | $40–$100 |
| **stainless-sheet subtotal** | | | | **$650–$950** |

### steel-structural

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [1.5" EMT conduit, 10 ft](https://www.homedepot.com/p/304229415) (550210000) | 6 stick | Home Depot | ventilation | $131 |
| 12mm steel plate, 150 × 150 cut | 4 ea | Metal Supermarkets | ibc-frame | $20–$40 |
| 25×25×3 mm steel SHS | 1 lot | Online Metals | shelf | $30 |
| 2×2×0.120in steel SHS (6 m bulk lengths) | 4 ea | Metal Supermarkets | ibc-frame | $120–$180 |
| 2×2×0.120in steel SHS (6 m bulk lengths) | 3 ea | Metal Supermarkets | door | $90–$120 |
| 2×2×0.120in steel SHS (6 m bulk lengths) | 4 ea | Metal Supermarkets | panel | $120–$160 |
| [3/8" 304/304L SS rod — U-joint stub shafts (1× 3 ft)](https://www.mcmaster.com/89535K87/) (89535K87) | 1 lot | McMaster-Carr | film | $13 |
| 304 flat-bar Z (tilt) + X (swing) cross-slides + UHMW pad + gib | 4 set | Metal Supermarkets | film | $316–$516 |
| [304 SS square tube 1½×1½×0.062in, single 17ft4in *](https://www.metalsdepot.com/stainless-steel-products/304-stainless-steel-square-tube) | 1 ea | Metals Depot | spray | $183 |
| 4mm folded plate | 8 ea | Local fab | ibc-frame | $60–$100 |
| 75mm Ø × 150mm steel stub shaft | 2 ea | Steel service center | lightlock | $30–$50 |
| Baffle duct sheet metal (cooler) | 1 lot | Local sheet metal | ventilation | $20 |
| Baffle duct sheet metal (fans) | 1 lot | Local sheet metal | ventilation | $30 |
| Cantilever bracket — standard (near/far) | 13 ea | Local fab | walkway | $390–$650 |
| Cantilever bracket — widened (near) | 5 ea | Local fab | walkway | $200–$350 |
| Combined corner plate (right corners) | 2 ea | Local fab | walkway | $50–$80 |
| Corner gusset plate, 3 mm | 4 ea | Steel offcut | shelf | $5 |
| Corner plate 304 SS (U-joint mount) | 4 ea | Metal Supermarkets | film | $236 |
| Drop-in rail saddles + tapered dowels | 4 ea | Local fab | swing | $80–$130 |
| Drum support cage, 1.5×1.5×0.120in steel SHS | 1 lot | Local fab | swing | $70–$120 |
| [EMT canopy base plates + ground stakes (×4)](https://www.homedepot.com/p/317889187) (PDB-F-1-4) | 1 4-pack | Home Depot | ventilation | $16 |
| [EMT canopy corner pull elbows (×4)](https://www.homedepot.com/p/203776547) (94510) | 4 ea | Home Depot | ventilation | $47 |
| [EMT canopy fittings (couplings, corner ells, connectors)](https://www.homedepot.com/p/100135091) (12210) | 8 ea | Home Depot | ventilation | $12 |
| Fabricated flanged wall-penetration box (front face + flange) | 1 lot | Local fab | electrical | $60–$100 |
| Floor-leg cantilever bracket (left walkway, ×5) | 5 ea | MetalsDepot | walkway | $65–$105 |
| Reinforcing plate (exterior) | 18 ea | Local fab | walkway | $75–$130 |
| Right walkway cantilever frame | 1 lot | MetalsDepot | walkway | $125–$153 |
| Shelf mount backing plates, 8mm steel (welded, ×3) | 3 ea | Local fab | shelf | $18–$30 |
| Shutter plate (⅛ steel 10×8) + slide channel | 1 ea | Local fab | optics | $25–$50 |
| Skate carriage plate (×4) — fab | 4 ea | Local fab | film | $136–$236 |
| Steel backing plate 60×205×8mm | 8 ea | Metal Supermarkets | ibc-frame | $32–$56 |
| Steel backing plate 6×6×⅛ + welded frame | 1 ea | Metal Supermarkets | optics | $20–$40 |
| [Steel flat bar 25×3mm — ribbon support cross-brace](https://www.mcmaster.com/6775T37-6775T373/) (6775T37) | 2 3ft bar | McMaster-Carr | water | $35 |
| Transition bearing plate | 2 ea | Local fab | walkway | $5–$10 |
| Wall cleat (left corners) | 2 ea | Local fab | walkway | $20–$35 |
| Wall mounting cleat + anchors | 1 lot | Local fab | shelf | $18 |
| Wall-seat saddle 10mm A36 plate (ICP-11) | 1 sheet | Metal Supermarkets | film | $102 |
| Wall-seat saddle 8mm A36 plate (ICP-11) | 1 sheet | Metal Supermarkets | film | $216 |
| Ø89×8mm CHS pivot post + machined hub / thrust collar | 1 ea | Metal Supermarkets | swing | $180–$300 |
| **steel-structural subtotal** | | | | **$3,401–$4,835** |

### substrate-fabric

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [Unbleached muslin, 60" wide](https://www.fabricdirect.com/shop/craft-fabric/broadcloth-and-muslin-fabric/essence-60-medium-weight-muslin-fabric-unbleached-150-yard-roll/) | 3 roll | Fabric Direct | chemistry | $300 |
| **substrate-fabric subtotal** | | | | **$300** |

### timber-ply

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [Corridor plumbing-panel ply (23/32" exterior)](https://www.homedepot.com/p/23-32-in-x-4-ft-x-8-ft-RTD-Southern-Yellow-Pine-Wood-Sheathing-Plywood-129323/303564747) (303564747) | 1 sheet | Home Depot | water | $29 |
| [EP plywood backing panel (18mm, ~700×2000mm)](https://www.homedepot.com/p/203414066) (454559) | 1 4'×8' sheet | Home Depot | electrical | $69 |
| [Pinhole-wall filter-skid backing ply (23/32" exterior)](https://www.homedepot.com/p/23-32-in-x-4-ft-x-8-ft-RTD-Southern-Yellow-Pine-Wood-Sheathing-Plywood-129323/303564747) (303564747) | 2 sheet | Home Depot | water | $59 |
| [Pressure-treated pine plywood (Fan B mount band + cooler base)](https://www.homedepot.com/p/206343229) (231428) | 1 4'×8' ¾" sheet | Home Depot | panel | $70 |
| [Pump-mount shirt ply (23/32" exterior)](https://www.homedepot.com/p/23-32-in-x-4-ft-x-8-ft-RTD-Southern-Yellow-Pine-Wood-Sheathing-Plywood-129323/303564747) (303564747) | 1 sheet | Home Depot | water | $29 |
| [UV-coated white plywood (work surface)](https://www.homedepot.com/p/302874373) (BPI6WUV2I) | 1 4'×8' 18mm sheet | Home Depot | shelf | $73 |
| **timber-ply subtotal** | | | | **$329** |

### tools-safety

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [4-mil black poly sheeting](https://www.homedepot.com/p/332820356) (51982) | 1 roll | Home Depot | film | $40 |
| [6-mil black LDPE sheeting](https://www.homedepot.com/p/332821399) (59803) | 1 roll | Home Depot | water | $55 |
| [Apera Instruments AI311 PH60 pH meter](https://www.amazon.com/dp/B01ENFOIQE) (B01ENFOIQE) | 1 ea | Amazon | water | $80 |
| [Chemical-resistant labels (GHS)](https://www.amazon.com/dp/B0BWFW5481) (B0BWFW5481) | 1 pack | Amazon | water | $24 |
| [Citric acid, food grade, 6 lb](https://www.amazon.com/dp/B0F1CKRT7G) (B0F1CKRT7G) | 2 bag | Amazon | water | $60 |
| [Nitrile gloves, box of 100](https://www.amazon.com/dp/B0CMZ5VXMS) (B0CMZ5VXMS) | 2 box | Amazon | water | $30 |
| [pH calibration solution set](https://www.amazon.com/dp/B09DCP4HNH) (B09DCP4HNH) | 1 set | Amazon | water | $8 |
| **tools-safety subtotal** | | | | **$297** |

### water-equipment

| Item | Qty | Supplier | Systems | Est. cost |
|------|-----|----------|---------|-----------|
| [Big Blue filter housing 4.5"×20" (separate)](https://www.amazon.com/dp/B0137680E6) (B0137680E6) | 3 ea | Amazon | water | $250 |
| [Big Blue housing mounting brackets (×3)](https://www.freshwatersystems.com/products/mounting-bracket-white-single-housing-for-10-20-big-blue-housings) (150061) | 3 ea | Fresh Water Systems | water | $32 |
| [CTO carbon block cartridge 4.5"×20"](https://www.amazon.com/dp/B07ZHPB6MB) (B07ZHPB6MB) | 2 ea | Amazon | water | $80 |
| [IBC tote (1,000 L caged)](https://www.repackify.com/buy-ibc-totes/california) | 4 ea | SoCal reconditioner | water | $600 |
| [KDF-55 heavy-metal cartridge 4.5"×20"](https://www.amazon.com/dp/B0DY1ZK47Z) (B0DY1ZK47Z) | 1 ea | Amazon | water | $80 |
| [MPP 5-micron sediment cartridge 4.5"×20"](https://www.amazon.com/dp/B0CJCVZ1L5) (B0CJCVZ1L5) | 2 ea | Amazon | water | $62 |
| Plywood offcut spacer blocks 25mm (filter skid) | 1 lot | offcuts | water | $0 |
| [SeaFlo accumulator (0.75 L)](https://www.amazon.com/dp/B01MUYL8F8) (SFAT-075-125-01) | 2 ea | Amazon | water | $72 |
| [Shurflo 2088-554-144 pump (×5 — P-01 Blue supply / P-02 Brown recycle-spray / P-03 waste evac / P-04 tray drain / P-05 Brown drain)](https://www.amazon.com/dp/B00C1M6B1C) (B00C1M6B1C) | 5 ea | Amazon | water | $500 |
| **water-equipment subtotal** | | | | **$1,675** |

## Supplier consolidation (largest orders first)

| Supplier | Line items | Types | Est. cost |
|----------|-----------|-------|-----------|
| Local fab | 19 | adhesives-finishes, aluminum, fabrication-labor, steel-structural | $2,160–$3,522 |
| containermgt.com | 1 | container | $2,000–$3,500 |
| Metal Supermarkets | 14 | aluminum, fasteners-hardware, steel-structural | $2,117–$2,643 |
| Amazon | 34 | adhesives-finishes, aluminum, bearings-motion, ducting-ventilation, electrical-distribution, electrical-power, fabric-textile, fasteners-hardware, plumbing-fittings, tools-safety, water-equipment | $2,106–$2,156 |
| Home Depot | 57 | adhesives-finishes, ducting-ventilation, electrical-distribution, fasteners-hardware, plumbing-fittings, steel-structural, timber-ply, tools-safety | $1,806–$1,943 |
| US Plastics | 4 | plastics-sheet | $1,665 |
| Grainger | 7 | aluminum, bearings-motion, electrical-distribution, plumbing-fittings | $1,626 |
| Artcraft Chemicals | 3 | chemistry-reagents | $1,414 |
| McMaster-Carr | 47 | aluminum, bearings-motion, fasteners-hardware, seals-gaskets, steel-structural | $1,346–$1,350 |
| Local plastic fab | 1 | fabrication-labor | $800–$1,150 |
| Online Metals | 3 | aluminum, stainless-sheet, steel-structural | $760–$1,080 |
| American Grating | 1 | plastics-sheet | $830–$1,050 |
| US Plastic Corp | 13 | plastics-sheet, plumbing-fittings | $1,001 |
| Off Grid Stores | 4 | electrical-distribution, electrical-power | $912 |
| Local sheet metal | 3 | fabrication-labor, steel-structural | $500–$900 |
| Commercial tilt-bed hire | 1 | fabrication-labor | $300–$800 |
| SoCal reconditioner | 1 | water-equipment | $600 |
| Inverter Supply | 2 | electrical-distribution, electrical-power | $396 |
| Central Coast Plastics | 1 | plastics-sheet | $380 |
| Powerwerx | 5 | electrical-distribution, electrical-power | $308 |
| Fabric Direct | 1 | substrate-fabric | $300 |
| igus | 1 | bearings-motion | $261 |
| MetalsDepot | 2 | steel-structural | $190–$258 |
| americandoorsupply | 1 | electrical-distribution | $244 |
| Waytek Wire | 15 | electrical-distribution, electrical-power | $229 |
| Bearings Direct | 2 | bearings-motion | $201 |
| Metals Depot | 1 | steel-structural | $183 |
| Amazon (bundle) | 1 | seals-gaskets | $157–$178 |
| Harbor Freight | 2 | fasteners-hardware | $118–$176 |
| LED Profiles | 1 | electrical-distribution | $162 |
| Inverter Service Center | 1 | electrical-power | $152 |
| Fasteners Plus | 2 | fasteners-hardware | $106–$136 |
| Super Bright LEDs | 2 | electrical-distribution | $122 |
| McNichols | 2 | fasteners-hardware, plastics-sheet | $80–$115 |
| Southco | 1 | fasteners-hardware | $76–$104 |
| Lenox Laser | 1 | stainless-sheet | $40–$100 |
| Hardware store | 3 | adhesives-finishes, seals-gaskets | $57–$92 |
| StrongAr Hardware | 1 | fasteners-hardware | $70–$90 |
| HitLights | 1 | electrical-distribution | $75–$85 |
| Uline / cargo-securing supplier | 1 | seals-gaskets | $40–$80 |
| Frost King + Canal Rubber | 1 | seals-gaskets | $40–$75 |
| TAP Plastics | 1 | plastics-sheet | $30–$70 |
| B&H Photo | 1 | fabric-textile | $69 |
| Blue Sea | 2 | electrical-distribution | $61 |
| US Plastic + Amazon | 1 | fasteners-hardware | $45–$60 |
| Fibergrate | 1 | adhesives-finishes | $40–$60 |
| AutomationDirect | 1 | electrical-distribution | $52 |
| Amazon (OKAYASU) | 1 | seals-gaskets | $24–$52 |
| Steel service center | 1 | steel-structural | $30–$50 |
| Polycase | 1 | electrical-distribution | $47 |
| Marine Fiberglass Direct | 1 | fasteners-hardware | $25–$45 |
| DripDepot | 3 | fasteners-hardware, plumbing-fittings | $38 |
| Ruland | 1 | fasteners-hardware | $28–$33 |
| Fresh Water Systems | 1 | water-equipment | $32 |
| Signature Solar | 1 | electrical-distribution | $30 |
| buyDeutsch | 1 | electrical-distribution | $27 |
| Harfington | 2 | electrical-distribution | $25 |
| CountryMax (Aqueon) | 1 | seals-gaskets | $17–$25 |
| Wurth Baer Supply | 1 | fasteners-hardware | $24 |
| Local machine shop | 1 | aluminum | $12–$18 |
| misterworker | 1 | plumbing-fittings | $14 |
| Bridge Fasteners | 1 | fasteners-hardware | $7–$11 |
| Steel offcut | 1 | steel-structural | $5 |
| Lowe's (Hillman) | 1 | fasteners-hardware | $2–$3 |
| offcuts | 1 | water-equipment | $0 |
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
| Ferric ammonium oxalate (AmFe) | <!-- BEGIN costing:om-amfe-g-standard -->342<!-- END costing:om-amfe-g-standard -->g | <!-- BEGIN costing:om-amfe-kg-standard -->17.1<!-- END costing:om-amfe-kg-standard --> kg |
| Potassium ferricyanide (3:1) | 130g | 6.5 kg |
| Ammonium dichromate (contrast, 0.1–0.4%) | ~1–4g | ~0.2 kg |
| Distilled water | ~2.6 L | ~130 L |

Standard ½-Ware is the working default; the leanest/richest viable strength — and the final order — is
pinned by the [Sensitizer Trials](sensitizer-trials.md). **Run cost ~$1,710 (Standard), range ~$1,250
(Lean) – ~$3,100 (Rich)** per 50-print run (~$25–62/print), incl. ~$300 muslin substrate — ~399 linear
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
| **[Photographers' Formulary](https://stores.photoformulary.com)** | Ferric ammonium oxalate (AmFe), ammonium dichromate | Condon, MT |
| **[Bostick & Sullivan](https://bostick-sullivan.com)** | Potassium ferricyanide + AmFe (cyanotype reagents) | Santa Fe, NM |
| **[Fabric Direct](https://www.fabricdirect.com)** | Unbleached cotton muslin, 150-yd rolls | Online |
| **[Fabric Wholesale Direct](https://www.fabricwholesaledirect.com)** | Unbleached muslin by yard or bolt | Online |
| **[Metal Supermarkets](https://www.metalsupermarkets.com)** | Steel, aluminum, cut-to-length | Anaheim · Van Nuys · San Diego |
| **[Grimco](https://www.grimco.com)** | Dibond ACM panels (sign industry) | City of Industry CA |
| **Automation Overstock** | Linear guides, carriages, surplus motion components | Gardena CA (walk-in) |
| **[Ruland](https://www.ruland.com)** | CL-16-ST clamp-style shaft collar (spray arm) | Ships nationally |
| **[Renogy](https://www.renogy.com)** | Solar panels, LiFePO4 battery, tilt mount | Online |
| **[altE Store](https://www.altestore.com)** | Victron MPPT, Victron chargers, off-grid power | Online |
| **[Powerwerx](https://powerwerx.com)** | Anderson Powerpole connectors and tools | Online |
| **[Waytek Wire](https://www.waytekwire.com)** | Deutsch DT connectors, automotive wire | Online |
| **[West Marine](https://www.westmarine.com)** | Blue Sea fuse blocks, marine DC wiring | Torrance CA |
| **[Container Exchanger](https://containerexchanger.com)** | Used IBC totes, food-grade — CA listings | Online |
| **[Ferguson Plumbing](https://www.ferguson.com)** | PVC pipe, valves, fittings | Multiple SoCal branches |
| **Pacific Coast Steel** | Hot-rolled A36 sheet, round bar, structural steel | Santa Fe Springs CA |
| **[TAP Plastics](https://www.tapplastics.com)** | UV-HDPE / PP / acrylic sheet + plastic fabrication | Multiple SoCal stores |
| **[Curbell Plastics](https://www.curbellplastics.com)** | PP / engineering plastic sheet | Online / SoCal |
| **[AutomationDirect](https://www.automationdirect.com)** | DC load-break isolators, E-stop push-buttons | Online |
| **[B&H Photo](https://www.bhphotovideo.com)** | Impact Duvetyne, photographic supplies | Online / NYC |
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