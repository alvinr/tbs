<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Plumbing Report

> **Two plumbing panels.** The water-handling equipment is split across two panels: the
> **Corridor Plumbing Panel** (pumps P-01/P-03/P-04/P-05, accumulator ACC-01, diverter DV-02,
> sample tap SV-02, pump-suction isolation valves — mounted in the IBC plumbing corridor) and the
> **Pinhole Wall Plumbing Panel** (the wet-end filter loop: pump P-02, the 3-stage Big Blue filter,
> diverter DV-01, sample tap SV-01 — mounted on the pinhole wall). This report covers both.

## Interactive 3D model

<div class="sketchfab-embed-wrapper" style="position:relative;width:100%;padding-bottom:56.25%;height:0;overflow:hidden;margin-bottom:1em;">
    <iframe title="TBS-001 Water System Model" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/1dae932430924e9b993e153a16f485fc/embed" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>
</div>
<p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"><a href="https://sketchfab.com/3d-models/1dae932430924e9b993e153a16f485fc" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">TBS-001 Water System Model</a> by <a href="https://sketchfab.com/alvin91403" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">alvin91403</a> on <a href="https://sketchfab.com" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>

## 1. Purpose

The water-handling equipment mounts on **two plumbing panels**:

- The **Corridor Plumbing Panel** — an 18mm marine plywood board mounted vertically at the
  front (cargo-door-facing) mouth of the IBC plumbing corridor on the front-portal frame
  (270mm corridor width × 2,060mm tall). It carries the waste/recycle pumps
  (P-01, P-03, P-04, P-05), the pressure accumulator (ACC-01), the Stage-A diverter (DV-02),
  the pH sample tap (SV-02), and the pump-suction isolation valves.
- The **Pinhole Wall Plumbing Panel** — the wet-end filter loop mounted on the pinhole wall:
  pump P-02, the 3-stage Big Blue filter (F1/F2/F3), the filter-output diverter (DV-01), and the
  pH sample tap (SV-01).

Each panel concentrates its part of the system in one accessible location. The panels serve
three functions:

1. **Structural mounting surface** — provides a rigid, flat substrate for
   equipment that would otherwise require individual mounting brackets on the
   corrugated container walls.
2. **Plumbing coordination** — all pump suction and discharge lines, filter
   connections, and valve positions are organized on one face, minimizing pipe
   runs and simplifying maintenance.
3. **Accessibility** — the panel faces the open end of the container (-X
   direction). The operator approaches from the right walkway
   and reaches into the 270mm corridor to access valves and pump switches.

---

## 2. Panel Specifications

| Parameter | Value |
|-----------|-------|
| Material | 18mm marine plywood (BS 1088 or equivalent) |
| Face dimensions | 270mm wide (Yd) × 2,060mm tall (Z) |
| Orientation | Vertical, perpendicular to sealed end wall |
| Bottom edge Z | 250mm (120mm above walkway deck) |
| Top edge Z | 2,310mm (78mm below ceiling of 2,388mm) |
| Corridor width | 270mm (between near and far IBC columns) |
| Mounting | L-brackets to the front-portal frame uprights, 4 points |
| Finish | Sealed with marine varnish or epoxy; white face for visibility |

The table above is the **Corridor Plumbing Panel**. The **Pinhole Wall Plumbing Panel** is the
wet-end board mounted on the pinhole wall (Yd0) carrying the 3-stage filter skid, its feed pump
P-02, the filter-output diverter DV-01, and the SV-01 sample tap — see [Water System Report](water-system-report.md)
§3 for its location and the spray-bar/chemistry-tap supply it feeds.

---

## 3. Equipment Layout

Equipment is split across the two panels. The **Pinhole Wall Plumbing Panel** carries the
3-stage filter skid and its feed pump P-02 (§3.1); the **Corridor Plumbing Panel** carries the
four corridor pumps (P-01/P-03/P-04/P-05) and the accumulator (§3.2–§3.3).

**Plumbing Panel Layout — Front elevation with pump zone, filter skid, valves, and full plumbing routing**
![TBS-001 — Plumbing Panel Layout](assets/panel-layout.png)

**Backside (corridor side section) — what is mounted on the *back* of the panel:**
the drain-riser backing spine (18mm ply teed off the panel, with a lowered top
and a capped shelf), the X3/X4 drain risers running from the P-05/P-03 discharges
down to the sealed end-wall ports, and the Blue fill trunk resting on the shelf.
Pumps mount on the front face; the drain/fill runs are on the back, in the
corridor gap clear of both tote columns.

