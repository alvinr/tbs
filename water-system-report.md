<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Water Processing Report


## 1. Purpose

The camera operates in remote locations with no municipal water or drainage. This document specifies a self-contained three-circuit water system that:

- Stores sufficient clean water for 9–14 full-size prints between resupply runs on fresh Blue alone (**~<!-- BEGIN fact:prints_per_resupply -->14<!-- END fact:prints_per_resupply --> prints** once Brown wash-2 recycling is counted — see §below)
- Recycles used wash water through a three-stage filter train, extending usable supply by approximately 40%
- Contains all waste water in a closed, transportable IBC for proper off-site disposal
- Runs entirely on 12V DC, compatible with a solar/battery off-grid power system

![Water System — Sheet 2: Overview](assets/water-system-sheet2.png)


**Three circuits:**

| Circuit | Color code | Purpose | Storage |
|---------|-------------|---------|---------|
| **Blue** | Blue — clean | Fresh water supply for processing | 2× 1,000L IBC totes (1,800L working fill total — 900L each), stacked side-by-side |
| **Brown** | Brown — used | Collected wash water; filtered and recycled back to Blue | 1× 1,000L IBC tote, stacked below Blue IBCs |
| **Black** | Black — waste | Heavily contaminated water; sealed IBC for off-site disposal | 1× 1,000L IBC tote, stacked below Blue IBCs |

![Water System — Sheet 1: System Schematic](assets/water-system-sheet1.png)

---

## 2. Cyanotype Wash Water — Chemistry and Constraints

### What is in the wash water?

When a cyanotype print is washed, the water picks up:

| Compound | Source | Notes |
|----------|--------|-------|
| Ferric ammonium citrate (FAC) | Unexposed sensitizer | Water-soluble, pale yellow; low toxicity |
| Potassium ferricyanide | Sensitizer component | Water-soluble, yellow-orange; low acute toxicity |
| Prussian blue particles | Exposed image pigment wash-off | Fine blue solid particles, ~1–10 micron |
| Iron(III) compounds | Oxidation products | Color the water blue-gray |

**pH:** Wash water starts slightly acidic to neutral (pH 6–7) and may drift alkaline as iron compounds accumulate. Alkaline conditions (pH >8) must be avoided — they accelerate slow breakdown of ferricyanide to ferrocyanide and trace cyanide ions.

**Environmental note:** Cyanotype wash water is low-toxicity and is generally accepted to the municipal sewer in dilute volumes (Photrio forum consensus; corroborated by Safety Data Sheets for FAC and potassium ferricyanide). **However, for remote field use with no sewer access, it must be contained and transported for disposal.** Do not pour on soil or into waterways.

