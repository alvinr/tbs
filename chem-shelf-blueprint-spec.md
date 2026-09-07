<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
<!-- Design spec / scope — NOT a published TBS artifact (not registered in publish.sh). -->

# Chemistry Prep Shelf — Definitive Blueprint Spec

**Status:** **SCOPING (2026-09-07)** — design decisions locked below; blueprint (dimensioned fab sheets +
fastener schedule + load case + datums + cascade) to be drawn. Follows the
[`ibc-frame-blueprint-spec.md`](ibc-frame-blueprint-spec.md) / `fp-corner-blueprint-spec.md` template:
promote the current arrangement-schematic shelf (`chemistry-prep-shelves.md` + `shelf-sheet1–3`) to a
dimensionally-exact, fabricator-ready package.

**Why now:** the fastener standardization (`fastener-standardization.md`) deferred the shelf's ply-attach
decision (M5×16 CSK into a thin wall) to this round. The round resolves it — and simplifies the whole shelf.

---

## Redesign — locked decisions (2026-09-07)

The schematic shelf was a welded 25×25×3 steel SHS perimeter frame with the ply captive inside it, attached
by M5×16 CSK from the frame underside. This round **removes the steel frame** and makes the **plywood the
primary structure**, with all attachments carried by **pronged tee-nuts in the ply** — the project's ply-mount
standard. This kills the M5 (no thin-wall countersink), removes the welded steelwork + powder coat, and lands
the shelf on the same 1/4″-20 tee-nut family used everywhere else.

| Element | Decision |
|---|---|
| **Board** | 18 mm UV-coated / phenolic plywood, **600 × 300 mm** — chemical-resistant (cyanotype + pH 3–4 citric), wipe-clean. **Primary structure** (no steel frame). |
| **Perimeter frame** | **REMOVED.** The ply carries the load; the frame's only jobs were the lip + the M5 attach, both re-solved below. |
| **Spill lip** | Light chemical-resistant lip on the **3 free edges** (not the hinge edge). *Default: HDPE/PVC angle, ~15 mm, screwed to the ply edge — inert in the splash zone; confirm material at review.* |
| **Ply attachment** | **Pronged tee-nuts in the ply underside** (1/4″-20, `tnut-quarter` standard). No M5 CSK. Wet-zone → 1/4″-20 hardware in **SS** (a documented splash-zone exception, like the M8 film-plane SS exception). |
| **Piano hinge** | 600 mm **bolt-on** (drilled-leaf) SS piano hinge — **shelf leaf** machine-screwed (1/4″-20 SS into the ply tee-nut row); **wall leaf** to the 8 mm wall backing plate. *(Was weld-on; bolt-on because the ply attaches by tee-nut, not weld.)* |
| **Stays** | **2 × 304 SS chain** — a **flat SS pad-eye (D-ring)** bolted flush to each front-corner underside (2× 1/4″-20 SS machine screws into tee-nuts — a pad-eye, NOT a threaded eye bolt, because the shortest eye-bolt shank (1″/25 mm) would pierce the 18 mm board) ↔ an **M8 eye bolt** in the wall backing-plate weld-nut ~230 mm above the hinge. Length-adjustable by link + quick-link. Tension-only. |
| **Wall side** | Piano-hinge cleat + 2 chain-anchor points bolt to **flat 8 mm steel backing plates welded to the corrugated-wall crests** (M8×25 into M8 weld-nuts, ~14 mm grip) — unchanged from the schematic. |
| **Transport latch** | Over-center / barrel latch at the top secures the folded-up board. |
| **M5×16 CSK** | **ELIMINATED** — the M5 family retires with this round (`fastener-standardization.md`). |

## Load basis

Design load **25 kg** (bottles, cylinders, roller tray, scale, staging), deployed horizontal. Load path:
**18 mm ply in bending** (simply supported: piano-hinge back edge + chain-held front edge, ~300 mm span) →
back edge to the **piano hinge** → front corners to the **2 chains** (tension) → **wall backing plates** →
crest welds. Elements to check (each demand → capacity → SF), in a driftproof `chem_shelf_load.py`:

- **Board bending / deflection** — 18 mm ply, 600 × 300, 25 kg UDL over the ~300 mm hinge-to-front span.
- **Chain + shelf-corner tee-nut** — chain angle ≈ 37° (front corner → anchor 230 mm up over 300 mm) →
  tension ≈ 12.5 kg / sin θ ≈ **~205 N/chain**; check the chain WLL and the **1/4″-20 pronged tee-nut
  pull-out in 18 mm ply**.
