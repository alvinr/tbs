<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Daily Electrical Consumption Report

## 1. Purpose & Scope

The [Electrical Report §3.1](electrical-report.md) budgets energy **per print session**.
This report rolls that up into **one full day of daylight operation** — multiple prints,
the continuous cooling/ventilation load, and the print-wash pumping — and checks it
against the battery and the solar recharge. The **Brown/Waste tote dump** is handled
separately (§6): it is a per-resupply servicing event, *not* a daily one.

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

> **The film plane is positioned manually** (hand-slid corners — no powered actuation load).
> Per-**session** energy (one print cycle incl. the morning cooling warmup) is ~**<!-- BEGIN energy:wh-session -->842<!-- END energy:wh-session --> Wh**; the cooler runs through
> the AC inverter (~<!-- BEGIN fact:evap_cooler_w_bus -->97<!-- END fact:evap_cooler_w_bus --> W on the 12 V bus).

---

## 3. Per-Print Energy (from the session budget)

| Phase / load | W | Min | Wh |
|---|--:|--:|--:|
| Dark adaptation (fans + cooler + safelight) | <!-- BEGIN energy:phase1-w -->256<!-- END energy:phase1-w --> | 20 | <!-- BEGIN energy:phase1-wh -->85<!-- END energy:phase1-wh --> |
| Load image plane (fans + cooler + safelight) | <!-- BEGIN energy:phase2-w -->256<!-- END energy:phase2-w --> | 45 | <!-- BEGIN energy:phase2-wh -->192<!-- END energy:phase2-wh --> |
| **Exposure** (fans + cooler) | <!-- BEGIN energy:phase3-w -->217<!-- END energy:phase3-w --> | 37.5 | <!-- BEGIN energy:phase3-wh -->136<!-- END energy:phase3-wh --> |
| Development & **wash** (fans + cooler + white light) | <!-- BEGIN energy:phase4-w -->323<!-- END energy:phase4-w --> | 20 | <!-- BEGIN energy:phase4-wh -->108<!-- END energy:phase4-wh --> |
| Cleanup (fans + cooler + white light) | <!-- BEGIN energy:phase5-w -->323<!-- END energy:phase5-w --> | 30 | <!-- BEGIN energy:phase5-wh -->162<!-- END energy:phase5-wh --> |
| Wash pump P-01 (Blue, 3× fills) | <!-- BEGIN energy:pump-w -->62<!-- END energy:pump-w --> | 15 | <!-- BEGIN energy:pump-p01-wh -->15.5<!-- END energy:pump-p01-wh --> |
| Wash pump P-02 (Brown recycled) | <!-- BEGIN energy:pump-w -->62<!-- END energy:pump-w --> | 10 | <!-- BEGIN energy:pump-p02-wh -->10.3<!-- END energy:pump-p02-wh --> |
| Tray-drain pump P-04 (continuous drain across the wash) | <!-- BEGIN energy:pump-w -->62<!-- END energy:pump-w --> | 25 | <!-- BEGIN energy:pump-p04-wh -->25.8<!-- END energy:pump-p04-wh --> |
| **Per print (manual)** | | | **~<!-- BEGIN energy:per-print-wh -->734<!-- END energy:per-print-wh -->** *(excl. one-time morning warmup)* |

The **continuous fans + evaporative cooler (217 W)** dominate — they are on the whole
cycle, so most of the energy is *climate control*, not imaging or pumping. The cooler
runs through the 12V→120V inverter (~<!-- BEGIN fact:evap_cooler_w_bus -->97<!-- END fact:evap_cooler_w_bus --> W on the bus).

---

## 4. Daily Roll-Up — Representative 3-Print Day

| Item | Wh |
|---|--:|
| Morning cooling warmup (once: fans + cooler, 30 min) | <!-- BEGIN energy:warmup-wh -->108<!-- END energy:warmup-wh --> |
| 3 prints × <!-- BEGIN energy:per-print-wh -->734<!-- END energy:per-print-wh --> Wh (cycle + wash/drain pumps) | <!-- BEGIN energy:prints-wh-3 -->2,201<!-- END energy:prints-wh-3 --> |
| **Daily total (3 prints)** | **~<!-- BEGIN energy:daily-wh-3 -->2,310<!-- END energy:daily-wh-3 --> Wh** |

