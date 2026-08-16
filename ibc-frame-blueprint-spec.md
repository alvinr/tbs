<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
<!-- Design spec / scope — NOT a published TBS artifact (not registered in publish.sh). -->

# IBC Stacking Frame — Definitive Blueprint Spec

**Status:** **Phases A–E COMPLETE (2026-08-15)** — restraint validated + redesigned (A), fastener + weld
schedule (B), datum/tolerance scheme (C), fab-detail sheets (D), cascade (E). **Scope extended to the whole
IBC-corridor metal construction** (corridor-panel brackets / pipe-run L-brackets / ribbon cross-beams /
walkway-arm connection, folded into §3.4–3.6 + the cut list).

**Delivered beyond the original plan (review sweep, Aug 15):**
- **Sheet 4 — Fabrication Details A–F** (added F = walkway-arm→upright clamp) + ~7 review passes correcting the
  actual joints: bar bolted (not welded) to the hanger, vertical J7 retention, flush cleat bolts, tee-nut on
  the ply BACK face, Detail D as a proper welded-L per Alvin's sketch, lighter steel tone.
- **NEW — Plate Fabrication Schedule (2 sheets)**: every plate 1:1 with hole Ø/positions/PCD (foot, hanger
  backing, hanger pocket as back-plate + seat faces, cleat, rear-panel tab, pipe-run L).
- **Design refinements:** wall-hanger back-plate + seat standardized to 60 mm (reuse the backing stock);
  **J7 → 1 centered bolt** (redundancy not strength); **rear-panel + pipe-run brackets W6/W7 → #14 TEK
  self-drillers (J8/J9)** — bolt-on to a painted frame, no hot work; `IBC_WBKT_* → FP_CORNER_SEAT_*` rename.

**Remaining / next:** (1) **3D-model reconciliation** — DONE 2026-08-16: pocket → 60/60 + centered J7 bolt +
the left-cantilever foot-X0 missed-cascade fix; all 6 affected models re-sent/saved/uploaded, drift-free.
(2) **Assembly / weld-sequence** notes — DONE 2026-08-16 (report §3.7: 4-phase shop-weld → bolt-on → install →
load, with balanced-weld distortion control). (3) Optional rendered load-case sheet — next. (4) **Coating /
surface-finish spec** — deferred to the fab/quoting stage. Then publish.

## Phase A outcome (R5 — approved 2026-08-14)

The EN 12195-1 loaded-transport case (the camera runs **self-contained**, so it ships **with water aboard**)
governs. A single 50×20×3 front bar is weak-axis (20 mm in the load direction, film-rail-slot-limited) and
**fails loaded (bending SF 0.79)**. Adopted redesign **R5**: **two 50×20×3 bars per tote face** (4→8 bars,
both in the 20 mm slot, sharing one wall hanger) **+ certified anti-slip matting** (μ 0.2→0.6) **+ 2 straps/
stack**. Result: bar **SF 1.59 bar-alone** (positive blocking, mat-independent) / **4.77 with the mat**;
all downstream elements SF ≥ 8; drained state SF ≥ 12. Computed in `ibc_frame_load.py`; written into
`ibc-stacking-report.md` §3.4. Cascaded: `tbs_constants` (IBC_FRONT_BAR_*), 3D `tote_restraint()`, weight
model (frame 90→119 kg), `parts.py` (+anti-slip mat, doubled bar steel) + costing (+$40/$80), 2D
ibc-frame/ibc-stacking sheets, 5 models re-sent.
**Purpose:** upgrade the IBC **stacking/restraint frame** from arrangement-schematic to a
**dimensionally-exact, fabricator-ready** drawing — the second subsystem to take the film-plane-corner
milestone standard (dimensioned details + fastener schedule + weld schedule + datums/GD&T + a computed
load case). Follows [`fp-corner-blueprint-spec.md`](fp-corner-blueprint-spec.md) as the template.

## Locked decisions (2026-08-14)

