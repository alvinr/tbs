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
| 6. Electrical — power, circuits, wiring | $2,025 | $2,575 |
| 7. Housed revolving-door light lock (plastic-skin custom fabrication) | $1,465 | $2,160 |
| 7a. Panel swing pivot (Ø89 pivot post + bearings + cage + wall stays + rail saddles) | $1,112 | $1,372 |
| 7b. Perimeter walkway (4 sections + drum-exit punch-out) | $1,826 | $2,607 |
| 8. Cooling & ventilation | $824 | $974 |
| 9. Printmaking chemistry — cyanotype, 50 prints (Low = Lean, High = Rich tier) | $1,210 | $2,980 |
| 10. Printmaking tools & consumables | $350 | $500 |
| 11. Safety & PPE | $120 | $180 |
| **TOTAL (base build + 50-print run)** | **~$20,026** | **~$29,623** |
<!-- END costing:master-summary -->

*Optional additions: electric film plane actuation (+$827), lens plate (+$400–$1,500), self-haul transport (+$30,000–$40,000).*

*Line 9 (printmaking chemistry) is now the **Mike Ware AmFe** recipe with the corrected ~$300 substrate, re-summed into the TOTAL: **Low = Lean ⅓-Ware (~$1,210), High = Rich full-Ware (~$2,980)**, working default Standard ½-Ware (~$1,650). The tier is pinned by the [Sensitizer Trials](sensitizer-trials.md); the TOTAL spans the Lean–Rich range, so it shifts within ±~$1,330 of the §9 line once a tier is locked.*

---

## 1. Container & Delivery
*Source: `pinhole-camera-construction.md`, `project-cost-breakdown.md`*

| Item | Spec | Supplier | Est. cost |
|------|------|----------|-----------|
| 20ft ISO container — Cargo Worthy grade | CSC-certified, WWT minimum | Container Management / Local container dealers | $2,000–$3,500 |
| Delivery — short haul (<50 miles, tilt-bed) | Commercial hire | Local crane/tilt-bed truck hire | $300–$800 |
| Delivery — long haul (100–300 miles, semi flatbed) | If needed | Commercial freight broker | $1,200–$2,500 |