**Source:** [Photrio — Cyanotype wash water composition](https://www.photrio.com/forum/threads/composition-of-cyanotype-wash-water.126234/) · [Ask MetaFilter — Disposing of cyanotyping water](https://ask.metafilter.com/374714/Disposing-of-cyanotyping-water)

### What filtration can and cannot do

A sediment + activated carbon filter train will:
- Remove Prussian blue particle load (sediment stages)
- Reduce some dissolved organics and iron-complex color (carbon stage)
- Restore water to a usable secondary-wash quality after 1–3 passes

It will **not**:
- Completely restore water to fresh-water quality
- Remove dissolved iron salts fully without iron-specific media
- Make the water safe for discharge to ground

**Rule of thumb:** Recycled Brown water may be reused for the **first wash** of each print (roughest wash). The **final wash** must always use Blue (clean) water to avoid re-depositing iron compounds onto the print. After 3 recycle passes, water goes to Black.

---

## 3. Water Volume Calculations

### Per-print water requirement

Processing a ~106 sq ft print in the processing tray (4459 × 2,200mm), flooded to 6mm (¼ inch) depth:

```
Volume per flood = 106 sq ft × (6mm / 304.8) = 106 × 0.0197 ft = 2.09 cu ft
                 = 2.09 × 7.48 = 15.6 gallons ≈ 16 gallons per wash cycle
```

| Wash cycle | Water source | Volume | Drain to |
|-----------|-------------|--------|---------|
| Wash 1 — 5 min | Blue (clean) | 16 gal | Brown tank |
| Wash 2 — 5 min | Brown (recycled) | 16 gal | Brown tank |
| Wash 3 — 5 min | Blue (clean) | 16 gal | Brown tank → Black if >3 recycles |
| **Total per print** | | **~32 gal net Blue consumed** | |

### Storage capacity vs. print count

| Scenario | Blue consumed per print | Prints from <!-- BEGIN fact:blue_supply_gal -->476<!-- END fact:blue_supply_gal --> gal Blue | Brown recycled |
|----------|------------------------|--------------------------|---------------|
| No recycling | 48 gal (3 × 16) | ~10 prints | 0 |
| With recycling (wash 2 from Brown) | 32 gal (2 × 16) | **~<!-- BEGIN fact:prints_per_resupply -->14<!-- END fact:prints_per_resupply --> prints** | ~224 gal reused |
| Brown recycle limit (3 passes) | — | — | 166 gal max before going to Black |

**~<!-- BEGIN fact:prints_per_resupply -->14<!-- END fact:prints_per_resupply --> prints per resupply run** — <!-- BEGIN fact:blue_supply_l -->1,800<!-- END fact:blue_supply_l -->L Blue supply (2× 900L) with Brown recycling for wash 2.

**Water balance — recovered vs. consumed.** Of the <!-- BEGIN fact:blue_supply_l -->1,800<!-- END fact:blue_supply_l -->L Blue supply, a 14-print run processes ~1,690L
(leaving ~110L of dregs, under one print): ~<!-- BEGIN fact:recovered_l -->1,260<!-- END fact:recovered_l -->L is recovered into the collection totes (Brown + Waste,
~<!-- BEGIN fact:collection_fill_l -->630<!-- END fact:collection_fill_l -->L each at their working fill) and ~<!-- BEGIN fact:lost_l -->434<!-- END fact:lost_l -->L (~31L per print, ~17% of the ~182L gross washed per print) is
open-process loss — water **carried out in the wet prints** (each full-plane muslin sheet, ~10.7 m²,
leaves saturated to dry), **evaporation** from the open spray-wash tray, and **unrecovered residual**
(tray-surface film, the sump dead-volume below the P-04 pickup, hose/manifold hold-up). This loss is *why
two <!-- BEGIN fact:collection_fill_l -->630<!-- END fact:collection_fill_l -->L collection totes balance the supply* — they are sized for the recovered fraction, not full
throughput. (The [weight report](weight-distribution-report.md) carries the same ~<!-- BEGIN fact:recovered_l -->1,260<!-- END fact:recovered_l -->L recovered figure
for its exhausted-state transport mass — 4,590 kg, ~540 kg below the loaded state.)

#### Extending capacity beyond 14 prints

**Maximizing the initial load.** The standard 900L-per-tote fill (<!-- BEGIN fact:blue_supply_l -->1,800<!-- END fact:blue_supply_l -->L → <!-- BEGIN fact:prints_per_resupply -->14<!-- END fact:prints_per_resupply --> prints) leaves a little
residue in each 1,000L tote; topping toward the ~950–1,000L tote limit (~1,900–2,000L) buys ~1–2 more prints
(~15–16), transport-validated to a worst-case static tip of 41.0° (see
[weight report §4.4](weight-distribution-report.md)). To actually realize those extra prints the
collection totes must also rise proportionally — they are sized at ~<!-- BEGIN fact:collection_fill_l -->630<!-- END fact:collection_fill_l -->L each for the 14-print recovery —
so the hard ceiling on a single hauled load is the **per-tote 1,000L volume**, capping it at ~16 prints.

**On-site top-up — extended deployment.** A deployment can run past the ~16-print single-load ceiling
using the external end-wall bulkhead ports — *no cargo-door access required*: **resupply Blue** from a
water bowser or tanker through the **X1** gravity-fill inlet (tees to both Blue totes), and **discharge
Brown/Waste** through the **X3 / X4** drain ports to a holding tank or tanker. In this mode the tote
volumes act as **buffers, not hard caps**, and print count is set by water *logistics* (bowser visits,
disposal access) rather than tote volume. This is a distinct operating mode from the hauled single load:
for transport the totes return to their validated fill states (Blue drained, Waste within its
return-haul limit). See the [Operating Manual](operating-manual.md) for the top-up procedure.

**Cooling-water overhead (hot-weather deployments):** the evaporative cooler draws clean water from the *same* Blue circuit (at TAP-01 on the pinhole wall), so it is not free of the processing budget. Its reservoir holds ~4.8 gal (~18 L) and evaporates ~3 L/hour while running ([Ventilation Report §5](ventilation-report.md)), so a deployment consumes roughly **one tankful (~18 L)** — about **15% of one print's net Blue draw**, or **~1% of the full <!-- BEGIN fact:blue_supply_l -->1,800<!-- END fact:blue_supply_l --> L supply**. This is sub-one-print of overhead: it does not move the <!-- BEGIN fact:prints_per_resupply -->14<!-- END fact:prints_per_resupply -->-print count for a 1–2 print outing, but a resupply spent entirely on hot, multi-print sessions should be planned as **~13 effective prints** to leave the cooler its margin. The <!-- BEGIN fact:prints_per_resupply -->14<!-- END fact:prints_per_resupply -->-print figure above counts processing water only.

---

## 4. System Architecture

### 4.1 Blue System — Clean Water Supply

```
IBC-1 (900L) ──┐
                ├──→ Manifold → BV-01 → P-01 → ACC-01 → BV-02 → Distribution
IBC-2 (900L) ──┘                                                      │
                                                                          ↓
                                                              FLOOD/SPRAY BAR
                                                              ↓ (Processing tray)
```

- Two IBC totes plumbed in parallel via 1" HDPE manifold with isolation valves
- The two Blue totes are tied at the base by a **1" equalization cross-tie** (tank body to tank body, low on the totes) so their levels self-balance as P-01 draws and X1 refills
- P-01: Shurflo 2088 12VDC diaphragm pump — 3.5 GPM, 45 PSI, self-priming
- **Check valves:** only **CV-1** is fitted, on the X1 gravity fill — the single flow path with no pump. Every return and drain leg is pump-driven, and the Shurflo 2088 pumps carry an **integral 1-way check valve** ([2088-554-144 datasheet](https://www.pumpagents.com/pdf/ShurfloPumps/2088-554-144.pdf)), so dedicated anti-siphon checks on the IBC-2 return, IBC-3 buffer return and IBC-4 waste legs would be redundant and are not used
- ACC-01: 0.75 L (23.5 oz) pressure accumulator — smooths pump cycling, maintains pressure when pump is off
- Low-level float switch on IBC-2 alerts operator when Blue supply is low
- Spray bar: gantry design — 40×25×3mm 304 SS RHS beam (laid flat, ~15mm pre-camber) spanning the open processing area (3,859mm) between walkway inner edges, with Ø32 wheel carriages rolling on the raised/sloped tray floor beneath walkway grating. A 3/4" LDPE manifold clipped to the beam side feeds 26 side-tapped flat-fan nozzles. See the [Processing Tray & Spray Bar](processing-tray-and-spray-bar.md) report for full mechanical design
- Fill inlet: single external 2" NPT bulkhead fitting (X1) with camlock on the container end wall centerline — gravity feed, no pump required. Inside, an internal tee (near X1) splits to a SIDE entry near the top of BOTH Blue totes (no top-cap access — <!-- BEGIN fact:ibc_ceiling_clearance_mm -->52<!-- END fact:ibc_ceiling_clearance_mm -->mm headroom), filling them in parallel and gravity-linked — one external hose. Remote resupply from water bowser or tanker (no cargo door access required)

### 4.2 Brown System — Used Water Recycling

```
Processing tray sump (P-04 suction pickup)
        │
   P-04 (tray drain transfer pump — suction from sump, lifts ~900mm to IBC-3 side-entry)
        │
     SV-02 SAMPLE TAP (meter incoming used-water pH → set DV-02 routing)
        │
   3W-DV-02 ──────────────────────────────────────────→ (to IBC-4 waste if heavily loaded)
        │
        ↓
   IBC-3 (600L buffer fill, side-entry near top — no top-cap access, 52mm headroom)
        │
       P-02
        │
       F-1 (50-micron sediment)
        │
       F-2 (5-micron sediment)
        │
       F-3 (GAC carbon block)
        │
     SV-01 SAMPLE TAP (draw sample → manual meter check before returning)
        │
   3W-DV-01 ──→ pH 6–7, visually acceptable: RETURN TO IBC-2 (Blue)
        │
        └──→ pH drift / discolored: FORWARD TO IBC-4 (waste)
```

**Filter train sizing:**

The filter train uses a single 3-stage whole-house filter unit (a **4.5"×10"** Big Blue 3-stage; Express Water / Geekpure / iSpring 10") with **Ø184 × 333mm** housings. *(Switched from 4.5"×20" to match the modeled BB_OD=184/BB_H=340 — see [component-dimension-audit.md](component-dimension-audit.md).)*. 1" NPT inlet/outlet; a single 1/2"→1" bushing reducer connects P-02 output to the unit inlet.

| Stage | Cartridge (4.5"×10") | Removes | Replace interval |
|-------|---------------------|---------|-----------------|
| F-1 | MPP 5-micron melt-blown polypropylene sediment | Gross sediment, fiber lint, Prussian blue particles | ~Every 14 prints |
| F-2 | KDF-55 heavy metal removal | Dissolved iron compounds from ferricyanide wash water | ~Every 15 prints |
| F-3 | CTO coconut shell activated carbon block | Residual organics, color | ~Every 10 prints |

The 10" cartridges (~½ the media of a 20") were chosen to match the modeled housing size, so service intervals are correspondingly shorter (~½). The unit includes triple drain valves for flushing individual stages without disassembly. Equivalent 3-stage Big Blue units are available from Express Water, Geekpure, iSpring and others — any unit accepting standard 4.5"×10" cartridges with 1" NPT ports will work.

**pH management:** Two pH sample taps are fitted. **SV-02** (½" valve + spout on the P-04 tray-drain discharge, before 3W-DV-02) lets the operator meter the incoming used water and choose the DV-02 routing — buffer to IBC-3 or divert straight to IBC-4 waste. **SV-01** confirms the cleaned water before it returns: draw the post-filter sample at the **SV-01 sample tap** (½" valve + spout before 3W-DV-01) and meter it. If filtered water reads pH <6, do nothing — slightly acidic is preferred. If pH >7.5, add citric acid solution (10g citric acid in 1 liter water) via the dosing port in the IBC-3 outlet, stir, retest. Do not return water with pH >8 to the Blue system.

### 4.3 Black System — Waste Containment

```
FROM 3W-DV-01 (rejected filter output — pH out of range)
FROM 3W-DV-02 (heavily contaminated drain water — operator judgment)
        │
   IBC-4 (600L waste)
        │
   Sealed, labeled per GHS/OSHA
        │
   TRANSPORT to licensed liquid waste disposal facility
```

- IBC-4 is a 1,000L caged composite tote with DN50 butterfly valve (S60×6 thread); "600 L"/"1,000 L" are fill levels
- IBC-4 sits in the right end zone in a 2x2 stack: bottom-far position
- Cap sealed before transport; label contents, date, location, UN numbers for ferricyanide/iron compounds
- Drained remotely via external 2" NPT bulkhead fitting with camlock on the container end wall centerline — no need to open cargo doors
- **Do not leave IBC valve open** — evaporation and UV exposure can drive ferricyanide chemistry

### 4.4 Processing Tray and Spray Bar

The processing tray and spray bar gantry are fully specified in the [Processing Tray & Spray Bar Report](processing-tray-and-spray-bar.md). Their role in the water system is summarized here.

**Processing tray:** A permanently installed 4459 × 2,200mm stainless steel tray sits on the optical zone floor between the film plane rails. A 1:200 dual-axis slope drains wash water to a pressed sump well on the right side nearest the pinhole wall. P-04 draws from the sump via a suction pickup tube — no penetration of the tray floor or container floor.

**Drain path:** P-04 suction pickup → 1" flexible hose over near rim → P-04 pump on the Corridor Plumbing Panel → 3W-DV-02 diverter → IBC-3 (Brown) or IBC-4 (Waste).

**External drain-out risers:** The Brown (IBC-3) and Waste (IBC-4) totes are pumped out to the sealed end-wall ports — X3 via P-05, X4 via P-03. The two vertical drain risers run down the IBC corridor gap and are clamped at ~400mm centers to an 18mm marine-ply backing spine that tees perpendicular off the Corridor Plumbing Panel. Its top is capped with a horizontal ply shelf that the Blue fill trunk rests on — so both the drain risers and the fill trunk are supported at the T rather than free-hanging.

**Spray bar:** A 3,859mm span 304 SS RHS beam gantry (40×25×3mm, laid flat) rolls on the raised/sloped tray floor beneath the walkway grating. Water from P-01 (Blue supply) reaches the bar via BV-02 → 4m flexible hose → ball-joint manifold → 7 feed tubes into the side LDPE manifold → 26 flat-fan nozzles at 150mm centers, spraying down-and-in.

**Supply path:** P-01 → ACC-01 → rigid 1/2" HDPE pipe along pinhole wall → BV-02 → coiled flexible hose → bulkhead fitting → beam bore → spray holes.

**Containment liner:** A fresh 6-mil black LDPE sheet is laid over the tray surface before each session to prevent direct stainless-to-print contact and simplify cleanup.

For full construction details, structural analysis, parts list, and engineering drawings, see [Processing Tray & Spray Bar](processing-tray-and-spray-bar.md).

---

## 5. Plumbing Specification

### Pipe sizing

All pump-driven internal runs use **1/2" pipe**, matching the Shurflo 2088 pump ports (1/2"-14 male parallel thread). This eliminates trunk-to-manifold reducer fittings entirely. The 3-stage combo filter unit has 1" NPT ports, requiring a single 1/2"→1" bushing reducer at the inlet; the outlet connects directly to DV-01 (1" FNPT). No inter-housing plumbing is needed — all filter-to-filter flow is internal to the combo unit. Larger pipe (1" or 2") is used only for the IBC fill/drain lines at the external bulkhead ports and the short filter outlet to DV-01, where gravity flow requires lower restriction. P-03 is mounted separately in the IBC plumbing corridor on the X4 waste drain run.

**Internal runs (1/2" HDPE Sch 40):**

| Circuit | Pipe | Size | Pressure rating | Material |
|---------|------|------|----------------|---------|
| Blue supply (IBC → BV-01 → P-01) | Sch 40 / SDR-11 | 1/2" nominal (OD 21mm) | 100 PSI min | HDPE |
| Blue discharge (P-01 → ACC-01 → BV-02 → spray bar) | Sch 40 / SDR-11 | 1/2" nominal (OD 21mm) | 100 PSI min | HDPE |
| Brown suction (IBC-3 → P-02) | Sch 40 / SDR-11 | 1/2" nominal (OD 21mm) | 100 PSI min | HDPE |
| Brown riser (P-02 → F1 inlet) | Sch 40 | 1/2" nominal (OD 21mm) | 100 PSI min | HDPE |
| Tray drain suction (sump → P-04) | Reinforced flex hose | 1/2" nominal | pump suction | HDPE/PVC braid |
| DV-02 outputs (→ IBC-3, → IBC-4) | Sch 40 | 1/2" nominal (OD 21mm) | 50 PSI min | HDPE |
| DV-01 outputs (→ Blue IBC-2, → Black IBC-4) | Sch 40 | 1/2" nominal (OD 21mm) | 50 PSI min | HDPE |
| ACC-01 inlet/outlet | Sch 40 | 1/2" nominal (OD 21mm) | 125 PSI min | HDPE |
| Spray bar | SDR-11 | 3/4" nominal | 100 PSI min | HDPE |

**Filter unit outlet (1" HDPE Sch 40):**

| Circuit | Pipe | Size | Pressure rating | Material |
|---------|------|------|----------------|---------|
| Combo filter outlet → SV-01 sample tap → DV-01 | Sch 40 | 1" nominal (OD 33mm) | 100 PSI min | HDPE |

**IBC fill/drain (1" HDPE Sch 40 — gravity flow, not pump-driven):**

| Circuit | Pipe | Size | Pressure rating | Material |
|---------|------|------|----------------|---------|
| External fill line (X1 bulkhead → tee → both Blue totes) | Sch 40 | 1" nominal (OD 33mm) | 50 PSI min | HDPE |
| External drain lines (X3/X4 bulkhead → IBCs) | Sch 40 | 1" nominal (OD 33mm) | 50 PSI min | HDPE |
| X1 fill tee (splits to IBC-1 & IBC-2) | — | 1" HDPE equal tee (Banjo TEE100) | 50 PSI min | HDPE |

At 3.5 GPM, flow velocity in 1/2" pipe (ID ~15.8mm) is approximately 1.1 m/s — well within the recommended 0.5–2.5 m/s range for water systems. The longest internal run (~5.5m from manifold to far-column IBC) contributes less than 0.3 bar friction loss at this velocity.

**Why HDPE, not PVC?** Standard gray PVC is not rated for photographic chemistry contact and can leach plasticizers. HDPE and CPVC are both acceptable. Do not use copper or galvanized fittings — iron compounds in the wash water will react.

### Fittings and connections

| Connection type | Use | Standard |
|----------------|-----|---------|
| 2" camlock (type A+B) | IBC tote inlet/outlet | Aluminum or polypropylene |
| 1" NPT threaded | Combo filter outlet → DV-01, IBC fill/drain lines | HDPE or brass |
| 1/2" NPT threaded | All pump-driven runs, pump ports, manifold connections, ACC-01, ball valves | HDPE or brass |
| 1/2"×1" NPT bushing reducer | P-02 riser to F1 filter inlet (1 required) | Polypropylene or brass |
| 2" NPT bulkhead | External fill/drain port (container wall) | 304 SS |
| Push-fit / compression | Secondary connections | John Guest / Speedfit style |

---

## 6. Electrical — 12V DC Power

| Item | Current draw | Hours/print | Wh/print |
|------|-------------|-------------|---------|
| P-01 Blue pump (Shurflo 2088) | 7.5 A @ 12V | 0.25 hr (15 min run) | 22.5 Wh |
| P-02 Brown pump (Shurflo 2088) | 7.5 A @ 12V | 0.17 hr (10 min run) | 15.2 Wh |
| P-03 Waste pump (Shurflo 2088) — *IBC corridor* | 7.5 A @ 12V | intermittent (waste disposal only) | — |
| P-04 Tray drain transfer pump (Shurflo 2088) | 7.5 A @ 12V | 0.08 hr (5 min run) | 7.5 Wh |
| pH meter | <0.1 A | — | <1 Wh |
| **Total per print** | | | **~46 Wh** |

A 100 Ah 12V lithium battery (1,200 Wh usable) provides **>25 prints** of pump power without recharging. A modest 100W solar panel recharges in ~3–4 hours of sun.

---

## 7. Equipment Layout

See **Sheet 2 — Plan View** (`water-system-sheet2.png`) for the water-system-specific P&ID layout. All four IBCs are in the provably shadow-free **right end zone** (X=4,649–5,893mm), arranged in a 2x2 stack. The optical zone contains only the processing tray and perimeter walkways at floor level.

**Container floor plan — all systems (top-down, 1:75):**
![TBS-001 Container Floor Plan — All Systems](assets/container-floorplan.png)

IBCs are arranged in a **2x2 stack** in the right end zone, right-justified to the far end wall. Near column: IBC-1 Blue (top) + IBC-3 Brown (bottom). Far column: IBC-2 Blue (top) + IBC-4 Waste (bottom). A 270mm plumbing corridor between the two columns carries all internal supply and return lines. Total physical capacity: 4×1,000L = 4,000L (totes are filled to working levels, not full). All IBCs are loaded empty through the cargo doors and filled/drained remotely via 3x external 2" NPT bulkhead fittings (X1/X3/X4) through the container end wall. IBC wall clearance is 30mm (near wall to near column edge).

| Zone | Contents | X (mm) | Yd (mm) | H (mm) |
|------|----------|--------|---------|--------|
| Right end zone | IBC-1 Blue (top, near column) | 4,674–5,893 | 30–1,046 | 1,168–2,336 |
| Right end zone | IBC-3 Brown (bottom, near column) | 4,674–5,893 | 30–1,046 | 0–1,010 |
| Right end zone | Plumbing corridor | 4,674–5,893 | 1,046–1,316 | 0–2,020 |
| Right end zone | IBC-2 Blue (top, far column) | 4,674–5,893 | 1,316–2,332 | 1,168–2,336 |
| Right end zone | IBC-4 Waste (bottom, far column) | 4,674–5,893 | 1,316–2,332 | 0–1,010 |
| Pinhole wall face | Pump manifold (P-01, P-02, P-04) | 2,400–2,700 | Y=0 | 200–600 |
| IBC plumbing corridor | P-03 waste pump (on X4 drain run) | 4,674–5,893 | 1,046–1,316 | ~200 |
| Optical zone floor | Processing tray (2 panels) | 170–4,629 | 60–2,300 | 0–50 |
| Optical zone | No equipment | 150–4,649 | — | — |

All equipment clears the optical cone at every depth — shadow-free proof in [Equipment Layout Report](equipment-layout-report.md).

**Hose routing:** The corridor pumps (P-01, P-04, P-05, P-03) mount on the **Corridor Plumbing Panel** at the front of the IBC stack, reaching into the 270mm plumbing corridor between the two IBC columns — so the pump↔tote suction and return lines are **short**, running entirely within the corridor to the IBCs' corridor-facing DN50 valves. P-02 (Brown filter feed) and the 3-stage filter stack sit on the **Pinhole Wall Plumbing Panel** on the pinhole wall face. The longest run is the **Blue supply to the spray bar**: P-01 → ACC-01 → rigid 1/2" HDPE along the pinhole wall to the tray center → BV-05 → ~4m coiled flexible hose → the rolling beam in the optical zone. The **tray drain** returns the other way — P-04's sump pickup → 1" flexible hose over the near rim → P-04 on the panel → 3W-DV-02 diverter → IBC-3 (Brown) or IBC-4 (Waste). **Waste evacuation** pumps P-05 (X3 / Brown) and P-03 (X4 / Waste) sit directly on the corridor drain risers, minimizing pipe to the external end-wall ports.

**External fill/drain ports:** Three 2" NPT bulkhead fittings with camlock fittings on the exterior are mounted on the container end wall centerline, stacked vertically:

| Port | Function | Connects to |
|------|----------|-------------|
| X1 — Fill Blue | Fresh water supply fill | IBC-1 (top, near column) — gravity feed |
| X3 — Drain Brown | Used water drain | IBC-3 (bottom, near column) |
| X4 — Drain Waste | Waste water drain | IBC-4 (bottom, far column) |

A single external fill port (X1) feeds an internal 1" tee in the corridor, which splits the flow to BOTH Blue IBCs (each branch **side-enters** the tote's corridor face near the top, 150mm + flange — no top-cap access, only <!-- BEGIN fact:ibc_ceiling_clearance_mm -->52<!-- END fact:ibc_ceiling_clearance_mm -->mm headroom). The two top totes fill in parallel, so only one external hose is needed — without a separate cross-connect pipe.

This allows remote filling (from water bowser or tanker) and draining (IBC-3/IBC-4 to disposal tanker) without opening the cargo doors or entering the container. Internal plumbing from each port routes through the 270mm central corridor between the two IBC columns to reach the respective tote. All ports are accessible from the container exterior.

---

## 8. Parts List

<!-- BEGIN parts:water -->
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [IBC tote (1,000 L caged)](https://containerexchanger.com/geo-sale-ads/us-ca/bulk-containers/ibc-totes-for-sale) | Caged composite tote, DN50 butterfly valve (S60×6 thread); side-entry fittings near top | 4 ea | Container Exchanger | $320–$600 |
| [Bulkhead fitting 2" NPT (304 SS)](https://www.mcmaster.com/4464K115) (4464K115) | External fill/drain port, welded through container wall | 3 ea | McMaster-Carr | $75–$120 |
| [Shurflo 2088-554-144 pump (P-01 Blue supply)](https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C) | 12VDC, 3.5 GPM, 45 PSI, 1/2" NPSM ports | 1 ea | Amazon | $55–$70 |
| [Shurflo 2088-554-144 pump (P-02 filter loop)](https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C) | 12VDC, 3.5 GPM, 45 PSI, 1/2" NPSM ports | 1 ea | Amazon | $55–$70 |
| Shurflo 2088-554-144 pump (P-03 waste evacuation) | 12VDC, 3.5 GPM, 45 PSI; empties IBC-4 residual below X4 (~120L) | 1 ea | Amazon | $65 |
| Shurflo 2088-554-144 pump (P-04 tray drain transfer) | 12VDC, 3.5 GPM, 45 PSI; tray drain to IBC-3 (~900mm lift) | 1 ea | Amazon | $65 |
| Shurflo 2088-554-144 pump (P-05 Brown drain) | 12VDC, 3.5 GPM, 45 PSI; evacuates IBC-3 (Brown) residual to the X3 end-wall port | 1 ea | Amazon | $65 |
| [SeaFlo accumulator (0.75 L)](https://www.amazon.com/Seaflo-Accumulator-Control-Internal-Bladder/dp/B01MUYL8F8) (SFAT-075-125-01) | 0.75 L, 125 PSI, 1/2" MNPT | 1 ea | Amazon | $35 |
| Shurflo pump mounting bracket | Stainless, 2088 series — one per pump (P-01..P-05) | 5 ea | Amazon | $50 |
| Corridor plumbing-panel marine ply (18mm) | 4×8 ft 18mm BS 1088 (or equivalent) marine plywood — rear backing board (~170×2196) + drain-riser backing spine (~456×1966) + spacer offcuts; ~1.3 m² used. Price est. | 1 sheet | marine plywood supplier / Home Depot | $120–$200 |
| Pump-mount shirt marine ply (25mm) | 25mm BS 1088 (or equivalent) marine plywood, ~610×1650 cut piece — pump-mount shirt behind P-01..P-05 + 6× shirt-to-panel spacer blocks. Price est. | 1 piece | marine plywood supplier / Home Depot | $70–$130 |
| Corridor panel mount hardware (brackets + fasteners) | 6× steel angle brackets (panel → IBC-frame front-portal uprights), shirt-to-panel screws, lag bolts. Price est. | 1 lot | Home Depot | $25–$50 |
| Big Blue filter housing (4.5"×10") | Ø184×333mm/housing, 1" NPT ports, integrated bracket (Express Water / Geekpure / iSpring) | 1 ea | Amazon | $200–$300 |
| MPP 5-micron sediment cartridge 4.5"×10" | Melt-blown polypropylene depth filter (F-1 stage) | 3 ea | Amazon | $18–$30 |
| KDF-55 heavy-metal cartridge 4.5"×10" | KDF-55 media for dissolved iron/metal removal (F-2 stage) | 2 ea | Amazon | $40–$70 |
| CTO carbon block cartridge 4.5"×10" | Coconut shell activated carbon block (F-3 stage) | 3 ea | Amazon | $24–$45 |
| Banjo V050FP ball valve 1/2" FNPT | PP full-port quarter-turn; pump-suction isolation BV-01 (P-01), BV-02 (P-05), BV-06 (P-03) | 3 ea | Amazon | $18–$30 |
| Banjo V050FP ball valve 1/2" FNPT | PP full-port quarter-turn; pump-suction isolation BV-03 (P-02) | 1 ea | Amazon | $6–$10 |
| Banjo V050FP ball valve 1/2" FNPT | PP full-port; supply isolation BV-04 (TAP-01 chem tap), BV-05 (spray-bar feed) | 2 ea | Amazon | $12–$20 |
| Banjo V100FP ball valve 1" FNPT | PP full-port; V1/V3/V4, VB1–VB3 (IBC fill/drain) | 6 ea | Amazon | $60–$96 |
| 3-way diverter valve 1/2" FNPT | L/T-port HDPE-compatible; 3W-DV-02 (tray drain) | 1 ea | Amazon | $12–$22 |
| 3-way diverter valve 1" FNPT | L/T-port; 3W-DV-01 (filter output) | 1 ea | Amazon | $18–$30 |
| pH sample tap (SV-01) — 1/2" PP ball valve + barb spout + branch tee | Filtered-water sample draw before 3W-DV-01; Banjo V050FP 1/2" PP ball valve + downturned 1/2" hose barb on a 1"×1/2" reducing branch tee, panel face above spill line | 1 ea | Amazon | $10–$18 |
| pH sample tap (SV-02) — 1/2" PP ball valve + barb spout + branch tee | pH sample on the P-04 tray-drain discharge, before 3W-DV-02; same build as SV-01 | 1 ea | Amazon | $10–$18 |
| 2" polypropylene camlock pairs (M+F) | External bulkhead connections (X1/X3/X4 + spare) | 4 pair | Amazon | $20–$32 |
| 1/2" NPT 90° elbow polypropylene | All pump-driven run bends | 14 ea | Amazon | $28–$56 |
| Banjo EL100-90 elbow 1" NPT | PP 90°; IBC bends, filter outlet to DV-01 | 4 ea | Amazon | $12–$20 |
| 1/2" NPT polypropylene tee | Blue suction/discharge tees, branches | 6 ea | Amazon | $12–$24 |
| Banjo TEE100 equal tee 1" NPT | PP; IBC drain tees (the X1 fill is now a 4-way cross) | 3 ea | Amazon | $12–$18 |
| 1" NPT 4-way cross fitting | X1 fresh-fill 4-way: X1 inlet + IBC-1 + IBC-2 + DV-01 blue recycle return (was a 3-way tee). Cost est. | 1 ea | Amazon | $8–$14 |
| 1/2" NPT polypropylene union | Maintenance disconnects on pump runs | 6 ea | Amazon | $24–$36 |
| 1/2"×1" NPT bushing reducer | P-02 riser to F1 filter inlet | 1 ea | Amazon | $3–$5 |
| S60×6 to 1" NPT adapter | IBC DN50 valve to 1" HDPE; PP S60×6 male × 1" NPT female | 8 ea | Amazon | $64–$120 |
| 1" bulkhead tank-body fittings (Blue equalization cross-tie) | Low tank-body penetration in each Blue tote (IBC-1 + IBC-2) for the 1" equalization cross-tie that self-balances the two Blue levels (run made from the 1" HDPE stock). Cost est. | 2 ea | Amazon | $12–$24 |
| 1" NPT spring check valve (CV1 — X1 gravity fill) | PVC body, EPDM seal, 1" FNPT × FNPT. Only CV-1 (X1 fill) remains — the Shurflo 2088 pumps have integral check valves, so CV-2/CV-3/CV-4 are redundant and dropped | 1 ea | Amazon | $8–$14 |
| Thread seal tape (PTFE) | 1/2" wide, 260" roll | 4 roll | Home Depot | $8 |
| [1/2" SDR-11 HDPE pipe](https://www.ferguson.com) | All pump-driven runs (80 ft); matches pump port size | 4 stick | Ferguson | $24–$40 |
| 1" SDR-11 HDPE pipe | Food-safe blue-stripe 20 ft; filter outlet + IBC lines | 1 stick | Ferguson | $12–$18 |
| Banjo TEE100 equal tee, 1" HDPE NPT | X1 fill tee — splits the fill to both Blue totes | 1 ea | Amazon | $4–$6 |
| 3/4" SDR-11 HDPE pipe | Spray bar run, 20 ft sticks | 2 stick | Ferguson | $20–$30 |
| 1/2" ID reinforced braided PVC hose | Pump inlet flexible connection, 6 ft per pump | 2 length | Amazon | $20 |
| 14 AWG duplex marine wire | Tinned copper, 25 ft | 1 roll | Amazon | $22 |
| Anderson Powerpole connectors 30A | Pump connections | 4 pair | Amazon | $8 |
| 10A blade fuses (pack) | Pump circuits (C1–C4) | 1 pack | Amazon | $5 |
| 6-mil black LDPE sheeting | 20 ft × 100 ft roll | 1 roll | Home Depot | $100 |
| [Apera Instruments AI311 PH60 pH meter](https://www.amazon.com/Apera-Instruments-AI311-Replaceable-2-00-16-00/dp/B01ENFOIQE) | Waterproof, 0–16 range, ±0.01 accuracy | 1 ea | Amazon | $55 |
| pH calibration solution set | pH 4 + pH 7 buffer sachets | 1 set | Amazon | $10 |
| Citric acid, food grade, 5 lb | pH adjustment (acidifier) | 2 bag | Amazon | $28 |
| Chemical-resistant labels (GHS) | For IBC totes | 1 pack | Amazon | $20 |
| Nitrile gloves, box of 100 | Size M/L | 2 box | Amazon | $28 |
| **Water total** | | | | **$1,995–$2,970** |
<!-- END parts:water -->

*The processing tray (§6.1), spray bar (§6.2), and IBC stacking frame are itemized in their own
reports — [Processing Tray & Spray Bar](processing-tray-and-spray-bar.md) and
[IBC Stacking](ibc-stacking-report.md) — and roll into the Total cost summary below.*

---

### Total cost summary

| Category | Low estimate | High estimate |
|----------|-------------|--------------|
| Water storage (4x IBC totes + bulkhead fittings) | $420 | $760 |
| Pumps and accumulator (P-01, P-02, P-04 manifold + P-03 IBC corridor) | $305 | $355 |
| Filter unit (3-stage combo + cartridges) | $470 | $652 |
| Valves and fittings (incl. S60×6 adapters, check valves) | $414 | $660 |
| Pipe | $76 | $108 |
| Processing tray (see [Processing Tray report](processing-tray-and-spray-bar.md) §6.1) | <!-- BEGIN costing:tray-low -->$1,300<!-- END costing:tray-low --> | <!-- BEGIN costing:tray-high -->$2,015<!-- END costing:tray-high --> |
| Spray bar assembly (see [Processing Tray report](processing-tray-and-spray-bar.md) §6.2) | <!-- BEGIN costing:spray-low -->$287<!-- END costing:spray-low --> | <!-- BEGIN costing:spray-high -->$375<!-- END costing:spray-high --> |
| Electrical (wiring only — fuse block in [Electrical Report](electrical-report.md)) | $35 | $35 |
| Processing consumables | $231 | $278 |
| **TOTAL** | **$3,486** | **$5,162** |

*Used IBC totes drive significant savings vs. new. The parts list consolidates to 4 primary suppliers: **Amazon** (~30 line items — qualifies for bulk/subscribe discounts), **McMaster-Carr** (tray hardware — single order, fast shipping), **Ferguson** (HDPE pipe — call for contractor pricing), and **Online Metals** (SS sheet). Obtain quotes from Ferguson before ordering pipe from Amazon — trade counter pricing is typically 20–30% below retail.*

---

## 9. Maintenance

| Task | Frequency | Notes |
|------|-----------|-------|
| Replace F-1 (50-micron cartridge) | ~Every 10 prints | Visually inspect — replace sooner if heavily discolored |
| Replace F-2 (5-micron cartridge) | Every 10 prints | Replace sooner if flow rate drops |
| Replace F-3 (GAC carbon) | Every 15 prints | Replace if taste/odor test fails |
| Flush Brown IBC-3 | Every 5 prints | Rinse with clean water, inspect for sediment buildup |
| pH check of filtered output | Every session | Before returning Brown water to Blue system |
| Drain and rinse Blue IBCs | Annually (or before long storage) | Prevent biofilm formation |
| Inspect IBC-4 valve and cap | Before every transport | Check for leaks |

---

## 10. Safety Notes

1. **Ferricyanide in alkaline conditions:** Do not allow IBC-4 waste water to contact strong alkalis (sodium hydroxide, bleach). In alkaline + UV conditions, ferricyanide can release trace cyanide ions. Keep pH < 7.5 in all containers. This is a theoretical rather than acute risk at the concentrations involved, but is worth managing.

2. **Prussian blue is non-toxic** — it is approved as a human antidote medication in some contexts — but the fine particles are a skin/eye irritant. Wear nitrile gloves and eye protection when handling wash trays.

3. **Citric acid dosing:** Always dissolve before adding to tank. Adding dry acid to iron-rich water can cause a brief exothermic reaction and bubbling. Mix in a separate container first.

4. **IBC-4 waste transport:** Ensure IBC cap is sealed and ball valve is closed before transport. Label contents before transport. The liquid is not classified as DOT hazardous material at these concentrations, but label clearly and keep upright. Drain remotely via external bulkhead port to a disposal tanker.

5. **Electrical:** Both pumps draw 7.5A each at 12V. The fuse block must be rated to handle simultaneous operation. Do not run pumps from the same fused circuit.

---

## 11. Source References

**Chemistry and safety:**
- [Photrio — Composition of cyanotype wash water](https://www.photrio.com/forum/threads/composition-of-cyanotype-wash-water.126234/)
- [Ask MetaFilter — Disposing of cyanotyping water](https://ask.metafilter.com/374714/Disposing-of-cyanotyping-water)
- [FMCSA ELDT curriculum (HDPE chemical resistance reference)](https://tpr.fmcsa.dot.gov/content/Resources/ELDT-Curriculum-Summary.pdf)

**Suppliers — consolidated by provider (see shopping list for direct part links):**
- [Amazon](https://www.amazon.com) — Pumps (Shurflo 2088), accumulator, filter housings, cartridges, Banjo valves/fittings, check valves, IBC adapters, electrical, consumables
- [McMaster-Carr](https://www.mcmaster.com) — Bulkhead fittings, tray hardware (bulkhead union, gasket, bolts)
- [Ferguson Plumbing Supply](https://www.ferguson.com) — HDPE pipe (1" and 3/4" SDR-11)
- [Container Exchanger](https://containerexchanger.com/geo-sale-ads/us-ca/bulk-containers/ibc-totes-for-sale) — Used IBC totes, California
- [Online Metals](https://www.onlinemetals.com) — 304 SS sheet for processing tray
- [Ronaqua](https://www.ronaqua.com) — GAC carbon filter cartridges

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
