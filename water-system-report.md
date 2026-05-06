<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Cyanotype Processing Water System
## Remote-Operation Design for the Giant Pinhole Camera

*For a camera deployed off-grid without access to running water or mains drainage.*
*Image plane: 5,893 × 2,388 mm (~140 sq ft). Container: 20 ft standard ISO shipping container.*

---

## Executive Summary

The camera operates in remote locations with no mains water or drainage. This document specifies a self-contained three-circuit water system that:

- Stores sufficient clean water for 8–10 full-size prints between resupply runs
- Recycles used wash water through a three-stage filter train, extending usable supply by approximately 40%
- Contains all waste water in closed, transportable drums for proper off-site disposal
- Runs entirely on 12V DC, compatible with a solar/battery off-grid power system

**Three circuits:**

| Circuit | Color code | Purpose | Storage |
|---------|-------------|---------|---------|
| **Blue** | Blue — clean | Fresh water supply for processing | 2× 600L IBC totes (≈316 gal total), Y-stacked in right end zone |
| **Brown** | Brown — used | Collected wash water; filtered and recycled back to Blue | 1× 600L IBC tote, Y-stacked behind Blue IBCs |
| **Black** | Black — waste | Heavily contaminated water; sealed drums for off-site disposal | 2× 55 gal HDPE drums (110 gal), side-by-side in right end zone |

---

## 1. Cyanotype Wash Water — Chemistry and Constraints

### What is in the wash water?

When a cyanotype print is washed, the water picks up:

| Compound | Source | Notes |
|----------|--------|-------|
| Ferric ammonium citrate (FAC) | Unexposed sensitiser | Water-soluble, pale yellow; low toxicity |
| Potassium ferricyanide | Sensitiser component | Water-soluble, yellow-orange; low acute toxicity |
| Prussian blue particles | Exposed image pigment wash-off | Fine blue solid particles, ~1–10 micron |
| Iron(III) compounds | Oxidation products | Colour the water blue-grey |

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

## 2. Water Volume Calculations

### Per-print water requirement

Processing a 140 sq ft print on the container floor, flooded to 6 mm (¼ inch) depth:

```
Volume per flood = 140 sq ft × (6 mm / 304.8) = 140 × 0.0197 ft = 2.76 cu ft
                 = 2.76 × 7.48 = 20.6 gallons ≈ 21 gallons per wash cycle
```

| Wash cycle | Water source | Volume | Drain to |
|-----------|-------------|--------|---------|
| Wash 1 — 5 min | Blue (clean) | 21 gal | Brown tank |
| Wash 2 — 5 min | Brown (recycled) | 21 gal | Brown tank |
| Wash 3 — 5 min | Blue (clean) | 21 gal | Brown tank → Black if >3 recycles |
| **Total per print** | | **~42 gal net Blue consumed** | |

### Storage capacity vs. print count

| Scenario | Blue consumed per print | Prints from 550 gal Blue | Brown recycled |
|----------|------------------------|--------------------------|---------------|
| No recycling | 63 gal (3 × 21) | ~8 prints | 0 |
| With recycling (wash 2 from Brown) | 42 gal (2 × 21) | **~13 prints** | ~168 gal reused |
| Brown recycle limit (3 passes) | — | — | 110 gal max before going to Black |

**Design target: 10 prints per resupply run** — comfortably achievable with the 550-gallon Blue supply.

---

## 3. System Architecture

### 3.1 Blue System — Clean Water Supply

```
IBC-1 (275 gal) ──┐
                   ├──→ Manifold → BV-01 → P-01 → ACC-01 → BV-02 → Distribution
IBC-2 (275 gal) ──┘                                                      │
                                                                          ↓
                                                              FLOOD/SPRAY BAR
                                                              ↓ (Processing tray)
```

