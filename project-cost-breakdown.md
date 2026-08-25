<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Complete Project Cost Breakdown

**Date:** April 2026
**Basis:** Ranges given where source documents provide them; midpoints used for totals. Costs marked † are from detailed procurement research in supporting documents; others are estimates.

**Related:** [Master Shopping List](master-shopping-list.md) (per-item procurement with suppliers and URLs) · [Funding Proposal](funding-proposal.md) (grant-ready summary at three funding levels)

---

## Summary — Total Project Cost

<!-- BEGIN costing:scenario -->
| Category | Low | Mid | High |
|----------|-----|-----|------|
| **1. Container purchase & delivery** | $2,300 | $3,300 | $4,300 |
| **2. Interior conversion** | $526 | $605 | $693 |
| **3. Optics — pinhole plate** | $100 | $155 | $215 |
| **4. Film plane mechanism (4-corner U-channel + acetal skate + U-joint, incl. wall-seat saddles)** | $4,110 | $4,309 | $4,512 |
| **5. Processing water system (incl. tray, spray bar, IBC stacking frame)** | $6,841 | $7,478 | $8,126 |
| **5a. Power & electrical system (solar · 1× LiFePO4 · MPPT · distribution · lighting · protection · master pump switch)** | $3,431 | $3,464 | $3,496 |
| **5b. Ventilation & cooling system (2 fans · evap cooler **+ 12V→120V inverter** · light-safe baffle-duct fab · shade canopy)** | $748 | $808 | $898 |
| **6. Housed revolving-door light lock (plastic-skin custom fabrication)** | $2,959 | $3,473 | $3,983 |
| **6a. Perimeter walkway (4 sections + drum-exit punch-out)** | $2,079 | $2,498 | $2,941 |
| **6b. Panel swing pivot + fixed door frame (Ø89 post + bearings + cage + wall stays + rail saddles)** | $1,180 | $1,395 | $1,610 |
| **6c. Hinged panel structure (stepped frame + HDPE skins + Al core + EPDM + cam latches + B2 bay + pull handle)** | $1,278 | $1,382 | $1,484 |
| **6d. Chemistry prep shelf (fold-down phenolic board + steel frame + hinge/stays + TAP-01 trunk extension)** | $223 | $229 | $235 |
| **7. Printmaking — 50 prints (cyanotype; Low=Lean, Mid=Standard, High=Rich tier)** | $1,250 | $1,710 | $3,100 |
| **8. Transportation (per deployment)** | $300 | $750 | $2,000 |
| **9. Licenses & permits** | $220 | $790 | $1,620 |
| **TOTAL (excl. own transport, CDL, lens)** | **$27,545** | **$32,346** | **$39,213** |
<!-- END costing:scenario -->

*Line 7 (cyanotype printmaking) is now re-summed into the TOTAL on the **Mike Ware New Cyanotype** chemistry (ferric ammonium oxalate) + corrected ~$300 substrate: **Low = Lean ⅓-Ware ($1,250), Mid = Standard ½-Ware ($1,710), High = Rich full-Ware ($3,100)** — matching §7.1 and the master shopping list §9. The tier is pinned by the [Sensitizer Trials](sensitizer-trials.md).*

*Optional additions that may apply — see individual sections:*

| Optional item | Low | Mid | High |
|---------------|-----|-----|------|
| Lens (Rodenstock / Nikkor, used) | $400 | $800 | $1,500 |
| CDL training + DOT medical + DMV fees | $2,345 | $4,570 | $6,870 |
| Own transport vehicle (QuickLoadz trailer) | $30,000 | $35,000 | $40,000 |

---

## 1. Container Purchase & Delivery

**Source document:** `container-report.md`

The 20 ft standard container is the camera body. Minimum acceptable grade is Wind & Watertight (WWT); Cargo Worthy (CW) is recommended.

<!-- BEGIN costing:container -->
| Item | Low | Mid | High | Notes |
|------|-----|-----|------|-------|
| 20 ft container — CW grade | $2,000 | $2,750 | $3,500 | From containermgt.com |
| Delivery — short haul (<50 miles) | $300 | $550 | $800 | Commercial tilt-bed hire |
| **Section total** | **$2,300** | **$3,300** | **$4,300** | |
<!-- END costing:container -->

**Grade comparison:**

| Grade | Price range | Notes |
|-------|-------------|-------|
| WWT (minimum viable) | $1,500–$3,000 | No holes; may need extensive light-sealing |
| Cargo Worthy (recommended) | $2,000–$3,500 | CSC-certified; fewest surprises |
| One-Trip (premium) | $3,500–$5,000 | Near-new condition; easiest light-sealing |

**If a long-distance delivery is required** (100–300 miles, semi flatbed): add $1,200–$2,500.

---

## 2. Interior Conversion

**Source document:** `container-report.md`

Converting the container interior from cargo hold to pinhole camera. Includes light-sealing, interior painting, door upgrades, and ventilation. (The rigid ACM image-plane backing is bonded to the moveable film-plane frame and costed with the film-plane mechanism, not here — §2.3.)

### 2.1 Light-sealing materials

| Item | Qty | Unit | Total | Notes |
|------|-----|------|-------|-------|
| D-profile foam weatherstripping, 1"×⅜" | 50 ft | $0.50/ft | $25 | Door perimeter seals |
| Black silicone sealant (11 oz cartridges) | 5 | $8 | $40 | Weld seam gaps, corner posts |
| 6-mil black polyethylene sheeting (10'×100') | 1 roll | $65† | $65 | Interior lining over persistent seams |
| 2" black Gorilla Tape (35 yd rolls) | 4 | $12† | $48 | Secondary sealing |
| **Light-seal subtotal** | | | **$178** | |

