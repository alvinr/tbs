<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Why the Film-Plane Corners Work the Way They Do

**Branch:** `film-plane-redesign`. This is the design-rationale report for the film-plane corner
mechanism — *why* each corner is built the way it is. Every choice traces to a specific engineering
fact; the sources are collected in [`film-plane-joint-research.md`](film-plane-joint-research.md), and
the resulting corner is drawn in `diagrams/film-corner-gimbal.png`.

---

## The job of a corner

The film plane is a **fixed-size rigid flat rectangle** (4,389 × 2,094 mm). To act as a view-camera
back it must **tilt** and **swing** — and also **focus** (move in depth) — while staying perfectly
**flat**. It is supported at its **four corners**, each riding a **push-to-slide, cam-clamp** stage
(friction slides in depth-Y and vertical-Z, plus a floating X slide). The corner joint is the piece that
connects the rigid frame to each moving carriage.
Getting it right was hard until we grounded it; here is the reasoning, in order.

---

## 1. Tilt and swing are TWO rotations — and never a twist

- **Tilt** = the plane rotates about a **horizontal** axis. **Swing** = about a **vertical** axis.
  Combined, the plane's normal can point anywhere in a shallow cone.
- Crucially, the plane **never rotates about its own normal (no "twist")** and **never warps** — it is
  a rigid, flat panel.
- **⇒ Each corner joint must allow exactly two rotational axes and lock the third (twist).** That is the
  textbook definition of a **universal (Cardan) joint** — two axes, torsionally rigid.

## 2. Why we do NOT bolt the corners rigidly — the over-constraint trap

- A free rigid body has **6 degrees of freedom** and needs **exactly 6 constraints** to be located —
  no more. **Four rigidly-located corners over-constrain it** (statically indeterminate): it can't
  decide which corners bear load, so it **rocks, racks, and warps** from the tiniest manufacturing or
  thermal mismatch. This is literally the wobbly-four-legged-table.
- **This is the real reason the earlier rigid/rod-end corner joints kept "fighting"** — no joint can fix
  an over-constrained architecture. (Maxwell's kinematic principle; Blanding, *Exact Constraint*; Hale,
  MIT/LLNL thesis — see the research doc §1.)

## 3. Why the corners SLIDE-AND-CLAMP — not driven screws

- **A pinhole has effectively infinite depth of field**, so positioning the plane is **scene /
  perspective control** (tilt, swing, rise, where the plane sits) — **not precise, repeatable focus.**
  Nothing here needs a leadscrew's micron-hold, so we don't pay for one: each corner is a **friction
  slide you push into position and lock with a cam clamp.**
- **Depth (Y) produces both tilt and swing.** Moving corners in depth is what articulates the plane: a
  top↔bottom depth difference gives **tilt**, a left↔right depth difference gives **swing** (all four
  together give focus / where the plane sits). This is the long ~2.2 m slide.
