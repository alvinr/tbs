<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
---
name: Tidy labels
description: The repeatable "tidy labels" pass for one diagram/generator — runs the static fixer (tidy_labels.py) for the source-detectable rules, then a rendered crop-zoom pass for the visual rules in skill_label_placement.md, auto-applies both, regenerates, and shows before/after. Invoke when asked to "tidy labels on <diagram>" or before shipping a new/edited diagram.
type: feedback
---

**What this automates:** the round-trip that used to be "I draw → the user hand-fixes labels → I extract a rule." Given one diagram (or its generator), it applies the label-placement rules and shows the result. It has two halves because the rules split two ways — **source-detectable** (deterministic, `tidy_labels.py`) and **visual** (needs a rendered look, done by you). Read `skills/skill_label_placement.md` first — that's the rule set; this skill is the *procedure* that applies it.

**Mode:** auto-apply + show. Apply the safe static fixes and the confident visual fixes, regenerate, then present the before/after render and a summary for review — don't stop for approval on each edit.

**Scope discipline:** one diagram/generator per pass. Regenerating a generator rewrites *its* PNGs only; `git checkout -- diagrams/` any PNG you didn't intend to change (generators that share an output, render-noise). Always drive matplotlib with `/usr/bin/python3`.

---

## The pipeline

### 1. Static half — `tidy_labels.py`
```
/usr/bin/python3 src/generators/tidy_labels.py --check <generator.py>   # see findings
/usr/bin/python3 src/generators/tidy_labels.py --fix   <generator.py>   # auto-apply the safe ones
```
`--fix` auto-applies, offset-free and formatting-preserving:
- **DIM range-suffix** — strips a redundant `(X=a–b)`/`(Yd=…)`/`(Z=n)` from a `draw_dim_*` label (the extension lines already show the span — P7).
- **DIM unit-less** — a bare `f"{expr}"` `draw_dim_*` label → `f"{expr}mm"` (P7).

It **flags** (does not touch) the ones that need judgement — carry these into the visual pass:
- **LEADER range-suffix** — a `(X=…)` on a leader may be a legit part id; decide per case.
- **LEADER spec-sheet** — a ≥3-line leader; move secondary specs (material, size, profile) to the notes block (P1).
- **NOTES hand-wrapped** — a notes list with `"   "` continuation items → pass logical one-string notes + `wrap=` (P8).

It deliberately does **not** judge dimension `offset` (scale-dependent — 3–8 data-units in detail views vs 25–80 mm-first) — that's a visual call.

### 1b. Render-based half — `--overflow` (automates the "off-frame / collision" check)
```
/usr/bin/python3 src/generators/tidy_labels.py --overflow <generator.py>   # render + measure
```
This RENDERS every sheet (monkeypatched `Figure.savefig`, no files written) and measures each text bbox against the axes data limits and its neighbours — the one *visual* failure that is mechanical. It reports, in priority order:
- **OVERFLOW** — a label off the frame **LEFT/RIGHT/TOP/BOTTOM** by >`--tol`% (default 4; `bbox_inches="tight"` absorbs a few %, so only real over-reach trips). This is the deterministic version of the "leaders over-reach — pull the end IN" work in step 3 — fix each by shortening/relocating the leader, wrapping the label narrower, or (for a notes line off the right edge) narrowing the notes `width`/`wrap`.
- **CROWDED** — two DIFFERENT labels overlapping ≥60% of the smaller (`--no-collisions` to skip). bbox-based, so a multi-line label's whitespace can over-report — **advisory**, confirm on the crop-zoom.

Run it before the manual crop-zoom: it hands you the exact labels to fix, so step 3 is spent on *judgement* (which clear pocket, which side) rather than *hunting*. Re-run after fixes until the OVERFLOW list is empty (or every remainder is a deliberate margin note). It needs matplotlib — drive with `/usr/bin/python3`.

### 2. Regenerate
```
/usr/bin/python3 src/generators/<generator.py>
```

### 3. Visual half — render, crop-zoom, apply (this is the part that used to be the "Tidy labels" commits)
Open the PNG and **crop-zoom every label cluster at 2.5–3×** (PIL crop — never judge from the full-frame thumbnail). Walk `skill_label_placement.md`'s self-review gate; the recurring, high-yield checks, in priority order:

1. **Notes box over the drawing?** (P8) — the #1 issue. If it overlaps geometry/ghost, move it to a clear margin; if the frame is full, extend the axis (`Z_LO`/`X_HI`/`PAD_*`) to open a band. After extending an `aspect="equal"` axis, re-tune the notes — the box shrinks and text can overflow. **Fit a notes block with three independent levers, not one:** (a) **position** (the `x,y` origin — move it into the clear band); (b) **width + `wrap`** (the wrap column); (c) **line-spacing** (the `draw_notes` spacing arg). Width trades against height: *widen* to pack each note onto fewer/longer lines and make the block **shorter** (use when there's horizontal room — a real tidy widened one block `2400→3600` to lower it out of a collision), or *narrow* it where the column is tight and pay for it in height. When a block must fit a **short band**, cut the line-spacing hard — the same tidy went spacing `60→24` (with width `2050→1450`) to seat a note list in its strip. Tune all three together and re-render; don't just shove the origin.
2. **Title block** clear of the diagram and notes? (P12)
3. **Leaders** each shortest into the *nearest clear pocket*, tip on the specific material edge, crossing the fewest bodies (P1/P3). Sweep the opposite side before keeping a long one. In practice the machine-placed targets **over-reach** — default long throws that sail past the nearby white space — so most of a tidy is **pulling label ends IN** to land just clear of the feature/neighbours (a real tidy trimmed leader throws `250→200`, `300→150`, `700→575`); occasionally push one **further OUT** to reach a genuinely clear pocket when the near side collides. "Shortest" means *shortest that clears*, not shortest possible.
4. **Text on a hatch/ghost/fill** → white `bbox=LBL_BG`, not just high zorder (P9).
5. **Dimensions** on the open side (`right=`/`above=` toward white space), sensible `offset` for *this* sheet's scale, no `<30mm` gap dimensioned between extension lines (P7).
6. **Collisions / clipping** — labels overlapping each other or running off the axes (**auto-surfaced by `--overflow` in step 1b** — resolve every OVERFLOW; confirm each CROWDED on the crop).
7. Resolve the **flags** from step 1 (spec-sheet leaders → notes; hand-wrapped notes → `wrap=`).

### 4. Re-render and verify
Regenerate, crop-zoom the same clusters again. Fix-then-eyeball — never ship the "final" unlooked-at.

### 5. Show + commit
Present a before/after crop (or the full render) and a one-line summary of what changed. Commit the generator + only its regenerated PNG(s):
```
git add src/generators/<generator.py> diagrams/<its-pngs>.png
git commit -m "tidy labels: <diagram> — <what changed>"
```

---

## Notes
- The static tool is a *floor*, not a ceiling — most of a real tidy is the visual pass. Don't skip step 3 because `--fix` reported "0 flagged."
- If the visual pass keeps hitting a pattern the static tool *could* catch deterministically, add a rule to `tidy_labels.py` (and cross-reference it in `skill_label_placement.md`) so the next pass gets it for free — that's how this pair improves.
- This does not replace `lint.py`/`check_consistency.py`; run those separately for constant/cascade drift.
