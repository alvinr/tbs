<!-- Working/internal tracker — NOT published (not registered in publish.sh). -->
# TODO & Actions — TBS-001

The **single record** of outstanding actions across the project. Review and tick here; add new
items as they arise. Tick `[x]` when done (leave a one-line note), or delete once it's clearly
historical. Detailed sub-trackers are linked where the detail is extensive.

**Completed sub-trackers (for reference):** [editorial review](editorial-review-todo.md) — DONE 49/49.

---

## Full audit (2026-07-04) — 53 confirmed findings → [audit-2026-07.md](audit-2026-07.md)
_Multi-agent audit across all subsystems × 5 dimensions (3 high / 28 med / 22 low), every finding independently verified. Verdict: **design is sound — no structural/optical defect**; the debt is documentation cascade-leakage. Full detail + per-finding fixes in the linked report; fix in priority order:_

_**✅ COMPLETE (2026-07-05):** all 53 findings resolved and pushed — G1–G6 (cascade/table/comment sweeps), ①·pinhole ring + ③·filter + D-ring (design decisions), and every ② datasheet blocker (wheel, pin, saddle, Powerpole, evap). All gates green throughout. (Sketchfab re-uploads are Alvin's standing manual step — not tracked here.)_

- [x] **① 3 high-severity contradictions — DONE.** BV-05 valve, pump 100→114, and the **pinhole disc retaining ring** — Alvin chose the **ring** (more serviceable): report §4/§9 rewritten, plate-drawing threaded-bore callout (M52×0.75), registry + cost (+$15/$25 optics) all reconciled, gates green.
- [x] **② Datasheet blockers — DONE.** All five settled (see ②·1–5 below): spray skate wheel, film-plane pivot pin, evap cooler, spray saddle strap, Powerpole count.
- [x] **③ Design-of-record — DONE.** **Filter** = 3 separate + slotted-angle frame (registry itemized, −$50/−$65). **D-ring count = 8** (Alvin, matches §4.1 + the 4-strap routing): `parts.py` qty 4→8, the **2D frame drawing** now draws 4/tier (8 total, verified on re-render), §9.1 BOM re-injects to 8 ea/$40–70, cost cascaded (+$20/+$35). *(The 3D overview does **not** model D-rings — that code was in the retired dead `ibc_rack()`; the live `cp.tote_restraint()` builds bars + hangers only, so **no overview re-send is needed** for this. See the 2D↔3D-parity follow-up below.)*
- [x] **④ Big cascade repair — DONE (G2/G3).** Drum +50 top-position refs → Z2250 (the drum *body* height correctly stays 2200 — the audit's `DRUM_H` bump was a false positive caught on re-render); RWK arm 405→325, walkway open-area 1,662→1,762, Fan A 2200→2000, F-01 50→5μm, LED 3rd panel, ext-panel-X, drum footprint.
- [x] **⑤ Hand-maintained-table sweep — DONE (G4).** weight-report battery/EP/plumbing rows + battery-Z constant (CG re-injected), ibc §9.3 total, cost-breakdown AmFe supplier/CV/P-05, ventilation Circuit E, fan labels.
- [x] **⑥ Low-severity comment refreshes — DONE (G6).** far-Yd/Z60/6-uprights comments, spraybar Ø8→Ø10, pinhole X=2874→2399, cost bands; + 2D derivations (evap-duct X, shelf evap-Z). *(dead `IBC_WBKT`/`BRACKET_*` constants → folded into the unused-imports cleanup below.)*

### ② Datasheet blockers — work through one by one
_Each needs a call (or a re-source), then the noted cascade. Independent — take them in any order._

- [x] **②·1 Spray skate wheel — DONE.** Re-spec'd to a **solid acetal (Delrin) Ø32×20×Ø10 plain-bore wheel** riding on the existing Ø10 **304 SS** axle — corrosion-immune + self-lubricating, no carbon-steel ball bearings (the ferricyanide/citric wash ruled the uxcell PE-body/steel-bearing part out). Kept the exact design geometry (Ø32×20×10) so **no cost/2D/3D cascade**; dropped the unsupported ≥25 kg rating (actual ~2.6 kg/wheel). Turned from McMaster acetal rod or an equivalent POM plain-bore roller. Every off-the-shelf 32-OD idler was confirmed 40mm-wide + steel-bearing, so a solid plain-bore wheel is the corrosion-safe route (316 SS bearing Ø30×9 was the no-machining alternative but changes geometry + is metal-on-tray).
- [x] **②·2 Film-plane pivot pin — DONE.** Pin was **1″ (25.4mm)** — 0.4mm too big to enter the metric `GIR25-DO` rod-end's **25.0mm** bore. Kept the well-specced metric rod-end and swapped the pin to **Ø25mm × 200mm SS316, slip-fit** (a metric Ø25 SS precision shaft/clevis pin; dropped the wrong McMaster #98173A150 1″ SKU — confirm the 25mm SKU at order). Same $8/qty-8 → no cost cascade; 0.4mm is below drawing resolution → no 2D/3D regen. Fixed the registry + the injected `parts:film` block + both hand-maintained BOM rows (cost-breakdown, analysis doc).
- [x] **②·3 Evap cooler — DONE.** MC18M was modeled 22×12×28in (559×305×711); official Hessaire spec is **20×10×28in (508×254×711)** — web-verified (the 22×12 was a retailer overstatement). `EVAP_W 559→508`, `EVAP_D 305→254`. Same part/$130/85W → **no cost or weight cascade**. Stow re-verified (X1450–1958, 51mm roomier). Constants + 2D + reports committed; **overview + electrical 3D re-sent, verified (cooler box 508×254×711), saved + committed.** *(Part identity was already Hessaire MC18M since 2026-06-15 — the "Portacool" note was stale.)*
- [x] **②·4 Spray saddle strap — DONE.** The report's **2mm** was the right design for a rolling-carriage axle retainer; the *cited part* (Amazon Boxonly stamped conduit clamp) was the flimsy ~0.5mm one. Re-spec'd to a **formed 2mm 304 SS saddle** (bent from McMaster multipurpose-304 flat bar, 2 bolt feet over the Ø10 axle) — matches the report, corrosion-safe, robust. Noted a 304 SS + EPDM **Adel loop clamp** (~3/8–7/16″ ID) as the off-the-shelf alternative. Same cost/qty → no cascade; dropped "conduit-style" from §3.4 wording.
- [x] **②·5 Powerpole connector count — DONE.** Alvin: **one pair per pump** → 4 → **5 pair** (P-01..P-05). +$2 cascaded through the costing WATER "Electrical (wiring only)" line, §5 EXPECTED, and grand total; BOM now 5 pair / $10; all gates green.

---

## Scheduled
- [ ] **Aug 2026** — re-price every part in `parts.py` against current supplier listings (April-2026
  indicative basis). Edit the low/high band → `parts.py --inject` cascades; `costing.py --check-registry`
  re-proves. (Reminder block lives atop `parts.py`.)

## Design / 3D (deferred)
- [x] **Overview / assembly-overview / electrical-diagram corridor-filter staleness — DONE.**
  assembly-overview (relabel corridor zone → pumps+ACC, ADD pinhole-wall Filter panel zone, legend) and
  electrical-diagram (every "pumps+filters" → "water pumps"; P-01/03/04/05 corridor + P-02 wall) fixed.
  **Overview needed no change** — its `F1_Z`/`F2_Z`/`F3_Z` usage is in the dead `equipment_panel`/
  `water_plumbing` functions (zero call sites; "safe to delete"), and the live overview already draws
  the pinhole-wall design via `cp.*`/`pw.*`. *(Optional future cleanup: delete those dead functions,
  which would also retire the legacy `FSKID_X`/`F1_Z`/`F2_Z`/`F3_Z` constants.)*
- [ ] **EP (Electrical Panel) interior needs a rework — 2D + 3D.** The IP65 enclosure internals —
  the A–G blade-fuse stack, the +/− busbars, and the wiring/circuit routing — have accreted to the
  point they're **not operator-usable**: fuses/terminals are cramped and hard to reach/trace for
  service and reset. Re-lay the internal layout for real serviceability (fuse access, labeled
  terminals, wire runs, clearances) and cascade it through the 3D (`electrical.skp` `power_core()`
  + the duplicated overview `ov.electrical()`) and the 2D (`generate_electrical_diagram.py` Sheet 5
  enclosure elevation + fuse schedule). `_pump_circuit()` re-org'd 2-column → single vertical
  column (4 corridor pumps at real AFF Z 615/940/1340/1740 per `panel-layout.png`; P-02 offset as the
  pinhole-wall pump). Was the only LIVE 2-column layout — overview/ibc-stack already use the `cp.*`
  single-column builders (overview's `equipment_panel`/`water_plumbing` are documented dead code).
  `electrical.rb` regenerated; **electrical.skp re-send pending** (see re-upload list — model not open).
- [x] **Film-plane 2D redraw (Option A) — DONE.** DC left as-is (2026-07-05 decision — a rigid DC can't
  animate the cross-slides). Redrew all 6 FPM sheets from the stale "4-CORNER INDEPENDENT / compound
  tilt+swing independently" framing to **Option A** (rigid plane, coordinated pairs; titles → OPTION A;
  Table 1 COMPOUND→COMBINED "limited, coordinated"; combined config kept but relabelled "(limited)" since
  the constants allow limited combined rigid rotation — only C7 compound *twist* is dropped). FPD dead
  compound special-case removed (output unchanged). Report's 3 prose phrasings aligned to "coordinated
  pairs". Verified visually (sheets 1/4/6); drift gates green. *(Analysis doc left as-is — it's the
  labelled historical analysis of the old stretching design.)*
- [x] **3D D-rings added — DONE.** Added 8 D-ring cylinders to the shared `cp.tote_restraint()` (4/tier on the front bars, mirroring the 2D). Overview sent + **verified 8 in the live model** (4/4 by tier). Shared function → the **ibc-stack + water** models pick them up on their next send. *(Dead `ibc_rack()` D-ring code left for a future delete.)*

## Cost / data modeling
- [ ] **Cost-analysis Bucket B** — model the alternative *configurations* (WWT container, itemized
  battery/solar BOM, poly-tray, galvanized grating, electric-upgrade kit) so savings levers 2–5 become
  real subtractions, not roll-ups. (`costing.py:530`; `cost-analysis-report.md` §4.)
- [ ] **Un-registered values audit** — ~35 values restated across ≥3 docs with no `tbs_constants` /
  `facts.yml` owner (59mm door clearance ×8, 97/85 W cooler, 52mm headroom, the 1260/630/430 L cascade…).
  Per candidate: find owner → add constant + fact → wrap the restatements.

## Docs / gallery
- [x] **Gallery-only diagrams — DONE (won't-do).** Gallery-only PNGs are fine without a dedicated owning report — they live in the `all-diagrams.md` visual index. That gallery is now **excluded from the brochure PDF** (`BROCHURE_EXCLUDE`) so the 100+ images don't bloat it.
- [ ] **`tilt-swing-board-analysis.md` §4** — the combined C0–C8 renders duplicate `distortion-renders.md`
  §3 with extra commentary; merge the two docs or point §4 to the gallery. (Inline TODO in the doc.)
- [x] **`component-dependency-map.md` — DONE.** Portacool note was already resolved (§1.8 = Hessaire
  MC18M). "See Also" done: extended the full **Reports:** + **Diagrams:** cross-ref pair (previously only
  on §1.8) to all 17 §1 registry entries — reports researched with verified section refs, diagrams from
  the §3 matrix. Injector blocks unchanged + green.
- [ ] **`plumbing-report.md` §3.2** — optional light re-review; touched in the master-switch→EP cascade
  but still carries its 2026-06-22 editorial "done" mark.

## Code hygiene
- [x] **Unused imports — DONE.** Removed **181** unused imports across 31 files (verified every generator + model runs clean, gates green, no output change). New stdlib checker `src/generators/check_unused_imports.py` (re-export-aware, `--fix`) is a **release gate** in `release.sh` so it can't drift back.
- [x] **`generate_pinhole_water_panel.py:511` refactor — DONE.** Water-panel context is now built muted **at source** via a `muted()` context manager (`ruby_box/cylinder/tri` resolve mute/alpha against it); the fragile post-build `mute_groups` re-coloring pass + its allow-list are retired. Verified visually-identical (same round(c*(1-f)+n*f) formula; 261 muted + 17 full steel, same split) and byte-transparent for other models.

## Paused directions
- [x] **`ibc-reconfig-v2` — DONE.** The IBC-layout redesign was resolved — the deep 4-leg direct-stack restraint box is the current design (reflected in `tbs_constants`, ibc-stacking-report, and the models).
