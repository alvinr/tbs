<!-- Working/internal tracker — NOT published (not registered in publish.sh). -->
# TODO & Actions — TBS-001

The **single record** of outstanding actions across the project. Review and tick here; add new
items as they arise. Tick `[x]` when done (leave a one-line note), or delete once it's clearly
historical. Detailed sub-trackers are linked where the detail is extensive.

**Completed sub-trackers (for reference):** [editorial review](editorial-review-todo.md) — DONE 49/49.

---

## Full audit (2026-07-04) — 53 confirmed findings → [audit-2026-07.md](audit-2026-07.md)
_Multi-agent audit across all subsystems × 5 dimensions (3 high / 28 med / 22 low), every finding independently verified. Verdict: **design is sound — no structural/optical defect**; the debt is documentation cascade-leakage. Full detail + per-finding fixes in the linked report; fix in priority order:_

- [ ] **① 3 high-severity contradictions** — spray-bar feed valve **BV-05 vs BV-02** (water-system report contradicts its own parts list — a wrong valve ID on a flow diagram); **pinhole disc retaining ring** the drawing makes but the report says doesn't exist (decide counterbore vs ring before anyone machines it); **pump protrusion 100 vs 114mm** (2 stale report cells, clearance-relevant).
- [ ] **② Datasheet blockers (settle before POs)** — spray skate wheel (cited part is 40mm wide vs 20mm + PE/carbon-steel bearings corrode in the wash); film-plane pivot pin (1″ won't fit the 25mm rod-end bore); evap cooler modeled ~51mm oversize vs the Hessaire MC18M datasheet.
- [ ] **③ Design-of-record decisions** — filter housings: 3 separate + slotted-angle frame vs 1 integrated combo (gates the BOM / frame hardware / cost); D-ring count 8 vs 4.
- [ ] **④ Big cascade repair (one commit)** — drum +50 lift Z2200→2250 (6 files incl. drawn 2D labels; import `DRUM_H_LT`). Batch the shared-root stragglers: RWK arm 405→325, walkway open-area 1,662→1,762, Fan A 2200→2000, evap resize.
- [ ] **⑤ Hand-maintained-table sweep (no gate polices these)** — weight-report battery/EP/plumbing-panel rows, ibc §9.3 total ($1,280/$2,405), cost-breakdown CV/P-05 cells, ventilation Circuit E (→40A/10AWG), fan labels (3A/40W→5A/60W). Convert to injected placeholders where possible so they can't drift again.
- [ ] **⑥ Low-severity comment refreshes** — stale inline comments (`tbs_constants` far-Yd 1962/570/4429/6.42, spraybar Ø8, Z60, pinhole X=2874, "6 uprights", cost 235–299) — latent seeds for the next cascade.

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
