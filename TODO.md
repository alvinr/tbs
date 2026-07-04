<!-- Working/internal tracker — NOT published (not registered in publish.sh). -->
# TODO & Actions — TBS-001

The **single record** of outstanding actions across the project. Review and tick here; add new
items as they arise. Tick `[x]` when done (leave a one-line note), or delete once it's clearly
historical. Detailed sub-trackers are linked where the detail is extensive.

**Completed sub-trackers (for reference):** [editorial review](editorial-review-todo.md) — DONE 49/49.

---

## Full audit (2026-07-04) — 53 confirmed findings → [audit-2026-07.md](audit-2026-07.md)
_Multi-agent audit across all subsystems × 5 dimensions (3 high / 28 med / 22 low), every finding independently verified. Verdict: **design is sound — no structural/optical defect**; the debt is documentation cascade-leakage. Full detail + per-finding fixes in the linked report; fix in priority order:_

_**Progress (2026-07-04):** the mechanical debt is cleared — buckets ④⑤⑥ DONE (commits G1–G6, all gates green, pushed). Remaining are the items that need a **decision or a datasheet**, not a wording fix._

- [~] **① 3 high-severity contradictions — 2 of 3 DONE (G1):** BV-05 valve fixed, pump 100→114 fixed. **Open (decision):** the **pinhole disc retaining ring** — the drawing makes a part the report says doesn't exist; decide counterbore vs ring before anyone machines it.
- [ ] **② Datasheet blockers (settle before POs)** — spray skate wheel (cited part is 40mm wide vs 20mm + PE/carbon-steel bearings corrode in the wash); film-plane pivot pin (1″ won't fit the 25mm rod-end bore); evap cooler ~51mm oversize vs Hessaire MC18M (resize → 3D re-send → stow re-verify); spray saddle strap 2→0.5mm (0.5mm structurally thin — re-source vs match); Powerpole connector count 4 vs 5 (wiring-design dependent).
- [ ] **③ Design-of-record decisions** — filter housings: 3 separate + slotted-angle frame vs 1 integrated combo (gates the BOM / frame hardware / cost); D-ring count 8 vs 4.
- [x] **④ Big cascade repair — DONE (G2/G3).** Drum +50 top-position refs → Z2250 (the drum *body* height correctly stays 2200 — the audit's `DRUM_H` bump was a false positive caught on re-render); RWK arm 405→325, walkway open-area 1,662→1,762, Fan A 2200→2000, F-01 50→5μm, LED 3rd panel, ext-panel-X, drum footprint.
- [x] **⑤ Hand-maintained-table sweep — DONE (G4).** weight-report battery/EP/plumbing rows + battery-Z constant (CG re-injected), ibc §9.3 total, cost-breakdown AmFe supplier/CV/P-05, ventilation Circuit E, fan labels.
- [x] **⑥ Low-severity comment refreshes — DONE (G6).** far-Yd/Z60/6-uprights comments, spraybar Ø8→Ø10, pinhole X=2874→2399, cost bands; + 2D derivations (evap-duct X, shelf evap-Z). *(dead `IBC_WBKT`/`BRACKET_*` constants → folded into the unused-imports cleanup below.)*

---

## Manual (Alvin) — Sketchfab re-uploads
_3D models embed as Sketchfab iframes; Alvin re-uploads manually reusing the same model ID._

- [ ] Re-upload the `.skp` models changed recently, same model IDs: **water** (Circuit-C power cabling),
  **electrical** + **overview** (master switch on the EP), **ibc-stack** (metadata/rename),
  **walkway** (audit G3: RWK center-arm reach 405→325 — geometry change, needs regenerate + `--send` + re-save).
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
