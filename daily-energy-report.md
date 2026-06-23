<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Daily Electrical Consumption Report

## 1. Purpose & Scope

The [Electrical Report §3.1](electrical-report.md) budgets energy **per print session**.
This report rolls that up into **one full day of daylight operation** — multiple prints,
the continuous cooling/ventilation load, the print-wash pumping, and the **end-of-day
pump-out of the Brown and Waste tanks** (a once-daily operation that is *not* in the
per-session budget) — and checks it against the battery and the solar recharge.

Per-session figures come from that per-session budget; the daily roll-up and operational
assumptions are derived here.

---

## 2. The Operating Day

A pinhole exposure uses one film plane at a time, so prints are **sequential**: load →
expose → develop & wash → cleanup, then the next. One cycle is ~182 min (~3 h), of which
the **exposure is 37.5 min**. A realistic daylight field day is therefore **~3 prints**
(≈ 9 h of cycles + setup/teardown); 4 is achievable when pushing, 2 on a short/poor-light
day. The container is cooled **once** in the morning and the fans + evaporative cooler
then run **continuously** through the operating day.

> **Standard build is manual** (electric actuation was dropped — see [Cost Analysis](cost-analysis-report.md)),
> so Circuit F draws nothing. Per-**session** energy (incl. the once-daily morning warmup) is ~**771 Wh** (vs 780 Wh with the optional
> actuators) — up from the old ~720 Wh now that the cooler runs through the AC inverter (~<!-- BEGIN fact:evap_cooler_w_bus -->97<!-- END fact:evap_cooler_w_bus --> W on the 12 V bus).

---

## 3. Per-Print Energy (from the session budget)

| Phase / load | W | Min | Wh |
|---|--:|--:|--:|
| Dark adaptation (fans + cooler + safelight) | 232 | 20 | 77 |
| Load image plane (fans + cooler + safelight) | 232 | 45 | 174 |
| **Exposure** (fans + cooler) | 217 | 37.5 | 136 |
| Development & **wash** (fans + cooler + white light) | 277 | 20 | 92 |
| Cleanup (fans + cooler + white light) | 277 | 30 | 138 |
| Wash pump P-01 (Blue, 3× fills) | 90 | 15 | 22.5 |
| Wash pump P-02 (Brown recycled) | 90 | 10 | 15.0 |
| Tray-drain pump P-04 (sump → IBC) | 90 | 5 | 7.5 |
| **Per print (manual)** | | | **~663** *(excl. one-time morning warmup)* |

The **continuous fans + evaporative cooler (217 W)** dominate — they are on the whole
cycle, so most of the energy is *climate control*, not imaging or pumping. The cooler now
runs through the 12V→120V inverter (~<!-- BEGIN fact:evap_cooler_w_bus -->97<!-- END fact:evap_cooler_w_bus --> W on the bus vs the old 80 W placeholder).

---

## 4. Daily Roll-Up — Representative 3-Print Day

| Item | Wh |
|---|--:|
| Morning cooling warmup (once: fans + cooler, 30 min) | 108 |
| 3 prints × 663 Wh (cycle + wash/drain pumps) | 1,989 |
| End-of-day Brown + Waste pump-out (§6) | ~37 |
| **Daily total (3 prints)** | **~2,134 Wh** |

| Day | Prints | Daily Wh |
|---|--:|--:|
| Short / poor light | 2 | ~1,471 |
| **Representative** | **3** | **~2,134** |
| Pushed | 4 | ~2,797 |

---

## 5. Print-Washing Load (called out)

Each print is washed by **P-01 (Blue fresh, 15 min)** + **P-02 (Brown recycled, 10 min)**
— 25 min of pumping at 90 W = **37.5 Wh of wash pumping per print** (P-04 adds 7.5 Wh of
tray-sump drain). Over a 3-print day that is **~112 Wh of wash pumping** plus the white
light during the wash/develop phase. Pumping is a **small fraction (~6%)** of the daily
energy — the cooling load is the real consumer.

---

## 6. End-of-Day Brown & Waste Pump-Out (called out)

At end of day the Brown (IBC-3) and Waste (IBC-4) totes are evacuated to the sealed
end-wall ports — **Brown → X3 via P-05**, **Waste → X4 via P-03** ([Equipment Panel
Report §4.3](plumbing-panel-report.md), [Water System Report §6](water-system-report.md)).

This is **gravity-assisted**: each tote gravity-drains through its low (Z = 200 mm) port,
and the pump only lifts the **~120 L residual** below the port:

| Pump | Tank | Volume pumped | Min @ 3.5 GPM | Wh @ 90 W |
|---|---|--:|--:|--:|
| P-05 | Brown IBC-3 → X3 | ~120 L residual | ~9 | ~14 |
| P-03 | Waste IBC-4 → X4 | ~120 L residual | ~9 | ~14 |
| | + white light for the ~20 min operation | | | ~10 |
| **End-of-day drain total** | | | | **~37 Wh** |

Because gravity does the bulk, the pump energy is **independent of how full the tanks
got** and is **tiny (<2% of the day)**. *Worst case* — if a tote had to be pumped out
entirely with no gravity assist (~600 L) — it would be ~45 min each, ~137 Wh for both;
still minor against the daily total. (Brown is normally *recycled* through the filter
back to Blue rather than dumped; this line covers the case where it is drained off.)

---

## 7. Solar Balance & Battery Autonomy

| | Value |
|---|--:|
| Solar generation (600 W × 5.5 peak-sun-h, Palm Springs) | ~3,300 Wh/day |
| Battery usable (200 Ah × 12 V LiFePO4, 100% DoD) | 2,400 Wh |

