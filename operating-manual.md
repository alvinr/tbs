<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
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
| 3 | Exposure | ~30–45 min (baseline) |
| 4 | Development | ~20 min |
| 5 | Cleanup and close-down | ~30 min |
| **Total** | **First print, ideal conditions** | **~4–4.5 hours** |

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

1. Direct the delivery driver to position the container with the **cargo doors at 90 degress from the subject**. The pinhole wall faces the subject.
2. Once set down, check level. Use 50mm timber sleepers under corner castings to correct — up to 50mm height difference is manageable without shimming the mechanism.
3. Open cargo doors and inspect interior:
   - No water ingress or condensation on image plane
   - All seals (door perimeter, neoprene cord) are intact
   - Film plane mechanism moves freely on all four corners

### 0.3 Light Trap — Revolving Drum Panel

1. Confirm the hinged drum panel is closed and all four Southco cam latches are engaged (quarter-turn, flush with panel face).
2. Check the EPDM perimeter gasket is seated with no gaps or folded sections.
3. Rotate the drum one full revolution by hand — it should turn freely with no binding or scraping.
4. Verify: step into the drum entry side and rotate through to the interior. Wait 2 minutes for dark adaptation. **No light should be visible at any baffle position.** Mark any leaks with chalk and seal with black silicone before proceeding.

> **Safety:** Do not attempt to reverse direction inside the drum — the baffles only clear forward rotation. If unsure of orientation, continue rotating forward until you exit on the intended side.

### 0.4 Solar Power System

1. Deploy solar panels on south-facing ground or roof rack, angled at 30° from horizontal (optimal for Palm Springs latitude).
2. Connect panels in parallel to the Victron SmartSolar MPPT 100/50 controller.
3. Connect controller to battery bank (2 × 100Ah LiFePO4 in parallel). **Observe polarity.**
4. Connect Blue Sea fuse block to battery positive busbar.
5. Check controller display: battery voltage should read 12.6–13.2V (full charge). If below 12.0V, charge before proceeding — a depleted battery bank cannot power the cooler and water system simultaneously.
6. Verify each circuit fuse is seated: A (intake fan), B (exhaust fan), C (water pump), D (safelight), E (evap cooler), F (actuators, if fitted).

> **Shore power backup:** If mains power is available at the site, connect the Victron IP65 charger to the NEMA 5-15 inlet on the container exterior. The charger maintains the battery bank automatically — leave it connected whenever shore power is available.

### 0.5 Water System

1. Fill IBC totes: Blue circuit (wash water) minimum 400 liters for one print; Grey circuit (waste) empty.
2. Open all ball valves and prime the pump by hand-filling the filter housing.
3. Switch on water pump (circuit C). Pressure should reach 2.5–3.5 bar within 30 seconds.
4. Check all pipe joints for drips. Tighten any fittings that are weeping.
5. Run water through the spray bar for 60 seconds. Check spray pattern is even across the full image plane width.
6. Switch pump OFF.
7. Confirm processing tray is installed between the film plane rails and drain hose is connected to 3W-DV-02.
8. Lay fresh 6-mil black LDPE containment liner over the tray surface, overlapping 50mm over the rims.

### 0.6 Ventilation and Cooling

1. Switch ON intake fan (circuit A) and exhaust fan (circuit B). Confirm airflow — hold a piece of tissue at each duct stub; it should deflect visibly.
2. **Cooling (hot climate):** Switch ON evaporative cooler (circuit E). Fill cooler reservoir. Run cooler for a minimum of **30 minutes before any operator entry** when ambient temperature exceeds 30°C. Interior should reach below 35°C before loading.
3. If using shade canopy: erect before solar noon. An 80% shade cloth over the container reduces interior temperature by 15–20°C.

> **Heat safety:** Do not enter the container if the interior temperature exceeds 40°C. A digital thermometer hung inside (read through a small gap before entry) is standard practice. In Palm Springs summer without shade, the steel container body can reach 75°C — **shade and pre-cooling are not optional in these conditions.**

