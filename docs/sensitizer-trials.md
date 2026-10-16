<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Sensitizer Trials — Cyanotype Coating Solution

**Status: OPEN — trials required before the chemistry bulk order is finalized.**

The per-print cyanotype sensitizer recipe is **not yet pinned down**, and the unknowns
have a large effect on the chemistry budget and the number of prints a given order
yields. This page lists the trials needed to lock the [operating manual](operating-manual.md)
§0.2 / §0.3 / §2.1 recipe and the [master shopping list](master-shopping-list.md) /
[cost breakdown](project-cost-breakdown.md) quantities.

**These can be run post-construction at full scale, or — preferably first — on the
TBS-002 proof-of-concept at small scale** to converge cheaply before
mixing kilograms of chemistry.

---

## Why this matters (not a rounding error)

The active image plane is **<!-- BEGIN fact:film_plane_width_mm -->4,389<!-- END fact:film_plane_width_mm --> × <!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm --> mm = 9.42 m²** and is coated **two wet-on-wet
coats** (§2.5). The per-print chemistry therefore scales as
`coverage (ml/m²) × 2 coats × 9.42 m² × concentration`. Two of those terms are estimates:

- **Coverage (muslin absorption):** sourced at **~120 ml/m²/coat** for cotton
  ([AlternativePhotography / Ruth Brown](https://www.alternativephotography.com/cyanotypes-on-fabric-preparing-the-fabric/):
  medium cotton 140 ml/m of 114 cm = ~123 ml/m²; cross-checked against
  [Jacquard](https://www.dickblick.com/products/jacquard-cyanotype-sensitizer-set/):
  ~473 ml over ~50 8×10 fabric prints = ~183 ml/m²) — but **not yet measured on our
  actual pre-washed muslin.** Plausible range ~100–180 ml/m²/coat.
- **Concentration:** [Ware New Cyanotype](https://www.mikeware.co.uk/mikeware/New_Cyanotype_Process.html)
  is **30 g AmFe : 10 g ferricyanide : 0.1 g ammonium dichromate per 100 ml** — but that
  strength is for **rod-coated paper** (29 ml/m²). Applied at fabric volumes it over-deposits
  ~8× the paper chemistry density, so fabric work runs **Ware's 3:1 ratio at a diluted
  strength.** How dilute (and still give adequate Dmax) is the open question.

**Impact:** these two unknowns set the chemistry order size directly. For the 50-print run the
AmFe order swings **~3× across the concentration tiers** (Lean ⅓-Ware → Rich full-Ware), and
coverage is still unmeasured on our muslin, so the real yield could sit further off still. The
per-tier masses and their cost band live in the [operating-manual §0.2 table](operating-manual.md)
and the [cost breakdown](project-cost-breakdown.md); the trials below pin which tier applies
before the bulk order commits.

---

## Trials

### T1 — Muslin absorption / coverage rate
**Goal:** measure ml/m² per coat on the actual substrate.
- Pre-wash the production muslin twice (remove sizing, per [chemistry-shopping-list §5](chemistry-shopping-list.md)).
- Mount a **1 m² test piece.** Weigh the sensitizer container before and after a single
  controlled brush/roller coat; mass ÷ density (~1.05 g/ml) = ml applied.
- Repeat for the **second wet-on-wet coat** and record the combined ml/m².
- **Output:** confirmed coverage (replaces the ~120 ml/m²/coat estimate).

### T2 — Concentration vs density (the cost driver)
**Goal:** find the **leanest** strength that still gives full shadow density, to avoid
wasting chemistry.
- Mix three strengths at Ware's fixed 3:1 ratio: **Lean ⅓-Ware (10 g AmFe/100 ml),
  Standard ½-Ware (15 g/100 ml), Rich full-Ware (30 g/100 ml).**
- Coat, expose identically (step wedge), develop, and read **Dmax / tonal separation.**
- **Output:** the production concentration tier → fixes per-print AmFe/ferricyanide.

### T3 — Ammonium dichromate contrast level
**Goal:** set the contrast agent for the scene/negative contrast without excess fog/stain.
- Vary dichromate **0.1% (baseline) / 0.2% / 0.4%** of the working volume on otherwise
  identical coats; expose and develop a step wedge.
- **Output:** the production dichromate % (Ware: "increase for more contrast").

### T4 — Single vs double coat
**Goal:** confirm two wet-on-wet coats are needed (vs one) for even density on muslin.
- Compare a single coat against two wet-on-wet coats at the chosen strength.
- **Output:** confirm or revise the ×2 coat assumption (halves/doubles the per-print volume).

### T5 — Exposure calibration at the locked recipe
**Goal:** baseline exposure time in full sun once T1–T4 fix the recipe (feeds operating-manual §3.1).

---

## Acceptance / sign-off

A tier and dichromate level are "locked" when T2/T3 show acceptable Dmax + contrast on the
production muslin, and T1 fixes the coverage. On sign-off, cascade the numbers into
operating-manual §0.2/§0.3/§2.1, the master shopping list, and the cost breakdown, and
mark this page **CLOSED** with the chosen values recorded.

---

## Source References

1. [AlternativePhotography — Cyanotypes on Fabric: Preparing the Fabric (Ruth Brown)](https://www.alternativephotography.com/cyanotypes-on-fabric-preparing-the-fabric/) — fabric coverage rate (~123 ml/m² on medium cotton).
2. [Jacquard Cyanotype Sensitizer Set (Dick Blick)](https://www.dickblick.com/products/jacquard-cyanotype-sensitizer-set/) — coverage cross-check (~183 ml/m² over ~50 8×10 fabric prints).
3. [Mike Ware — The New Cyanotype Process](https://www.mikeware.co.uk/mikeware/New_Cyanotype_Process.html) — AmFe sensitizer chemistry, the 3:1 ratio, and dichromate contrast control.
