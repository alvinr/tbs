<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
---
name: fastener-convention
description: How to draw a structural through-bolt/screw correctly in the 3D models — the ruby_bolt axis/head/nut sign convention, the edge-distance/grip/orientation rules that kept slipping to review, and the check_interference.py --bolts lint that catches them
metadata:
  type: reference
---

## Purpose

Bolts are the single biggest source of *rework* in this project. A bolt is easy
to place with the right coordinates and still be **physically wrong** — pointed
along the wrong axis, driven through the wrong *face*, too near an edge, the
wrong length, or floating in air. None of that shows in the numbers; it only
surfaces when someone eyeballs a render. This session's log is full of it: *"J2
cleat → single horizontal bolt (fixes edge distance)"*, *"bolts now clamp the
assembly (were projecting past the plates)"*, *"tee-nut on the correct (back)
face"*, *"Detail B bolts flush"*.

Read this before adding or moving any fastener in `src/models/`. The companion
automated check is **`check_interference.py --bolts`** (below) — run it before
handing a model off.

Coordinate system is the shared one (X along the container, **Yd** across, Z up)
— see `skills/skill_diagram_structure.md`.

---

## The `ruby_bolt` sign convention (memorize this)

```python
ruby_bolt(name, x, y, z, length, radius=6.0, axis="z", color=None,
          head="base", nut="far", mute=None)
```

- The **shank** is an Ø(2·radius) cylinder starting at `(x, y, z)` and running
  **+`axis`** for `length`. So the START point is the `axis`-**minimum** end, and
  the shank grows in the **positive** axis direction. To run a bolt in −X you
  still give the low-X point as `(x,y,z)` and it extends +X — there is no negative
  length; pick the base point accordingly.
- **`head` / `nut`** name which *end* each sits on:
  - `"base"` = the `(x,y,z)` end (the axis-minimum end).
  - `"far"`  = the `(x,y,z)+length` end (the axis-maximum end).
  - `None`   = omit it (a floor anchor has `nut=None`; a self-drilling TEK screw
    has `nut=None`).
- Head/nut are hex prisms that protrude **just proud** of the shank end, against
  the clamped face. So `head="base"` puts the hex head at the low-axis end — the
  head is on the side you approach from.
- **Radius is the DRAWN shank**, ~half the nominal + a hair (M12 → radius 6). The
  `--bolts` lint reads D from this AABB, so it is slightly conservative vs the
  nominal thread.

**Worked example — the J6 moment bolt** (through end-plate → upright → backing
plate, hex head on the walkway side, nut on the box-interior side):

```python
bx0  = RWK_X_UP - ep_t                 # low-X face = the end-plate front
blen = IBC_FRAME_RHS + 2*ep_t + 8      # spans the whole stack + nut protrusion
ruby_bolt("RWk J6 bolt M12", bx0, ac_y, bz, blen, radius=6, axis="x",
          head="base", nut="far")      # head at bx0 (front), nut at the far (interior) end
```

---

## The rules that keep biting (check every one)

1. **Edge distance ≥ 1.5·D, in the member that MATTERS.** Center-to-edge, in the
   structural member the bolt grips. This is the J2/J7 flaw: the retaining bar is
   a `50×20` RHS; a vertical bolt through the **20 mm** face gives a Ø14 hole
   ~3 mm of edge. The fix was to run the bolt **horizontally through the tall
   50 mm web** → ~18 mm edge. **When a hollow section is bolted, drive the bolt
   through the WIDE face/web, not the narrow one.**

2. **Grip the whole stack.** `length` must span every member from the head face
   to just past the nut. A bolt that stops inside the stack does not clamp; a bolt
   that runs far past the last plate is the *"projecting past the plates"* defect.
   Compute the length from the members' thicknesses (+ ~1·D for the nut), don't
   eyeball it.

3. **Head and nut on ACCESSIBLE faces.** A nut you can't get a wrench on is
   unbuildable. Through-bolts into the thin corrugated container wall put the
   **hex head OUTSIDE** and the nut inside; check there is wrench clearance on the
   nut side (the J6 bolts sit *above the arm* so both can be tightened).

4. **The bolt must PIERCE a structural member** — not float in air, not only
   catch a thin notched-beam remnant. If it grips nothing, it's mis-placed.

5. **Orient the axis to the joint, not to habit.** A cleat that resists a −X
   thrust wants the bolt in shear across that thrust; a wall hanger wants the bolt
   normal to the wall (Yd). State the axis from the load path.

6. **Back a wall/thin-skin bolt with a spreader plate.** The corrugated wall pulls
   through under load — every wall through-bolt gets an exterior backing plate
   (load spread, hex heads outside).

---

## The automated check — `check_interference.py --bolts`

Run it against the live model (it queries whatever's open — use **overview**, it
carries every structural member) before any hand-off:

```bash
python3 src/models/check_interference.py --bolts
```

Read-only, advisory. For every structural grip bolt it finds the members its
centerline pierces and flags:

- **EDGE** — center-to-edge < 1.5·D in the gripped member (the J2/J7 class).
- **FLOATING** — the bolt pierces no structural member (mis-placed).
- **PROJECT** — the shank runs > 25 mm past the outermost member it grips.

Scope + caveats (so you read the output correctly):

- Scoped to **structural steel** through-bolts. The film-plane precision
  mechanism (skate axles, cam-brakes, clamp/ball-joint) and liquid vessels are
  filtered out (`_MECH_KEYS`, slenderness gate) — those carry precision-fit rules,
  not 1.5·D-in-steel.
- **Drawn-D, so slightly conservative** (M12 draws as D12–14 → wants 18–21 mm; the
  nominal M12 rule is 18 mm). A flag within a few mm of the bar may be nominal-OK.
- It's a **TRIAGE list**: when a bolt pierces several members the *worst-edge* one
  is named, which may be an incidental notched-beam remnant rather than the primary
  plate. A human confirms — a flag is a "look here," not a verdict.

---

## Where this is heading (don't hand-place if you can emit)

The durable fix for orientation rework is a **`bolted_joint()` emitter**: give it
the two members + the mating face and it emits the plate(s), the bolt (auto-normal
to the face), nut, and backing plate *together*, with the grip length **computed**
from the real stack and the edge distance **asserted**. Orientation becomes
correct-by-construction instead of re-derived (and re-broken) at each joint. Until
that exists, follow the rules above and run `--bolts`. (Tracked in `TODO.md`.)