| Day | Prints | Daily Wh |
|---|--:|--:|
| Short / poor light | 2 | ~<!-- BEGIN energy:daily-wh-2 -->1,576<!-- END energy:daily-wh-2 --> |
| **Representative** | **3** | **~<!-- BEGIN energy:daily-wh-3 -->2,310<!-- END energy:daily-wh-3 -->** |
| Pushed | 4 | ~<!-- BEGIN energy:daily-wh-4 -->3,044<!-- END energy:daily-wh-4 --> |

---

## 5. Print-Washing Load (called out)

Each print is washed by **P-01 (Blue fresh, 15 min)** + **P-02 (Brown recycled, 10 min)**
— 25 min of pumping at <!-- BEGIN energy:pump-w -->62<!-- END energy:pump-w --> W = **<!-- BEGIN energy:wash-wh-print -->25.8<!-- END energy:wash-wh-print --> Wh of wash pumping per print** (P-04 adds <!-- BEGIN energy:pump-p04-wh -->25.8<!-- END energy:pump-p04-wh --> Wh of
tray-sump drain, running across the wash). Over a 3-print day that is **~<!-- BEGIN energy:wash-wh-3 -->78<!-- END energy:wash-wh-3 --> Wh of wash pumping** plus the white
light during the wash/develop phase. All pumping together is a **small fraction (~<!-- BEGIN energy:pump-pct-day -->7<!-- END energy:pump-pct-day -->%)** of the daily
energy — the cooling load is the real consumer.

---

## 6. Resupply Brown & Waste Pump-Out (per dump run — not daily)

The Brown (IBC-3) and Waste (IBC-4) totes are evacuated to the sealed end-wall ports —
**Brown → X3 via P-05**, **Waste → X4 via P-03** ([Plumbing
Report §5.3](plumbing-report.md), [Water System Report §7](water-system-report.md))
— only at a **resupply / dump run**, when the clean-water supply is replenished. That
service interval is set by the Blue water (~<!-- BEGIN fact:prints_per_resupply -->15<!-- END fact:prints_per_resupply --> prints ≈ 5 days at 3/day, §8.2), so the
totes are emptied roughly **every ~5 days, not every evening** — the camera can sit on
site for several days between dump runs.

This is **gravity-assisted**: each tote gravity-drains through its low port,
and the pump only lifts the **~120 L residual** below the port:

| Pump | Tank | Volume pumped | Min @ 3.5 GPM | Wh @ <!-- BEGIN energy:pump-w -->62<!-- END energy:pump-w --> W |
|---|---|--:|--:|--:|
| P-05 | Brown IBC-3 → X3 | ~120 L residual | ~<!-- BEGIN energy:drain-min-tote -->9<!-- END energy:drain-min-tote --> | ~<!-- BEGIN energy:drain-pump-wh-tote -->9<!-- END energy:drain-pump-wh-tote --> |
| P-03 | Waste IBC-4 → X4 | ~120 L residual | ~<!-- BEGIN energy:drain-min-tote -->9<!-- END energy:drain-min-tote --> | ~<!-- BEGIN energy:drain-pump-wh-tote -->9<!-- END energy:drain-pump-wh-tote --> |
| | + white light for the ~20 min operation | | | ~10 |
| **Per-dump-run drain total** | | | | **~<!-- BEGIN energy:drain-wh -->36<!-- END energy:drain-wh --> Wh** |

Because gravity does the bulk, the pump energy is **independent of how full the totes
got** and is **tiny — ~<!-- BEGIN energy:drain-wh -->36<!-- END energy:drain-wh --> Wh per dump run** (a fraction of a single operating day's ~<!-- BEGIN energy:daily-wh-3 -->2,310<!-- END energy:daily-wh-3 --> Wh,
and incurred only once per resupply, not daily). *Worst case* — if a tote had to be pumped
out entirely with no gravity assist (~600 L) — it would be ~<!-- BEGIN energy:drain-full-min -->45<!-- END energy:drain-full-min --> min each, ~<!-- BEGIN energy:drain-full-wh -->94<!-- END energy:drain-full-wh --> Wh for both;
still minor. (Brown is normally *recycled* through the filter for the first wash rather than
dumped; this line covers the case where it is drained off.)

