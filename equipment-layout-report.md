<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Equipment Layout — Shadow-Free End-Zone Design

## 1. Design Principle — Shadow-Free End Zones

The optical cone from the pinhole narrows as it approaches the pinhole wall and
widens as it approaches the film plane. Any equipment placed inside the cone casts
a shadow on the film plane, producing an unexposed void in the image.

**Solution:** Reduce the active film plane from the full 5893mm container width
to a 4499mm span (X=150–4649mm). This creates two **provably shadow-free end
zones** — one at each end of the container — where equipment can be placed at any
depth without entering the optical cone.

The right end zone contains a 2×2 IBC stack (including a dedicated 600L waste
IBC),  leaving the left zone to contain the light trap drum.
The right zone boundary sits at X=4649mm, giving a 4499mm active film plane
(rev 5, 2026-05-06).

### Optical Cone (rev 6 geometry)

The pinhole is centered on the film plane at X=2399mm. At depth Y from the
pinhole wall, the cone boundaries are:

```
X_left(Y)  = 2,399 − 2,249 × Y/2,262    [left cone boundary]
X_right(Y) = 2,399 + 2,250 × Y/2,262    [right cone boundary]
```

At the film plane (Y=2262mm): X_left=150mm, X_right=4649mm — exactly the
film plane edges. The cone never extends beyond these X values at any depth ≤ 2262mm.

### Zone Definitions

| Zone | X range | Shadow-free? | Equipment assigned |
|------|---------|--------------|--------------------|
| **Left end zone** | 0–150mm | YES at all depths | Light trap drum, hinged panel (stepped) |
| **Optical zone** | 150–4649mm | NO | Film plane, rails, processing tray, perimeter walkway |
| **Right end zone** | 4649–5893mm | YES at all depths | IBC tanks (2×2 stack: 2× Blue, 1× Brown, 1× Waste) |
| **Pinhole wall face** | Y=0 surface | YES (cone collapses to point) | Electrical panel, battery, pump |

**Shadow-free proof:**
- Left zone (X=0–150): cone left boundary ≥ 150mm at all depths Y ≤ 2262mm.
  All left-zone equipment (light trap drum, hinged panel) stays within zone. ✓
- Right zone (X=4,649–5,893): cone right boundary ≤ 4649mm at all depths Y ≤ 2262mm.
  All right-zone equipment has X_left ≥ 4674mm — well inside the zone. ✓
- Pinhole wall (Y=0): cone collapses to a single point (the pinhole). ✓

---

## 2. Equipment Positions

Overall floorplan can be seen below. Its essentially split into three areas, left, center and right which are discussed below.

**Floor plan**
![TBS-001 Container Floor Plan — End-Zone Layout](assets/container-floorplan.png)

### 2.1 Left End Zone — X=0–150mm (shadow-free at all depths)

| Item | X (mm) | Yd (mm) | H (mm) | Notes |
|------|--------|---------|--------|-------|
| Hinged panel (stepped) | 0–40 (corner) / 0–120 (center) | 0–2,362 | 0–2,388 | Stepped profile: 40mm corners, 120mm center (drum housing). Swings ~56° about the Ø89 pivot for transport. |
| Light trap drum | −375–375 | 806–1,556 (centered at CW/2=1181mm) | 0–2,200 | Centered at X=0 (spans container wall); integrated into panel center zone; rotary drum entry |

### 2.2 Pinhole Wall Face — Y=0 surface (shadow-free)

| Item | X (mm) | H (mm) | Notes |
|------|--------|--------|-------|
| Evaporative cooler | 700–1,300 | ground | 12V DC 80W; ground-placed outside, flex duct to wall stub at Z=1900mm |
| Electrical panel | 1,910–2,210 | 1,500–2,100 | IP65, wall-mount (stacked above the battery bank; clears the upper transport-stay anchor). rev11: dropped 150mm (was Z1,650–2,250) — originally to clear the film-plane brace top beam; that brace cage is now retired for wall-seat saddles, but the EP is kept at this height |
| Battery bank (2× 100Ah LiFePO4) | 1,600–2,100 | 0–500 | Wall-bracket below panel |
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

The processing tray sits below the film plane carriage blocks (minimum Z=140mm at maximum 42° tilt), providing 90mm clearance above the tray rim. The tray does not contact or interfere with the HGR20 rail channels at X=150 and X=4,649.

### 2.4 Right End Zone — X=4649–5893mm (shadow-free at all depths)

2×2 IBC stack — right-justified flush to the far end wall. Four IBCs in two
columns at X=4674mm (25mm clearance from zone boundary), separated by a
270mm plumbing corridor between near and far columns. IBC wall clearance
is 30mm on each side.

