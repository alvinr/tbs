<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
<!-- Design spec / scope — NOT a published TBS artifact (not registered in publish.sh). -->

# Walkway System — Definitive Blueprint Spec

**Status:** scoped, awaiting sign-off before implementation. Branch **`walkway-bp`**.
**Purpose:** upgrade the perimeter walkway from arrangement-schematic to a **dimensionally-exact,
fabricator-ready** drawing package — the third subsystem to take the film-plane-corner milestone
standard (dimensioned details + fastener schedule + weld schedule + datums/GD&T + a computed load
case), driven parametrically from `tbs_constants` so it can't drift. Follows
[`ibc-frame-blueprint-spec.md`](ibc-frame-blueprint-spec.md) and
[`fp-corner-blueprint-spec.md`](fp-corner-blueprint-spec.md) as the templates.

The distinguishing feature of this pass: four **real geometry fixes** (Phase 0) must land in the 3D
model *before* dimensioning, because you cannot blueprint geometry that is about to move.

## Locked decisions (2026-08-18)

1. **Fix first, then dimension.** Resolve all four geometry fixes in the generators, regenerate,
   `--send`, verify with `check_interference.py --solids`, ALVIN saves + uploads the corrected models —
   **then** dimension the corrected geometry. (Alvin 2026-08-18.)
2. **Structural load basis = US IBC/OSHA.** IBC 2021 Table 1607.1 "walkways and elevated platforms" =
   **60 psf (2.87 kPa) uniform** + a **300 lbf (1.33 kN) concentrated** footfall on a small area
   (ASCE 7 / OSHA 1910.22). US codes for a US build; cited in the validation table. (Alvin 2026-08-18.)
3. **One branch, single phased pass** (`walkway-bp`): Phase 0 → 1 → A → B → C → D → E, mirroring the
   IBC-frame blueprint one-to-one.
4. **Scope boundary — the walkway owns every cantilever EXCEPT the two IBC-post arms.** The walkway
   blueprint OWNS: the near/far wall-cantilever gusset brackets, the 5 left floor-leg cantilever
   brackets, the right cantilever-rectangle (long + end + cranked beams), the wall cleats, the grating
   cut-plans, and the walkway side of the combined corner plate. **The two center cantilever arms that
   mount on the IBC front uprights — and their J6 connection — are owned by the IBC-frame component**
   ([`ibc-frame-blueprint-spec.md`](ibc-frame-blueprint-spec.md) §3.4–3.6); the walkway blueprint
   cross-references them and does NOT dimension, validate, or cost them. (Alvin 2026-08-18.) **BOM
   consequence (Phase E):** the `walkway-cantilever-arms`, J6 end/backing-plate, and crush-sleeve lines
   currently sit in the *walkway* parts list — reconcile their placement to the IBC frame (touches the
   IBC-frame total, so do it deliberately, not silently). The **combined corner plate** (shared with the
   film-plane bottom/top rail) is likewise cross-referenced, not silently re-specced.

## Design of record (from `walkway-report.md` + `tbs_constants.py`)

