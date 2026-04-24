# Equipment Layout — Shadow-Free End-Zone Design
## TBS-001 — Film Plane Reduction Redesign

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*

---

## 1. Design Principle — Shadow-Free End Zones

The optical cone from the pinhole narrows as it approaches the pinhole wall and
widens as it approaches the film plane. Any equipment placed inside the cone casts
a shadow on the film plane, producing an unexposed void in the image.

**Solution:** Reduce the active film plane from the full 5,893 mm container width
to a 4,024 mm span (X=625–4,649mm). This creates two **provably shadow-free end
zones** — one at each end of the container — where equipment can be placed at any
depth without entering the optical cone.

The black-water drums (2× 55-gal) are relocated to the left end zone (Y-stacked
behind the evap cooler), which frees the right end zone for IBCs only and allows the
right zone boundary to move inward from X=4,019mm to X=4,649mm — widening the film
plane by 630mm (rev 2, 2026-04-23).

### Optical Cone (rev 3 geometry)

The pinhole is centred on the new film plane at X=2,637mm. At depth Y from the
pinhole wall, the cone boundaries are:

```
X_left(Y)  = 2,637 − 2,012 × Y/2,262    [left cone boundary]
X_right(Y) = 2,637 + 2,012 × Y/2,262    [right cone boundary]
```

At the film plane (Y=2,262mm): X_left=625mm, X_right=4,649mm — exactly the
film plane edges. The cone never extends beyond these X values at any depth ≤ 2,262mm.

### Zone Definitions

| Zone | X range | Shadow-free? | Equipment assigned |
|------|---------|--------------|--------------------|
| **Left end zone** | 0–625mm | YES at all depths | Light trap drum, 55-gal drums ×2 (Yd=25–605mm) |
| **Optical zone** | 625–4,649mm | NO | Film plane, rails only |
| **Right end zone** | 4,649–5,893mm | YES at all depths | IBC tanks only |
| **Pinhole wall face** | Y=0 surface | YES (cone collapses to point) | Electrical panel, battery, pump |

**Shadow-free proof:**
- Left zone (X=0–625): cone left boundary ≥ 625mm at all depths Y ≤ 2,262mm.
  All left-zone equipment has X_right ≤ 600mm — well inside the zone. ✓
- Right zone (X=4,649–5,893): cone right boundary ≤ 4,649mm at all depths Y ≤ 2,262mm.
  All right-zone equipment has X_left ≥ 4,674mm — well inside the zone. ✓
- Pinhole wall (Y=0): cone collapses to a single point (the pinhole). ✓

---

## 2. Equipment Positions

### 2.1 Left End Zone — X=0–625mm (shadow-free at all depths)

| Item | X (mm) | Yd (mm) | H (mm) | Notes |
|------|--------|---------|--------|-------|
| Light trap drum | −375–375 | 806–1,556 (centred at CW/2=1,181mm) | 0–2,000 | Centred at X=0 (spans container wall); rotary drum entry |
| 55-gal drums ×2 (stacked) | 20–600 | 25–605 | 0–1,740 | Z-stacked; CX=310mm, Yd below light trap drum Yd band (806mm+) |

### 2.2 Pinhole Wall Face — Y=0 surface (shadow-free)

| Item | X (mm) | H (mm) | Notes |
|------|--------|--------|-------|
| Evaporative cooler | 700–1,300 | 0–800 | 12V DC 80W; protrudes 350mm from wall into Yd=0–350mm |
| Electrical panel | 2,050–2,350 | 900–1,500 | IP65, wall-mount |
| Battery bank (2× 100Ah LiFePO4) | 2,050–2,550 | 0–500 | Wall-bracket below panel |
| Solar charge controller | Within panel | — | Mounted inside enclosure |
| Pump manifold (3-circuit) | 2,400–2,700 | 200–600 | Wall-bracket |
| Cable trunking | Along wall face, H=1,800mm | — | Full length |

### 2.3 Optical Zone — X=625–4,649mm

Nothing at floor level. Rail slots in floor/ceiling only. Film plane frame
spans this zone at depth Y=2,262mm (nominal far position).

### 2.4 Right End Zone — X=4,649–5,893mm (shadow-free at all depths)

