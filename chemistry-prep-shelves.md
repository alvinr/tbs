<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Chemistry Prep Shelf — TBS-001

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*

---

## 1. Purpose

Cyanotype processing requires a clean, stable work surface for:

- Mixing sensitizer chemistry (ammonium iron(III) oxalate + potassium ferricyanide)
- Measuring and dispensing solutions (graduated cylinders, digital scale)
- Coating muslin substrate with sensitizer (roller tray, foam roller)
- Staging materials (bottles, pH meter, gloves, timer)
- Post-exposure citric acid wash preparation

The shelf must not obstruct walkway navigation (the operator walks the full length of the near walkway during film loading and coating). A ceiling-suspended platform in the right corner — on the tray side of the near walkway — provides 0.18 m² of counter-height workspace while leaving the walkway completely clear.

A dedicated water tap (TAP-01) on the pinhole wall at X=3,729mm, Z=1,150mm provides filtered water from the blue supply line for chemistry mixing and wash-down. Ball valve BV-06, mounted inline on the 3/4" branch pipe at X=3,600mm (129mm to the left of the shelf edge), gives the operator easy shut-off control from the prep position.

---

## 2. Location and Spatial Constraints

The shelf occupies the right corner of the processing area, just inside the walkway perimeter. It sits between the near walkway outer edge (Yd=300mm) and the processing tray far side (Yd=900mm), immediately left of the right walkway (X=3,729–4,329mm). The operator accesses the shelf from the near walkway by turning 90° to face the tray side. No walkway is obstructed.

### 2.1 Optical Cone Clearance

At Yd=450mm (shelf centroid), the optical cone right boundary is:

    cone_right(450) = PH_X + (FP_X_R − PH_X) × 450 / FP_Y
                    = 2,637 + (4,649 − 2,637) × 450 / 2,362
                    = 2,637 + 384 = 3,021mm

The shelf left edge (X=3,729mm) is 708mm outside the optical cone. The shelf cannot vignette the image at any film plane position.

### 2.2 Spatial Constraints

| Constraint | Value |
|-----------|-------|
| Shelf X range | X=3,729–4,329mm (600mm) |
| Shelf Yd range | Yd=300–600mm (300mm) |
| Near walkway | Yd=0–300mm — shelf starts at walkway outer edge |
| Processing tray | Floor level (rim H=50mm) — well below shelf at H=1,025mm |
| Right walkway | X=4,329–4,629mm, ceiling-hung (adjacent, Yd=0–300mm) |
| Ceiling height | H=2,388mm (container interior) |
| Cable trunking | H=1,800mm (40×25mm PVC, horizontal full length) |

---

## 3. Design Specification

### 3.1 Shelf Dimensions

Single ceiling-suspended platform:

| Parameter | Value |
|-----------|-------|
| Position | X=3,729–4,329mm, Yd=300–600mm |
| Width (X direction) | 600mm |
| Depth (Yd direction) | 300mm |
| Work surface height | H=1,025mm above floor (925mm above walkway deck) |
| Shelf thickness | 22mm (18mm ply + 4mm perimeter frame) |
| Work surface area | 600 × 300 = 180,000 mm² (0.18 m²) |
| Hanger rod length | 1,363mm (ceiling to shelf top) |
| Hanger rod diameter | M10 (matches right walkway system) |
| Number of hanger rods | 4 (one at each corner, inset 30mm) |

### 3.2 Construction

**Work surface:** 18mm phenolic-faced plywood (concrete form ply). The phenolic resin face provides excellent chemical resistance to cyanotype solutions (ferric/ferricyanide salts, pH 3–4 citric acid). Surface is smooth, non-absorbent, and easily wiped clean. If damaged after extended use, the ply panel can be unbolted and replaced for ~$30.

**Perimeter frame:** 25×25×3mm mild steel SHS (square hollow section), welded into a rectangular perimeter frame (600×300mm outer). The ply panel sits inside the frame, flush with the top surface. Frame corners have gusset plates for rigidity. Finish: flat black powder coat.

