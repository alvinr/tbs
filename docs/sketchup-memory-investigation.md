<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
<!-- Supporting software-engineering investigation — NOT a TBS artifact, NOT published
     (not registered in publish.sh / mkdocs.yml / setup_docs.py). Repo-internal record. -->

# SketchUp Memory-Bloat Investigation — TBS models

**Question:** Is memory bloat in SketchUp caused by Ruby variables in our generated
`.rb` not being scoped correctly (leaking across `--send` rebuilds)?

**Answer: No — the variable-scoping hypothesis is falsified end-to-end.** Tested empirically
against the running plugin (SketchUp 2026 / Ruby 3.2.2). The bloat is real but it lives on the
**SketchUp C++ side**: the native allocator high-water-marks and does **not** return freed pages
to the OS — not even after the document is closed. `GC` / `purge_unused` / File>New do **not**
reclaim it; **only quitting/restarting SketchUp** does. Our generated Ruby is well-scoped and
rebuild-clean, and needs no fix. The only action item is workflow (restart cadence during heavy
send sessions). Full evidence below; the narrative preserves the hypothesis → test → result
trail, including one intermediate guess (§5/§6a "File>New clears it") that Test C later refuted.

---

## 1. How the code actually runs

- `sketchup_client.py` sends the **entire** `.rb` (up to 2.6 MB — `construction.rb`) as a
  single `eval_ruby` call. No chunking.
- The plugin (`~/Library/.../Plugins/su_mcp/main.rb:1826`) evaluates it as:
  ```ruby
  binding = TOPLEVEL_BINDING.dup
  result  = eval(params["code"], binding)
  ```
  `TOPLEVEL_BINDING.dup` is the **standard idiom for an isolated binding** (stdlib ERB uses
  it identically). Locals assigned in the eval'd code live in the *dup*, which is GC'd when
  `eval_ruby` returns.

## 2. What our generated Ruby contains (static scan of `src/models/*.rb`)

| Persistent-scope vector | Count | Verdict |
|---|---|---|
| Globals we create (`$foo`) | 0 | `$dc_observers` is **read-only reference** to SketchUp's built-in DynamicComponents global, guarded by `defined?` |
| Top-level constants (`CONST =`) | 0 | none — constants would persist on `Object` forever |
| Top-level `def` | 1 (`def scene` in water.rb) | redefined each send; negligible |
| Instance vars `@foo` | 0 | `@Z160` is a false positive inside a text string |
| `proc` / `lambda` closures | 0 | none |

Every geometry local (`grp`, `face`, `mat`, `defn`, `ents`) is **reused/reassigned**, so even
in a worst-case shared binding only ~12 dangling refs could persist — not a bloat vector.

## 3. Empirical probes against the LIVE plugin (read-only)

Model open: `ibc-stack`. Ruby 3.2.2.

```
local_leaks_into_real_toplevel_within_call : false      ← dup binding isolates locals
cross_call_local                           : "isolated" ← local from prev eval is GONE next call
total_defs        : 854  (840 group + 14 component)
zero_instance_defs: 0        ← purge_unused works; no orphan-definition accumulation
hashnumbered_defs : 0        ← no "#N" name-collision duplicates
heap_live_slots   : 81,652   ← Ruby heap is TINY
total_allocated_objects: 304,266
rss_mb            : 379.1     ← memory is in SketchUp C++, not Ruby objects
```

**Interpretation:** Ruby-side leakage is negligible (81k live slots). The 379 MB RSS is
SketchUp's C++ model. Rebuilds are clean: 0 orphan definitions, 0 dup names.

## 4. Rebuild hygiene already in place (per generator preamble)

- Single `model.start_operation(name, true)` … `model.commit_operation` (one undo entry/send —
  required by Extension Warehouse to avoid flooding the undo stack).
- Idempotent erase: `entities.erase_entities(groups+instances+text)` then
  `model.definitions.purge_unused`.
- Pages erased+re-added; stray layers removed; materials reused by name (`materials[n] || add`).

## 5. Bloat candidates considered (none are variable scope)

_These were the pre-test hypotheses. Tests A/C/D below resolve them: #1 is the mechanism but is
NOT cleared by File>New (Test C); #3 is exonerated (Test D)._

1. **Undo-stack / C++ model-cache accumulation across sends in one session** — *prime suspect.*
   Each `--send` is a new committed operation; SketchUp retains the erased+recreated geometry.
   `purge_unused` does **not** clear it; there is no public "clear undo" API. _(Initial guess: a
   File>New / reopen clears it — Test C shows it does NOT; only a restart does.)_
2. **Large-string eval heap churn** — parsing a 2.6 MB string builds a big transient AST/iseq.
   Ruby heap stays small here, so likely minor, but native malloc arenas can grow without
   returning pages to the OS. (This is what Test A/C ultimately point to.)