- **Piano-hinge back-edge reaction** — ~12.5 kg spread over 600 mm; per-tee-nut screw shear/pull-out.
- **Wall backing-plate group** — M8×25 into weld-nuts + crest-weld throat vs the hinge + chain reactions.

## Blueprint deliverables (phases)

1. **Structural validation** — `chem_shelf_load.py` → a computed demand/capacity/SF table into
   `chemistry-prep-shelves.md` §3.3 (replacing the qualitative text), authoritative voice, each cited.
2. **Dimensioned fab sheets** — upgrade `shelf-sheet1–3`: board + lip cut sheet (hole positions for the
   tee-nuts), the hinge + tee-nut row detail, the chain + eye + wall-anchor detail, the 8 mm backing-plate
   plate schedule (1:1, hole Ø/PCD), the transport-latch keeper.
3. **Fastener + weld schedule** — the tee-nut/hinge/chain/wall-bolt schedule + the crest-weld callouts.
4. **Datums + tolerances** — board datum, tee-nut PCD tolerance, backing-plate hole tolerance, deployed-level
   ± from the chain adjustment.
5. **Cascade** — `tbs_constants` (SHELF_* + new tee-nut/chain constants), `parts.py` shelf system (drop the
   25×25×3 SHS + M5 CSK; add tee-nuts + machine screws + SS chain + eye bolts + wall eyes/hooks), `costing.py`
   shelf section, the **3D `chem_shelf()` builder in `generate_sketchup_model.py`** (overview — remove the
   frame, add the chain stays + lip; re-send overview + construction if it reuses the builder), and
   `all-diagrams.md` / `dependencies.yml`.

## Parts — standard-part reuse vs new to source

The whole **ply-side and wall-side** collapses onto hardware already in the registry — the payoff of the
tee-nut decision. Only the chain stays + the bolt-on hinge variant are genuinely new.

**Reuse (no new SKU — bump qty / material-exception only):**
- **Tee-nuts** → `tnut-quarter` (825001), 1/4″-20 pronged, ~10 off (hinge row + 2 pad-eyes).
- **Ply-attach machine screws** → the 1/4″-20 ply-mount screw pattern (`panel-machine-screws` 826771), **~3/4″,
  in SS** for the splash zone (wet-zone exception) — hinge leaf + pad-eyes.
- **Wall side** → the M8 group: M8×25 (91280A534) + nut (90591A161) + washer (91166A270) into the 8 mm backing
  plates (hinge cleat + 2 chain wall anchors).
- **Spill lip** → a sealed strip of the **same 18 mm ply** (offcut) or an **HDPE offcut** (46684/46685) — no new material.
- **Board** (`BPI6WUV2I`), **8 mm backing plates** (local fab) — existing.

**New to source (full spec):**
1. **Bolt-on piano hinge, 600 mm** — 304 SS, **drilled leaves** (bolt-on), ~32 mm open width. *(Re-spec of the existing hinge line.)*
2. **Flat SS pad-eye / D-ring anchor plate ×2** — 304 SS, 2× 1/4″-20 bolt holes, WLL ≥ 25 kg — front-corner chain anchors (bolt flush to the underside; replaces threaded eye bolts, which the 1″ min shank rules out on an 18 mm board).
3. **M8 eye bolt ×2** — 304 SS, M8 × ~1″ shank — chain wall anchors into the backing-plate weld-nuts.
4. **304 SS chain** — ~4 mm / 1/8″, WLL ≥ 25 kg, ~1 m total.
5. **304 SS quick-links ×4** — ~4 mm, chain ends + length adjust.
6. **Transport latch ×1** — 304 SS over-center toggle latch + keeper (or borrow the panel cam-latch family, McMaster 1619A74).

**Remaining opens (confirm at review):** lip material (ply vs HDPE offcut); tee-nut count (from the hinge screw
pitch); board face (keep UV-ply vs phenolic); latch — dedicated toggle vs the cam-latch family.

## Not in scope
The wall backing plates + M8 weld-nut group + the pinhole-wall crest welding are the existing wall interface
(unchanged). The tap/plumbing to the left of the shelf is a separate subsystem.