- Two IBC totes plumbed in parallel via 1" HDPE manifold with isolation valves
- P-01: Shurflo 2088 12VDC diaphragm pump — 3.5 GPM, 45 PSI, self-priming
- ACC-01: 1-gallon pressure accumulator — smooths pump cycling, maintains pressure when pump is off
- Low-level float switch on IBC-2 alerts operator when Blue supply is low
- Spray bar: 3/4" HDPE tube running the width of the processing area with 1" NPT spray inlets every 600 mm for even flood distribution
- Fill inlet (top of IBC-1): 2" camlock connection for resupply from water bowser or tanker

### 3.2 Brown System — Used Water Recycling

```
Processing tray drain
        │
   3W-DV-02 ──────────────────────────────────────────→ (to Black drums if heavily loaded)
        │
        ↓
   IBC-3 (275 gal buffer)
        │
       P-02
        │
       F-1 (50-micron sediment)
        │
       F-2 (5-micron sediment)
        │
       F-3 (GAC carbon block)
        │
     pH TEST POINT (manual meter check before returning)
        │
   3W-DV-01 ──→ pH 6–7, visually acceptable: RETURN TO IBC-2 (Blue)
        │
        └──→ pH drift / discoloured: FORWARD TO Black drums
```

**Filter train sizing:**

| Stage | Housing | Cartridge | Removes | Replace interval |
|-------|---------|-----------|---------|-----------------|
| F-1 | Big Blue 4.5"×10" | 50-micron poly depth | Gross sediment, Prussian blue particles | Every 20 prints |
| F-2 | Big Blue 4.5"×10" | 5-micron poly sediment | Fine particles, residual blue | Every 10 prints |
| F-3 | Big Blue 4.5"×10" | GAC carbon block | Organics, colour, taste | Every 15 prints |

**pH management:** If filtered water reads pH <6, do nothing — slightly acidic is preferred. If pH >7.5, add citric acid solution (10g citric acid in 1 litre water) via the dosing port in the IBC-3 outlet, stir, retest. Do not return water with pH >8 to the Blue system.

### 3.3 Black System — Waste Containment

```
FROM 3W-DV-01 (rejected filter output)
FROM 3W-DV-02 (direct bypass — heavily contaminated first rinse, if needed)
        │
   DRUM-1 (55 gal) → OVERFLOW → DRUM-2 (55 gal)
        │
   Sealed, labelled per GHS/OSHA
        │
   TRANSPORT to licensed liquid waste disposal facility
```

- Drums are DOT-compliant UN-rated 55-gallon HDPE closed-head drums
- Bungs sealed with drum wrench before transport
- Label each drum: contents, date, location, UN numbers for ferricyanide/iron compounds
- **Do not leave drums open** — evaporation and UV exposure can drive ferricyanide chemistry

### 3.4 Processing Tray

Print washing takes place inside the container on a shallow processing tray that sits on the optical zone floor. The tray collects wash water and gravity-drains to 3W-DV-02 (the Brown/Black diverter valve).

**Tray specification:**

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Material | 16-gauge (1.5mm) 304 stainless steel, #4 brushed finish | Chemically inert to ferricyanide wash water; stainless resists pitting from citric acid pH adjustment |
| Overall footprint | 3,984 × 2,240 mm (2 panels, field-bolted) | Fits inside film plane rails (X=625–4,649) with 20mm clearance per side. Clears carriage travel (Y=100–2,262) with 30mm margin |
| Panel size (each) | 1,992 × 2,240 mm | Two equal panels, butted at midpoint and sealed with silicone gasket + bolted flange. Each panel fits through the cargo door opening (2,340 × 2,280 mm) |
| Rim height | 50 mm (all four sides) | Contains 6mm flood depth with margin. Maximum height constrained to 75mm by film plane carriage clearance at 140mm (rail offset 100mm + carriage 40mm) |
| Floor-to-rim height | 50 mm | Tray sits directly on the container floor. No riser needed — drain is at tray floor level |
| Fall | 1:200 (10mm over 1,992mm) toward pinhole wall (Y=0) | Gravity drain to a single 1" NPT bulkhead fitting at the low corner |
| Drain fitting | 1" NPT stainless bulkhead union, welded to tray floor at low point (X=2,637, Y=60) | Connects via 1" HDPE pipe to existing 3W-DV-02 diverter valve |
| Weight (empty) | ~110 kg (2 panels × ~55 kg) | 304 SS, 1.5mm × 4.46 m² per panel × 7.93 kg/m² per mm |

