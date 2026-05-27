<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Walkway System
## TBS-001 — Engineering Report

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*

---

## 1. Purpose

The perimeter walkway provides dry-foot operator access around all four sides of
the processing tray without wading through chemical solution. It serves four
access functions:

- **Near walkway** (pinhole wall side) — access to electrical panel, battery
  bank, tilt-swing adjusters, and valve manifold.
- **Far walkway** (film plane wall side) — access to film plane carriage clamps,
  rail end-stops, and far-side spray bar pole slot.
- **Left walkway** (cargo door end) — access to hinged light-trap panel latches
  and revolving drum. Removable for panel transport.
- **Right walkway** (IBC end) — access to IBC valves, filter skid, and pump
  manifold. Ceiling-hung to clear the IBC stack below.

All four sections share a common 100mm deck height (75mm bracket arm or bearer
top + 25mm grating) and 300mm standard width, creating a level perimeter walking
surface.

The design enforces **zero processing tray contact** — all walkway supports are
either wall-mounted, ceiling-hung, or placed outside the tray footprint. This
prevents chemical contamination of walkway structures and avoids disrupting the
tray's watertight seal.

---

## 2. System Specifications

| Parameter | Value |
|-----------|-------|
| Standard walkway width | 300mm |
| Deck height (floor to grate top) | 100mm |
| Grating thickness | 25mm press-locked galvanized steel |
| Grating bearing bars | 30×3mm at 34.2mm pitch |
| Bracket arm height | 75mm above finished floor |
| Bracket spacing (near/far) | 457mm (18") — aligned to container rib spacing |
| Container rib spacing | 457mm (18") — ISO standard corrugation pitch |
| Near walkway widened section | 500mm at X=1,600–2,310mm |
| Open processing area | 3,859×1,662mm = 6.41 m² |
| Spray bar slit width | 30mm (near and far walkways) |
| Total walkway sections | 4 (all removable) |

---

## 3. Near and Far Walkways — Wall-Cantilevered

The near (pinhole wall, Yd=0) and far (film plane wall, Yd=2,362mm) walkways run
the full length of the processing tray zone, from the left walkway butt joint at
X=470mm to the right walkway butt joint at X=4,629mm — a span of 4,159mm.

### 3.1 Cantilever Bracket Design

Each bracket is a three-piece welded 8mm steel plate assembly:

| Component | Dimensions | Function |
|-----------|-----------|----------|
| Vertical mounting plate | 8×150mm (height), flat against wall rib | Bolted to container corrugation rib interior face |
| Horizontal arm | 8mm plate, 300mm cantilever (500mm in widened zone) | Supports grating — top surface at Z=75mm |
| Triangular gusset | Right triangle, 70mm reach from wall | Braces arm from below; reach stops before tray rim at Yd=80mm |

![TBS-001 Walkway — Sheet 2: Cross-Section with Bracket Detail](assets/walkway-sheet2.png)

**Attachment:** 3× M12 through-bolts per bracket in a triangular pattern,
passing through the full wall assembly: hex head → reinforcing plate (6mm) →
exterior panel (1.6mm Corten) → air gap → rib interior face (1.6mm) →
bracket vertical plate (8mm) → nut. Two lower bolts at Z=35 mm straddle
the 8mm gusset plate at ±27 mm from the plate centerline in X (centered
between plate edge and gusset). One upper bolt at Z=120 mm (above grating deck at Z=100,
30 mm from plate top) is centered on the gusset centerline. The container
corrugation ribs are hollow — each bolt bridges the air gap inside the rib.
A 6mm reinforcing plate (100×180mm) is welded to the exterior panel face to
provide a bearing surface for the bolt heads and washers. See View B for the bolt pattern detail.

**Spacing:** Brackets mount at every container rib — 457mm (18") centers.

### 3.2 Near Walkway Widened Section

The near walkway widens from 300mm to 500mm between X=1,600mm and X=2,310mm
(710mm length) to provide additional standing room in front of the electrical
panel (EP, X=1,600–1,900mm) and battery bank (X=1,810–2,310mm). These wall-mounted
equipment items require front access for operation and maintenance.

Two brackets in this zone (at X=1,613mm and X=2,070mm) use a heavier design
to support the 500mm cantilever arm.

![TBS-001 Walkway — Sheet 2: Cross-Section with Bracket Detail](assets/walkway-sheet7.png)

| Parameter | Standard bracket | Widened bracket |
|-----------|-----------------|-----------------|
| Plate thickness | 8mm | 10mm |
| Vertical leg height | 150mm | 200mm |
| Arm reach | 300mm | 500mm |
| Gusset reach | 70mm | 70mm (tray rim constrained) |
| Bolt pattern | 3x M12 triangular (2+1) | 4x M12 rectangular (2+2) |
| Reinforcing plate | 100x180x6mm | 120x220x6mm |

The gusset reach remains 70mm on both bracket types — limited by the processing
tray rim at Yd=80mm. The widened bracket compensates with heavier plate, taller
vertical leg for greater wall engagement, and the additional bolt for higher
moment capacity.

**Attachment:** 4× M12 through-bolts per bracket in a rectangular pattern,
passing through the full wall assembly: hex head → reinforcing plate (6mm) →
exterior panel (1.6mm Corten) → air gap → rib interior face (1.6mm) →
bracket vertical plate (10mm) → nut. Two lower bolts at Z=35 mm straddle
the 10mm gusset plate at ±32 mm from the plate centerline in X (centered
between plate edge and gusset). Two upper bolts at Z=160 mm (above grating
deck at Z=100, 40 mm from plate top) at the same ±32 mm X offset. The
container corrugation ribs are hollow — each bolt bridges the air gap inside
the rib. A 6mm reinforcing plate (120×220mm) is welded to the exterior panel
face to provide a bearing surface for the bolt heads and washers. See Sheet 7,
View B for the bolt pattern detail.

### 3.3 Spray Bar Slit

A 30mm wide slot is cut through both near and far walkway grating at the beam
center X position, providing clearance for the spray bar telescoping pole to
pass through the walkway during processing operations. See
[Processing Tray & Spray Bar](processing-tray-and-spray-bar.md) for pole
assembly details.

![TBS-001 Walkway —Positions of walkway slits](assets/spray-bar-sheet3.png)

---

## 4. Right Walkway — Ceiling-Hung

The right walkway at the IBC end (X=4,329–4,629mm) cannot use wall-cantilevered
brackets because the IBC stack (X=4,674–5,893mm) occupies the floor below. Instead,
the walkway is suspended from the container ceiling by threaded rod hangers.

![TBS-001 Walkway — Sheet 3: Ceiling-Hung Support](assets/walkway-sheet3.png)

### 4.1 Bearer Angles

Two 25×25×5mm steel L-angle bearers run the full container width (2,362mm along
Yd) at X=4,329mm and X=4,629mm. The 300mm grating spans between these bearers.
Near and far ends of the bearers bear on the adjacent near/far walkway bracket
arm structures at the butt joints.

### 4.2 Ceiling Hangers

| Parameter | Value |
|-----------|-------|
| Hanger rod | M10 threaded rod |
| Rod length | 2,313mm (ceiling to bearer top) |
| Number of hanger pairs | 5 |
| First pair position | Yd=320mm |
| Remaining pairs spacing | 457mm centers |
| All hangers at | Yd ≤ 2,057mm (clear of optical cone) |
| Ceiling bracket plate | 100×60×6mm steel |
| Ceiling attachment | 2× M10 through-bolts per plate, through ceiling corrugation |

Each hanger pair consists of two M10 rods — one at each bearer (X=4,329mm and
X=4,629mm). The rod passes through the horizontal flange of the L-angle bearer
with a nut and washer above and below the flange, then extends up to a ceiling
bracket plate bolted through the ceiling corrugation.

### 4.3 Design Rationale

The ceiling-hung design achieves three goals:

1. **Zero floor contact** — clears the IBC stack entirely; no legs or supports
   on the container floor in the IBC zone.
2. **Zero tray contact** — the walkway floats above the processing tray.
3. **Level deck** — 100mm deck height matches all four walkway sections.

---

## 5. Left Walkway — Removable Lift-Out

The left walkway at the cargo door end (X=170–470mm) cannot use wall-cantilevered
brackets because the hinged light-trap panel occupies the end wall and slides
300mm inward (to X=420mm) for transport mode. The left walkway is therefore a
removable lift-out section supported by three independent elements.

![TBS-001 Walkway — Sheet 4: Lift-Out at Butt Joint](assets/walkway-sheet5.png)

### 5.1 Support System

| Component | Specification | Position |
|-----------|--------------|----------|
| Bearer beam | 50×50×3mm aluminum RHS | X=470mm, spans 1,762mm along Yd between near/far bracket vertical legs |
| Floor-standing support legs | 25×25×3mm aluminum SHS, 3 legs | X=140mm (on bare floor outside tray), 440mm spacing |
| Foot plates | 60×60×3mm aluminum with rubber pad | At base of each floor leg |
| Bearing strip | 25×25×3mm aluminum angle | On processing tray rim at X=170mm (removable) |

The bearer beam at X=470mm is the primary structural element. It spans 1,762mm
(the distance between the near and far walkway bracket vertical legs at
Yd=300mm and Yd=1,962mm) and is bolted to those bracket vertical legs. The grating
rests on the bearer beam top surface at Z=75mm.

On the cargo door side (X=170mm), the grating rests on a 25×25×3mm aluminum angle
bearing strip placed on top of the processing tray rim (rim top at Z=50mm, strip
top at Z=75mm). Below the bearing strip, three floor-standing support legs at
X=140mm provide vertical support. These legs stand on bare floor outside the
processing tray footprint — zero tray contact.

### 5.2 Bearer Beam Anti-Slip Restraint

The bearer beam is restrained against sliding in the X direction by a flat plate
and lock block system on each bracket arm:

| Component | Specification |
|-----------|--------------|
| Flat plate | 5mm thick × 80mm wide, on bracket arm top |
| Stop lip | 5×20mm, bent up from plate — forms pocket with base |
| Lock block | 20×20mm, on far side of beam |
| Lock bolt | M8 through 50mm slot in plate — adjustable, hand-tightenable |

The beam drops into the pocket formed between the stop lip and lock block. The
M8 bolt through the slotted hole secures the lock block in position. No tools
required for removal — loosen the thumb-screw bolt, slide the lock block, and
lift the beam out.

### 5.3 Panel Transport Clearance

| Clearance | Value |
|-----------|-------|
| Panel transport inner face | X=420mm (300mm slide + 120mm center thickness) |
| Near walkway bracket at butt joint | X=470mm |
| Clearance | 50mm |
| Panel bottom edge | Z=80mm (above 50mm tray rim) |

![TBS-001 Walkway — Sheet 4: Lift-Out at Butt Joint](assets/walkway-sheet4.png)

The left walkway, bearer beam, support legs, and bearing strip must all be
removed before the hinged panel can slide to transport position. The 50mm
clearance between the panel transport envelope (X=420mm) and the first near/far
walkway bracket (X=470mm) ensures the panel never contacts the permanent walkway
structure.

---

## 6. Corner Joints

All four corners use butt joints (not miter joints). The near and far walkway
grating sections terminate at the butt joint lines, and the left and right
walkway grating sections rest on or abut the near/far bracket arms at these
intersections.

| Corner | Butt joint X | Design |
|--------|-------------|--------|
| Near-left / Far-left | X=470mm | Left walkway grating rests on bracket arm top |
| Near-right / Far-right | X=4,629mm | Right walkway grating abuts near/far grating |

Butt joints are used rather than miters for two reasons:

1. **Panel clearance** — near/far walkways start at X=470mm, entirely past the
   panel transport envelope (X ≤ 420mm), so only the left walkway needs removal
   for transport mode.
2. **Simplicity** — each grating section lifts off independently without
   affecting adjacent sections.

---

## 7. Evaporative Cooler Transport Stowage

During transport, the evaporative cooler (600×350mm, ~20kg dry) is stowed on the
near walkway grating at X=500–1,100mm, Yd=0–350mm. The cooler sits on a 12mm
plywood base plate that distributes load across the grating and prevents the
housing from catching in grate openings. Two 25mm ratchet straps loop over the
cooler and hook to near walkway cantilever bracket arms at X≈457mm and X≈914mm.

The 350mm cooler depth slightly exceeds the 300mm walkway width — the cooler
overhangs 50mm into the processing tray zone. This is acceptable because the
tray is drained and empty during transport.

---

## 8. Grating Specification

All four walkway sections use the same grating:

| Parameter | Value |
|-----------|-------|
| Type | Press-locked galvanized steel grating |
| Thickness | 25mm |
| Bearing bar size | 30×3mm |
| Bearing bar pitch | 34.2mm |
| Cross bar type | Twist-locked at mid-height |
| Surface finish | Hot-dip galvanized |

### 8.1 Grating Retention by Walkway Section

| Walkway | Retention Method | Attachment Point | Removal |
|---------|-----------------|------------------|---------|
| Near (pinhole wall) | M saddle clips + TEK screws | Bracket arm top surface | Unscrew TEK screws, lift grating |
| Far (film plane wall) | M saddle clips + TEK screws | Bracket arm top surface | Unscrew TEK screws, lift grating |
| Right (IBC end) | M saddle clips + TEK screws | L-angle bearer horizontal leg | Unscrew TEK screws, lift grating |
| Left (cargo door) | Gravity + guide tabs | Bearer beam (X=470) + bearing strip (X=170) | Lift straight up — no fasteners |

**Near and far walkways** use M saddle clips that straddle two grating bearing
bars. Each clip is secured to the bracket arm with a self-drilling TEK screw
through the clip's center hole. Clips are spaced at every other bracket
(~914mm centers).

**Right walkway** uses the same M saddle clip design, but the TEK screws drive
into the horizontal leg of the 25×25×5mm L-angle bearers rather than bracket
arms.

**Left walkway** uses gravity retention only. The grating sits on twin support
lines (bearer beam at X=470mm and bearing strip at X=170mm) and is held in
position laterally by small guide tabs — 3mm steel angle pieces welded to the
bearer beam top surface. The twin support lines prevent rocking. No fasteners
are used because the left walkway must be removed quickly for hinged panel
transport mode — lift straight up and carry out.

---

## 9. Load Considerations

The walkway must support an operator (~100kg) plus portable equipment. The
critical load case is the widened near walkway section (500mm cantilever) with an
operator standing at the outer edge.

The standard 8mm steel plate gusset brackets at 457mm centers provide substantial
structural capacity. Each standard bracket is a rigid triangle (vertical leg +
horizontal arm + gusset) with 3x M12 through-bolts to the container rib. The two
widened brackets in the EP/battery zone use 10mm plate with 4x M12 rectangular
bolt patterns and 200mm vertical legs for the increased moment demand of the
500mm cantilever arm.

The ceiling-hung right walkway is the most compliant section. Five pairs of M10
threaded rod hangers (2,313mm free length) support the two bearer angles and
grating. Rod deflection under load is proportional to length — the 2.3m rods
will deflect more than the short cantilever brackets. However, the 300mm
walkway width limits the moment arm, and the 5-pair hanger arrangement
distributes load across multiple rods.

---

## 10. Parts List

| # | Item | Specification | Qty | Est. Cost |
|---|------|--------------|-----|-----------|
| 1 | Press-locked galvanized steel grating | 25mm thick, 30×3mm bearing bars at 34.2mm pitch | ~6.5 m² (4 sections) | $350–$550 |
| 2 | Cantilever bracket — standard (near/far) | 8mm steel plate: 150mm vert leg + 300mm arm + 70mm gusset, welded | ~16 (7 near + 9 far at 457mm centers) | $480–$800 |
| 3 | Cantilever bracket — widened (near) | 10mm steel plate: 200mm vert leg + 500mm arm + 70mm gusset, welded | ~2 (EP/battery zone) | $80–$140 |
| 4 | M12×80mm through-bolt kit | Hex bolt + 2× washers + nut, grade 8.8 | 56 (3 per std bracket + 4 per widened) | $85–$140 |
| 5 | Reinforcing plate (exterior) | 6mm steel: 100×180mm std (×16) + 120×220mm widened (×2) | 18 | $75–$130 |
| 6 | Bearer angle (right walkway) | 25×25×5mm steel L-angle, 2,362mm long | 2 | $40–$70 |
| 7 | M10 threaded rod | 2,313mm length (ceiling to bearer) | 10 (5 pairs) | $50–$80 |
| 8 | Ceiling bracket plate | 100×60×6mm steel | 10 | $30–$50 |
| 9 | M10 bolt kit (ceiling) | Through-bolt + nut + washer (ceiling attachment) | 20 (2 per plate) | $20–$35 |
| 10 | M10 nut + washer set (bearer) | Nut + washer above and below bearer flange, per rod | 20 sets | $15–$25 |
| 11 | Bearer beam (left walkway) | 50×50×3mm aluminum RHS, 1,762mm long | 1 | $25–$45 |
| 12 | Floor support leg | 25×25×3mm aluminum SHS, 75mm tall | 3 | $10–$20 |
| 13 | Foot plate | 60×60×3mm aluminum + 2mm rubber pad | 3 | $10–$15 |
| 14 | Bearing strip | 25×25×3mm aluminum angle, ~1,762mm long | 1 | $15–$25 |
| 15 | Anti-slip restraint kit | 5mm flat plate + stop lip + lock block + M8 thumb screw bolt per bearer end | 2 sets | $20–$35 |
| 16 | Grating clips | Removable spring clips, stainless | ~30 | $30–$50 |
| 17 | Plywood base plate (evap cooler stowage) | 12mm plywood, 600×350mm | 1 | $5–$10 |
| 18 | Ratchet strap (evap cooler) | 25mm×3m, 500kg WLL | 2 | $15–$25 |
| | **Total** | | | **$1,425–$2,365** |

---

## 11. Maintenance

| Interval | Task |
|----------|------|
| Before each session | Inspect all grating clips are seated; test left walkway lift-out for freedom of movement |
| Before each session | Check bearer beam anti-slip restraint — lock blocks secure, thumb screws tight |
| Monthly | Inspect cantilever bracket bolts for tightness (3× M12 std, 4× M12 widened) |
| Monthly | Check ceiling hanger nuts — ensure double-nut lock on bearer flange side |
| Monthly | Inspect grating for corrosion, damaged bearing bars, or bent cross bars |
| Quarterly | Inspect reinforcing plates (exterior) for corrosion — touch up paint if needed |
| Quarterly | Check right walkway hanger rods for straightness and thread condition |
| Before transport | Remove left walkway: lift grating, remove bearing strip and floor legs, unbolt bearer beam |
| Before transport | Verify evap cooler ratchet straps to bracket arms; check anti-slide cleats |
| After transport | Reinstall left walkway in reverse order; check all sections for level deck |

---

## 12. Source References

1. [ISO 668:2020](https://www.iso.org/standard/76912.html) — Series 1 freight containers: Classification, dimensions and ratings.
   Container rib spacing 457mm (18").
2. [ANSI/NAAMM MBG 531](https://www.naamm.org/publications/metal-bar-grating-manual) — Metal bar grating manual. Press-locked grating design.
3. [AS 1657-2018](https://www.standards.org.au/standards-catalogue/sa-snz/building/me-064/as--1657-2018) — Fixed platforms, walkways, stairways and ladders: Design,
   construction and installation. 300mm minimum clear width for walkways.
4. [Shurflo 2088 Series datasheet](https://www.shurflo.com/products/2088-series) — Pump dimensions for manifold access clearance.
5. [Equipment Layout Report](equipment-layout-report.md) — Component positions
   and access requirements.
6. [Processing Tray & Spray Bar Report](processing-tray-and-spray-bar.md) — Tray
   dimensions, rim height, spray bar slit requirements.
7. [Hinged Panel Report](hinged-panel-report.md) — Panel transport envelope,
   slide travel, floor gap.
8. [Light Trap Selection Report](light-trap-selection.md) — Panel and drum
   dimensions at cargo door end.
9. [IBC Stacking Report](ibc-stacking-report.md) — IBC stack dimensions and
   floor zone clearance requirements.
