<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# IBC Stacking System

## 1. Purpose

TBS-001's three-circuit water system requires four 600 L IBC totes arranged in a
2×2 stack in the right end zone (X=4674–5893mm) of the container. Two Blue supply
totes (IBC-1 and IBC-2) sit on top; one Brown recycle tote (IBC-3) and one Waste tote
(IBC-4) sit on the bottom. A welded mild steel stacking frame supports the upper tier,
restrains all four totes for transport, and maintains a 270mm plumbing corridor
between the near and far columns for internal pipe routing, valves, and the equipment
panel.

**Design goals:**

- Support 4× 600 L IBC totes in a 2×2 stack (2 columns × 2 tiers)
- Restrain all totes for road transport with D-ring lashing points
- Maintain a central plumbing corridor for pipe routing and valve access
- Provide access gates for bottom-tier drain valves
- Enable external fill and drain without opening cargo doors
- Fit within the 2388mm container ceiling height with adequate clearance

---

## 2. IBC Totes

### 2.1 Specification

| Parameter | Value |
|-----------|-------|
| Model | Schutz Ecobulk MX 640 L (or equivalent US 48×40 composite tote) |
| Capacity | 600 L (~158 US gal) usable per tote |
| Overall dimensions | 1,219 × 1016 × 1010mm (W × D × H) |
| Pallet format | US 48" × 40" composite |
| Pallet base height | 168mm (includes feet/runners) |
| Cage upright tube | Ø25mm |
| Cage top rail | 25mm OD |
| Drain valve | DN50 butterfly valve, S60×6 thread, at Z=185mm above IBC base |
| Fill cap | DN150 screw cap on top |
| Tare weight | ~55 kg per tote |
| Full weight (600 L) | ~655 kg per tote |
| Total system weight (4 totes full) | ~2,620 kg |

### 2.2 Tote Assignments

| Tote | Position | Circuit | Function |
|------|----------|---------|----------|
| IBC-1 | Top tier, near column | Blue (clean supply) | Primary clean water supply for spray bar |
| IBC-2 | Top tier, far column | Blue (clean supply) | Secondary supply, self-levels via 2" cross-connect from IBC-1 |
| IBC-3 | Bottom tier, near column | Brown (recycled) | Wash water buffer — filtered and recycled back to Blue |
| IBC-4 | Bottom tier, far column | Black (waste) | Contaminated water sealed for off-site disposal |

### 2.3 Layout

| Parameter | Value |
|-----------|-------|
| Near column Yd | 30–1046mm (pushed to near/pinhole wall, 30mm clearance) |
| Far column Yd | 1316–2332mm (pushed to far wall, 30mm clearance) |
| Column X range | 4674–5893mm (right-justified to sealed end wall) |
| Plumbing corridor | Yd=1046–1316mm (270mm gap between columns) |
| Single IBC height | 1010mm |
| Stacked height (2 totes + frame + mat) | 2020mm (totes) + 50mm (frame beam) + 12mm (rubber mat) = 2082mm |
| Ceiling clearance | 306mm (2388 − 2082mm) |

---

## 3. Stacking Frame

### 3.1 General Arrangement