![TBS-001 — Plumbing Panel Backside](assets/panel-layout-back.png)

### 3.1 Pinhole Wall Plumbing Panel — Filter Skid + P-02

Three 4.5"×10" Big Blue filter housings mounted vertically (sump down) in a
slotted angle frame. The housings stack vertically with 30mm gaps between them.
Flow path: P-02 output → F-01 (top, coarsest) → F-02 (middle) → F-03 (bottom,
finest) → SV-01 sample tap → 3W-DV-01.

| Component | Position (Z, mm) | Specification |
|-----------|-----------------|---------------|
| F-01 (sediment) | 940–1,280 | 4.5"×10" Big Blue, 50μm MPP melt-blown polypropylene |
| F-02 (heavy metal) | 570–910 | 4.5"×10" Big Blue, KDF-55 heavy metal removal |
| F-03 (carbon) | 200–540 | 4.5"×10" Big Blue, CTO coconut shell activated carbon |
| Slotted angle frame | 200–1,280 | 25×25×3mm slotted steel angle, 130mm wide |

Each housing has 1" NPT inlet and outlet ports on the head (top). Inter-housing
piping connects F-01 OUT → F-02 IN and F-02 OUT → F-03 IN using 1" HDPE pipe
with 90° elbows routed outside the housing bodies. Housings mount to an 18mm
plywood backing board within the slotted angle frame via U-bracket clamps with
25mm HDPE spacer blocks for sump-bowl clearance.

**Replacement interval:**

| Stage | Cartridge | Removes | Replace every |
|-------|-----------|---------|--------------|
| F-01 | 5μm MPP sediment | Gross sediment, fiber lint, Prussian blue particles | 25 prints |
| F-02 | KDF-55 | Dissolved iron from ferricyanide wash water | 30 prints |
| F-03 | CTO carbon block | Residual organics, color | 20 prints |

**Alternative:** A single 3-stage combo unit (e.g. Purcooflow WHF2045B302 or
iSpring WGB32B) with 4.5"×20" cartridges eliminates inter-housing plumbing and
the separate frame. The combo unit mounts directly to the panel with its
integrated bracket. 1" NPT inlet/outlet; a single 1/2"→1" bushing reducer
connects P-02 output to the unit inlet. See
[Water System Report](water-system-report.md) §3.2 for sizing rationale.

### 3.2 Corridor Plumbing Panel — Pump Zone

**Four** Shurflo 2088 pumps mount on the Corridor panel (P-02 lives on the Pinhole Wall
panel with the filter loop, §3.1). The accumulator ACC-01 sits at the column foot (§3.3).

| Pump | Circuit | Function |
|------|---------|----------|
| P-01 | Blue | Clean water supply to spray bar (via ACC-01) |
| P-04 | Brown/Black | Tray drain transfer (sump → IBC-3 or IBC-4) |
| P-03 | Black | Waste evacuation (IBC-4 residual → external drain X4) |
| P-05 | Brown | Brown drain-out (IBC-3 → external drain X3) |

All pumps are identical Shurflo 2088-554-144 units: 12VDC, 3.5 GPM, 45 PSI,
self-priming diaphragm. Vertical mount, ports at the head, 127mm body width ×
218mm body height × ~114mm protrusion. Each mounts on a stainless 4-bolt bracket
through the plywood. They sit in a single vertical column in the 270mm corridor;
P-01 and P-04 draw from the near IBC column, P-03 and P-05 from the far column.

#### Pump electrical — Circuit C (one at a time)

All five pumps run from the **single Circuit C feed** (12V DC, 15A fuse, 14 AWG
from the Blue Sea fuse block — see [Electrical Report §7.2–7.3](electrical-report.md)).
At the panel the feed lands on a **12V DC distribution block** (positive + shared
negative bus) at the top of the pump zone; from it, **five individual IP-rated rocker
switches — one per pump** — fan out, each feeding its pump on a short 16 AWG branch.

| Item | Spec |
|------|------|
| Feed | Circuit C, 14 AWG, 15A fuse (one feed for all five pumps) |
| Distribution | 12V DC + / − bus block at the pump-zone top |
| Switches | 5 × IP-rated sealed rocker (12V, 16A), panel-face-mounted by each pump for corridor access |
| Branches | 16 AWG, ~0.5–1m, switch → pump + (7.5A / 90W per pump) |

