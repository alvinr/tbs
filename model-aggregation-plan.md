<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->

# Model Aggregation Plan — make `overview` a thin aggregator, eliminate drift

Repo-only planning doc (not published). Goal: **each component's definitive builder lives in
its dedicated sub-model; `overview` becomes a simple aggregation that imports every builder** —
the way it already does for the water systems. Supersedes nothing; this is the concrete plan
for the "Model-drift audit" item in `TODO.md`.

---

## 1. Why drift happens today

`generate_sketchup_model.py` ("overview") is **three things at once**:

1. **The shared primitive library** — `mm`, `ruby_box`, `ruby_cylinder`, `ruby_pipe_run`,
   `ruby_flex_run`, `ruby_coil_cord`, `component()`, the color palette (`C_*`), the tag/scene
   machinery. *Every* model does `import generate_sketchup_model as ov` just to draw anything.
2. **The owner of the structural builders** — walkways, film plane, IBC stack, spray bar,
   processing tray, shell, fans, pinhole/optical. The dedicated sub-models **import these back
   out of overview**.
3. **The aggregator** — `generate_ruby()` assembles the 37 components into the combined model.

Water escaped drift because its geometry lives in `cp`/`pw` and overview only *imports* it.
Everything authored (or re-composed) in overview can diverge from its sub-model — which is the
exact failure chased this session (Cct-E ceiling loop, Cct-C route, missing pull switches).

---

## 2. Current composition — the four patterns

### ① Sub-model definitive · overview imports directly — **TARGET PATTERN (Water)**
- `cp.*` (`generate_corridor_water_panel`): `frame`, `tote_restraint`, `rear_panel`,
  `equipment`, `drains_ports`, `plumbing`, `ribbon_supports`.
- `pw.*` (`generate_pinhole_water_panel`): `backing`, `kit`, `skid_row`, `skid_plumbing`,
  `panel_power`, `tap01_supply`.

### ② Sub-model definitive · overview RE-COMPOSES in a wrapper — **drift-prone (Electrical, Light-trap)**
- Electrical (`em` = `generate_electrical_model`): overview's `electrical()`,
  `ep_external_wiring()`, `lighting_wiring()`, `fan_wiring()`, `evap_cooler()` each hand-pick and
  re-assemble `em.*` builders. The sub-model owns the *pieces*, but the *composition* is authored
  twice → the two assemblies can pick different pieces/params (the drift we kept fixing).
- Light-trap (`lt` = `generate_lighttrap_model`): `light_trap_drum/cage/bay/frame()` wrap `lt.*`.
  **BUG found:** `light_trap_cage()` returns `lt.drum_frame() + "\n" + lt.drum_frame()` — the drum
  frame is emitted **twice**. Fix when this subsystem is touched.

### ③ Overview definitive · sub-models import FROM overview — **BACKWARDS (Structural)**
Owned in overview, consumed by the sub-models via `ov.*`:
| Builder(s) in overview | Consumed by |
|---|---|
| `walkways`, `right_walkway_cantilever`, `right_walkway_grate` | walkway, ibc, film-plane |
| `film_plane_mechanism`, `film_plane_saddles`, `fp_combined_corner_plate(s)`, `panel_pivot` | film-plane, walkway |
| `ibc_stack` | ibc |
| `spray_bar` | (spraybar builds its own? verify) |
| `processing_tray` | walkway, spraybar, film-plane |
| `container_shell`, `far_wall`, `fans`, `pinhole_assembly`, `optical_cone` | — (overview only, but still authored here) |

### Reverse edge
`solar_array()` and `shelf()` are overview-owned and **imported by `electrical.skp`** — the one
place the electrical model depends back on overview.

---

## 3. Target architecture

```
tbs_draw.py   (NEW neutral module: mm, ruby_*, component(), colors, tag/scene helpers)
   ▲  ▲  ▲  ▲
   │  │  │  └── generate_corridor_water_panel.py   (cp)   owns corridor water geometry
   │  │  └───── generate_pinhole_water_panel.py    (pw)   owns pinhole water geometry
   │  └──────── generate_electrical_model.py       (em)   owns ALL electrical geometry
   │  └──────── generate_walkway_model.py          (wm)   owns walkway geometry
   │  └──────── generate_ibc_model.py              (ib)   owns IBC stack geometry
   │  └──────── generate_spraybar_model.py         (sb)   owns spray bar + processing tray
   │  └──────── generate_film_plane_mechanism_model.py (fp) owns film-plane geometry
   │  └──────── generate_lighttrap_model.py        (lt)   owns light-trap geometry
   ▼
generate_sketchup_model.py  (overview) = ONLY generate_ruby(): a list of
   component(name, tag, <module>.<builder>()) calls + the shell/context. No geometry authored here.
```

