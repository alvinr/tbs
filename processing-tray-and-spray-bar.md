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
directly on the shims.

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
| Spray bar (rides on tray floor beneath walkway grating) | Beam top at Z=50mm, grating bottom at Z=75mm | Clear |
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

The beam spans 3859mm between the inner edges of the left and right walkways
(X=470 to X=4,329), extending under the walkway grating at each end. At each end, a
two-wheel carriage rolls on the processing tray floor beneath the grating. A 1" PVC
Sch 40 pipe inside the aluminum SHS bore serves as the spray pipe — water flows through
the PVC pipe and exits through 2mm holes drilled in the pipe wall, aligned with 12mm
apertures in the beam bottom face.

**Design constraints:**

- Beam top must clear walkway grating underside (Z=75mm) — no contact during travel
- Wheels must fit within the 50mm tray rim height, rolling on the tray floor beneath walkways
- Single-operator use — push/pull from the near walkway via telescoping pole through a 30mm slit
- Must travel 2200mm along Yd (tray depth, near rim to far rim)
- Tray rim walls provide lateral guidance — no separate guide rails required
- Must accommodate a flexible water connection that follows the bar as it moves

### 3.2 Assembly Components

| Component | Specification | Qty | Purpose |
|-----------|--------------|-----|---------|
| Beam | 6061-T6 AL SHS, 40×40×3mm, 3859mm long (two 8 ft lengths joined with splice sleeve) | 1 | Structural beam housing internal spray pipe |
| Internal spray pipe | 1" Sch 40 PVC (OD 33.4mm), 2mm holes at each aperture | 1 | Water distribution inside beam bore |
| PVC socket caps | 1" Sch 40, solvent welded to pipe ends | 2 | Seal both ends of PVC pipe |
| Bulkhead fitting | 1/2" NPT, brass, through beam wall at center | 1 | Center feed — connects hose to PVC pipe bore |
| Nylon wheels | 50mm OD × 20mm wide, 10mm bore, flat tread | 4 | Roll on tray floor beneath walkway grating |
| Wheel fork brackets | 6061-T6 AL plate 6mm, U-fork profile | 4 | Mount wheels on axle pins |
| Axle pins | 10mm SS clevis pin + snap rings | 4 | Wheel spindles (snap ring retention both ends) |
| L-brackets | 6061-T6 AL plate 5mm, horizontal arm | 2 | Connect carriages to beam via U-clamp |
| U-clamps | SS, flared legs, wing nuts — wraps 40mm SHS | 2 | Attach beam to L-bracket, tool-free adjustment |
| Ball joint | Ø20mm SS ball, zinc socket, M12 stud, 50mm flange | 1 | Multi-axis arm articulation on beam top face |
| M8 U-bolt | SS, wraps over ball joint socket, nyloc nuts | 1 | Clamps ball joint to beam |
| Arm tube | 6061-T6 AL round tube, 25mm OD × 2mm wall, ~500mm | 1 | Vertical arm from ball joint to pole |
| M6 pinch bolt | SS hex bolt + nut | 1 | Clamps arm tube onto ball joint stud |
| Push pole | Telescoping aluminum pool pole, 1.2–2.4 m | 1 | Operator controls bar position from walkway |
| Flexible hose | 1/2" reinforced braided PVC, ~4 m coiled | 1 | Connects BV-02 to center feed bulkhead |
| Hose barb fitting | 1/2" MNPT × 1/2" barb, brass | 1 | Connects hose to bulkhead fitting exterior |
| Zip ties | Nylon, 200mm | ~6 | Secure flex hose to arm tube |

### 3.3 Beam / Spray Pipe

The structural beam doubles as the water distribution pipe. A single 6061-T6 aluminum
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
Metals, and metals suppliers. Two 8 ft lengths are required; see §3.7 for splice joint.

**Spray holes:**

| Property | Value |
|----------|-------|
| Hole diameter | 3mm |
| Hole spacing | 100mm center-to-center |
| Number of holes | 38 |
| End margin | 79.5mm each end |
| Total hole area | 268.6mm² |
| Bore cross-section area | 1156mm² |
| Hole-to-bore area ratio | 23.2% |

The 23% hole-to-bore ratio ensures reasonably uniform pressure along the beam length.
At 3.5 GPM total flow, bore inlet velocity is only 0.19 m/s (Re ≈ 6,500) — friction
losses along the bore are small compared to the orifice pressure drop through each 3mm
hole. End-to-end flow variation is estimated at <15%.