**Spill guard:** 15mm-tall steel lip welded to the frame top edge on all four sides. Prevents chemistry bottles or solution from sliding off during road transport vibration. The lip doubles as a retainer for loose items.

**Hanger rods:** 4× M10 threaded rod, 1,363mm long, connecting the shelf frame to ceiling mounting plates. Each rod passes through the shelf frame corner (drilled hole in SHS top member), secured top and bottom with double nuts + flat washers for leveling adjustment.

### 3.3 Ceiling Mounting

The hanger system replicates the right walkway ceiling attachment:

- **Ceiling plates:** 100×60×6mm mild steel plate, one per hanger rod. Each plate spans one ceiling corrugation rib.
- **Attachment:** 2× M8×30mm hex bolts per plate, through-bolted to the ceiling corrugation rib with backing washers on the exterior (roof side).
- **Rod connection:** M10 threaded rod passes through a centered Ø11mm hole in the ceiling plate, secured with M10 nut + washer above and below the plate for vertical adjustment.
- **Rib spacing:** Container ceiling corrugations at 150mm pitch. Hanger positions (30mm inset from shelf corners) align with available ribs — minor X/Yd offset (<30mm) to nearest rib is acceptable.

### 3.4 Load Rating

| Parameter | Value |
|-----------|-------|
| Design load | 25 kg (55 lbs) |
| Load per hanger rod | 6.25 kg (including shelf self-weight ~8 kg → 8.25 kg per rod total) |
| M10 rod tensile capacity | ~15 kN (far exceeds 330 N total load) |
| Ceiling plate bolt shear | 2× M8 per plate = ~24 kN capacity (far exceeds) |
| Safety factor | >40× on rod tension; >70× on bolt shear |

25 kg accommodates: a full 1L bottle of chemistry (~1.1 kg), graduated cylinders, roller tray with solution, digital scale, and staging materials — with ample margin. The ceiling-hung system is massively over-engineered for this load (same M10 hardware supports the 4.5m right walkway).

### 3.5 Leveling

Double-nut arrangement on each hanger rod allows ±10mm vertical adjustment per corner. After initial installation, level the shelf with a spirit level by adjusting the lower nut positions, then lock with upper jam nuts. The rod length tolerance (±2mm from cutting) is absorbed by this adjustment range.

---

## 4. Transport Mode

The shelf is permanently installed — it does not fold or detach for transport. This is safe because:

| Check | Status |
|-------|--------|
| Walkway clearance | Shelf is on the tray side (Yd=300–900) — near walkway (Yd=0–300) completely unobstructed ✓ |
| Overhead clearance | Shelf top at H=1,025mm — 775mm below cable trunking (H=1,800mm) ✓ |
| Items on shelf | Spill guard lip + transport lashing point (welded D-ring on frame) retains items ✓ |
| Hanger rod vibration | M10 rod at 1,363mm span: fundamental frequency ~45 Hz — well above road excitation (1–15 Hz). No resonance concern ✓ |
| ISO 668 transport loads | 25 kg shelf load × 2g lateral acceleration = 500 N. Distributed across 4× M10 rods = 125 N shear per rod (rod shear capacity ~15 kN) ✓ |

---

## 5. Operator Access

The operator stands on the near walkway (deck at H=100mm) at approximately X=4,029mm (shelf midpoint in X), turned 90° to face the processing tray side. The shelf work surface is at H=1,025mm (925mm above the walkway deck) — ergonomic counter height for standing prep work.

The shelf near edge (Yd=300mm) aligns with the near walkway outer edge, so the operator can reach the full 300mm shelf depth from the walkway without leaning. Items used most frequently (scale, graduated cylinders) are staged at the near edge; bulk storage (bottles, wash trays) at the far edge.

The near walkway remains completely clear for transit in both directions — no fold-down mechanism, no legs on the walkway, no obstruction at any time.

---

## 6. Assembly Sequence