### 0.7 Light-Leak Inspection

1. Latch the drum panel (all four Southco cam latches engaged).
2. Switch ON interior safelight (circuit D, red LED only). Enter through the revolving drum.
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
- [ ] 2 × 2-liter mixing jugs (graduated)
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

> **Storage:** Part A and Part B stock solutions keep for 6–8 weeks in sealed dark bottles. Mixed together (the working sensitizer), shelf life is 4–6 hours. Mix only what you need per session.

### 1.4 Prepare Working Sensitiser

**Mix Parts A and B in equal volumes immediately before use:**

| For 1 print (~103 sq ft) | Volume |
|------------------------|--------|
| Part A | 600 ml |
| Part B | 600 ml |
| **Working sensitizer** | **1,200 ml** |

1. Pour equal volumes into a third jug. Stir gently. The mix turns yellow-green.
2. Pour into the roller tray immediately before entering for coating.

> **UV sensitivity:** The mixed sensitizer is UV-sensitive but is safe under red LED safelight. Do not expose to daylight, blue sky light, or white LED light once mixed. Work quickly once inside.

### 1.5 Humidity Check

Cyanotype coating is sensitive to humidity. Check with a digital hygrometer:

| Humidity | Action |
|----------|--------|
| Below 30% (typical Palm Springs) | Mist the muslin lightly with plain water 5 min before coating |
| 30–65% | Coat normally |
| Above 70% | Delay — coating may not dry under safelight, increasing fogging risk |

**GO/NO-GO checkpoint:** Both solutions prepared and labelled. Working sensitizer mixed. Humidity within range. Roller tray loaded and ready to carry in.

---

## Phase 2 — Loading the Image Plane

**Time: ~45 minutes. Entire phase performed in near-darkness under red LED safelight.**

### 2.1 Entering via the Light Trap

**Revolving drum entry procedure (memorize this — you will do it in dim conditions):**

1. Confirm drum panel is latched (all four Southco cam latches engaged).
2. Carry all equipment to the drum entry side. Set it down at your feet.
3. Push the drum wall forward until the first baffle clears. Step in.
4. Continue rotating forward until you exit into the container interior.
5. Pass equipment through the drum in the same direction — one item at a time.
6. Switch ON the safelight (circuit D switch, located on the electrical panel).

> **Rule:** The drum seals automatically as it rotates — no doors to leave open. However, do not wedge equipment in the drum aperture. If a load is too large for the drum, it must be loaded during a full dark period (after sunset) with the panel unlatched and swung open.

### 2.2 Mounting the Muslin

1. Retrieve the pre-cut muslin from its light-safe bag (unbleached cotton muslin, 5,900 × 2,400mm with 100mm hem allowance).
2. Start at the **bottom edge** of the image plane frame. Clip every 150mm using the spring clips along the bottom channel.
3. Work upward — stretch the fabric taut (approximately 5N tension — enough to remove all wrinkles) and clip the top edge.
4. Clip the left and right edges, pulling outward from centre.
5. Final check: no wrinkles or sags when viewed with the safelight from 2 meters. Any slack will print as a soft zone.

### 2.3 Applying the Sensitiser

Work efficiently — aim to complete coating within 20 minutes of opening the tray.

1. Load the foam roller with sensitizer. Roll out any excess onto scrap card — the roller should be evenly loaded, not dripping.
2. **First pass:** roll horizontally from left to right across the full width of the muslin. Even strokes, 50% overlap. Work top to bottom.
3. **Second pass:** roll vertically, top to bottom. Cross-direction ensures even coverage.
4. Check edges — roller tends to undercoat at the far edges. Finish with a hand-held foam brush on the last 50mm of each edge.
5. Set the empty tray and roller aside. **Do not leave the roller sitting in residual sensitizer — it will skin over.**

### 2.4 Tack-Drying

