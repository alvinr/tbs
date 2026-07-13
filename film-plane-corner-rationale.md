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
**flat**. It is supported at its **four corners**, each riding a moving carriage (an X–Z cross-slide on
a depth leadscrew). The corner joint is the piece that connects the rigid frame to each moving carriage.
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

## 3. Why the cross-slides FLOAT

- When a rigid plane rotates, **each corner sweeps a small in-plane arc.** The **floating X–Z
  cross-slide** at each corner absorbs that arc travel.
- In exact-constraint language, the floating slide is the **"added freedom" that removes the redundant
  constraint** — it is precisely what makes four corners **legal** instead of over-constrained. So the
  cross-slides were the right idea all along; the over-constraint theory *validates* them (research doc §2).

## 4. Why the joint is a 2-axis gimbal — not a ball joint, not a rod-end

- The motion needs **two axes + no twist ⇒ a universal joint** (§1). A **ball joint** also spans both
  axes but adds a **third, redundant twist freedom** we don't want.
- More decisively: **plain ball/spherical bearings and rod ends only articulate ±16–22°** — they
  **physically cannot reach ±45°** (Machinery's Handbook; SKF & Aurora catalogs). That fact is why the
  entire rod-end path (Ø25 bore, 2458K435, 60645K591…) was a dead end, and it is now retired for cause.
- A **standard Cardan cross** binds around **±37°** (the yokes collide). So we build the universal joint
  as a **gimbal** — **two perpendicular pins on an intermediate block, offset so their bores clear** —
  where **each pin independently reaches ±45°+**, and each is in **double shear**. (Research doc §3–4.)

## 5. Why acetal/PTFE bushings on stainless pins

- The corner runs inside the **ferricyanide / citric-acid wash** environment. **Rolling and needle
  bearings corrode and seize** there.
- **Self-lubricating plain bushings** (acetal / PTFE-lined, e.g. igus iglidur) on **316 stainless pins**
  run **dry, don't corrode, and carry load through their own material** — the same corrosion-safe,
  grease-free bearing choice telescope makers use (Dobsonian PTFE pads) and that igus/SKF sell for
  wash-down service. (Research doc §6.)

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

- **1 × gimbal block** — 316 SS or 6061, ~50 × 70 × 44 mm, two **offset** perpendicular Ø30 bores
- **2 × Ø24 shoulder bolt** — 70 mm shoulder, M20 (McMaster 90269A925) — the two gimbal pins
- **4 × acetal/PTFE flanged bushing** — Ø24 bore × Ø30 OD (igus iglidur), self-lubricating
- **1 × cross-slide yoke + 1 × frame yoke** — 6061, two lugs each, mounted 90° apart
- **2 × M20 nyloc nut** — 316 SS
- …all sitting on the **floating X–Z cross-slide** and its **depth leadscrew**.

Drawn (dimensioned, with ±45° articulation checks) in `diagrams/film-corner-gimbal.png`.

## Design rules adopted (all grounded in the research)

1. **Articulate on determinate freedoms; float the redundant DOF** — the cross-slides absorb the arc
   travel, so four corners aren't over-constrained.
2. **2-axis, torsion-locked joint (gimbal)** — gives tilt + swing, enforces "no twist," clears ±45°.
3. **Double shear on every pin;** self-lubricating plain bushings; **316 SS / acetal** throughout for
   the wet environment.
4. **Coordinate the driven pairs** so the four corner depths never command conflicting positions (a
   control/coordination rule, not a joint fix).

*This rationale will fold into `film-plane-mechanism-report.md` when the redesign lands; for now it lives
on the `film-plane-redesign` branch alongside the research.*
