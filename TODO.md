<!-- Working/internal tracker — NOT published (not registered in publish.sh). -->
# TODO & Actions — TBS-001

The **single record** of outstanding actions across the project. Review and tick here; add new
items as they arise. Tick `[x]` when done (leave a one-line note), or delete once it's clearly
historical. Detailed sub-trackers are linked where the detail is extensive.

**Completed sub-trackers (for reference):** [editorial review](editorial-review-todo.md) — DONE 49/49.

---

## Manual (Alvin) — Sketchfab re-uploads
_3D models embed as Sketchfab iframes; Alvin re-uploads manually reusing the same model ID._

- [ ] Re-upload the `.skp` models changed recently, same model IDs: **water** (Circuit-C power cabling),
  **electrical** + **overview** (master switch on the EP), **ibc-stack** (metadata/rename).
- [ ] Older pending re-uploads: the **light-trap** interactive DC model (B2 refactor); the
  plumbing-panel-rename re-uploads (overview / ibc-stack).

## Scheduled
- [ ] **Aug 2026** — re-price every part in `parts.py` against current supplier listings (April-2026
  indicative basis). Edit the low/high band → `parts.py --inject` cascades; `costing.py --check-registry`
  re-proves. (Reminder block lives atop `parts.py`.)

## Design / 3D (deferred)
- [ ] **Fan A ↔ IBC clash** — the 1000L stack (top Z2336) buries Fan A's old high exhaust spot; only
  ~52mm headroom. Likely fix: relocate Fan A into the 270mm plumbing-corridor gap.
- [ ] **Evap cooler part is PARKED** — "Portacool Jetstream 110" doesn't exist. Pick a real replacement
  spec (see `component-dimension-audit.md`), then 3D re-send + cost re-sum.
- [ ] **3D electrical pump positions** — still the legacy 2-column layout in `generate_electrical_model.py`
  `_pump_circuit()`; re-org to a single column to match `panel-layout.png` / the 2D sheet4.
- [ ] **Film-plane click-DC** — multi-attribute DC + 2D FPM/FPD diagram redraw (foreshortening geometry).

## Cost / data modeling
- [ ] **Cost-analysis Bucket B** — model the alternative *configurations* (WWT container, itemized
  battery/solar BOM, poly-tray, galvanized grating, electric-upgrade kit) so savings levers 2–5 become
  real subtractions, not roll-ups. (`costing.py:530`; `cost-analysis-report.md` §4.)
- [ ] **Un-registered values audit** — ~35 values restated across ≥3 docs with no `tbs_constants` /
  `facts.yml` owner (59mm door clearance ×8, 97/85 W cooler, 52mm headroom, the 1260/630/430 L cascade…).
  Per candidate: find owner → add constant + fact → wrap the restatements.

## Docs / gallery
- [ ] **Gallery-only diagrams** — ~11 PNGs in `all-diagrams.md` with no owning report; decide
  embed/leave/retire each. Strongest action: `tilt-swing-board-sheet1/2/3` → into `tilt-swing-board-report`.
- [ ] **`tilt-swing-board-analysis.md` §4** — the combined C0–C8 renders duplicate `distortion-renders.md`
  §3 with extra commentary; merge the two docs or point §4 to the gallery. (Inline TODO in the doc.)
- [ ] **`component-dependency-map.md`** — the "Portacool note + See Also" section still open.
- [ ] **`plumbing-report.md` §3.2** — optional light re-review; touched in the master-switch→EP cascade
  but still carries its 2026-06-22 editorial "done" mark.

## Code hygiene
- [ ] **Unused imports** — 215 "imported but unused" warnings across 29 files (nothing broken). Detail +
  file list: [unused-imports-todo.md](unused-imports-todo.md).
- [ ] **`generate_pinhole_water_panel.py:511`** — drawing-helper refactor TODO.

## Paused directions
- [ ] **`ibc-reconfig-v2`** — recorded restart direction for the IBC layout (keep Blue-on-top, capacity
  from 1000L sizing, direct-stack restraint frame, Blue=1600L, plumbing-panel frame also carries the right
  walkway). Not started; v1 `ibc-reconfig` abandoned but kept for cherry-pick.
