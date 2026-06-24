# Cost Analysis Report

## 1. Purpose & Scope

A companion to the [Weight Distribution Report](weight-distribution-report.md): where the
weight study asks *where is the mass and where can it be cut*, this asks **where is the
cost and where can it be saved**. It breaks the build down by system, separates one-time
capital from recurring/consumable spend, and ranks the realistic savings levers.

All figures are the **mid-column** estimates from the
[Cost Breakdown](project-cost-breakdown.md) (the itemized source of truth); the build
mid-total is **~<!-- BEGIN costing:ca-mid-total -->$27,068<!-- END costing:ca-mid-total -->**.

---

## 2. Method — Capital vs Recurring

Just as the weight study set aside the fixed container shell to find the *addressable*
design, a cost study has to separate the one-time **capital build** from spend that
recurs or is consumed — savings strategy is different for each.

<!-- BEGIN costing:ca-buckets -->
| Bucket | Mid | What it is |
|---|--:|---|
| **Capital build** (one-time hardware) | **$23,878** | The systems you build once — this is where build-savings live |
| Consumable (per 50-print batch) | $1,650 | Cyanotype chemistry + substrate (Standard ½-Ware) — recurs every batch |
| Recurring (per deployment) | $750 | Commercial-hire transport |
| Soft / regulatory | $790 | Licenses & permits |
<!-- END costing:ca-buckets -->

Build-savings work on the **<!-- BEGIN costing:ca-capital -->$23,878<!-- END costing:ca-capital --> capital**. The <!-- BEGIN costing:ca-consumable -->$1,650<!-- END costing:ca-consumable --> consumable is attacked
separately (bulk chemistry, cheaper substrate) because it repeats every batch and
quickly dominates lifetime cost.

---

## 3. Where the Cost Is

Capital systems ranked by mid cost:

<!-- BEGIN costing:ca-ranking -->
| System | Mid | % of capital | Notes |
|---|--:|--:|---|
| **Processing water system** | $5,258 | 22% | Tray (304 SS) + IBC frame dominate |
| **Film-plane mechanism** | $3,813 | 16% | Carriages, Option-A cross-slides, cam-lever clamps, wall-seat saddles |
| **Container + delivery** | $3,300 | 14% | Grade-dependent (CW vs WWT) |
| **Perimeter walkway** | $2,488 | 10% | GRP grating + steel cantilevers |
| **Power & electrical** | $2,350 | 10% | Battery + solar + distribution + protection |
| **Light lock** | $1,728 | 7% | Plastic-skin custom fabrication |
| **Hinged panel structure** | $1,408 | 6% | Stepped frame + PP skins + Al core + EPDM + latches + B2 bay |
| **Swing pivot** | $1,143 | 5% | Pivot post + bearings + cage + fixed RHS door frame |
| **Interior conversion** | $1,138 | 5% | Insulation, sealing, safelight |
| **Ventilation & cooling** | $884 | 4% | Fans + cooler + inverter + baffle-duct fab + canopy |
| **Chemistry prep shelf** | $203 | 0.9% | Fold-down phenolic board + frame + hinge/stays + tap extension |
| **Optics — pinhole** | $165 | 0.7% | Trivial (it is a pinhole) |
<!-- END costing:ca-ranking -->

The **water system is <!-- BEGIN costing:ca-water-pct -->22<!-- END costing:ca-water-pct -->% of the capital build** and the **304 SS processing tray is its
single biggest line** (~$1,177–1,857) — the same item that topped the weight study.

---

## 4. Savings Opportunities

Ranked by dollar potential and ease. Status is updated as levers are actioned.

| # | Lever | System | Saves | Ease / risk | Status |
|---|---|---|--:|---|---|
| 1 | **Container grade CW → WWT** (wind-water-tight used vs cargo-worthy — fine for a stationary darkroom) | Container | ~$1,350 | Easy, low risk | Available |
| 2 | **Drop film-plane electric actuation → manual** (the mechanism already supports manual tilt/swing) | Film plane | ~$827 | Easy, if manual is acceptable | **Actioned 2026-06-13** — manual is now the standard build; electric is a documented upgrade only ([Cost Breakdown §4.4](project-cost-breakdown.md)) |
| 3 | **Processing tray: 304 SS → poly / thinner gauge** | Water | ~$600–1,000 | Medium — chem-compat + stiffness check | Available (win-win — also cuts weight) |
| 4 | **Battery 200 Ah → 100 Ah** ([Water System Report](water-system-report.md): 1×100 Ah ≈ 25+ prints/charge) | Power | ~$350 | Easy, if fewer sessions/charge is OK | Available |
| 5 | **Solar 3 → 2 panels** (if the power budget allows) | Power | ~$130 | Easy | Available |
| 6 | **Valves / fittings value-engineering** | Water | ~$100–200 | Medium | Available |

Levers 1–5 together trim **~$3,250–3,650** off the ~$22k capital build (**~15%**) without
touching the core optical or structural design.

---

## 5. The Cost–Weight Tension

Cost and weight do not always move together — some weight savings *cost* money, and vice
versa. Worth keeping in view when prioritizing:

- The **GRP walkway grating** (specified for corrosion immunity in the chemistry zone)
  *added* ~$720–890 to save 62 kg. If cost now outranks weight, **reverting GRP →
  galvanized steel recovers ~$800** — at the cost of the corrosion immunity and the 62 kg.
- The **processing tray** (lever #3) is the rare **win-win**: SS → poly cuts *both* cost
  *and* weight, and is corrosion-proof. It is the highest-value single move across both
  studies.

---

## 6. What Is Effectively Fixed

- **Container shell** — already the cheapest large steel box; only the *grade* is a lever
  (#1).
- **Light lock** — already the cheap custom option (~$1,800 vs $2,500–4,500 for a
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
