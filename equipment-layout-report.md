# Equipment Layout — Optical Clearance Redesign
## TBS-001 — Pinhole Wall Colonnade

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*

---

## 1. The Problem — Original Layout Blocked the Optical Cone

The original equipment layout placed three 1,000L IBC totes and ancillary systems
across the full container width (X=0–2,700mm long axis, Y=100–2,330mm depth from
pinhole wall). The [line-of-sight analysis](engineering-diagrams.md#13-optical-line-of-sight-clearance)
confirmed that six items fell inside the optical cone:

| Item | Plan intersection? | Elevation intersection? |
|------|--------------------|------------------------|
| Blue IBC ×2 (rear) | ✗ — entered at Yd=1,246mm | ✗ |
| Brown IBC ×1 | ✗ | ✗ |
| 55-gal Drum 1 | ✗ | ✗ |
| 55-gal Drum 2 | ✗ | ✗ |
| Evap cooler | ✗ | ✗ |
| Pump manifold | ✗ | ✗ |

Any item in the optical cone casts a shadow on the film plane, producing an
unexposed void in the image. For a camera where a single exposure covers 140 sq ft
of muslin, any shadow is unacceptable.

---

## 2. The Fix — Pinhole Wall Colonnade

**Core principle:** The optical cone is narrowest near the pinhole wall (Yd=0).
At depth Yd, the cone spans only a central band:

```
X_left(Yd)  = 2,946 × (1 − Yd/2,262)     [left cone boundary]
X_right(Yd) = 2,946 + 2,947 × (Yd/2,262) [right cone boundary]
```

By keeping all equipment within **Yd ≤ 1,220mm** of the pinhole wall, and
positioning it in **two wings that flank the pinhole in the X direction**, every
item stays outside the cone.

At Yd=1,220mm the cone spans X=1,470–4,424mm — a 2,954mm wide band. The two
equipment wings sit entirely outside this band:
- **LEFT WING:** X=0–2,380mm — equipment ends at X=2,380mm, cone left boundary
  at Yd=1,220mm is X=1,470mm. Items must have their **right edge** < 1,470mm
  for the deepest items, or shallower depth if placed closer to the pinhole.
- **RIGHT WING:** X=3,900–5,893mm — equipment left edge ≥ 3,900mm, cone right
  boundary at Yd=680mm (drum depth) is X=3,831mm.

The result: **optical zone Yd=1,220–2,262mm is completely clear**
across the full container width. The line-of-sight diagram with the new layout
shows zero obstructions.

**Floor plan — new layout:**

![TBS-001 Container Floor Plan — Pinhole Wall Colonnade](assets/container-floorplan.png)

**Optical line-of-sight — all clear:**

![TBS-001 Optical Line-of-Sight Clearance — New Layout](assets/line-of-sight.png)

---

## 3. New Equipment Positions

### 3.1 Left Wing (X=0–2,380mm, Yd=0–1,116mm)

| Item | X (mm) | Yd (mm) | H (mm) | Cone clearance |
|------|--------|---------|--------|---------------|
| Blue IBC stack ×2 (600L each) | 100–1,319 | 100–1,116 | 0–2,020 | Right edge 1,319 < X_left(1,116)=1,494 ✓ |
| Evaporative cooler | 1,380–1,980 | 100–450 | 0–800 | Right edge 1,980 < X_left(450)=2,360 ✓ |
| Pump manifold | 1,980–2,380 | 100–400 | 0–500 | Right edge 2,380 < X_left(400)=2,424 ✓ |
| Electrical panel | 2,050–2,350 | 0–80 | 900–1,500 | Wall-mounted (Yd=0) — no cone risk ✓ |

### 3.2 Right Wing (X=3,900–5,893mm, Yd=0–1,116mm)

| Item | X (mm) | Yd (mm) | H (mm) | Cone clearance |
|------|--------|---------|--------|---------------|
| 55-gal drum stack ×2 | 3,900–4,480 | 100–680 | 0–1,740 | Left edge 3,900 > X_right(680)=3,831 ✓ |
| Brown IBC ×1 (600L) | 4,674–5,893 | 100–1,116 | 0–1,010 | Left edge 4,674 > X_right(1,116)=4,400 ✓ |

### 3.3 Pinhole Wall Face (Yd=0 surface)

All electrical and plumbing runs on the **pinhole long wall face** — no
conduit or cabling enters the optical zone:

| System | Position | Notes |
|--------|----------|-------|
| Main electrical enclosure | X=2,050–2,350mm, H=900–1,500mm | IP65, flush-mount |
| Battery bank (2× 100Ah LiFePO4) | Below enclosure, H=0–500mm | Wall-bracket mount |
| Solar charge controller | Within enclosure | — |
| Plumbing manifold (3-circuit) | X=2,400–2,600mm, H=200–600mm | Wall-bracket |
| Fill ports & drain valves | Accessible from pinhole wall side | No floor intrusion |
| Circuit conduit | Horizontal trunking, Y=0 wall face, H=1,800mm | Never crosses optical zone |

---

## 4. Why Stack IBCs — The Height Problem

**Current 1,000L IBC (h=1,163mm):** Stacking two gives 2,326mm total — only
62mm below the 2,388mm container ceiling. Under road vibration this is unsafe
and violates IBC manufacturer stacking guidelines for transport.

**Solution: Switch to 600L IBCs (h≈1,010mm).** Stacking two gives 2,020mm —
368mm ceiling clearance. This is safe for transport (fully loaded) within a
self-contained stacking frame.

| IBC type | H (mm) | Stacked pair | Ceiling clearance | Transport safe? |
|----------|--------|--------------|-------------------|----------------|
| 1,000L standard | 1,163 | 2,326mm | 62mm | NO |
| **600L** | **1,010** | **2,020mm** | **368mm** | **YES** |
| 800L | 1,116 | 2,232mm | 156mm | Marginal |

---

## 5. IBC Stacking Frame — Design Specification

A welded mild steel frame holds the two 600L IBCs, one above the other,
as a single unit. The frame provides lashing points for transport and a
removable access panel for the lower IBC drain valve.

**Sheet 1 — Stacking Frame Assembly:**

| Item | Specification |
|------|--------------|
| Frame material | 50×50×3mm RHS mild steel |
| Platform height | 1,060mm (lower IBC height 1,010mm + 50mm clearance plate) |
| Frame footprint | 1,350mm × 1,150mm (IBC footprint + 65mm per side) |
| Total loaded height | 2,020mm (IBC ×2) + 1,060mm frame platform = 2,070mm with frame base |
| Lashing points | 25mm D-ring, 4× per tier (8× total), welded at frame corners |
| Access gate | Bolted removable panel at H=0–300mm (lower IBC drain valve access) |
| Anti-rotation | 40mm steel lip on platform perimeter retains upper IBC cage |
| Surface finish | Grey oxide primer + flat black powder coat (interior) |
| Approx. weight | 45–60kg (frame alone) |
| Approx. cost | USD $400–$600 (local mild steel fabrication) |

**Raw material suppliers:**

| Item | Supplier | Notes |
|------|----------|-------|
| 50×50×3mm RHS mild steel | Pacific Coast Steel, Santa Fe Springs CA | A500 Grade B; ~$4/linear foot |
| D-ring lashing points (×8) | McMaster-Carr #3641T29 | 1,100kg WLL per ring |
| M12 bolts (access gate, ×8) | McMaster-Carr or local hardware | SS A2-70 |
| Anti-slip platform mat | McMaster-Carr #6009K14 | 12mm rubber sheet, 1.2m × 1.0m |

**Transport protocol:**

1. Drain both IBCs before transport, or reduce fill to ≤25% (250L per unit) per
   manufacturer guidelines for road vibration
2. Lash each IBC tier independently with 32mm polyester strap (Cordstrap or
   equivalent, WLL ≥ 1,600kg), 2× straps per tier crossing diagonally
3. Anti-slip 12mm rubber mat between frame base and container floor
4. 4× container floor lashing points engaged (D-rings welded to container floor
   at X=100, X=1,319mm — installed during container conversion)

---

## 6. Alternative Tank Options Evaluated

| Option | Footprint (mm) | Height | Capacity | Assessment |
|--------|---------------|--------|---------|------------|
| **600L IBC (recommended)** | 1,219×1,016 | **1,010** | 600L | Best balance — stacks at 2,020mm; standard cage frame |
| 800L IBC | 1,219×1,016 | 1,116 | 800L | Stacks at 2,232mm — 156mm clearance; acceptable |
| 1,000L IBC (current) | 1,219×1,016 | 1,163 | 1,000L | Cannot stack safely — only 62mm ceiling clearance |
| Norwesco 500-gal low-profile | 2,400×2,337 | 435 | 1,893L | Footprint exceeds container interior width (2,362mm) |
| Rectangular HDPE tank 500L | ~1,200×800 | ~900 | 500L | Non-standard; chemical compatibility check required |
| Horizontal 55-gal drum cradle | Ø585×870 horizontal | ~585 | 208L | Reduces height but increases footprint length |

**Recommendation:** 3× 600L IBCs total (2× Blue, 1× Brown) + 2× 55-gal drums.

| Tank | Qty | Capacity | Role |
|------|-----|---------|------|
| 600L Blue IBC (stacked ×2) | 2 | 1,200L | Clean wash water |
| 600L Brown IBC | 1 | 600L | Recycled wash / fix |
| 55-gal drum (stacked ×2) | 2 | 416L | Waste (sealed) |
| **Total** | — | **2,216L** | — |

2,216L supports **7–8 prints per resupply** with 40% water recycling (vs. the
original 3,000L design capacity of ~10 prints). To restore 10-print capacity,
add a 4th 600L IBC (2,816L total → 9–10 prints).

---

## 7. 55-Gallon Drum Stacking

Standard closed-head 55-gallon drums are rated for vertical stacking when chimed
rims are engaged. The lower drum's chime supports the upper drum's bottom.
Two drums stacked: 2 × 870mm = 1,740mm — 648mm clearance from container ceiling.

For additional stability during transport, a simple two-level drum stacking rack
(welded steel channel, ~$150 fabricated locally) can replace direct chime-on-chime
stacking. Lash as for IBCs with 25mm polyester strap.

---

## 8. Plumbing and Electrical — Pinhole Wall Routing

All services route along the pinhole long wall face (Yd=0). No conduit, pipe, or
cable runs through the optical zone.

**Plumbing manifold:** 3-circuit distribution header (Wash 1, Wash 2, Waste)
wall-mounted at X=2,400–2,600mm, H=200–600mm. Hose runs drop vertically to
IBCs and pump. No hose crosses the container interior beyond Yd=1,220mm.

**Electrical conduit:** 25mm PVC trunking, horizontal at H=1,800mm, running the
full container length on the pinhole wall face. Branch drops at each circuit
termination. Circuit lengths from [Electrical Report](electrical-report.md):
- Fan exhaust (far end): ~8m run, along pinhole wall face → up ceiling corner rail
- All other circuits: ≤6m, entirely within pinhole wall face zone

**Solar inlet + shore power:** NEMA 5-15R weatherproof inlet on exterior of
pinhole wall, centred at X=2,946mm (pinhole side), H=400mm.

---

## 9. Impact on Water System Capacity

See [Processing System Report](water-system-report.md) for full water circuit design.
The colonnade layout changes tank types but not the circuit topology or chemistry.

| Metric | Original | New (3× 600L IBC) | New + 4th IBC |
|--------|---------|-------------------|---------------|
| Clean water | 2,000L (2×1,000L) | 1,200L (2×600L stacked) | 1,800L (3×600L stacked) |
| Recycled water | 1,000L (1×1,000L) | 600L (1×600L) | 600L |
| Waste drums | 416L (2×55-gal) | 416L | 416L |
| Total capacity | ~3,416L | ~2,216L | ~2,816L |
| Prints per resupply | ~10 | ~7–8 | ~9–10 |

The 3-IBC colonnade layout is the baseline. The 4-IBC option (adding a 4th 600L
IBC to the right wing at X=4,674–5,893mm, stacked on the Brown IBC) restores full
10-print capacity if required.

---

## 10. Summary of Changes

| System | Before | After |
|--------|--------|-------|
| Equipment zone concept | X=0–2,700mm (by long axis) | Yd=0–1,220mm (by depth from pinhole wall) |
| Blue IBCs | 2× 1,000L, side by side in Yd | 2× 600L, stacked vertical, LEFT WING |
| Brown IBC | 1× 1,000L, X=1,380mm | 1× 600L, RIGHT WING X=4,674mm |
| 55-gal drums | 2× floor-standing, Yd=1,310mm | 2× stacked, RIGHT WING X=3,900mm |
| Evap cooler | X=1,380mm, Yd=1,980mm | X=1,380mm, Yd=100mm (pinhole side) |
| Pump manifold | X=2,050mm, Yd=1,980mm | X=1,980mm, Yd=100mm |
| Electrical panel | Short wall X=0 | Pinhole long wall, flush-mount |
| Items in optical cone | 6 | **0** |
| Max equipment depth | Yd=2,330mm | **Yd=1,116mm** |
| Optical clear zone | Partial (vignetting) | **Full — Yd=1,220–2,262mm clear** |
