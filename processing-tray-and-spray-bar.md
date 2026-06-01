<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Processing Tray & Spray Bar Assembly

## 1. Purpose

Cyanotype prints on muslin substrate (4499 × 2388mm) require a controlled flood wash
to remove unexposed sensitizer chemistry after UV exposure. The processing tray provides
the containment surface and the spray bar delivers even water distribution across the
full print width. Together they form the print washing subsystem of the
[water system](water-system-report.md).

**Design goals:**

- Flood the entire print surface uniformly in a single pass (~44 seconds)
- Contain all wash water within a sealed tray — no penetration of the container floor
- Drain water to a sump for pump-out and recycling via the Brown circuit
- Single-operator use from the walkway — no stepping on the print surface
- Permanently installed — no removal required for transport mode conversion

---

## 2. Processing Tray

### 2.1 Specification

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Material | 16-gauge (1.5mm) 304 stainless steel, #4 brushed finish | Chemically inert to ferricyanide wash water; resists pitting from citric acid pH adjustment |
| Overall footprint | 4459 × 2200mm (2 panels, field-bolted) | Fits inside film plane rails (X=150–4,649) with 20mm clearance per side |
| Position | X=170–4,629, Yd=80–2,280 | Between film plane rails, inboard of walkway perimeter |
| Panel size (each) | 2229 × 2200mm | Two equal panels, butted at midpoint with silicone gasket + bolted flange. Each panel fits through the cargo door opening (2340 × 2280mm) |
| Rim height | 50mm (all four sides) | Contains 6mm flood depth with margin; constrained to ≤75mm by film plane carriage clearance |
| Floor-to-rim height | 50mm | Tray sits on tapered HDPE shim strips on the container floor |
| Fall | 1:200 dual-axis (10mm over 2200mm Yd + 11mm over 2229mm X) toward sump | Water converges from both axes toward the sump well |
| Sump well | 150 × 100mm, 20mm deep, pressed into tray floor at low point | Collects water at lowest point; P-04 suction pickup sits in sump |
| Weight (empty) | ~116 kg (2 panels × ~58 kg) | 304 SS, 1.5mm × 4.90 m² per panel × 7.93 kg/m² per mm |
| Weight (operating, 6mm flood) | ~233 kg | Tray + ~117 kg water |

### 2.2 Slope Support — Tapered HDPE Shim Strips

The tray's 1:200 dual-axis slope is achieved by tapered HDPE shim strips bonded to the
container floor beneath the tray. No risers, no under-tray plumbing — the tray sits
directly on the shims to flow the water into the bottom right for pickup by the sump pump.

![Water System — Sheet 3: Drainage Plan](assets/water-system-sheet3.png)

| Parameter | Value |
|-----------|-------|
| Material | HDPE flat bar, 50mm wide |
| Quantity | 5 strips running full tray depth (Yd direction, 2200mm each) |
| Spacing | ~1000mm apart across tray width (X direction) |
| Profile | Tapered: 0mm at near rim (Yd=80, drain end) → 10mm at far rim (Yd=2,280) |
| Attachment | Construction adhesive (Loctite PL Premium or equivalent) to container floor |
| Function | Creates the Yd-axis slope; X-axis slope is formed into the tray panels during fabrication (pressed crown) |

### 2.3 Sump Well and Pickup

Instead of a through-floor drain fitting, the tray has a shallow sump well pressed into
the floor at the low point. P-04 draws water from the sump via a suction pickup tube —
no penetration of the tray floor or the container floor.

![Water System — Sheet 4: Drain Cross-Section](assets/water-system-sheet4.png)

| Parameter | Value |
|-----------|-------|
| Sump dimensions | 150mm (X) × 100mm (Yd) × 20mm deep |
| Sump location | X=2,399 (tray center), Yd=80 (near rim, low point) |
| Forming | Pressed/stamped into tray panel during fabrication |
| Pickup tube | 1" HDPE dip tube, stainless foot valve with strainer screen |
| Pickup height | Tube bottom 5mm above sump floor (leaves ~0.75 L residual) |
| Suction line | 1" flexible reinforced hose, routed over near rim to P-04 |
| Pump | P-04 (Shurflo 2088, 12V DC, 3.5 GPM, 45 PSI, self-priming) |
| Discharge | P-04 → 3W-DV-02 diverter → IBC-3 (Brown recycling) or IBC-4 (Waste) |

**Why sump pickup instead of a through-floor drain:**