| Item | X (mm) | Yd (mm) | H (mm) | Notes |
|------|--------|---------|--------|-------|
| Blue IBC-1 (600L, top near) | 4,674–5,893 | 30–1,046 | 1,010–2,020 | Near column top; stacked frame |
| Blue IBC-2 (600L, top far) | 4,674–5,893 | 1,316–2,332 | 1,010–2,020 | Far column top; stacked frame |
| Brown IBC-3 (600L, bottom near) | 4,674–5,893 | 30–1,046 | 0–1,010 | Near column bottom; recycled wash/fix |
| Waste IBC-4 (600L, bottom far) | 4,674–5,893 | 1,316–2,332 | 0–1,010 | Far column bottom; sealed waste collection |

---

## 3. Floor Plan and Line-of-Sight Diagrams

**Optical line-of-sight**

![TBS-001 Optical Line-of-Sight Clearance — New Layout](assets/line-of-sight.png)

The line-of-sight analysis confirms zero equipment items intersect the optical
cone in either the plan (top-down) or elevation (side) view.

---

## 4. Why IBC Y-Stacking (Front-to-Back)

In the current layout (rev 5) the entire right end zone is
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

A welded mild steel frame holds the 2×2 IBC stack (4× 600L IBCs total — two
columns, two tiers each) as a single unit. The frame provides lashing points
for transport and removable access panels for the lower IBC drain valves.

| Item | Specification |
|------|--------------|
| Frame material | 50×50×3mm RHS mild steel |
| Platform height | 1060mm (lower IBC height 1010mm + 50mm clearance plate) |
| Frame footprint | 2362mm × 1284mm portal frame — platform beams simply supported wall-to-wall (corridor uprights + welded wall seat brackets), 1284mm depth. Corridor uprights at inner IBC edges define the 270mm plumbing corridor between columns |
| Total loaded height | 2020mm (IBC ×2) — 368mm ceiling clearance ✓ |
| Lashing points | 25mm D-ring, 4× per tier (8× total), welded at frame corners |
| Access gates | Bolted removable panels at H=0–300mm (lower IBC drain valve access, ×2) |
| Anti-rotation | 40mm steel lip on platform perimeter retains upper IBC cage |
| Center divider | 50×50×3mm RHS cross-member on platform between near/far columns |
| Panel support frame | Mid-bay corridor uprights extended to Z=2260mm + top rail + floor beam — the wet-end equipment panel butts the film-plane face of this rectangle and bolts to it |
| Surface finish | Gray oxide primer + flat black powder coat (interior) |
| Approx. weight | ~144kg (frame incl. floor flange feet + wall seat brackets + panel support frame) |
| Approx. cost | USD $500–$800 (local mild steel fabrication) |

**Why 600L IBCs, not 1,000L:**

| IBC type | H (mm) | Stacked pair | Ceiling clearance | Transport safe? |
|----------|--------|--------------|-------------------|----------------|
| 1,000L standard | 1,163 | 2326mm | 62mm | NO |
| **600L** | **1,010** | **2020mm** | **368mm** | **YES** |
| 800L | 1,116 | 2232mm | 156mm | Marginal |

**Stacking two 600L IBCs gives 2020mm height — 368mm ceiling clearance**, safe
for road transport with full load.

**Raw material suppliers:**

| Item | Supplier | Notes |
|------|----------|-------|
| 50×50×3mm RHS mild steel | Pacific Coast Steel, Santa Fe Springs CA | A500 Grade B; ~$4/linear foot |
| D-ring lashing points (×8) | McMaster-Carr #3641T29 | 1,100kg WLL per ring |
| M12 bolts (access gate, ×8) | McMaster-Carr or local hardware | SS A2-70 |
| Anti-slip platform mat | McMaster-Carr #6009K14 | 12mm rubber sheet, 1.2m × 1.0m |

---

## 6. Left End Zone — Simplified Layout (Rev 5)

Waste collection is handled by IBC-4 (600L, sealed) in the right end zone 2×2 stack.
The left end zone contains only the light trap drum and the hinged panel — no
floor-mounted equipment, no dolly tracks, no bridge sections, providing
unobstructed egress at the cargo door end.

### 6.1 Stepped Panel and Swing Pivot (Transport Mode)

The hinged panel has a stepped profile: 40mm thick at the corner zones and 120mm thick at the center zone
where the light trap drum is mounted. For transport the panel + drum SWING ~56° about a
vertical Ø89×8mm CHS pivot post (the reused film-plane far-left upright at X=175, Yd=2287),
carrying the punch-out bay inboard of the door plane. Two narrow strips stay fixed at the
door plane (near Yd0–180, far Yd2287–2362, which carries the pivot); the cargo doors close
outboard of the fixed near strip. The earlier "slide 880mm on HGR20 rails" scheme is retired.

| Position | Description | Doors clear? |
|----------|-------------|-------------|
| Operational (0°) | Panel closed at the door plane; the B2 punch-out bay protrudes ~890mm outside | No — the doors stay open during camera operation |
| Transport (swung 56°) | Panel + drum revolved about the pivot, swept inboard | Yes — true minimum clearance to the closed door is +59mm |