---

## 7. Solar Balance & Battery Autonomy

| | Value |
|---|--:|
| Solar generation (600 W × 5.5 peak-sun-h, Palm Springs) | ~<!-- BEGIN energy:solar-wh-day -->3,300<!-- END energy:solar-wh-day --> Wh/day |
| Battery usable (200 Ah × 12 V LiFePO4, 100% DoD) | <!-- BEGIN energy:battery-wh-2pack -->2,400<!-- END energy:battery-wh-2pack --> Wh |

| Day | Daily draw | Solar net | Within one battery charge? |
|---|--:|--:|---|
| 2 prints | ~<!-- BEGIN energy:daily-wh-2 -->1,576<!-- END energy:daily-wh-2 --> | **+<!-- BEGIN energy:solar-net-2 -->1,724<!-- END energy:solar-net-2 -->** | Yes (with wide margin) |
| 3 prints | ~<!-- BEGIN energy:daily-wh-3 -->2,310<!-- END energy:daily-wh-3 --> | **+<!-- BEGIN energy:solar-net-3 -->990<!-- END energy:solar-net-3 -->** | Yes — full overnight autonomy |
| 4 prints | ~<!-- BEGIN energy:daily-wh-4 -->3,044<!-- END energy:daily-wh-4 --> | **+<!-- BEGIN energy:solar-net-4 -->256<!-- END energy:solar-net-4 -->** | Exceeds the <!-- BEGIN energy:battery-wh-2pack -->2,400<!-- END energy:battery-wh-2pack --> Wh battery by ~<!-- BEGIN energy:over-battery-4 -->644<!-- END energy:over-battery-4 --> Wh → covered by **daytime solar** (which runs during the prints), not battery alone |

**Conclusions:**
- The system is **solar-positive at every realistic daily throughput** — even a 4-print
  day generates more than it consumes, so it sustains indefinitely on sun.
- A **3-print day fits within a 2-pack battery charge** (2×100 Ah = 2,400 Wh), giving a full
  day of operation on a dead-cloudy day from the battery alone. **The standard build is 1 pack
  (1,200 Wh)** — good for ~1.5 prints battery-alone, relying on daytime solar for the rest; the
  2nd pack is the optional config analyzed in §8.
- A **4-print day relies on the panels topping up during the day** (the loads run in
  daylight, so this is normally fine); a fully overcast day supports ~3 prints. The
  higher-draw AC cooler (~<!-- BEGIN fact:evap_cooler_w_bus -->97<!-- END fact:evap_cooler_w_bus --> W) puts the 4-print battery
  shortfall at ~521 Wh — still solar-covered, but battery-only 4-print days are off the table.
- The dominant load is **climate control (fans + evaporative cooler, ~2,050 Wh/day)**, not
  imaging or pumping — the biggest lever on daily energy is *cooling runtime*, not the
  print workflow.

---

## 8. Disconnected Endurance — How Long Off-Grid?

The question: with **no AC charge** (a remote deployment running on solar top-up + the
battery alone), how long can the system operate — and does adding the **second battery
pack** extend it? Two limits compete: **power** and **clean water**.

### 8.1 Power is not the limit (with sun)

Solar generates ~<!-- BEGIN energy:solar-wh-day -->3,300<!-- END energy:solar-wh-day --> Wh/day; a 3-print day draws ~<!-- BEGIN energy:daily-wh-3 -->2,310<!-- END energy:daily-wh-3 --> Wh — a **+<!-- BEGIN energy:solar-net-3 -->990<!-- END energy:solar-net-3 --> Wh/day surplus**,
so on sunny days the battery never depletes and the system runs **indefinitely**. The
battery's job is to ride out *cloudy* days, and that reserve is what the pack count changes:

| Battery | Usable | No-sun reserve (at ~<!-- BEGIN energy:daily-wh-3 -->2,310<!-- END energy:daily-wh-3 --> Wh/day) | With sun |
|---|--:|--:|---|
| **1 pack** (1×100 Ah) | <!-- BEGIN energy:battery-wh-1pack -->1,200<!-- END energy:battery-wh-1pack --> Wh | ~<!-- BEGIN energy:reserve-1pack-day -->0.5<!-- END energy:reserve-1pack-day --> day (≈ 2 prints) | Indefinite (solar-positive) |
| **2 packs** (2×100 Ah) | <!-- BEGIN energy:battery-wh-2pack -->2,400<!-- END energy:battery-wh-2pack --> Wh | ~<!-- BEGIN energy:reserve-2pack-day -->1.0<!-- END energy:reserve-2pack-day --> day (≈ 3 prints) | Indefinite (solar-positive) |

