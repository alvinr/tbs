# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/generate_corner_gimbal_model.py — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("Film-Plane Corner Mechanism", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

to_erase = entities.to_a.select { |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

  model.layers.add("Corners") unless model.layers["Corners"]
  model.layers.add("Film Plane") unless model.layers["Film Plane"]
  model.layers.add("Pinhole") unless model.layers["Pinhole"]
  model.layers.add("Context") unless model.layers["Context"]
  model.layers.add("Labels") unless model.layers["Labels"]

  # ═══ Corners ═══
  defn = model.definitions.add("Corners")
  ents = defn.entities
  # U-rail STUB (fixed, parks corner) web BL
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) web BL"
  face = grp.entities.add_face([131.mm,2090.mm,232.mm], [136.mm,2090.mm,232.mm], [136.mm,2362.mm,232.mm], [131.mm,2362.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) flange BL 303
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) flange BL 303"
  face = grp.entities.add_face([131.mm,2090.mm,303.mm], [169.mm,2090.mm,303.mm], [169.mm,2362.mm,303.mm], [131.mm,2362.mm,303.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) flange BL 232
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) flange BL 232"
  face = grp.entities.add_face([131.mm,2090.mm,232.mm], [169.mm,2090.mm,232.mm], [169.mm,2362.mm,232.mm], [131.mm,2362.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) bottom-flange lip BL
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) bottom-flange lip BL"
  face = grp.entities.add_face([164.mm,2090.mm,237.mm], [169.mm,2090.mm,237.mm], [169.mm,2362.mm,237.mm], [164.mm,2362.mm,237.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail REMOVABLE (out for transport) web BL
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) web BL"
  face = grp.entities.add_face([131.mm,0.mm,232.mm], [136.mm,0.mm,232.mm], [136.mm,2090.mm,232.mm], [131.mm,2090.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) flange BL 303
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) flange BL 303"
  face = grp.entities.add_face([131.mm,0.mm,303.mm], [169.mm,0.mm,303.mm], [169.mm,2090.mm,303.mm], [131.mm,2090.mm,303.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) flange BL 232
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) flange BL 232"
  face = grp.entities.add_face([131.mm,0.mm,232.mm], [169.mm,0.mm,232.mm], [169.mm,2090.mm,232.mm], [131.mm,2090.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) bottom-flange lip BL
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) bottom-flange lip BL"
  face = grp.entities.add_face([164.mm,0.mm,237.mm], [169.mm,0.mm,237.mm], [169.mm,2090.mm,237.mm], [164.mm,2090.mm,237.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.3
  grp.material = mat

  # Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL
  grp = ents.add_group
  grp.name = "Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"
  face = grp.entities.add_face([119.mm,2030.mm,232.mm], [131.mm,2030.mm,232.mm], [131.mm,2180.mm,232.mm], [119.mm,2180.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Retaining screw (bridge→STUB) BL
  grp = ents.add_group
  grp.name = "Retaining screw (bridge→STUB) BL"
  ge = grp.entities
  circle = ge.add_circle([109.mm,2135.mm,270.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(26.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail far flange (pivot post) BL
  grp = ents.add_group
  grp.name = "Rail far flange (pivot post) BL"
  face = grp.entities.add_face([95.mm,2350.mm,227.mm], [205.mm,2350.mm,227.mm], [205.mm,2362.mm,227.mm], [95.mm,2362.mm,227.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(86.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Pinhole-wall gusset/seat BL
  grp = ents.add_group
  grp.name = "Pinhole-wall gusset/seat BL"
  face = grp.entities.add_face([94.mm,0.mm,202.mm], [206.mm,0.mm,202.mm], [206.mm,45.mm,202.mm], [94.mm,45.mm,202.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(131.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Length splice (pinhole end, outboard web) BL
  grp = ents.add_group
  grp.name = "Length splice (pinhole end, outboard web) BL"
  face = grp.entities.add_face([119.mm,205.mm,232.mm], [131.mm,205.mm,232.mm], [131.mm,315.mm,232.mm], [119.mm,315.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal wheel Ø32 (weight) BL 2232
  grp = ents.add_group
  grp.name = "Acetal wheel Ø32 (weight) BL 2232"
  ge = grp.entities
  circle = ge.add_circle([142.mm,2232.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 BL 2232
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 BL 2232"
  ge = grp.entities
  circle = ge.add_circle([142.mm,2232.mm,253.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(47.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift) BL 2232
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift) BL 2232"
  ge = grp.entities
  circle = ge.add_circle([144.mm,2232.mm,293.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 BL 2232
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 BL 2232"
  ge = grp.entities
  circle = ge.add_circle([144.mm,2232.mm,293.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal wheel Ø32 (weight) BL 2276
  grp = ents.add_group
  grp.name = "Acetal wheel Ø32 (weight) BL 2276"
  ge = grp.entities
  circle = ge.add_circle([142.mm,2276.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 BL 2276
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 BL 2276"
  ge = grp.entities
  circle = ge.add_circle([142.mm,2276.mm,253.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(47.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift) BL 2276
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift) BL 2276"
  ge = grp.entities
  circle = ge.add_circle([144.mm,2276.mm,293.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 BL 2276
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 BL 2276"
  ge = grp.entities
  circle = ge.add_circle([144.mm,2276.mm,293.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (bolted to skate axles) BL
  grp = ents.add_group
  grp.name = "Carriage plate (bolted to skate axles) BL"
  face = grp.entities.add_face([177.mm,2222.mm,154.mm], [191.mm,2222.mm,154.mm], [191.mm,2302.mm,154.mm], [177.mm,2302.mm,154.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(157.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) BL 2232
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) BL 2232"
  ge = grp.entities
  circle = ge.add_circle([183.mm,2232.mm,231.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) BL 2276
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) BL 2276"
  ge = grp.entities
  circle = ge.add_circle([183.mm,2276.mm,231.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT, green) BL
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT, green) BL"
  face = grp.entities.add_face([180.mm,2253.mm,156.mm], [196.mm,2253.mm,156.mm], [196.mm,2271.mm,156.mm], [180.mm,2271.mm,156.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(113.mm)
  mat = model.materials["Vertical Z slide rail (TILT, green) BL"] || model.materials.add("Vertical Z slide rail (TILT, green) BL")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING, purple) BL
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING, purple) BL"
  face = grp.entities.add_face([150.mm,2255.mm,156.mm], [410.mm,2255.mm,156.mm], [410.mm,2269.mm,156.mm], [150.mm,2269.mm,156.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X slide rail (SWING, purple) BL"] || model.materials.add("Horizontal X slide rail (SWING, purple) BL")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint BL
  grp = ents.add_group
  grp.name = "U-joint BL"
  face = grp.entities.add_face([138.mm,2250.mm,146.mm], [162.mm,2250.mm,146.mm], [162.mm,2274.mm,146.mm], [138.mm,2274.mm,146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Frame corner bracket (angle frame → U-joint) BL
  grp = ents.add_group
  grp.name = "Frame corner bracket (angle frame → U-joint) BL"
  face = grp.entities.add_face([136.mm,2254.mm,134.mm], [184.mm,2254.mm,134.mm], [184.mm,2270.mm,134.mm], [136.mm,2270.mm,134.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(52.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (angle frame → bracket) BL
  grp = ents.add_group
  grp.name = "Frame-corner bolt (angle frame → bracket) BL"
  ge = grp.entities
  circle = ge.add_circle([183.mm,2256.mm,160.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) web BR
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) web BR"
  face = grp.entities.add_face([4638.mm,0.mm,232.mm], [4643.mm,0.mm,232.mm], [4643.mm,2362.mm,232.mm], [4638.mm,2362.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) flange BR 303
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) flange BR 303"
  face = grp.entities.add_face([4605.mm,0.mm,303.mm], [4643.mm,0.mm,303.mm], [4643.mm,2362.mm,303.mm], [4605.mm,2362.mm,303.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) flange BR 232
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) flange BR 232"
  face = grp.entities.add_face([4605.mm,0.mm,232.mm], [4643.mm,0.mm,232.mm], [4643.mm,2362.mm,232.mm], [4605.mm,2362.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) bottom-flange lip BR
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) bottom-flange lip BR"
  face = grp.entities.add_face([4605.mm,0.mm,237.mm], [4610.mm,0.mm,237.mm], [4610.mm,2362.mm,237.mm], [4605.mm,2362.mm,237.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail end flange (outboard-trimmed) BR 0
  grp = ents.add_group
  grp.name = "Rail end flange (outboard-trimmed) BR 0"
  face = grp.entities.add_face([4569.mm,0.mm,227.mm], [4644.mm,0.mm,227.mm], [4644.mm,12.mm,227.mm], [4569.mm,12.mm,227.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(86.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Rail end flange (outboard-trimmed) BR 2350
  grp = ents.add_group
  grp.name = "Rail end flange (outboard-trimmed) BR 2350"
  face = grp.entities.add_face([4569.mm,2350.mm,227.mm], [4644.mm,2350.mm,227.mm], [4644.mm,2362.mm,227.mm], [4569.mm,2362.mm,227.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(86.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal wheel Ø32 (weight) BR 2232
  grp = ents.add_group
  grp.name = "Acetal wheel Ø32 (weight) BR 2232"
  ge = grp.entities
  circle = ge.add_circle([4616.mm,2232.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 BR 2232
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 BR 2232"
  ge = grp.entities
  circle = ge.add_circle([4585.mm,2232.mm,253.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(47.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift) BR 2232
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift) BR 2232"
  ge = grp.entities
  circle = ge.add_circle([4618.mm,2232.mm,293.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 BR 2232
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 BR 2232"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2232.mm,293.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(37.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal wheel Ø32 (weight) BR 2276
  grp = ents.add_group
  grp.name = "Acetal wheel Ø32 (weight) BR 2276"
  ge = grp.entities
  circle = ge.add_circle([4616.mm,2276.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 BR 2276
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 BR 2276"
  ge = grp.entities
  circle = ge.add_circle([4585.mm,2276.mm,253.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(47.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift) BR 2276
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift) BR 2276"
  ge = grp.entities
  circle = ge.add_circle([4618.mm,2276.mm,293.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 BR 2276
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 BR 2276"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2276.mm,293.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(37.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (bolted to skate axles) BR
  grp = ents.add_group
  grp.name = "Carriage plate (bolted to skate axles) BR"
  face = grp.entities.add_face([4585.mm,2222.mm,154.mm], [4599.mm,2222.mm,154.mm], [4599.mm,2302.mm,154.mm], [4585.mm,2302.mm,154.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(157.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) BR 2232
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) BR 2232"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2232.mm,231.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) BR 2276
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) BR 2276"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2276.mm,231.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT, green) BR
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT, green) BR"
  face = grp.entities.add_face([4588.mm,2253.mm,156.mm], [4604.mm,2253.mm,156.mm], [4604.mm,2271.mm,156.mm], [4588.mm,2271.mm,156.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(113.mm)
  mat = model.materials["Vertical Z slide rail (TILT, green) BL"] || model.materials.add("Vertical Z slide rail (TILT, green) BL")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING, purple) BR
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING, purple) BR"
  face = grp.entities.add_face([4364.mm,2255.mm,156.mm], [4624.mm,2255.mm,156.mm], [4624.mm,2269.mm,156.mm], [4364.mm,2269.mm,156.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X slide rail (SWING, purple) BL"] || model.materials.add("Horizontal X slide rail (SWING, purple) BL")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint BR
  grp = ents.add_group
  grp.name = "U-joint BR"
  face = grp.entities.add_face([4612.mm,2250.mm,146.mm], [4636.mm,2250.mm,146.mm], [4636.mm,2274.mm,146.mm], [4612.mm,2274.mm,146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Frame corner bracket (angle frame → U-joint) BR
  grp = ents.add_group
  grp.name = "Frame corner bracket (angle frame → U-joint) BR"
  face = grp.entities.add_face([4590.mm,2254.mm,134.mm], [4638.mm,2254.mm,134.mm], [4638.mm,2270.mm,134.mm], [4590.mm,2270.mm,134.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(52.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (angle frame → bracket) BR
  grp = ents.add_group
  grp.name = "Frame-corner bolt (angle frame → bracket) BR"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2256.mm,160.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) web TL
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) web TL"
  face = grp.entities.add_face([112.mm,2090.mm,2377.mm], [188.mm,2090.mm,2377.mm], [188.mm,2362.mm,2377.mm], [112.mm,2362.mm,2377.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) flange TL 112
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) flange TL 112"
  face = grp.entities.add_face([112.mm,2090.mm,2344.mm], [117.mm,2090.mm,2344.mm], [117.mm,2362.mm,2344.mm], [112.mm,2362.mm,2344.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) flange TL 183
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) flange TL 183"
  face = grp.entities.add_face([183.mm,2090.mm,2344.mm], [188.mm,2090.mm,2344.mm], [188.mm,2362.mm,2344.mm], [183.mm,2362.mm,2344.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail REMOVABLE (out for transport) web TL
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) web TL"
  face = grp.entities.add_face([112.mm,0.mm,2377.mm], [188.mm,0.mm,2377.mm], [188.mm,2090.mm,2377.mm], [112.mm,2090.mm,2377.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) flange TL 112
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) flange TL 112"
  face = grp.entities.add_face([112.mm,0.mm,2344.mm], [117.mm,0.mm,2344.mm], [117.mm,2090.mm,2344.mm], [112.mm,2090.mm,2344.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) flange TL 183
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) flange TL 183"
  face = grp.entities.add_face([183.mm,0.mm,2344.mm], [188.mm,0.mm,2344.mm], [188.mm,2090.mm,2344.mm], [183.mm,2090.mm,2344.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.3
  grp.material = mat

  # Welded bridge (welded to REMOVABLE, bears on stub, over web) TL
  grp = ents.add_group
  grp.name = "Welded bridge (welded to REMOVABLE, bears on stub, over web) TL"
  face = grp.entities.add_face([112.mm,2030.mm,2382.mm], [188.mm,2030.mm,2382.mm], [188.mm,2180.mm,2382.mm], [112.mm,2180.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Retaining screw (bridge→STUB) TL
  grp = ents.add_group
  grp.name = "Retaining screw (bridge→STUB) TL"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2135.mm,2386.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(26.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail far flange (pivot post) TL
  grp = ents.add_group
  grp.name = "Rail far flange (pivot post) TL"
  face = grp.entities.add_face([95.mm,2350.mm,2339.mm], [205.mm,2350.mm,2339.mm], [205.mm,2362.mm,2339.mm], [95.mm,2362.mm,2339.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Pinhole-wall gusset/seat TL
  grp = ents.add_group
  grp.name = "Pinhole-wall gusset/seat TL"
  face = grp.entities.add_face([94.mm,0.mm,2314.mm], [206.mm,0.mm,2314.mm], [206.mm,45.mm,2314.mm], [94.mm,45.mm,2314.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(93.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Length splice (pinhole end, over web) TL
  grp = ents.add_group
  grp.name = "Length splice (pinhole end, over web) TL"
  face = grp.entities.add_face([112.mm,205.mm,2382.mm], [188.mm,205.mm,2382.mm], [188.mm,315.mm,2382.mm], [112.mm,315.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal guide wheel Ø32 (10mm narrower than the yoke; ~5mm clearance each side) TL 2232
  grp = ents.add_group
  grp.name = "Acetal guide wheel Ø32 (10mm narrower than the yoke; ~5mm clearance each side) TL 2232"
  ge = grp.entities
  circle = ge.add_circle([124.mm,2232.mm,2361.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(52.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Guide axle Ø10 (in throat) TL 2232
  grp = ents.add_group
  grp.name = "Guide axle Ø10 (in throat) TL 2232"
  ge = grp.entities
  circle = ge.add_circle([117.mm,2232.mm,2361.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(66.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal guide wheel Ø32 (10mm narrower than the yoke; ~5mm clearance each side) TL 2276
  grp = ents.add_group
  grp.name = "Acetal guide wheel Ø32 (10mm narrower than the yoke; ~5mm clearance each side) TL 2276"
  ge = grp.entities
  circle = ge.add_circle([124.mm,2276.mm,2361.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(52.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Guide axle Ø10 (in throat) TL 2276
  grp = ents.add_group
  grp.name = "Guide axle Ø10 (in throat) TL 2276"
  ge = grp.entities
  circle = ge.add_circle([117.mm,2276.mm,2361.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(66.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Yoke arm + lip hook (thru opening) TL 117
  grp = ents.add_group
  grp.name = "Yoke arm + lip hook (thru opening) TL 117"
  face = grp.entities.add_face([115.mm,2228.mm,2330.mm], [119.mm,2228.mm,2330.mm], [119.mm,2296.mm,2330.mm], [115.mm,2296.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(31.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Yoke arm + lip hook (thru opening) TL 183
  grp = ents.add_group
  grp.name = "Yoke arm + lip hook (thru opening) TL 183"
  face = grp.entities.add_face([181.mm,2228.mm,2330.mm], [185.mm,2228.mm,2330.mm], [185.mm,2296.mm,2330.mm], [181.mm,2296.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(31.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Yoke cross-piece (joins the two arms) TL
  grp = ents.add_group
  grp.name = "Yoke cross-piece (joins the two arms) TL"
  face = grp.entities.add_face([115.mm,2228.mm,2322.mm], [185.mm,2228.mm,2322.mm], [185.mm,2296.mm,2322.mm], [115.mm,2296.mm,2322.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Yoke rail (→ inboard carriage) TL
  grp = ents.add_group
  grp.name = "Yoke rail (→ inboard carriage) TL"
  face = grp.entities.add_face([183.mm,2228.mm,2324.mm], [208.mm,2228.mm,2324.mm], [208.mm,2296.mm,2324.mm], [183.mm,2296.mm,2324.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (bolted to skate axles) TL
  grp = ents.add_group
  grp.name = "Carriage plate (bolted to skate axles) TL"
  face = grp.entities.add_face([196.mm,2222.mm,2328.mm], [210.mm,2222.mm,2328.mm], [210.mm,2302.mm,2328.mm], [196.mm,2302.mm,2328.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) TL 2232
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) TL 2232"
  ge = grp.entities
  circle = ge.add_circle([202.mm,2232.mm,2339.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) TL 2276
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) TL 2276"
  ge = grp.entities
  circle = ge.add_circle([202.mm,2276.mm,2339.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT, green) TL
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT, green) TL"
  face = grp.entities.add_face([199.mm,2253.mm,2330.mm], [215.mm,2253.mm,2330.mm], [215.mm,2271.mm,2330.mm], [199.mm,2271.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(47.mm)
  mat = model.materials["Vertical Z slide rail (TILT, green) BL"] || model.materials.add("Vertical Z slide rail (TILT, green) BL")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING, purple) TL
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING, purple) TL"
  face = grp.entities.add_face([150.mm,2255.mm,2330.mm], [410.mm,2255.mm,2330.mm], [410.mm,2269.mm,2330.mm], [150.mm,2269.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X slide rail (SWING, purple) BL"] || model.materials.add("Horizontal X slide rail (SWING, purple) BL")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint TL
  grp = ents.add_group
  grp.name = "U-joint TL"
  face = grp.entities.add_face([138.mm,2250.mm,2320.mm], [162.mm,2250.mm,2320.mm], [162.mm,2274.mm,2320.mm], [138.mm,2274.mm,2320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Frame corner bracket (angle frame → U-joint) TL
  grp = ents.add_group
  grp.name = "Frame corner bracket (angle frame → U-joint) TL"
  face = grp.entities.add_face([136.mm,2254.mm,2308.mm], [184.mm,2254.mm,2308.mm], [184.mm,2270.mm,2308.mm], [136.mm,2270.mm,2308.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(52.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (angle frame → bracket) TL
  grp = ents.add_group
  grp.name = "Frame-corner bolt (angle frame → bracket) TL"
  ge = grp.entities
  circle = ge.add_circle([183.mm,2256.mm,2334.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) web TR
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) web TR"
  face = grp.entities.add_face([4586.mm,0.mm,2377.mm], [4662.mm,0.mm,2377.mm], [4662.mm,2362.mm,2377.mm], [4586.mm,2362.mm,2377.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) flange TR 4586
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) flange TR 4586"
  face = grp.entities.add_face([4586.mm,0.mm,2344.mm], [4591.mm,0.mm,2344.mm], [4591.mm,2362.mm,2344.mm], [4586.mm,2362.mm,2344.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) flange TR 4657
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) flange TR 4657"
  face = grp.entities.add_face([4657.mm,0.mm,2344.mm], [4662.mm,0.mm,2344.mm], [4662.mm,2362.mm,2344.mm], [4657.mm,2362.mm,2344.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail end flange (outboard-trimmed) TR 0
  grp = ents.add_group
  grp.name = "Rail end flange (outboard-trimmed) TR 0"
  face = grp.entities.add_face([4569.mm,0.mm,2339.mm], [4644.mm,0.mm,2339.mm], [4644.mm,12.mm,2339.mm], [4569.mm,12.mm,2339.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Rail end flange (outboard-trimmed) TR 2350
  grp = ents.add_group
  grp.name = "Rail end flange (outboard-trimmed) TR 2350"
  face = grp.entities.add_face([4569.mm,2350.mm,2339.mm], [4644.mm,2350.mm,2339.mm], [4644.mm,2362.mm,2339.mm], [4569.mm,2362.mm,2339.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal guide wheel Ø32 (10mm narrower than the yoke; ~5mm clearance each side) TR 2232
  grp = ents.add_group
  grp.name = "Acetal guide wheel Ø32 (10mm narrower than the yoke; ~5mm clearance each side) TR 2232"
  ge = grp.entities
  circle = ge.add_circle([4598.mm,2232.mm,2361.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(52.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Guide axle Ø10 (in throat) TR 2232
  grp = ents.add_group
  grp.name = "Guide axle Ø10 (in throat) TR 2232"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2232.mm,2361.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(66.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal guide wheel Ø32 (10mm narrower than the yoke; ~5mm clearance each side) TR 2276
  grp = ents.add_group
  grp.name = "Acetal guide wheel Ø32 (10mm narrower than the yoke; ~5mm clearance each side) TR 2276"
  ge = grp.entities
  circle = ge.add_circle([4598.mm,2276.mm,2361.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(52.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Guide axle Ø10 (in throat) TR 2276
  grp = ents.add_group
  grp.name = "Guide axle Ø10 (in throat) TR 2276"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2276.mm,2361.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(66.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Yoke arm + lip hook (thru opening) TR 4591
  grp = ents.add_group
  grp.name = "Yoke arm + lip hook (thru opening) TR 4591"
  face = grp.entities.add_face([4589.mm,2228.mm,2330.mm], [4593.mm,2228.mm,2330.mm], [4593.mm,2296.mm,2330.mm], [4589.mm,2296.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(31.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Yoke arm + lip hook (thru opening) TR 4657
  grp = ents.add_group
  grp.name = "Yoke arm + lip hook (thru opening) TR 4657"
  face = grp.entities.add_face([4655.mm,2228.mm,2330.mm], [4659.mm,2228.mm,2330.mm], [4659.mm,2296.mm,2330.mm], [4655.mm,2296.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(31.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Yoke cross-piece (joins the two arms) TR
  grp = ents.add_group
  grp.name = "Yoke cross-piece (joins the two arms) TR"
  face = grp.entities.add_face([4589.mm,2228.mm,2322.mm], [4659.mm,2228.mm,2322.mm], [4659.mm,2296.mm,2322.mm], [4589.mm,2296.mm,2322.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Yoke rail (→ inboard carriage) TR
  grp = ents.add_group
  grp.name = "Yoke rail (→ inboard carriage) TR"
  face = grp.entities.add_face([4572.mm,2228.mm,2324.mm], [4663.mm,2228.mm,2324.mm], [4663.mm,2296.mm,2324.mm], [4572.mm,2296.mm,2324.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (bolted to skate axles) TR
  grp = ents.add_group
  grp.name = "Carriage plate (bolted to skate axles) TR"
  face = grp.entities.add_face([4566.mm,2222.mm,2328.mm], [4580.mm,2222.mm,2328.mm], [4580.mm,2302.mm,2328.mm], [4566.mm,2302.mm,2328.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["Acetal wheel Ø32 (weight) BL 2232"] || model.materials.add("Acetal wheel Ø32 (weight) BL 2232")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) TR 2232
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) TR 2232"
  ge = grp.entities
  circle = ge.add_circle([4572.mm,2232.mm,2339.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) TR 2276
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) TR 2276"
  ge = grp.entities
  circle = ge.add_circle([4572.mm,2276.mm,2339.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT, green) TR
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT, green) TR"
  face = grp.entities.add_face([4569.mm,2253.mm,2330.mm], [4585.mm,2253.mm,2330.mm], [4585.mm,2271.mm,2330.mm], [4569.mm,2271.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(47.mm)
  mat = model.materials["Vertical Z slide rail (TILT, green) BL"] || model.materials.add("Vertical Z slide rail (TILT, green) BL")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING, purple) TR
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING, purple) TR"
  face = grp.entities.add_face([4364.mm,2255.mm,2330.mm], [4624.mm,2255.mm,2330.mm], [4624.mm,2269.mm,2330.mm], [4364.mm,2269.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X slide rail (SWING, purple) BL"] || model.materials.add("Horizontal X slide rail (SWING, purple) BL")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint TR
  grp = ents.add_group
  grp.name = "U-joint TR"
  face = grp.entities.add_face([4612.mm,2250.mm,2320.mm], [4636.mm,2250.mm,2320.mm], [4636.mm,2274.mm,2320.mm], [4612.mm,2274.mm,2320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL"] || model.materials.add("Welded bridge (welded to REMOVABLE, bears on stub, outboard web) BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Frame corner bracket (angle frame → U-joint) TR
  grp = ents.add_group
  grp.name = "Frame corner bracket (angle frame → U-joint) TR"
  face = grp.entities.add_face([4590.mm,2254.mm,2308.mm], [4638.mm,2254.mm,2308.mm], [4638.mm,2270.mm,2308.mm], [4590.mm,2270.mm,2308.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(52.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (angle frame → bracket) TR
  grp = ents.add_group
  grp.name = "Frame-corner bolt (angle frame → bracket) TR"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2256.mm,2334.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Floor
  grp = ents.add_group
  grp.name = "Floor"
  face = grp.entities.add_face([-100.mm,0.mm,-12.mm], [4874.mm,0.mm,-12.mm], [4874.mm,2512.mm,-12.mm], [-100.mm,2512.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Floor"] || model.materials.add("Floor")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.05
  grp.material = mat

  # Ceiling
  grp = ents.add_group
  grp.name = "Ceiling"
  face = grp.entities.add_face([-100.mm,0.mm,2388.mm], [4874.mm,0.mm,2388.mm], [4874.mm,2512.mm,2388.mm], [-100.mm,2512.mm,2388.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Floor"] || model.materials.add("Floor")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.05
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corners"
  inst.layer = model.layers["Corners"]

  # ═══ Film Plane ═══
  defn = model.definitions.add("Film Plane")
  ents = defn.entities
  # Film-plane ACM backing (ghost)
  grp = ents.add_group
  grp.name = "Film-plane ACM backing (ghost)"
  face = grp.entities.add_face([183.mm,2262.mm,160.mm], [4591.mm,2262.mm,160.mm], [4591.mm,2266.mm,160.mm], [183.mm,2266.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2174.mm)
  mat = model.materials["Film-plane ACM backing (ghost)"] || model.materials.add("Film-plane ACM backing (ghost)")
  mat.color = Sketchup::Color.new(31, 59, 102)
  mat.alpha = 0.14
  grp.material = mat

  # Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)
  grp = ents.add_group
  grp.name = "Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)"
  face = grp.entities.add_face([183.mm,2212.mm,2329.mm], [4591.mm,2212.mm,2329.mm], [4591.mm,2262.mm,2329.mm], [183.mm,2262.mm,2329.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)"] || model.materials.add("Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 304 SS angle — top (in-plane leg / ACM seat)
  grp = ents.add_group
  grp.name = "Film frame 2x2 304 SS angle — top (in-plane leg / ACM seat)"
  face = grp.entities.add_face([183.mm,2257.mm,2284.mm], [4591.mm,2257.mm,2284.mm], [4591.mm,2262.mm,2284.mm], [183.mm,2262.mm,2284.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)"] || model.materials.add("Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 304 SS angle — bottom (perp leg / muslin clamp)
  grp = ents.add_group
  grp.name = "Film frame 2x2 304 SS angle — bottom (perp leg / muslin clamp)"
  face = grp.entities.add_face([183.mm,2212.mm,160.mm], [4591.mm,2212.mm,160.mm], [4591.mm,2262.mm,160.mm], [183.mm,2262.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)"] || model.materials.add("Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 304 SS angle — bottom (in-plane leg / ACM seat)
  grp = ents.add_group
  grp.name = "Film frame 2x2 304 SS angle — bottom (in-plane leg / ACM seat)"
  face = grp.entities.add_face([183.mm,2257.mm,160.mm], [4591.mm,2257.mm,160.mm], [4591.mm,2262.mm,160.mm], [183.mm,2262.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)"] || model.materials.add("Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 304 SS angle — left (perp leg / muslin clamp)
  grp = ents.add_group
  grp.name = "Film frame 2x2 304 SS angle — left (perp leg / muslin clamp)"
  face = grp.entities.add_face([183.mm,2212.mm,160.mm], [188.mm,2212.mm,160.mm], [188.mm,2262.mm,160.mm], [183.mm,2262.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2174.mm)
  mat = model.materials["Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)"] || model.materials.add("Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 304 SS angle — left (in-plane leg / ACM seat)
  grp = ents.add_group
  grp.name = "Film frame 2x2 304 SS angle — left (in-plane leg / ACM seat)"
  face = grp.entities.add_face([183.mm,2257.mm,160.mm], [233.mm,2257.mm,160.mm], [233.mm,2262.mm,160.mm], [183.mm,2262.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2174.mm)
  mat = model.materials["Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)"] || model.materials.add("Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 304 SS angle — right (perp leg / muslin clamp)
  grp = ents.add_group
  grp.name = "Film frame 2x2 304 SS angle — right (perp leg / muslin clamp)"
  face = grp.entities.add_face([4586.mm,2212.mm,160.mm], [4591.mm,2212.mm,160.mm], [4591.mm,2262.mm,160.mm], [4586.mm,2262.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2174.mm)
  mat = model.materials["Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)"] || model.materials.add("Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 304 SS angle — right (in-plane leg / ACM seat)
  grp = ents.add_group
  grp.name = "Film frame 2x2 304 SS angle — right (in-plane leg / ACM seat)"
  face = grp.entities.add_face([4541.mm,2257.mm,160.mm], [4591.mm,2257.mm,160.mm], [4591.mm,2262.mm,160.mm], [4541.mm,2262.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2174.mm)
  mat = model.materials["Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)"] || model.materials.add("Film frame 2x2 304 SS angle — top (perp leg / muslin clamp)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film Plane"
  inst.layer = model.layers["Film Plane"]

  # ═══ Pinhole ═══
  defn = model.definitions.add("Pinhole")
  ents = defn.entities
  # Pinhole wall (far)
  grp = ents.add_group
  grp.name = "Pinhole wall (far)"
  face = grp.entities.add_face([0.mm,-14.mm,0.mm], [5893.mm,-14.mm,0.mm], [5893.mm,0.mm,0.mm], [0.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Pinhole wall (far)"] || model.materials.add("Pinhole wall (far)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.06
  grp.material = mat

  # Pinhole aperture
  grp = ents.add_group
  grp.name = "Pinhole aperture"
  face = grp.entities.add_face([2388.mm,-18.mm,1183.mm], [2410.mm,-18.mm,1183.mm], [2410.mm,4.mm,1183.mm], [2388.mm,4.mm,1183.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Pinhole aperture"] || model.materials.add("Pinhole aperture")
  mat.color = Sketchup::Color.new(16, 16, 20)
  mat.alpha = 1.0
  grp.material = mat

  # light cone — pinhole → 4 panel corners
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(183.mm, 2262.mm, 2334.mm))
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(4591.mm, 2262.mm, 2334.mm))
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(183.mm, 2262.mm, 160.mm))
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(4591.mm, 2262.mm, 160.mm))

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Pinhole"
  inst.layer = model.layers["Pinhole"]

  # ═══ Context (walkway + IBC cantilever/beams) ═══
  defn = model.definitions.add("Context (walkway + IBC cantilever/beams)")
  ents = defn.entities
  # Walkway Near (left section)
  grp = ents.add_group
  grp.name = "Walkway Near (left section)"
  face = grp.entities.add_face([470.mm,8.mm,115.mm], [1055.mm,8.mm,115.mm], [1055.mm,300.mm,115.mm], [470.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (widened)
  grp = ents.add_group
  grp.name = "Walkway Near (widened)"
  face = grp.entities.add_face([1055.mm,10.mm,115.mm], [2169.mm,10.mm,115.mm], [2169.mm,500.mm,115.mm], [1055.mm,500.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (right section)
  grp = ents.add_group
  grp.name = "Walkway Near (right section)"
  face = grp.entities.add_face([2169.mm,8.mm,115.mm], [4329.mm,8.mm,115.mm], [4329.mm,300.mm,115.mm], [2169.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far
  grp = ents.add_group
  grp.name = "Walkway Far"
  face = grp.entities.add_face([470.mm,2062.mm,115.mm], [4329.mm,2062.mm,115.mm], [4329.mm,2354.mm,115.mm], [470.mm,2354.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Right (IBC end)
  grp = ents.add_group
  grp.name = "Walkway Right (IBC end)"
  face = grp.entities.add_face([4329.mm,0.mm,115.mm], [4629.mm,0.mm,115.mm], [4629.mm,2362.mm,115.mm], [4329.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left (REMOVABLE — transport)
  grp = ents.add_group
  grp.name = "Walkway Left (REMOVABLE — transport)"
  face = grp.entities.add_face([170.mm,0.mm,115.mm], [470.mm,0.mm,115.mm], [470.mm,2362.mm,115.mm], [170.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Left (REMOVABLE — transport)"] || model.materials.add("Walkway Left (REMOVABLE — transport)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left punch-out (drum exit)
  grp = ents.add_group
  grp.name = "Walkway Left punch-out (drum exit)"
  face = grp.entities.add_face([470.mm,800.mm,115.mm], [770.mm,800.mm,115.mm], [770.mm,1560.mm,115.mm], [470.mm,1560.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Left (REMOVABLE — transport)"] || model.materials.add("Walkway Left (REMOVABLE — transport)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 plate"
  face = grp.entities.add_face([638.mm,0.mm,0.mm], [758.mm,0.mm,0.mm], [758.mm,8.mm,0.mm], [638.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([698.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([663.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([733.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 arm"
  face = grp.entities.add_face([694.mm,8.mm,105.mm], [702.mm,8.mm,105.mm], [702.mm,300.mm,105.mm], [694.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 gusset"
  ge = grp.entities
  f = ge.add_face([694.mm,8.mm,0.mm], [694.mm,8.mm,105.mm], [694.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) plate"
  face = grp.entities.add_face([1095.mm,0.mm,0.mm], [1215.mm,0.mm,0.mm], [1215.mm,10.mm,0.mm], [1095.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1120.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1190.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1120.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1190.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) arm"
  face = grp.entities.add_face([1150.mm,10.mm,103.mm], [1160.mm,10.mm,103.mm], [1160.mm,500.mm,103.mm], [1150.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1150.mm,10.mm,0.mm], [1150.mm,10.mm,103.mm], [1150.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) plate"
  face = grp.entities.add_face([1552.mm,0.mm,0.mm], [1672.mm,0.mm,0.mm], [1672.mm,10.mm,0.mm], [1552.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1577.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1647.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1577.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1647.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) arm"
  face = grp.entities.add_face([1607.mm,10.mm,103.mm], [1617.mm,10.mm,103.mm], [1617.mm,500.mm,103.mm], [1607.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1607.mm,10.mm,0.mm], [1607.mm,10.mm,103.mm], [1607.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) plate"
  face = grp.entities.add_face([2009.mm,0.mm,0.mm], [2129.mm,0.mm,0.mm], [2129.mm,10.mm,0.mm], [2009.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2034.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2104.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2034.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2104.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) arm"
  face = grp.entities.add_face([2064.mm,10.mm,103.mm], [2074.mm,10.mm,103.mm], [2074.mm,500.mm,103.mm], [2064.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2064.mm,10.mm,0.mm], [2064.mm,10.mm,103.mm], [2064.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 plate"
  face = grp.entities.add_face([2466.mm,0.mm,0.mm], [2586.mm,0.mm,0.mm], [2586.mm,8.mm,0.mm], [2466.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2526.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2491.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2561.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 arm"
  face = grp.entities.add_face([2522.mm,8.mm,105.mm], [2530.mm,8.mm,105.mm], [2530.mm,300.mm,105.mm], [2522.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 gusset"
  ge = grp.entities
  f = ge.add_face([2522.mm,8.mm,0.mm], [2522.mm,8.mm,105.mm], [2522.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 plate"
  face = grp.entities.add_face([2923.mm,0.mm,0.mm], [3043.mm,0.mm,0.mm], [3043.mm,8.mm,0.mm], [2923.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2983.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2948.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3018.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 arm"
  face = grp.entities.add_face([2979.mm,8.mm,105.mm], [2987.mm,8.mm,105.mm], [2987.mm,300.mm,105.mm], [2979.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 gusset"
  ge = grp.entities
  f = ge.add_face([2979.mm,8.mm,0.mm], [2979.mm,8.mm,105.mm], [2979.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 plate"
  face = grp.entities.add_face([3380.mm,0.mm,0.mm], [3500.mm,0.mm,0.mm], [3500.mm,8.mm,0.mm], [3380.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3440.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3405.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3475.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 arm"
  face = grp.entities.add_face([3436.mm,8.mm,105.mm], [3444.mm,8.mm,105.mm], [3444.mm,300.mm,105.mm], [3436.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 gusset"
  ge = grp.entities
  f = ge.add_face([3436.mm,8.mm,0.mm], [3436.mm,8.mm,105.mm], [3436.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 plate"
  face = grp.entities.add_face([3837.mm,0.mm,0.mm], [3957.mm,0.mm,0.mm], [3957.mm,8.mm,0.mm], [3837.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3897.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3862.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3932.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 arm"
  face = grp.entities.add_face([3893.mm,8.mm,105.mm], [3901.mm,8.mm,105.mm], [3901.mm,300.mm,105.mm], [3893.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 gusset"
  ge = grp.entities
  f = ge.add_face([3893.mm,8.mm,0.mm], [3893.mm,8.mm,105.mm], [3893.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 plate"
  face = grp.entities.add_face([638.mm,2354.mm,0.mm], [758.mm,2354.mm,0.mm], [758.mm,2362.mm,0.mm], [638.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([698.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([663.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([733.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 arm"
  face = grp.entities.add_face([694.mm,2062.mm,105.mm], [702.mm,2062.mm,105.mm], [702.mm,2354.mm,105.mm], [694.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 gusset"
  ge = grp.entities
  f = ge.add_face([694.mm,2354.mm,0.mm], [694.mm,2354.mm,105.mm], [694.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 plate"
  face = grp.entities.add_face([1095.mm,2354.mm,0.mm], [1215.mm,2354.mm,0.mm], [1215.mm,2362.mm,0.mm], [1095.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1155.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1120.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1190.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 arm"
  face = grp.entities.add_face([1151.mm,2062.mm,105.mm], [1159.mm,2062.mm,105.mm], [1159.mm,2354.mm,105.mm], [1151.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 gusset"
  ge = grp.entities
  f = ge.add_face([1151.mm,2354.mm,0.mm], [1151.mm,2354.mm,105.mm], [1151.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 plate"
  face = grp.entities.add_face([1552.mm,2354.mm,0.mm], [1672.mm,2354.mm,0.mm], [1672.mm,2362.mm,0.mm], [1552.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1612.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1577.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1647.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 arm"
  face = grp.entities.add_face([1608.mm,2062.mm,105.mm], [1616.mm,2062.mm,105.mm], [1616.mm,2354.mm,105.mm], [1608.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 gusset"
  ge = grp.entities
  f = ge.add_face([1608.mm,2354.mm,0.mm], [1608.mm,2354.mm,105.mm], [1608.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 plate"
  face = grp.entities.add_face([2009.mm,2354.mm,0.mm], [2129.mm,2354.mm,0.mm], [2129.mm,2362.mm,0.mm], [2009.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2069.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2034.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2104.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 arm"
  face = grp.entities.add_face([2065.mm,2062.mm,105.mm], [2073.mm,2062.mm,105.mm], [2073.mm,2354.mm,105.mm], [2065.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 gusset"
  ge = grp.entities
  f = ge.add_face([2065.mm,2354.mm,0.mm], [2065.mm,2354.mm,105.mm], [2065.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 plate"
  face = grp.entities.add_face([2466.mm,2354.mm,0.mm], [2586.mm,2354.mm,0.mm], [2586.mm,2362.mm,0.mm], [2466.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2526.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2491.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2561.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 arm"
  face = grp.entities.add_face([2522.mm,2062.mm,105.mm], [2530.mm,2062.mm,105.mm], [2530.mm,2354.mm,105.mm], [2522.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 gusset"
  ge = grp.entities
  f = ge.add_face([2522.mm,2354.mm,0.mm], [2522.mm,2354.mm,105.mm], [2522.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 plate"
  face = grp.entities.add_face([2923.mm,2354.mm,0.mm], [3043.mm,2354.mm,0.mm], [3043.mm,2362.mm,0.mm], [2923.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2983.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2948.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3018.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 arm"
  face = grp.entities.add_face([2979.mm,2062.mm,105.mm], [2987.mm,2062.mm,105.mm], [2987.mm,2354.mm,105.mm], [2979.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 gusset"
  ge = grp.entities
  f = ge.add_face([2979.mm,2354.mm,0.mm], [2979.mm,2354.mm,105.mm], [2979.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 plate"
  face = grp.entities.add_face([3380.mm,2354.mm,0.mm], [3500.mm,2354.mm,0.mm], [3500.mm,2362.mm,0.mm], [3380.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3440.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3405.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3475.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 arm"
  face = grp.entities.add_face([3436.mm,2062.mm,105.mm], [3444.mm,2062.mm,105.mm], [3444.mm,2354.mm,105.mm], [3436.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 gusset"
  ge = grp.entities
  f = ge.add_face([3436.mm,2354.mm,0.mm], [3436.mm,2354.mm,105.mm], [3436.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 plate"
  face = grp.entities.add_face([3837.mm,2354.mm,0.mm], [3957.mm,2354.mm,0.mm], [3957.mm,2362.mm,0.mm], [3837.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3897.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3862.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3932.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 arm"
  face = grp.entities.add_face([3893.mm,2062.mm,105.mm], [3901.mm,2062.mm,105.mm], [3901.mm,2354.mm,105.mm], [3893.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 gusset"
  ge = grp.entities
  f = ge.add_face([3893.mm,2354.mm,0.mm], [3893.mm,2354.mm,105.mm], [3893.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 1 foot plate"
  face = grp.entities.add_face([38.mm,220.mm,0.mm], [166.mm,220.mm,0.mm], [166.mm,280.mm,0.mm], [38.mm,280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 1 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,220.mm,0.mm], [165.mm,220.mm,0.mm], [165.mm,280.mm,0.mm], [115.mm,280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 arm (to X470)
  grp = ents.add_group
  grp.name = "Left cantilever 1 arm (to X470)"
  face = grp.entities.add_face([165.mm,230.mm,75.mm], [470.mm,230.mm,75.mm], [470.mm,270.mm,75.mm], [165.mm,270.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 2 foot plate"
  face = grp.entities.add_face([38.mm,770.mm,0.mm], [166.mm,770.mm,0.mm], [166.mm,830.mm,0.mm], [38.mm,830.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 2 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,770.mm,0.mm], [165.mm,770.mm,0.mm], [165.mm,830.mm,0.mm], [115.mm,830.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 2 arm (to X770)"
  face = grp.entities.add_face([165.mm,770.mm,75.mm], [770.mm,770.mm,75.mm], [770.mm,830.mm,75.mm], [165.mm,830.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 3 foot plate"
  face = grp.entities.add_face([38.mm,1150.mm,0.mm], [166.mm,1150.mm,0.mm], [166.mm,1210.mm,0.mm], [38.mm,1210.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 3 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,1150.mm,0.mm], [165.mm,1150.mm,0.mm], [165.mm,1210.mm,0.mm], [115.mm,1210.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 3 arm (to X770)"
  face = grp.entities.add_face([165.mm,1150.mm,75.mm], [770.mm,1150.mm,75.mm], [770.mm,1210.mm,75.mm], [165.mm,1210.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 4 foot plate"
  face = grp.entities.add_face([38.mm,1530.mm,0.mm], [166.mm,1530.mm,0.mm], [166.mm,1590.mm,0.mm], [38.mm,1590.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 4 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,1530.mm,0.mm], [165.mm,1530.mm,0.mm], [165.mm,1590.mm,0.mm], [115.mm,1590.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 4 arm (to X770)"
  face = grp.entities.add_face([165.mm,1530.mm,75.mm], [770.mm,1530.mm,75.mm], [770.mm,1590.mm,75.mm], [165.mm,1590.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 5 foot plate"
  face = grp.entities.add_face([38.mm,2080.mm,0.mm], [166.mm,2080.mm,0.mm], [166.mm,2140.mm,0.mm], [38.mm,2140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 5 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,2080.mm,0.mm], [165.mm,2080.mm,0.mm], [165.mm,2140.mm,0.mm], [115.mm,2140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 arm (to X470)
  grp = ents.add_group
  grp.name = "Left cantilever 5 arm (to X470)"
  face = grp.entities.add_face([165.mm,2090.mm,75.mm], [470.mm,2090.mm,75.mm], [470.mm,2130.mm,75.mm], [165.mm,2130.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner plate (near)"
  face = grp.entities.add_face([4574.mm,0.mm,58.mm], [4724.mm,0.mm,58.mm], [4724.mm,10.mm,58.mm], [4574.mm,10.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(177.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (near)"
  face = grp.entities.add_face([4574.mm,-50.mm,58.mm], [4724.mm,-50.mm,58.mm], [4724.mm,-40.mm,58.mm], [4574.mm,-40.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(177.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (near)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (near)"
  face = grp.entities.add_face([4574.mm,0.mm,58.mm], [4724.mm,0.mm,58.mm], [4724.mm,55.mm,58.mm], [4574.mm,55.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (near)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (near)"
  face = grp.entities.add_face([4619.mm,0.mm,148.mm], [4679.mm,0.mm,148.mm], [4679.mm,55.mm,148.mm], [4619.mm,55.mm,148.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4599 Z84
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4599 Z84"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,-50.mm,84.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4599 Z188
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4599 Z188"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,-50.mm,188.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4699 Z84
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4699 Z84"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,-50.mm,84.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4699 Z188
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4699 Z188"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,-50.mm,188.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner plate (far)
  grp = ents.add_group
  grp.name = "FP combined corner plate (far)"
  face = grp.entities.add_face([4574.mm,2352.mm,58.mm], [4724.mm,2352.mm,58.mm], [4724.mm,2362.mm,58.mm], [4574.mm,2362.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(177.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (far)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (far)"
  face = grp.entities.add_face([4574.mm,2402.mm,58.mm], [4724.mm,2402.mm,58.mm], [4724.mm,2412.mm,58.mm], [4574.mm,2412.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(177.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (far)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (far)"
  face = grp.entities.add_face([4574.mm,2307.mm,58.mm], [4724.mm,2307.mm,58.mm], [4724.mm,2362.mm,58.mm], [4574.mm,2362.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (far)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (far)"
  face = grp.entities.add_face([4619.mm,2307.mm,148.mm], [4679.mm,2307.mm,148.mm], [4679.mm,2362.mm,148.mm], [4619.mm,2362.mm,148.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4599 Z84
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4599 Z84"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,2352.mm,84.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4599 Z188
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4599 Z188"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,2352.mm,188.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4699 Z84
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4699 Z84"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,2352.mm,84.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4699 Z188
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4699 Z188"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,2352.mm,188.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([4654.mm,1046.mm,0.mm], [4704.mm,1046.mm,0.mm], [4704.mm,1096.mm,0.mm], [4654.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([4654.mm,1266.mm,0.mm], [4704.mm,1266.mm,0.mm], [4704.mm,1316.mm,0.mm], [4654.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([5104.mm,1046.mm,0.mm], [5154.mm,1046.mm,0.mm], [5154.mm,1096.mm,0.mm], [5104.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([5104.mm,1266.mm,0.mm], [5154.mm,1266.mm,0.mm], [5154.mm,1316.mm,0.mm], [5104.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([4654.mm,1096.mm,0.mm], [4704.mm,1096.mm,0.mm], [4704.mm,1266.mm,0.mm], [4654.mm,1266.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([5104.mm,1096.mm,0.mm], [5154.mm,1096.mm,0.mm], [5154.mm,1266.mm,0.mm], [5104.mm,1266.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1046.mm,0.mm], [5104.mm,1046.mm,0.mm], [5104.mm,1096.mm,0.mm], [4704.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1266.mm,0.mm], [5104.mm,1266.mm,0.mm], [5104.mm,1316.mm,0.mm], [4704.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([4654.mm,1096.mm,2246.mm], [4704.mm,1096.mm,2246.mm], [4704.mm,1266.mm,2246.mm], [4654.mm,1266.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([5104.mm,1096.mm,2246.mm], [5154.mm,1096.mm,2246.mm], [5154.mm,1266.mm,2246.mm], [5104.mm,1266.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1046.mm,2246.mm], [5104.mm,1046.mm,2246.mm], [5104.mm,1096.mm,2246.mm], [4704.mm,1096.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1266.mm,2246.mm], [5104.mm,1266.mm,2246.mm], [5104.mm,1316.mm,2246.mm], [4704.mm,1316.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([4604.mm,996.mm,0.mm], [4754.mm,996.mm,0.mm], [4754.mm,1146.mm,0.mm], [4604.mm,1146.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([4604.mm,1216.mm,0.mm], [4754.mm,1216.mm,0.mm], [4754.mm,1366.mm,0.mm], [4604.mm,1366.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([5054.mm,996.mm,0.mm], [5204.mm,996.mm,0.mm], [5204.mm,1146.mm,0.mm], [5054.mm,1146.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([5054.mm,1216.mm,0.mm], [5204.mm,1216.mm,0.mm], [5204.mm,1366.mm,0.mm], [5054.mm,1366.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.mm,90.mm], [5152.mm,1096.mm,90.mm], [5152.mm,1136.mm,90.mm], [5122.mm,1136.mm,90.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.mm,1118.mm], [5152.mm,1096.mm,1118.mm], [5152.mm,1136.mm,1118.mm], [5122.mm,1136.mm,1118.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.mm,2146.mm], [5152.mm,1096.mm,2146.mm], [5152.mm,1136.mm,2146.mm], [5122.mm,1136.mm,2146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1226.mm,90.mm], [5152.mm,1226.mm,90.mm], [5152.mm,1266.mm,90.mm], [5122.mm,1266.mm,90.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1226.mm,1118.mm], [5152.mm,1226.mm,1118.mm], [5152.mm,1266.mm,1118.mm], [5122.mm,1266.mm,1118.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1226.mm,2146.mm], [5152.mm,1226.mm,2146.mm], [5152.mm,1266.mm,2146.mm], [5122.mm,1266.mm,2146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,0.mm,560.mm], [4674.mm,0.mm,560.mm], [4674.mm,1096.mm,560.mm], [4654.mm,1096.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,0.mm,1760.mm], [4674.mm,0.mm,1760.mm], [4674.mm,1096.mm,1760.mm], [4654.mm,1096.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,1266.mm,560.mm], [4674.mm,1266.mm,560.mm], [4674.mm,2362.mm,560.mm], [4654.mm,2362.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,1266.mm,1760.mm], [4674.mm,1266.mm,1760.mm], [4674.mm,2362.mm,1760.mm], [4654.mm,2362.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,520.mm,585.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,520.mm,1785.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,940.mm,585.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,940.mm,1785.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1422.mm,585.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1422.mm,1785.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1842.mm,585.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1842.mm,1785.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,0.mm,530.mm], [4712.mm,0.mm,530.mm], [4712.mm,4.mm,530.mm], [4646.mm,4.mm,530.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,0.mm,556.mm], [4708.mm,0.mm,556.mm], [4708.mm,70.mm,556.mm], [4650.mm,70.mm,556.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,-48.mm,517.5.mm], [4729.mm,-48.mm,517.5.mm], [4729.mm,-40.mm,517.5.mm], [4629.mm,-40.mm,517.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,-48.mm,539.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,-48.mm,630.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,-48.mm,539.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,-48.mm,630.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,0.mm,1730.mm], [4712.mm,0.mm,1730.mm], [4712.mm,4.mm,1730.mm], [4646.mm,4.mm,1730.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,0.mm,1756.mm], [4708.mm,0.mm,1756.mm], [4708.mm,70.mm,1756.mm], [4650.mm,70.mm,1756.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,-48.mm,1717.5.mm], [4729.mm,-48.mm,1717.5.mm], [4729.mm,-40.mm,1717.5.mm], [4629.mm,-40.mm,1717.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,-48.mm,1739.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,-48.mm,1830.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,-48.mm,1739.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,-48.mm,1830.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,2358.mm,530.mm], [4712.mm,2358.mm,530.mm], [4712.mm,2362.mm,530.mm], [4646.mm,2362.mm,530.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,2292.mm,556.mm], [4708.mm,2292.mm,556.mm], [4708.mm,2362.mm,556.mm], [4650.mm,2362.mm,556.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,2402.mm,517.5.mm], [4729.mm,2402.mm,517.5.mm], [4729.mm,2410.mm,517.5.mm], [4629.mm,2410.mm,517.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,2352.mm,539.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,2352.mm,630.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,2352.mm,539.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,2352.mm,630.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,2358.mm,1730.mm], [4712.mm,2358.mm,1730.mm], [4712.mm,2362.mm,1730.mm], [4646.mm,2362.mm,1730.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,2292.mm,1756.mm], [4708.mm,2292.mm,1756.mm], [4708.mm,2362.mm,1756.mm], [4650.mm,2362.mm,1756.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,2402.mm,1717.5.mm], [4729.mm,2402.mm,1717.5.mm], [4729.mm,2410.mm,1717.5.mm], [4629.mm,2410.mm,1717.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["U-rail STUB (fixed, parks corner) web BL"] || model.materials.add("U-rail STUB (fixed, parks corner) web BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,2352.mm,1739.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,2352.mm,1830.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,2352.mm,1739.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,2352.mm,1830.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Context (walkway + IBC cantilever/beams)"
  inst.layer = model.layers["Context"]


# ── "Labeled" callouts (Labels tag) ──

tt = entities.add_text("PINHOLE (far wall) — the film plane faces it across the throw", Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Vector3d.new(60.mm, -50.mm, 30.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Film plane 4408.0 x 2174 (edges seated in the carriers; bottom @Z160 above walkway, weight on the bottom rail; top = light guide only)", Geom::Point3d.new(2400.mm, 2262.mm, 1194.mm), Geom::Vector3d.new(60.mm, 45.mm, 20.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("TOP pair vs BOTTOM pair depth = TILT", Geom::Point3d.new(150.mm, 2262.mm, 2388.mm), Geom::Vector3d.new(-60.mm, -40.mm, 30.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("LEFT pair vs RIGHT pair depth = SWING", Geom::Point3d.new(4624.mm, 2262.mm, 160.mm), Geom::Vector3d.new(60.mm, 40.mm, -20.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("UPPER rails (ceiling) — TOP corners hang (tension)", Geom::Point3d.new(2400.mm, 1912.mm, 2388.mm), Geom::Vector3d.new(45.mm, -40.mm, 12.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("LOWER rails (floor) — BOTTOM corners bear (compression)", Geom::Point3d.new(2400.mm, 1912.mm, 0.mm), Geom::Vector3d.new(45.mm, -40.mm, -12.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("DEPTH slide (Y, GREY) — drives tilt + swing", Geom::Point3d.new(150.mm, 1962.mm, 120.mm), Geom::Vector3d.new(-55.mm, -40.mm, -10.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("VERTICAL slide (Z, GREEN) — absorbs TILT", Geom::Point3d.new(120.mm, 2262.mm, 180.mm), Geom::Vector3d.new(-60.mm, -40.mm, 10.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("HORIZONTAL slide (X, PURPLE) — absorbs SWING", Geom::Point3d.new(270.mm, 2262.mm, 170.mm), Geom::Vector3d.new(55.mm, -40.mm, 5.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("U-joint (tilt + swing, twist locked)", Geom::Point3d.new(150.mm, 2250.mm, 160.mm), Geom::Vector3d.new(-55.mm, -45.mm, 15.mm))
tt.layer = model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

model.definitions.purge_unused
model.materials.purge_unused

keep_tags = ["Corners", "Film Plane", "Pinhole", "Context", "Labels"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

# ── iso scenes (Overview [with context] / Corner detail) ──
[["Overview", ["Corners", "Film Plane", "Pinhole", "Context"], [2400.mm, 1562.mm, 1194.mm, 9500.mm]], ["Corner detail", ["Corners", "Film Plane", "Pinhole"], [150.mm, 2262.mm, 190.mm, 620.mm]]].each { |name, tags, tgt|
  model.layers.each { |l| l.visible = (l == default_layer || tags.include?(l.name)) }
  t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
  cdir = Geom::Vector3d.new(0.5, -0.7, 0.4); cdir.normalize!
  model.active_view.camera = Sketchup::Camera.new(t.offset(cdir, tgt[3]), t, Z_AXIS)
  page = model.pages.add(name)
  page.use_camera = true
}

# ── Tilt (side) — look along +X at the left edge: depth (Y) horizontal, height (Z) vertical ──
model.layers.each { |l| l.visible = (l == default_layer || ["Corners", "Film Plane", "Pinhole"].include?(l.name)) }
tc = Geom::Point3d.new(150.mm, 2262.mm, 1194.mm)
te = Geom::Point3d.new(-4050.mm, 2262.mm, 1194.mm)
model.active_view.camera = Sketchup::Camera.new(te, tc, Z_AXIS)
ps = model.pages.add("Tilt (side)"); ps.use_camera = true

# ── Swing (top) — top-down over the pinhole→panel span: width (X) and depth (Y) ──
sc = Geom::Point3d.new(2399.mm, 1131.mm, 0)
se = Geom::Point3d.new(2399.mm, 1131.mm, 9500.mm)
model.active_view.camera = Sketchup::Camera.new(se, sc, Y_AXIS)
ps2 = model.pages.add("Swing (top)"); ps2.use_camera = true

# ── Labeled (Labels tag) — LAST scene ──
model.layers.each { |l| l.visible = (l == default_layer || ["Corners", "Film Plane", "Pinhole", "Labels"].include?(l.name)) }
lc = Geom::Point3d.new(2400.mm, 1862.mm, 1194.mm)
ldir = Geom::Vector3d.new(0.5, -0.7, 0.4); ldir.normalize!
model.active_view.camera = Sketchup::Camera.new(lc.offset(ldir, 7200.mm), lc, Z_AXIS)
pl = model.pages.add("Labeled"); pl.use_camera = true

model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "Film-Plane Corner Mechanism",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