The pumps are operated **one at a time**: the operator enables the pump for the
current task at its switch (others off), opens the relevant ball valves, and the
Shurflo's **internal demand/pressure switch** then runs the pump on demand. The 15A
fuse covers a single pump with margin; simultaneous running is not intended.
Switches and the distribution block sit **above the spill line**, IP-rated and sealed,
with drip loops, per the wet-zone rules in [Electrical Report §7.5](electrical-report.md).

### 3.3 Accumulator

| Parameter | Value |
|-----------|-------|
| Model | SeaFlo SFAT-075-125-01, 0.75L (23.5 oz) |
| Dimensions | 127mm OD × 200mm length |
| Position | Corridor panel, at the column **foot** (below P-01 — the P-01/ACC order was swapped to drop the accumulator to the base) |
| Port | 1/2" NPT, bottom |
| Function | Smooths P-01 pump cycling, maintains pressure when the pump is off |

ACC-01 sits inline on the Blue discharge path between the P-01 outlet and the spray-bar supply trunk (BV-05).
The accumulator's air bladder absorbs pressure pulsations from the diaphragm
pump, providing steady flow to the spray bar.

---

## 4. Valves

### 4.1 Ball Valves (Isolation)

| Valve | Size | Panel | Function |
|-------|------|-------|----------|
| BV-01 | 1/2" | Corridor | P-01 (Blue supply) suction isolation |
| BV-02 | 1/2" | Corridor | P-05 (Brown drain) suction isolation |
| BV-03 | 1/2" | Pinhole Wall | P-02 (filter loop) suction isolation |
| BV-04 | 1/2" | supply | TAP-01 chemistry-tap isolation |
| BV-05 | 1/2" | supply | Spray-bar feed isolation |
| BV-06 | 1/2" | Corridor | P-03 (waste evacuation) suction isolation |

BV-01/BV-02/BV-06 are the Corridor panel pump-suction isolation valves; BV-03 the
Pinhole Wall panel's. **BV-05** is the primary operator-controlled valve — on the
spray-bar feed, opened during wash passes; **BV-04** isolates the TAP-01 chemistry
tap. All six are 1/2" Banjo V050FP quarter-turn ball valves.

### 4.2 Diverter Valves (3-Way)

| Valve | Size | Position | Function |
|-------|------|----------|----------|
| 3W-DV-01 | 1" FNPT | After filter skid + SV-01 sample tap | Routes filtered Brown water to Blue (IBC-2) or Black (IBC-4) based on the SV-01 pH reading |
| 3W-DV-02 | 1/2" FNPT | P-04 discharge | Routes tray drain water to Brown (IBC-3) or Black (IBC-4) based on operator judgment |

**3W-DV-02** is the operator judgment valve: set to Brown (default) for normal
rinse water, switch to Black for heavy contamination events.

**3W-DV-01** is the pH-gated valve: draw a sample at **SV-01** (below) and meter it — if filtered water reads pH 6–7, route to
Blue (IBC-2) for recycling; if pH >7.5 or discolored, route to Black (IBC-4).

### 4.3 Check Valves

| Valve | Size | Position | Function |
|-------|------|----------|----------|
| CV-1 | 1" NPT | X1 bulkhead fill line | Prevents backflow from the Blue totes to the external fill port |

**Only CV-1 remains.** The Shurflo 2088 pumps have integral check valves, so the
previously-specified CV-2/CV-3/CV-4 on the pump-driven return/drain lines are
redundant and were dropped — CV-1 guards the single gravity (non-pumped) path, the
X1 fresh-fill. Installed in the IBC zone, not on a panel.

### 4.4 Sample Tap (SV-01)

| Valve | Size | Panel | Function |
|-------|------|-------|----------|
| SV-01 | 1/2" | Pinhole Wall | Filtered-Brown line (F-03 outlet → 3W-DV-01) — pH sample before the Blue/Black diversion |
| SV-02 | 1/2" | Corridor | P-04 tray-drain discharge (→ 3W-DV-02) — pH sample before the Brown/Black diversion |

The filter output has no usable sampling point without SV-01 — a capped tee
cannot be drawn from. **SV-01** is a 1/2" PP quarter-turn ball valve (same Banjo
family as the BV isolation valves) on a 1"×1/2" reducing branch tee, with a short
downturned hose-barb spout. It sits on the panel face **above the spill line**,
spout pointing toward the operator (−X) so a cup fits beneath it from the right
walkway.

