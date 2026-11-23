<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Complete Project Cost Breakdown

**Basis:** Ranges given where source documents provide them; midpoints used for totals. Costs marked † are from detailed procurement research in supporting documents; others are estimates.

**Related:** [Master Shopping List](master-shopping-list.md) (per-item procurement with suppliers and URLs) · [Funding Proposal](funding-proposal.md) (grant-ready summary at three funding levels)

---

## 1. Summary — Total Project Cost

<!-- BEGIN costing:scenario -->
| Category | Low | Mid | High |
|----------|-----|-----|------|
| **1. Container purchase & delivery** | $2,300 | $3,300 | $4,300 |
| **2. Interior conversion** | $446 | $505 | $563 |
| **3. Optics — pinhole wall interface** | $35 | $52 | $70 |
| **4. Film plane mechanism (4-corner U-channel + acetal skate + U-joint, incl. wall-seat saddles)** | $3,933 | $4,159 | $4,391 |
| **5. Processing water system (incl. tray, spray bar, IBC stacking frame)** | $6,989 | $7,670 | $8,355 |
| **5a. Power & electrical system (solar · 1× LiFePO4 · MPPT · distribution · lighting · protection · master pump switch + drain-pump switches)** | $3,449 | $3,502 | $3,555 |
| **5b. Ventilation & cooling system (2 fans · evap cooler **+ 12V→120V inverter** · light-safe baffle-duct fab · shade canopy)** | $788 | $848 | $938 |
| **6. Housed revolving-door light lock (plastic-skin custom fabrication)** | $3,156 | $3,667 | $4,175 |
| **6a. Perimeter walkway (4 sections + drum-exit punch-out)** | $2,290 | $2,722 | $3,177 |
| **6b. Panel swing pivot + fixed door frame (Ø89 post + bearings + cage + wall stays + rail saddles)** | $1,286 | $1,526 | $1,766 |
| **6c. Hinged panel structure (stepped frame + HDPE skins + Al core + EPDM + cam latches + B2 bay + pull handle)** | $1,195 | $1,282 | $1,368 |
| **6d. Chemistry prep shelf (fold-down UV-white ply board + hinge/stays + TAP-01 trunk extension)** | $268 | $275 | $280 |
| **7. Printmaking — 50 prints (cyanotype; Low=Lean, Mid=Standard, High=Rich tier)** | $1,230 | $1,680 | $3,040 |
| **8. Transportation (per deployment)** | $300 | $750 | $2,000 |
| **9. Licenses & permits (per-deployment permits; High adds CDL)** | $10 | $300 | $7,320 |
| **TOTAL (excl. own transport, lens)** | **$27,675** | **$32,238** | **$45,298** |
<!-- END costing:scenario -->

*Line 7 (cyanotype printmaking) brackets the **Mike Ware New Cyanotype** concentration tiers — **Low = Lean ⅓-Ware, Mid = Standard ½-Ware, High = Rich full-Ware** — including the ~<!-- BEGIN costing:pcb-muslin-run -->$300<!-- END costing:pcb-muslin-run --> muslin substrate (§10.1). The [Sensitizer Trials](sensitizer-trials.md) pin the tier.*

*Optional additions that may apply — see individual sections:*

<!-- BEGIN costing:optional-additions -->
| Optional item | Low | Mid | High |
|---------------|-----|-----|------|
| Lens (Rodenstock / Nikkor, used) | $400 | $800 | $1,500 |
| Own transport vehicle (QuickLoadz trailer) | $30,000 | $35,000 | $40,000 |
<!-- END costing:optional-additions -->

---

## 2. Container Purchase & Delivery

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

**If a long-distance delivery is required** (100–300 miles, semi flatbed): add <!-- BEGIN costing:pcb-delivery-long -->$1,200–$2,500<!-- END costing:pcb-delivery-long --> (§11.1).

---

## 3. Interior Conversion

**Source document:** `container-report.md`

Converting the container interior from cargo hold to pinhole camera. Includes light-sealing, interior painting, and door upgrades. The itemized interior parts, with suppliers and prices, are in the [Master Shopping List](master-shopping-list.md?system=interior). The section roll-up:

### Section total

<!-- BEGIN costing:interior -->
| Category | Low | Mid | High |
|----------|-----|-----|------|
| Light-sealing | $157 | $168 | $178 |
| Interior paint | $125 | $125 | $125 |
| Door & access | $84 | $102 | $130 |
| Misc. hardware | $80 | $110 | $130 |
| **Interior conversion total** | **$446** | **$505** | **$563** |
<!-- END costing:interior -->

---

## 4. Optics — Pinhole Wall Interface

**Source document:** `pinhole-report.md`, `pinhole-disc-holder-report.md`

The pinhole/lens **mount** is the [pinhole disc holder](pinhole-disc-holder-report.md) in the front-board system. Its Ø80 carrier takes either the pinhole or a lens, and it carries the pinhole element, retaining ring and mount bolts. This section is the **wall interface** the front board bolts to.

### 4.1 Pinhole wall interface

<!-- BEGIN costing:optics -->
| Item | Low | Mid | High | Notes |
|------|-----|-----|------|-------|
| Wall-frame adapter plate + weld | $20 | $30 | $40 | Flat steel adapter welded over the corrugation; 4× M6 @ Ø150 datum |
| Aperture dark slide / cap | $15 | $22 | $30 | Light-tight cover over the aperture between exposures |
| **Wall-interface total** | **$35** | **$52** | **$70** | |
<!-- END costing:optics -->

