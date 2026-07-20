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

- **Film-plane parts BOM: leadscrew Option-A → U-channel mechanism** — retired the 11 superseded
  leadscrew SKUs (HGR20 rail+carriage, Acme leadscrew/nut, 8" handwheel, locking collar, HGR15
  cross-slides, rod-end + pivot pin) and swapped in the **built** corner mechanism: 304 U-channel
  depth rails (McMaster 1262T21, $362/6ft), Ruland **USKC12-6-6-SS** U-joint ($276 ea) + nitrile
  boot, McMaster **4040N12** 304 shaft support ($58 ea), 3/8" 304 stub rod (**89535K87**, $13.25/3ft),
  acetal 4-wheel skate, 316 flat-bar Z/X cross-slides + UHMW + gib, cam-lever rail brakes, and the
  304 corner plate. Cascaded across `parts.py`, `costing.py` (§4.1 + EXPECTED), report §7, master
  shopping list, and project-cost-breakdown §4, and swept the leadscrew/handwheel prose from
  funding-proposal / equipment-layout / project-summary / component-dimension-audit. **Film section
  +~$2.9k mid → $6,063–7,039** (U-channel $2,172 + U-joint $1,104 the drivers); grand total →
  $25,462 / $31,531 / $39,476. Skate / cross-slide / cam-clamp are fab estimates — firm at order.
  Cleared 8 of the parts-identity dead-SKU lint warnings.
- **Light-trap door top/bottom seals → strip brush** — the two horizontal door-frame seals the
  swinging panel edge *sweeps across* were changed from a steel seal-lip + EPDM compression to a
  **nylon-filament strip brush** (McMaster 74405T12 brush in an 8813T53 holder): a compression seal
  drags under the sideways sweep, a brush passes the edge through cleanly (same principle as the
  drum-opening brush seals). The panel/drum-box top edge's deliberate ~30mm overlap is now recorded
  as intended bristle engagement, **not** a clash. Cascaded across the light-trap 3D model (seals
  recolored for clarity — medium green = brush, dark green = the EPDM that stays on the verticals /
  cut seals / housing surround), `hinged-panel-report.md` §2.3/§5/§6/§7, `parts.py`, and `costing.py`
  (door §6b +$65/$92/$120). Also landed in the light-trap model: the **removable left film rail is now
  a Panel-Swing DC child** that hides in the transport (swung) position so it can't clash the drum
  surround, and the **SKF 6215 drum bearing width corrected to 25mm** (was drawn 45mm).
- **Film-plane active height FP_H 2138 → 2094mm** — the film-plane top rail was lowered 44mm
  (to raise the top carriage/fittings 25mm clear of the ceiling), dropping the active image top edge
  the same 44mm: active plane 4499×2138 → 4499×2094mm, area 104 → 101 sq ft (9.62 → 9.42 m²).
  The overloaded `RAIL_OFF` (100mm) was split — new `RAIL_OFF_TOP` (144mm) drives the film-plane
  top rail + `BRACE_Z_TOP`, while floor-standing equipment stays on `RAIL_OFF`. Chemistry tiers
  and muslin yardage rescaled with the area; vertical muslin-clip count 15 → 14 (total 90 → 88).
  Cascaded across `tbs_constants` / facts / costing / parts / 2D diagrams / 3D models / docs.

- **`film-plane.skp` reconciled to the current corner mechanism** — the older leadscrew-DC
  model's Option-A hardware (HGR20 rails + Acme leadscrews + rod-ends) replaced by the current
  design (304 U-channel rails + acetal skate + 316 flat-bar X/Z slides + cam clamp + U-joint
  USKC12-6-6-SS + 304 SS corner plate) across every scene — the Overview/No-Container main model
  and all four Corner-detail diagrams — built from one shared `_corner_parts()` helper. The
  click Dynamic Components (swing / rail-slide / swing-arc / rotate-plane) are unchanged.
- **Renamed the articulated-corner 3D model `corner-gimbal` → `film-plane-mechanism`** — the
  `.skp`, `.rb`, generator (`generate_film_plane_mechanism_model.py`), dependency-map key and
  Sketchfab config key all follow; the Sketchfab UID (embed URL) is unchanged.
- **Film-plane spring-clip muslin clamp** — retired the cam-lever design for a spring clip
  (bracket through-bolted to the frame upstand, nuts on the inside; spring jaw presses a neoprene
  pad + the muslin onto the ACM board). Cascaded across constants, parts, costing (cost unchanged),
  the clamp report, and Sheet 6 (Panel A rotated to pinhole-left, Panels C/D reworked).
- **Sheet 9 View B** gained a **4040N12 304 shaft support** clamping the U-joint input stub to the
  X (swing) slide — mirrored into the 3D model at each corner.
- **Sheet 7** rebuilt as a true-scale proportional elevation (frame at its real Z extent, components
  drawn to size); Sheets 3/4/8 scale notes corrected; Sheet 9 relabelled "to scale."
