<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Equipment Layout — Shadow-Free End-Zone Design

## 1. Design Principle — Shadow-Free End Zones

The optical cone from the pinhole narrows as it approaches the pinhole wall and
widens as it approaches the film plane. Any equipment placed inside the cone casts
a shadow on the film plane, producing an unexposed void in the image.

**Solution:** Reduce the active film plane from the full <!-- BEGIN fact:container_interior_length_mm -->5893<!-- END fact:container_interior_length_mm -->mm container width
to a <!-- BEGIN fact:film_plane_width_mm -->4499<!-- END fact:film_plane_width_mm -->mm span. This creates two **provably shadow-free end
zones** — one at each end of the container — where equipment can be placed at any
depth without entering the optical cone. The right end zone contains a 2×2 IBC stack,  leaving the left zone to contain the light trap drum.

### Zone Definitions

| Zone | X range | Shadow-free? | Equipment assigned |
|------|---------|--------------|--------------------|
| **Left end zone** | 0–150mm | YES at all depths | Light trap drum, hinged panel (stepped) |
| **Optical zone** | 150–4649mm | NO | Film plane, rails, processing tray, perimeter walkway |
| **Right end zone** | 4649–5893mm | YES at all depths | IBC tanks (2×2 stack: 2× Blue, 1× Brown, 1× Waste) |
| **Pinhole wall face** | Y=0 surface | YES (cone collapses to point) | Electrical panel, battery, pump |

---

## 2. Equipment Positions

Overall floorplan can be seen below. Its essentially split into three areas, left, center and right which are discussed below.

**Floor plan**
![TBS-001 Container Floor Plan — End-Zone Layout](assets/container-floorplan.png)

### 2.1 Left End Zone — X=0–150mm

| Item | X (mm) | Yd (mm) | H (mm) | Notes |
|------|--------|---------|--------|-------|
| Hinged panel (stepped) | 0–40 (corner) / 0–120 (center) | 0–2,362 | 0–<!-- BEGIN fact:film_plane_height_mm -->2388<!-- END fact:film_plane_height_mm --> | Stepped profile: 40mm corners, 120mm center (drum housing). Swings ~56° about the Ø89 pivot for transport. |
| Light trap drum | −375–375 | 806–1,556 (centered at CW/2=1181mm) | 0–2,200 | Centered at X=0 (spans container wall); integrated into panel center zone; rotary drum entry |

### 2.2 Pinhole Wall Face — Y=0 surface mounted

| Item | X (mm) | H (mm) | Notes |
|------|--------|--------|-------|
| Evaporative cooler | 700–1,300 | ground | Hessaire MC18M, 120V AC 85W (97W on 12V bus via inverter); ground-placed outside, flex duct to wall stub at Z=1900mm |
| Cooler inverter (Cct E) | 1,910–2,030 | 1,180–1,415 | Victron Phoenix 12/375 GFCI, wall-mounted below the EP (12V→120V for the cooler) |
| Electrical panel | 1,910–2,210 | 1,500–2,100 | IP65, wall-mount (stacked above the battery bank; clears the upper transport-stay anchor). rev11: dropped 150mm (was Z1,650–2,250) — originally to clear the film-plane brace top beam; that brace cage is now retired for wall-seat saddles, but the EP is kept at this height |
| Battery bank (2× 100Ah LiFePO4, each 330×172×214mm) | 1,540–2,220 | 150–364 | Wall shelf below panel; side-by-side, clears the optical cone |
| Solar charge controller | Within panel | — | Mounted inside enclosure |
| Pump manifold (3 pumps: P-01, P-02, P-04) | 2,400–2,700 | 200–600 | Wall-bracket |
| Cable trunking | Along wall face, H=1800mm | — | Full length |

### 2.3 Optical Zone — X=150–4649mm

Rail slots in floor/ceiling at X=150 and X=4,649. Film plane frame
spans this zone at depth Y=2262mm (nominal far position).