**End caps:**

Each beam end is sealed with a 3mm 6061-T6 aluminum plate, cut to a 40×40mm square
with radiused corners. TIG welded to the beam end face with a continuous perimeter bead.

- **Feed end (left, X=470):** Center-drilled and tapped for a 1/2" NPT bulkhead fitting.
- **Dead end (right, X=4,329):** Solid plate, fully welded and watertight.

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
| Beam bottom (with 17mm bracket drop) | 10 |
| Wheel axle centerline | 27 |
| Beam top | 50 |
| Tray rim top | 50 |
| Wheel top | 52 |
| Walkway grating bottom | 75 |
| Walkway grating top (deck surface) | 100 |

**Clearances:**

| Interface | Gap | Notes |
|-----------|-----|-------|
| Beam top → grating bottom | 25mm | Ample clearance; no contact during travel |
| Beam bottom → tray floor | 8mm | Reduces to ~0.5mm at midspan under full water load (see §3.6) |
| Wheel top → grating bottom | 23mm | Wheels roll freely under grating |

**Wheel fork brackets:** Each wheel is held by a U-shaped fork bracket fabricated from
6mm 6061-T6 aluminum plate. The fork straddles the wheel with ~2mm side clearance,
drilled for a 10mm clevis pin axle. The fork's base plate has two M6 through-holes for
bolting to the L-bracket horizontal arm.

### 3.5 L-Bracket Design

Each carriage uses an L-bracket to lower the beam 17mm below the wheel axle
centerline, creating 25mm clearance between beam top (Z=50mm) and walkway grating
bottom (Z=75mm).

Formed from 5mm 6061-T6 aluminum plate, bent to an L-profile:

- **Horizontal arm:** Extends from the walkway inner edge outward under the grating at
  wheel axle height (Z=27mm). Length ≈200mm. Two wheel fork brackets bolt to the top
  face, spaced 200mm apart in Yd.
- **Vertical leg:** At the inboard end, bends downward 17mm to Z=10mm. The beam's
  side face bolts to the vertical leg with 2× M6×20 stainless bolts.

**Lateral guidance:** The tray rim walls (50mm high, at X=170 and X=4,629) act as
lateral guides. The wheel carriages roll between the tray rim and the walkway support
structure. The 200mm wheel spacing in Yd prevents significant skew.

### 3.6 Structural Analysis

**Loading (simply supported, uniform distributed load across 3859mm span):**

| Component | Linear mass (kg/m) | Linear weight (N/m) |
|-----------|-------------------|---------------------|
| Beam (6061-T6 AL, 40×40×3mm SHS) | 1.199 | 11.76 |
| Water in bore (34×34mm filled) | 1.156 | 11.34 |
| **Total UDL** | **2.355** | **23.10** |

Water volume in bore: 34 × 34 × 3,859 = 4.46 liters (4.46 kg).

**Deflection — δ = 5wL⁴ / 384EI, E = 68,900 MPa:**

| Condition | w (N/m) | δ center (mm) | Span ratio |
|-----------|---------|---------------|------------|
| Dry (beam self-weight only) | 11.76 | 4.8 | L/799 |
| Wet (beam + water in bore) | 23.10 | 9.5 | L/406 |

The L/406 span ratio under full water load is marginal by structural standards but
acceptable for a spray bar application — no foot traffic, precision loads, or dynamic
impact. The deflection is entirely elastic and fully recoverable.

**Pre-camber recommendation:** Apply 5mm upward pre-camber during fabrication to offset
roughly half the wet deflection, maintaining ≥5mm floor clearance at midspan. Method:
support beam at both ends on blocks during end cap welding; apply 5mm upward shim at
center; tack caps in bowed position. Residual stress in the end cap welds holds the
camber permanently.

**Weight summary:**

| Component | Mass (kg) |
|-----------|-----------|
| Beam (40×40×3mm × 3859mm) | 4.63 |
| Water in bore | 4.46 |
| L-brackets (2×) | 0.40 |
| Wheel assemblies (4× wheel + fork + axle) | 0.60 |
| End caps + bulkhead fitting | 0.10 |
| Hardware (bolts, clips) | 0.30 |
| **Dry total** | **~6.0 kg** |
| **Wet total (operating)** | **~10.5 kg** |