1. Run the ventilation fans (circuits A and B) on **low speed** — just enough airflow to assist drying. Avoid directed airflow directly at the coated surface.
2. Wait **15–20 minutes** under safelight. The sensitizer changes from wet-glossy to a matte tack-dry state.
3. Confirm by lightly touching the corner of the coated area with a gloved fingertip. It should not transfer to the glove.

> **Do not proceed with a wet coat.** A wet coat will run during exposure and will not produce a sharp image.

### 2.5 Exiting via the Light Trap

**Revolving drum exit procedure:**

1. Switch OFF safelight.
2. Step into the drum from the interior side. Rotate forward (same direction as entry) until you exit to the exterior.
3. The drum seals behind you as it rotates.

**GO/NO-GO checkpoint:** Muslin fully clipped and taut. Sensitizer dry to touch. Drum panel latched.

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
3. Lay the muslin face-up on the LDPE containment sheet on the processing zone floor (optical zone, between the film plane rails).

### 4.2 Development in Water

Cyanotype develops by oxidation — the iron salts convert to Prussian blue on contact with water and air. The full blue color deepens over the first few minutes of drying.

**Wash sequence using the Blue circuit:**

1. Switch ON water pump (circuit C).
2. Open the Blue circuit supply valve. Allow water to flow over the full surface of the muslin for **5 minutes**. The wash water will run yellow-green as unreacted sensitizer clears. This is normal and non-toxic.
3. Close the Blue circuit valve. Open the Grey circuit return valve and allow the wash water to drain to the grey recovery tank.
4. Repeat for a total of **3 wash cycles** (15 minutes total).
5. Final rinse: open the Blue circuit for a 2-minute final flush. Drain.

> **Visual check after the second wash:** The image should be clearly visible — Prussian blue shadows against a white or off-white highlight. If the image appears flat or very faint, the print was underexposed. Allow it to complete washing and dry — images that appear pale when wet frequently darken significantly on drying. If still flat after drying, re-expose for 1.5× the original time.

### 4.3 Drying

1. After the final wash, carry the muslin outside through the light trap. Cyanotype is no longer light-sensitive after washing — daylight exposure is safe and accelerates oxidation.
2. Hang the developed muslin to dry — horizontal is ideal (prevents drip marks). Wooden poles or a rope line between two vehicles work well.
3. Drying time: 20–60 minutes depending on temperature and airflow. The blue intensifies as the image oxidizes in air.
4. Final color appears approximately 30 minutes after the print appears dry to the touch.

---

## Phase 5 — Cleanup and Close-Down

**Time: ~30 minutes.**

### 5.1 Chemistry Disposal

- Spent wash water (yellow-green): cyanotype wash water at this dilution is non-hazardous and can be disposed of via the grey water recovery tank, or diluted and poured on ground away from water sources. Do not dispose into storm drains without verification of local regulations.
- Unused sensitizer: seal and store in a dark bottle (4-week shelf life for separated A and B solutions). Mixed working sensitizer: discard — working life is 6 hours.
- Rinse all trays, rollers, and brushes in plain water immediately. Dried sensitizer is harder to remove.

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

### 5.4 Securing the Container (Operational Mode)

1. Engage all four Southco cam latches on the drum panel.
2. Apply secondary locking bar across the drum panel face if the container will be unattended overnight.
3. Cap all ventilation duct stubs on the exterior.
4. Secure solar panels — if conditions allow, lay flat or fold to minimize wind load.

### 5.5 Transport Mode Conversion (Packing Up)

**Time: ~15–20 minutes. Single-person operation.**

The stepped hinged panel rides on a sliding carriage (HGR20 linear rails, 300mm travel). The waste drums sit on V-groove roller dollies (305mm travel). Both must slide inward before the container doors can close.

The dolly tracks are split into two sections: permanent tracks (X=40–620mm, within the left end zone) and removable bridge sections (355mm long) that span over the film plane floor rail at X=625mm. The bridges are installed only during mode conversion — they must be removed before operating the film plane.