**Clearance verification:**

| Constraint | Clearance | Status |
|------------|-----------|--------|
| Film plane carriage blocks (Z=140mm at max tilt) | 90mm above tray rim (140 − 50) | Clear |
| Film plane rails at X=625 and X=4,649 (rail channel 20mm wide) | 20mm gap between tray edge and rail | Clear |
| Dolly track bridge sections (X=600–955, Z=30–70mm, transport mode only) | Tray left edge at X=645 — bridge track enters at X=600. 45mm overlap. **Tray must be installed after bridge tracks are removed during operational mode conversion. Bridge tracks are only used during transport mode.** | Clear — operational sequence prevents conflict |
| Pump manifold drain outlet (X=2,600–2,900, Y=0, Z=200–600) | Tray drain pipe routes along pinhole wall (Y=0) below manifold at Z=0–50. Manifold is at Z=200 minimum | Clear |
| Spray bar (overhead, Z=400–600 estimated) | 350mm+ above tray rim | Clear |
| Waste drums (X=40–620, left end zone) | Tray starts at X=645 — 25mm gap to drum footprint edge | Clear |
| IBCs (X=4,674+, right end zone) | Tray ends at X=4,629 — 45mm gap | Clear |

**Installation and removal:**

The tray is installed as part of operational mode conversion (after waste drums are rolled to their working positions and bridge tracks removed). The two panels are carried through the cargo door, positioned between the film plane rails, bolted together at the center flange, and the drain hose connected to the 3W-DV-02 stub. For transport mode conversion, the process reverses: disconnect drain, unbolt panels, carry out through cargo door, stow panels vertically against the container exterior or in a transport rack.

**Containment liner:** A fresh 6-mil black LDPE sheet is laid over the tray surface before each session. The liner prevents direct stainless-to-print contact (avoiding metallic marks on wet cyanotype) and simplifies cleanup. Overlap the liner 50mm over the tray rims.

---

## 4. Processing Procedure — Step by Step

### Before each session
1. Check Blue IBC levels — minimum 100 gal required per print session
2. Check Black drums — must have at least 55 gal headroom before starting
3. Run Brown recycle pump for 2 minutes to verify filter flow and check pH
4. Confirm processing tray is installed and drain hose is connected to 3W-DV-02
5. Lay fresh 6-mil black LDPE containment sheet over the tray surface, overlap 50mm over rims
6. Verify all valves in correct position (see valve matrix below)

### Print processing
1. Expose print in camera (no water involved)
2. Transfer print to processing tray in subdued light — lay face-up on containment liner
3. Open BV-02 (Blue supply) → flood print with 21 gal via spray bar — 5 minutes
4. Close BV-02 → open 3W-DV-02 to Brown (floor drain to IBC-3) → drain
5. If Brown tank has filtered stock: pump filtered water via spray bar for Wash 2 — 5 minutes → drain to Brown
6. Wash 3: open BV-02 → 21 gal clean Blue water → 5 minutes → drain
7. Inspect print — optional brightener: 0.5% hydrogen peroxide mist, 2 minutes, water rinse
8. Hang print to dry — use internal or external line
9. Allow residual water to gravity-drain from tray to Brown or Black as appropriate

### Valve matrix

