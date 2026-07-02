<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Archived models

Superseded SketchUp study models — kept for reference, NOT part of the active build
(not in `dependencies.yml`, not re-sent/committed as `.skp`).

- **`generate_right_cantilever_study.py` / `right-cantilever-study.rb`** — the right-walkway
  cantilever-rectangle study model (film-plane Option-A era). Archived 2026-07-02: it drew the
  old single-portal `ibc_rack()` (X4734), not the current deep-box `cp.frame()` (X4654), so it no
  longer matches the as-built design. The adopted design + load check live in the still-active
  decision record **`right-walkway-cantilever-study.md`**, and the built geometry is in
  `walkway.skp` / `overview.skp`. To revive: re-point the frame to `cp.frame()` and fix the
  `import generate_sketchup_model` path (it expects to run from `src/models/`).
