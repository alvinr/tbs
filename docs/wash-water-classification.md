<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Wash-Water Classification

## 1. Purpose

The collected wash water leaves the camera through a hauler, so it has to be classified before it can be
disposed of. This report sets out the regulatory basis for that classification, for the baseline iron-only
chemistry and for the optional ammonium dichromate. The [Water System Report §2](water-system-report.md)
describes the chemistry and how the design acts on these results (DV-02 separation, the disposal route by
chemistry). The one-time measurements that confirm them are [Sensitizer Trials](sensitizer-trials.md) T6
and T7.

---

## 2. The Rules

Waste is classified against two sets of rules. The federal toxicity characteristic
([40 CFR 261.24](https://www.law.cornell.edu/cfr/text/40/261.24)) lists eight metals. A waste with less
than 0.5% filterable solids is its own extract after filtering, so filtered wash water is compared directly
against the limits. California ([22 CCR 66261.24](https://www.law.cornell.edu/regulations/california/22-CCR-66261.24))
applies the federal list plus its own soluble (STLC) and total (TTLC) limits for a longer list of metals,
and a fish-toxicity criterion (96-hour LC50 below 500 mg/L).

| Rule | Chromium limit | Test |
|------|----------------|------|
| Federal toxicity characteristic, D007 (40 CFR 261.24) | 5.0 mg/L | Filtered liquid compared directly |
| California, federal list (22 CCR 66261.24(a)(1)) | 5.0 mg/L | As federal |
| California soluble limit, STLC (22 CCR 66261.24(a)(2)) | 5 mg/L, chromium(VI) and total chromium | Waste Extraction Test; element basis |
| California total limit, TTLC (22 CCR 66261.24(a)(2)) | 500 mg/kg chromium(VI); 2,500 mg/kg total | Not controlling for a dilute liquid |

---

## 3. Baseline (Iron-Only) — Non-Hazardous, Confirmed Once

None of the baseline chemistry's elements (iron, potassium, carbon, nitrogen, oxygen) is on the federal
metal list or California's STLC/TTLC list. Two criteria are not settled by the composition alone:
California's fish-toxicity criterion, and whether the ferricyanide's cyanide counts toward the reactivity
characteristic. Ferricyanide is a tightly bound iron-cyanide complex, not free cyanide, and the stored water
is held below the alkaline range that breaks it down ([Water System Report §2.2](water-system-report.md)).

The collected water is therefore classified **non-hazardous**: both totes go to a liquid-waste hauler or a
wastewater plant that accepts it. A **one-time check** (fish toxicity, cyanide, metals) confirms it: first on
bench-washed muslin before the build, then once on the collected water before the first disposal
([Sensitizer Trials](sensitizer-trials.md) T6). A failure moves the baseline to the hazardous route.

---

## 4. Dichromate Option — Hazardous (D007)

The classification follows from four facts: the dose, where it goes, the dilution, and the limit.

1. **Dose.** The working sensitizer is the muslin coverage (two coats) over the active plane: ~<!-- BEGIN fact:sensitizer_l_per_print -->2.2<!-- END fact:sensitizer_l_per_print --> L per print. At 0.1–0.4% that is <!-- BEGIN fact:dichromate_g_lo -->2.2<!-- END fact:dichromate_g_lo -->–<!-- BEGIN fact:dichromate_g_hi -->8.8<!-- END fact:dichromate_g_hi --> g of dichromate per print. Chromium is 41.3% of (NH₄)₂Cr₂O₇ by mass, so each print carries **<!-- BEGIN fact:cr_g_lo -->0.91<!-- END fact:cr_g_lo -->–<!-- BEGIN fact:cr_g_hi -->3.63<!-- END fact:cr_g_hi --> g of chromium**.
2. **Where it goes.** The wash exists to remove the soluble, unexposed sensitizer, and dichromate is fully water-soluble, so the classification takes all of it into the wash water. Part of the chromium(VI) may be reduced to chromium(III) during exposure. That does not change the result: both limits count chromium as the element, whatever its oxidation state.
3. **Dilution.** Each print sends ~<!-- BEGIN fact:recovered_per_print_l -->83<!-- END fact:recovered_per_print_l --> L of water to the collection totes ([Water System Report §3](water-system-report.md)). Spread over all of it, the chromium is **<!-- BEGIN fact:cr_waste_mg_l_lo -->11<!-- END fact:cr_waste_mg_l_lo -->–<!-- BEGIN fact:cr_waste_mg_l_hi -->43.7<!-- END fact:cr_waste_mg_l_hi --> mg/L**. A single all-Blue print on its own (~<!-- BEGIN fact:first_print_recovered_l -->139<!-- END fact:first_print_recovered_l --> L recovered) reaches <!-- BEGIN fact:cr_first_print_mg_l -->6.5<!-- END fact:cr_first_print_mg_l --> mg/L. Evaporation, which would concentrate it further, is not credited.
4. **Limit.** That is **<!-- BEGIN fact:cr_limit_x_lo -->2.2<!-- END fact:cr_limit_x_lo -->–<!-- BEGIN fact:cr_limit_x_hi -->8.7<!-- END fact:cr_limit_x_hi -->× the 5 mg/L limit**: a federal D007 hazardous waste, and so a California hazardous waste too. For it to pass at the lowest dose, less than <!-- BEGIN fact:cr_washout_breakeven_pct -->45<!-- END fact:cr_washout_breakeven_pct -->% of the chromium would have to leave the print in the wash. No source supports that much retention on the print, so the classification rests on this calculation, not on testing each batch.

**Where the chromium sits.** Wash 1 is the leaching wash and carries most of it; that is why the design
sends wash 1 straight to IBC-4 under this option ([Water System Report §2.3](water-system-report.md)).
IBC-4 is therefore hazardous (D007). How much chromium washes 2 and 3 carry into IBC-3 (Brown) is not
known, so Brown is **hazardous until measured**. A one-time measurement decides it
([Sensitizer Trials](sensitizer-trials.md) T7): a bench test of the chromium in washes 2–3, confirmed once
on IBC-3. Below 5 mg/L, Brown takes the baseline non-hazardous route. At or above it, both totes are
hazardous.

---

## 5. Generator Category

A hazardous waste ships on a manifest with a licensed transporter, and the generator needs an EPA ID
number. The [federal generator category](https://www.epa.gov/hwgenerators/categories-hazardous-waste-generators)
is set by the hazardous waste generated in a calendar month
([40 CFR 262.13](https://www.law.cornell.edu/cfr/text/40/262.13)). The whole collected water counts, not just
the chromium in it. That is an inference: the hazardous waste is the liquid that fails the limit, and none of
the 262.13(c) exclusions fits stored wastewater, but no rule text states it for a dilute wastewater. At
~1 kg/L:

| Hazardous fraction | kg per print | Over 100 kg (very-small ceiling) | 1,000 kg (large-quantity threshold) |
|---|---|---|---|
| IBC-4 only (Brown measured below the limit) | ~<!-- BEGIN fact:wash1_to_waste_l -->46<!-- END fact:wash1_to_waste_l --> | <!-- BEGIN fact:prints_sqg_month_w1 -->3<!-- END fact:prints_sqg_month_w1 --> prints a month | <!-- BEGIN fact:prints_lqg_month_w1 -->22<!-- END fact:prints_lqg_month_w1 --> prints a month |
| Both totes (Brown not measured, or above the limit) | ~<!-- BEGIN fact:recovered_per_print_l -->83<!-- END fact:recovered_per_print_l --> | <!-- BEGIN fact:prints_sqg_month -->2<!-- END fact:prints_sqg_month --> prints a month | <!-- BEGIN fact:prints_lqg_month -->13<!-- END fact:prints_lqg_month --> prints a month |

A full resupply run is ~<!-- BEGIN fact:prints_per_resupply -->15<!-- END fact:prints_per_resupply --> prints, so separating wash 1 keeps a run inside one month below the
large-quantity threshold, provided Brown measures below the limit. Federal rules also allow one planned
"episodic event" per calendar year without changing category, with 30 days' notice and 60 days to ship
([40 CFR 262.232](https://www.law.cornell.edu/cfr/text/40/262.232)). California's adoption of that rule has
not been confirmed.

---

## 6. Source References

- [EPA — 40 CFR 261.24, Toxicity Characteristic](https://www.law.cornell.edu/cfr/text/40/261.24) — chromium (D007) 5.0 mg/L; a waste with under 0.5% solids is its own extract
- [California — 22 CCR 66261.24, Characteristic of Toxicity](https://www.law.cornell.edu/regulations/california/22-CCR-66261.24) — STLC/TTLC for chromium(VI) and total chromium; aquatic toxicity criterion
- [EPA — 40 CFR 262.13, Generator category determination](https://www.law.cornell.edu/cfr/text/40/262.13) — monthly counting basis and exclusions
- [EPA — Categories of Hazardous Waste Generators](https://www.epa.gov/hwgenerators/categories-hazardous-waste-generators) — VSQG / SQG / LQG monthly thresholds
- [EPA — 40 CFR 262.232, Episodic generation](https://www.law.cornell.edu/cfr/text/40/262.232) — one planned event per year, 60 days to ship
- [Mike Ware — The New Cyanotype Process](https://www.mikeware.co.uk/mikeware/New_Cyanotype_Process.html) — sensitizer recipe and dichromate dose