1. **Structural-transport basis = EN 12195-1:2010** (European load-securing standard for road transport).
2. **Scope EXTENDED 2026-08-14 → the whole IBC plumbing-corridor METAL construction.** The deep-box frame
   is one welded structure serving three roles, so the blueprint now covers: the restraint frame + tote
   restraint + wall-anchoring (Phase A–D) **PLUS** the plumbing-corridor metal that shares it — the
   rear-panel/corridor-panel brackets (×6), the pump-support L-brackets (×12), the ribbon cross-beams, and
   the **walkway cantilever-arm CONNECTION into the front uprights** (arm's own detailing stays with the
   walkway blueprint — Alvin's boundary). The purchased totes, the ply panels, and the water plumbing/pumps
   are interfaces, not in scope.
3. **Do Phase A (structural validation) + Phase B (fastener/weld schedule) first.** Phases C (datums/
   tolerances) and D (fab-detail sheets) + E (cascade) follow as a second pass.

## Design of record (from `ibc-stacking-report.md` §3.2 — the restraint deep 4-leg box)

| Element | Spec |
|---|---|
| Frame | 2×2×0.120in (50.8×50.8×3.05) **A500 Gr.B RHS** — deep 4-leg box, front pair X4654 + back pair X5104, butt-jointed top + bottom rings; **restraint-only** (no vertical service load) |
| Floor feet | 4 × **150×150×12** steel flange plate, **4× M12 anchor** each (front feet reach ~25 mm under the tray) |
| Front retaining bars | **8 × 50×20×3 RHS — 2 per tote face** (R5), wall→upright per column, span ~1,046 mm |
| Anti-slip matting | 4 × certified anti-slip mat (**μ ≥ 0.6**) under the tote interfaces |
| Front-bar → upright cleats | **M12×40** 18-8 SS (92314A744), 2/bar × 4 = 8 |
| Wall joist hangers | 4 × Simpson-style **4 mm folded U-pocket**, each **through-bolted 4× M12×65 Gr.8.8** (91280A728) to an exterior backing plate |
| Exterior backing plates | 4 × **100×135×8** steel, OUTSIDE the corrugated side wall (hex heads out), 4× M12 holes — spreads tote thrust so bolts can't pull through the thin wall |
| Weld-on lashing rings | 8 × 1½" weld-on (3028T31), 6,600 lb ring WLL; on the front bars (4/tier × 2 tiers) |
| Ratchet straps | 4 × 2" (50 mm), 3,333 lb (~1,512 kg) assembly WLL |
| Joints | fillet weld throughout (sizes to be scheduled — Phase B) |

## Load basis — EN 12195-1:2010

**Acceleration (mass) coefficients** (road transport):

| Direction | Coefficient | Note |
|---|---|---|
| Longitudinal, forward (braking) | c_x = **0.8 g** | governs the front retaining bars |
| Longitudinal, rearward | c_x = **0.5 g** | |
| Sideways (cornering) | c_y = **0.5 g** | governs wall-trapping + hangers |
| Vertical (down, sliding formula) | c_z = **1.0 g** | friction-credit term |

**Method + citations:** blocking (positive restraint) **BC ≥ f_s·m·g·(c − μ·c_z)**; f_s = 1.25 fwd /
1.1 else; μ = 0.20 bare (unlisted plastic/steel fallback) → 0.60 with certified anti-slip mat (Annex B).
Sources: [EN 12195-1:2010 (SIST preview — Table 2, §5, Annex B)](https://cdn.standards.iteh.ai/samples/32961/4592590bcf194f1a8ffa917a5db7d258/SIST-EN-12195-1-2011.pdf),
[MariTerm HVTT13 (coefficients + blocking equation + f_s)](https://hvttforum.org/wp-content/uploads/2019/11/Johansson-International-guidelines-on-safe-load-securing-for-road-transport.pdf),
[BG Verkehr KB 029-2 (μ table)](https://res.jedermann.de/data/downloads/KB029-2_Gesamtdokument.pdf).

**Design mass — RESOLVED (Alvin: "design for both").** Both states carried: **drained** (nominal — totes
site-filled, 65 kg tare) and **loaded** (self-contained transport, a full top-tier Blue tote ≈ **965 kg**,
900 L + tare, high CG). The restraint is sized so the loaded case passes; the drained case then clears
≥ 12× everywhere.

## Phase A — Structural validation (compute demand vs capacity, with SF)

Driftproof compute script (analog of `fp_corner_load.py`): **`ibc_frame_load.py`** → optional load-case
sheet. Elements to check, each with an EN 12195-1 design force → capacity → SF:

- [x] **Front retaining bar** (50×20×3 RHS, ~1,046 mm span) — bending + shear under the top-tote forward thrust (0.8 g, friction-credited).
- [x] **Wall-hanger bolt group** — 4× M12×65 Gr.8.8 in shear + **backing-plate bearing / corrugated-wall pull-through** (100×135×8 plate). The corrugation-depth (30 mm) is the pull-through assumption — ties to the parked procurement gate.
- [x] **Front-bar → upright cleat** — M12×40 18-8 SS shear.
- [x] **Floor-foot anchors** — 4× M12 per foot, shear + uplift into the slab.
- [x] **Lashing ring + strap** — 6,600 lb ring / 3,333 lb strap WLL vs the EN 12195-1 vertical + lateral tie-down demand.
- [ ] **Weld throats** — ring→bar, upright↔ring, foot↔upright fillet throat vs demand → **moved to Phase B** (weld schedule).

Deliverable: a computed validation table into `ibc-stacking-report.md` §3.4 (replacing the qualitative
text), authoritative voice, each capacity/coefficient cited.

## Phase B — Fastener + weld schedule — DONE 2026-08-14

- [x] **Fastener schedule J1–J3** (report §3.5): J1 floor foot-plate → #14×3¼″ 410 SS self-driller ×16 (driven to seat); J2 bar→upright cleat → M12×40 A2-70 ×16 (~50 N·m + anti-seize, nyloc); J3 wall-hanger through-bolt → M12×65 Gr.8.8 ×16 (~90 N·m, plain nut + split-lock). Torques cited (Fastenal/Bossard/ITW-Buildex). **Caught a Phase-A miss:** the cleat bolts (M12×40) were still qty 8 — doubled to **16** with the 8 bars (+$12 ibc-frame).
- [x] **Weld schedule W1–W5** (report §3.5, sized in `ibc_frame_load.py`): W4 lashing-ring→bar 6 mm fillet (SF 9.1 vs strap WLL) + W3 cleat→upright 4 mm (SF 37) are load-checked; W1 upright↔ring 5 mm, W2 foot↔upright 6 mm, W5 hanger-seat↔pocket 4 mm are AWS D1.1 minimum practical fillets (frame load << capacity). Hangers are folded (not welded); backing plates loose (bolted).
- [x] Added as tables in `ibc-stacking-report.md` §3.5. (A dedicated fastening/weld detail SHEET is deferred to Phase D.)

## Phase C — Datum + tolerance scheme — DONE 2026-08-14

- [x] Report §3.6: datums **A** (4-foot underside plane), **B** (front-upright faces X4654), **C** (corridor CL Yd1181) + functional tolerances (foot coplanarity ±1.5, upright plumb ±2/2296, diagonal square ±3, foot M12 PCD ±0.5, bar-seat/hanger Z ±2, backing-plate holes ±1, corridor width +2/−0); general = ISO 13920 Class B, welds AWS D1.1.
- [x] The scheme is also drawn on `ibc-frame-sheet1` as a DATUMS & TOLERANCES callout block.

## Phase D — Fab-detail sheets — CORE DONE 2026-08-14 (detail insets pending)

- [x] **Member cut list** — drawn on `ibc-frame-sheet1` (4 uprights @2296, ring rails, 8 bars @1046, 4 feet, 8 backing plates @60×205, 8 hangers, 8 cleats), lengths computed from the frame constants.
- [x] **Datum + tolerance callout block** on sheet1 (from §3.6); weld-schedule (§3.5 W1–W5 leg sizes) folded into the fab notes.
- [x] Stale-value cleanup: sheet labels/notes 100×80→60×205, ~119→~123 kg, bar Z560/1760→Z500/950+1500/1950.
- [x] **Detail INSETS — DONE 2026-08-14:** new **Sheet 4 (Fabrication Details)** with DETAIL A wall joist hanger (per-bar 2-bolt, 50mm clearance, backing plate), B bar→upright cleat, C weld-on lashing ring, D rear-panel bracket, E pump-support L-bracket — each with its weld (W) + fastener (J) callout + a notes cell. Registered (gallery/publish/setup_docs), embedded in report §3.5 + §8. (The foot-plate inset already lived on sheet 1.) Optional rendered load-case sheet still deferred.

## Phase E — Cascade + close (as changes land)

- Firm any spec change into `parts.py`/`costing.py`/BOM/master-shopping-list; regenerate + gallery-register any new sheet; re-send models only if geometry detail changed; `lint.py`; RELEASE `[Unreleased]`; TODO. (Ongoing — done for A/B/C/D-core.)

## Open decisions

1. **Transport fill state — RESOLVED (Alvin 2026-08-14): design for BOTH** (drained nominal + loaded
   over-spec). Restraint sized for loaded → R5. Done.
2. **Load-case sheet — deferred to Phase D.** Phase A landed as the §3.4 report table (SF matrix); a
   rendered `ibc-frame` load-case sheet (like fp Sheet 10) can be added with the fab-detail sheets if wanted.