1. **No penetration** — eliminates leak risk from a bulkhead fitting seal
2. **No under-tray clearance needed** — tray sits flat on shim strips
3. **Simpler fabrication** — pressed sump is cheaper and more reliable than a welded bulkhead union
4. **Easier to protect** — no exposed plumbing beneath the tray during transport
5. **Field-serviceable** — pickup tube lifts out for cleaning; no tools required

### 2.4 Containment Liner

A fresh 6-mil black LDPE sheet is laid over the tray surface before each session. The
liner prevents direct stainless-to-print contact (avoiding metallic marks on wet
cyanotype) and simplifies cleanup. Overlap the liner 50mm over the tray rims. Cut or
fold the liner around the sump pickup tube.

### 2.5 Clearance Verification

| Constraint | Clearance | Status |
|------------|-----------|--------|
| Film plane carriage blocks (Z=140mm at max tilt) | 90mm above tray rim (140 − 50) | Clear |
| Film plane rails at X=150 and X=4,649 | 20mm gap between tray edge and rail | Clear |
| Spray bar (rides on tray floor beneath walkway grating) | Spacer top at Z=42.5mm, grating bottom at Z=75mm | Clear |
| IBCs (X=4,674+, right end zone) | Tray ends at X=4,629 — 45mm gap | Clear |
| Pump manifold (equipment panel at Yd=1,046) | Suction hose routes over near rim exterior | Clear |

### 2.6 Permanent Installation

The processing tray is permanently installed — it remains in place during both
operational and transport modes. The two panels are positioned between the film plane
rails, bolted together at the center flange. The P-04 suction pickup tube sits in the
sump well permanently. The 50mm rim height is below all transport-mode clearance
envelopes, so no removal is required for mode conversion. This eliminates the former
15–20 minute tray install/remove step; mode conversion now requires only the panel slide
(~5 minutes).

---

## 3. Spray Bar Assembly — Gantry Design

### 3.1 Design Concept

The spray bar delivers Blue (clean) water evenly across the processing tray during print
washing. The operator slides the bar along the tray (Yd direction, from film-plane side
toward the pinhole wall), flooding the print surface progressively.

![Sheet 1 — Gantry Elevation](assets/spray-bar-sheet1.png)

The beam spans 3859mm between the inner edges of the left and right walkways
(X=470 to X=4,329), extending under the walkway grating at each end. At each end, a
two-wheel carriage rolls on the processing tray floor beneath the grating. A 3/4" LDPE
irrigation poly pipe inside the aluminum SHS bore serves as the spray pipe — water
enters through a barbed center feed fitting and exits through six barbed flat-fan
irrigation nozzles spaced evenly along the beam bottom face.

![Sheet 2 — Cross Section: Beam Assembly](assets/spray-bar-sheet2.png)

**Design constraints:**

- Carriage plate top must clear walkway grating underside (Z=75mm) — no contact during travel
- Wheels must fit within the 50mm tray rim height, rolling on the tray floor beneath walkways
- Single-operator use — push/pull from the near walkway via telescoping pole through a 30mm slit
- Must travel 2200mm along Yd (tray depth, near rim to far rim)
- Tray rim walls provide lateral guidance — no separate guide rails required
- Must accommodate a flexible water connection that follows the bar as it moves

### 3.2 Assembly Components