| Element | Spec |
|---|---|
| Deck | 300 mm wide (`WALKWAY_W`), 140 mm high (`WALKWAY_H`) = Z115 arm/bracket top + 25 mm grate (`WALKWAY_GRATE_T`) |
| Grating | 1" (25 mm) molded GRP, vinyl-ester grit — McNichols MS-S-100; 4 removable sections |
| Near/far wall gusset bracket — standard | 8 mm plate (`WALKWAY_BRACKET_T`): 150 mm leg (`WALKWAY_BRACKET_H`) + 300 mm arm + 70 mm gusset; **3× M12** through-bolt (2+1) at 457 mm rib centers (`WALKWAY_BRACKET_SPACING`); 100×180×6 exterior reinforcing plate |
| Near wall gusset bracket — widened | 10 mm plate (`WALKWAY_WIDE_BRACKET_T`): 200 mm leg (`WALKWAY_WIDE_BRACKET_H`) + 500 mm arm (`WALKWAY_NEAR_WIDE_W`) + 70 mm gusset; **4× M12** (2+2); 120×220×6 reinforcing plate; ×5 over X1055–3083 |
| Width-transition bearing plate | 40×500×5 flat bar, welded to arm top at each 300↔500 transition (×2) |
| Right cantilever rectangle | 2×1×0.120in (50.8×25.4) A500 RHS closed frame: 2 long beams (`RWK_BEARER_W`, span `C_WID` 2362) + 2 end beams (~300), soffit Z89.6 (`LEFT_WK_CANT_ARM_Z0`/`RWK_ARM_BOT`) clears the 1½ spray beam by 11.6 mm |
| Cranked inner beam | inner long beam jogged outboard 100 mm (`RWK_CRANK_DX`) over the muslin notch Yd1912–2062 with 100 mm ramps (`RWK_CRANK_*`) — one continuous uncut member |
| Center cantilever arms (×2) — **IBC-frame owned** | **solid** 2×1in bar, half-lapped over both long beams (`RWK_HL_TIP` 95.0 / `RWK_HL_POST` 105.6 rebalanced splits); cantilever off the IBC front uprights (`RWK_X_UP` 4654). Detailed/validated/costed in the **IBC-frame blueprint** (J6); listed here only for the rectangle interface (the mid-span pickup) |
| Combined corner plate (right ×2) | 10 mm plate, 150 mm wide — carries the walkway right beam (70 mm seat) AND the film bottom/top rail (150 mm seat); 4× M12 permanent, interior+exterior sandwich (`fp_combined_corner_plate`) |
| Wall cleat (left corners of right walkway ×2) | 8 mm back-plate + exterior plate + shelf; M12 through-bolt |
| Floor-leg cantilever bracket (left walkway ×5) | 2×2×0.120in SHS post (~115 mm, `LEFT_WK_CANT_POST`) + 2×1×0.120in arm (`LEFT_WK_CANT_ARM_*`, reach X470 std ×2 / X770 punch-out ×3) + 128×60×8 foot plate (`LEFT_WK_CANT_FOOT`); **4× #14×2″ 410 SS** screws into ply-over-steel floor (`LEFT_WK_CANT_FOOT_BOLT_N`) |
| Grate retention | 316 SS hold-down clips (near/far/right, ~914 mm centers); gravity lift-out (left) |
| Grate cut features | spray-bar slits (30 mm, near+far), left drum-exit punch-out (600 mm, Yd800–1560), near bump-out (500 mm, X1055–3083), muslin notches (100×150, left+right) |

## Load basis — IBC 2021 / ASCE 7 / OSHA 1910.22

| Case | Value | Governs |
|---|---|---|
| Uniform live load | **60 psf = 2.87 kPa** (IBC Table 1607.1, walkways/elevated platforms) | grate span, distributed bracket demand |
| Concentrated load | **300 lbf = 1.33 kN** on a 2"×2" area (ASCE 7 / OSHA 1910.22) | cantilever arm tips, single-footfall worst case |
| Load factor / basis | ASD service check with SF reported; steel Fy = 250 MPa (A500 Gr.B / A36) | all steel elements |

