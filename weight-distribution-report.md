<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Weight Distribution Analysis

## 1. Purpose

This report provides a comprehensive weight analysis of TBS-001, covering:

- Total weight of the container with all equipment installed (dry)
- Total weight with all liquids added (camera ready)
- Weight distribution (front-back, left-right) for three operational states
- Center-of-gravity (CG) position and migration between states
- ISO container gross weight compliance verification

The analysis is essential for transport planning, trailer axle placement,
structural assessment, and understanding how the system's weight distribution
changes during a photographic session.

---

## 2. Container Baseline

| Parameter | Value | Source |
|-----------|-------|--------|
| Container type | 20 ft standard ISO | ISO 668 |
| Tare weight (empty container) | 2,200 kg (4,850 lbs) | Hapag-Lloyd Container Spec |
| Max gross weight | 24,000 kg (52,910 lbs) | ISO 668 |
| Max payload | 21,800 kg (48,060 lbs) | Gross − tare |
| Interior dimensions | 5,893 × 2,362 × 2,388mm | ISO 668 |

---

## 3. Component Weight Inventory

All weights are calculated from first principles (material density × volume)
unless a specific report value is cited. Material densities used:
mild steel 7,850 kg/m³, 304 SS 7,930 kg/m³, aluminum 2,700 kg/m³,
marine plywood 600 kg/m³, polypropylene (PP plastic sheet) 905 kg/m³,
UV-HDPE 950 kg/m³, water 1,000 kg/m³.

### 3.1 Container

| Component | Weight (kg) | Position | Calculation Basis |
|-----------|------------|----------|-------------------|
| Container shell (excl. doors) | 1,920 | Full footprint | Hapag-Lloyd 20ft ISO tare (2,200 kg) minus doors (280 kg) |
| Cargo door — near leaf | 140 | Closed: X=−100 to −40 / Open: along near wall | ISO door leaf, ~140 kg each |
| Cargo door — far leaf | 140 | Closed: X=−100 to −40 / Open: along far wall | ISO door leaf, ~140 kg each |

### 3.2 Structural Components

| Component | Weight (kg) | X Range (mm) | Yd Range (mm) | Calculation Basis |
|-----------|------------|-------------|---------------|-------------------|
| Hinged panel (incl. Ø900 housing + punch-out bay) | 171 | 0–80 (deployed); swung ~56° about the pivot (transport) | 0–2,362 | Framed panel: 4mm-PP plastic skins + 18mm-ply Fan-B mount band + 3mm-Al corner cores + 50×50×3 steel RHS center ≈ 125 kg + bolted 5mm-HDPE Ø900 housing ≈ 22 kg + 4mm-PP punch-out bay ≈ 25 kg (first-principles). The Ø89 pivot post + bearings + cage are counted under "Swing pivot + cage hardware". See [Hinged Panel Report §2.4–2.5](hinged-panel-report.md) for the full movable-assembly breakdown |
| Light-trap drum (rotating) | 38 | 0–40 (deployed); swung ~56° about the pivot (transport) | 653–1,709 | Ø864 C-shell, 4mm PP plastic skin, no fins (suspended with panel) + PP end caps + steel Ø75 stub shafts + 2× SKF 6215 bearings |
| Processing tray | 116 | 170–4,629 | 80–2,280 | 304 SS 1.5mm, 2 panels × 58 kg ([Water System Report](water-system-report.md) §4) |
| Near walkway | 37 | 470–4,629 | 0–300 | 10 brackets @ ~2.7 kg + 11 kg/m² GRP grating |
| Far walkway | 37 | 470–4,629 | 2,062–2,362 | Same as near walkway |
| Right walkway | 44 | 4,329–4,629 | 0–2,362 | Cantilever-rectangle: closed frame (2 long + 2 end beams) + 2 center cantilever arms off the IBC uprights (40×40×3 SHS) + wall cleats + combined corner plates (shared with the BR film rail) + GRP grating |
| Left walkway | 25 | 170–470 | 0–2,362 | Removable lift-out: GRP grating + 5 floor-leg cantilever brackets (50×50 post + arm on bare floor outside the tray) + drum-exit punch-out (deeper grating) |
| Swing pivot + cage hardware | 38 | 0–400 | 700–2,287 | Rotation transport hardware: pivot bearings + collar + drum cage + wall stays + rail saddles, at the cargo-door end. Estimate — refine vs the rotation-hardware BOM |
| Container mods | 65 | Distributed | Distributed | Light seal foam + reinforcement plates (estimate) |
| Chem-prep shelf (fold-down, stowed) | 7 | 1,180–1,780 | 0–22 | Wall-hinged fold-down: 18mm phenolic ply + 2" Al angle frame + spill lip + continuous piano hinge + 2 stays ≈ 7 kg. Modeled **stowed** (folded up vs the pinhole wall) in all states; the ~25 kg deployed mixing load is a transient prep case (film plane parked) — see [Chemistry Prep Shelves §3](chemistry-prep-shelves.md) |
| **Structure subtotal** | **<!-- BEGIN weight:wt-cat-structure -->584<!-- END weight:wt-cat-structure -->** | | | |

