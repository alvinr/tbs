<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# The Big Shoebox Project — Claude Code Working Instructions

## Project Identity

- **Project name:** The Big Shoebox Project
- **Camera designation:** TBS-001
- **Parts prefix:** ICP-XX (e.g. ICP-01, ICP-02…)
- **Container:** 20ft ISO standard shipping container, 2362mm interior focal depth
- **Image plane:** 4389 × 2094mm active (X=260–4649mm; left edge pulled inboard clear of the pivot hub — 2026-08-11; height mechanism-limited by the corner slides + walkway clearance); container interior 5893 × 2388mm
- **Pinhole:** Ø2.17mm, SS-302 shim, f/1088 (Rayleigh formula, λ=550nm)
- **Site:** https://alvinr.github.io/tbs/

---

## Repository Structure

```
/                        ← project root: .md reports, config files
src/generators/          ← all .py scripts (diagram generators, helpers, setup)
diagrams/                ← generated PNGs and SVGs (output of generators)
skills/                  ← codified drawing and labeling conventions (read before creating diagrams)
published/               ← MkDocs input — auto-populated by publish.sh (gitignored, never edit directly)
published/assets/        ← images — auto-populated by publish.sh
site/                    ← built output — gitignored, never commit
.claude/                 ← Claude session files — never commit
```

**Key config files:** `mkdocs.yml` (nav + theme), `publish.sh` (sync + deploy), `src/generators/setup_docs.py` (one-time setup).

**Skills** (read these before working on diagrams):
- `skills/skill_diagram_structure.md` — coordinate system, view conventions, multi-sheet generator boilerplate, shared helper catalog
- `skills/skill_label_placement.md` — the label/leader/dimension/notes RULE SET (12 principles + self-review gate)
- `skills/skill_tidy_labels.md` — the PROCESS that applies those rules to one diagram: `tidy_labels.py --fix` (static) + a rendered crop-zoom visual pass; invoke when asked to "tidy labels on <diagram>" or before shipping a new/edited diagram
- `skills/skill_plumbing_drawing.md` — pipe drawing conventions, fittings, crossings, flow arrows
- `skills/skill_model_consistency.md` — find 2D↔3D↔docs drift: failure-mode taxonomy + the `check_consistency.py` audit (run after any geometry/design change)
- `skills/skill_report_writing.md` — house style for the report `.md` narrative: prose-vs-single-source-vs-diagram triage, placeholder-first, one-source-of-record (no duplication), no old-vs-new archaeology, source citation, terminology/spelling (read before writing or editing any report)

---

## Workflow: Adding a New Document

1. Write `<name>.md` in the project root.
2. If drawings are needed: write `src/generators/generate_<name>.py` → outputs to `diagrams/<name>-sheet1.png`, `diagrams/<name>-sheet2.png`, etc. (all generated PNGs go into `diagrams/`).
3. Register the `.md` in `publish.sh` → `MD_FILES` array.
4. Register any new `.png` files in `publish.sh` → `DIAG_FILES` array (for generated diagrams) or `IMG_FILES` (for root-only images like logos).
5. Register the `.md` in `src/generators/setup_docs.py` → `MD_FILES` list (controls nav title).
6. Register any new `.png` files in `src/generators/setup_docs.py` → `DIAG_IMAGE_FILES` list (for generated diagrams) or `ROOT_IMAGE_FILES` (for root-only images).
7. **Add every new diagram PNG to `all-diagrams.md`** (the gallery index) under the right section, in sheet order. **This applies to a NEW SHEET added to an EXISTING generator too — not just new documents** (the common miss: `electrical-sheet4/5` and `hingepanel-sheet6` were added to existing generators and never reached the gallery). Audit any time — the output must be empty:
   `comm -23 <(ls diagrams/*.png | xargs -n1 basename | sort -u) <(grep -oE 'assets/[^)]+\.png' all-diagrams.md | sed 's|assets/||' | sort -u)`
8. Add a row to the `INDEX_MD` table in `setup_docs.py`.
9. Add a nav entry to `mkdocs.yml` → `nav:` block.
10. Add a row to `docs/index.md` → Documents table.
11. Run `bash publish.sh` to sync and deploy.
12. Commit all source files together: scripts + `.md` + `.png`.

