<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# TBS-001 — Master Shopping List

**Camera:** The Big Shoebox Project — TBS-001
**Basis:** April 2026. All prices USD. Prices marked † confirmed from supplier listings; others are close estimates.
**Process assumed:** Cyanotype (lowest cost, no hazmat, no silver). See `chemistry-shopping-list.md` for alternative process costs.
**Power assumed:** 12V DC off-grid solar + LiFePO4. See `electrical-report.md` for full architecture.

Items are grouped by build area. Source documents are cross-referenced in each section header.

## Summary — Estimated Total
| Area | Low | High |
|------|-----|------|
| 1. Container & delivery | $2,300 | $4,300 |
| 2. Interior conversion (light-seal, paint, backing) | $950 | $1,350 |
| 3. Pinhole optics plate | $95 | $240 |
| 4. Film plane mechanism (4-corner, manual, incl. brace cage) | $2,800 | $3,300 |
| 5. Print washing — water system (incl. IBC stacking frame) | $4,905 | $7,396 |
| 6. Electrical — power, circuits, wiring | $1,785 | $1,890 |
| 7. Housed revolving-door light lock (custom fabrication) | $1,785 | $2,460 |
| 7a. Panel sliding carriage | $1,036 | $1,036 |
| 7b. Perimeter walkway (4 sections + drum-exit punch-out) | $1,000 | $1,515 |
| 7c. Ceiling rail suspension | $208 | $208 |
| 8. Cooling & ventilation | $370 | $450 |
| 9. Printmaking chemistry — cyanotype, 50 prints | $2,500 | $3,200 |
| 10. Printmaking tools & consumables | $350 | $500 |
| 11. Safety & PPE | $120 | $180 |
| **TOTAL (base build + 50-print run)** | **~$20,216** | **~$27,191** |

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
**Section total: ~$1,000–$1,350**

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
| [Linear guide rail HGR20](https://www.amazon.com/s?k=HGR20+linear+rail+guide) | 2200mm length | 4 | Amazon / Automation Overstock | [McMaster #5901T777](https://www.mcmaster.com/5901T777) | $45 |
| [Rail carriage HGH20CA](https://www.amazon.com/s?k=HGH20CA+carriage+block) | Flanged block | 8 | Amazon / Automation Overstock | McMaster-Carr | $18 |
| [Acme leadscrew ¾"-6](https://www.roton.com) | 8ft length | 4 | [Roton Products](https://www.roton.com) | [McMaster #6289K36](https://www.mcmaster.com/6289K36) | $95 |
| [Acme nut, bronze ¾"-6](https://www.roton.com) | — | 4 | [Roton Products](https://www.roton.com) | [McMaster #6289K512](https://www.mcmaster.com/6289K512) | $12 |
| [Handwheel 8" dia](https://www.mcmaster.com/6440K64) | ¾" bore, cast aluminum | 4 | McMaster-Carr | McMaster #6440K64 | $35 |
| [Locking collar SS316](https://www.mcmaster.com/6436K12) | ¾" bore | 4 | McMaster-Carr | McMaster #6436K12 | $12 |
| Corner bracket L-plate | ¼" aluminum plate, 6"×8" | 4 | Metal Supermarkets SoCal | [Online Metals](https://www.onlinemetals.com) | $20 |
| [Rod-end spherical bearing](https://www.mcmaster.com/60645K73) | GIR25-DO or equiv., 25mm bore | 8 | McMaster-Carr | McMaster #60645K73 | $22 |
| [Pivot pin SS316](https://www.mcmaster.com/98173A150) | 1" dia × 8" long | 8 | McMaster-Carr | McMaster #98173A150 | $8 |
**Rails & structural subtotal: ~$1,260**

### Film plane frame & backing
| Item | Spec | Qty | Supplier A | Supplier B | Est. unit |
|------|------|-----|-----------|-----------|-----------|
| Aluminum angle 2"×2"×3/16" | 8ft lengths | 10 | Metal Supermarkets SoCal | [Online Metals](https://www.onlinemetals.com) | $22 |
| [Dibond ACM panel 4mm](https://www.grimco.com) | 4'×8' sheets | 6 | Grimco, City of Industry CA | Signwarehouse | $85 |
| [Black EPDM foam tape 1"×½"](https://www.mcmaster.com/8614K84) | 50ft rolls | 3 | McMaster-Carr #8614K84 | — | $28 |
| [Rosco Duvetyne blackout fabric](https://www.rosebrand.com) | 60" wide, 10 yd | 1 | [Rose Brand](https://www.rosebrand.com) (Burbank CA) | B&H Photo | $95 |
| [Aluminum piano hinge 72"](https://www.mcmaster.com/1580A51) | 2" wide, 1/16" leaf | 2 | McMaster-Carr #1580A51 | — | $28 |
| 6-mil black poly sheeting | 10'×100' roll | 1 | Home Depot | — | $65 |
| 2" black Gorilla Tape | 35 yd rolls | 6 | Home Depot | Amazon | $12 |
**Frame subtotal: ~$1,102**

### Optional: electric actuation (add-on)
| Item | Spec | Qty | Supplier | Est. unit |
|------|------|-----|----------|-----------|
| [PA-14 linear actuator](https://www.progressiveautomations.com) | 12V, 20" stroke, 150 lb | 4 | [Progressive Automations](https://www.progressiveautomations.com) | $185 |
| 12V 30A power supply | Enclosed | 1 | [Mouser](https://www.mouser.com) / Digi-Key | $55 |
| DPDT momentary rocker switch | Panel-mount, 20A | 4 | [Mouser](https://www.mouser.com) | $8 |
**Electric actuation subtotal: ~$827 (optional)**

### Demountable brace cage (ICP-11 through ICP-14)
*Two rectangular end portals of 50×50×3mm RHS brace the four-corner rail assembly; demountable joints for transport.*

| Item | ICP # | Spec | Qty | Supplier A | Supplier B | Est. unit | Est. total |
|------|-------|------|-----|-----------|-----------|-----------|------------|
| [Mild steel RHS square tube — structural welded](https://www.metalsupermarkets.com/product/mild-steel-square-tube-structural-welded/) | ICP-11 | 50×50×3mm; 4 verticals @ 2188mm + 4 cross-beams @ 4499mm = 26.75 m net; order 30 m to cover saw kerf + saddle-seat cuts (~98 ft) | 30 m | [Metal Supermarkets SoCal](https://www.metalsupermarkets.com/) (Anaheim / Van Nuys / San Diego — cut to length, walk-in) | [Online Metals — 50mm×3mm carbon steel sq. tube](https://www.onlinemetals.com/en/buy/carbon-steel/50mm-x-3mm-carbon-steel-square-tube-1018-metric-60-length/pid/22489) (ships; ~$47 per 20 ft stick) | ~$7/ft est. | ~$230 est. |
| Square tube saddle clamp, 50mm | ICP-12 | Two-piece bolt-together saddle — seats one 50×50mm RHS member over another at a demountable joint | 16 | [McMaster-Carr — steel tube clamps](https://www.mcmaster.com/products/steel-tube-clamps/) | [Amazon — 2" square tube clamps](https://www.amazon.com/2-square-tube-clamp/s?k=2%22+square+tube+clamp) | ~$8–12 est. | ~$160 est. |
| [M8×20mm knurled thumbscrew DIN 464, SS 303](https://www.amazon.com/knurled-thumb-screws-din-464/s?k=knurled+thumb+screws+din+464) | ICP-13 | High-type knurled head, fully threaded; 2 per saddle clamp joint; 32 working + 8 spares | 40 | [Amazon — DIN 464 M8 stainless (various sellers)](https://www.amazon.com/knurled-thumb-screws-din-464/s?k=knurled+thumb+screws+din+464) | [Maedler North America — PN 65499225](https://maedlernorthamerica.com/partshop/knurled-thumb-screw-din-464-m8-x-20mm-long-stainless-steel-1-4305-pn-65499225/) (~$15–17 ea. direct; Amazon cheaper in packs) | ~$3 est. | ~$120 est. |
| [Quick-release ball-lock pin, Ø10mm SS](https://www.mcmaster.com/products/ball-lock-pins/) | ICP-14 | 50mm usable length, stainless steel; retains demountable left-rail segment for drum-mode (4 working + 4 spares) | 8 | [McMaster-Carr — ball lock pins](https://www.mcmaster.com/products/ball-lock-pins/) | [Amazon — quick-release ball lock pins](https://www.amazon.com/quick-release-ball-lock-pins/s?k=quick+release+ball+lock+pins) | ~$6–10 est. | ~$65 est. |

**Brace cage subtotal: ~$575 est.**

*All prices estimated — Metal Supermarkets and McMaster-Carr do not publish per-unit pricing online; call or add to cart for a current quote. Blue Sky Supplies (blueskysupplies.com) confirmed 2"×2"×⅛" × 20 ft at $47.43 (May 2026). M8 thumbscrew pricing confirmed at ~$15–17 each from Maedler North America (PN 65499225, May 2026); Amazon multi-packs from various sellers run ~$2–5 ea. depending on pack size.*

**Section total (manual, incl. brace cage): ~$2,937**

> **4-corner vs original 2-beam design delta:** Removed 2× 80/20 T-slot beams (5893mm) — saves $416. Added: 2× extra leadscrews +$190, 2× extra handwheels +$70, 4× rod-end spherical bearings +$88, 4× corner L-brackets +$80. Added brace cage (ICP-11–14): +$575. Net change vs original two-beam design: +$587 for significantly greater geometric capability and integral structural rigidity. Excl. fabrication, fasteners, and optional electric actuation.

---

## 5. Print Washing — Water System
*Source: `water-system-report.md`*

### Water storage
| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| [IBC tote 275 gal, food-grade, used/rinsed](https://containerexchanger.com/geo-sale-ads/us-ca/bulk-containers/ibc-totes-for-sale) | HDPE cage, DN50 butterfly valve (S60×6) — Blue (×2), Brown (×1), Waste (×1) | 4 | Container Exchanger | $80–$150 | $320–$600 |
| [2" NPT bulkhead fitting (304 SS)](https://www.mcmaster.com/4464K115) | External drain/fill port, welded through container wall (X1/X3/X4) | 3 | McMaster-Carr | $25–$40 | $75–$120 |
| Reinforcing plate, 6mm A36 steel, 150×150mm | Backing plate for external bulkhead ports (one per fitting) | 3 | Metal Supermarkets SoCal | $8–$12 | $24–$36 |
**Storage subtotal: ~$388–$698**

### IBC stacking frame
*Source: `ibc-stacking-report.md` §3, §9.1. Welded 50×50×3mm RHS frame for the 2×2 IBC stack — platform beams simply supported wall-to-wall (corridor uprights + welded wall seat brackets), uprights anchored to the floor.*

| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| [Mild steel RHS 50×50×3mm, 6 m length](https://www.metalsupermarkets.com/product/mild-steel-square-tube-structural-welded/) | Uprights, beams, cross-members + mid-bay panel support frame (extended uprights, top rail, floor beam) (A500 Grade B) | 8 | [Metal Supermarkets SoCal](https://www.metalsupermarkets.com/) / [Online Metals](https://www.onlinemetals.com) | $30–$45 | $240–$360 |
| [Steel plate 12mm, 150×150mm cut](https://www.onlinemetals.com/en/buy/carbon-steel) | Upright floor flange feet | 6 | Metal Supermarkets SoCal / Online Metals | $4–$8 | $25–$45 |
| Steel plate 8mm (back-plates, seats, gussets) | 6 welded wall seat brackets (cut from ~0.3 m²) | 1 lot | Metal Supermarkets SoCal | $50–$80 | $50–$80 |
| Steel flat bar 5mm (~8 m) | Anti-rotation lip on platform perimeter | 1 | Metal Supermarkets SoCal | $30–$50 | $30–$50 |
| Closed-cell rubber mat, 12mm (1000×1200mm) | Anti-slip platform mats (one per column) | 2 | [McMaster-Carr](https://www.mcmaster.com/) / Amazon | $20–$30 | $40–$60 |
| [Welded D-ring, 25mm, 1,100 kg WLL](https://www.mcmaster.com/3641T29) | Lashing points on 6mm mount plates | 8 | McMaster-Carr #3641T29 | $5–$8 | $40–$65 |
| [Ratchet strap, 25mm, 1,100 kg WLL](https://www.amazon.com/s?k=25mm+ratchet+strap+1100kg) | Transport securing (2 per tier) | 4 | Amazon / Harbor Freight | $8–$13 | $30–$50 |
| [M12×40 hex bolt, Grade 8.8 + nut/washer](https://www.mcmaster.com/91290A655) | Wall seat brackets, 4 each into wall ribs | 24 | McMaster-Carr / Fastenal | $1–$2 | $25–$45 |
| [M12 wedge/sleeve floor anchor](https://www.mcmaster.com/concrete-anchors) | Upright flange feet, 4 each into container floor | 24 | McMaster-Carr / Home Depot | $2–$3 | $40–$70 |
| Steel flat bar (X-bracing) | Bottom-tier racking resistance | 4 | Metal Supermarkets SoCal | $5–$9 | $20–$35 |
| Access gate panel, 300mm steel | Removable drain-valve access, 4× M12 each | 2 | Local fab | $20–$30 | $40–$60 |
| Welding / fabrication | ~26–36 hrs (incl. feet + seat brackets) | 1 | Local fab shop | $1,150–$1,650 | $1,150–$1,650 |
| Primer + flat-black powder coat | Anti-corrosion finish | 1 | Local | $40–$60 | $40–$60 |
**IBC stacking frame subtotal: ~$1,770–$2,630**

### Pumps
| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| [Shurflo 2088-554-144 pump](https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C) | 12VDC, 3.5 GPM, 45 PSI, ½" NPSM ports (P-01, P-02, P-04 manifold + P-03 IBC corridor) | 4 | Amazon | $55–$70 | $220–$280 |
| [SeaFlo pressure accumulator](https://www.amazon.com/Seaflo-Accumulator-Control-Internal-Bladder/dp/B01MUYL8F8) | 0.75 L (23.5 oz), 125 PSI, ½" MNPT | 1 | Amazon | $25–$45 | $35 |
| [Shurflo pump mounting bracket](https://www.amazon.com/s?k=shurflo+2088+mounting+bracket+stainless) | Stainless, for 2088 series (3× manifold + 1× IBC corridor for P-03) | 4 | Amazon | $8–$12 | $32–$48 |
**Pump subtotal: ~$167–$203**

### Filter unit
| Item | Spec | Qty | Supplier | Est. unit | Total |
|------|------|-----|----------|-----------|-------|
| [3-stage Big Blue combo filter 4.5"×20"](https://www.purcooflow.com/products/whf2045b302-3-stage-kdf-heavy-metal-water-filter) | 1" NPT ports, integrated bracket, triple drain valves. Purcooflow WHF2045B302 or equiv. (iSpring WGB32B, Express Water) | 1 | Purcooflow / Amazon | $350–$450 | $350–$450 |
| [MPP 5-micron sediment cartridge 4.5"×20"](https://www.amazon.com/s?k=4.5x20+melt+blown+polypropylene+sediment+filter+5+micron) | Melt-blown polypropylene depth filter (F-1 stage) | 3 + spares | Amazon | $8–$14 | $24–$42 |
| [KDF-55 heavy metal cartridge 4.5"×20"](https://www.amazon.com/s?k=4.5x20+KDF+55+heavy+metal+water+filter) | KDF-55 media for dissolved iron removal (F-2 stage) | 2 + spares | Amazon | $30–$50 | $60–$100 |
| [CTO carbon block cartridge 4.5"×20"](https://www.amazon.com/s?k=4.5x20+CTO+coconut+shell+carbon+block+filter) | Coconut shell activated carbon block (F-3 stage) | 3 + spares | Amazon | $12–$20 | $36–$60 |
**Filter subtotal: ~$470–$652**

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
**Valves, fittings & pipe subtotal: ~$502–$815**

### Processing tray
| Item | Spec | Qty | Supplier | Unit price | Est. cost |
|------|------|-----|----------|-----------|-----------|
| [304 SS sheet, 16-ga (1.5mm)](https://www.onlinemetals.com/en/buy/stainless-steel/304-stainless-steel-sheet) | #4 brushed, 4'×8' sheets | 4 | Online Metals | $180–$250/sheet | $720–$1,000 |
| Fabrication (cut, brake, weld, press sump) | Two tray halves: 2229×2200mm, 50mm rims, pressed sump well (150×100×20mm) | 1 job | Local sheet metal shop | $450–$850 | $450–$850 |
| [HDPE flat bar 50×10mm](https://www.mcmaster.com/8619K451) | Tapered shim strips for slope support, 2200mm long | 5 | McMaster-Carr / TAP Plastics | $8–$15 each | $40–$75 |
| [1" SS foot valve with strainer](https://www.amazon.com/s?k=1+inch+stainless+foot+valve+strainer) | Sump pickup, prevents debris, maintains prime | 1 | Amazon | $15–$25 | $20 |
| [1" reinforced suction hose, 6 ft](https://www.amazon.com/s?k=1+inch+reinforced+suction+hose+6+ft) | P-04 suction from sump pickup over tray rim to pump manifold | 1 | Amazon | $12–$20 | $15 |
| [Silicone gasket strip, FDA grade](https://www.mcmaster.com/1460N14) | 1/16" × 1" × 10 ft, center flange seal | 1 roll | McMaster-Carr | $15–$25 | $20 |
| [M6×16 SS hex bolts + flange nuts](https://www.mcmaster.com/92196A150) | Center flange, 200mm spacing | 24 | McMaster-Carr | $0.50 each | $12 |
**Processing tray subtotal: ~$1,277–$1,992**

### Spray bar assembly (gantry design)
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [6061-T6 aluminum SHS 1½"×1½"×⅛"](https://www.onlinemetals.com/en/buy/aluminum/6061-t6-aluminum-square-tube) | 40×40×3mm structural beam, 8 ft lengths (2 joined with sleeve for 3859mm). 12mm holes drilled for nozzle fittings | 2 | Online Metals | $36–$56 |
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
**Spray bar subtotal: ~$200–$270**

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

**Section total: $3,135–$4,766**

## 6. Electrical — Power, Circuits & Wiring
*Source: `electrical-report.md`*

### Solar & battery (primary power)
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [Solar panels, 200W monocrystalline](https://www.renogy.com/200-watt-12-volt-monocrystalline-solar-panel/) | 12V nominal | 3 | [Renogy](https://www.renogy.com) | ~$400 total |
| [Victron SmartSolar MPPT 100/50](https://www.altestore.com) | MPPT charge controller | 1 | [altE Store](https://www.altestore.com) | ~$200 |
| [LiFePO4 battery 100Ah 12V](https://www.renogy.com/12v-100ah-smart-lithium-iron-phosphate-battery/) | Renogy Smart Lithium or Battle Born | 2 | [Renogy](https://www.renogy.com) | ~$700 total |
| [Victron Blue Smart IP65 12/15](https://www.altestore.com) | Shore backup charger | 1 | [altE Store](https://www.altestore.com) | ~$150 |
| NEMA 5-15R inlet (weatherproof) | Mounted in flush-mount power panel | 1 | Amazon | ~$25 |
| [Solar panel ground mount frame](https://www.renogy.com) | Tilt frame, 30° | 1 | [Renogy](https://www.renogy.com) | ~$80 |
| PV cable 10 AWG | MC4 connectors | 1 lot | Amazon | ~$30 |
| Aluminum plate 340×240×3mm | Flush-mount face plate, power panel | 1 | [Online Metals](https://www.onlinemetals.com) | ~$18 |
| Neoprene gasket 340×240×3mm | Weatherseal between plate and wall | 1 | McMaster-Carr | ~$6 |
| M6 bolt + nut + washer set | Panel mounting hardware, SS | 4 | McMaster-Carr | ~$5 |
| [MC4 bulkhead connector pairs](https://www.amazon.com/s?k=MC4+bulkhead+connector+panel+mount+IP67) | IP67 panel-mount | 3 pairs | Amazon | ~$25 |
| Deutsch DT 2-pin bulkhead connector | Panel-mount, IP67, Circuit E cooler output | 1 | [Waytek Wire](https://www.waytekwire.com) | ~$5 |
**Solar & battery subtotal: ~$1,645**

### Distribution & wiring
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [Blue Sea 5026 fuse block](https://www.amazon.com/s?k=Blue+Sea+5026+fuse+block) | 12-circuit ST-blade | 1 | Amazon / [West Marine](https://www.westmarine.com) | ~$55 |
| [200A ANL main fuse + holder](https://www.amazon.com/s?k=200A+ANL+fuse+holder+Blue+Sea) | Blue Sea ANL fuse block | 1 | Amazon | ~$30 |
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
**Distribution & wiring subtotal: ~$600**

**Section total: ~$1,785–$1,890**

## 7. Housed Revolving-Door Light Lock — Custom Fabrication
*Source: `light-trap-selection.md` § 4 (rev 8). Custom-fabricated Ø900 fixed housing + single-opening C-shell drum (no fins) built into the hinged cargo-door panel — light-tight by geometry. Replaces the failed Ø750 4-fin drum. Single-operator entry/exit at any time without admitting daylight.*

### Housing + drum body
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 3mm mild steel sheet, 1200×2400mm | Hot-rolled A36 — Ø900 housing + Ø864 drum shells (rolled, ~12 m²) | 4 sheets | Pacific Coast Steel — Santa Fe Springs CA | ~$80/sheet → ~$320 |
| 5mm steel plate (offcut) | Top and bottom drum caps, flanged | ~0.5m² | Pacific Coast Steel / Metal Supermarkets SoCal | ~$40 |
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

### Surface treatment
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Flat black powder coat — interior housing + drum surfaces | RAL 9005 matte; shot-blast prep + coat | 1 job | Local powder coat shop (SoCal) | ~$180–$260 |
| Grey oxide primer + grey topcoat — exterior drum face | Standard exterior steel finish | 1 job | Included with powder coat job above, or rattle-can | ~$0–$30 |

### Fabrication labour
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Metal fabrication — roll 2 cylinders (housing + drum), seam weld, cap/shaft weld, bearing fit | 22–28 hrs at local metal fab shop | 1 job | Local fabrication shop (SoCal) — get 2–3 quotes | ~$1,100–$1,500 |
**Section total: ~$1,785–$2,460**

*Note: This is for the drum body only. The hinged panel that the drum mounts into (50×50mm RHS frame, 18mm ply skins, EPDM perimeter gasket) is covered in § 2 (Interior Conversion) above. See [light-trap-selection.md](light-trap-selection.md) for full specification and supplier notes.*

## 7a. Panel Sliding Carriage
*Source: `equipment-layout-report.md` § 6.1. Enables transport mode: panel slides inward 300mm, clearing container doors for closure. Single-person operation (~5 min, panel slide only).*

### Panel slide system
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [HGR20 linear rail, 500mm](https://www.amazon.com/s?k=HGR20+linear+rail+500mm) | Both walls, floor + ceiling, X-direction | 4 | Amazon / Automation Overstock | ~$88 |
| [HGH20CA carriage blocks](https://www.amazon.com/s?k=HGH20CA+carriage+block) | Flanged, 2 per rail | 8 | Amazon / Automation Overstock | ~$144 |
| Carriage beam, 60×60×3mm SHS | 2400mm tall, mild steel | 1 | Metal Supermarkets | ~$35 |
| Hinge mounting plates, 6mm steel | 220×80mm | 3 | Local fab | ~$30 |
| Rail mounting brackets, 8mm angle | Both walls, floor + ceiling | 8 | Local fab | ~$64 |
| [Destaco 207-U toggle clamps](https://www.amazon.com/s?k=Destaco+207-U+toggle+clamp) | 2 per position × 2 positions | 4 | Amazon / McMaster-Carr | ~$100 |
| Strike pins, 16mm hardened dowel | Pressed into carriage base | 4 | McMaster-Carr | ~$12 |
**Panel slide subtotal: ~$473**

### Fixed door frame + seals
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 50×50×3mm RHS welded frame | Full door perimeter ~9.5m | 1 | Metal Supermarkets | ~$120 |
| 3mm steel plate/angle, ~110mm × ~4m | Top + bottom seal lips — frame-top downstand (top, continuous full width) + threshold upstand (bottom, notched around drum); light paths #6–#7 | 1 | Metal Supermarkets | ~$60 |
| Seal landing machining | Mill flat on all frame faces | 1 | Local fab | ~$80 |
| [Brush seal strip (doubled nylon bristle)](https://www.mcmaster.com/brush-seal-strip) | Left carriage beam slot, 2400mm × 2 layers | 2 | McMaster-Carr | ~$50 |
| [Brush seal strip (doubled nylon bristle)](https://www.mcmaster.com/brush-seal-strip) | Right guide slot, 2400mm × 2 layers | 2 | McMaster-Carr | ~$50 |
| [EPDM gasket 20×15mm](https://www.mcmaster.com/8635K31) | ~9.5m | 1 | McMaster-Carr #8635K31 | ~$45 |
| Neoprene backup strip, 10×10mm | Self-adhesive, ~9.5m | 1 | McMaster-Carr | ~$22 |
| Neoprene rail channel pads, 10mm | 50×30mm, closed-cell, 4 rail penetrations | 4 | McMaster-Carr | ~$8 |
| EPDM edge strips, 15mm | Self-adhesive, 2400mm × 2 sides | 2 | McMaster-Carr | ~$18 |
| Fasteners, misc | M10/M12 stainless, assorted | 1 lot | McMaster-Carr | ~$60 |
| Flat black paint | Touch-up, 1 qt | 1 | Home Depot | ~$15 |
| Fan B flex cable (coiled, 16AWG 2-cond, silicone) | 1m coiled, Deutsch DT 2-pin connectors each end | 1 | Waytek Wire / McMaster-Carr | ~$35 |
**Door frame subtotal: ~$563**

**Section total (materials): ~$976**
**Fabrication labor: ~12–16 hrs × $80–$100/hr = $960–$1,600**

## 7b. Perimeter Walkway
*Source: `generate_walkway_diagram.py`, `engineering-diagrams.md` §14. Four removable grated walkway sections around the processing tray. Near walkway widens from 300mm to 500mm at EP/battery/slit zone (X≈1,155–2,629). Near/far: wall-cantilevered brackets bolted to corrugated wall ribs. Right: ceiling-hung from M10 threaded rod hangers (no floor contact — clears IBC stack entirely). Left: removable lift-out (panel conflict — no brackets). Butt joints at all corners. No floor contact on any section — entire tray interior completely clear for film loading. Deck height 80mm (65mm support + 15mm grate).*

### Walkway sections (4 off)
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [Press-locked steel grating, 15mm](https://www.mcnichols.com/products/grating/bar-grating/) | Galvanized, 15×3mm bars, 34mm pitch. Cut to size: near 4459×300mm (with 1474×500mm bump-out), far 4459×300mm, right 2362×300mm, left 2362×300mm (removable) | ~4.5 m² | [McNichols](https://www.mcnichols.com) | ~$290–$430 |
| Standard wall brackets, 8mm steel plate | Triangular gusset: 150mm vert × 300mm arm, welded. Hot-dip galvanized. | 14 | Local fab / Metal Supermarkets | ~$112–$175 |
| Widened wall brackets, 10mm steel plate | 200mm vert × 500mm arm, 70mm gusset, welded. Hot-dip galvanized. EP/battery/slit zone. | 4 | Local fab / Metal Supermarkets | ~$72–$112 |
| Reinforcing plates, 100×180×6mm mild steel | Welded to exterior wall face behind each standard bracket | 14 | Metal Supermarkets | ~$31–$49 |
| Reinforcing plates, 120×220×6mm mild steel | Wider plates behind each widened bracket (4-bolt pattern) | 4 | Metal Supermarkets | ~$16–$24 |
| M12×60mm hex bolts, nuts, flat washers | Grade 8.8, galvanized. 3 per standard bracket (42) + 4 per widened bracket (16). | 58 | McMaster-Carr | ~$57–$87 |
| Transition bearing plate, 40×500×5mm flat bar | Welded to bracket arm top at width transitions (X≈1,156 and X≈2,526). Both grating widths land on plate. | 2 | Metal Supermarkets | ~$5–$10 |
| Steel angle bearer, 25×25×5mm L-angle | Hot-dip galvanized. 2× 2362mm lengths (right walkway). | 2 | Metal Supermarkets | ~$20–$35 |
| M10 threaded rod, galvanized | 2313mm long, grade 8.8. 10 rods (5 hanger pairs). | 10 | McMaster-Carr | ~$40–$60 |
| Ceiling bracket plates, 100×60×6mm steel | Galvanized. 10 plates (1 per hanger). | 10 | Local fab | ~$20–$35 |
| M10 nuts, flat washers, lock washers | Galvanized. 4 per hanger rod. | 40+40 | McMaster-Carr | ~$20–$30 |
| [M saddle clips + TEK screws](https://www.mcnichols.com/products/grating/accessories/) | M saddle clips straddle 2 bearing bars, TEK screw through bracket arm or L-angle. Near/far/right walkways. | ~20 | [McNichols](https://www.mcnichols.com) | ~$15–$25 |
| Guide tabs, 3mm steel angle | Welded to left walkway bearer beam. Prevent lateral grating slide. | 4 | Local fab | ~$5–$10 |
| Drum-exit punch-out — extra grating (~0.23 m²) + 50×50×3mm Al RHS bearer (~0.8m) + 25×25 Al SHS leg + foot | Deeper landing (600mm) at the light-lock exit | 1 lot | Metal Supermarkets / McNichols | ~$45 |
| Fabrication + installation | Cut/weld/galvanize 14 std + 4 widened brackets, reinforcing plates, drill wall ribs, hang right walkway bearers, weld guide tabs, install | 1 job | Local fab / metal shop | ~$280–$440 |
**Walkway subtotal: ~$1,005–$1,530**

*Near/far grating secured with M saddle clips + TEK screws to bracket arms. Right walkway grating secured with M saddle clips + TEK screws to L-angle bearer horizontal leg. Left walkway uses gravity retention with guide tabs welded to bearer beam — lift straight up to remove (no fasteners). Near walkway widens to 500mm at EP/battery/slit zone (X≈1,155–2,629) with heavier 10mm brackets (see Sheet 7). Slits cut to tray lip only (near: 420mm, far: 218mm), not full walkway depth. Transition bearing plates at width change brackets (X≈1,156 and X≈2,526). Butt joints at all corners. No floor contact on any section — entire tray interior clear.*

## 7c. Ceiling Rail Suspension
*Source: `generate_ceiling_rail_diagram.py`, `engineering-diagrams.md` §13. HGR20 ceiling-mounted linear rails suspend the hinged panel with 80mm floor gap, clearing the 50mm processing tray rim during transport slide.*

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [HGR20 linear rail, 500mm](https://www.amazon.com/s?k=HGR20+linear+rail+500mm) | Ceiling-mounted, both walls, X-direction | 2 | Amazon / Automation Overstock | ~$44 |
| [HGH20CA carriage blocks](https://www.amazon.com/s?k=HGH20CA+carriage+block) | Flanged, 2 per rail | 4 | Amazon / Automation Overstock | ~$72 |
| Ceiling mounting brackets, 8mm angle | Welded to container ceiling ribs | 4 | Local fab | ~$32 |
| Drop rod / hanging bracket, 6mm steel | Connects carriage block to panel top rail | 4 | Local fab | ~$40 |
| Fasteners, misc | M10 stainless | 1 lot | McMaster-Carr | ~$20 |
**Ceiling rail subtotal: ~$208**

*Note: The panel sliding carriage (§7a) uses 4 rails at floor + ceiling on both walls. This section covers the 2 additional ceiling rails that provide panel suspension and floor gap clearance.*

## 8. Cooling & Ventilation
*Source: `electrical-report.md`*

### Ventilation fans (upgrade from original 4" spec)
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [AC Infinity S6 inline DC fan](https://www.amazon.com/s?k=AC+Infinity+S6+inline+fan+6+inch) | 6" (150mm), 12V, ~200 CFM | 2 | Amazon | ~$120 total |
| 6" duct stub fittings | Wall penetration collars | 2 | Amazon | ~$20 |
| Fan baffle plates (3mm mild steel) | 2 baffles per fan, offset S-path | 1 lot | Metal Supermarkets | ~$40 |
**Ventilation subtotal: ~$180**

### Shade canopy
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 80% shade cloth 20×10ft | UV-stabilized, over container roof | 1 | Amazon / Farm supply | ~$80 |
| Canopy frame | 1.5" EMT conduit + T-fittings | 1 lot | Home Depot | ~$120 |
**Shade canopy subtotal: ~$200**

### Evaporative cooler
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [12V DC evaporative cooler](https://www.portacool.com) | ~80W, ~300 CFM (Portacool Jetstream 110 12V or equiv.) | 1 | [Portacool](https://www.portacool.com) / Amazon | ~$280 |
| Ø200mm insulated flex duct | ~1.2m, aluminum foil jacket, cooler to wall stub | 1 | [Home Depot](https://www.homedepot.com/s/8%20inch%20insulated%20flex%20duct) / McMaster-Carr | ~$22 |
| Ø200mm (8") 90° duct elbow | Galvanized — vertical riser off cooler to horizontal wall entry | 1 | [Home Depot](https://www.homedepot.com/s/8%20inch%20duct%20elbow) | ~$14 |
| Ø200mm duct collar + hose clamp | Galvanized, wall stub coupling | 1 | [Home Depot](https://www.homedepot.com/s/8%20inch%20duct%20collar) | ~$12 |
| Ø200mm weatherproof duct cap | Removable, protects wall stub when cooler disconnected | 1 | [Home Depot](https://www.homedepot.com/s/8%20inch%20duct%20cap) | ~$8 |
| 200mm baffle duct + plates | Light-safe baffled intake, 300mm stub, 2× offset baffles | 1 lot | McMaster-Carr / local fab | ~$20 |
| Cooler external power cable | 1.5m, 14 AWG 2-cond, Deutsch DT 2-pin plugs each end | 1 | [Waytek Wire](https://www.waytekwire.com) / Amazon | ~$20 |
| 25mm ratchet strap, 2m | Cooler transport stowage on near walkway | 2 | Amazon / Harbor Freight | ~$10 |
| 12mm plywood base plate 600×350mm | Load distribution on walkway grating | 1 | Offcut / local | ~$5 |
| 25×25×3mm Al angle cleats, 100mm | Anti-slide cleats screwed to base plate | 2 | Metal Supermarkets / online | ~$4 |
**Cooler subtotal: ~$395**

**Section total: ~$759**
*Note: fans wired to Circuits A & B, cooler to Circuit E — all from main fuse block. Cooler power supplied via Deutsch DT bulkhead connector on external power panel.*

## 9. Printmaking Chemistry — Cyanotype (50 prints)
*Source: `chemistry-shopping-list.md`*

**Recommended process.** No silver, no DEA registration, no hazmat shipping, development in plain cold water.

### Chemistry
| Item | Per print | × 50 prints | Supplier | Unit | Units | Unit price | Total |
|------|-----------|-------------|---------|------|-------|-----------|-------|
| [Ferric ammonium citrate (FAC), green grade, 1 lb](https://stores.photoformulary.com) | 224g | 11.2 kg | [Photographers' Formulary](https://stores.photoformulary.com) | 454g (1 lb) | 27 | ~$30† | ~$810 |
| [Potassium ferricyanide, 1 kg](https://bostick-sullivan.com) | 91g | 4.55 kg | [Bostick & Sullivan](https://bostick-sullivan.com) | 1,000g | 5 | $24.29† | $121 |
| Distilled water | ~2 L | ~100 L | Tap water + DI filter adequate | — | — | — | ~$0 |

> **FAC note:** Order green grade only (Fe³⁺). Brown grade (Fe²⁺) is not light-sensitive for cyanotype. Photographers' Formulary and Bostick & Sullivan both specify green grade.
**Chemistry subtotal: ~$931**

### Substrate
| Item | Qty | Supplier | Unit | Units | Unit price | Total |
|------|-----|---------|------|-------|-----------|-------|
| [Unbleached cotton muslin, 60" wide](https://www.fabricdirect.com) | 1,650 linear yards | [Fabric Direct](https://www.fabricdirect.com) | 150-yd roll | 11 | ~$100 | ~$1,100 |
| OR [unbleached cotton muslin by the yard](https://www.fabricwholesaledirect.com) | 1,650 yd | [Fabric Wholesale Direct](https://www.fabricwholesaledirect.com) | per yard | 1,650 | $0.80–$1.20/yd | $1,320–$1,980 |

> **Muslin note:** Pre-wash all fabric twice in hot water, no detergent, to remove sizing. Sizing repels water-based sensitisers. 60" width requires 5 strips per print — or source 120" (theatrical/backdrop) width to eliminate vertical seams.
**Substrate subtotal: ~$1,100**

**Section total: ~$2,031–$2,842** (per 50-print run, ~$57/print)

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
| Spray bottle (1 litre) | Humidity/misting in low-RH conditions | 2 | Amazon / garden supply | ~$15 |
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
| **[McNichols](https://www.mcnichols.com)** | Press-locked steel grating, clips | Online / Multiple branches |
| **[Purcooflow](https://www.purcooflow.com)** | 3-stage combo filter units, replacement cartridges | Online |
| **[Grainger](https://www.grainger.com)** | Industrial supply — local branches throughout SoCal | Multiple SoCal branches |
| **[Lenox Laser](https://www.lenoxlaser.com)** | Custom precision laser-drilled pinholes | Glen Arm, MD |
| **[Portacool](https://www.portacool.com)** | 12V DC evaporative coolers | Online |
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