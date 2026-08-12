<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Component Dimension Audit — Purchased Parts vs. As-Drawn

**Purpose.** After the IBC tote sizing error (assumed "600 L" small totes; the real
food-grade caged product is **1,000 L / 1219×1016×1,168 mm**, which forced the entire
`ibc-reconfig-v2` rework), this audit reconciles **every major purchased-as-is
component** against the size used in the 3D models / 2D diagrams (`tbs_constants.py`).
The goal: no other component is modeled at an assumed size that the real product
doesn't match.

**Scope.** Purchased components with a fixed catalog size — fans, pumps, accumulator,
filters, IBC totes, batteries, solar, evap cooler, bearings, linear guides, leadscrews,
nozzles. **Excluded:** fasteners and standard small fittings (nuts/bolts/valves/elbows/
camlocks/unions), and **fabricated-to-spec** items (RHS steel, ACM panels, the Ø900 drum,
the Ø89 pivot post, plywood) — those are cut to the drawing, so there is no
"product ≠ drawing" risk.

**Method.** Real dimensions are from the manufacturer/retailer datasheet (linked).
Modeled dimensions are the `tbs_constants.py` value(s) the generators draw. mm.

---

## 1. Findings summary

<!-- BEGIN parts:dimension-audit -->
| # | Component | Real product (datasheet) | Modeled | Verdict |
|---|-----------|--------------------------|---------|---------|
| 1 | IBC tote (1,000 L caged) | 1219×1016×1168 | `IBC_W/IBC_D/IBC_H_1000` | ✅ FIXED (v2) |
| 2 | LiFePO4 battery, 100Ah 12V (Renogy Core Series) | 260×169×211 — Renogy 12V 100Ah Core Series | `BA_W/BA_D/BA_H` | ✅ FIXED |
| 3 | Shurflo 2088-554-144 pump (×5 — P-01 Blue supply / P-02 Brown recycle-spray / P-03 waste evac / P-04 tray drain / P-05 Brown drain) | 216×127×114 — Shurflo 2088-554-144 | `PUMP_D×PUMP_YD_SPAN×Z` | ✅ FIXED (minor) — protrusion PUMP_D 100→114 |
| 4 | Big Blue filter housing 4.5"×20" (separate) | Ø184×594 — Pentek 4.5×20 BB | `BB_OD/BB_H` | 3-separate design of record (2026-07): combo → 3 separate housings + frame per plumbing-report §3.1/§7.2. Prices indicative — firm at the Aug-2026 re-price. |
| 5 | 150×150×50mm axial fans (12V DC) | 150×150×50 | `FAN_DIAM/FAN_BODY_D` | ✅ FIXED |
| 6 | Evaporative cooler | 508×254×711 — Hessaire MC18M | `EVAP_W/EVAP_D/EVAP_H` | ✅ RESOLVED |
| 7 | SeaFlo accumulator (0.75 L) | 200×127×125 — SeaFlo SFAT-075-125-01 | `Ø127×200 cyl` | ✅ FIXED — cylinder 150→200 |
| 8 | 304 SS square tube 1½×1½×0.062in, single 17ft4in * | 38×38×1.6 | `SPRAY_BAR_BEAM_W/SPRAY_BAR_BEAM_H` |  |
<!-- END parts:dimension-audit -->

**Excluded from the model but listed for BoM completeness:** Solar panel (Renogy 200 W
rigid ≈ 1491×699×35, varies by model — mounted externally, no container clash).

---

## 2. Detail + sources

*All items below are now resolved (see the §1 summary and §4 remediation); each entry
is retained as the **as-found** audit record — the Problem/Action text describes the
discrepancy and the fix that was applied.*