### 3.3 Equipment

| Component | Weight (kg) | X Range (mm) | Yd Range (mm) | Calculation Basis |
|-----------|------------|-------------|---------------|-------------------|
| Electrical panel | 15 | 1,910–2,210 | 0–150 | Wall-mount distribution panel |
| Battery bank | 13 | 1,540–2,220 | 0–150 | 1× 100Ah LiFePO4 @ 13 kg (standard build; +13 kg for the optional 2nd pack) |
| Solar controller | 2 | 1,700–1,800 | 0–100 | MPPT charge controller |
| Plumbing — Corridor panel | 5 | 4,760–4,874 | 1,046–1,160 | 4× Shurflo 2088 (P-01/P-03/P-04/P-05) + ACC-01 |
| Plumbing — Pinhole Wall panel | 8 | 3,300–4,016 | 12–196 | P-02 + 3-stage Big Blue filter (dry); on the pinhole wall — est. |
| Film plane carriage | 32 | 150–4,649 | 2,212–2,312 | Anodized 6061 Al angle frame (50.8×50.8×4.8mm; EXPENDABLE — kept aluminum for weight + cost, replace on pitting) + 90 cam-lever clamps + 4 HGH20CA carriages |
| Tilt-swing board | 30 | 2,089–2,709 | 0–100 | 620×620×45mm Al plate + spherical pivot + screws |
| Fans (A+B) | 4 | End walls | Near corners | 2× 150mm axial panel fans |
| Baffle ducts | 6 | Distributed | Distributed | 2× galvanized steel baffle ducts |
| Blue IBC-1 (tote) | 65 | 4,674–5,893 | 30–1,046 | 1,000L caged composite tare (top tier, near) |
| Blue IBC-2 (tote) | 65 | 4,674–5,893 | 1,316–2,332 | 1,000L caged composite tare (top tier, far) |
| Brown IBC-3 (tote) | 65 | 4,674–5,893 | 30–1,046 | 1,000L caged composite tare (bottom tier, near) |
| Waste IBC-4 (tote) | 65 | 4,674–5,893 | 1,316–2,332 | 1,000L caged composite tare (bottom tier, far) |
| IBC restraint frame | 90 | 4,654–5,104 | 1,046–1,316 | 50×50×3mm RHS restraint-only deep 4-leg box (totes direct-stack cage-on-cage): 4 full-height uprights (front pair X4654 + back pair X5104) + top/bottom rings + 4 floor flange feet + front retaining bars + 4 wall joist hangers (through-bolted to 4 exterior backing plates) + rear-panel brackets ([Equipment Layout](equipment-layout-report.md) §5) |
| **Equipment subtotal** | **<!-- BEGIN weight:wt-cat-equipment -->465<!-- END weight:wt-cat-equipment -->** | | | |

