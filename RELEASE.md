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

- **Walkway grating corrected 15mm → 25mm** — the 15mm molded-FRP grate was a **bogus spec**: the thinnest
  molded FRP made is 1"/25mm (McNichols **MS-S-100**, 1½" square mesh, vinyl-ester, 2.60 lb/sf — validated
  against the datasheet load table; a 100kg operator deflects ~2.5mm at the 457mm span, within the ¼"
  pedestrian limit). Corrected to 25mm; the extra 10mm is absorbed **upward** (Option A: deck `WALKWAY_H`
  130→140, the Z115 bracket arm unchanged), verified against the full 56° hinge-panel swing arc (arc only
  crosses the removable lift-out decks + open tray). Cascaded: film-plane bottom rail `RAIL_OFF_BOT` 150→160
  (−10mm image, FP wall anchors move), battery + evap-stow +10mm, grate weight 11→12.7 kg/m²; ~24 diagrams
  and 7 models regenerated.
- **EP skinny-column reorg** — the EP was reorganized into a tall narrow **vertical column** (battery
  packs re-stacked vertically, gear above, PV array disconnect dropped to operator reach) to fit the one
  clear wall band between the pinhole, chem shelf, and transport-stay anchors; the layout is formalized
  into `tbs_constants`. The overview's EP now **delegates to the electrical model's builders**, eliminating
  the hand-maintained duplicate that kept drifting. Cascaded to the 2D (battery drawn as the stacked pair;
  Sheet-5 panel layout redrawn as the full column) and the weight CG. The near-walkway 500mm **widened
  access band** was then re-worked around the EP + chem shelf: it's now **cantilever-limited to X1055–2169**
  (≤100mm grate overhang past the outer brackets, deflection TBD), the **EP column relocated left to X1829**
  to fit inside it (right edge = the overhang limit; the transport-stay anchor follows), and the **chem-shelf
  depth trimmed 300→225** for walk-around clearance (275mm past the shelf, 328mm behind the EP).
- **Electrical panel (EP) rework** — reworked the EP across the electrical + overview 3D models, the 2D
  electrical diagrams, and the parts/cost/report: the IP65 enclosure box is replaced by an open **plywood
  backing panel** (every component surface-mounts on it — MPPT on a forward sub-panel, fuse block, busbars,
  disconnects, inverter, battery bank); the MPPT is pulled forward clear of the fuse-stack risers; the **PV
  array disconnect** is brought onto the panel and wired **in-line**; both E-stops are wired to the contactor
  coil loop; and the battery DC cables now land on the disconnect terminals. Parts: added
  `ep-backing-panel` (18mm plywood backboard, the mounting surface everything fixes to) alongside the
  retained `ip65-enclosure` (now sealing just the fuse-block/busbar DC terminals, bolted to the plywood);
  electrical subtotal +$60.

## [0.1] — 2026-07-03

Initial release of the basic design of all system components, and their integration