Per wheel load (wet): 10.5 / 4 = 2.6 kg — well within any small nylon wheel's rating.

### 3.7 Beam Splice Joint

Two 8 ft (2438mm) SHS lengths are joined with an internal sleeve splice at midspan:

- **Sleeve:** 150mm of 30×30mm solid aluminum bar stock, inserted into the 34×34mm bore (2mm clearance per side)
- **Sealant:** Marine-grade RTV silicone on sleeve exterior — watertight, allows future disassembly with heat
- **Fastening:** 2× M5 set screws through SHS wall on each side (4 total), engaging dimples in sleeve
- **Location:** Midspan (1930mm from each end). The solid bar has higher I than the hollow beam wall, so the splice is not the weak point.

**Alternative:** Source a single 16 ft or 20 ft length by special order to eliminate
the splice entirely.

### 3.8 Flow Analysis

| Parameter | Value |
|-----------|-------|
| Supply pump | P-01 (Shurflo 2088), 3.5 GPM at 45 PSI |
| Bore cross-section | 34 × 34mm = 1156mm² |
| Bore inlet velocity | 0.19 m/s (at 3.5 GPM) |
| Reynolds number (bore) | ~6,500 (transitional/low turbulent) |
| Spray holes | 38 × Ø3mm |
| Total hole area | 268.6mm² |
| Flow per hole | 0.092 GPM (0.35 L/min) |

The bore is deliberately oversized relative to total spray hole area (bore 4.3× larger).
This ensures the bore acts as a low-loss plenum: pressure is nearly uniform along the
bore length, and each hole delivers approximately equal flow regardless of distance from
the feed end.

### 3.9 Water Connection

