# Film-Plane Mechanism — Demountable Brace Cage, Drum Clearance & Walkway Interface

**Date:** 2026-06-01
**Status:** Design approved, pending spec review
**Branch:** `film-plane-demountable-frame` (off `main`)

## Background

The TBS-001 film plane rides a **4-corner independent mechanism**: four corner
carriages (TL, TR, BL, BR), each on its own leadscrew-driven rail, joined to the
film frame through universal joints so the frame can tilt, swing, and compound.

Reviewing the 3D Overview model surfaced three coupled problems with the current
design as drawn:

1. **Rails are unbraced.** The four rails stand off the floor/ceiling by 100mm
   (`RAIL_OFF`) and are tied together only by the *moving* carriage. Nothing
   braces the fixed track, so the rails cantilever and can rack/twist.
2. **The left rail collides with the light-trap drum.** The drum is a vertical
   Ø750 cylinder centered at (X=0, Yd=1181), occupying X −375…+375, Yd 806…1556,
   Z 0…2200. The fixed left rail (X=150) and the moving carriage's left edge pass
   straight through that volume — for the rail, across Yd ≈ 837…1525. The drum
   cannot rotate with the rail there.
3. **Bottom members collide with the walkways.** The floor rails sit at Z=100 —
   exactly the walkway grate height (75–100). Bottom rails and any bottom
   cross-beam interfere with the near walkway (Yd 0–300), far walkway (2062–2362)
   and clip the left/right walkways (X 170–470, 4329–4629).

### Coordinate reference (mm; X = length 0–5893, Yd = depth 0–2362, Z = height 0–2388)

| Element | X | Yd | Z |
|---|---|---|---|
| Film rails (4 corners) | left 150, right 4649 | run 100→2262 | floor 100, ceiling 2288 |
| Light-trap drum (Ø750) | center 0 → −375…+375 | center 1181 → 806…1556 | 0…2200 |
| Near / far walkway | — | 0–300 / 2062–2362 | grate 75–100 |
| Left / right walkway | 170–470 / 4329–4629 | full length | grate 75–100 |

## Design decisions

The unifying principle: **the film frame is a composition aid that only needs to
hold position during the exposure.** It does not need a welded monocoque. So the
brace structure is a *demountable clamped cage* — saddles plus thumbscrews /
locking pins — which is "rigid enough" for a static exposure and, critically,
knocks down for transport. That single choice resolves all three issues.

### 1. Demountable brace cage (rigidity)

Add a rectangular **portal frame at each end** of the rail set:

- Pinhole-end portal at Yd=100, film-end portal at Yd=2262.
- Each portal = left vertical (X=150) + right vertical (X=4649), both spanning
  Z 100→2288, plus a **top cross-beam** (Z≈2288) and a **bottom cross-beam**
  (under-grate, see §3) spanning X 150→4649.
- Four rails + two portals = a torsionally rigid box, independent of the
  (corrugated, non-structural) container shell.
- **Joints are saddles + thumbscrews / locking pins, not welds.** The frame is
  pre-set and locked for use; it disassembles for transport.

Proposed member section: **50×50×3mm RHS** (matches the IBC rack precedent);
final sizing is an implementation detail to confirm against load/deflection.

### 2. Drum clearance via a demountable left-rail segment

The end portals already clear the drum (their verticals are at Yd 100 and 2262,
outside the drum's Yd 806–1556). The conflict is the **continuous left rail** and
the **carriage's left edge** passing through the drum zone. Resolution:

- The **left-rail segment spanning Yd ≈ 806–1556 is swing-away / demountable** on
  its saddles (consistent with the clamped-cage design).
- **Two operating modes**, enforced by an operational interlock:
  - *Drum mode* (human entry/exit): left segment swung clear, carriage parked at
    the film end (Yd > 1556) so its left corner is outside the drum envelope, drum
    free to rotate.
  - *Film mode*: left segment locked in, carriage free to use full travel
    (Yd 100–2262) for tilt/swing, drum static.
- **Image width is preserved** — `FP_X_L` stays at 150 (rejected: insetting the
  left edge, which would shrink the image; rejected: external vestibule, which
  conflicts with the transport requirement).

### 3. Walkway interface via the under-grate plenum

- Run the **floor rails and bottom cross-beams at Z ≈ 0–70**, below the grating
  (which sits at 75–100 on its brackets). The grate runs continuous over them.
- **Notch the grate ~30–50mm only at the two frame edges** (X=150 and 4649) where
  the cage's vertical members pass up through grate height.
- Image height is preserved (rejected: raising the mechanism, which loses bottom
  support; rejected: cutting walkway gaps at crossings, a trip hazard).
- Accepted operational limit: at extreme forward travel (Yd→100) the full-height
  carriage occupies the near-walkway band (Yd 100–300); that band is kept clear
  during composition.

## Scope — files to change

**Generators / constants**
- `src/generators/tbs_constants.py` — new constants: brace member section,
  under-grate bottom-member Z band, grate-notch width, demountable left-rail Yd
  span (≈806–1556), carriage park position for drum mode.
- `generate_film_plane_mechanism.py` — draw both end portals, saddle/thumbscrew
  joints, under-grate bottom members, swing-away left-rail segment; update notes
  and BOM; show the two operating modes.
- `generate_walkway_diagram.py` — under-grate plenum routing + edge notches at
  X=150/4649.
- `generate_lighttrap_diagram.py` and/or `generate_floorplan_diagram.py` —
  drum-mode clearance, swing-away left rail, operational interlock note.

**Reports (per CLAUDE.md: drawing-spec changes propagate to parts/cost docs)**
- Owning report `.md`(s) for the film-plane mechanism — parts list.
- `master-shopping-list.md` and `project-cost-breakdown.md` — add brace members,
  saddles, thumbscrews/locking pins; supplier options + prices.

**Downstream (separate, later)**
- Re-apply to the 3D Overview model on the `3d-models` branch (Film Plane
  Mechanism + Ceiling Rail + Walkway components).

## Out of scope

- Detailed leadscrew/drive redesign (the corner drives are unchanged).
- The 3D model update (tracked separately; see the resume note).
- Any change to image dimensions, pinhole, or optical constants.

## Open implementation details (tunable, not blocking)

- Final brace member section and joint hardware spec.
- Exact grate-notch dimensions and under-grate Z band.
- Exact carriage park Yd for drum mode (any value > 1556 clears the drum).