### 2.2 Interior paint

| Item | Qty | Unit | Total | Notes |
|------|-----|------|-------|-------|
| Flat black latex paint (zero sheen) | 3 gal | $25 | $75 | Two long walls, two short walls, ceiling (~755 sq ft) |
| Primer (if bare steel) | 1 gal | $30 | $30 | One coat on new welds/repairs |
| Rollers, brushes, trays | 1 kit | $20 | $20 | |
| **Paint subtotal** | | | **$125** | |

### 2.3 Image-plane flat backing — costed with the Film Plane Mechanism

The rigid ACM backing is **bonded to the moveable film-plane frame**, so it is costed with the film-plane mechanism (`dibond-acm-film`: 4× black 3mm 4'×8' ACM ≈ $380 — see [Film Plane Mechanism](film-plane-mechanism-report.md)). The design uses the moveable back, not a wall-mounted panel.

### 2.4 Ventilation

| Item | Qty | Unit | Total | Notes |
|------|-----|------|-------|-------|
| 4" inline duct fan (reversible) | 2 | $35 | $70 | One intake / one exhaust, short walls |
| 4" light-trap baffle (steel angle, DIY) | 2 | $15 | $30 | Blocks direct light while allowing airflow |
| **Ventilation subtotal** | | | **$100** | |

### 2.5 Door & access upgrades

| Item | Qty | Unit | Total | Notes |
|------|-----|------|-------|-------|
| Personnel-door hinges (heavy-duty) | 3 | $6 | $18 | Access-door hang |
| Weatherproof door latch/lock set | 1 | $30 | $30 | Secure closure |
| Door perimeter weatherstrip + threshold | 1 | $16 | $16 | Light + weather seal |
| Door pull handle + mounting hardware | 1 | $39 | $39 | Firm quote |
| **Door subtotal** | | | **$103** | |

### 2.6 Miscellaneous conversion hardware

| Item | Est. total |
|------|-----------|
| Fasteners, angles, misc. steel | $60 |
| Black spray paint for touchup | $20 |
| Weld repair (if needed, DIY) | $30 |
| **Misc. subtotal** | **$110** |

### Section total

<!-- BEGIN costing:interior -->
| Category | Low | Mid | High |
|----------|-----|-----|------|
| Light-sealing | $157 | $168 | $178 |
| Interior paint | $125 | $125 | $125 |
| Ventilation | $80 | $100 | $130 |
| Door & access | $84 | $102 | $130 |
| Misc. hardware | $80 | $110 | $130 |
| **Interior conversion total** | **$526** | **$605** | **$693** |
<!-- END costing:interior -->

---

## 3. Optics — Pinhole Plate

**Source document:** `container-report.md`, `pinhole-optics-report.md`

The precision aperture is the optical heart of the camera. Optimal diameter for this focal length: **2.17mm** (Rayleigh formula, λ = 550 nm).

### 3.1 Pinhole plate

