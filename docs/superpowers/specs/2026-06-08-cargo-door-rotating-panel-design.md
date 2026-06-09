# Cargo-Door Rotating Hinge-Panel — Transport Scheme (Design Spec)

**Date:** 2026-06-08
**Branch:** `hinge-panel-study` (study artifacts only; nothing cascaded yet)
**Status:** Design agreed in study — pre-cascade. To be reviewed before touching production.
**Replaces:** the slide-based transport of the light-trap panel (rev9 "B2": panel slid
880 mm inboard). The slide exploration is preserved in git tag `transport-study-explore`.

---

## 1. Problem & context

The light-trap panel + drum at the cargo-door end (X≈0) must retract for transport so the
steel cargo doors can close. Three interacting systems drive the design:

1. **Hinge panel** — seals the cargo opening; must open for operator access *and* retract
   for transport.
2. **Light-trap drum** — Ø900 revolving light lock. In **camera mode it extends OUT** the
   door (X−400) so it sits clear of the light cone → no shadow on the image (maximises the
   image/film size). It is **heavy**.
3. **Film plane** — to be maximised; its left-hand structure (rails + uprights at X150) sits
   right where the panel/drum must move.

The prior **slide** scheme failed: sliding the panel/drum 880 mm inboard drove them into the
film-plane left rails, and the heavy drum could not be supported in camera mode without
ceiling hangers extending out past the cargo doors.

**This spec replaces the slide with a ROTATION about a vertical axle.**

---

## 2. The scheme (agreed)

Rotate the rigid panel-+-drum frame **~56° about a vertical axle**, swinging it into the
container so the cargo doors close. Decisions and rationale:

### 2.1 Pivot / axle — and why it's the key idea
- Vertical axle at the **film-plane FAR upright** (X150, Yd2262; rotation axis = the upright
  centre, **X175 / Yd2287**). The pivot **reuses that structural post** — there is no separate
  axle, which removes the earlier interference.
- The axle **carries the assembly weight** via a **floor thrust bearing** + a **top guide
  bearing** (Ø120 — wraps the 50×50 upright and clears the far wall by 15 mm). The frame
  attaches to the axle via a **hub/collar + 3 hinge brackets**.
- **Rotation and support are one mechanism.** This is the unlock: it supports the heavy drum
  in every position (camera, mid-swing, transport) — solving what the slide + ceiling hangers
  could not.

### 2.2 The swing
- **Partial swing to ~56°** — just enough to pull the protruding drum/bay inboard of the door
  plane (X0), then **LOCK** at that angle. Not 90°.
- At 56° the frame **fully clears the door plane** (true min X = +4 mm).
- It **stows toward the FAR wall**, keeping the **near-wall equipment accessible** in the
  stowed state.
- The cargo doors are **open during the swing**; they close after lock.

### 2.3 The panel — split into fixed + swinging + fixed
- The panel is cut vertically into **three** zones: a **FIXED LEFT PANEL (Yd0–180)**, the
  **SWINGING part (Yd180–2287)**, and a **FIXED FAR STRIP (Yd2287–2362)**. The swinging part
  runs exactly **cut → pivot**.
- **Fixed left panel (180 mm):** fixed to the door frame, does **not** swing — it covers the
  near-wall strip past the **NEAR film-plane upright** (Yd100–150). (150 mm clips the upright
  at 3° into the swing; 160 mm is the minimum that clears; **180 mm** chosen for margin.)
- **Swinging part:** rotates with the frame; trimmed to span **just the panel** (the vestigial
  Yd0 left-hinge hardware — piano hinges + full-width top EPDM — removed; top seal re-added
  trimmed to the panel).
