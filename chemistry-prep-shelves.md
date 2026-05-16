<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Chemistry Prep Shelves — TBS-001

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*

---

## 1. Purpose

Cyanotype processing requires a clean, stable work surface for:

- Mixing sensitizer chemistry (ammonium iron(III) oxalate + potassium ferricyanide)
- Measuring and dispensing solutions (graduated cylinders, digital scale)
- Coating muslin substrate with sensitizer (roller tray, foam roller)
- Staging materials (bottles, pH meter, gloves, timer)
- Post-exposure citric acid wash preparation

No permanent bench is practical — floor space is occupied by the processing tray and walkway, and any fixed furniture would obstruct film loading. Two fold-down shelves on the pinhole wall provide chemistry prep capability when needed and fold flat for transport.

---

## 2. Location and Spatial Constraints

The shelves mount on the pinhole wall (Yd=0) in the clear zone to the right of the pump manifold. This area is provably shadow-free (at Yd=0 the optical cone collapses to a point), so the shelves cannot vignette the image regardless of film plane position.

| Constraint | Value |
|-----------|-------|
| Available X range on wall | X=2,800–4,629mm (1,829mm) |
| Left boundary | Pump manifold right edge (X=2,800mm) |
| Right boundary | Near walkway end / IBC zone start |
| Cable trunking | H=1,800mm (40×25mm PVC, horizontal full length) |
| Near walkway | Yd=0–300mm, deck H=100mm |
| Processing tray near edge | Yd=80mm, rim H=50mm (below shelf — no conflict) |

The operator stands on the near walkway (deck at H=100mm) directly in front of the shelves. Ergonomic counter height for standing work is 900–950mm above standing surface, yielding a target work surface height of H=1,000–1,050mm above floor.

---

## 3. Design Specification

### 3.1 Shelf Dimensions

Two identical shelves centered in the available zone:

| Parameter | Value |
|-----------|-------|
| Shelf A position | X=2,900–3,650mm |
| Shelf B position | X=3,879–4,629mm |
| Width (each) | 750mm |
| Depth (deployed) | 450mm (Yd=0 to Yd=450mm) |
| Gap between shelves | 229mm |
| Work surface height | H=1,025mm above floor (925mm above walkway deck) |
| Shelf thickness | 22mm (18mm ply + 4mm perimeter frame) |
| Protrusion when folded | 22mm from wall face |
| Folded top edge height | H=1,475mm (325mm below cable trunking) |
| Walkway overhang (deployed) | 150mm past walkway outer edge |
| Total work surface area | 2 × 750 × 450 = 675,000 mm² (0.675 m²) |

### 3.2 Construction

**Work surface:** 18mm phenolic-faced plywood (concrete form ply). The phenolic resin face provides excellent chemical resistance to cyanotype solutions (ferric/ferricyanide salts, pH 3–4 citric acid). Surface is smooth, non-absorbent, and easily wiped clean. If damaged after extended use, the ply panel can be unbolted and replaced for ~$30.

**Frame:** 25×25×3mm mild steel SHS (square hollow section), welded into a rectangular perimeter frame matching the ply panel. The frame provides rigidity and the attachment points for the piano hinge and folding leg. Finish: flat black powder coat (interior standard).

**Folding leg:** One per shelf. 25×25×3mm steel SHS, approximately 925mm long (spans from shelf underside at Yd=300 down to walkway deck at H=100mm). Pivots on a M8 shoulder bolt at the shelf frame's front cross-member, at the 2/3 depth point (Yd=300mm from wall). When deployed, the leg is vertical — foot rests on the walkway grating. When folded, the leg swings up and lies flat against the shelf underside, retained by a neodymium disc magnet.

### 3.3 Fold Mechanism

The shelf folds **up** against the wall:

- **Hinge:** Stainless steel continuous (piano) hinge, 50mm wide × 750mm long, along the bottom edge of the shelf. One hinge leaf bolts to the wall angle bracket; the other is riveted to the shelf frame.
- **Deployed:** Shelf is horizontal at H=1,025mm. The 90° stop tab (welded steel, on the wall bracket) prevents the shelf from rotating past horizontal under load.
- **Folded (transport):** Shelf swings up 90° and lies flat against the wall, face inward. A heavy-duty stainless ball catch (50N engagement force) at mid-width engages a strike plate on the wall bracket, holding the shelf secure during road transport.

### 3.4 Load Rating

| Parameter | Value |
|-----------|-------|
| Design load per shelf | 20 kg (44 lbs) |
| Moment at hinge (20 kg at 225mm centroid) | 44 N·m |
| Support | Piano hinge (distributed) + folding leg at Yd=300 |
| Safety factor | >3× (piano hinge shear capacity ~150 N·m per 750mm) |

20 kg accommodates: a full 1L bottle of chemistry (~1.1 kg), graduated cylinders, roller tray with solution, digital scale, and staging materials — with ample margin.

---

## 4. Wall Mounting Detail

