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
open-process loss — water **carried out in the wet prints** (each full-plane muslin sheet, ~9.42 m²,
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
water bowser or tanker through the **X1** gravity-fill inlet (a 4-way cross feeds both Blue totes), and **discharge
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
                ├──→ Manifold → BV-01 → P-01 → ACC-01 → BV-05 → Distribution
IBC-2 (900L) ──┘                                                      │
                                                                          ↓
                                                              FLOOD/SPRAY BAR
                                                              ↓ (Processing tray)
```

- Two IBC totes plumbed in parallel via 1" PVC manifold with isolation valves
- The two Blue totes are tied at the base by a **1" equalization cross-tie** (tank body to tank body, low on the totes) so their levels self-balance as P-01 draws and X1 refills
- P-01: Shurflo 2088 12VDC diaphragm pump — 3.5 GPM, 45 PSI, self-priming
- **Check valves:** only **CV-1** is fitted, on the X1 gravity fill — the single flow path with no pump. Every return and drain leg is pump-driven, and the Shurflo 2088 pumps carry an **integral 1-way check valve** ([2088-554-144 datasheet](https://www.pumpagents.com/pdf/ShurfloPumps/2088-554-144.pdf)), so dedicated anti-siphon checks on the IBC-2 return, IBC-3 buffer return and IBC-4 waste legs would be redundant and are not used
- ACC-01: 0.75 L (23.5 oz) pressure accumulator — smooths pump cycling, maintains pressure when pump is off
- Low-level float switch on IBC-2 alerts operator when Blue supply is low
- Spray bar: gantry design — 40×25×3mm 304 SS RHS beam (laid flat, ~15mm pre-camber) spanning the open processing area (3,859mm) between walkway inner edges, with Ø32 wheel carriages rolling on the raised/sloped tray floor beneath walkway grating. A 3/4" LDPE manifold clipped to the beam side feeds 39 side-tapped 90° down-jet nozzles. See the [Processing Tray & Spray Bar](processing-tray-and-spray-bar.md) report for full mechanical design
- Fill inlet: single external 2" NPT bulkhead fitting (X1) with camlock on the container end wall centerline — gravity feed, no pump required. Inside, an internal 4-way cross (near X1) — where the DV-01 blue recycle also joins — splits to a SIDE entry near the top of BOTH Blue totes (no top-cap access — <!-- BEGIN fact:ibc_ceiling_clearance_mm -->52<!-- END fact:ibc_ceiling_clearance_mm -->mm headroom), filling them in parallel and gravity-linked — one external hose. Remote resupply from water bowser or tanker (no cargo door access required)

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
       F-1 (5-micron MPP sediment)
        │
       F-2 (KDF-55 heavy-metal)
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

The filter train is **three separate 4.5"×20" Big Blue housings** (Ø184 × 594mm each; Express Water / Geekpure / iSpring), mounted as a horizontal bank high on the pinhole wall — heads pinned near the ceiling, sumps hanging below. Each has 1" NPT inlet/outlet; a single 1/2"→1" bushing reducer matches P-02's 1/2" output to F-1, and F-1 → F-2 → F-3 connect by short 1" PVC jumpers with 90° elbows outside the bodies (full mechanical detail in [Plumbing Report](plumbing-report.md) §3.1).

| Stage | Cartridge (4.5"×20") | Removes |
|-------|---------------------|---------|
| F-1 | MPP 5-micron melt-blown polypropylene sediment | Gross sediment, fiber lint, Prussian blue particles |
| F-2 | KDF-55 heavy-metal removal | Dissolved iron compounds from ferricyanide wash water |
| F-3 | CTO coconut-shell activated carbon block | Residual organics, color |

The 4.5"×20" cartridges carry ~2× the media of a 10", so service intervals run correspondingly longer; the per-stage replacement intervals live in [Plumbing Report](plumbing-report.md) §3.1. A single 3-stage combo unit (4.5"×20" cartridges, 1" NPT) is an equivalent alternative that eliminates the inter-housing jumpers — any unit accepting standard 4.5"×20" cartridges with 1" NPT ports will work.

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

**Spray bar:** A 3,859mm span 304 SS RHS beam gantry (40×25×3mm, laid flat) rolls on the raised/sloped tray floor beneath the walkway grating. Water from P-01 (Blue supply) reaches the bar via BV-05 → 4m flexible hose → single center feed into the side LDPE manifold → 39 90° down-jet nozzles at 100mm centers, spraying straight down.

**Supply path:** P-01 → ACC-01 → rigid 1/2" PVC pipe along pinhole wall → BV-05 → coiled flexible hose → bulkhead fitting → beam bore → spray holes.

**Containment liner:** A fresh 6-mil black LDPE sheet is laid over the tray surface before each session to prevent direct stainless-to-print contact and simplify cleanup.

For full construction details, structural analysis, parts list, and engineering drawings, see [Processing Tray & Spray Bar](processing-tray-and-spray-bar.md).

---

## 5. Plumbing Specification

### Pipe sizing

All pump-driven internal runs use **1/2" pipe**, matching the Shurflo 2088 pump ports (1/2"-14 male parallel thread). This eliminates trunk-to-manifold reducer fittings entirely. The three Big Blue filter housings have 1" NPT ports: a single 1/2"→1" bushing reducer feeds F-1, the F-1→F-2 and F-2→F-3 jumpers are short 1" PVC with 90° elbows, and the F-3 outlet connects to DV-01 (1" FNPT). Larger pipe (1" or 2") is used only for the IBC fill/drain lines at the external bulkhead ports and the short filter outlet to DV-01, where gravity flow requires lower restriction. P-03 is mounted separately in the IBC plumbing corridor on the X4 waste drain run.

**Internal runs (1/2" PVC Sch-40):**

| Circuit | Pipe | Size | Pressure rating | Material |
|---------|------|------|----------------|---------|
| Blue supply (IBC → BV-01 → P-01) | Sch 40 | 1/2" nominal (OD 21mm) | 100 PSI min | PVC |
| Blue discharge (P-01 → ACC-01 → BV-05 → spray bar) | Sch 40 | 1/2" nominal (OD 21mm) | 100 PSI min | PVC |
| Brown suction (IBC-3 → P-02) | Sch 40 | 1/2" nominal (OD 21mm) | 100 PSI min | PVC |
| Brown riser (P-02 → F1 inlet) | Sch 40 | 1/2" nominal (OD 21mm) | 100 PSI min | PVC |
| Tray drain suction (sump → P-04) | Reinforced flex hose | 1/2" nominal | pump suction | PVC braid |
| DV-02 outputs (→ IBC-3, → IBC-4) | Sch 40 | 1/2" nominal (OD 21mm) | 50 PSI min | PVC |
| DV-01 outputs (→ Blue IBC-2, → Black IBC-4) | Sch 40 | 1/2" nominal (OD 21mm) | 50 PSI min | PVC |
| ACC-01 inlet/outlet | Sch 40 | 1/2" nominal (OD 21mm) | 125 PSI min | PVC |
| Spray bar | Sch 40 | 3/4" nominal | 100 PSI min | PVC |

**Filter unit outlet (1" PVC Sch-40):**

| Circuit | Pipe | Size | Pressure rating | Material |
|---------|------|------|----------------|---------|
| Filter train (F-3) outlet → SV-01 sample tap → DV-01 | Sch 40 | 1" nominal (OD 33mm) | 100 PSI min | PVC |

**IBC fill/drain (1" PVC Sch-40 — gravity flow, not pump-driven):**

| Circuit | Pipe | Size | Pressure rating | Material |
|---------|------|------|----------------|---------|
| External fill line (X1 bulkhead → 4-way cross → both Blue totes) | Sch 40 | 1" nominal (OD 33mm) | 50 PSI min | PVC |
| External drain lines (X3/X4 bulkhead → IBCs) | Sch 40 | 1" nominal (OD 33mm) | 50 PSI min | PVC |
| X1 fill 4-way cross (X1 in + IBC-1 + IBC-2 + DV-01 recycle) | — | 1" PVC cross (cross-100) | 50 PSI min | PVC |

At 3.5 GPM, flow velocity in 1/2" pipe (ID ~15.8mm) is approximately 1.1 m/s — well within the recommended 0.5–2.5 m/s range for water systems. The longest internal run (~5.5m from manifold to far-column IBC) contributes less than 0.3 bar friction loss at this velocity.

**Why PVC Sch-40?** **Rigid** PVC pipe (Sch-40/80, "uPVC") is *unplasticized* — the plasticizer-leaching concern applies to *flexible* PVC (vinyl tubing), not the rigid run, and NSF-61 potable-grade rigid PVC is water-safe and chemically compatible with the dilute cyanotype wash (potassium ferricyanide, ferric ammonium oxalate, citric acid). PVC is chosen over HDPE for **buildability** — it solvent-welds with primer + cement and hand tools, whereas HDPE can't be glued (see the joint convention in [Plumbing Report](plumbing-report.md) §5.1–5.2). Only the flexible pump-connection hose is braided PVC. Do not use copper or galvanized fittings — iron compounds in the wash water will react.

### Fittings and connections

| Connection type | Use | Standard |
|----------------|-----|---------|
| 2" camlock (type A+B) | IBC tote inlet/outlet | Aluminum or polypropylene |
| 1" NPT threaded | Filter (F-3) outlet → DV-01, inter-housing jumpers, IBC fill/drain lines | PVC or brass |
| 1/2" NPT threaded | All pump-driven runs, pump ports, manifold connections, ACC-01, ball valves | PVC or brass |
| 1/2"×1" NPT bushing reducer | P-02 riser to F1 filter inlet (1 required) | Polypropylene or brass |
| 2" NPT bulkhead | External fill/drain port (container wall) | 304 SS |
| Push-fit / compression | Secondary connections | John Guest / Speedfit style |

---

## 6. Electrical — 12V DC Power

| Item | Current draw | Hours/print | Wh/print |
|------|-------------|-------------|---------|
| P-01 Blue pump (Shurflo 2088) | 7.5 A @ 12V | 0.25 hr (15 min run) | 22.5 Wh |
| P-02 Filter-loop feed pump (Shurflo 2088) | 7.5 A @ 12V | 0.17 hr (10 min run) | 15.2 Wh |
| P-03 Waste pump (Shurflo 2088) — *IBC corridor* | 7.5 A @ 12V | intermittent (waste disposal only) | — |
| P-04 Tray drain transfer pump (Shurflo 2088) | 7.5 A @ 12V | 0.08 hr (5 min run) | 7.5 Wh |
| P-05 Brown drain-out pump (Shurflo 2088) — *IBC corridor* | 7.5 A @ 12V | intermittent (drain-out only) | — |
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
| Pinhole wall face | Pinhole Wall panel — P-02 + 3-stage filter bank (high, sumps hanging) | 3,300–3,976 | ~100 | 1,746–2,340 |
| IBC plumbing corridor | Corridor panel — P-01/P-03/P-04/P-05 + ACC-01 | 4,654–5,104 | 1,046–1,316 | 355–1,930 |
| Optical zone floor | Processing tray | 170–4,629 | 60–2,300 | 0–50 |
| Optical zone | No equipment | 150–4,649 | — | — |

All equipment clears the optical cone at every depth — shadow-free proof in [Equipment Layout Report](equipment-layout-report.md).

**Hose routing:** The corridor pumps (P-01, P-04, P-05, P-03) mount on the **Corridor Plumbing Panel** at the front of the IBC stack, reaching into the 270mm plumbing corridor between the two IBC columns — so the pump↔tote suction and return lines are **short**, running entirely within the corridor to the IBCs' corridor-facing DN50 valves. P-02 (Brown filter feed) and the 3-stage filter stack sit on the **Pinhole Wall Plumbing Panel** on the pinhole wall face. The longest run is the **Blue supply to the spray bar**: P-01 → ACC-01 → rigid 1/2" PVC along the pinhole wall to the tray center → BV-05 → ~4m coiled flexible hose → the rolling beam in the optical zone. The **tray drain** returns the other way — P-04's sump pickup → 1" flexible hose over the near rim → P-04 on the panel → 3W-DV-02 diverter → IBC-3 (Brown) or IBC-4 (Waste). **Waste evacuation** pumps P-05 (X3 / Brown) and P-03 (X4 / Waste) sit directly on the corridor drain risers, minimizing pipe to the external end-wall ports. The four lines that connect the corridor equipment to the Pinhole Wall panel run together as a flat **ribbon** in the dead space under the right-walkway grate — see [Plumbing Report](plumbing-report.md) §8.1 and [Walkway Pipe Routing](walkway-routing-sections.md).

**External fill/drain ports:** Three 2" NPT bulkhead fittings with camlock fittings on the exterior are mounted on the container end wall centerline, stacked vertically:

| Port | Function | Connects to |
|------|----------|-------------|
| X1 — Fill Blue | Fresh water supply fill | IBC-1 (top, near column) — gravity feed |
| X3 — Drain Brown | Used water drain | IBC-3 (bottom, near column) |
| X4 — Drain Waste | Waste water drain | IBC-4 (bottom, far column) |

A single external fill port (X1) feeds an internal 1" 4-way cross in the corridor — where the DV-01 blue recycle return also joins — which splits the flow to BOTH Blue IBCs (each branch **side-enters** the tote's corridor face near the top, 150mm + flange — no top-cap access, only <!-- BEGIN fact:ibc_ceiling_clearance_mm -->52<!-- END fact:ibc_ceiling_clearance_mm -->mm headroom). The two top totes fill in parallel, so only one external hose is needed — without a separate cross-connect pipe.

This allows remote filling (from water bowser or tanker) and draining (IBC-3/IBC-4 to disposal tanker) without opening the cargo doors or entering the container. Internal plumbing from each port routes through the 270mm central corridor between the two IBC columns to reach the respective tote. All ports are accessible from the container exterior.

---

## 8. Parts List

<!-- BEGIN parts:water -->
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [IBC tote (1,000 L caged)](https://www.repackify.com/buy-ibc-totes/california) | Reconditioned food-grade (prior-food-contents) 275-gal/1000L caged composite tote, DN50 butterfly valve (S60×6 thread); side-entry fittings near top. ~$150/ea local SoCal (Container Exchanger food-grade lots have a ~12-tote min; buy 4 local). Firm ~$150. | 4 ea | SoCal reconditioner / Repackify | $600 |
| [Bulkhead fitting 2" NPT (304 SS)](https://www.mcmaster.com/4464K115) (4464K115) | External fill/drain port, welded through container wall | 3 ea | McMaster-Carr | $410 |
| [Shurflo 2088-554-144 pump (×5 — P-01 Blue supply / P-02 filter loop / P-03 waste evac / P-04 tray drain / P-05 Brown drain)](https://www.amazon.com/dp/B00C1M6B1C) (B00C1M6B1C) | 12VDC, 3.5 GPM, 45 PSI, 1/2" NPSM ports; 5 identical pumps, one per water-system duty (P-01..P-05). 2026-07-27: consolidated from 5 lines; firm $100 ea (Amazon B00C1M6B1C, was $80–89 Fresh Water Systems est) | 5 ea | Amazon / Fresh Water Systems | $500 |
| [SeaFlo accumulator (0.75 L)](https://www.amazon.com/dp/B01MUYL8F8) (SFAT-075-125-01) | 0.75 L, 125 PSI, 1/2" MNPT | 1 ea | Amazon | $36 |
| Shurflo pump mounting bracket | Stainless, 2088 series — one per pump (P-01..P-05) | 5 ea | Fresh Water Systems | $50 |
| [Corridor plumbing-panel ply (23/32" exterior)](https://www.homedepot.com/p/23-32-in-x-4-ft-x-8-ft-RTD-Southern-Yellow-Pine-Wood-Sheathing-Plywood-129323/303564747) (303564747) | 4×8 ft 23/32" (18mm) RTD Southern Yellow Pine exterior sheathing — rear backing board + drain-riser spine + spacer offcuts. STANDARD exterior per project rule (was mis-spec'd marine ~$179-250). Firm $29.30 (Home Depot 2026-07-23). Seal cut edges. | 1 sheet | Home Depot | $29 |
| [Pump-mount shirt ply (23/32" exterior)](https://www.homedepot.com/p/23-32-in-x-4-ft-x-8-ft-RTD-Southern-Yellow-Pine-Wood-Sheathing-Plywood-129323/303564747) (303564747) | 4×8 ft 23/32" (18mm) RTD Southern Yellow Pine exterior sheathing — pump-mount shirt (~610×1650 cut) behind P-01..P-05 + 6× spacer blocks. Same SKU as ply-18; 5× Shurflo 2088 (~6.5 kg total) need no more than 3/4". STANDARD exterior per project rule (was marine ~$212). Firm $29.30 (Home Depot 2026-07-23). May nest with ply-18 in one sheet at cut — carried separate for margin. Double-layer locally if extra pump-rail stiffness wanted. | 1 sheet | Home Depot | $29 |
| 6× steel angle brackets (corridor panel → IBC uprights) | L-brackets fixing the corridor plumbing panel to the IBC-frame front-portal uprights. Price est. | 6 ea | Home Depot | $15–$39 |
| Corridor panel mount fasteners (shirt-to-panel screws + lag bolts) | Shirt-to-panel screws + lag bolts landing the brackets into the panel/uprights. Price est. | 1 lot | Home Depot | $10–$11 |
| [Big Blue filter housing 4.5"×20" (separate)](https://www.amazon.com/dp/B0137680E6) (B0137680E6) | Ø184×594mm/housing (4.5×20), 1" NPT ports, accepts standard 20"×4.5" cartridges (Alvin-verified 2026-07-27) — three SEPARATE Pentair Pentek 150234 high-flow PP housings on the mounting brackets | 3 ea | Amazon | $250 |
| [Big Blue housing mounting brackets (×3)](https://www.freshwatersystems.com/products/mounting-bracket-white-single-housing-for-10-20-big-blue-housings) (150061) | Pentair 150061 zinc-plated single-housing mounting bracket, one per 4.5×20 Big Blue (×3), lag-screwed to the 18mm ply backing. Purpose-built — replaces the welded slotted-angle frame (Alvin 2026-07-27). | 3 ea | Fresh Water Systems | $32 |
| [SS lag/wood screws — filter housings to ply backing](https://www.homedepot.com/p/302007729) (812670) | 2 per housing × 3 = 6 needed — Everbilt 5/16"×1½" SS hex lag screws through the housing's mounting-hole ears into the 18mm plywood backing (no custom bracket). Sold in 5-packs → 2 packs (10, 4 spare). | 2 5-pack | Home Depot | $14 |
| Plywood offcut spacer blocks 25mm (filter skid) | 25mm standoff blocks between the housing's mounting ears and the ply backing — sump-bowl hang clearance (the housing lag-screws through them into the ply). Cut from PLYWOOD OFFCUTS (Alvin 2026-07-25 — no need for HDPE; dry standoff, not a wet-immersion part). | 1 lot | offcuts | $0 |
| [MPP 5-micron sediment cartridge 4.5"×20"](https://www.amazon.com/dp/B0CJCVZ1L5) (B0CJCVZ1L5) | Pentek DGD-5005-20 dual-gradient-density 5-micron sediment cartridge (F-1 stage); ~50-print interval. $61.66/2-pack = $30.83 ea. | 2 ea | Amazon | $62 |
| [KDF-55 heavy-metal cartridge 4.5"×20"](https://www.amazon.com/dp/B0DY1ZK47Z) (B0DY1ZK47Z) | KDF-55 media for dissolved iron/metal removal (F-2 stage); ~60-print interval. Aquaboon 20×4.5 KDF whole-house cartridge (proper KDF media — supersedes the earlier VEVOR chlorine-only cartridge). | 1 ea | Amazon | $80 |
| [CTO carbon block cartridge 4.5"×20"](https://www.amazon.com/dp/B07ZHPB6MB) (B07ZHPB6MB) | Coconut shell activated carbon block (F-3 stage); ~40-print interval. Aquaboon CTO, $79.79/2-pack = $39.90 ea (same brand as the KDF/sediment cartridges). | 2 ea | Amazon | $80 |
| [Banjo V050FP ball valve 1/2" FNPT](https://www.usplastic.com/catalog/item.aspx?itemid=30651) (30651) | PP full-port quarter-turn; pump-suction isolation BV-01 (P-01), BV-02 (P-05), BV-06 (P-03) | 3 ea | US Plastic Corp / Amazon | $133 |
| [Banjo V050FP ball valve 1/2" FNPT](https://www.usplastic.com/catalog/item.aspx?itemid=30651) (30651) | PP full-port quarter-turn; pump-suction isolation BV-03 (P-02) | 1 ea | US Plastic Corp / Amazon | $44 |
| [Banjo V050FP ball valve 1/2" FNPT](https://www.usplastic.com/catalog/item.aspx?itemid=30651) (30651) | PP full-port; supply isolation BV-04 (TAP-01 chem tap), BV-05 (spray-bar feed) | 2 ea | US Plastic Corp / Amazon | $89 |
| [Banjo V100FP ball valve 1" FNPT](https://www.usplastic.com/catalog/item.aspx?itemid=30653) (30653) | PP full-port; V1/V3/V4, VB1–VB3 (IBC fill/drain) | 6 ea | US Plastic Corp / Amazon | $297 |
| [3-way diverter valve 1/2" FNPT](https://www.usplastic.com/catalog/item.aspx?itemid=22365) (22365) | L/T-port PVC-compatible; 3W-DV-02 (tray drain) | 1 ea | US Plastic Corp | $24 |
| [3-way diverter valve 1" FNPT](https://www.usplastic.com/catalog/item.aspx?itemid=31268) (31268) | L/T-port; 3W-DV-01 (filter output) | 1 ea | US Plastic Corp | $61 |
| [pH sample tap (SV-01) — 1/2" PP ball valve + barb spout + branch tee](https://www.usplastic.com/catalog/item.aspx?itemid=36903) (36903) | Filtered-water sample draw before 3W-DV-01; 1/2" PP sample valve (US Plastic 36903) + downturned 1/2" hose barb on a 1"×1/2" reducing branch tee, panel face above spill line | 1 ea | US Plastic Corp | $19 |
| [pH sample tap (SV-02) — 1/2" PP ball valve + barb spout + branch tee](https://www.usplastic.com/catalog/item.aspx?itemid=36903) (36903) | pH sample on the P-04 tray-drain discharge, before 3W-DV-02; same build/SKU as SV-01 (US Plastic 36903 $19.26 — Alvin priced SV-01; applied to SV-02 as the identical build) | 1 ea | US Plastic Corp | $19 |
| [2" polypropylene camlock pairs (M+F)](https://www.usplastic.com/catalog/item.aspx?itemid=30754) (30754) | External bulkhead connections (X1/X3/X4 + spare). 2026-07-27: pair = US Plastic 30754 female coupler $16.23 + 30619 male adapter $6.70 = $22.93 (Banjo FRPP, EPDM) | 4 pair | US Plastic Corp | $92 |
| [1/2" PVC Sch-40 slip 90° elbow](https://www.homedepot.com/p/203812033) (PVC023000600HD) | All pump-driven run bends. Charlotte PVC Sch-40 90° S×S — CONFIRMED slip / solvent-cement (Alvin 2026-07-28), NOT threaded. | 14 ea | Home Depot | $10 |
| [1" PVC Sch-40 slip 90° elbow](https://www.homedepot.com/p/203812125) (PVC023001000HD) | 1" PVC slip run bends (joint convention §5.1): IBC bends, filter outlet to DV-01. 2026-07-27 fork b — was threaded Banjo FRPP $4.59. Charlotte PVC023001000HD 90° S×S. | 4 ea | Home Depot | $6 |
| [1/2" PVC Sch-40 slip tee](https://www.homedepot.com/p/203812195) (PVC024000600HD) | Blue suction/discharge tees, branches. Charlotte PVC Sch-40 S×S×S — CONFIRMED slip / solvent-cement (Alvin 2026-07-28), NOT threaded. | 6 ea | Home Depot | $5 |
| [1" PVC Sch-40 slip tee](https://www.homedepot.com/p/203812199) (PVC024001000HD) | 1" PVC slip run tees (joint convention §5.1): 3× IBC drain. 2026-07-27: X1 fill split dropped — X1 is a 4-way cross (cross-100), not a tee (was qty 4). Charlotte PVC024001000HD S×S×S. | 3 ea | Home Depot | $6 |
| [1/2" PVC slip×MNPT male adapter](https://www.homedepot.com/p/203811636) (PVC021090600HD) | ½" landings (22 — P&ID takeoff 2026-07-28): 6× BV ball valves (BV-01–06, run side) + 5× pump discharges (P-01–05, hose→run) + 3W-DV-02 (3 ports) + SV-01/SV-02 taps (2) + accumulator ACC-01 (1, slip×FPT) + 2× ½" unions (4, slip×MNPT each side) + bushing-reducer ½" run side (1). Charlotte PVC021090600HD. | 22 ea | Home Depot | $17 |
| [1" PVC slip×MNPT male adapter](https://www.homedepot.com/p/203811640) (PVC021091000HD) | 1" landings (26 — P&ID takeoff 2026-07-28): 6× V100 valves (V1/V3/V4, VB1–3, run side) + 8× s60-adapter IBC-valve landings (each lands on its own 1" glued-run segment) + 3W-DV-01 (3 ports) + CV-1 (2 ports) + 5× filter housing ports (F-01 OUT, F-02 IN/OUT, F-03 IN/OUT; F-01 IN = bushing-reducer) + 2× Blue equalization bulkheads. Charlotte PVC021091000HD. | 26 ea | Home Depot | $30 |
| [1" PVC 4-way cross fitting](https://www.amazon.com/dp/B0CGGV74MB) (B0CGGV74MB) | X1 fresh-fill 4-way (Alvin-confirmed 2026-07-27): X1 inlet + IBC-1 + IBC-2 + DV-01 blue-recycle riser all join here on the corridor spine, then distribute to both Blue totes. 1" PVC cross — slip glue joint, gravity/low-pressure fill. Design of record: the 3D model + corridor panel-layout + plumbing-report all build this cross. | 1 ea | Amazon | $6 |
| [1/2" PVC Sch-40 slip coupling](https://www.homedepot.com/p/203811331) (PVC021000600HD) | Permanent solvent-weld run joins (4×). Charlotte PVC Sch40 S×S coupling. | 4 ea | Home Depot | $3 |
| [1/2" PVC union (serviceable break)](https://www.homedepot.com/p/317901071) (PVCU12F) | True hand-unscrew unions at the 2 points where a whole sub-assembly must come out as a unit (pump manifold + filter-bank inlet). Apollo ½" PVC FIP×FIP (threaded) union — lands on the slip run via a slip×MNPT adapter each side (4 total across the 2 unions, in the pvc-adapter-half allowance). | 2 ea | Home Depot | $10 |
| [1/2"×1" NPT bushing reducer](https://www.homedepot.com/p/204836713) (PVC021121800HD) | P-02 riser → F1 filter inlet — THREADED (lands on the filter = hard component, per the joint convention). Charlotte PVC Sch40 1×½ reducer bushing | 1 ea | Home Depot | $3 |
| [S60×6 female buttress → 2" MNPT IBC tote adapter](https://www.amazon.com/Granatan-Adapter-Buttress-Fittings-Connector/dp/B095SCHBC6) (B095SCHBC6) | IBC DN50 tote outlet (male S60×6) → 2" male NPT, polypropylene (Granatan). No US single-piece S60→1" NPT exists (the 1" ones are BSP or garden-hose thread), so reduce 2"→1" via s60-reducer. $9.99 firm (Alvin 2026-07-29). | 8 ea | Amazon | $80 |
| [2"→1" PVC Sch-80 reducing coupling (FNPT×FNPT)](https://www.homedepot.com/p/203811533) (PVC021071300HD) | Charlotte 2"×1" PVC Sch-40 reducer bushing, SPIGOT×SLIP (solvent-weld), $3.21 (Alvin 2026-07-29). INTERFACE FLAG: the s60-adapter output is 2" MALE NPT and a spigot×slip bushing is glue-only, so it needs a 2" MPT×socket transition to mate (or swap to a 2"FNPT×1" reducer). Verify the tote-adapter interface at the bench. | 8 ea | Home Depot | $26 |
| [1" MNPT × 1" hose barb (Banjo HB100)](https://www.usplastic.com/catalog/item.aspx?itemid=135135) (31527) | Tote-side barb — 1" MNPT threads onto the reduced tote-adapter port; flex hose slips onto the barb. Banjo HB100 glass-reinforced PP, 300 psi. $1.79 firm (Alvin 2026-07-29). | 8 ea | US Plastic Corp | $14 |
| [1" FNPT × 1" hose barb (Banjo)](https://www.usplastic.com/catalog/item.aspx?itemid=135154) (31544) | Run-side barb — flex hose slips on; its 1" FNPT receives the pvc-adapter-1in (1" MNPT) that glues to the run. Banjo glass-reinforced PP. $3.00 firm (Alvin 2026-07-29). | 8 ea | US Plastic Corp | $24 |
| [#20 stainless hose clamp (10-pack)](https://www.homedepot.com/p/330548109) (IDL0410PK) | 2 clamps per flex jumper × 8 = 16 (2× 10-packs, 4 spare). Apollo 300-series SS #12 (½in–1¼in), external. $18.52/10-pack (Alvin 2026-07-29). SIZE FLAG: verify the #12 (max 1¼in) closes over the 1¼in-OD tray-suction hose + barb — a #16 may be needed if it bottoms out. | 2 10-pack | Home Depot | $37 |
| [1" bulkhead tank-body fittings (Blue equalization cross-tie)](https://www.usplastic.com/catalog/item.aspx?itemid=32194) (32194) | Low tank-body penetration in each Blue tote (IBC-1 + IBC-2) for the 1" equalization cross-tie that self-balances the two Blue levels (run made from the 1" PVC stock). Confirmed firm $12.62 (Alvin 2026-07-28); SKU 32194 (alternate listing itemid 65992). | 2 ea | US Plastic Corp | $25 |
| [1" NPT spring check valve (CV1 — X1 gravity fill)](https://www.usplastic.com/catalog/item.aspx?itemid=31415) (31415) | PVC body, EPDM seal, 1" FNPT × FNPT. Only CV-1 (X1 fill) remains — the Shurflo 2088 pumps have integral check valves, so CV-2/CV-3/CV-4 are redundant and dropped | 1 ea | US Plastic Corp | $24 |
| [Steel flat bar 25×3mm — ribbon support cross-brace](https://www.mcmaster.com/6775T37-6775T373/) (6775T37) | Low-carbon steel flat bar 25×3mm × 3 ft. Welded between the two right-walkway long bearers at 4 stations to carry the under-walkway pipe ribbon (four corridor↔pinhole lines); 4 braces ~300mm each = cut from 2× 3-ft bars (2 spare pieces). | 2 3ft bar | McMaster-Carr | $35 |
| Cushioned pipe clip | Secures the four under-walkway ribbon lines to the support cross-braces (4 lines × 4 supports) | 16 ea | Amazon | $16–$32 |
| Thread seal tape (PTFE) | 1/2" wide, 260" roll | 4 roll | Home Depot | $8 |
| [1/2" PVC Sch-40 pipe](https://www.homedepot.com/p/319692959) (30-05010HD) | All pump-driven runs (~80 ft = 8× 10-ft sticks), PVC Sch-40 solvent-weld (IPEX potable-pressure). Matches pump port size. | 8 stick | Home Depot | $38 |
| [1" PVC Sch-40 pressure pipe](https://www.homedepot.com/p/319692953) (22405) | IPEX 1"×10 ft white PVC Sch-40 POTABLE PRESSURE water pipe (model 22405); ~40 ft = 4× 10-ft sticks; filter inter-stage/outlet + IBC internal fill/drain manifold + X1 fill + equalization tie. Pressure-rated (Alvin 2026-07-28). Re-count DONE 2026-07-29 (Alvin): 2→4 sticks — the IBC-zone 1" internal fill/drain (§5 pipe table, ~39 ft total) was omitted from the old 20 ft estimate. | 4 stick | Home Depot | $35 |
| [3/4" PVC Sch-40 pipe](https://www.homedepot.com/p/100348472) (PVC-04007-0600) | Spray bar run, PVC Sch-40 pressure pipe (plain end), 2× 10-ft sticks. $5.76/stick (Alvin sent $576 — read as a decimal typo; ¾" pressure pipe sits between the ½" $4.81 and 1" $8.65). Re-count vs actual run length. | 2 stick | Home Depot | $12 |
| [1/2" ID reinforced braided PVC hose](https://www.usplastic.com/catalog/item.aspx?itemid=60703) (60703) | Pump inlet flexible connection, 6 ft per pump | 2 length | US Plastic Corp | $12 |
| 14 AWG duplex marine wire | Tinned copper, 25 ft | 1 roll | Waytek Wire | $22 |
| Anderson Powerpole connectors 30A | Pump connections — one pair per pump (P-01..P-05) | 5 pair | Powerwerx | $10 |
| 15A blade fuse | Pump Circuit C (single feed, all pumps) | 1 ea | Waytek Wire | $5 |
| [6-mil black LDPE sheeting](https://www.homedepot.com/p/332821399) (59803) | Film-Gard 8 ft × 100 ft × 6-mil black poly (800 sq ft). Water splash/light-proof sheeting + the tray liners are cut from this same roll (tray-liner line retired 2026-07-27 — same material, ~10 liners/roll). Re-count area if the water use alone exceeds 800 sq ft. | 1 roll | Home Depot | $55 |
| [Apera Instruments AI311 PH60 pH meter](https://www.amazon.com/dp/B01ENFOIQE) (B01ENFOIQE) | Waterproof, 0–16 range, ±0.01 accuracy | 1 ea | Amazon | $80 |
| pH calibration solution set | pH 4 + pH 7 buffer sachets | 1 set | Amazon | $10 |
| Citric acid, food grade, 5 lb | pH adjustment (acidifier) | 2 bag | Amazon | $28 |
| Chemical-resistant labels (GHS) | For IBC totes | 1 pack | Amazon | $20 |
| [Nitrile gloves, box of 100](https://www.amazon.com/dp/B0CMZ5VXMS) (B0CMZ5VXMS) | TitanFlex nitrile, textured, box of 100 (size M/L). | 2 box | Amazon | $30 |
| **Water total** | | | | **$3,716–$3,757** |
<!-- END parts:water -->

*The processing tray (§6.1), spray bar (§6.2), and IBC stacking frame are itemized in their own
reports — [Processing Tray & Spray Bar](processing-tray-and-spray-bar.md) and
[IBC Stacking](ibc-stacking-report.md) — and roll into the Total cost summary below.*

---

### Total cost summary

| Category | Low estimate | High estimate |
|----------|-------------|--------------|
| Water equipment — §8 BOM (IBC storage, pumps + accumulator, 3-stage filter train, valves & fittings, pipe, wiring, consumables) | $2,073 | $3,123 |
| Processing tray (see [Processing Tray report](processing-tray-and-spray-bar.md) §6.1) | <!-- BEGIN costing:tray-low -->$1,583<!-- END costing:tray-low --> | <!-- BEGIN costing:tray-high -->$2,271<!-- END costing:tray-high --> |
| Spray bar assembly (see [Processing Tray report](processing-tray-and-spray-bar.md) §6.2) | <!-- BEGIN costing:spray-low -->$377<!-- END costing:spray-low --> | <!-- BEGIN costing:spray-high -->$449<!-- END costing:spray-high --> |
| **TOTAL** | **$3,660** | **$5,513** |

*The Water-equipment row is the generated §8 `parts:water` BOM total (single source of record for the water subsystem — storage/pumps/filters/valves/pipe/consumables); the tray and spray-bar rows are `costing.py` blocks. The TOTAL is a hand sum of the three and should itself become a generated block (Phase-1 backlog).*

*Used IBC totes drive significant savings vs. new. The parts list consolidates to 4 primary suppliers: **Amazon** (~30 line items — qualifies for bulk/subscribe discounts), **McMaster-Carr** (tray hardware — single order, fast shipping), **Ferguson** (PVC pipe — call for contractor pricing), and **Online Metals** (SS sheet). Obtain quotes from Ferguson before ordering pipe from Amazon — trade counter pricing is typically 20–30% below retail.*

---

## 9. Maintenance

| Task | Frequency | Notes |
|------|-----------|-------|
| Replace F-1 (5-micron MPP sediment) | ~Every 50 prints | Visually inspect — replace sooner if heavily discolored (intervals: [plumbing §3.1](plumbing-report.md)) |
| Replace F-2 (KDF-55 heavy-metal) | ~Every 60 prints | Replace sooner if flow rate drops |
| Replace F-3 (GAC carbon block) | ~Every 40 prints | Replace if taste/odor test fails |
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

5. **Electrical:** Each pump draws 7.5A at 12V. All five pumps share a single **Circuit C** (12V, 15A fuse, 14 AWG) and run **one at a time**, so the single feed carries them — see [Plumbing Report §3.2](plumbing-report.md).

---

## 11. Source References

**Chemistry and safety:**
- [Photrio — Composition of cyanotype wash water](https://www.photrio.com/forum/threads/composition-of-cyanotype-wash-water.126234/)
- [Ask MetaFilter — Disposing of cyanotyping water](https://ask.metafilter.com/374714/Disposing-of-cyanotyping-water)
- [FMCSA ELDT curriculum (HDPE chemical resistance reference)](https://tpr.fmcsa.dot.gov/content/Resources/ELDT-Curriculum-Summary.pdf)

**Suppliers — consolidated by provider (see shopping list for direct part links):**
- [Amazon](https://www.amazon.com) — Pumps (Shurflo 2088), accumulator, filter housings, cartridges, Banjo valves/fittings, check valves, IBC adapters, electrical, consumables
- [McMaster-Carr](https://www.mcmaster.com) — Bulkhead fittings, tray hardware (bulkhead union, gasket, bolts)
- [Ferguson Plumbing Supply](https://www.ferguson.com) — PVC pipe (1" and 3/4" Sch-40)
- [Container Exchanger](https://containerexchanger.com/geo-sale-ads/us-ca/bulk-containers/ibc-totes-for-sale) — Used IBC totes, California
- [Online Metals](https://www.onlinemetals.com) — 304 SS sheet for processing tray
- [Ronaqua](https://www.ronaqua.com) — GAC carbon filter cartridges
