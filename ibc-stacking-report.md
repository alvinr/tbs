<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# IBC Stacking System

## 1. Purpose

TBS-001's three-circuit water system requires four 1,000 L caged composite totes arranged in a
2×2 stack in the right end zone of the container. Two Blue supply
totes (IBC-1 and IBC-2) sit on top; one Brown recycle tote (IBC-3) and one Waste tote
(IBC-4) sit on the bottom. A welded mild steel **restraint-only** frame restrains all four direct-stacked totes for transport, and maintains a <!-- BEGIN fact:corridor_width_mm -->270<!-- END fact:corridor_width_mm -->mm plumbing corridor
between the near and far columns for internal pipe routing, valves, and the equipment
panel.

**Design goals:**

- Restrain 4× 1,000 L caged totes in a 2×2 direct-stack (2 columns × 2 tiers)
- Restrain all totes for road transport with weld-on lashing rings
- Maintain a central plumbing corridor for pipe routing and valve access
- Enable external fill and drain without opening cargo doors
- Fit within the <!-- BEGIN fact:container_height_mm -->2,388<!-- END fact:container_height_mm -->mm container ceiling height with adequate clearance

<!-- brochure:skip -->
**Interactive 3D model** — the four IBC totes, the welded stacking frame, and the plumbing corridor. Drag to orbit, scroll to zoom.

<div class="sketchfab-embed-wrapper">
  <div style="position:relative;width:100%;padding-bottom:56.25%;">
    <iframe title="TBS-001 IBC Model" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/8d091c60e93848f38e26c9c89a08cbc8/embed" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>
  </div>
  <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"><a href="https://sketchfab.com/3d-models/tbs001-ibc-model-8d091c60e93848f38e26c9c89a08cbc8?utm_medium=embed&utm_campaign=share-popup&utm_content=8d091c60e93848f38e26c9c89a08cbc8" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">TBS001 - IBC Model</a> by <a href="https://sketchfab.com/alvin91403?utm_medium=embed&utm_campaign=share-popup&utm_content=8d091c60e93848f38e26c9c89a08cbc8" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">alvin91403</a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=8d091c60e93848f38e26c9c89a08cbc8" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>
</div>
<!-- brochure:endskip -->

---

## 2. IBC Totes

### 2.1 Specification

| Parameter | Value |
|-----------|-------|
| Model | Schütz Ecobulk MX 1000L (or equivalent US 48×40 caged composite tote) |
| Capacity | 1,000 L (~264 US gal) per tote. **"600 L" / "1,000 L" are fill levels, not tote sizes** — all four totes are identical |
| Overall dimensions | 1,219 × 1016 × 1,168mm (W × D × H) |
| Pallet format | US 48" × 40" composite |
| Pallet base height | 168mm (includes feet/runners) |
| Cage upright tube | Ø25mm |
| Cage top rail | 25mm OD |
| Drain valve | DN50 butterfly valve, S60×6 thread |
| Fill | **side entry near the top** (no top-cap access — only <!-- BEGIN fact:ibc_ceiling_clearance_mm -->52<!-- END fact:ibc_ceiling_clearance_mm -->mm headroom stacked) |
| Tare weight | ~65 kg per tote |
| Full weight (1,000 L) | ~1,065 kg per tote |
| Total tare (4 totes) | ~260 kg; water load see [weight-distribution report](weight-distribution-report.md) |

### 2.2 Tote Assignments

| Tote | Position | Circuit | Function |
|------|----------|---------|----------|
| IBC-1 | Top tier, near column | Blue (clean supply) | Primary clean water supply for spray bar |
| IBC-2 | Top tier, far column | Blue (clean supply) | Secondary supply, filled in parallel with IBC-1 from the X1 fill tee |
| IBC-3 | Bottom tier, near column | Brown (recycled) | Wash water buffer — filtered and recycled back to Blue |
| IBC-4 | Bottom tier, far column | Black (waste) | Contaminated water sealed for off-site disposal |

### 2.3 Layout