| Valve | Default | Wash 1 | Drain 1→Brown | Wash 2 (recycled) | Drain 2→Brown | Wash 3 | Drain 3 |
|-------|---------|--------|---------------|-------------------|---------------|--------|---------|
| BV-01 (Blue manifold) | Open | Open | Open | Open | Open | Open | Open |
| BV-02 (Blue to floor) | Closed | **Open** | Closed | Closed | Closed | **Open** | Closed |
| 3W-DV-02 (tray drain) | Brown | Brown | **Brown** | Brown | **Brown** | Brown | **Brown** |
| P-02 (Brown pump) | Off | Off | Off | **On** | Off | Off | Off |
| 3W-DV-01 (filter out) | Blue return | Blue | Blue | Blue | Blue | Blue | Blue |

---

## 5. Plumbing Specification

### Pipe sizing

| Circuit | Pipe | Size | Pressure rating | Material |
|---------|------|------|----------------|---------|
| Blue supply main | Sch 40 / SDR-11 | 1" nominal | 100 PSI min | HDPE |
| Brown recycle | Sch 40 / SDR-11 | 1" nominal | 100 PSI min | HDPE |
| Spray bar | SDR-11 | 3/4" nominal | 100 PSI min | HDPE |
| Filter inlet/outlet | Sch 40 | 1" nominal | 100 PSI min | HDPE |
| Tray drain | Sch 40 / SDR-11 | 1" nominal | gravity | HDPE |
| Black waste gravity drain | Sch 40 | 1" nominal | 50 PSI min | HDPE |

**Why HDPE, not PVC?** Standard grey PVC is not rated for photographic chemistry contact and can leach plasticisers. HDPE and CPVC are both acceptable. Do not use copper or galvanized fittings — iron compounds in the wash water will react.

### Fittings and connections

| Connection type | Use | Standard |
|----------------|-----|---------|
| 2" camlock (type A+B) | IBC tote inlet/outlet | Aluminum or polypropylene |
| 1" NPT threaded | Pump inlet/outlet, valve connections | HDPE or brass |
| 2" NPT bung | Drum fill/drain | HDPE bung plug |
| Push-fit / compression | Secondary connections | John Guest / Speedfit style |

---

## 6. Electrical — 12V DC Power

| Item | Current draw | Hours/print | Wh/print |
|------|-------------|-------------|---------|
| P-01 Blue pump (Shurflo 2088) | 7.5 A @ 12V | 0.25 hr (15 min run) | 22.5 Wh |
| P-02 Brown pump (Shurflo 2088) | 7.5 A @ 12V | 0.17 hr (10 min run) | 15.2 Wh |
| pH meter | <0.1 A | — | <1 Wh |
| **Total per print** | | | **~38 Wh** |

A 100 Ah 12V lithium battery (1,200 Wh usable) provides **>30 prints** of pump power without recharging. A modest 100W solar panel recharges in ~3–4 hours of sun.

---

## 7. Equipment Layout

See **Sheet 2 — Plan View** (`water-system-sheet2.png`) for the water-system-specific P&ID layout. IBCs are in the provably shadow-free **right end zone** (X=4,649–5,893mm); waste drums are in the **left end zone** (X=0–625mm, Z-stacked at Yd=25–605mm). The optical zone (X=625–4,649mm) is completely clear.

**Container floor plan — all systems (top-down, 1:75):**
![TBS-001 Container Floor Plan — All Systems](assets/container-floorplan.png)

IBCs are **Y-stacked** (front-to-back along the depth axis) in a single column at X=4,674mm, right-justified to the far end wall. The 2 × 55-gal drums are placed **one per Yd corner** of the left end zone — D-1 near the pinhole wall (Yd=25–605mm) and D-2 near the far wall (Yd=1,757–2,337mm). The light trap drum (Yd=806–1,556mm) sits between them with 201mm clearance either side.

| Zone | Contents | X (mm) | Yd (mm) | H (mm) |
|------|----------|--------|---------|--------|
| Right end zone | IBC-1 + IBC-2 Blue (600L each, stacked) | 4,674–5,893 | 100–1,116 | 0–2,020 |
| Right end zone | IBC-3 Brown (600L) | 4,674–5,893 | 1,141–2,157 | 0–1,010 |
| Left end zone | D-1 55-gal drum (near, pinhole wall corner) | 20–600 | 25–605 | 0–870 |
| Left end zone | D-2 55-gal drum (far, film plane corner) | 20–600 | 1,757–2,337 | 0–870 |
| Pinhole wall face | Pump manifold | 2,400–2,700 | Y=0 | 200–600 |
| Optical zone floor | Processing tray (2 panels) | 645–4,629 | 60–2,300 | 0–50 |
| Optical zone | No equipment | 625–4,649 | — | — |