| Component | Specification | Qty | Purpose |
|-----------|--------------|-----|---------|
| Beam | 6061-T6 AL SHS, 40×40×3mm, 3859mm long (two 8 ft lengths joined with splice sleeve) | 1 | Structural beam housing internal spray pipe |
| Internal spray pipe | 3/4" LDPE irrigation poly pipe (OD 25mm, ID 19mm) | 1 | Water distribution inside beam bore |
| Flat-fan spray nozzles | Barbed inlet, irrigation-type, 180° fan pattern | 6 | Spray distribution through beam bottom wall |
| Barbed center feed fitting | 3/4" barb × 1/2" barb adapter, through beam top wall | 1 | Center feed — connects flex hose to poly pipe |
| Retainer clips | SS or nylon, for 3/4" LDPE fold-back closure | 2 | Seal both ends of poly pipe (fold-back termination) |
| [Nylon skate wheels](https://www.mcmaster.com/products/rollers/skate-wheels-1~/) | 50mm OD × 20mm wide, 10mm bore, flat tread | 8 | Roll on tray floor beneath walkway grating (2 pairs per carriage) |
| [Axle pins (4-pack)](https://www.amazon.com/uxcell-Single-Hole-Clevis-Pins/dp/B0816MQ5T6) | 10mm × 60mm 304 SS clevis pin, flat head, single hole | 8 (2 packs) | Wheel spindles |
| [Axle retention saddle clamps (10-pack)](https://www.amazon.com/Boxonly-Fixing-Stainless-Saddle-Tension/dp/B0CG1CNQKX) | 304 SS, 10mm, two-hole U-shaped strap | 8 | Bolted to carriage plate underside, retains axle in position |
| Carriage plates | 6061-T6 AL plate 5mm, notched for U-clamp | 2 | Connect wheel forks to beam via spacer + U-clamp |
| Spacer blocks | 6061-T6 AL, 8.5mm thick, under U-clamp feet | 4 | Raise U-clamp seat from plate top (Z=34) to beam center height (Z=42.5) |
| U-clamps | SS, under-slung, flared feet + wing nuts — cradles 40mm SHS from below | 2 | Attach beam to carriage plate, tool-free adjustment |
| Ball joint | Ø20mm SS ball, zinc socket, M12 stud, 50mm flange | 1 | Multi-axis arm articulation on beam top face |
| M8 U-bolt | SS, wraps over ball joint socket, nyloc nuts | 1 | Clamps ball joint to beam |
| Arm tube | 6061-T6 AL round tube, 25mm OD × 2mm wall, ~500mm | 1 | Vertical arm from ball joint to pole |
| M6 pinch bolt | SS hex bolt + nut | 1 | Clamps arm tube onto ball joint stud |
| Push pole | Telescoping aluminum pool pole, 1.2–2.4 m | 1 | Operator controls bar position from walkway |
| Flexible hose | 1/2" reinforced braided PVC, ~4 m coiled | 1 | Connects BV-02 to center feed barbed fitting |
| Zip ties | Nylon, 200mm | ~6 | Secure flex hose to arm tube |

### 3.3 Beam / Spray Pipe

The structural beam houses a 3/4" LDPE irrigation poly pipe for water distribution. A single 6061-T6 aluminum
SHS (40×40×3mm, imperial 1-1/2" × 1-1/2" × 1/8") spans 3859mm between the inner
edges of the left and right walkways.

**Beam properties:**

| Property | Value |
|----------|-------|
| Material | 6061-T6 aluminum alloy |
| Section | 40×40×3mm SHS (1-1/2" × 1-1/2" × 1/8") |
| Internal bore | 34×34mm |
| Span | 3859mm (X=470 to X=4,329) |
| Second moment of area (I) | 101972mm⁴ |
| Cross-sectional area | 444mm² |
| Linear mass (beam only) | 1.20 kg/m |
| Beam mass (3859mm) | 4.63 kg |

**Sourcing:** Standard 8 ft (2438mm) lengths are widely stocked at Home Depot, Online
Metals, and metals suppliers. Two 8 ft lengths are required; see §3.8 for splice joint.

**Spray nozzles:**

| Property | Value |
|----------|-------|
| Nozzle type | Flat-fan irrigation nozzle, barbed inlet |
| Number of nozzles | 6 |
| Nozzle spacing | ~640mm center-to-center |
| Spray pattern | 180° flat fan |
| Pipe OD / ID | 25mm / 19mm (3/4" LDPE) |
| Bore clearance | 4.5mm per side (pipe loose in 34mm bore) |

The six barbed fittings (plus the center feed fitting) pass through drilled holes
in the beam wall and grip the LDPE pipe by their barb ridges. These seven through-wall
fittings act as locating pins, preventing the poly pipe from sliding or rotating
inside the oversized bore — no additional pipe restraint is needed.

**Beam ends (open):**

The aluminum SHS ends are left open — no end caps or welding. The internal 3/4" LDPE
poly pipe terminates at each beam end with a standard fold-back closure: the pipe
folds 180° back on itself and is secured with a stainless steel or nylon retainer
clip (see Sheet 4, Detail A). The fold-back and retainer clip provide a watertight
seal; the aluminum SHS serves only as structural housing.

- **Feed end (center, X=2500):** Barbed center feed fitting installed through the
  beam top wall — connects flex hose from BV-02 to the poly pipe bore.
- **Both ends (X=470 and X=4,329):** LDPE fold-back with retainer clip — fully sealed.

### 3.4 Wheel Carriage Assemblies

Each end of the beam is supported by a wheel carriage that rolls on the processing tray
floor beneath the walkway grating. Two carriages (left and right), each carrying two
wheels spaced 200mm apart in the Yd direction for stability against tipping.

**Wheel specification:**

| Property | Value |
|----------|-------|
| Type | Fixed (non-swivel) nylon wheel |
| Diameter | 50mm |
| Width | 20mm |
| Bore | 10mm |
| Load rating | ≥25 kg per wheel (actual load ~2.6 kg per wheel wet) |
| Tread profile | Flat (rolls on flat stainless tray floor) |
| Material | Glass-filled nylon or Delrin |

**Vertical geometry (all dimensions mm above finished floor):**

| Reference point | Z (mm AFF) |
|-----------------|------------|
| Container floor | 0 |
| Tray floor (SS sheet on floor) | ~2 |
| Nozzle bottom (6mm body) | 14 |
| Beam bottom | 20 |
| Wheel axle centerline | 27 |
| Carriage plate bottom | 29 |
| Carriage plate top | 34 |
| Spacer block top / U-clamp seat | 42.5 |
| Tray rim top | 50 |
| Wheel top | 52 |
| Beam top | 60 |
| Walkway grating bottom | 75 |
| Walkway grating top (deck surface) | 100 |

**Clearances:**

| Interface | Gap | Notes |
|-----------|-----|-------|
| Spacer top → grating bottom | 32.5mm | Ample clearance; no contact during travel |
| Beam bottom → tray floor | 18mm | Reduces to ~11mm at midspan under full water load (see §3.7) |
| Nozzle bottom → tray floor | 12mm | Nozzle body clears floor at all carriage positions |
| Wheel top → grating bottom | 23mm | Wheels roll freely under grating |

**Axle retention:** Each wheel axle (10mm SS clevis pin) is held by a SS U-clamp
(2mm strap) bolted to the underside of the carriage plate. The U-clamp wraps under
the axle pin with 1mm clearance, and through-bolts pass up through the clamp legs
and carriage plate to secure the axle in position.

### 3.5 Carriage Plate Design

Each carriage uses a flat aluminum plate positioned 2mm above the wheel axle (Z=29–34mm).
The plate has a central notch that straddles the beam U-clamp legs. Aluminum spacer
blocks (8.5mm tall) sit on the plate wings beneath the U-clamp feet, raising the
U-clamp seat to Z=42.5mm so the beam remains at its design height (Z=20–60mm).

Formed from 5mm 6061-T6 aluminum plate:

- **Plate wings:** Two flat sections extending outward from the beam notch to the
  wheel fork attachment points. Total plate width spans both wheel fork positions
  plus 18mm overhang on each side.
- **Center notch:** Cut-out slightly wider than the U-clamp outer width, allowing
  the clamp legs to pass through the plate and grip the beam.
- **Spacer blocks:** Two 8.5mm aluminum blocks, one per U-clamp foot, bolted through
  the plate with the U-clamp bolts. Raise the effective clamp seat from plate top
  (Z=34mm) to the beam center height (Z=42.5mm).
- **Ball joint mount:** The ball joint flange bolts to the beam top face (Z=60mm),
  keeping the socket housing below grating level (Z=75mm).

**Lateral guidance:** The tray rim walls (50mm high, at X=170 and X=4,629) act as
lateral guides. The wheel carriages roll between the tray rim and the walkway support
structure. The 200mm wheel spacing in Yd prevents significant skew.

### 3.6 Carriage Fabrication

Each carriage is built from two sub-assemblies: a carriage plate with spacer blocks,
and four wheel-and-axle units retained by U-clamps. Two identical carriages are
required (left end and right end of beam).

![Sheet 2 — Cross Section: Beam Assembly](assets/spray-bar-sheet2.png)

#### 3.6.1 Carriage Plate Fabrication (2 required)

Each carriage plate is a flat 5mm 6061-T6 aluminum plate with a central notch for the
beam U-clamp. The plate sits 2mm above the wheel axle (Z=29–34mm), connecting the
wheels to the beam via spacer blocks and beam U-clamp.

**Blank:** Cut two pieces from 5mm plate, each 280mm long × 60mm wide.

| Step | Operation | Detail |
|------|-----------|--------|
| 1 | Mark notch | Scribe center notch outline — width matches beam U-clamp outer span plus 1mm clearance each side |
| 2 | Cut notch | Jigsaw or bandsaw the center notch from one long edge |
| 3 | Mark axle U-clamp positions | On each wing, mark two Ø5.5mm clearance holes (M5) per wheel position for axle retention U-clamps |
| 4 | Mark beam U-clamp bolt positions | Two Ø5.5mm holes on each side of the notch, aligning with beam U-clamp flared feet |
| 5 | Drill all holes | Drill press for accuracy — 8 axle U-clamp holes + 4 beam U-clamp holes total |
| 6 | Deburr | Remove all burrs from edges, notch, and holes |

#### 3.6.2 Wheel Assembly (4 required)

![Sheet 5 — Detail C: Wheel Attachment](assets/spray-bar-sheet5.png)

Each wheel is retained by a SS U-clamp (2mm strap) bolted to the carriage plate
underside. The U-clamp wraps under the 10mm axle pin with 1mm clearance.

| Step | Operation |
|------|-----------|
| 1 | Place nylon wheel (50mm × 20mm, 10mm bore) in position under the carriage plate |
| 2 | Insert 10mm SS clevis pin through wheel bore |
| 3 | Position axle retention U-clamp under the axle, legs facing up toward plate |
| 4 | Insert 2× M5 bolts up through U-clamp legs and carriage plate; secure with nyloc nuts on top |
| 5 | Tighten finger-tight only until all four wheels are installed |
| 6 | Spin wheel by hand — confirm free rotation with no lateral wobble |

#### 3.6.3 Carriage Assembly (2 required)

![Sheet 6 — Detail D: Wheel Plan](assets/spray-bar-sheet6.png)

| Step | Operation |
|------|-----------|
| 1 | Place carriage plate flat on bench, notch centered |
| 2 | Install first wheel-and-U-clamp unit on the near wing (wheel hanging below bench edge) — finger-tight |
| 3 | Repeat for the second wheel on the near wing (200mm Yd spacing) |
| 4 | Repeat for both wheels on the far wing |
| 5 | Verify 200mm wheel spacing (center-to-center, Yd direction) |
| 6 | Tighten all nyloc nuts to 4 Nm |
| 7 | Stand the carriage on a flat surface — all four wheels must contact simultaneously. Shim if needed before final torque |

#### 3.6.5 Beam Attachment

The carriages attach to the beam using SS U-clamps in a cradle configuration. The
U-clamp wraps under the beam from below, with its legs passing up through the carriage
plate notch and flared feet resting on top of the spacer blocks. Bolts pass through the
U-clamp feet, spacer blocks, and carriage plate; wing nuts thread on below. This
provides tool-free adjustment of the carriage position along the beam.

| Step | Operation |
|------|-----------|
| 1 | Slide one U-clamp under the beam SHS approximately 30mm from each end |
| 2 | Lower the carriage plate over the beam so the notch straddles the U-clamp legs |
| 3 | Align the U-clamp flared feet against the carriage plate underside |
| 4 | Pass bolts through the plate from above, through the U-clamp feet |
| 5 | Thread wing nuts onto each bolt below the feet and tighten by hand until the clamp grips the beam firmly |
| 6 | Set the assembled spray bar on the processing tray floor. Confirm plate top (Z=42.5mm) clears walkway grating bottom (Z=75mm) — 32.5mm gap. Confirm all wheels roll freely on the tray floor |
| 7 | Push the bar through its full 2200mm Yd travel to verify it tracks straight between the tray rim walls without binding |

### 3.7 Structural Analysis

**Loading (simply supported, uniform distributed load across 3859mm span):**

| Component | Linear mass (kg/m) | Linear weight (N/m) |
|-----------|-------------------|---------------------|
| Beam (6061-T6 AL, 40×40×3mm SHS) | 1.199 | 11.76 |
| LDPE pipe (OD 25mm, ID 19mm, wall 3mm) | 0.193 | 1.89 |
| Water in pipe (19mm ID bore) | 0.283 | 2.78 |
| **Total UDL** | **1.675** | **16.43** |

Water volume in pipe: π × 9.5² × 3,859 = 1.09 liters (1.09 kg). The water is contained
within the LDPE pipe bore, not the full SHS bore.

**Deflection — δ = 5wL⁴ / 384EI, E = 68,900 MPa:**

| Condition | w (N/m) | δ center (mm) | Span ratio |
|-----------|---------|---------------|------------|
| Dry (beam only) | 11.76 | 4.8 | L/799 |
| Dry (beam + pipe) | 13.65 | 5.6 | L/689 |
| Wet (beam + pipe + water) | 16.43 | 6.8 | L/568 |

The L/568 span ratio under full water load is acceptable for a spray bar application —
no foot traffic, precision loads, or dynamic impact. The deflection is entirely elastic
and fully recoverable. With 18mm beam-to-floor clearance at the supports, midspan
clearance under full load is approximately 11mm.

**Pre-camber recommendation:** Apply 3mm upward pre-camber during fabrication to offset
roughly half the wet deflection. Method: introduce the camber at the midspan splice
joint (§3.8) — shim the sleeve 3mm off-axis during set-screw tightening so the two SHS
halves meet at a shallow upward angle.

**Weight summary:**

| Component | Mass (kg) |
|-----------|-----------|
| Beam (40×40×3mm × 3859mm) | 4.63 |
| LDPE pipe (OD 25mm × 3859mm) | 0.74 |
| Water in pipe | 1.09 |
| Carriage plates (2×) | 0.35 |
| Wheel assemblies (4× wheel + fork + axle) | 0.60 |
| Nozzles + fittings | 0.15 |
| Hardware (bolts, clips, U-clamps) | 0.30 |
| **Dry total** | **~6.8 kg** |
| **Wet total (operating)** | **~7.9 kg** |

Per wheel load (wet): 7.9 / 4 = 2.0 kg — well within any small nylon wheel's rating.

### 3.8 Beam Splice Joint

Two 8 ft (2438mm) SHS lengths are joined with an internal sleeve splice at midspan:

- **Sleeve:** 150mm of 30×30mm solid aluminum bar stock, inserted into the 34×34mm bore (2mm clearance per side)
- **Sealant:** Marine-grade RTV silicone on sleeve exterior — watertight, allows future disassembly with heat
- **Fastening:** 2× M5 set screws through SHS wall on each side (4 total), engaging dimples in sleeve
- **Location:** Midspan (1930mm from each end). The solid bar has higher I than the hollow beam wall, so the splice is not the weak point.

**Alternative:** Source a single 16 ft or 20 ft length by special order to eliminate
the splice entirely.

### 3.9 Flow Analysis

| Parameter | Value |
|-----------|-------|
| Supply pump | P-01 (Shurflo 2088), 3.5 GPM at 45 PSI |
| Pipe bore (LDPE) | 19mm ID = 283.5mm² |
| Pipe inlet velocity | 0.78 m/s (at 3.5 GPM) |
| Spray nozzles | 6 × flat-fan irrigation nozzles |
| Flow per nozzle | 0.58 GPM (2.2 L/min) |

The center feed position minimizes pipe friction losses by splitting flow equally to
three nozzles on each side. The 19mm bore provides adequate flow capacity at 3.5 GPM.
Each irrigation nozzle delivers a 180° flat fan pattern, providing overlapping coverage
along the 3859mm beam span.

### 3.10 Water Connection

BV-02 (1/2" ball valve, Blue supply isolation) is mounted on the pinhole wall (Yd=0) at
X=2399mm (pinhole centerline), Z=900mm — waist height from the walkway deck. A
1/2" HDPE riser runs from the Blue supply trunk up to BV-02. A 4 m length of 1/2"
reinforced braided PVC hose connects from BV-02 down to the beam's center feed barbed
fitting. The hose coils when the bar is near the pinhole wall and extends as the bar is
pushed toward the far wall. The hose trails along the near tray rim, staying clear of
the print surface.

![Sheet 7 — Detail B: Center Feed Connection](assets/spray-bar-sheet7.png)

**Supply path:** P-01 → ACC-01 → rigid 1/2" HDPE pipe along pinhole wall → BV-02 →
coiled flexible hose → barbed center feed → poly pipe bore → 6× spray nozzles.

### 3.11 Walkway Slit

The operator controls the spray bar position from the near walkway using a telescoping
aluminum pool pole (1.2–2.4 m). The pole passes through a 30mm wide slit cut into the
walkway grating at the beam centerline X=2500mm. A matching slit is cut into the far
walkway grating at the same X position. The slit positions are shown on the
[walkway plan view](engineering-diagrams.md#14-perimeter-walkway).

![Sheet 3 — Plan View: Walkways & Slit Positions](assets/spray-bar-sheet3.png)

### 3.12 Ball Joint and Arm

A Ø20mm stainless steel ball joint on the beam top face provides multi-axis
articulation between the beam and the operator's pole. The ball sits in a zinc socket
housing (M12 stud, 50mm flange), clamped to the beam with an M8 stainless U-bolt and
nyloc nuts.

A 25mm OD × 2mm wall aluminum round tube (~500mm long) connects from the ball joint
stud to the telescoping pole. An M6 pinch bolt clamps the arm tube onto the stud. The
1/2" flexible hose is zip-tied to the arm tube at ~200mm intervals.

---

## 4. Operation

The step-by-step spray bar setup, wash pass procedure, Brown water recycling passes, and storage are documented in the [Operating Manual — Phase 4: Development](operating-manual.md#42-development-in-water).

---

## 5. Engineering Drawings

Seven detail sheets cover the spray bar assembly and processing tray:

| Sheet | Title | Content |
|-------|-------|---------|
| 1 | Gantry Elevation | X-Z section from film plane (4× vert exag) — beam, BV-02, pole, walkway slit, operator silhouette |
| 2 | Cross Section — Beam Assembly | Yd-Z composite at 1:1 — wheels, L-bracket, U-clamp, ball joint, arm, hose |
| 3 | Plan View | Container floor plan — walkways, slit positions, beam travel range |
| 4 | Detail A — Beam End | Longitudinal section at 2:1 — LDPE fold-back end closure with retainer clip |
| 5 | Detail C — Wheel Attachment | Section along axle at 2:1 — fork arms, nylon wheel, axle pin, snap rings |
| 6 | Detail D — Wheel Plan | Plan view of carriage — beam, L-bracket arm, U-clamp, wheels |
| 7 | Detail B — Center Feed | Longitudinal section at 2:1 — barbed center feed and nozzle connection details |

![Sheet 1 — Gantry Elevation](assets/spray-bar-sheet1.png)

![Sheet 2 — Cross Section: Beam Assembly](assets/spray-bar-sheet2.png)

![Sheet 3 — Plan View: Walkways & Slit Positions](assets/spray-bar-sheet3.png)

![Sheet 4 — Detail A: Beam End](assets/spray-bar-sheet4.png)

![Sheet 5 — Detail C: Wheel Attachment](assets/spray-bar-sheet5.png)

![Sheet 6 — Detail D: Wheel Plan](assets/spray-bar-sheet6.png)

![Sheet 7 — Detail B: Center Feed Connection](assets/spray-bar-sheet7.png)

Additional processing tray drainage detail is shown in the
[water system drawings](engineering-diagrams.md#9-processing-water-system) (sheets 3–4:
tray drainage plan and sump cross-section).

---

## 6. Parts List

### 6.1 Processing Tray

| Item | Specification | Qty | Est. Cost |
|------|--------------|-----|-----------|
| 304 SS sheet, 16-gauge (1.5mm), #4 brushed | 2229 × 2200mm panels | 2 | $720–$1,000 |
| Fabrication (cut, brake, weld, press sump) | Two panels with center flange + sump well | 1 lot | $450–$850 |
| HDPE flat bar, 50mm wide | Tapered shim strips, 2200mm each | 5 | $40–$75 |
| Loctite PL Premium construction adhesive | Shim-to-floor bond | 2 tubes | $15 |
| 1" SS foot valve with strainer screen | Sump pickup tube | 1 | $20 |
| 1" reinforced suction hose, 6 ft | Pickup tube to P-04 | 1 | $15 |
| Silicone gasket strip | Center flange seal | 1 | $20 |
| M6 SS hex bolts + flange nuts | Panel flange bolts | 12 | $12 |
| 6-mil black LDPE sheet, 10 ft × 8 ft | Containment liner (consumable, per session) | 1 | $8 |
| **Tray subtotal** | | | **$1,300–$2,015** |

### 6.2 Spray Bar Assembly

| Item | Specification | Qty | Est. Cost |
|------|--------------|-----|-----------|
| 6061-T6 AL SHS 1-1/2" × 1-1/2" × 1/8", 8 ft | 40×40×3mm, joined with internal sleeve | 2 | $36–$56 |
| 6061-T6 AL plate 3/16" (5mm) | Carriage plates + spacer blocks (~300 × 500mm sheet) | 1 | $15–$25 |
| 30×30mm AL solid bar, 150mm | Internal splice sleeve | 1 | $8–$12 |
| 3/4" LDPE irrigation poly pipe, 15 ft | Internal spray pipe (OD 25mm, ID 19mm) | 1 | $10 |
| Flat-fan irrigation spray nozzles, barbed | 180° fan pattern, barbed inlet | 6 | $18 |
| 3/4" barb × 1/2" barb adapter | Center feed through beam top wall | 1 | $4 |
| SS/nylon retainer clips for 3/4" LDPE | Fold-back end closures | 2 | $4 |
| [Nylon skate wheel, 50mm × 20mm, 10mm bore](https://www.mcmaster.com/products/rollers/skate-wheels-1~/) | Flat tread, ≥25 kg rated (2 pairs per carriage) | 8 | $24–$40 |
| 1/2" barb × 1/2" hose barb, brass | Flex hose to center feed adapter | 1 | $4 |
| Telescoping aluminum pool pole, 4–8 ft | Standard pool skimmer handle | 1 | $15 |
| 1/2" reinforced braided PVC hose, 15 ft | BV-02 to beam feed (4 m coiled) | 1 | $15 |
| [10mm × 60mm 304 SS clevis pin (4-pack)](https://www.amazon.com/uxcell-Single-Hole-Clevis-Pins/dp/B0816MQ5T6) | Wheel axle pins | 8 (2 packs) | $10 |
| [304 SS saddle clamp, 10mm (10-pack)](https://www.amazon.com/Boxonly-Fixing-Stainless-Saddle-Tension/dp/B0CG1CNQKX) | Axle retention, bolted to plate underside | 8 | $10 |
| M6×20 SS bolts + nyloc nuts | Carriage plate, axle U-clamp, splice fasteners | 16 | $7 |
| M8 SS U-bolt + nyloc nuts | Ball joint to beam clamp | 1 | $5 |
| Ø20mm ball joint, zinc socket, M12 stud | Multi-axis arm articulation | 1 | $12 |
| SS U-clamp, flared legs, wing nuts (40mm) | Beam to carriage plate (tool-free) | 2 | $10 |
| 6061-T6 AL round tube 25mm OD × 2mm wall, 500mm | Arm tube | 1 | $6 |
| M6 SS hex bolt + nut | Pinch bolt for arm tube | 1 | $1 |
| Nylon zip ties, 200mm | Hose to arm tube | 6 | $1 |
| **Spray bar subtotal** | | | **$216–$268** |

### 6.3 Combined Total

| Subsystem | Cost Range |
|-----------|-----------|
| Processing tray | $1,300–$2,015 |
| Spray bar assembly | $216–$268 |
| **Total** | **$1,516–$2,283** |

---

## 7. Maintenance

| Task | Interval | Procedure |
|------|----------|-----------|
| Tray wipe-down | After each session | Remove LDPE liner, wipe tray with damp cloth, inspect sump for debris |
| Sump pickup clean | Monthly | Lift pickup tube, rinse strainer screen, check foot valve seal |
| Spray nozzles | Monthly | Flush beam bore with clean water; remove and soak nozzles in vinegar to clear mineral deposits |
| Wheel inspection | Quarterly | Check for flat spots, debris in tread, axle pin retention |
| Hose inspection | Quarterly | Check for kinks, abrasion, fitting tightness |
| Tray panel flange | Annually | Inspect silicone gasket, retighten flange bolts if needed |

---

## 8. Source References

- [Shurflo 2088 Series datasheet](https://www.shurflo.com/products/2088-series) — SHURflo / Pentair. Performance curves, priming capability, electrical specifications.
- [6061-T6 aluminum SHS](https://www.onlinemetals.com/en/buy/aluminum/6061-t6-aluminum-square-tube) — Metals Depot / Online Metals catalog. Mechanical properties per [ASTM B221](https://www.astm.org/b0221-21.html).
- [304 stainless steel sheet](https://www.onlinemetals.com/en/buy/stainless-steel/304-stainless-steel-sheet) — AK Steel Product Data Bulletin. Chemical resistance, mechanical properties per [ASTM A240](https://www.astm.org/a0240_a0240m-22a.html).
- [HDPE chemical resistance](https://www.cpchem.com/what-we-do/solutions/polyethylene/polyethylene-resources) — Chevron Phillips Chemical Company. Flat bar available from [McMaster-Carr (catalog #8619K)](https://www.mcmaster.com/8619K).
- **Cyanotype chemistry** — Ware, Mike. [*Cyanotype: The History, Science & Art of Photographic Printing in Prussian Blue*](https://www.mikeware.co.uk/mikeware/Cyanotype_Monograph.html) (2014). Wash water composition and pH requirements.

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
