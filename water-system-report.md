<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Cyanotype Processing Water System
## Remote-Operation Design for the Giant Pinhole Camera

*For a camera deployed off-grid without access to running water or mains drainage.*
*Image plane: 4,499 × 2,388 mm (~116 sq ft). Processing tray: 4,459 × 2,200 mm (~106 sq ft). Container: 20 ft standard ISO shipping container.*

---

## Executive Summary

The camera operates in remote locations with no mains water or drainage. This document specifies a self-contained three-circuit water system that:

- Stores sufficient clean water for 8–10 full-size prints between resupply runs
- Recycles used wash water through a three-stage filter train, extending usable supply by approximately 40%
- Contains all waste water in a closed, transportable IBC for proper off-site disposal
- Runs entirely on 12V DC, compatible with a solar/battery off-grid power system

**Three circuits:**

| Circuit | Color code | Purpose | Storage |
|---------|-------------|---------|---------|
| **Blue** | Blue — clean | Fresh water supply for processing | 2× 600L IBC totes (≈316 gal total), Y-stacked in right end zone |
| **Brown** | Brown — used | Collected wash water; filtered and recycled back to Blue | 1× 600L IBC tote, Y-stacked behind Blue IBCs |
| **Black** | Black — waste | Heavily contaminated water; sealed IBC for off-site disposal | 1× 600L IBC tote (IBC-4, ~158 gal), Y-stacked in right end zone |

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

Processing a ~106 sq ft print in the processing tray (4,459 × 2,200 mm), flooded to 6 mm (¼ inch) depth:

```
Volume per flood = 106 sq ft × (6 mm / 304.8) = 106 × 0.0197 ft = 2.09 cu ft
                 = 2.09 × 7.48 = 15.6 gallons ≈ 16 gallons per wash cycle
```

| Wash cycle | Water source | Volume | Drain to |
|-----------|-------------|--------|---------|
| Wash 1 — 5 min | Blue (clean) | 16 gal | Brown tank |
| Wash 2 — 5 min | Brown (recycled) | 16 gal | Brown tank |
| Wash 3 — 5 min | Blue (clean) | 16 gal | Brown tank → Black if >3 recycles |
| **Total per print** | | **~32 gal net Blue consumed** | |

### Storage capacity vs. print count

| Scenario | Blue consumed per print | Prints from 316 gal Blue | Brown recycled |
|----------|------------------------|--------------------------|---------------|
| No recycling | 48 gal (3 × 16) | ~6 prints | 0 |
| With recycling (wash 2 from Brown) | 32 gal (2 × 16) | **~10 prints** | ~160 gal reused |
| Brown recycle limit (3 passes) | — | — | 158 gal max before going to Black |

**Design target: 10 prints per resupply run** — achievable with the 316-gallon (1,200L) Blue supply using Brown recycling for wash 2.

---

## 3. System Architecture

### 3.1 Blue System — Clean Water Supply

```
IBC-1 (600L) ──┐
                ├──→ Manifold → BV-01 → P-01 → ACC-01 → BV-02 → Distribution
IBC-2 (600L) ──┘                                                      │
                                                                          ↓
                                                              FLOOD/SPRAY BAR
                                                              ↓ (Processing tray)
```

- Two IBC totes plumbed in parallel via 1" HDPE manifold with isolation valves
- P-01: Shurflo 2088 12VDC diaphragm pump — 3.5 GPM, 45 PSI, self-priming
- ACC-01: 0.75 L (23.5 oz) pressure accumulator — smooths pump cycling, maintains pressure when pump is off
- Low-level float switch on IBC-2 alerts operator when Blue supply is low
- Spray bar: aluminum structural beam + 3/4" HDPE spray tube spanning the full processing tray width (4,459mm), riding on walkway grating. See §3.5 for full design
- Fill inlet: single external 2" NPT bulkhead fitting (X1) with camlock on the container end wall centerline (Yd=1,181mm) at Z=2,250mm — positioned above IBC tops (Z=2,082mm) for gravity feed to IBC-1, no pump required. IBC-2 self-levels via permanently open 2" cross-connect at valve height. Remote resupply from water bowser or tanker (no cargo door access required)

### 3.2 Brown System — Used Water Recycling

```
Processing tray sump (P-04 suction pickup)
        │
   P-04 (tray drain transfer pump — suction from sump, lifts ~900mm to IBC-3 fill cap)
        │
   3W-DV-02 ──────────────────────────────────────────→ (to IBC-4 waste if heavily loaded)
        │
        ↓
   IBC-3 (600L buffer, filled via DN150 fill cap on top)
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
        └──→ pH drift / discoloured: FORWARD TO IBC-4 (waste)
```

**Filter train sizing:**

