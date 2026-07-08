<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Release Log — The Big Shoebox Project (TBS-001)

Version history for the project. Each tagged [GitHub release](https://github.com/alvinr/tbs/releases)
has a dated section below summarizing what changed since the previous release. Versioning is
informal `MAJOR.MINOR` — this is a design + documentation repository, not shipped software.

## How releases work — the gate

Between releases, **jot every notable change under [Unreleased]** as it lands (one bullet per
change). That running list is the source we curate from. **Cutting a release is gated on this
file** — a release must not ship without a changelog entry:

1. Make sure **[Unreleased]** captures everything since the last tag.
2. Promote it: rename `## [Unreleased]` → `## [X.Y] — YYYY-MM-DD` and start a fresh empty
   **[Unreleased]** above it.
3. Commit, tag, and create the GitHub release from that section's notes.

**`bash release.sh X.Y`** automates steps 2–3 (promote → commit → tag → `gh release create`) and
**refuses to proceed if [Unreleased] is empty**, which is what enforces the gate.

---

## [Unreleased]

- **Brochure layout tweaks** — tightened the blank space after section headings (heading `b_margin`
  0.4→0.15 via `TextStyle`, plus a tighter heading line-height in the `HTML2FPDF` subclass), and made a
  subheading stacked directly under a section heading (e.g. `### What` under `## 2.`) sit close too
  (merge stacked-heading fragments + reduce the following heading's top margin); moved the **Daily
  Energy** report into the **Research** section and dropped the **Operating Manual** section from the
  PDF; renamed the TBS-002 nav section **PoC → Design for Educational Use**. 207 → 197 pp.
- **License header on every source file, enforced** — added the SPDX/© header to every `.py`, `.rb`,
  and `.md` that lacked it (generated `.rb` now emit it from their generator's Ruby preamble), and added
  a `lint.py` GATE that blocks any commit where a tracked `.py/.rb/.md` is missing it. New rule in
  CLAUDE.md § License Headers.
- **Copyright de-duplication + source licensing** — removed the visible `*© … GNU AGPLv3*` footer line
  that each report duplicated in its body (the site footer already carries it, now with the version, so
  it was showing twice); and added the hidden SPDX/copyright comment header (`<!-- SPDX-License-Identifier
  … -->`) to every remaining `.md` so each file is licensed at the source regardless of the footer.
- **Version stamp on every page** — the released version now shows on every PDF page (footer:
  copyright left, **v0.2 centered**, chapter/page right) and every site page (footer: copyright left,
  **v0.2** right). It is **derived from RELEASE.md's latest `## [X.Y]` header** — a single source, no
  stored copy: a new `src/generators/tbs_version.py` helper, read by the brochure directly and by the
  site via a build hook (`mkdocs_version_hook.py` → `config.extra.version`, rendered by a footer
  override `overrides/partials/copyright.html`). `release.sh` now also **publishes** the site + brochure
  as part of cutting a release, so promoting RELEASE.md propagates the new version everywhere with no
  extra bump step.
- **Brochure readability + site-matching fonts** — the PDF read dense and used Arial. Now it renders in
  **IBM Plex Sans / IBM Plex Mono** (the mkdocs Material site font), bundled in `src/generators/fonts/`
  (OFL 1.1) with Arial Unicode kept as a per-glyph fallback; and the `write_html` leading (fpdf2's tight
  1.0× default vs the site's ~1.6×) is opened to **1.5×** via a `HTML2FPDF` subclass with a small
  inter-paragraph gap, leaving table/CSS line-heights compact. 195 → 209 pp.
- **3D overview scene + label pass** — reworked the per-subsystem scenes so each reads cleanly: the
  Ventilation scene gains the Fan A/B power cables (own tag) routed back to the EP, drops the
  plumbing-panel pump wiring, and shows only the evap-cooler (Cct E) circuit at the external panel — the
  PV + E-stop runs split onto a new "EP Ext Wiring" tag, kept in the Electrical scene. Labeled-scene
  leaders fixed (Fan B exits the cargo-door end, the filter-skid leader lands on the filters) and the
  solar array is ghosted so the exterior labels read through it.
- **Spray-bar supply hose** — added the flexible coiled feed from BV-05 (90° elbow → coil) up to the
  raised spray-bar feed pole, in both the overview and water models.
- **Spray-bar carriage bolts** — the tray-facing clamp-bolt heads are now drawn **countersunk** (a flush
  frustum seated in the clamp underside, top nut still proud) in the 3D model, matching the 2D detail.
- **Walkway top-rail brackets** — restored the film-plane **top-rail wall-seat saddle brackets**
  (interior back-plate + exterior through-bolted plate, at both the near and far walls) that the walkway
  model had dropped; the bottom rail stays on the shared combined corner plate.
- **Sketchfab material budget** — collapsed near-identical color materials at the RGB level (tight greys
  at Δ≤6 plus a few same-hue pairs at Δ≤10, all imperceptible), dropping the overview from **100 → ~87**
  unique materials so it uploads under the material ceiling.
- **Electrical focus model** — dropped the ghost ceiling so the model orbits freely without it occluding
  the gear, and added the two fan-feed callouts (Cct-A → Fan A at the sealed end; Cct-B → Fan B wall box
  + flex jumper) to the Labeled scene.
- **Stray "perspective" lines removed** — the swept-torus pipe elbow (`followme`) left its arc centerline
  behind as **loose edges** inside every elbow (>1,200 in the water model), rendering as dashed lines all
  over the diagram. The shared `ruby_elbow` helper now erases those after the sweep, and the water build
  also clears stale construction lines / root loose edges on every send.
- **Brochure condensation** — turning the 407-page PDF into a ~200-page funding/validation prospectus,
  with the live docs site remaining the full deep-dive. **Phase 1:** dropped exploratory / superseded /
  internal / gallery docs to web-only via `BROCHURE_EXCLUDE` (**407 → 330**). **Mechanism:** a new
  `<!-- brochure:skip -->…<!-- brochure:endskip -->` marker lets the PDF omit detail sections while the
  website (HTML comments) still renders them in full — **additive, reversible, nothing deleted**. First
  applied to `distortion-renders` (thumbnail tables skipped → **330 → 305**). Design:
  `docs/superpowers/specs/2026-07-07-brochure-condensation-design.md`.
- **Water model cleanup** — the pinhole-wall water model drops the external EP panel + evap cooler, adds
  the spray bar for context, removes the green PV / grey E-stop EP cables, and reconnects the purple
  Cct-C pump feed to the panel's own master switch.
- **Non-destructive Sketchfab metadata** — the in-model metadata stamp is now fill-only-if-blank, so a
  regenerate / re-send never overwrites a model's saved title, description, tags, or stable UID.

## [0.2] — 2026-07-07
- **Electrical Panel Redesign** — the EP was reorganized into a tall narrow **vertical column** (battery
  packs re-stacked vertically, gear above, PV array disconnect dropped to operator reach) to fit the one
  clear wall band between the pinhole, chem shelf, and transport-stay anchors; the layout is formalized
  into `tbs_constants`. The 5026 fuse block and the IP65
  enclosure was corrected to its real datasheet footprint. The overview's EP now **delegates to the electrical model's builders**, eliminating
  the hand-maintained duplicate that kept drifting. Cascaded to the 2D (battery drawn as the stacked pair;
  Sheet-5 panel layout redrawn as the full column) and the weight CG. The near-walkway 500mm **widened
  access band** was then re-worked around the EP + chem shelf. The **EP column relocated left**
  to fit inside it, and the **chem-shelf
  depth trimmed 300→225** for walk-around clearance (275mm past the shelf, 328mm behind the EP).
- **Reconcile part dimensions** - resolved a number of drifts from the actual part dimensions vs. what had been
  codified and drawn in 2d and 3d models. Some parts rectified were evap cooler, skate wheels, film plane pivot, saddle straps etc.
- **Drift-tooling hardening** — added `lint.py --verify-all`, a staging-independent full sweep that
  regenerates every model `.rb` and byte-compares it against the working tree, catching **committed-stale**
  outputs that the staged-diff missing-cascade check can miss; wired it into the `publish.sh` deploy gate.
  Promoted the release-only `check_unused_imports` to a per-commit `lint.py` advisory and cleaned the 14 imports
  the EP re-lay had orphaned.
- **Single-source facts audit** — registered 5 previously-unpoliced system constants as `facts.yml` facts
  (corridor width, container rib spacing, IBC stack height, widened near-walkway, clamp spacing), each a
  `constant:` reference with a tight, verified alias, so a future prose restatement of these now trips the
  drift gate; wrapped the corridor-width restatements in `plumbing-report §3.2` as auto-updating placeholders.
- **Distortion-render de-duplication** — `tilt-swing-board-analysis §4` re-embedded the same nine C0–C8
  combined renders that `distortion-renders §3` (the dedicated gallery) already owns; §4 now points to the
  gallery and keeps only its unique content — the projection model and per-configuration optical analysis
  (renamed "Combined Distortion Analysis").
- **Walkway grating corrected 15mm → 25mm** — the 15mm molded-FRP grate was a **bogus spec**: the thinnest
  molded FRP made is 1"/25mm. Corrected to 25mm; the extra 10mm is absorbed **upward**, verified against the full 56° hinge-panel swing arc (arc only crosses the removable lift-out decks + open tray). Cascaded: film-plane
  bottom rail `RAIL_OFF_BOT` 150→160
  (−10mm image, FP wall anchors move), battery + evap-stow +10mm, grate weight 11→12.7 kg/m²



## [0.1] — 2026-07-03

Initial release of the basic design of all system components, and their integration
