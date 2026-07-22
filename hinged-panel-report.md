<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Hinged Light-Trap Panel

## 1. Purpose

TBS-001 requires a light-tight seal at the cargo door end of the container that
simultaneously allows personnel access during operation without admitting daylight.
The hinged light-trap panel fills both roles: it seals the full <!-- BEGIN fact:container_width_mm -->2,362<!-- END fact:container_width_mm --> × <!-- BEGIN fact:container_height_mm -->2,388<!-- END fact:container_height_mm -->mm
cargo door opening as a rigid structural panel, and incorporates a revolving drum
light trap that permits operators to enter and exit the darkened interior at any
time without opening the panel or breaking the light seal. In case of emergency, or to easy loading and unloading of materials, the whole hinged panel can open fully, being locked from the inside.

**Sheet 1 — Front Elevation (1:20): Panel Dimensions, Drum, Hinges, Latches (interior face)**
![TBS-001 Hinged Panel — Sheet 1: Front Elevation](assets/hingepanel-sheet1.png)

**Design goals:**

- 100% light exclusion — no straight-line optical path from exterior to interior
- Single-operator personnel access at any time during exposure
- 180° outward swing for full-width loading access (IBC totes, equipment)
- ~<!-- BEGIN fact:panel_swing_deg -->56<!-- END fact:panel_swing_deg -->° transport swing about the Ø89 pivot post — carries the B2 punch-out bay inboard of the ISO container doors (true min X +<!-- BEGIN fact:swung_door_clearance_mm -->59<!-- END fact:swung_door_clearance_mm -->mm) + hardware
- Emergency egress operable from inside without tools
- Weatherproof for outdoor field deployment (IP44 rated seals)
- Single-person mode conversion (~5 minutes)

<!-- brochure:skip -->
**Interactive 3D model** — the revolving light-trap drum, hinged stepped panel, Ø89 swing pivot, fixed door frame (with the bottom brush seal), and Fan B. Drag to orbit, scroll to zoom.

<div class="sketchfab-embed-wrapper">
  <div style="position:relative;width:100%;padding-bottom:56.25%;">
    <iframe title="TBS-001 Lighttrap Model" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/a4f73191b8bb4d17a6e764585ca695be/embed" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>
  </div>
  <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"><a href="https://sketchfab.com/3d-models/tbs-001-lighttrap-model-a4f73191b8bb4d17a6e764585ca695be?utm_medium=embed&utm_campaign=share-popup&utm_content=a4f73191b8bb4d17a6e764585ca695be" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">TBS-001 Lighttrap Model</a> by <a href="https://sketchfab.com/alvin91403?utm_medium=embed&utm_campaign=share-popup&utm_content=a4f73191b8bb4d17a6e764585ca695be" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">alvin91403</a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=a4f73191b8bb4d17a6e764585ca695be" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>
</div>
<!-- brochure:endskip -->

---

## 2. Panel Construction

### 2.1 Stepped Profile

The panel has three thickness zones to accommodate the revolving drum in the center
while keeping the corners flush with the container walls.

**Sheet 2 — Plan Cross-Section (1:10 horiz / 1:1 depth): Housed Revolving Door — Housing, Drum & Light-Tight Geometry**
![TBS-001 Hinged Panel — Sheet 2: Plan Cross-Section](assets/hingepanel-sheet2.png)

| Zone | Width (mm) | Thickness (mm) | Construction |
|------|--------------|-----------|---------------|-------------|
| Near corner | 653 | 40 | 4mm PP skin + 3mm Al core + 4mm PP skin (40mm framed); **18mm-ply Fan-B mount band** bottom→1,125mm |
| Center | 1,056 | 120 | 4mm PP skin + 84mm RHS frame + 4mm PP skin |
| Far corner | 653 | 40 | 4mm PP skin + 3mm Al core + 4mm PP skin (40mm framed) |

The 80mm step between corner and center zones to locate the
light-trap housing; the corner zones are
flush-faced panels that seal against the fixed door frame.

### 2.2 Frame

| Parameter | Value |
|-----------|-------|
| Frame material | 50 × 50 × 3mm RHS mild steel |
| Outer dimensions | <!-- BEGIN fact:container_width_mm -->2,362<!-- END fact:container_width_mm --> × <!-- BEGIN fact:container_height_mm -->2,388<!-- END fact:container_height_mm -->mm |
| Skin (each face) | **4mm PP plastic sheet** (rev11; same material as the drum/housing), set in U-channels — black-pigmented, light-tight, moisture/chemical-proof. **Exception:** an 18mm exterior-grade plywood band on the Fan B corner (bottom up to 1,125mm) for rigid fan/duct mounting + screw retention |
| Interior finish | Black-pigmented sheet (PP) + flat-black touch-in — optically dead at visible wavelengths |
| Frame perimeter | Welded corners, mitered joints |
| Panel weight (full panel: skins + Ø900 housing + B2 bay, excl. drum) | ~171 kg (first-principles: 125 kg framed skins + 22 kg housing + 25 kg B2 bay). The 4mm-PP-skin swap cut ~72 kg vs the 18mm-ply build. See §2.4–2.5 for the movable breakdown + trade study |