IBCs only — right-justified flush to the far end wall. All three IBCs occupy a
single X column at X=4,674mm (25mm clearance from zone boundary).

| Item | X (mm) | Yd (mm) | H (mm) | Notes |
|------|--------|---------|--------|-------|
| Blue IBC stack ×2 (600L each) | 4,674–5,893 | 100–1,116 | 0–2,020 | Y-stacked front; stacked frame |
| Brown IBC ×1 (600L) | 4,674–5,893 | 1,141–2,157 | 0–1,010 | Y-stacked rear (behind Blue stack) |

---

## 3. Floor Plan and Line-of-Sight Diagrams

**Floor plan — new end-zone layout:**

![TBS-001 Container Floor Plan — End-Zone Layout](assets/container-floorplan.png)

**Optical line-of-sight — all clear:**

![TBS-001 Optical Line-of-Sight Clearance — New Layout](assets/line-of-sight.png)

The line-of-sight analysis confirms zero equipment items intersect the optical
cone in either the plan (top-down) or elevation (side) view.

---

## 4. Why IBC Y-Stacking (Front-to-Back)

In the previous colonnade layout, IBCs were placed side-by-side in the X direction
at shallow Yd depth. In the new layout the entire right end zone is X-clear from
X=4,649mm to the end wall — all tanks can occupy the same X column and be arranged
along the Y (depth) axis instead.

| Arrangement | X span used | Max Y depth |
|-------------|------------|------------|
| Old (side-by-side X) | 2,400 mm | 1,116 mm |
| **New (Y-stacked, right-justified)** | **1,219 mm** | **2,157 mm** |

Y-stacking gives a 1,219mm X footprint (= IBC cage width), right-justified to the
far end wall. The zone itself is only 1,244mm wide (X=4,649–5,893mm), so the IBCs
fit with 25mm clearance on the zone boundary side.

---

## 5. IBC Stacking Frame — Design Specification

A welded mild steel frame holds the two 600L Blue IBCs, one above the other,
as a single unit. The frame provides lashing points for transport and a
removable access panel for the lower IBC drain valve.

| Item | Specification |
|------|--------------|
| Frame material | 50×50×3mm RHS mild steel |
| Platform height | 1,060mm (lower IBC height 1,010mm + 50mm clearance plate) |
| Frame footprint | 1,350mm × 1,150mm (IBC footprint + 65mm per side) |
| Total loaded height | 2,020mm (IBC ×2) — 368mm ceiling clearance ✓ |
| Lashing points | 25mm D-ring, 4× per tier (8× total), welded at frame corners |
| Access gate | Bolted removable panel at H=0–300mm (lower IBC drain valve access) |
| Anti-rotation | 40mm steel lip on platform perimeter retains upper IBC cage |
| Surface finish | Grey oxide primer + flat black powder coat (interior) |
| Approx. weight | 45–60kg (frame alone) |
| Approx. cost | USD $400–$600 (local mild steel fabrication) |

**Why 600L IBCs, not 1,000L:**

| IBC type | H (mm) | Stacked pair | Ceiling clearance | Transport safe? |
|----------|--------|--------------|-------------------|----------------|
| 1,000L standard | 1,163 | 2,326mm | 62mm | NO |
| **600L** | **1,010** | **2,020mm** | **368mm** | **YES** |
| 800L | 1,116 | 2,232mm | 156mm | Marginal |

**Stacking two 600L IBCs gives 2,020mm height — 368mm ceiling clearance**, safe
for road transport with full load.

**Raw material suppliers:**

| Item | Supplier | Notes |
|------|----------|-------|
| 50×50×3mm RHS mild steel | Pacific Coast Steel, Santa Fe Springs CA | A500 Grade B; ~$4/linear foot |
| D-ring lashing points (×8) | McMaster-Carr #3641T29 | 1,100kg WLL per ring |
| M12 bolts (access gate, ×8) | McMaster-Carr or local hardware | SS A2-70 |
| Anti-slip platform mat | McMaster-Carr #6009K14 | 12mm rubber sheet, 1.2m × 1.0m |

---

## 6. 55-Gallon Drum Left-Zone Placement