The frame is a portal spine structure running along the 270mm plumbing corridor.
The platform cross-beams supporting the upper tier are **simply supported
wall-to-wall** — propped at the two corridor uprights *and* at the container side
walls by welded seat brackets. (This replaces the earlier cantilever scheme; see
[§3.5](#35-structural-validation).) Three bays along X (front/mid/back uprights at
642mm centers) provide the structural grid. Each of the six corridor uprights is
anchored to the container floor by a flange-plate foot. The frame has no end posts
in the X direction — IBCs are loaded from above via the corridor when the right
walkway is removed.

### 3.2 Frame Specification

| Parameter | Value |
|-----------|-------|
| Material | 50 × 50 × 3mm RHS mild steel (A500 Grade B) |
| Footprint (X × Yd) | 1284 × 2362mm (wall-to-wall, 3 bays along X) |
| Total height | 2070mm (floor to top rail) |
| Corridor uprights | 6 total (3 per side of corridor, at X=0/642/1284mm) |
| Platform level | Z=1010mm (top of bottom-tier IBCs) |
| Top rail level | Z=2070mm (top of stacked IBC cages + frame beam) |
| Bay spacing | 642mm (3 bays: front, mid, back) |
| Floor anchorage | 6 × 150 × 150 × 12mm flange-plate feet, 4 × M12 anchors each |
| Wall seat brackets | 6 (one per platform-beam outer end) — welded 8mm back-plate + 10mm seat + 8mm triangular gusset web; load-bearing |
| Bracket attachment | 4 × M12 to wall corrugation ribs per bracket; gusset web transfers the seat reaction into the back-plate |
| Top lateral ties | Light clip at each top-beam wall end (restraint only) |
| Frame weight | ~130 kg (incl. feet + seat brackets) |
| Joints | Welded (fillet weld throughout, mitred corners) |

### 3.3 Platform

The platform sits at Z=1010mm and supports the upper-tier IBCs.

| Parameter | Value |
|-----------|-------|
| Platform beams | 50 × 50 × 3mm RHS, spanning each column width |
| Cross-beams | 50 × 50 × 3mm RHS bridging the plumbing corridor at platform and top rail levels |
| Anti-slip mat | 12mm closed-cell rubber, one mat per column, placed on platform beams |
| Anti-rotation lip | 5mm steel plate × 40mm height, fillet-welded to platform beam perimeter |
| Lip function | Engages IBC cage foot to prevent lateral movement during transport |

### 3.4 X-Bracing

Bottom-tier bays include diagonal X-bracing (flat bar) for racking resistance during
transport. The bracing runs between the front/mid and mid/back uprights on the
corridor side of each column.

### 3.5 Structural Validation

**Section.** 50 × 50 × 3mm RHS, [A500 Grade B](https://www.astm.org/a0500_a0500m-23.html)
(minimum yield F<sub>y</sub> = 315 MPa). Second moment of area I = 20.8 cm⁴,
elastic section modulus Z = 8.34 cm³, E = 200 GPa
([Atlas Steels — Square & Rectangular Hollow Sections, dimensions & properties](https://www.atlassteels.com.au/documents/Atlas_Technical_Handbook_rev_Aug_2013-web.pdf)).

**Design load.** Worst case is the *camera-ready* state with the top tier holding
two full Blue totes (water), 655 kg each. Each top tote is carried over the span
from its container-wall seat bracket to the adjacent corridor upright (L ≈ 1046mm),
shared across the three platform cross-beams — a governing patch of ≈ 218 kg per
beam, modeled as a uniform load.

**Cantilever vs. simple span.** Propping the beam end at the wall (rather than
cantilevering it off the corridor spine) is what makes the section work
([simply-supported beam](https://www.engineeringtoolbox.com/beams-support-loads-deflection-d_1311.html),
[cantilever beam](https://www.engineeringtoolbox.com/cantilever-beams-d_1848.html)):

| Load path | Max moment | Bending stress σ = M/Z | Safety factor F<sub>y</sub>/σ | Deflection | Verdict |
|-----------|-----------|------------------------|-------------------------------|-----------|---------|
| Cantilever (old) | 1.12 kN·m | 134 MPa | 2.3 | 7.4mm (L/141) | Marginal |
| **Simple span (new)** | **0.28 kN·m** | **34 MPa** | **9.3** | **0.8mm (L/1300)** | **Ample** |

Converting to a simple span cuts bending stress ~4× and deflection ~9×.

**Reactions & securing.**

- Each **wall seat bracket** carries the simple-span end reaction ≈ **110 kg
  (1.1 kN)** vertical. The 8mm back-plate bolts to the wall ribs with 4 × M12; the
  triangular gusset web transfers the seat reaction into the back-plate. At 110 kg
  the M12 group (≈ 11 kN shear capacity each in Grade 8.8) is loaded to a small
  fraction of capacity.
- Each of the **6 corridor uprights** is anchored by a 150 × 150 × 12mm floor
  flange plate with 4 × M12 anchors, restraining uplift and the lateral (transport)
  loads carried into the bottom rail.

---

## 4. Securing for Transport

### 4.1 D-Ring Lashing Points

| Parameter | Value |
|-----------|-------|
| Quantity | 8 total (4 per tier) |
| Type | 25mm welded D-ring on 6mm mounting plate |
| Working load limit | 1,100 kg per ring |
| Mounting | Fillet-welded to corridor-facing frame uprights |
| Supplier | McMaster-Carr #3641T29 |

### 4.2 Ratchet Straps

| Parameter | Value |
|-----------|-------|
| Type | 25mm ratchet strap |
| Working load limit | 1,100 kg |
| Routing | D-ring to D-ring, over IBC top, 1 strap per tier per side |
| Total straps | 4 (2 per tier) |
| Pre-transport | Tighten all straps; re-check tension after 50 km |

### 4.3 Anti-Rotation Lip

The 40mm steel lip welded around the platform perimeter engages the upper-tier IBC
cage feet, preventing lateral sliding or rotation. Combined with the ratchet straps
from above and the pallet sitting on the rubber mat, the upper-tier IBCs are
positively restrained in all six degrees of freedom.

Bottom-tier IBCs sit on the container floor with their cage feet constrained by the
frame uprights on three sides (two uprights plus the wall bracket side). Ratchet
straps provide vertical and lateral restraint.

---

## 5. Access Gates

Removable gate panels at the base of each column provide access to the bottom-tier
IBC drain valves (DN50 butterfly, corridor-facing at Z=185mm).

| Parameter | Value |
|-----------|-------|
| Quantity | 2 (one per column, corridor-facing) |
| Gate height | 300mm (Z=0–300mm) |
| Attachment | 4 × M12 hex bolts per gate |
| Operation | Remove gate panel to access drain valve for maintenance; re-bolt after |
| Normal operation | Drain pipes connect permanently through gate opening — gate stays installed except for valve maintenance |

---

## 6. External Plumbing Panel

Three 2" NPT bulkhead unions penetrate the sealed end wall on the container
centerline (Yd=1181mm), allowing external fill and drain without opening cargo
doors.

### 6.1 Port Layout

| Port | Height (Z) | Circuit | Function |
|------|-----------|---------|----------|
| X1 | 2250mm | Blue | Fill IBC-1 — above IBC tops (2082mm) for gravity feed; IBC-2 self-levels via 2" cross-connect |
| X3 | 400mm | Brown | Drain IBC-3 — bottom tier, near column |
| X4 | 200mm | Waste | Drain IBC-4 — bottom tier, far column |

### 6.2 Exterior Fittings

| Parameter | Value |
|-----------|-------|
| Bulkhead type | 2" NPT bulkhead union |
| Exterior fittings | Type DC camlock (2" aluminum) — quick-connect for fill/drain hose |
| Reinforcing plate | 6mm mild steel, ~300mm wide, welded to wall interior before penetrations |
| Seal | Neoprene gasket — light-tight and watertight |
| IBC-2 fill | No dedicated port — self-levels from IBC-1 via permanently open 2" cross-connect at valve height |

---

## 7. Internal Plumbing

### 7.1 Pipe Specification

| Parameter | Value |
|-----------|-------|
| Material | 1" HDPE SDR-11 (33.4mm OD, 3mm wall) |
| Elbows | Banjo LE100, 1" HDPE NPT, 90° |
| Ball valves | Banjo V100FP, 1" full-port poly, quarter-turn |
| Cross-connect | 2" HDPE pipe, IBC-1 ↔ IBC-2 (self-leveling, permanently open, no valve) |

### 7.2 Pipe Routing

All pipes route through the 270mm plumbing corridor between the near and far IBC
columns. IBC valve faces point toward the corridor (DN50 butterfly valve, S60×6
thread).

| Pipe | Route | Notes |
|------|-------|-------|
| X1 fill (Blue) | End wall bulkhead → corridor → V1 ball valve → IBC-1 fill cap (DN150, from top) | Gravity feed from Z=2250mm |
| X3 drain (Brown) | IBC-3 DN50 valve → V3 ball valve → corridor → end wall bulkhead | Gravity drain at Z=400mm |
| X4 drain (Waste) | IBC-4 DN50 valve → V4 ball valve → corridor → end wall bulkhead | Gravity drain at Z=200mm |
| Cross-connect | IBC-1 valve height → IBC-2 valve height | 2" pipe, self-leveling, no valve |

### 7.3 Equipment Panel

An 18mm marine plywood panel spans across the IBC plumbing corridor
(Yd=1046–1316mm) at X=5000mm. All pumps, filters, accumulator, and diverter
valves mount on this panel.

| Equipment | Specification |
|-----------|--------------|
| Pumps | P-01, P-02, P-03, P-04 — Shurflo 2088 (12V DC, 3.5 GPM, 45 PSI) |
| Accumulator | ACC-01 — 0.75 L (23.5 oz), 125 PSI |
| Filter unit | Purcooflow WHF2045B302 3-stage (F1: 5μ sediment, F2: KDF-55, F3: GAC carbon) |
| Panel size | 270 × ~1110mm (corridor width × working height) |

---

## 8. Engineering Drawings

Eight construction drawings cover the IBC system across two drawing sets:

### IBC Stacking & Securing (5 sheets)

**Sheet 1 — Cross-section elevation: 2-tier stack, frame, D-rings, ceiling clearance**
![TBS-001 IBC Stacking — Sheet 1](assets/ibc-stacking-sheet1.png)

**Sheet 2 — Fastening details: D-ring lashing, anti-rotation lip, access gate, strap routing**
![TBS-001 IBC Stacking — Sheet 2](assets/ibc-stacking-sheet2.png)

**Sheet 3 — External plumbing panel: Sealed end wall elevation with 3× bulkhead ports**
![TBS-001 IBC Stacking — Sheet 3](assets/ibc-stacking-sheet3.png)

**Sheet 4 — Internal plumbing plan view: IBC layout, pipe routing, valves, equipment panel**
![TBS-001 IBC Stacking — Sheet 4](assets/ibc-stacking-sheet4.png)

**Sheet 5 — Internal plumbing elevation: Pipe routing from IBCs to bulkhead unions**
![TBS-001 IBC Stacking — Sheet 5](assets/ibc-stacking-sheet5.png)

### IBC Support Frame Fabrication (3 sheets)

**Sheet 1 — Front elevation: Corridor uprights, beams, wall seat brackets, floor flange feet, D-rings, access gates**
![TBS-001 IBC Frame — Sheet 1](assets/ibc-frame-sheet1.png)

**Sheet 2 — Side elevation: Three-bay structure, X-bracing, longitudinal beams, floor flange feet**
![TBS-001 IBC Frame — Sheet 2](assets/ibc-frame-sheet2.png)

**Sheet 3 — Plan view at platform level: Beam layout, wall seat brackets, floor feet, lip perimeter, rubber mats**
![TBS-001 IBC Frame — Sheet 3](assets/ibc-frame-sheet3.png)

Full drawings also appear in [Engineering Diagrams](engineering-diagrams.md) §15
(stacking) and §17 (frame fabrication).

---

## 9. Parts List

### 9.1 Stacking Frame

| Item | Specification | Qty | Est. cost (USD) |
|------|--------------|-----|----------------|
| 50 × 50 × 3mm RHS mild steel (6 m lengths) | Frame uprights, beams, cross-members | 8 | $240–$360 |
| 12mm steel plate, 150 × 150 cut | Upright floor flange feet | 6 | $25–$45 |
| 8mm steel plate (back-plates, seats, gussets) | 6 welded wall seat brackets | 1 lot | $50–$80 |
| 5mm steel plate (flat bar) | Anti-rotation lip (perimeter, ~8 m total) | 1 | $30–$50 |
| 12mm closed-cell rubber mat (1000 × 1200mm) | Anti-slip platform mats | 2 | $40–$60 |
| 25mm welded D-ring (McMaster #3641T29) | Lashing points with 6mm mount plates | 8 | $40–$65 |
| 25mm ratchet strap, 1,100 kg WLL | Transport securing | 4 | $30–$50 |
| M12 × 40 bolt, Grade 8.8 (into wall ribs) | Wall seat brackets, 4 each | 24 | $25–$45 |
| M12 floor anchor (wedge/sleeve, container floor) | Upright flange feet, 4 each | 24 | $40–$70 |
| Flat bar X-bracing | Bottom-tier racking resistance | 4 | $20–$35 |
| Access gate panels (300mm high, steel) | Removable, 4 × M12 bolts each | 2 | $40–$60 |
| Welding / fabrication (frame assembly) | ~26–36 hrs labor (incl. feet + seat brackets) | 1 | $1,150–$1,650 |
| Primer + paint | Anti-corrosion coating | 1 | $40–$60 |
| **Frame subtotal** | | | **$1,770–$2,630** |

### 9.2 External Plumbing Panel

| Item | Specification | Qty | Est. cost (USD) |
|------|--------------|-----|----------------|
| 2" NPT bulkhead union | End wall penetrations | 3 | $45–$75 |
| 2" Type DC aluminum camlock | Exterior quick-connect fittings | 3 | $30–$50 |
| 6mm mild steel reinforcing plate (~300 × 2100mm) | Welded to wall interior | 1 | $40–$60 |
| Neoprene gaskets | Light-tight, watertight seal | 3 | $10–$15 |
| **External plumbing subtotal** | | | **$125–$200** |

### 9.3 Internal Plumbing

| Item | Specification | Qty | Est. cost (USD) |
|------|--------------|-----|----------------|
| 1" HDPE SDR-11 pipe (per meter) | Corridor pipe runs (~10 m total) | 10 m | $30–$50 |
| 2" HDPE pipe | Cross-connect IBC-1 ↔ IBC-2 (~2 m) | 2 m | $10–$20 |
| Banjo LE100 90° elbow (1" HDPE NPT) | Direction changes | 8 | $25–$40 |
| Banjo V100FP ball valve (1" full-port) | V1, V3, V4 isolation valves | 3 | $30–$45 |
| Hose clamps + fittings | IBC connections, bulkhead connections | 12 | $20–$30 |
| **Internal plumbing subtotal** | | | **$115–$185** |

### 9.4 IBC Totes

| Item | Specification | Qty | Est. cost (USD) |
|------|--------------|-----|----------------|
| 600 L IBC tote (Schutz Ecobulk MX or equiv.) | New or reconditioned US 48×40 composite | 4 | $200–$600 |
| **IBC subtotal** | | | **$200–$600** |

### 9.5 Cost Summary

| Assembly | Low estimate | High estimate |
|----------|------------|--------------|
| Stacking frame | $1,770 | $2,630 |
| External plumbing panel | $125 | $200 |
| Internal plumbing | $115 | $185 |
| IBC totes (4×) | $200 | $600 |
| **Total** | **$2,210** | **$3,615** |

---

## 10. Maintenance Schedule

| Interval | Task |
|----------|------|
| Every use | Visually inspect ratchet strap tension before transport |
| Every 10 prints | Inspect IBC valve seals (DN50 butterfly) for drips; tighten or replace O-ring |
| Every 10 prints | Check external camlock fittings for cross-threading; clean dust caps |
| Every 25 prints | Replace F-1 sediment cartridge (5μ melt-blown PP) |
| Every 20 prints | Replace F-3 GAC carbon block cartridge |
| Every 30 prints | Replace F-2 KDF-55 heavy metal cartridge |
| Every 6 months | Inspect D-ring welds for cracking; load-test straps |
| Every 6 months | Inspect rubber mats for compression set; replace if permanently deformed |
| Every 6 months | Inspect anti-rotation lip welds; check lip height (40mm minimum) |
| Annually | Inspect frame welds (all joints) for fatigue cracking |
| Annually | Touch up paint on frame where chipped or rusted |
| Annually | Inspect wall seat bracket bolts and upright floor-anchor bolts for loosening; re-torque to spec |
| Annually | Flush all internal pipes with clean water; inspect for biofilm |
| As needed | Replace camlock gaskets if leaking |
| As needed | Clean IBC interiors between circuit changes (bleach rinse + water flush) |

---

## 11. Sources

| Item | Source |
|------|--------|
| Schutz Ecobulk MX 640 L IBC | [Schutz GmbH product catalog](https://www.schuetz-packaging.net/schuetz-usa/en/ibcs/ecobulk/ecobulk-mx/) — US 48×40 composite tote, DN50 valve, UN31HA1/Y |
| D-ring lashing point | [McMaster-Carr #3641T29](https://www.mcmaster.com/3641T29) — 25mm, 1,100 kg WLL |
| Banjo V100FP ball valve | [Banjo Corp catalog](https://www.banjocorp.com/banjo/Valves/V100FP/p/2832572) — 1" full-port polypropylene, quarter-turn |
| Banjo LE100 90° elbow | [Banjo Corp catalog](https://www.banjocorp.com/banjo/Pipe-Fittings/EL100-90/p/2796532) — 1" HDPE NPT |
| HDPE SDR-11 pipe | [Standard 1" IPS](https://www.ferguson.com/category/pipe-tubing/plastic-pipe-tubing/plastic-pipe/?prefn1=sku_Material_Type_ss&prefv1=HDPE) — PE4710 resin, 200 PSI rated |
| Type DC camlock fitting | [2" aluminum, MIL-C-27487 spec](https://www.amazon.com/s?k=2+inch+aluminum+camlock+type+DC) |
| Shurflo 2088 pump | [Pentair Shurflo catalog](https://www.shurflo.com/products/2088-series) — 12V DC, 3.5 GPM, 45 PSI, self-priming diaphragm |
| Water system architecture | [Water System Report](water-system-report.md) §3 |
| IBC layout and stacking | [Equipment Layout Report](equipment-layout-report.md) §5 |
| Frame fabrication drawings | [Engineering Diagrams](engineering-diagrams.md) §15, §17 |
| Equipment panel specification | [Engineering Diagrams](engineering-diagrams.md) §18 |

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