| Item | X (mm) | Yd (mm) | H (mm) | Notes |
|------|--------|---------|--------|-------|
| Processing tray (2 panels, 304 SS) | 170–4,629 | 80–2,280 | 0–50 | 50mm rim; 20mm clearance to film plane rails; sump well at X=2,399, Yd=80 with P-04 suction pickup to 3W-DV-02. On tapered HDPE shim strips. Permanently installed. |
| Perimeter walkway (4 sections, removable) | 170–4,629 | 0–300 / 2,062–2,362 | 0–130 | 300mm wide, 130mm deck height (raised +50; 115mm support + 15mm grate). Near/far: wall-cantilevered 8mm gusset brackets at 457mm centers. Right: brackets on angle iron welded to end wall. Left: removable lift-out grate on 5 floor-leg cantilever brackets bolted to bare floor outside the tray (arms to X=470, 3 extended to X=770 on the punch-out; the panel occupies this end wall), 15mm grating. Left corners: butt joint (no miter). No tray contact (left brackets bolt to bare floor outside the tray). Floor-leg arm (Z=75–115) clears the 50mm tray rim and the Z60 spray bar by 15mm. |

The processing tray sits below the film plane carriage blocks (minimum Z=140mm at maximum 40° tilt; the lower max angle only increases clearance), providing 90mm clearance above the tray rim. The tray does not contact or interfere with the HGR20 rail channels at X=150 and X=4,649.

### 2.4 Right End Zone — X=4649–5893mm

2×2 IBC stack — right-justified flush to the far end wall. Four IBCs in two
columns (25mm clearance from zone boundary), separated by a
270mm plumbing corridor between near and far columns. IBC wall clearance
is 30mm on each side.

| Item | X (mm) | Yd (mm) | H (mm) | Notes |
|------|--------|---------|--------|-------|
| Blue IBC-1 (800L fill, top near) | 4,674–5,893 | 30–1,046 | 1,168–2,336 | Near column top; restraint frame |
| Blue IBC-2 (800L fill, top far) | 4,674–5,893 | 1,316–2,332 | 1,168–2,336 | Far column top; restraint frame |
| Brown IBC-3 (recycle buffer, bottom near) | 4,674–5,893 | 30–1,046 | 0–1,168 | Near column bottom; recycled wash/fix |
| Waste IBC-4 (waste, bottom far) | 4,674–5,893 | 1,316–2,332 | 0–1,168 | Far column bottom; sealed waste collection |

---

## 3. Floor Plan and Line-of-Sight Diagrams

**Optical line-of-sight**

![TBS-001 Optical Line-of-Sight Clearance — New Layout](assets/line-of-sight.png)

The line-of-sight analysis confirms zero equipment items intersect the optical
cone in either the plan (top-down) or elevation (side) view.

---

## 4. Why IBC Y-Stacking (Front-to-Back)

In the current layout the entire right end zone is
X-clear from X=4649mm to the end wall — all four tanks occupy the same X column
in a 2×2 arrangement (two columns along Y, two tiers high).

| Arrangement | X span used | Max Y depth |
|-------------|------------|------------|
| Old (side-by-side X) | 2400mm | 1116mm |
| **New (Y-stacked, right-justified)** | **1219mm** | **2302mm** |

The 2×2 stack gives a 1219mm X footprint (= IBC cage width), right-justified to
the far end wall. The zone itself is only 1244mm wide (X=4649–5893mm), so the
IBCs fit with 25mm clearance on the zone boundary side. The two columns are
separated by a 270mm plumbing corridor, with
30mm wall clearance on each side.

---

## 5. IBC Stacking Frame — Design Specification

A welded mild steel **restraint-only** frame holds the 2×2 IBC stack (4× 1000L
caged composite totes — two columns, two tiers each, direct-stacked) as a single
unit. The totes stack cage-on-cage, so the frame does not carry vertical load — it
only restrains them for transport (front retaining bars + D-ring lashing).

| Item | Specification |
|------|--------------|
| Frame material | 50×50×3mm RHS mild steel |
| Frame type | RESTRAINT-ONLY single **front portal** — the 1000L caged totes direct-stack cage-on-cage (no load-bearing deck), so the frame only restrains them |
| Uprights | 2 full-height corridor uprights (Yd 1046/1266) at the IBC front (X≈4734) on 150×150×12mm floor flange feet (4× M12 each); define the 270mm plumbing corridor |
| Front retaining bars | 4× 50×20×3 RHS at the IBC front (Z560 + Z1760), seated in the 25mm gap to the film rail — stop the totes sliding out the front; each bar's wall end drops into a Simpson-style joist hanger (×4) |
| Wall attachment | each joist hanger is through-bolted (4× M12) to a 100×135×8mm **exterior** backing plate (×4, hex heads outside) that spreads the load into the thin corrugated side wall |
| Lashing points | 25mm D-ring holders on the front bars (1,100kg WLL); ratchet straps pass over each stack and tie down to them |
| Total stacked height | 2336mm (2× 1168mm direct-stack) — 52mm ceiling clearance |
| Panel mount | the front portal also carries the (forward) wet-end equipment panel and the right-walkway cantilever arms |
| Surface finish | Gray oxide primer + flat black powder coat (interior) |
| Approx. weight | ~178kg (uprights + feet + front bars + hangers + exterior wall plates + panel mount) |
| Approx. cost | USD <!-- BEGIN costing:eq-ibc-frame-cost -->$955–$1,455<!-- END costing:eq-ibc-frame-cost --> (local mild steel fabrication) |