1. Cut 4× M10 threaded rod to 1,400mm (allows 37mm trim margin for leveling)
2. Fabricate 4× ceiling plates (100×60×6mm, drill 2× Ø9mm + 1× Ø11mm per plate)
3. Mark ceiling rib positions for 4 hanger locations (corners of 600×300mm rectangle, inset 30mm)
4. Drill 2× Ø9mm holes per ceiling plate location through ceiling ribs
5. Install ceiling plates with M8×30mm bolts + backing washers (torque to 20 N·m)
6. Thread M10 rods through ceiling plates; secure with nut + washer above and below plate
7. Fabricate shelf frame: weld 25×25×3mm SHS perimeter rectangle (300×600mm) with corner gussets
8. Weld 15mm spill guard lip to frame top edge (all four sides)
9. Weld transport D-ring to one long-side member
10. Drill 4× Ø11mm holes in frame top member at corner positions (matching hanger spacing)
11. Insert ply panel into frame; secure with M5 CSK screws through frame underside
12. Lift shelf frame into position; thread hanger rods through frame corner holes
13. Secure each rod below frame with M10 nut + flat washer
14. Level shelf using a spirit level; adjust lower nuts until horizontal
15. Lock all nuts with upper jam nuts (torque to 25 N·m)
16. Verify: shelf level, spill guard intact, hanger rods vertical, no fouling with walkway or tray

---

## 7. Shopping List

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Phenolic-faced plywood, 18mm | 1220×2440mm sheet (cut to 300×600) | 1 | Local lumber yard / Home Depot | ~$60 |
| 25×25×3mm steel SHS | 6m length (frame + spill guard) | 1 | Pacific Coast Steel / Online Metals | ~$30 |
| M10 threaded rod, 1m | Zinc-plated (join 2× for 1,400mm) | 4 | McMaster-Carr #90322A130 / Home Depot | ~$20 |
| M10 coupling nuts | Join rod sections | 4 | McMaster-Carr #90264A130 | ~$8 |
| 100×60×6mm mild steel plate | Ceiling plates | 4 | Metal offcut / local fab | ~$15 |
| M10 hex nuts, zinc | Rod attachment (3 per rod: ceiling lock + shelf top/bottom) | 12 | McMaster-Carr | ~$6 |
| M10 flat washers, zinc | All nut positions | 12 | McMaster-Carr | ~$4 |
| M8×30mm hex bolts, zinc | Ceiling plate attachment (2 per plate) | 8 | McMaster-Carr | ~$8 |
| M8 flat washers (backing) | Roof-side backing | 8 | McMaster-Carr | ~$3 |
| M8 nuts, zinc | Ceiling bolts | 8 | McMaster-Carr | ~$3 |
| M5×16mm CSK screws | Ply panel attachment | 8 | McMaster-Carr | ~$4 |
| Corner gusset plate, 3mm | 50×50mm triangular (weld to frame) | 4 | Steel offcut | ~$5 |
| Flat black epoxy spray paint | Frame + plate finish | 1 can | Hardware store | ~$12 |
| D-ring, welded (25mm) | Transport lashing point | 1 | Amazon / McMaster-Carr | ~$6 |
| **Total** | | | | **~$184** |

---

## 8. Diagrams

### Sheet 1 — Plan View

Top-down view showing the shelf position (X=3,729–4,329mm, Yd=300–600mm) relative to the near walkway, right walkway, processing tray, and optical cone boundary. The shelf is entirely outside the optical cone and inside the walkway perimeter — no walkway overlap.

![Chemistry Prep Shelf — Sheet 1: Plan View](assets/shelf-sheet1.png)

---

### Sheet 2 — Section Elevation

Cross-section at X=4,029mm (shelf midpoint) looking along the X-axis. Shows the ceiling-hung hanger rods (1,363mm), shelf platform at H=1,025mm, operator silhouette on the near walkway, and the processing tray at floor level below.

![Chemistry Prep Shelf — Sheet 2: Section Elevation](assets/shelf-sheet2.png)

---

### Sheet 3 — Hanger Connection Detail

Detail of one hanger rod connection showing: ceiling corrugation rib, ceiling plate (100×60×6mm) with M8 through-bolts, M10 threaded rod with double-nut leveling, shelf SHS frame cross-section, and 15mm spill guard lip.

![Chemistry Prep Shelf — Sheet 3: Hanger Connection Detail](assets/shelf-sheet3.png)