---

## Drawing Style Conventions

Reuse all helpers from `tbs_drawing.py`:

```python
draw_dim_h(ax, x1, x2, y, label, ...)   # horizontal dimension
draw_dim_v(ax, x, y1, y2, label, ...)   # vertical dimension
draw_cl(ax, x1, x2, y, ...)             # centre line
draw_circle(ax, cx, cy, r, ...)         # circle with centre marks
draw_rect(ax, x, y, w, h, ...)          # rectangle
leader(ax, x1, y1, x2, y2, label, ...)  # leader line + label
bolt_holes(ax, cx, cy, pcd, n, ...)     # bolt hole pattern
hatch_rect(ax, x, y, w, h, ...)        # cross-hatched section
```

**Color palette (white background):**

```python
C_OUT   = "#1A1A1A"   # outlines
C_CL    = "#2060A0"   # centre lines (blue, dashed)
C_DIM   = "#404040"   # dimensions
C_ALUM  = "#C8D8E8"   # aluminum section fill
C_STEEL = "#B0B0B8"   # steel section fill
C_GASKT = "#5A3020"   # gasket/neoprene fill
```

**Title block:** series `TBS-XXX`. Reference `generate_film_plane_mechanism.py` for multi-sheet layout and `title_block()` helper.

**Thin cross-sections:** for plates that are much wider than they are thick, use separate scale functions to avoid unreadable flat sections:

```python
def sx(mm): return mm / 5.0   # horizontal 1:5
def sy(mm): return mm * 1.0   # vertical 1:1 — thickness exaggerated
```
Always annotate: `HORIZONTAL SCALE 1:5 / VERTICAL SCALE 1:1 — thickness exaggerated for clarity`.

---

## Report Style Conventions

- Every engineering claim links to a citable source: peer-reviewed paper, manufacturer datasheet, or textbook.
- **All source references must include hyperlinks** — no bare titles or catalog names without URLs. Format as `[Source Name](URL)` for standards, datasheets, catalogs, books, and papers.
- **When any engineering drawing specification changes** (dimensions, quantities, materials, bolt patterns, etc.), always update the report's parts list, `master-shopping-list.md`, and `project-cost-breakdown.md` in the same commit.
- Shopping lists: 2+ US/SoCal supplier options per major component; include part numbers and current prices.
- Distortion renders: dark background (`PRU_DEEP = "#0F2D5E"`), 800×600px per configuration, 3×3 summary grid as a separate PNG.
- Logo/favicon palette constants live in `generate_logo_final.py` and `generate_favicon.py` — reuse if needed.
- **Use American English spelling throughout** — e.g. "center" not "centre", "color" not "colour", "aluminum" not "aluminium", "analyze" not "analyse".
- **Plywood = standard exterior grade (BC / ACX, exterior glue), NOT marine, unless a part carries a genuine marine / water-immersion load.** Marine ply is ~3–4× the price for no benefit on backboards, mounts, or shirts (e.g. the corridor plumbing panel, Fan-B band). A spec must never drift back to "marine" for a dry/backing use — flag it if it does.
- **Describe the current design only; put design history in a changelog** (the `tbs_constants.py` rev-history header is the pattern). No "Old vs New" comparison tables in a living report — they accumulate stale archaeology.
- **Report narrative house style is codified in `skills/skill_report_writing.md`** (prose-vs-single-source-vs-diagram triage, one-source-of-record / summaries-point-not-restate, source citation, terminology). Read it before writing or editing a report. `python3 src/generators/editorial_lint.py` is a **manual** check (not in the hook) for spelling, bare source links, and raw values that should be placeholders.

---

## Single Source of Truth

Restated numbers drift. Every value that recurs across docs has ONE home; everything else references it.