The two 55-gal drums are Z-stacked (one above the other) in the left end zone,
near the cargo door end wall. The Yd position (25–605mm) is entirely below the
light trap drum's Yd band (≈806–1,556mm), so there is no X-clearance conflict
regardless of how close the drums are to the light trap in the X direction.

| Parameter | Value |
|-----------|-------|
| Centre X | 310mm (20mm clearance from cargo door end wall) |
| Centre Yd | 315mm (25mm near edge + 290mm drum radius) |
| Footprint | Ø580mm circle (X=20–600mm, Yd=25–605mm) |
| Stacked height | 1,740mm (2× 870mm drums) |
| Ceiling clearance | 2,388 − 1,740 = 648mm ✓ |
| X zone check | X_right = 310 + 290 = 600mm < 625mm zone boundary ✓ |
| Yd vs light trap | Drum Yd_hi=605mm < light trap Yd_lo≈806mm — no conflict ✓ |

Stacking requires a welded steel drum cradle or 870mm platform. Access is from
the Yd direction (side of drums) with ~350mm of open floor between drum far edge
(Yd=605mm) and the light trap drum centre area (Yd≈1,181mm).

**Lashing:** 25mm polyester strap (WLL ≥ 1,600kg) × 2 per drum, crossed diagonally
over the drum top and anchored to D-rings in the container floor or cargo door end wall.

---

## 7. Plumbing and Electrical — Pinhole Wall Routing

All services route along the pinhole wall face (Y=0). No conduit, pipe, or cable
runs through the optical zone.

**Plumbing manifold:** 3-circuit distribution header (Wash 1, Wash 2, Waste)
wall-mounted at X=2,400–2,700mm, H=200–600mm. Hose runs drop vertically from
manifold to IBCs in the right end zone. Maximum hose run: ~5.5m (manifold to
Brown IBC at Yd=1,141mm — along pinhole wall then along right end wall).

**Electrical conduit:** 25mm PVC trunking, horizontal at H=1,800mm, along the
full container length on the pinhole wall face. Branch drops at each circuit
termination. All circuits ≤ 9m — within voltage-drop budget for 12V DC with
10 AWG wire.

**Solar inlet + shore power:** NEMA 5-15R weatherproof inlet on exterior of
pinhole wall at X=2,637mm (pinhole side), H=400mm.

---

## 8. Water Capacity Summary

| Tank | Qty | Capacity | Role |
|------|-----|---------|------|
| 600L Blue IBC (stacked ×2) | 2 | 1,200L | Clean wash water |
| 600L Brown IBC | 1 | 600L | Recycled wash / fix |
| 55-gal drum | 2 | 416L | Waste (sealed) |
| **Total** | — | **2,216L** | — |

2,216L supports **7–8 prints per resupply** with 40% water recycling.

See [Processing System Report](water-system-report.md) for full water circuit design.

---

## 9. Summary

| Parameter | Old (colonnade) | New (end-zone) |
|-----------|----------------|----------------|
| Equipment zone concept | Yd=0–1,220mm depth band | X=0–625mm and X=4,649–5,893mm end zones |
| Pinhole position | X=2,946mm | **X=2,637mm** (centred on active FP) |
| Active film plane width | 5,893mm | **4,024mm** (X=625–4,649mm) |
| Rail positions | X=200mm, X=5,693mm | **X=625mm, X=4,649mm** |
| Rail span | 5,493mm | **4,024mm** |
| Max swing angle | 20.3° | **28.3°** |
| Blue IBCs | Left side, X=100–1,319mm | Right end zone, X=4,674mm, Y-stacked |
| Brown IBC | Right side, X=4,674mm | Right end zone, X=4,674mm, Y behind Blue |
| 55-gal drums | Right side, X=3,900mm | **Left end zone, CX=310mm, Yd=25–605mm** |
| Evap cooler | X=1,380mm (near optical zone) | **Pinhole wall face (Yd=0), X=700–1,300mm** |
| Items in optical cone | 0 (colonnade already fixed) | **0** ✓ |
| Shadow-free proof | Depth-limited (max Yd=1,220mm) | **Geometry-limited (exact cone fit at film plane edges)** |
