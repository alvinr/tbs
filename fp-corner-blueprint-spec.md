<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
<!-- Design spec / scope — NOT a published TBS artifact (not registered in publish.sh). -->

# Film-Plane Corner Mechanism — Definitive Blueprint Spec

**Status:** scoped, awaiting sign-off before implementation.
**Purpose:** upgrade ONE film-plane corner from arrangement-schematic to a **dimensionally-exact,
fabricator-ready** drawing — the **template** for rolling the same standard across every subsystem
(water/tray, IBC frame, walkway, hinged panel, light lock, electrical, optics).

## Locked decisions (2026-08-10)

1. **Upgrade the existing corner sheets 3/4/8/9 in place** (in `generate_film_plane_mechanism.py`)
   + add a new **guide-corner sheet**. No separate generator.
2. **Cover both corners**: bottom = **weight** corner (rail web-vertical, skate load-bearing);
   top = **guide** corner (rail flat, skate as guide only) — the mirror pair.
3. **304 stainless** for the cross-slide bar + skate axle (procurement BOM is source of record; the
   cyanotype wash is chloride-free). Fix the stale **316** references.

## Design of record (one corner)

| Element | Spec | Finish |
|---|---|---|
| Depth rail | 3×1½" (76×38) **6061-T6 Al U-channel**, 8 ft (Grainger 795M51) | mill |
| Carriage | 4-wheel **acetal skate** — Ø32 load + Ø20 keeper rollers on Ø10 **304** axles + fab carriage plate | — |
| Cam clamp | 3/corner McMaster **5128A63** low-profile hold-down toggle | zinc |
| Z + X cross-slide | **304** flat-bar ¼"×1½" (6.35×38.1) on UHMW pad + brass-tip gib | — |
| U-joint | **Belden UJ-SS750x375** (3/8" bore, 0.75" OD, 45°), Belden 806VF1 boot; input stub in McMaster **4040N12** 304 shaft support; 3/8" 304 stub | 303/416 SS |
| Corner plate | ¼" **304 SS** 6×8" blank, press-brake **L-bracket** | 304 |
| Frame angle | 2×2×⅛" **6061-Al** angle, welded rigid rectangle 4,499×2,094 | mill |