### 3.4 Dry Weight Summary

| Category | Weight (kg) | % of Dry Total |
|----------|------------|---------------|
| Container (shell + doors) | <!-- BEGIN weight:wt-cat-container -->2,200<!-- END weight:wt-cat-container --> | <!-- BEGIN weight:wt-pct-container -->67.7<!-- END weight:wt-pct-container -->% |
| Structure | <!-- BEGIN weight:wt-cat-structure -->584<!-- END weight:wt-cat-structure --> | <!-- BEGIN weight:wt-pct-structure -->18.0<!-- END weight:wt-pct-structure -->% |
| Equipment | <!-- BEGIN weight:wt-cat-equipment -->465<!-- END weight:wt-cat-equipment --> | <!-- BEGIN weight:wt-pct-equipment -->14.3<!-- END weight:wt-pct-equipment -->% |
| **Total dry** | **<!-- BEGIN weight:wt-total-dry -->3,249<!-- END weight:wt-total-dry -->** | **100%** |

**Grating weight assumption:** 5/8" (15mm) molded GRP (fiberglass) grating,
vinyl-ester resin with grit top, weighs approximately 11 kg/m² over the 4.14 m²
of deck. GRP is specified for corrosion immunity in the wet photo-chemistry
environment, at a cost premium of ~$720–$890 (see [cost breakdown §6a](project-cost-breakdown.md)).
The 15mm depth keeps the lowered deck and the spray-bar carriage clearance under
the left cantilever arms unchanged. Confirm the final product's kg/m² against its
datasheet; a 1"/25mm GRP would weigh more and force a deck-height redesign.

---

## 4. Liquid States

### 4.1 Camera Ready (Full Blue IBCs)

All wash water loaded in the two top-tier Blue IBCs. Bottom-tier Brown and
Waste IBCs are empty. Processing tray is empty (water is pumped to the tray
during processing, not pre-loaded).

| Liquid | Volume (L) | Weight (kg) | Position | Tier |
|--------|-----------|------------|----------|------|
| Blue IBC-1 water | 900 | 900 | X=4,674–5,893, Yd=30–1,046 | Top (Z=1,336–2,236) |
| Blue IBC-2 water | 900 | 900 | X=4,674–5,893, Yd=1,316–2,332 | Top (Z=1,336–2,236) |
| **Total liquid** | **1,800** | **1,800** | | |

**Total loaded weight: <!-- BEGIN weight:wt-total-loaded -->5,049<!-- END weight:wt-total-loaded --> kg** (<!-- BEGIN weight:wt-total-dry -->3,249<!-- END weight:wt-total-dry --> dry + 1,800 liquid)

### 4.2 Materials Exhausted (Ready for Resupply)

After a full session, wash water has been consumed and redistributed.
Blue IBCs are empty; Brown (recycled) and Waste IBCs hold the ~<!-- BEGIN fact:recovered_l -->1,260<!-- END fact:recovered_l -->L
recovered (~<!-- BEGIN fact:collection_fill_l -->630<!-- END fact:collection_fill_l -->L each). The processing tray has been drained; the other
~<!-- BEGIN fact:lost_l -->434<!-- END fact:lost_l -->L was lost to the open process (evaporation, wet-print carryout,
unrecovered residual — see [water-system report §4](water-system-report.md)).

| Liquid | Volume (L) | Weight (kg) | Position | Tier |
|--------|-----------|------------|----------|------|
| Brown IBC-3 water | 630 | 630 | X=4,674–5,893, Yd=30–1,046 | Bottom (Z=168–798) |
| Waste IBC-4 water | 630 | 630 | X=4,674–5,893, Yd=1,316–2,332 | Bottom (Z=168–798) |
| Processing tray | — | 0 | Drained | — |
| **Total liquid** | **1,260** | **1,260** | | |