So the **second pack does not lengthen the deployment** — it buys a **cloudy-day buffer**
(ride out ~1 fully-overcast day instead of half a day) and the headroom for a 4-print day
(which exceeds a single 100 Ah pack). On solar, even one pack sustains operation forever.

### 8.2 Clean water *is* the limit

Power being effectively unlimited on sun, the binding constraint is the **fresh (Blue)
water supply**. Each print consumes **~<!-- BEGIN fact:blue_per_print_gal -->30<!-- END fact:blue_per_print_gal --> gal (<!-- BEGIN fact:blue_per_print_l -->114<!-- END fact:blue_per_print_l --> L) of net Blue water** even with Brown
recycling ([Water System Report §3–4](water-system-report.md)), so:

| Constraint | Capacity | Per print | Endurance |
|---|--:|--:|---|
| **Clean water (Blue, in)** | <!-- BEGIN fact:blue_supply_l -->1,800<!-- END fact:blue_supply_l --> L (<!-- BEGIN fact:blue_supply_gal -->476<!-- END fact:blue_supply_gal --> gal) | <!-- BEGIN fact:blue_per_print_l -->114<!-- END fact:blue_per_print_l --> L (<!-- BEGIN fact:blue_per_print_gal -->30<!-- END fact:blue_per_print_gal --> gal) | **~<!-- BEGIN fact:prints_per_resupply -->15<!-- END fact:prints_per_resupply --> prints ≈ 5 days** @ 3/day |
| Power, 2 packs + sun | — | ~<!-- BEGIN energy:per-print-wh -->734<!-- END energy:per-print-wh --> Wh | Indefinite |
| Power, 2 packs, no sun | <!-- BEGIN energy:battery-wh-2pack -->2,400<!-- END energy:battery-wh-2pack --> Wh | ~<!-- BEGIN energy:per-print-wh -->734<!-- END energy:per-print-wh --> Wh | ~3 prints (~<!-- BEGIN energy:reserve-2pack-day -->1.0<!-- END energy:reserve-2pack-day --> day) |

A disconnected deployment therefore runs **~<!-- BEGIN fact:prints_per_resupply -->15<!-- END fact:prints_per_resupply --> prints (~4.7 days at 3/day)** before it needs
a **resupply run** — which is fundamentally a *water* event (refill Blue), not a charging
event.

### 8.3 The waste side is a second limit

The endurance is bounded on **both ends of the water loop**. The **Black (waste) tote fills to ~600 L** (a 1,000 L tote at its working fill) — a *parallel* out-flow limit: in fully self-contained field use (no sewer, waste
pumped out to a hauler for disposal), the waste tank can fill before the Blue tank empties, so a
resupply run must **empty Black as well as refill Blue**. If waste cannot be disposed at
all, that — not power or fresh water — becomes the hard stop.

### 8.4 Verdict

- **The deployment length is set by clean water (~<!-- BEGIN fact:prints_per_resupply -->15<!-- END fact:prints_per_resupply --> prints / ~4.7 days), not power.**
- **One vs two battery packs does not change that** — both run indefinitely on sun. The
  second pack buys a **~1-day cloudy-weather reserve** (vs ~half a day) and enables 4-print
  days; for a *fresh-water-limited* 10-print deployment, a single pack is energetically
  sufficient on solar, with the second pack a resilience upgrade rather than an
  endurance one.

---

## 9. Source References

1. [Electrical Report §3](electrical-report.md) — power budget and the per-session itemized energy.
2. [Water System Report §3, §6–7](water-system-report.md) — wash cycles, the flow-through wash, and the Brown/Waste drain-out ports.
3. [Plumbing Report §5.3](plumbing-report.md) — P-03 (Waste evac) and P-05 (Brown drain) duties; the ~120 L gravity-drain residual.
4. [Cost Analysis](cost-analysis-report.md) — the capital build cost and savings levers.
