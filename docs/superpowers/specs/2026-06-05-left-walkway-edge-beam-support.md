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

1. **Edge beam, not a buried bearer.** Stand a **steel 50×50×3 SHS** on the deck's
   inner edge, occupying the full usable envelope **Z≈45–95** — above the bath
   (Z≈42) and below the film-frame bottom (Z=100). It is ~15 mm proud of the deck,
   which doubles as a **toe-board / safety kerb** at the tray edge. Steel (not
   aluminum) for stiffness over the span. Full width, X≈470, Yd 0→2362; the grate
   inner edge bolts to it.

2. **Bolt-through wall seats, not a cantilever** (the IBC load path). The edge
   beam is **simply supported wall-to-wall** on a seat bracket **bolted through the
   corrugated wall** at each end (interior seat plate + 3× M12 through-bolts +
   exterior backing plate, like the IBC wall-seat brackets). The person's load
   goes grate → beam → wall as a clean end reaction, not a cantilever moment.

The beam also picks up the near/far walkways' door-end grate edges (it sits at
their X=470 start), so the X=470 cantilever bracket is removed.

## Why it's sound (hand-check, ≈1 kN person at midspan, span = full width 2362 mm)
- Bending ≈71 MPa vs ~250 MPa yield → **FoS ≈3.5**.
- Deflection ≈6.6 mm = **L/358** (stiff; not bouncy).
- Beam mass ≈10.5 kg → liftable for the lift-out.
- Each wall reaction ≈0.5 kN — the IBC wall seats carry ~50× that (4×600 L water).

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
