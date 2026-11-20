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

The active image plane is **<!-- BEGIN fact:film_plane_width_mm -->4,389<!-- END fact:film_plane_width_mm --> × <!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm --> mm = <!-- BEGIN fact:image_area_m2 -->9.19<!-- END fact:image_area_m2 --> m²** and is coated **two wet-on-wet
coats** (§2.5). The per-print chemistry therefore scales as
`coverage (ml/m²) × 2 coats × <!-- BEGIN fact:image_area_m2 -->9.19<!-- END fact:image_area_m2 --> m² × concentration`. Two of those terms are estimates:

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

### T3 — Ammonium dichromate contrast level (dichromate option)
**Goal:** map the contrast range the optional dichromate gives, so the creative choice per print is an informed one. The baseline is iron-only.
- Vary dichromate **0.1% (baseline) / 0.2% / 0.4%** of the working volume on otherwise
  identical coats; expose and develop a step wedge.
- **Output:** the contrast step per dichromate level (Ware: "increase for more contrast"), for the operator's choice.

### T4 — Single vs double coat
**Goal:** confirm two wet-on-wet coats are needed (vs one) for even density on muslin.
- Compare a single coat against two wet-on-wet coats at the chosen strength.
- **Output:** confirm or revise the ×2 coat assumption (halves/doubles the per-print volume).

### T5 — Exposure calibration at the locked recipe
**Goal:** baseline exposure time in full sun once T1–T4 fix the recipe (feeds operating-manual §3.1).

### T6 / T7 — Wash-water checks (one-time)

[Water System Report §2.3](water-system-report.md) classifies the collected wash water by chemistry. Two
results there rest on a one-time measurement: the baseline (iron-only) water is non-hazardous (T6),
and Brown is hazardous under the dichromate option until measured (T7). Both run first as a
**bench test alongside T1**, on 1 m² muslin pieces, so the disposal route is known before the
container is built. Each is then confirmed once on the real totes.

**Bench scale.** One full-plane wash floods ~<!-- BEGIN fact:wash_l_per_m2 -->6.2<!-- END fact:wash_l_per_m2 --> L per m² of image
area. Coating a 1 m² piece at the production coverage and washing it in three successive baths of
that volume gives wash water at the **same concentrations as full scale**, so the bench results
compare directly against the limits.

**Bench procedure (both tests).**
1. Coat each 1 m² piece of pre-washed production muslin at the T1 coverage (two wet-on-wet coats)
   and let it dry. Use the T2 tier in use.
2. Expose the piece to full sun for the baseline exposure time, uncovered. A full exposure is the
   realistic case: it converts sensitizer to image, and part of the dichromate is reduced.
3. Wash in **three separate baths** of ~<!-- BEGIN fact:wash_l_per_m2 -->6.2<!-- END fact:wash_l_per_m2 --> L each, 5 minutes each, with
   gentle agitation, in clean polyethylene tubs. Keep each bath's water separate.
4. Record the bath volumes, the sensitizer mass applied (weighed, as in T1) and the dichromate %.

#### T6 — Baseline (iron-only) wash water

**Goal:** confirm the baseline wash water is not hazardous under the criteria §2.3 leaves
unassessed.
- **Sample:** combine baths 1–3 from a baseline piece in proportion. That mixture is the collected
  water (both totes, before any recycling).