BV-02 (1/2" ball valve, Blue supply isolation) is mounted on the pinhole wall (Yd=0) at
X=2399mm (pinhole centerline), Z=900mm — waist height from the walkway deck. A
1/2" HDPE riser runs from the Blue supply trunk up to BV-02. A 4 m length of 1/2"
reinforced braided PVC hose connects from BV-02 down to the beam's center feed bulkhead
fitting. The hose coils when the bar is near the pinhole wall and extends as the bar is
pushed toward the far wall. The hose trails along the near tray rim, staying clear of
the print surface.

**Supply path:** P-01 → ACC-01 → rigid 1/2" HDPE pipe along pinhole wall → BV-02 →
coiled flexible hose → bulkhead fitting → beam bore → spray holes.

### 3.10 Walkway Slit

The operator controls the spray bar position from the near walkway using a telescoping
aluminum pool pole (1.2–2.4 m). The pole passes through a 30mm wide slit cut into the
walkway grating at the beam centerline X=2500mm. A matching slit is cut into the far
walkway grating at the same X position. The slit positions are shown on the
[walkway plan view](engineering-diagrams.md#14-perimeter-walkway).

### 3.11 Ball Joint and Arm

A Ø20mm stainless steel ball joint on the beam top face provides multi-axis
articulation between the beam and the operator's pole. The ball sits in a zinc socket
housing (M12 stud, 50mm flange), clamped to the beam with an M8 stainless U-bolt and
nyloc nuts.

A 25mm OD × 2mm wall aluminum round tube (~500mm long) connects from the ball joint
stud to the telescoping pole. An M6 pinch bolt clamps the arm tube onto the stud. The
1/2" flexible hose is zip-tied to the arm tube at ~200mm intervals.

---

## 4. Operation

### 4.1 Setup

1. Lay a fresh 6-mil black LDPE liner over the tray surface; overlap 50mm over rims
2. Position the spray bar at the far end of the tray (Yd≈2,280, film-plane side)
3. Attach the telescoping pole to the arm tube

### 4.2 Wash Pass

1. Open BV-02 — water flows through the coiled hose into the beam bore and out the spray holes
2. Using the pole, slowly pull the bar toward the pinhole wall (decreasing Yd), flooding the print progressively
3. Travel speed approximately 50 mm/second — full traverse takes ~44 seconds
4. At the near rim (Yd≈80), close BV-02. One wash pass complete.
5. For additional passes, push the bar back to the far end and repeat

### 4.3 Brown (Recycled) Water Passes

Same spray bar — the operator switches by closing BV-02 and activating P-02 through the
filter train. Recycled water from IBC-3 is pumped through the three-stage filter skid and
back into the beam bore via the same supply path.

### 4.4 Storage

The spray bar rests at either end of its travel with wheels on the tray floor. The
flexible hose coils naturally at the pinhole wall. The telescoping pole detaches and
stores alongside the bar or clips to the container wall.

---

## 5. Engineering Drawings

Six detail sheets cover the spray bar assembly and processing tray:

| Sheet | Title | Content |
|-------|-------|---------|
| 1 | Gantry Elevation | X-Z section from film plane (4× vert exag) — beam, BV-02, pole, walkway slit, operator silhouette |
| 2 | Cross Section — Beam Assembly | Yd-Z composite at 1:1 — wheels, L-bracket, U-clamp, ball joint, arm, hose |
| 3 | Plan View | Container floor plan — walkways, slit positions, beam travel range |
| 4 | Detail A — Beam End | Longitudinal section at 2:1 — PVC pipe extension, socket cap, solvent weld |
| 5 | Detail C — Wheel Attachment | Section along axle at 2:1 — fork arms, nylon wheel, axle pin, snap rings |
| 6 | Detail D — Wheel Plan | Plan view of carriage — beam, L-bracket arm, U-clamp, wheels |

![Sheet 1 — Gantry Elevation](assets/spray-bar-sheet1.png)

![Sheet 2 — Cross Section: Beam Assembly](assets/spray-bar-sheet2.png)

![Sheet 3 — Plan View: Walkways & Slit Positions](assets/spray-bar-sheet3.png)

![Sheet 4 — Detail A: Beam End](assets/spray-bar-sheet4.png)

![Sheet 5 — Detail C: Wheel Attachment](assets/spray-bar-sheet5.png)

![Sheet 6 — Detail D: Wheel Plan](assets/spray-bar-sheet6.png)

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
| 6061-T6 AL plate 3/16" (5mm) | L-brackets + end caps (~300 × 600mm sheet) | 1 | $15–$25 |
| 30×30mm AL solid bar, 150mm | Internal splice sleeve | 1 | $8–$12 |
| 1" Sch 40 PVC pipe, 10 ft | Internal spray pipe (cut to beam length) | 1 | $8 |
| 1" PVC socket caps | Solvent welded to pipe ends | 2 | $3 |
| PVC solvent cement + primer | Pipe end assembly | 1 set | $8 |
| Nylon fixed wheel, 50mm × 20mm, 10mm bore | Flat tread, ≥25 kg rated | 4 | $12–$20 |
| 1/2" NPT bulkhead fitting, brass | Center feed cap | 1 | $8 |
| 1/2" MNPT × 1/2" hose barb, brass | Hose to bulkhead adapter | 1 | $4 |
| Telescoping aluminum pool pole, 4–8 ft | Standard pool skimmer handle | 1 | $15 |
| 1/2" reinforced braided PVC hose, 15 ft | BV-02 to beam feed (4 m coiled) | 1 | $15 |
| 10mm clevis pins + snap rings | Wheel axle pins | 4+4 | $8 |
| M6×20 SS bolts + nyloc nuts | L-bracket, fork, splice fasteners | 16 | $7 |
| M8 SS U-bolt + nyloc nuts | Ball joint to beam clamp | 1 | $5 |
| Ø20mm ball joint, zinc socket, M12 stud | Multi-axis arm articulation | 1 | $12 |
| SS U-clamp, flared legs, wing nuts (40mm) | Beam to L-bracket (tool-free) | 2 | $10 |
| 6061-T6 AL round tube 25mm OD × 2mm wall, 500mm | Arm tube | 1 | $6 |
| M6 SS hex bolt + nut | Pinch bolt for arm tube | 1 | $1 |
| Nylon zip ties, 200mm | Hose to arm tube | 6 | $1 |
| **Spray bar subtotal** | | | **$182–$224** |

### 6.3 Combined Total

| Subsystem | Cost Range |
|-----------|-----------|
| Processing tray | $1,300–$2,015 |
| Spray bar assembly | $182–$224 |
| **Total** | **$1,482–$2,239** |

---

## 7. Maintenance

| Task | Interval | Procedure |
|------|----------|-----------|
| Tray wipe-down | After each session | Remove LDPE liner, wipe tray with damp cloth, inspect sump for debris |
| Sump pickup clean | Monthly | Lift pickup tube, rinse strainer screen, check foot valve seal |
| Spray holes | Monthly | Flush beam bore with clean water; use 3mm drill bit to clear any blocked holes |
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