The shelves attach to the container's corrugated wall ribs (457mm spacing) using the same through-bolt + exterior reinforcing plate pattern as the walkway brackets:

1. **Angle bracket:** 50×50×5mm mild steel angle iron, 750mm long (full shelf width). Horizontal leg supports the piano hinge; vertical leg bolts to wall ribs.
2. **Through-bolts:** 4× M10×75mm hex bolts per shelf (2 per rib, 2 ribs). Pass through: exterior reinforcing plate → wall steel → rib → angle bracket vertical leg.
3. **Reinforcing plates:** 75×100×6mm mild steel, one per rib intersection (4 per shelf). Prevents bolt pull-through of the thin (2mm) corrugated wall steel.
4. **Washers:** M10 flat + spring washer on both sides.

This method requires no welding inside the container and can be installed with basic hand tools (drill, socket set).

---

## 5. Transport Mode Verification

| Check | Status |
|-------|--------|
| Folded protrusion from wall | 22mm — well within 300mm walkway clearance ✓ |
| Folded top edge | H=1,475mm — 325mm below cable trunking (H=1,800mm) ✓ |
| Ball catch engagement | 50N — holds against road vibration (ISO 668 transport loads) ✓ |
| Folding leg stored | Flat against shelf underside, magnet-retained ✓ |
| Conflicts with other systems | None — clear of pump manifold, IBC stack, walkway ✓ |

---

## 6. Assembly Sequence

1. Mark rib positions on interior pinhole wall at X=2,900 and X=3,879 (shelf left edges)
2. Drill 4× Ø11mm holes per shelf through wall at marked rib intersections (H≈970mm)
3. Position exterior reinforcing plates; insert M10 bolts from outside
4. Mount angle brackets to interior face; torque M10 nuts to 40 N·m
5. Attach piano hinge to angle bracket horizontal leg (pre-drilled, M5 CSK screws)
6. Attach shelf frame to piano hinge (rivets or M5 screws)
7. Install 90° stop tabs (weld or bolt to angle bracket)
8. Install ball catch receivers on wall bracket, strike plates on shelf edge
9. Attach folding legs to shelf frames (M8 shoulder bolts)
10. Test deployment and folding; verify horizontal with spirit level

---

## 7. Shopping List

| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Phenolic-faced plywood, 18mm | 1220×2440mm sheet (cut to 2× 750×450) | 1 | Local lumber yard / Home Depot | ~$60 |
| 25×25×3mm steel SHS | 6m length | 2 | Pacific Coast Steel / Online Metals | ~$60 |
| 50×50×5mm steel angle | 6m length (cut to 2× 750mm) | 1 | Pacific Coast Steel / Online Metals | ~$40 |
| SS piano hinge, 50mm × 900mm | Cut to 2× 750mm | 1 | McMaster-Carr #1658A31 | ~$30 |
| M10×75mm hex bolts, SS | Through-bolts | 8 | McMaster-Carr | ~$12 |
| M10 flat + spring washers + nuts | Stainless | 8 sets | McMaster-Carr | ~$8 |
| 75×100×6mm mild steel plate | Reinforcing plates (exterior) | 8 | Metal offcut / local fab | ~$20 |
| 25×25×3mm steel SHS (legs) | 1m per leg × 2 | 1m | Offcut from frame stock | ~$10 |
| M8 shoulder bolts | Leg pivot (2 per shelf) | 4 | McMaster-Carr #91259A589 | ~$12 |
| Heavy-duty ball catch, SS (50N) | Sugatsune BC-5 or equiv. | 2 | Amazon / Sugatsune | ~$16 |
| Neodymium disc magnets, 15mm | Leg retention | 4 | Amazon | ~$8 |
| M5×16mm CSK screws | Hinge attachment | 24 | McMaster-Carr | ~$6 |
| Flat black epoxy spray paint | Frame + bracket finish | 1 can | Hardware store | ~$12 |
| 90° stop tabs, 40×30×5mm flat bar | Weld or bolt to bracket | 2 | Steel offcut | ~$5 |
| **Total** | | | | **~$299** |

---

## 8. Diagrams

### Sheet 1 — Pinhole Wall Elevation

Interior elevation showing both shelves in deployed position (solid) and folded transport position (dashed ghost). Pump manifold and cable trunking shown for context.

![Chemistry Prep Shelves — Sheet 1: Wall Elevation](assets/shelf-sheet1.png)

---

### Sheet 2 — Plan View

Top-down view showing shelf depth relative to the 300mm near walkway. The 150mm overhang past the walkway outer edge does not obstruct walkway passage — operator stands between the wall and the shelf front edge.

![Chemistry Prep Shelves — Sheet 2: Plan View](assets/shelf-sheet2.png)

---

### Sheet 3 — Hinge & Support Detail

Cross-section through one shelf perpendicular to the pinhole wall, showing the piano hinge, angle bracket, through-bolt, folding leg, ball catch, and 90° stop tab.

![Chemistry Prep Shelves — Sheet 3: Hinge & Support Detail](assets/shelf-sheet3.png)