3. **DC observer leaks** — only the click-to-build models (`construction.rb`, `lighttrap.rb`,
   `mini-tbs.rb`) touch `$dc_observers.get_latest_class`. Known SketchUp bug class: observers
   not freed after the observed entity is erased. **Exonerated by Test D.**

---

## 6. Test plan (distinguishes the causes)

**Test A — Repeated-send RSS curve (the decisive test).** Re-send ONE model K times (10–20),
recording `ps -o rss` + `GC.stat` after each. Between two of the sends, also call
`GC.start; model.definitions.purge_unused` and re-measure.
- Monotonic climb per send that does **not** drop after GC+purge → C++ side (undo / model
  caches), NOT Ruby. → hypothesis #1.
- Climb that drops after `GC.start` → Ruby retention (would contradict the probes; unexpected).
- Flat → no per-send leak at all (the model just costs what it costs).

**Test B — Isolate eval churn from model build.** In the SAME session, `eval` a ~1 MB throwaway
string that allocates and discards (no model writes) N times; watch RSS. Separates
"parsing/eval big strings" from "building geometry." _(Not run — Tests A/C/D were conclusive.)_

**Test C — Undo confirmation.** After Test A's climb, open a fresh empty model (or File>New)
and re-measure. If it drops back near baseline, the retained memory was the model/undo of the
previous doc.

**Test D — DC observer check (only construction/lighttrap/mini-tbs).** Re-send one of those
K times; watch DC-attributed defs / `$dc_observers` timers / live observers / footprint vs a
non-DC model run the same number of times. A steeper curve for the DC model implicates observer
retention.

## 6a. Test A RESULT (ibc-stack, 12 re-sends, SketchUp 2026 / Ruby 3.2.2)

```
step             rss_mb   d_rss  defs pages  heap_live   total_alloc
baseline          251.2    +0.0   854     5      79,659       337,933
send1             422.3  +171.1   854     5     197,451       706,869
send2             539.3  +117.0   854     5     190,345     1,075,314
send3             641.3  +102.0   854     5     190,623     1,444,040
send4             767.2  +125.9   854     5     252,111     1,812,485
send5             909.0  +141.8   854     5     236,627     2,180,930
send6            1046.6  +137.6   854     5     219,347     2,549,375
after-gc+purge   1030.0   -16.6   854     5     157,680     2,549,753   ← GC+purge barely moves it
send7             848.5  -181.5   854     5     204,943     2,918,479   ← C++ side self-releases
send8             929.0   +80.5   854     5     203,749     3,286,924
send9             887.4   -41.6   854     5     211,294     3,655,369
send10            742.2  -145.2   854     5     217,404     4,023,814
send11            841.7   +99.5   854     5     204,315     4,392,259
send12            954.5  +112.8   854     5     203,074     4,760,704
```

**Reading:**
- **Ruby side is flat & bounded.** `heap_live` oscillates ~158k–252k (never climbs);
  `defs`=854 and `pages`=5 are **constant** every send (purge + page-erase working).
  `total_alloc` rises only because it is a *cumulative lifetime counter*, not live memory.
  → **Zero Ruby-object / variable-scope leak. Hypothesis definitively falsified.**
- **RSS climbs ~+130 MB/send for the first 6 sends** (251 → 1046 MB), then **plateaus and
  sawtooths** between ~742–954 MB (sends 7–12) — it does **not** grow unbounded (per `ps rss`;
  see the Test C caveat — `ps rss` is compression-noisy on macOS, so treat these absolute MB as
  a trend, not exact).
- **`GC.start(full) + purge_unused` reclaimed only 16 MB** of the growth → the memory is in
  **SketchUp's C++ layer, not Ruby.**

## 6b. Test C RESULT — document close does NOT reclaim memory (authoritative)