**Invariant after the refactor:** no model imports `generate_sketchup_model` (overview) for
geometry. Overview imports everyone; nobody imports overview. The circular edge is gone.

---

## 4. Phased plan (one subsystem per phase · cascade + verify each before the next)

### Phase 0 — Extract the shared primitives (PREREQUISITE) — ✅ DONE 2026-10-06
Moved `mm`, the material/mute machinery (`_CANON_RGB`, `hex_to_rgb`, `mute_hex`, `shared_mat_name`,
`_MAT_BY_COLOR`, `muted`, `_mute_ctx`, `_CTX_*`), `ruby_box/prism/cylinder/cone_wire/bolt/tri/arc_wall`,
`tilted_slab`, `component()`, `ruby_pipe/flex_duct/coil_cord/elbow/pipe_run/flex_run/tee` + vector
helpers into **`src/models/tbs_draw.py`** (verbatim, AST-extracted). Overview keeps `generate_ruby()` +
the tag/scene machinery + the `C_*` palette (primitives take color as a param) and does
`from tbs_draw import *`. Re-pointed all 11 sub-models `ov.<primitive>` → `draw.<primitive>` (631 refs);
`construction` reads the live `draw._CTX_FORCE`.
- **Result:** 10 of 11 models byte-identical. **Overview changed benignly** — the shared material
  registry unified, consolidating 12 redundant duplicates (same color+alpha, previously split because
  sub-models' import-time `ruby_box = ov.ruby_box` aliases captured a separate registry path):
  **unique materials 103 → 91**, geometry + appearance 100% identical. Bonus: base was at 103, *over*
  the ~100 Sketchfab cap the code targets — Phase 0 brings it back under. Only `overview.skp` re-sent.
- `tbs_draw.py` needs no `dependencies.yml` entry (shared library, no `.skp`/`.png` output).
- **Colors + metadata also moved (2026-10-06, same commit series):** the 38-color 3D palette and the
  model-metadata helpers (`sketchfab_meta_ruby`, `model_uid`, `license_note`, `LICENSE_TEXT`) now live in
  `tbs_draw` too. **All 11 models byte-identical** (no re-send). Sub-models now import overview for
  **only the structural builders** Phase 1 relocates — and `mini-tbs` + `pinhole-disc-holder` already
  import overview for **nothing** (fully decoupled). Phase 1 builder-moves are now clean: a moved
  builder uses only `tbs_draw` (`draw.ruby_*`, `draw.C_*`) + `tbs_constants`, never `ov`.
- **Phase 1 move checklist (per builder):** (1) ensure the target sub-model imports the `tbs_constants`
  it needs (e.g. `ib` has NO `from tbs_constants import` yet — add one); (2) move the def verbatim,
  rewriting bare `C_*`→`draw.C_*`, `ruby_*`→`draw.ruby_*`; (3) re-point every consumer `ov.<b>`→`<sub>.<b>`
  and add the sub-model import (watch the 5-consumer builders like `ibc_stack`); (4) overview late-imports
  the sub-model in `generate_ruby`; (5) `manifest --check` must stay byte-identical (pure relocation).

### Phase 1 — Invert the structural owners (pattern ③ → ①), lowest-risk first
**Progress 2026-10-06 (all byte-identical, no re-sends):**
- ✅ `ibc_stack` → `generate_ibc_model` (`ib.ibc_stack`). True ③ inversion; 5 consumers re-pointed.
- ✅ `spray_bar` → `generate_spraybar_model` (`sb.spray_bar`). Was actually ② — overview's and pw's
  `spray_bar()` were IDENTICAL wrappers over `sb.build_*`; collapsed to one `sb.spray_bar()`.
- ✅ `fans` + `fan_duct` → `generate_electrical_model` (`em.fans` / `em.fan_duct`; em owns the Cct A/B
  fan circuits). overview + construction draw `em.fans()`; the light-trap model draws `em.fan_duct()`.
- ✅ `processing_tray` → `pw` (water). `sb`↔`pw` cycle broken by a late import in `sb.build_tray()`.
- ✅ **Walkway cluster** → `wm`: 14 builders (walkways, right_walkway_cantilever/grate, near/left grates,
  walkway_brackets, ibc_cantilever_arms, fp_combined_corner_plate(s), `_rwk_*`) moved verbatim; wm gained
  48 constants + ruby_prism/cone_wire aliases. 6 consumers re-pointed incl. pw's dynamic `getattr(ov,fn)`.
  Cycles: wm late-imports pw; fp/pw/ib/lt import wm at module (wm imports none of them at module).
- ✅ **Film-plane cluster** → `fp` + `lt`: `film_plane_saddles` + `film_plane_mechanism` → fp (the latter
  was a wrapper over `fp.corner()`); **`panel_pivot` → `lt`** (refinement of the plan — it's the cargo-
  door/hinge-panel swing, lt's domain, built from `lt.axle/fan_b_mount_panel/wall_anchors/frame_hooks`).
- **All 6 Phase 1 moves byte-identical — zero re-sends.** Overview is down from ~60 defs to 18.

**Remaining (beyond the tray+cluster focused pass):**
- **Still-③ with no sub-model owner:** `container_shell`, `far_wall`, `pinhole_assembly`, `optical_cone`,
  `solar_array`, `shelf`, `light_seal`, `light_trap_frame` — decide: a shared `context` home (maybe
  `tbs_draw`) or genuinely overview-level.
- **Phase 2 wrapper collapses (②):** `electrical`/`ep_external_wiring`/`lighting_wiring`/`fan_wiring`/
  `evap_cooler` → one `em` composition; `light_trap_drum`/`cage`/`bay` → `lt` (fix the `cage` double-draw).

**Owner decisions made (2026-10-06):** processing_tray → a **water model (pw)**; fans → **em** (done);
the walkway+film-plane cluster → **one focused group move**.

**`processing_tray` → pw — NOT YET DONE (two gotchas to handle in the focused pass):**
1. **Circular import:** `sb.build_tray()` would need `pw.processing_tray`, but `pw` already imports `sb`
   (for `sb.spray_bar`). Break it with a LATE `import generate_pinhole_water_panel as pw` inside
   `sb.build_tray()` (not module-level).
2. **pw reads constants via `ov.CONSTANT`** (e.g. `ov.PROC_TRAY_YD_NEAR`) — it has NO `from tbs_constants
   import`. So the moved `processing_tray` uses `ov.PROC_TRAY_*`/`ov.tray_floor_z` (matches pw's pattern)
   — ownership moves but a constant-coupling to ov remains. Consider giving pw (and cp) their own
   `tbs_constants` imports as separate hygiene (several sub-models lean on `ov.<CONSTANT>` re-export).
   Consumers to re-point: overview, construction, sb (ghost), wm, fp (`ov.processing_tray` → `pw.`).
- **Findings that reshape the remaining work:**
  - `processing_tray` — owner still undecided (sb already ghosts it via `ov.processing_tray`; consumers:
    overview, sb, wm, fp, construction). Decide owner before the walkway/film-plane moves.
  - `fans`/`fan_duct` — **`fan_duct` is shared by overview's `fans()` AND the light-trap model** (Fan B
    on the hinge panel). So "fans → em" isn't clean; `fan_duct` is a shared builder needing a neutral
    home (or stays a shared owner). Decide owner.
  - `walkways` + `right_walkway_cantilever` + grates + `fp_combined_corner_plate(s)` + the `_rwk_*`
    helpers, and `film_plane_mechanism` + `film_plane_saddles` + `panel_pivot` — a **tightly-coupled
    structural cluster** (shared internal helpers, cross-consumed by wm/fp/ib/overview/construction).
    These should move as a GROUP, not one at a time, and likely want their shared helpers hosted
    cleanly. This is the bulk of remaining Phase 1 and deserves its own focused pass.
  - `container_shell`/`far_wall`/`pinhole_assembly`/`optical_cone` — no dedicated sub-model; candidates
    for a shared `context`/`tbs_draw` home or they genuinely stay overview-level.

For each, MOVE the builder from overview into its sub-model, delete overview's copy, and have
overview + all other consumers import the new owner. Regenerate → reconcile → cascade (see §5).

1. **Spray bar + processing tray → `sb` (spraybar model).** Decide: tray co-owned with the bar in
   `sb`, or a standalone `tray` owner. `processing_tray` has the most consumers (water, walkway,
   film-plane) — pick its owner first, it ripples widest.
2. **IBC stack → `ib`.** `ibc_stack` moves to `generate_ibc_model`; overview imports `ib.ibc_stack`.
3. **Walkways → `wm`.** `walkways`, `right_walkway_cantilever`, `right_walkway_grate` move to
   `generate_walkway_model`; overview + ib + fp import them from `wm`. (Biggest consumer web —
   do after tray so the ordering settles.)
4. **Film plane → `fp`.** `film_plane_mechanism`, `film_plane_saddles`,
   `fp_combined_corner_plate(s)`, `panel_pivot` move to `generate_film_plane_mechanism_model`.
5. **Fans → `em`.** `fans()` (Cct A/B physical fixtures) move to electrical; retire the fan ghosts
   in `em.context()` the same way the LED/safelight ghosts were retired.

**Still-needs-an-owner (decide during Phase 1):** `container_shell` + `far_wall` (container itself
— likely a shared `context`/shell builder in `tbs_draw.py` since every model ghosts a shell);
`pinhole_assembly` + `optical_cone` (no dedicated model — new `pinhole` owner, or leave in overview
as genuinely overview-level geometry).

### Phase 2 — Collapse the electrical + light-trap wrappers (pattern ② → ①)
The fix is one composition, not two:
- Give `em` a single documented aggregator (e.g. `em.electrical_system(scene=...)`) that returns
  the full electrical assembly. **`electrical.skp`'s `generate_ruby()` and overview both call it**,
  so the composition can't diverge. Fold `electrical()`, `ep_external_wiring()`, `lighting_wiring()`,
  `fan_wiring()`, `evap_cooler()` into it (the construction phases keep their phase-scoped slices
  via parameters).
- Same for `lt`: overview's `light_trap_drum/cage/bay/frame()` become one `lt.*` composition call;
  **fix the `drum_frame()` double-draw** here.
- Resolve the reverse edge: move `solar_array` + `shelf` to their proper owner (solar → `em`;
  shelf → a `context`/furniture owner) so electrical stops importing overview.

### Phase 3 — Overview is pure aggregation
`generate_ruby()` is only `component(name, tag, <module>.<builder>(...))` lines + the tag/scene
tables. Add a lint check: **`generate_sketchup_model.py` defines no `ruby_*`/`*_build` geometry
functions** (only `generate_ruby`, scenes, and imports) — so overview can never silently re-grow
an owned builder.

---

## 5. Per-phase verification + cascade protocol (non-negotiable)
Every phase follows the rule set we've been using:
1. Edit the generators; `--save` the `.rb`.
2. `manifest.py --check` → the authoritative stale list (geometry-moving phases will list the
   affected `.skp`; Phase 0 must list **none**).
3. For each stale model, focus-model-first: verify the live doc title → `--send` → render-verify →
   `check_interference.py` **0 crossings** (only the 2 known pre-existing out-of-EP flags) → ALVIN
   saves → CLAUDE `push_sketchfab.py` → next model.
4. `manifest.py --update`; refresh `interference-report.txt` (overview audit).
5. Commit source + `.skp` + `dependencies.yml` together; update `RELEASE.md [Unreleased]`.
6. **A move is only "done" when the moved geometry is byte-identical** (hash-equal) or the diff is
   understood and verified — the point is zero behavior change, pure relocation.

---

## 6. Risks / notes
- **Circular imports:** Phase 0 is the unlock — until the primitives are neutral, moving a builder
  into a sub-model that overview imports would create an import cycle. Do Phase 0 first, confirm
  byte-identical, then proceed.
- **`processing_tray` fan-out:** it's consumed by 4 models; settle its owner before the walkway/
  film-plane moves so they re-point once, not twice.
- **Construction model** composes many of these via phases (`generate_construction_model`); it must
  re-point to the new owners in lockstep each phase (it's in every cascade anyway).
- **Scope discipline:** one subsystem per phase, fully cascaded + committed, before the next — so a
  regression is always isolated to one move.