**Total exhausted weight: <!-- BEGIN weight:wt-total-exhausted -->4,509<!-- END weight:wt-total-exhausted --> kg** (<!-- BEGIN weight:wt-total-dry -->3,249<!-- END weight:wt-total-dry --> dry + 1,260 liquid)

### 4.3 State Comparison

| State | Total (kg) | X_cg (mm) | Yd_cg (mm) | Z_cg (mm) | Front/Rear | Near/Far |
|-------|-----------|-----------|------------|-----------|------------|----------|
| Dry (Transport) | <!-- BEGIN weight:wt-dry-total -->3,249<!-- END weight:wt-dry-total --> | <!-- BEGIN weight:wt-dry-x -->2,724<!-- END weight:wt-dry-x --> | <!-- BEGIN weight:wt-dry-yd -->1,193<!-- END weight:wt-dry-yd --> | <!-- BEGIN weight:wt-dry-z -->1,096<!-- END weight:wt-dry-z --> | <!-- BEGIN weight:wt-dry-fr -->54.0<!-- END weight:wt-dry-fr -->/<!-- BEGIN weight:wt-dry-rr -->46.0<!-- END weight:wt-dry-rr -->% | <!-- BEGIN weight:wt-dry-nr -->48.5<!-- END weight:wt-dry-nr -->/<!-- BEGIN weight:wt-dry-fa -->51.5<!-- END weight:wt-dry-fa -->% |
| Loaded Transport (Blue full) | <!-- BEGIN weight:wt-loadedtx-total -->5,049<!-- END weight:wt-loadedtx-total --> | <!-- BEGIN weight:wt-loadedtx-x -->3,636<!-- END weight:wt-loadedtx-x --> | <!-- BEGIN weight:wt-loadedtx-yd -->1,189<!-- END weight:wt-loadedtx-yd --> | <!-- BEGIN weight:wt-loadedtx-z -->1,342<!-- END weight:wt-loadedtx-z --> | <!-- BEGIN weight:wt-loadedtx-fr -->34.8<!-- END weight:wt-loadedtx-fr -->/<!-- BEGIN weight:wt-loadedtx-rr -->65.2<!-- END weight:wt-loadedtx-rr -->% | <!-- BEGIN weight:wt-loadedtx-nr -->49.0<!-- END weight:wt-loadedtx-nr -->/<!-- BEGIN weight:wt-loadedtx-fa -->51.0<!-- END weight:wt-loadedtx-fa -->% |
| Camera Ready (Deployed) | <!-- BEGIN weight:wt-ready-total -->5,049<!-- END weight:wt-ready-total --> | <!-- BEGIN weight:wt-ready-x -->3,633<!-- END weight:wt-ready-x --> | <!-- BEGIN weight:wt-ready-yd -->1,173<!-- END weight:wt-ready-yd --> | <!-- BEGIN weight:wt-ready-z -->1,341<!-- END weight:wt-ready-z --> | <!-- BEGIN weight:wt-ready-fr -->34.8<!-- END weight:wt-ready-fr -->/<!-- BEGIN weight:wt-ready-rr -->65.2<!-- END weight:wt-ready-rr -->% | <!-- BEGIN weight:wt-ready-nr -->50.3<!-- END weight:wt-ready-nr -->/<!-- BEGIN weight:wt-ready-fa -->49.7<!-- END weight:wt-ready-fa -->% |
| Materials Exhausted (Transport) | <!-- BEGIN weight:wt-exhausted-total -->4,509<!-- END weight:wt-exhausted-total --> | <!-- BEGIN weight:wt-exhausted-x -->3,439<!-- END weight:wt-exhausted-x --> | <!-- BEGIN weight:wt-exhausted-yd -->1,190<!-- END weight:wt-exhausted-yd --> | <!-- BEGIN weight:wt-exhausted-z -->925<!-- END weight:wt-exhausted-z --> | <!-- BEGIN weight:wt-exhausted-fr -->38.9<!-- END weight:wt-exhausted-fr -->/<!-- BEGIN weight:wt-exhausted-rr -->61.1<!-- END weight:wt-exhausted-rr -->% | <!-- BEGIN weight:wt-exhausted-nr -->48.9<!-- END weight:wt-exhausted-nr -->/<!-- BEGIN weight:wt-exhausted-fa -->51.1<!-- END weight:wt-exhausted-fa -->% |