- **Four value stores, keyed by consumer:** `tbs_constants.py` (geometry/engineering), `parts.py` (the **parts registry** — every purchasable item: qty, type, supplier, low/high cost, verified size, cyanotype chemistry), `costing.py` (money — the scenario cost model), `facts.yml` (registry of prose-restated numbers + regex aliases that police them). **Never put a cost in `facts.yml`; `tbs_constants.py` never imports from `facts.yml`.** (See the `facts.yml` header for the store-selection rule.)
- **`parts.py` is the procurement source of record; `costing.py` is a reconciled scenario layer on top.** The registry owns the firm **low/high** item costs (and generates the master by-type BOM, every report's §Parts-List, the dimension audit, and the cyanotype shopping list — all as `<!-- BEGIN parts:KEY -->` blocks). `costing.py` adds only what the registry deliberately doesn't carry — the **mid** and the **scenario uncertainty bands** (e.g. ventilation/power/transport/permits) — and its section low/high **derive from** `parts.system_total`. The invariant is gated both ways: `parts.py --check` (registry → costing) and `costing.py --check-registry` (each registry-backed section == sum of its registry systems). So a cost can't drift between the BOM and the budget. `parts.py` imports `costing.py` (for the chemistry tier model); `costing.py` only **late-imports** `parts` inside `check_registry()` — keep that direction (no top-level `import parts` in costing).
- **Placeholder-first.** A restated owned value gets a `<!-- BEGIN fact:KEY -->…<!-- END fact:KEY -->` (engineering) or `<!-- BEGIN costing:KEY -->…<!-- END costing:KEY -->` (money) placeholder — *not raw text*, **especially in the fact's owner doc**. The alias scan only POLICES raw values (flags disagreement); a placeholder AUTO-UPDATES on every constant change (`python3 src/generators/facts.py --inject` / `costing.py --inject`), which is what makes a value cascade for free.
- **Derive, don't hardcode.** If a value is computable from existing constants, make it a *computed* constant (e.g. `IBC_CEILING_CLEARANCE_MM = C_HGT - IBC_H_STK_1000`) so it can never drift.
- **Diagram-of-record stays in the diagram.** Exact coordinates/positions a reader would verify by *measuring the drawing* belong in the diagram (and its position tables), not single-sourced as facts. Single-source *system-defining* and *derivable* values; leave detail dims.

---

## Generator ↔ 3D Model Sync

The 2D diagram generators (`src/generators/`) and the SketchUp 3D models
(`src/models/`) both read spatial constants from `tbs_constants.py`, so changes
ripple into both.

- **HARD RULE — models are ALWAYS generated from code; never hand-edit the live model.**
  A `.skp` is a build artifact, not a source of truth. Do **not** move/nudge/transform/delete
  geometry directly in the live model via `eval_ruby` to "fix" a position — that diverges the
  model from the generator and is silently overwritten on the next regen. Every geometry change
  goes in the generating Python (`src/models/*.py`) → regenerate → `--send` → verify → ALVIN
  saves. **`eval_ruby` is for READ-ONLY inspection/verification only** (querying bounds/positions),
  never mutation. If the live model looks wrong, either the code is wrong (fix it) or the model
  is stale (re-send it) — never patch the model by hand.

- **HARD RULE — `--send` ONLY into the matching model's own doc; VERIFY the match first.**
  `--send` clears and rebuilds whatever is in the ACTIVE SketchUp document, so sending model Y into
  model X's doc **clobbers ALVIN's live view**. Before any `--send`, query the live doc and confirm it
  IS the model you are about to send:
  1. Make the code edits and run `--save` (writes the `.rb`, does NOT touch the live doc).
  2. Query the live model (`Sketchup.active_model.title` via `eval_ruby`). **If it matches** the model
     you're sending → you MAY `--send` WITHOUT asking (rebuilding the same model into its own open doc
     is safe — no clobber), then verify (`eval_ruby` read-only). **If it does NOT match** → do NOT send;
     ASK ALVIN to open the right model and wait for confirmation.
  3. Tell ALVIN "clean — save + upload". ALVIN is the SOLE saver: he does File>Save + re-uploads to
     Sketchfab (same model ID).
  4. **ASK him to confirm "saved + uploaded", and only THEN `git commit` the `.skp`.**
  Never send a model into a different model's doc. Recover a clobber by re-sending the model he actually
  had open, then waiting.

