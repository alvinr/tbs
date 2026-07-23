<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Cost Savings Analysis Report

## 1. Purpose & Scope

A companion to the [Weight Distribution Report](weight-distribution-report.md): where the
weight study asks *where is the mass and where can it be cut*, this asks **where is the
cost and where can it be saved**. It breaks the build down by system, separates one-time
capital from recurring/consumable spend, and ranks the realistic savings levers.

All figures are the **mid-column** estimates from the
[Cost Breakdown](project-cost-breakdown.md) (the itemized source of truth); the build
mid-total is **~<!-- BEGIN costing:ca-mid-total -->$31,181<!-- END costing:ca-mid-total -->**.

---

## 2. Method — Capital vs Recurring

Just as the weight study set aside the fixed container shell to find the *addressable*
design, a cost study has to separate the one-time **capital build** from spend that
recurs or is consumed — savings strategy is different for each.

<!-- BEGIN costing:ca-buckets -->
| Bucket | Mid | What it is |
|---|--:|---|
| **Capital build** (one-time hardware) | **$28,151** | The systems you build once — this is where build-savings live |
| Consumable (per 50-print batch) | $1,490 | Cyanotype chemistry + substrate (Standard ½-Ware) — recurs every batch |
| Recurring (per deployment) | $750 | Commercial-hire transport |
| Soft / regulatory | $790 | Licenses & permits |
<!-- END costing:ca-buckets -->

Build-savings work on the **<!-- BEGIN costing:ca-capital -->$28,151<!-- END costing:ca-capital --> capital**. The <!-- BEGIN costing:ca-consumable -->$1,490<!-- END costing:ca-consumable --> consumable is attacked
separately (bulk chemistry, cheaper substrate) because it repeats every batch and
quickly dominates lifetime cost.

---

## 3. Where the Cost Is

Capital systems ranked by mid cost:

<!-- BEGIN costing:ca-ranking -->
| System | Mid | % of capital | Notes |
|---|--:|--:|---|
| **Processing water system** | $6,675 | 24% | Tray (304 SS) + IBC frame dominate |
| **Film-plane mechanism** | $6,427 | 23% | Carriages, Option-A cross-slides, muslin spring clips, wall-seat saddles |
| **Container + delivery** | $3,300 | 12% | Grade-dependent (CW vs WWT) |
| **Power & electrical** | $2,873 | 10% | Battery + solar + distribution + protection |
| **Perimeter walkway** | $2,503 | 9% | GRP grating + steel cantilevers |
| **Light lock** | $1,768 | 6% | Plastic-skin custom fabrication |
| **Hinged panel structure** | $1,403 | 5% | Stepped frame + PP skins + Al core + EPDM + latches + B2 bay |
| **Swing pivot** | $1,395 | 5% | Pivot post + bearings + cage + fixed RHS door frame |
| **Ventilation & cooling** | $817 | 3% | Fans + cooler + inverter + baffle-duct fab + canopy |
| **Interior conversion** | $578 | 2% | Insulation, sealing, safelight |
| **Chemistry prep shelf** | $227 | 0.8% | Fold-down phenolic board + frame + hinge/stays + tap extension |
| **Optics — pinhole** | $185 | 0.7% | Trivial (it is a pinhole) |
<!-- END costing:ca-ranking -->

The **water system is <!-- BEGIN costing:ca-water-pct -->24<!-- END costing:ca-water-pct -->% of the capital build** and the **304 SS processing tray is its
single biggest line** (<!-- BEGIN costing:tray-low -->$1,293<!-- END costing:tray-low -->–<!-- BEGIN costing:tray-high -->$2,016<!-- END costing:tray-high -->) — the same item that topped the weight study.

---

## 4. Savings Opportunities

Ranked by dollar potential and ease. Status is updated as levers are actioned.

