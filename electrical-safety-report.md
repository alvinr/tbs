<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Electrical Safety Report

## 1. Purpose & Scope

TBS-001 is a **steel (electrically conductive) shipping container** housing a
**direct-current electrical system** alongside **water and wet photo-chemistry**.
That combination triggers a reasonable concern about electrical safety. This report
assesses the hazards specifically created by that environment, documents the controls
already in the design, and specifies the protective measures added to close the
residual gaps.

It covers the 12 V DC power system (solar → MPPT → LiFePO4 → distribution → loads),
its interaction with the conductive enclosure and the wet zones, and the **two AC
interfaces** — the external shore-power charger and the dedicated **Circuit-E cooler
inverter** (12 V→120 V; isolation/GFCI design in [electrical §7.6](electrical-report.md#ac-safety)).
It does **not** re-derive the power budget or component selection — see the
[Electrical Report](electrical-report.md).

---

## 2. The Key Insight — This Is a Fire-Risk Problem, Not a Shock Problem

The intuition "electricity + liquids + a conductive metal box = electrocution" is the
right instinct to check, but it **largely does not apply here**, because of one
deliberate architectural choice:

> **Everything inside the container runs at 12 V DC. There is no grid-AC distribution
> inside the container** ([Electrical Report §2](electrical-report.md)).

12 V DC is **Extra-Low Voltage (ELV)** — below every shock-safety threshold in the
recognized standards, **including wet and immersed conditions**:

| Condition | Conventional safe touch-voltage limit (DC) | TBS-001 |
|---|---|---|
| Dry | ≤ 120 V DC (IEC 61140 / 60364-4-41 SELV) | 12 V ✓ |
| Wet / damp location | ≤ 60 V DC | 12 V ✓ |
| Immersed / submerged body | ≤ 30 V DC (and lower in some codes) | 12 V ✓ |

A worst-case wet contact (12 V across a ~300 Ω immersed-body resistance) is ~40 mA DC —
perceptible, but an order of magnitude below the ~300 mA+ ventricular-fibrillation
threshold for DC, which is itself far higher than for AC ([IEC/TS 60479-1 body-current
effects](https://webstore.iec.ch/publication/62920)). **You cannot get a dangerous
shock from the 12 V system, even standing in chemistry.**

**The one exception — Circuit E.** A single 12 V→120 V pure-sine inverter powers the
*outdoor* evaporative cooler; its 120 V AC output **is** a real shock hazard. It is the
*only* AC originating inside the box, kept off the 12 V distribution and contained by a
GFCI + single-point-bonding design ([electrical §7.6](electrical-report.md#ac-safety)) —
assessed as **Hazard #6** below. Everything *else* in the container is 12 V ELV.

So for the 12 V system the hazard model shifts from **electrocution → fire / arc /
corrosion / thermal**.
The LiFePO4 pack can deliver hundreds-to-thousands of amps into a fault, and **DC arcs
do not self-extinguish** (no current zero-crossing), so the real exposures are
*sustained short-circuit arcing, conductor/joint heating, and corrosion-driven
faults* — all of which are controlled by **fusing, isolation, sealing, and bonding**,
not by insulation against shock.

The closest applicable standard is **[ABYC E-11 — AC & DC Electrical Systems on
Boats](https://abycinc.org/)**: a low-voltage DC system in a conductive enclosure
exposed to water and spray is functionally the marine case, and E-11 (not the AC-oriented
NEC) is the right yardstick for fuse placement, conductor protection, and bonding.

---

## 3. Controls Already in the Design

These were specified independently of this review and form a sound baseline.

| Control | What it does | Source |
|---|---|---|
| **12 V DC distribution; AC isolated to Circuit E** | Eliminates the lethal-voltage path for every interior load except the one isolated, GFCI-protected cooler inverter (Hazard #6) | [Elec §2, §7.6](electrical-report.md) |
| **LiFePO4 chemistry** | No thermal runaway (unlike NMC / lead-acid); rated −20 to +60 °C for the hot container; internal per-cell BMS (over-current / over-temp / over-discharge) | [Elec §5.2](electrical-report.md) |
| **Layered fusing** | 200 A main fuse at the battery + per-circuit fuses (Blue Sea block) + 30 A per-string solar fuses | [Elec §7](electrical-report.md) |
| **Negative-ground bonding** | Steel shell bonded to battery-negative (4 AWG) + 8-ft earth stake — a positive-to-shell fault becomes a short the fuse clears | [Elec §7.3](electrical-report.md) |
| **IP-rated enclosures / penetrations** | IP65 distribution enclosure; IP67 Deutsch DT exterior connectors; IP67 MC4 solar | [Elec §5.4, §7.3](electrical-report.md) |
| **Protected, elevated routing** | Wiring in corrugated conduit + ceiling trunking, kept high and clear of the wet floor | [Elec §7.3](electrical-report.md) |

---

## 4. Hazard & Risk Assessment

Ranked by residual risk *as first assessed* — the Sev × Like ratings are the *pre-control*
values for the 12 V-DC-in-a-wet-conductive-box environment; the final column tracks how each
gap is now **closed** by the §5 controls.

| # | Hazard | Mechanism | Sev. | Like. | Existing control | Residual gap → closed by |
|---|--------|-----------|:----:|:-----:|------------------|--------------|
| 1 | **Sustained DC short / arc → fire** | LiFePO4 delivers huge fault current; DC arc won't self-extinguish. Chafed conductor on the steel shell, dropped tool on the busbar, or liquid bridging a terminal | High | Med | 200 A + per-circuit fuses, BMS | Main fuse far from battery; **no manual disconnect**; chafe not specified; **PV/charge side not load-break isolatable** → **all closed (§5 #1):** terminal-mount fuse, manual disconnect + **two E-stops (in/out)**, **PV disconnect**, **charge-line fuse**, **per-pack MRBF**, chafe protection |
| 2 | **Corroded wet-zone connections** | Developer/fixer vapor + condensation attacks unsealed terminals → high-resistance joints (heating) or intermittent faults. The 5 Shurflo pumps live in the wet IBC corridor / tray end | Med | High | IP65 enclosure (clean side only) | **Anderson Powerpole — not sealed**; wire not tinned → **closed (§5 #2):** sealed IP-rated connectors + tinned wire + dielectric grease |
| 3 | **Battery busbar arc-flash** | 200 A+ available; a dropped wrench arcs, throws molten metal, burns | High | Low | Fusing limits duration | **No terminal covers**; no insulated-tool note → **closed (§5 #3):** terminal covers + insulated-tool rule |
| 4 | **Battery thermal / venting** | Cells can vent under BMS failure / overcharge / abuse; container reaches 60 °C, and the BMS blocks charging above ~45 °C (mid-day charge lock-out) | High | Low | LiFePO4 (very stable), 60 °C rating, BMS | Charge lock-out > 45 °C → **closed (§5 #4):** thermal siting — low/shaded/cooled-air (§5.2); confirm < 45 °C at commissioning |
| 5 | **Shore-power AC** | Grid AC feeds the exterior charger only — but the *site supply* and any extension cord are a genuine electrocution hazard | High | Low | AC kept exterior (IP65 charger); never distributed inside | Depends on site RCD/GFCI + the operational rule → **managed (§5 #5 / §6):** exterior-only AC, site-RCD rule, commissioning check |
| 6 | **Circuit-E cooler inverter (120 V AC)** | The only interior-derived AC: a 12 V→120 V inverter feeds an outdoor, water-wetted cooler beside the grounded steel box — a line-to-metal shock path | High | Low | Separately-derived source, single-point neutral-ground bond; **GFCI** on the cooler outlet; shell/chassis/cooler equipotential bond; DC-side fuse + dedicated disconnect; transformer galvanic isolation ([electrical §7.6](electrical-report.md#ac-safety)) | → **managed (§6 / §7.6):** cooler unplugged + inverter DC-disconnect for transport; periodic GFCI trip test |

---

## 5. Improvements — Specified & Cascaded

Each §4 residual gap is closed by a measure now part of the design — **specified in full**
in [electrical §7.5 (Circuit Protection & Electrical Safety)](electrical-report.md) and
[§7.6 (Circuit-E AC Isolation)](electrical-report.md#ac-safety), and priced in
[electrical §8](electrical-report.md) / [Master Shopping List §6](master-shopping-list.md).
This report maps each gap to its control; it does not re-specify the hardware.

| Gap (Hazard #) | Control | Specified in |
|---|---|---|
| **#1** — DC short / arc | **Two E-stops (interior + exterior)** → magnetic-latch battery contactor; manual main disconnect; terminal-mount main fuse at the battery post; **PV array disconnect** (isolates the charge side the E-stops don't reach); **MPPT charge-line fuse**; **per-parallel-pack MRBF fuse**; chafe protection; equipotential bonding | elec §7.5, §5.1–5.2 |
| **#2** — wet-zone corrosion | Sealed IP-rated wet-zone connectors + tinned marine wire + dielectric grease; wet wiring elevated above the spill line with drip loops | elec §7.5 |
| **#3** — busbar arc-flash | Battery terminal covers + insulated-tool rule (the main disconnect also de-energizes the bus) | elec §7.5 |
| **#4** — battery thermal | Battery **sited low + shaded + in the cooled-air path** so it stays in the ≤45 °C charge window (the BMS blocks charging above ~45 °C); commissioning temperature check | elec §5.2 |
| **#5** — shore AC | Shore AC terminates at the exterior charger only; site RCD/GFCI rule (§6) | §6 |
| **#6** — Circuit-E AC | Single-point neutral-ground bond + mandatory GFCI + equipotential bond + DC fuse/disconnect + transformer galvanic isolation | elec §7.6 |

The #1–#3 / #5 measures were the cheap, high-value first tranche; all are now specified
and cascaded into the electrical BOM.

---

## 6. The Operational Rule That Matters Most

Keep the **12 V ELV boundary intact: no grid AC distributed inside the container, ever.**
The one designed-in AC branch — the Circuit-E cooler inverter — is deliberately isolated
and GFCI-protected (§7.6); apart from it, everything inside is 12 V ELV and this is a
fire-risk-management problem (fusing, isolation, sealing, bonding), not a life-safety
electrocution one.

- The shore-power AC input terminates at the **exterior** Victron charger only — never
  run an AC extension cord or generator output into the wet interior.
- Confirm the deployment **site's AC supply is on an RCD/GFCI-protected circuit** before
  connecting the shore charger.
- Plug the cooler into the Circuit-E GFCI outlet **only during sessions**; for transport,
  unplug it and open the inverter DC-disconnect (§7.6). Trip-test that GFCI periodically.

---

## 7. Commissioning & Periodic Checks

| When | Check |
|---|---|
| At commissioning | Main fuse ≤180 mm from battery +; disconnect operates; shell-to-battery-negative bond < 0.1 Ω; all metalwork bonded; terminal covers fitted |
| At commissioning | **Both E-stops** (interior + exterior) each trip the contactor; PV array disconnect operates; MPPT charge-line fuse present (60 A); each parallel pack has its own MRBF fuse |
| At commissioning | **Battery bay < 45 °C** under peak-sun load (thermal siting, §5.2); insulation check: positive-bus-to-shell resistance high with loads off |
| At commissioning | Circuit E: neutral-ground bonded at the inverter only; cooler-outlet GFCI trips on test; inverter chassis/cooler/shell bonded; DC disconnect operates |
| Before each session | Wet-zone connectors seated and dry; no liquid pooling at any connection |
| Before each cooling session | Trip-test the Circuit-E cooler-outlet GFCI; cord and outlet undamaged |
| Monthly | Terminals for corrosion/discoloration (heat); re-grease as needed; fuse and disconnect tight |
| Before shore connect | Site supply is RCD/GFCI-protected |

---

## 8. Source References

1. [ABYC E-11 — AC & DC Electrical Systems on Boats](https://abycinc.org/) — fuse placement (≤7"/180 mm from the source), DC conductor protection, and bonding for low-voltage DC in conductive, wet enclosures.
2. [IEC 61140 — Protection against electric shock](https://webstore.iec.ch/publication/4151) — extra-low-voltage (ELV/SELV) limits.
3. [IEC 60364-4-41 — Low-voltage installations: protection against electric shock](https://webstore.iec.ch/publication/63337) — SELV/PELV touch-voltage limits, including reduced limits for wet conditions.
4. [IEC/TS 60479-1 — Effects of current on human beings and livestock](https://webstore.iec.ch/publication/62920) — body-current thresholds (DC vs AC, fibrillation).
5. [NFPA 70 (NEC) Article 690 — Solar Photovoltaic Systems](https://www.nfpa.org/codes-and-standards/nfpa-70-standard-development/70) — PV-side fusing and disconnect practice.
6. [Blue Sea Systems — Circuit Protection / MRBF terminal fuses & m-Series switches](https://www.bluesea.com/) — terminal-mount fusing and battery disconnects.
7. [Electrical Report](electrical-report.md) — power architecture, battery, wiring, and the full parts list this report draws on.
8. [Plumbing Report](plumbing-report.md) · [Water System Report](water-system-report.md) — the wet-zone pumps and where electrics meet liquids.

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