Sources to cite in the validation table: [IBC 2021 §1607 / Table 1607.1](https://codes.iccsafe.org/content/IBC2021P2/chapter-16-structural-design),
[OSHA 1910.22 walking-working surfaces](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.22),
[ASCE 7-22](https://www.asce.org/publications-and-news/asce-7). (Grating capacity from the
[Fibergrate molded-grating load tables](https://www.fibergrate.com/products/molded-gratings/).)

## Phase 0 — Geometry fixes (model + cascade; ALVIN saves/uploads) — PRECONDITION

Resolve each in the generating Python (`src/models/*.py` + `tbs_constants.py`), regenerate, `--send`
into the matching open doc, verify with `check_interference.py --solids` + read-only `eval_ruby`, then
ALVIN saves + uploads. Re-send order **focus-model-first** (walkway before overview/construction).

- [x] **F1 — Shorten the right walkway.** It currently overruns into the film-plane bottom-rail
  support brackets. Pull the right deck / cantilever-rectangle right edge back so it stops clear of
  those brackets. Derive the new right edge from the film-plane bracket X; check IBC-valve/filter/pump
  reach-in access is preserved. (Alvin 2026-08-17.)
- [x] **F2 — One shared right-corner bracket.** At each near/far RIGHT corner the film-plane beam
  bracket and the walkway right-beam bracket read as two separate brackets — make the geometry read as
  **one** (the `fp_combined_corner_plate` already shares the seat). Cross-ref the film-plane blueprint.
  (Alvin 2026-08-17.)
- [x] **F3 — Relocate floor-leg foot anchors.** On `walkway-sheet6` View B the post is drawn welded
  **over** the 4 foot-plate anchor holes, so the screws can't be driven. Move the 4 anchors into the
  foot's outboard **outrigger** (X≈147–225, clear of the 50.8 post at X225–275 after the 2026-08-16
  foot-X0 derive fix), or otherwise clear the post footprint. Add a foot-anchor PCD constant.
- [x] **F4 — Resolve cantilever/bolt/grate clashes.** Two zones: (1) the **left lift-out** section —
  cantilever arm / bolt / grate overlap; (2) the **far** section — same class of clash. Trace each in
  the model, resolve (shorten/reposition arm, move bolt, or trim grate), verify clean with
  `check_interference.py --solids`. Likely coupled to F1/F2.

**Gate:** Phase 0 complete = `check_interference.py --solids` clean on the walkway zone + ALVIN
confirms "saved + uploaded" for every re-sent model. Only then start Phase 1.

## Phase 1 — Reconcile + parametrize (so every drawn dimension is a constant)

- [x] **Promote model-local structural constants → `tbs_constants.py`.** DONE (Phase 1.1, commit
  `a8dc8788`): the 26-constant `RWK_*` family moved out of `generate_sketchup_model.py` into the shared
  constants (models byte-identical → no re-send). Repointing `generate_walkway_diagram.py` surfaced +
  fixed real drift on **sheet 3** (right-walkway plan): beam section "40×40×3 SHS" → **2×1in** (50.8×25.4,
  tube long/end + solid flat-bar arm), deck **300 → 245** (F1), outer/end-beam layout now model-accurate;
  sheet 1 label reconciled.
- [x] **Add the un-parametrized blueprint dimensions as constants.** DONE + scoped (Phase 1.2, commit
  `c01542cd`):
  - **Promoted** (were duplicated in the model + diagram): reinforcing-plate blanks (`WALKWAY_REINF_W/H/T`
    100/180/6 std, `_W_WIDE/_H_WIDE` 120/220), gusset reach (`WALKWAY_GUSSET_REACH` 70), wall-bolt edge
    distances. **Standard** bracket = `WALKWAY_BRACKET_BOLT_DX` **27** (Sheet 2 View B; 23mm edge on the
    100mm plate); **widened** bracket = `WALKWAY_BRACKET_BOLT_DX_WIDE` **32** (Sheet 7 View B; 120mm plate).
    `_BOLT_Z_LO` 42 / `_LO_WIDE` 35. The 3D model had drifted to ±32 for BOTH — corrected in Phase 1.3 to
    ±27 standard (matches the drawings), re-sending walkway/overview/construction.
  - **Already done** (Phase 0): foot-anchor PCD (`LEFT_WK_CANT_FOOT_BOLT_DX/DY`).
  - **Out of scope — IBC-frame-owned:** the arm end-plate blank (65×155×8) is the **J6** joint (walkway
    arm → IBC upright), drawn on **IBC-frame Sheet 5**; the walkway blueprint cross-references it, does not
    re-dimension it. (Height already single-sourced as `RWK_J6_EP_H`.)
  - **Retired:** the "transition bearing plate (40×500×5)" no longer exists — the left edge beam + wall
    seats were replaced by the floor-leg cantilevers.
  - **Deferred to Phase D** (single-consumer detail dims → promote when their cut sheet is authored, per
    the "leave detail dims" rule): the **wall-cleat blank** and the **grate-clip pitch** (fix against the
    McNichols clip datasheet). Logged in TODO.
- [x] **Drift sweep** — DONE (Phase 1.3): stale literals in `walkway-report.md`, the two generators, and
  `component-dependency-map.md`; reconcile any residual "4734" RWK comments and pre-Phase-0 geometry.
  Also confirm the walkway-report's **J6** mention points to IBC-frame Sheet 5 (a mark must resolve to a
  labeled drawing).

## Phase A — Structural validation (`walkway_load.py`, analog of `ibc_frame_load.py`)

New driftproof compute script → optional rendered `walkway-load-case.png`. Each element: IBC/OSHA
design force → capacity → SF, authoritative voice, every capacity/coefficient cited.

- [x] **Grate span** — MS-S-100 molded FRP between bearers under 2.87 kPa uniform + 1.33 kN
  concentrated; deflection + bearing.
- [x] **Standard wall gusset bracket** — 8 mm plate arm (300 mm cantilever) bending/deflection at the
  arm tip; gusset.
- [x] **Widened wall gusset bracket** — 10 mm plate, 500 mm cantilever (governing wall bracket).
- [x] **Wall bolt group** — 3× (std) / 4× (widened) M12 in shear + **reinforcing-plate bearing /
  corrugated-wall pull-through** (ties to the parked 30 mm corrugation-depth procurement gate).
- [x] **Floor-leg cantilever** — worst = extended punch-out arm (X770 reach): 2×1 arm + 2×2 post
  bending; **foot-anchor group** (4× #14×2 screws) shear + uplift into ply-over-steel.
- [x] **Right cantilever rectangle** — long/end/cranked-beam bending + rectangle deflection **assuming
  the mid-span pickup** by the two IBC-post arms; half-lap notch net section at the crossings. The
  arm-root moment (≈0.35 kN·m vs ≈0.84 kN·m capacity per the
  [cantilever study](right-walkway-cantilever-study.md)) is the **IBC-frame** J6's check — cross-ref
  `ibc_frame_load.py`, do not re-validate here.
- [x] **Combined corner plate** — 10 mm plate carrying walkway beam + film rail; bolt group.

Deliverable: a computed validation table into `walkway-report.md` §9 (replacing the qualitative
hand-check prose). Fold the existing `right-walkway-cantilever-study.md` numbers into the script so
they can't drift.

## Phase B — Fastener + weld schedule

- [x] **Fastener schedule J1…Jn** (size/grade/torque/washer/locker, cited): std bracket wall bolt
  (M12×65 91280A728); widened bracket wall bolt (M12×65); right cleat / combined-corner bolt (M12×70
  91280A732); floor-leg foot screw (#14×2 410 SS self-driller); grating clips. (The center-arm end-plate
  bolt M12×100 + the half-lap hold-down screws that fix the two arms belong to the **IBC-frame** J6
  schedule — cross-ref, not scheduled here.)
- [x] **Weld schedule W1…Wn** (leg/symbol/extent): bracket gusset↔leg↔arm fillets; reinforcing-plate;
  rectangle long↔end beam corners; cranked-beam ramps; floor-leg post↔foot + post↔arm; wall-cleat welds;
  combined-corner-plate seats. Load-check the governing throats in `walkway_load.py`; the rest are AWS
  D1.1 minimum practical fillets (note which). (The half-lap seat + arm-end-plate welds are the
  **IBC-frame** J6/W schedule — cross-ref, not scheduled here.)
- [x] Tables into `walkway-report.md` (§ near the parts list); J/W callouts land on the sheets in Phase D.

## Phase C — Datum + tolerance scheme

- [x] **Datums:** A = floor plane (foot undersides / container floor); B = pinhole + film-plane wall
  faces (the two long walls the brackets bolt to); C = rail datum X260/X4649 (film-plane left/right).
- [x] **Functional tolerances:** deck level/coplanarity, bracket arm reach, wall-bolt PCDs, foot-anchor
  PCD, grate cut/slit/notch positions, corner-plate seat Z. General = ISO 13920 Class B; welds = AWS D1.1.
- [x] Report § + a **DATUMS & TOLERANCES** callout block on the plan sheet.

## Phase D — Fab-detail sheets (extend `generate_walkway_diagram.py`)

- [x] **J/W callouts** onto the existing detail sheets (bracket cross-section Sheet 2/7, floor-leg
  Sheet 6, transition Sheet 8, right cantilever Sheet 3).
- [x] **Member cut list** — computed from the constants (near/far bracket plates, right-rectangle long
  + end + cranked beams, floor-leg posts/arms, feet, reinforcing plates, cleats, corner plates,
  transition plates + a stock linear-feet summary). The two IBC-post arms are in the **IBC-frame** cut
  list, not here.
- [x] **Plate fabrication schedule (1:1)** — foot plate (with relocated anchors), std + widened
  reinforcing plates, combined corner plate, wall cleat, transition bearing plate — each with hole
  Ø/positions/PCD. (The J6 arm end/backing plates are on the **IBC-frame** plate schedule.)
- [x] **Grate cut-plan** — the 4 sections dimensioned with spray slits, drum-exit punch-out, near
  bump-out, muslin notches, and clip positions (a fabricator/nesting drawing).
- [x] **Consolidated weld map** — W1…Wn ticked to their frame locations + the schedule.
- [x] Register every new sheet: `all-diagrams.md` gallery, `publish.sh`, `setup_docs.py`,
  `dependencies.yml`; embed in the report.

## Phase E — Cascade + close (as changes land)

- [x] Firm any spec change into `parts.py` / `costing.py` / master-shopping-list / cost-breakdown (same
  commit); `parts.py --check` + `costing.py --check-registry`.
- [x] Regenerate + gallery-register new sheets; re-send models only if geometry detail changed (Phase 0
  already covers the geometry); `manifest.py --update`.
- [x] `lint.py` (+ `--verify-all` before publish) + `check_consistency.py` clean.
- [x] RELEASE `[Unreleased]` bullet; tick the TODO "Walkway blueprint pass" sub-items.

## Open decisions

1. **F1 shortening target** — the exact new right-walkway right edge (derive from the film-plane
   bottom-rail bracket X; confirm IBC reach-in access survives). Settle in Phase 0.
2. **Coating / surface-finish spec** — deferred to the fab/quoting stage (as with the IBC frame).
3. **Rendered load-case sheet** — build `walkway-load-case.png` in Phase D if wanted (optional, like
   `ibc-frame-load-case.png`); Phase A lands as the §9 table regardless.
