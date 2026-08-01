<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Plumbing Report

> **Two plumbing panels.** The water-handling equipment is split across two panels: the
> **Corridor Plumbing Panel** (pumps P-01/P-03/P-04/P-05, accumulator ACC-01, diverter DV-02,
> sample tap SV-02, pump-suction isolation valves — mounted in the IBC plumbing corridor) and the
> **Pinhole Wall Plumbing Panel** (the wet-end filter loop: pump P-02, the 3-stage Big Blue filter,
> diverter DV-01, sample tap SV-01 — mounted on the pinhole wall). This report covers both.

<!-- brochure:skip -->
## Interactive 3D model

<div class="sketchfab-embed-wrapper" style="position:relative;width:100%;padding-bottom:56.25%;height:0;overflow:hidden;margin-bottom:1em;">
    <iframe title="TBS-001 Water System Model" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/1dae932430924e9b993e153a16f485fc/embed" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>
</div>
<p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"><a href="https://sketchfab.com/3d-models/1dae932430924e9b993e153a16f485fc" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">TBS-001 Water System Model</a> by <a href="https://sketchfab.com/alvin91403" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">alvin91403</a> on <a href="https://sketchfab.com" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>
<!-- brochure:endskip -->

## 1. Purpose

The water-handling equipment mounts on **two plumbing panels**:

- The **Corridor Plumbing Panel** — an 18mm marine plywood board mounted vertically at the
  front (cargo-door-facing) mouth of the IBC plumbing corridor on the front-portal frame
  (<!-- BEGIN fact:corridor_width_mm -->270<!-- END fact:corridor_width_mm -->mm corridor width × 2,060mm tall). It carries the waste/recycle pumps
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
3. **Accessibility** — the panel faces the open end of the container. The operator approaches from the right walkway
   and reaches into the <!-- BEGIN fact:corridor_width_mm -->270<!-- END fact:corridor_width_mm -->mm corridor to access the valves (the pumps are switched at the EP — §3.2).

---

## 2. Panel Specifications

| Parameter | Value |
|-----------|-------|
| Material | 18mm marine plywood (BS 1088 or equivalent) |
| Face dimensions | 270mm wide (Yd) × 2,060mm tall (Z) |
| Orientation | Vertical, perpendicular to sealed end wall |
| Bottom edge | Just above the walkway deck (clear of the spill line) |
| Top edge | Just below the container ceiling |
| Corridor width | 270mm (between near and far IBC columns) |
| Mounting | L-brackets to the front-portal frame uprights, 4 points |
| Finish | Sealed with marine varnish or epoxy; white face for visibility |

The table above is the **Corridor Plumbing Panel**. The **Pinhole Wall Plumbing Panel** is the
wet-end board mounted on the pinhole wall carrying the 3-stage filter skid, its feed pump
P-02, the filter-output diverter DV-01, and the SV-01 sample tap — see [Water System Report](water-system-report.md)
§3 for its location and the spray-bar/chemistry-tap supply it feeds.

---

## 3. Equipment Layout

The **Pinhole Wall Plumbing Panel** carries the
3-stage filter skid and its feed pump P-02 (§3.1); the **Corridor Plumbing Panel** carries the
four corridor pumps (P-01/P-03/P-04/P-05) and the accumulator (§3.2–§3.3). Each panel has its
own front-elevation drawing; the corridor backside (drain-riser spine + Circuit-C power) is a
third sheet.

### 3.1 Pinhole Wall Plumbing Panel — Filter Skid + P-02

