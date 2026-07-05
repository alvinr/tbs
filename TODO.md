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
- [x] **③ Design-of-record — DONE.** **Filter** = 3 separate + slotted-angle frame (registry itemized, −$50/−$65). **D-ring count = 8** (Alvin, matches §4.1 + the 4-strap routing): `parts.py` qty 4→8, the **2D frame drawing** now draws 4/tier (8 total, verified on re-render), §9.1 BOM re-injects to 8 ea/$40–70, cost cascaded (+$20/+$35). *(The 3D overview does **not** model D-rings — that code was in the retired dead `ibc_rack()`; the live `cp.tote_restraint()` builds bars + hangers only, so **no overview re-send is needed** for this. See the 2D↔3D-parity follow-up below.)*
- [x] **④ Big cascade repair — DONE (G2/G3).** Drum +50 top-position refs → Z2250 (the drum *body* height correctly stays 2200 — the audit's `DRUM_H` bump was a false positive caught on re-render); RWK arm 405→325, walkway open-area 1,662→1,762, Fan A 2200→2000, F-01 50→5μm, LED 3rd panel, ext-panel-X, drum footprint.
- [x] **⑤ Hand-maintained-table sweep — DONE (G4).** weight-report battery/EP/plumbing rows + battery-Z constant (CG re-injected), ibc §9.3 total, cost-breakdown AmFe supplier/CV/P-05, ventilation Circuit E, fan labels.
- [x] **⑥ Low-severity comment refreshes — DONE (G6).** far-Yd/Z60/6-uprights comments, spraybar Ø8→Ø10, pinhole X=2874→2399, cost bands; + 2D derivations (evap-duct X, shelf evap-Z). *(dead `IBC_WBKT`/`BRACKET_*` constants → folded into the unused-imports cleanup below.)*

### ② Datasheet blockers — work through one by one
_Each needs a call (or a re-source), then the noted cascade. Independent — take them in any order._

- [x] **②·1 Spray skate wheel — DONE.** Re-spec'd to a **solid acetal (Delrin) Ø32×20×Ø10 plain-bore wheel** riding on the existing Ø10 **304 SS** axle — corrosion-immune + self-lubricating, no carbon-steel ball bearings (the ferricyanide/citric wash ruled the uxcell PE-body/steel-bearing part out). Kept the exact design geometry (Ø32×20×10) so **no cost/2D/3D cascade**; dropped the unsupported ≥25 kg rating (actual ~2.6 kg/wheel). Turned from McMaster acetal rod or an equivalent POM plain-bore roller. Every off-the-shelf 32-OD idler was confirmed 40mm-wide + steel-bearing, so a solid plain-bore wheel is the corrosion-safe route (316 SS bearing Ø30×9 was the no-machining alternative but changes geometry + is metal-on-tray).
- [x] **②·2 Film-plane pivot pin — DONE.** Pin was **1″ (25.4mm)** — 0.4mm too big to enter the metric `GIR25-DO` rod-end's **25.0mm** bore. Kept the well-specced metric rod-end and swapped the pin to **Ø25mm × 200mm SS316, slip-fit** (a metric Ø25 SS precision shaft/clevis pin; dropped the wrong McMaster #98173A150 1″ SKU — confirm the 25mm SKU at order). Same $8/qty-8 → no cost cascade; 0.4mm is below drawing resolution → no 2D/3D regen. Fixed the registry + the injected `parts:film` block + both hand-maintained BOM rows (cost-breakdown, analysis doc).
- [ ] **②·3 Evap cooler** — modeled/reported **~51mm oversize** (W & D) vs the **Hessaire MC18M** datasheet (508×254×711); the part was also PARKED on a non-existent "Portacool Jetstream 110." **Confirm the cooler part**, then set `EVAP_W=508` / `EVAP_D=254` (keep `EVAP_H=711`), fix "22×12×28 in"→"20×10×28 in", **regenerate overview + lighttrap 3D → `--send` → re-verify stow clearance**.
- [x] **②·4 Spray saddle strap — DONE.** The report's **2mm** was the right design for a rolling-carriage axle retainer; the *cited part* (Amazon Boxonly stamped conduit clamp) was the flimsy ~0.5mm one. Re-spec'd to a **formed 2mm 304 SS saddle** (bent from McMaster multipurpose-304 flat bar, 2 bolt feet over the Ø10 axle) — matches the report, corrosion-safe, robust. Noted a 304 SS + EPDM **Adel loop clamp** (~3/8–7/16″ ID) as the off-the-shelf alternative. Same cost/qty → no cascade; dropped "conduit-style" from §3.4 wording.
- [x] **②·5 Powerpole connector count — DONE.** Alvin: **one pair per pump** → 4 → **5 pair** (P-01..P-05). +$2 cascaded through the costing WATER "Electrical (wiring only)" line, §5 EXPECTED, and grand total; BOM now 5 pair / $10; all gates green.

---

## Manual (Alvin) — Sketchfab re-uploads
_3D models embed as Sketchfab iframes; Alvin re-uploads manually reusing the same model ID._

- [ ] Re-upload the `.skp` models changed recently, same model IDs:
  - **overview** — master switch on the EP + audit D-rings (sent, verified, **saved + committed**) → **re-upload to Sketchfab**.
  - **ibc-stack** — metadata + audit D-rings (sent, verified, **saved + committed**) → **re-upload to Sketchfab**.
  - **water** — Circuit-C power cabling + audit D-rings + title/description restored (sent, verified, **saved + committed**) → **re-upload to Sketchfab**.
  - **electrical** — master switch on the EP → save + re-upload.
  - **walkway** — audit G3: RWK center-arm reach 405→325 (geometry) → regenerate + `--send` + save + re-upload.
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
- [x] **3D D-rings added — DONE.** Added 8 D-ring cylinders to the shared `cp.tote_restraint()` (4/tier on the front bars, mirroring the 2D). Overview sent + **verified 8 in the live model** (4/4 by tier). Shared function → the **ibc-stack + water** models pick them up on their next send. *(Dead `ibc_rack()` D-ring code left for a future delete.)*

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