- **Analyses:**
  - **96-hour acute fish bioassay**, California criterion: hazardous if LC50 < 500 mg/L
    ([22 CCR 66261.24(a)(6)](https://www.law.cornell.edu/regulations/california/22-CCR-66261.24)).
    The method is the Department of Fish and Game's *Static Acute Bioassay Procedures for Hazardous
    Waste Samples* (1988), incorporated by reference in
    [22 CCR 66260.11](https://www.law.cornell.edu/regulations/california/22-CCR-66260.11).
  - **Total and free cyanide.** Tell the lab the matrix contains potassium ferricyanide: it is a
    complexed cyanide, and an oxidizer.
  - **Title 22 metals panel** (STLC metals) on the filtered sample, which covers anything picked up
    from the tray or water supply.
  - **pH**, for the corrosivity characteristic.
- **Pass:** LC50 ≥ 500 mg/L, no listed metal at or above its STLC, and pH between 2 and 12.5. The
  cyanide result goes on the waste profile.
- **Confirmation:** after the first baseline prints in the container, sample IBC-4 (and IBC-3 if it
  is to be pumped out) once, for the same panel, before the first disposal.
- **Output:** the non-hazardous classification on record for the liquid-waste hauler or wastewater
  plant. A failure moves the baseline to the hazardous route, and §2.3 is revised.

#### T7 — Dichromate option: chromium split between washes

**Goal:** find how much chromium washes 2 and 3 carry, which decides whether Brown can leave the
hazardous route, and check §2.3's assumption that all the dichromate washes out.
- **Sample:** one 1 m² piece coated with dichromate at the **highest level in use** (from T3). Bath 1
  goes to IBC-4 in operation, so it is analyzed on its own. Baths 2 and 3 are analyzed **separately
  and as a proportional mix**, since that mix is what reaches Brown.
- **Analyses:** total chromium on the filtered water (federal D007 and California STLC, both
  5 mg/L), plus chromium(VI). Filtering through a 0.6–0.8 µm glass-fiber filter is how a liquid
  waste with less than 0.5% solids is tested
  ([EPA Method 1311 §2.1](https://www.epa.gov/sites/default/files/2015-12/documents/1311.pdf)).
- **Pass (Brown non-hazardous):** the bath 2+3 mix is **below 5 mg/L with margin** (target ≤
  2.5 mg/L). In full-scale terms, washes 2–3 may carry at most ~<!-- BEGIN fact:brown_cr_max_g -->0.47<!-- END fact:brown_cr_max_g --> g
  of chromium per print (5 mg/L over the ~<!-- BEGIN fact:brown_in_l_per_print -->93<!-- END fact:brown_in_l_per_print --> L they send to Brown).
  That is <!-- BEGIN fact:brown_cr_max_pct_lo -->52<!-- END fact:brown_cr_max_pct_lo -->% of the chromium at a 0.1% dose, but only
  <!-- BEGIN fact:brown_cr_max_pct_hi -->13<!-- END fact:brown_cr_max_pct_hi -->% at 0.4%.
- **Mass balance:** the chromium in baths 1–3 together, compared with the dichromate applied, gives
  the washout fraction. The §2.3 classification holds as long as more than <!-- BEGIN fact:cr_washout_breakeven_pct -->45<!-- END fact:cr_washout_breakeven_pct -->% washes out.
- **Confirmation:** after a run of dichromate prints, sample IBC-3 once for total chromium. Re-test if
  the dichromate level or the wash sequence changes.
- **Output:** the Brown route under the dichromate option, and the measured washout fraction.

#### Sampling and lab handling

Use a lab accredited by California's [Environmental Laboratory Accreditation Program](https://www.waterboards.ca.gov/drinking_water/certlic/labs/)
(ELAP) for the analyses, and confirm the sample volume each test needs before the bench run. The fish
bioassay needs the most volume, so scale the test area up if needed. Containers, preservation and
holding times follow [40 CFR 136.3 Table II](https://www.law.cornell.edu/cfr/text/40/136.3):

| Analysis | Container | Preservation | Max hold |
|----------|-----------|--------------|----------|
| Metals, incl. total chromium | Plastic or glass | Nitric acid to pH < 2 (may be added at the lab, ≥ 24 h before analysis) | 6 months |
| Chromium(VI) | Plastic or glass | Cool ≤ 6 °C; ammonium sulfate buffer to pH 9.3–9.7 (EPA 218.6) | 28 days |
| Cyanide, total and free | Plastic or glass | Cool ≤ 6 °C; NaOH to pH > 10; reducing agent if an oxidizer is present | 14 days |
| Fish bioassay | Per the lab | Cool, unpreserved | Per the lab |

---

## Acceptance / sign-off

A tier is "locked" (and the dichromate contrast range mapped) when T2/T3 show acceptable Dmax + contrast on the
production muslin, and T1 fixes the coverage. On sign-off, cascade the numbers into
operating-manual §0.2/§0.3/§2.1, the master shopping list, and the cost breakdown, and
mark this page **CLOSED** with the chosen values recorded.

The wash-water checks close separately. T6 and T7 close on their bench results plus the one-time
confirmation on the totes. Their results go into [Water System Report §2.3](water-system-report.md)
and the manual's disposal steps (§5.1.1).

---

## Source References

1. [AlternativePhotography — Cyanotypes on Fabric: Preparing the Fabric (Ruth Brown)](https://www.alternativephotography.com/cyanotypes-on-fabric-preparing-the-fabric/) — fabric coverage rate (~123 ml/m² on medium cotton).
2. [Jacquard Cyanotype Sensitizer Set (Dick Blick)](https://www.dickblick.com/products/jacquard-cyanotype-sensitizer-set/) — coverage cross-check (~183 ml/m² over ~50 8×10 fabric prints).
3. [Mike Ware — The New Cyanotype Process](https://www.mikeware.co.uk/mikeware/New_Cyanotype_Process.html) — AmFe sensitizer chemistry, the 3:1 ratio, and dichromate contrast control.
4. [California — 22 CCR 66261.24, Characteristic of Toxicity](https://www.law.cornell.edu/regulations/california/22-CCR-66261.24) — STLC limits and the 96-hour LC50 < 500 mg/L fish-toxicity criterion (T6, T7).
5. [California — 22 CCR 66260.11, References](https://www.law.cornell.edu/regulations/california/22-CCR-66260.11) — incorporates the Department of Fish and Game *Static Acute Bioassay Procedures for Hazardous Waste Samples* (1988).
6. [EPA SW-846 Method 1311 (TCLP)](https://www.epa.gov/sites/default/files/2015-12/documents/1311.pdf) — §2.1: a waste under 0.5% solids, filtered through a 0.6–0.8 µm glass-fiber filter, is its own extract.
7. [40 CFR 136.3 Table II](https://www.law.cornell.edu/cfr/text/40/136.3) — containers, preservation and holding times for metals, chromium(VI) and cyanide.
8. [California ELAP](https://www.waterboards.ca.gov/drinking_water/certlic/labs/) — the state's environmental laboratory accreditation program.