Three 4.5"×20" Big Blue filter housings in a **horizontal bank mounted high on
the pinhole wall** — the heads (with the 1" NPT ports) pinned just below the
ceiling, the sump bowls hanging below — so the walkway stays clear and the
operator reaches up to service them. Flow path: P-02 output → F-01 (5μm sediment)
→ F-02 (KDF-55) → F-03 (carbon) → SV-01 sample tap → 3W-DV-01.

**Pinhole Wall Plumbing Panel — Front elevation: P-02, 3-stage filter bank, SV-01 sample tap, and DV-01 diverter**
![TBS-001 — Pinhole Wall Plumbing Panel Layout](assets/pinhole-panel.png)

| Stage | Media | Housing |
|-------|-------|---------|
| F-01 (sediment) | 5μm MPP melt-blown polypropylene | 4.5"×20" Big Blue |
| F-02 (heavy metal) | KDF-55 heavy-metal removal | 4.5"×20" Big Blue |
| F-03 (carbon) | CTO coconut-shell activated carbon | 4.5"×20" Big Blue |

Each housing has 1" NPT inlet and outlet on the head; the heads sit on a common
line and the sumps hang below on a shared 25×25×3mm slotted-angle backing frame.
Inter-housing piping connects F-01 OUT → F-02 IN and F-02 OUT → F-03 IN using
1" PVC pipe (threaded at the filter ports) with 90° elbows routed outside the housing
bodies. Each housing lag-screws through its own mounting-hole ears (on 25mm plywood-offcut standoff blocks) into
the 18mm ply backing, giving sump-bowl clearance — no custom bracket (see the
**DETAIL — HOUSING MOUNT (section)** inset on the panel elevation above).

**Head clearance:** the 20" sumps hang ~250mm lower than a 10" housing would —
to roughly shoulder height for the 1.75m scale operator — in exchange for ~2× the
interval between cartridge changes. If the lower bank proves an operational
nuisance, the housings swap directly to 4.5"×10" (same heads and ports, shorter
sumps, half the interval).

**Replacement interval** (4.5"×20" cartridges — roughly 2× the 10" life):

| Stage | Cartridge | Removes | Replace every |
|-------|-----------|---------|--------------|
| F-01 | 5μm MPP sediment | Gross sediment, fiber lint, Prussian blue particles | ~50 prints |
| F-02 | KDF-55 | Dissolved iron from ferricyanide wash water | ~60 prints |
| F-03 | CTO carbon block | Residual organics, color | ~40 prints |

**Alternative:** A single 3-stage combo unit (e.g. Purcooflow WHF2045B302 or
iSpring WGB32B) with 4.5"×20" cartridges eliminates the inter-housing plumbing
and the separate frame — one integrated bracket, 1" NPT inlet/outlet, a single
1/2"→1" bushing at the P-02 feed. See
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
216mm body height × ~114mm protrusion. Each mounts on a stainless 4-bolt bracket
through the plywood. They sit in a single vertical column in the <!-- BEGIN fact:corridor_width_mm -->270<!-- END fact:corridor_width_mm -->mm corridor;
P-01 and P-04 draw from the near IBC column, P-03 and P-05 from the far column.

#### Pump electrical — Circuit C (one at a time)

All five pumps run from the **single Circuit C feed** (12V DC, 15A fuse, 14 AWG
from the Blue Sea fuse block — see [Electrical Report §7.2–7.3](electrical-report.md)).
Circuit C is switched at a **master pump switch on the Electrical Panel (EP)** — one
IP-rated cutoff for the whole pump circuit, upstream of everything — then runs the
ceiling trunk to a **12V DC distribution block** (positive + shared negative bus) on
the rear of this panel; from it a short 16 AWG branch feeds each pump directly.

| Item | Spec |
|------|------|
| Feed | Circuit C, 14 AWG, 15A fuse (one feed for all five pumps) |
| Master switch | 1 × IP-rated sealed rocker/disconnect (12V, 16A), **mounted on the EP** — single cutoff upstream of the whole circuit; no per-pump switches (each Shurflo runs on its internal pressure switch) |
| Distribution | 12V DC + / − bus block on the rear of the plumbing panel, fed from the EP master switch |
| Branches | 16 AWG, ~0.5–1m, block → pump, curved-elbow conduit (7.5A / 90W per pump) |

The pumps are operated **one at a time**: with the EP master switch on, the operator
opens the relevant ball valves for the current task (others closed), and that pump's
Shurflo **internal demand/pressure switch** then runs it on demand. The 15A fuse
covers a single pump with margin; simultaneous running is not intended.
The distribution block sits **above the spill line**, IP-rated and sealed, with drip
loops, per the wet-zone rules in [Electrical Report §7.5](electrical-report.md); the
master switch is on the EP, clear of the wet zone.

**Corridor Plumbing Panel — Front elevation: four pumps, ACC-01, DV-02 diverter, SV-02 sample tap, and full pipe routing**
![TBS-001 — Corridor Plumbing Panel Layout](assets/panel-layout.png)

**Spine side-sections (corridor side section) — two sheets, opposite
faces of the drain-riser spine** (18mm ply teed off the panel). Pumps mount on
the front face; the drain runs hang on the spine in the corridor gap clear of
both tote columns; the Circuit-C pump-power distribution feeds all five pumps.
P-02 lives on the Pinhole Wall panel and shares Circuit C. The two views share
all structure + fittings as landmarks; each face's own pipe runs appear on its
own sheet.

**Spine View A — intake face:** suctions (BV-01 Blue, tray sump, IBC-3),
the DV-01 blue-recycle riser climbing the spine into the X1 fill cross, the
DV-01-waste → IBC-4 merge, and the IBC-1 / Blue-supply fills.
![TBS-001 — Corridor Plumbing Panel Spine View A (−Yd intake face)](assets/panel-spine-view-a.png)

**Spine View B — discharge face (a mirror of A):** the X3 brown (P-05) and X4
gray (P-03) pump discharges running full along the spine to the sealed end-wall
ports, the P-01 → ACC drop, the P-04 discharge through SV-02, and the IBC-2 fill.
![TBS-001 — Corridor Plumbing Panel Spine View B (+Yd discharge face)](assets/panel-spine-view-b.png)

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

** Check Value CV-1** The Shurflo 2088 pumps have integral check valves. CV-1 guards the single gravity (non-pumped) path, the
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
spout pointing toward the operator so a cup fits beneath it from the right
walkway.

**Use:** run P-02 to pressurize the filtered line, crack SV-01 to catch ~50 ml in
a cup, close it, read pH on the meter, then set 3W-DV-01 to Blue-return (pH 6–7)
or Black-waste (pH drift / discolored).

---

## 5. Pipe Specifications

| Run | Schedule | Nominal Size | OD (mm) | Material | Notes |
|-----|----------|-------------|---------|----------|-------|
| Pump suction/discharge | Sch 40 | 1/2" | 21 | PVC Sch 40 | Matches Shurflo 2088 port thread |
| DV-02 outputs | Sch 40 | 1/2" | 21 | PVC Sch 40 | To IBC-3 or IBC-4 |
| DV-01 outputs | Sch 40 | 1/2" | 21 | PVC Sch 40 | To Blue IBC-2 or Black IBC-4 |
| Filter inter-stage | Sch 40 | 1" | 33 | PVC Sch 40 | Matches Big Blue 1" NPT ports |
| Filter outlet → DV-01 | Sch 40 | 1" | 33 | PVC Sch 40 | Gravity flow, lower restriction |
| IBC fill/drain (internal) | Sch 40 | 1" | 33 | PVC Sch 40 | IBC valve to corridor |
| IBC fill/drain (external bulkhead) | Sch 40 | 2" | — | PP (EPDM gaskets) | Bulkhead unions with camlock |
| Spray bar flex hose | — | 1/2" | — | Reinforced braided PVC | ~4m coiled, BV-05 to beam center feed |

All pump-driven internal runs use 1/2" pipe, matching the Shurflo 2088 pump
ports (1/2"-14 male parallel thread). This eliminates reducer fittings at pump
connections. The only reducer is a single 1/2"→1" bushing at the filter skid
inlet (P-02 output to F-01 input).

### 5.1 Joint Convention

**Pipe joints are solvent-weld (slip socket) by default — the run is glued PVC.**
**Threaded (NPT) is used *only* where a run lands on a hard component that must be
removable for service:** pumps, filter housings, valves, check valves, tank
bulkheads, sample taps, and the accumulator. Each such interface uses a **slip×NPT
transition adapter** (a male adapter glued into the run, threaded into the
component's port). This keeps the run cheap and leak-free while every component
stays unthreadable for maintenance.

Classifying the current BOM by this rule:

| Category | Connection | Parts |
|---|---|---|
| **Run joints — SLIP** | glued PVC socket | tees, elbows, cross, couplings, pipe |
| **Component interfaces — THREADED** | NPT (via slip×NPT adapter) | ball/diverter/check valves, camlocks, tank bulkheads, pump & filter ports, sample taps, accumulator |

Applying this convention **(a) resolved 2026-07-27: the run material is PVC Sch-40**
(see §5.2 — the §5 table is updated). **Still open (see [TODO](TODO.md)):** (b) the 1"
run tees/elbows now carried as threaded **Banjo FRPP** move to PVC slip, and (c) a
**slip×NPT male adapter** is added at each component interface (currently absent from
the BOM). The valves, camlocks, bulkheads, check valve, and pump/filter ports stay threaded.

### 5.2 Material: PVC Schedule 40 (justification)

The run pipe is **PVC Sch-40, solvent-welded**. PVC is chosen over HDPE because for this
service the deciding factors are **buildability and cost**, not the toughness where HDPE leads:

- **Joining — decisive for a hand-built system.** PVC solvent-welds with primer + cement and
  hand tools; HDPE *cannot be glued* — it needs heat-fusion equipment or bulkier, costlier
  mechanical/barbed fittings. Solvent-weld is what makes the §5.1 slip convention practical.
- **Pressure.** At the 45 PSI Shurflo 2088 service, Sch-40 (½" ≈ 600 PSI @ 73 °F) carries a
  ~13× margin — a non-issue for either material.
- **Chemistry.** Both are fully compatible with the dilute cyanotype wash (potassium
  ferricyanide, ferric ammonium oxalate, citric acid) — no advantage either way.
- **Cost & availability.** PVC pipe, fittings, and valves are the cheapest option and stocked
  everywhere (Home Depot); HDPE fittings are scarcer and pricier.

**The trade accepted:** HDPE's edge is toughness — impact, vibration, and freeze resistance
for a transported system. Both risks are mitigated operationally: the system is **drained for
transport** (no freeze-crack, less vibration mass) and every **pump connection uses flexible
braided hose** (absorbs vibration that would fatigue rigid joints); rigid runs are clipped at
close intervals. Keep runs off the sunniest wall face — PVC softens near 60 °C, though it
retains > 200 PSI hot, far above service. (If a future deployment must travel wet or in freezing
conditions, PEX is the tougher DIY alternative.)

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
- Backing board (18mm plywood) within the frame for the housing lag-screws

Each filter housing mounts through its own **mounting-hole ears** — Big Blue
heads are pre-drilled for wall mounting — with **SS lag/wood screws straight into
the 18mm plywood backing** (no custom bracket). 25mm plywood-offcut standoff blocks behind
each ear space the housing off the ply so the sump bowl hangs free and clears for
cartridge changes. Two lag screws per housing.

### 7.3 Pump Mounting

Each Shurflo 2088 mounts on a stainless steel 4-bolt bracket (Shurflo OEM
accessory). The bracket screws through the plywood panel. Pump body orientation
is vertical with ports at the head (top), facing left and
right. This orientation minimizes the footprint on the 270mm-wide
panel and allows gravity to assist with priming.

### 7.4 Panel Protrusion Envelope

| Component | Protrusion from panel face (-X) |
|-----------|-------------------------------|
| Pump body (Shurflo 2088) | 114mm |
| Filter housing (Big Blue 4.5"×20") | 130mm |
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

### 8.1 Corridor ↔ pinhole-wall ribbon (under the right walkway)

The four lines that connect the corridor equipment to the pinhole-wall panel —
IBC-3 (Brown) → P-02, the filtered return (SV-01 → DV-01), the tray-sump pickup
→ P-04, and the Blue supply trunk → TAP-01/spray bar — run together as a flat
**ribbon** in the otherwise-dead space **under the right-walkway grate**, in the
clear channel between the two walkway long beams (hugged to the outer/IBC edge,
clear of the print zone). The lanes ride **flush against the grate underside** so
the whole over-tray run clears the spray-bar carriage beneath it, and the two
middle lanes alternate (Blue trunk / Brown sump) so the blue and brown lines never
cross. This replaces routing them through the congested tray↔IBC gap.

At the first cantilever (nearest the pinhole wall) each line **loops up over the
cantilever** — then returns to the flush ribbon
height. Rather than dipping under the walkway support beam (which would foul the
spray carriage), each line crosses the **outer long beam through an open-top notch**
and drops the **tray-edge slot** — clear of the carriage travel — into the corridor,
where it rises to its equipment connection. The pump-suction lines carry their own
service turns (P-04's sump pickup rises straight out of the widened sump well and
elbows flat into the ribbon lane at flush height — no over-deck loop; DV-01's filtered
return makes a square 90° turn into the diverter's IN port). The ribbon is carried by four welded steel cross-braces between the walkway
bearers, with the lines clipped to them. The full set of cross-sections — routing
envelope, clearances, and the beam notch — is in
[Walkway Pipe Routing](walkway-routing-sections.md); routing is verified
collision-free by `src/models/check_interference.py` (the ribbon is a sanctioned
exception to the processing-tray exclusion zone — it runs above the tray rim, under
the grate).

---

## 9. Parts List

The panel-mounted equipment for each plumbing panel is listed below — generated from the parts
registry (firm low–high bands, April-2026 indicative basis). The **full** water-system BOM (pipe,
fittings, IBC totes, external bulkhead ports, wiring, consumables) is in the
[Water System Report](water-system-report.md) §Parts-List; the panel ply/backing and mounting
hardware are sourced there and in the IBC stacking frame line.

### 9.1 Corridor Plumbing Panel

<!-- BEGIN parts:corridor-plumbing-panel -->
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [Shurflo 2088-554-144 pump (×5 — P-01 Blue supply / P-02 filter loop / P-03 waste evac / P-04 tray drain / P-05 Brown drain)](https://www.amazon.com/dp/B00C1M6B1C) (B00C1M6B1C) | 12VDC, 3.5 GPM, 45 PSI, 1/2" NPSM ports; 5 identical pumps, one per water-system duty (P-01..P-05). 2026-07-27: consolidated from 5 lines; firm $100 ea (Amazon B00C1M6B1C) | 5 ea | Amazon / Fresh Water Systems | $500 |
| [SeaFlo accumulator (0.75 L)](https://www.amazon.com/dp/B01MUYL8F8) (SFAT-075-125-01) | 0.75 L, 125 PSI, 1/2" MNPT | 1 ea | Amazon | $36 |
| [Corridor plumbing-panel ply (23/32" exterior)](https://www.homedepot.com/p/23-32-in-x-4-ft-x-8-ft-RTD-Southern-Yellow-Pine-Wood-Sheathing-Plywood-129323/303564747) (303564747) | 4×8 ft 23/32" (18mm) RTD Southern Yellow Pine exterior sheathing — rear backing board + drain-riser spine + spacer offcuts. STANDARD exterior per project rule. Firm $29.30 (Home Depot 2026-07-23). Seal cut edges. | 1 sheet | Home Depot | $29 |
| [Pump-mount shirt ply (23/32" exterior)](https://www.homedepot.com/p/23-32-in-x-4-ft-x-8-ft-RTD-Southern-Yellow-Pine-Wood-Sheathing-Plywood-129323/303564747) (303564747) | 4×8 ft 23/32" (18mm) RTD Southern Yellow Pine exterior sheathing — pump-mount shirt (~610×1650 cut) behind P-01..P-05 + 6× spacer blocks. Same SKU as ply-18; 5× Shurflo 2088 (~6.5 kg total) need no more than 3/4". STANDARD exterior per project rule. Firm $29.30 (Home Depot 2026-07-23). May nest with ply-18 in one sheet at cut — carried separate for margin. Double-layer locally if extra pump-rail stiffness wanted. | 1 sheet | Home Depot | $29 |
| 6× steel angle brackets (corridor panel → IBC uprights) | L-brackets fixing the corridor plumbing panel to the IBC-frame front-portal uprights. Price est. | 6 ea | Home Depot | $15–$39 |
| Corridor panel mount fasteners (shirt-to-panel screws + lag bolts) | Shirt-to-panel screws + lag bolts landing the brackets into the panel/uprights. Price est. | 1 lot | Home Depot | $10–$11 |
| [Banjo V050FP ball valve 1/2" FNPT](https://www.usplastic.com/catalog/item.aspx?itemid=30651) (30651) | PP full-port quarter-turn; pump-suction isolation BV-01 (P-01), BV-02 (P-05), BV-06 (P-03) | 3 ea | US Plastic Corp / Amazon | $133 |
| [3-way diverter valve 1/2" FNPT](https://www.usplastic.com/catalog/item.aspx?itemid=22365) (22365) | L/T-port PVC-compatible; 3W-DV-02 (tray drain) | 1 ea | US Plastic Corp | $24 |
| [pH sample tap (SV-02) — 1/2" PP ball valve + barb spout + branch tee](https://www.usplastic.com/catalog/item.aspx?itemid=36903) (36903) | pH sample on the P-04 tray-drain discharge, before 3W-DV-02; same build/SKU as SV-01 (US Plastic 36903 $19.26 — priced under SV-01; applied to SV-02 as the identical build) | 1 ea | US Plastic Corp | $19 |
| [Steel flat bar 25×3mm — ribbon support cross-brace](https://www.mcmaster.com/6775T37-6775T373/) (6775T37) | Low-carbon steel flat bar 25×3mm × 3 ft. Welded between the two right-walkway long bearers at 4 stations to carry the under-walkway pipe ribbon (four corridor↔pinhole lines); 4 braces ~300mm each = cut from 2× 3-ft bars (2 spare pieces). | 2 3ft bar | McMaster-Carr | $35 |
| [Cushioned pipe clip](https://www.amazon.com/dp/B01HPE188Q) (B01HPE188Q) | Cushioned clamp for ½" pipe (0.84"/21mm OD); secures the four under-walkway ribbon lines to the support cross-braces (4 lines × 4 supports). Sold in 20-packs at $9.99 ($0.50/ea); one pack covers the 16 + spares. | 16 ea | Amazon | $8 |
| **Corridor Plumbing Panel total** | | | | **$839–$864** |
<!-- END parts:corridor-plumbing-panel -->

### 9.2 Pinhole Wall Plumbing Panel

<!-- BEGIN parts:pinhole-wall-plumbing-panel -->
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [Big Blue filter housing 4.5"×20" (separate)](https://www.amazon.com/dp/B0137680E6) (B0137680E6) | Ø184×594mm/housing (4.5×20), 1" NPT ports, accepts standard 20"×4.5" cartridges (verified 2026-07-27) — three SEPARATE Pentair Pentek 150234 high-flow PP housings on the mounting brackets | 3 ea | Amazon | $250 |
| [Big Blue housing mounting brackets (×3)](https://www.freshwatersystems.com/products/mounting-bracket-white-single-housing-for-10-20-big-blue-housings) (150061) | Pentair 150061 zinc-plated single-housing mounting bracket, one per 4.5×20 Big Blue (×3), lag-screwed to the 18mm ply backing. Purpose-built — replaces the welded slotted-angle frame (2026-07-27). | 3 ea | Fresh Water Systems | $32 |
| [SS lag/wood screws — filter housings to ply backing](https://www.homedepot.com/p/302007729) (812670) | 2 per housing × 3 = 6 needed — Everbilt 5/16"×1½" SS hex lag screws through the housing's mounting-hole ears into the 18mm plywood backing (no custom bracket). Sold in 5-packs → 2 packs (10, 4 spare). | 2 5-pack | Home Depot | $14 |
| Plywood offcut spacer blocks 25mm (filter skid) | 25mm standoff blocks between the housing's mounting ears and the ply backing — sump-bowl hang clearance (the housing lag-screws through them into the ply). Cut from PLYWOOD OFFCUTS (2026-07-25 — no need for HDPE; dry standoff, not a wet-immersion part). | 1 lot | offcuts | $0 |
| [MPP 5-micron sediment cartridge 4.5"×20"](https://www.amazon.com/dp/B0CJCVZ1L5) (B0CJCVZ1L5) | Pentek DGD-5005-20 dual-gradient-density 5-micron sediment cartridge (F-1 stage); ~50-print interval. $61.66/2-pack = $30.83 ea. | 2 ea | Amazon | $62 |
| [KDF-55 heavy-metal cartridge 4.5"×20"](https://www.amazon.com/dp/B0DY1ZK47Z) (B0DY1ZK47Z) | KDF-55 media for dissolved iron/metal removal (F-2 stage); ~60-print interval. Aquaboon 20×4.5 KDF whole-house cartridge (proper KDF media — supersedes the earlier VEVOR chlorine-only cartridge). | 1 ea | Amazon | $80 |
| [CTO carbon block cartridge 4.5"×20"](https://www.amazon.com/dp/B07ZHPB6MB) (B07ZHPB6MB) | Coconut shell activated carbon block (F-3 stage); ~40-print interval. Aquaboon CTO, $79.79/2-pack = $39.90 ea (same brand as the KDF/sediment cartridges). | 2 ea | Amazon | $80 |
| [Banjo V050FP ball valve 1/2" FNPT](https://www.usplastic.com/catalog/item.aspx?itemid=30651) (30651) | PP full-port quarter-turn; pump-suction isolation BV-03 (P-02) | 1 ea | US Plastic Corp / Amazon | $44 |
| [3-way diverter valve 1" FNPT](https://www.usplastic.com/catalog/item.aspx?itemid=31268) (31268) | L/T-port; 3W-DV-01 (filter output) | 1 ea | US Plastic Corp | $61 |
| [pH sample tap (SV-01) — 1/2" PP ball valve + barb spout + branch tee](https://www.usplastic.com/catalog/item.aspx?itemid=36903) (36903) | Filtered-water sample draw before 3W-DV-01; 1/2" PP sample valve (US Plastic 36903) + downturned 1/2" hose barb on a 1"×1/2" reducing branch tee, panel face above spill line | 1 ea | US Plastic Corp | $19 |
| **Pinhole Wall Plumbing Panel total** | | | | **$642** |
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
| Monthly | Inspect filter housing clamp bands and mounting lag screws |
| Every ~40 prints | Replace F-03 (CTO carbon block) cartridge |
| Every ~50 prints | Replace F-01 (5μm sediment) cartridge |
| Every ~60 prints | Replace F-02 (KDF-55) cartridge |
| Quarterly | Check accumulator pre-charge pressure (should hold 30 PSI) |
| Quarterly | Inspect check valve CV-1 (X1 fill line) for proper seating |
| Annually | Inspect plywood panel for delamination or moisture damage; reseal if needed |

**Filter replacement procedure:** Close P-02 supply valve. Place bucket under
housing. Turn sump bowl counter-clockwise with Big Blue wrench (included with
housing). Remove spent cartridge, inspect housing interior, insert new
cartridge, re-seat sump bowl, hand-tighten plus 1/4 turn. Run P-02 for 1
minute to flush; check for leaks.

---

## 11. Source References

1. [Shurflo 2088-554-144 datasheet](https://www.shurflo.com/products/2088-series) — 12VDC diaphragm pump, 3.5 GPM, 45 PSI,
   self-priming. 127mm × 216mm × 114mm body dimensions, 1/2"-14 NPSM ports.
2. [Pentek Big Blue 4.5"×20" housing specifications](https://www.pentair.com/en-us/water-treatment-components/filter-housings/big_blue_heavy_duty_series.html) — 1" NPT inlet/outlet,
   184mm OD, ~594mm total height, polypropylene head.
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
   Tray sump, P-04 suction pickup, spray bar connection to BV-05.
9. [Walkway Pipe Routing](walkway-routing-sections.md) — Cross-sections of the
   corridor↔pinhole-wall ribbon under the right walkway: routing envelope,
   clearances, the beam notch, and the spray-carriage clearance (§8.1).
