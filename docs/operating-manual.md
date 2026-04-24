# Operating Manual — TBS-001

**The Big Shoebox Project — Camera No. 1**
Single-operator workflow for cyanotype on cotton muslin.

> **Before you begin:** Read this manual end-to-end once before your first deployment. Each phase has a time estimate and a GO/NO-GO checkpoint. Do not proceed past a checkpoint unless all conditions are met.

---

## Quick Reference

| Phase | What | Time |
|-------|------|------|
| 0 | Pre-deployment setup | ~2 hours |
| 1 | Chemistry preparation | ~30 min |
| 2 | Load image plane (darkness) | ~45 min |
| 3 | Exposure | ~2 hr (baseline) |
| 4 | Development | ~20 min |
| 5 | Cleanup and close-down | ~30 min |
| **Total** | **First print, ideal conditions** | **~5–6 hours** |

Baseline exposure is **30–45 minutes** under direct full sun (Mike Ware New Cyanotype formula on cotton muslin, ISO equivalent ~2–4; no reciprocity correction required). See the [Exposure Adjustment Table](#exposure-adjustment-table) for cloud cover and time-of-day corrections.

---

## Phase 0 — Pre-Deployment Setup

**Time: ~2 hours. Complete the day before or early on shoot day.**

### 0.1 Site Selection

- [ ] Ground is level to within 5° (use a spirit level on the container floor after delivery)
- [ ] Subject is visible from the pinhole wall — nothing blocking the view within 5m
- [ ] Shade structure can be erected over the container (trees, canopy, building shadow)
- [ ] Solar panel deployment area: clear southern exposure, ~4m × 3m
- [ ] Water source within 20m, or tanker access for IBC tote fill
- [ ] Emergency vehicle access not blocked by container placement

### 0.2 Container Positioning

1. Direct the delivery driver to position the container with the **cargo doors facing away from the subject**. The pinhole wall faces the subject.
2. Once set down, check level. Use 50mm timber sleepers under corner castings to correct — up to 50mm height difference is manageable without shimming the mechanism.
3. Open cargo doors and inspect interior:
   - No water ingress or condensation on image plane
   - All seals (door perimeter, neoprene cord) are intact
   - Film plane mechanism moves freely on all four corners

### 0.3 Light Trap Vestibule

1. Bolt the vestibule frame to the container corner castings (8 × M10 bolts, 30 Nm torque).
2. Check that the S-path baffles are seated flat against the vestibule walls.
3. Hang the three-layer Duvetyne blackout curtains inside the vestibule — check overlaps are a minimum of 200mm at each layer.
4. Verify: stand inside the closed vestibule with the outer door closed and container door open. Wait 2 minutes for dark adaptation. **No light should be visible from any angle.** Mark any leaks with chalk and seal with black gaffer tape before proceeding.

> **Safety:** The vestibule inner door operates the same as the main container cargo doors. Familiarise yourself with the latching mechanism before entering in darkness.

### 0.4 Solar Power System

1. Deploy solar panels on south-facing ground or roof rack, angled at 30° from horizontal (optimal for Palm Springs latitude).
2. Connect panels in parallel to the Victron SmartSolar MPPT 100/50 controller.
3. Connect controller to battery bank (2 × 100Ah LiFePO4 in parallel). **Observe polarity.**
4. Connect Blue Sea fuse block to battery positive busbar.
5. Check controller display: battery voltage should read 12.6–13.2V (full charge). If below 12.0V, charge before proceeding — a depleted battery bank cannot power the cooler and water system simultaneously.
6. Verify each circuit fuse is seated: A (intake fan), B (exhaust fan), C (water pump), D (safelight), E (evap cooler), F (actuators, if fitted).

> **Shore power backup:** If mains power is available at the site, connect the Victron IP65 charger to the NEMA 5-15 inlet on the container exterior. The charger maintains the battery bank automatically — leave it connected whenever shore power is available.

### 0.5 Water System

1. Fill IBC totes: Blue circuit (wash water) minimum 400 litres for one print; Grey circuit (waste) empty.
2. Open all ball valves and prime the pump by hand-filling the filter housing.
3. Switch on water pump (circuit C). Pressure should reach 2.5–3.5 bar within 30 seconds.
4. Check all pipe joints for drips. Tighten any fittings that are weeping.
5. Run water through the spray bar for 60 seconds. Check spray pattern is even across the full image plane width.
6. Switch pump OFF.

### 0.6 Ventilation and Cooling

1. Switch ON intake fan (circuit A) and exhaust fan (circuit B). Confirm airflow — hold a piece of tissue at each duct stub; it should deflect visibly.
2. **Cooling (hot climate):** Switch ON evaporative cooler (circuit E). Fill cooler reservoir. Run cooler for a minimum of **30 minutes before any operator entry** when ambient temperature exceeds 30°C. Interior should reach below 35°C before loading.
3. If using shade canopy: erect before solar noon. An 80% shade cloth over the container reduces interior temperature by 15–20°C.

> **Heat safety:** Do not enter the container if the interior temperature exceeds 40°C. A digital thermometer hung inside (read through a small gap before entry) is standard practice. In Palm Springs summer without shade, the steel container body can reach 75°C — **shade and pre-cooling are not optional in these conditions.**

### 0.7 Light-Leak Inspection

1. Close all doors including the vestibule outer door.
2. Switch ON interior safelight (circuit D, red LED only). Enter through the vestibule.
3. Switch OFF safelight. Stand still for **15 minutes** minimum — full dark adaptation.
4. Inspect all seams, door perimeters, and duct penetrations. Even a pinprick leak will be visible.
5. Exit. Seal any leaks found with black silicone sealant or gaffer tape. Repeat inspection.

**GO/NO-GO checkpoint:** All leaks sealed. Interior temperature below 35°C. Battery bank above 12.4V. Water system pressure confirmed.

---

## Phase 1 — Chemistry Preparation

**Time: ~30 minutes. Do this outside or in a well-ventilated area.**

### 1.1 Equipment

- [ ] UV-blocking safety glasses (wear throughout)
- [ ] Nitrile gloves (change between Part A and Part B mixing)
- [ ] 18" foam roller + roller tray (two sets — one per coat pass)
- [ ] 2 × 2-litre mixing jugs (graduated)
- [ ] Funnel and stirring rod
- [ ] Digital scale (1g resolution)

### 1.2 Mixing Part A — Ammonium Iron(III) Oxalate (Mike Ware formula)

Prepare a concentrated solution using **warm water (50–60°C)**. AmFe does not dissolve at room temperature.

| Print count | AmFe (dry) | Water (warm) |
|-------------|-----------|-------|
| 1 print | 200 g | 300 ml |
| 5 prints | 1,000 g | 1,500 ml |

1. Heat water to 50–60°C (a kettle left to stand for 2 minutes after boiling is ideal).
2. Weigh AmFe into the mixing jug.
3. Pour warm water over the AmFe. Stir continuously until fully dissolved — the solution turns pale yellow-green and is clear, not cloudy. This may take 3–5 minutes.
4. Allow to cool to room temperature before use.
5. Label the jug **PART A — AmFe (WARE)**. Store in a sealed dark bottle in shade.

### 1.3 Mixing Part B — Potassium Ferricyanide + Ammonium Dichromate

Prepare an 8% solution by weight. Add a small amount of ammonium dichromate for contrast enhancement.

| Print count | Potassium ferricyanide | Ammonium dichromate | Water |
|-------------|----------------------|---------------------|-------|
| 1 print | 100 g | 10 g | 1,150 ml |
| 5 prints | 500 g | 50 g | 5,750 ml |

1. Weigh potassium ferricyanide and ammonium dichromate into the second jug.
2. Add water (room temperature). Stir until fully dissolved — the solution turns bright orange-red.
3. Label the jug **PART B — KFe + AmDichr**. Store in shade, away from Part A.

> **⚠ Ammonium dichromate** is a Category 1A carcinogen. Wear nitrile gloves when handling dry powder. Do not inhale dust. The small quantity used here (~10g per print) is well within safe handling range for a ventilated workspace.

> **Storage:** Part A and Part B stock solutions keep for 6–8 weeks in sealed dark bottles. Mixed together (the working sensitiser), shelf life is 4–6 hours. Mix only what you need per session.

### 1.4 Prepare Working Sensitiser

**Mix Parts A and B in equal volumes immediately before use:**

| For 1 print (140 sq ft) | Volume |
|------------------------|--------|
| Part A | 600 ml |
| Part B | 600 ml |
| **Working sensitiser** | **1,200 ml** |

1. Pour equal volumes into a third jug. Stir gently. The mix turns yellow-green.
2. Pour into the roller tray immediately before entering for coating.

> **UV sensitivity:** The mixed sensitiser is UV-sensitive but is safe under red LED safelight. Do not expose to daylight, blue sky light, or white LED light once mixed. Work quickly once inside.

### 1.5 Humidity Check

Cyanotype coating is sensitive to humidity. Check with a digital hygrometer:

| Humidity | Action |
|----------|--------|
| Below 30% (typical Palm Springs) | Mist the muslin lightly with plain water 5 min before coating |
| 30–65% | Coat normally |
| Above 70% | Delay — coating may not dry under safelight, increasing fogging risk |

**GO/NO-GO checkpoint:** Both solutions prepared and labelled. Working sensitiser mixed. Humidity within range. Roller tray loaded and ready to carry in.

---

## Phase 2 — Loading the Image Plane

**Time: ~45 minutes. Entire phase performed in near-darkness under red LED safelight.**

### 2.1 Entering via the Light Trap

**Light-trap entry procedure (memorise this — you will do it in dim conditions):**

1. Carry all equipment into the vestibule. Close the outer door. Latch it.
2. Wait 10 seconds in the vestibule darkness.
3. Open the container cargo doors fully. Secure them to the door-stop hooks.
4. Enter the container. Close the cargo doors behind you.
5. Switch ON the safelight (circuit D switch, located on the electrical panel adjacent to the door).

> **Rule:** Never have both the outer vestibule door and the container cargo doors open simultaneously. One must always be closed.

### 2.2 Mounting the Muslin

1. Retrieve the pre-cut muslin from its light-safe bag (unbleached cotton muslin, 5,900 × 2,400mm with 100mm hem allowance).
2. Start at the **bottom edge** of the image plane frame. Clip every 150mm using the spring clips along the bottom channel.
3. Work upward — stretch the fabric taut (approximately 5N tension — enough to remove all wrinkles) and clip the top edge.
4. Clip the left and right edges, pulling outward from centre.
5. Final check: no wrinkles or sags when viewed with the safelight from 2 metres. Any slack will print as a soft zone.

### 2.3 Applying the Sensitiser

Work efficiently — aim to complete coating within 20 minutes of opening the tray.

1. Load the foam roller with sensitiser. Roll out any excess onto scrap card — the roller should be evenly loaded, not dripping.
2. **First pass:** roll horizontally from left to right across the full width of the muslin. Even strokes, 50% overlap. Work top to bottom.
3. **Second pass:** roll vertically, top to bottom. Cross-direction ensures even coverage.
4. Check edges — roller tends to undercoat at the far edges. Finish with a hand-held foam brush on the last 50mm of each edge.
5. Set the empty tray and roller aside. **Do not leave the roller sitting in residual sensitiser — it will skin over.**

### 2.4 Tack-Drying

1. Run the ventilation fans (circuits A and B) on **low speed** — just enough airflow to assist drying. Avoid directed airflow directly at the coated surface.
2. Wait **15–20 minutes** under safelight. The sensitiser changes from wet-glossy to a matte tack-dry state.
3. Confirm by lightly touching the corner of the coated area with a gloved fingertip. It should not transfer to the glove.

> **Do not proceed with a wet coat.** A wet coat will run during exposure and will not produce a sharp image.

### 2.5 Exiting via the Light Trap

**Reverse the entry sequence:**

1. Switch OFF safelight.
2. Open container cargo doors.
3. Exit into vestibule. Close cargo doors behind you.
4. Open the outer vestibule door. Exit.

**GO/NO-GO checkpoint:** Muslin fully clipped and taut. Sensitiser dry to touch. Container cargo doors latched. Outer vestibule door closed.

---

## Phase 3 — Exposure

**Time: ~30–45 minutes baseline + adjustment (Ware formula). Shutter operated entirely from outside.**

### 3.1 Exposure Calculation

Baseline exposure: **30–45 minutes** in direct unobstructed sun, mid-morning to mid-afternoon, summer (Mike Ware New Cyanotype formula on cotton muslin). This is 4–8× faster than the traditional Herschel formula (~2–3 hours baseline) due to the higher UV sensitivity of ammonium iron(III) oxalate.

**Exposure Adjustment Table**

| Condition | Multiply baseline by |
|-----------|---------------------|
| Full direct sun | × 1.0 |
| Thin haze / milky sky | × 1.5 |
| Broken cloud (50% coverage) | × 2.0 |
| Heavy overcast | × 4.0 |
| Early morning / late afternoon (2h before/after sunset) | × 2.0 |
| Winter sun at mid-latitude | × 1.5 |

*For compound conditions (e.g. thin haze + early morning), multiply the factors: 1.5 × 2.0 = × 3.0.*

These factors are EV-based estimates for light level changes. Cyanotype is an iron-based process and does not exhibit Schwarzschild reciprocity failure — no additional reciprocity correction is required beyond the factors above. For critical work, run a test strip first: cut a 200mm × full-height strip of coated muslin, expose in **5-minute intervals** using a card mask, develop immediately, and compare zones.

### 3.2 Opening the Shutter

1. Confirm the vestibule outer door is closed and latched.
2. Set a timer for your calculated exposure time.
3. Open the pinhole shutter from the exterior operating handle.
4. **Do not open any doors, stand in front of the pinhole wall, or allow shadows to cross the pinhole during exposure.**

### 3.3 Monitoring During Exposure

- Check the battery bank voltage on the MPPT controller display every 15 minutes. If voltage drops below 11.8V, switch off the evaporative cooler (non-essential during exposure).
- Light conditions: note any significant cloud cover changes. If conditions change substantially mid-exposure (e.g. sky goes from clear to heavy overcast), close the shutter, note elapsed time, wait for conditions to return, then re-open for the remaining time.

### 3.4 Closing the Shutter

1. At the calculated time, close the pinhole shutter using the exterior operating handle.
2. Verify the shutter indicator reads CLOSED before entering.

**GO/NO-GO checkpoint:** Shutter confirmed closed. Elapsed time within ± 2 min of target.

---

## Phase 4 — Development

**Time: ~20 minutes.**

### 4.1 Entering and Removing the Muslin

1. Enter via light trap (same procedure as Phase 2.1). Safelight ON.
2. Unclip the muslin from the image plane — work top-down, supporting the fabric weight as the upper clips release. The image is latent at this point and may be barely visible as a pale yellow ghost.
3. Carry the muslin to the development area (can be outside — cyanotype develops in daylight).
4. Exit via light trap.

### 4.2 Development in Water

Cyanotype develops by oxidation — the iron salts convert to Prussian blue on contact with water and air. The full blue colour deepens over the first few minutes of drying.

**Wash sequence using the Blue circuit:**

1. Switch ON water pump (circuit C).
2. Open the Blue circuit supply valve. Allow water to flow over the full surface of the muslin for **5 minutes**. The wash water will run yellow-green as unreacted sensitiser clears. This is normal and non-toxic.
3. Close the Blue circuit valve. Open the Grey circuit return valve and allow the wash water to drain to the grey recovery tank.
4. Repeat for a total of **3 wash cycles** (15 minutes total).
5. Final rinse: open the Blue circuit for a 2-minute final flush. Drain.

> **Visual check after the second wash:** The image should be clearly visible — Prussian blue shadows against a white or off-white highlight. If the image appears flat or very faint, the print was underexposed. Allow it to complete washing and dry — images that appear pale when wet frequently darken significantly on drying. If still flat after drying, re-expose for 1.5× the original time.

### 4.3 Drying

1. Hang the developed muslin to dry — horizontal is ideal (prevents drip marks). Wooden poles or a rope line between two vehicles work well.
2. Drying time: 20–60 minutes depending on temperature and airflow. The blue intensifies as the image oxidises in air.
3. Final colour appears approximately 30 minutes after the print appears dry to the touch.

---

## Phase 5 — Cleanup and Close-Down

**Time: ~30 minutes.**

### 5.1 Chemistry Disposal

- Spent wash water (yellow-green): cyanotype wash water at this dilution is non-hazardous and can be disposed of via the grey water recovery tank, or diluted and poured on ground away from water sources. Do not dispose into storm drains without verification of local regulations.
- Unused sensitiser: seal and store in a dark bottle (4-week shelf life for separated A and B solutions). Mixed working sensitiser: discard — working life is 6 hours.
- Rinse all trays, rollers, and brushes in plain water immediately. Dried sensitiser is harder to remove.

### 5.2 Container Ventilation

1. Open both ventilation fans to full speed (circuits A and B).
2. Leave ventilating for **30 minutes minimum** after development is complete, especially if working in hot conditions — the container interior will have accumulated heat and humidity from the wash operation.

### 5.3 Power-Down Sequence

Power down in this order to avoid voltage spikes on sensitive electronics:

1. Evaporative cooler (circuit E)
2. Water pump (circuit C)
3. Ventilation fans (circuits A, B)
4. Safelight (circuit D)
5. Film plane actuators if used (circuit F)
6. Disconnect solar panel inputs at the MPPT controller

If shore charger is connected, leave it running overnight to top up the battery bank.

### 5.4 Securing the Container

1. Close and latch all vestibule curtains.
2. Close and latch the cargo doors. Apply secondary locking bar if the container will be unattended overnight.
3. Cap all ventilation duct stubs on the exterior.
4. Secure solar panels — if conditions allow, lay flat or fold to minimise wind load.

---

## Exposure Adjustment Table

*Full reference table for use in Phase 3.*

| Baseline | 120 min | Direct full sun, summer, 10:00–14:00 |
|----------|---------|-------------------------------------|
| Thin haze | 180 min | |
| Broken cloud | 240 min | |
| Heavy overcast | 480 min | |
| Early/late sun | 240 min | |
| Winter mid-latitude | 180 min | |
| Thin haze + early sun | 360 min | Multiply factors: 1.5 × 2.0 |

---

## Troubleshooting

| Symptom | Likely cause | Action |
|---------|-------------|--------|
| Image very faint after full drying | Underexposure | Re-coat (re-expose existing print is not possible after development) — increase time by 50% |
| Image too dark / no highlight detail | Overexposure | Reduce time by 30% on next print |
| Streaks or tide-marks | Uneven coating or drips during development | Improve roller technique; ensure even wash flow |
| Soft or blurred image | Muslin slack at coating or during exposure | Increase clip tension; check frame is not vibrating in wind |
| Blue haze (fogging) in shadows | Light leak or sensitiser exposed to UV before loading | Re-inspect light trap; check sensitiser storage |
| Uneven colour — cool/warm zones | Humidity variation across coating | Ensure even pre-misting if in dry climate |
| Battery low warning during session | Higher-than-expected draw or low state of charge | Switch off evaporative cooler; complete session on fans and pump only |

---

## See Also

- [Electrical & Systems Report](electrical-report.md) — power system, light trap construction, cooling specification
- [Film Plane Mechanism](film-plane-mechanism-report.md) — image plane adjustment and setup
- [Tilt-Swing Front Board](tilt-swing-board-report.md) — pinhole steering and angular calibration
- [Chem Shopping List](chemistry-shopping-list.md) — chemistry suppliers and quantities
- [Processing System](water-system-report.md) — water system circuit operation
