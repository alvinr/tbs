<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Hinged Light-Trap Panel

## 1. Purpose

TBS-001 requires a light-tight seal at the cargo door end of the container that
simultaneously allows personnel access during operation without admitting daylight.
The hinged light-trap panel fills both roles: it seals the full 2362 × 2388mm
cargo door opening as a rigid structural panel, and incorporates a revolving drum
light trap that permits operators to enter and exit the darkened interior at any
time without opening the panel or breaking the light seal. In case of emergency, or to easy loading and unloading of materials, the whole hinged panel can open fully, being locked from the inside.

**Sheet 1 — Front Elevation (1:20): Panel Dimensions, Drum, Hinges, Latches (interior face)**
![TBS-001 Hinged Panel — Sheet 1: Front Elevation](assets/hingepanel-sheet1.png)

**Design goals:**

- 100% light exclusion — no straight-line optical path from exterior to interior
- Single-operator personnel access at any time during exposure
- 180° outward swing for full-width loading access (IBC totes, equipment)
- ~880mm inward slide for transport mode — retracts the B2 punch-out bay behind the ISO container doors + hardware
- Emergency egress operable from inside without tools
- Weatherproof for outdoor field deployment (IP44 rated seals)
- Single-person mode conversion (~5 minutes)

**Interactive 3D model** — the revolving light-trap drum, hinged stepped panel, sliding carriage, fixed door frame (with the bottom seal lip), and Fan B. Drag to orbit, scroll to zoom.

<div class="sketchfab-embed-wrapper">
  <div style="position:relative;width:100%;padding-bottom:56.25%;">
    <iframe title="TBS-001 Lighttrap Model" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/6a794d0d2ff44a4e975e021012c69666/embed" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>
  </div>
  <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"><a href="https://sketchfab.com/3d-models/tbs-001-lighttrap-model-6a794d0d2ff44a4e975e021012c69666?utm_medium=embed&utm_campaign=share-popup&utm_content=6a794d0d2ff44a4e975e021012c69666" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">TBS-001 Lighttrap Model</a> by <a href="https://sketchfab.com/alvin91403?utm_medium=embed&utm_campaign=share-popup&utm_content=6a794d0d2ff44a4e975e021012c69666" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">alvin91403</a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=6a794d0d2ff44a4e975e021012c69666" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>
</div>

---

## 2. Panel Construction

### 2.1 Stepped Profile

The panel has three thickness zones to accommodate the revolving drum in the center
while keeping the corners flush with the container walls.

**Sheet 2 — Plan Cross-Section (1:10 horiz / 1:1 depth): Housed Revolving Door — Housing, Drum & Light-Tight Geometry**
![TBS-001 Hinged Panel — Sheet 2: Plan Cross-Section](assets/hingepanel-sheet2.png)

| Zone | Yd range (mm) | Width (mm) | Thickness (mm) | Construction |
|------|--------------|-----------|---------------|-------------|
| Near corner | 0–653 | 653 | 40 | 18mm ply + 3mm aluminum plate + 18mm ply |
| Center | 653–1,709 | 1,056 | 120 | 18mm ply + 84mm RHS frame + 18mm ply |
| Far corner | 1,709–2,362 | 653 | 40 | 18mm ply + 3mm aluminum plate + 18mm ply |

The 80mm step between corner and center zones occurs at Yd=653mm and
Yd=1709mm (widened in rev 8 to frame the Ø900 housing). The center zone houses the
light-trap housing; the corner zones are
flush-faced panels that seal against the fixed door frame.

### 2.2 Frame

| Parameter | Value |
|-----------|-------|
| Frame material | 50 × 50 × 3mm RHS mild steel |
| Outer dimensions | 2362 × 2388mm |
| Skin (each face) | 18mm exterior-grade plywood |
| Interior finish | Flat black (RAL 9005) — optically dead at visible wavelengths |
| Frame perimeter | Welded corners, mitered joints |
| Panel weight (sandwich + Ø900 housing, excl. drum) | ~223 kg (first-principles: 187 kg sandwich + 36 kg housing) |

### 2.3 EPDM Perimeter Seal

A 20mm closed-cell EPDM compression gasket runs the full perimeter of the panel,
seated in an extruded aluminum channel. The gasket compresses against a fixed welded
door frame (50 × 50 × 3mm RHS) at X=0 when the four cam latches engage. The seal
provides light-tight compression on all four sides.

