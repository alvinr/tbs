<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Brochure Condensation — Design Spec

**Goal:** shrink `tbs-brochure.pdf` from **407 → ~175 pages**.
**Audience (twofold):** a **funding prospectus** AND enough engineering for **3rd-party design
validation** during funding. The live docs site remains the deep-dive appendix — nothing is deleted,
only removed from the printed PDF.

**Approach:** *Overview prospectus.* The brochure carries the story + specs + one credible report per
subsystem; exploratory / superseded / internal / gallery content moves to web-only; the biggest reports
and galleries are condensed to conclusions.

**Resolved decisions (2026-07-07):** target **~200 pp** (no report merges — every report stays
standalone). Condensation is **brochure-only** — the website keeps the FULL reports.

## Mechanism
- **Drop whole doc → web-only:** add the file to `BROCHURE_EXCLUDE` in `generate_brochure.py`.
- **Condense a section brochure-only:** wrap it in `<!-- brochure:skip -->` … `<!-- brochure:endskip -->`.
  `md_to_html` strips the region from the PDF; the markers are HTML comments so mkdocs renders the full
  content on the site. **Additive + reversible — no content is deleted anywhere.** (No `.md` prose is
  cut; the website is byte-for-byte unchanged in what it *shows*.)

## Phase 1 — Drops — ✅ DONE (2026-07-07): 407 → 330
Added to `BROCHURE_EXCLUDE`: `engineering-diagrams`, `film-plane-mechanism-analysis` (superseded),
`lens-options`, `lens-vs-pinhole-exposure`, `pinhole-option-b-optics`, `container-transport-options`,
`process-comparison`, `tilt-swing-board-analysis`, `right-walkway-cantilever-study`,
`component-dimension-audit`, `cost-analysis-report`. (Already excluded: `component-dependency-map`,
`all-diagrams`.)

## Phase 2 — Galleries + condense-to-conclusions — APPROVED, doc-by-doc
Thin galleries and condense the biggest reports to their conclusions (no prose-quality loss for a
validator; full detail stays on the web).

| Doc | now | target | action |
|---|---|---|---|
| distortion-renders | 26 | ~5 | keep the 3×3 summary grid + 1–2 hero renders; drop the rest |
| processing-tray-and-spray-bar | 31 | ~14 | thin the 17 embedded images to the essential views |
| electrical-report | 25 | ~15 | condense to as-built + key specs; trim derivations |
| walkway-report | 22 | ~14 | condense; thin images |
| film-plane-mechanism-report | 15 | ~10 | condense |
| photosensitive-plane-options | 14 | ~6 | keep the chosen material + brief alternatives table |
| tilt-swing-board-report | 13 | ~8 | condense |
| weight-distribution-report | 13 | ~9 | condense |
| master-shopping-list | 11 | ~8 | summary + link to full web list |
| container-report | 10 | ~7 | condense |
| operating-manual, cost-breakdown, water, plumbing, ibc-stacking, ventilation, hinged-panel, chem-shelves, walkway-routing | — | −~30% | conclusion-first trim |

**Phase 2 budget:** galleries + conclusion-trims land the PDF at **~200–210 pp**.

## Merges — DECIDED: no
Report merges were considered (would reach ~175) but **declined** — every report stays standalone.
Target is **~200 pp**, reached by `brochure:skip` markers on detail sections + gallery thumbnail tables.

## Progress
- ✅ Phase 1 drops → 330.
- ✅ Mechanism (`brochure:skip`) built + proven on `distortion-renders` (26 → 1 pp) → **305**.
- ⏳ Remaining: mark detail/thumbnail regions in `processing-tray-and-spray-bar`, `electrical-report`,
  `walkway-report`, `photosensitive-plane-options`, `film-plane-mechanism-report`, `tilt-swing-board-report`,
  `weight-distribution-report`, `master-shopping-list`, `container-report`, and conclusion-first skips on
  the mid reports. Target ~200.
