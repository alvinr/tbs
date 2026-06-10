<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Right Walkway — Cantilever Support Study

**Status:** STUDY for review (not yet adopted). Baseline remains the ceiling-hung right walkway until this is approved.

## 1. Why

The right walkway (IBC-end access, X4329–4629, spanning the full width Yd 0–2362) is currently **ceiling-hung** — five M10 rod-pairs from the deck up to the roof. The film-plane rework (wall-seat saddles, rails now running the full width to X4649) exposed a conflict: **those vertical rods sit in the film plane's X-footprint (X4329–4629 ⊂ X150–4649) and in the volume the tilting plane sweeps** — the plane's right corner reaches Yd1760 at 28° tilt and Yd1575 at 40°, colliding with the hangers at Yd1828/1371 — plus the rods sit in the optical band (shadow risk). See [Film Plane Report](film-plane-mechanism-report.md) and the corner analysis.

**Key insight:** the **deck itself was never the problem** — it sits at Z130, tucked *under* the film-frame bottom (Z150). Only the **vertical rods** intrude. Remove the rods and the film-plane conflict disappears, **with no reduction in film size and the same swing range on both sides**.

## 2. The clearance that makes this possible now

The earlier design went ceiling-hung because there was thought to be no room for floor/wall support. That changed:

| Element | Z | Note |
|---|---|---|
| Tray rim | 50 | |
| **Spray-bar gantry (top)** | **60** | rides on Ø50 wheels in the tray — *low* |
| **Clear band under the grate** | **60 → 115 (55mm)** | newly free |
| Walkway grate | 115–130 | |
| Film-frame bottom rail | 150 | deck clears it by 20mm |

Plus a **45mm gap (X4629–4674)** between the tray's right edge and the IBC frame face. So there's now both vertical and horizontal room the old layout lacked.

## 3. Proposed design — cantilever off the IBC frame

Carry the deck from the **IBC stacking-frame near face (X4674)** instead of the ceiling:

- **4 cantilever arms** — 40×45 SHS, reaching **345mm** back from the frame face (X4674) to the deck's left edge (X4329), at the frame's existing upright lines **Yd 0 / 1046 / 1316 / 2362**. Arms sit at **Z70–115** — 10mm above the spray bar (Z60), below the film frame (Z150).
- **Anchor** — each arm bolts to its IBC-frame upright with an 8mm gusset plate + 2× M12 (a moment connection).
- **2 longitudinal bearers** (Yd-running, at X4329 + X4629) on the arm tops; the grate spans the ≤1046mm between arms.
- **No ceiling rods. Nothing into the tray. Nothing in the optical band above the deck.**

3D study model: `src/models/generate_right_cantilever_study.py` (scenes: Combined / Cantilever only / Clearance / Labeled).

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

**Still solved separately (parked, per direction):** the **chem prep shelf** (its own ceiling rods at X3729–4329 / Yd300–600 — clear of the film sweep, but a ceiling-crowding/optics item to revisit) and the **sump pickup + tray-drain plumbing** in the near-right corner.

## 6. Comparison

| | Ceiling-hung (current) | **Cantilever off IBC frame (proposed)** |
|---|---|---|
| Rods in film-plane sweep / optics | **yes** (the conflict) | **none** |
| Forces film-size reduction? | (else yes) | **no** — full width, symmetric swing |
| Tray / spray-bar intrusion | none | none (arms at Z70–115, above the gantry) |
| Adds load to | roof ribs | IBC frame (minor; needs connection sign-off) |
| Cost | 5 rod-pairs + 10 roof plates | 4 arms + 4 gussets + 8 bolts (≈ neutral) |

## 7. If approved — next steps

1. Move `right_cantilever()` into the walkway model (replace `right_hangers()`) + the overview (single-sourced).
2. Update the 2D walkway diagram + `component-dependency-map`.
3. Update BoM/costs (swap the ceiling-hanger hardware for the cantilever arms/gussets — roughly neutral) and the weight model (similar mass, moved load path).
4. Then chem shelf + sump as follow-ups.
