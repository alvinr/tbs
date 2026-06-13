#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
calculate_energy_budget.py — TBS-001 per-session energy budget

Computes itemized energy consumption for one complete print session
based on circuit power ratings and operating-manual phase timings.
Outputs a markdown table suitable for the electrical report.

Run:  python3 calculate_energy_budget.py
"""

# ── Circuit power ratings (watts) ─────────────────────────────────────────────
# From electrical-report.md §3 Power Budget table

FAN_EXHAUST_W   = 60    # Circuit A — 6" exhaust fan, far end wall high (AC Infinity S6)
FAN_INTAKE_W    = 60    # Circuit B — 6" intake fan, cargo door panel low (AC Infinity S6)
PUMP_W          = 90    # Circuit C — Shurflo 2088: 7.5A × 12V = 90W (one pump at a time)
SAFELIGHT_W     = 15    # Circuit D — red LED strips
COOLER_W        = 80    # Circuit E — 12V DC evaporative cooler
ACTUATOR_W      = 100   # Circuit F — film plane actuators (optional, peak)
WHITE_LIGHT_W   = 60    # Circuit G — 3× 20W LED panels

# ── Battery bank ──────────────────────────────────────────────────────────────

# Standard build = 1× 100Ah pack (cost). The distribution busbar + fuse block are
# provisioned for a 2nd 100Ah in parallel as a plug-in expansion (no rewiring) —
# the autonomy model below reports both 1- and 2-pack reserves.
BATTERY_AH_PER_PACK = 100
STANDARD_PACKS      = 1     # fitted in the standard build (2nd is ghosted/optional)
BATTERY_AH      = STANDARD_PACKS * BATTERY_AH_PER_PACK
BATTERY_V       = 12    # nominal voltage
DOD             = 1.0   # LiFePO4: 100% depth of discharge usable

# ── Solar array ───────────────────────────────────────────────────────────────

SOLAR_W         = 600   # 3× 200W panels
PEAK_SUN_HOURS  = 5.5   # Palm Springs annual average

# ── Phase durations (minutes) ─────────────────────────────────────────────────
# From operating-manual.md phase table and step-level timings.
# Only phases with electrical load are counted.
#
# Phase 0 (pre-departure) is at home — no battery draw.
# Phase 1.1–1.5 (mode conversion, light trap, water checks) draw negligible power.
# Electrical draw begins at Phase 1.6 (cooling warmup).

COOLING_WARMUP_MIN  = 30    # Phase 1.6: cooler + fans ON 30 min before entry
DARK_ADAPT_MIN      = 20    # Phase 1.7–1.8: ventilation check + dark adaptation
LOADING_MIN         = 45    # Phase 2: coat + dry under safelight
EXPOSURE_MIN        = 37.5  # Phase 3: midpoint of 30–45 min baseline
DEVELOPMENT_MIN     = 20    # Phase 4: 3× wash cycles + drain
CLEANUP_MIN         = 30    # Phase 5: ventilation flush + pack-down

# ── Pump runtimes per print (minutes) ─────────────────────────────────────────
# From water-system-report.md §8 electrical table.
# Pumps run one at a time (never simultaneous).

P01_BLUE_MIN    = 15    # 3× wash fills at 3.5 GPM
P02_BROWN_MIN   = 10    # recycled wash (if Brown stock available)
P04_DRAIN_MIN   =  5    # tray sump drain between washes
ACTUATOR_MIN    =  5    # brief positioning moves (optional)

# ── Daily operating model ─────────────────────────────────────────────────────
# A pinhole exposure uses one film plane at a time, so prints are sequential
# (~3h cycle each). The container is cooled ONCE in the morning; fans + cooler
# then run continuously. Standard build is manual (electric actuation dropped —
# see cost-analysis-report.md), so Circuit F draws nothing by default.

PRINTS_PER_DAY    = 3       # representative daylight field day (2 short / 4 pushed)
INCLUDE_ACTUATORS = False   # manual build is standard; set True to add Circuit F

# End-of-day Brown + Waste pump-out (P-05 Brown→X3, P-03 Waste→X4). Gravity-assisted:
# each tote gravity-drains through its low Z=200mm port; the pump lifts only the
# ~120L residual below the port (equipment-panel-report.md §4.3).
PUMP_LPM          = 13.2    # 3.5 GPM Shurflo 2088
DRAIN_RESIDUAL_L  = 120     # residual below the X3/X4 port, pumped per tote
DRAIN_LIGHT_MIN   = 10      # white light during the ~20-min drain operation

# ── Water supply (clean-water autonomy) ───────────────────────────────────────
# The binding endurance constraint for a disconnected (solar-only) deployment is
# usually the FRESH water supply, not power. From water-system-report.md §3-4.
BLUE_SUPPLY_L       = 1200  # 2× 600L Blue (fresh) totes (= 316 US gal)
FRESH_PER_PRINT_GAL = 32    # net Blue consumed per print WITH Brown recycling (wash 2 from Brown)
WASTE_CAP_L         = 600   # 1× Black (waste) tote — parallel out-flow constraint
GAL_TO_L            = 3.785

# ── Phase-by-phase load matrix ────────────────────────────────────────────────
# Each phase specifies which circuits are ON and for how long.
# Pumps and actuators are itemized separately (they don't run for
# the full phase duration).

phases = [
    {
        "name":     "1.6  Cooling warmup",
        "minutes":  COOLING_WARMUP_MIN,
        "loads": {
            "Fan A (exhaust)":  FAN_EXHAUST_W,
            "Fan B (intake)":   FAN_INTAKE_W,
            "Evap cooler":      COOLER_W,
        },
    },
    {
        "name":     "1.7–1.8  Dark adaptation",
        "minutes":  DARK_ADAPT_MIN,
        "loads": {
            "Fan A (exhaust)":  FAN_EXHAUST_W,
            "Fan B (intake)":   FAN_INTAKE_W,
            "Evap cooler":      COOLER_W,
            "Safelight":        SAFELIGHT_W,
        },
    },
    {
        "name":     "2  Load image plane",
        "minutes":  LOADING_MIN,
        "loads": {
            "Fan A (exhaust)":  FAN_EXHAUST_W,
            "Fan B (intake)":   FAN_INTAKE_W,
            "Evap cooler":      COOLER_W,
            "Safelight":        SAFELIGHT_W,
        },
    },
    {
        "name":     "3  Exposure",
        "minutes":  EXPOSURE_MIN,
        "loads": {
            "Fan A (exhaust)":  FAN_EXHAUST_W,
            "Fan B (intake)":   FAN_INTAKE_W,
            "Evap cooler":      COOLER_W,
        },
    },
    {
        "name":     "4  Development & wash",
        "minutes":  DEVELOPMENT_MIN,
        "loads": {
            "Fan A (exhaust)":  FAN_EXHAUST_W,
            "Fan B (intake)":   FAN_INTAKE_W,
            "Evap cooler":      COOLER_W,
            "White light":      WHITE_LIGHT_W,
        },
    },
    {
        "name":     "5  Cleanup",
        "minutes":  CLEANUP_MIN,
        "loads": {
            "Fan A (exhaust)":  FAN_EXHAUST_W,
            "Fan B (intake)":   FAN_INTAKE_W,
            "Evap cooler":      COOLER_W,
            "White light":      WHITE_LIGHT_W,
        },
    },
]

# Standalone items that span multiple phases (runtime is total, not per-phase)
standalone_items = [
    ("Pumps (P-01 Blue)",       PUMP_W, P01_BLUE_MIN),
    ("Pumps (P-02 Brown)",      PUMP_W, P02_BROWN_MIN),
    ("Pumps (P-04 drain)",      PUMP_W, P04_DRAIN_MIN),
    ("Actuators (optional)",    ACTUATOR_W, ACTUATOR_MIN),
]


def compute():
    """Return (phase_rows, standalone_rows, total_wh, summary_dict)."""
    phase_rows = []
    total_wh = 0.0
    total_min = 0.0

    for ph in phases:
        hours = ph["minutes"] / 60.0
        phase_wh = 0.0
        load_names = []
        for name, watts in ph["loads"].items():
            wh = watts * hours
            phase_wh += wh
            load_names.append(name)
        phase_rows.append({
            "phase": ph["name"],
            "minutes": ph["minutes"],
            "loads": ", ".join(ph["loads"].keys()),
            "power": sum(ph["loads"].values()),
            "wh": phase_wh,
        })
        total_wh += phase_wh
        total_min += ph["minutes"]

    standalone_rows_out = []
    standalone_wh = 0.0
    for name, watts, mins in standalone_items:
        wh = watts * (mins / 60.0)
        standalone_rows_out.append({
            "name": name,
            "watts": watts,
            "minutes": mins,
            "wh": wh,
        })
        standalone_wh += wh
        total_wh += wh

    battery_wh = BATTERY_AH * BATTERY_V * DOD
    sessions_per_charge = battery_wh / total_wh
    solar_wh_day = SOLAR_W * PEAK_SUN_HOURS

    summary = {
        "total_continuous_min": total_min,
        "total_continuous_h": total_min / 60.0,
        "standalone_wh": standalone_wh,
        "total_wh": total_wh,
        "total_kwh": total_wh / 1000.0,
        "battery_wh": battery_wh,
        "sessions_per_charge": sessions_per_charge,
        "solar_wh_day": solar_wh_day,
        "recharge_prints_day": solar_wh_day / total_wh,
    }

    return phase_rows, standalone_rows_out, total_wh, summary


# ── Daily roll-up + disconnected-endurance (autonomy) model ───────────────────

def _phase_wh(ph):
    return sum(ph["loads"].values()) * ph["minutes"] / 60.0


def warmup_wh():
    """One-time-per-day cooling warmup (Phase 1.6)."""
    return _phase_wh(phases[0])


def per_print_wh(include_actuators=INCLUDE_ACTUATORS):
    """Energy for one print cycle EXCLUDING the one-time morning warmup."""
    cont = sum(_phase_wh(ph) for ph in phases[1:])            # dark-adapt … cleanup
    pumps = sum(w * m / 60.0 for n, w, m in standalone_items
                if not (("Actuator" in n) and not include_actuators))
    return cont + pumps


def end_of_day_drain_wh():
    """End-of-day Brown (P-05→X3) + Waste (P-03→X4) pump-out — gravity-assisted residual."""
    pump_min_per_tote = DRAIN_RESIDUAL_L / PUMP_LPM
    pump_wh = 2 * PUMP_W * pump_min_per_tote / 60.0
    light_wh = WHITE_LIGHT_W * DRAIN_LIGHT_MIN / 60.0
    return pump_wh + light_wh


def compute_daily(n=PRINTS_PER_DAY, include_actuators=INCLUDE_ACTUATORS):
    """Energy for one full operating day of `n` sequential prints."""
    w = warmup_wh()
    pp = per_print_wh(include_actuators)
    drain = end_of_day_drain_wh()
    return {"n": n, "warmup_wh": w, "per_print_wh": pp, "drain_wh": drain,
            "daily_wh": w + n * pp + drain}


def compute_autonomy(battery_ah, prints_per_day=PRINTS_PER_DAY):
    """Disconnected (no AC charge) endurance: power vs clean-water limited."""
    daily = compute_daily(prints_per_day)["daily_wh"]
    battery_wh = battery_ah * BATTERY_V * DOD
    solar = SOLAR_W * PEAK_SUN_HOURS
    fresh_l = FRESH_PER_PRINT_GAL * GAL_TO_L
    prints_water = BLUE_SUPPLY_L / fresh_l
    return {
        "battery_ah": battery_ah, "battery_wh": battery_wh,
        "prints_per_day": prints_per_day, "daily_wh": daily,
        "battery_only_days": battery_wh / daily,        # no sun at all
        "solar_wh_day": solar, "solar_net_wh": solar - daily,  # >0 ⇒ indefinite with sun
        "prints_water": prints_water,                    # ← usual binding limit
        "days_water": prints_water / prints_per_day,
    }


def print_daily_report():
    d = compute_daily()
    print("\n" + "=" * 72)
    print(f"DAILY MODEL — {d['n']} sequential prints/day"
          f" ({'manual' if not INCLUDE_ACTUATORS else 'with actuators'})")
    print("=" * 72)
    print(f"  Morning cooling warmup (once)   : {d['warmup_wh']:6.0f} Wh")
    print(f"  Per print (cycle + wash/drain)  : {d['per_print_wh']:6.0f} Wh  × {d['n']}"
          f" = {d['per_print_wh']*d['n']:6.0f} Wh")
    print(f"  End-of-day Brown+Waste pump-out : {d['drain_wh']:6.0f} Wh")
    print(f"  ── Daily total                  : {d['daily_wh']:6.0f} Wh")
    print(f"\n  2 prints: {compute_daily(2)['daily_wh']:.0f} Wh   "
          f"4 prints: {compute_daily(4)['daily_wh']:.0f} Wh")

    print("\n" + "=" * 72)
    print("DISCONNECTED ENDURANCE (no AC charge — solar top-up only)")
    print("=" * 72)
    fresh_l = FRESH_PER_PRINT_GAL * GAL_TO_L
    print(f"  CLEAN WATER (Blue {BLUE_SUPPLY_L}L / {fresh_l:.0f}L net per print)"
          f" → {BLUE_SUPPLY_L/fresh_l:.1f} prints"
          f" ≈ {BLUE_SUPPLY_L/fresh_l/PRINTS_PER_DAY:.1f} days @ {PRINTS_PER_DAY}/day")
    print(f"  WASTE OUT (Black {WASTE_CAP_L}L) — must be emptied at resupply (parallel limit)\n")
    for ah, label in [(100, "1 pack (100Ah)"), (200, "2 packs (200Ah)")]:
        a = compute_autonomy(ah)
        sun = "INDEFINITE (solar-positive)" if a["solar_net_wh"] > 0 else "solar-negative"
        print(f"  {label:18s}: battery {a['battery_wh']:.0f}Wh →"
              f" {a['battery_only_days']:.1f} day no-sun reserve;"
              f" with sun: {sun} (+{a['solar_net_wh']:.0f} Wh/day)")
    print("\n  ⇒ Endurance is CLEAN-WATER limited, not power limited. Battery count sets the"
          "\n    cloudy-day reserve + peak daily throughput, NOT the deployment length.")


def print_report():
    phase_rows, standalone_rows, total_wh, s = compute()

    print("=" * 72)
    print("TBS-001 ENERGY BUDGET PER PRINT SESSION")
    print("=" * 72)

    # Phase table
    print("\n### Continuous loads by phase\n")
    print(f"| {'Phase':<28} | {'Min':>5} | {'Loads':<42} | {'W':>5} | {'Wh':>7} |")
    print(f"|{'-'*30}|{'-'*7}|{'-'*44}|{'-'*7}|{'-'*9}|")
    phase_total_wh = 0.0
    for r in phase_rows:
        mins = r["minutes"]
        mins_str = f"{mins:.0f}" if mins == int(mins) else f"{mins:.1f}"
        print(f"| {r['phase']:<28} | {mins_str:>5} | {r['loads']:<42} | {r['power']:>5} | {r['wh']:>7.1f} |")
        phase_total_wh += r["wh"]
    print(f"| {'**Subtotal (continuous)**':<28} | {s['total_continuous_min']:>5.0f} |"
          f" {'':<42} |       | {phase_total_wh:>7.1f} |")

    # Standalone items
    print(f"\n### Intermittent loads (total runtime per print)\n")
    print(f"| {'Item':<28} | {'W':>5} | {'Min':>5} | {'Wh':>7} |")
    print(f"|{'-'*30}|{'-'*7}|{'-'*7}|{'-'*9}|")
    for r in standalone_rows:
        print(f"| {r['name']:<28} | {r['watts']:>5} | {r['minutes']:>5} | {r['wh']:>7.1f} |")
    print(f"| {'**Subtotal (intermittent)**':<28} |       |       | {s['standalone_wh']:>7.1f} |")

    # Grand total
    print(f"\n**Total energy per session: {s['total_wh']:.0f} Wh ({s['total_kwh']:.2f} kWh)**\n")

    # Battery and solar
    print(f"### Battery and solar\n")
    print(f"| Parameter | Value |")
    print(f"|-----------|-------|")
    print(f"| Battery capacity | {BATTERY_AH} Ah × {BATTERY_V}V = {s['battery_wh']:.0f} Wh |")
    print(f"| Sessions per full charge | {s['sessions_per_charge']:.1f} |")
    print(f"| Solar generation | {SOLAR_W}W × {PEAK_SUN_HOURS}h = {s['solar_wh_day']:.0f} Wh/day |")
    print(f"| Solar sessions/day | {s['recharge_prints_day']:.1f} |")


def generate_markdown():
    """Return the markdown text for the energy budget section."""
    phase_rows, standalone_rows, total_wh, s = compute()

    lines = []

    lines.append("### 3.1 Itemized Energy Budget (per print session)\n")
    lines.append("*Generated by `calculate_energy_budget.py` — rerun after any specification change.*\n")

    # Phase table
    lines.append("**Continuous loads by phase:**\n")
    lines.append("| Phase | Min | Active circuits | W | Wh |")
    lines.append("|-------|----:|-----------------|--:|---:|")
    phase_total_wh = 0.0
    for r in phase_rows:
        mins = r["minutes"]
        mins_str = f"{mins:.0f}" if mins == int(mins) else f"{mins:.1f}"
        lines.append(f"| {r['phase']} | {mins_str} | {r['loads']} | {r['power']} | {r['wh']:.0f} |")
        phase_total_wh += r["wh"]
    lines.append(f"| **Subtotal** | **{s['total_continuous_min']:.0f}** | | | **{phase_total_wh:.0f}** |")

    # Standalone items
    lines.append("\n**Intermittent loads (total runtime per print):**\n")
    lines.append("| Item | W | Min | Wh |")
    lines.append("|------|--:|----:|---:|")
    for r in standalone_rows:
        lines.append(f"| {r['name']} | {r['watts']} | {r['minutes']} | {r['wh']:.1f} |")
    lines.append(f"| **Subtotal** | | | **{s['standalone_wh']:.0f}** |")

    lines.append(f"\n**Total energy per session: {s['total_wh']:.0f} Wh ({s['total_kwh']:.2f} kWh)**")

    lines.append(f"\n**Battery bank capacity:** {BATTERY_AH} Ah × {BATTERY_V}V"
                 f" = {s['battery_wh']:.0f} Wh (LiFePO4, 100% DoD)"
                 f" → **{s['sessions_per_charge']:.1f} full sessions per charge**.")

    lines.append(f"\n**Solar recharge:** {SOLAR_W}W array × {PEAK_SUN_HOURS} peak sun hours"
                 f" (Palm Springs) = {s['solar_wh_day']:.0f} Wh/day"
                 f" → supports {s['recharge_prints_day']:.1f} sessions/day from solar alone.")

    return "\n".join(lines)


if __name__ == "__main__":
    print_report()
    print_daily_report()
    print("\n" + "=" * 72)
    print("MARKDOWN OUTPUT (for electrical-report.md §3.1):")
    print("=" * 72 + "\n")
    print(generate_markdown())
