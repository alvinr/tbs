<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Right Walkway — Cantilever Support Study

**Status:** ADOPTED — **design rationale**. The right walkway is cantilevered off the IBC frame and the side walls. The as-built version (a closed cantilever rectangle) is in [Walkway Report §4](walkway-report.md); this page records *why* a cantilever rather than a ceiling-hung walkway, and the first-order load check behind it.

## 1. Why

A **ceiling-hung** walkway — five M10 rod-pairs from the deck up to the roof — conflicts with the film plane, whose rails run the full width on wall-seat saddles: **the vertical rods would sit in the film plane's X-footprint (X4329–4629 ⊂ X260–4649) and in the volume the tilting plane sweeps** — the plane's right corner reaches Yd1760 at <!-- BEGIN fact:film_plane_max_swing -->28<!-- END fact:film_plane_max_swing -->° swing and Yd1575 at <!-- BEGIN fact:film_plane_max_tilt -->40<!-- END fact:film_plane_max_tilt -->° tilt, colliding with the hangers at Yd1828/1371 — plus the rods would sit in the optical band (shadow risk). See [Film Plane Report](film-plane-mechanism-report.md) and the corner analysis.

**Key insight:** the **deck itself is not the problem** — it sits at Z140, tucked *under* the film-frame bottom (Z160). Only the **vertical rods** intrude. Remove the rods and the film-plane conflict disappears, **with no reduction in film size and the same swing range on both sides**.

## 2. The clearance that makes a cantilever possible

A floor- or wall-supported deck needs room under the grate and beside the tray. Both exist:

| Element | Z | Note |
|---|---|---|
| Tray rim | 50 | |
| **Spray-bar gantry (top)** | **~67–78** | Ø32 wheels + 1½in-square SS beam, rides the Yd-sloped floor — *low* |
| **Clear band under the grate** | **~30mm (worst, far-left)** | see [Walkway Routing Sections §H-H](walkway-routing-sections.md) |
| Walkway grate | 115–130 | |
| Film-frame bottom rail | 150 | deck clears it by 20mm |

Plus a **45mm gap (X4629–4674)** between the tray's right edge and the IBC frame face. So there is both vertical and horizontal room for the supports.

## 3. The design — hybrid anchor (IBC frame + side walls)

*The as-built closed cantilever rectangle is in [Walkway Report §4](walkway-report.md). The support strategy: cantilever off the IBC frame + wall anchors, no ceiling rods.*

The IBC stacking frame only has uprights at the **corridor (Yd 1046 / 1266, at X4654)** — there is **nothing at the perimeter (Yd0 / 2362)** to bolt to. So the support is split:

- **2 inner cantilever arms** — off the **IBC corridor uprights** (X4654, deep-box front upright). The arm bolts to each upright through a CJ end-plate (M12×100 + rear backing plate — the as-built connection; see [Walkway §4.2](walkway-report.md)); the arm (2×1×0.120in, 50.8×25.4mm) reaches ~325mm back to the deck's left edge (X4329).
- **2 outer wall-mounted ledgers** — on the **near (Yd0) and far (Yd2362) container walls**, each **through-bolted** (interior + exterior plate, 2 bolts) at 2 X stations along the deck width. These carry the deck's ends, where the frame can't reach.
- **2 longitudinal bearers** (Yd-running, at X4329 + X4629) ride the arms + ledgers; the grate spans the ≤1,046mm between supports.
- All members sit at **Z70–115** — ~10mm above the spray-bar top at the (low-side) cantilever stations, below the film frame (Z150). **No ceiling rods. Nothing into the tray. Nothing in the optical band above the deck.**

3D study model: `src/models/generate_right_cantilever_study.py` (scenes: Combined / **Anchors (frame + walls)** / Clearance / Labeled — the Anchors scene shows both the upright arm-mounts and the wall ledgers).

## 4. Load check (first-order — favorable)

| Quantity | Value | Notes |
|---|---|---|
| Deck self-weight | ~0.45 kN | right walkway ≈ 46 kg ([Weight Dist. §3.2](weight-distribution-report.md)) |
| Live load (one person) | 1.0 kN | ~100 kg |
| Worst cantilever arm | 325mm | person at the far deck edge, over one arm |
| **Worst single-arm moment** | **~0.33 kN·m** | 1.0 kN × 0.325 m (conservative; normally shared 2 arms) |
| Arm bending stress (as-built **2×1×0.120in**, Z≈3.35 cm³) | ~98 MPa | vs 250 MPa yield → **SF ≈ 2.5** (single-arm, conservative; shared across the 2 mid-span arms in service). 2×1 is the shallowest stock section that clears the spray beam (2×⅞ is non-stock) |
| Added stress on IBC upright (2×2×0.120in, Z≈8.8 cm³) | ~37 MPa | small vs the frame's stack duty |
| Anchor bolt force (2 bolts @ ~100mm) | ~3.3 kN/bolt | vs ~15–20 kN M12 capacity → **SF ≈ 5** |

The IBC frame already carries the 2×2 IBC stack and is anchored to floor + walls; the added ~0.33 kN·m cantilever is minor. **Recommend a structural sign-off on the gusset connection**, but first-order it's comfortable.

## 5. What it resolves / what stays separate

**Resolved:** the film-plane ↔ walkway conflict (no rods in the sweep or optical band); film plane keeps **full width (X260–4649)** and the **same tilt/swing range on both sides**; ceiling de-cluttered on the right.

**Related clearances:** the **chem prep shelf** sits left of the tap (X3129–3729 / Yd300–600), clear of the film-plane swing envelope, and the **sump pickup + tray-drain plumbing** return riser runs in the grate gap with a Yd twist to clear the right-walkway beam.

## 6. Comparison

| | Ceiling-hung | **Cantilever off IBC frame (adopted)** |
|---|---|---|
| Rods in film-plane sweep / optics | **yes** (the conflict) | **none** |
| Forces film-size reduction? | yes, unless the film plane narrows | **no** — full width, symmetric swing |
| Tray / spray-bar intrusion | none | none (arms at Z70–115, above the gantry) |
| Adds load to | roof ribs | IBC frame (2 inner arms) + near/far walls (2 ledgers); minor — needs connection sign-off |
| Cost | 5 rod-pairs + 10 roof plates | 2 arms + 2 wall ledgers + clamps/bolts (≈ neutral) |

## 7. See Also

- [Walkway Report §4](walkway-report.md) — the as-built right-walkway cantilever rectangle.
- [Film Plane Mechanism Report](film-plane-mechanism-report.md) — the film-plane sweep the walkway must clear.
- [Weight Distribution Report §3.2](weight-distribution-report.md) — the right-walkway mass used in the load check.