All equipment clears the optical cone at every depth — shadow-free proof in [Equipment Layout Report](equipment-layout-report.md).

**Hose routing:** Pump manifold is wall-mounted at X=2,400–2,700mm on the pinhole wall (Y=0 face). Supply hoses run along the pinhole wall to the right end zone, then along the right end wall to the IBC inlets — maximum run ~5.5m (manifold to Brown IBC rear at Yd=1,141mm). Waste hose from manifold to drums runs to the left end zone — maximum run ~3m.

**Flexible drum connections:** The 55-gallon waste drums sit on V-groove roller dollies with 305mm of X-direction travel for transport mode conversion (see [Equipment Layout Report](equipment-layout-report.md) §6.1). The waste hose connection to each drum must use a flexible section to accommodate this movement. Each drum connects via a 1m coiled reinforced PVC hose (1" ID, rated 50 PSI) with quick-disconnect camlock fittings (1" polypropylene Type E × Hose Barb) at the drum bung and at the fixed floor pipe stub. The coiled hose absorbs 305mm of linear travel without kinking. Quick-disconnects are released before sliding drums for transport.

---

## 8. Parts List and Shopping List

### 8.1 Water storage

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| IBC tote 275 gal, food-grade, used/rinsed | HDPE cage tote, 2" ball valve | 3 | [Container Exchanger — CA listings](https://containerexchanger.com/geo-sale-ads/us-ca/bulk-containers/ibc-totes-for-sale) | $80–$150 | **$240–$450** |
| 55 gal HDPE drum, closed-head, UN-rated | Blue, 2" NPS + 2" buttress bungs | 2 | [BASCO USA](https://bascousa.com/55-gallon-closed-head-plastic-drum-blue.html) · [The Cary Company](https://www.thecarycompany.com/55-gallon-un-blue-hdpe-tight-head-drum-2-npt-2-buttress-fittings-un-rated) | $55–$75 | **$110–$150** |
| Drum bung wrench (2" NPT + 2" buttress) | Polypropylene | 1 | Amazon / BASCO | $12–$20 | **$15** |

**Storage subtotal: ~$365–$615**

### 8.2 Pumps and pressure management

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| Shurflo 2088-554-144 pump | 12VDC, 3.5 GPM, 45 PSI, 1/2" NPSM ports | 2 | [Amazon — Shurflo 2088](https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C) | $55–$70 | **$110–$140** |
| SeaFlo / Kohree pressure accumulator | 1 gal, 125 PSI, 1/2" NPT | 1 | [Amazon — SeaFlo accumulator system](https://www.amazon.com/SEAFLO-Water-Pump-Accumulator-System/dp/B076JHCCBH) | $25–$45 | **$35** |
| Pump mounting bracket (stainless) | For 2088 series | 2 | Amazon | $8–$12 | **$20** |

**Pump subtotal: ~$165–$195**

### 8.3 Filter skid

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| Big Blue filter housing 4.5"×10" | 1" NPT brass ports, pressure relief, wrench included | 3 | [Amazon — Geekpure Big Blue 10"](https://www.amazon.com/Geekpure-Filter-Housing-1-Inch-Bracket-Blue/dp/B07799BBST) · [Bluonics two-pack](https://www.bluonics.com/products/big-blue-10-inch-two-whole-house-water-filter-carbon-sediment-solid-housing) | $28–$45 each | **$85–$135** |
| 50-micron sediment cartridge 4.5"×10" | Polypropylene depth filter | 4 (+ spares) | [Amazon — Pentair Pentek DGD-5005](https://www.amazon.com/Pentair-Pentek-Sediment-Water-Filter/dp/B0CM8PY8Q9) | $8–$12 each | **$35–$50** |
| 5-micron sediment cartridge 4.5"×10" | Polypropylene wound/pleated | 4 (+ spares) | [Amazon — Pentair Pentek RFC-BB](https://www.amazon.com/Pentair-Pentek-Carbon-Water-Filter/dp/B0F1Z2TXKQ) | $10–$15 each | **$45–$60** |
| GAC carbon block 4.5"×10" | Granular activated carbon, 25-micron | 4 (+ spares) | [Amazon — Ronaqua Big Blue GAC](https://www.ronaqua.com/products/10-inch-big-blue-granular-activated-carbon-whole-house-water-filter) | $15–$22 each | **$65–$90** |
| Filter skid frame | 600×900mm slotted steel angle, DIY | 1 | Home Depot / Lowe's (steel angle iron) | $25–$40 | **$35** |

**Filter subtotal: ~$265–$370**

### 8.4 Valves and fittings

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| Ball valve 1" FNPT, full-bore | HDPE-body or brass, lever handle | 8 | Amazon / Home Depot / Ferguson Plumbing | $8–$14 | **$65–$110** |
| 3-way diverter valve 1" FNPT | L-port or T-port, HDPE compatible | 2 | [Amazon — 1" 3-way ball valve](https://www.amazon.com/3-way-ball-valve/s?k=1+inch+3+way+ball+valve) | $18–$30 | **$40–$60** |
| 2" camlock fitting pairs (M+F) | Polypropylene, 2" | 6 pairs | Amazon / Grainger | $5–$8/pair | **$35–$50** |
| 1" NPT elbows (HDPE) | 90° street elbow | 12 | Home Depot / Ferguson | $3–$5 | **$40–$60** |
| 1" NPT tees (HDPE) | Equal tee | 8 | Home Depot / Ferguson | $4–$6 | **$35–$50** |
| 1" NPT unions | For maintenance disconnects | 6 | Ferguson / Amazon | $6–$10 | **$40–$60** |
| Thread seal tape (PTFE) | 1/2" wide, 260" roll | 4 | Home Depot | $2 | **$8** |

**Valves & fittings subtotal: ~$263–$398**

### 8.5 Pipe

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| 1" SDR-11 HDPE pipe | Food-safe, blue-stripe, 20 ft sticks | 5 sticks (100 ft) | [Ferguson Plumbing Supply](https://www.ferguson.com) · Winsupply | $12–$18/stick | **$60–$90** |
| 3/4" SDR-11 HDPE pipe | Spray bar run, 20 ft sticks | 2 sticks (40 ft) | Ferguson / Winsupply | $9–$14/stick | **$20–$30** |
| 1/2" ID reinforced braided PVC hose | Pump inlet flexible connection, 6 ft per pump | 2 lengths | Home Depot / Amazon | $8–$12/length | **$20** |
| 1" ID reinforced coiled PVC hose | Drum flex connection, 1m per drum (305mm travel) | 2 lengths | Home Depot / Amazon | $10–$15/length | **$20–$30** |
| 1" polypropylene camlock (Type E × Hose Barb) | Quick-disconnect at drum and floor stub | 4 pairs | Amazon / Grainger | $5–$8/pair | **$20–$32** |

**Pipe subtotal: ~$140–$202**

### 8.6 Processing tray

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| 304 SS sheet, 16-ga (1.5mm) | #4 brushed, 4'×8' sheets | 4 | [Metal Supermarkets](https://www.metalsupermarkets.com) · [Online Metals](https://www.onlinemetals.com) | $180–$250/sheet | **$720–$1,000** |
| Fabrication (cut, brake, weld) | Two tray halves: each 1,992×2,240mm with 50mm rims, 1:200 fall, welded corners | 1 job | Local sheet metal shop (e.g. Valley Metal Fab, SoCal) | $400–$800 | **$400–$800** |
| 1" NPT SS bulkhead union | 304 SS, welded to tray floor at drain point | 1 | [McMaster-Carr #4464K115](https://www.mcmaster.com) · Grainger | $18–$30 | **$25** |
| Silicone gasket strip, FDA grade | 1/16" × 1" × 10 ft, for center flange seal | 1 roll | McMaster-Carr / Amazon | $15–$25 | **$20** |
| M6×16 SS hex bolts + flange nuts | Center flange bolts, 200mm spacing | 24 | McMaster-Carr / Bolt Depot | $0.50 each | **$12** |

**Processing tray subtotal: ~$1,177–$1,857**

*Fabrication cost varies significantly by region. Get quotes from at least two local shops. For DIY builders with access to a sheet metal brake and TIG welder, material cost alone is $720–$1,000.*

### 8.7 Electrical

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| 12V fuse block (6-way) | Blade fuse, 10A per channel | 1 | Amazon | $12–$20 | **$15** |
| 14 AWG duplex marine wire | Tinned copper, 25 ft | 1 roll | West Marine / Amazon | $18–$28 | **$22** |
| Anderson Powerpole connectors | 30A, for pump connections | 4 pairs | Amazon | $1.50/pair | **$8** |
| 10A blade fuses (pack) | For pump circuits | 10 | Amazon / AutoZone | $5/pack | **$5** |

**Electrical subtotal: ~$50**

### 8.8 Processing consumables

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| 6-mil black LDPE sheeting | 20 ft × 100 ft roll | 1 | Home Depot / Uline | $80–$120 | **$100** |
| pH meter (waterproof) | 0–14 range, ±0.1 accuracy | 1 | [Amazon — Apera Instruments PH20](https://www.amazon.com/Apera-Instruments-Waterproof-Automatic-Calibration/dp/B01LZ5KCNX) | $35–$55 | **$45** |
| pH calibration solution set | pH 4 + pH 7 buffer sachets | 1 set | Amazon | $8–$12 | **$10** |
| Citric acid, food grade, 5 lb | pH adjustment (acidifier) | 2 bags | Amazon / bulk food supplier | $12–$18 | **$28** |
| Chemical-resistant labels (GHS) | For drums and totes | 1 pack | Amazon / Labelmaster | $15–$25 | **$20** |
| Funnel with filter screen (2") | For drum filling | 2 | Amazon / Grainger | $8–$12 | **$18** |
| Nitrile gloves, box of 100 | Size M/L | 2 boxes | Amazon / Home Depot | $12–$18 | **$28** |

**Consumables subtotal: ~$249–$304**

---

### 8.9 Total cost summary

| Category | Low estimate | High estimate |
|----------|-------------|--------------|
| Water storage (IBC totes + drums) | $365 | $615 |
| Pumps and accumulator | $165 | $195 |
| Filter skid (housings + cartridges) | $265 | $370 |
| Valves and fittings | $263 | $398 |
| Pipe (incl. drum flex hoses) | $140 | $202 |
| Processing tray (304 SS, fabricated) | $1,177 | $1,857 |
| Electrical | $50 | $50 |
| Processing consumables | $249 | $304 |
| **TOTAL** | **$2,674** | **$3,991** |

*Used IBC totes drive significant savings vs. new. Ferguson Plumbing Supply and Grainger may offer better pricing on bulk pipe and fittings than retail stores — obtain quotes before ordering.*

---

## 9. Maintenance Schedule

| Task | Frequency | Notes |
|------|-----------|-------|
| Replace F-1 (50-micron cartridge) | Every 20 prints | Visually inspect — replace sooner if heavily discolored |
| Replace F-2 (5-micron cartridge) | Every 10 prints | Replace sooner if flow rate drops |
| Replace F-3 (GAC carbon) | Every 15 prints | Replace if taste/odour test fails |
| Flush Brown IBC-3 | Every 5 prints | Rinse with clean water, inspect for sediment buildup |
| pH check of filtered output | Every session | Before returning Brown water to Blue system |
| Drain and rinse Blue IBCs | Annually (or before long storage) | Prevent biofilm formation |
| Inspect drum bungs | Before every transport | Check for leaks |

---

## 10. Safety Notes

1. **Ferricyanide in alkaline conditions:** Do not allow Black drum water to contact strong alkalis (sodium hydroxide, bleach). In alkaline + UV conditions, ferricyanide can release trace cyanide ions. Keep pH < 7.5 in all containers. This is a theoretical rather than acute risk at the concentrations involved, but is worth managing.

2. **Prussian blue is non-toxic** — it is approved as a human antidote medication in some contexts — but the fine particles are a skin/eye irritant. Wear nitrile gloves and eye protection when handling wash trays.

3. **Citric acid dosing:** Always dissolve before adding to tank. Adding dry acid to iron-rich water can cause a brief exothermic reaction and bubbling. Mix in a separate container first.

4. **Black drum transport:** Ensure drums are sealed with bung wrench (≥20 Nm torque). Label contents before transport. The liquid is not classified as DOT hazardous material at these concentrations, but label clearly and keep upright.

5. **Electrical:** Both pumps draw 7.5A each at 12V. The fuse block must be rated to handle simultaneous operation. Do not run pumps from the same fused circuit.

---

## 11. Schematic Diagrams

| Drawing | File |
|---------|------|
| Sheet 1 — System flow schematic (P&ID) | `water-system-sheet1.png` |
| Sheet 2 — Equipment layout plan + parts list | `water-system-sheet2.png` |
| Container floor plan — all systems | See [Electrical & Systems Report](electrical-report.md) Section 5.8 |

**Sheet 1 — System Flow Schematic (P&ID)**
![Water System — Sheet 1: P&ID Flow Schematic](assets/water-system-sheet1.png)

---

**Sheet 2 — Equipment Layout Plan**
![Water System — Sheet 2: Equipment Layout](assets/water-system-sheet2.png)

---

## 12. Sources and References

- [Photrio — Composition of cyanotype wash water](https://www.photrio.com/forum/threads/composition-of-cyanotype-wash-water.126234/)
- [Ask MetaFilter — Disposing of cyanotyping water](https://ask.metafilter.com/374714/Disposing-of-cyanotyping-water)
- [Container Exchanger — IBC totes for sale, California](https://containerexchanger.com/geo-sale-ads/us-ca/bulk-containers/ibc-totes-for-sale)
- [BASCO USA — 55 gal closed-head HDPE drums](https://bascousa.com/55-gallon-closed-head-plastic-drum-blue.html)
- [The Cary Company — 55 gal UN-rated blue drum](https://www.thecarycompany.com/55-gallon-un-blue-hdpe-tight-head-drum-2-npt-2-buttress-fittings-un-rated)
- [Amazon — Shurflo 2088-554-144 pump](https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C)
- [Amazon — SeaFlo pump + accumulator system](https://www.amazon.com/SEAFLO-Water-Pump-Accumulator-System/dp/B076JHCCBH)
- [Amazon — Geekpure Big Blue 10" filter housing](https://www.amazon.com/Geekpure-Filter-Housing-1-Inch-Bracket-Blue/dp/B07799BBST)
- [Amazon — Pentair Pentek DGD-5005 sediment cartridge](https://www.amazon.com/Pentair-Pentek-Sediment-Water-Filter/dp/B0CM8PY8Q9)
- [Ronaqua — Big Blue GAC carbon cartridge](https://www.ronaqua.com/products/10-inch-big-blue-granular-activated-carbon-whole-house-water-filter)
- [Repackify — IBC totes for sale in California](https://www.repackify.com/buy-ibc-totes/california)
- [FMCSA ELDT curriculum (HDPE chemical resistance reference)](https://tpr.fmcsa.dot.gov/content/Resources/ELDT-Curriculum-Summary.pdf)
