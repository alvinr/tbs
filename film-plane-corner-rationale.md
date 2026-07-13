<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Why the Film-Plane Corners Work the Way They Do

**Branch:** `film-plane-redesign`. This is the design-rationale report for the film-plane corner
mechanism — *why* each corner is built the way it is. Every choice traces to a specific engineering
fact; the sources are collected in [`film-plane-joint-research.md`](film-plane-joint-research.md), and
the resulting corner is drawn in `diagrams/film-corner-gimbal.png`.

---

## The job of a corner

The film plane is a **fixed-size rigid flat rectangle** (4,499 × 2,388 mm). To act as a view-camera
back it must **tilt** and **swing** — and also **focus** (move in depth) — while staying perfectly
**flat**. It is supported at its **four corners**, each riding a moving carriage (a floating X slide + a
driven vertical Z leadscrew, on a depth-Y leadscrew). The corner joint is the piece that connects the
rigid frame to each moving carriage.
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

## 3. Why the horizontal slide FLOATS — and the vertical is DRIVEN

- When a rigid plane rotates, **each corner sweeps an in-plane arc.** That arc has a **horizontal (X)**
  and a **vertical (Z)** component; both must be accommodated at the corner.
- The **horizontal (X) component free-floats** — a low-friction slide absorbs it. In exact-constraint
  language it is the **"added freedom" that removes the redundant constraint**, making four corners
  **legal** instead of over-constrained (research doc §2). Gravity is neutral to a horizontal slide, so
  it can float freely.
- The **vertical (Z) component cannot free-float.** It is gravity-loaded — the top corners *hang* in
  tension, the bottom corners *bear* in compression — and a frictionless vertical slide provides **no
  vertical reaction**, so the panel would simply drop. So **Z is a driven, self-locking leadscrew** at
  each corner; its redundancy is then **managed by coordination** (rule 4), not removed by compliance. At
  full ±40° tilt this vertical travel is large (~280 mm/corner), which is exactly why it is driven rather
  than sprung or free.

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
  45°** ([Ruland US12-6-6-SS](https://www.ruland.com/us12-6-6-ss.html) — 303 SS, self-lubricating
  sintered-bronze plain bearing, grease-free), which covers our ±40° tilt / ±28° swing at trivial load.
  Because this is *static articulation*, not continuous high-speed rotation, the joint is usable to its
  full angle. **So the 2-axis, twist-locked joint is an off-the-shelf single U-joint — no custom gimbal
  fabrication.** It is exactly the two-crossed-pins, torsion-locked kinematics above, but factory-aligned
  (low lash), shorter than a fabricated gimbal (recovering film-plane height), in stock, and ~$195/corner.
  (Research doc §3–4.)

## 5. Why a self-lubricating plain-bearing joint (not needle/ball)

- The corner runs inside the **ferricyanide / citric-acid wash** environment. **Rolling and needle
  bearings corrode and seize** there, and greased joints wash out.
- So we pick the U-joint with a **self-lubricating sintered-bronze plain bearing** — it runs
  **dry/grease-free** and carries load through its own material, the same corrosion-safe, wash-down choice
  igus/SKF sell (and telescope makers use — Dobsonian PTFE pads). **303 stainless** suits the splash/rinse
  exposure here; step to a **316** joint only if it is soaked rather than rinsed. (Research doc §6.)

## 6. Why four corners at all — and not a single central gimbal

- A central 2-axis gimbal (the classic view-camera rear standard) would tilt and swing beautifully, but
  it does **only** tilt and swing. The **four corners + four depth leadscrews** are what also give
  **focus, rise, shift, and back-focus** — the full set of view-camera movements.
- So we **keep the four-corner architecture** and make it correct: **floating cross-slides** (§3) remove
  the over-constraint, and a **2-axis gimbal** (§4) at each corner provides the tilt/swing articulation
  without twist. (Research doc §7, options A–C — this is option A.)

---

## The result — one corner (Design A)

Per corner (×4, driven in coordinated pairs on the depth leadscrews):

- **1 × single universal joint** — [Ruland US12-6-6-SS](https://www.ruland.com/us12-6-6-ss.html): 303
  stainless, self-lubricating **sintered-bronze plain bearing**, **45° max articulation**, 3/8" bore,
  68 mm long, grease-free — the off-the-shelf 2-axis torsion-locked pivot (~$195, in stock)
- **2 × stub-shaft mount** — a short 3/8" stub + clamp/plate at each yoke: one to the floating X slide,
  one to the film-frame corner (drilled plate, not a precision-reamed gimbal)
- …all sitting on the **floating X slide**, the **driven vertical (Z) leadscrew**, and the **depth (Y)
  leadscrew**.

The off-the-shelf single U-joint (~$1,200 for four) **replaces the earlier custom gimbal** (ring + two
yokes + four reamed bores per corner) — cheaper, shorter, factory-aligned, and in stock. Drawn in
`diagrams/film-corner-gimbal.png`.

## Design rules adopted (all grounded in the research)

1. **Articulate on determinate freedoms; float the redundant horizontal DOF** — the X slide absorbs the
   horizontal arc travel, so four corners aren't over-constrained on that axis; the gravity-loaded vertical
   is driven, not floated.
2. **2-axis, torsion-locked joint** — an off-the-shelf single stainless U-joint (Ruland US12-6-6-SS, 45°)
   gives tilt + swing, enforces "no twist," clears our ±40°/±28° at trivial load, and needs no custom fab.
3. **Self-lubricating plain-bearing joint, grease-free** — the U-joint's sintered-bronze plain bearing
   (no needle/ball rollers to corrode or wash out); 303 SS suits splash/rinse exposure (316 if soaked).
4. **Coordinate the driven pairs** so the four corners' depth *and* vertical drives never command
   conflicting positions (a control/coordination rule, not a joint fix).

*This rationale will fold into `film-plane-mechanism-report.md` when the redesign lands; for now it lives
on the `film-plane-redesign` branch alongside the research.*
