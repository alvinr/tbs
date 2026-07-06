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