**Why 1000L caged composite (all four totes):**

All four positions use the 275-gal (≈1000 L) caged composite tote — the only
food-grade, 48×40-footprint tote stocked.
"600 L" / "1000 L" are **fill levels**, not tote sizes.

| IBC type | H (mm) | Stacked pair | Ceiling clearance |
|----------|--------|--------------|-------------------|
| **1000L caged composite** | **1,168** | **2336mm** | **52mm** |

The 52mm headroom is tight but **transport-validated**: the loaded-transport CG sits at
Z=1,306mm (static sideways tip threshold ≈42°, ≈20% of the ISO gross limit) — see the
[weight-distribution report](weight-distribution-report.md).

**Raw material suppliers:**

| Item | Supplier | Notes |
|------|----------|-------|
| 50×50×3mm RHS mild steel | Pacific Coast Steel, Santa Fe Springs CA | A500 Grade B; ~$4/linear foot |
| D-ring lashing holders (×4) | McMaster-Carr #3641T29 | 1,100kg WLL per ring |
| M12 bolts (wall-hanger through-bolts ×16 + front-bar cleats) | McMaster-Carr or local hardware | SS A2-70; M12×80 through-bolts for the exterior plates |
| Simpson-style wall joist hangers (×4) | Simpson Strong-Tie or local | folded 4mm plate, through-bolted to exterior backing plate |
| Exterior wall backing plates (×4) | Metal Supermarkets / local | 100×135×8mm steel, hex heads outside |

---

## 6. Left End Zone — Simplified Layout

The left end zone contains only the light trap drum and the hinged panel — providing
unobstructed egress at the cargo door end.

### 6.1 Stepped Panel and Swing Pivot (Transport Mode)

The hinged panel has a stepped profile: 40mm thick at the corner zones and 120mm thick at the center zone
where the light trap drum is mounted. For transport the panel + drum SWING ~56° about a
vertical Ø89×8mm CHS pivot post (sharing the film-plane far-left upright),
carrying the punch-out bay inboard of the door plane. Two narrow strips stay fixed at the
door plane; the cargo doors close
outboard of the fixed near strip.

| Position | Description | Doors clear? |
|----------|-------------|-------------|
| Operational (0°) | Panel closed at the door plane; the B2 punch-out bay protrudes ~890mm outside | No — the doors stay open during camera operation |
| Transport (swung 56°) | Panel + drum revolved about the pivot, swept inboard | Yes — true minimum clearance to the closed door is +59mm |

A fixed welded door frame (50×50×3mm RHS) provides the EPDM seal landing. The panel seals
against this frame with the Southco C2-33 cam latches and 20mm EPDM gaskets in the closed
(latched) position; the latches release to free the seals before the swing.

#### 6.1.1 Swinging Panel Light Seal Design

The swinging panel seals against the fixed door frame in its operational (closed)
position via five light-tight paths — panel perimeter, the two swing-cut seals, the
bottom and top frame seal lips, and the Ø900 housing-surround ring — all 20mm EPDM,
compressed by the four Southco C2-33 cam latches and released before the swing. See
**[Hinged Panel Report §6 — Light Seal Design](hinged-panel-report.md)** for the full
per-path seal table and the dark-adaptation verification check.

### 6.2 Evaporative Cooler Transport Stowage

The evaporative cooler (**Hessaire MC18M**, 559×305×711mm) sits on the ground outside the container during operation, connected to the wall penetration via Ø200mm flex cord and powered from the interior inverter (Circuit E, 120V AC). It must be stowed inside the container for transport.

**Stowage position:** On the near walkway grating in the wide section. The cooler sits on a 12mm plywood base plate (559×305mm) that distributes the load across the grating and prevents the housing from catching in the grate openings. The wide section (500mm) fully contains the 305mm cooler depth with ~195mm clearance — no overhang into the processing tray zone. The lighter (16 lb) unit also eases the handling.