A fixed welded door frame (50×50×3mm RHS) provides the EPDM seal landing. The panel seals
against this frame with the Southco C2-33 cam latches and 20mm EPDM gaskets in the closed
(latched) position; the latches release to free the seals before the swing.

#### 6.1.1 Swinging Panel Light Seal Design

The swinging panel seals against the fixed door frame in its operational (camera-ready,
closed) position. Five light ingress paths are sealed:

| # | Light path | Seal method |
|---|-----------|-------------|
| 1 | **Panel perimeter → door frame** | 20mm EPDM gasket in an aluminum channel, compressed by the 4× Southco C2-33 cam latches against the fixed door frame at X=0. |
| 2 | **Swing cuts → fixed strips** | The swinging center+corners separate from the two fixed strips along vertical cuts at Yd=180 and Yd=2287. A 20mm EPDM cut seal runs the full panel height down each cut, compressed by the cam latches when the panel is latched at the door plane. (Replaces the old sliding-carriage beam/guide-slot brush seals.) |
| 3 | **Panel bottom → 130mm floor gap** | Fixed-frame bottom seal lip — a continuous steel threshold upstand, full panel-bottom width (no notch; the drum rides at Z=130). A 20mm EPDM strip on the panel bottom edge compresses against it, latched by the lower cam latches; releases before the swing. |
| 4 | **Panel top → frame gap** | Fixed-frame top seal lip — a steel downstand from the frame top rail, full panel-top width, continuous across the center. A 20mm EPDM strip on the panel top edge compresses against it, latched by the upper cam latches. |
| 5 | **Housing surround → door frame** | A second 20mm EPDM gasket rings the Ø900 housing aperture, concentric inboard of the perimeter seal, sealing the housing surround to the frame in the closed position. |

**Light seal verification:** After mode conversion to operational position, the
operator performs a dark-adaptation check (5 minutes in a darkened container with
all seals engaged). Any visible light points are marked with gaffer tape for
re-sealing. The cut seals at the swing boundaries and the bottom/top lips are the
critical compression seals.

### 6.2 Evaporative Cooler Transport Stowage

The evaporative cooler (Portacool Jetstream 110 or equivalent, ~600×350×800mm, ~20 kg dry) sits on the ground outside the container during operation, connected to the wall penetration via Ø200mm flex duct. It must be stowed inside the container for transport.

**Stowage position:** On the near walkway grating in the wide section. The cooler sits on a 12mm plywood base plate (600×350mm) that distributes the load across the grating and prevents the housing from catching in the grate openings. The wide section (500mm) fully contains the 350mm cooler depth with 150mm clearance — no overhang into the processing tray zone.

**Securing:** Two 25mm ratchet straps loop over the cooler and hook to the nearest cantilever bracket arms. Two aluminum angle cleats (25×25×3mm, 100mm long) screwed to the base plate prevent lateral sliding.

| Parameter | Value |
|-----------|-------|
| Stowage zone | X=1450–2050mm, Yd=0–350mm (near walkway wide section) |
| Cooler footprint | 600×350mm (long axis along X) |
| Cooler height on grating | 800mm (top at Z=900mm) |
| Weight (dry) | ~20 kg |
| Securing | 2× ratchet straps to bracket arms |
| Base plate | 12mm ply, 600×350mm |
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

| Tank | Qty | Capacity | Role |
|------|-----|---------|------|
| 600L Blue IBC (stacked ×2) | 2 | 1,200L | Clean wash water |
| 600L Brown IBC | 1 | 600L | Recycled wash / fix |
| 600L Waste IBC | 1 | 600L | Waste (sealed) |
| **Total** | — | **2,400L** | — |

2,400L supports **~10 prints per resupply** with 40% water recycling (16 gal per wash cycle, 32 gal Blue consumed per print with Brown recycling).

See [Processing System Report](water-system-report.md) for full water circuit design.

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
| Active film plane width | 5893mm | **4499mm** (X=150–4649mm) |
| Rail positions | X=200mm, X=5693mm | **X=150mm, X=4649mm** |
| Rail span | 5493mm | **4499mm** |
| Max swing angle | 20.3° | **25.7°** |
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
2. [Schutz Ecobulk MX 600L](https://www.schuetz-packaging.net/schuetz-usa/en/ibcs/ecobulk/ecobulk-mx/) — IBC tote specifications and cage dimensions.
3. [Light Trap Selection Report](light-trap-selection.md) — Revolving drum specification and panel integration.
4. [Hinged Panel Report](hinged-panel-report.md) — Stepped panel construction and swing-pivot specification.
5. [Water System Report](water-system-report.md) — IBC layout, plumbing manifold, and pump positions.
6. [Walkway System Report](walkway-report.md) — Perimeter walkway dimensions and cantilever bracket design.

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