The filter train uses a single 3-stage whole-house filter unit (e.g. [Purcooflow WHF2045B302](https://www.purcooflow.com/products/whf2045b302-3-stage-kdf-heavy-metal-water-filter) or equivalent) with 4.5"×20" Big Blue cartridges. This eliminates all inter-housing plumbing and the separate filter skid frame — the unit mounts directly to the pinhole wall with its integrated bracket. 1" NPT inlet/outlet; a single 1/2"→1" bushing reducer connects P-02 output to the unit inlet.

| Stage | Cartridge (4.5"×20") | Removes | Replace interval |
|-------|---------------------|---------|-----------------|
| F-1 | MPP 5-micron melt-blown polypropylene sediment | Gross sediment, fiber lint, Prussian blue particles | Every 25 prints |
| F-2 | KDF-55 heavy metal removal | Dissolved iron compounds from ferricyanide wash water | Every 30 prints |
| F-3 | CTO coconut shell activated carbon block | Residual organics, color, taste | Every 20 prints |

The 20" cartridges hold roughly 2× the media volume of the previous 10" cartridges, extending service life proportionally. The unit includes triple drain valves for flushing individual stages without disassembly. Equivalent 3-stage Big Blue units are available from iSpring (WGB32B), Express Water, and other vendors — any unit accepting standard 4.5"×20" cartridges with 1" NPT ports will work.

**pH management:** If filtered water reads pH <6, do nothing — slightly acidic is preferred. If pH >7.5, add citric acid solution (10g citric acid in 1 litre water) via the dosing port in the IBC-3 outlet, stir, retest. Do not return water with pH >8 to the Blue system.

### 3.3 Black System — Waste Containment

```
FROM 3W-DV-01 (rejected filter output — pH out of range)
FROM 3W-DV-02 (heavily contaminated drain water — operator judgment)
        │
   IBC-4 (600L waste)
        │
   Sealed, labelled per GHS/OSHA
        │
   TRANSPORT to licensed liquid waste disposal facility
```

- IBC-4 is a standard 600L HDPE cage tote with DN50 butterfly valve (S60×6 thread), identical frame to IBC-1 through IBC-3
- IBC-4 sits in the right end zone in a 2x2 stack: bottom-far position (Yd=1,316–2,332)
- Cap sealed before transport; label contents, date, location, UN numbers for ferricyanide/iron compounds
- Drained remotely via external 2" NPT bulkhead fitting with camlock on the container end wall centerline (Yd=1,181mm, Z=200mm) — no need to open cargo doors
- **Do not leave IBC valve open** — evaporation and UV exposure can drive ferricyanide chemistry

### 3.4 Processing Tray

Print washing takes place inside the container on a shallow processing tray that sits on the optical zone floor. Water collects at the low point and is pumped out by P-04 via a sump pickup — there is no penetration of the tray floor or container floor.

**Tray specification:**

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Material | 16-gauge (1.5mm) 304 stainless steel, #4 brushed finish | Chemically inert to ferricyanide wash water; stainless resists pitting from citric acid pH adjustment |
| Overall footprint | 4,459 × 2,200 mm (2 panels, field-bolted) | Fits inside film plane rails (X=150–4,649) with 20mm clearance per side. Spans Yd=80–2,280 |
| Panel size (each) | 2,229 × 2,200 mm | Two equal panels, butted at midpoint and sealed with silicone gasket + bolted flange. Each panel fits through the cargo door opening (2,340 × 2,280 mm) |
| Rim height | 50 mm (all four sides) | Contains 6mm flood depth with margin. Maximum height constrained to 75mm by film plane carriage clearance at 140mm (rail offset 100mm + carriage 40mm) |
| Floor-to-rim height | 50 mm | Tray sits on tapered HDPE shim strips on the container floor (see slope support below) |
| Fall | 1:200 dual-axis (10mm over 2,200mm Yd-axis + 11mm over 2,229mm X-axis) toward sump at near rim center | Water converges from both axes toward the sump well |
| Sump well | 150 × 100 mm, 20mm deep, pressed into tray floor at low point (X=2,399, Yd=80) | Collects water at lowest point; P-04 suction pickup tube sits in sump |
| Weight (empty) | ~116 kg (2 panels × ~58 kg) | 304 SS, 1.5mm × 4.90 m² per panel × 7.93 kg/m² per mm |

**Slope support — tapered HDPE shim strips:**

The tray's 1:200 dual-axis slope is achieved by tapered HDPE shim strips bonded to the container floor beneath the tray. No risers, no under-tray plumbing — the tray sits directly on the shims.

| Parameter | Value |
|-----------|-------|
| Material | HDPE flat bar, 50mm wide |
| Quantity | 5 strips running the full tray depth (Yd direction, 2,200mm each) |
| Spacing | ~1,000mm apart across tray width (X direction) |
| Profile | Tapered: 0mm at near rim (Yd=80, drain end) → 10mm at far rim (Yd=2,280) |
| Attachment | Construction adhesive (Loctite PL Premium or equivalent) to container floor |
| Function | Creates the Yd-axis slope. X-axis slope is formed into the tray panels during fabrication (pressed crown) |

**Sump well and pickup:**

Instead of a through-floor drain fitting, the tray has a shallow sump well pressed into the floor at the low point. P-04 draws water from the sump via a suction pickup tube — no penetration of the tray floor or the container floor.

| Parameter | Value |
|-----------|-------|
| Sump dimensions | 150mm (X) × 100mm (Yd) × 20mm deep |
| Sump location | X=2,399mm (tray center), Yd=80mm (near rim, low point) |
| Sump forming | Pressed/stamped into tray panel during fabrication |
| Pickup tube | 1" HDPE dip tube, stainless foot valve with strainer screen (prevents debris) |
| Pickup height | Tube bottom 5mm above sump floor (leaves ~0.75L residual) |
| Suction line | 1" flexible reinforced hose from pickup tube, routed over near rim to P-04 suction inlet on pump manifold |
| Pump | P-04 (Shurflo 2088, 12V DC, 3.5 GPM, 45 PSI, self-priming) |
| Discharge | P-04 output → 3W-DV-02 diverter → IBC-3 (Brown) or IBC-4 (Waste) |

**Why sump pickup instead of a through-floor drain:**

1. **No penetration** — eliminates leak risk from a bulkhead fitting seal under the tray
2. **No under-tray clearance needed** — tray sits flat on shim strips, no plumbing runs below
3. **Simpler fabrication** — pressed sump is cheaper and more reliable than a welded bulkhead union
4. **Easier to protect** — no exposed plumbing beneath the tray that could be damaged during transport
5. **Field-serviceable** — pickup tube lifts out for cleaning; no tools required

**Clearance verification:**

| Constraint | Clearance | Status |
|------------|-----------|--------|
| Film plane carriage blocks (Z=140mm at max tilt) | 90mm above tray rim (140 − 50) | Clear |
| Film plane rails at X=150 and X=4,649 (rail channel 20mm wide) | 20mm gap between tray edge and rail | Clear |
| Container left end zone equipment (X=0–625) | Tray left edge at X=170 — extends into optical zone only | Clear |
| Pump manifold (X=4,800–5,580, Yd=1,046, Z=900–1,400) — equipment panel | Suction hose routes over tray rim at Z=50, along rim exterior to equipment panel. No conflict | Clear |
| Spray bar (rides on walkway grating, Z=100mm deck) | Slides along Yd on walkway surfaces, below carriage height (Z≈140mm) | Clear |
| IBCs (X=4,674+, right end zone) | Tray ends at X=4,629 — 45mm gap | Clear |

**Permanent installation:**

The processing tray is permanently installed — it remains in place during both operational and transport modes. The two panels are positioned between the film plane rails, bolted together at the center flange. The P-04 suction pickup tube sits in the sump well permanently; the flexible suction hose routes over the near rim, along the rim exterior, and across to the equipment panel in the IBC corridor. The 50mm rim height is below all transport-mode clearance envelopes, so no removal is required for mode conversion. This eliminates the former 15–20 minute mode conversion procedure (dolly track removal, drum repositioning, tray install); mode conversion now requires only the panel slide (~5 minutes).

**Containment liner:** A fresh 6-mil black LDPE sheet is laid over the tray surface before each session. The liner prevents direct stainless-to-print contact (avoiding metallic marks on wet cyanotype) and simplifies cleanup. Overlap the liner 50mm over the tray rims. Cut or fold the liner around the sump pickup tube.

### 3.5 Spray Bar Assembly

The spray bar delivers Blue (clean) and Brown (recycled) water evenly across the full width of the processing tray during print washing. The operator slides the bar along the length of the print (Yd direction, from film-plane side toward the pinhole wall), flooding the surface progressively.

**Design constraints:**

- Must span the full processing tray width (4,459mm, X=170–4,629mm) including the areas beneath both walkway gratings, to ensure the entire print receives even wash coverage
- Single-operator use — push/pull from the near walkway
- Must be stiff enough to avoid excessive sag over a 3.9m unsupported span
- Must travel 2,200mm along Yd (tray depth, from near rim to far rim)
- Must accommodate a flexible water connection that follows the bar as it moves

**Assembly components:**

| Component | Specification | Purpose |
|-----------|--------------|---------|
| Structural beam | 6061-T6 aluminum SHS, 4,459mm long (see sizing below) | Spans tray width, supports spray tube, resists sag |
| Spray tube | 3/4" HDPE SDR-11, 4,459mm long, clamped to beam underside | Water distribution with drilled spray holes |
| Runner pads (×2) | UHMW polyethylene blocks, ~100×50×30mm | Slide on walkway grating surface at each end |
| Guide rail (×2) | 25×25×3mm aluminum angle, ~2,200mm long, bolted to grating | Keeps bar tracking straight along Yd axis |
| Push pole | Telescoping aluminum pool pole, 1.2–2.4m | Operator controls bar position from near walkway |
| Pole clip | Stainless spring clip or quick-release bracket | Attaches pole to beam center |
| Flexible hose | 1/2" reinforced braided PVC, ~4m coiled length | Connects BV-02 to spray tube feed end |
| Pipe clamps (×8) | Stainless steel, 3/4" hose clamp or nylon zip ties | Secure HDPE tube to aluminum beam |
| End caps (×2) | 3/4" HDPE threaded cap | Seal spray tube ends |
| Feed adapter | 3/4" FNPT × 1/2" barb reducer | Connects flexible hose to spray tube inlet |

**Structural beam sizing:**

The beam is supported at the inner edges of the left and right walkways (X=470 and X=4,329, span=3,859mm), with 300mm overhangs at each end resting on the walkway grating. Load includes beam self-weight, spray tube, water in tube, and hardware.

| Beam size | I (mm⁴) | Beam mass | Total assembly | Center deflection | Span ratio |
|-----------|---------|-----------|---------------|-------------------|------------|
| 25×25×3mm (1"×1"×⅛") | 21,692 | 2.8 kg | 6.2 kg | 22.8mm | L/169 |
| 30×30×3mm (1¼"×1¼"×⅛") | 39,852 | 3.6 kg | 7.1 kg | 14.1mm | L/274 |
| **40×40×3mm (1½"×1½"×⅛")** | **101,972** | **4.9 kg** | **8.3 kg** | **6.5mm** | **L/595** |
| **50×25×3mm (2"×1"×⅛") rect.** | **125,542** | **4.2 kg** | **7.6 kg** | **4.8mm** | **L/797** |
| 50×50×3mm (2"×2"×⅛") | 208,492 | 6.1 kg | 9.6 kg | 3.6mm | L/1058 |

**Recommended:** 40×40×3mm aluminum SHS (widely available as 1-1/2" × 1-1/2" × 1/8" at Home Depot, metals suppliers). Center deflection of 6.5mm (L/595) is acceptable for a spray application. Total assembly weight ~8.3kg.

**Alternative:** 50×25×3mm rectangular tube oriented tall (2" × 1" × 1/8"). Stiffer (4.8mm, L/797) and lighter (7.6kg) but less commonly stocked. Use if available.

**Runner and guide system:**

Each end of the beam rides on a UHMW polyethylene slider pad that rests on the walkway grating surface (Z=100mm). The grating is press-locked steel mesh with ~60% open area — water from the spray tube passes through the mesh to reach the print below the walkway. The pads are bolted to the beam ends with stainless M6 bolts.

A guide rail (25×25×3mm aluminum angle, 2,200mm long) is bolted to each walkway grating along the Yd direction. The UHMW pad has a groove that captures the angle's vertical leg, preventing lateral drift as the operator pushes the bar. The guide rail also defines the start and end positions of the bar's travel.

**Clearances:**

| Interface | Dimension | Status |
|-----------|-----------|--------|
| Tray rim to grating bottom | 25mm (Z=50 to Z=75) | Spray tube passes through this gap — 3/4" HDPE OD=26.7mm is tight; tube mounts flush against beam underside, clears at beam centerline height |
| Grating surface to beam bottom | 30mm (runner pad height) | UHMW pad lifts beam above grating |
| Beam top (Z=170mm max) to film carriage (Z=140mm max tilt) | No conflict — spray bar is in Yd=80–2,280 zone, film carriage rides on rails at Yd edges | Clear |

**Spray hole pattern:**

The HDPE spray tube has 3mm holes drilled at 100mm intervals along the bottom centerline (45 holes total across 4,459mm). At 3.5 GPM (P-01 flow rate) and 45 PSI system pressure, each hole delivers approximately 0.08 GPM. Holes are deburred to prevent drip accumulation. Alternatively, 1/4" FNPT tee adapters at 600mm intervals (8 nozzles) with adjustable fan-spray tips provide more even distribution but add cost and assembly time.

**Flexible hose connection:**

BV-02 (1/2" ball valve, Blue supply isolation) is mounted on the pinhole wall (Yd=0) at Z≈150mm, near the near-wall tray rim. A 4m length of 1/2" reinforced braided PVC hose connects from BV-02 to the spray bar feed adapter at one end (X=170, the left/near end of the bar). The hose is coiled when the bar is near the pinhole wall (Yd=80) and extends as the bar is pushed toward the far wall (Yd=2,280). The hose trails along the near tray rim, staying clear of the print surface.

The supply path is: P-01 → ACC-01 → rigid 1/2" HDPE pipe along pinhole wall → BV-02 → coiled flexible hose → spray bar feed adapter → 3/4" HDPE spray tube → spray holes.

**Operation:**

1. Place the spray bar on the walkway grating at the far end of the tray (Yd≈2,280, film-plane side)
2. Open BV-02 — water flows through the coiled hose to the spray tube
3. Using the telescoping pole, slowly pull the bar toward the pinhole wall (decreasing Yd), flooding the print progressively
4. The bar travels at approximately 50mm/second — full traverse takes ~44 seconds
5. At the near rim (Yd=80), close BV-02. One wash pass complete.
6. For additional wash passes, push the bar back to the far end and repeat
7. Between wash passes, switch to Brown (recycled) water by closing BV-02 and activating P-02 through the filter train

**Storage:** When not in use, the spray bar rests on the walkway grating at either end of its travel, parallel to the tray rim. The flexible hose coils naturally at the near wall. The telescoping pole detaches and stores alongside the bar.

---

## 4. Processing Procedure — Step by Step

### Before each session
1. Check Blue IBC levels — minimum 100 gal required per print session
2. Check IBC-4 (waste) level — must have at least 55 gal headroom before starting
3. Run Brown recycle pump for 2 minutes to verify filter flow and check pH
4. Confirm P-04 suction pickup tube is seated in sump well and suction hose is connected (permanently installed — visual check only)
5. Lay fresh 6-mil black LDPE containment sheet over the tray surface, overlap 50mm over rims
6. Verify all valves in correct position (see valve matrix below)

### Print processing
1. Expose print in camera (no water involved)
2. Transfer print to processing tray in subdued light — lay face-up on containment liner
3. Open BV-02 (Blue supply) → flood print with 16 gal via spray bar — 5 minutes
4. Close BV-02 → switch ON P-04 to pump sump to IBC-3 via 3W-DV-02 (set to Brown) → drain
5. If Brown tank has filtered stock: pump filtered water via spray bar for Wash 2 — 5 minutes → drain to Brown
6. Wash 3: open BV-02 → 16 gal clean Blue water → 5 minutes → drain
7. Inspect print — optional brightener: 0.5% hydrogen peroxide mist, 2 minutes, water rinse
8. Hang print to dry — use internal or external line
9. Allow residual water to collect in sump; run P-04 to pump residual to Brown or Black as appropriate

### Valve matrix

| Valve | Default | Wash 1 | Drain 1→Brown | Wash 2 (recycled) | Drain 2→Brown | Wash 3 | Drain 3 |
|-------|---------|--------|---------------|-------------------|---------------|--------|---------|
| BV-01 (Blue manifold) | Open | Open | Open | Open | Open | Open | Open |
| BV-02 (Blue to floor) | Closed | **Open** | Closed | Closed | Closed | **Open** | Closed |
| BV-06 (Chem tap) | Closed | Closed | Closed | Closed | Closed | Closed | Closed |
| 3W-DV-02 (tray drain) | Brown | Brown | **Brown** | Brown | **Brown** | Brown | **Brown** |
| P-02 (Brown pump) | Off | Off | Off | **On** | Off | Off | Off |
| 3W-DV-01 (filter out) | Blue return | Blue | Blue | Blue | Blue | Blue | Blue |

### Diverter valve operator decisions

The two 3-way diverter valves serve different roles in the water triage chain. Understanding when and why to switch each valve is critical to avoiding cross-contamination of the Blue clean supply.

**3W-DV-02 — Tray drain diverter (operator judgment call)**

DV-02 sits on the P-04 pump discharge and controls whether drain water from the processing tray goes to Brown (IBC-3, for filtering and potential recycling) or Black (IBC-4, waste for external disposal). There is no automated test at this valve — the operator decides based on what happened during the session:

- **Set to Brown (default):** Normal processing rinse water. The water contains only trace amounts of residual cyanotype chemistry (ferric ammonium oxalate and potassium ferricyanide) from the print surface. This water is suitable for filtering and potential recycling back to Blue.
- **Switch to Black:** Heavy contamination events — concentrated chemistry spills, failed sensitizer coating that washes off in bulk, or any situation where the drain water is visibly discolored beyond a pale yellow tint. This water goes directly to IBC-4 for external disposal and never enters the filter/recycle path.

**Rule of thumb:** If the drain water looks like rinse water (clear to pale yellow), send it to Brown. If it looks like chemistry (deep yellow, orange, or green), send it to Black.

**3W-DV-01 — Filter output diverter (pH meter reading)**

DV-01 sits after the filter skid (F1→F2→F3) and the pH test point. After brown water has been filtered, the operator checks the pH reading:

- **Set to Blue return (default):** pH is between 6.5 and 8.0, indicating the filtered water is chemically neutral enough to return to IBC-2 (Blue clean supply) for reuse.
- **Switch to Black:** pH is outside the acceptable range, or the water is visibly discolored after filtering. This water goes to IBC-4 (waste) rather than contaminating the clean supply.

| Valve | Decision | Basis | Who decides |
|-------|----------|-------|-------------|
| 3W-DV-02 (tray drain) | Brown vs Black | Contamination severity at drain time | Operator — visual judgment |
| 3W-DV-01 (filter output) | Blue vs Black | Water quality after filtering | Operator — pH meter reading |

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
| Combo filter outlet → pH test → DV-01 | Sch 40 | 1" nominal (OD 33mm) | 100 PSI min | HDPE |

**IBC fill/drain (1" HDPE Sch 40 — gravity flow, not pump-driven):**

| Circuit | Pipe | Size | Pressure rating | Material |
|---------|------|------|----------------|---------|
| External fill line (X1 bulkhead → IBC-1) | Sch 40 | 1" nominal (OD 33mm) | 50 PSI min | HDPE |
| External drain lines (X3/X4 bulkhead → IBCs) | Sch 40 | 1" nominal (OD 33mm) | 50 PSI min | HDPE |
| IBC-1 ↔ IBC-2 cross-connect | Sch 40 | 2" nominal (OD 60mm) | 50 PSI min | HDPE |

At 3.5 GPM, flow velocity in 1/2" pipe (ID ~15.8mm) is approximately 1.1 m/s — well within the recommended 0.5–2.5 m/s range for water systems. The longest internal run (~5.5m from manifold to far-column IBC) contributes less than 0.3 bar friction loss at this velocity.

**Why HDPE, not PVC?** Standard grey PVC is not rated for photographic chemistry contact and can leach plasticizers. HDPE and CPVC are both acceptable. Do not use copper or galvanized fittings — iron compounds in the wash water will react.

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

See **Sheet 2 — Plan View** (`water-system-sheet2.png`) for the water-system-specific P&ID layout. All four IBCs are in the provably shadow-free **right end zone** (X=4,649–5,893mm), arranged in a 2x2 stack. The optical zone (X=150–4,649mm) contains only the processing tray and perimeter walkways at floor level.

**Container floor plan — all systems (top-down, 1:75):**
![TBS-001 Container Floor Plan — All Systems](assets/container-floorplan.png)

IBCs are arranged in a **2x2 stack** in the right end zone at X=4,674mm, right-justified to the far end wall. Near column (Yd=30–1,046): IBC-1 Blue (top) + IBC-3 Brown (bottom). Far column (Yd=1,316–2,332): IBC-2 Blue (top) + IBC-4 Waste (bottom). A 270mm plumbing corridor between the two columns (Yd=1,046–1,316) carries all internal supply and return lines. Total capacity: 4x600L = 2,400L. All IBCs are loaded empty through the cargo doors and filled/drained remotely via 3x external 2" NPT bulkhead fittings (X1/X3/X4) through the container end wall. IBC wall clearance is 30mm (near wall to near column edge).

| Zone | Contents | X (mm) | Yd (mm) | H (mm) |
|------|----------|--------|---------|--------|
| Right end zone | IBC-1 Blue (top, near column) | 4,674–5,893 | 30–1,046 | 1,010–2,020 |
| Right end zone | IBC-3 Brown (bottom, near column) | 4,674–5,893 | 30–1,046 | 0–1,010 |
| Right end zone | Plumbing corridor | 4,674–5,893 | 1,046–1,316 | 0–2,020 |
| Right end zone | IBC-2 Blue (top, far column) | 4,674–5,893 | 1,316–2,332 | 1,010–2,020 |
| Right end zone | IBC-4 Waste (bottom, far column) | 4,674–5,893 | 1,316–2,332 | 0–1,010 |
| Pinhole wall face | Pump manifold (P-01, P-02, P-04) | 2,400–2,700 | Y=0 | 200–600 |
| IBC plumbing corridor | P-03 waste pump (on X4 drain run) | 4,674–5,893 | 1,046–1,316 | ~200 |
| Optical zone floor | Processing tray (2 panels) | 645–4,629 | 60–2,300 | 0–50 |
| Optical zone | No equipment | 625–4,649 | — | — |

All equipment clears the optical cone at every depth — shadow-free proof in [Equipment Layout Report](equipment-layout-report.md).

**Hose routing:** Pump manifold (P-01, P-02, P-04) is wall-mounted at X=2,400–2,700mm on the pinhole wall (Y=0 face). Supply and return hoses run along the pinhole wall to the right end zone, then through the 270mm central plumbing corridor (Yd=1,046–1,316) between the two IBC columns. Maximum run ~5.5m (manifold to far-column IBCs at Yd=1,316mm). Waste line from 3W-DV-01/3W-DV-02 routes along the pinhole wall through the corridor to IBC-4 in the far column — maximum run ~4m. P-03 (waste evacuation) is mounted in the IBC plumbing corridor directly on the X4 waste drain run, minimizing pipe length from IBC-4 to the external drain port (~700mm vs. ~5,550mm if routed via manifold).

**External fill/drain ports:** Three 2" NPT bulkhead fittings with camlock fittings on the exterior are mounted on the container end wall centerline (Yd=1,181mm), stacked vertically:

| Port | Function | Z (mm) | Connects to |
|------|----------|--------|-------------|
| X1 — Fill Blue | Fresh water supply fill | 2,250 | IBC-1 (top, near column) — gravity feed |
| X3 — Drain Brown | Used water drain | 400 | IBC-3 (bottom, near column) |
| X4 — Drain Waste | Waste water drain | 200 | IBC-4 (bottom, far column) |

A single fill port (X1) feeds IBC-1 directly. IBC-2 self-levels via a permanently open 2" cross-connect pipe between the two Blue IBCs at valve height (~Z=1,195mm), running through the 270mm plumbing corridor. This eliminates the second fill port and simplifies external connections — only one hose is needed for filling.

This allows remote filling (from water bowser or tanker) and draining (IBC-3/IBC-4 to disposal tanker) without opening the cargo doors or entering the container. Internal plumbing from each port routes through the 270mm central corridor between the two IBC columns to reach the respective tote. All ports are accessible from the container exterior.

---

## 8. Parts List and Shopping List

### 8.1 Water storage

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| [IBC tote 600L, food-grade, used/rinsed](https://containerexchanger.com/geo-sale-ads/us-ca/bulk-containers/ibc-totes-for-sale) | HDPE cage tote, DN50 butterfly valve (S60×6 thread), fill cap DN150 | 4 | Container Exchanger | $80–$150 | **$320–$600** |
| [2" NPT bulkhead fitting (304 SS)](https://www.mcmaster.com/4464K115) | External fill/drain port, welded through container wall | 3 | McMaster-Carr | $25–$40 | **$75–$120** |

**Storage subtotal: ~$420–$760**

### 8.2 Pumps and pressure management

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| [Shurflo 2088-554-144 pump](https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C) (P-01, P-02) | 12VDC, 3.5 GPM, 45 PSI, 1/2" NPSM ports | 2 | Amazon | $55–$70 | **$110–$140** |
| [Shurflo 2088-554-144 pump](https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C) (P-03 waste evacuation — *mounted in IBC plumbing corridor on X4 drain run*) | 12VDC, 3.5 GPM, 45 PSI. Empties IBC-4 residual below X4 gravity-drain height (Z=200mm, ~120L) | 1 | Amazon | $55–$70 | **$65** |
| [Shurflo 2088-554-144 pump](https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C) (P-04 tray drain transfer) | 12VDC, 3.5 GPM, 45 PSI. Pumps used chemistry from tray drain to IBC-3 fill cap (~900mm lift) | 1 | Amazon | $55–$70 | **$65** |
| [SeaFlo pressure accumulator](https://www.amazon.com/Seaflo-Accumulator-Control-Internal-Bladder/dp/B01MUYL8F8) | 0.75 L (23.5 oz), 125 PSI, 1/2" MNPT | 1 | Amazon | $25–$45 | **$35** |
| [Shurflo pump mounting bracket](https://www.amazon.com/s?k=shurflo+2088+mounting+bracket+stainless) | Stainless, for 2088 series (3× manifold + 1× IBC corridor for P-03) | 4 | Amazon | $8–$12 | **$40** |

**Pump subtotal: ~$305–$355**

### 8.3 Filter unit

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| [3-stage Big Blue combo filter unit 4.5"×20"](https://www.purcooflow.com/products/whf2045b302-3-stage-kdf-heavy-metal-water-filter) | 1" NPT ports, integrated bracket, triple drain valves. Purcooflow WHF2045B302 or equivalent (iSpring WGB32B, Express Water, etc.) | 1 | Purcooflow / Amazon | $350–$450 | **$350–$450** |
| [MPP 5-micron sediment cartridge 4.5"×20"](https://www.amazon.com/s?k=4.5x20+melt+blown+polypropylene+sediment+filter+5+micron) | Melt-blown polypropylene depth filter (F-1 stage) | 3 + spares | Amazon | $8–$14 each | **$24–$42** |
| [KDF-55 heavy metal cartridge 4.5"×20"](https://www.amazon.com/s?k=4.5x20+KDF+55+heavy+metal+water+filter) | KDF-55 media for dissolved iron/metal removal (F-2 stage) | 2 + spares | Amazon | $30–$50 each | **$60–$100** |
| [CTO carbon block cartridge 4.5"×20"](https://www.amazon.com/s?k=4.5x20+CTO+coconut+shell+carbon+block+filter) | Coconut shell activated carbon block (F-3 stage) | 3 + spares | Amazon | $12–$20 each | **$36–$60** |

**Filter subtotal: ~$470–$652**

### 8.4 Valves and fittings

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| [Banjo V050FP ball valve 1/2" FNPT](https://www.amazon.com/s?k=banjo+1%2F2+inch+ball+valve+polypropylene) | Polypropylene, full-port, quarter-turn. BV-01, BV-02, plus spares | 4 | Amazon | $6–$10 | **$24–$40** |
| [Banjo V100FP ball valve 1" FNPT](https://www.amazon.com/Banjo-V100FP-Polypropylene-Ball-Valve/dp/B003CF2EN0) | Polypropylene, full-port, quarter-turn. V1/V3/V4, VB1–VB3 (IBC fill/drain valves) | 6 | Amazon | $10–$16 | **$60–$96** |
| [Banjo V075FP ball valve 3/4" FNPT](https://www.amazon.com/Banjo-V075FP-Polypropylene-Ball-Valve/dp/B003CF2DXA) | Polypropylene, full-port, quarter-turn. BV-06 (chemistry tap shut-off) | 1 | Amazon | $8–$12 | **$8–$12** |
| [3-way diverter valve 1/2" FNPT](https://www.amazon.com/s?k=1%2F2+inch+3+way+ball+valve+NPT) | L-port or T-port, HDPE compatible. 3W-DV-02 (tray drain) | 1 | Amazon | $12–$22 | **$12–$22** |
| [3-way diverter valve 1" FNPT](https://www.amazon.com/s?k=1+inch+3+way+ball+valve+NPT) | L-port or T-port, HDPE compatible. 3W-DV-01 (filter output — matches 1" filter port) | 1 | Amazon | $18–$30 | **$18–$30** |
| [2" polypropylene camlock pairs (M+F)](https://www.amazon.com/s?k=2+inch+polypropylene+camlock+fitting+pair) | For external bulkhead connections (X1/X3/X4 + spare) | 4 pairs | Amazon | $5–$8/pair | **$20–$32** |
| [1/2" NPT 90° elbow polypropylene](https://www.amazon.com/s?k=1%2F2+NPT+90+elbow+polypropylene) | All pump-driven run bends (manifold internal + external runs) | 14 | Amazon | $2–$4 | **$28–$56** |
| [Banjo LE100 90° elbow 1" NPT](https://www.amazon.com/Banjo-LE100-Polypropylene-90-Degree-Elbow/dp/B003CF2FWI) | Polypropylene street elbow. IBC fill/drain bends, filter outlet to DV-01 | 4 | Amazon | $3–$5 | **$12–$20** |
| [1/2" NPT polypropylene tee](https://www.amazon.com/s?k=1%2F2+NPT+tee+polypropylene) | Blue suction/discharge tees, system branches | 6 | Amazon | $2–$4 | **$12–$24** |
| [Banjo TEE100 equal tee 1" NPT](https://www.amazon.com/Banjo-TEE100-Polypropylene-Pipe-Fitting/dp/B003CF2FI2) | Polypropylene. IBC fill/drain tees | 4 | Amazon | $4–$6 | **$16–$24** |
| [1/2" NPT polypropylene union](https://www.amazon.com/s?k=1%2F2+inch+NPT+polypropylene+union) | For maintenance disconnects on pump runs | 6 | Amazon | $4–$6 | **$24–$36** |
| [1/2"×1" NPT bushing reducer](https://www.amazon.com/s?k=1%2F2+inch+to+1+inch+NPT+bushing+reducer+polypropylene) | P-02 riser to F1 filter inlet (1 required) | 1 | Amazon | $3–$5 | **$3–$5** |
| [S60×6 to 1" NPT adapter](https://www.amazon.com/s?k=IBC+S60x6+1+NPT+adapter) | IBC DN50 butterfly valve to 1" HDPE pipe. Polypropylene, S60×6 coarse thread male × 1" NPT female | 8 | Amazon | $8–$15 | **$64–$120** |
| [1" NPT spring check valve](https://www.amazon.com/s?k=1+inch+NPT+spring+check+valve+PVC) (CV1/CV3/CV4) | Inline non-return valve on each bulkhead line. PVC body, EPDM seal, 1" FNPT × FNPT | 3 | Amazon | $8–$14 | **$24–$42** |
| Thread seal tape (PTFE) | 1/2" wide, 260" roll | 4 | Home Depot | $2 | **$8** |

**Valves & fittings subtotal: ~$414–$660**

### 8.5 Pipe

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| [1/2" SDR-11 HDPE pipe](https://www.ferguson.com) | All pump-driven runs (IBC to manifold, manifold to spray bar, tray drain, DV outputs). Matches pump port size | 4 sticks (80 ft) | Ferguson | $6–$10/stick | **$24–$40** |
| [1" SDR-11 HDPE pipe](https://www.ferguson.com) | Food-safe, blue-stripe, 20 ft stick. Filter outlet to DV-01 and IBC fill/drain lines only | 1 stick (20 ft) | Ferguson | $12–$18/stick | **$12–$18** |
| [2" SDR-11 HDPE pipe](https://www.ferguson.com) | IBC-1 ↔ IBC-2 cross-connect (~300mm needed, remainder spare). 20 ft stick | 1 stick (20 ft) | Ferguson | $18–$28/stick | **$18–$28** |
| [3/4" SDR-11 HDPE pipe](https://www.ferguson.com) | Spray bar run, 20 ft sticks | 2 sticks (40 ft) | Ferguson | $9–$14/stick | **$20–$30** |
| [1/2" ID reinforced braided PVC hose](https://www.amazon.com/s?k=1%2F2+inch+reinforced+braided+PVC+hose+6+ft) | Pump inlet flexible connection, 6 ft per pump | 2 lengths | Amazon | $8–$12/length | **$20** |

**Pipe subtotal: ~$76–$108**

### 8.6 Processing tray

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| [304 SS sheet, 16-ga (1.5mm)](https://www.onlinemetals.com/en/buy/stainless-steel/304-stainless-steel-sheet) | #4 brushed, 4'×8' sheets | 4 | Online Metals | $180–$250/sheet | **$720–$1,000** |
| Fabrication (cut, brake, weld, press sump) | Two tray halves: each 2,229×2,200mm with 50mm rims, pressed sump well (150×100×20mm) in near panel, welded corners | 1 job | Local sheet metal shop | $450–$850 | **$450–$850** |
| [HDPE flat bar 50×10mm](https://www.mcmaster.com/8619K451) | Tapered shim strips for tray slope support, 2,200mm long, 5 required | 5 | McMaster-Carr / TAP Plastics | $8–$15 each | **$40–$75** |
| [1" SS foot valve with strainer](https://www.amazon.com/s?k=1+inch+stainless+foot+valve+strainer) | Suction pickup for sump well, prevents debris and maintains prime | 1 | Amazon | $15–$25 | **$20** |
| [1" reinforced suction hose, 6 ft](https://www.amazon.com/s?k=1+inch+reinforced+suction+hose+6+ft) | P-04 suction line from sump pickup over tray rim to pump manifold (P-04) | 1 | Amazon | $12–$20 | **$15** |
| [Silicone gasket strip, FDA grade](https://www.mcmaster.com/1460N14) | 1/16" × 1" × 10 ft, for center flange seal | 1 roll | McMaster-Carr | $15–$25 | **$20** |
| [M6×16 SS hex bolts + flange nuts](https://www.mcmaster.com/92196A150) | Center flange bolts, 200mm spacing | 24 | McMaster-Carr | $0.50 each | **$12** |

**Processing tray subtotal: ~$1,277–$1,992**

*Fabrication cost varies significantly by region. Get quotes from at least two local shops. For DIY builders with access to a sheet metal brake and TIG welder, material cost alone is $720–$1,000.*

### 8.7 Electrical

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| [12V fuse block (6-way)](https://www.amazon.com/s?k=12V+6+way+blade+fuse+block) | Blade fuse, 10A per channel | 1 | Amazon | $12–$20 | **$15** |
| [14 AWG duplex marine wire](https://www.amazon.com/s?k=14+AWG+duplex+marine+wire+tinned+copper+25+ft) | Tinned copper, 25 ft | 1 roll | Amazon | $18–$28 | **$22** |
| [Anderson Powerpole connectors 30A](https://www.amazon.com/s?k=anderson+powerpole+30A+connector) | For pump connections | 4 pairs | Amazon | $1.50/pair | **$8** |
| [10A blade fuses (pack)](https://www.amazon.com/s?k=10A+standard+blade+fuse+pack) | For pump circuits | 10 | Amazon | $5/pack | **$5** |

**Electrical subtotal: ~$50**

### 8.8 Processing consumables

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| 6-mil black LDPE sheeting | 20 ft × 100 ft roll | 1 | Home Depot | $80–$120 | **$100** |
| [Apera Instruments PH20 pH meter](https://www.amazon.com/Apera-Instruments-Waterproof-Automatic-Calibration/dp/B01LZ5KCNX) | Waterproof, 0–14 range, ±0.1 accuracy | 1 | Amazon | $35–$55 | **$45** |
| [pH calibration solution set](https://www.amazon.com/s?k=pH+calibration+buffer+solution+4+7+sachet) | pH 4 + pH 7 buffer sachets | 1 set | Amazon | $8–$12 | **$10** |
| [Citric acid, food grade, 5 lb](https://www.amazon.com/s?k=citric+acid+food+grade+5+lb) | pH adjustment (acidifier) | 2 bags | Amazon | $12–$18 | **$28** |
| [Chemical-resistant labels (GHS)](https://www.amazon.com/s?k=GHS+chemical+resistant+labels) | For IBC totes | 1 pack | Amazon | $15–$25 | **$20** |
| [Nitrile gloves, box of 100](https://www.amazon.com/s?k=nitrile+gloves+100+pack) | Size M/L | 2 boxes | Amazon | $12–$18 | **$28** |

**Consumables subtotal: ~$231–$278**

### 8.9 Spray bar assembly

| Item | Spec | Qty | Supplier | Unit price | Total |
|------|------|-----|---------|-----------|-------|
| [6061-T6 aluminum SHS 1-1/2"×1-1/2"×1/8"](https://www.onlinemetals.com/en/buy/aluminum/6061-t6-aluminum-square-tube) | 40×40×3mm, 8 ft lengths. Need 2 pieces joined (or 1× 16 ft length if available) for 4,459mm total | 2 | Online Metals / Metal Supermarket | $18–$28/8ft | **$36–$56** |
| [3/4" HDPE SDR-11 pipe](https://www.ferguson.com) | Spray tube, 4,459mm. Already in §8.5 pipe list — no additional purchase needed | — | — | — | **included** |
| [UHMW polyethylene block 100×50×30mm](https://www.mcmaster.com/8702K74) | Runner pads for walkway grating. Machine groove for guide rail | 2 | McMaster-Carr | $8–$12 | **$16–$24** |
| [6061-T6 aluminum angle 1"×1"×1/8"](https://www.onlinemetals.com/en/buy/aluminum/6061-t6-aluminum-angle) | Guide rails, 2,200mm long, bolted to walkway grating | 2 | Online Metals | $10–$16/8ft | **$20–$32** |
| [Telescoping aluminum pool pole](https://www.amazon.com/s?k=telescoping+aluminum+pool+pole+8+ft) | 4–8 ft (1.2–2.4m), standard pool skimmer handle | 1 | Amazon / Home Depot | $12–$20 | **$15** |
| [1/2" reinforced braided PVC hose, 15 ft](https://www.amazon.com/s?k=1%2F2+inch+reinforced+braided+PVC+hose+15+ft) | Flexible connection from BV-02 to spray bar (4m coiled length) | 1 | Amazon | $12–$18 | **$15** |
| [3/4" FNPT × 1/2" barb reducer](https://www.amazon.com/s?k=3%2F4+FNPT+1%2F2+barb+reducer+polypropylene) | Feed adapter at spray tube inlet end | 1 | Amazon | $3–$5 | **$4** |
| [3/4" HDPE threaded end cap](https://www.amazon.com/s?k=3%2F4+HDPE+threaded+end+cap) | Seal spray tube ends | 2 | Amazon | $2–$3 | **$5** |
| [Stainless hose clamps 3/4"](https://www.amazon.com/s?k=3%2F4+stainless+hose+clamp+pack) | Secure spray tube to beam (or nylon zip ties) | 8 | Amazon | $0.50 | **$4** |
| [M6×20 stainless bolts + nylock nuts](https://www.mcmaster.com/92196A150) | Runner pad mounting, guide rail mounting | 12 | McMaster-Carr | $0.40 | **$5** |
| [Stainless spring clip / quick-release](https://www.amazon.com/s?k=pool+pole+tip+clip+stainless) | Pole clip to beam center | 1 | Amazon | $5–$8 | **$6** |

**Spray bar subtotal: ~$126–$166**

---

### 8.10 Total cost summary

| Category | Low estimate | High estimate |
|----------|-------------|--------------|
| Water storage (4x IBC totes + bulkhead fittings) | $420 | $760 |
| Pumps and accumulator (P-01, P-02, P-04 manifold + P-03 IBC corridor) | $305 | $355 |
| Filter unit (3-stage combo + cartridges) | $470 | $652 |
| Valves and fittings (incl. S60×6 adapters, check valves) | $414 | $660 |
| Pipe | $76 | $108 |
| Processing tray (304 SS, fabricated) | $1,177 | $1,857 |
| Spray bar assembly | $126 | $166 |
| Electrical | $50 | $50 |
| Processing consumables | $231 | $278 |
| **TOTAL** | **$3,269** | **$4,886** |

*Used IBC totes drive significant savings vs. new. The parts list consolidates to 4 primary suppliers: **Amazon** (~30 line items — qualifies for bulk/subscribe discounts), **McMaster-Carr** (tray hardware — single order, fast shipping), **Ferguson** (HDPE pipe — call for contractor pricing), and **Online Metals** (SS sheet). Obtain quotes from Ferguson before ordering pipe from Amazon — trade counter pricing is typically 20–30% below retail.*

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
| Inspect IBC-4 valve and cap | Before every transport | Check for leaks |

---

## 10. Safety Notes

1. **Ferricyanide in alkaline conditions:** Do not allow IBC-4 waste water to contact strong alkalis (sodium hydroxide, bleach). In alkaline + UV conditions, ferricyanide can release trace cyanide ions. Keep pH < 7.5 in all containers. This is a theoretical rather than acute risk at the concentrations involved, but is worth managing.

2. **Prussian blue is non-toxic** — it is approved as a human antidote medication in some contexts — but the fine particles are a skin/eye irritant. Wear nitrile gloves and eye protection when handling wash trays.

3. **Citric acid dosing:** Always dissolve before adding to tank. Adding dry acid to iron-rich water can cause a brief exothermic reaction and bubbling. Mix in a separate container first.

4. **IBC-4 waste transport:** Ensure IBC cap is sealed and ball valve is closed before transport. Label contents before transport. The liquid is not classified as DOT hazardous material at these concentrations, but label clearly and keep upright. Drain remotely via external bulkhead port to a disposal tanker.

5. **Electrical:** Both pumps draw 7.5A each at 12V. The fuse block must be rated to handle simultaneous operation. Do not run pumps from the same fused circuit.

---

## 11. Schematic Diagrams

| Drawing | File |
|---------|------|
| Sheet 1 — System flow schematic (P&ID) | `water-system-sheet1.png` |
| Sheet 2 — Equipment layout plan + parts list | `water-system-sheet2.png` |
| Sheet 3 — Processing tray drainage plan | `water-system-sheet3.png` |
| Sheet 4 — Drain cross-section elevation (fitting detail + flow path) | `water-system-sheet4.png` |
| Filter skid — plumbing elevation detail | `filter-skid-sheet1.png` |
| Container floor plan — all systems | See [Electrical & Systems Report](electrical-report.md) Section 5.8 |

**Sheet 1 — System Flow Schematic (P&ID)**
![Water System — Sheet 1: P&ID Flow Schematic](assets/water-system-sheet1.png)

---

**Sheet 2 — Equipment Layout Plan**
![Water System — Sheet 2: Equipment Layout](assets/water-system-sheet2.png)

---

**Sheet 3 — Processing Tray Drainage Plan**
![Water System — Sheet 3: Drainage Plan](assets/water-system-sheet3.png)

---

**Sheet 4 — Processing Tray Drain Cross-Section Elevation**
![Water System — Sheet 4: Drain Cross-Section](assets/water-system-sheet4.png)

---

**Filter Skid — Plumbing Elevation Detail (1:5)**
![Filter Skid — Plumbing Elevation](assets/filter-skid-sheet1.png)

---

## 12. Sources and References

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