- **When a change touches `tbs_constants.py` (or otherwise alters a system
  component's geometry), re-run every SketchUp model that contains the affected
  component** — regenerate, re-send, and re-save it:
  `python3 src/models/generate_sketchup_model.py --save --send` (then commit the
  updated `*.skp` + `*.rb` alongside the diagram/constant change).
- **`dependencies.yml` is the machine source of truth** for the `script → output-file`
  graph (which generator/model writes which PNG / `.skp` / `.rb`). It is validated by
  `lint.py` (so it can't drift) and the per-constant cascade is **computed** from it —
  run `python3 src/generators/lint.py --cascade <CONSTANT>` to see exactly what a change
  re-runs, and the commit-time *missing-cascade* check enforces it. **Add an entry to
  `dependencies.yml` whenever a generator or model is added.**
  - **`--cascade` is the AUTHORITATIVE re-run/re-send list — drive from it, never from grep or memory.**
    It follows the **module-import graph** (fixed 2026-08-03): a model that reuses another module's
    builders (e.g. `generate_pinhole_water_panel.py` → `water.skp` does `import generate_sketchup_model
    as ov` and reuses `ov.processing_tray()`) inherits that module's constant deps even though it never
    names the constant. The old grep-only scan MISSED these — that's how `water.skp` fell out of the
    tray-drain cascade. After ANY constant change: run `--cascade <CONST>`, regenerate/re-send EVERY
    script it lists (including build-to-`.skp`-direct models with no `.rb`), and commit nothing until
    the list is clean. Before publish, also run `lint.py --verify-all` (regenerates every registered
    output; names any direct-`.skp` model to re-send). `component-dependency-map.md`
  now holds the human design rationale (§1 component→constant registry, §3 diagram matrix,
  §3.1 per-model narrative) — keep that updated when a component's design changes.
- Today there is one model (`overview.skp`) containing nearly every component, so
  in practice any `tbs_constants.py` change ⇒ re-run `overview`.
- **Audit for drift** after a geometry/design change (or when asked "does this
  diagram match the 3D model?"): `python3 src/generators/check_consistency.py`.
  It scans for stale literals (old constant values in labels/comments), 2D↔3D
  git divergence, import asymmetry, and part/label gaps. See
  `skills/skill_model_consistency.md`.
- **Cascade checklist for any `tbs_constants.py` value change:** (1) edit the constant;
  (2) facts/costing placeholders auto-fill via `--inject`; (3) regenerate the affected
  models + diagrams and confirm *only the affected sheets changed* (value-identical = no
  change — the `lint.py` missing-cascade check now byte-diffs to prove this); (4) sweep
  prose for raw restatements **and** generator label literals; (5) `lint.py`;
  (6) `check_consistency.py`. **A numeric literal in a generator's label string is a latent
  stale value the constant cascade can miss — reference the constant** (`f"{BLUE_SUPPLY_L}L"`,
  not `"1800L"`). When a value looks stale, verify it against the *subsystem's dedicated
  report* before changing it (the authoritative source, not a summary that may itself be stale).

---

## Key Optical Constants

| Constant | Value | Derivation |
|----------|-------|-----------|
| Focal length | 2362mm | Container interior depth |
| Optimal pinhole Ø | 2.17mm | Rayleigh: d = 1.9√(fλ), λ=550nm |
| f-number | f/1088 | f / d |
| Container interior | 5893 × 2388mm | Full interior face |
| Film plane (active) | 4389 × 2094mm | X=260–4649mm (left edge inboard of the pivot hub, r60 bearing); height = C_HGT − RAIL_OFF_TOP − RAIL_OFF_BOT (top rail lowered 44mm) |
| Pinhole X position | 2454mm | Center of active film plane (260 + 4389/2) |
| Rail left X | 260mm | Left rail / film plane left edge (inboard of the pivot hub; PIVOT_X pinned at 175) |
| Rail right X | 4649mm | Right rail / film plane right edge |
| Rail span | 4389mm | RAIL_X_R − RAIL_X_L |
| Board tilt 5° → image shift | 207mm | 2362 × tan(5°) |
| Film plane max tilt | ±40° | Option A rigid-plane, single-axis (`MAX_TILT_DEG`, cross-slide-Z limit) |
| Film plane max swing | ±28° | Option A rigid-plane, single-axis (`MAX_SWING_DEG`, rail-depth limit ~28.7°) |
| Tilt-swing board max | ±5.3° | Screw shoulder hard stop |

---

## Optional Heavy Dependencies (lint gates run dependency-free)

The value-injection gates (`weight`, `energy`) run their generator under the commit hook's `python3`,
which may not have — or may have an arch/ABI-broken — numpy/matplotlib. Those generators therefore guard
the heavy deps and fall back to a pure-`math` compute path. **Guard optional numpy/matplotlib imports
with `except ImportError`, NOT `except ModuleNotFoundError`.** A dep built for the wrong arch (e.g. an
arm64 numpy `.so` loaded by an x86_64 python) fails `dlopen` with a **bare `ImportError`** that
`ModuleNotFoundError` does not catch — so the "dependency-free" fallback would crash the gate (and block
every commit) instead of degrading. Enforced by the `lint.py` check *"optional dep guards use except
ImportError"*.

---

## Deployment

```bash
bash publish.sh          # sync docs/ + gh-deploy → GitHub Pages
bash publish.sh --local  # local preview: http://127.0.0.1:8000
bash publish.sh --build  # build to site/ only (no push)
```

The script auto-detects whether a git remote is set. If not, it falls back to `--build`.

---

## License Headers

**Every `.py`, `.rb`, and `.md` file MUST carry the SPDX license header.** Enforced by a `lint.py`
GATE (`license headers on every .py/.rb/.md`) that blocks the commit if any tracked file lacks it —
so new files can't ship without it.

- **Python / Ruby** — after the shebang if present:
  ```
  # SPDX-License-Identifier: AGPL-3.0-only
  # © 2026 Alvin Richards
  ```
- **Markdown** — top of file, as HTML comments (hidden on the rendered site):
  ```
  <!-- SPDX-License-Identifier: AGPL-3.0-only -->
  <!-- © 2026 Alvin Richards -->
  ```
- **Generated `.rb`** get the header from their generator's Ruby preamble — edit the generator and
  regenerate, never hand-edit the `.rb`.
- The Markdown header is the *source* protection; the rendered site shows the copyright once, in the
  **footer** (with the version) — do NOT restate it in the body.

## Git

Standing permission to commit and redeploy on every request in this project.

- **HARD RULE — NEVER `git add -A` / `git add -a` / `git add .` / `git add <glob>`, in ANY form, including scoped (`git add -A docs/`).** Always `git add` the explicit list of files you actually changed. Scoped `-A` still sweeps in untracked/unrelated files (it has bitten this repo — `docs/` auto-gen files, the license-header gate). Type the paths.
- Commit all source files together: scripts + `.md` + `.png`.
- Never commit `site/` (gitignored) or `.claude/` session/memory files.
- `docs/` files are auto-generated by `publish.sh` — they can be committed but are not the source of truth.

## Releases

`RELEASE.md` is the curated changelog. **As notable changes land, add a bullet under its `[Unreleased]` section — in the SAME work, not "later."** That running list is what each release summarizes from. Cutting a release is **gated** on it: `bash release.sh <version>` promotes `[Unreleased]` → a dated `## [X.Y]` section, commits, tags, and runs `gh release create` — and **refuses to run if `[Unreleased]` is empty**. Keep `[Unreleased]` current; a release must never ship without a changelog entry.

- **HARD RULE — the `[Unreleased]` obligation carries across sessions; a fresh session does NOT reset it.** Landing notable work without updating `[Unreleased]` is incomplete work, even if the changes are committed. At the **start of any session that will change the project, and again whenever a batch of work lands,** check `[Unreleased]` against the commits since the last `## [X.Y]` section (`git log <last-tag>..HEAD`) and backfill anything missing. Don't let the list drift empty while commits pile up — that's how a release ends up with nothing to summarize.

## Tracking

`TODO.md` is the **single record** of outstanding actions/TODOs (repo-only, not published). Add new items there rather than scattering `# TODO` comments through the code; review and tick them off as they're done. `editorial-review-todo.md` (complete) and `unused-imports-todo.md` are detailed sub-trackers linked from it.