- **Fixed far strip (~75 mm, Yd2287–2362):** mirror of the fixed left panel at the pivot/far-wall
  side — it ends the swinging panel **at the pivot line** so nothing swings outboard of the door
  plane (see §4-#10). Carries its own perimeter EPDM + the vertical cut seal the swinging panel
  butts against.
- **Fan B** is on the swinging part.

### 2.4 Removable film beams
- The **two LEFT film rails** (TL + BL) are **REMOVABLE** — lifted out for transport so the
  assembly can transition the gap. The film-plane **uprights/posts stay** (the far one is the
  pivot; the near one is the obstacle the split panel clears).

### 2.5 Drum support cage
- A **steel box cage** around the drum: **top + bottom rectangles** (50×50 RHS, 4 rails each)
  + **4 corner posts**, **full depth** (Z130–2250), X−890…50 × Yd700…1662.
- **Cross-members top + bottom** carry the **central drum bearings**.
- **Full depth is required** to react the overturning moment of the tall Ø900 drum — two
  axially-separated reaction points tied by the posts. (A shallow bearing-only frame would
  cantilever and wobble.)
- The cage rotates with the assembly.

### 2.6 Stepped frame (camera mode)
- The drum is **stepped forward (X−400)** of the panel in camera mode so it clears the light
  cone (shadow-free image). The step rotates with the frame.

### 2.7 Weight (rough estimate)
- Swinging assembly **≈ 330 kg** (panel ~140, cage ~90, drum ~40, bay ~25, fan ~15,
  hub/brackets ~20). Implications: a **2-person / assisted** swing, and the axle + thrust
  bearing must be sized for ~330 kg static + transit/dynamic loads.

---

## 3. Clearances verified (in the study)

| Check | Result |
|---|---|
| Door clearance at 56° | clears (true min X **+72 mm** after the panel is ended at the pivot — #10) |
| Near film-plane upright | cleared by the 180 mm fixed panel + split |
| Far film-plane upright | it **is** the pivot |
| Drum/bay through the gap | clears once the two left rails are removed |
| Swing arc vs processing tray (rim Z50) | frame underside at Z130 clears by **80 mm** |
| vs near/far walkway grates | **RESOLVED** — grates dropped to Z118 (12 mm below the Z130 frame underside); panel swept the near grate @4–25° + far @36.5–56° |
| Left walkway (in the arc) | the removable lift-out — out for transport |
| Bearings vs far wall | Ø120 clears by 15 mm |

---

## 4. Open items (punch-list — resolve before / with the cascade)

1. ~~**Lock mechanism** at the 56° transport angle.~~ **RESOLVED** — top + bottom **wall
   stays** (hook on the frame ↔ eye on the near wall, with turnbuckle), forming a couple
   that resists transit twist/rattle. The eye reacts into a **bolted plate anchor** (inside
   + outside plates, 4× M16 through the wall) — no welding to the container skin, and off
   the floor (the floor is the angled processing-tray basin). In the model.
2. ~~**Seals:** the vertical cut seal (fixed panel ↔ swinging part); the fixed-panel perimeter
   seal; the swinging panel's perimeter seal against the door frame.~~ **RESOLVED** — all three
   in the model as EPDM (lt's 40×20 convention): (a) a full-height **vertical cut bulb** at
   Yd180 the swinging panel compresses against; (b) the **fixed left-panel perimeter** (top,
   bottom, near-wall left edge); (c) the swinging panel's perimeter — trimmed **top** +
   **bottom-L** (re-added after the near-corner erase) + surviving bottom-R/right strips. All
   on the Panel-skin tag. *(Open detail: the cut-seal bulb profile + the moving panel's seat
   against the door-frame top/bottom lips when shut — refine with the latch design.)*
3. ~~**Film-plane left-rail removal** mechanism — demount, re-seat, and alignment back to the
   film-plane datum after transport.~~ **RESOLVED** — each left rail (TL/BL) drops into a
   **U-saddle** at both ends (shelf + X-side cheeks), located by a **tapered dowel** back to
   the film datum and held by a **removable clamp bar**; the rail lifts straight up for
   transport, no threading. The far-end saddle bolts to the **Ø89 pivot post**, sat clear of
   the rotating hub band. In the model (rails ghosted = struck; saddles fixed). Also ran the
   film-cage **brace beams out to the container/walkway far extent** (drawing consistency).
   *(Open detail: rail stowage
   clips + a weight/2-person handling check on the ~2.2 m rails.)*
4. ~~**Fan B** — confirm intake/duct routing still works on the swinging part.~~ **RESOLVED** —
   Fan B (Yd365, outboard of the Yd180 cut) is on the **swinging part** and is a **self-contained
   wall fan** (exterior louvre + light baffle + fan + flange all in the panel) — there is no fixed
   duct to disconnect, so the swing carries the whole intake path intact. It runs in **camera mode
   only** (panel shut at the door, drawing outside air through the open cargo doors); in transit it
   swings to **X≈1838** (deep inboard, off). Verified through the full 0→56° sweep: never overlaps
   the near upright, and clears the door plane at the locked angle. *(Note: the 2D study
   `generate_rotation_study.py` still uses the older Yd653 cut and labels Fan B on the FIXED
   section — a 2D↔3D drift to reconcile to the 3D's Yd180 cut.)*
5. ~~**Drum bearings** — top central (top-suspended) + bottom; confirm the bottom cross-member
   bearing reads as a floor-gap threshold (no trip), per the agreed "cross-members top+bottom"
   (not a perimeter guide). Size the bearings.~~ **RESOLVED** — the drum revolves about its own
   vertical axis (person access, separate from the assembly swing) on **central** bearings on the
   cage cross-members: **bottom = a Ø220 low-profile thrust/slew pad recessed into the under-drum
   gap so its top is FLUSH with the Z130 threshold sill** (a step-over door sill — verified Z108–130,
   no trip beam), plus a flush chamfered sill plate; **top = a Ø120 radial guide journal** that only
   steadies the tall drum. Sized for a light-skin drum (~50 kg) + transient lean (~100 kg) ⇒ ~1.5 kN
   axial bottom / ~0.5 kN lateral top — ample for a flat thrust race + sleeve journal. In the model.
   *(Open detail: confirm the drum build mass at the cascade; firm part numbers with the shopping list.)*
6. ~~**Axle + floor thrust bearing sizing** for ~330 kg + dynamic.~~ **RESOLVED** — **Ø89×8
   CHS** post (σ ~95 MPa, SF ~3.7 on S355 against the ~3.6 kN·m swing cantilever), floor +
   roof mount plates, a thrust collar carrying the ~330 kg, and a top + bottom radial hub
   bearing pair reacting the overturning couple. In the model.
7. ~~**Operating sequence** (deploy ↔ transport), including film-plane parking/de-rig.~~
   **RESOLVED** — full step-by-step in **§5** below; ordering conflicts surfaced and resolved.
8. ~~**Walkway-grate tangent** — a few-mm gap (drop grate locally or lift the frame).~~
   **RESOLVED** — chose **drop the grate** (keeps the panel floor-seal gap + drum threshold at
   Z130): the near + far walkway grates are set **12 mm low (top Z118)**, clearing the swinging
   frame underside (Z130). Verified the panel underside otherwise sweeps the near grate @4–25°
   and the far grate @36.5–56°. In the model. (The left walkway is lifted out anyway.)
9. **Mass reduction** if ~330 kg is too heavy (lighter panel skins / slimmer cage).
10. ~~Confirm the residual flap/poke-out is fully resolved by the pivot-at-upright-centre move.~~
    **RESOLVED (properly, not by tolerance).** The pivot-at-upright move alone left only **+5.4 mm**
    — the compressible EPDM lip skating the door plane, not a real clearance. Fixed at the root:
    **end the swinging panel at the pivot line (Yd2287)** and cover the residual ~75 mm with a
    **FIXED FAR STRIP (Yd2287–2362)**, mirror of the fixed left panel (§2.3). Now **no** swing
    panel/EPDM geometry extends past the pivot (verified), and the true min X at 56° is **+72 mm**.
11. **POST-MERGE / deferred:** the **lower film-plane brace beam sits at the same Z level as the
    walkway grate** (lower rail/beam at Z≈100–150 vs walkway grate Z≈115–130) — a physical
    clash. Flagged for resolution **after the merge** (drop the beam, step the walkway locally,
    or re-level one of them); not blocking the rotation study.

---

## 5. Operating sequence (deploy ↔ transport)

The sequence is driven by one hard rule: **the swing path through the X150 rail plane must be
clear before the frame rotates** — so the removable rails and the left walkway come out first,
and the wall stays go on last (they only reach at 56°).

### 5.1 Camera → Transport (stow)
1. **End camera use.** Power off **Fan B**; finish any darkroom access.
2. **Park the drum.** Rotate the revolving drum to its closed/aligned position and **pin its
   rotation** (detent) so it can't flop during the move.
3. **Lift out the removable LEFT walkway** — it sits inside the swing arc.
4. **Strike the two left film rails (TL + BL).** Release each clamp bar, lift the rail straight
   up out of its saddles, and **stow** (clipped to the near wall). *Required before the swing —
   otherwise the drum cage fouls the X150 rail plane.*
5. **Unlatch the swinging panel** from the door frame (Southco cam latches) — releases the
   perimeter + cut seals.
6. **Swing the frame ~56° inboard** (toward the far wall), assisted (~330 kg). The vertical
   pivot gives **no gravity torque** (the assembly is balanced at any angle) — effort is only
   overcoming inertia + bearing friction and **controlling momentum** at the stops.
7. **Engage the transport lock** — connect the **top + bottom wall stays** (hook the rods from
   the frame hooks to the near-wall eyes, tension the turnbuckles).
8. **Close + secure the cargo doors.** They close **outboard of the fixed left panel** (Yd0–180,
   which stays at the door plane); the swung frame clears the door plane (true min X +4 mm).

### 5.2 Transport → Camera (deploy) — the reverse
1. **Open the cargo doors.**
2. **Release the wall stays** (slack the turnbuckles, unhook top + bottom).
3. **Swing the frame back** to the door plane (camera position).
4. **Latch the panel** to the door frame (Southco cam latches) — compress the perimeter + cut
   seals.
5. **Re-fit the two left film rails** — drop TL + BL into their saddles; the **tapered dowels set
   the film datum**; clamp down.
6. **Re-fit the left walkway.**
7. **Verify film-plane alignment** — confirm the re-seated rails return the plane square/planar to
   datum before shooting.
8. **Un-pin the drum** (ready for access); **power up Fan B.**

### 5.3 Ordering conflicts surfaced (and how they're resolved)
- **Rails vs swing:** rails must be **out before** any swing and **back in after** the swing-back
  (the cage sweeps the X150 plane). Sequenced at 5.1-4 / 5.2-5.
- **Left walkway vs swing arc:** out before the swing (5.1-3), back after (5.2-6).
- **Stays only reach at 56°:** engage **after** the swing, release **before** the swing-back
  (5.1-7 / 5.2-2).
- **Panel latches:** release before the swing, re-engage after the swing-back (so the seals aren't
  dragged) (5.1-5 / 5.2-4).
- **Drum flop:** pinned before the move, un-pinned on deploy (5.1-2 / 5.2-8).
- **Near-wall congestion:** rail + walkway **stowage must not clash with the stay anchors** (both
  live on the near wall) — allocate separate stow positions. *(Open detail for the cascade.)*
- **Alignment recovery:** the removable rails return to datum via the dowels, but a **post-deploy
  film-plane alignment check** is mandatory before use (5.2-7).

---

## 6. Cascade impact (when we proceed)

This replaces the slide in the production model + docs — a significant change:

- **`tbs_constants.py`** — add: pivot location, swing angle (56°), panel cut (180), removable
  left rails, drum cage, drum bearings. Retire the slide constants (`PANEL_SLIDE`, the
  carriage rails / Destaco locks).
- **`lighttrap.skp`** — rebuild around the rotation (replace the DC slide with the swing DC).
- **2D diagrams** — the hinged-panel sheets: redraw for the rotation.
- **Reports** — `hinged-panel-report.md` (transport mechanism), `light-trap-selection.md`.
- **`master-shopping-list.md` + `project-cost-breakdown.md`** — axle/thrust bearing, top guide
  bearing, drum cage steel, removable-rail hardware, lock; retire the slide carriage/rails.
- **`component-dependency-map.md`** — update the matrix.

---

## 7. Study artifacts (reference)

- **2D plan:** `src/generators/generate_rotation_study.py` → `diagrams/rotation-study.png`
- **3D model:** `src/models/generate_rotation_model.py` → `models/rotation-study.skp`
  (scenes: Camera / Transport (swung 56°) / Structure (no panel skins))
- **Faithful lighttrap baseline:** `src/models/generate_transport_study_model.py` →
  `models/transport-study.skp`
- **Slide exploration (superseded):** git tag `transport-study-explore`
