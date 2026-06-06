<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Left Walkway Support — Edge Beam on Bolt-Through Wall Seats (design)

**Status:** approved 2026-06-05. Replaces the cantilevered Al bearer beam.

## Problem
The removable left walkway (cargo-door end, X≈170–470, full width) sits over the
processing tray, so its **inner edge (X≈470) cannot be supported from below**
(no fluid contact). The deck is held LOW (top Z=80) so the film plane travels
above it (film-frame bottom Z=100) — leaving only ~15 mm between the tray rim
(Z=50) and the grate underside (Z=65). The previous inner-edge support — a 50×50
Al RHS bearer **cantilevered** from the side-wall brackets — failed two ways:
1. A full 50×50 section can't fit the 15 mm clearance, so it either dipped into
   the bath (Z≈42) or shrank to a flimsy 15 mm bar.
2. It dumped a person's reaction onto the **tip of a 300 mm cantilever arm**
   (mostly unbraced) — grossly overstressed; the walkway brackets were sized for
   the light distributed grate load, not a concentrated bearer reaction.

Ruled out: **rod/ceiling suspension** (would foul the film plane, which sweeps the
whole image zone X 150–4649 above Z=100 — unlike the right walkway at the far end).

## Decision
Two changes:

1. **Edge beam, not a buried bearer.** Stand a **steel 40×40×3 SHS** on the deck's
   inner edge, occupying the envelope **Z≈52–92**. It is ~12 mm proud of the deck,
   which doubles as a **toe-board / safety kerb** at the tray edge. Steel (not
   aluminum) for stiffness over the span. Full width, X≈470, Yd 0→2362; the grate
   inner edge rests on a Z65 ledge and is located by the proud kerb.

   *Section sizing (rev 2026-06-05).* The first cut was a 50×50 SHS at Z≈45–95. But
   the beam crosses the tray's **near and far perimeter rims** (Z0–50, at Yd≈80 and
   2280) on its way wall-to-wall, and a beam bottom at Z45 **fouled those rims by
   5 mm**. Dropping to a **40 mm** section and raising the underside to **Z52** gives
   a 2 mm clearance over the rim (Z50), still clears the bath (Z42) by 10 mm and the
   film-frame bottom (Z100) by 8 mm, and keeps the load entirely on the wall seats
   (the thin SS tray rim carries nothing). Trade-off: ~half the second moment of
   area, so the beam is springier (see below) — accepted for occasional single-person
   access.

2. **Bolt-through wall seats, not a cantilever** (the IBC load path). The edge
   beam is **simply supported wall-to-wall** on a seat bracket **bolted through the
   corrugated wall** at each end (interior seat plate + 3× M12 through-bolts +
   exterior backing plate, like the IBC wall-seat brackets). The person's load
   goes grate → beam → wall as a clean end reaction, not a cantilever moment.

The beam also picks up the near/far walkways' door-end grate edges (it sits at
their X=470 start), so the X=470 cantilever bracket is removed.

## Why it's sound (hand-check, ≈1 kN person at midspan, span = full width 2362 mm)
40×40×3 SHS: I ≈ 1.02×10⁵ mm⁴, Z ≈ 5.1×10³ mm³.
- Bending ≈116 MPa vs ~250 MPa yield → **FoS ≈2.2**.
- Deflection ≈13 mm = **L/175** (springy but serviceable for occasional single-person
  access; a midspan stiffener or the notched-50×50 alternative is the fallback if
  the bounce is objectionable).
- Beam mass ≈8.2 kg → liftable for the lift-out.
- Each wall reaction ≈0.5 kN — the IBC wall seats carry ~50× that (4×600 L water).
- Bottom clears the tray rim (Z50) by 2 mm, so it never loads the SS rim.

## Transport
Unlike the IBC seats (permanent, sealed end), these sit at **X≈470 — in the cargo-
panel transport-slide path** — so the **edge beam + interior seat brackets are
demountable** (a few bolts) and come out with the left lift-out before the panel
slides. The through-bolts + exterior backing plate stay on the wall.

## Outer edge (unchanged)
A 15 mm Al bearing strip on the tray rim (X=170) + 3 floor legs (25×25×3 Al SHS,
X≈140, on bare floor outside the tray) — no tray load.

## Propagation
- `tbs_constants.py` — left-walkway support constants (material → steel; add
  wall-seat bracket params; demountable).
- `generate_walkway_model.py` — `left_support()` (done): edge beam + wall seats.
- `generate_walkway_diagram.py` — the left-support detail (View/Sheet).
- `walkway-report.md`, `master-shopping-list.md`, `project-cost-breakdown.md` —
  BOM (steel edge beam + 2 wall-seat brackets + bolts, vs the Al bearer).

## Open / to verify
- Confirm nothing on the film plane hangs below Z=100 (≈5 mm margin to the kerb top).
- A real structural sign-off (this is a hand-check, not an analysis).