| # | Lever | System | Saves | Ease / risk | Status |
|---|---|---|--:|---|---|
| 1 | **Container grade CW → WWT** (wind-water-tight used vs cargo-worthy — fine for a stationary darkroom) | Container | ~<!-- BEGIN costing:ca-lever-container -->$1,350<!-- END costing:ca-lever-container --> | Easy, low risk | Available |
| 2 | **Drop film-plane electric actuation → manual** (the mechanism already supports manual tilt/swing) | Film plane | ~<!-- BEGIN costing:ca-lever-film -->$827<!-- END costing:ca-lever-film --> | Easy, if manual is acceptable | **Actioned 2026-06-13 (banked)** — manual is the standard build, so this is already realized, not a still-available saving; electric is a documented upgrade only ([Cost Breakdown §4.4](project-cost-breakdown.md)) |
| 3 | **Processing tray: 304 SS → poly** (poly needs a support frame over the 4.5 m span + poly-weld fab) | Water | ~<!-- BEGIN costing:ca-lever-tray-low -->$600<!-- END costing:ca-lever-tray-low -->–<!-- BEGIN costing:ca-lever-tray-high -->$1,000<!-- END costing:ca-lever-tray-high --> | Medium | **Decided 2026-07-05 — keep 304 SS** (self-supporting + durable; not revisiting) |
| 4 | **Battery — already 1×100 Ah** (the lean config; [Water System Report](water-system-report.md): 1×100 Ah ≈ 25+ prints/charge). A 2nd pack is a +<!-- BEGIN costing:ca-lever-battery -->$375<!-- END costing:ca-lever-battery --> optional **upgrade**, not a saving. | Power | +$375 (add) | — | **Not a saving** — 100 Ah is the standard |
| 5 | **Solar 3 → 2 panels** (if the power budget allows) | Power | ~<!-- BEGIN costing:ca-lever-solar -->$133<!-- END costing:ca-lever-solar --> | Easy | Available — computed (drop 1× 200W panel) |
| 6 | **Valves / fittings value-engineering** | Water | ~<!-- BEGIN costing:ca-lever-valves-low -->$100<!-- END costing:ca-lever-valves-low -->–<!-- BEGIN costing:ca-lever-valves-high -->$200<!-- END costing:ca-lever-valves-high --> | Medium | Available |

After the material decisions, the only still-**available** build-savings levers are **1 (container grade) + 5 (solar)** — together **~<!-- BEGIN costing:ca-savings-low -->$1,500<!-- END costing:ca-savings-low -->** off the <!-- BEGIN costing:ca-capital -->$28,151<!-- END costing:ca-capital --> capital build (**~<!-- BEGIN costing:ca-savings-pct-low -->5<!-- END costing:ca-savings-pct-low -->%**), plus ~$100–200 of valve value-engineering (#6). Everything else is settled: lever 2 **banked** (manual is the standard build), lever 3 **kept 304 SS** (decision), lever 4 **already 1×100 Ah**.

> **Derivation note.** Lever 1 (container grade), lever 5 (solar), and the roll-up total +
> percentage are computed in `costing.py` — container is a true CW − WWT subtraction off the
> scenario layer, solar is a real 1-panel subtraction (drop 1× `solar-panel-200w`), and the roll-up
> is the summed **still-available** levers over the capital build, so all cascade on any cost change.
> Bucket-B finding (2026-07-05): modeling each option against the as-built BOM showed lever 2 (film)
> is already **banked** — manual is the standard build — and lever 4 (battery) is moot — the standard
> is already 1×100 Ah, and its 2nd pack is a +$375 **upgrade**, not a saving — so both were dropped
> from the roll-up. Lever 3 (tray) is now **decided** too — 304 SS kept (over the 4.5 m span a poly
> tray needs a support frame that erodes the saving, plus poly-weld fab) — so it also leaves the roll-up.

---

## 5. The Cost–Weight Tension

Cost and weight do not always move together — some weight savings *cost* money, and vice
versa. Worth keeping in view when prioritizing:

- The **GRP walkway grating** (corrosion immunity in the chemistry zone) *added* ~$720–890 to
  save 62 kg. **Decided 2026-07-05 — keep molded GRP:** the 62 kg weight saving + corrosion
  immunity are worth the premium; the ~$800 galvanized-steel alternative is **not** being taken.
- The **processing tray** (lever #3): SS → poly would cut *both* cost and weight, but **decided
  2026-07-05 to keep 304 SS** — over the 4.5 m span a poly tray needs a support frame (eroding the
  saving) plus poly-weld fabrication; 304 SS is self-supporting and durable.

---

## 6. What Is Effectively Fixed

- **Container shell** — already the cheapest large steel box; only the *grade* is a lever
  (#1).
- **Light lock** — already the cheap custom option (<!-- BEGIN costing:ca-lightlock-mid -->$1,768<!-- END costing:ca-lightlock-mid --> mid vs $2,500–4,500 for a
  commercial darkroom door).
- **Swing pivot, ventilation, optics** — small absolute spend; diminishing returns.
- **IBC frame, pumps, filters** — load-bearing or commodity; little to cut safely.

---

## 7. Source References

1. [Cost Breakdown](project-cost-breakdown.md) — itemized build cost, three scenarios, all sources cited (the figures this report summarizes).
2. [Weight Distribution Report](weight-distribution-report.md) — the companion mass study; the tray is the shared top lever.
3. [Film Plane Mechanism Report](film-plane-mechanism-report.md) — manual vs electric actuation (lever #2).
4. [Water System Report](water-system-report.md) — processing tray (304 SS) and battery/pump sizing (levers #3, #4).
5. [Electrical Report](electrical-report.md) — power-system sizing (levers #4, #5).