### 2.3 Perimeter Seals

A 20mm closed-cell EPDM compression gasket runs the two **vertical** edges of the panel,
seated in an extruded aluminum channel, and compresses against the fixed welded door
frame (50 × 50 × 3mm RHS) when the four cam latches engage. The **top and bottom** edges
are **nylon strip-brush** light seals instead (§6, paths #3/#4): because the panel edge
**sweeps sideways** through the seal as it swings, a brush passes the edge through cleanly
where a compression EPDM would drag and deform. Together they give a light-tight seal on
all four sides.

A **second** 20mm EPDM gasket — the **housing-surround seal** — runs as a ring around
the Ø900 light-trap housing aperture. Because the housing is **fixed** (only the drum
rotates inside it), this gasket seals the fixed surround to the frame independently of
the moving panel, all the way around the opening the housing passes through. It sits in
the same exterior door plane, concentric inboard of the panel-perimeter seal (see
§6, light-path #8).

### 2.4 Movable-Panel Weight Breakdown

The transport scheme swings the panel + drum ~<!-- BEGIN fact:panel_swing_deg -->56<!-- END fact:panel_swing_deg -->° about the vertical Ø89 pivot, so
the **movable assembly** is everything that rotates about that pivot. The breakdown
below is first-principles from the geometry constants (reproducible via
`src/generators/generate_movable_panel_weight.py`); it isolates the swing zone
 and deducts the Ø900 housing aperture from the center skins, so it
is slightly lower than the whole-panel figure carried in the
[Weight Distribution Report §3.2](weight-distribution-report.md).

| Group | Component | Construction | kg |
|-------|-----------|-------------|---:|
| **A · Skins + frame** | Fan B mount band | 18mm ply, 0.47m × 0.99m, 2 faces | 10.2 |
| | PP corner skins | 4mm PP (near above band + far) | 14.8 |
| | Corner Al core plates | 3mm 5052 | 20.3 |
| | Center RHS frame | 50×50×3 steel SHS, 11.1m | 49.2 |
| | PP center skins | 4mm PP, Ø900 aperture deducted | 13.7 |
| | **A subtotal** | | **108.1** |
| **B · Housing** | HDPE shell + steel flange/hub | Ø900×5mm, two 80° openings | 21.8 |
| **C · Drum** | PP C-shell + caps + Ø75 shafts + 2× SKF 6215 + stiffeners + grab rail | Ø864×4mm | 37.8 |
| **D · Bay** | B2 punch-out bay walls | 4mm PP, 4-wall tube 0.89m deep | 24.9 |
| **E · Cage** | Drum support cage frame | ~25×25×3 angle, 16.1m box | 16.1 |
| **F · Seals** | Vertical perimeter + housing EPDM + top/bottom strip brush + drum wipers | 20mm foam + strip/felt brush | 2.7 |
| **G · Latches** | Cam latches (4) | ~0.5 kg each | 2.0 |
| **H · Pivot (rotating)** | Thrust/journal bearings + collar/hub | carries leaf at pivot | 13.0 |
| | **MOVABLE TOTAL (carried-rotating)** | | **≈226** |
| | *+ transport-only locks (stays + 4 saddles)* | engaged only when swung | +10 |

**By material:** steel 103 kg (46%), PP 74 kg (33%), aluminum 20 kg (9%),
HDPE 16 kg (7%), plywood 10 kg (4%, Fan B band only), EPDM/other 3 kg.

**Findings.** The largest remaining single item is the **steel center
RHS frame (49 kg)** — the structural spine carrying the drum — which is the only
meaningful target left (§2.5). Because the swing axis is **vertical**, this mass
produces **no gravity overturning torque** at any swing angle; it matters for the
thrust-bearing/pivot-post sizing, for handling during assembly (still beyond a
two-person lift — an engine crane or gantry hoist is required), and for total
container payload.

### 2.5 Weight-Reduction

Black-pigmented PP
is light-tight (proven on the drum), moisture- and chemical-proof in the wet darkroom,
and floats in its channel to absorb its higher thermal expansion. A tighter stiffener-
channel grid (~400–450mm centers) keeps the floppier 4mm sheet flat at the EPDM seal
line. **One exception:** the Fan B corner keeps an **18mm plywood band** (bottom up to
1,125mm) for rigid fan/duct mounting + screw retention. Net: **~72 kg off** the panel
(243 → 171 kg), at roughly comparable material cost (PP sheet + U-channel ≈ ply +
adhesive/fasteners; panel BOM rises ~$100, see §8.1).

---

## 3. Housed Revolving-Door Light Lock

> The light lock is  a
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
| Height | Top at Z=2,250mm (upper bearing on panel top rail) |
| Mounting | **Carried with the panel** — rides at Z=130 on the panel bottom rail (130mm floor gap → clears the tray rim, and the swinging cage passes over the Z115 walkway brackets). Operator steps up ~130mm over the threshold to enter; exits level onto the walkway deck (also Z=130). |
| Wall thickness | 5mm UV-HDPE housing (LT_HOUSING_T) + 4mm PP drum (LT_DRUM_T) — rolled and extrusion-welded plastic skin (rev 9 / B2; was 3mm aluminum); opening edge-stiffened |
| Interior finish | Black-pigmented sheet + flat-black touch-in at welds (no etch-prime) |
| Exterior finish | UV-stabilized black/gray sheet — inherent, no primer |
| Clear walking height | 1,910mm (between bearings) |
| Internal baffles | **None** — light-tightness is by the fixed-housing geometry (§3.3) |
| Weight | housing ~22 kg + rotating drum ~38 kg = **~60 kg** (plastic skin, ≈60% of the 3mm-aluminum ~99 kg; the steel shaft/bearings set a floor the shell mass can't drop below) |

### 3.2 Bearings

| Item | Specification |
|------|--------------|
| Bearing model (×2) | SKF 6215-2RS1 sealed deep-groove ball bearing |
| Bore | 75mm ID, 130mm OD, 25mm wide |
| Clearance | C3 |
| Radial load rating | 52.7 kN (basic dynamic C) |
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

See [Light Trap Selection](light-trap-selection.md) §5 and **Sheet 5**
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
at 900mm height. The handle is attached by a welded bracket — no through-bolt
penetration of the drum wall on the exterior face. This eliminates a potential
light leak path. The operator enters by pushing the bare exterior drum wall, then
uses the interior grab rail to pull the drum closed and brace during exit.

### 3.6 Access & Light-Tightness Verification (both tests pass)

**Sheet 5 — Light-lock access & light-tightness verification**
![TBS-001 Hinged Panel — Sheet 5: Light-Lock Verification](assets/hingepanel-sheet5.png)

**1. Does a person fit? — Yes.** The drum is a
single-opening C-shell, so the whole **~Ø850mm bore** is clear standing space. The
80° opening gives a **~555mm passage** (sideways entry), enough for a single operator to enter and
turn inside. Emergency egress remains the whole panel swinging open.

**2. As the drum rotates, can daylight enter? — No.** The fixed housing's two 80°
openings are 180° apart, so the 80° drum opening can never reach both at once: at
**enter** the exterior opening feeds the bore but the interior opening is covered by
the drum's solid wall; at **transit** both housing openings are covered; at **exit**
the exterior opening is covered. There is no straight-line path at any angle.

---

## 4. Hinges and Latches

### 4.1 Hinges

| Parameter | Value |
|-----------|-------|
| Type | Vertical **Ø89×8 CHS pivot post** (the reused film-plane far-left upright) on a thrust collar + top/bottom hub bearings — **STRUCTURAL SIGN-OFF REQUIRED** |
| Quantity | 1 post (carries the full bay + housing + drum swing cantilever, ~3.6 kN·m, SF ~3.7 in S355) |
| Position | Far-left panel edge |
| Mounting | Post fixed top + bottom to the container end structure; the swinging frame rotates on the hub bearings (vertical axis ⇒ balanced at any angle, no gravity torque) |
| Swing | ~<!-- BEGIN fact:panel_swing_deg -->56<!-- END fact:panel_swing_deg -->° inboard to the transport position (locked by the top + bottom wall stays); swings clear of the door plane for personnel/equipment access |

The plastic-skinned drum/housing (LT_DRUM_T = 4mm PP,
LT_HOUSING_T = 5mm UV-HDPE) keeps the added mass modest. Because the pivot axis is
**vertical**, the assembly is balanced at any swing angle — no gravity torque and no
free-edge sag, so no swing-support caster is needed (the old B2 barrel-hinge + caster
scheme is retired). The **pivot post and its bearing + weld pattern require a structural
engineer's sign-off** before fabrication.

### 4.2 Cam Latches

| Parameter | Value |
|-----------|-------|
| Model | Southco C2-33 cam compression latch |
| Quantity | 4 (one at each corner) |
| Positions | 210mm and 2,152mm from side edges, 220mm and 2,168mm from floor |
| Mounting face | **Interior** — deliberate safety design for emergency egress |
| Seal compression | Compresses EPDM perimeter gasket against fixed door frame |

**Emergency egress:** If the revolving drum jams and prevents normal egress, an
operator inside the container can release all four interior-mounted cam latches
independently and push the panel open outward. The panel swings 180° clear of all
interior equipment.

### 4.3 Interior Pull Handle

A grab/pull handle is **through-bolted to the panel's structural frame on the interior
face** — the **left jamb of the drum aperture**, at waist height — so a single operator
can grip it and swing the heavy (~171 kg movable) panel open from **inside** the container,
both for the emergency-egress swing (§4.2) and to initiate the transport rotation (§5). It
bolts to the steel frame, not the PP skin.

| Parameter | Value |
|-----------|-------|
| Type | 316 SS D-grab pull handle, ~300mm grip span, 25mm round bar |
| Mounting | Through-bolted to the 50 × 50 × 3mm RHS frame jamb beside the drum aperture — **2 × M8 SS bolts** passing through **both** RHS walls into an interior backing plate/washers (not screwed to the PP skin) |
| Position | Interior face of the **swinging** panel, on the **left drum-aperture jamb**. The transport swing pivots on the **far** edge (§5), so this near-of-center jamb keeps the operator's leverage while landing the load on frame steel right beside the drum (rather than the unbacked PP skin) |
| Finish | **Matte-black powder-coat** — the interior must stay optically dead (stray-light control for the pinhole), so the handle is not left bare/reflective |

See [§8.1](#81-panel-structure) for the part; the handle is also shown on the interior-face
**Sheet 1** front elevation.

**Sheet 6 — Interior Pull Handle: mounting detail (handle through-bolted to the RHS frame)**
![TBS-001 Hinged Panel — Sheet 6: Pull Handle Mounting Detail](assets/hingepanel-sheet6.png)

---

## 5. Rotating Transport System

For transport the entire swinging assembly — the panel center section, the B2
punch-out bay, and the housing + revolving drum — **revolves ~<!-- BEGIN fact:panel_swing_deg -->56<!-- END fact:panel_swing_deg -->° about a vertical Ø89mm CHS
pivot post** (the reused film-plane far-left upright, at X=175mm / Yd=2,287mm). The swing carries
the bay's ~890mm exterior overhang from outside the cargo-door plane to inboard of it, so the ISO
doors close.

Two narrow strips stay fixed at the door plane and do **not** swing: the near strip
and the far strip. The cargo doors close outboard of the
fixed near strip.

To let the swinging cage cross the X=150mm film-plane rail line, the **two left film rails
(top-left + bottom-left) lift out of their drop-in saddles** and the **left walkway + door-end
near-deck section lift out** before the swing; all are re-seated to datum afterward.

### 5.1 Panel Positions

**Sheet 4 — Rotating transport + swing clearance: panel swings <!-- BEGIN fact:panel_swing_deg -->56<!-- END fact:panel_swing_deg -->° about the pivot (camera vs swung), removable left rails**
![TBS-001 Hinged Panel — Sheet 4: Rotating Transport + Swing Clearance](assets/hingepanel-sheet4.png)

| Position | Bay front-right corner X | Container doors clear? |
|----------|-------------------------|----------------------|
| Operational (0°) | −890mm (bay protrudes ~890mm outside the door plane) | No — the cargo doors stay open during operation |
| Transport (swung <!-- BEGIN fact:panel_swing_deg -->56<!-- END fact:panel_swing_deg -->°) | +<!-- BEGIN fact:swung_door_clearance_mm -->59<!-- END fact:swung_door_clearance_mm -->mm (true min X over the whole swept assembly — computed 58.6mm at this corner) | Yes — the swept frame is fully inboard of the closed door |

### 5.2 Locking

| State | Method |
|-------|--------|
| Operational (0°) | 4 × interior cam latches (§4) compress the EPDM **vertical** perimeter + cut seals against the door frame; the top + bottom **strip-brush** seals are passive (always engaged, no compression) |
| Transport (swung <!-- BEGIN fact:panel_swing_deg -->56<!-- END fact:panel_swing_deg -->°) | Top + bottom **wall stays** — hook welded to the **swinging panel's left perimeter 50×50×3 RHS stile** (the steel frame member at the swing cut) ↔ eye on the near wall, tensioned by turnbuckle, forming a couple. Engaged after the swing, released before swing-back. |

> **Stay hooks land on steel, not the skin.** The transport-stay couple carries real tension, so both hooks weld to the **left perimeter RHS stile** of the swinging frame — *not* the 4mm PP plastic skin (rev11). They were relocated from the mid-corner (Yd≈350), which the plastic-skin swap left unbacked above the plywood band; the perimeter stile is the farthest point from the pivot (best lever arm) and a continuous welded steel load path into the frame.

### 5.3 Floor Gap

The panel + drum cage ride at a **130mm floor gap** (the grate-top level set
by the +50mm walkway raise), carried by the pivot post on its thrust collar + hub
bearings. The gap clears the processing tray rim with margin; it is also the threshold
the drum revolves over and the floor datum the swing arc sweeps at.

**The housing + drum ride at the same Z=130**, so the swinging cage passes over the
tray basin — and over the Z115 door-end walkway brackets — rather than colliding with
them. The swing (about a vertical pivot, so the bottom edge stays at Z=130 throughout)
is what makes the deep Ø900 housing transport-feasible without a slide; a floor-mounted
housing would have fouled the tray. The 130mm floor gap is closed in the operational
position by the continuous bottom brush seal (§6).

The 130mm gap would otherwise be a straight light path, so it is light-sealed by the
fixed-frame **bottom brush seal** described in §6 — a threshold-mounted nylon-filament
strip brush whose bristles the panel bottom edge sweeps through. Because it is a brush
(neither a floor-contact seal nor a compression EPDM), it never fouls the tray rim, seals
continuously without cam-latch compression, and the panel edge passes through it cleanly
on the swing.

### 5.4 Transport Conversion Sequence

The rotation transport + swing clearance vs the film-plane left mechanism is shown in
**Sheet 4** (above): the panel + drum swing ~<!-- BEGIN fact:panel_swing_deg -->56<!-- END fact:panel_swing_deg -->° about the pivot, pulling the bay inboard of
the door plane (true min X +<!-- BEGIN fact:swung_door_clearance_mm -->59<!-- END fact:swung_door_clearance_mm --> mm); the two left film rails are struck (removable) so the
swinging cage transitions the X=150 rail plane, then re-seat to the film datum.

The swing carries the drum cage through **X=150**, where the film-plane mechanism's
left edge sits, so the **two left film rails (TL + BL) must be struck before the swing**
and re-seated after (the tapered dowels return the film datum). The muslin screen must
be struck regardless — the fragile screen cannot travel mounted. The swing **clears the
door-end walkway brackets at Z**: the cage underside at Z=130 passes over the Z=115
bracket tops, so **no walkway bracket is demounted** (superseding the old slide, which
swept past them at floor level and required striking them).

Order of operations (single person, ~10 min) — see the [Operating Manual](operating-manual.md) §5.5:

1. Park the revolving drum and pin its rotation.
2. Remove the muslin screen from its frame and stow it (rolled); knock down the
   demountable brace cage (saddle/thumbscrew portals).
3. Lift out the left walkway + door-end near-deck section.
4. **Strike the two left film rails (TL + BL)** — release each clamp bar, lift the rail
   out of its saddles, and stow.
5. Release the four Southco cam latches (releases the perimeter + cut seals).
6. **Swing the frame ~<!-- BEGIN fact:panel_swing_deg -->56<!-- END fact:panel_swing_deg -->° inboard** about the pivot, assisted (balanced about the
   vertical axis — no gravity torque; control momentum at the stop).
7. Engage the top + bottom wall stays (the transport lock).
8. Close the ISO cargo doors (they clear the swung frame by +<!-- BEGIN fact:swung_door_clearance_mm -->59<!-- END fact:swung_door_clearance_mm --> mm).

Re-deployment reverses the sequence.

---

## 6. Light Seal Design

The swinging panel seals against the fixed door frame in its operational (closed)
position. Five light ingress paths are sealed:

| # | Light path | Seal method |
|---|-----------|-------------|
| 1 | Panel perimeter (left/right) → door frame | 20mm EPDM gasket in an aluminum channel down each **vertical** edge, compressed by the 4 × Southco C2-33 cam latches against the fixed door frame at X=0. (The **top + bottom** edges are strip-brush seals — paths #3/#4 — not compression EPDM.) |
| 2 | Swing cuts → fixed strips | The swinging center+corners separate from the two FIXED strips (near Yd0–180, far Yd2287–2362, which carries the pivot) along vertical cuts. A 20mm EPDM **cut seal** runs the full panel height down each cut, compressed by the cam latches when the panel is latched at the door plane. Replaces the old sliding-carriage beam/guide-slot brush seals. (Sheet 3, Detail D.) |
| 3 | Panel bottom → 130mm floor gap | Fixed-frame **bottom brush seal** — a continuous nylon-filament strip brush in an aluminum holder on the threshold, its bristles rising above the panel bottom edge (Z=130) across the **full panel-bottom width, continuous (no notch)** — the housing/drum ride at Z=130 and never reach the floor, so the gap is uniform and the bristle wall closes it light-tight. The panel bottom edge **sweeps through the bristles** as the panel swings — so this edge is a **brush, not a compression seal** (a compression EPDM would drag and deform under the sideways sweep; a brush passes the edge through cleanly — the same principle as the drum-opening brush seals). The bristle density is the seal; no cam-latch compression on this edge. (Sheet 3, Detail B.) |
| 4 | Panel top → frame gap | Fixed-frame **top brush seal** — the mirror of #3: a nylon-filament strip brush in a holder on the frame top rail, its bristles reaching ~30mm below the panel top edge. The drum stub shaft stops below it, so the brush runs as **one continuous member across the full panel-top width — no notch — meeting across the center**. The panel + drum-box top edge **sweeps through the bristles** as the panel swings — a deliberate ~30mm bristle overlap in the closed position, **not a clash**. No cam-latch compression on this edge; the bristles are the seal. (Sheet 3, Detail C.) |
| 5 | Housing surround → door frame | The Ø900 light-trap housing carries the revolving drum and swings with the panel. A **second 20mm EPDM gasket** rings the housing aperture (floor gap up to the housing top at Z=2250), concentric **inboard** of the panel-perimeter seal (#1), seated in the door plane. In the closed position it seals the housing surround to the frame all the way around the opening — light-tight. (3D: the `door_frame()` "Housing surround seal", in both the light-trap and overview models.) |

**Seal verification:** After mode conversion, the operator performs a 5-minute
dark-adaptation check inside the container with all seals engaged. Any visible light
points are marked with gaffer tape for re-sealing.

---

## 7. Fixed Door Frame

A fixed welded door frame provides the seal landing surface (perimeter, cut, and lip
seals) for the swinging panel, and the structural anchor for the wall-stay eyes.

| Parameter | Value |
|-----------|-------|
| Material | 50 × 50 × 3mm RHS mild steel |
| Position | X=0 (container end wall inner face) |
| Function | Seal landing for the swinging-panel **vertical** perimeter + cut seals + housing-surround EPDM, plus the **top + bottom strip-brush** light seals |
| Attachment | Welded to container end wall structural members |
| Cut-seal landings | 2 × vertical EPDM landings (the swing cuts between the swinging panel and the fixed strips) |
| Bottom brush seal | Continuous nylon-filament **strip brush** in an aluminum holder on the threshold, **full panel-bottom width (no notch — drum rides at Z=130)** — the panel bottom edge sweeps through the bristles (see §6 path #3) |
| Top brush seal | Mirror of the bottom: continuous nylon-filament **strip brush** in a holder on the frame top rail, bristles reaching ~30mm below the panel top edge, full panel-top width and **continuous across the center** (the drum does not reach the top, so no notch) — the panel + drum-box top edge sweeps through the bristles (see §6 path #4) |

---

## 8. Parts List

### 8.1 Panel Structure

<!-- BEGIN parts:panel -->
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 50 × 50 × 3mm RHS mild steel (6 m lengths) | Frame perimeter + internal members | 4 ea | Metal Supermarkets | $120–$160 |
| 4mm black PP plastic sheet (1220 × 2,440mm) | Panel skins, both faces (~12 m²) — rev11, replaces 18mm ply | 4 sheet | TAP Plastics / Curbell | $260–$420 |
| Exterior-grade plywood (Fan B mount band) | ¾" (18mm) exterior-grade project panel (610×1220mm); Fan B mount band, one corner bottom→1,125mm | 1 2'×4' ¾" panel | Home Depot | $30–$50 |
| 3mm aluminum plate (1220 × 2,440mm) | Corner zone core plates | 2 ea | Online Metals | $360–$460 |
| 20mm EPDM gasket (per meter, closed-cell) | Perimeter seal (~10 m) + housing-surround ring (~6 m) + 2× vertical cut seals at Yd180/2287 (~5 m) | 21 m | McMaster-Carr | $84–$126 |
| Aluminum U-channel (per meter) | Gasket retainer + PP-skin retention (perimeter + housing-surround + stiffener grid) | 40 m | Online Metals | $120–$200 |
| Southco C2-33 cam compression latch | Interior-mounted corner latches (compress the perimeter + cut + lip seals) | 4 ea | Southco / McMaster-Carr | $76–$104 |
| 4mm black PP sheet + EPDM lip | B2 punch-out bay — 4-wall light-tight tube (~890mm deep) around the housing (rev11) | 1 lot | TAP Plastics | $60–$120 |
| Flat black paint (RAL 9005) | Bay/weld touch-in (PP skins are pre-pigmented black) | 1 qt | Local fab | $10–$20 |
| 316 SS D-grab pull handle (~300mm) + 2× M8 SS bolts + backing plate, matte-black | Interior pull handle — through-bolted to the frame (§4.3) | 1 ea | McMaster-Carr | $20–$35 |
| **Panel total** | | | | **$1,140–$1,695** |
<!-- END parts:panel -->


*The panel pivot post + bearings + drum cage + wall stays are itemized in §8.3.*

### 8.2 Housed Revolving Door (housing + drum)

<!-- BEGIN parts:lightlock -->
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 5mm UV-stabilized HDPE sheet (black) | Ø900 fixed housing shell — LT_HOUSING_T (rolled + extrusion-welded, ~7 m²) | 1 lot | TAP Plastics / Online Metals | $180–$280 |
| 4mm black polypropylene sheet | Ø864 revolving drum shell + top/bottom caps — LT_DRUM_T (~7 m²) | 1 lot | TAP Plastics / Curbell | $150–$240 |
| [SKF 6215-2RS1 sealed bearing](https://bearingsdirect.com/6215-2rs-ball-bearing-75x130x25-sealed-6215-2nse/) (6215-2RS) | Top and bottom (drum rotation). Ø75 bore × Ø130 OD × 25mm wide, C=52.7 kN, both-sides sealed (6215-2RS / 6215-2NSE; SKF designation 6215-2RS1). Buy the ABEC-1 grade: the drum is a hand-rotated, low-speed, low-load light-lock — the tighter ABEC-3 tolerance buys nothing here (SKF's standard 6215-2RS1 is Normal/P0 = ABEC 1). VERIFIED $60.59 ea at Bearings Direct 2026-07-18. ALT: McMaster 6138K125 @ $394.88 ea — a heavy commodity-bearing premium, prefer the distributor. | 2 ea | Bearings Direct / McMaster-Carr | $121 |
| 75mm Ø × 150mm steel stub shaft | Bearing shafts | 2 ea | Steel service center | $30–$50 |
| Felt/brush wiper strip + 12mm closed-cell neoprene | Drum↔housing rotating seal (opening edges + top/bottom rings) + drum top/bottom | 1 lot | McMaster-Carr | $40–$60 |
| Silicone bead sealant (black, UV-stable) | Bearing housing seal | 1 ea | McMaster-Carr | $10–$15 |
| 100mm Ø SS grab rail | Interior handle, 400mm cut length | 1 ea | McMaster-Carr | $15–$25 |
| Matte-black interior finish | Black-pigmented sheet (no etch-prime); scuff + flat-black touch-in at welds | 1 ea | Local fab | $40–$70 |
| Stainless fasteners + nylon isolation washers | Steel shaft/bearing ↔ plastic shell joints (no galvanic couple) | 1 lot | McMaster-Carr | $30–$50 |
| Plastic fabrication (roll 2 cylinders, hot-air / extrusion weld, fit, bearings) | 16–22 hrs labor | 1 lot | Local plastic fab | $800–$1,150 |
| **Lightlock total** | | | | **$1,416–$2,061** |
<!-- END parts:lightlock -->


### 8.3 Swing Pivot Hardware

<!-- BEGIN parts:swing -->
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Ø89×8mm CHS pivot post + machined hub / thrust collar | Upgrades the reused film far-left upright; carries the ~3.6 kN·m swing cantilever — SF 3.7 in S355. Two journal bands (where the DU sleeves ride) turned/ground to Ra ≤0.5 µm — unhardened S355 acceptable per GGB DU (hardening improves life). | 1 ea | Metal Supermarkets / Local fab | $180–$300 |
| [Thrust ball bearing, 51118 (Ø90 bore, single-direction)](https://www.motion.com/products/sku/00132858) (51118) | Carries the ~330 kg (3.24 kN) vertical load at the post base; thrust-only (radial + moment taken by the DU sleeves). 51118 = 90 × 120 × 22mm, static Cₒ ≈190 kN → SF >50; single-direction (gravity-down). Ø90 bore matches the Ø89 post — the machined thrust collar bears on the shaft washer. Chrome steel: grease + wipe annually (humid darkroom); stainless S51118 available ~$100+ if preferred. | 1 ea | Motion / McMaster-Carr | $40–$60 |
| [DU self-lubricating sleeve (journal) bearing, Ø90 bore](https://www.applied.com/c-brands/c-ggb/mb9060du/DU-Self-Lubricating-Bearing/p/102013642) (MB9060DU) | Top + bottom radial location of the post. GGB DU steel-backed PTFE, Ø90 ID × Ø95 OD × 60L (0.796 lb). Cylindrical — pressed into the hub bores (H7/r6); the axial load is on the 51118 thrust bearing so no flange needed. Maintenance-free (dry-running), no oil to re-embed. Service pressure ≈2 N/mm² vs 140 N/mm² dynamic (>60× margin). Price TBD from Applied — placeholder band. | 2 ea | Applied / Isostatic (TU equiv.) | $60–$110 |
| Drum support cage, 40 × 40 × 3mm SHS | Steel frame carrying the Ø900 housing + drum on the swinging leaf | 1 lot | Local fab | $70–$120 |
| Top + bottom wall stays + 4-bolt anchor plates | Transport lock — M16 turnbuckle + eye/hook rods + inside/outside wall plates | 2 set | McMaster-Carr | $90–$160 |
| Drop-in rail saddles + tapered dowels | For the 2 removable left film rails (TL + BL); dowels set the film datum | 4 ea | Local fab / McMaster-Carr | $80–$130 |
| **Swing total** | | | | **$520–$880** |
<!-- END parts:swing -->


### 8.4 Fixed Door Frame

<!-- BEGIN parts:door -->
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| 50 × 50 × 3mm RHS mild steel (6 m lengths) | Frame members | 3 ea | Metal Supermarkets | $90–$120 |
| [Tight-seal nylon strip brush + aluminum holder (~4.7 m, top + bottom)](https://www.mcmaster.com/74405T12-74405T126/) (74405T12) | Top + bottom door-frame light seals (paths #3–#4) — 2× McMaster 74405T12 nylon Tight-Seal Strip Brush (8 ft, 1" overall height, $28.88 ea) in 2× McMaster 8813T53 aluminum holder channel (8 ft, $35.37 ea) = $128.50 firm; covers full panel width top + bottom (~2× C_WID ≈ 4.7 m ≈ 15.5 ft, from 4× 8 ft lengths). The swinging panel edge SWEEPS THROUGH the bristles, so a brush (not a compression EPDM, which would drag under the sideways sweep) — same principle as the drum-opening brush seals. | 1 lot | McMaster-Carr | $129 |
| Welding / fabrication | Frame assembly + wall attachment | 1 lot | Local fab | $200–$350 |
| **Door total** | | | | **$419–$599** |
<!-- END parts:door -->


### 8.5 Cost Summary

| Assembly | Low estimate | High estimate |
|----------|------------|--------------|
| Panel structure (incl. B2 bay + pull handle) | <!-- BEGIN costing:hp-panel-low -->$1,140<!-- END costing:hp-panel-low --> | <!-- BEGIN costing:hp-panel-high -->$1,695<!-- END costing:hp-panel-high --> |
| Housing + drum (plastic skin) | <!-- BEGIN costing:hp-housing-low -->$1,416<!-- END costing:hp-housing-low --> | <!-- BEGIN costing:hp-housing-high -->$2,061<!-- END costing:hp-housing-high --> |
| Swing pivot hardware | <!-- BEGIN costing:hp-swing-low -->$520<!-- END costing:hp-swing-low --> | <!-- BEGIN costing:hp-swing-high -->$880<!-- END costing:hp-swing-high --> |
| Fixed door frame | <!-- BEGIN costing:hp-doorframe-low -->$419<!-- END costing:hp-doorframe-low --> | <!-- BEGIN costing:hp-doorframe-high -->$599<!-- END costing:hp-doorframe-high --> |
| **Total** | **<!-- BEGIN costing:hp-total-low -->$3,495<!-- END costing:hp-total-low -->** | **<!-- BEGIN costing:hp-total-high -->$5,235<!-- END costing:hp-total-high -->** |

---

## 9. Maintenance

| Interval | Task |
|----------|------|
| Every use | Dark-adaptation light seal check (5 min) — mark any light points with gaffer tape |
| Every 20 mode conversions | Inspect the EPDM cut seals at the swing boundaries (Yd180/2287) for wear |
| Every 6 months | Inspect EPDM perimeter gasket compression; replace if permanently deformed |
| Every 6 months | Inspect neoprene drum seals (top/bottom) for wear and adhesion |
| Annually | Inspect the wall-stay turnbuckles, hooks, and eye anchors; verify tension at the locked angle |
| Annually | Grease the 51118 pivot thrust bearing; the DU journal bushings run dry — do **not** oil/grease them — wipe the post journal bands clean and check for free, smooth rotation |
| Annually | Check SKF 6215 bearings for roughness — sealed for life, replace only if failed |
| Annually | Check the drop-in rail saddles + tapered dowels seat the left film rails square to datum |
| Annually | Inspect Southco cam latches for compression force; adjust or replace striker |
| Every 2 years | Re-seal drum top/bottom neoprene wiper strips and silicone bead |
| As needed | Re-apply flat black interior paint where scuffed or worn |

---

## 10. Source References

| Item | Source |
|------|--------|
| SKF 6215-2RS1 bearing specification | [SKF Product Catalog](https://www.skf.com/group/products/rolling-bearings/ball-bearings/deep-groove-ball-bearings/productid-6215-2RS1) — radial load 52.7 kN basic dynamic (C), sealed, C3 clearance |
| Southco C2-33 cam latch | [Southco catalog](https://southco.com/en_us_int/c2-33-11) — flush-mount cam compression latch |
| Turnbuckle + eye/hook (wall stays) | [McMaster-Carr turnbuckles](https://www.mcmaster.com/turnbuckles/) — drop-forged jaw/eye turnbuckles for the transport lock |
| Pivot thrust bearing (51118) | [Motion — SKF 51118](https://www.motion.com/products/sku/00132858) — single-direction thrust ball bearing, Ø90 × 120 × 22mm, static Cₒ ≈190 kN, for the pivot base |
| Pivot journal bushings (MB9060DU) | [Applied — GGB MB9060DU](https://www.applied.com/c-brands/c-ggb/mb9060du/DU-Self-Lubricating-Bearing/p/102013642) — DU self-lubricating sleeve, Ø90 ID × 95 OD × 60L, top + bottom post radial location |
| EPDM gasket material | [McMaster-Carr](https://www.mcmaster.com/epdm-rubber-sheets) — closed-cell EPDM, UV-stable |
| Neoprene wiper strip | [McMaster-Carr #93855K6](https://www.mcmaster.com/93855K6) — closed-cell, pressure-sensitive adhesive |
| Revolving drum light trap design | See [Light Trap Selection](light-trap-selection.md) for full commercial comparison and custom specification |
| Swing mechanism specification | See [Equipment Layout Report](equipment-layout-report.md) §6 for clearance analysis and light seal design |
| Panel construction drawings | See [Engineering Diagrams](engineering-diagrams.md) §12 — Sheets 1–5 |