1. Stow all interior items. Retract film plane carriage to Yd=100mm. **Confirm carriage is parked** — the bridge sections cannot be installed with the carriage in the drum track zone.
2. Install 4 bridge track sections (2 per drum): drop each bridge onto the permanent track end, engage the 2 locating dowel pins per bridge. Confirm bridges are seated and level.
3. Release all 4 Southco cam latches. Swing the panel open 180° outward.
4. Unlash waste drums (remove 2 ratchet straps per drum).
5. Slide each drum inward: release spring plunger pin → push dolly 305mm (~11N force) → pin engages transport hole. Drums cross the film plane rail on the bridge sections.
6. Remove 4 bridge track sections. Stow inside container (e.g. behind IBC column).
7. Swing panel closed (do not latch).
8. Release 2 Destaco toggle clamps at operational position.
9. Push panel inward 300mm on HGR20 rails. Carriage contacts transport end stops.
10. Engage 2 Destaco toggle clamps at transport position.
11. Close and latch standard ISO container cargo doors.
12. Relash drums for transport (ratchet straps to dolly D-rings).

### 5.6 Operational Mode Conversion (Setting Up)

**Time: ~15–20 minutes. Single-person operation. Reverse of 5.5.**

1. Open container cargo doors fully.
2. Release 2 Destaco toggle clamps at transport position.
3. Pull panel outward 300mm. Engage 2 Destaco toggle clamps at operational position.
4. Swing panel open 180°.
5. Install 4 bridge track sections (2 per drum): engage locating dowel pins.
6. Unlash waste drums. Slide each drum outward: release pin → push dolly 305mm → pin engages operational hole.
7. Remove 4 bridge track sections. Stow inside container.
8. Lash drums in operational position (ratchet straps to dolly D-rings).
9. Swing panel closed. Engage all 4 Southco cam latches.
10. Perform dark-adaptation check (Phase 0.3 step 4).

---

## Exposure Adjustment Table

*Full reference table for use in Phase 3.*

| Baseline | 35 min | Direct full sun, summer, 10:00–14:00 (Ware formula) |
|----------|--------|-----------------------------------------------------|
| Thin haze | 55 min | |
| Broken cloud | 70 min | |
| Heavy overcast | 140 min | |
| Early/late sun | 70 min | |
| Winter mid-latitude | 55 min | |
| Thin haze + early sun | 105 min | Multiply factors: 1.5 × 2.0 |

---

## Troubleshooting

| Symptom | Likely cause | Action |
|---------|-------------|--------|
| Image very faint after full drying | Underexposure | Re-coat (re-expose existing print is not possible after development) — increase time by 50% |
| Image too dark / no highlight detail | Overexposure | Reduce time by 30% on next print |
| Streaks or tide-marks | Uneven coating or drips during development | Improve roller technique; ensure even wash flow |
| Soft or blurred image | Muslin slack at coating or during exposure | Increase clip tension; check frame is not vibrating in wind |
| Blue haze (fogging) in shadows | Light leak or sensitizer exposed to UV before loading | Re-inspect light trap; check sensitizer storage |
| Uneven color — cool/warm zones | Humidity variation across coating | Ensure even pre-misting if in dry climate |
| Battery low warning during session | Higher-than-expected draw or low state of charge | Switch off evaporative cooler; complete session on fans and pump only |

---

## See Also

- [Electrical & Systems Report](electrical-report.md) — power system, light trap construction, cooling specification
- [Film Plane Mechanism](film-plane-mechanism-report.md) — image plane adjustment and setup
- [Tilt-Swing Front Board](tilt-swing-board-report.md) — pinhole steering and angular calibration
- [Chem Shopping List](chemistry-shopping-list.md) — chemistry suppliers and quantities
- [Processing System](water-system-report.md) — water system circuit operation