**Loaded Transport** is the camera-ready water load (full top-tier Blue IBCs,
1,800 kg) carried in the *transport* configuration — panel swung in, cargo doors
closed. The water sits in the **top** tier, so its vertical CG is **Z=<!-- BEGIN weight:wt-loadedtx-z -->1,342<!-- END weight:wt-loadedtx-z -->mm —
<!-- BEGIN weight:wt-mig-dz -->417<!-- END weight:wt-mig-dz -->mm higher** than the exhausted state (<!-- BEGIN weight:wt-exhausted-z -->925<!-- END weight:wt-exhausted-z -->mm), making it the **highest-CG
transport case** that governs road-transport stability (tie-down and cornering).
The exhausted (return) state is both lighter — **<!-- BEGIN weight:wt-total-exhausted -->4,509<!-- END weight:wt-total-exhausted --> kg**, since ~<!-- BEGIN fact:lost_l -->434<!-- END fact:lost_l --> kg of the
processed water is lost to the open process rather than recovered — and lower-CG,
so it is never the governing case. Even at the loaded worst case the static sideways
tip threshold is **~41°** (½-width 1,181mm ÷ Z_cg <!-- BEGIN weight:wt-loadedtx-z -->1,342<!-- END weight:wt-loadedtx-z -->mm), so the deliberate
Blue-on-top layout stays comfortably stable.

### 4.4 Optional Max-Blue-Fill Transport Case

The standard load fills each Blue tote to 900L (1,800L). The totes are 1,000L vessels, so the
[equipment-layout report §8](equipment-layout-report.md) notes they can be topped further — to
**~1,900L** (~950L per tote) — for one more print (~15). Re-running the weight model confirms even
that heavier load stays well within transport limits:

| Loaded Transport | Gross mass | Z_cg | Static tip threshold |
|------------------|-----------:|-----:|---------------------:|
| Standard Blue fill (1,800L) | 5,044 kg | 1,345mm | 41.3° |
| **Max Blue fill (1,900L)** | **5,144 kg** | **1,362mm** | **40.9°** |

