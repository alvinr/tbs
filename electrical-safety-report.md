# Electrical Safety Report

## 1. Purpose & Scope

TBS-001 is a **steel (electrically conductive) shipping container** housing a
**direct-current electrical system** alongside **water and wet photo-chemistry**.
That combination triggers a reasonable concern about electrical safety. This report
assesses the hazards specifically created by that environment, documents the controls
already in the design, and specifies the protective measures added to close the
residual gaps.

It covers the 12 V DC power system (solar → MPPT → LiFePO4 → distribution → loads),
its interaction with the conductive enclosure and the wet zones, and the single
external AC interface (the shore-power charger). It does **not** re-derive the power
budget or component selection — see the [Electrical Report](electrical-report.md).

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

So the hazard model shifts from **electrocution → fire / arc / corrosion / thermal**.
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
| **12 V DC only; no interior AC** | Eliminates the lethal-voltage path entirely | [Elec §2](electrical-report.md) |
| **LiFePO4 chemistry** | No thermal runaway (unlike NMC / lead-acid); rated −20 to +60 °C for the hot container; internal per-cell BMS (over-current / over-temp / over-discharge) | [Elec §5.2](electrical-report.md) |
| **Layered fusing** | 200 A main fuse at the battery + per-circuit fuses (Blue Sea block) + 30 A per-string solar fuses | [Elec §7](electrical-report.md) |
| **Negative-ground bonding** | Steel shell bonded to battery-negative (4 AWG) + 8-ft earth stake — a positive-to-shell fault becomes a short the fuse clears | [Elec §7.3](electrical-report.md) |
| **IP-rated enclosures / penetrations** | IP65 distribution enclosure; IP67 Deutsch DT exterior connectors; IP67 MC4 solar | [Elec §5.4, §7.3](electrical-report.md) |
| **Protected, elevated routing** | Wiring in corrugated conduit + ceiling trunking, kept high and clear of the wet floor | [Elec §7.3](electrical-report.md) |

---

## 4. Hazard & Risk Assessment

Ranked by residual risk *before* the §5 improvements. Severity × likelihood for the
12 V-DC-in-a-wet-conductive-box environment.

| # | Hazard | Mechanism | Sev. | Like. | Existing control | Residual gap |
|---|--------|-----------|:----:|:-----:|------------------|--------------|
| 1 | **Sustained DC short / arc → fire** | LiFePO4 delivers huge fault current; DC arc won't self-extinguish. Chafed conductor on the steel shell, dropped tool on the busbar, or liquid bridging a terminal | High | Med | 200 A + per-circuit fuses, BMS | Main fuse may be ~0.5 m from the battery (cable unprotected); **no manual disconnect**; chafe protection at shell penetrations not specified |
| 2 | **Corroded wet-zone connections** | Developer/fixer vapor + condensation attacks unsealed terminals → high-resistance joints (heating) or intermittent faults. The 5 Shurflo pumps live in the wet IBC corridor / tray end | Med | High | IP65 enclosure (clean side only) | **Interior connectors are Anderson Powerpole — not sealed**; wet-zone wire not specified tinned |
| 3 | **Battery busbar arc-flash** | 200 A+ available; a dropped wrench arcs, throws molten metal, burns | High | Low | Fusing limits duration | **No terminal covers**; no insulated-tool note |
| 4 | **Battery thermal / venting** | Cells can vent under BMS failure / overcharge / abuse; container reaches 60 °C | High | Low | LiFePO4 (very stable), 60 °C rating, BMS | Confirm the mounted location has airflow and isn't a sealed, sun-baked pocket |
| 5 | **Shore-power AC (the one lethal node)** | Grid AC feeds the exterior charger only — but the *site supply* and any extension cord are a genuine electrocution hazard | High | Low | AC kept exterior (IP65 charger); never distributed inside | Depends on the **site supply being RCD/GFCI-protected**; operational rule must be enforced |

---

## 5. Improvements — Specified & Cascaded

The following measures are now part of the design and BOM ([Electrical Report §8](electrical-report.md),
[Master Shopping List §6](master-shopping-list.md)).

### 5.1 Do First (cheap, closes real gaps)

| Measure | Detail | Closes |
|---|---|---|
| **External emergency cut-off (E-stop)** | A red weatherproof E-stop (IP66) on the external power-panel face trips a magnetic-latch contactor (Blue Sea ML-RBS) in the battery + feed — kills all DC power **from outside the container, without entry**, at zero standby draw | #1 |
| **Battery main disconnect switch** | A manual isolator (Blue Sea m-Series 300 A) between the contactor and the distribution busbar — maintenance / service de-energization (a fuse is not a switch) | #1, #3 |
| **Fuse at the battery terminal** | Relocate the main fuse to within **≤180 mm of the battery + post** (ABYC E-11) — terminal-mount MRBF fuse — so the main cable is protected along its whole length | #1 |
| **Battery terminal covers + tool rule** | Insulating boots over both posts/busbar; "insulated tools only at the busbar" maintenance note | #3 |
| **Sealed wet-zone connections** | Replace the Anderson Powerpoles on the pump circuits with IP-rated connectors (Deutsch DT or adhesive-lined heat-shrink); **tinned marine-grade wire** on wet runs; **dielectric grease** on any terminal exposed to chemistry vapor | #2 |

### 5.2 Do Next

| Measure | Detail | Closes |
|---|---|---|
| **Chafe protection at shell penetrations** | Rubber grommets / cable glands at every steel-shell pass-through; keep + and − conductors paired/sheathed to minimize the loop a fault could energize | #1 |
| **Elevate wet-zone wiring** | Route pump wiring above the spill/flood line; drip loops; no connectors at the lowest point where liquid pools | #2 |
| **Equipotential bonding of metalwork** | Bond the IBC stacking frame, walkways, and tray-adjacent metal to the battery-negative reference (6 AWG) — minor for shock at 12 V, but it guarantees clean fault-clearing and removes stray potentials | #1 |
| **Confirm battery thermal margin** | Verify the mounted location (pinhole wall, near the EP) has airflow and stays within the LiFePO4 rating in a 60 °C container | #4 |

---

## 6. The Operational Rule That Matters Most

Keep the **12 V ELV boundary intact: no grid AC inside the container, ever.** As long
as that holds, this is a fire-risk-management problem (fully addressed by fusing,
isolation, sealing, and bonding), not a life-safety electrocution problem.

- The shore-power AC input terminates at the **exterior** Victron charger only — never
  run an AC extension cord or generator output into the wet interior.
- Confirm the deployment **site's AC supply is on an RCD/GFCI-protected circuit** before
  connecting the shore charger.

---

## 7. Commissioning & Periodic Checks

| When | Check |
|---|---|
| At commissioning | Main fuse ≤180 mm from battery +; disconnect operates; shell-to-battery-negative bond < 0.1 Ω; all metalwork bonded; terminal covers fitted |
| At commissioning | Insulation check: positive-bus-to-shell resistance high (no leakage) with loads off |
| Before each session | Wet-zone connectors seated and dry; no liquid pooling at any connection |
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
8. [Equipment Panel Report](equipment-panel-report.md) · [Water System Report](water-system-report.md) — the wet-zone pumps and where electrics meet liquids.