### 4.2 Optional large-format lens

**Source document:** `lens-options.md`

The disc holder takes a Copal/Compur **lens board** (0/1/3) in place of a pinhole board — for portrait or shorter-exposure work. Focus is set at the film plane (depth rail).

Used process lenses that cover the plane run ~<!-- BEGIN costing:pcb-lens-range -->$400–$1,500<!-- END costing:pcb-lens-range -->; the candidates and their coverage are compared in [Lens Options](lens-options.md).

*Lens is an optional upgrade — not required for pinhole operation. Not included in base total.*

---

## 5. Film Plane Mechanism (4-Corner Independent)

**Source document:** `film-plane-mechanism-report.md`

A view-camera-style movable film plane: a **fixed-size rigid** plane with four independently set corners (TL, TR, BL, BR). Each corner rides an acetal skate in a U-channel depth rail, coupled to a 2-axis cross-slide through one universal joint. That gives tilt (±<!-- BEGIN fact:film_plane_max_tilt -->40<!-- END fact:film_plane_max_tilt -->°), swing (±<!-- BEGIN fact:film_plane_max_swing -->28<!-- END fact:film_plane_max_swing -->°) and limited compound movements.

The full itemized parts list is the [Film Plane Mechanism report Parts List](film-plane-mechanism-report.md), held in the parts registry. The cost roll-up is the [Section total](#section-total) below.

**Wall-seat saddles** — each of the 8 rail ends anchors to the container: **4 on a standalone wall-seat saddle**, the **2 far-left ends on the pivot-post floor/roof mount plates**, and the **2 bottom-right (BR) ends on a corner plate shared with the right walkway**. The **right** rails are permanently bolted; the **left** rails drop into their saddles on knurled thumb screws so they lift out for the drum swing.

### Section total

Line items (Option A, manual handwheel actuation) — **generated from `costing.py`; do not hand-edit the numbers**:

<!-- BEGIN costing:film -->
| Item | Low | Mid | High |
|------|-----|-----|------|
| 6061 Al U-channel depth rails 3×1½" (×4 wall-to-wall) | $327 | $328 | $327 |
| Belden SSNBUJ750x3/8KB needle-bearing U-joints (×4) + keys | $1,010 | $1,010 | $1,010 |
| McMaster 4040N12 304 shaft supports (×4) + 3/8" 304 stub rod (89535K87, 3ft) | $284 | $284 | $284 |
| Acetal skates (×4) — Ø32/Ø20 acetal rollers + 304 axle pins + fab carriage plates | $214 | $262 | $314 |
| 304 flat-bar Z/X cross-slides (×4) + UHMW pads + gibs | $316 | $415 | $516 |
| McMaster 5128A63 hold-down toggle clamps (×12, rail brake) | $155 | $155 | $155 |
| Corner plates, ¼" 304 SS 6×8 (×4) | $101 | $130 | $161 |
| Aluminum angle 2×2×1/8 (6061-T6 plain, expendable) 16 ft (×3) — weld-free frame | $45 | $45 | $45 |
| Dibond ACM 3mm 4×8 black sheets (×4, Option A strips) — single rigid plane | $528 | $528 | $528 |
| Light-seal set — EPDM tape (×2) + Impact duvetyne (57" 9oz, B&H $69) + 4-mil poly + Gorilla tape (×6) | $380 | $380 | $380 |
| Muslin clamps — nylon spring clamp ×58 (Pittsburgh 69289) | $1 | $1 | $1 |
| Muslin clamp filler — HDPE L-channel strip | $115 | $144 | $173 |
| Wall-seat saddles ×6 — 8mm steel plate, cut + welded (ICP-11) | $30 | $50 | $70 |
| Saddle fasteners — M12×70 through-bolts (×28) + M8 thumbscrews (×12) + M8×25 hex bolts (×8) | $228 | $228 | $228 |
| **Section total — film plane mechanism (U-channel + U-joint, incl. saddles)** | **$3,933** | **$4,159** | **$4,391** |
<!-- END costing:film -->


---

## 6. Processing Water System

**Source document:** `water-system-report.md`

Self-contained three-circuit water system for remote/off-grid cyanotype processing. Provides ~<!-- BEGIN fact:prints_per_resupply -->15<!-- END fact:prints_per_resupply --> full-size prints (~<!-- BEGIN fact:image_area_sqft -->99<!-- END fact:image_area_sqft --> sq ft each) between water resupply runs, with Brown wash-1 recycling (~<!-- BEGIN fact:prints_no_recycle -->10<!-- END fact:prints_no_recycle --> on fresh Blue alone).

<!-- BEGIN costing:water -->
| Category | Low† | High† |
|----------|------|-------|
| Water storage (4× IBC totes, 3× bulkhead fittings, X1 fill tee) | $664 | $664 |
| IBC stacking frame (2×2×0.120in restraint deep 4-leg box + 4 floor feet + 50×20 front retaining bars + wall joist hangers through-bolted to exterior backing plates + fabrication, per [Stacking](ibc-stacking-report.md)) | $1,419 | $2,036 |
| Pumps and accumulator (P-01/P-02/P-03/P-05 IBC corridor + P-04 tray-drain on the filter skid) | $572 | $572 |
| Corridor plumbing panel structure (23/32" exterior ply backing board + drain-riser spine, 25mm pump-mount shirt, mount brackets + fasteners) | $40 | $40 |
| Pinhole-wall filter-skid backing ply (23/32" exterior, pieced from 2 sheets) | $58 | $58 |
| Under-walkway pipe-ribbon supports (4× welded cross-braces + 16 pipe clips) | $43 | $43 |
| Pump-run support boards + L-brackets + P-clips (corridor side boards, spine, skid) | $65 | $99 |
| Filter skid (3× Big Blue housings + cartridges) | $527 | $527 |
| Captive tee-nut ply-mount hardware (¼-20 + 5/16 pronged tee-nuts + zinc machine screws) | $37 | $37 |
| Valves and fittings (BV/V100/3-way valves, X1 cross, CV-1, SV taps, equalization tie, PVC slip fittings + transition adapters, unions) | $860 | $907 |
| IBC tote flexible connections (8× S60→2" tote adapter + 2→1 reducer + 1" hose barbs + SS clamps) | $209 | $209 |
| Pump flexible connections (braided flex both ports × 5 pumps + 18 barb couplings + 18 SS clamps) | $55 | $55 |
| Pipe (PVC Sch-40 — spray bar + 1"/½" runs) | $84 | $84 |
| Processing tray (304 SS, fabricated, 2 panels) | $1,473 | $2,121 |
| Spray bar assembly (gantry: beam, LDPE pipe, 43 nozzles, single center feed, 4 wheels, ball joint, arm, hose) | $595 | $615 |
| Electrical (wiring only — fuse block in Electrical Report) | $31 | $31 |
| Processing consumables (6-mil poly, pH meter, citric acid) | $257 | $257 |
| **Water system total** | **$6,989** | **$8,355** |
<!-- END costing:water -->

*The budget prices used IBC totes, sourced locally (Container Exchanger CA), well below new.*

---

## 7. Housed Revolving-Door Light Lock — Custom Fabrication

**Source document:** `light-trap-selection.md`

Personnel enter through a **Ø800 fixed housing + single-opening C-shell drum** in the hinged cargo-door panel. It is light-tight by geometry: the housing's two 80° openings sit 180° apart, so the drum opening can never bridge both. The drum turns on two SKF 6215 bearings; housing and drum are HDPE skins (5mm UV-HDPE housing, 1/8" drum). It is custom-built because commercial darkroom doors (~$2,500–$4,500) are not weatherproof, transport-rated, or adaptable to a removable panel.

<!-- BEGIN costing:lightlock -->
| Item | Low | Mid | High | Notes |
|------|-----|-----|------|-------|
| 5mm (3/16in) UV-stabilized HDPE — Ø800 housing shell (~7 m²) | $555 | $555 | $555 | rolled + extrusion-welded; TAP / Online Metals |
| 1/8" HDPE — Ø764 drum shell (~7 m²) | $370 | $370 | $370 | TAP / Curbell; caps are now Al (separate line) |
| 8mm 6061-T6 Al plate — 2 drum caps (Ø755, waterjet) | $400 | $550 | $700 | est. material + waterjet, Online Metals (Aug-2026 re-price) |
| 25×25×3 6061-T6 Al angle — 2 rim rings (rolled R427) | $45 | $68 | $90 | shell→cap lap lip; material + roll; est. |
| SKF 6215-2RS1 sealed bearing (×2) | $121 | $121 | $121 | $60.59 ea firm, Bearing World / Applied |
| Bearing retaining rings + upper end-retainer plate — 3× DIN 471 (inner) + 1× DIN 472 (outer) + Ø90×4 plate | $17 | $17 | $18 | upper hub hang on a bolted end plate (not a lone circlip); outer race located (shoulder + DIN 472), lower floats; firm |
| 75mm Ø × 150mm steel stub shafts (×2) | $30 | $40 | $50 | steel service center |
| SS blind rivets — shell→cap (97525A425, 100-pack) | $14 | $14 | $14 | $13.83/100 firm, McMaster |
| SS blind rivets — housing→frame (97525A435, 100-pack) | $15 | $15 | $15 | $14.59/100, McMaster |
| 3M Scotch-Weld DP8010 structural adhesive (green, 45 mL) | $76 | $76 | $76 | $76.29 firm, McMaster 7467A36; LSE bond + light-seal for the HDPE laps |
| Al U-channel opening-edge stiffeners (×4) + L-clips + M8 | $152 | $152 | $152 | housing free-edge stiffeners (replaces jamb posts); rivet-only 2026-09-08; est. |
| Al U-channel — rotating-drum opening-edge stiffeners (×2) + rivets | $30 | $43 | $55 | drum free-edge stiffeners (2026-09-08); rivet-only; est. |
| Formed-Al strip channel-support beams (×4) + rivets | $69 | $69 | $69 | one across each housing opening top+bottom, rail-to-rail so the U-channels rivet to a member; SS blind-riveted to the frame beams; smallest formed section (SKU pending); est. |
| Running-gap wiper — #4 (3/16") black-nylon strip brush ×4 (Gordon/Tanis, 8 ft) | $88 | $124 | $160 | 4 lines snapped into Al flange holders; est., firm at order |
| Al straight-flange holders for the #4 wiper brush ×4 (8 ft) | $72 | $116 | $160 | flange-riveted to the drum OD — rivets clear of the brush; est. |
| 12mm closed-cell neoprene — top/bottom cap wiper seals | $25 | $33 | $40 | cap↔frame seals; the running-gap seal is the drum brush |
| Silicone bead sealant (bearing housing) | $12 | $16 | $20 | Maxisil black 10.5 oz $19.91, Home Depot |
| 12" round pull handle — McMaster 1871A65 | $20 | $20 | $20 | $6.43 firm; off-the-shelf, BOLTED to the stile (1/4" tapped), not welded |
| 40×40×5 SS RHS pull-handle stile (cap→cap) + M12 cap bolts | $6 | $6 | $6 | pull load into the Al caps (not the HDPE wall); est. |
| Matte-black interior finish | $50 | $73 | $95 | scuff + flat-black touch-in |
| Bolts/nuts/isolation washers — cap/ring/collar/stile/handle/edge/housing (SS) | $40 | $55 | $70 | ≈$91 firm, McMaster F1–F7 + W (one pack per line) |
| SS blind rivets — housing skin → outer beam face (97525A425, 100-pack) | $95 | $95 | $95 | 2026-09-08: rim-angle dropped, skin fixes directly to the outer beam face (Sheets 9/10); $13.83/100 firm |
| M10 twist-resistant rivet-nuts ×20 (95105A199) + setting tool (96349A866) | $14 | $14 | $14 | $53 firm; 14 into the 3mm RHS beam wall (ring/collar→beam) |
| 1/8" blind rivets — brush-holder → drum OD (97447A015, 250-pack) | $24 | $34 | $44 | $10.78 firm; ~72 for the Al holder flanges |
| Fabrication — roll + weld 2 cylinders, roll rim-angle, fit metal caps/bearings (16–22 hrs) | $16 | $16 | $16 | Local plastic + metal fab |
| **Housing + drum total** | **$3,156** | **$3,667** | **$4,175** | |
<!-- END costing:lightlock -->

*Note: the hinged panel that the housing mounts into (2×2×0.120in steel frame, 1/8" HDPE plastic skins (18mm-ply Fan-B mount band), EPDM perimeter gasket) is part of the interior conversion covered in Section 2.*

---

## 8. Perimeter Walkway

**Source documents:** `engineering-diagrams.md` §14, `generate_walkway_diagram.py`

Four removable grated walkway sections surround the processing tray. The near walkway widens to <!-- BEGIN fact:walkway_near_wide_w_mm -->500<!-- END fact:walkway_near_wide_w_mm -->mm at the EP/battery/slit zone. The 140mm deck clears the tray and spray bar, and no section touches the tray, so its whole interior stays clear for loading the muslin.

Near/far walkways: wall-cantilevered brackets bolted to corrugated wall ribs (13 standard 8mm + 5 widened 10mm).

Right walkway: cantilever rectangle — a closed 2×1×0.120in steel frame on 2 center arms off the IBC corridor uprights, left corners on wall cleats, right corners on combined corner plates shared with the bottom film rail.

Left walkway: removable lift-out grate on 5 floor-leg cantilever brackets bolted to bare floor outside the tray. The arms extend further in the middle punch-out section to ease egress. Grate lifts out for transport. Butt joints at all corners.

<!-- BEGIN costing:walkway -->
| Item | Low | Mid | High | Notes |
|------|-----|-----|------|-------|
| Molded GRP grating (American Grating cut-to-size) | $835 | $945 | $1,060 | 2026-07-23: PRIMARY American Grating public list ~$830 (2×3'×10' @ $415) + freight/cut band to $1,050; McNichols $1,700.51 held as secondary ceiling. +$5/$10 walkway reconcile rounding |
| GRP grating edge-seal kit (Fibergrate) | $40 | $50 | $60 | field-seal molded FRP cut edges (epoxy, not snap-trim) |
| Standard wall brackets, 8mm steel plate (×13) | $112 | $143 | $175 | Near/far walls; 150mm vert × 300mm arm |
| Widened wall brackets, 10mm steel plate (×5) | $84 | $102 | $134 | EP/battery/slit zone; 200mm vert × 500mm arm (bump extended a 2nd rib toward IBC, X1055–3083 = 5 bays) |
| Reinforcing plates, std 100×180×6mm (×13) + wide 120×220×6mm (×5) | $47 | $60 | $73 | Welded to wall exterior behind each bracket |
| M12×70 partial-thread bolts + nuts + washers (×59) | $141 | $141 | $141 | 91280A728 $1.595 + plain nut 90591A181 $0.256 + 4 flat 91166A290 + split 91202A246 /bolt; 3 per std bracket (39) + 4 per widened (20) |
| Transition bearing plates, 40×500×5mm flat bar (×2) | $116 | $116 | $117 | Welded to arm top at width transitions |
| Right walkway cantilever frame (long + end beams), 2×1×0.120in steel (~5.4m) | $5 | $8 | $10 | rev12: closed rectangle (2 long + 2 end beams); the 2 center arms are IBC-owned (see the IBC frame §5) |
| Right walkway wall cleats, 8mm steel (×2) | $125 | $139 | $153 | Left corners — through-bolted to the wall |
| Combined corner plates, 10mm steel (×2) | $94 | $94 | $93 | Right corners — shared with the bottom film rail |
| M12×70 partial-thread bolts + nuts/washers (~20) | $20 | $28 | $35 | 91280A732 $1.736 + plain nut + 4 flat + split /bolt; wall cleats + combined plates (arms bolt via the CJ end-plate, now IBC-frame §5) |
| 316 SS hold-down clips (FRP M/G-clip, ×20) | $50 | $65 | $80 | Near/far/right walkway GRP grating retention |
| Left floor-leg cantilever brackets (×5) | $53 | $53 | $53 | 2×2×0.120in posts + 2×1×0.120in arms + foot plates |
| Floor-anchor sub-plate (strongback) + self-drilling TEKs + leg bolts | $25 | $32 | $40 | One continuous self-tapped sub-plate under the 5-leg line (the legs sit at ~one X; cross-member pitch not standardized). ~1,900×350×8 steel (material est) + #14×3½″ TEKs (×20) + 20× M12×30 leg bolts into tapped bosses; finalized on the acquired container |
| Fabrication (brackets, cantilever frame, install) | $65 | $80 | $105 | 13 std + 5 widened brackets, right cantilever frame, 5 left floor-leg brackets, install; bracket scope matches the walkway-report §10 all-in figures; trimmed −$30/−$58 to reconcile with the parts registry after the M12 bolts firmed to real flat prices |
| **Perimeter walkway total** | **$2,290** | **$2,722** | **$3,177** | |
<!-- END costing:walkway -->

---

## 9. Panel Swing Pivot

**Source documents:** `hinged-panel-report.md` §4–5

The panel + drum SWING ~56° about a vertical Ø89×8mm CHS pivot post, carrying the punch-out bay inboard of the door plane so the cargo doors close. See the rotation-hardware detail in [Master Shopping List](master-shopping-list.md?system=swing).

<!-- BEGIN costing:swingpivot -->
| Item | Low | Mid | High | Notes |
|------|-----|-----|------|-------|
| Ø89×8 CHS pivot post + machined hub / thrust collar | $180 | $240 | $300 | carries ~3.6 kN·m swing cantilever; Metal Supermarkets / local fab |
| Turntable thrust bearing, 12″ (Ø305) 1000 lb | $70 | $95 | $120 | VXB |
| Flanged sleeve (journal) bearings, Ø90 bore (×2) | $80 | $80 | $80 | McMaster SAE 841 |
| Drum support cage, 1.5×1.5×0.120in steel SHS | $261 | $261 | $261 | Local fab |
| Top + bottom wall stays + 4-bolt anchor plates | $70 | $95 | $120 | turnbuckles + rods + plates |
| Drop-in rail saddles + tapered dowels (×4, removable left film rails) | $90 | $105 | $120 | Local fab / McMaster |
| Fixed door frame — 50×20×3 RHS members (×3) | $36 | $36 | $36 | Metal Supermarkets |
| Fixed door frame — top/bottom seal lips (3mm steel ~110×4m) | $128.5 | $128.5 | $128.5 | seal paths #3–#4 |
| Fixed door frame — welding/fabrication + wall attachment | $80 | $105 | $130 | Local fab |
| **Panel swing pivot + door frame total** | **$938.5** | **$1,208.5** | **$1,478.5** | |
<!-- END costing:swingpivot -->

---

## 10. Printmaking — 50 Prints (Cyanotype)

**Source document:** `chemistry-shopping-list.md`

Cyanotype is the chosen process: no silver, no DEA registration, no hazmat shipping, processing in plain water. Cost is lowest of all processes evaluated at this scale.

### 10.1 Chemistry and substrate (50 prints)

> **⚠ Chemistry is a RANGE — pending [Sensitizer Trials](sensitizer-trials.md).** The
> **Mike Ware New Cyanotype** formula: ammonium iron(III) oxalate (**AmFe**),
> **3:1 AmFe:ferricyanide ratio**, and **two wet-on-wet coats** over the <!-- BEGIN fact:image_area_m2 -->9.19<!-- END fact:image_area_m2 --> m² active plane.
> Per-print AmFe is **<!-- BEGIN costing:pcb-amfe-g-range -->222–668<!-- END costing:pcb-amfe-g-range --> g** by concentration tier (Lean ⅓-Ware / Standard ½-Ware / Rich full-Ware —
> operating-manual §0.2), so the chemistry cost spans a wide band until a tier is trialled. **Standard
> (½-Ware) is the working default.**

<!-- BEGIN costing:chemistry-7-1 -->
| Item (50 prints) | Lean (⅓-Ware) | **Standard (½-Ware) — default** | Rich (full-Ware) | Source |
|---|---|---|---|---|
| Ferric ammonium oxalate (AmFe) | 11.1 kg / ~$710 | **16.7 kg / ~$1,070** | 33.4 kg / ~$2,140 | Artcraft Chemicals (~$64/kg) |
| Potassium ferricyanide (3:1 ratio) | 3.7 kg / ~$189 | **5.6 kg / ~$286** | 11.1 kg / ~$566 | Artcraft Chemicals ($51/kg) |
| Ammonium dichromate (optional contrast, 0.1–0.4%) | ~$25 | **~$25** | ~$25 | Artcraft Chemicals |
| Unbleached cotton muslin, 60″ — 3 × 150-yd rolls (~360 yd) | ~$300 | **~$300** | ~$300 | Fabric Direct (~$100/roll) |
| **Cyanotype total — 50 prints** | **~$1,230** | **~$1,680** | **~$3,040** | |
<!-- END costing:chemistry-7-1 -->

*Note: development requires only plain cold water — no darkroom chemistry. The §6 water system provides all wash water.*

*Muslin sizing: three 60″ strips cover the <!-- BEGIN fact:film_plane_width_mm -->4,389<!-- END fact:film_plane_width_mm --> mm width (× <!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm --> mm tall = ~21 ft/print); 50 prints + 15% waste = ~<!-- BEGIN costing:pcb-muslin-yd -->360<!-- END costing:pcb-muslin-yd --> yd = **<!-- BEGIN costing:pcb-muslin-rolls -->3 × 150-yd rolls<!-- END costing:pcb-muslin-rolls --> ≈ <!-- BEGIN costing:pcb-muslin-run -->$300<!-- END costing:pcb-muslin-run --> (~<!-- BEGIN costing:pcb-pp-muslin -->$6<!-- END costing:pcb-pp-muslin -->/print)**.*

### 10.2 Per-print cost (cyanotype — Standard ½-Ware tier; range locked by trial)

| Component | Cost per print (Standard) |
|-----------|---------------|
| Ferric ammonium oxalate (AmFe, Part A) | ~<!-- BEGIN costing:pcb-pp-amfe -->$21<!-- END costing:pcb-pp-amfe --> |
| Potassium ferricyanide (Part B) | ~<!-- BEGIN costing:pcb-pp-ferri -->$6<!-- END costing:pcb-pp-ferri --> |
| Ammonium dichromate (optional contrast) | ~<!-- BEGIN costing:pcb-pp-dichromate -->$0.50<!-- END costing:pcb-pp-dichromate --> |
| Muslin substrate (~<!-- BEGIN fact:image_area_sqft -->99<!-- END fact:image_area_sqft --> sq ft = ~9 yd of 60″ + 15% waste) | ~<!-- BEGIN costing:pcb-pp-muslin -->$6<!-- END costing:pcb-pp-muslin --> |
| Water & consumables (6-mil liner, gloves) | ~<!-- BEGIN costing:pcb-pp-consumables -->$3<!-- END costing:pcb-pp-consumables --> |
| **Total per print (Standard)** | **~<!-- BEGIN costing:pcb-pp-total -->$37<!-- END costing:pcb-pp-total -->** |

*Across tiers, chemistry moves the per-print total to ~**<!-- BEGIN costing:pcb-pp-range -->$28 (Lean) – $64 (Rich)<!-- END costing:pcb-pp-range -->**; the [Sensitizer Trials](sensitizer-trials.md) lock the tier. Muslin is ~<!-- BEGIN costing:pcb-pp-muslin -->$6<!-- END costing:pcb-pp-muslin -->/print (see §10.1), so the §10.1 totals = this per-print × 50, less the ~<!-- BEGIN costing:pcb-pp-consumables -->$3<!-- END costing:pcb-pp-consumables -->/print consumables that §10.1 excludes.*

### 10.3 Alternative process cost comparison

| Process | 50-print total† | Per print | Key constraint |
|---------|----------------|-----------|----------------|
| **Cyanotype** | **~<!-- BEGIN costing:s73-50run-range -->$1,400–3,200<!-- END costing:s73-50run-range -->** (Std ~<!-- BEGIN costing:s73-50run-std -->$1,850<!-- END costing:s73-50run-std -->)‡ | **~<!-- BEGIN costing:s73-pp-range -->$28–64<!-- END costing:s73-pp-range -->** (Std ~<!-- BEGIN costing:s73-pp-std -->$37<!-- END costing:s73-pp-std -->)‡ | None — easiest |
| Gum bichromate | ~$5,150 | ~$103 | Hazmat shipping (dichromate) |
| Van Dyke Brown | ~$11,000 | ~$220 | DEA form; AgNO₃ price volatility |
| Ilford RC paper | ~$20,500 | ~$410 | Paper rolls very expensive at this size |
| Liquid Light on muslin | ~$21,800 | ~$436 | Contact Rockland for bulk pricing |
| Salt print | ~$26,900 | ~$538 | 3× more silver than Van Dyke — not recommended |

*Silver nitrate is the cost driver for Van Dyke, salt print, and Liquid Light. Cyanotype and gum bichromate are the only processes under $5,000 for a 50-print run.*

*‡ Cyanotype chemistry is a **range** pending [Sensitizer Trials](sensitizer-trials.md) — the per-print AmFe (and the 50-print chemistry cost) spans the concentration tier (Lean → Rich, <!-- BEGIN costing:pcb-tier-x -->3<!-- END costing:pcb-tier-x -->×) times the unmeasured muslin coverage (<!-- BEGIN costing:pcb-cov-range -->100–180<!-- END costing:pcb-cov-range --> ml/m²/coat, <!-- BEGIN costing:pcb-cov-x -->1.8<!-- END costing:pcb-cov-x -->×): up to ~<!-- BEGIN costing:pcb-chem-x -->5.4<!-- END costing:pcb-chem-x -->× end to end. Muslin is ~$300 / ~$6 per print (§10.1). The Standard (½-Ware) tier is the working default.*

---

## 11. Transportation

**Source document:** `container-transport-options.md`

Costs are **per deployment** (one move). The container requires no oversize/overweight permit when empty on Interstate highways.

### 11.1 Commercial hire (no CDL required)

| Move type | Option | Per-move cost |
|-----------|--------|--------------|
| Local (<30 miles) | Tilt-bed delivery truck | <!-- BEGIN costing:pcb-delivery-local -->$300–$500†<!-- END costing:pcb-delivery-local --> |
| Short haul (30–100 miles) | Tilt-bed delivery truck | <!-- BEGIN costing:pcb-delivery-short -->$500–$1,200†<!-- END costing:pcb-delivery-short --> |
| Long distance (100–300 miles) | Semi flatbed | <!-- BEGIN costing:pcb-delivery-long-row -->$1,200–$2,500†<!-- END costing:pcb-delivery-long-row --> |
| Cross-country (>1,000 miles) | Semi flatbed | <!-- BEGIN costing:pcb-delivery-xc -->$3,500–$6,000†<!-- END costing:pcb-delivery-xc --> |

*If no forklift at destination: add $200–$1,200 for crane truck or forklift rental.*

### 11.2 Self-haul (capital investment, requires CDL)

| Equipment | Purchase cost | Notes |
|-----------|--------------|-------|
| QuickLoadz 20k trailer (self-loading, no crane needed) | <!-- BEGIN costing:pcb-trailer -->$30,000–$40,000†<!-- END costing:pcb-trailer --> | F-250+ pickup required |
| Container chassis 20 ft (used gooseneck) | $5,000–$15,000† | Requires crane/forklift at destination |
| Used Class 7 tilt-bed truck | $65,000–$100,000† | Class B CDL required |

*Self-haul only makes economic sense if the container will be moved 60–80+ times (break-even vs. hire at ~$600/move).*

### 11.3 Chassis + semi rental (frequent repositioning, CDL required)

| Item | Day rate† | Week rate† |
|------|----------|-----------|
| Container chassis (FlexiVan FlexiDay) | $30–$60 | $175–$350 |
| Semi tractor (Penske/Ryder) | $200–$400 | $1,000–$1,800 |
| **Combined** | **$230–$460/day** | **$1,175–$2,150/wk** |

---

## 12. Licenses & Permits

**Source document:** `container-transport-options.md`; location permit costs are estimates not covered by existing research.

### 12.1 CDL (if self-hauling)

<!-- BEGIN costing:cdl -->
| Item | Cost† |
|------|-------|
| DOT medical examination | $75–$150 |
| DMV fees (CLP + CDL + tests) | $170–$220 |
| CDL training — budget private school (Class A) | $2,000–$3,000 |
| CDL training — mid-range / community college (Class A) | $4,000–$6,200 |
| **CDL all-in (community college + medical + DMV)** | **~$4,245–$6,570** |
<!-- END costing:cdl -->

*CDL Class A is recommended — covers both tilt-bed truck operation (Class B) and semi tractor operation (Class A). El Camino College Torrance: $5,995 all-inclusive including DMV fees. WIOA funding may cover full tuition for eligible applicants.*

*CDL is only required if self-hauling. Commercial hire (§11.1) requires no license from the customer.*

### 12.2 Location / filming permits

Permit requirements vary by jurisdiction. Estimates below are based on general knowledge — no specific research document covers this.

| Location type | Permit | Typical cost | Notes |
|---------------|--------|-------------|-------|
| Public road / street (California) | City/county film permit | $0–$500/day | Many small cities waive fees for non-commercial art |
| LA County parks | Parks filming permit | $250–$500/day | Recreation & Parks Dept |
| California State Parks | State filming permit | $200–$500/day | CDPR Film Office |
| Private land | Negotiated with landowner | $0–$2,000/day | Most affordable for rural locations |
| Federal land (BLM, Forest Service) | Special Use Permit | $50–$150 processing fee + $150–$1,500/day | Site-specific |
| Commercial operation (selling prints) | Business license | $50–$200/year | City of operation |

*For a non-commercial art/documentary deployment at a single location: budget <!-- BEGIN costing:pcb-permit-range -->$0–$500<!-- END costing:pcb-permit-range --> for permit costs. For regular commercial touring: budget $500–$2,000/deployment.*

### 12.3 Section total

<!-- BEGIN costing:licenses-permits -->
| Item | Low | Mid | High |
|------|-----|-----|------|
| CDL Class A — training + DOT medical + DMV (High only: self-haul; one-time, §12.1) | $0 | $0 | $6,570 |
| Location permit (§12.2) | $0 | $200 | $500 |
| Business license (annual, prorated) | $10 | $25 | $50 |
| Misc. (insurance certificate, site access) | $0 | $75 | $200 |
| **9. Licenses & permits total** | **$10** | **$300** | **$7,320** |
<!-- END costing:licenses-permits -->

*The baseline is commercial hire (§11.1), which needs no CDL, so Low and Mid carry permits only. High carries the one-time CDL for self-hauling. The permit lines recur per deployment (non-commercial art use).*

---

## 13. Ongoing Operating Costs (After Build)

### Per print (cyanotype, after initial capital spent)

<!-- BEGIN costing:running-per-print -->
| Item | Cost |
|------|------|
| Muslin substrate | ~$6 |
| Sensitizer chemistry (Standard tier, incl. the optional dichromate allowance) | ~$28 |
| Water (30 gal Blue, tanker at ~$0.01/gal) | ~$0.30 |
| Processing consumables (liner, gloves, citric acid, pH) | ~$3 |
| Filter cartridges, amortized (est.) | ~$5 |
| Roller, brush and glove restock (one printing session) | ~$50 |
| **Per-print running cost** | **~$92** |
<!-- END costing:running-per-print -->

### Per deployment

<!-- BEGIN costing:running-per-deployment -->
| Item | Cost |
|------|------|
| Transport (short haul, commercial hire — §2 delivery line) | $300–$800 |
| Water resupply (tanker) | $25–$50 |
| Location permit (§12.3) | $0–$500 |
| **Per-deployment overhead** | **~$325–$1,350** |
<!-- END costing:running-per-deployment -->

---

## 14. Complete Budget Scenarios

### Scenario A — Minimum viable build, local use, commercial hire transport

<!-- BEGIN costing:scenario-a -->
| Item | Cost |
|------|------|
| Container (WWT) + delivery | $1,800 |
| Interior conversion (minimal) | $446 |
| Pinhole plate | $35 |
| Film plane mechanism (4-corner U-channel + U-joint, incl. wall-seat saddles) | $3,933 |
| Water system (incl. processing tray, spray bar, IBC stacking frame) | $6,989 |
| Power & electrical system (solar · 1× LiFePO4 · distribution · lighting · protection · master pump switch) | $3,449 |
| Ventilation & cooling system (2 fans · evap cooler + inverter · light-safe baffle-duct fab · shade canopy) | $788 |
| Revolving drum light trap (plastic-skin custom fabrication) | $3,156 |
| Perimeter walkway (4 sections, removable, GRP grating) | $2,290 |
| Panel swing pivot + fixed door frame (Ø89 pivot + bearings + cage + wall stays + saddles + door frame) | $1,286 |
| Hinged panel structure (stepped frame + HDPE skins + Al core + EPDM + latches + B2 bay + handle) | $1,195 |
| Chemistry prep shelf (fold-down board + tap trunk extension) | $268 |
| Cyanotype chemistry + substrate (50 prints) | $1,230 |
| Transport per deployment (local) | $400 |
| Permits (minimal) | $50 |
| **Scenario A total** | **~$27,315** |
<!-- END costing:scenario-a -->

### Scenario B — Recommended build, regional deployment

<!-- BEGIN costing:scenario-b -->
| Item | Cost |
|------|------|
| Container (CW) + delivery | $3,150 |
| Interior conversion (full) | $505 |
| Pinhole plate | $52 |
| Film plane mechanism (4-corner U-channel + U-joint + wall-seat saddles) | $4,159 |
| Water system (incl. processing tray, spray bar, IBC stacking frame) | $7,670 |
| Power & electrical system (solar · 1× LiFePO4 · distribution · lighting · protection · master pump switch) | $3,502 |
| Ventilation & cooling system (2 fans · evap cooler + inverter · light-safe baffle-duct fab · shade canopy) | $848 |
| Revolving drum light trap (plastic-skin custom fabrication) | $3,667 |
| Perimeter walkway (4 sections, removable, GRP grating) | $2,722 |
| Panel swing pivot + fixed door frame (Ø89 pivot + bearings + cage + wall stays + saddles + door frame) | $1,526 |
| Hinged panel structure (stepped frame + HDPE skins + Al core + EPDM + latches + B2 bay + handle) | $1,282 |
| Chemistry prep shelf (fold-down board + tap trunk extension) | $275 |
| Cyanotype chemistry + substrate (50 prints) | $1,680 |
| Rodenstock Apo-Ronar 1,200mm lens | $800 |
| Transport per deployment (50–100 miles) | $900 |
| Permits (typical public land) | $300 |
| **Scenario B total (excl. CDL)** | **~$33,038** |
<!-- END costing:scenario-b -->

### Scenario C — Full production, own transport, CDL

<!-- BEGIN costing:scenario-c -->
| Item | Cost |
|------|------|
| Scenario B build (less the $900 commercial transport, replaced here by owned transport) | $32,138 |
| CDL Class A training + medical + DMV | $6,570 |
| QuickLoadz self-loading trailer | $35,000 |
| Ford F-350+ pickup (if needed) | $50,000–$80,000 (new) |
| **Scenario C total** | **~$123,708–$153,708** |
<!-- END costing:scenario-c -->

*Own transport only makes sense if the camera will be deployed frequently. For fewer than 60 moves, commercial hire is cheaper.*

---

## 15. Cost Confidence

Most lines are firm registry prices ([Master Shopping List](master-shopping-list.md)). These remain
estimates, and the scenario bands in §14 carry them:

| Item | Basis | Status |
|------|-------|--------|
| Wall-seat saddle plate (ICP-11, 4 saddles) | 8mm + 10mm A36 plate, cut; welded by the owner | Estimate; firmed by a fab quote once the blueprints are final |
| Pinhole carrier set (Lenox Laser) | Laser-drilled SS-302 shim on 6061 discs, $20–40 each | Quote pending |
| Location permit fees (§12) | Typical jurisdiction fees | Varies by jurisdiction |
| Commercial photography insurance | General liability + inland marine, ~$800–$2,000/year | Not in the budget; not researched |
| Site preparation (leveling, power, fencing) | $0–$5,000 | Not in the budget; site-specific |

The alternative-process figures in §10.3 (Liquid Light and the silver-nitrate processes) are
comparison estimates only. They are not part of the budget.

## 16. See Also

- [Master Shopping List](master-shopping-list.md) — the itemized by-type BOM
- [Cost Analysis](cost-analysis-report.md) — scenario cost modeling and levers
- [Proposal](funding-proposal.md) — the funding case