The extra ~100 kg sits in the top tier, raising the worst-case vertical CG only 17mm and lowering
the static sideways tip threshold ~0.4° (to 40.9° — still far above any rollover concern). Gross
weight stays at ~22% of the [ISO 668](https://www.iso.org/standard/76912.html) 24,000 kg limit. The
optional max-Blue-fill top-up is therefore transport-validated.

---

## 5. Weight Distribution Diagrams

### 1 — Summary Comparison

Three-state side-by-side comparison with CG positions and summary table.
The dry state is nearly balanced; the camera-ready/loaded states shift the CG rearward by ~<!-- BEGIN weight:wt-cg-shift -->910<!-- END weight:wt-cg-shift -->mm (the lighter exhausted return state by ~<!-- BEGIN weight:wt-cg-shift-ex -->715<!-- END weight:wt-cg-shift-ex -->mm).

![TBS-001 — Weight Analysis: Summary Comparison](assets/weight-analysis-sheet1.png)

### 2 — Dry Weight (Configured for Transport)

All dry components shown at actual footprint positions, color-coded by
category. The hinged panel is swung ~56° about the pivot (transport position),
shifting its mass toward the far/pivot side. The right end zone (IBC stack area)
is the densest zone.

![TBS-001 — Weight Analysis: Dry — Transport](assets/weight-analysis-sheet2.png)

### 3 — Camera Ready (Panel Deployed)

Weight distribution with full Blue IBCs (top tier) and hinged panel
deployed to its operational position at the cargo door end (X=0–80).
CG marker shows the loaded center of gravity at X=<!-- BEGIN weight:wt-ready-x -->3,633<!-- END weight:wt-ready-x -->, Yd=<!-- BEGIN weight:wt-ready-yd -->1,173<!-- END weight:wt-ready-yd -->.
Quadrant weights show the rear-heavy bias from the IBC stack.

![TBS-001 — Weight Analysis: Camera Ready](assets/weight-analysis-sheet3.png)

### 4 — Materials Exhausted (Configured for Transport)

Water has migrated from top-tier Blue IBCs to bottom-tier Brown/Waste IBCs, and ~<!-- BEGIN fact:lost_l -->434<!-- END fact:lost_l --> kg of it has
been lost to the open process (evaporation, wet-print carryout, unrecovered residual — see
[water-system report §4](water-system-report.md)), so only ~<!-- BEGIN fact:recovered_l -->1,260<!-- END fact:recovered_l --> kg is recovered. The hinged panel
is swung ~56° about the pivot to its transport position. Total mass therefore drops to **<!-- BEGIN weight:wt-total-exhausted -->4,509<!-- END weight:wt-total-exhausted --> kg**
(~<!-- BEGIN weight:wt-mass-drop -->540<!-- END weight:wt-mass-drop --> kg below the loaded state), and the vertical CG drops by <!-- BEGIN weight:wt-mig-dz -->417<!-- END weight:wt-mig-dz -->mm (Z: <!-- BEGIN weight:wt-loadedtx-z -->1,342<!-- END weight:wt-loadedtx-z --> → <!-- BEGIN weight:wt-exhausted-z -->925<!-- END weight:wt-exhausted-z -->mm) as the
remaining water settles in the bottom tier. This is the lightest, lowest-CG transport state — never
the governing case.

![TBS-001 — Weight Analysis: Materials Exhausted](assets/weight-analysis-sheet4.png)

### 5 — Loaded Transport (Full Blue IBCs)

The camera-ready water load (1,800 kg in the top-tier Blue IBCs) carried in
transport configuration — panel swung in, cargo doors closed. The water is in
the **top** tier, raising the vertical CG to **Z=<!-- BEGIN weight:wt-loadedtx-z -->1,342<!-- END weight:wt-loadedtx-z -->mm** (+<!-- BEGIN weight:wt-mig-dz -->417<!-- END weight:wt-mig-dz -->mm vs the lighter
exhausted state at <!-- BEGIN weight:wt-exhausted-z -->925<!-- END weight:wt-exhausted-z -->mm). This is the worst-case transport vertical CG.

![TBS-001 — Weight Analysis: Loaded Transport](assets/weight-analysis-sheet5.png)

---

## 6. Analysis and Findings

### 6.1 ISO Gross Weight Compliance

All four states are well within the ISO 24,000 kg maximum gross weight:

| State | Total (kg) | Margin (kg) | Utilization |
|-------|-----------|------------|-------------|
| Dry | <!-- BEGIN weight:wt-dry-total -->3,249<!-- END weight:wt-dry-total --> | <!-- BEGIN weight:wt-iso-dry-margin -->20,751<!-- END weight:wt-iso-dry-margin --> | <!-- BEGIN weight:wt-iso-dry-util -->13.5<!-- END weight:wt-iso-dry-util -->% |
| Camera Ready | <!-- BEGIN weight:wt-ready-total -->5,049<!-- END weight:wt-ready-total --> | <!-- BEGIN weight:wt-iso-ready-margin -->18,951<!-- END weight:wt-iso-ready-margin --> | <!-- BEGIN weight:wt-iso-ready-util -->21.0<!-- END weight:wt-iso-ready-util -->% |
| Materials Exhausted | <!-- BEGIN weight:wt-exhausted-total -->4,509<!-- END weight:wt-exhausted-total --> | <!-- BEGIN weight:wt-iso-exhausted-margin -->19,491<!-- END weight:wt-iso-exhausted-margin --> | <!-- BEGIN weight:wt-iso-exhausted-util -->18.8<!-- END weight:wt-iso-exhausted-util -->% |
| Loaded Transport | <!-- BEGIN weight:wt-loadedtx-total -->5,049<!-- END weight:wt-loadedtx-total --> | <!-- BEGIN weight:wt-iso-loadedtx-margin -->18,951<!-- END weight:wt-iso-loadedtx-margin --> | <!-- BEGIN weight:wt-iso-loadedtx-util -->21.0<!-- END weight:wt-iso-loadedtx-util -->% |

The container operates at about 19–21% of its rated capacity in all states.
There is no structural concern from a gross weight perspective.

### 6.2 Left-Right Balance (Near/Far)

The near/far split stays close to balanced in all states (<!-- BEGIN weight:wt-near-lo -->48.5<!-- END weight:wt-near-lo -->–<!-- BEGIN weight:wt-near-hi -->50.3<!-- END weight:wt-near-hi -->% near). The
transport states lean slightly far (up to ~<!-- BEGIN weight:wt-far-hi -->51.5<!-- END weight:wt-far-hi -->% far) because the swung panel + drum carry
their mass toward the far/pivot side. This is by
design: equipment on the pinhole wall (near side) is lightweight (electrical
panel, battery, and solar controller totaling ~<!-- BEGIN weight:wt-near-elec -->30<!-- END weight:wt-near-elec --> kg), the pump manifold is on the Corridor Plumbing Panel
centered in the IBC corridor (Yd=1,046), and the IBC stack is centered
across the container width. The film plane carriage contributes ~<!-- BEGIN weight:wt-comp-film -->32<!-- END weight:wt-comp-film --> kg to
the far side but is offset by the tilt-swing board on the near side.

### 6.3 Front-Rear Balance

The dry/transport state has a front-biased split (<!-- BEGIN weight:wt-dry-fr -->54.0<!-- END weight:wt-dry-fr -->/<!-- BEGIN weight:wt-dry-rr -->46.0<!-- END weight:wt-dry-rr -->%), with CG at
X=<!-- BEGIN weight:wt-dry-x -->2,724<!-- END weight:wt-dry-x -->mm. This front bias comes from the cargo doors (<!-- BEGIN weight:wt-doors-total -->280<!-- END weight:wt-doors-total --> kg total) being
in their closed position at X≈−70mm, pulling the CG toward the cargo door
end. The hinged panel is also swung ~56° about the pivot, keeping its mass
in the front (door-end) half.

When liquids are added and the panel and doors are deployed (camera ready),
the CG shifts rearward to X=<!-- BEGIN weight:wt-ready-x -->3,633<!-- END weight:wt-ready-x -->mm (~<!-- BEGIN weight:wt-cg-shift -->910<!-- END weight:wt-cg-shift -->mm past the dry CG). The doors
swing open flat against the side walls (X=0–1,221mm), redistributing
<!-- BEGIN weight:wt-doors-total -->280<!-- END weight:wt-doors-total --> kg from X≈−70 to X≈610, while 1,800 kg of water loads in the IBC stack
zone (X=4,674–5,893mm). This creates a <!-- BEGIN weight:wt-ready-fr -->34.8<!-- END weight:wt-ready-fr -->/<!-- BEGIN weight:wt-ready-rr -->65.2<!-- END weight:wt-ready-rr -->% front/rear split — the heavy
1,000L totes sit at the sealed end.

**Transport implication:** When loaded for transport (materials exhausted,
doors closed), the container's CG is at <!-- BEGIN weight:wt-cg-lengthpct -->58.4<!-- END weight:wt-cg-lengthpct -->% of the length from the cargo
door end. For trailer placement, the container
should be positioned so the rear (sealed) end sits over or near the trailer
axle(s) to balance the load.

### 6.4 Vertical CG and Self-Stabilizing Design

The most significant finding is the **vertical CG migration** between states:

- **Loaded (top-tier water):** Z_cg = <!-- BEGIN weight:wt-loadedtx-z -->1,342<!-- END weight:wt-loadedtx-z -->mm (1,800 kg of water in top-tier IBCs)
- **Materials Exhausted:** Z_cg = <!-- BEGIN weight:wt-exhausted-z -->925<!-- END weight:wt-exhausted-z -->mm (<!-- BEGIN fact:recovered_l -->1,260<!-- END fact:recovered_l --> kg of recovered water in bottom-tier IBCs)
- **ΔZ = −<!-- BEGIN weight:wt-mig-dz -->417<!-- END weight:wt-mig-dz -->mm** (CG drops ~<!-- BEGIN weight:wt-mig-dz -->417<!-- END weight:wt-mig-dz -->mm during a session)

This is an inherent self-stabilizing feature of the 2×2 IBC stack design.
1,800 kg of clean water is loaded into the top-tier Blue IBCs and processed during a
session; ~<!-- BEGIN fact:recovered_l -->1,260<!-- END fact:recovered_l --> kg is recovered into the bottom-tier Brown/Waste IBCs and ~<!-- BEGIN fact:lost_l -->434<!-- END fact:lost_l --> kg is
lost to the open process, so total mass drops from <!-- BEGIN weight:wt-total-loaded -->5,049<!-- END weight:wt-total-loaded --> to **<!-- BEGIN weight:wt-total-exhausted -->4,509<!-- END weight:wt-total-exhausted --> kg**. The water that
remains migrates from the top tier to the bottom tier, dropping the center of gravity by
<!-- BEGIN weight:wt-mig-dz -->417<!-- END weight:wt-mig-dz -->mm and improving stability through the session.

### 6.5 Walkway Weight Sensitivity

The walkway system contributes <!-- BEGIN weight:wt-walkway-total -->150<!-- END weight:wt-walkway-total --> kg (<!-- BEGIN weight:wt-walkway-pct -->4.6<!-- END weight:wt-walkway-pct -->% of dry weight), making it the
second-largest structural subsystem after the hinged panel. The deck grating —
15mm molded GRP (fiberglass) at ≈11 kg/m² — is the largest single line in the
walkway; GRP is specified for corrosion immunity in the wet photo-chemistry
environment. The GRP is vinyl-ester resin with a grit
top for slip resistance; the 15mm grate depth keeps the lowered deck height
unchanged (the spray-bar carriage clearance beneath it is set by the Ø32-wheel /
40×25-SS-beam shrink — see the [Processing Tray & Spray Bar](processing-tray-and-spray-bar.md) report).

---

## 7. Source References

1. [ISO 668:2020](https://www.iso.org/standard/76912.html) — Series 1 freight containers: Classification, dimensions and ratings
2. [Hapag-Lloyd Container Specification](https://www.hapag-lloyd.com/en/products/fleet/container/20-foot-standard.html) — 20ft Standard Dry Container
3. [McNICHOLS — Fiberglass Grating](https://www.mcnichols.com/fiberglass-grating) / [Grating Pacific — Molded FRP](https://gratingpacific.com/product/molded-fiberglass-grating/) — Molded GRP (fiberglass) grating, vinyl-ester, weight tables
4. [Schütz Ecobulk MX 1000L](https://www.schuetz-packaging.net/schuetz-usa/en/ibcs/ecobulk/ecobulk-mx/) — 1,000L caged composite IBC tote specifications (~65 kg tare; all four positions standardize on this size — a 600L caged tote does not exist)
5. [Water System Report](water-system-report.md) — Processing tray weight (§4), IBC layout (§5)
6. [Light Trap Selection](light-trap-selection.md) — Panel + drum weight (§7)