- **Film-plane corner mechanism — U-joint mount is now a 304 SS corner plate** — the U-joint funnels
  the whole corner load into a few bolts, too concentrated for the 6061 angle, so each corner now bolts
  to a **304 stainless corner plate** (steel for the load, stainless for the wet zone + a galvanic match
  to the 303 SS U-joint); the perimeter angle stays expendable 6061. Cascaded across parts/costing
  (film +$72/$100/$128), the 3D film-plane-mechanism, and 2D Sheets 3/8. New **Sheet 9** details the
  frame + ACM ↔ 304 SS corner plate ↔ U-joint ↔ X (swing) slide connection square-on and in section.
- **Film-plane Sheet 6 — muslin clamp corrected to a spring clip** — the muslin attachment was redrawn
  from a cam-lever toggle to a **spring clip**: a fixed jaw bolted to the ALU frame edge (countersunk)
  + a spring-loaded jaw that pinches the muslin against the frame edge, squeeze-to-open (torsion spring
  holds closed). The separate open/closed panel was folded into the main detail as a ghost + swing arc,
  and the plan/elevation panels reworked to match.
- **Film-plane report reconciled to the U-channel corner design** — the report, dependency-map, and
  analysis-doc scope note were rewritten from the superseded leadscrew Option-A prose to the current
  304 U-channel + acetal skate + 316 cross-slide + Ruland U-joint mechanism; the Sketchfab embed now
  points at the film-plane-mechanism model.

- **Film-plane frame + corner L-bracket → expendable anodized 6061** — the wetted-zone film
  structure was clarified as an **expendable** part: a 304 SS swap was evaluated (~+$1,430–1,980,
  +32 kg) and rejected in favor of **anodized 6061-T6** (inspect annually / replace on pitting),
  chosen for weight + cost — anodized Al corrodes slowly in the splash-not-immersed cyanotype zone,
  and the ACM backing carries the flatness. Both the perimeter angle and the corner L-bracket carry
  the caveat; specs updated across parts, the weight-model note, the 3D film-plane-mechanism, and 2D Sheets 3/6.
- **Film-plane Sheet 8 (new)** — a dedicated *frame-corner ↔ cross-slide attachment* detail:
  an assembled elevation (the tilt stack) + a plan (the swing stack) showing how each corner
  hangs off BOTH cross-slides through the single U-joint, with the five bolted joints J1–J5 and
  a fastener schedule. Answers "how does the frame interact with the two slides?".
- **TBS-002 "Mini-TBS" classroom camera** — the proof-of-concept two-box cardboard pinhole
  camera was recast as an educational design (Part I teaching / Part II build) and refined
  throughout: the film plane became a cut-cardboard flap (no foam board), push-pin paper
  mounting, a pin-load-seal-coat-dry coating sequence done by feel in the sealed box (no
  safelight), a single wash tray, a re-centered pinhole, and — the key fix — print extraction
  through the boxes' **own top flaps** (built flaps-up) instead of a custom-cut wall. Added an
  interactive **Sketchfab 3D model** (ghosted boxes joined with grey tape; clickable shutter,
  film-plane panel, and top flaps) embedded in the doc, generated from a new
  `generate_mini_tbs_model.py` with geometry single-sourced from `mini_tbs_constants.py`.

- **Site footer version format** — the footer now reads inline as
  `© 2026 Alvin Richards — Released under GNU AGPLv3. Version v0.3` instead of dropping the bare
  `v0.3` onto its own right-justified line (which wrapped and read oddly). `overrides/partials/copyright.html`.

## [0.3] — 2026-07-09

- **Fix: an arch-broken heavy dep no longer blocks commits** — the weight generator guarded optional
  numpy/matplotlib with `except ModuleNotFoundError`, which does NOT catch a wrong-arch/ABI `dlopen`
  failure (a *bare* `ImportError`), so an arm64 numpy under an x86_64 python crashed the `weight` lint
  gate and blocked check-in. Broadened the guards to `except ImportError` (degrade to the math path),
  added a `lint.py` check that flags the narrow pattern, and documented the rule (CLAUDE.md § Optional
  Heavy Dependencies).
- **2d label cleanup** - pass to clean up messy and unreadable labels on all 2d diagrams
- **IBC report — diagrams inline** — the IBC stacking report embedded its 8 construction sheets only in
  the §8 gallery; each sheet now also appears **inline next to the section it illustrates** (cross-section
  + frame elevations in §3, fastening details in §4, bulkhead ports in §6, internal plumbing in §7),
  matching the other reports. The §8 gallery stays on the site but is `brochure:skip`-ped so the PDF
  shows the inline set only (no double-embed).
- **Brochure reconciliation** — Reduced dead space in the document (e.g. heading spacing, diagram size), removed sections that were not required (e.g. operating manual), followed format style of github site, and general re-organization of the PDF content.
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
- **Electrical focus model** — dropped the ghost ceiling so the model orbits freely without it occluding
  the gear, and added the two fan-feed callouts (Cct-A → Fan A at the sealed end; Cct-B → Fan B wall box
  + flex jumper) to the Labeled scene.
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