| Parameter | Value |
|-----------|-------|
| Near column Yd | 30–1,046mm (pushed to near/pinhole wall, 30mm clearance) |
| Far column Yd | 1,316–2,332mm (pushed to far wall, 30mm clearance) |
| Column X range | 4,674–5,893mm (right-justified to sealed end wall) |
| Plumbing corridor | Yd=1,046–1,316mm (270mm gap between columns) |
| Single IBC height | 1,168mm |
| Stacked height (2 totes, direct-stack cage-on-cage) | <!-- BEGIN fact:ibc_stack_height_mm -->2,336<!-- END fact:ibc_stack_height_mm -->mm (2 × 1,168mm — no deck/mat between tiers) |
| Ceiling clearance | <!-- BEGIN fact:ibc_ceiling_clearance_mm -->52<!-- END fact:ibc_ceiling_clearance_mm -->mm (2388 − 2,336mm) — tight but transport-validated (see [weight report](weight-distribution-report.md)) |

---

## 3. Stacking Frame — Restraint-Only Deep 4-Leg Box

### 3.1 General Arrangement

The 1,000L caged totes **direct-stack cage-on-cage** — the upper tote's pallet base
bears directly on the lower tote's cage top, leaving only <!-- BEGIN fact:ibc_ceiling_clearance_mm -->52<!-- END fact:ibc_ceiling_clearance_mm -->mm of ceiling headroom.
There is no room for (and no need for) a load-bearing platform deck between tiers, so
the frame is **restraint-only**: it carries no vertical service load, it only keeps the
totes from moving during transport.

The frame is a **deep 4-leg box** at the IBC front, spanning the plumbing corridor: a
**front pair** of full-height 2×2×0.120in uprights at the corridor mouth and a **back pair**
~450mm behind, tied by butt-jointed top and bottom rings, on four floor-flange feet (the
front feet reach ~25mm under the tray edge). Transport restraint is provided by:

- **front retaining bars** across each column at the IBC front that stop
  the totes sliding out the open front, their wall ends dropped into Simpson-style joist
  hangers;
- **Weld-on lashing rings** on the front bars, with ratchet straps over each stack;
- the totes are otherwise trapped by the container side walls (30mm gap) and sealed end wall.

The box carries the **Corridor Plumbing Panel** (pumps) and its **drain-riser backing spine**
on the back uprights, and gives the right-walkway cantilever arms their clamp point on the
front uprights.

![TBS-001 IBC Stacking — Sheet 1: Cross-Section Elevation](assets/ibc-stacking-sheet1.png)

![TBS-001 IBC Frame — Sheet 1: Front Elevation](assets/ibc-frame-sheet1.png)

### 3.2 Frame Specification