**Securing:** Two 25mm ratchet straps loop over the cooler and hook to the nearest cantilever bracket arms. Two aluminum angle cleats (25×25×3mm, 100mm long) screwed to the base plate prevent lateral sliding.

| Parameter | Value |
|-----------|-------|
| Stowage zone | X=1450–2009mm, Yd=0–305mm (near walkway wide section) |
| Cooler footprint | 559×305mm (long axis along X) |
| Cooler height on grating | 711mm (top at Z=861mm) |
| Weight (dry) | ~7.3 kg (16 lb) |
| Securing | 2× ratchet straps to bracket arms |
| Base plate | 12mm ply, 559×305mm |
| Clearance to panel swing sweep | ~55mm (the swing reaches X≈1,395 in the near-walkway zone; the cooler starts at X=1,450 — moved deeper from X=1,200 in rev10 to clear the deeper swing) |

See [Walkway Diagram — Sheet 1](engineering-diagrams.md) for stowage position in plan view.

---

## 7. Plumbing and Electrical — Pinhole Wall Routing

All services route along the pinhole wall face. No conduit, pipe, or cable
runs through the optical zone.

**Plumbing manifold:** 3-pump distribution header (P-01 Blue spray bar, P-02 Brown
recycle, P-04 tray sump pickup) wall-mounted.
P-03 (waste evacuation) is mounted separately in the IBC plumbing corridor on
the X4 waste drain run, minimizing pipe length to the external drain port.
Hose runs drop vertically from manifold to IBCs in the right end zone. Maximum
hose run: ~5.5m (manifold to Brown IBC - along pinhole wall then
along right end wall).

**Electrical conduit:** 25mm PVC trunking along the
full container length on the pinhole wall face. Branch drops at each circuit
termination. All circuits ≤ 9m — within voltage-drop budget for 12V DC with
10 AWG wire.

**Solar inlet + shore power:** NEMA 5-15R weatherproof inlet on exterior of
pinhole wall at X=2399mm (pinhole side), H=400mm.

---

## 8. Water Capacity Summary

All four positions are identical 1000L caged composite IBCs — the 600L / 800L figures
are **fill levels, not tote sizes** (a 600L caged tote does not exist). Each tote's fill
swings between the two ends of a resupply cycle:

| IBC (identical 1000L tote) | Role | Camera ready | Supply exhausted |
|----------------------------|------|-------------:|-----------------:|
| Blue ×2 (stacked) | Clean wash supply | <!-- BEGIN fact:blue_supply_l -->1,600<!-- END fact:blue_supply_l -->L (2× 800L) | 0L |
| Brown | Recycled wash / fix buffer | 0L | 600L |
| Waste (sealed) | Waste collection | 0L | 600L |
| **Total in system** | — | **1,600L clean** | **1,200L used** |

A session starts camera-ready with both Blue totes full (800L each) and the Brown/Waste totes
empty; the supply is **exhausted when the Blue totes are empty**. The collection totes hold ~1,200L
while ~1,600L of Blue was consumed — the ~400L difference is open-process loss (wet-print carryout,
evaporation, unrecovered residual).

**Print capacity.** The <!-- BEGIN fact:blue_supply_l -->1,600<!-- END fact:blue_supply_l -->L nominal load supports **~<!-- BEGIN fact:prints_per_resupply -->13<!-- END fact:prints_per_resupply --> prints per resupply**; filling Blue toward the
tote's physical maximum (~1,900L) raises this to ~15–16 (transport-validated,
[Weight Report §4.4](weight-distribution-report.md)), and on-site top-up via the X1 / X3 / X4 bulkhead
ports extends it further. See [Processing System Report §4](water-system-report.md) for the full water
balance, max-fill, and top-up analysis, and the full water circuit design.

---

## 9. Egress Safety Assessment

When the hinged panel is opened 180° from the inside, the light trap drum (mounted
in the panel center zone, Yd=653–1709mm) swings outward with the panel. With the
waste drums eliminated (rev 5), the entire left end zone floor is clear.

### 9.1 Egress Gap

