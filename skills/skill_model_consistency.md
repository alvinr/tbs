---
name: model-consistency
description: Find and fix drift between the 2D diagram generators, the 3D SketchUp models, and the reports — failure-mode taxonomy, the check_consistency.py audit, and a judgment checklist
metadata:
  type: reference
---

## Purpose

The 2D diagrams (`src/generators/`), the 3D models (`src/models/`), and the
reports (`*.md`) describe the same machine three different ways. They drift.
You **cannot** diff a PNG against a `.skp`, but nearly every real anomaly traces
to one of five root causes — four of which are mechanical. Run this audit after
any geometry/design change, and whenever you're asked "does diagram X match the
3D model?"

**The governing rule:** *geometry lives only in `tbs_constants.py`. Everything
else — every generator, every model builder, every report — references it.* A
dimension written as a literal anywhere else is a latent stale value.

## The five failure modes (from real anomalies)

| # | Cause | Examples we hit | Caught by |
|---|-------|-----------------|-----------|
| 1 | **Hardcoded value** that should read a constant (label/comment/literal) | `Ø750mm` labels, `# = 375mm`, `Yd 806–1556`, `$1,200` drum cost | CHECK A |
| 2 | **Drawing logic didn't follow a design change** (shape, projection, presence of a feature) | 4-fin drum after it went finless; face-on fan vs horizontal axis; un-notched "fork" plate | CHECK D + judgment |
| 3 | **Change applied to one side only** (2D or 3D, not both) | zip-tie loops & top shelf in 3D only; aluminum colour; weight pin | CHECK C + B |
| 4 | **Doc / number staleness** | weights, costs, passage 625→555 | CHECK A |
| 5 | **Latent duplicate** — a constant nobody uses, or a bare literal equal to a constant's *current* value (matches today, the inverse of #1, waiting to drift) | 2D `N_NOZZLES = 26` vs computed `SPRAY_BAR_N_NOZZLES`; `PANEL_H = 2060` vs unused `EQPANEL_H` | CHECK E + `--literals` |

## The audit tool

```bash
python3 src/generators/check_consistency.py          # CHECK A–E
python3 src/generators/check_consistency.py --scan 750,375,1606   # hunt specific old values
python3 src/generators/check_consistency.py --literals           # latent duplicates (noisy)
```

**CHECK A — stale-value scan (the money check).** Recovers every *prior* value of
a changed constant (from `git log -p tbs_constants.py` and inline `was N`
comments), then flags those values appearing in **labels and comments** across
generators, models, `.rb`, and docs. It deliberately skips bare code literals
(a `W+750` offset is almost always coincidental) and skips lines that read as
history (`was`, `replaces the failed`, `rev N`, …) — those are *correct* and must
not be "fixed." Triage each hit: a current dimension that merely equals an old
value (e.g. an `1800mm` person height when `FAN_B_H` used to be 1800) is a false
positive; a label/comment describing the *changed* component is real drift.

**CHECK B — import asymmetry.** For each paired (2D generator, 3D builder), the
constants imported by one side but not the other. Often benign (different views
need different constants), but a *geometry* constant on one side only is worth a
look. Ignore `C_*` colours and `DIAGRAMS_DIR`.

**CHECK C — git divergence.** Commits touching the 3D builder but not its 2D
generator (and vice versa) since they last moved together. A 3D-only commit that
changed geometry/features is the classic "updated one side" drift — this is
exactly how the spray-bar zip-tie loops were found. Read the commit subjects: a
"fix"/"add"/"reflect" on one side with no twin on the other is the signal.

**CHECK D — part/label inventory.** The 3D `ruby_*` part names vs the 2D drawn
labels, side by side. Wording differs, so this is an eyeball aid, not a diff: a
3D part with no plausible 2D counterpart (or vice versa) is a candidate feature
gap. (`Carriage Plate L/R` in 3D vs a single un-notched plate in 2D was this.)

**CHECK E — dead constants (the inverse-drift seedbed).** Constants defined in
`tbs_constants.py` but referenced by no generator or model (and not used to derive
another constant). Each is either design intent nobody draws yet, or a value that
will get hand-copied as a literal later and then silently drift. Two remedies:
**wire it in** (import and use it — e.g. `EQPANEL_H` now feeds `panel_layout`'s
`PANEL_H`), or annotate the definition line `# reserved` (a spec/alias/history
value kept on purpose). CHECK E skips any line whose comment contains *reserved*,
so it only nags on genuinely new orphans.

**`--literals` (opt-in, noisy) — bare literal == a current constant.** The inverse
of CHECK A: a number hardcoded in a generator/model that *equals* a constant's
value **today**. Matches now, drifts on the next geometry change. Most hits are
coincidental (padding, axis limits, RGB tuples, `/1000` unit conversions, `1800mm`
person heights) — triage by line. The real ones are literals that *position, size,
or label that constant's own feature*: those were `N_NOZZLES = 26` (should read
`SPRAY_BAR_N_NOZZLES`) and the `EQPANEL_X`/`C_LEN` values baked into drawn labels
(now `f"…(X={int(EQPANEL_X)})"`). Not run by default because the signal-to-noise
is low; reach for it when hunting a suspected duplicate.

Findings are heuristics, never failures — the script always exits 0.

## Judgment checklist (what grep can't see — failure mode 2)

For the component under review, open the 2D sheet(s) and the 3D model and confirm:

- [ ] **Projection / axis.** A face-on circle in a *plan/section* implies a
      vertical axis; a horizontal-axis part must read **edge-on** in that view.
      (The fan sheets drew the axial fan face-on in a section — wrong.)
- [ ] **Feature presence.** Every distinct 3D feature (a fork notch, a shelf, a
      clamp, zip-ties, a seal) appears in at least one 2D sheet, and vice versa.
- [ ] **Shape, not just label.** If a 2D label says "NOTCHED" / "C-shell" /
      "no fins", the *drawing* actually shows it (the fork plate was labelled
      notched but drawn solid).
- [ ] **Material / finish.** Colour and callouts agree (2D aluminium vs a
      steel-toned 3D drum).
- [ ] **Orientation / mirror.** End-wall views, near/far, exterior/interior all
      point the right way.

## When you find drift

1. **Fix at the source.** If a literal should be a constant, replace it with the
   constant reference so it can't drift again (e.g. `f"Ø{DRUM_D}mm"`, not `"Ø900mm"`;
   import the computed `SPRAY_BAR_N_NOZZLES` rather than re-typing `26`). For a dead
   constant (CHECK E), either wire it in or mark its line `# reserved`.
2. **Keep history notes.** "Replaces the failed Ø750 / 4-fin drum" and dated
   `Redesign basis (rev N)` blocks are correct — leave them.
3. **Regenerate + verify visually.** Re-run the generator; read the PNG. For 3D,
   re-send to SketchUp and confirm in the window.
4. **Cascade per CLAUDE.md.** A geometry/material/spec change updates the report
   parts list, `master-shopping-list.md`, `project-cost-breakdown.md`, and
   `component-dependency-map.md` in the same commit; re-run every model that
   contains the affected component.

See also: [[skill_diagram_structure]], [[skill_label_placement]],
[[skill_plumbing_drawing]], and `component-dependency-map.md` (the 2D↔3D index).