### 2. Battery — Renogy 12 V 100 Ah LiFePO4 ✅ RESOLVED (§4)
- **Real:** 260 × 169 × 211 mm (L×W×H), 10.5 kg, side busbar terminals. [Renogy Core Series (Off Grid Stores)](https://offgridstores.com/products/renogy-12v-100ah-core-series-deep-cycle-lithium-iron-phosphate-battery) (RBT12100LFP-US; switched from the Smart Lithium 330×172×214 for the side busbar → simpler vertical stacking)
- **Modeled:** `BA_X`=1810, `BA_W`=500, `BA_D`=120, `BA_H_LO`=150, `BA_H_HI`=650 → bank 500(X)×120(Yd)×500(Z); each of 2 packs ~240×120×500.
- **Problem:** the modeled pack is **500 mm tall and only 120 mm deep**; the real pack is **214 mm tall and 172 mm deep**. Two packs side-by-side along X are 2×330 = **660 mm** (vs modeled 500), or stacked are 428 mm tall (vs 500). The battery-bank footprint on the pinhole wall and its clearances (electrical panel above, cable runs) are all drawn against the wrong box.
- **Action:** set `BA_*` to two real 260×169×211 packs (decide side-by-side vs stacked), re-render electrical/floorplan/assembly + the film-plane near-wall ghost, re-check EP-above-battery clearance.

### 3. Pump — Shurflo 2088-554-144 ✅ RESOLVED (§4)
- **Real:** 8.5"L × 5"W × 4.5"H = **216 × 127 × 114 mm**. [Fresh Water Systems](https://www.freshwatersystems.com/products/shurflo-2088-554-144-delivery-pump-3-5-gpm-45-psi-12vdc-no-cord) · [datasheet PDF](https://www.pumpagents.com/pdf/ShurfloPumps/2088-554-144.pdf)
- **Modeled:** `PUMP_D`=100 (pump zone width). 4–5 pumps tile the Corridor Plumbing Panel.
- **Problem:** a real 2088 is **216 mm long × 127 mm wide** — the panel pump columns are drawn ~half-size. With 5 of them plus the accumulator + 3× 594 mm filters, the **panel layout must be re-checked for fit** (panel face is <!-- BEGIN fact:corridor_width_mm -->270<!-- END fact:corridor_width_mm --> mm corridor × 2,060 mm tall).
- **Action:** set the modeled pump footprint to ~216×127×114, re-lay-out the panel (`generate_panel_layout.py` + 3D `equipment_panel()`), re-check corridor depth.

### 4. Filter housing — Big Blue 4.5" × 20" ✅ RESOLVED (§4)
- **Real:** Pentek 20×4.5 BB = 23⅜" × 7¼" = **594 mm tall × Ø184 mm**. [Pentek 20" BB](https://www.filterwater.com/p-541-pentek-20-big-blue-water-filter-housing-15-inch.aspx) · [allfilters 20×4.5](https://www.allfilters.com/filterhousings/20x4.5/20-bb-housing)
- **Modeled:** `BB_OD`=184, `BB_H`=594 (a 4.5×20 housing — matches the real dimension above).
- **As found:** `BB_OD`=130, `BB_H`=340 drew a **10"** housing while the BoM specified **4.5"×20"** cartridges.
- **Resolution:** kept **4.5"×20"** for the media life (~2× the interval between changes). The model was set to `BB_OD`=184 / `BB_H`=594; the housings hang as a **horizontal bank high on the pinhole wall** (heads pinned near the ceiling, sumps to ~Z1746), not a vertical stack, so the extra length costs walkway head clearance (shoulder height) rather than a tall panel run. Panel re-rendered, filter cost re-summed. Reversible to 4.5"×10" (same heads/ports) if the clearance becomes an operational issue.

### 5. Fan — AC Infinity Cloudline S6 ✅ RESOLVED (§4)
- **Real:** 6" (152 mm) duct; unit 7.9×12.6×8.4" = **200 × 320 × 213 mm**, an **inline duct fan**. [AC Infinity S6](https://acinfinity.com/cloudline-s6-quiet-inline-fan-6-with-speed-controller/)
- **Modeled:** `FAN_DIAM`=150 (≈ the 152 duct ✓) but `FAN_BODY_D`=50 — drawn as a **thin axial panel fan** in a 300 mm baffle duct (`DUCT_DEPTH`=300).
- **Problem:** the S6 is **320 mm long** — it won't sit flush ("fan bodies do not protrude beyond the panel face" is false for an S6) and it **exceeds the 300 mm baffle-duct depth**. The design intends a compact 150 mm axial **panel** fan; the S6 is a different form factor.
- **Action (decision needed):** either (a) spec a thin 150 mm 12 V **axial panel fan** (matches the drawing) and drop "AC Infinity S6", or (b) keep an inline fan and redesign the baffle-duct housing to accept a ~320 mm inline body.

### 6. Evaporative cooler — assumed a nonexistent 12 V DC unit ✅ RESOLVED
- **Was:** the model assumed a **12 V DC "Jetstream 110"** ground cooler that **does not exist** — [Portacool](https://www.portacool.com/legacy-evaporative-coolers/jetstream-series/)'s real Jetstream line (models 220–270) runs on **120 V AC**, not 12 V DC.
- **Market reality (researched):** there is **no good native-12 V DC ground-placed** evap cooler. The only 12 V options are RV-**roof** units (TurboKool 2B-0001, ~$300 — rejected: roof penetration, roof-coupled vibration, transport conflict), a too-weak personal spot cooler (Transcool E3), or the premium [Solar Chill](https://www.southwest-solar.com/stainless-steel-solar-chill-coolers) line (native 12 V, ground, but $1,100+ and sole-source).
- **Decision:** a **commodity 120 V AC swamp cooler (Hessaire MC18M, ~$130)** on a **dedicated 12V→120V pure-sine inverter (Victron Phoenix 12/375 GFCI, ~$210)**. Keeps the cooler a swappable multi-vendor part; the inverter is general-purpose. Trade-off accepted: +inverter complexity and a 4-print day now needs solar (already within the published envelope).
- **Done:** `EVAP_*` → 508×254×711 (real Hessaire MC18M, official 20×10×28 in); `INVERTER_*` constants added; Circuit E re-based **80 W → <!-- BEGIN fact:evap_cooler_w_bus -->97<!-- END fact:evap_cooler_w_bus --> W on the 12 V bus** (<!-- BEGIN fact:evap_cooler_w_ac -->85<!-- END fact:evap_cooler_w_ac --> W AC ÷ 0.88) in `calculate_energy_budget.py`; energy/cost/shopping/ventilation/electrical reports re-summed; stow zone re-checked (cooler X1450–1958, clear — 51mm roomier after the datasheet correction); AC **isolation/GFCI/equipotential-bonding** design added in [Electrical §7.6](electrical-report.md#ac-safety).

### 7. Accumulator — SeaFlo 0.75 L (SFAT-075-125-01) ✅ RESOLVED (§4)
- **Real:** ~200 × 127 × 125 mm. [Amazon B01MUYL8F8](https://www.amazon.com/Seaflo-Accumulator-Control-Internal-Bladder/dp/B01MUYL8F8) · [environmentalmarine SFAT-075](https://environmentalmarine.com/seaflo/fresh-water-pumps-accumulators/seaflo-1-gallon-accumulator-tank-sfat-075-125-01/)
- **Modeled:** Ø127 × 150 cylinder. Ø matches; tweak length to ~200 when the panel is re-laid-out.

### 8. Spray-bar beam ✅ RESOLVED (§4 — naming)
- BoM line says **1½"×1½"×⅛"** (= 38.1×38.1×3.2 mm); the spec/model use **40×40×3 mm**. Pick one — they differ by ~2 mm and the carriage saddle clamps are cut to the chosen section.

---

## 3. Catalog parts — spec'd by part number (confirm dims match the catalog)

These are ordered by an exact catalog number, so the model **should** already match —
listed for completeness; confirm the drawn size equals the catalog dimension:

| Component | Catalog | Expected dim | Status |
|-----------|---------|--------------|--------|
| ~~Linear rail HGR20~~ (retired → 304 U-channel 1262T21) | — | — | RETIRED — Option-A leadscrew drive superseded by the U-channel/skate/U-joint mechanism |
| Carriage HGH20CA | HGH20CA flanged | standard HGH20CA block | confirm |
| ~~Acme leadscrew ¾"-6~~ (retired) | — | — | RETIRED — no leadscrews in the current design |
| Rod-end bearing | GIR25-DO / McMaster 60645K73 | 25 mm bore | confirm |
| Drum bearing | SKF 6215-2RS1 | 75×130×25 | confirm |
| Tilt-swing bearing | GE50-DO-2RS | Ø50 bore | confirm |
| Solar panel | Renogy 200 W | ~1491×699×35 (external) | no clash |
| MPPT | Victron 100/50 | ~100×113×40 (in enclosure) | no clash |

---

## 4. Resolved decisions (2026-06-15) + remediation

| Component | Decision | Real dim used | Model change | BoM change | Status |
|-----------|----------|---------------|--------------|------------|--------|
| **Fan** | keep the drawn 150 mm axial **panel** fan; swap the product | 150×150×50 | none (model already 150×50) | "AC Infinity S6" → 150×150×50 mm 12 V DC axial fan ([15050-12V](https://www.coolingfanfactory.com/product/DC-Fan-15050-12V-24V-48V-150mm.html)) | ✅ done |
| **Filter** | keep **4.5"×20"** (media life) | 594 × Ø184 | `BB_OD` 130 → 184, `BB_H` 340 → 594 | spec/model = 4.5×20; cost ~$336–550; cartridge intervals ~2× | ✅ done |
| **Battery** | Core pack, **stacked** | 1× 260×169×211 (+ opt. 2nd stacked) | `BA_D`169/`BA_H_HI`371/`BA_W`260/`BA_X`1829 | dims updated | ✅ done (line-of-sight passes) |
| **Pump** | resize | 216×127×114 | `PUMP_D` 100→114 (W/L already matched) | dims added | ✅ done |
| **Accumulator** | minor | 200×127×125 | cyl 150→200 | dims added | ✅ done |
| **Spray beam** | resize to a sourceable imperial square (metric 40×25 not stock) | 38.1×38.1 (1½×1½×0.062in) | `SPRAY_BAR_BEAM_W/H` 40/25→38.1; span→4,399 (full width) | Metals Depot 17ft4in $183 (was 40×25 $153.80); nozzles 4→5×10-pk (44) | ✅ done |
| **Evap cooler** | 120 V AC cooler + 12V→120V inverter (no good 12 V DC ground unit exists) | 508×254×711 (Hessaire MC18M) | `EVAP_*` 600×350×800→508×254×711; `INVERTER_*` added | Circuit E re-based 80→<!-- BEGIN fact:evap_cooler_w_bus -->97<!-- END fact:evap_cooler_w_bus --> W; AC isolation/GFCI/bonding [Electrical §7.6](electrical-report.md#ac-safety) | ✅ done |

**3D re-sends — done.** The earlier audit batch (filter Ø + ACC + battery) was sent and
`overview.skp` re-saved 2026-06-15; the evap-box re-dimension (Hessaire MC18M) + Circuit-E
inverter box followed (overview re-saved in `1872583b`, inverter leader label in `99ec629c`).
`generate_sketchup_model.py` builds the evap at `EVAP_W×EVAP_D×EVAP_H` + the inverter. Only the
manual Sketchfab re-uploads (Alvin's step, same model IDs) may remain.

**Cost re-sum CLOSED (2026-06-15):** the held bundle (fan −~$70, filter, evap cooler + inverter)
is now re-summed. Cooler subsystem (cooler $130 + inverter $210 + DC protection $40 + AC outlet $25)
lands in cost-breakdown **5b** ($769→$830 mid); the new fan ($50) is folded in; grand total
$25,399→**$25,460** mid; Scenario A $19,882→**$19,952**, Scenario B $25,322→**$25,383**. (The
cost-breakdown's water-system filter estimate already reflected a 10″-class figure, so no separate
cat-5 filter adjustment was needed; the master-shopping-list BOM filter $282–445 is authoritative.)
*(These totals are the 2026-06-15 remediation deltas — a dated snapshot; the current build total is generated in the [Cost Breakdown](project-cost-breakdown.md).)*

*This document is the source of truth for the purchased-part dimensional reconciliation; update it as each component is resolved.*