| Measurement | Value |
|-------------|-------|
| **Clear passage width** | **2362mm (93") — full container width** |
| At door frame (X=0) | ~2362mm (full frame opening) |
| Obstructions in egress path | None |

**Human factors reference:**

- Average male shoulder width: ~460mm (18")
- Standard doorway minimum (IBC/IRC): 762mm (30")
- Emergency egress minimum: 610mm (24")

The 2362mm passage exceeds all minimums by more than 3×. No equipment narrows
the egress path at any point. The elimination of waste drums from the left end
zone provides completely unobstructed access to the cargo doors.

### 9.2 Hinge Door Swing Clearance

The panel + drum swing about the Ø89 pivot — ~56° inboard for transport (the swing sweep reaches X≈1,395 near the door end) and open about the pivot for loading/egress. All fixed interior equipment sits inboard of the door-end swing sweep:

| Component | Position | In swing path? |
|-----------|----------|---------------|
| Light trap drum | Panel-mounted (center zone) | Moves with the panel |
| Fan B intake duct | Panel-mounted, Yd=365, H=600 (rev9/B2 swap — near pinhole wall) | Moves with the panel |
| Fan B cable | 1m coiled cable, ceiling service loop | Accommodates the ~56° panel swing (with slack) |
| Evap cooler duct stub | X=1,000, Yd=0 (wall penetration) | No — flush with wall |
| Electrical panel | X=1,910–2,210 | No — inboard of the X≈1,395 swing sweep |
| Battery bank | X=1,810–2,310 | No — inboard of the swing sweep |
| Pump manifold | X=5,140–5,240 (IBC corridor) | No — far inboard (IBC end) |
| Water lines | Pinhole wall (Yd=0), X=2,400+ | No — far inboard |

**Cargo door egress detail — panel open 180° outward:**
![TBS-001 Cargo Door Egress Detail](assets/container-floorplan-sheet2.png)

The light trap drum (900mm dia, center ~1181mm from hinge axis) sweeps through exterior space during 180° rotation. With waste drums eliminated, no interior equipment exists in the left end zone floor area.

**Conclusion:** No components obstruct egress. The left end zone is entirely clear at floor level, providing unobstructed single-person egress and full swing clearance at the cargo door end.

---

## 10. Summary

| Parameter | Old (colonnade) | New (end-zone) |
|-----------|----------------|----------------|
| Equipment zone concept | Yd=0–1220mm depth band | X=0–150mm and X=4649–5893mm end zones |
| Pinhole position | X=2946mm | **X=2399mm** (centered on active FP) |
| Active film plane width | <!-- BEGIN fact:container_interior_length_mm -->5893<!-- END fact:container_interior_length_mm -->mm | **<!-- BEGIN fact:film_plane_width_mm -->4499<!-- END fact:film_plane_width_mm -->mm** (X=150–4649mm) |
| Rail positions | X=200mm, X=5693mm | **X=150mm, X=4649mm** |
| Rail span | 5493mm | **<!-- BEGIN fact:film_plane_width_mm -->4499<!-- END fact:film_plane_width_mm -->mm** |
| Max swing angle | 20.3° | **<!-- BEGIN fact:film_plane_max_swing -->28<!-- END fact:film_plane_max_swing -->°** |
| Blue IBCs (×2) | Left side, X=100–1319mm | Right end zone, X=4674mm, 2×2 stack top tier |
| Brown IBC | Right side, X=4674mm | Right end zone, X=4674mm, 2×2 stack bottom near |
| Waste IBC | — (55-gal drums) | **Right end zone, X=4674mm, 2×2 stack bottom far** |
| 55-gal drums | Right side, X=3900mm | **Eliminated — waste via IBC-4 in right end zone** |
| Evap cooler | X=1380mm (near optical zone) | **Ground-placed outside; duct penetration at Yd=0, X=1000mm** |
| Items in optical cone | 0 (colonnade already fixed) | **0** ✓ |
| Shadow-free proof | Depth-limited (max Yd=1220mm) | **Geometry-limited (exact cone fit at film plane edges)** |

---

## 11. Source References

1. [ISO 668:2020](https://www.iso.org/standard/76912.html) — Series 1 freight containers: Classification, dimensions and ratings.
2. [Schütz Ecobulk MX 1000L](https://www.schuetz-packaging.net/schuetz-usa/en/ibcs/ecobulk/ecobulk-mx/) — 1000L caged composite IBC tote specifications and cage dimensions (~65 kg tare; a 600L caged tote does not exist).
3. [Light Trap Selection Report](light-trap-selection.md) — Revolving drum specification and panel integration.
4. [Hinged Panel Report](hinged-panel-report.md) — Stepped panel construction and swing-pivot specification.
5. [Water System Report](water-system-report.md) — IBC layout, plumbing manifold, and pump positions.
6. [Walkway System Report](walkway-report.md) — Perimeter walkway dimensions and cantilever bracket design.

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