| Parameter | Value |
|-----------|-------|
| Material | 2×2×0.120in RHS mild steel (A500 Grade B) |
| Uprights | 4 full-height (deep 4-leg box: front pair at the corridor mouth + back pair ~450mm behind), tied by butt-jointed top + bottom rings |
| Floor anchorage | 4 × 150 × 150 × 12mm flange-plate feet, 4 × M12 anchors each (front feet reach ~25mm under the tray) |
| Front retaining bars | **8 × 50×20×3 RHS** — **two per tote face** (upper + lower), both seated in the 25mm gap to the film rail, wall → upright per column. Doubled from one to carry the loaded-transport case (§3.4) |
| Anti-slip matting | **4 × certified anti-slip mat (μ ≥ 0.6)** under the tote interfaces (2 on the floor + 2 on the lower-tote cage tops) — raises the sliding friction that credits against the forward thrust (§3.4) |
| Wall joist hangers | **8 × identical 2-bolt Simpson-style U-pocket** — one per bar (the pair uses identical hangers for fab simplicity), each **through-bolted (2 × M12×65) to an exterior backing plate** (M12×65 spans the 8mm plate + corrugation + 4mm hanger grip). Wall penetrations unchanged at 16 |
| Exterior backing plates | 8 × 60 × 205 × 8mm steel (one per hanger), on the **outside** of the container side walls (hex heads outside) — spread the totes' transport thrust into the thin corrugated wall so the bolts can't pull through |
| Weld-on lashing rings | 8 on the front bars (4 per tier); 3,333 lb (~1,512 kg) assembly WLL (2" strap-limited), 2 straps per stack |
| Panel mount | the box carries the Corridor (pump) Plumbing Panel + drain-riser spine on the back uprights, and the right-walkway cantilever arms on the front uprights |
| Frame weight | ~123 kg (4 uprights + rings + 4 feet + 8 front bars + 8 hangers + 8 exterior plates + rear-panel brackets + 4 mats — see [weight report](weight-distribution-report.md)) |
| Joints | Welded (fillet weld throughout — sizes scheduled in §3.5) |

![TBS-001 IBC Frame — Sheet 2: Side Elevation](assets/ibc-frame-sheet2.png)

![TBS-001 IBC Frame — Sheet 3: Plan View at Platform Level](assets/ibc-frame-sheet3.png)

### 3.3 Direct-Stack Junction

The upper tote bears directly on the lower tote's galvanized cage top rail
(no platform, mat or lip) — the totes' normal warehouse cage-on-cage stacking interface,
rated for a full upper tote.

### 3.4 Structural Validation (transport restraint) — EN 12195-1:2010

The frame carries **no vertical service load** (the totes stack on themselves), so there is no
platform-beam bending case. The governing case is **transport restraint**: the totes must not shift
when the container is moved by road — and, because the camera is designed to run **self-contained**
(disconnected from mains water and power), it is transported with **water aboard**. The restraint is
therefore designed for the loaded case, not just the drained one.

**Load basis — [EN 12195-1:2010](https://cdn.standards.iteh.ai/samples/32961/4592590bcf194f1a8ffa917a5db7d258/SIST-EN-12195-1-2011.pdf)** (the European cargo-securing standard for road transport). Design accelerations: **0.8 g forward** (braking), 0.5 g rearward, 0.5 g lateral, with **1.0 g vertical** in the friction term; safety factor **f_s = 1.25 forward / 1.1 otherwise** ([Table 2 + §5](https://hvttforum.org/wp-content/uploads/2019/11/Johansson-International-guidelines-on-safe-load-securing-for-road-transport.pdf)). A blocking (positive-restraint) device must carry **BC ≥ f_s · m · g · (c − μ·c_z)** — the inertia demand less the friction credit. Sliding friction **μ = 0.20** bare (the conservative fallback for an unlisted plastic-pallet-on-steel pairing), rising to **μ = 0.60** with certified anti-slip matting ([EN 12195-1 Annex B](https://res.jedermann.de/data/downloads/KB029-2_Gesamtdokument.pdf)). Forward (0.8 g) governs: it is the only direction with no wall to trap the totes (the side walls trap laterally, the sealed end wall rearward). The design mass is a full top-tier Blue tote, **965 kg** (65 kg tare + 900 L). Computed in [`ibc_frame_load.py`](https://github.com/alvinr/tbs/blob/main/src/generators/ibc_frame_load.py).

The forward thrust is blocked by the **front retaining bars**, seated in the 25mm film-rail slot — which limits each bar to a **20mm depth in the load direction** (weak-axis bending). A single bar per tote face fails this case (bending SF **0.79**). The design therefore uses **two bars per tote face** sharing the thrust, plus certified anti-slip matting to cut the demand:

| Element | Demand (loaded) | Capacity | SF (bar-alone) | SF (+ anti-slip mat) |
|---|---|---|---|---|
| Front retaining bar — bending (2 × 50×20×3, weak-axis) | 464 N·m | 738 N·m | **1.59** | **4.77** |
| Wall-hanger bolts (2 × M12×65 Gr.8.8 per bar) | 1,775 N | 80,900 N | 46 | — |
| Wall bearing (60×205×8 plate, 1.6mm wall, 2 holes) | 1,775 N | 15,400 N | 8.7 | — |
| Bar → upright cleat (2 × M12×40 A2, shear) | 1,775 N | 70,800 N | 40 | — |
| Lashing strap — vertical tie-down (2 straps/stack) | 9,467 N | 29,650 N | 3.1 | — |

The two bars give **defense in depth**: as positive blocking they pass on their own (**SF 1.59**, mat degraded or absent); with the anti-slip mat the friction credit lifts the margin to **SF 4.77**. Everything downstream of the bars is comfortably strong — the wall-hanger bolts, the corrugated-wall bearing (backing-plate-spread), the cleat bolts, and the tie-down straps all clear SF ≥ 8. In the **drained** transport state (site-filled water, totes empty) every element clears SF ≥ 12.

- **Front retaining bars** (two per tote face, 50×20×3 RHS, ~1,046mm span) share each tote's forward (−X) thrust into the floor feet + wall hangers.
- **Wall joist hangers** — **one identical 2-bolt hanger per bar** (8 total; the two bars of a pair use identical hangers for fabrication simplicity), each **through-bolted (2 × M12×65) to a 60×205×8mm exterior backing plate** on the outside of each side wall — the plate spreads the bolt load so the thin corrugated wall cannot pull through. Total wall penetrations stay at 16 (8 hangers × 2 bolts = the old 4 × 4). M12×65 (partial thread) spans the ~42–54mm sandwich (8mm plate + corrugation + 4mm hanger); the front-bar → upright cleats stay M12×40 (short grip).
- **Anti-slip matting** (certified μ ≥ 0.6) under each tote interface is the primary friction lever — it triples the effective margin and directly answers the "totes must not shift" requirement.
- **Weld-on lashing rings + 2 straps/stack** (3,333 lb / ~1,512 kg per strap) provide vertical tie-down against the forward-tipping mode of the tall loaded stack (CG Z≈1,345mm) and supplement lateral restraint; the totes are otherwise wall-trapped.
- **Floor feet** (150×150×12, 4 × M12 each) anchor the uprights against uplift and transfer loads into the slab.

---

## 4. Securing for Transport

### 4.1 Weld-On Lashing Rings

| Parameter | Value |
|-----------|-------|
| Quantity | 8 total (4 per tier) |
| Type | 1½" (38mm) ID weld-on tie-down ring, ½" thick, zinc-plated steel |
| Working load limit | 6,600 lb (2,994 kg) ring — assembly strap-limited to 3,333 lb (~1,512 kg) |
| Mounting | Fillet-welded directly to the front retaining bars (integrated weld base — no separate plate) |
| Supplier | McMaster-Carr #3028T31 |

### 4.2 Ratchet Straps

| Parameter | Value |
|-----------|-------|
| Type | 2" (50mm) ratchet strap (Keeper 82827) |
| Working load limit | 3,333 lb (~1,512 kg) |
| Routing | ring to ring, over IBC top, 1 strap per tier per side |
| Total straps | 4 (2 per tier) |
| Pre-transport | Tighten all straps; re-check tension after 50 km |

### 4.3 Wall Trapping

There is no anti-rotation lip. The direct-stacked totes are trapped
laterally by the container side walls (30mm gap each side) and the sealed end wall;
the front retaining bars + lashing-ring ratchet straps restrain the open front and
provide vertical tie-down. Together these restrain both tiers in all six DOF.

### 4.4 Anti-Slip Matting

| Parameter | Value |
|-----------|-------|
| Quantity | 4 (one under each tote: 2 on the container floor, 2 on the lower-tote cage tops) |
| Type | Certified anti-slip cargo matting, **μ ≥ 0.6** ([EN 12195-1 Annex B](https://res.jedermann.de/data/downloads/KB029-2_Gesamtdokument.pdf)) — cut to the tote pallet footprint |
| Purpose | Raises the sliding friction that credits against the forward thrust (μ 0.2→0.6), tripling the front-bar margin (SF 1.59→4.77, §3.4) — the primary "totes don't shift" lever |
| Note | Must be a **tested/certified** μ ≥ 0.6 product; untested rubber caps at μ 0.2 |

![TBS-001 IBC Stacking — Sheet 2: Fastening Details](assets/ibc-stacking-sheet2.png)

---

## 5. Drain Valve Access

The bottom-tier drain valves (DN50 butterfly, corridor-facing) are reached
directly from the **open corridor front** — with the Corridor Plumbing Panel moved forward and
no load-bearing base frame, there are no removable access gates. The operator reaches in
from the right walkway.

---

## 6. External Bulkhead Ports

Three 2" NPT bulkhead ports penetrate the sealed end wall on the container
centerline — **X1** (Blue fill), **X3** (Brown drain), and **X4** (Waste drain) —
so all four totes fill and drain without opening the cargo doors. X1 gravity-feeds
an internal tee that side-enters both Blue totes near the top, so one external hose
fills both. Each penetration is backed by a welded wall reinforcing plate that
spreads its load into the corrugated wall (the same approach as the frame's
exterior backing plates, [§3.2](#32-frame-specification)).

The port elevations are the diagram-of-record (see [§8 Sheet 3](#8-engineering-drawings)).
The bulkhead fittings, camlock, and seals are specified in the
[Water System Report](water-system-report.md) §5 and §7; the bulkhead BOM,
including the reinforcing plates, is in the
[master shopping list](master-shopping-list.md). (These end-wall ports are
distinct from the two equipment **Plumbing Panels** — Corridor and Pinhole Wall —
in [§7](#7-internal-plumbing).)

![TBS-001 IBC Stacking — Sheet 3: External Bulkhead Ports Elevation](assets/ibc-stacking-sheet3.png)

---

## 7. Internal Plumbing

All internal supply and return lines route through the <!-- BEGIN fact:corridor_width_mm -->270<!-- END fact:corridor_width_mm -->mm plumbing corridor
between the near and far IBC columns, reaching each tote's corridor-facing DN50
butterfly valve (S60×6 thread). The pipe specification, the per-circuit routing
(X1 Blue gravity-fill teed to both top totes, X3 Brown and X4 Waste pumped drains,
and the recycle returns), and the valve schedule are specified in the
[Water System Report](water-system-report.md) §4–§5 and §7. The pumps and
diverter valves that drive those circuits — on the **Corridor Plumbing Panel**
(plywood, at the front (cargo-door) mouth of the corridor, bolted to the
deep-box frame, see [§3.2](#32-frame-specification)) — together with the
3-stage filter bank on the **Pinhole Wall Plumbing Panel** are specified in the
[Plumbing Report](plumbing-report.md). This report treats the corridor plumbing
and both panels only as loads the stacking frame carries.

![TBS-001 IBC Stacking — Sheet 4: Internal Plumbing Plan View](assets/ibc-stacking-sheet4.png)

![TBS-001 IBC Stacking — Sheet 5: Internal Plumbing Elevation](assets/ibc-stacking-sheet5.png)

---

## 8. Engineering Drawings

Eight construction drawings cover the IBC system across two drawing sets. They are shown inline in the
relevant sections above; the full set is collected here and in [Engineering Diagrams](engineering-diagrams.md).

<!-- brochure:skip -->

### IBC Stacking & Securing (5 sheets)

**Sheet 1 — Cross-section elevation: 2-tier direct-stack, restraint deep 4-leg box, front retaining bars + wall hangers, direct-stack junction, <!-- BEGIN fact:ibc_ceiling_clearance_mm -->52<!-- END fact:ibc_ceiling_clearance_mm -->mm clearance**
![TBS-001 IBC Stacking — Sheet 1](assets/ibc-stacking-sheet1.png)

**Sheet 2 — Fastening details: front-bar→upright cleat + lash eye, wall joist hanger, ratchet lashing over the stack**
![TBS-001 IBC Stacking — Sheet 2](assets/ibc-stacking-sheet2.png)

**Sheet 3 — External bulkhead ports: Sealed end wall elevation with 3× ports**
![TBS-001 IBC Stacking — Sheet 3](assets/ibc-stacking-sheet3.png)

**Sheet 4 — Internal plumbing plan view: IBC layout, pipe routing, valves, Corridor Plumbing Panel**
![TBS-001 IBC Stacking — Sheet 4](assets/ibc-stacking-sheet4.png)

**Sheet 5 — Internal plumbing elevation: Pipe routing from IBCs to bulkhead unions**
![TBS-001 IBC Stacking — Sheet 5](assets/ibc-stacking-sheet5.png)

### IBC Support Frame Fabrication (3 sheets)

**Sheet 1 — Front elevation: deep-box uprights (front pair, back pair 450mm behind), floor feet, front retaining bars + wall hangers + weld-on lashing rings, direct-stack junction**
![TBS-001 IBC Frame — Sheet 1](assets/ibc-frame-sheet1.png)

**Sheet 2 — Side elevation: deep 4-leg box (front + back uprights + top/bottom rings) + front bars (end-on) + walkway cantilever arm**
![TBS-001 IBC Frame — Sheet 2](assets/ibc-frame-sheet2.png)

**Sheet 3 — Plan view: deep 4-leg box (4 legs + ring perimeter) + retaining bars + 4 floor feet + IBC footprints + corridor + walkway arms**
![TBS-001 IBC Frame — Sheet 3](assets/ibc-frame-sheet3.png)

<!-- brochure:endskip -->

Full drawings also appear in [Engineering Diagrams](engineering-diagrams.md) §15
(stacking) and §17 (frame fabrication).

---

## 9. Parts List

### 9.1 Stacking Frame

<!-- BEGIN parts:ibc-frame -->
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 2×2×0.120in steel SHS (6 m bulk lengths) | Deep 4-leg box uprights (front + back pair) + top/bottom rings + front retaining bars + panel-mount rail (~24 m; front retaining bars DOUBLED to 8 (2/tote face, 50×20×3, ~8.8 m) after the EN 12195-1 loaded-transport case — ibc_frame_load.py; the 50×20×3 bars are a separate section from the 2×2 uprights, lumped here as bulk steel pending the Phase-D split). MATERIAL = 2×2×⅛in A500 square tube (US equiv, confirmed 2026-08-01). SOURCING: full 6m/20-24ft sticks minimize splices but ship only by freight — online cut-to-size shops cap at 96in (UPS max: AllMetals/InchOfMetal 96in, Speedy $7.27/ft cut-retail ≤90in). So the ~$120-180 (4×$30-45) est is realistic BULK full-length pricing (~$1.50-2.50/ft); firm it from a local steel-yard / MetalsDepot 24ft freight quote — NOT an online cut-to-size lookup (which overprices bulk ~3×). | 4 ea | Metal Supermarkets | $120–$180 |
| 12mm steel plate, 150 × 150 cut | Deep-box upright floor flange feet (one per leg; front feet reach under the tray) | 4 ea | Metal Supermarkets | $20–$40 |
| 4mm folded plate | Simpson-style U-pocket wall joist hangers — 8 IDENTICAL 2-bolt hangers, one per front retaining bar (the pair uses identical hangers for fab simplicity — Alvin 2026-08-14). Each through-bolted (2× M12×65) to its own exterior 60×205×8 backing plate on the outside of the container side wall. Wall penetrations unchanged at 16 (8 hangers × 2 = old 4 × 4). | 8 ea | Local fab | $60–$100 |
| [Weld-on lashing ring, 1½" ID](https://www.mcmaster.com/3028t31/) (3028T31) | Zinc-plated steel weld-on tie-down rings — 1½" (38mm) inside × ½" thick, 6,600 lb WLL; fillet-welded to the front retaining bars (4 per tier × 2 tiers). Integrated weld base — no separate mount plate. Ring (6,600 lb) exceeds the 2"-strap-limited 3,333 lb (~1,512 kg) assembly WLL. | 8 ea | McMaster-Carr | $40 |
| [2" (50mm) ratchet strap, 3,333 lb WLL](https://www.homedepot.com/p/331257450) (82827) | Transport securing, over each stack (2 per stack × 2 stacks). Keeper 82827 heavy-duty 2"×27ft, 3,333 lb (~1,512 kg) WLL / 10,000 lb break — width corrected 25mm→50mm (a 1" strap can't hold the 1,100 kg the restraint needs). EN 12195-1 vert tie-down SF 3.1 loaded (ibc_frame_load.py). | 4 ea | Home Depot | $68 |
| Certified anti-slip cargo matting (μ≥0.6) | Certified anti-slip rubber matting under each tote interface (4: 2 on the container floor + 2 on the lower-tote cage tops). Raises the sliding friction μ 0.2→0.6 per EN 12195-1 Annex B, cutting the front-bar forward-blocking demand ~3× (bar SF 1.59 bar-alone → 4.77 with mat; ibc_frame_load.py). Cut to the tote pallet footprint (~1.0×1.2 m). REQUIRES a certified/tested μ≥0.6 product (untested rubber caps at μ 0.2). | 4 ea | Uline / cargo-securing supplier | $40–$80 |
| [Self-drilling structural screw, #14×3¼″ winged, 410 SS](https://www.fastenersplus.com/products/14-x-3-1-4-self-drilling-flat-head-screw-with-wings-410-stainless-steel-pkg-100) (F14C325FDC) | 4 deep-box flange feet × 4 each. Self-drills the 6mm foot plate + 28mm plywood and taps the ~4mm steel crossmember — LAND EACH FOOT OVER A CROSSMEMBER (~450mm centers). Wings ream the plate/ply clearance then snap off at the steel. 410 SS (martensitic — self-drills steel; 316 can't). The IBC dead load bears in compression on the floor; the screws resist sliding/uplift only. Through-bolt 316 + backing nut instead where a crossmember underside is reachable. $1.02/ea (100-pk). | 16 ea | Fasteners Plus / ASMC | $16 |
| [M12×40 hex bolt, 18-8 SS](https://www.mcmaster.com/92314A744/) (92314A744) | Front-bar → upright angle cleats (2 each × 4 bars = 8). Short grip (bar + cleat + upright flange) → M12×40 fully threaded is correct. McMaster 92314A744: M12×1.75 × 40mm 18-8 stainless hex head screw — confirmed vs the eng-specs PDF (M12×1.75, 40mm, 18-8 SS). $14.73/pack of 10 firm (2026-08-01; 8 used). (Wall-hanger through-bolts are the M12×65 below.) | 8 ea | McMaster-Carr | $12 |
| [M12×65 hex through-bolt, Grade 8.8 zinc, partial-thread](https://www.mcmaster.com/91280A728/) (91280A728) | IBC wall-hanger through-bolts (2 each × 8 hangers = 16) — through the corrugated side wall to the exterior 60×205×8 backing plate (hex heads outside). Grip = 8mm plate + ~30mm corrugation + 4mm hanger flange ≈ 42–54mm → M12×65 partial-thread (the fully-threaded M12×40 could not span it). $15.95/pack of 10 → 2 packs for 16. Pad with 1–2 M12 flat washers if the actual corrugation is <30mm. | 16 ea | McMaster-Carr | $26 |
| [M12 hex nut, plain](https://www.mcmaster.com/90591A181/) (90591A181) | Plain hex nut (inside the container) — M12×65 wall-hanger through-bolts (+ split lock washer). $12.78/pack of 50. Pitch M12×1.75 coarse — confirmed vs 90591A181 PDF 2026-07-29. | 16 ea | McMaster-Carr | $4 |
| [M12 flat washer, zinc](https://www.mcmaster.com/91166a290/) (91166A290) | Flat washers, M12×65 wall-hanger bolts — 2 functional + 2 shim/bolt (shims pad the grip if corrugation <30mm). $9.71/pack of 100. | 64 ea | McMaster-Carr | $6 |
| [M12 split lock washer, zinc](https://www.mcmaster.com/91202A246/) (91202A246) | Split lock washer under each nut — M12×65 wall-hanger bolts (plain nut + split = locked). $11.97/pack of 100. | 16 ea | McMaster-Carr | $2 |
| Steel backing plate 60×205×8mm | Exterior wall backing plates — 8 identical, one per 2-bolt hanger — flat 60×205×8mm steel on the OUTSIDE of the container side wall (hex heads outside), 2× M12 holes; spreads the totes' transport thrust into the thin corrugated wall so the through-bolts can't pull through. | 8 ea | Metal Supermarkets | $32–$56 |
| Welding / fabrication (frame assembly) | ~14–20 hrs labor (deep 4-leg box — the ring/back-upright welds sit at the upper end of the range) | 1 lot | Local fab | $688–$1,018 |
| Primer + paint | Anti-corrosion coating | 1 lot | Hardware store | $30–$50 |
| **Ibc-Frame total** | | | | **$1,163–$1,697** |
<!-- END parts:ibc-frame -->

### 9.2 IBC Totes

| Item | Specification | Qty | Est. cost (USD) |
|------|--------------|-----|----------------|
| 1,000 L caged composite IBC tote (Schütz Ecobulk MX 1000 or equiv.) | New or reconditioned US 48×40 caged composite (~65 kg) | 4 | $300–$900 |
| **IBC subtotal** | | | **$300–$900** |

The corridor and bulkhead **plumbing parts** (pipe, valves, fittings, camlock,
bulkhead unions, reinforcing plates) are budgeted in the
[Water System Report](water-system-report.md) §8 and the
[master shopping list](master-shopping-list.md), not here — this BOM covers only
the stacking structure and the totes it restrains.

### 9.3 Cost Summary

| Assembly | Low estimate | High estimate |
|----------|------------|--------------|
| Stacking frame (restraint deep 4-leg box) | <!-- BEGIN costing:ibc-frame-low -->$1,163<!-- END costing:ibc-frame-low --> | <!-- BEGIN costing:ibc-frame-high -->$1,697<!-- END costing:ibc-frame-high --> |
| IBC totes (4×) | $300 | $900 |
| **Total** | **$1,280** | **$2,405** |

---

## 10. Maintenance Schedule

| Interval | Task |
|----------|------|
| Every use | Visually inspect ratchet strap tension before transport |
| Every 10 prints | Inspect IBC valve seals (DN50 butterfly) for drips; tighten or replace O-ring |
| Every 10 prints | Check external camlock fittings for cross-threading; clean dust caps |
| Every 6 months | Inspect lashing-ring welds for cracking; load-test straps |
| Every 6 months | Inspect lashing rings + ratchet straps for wear; re-tension straps |
| Annually | Inspect frame welds (all joints) for fatigue cracking |
| Annually | Touch up paint on frame where chipped or rusted |
| Annually | Inspect front-bar/wall-hanger bolts and upright floor-anchor bolts for loosening; re-torque to spec |
| Annually | Flush all internal pipes with clean water; inspect for biofilm |
| As needed | Replace camlock gaskets if leaking |
| As needed | Clean IBC interiors between circuit changes (bleach rinse + water flush) |

---

## 11. Sources

| Item | Source |
|------|--------|
| Schütz Ecobulk MX 1000 L IBC | [Schütz product catalog](https://www.schuetz-packaging.net/schuetz-usa/en/ibcs/ecobulk/ecobulk-mx/) — US 48×40 composite tote, DN50 valve, UN31HA1/Y (all four totes are this size; "600 L"/"640 L" are fill levels, not tote sizes) |
| Weld-on lashing ring | [McMaster-Carr #3028T31](https://www.mcmaster.com/3028t31/) — 1½" ID, ½" thick, 6,600 lb WLL |
| Plumbing fittings, pipe, valves, camlock, pumps | Specified and sourced in the [Water System Report](water-system-report.md) §11 and [Plumbing Report](plumbing-report.md) §11 |
| Water system architecture | [Water System Report](water-system-report.md) §3 |
| IBC layout and stacking | [Equipment Layout Report](equipment-layout-report.md) §5 |
| Frame fabrication drawings | [§8 — Engineering Drawings](#8-engineering-drawings) (this report) · [All Diagrams](all-diagrams.md) |
| Plumbing panel specification | [Plumbing Report](plumbing-report.md) |