- **When the plane tilts or swings, each corner foreshortens** — it must shift toward the panel center
  *in the plane* (the rigid panel can't stretch). **Two matched accommodation slides** absorb that shift:
  the **vertical (Z) slide absorbs the TILT foreshortening**, the **horizontal (X) slide absorbs the
  SWING foreshortening**. They are a pair — Z ↔ tilt, X ↔ swing.
- **They differ only in gravity.** The **X (swing)** slide is horizontal → gravity-neutral → it **floats
  freely** as you set up (in exact-constraint terms, the "added freedom" that keeps four corners from
  over-constraining, research doc §2). The **Z (tilt)** slide is vertical → gravity-loaded (top corners
  *hang* in tension, bottom *bear* in compression) → it uses an **adjustable-friction slide** (igus
  DryLin-style) that **stays where you leave it**. Both take a **cam clamp** that locks them for the shot
  and for transport.
- **This is kinematically cleaner than driven screws.** You position every corner while everything is
  free (compliant), then **clamp at the plane's *natural* pose** — you lock where it already sits, so
  four rigid clamps never *force* the panel into a fight (no over-constraint). Driving four screws would
  have to be coordinated to avoid exactly that; slide-and-clamp sidesteps it.
- **Bonus:** this drops the entire drive train — **8 Acme leadscrews, 8 handwheels, 4 bevel gearboxes,
  extension shafts, nuts, collars** — and dissolves the ±40°/±28° cost (the big angles now just mean
  *longer plain slides*, which are trivial to push, instead of ~470-turn, whippy 2.4 m screws).

## 4. Why the joint is a 2-axis gimbal — not a ball joint, not a rod-end

- The motion needs **two axes + no twist ⇒ a universal joint** (§1). A **ball joint** also spans both
  axes but adds a **third, redundant twist freedom** we don't want.
- More decisively: **plain ball/spherical bearings and rod ends only articulate ±16–22°** — they
  **physically cannot reach ±45°** (Machinery's Handbook; SKF & Aurora catalogs). That fact is why the
  entire rod-end path (Ø25 bore, 2458K435, 60645K591…) was a dead end, and it is now retired for cause.
- **Even a large-swivel ball joint does not rescue the approach — and this is the decisive reason, not the
  angle.** A stud-type ball joint rated to **50° swivel** ([McMaster 60745K611](https://www.mcmaster.com/60745K611/))
  clears ±45° on angle, so the articulation objection is gone. But it is a **3-DOF spherical joint** (cone
  swivel + free spin about the stud), so it **cannot lock twist** (§1). Chaining **two** at 90° *adds*
  freedom rather than removing it: the frame-to-carrier twist stays free, and the link between them gains
  a redundant spin (the classic spherical–spherical strut) — four such corners let the flat panel **rack
  and rotate in plane**, the exact failure the joint exists to prevent. Ball joints also carry **lash** (a
  linkage part, not a precision locator) and react **no moment** at a point contact. **The gimbal's two
  joints are pins — pure 1-DOF hinges, torsionally rigid — so two crossed pins give exactly tilt + swing
  with twist locked and zero lash. That torsional rigidity is the one property a ball structurally cannot
  provide, and it is exactly the requirement.**
- We first assumed a Cardan cross binds too early (~±37°) and would need a **custom offset-pin gimbal**
  (two perpendicular pins on a block, offset so their bores clear, each in double shear). **Grounded
  catalog research corrected that:** relieved-yoke **single stainless universal joints are published to
  45°** ([Belden SSNBUJ750x3/8KB](https://www.grainger.com/product/BELDEN-Universal-Joint-Stainless-41D816) — stainless, needle-bearing
  (friction) bearing, grease-free), which covers our ±40° tilt / ±28° swing at trivial load.
  Because this is *static articulation*, not continuous high-speed rotation, the joint is usable to its
  full angle. **So the 2-axis, twist-locked joint is an off-the-shelf single U-joint — no custom gimbal
  fabrication.** It is exactly the two-crossed-pins, torsion-locked kinematics above, but factory-aligned
  (low lash), shorter than a fabricated gimbal (recovering film-plane height), in stock, and ~$113/corner.
  (Research doc §3–4.)

## 5. Why a plain needle bearing joint (not needle/ball)

- The corner runs inside the **ferricyanide / citric-acid wash** environment. **Rolling and needle
  bearings corrode and seize** there, and greased joints wash out.
- So we pick a **stainless needle bearing plain (friction) bearing** — pins riding in blocks, no rollers.
  It runs **dry/grease-free**, and because the corner is a **static, near-zero-cycle positioning joint**
  (set the angle, clamp, expose), bearing wear and lubrication are non-issues; the corrosion-safe choice is
  the material, not a grease film. **stainless stainless** suits the splash/rinse exposure here; step to a
  more resistant joint only if it is soaked rather than rinsed. (Research doc §6.)
- **The joint is factory-booted** (the SSNBUJ750x3/8KB ships with an integral bellows over its needle bearings,
  OD 1-9/32"/32.54mm × OL 1-1/4"/31.75mm — no separate boot part) — it keeps the ferricyanide/citric wash
  and debris out of the needle bearings. Nitrile resists water/alcohol well. We fit it **DRY** (a contaminant
  barrier only), **not** grease-packed, consistent with the grease-free bearing. The **DryLin slides**
  likewise need no seals — dry-running polymer is unaffected by the wash.

## 6. Why four corners at all — and not a single central gimbal

- A central 2-axis gimbal (the classic view-camera rear standard) would tilt and swing beautifully, but
  it does **only** tilt and swing. The **four independently positioned corners** are what also give
  **rise, shift, and where-the-plane-sits** — the full set of view-camera movements.
- So we **keep the four-corner architecture** and make it correct: **slide-and-clamp corners with a
  floating X** (§3) remove the over-constraint, and a **2-axis U-joint** (§4) at each corner provides the
  tilt/swing articulation without twist. (Research doc §7, options A–C — this is option A.)

---

## The result — one corner (Design A)

Per corner (×4):

- **1 × single universal joint** — [Belden SSNBUJ750x3/8KB](https://www.grainger.com/product/BELDEN-Universal-Joint-Stainless-41D816): stainless
  stainless **needle bearing plain (friction) bearing**, **45° max articulation**, 3/8" bore,
  68 mm long, grease-free — the off-the-shelf 2-axis torsion-locked pivot (~$113, in stock)
- **2 × base-mount shaft support** — [McMaster 4040N12](https://www.mcmaster.com/4040N12/), 304 SS,
  clamps a 3/8" stub (removable cap + two 6-32 screws): one to the floating X slide, one to the
  film-frame corner (off-the-shelf clamp, not a precision-reamed gimbal)
- **2 × stub shaft** — 3/8" (9.5 mm) 304 SS rod, ~60 mm each: one end into the U-joint hub (set-screw
  locked), the other clamped in the shaft support
- **Integral boot** — the SSNBUJ750x3/8KB is factory-booted (bellows over the needle bearings; no separate part):
  integral bellows sealing the needle bearings from the wash
- **Depth (Y): friction slide (~2.2 m) + cam clamp** — produces tilt + swing (+ focus); push, then lock
- **Vertical (Z): friction slide + cam clamp** — absorbs the **tilt** foreshortening; holds when released, then locks
- **Horizontal (X): float/friction slide + cam clamp** — absorbs the **swing** foreshortening; floats free during setup, then locks

The off-the-shelf single U-joint (~$451 for four) **replaces the earlier custom gimbal** (ring + two
yokes + four reamed bores per corner), and **slide-and-clamp replaces the whole leadscrew/handwheel drive
train** — cheaper, simpler, factory-aligned, and in stock. Drawn in `diagrams/film-corner-gimbal.png`.

## Design rules adopted (all grounded in the research)

1. **Articulate on determinate freedoms; float the redundant horizontal DOF** — the X slide absorbs the
   horizontal arc travel, so four corners aren't over-constrained on that axis; the gravity-loaded vertical
   is held by a friction slide + clamp, not a screw.
2. **2-axis, torsion-locked joint** — an off-the-shelf single stainless U-joint (Belden SSNBUJ750x3/8KB, 45°)
   gives tilt + swing, enforces "no twist," clears our ±40°/±28° at trivial load, and needs no custom fab.
3. **Plain needle bearing joint, grease-free** — stainless pins-in-blocks, no needle/ball rollers to
   corrode or wash out; a static low-cycle joint so it needs no lubrication; stainless suits splash/rinse.
4. **Position free, then clamp at the natural pose** — set every corner while the slides are free, then
   lock the cam clamps where the rigid plane already sits, so four clamps never force it (no
   over-constraint, no drive coordination to get wrong). A pinhole's infinite DoF is what lets us do this
   — it's scene control, not focus.

*This rationale will fold into `film-plane-mechanism-report.md` when the redesign lands; for now it lives
on the `film-plane-redesign` branch alongside the research.*
