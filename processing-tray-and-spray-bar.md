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
| Spray bar (rides on tray floor beneath walkway grating) | Top clamp plate at Z=63mm (nut ~66mm), grating bottom at Z=75mm | Clear |
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
enters through a barbed center feed fitting and exits through twenty-six barbed flat-fan
irrigation nozzles at 150mm pitch along the beam bottom face.

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
| Flat-fan spray nozzles | Barbed inlet, irrigation-type, 180° fan pattern | 26 | Spray distribution through beam bottom wall (150mm pitch) |
| Barbed center feed fitting | 3/4" barb × 1/2" barb adapter, through beam top wall | 1 | Center feed — connects flex hose to poly pipe |
| Retainer clips | SS or nylon, for 3/4" LDPE fold-back closure | 2 | Seal both ends of poly pipe (fold-back termination) |
| [Nylon skate wheels](https://www.mcmaster.com/products/rollers/skate-wheels-1~/) | 50mm OD × 20mm wide, 10mm bore, flat tread | 4 | Roll on tray floor beneath walkway grating (2 per carriage, 200mm Yd spacing) |
| [Axle pins (4-pack)](https://www.amazon.com/uxcell-Single-Hole-Clevis-Pins/dp/B0816MQ5T6) | 10mm × 60mm 304 SS axle pin, flat head | 4 (1 pack) | Wheel spindles |
| [Axle retention saddle clamps (10-pack)](https://www.amazon.com/Boxonly-Fixing-Stainless-Saddle-Tension/dp/B0CG1CNQKX) | 304 SS, curved conduit-style saddle, 10mm, two bolt holes | 8 | Retain the wheel axles — bolted to the carriage plate underside |
| Carriage plates | 6061-T6 AL plate 5mm, wings extend in to meet beam faces | 2 | Carry wheels; captured between beam clamp plates |
| Beam clamp plates | SS, top + bottom plate (~3mm) sandwiching the 40mm SHS | 4 (2 per carriage) | Clamp beam to carriage plate, bolted vertically |
| Spacer blocks | 6061-T6 AL, between top & bottom clamp plates, one each side of beam | 4 | Set clamp gap to beam height so bolts grip the beam rather than bend the plates |
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
| Number of nozzles | 26 |
| Nozzle spacing | 150mm center-to-center |
| Spray pattern | 180° flat fan |
| Pipe OD / ID | 25mm / 19mm (3/4" LDPE) |
| Bore clearance | 4.5mm per side (pipe loose in 34mm bore) |

The twenty-six barbed fittings (plus the center feed fitting) pass through drilled holes
in the beam wall and grip the LDPE pipe by their barb ridges. These twenty-seven through-wall
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
| Bottom clamp plate (under beam) | 17–20 |
| Nozzle bottom (6mm body) | 14 |
| Beam bottom | 20 |
| Wheel axle centerline | 27 |
| Carriage plate bottom | 29 |
| Carriage plate top | 34 |
| Tray rim top | 50 |
| Wheel top | 52 |
| Beam top | 60 |
| Top clamp plate (+ bolt nut) | 60–63 (66) |
| Walkway grating bottom | 75 |
| Walkway grating top (deck surface) | 100 |

**Clearances:**

| Interface | Gap | Notes |
|-----------|-----|-------|
| Top clamp plate nut → grating bottom | ~9mm | Clears grating; the top clamp plate is now the highest carriage point |
| Beam bottom → tray floor | 18mm | Reduces to ~11mm at midspan under full water load (see §3.7) |
| Nozzle bottom → tray floor | 12mm | Nozzle body clears floor at all carriage positions |
| Wheel top → grating bottom | 23mm | Wheels roll freely under grating |

**Axle retention:** Each wheel axle (10mm SS axle pin) is held by a curved conduit-style
saddle clamp (2mm SS strap) bolted to the underside of the carriage plate. The saddle
cradles the axle pin with 1mm clearance; two bolts pass up through the saddle feet and
carriage plate to lock the axle in position.

### 3.5 Carriage Plate Design

Each carriage uses a flat aluminum plate positioned 2mm above the wheel axle (Z=29–34mm).
The plate wings extend inward to meet the beam faces; the beam is gripped by a top and
bottom clamp plate that sandwich it vertically, with the carriage plate wing captured in
the same bolted stack. The beam stays at its design height (Z=20–60mm).

Formed from 5mm 6061-T6 aluminum plate:

- **Plate wings:** Two flat sections extending from the beam faces out to the
  wheel axle positions. Total plate width spans both wheel positions plus 18mm
  overhang on each side; the outer edge is flush with the beam end.
- **Center notch:** The wings butt against the 40mm beam faces (no gap), so the
  carriage and beam read as one continuous body.
- **Beam clamp:** A bottom clamp plate (under the beam, Z=17–20mm) and a top clamp
  plate (over the beam, Z=60–63mm) are drawn together by bolts on each side of the
  beam. A solid aluminum spacer block beside each beam face fills the gap between the
  plates so tightening grips the beam instead of bending the plates.
- **Ball joint mount:** The ball joint flange bolts to the beam top face (Z=60mm),
  keeping the socket housing below grating level (Z=75mm).

**Lateral guidance:** The tray rim walls (50mm high, at X=170 and X=4,629) act as
lateral guides. The wheel carriages roll between the tray rim and the walkway support
structure. The 200mm wheel spacing in Yd prevents significant skew.

### 3.6 Carriage Fabrication

Each carriage is built from two sub-assemblies: a carriage plate, and wheel-and-axle
units retained by curved saddle clamps. The beam is then sandwiched between a top and
bottom clamp plate bolted through the carriage plate. Two identical carriages are
required (left end and right end of beam).

![Sheet 2 — Cross Section: Beam Assembly](assets/spray-bar-sheet2.png)

#### 3.6.1 Carriage Plate Fabrication (2 required)

Each carriage plate is a flat 5mm 6061-T6 aluminum plate whose wings meet the beam
faces. The plate sits 2mm above the wheel axle (Z=29–34mm); the beam clamp bolts pass
through it, capturing the plate between the top and bottom clamp plates.

**Blank:** Cut two pieces from 5mm plate, each 280mm long × 60mm wide.

| Step | Operation | Detail |
|------|-----------|--------|
| 1 | Mark notch | Scribe the central notch so the wings butt the 40mm beam faces (outer edge flush with beam end) |
| 2 | Cut notch | Jigsaw or bandsaw the center notch from one long edge |
| 3 | Mark axle saddle positions | On each wing, mark two Ø5.5mm clearance holes (M5) per saddle clamp for axle retention |
| 4 | Mark beam clamp bolt positions | Two Ø5.5mm holes on each side of the beam, aligning with the top/bottom clamp plate bolts |
| 5 | Drill all holes | Drill press for accuracy — 8 axle saddle holes + 4 beam clamp holes per plate |
| 6 | Deburr | Remove all burrs from edges, notch, and holes |

#### 3.6.2 Wheel Assembly (2 per carriage, 4 total)

![Sheet 5 — Detail C: Wheel Attachment](assets/spray-bar-sheet5.png)

Each wheel axle is retained by a curved SS saddle clamp (2mm strap) bolted to the
carriage plate underside. The saddle cradles the 10mm axle pin with 1mm clearance.

| Step | Operation |
|------|-----------|
| 1 | Place nylon wheel (50mm × 20mm, 10mm bore) in position under the carriage plate |
| 2 | Insert 10mm SS axle pin through wheel bore |
| 3 | Position the saddle clamp over the axle, feet against the plate underside |
| 4 | Insert 2× M5 bolts up through the saddle feet and carriage plate; secure with nyloc nuts on top |
| 5 | Tighten finger-tight only until all wheels are installed |
| 6 | Spin wheel by hand — confirm free rotation with no lateral wobble |

#### 3.6.3 Carriage Assembly (2 required)

![Sheet 6 — Detail D: Wheel Plan](assets/spray-bar-sheet6.png)

| Step | Operation |
|------|-----------|
| 1 | Place carriage plate flat on bench, notch centered |
| 2 | Install the near wheel-and-saddle unit (wheel hanging below bench edge) — finger-tight |
| 3 | Install the far wheel-and-saddle unit (200mm Yd spacing) |
| 4 | Verify 200mm wheel spacing (center-to-center, Yd direction) |
| 5 | Tighten all nyloc nuts to 4 Nm |
| 6 | Stand the carriage on a flat surface — both wheels must contact simultaneously. Shim if needed before final torque |

#### 3.6.5 Beam Attachment

The carriages attach to the beam with a top + bottom clamp plate that sandwich the SHS
vertically. The bottom plate sits under the beam (Z=17–20mm) and the top plate over it
(Z=60–63mm); a solid aluminum spacer block beside each beam face fills the gap so the
bolts grip the beam rather than bending the plates. Four bolts per carriage pass through
the top plate, spacer, carriage plate wing, and bottom plate, with nuts top and bottom.

| Step | Operation |
|------|-----------|
| 1 | Position the bottom clamp plate under the beam SHS, with its outer edge flush with the beam end |
| 2 | Set the carriage plate over the beam so the wings butt the beam faces |
| 3 | Place a spacer block against each beam face, between the plate wings |
| 4 | Lay the top clamp plate over the beam, aligning the bolt holes with the bottom plate |
| 5 | Pass four bolts down through top plate + spacer + carriage wing + bottom plate; thread nuts top and bottom and tighten evenly until the beam is gripped |
| 6 | Set the assembled spray bar on the processing tray floor. Confirm the top clamp plate (Z=63mm, nut ~66mm) clears the walkway grating bottom (Z=75mm). Confirm all wheels roll freely on the tray floor |
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
| Wheel assemblies (4× wheel + axle + 8 saddle clamps) | 0.50 |
| Nozzles + fittings (26×) | 0.30 |
| Hardware (bolts, clips, clamp plates) | 0.35 |
| **Dry total** | **~6.9 kg** |
| **Wet total (operating)** | **~8.0 kg** |

Per wheel load (wet): 8.0 / 4 = 2.0 kg — well within any small nylon wheel's rating.

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
| Spray nozzles | 26 × flat-fan irrigation nozzles |
| Flow per nozzle | 0.135 GPM (0.51 L/min) |

The center feed position minimizes pipe friction losses by splitting flow equally to
thirteen nozzles on each side. The 19mm bore provides adequate flow capacity at 3.5 GPM.
Each irrigation nozzle delivers a 180° flat fan pattern; at 150mm pitch the fans overlap
heavily, giving near-continuous wash coverage along the 3859mm beam span.

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
coiled flexible hose → barbed center feed → poly pipe bore → 26× spray nozzles.

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
| 2 | Cross Section — Beam Assembly | Yd-Z composite at 1:1 — wheels, carriage plate, beam clamp plates, saddle clamps, ball joint, arm, hose |
| 3 | Plan View | Container floor plan — walkways, slit positions, beam travel range |
| 4 | Detail A — Beam End | Longitudinal section at 2:1 — LDPE fold-back end closure with retainer clip |
| 5 | Detail C — Wheel Attachment | Section along axle at 4:1 — carriage plate, nylon wheel, axle pin, saddle clamp |
| 6 | Detail D — Wheel Plan | Plan view of carriage — beam, carriage plate, beam clamp plate, saddle clamps, wheels |
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
| Flat-fan irrigation spray nozzles, barbed | 180° fan pattern, barbed inlet | 26 | $30–$50 |
| 3/4" barb × 1/2" barb adapter | Center feed through beam top wall | 1 | $4 |
| SS/nylon retainer clips for 3/4" LDPE | Fold-back end closures | 2 | $4 |
| [Nylon skate wheel, 50mm × 20mm, 10mm bore](https://www.mcmaster.com/products/rollers/skate-wheels-1~/) | Flat tread, ≥25 kg rated (2 per carriage) | 4 | $12–$20 |
| 1/2" barb × 1/2" hose barb, brass | Flex hose to center feed adapter | 1 | $4 |
| Telescoping aluminum pool pole, 4–8 ft | Standard pool skimmer handle | 1 | $15 |
| 1/2" reinforced braided PVC hose, 15 ft | BV-02 to beam feed (4 m coiled) | 1 | $15 |
| [10mm × 60mm 304 SS axle pin (4-pack)](https://www.amazon.com/uxcell-Single-Hole-Clevis-Pins/dp/B0816MQ5T6) | Wheel axle pins | 4 (1 pack) | $5 |
| [304 SS saddle clamp, 10mm (10-pack)](https://www.amazon.com/Boxonly-Fixing-Stainless-Saddle-Tension/dp/B0CG1CNQKX) | Axle retention, bolted to plate underside | 8 | $10 |
| M6×20 SS bolts + nyloc nuts | Carriage plate, beam clamp, saddle clamp, splice fasteners | 16 | $7 |
| M8 SS U-bolt + nyloc nuts | Ball joint to beam clamp | 1 | $5 |
| Ø20mm ball joint, zinc socket, M12 stud | Multi-axis arm articulation | 1 | $12 |
| SS beam clamp plates (top + bottom) + spacers (40mm) | Beam to carriage plate (sandwich, bolted) | 4 | $10 |
| 6061-T6 AL round tube 25mm OD × 2mm wall, 500mm | Arm tube | 1 | $6 |
| M6 SS hex bolt + nut | Pinch bolt for arm tube | 1 | $1 |
| Nylon zip ties, 200mm | Hose to arm tube | 6 | $1 |
| **Spray bar subtotal** | | | **$211–$275** |

### 6.3 Combined Total

| Subsystem | Cost Range |
|-----------|-----------|
| Processing tray | $1,300–$2,015 |
| Spray bar assembly | $211–$275 |
| **Total** | **$1,511–$2,290** |

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
