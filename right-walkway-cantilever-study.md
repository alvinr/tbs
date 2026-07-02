<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Right Walkway — Cantilever Support Study

**Status:** ADOPTED (rev12) — **decision record**. The right walkway is now the wall-/IBC-cantilevered design; the ceiling-hung scheme it replaced is retired. The as-built version (refined into a closed cantilever rectangle) is in [Walkway Report §4](walkway-report.md); this page records *why* the change was made and the first-order load check behind it.

## 1. Why

The right walkway (IBC-end access, X4329–4629, spanning the full width Yd 0–2362) was originally **ceiling-hung** — five M10 rod-pairs from the deck up to the roof. The film-plane rework (wall-seat saddles, rails now running the full width to X4649) exposed a conflict: **those vertical rods sit in the film plane's X-footprint (X4329–4629 ⊂ X150–4649) and in the volume the tilting plane sweeps** — the plane's right corner reaches Yd1760 at 28° tilt and Yd1575 at 40°, colliding with the hangers at Yd1828/1371 — plus the rods sit in the optical band (shadow risk). See [Film Plane Report](film-plane-mechanism-report.md) and the corner analysis.

**Key insight:** the **deck itself was never the problem** — it sits at Z130, tucked *under* the film-frame bottom (Z150). Only the **vertical rods** intrude. Remove the rods and the film-plane conflict disappears, **with no reduction in film size and the same swing range on both sides**.

## 2. The clearance that makes this possible now

The earlier design went ceiling-hung because there was thought to be no room for floor/wall support. That changed:

| Element | Z | Note |
|---|---|---|
| Tray rim | 50 | |
| **Spray-bar gantry (top)** | **~54–85** | Ø32 wheels + 40×25 SS beam, rides the raised/sloped floor — *low* |
| **Clear band under the grate** | **~30mm (worst, far-left)** | see [Walkway Routing Sections §H-H](walkway-routing-sections.md) |
| Walkway grate | 115–130 | |
| Film-frame bottom rail | 150 | deck clears it by 20mm |

Plus a **45mm gap (X4629–4674)** between the tray's right edge and the IBC frame face. So there's now both vertical and horizontal room the old layout lacked.

## 3. The design — hybrid anchor (IBC frame + side walls)

*As-built (rev12): refined into a closed cantilever rectangle — see [Walkway Report §4](walkway-report.md). The support strategy below is what was built: cantilever off the IBC frame + wall anchors, no ceiling rods.*

The IBC stacking frame only has uprights at the **corridor (Yd 1046 / 1266, at X4654)** — there is **nothing at the perimeter (Yd0 / 2362)** to bolt to. So the support is split:

- **2 inner cantilever arms** — off the **IBC corridor uprights** (X4654, deep-box front upright). A U-clamp grips each upright with 2× M12; the arm (40×45 SHS) reaches ~405mm back to the deck's left edge (X4329).
- **2 outer wall-mounted ledgers** — on the **near (Yd0) and far (Yd2362) container walls**, each **through-bolted** (interior + exterior plate, 2 bolts) at 2 X stations along the deck width. These carry the deck's ends, where the frame can't reach.
- **2 longitudinal bearers** (Yd-running, at X4329 + X4629) ride the arms + ledgers; the grate spans the ≤1,046mm between supports.
- All members sit at **Z70–115** — ~10mm above the spray-bar top at the (low-side) cantilever stations, below the film frame (Z150). **No ceiling rods. Nothing into the tray. Nothing in the optical band above the deck.**

3D study model: `src/models/generate_right_cantilever_study.py` (scenes: Combined / **Anchors (frame + walls)** / Clearance / Labeled — the Anchors scene shows both the upright U-clamps and the wall ledgers).

## 4. Load check (first-order — favorable)

| Quantity | Value | Notes |
|---|---|---|
| Deck self-weight | ~0.45 kN | right walkway ≈ 46 kg ([Weight Dist. §3.2](weight-distribution-report.md)) |
| Live load (one person) | 1.0 kN | ~100 kg |
| Worst cantilever arm | 345mm | person at the far deck edge, over one arm |
| **Worst single-arm moment** | **~0.35 kN·m** | 1.0 kN × 0.345 m (conservative; normally shared 2 arms) |
| Arm bending stress (40×40×3 SHS, Z≈4.0 cm³) | ~86 MPa | vs 250 MPa yield → **SF ≈ 3** (upsize to 50×50 for SF≈5) |
| Added stress on IBC upright (50×50×3, Z≈7.9 cm³) | ~44 MPa | small vs the frame's stack duty |
| Anchor bolt force (2 bolts @ ~100mm) | ~3.5 kN/bolt | vs ~15–20 kN M12 capacity → **SF ≈ 5** |

The IBC frame already carries the 2×2 IBC stack and is anchored to floor + walls; the added ~0.35 kN·m cantilever is minor. **Recommend a structural sign-off on the gusset connection**, but first-order it's comfortable.

## 5. What it resolves / what stays separate

**Resolved:** the film-plane ↔ walkway conflict (no rods in the sweep or optical band); film plane keeps **full width (X150–4649)** and the **same tilt/swing range on both sides**; ceiling de-cluttered on the right.

**Resolved as follow-ups (rev12):** the **chem prep shelf** was moved left of the tap (X3129–3729 / Yd300–600) to clear the film-plane swing envelope, and the **sump pickup + tray-drain plumbing** return riser was rerouted into the grate gap with a Yd twist to clear the new right-walkway beam.

## 6. Comparison

| | Ceiling-hung (former) | **Cantilever off IBC frame (adopted, rev12)** |
|---|---|---|
| Rods in film-plane sweep / optics | **yes** (the conflict) | **none** |
| Forces film-size reduction? | (else yes) | **no** — full width, symmetric swing |
| Tray / spray-bar intrusion | none | none (arms at Z70–115, above the gantry) |
| Adds load to | roof ribs | IBC frame (2 inner arms) + near/far walls (2 ledgers); minor — needs connection sign-off |
| Cost | 5 rod-pairs + 10 roof plates | 2 arms + 2 wall ledgers + clamps/bolts (≈ neutral) |

## 7. Implementation (rev12 — complete)

Adopted and built per [Walkway Report §4](walkway-report.md): the cantilever rectangle replaced the ceiling hangers in the walkway + overview 3D models, the 2D walkway diagram + `component-dependency-map` were updated, and the BoM/cost and weight models were rebased (ceiling-hanger hardware → cantilever arms/gussets — roughly neutral). The chem-shelf shift and sump reroute followed (§5).

## 8. See Also

- [Walkway Report §4](walkway-report.md) — the as-built right-walkway cantilever rectangle (rev12).
- [Film Plane Mechanism Report](film-plane-mechanism-report.md) — the film-plane rework that drove the change.
- [Weight Distribution Report §3.2](weight-distribution-report.md) — the right-walkway mass used in the load check.

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