**Use:** run P-02 to pressurize the filtered line, crack SV-01 to catch ~50 ml in
a cup, close it, read pH on the meter, then set 3W-DV-01 to Blue-return (pH 6–7)
or Black-waste (pH drift / discolored).

---

## 5. Pipe Specifications

| Run | Schedule | Nominal Size | OD (mm) | Material | Notes |
|-----|----------|-------------|---------|----------|-------|
| Pump suction/discharge | Sch 40 | 1/2" | 21 | HDPE | Matches Shurflo 2088 port thread |
| DV-02 outputs | Sch 40 | 1/2" | 21 | HDPE | To IBC-3 or IBC-4 |
| DV-01 outputs | Sch 40 | 1/2" | 21 | HDPE | To Blue IBC-2 or Black IBC-4 |
| Filter inter-stage | Sch 40 | 1" | 33 | HDPE | Matches Big Blue 1" NPT ports |
| Filter outlet → DV-01 | Sch 40 | 1" | 33 | HDPE | Gravity flow, lower restriction |
| IBC fill/drain (internal) | Sch 40 | 1" | 33 | HDPE | IBC valve to corridor |
| IBC fill/drain (external bulkhead) | Sch 40 | 2" | — | Steel/brass | Bulkhead unions with camlock |
| Spray bar flex hose | — | 1/2" | — | Reinforced braided PVC | ~4m coiled, BV-02 to beam center feed |