After Test A, closed `ibc-stack` (Don't Save) → opened a **fresh empty untitled model**
(1 def, 1 entity, 0 pages). Measured with macOS `footprint`/`vmmap` (reliable — not `ps rss`):

```
empty untitled model:
  phys_footprint       : 2554 MB   ← EMPTY model still holds 2.5 GB
  phys_footprint_peak  : 4345 MB   ← session peak
  ps rss               : 1.69 GB
  ruby heap_live       : 203,506 slots (tiny — not Ruby)
```

**This refutes the intermediate "File>New returns to baseline" guess.** Closing the document and
opening an empty one did **not** free the ~2.5 GB. The memory is retained at the **C++ process
level** for the process lifetime — the native allocator holds freed pages rather than returning
them to the OS.

> ⚠️ **`ps rss` (and the Ruby `ps -o rss` probe) is unreliable on macOS** — it excludes
> compressed memory, so it swung 74.8 → 260 → 1689 MB within seconds as macOS compressed/
> decompressed idle pages. **Use `footprint -p PID` / `vmmap --summary` (phys_footprint)** for
> real numbers. The Test A RSS *curve* still shows the accumulation trend correctly, but the
> absolute MB values there are compression-noisy.

## 6c. Test D RESULT — DC observers are NOT the cause

Re-sent a **DC model (lighttrap, 8 dynamic components)** 5× then a **non-DC model
(electrical)** 5×, tracking DC-specific metrics (macOS `footprint` for memory):

```
DC model: lighttrap        foot_mb    d   defs dc_defs timers eobs   t_data
send1..5                  2564→2798  +10..+13  925    8      0     0   ~36k   (all flat)

non-DC model: electrical   foot_mb    d   defs dc_defs timers eobs   t_data
send1..5                  2837→3089  +39..+54  767    0      0     0   ~49k
```

- **`dc_defs` stays 8 across all 5 lighttrap sends** (bounded, not accumulating) and **drops to
  0** the moment electrical replaces it → DC-attributed definitions are **fully cleaned** by the
  erase+`purge_unused` rebuild; they do not leak across sends or model switches.
- **`timer_ids`=0 and `entity_observers`=0 the entire time** — no lingering DC redraw timers, no
  leaked observer objects.
- The DC model's per-send footprint growth is **not steeper** than the non-DC model's — both just
  feed the same general C++ high-water climb from §6b. **DC observers exonerated.**

## 7. FINAL conclusion & mitigations

**What the evidence establishes:**
1. **NOT a Ruby variable-scoping problem.** `TOPLEVEL_BINDING.dup` isolates locals
   (`cross_call_local: "isolated"`), Ruby `heap_live` stays flat (~80k–250k slots) across 12
   sends, we create zero globals/constants/closures. Falsified end-to-end.
2. **The bloat is SketchUp C++ process-level memory retention** — the native allocator
   high-water-marks (peak 4.2 GB) and does **not** return freed pages to the OS, even after
   the document is closed (empty model = 2.5 GB). Driven by repeated full erase+rebuild sends
   (each rebuilds all ~854 groups), plus every large model opened in the session.
3. `GC.start` + `purge_unused` do **not** reclaim it; **document close does not** reclaim it.
   **Only quitting/restarting SketchUp** returns to baseline.

**Mitigations (in priority order):**
- **Restart SketchUp periodically during heavy modeling sessions** — this is the only real
  reclaim. A quit/relaunch before a long batch of re-sends (or after footprint crosses ~3–4 GB)
  keeps it healthy. `footprint -p <pid>` is the gauge.
- **Reduce full-rebuild churn.** Each `--send` erases + rebuilds the ENTIRE model; that
  allocation/free churn is what feeds the high-water-mark. Where we iterate on one subsystem,
  a smaller/targeted model (mini-tbs-style) sends far less. Not worth an incremental-update
  refactor.
- Keep the single `start_operation`/`commit_operation` (already done) — avoids multiplying
  undo entries per send.
- **`materials.purge_unused` — DONE (2026-08-10).** Already standard in 9/11 generators at the
  end-of-build cleanup; added to the two that lacked it (`generate_corridor_water_panel.py`,
  `generate_pinhole_water_panel.py`) so every rebuild self-cleans orphan materials. No-op on
  clean models (0 orphans today) → `water.skp` byte-unchanged, no re-send needed.
- **`layers.purge_unused` — deliberately NOT added.** The 9 generators already do explicit
  `keep_tags`-based tag pruning (e.g. `generate_ibc_model.py`), which is *stricter and safer*:
  `purge_unused` would drop an allow-listed tag that happens to be empty (breaking scene
  visibility) and would *miss* a non-empty stale tag the explicit prune catches. It would
  override author intent, so it is not "insurance" here.
- If a future regression implicates DC observers in `construction/lighttrap/mini-tbs`, add an
  explicit `remove_observer` on erase.

**Our generated Ruby needs no fix.** The action item, if any, is workflow (restart cadence),
not code.

## Appendix — how to reproduce

Probe scripts used (kept out of the repo; recreate as needed):
- **Read-only probes** — one-shot `eval_ruby` via `python3 src/models/sketchup_client.py -c '<ruby>'`
  reporting `GC.stat`, `model.definitions`, binding-isolation checks.
- **Test A** — loop that re-sends a model's `.rb` K times, measuring `ps -o rss` + `GC.stat`
  after each, with a `GC.start; purge_unused` mid-run.
- **Test C** — `footprint -p <pid>` / `vmmap --summary <pid>` on the empty model after File>New.
- **Test D** — re-send a DC model then a non-DC model K times each, tracking `dc_defs`
  (defs with a `dynamic_attributes` dict), `$dc_observers` `@timer_ids`, live
  `Sketchup::EntityObserver` count, and `footprint`.