| Day | Daily draw | Solar net | Within one battery charge? |
|---|--:|--:|---|
| 2 prints | ~1,471 | **+1,829** | Yes (with wide margin) |
| 3 prints | ~2,134 | **+1,166** | Yes — full overnight autonomy |
| 4 prints | ~2,797 | **+503** | Exceeds the 2,400 Wh battery by ~400 Wh → covered by **daytime solar** (which runs during the prints), not battery alone |

**Conclusions:**
- The system is **solar-positive at every realistic daily throughput** — even a 4-print
  day generates more than it consumes, so it sustains indefinitely on sun.
- A **3-print day fits within a single 2-pack battery charge**, giving a full day of operation
  on a dead-cloudy day from the battery alone.
- A **4-print day relies on the panels topping up during the day** (the loads run in
  daylight, so this is normally fine); on a fully overcast day, cap at ~3 prints. The
  higher-draw AC cooler (~<!-- BEGIN fact:evap_cooler_w_bus -->97<!-- END fact:evap_cooler_w_bus --> W vs the old 80 W placeholder) widened the 4-print battery
  shortfall from ~220 Wh to ~400 Wh — still solar-covered, but battery-only 4-print days are off the table.
- The dominant load is **climate control (fans + evaporative cooler, ~2,050 Wh/day)**, not
  imaging or pumping — the biggest lever on daily energy is *cooling runtime*, not the
  print workflow.

---

## 8. Disconnected Endurance — How Long Off-Grid?

The question: with **no AC charge** (a remote deployment running on solar top-up + the
battery alone), how long can the system operate — and does adding the **second battery
pack** extend it? Two limits compete: **power** and **clean water**.

### 8.1 Power is not the limit (with sun)

Solar generates ~3,300 Wh/day; a 3-print day draws ~2,134 Wh — a **+1,166 Wh/day surplus**,
so on sunny days the battery never depletes and the system runs **indefinitely**. The
battery's job is to ride out *cloudy* days, and that reserve is what the pack count changes:

| Battery | Usable | No-sun reserve (at ~2,134 Wh/day) | With sun |
|---|--:|--:|---|
| **1 pack** (1×100 Ah) | 1,200 Wh | ~0.6 day (≈ 2 prints) | Indefinite (solar-positive) |
| **2 packs** (2×100 Ah) | 2,400 Wh | ~1.1 day (≈ 3 prints) | Indefinite (solar-positive) |

So the **second pack does not lengthen the deployment** — it buys a **cloudy-day buffer**
(ride out ~1 fully-overcast day instead of half a day) and the headroom for a 4-print day
(which exceeds a single 100 Ah pack). On solar, even one pack sustains operation forever.

### 8.2 Clean water *is* the limit

Power being effectively unlimited on sun, the binding constraint is the **fresh (Blue)
water supply**. Each print consumes **~32 gal (121 L) of net Blue water** even with Brown
recycling ([Water System Report §3–4](water-system-report.md)), so:

| Constraint | Capacity | Per print | Endurance |
|---|--:|--:|---|
| **Clean water (Blue, in)** | <!-- BEGIN fact:blue_supply_l -->1,800<!-- END fact:blue_supply_l --> L (<!-- BEGIN fact:blue_supply_gal -->476<!-- END fact:blue_supply_gal --> gal) | 121 L (32 gal) | **~<!-- BEGIN fact:prints_per_resupply -->14<!-- END fact:prints_per_resupply --> prints ≈ 4.7 days** @ 3/day |
| Power, 2 packs + sun | — | ~620 Wh | Indefinite |
| Power, 2 packs, no sun | 2,400 Wh | ~620 Wh | ~3 prints (~1.1 day) |

A disconnected deployment therefore runs **~<!-- BEGIN fact:prints_per_resupply -->14<!-- END fact:prints_per_resupply --> prints (~4.7 days at 3/day)** before it needs
a **resupply run** — which is fundamentally a *water* event (refill Blue), not a charging
event.

### 8.3 Watch the waste side too

The endurance is bounded on **both ends of the water loop**. The **Black (waste) tote fills to ~600 L** (a 1,000 L tote at its working fill) — a *parallel* out-flow limit: in fully self-contained field use (no sewer, waste
transported for disposal), the waste tank can fill before the Blue tank empties, so a
resupply run must **empty Black as well as refill Blue**. If waste cannot be disposed at
all, that — not power or fresh water — becomes the hard stop.

### 8.4 Verdict

- **The deployment length is set by clean water (~<!-- BEGIN fact:prints_per_resupply -->14<!-- END fact:prints_per_resupply --> prints / ~4.7 days), not power.**
- **One vs two battery packs does not change that** — both run indefinitely on sun. The
  second pack buys a **~1-day cloudy-weather reserve** (vs ~half a day) and enables 4-print
  days; for a *fresh-water-limited* 10-print deployment, a single pack is energetically
  sufficient on solar, with the second pack a resilience upgrade rather than an
  endurance one.

---

## 9. Source References

1. [Electrical Report §3](electrical-report.md) — power budget and the per-session itemized energy.
2. [Water System Report §6](water-system-report.md) — pump runtimes, wash cycles, and the Brown/Waste drain-out path.
3. [Plumbing Panel Report §4.3](plumbing-panel-report.md) — P-03 (Waste evac) and P-05 (Brown drain) duties; the ~120 L gravity-drain residual.
4. [Cost Analysis](cost-analysis-report.md) — the manual-actuation decision (Circuit F unused in the standard build).

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