_(The TODO's "Ruland US12-6-6-SS" is stale — the U-joint was changed to Belden. "Wheels/trolley on
316 pipe" is a superseded concept — the built design is the U-channel + acetal skate.)_

## Phase 1 — Reconcile + parametrize (precondition; no drawing yet)

**1a. Resolve conflicts (drift sweep):**
- Cross-slide bar + skate axle **316 → 304** in: `film-plane-mechanism-report.md` §4, `generate_film_plane_mechanism.py` Sheet-8 note, `component-dependency-map.md` §3.1/§1.3 and the FPM note.
- Rail **material** in depmap "304 U-channel" → **6061-Al**; rail **supplier** stale "McMaster 1262T21" → **Grainger 795M51** (depmap §1.3 + 2D generator comment).
- Rail **scheme**: adopt the 3D model's **two-orientation** build as the design of record (bottom web-vertical weight / top flat guide); fix the report/parts "uniform, one skate rides inside each" wording; drop stale "4×2" / "V-trolley" / "trolley" comments in constants + model.

**1b. Promote/add constants to `tbs_constants.py`** (so the drawing is parametric, can't drift):
- Promote `XSLIDE_Z_TRAVEL` / `XSLIDE_X_TRAVEL` / `XSLIDE_STROKE` / `XSLIDE_N` from **`reserved` → firm** (verify the travel numbers against the swing/tilt geometry first).
- **New:** `XSLIDE_BAR_W=38.1`, `XSLIDE_BAR_T=6.35` (cross-slide bar section); `XSLIDE_UHMW_T`, `XSLIDE_GIB_*`.
- **New:** `UJOINT_BORE=9.53`, `UJOINT_OD=19.05`, `UJOINT_ANGLE=45`, `UJOINT_LEN` (from the Belden datasheet).
- **New:** `SKATE_ROLLER_OD=32`, `SKATE_KEEPER_OD=20`, `SKATE_AXLE_OD=10`, skate roller spacing / carriage-plate W×H×T.
- **New:** `CORNER_PLATE_W=203.2`, `CORNER_PLATE_H=152.4`, `CORNER_PLATE_T=6.35`, bend line + leg lengths.
- **New:** hole **PCDs / edge distances** — see Phase 2 (designed, then captured as constants).

**1c. Firm the load** — compute the **per-corner load** from the reconciled moving mass (carriage 66 kg
incl. ACM, from the weight model) and the **cross-slide bending SF** for the ¼"×1½" 304 bar. This is the
number the milestone says this drawing "firms."

## Phase 2 — Dimensioned drawing upgrades

**Hole positions** — take fixed patterns from datasheets (4040N12 shaft support, 5128A63 cam-clamp
base, U-joint bore); **design** the patterns on our fab plates (carriage plate, L-plate, cross-slide
mounts) to ≥2×Ø edge distance, then capture all as constants (Phase 1b).

- **Sheet 3** (corner carriage detail) → add hole PCDs + edge distances for the skate rollers/axles,
  carriage plate, and U-channel capture; add datum flags; dimension roller spacing.
- **Sheet 4** (rail mounting + transport drop-in) → dimension the rail-end mount, the transport
  drop-in bridge, and the right-flange bolt pattern (PCD/edge distance).
- **Sheet 8** (frame-corner ↔ cross-slide + J1–J5) → dimension the cross-slide **bar section + travel
  + gib/UHMW**; complete J1–J5 (below).
- **Sheet 9** (frame + ACM ↔ U-joint ↔ X-slide) → make it a **dimensioned fabrication section**;
  add the **U-joint envelope** and the **L-plate bend** (bend line, radius, leg lengths, PCDs).
- **NEW Sheet 10** (guide/top corner) → the mirror: rail laid flat, skate as guide (no load path),
  same cross-slide/U-joint stack — call out only the **deltas** from the weight corner.

## Phase 3 — Fastener schedule (complete J1–J5)

Existing J1–J5 (Sheet 8) carry size/thread only. Add per joint: **thread pitch + class**, **torque**
(from the fastener's proof load), **washer** (flat/split), and **thread-locker** (Loctite grade) callout.
- J1/J2 = M8 (carriage/plate); J3 = 3/8" stub → U-joint (key + clamp); J4 = shaft-support setscrew;
  J5 = M6 legs tapped into the frame angle. Verify each against its datasheet.

## Phase 4 — Datum + tolerance scheme

Establish a datum reference frame for the corner (e.g. **A** = frame-angle mounting face, **B** = rail
web, **C** = optical axis) and apply position/parallelism tolerances to the critical features
(cross-slide travel squareness, U-joint bore concentricity, rail capture). Add a title-block tolerance
block (general ±, then per-feature GD&T where it matters).

## Phase 5 — Cascade + close

- Reconcile `parts.py` / `costing.py` / report §7 / master BOM to any spec change (304 confirm = no
  cost move; new constants = no cost move).
- Re-send the `film-plane-mechanism.skp` model so its (currently hardcoded) corner geometry reads the
  new constants; reconcile depmap §3.1.
- Run the gates (`lint.py`, `check_consistency.py`), gallery + registration for the new Sheet 10.
- Tick the milestone sub-items in `TODO.md`; RELEASE `[Unreleased]`.

## Acceptance criteria

A fabricator can build one weight corner **and** one guide corner from Sheets 3/4/8/9/10 alone:
every hole located (PCD/edge distance), every fastener called out (size/thread/torque/locker), every
part's material + finish stated, sections dimensioned, and a datum/tolerance scheme present — all driven
from `tbs_constants` with **zero** `reserved`/prose-only corner dimensions remaining.

## Open items to settle during design

- Exact travel values for the promoted `XSLIDE_*` (verify vs swing/tilt geometry).
- Belden UJ-SS750x375 booted length + bolt/key detail (datasheet).
- Carriage-plate + L-plate hole patterns (design to edge-distance rules).
- Per-corner load + cross-slide bending SF (compute in Phase 1c).