All pump-driven internal runs use 1/2" pipe, matching the Shurflo 2088 pump
ports (1/2"-14 male parallel thread). This eliminates reducer fittings at pump
connections. The only reducer is a single 1/2"→1" bushing at the filter skid
inlet (P-02 output to F-01 input).

---

## 6. Flow Paths

### 6.1 Blue System — Clean Water Supply

```
IBC-1/IBC-2 → BV-01 → P-01 → ACC-01 → BV-05 → spray bar
```

P-01 draws from the Blue IBC manifold (two IBCs plumbed in parallel via 1"
HDPE with isolation valves), pressurizes through ACC-01 (0.75L accumulator),
and delivers to BV-05 on the spray-bar feed. A 4m flexible hose connects BV-05
to the spray bar center feed bulkhead.

### 6.2 Brown System — Used Water Recycling

```
Tray sump → P-04 → 3W-DV-02 → IBC-3
IBC-3 → P-02 → 1/2"→1" reducer → F-01 → F-02 → F-03 → SV-01 sample tap → 3W-DV-01
  → IBC-2 (if pH 6–7) or IBC-4 (if pH drift)
```

P-04 lifts drain water from the processing tray sump (~900mm head) to IBC-3.
P-02 recirculates IBC-3 water through the 3-stage filter train. After filtering,
the operator draws a sample at SV-01, checks pH, and sets 3W-DV-01 to route either back to Blue (IBC-2)
or to Waste (IBC-4).

### 6.3 Black System — Waste Containment

```
3W-DV-01 reject → IBC-4
3W-DV-02 contaminated → IBC-4
IBC-4 → P-03 → external drain port X4 (gravity + pump assist)
```

P-03 is dedicated to waste evacuation. IBC-4 gravity-drains through external
port X4 down to approximately 120L residual; P-03 pumps the residual
below the gravity drain height to a disposal tanker.

---

## 7. Mounting and Structure

### 7.1 Plumbing Panel Mounting

The plywood panel is secured to the IBC restraint front-portal frame uprights
(at the corridor mouth) at four points using L-brackets with M10 bolts.
The frame provides rigid lateral restraint — the panel does not contact the
container walls directly.

### 7.2 Filter Skid Frame

The filter skid uses a separate 25×25×3mm slotted steel angle frame bolted to the
plywood panel. The frame provides:

- Adjustable housing height via slotted holes in the uprights
- Rigid support for the ~5kg weight of each filled filter housing
- Backing board (18mm plywood) within the frame for U-bracket attachment

Each filter housing mounts via a steel U-bracket that wraps around the head
section. HDPE spacer blocks (25mm) between the bracket and backing board provide
clearance for the sump bowl to hang freely below. Two bolts per bracket
through the backing board.

### 7.3 Pump Mounting

Each Shurflo 2088 mounts on a stainless steel 4-bolt bracket (Shurflo OEM
accessory). The bracket screws through the plywood panel. Pump body orientation
is vertical (long axis along Z) with ports at the head (top), facing left and
right (along Yd). This orientation minimizes the footprint on the 270mm-wide
panel and allows gravity to assist with priming.

### 7.4 Panel Protrusion Envelope

| Component | Protrusion from panel face (-X) |
|-----------|-------------------------------|
| Pump body (Shurflo 2088) | 100mm |
| Filter housing (Big Blue 4.5"×10") | 130mm |
| Accumulator (ACC-01) | 127mm |
| Pipe fittings + valves | ~50mm |

The maximum protrusion is 130mm (filter housings). Combined with the 18mm panel
thickness, the total X footprint is 148mm. There is a 653mm clear between the walkway and the nearest protruding
component.

---

## 8. Pipe Routing Conventions

All piping on the plumbing panel follows the parallel-wall drawing convention
used throughout TBS-001 engineering diagrams:

- **Blue pipes** — front layer (closest to viewer/operator)
- **Brown pipes** — middle layer
- **Black/waste pipes** — rear layer (closest to panel)

Pipe crossings use the gap-break method (rear pipe broken at crossing) for pipes
of different system colors, and the bridge-arc method for same-color crossings.

Pipes enter and exit the panel zone at the left and right panel edges:
- **Left edge** (near wall side) — Blue IBC suction, Blue discharge
  riser to pinhole wall
- **Right edge** (far wall side) — Brown/Waste IBC connections,
  external drain routing

---

## 9. Parts List

The panel-mounted equipment for each plumbing panel is listed below — generated from the parts
registry (firm low–high bands, April-2026 indicative basis). The **full** water-system BOM (pipe,
fittings, IBC totes, external bulkhead ports, wiring, consumables) is in the
[Water System Report](water-system-report.md) §Parts-List; the panel ply/backing and mounting
hardware are sourced there and in the IBC stacking frame line.

> **Ball valves (BV-0x) pending:** the pump-suction and supply isolation valves are not yet split
> per panel — that inventory is being reconciled against the as-built model. They appear in the
> Water System Report's valve line for now.

### 9.1 Corridor Plumbing Panel

<!-- BEGIN parts:corridor-plumbing-panel -->
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [Shurflo 2088-554-144 pump (P-01 Blue supply)](https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C) | 12VDC, 3.5 GPM, 45 PSI, 1/2" NPSM ports | 1 ea | Amazon | $55–$70 |
| Shurflo 2088-554-144 pump (P-03 waste evacuation) | 12VDC, 3.5 GPM, 45 PSI; empties IBC-4 residual below X4 (~120L) | 1 ea | Amazon | $65 |
| Shurflo 2088-554-144 pump (P-04 tray drain transfer) | 12VDC, 3.5 GPM, 45 PSI; tray drain to IBC-3 (~900mm lift) | 1 ea | Amazon | $65 |
| Shurflo 2088-554-144 pump (P-05 Brown drain) | 12VDC, 3.5 GPM, 45 PSI; evacuates IBC-3 (Brown) residual to the X3 end-wall port | 1 ea | Amazon | $65 |
| [SeaFlo accumulator (0.75 L)](https://www.amazon.com/Seaflo-Accumulator-Control-Internal-Bladder/dp/B01MUYL8F8) (SFAT-075-125-01) | 0.75 L, 125 PSI, 1/2" MNPT | 1 ea | Amazon | $35 |
| Banjo V050FP ball valve 1/2" FNPT | PP full-port quarter-turn; pump-suction isolation BV-01 (P-01), BV-02 (P-05), BV-06 (P-03) | 3 ea | Amazon | $18–$30 |
| 3-way diverter valve 1/2" FNPT | L/T-port HDPE-compatible; 3W-DV-02 (tray drain) | 1 ea | Amazon | $12–$22 |
| pH sample tap (SV-02) — 1/2" PP ball valve + barb spout + branch tee | pH sample on the P-04 tray-drain discharge, before 3W-DV-02; same build as SV-01 | 1 ea | Amazon | $10–$18 |
| **Corridor Plumbing Panel total** | | | | **$325–$370** |
<!-- END parts:corridor-plumbing-panel -->

### 9.2 Pinhole Wall Plumbing Panel

<!-- BEGIN parts:pinhole-wall-plumbing-panel -->
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [Shurflo 2088-554-144 pump (P-02 filter loop)](https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C) | 12VDC, 3.5 GPM, 45 PSI, 1/2" NPSM ports | 1 ea | Amazon | $55–$70 |
| Big Blue filter housing (4.5"×10") | Ø184×333mm/housing, 1" NPT ports, integrated bracket (Express Water / Geekpure / iSpring) | 1 ea | Amazon | $200–$300 |
| MPP 5-micron sediment cartridge 4.5"×10" | Melt-blown polypropylene depth filter (F-1 stage) | 3 ea | Amazon | $18–$30 |
| KDF-55 heavy-metal cartridge 4.5"×10" | KDF-55 media for dissolved iron/metal removal (F-2 stage) | 2 ea | Amazon | $40–$70 |
| CTO carbon block cartridge 4.5"×10" | Coconut shell activated carbon block (F-3 stage) | 3 ea | Amazon | $24–$45 |
| Banjo V050FP ball valve 1/2" FNPT | PP full-port quarter-turn; pump-suction isolation BV-03 (P-02) | 1 ea | Amazon | $6–$10 |
| 3-way diverter valve 1" FNPT | L/T-port; 3W-DV-01 (filter output) | 1 ea | Amazon | $18–$30 |
| pH sample tap (SV-01) — 1/2" PP ball valve + barb spout + branch tee | Filtered-water sample draw before 3W-DV-01; Banjo V050FP 1/2" PP ball valve + downturned 1/2" hose barb on a 1"×1/2" reducing branch tee, panel face above spill line | 1 ea | Amazon | $10–$18 |
| **Pinhole Wall Plumbing Panel total** | | | | **$371–$573** |
<!-- END parts:pinhole-wall-plumbing-panel -->

---

## 10. Maintenance

| Interval | Task |
|----------|------|
| Before each session | Verify all valve positions per valve matrix (see [Water System Report](water-system-report.md) §4) |
| Before each session | Run P-02 for 2 minutes to verify filter flow; draw a sample at SV-01 and check pH of filtered output |
| Before each session | Confirm P-04 suction pickup tube seated in sump well (visual check) |
| After each session | Run P-04 to evacuate residual tray water to Brown or Black as appropriate |
| Monthly | Inspect all pipe joints for leaks; tighten compression fittings if needed |
| Monthly | Check pump mounting bracket bolts for tightness |
| Monthly | Inspect filter housing clamp bands and U-bracket bolts |
| Every 20 prints | Replace F-03 (CTO carbon block) cartridge |
| Every 25 prints | Replace F-01 (5μm sediment) cartridge |
| Every 30 prints | Replace F-02 (KDF-55) cartridge |
| Quarterly | Check accumulator pre-charge pressure (should hold 30 PSI) |
| Quarterly | Inspect check valves CV-1/CV-3/CV-4 for proper seating |
| Annually | Inspect plywood panel for delamination or moisture damage; reseal if needed |

**Filter replacement procedure:** Close P-02 supply valve. Place bucket under
housing. Turn sump bowl counter-clockwise with Big Blue wrench (included with
housing). Remove spent cartridge, inspect housing interior, insert new
cartridge, re-seat sump bowl, hand-tighten plus 1/4 turn. Run P-02 for 1
minute to flush; check for leaks.

---

## 11. Source References

1. [Shurflo 2088-554-144 datasheet](https://www.shurflo.com/products/2088-series) — 12VDC diaphragm pump, 3.5 GPM, 45 PSI,
   self-priming. 127mm × 218mm × 100mm body dimensions, 1/2"-14 NPSM ports.
2. [Pentek Big Blue 4.5"×10" housing specifications](https://www.pentair.com/en-us/water-treatment-components/filter-housings/big_blue_heavy_duty_series.html) — 1" NPT inlet/outlet,
   130mm OD, 340mm total height, polypropylene head.
3. [SeaFlo accumulator specifications](https://www.seaflo.com/products/accumulator-tank) — 0.75L capacity, 125 PSI max, 1/2" NPT
   port, 127mm OD × 200mm length.
4. [Purcooflow WHF2045B302](https://www.purcooflow.com/products/whf2045b302-3-stage-kdf-heavy-metal-water-filter) — 3-stage whole-house filter, 4.5"×20" Big Blue
   cartridges, 1" NPT inlet/outlet, integrated mounting bracket.
5. [Water System Report](water-system-report.md) — Flow circuits, valve matrix,
   processing procedure, pipe specifications.
6. [Equipment Layout Report](equipment-layout-report.md) — Component positions,
   IBC corridor dimensions, line-of-sight clearance.
7. [IBC Stacking Report](ibc-stacking-report.md) — IBC arrangement, stacking
   frame, external bulkhead ports, internal pipe routing.
8. [Processing Tray & Spray Bar Report](processing-tray-and-spray-bar.md) —
   Tray sump, P-04 suction pickup, spray bar connection to BV-02.

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
