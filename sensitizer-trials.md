# Sensitizer Trials — Cyanotype Coating Solution

**Status: OPEN — trials required before the chemistry bulk order is finalized.**

The per-print cyanotype sensitizer recipe is **not yet pinned down**, and the unknowns
have a large effect on the chemistry budget and the number of prints a given order
yields. This page lists the trials needed to lock the [operating manual](operating-manual.md)
§0.2 / §0.3 / §2.1 recipe and the [master shopping list](master-shopping-list.md) /
[cost breakdown](project-cost-breakdown.md) quantities.

**These can be run post-construction at full scale, or — preferably first — on the
[TBS-002 proof-of-concept](mini-tbs-poc.md) at small scale** to converge cheaply before
mixing kilograms of chemistry.

---

## Why this matters (not a rounding error)

The active image plane is **4499 × 2388 mm = 10.74 m²** and is coated **two wet-on-wet
coats** (§2.5). The per-print chemistry therefore scales as
`coverage (ml/m²) × 2 coats × 10.74 m² × concentration`. Two of those terms are estimates:

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

**Impact:** at the corrected two-coat figures, the planned **8.45 kg AmFe order yields only
~11–32 prints, not 50** (see the operating-manual §0.2 table). Picking the wrong tier mis-sizes
the chemistry order — and its ~$900 cost — by up to **4.6×.**

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