<!-- BEGIN costing:optics -->
| Item | Low | Mid | High | Notes |
|------|-----|-----|------|-------|
| Custom laser-drilled pinhole, SS-302/304 shim, 3"×3" | $40 | $70 | $100 | Lenox Laser, lenoxlaser.com — ±0.025mm tolerance, SEM-verified |
| Steel backing plate 6"×6"×⅛", welded frame | $20 | $30 | $40 | Houses the precision insert |
| Shutter plate (⅛" steel, 10"×8") + slide channel | $25 | $35 | $50 | Simple sliding shutter, operated from outside |
| Disc retaining ring (Al 6061-T6, M52×0.75 thread) | $15 | $20 | $25 | Screws into the plate counterbore; clamps the disc flat; unscrews for swap/clean |
| **Pinhole plate total** | **$100** | **$155** | **$215** | |
<!-- END costing:optics -->

### 3.2 Optional lens (alternative to or supplement with pinhole)

**Source document:** `lens-options.md`

The pinhole plate is interchangeable. A lens plate can be swapped in for portrait or shorter-exposure work.

| Lens | f | Image circle | Used price | Notes |
|------|---|-------------|-----------|-------|
| Rodenstock Apo-Ronar 1,200mm | f/14 | ~400mm | $400–$1,200 | Primary recommendation — excellent on flat field |
| Nikkor T 1,200mm f/11 | f/11 | ~450mm | $600–$1,500 | One stop faster than Rodenstock |
| Schneider Apo-Symmar 800mm | f/14 | ~500mm | $300–$800 | Shorter focal length; needs separate focus board |
| Acrylic Fresnel 600×600mm @ 1,400mm | f/2.3 | ~600mm | $40–$120 | Cheap artistic option; significant aberrations |

*Lens is an optional upgrade — not required for pinhole operation. Not included in base total.*

---

## 4. Film Plane Mechanism (4-Corner Independent)

**Source document:** `film-plane-mechanism-report.md`

View-camera-style moveable film plane — a **fixed-size rigid** plane whose four corners each ride an acetal skate inside a 6061 Al U-channel depth rail, coupled to a 2-axis 304 cross-slide through a single Belden universal joint — with four independently set corners (TL, TR, BL, BR), enabling tilt (±40°), swing (±28°), and limited compound movements.

The full itemized parts list — specs, SKUs, ICP numbers, per-item quantities — is the [Film Plane Mechanism report Parts List](film-plane-mechanism-report.md), held in the parts registry so it can't drift. The cost roll-up is the [Section total](#section-total) below.

**Wall-seat saddles** — each of the 8 rail ends anchors to the container: **6 with a standalone wall-seat saddle** (back-plate + seat + gusset, through-bolted with a 4-bolt pattern to an exterior wall plate — the container shell carries the rigidity); the **2 bottom-right (BR) ends share a combined corner plate with the right walkway** (costed in §6a / the walkway BoM, not here). The **right** rails are permanently bolted; the **left** rails drop into their saddles on knurled thumb screws so they lift out for the drum swing.

### Optional electric actuation

*Not included in any standard build — Scenarios A–C are all **manual** (each corner is hand-slid along its U-channel and cam-clamped). This is a documented upgrade only (the [Cost Analysis](cost-analysis-report.md) drops it from the recommended build to save ~$827): it motorizes the four corners with PA-14 actuators for entry-free repositioning. See the [Film Plane Mechanism Report §electric actuation](film-plane-mechanism-report.md).*

| Item | Spec | Qty | Unit | Total |
|------|------|-----|------|-------|
| PA-14 linear actuator | 12V, 20" stroke, 150 lb | 4 | $185† | $740 |
| 12V 30A power supply | Enclosed | 1 | $55† | $55 |
| DPDT momentary rocker | Panel-mount, 20A | 4 | $8† | $32 |

### Section total

Line items (Option A, manual handwheel actuation) — **generated from `costing.py`; do not hand-edit the numbers**:

<!-- BEGIN costing:film -->
| Item | Low | Mid | High |
|------|-----|-----|------|
| 6061 Al U-channel depth rails 3×1½" (×4 wall-to-wall) | $327 | $328 | $327 |
| Belden SSNBUJ750x3/8KB needle-bearing U-joints (×4) + keys | $1,014 | $1,016 | $1,018 |
| McMaster 4040N12 304 shaft supports (×4) + 3/8" 304 stub rod (89535K87, 3ft) | $245 | $245 | $245 |
| Acetal skates (×4) — Ø32/Ø20 acetal rollers + 304 axle pins + fab carriage plates | $182 | $230 | $282 |
| 304 flat-bar Z/X cross-slides (×4) + UHMW pads + gibs | $316 | $415 | $516 |
| McMaster 5128A63 hold-down toggle clamps (×12, rail brake) | $155 | $155 | $155 |
| Corner plates, ¼" 304 SS 6×8 (×4) | $236 | $236 | $236 |
| Aluminum angle 2×2×1/8 (6061-T6 plain, expendable) 16 ft (×3) — weld-free frame | $528 | $528 | $528 |
| Dibond ACM 3mm 4×8 black sheets (×4, Option A strips) — single rigid plane | $380 | $380 | $380 |
| Light-seal set — EPDM tape (×2) + Impact duvetyne (57" 9oz, B&H $69) + 4-mil poly + Gorilla tape (×6) | $214 | $214 | $214 |
| Muslin clamps — nylon spring clamp ×58 (Pittsburgh 69289) | $115 | $144 | $173 |
| Muslin clamp filler — HDPE L-channel strip | $30 | $50 | $70 |
| Wall-seat saddles ×6 — 8mm steel plate, cut + welded (ICP-11) | $228 | $228 | $228 |
| Saddle fasteners — M12×65 through-bolts (×28) + M8 thumbscrews (×12) + M8×25 hex bolts (×8) | $140 | $140 | $140 |
| **Section total — film plane mechanism (U-channel + U-joint, incl. saddles)** | **$4,110** | **$4,309** | **$4,512** |
<!-- END costing:film -->

*Electric actuation (optional add-on, not in any standard build): +$827 — see Optional electric actuation above.*

*Includes $145–243 for the muslin clamp system (58 Pittsburgh 69289 nylon spring clamps + HDPE filler). Range reflects generic vs quality.*

---

## 5. Processing Water System

**Source document:** `water-system-report.md`

Self-contained three-circuit water system for remote/off-grid cyanotype processing. Provides ~<!-- BEGIN fact:prints_per_resupply -->15<!-- END fact:prints_per_resupply --> full-size prints (~<!-- BEGIN fact:image_area_sqft -->99<!-- END fact:image_area_sqft --> sq ft each) between water resupply runs, with Brown wash-2 recycling (~8–10 on fresh Blue alone).

<!-- BEGIN costing:water -->
| Category | Low† | High† |
|----------|------|-------|
| Water storage (4× IBC totes, 3× bulkhead fittings, X1 fill tee) | $664 | $664 |
| IBC stacking frame (2×2×0.120in restraint deep 4-leg box + 4 floor feet + 50×20 front retaining bars + wall joist hangers through-bolted to exterior backing plates + fabrication, per [Stacking §9.1](ibc-stacking-report.md)) | $1,309 | $1,872 |
| Pumps and accumulator (P-01/P-02/P-03/P-05 IBC corridor + P-04 tray-drain on the filter skid) | $572 | $572 |
| Corridor plumbing panel structure (23/32" exterior ply backing board + drain-riser spine, 25mm pump-mount shirt, mount brackets + fasteners) | $84 | $109 |
| Pinhole-wall filter-skid backing ply (23/32" exterior, pieced from 2 sheets) | $58 | $58 |
| Under-walkway pipe-ribbon supports (4× welded cross-braces + 16 pipe clips) | $43 | $43 |
| Pump-run support boards + L-brackets + P-clips (corridor side boards, spine, skid) | $44 | $81 |
| Filter skid (3× Big Blue housings + cartridges) | $527 | $527 |
| Captive tee-nut ply-mount hardware (¼-20 + 5/16 pronged tee-nuts + zinc machine screws) | $46 | $46 |
| Valves and fittings (BV/V100/3-way valves, X1 cross, CV-1, SV taps, equalization tie, PVC slip fittings + transition adapters, unions) | $826 | $826 |
| IBC tote flexible connections (8× S60→2" tote adapter + 2→1 reducer + 1" hose barbs + SS clamps) | $181 | $181 |
| Pump flexible connections (braided flex both ports × 5 pumps + 18 barb couplings + 18 SS clamps) | $55 | $55 |
| Pipe (PVC Sch-40 — spray bar + 1"/½" runs) | $84 | $84 |
| Processing tray (304 SS, fabricated, 2 panels) | $1,473 | $2,121 |
| Spray bar assembly (gantry: beam, LDPE pipe, 44 nozzles, single center feed, 4 wheels, ball joint, arm, hose) | $587 | $599 |
| Electrical (wiring only — fuse block in Electrical Report) | $31 | $31 |
| Processing consumables (6-mil poly, pH meter, citric acid) | $257 | $257 |
| **Water system total** | **$6,841** | **$8,126** |
<!-- END costing:water -->

*Used IBC totes (available locally, ~$80–$150 each from Container Exchanger CA) drive significant savings vs. new.*

---

## 6. Housed Revolving-Door Light Lock — Custom Fabrication

**Source document:** `light-trap-selection.md`

Personnel access during operation is via a **Ø900 fixed housing + single-opening C-shell drum** built into the hinged cargo-door panel — light-tight by geometry (two 80° housing openings 180° apart; the drum opening can never bridge both). The drum rotates on two SKF 6215 bearings. The drum and housing from a all-HDPE plastic skin — 5mm UV-HDPE housing + 1/8" HDPE drum. Custom fabrication remains preferred over commercial darkroom doors (~$2,500–$4,500) — those are not weatherproof, transport-rated, or adaptable to a removable panel.

<!-- BEGIN costing:lightlock -->
| Item | Low | Mid | High | Notes |
|------|-----|-----|------|-------|
| 5mm UV-stabilized HDPE — Ø900 housing shell (~7 m²) | $555 | $555 | $555 | rolled + extrusion-welded; TAP / Online Metals |
| 1/8" HDPE — Ø864 drum shell (~7 m²) | $370 | $370 | $370 | TAP / Curbell; caps are now Al (separate line) |
| 8mm 6061-T6 Al plate — 2 drum caps (Ø855, waterjet) | $400 | $550 | $700 | est. material + waterjet, Online Metals (Aug-2026 re-price) |
| 25×25×3 6061-T6 Al angle — 2 rim rings (rolled R427) | $45 | $68 | $90 | shell→cap lap lip; material + roll; est. |
| SKF 6215-2RS1 sealed bearing (×2) | $121 | $121 | $121 | $60.59 ea firm, Bearing World / Applied |
| Bearing retaining rings — 4× DIN 471 (inner) + 1× DIN 472 (outer, upper) | $14 | $14 | $14 | outer-race retention: upper located (shoulder + DIN 472), lower floats; est. |
| 75mm Ø × 150mm steel stub shafts (×2) | $30 | $40 | $50 | steel service center |
| SS blind rivets — shell→cap (97525A425, 100-pack) | $14 | $14 | $14 | $13.83/100 firm, McMaster |
| SS blind rivets — housing→frame (97525A435, 100-pack) | $15 | $15 | $15 | $14.59/100, McMaster |
| 3M Scotch-Weld DP8010 structural adhesive (green, 45 mL) | $76 | $76 | $76 | $76.29 firm, McMaster 7467A36; LSE bond + light-seal for the HDPE laps |
| Al U-channel opening-edge stiffeners (×4) + L-clips + M8 | $55 | $83 | $110 | housing free-edge stiffeners (replaces jamb posts); est. |
| Running-gap wiper — #4 (3/16") black-nylon strip brush ×4 (Gordon/Tanis, 8 ft) | $88 | $124 | $160 | 4 lines snapped into Al flange holders; est., firm at order |
| Al straight-flange holders for the #4 wiper brush ×4 (8 ft) | $72 | $116 | $160 | flange-riveted to the drum OD — rivets clear of the brush; est. |
| 12mm closed-cell neoprene — top/bottom cap wiper seals | $25 | $33 | $40 | cap↔frame seals; the running-gap seal is the drum brush |
| Silicone bead sealant (bearing housing) | $20 | $20 | $20 | Maxisil black 10.5 oz $19.91, Home Depot |
| 12" round pull handle — McMaster 1871A65 | $6 | $6 | $6 | $6.43 firm; off-the-shelf, BOLTED to the stile (1/4" tapped), not welded |
| 40×40×5 SS RHS pull-handle stile (cap→cap) + M12 cap bolts | $50 | $73 | $95 | pull load into the Al caps (not the HDPE wall); est. |
| Matte-black interior finish | $40 | $55 | $70 | scuff + flat-black touch-in |
| Bolts/nuts/isolation washers — cap/ring/collar/stile/handle/edge/housing (SS) | $91 | $91 | $91 | ≈$91 firm, McMaster F1–F7 + W (one pack per line) |
| Rim-angle → beam TEK screws (~24× #14 self-drilling) | $8 | $10 | $12 | weld→TEK (Sheets 9/10); est. |
| M10 twist-resistant rivet-nuts ×20 (95105A199) + setting tool (96349A866) | $53 | $53 | $53 | $53 firm; 14 into the 3mm RHS beam wall (ring/collar→beam) |
| 1/8" blind rivets — brush-holder → drum OD (97447A015, 250-pack) | $11 | $11 | $11 | $10.78 firm; ~72 for the Al holder flanges |
| Fabrication — roll + weld 2 cylinders, roll rim-angle, fit metal caps/bearings (16–22 hrs) | $800 | $975 | $1,150 | Local plastic + metal fab |
| **Housing + drum total** | **$2,959** | **$3,473** | **$3,983** | |
<!-- END costing:lightlock -->

*Note: the hinged panel that the housing mounts into (2×2×0.120in steel frame, 1/8" HDPE plastic skins (18mm-ply Fan-B mount band), EPDM perimeter gasket) is part of the interior conversion covered in Section 2. Still below the $2,500–$4,500 commercial darkroom-door range, and weatherproof + transport-rated.*

---

## 6a. Perimeter Walkway

**Source documents:** `engineering-diagrams.md` §14, `generate_walkway_diagram.py`

Four removable grated walkway sections around all 4 sides of the processing tray. Near walkway widens to <!-- BEGIN fact:walkway_near_wide_w_mm -->500<!-- END fact:walkway_near_wide_w_mm -->mm at EP/battery/slit zone. 140mm deck height to clear the processing tray and spray bar. No tray contact on any section — entire tray interior completely clear for film loading.

Near/far walkways: wall-cantilevered brackets bolted to corrugated wall ribs (13 standard 8mm + 5 widened 10mm).

Right walkway: cantilever rectangle — a closed 2×1×0.120in steel frame on 2 center arms off the IBC corridor uprights, left corners on wall cleats, right corners on combined corner plates shared with the bottom film rail.

Left walkway: removable lift-out grate on 5 floor-leg cantilever brackets bolted to bare floor outside the tray. Arms are extened in the middle punch out section to ease operator egress. Grate lifts out for transport. Butt joints at all corners.

<!-- BEGIN costing:walkway -->
| Item | Low | Mid | High | Notes |
|------|-----|-----|------|-------|
| Molded GRP grating (American Grating cut-to-size) | $835 | $945 | $1,060 | 2026-07-23: PRIMARY American Grating public list ~$830 (2×3'×10' @ $415) + freight/cut band to $1,050; McNichols $1,700.51 held as secondary ceiling. +$5/$10 walkway reconcile rounding |
| GRP grating edge-seal kit (Fibergrate) | $40 | $50 | $60 | field-seal molded FRP cut edges (epoxy, not snap-trim) |
| Standard wall brackets, 8mm steel plate (×13) | $112 | $143 | $175 | Near/far walls; 150mm vert × 300mm arm |
| Widened wall brackets, 10mm steel plate (×5) | $84 | $102 | $134 | EP/battery/slit zone; 200mm vert × 500mm arm (bump extended a 2nd rib toward IBC, X1055–3083 = 5 bays) |
| Reinforcing plates, std 100×180×6mm (×13) + wide 120×220×6mm (×5) | $47 | $60 | $73 | Welded to wall exterior behind each bracket |
| M12×65 partial-thread bolts + nuts + washers (×59) | $137 | $137 | $137 | 91280A728 $1.595 + plain nut 90591A181 $0.256 + 4 flat 91166A290 + split 91202A246 /bolt; 3 per std bracket (39) + 4 per widened (20) |
| Transition bearing plates, 40×500×5mm flat bar (×2) | $5 | $8 | $10 | Welded to arm top at width transitions |
| Right walkway cantilever frame (long + end beams), 2×1×0.120in steel (~5.4m) | $125 | $139 | $153 | rev12: closed rectangle (2 long + 2 end beams); the 2 center arms are IBC-owned (see the IBC frame §5) |
| Right walkway wall cleats, 8mm steel (×2) | $20 | $28 | $35 | Left corners — through-bolted to the wall |
| Combined corner plates, 10mm steel (×2) | $50 | $65 | $80 | Right corners — shared with the bottom film rail |
| M12×70 partial-thread bolts + nuts/washers (~20) | $53 | $53 | $53 | 91280A732 $1.736 + plain nut + 4 flat + split /bolt; wall cleats + combined plates (arms bolt via the J6 end-plate, now IBC-frame §5) |
| 316 SS hold-down clips (FRP M/G-clip, ×20) | $25 | $32 | $40 | Near/far/right walkway GRP grating retention |
| Drum-exit punch-out — extra GRP grating (~0.23 m²) | $50 | $57 | $65 | 600mm-deep landing at the light-lock exit |
| Left floor-leg cantilever brackets (×5) | $65 | $80 | $105 | 2×2×0.120in posts + 2×1×0.120in arms + foot plates |
| Floor screws — #14×2″ HWH 410 SS self-drilling (×20) | $7 | $9 | $11 | 2026-07-22: wedge anchors → structural self-drillers (ply-over-steel container floor); Bridge Fasteners ~$0.35–0.55 ea |
| Fabrication (brackets, cantilever frame, install) | $424 | $590 | $750 | 13 std + 5 widened brackets, right cantilever frame, 5 left floor-leg brackets, install; bracket scope matches the walkway-report §10 all-in figures; trimmed −$30/−$58 to reconcile with the parts registry after the M12 bolts firmed to real flat prices |
| **Perimeter walkway total** | **$2,079** | **$2,498** | **$2,941** | |
<!-- END costing:walkway -->

---

## 6b. Panel Swing Pivot

**Source documents:** `equipment-layout-report.md` §6.1, `hinged-panel-report.md` §4–5

The panel + drum SWING ~56° about a vertical Ø89×8mm CHS pivot post, carrying the punch-out bay inboard of the door plane so the cargo doors close. See the rotation-hardware detail in [master-shopping-list.md](master-shopping-list.md) §7a.

<!-- BEGIN costing:swingpivot -->
| Item | Low | Mid | High | Notes |
|------|-----|-----|------|-------|
| Ø89×8 CHS pivot post + machined hub / thrust collar | $180 | $240 | $300 | carries ~3.6 kN·m swing cantilever; Metal Supermarkets / local fab |
| Turntable thrust bearing, 12″ (Ø305) 1000 lb | $80 | $80 | $80 | VXB |
| Flanged sleeve (journal) bearings, Ø90 bore (×2) | $261 | $261 | $261 | McMaster SAE 841 |
| Drum support cage, 1.5×1.5×0.120in steel SHS | $70 | $95 | $120 | Local fab |
| Top + bottom wall stays + 4-bolt anchor plates | $90 | $105 | $120 | turnbuckles + rods + plates |
| Drop-in rail saddles + tapered dowels (×4, removable left film rails) | $80 | $105 | $130 | Local fab / McMaster |
| Fixed door frame — 2×2×0.120in members (×3) | $90 | $105 | $120 | Metal Supermarkets |
| Fixed door frame — top/bottom seal lips (3mm steel ~110×4m) | $128.5 | $128.5 | $128.5 | seal paths #3–#4 |
| Fixed door frame — welding/fabrication + wall attachment | $129 | $129 | $129 | Local fab |
| **Panel swing pivot + door frame total** | **$938.5** | **$1,208.5** | **$1,478.5** | |
<!-- END costing:swingpivot -->

---

## 7. Printmaking — 50 Prints (Cyanotype)

**Source document:** `chemistry-shopping-list.md`

Cyanotype is the chosen process: no silver, no DEA registration, no hazmat shipping, processing in plain water. Cost is lowest of all processes evaluated at this scale.

### 7.1 Chemistry and substrate (50 prints)

> **⚠ Chemistry is a RANGE — pending [Sensitizer Trials](sensitizer-trials.md).** The
> **Mike Ware New Cyanotype** formula: ammonium iron(III) oxalate (**AmFe**),
> **3:1 AmFe:ferricyanide ratio**, and **two wet-on-wet coats** over the 9.42 m² active plane.
> Per-print AmFe is **260–780 g** by concentration tier (Lean ⅓-Ware / Standard ½-Ware / Rich full-Ware —
> operating-manual §0.2), so the chemistry cost spans a wide band until a tier is trialled. **Standard
> (½-Ware) is the working default.**

<!-- BEGIN costing:chemistry-7-1 -->
| Item (50 prints) | Lean (⅓-Ware) | **Standard (½-Ware) — default** | Rich (full-Ware) | Source |
|---|---|---|---|---|
| Ferric ammonium oxalate (AmFe) | 11.4 kg / ~$730 | **17.1 kg / ~$1,100** | 34.2 kg / ~$2,200 | Artcraft Chemicals (~$64/kg) |
| Potassium ferricyanide (3:1 ratio) | 3.8 kg / ~$194 | **5.7 kg / ~$291** | 11.4 kg / ~$582 | Artcraft Chemicals ($51/kg) |
| Ammonium dichromate (contrast, 0.1–0.4%) | ~$25 | **~$25** | ~$25 | Artcraft Chemicals |
| Unbleached cotton muslin, 60″ — 3 × 150-yd rolls (~360 yd) | ~$300 | **~$300** | ~$300 | Fabric Direct (~$100/roll) |
| **Cyanotype total — 50 prints** | **~$1,250** | **~$1,710** | **~$3,100** | |
<!-- END costing:chemistry-7-1 -->

*Note: development requires only plain cold water — no darkroom chemistry. The §5 water system provides all wash water.*

*Muslin sizing: three 60″ strips cover the <!-- BEGIN fact:film_plane_width_mm -->4,389<!-- END fact:film_plane_width_mm --> mm width (× <!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm --> mm tall = ~21 ft/print); 50 prints + 15% waste = ~400 yd = **3 × 150-yd rolls ≈ $300 (~$6/print)**.*

### 7.2 Per-print cost (cyanotype — Standard ½-Ware tier; range locked by trial)

| Component | Cost per print (Standard) |
|-----------|---------------|
| Ferric ammonium oxalate (AmFe, Part A) | ~$75 |
| Potassium ferricyanide (Part B) | ~$3 |
| Ammonium dichromate (contrast) | ~$0.50 |
| Muslin substrate (~<!-- BEGIN fact:image_area_sqft -->99<!-- END fact:image_area_sqft --> sq ft = ~9 yd of 60″ + 15% waste) | ~$6 |
| Water & consumables (6-mil liner, gloves) | ~$3 |
| **Total per print (Standard)** | **~$36** |

*Across tiers, chemistry moves the per-print total to ~**$27 (Lean) – ~$63 (Rich)**; the [Sensitizer Trials](sensitizer-trials.md) lock the tier. Muslin is ~$6/print (see §7.1), so the §7.1 totals = this per-print × 50 (± the $3/print consumables that §7.1 excludes).*

### 7.3 Alternative process cost comparison

| Process | 50-print total† | Per print | Key constraint |
|---------|----------------|-----------|----------------|
| **Cyanotype** | **~<!-- BEGIN costing:s73-50run-range -->$1,400–3,250<!-- END costing:s73-50run-range -->** (Std ~<!-- BEGIN costing:s73-50run-std -->$1,850<!-- END costing:s73-50run-std -->)‡ | **~<!-- BEGIN costing:s73-pp-range -->$28–65<!-- END costing:s73-pp-range -->** (Std ~<!-- BEGIN costing:s73-pp-std -->$37<!-- END costing:s73-pp-std -->)‡ | None — easiest |
| Gum bichromate | ~$5,150 | ~$103 | Hazmat shipping (dichromate) |
| Van Dyke Brown | ~$11,000 | ~$220 | DEA form; AgNO₃ price volatility |
| Ilford RC paper | ~$20,500 | ~$410 | Paper rolls very expensive at this size |
| Liquid Light on muslin | ~$21,800 | ~$436 | Contact Rockland for bulk pricing |
| Salt print | ~$26,900 | ~$538 | 3× more silver than Van Dyke — not recommended |

*Silver nitrate is the cost driver for Van Dyke, salt print, and Liquid Light. Cyanotype and gum bichromate are the only processes under $5,000 for a 50-print run.*

*‡ Cyanotype chemistry is a **range** pending [Sensitizer Trials](sensitizer-trials.md) — the corrected Ware-3:1 / two-coat figures swing the per-print AmFe (and the 50-print chemistry cost) by up to ~4.6×. Muslin is ~$300 / ~$6 per print (§7.1). The Standard (½-Ware) tier is the working default.*

---

## 8. Transportation

**Source document:** `container-transport-options.md`

Costs are **per deployment** (one move). The container requires no oversize/overweight permit when empty on Interstate highways.

### 8.1 Commercial hire (no CDL required)

| Move type | Option | Per-move cost |
|-----------|--------|--------------|
| Local (<30 miles) | Tilt-bed delivery truck | $300–$500† |
| Short haul (30–100 miles) | Tilt-bed delivery truck | $500–$1,200† |
| Long distance (100–300 miles) | Semi flatbed | $1,200–$2,500† |
| Cross-country (>1,000 miles) | Semi flatbed | $3,500–$6,000† |

*If no forklift at destination: add $200–$1,200 for crane truck or forklift rental.*

### 8.2 Self-haul (capital investment, requires CDL)

| Equipment | Purchase cost | Notes |
|-----------|--------------|-------|
| QuickLoadz 20k trailer (self-loading, no crane needed) | $30,000–$40,000† | F-250+ pickup required |
| Container chassis 20 ft (used gooseneck) | $5,000–$15,000† | Requires crane/forklift at destination |
| Used Class 7 tilt-bed truck | $65,000–$100,000† | Class B CDL required |

*Self-haul only makes economic sense if the container will be moved 60–80+ times (break-even vs. hire at ~$600/move).*

### 8.3 Chassis + semi rental (frequent repositioning, CDL required)

| Item | Day rate† | Week rate† |
|------|----------|-----------|
| Container chassis (FlexiVan FlexiDay) | $30–$60 | $175–$350 |
| Semi tractor (Penske/Ryder) | $200–$400 | $1,000–$1,800 |
| **Combined** | **$230–$460/day** | **$1,175–$2,150/wk** |

---

## 9. Licenses & Permits

**Source document:** `container-transport-options.md`; location permit costs are estimates not covered by existing research.

### 9.1 CDL (if self-hauling)

| Item | Cost† |
|------|-------|
| DOT medical examination | $75–$150 |
| DMV fees (CLP + CDL + tests) | $170–$220 |
| CDL training — budget private school (Class A) | $2,000–$3,000 |
| CDL training — mid-range / community college (Class A) | $4,000–$6,200 |
| **CDL all-in (mid-range + medical + DMV)** | **~$4,345–$6,570** |

*CDL Class A is recommended — covers both tilt-bed truck operation (Class B) and semi tractor operation (Class A). El Camino College Torrance: $5,995 all-inclusive including DMV fees. WIOA funding may cover full tuition for eligible applicants.*

*CDL is only required if self-hauling. Commercial hire (Sections 7.1) requires no license from the customer.*

### 9.2 Location / filming permits

Permit requirements vary by jurisdiction. Estimates below are based on general knowledge — no specific research document covers this.

| Location type | Permit | Typical cost | Notes |
|---------------|--------|-------------|-------|
| Public road / street (California) | City/county film permit | $0–$500/day | Many small cities waive fees for non-commercial art |
| LA County parks | Parks filming permit | $250–$500/day | Recreation & Parks Dept |
| California State Parks | State filming permit | $200–$500/day | CDPR Film Office |
| Private land | Negotiated with landowner | $0–$2,000/day | Most affordable for rural locations |
| Federal land (BLM, Forest Service) | Special Use Permit | $50–$150 processing fee + $150–$1,500/day | Site-specific |
| Commercial operation (selling prints) | Business license | $50–$200/year | City of operation |

*For a non-commercial art/documentary deployment at a single location: budget $0–$500 for permit costs. For regular commercial touring: budget $500–$2,000/deployment.*

### 9.3 Permits summary (per deployment, non-commercial art use)

| Item | Low | Mid | High |
|------|-----|-----|------|
| Location permit | $0 | $200 | $500 |
| Business license (annual, prorated) | $10 | $25 | $50 |
| Misc. (insurance certificate, site access) | $0 | $75 | $200 |
| **Licenses & permits per deployment** | **$10** | **$300** | **$750** |

*CDL costs are one-time and listed separately above. If CDL is obtained, add $4,345–$6,570 to the project total.*

---

## 10. Ongoing Operating Costs (After Build)

### Per print (cyanotype, after initial capital spent)

| Item | Cost |
|------|------|
| Muslin substrate | ~$43 |
| Sensitizer chemistry | ~$21 |
| Water (32 gal Blue circuit) | ~$0.35 (if resupplied by tanker at ~$0.01/gal) |
| Containment poly & consumables | ~$2 |
| Filter cartridge amortized (4.5×20; replace every ~40–60 prints) | ~$5 |
| **Per-print running cost** | **~$71** |

### Per deployment

| Item | Cost |
|------|------|
| Transport (short haul, commercial hire) | $300–$800 |
| Water resupply (~420 gal / <!-- BEGIN fact:blue_supply_l -->1,800<!-- END fact:blue_supply_l -->L Blue ≈ <!-- BEGIN fact:prints_per_resupply -->15<!-- END fact:prints_per_resupply --> prints) | $25–$50 |
| Location permit | $0–$500 |
| **Per-deployment overhead** | **~$325–$1,350** |

---

## 11. Complete Budget Scenarios

### Scenario A — Minimum viable build, local use, commercial hire transport

<!-- BEGIN costing:scenario-a -->
| Item | Cost |
|------|------|
| Container (WWT) + delivery | $1,800 |
| Interior conversion (minimal) | $526 |
| Pinhole plate | $100 |
| Film plane mechanism (4-corner U-channel + U-joint, incl. wall-seat saddles) | $4,110 |
| Water system (incl. processing tray, spray bar, IBC stacking frame) | $6,841 |
| Power & electrical system (solar · 1× LiFePO4 · distribution · lighting · protection · master pump switch) | $3,431 |
| Ventilation & cooling system (2 fans · evap cooler + inverter · light-safe baffle-duct fab · shade canopy) | $748 |
| Revolving drum light trap (plastic-skin custom fabrication) | $2,959 |
| Perimeter walkway (4 sections, removable, GRP grating) | $2,079 |
| Panel swing pivot + fixed door frame (Ø89 pivot + bearings + cage + wall stays + saddles + door frame) | $1,180 |
| Hinged panel structure (stepped frame + HDPE skins + Al core + EPDM + latches + B2 bay + handle) | $1,278 |
| Chemistry prep shelf (fold-down board + tap trunk extension) | $223 |
| Cyanotype chemistry + substrate (50 prints) | $1,250 |
| Transport per deployment (local) | $400 |
| Permits (minimal) | $50 |
| **Scenario A total** | **~$26,975** |
<!-- END costing:scenario-a -->

### Scenario B — Recommended build, regional deployment

<!-- BEGIN costing:scenario-b -->
| Item | Cost |
|------|------|
| Container (CW) + delivery | $3,150 |
| Interior conversion (full) | $605 |
| Pinhole plate | $155 |
| Film plane mechanism (4-corner U-channel + U-joint + wall-seat saddles) | $4,309 |
| Water system (incl. processing tray, spray bar, IBC stacking frame) | $7,478 |
| Power & electrical system (solar · 1× LiFePO4 · distribution · lighting · protection · master pump switch) | $3,464 |
| Ventilation & cooling system (2 fans · evap cooler + inverter · light-safe baffle-duct fab · shade canopy) | $808 |
| Revolving drum light trap (plastic-skin custom fabrication) | $3,473 |
| Perimeter walkway (4 sections, removable, GRP grating) | $2,498 |
| Panel swing pivot + fixed door frame (Ø89 pivot + bearings + cage + wall stays + saddles + door frame) | $1,395 |
| Hinged panel structure (stepped frame + HDPE skins + Al core + EPDM + latches + B2 bay + handle) | $1,382 |
| Chemistry prep shelf (fold-down board + tap trunk extension) | $229 |
| Cyanotype chemistry + substrate (50 prints) | $1,710 |
| Rodenstock Apo-Ronar 1,200mm lens | $800 |
| Transport per deployment (50–100 miles) | $900 |
| Permits (typical public land) | $300 |
| **Scenario B total (excl. CDL)** | **~$32,656** |
<!-- END costing:scenario-b -->

### Scenario C — Full production, own transport, CDL

<!-- BEGIN costing:scenario-c -->
| Item | Cost |
|------|------|
| Scenario B build (less the $900 commercial transport, replaced here by owned transport) | $31,756 |
| CDL Class A training + medical + DMV | $4,500 |
| QuickLoadz self-loading trailer | $35,000 |
| Ford F-350+ pickup (if needed) | $50,000–$80,000 (new) |
| **Scenario C total** | **~$121,256–$151,256** |
<!-- END costing:scenario-c -->

*Own transport only makes sense if the camera will be deployed frequently. For fewer than 60 moves, commercial hire is cheaper.*

---

## 12. Research Gaps & Cost Verification Required

The following costs are not covered by existing research documents and should be verified before committing:

| Item | Status | Action |
|------|--------|--------|
| Wall-seat saddle plate steel (ICP-11) | Estimated ~$3–5/kg | Confirm at Metal Supermarkets SoCal (walk-in) or Online Metals for 8mm mild-steel plate; ~28 kg needed (8 saddles, laser/plasma cut) |
| Saddle clamps for 2in (50.8mm) steel tube (ICP-12) | Estimated ~$10 ea. | Confirm at McMaster-Carr (steel tube clamps category) — verify fit for 2×2in (50.8mm) square section |
| M8 thumbscrews DIN 464 SS (ICP-13) | Estimated ~$2–5 ea. | Amazon multi-packs typical; Maedler NA PN 65499225 confirmed at ~$15–17 ea. (May 2026) |
| Ball-lock pins Ø10mm SS (ICP-14) | Estimated ~$6–10 ea. | Confirm at McMaster-Carr ball lock pins category; verify 50mm usable length fits joint |
| Lenox Laser pinhole fabrication price | Estimated | Request quote at lenoxlaser.com — specify 2.17mm ±0.025mm in SS-302 shim, 75mm × 75mm |
| Grimco ACM panel pricing | Listed at ~$85† | Confirm current price; Grimco City of Industry: 626-912-9600 |
| Rockland Liquid Light bulk pricing | Unconfirmed | Contact rockaloid.com before committing to that process |
| Silver nitrate bulk pricing | Volatile | Get quote within 2 weeks of ordering — AgNO₃ price can shift 20–30%/month |
| Location permit fees | Estimated | Check specific jurisdiction's film permit office before site selection |
| Commercial photography insurance | Not researched | General liability + inland marine for equipment; estimate $800–$2,000/year |
| Site preparation (levelling, power, fencing) | Not researched | Highly site-specific; budget $0–$5,000 depending on location |