**Section total: $2,300–$4,300**

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
| [Dibond ACM panel 4mm](https://www.grimco.com) | 4'×8' sheets — flat backing surface | 6 | Grimco, City of Industry CA | $85† | $510 |
| Through-bolts + hardware | Into structural ribs every 18" | 1 lot | McMaster-Carr | $40 | $40 |
**Backing subtotal: ~$550**

### Door & access
| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| Door gasket set | OEM-style rubber seal for container cargo doors | 1 | Container parts suppliers | $45 | $45 |
| Miscellaneous hardware (fasteners, steel angle, touchup paint) | — | 1 lot | Home Depot | — | $110 |
**Section total: ~$950–$1,350**

## 3. Pinhole Optics Plate
*Source: `pinhole-report.md`, `pinhole-camera-construction.md`*

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [Custom laser-drilled pinhole](https://www.lenoxlaser.com) | Ø2.17mm ±0.025mm, SS-302 shim 3"×3", SEM-verified | 1 | Lenox Laser | $50–$150 |
| Steel backing plate 6"×6"×⅛" + welded frame | Houses precision insert in wall plate | 1 | Metal Supermarkets SoCal | $20–$40 |
| Shutter plate ⅛" steel, 10"×8" + slide channel | Simple sliding shutter, exterior operation | 1 | Metal Supermarkets | $25–$50 |

**Section total: $95–$240**

## 4. Film Plane Mechanism (4-Corner Independent)
*Source: `film-plane-mechanism-report.md`, `project-cost-breakdown.md`*

### Structural & rails
| Item | Spec | Qty | Supplier A | Supplier B | Est. unit |
|------|------|-----|-----------|-----------|-----------|
| [Linear guide rail HGR20](https://www.amazon.com/s?k=HGR20+linear+rail+guide) | 2,200mm length | 4 | Amazon / Automation Overstock | [McMaster #5901T777](https://www.mcmaster.com/5901T777) | $45 |
| [Rail carriage HGH20CA](https://www.amazon.com/s?k=HGH20CA+carriage+block) | Flanged block | 8 | Amazon / Automation Overstock | McMaster-Carr | $18 |
| [Acme leadscrew ¾"-6](https://www.roton.com) | 8ft length | 4 | [Roton Products](https://www.roton.com) | [McMaster #6289K36](https://www.mcmaster.com/6289K36) | $95 |
| [Acme nut, bronze ¾"-6](https://www.roton.com) | — | 4 | [Roton Products](https://www.roton.com) | [McMaster #6289K512](https://www.mcmaster.com/6289K512) | $12 |
| [Handwheel 8" dia](https://www.mcmaster.com/6440K64) | ¾" bore, cast aluminum | 4 | McMaster-Carr | McMaster #6440K64 | $35 |
| [Locking collar SS316](https://www.mcmaster.com/6436K12) | ¾" bore | 4 | McMaster-Carr | McMaster #6436K12 | $12 |
| Corner bracket L-plate | ¼" aluminum plate, 6"×8" | 4 | Metal Supermarkets SoCal | [Online Metals](https://www.onlinemetals.com) | $20 |
| Cross-slide rail HGR15 (Option A) | 300mm — X-Z floating stage | 8 | Amazon / Automation Overstock | McMaster-Carr | $25 |
| Cross-slide carriage HGH15CA (Option A) | Flanged block | 8 | Amazon / Automation Overstock | McMaster-Carr | $12 |
| Cross-slide intermediate plate (Option A) | ¼" aluminum, joins X slide to Z slide | 4 | Metal Supermarkets SoCal | [Online Metals](https://www.onlinemetals.com) | $15 |
| [Rod-end spherical bearing](https://www.mcmaster.com/60645K73) | GIR25-DO or equiv., 25mm bore | 8 | McMaster-Carr | McMaster #60645K73 | $22 |
| [Pivot pin SS316](https://www.mcmaster.com/98173A150) | 1" dia × 8" long | 8 | McMaster-Carr | McMaster #98173A150 | $8 |
**Rails & structural subtotal: ~$1,616** *(incl. Option A cross-slides +$356)*

### Film plane frame & backing
| Item | Spec | Qty | Supplier A | Supplier B | Est. unit |
|------|------|-----|-----------|-----------|-----------|
| Aluminum angle 2"×2"×3/16" | 8ft lengths | 10 | Metal Supermarkets SoCal | [Online Metals](https://www.onlinemetals.com) | $22 |
| [Dibond ACM panel 4mm](https://www.grimco.com) | 4'×8' sheets — **single rigid backing** (Option A), <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->×<!-- BEGIN fact:film_plane_height_mm -->2,388<!-- END fact:film_plane_height_mm -->mm | 6 | Grimco, City of Industry CA | Signwarehouse | $85 |
| [Black EPDM foam tape 1"×½"](https://www.mcmaster.com/8614K84) | 50ft rolls — panel perimeter seal + housing-surround ring (Ø900 aperture) | 4 | McMaster-Carr #8614K84 | — | $37 |
| [Rosco Duvetyne blackout fabric](https://www.rosebrand.com) | 60" wide, 10 yd | 1 | [Rose Brand](https://www.rosebrand.com) (Burbank CA) | B&H Photo | $95 |
| 6-mil black poly sheeting | 10'×100' roll | 1 | Home Depot | — | $65 |
| 2" black Gorilla Tape | 35 yd rolls | 6 | Home Depot | Amazon | $12 |
**Frame subtotal: ~$1,055** *(Option A: single rigid ACM backing — folding piano hinge removed, –$56)*

### Optional: electric actuation (add-on)
| Item | Spec | Qty | Supplier | Est. unit |
|------|------|-----|----------|-----------|
| [PA-14 linear actuator](https://www.progressiveautomations.com) | 12V, 20" stroke, 150 lb | 4 | [Progressive Automations](https://www.progressiveautomations.com) | $185 |
| 12V 30A power supply | Enclosed | 1 | [Mouser](https://www.mouser.com) / Digi-Key | $55 |
| DPDT momentary rocker switch | Panel-mount, 20A | 4 | [Mouser](https://www.mouser.com) | $8 |
**Electric actuation subtotal: ~$827 (optional)**

### Wall-seat saddles (ICP-11 through ICP-14) — rev 11, replaces the brace cage
*Each of the 8 film-plane rail ends anchors to the container with a wall-seat saddle (back-plate + seat + gusset), through-bolted with a 4-bolt pattern to an exterior wall plate — the container shell carries the rigidity. Right rails permanently bolted; left rails thumb-screw drop-in (lift out for the drum swing).*

| Item | ICP # | Spec | Qty | Supplier A | Supplier B | Est. unit | Est. total |
|------|-------|------|-----|-----------|-----------|-----------|------------|
| [Mild steel plate 8mm — laser/plasma cut](https://www.metalsupermarkets.com/product/mild-steel-plate/) | ICP-11 | back-plate + exterior plate + seat + gusset per saddle; ~28 kg total over 8 saddles, cut + welded | 8 saddles | [Metal Supermarkets SoCal](https://www.metalsupermarkets.com/) (Anaheim / Van Nuys / San Diego — cut to size, walk-in) | [Online Metals — A36 steel plate 8mm](https://www.onlinemetals.com/en/buy/carbon-steel) (ships; cut to size) | ~$53 est. | ~$425 est. |
| [M12×90mm hex through-bolt + nut + washers, SS](https://www.mcmaster.com/products/screws/) | ICP-12 | Wall sandwich through-bolt (interior↔exterior plate); 4 per saddle × 8 = 32 + 4 spare | 36 | [McMaster-Carr — A2 stainless cap screws](https://www.mcmaster.com/products/screws/) | [Amazon — M12 stainless bolts](https://www.amazon.com/s?k=m12+stainless+bolt+90mm) | ~$2.50 est. | ~$90 est. |
| [M8×25mm knurled thumbscrew DIN 464, SS 303](https://www.amazon.com/knurled-thumb-screws-din-464/s?k=knurled+thumb+screws+din+464) | ICP-13 | Left-rail drop-in hold-down (lifts out for drum swing); 2 per saddle × 4 left saddles = 8 + 4 spare | 12 | [Amazon — DIN 464 M8 stainless](https://www.amazon.com/knurled-thumb-screws-din-464/s?k=knurled+thumb+screws+din+464) | [Maedler North America — PN 65499225](https://maedlernorthamerica.com/partshop/knurled-thumb-screw-din-464-m8-x-20mm-long-stainless-steel-1-4305-pn-65499225/) (~$15–17 ea. direct; Amazon cheaper in packs) | ~$3 est. | ~$36 est. |
| [M8 hex fixing bolt + nut, SS](https://www.mcmaster.com/products/screws/) | ICP-14 | Right-rail permanent fixing (rail bolted to seat); 2 per saddle × 4 right saddles = 8 + spare | 12 | [McMaster-Carr — A2 stainless](https://www.mcmaster.com/products/screws/) | [Amazon — M8 stainless bolts](https://www.amazon.com/s?k=m8+stainless+bolt) | ~$2 est. | ~$24 est. |

**Wall-seat saddle subtotal: ~$575 est.** *(roughly cost-neutral with the retired brace cage)*

*All prices estimated — Metal Supermarkets and McMaster-Carr do not publish per-unit pricing online; call or add to cart for a current quote. 8mm A36 plate runs ~$3–5/kg cut. M8 thumbscrew pricing confirmed at ~$15–17 each from Maedler North America (PN 65499225, May 2026); Amazon multi-packs run ~$2–5 ea. depending on pack size.*

**Section total (manual, incl. wall-seat saddles + Option A cross-slides): ~$3,538–$4,088** *(= cost-breakdown §4)*

> **Option A delta (2026-06-06):** the film plane is now a **fixed-size rigid** rectangle posed by **8 corner cross-slides** (2-axis X-Z stage per corner) that absorb the rigid-rotation arc travel. Added 8 cross-slide rails +$200, 8 carriages +$96, 4 intermediate plates +$60 (= +$356); removed the folding-backing piano hinge –$56 → **net +$300**. Single rigid ACM backing replaces the hinged two-panel system; the achievable envelope is tilt ±40° / swing ±28° single-axis (combined limited; the old compound-twist config is dropped).
>
> **4-corner vs original 2-beam design delta:** Removed 2× 80/20 T-slot beams (5,893mm) — saves $416. Added: 2× extra leadscrews +$190, 2× extra handwheels +$70, 4× rod-end spherical bearings +$88, 4× corner L-brackets +$80. Added wall-seat saddles (ICP-11–14): +$575. Excl. fabrication, fasteners, and optional electric actuation.

---

## 5. Print Washing — Water System
*Source: `water-system-report.md`*

### Water storage
| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| [IBC tote 275 gal, food-grade, used/rinsed](https://containerexchanger.com/geo-sale-ads/us-ca/bulk-containers/ibc-totes-for-sale) | **1219×1016×1,168mm** caged composite, DN50 butterfly valve (S60×6) — Blue (×2), Brown (×1), Waste (×1) | 4 | Container Exchanger | $80–$150 | $320–$600 |
| [2" NPT bulkhead fitting (304 SS)](https://www.mcmaster.com/4464K115) | External drain/fill port, welded through container wall (X1/X3/X4) | 3 | McMaster-Carr | $25–$40 | $75–$120 |
| Reinforcing plate, 6mm A36 steel, 150×150mm | Backing plate for external bulkhead ports (one per fitting) | 3 | Metal Supermarkets SoCal | $8–$12 | $24–$36 |
**Storage subtotal: ~$388–$698**

### IBC stacking frame
*Source: `ibc-stacking-report.md` §3, §9.1. Welded 50×50×3mm RHS **restraint-only** frame (single front portal) for the 2×2 direct-stack — the totes stack cage-on-cage, so there is no load-bearing platform; front retaining bars + Simpson-style wall joist hangers + D-ring lashing restrain them for transport.*

| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| [Mild steel RHS 50×50×3mm, 6 m length](https://www.metalsupermarkets.com/product/mild-steel-square-tube-structural-welded/) | Front-portal uprights + panel-mount rail (50×50×3) + front retaining bars (50×20×3) (A500 Grade B) | 4 | [Metal Supermarkets SoCal](https://www.metalsupermarkets.com/) / [Online Metals](https://www.onlinemetals.com) | $30–$45 | $120–$180 |
| [Steel plate 12mm, 150×150mm cut](https://www.onlinemetals.com/en/buy/carbon-steel) | Upright floor flange feet | 2 | Metal Supermarkets SoCal / Online Metals | $4–$8 | $10–$20 |
| Steel folded plate 4mm | Simpson-style wall joist hangers | 4 | Metal Supermarkets SoCal / [Simpson Strong-Tie](https://www.strongtie.com/) | $7–$12 | $30–$50 |
| [Steel plate 8mm, 100×135mm cut](https://www.onlinemetals.com/en/buy/carbon-steel) | Exterior wall backing plates (load-spread, hex heads outside the container wall) | 4 | Metal Supermarkets SoCal / Online Metals | $4–$8 | $16–$32 |
| [Welded D-ring, 25mm, 1,100 kg WLL](https://www.mcmaster.com/3641T29) | Lashing holders on the front bars, 6mm mount plates | 4 | McMaster-Carr #3641T29 | $5–$8 | $20–$35 |
| [Ratchet strap, 25mm, 1,100 kg WLL](https://www.amazon.com/s?k=25mm+ratchet+strap+1100kg) | Transport securing, over each stack | 4 | Amazon / Harbor Freight | $8–$13 | $30–$50 |
| [M12 wedge/sleeve floor anchor](https://www.mcmaster.com/concrete-anchors) | Upright flange feet, 4 each into container floor | 8 | McMaster-Carr / Home Depot | $2–$3 | $15–$30 |
| [M12×80 hex bolt, Grade 8.8 + washer + nut](https://www.mcmaster.com/91290A655) | Wall-hanger through-bolts to the exterior backing plates, 4 each × 4 hangers | 16 | McMaster-Carr / Fastenal | $1.50–$2.50 | $24–$40 |
| [M12×40 hex bolt, Grade 8.8 + nut/washer](https://www.mcmaster.com/91290A655) | Front-bar-to-upright cleats | 8 | McMaster-Carr / Fastenal | $1–$2 | $8–$16 |
| Welding / fabrication | ~14–20 hrs (single front portal — far less than the old load-bearing rack) | 1 | Local fab shop | $650–$950 | $650–$950 |
| Primer + flat-black powder coat | Anti-corrosion finish | 1 | Local | $30–$50 | $30–$50 |
**IBC stacking frame subtotal: ~$955–$1,455**

### Pumps
| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| [Shurflo 2088-554-144 pump](https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C) | **216×127×114mm**, 12VDC, 3.5 GPM, 45 PSI, ½" NPSM ports (P-01, P-02, P-04 manifold + P-03 IBC corridor) | 4 | Amazon | $55–$70 | $220–$280 |
| [SeaFlo pressure accumulator](https://www.amazon.com/Seaflo-Accumulator-Control-Internal-Bladder/dp/B01MUYL8F8) | **~200×127×125mm**, 0.75 L (23.5 oz), 125 PSI, ½" MNPT | 1 | Amazon | $25–$45 | $35 |
| [Shurflo pump mounting bracket](https://www.amazon.com/s?k=shurflo+2088+mounting+bracket+stainless) | Stainless, for 2088 series (3× manifold + 1× IBC corridor for P-03) | 4 | Amazon | $8–$12 | $32–$48 |
**Pump subtotal: ~$167–$203**

### Filter unit
| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| [3-stage Big Blue combo filter **4.5"×10"**](https://www.amazon.com/s?k=3+stage+10+inch+big+blue+whole+house+water+filter) | **Ø184 × 333mm per housing**, 1" NPT ports, integrated bracket (e.g. Express Water / Geekpure / iSpring 10" 3-stage). *Was 4.5"×20" — switched to 10" to match the modeled BB_OD=184/BB_H=340; see [dimension audit](component-dimension-audit.md). NB: 10" cartridges hold ~½ the media → ~½ the service interval vs 20"* | 1 | Amazon | $200–$300 | $200–$300 |
| [MPP 5-micron sediment cartridge 4.5"×10"](https://www.amazon.com/s?k=4.5x10+melt+blown+polypropylene+sediment+filter+5+micron) | Melt-blown polypropylene depth filter (F-1 stage) | 3 + spares | Amazon | $6–$10 | $18–$30 |
| [KDF-55 heavy metal cartridge 4.5"×10"](https://www.amazon.com/s?k=4.5x10+KDF+55+heavy+metal+water+filter) | KDF-55 media for dissolved iron removal (F-2 stage) | 2 + spares | Amazon | $20–$35 | $40–$70 |
| [CTO carbon block cartridge 4.5"×10"](https://www.amazon.com/s?k=4.5x10+CTO+coconut+shell+carbon+block+filter) | Coconut shell activated carbon block (F-3 stage) | 3 + spares | Amazon | $8–$15 | $24–$45 |
**Filter subtotal: ~$282–$445** *(was ~$470–$652 for 4.5"×20"; folded into the re-summed category-5 + grand totals with the evap-cooler resolution — see [cost breakdown](project-cost-breakdown.md))*

### Valves, fittings & pipe
| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| [Banjo V050FP ball valve 1/2" FNPT](https://www.amazon.com/s?k=banjo+1%2F2+inch+ball+valve+polypropylene) | Polypropylene, full-port, quarter-turn. BV-01, BV-02, plus spares | 4 | Amazon | $6–$10 | $24–$40 |
| [Banjo V100FP ball valve 1" FNPT](https://www.amazon.com/s?k=Banjo+V100FP+polypropylene+ball+valve) | Polypropylene, full-port, quarter-turn. V1/V3/V4, VB1–VB3 (IBC fill/drain valves) | 6 | Amazon | $10–$16 | $60–$96 |
| [Banjo V075FP ball valve 3/4" FNPT](https://www.amazon.com/s?k=Banjo+V075FP+polypropylene+ball+valve) | Polypropylene, full-port, quarter-turn. BV-06 (chemistry tap shut-off) | 1 | Amazon | $8–$12 | $8–$12 |
| [3-way diverter valve 1/2" FNPT](https://www.amazon.com/s?k=1%2F2+inch+3+way+ball+valve+NPT) | L-port or T-port, HDPE compatible. 3W-DV-02 (tray drain) | 1 | Amazon | $12–$22 | $12–$22 |
| [3-way diverter valve 1" FNPT](https://www.amazon.com/s?k=1+inch+3+way+ball+valve+NPT) | L-port or T-port, HDPE compatible. 3W-DV-01 (filter output) | 1 | Amazon | $18–$30 | $18–$30 |
| [2" polypropylene camlock pairs (M+F)](https://www.amazon.com/s?k=2+inch+polypropylene+camlock+fitting+pair) | For external bulkhead connections (X1/X3/X4 + spare) | 4 pairs | Amazon | $5–$8/pair | $20–$32 |
| [1/2" NPT 90° elbow polypropylene](https://www.amazon.com/s?k=1%2F2+NPT+90+elbow+polypropylene) | All pump-driven run bends (manifold internal + external runs) | 14 | Amazon | $2–$4 | $28–$56 |
| [Banjo EL100-90 elbow 1" NPT](https://www.amazon.com/Banjo-EL100-90-Polypropylene-Fitting-Schedule/dp/B00AB5XSZ8) | Polypropylene 90° elbow. IBC fill/drain bends, filter outlet to DV-01 | 4 | Amazon | $3–$5 | $12–$20 |
| [1/2" NPT polypropylene tee](https://www.amazon.com/s?k=1%2F2+NPT+tee+polypropylene) | Blue suction/discharge tees, system branches | 6 | Amazon | $2–$4 | $12–$24 |
| [Banjo TEE100 equal tee 1" NPT](https://www.amazon.com/s?k=Banjo+TEE100+polypropylene+tee+1+inch) | Polypropylene. IBC fill/drain tees | 4 | Amazon | $4–$6 | $16–$24 |
| [1/2" NPT polypropylene union](https://www.amazon.com/s?k=1%2F2+inch+NPT+polypropylene+union) | Maintenance disconnects on pump runs | 6 | Amazon | $4–$6 | $24–$36 |
| [1/2"×1" NPT bushing reducer](https://www.amazon.com/s?k=1%2F2+inch+to+1+inch+NPT+bushing+reducer+polypropylene) | P-02 riser to F1 filter inlet | 1 | Amazon | $3–$5 | $3–$5 |
| [S60×6 to 1" NPT adapter](https://www.amazon.com/s?k=IBC+S60x6+1+NPT+adapter) | IBC DN50 valve to 1" HDPE pipe | 8 | Amazon | $8–$15 | $64–$120 |
| [1" NPT spring check valve](https://www.amazon.com/s?k=1+inch+NPT+spring+check+valve+PVC) (CV1/CV3/CV4) | Non-return valve, PVC body, EPDM seal | 3 | Amazon | $8–$14 | $24–$42 |
| PTFE thread seal tape | ½" wide, 260" roll | 4 | Home Depot | $2 | $8 |
| [1/2" SDR-11 HDPE pipe](https://www.ferguson.com) | All pump-driven runs (IBC to manifold, manifold to spray bar, tray drain, DV outputs). 20ft sticks | 4 sticks | Ferguson | $6–$10/stick | $24–$40 |
| [1" SDR-11 HDPE pipe](https://www.ferguson.com) | Food-safe, blue-stripe, 20ft stick. Filter outlet to DV-01 and IBC fill/drain lines only | 1 stick | Ferguson | $12–$18/stick | $12–$18 |
| [Banjo TEE100 equal tee, 1" HDPE NPT](https://www.amazon.com/s?k=Banjo+TEE100+polypropylene+tee+1+inch) | X1 fill tee — splits the fill to both Blue totes (replaces the 2" cross-connect) | 1 | Amazon | $4–$6 | $4–$6 |
| [¾" SDR-11 HDPE pipe](https://www.ferguson.com) | Spray bar run, 20ft sticks | 2 sticks | Ferguson | $9–$14/stick | $20–$30 |
| [½" ID reinforced braided PVC hose](https://www.amazon.com/s?k=1%2F2+inch+reinforced+braided+PVC+hose+6+ft) | Pump inlet flexible connection, 6ft per pump | 2 lengths | Amazon | $8–$12/length | $20 |
| [1" polypropylene camlock (Type E)](https://www.amazon.com/s?k=1+inch+polypropylene+camlock+type+E) | Quick-disconnect at IBC and pipe stubs | 4 pairs | Amazon | $5–$8/pair | $20–$32 |
| [18mm marine plywood offcut (~0.4 m²)](https://www.homedepot.com/b/Lumber-Composites-Plywood-Marine-Plywood/N-5yc1vZc6ad) | Drain-riser backing spine + capped top shelf — teed off the equipment panel; mounts the X3/X4 risers and supports the Blue fill trunk in the corridor | 1 | Home Depot / local lumber | $12–$20 | $12–$20 |
| [SS 2-hole pipe straps / cushioned P-clips, ½"–¾"](https://www.mcmaster.com/products/pipe-clamps/) | Clamp the X3/X4 drain risers (~400mm centers) + the Blue fill trunk on the top shelf (+ SS screws) | 11 | McMaster-Carr | $1–$2 each | $12–$22 |
**Valves, fittings & pipe subtotal: ~$526–$857**

### Processing tray
| Item | Spec | Qty | Supplier | Unit price | Est. cost |
|------|------|-----|----------|-----------|-----------|
| [304 SS sheet, 16-ga (1.5mm)](https://www.onlinemetals.com/en/buy/stainless-steel/304-stainless-steel-sheet) | #4 brushed, 4'×8' sheets | 4 | Online Metals | $180–$250/sheet | $720–$1,000 |
| Fabrication (cut, brake, weld, press sump) | Two tray halves: 2229×2,200mm, 50mm rims, pressed sump well (150×100×20mm) | 1 job | Local sheet metal shop | $450–$850 | $450–$850 |
| [HDPE flat bar 50×10mm](https://www.mcmaster.com/8619K451) | Tapered shim strips for slope support, 2,200mm long | 5 | McMaster-Carr / TAP Plastics | $8–$15 each | $40–$75 |
| [1" SS foot valve with strainer](https://www.amazon.com/s?k=1+inch+stainless+foot+valve+strainer) | Sump pickup, prevents debris, maintains prime | 1 | Amazon | $15–$25 | $20 |
| [1" reinforced suction hose, 6 ft](https://www.amazon.com/s?k=1+inch+reinforced+suction+hose+6+ft) | P-04 suction from sump pickup over tray rim to pump manifold | 1 | Amazon | $12–$20 | $15 |
| [Silicone gasket strip, FDA grade](https://www.mcmaster.com/1460N14) | 1/16" × 1" × 10 ft, center flange seal | 1 roll | McMaster-Carr | $15–$25 | $20 |
| [M6×16 SS hex bolts + flange nuts](https://www.mcmaster.com/92196A150) | Center flange, 200mm spacing | 24 | McMaster-Carr | $0.50 each | $12 |
**Processing tray subtotal: ~<!-- BEGIN costing:tray-low -->$1,300<!-- END costing:tray-low -->–<!-- BEGIN costing:tray-high -->$2,015<!-- END costing:tray-high -->** — canonical figure from the [Processing Tray & Spray Bar report](processing-tray-and-spray-bar.md) §6.1; rows above are the procurement detail.

### Spray bar assembly (gantry design)
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [6061-T6 aluminum SHS **40×40×3mm**](https://www.onlinemetals.com/en/buy/aluminum/6061-t6-aluminum-square-tube) | 40×40×3mm structural beam (metric — matches the model + carriage saddle cut; was mislabeled "1½×1½×⅛"), 8 ft lengths (2 joined with sleeve for 3,859mm). 12mm holes drilled for nozzle fittings | 2 | Online Metals | $36–$56 |
| [3/4" LDPE irrigation poly pipe](https://www.amazon.com/s?k=3%2F4+inch+LDPE+irrigation+poly+pipe) | Internal spray pipe (OD 25mm, ID 19mm), 15 ft length | 1 | Home Depot / Amazon | $10 |
| [Flat-fan irrigation spray nozzles, barbed](https://www.amazon.com/s?k=flat+fan+irrigation+spray+nozzle+barbed) | 180° fan pattern, barbed inlet through beam wall (26 @ 150mm pitch) | 26 | Amazon | $30–$50 |
| [Distribution manifold, 1/2" → multi barb](https://www.amazon.com/s?k=irrigation+distribution+manifold+1%2F2+barb) | Mounted at ball joint, splits supply hose to 7 feed tubes | 1 | Amazon | $12 |
| [1/4" irrigation poly tube](https://www.amazon.com/s?k=1%2F4+inch+irrigation+poly+tubing) | Manifold to beam feed points (~7m total) | 1 | Amazon / Home Depot | $6 |
| [Barbed feed fittings, through beam top](https://www.amazon.com/s?k=irrigation+barbed+insert+fitting) | Irrigation tube to poly pipe, 7 feed points (~550mm pitch) | 7 | Amazon | $10 |
| [SS/nylon retainer clips for 3/4" poly pipe](https://www.amazon.com/s?k=retainer+clip+3%2F4+poly+pipe+fold+back) | Fold-back end closures | 2 | Amazon | $4 |
| [6061-T6 aluminum plate 3/16" (5mm)](https://www.onlinemetals.com/en/buy/aluminum/6061-t6-aluminum-sheet-plate) | Carriage plates (5mm, notched to meet beam) + end caps — ~300×500mm sheet | 1 | Online Metals | $12–$20 |
| [30×30mm aluminum solid bar](https://www.onlinemetals.com/en/buy/aluminum/6061-t6-aluminum-square-bar) | Internal splice sleeve, 150mm long | 1 | Online Metals | $8–$12 |
| [SS flat bar, ~3mm](https://www.onlinemetals.com/en/buy/stainless-steel/stainless-steel-flat-bar) | Beam clamp plates (top + bottom) sandwiching the 40mm SHS; 40mm AL offcut spacer beside each beam face | 4 plates | Online Metals / Amazon | $12–$18 |
| [Nylon skate wheel, 50mm×20mm, 10mm bore](https://www.mcmaster.com/products/rollers/skate-wheels-1~/) | Carriage wheels, flat tread, ≥25 kg rated (2 per carriage) | 4 | McMaster-Carr | $12–$20 |
| [Telescoping aluminum pool pole](https://www.amazon.com/s?k=telescoping+aluminum+pool+pole+8+ft) | 4–8 ft push handle | 1 | Amazon / Home Depot | $15 |
| [½" reinforced braided PVC hose, 15 ft](https://www.amazon.com/s?k=1%2F2+inch+reinforced+braided+PVC+hose+15+ft) | Flexible connection BV-02 to the distribution manifold | 1 | Amazon | $15 |
| [M5×16 SS hex bolt + nyloc nut + washers](https://www.mcmaster.com/91292A126) | Axle saddle-clamp through-bolts (2 per saddle, 8 saddles) | 16 sets | McMaster-Carr | $12 |
| [20mm ball joint, SS ball + zinc socket](https://www.amazon.com/s?k=20mm+ball+joint+stud+zinc+socket) | Multi-axis arm articulation on beam top face. Ø36mm socket, 50mm flange base, M12 stud | 1 | Amazon / McMaster | $8–$15 |
| [Self-tapping SS screws, thread-forming (8-pack)](https://www.amazon.com/s?k=stainless+self+tapping+screws) | Fasten ball-joint flange to the 3mm SHS beam top wall (no internal access for nuts) | 4 | Amazon / McMaster-Carr | $3–$5 |
| [25mm OD × 2mm wall 6061-T6 AL round tube](https://www.onlinemetals.com/en/buy/aluminum/6061-t6-aluminum-round-tube) | Vertical arm tube, ~500mm long, clamped to ball joint stud | 1 | Online Metals | $5–$8 |
| M6×25 SS hex bolt + nut | Pinch bolt — clamps arm tube onto ball joint stud | 1 | McMaster-Carr | $1 |
| [½" barb × ½" hose barb, brass](https://www.amazon.com/s?k=1%2F2+hose+barb+brass) | Flex hose to manifold inlet | 1 | Amazon | $4 |
| [10mm × 60mm 304 SS axle pin (4-pack)](https://www.amazon.com/uxcell-Single-Hole-Clevis-Pins/dp/B0816MQ5T6) | Wheel axle pins, flat head | 4 (1 pack) | Amazon | $4–$8 |
| [304 SS saddle clamp, 10mm (10-pack)](https://www.amazon.com/Boxonly-Fixing-Stainless-Saddle-Tension/dp/B0CG1CNQKX) | Curved conduit-style axle retention — bolted to carriage plate underside, cradles axle pin | 8 | Amazon | $8–$12 |
| SS spring clip / pole attachment | Pole-to-arm quick-release clip | 1 | Amazon | $6 |
| [Cable ties, 200mm, nylon](https://www.amazon.com/s?k=cable+ties+200mm+nylon) | Secure flex hose to arm tube | 1 pack | Amazon | $5 |
**Spray bar subtotal: ~<!-- BEGIN costing:spray-low -->$235<!-- END costing:spray-low -->–<!-- BEGIN costing:spray-high -->$299<!-- END costing:spray-high -->** — canonical figure from the [Processing Tray & Spray Bar report](processing-tray-and-spray-bar.md) §6.2; rows above are the procurement detail.

### Water system processing consumables
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [Apera Instruments AI311 PH60 pH meter](https://www.amazon.com/Apera-Instruments-AI311-Replaceable-2-00-16-00/dp/B01ENFOIQE) | Waterproof, 0–16, ±0.01 accuracy | 1 | Amazon | $45–$65 |
| [pH calibration solution set](https://www.amazon.com/s?k=pH+calibration+buffer+solution+4+7+sachet) | pH 4 + pH 7 buffer sachets | 1 set | Amazon | $10 |
| [Citric acid, food grade, 5 lb](https://www.amazon.com/s?k=citric+acid+food+grade+5+lb) | pH adjustment (acidifier) | 2 bags | Amazon | $28 |
| [Chemical-resistant GHS labels](https://www.amazon.com/s?k=GHS+chemical+resistant+labels) | For IBC totes | 1 pack | Amazon | $20 |
| Funnel with filter screen 2" | For IBC filling | 2 | Amazon | $18 |

| Containment liner, 6-mil black LDPE | 20' × 10' sheet — secondary spill containment under IBCs and filter skid | 4 | Amazon | $18–$28/sheet | $75–$110 |
**Water consumables subtotal: ~$205–$240**

**Section total: $4,063–$6,104**

## 6. Electrical — Power, Circuits & Wiring
*Source: `electrical-report.md`*

### Solar & battery (primary power)
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [Solar panels, 200W monocrystalline](https://www.renogy.com/200-watt-12-volt-monocrystalline-solar-panel/) | 12V nominal | 3 | [Renogy](https://www.renogy.com) | ~$400 total |
| [Victron SmartSolar MPPT 100/50](https://www.altestore.com) | MPPT charge controller | 1 | [altE Store](https://www.altestore.com) | ~$200 |
| [LiFePO4 battery 100Ah 12V](https://www.renogy.com/12v-100ah-smart-lithium-iron-phosphate-battery/) | Renogy Smart Lithium or Battle Born, **each 330×172×214mm**. **1 standard**; busbar provisioned for a 2nd in parallel (plug-in, no rewiring — see [Electrical Report §5.2](electrical-report.md)) | 1 | [Renogy](https://www.renogy.com) | ~$350 (+$350 optional 2nd) |
| [Victron Blue Smart IP65 12/15](https://www.altestore.com) | Shore backup charger | 1 | [altE Store](https://www.altestore.com) | ~$150 |
| NEMA 5-15R inlet (weatherproof) | Mounted in flush-mount power panel | 1 | Amazon | ~$25 |
| [Solar panel ground mount frame](https://www.renogy.com) | Tilt frame, 30° | 1 | [Renogy](https://www.renogy.com) | ~$80 |
| PV cable 10 AWG | MC4 connectors | 1 lot | Amazon | ~$30 |
| Aluminum plate 340×240×3mm | Flush-mount face plate, power panel | 1 | [Online Metals](https://www.onlinemetals.com) | ~$18 |
| Neoprene gasket 340×240×3mm | Weatherseal between plate and wall | 1 | McMaster-Carr | ~$6 |
| M6 bolt + nut + washer set | Panel mounting hardware, SS | 4 | McMaster-Carr | ~$5 |
| [MC4 bulkhead connector pairs](https://www.amazon.com/s?k=MC4+bulkhead+connector+panel+mount+IP67) | IP67 panel-mount | 3 pairs | Amazon | ~$25 |
| Panel cooler output | 120V AC — now a **GFCI outlet** (Circuit E); counted in the Evaporative cooler section (was a DC Deutsch bulkhead) | — | — | (see cooling) |
**Solar & battery subtotal: ~$1,295**  *(1-pack standard; +$350 for the optional 2nd pack)*

### Distribution & wiring
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [Blue Sea 5026 fuse block](https://www.amazon.com/s?k=Blue+Sea+5026+fuse+block) | 12-circuit ST-blade | 1 | Amazon / [West Marine](https://www.westmarine.com) | ~$55 |
| [200A main fuse — MRBF terminal-mount](https://www.amazon.com/s?k=Blue+Sea+MRBF+terminal+fuse) | On the battery + post (≤180mm from battery, ABYC E-11) | 1 | Amazon | ~$25 |
| [Battery main disconnect switch](https://www.bluesea.com/products/category/8/2/Battery_Switches) | Blue Sea m-Series 300A — manual isolator, contactor to busbar | 1 | [West Marine](https://www.westmarine.com) / Amazon | ~$40 |
| [Remote battery switch (contactor)](https://www.bluesea.com/products/category/8/2/Battery_Switches) | Blue Sea ML-RBS 500A magnetic-latch — in battery + feed, tripped by the external E-stop | 1 | [West Marine](https://www.westmarine.com) / Amazon | ~$150 |
| [External emergency cut-off (E-stop)](https://www.automationdirect.com/) | Red mushroom push-button, IP66, panel-mount on the external power panel + 2× 18 AWG control loop | 1 | [AutomationDirect](https://www.automationdirect.com/) / Amazon | ~$30 |
| Battery terminal covers (pair) | Insulating boots over + / − posts | 1 | Amazon | ~$10 |
| [Sealed wet-zone connectors](https://www.waytekwire.com) | Deutsch DT / adhesive-lined heat-shrink — pump circuits in the IBC corridor / tray end | 1 lot | [Waytek Wire](https://www.waytekwire.com) | ~$25 |
| [Pump switches (Circuit C)](https://www.amazon.com/s?k=IP67+rocker+switch+12V+16A) | IP67 sealed rocker, 12V 16A — one per pump (P-01–P-05), panel-face | 5 | Amazon / Waytek Wire | ~$30 |
| [Pump distribution block](https://www.amazon.com/s?k=12V+bus+bar+distribution+block) | 12V DC + bus + negative bus (6-way), panel-mount, equipment panel | 1 | Blue Sea / Amazon | ~$15 |
| Dielectric grease | Marine-grade — chemistry-vapor terminal protection | 1 | Amazon | ~$10 |
| Tinned marine wire (wet-zone runs) | 14/16 AWG tinned copper, ~25ft | 1 | [Waytek Wire](https://www.waytekwire.com) | ~$30 |
| Cable grommets / glands | Steel-shell penetrations (chafe protection) | 1 lot | McMaster-Carr | ~$15 |
| Equipotential bonding kit | 6 AWG green/yellow + ring lugs — IBC frame / walkway / tray-metal to battery-negative | 1 | Amazon | ~$20 |
| [IP65 enclosure 300×200×130mm](https://www.amazon.com/s?k=IP65+enclosure+300x200+junction+box) | Houses fuse block + MPPT | 1 | Amazon | ~$60 |
| Wiring kit — 12/14/16/18 AWG | 50ft each color, tinned copper | 1 kit | [Waytek Wire](https://www.waytekwire.com) / Amazon | ~$80 |
| 2/0 AWG cable | Battery–fuse–busbar, 3ft | 1 lot | Amazon | ~$30 |
| [Anderson Powerpole connectors 30A](https://powerwerx.com/anderson-powerpole-connectors) | 50 pairs | 1 kit | [Powerwerx](https://powerwerx.com) | ~$40 |
| [Deutsch DT connectors 2-pin](https://www.waytekwire.com) | Exterior penetrations, IP67 | 10 sets | [Waytek Wire](https://www.waytekwire.com) | ~$30 |
| 40×25mm PVC cable trunking | 5m lengths | 4 | McMaster-Carr | ~$40 |
| [10mm corrugated conduit](https://www.mcmaster.com/7828K48) | Drop conduits to devices | 10m | McMaster-Carr #7828K48 | ~$30 |
| [Brady M210 wire label kit](https://www.amazon.com/s?k=Brady+M210+label+printer+wire) | Wire label cartridge | 1 | Amazon | ~$80 |
| [12V LED flat panel 300×600mm](https://www.amazon.com/s?k=12V+LED+flat+panel+300x600+4000K) | 20W neutral white, ceiling-mount | 3 | Amazon | ~$75 total |
| Pull-cord ceiling switch, 12V 6A SPST | Inline switch for lighting Ccts D & G | 2 | Amazon | ~$16 total |
| Copper ground stake 8ft × ⅝" dia | Earth connection | 1 | Home Depot | ~$20 |
| 4 AWG ground wire, green/yellow | 3m | 1 | Amazon | ~$15 |
**Distribution & wiring subtotal: ~$970**  *(+$325 circuit-protection / wet-zone-sealing hardware — external emergency cut-off + battery contactor, disconnect, terminal fuse, sealed connectors, bonding; see [Electrical Safety Report](electrical-safety-report.md) §5; +$45 Circuit-C pump-control — 5 switches + distribution block)*

**Section total: ~$2,265**  *(= Solar & battery $1,295 + Distribution & wiring $970; 1-pack standard, +$350 for the optional 2nd pack)*

## 7. Housed Revolving-Door Light Lock — Custom Fabrication
*Source: `light-trap-selection.md` § 4 (rev 9 / B2). Custom-fabricated Ø900 fixed housing + single-opening C-shell drum (no fins) built into the hinged cargo-door panel — light-tight by geometry. **rev 9 switches the drum/housing from 3mm aluminum to a hybrid plastic skin (5mm UV-HDPE housing, 4mm PP drum)** — cutting the drum/housing mass (~99 kg → ~60 kg), removing galvanic concerns, and lowering fabrication cost. Replaces the failed Ø750 4-fin drum. Single-operator entry/exit at any time without admitting daylight.*

### Housing + drum body
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 5mm UV-stabilized HDPE sheet (black) | Ø900 fixed housing shell — LT_HOUSING_T (rolled + extrusion-welded, ~7 m²) | ~7 m² | [TAP Plastics (SoCal)](https://www.tapplastics.com/) / Online Metals plastics | ~$180–$280 |
| 4mm black polypropylene sheet | Ø864 drum shell + top/bottom caps + opening edge stiffeners — LT_DRUM_T (~7 m²) | ~7 m² | TAP Plastics / Curbell Plastics (SoCal) | ~$150–$240 |
| 75mm Ø solid round bar, cut to 150mm | Upper and lower stub shafts (×2) | 2 pieces | Pacific Coast Steel or any steel service center | ~$30 |

### Bearings
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [SKF 6215-2RS1 sealed deep-groove ball bearing](https://www.amazon.com/s?k=SKF+6215-2RS1+bearing) | 75mm ID × 130mm OD × 25mm wide, C3 clearance | 2 | Amazon / Bearing World (Anaheim CA) | ~$45–$65 each → ~$90–$130 |
| [Circlip for 75mm shaft](https://www.mcmaster.com/98541A113) | DIN 471, shaft circlip | 4 | McMaster-Carr #98541A113 | ~$10 |

### Seals
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [12mm closed-cell neoprene wiper strip](https://www.mcmaster.com/93855K6) | PSA-backed, drum cap + top/bottom housing wiper seals; 3m | 1 pack (3m) | McMaster-Carr #93855K6 | ~$22 |
| [Nylon/felt brush wiper strip](https://www.mcmaster.com/brush-seal-strip) | Drum↔housing rotating seal at the two opening edges (full height ×2) | ~5m | McMaster-Carr | ~$40 |
| [20mm neoprene compression strip](https://www.mcmaster.com/8635K31) | PSA-backed, drum-to-panel gap seal | 2.4m | McMaster-Carr #8635K31 | ~$20 |
| [Black UV-stable silicone sealant](https://www.mcmaster.com/7587A3) | Bead seal at top and bottom mount plates | 2 tubes | McMaster-Carr #7587A3 | ~$18 |

### Hardware
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [SS round grab rail, 100mm Ø × 400mm](https://www.mcmaster.com/4530T37) | Interior face only, welded bracket | 1 | McMaster-Carr #4530T37 | ~$20 |
| M10 × 40mm hex bolt, stainless + flat washer | Lower bearing collar — 8 off | 1 lot | McMaster-Carr | ~$20 |
| M10 × 35mm hex bolt, stainless + flat washer | Upper bearing housing — 6 off | 1 lot | McMaster-Carr | ~$15 |
| Nylon isolation washers + stainless fasteners | Steel shaft/bearing ↔ plastic shell joints (plastic↔plastic elsewhere — no galvanic couple) | 1 lot | McMaster-Carr | ~$25–$40 |

### Surface treatment
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Matte-black interior finish | Black-pigmented sheet (no etch-prime); scuff + flat-black touch-in at extrusion welds | 1 job | Rattle-can / local shop | ~$40–$70 |

### Fabrication labor
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Plastic fabrication — roll 2 cylinders (housing + drum), hot-air / extrusion weld, cap/shaft fit, bearing fit | 16–22 hrs at local plastic fab shop | 1 job | Local plastic fabrication shop (SoCal) — get 2–3 quotes | ~$800–$1,150 |
**Section total: ~$1,465–$2,160**

*Note: This is for the drum body only. The hinged panel that the drum mounts into (50×50mm RHS frame, 4mm PP plastic skins (18mm-ply Fan-B mount band), EPDM perimeter gasket) is covered in § 2 (Interior Conversion) above. See [light-trap-selection.md](light-trap-selection.md) for full specification and supplier notes.*

## 7a. Panel Swing Pivot
*Source: `equipment-layout-report.md` § 6.1, `hinged-panel-report.md` § 4–5. Enables transport mode: the panel + drum SWING ~56° about a vertical Ø89×8mm CHS pivot post (rev10 — supersedes the B2 slide), carrying the punch-out bay inboard of the door plane (true min X +<!-- BEGIN fact:swung_door_clearance_mm -->59<!-- END fact:swung_door_clearance_mm -->mm) so the cargo doors close. Single-person operation (~5 min, swing assisted; strike the two left film rails + the left walkway first, then swing).*

### Swing pivot system

*Firmed BOM (Stage 4, 2026-06-10). Structural member check DONE: the Ø89×8 post gives
Z ≈ 37.9 cm³, so the ~3.6 kN·m swing cantilever puts σ ≈ 95 MPa on an S355 (355 MPa)
section → **SF ≈ 3.7** (matches `hinged-panel-report.md` §4.1). The journal couple is
H = M/h = 3.6 kN·m / 2.2 m ≈ 1.6 kN per bearing → sleeve bearing pressure ≈ 0.37 MPa «
14 MPa allowable for SAE 841 bronze. **Remaining sign-off: the post-to-container
top/bottom weld + anchor connection** (fabricator/PE review) — not the member itself.*

| Item | Spec | Qty | Suppliers (A / B) + part # | Est. cost |
|------|------|-----|----------------------------|-----------|
| Pivot post — 3.5″ OD × 0.375″ wall DOM tube, ~2,300mm | A513 DOM (≈Ø89×9.5, **exceeds** the Ø89×8 S355 spec); upgrades the reused film far-left upright; carries the ~3.6 kN·m swing cantilever (SF 3.7) | 1 | [Online Metals #12976](https://www.onlinemetals.com/en/buy/carbon-steel/3-5-od-x-0-375-wall-x-2-75-id-carbon-steel-round-tube-a513-type-5-dom/pid/12976) / [Metals Depot DOM](https://www.metalsdepot.com/steel-products/steel-round-tube-dom) · Metal Supermarkets SoCal (cut-to-size) | ~$110 |
| Turntable thrust bearing — 12″ (Ø305), 1000 lb | Axial only at the post base — carries the ~330 kg (3.24 kN) vertical load; the overturning moment is taken by the journal couple, so a thrust-only turntable suffices | 1 | [VXB Lazy-Susan 1000 lb, USA](https://vxb.com/products/12inch-lazy-susan-5-16-thick-turntable-bearings-made-in-usa-1000-lbs-capacity) / [Shepherd 9549E](https://www.shepherdhardware.com/product/12-inch-lazy-susan-round-turntable-1000-lb-load-capacity) | ~$40 |
| Flanged sleeve (journal) bearing — 3½″ (89mm) bore | SAE 841 bronze (oil-embedded); top + bottom radial location of hub on post; 1.6 kN radial each | 2 | [McMaster-Carr 6391K-series](https://www.mcmaster.com/sleeve-bearings/) / [Grainger](https://www.grainger.com/category/power-transmission/bearings/sleeve-bearings) | ~$100 |
| Pivot hub + thrust collar, machined steel | Couples the swinging frame to the post; bores Ø89 for the sleeves + seats the turntable; includes machining the post bearing landings | 1 | Local fab (SoCal machine shop) | ~$160 |
| Drum support cage — [40×40×3mm SHS](https://www.metalsupermarkets.com/product/square-tube/) (~4m) | Steel frame carrying the Ø900 housing + drum on the swinging leaf | 1 | Metal Supermarkets SoCal / local fab | ~$90 |
| Top + bottom **wall stays** (transport lock) | [M16 turnbuckle](https://www.mcmaster.com/turnbuckles/) (eye-eye) + [eye bolt](https://www.mcmaster.com/eyebolts/) + hook rod, each | 2 | [McMaster-Carr 3411T-series](https://www.mcmaster.com/turnbuckles/) / [Grainger](https://www.grainger.com/category/material-handling/rigging/turnbuckles) | ~$90 |
| Wall-stay anchor plates + M16 bolts | Inside + outside 4-bolt plates per stay eye, sandwiching the side wall (same pattern as the walkway anchors) | 2 sets | Local fab / [McMaster-Carr M16](https://www.mcmaster.com/bolts/) | ~$60 |
| Drop-in rail saddles + tapered dowels + clamp bars | Drop-in saddles for the 2 removable left film rails (TL + BL) — the dowels set the film datum on re-seat | 4 | Local fab / McMaster-Carr | ~$120 |
| **Swing pivot subtotal** | | | (firmed — was a ~$770 estimate, now priced line-by-line) | **~$770** |

### Fixed door frame + seals
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 50×50×3mm RHS welded frame | Full door perimeter ~9.5m | 1 | Metal Supermarkets | ~$120 |
| 3mm steel plate/angle, ~110mm × ~4m | Top + bottom seal lips — frame-top downstand (top, continuous full width) + threshold upstand (bottom, full width, no notch — drum rides at Z130); seal paths #3–#4 | 1 | Metal Supermarkets | ~$60 |
| Seal landing machining | Mill flat on all frame faces + the 2 vertical cut-seal landings | 1 | Local fab | ~$80 |
| [EPDM gasket 20×15mm](https://www.mcmaster.com/8635K31) | Perimeter (~9.5m) + 2× vertical **cut seals** at Yd180/2287 (~4.8m) + top/bottom lip strips | 1 | McMaster-Carr #8635K31 | ~$70 |
| Neoprene backup strip, 10×10mm | Self-adhesive, ~9.5m | 1 | McMaster-Carr | ~$22 |
| Fasteners, misc | M10/M12 stainless, assorted | 1 lot | McMaster-Carr | ~$60 |
| Flat black paint | Touch-up, 1 qt | 1 | Home Depot | ~$15 |
| Fan B flex cable (coiled, 16AWG 2-cond, silicone) | 1m coiled, Deutsch DT 2-pin connectors each end — accommodates the ~56° swing | 1 | Waytek Wire / McMaster-Carr | ~$35 |
**Door frame subtotal: ~$462**

**Section total (materials): ~$1,112–$1,372** *(swing pivot + fixed RHS door frame; = cost-breakdown §6b)*
**Fabrication labor: ~12–16 hrs × $80–$100/hr = $960–$1,600**

## 7b. Perimeter Walkway
*Source: `generate_walkway_diagram.py`, `engineering-diagrams.md` §14. Four removable grated walkway sections around the processing tray. Near walkway widens from 300mm to 500mm at EP/battery/slit zone (X≈1,155–2,629). Near/far: wall-cantilevered brackets bolted to corrugated wall ribs. Right (rev12): cantilever rectangle — a closed 40×40 SHS frame on 2 center arms off the IBC corridor uprights, left corners on wall cleats, right corners on combined corner plates shared with the bottom film rail (no floor contact — clears IBC stack entirely). Left: removable lift-out grate on 5 floor-leg cantilever brackets (50×50 post on bare floor + arm to X=470, 3 extended to X=770 on the punch-out). Butt joints at all corners. No tray contact on any section — entire tray interior completely clear for film loading. Deck height 130mm (115mm support + 15mm grate; raised +50 so the support clears the floor-level spray bar).*

### Walkway sections (4 off)
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [Molded GRP (fiberglass) grating, 15mm](https://www.mcnichols.com/fiberglass-grating) | 5/8" (15mm) molded FRP, **vinyl-ester resin, grit top** (corrosion-proof in the chemistry zone; 15mm depth keeps the lowered deck + spray-bar clearance). Cut to size: near 4459×300mm (with 1474×500mm bump-out), far 4459×300mm, right 2362×300mm, left 2362×300mm (removable) | ~4.5 m² | [McNichols](https://www.mcnichols.com) / [Grating Pacific](https://gratingpacific.com) (SoCal) | ~$970–$1,260 |
| Standard wall brackets, 8mm steel plate | Triangular gusset: 150mm vert × 300mm arm, welded. Hot-dip galvanized. | 14 | Local fab / Metal Supermarkets | ~$112–$175 |
| Widened wall brackets, 10mm steel plate | 200mm vert × 500mm arm, 70mm gusset, welded. Hot-dip galvanized. EP/battery/slit zone. | 4 | Local fab / Metal Supermarkets | ~$72–$112 |
| Reinforcing plates, 100×180×6mm mild steel | Welded to exterior wall face behind each standard bracket | 14 | Metal Supermarkets | ~$31–$49 |
| Reinforcing plates, 120×220×6mm mild steel | Wider plates behind each widened bracket (4-bolt pattern) | 4 | Metal Supermarkets | ~$16–$24 |
| M12×60mm hex bolts, nuts, flat washers | Grade 8.8, galvanized. 3 per standard bracket (42) + 4 per widened bracket (16). | 58 | McMaster-Carr | ~$57–$87 |
| Transition bearing plate, 40×500×5mm flat bar | Welded to bracket arm top at width transitions (X≈1,156 and X≈2,526). Both grating widths land on plate. | 2 | Metal Supermarkets | ~$5–$10 |
| Mild steel SHS 40×40×3mm, galvanized | Right walkway CANTILEVER frame (rev12): 2 long beams (2,362mm) + 2 end beams (300mm) + 2 center arms (405mm); order 8m | 8 m | Metal Supermarkets | ~$28–$40 |
| Right walkway wall cleats (left corners, ×2) | 8mm steel — back-plate + exterior plate + shelf the long beam lands on, through-bolted to the wall | 2 | Local fab | ~$20–$35 |
| Combined corner plates (right corners, ×2) | 10mm steel, 150mm-wide — secures BOTH the bottom film rail (BR) AND the walkway right beam (interior + exterior plate + 2 seats). Shared with the film plane: REPLACES the BR rail saddle | 2 | Local fab | ~$50–$80 |
| M12 through-bolts + nuts, flat + lock washers | Wall cleats + combined plates (through-wall) + the 2 center-arm U-clamps to the IBC corridor uprights. Galvanized, grade 8.8. | ~24 | McMaster-Carr | ~$30–$50 |
| [316 SS hold-down clips (M/G-clip, FRP)](https://www.mcnichols.com/fiberglass-grating/) | Stainless hold-down clips clamp the GRP panel to the bracket arm / L-angle (no TEK-into-bar — FRP uses a clamp clip). Near/far/right walkways. | ~20 | [McNichols](https://www.mcnichols.com) | ~$25–$40 |
| Left floor-leg cantilever brackets (×5) | Each = 50×50×3mm steel SHS post (~115mm, floor to grate bottom) + 40×40×3mm SHS arm (2× standard reach to X470, 3× extended to X770 on the drum-exit punch-out) + 128×60×8mm foot plate. Bolted to bare floor outside the tray (X<170); arms pass 15mm over the spray bar. Hot-dip galvanized. | 5 | Metal Supermarkets / local fab | ~$55–$95 |
| [M10 wedge anchors + nuts/washers](https://www.mcmaster.com/) | Galvanized. 4 per foot plate (20 total) — sealed penetrations into the container floor. | 20 | McMaster-Carr | ~$25–$45 |
| Drum-exit punch-out — extra GRP grating (~0.23 m²) | Deeper landing (600mm) at the light-lock exit; carried by the 3 extended bracket arms (to X770) — no separate bearer/leg. | 1 lot | McNichols / Grating Pacific | ~$50–$65 |
| Fabrication + installation | Cut/weld/galvanize 14 std + 4 widened wall brackets, reinforcing plates, drill wall ribs, fabricate + fit the right walkway cantilever frame (clamp 2 center arms to the IBC uprights, bolt wall cleats + combined corner plates), fit 5 left floor-leg cantilever brackets + drill/seal floor anchors, install | 1 job | Local fab / metal shop | ~$290–$455 |
**Walkway subtotal: ~$1,865–$2,650**  *(GRP grating swap: +$720–$890 vs galvanized steel; buys −62 kg + corrosion immunity in the chemistry zone)*

*Near/far grating secured with M saddle clips + TEK screws to bracket arms. Right walkway grating secured with M saddle clips + TEK screws to L-angle bearer horizontal leg. Left walkway uses gravity retention — the grating rests on the floor-leg cantilever arms (5 brackets on bare floor at X=140, arms reaching X=470, three extended to X=770 on the punch-out); lift straight up to remove (no fasteners, no kerb). The brackets are bolted to the floor (permanent); only the grating lifts out for transport. No edge beam, no bearing strip, no tray contact (the +50mm walkway raise lifts the arms clear of the floor-level spray bar). Near walkway widens to 500mm at EP/battery/slit zone (X≈1,155–2,629) with heavier 10mm brackets (see Sheet 7). Slits cut to tray lip only (near: 420mm, far: 218mm), not full walkway depth. Transition bearing plates at width change brackets (X≈1,156 and X≈2,526). Butt joints at all corners. No floor contact on any section — entire tray interior clear.*

## 8. Cooling & Ventilation
*Source: `electrical-report.md`*

### Ventilation fans (upgrade from original 4" spec)
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [150×150×50mm 12V DC axial panel fan](https://www.coolingfanfactory.com/product/DC-Fan-15050-12V-24V-48V-150mm.html) | **150×150×50mm**, 12V DC, ball-bearing, ~150–200 CFM (e.g. GDSTIME / Wathai 15050-12V). *Thin axial PANEL fan — fits flush + inside the 300mm baffle duct (NOT the 320mm-long AC Infinity S6 inline fan; see [dimension audit](component-dimension-audit.md))* | 2 | Amazon | ~$50 total |
| 6" duct stub fittings | Wall penetration collars | 2 | Amazon | ~$20 |
| Fan baffle plates (3mm mild steel) | 2 baffles per fan, offset S-path | 1 lot | Metal Supermarkets | ~$40 |
**Ventilation subtotal: ~$110** *(fan corrected to a real 150×150×50 axial panel fan; folded into the re-summed grand totals with the evap-cooler resolution — see [cost breakdown](project-cost-breakdown.md))*

### Shade canopy
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 80% shade cloth 20×10ft | UV-stabilized, over container roof | 1 | Amazon / Farm supply | ~$80 |
| Canopy frame | 1.5" EMT conduit + T-fittings | 1 lot | Home Depot | ~$120 |
**Shade canopy subtotal: ~$200**

### Evaporative cooler (+ inverter)
*Resolves the parked evap cooler ([dimension audit](component-dimension-audit.md)): a commodity 120V AC swamp cooler on a dedicated 12V→120V inverter, instead of the fictional "Portacool Jetstream 110 12V DC". AC isolation/GFCI/bonding per [Electrical Report §7.6](electrical-report.md#ac-safety).*

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [Evaporative cooler — Hessaire MC18M](https://hessaire.com/mobile-cooling/1300-cfm-mobile-cooler) | 120V AC, <!-- BEGIN fact:evap_cooler_w_ac -->85<!-- END fact:evap_cooler_w_ac -->W, 1300 CFM (run on **low** for the Ø200 duct), 16 lb, 559×305×711mm, 4.8 gal | 1 | [Hessaire](https://hessaire.com/mobile-cooling/1300-cfm-mobile-cooler) / Amazon | ~$130 |
| [Cooler inverter — Victron Phoenix 12/375 GFCI](https://www.victronenergy.com/inverters/phoenix-inverter-vedirect-250va-800va) | 12V→120V pure-sine, **built-in GFCI**, factory bonded neutral, 0.9W idle (Circuit E) | 1 | [Victron](https://www.victronenergy.com/inverters/phoenix-inverter-vedirect-250va-800va) / Amazon | ~$210 |
| Inverter DC protection | 40A ANL fuse + holder + DC disconnect switch (inverter feed) | 1 | Blue Sea / Amazon | ~$40 |
| Panel GFCI AC outlet | Weatherproof NEMA 5-15R + in-use (bubble) cover (Circuit E panel outlet) | 1 | Leviton / Amazon | ~$25 |
| Ø200mm insulated flex duct | ~1.2m, aluminum foil jacket, cooler to wall stub | 1 | [Home Depot](https://www.homedepot.com/s/8%20inch%20insulated%20flex%20duct) / McMaster-Carr | ~$22 |
| Ø200mm (8") 90° duct elbow | Galvanized — vertical riser off cooler to horizontal wall entry | 1 | [Home Depot](https://www.homedepot.com/s/8%20inch%20duct%20elbow) | ~$14 |
| Ø200mm duct collar + hose clamp | Galvanized, wall stub coupling | 1 | [Home Depot](https://www.homedepot.com/s/8%20inch%20duct%20collar) | ~$12 |
| Ø200mm weatherproof duct cap | Removable, protects wall stub when cooler disconnected | 1 | [Home Depot](https://www.homedepot.com/s/8%20inch%20duct%20cap) | ~$8 |
| 200mm baffle duct + plates | Light-safe baffled intake, 300mm stub, 2× offset baffles | 1 lot | McMaster-Carr / local fab | ~$20 |
| Cooler power cord | 1.5m outdoor SJOOW, NEMA 5-15P each end (panel outlet → cooler) | 1 | Amazon | ~$20 |
| 25mm ratchet strap, 2m | Cooler transport stowage on near walkway | 2 | Amazon / Harbor Freight | ~$10 |
| 12mm plywood base plate 559×305mm | Load distribution on walkway grating | 1 | Offcut / local | ~$5 |
| 25×25×3mm Al angle cleats, 100mm | Anti-slide cleats screwed to base plate | 2 | Metal Supermarkets / online | ~$4 |
**Cooler + inverter subtotal: ~$520**

**Section total: ~$824–$974** *(ventilation $110 + shade $200 + cooler/inverter $520; = cost-breakdown §5b)*
*Note: fans wired to Circuits A & B (DC); the cooler runs from the interior inverter (Circuit E) → GFCI panel outlet → outdoor cord. The cooler subsystem (cooler + inverter + DC protection + AC outlet) is the only 120V AC branch — see [Electrical Report §7.6](electrical-report.md#ac-safety).*

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