A **second** 20mm EPDM gasket — the **housing-surround seal** — runs as a ring around
the Ø900 light-trap housing aperture. Because the housing is **fixed** (only the drum
rotates inside it), this gasket seals the fixed surround to the frame independently of
the moving panel, all the way around the opening the housing passes through. It sits in
the same exterior door plane (X=0), concentric inboard of the panel-perimeter seal (see
§6, light-path #8).

---

## 3. Housed Revolving-Door Light Lock

> **rev 8.** Replaces the earlier Ø750mm / 4-fin revolving drum, which failed both
> personnel-fit and rotation light-tightness (see §3.6). The light lock is now a
> **fixed cylindrical housing + single-opening C-shell drum** — the standard
> commercial-darkroom-door arrangement — sized for a single operator.

**Sheet 3 — Drum Vertical Section Elevation (Section A-A): Walking-height orientation confirmation + Details B & C (panel bottom & top light seals)**
![TBS-001 Hinged Panel — Sheet 3: Drum Elevation](assets/hingepanel-sheet3.png)


### 3.1 Specification

| Parameter | Value |
|-----------|-------|
| Type | Fixed cylindrical housing + single-opening C-shell revolving drum (no internal fins) |
| Housing outer diameter | Ø900mm (fixed, built into the panel center zone) |
| Housing openings | Two, **80° arc each, 180° apart** — one facing exterior, one facing the interior/walkway |
| Drum (rotating) | Ø864mm C-shell, single 80° opening, **~Ø850mm clear bore** |
| Passage width | **~555mm** (the 80° opening) — single operator, sideways entry |
| Height | Top at Z=2200mm (upper bearing on panel top rail) |
| Mounting | **Suspended with the panel** — bottom hangs at Z=80 on the panel bottom rail (80mm floor gap → clears the 50mm tray rim during the transport slide). Operator steps up ~80mm over the threshold to enter; exits level onto the walkway deck (also Z=80). |
| Wall thickness | 5mm UV-HDPE housing (LT_HOUSING_T) + 4mm PP drum (LT_DRUM_T) — rolled and extrusion-welded plastic skin (rev 9 / B2; was 3mm aluminum); opening edge-stiffened |
| Interior finish | Black-pigmented sheet + flat-black touch-in at welds (no etch-prime) |
| Exterior finish | UV-stabilized black/gray sheet — inherent, no primer |
| Clear walking height | 1910mm (between bearings) |
| Internal baffles | **None** — light-tightness is by the fixed-housing geometry (§3.3) |
| Weight | housing ~22 kg + rotating drum ~38 kg = **~60 kg** (plastic skin, ≈60% of the 3mm-aluminum ~99 kg; the steel shaft/bearings set a floor the shell mass can't drop below) |

### 3.2 Bearings

| Item | Specification |
|------|--------------|
| Bearing model (×2) | SKF 6215-2RS1 sealed deep-groove ball bearing |
| Bore | 75mm ID, 130mm OD, 25mm wide |
| Clearance | C3 |
| Radial load rating | 52.7 kN (static) |
| Operating temperature | 0–120°C |
| Stub shafts | 75mm Ø × 150mm steel, bolted through an isolated steel hub to the aluminum drum caps (dissimilar-metal joint) |
| Axial retention | Circlip on stub shaft each side |
| Upper mount | Aluminum housing top ring bolted to panel top rail (6 × M10 SS, nylon-isolated) |
| Lower mount | Welded steel floor collar bolted to panel bottom rail (8 × M10 SS) |
| Bearing housing height | 45mm (each) |

### 3.3 Light Path Verification

The light lock is light-tight **by geometry**. The fixed housing has two openings
(one facing the exterior, one facing the interior/walkway), each **80° of arc and
180° apart**; the rotating drum is a C-shell with a **single 80° opening and no
internal fins**. Because each opening is narrower than 90° and the two housing
openings are 180° apart, the drum opening can never align with both at once — the
housing's solid wall always covers whichever opening the drum opening is *not*
facing. So at **no rotation angle** is there a straight-line path from exterior to
interior: daylight entering the bore through the exterior opening is stopped by the
drum's solid wall before it can reach the interior opening.

This resolves both failure modes of the earlier Ø750 / 4-fin drum (§3.6): a single
operator fits the open ~Ø850mm bore, and there is no transit angle that admits
daylight. See [Light Trap Selection](light-trap-selection.md) §5 and **Sheet 5**
(enter / transit / exit verification).

### 3.4 Drum Seals

| Location | Seal method |
|----------|------------|
| Top | 12mm closed-cell neoprene wiper ring bonded to drum top cap + silicone bead against ceiling mount plate |
| Bottom | 12mm closed-cell neoprene wiper ring bonded to drum bottom cap + silicone bead against floor mount plate |
| **Drum↔housing rotating seal** | Felt/brush wiper strips on the two vertical edges of the drum opening sweep against the housing inner wall as the drum turns, blocking light leaking around the opening; top + bottom felt wiper rings close the ~15mm annular running gap |
| Housing-to-panel gap | 15mm radial clearance, closed by 20mm neoprene compression strip bonded to the panel aperture |
| Weather rating | IP44 (splash and rain protection) |

### 3.5 Handle

A 100mm Ø × 400mm stainless steel grab rail is mounted on the interior face
only at 900mm height. The handle is attached by a welded bracket — no through-bolt
penetration of the drum wall on the exterior face. This eliminates a potential
light leak path. The operator enters by pushing the bare exterior drum wall, then
uses the interior grab rail to pull the drum closed and brace during exit.

### 3.6 Access & Light-Tightness Verification (both tests pass)

Two questions decide whether a revolving light lock actually works. The rev-8
housed revolving door **passes both** — the same two questions on which the earlier
Ø750mm / 4-fin drum failed (that failure is what drove this redesign).

**Sheet 5 — Light-lock access & light-tightness verification**
![TBS-001 Hinged Panel — Sheet 5: Light-Lock Verification](assets/hingepanel-sheet5.png)

**1. Does a person fit? — Yes.** The four radial fins are gone; the drum is a
single-opening C-shell, so the whole **~Ø850mm bore** is clear standing space. The
80° opening gives a **~555mm passage** (sideways entry), enough for a single operator to enter and
turn inside. Emergency egress remains the whole panel swinging open.

**2. As the drum rotates, can daylight enter? — No.** The fixed housing's two 80°
openings are 180° apart, so the 80° drum opening can never reach both at once: at
**enter** the exterior opening feeds the bore but the interior opening is covered by
the drum's solid wall; at **transit** both housing openings are covered; at **exit**
the exterior opening is covered. There is no straight-line path at any angle.

**Why the earlier 4-fin drum failed (for the record).** Four fins from the bore
center to the wall split the Ø744mm bore into 90° wedges (~250–300mm of body space —
a person could not fit), and a revolving drum with a person-sized opening and *no
fixed housing* necessarily bridged exterior and interior at the transit angles. The
fix — a **fixed housing** with two offset openings narrower than 90° — is the
standard commercial-darkroom-door arrangement, here custom-built to the panel.

---

## 4. Hinges and Latches

### 4.1 Hinges

| Parameter | Value |
|-----------|-------|
| Type | Heavy-duty weld-on barrel hinges — **STRUCTURAL SIGN-OFF REQUIRED** |
| Quantity | 3 |
| Positions (from floor) | 220mm, 1190mm, 2158mm |
| Mounting | Left edge of panel (exterior view), welded to a steel hinge post |
| Swing | 180° outward — clears full door opening and all interior equipment |

Under rev 9 (B2) the panel no longer carries just plywood skins: the punch-out bay,
the fixed Ø900 housing, and the revolving drum all hang off the swinging leaf,
roughly tripling the cantilevered swing-out moment about the hinge line. A 200mm
ball-bearing piano hinge is no longer adequate; the leaf is hung on three heavy-duty
weld-on barrel hinges on a welded steel post. The plastic-skinned drum/housing
(LT_DRUM_T = 4mm PP, LT_HOUSING_T = 5mm UV-HDPE) keeps that added mass modest — the
core is light — but the moment arm is long, so the **hinge post, barrel hinges, and
their weld pattern require a structural engineer's sign-off** before fabrication. A
**retractable swing-support caster** at the free (latch) edge carries the leaf weight
through its 180° arc so the load is not borne by the hinges alone while open.

### 4.2 Cam Latches

| Parameter | Value |
|-----------|-------|
| Model | Southco C2-33 cam compression latch |
| Quantity | 4 (one at each corner) |
| Positions | 210mm and 2152mm from side edges, 220mm and 2168mm from floor |
| Mounting face | **Interior** — deliberate safety design for emergency egress |
| Seal compression | Compresses EPDM perimeter gasket against fixed door frame |

**Emergency egress:** If the revolving drum jams and prevents normal egress, an
operator inside the container can release all four interior-mounted cam latches
independently and push the panel open outward. The panel swings 180° clear of all
interior equipment.

---

## 5. Sliding Carriage System

The entire panel (including the bay, housing + drum) slides ~880mm in the X direction on linear
rails for transport mode conversion. This slide retracts the B2 punch-out bay's exterior
overhang behind the container door closure plane.

**Sheet 1 — Side elevation cross-section: Panel suspended from ceiling rail, operational and transport positions, processing tray clearance**
![TBS-001 Ceiling Rail — Sheet 1: Side Elevation](assets/ceiling-rail-sheet1.png)

See [Ceiling Rail Design](ceiling-rail-report.md) for full details.

### 5.1 Panel Positions

**Sheet 4 — Rotating transport + swing clearance: panel swings 56° about the pivot (camera vs swung), removable left rails**
![TBS-001 Hinged Panel — Sheet 4: Rotating Transport + Swing Clearance](assets/hingepanel-sheet4.png)

| Position | Panel corner inner face X | Drum exterior edge X | Container doors clear? |
|----------|--------------------------|---------------------|----------------------|
| Operational | 40mm | −850mm (bay front −890mm) | No — the B2 punch-out bay protrudes ~890mm; the cargo doors stay open during operation |
| Transport (slid +880mm) | — | +30mm | Yes — the bay retracts behind the door plane by ~30mm |

### 5.2 Locking

| Lock position | Method |
|--------------|--------|
| Operational (X=0) | 2 × Destaco 207-U toggle clamps |
| Transport (X≈870) | 2 × Destaco 207-U toggle clamps |

### 5.3 Floor Gap

The panel is suspended from the ceiling HGR20 rails with an 80mm gap between the
panel bottom edge and the container floor. This gap clears the 50mm processing tray
rim with 30mm margin, allowing the panel to slide freely in both directions without
contacting the tray.

**The housing + drum hang at the same Z=80** (lower bearing on the panel bottom
rail), so they too clear the tray rim by 30mm. This matters in transport: the ~880mm
inward slide carries the Ø900 housing into the near-tray zone (its interior edge
reaches ~X=930), but because the whole assembly is suspended it passes over the tray
basin rather than colliding with it. A floor-mounted housing would have fouled the
tray; suspension is what makes the deeper-housing transport slide feasible. The 80mm
floor gap is closed by the now-continuous bottom seal lip (§6 path #6).

The 80mm gap would otherwise be a straight light path, so it is light-sealed in the
operational position by the fixed-frame bottom seal lip described in §6 (path #6) —
a threshold upstand the panel bottom edge recedes into, with an EPDM strip compressed
by the lower cam latches. Because the seal is a non-floor compression seal against a
frame lip (not a contact seal to the floor), it never fouls the tray rim and lifts
clear the moment the clamps are released for transport.

### 5.4 Transport Conversion Sequence

The rotation transport + swing clearance vs the film-plane left mechanism is shown in
**Sheet 4** (above): the panel + drum swing ~56° about the pivot, pulling the bay inboard of
the door plane (true min X +59 mm); the two left film rails are struck (removable) so the
swinging cage transitions the X=150 rail plane, then re-seat to the film datum.

The inward slide carries the panel to **X 880–1000**, so it sweeps through **X=150**,
where the film-plane mechanism's left edge sits. The film-plane left rail (running in
Yd at X=150, floor + ceiling) — **now continuous in operation**, since the B2 punch-out
bay offsets the drum clear of it — plus the lengthwise brace-cage beams (X 150→4649)
and the muslin screen are all in the slide path; the deeper slide also reaches the
**door-end walkway brackets (X≈698, 1155)**. **The film plane and those door-end
brackets must therefore be struck before the panel is slid.** Striking the film plane
is required regardless: the fragile muslin screen cannot travel mounted.

Order of operations (single person, ~10 min):

1. Remove the muslin screen from its frame and stow it (rolled).
2. Knock down the brace cage (saddle/thumbscrew portals — it is a demountable box).
3. **Remove the full film-plane left rail** (floor + ceiling — continuous in operation,
   lifted out whole for transport). Park the film-plane carriage clear.
4. **Strike the door-end near/far walkway brackets** (X≈698, 1155) — the deeper slide
   sweeps past them.
5. Lift out the left walkway.
6. Release the four cam latches and the two operational toggle clamps.
7. Slide the panel inward ~880mm; engage the transport toggle clamps.
8. Close the ISO cargo doors.

Re-deployment reverses the sequence. (rev 9 / B2 offsets the drum out via the punch-out
bay so the left rail is continuous in operation, and deepens the slide to ~880mm.)

---

## 6. Light Seal Design

The sliding mechanism introduces seven potential light ingress paths that must be
sealed when the panel is in the operational position.

| # | Light path | Seal method |
|---|-----------|-------------|
| 1 | Panel perimeter → door frame | 20mm EPDM gasket in aluminum channel, compressed by 4 × Southco C2-33 cam latches against fixed door frame at X=0 |
| 2 | Left carriage beam slot | Doubled nylon brush strip (~70 × 2400mm slot), bristles inward from both sides, bonded to frame slot edges |
| 3 | Right guide slot | Matching doubled nylon brush strip (~70 × 2400mm slot), same treatment as left slot |
| 4 | Rail channels at floor/ceiling (×4) | 10mm closed-cell neoprene compression pad (50 × 30mm) bonded to frame face around each rail penetration |
| 5 | Panel edge-to-wall clearance gaps | 15mm closed-cell EPDM strips (self-adhesive, full panel height) bonded to fixed door frame inner face at each side |
| 6 | Panel bottom → 80mm floor gap | Fixed-frame **bottom seal lip** — a continuous steel upstand welded to the threshold, rising ~110mm (above the panel bottom edge at Z=80) across the **full panel-bottom width, continuous (no notch)** — the housing/drum is **suspended at Z=80** and no longer reaches the floor, so the floor gap is uniform and the lip closes it as a solid wall; a 20mm EPDM strip on the panel bottom edge **recedes into / sandwiches against the lip** and is compressed by the lower pair of Southco cam latches in the operational ("camera") position. The clamps are released to lift the seal and slide the panel to transport. (Sheet 3, Detail B.) |
| 7 | Panel top → frame gap (panel hangs below the ceiling rails) | Fixed-frame **top seal lip** — the mirror of #6: a steel downstand from the frame top rail reaching ~30mm below the panel top edge. The drum does not reach the top (its stub shaft stops below the lip), so unlike the bottom lip this one runs as **one continuous member across the full panel-top width — no notch — meeting across the center**. A 20mm EPDM strip on the panel top edge sandwiches against it, compressed by the upper pair of cam latches in the operational position; released to slide to transport. (Sheet 3, Detail C.) |
| 8 | Fixed housing surround → door frame | The Ø900 light-trap housing is **fixed** (only the drum rotates inside it). A **second 20mm EPDM gasket** runs as a **ring around the housing aperture** (Yd 713–1649, floor-gap up to the housing top at Z=2200), concentric **inboard** of the panel-perimeter seal (#1), in the exterior door plane (X=0). It seals the fixed surround to the frame all the way around the opening the housing passes through — light-tight independent of the moving panel. (3D: the `door_frame()` "Housing surround seal", in both the light-trap and overview models.) |

**Seal verification:** After mode conversion, the operator performs a 5-minute
dark-adaptation check inside the container with all seals engaged. Any visible light
points are marked with gaffer tape for re-sealing.

---

## 7. Fixed Door Frame

A fixed welded door frame provides the seal landing surface and structural anchor
for the sliding carriage.

| Parameter | Value |
|-----------|-------|
| Material | 50 × 50 × 3mm RHS mild steel |
| Position | X=0 (container end wall inner face) |
| Function | EPDM seal landing, carriage beam slot housing, rail mounting |
| Attachment | Welded to container end wall structural members |
| Slots | 2 × vertical (~70 × 2400mm) for carriage beam and right-side guide |
| Rail penetrations | 4 × (floor and ceiling, both walls) sealed by neoprene pads |
| Bottom seal lip | Continuous 3mm steel upstand welded to the threshold, ~110mm tall, **full panel-bottom width (no notch — drum suspended at Z=80)** — the EPDM bottom seal compresses against it (see §6 path #6) |
| Top seal lip | Mirror of the bottom: continuous 3mm steel downstand from the frame top rail, reaching ~30mm below the panel top edge, full panel-top width and **continuous across the center** (the drum does not reach the top, so no notch) — the EPDM top seal compresses against it (see §6 path #7) |

---

## 8. Parts List

### 8.1 Panel Structure

| Item | Specification | Qty | Est. cost (USD) |
|------|--------------|-----|----------------|
| 50 × 50 × 3mm RHS mild steel (6 m lengths) | Frame perimeter + internal members | 4 | $120–$160 |
| 18mm exterior-grade plywood (1220 × 2440mm sheets) | Panel skins (both faces) | 6 | $180–$300 |
| 3mm aluminum plate (1220 × 2440mm) | Corner zone core plates | 2 | $360–$460 |
| 20mm EPDM gasket (per meter, closed-cell) | Perimeter seal (~10 m) + housing-surround ring (~6 m) | 16 m | $64–$96 |
| Aluminum U-channel (per meter) | Gasket retainer — perimeter + housing-surround ring | 16 m | $48–$80 |
| Heavy-duty weld-on barrel hinge + steel hinge post | Left-edge hinges — carry bay + housing + drum swing moment (**structural sign-off**) | 3 | $180–$300 |
| Retractable heavy-duty swivel caster | Free-edge swing support through the 180° arc | 1 | $40–$80 |
| Southco C2-33 cam compression latch | Interior-mounted corner latches | 4 | $60–$100 |
| 6mm exterior plywood + EPDM lip | B2 punch-out bay — 4-wall light-tight tube (~890mm deep) around the housing | 1 lot | $60–$120 |
| Flat black paint (RAL 9005) | Interior face + bay interior | 2 qt | $20–$30 |
| **Panel subtotal** | | | **$1,090–$1,660** |

### 8.2 Housed Revolving Door (housing + drum)

| Item | Specification | Qty | Est. cost (USD) |
|------|--------------|-----|----------------|
| 5mm UV-stabilized HDPE sheet (black) | Ø900 fixed housing shell — LT_HOUSING_T (rolled + extrusion-welded, ~7 m²) | 1 lot | $180–$280 |
| 4mm black polypropylene sheet | Ø864 revolving drum shell + top/bottom caps — LT_DRUM_T (~7 m²) | 1 lot | $150–$240 |
| SKF 6215-2RS1 sealed bearing | Top and bottom (drum rotation) | 2 | $90–$130 |
| 75mm Ø × 150mm steel stub shaft | Bearing shafts | 2 | $30–$50 |
| Felt/brush wiper strip + 12mm closed-cell neoprene | Drum↔housing rotating seal (opening edges + top/bottom rings) + drum top/bottom | 1 lot | $40–$60 |
| Silicone bead sealant (black, UV-stable) | Bearing housing seal | 1 | $10–$15 |
| 100mm Ø SS grab rail | Interior handle, 400mm cut length | 1 | $15–$25 |
| Matte-black interior finish | Black-pigmented sheet (no etch-prime); scuff + flat-black touch-in at welds | 1 | $40–$70 |
| Stainless fasteners + nylon isolation washers | Steel shaft/bearing ↔ plastic shell joints (no galvanic couple, plastic↔plastic elsewhere) | 1 lot | $30–$50 |
| Plastic fabrication (roll 2 cylinders, hot-air / extrusion weld, fit, bearings) | 16–22 hrs labor | 1 | $800–$1,150 |
| **Housing + drum subtotal** | | | **$1,385–$2,070** |

### 8.3 Sliding Carriage

| Item | Specification | Qty | Est. cost (USD) |
|------|--------------|-----|----------------|
| HGR20 linear guide rail (1200mm) | Floor/ceiling rails, both walls — span the ~880mm transport slide + carriage | 4 | $180–$280 |
| HGH20CA carriage block | 2 per rail | 8 | $120–$200 |
| 60 × 60 × 3mm SHS mild steel (2400mm) | Left-side carriage beam | 1 | $25–$40 |
| Destaco 207-U toggle clamp | Operational + transport locks | 4 | $60–$100 |
| Nylon brush strip (doubled, per meter) | Carriage beam slot seals — ~5 m each side | 10 m | $40–$60 |
| 10mm closed-cell neoprene pad (50 × 30mm) | Rail channel seals | 4 | $10–$15 |
| 15mm EPDM strip (self-adhesive, per meter) | Panel edge-to-wall clearance seals — ~5 m each side | 10 m | $30–$50 |
| **Carriage subtotal** | | | **$465–$745** |

### 8.4 Fixed Door Frame

| Item | Specification | Qty | Est. cost (USD) |
|------|--------------|-----|----------------|
| 50 × 50 × 3mm RHS mild steel (6 m lengths) | Frame members | 3 | $90–$120 |
| 3mm steel plate/angle (~110mm × ~4 m) | Top + bottom seal lips — threshold upstand (bottom, notched around drum) + frame-top downstand (top, continuous full width); light paths #6–#7 | 1 | $45–$80 |
| Welding / fabrication | Frame assembly + wall attachment | 1 | $200–$350 |
| **Door frame subtotal** | | | **$335–$550** |

### 8.5 Cost Summary

| Assembly | Low estimate | High estimate |
|----------|------------|--------------|
| Panel structure (incl. B2 bay) | $1,090 | $1,660 |
| Housing + drum (plastic skin) | $1,385 | $2,070 |
| Sliding carriage | $465 | $745 |
| Fixed door frame | $335 | $550 |
| **Total** | **$3,275** | **$5,025** |

---

## 9. Maintenance

| Interval | Task |
|----------|------|
| Every use | Dark-adaptation light seal check (5 min) — mark any light points with gaffer tape |
| Every 20 mode conversions | Inspect doubled nylon brush strips at carriage beam slots for wear |
| Every 6 months | Inspect EPDM perimeter gasket compression; replace if permanently deformed |
| Every 6 months | Inspect neoprene drum seals (top/bottom) for wear and adhesion |
| Annually | Replace brush strips (all carriage/guide slots) |
| Annually | Lubricate HGR20 rails and carriage blocks per manufacturer spec |
| Annually | Check SKF 6215 bearings for roughness — sealed for life, replace only if failed |
| Annually | Inspect Destaco toggle clamps for latch engagement and spring tension |
| Annually | Inspect Southco cam latches for compression force; adjust or replace striker |
| Every 2 years | Re-seal drum top/bottom neoprene wiper strips and silicone bead |
| As needed | Re-apply flat black interior paint where scuffed or worn |

---

## 10. Source References

| Item | Source |
|------|--------|
| SKF 6215-2RS1 bearing specification | [SKF Product Catalog](https://www.skf.com/group/products/rolling-bearings/ball-bearings/deep-groove-ball-bearings/productid-6215-2RS1) — radial load 52.7 kN static, sealed, C3 clearance |
| Southco C2-33 cam latch | [Southco catalog](https://southco.com/en_us_int/c2-33-11) — flush-mount cam compression latch |
| Destaco 207-U toggle clamp | [Destaco catalog](https://www.destaco.com/207-u.html) — horizontal hold-down clamp, 375 lb capacity |
| HGR20 / HGH20CA linear guide | [HIWIN equivalent](https://hiwin.com/products/linear-guideways/) — generic 20mm profile linear rail system |
| EPDM gasket material | [McMaster-Carr](https://www.mcmaster.com/epdm-rubber-sheets) — closed-cell EPDM, UV-stable |
| Neoprene wiper strip | [McMaster-Carr #93855K6](https://www.mcmaster.com/93855K6) — closed-cell, pressure-sensitive adhesive |
| Revolving drum light trap design | See [Light Trap Selection](light-trap-selection.md) for full commercial comparison and custom specification |
| Sliding carriage specification | See [Equipment Layout Report](equipment-layout-report.md) §6 for clearance analysis and light seal design |
| Panel construction drawings | See [Engineering Diagrams](engineering-diagrams.md) §12 — Sheets 1–5 |

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
